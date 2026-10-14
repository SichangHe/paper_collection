                                         Unfolding Iterators: Specification and Verification
                                                of Higher-Order Iterators in OCaml

                                                                    Ion Chirica and Mário Pereira

                                                   NOVA LINCS, Nova School of Science and Technology, Portugal
arXiv:2506.20310v1 [cs.PL] 25 Jun 2025




                                               Abstract. Albeit being a central notion of every programming language,
                                               formally and modularly reasoning about iteration proves itself to be a
                                               non-trivial feat, specially in the context of higher-order iteration. In this
                                               paper, we present a generic approach to the specification and deductive
                                               verification of higher-order iterators, written in the OCaml language. Our
                                               methodology follows two key principles: first, the usage of the Gospel
                                               specification language to describe the general behaviour of any iteration
                                               schema; second, the usage of the Cameleer framework to deductively verify
                                               that every iteration client is correct with respect to its logical specification.
                                               To validate our approach we develop a set of verified case studies, ranging
                                               from classic list iterators to graph algorithms implemented in the widely
                                               used OCamlGraph library.


                                         1    Introduction

                                         Iteration plays a crucial role in every programming language. It comes in various
                                         shapes, be it through cycles, recursive functions or even higher-order iterators.
                                         The usage of an iteration process is normally associated with the need to repeat a
                                         computation, e.g., process every element in a data structure. Nonetheless, despite
                                         our extensive experience with the use of iteration, implementing and ensuring
                                         that an iterative algorithm is exempt from errors remains a non-trivial task.
                                             Testing is a very popular approach to analyze a given program. It is a simple
                                         and fast methodology that can be easily incorporated into traditional development
                                         cycles. However, tests are rarely exhaustive and for that reason, their correctness
                                         guarantees are as limited as their coverage. If we wish to give the highest assurance
                                         of program correctness, we quickly turn to formal methods [18]. This field uses
                                         mathematical tools to reason about program correctness. In particular, we focus
                                         on deductive software verification [12], which translates correctness properties
                                         into logical implications to be proven by a computer. This technique is also known
                                         as formal software proving.
                                             In this work we tackle the problem of formally verifying programs that employ
                                         higher-order iterators. The iteration patterns defined within the class of higher-
                                         order iterators are so common and well established that we believe a generic
                                         specification should be able to formally capture its behaviour. Our purpose is
                                         to establish a quasi -automatic verification methodology, in a way that we avoid
                                         the cumbersome effort of conducting such reasoning in a proof assistant. The
2       I. Chirica, M. Pereira

programs of interest are written in OCaml, a language of the ML family, where
iteration is naturally expressed using higher-order functions. While OCaml allows
combining a functional programming style with imperative mechanisms, notably
memory writes, this turns out to be a challenge for deductive verification tools.
To address these challenges, we present (1) a generic way to specify high-order
iterators where we capture, in first-order logic, essential patterns that any iterator
should adopt; (2) a proof methodology based on translating a higher-order iterator
into an equivalent program in first-order, utilizing the notion of cursor, i.e., a
step-by-step iterator. Our approach is implemented as a set of extensions to the
specification language Gospel [6] and Cameleer [20], a deductive verification tool
for OCaml programs. All the examples are available in an online artifact [7].

2    Background
Reasoning about iteration. The effort to formally reason about iteration is not
novel, having been explored through loop invariants [16], verification condition
generation [11]. More recently, Filliâtre and Pereira [15] proposed a modular
approach using two predicates per iterator: permitted (for values produced during
iteration) and completed (for termination), and a sequence of visited elements.
Exemplifying, when iterating over a sequence s, the permitted predicate ensures
that any sequence of visited elements v must be a valid prefix of s, formally:
         permittedpv, sq fi ||v|| ď ||s|| ^ @i.0 ď i ď ||v|| ùñ vris “ sris
On the other hand, the complete predicate then simply states that the iteration
is finished when the length of the visited sequence v equals the length (|| ¨ ||) of s,
formally captured with:
                            completepv, sq fi ||v|| “ ||s||
    Based on these two predicates, we are able to capture any kind of iteration,
be it over a collection or enumeration of results of an algorithm, be it finite and
deterministic or infinite and non-deterministic [15].

Specification and Verification of OCaml programs. Gospel (Generic Ocaml SPEci-
fication Language) is a behavioural specification language for OCaml interfaces [6].
It is a contract-based, strongly typed language with formal semantics defined
employing translation into Separation Logic [22]. The main goal of Gospel is
to provide a concise and accessible specification language for OCaml interfaces,
which can be used for various purposes. However, with a strong emphasis on
verification with the use of tools that translate Gospel annotated OCaml into
languages understandable by automated theorem provers. Gospel specifications
are added as comments beginning with @, (*@ ... *), at the end of the function
definition. Conversely, Cameleer, is a tool for deductive verification of OCaml
programs, conceived with proof automation in mind [20]. This tool takes Gospel,
additionally supporting implementation specifications, annotated OCaml code and
translates it to an equivalent WhyML [13], which can be verified using automated
provers like CVC5, Alt-Ergo, or Z3, or interactive ones such as Rocq and Isabelle.
                                                          Unfolding Iterators   3

3     Motivating example

To motivate our approach and tool choices, we consider summing a finite, de-
terministic sequence of integers using two classic patterns: recursion and loops.
Later, we revisit this example using cursors and higher-order iterators.
    From a recursive perspective, the function sums elements from upper to lower,
