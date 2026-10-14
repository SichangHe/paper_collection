                                        Fast Collection Operations from Indexed Stream Fusion
                                        Indexed Iterators for Everyone

                                        SCOTT KOVACH, Stanford University, USA
                                        PRANEETH KOLICHALA, Stanford University, USA
                                        KYLE A. MILLER, University of California, Santa Cruz, USA
                                        DAVID BROMAN, KTH Royal Institute of Technology, Sweden and Stanford University, USA
                                        FREDRIK KJOLSTAD, Stanford University, USA
arXiv:2507.06456v1 [cs.PL] 8 Jul 2025




                                        We present a system of efficient methods for traversing and combining associative collection data structures.
                                        A distinguishing feature of the system is that, like traditional sequential iterator libraries, it does not require
                                        specialized compiler infrastructure or staged compilation for efficiency and composability. By using a rep-
                                        resentation based on indexed streams, the library can express complex joins over input collections while
                                        using no intermediate allocations. We implement the library for the Lean, Morphic, and Rust programming
                                        languages and provide a mechanized proof of functional correctness in Lean.

                                        1   INTRODUCTION
                                        Many contemporary programming languages include an iterator interface that provides a uniform
                                        way of sequentially traversing any data type that implements it. This approach powers the for-loop
                                        syntax available in Python, Javascript, Rust, and many other popular languages. Some standard
                                        libraries additionally provide combinators such as map, filter, fold, and zip to combine and transform
                                        iterators. Compilers can leverage deforestation techniques such as stream fusion [7, 11, 30, 31] to
                                        dramatically improve the performance of such programs by eliminating redundant traversals and
                                        memory allocations.
                                           Similar combinators can be defined for data structures that represent associative arrays, which
                                        encode finite maps from keys to values. However, performance trade-offs arise when using these
                                        combinators as they are traditionally defined. We can see this with a simple example task: given a set
                                        (s : Set k) and a map (m : Map k v), find the set of keys that are present in s and associated with
                                        a value v in m that satisfies v > 10. Consider the following API for sets and maps in the functional
                                        language Lean [22] and three natural ways of implementing the program:
                                             lookup    : Map k v → k → Option v
                                             contains : Set k    → k → Bool
                                             select    : Map k v → (k → v → Bool) → Set k
                                             filter    : Set k   → (k → Bool) → Set k
                                             intersect : Set k   → Set k → Set k

                                             variable (s : Set k) (m : Map k v)
                                             -- three equivalent programs:
                                             def p1 := intersect s (select m (fun _ v => v > 10))
                                             def p2 := select m (fun k v => v > 10 && contains s k)
                                             def p3 := filter s (fun k => case lookup m k of
                                                                 | None => False
                                                                 | Just v => v > 10)
                                          In the definition p1, we filter m before intersecting it with s. This uses a potentially optimized
                                        function intersect for intersecting sets, but comes at the cost of reifying the filtered version of
                                        Authors’ addresses: Scott Kovach, Stanford University, USA, dskovach@stanford.edu; Praneeth Kolichala, Stanford Uni-
                                        versity, USA, pkolich@stanford.edu; Kyle A. Miller, University of California, Santa Cruz, USA, kymiller@ucsc.edu; David
                                        Broman, KTH Royal Institute of Technology, Sweden and and Stanford University, USA, dbro@kth.se; Fredrik Kjolstad,
                                        Stanford University, USA, kjolstad@stanford.edu.
2                                                                                           Kovach et al.


m as a set and traversing it twice. The other two programs are manually fused: they combine all
operations within one traversal. In p2, we traverse m while using contains to query s, and in p3, we
traverse s while using lookup to query m.
   Although p2 and p3 avoid the unnecessary memory allocations of p1, they have different perfor-
mance depending on the relative sizes of s and m. Identifying the superior choice may be difficult to
do statically or require runtime size checks that grow more complex for larger examples. Although
p1 is more modular, achieving fusion seems to require either implementations of intersect for all
pairs of data structures, or restriction to a single data structure for collections. The latter approach
is often made internally within software such as database engines, but is awkward for general
purpose programs. This situation suggests that a desirable interface is missing.
   In this work, we propose such an interface and implement it within three general purpose
languages (Lean [22], Rust [20], and Morphic [5]). Our methods achieve fusion by internally using
a data structure based on indexed streams [16]. Our key contribution is a fold function for indexed
streams that can be ported and reliably optimized by general purpose language compilers capable of
specialization. This function elegantly ties together the essential components of an iterator library:
methods to define iterators for new data types, methods for transforming and combining iterators,
and methods for collecting the values of an iterator into a concrete data structure of the user’s
choice. We design and implement (for each language) these library components using an interface
that is only mildly more complex than traditional iterators, while enabling asymptotic speedups in
computation time and greater expressiveness.
   In addition to performance benefits, the small set of data concepts used in the library simplify
the programming experience. All underying data structures are wrapped in a Map-like type that
we denote (k →𝑠 v). Notationally, this emphasizes that a structure maps keys to values, just as
a function does. Sets are represented with the type k →𝑠 Bool, and hierarchical data structure
types are akin to curried functions: k1 →𝑠 k2 →𝑠 v. We give several examples later to clarify and
demonstrate the expressiveness of the library API. Here, we show that intersect and select can
be defined in terms of two more primitive API functions:
    -- new API:
    map     : (k → a → b) → (k →𝑠 a) → (k →𝑠 b)
    zipWith : (a → b → c) → (k →𝑠 a) → (k →𝑠 b) → (k →𝑠 c)

    variable (s1 s2 : k →𝑠 Bool) (m : k →𝑠 v)
    intersect s1 s2 := zipWith (fun x y => x && y) s1 s2
    select m f := map f m
    def p1 := intersect s (select m (fun _ v => v > 10))
  Thus, p1, written exactly as before, encodes an algorithm that is fused (the use of map and zipWith
does not allocate or perform extra traversals), and that achieves worst-case optimal performance [23]
no matter which argument is smaller. Moreover, if its continuation is another stream operation, it
avoids allocating the unnecessary Set that all three previous programs would allocate.
  Our contributions:
     • An indexed stream fold method that simplifies and generalizes previous approaches to
       compiling indexed streams that avoid intermediate memory allocations.
     • A design for the interfaces and methods needed to embed this in a practical library for
       working with associative container types (implemented in Lean, Morphic, and Rust).
     • Computer-checked proofs of correctness for the Lean library.
  As evaluation, we demonstrate that the generality of the approach does not introduce a detri-
mental performance overhead by comparing stream-based programs to idiomatic baselines in each
language. Additionally, we give proofs of correctness for the Lean library itself, not an abstract
Fast Collection Operations                                                                             3


substitute model. Thus, if we include the Lean compiler in our trusted codebase, we have a proof of
correctness for the core stream operations themselves, which gives users seeking to develop high
performance, formally verified applications a strong starting point.

2   OVERVIEW
The paper shows how to implement a shallowly embedded library, meaning it does not require
a domain-specific compiler infrastructure, for operations on associative arrays based on indexed
streams. The library is expressive (programs syntactically resemble high level queries), has high
performance (matching the runtime of hand written programs), enables seamless composition of
queries and other application code (does not rely on deep embedding), and is based on rigorous
principles (simple composition principles and a correctness proof in Lean).
   Our approach rests on a novel formulation of the indexed stream fold function, which subsumes
previous compilation algorithms. The design is portable to multiple host languages, which we
demonstrate with implementations for Lean, Rust, and Morphic. In the following sections, we
describe the approach from three points of view: the library’s external user-facing interface, the
internal interface for extending the library with new operators and data structures, and the interface
with the host language that we rely on for good performance. These correspond to three types of
user: a programmer using one of the stream libraries, a programmer extending the library, or a
programmer porting the stream library concept to a new language.

   Outer Interface. In Section 3, we define the high-level stream operators used in our library to
express queries. These operators suffice for defining relational queries built using joins, aggregates,
functional predicates, and more. We also provide traditional array programming operators such
as map, zipWith, and fold. The library is suitable for high-performance computation involving
high-dimensional associative arrays, regardless of what they represent (tensors, graphs, tables, . . . )
or what data structures are used to represent them (trees, arrays, hash maps, function closures, . . . ,
or mixtures of these).

   Inner Interface. In Section 4.1, we describe one way of realizing indexed streams as a data type
composed of ordinary functions in Lean. In Section 4.2, we describe the suitability of the stream
abstraction for several concrete data types. Finally, in Section 4.3 we discuss the design of the stream
fold function and associated interfaces. We introduce a method of constructing heterogeneous data
structures for hierarchical maps out of complex stream expressions.

   Host Language Interface. In Section 5, we introduce some details from our implementations
written in Lean, Rust, and Morphic. We explain the data representation choices that enable spe-
cialization in each language. We discuss how our high performance goal, which demands minimal
copying and memory allocation, can be achieved even in Lean and Morphic, which are functional
languages with pure semantics.
   Until Section 5, all of our code examples will be taken from the Lean version of the library.

3   LIBRARY INTERFACE DESIGN
Our library API design is motivated by the insight that many common manipulations of collection
data types can be more elegantly and efficiently expressed using functions that operate on the
collections as a whole. These operations allows us to abstract away particular data structures,
instead treating them uniformly as associative arrays. An associative array associates finitely many
elements of a key type 𝑘 with elements of its value type 𝑣. Put another way, it represents a function
of type 𝑘 → 𝑣 that returns a default value if the key is not present, while also allowing values
4                                                                                              Kovach et al.


           -- We use right-associative notation ′ →𝑠 ′ for the Stream type.
           -- It takes two type parameters representing key and value types.
           infixr " →𝑠 " => Stream

           -- (1) Stream construction.
           repeat : v → (k →𝑠 v)
           range   : (lo : Int) → (hi : Int) → (Int →𝑠 Int)
           -- Various data structure-specific iterators omitted; see 4.2.

           -- (2) Core combinator methods.
           map     : (f : k → a → b) → (k →𝑠 a) → (k →𝑠 b)
           zipWith : (f : a → b → c) → (k →𝑠 a) → (k →𝑠 b) → (k →𝑠 c)
           filter : (f : v → Bool) → (k →𝑠 v) → (k →𝑠 v)
           -- Arithmetic operators defined in terms of zipWith and fold.
           mul     : [Mul v] → (k →𝑠 v) → (k →𝑠 v) → (k →𝑠 v)
           sum     : [Add v] → (k →𝑠 v) → v

           -- (3) Core methods for accumulating the values of a stream into a collection.
           fold    : (m → k → v → m) → (k →𝑠 v) → m → m
           eval    : [OfStream v v′ ] → v → v′ → v′ -- discussed in Section 4.3
           memo    : [OfStream a b] → [ToStream b c] → a → c

      Fig. 1. A type-level summary of our methods for stream iteration, combination, and accumulation.

to be inserted and updated by key. In the remainder, the term “array” will generally refer to an
associative array. In this section, we summarize the API and discuss nested collections.

3.1     API Summary
An iteration library needs to have three basic parts: methods to turn data structures into streams,
methods to transform and combine streams, and methods to turn the stream back into a data
structure. The API described in Figure 1 presents a subset of the methods made available by our
library for these purposes. We refer to the transformation/combination methods in particular as
combinators. The choice of combinators is inspired by prior work demonstrating that a large number
of data processing tasks boil down to three categories:
       • applying a functional transformation to a single data collection (map, filter),
       • joining two or more collections (zipWith, mul), and
       • aggregating the values of a collection into a singular value (sum, fold, eval, memo).
  These methods fully abstract away the underlying streaming representation of data. They are
sufficient to express the positive algebra [12], which generalizes relational algebra to cover numeric
operations and aggregates. The small number of methods are expressive: this framework can be
used to represent database queries, tensor arithmetic, dataflow analysis problems, graph queries,
parsing, probabilistic optimization, and more [8, 9].

3.2     Nested Data
Indexed streams are directly capable of traversing nested data efficiently. For instance, if we have
two streams of type Int →𝑠 String →𝑠 Bool representing sets of (Int, String) pairs, the zipWith
or mul API functions can be used to efficiently traverse their intersection. This intersection will be
calculated by first intersecting the outer Int valued keys, and then for each of those calculating
the intersection of the String keys. This strategy resembles the hierarchical indices often used
Fast Collection Operations                                                                             5


to accelerate database joins. This method is well-known to guarantee worst-case optimal [24]
performance with respect to table size.
  Example: Matrix Multiplication. In our Lean implementation, we provide syntactic macros that
enable very concise expressions of join queries; for instance, multiplication of two sparse matrices:
     def matMul (a : I →𝑠 J →𝑠 v) (b : J →𝑠 K →𝑠 v) : I →𝑠 K →𝑠 v :=
       Σ j => a(i,j) * b(j,k)