using get to access elements (whose complexity we ignore in the context of this
example). Termination is ensured by making upper the decreasing argument and
bounding both lower and upper within s. We ensure that the result matches
the mathematical sum over that range.
  let rec sum_recursive s lower upper =                         Gospel + OCaml
      if upper ď lower then 0
      else (get s (upper - 1)) + sum_recursive s lower (upper - 1)
    (*@ r = sum_recursive s lower upper
        variant upper
        requires 0 ďřlower ď upper ď ||s||
        ensures r = upper
                      i=lower s[i]*)

Using a cycle, this can be solved by introducing two mutable variables, index to
get the n-th element of a sequence, and acc the accumulator of the sum. In this
cycle, we iterate over the length of s and successively add its elements:
  let sum_cycle s =                                                       OCaml
     let index = ref 0 and acc = ref 0 in
     while !index ă (length s) do

The loop specification first states that the termination measure is given by
a decrease in the to-be visited elements, followed by the invariant: index is
contained within the limits of the sequence and the contents of acc holds the
current sum of the elements on s, up until !index, as follows:
    (*@ variant ||s|| - !index                                 Gospel + OCaml
         invariant 0 ď !index ď ||s|| ^ !acc =              s[i] *)
                                                  ř!index
                                                    i=0
       acc := !acc + (get s !index);
       index := !index + 1;
     done;
     !acc

Finally, the specification of sum_cycle is given by the post-condition that the
result, r, of calling this function equals the logical definition of a sum:
  (*@ r = sum_cycle s                                              Gospel + OCaml
        ensures r =     i=0 s[i]*)
                      ř||s||

This specification we present here is a very high-level one, however, there is a
definition within Gospel’s Standard Library for the summation operator. When
fed to Cameleer, the above specifications and OCaml implementations, will be
translated into a WhyML program for which Why3 generates a total of 9 Verifica-
tion Conditions (VCs), 4 for the recursive definition and 5 for the cycle based
one, all of them quickly dispatched by the Alt-Ergo SMT solver.
4       I. Chirica, M. Pereira

4     Revisiting modular specification for first order iteration

In this section we present a refinement of the existing WhyML cursor specification.
This refinement is a key part of our translation schemas (c.f. Section 6), where
we resort to Why3’s module system to achieve a generic specification for cursors.
    Cursors are defined using two functions, has_next() and next(), testing
whether the iteration has completed, and returning the next element in the
iteration, respectively. Building on the ideas of Filliâtre and Pereira [15], we
propose an extension to their cursors in WhyML. This extension, unable at the
time due to limitations in Why3 to express type invariants, embeds the predicates
permitted and complete within the type of the cursor, as follows:
   type cursor α = abstract {                                            WhyML
      mutable visited   : seq α;
              permitted : seq α Ñ bool;
              complete : seq α Ñ bool;
    } invariant { permitted visited }

The sequence of visited elements, the first field, visited, holds the sequence of
polymorphic elements visited, and the other two are predicates, parameterized
with a sequence of polymorphic elements. By embedding these predicates within
the cursor type, we generalize the iteration to any collection. Additionally, this
allows us to decorate this type definition with a type invariant, stating that: at
any point before a function call, possibly invalidated in between, but fully restored
by the function’s exit, the sequence of visited elements, visited, is permitted.
This type is abstract, that is, its fields are visible in the specification while
being opaque in the implementation.
    This refinement of a cursor and the functions next and has_next are fully
generic, irrespective of which iteration we desire to express. Notwithstanding,
we lack a function that creates a cursor, create. Fundamentally, this function
differs from cursor to cursor, and thus unable to be generic. For that reason, the
definition of this function is delegated to the cursor client, allowing for iterations
over diverse data structures or the specification of custom iteration patterns.
    Coming back to our recurring theme of iterations over sequences, we can
finish the definition of such a cursor by instantiating its fields, like so:
   val create (s: seq α) : (c : cursor α)                                    WhyML
     ensures { result.visited   = empty }
     ensures { result.permitted = (fun v Ñ ||v|| ď ||s|| ^
                                   @ i. 0 ď i ă ||v|| Ñ v[i] = s[i]) }
     ensures { result.complete = (fun v Ñ ||v|| = ||s||) }

The first post-condition is natural, at creation we ensure a cursor with an
empty sequence of visited elements. Afterwards, we give body to the predicates
permitted, with the definition of v being a prefix of the collection to be iterated,
and the complete given by the comparison of both lengths. The direct conclusion
is that by instantiating the pair permitted/complete at the cursor creation, we
claim the same result as the work of Filliâtre and Pereira [15].
                                                          Unfolding Iterators       5

    Having defined a cursor over sequences, let us now see how a client might use
this construct to sum all the elements of a sequence of integers:
  let sum_cursor (s: int seq) : int                                      WhyML
A   ensures { result = sum (fun i Ñ s[i]) 0 (length s) } =
    let acc = ref 0 in
    let c = create s in
B   while has_next c do
        variant { ||s|| - ||c.visited|| }
C     invariant { !acc = sum (fun i Ñ c.visited[i]) 0 ||c.visited|| }
D     let x = next c in
      acc := !acc + x;
    done;
    !acc

Its specification can be given in the following way: in A we ensure that the result
is equal to the mathematical sum1 of all the elements of s; from B to C we find
the test of termination, the cycle variant and invariant, given by the accumulator
being the sum of all the visited elements; finally, in D we produce an element, x,
and the subsequently update to the accumulator with the sum of acc and x.
    If we instantiate Why3 on sum_cursor and the presented specification, we
end up with 6 VCs, three of them concerned with the loop invariants, two with
the preconditions of the next and has_next and the last with the post-condition
of sum_cursor. All were fully dispatched by Alt-Ergo.


5   Higher-order iteration specification

Computing the sum of all elements in a sequence naturally aligns with a well-
known higher-order iteration pattern: a so called fold function. This is ubiquitous
in mainstream languages such as OCaml, Haskell, or Scala. In this section, we
formalize such a computation by considering a parameterized OCaml module,
Sequences, which captures the essence of this higher-order abstraction.
    This module is parameterized over another module S, which specifies a