This expression elides quite a lot of detail that the programmer need not be aware of to use the
library: first, before multiplication can be done, the streams must be made the same shape using
repeat; then the multiplication operator for three-level nested streams needs to be unfolded; and
finally, if eval is applied to this expression, an aggregation needs to be done so that the indices
𝐼 and 𝐾 end up in the result expression, but 𝐽 is aggregated. We can approximately write a fully
explicit version of this function like so:
     -- initially, a has shape I×J and b has shape J×K
     eval (Σ j => a(i,j) * b(j,k))
     -- each factor now has shape I×J×K
     let a′ := map (map repeat) a
     let b′ := repeat b
     = Σ j => a′ * b′
     -- now we expand (*). we need to map the (*) function across all three stream
      layers:
     let mulIJK := zipWith (zipWith (zipWith (fun x y => x * y)))
     = Σ j => mulIJK a′ b′
     -- finally we can eliminate the summation
     let stream := mulIJK a′ b′
     = fold update (map sum (map (map (fold update) . empty) stream)) empty

   This final line, with its baffling series of mapped operations, is calculated automatically by our
implementation of eval, which extends to arbitrarily complex join expressions. The programmer
works with a simple algebraic model of relational algebra: joins and selects are product; project
and aggregate are sum; data is transformed with map. These operations are applied directly to the
data structures of the program with no intermediary. The eval function works out the minimal set
of nested folds to force the expression, and the host language compiler optimizes this into a set of
simple loops. In the remainder of the paper, we will unpack the definitions needed to make this
sort of computation possible.

4   LIBRARY INTERNALS DESIGN
Indexed streams are a simple generalization of traditional iterators, which are structures containing
one or more functions that abstract away an underlying collection to be traversed. The sequential
iterator approach is a fundamental part of many languages because iterators can express useful
data transformations that ultimately compile to efficient loops with minimal memory allocation.
To implement the iterator interface for a new data structure or a new transformation method, it is
necessary to understand its methods and how they are used to construct a result data structure.
   In this section, our goal is to enable someone who is familiar with these issues to work with
indexed stream iterators instead. First, we explain how the data type differs from traditional iterators.
Second, we discuss two concrete instantiations of the indexed stream iterator type: one for static
data structures backed by linear arrays, and one for dynamic data structures backed by trees. Finally,
we discuss a primary contribution: an efficiently compilable stream fold function that ties together
iteration, transformation, and construction of nested data structures.
6                                                                                                         Kovach et al.


4.1    Indexed Stream Data Structure
In this section, we provide background on streams and indexed streams using a series of code
examples in Lean. To motivate indexed streams, we start with traditional streams, which are more
often called iterators in modern programming languages. There are many approaches to defining
the iterator type. In this section we start with the following one inspired by stream fusion [7]: 1
      inductive Step (s v : Type)
        | skip (q : s)
        | emit (q : s) (value : v)

      structure Stream (v : Type) where
         s : Type
         q : s
         valid : s → Bool
         next : s → Step s v
   A stream is a state machine possessing a current state q. When a stream is advanced by next, it
produces a new state and (optionally) a value. These two possibilities are represented in the Step
type. The function valid checks whether a state is terminal (next should not be called on such a
state). Users of the stream do not need to concern themselves with its internal state type 𝑠, so this
is kept as a structure field rather than a type parameter.
   The essential difference with indexed streams [16] is that they are free to skip over values that
are not relevant to the output of the computation. This makes them available in computations
where sequential iteration would introduce an unacceptable slowdown. They are used to model
key-value stores, so their type gains an extra type parameter k, and we make two changes to the
interface to support skipping:
     key lower bound When combining two or more streams, we will prefer to use ordered
         iteration. This way, a stream that is ahead in the key space can rapidly advance the others.
        To support this, we add an interface function called index that returns a lower bound on
         the next accessible key.
     seek to key To make use of these lower bound estimates, we need to replace next with a
         function that accepts an extra parameter that specifies a range of values that may be skipped
         over. We call the new function seek. It takes a key value and a boolean that indicates whether
         it may advance up to or past that value.
   This is the type we arrive at:
      structure Stream (k v : Type) where
         s : Type
         q : s
         valid : s → Bool
         index : s → k
         seek : s → (k × Bool) → Step s v
  In order to streamline later definitions and support formal verification, we use a nearly equivalent
type that corresponds to that from [16]. This new type prevents the stream functions from being
applied to invalid states, and also eliminates the need for Step. In Lean, given some proposition P,
we can denote the type of values that satisfy P using the syntax {t // P t}. We use this to constrain
the domain of index and seek to only the valid states. Additionally, we introduce a new predicate
1 Some Lean terminology: structure defines a new record type. An inductive is a possibly recursive algebraic data type.

The notation “(s v : Type)” states that s and v are types that are parameters to the Step type. Structures can be given
fields of any type, including types (s, the stream’s state type), and functions (valid and next) whose types depend on
other members.
Fast Collection Operations                                                                                             7


ready that delimits states that are ready to produce an output key-value pair. This eliminates the
need for the skip case of step, so we can remove it entirely. We arrive at this final type used in our
library: 2
      structure Stream (k : Type) (v : Type u) where
         s : Type
         q : s
         -- predicates:
         valid : s → Bool
         ready : {q // valid q} → Bool
         -- core component functions:
         index : {q // valid q} → k
         seek : {q // valid q} → (k × Bool) → s
         value : {q // ready q} → v

   To produce the sequence of values in a stream, it is necessary to have a next function. We do not
include it in the interface above because it is definable in terms of the other methods: it is sufficient
to use next q := seek (index q) (ready q). This advances the stream toward the current index if
it has not yet produced a value for that key (not ready), and beyond that key value if it has.
   To conclude, we note that any arbitrarily complex stream expression reduces to one instance of
this data structure. This has the important consequence that the problem of evaluating a stream
does not depend on the expression that created it. As an example, here is a version of the stream
multiplication operator:
      def mul (a b : Stream k v) : Stream k v where
        s     := a.s × b.s
        q     := (a.q, b.q)
        valid := fun (qa, qb) => a.valid qa && b.valid qb
        index := fun (qa, qb) => max (a.index qa) (b.index qb)
        seek := fun (qa, qb) i => (a.seek qa i, b.seek qb i)
        ready := fun (qa, qb) => a.ready qa && b.ready qb && (a.index qa = b.index qb)
        value := fun (qa, qb) => a.value qa * b.value qb

   This stream computes the product of two streams by traversing the keys that they share. The
definition exhibits a pattern that is usual for stream operators: each of the fields of the structure
is defined directly in terms of those of the arguments. This makes possible the inlining and
specialization optimizations we describe later.

4.2    Collection Data Structures
The library would be vacuous if the indexed stream type could not be instantiated for useful data
types used in real programs. In this section, we give an overview of its generality.
4.2.1 Generalizing Sequential Streams. First, we note that the indexed stream concept is at least as
general as the traditional stream concept: it is always possible to take a sequential iterator for a
collection data structure and wrap it with an indexed stream. The corresponding definition of seek
checks to see if the current key value is lagging behind the argument key value, and calls next if so:
      seek q (i, r) :=
        let currentKey := index q
        let shouldAdvance := (currentKey < i) || (r && (currentKey = i))
        if shouldAdvance then next(q) else q

2 This is used in Lean, but for the Morphic and Rust implementations, we use simpler encodings that avoid dependent types
8                                                                                           Kovach et al.


   However, this definition does not exploit the potential of collections with fast lookup methods.
Given knowledge of the type being traversed, we might want to implement seek so that it avoids
traversing unnecessary parts (Section 4.2.3).
4.2.2 Sorted Linear Arrays. Walking through a complete example is useful to review each of the
indexed stream components:
    def sparseLinearIterator (n : Nat) [LinearOrder k]
        (keys : Vec k n) (values : Vec v n) : k →𝑠 v where
      q := (0 : Nat)
      valid q := q < n
      index q := keys[q.1]′ (by simpa using q.2)
      seek q := fun (j, r) =>
        let i := keys[q.1]′ (by simpa using q.2)
        let advance := (i < j) || (r && (i = j))
        if advance then q+1 else q
      ready _ := true
      value    := fun ⟨q, _⟩ => values[q.1]′ (by simpa using q.2)

   First, the intent of this stream is to iterate through a series of key value pairs that are stored
explicitly as arrays, with the first value of keys associated with the first value of values and so on.
This data structure is a near optimal representation for traversing data with a static key set. We
discuss the code line-by-line:
    parameters First we have the parameters to this stream: an array of keys and an array of
       values. There are two type constraints: the arrays have the same length, n, and the key type
       is constrained to be linearly ordered. Besides this, the key and value types can be arbitrary.
    state The state of the stream consists of a single natural number, initially zero.
    valid The stream is valid as long as q is less than n. Because of this static information, there
       are no run time bounds checks and no possibility of out of bounds error.
    index The index function is passed a tuple: a natural number along with a proof that the
       number is less than n. The lower bound on the next possible key is simply the current key
       value. The notation array[index]′ proof allows us to extract it safely by passing a bounds
       proof. The proof itself uses simplification to make the type of q.2 match the expected type.
    seek This seek function implements linear traversal. It is passed a target index j and a
       strictness boolean r. It must advance if the current index is strictly before j, or if they are
       equal and the strictness flag is true. The correctness of the library does not require every
       seek function to advance to the given index; it only needs to make adequate progress (see
       Section 6 for formal details).
    ready This iterator is always ready to produce its current value, so ready ignores the current
       state value and returns true.
    value Finally, value returns the current element of the array values. This function is passed
       both a proof of validity and a proof of readiness; since the second is uninformative, we use
       pattern destructuring to ignore it.
  It is straightforward to define other array based streams, such as a sparse array that uses binary
search on the key array instead of linear search (included in our evaluation), or a dense array that
can be advanced in constant time.
4.2.3 Search Trees. A typical in-order tree traversal can be adapted in a straightforward way to
implement seek. This approach combines the benefits of iteration and key-based lookup: because
seek is passed the next key value the overall computation is interested in, it can potentially skip over
Fast Collection Operations                                                                                    9


subtrees with key values that are too small. However, instead of just returning the corresponding
tree value, it returns a tree node from which iteration can be resumed.
   Compared to sequential iteration, this can asymptotically speed up a computation by replacing
a linear factor with a logarithmic one. Compared to approaches that traverse one data structure
while repeatedly calling lookup on the other, this can also asymptotically speed up the computation
by removing a logarithmic factor. Moreover, the approach is reasonably simple, consisting of an
upward pass that locates a parent node with sufficiently large key followed by a downward pass of
ordinary search to find the valid successor (see appendix for our Rust implementation).
   Although we only implemented red-black trees in our three libraries, this strategy applies equally
to any search-tree style data structure.
4.2.4 Other Data Types. We also provide methods to compute with unordered collections and
implicit collections represented by functions.
   Unordered streams. Unordered collections can arise even when inputs are ordered. For example,
if a function is mapped over the keys of a stream, their orderedness may be lost. Such a stream can
still be traversed or aggregated. These have limited composability: for instance, it may be inefficient
to intersect two unordered collections. We provide a memoization operator which, among other
purposes, can be used to collect the contents of an unordered stream into a data structure that
supports ordered traversal.
   Implicit streams. It is sometimes most natural and space efficient to represent a stream as either a
function or a state machine. These are implicit in the sense of having almost no in-memory runtime
representation at all. For instance, we might express a filter predicate as a boolean function (as in
the example from the introduction) or express an indicator function such as fun i j => if i = j
then 1 else 0 (the identity matrix), or access the elements of a hash-map by applying it to the keys
enumerated by another stream. We provide methods for multiplying these streams with ordinary
streams to enact filters, as in the following example.
   Example: Array slice. Array programs typically make use of array slicing: a way of extracting a
sub-array, typically with a notation like 𝐴[𝑖 : 𝑗] to denote the values of 𝐴 corresponding to indices
from 𝑖 up to 𝑗. For a dense array 𝐴, the expectation is that enumerating these values depends only
on | 𝑗 − 𝑖 |, not the size of the array.
   We reinterpret [𝑖 : 𝑗] above as specifying an array itself that maps key values {𝑖, 𝑖 + 1, . . . , 𝑗 − 1, 𝑗 }
to 1 and all other key values to 0. Then the slice is equivalent to computing [𝑖 : 𝑗] · 𝐴, a mask of 𝐴:
     def slice (arr : Nat →𝑠 v) (i j : Nat) : Nat →𝑠 v := mul (range i j) arr
Despite relying on multiplication, it maintains the expected efficiency. The cost is equal to the
cost of traversing the range of indices from i to j, plus the cost of locating the first index past i
inside arr and the cost of enumerating each successive value of arr. In the case that arr is dense,
these costs are constant, matching the usual behavior. This same operation also applies to arbitrary
associative arrays, achieving predictable performance for those as well.
4.2.5 Correctness. As a final note to implementers of the stream interface, we provide a basic
explanation of the notions of (strict) monotonicity and lawfulness (Section 6.1). Ensuring that your
stream implementation satisfies these properties guarantees that it can be arbitrarily joined or
nested with other stream types without issue.
   Monotonicity requires that the state returned by seek always has an index at least as large as
the prior one. Strict monotonicity requires that, if seek is called at a ready state, it returns a state
with strictly greater index value. If the stream has a finite state space, this property is sufficient to
guarantee termination. Finally, lawfulness requires that the seek function does not go too far or
10                                                                                              Kovach et al.


otherwise change the value of the stream at indices beyond the key it is passed. See Section 6 for
full details.

4.3     Indexed Stream Fold
Evaluating a standard iterator is straightforward: repeatedly call next and collect each value into
the output data structure of choice. Indexed streams have a similar formula: call next, and at each
ready state, collect the key-value pair into the output data structure of choice. However, indexed
streams lend themselves to nested data structures, so joins across inputs with multiple levels are
typical. To reduce the stream, it is insufficient to store a linear series of key-value pairs into a data
structure, because the value itself is a stream. In this section, we describe the building blocks we
use in Lean handle nested streams using only a single one-dimensional fold function.
4.3.1 Fold. This version of fold is taken from Lean (the definitions in Morphic and Rust are similar):
@[inline] def fold (f : m → k → v → m) (s : k →𝑠 v) : m → m :=
  let ⟨_, q, valid, index, seek, ready, value⟩ := s
  let rec @[specialize] go f q acc : m :=
     if valid q then
        let i := index q
        let q′ := next q i
        let acc′ := if ready q then f acc i (value q) else acc
        go f q′ acc′
     else acc
  go f q

  The function is quite simple, consisting of a tail-recursive loop called go. The body of the loop
checks if the stream is valid; if not, it returns the accumulator. If it is valid and also ready, it updates
the accumulator. Whether or not it is ready, it updates the state and continues to the next iteration.
  For the remaining discussion, it is sufficient to understand its type:
       fold : (m → k → v → m) → (k →𝑠 v) → m → m

This is a standard fold-like type signature: given the collection and a combining function, transform
the accumulator.
4.3.2 Data Construction. We rely on a simple interface for incrementally constructing output
collections:
class Modifiable (k v m : Type) where
     update : m → k → (modify: v → v) → m

   A collection type m is modifiable if it implements this function, which applies a function modify
to the value associated with given key. In practice, we further assume that the type v has a default
value. This way, when update is applied to a key that isn’t present in a collection, this default value
is passed to modify. For nested data structures (when the collection is used to store values that are
also Modifiable), this approach recovers the “destination passing style” [16, 17, 28] well known to
array language compilers.
4.3.3 Evaluation. We define a class called OfStream to transform streams into data collections. This
is analogous to FromIterator in Rust. Implementations of this class record how to transform a
stream into an update function for a particular data type:
     class OfStream (v v′ : Type) where
            eval : v → v′ → v′
Fast Collection Operations                                                                                                11


   Instead of simply giving eval the type v → v′ , we give it this type because it is more natural
for incrementally updating the elements of a map. This connects more easily with the Modifiable
method, as we will see shortly. This is defined as a class so that the compiler can automatically
deduce the needed instance when eval is applied to a stream/data-structure pairing.
   Remarkably, only a few instances of this class are needed, with the most important being the
case of a nested stream. We write out the definition first and then discuss each of its parts:
instance [OfStream v v′ ] [Modifiable k v′ m] : OfStream (k →𝑠 v) m where
     eval := fold Modifiable.update ◦ map eval
   This method subsumes the compilation method of Kovach et al. [16] while being substantially
more concise and portable across languages. 3 When fully unfolded, it can be compiled into a simple
nest of loops. We unpack the mechanism behind it next.
   In Lean, instance parameters are written [OfStream v v′ ]. We read this parameter as “values of
type v can be transformed into values of type v′ ”. These arguments do not need to be explicitly
passed when eval is called; they are inferred by type class search.
   The way to read the types in the first line of this definition is as follows: if we can transform
type v into v′ , and if m is a collection type storying k-v′ type pairs, then we can transform a
stream of k-v pairs into a collection of type m. When v is itself a stream type, the definition uses its
OfStream instance (in the expression map eval) to recursively transform its values into the concrete
values of type v′ that are stored in m. The total transformation is achieved in two steps: map
eval over the values of the stream, then fold the resulting stream using update. The first step is a
stream transformation: no computation is done immediately. The second step ultimately forces
computation.
   To further unpack this, using the type signatures previously given for fold, update, and eval, we
can calculate the types of the subexpressions as follows:
    fold        : (m → k → v → m) → (k →𝑠 v) → m → m
    update      : m → k → (v → v) → m
    eval        : v → v′ → v′
    map eval    : (k →𝑠 v) → (k →𝑠 (v′ → v′ ))
    fold update :              (k →𝑠 (v′ → v′ )) → m → m
    -------------------------------------------------------
    fold update ◦ map eval : (k →𝑠 v) → m → m
   The apparent inefficiency of using map to create a stream of function closures is in fact never an
issue: we rely on the power of the host language to perform specializing compilation to completely
inline and optimize the computation. We discuss this in greater detail in the following section.

5    PORTABILITY DESIGN
The iterator concept has found a home in many mainstream programming languages, providing a
uniform and performant interface to sequential iteration. Similarly, indexed stream iteration can
find a home in many languages and provide a uniform interface to non-sequential iteration.
   In this section, we explain how the indexed streams can be implemented in substantially different
programming languages in such a way that their compilers ensure indexed stream fusion. We
discuss how the features of Lean, Morphic, and Rust lead to different stream type definitions that
ultimately lead to similar performance and expressiveness.
   As a simple example to introduce the Morphic and Rust implementations, we will use the
                           Í
following computation: 𝑛−1   𝑖=0 𝑖 (mod 5). Although this example does not require non-sequential
3 There is one other instance, needed to handle aggregations, that is similarly simple but omitted for space. There is also a

base case for scalar values.
12                                                                                        Kovach et al.


                                                     pub range(lo: Int, hi: Int): Stream
      pub type Stream k v {                            Int Int =
        pub Stream(                                    Stream(
          ()        -> Bool,       // valid              \()     -> lo < hi,   // valid
          ()        -> k,          // index              \()     -> lo,        // index
          (k, Bool) -> Stream k v, // seek               \(j, r) -> range(     // seek
          ()        -> Bool,       // ready                max(lo, j + bool_to_nat(r)),
          ()        -> v,          // value                hi),
        )                                                \()     -> True,      // ready
      }                                                  \()     -> lo         // value
                                                       )
      pub sum(s : Stream k Int) : Int =
        fold(\(acc, _, v) -> acc + v, s, 0)          pub eg(n: Int): Int =
                                                       sum(map(\k -> mod(k,5), range(0,n)))

                                Fig. 2. Stream definitions in Morphic


iteration for optimal performance, it serves well as a minimal example for the code generation
issues faced by our library.

5.1   Lean
As described previously, in Lean we have a single stream data type. Each operator takes one or
more streams as arguments and produces a single output stream. Lean’s dependent type system
allows us to hide the stream’s state type and also enforce various correctness hypotheses by
construction. These propositional arguments are erased during code generation, so they have no
effect on performance.
   Lean has a specialize attribute which can be used to tag a recursive function definition. This
is a request to the compiler to generate specialized versions (if possible). We use this on a single
function: the stream fold function, which is recursive and higher-order. The remainder of the
library is designed carefully so that stream constructions are always immediately available to the
inline/specialize machinery.
   In particular, type classes are used to resolve the eval method, which is responsible for calling
fold on nested streams, described in the previous section. Because type class resolution is performed
at compile time, the Lean compiler is able to generate custom code for each invocation of fold by
fully deconstructing the stream constructions passed as arguments.
   Finally, we note that although Lean has pure semantics, it features an opportunistic optimization
that performs mutable updates to constructors when they are held by a unique reference. Within the
Lean standard library, this feature is used to provide high performance mutable arrays and optimize
list functions which would otherwise heavily allocate. Our library cooperates with this feature: the
fold and update combinators are designed to sequentially update an output data structure, so if
that data structure is amenable to the mutation optimization, it will be used.

5.2   Morphic
Morphic [5] is a pure functional language in the ML family. Its compiler is capable of automatically
specializing all higher-order definitions throughout a program. In Morphic, like Lean, we use a
single stream data structure. Each stream operator defines a new element of this structure in terms
of the components of the streams it is passed. However, the stream definition in Morphic (Figure 2,
left) is slightly more simple and unusual than the others.
Fast Collection Operations                                                                          13


   Notably, instead of taking in a state parameter, everything except for seek is simply a thunk
which evaluates to the appropriate value. We can motivate this design choice with the stream for
the range operator used by our motivating example (Figure 2, right).
   Note that the thunks are closed over the two parameters of range, and also that seek recursively
calls range with updated lo argument. One might expect the runtime to allocate five closures
for every iteration of this stream. However, as we explain next, the Morphic compiler entirely
eliminates this apparent cost.
   In fact, the generated code that loops over the values of this stream simply allocates stack space
for lo and hi, allocates no closures, and makes no calls. When the compiler analyzes the call to
fold (Figure 3, right) invoked by sum on this particular example, it is specialized to the lambda
structure of range. The structure of the closures that would otherwise be allocated is reified as an
algebraic data type to hold the values that would be closed over (lo and hi). Essentially, the call to
range(lo, hi) is itself the state of the stream. Finally, the logic needed to extract values from this
data type (corresponding to each component function) is inlined into fold, fold compiles to a loop,
and the datatype itself is unboxed onto the stack.
   This approach is also practically useful because the type system of Morphic does not have a
feature to hide the state type. We credit this idiom to the authors of Morphic’s standard library
iterator definition.

5.3    Rust
Rust monomorphizes all polymorphic functions during compilation. For each instantiation of
a given polymorphic function, this process generates code that is specialized to the given type
arguments. Rust also features traits, an ad-hoc polymorphism mechanism. A trait packages one or
more types and methods together in an interface that can be implemented for multiple types. Calls
to trait methods are also monomorphized, and we use this to guarantee specialization of stream
code by defining the fold function as a trait method.
   Each stream-constructing operator has a corresponding struct type that holds its state. This
struct must implement the indexed stream trait. This approach is idiomatic Rust: it mirrors the
strategy of implementing IntoIterator and FromIterator from the standard library in order to
provide sequential iteration of data structures and construction of a data structure after one or
more iterator operations (map, filter, etc) are applied.
   The running example in Rust is as follows:
      pub fn eg(n: i64) -> i64 {
          RangeStream::new(0, n).map(|i, _| i % 5).sum()
      }
  It is instructive to break down the types of this expression:
          let s1: RangeStream = RangeStream::new(0, n);
          let s2: MappedStream<RangeStream, _, i64> = s1.map(|i, _| i % 5);
          let s3: i64 = s2.sum();
          s3
to note that the type of s2 records the fact that s2 is the result of mapping a function over a range
(the underscore is a placeholder for the function’s type). It is at s3 that the equivalent to collect()
is called in order to realize the stream computation as a concrete value (in this case an integer). See
Figure 3, left, for the Rust version of stream fold.
   Inspecting assembly output, we verified that the code generated for this expression is identical
(modulo register and label names) to that of the following:
      let mut result: i64 = 0;
14                                                                                        Kovach et al.


        // Rust
        fn try_fold<B, F, R>(&mut self,
                                init: B, mut
         f: F)                                           // Morphic
            -> ControlFlow<R, B>                         pub fold(f: (m,k,v) -> m,
        where F: FnMut(B, Self::I, Self::V)                         s: Stream k v, acc: m): m =
                  -> ControlFlow<R, B>,                      let Stream(valid, index, seek,
        {                                                                  ready, value) = s in
             let mut acc = init;                             if valid() {
             while self.valid() {                               let r = ready() in
                 if self.ready() {                              let i = index() in
                      let i = self.index();                     let acc_ = if r {
                      let v = self.value();                          f(acc, i, value())
                      self.next();                                 } else { acc } in
                      acc = f(acc, i, v)?;                      fold(f, seek(i, r), acc_)
                 } else {                                    } else {
                      self.next();                              acc
                 }                                           }
             }
             ControlFlow::Continue(acc)
        }



                      Fig. 3. The fold function in Rust (left) and Morphic (right).



      for i in 0..n {
          result += i % 5;
      }
      result


5.4    Discussion and Limitations
   Ideal Language Characteristics. Our experience suggests that languages offering static guarantees
of specialization and linear data update are most suitable to host indexed iterators. The Lean
compiler’s optimizations appear to be less reliable at this time than Morphic; Morphic’s optimizer
is designed around a type theoretic static analysis with completeness guarantee. Additionally,
we expect that, for example, Koka would be a reliable host language [18], as it also implements
specialization and additionally offers a type system for in-place update of pure data structures.
   Limitations. Our approach assumes that stream computations appear as static parts of the
program text; they cannot be generated based on runtime values or hidden behind recursive
function applications. This is a simple consequence of the static analyses for specialization that we
rely on.

6     CORRECTNESS
The Lean implementation of indexed streams allows for easy and modular correctness proofs. Prior
work by Kovach et al. [16] proposed indexed streams as an IR for a deeply embedded compiler for
positive algebra contraction expressions. Although they proved that the indexed stream model
faithfully computes the solution to contraction problems, an end-to-end correctness guarantee was
left open. While end users could be confident of the mathematical details of the abstract indexed
Fast Collection Operations                                                                          15


streams as used by their compiler, they would have to trust that the custom code generator faithfully
translated indexed streams to imperative code.
   However, if we directly evaluate indexed streams in Lean as in the shallow embedding of this
work, the previous correctness proofs apply directly—end users now only have to trust the Lean
compiler, which is widely used and well-tested, rather than a custom code generator. Moreover,
end users can more easily extend and integrate indexed streams with other verified computation.
In this section, we describe how we adapted the proof structure of Kovach et al. [16] to a shallowly
embedded library.

6.1    Stream Laws
We briefly review the stream laws from Kovach et al. [16]. First, we ask that streams be monotonic,
meaning that calling seek never decreases the index. We say a stream is lawful, if, in addition to
being monotonic, it satisfies the property that when the stream is at state 𝑞, calling seek with
parameters (𝑖, 𝑏) (where 𝑖 : 𝜄 and 𝑏 : Bool) does not change the final semantic evaluation (i.e.
interpretation of the stream as a function from indices (keys) to values; see 6.3), at any index 𝑗
where ( 𝑗, 0) ≥ (𝑖, 𝑏) in the lexicographic ordering. Intuitively, calling seek i permits the stream to
move up to index 𝑖, but it should not affect emissions whose indices are beyond 𝑖. In Lean, these
requirements are expressed as
      class IsLawful [LinearOrder 𝜄] [AddZeroClass α] (s : Stream 𝜄 α) where
        mono : ∀ q i, s.index q ≤ s.index′ (s.seek q i)
        seek_spec : ∀ q i j, (i ≤ (j, false)) → s.eval (s.seek q i) j = s.eval q j

   If, additionally, the stream always strictly increases its index when advanced from a ready state,
we say it is strictly monotonic. Finally, we say a stream is bounded if, roughly, for every infinite
sequence of seek calls which can be made without ever terminating the stream, only finitely many
of those calls are to indices past the index of the stream at the state when the seek call is made.
   Most of the basic combinators we supply preserve these properties—taking bounded streams to
bounded streams, monotonic streams to monotonic streams, and so on. Note that strict monotonicity
can always be recovered from any bounded, disordered stream using the memo operation. This is
useful if one e.g. wishes to use imap with a generic 𝑓 .
   The stream laws permit users to build sophisticated, efficient, verified computations by composing
the basic combinators, while retaining confidence that these compositions of combinators remain
correct. Moreover, users who wish to extend our library of combinators must only prove these
properties in order to be able to automatically integrate with the rest of our library.
   Finally, our shallow embedding of indexed streams and Lean’s dependent type system permit us to
use information about stream laws when deciding how to evaluate streams, which was not possible
in previous work. For example, we could define an instance OfStream {s // s.IsStrictMono},
describing evaluation of the subtype of streams which are strictly monotonic, rather than simply
monotonic. The evaluation function could then be optimized for the case where it is guaranteed
that each index will only be seen once.

6.2    Changes in Core Theorems
We were able to reuse most proofs from the prior work [16] almost directly, modulo some small
changes. In particular, previously, ready produced values on all states, implicitly duplicating the
work of checking if valid is true. While this was acceptable for an abstract model, we now require
that a call to ready be supplied with a proof of valid to improve performance.
  Similarly, other changes were made so that the indexed stream model could function as a
shallow embedding of indexed streams. For example, previously, valid and ready were Prop-valued
16                                                                                         Kovach et al.


functions, not necessarily decidable. The signature of these functions was changed to return Bool
to allow computation, and this necessitated a straightforward refactor of the core lemmas.

6.3    Semantics
In addition to concrete evaluation, which evaluates streams to associative arrays as described in
4.3, we also have a semantics which evaluates streams to finitely supported functions. If we define
      def eval0 [Zero α] (s) (q : {q // s.valid q}) : 𝜄 →0 α :=
        if h : s.ready q then
           -- function which maps ‵ s.index q′ to ‵ s.value q′ and is 0 elsewhere
           fun0 | s.index q => (s.value ⟨q, h⟩)
        else 0
then we can define the semantics as:
      def eval [AddZeroClass α] (s) [IsBounded s] : s.𝜎 → 𝜄 →0 α
      | q => if h : s.valid q then
                -- (proof of termination elided)
                eval0 s ⟨q, h⟩ + eval s (s.next q)
             else 0
This is an adaptation of the semantics given in Appendix B. Note that we have replaced the output
type 𝜄 → Option 𝛼 with a finitely supported function 𝜄 →0 𝛼, taking the point of view that an
associative array has a default 0 value which is its value at any missing key. This version is actually
more general since we can always assign 𝛼 := Option 𝛼 ′ , and set the zero value to be none
  This allows us to consider streams while remaining agnostic to any particular data structure. All
proofs of correctness for the core combinators in our library are given in terms of this semantic
evaluation. For example, the correctness theorem for multiplication looks as follows:
      theorem mul_spec (a b : Stream 𝜄 α) [IsStrictLawful a] [IsStrictLawful b]
          (q : (a.mul b).𝜎) :
        (a.mul b).eval q = a.eval q.1 * b.eval q.2
   By providing a semantics which is agnostic to data structure, we allow combinators to be verified
in isolation, once and for all, rather than once for every data structure that could be backing the
input streams.

6.4    Data Structure Interface
The most significant difference from prior work in the proofs is the integration of concrete data
structures that model associative arrays. We need to be able to connect the semantic evaluation to
the actual compilation of streams into these data structures.
   In order to do this, we add a canonical evaluation from our data structure to finitely supported
functions from the index type to the value type—that is, a canonical interpretation of our data
structure as an associative array. Recall that our abstract semantics also provide a canonical way
to evaluate a stream into a finitely supported function. Thus, the laws that OfStream and ToStream
must satisfy simply assert that these evaluations commute:
      class LawfulOfStream [EvalToFinsupp α γ] [EvalToFinsupp β γ] [Add γ]
           extends OfStream α β where
        eval_of_stream : ∀ (s : α) (b : β),
             (evalFinsupp (eval s b) : γ) = evalFinsupp b + evalFinsupp s

      class LawfulToStream [EvalToFinsupp α γ] [EvalToFinsupp β γ]
           extends ToStream α β where
        to_stream_eval : ∀ (d : α), (evalFinsupp (stream d) : γ) = evalFinsupp d
Fast Collection Operations                                                                                                           17


           1.2                                      1.1                                 1.2
           1.1                                                                          1.1
time, linear




                                                    1.0
           1.0                                                                          1.0
                                                    0.9                                 0.9
           0.9
           0.8                                      0.8                                 0.8
           0.7                                      0.7                                 0.7
                     _b
                     ge

                            b!
                            st

                                      b
                                          _b
                                               v3




                                                               _b
                                                               ge

                                                                 b
                                                                st

                                                              _b!

                                                                           v3

                                                                                _b




                                                                                                _b

                                                                                                      ge

                                                                                                                b

                                                                                                                      st

                                                                                                                           _b

                                                                                                                                v3
                                  st_




                                                             st_




                                                                                                            st_
                          ne




                                                             ne




                                                                                                                    ne
                         st_
                  ge




                                          v3




                                                            ge




                                                                                v3




                                                                                               ge




                                                                                                                           v3
                 ran




                                                           ran




                                                                                                     ran
                                                           v3
                                  ne




                                                          ne




                                                                                                           ne
                ran




                                                      ran




                                                                                              ran
                       ne




                       (a) Rust                              (b) Morphic                                   (c) Lean

                          Fig. 4. Runtimes normalized to best baseline for each test (smaller is better).


   Once these laws are proved for some data structures, we can easily provide end-to-end proofs for
stream computations that freely mix and match those data structures. Moreover, users can easily
integrate their own data structures and verify their properties; it suffices define OfStream, ToStream,
and EvalToFinsupp for the data structure and to prove that these two laws hold.
   In order to make this more convenient, we have proved that for data structures implementing
Modifiable satisfying some additional basic correctness properties (e.g. updating an index leaves
other indices unchanged), the corresponding OfStream instance defined in Section 4.3 satisfies
the LawfulOfStream property. Thus, for a broad range of data structures which fit the Modifiable
pattern, we get a reasonably efficient LawfulOfStream implementation almost for free.

7              EVALUATION
To evaluate our libraries, we address two questions:
               (1) Can the stream combinators match the performance of idiomatic, manually fused programs
                   written in the host language, and how do their code size compare?
               (2) In a version of the library with ideal performance, how much do we gain from using
                   combinators over other traditional iteration methods?
  To address the first, we wrote three benchmarks of stream primitives and ported them to each
language. We compare the stream-based programs to one or more baseline programs written
using idiomatic loop constructs. These measure overhead when using our library to implement an
identical algorithm.
  To address the second, using our Rust library we (1) implemented three methods of evaluating
the skewed triangle relational join query [24] and (2) compared our red-black tree stream to the
red-black tree iterate/lookup strategy. These measure algorithmic speedups that come from using
fused iteration strategies over more naive strategies.
  Benchmarks were compiled with rustc version 1.79, Lean4 version 4.7.0, and Morphic at commit
hash d692f4cdd/llvm 16. Tests were run single-threaded on an Intel i7-10710U; each test measure-
ment is an average of at least 100 runs.

7.1              Comparison to Idiomatic Fused Loops
For each implementation, we run the three tests depicted in Figure 4. For each of the following
cases, those with suffix “_b” are baselines, “_b!” is the best baseline when more than one baseline is
evaluated, and those without are computed using indexed streams:
                • range constructs a range iterator, maps a function over it, and sums the values
                • nest sums the values of an 𝑛 × 𝑛 nested stream.
18                                                                                           Kovach et al.


       // slower baseline
       pub fn nested_baseline(n: i64) ->
       i64 {
           let mut result: i64 = 0;
           for _ in 0..n {                               // faster baseline
               for j in 0..n {                           pub fn nested_baseline_2(n: i64) ->
                   result += j % 5;                      i64 {
               }                                             let mut result: i64 = 0;
           }                                                 for _ in 0..n {
           result                                                let mut a = 0;
       }                                                         for j in 0..n {
                                                                     a += j % 5;
       // the stream combinator version:                         }
       pub fn nested_iterator(n: i64) ->                         result += a;
       i64 {                                                 }
           let s = RangeStream::new(0,                       result
       n).map(|_, _| RangeStream::new(0,                 }
       n));
           s.map(|_, v| v.map(|i, _| i %
       5).sum()).sum()
       }

                                    Fig. 5. Rust summation baseline.


     • v3 computes the product of the values (over the intersection of keys) of three randomly
       generated sparse vectors. We do so by simultaneously traversing all three (there is no
       intermediate formed).
   These tests are meant to stress the library: because minimal computation is performed, we should
see only the iteration overhead introduced by our generic methods. They are reasonably complete
because more complex programs are simply compositions of these basic elements: implicit stream
construction, maps, and intersections. Overall, we conclude from these tests that indexed streams
introduce negligible overhead over the best baselines, and sometimes outperform simpler code that
one might write in practice (see the following paragraph for discussion).
   Implementation discussion. The implementations using indexed streams are shorter: in every
implementation, each of the three benchmarks consists of one or two expressions. The baseline
implementations range from 5–35 lines of code. In several cases the obvious baseline turned out to
be less efficient than the stream version. For instance, it took a little trial and error to discover the
second Rust program in Figure 5, which performs about 20% faster than the first:
   For these cases we show both the best baseline we found and the more obvious one in the figure.
   In some cases, such as the intersection of three vectors, the baseline code size scales linearly or
quadratically with the number of factors involved, making that approach impractical for larger
joins. The difficulty of implementing a correct implementation also increases when different data
structures are involved, especially if they have unique traversal methods. When data types change,
the stream programs remain the same: the only difference is in input and output type annotations.
Finally, we reiterate that the stream functions compose, whereas the baseline approach requires
writing a manually fused program for each new problem.
   The programs in Rust and Morphic are somewhat more verbose than those in Lean, because we
did not implement an equivalent to the algebraic notation and eval present in the Lean library. For
Rust, we believe this would be possible using additional traits and Rust macros.
Fast Collection Operations                                                                                     19


                     103
       time, log-scale




                                                           time, linear
                     102
                              ive




                                           ed



                                                      ed




                                                                           2



                                                                                        p


                                                                                             3



                                                                                                           p
                                        fus



                                                   fus




                                                                          rb.



                                                                                       oo


                                                                                            rb.



                                                                                                         oo
                            na




                                                                                    2_l




                                                                                                      3_l
                           tri.




                                      un



                                                  tri.
                                     tri.




                                                                                  rb.




                                                                                                     rb.
                             (a) Triangle Query                                 (b) Red-black Tree

  Variance across languages. In our tests, Rust performed best in absolute terms, with about a 2x
edge over Morphic. Lean was less consistent: seemingly small changes can easily affect inlining
behavior and made benchmarking relatively challenging. We also struggled to consistently ensure
application of the constructor reuse optimization, which is needed to ensure that no redundant
memory allocations occur.

7.2   Comparison to Traditional Iterators
For our second test, we use the Rust implementation to implement two problems: the triangle join
query and a test of red-black tree traversal.
   Triangle Join. The triangle join query is the following relational algebra expression: 𝑅(𝑎, 𝑏) ⊲⊳
𝑆 (𝑏, 𝑐) ⊲⊳ 𝑇 (𝑎, 𝑐). This benchmark tests many components of the library: nested iteration of sparse
data structures, construction of a nested output data structure, and sparse intersections. We use it
to illustrate that order-of-magnitude gains can be made when passing from a naive implementation
to an unfused stream-based implementation and then to a fused stream implementation. The data
for this benchmark is stored using sparse arrays as a variant of CSR format. We use three relations
each containing 20,000 pairs of Strings.
   The tri.naive implementation measured in Figure 6a is an implementation of iterate and lookup:
it uses standard Rust iterators to get values of 𝑎 and 𝑏 from 𝑅, then does a lookup on 𝑏 into 𝑆,
traverses the corresponding values of 𝑐, and finally uses lookup to check if 𝑎, 𝑐 is an element of 𝑇 .
The relatively high cost of this method arises from the many binary searches done for the lookups.
   The second implementation (tri.unfused) performs pairwise joins using galloping binary search:
we use indexed streams to first join 𝑅 and 𝑆 into a temporary relation, and then join this temporary
with 𝑇 . The speedup of 5x demonstrates the value of incrementally scanning and initiating fewer
searches from scratch.
   The final implementation (tri.fused) is fused: it computes the 𝑎 attribute values, then the 𝑏
values, and then the 𝑐 values. This method also uses streams that perform galloping binary search,
but it only traverses each input a single time and avoids allocating an intermediate result that is
asymptotically larger than the final result value, leading to a speedup of about 20x in this case. This
is the default approach that results from using stream combinators to tackle this problem.
   Joint Tree Traversal. When intersecting the keys of two or more trees, we can either traverse
one and access the other by key, or simultaneously traverse them as indexed streams. The relative
performance is shown in Figure 6b, where rb.2 (intersection of two trees) and rb.3 (intersection of
three trees) are the streaming tests. These intersect red-black trees containing one million random
integer keys each. The streaming approach is faster by about 2x.
20                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               Kovach et al.


8     RELATED WORK                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             associative
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               <latexit sha1_base64="WRYO5B4cW9e+LQqP3jhu0mf9Bug=">AAAEMHicdZPPb9MwFMe9BdgoP7bBkUtEhcQhTHHapt1tGgc4DkS3SW01Oc5ra9WxI8cZVFH+DK7wP/DXwAlx5a/ASVNUVmMl0vPz5/v83ldylHKWad//sbPr3Ll7b2//fuvBw0ePDw6PnlxkMlcUhlRyqa4ikgFnAoaaaQ5XqQKSRBwuo8Xr6vzyBlTGpPiglylMEjITbMoo0SY1IlkmKTPxDVwftv1jv17udoCboI2adX595ByMY0nzBISm3FQaYT/Vk4IozSiHsjXOM0gJXZAZjEwoSALZpKh7Lt0XJhO7U6nML7RbZzcVBUmybJlEhkyInme3z6qk7WyU6+lgUjCR5hoEXV00zbmrpVsZ4MZMAdV8aQJCFTO9unROFKHa2NRqjWOYGi/rfgpNqHwV8RzK4v2bs7II+x7uDryg2y8tYEzUYgPu9LyT0MP9no3lbDbXGzAOPIy7pnLXRs8UgGjI3sDDQeh1rGXTXKX8b01s0BNTs2NDpSJitkaDHjaTdT3sh/b7ybIh+6FXfwYT8JHKJCEiLsYVVo8zwhOzg096y8E2Li2i1Wg2VTO0XdYMatOtPbALm7FtwrUj/2vUeGDvszKnEpknhG8/mO3gIjjG4XHvXdA+PWse0z56hp6jlwijPjpFb9E5GiKKJPqMvqCvzjfnu/PT+bVCd3cazVP0z3J+/wG9QWhV</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            lists
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            <latexit sha1_base64="eammUjzgEPd98GlQ+UzJaLwGS1g=">AAAEKnicdZPdbtMwFMe9hY9RPrbBJTcRFRIXoYrTNu3upnEBlwPRbVJbTY5z2lp1nMh2gCrKM3AL78DTcDdxy4PgpCkqq7ES6fj49z8+5y85yjhT2vdv9vadO3fv3T940Hr46PGTw6PjpxcqzSWFEU15Kq8iooAzASPNNIerTAJJIg6X0fJNdX75CaRiqfioVxlMEzIXbMYo0SY1qm5Q10dtv+PXy90NcBO0UbPOr4+dw0mc0jwBoSknSo2xn+lpQaRmlEPZmuQKMkKXZA5jEwqSgJoWdbel+9JkYneWSvML7dbZbUVBEqVWSWTIhOiFun1WJW1n41zPhtOCiSzXIOj6olnOXZ261ehuzCRQzVcmIFQy06tLF0QSqo1BrdYkhplxse6n0ISmryOeQ1l8eHtWFuHAw72hF/QGpQWMiVxuwd2+dxJ6eNC3sZzNF3oLxoGHcc9U7tnouQQQDdkfejgIva61bJbLjP+tiQ16Ymp2bWgqiZhv0KCPzWQ9D/uh/X6yashB6NWfwQR8pmmSEBEXkwqrxxnjqdnBF73jYBuXFtF6NJuqGdouawa16TYe2IXN2DbhxpH/NWo8sPdZmVOJzBPCtx/MbnARdHDY6b8P2qdnzWM6QM/RC/QKYTRAp+gdOkcjRBFDX9E39N354fx0bpxfa3R/r9E8Q/8s5/cfpQFlrQ==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 arrays                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              <latexit sha1_base64="Cs1A+Au4/IU10RYmzmXbT20xxJI=">AAAEK3icdZPdbtMwFMe9hY9RPrbBJTcRFRIXoYrTNO3upnEBlwPRblIbTY7jtl4dJ7IdIIryDtzCO/A0XIG45T1w0hSV1ViJdHz8+x+f85ccZYxK5bo/9vatW7fv3D2417n/4OGjw6PjxxOZ5gKTMU5ZKi4jJAmjnIwVVYxcZoKgJGLkIlq9qs8vPhAhacrfqyIjYYIWnM4pRkqnJkgIVMiro67bc5tl7wawDbqgXedXx9bhLE5xnhCuMENSTqGbqbBEQlHMSNWZ5ZJkCK/Qgkx1yFFCZFg27Vb2c52J7Xkq9M+V3WS3FSVKpCySSJMJUkt586xOms6muZqPwpLyLFeE4/VF85zZKrXr2e2YCoIVK3SAsKC6VxsvkUBYaYc6nVlM5trGpp9SIZy+jFhOqvLd67OqDIYO9EeO5w8rAxgjsdqC+wPnJHDgcGBiGV0s1RYMPQdCX1f2TfRCEMJbcjByoBc4fWPZLBcZ+1sTavRE1+yb0FQgvtig3gDqyXwHuoH5flS05DBwmk9jnHzEaZIgHpezGmvGmcJQ78gnteNgF1YG0Xo0k6od2ixrBzXpNh6Yhe3YJuHGkf81qj0w91mbU4v0E4I3H8xuMPF6MOgN3nrd07P2MR2Ap+AZeAEgGIJT8AacgzHA4Bp8Bl/AV+ub9d36af1ao/t7reYJ+GdZv/8AQkhmGg==</latexit>




Indexed streams generalize the idea of stream fusion, which ap-
                                                                       shallow
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  <latexit sha1_base64="KfQ+bT+z5M3K2O/nUGkeY77d+jw=">AAAELHicdZPPb9MwFMe9BdgoP7bBkUtEhcQhVHGapt1tGgc4DkTXSW01OY7bWnXsyHYYVZQ/giv8D/w1XBDiyt+Bk6aorMZKpOfnz/f5va/kOGNUad//sbfv3Ll77+DwfuvBw0ePj45PnlwqkUtMhlgwIa9ipAijnAw11YxcZZKgNGZkFC9fV+ejj0QqKvgHvcrINEVzTmcUI21SI7VAjImb6+O23/Hr5e4GsAnaoFkX1yfO0SQROE8J15ghpcbQz/S0QFJTzEjZmuSKZAgv0ZyMTchRStS0qPst3Rcmk7gzIc3PtVtntxUFSpVapbEhU6QX6vZZlbSdjXM9G0wLyrNcE47XF81y5mrhVsO7CZUEa7YyAcKSml5dvEASYW0sarUmCZkZH+t+Co2weBWznJTF+zfnZRH1PRgOvCDslxYwQXK5BXd73mnkwX7PxjI6X+gtGAYehKGpHNrouSSEN2Rv4MEg8rrWslkuM/a3JjToqanZtaFCIj7foEEPmslCD/qR/X60ash+5NWfwTi5wSJNEU+KSYXV44zh1OzIJ73jYBuWFtF6NJuqGdouawa16TYe2IXN2DbhxpH/NWo8sPdZmVOJzBOCtx/MbnAZdGDU6b0L2mfnzWM6BM/Ac/ASQNAHZ+AtuABDgMESfAZfwFfnm/Pd+en8WqP7e43mKfhnOb//APLeZow=</latexit>




plies to operations on lists, to operations on associative arrays. We embedding Sect          Our work
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        <latexit sha1_base64="JN1etvFdVYlCSkBSQNHiGqg2KZY=">AAAELXicdZPdbtMwFMe9hY9RPrbBJTcRFRIXoYrTNu3upnEBdwxEt0ptNTmOm1p17Mh2GFWUl+AW3oGn4QIJcctr4KQpKquxEun4+Pc/PucvOcoYVdr3f+ztO7du37l7cK91/8HDR4dHx48vlMglJiMsmJDjCCnCKCcjTTUj40wSlEaMXEbLV9X55UciFRX8g15lZJaihNM5xUib1PhtLt1rIZdXR22/49fL3Q1gE7RBs86vjp3DaSxwnhKuMUNKTaCf6VmBpKaYkbI1zRXJEF6ihExMyFFK1KyoGy7d5yYTu3Mhzc+1W2e3FQVKlVqlkSFTpBfq5lmVtJ1Ncj0fzgrKs1wTjtcXzXPmauFW07sxlQRrtjIBwpKaXl28QBJhbTxqtaYxmRsj634KjbB4GbGclMX712dlEQ482Bt6QW9QWsAYyeUW3O17J6EHB30by2iy0FswDDwIe6Zyz0YnkhDekP2hB4PQ61rLZrnM2N+a0KAnpmbXhgqJeLJBgz40k/U86If2+9GqIQehV38G4+QaizRFPC6mFVaPM4EzsyOf9I6DbVhaROvRbKpmaLusGdSm23hgFzZj24QbR/7XqPHA3mdlTiUyTwjefDC7wUXQgWGn/y5on541j+kAPAXPwAsAwQCcgjfgHIwABgx8Bl/AV+eb89356fxao/t7jeYJ+Gc5v/8AkCZmtQ==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        sha1_base64="Y+Cs7jyPe1l1f5dY2cLehSpkxTI=">AAAEMHicdZPdbtMwFMe9hY9RPraxS24iKiQuQhWnbdrdTeMCLsdHt0ltNTmOm1p17Mh2gCoKb7FbeAeeBq4QtzwFTpqishorUU6Of//jc/6So4xRpX3/x86uc+v2nbt791r3Hzx8tH9w+PhciVxiMsKCCXkZIUUY5WSkqWbkMpMEpREjF9HiZbV/8YFIRQV/r5cZmaYo4XRGMdImNX5HcPX9POzAq4O23/Hr5W4HsAnaoFlnV4fO/iQWOE8J15ghpcbQz/S0QFJTzEjZmuSKZAgvUELGJuQoJWpa1D2X7jOTid2ZkObl2q2zm4oCpUot08iQKdJzdXOvStr2xrmeDacF5VmuCcerg2Y5c7VwKwPcmEozNFuaAGFJTa8uniOJsDY2tVqTmMyMl3U/hUZYvIhYTsri7avTsggHHuwNvaA3KC1gjORiA+72vePQg4O+jWU0mesNGAYehD1TuWejE0kIb8j+0INB6HWtZbNcZuxvTWjQY1Oza0OFRDxZo0Efmsl6HvRD+/lo2ZCD0Ksfg3HyEYs0RTwuJhVWjzOGU/NHPuktB9uwtIhWo9lUzdB2WTOoTbf2wC5sxrYJ1478r1Hjgb3PypxKZK4QvHlhtoPzoAPDTvgmaJ+cNpdpDzwBT8FzAMEAnIDX4AyMAAYCXIMv4Kvzzfnu/HR+rdDdnUZzBP5Zzu8/ItZnpQ==</latexit>




                                                                         <latexit sha1_base64="6noIpgTgku6ID/9BykaZrp42tCA=">AAAELnicdZPNjtMwEMe9G2CX8rEfHLlEVEgcQhWnbdq9rZYDHBdEdxe11cpxpqlVx4kcB7aK8hRc4R14GiQOiCuPgZOmqGyNlUjj8e8/nvlLDlLOMuW6P3Z2rTt37+3t3289ePjo8cHh0fFFluSSwogmPJFXAcmAMwEjxRSHq1QCiQMOl8HiVXV++RFkxhLxXi1TmMYkEmzGKFE69QHiAMKQiej6sO123HrZ2wFugjZq1vn1kXUwCROaxyAU5STLxthN1bQgUjHKoWxN8gxSQhckgrEOBYkhmxZ1x6X9XGdCe5ZI/Qtl19lNRUHiLFvGgSZjoubZ7bMqaTob52o2nBZMpLkCQVcXzXJuq8SuxrdDJoEqvtQBoZLpXm06J5JQpU1qtSYhzLSTdT+FIjR5GfAcyuLd67Oy8AcO7g0drzcoDWBI5GID7vadE9/Bg76J5Syaqw0Yew7GPV25Z6IjCSAasj90sOc7XWPZNJcp/1sTa/RE1+ya0EQSEa1Rr4/1ZD0Hu775frJsyIHv1J/GBHyiSRwTERaTCqvHGeOp3sGN2nKwjUuDaDWaSdUMbZY1g5p0aw/MwmZsk3DtyP8a1R6Y+6zMqUT6CeHbD2Y7uPA62O/033rt07PmMe2jp+gZeoEwGqBT9AadoxGiKEaf0Rf01fpmfbd+Wr9W6O5Oo3mC/lnW7z+zDmdF</latexit>




                                                                                     ion
discuss prior work on stream fusion, as well as work on deeply em-        deep           8.1
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        <latexit sha1_base64="hdP9vKKWnmiR8Q+8JZxAiywJCQY=">AAAEKXicdZPNjtMwEMe9Gz6W8rG7cOQSUSFxCFWctmn3tloOcFwQ3V2prVaOM22tOk5kO0AV5RW4wjvwNNyAKy+Ck6aobI2VSOPx7z+e+UuOMs6U9v2fe/vOrdt37h7ca91/8PDR4dHx4wuV5pLCiKY8lVcRUcCZgJFmmsNVJoEkEYfLaPmqOr/8AFKxVLzXqwymCZkLNmOU6CoVA2TXR22/49fL3Q1wE7RRs86vj53DSZzSPAGhKSdKjbGf6WlBpGaUQ9ma5AoyQpdkDmMTCpKAmhZ1s6X73GRid5ZK8wvt1tltRUESpVZJZMiE6IW6eVYlbWfjXM+G04KJLNcg6PqiWc5dnbrV5G7MJFDNVyYgVDLTq0sXRBKqjT+t1iSGmTGx7qfQhKYvI55DWbx7fVYW4cDDvaEX9AalBYyJXG7B3b53Enp40LexnM0XegvGgYdxz1Tu2ei5BBAN2R96OAi9rrVslsuM/62JDXpianZtaCqJmG/QoI/NZD0P+6H9frJqyEHo1Z/BBHykaZIQEReTCqvHGeOp2cEnveNgG5cW0Xo0m6oZ2i5rBrXpNh7Yhc3YNuHGkf81ajyw91mZU4nME8I3H8xucBF0cNjpvw3ap2fNYzpAT9Ez9AJhNECn6A06RyNE0QJ9Rl/QV+eb89354fxao/t7jeYJ+mc5v/8AWu9lEg==</latexit>




bedded libraries for operations on dictionaries and their compilers. embedding               Section 8.2
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  <latexit sha1_base64="r2W/1FZUIJlDHYwvrZCoIjdq6oY=">AAAEMHicdZPdbtMwFMe9hY9RPraxS24iKiQuQhWnbdrdTeMCLsdHt0ltNTmOm1p17Mh2gCoKb7FbeAeeBq4QtzwFTpqishorUU6Of//jc/6So4xRpX3/x86uc+v2nbt791r3Hzx8tH9w+PhciVxiMsKCCXkZIUUY5WSkqWbkMpMEpREjF9HiZbV/8YFIRQV/r5cZmaYo4XRGMdImNX5HcPX9POwEVwdtv+PXy90OYBO0QbPOrg6d/UkscJ4SrjFDSo2hn+lpgaSmmJGyNckVyRBeoISMTchRStS0qHsu3WcmE7szIc3LtVtnNxUFSpVappEhU6Tn6uZelbTtjXM9G04LyrNcE45XB81y5mrhVga4MZVmaLY0AcKSml5dPEcSYW1sarUmMZkZL+t+Co2weBGxnJTF21enZREOPNgbekFvUFrAGMnFBtzte8ehBwd9G8toMtcbMAw8CHumcs9GJ5IQ3pD9oQeD0Otay2a5zNjfmtCgx6Zm14YKiXiyRoM+NJP1POiH9vPRsiEHoVc/BuPkIxZpinhcTCqsHmcMp+aPfNJbDrZhaRGtRrOpmqHtsmZQm27tgV3YjG0Trh35X6PGA3uflTmVyFwhePPCbAfnQQeGnfBN0D45bS7THngCnoLnAIIBOAGvwRkYAQwEuAZfwFfnm/Pd+en8WqG7O43mCPyznN9/ACaYZ6Y=</latexit>




                                                                         <latexit sha1_base64="6noIpgTgku6ID/9BykaZrp42tCA=">AAAELnicdZPNjtMwEMe9G2CX8rEfHLlEVEgcQhWnbdq9rZYDHBdEdxe11cpxpqlVx4kcB7aK8hRc4R14GiQOiCuPgZOmqGyNlUjj8e8/nvlLDlLOMuW6P3Z2rTt37+3t3289ePjo8cHh0fFFluSSwogmPJFXAcmAMwEjxRSHq1QCiQMOl8HiVXV++RFkxhLxXi1TmMYkEmzGKFE69QHiAMKQiej6sO123HrZ2wFugjZq1vn1kXUwCROaxyAU5STLxthN1bQgUjHKoWxN8gxSQhckgrEOBYkhmxZ1x6X9XGdCe5ZI/Qtl19lNRUHiLFvGgSZjoubZ7bMqaTob52o2nBZMpLkCQVcXzXJuq8SuxrdDJoEqvtQBoZLpXm06J5JQpU1qtSYhzLSTdT+FIjR5GfAcyuLd67Oy8AcO7g0drzcoDWBI5GID7vadE9/Bg76J5Syaqw0Yew7GPV25Z6IjCSAasj90sOc7XWPZNJcp/1sTa/RE1+ya0EQSEa1Rr4/1ZD0Hu775frJsyIHv1J/GBHyiSRwTERaTCqvHGeOp3sGN2nKwjUuDaDWaSdUMbZY1g5p0aw/MwmZsk3DtyP8a1R6Y+6zMqUT6CeHbD2Y7uPA62O/033rt07PmMe2jp+gZeoEwGqBT9AadoxGiKEaf0Rf01fpmfbd+Wr9W6O5Oo3mC/lnW7z+zDmdF</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           <latexit sha1_base64="xoyZPWdbq4/5hVGcc4bThtu+BXQ=">AAAEL3icdZPdbtMwFMe9hY9RPrbBJTcRFdKQwhSnbdrdTXABlwPRbaKtJsc5ba06TmQ7QBXlLbiFd+BpEDeIW94CJ01RWY2VSCfHv//xOX/FUcaZ0r7/Y2fXuXHz1u29O6279+4/2D84fHiu0lxSGNKUp/IyIgo4EzDUTHO4zCSQJOJwES1eVvsXH0Aqlop3epnBJCEzwaaMEm1S749ommSMg3x2ddD2j/16udsBboI2atbZ1aGzP45TmicgNOVEqRH2Mz0piNSMcihb41xBRuiCzGBkQkESUJOibrl0n5pM7E5TaV6h3Tq7qShIotQyiQyZED1X1/eqpG1vlOvpYFIwkeUaBF0dNM25q1O3mt+NmQSq+dIEhEpmenXpnEhCtXGp1RrHMDVW1v0UmtD0ecRzKIu3r16URdj3cHfgBd1+aQFjIhcbcKfnnYQe7vdsLGezud6AceBh3DWVuzZ6JgFEQ/YGHg5Cr2Mtm+Uy439rYoOemJodG5pKImZrNOhhM1nXw35oP58sG7IfevVjMAEfzd+TEBEX4wqrxxnhifmCT3rLwTYuLaLVaDZVM7Rd1gxq0609sAubsW3CtSP/a9R4YO+zMqcSmSuEr1+Y7eA8OMbhce9N0D4dNJdpDz1GT9ARwqiPTtFrdIaGiCKBPqMv6Kvzzfnu/HR+rdDdnUbzCP2znN9/AAouZ1I=</latexit>




                                                                        (compiler)
Figure 7 gives an overview of how our work relates to prior work Fig. 7. Related work overview
on shallowly embedded stream fusion, and prior work on deeply
embedded approaches to domain-specific compilation of operations on associative arrays.

8.1    Stream Fusion on Lists
The idea of fusing combinators dates back to Wadler’s early work on deforestion [31], where
combinators such as sum, map, and upto could be fused if expressed in a treeless form. By contrast,
the work by Gill et al. [11] allows any programs as input and uses two combinators build and foldr
for fusion, enabling many standard list functions. The build/foldr rule cannot, however, handle
a zip combinator or functions that use accumulators, such as foldl. Svenningsson [30] takes a
different approach, using unfoldr (to build lists) and destroy (to consume lists), which enables the
use of accumulator functions but cannot handle nested lists or list comprehension.
   Coutts et al. [7] propose a generalized stream approach that solves the above problems, including
handling of zip, concat, and list comprehension. In contrast to previous work, this approach uses
an explicit co-structure: the Stream type. The key idea is to use two functions, stream and unstream,
to convert between lists and streams and eliminate such pairs using rewriting rules. Another idea
introduced in this work is to use Skip, which is not necessary for the semantics but essential for the
implementation. The stream fusion work is implemented as a Haskell library, making use of rewrite
rules for eliminating stream–unstream pairs. Similar to our work, stream fusion relies heavily on
standard optimization phases in the compiler to eliminate temporary data.
   There are several extensions to the stream fusion approach presented by Coutts et al. [7]. Gener-
alized stream fusion [19] extends the ideas of stream fusion with a way to bundle multiple stream
representations, enabling vector instructions and SIMD computation. Although the build/foldr
approach by Gill et al. [11] supported the concatMap function, the original stream fusion work was
implemented as user-level rewrites in GHC, and could not handle concatMap. Farmer et al. [10]
presents a solution that turns concatMap into flatten, a combinator that is specialized on a fixed
state type and step function for the inner stream. Moreover, rewrites are performed using the
GHC plugin HERMIT. In our setting, programs can instead be written naturally directly with a
flattened style. Kiselyov et al. [14] present a library approach called strymonas that enables both
guaranteed high performance and expressiveness. Their approach is based on staging, in this
case, metaprogramming using LMS [25] for Scala and BER MetaOCaml [13]. Similar to the above
approaches, our representation can encode several combinators for stream fusion, including, e.g.,
zip and map. Instead of explicit staging, we use specialization, enabling a limited form of partial
evaluation. In contrast to the work on stream fusion, our work applies to associative arrays.

8.2    Fusion of Associative Arrays using Deep Embedding
Over the last ten years, several research groups have explored compiler support for deeply embedded
sparse collection languages [1, 15, 16, 29]. In these systems, operations on sparse collections such
as tensors, dictionaries, and relations, are implemented separately from the host language, for
example as a LLVM-based runtime compiler inside a C++ library.
  Our indexed stream fusion approach builds on the ideas of the indexed streams of Kovach et al.
[16]. Their Etch system, however, is a deeply embedded library that compiles contraction programs
Fast Collection Operations                                                                                              21


written in a separate domain-specific language. It also compiles contraction programs directly to
C code, and uses the indexed stream abstraction only for verification. In contrast, we show how
indexed streams can be written as an extensible library and how fusion can be carried out by the
host language itself.
   Shaikhha et al. [29] proposed a functional language (SDQL) over semi-ring dictionaries and
showed how it expresses both relational and linear algebra. They also propose a deeply embedded
compilation approach that fuses semi-ring operations over these dictionaries. Unlike indexed
streams, SDQL is restricted to collections that support lookup (e.g., a hash map). Shaikhha [27]
also showed how to fuse recursive operations on monoid dictionaries, which can represent sparse
linear algebra (e.g., the nested operations required for matrix multiplication). The fusion approach
removes temporaries within the recursive operations, relies on staged compilation, and restricts
the underlying dictionary data structures.
   Another line of work on compilers for sparse collections are on compiling sparse linear/tensor
algebra. The first approach was the MT1 compiler of Bik and Wijshoff [2, 3, 4]. The TACO com-
piler [15] developed a different approach that generalized to sparse tensor algebra and supported
fusion, by generating co-iteration code over sparse data structures. It also supported user-defined
data structures [6] and scheduling [26]. The Finch compiler [1] further generalized the co-iteration
approach. These systems, however, are limited to sparse tensor algebra and are also implemented
as deeply embedded compilers inside C++ or Julia libraries, in large part due to their complexity.
   Finally, the C# language provides the LINQ library [21] for querying in-memory collections
and other iterables. The LINQ query language is SQL, which is higher level than our collection
operators and can be built on top of them. Furthermore, users can insert new data structures into
LINQ by overloading the Enumerable interface, but the execution strategy is left to client code, so
any domain-specific compilation approach must be implemented as a deeply embedded compiler.

9   CONCLUSION
In this paper we have shown how to develop a library that makes indexed iteration over associative
data structures as convenient as sequential iteration without sacrificing performance. We hope
that this technique might become as pervasive as the iterator so that users are free to write correct,
performant data processing applications that avoid the friction of piping data into a database
instance or domain specific language. We believe this work puts associative array manipulations on
a solid foundation, enabling library development for general purpose languages so that specialized
compilers are no longer needed.

REFERENCES
 [1] Willow Ahrens, Daniel Donenfeld, Fredrik Kjolstad, and Saman Amarasinghe. 2023. Looplets: A Language for Structured
     Coiteration. In Proceedings of the 21st ACM/IEEE International Symposium on Code Generation and Optimization. 41–54.
 [2] Aart JC Bik and Harry AG Wijshoff. 1993. Advanced compiler optimizations for sparse computations. In Proceedings
     of the 1993 ACM/IEEE conference on Supercomputing. 430–439.
 [3] Aart JC Bik and Harry AG Wijshoff. 1993. Compilation techniques for sparse matrix computations. In Proceedings of
     the 7th international conference on Supercomputing. 416–424.
 [4] Aart J. C. Bik and Harry A. G. Wijshoff. 1996. Automatic data structure selection and transformation for sparse matrix
     computations. IEEE Transactions on Parallel and Distributed Systems 7, 2 (1996), 109–126.
 [5] William Brandon, Benjamin Driscoll, Frank Dai, Wilson Berkow, and Mae Milano. 2023. Better Defunctionalization
     Through Lambda Set Specialization. Proceedings of the ACM on Programming Languages 7, PLDI (2023), 977–1000.
 [6] Stephen Chou, Fredrik Kjolstad, and Saman Amarasinghe. 2018. Format Abstraction for Sparse Tensor Algebra
     Compilers. Proc. ACM Program. Lang. 2, OOPSLA, Article 123 (Oct. 2018), 30 pages. https://doi.org/10.1145/3276493
 [7] Duncan Coutts, Roman Leshchinskiy, and Don Stewart. 2007. Stream Fusion: From Lists to Streams to Nothing at All.
     SIGPLAN Not. 42, 9 (Oct. 2007), 315–326. https://doi.org/10.1145/1291220.1291199
22                                                                                                           Kovach et al.


 [8] Stephen Dolan. 2013. Fun with semirings: a functional pearl on the abuse of linear algebra. In Proceedings of the 18th
     ACM SIGPLAN international conference on Functional programming. 101–110.
 [9] Conal Elliott. 2019. Generalized Convolution and Efficient Language Recognition. (2019). arXiv:1903.10677 [cs.PL]
[10] Andrew Farmer, Christian Hoener zu Siederdissen, and Andy Gill. 2014. The HERMIT in the stream: fusing stream
     fusion’s concatMap. In Proceedings of the ACM SIGPLAN 2014 Workshop on Partial Evaluation and Program Manipulation
     (San Diego, California, USA) (PEPM ’14). Association for Computing Machinery, New York, NY, USA, 97–108. https:
     //doi.org/10.1145/2543728.2543736
[11] Andrew Gill, John Launchbury, and Simon L. Peyton Jones. 1993. A short cut to deforestation. In Proceedings of the
     Conference on Functional Programming Languages and Computer Architecture (Copenhagen, Denmark) (FPCA ’93).
     Association for Computing Machinery, New York, NY, USA, 223–232. https://doi.org/10.1145/165180.165214
[12] Todd J. Green, Grigoris Karvounarakis, and Val Tannen. 2007. Provenance Semirings. In Proceedings of the Twenty-Sixth
     ACM SIGMOD–SIGACT–SIGART Symposium on Principles of Database Systems (Beijing, China) (PODS ’07). Association
     for Computing Machinery, New York, NY, USA, 31–40. https://doi.org/10.1145/1265530.1265535
[13] Oleg Kiselyov. 2014. The design and implementation of BER MetaOCaml: System description. In Functional and Logic
     Programming: 12th International Symposium, FLOPS 2014, Kanazawa, Japan, June 4-6, 2014. Proceedings 12. Springer,
     86–102.
[14] Oleg Kiselyov, Aggelos Biboudis, Nick Palladinos, and Yannis Smaragdakis. 2017. Stream fusion, to completeness. In
     Proceedings of the 44th ACM SIGPLAN Symposium on Principles of Programming Languages (POPL ’17). ACM, 285–299.
     https://doi.org/10.1145/3093333.3009880
[15] Fredrik Kjolstad, Shoaib Kamil, Stephen Chou, David Lugato, and Saman Amarasinghe. 2017. The Tensor Algebra
     Compiler. Proceedings of the ACM on Programming Languages 1, OOPSLA (2017), 1–29. https://doi.org/10.1145/3133901
[16] Scott Kovach, Praneeth Kolichala, Tiancheng Gu, and Fredrik Kjolstad. 2023. Indexed Streams: A Formal Intermediate
     Representation for Fused Contraction Programs (PLDI 2023). Association for Computing Machinery. https://doi.org/
     10.1145/3591268
[17] Amanda Liu, Gilbert Louis Bernstein, Adam Chlipala, and Jonathan Ragan-Kelley. 2022. Verified Tensor-Program
     Optimization via High-Level Scheduling Rewrites. Proc. ACM Program. Lang. 6, POPL, Article 55 (Jan. 2022), 28 pages.
     https://doi.org/10.1145/3498717
[18] Anton Lorenzen, Daan Leijen, and Wouter Swierstra. 2023. FP2 : Fully in-Place Functional Programming (TR). Techni-
     cal Report MSR-TR-2023-19. Microsoft. https://www.microsoft.com/en-us/research/publication/fp2-fully-in-place-
     functional-programming/ Extended version of the ICFP’23 publication.
[19] Geoffrey Mainland, Roman Leshchinskiy, and Simon Peyton Jones. 2013. Exploiting vector instructions with generalized
     stream fusion. SIGPLAN Not. 48, 9 (sep 2013), 37–48. https://doi.org/10.1145/2544174.2500601
[20] Nicholas D Matsakis and Felix S Klock II. 2014. The rust language. In ACM SIGAda Ada Letters, Vol. 34. ACM, 103–104.
[21] Microsoft. 2024. Language Integrated Query (LINQ). https://s-arash.github.io/ascent/cc22main-p95-seamless-deductive-
     inference-via-macros.pdf
[22] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem Prover and Programming Language. In
     International Conference on Automated Deduction. Springer, 625–635. https://doi.org/10.1007/978-3-030-79876-5_37
[23] Hung Q Ngo, Ely Porat, Christopher Ré, and Atri Rudra. 2018. Worst-case optimal join algorithms. Journal of the ACM
     (JACM) 65, 3 (2018), 1–40. https://doi.org/10.1145/3180143
[24] Hung Q Ngo, Christopher Ré, and Atri Rudra. 2014. Skew strikes back: New developments in the theory of join
     algorithms. ACM SIGMOD Record 42, 4 (2014), 5–16. https://doi.org/10.1145/2590989.2590991
[25] Tiark Rompf and Martin Odersky. 2010. Lightweight modular staging: a pragmatic approach to runtime code generation
     and compiled DSLs. In Proceedings of the Ninth International Conference on Generative Programming and Component
     Engineering (Eindhoven, The Netherlands) (GPCE ’10). Association for Computing Machinery, New York, NY, USA,
     127–136. https://doi.org/10.1145/1868294.1868314
[26] Ryan Senanayake, Changwan Hong, Ziheng Wang, Amalee Wilson, Stephen Chou, Shoaib Kamil, Saman Amarasinghe,
     and Fredrik Kjolstad. 2020. A Sparse Iteration Space Transformation Framework for Sparse Tensor Algebra. Proc.
     ACM Program. Lang. 4, OOPSLA, Article 158 (Nov. 2020), 30 pages. https://doi.org/10.1145/3428226
[27] Amir Shaikhha. 2022. Deep Fusion for Efficient Nested Recursive Computations. In Proceedings of the 21st ACM SIGPLAN
     International Conference on Generative Programming: Concepts and Experiences (Auckland, New Zealand) (GPCE 2022).
     Association for Computing Machinery, New York, NY, USA, 33–44. https://doi.org/10.1145/3564719.3568698
[28] Amir Shaikhha, Andrew Fitzgibbon, Simon Peyton Jones, and Dimitrios Vytiniotis. 2017. Destination-Passing Style
     for Efficient Memory Management. In Proceedings of the 6th ACM SIGPLAN International Workshop on Functional
     High-Performance Computing (Oxford, UK) (FHPC 2017). Association for Computing Machinery, New York, NY, USA,
     12–23. https://doi.org/10.1145/3122948.3122949
[29] Amir Shaikhha, Mathieu Huot, Jaclyn Smith, and Dan Olteanu. 2022. Functional collection programming with semi-
     ring dictionaries. Proceedings of the ACM on Programming Languages 6, OOPSLA1 (2022), 1–33. https://doi.org/10.
Fast Collection Operations                                                                                        23


     1145/3527333
[30] Josef Svenningsson. 2002. Shortcut fusion for accumulating parameters &amp; zip-like functions. In Proceedings
     of the Seventh ACM SIGPLAN International Conference on Functional Programming (Pittsburgh, PA, USA) (ICFP ’02).
     Association for Computing Machinery, New York, NY, USA, 124–132. https://doi.org/10.1145/581478.581491
[31] Philip Wadler. 1990. Deforestation: transforming programs to eliminate trees. Theoretical Computer Science 73, 2
     (1990), 231–248. https://doi.org/10.1016/0304-3975(90)90147-A


A    RBTREE SEEK IN RUST

     /// Continue advancing like next() but skip over nodes designated by cmp_fn
     /// cmp_fn should be downwards closed i.e., if cmp_fn(a), then for all b < a,
      cmp_fn(b)
     /// Takes O(log n) time, where n=size of tree
     #[inline]
     fn seek(self, cmp_fn: impl Fn(&K) -> bool) -> NodePtr<K, V> {
          if self.is_null() || !cmp_fn(unsafe { &(*self.0).key }) {
               return self; // minor edge case: never advance backwards
          }

         // let ‵ target‵ be the least node not satisfying ‵ cmp_fn‵ (the one we want to
     return)
         // Let ‵ ancestor‵ be the least ancestor of ‵ candidate‵ greater than it.
         // We maintain the following loop invariants:
         // 1. If target < ancestor, either target = candidate or target is a
     descendant of current
         // 2. current < ancestor
         // Note that these invariants always hold if current = candidate.right() and
     target > candidate
         let mut candidate = self;
         let mut current = self.right();
         // In principle, this loop should be ‵ while !candidate.is_null() &&
     cmp_fn(unsafe { &(*candidate.0).key })‵ (i.e., target > candidate).
         // However, for efficiency, we instead write this as a loop with explicit
     breaks when the condition is false
         // (We′ ve also explicitly checked the condition at the beginning of the
     function)
         loop {
             // For optimization, tell the compiler that the loop condition holds
     explicitly
             if candidate.is_null() { unsafe { unreachable_unchecked() }; }
             let parent = candidate.parent();
             let is_left_child = parent.is_null() || parent.left() == candidate;
             // We will assign candidate to its parent, but in the comments below, ‵
     candidate‵ refers to the old value of candidate.
             // From target > candidate (loop condition), the loop invariant becomes:
     if target < ancestor, target is a descendant of current
             // (target = candidate is impossible)
             candidate = parent;
             if is_left_child {
                  // Case 1: candidate is a left child (so ancestor = parent)
                  if candidate.is_null() || !cmp_fn(unsafe { &(*candidate.0).key }) {
                       // Case 1a: target <= parent
                       // The loop invariant says if target < parent, target is a
     descendant of current.
24                                                                               Kovach et al.


                     // Thus, either target = parent or target is a descendant of
     current.
                     // Also, (2) clearly continues to hold since ancestor can only
     increase.
                      // Thus, the loop invariants continue to hold with candidate :=
     parent (and the loop ends).
                      break;
                 } else {
                      // Case 1b: target > parent
                      // In this case, assign current = parent.right() and continue the
     loop.
                      // The invariants hold because target > parent (just like in
     initialization).
                      current = candidate.right();
                 }
             } else {
                 // Case 2: candidate is a right child
                 // In this case, ancestor does not change when candidate := parent
     since parent < candidate
                 // so the invariant continues to hold with candidate := parent.
     Similarly, we don′ t
                 // need to check the loop condition to see if we should break since
     target > candidate > parent.
                 // This entire case could be a no-op. For optimization purposes,
     however, we do one step
                 // of a binary search for target from current
                 // (which maintains the invariant that if target was a descendant of
     current, it still will be).
                 if !current.is_null() {
                      if cmp_fn(unsafe { &(*current.0).key }) {
                           current = current.right();
                      } else {
                           // If we find target <= current, then since current < ancestor
                           // we know target is a descendant of current.
                           // Thus we can end the loop early (you can check that the
     invariants still hold).
                           candidate = current;
                           current = current.left();
                           break;
                      }
                 }
             }
         }

         // At the end of the loop, we must have target <= candidate. Thus, target <
     ancestor,
         // so either target = candidate or target is a descendant of current. We do a
     binary search from current for target.
         while !current.is_null() {
             if cmp_fn(unsafe { &(*current.0).key }) {
                  current = current.right();
             } else {
                  candidate = current;
                  current = current.left();
Fast Collection Operations                                                                                           25


              }
          }
          candidate
     }


B    BACKGROUND: STREAM FUSION TO INDEXED STREAMS
This section contains background material on stream fusion [7] and indexed streams [16]. It is
a more gradual version of Section 4.1. We explain their relationship by starting with streams
representing sequences of data and gradually augmenting their definition until we arrive at a
representation for streams that represent associative arrays. Thus, we show how indexed streams
can be conceived of as a gradual evolution from sequential streams. We will highlight a few points
where further attention is required to enable application of the indexed stream concept to practical
functional programming. All code examples in this section are in Lean.

Sequential Stream Fusion
Stream fusion [7] is an approach to fusing computations on sequential data structures such as lists
and strict arrays. Its key idea is to replace the recursive list definition with an iteration function
that maps a state to an optional value and successive state. The iteration function must be able to
return a special value to signal termination. The following code defines an inductive datatype Step
with three constructors4 and a structure (record) Stream with named fields:
inductive Step (𝜎 α : Type)
  | done
  | skip (state : 𝜎)
  | emit (state : 𝜎) (value : α)

structure Stream (α : Type) where
  𝜎 : Type
   q : 𝜎
   next : 𝜎 → Step 𝜎 α

A Stream contains a state type 𝜎, a state q, and transition function next. At a given state, the next
function may return done, signaling the absence of any more values in the stream, skip, indicating
that no value is produced at the current state and yielding a new state, or emit, yielding a value
and successor state.
  Now a function such as map can be defined non-recursively:
def map : (α → β) → Stream α → Stream β := fun f s => {
  s with
  next := fun state =>
    match s.next state with
    | done             => done
    | skip state       => skip state
    | emit state value => emit state (f value)
}

The function map returns a structure of type Stream by updating field next of s using the with
construct. This transformation to non-recursive form aids the optimizer: it is more straightforward
to inline successive operations, potentially avoiding both list cell allocations and allocations from
4 The constructor emit has the same meaning as yield in the original paper on stream fusion [7]. We use the name emit to

make it consistent throughout the paper.
26                                                                                         Kovach et al.


user code. The pioneering stream fusion work [7] showed that standard compilation techniques are
sufficient to transform pipelines built from map, filter, zip, and other operations into a single loop.
  The streams we have seen so far can be given a semantics in terms of lists:
partial def eval : Stream α → List α := fun {q, next} =>
  match next q with
  | done => []
  | skip q => eval {q, next}
  | emit q value => value :: eval {q, next}
This implements the correspondence between done with the empty list and emit with list cons. The
example function is partial, to allow general recursion without requiring Lean to prove termination.

Sequential Container Fusion
After evaluating a stream, each value is equipped with an implicit position within the overall output
sequence; this position is of semantic relevance for combinators such as zip, which pairs together
the output values of two streams one by one. This positional semantics works fine for sequences,
but we are building towards a stream representation for data structures encoding associative arrays.
In this setting, each output value is associated with a particular key, or index, not its position.
   Taking inspiration from Kovach et al. [16], we make a new definition with a type parameter 𝜄,
values of which we call indices, and we allow the new emit constructor to produce both an index
and a value:
inductive Step (𝜎 𝜄 α : Type) where
  | done
  | skip (state : 𝜎)
  | emit (state : 𝜎) (index : 𝜄) (value : α)
This change allows for streams that do not produce output at every index. Semantically, we want a
stream using this new Step type to represent an associative array, which is most easily specified
abstractly as a mapping of type 𝜄 → Option 𝛼. We define the abstract semantics like so:
-- a map with no entries
def zero : 𝜄 → Option α := fun _ => none

-- a map with one entry
def singleton : 𝜄 → α → 𝜄 → Option α := fun i v x =>
  if x = i then some v else none

-- a map containing all entries yielded by the stream
partial def eval [Add α] : Stream 𝜄 α → (𝜄 → Option α) := fun {q, next} =>
    match next q with
    | done => zero
    | skip q => eval {q, next}
    | emit q i v => (singleton i v) + eval {q, next}
Notice the close similarity to the previous eval function. The result of eval is a function with
finitely many non-none values. We require that the values can be combined using Add in case the
stream yields the same index at multiple steps. In contrast to the previous list-based eval function,
this one does not produce an efficient representation of its output (the result is a sum of closures).
Nevertheless, it mirrors the structure of the efficient one we will derive in a later section.
   This representation is already sufficient to fuse filter and map operations. These operations
operate on all the elements of one collection, so there is no harm in treating it as a sequence to
apply them.
Fast Collection Operations                                                                            27


   Intersection/Multiplication. Now we turn to combining data from multiple streams. The most
widely used data processing combinator is probably the natural join. Prior work has shown that join
can be obtained in full generality from a simple building block: the product of two streams, which
yields values at indices shared by both streams. That is, when the value type 𝛼 has a multiplication
operator satisfying 0 · 𝑎 = 𝑎 · 0 = 0, there is a natural way of lifting it to act on an entire stream. A
key insight of our work is that this single operation generalizes surprisingly well, enabling both
efficient compilation and new operations and applications, including relational join and sparse
tensor operations. Here is our first pass at a definition:
def mul [Mul α] : Stream 𝜄 α → Stream 𝜄 α → Stream 𝜄 α := fun a b => {
  q := (a.q, b.q),
  next := fun q =>
    match a.next q.fst, b.next q.snd with
    | done, _                    => done
    | _, done                    => done
    | skip q1 , _                => skip (q1 , q.snd)
    | _, skip q2                 => skip (q.fst, q2 )
    | emit q1 i1 v1 ,
      emit q2 i2 v2 =>
      match compare i1 i2 with
      | .lt                      => skip (q1 , q.snd)
      | .gt                      => skip (q.fst, q2 )
      | .eq                      => emit (q1 , q2 ) i1 (v1 * v2 )
}
The correctness of this function relies on strict monotonicity of the input streams, the assumption
that the sequence of indices yielded by emit always increases. The function merges together the
index sequences for a and b, emitting the product of values whenever indices match. Notice that
when either input is sparse (non-zero at relatively few values of 𝜄) the output is likewise sparse,
because it only yields values at indices in the intersection.
  A small refactor. However, this definition computes the intersection inefficiently. The issue is
that it inevitably traverses all of the states of at least one stream before terminating. In the final
case branch, we know that the larger of 𝑖 1 and 𝑖 2 is a lower bound for the next non-zero output. If
the other stream is traversing a realistic data structure, it likely supports a way of quickly finding
that index. Thus, there is a missed opportunity to quickly advance or seek the stream forward.
  Before describing a solution, we will make a semantics-preserving change to the stream definition.
The goal of this change is to remove the need for the Step type, which ultimately simplifies the
definition and compilation of combinators down the line. We call this a sequential stream:
structure Stream (𝜄 α : Type) where
   (𝜎 : Type) (q : 𝜎)
   valid : 𝜎 → Bool                          -- "done"
   next : {x : 𝜎 // valid x} → 𝜎
   ready : {x : 𝜎 // valid x} → Bool         -- "skip"
   index : {x : _ // ready x} → 𝜄            -- "emit"
   value : {x : _ // ready x} → α            -- "emit"
   We have labeled each function with the Step constructor it approximately corresponds to (next
still corresponds to itself). In addition to explaining why this is equivalent to the previous Stream
definition, we take this opportunity to explain some Lean notation. In particular, the notation
{x : T // P x} is notation for a subtype: an element of {x : T // P x} is a pair of a value 𝑥 : 𝑇
and a proof that 𝑃 holds for 𝑥. These proofs are eliminated during code generation. The type 𝑇 can
be inferred from the type of 𝑃, so it is generally possible to omit it.
28                                                                                                           Kovach et al.


    The valid predicate is used to signal termination. When the next function of the previous
formulation would return done, in the present formulation it returns a state 𝑞 ′ where valid q′ =
false. The ready predicate, which can be applied only to valid states, marks states that yield output.
When the previous stream would return skip q′ , instead here we have ready q′ = false.
    Finally, the successor state and yielded index/value pair are accessed using the remaining three
methods. In the prior case of next q = emit q′ i v, we have next q = q′ , index q′ = i, and value
q ′ = v.

Indexed Streams
We can present the final indexed stream formulation: 5
structure Stream (𝜄 α : Type) where
   (𝜎 : Type) (q : 𝜎)
   valid : 𝜎 → Bool
   index : {x // valid x} → 𝜄           -- available whenever valid
   seek : {x // valid x} → 𝜄 × Bool → 𝜎 -- replaces ‵ next‵ :
   ready : {x // valid x} → Bool
   value : {x // ready x} → α
   Notice that we have only made two small changes:
    (1) addition of an index and boolean parameter to next, which we rename seek
    (2) index returns a value at all valid states, not just ready states.
   As previously noted, the purpose of the 𝜄 parameter to seek is to allow seek q (i, b) to return a
state that makes progress toward a state 𝑞 ′ with index at least 𝑖; it may skip any states with lesser
index. The boolean parameter essentially indicates whether the stream may advance past the given
index (this technical detail plays an important role during evaluation and proving correctness,
which we elaborate later on).
   The latter change to index is simple: we require that index provides a lower bound on the next
non-zero value. When two data structures are traversed simultaneously, as in the multiplication
combinator, this index information can enable the seek method of the secondary stream to advance
more effectively, even when neither stream is ready to provide a value.
   These two changes in fact generalize the previous definition. Given seek, the canonical definition
of next is next q := seek q (index q, ready q), which asks the stream to make progress towards
moving past the index it is currently at. Conversely, given next, we can always define seek by
simply calling next if the requested index is at least the current index (and doing nothing otherwise).
Many data structures, however, offer more efficient implementations of seek.
   Hierarchical data. Finally, since a stream encodes a particular associative array (which can be
thought of as a function), we encourage the reader to regard a stream as a sort of function. We
adopt the notation 𝜄 →𝑠 𝛼 for the type Stream 𝜄 𝛼 . This suggests the possibility of nested stream
types such as N →𝑠 N →𝑠 R; this is a stream whose values are streams whose values are real
numbers. Such streams can encode hierarchical data, for instance matrices, graphs, or data tables.
   Array programming languages traditionally support one indexing type: the natural numbers.
Here, we allow arbitrary ordered types. Each level of a stream is annotated with a label. We refer to
a (label, type) pair as an attribute or level, and the sequence of attributes for a stream is its shape.




5 In order to avoid confusion with the stream fusion skip constructor, we use the term “seek” for what is called “skip” in

prior work [16].