polymorphic sequence type seq2 and two higher-order functions: fold and iter.
The function fold takes three arguments: a binary function of type α Ñ β Ñ α,
an initial accumulator value of type α, and a sequence of type β seq, returning a
final accumulated value of type α. The second function, iter, applies a function
of type α Ñ unit to each element of a given sequence, solely for its side effects.
    In the Sequences module, we define sum_fold, which computes the sum of a
sequence using fold with the binary sum as the consumer function and initial
value 0. We also define stack_of_seq, which builds a stack from a sequence
using iter, where the consumer function pushes elements onto the stack in-place.
1
  The function sum f l u, defined as the sum ui=l f(i), is included in the Why3
                                                    ř
  Standard Library. https://www.why3.org/stdlib/int.html
2
  This type denotes a sequence: an ordered collection of elements in which repetitions
  are permitted, e.g., lists or arrays. It should not be mistaken with OCaml’s Seq.seq
  type.
6        I. Chirica, M. Pereira



    module Sequences (S : sig                                       OCaml
      type α seq
      val fold : (α Ñ β Ñ α) Ñ α Ñ β seq Ñ α
      val iter : (α Ñ unit) Ñ α seq Ñ unit
    end) = struct
      let sum_fold (s : int S.seq) = S.fold (fun acc x Ñ acc + x) 0 s

      let stack_of_seq s =
        let stack = Stack.create () in
        S.iter (fun x Ñ Stack.push x stack) s; stack
    end
    In the previous section, we presented a generic approach to iteration through
the use of cursors, focusing exclusively on the definition of the create function.
We observed that iteration is a two-fold task: first, abstracting what it means to
iterate over an arbitrary collection; and second, defining the concrete semantics
of the iteration process itself. The former is captured by an OCaml interface, in
this context, via the definition of the fold function, while the latter is tied to
the implementation, specifically when fold is invoked.
    In the remaining of this section, we demonstrate how such constructs can be
formally specified using Gospel. We then present our extensions to the language,
together with their translation into WhyML via Cameleer. Our focus lies in
providing specification support for the most commonly used iteration patterns,
namely iter, fold, filter, and map. Furthermore, we argue that supporting
fold alone would be theoretically sufficient, as the remaining patterns can be
viewed as degenerate forms of the fold abstraction.

5.1    Interface overview
Considering the previous example, let us explain how we can define an iteration
over a sequence, using our extension to the Gospel language, and in terms of
permitted and complete. Gospel specifications of functions start by introducing
arbitrary, and user-selected, names of the function’s result, r and its arguments,
func, acc and col:
  val fold: (α Ñ β Ñ α) Ñ α Ñ β seq Ñ α                          Gospel + OCaml
    (*@ r = fold func acc col
Our extensions to the language begin by specifying which iteration pattern we
wish to define, and dealing with a fold, we indicate this using the keyword:
    folds                                                                Gospel
After that, we instantiate the predicates permitted and complete, both of which
take the sequence of visited elements as an argument. To refer to the collection
being iterated over within these predicates, one utilizes the keyword collection:
    ~permitted:(fun v Ñ ||v|| ď ||collection|| ^                            Gospel
                  @ i. 0 ď i ă ||v|| Ñ v[i] = (collection)[i])
      ~complete:(fun v Ñ ||v|| = ||collection||)
                                                         Unfolding Iterators        7

At this point, we have to be explicit about some typing information: the type
of the structure we are iterating over, structure, the type of elements that the
cursor produces, elt, and as auxiliary information, what is the name of the
accumulator in the header of the specification:
     with structure = (β seq), elt = β, accumulator = acc *)             Gospel
    The reader may have noticed that, although an argument of fold, we make no
mention of the consumer function, func. Part of turning a higher-order iterator
into a first-order cursor client is delaying acknowledging its existence until it
has been instantiated. In fact, our specification of fold abstracts away three
fundamental aspects of the consumer function: (1) the only side-effects performed
by the higher-order iteration are those of the consumer function. (2) the only
exceptions, potentially, raised by the higher-order iteration are those raised by
the consumer function. (3) we state the consumer function re-establishes the
user-supplied invariant, step-by-step, for each new enumerated element.


5.2   Implementation overview

Having covered how one might define a generic cursor in an interface, let us now
see how one might go onto specifying its behaviour. This is only possible to do
when one calls fold, during the implementation. Recalling the function sum:
  let sum (s: S.seq) = S.fold (fun a x Ñ a + x) 0 s                      OCaml
This function employs the higher-order iteration function fold. However, its
implementation is opaque to the user. They do not know how the iteration takes
place, but they expect the consumer function to be applied to every element
of s, with an initial accumulator 0. We argue that by hiding how the iteration
takes place in logic, we only ask the user to specify the essentials. Specifying its
semantics first starts by stating the kind of iteration pattern they expect, and
seeing as we are dealing with a fold, we start with the keyword:
  (*@ folds                                                                 Gospel
Next, and in no particular order, they indicate the collection being iterated over:
      ~collection:s                                                          Gospel
The termination measure, in the case of finite and deterministic enumerations,
follows a pattern: the number of to-be-visited elements converging to zero:
       ~convergence:(fun c v Ñ ||c|| - ||v||)                           Gospel
And lastly, the iteration invariant:
      ~inv:(fun a v Ñ a = sum (fun i Ñ v[i]) 0 ||v||) *)                       Gospel
This new syntax may have introduced a lot of new ideas at once. Let us make
them clear. As we have also seen in the interface, we have to identify what
iteration pattern we wish to express, through the keyword folds, which helps to
decide what first-order client schema to generate during translation. All the other
parametric fields are Gospel logical terms. Note how the parameter convergence
8        I. Chirica, M. Pereira

takes two arguments, the collection that is being iterated and the sequence of
visited elements. The inv, in the case of a fold, which introduced the notion of an
accumulator, is also parameterized with two arguments, the current value of the
accumulator and the sequence of visited elements. In both cases, the arguments
of convergence and inv, are automatically applied during translation.


6     Translation-based approach to iteration semantics

In this section we present our extensions to Cameleer through translation schemas.
Though we implemented four schemas, one for each iteration pattern, for presen-
tation purposes, we will only focus on the fold. Once again, we argue that the
other patterns (iter, filter, and map) are degenerate cases of fold. Specifically,
iter corresponds to a fold where the accumulator has type unit, and map can
be expressed as a fold that builds a new collection by applying a function to
each element and adding the result. Likewise, filter can be implemented as a
fold that adds elements to the new collection only if they satisfy a predicate.


6.1    Translating iteration declarations

The first translation schema is concerned with a higher-order function declaration.
These declarations can be found in OCaml interface files or as arguments of a
functor. The general specification form for a fold is the following:
  val fold: (α Ñ β Ñ α) Ñ α Ñ β t Ñ α                            Gospel + OCaml
    (*@ r = fold func acc col
        folds ~permitted:(fun v Ñ term p ) ~complete:(fun v Ñ term c )
        with structure = τs , elt = τe , accumulator = acc *)

As we have seen, permitted and complete are defined using Gospel logical
terms. The types structure and elt are also part of the specification, and the
accumulator is identified by its name in the header.
    With this context in place, we are now in a position to translate the spec-
ification into the creation of a cursor. In Cameleer, this translation replaces
the original function declaration with a scope, that is, a namespace [14]. The
translation schema follows the general shape:
   scope Fold                                                          WhyML
      use seq.Seq
      clone export cursor.CursorLib
      val create (collection: τs ) : cursor τe
        ensures { result.visited = empty }
        ensures { result.permitted = (fun v Ñ term p ) }
        ensures { result.complete = (fun v Ñ term c ) }
    end

Within the scope, we clone the CursorLib module, containing the developments
from Section 4, to expose the generics of a cursor, and define the create function
by extracting and translating the types, τs and τe , and terms, term p and term c .
                                                         Unfolding Iterators       9

6.2       Translating an iteration call

When it comes to iteration clients, we extend Cameleer to translate the specifica-
tion below into a first-order iteration using a cursor client:
   fold (fun a e Ñ ...) col x0                                 Gospel + OCaml
  (*@ folds ~inv: (fun a v Ñ term i ) ~collection: term c1
      ~convergence: (fun c v Ñ term v ) *)

Our translation schema starts by initializing the accumulator, acc. We are able
to get the value, x0 , as we have identified in the interface specification it in the
list of arguments. We then follow by creating a cursor over the collection term c1 :
   let acc = ref x0 in                                                      WhyML
  let cursor = Fold.create term c1 in

Here we find the while-loop, conditioned by the has_next function. Note that if
this loop ends, then when it does, the cursor predicate complete holds:
  while Fold.has_next cursor do                                       WhyML

The variant of the loop is term v , where we apply term c1 , the collection that is
being iterated, and the sequence of visited elements. On the other hand, the
invariant is term i , where we apply the accumulator and the visited sequence:
       variant { (fun c v Ñ term v ) term c1 cursor.visited }             WhyML
      invariant { (fun a v Ñ term i ) !acc cursor.visited }

We produce the next element in the iteration and store it in x. Followed by the
application of the consumer function to the accumulator and x:
    let x = Fold.next cursor in                                        WhyML
    acc := (fun a e Ñ ...) !acc x;
  done;

Finally, we return the contents of the accumulator:
  !acc                                                                      WhyML

This concludes our translation schema, which makes higher-order specifications
amenable to automated verification by translating them into a first-order form.


6.3       Capturing nested iterations

A natural question is: what about nested iteration, where the consumer function
itself uses a higher-order iterator? By analogy with classical reasoning, nested
loops require the inner one to preserve the invariant of the outer. Consider the
following example, adapted to our translation:
   while has_next cursor do                                             WhyML
      A invariant { I !a v } ...
      while has_next cursor’ do
       B invariant { I’ !a’ v’ } ...
10        I. Chirica, M. Pereira

We aim to preserve the invariant A , parameterized by the current accumulator !a
and visited elements v, inside the inner loop B . We track the history of these
arguments: for fold, map, and filter, both accumulator and visited elements; for
iter, only the visited elements. During translation, we propagate these arguments
to inner invariants, which must now account for:
  A invariant { I !a v }                                                  WhyML
    B   invariant { I’ !a’ v’ !a v }
More generally, we append (‘) the arguments from all levels above the current
one, l, while accounting for partial applications, represented by B as a sequence
of partially applied arguments:
                         l
    invariant { I B ( ‘ (!ai )? (vi )) }                                 WhyML
                          i“0




7       Coping with mutability
We have promised that our methodology is also capable of capturing iterations
where the consumer function performs side-effects, e.g., writes to a reference.
Let us present an example of a function that produces a stack from a sequence.
This function employs the iter higher-order iterator to traverse a sequence and
systematically push elements to the stack, modifying the stack in-place. Recalling
the iter function, previously presented in Section 5, we can decorate it with a
specification in the following way:
  val iter: (α Ñ unit) Ñ α seq Ñ unit                           Gospel + OCaml
     (*@ r = iter func col
       iters ~permitted:(fun v Ñ ||v|| ď ||collection|| ^
                         @ i. 0 ď i ă ||v|| Ñ v[i] = (collection)[i])
             ~complete:(fun v Ñ ||v|| = ||collection||)
       with structure = (α seq), elt = α *)
This specification is very similar to that of fold, with the primary differences
being the use of the iters keyword and the absence of an explicit accumulator.
This is expected, as both iterators operate over the same data structure and in
the same direction, resulting in identical definitions for permitted and complete.
   Consider the stack_of_seq function: it begins by creating an empty stack,
modeled logically as a list, and then uses iter to traverse the sequence s, pushing
each element onto the stack. Once iteration completes, the stack is returned.
  let stack_of_seq s =                                            Gospel + OCaml
       let stack = Stack.create () in
       S.iter (fun x Ñ Stack.push x stack) s
       (*@ iters ~inv:(fun v Ñ reverse stack = s[..||v||])
           ~collection:s ~convergence:(fun c v Ñ ||c|| - ||v||) *); stack
     (*@ r = stack_of_seq s
         ensures reverse r = s *)
The iteration invariant states that the reverse of the stack, reflecting insertion
order, equals the visited prefix, s[..i] is the prefix of s until i. The variant
                                                        Unfolding Iterators      11

is the decreasing number of elements left to visit. The postcondition follows
from termination: once has_next returns false, the loop exits, ensuring that
complete holds. By the invariant, the accumulator then contains the full reverse
of s. Despite the side effects, Alt-Ergo discharges the VCs, in under 3 seconds.


8     Case study: OCamlGraph

In this section, we present our main case study, proving the correctness of modules
taken from OCamlGraph, a generic library with a wide range of graph structures
and algorithms [8]. Widely used across OPAM packages, it relies on higher-order
iterators, making it a suitable candidate to validate our methodology.
    A particular module within OCamlGraph we aimed to prove correct is the
module Oper3 . This module provides common operations over graphs, such as, the
intersection and union of two graphs, and the complement and mirror of a graph.
In the subsequent sections, we present a logical model of a graph, the specification
of iterations over graphs, and illustrate a specification and application of our
methodology to the union of two graphs.


8.1    Logical model of a graph

The mathematical definition of a graph is through sets, and for our purposes
these will be finite. It is modeled using a domain, the set of vertices that make
up a graph, and a function that takes a vertex and returns a set vertices, these
will be our successors of a vertex. In other words, the set of edges in the graph.
    The module Oper takes as an argument another module, G, that represents
our graph. The module Oper starts by defining the type of a vertex and a graph:
  module Oper (G : sig                                                     OCaml
      type vt (* arbitrary vertex type *)
      type gt (* arbitrary graph type *)

The type graph is annotated with a logical model. It is made up of a domain dom
and the map suc. Additionally, we give this type an invariant stating that the
graph’s domain is closed under the map suc, and for every element that is not in
the domain, its set of successors is empty.
    (*@ model dom: vt fset                                              Gospel
         model suc: vt Ñ vt fset
         invariant (@ v1, v2. v1 P dom ^ v2 P (suc v1) Ñ v2 P dom) ^
                   (@ v1. ␣(v1 P dom) Ñ (suc v1) == H) *)

An empty graph is not very useful, so we define two functions to build its domain
and successors: add_vertex and add_edge. The first takes a graph and a vertex
and returns a new graph with the vertex added to the domain and the successor
map remains unchanged:
3
    https://github.com/backtracking/ocamlgraph/blob/master/src/oper.ml
12      I. Chirica, M. Pereira



      val add_vertex : gt Ñ vt Ñ gt                        Gospel + OCaml
      (*@ g’ = add_vertex g v
          ensures g’.dom = add v (g.dom) ^ @ v. g’.suc v = g.suc v *)
The second function adds an edge from v to v’, returning a graph where the
domain is unchanged, and the successor map updates v with the addition of v’:
   val add_edge : gt Ñ vt Ñ vt Ñ gt                         Gospel + OCaml
      (*@ g’ = add_edge g v v’
          ensures g’.dom = g.dom ^ g’.suc = g.suc[v Ð add v’ (g.suc v)] *)
Finally, let us also specify a function that yields a copy of a graph, copy:
    val copy: gt Ñ gt                                             Gospel + OCaml
      (*@ g’ = copy g
          ensures g.dom = g’.dom ^ @ v. g.suc v = g’.suc v *)
These functions cover the necessary ground to build graphs, expanding its domain
set or set of successor. We make use of these functions later on.

8.2    Higher-order iterators over graphs
We have covered how to build graphs, but we are yet to mention how to iterate
over one. The module Oper makes use of two functions, fold_vertex, fold_succ,
to iterate over graphs, more precisely, over finite sets. Let us see how we can
specify an iteration over vertices with the first function:
     val fold_vertex : (vt Ñ α Ñ α) Ñ gt Ñ α Ñ α                         OCaml
In order to produce elements, the visited set has to be a subset (Ď) of the graph’s
domain; and have to be all distinct as a sequence. The iteration is complete
when we have visited all the elements in the graph’s domain. From the function’s
arguments we conclude that we are iterating over a graph and producing vertices.
     (*@ r = fold_vertex func graph acc                                     Gospel
       folds ~complete:(fun v Ñ v = collection.dom)
             ~permitted:(fun v Ñ v Ď collection.dom ^ distinct v)
       with structure = gt, elt = vt, accumulator = acc *)
The second function that iterates a graph is fold_succ, taking as an argument a
graph and a vertex, while iterating over its successors. Its signature is as follows:
    val fold_succ : (gt Ñ α Ñ α) Ñ α Ñ gt Ñ vt Ñ α                            OCaml
This iteration is also over sets, with the structure of iteration being a pair pgt, vtq,
as it does not make much sense to iterate over a vertex without a graph nor over
successors of which we do not know their origin. Both permitted and complete
are in regard to the successors of s in g. This iteration produces vertices.
     (*@ r = fold_succ func acc pair                                            Gospel
       folds ~complete:(fun v Ñ let (g, s) = collection in ||v|| = ||g.suc s||)
             ~permitted:(fun v Ñ let (g, s) = collection in
                                  v Ď (g.suc s) ^ distinct v)
       with structure = (gt * vt), elt = vt, accumulator = acc *)
                                                         Unfolding Iterators     13

We are less precise in the complete predicate: we only say that they have to be
equal in their cardinality (|| ¨ ||) but not in the enumeration of their elements.
This is also correct, from classical set theory follows that if a set s1 is a subset
of s2 and their cardinality is the same, then they are the same set.


8.3   Union

The union of two graphs, g1 and g2, produces a new graph that combines their
vertex sets and successor functions. This is done by iterating over each vertex s in
g1 and adding s and its successors to a copy of g2, used as an accumulator. The
result satisfies the postcondition of representing the full union of both graphs.
  let union g1 g2 =                                               Gospel + OCaml
    fold_vertex
      (fun g v Ñ
        fold_succ (fun e g Ñ add_edge g v e) (add_vertex g v) g1 v
        (*@ folds ~inv:(union_inner g1 g2 v) ~collection:(g1,v)
           ~convergence:(fun (g, s) v Ñ ||g.suc s|| - ||v||) *)) g1 (copy g2)
    (*@ folds ~inv:(union_outer g1 g2) ~collection:g1
       ~convergence:(fun g v Ñ ||g.dom|| - ||v||) *)
  (*@ gr = union g1 g2
      ensures gr.dom = g1.dom   g2.dom
      ensures @ src. (gr.suc src) = (g1.suc src)     (g2.suc src) *)

Since we are dealing with two higher-order iterators, each requires an invariant.
The outer one, union_outer, applies to fold_vertex. It states that the accu-
mulator’s domain is the union of g2’s domain and the visited vertices of g1; for
visited vertices v, their successors in acc are the union from g1 and g2; and for
unvisited vertices, successors match those in g2. As the information automatically
applied during translation is insufficient, we manually partially apply the graphs
to both invariants, and additionally the vertex being iterated to the innermost.
  (*@ predicate union_outer (g1 g2: gt)                                    Gospel
    (* outer iteration *) (visited: vt seq) (acc: gt) =
    (acc.dom = visited   g2.dom)
  ^ (@ v. v P visited Ñ acc.suc v = (g1.suc v)   (g2.suc v))
  ^ (@ v. v P (acc.dom z visited) Ñ acc.suc v = g2.suc v) *)

The inner invariant, union_inner, is more subtle. We begin by stating that the
accumulator graph’s domain is the union of the visited vertices and that of g2:
  (*@ predicate union_inner (g1 g2: gt) (src: vt)                        Gospel
      (* inner iteration *) (visited’: vt seq) (acc’: gt)
      (* outer iteration *) (visited: vt seq) (acc: gt) =
      (acc’.dom = visited   g2.dom)

Successors of unvisited vertices are still those from g2:
   ^ (@ v. v P (acc’.dom z visited) Ñ acc’.suc v = g2.suc v)

For visited vertices other than the one currently being processed, its successors
in the accumulator are the union from both graphs:
14      I. Chirica, M. Pereira

     ^ (@ v. v P visited ^ v ‰ src Ñ acc’.suc v = (g1.suc v)          (g2.suc v))

Finally, the current vertex src accumulates successors incrementally:
     ^ (acc’.suc src = visited’        (g2.suc src)) *)

Note that we did not use the outer accumulator, since acc’ is already an updated
version of acc. Alt-Ergo dispatches all the generated VCs of union.


8.4    Summary of verified case studies

In this section we summarize a collection of case studies, and Table 1 summarizes
some statistics. The examples defined with an iter all have side-effects. We note
that the user never had to reason about the generated WhyML code, and all
the verification conditions were automatically dispatched. The case-studies and
extensions to the tools are available in an online artifact [7].


 Iteration client                # VCs LoC / LoS Time (s)   Iteration Effects
 Sequences                         18    10 / 12
    sum_seq                        6      1/2     10.45       fold       -
    stack_of_seq                   1      3/2      3.01       iter
    queue_of_seq                   1      3/2      1.13       iter
    gt_seq                         8      1/2     16.01      filter      -
    counter_filter_seq             1      1/2      0.32      filter
    counter_map_seq                1      1/2      0.29        map
 Graphs                           275  124 / 286
    intersect                      13    12 / 15   3.13   fold + fold    -
    union                          11    4 / 17    4.40   fold + fold    -
    complement                     12    8 / 23    5.80   fold + fold    -
    mirror                         6      5/8      2.51       fold       -
    copy_vertices                  1      1/2      1.64       fold       -
    check_path                     71   44 / 103  47.79       iter
    check_path:                   161   50 / 118  105.07        -
 Binary trees                      14     5/6
    sum_tree                       5      1/2     10.51       fold       -
    height_tree                    1      1/2      1.02       fold       -
    gt_tree                        8      3/2     37.05       iter

               Table 1: Summary of verified iteration case studies.


   Sequences. The sum_seq function generates more VCs than others in the
module, due to split_vc and in_line goals introduced by a Why3 strategy.
Yet, examples with a single VC suggest this splitting was unnecessary. Although
queue_of_seq and stack_of_seq are similar, the latter’s specification includes a
sequence reversal, adding a slight overhead to proof replay. The gt_seq function
counts elements above a threshold by filtering and then measuring the length of
the resulting sequence. Finally, counter_filter_seq and counter_map_seq are
                                                          Unfolding Iterators      15

simple iterators: one filters positives, the other increments elements. Both write
to a reference, but their effects are correctly identified by the consumer functions.
    Graphs. All graph operations are fully automatic. The slowest among these
is the complement of a graph, essentially due to its verbosity and need to keep
track of the universe of vertices that have not been explored. This verbosity
is observable when relating the number of lines of specification (LoS) of each
case study to their proof time, which tends to grow linearly. Within the Check4
module, we revisited a path-checking algorithm, check_path. A version of this
function, proved correctly in previous work [4], check_path: , relied on manually
deconstructing the iteration into a recursive function and then specifying the
iteration. In contrast, our approach allows for a direct specification of the higher-
order iterators, resulting in half as many VCs, thus, halving the proof time.
    Binary Trees. We specified iteration over binary trees using classical structures.
The permitted predicate flattens a tree into a sequence and reasoning about it
as such. The sum of integers values of a tree sum_tree has similar performance
as its counterpart sum_seq, though facing similar challenges. For computing tree
height, we used a different higher-order iterator, fold_level, which proceeds
level by level, akin to breadth-first search. Its permitted predicate ensures that
each position i of the visited sequence holds all elements at level i. The height
then follows directly from this specification. Alternatively, in gt_tree, we used
an iter to count elements exceeding a threshold. The impact in performance is
clearly noticeable, this can be partially due to either the fact that we are flatting
the tree into a sequence or using an iterator with effects.
    In any case, we observe that the number of lines of specification (LoS) tends
to exceed the number of lines of code (LoC). This is not surprising, as the
specification effort is generally greater than the implementation. The benchmarks
were conducted on a machine with a processor i5-2520M 2-cores @ 3.2GHz; 12Gb
RAM; 64-bit Linux Kernel 6.9.5. The proof replay times are results of 5 executions
of Why3’s replay command, using hyperfine with 3 warm-up executions.


9     Related work

Recently, several works have been published addressing the formal verification of
higher-order iterators. Like our approach, these works are based on a specifica-
tion methodology that exploit the pair of predicates permitted and complete.
However, the works described below differ from our presentation primarily in
their target language (none use OCaml) and the verification toolchain employed.
    Regarding the Rust programming language, we find the works of Denis and
Jourdan [9], as well as the work by Bílý et al. [3]. The former use the permitted
and complete predicates to formally verify higher-order iterators using the
Creusot tool [10]. The latter adopt the same underlying methodology but carry
out the verification process in Prusti [1], a tool that translates Rust programs
into the Viper verification language [19]. Unlike traditional functional languages,
4
    https://github.com/backtracking/ocamlgraph/blob/master/src/path.ml
16      I. Chirica, M. Pereira

Rust does not provide a type for anonymous functions. It is up to the user to
decide, in each case, the appropriate kind of closure to use: Fn, FnMut, or FnOnce,
that is, by ownership, mutable reference, or immutable reference. This decision
has a direct impact on the verbosity of the resulting specification. In OCaml, and
in our approach in particular, we support any consumer function, regardless of
its nature, without affecting the generated specification.
    Additionally, Pottier’s work [21] represents a significant application of the
permitted{complete methodology outside the scope of an automatic verification
platform. In this work, the author uses the CFML [5] tool to formally verify the
implementation of a hash table from the OCaml standard library, as well as the
iterators provided for this data structure. The proofs are carried out entirely in
Rocq, which demands a high level of proof effort and human interaction, especially
when compared to our approach using Cameleer.


10    Conclusions & future work

We developed an extension to Gospel focused on the specification of higher-order
iterators. We also developed an extension to Cameleer that could translate these
specifications into regular WhyML code that could, in turn, be deductively verified
using Why3. Additionally, we devised a collection of case studies that showcase how
one might use our work to verify higher-order iterators, through the permitted
and complete predicates. We tackled the verification of realistic OCaml code, as
taken from the OCamlGraph library, which shows that our methodology scales-
up well in practice. In summary, we presented a simple, generic and modular
specification to capture higher-order iteration. This specifications abstracts away
how the iteration is implemented, focusing only on the important logical elements
of an iteration: the permitted/complete relations and a user-supplied invariant.
    In the following, we highlight some lines of possible future work.
    Generic specification for patterns. Our generic iteration specification captures
patterns that any client or iterator must follow, regardless of their concrete imple-
mentation. This specification would introduce a concept similar to typeclasses or
traits in Gospel, as it would only be necessary to describe the general abstractions
and provide concrete instances for each specific use.
    Relational equivalence. The correctness of our translation schemas is based on
an informal argument that a higher-order iterator can be converted in a cursor
that plays the iteration part. One possible extension to our methodology could
be to generate a skeleton of a proof, for example, in Rocq that captures such
equivalence. It would be natural to resort to binary logic, e.g., Relational Hoare
Logic [2], allowing us to reason about the equivalence of two OCaml programs.
    Verification of Iteration Implementations. While we focused on specifying
higher-order iterators and translating them into cursor-based definitions and
clients, we have yet to verify existing implementations against these specifications.
In that regard, we propose verifying that higher-order function implementations
conform to their permitted/complete based specifications, likely requiring formal
proofs in frameworks like CFML or Iris [17].
                                                            Unfolding Iterators      17

References
 1. Astrauskas, V., Müller, P., Poli, F., Summers, A.J.: Leveraging Rust types for
    Modular Specification and Verification. Proc. ACM Program. Lang. 3(OOPSLA),
    147:1–147:30 (2019). https://doi.org/10.1145/3360573
 2. Benton, N.: Simple Relational correctness proofs for Static Analyses and Program
    Transformations. SIGPLAN Not. 39(1), 14–25 (Jan 2004). https://doi.org/10.
    1145/982962.964003
 3. Bílý, A., Hansen, J., Müller, P., Summers, A.J.: Compositional Reasoning for Side-
    effectful Iterators and Iterator Adapters (2022), https://arxiv.org/abs/2210.
    09857
 4. Castanho, D., Pereira, M.: Auto-active Verification of Graph Algorithms, Written
    in OCaml (2022), https://arxiv.org/abs/2207.09854
 5. Charguéraud, A.: Characteristic formulae for the verification of imperative programs.
    SIGPLAN Not. 46(9), 418–430 (sep 2011). https://doi.org/10.1145/2034574.
    2034828
 6. Charguéraud, A., Filliâtre, J., Lourenço, C., Pereira, M.: GOSPEL — Providing
    OCaml with a Formal Specification Language. In: Formal Methods - The Next 30
    Years - Third World Congress. Lecture Notes in Computer Science, vol. 11800, pp.
    484–501. Springer (2019), 10.1007/978-3-030-30942-8_29
 7. Chirica, I., Pereira, M.: Unfolding Iterators. https://ionchirica.github.io/
    ifm2025 (2025), Companion artifact
 8. Conchon, S., Filliâtre, J., Signoles, J.: Designing a Generic Graph Library Using
    ML Functors. In: Morazán, M.T. (ed.) Proceedings of the Eighth Symposium on
    Trends in Functional Programming, TFP 2007, New York City, New York, USA.
    Trends in Functional Programming, vol. 8, pp. 124–140. Intellect (2007)
 9. Denis, X., Jourdan, J.H.: Specifying and Verifying Higher-order Rust Iterators.
    In: Sankaranarayanan, S., Sharygina, N. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems (TACAS). Lecture Notes in Computer
    Science, vol. 13994, pp. 93–110. ETAPS, Springer, Paris, France (Apr 2023). https:
    //doi.org/10.1007/978-3-031-30820-8_9
10. Denis, X., Jourdan, J., Marché, C.: Creusot: A Foundry for the Deductive Ver-
    ification of Rust Programs. In: Riesco, A., Zhang, M. (eds.) Formal Methods
    and Software Engineering - 23rd International Conference on Formal Engineer-
    ing Methods, ICFEM 2022, Madrid, Spain, October 24-27, 2022, Proceedings.
    Lecture Notes in Computer Science, vol. 13478, pp. 90–105. Springer (2022).
    https://doi.org/10.1007/978-3-031-17244-1_6
11. Dijkstra, E.W.: A Discipline of Programming. Prentice Hall PTR, USA, 1st edn.
    (1997)
12. Filliâtre, J.C.: Deductive Software Verification. International Journal on Soft-
    ware Tools for Technology Transfer (STTT) 13(5), 397–403 (Aug 2011), 10.1007/
    s10009-011-0211-0
13. Filliâtre, J.C., Paskevich, A.: Why3: where programs meet provers. In: Proceedings
    of the 22nd European Conference on Programming Languages and Systems. p.
    125–128. ESOP’13, Springer-Verlag, Berlin, Heidelberg (2013). https://doi.org/
    10.1007/978-3-642-37036-6_8
14. Filliâtre, J.C., Paskevich, A.: Abstraction and Genericity in Why3. In: ISoLA 2021
    - 9th International Symposium On Leveraging Applications of Formal Methods,
    Verification and Validation. vol. 12476. Rhodes, Greece (Oct 2021). https://doi.
    org/10.1007/978-3-030-61362-4_7
18      I. Chirica, M. Pereira

15. Filliâtre, J.C., Pereira, M.: A Modular Way to Reason About Iteration. In:
    Rayadurgam, S., Tkachuk, O. (eds.) NASA Formal Methods. pp. 322–336. Springer
    International Publishing, Cham (2016)
16. Hoare, C.A.R.: An Axiomatic Basis for Computer Programming. Commun. ACM
    12(10), 576–580 (oct 1969). https://doi.org/10.1145/363235.363259
17. Jung, R., Krebbers, R., Jourdan, J.H., Bizjak, A., Birkedal, L., Dreyer, D.: Iris From
    the Ground Up: A Modular Foundation For Higher-order Concurrent Separation
    Logic. Journal of Functional Programming 28(e20) (2018). https://doi.org/10.
    1017/S0956796818000151
18. Monin, J.: Understanding Formal Methods. Springer (2003), http://www.springer.
    com/computer/swe/book/978-1-85233-247-1
19. Müller, P., Schwerhoff, M., Summers, A.: Viper: A verification infrastructure for
    permission-based reasoning, pp. 104–125 (01 2017). https://doi.org/10.3233/
    978-1-61499-810-5-104
20. Pereira, M., Ravara, A.: Cameleer: A Deductive Verification Tool for OCaml. In:
    Silva, A., Leino, K.R.M. (eds.) Computer Aided Verification - 33rd International
    Conference, CAV 2021, Virtual Event, July 20-23, 2021, Proceedings, Part II.
    Lecture Notes in Computer Science, vol. 12760, pp. 677–689. Springer (2021)
21. Pottier, F.: Verifying a hash table and its iterators in higher-order separation logic.
    In: Proceedings of the 6th ACM SIGPLAN Conference on Certified Programs and
    Proofs. p. 3–16. CPP 2017, Association for Computing Machinery, New York, NY,
    USA (2017). https://doi.org/10.1145/3018610.3018624
22. Reynolds, J.: Separation Logic: A Logic for Shared Mutable Data Structures. In:
    Proceedings 17th Annual IEEE Symposium on Logic in Computer Science. pp.
    55–74 (2002). https://doi.org/10.1109/LICS.2002.1029817
