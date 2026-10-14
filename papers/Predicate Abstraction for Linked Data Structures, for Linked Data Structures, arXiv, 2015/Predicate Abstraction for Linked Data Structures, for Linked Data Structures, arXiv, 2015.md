                                                              Predicate Abstraction
                                                           for Linked Data Structures

                                                                 Alexander Bakst and Ranjit Jhala

                                                                  University of California, San Diego
arXiv:1505.02298v2 [cs.PL] 31 Oct 2015




                                                                   {abakst,jhala}@cs.ucsd.edu



                                               Abstract. We present Alias Refinement Types (Art), a new approach
                                               that uses predicate-abstraction to automate the verification of correct-
                                               ness properties of linked data structures. While there are many tech-
                                               niques for checking that a heap-manipulating program adheres to its
                                               specification, they often require that the programmer annotate the be-
                                               havior of each procedure, for example, in the form of loop invariants and
                                               pre- and post-conditions. We introduce a technique that lifts predicate
                                               abstraction to the heap by factoring the analysis of data structures into
                                               two orthogonal components: (1) Alias Types, which reason about the
                                               physical shape of heap structures, and (2) Refinement Types, which use
                                               simple predicates from an SMT decidable theory to capture the logical
                                               or semantic properties of the structures. We evaluate Art by implement-
                                               ing a tool that performs type inference for an imperative language, and
                                               empirically show, using a suite of data-structure benchmarks, that Art
                                               requires only 21% of the annotations needed by other state-of-the-art
                                               verification techniques.


                                         1   Introduction
                                         Separation logic (SL) [30] has proven invaluable as a unifying framework for
                                         specifying and verifying correctness properties of linked data structures. Para-
                                         doxically, the richness of the logic has led to a problem – analyses built upon it
                                         are exclusively either expressive or automatic. To automate verification, we must
                                         restrict the logic to decidable fragments, e.g. list-segments [3,20], and design cus-
                                         tom decision procedures [13,15,5,26,27] or abstract interpretations [22,39,6]. Con-
                                         sequently, we lose expressiveness as the resulting analyses cannot be extended to
                                         user -defined structures. To express properties of user-defined structures, we must
                                         fall back upon arbitrary SL predicates. We sacrifice automation as we require
                                         programmer assistance to verify entailments over such predicates [23,9]. Even
                                         when entailment is automated by specializing proof search, the programmer has
                                         the onerous task of providing complex auxiliary inductive invariants [8,29].
                                             We observe that the primary obstacle towards obtaining expressiveness and
                                         automation is that in SL, machine state is represented by monolithic assertions
                                         that conflate reasoning about heap and data. While SL based tools commonly
                                         describe machine state as a conjunction of a pure, heap independent formula,
                                         and a * combination of heap predicates, the heap predicates themselves conflate
2

        abs :: pintq ñ nat1                absR :: px : xdata : intyq ñ pq{&x ÞÑ xdata : nat2 y
function abs(x){ x : int                                               .
                                                                    Γ “ x : x&xy
  if (0 <= x)        p0 ď xq; x : int      function absR(x){ 0 .
                                                                    Σ0 “ &x ÞÑ xdata : inty
    return x;                                                          .
                                             var d = x.data; Γ1 “ d : int; Γ0
                     r : tν “ 0 ´ xu;                                  .
                                             var t = abs(d); Γ2 “ t : nat1 ; Γ1
  var r = 0 - x;                                                        .
                        p0 ď xq; x : int     x.data = t;            Σ1 “ &x ÞÑ xdata : ν “ ty
  return r;                                  return;
}                                          }

        Fig. 1: Refinement types                Fig. 2: Strongly updating a location

reasoning about links (e.g. reachability) and correctness properties (e.g. sizes or
data invariants), which complicates automatic checking and inference.
    In this paper, we introduce Alias Refinement Types (Art), a subset of separa-
tion logic that reconciles expressiveness and automation by factoring the repre-
sentation of machine state along two independent axes: a “physical” component
describing the basic shape and linkages between heap cells and a “logical” com-
ponent describing semantic or relational properties of the data contained within
them. We connect the two components in order to describe global logical prop-
erties and relationships of heap structures, using heap binders that name pure
“snapshots” of the mutable data stored on the heap at any given point.
    The separation between assertions about the heap’s structure and heap-
oblivious assertions about pure values allow Art to automatically infer precise
data invariants. First, the program is type-checked with respect to the physical
type system. Next, we generate a system of subtyping constraints over the logical
component of the type system. Because the logical component of each type is
heap-oblivious, solving the system of constraints amounts to solving a system
of Horn clauses. We use predicate abstraction to solve these constraints, thus
yielding precise refinements that summarize unbounded collections of objects.
    In summary, this paper makes the following contributions:
    – a description of Art and formalization of a constraint generation algorithm
      for inferring precise invariants of linked data structures;
    – a novel soundness argument in which types are interpreted as assertions in
      separation logic, and thus typing derivations are interpreted as proofs;
    – an evaluation of a prototype implementation that demonstrates Art is ef-
      fective at verifying and, crucially, inferring data structure properties ranging
      from the sizes and sorted-ness of linked lists to the invariants defining binary
      search trees and red-black trees. Our experiments demonstrate that Art re-
      quires only 21% of the annotation required by other techniques to verify
      intermediate functions in these benchmarks.


2      Overview

Refinements Types and Templates. A basic refinement type is a basic type,
                                                                  .
e.g. int, refined with a formula from a decidable logic, e.g. nat “ tν : int | 0 ď νu
is a refinement type denoting the set of non-negative integers, where int is
                                                                                       3

the basic or physical part of the type and the refinement 0 ď ν is the log-
ical part. A template is a refinement type where, instead of concrete formu-
las we have variables κ that denote the unknown to-be-inferred refinements.
In the case that the refinement is simply true, we omit the refinement (e.g.
int =tν : int | trueu). We specify the behaviors of functions using refined func-
tion types: px1 : t1 , . . . , xn : tn q ñ t. The input refinement types ti specify the
function’s preconditions and t describes the postcondition.
Verification. Art splits verification into two phases: (1) constraint generation,
which traverses the program to create a set of Horn clause constraints over the
κ, and (2) constraint solving, which uses an off the shelf predicate abstraction
based Horn clause solver [31] that computes a least fixpoint solution that yields
refinement types that verify the program. Here, we focus on the novel step (1).
Path Sensitive Environments. To generate constraints Art traverses the
code, building up an environment of type bindings, mapping program variables
to their refinement types (or templates, when the types are unknown.) At each
call-site (resp. return), Art generates constraints that the arguments (resp. re-
turn value) are a subtype of the input (resp. output) type. Consider abs in Fig. 1
which computes the absolute value of the integer input x. Art creates a tem-
plate pintq ñ tν : int | κ1 u where κ1 denotes the unknown output refinement.
(We write nat1 in the figure to connect the inferred refinement with its κ.) In
Fig. 1, the environment after each statement is shown on the right side. The
initial environment contains a binder for x, which assumes that x may be any
int. In each branch of the if statement, the environment is extended with a
guard predicate reflecting the condition under which the branch is executed. As
the type tν : int | ν “ xu is problematic if x is mutable, we use SSA renaming to
ensure each variable is assigned (statically) at most once.
Subtyping. The returns in the then and else yield subtyping constraints:
                                 x : int, 0 ď x $ tν : int | ν “ xu ĺ tν : int | κ1 u
                                                                                      (1)
  x : int, p0 ď xq, r : tν : int | ν “ 0 ´ xu $ tν : int | ν “ ru ĺ tν : int | κ1 u
which respectively reduce to the Horn implications
                          ptrue ^ 0 ď xq ñ pν “ xq ñ κ1
         ptrue ^  p0 ď xq ^ r “ 0 ´ xq ñ pν “ rq ñ κ1
                                                      .
By predicate abstraction [31] we find the solution κ1 “ 0 ď ν and hence infer
that the returned value is a nat, i.e. non-negative.
References and Heaps. In Fig. 2, absR takes a reference to a structure con-
taining an int valued data field, and updates the data field to its absolute
value. We use κ2 for the output refinement; hence the type of absR desugars
to: px : &xq{&x ÞÑ xdata : inty ñ pq{&x ÞÑ xdata : κ2 y which states that absR
requires a parameter x that is a reference to a location named &x. in an input
heap where &x contains a structure with an int-valued data field. The function
returns pq (i.e. no value) in an output heap where the location &x is updated to
a structure with a κ2 -valued data-field.
4

                  absL :: px : listrintsq ñ pq{&x ÞÑ listrnat3 s
                        .                .
function absL(x){ Γ0 “  . x : x&xy, Σ0 “ &x ÞÑ x0 : listrints
                    Γ1 “ Γ0
  //: unfold(&x);        .
                    Σ1 “ &x ÞÑ x1 : xdata : int, next : ?x&tyy ˚ &t ÞÑ t0 : listrints
  var d = x.data;       .
                    Γ “ d : int, xn : tν : ?x&ty | ν “ x2 .nextu, Γ1
  x.data = abs(d); 2 .
                    Σ “ &x ÞÑ x2 : xdata : nat1 , next : ?x&tyy ˚ &t ÞÑ t0 : listrints
  var xn = x.next; 2
  if (xn == null){      .                       .
    //: fold(&x); Γ3 “     xn “ null, Γ2 , Σ3 “ &x ÞÑ listrnat3 s
    return;
  }                     .
                    Γ4 “ xn ‰ null; Γ2
  absL(xn);              .
                    Σ4 “ &x ÞÑ x2 : xdata : nat1 , next : ?x&tyy ˚ &t ÞÑ t1 : listrnat3 s
                        .          .
  //: fold(&x);     Γ5 “ Γ4 Σ5 “ &x ÞÑ x3 : listrnat3 s
  return;
}

Fig. 3: Strongly updating a collection. The fold and unfold annotations are automat-
ically inserted by a pre-analysis (§ E)

    We extend the constraint generation to precisely track updates to locations.
In Fig. 2, each statement of the code is followed by the environment Γ and heap
Σ that exists after the statement executes. Thus, at the start of the function,
x refers to a location, &x, whose data field is an arbitrary int. The call abs(d)
returns a κ1 that is bound to t, which is then used to strongly update the data
field of &x from int to κ1 . At the return we generate a constraint that the return
value and heap are sub-types of the function’s return type and heap. Here, we
get the heap subtyping constraint:
       x : x&xy, d : int, t : κ1 $ &x ÞÑ xdata: ν “ ty ĺ &x ÞÑ xdata: κ2 y
which reduces by field subtyping to the implication: κ1 rt{νs ñ pν “ tq ñ κ2
                                                                          .
which (together with the previous constraints) can be solved to κ2 “ 0 ď ν
letting us infer that absR updates the structure to make data non-negative. This
is possible because the κ variables denote pure formulas, as reasoning about
the heap shape is handled by the alias type system. Next we see how this idea
extends to infer strong updates to collections of linked data structures.
Linked Lists. Linked lists can be described as iso-recursive alias types [37]. The
definition
                            .
             type listrAs “ D!ℓ ÞÑ t : listrAs.h : xdata: A, next : ?xℓyy
says listrAs is a head structure with a data field of type A, and a next field
that is either null or a reference to the tail, denoted by the ?xℓy type. The heap
ℓ ÞÑ t : listrAs denotes that a singleton listrAs is stored at the location denoted
by ℓ if it is reachable at runtime. The D! quantification means that the tail is
distinct from every other location, ensuring that the list is inductively defined.
    Consider absL from Fig. 3, which updates each data field of a list with its
absolute value. As before, we start by creating a κ3 for the unknown output
refinement, so the function gets the template
              px : x&xyq{&x ÞÑ x0 : listrints ñ pq{&x ÞÑ xr : listrκ3 s
Fig. 3 shows the resulting environment and heap after each statement.
                                                                                  5

    The annotations unfold and fold allow Art to manage updates to collections
such as lists. In Art, the user does not write fold and unfold annotations; these
may be inferred by a straightforward analysis of the program(§ E) .
Unfold. The location &x that the variable x refers to initially contains a listrints
named with a heap binder x0 . The binder x0 may be used in refinements. Suppose
that x is a reference to a location containing a value of type listrAs. We require
that before the fields of x can be accessed, the list must be unfolded into a head
cell and a tail list. This is formalized with an unfold(&x) operation that unfolds
the list at &x from &x ÞÑ x0 : listrints to
             &x ÞÑ x1 : xdata : int, next : ?x&tyy ˚ &t ÞÑ t0 : listrints,
corresponding to materializing in shape analysis. The type system guarantees
that the head structure and (if next is not null) the newly unfolded tail structure
are unique and distinct. So, after unfolding, the structure at &x can be strongly
updated as in absR. Hence, the field assignment generates a fresh binder x2 for
the updated structure whose data field is a κ1 , the output of abs.
Fold. After updating the data field of the head, the function tests whether the
next field assigned to xn is null, and if so returns. Since the expected output is
a list, Art requires that we fold the structure back into a listrκ3 s – effectively
computing a summary of the structure rooted at &x. As xn is null and xn :
tν : ?x&ty | ν “ x2 .nextu, fold(&x) converts &x ÞÑ x2 : xdata: κ1 , next: ?x&tyy
to &x ÞÑ listrκ3 s after generating a heap subtyping constraint which forces the
“head” structure to be a subtype of the folded list’s “head” structure.
          Γ3 $ &x ÞÑ x2 : xdata: κ1 , . . .y ĺ &x ÞÑ x2 : xdata : κ3 , . . .y   (2)
If instead, xn is non-null, the function updates the tail by recursively invoking
absL(xn). In this case, we can inductively assume the specification for absL and
so in the heap after the recursive call, the tail location &t contains a listrκ3 s.
As xn and hence the next field of x2 is non-null, the fold(&x) transforms
              &x ÞÑ x2 : xdata : κ1 , next: ?x&tyy ˚ &t ÞÑ t1 : listrκ3 s
into &x ÞÑ listrκ3 s, as required at the return, by generating a heap subtyping
constraints for the head and tail:
          Γ5 $ &x ÞÑ x2 : xdata : κ1 , . . .y ĺ &x ÞÑ x2 : xdata: κ3 , . . .y   (3)
          Γ5 $ &t ÞÑ t1 : listrκ3 s ĺ &t ÞÑ t1 : listrκ3 s                      (4)
The constraints eq. (2), eq. (3) and eq. (4) are simplified field-wise into the
implications κ1 ñ κ3 , κ1 ñ κ3 and κ3 ñ κ3 which, together with the previous
                                   .
constraints (eq. (1)) solve to: κ3 “ 0 ď ν. Plugging this back into the template
for absL we see that we have automatically inferred that the function strongly
updates the contents of the input list to make all the data fields non-negative.
    Art infers the update the type of the value stored at &x at fold and unfold
locations because reasoning about the shape of the updated list is delegated to
the alias type system. Prior work in refinement type inference for imperative
programs [32] can not type check this simple example as the physical type sys-
tem is not expressive enough. Increasing the expressiveness of the physical type
system allows Art to “lift” invariant inference to collections of objects.
6

             insert :: pA, x : ?listrAsq ñ tν : listrAs | plenpνq “ 1 ` lenpxqq4 u
   function insert(k, x)          Γ0 “ k : A; x : ?x&xy Σ0 “ &x ÞÑ x0 : listrAs
     if (x == null) {                 .
       var y =                    Γ1 “ y : x&yy; x “ null; Γ0
A:
        {data:k,next:null}; Σ1 “       .
                                      . &x ÞÑ x0 : listrAs ˚ &y ÞÑ y0 : xdata : A, next : nully
                                  Γ2 “ lenpy1 q “ 1; Γ1
B:     //: fold(&y)                    .
                                  Σ2 “ &x ÞÑ x0 : listrAs ˚ &y ÞÑ y1 : listrAs
       return y;
C:
     }                                .
                                  Γ3 “ lenpx0 q “ 1 ` lenpt0 q; x ‰ null; Γ0
     //: unfold(&x)                    .
                                  Σ3 “ &x ÞÑ x1 : xdata : a, next : ?x&tyy ˚ &t ÞÑ t0 : listras
     if (k <= x.data) {               .
       var y =                    Γ4 “ y : x&yy; Γ3
        {data:k,next:x};               .
                                  Σ4 “. &y ÞÑ y2 : xdata : A, next : ?x&xyy ˚ Σ3
                                  Γ5 “ lenpx2 q “ 1 ` lenpt0 q; Γ4
       //: fold(&x)                    .
                                  Σ5 “. &x ÞÑ x2 : listrAs ˚ &y ÞÑ y2 : .xdata : A, next : ?x&xyy
       //: fold(&y)               Γ6 “ lenpy3 q “ 1 ` lenpx2 q; Γ5 Σ6 “ &x ÞÑ y3 : listrAs
       return y;
     }
     var z = x.next;                  .
                                  Γ7 “ u0 : κ4 rt0 {x0 s; u : x&uy; z : ?x&ty; Γ3
     var u = insert(k,z);              .
                                  Σ7 “ &x ÞÑ x1 : xdata : A, next : x&uyy ˚ &u ÞÑ u0 : listrAs
     x.next = u;                      .                                     .
     //: fold(&x)                 Γ8 “ lenpx2 q “ 1 ` lenpu0 q; Γ7 Σ8 “ &x ÞÑ x2 : listrAs
     return x;
   }

                             Fig. 4: Inserting into a collection
Snapshots. So far, our strategy is to factor reasoning about pointers and the
heap into a “physical” alias type system, and functional properties (e.g. values
of the data field) into quantifier- and heap-free “logical” refinements that may be
inferred by classical predicate abstraction. However, reasoning about recursively
defined properties, such as the length of a list, depends on the interaction between
the physical and logical systems.
    We solve this problem by associating recursively defined properties not di-
rectly with mutable collections on the heap, but with immutable snapshot values
that capture the contents of the collection at a particular point in time. These
snapshots are related to the sequences of pure values that appear in the definition
of predicates such as list in [30]. Consider the heap Σ defined as:
     &x0 ÞÑ h : xdata “ 0, next “ &x1 y ˚ &x1 ÞÑ t : xdata “ 1, next “ nully
We say that snapshot of &x0 in Σ is the value v0 defined as:
      .                                  .
  v0 “ p&x0 , xdata “ 0, next “ v1 yq v1 “ p&x1 , xdata “ 1, next “ nullyq
    Now, the logical system can avoid reasoning about the heap reachable from
x0 – which depends on the heap – and can instead reason about the length of
the snapshot v0 which is independent of the heap.
Heap Binders. We use heap binders to name snapshots in the refinement logic.
In the desugared signature for absR from Fig. 2,
               px : x&xyq{&x ÞÑ x0 : listrints ñ pq{&x ÞÑ xr : listrnats
the name x0 refers to the snapshot of input heap at &x. In Art, no reachable
cell of a folded recursive structure (e.g. the list rooted at &x) can be modified
                                                                                    7

without first unfolding the data structure starting at the root: references pointing
into the cells of a folded structure may not be dereferenced. Thus we can soundly
update heap binders locally without updating transitively reachable cells.
Measures. We formalize structural properties like the length of a list or the
height of a tree and so on, with a class of recursive functions called measures,
which are catamorphisms over (snapshot values of) the recursive type. For ex-
ample, we specify the length of a list with the measure:
       len :: listrAs ñ int      lenpnullq “ 0       lenpxq “ 1 ` lenpx.nextq
We must reason algorithmically about these recursively defined functions. The
direct approach of encoding measures as background axioms is problematic due
to the well known limitations and brittleness of quantifier instantiation heuris-
tics [12]. Instead, we encode measures as uninterpreted functions, obeying the
congruence axiom, @x, y.x “ y ñ f pxq “ f pyq. Second, we recover the seman-
tics of the function by adding instantiation constraints describing the measure’s
semantics. We add the instantiation constraints at fold and unfold operations,
automating the reasoning about measures while retaining completeness [35].
    Consider insert in Fig. 4, which adds a key k of type A into its position in an
(ordered) listrAs, by traversing the list, and mutating its links to accomodate
the new structure containing k. We generate a fresh κ4 for the output type to
obtain the function template:
           pA, x : ?x&xyq{&x ÞÑ x0 : listrAs ñ x&ly{&l ÞÑ tν : listrAs | κ4 u
Here, the snapshot of the input list x upon entry is named with the heap binder
x0 ; the output list must satisfy the (as yet unknown) refinement κ4 .
     Constraint generation proceeds by additionally instantiating measures at
each fold and unfold. When x is null, the fold(&y) transforms the binding
&y ÞÑ y0 : xdata: A, next : nully into a (singleton) list &y ÞÑ y1 : listrAs and
so we add the instantiation constraint lenpy1 q “ 1 to the environment. Hence,
the subsequent return yields a subtyping constraint over the output list that
simplifies to the implication:
                     lenpx0 q “ 0 ^ lenpy1 q “ 1 ñ ν “ y1 ñ κ4                (5)
When x is non-null, unfold(&x) transforms the binding &x ÞÑ x0 : listrAs to
                &x ÞÑ x1 : xdata : a, next: ?x&tyy ˚ &t ÞÑ t0 : listrAs
yielding the instantiation constraint lenpx0 q “ 1 ` lenpt0 q that relates the length
of the list’s snapshot with that of its tail’s. When k <= x.data the subsequent
folds create the binders x2 and y3 with instantiation constraints relating their
sizes. Thus, at the return we get the implication:
lenpx0 q “ 1`lenpt0 q^lenpx2 q “ 1`lenpt0 q^lenpy3 q “ 1`lenpx2 q ñ ν “ y3 ñ κ4
                                                                                  (6)
Finally, in the else branch, after the recursive call to insert, and subsequent
fold, we get the subtyping implication
  lenpx0 q “ 1`lenpt0 q^κ4 rν, x0 {u0 , t0 s^lenpx2 q “ 1`lenpu0 q ñ ν “ x2 ñ κ4 (7)
The recursive call that returns u0 constrains it to satisfy the unknown refinement
κ4 (after substituting t0 for the input binder x0 ). Since the heap is factored out by
8

                  px: ?listrAsq ñ tν : ?incListrAs | lenpνq “ lenpxqu
                  function insertSort(x){
                    if (x == null) return null;
                    //: unfold(&x);
                    var y = insertSort(x.next);
                    var t = insert(x.data, y);
                    //: fold(&t);
                    return t;
                  }

                                Fig. 5: Insertion Sort

the type system, the classical predicate abstraction fixpoint computation solves
                       .
eqs. (5) to (7) to κ4 “ lenpνq “ 1 ` lenpx0 q inferring a signature that states that
insert’s output has size one more than the input.
Abstract Refinements. Many important invariants of linked structures require
us to reason about relationships between elements of the structure. Next, we show
how our implementation of Art allows us to use abstract refinements, developed
in the purely functional setting [36], to verify relationships between elements of
linked data structures, allowing us to prove that insertSort in Fig. 5 returns an
ordered list. To this end, we parameterize types with abstract refinements that
describe relationships between elements of the structure. For example,
                    .
  type listrAsxpy “ D!l ÞÑ t : listrtν : A | ppdata, νqusxpy.h : xdata : A, next : ?xlyy
is the list type as before, but now parameterized by an abstract refinement p
which is effectively a relation between two A values. The type definition states
that, if the data fields have values x1 , . . . , xn where xi is the ith element of the
list, then for each i ă j we have ppxi , xj q.
Ordered Lists. We instantiate the refinement parameters with concrete refine-
ments to obtain invariants about linked data structures. For example, increasing
                                                  .
lists are described by the type incListrAs “ listrAsxpďqy.
Verification. Properties like sortedness may be automatically infered by using
liquid typing [31]. Art infers the types:
insertSort :: p?listrAsq ñ incListrAs insert :: pA, ?incListrAsq ñ incListrAs
i.e. that insert and insertSort return sorted lists. Thus, alias refinement types,
measures, and abstract refinements enable both the specification and automated
verification of functional correctness invariants of linked data structures.

3     Type Inference
To explain how Art infers refinement types as outlined in § 2, we first explain
the core features of Art’s refinement type system. We focus on the more novel
features of our type system; a full treatment may be found in Fig. 10 .

3.1   Type Rules
Type Environments. We describe Art in terms of an imperative language
Imp with record types and with the usual call by value semantics, whose syntax
                                                                                      9

Expressions e ::“ n | true | false | null | rℓ | x | e ‘ e
Statements s ::“ s; s | x “ e | y “ x.f | x.f “ e | if e then s else s
                     | return e | x “ alloc tf : eu | x “ f peq
                     | unfoldpℓq | foldpℓq | concrpxq | padpℓq
Programs       p ::“ function f pxq {s}
Primitive Types b ::“ int | bool | α | null | xℓy | ?xℓy
Types                τ ::“ b | CrT s | xf : T y
Refined Types        T ::“ tν : τ | pu
                                   .
Type Definition C ::“ Crαs “ D! Σ. x : xf : T y
Contexts             Γ ::“ H | x : T ; Γ | e; Γ
Heaps                Σ ::“ emp | Σ ˚ ℓ ÞÑ x : CrT s | Σ ˚ ℓ ÞÑ x : xf : T y
Function Types S ::“ @ℓ, α. px : T q{Σ ñ D!ℓ1 . x1 : T 1 {Σ 1
n P Integers, rℓ P Reference Constants, x, y, f P Identifiers, ‘ P t`, ´, . . .u

                       Fig. 6: Syntax of Imp programs and types
is given in Fig. 6. A function environment is defined as a mapping, Φ, from
functions f to function schemas S. A type environment (Γ ) is a sequence of type
bindings x : T and guard expressions e. A heap (Σ) is a finite, partial map from
locations (ℓ) to type bindings. We write Γ pxq to refer to T where x : T P Γ , and
Σpℓq to refer to x : T where the mapping ℓ ÞÑ x : T P Σ.
Type Judgements. The type system of Art defines a judgement Φ $ f :: S,
which says given the environment Φ, the function f behaves according to its
pre- and post-conditions as defined by S. An auxiliary judgement Φ, Γ, Σ $ s ::
Γ 1 {Σ 1 says that, given the input environments Γ and Σ, s produces the output
environments Γ 1 and Σ 1 . We say that a program p typechecks with respect to Φ
if, for every function f defined in p, Φ $ f :: Φpf q.
Well-Formedness. We require that types T be well formed in their local envi-
ronments Γ and heaps Σ, written Γ, Σ $ T . A heap Σ must heap be well formed
in its local environment Γ , written Γ $ Σ. The rules for the judgment (§ B)
capture the intuition that a type may only refer to binders in its environment.
Subtyping. We require a notion of subsumption, e.g. so that the integer 2
can be typed either as tν : int | ν “ 2u or simply int. The subtyping relation
depends on the environment. For example, tν : int | ν “ xu is a subtype of
tν : int | ν “ 2u if x : tν : int | ν “ 2u holds as well. Subtyping is formalized by the
judgment Γ $ T1 ĺ T2 , of which selected rules are shown in Fig. 11. Subtyping
in Imp reduces to the validity of logical implications between refinement predi-
cates. As the refinements are drawn from a decidable logic of Equality, Linear
Arithmetic, and Uninterpreted Functions, validity can be automatically checked
by SMT solvers [12]. The last two rules convert between non-null and possibly
null references (xℓy and ?xℓy).
Heap Subtyping. The heap subtyping judgment Γ $ Σ ĺ Σ 1 describes when
one heap is subsumed by another. Fig. 11 summarizes the rules for heap sub-
sumption. Heap subtyping is covariant, which is sound because our type system
is flow sensitive – types in the heap are updated after executing a statement.
Statements. When the condition x, y fresh appears in the antecedent of a rule,
it means that x and y are distinct names that do not appear in the input en-
10




Subtyping                                                             Γ $ T1 ĺ T2 , Γ $ Σ ĺ Σ 1

                                ValidpJ Γ K ñ J p K ñ J p1 Kq
                                                                      ĺ-b
                                Γ $ tν : b | pu ĺ tν : b | p1 u

                      ValidpJ Γ K ñ J p K ñ J p1 ^ ν ‰ null Kq
                                                                         ĺ-down
                           Γ $ tν : ?xℓy | pu ĺ tν : xℓy | p1 u

     Valid pJ Γ K ñ J p K ñ J p1 Kq                     Valid pJ Γ K ñ J p K ñ J p1 Kq
                                      1
                                          ĺ-up1                                               ĺ-up2
 Γ $ tν : xℓy | pu ĺ tν : ?xℓy | p u                 Γ $ tν : null | pu ĺ tν : ?xℓy | p1 u

                                             Γ $ Σ ĺ Σ1 Γ $ T ĺ T 1
                              ĺ-emp                                                    ĺ-heap
        Γ $ emp ĺ emp                     Γ $ Σ ˚ ℓ ÞÑ x : T ĺ Σ 1 ˚ ℓ ÞÑ x : T 1

Heap Folding                                                            Γ $ x : T1 {Σ1 ✄ x : T2 {Σ2

                     locspT1 q X DompΣ1 q “ H Γ $ T1 ĺ T2
                                                                            F-base
                              Γ $ x : T1 {Σ1 ✄ x : T2 {Σ2

                    Σ1 “ Σ11 ˚ ℓ ÞÑ x : T Σ2 “ Σ21 ˚ ℓ ÞÑ x : T 1
                  Γ $ tν : xℓy | pu ĺ T2 Γ $ x : T {Σ11 ✄ x : T 1 {Σ21
                                                                               F-ref
                         Γ $ y : tν : xℓy | pu{Σ1 ✄ y : T2 {Σ2
                                  Γ $ tν : ?xℓy | pu ĺ T2
                      Σ1 “ Σ11 ˚ ℓ ÞÑ y : T Σ2 “ Σ21 ˚ ℓ ÞÑ y : T 1
                x : tν : ?xℓy | p ^ ν ‰ nullu; Γ $ y : T {Σ11 ✄ y : T 1 {Σ21
                x : tν : ?xℓy | p ^ ν “ nullu; Γ $ y : T {Σ11 ✄ y : T 1 {Σ21
                                                                                F-?ref
                           Γ $ x : tν : ?xℓy | pu{Σ1 ✄ x : T2 {Σ2
                               Γ $ x : Ti {Σ1 ✄ x : Ti1{Σ2
                                                                       F-heap
                         Γ $ y : xfi : Ti y{Σ1 ✄ y : xfi : Ti1 y{Σ2

           Fig. 7: Selected subtyping, heap subtyping, and heap folding rules
                                                                                                          11

Statement Typing                                                                Φ, Γ, Σ $ s :: Γ 1 {Σ 1

                           Γ $ x : xℓy ℓ ÞÑ z : xfi : Ti y P Σ
                                                                      T-rd
                           Φ, Γ, Σ $ y “ x.fi :: y : Ti ; Γ {Σ

                      Γ $ x : xℓy Γ $ e : tν : τ | pu
        Tr “ NameFieldspz, xf0 : T0 , . . . , fi : tν : τ | ν “ eu, . . .yq     z fresh
                                                                                           T-wr
              Φ, Γ, ℓ ÞÑ y : xfj : Tj y ˚ Σ $ x.fi “ e :: Γ {ℓ ÞÑ z : Tr ˚ Σ

    for each ef , Γ, Σ $ ef : Tf       T “ NameFieldspz, xf : T yq            ℓ, z fresh
                                                                                            T-alloc
            Φ, Γ, Σ $ x “ alloc tf : ef u :: x : xℓy; Γ {ℓ ÞÑ z : T ˚ Σ

      Γ, Σ $ x : xℓy Ty “ tν : τ | pu Tz “ tν : τ | ν “ yu z fresh
                                                                         T-concr
         Φ, Γ, ℓ ÞÑ y : Ty ˚ Σ $ concrpxq :: y : Ty ; Γ {ℓ ÞÑ z : Tz ˚ Σ
                                                              .
            Γ $ Crαs “ D! Σc . xc : Tc Crαs $M mpxq “ em
                                     1
  Σ “ ℓ ÞÑ x : tν : CrT s | qu ˚ Σ0 Σ “ ℓ ÞÑ xc : rT {αsTc ˚ rT {αsΣc ˚ Σ0
       Γ, Σ $ T Γ, Σ 1 $ Σ 1 DompΣc q, BinderspΣc q, xc fresh
                                                                            T-unfold
                Φ, Γ, Σ $ unfoldpℓq :: p mpxq “ em q; Γ {Σ 1
                                        Ź
                                              m

                            Γ $ Crαs “ D! Σc . x : Tc
  Γ $ x : Tx {Σx ✄ x : rT {αsTc {rT {αsΣc Γ $ Źℓ ÞÑ y : Ty ˚ Σ 1 Γ $ Σ ĺ Σ 1
                         .
      Crαs $M mpxq “ em Ty “ tν : CrT s | m mpνq “ em u y fresh
                                                                                                T-fold
            Φ, Γ, ℓ ÞÑ x : Tx ˚ Σx ˚ Σ $ foldpℓq :: Γ {ℓ ÞÑ y : Ty ˚ Σ 1

Fig. 8: Selected Statement Typing Rules. We assume that type definitions (and, hence,
measures over these definitions) Γ $ Crαs “ D! Σ. x : T are α-convertible.
vironment Γ or heap Σ. We write ry{xs for the capture avoiding substitution
that maps x to y. The rules for sequencing, assignment, control-flow joins, and
function calls are relatively straightforward extensions from previous work (e.g.
[32]). The complete set of rules may be found in Fig. 10 .
Allocation. In T-alloc, a record is constructed from a sequence of field name
and expression bindings. The rule types each expression ef as Tf , generates a
record type T , and allocates a fresh location ℓ on the heap whose type is T . To
connect fields with their containing records, we create a new binder y denoting
the record, and use the helper NameFields(Fig. 10) to strengthen the type of
each field-binding for y from f : tνf : τ | pu, to f : tνf : τ | p ^ νf “ Fieldpν, f qu.
Here, Field is an uninterpreted function.
Access. T-rd and T-wr both require that non-null pointers are used to access
a field in a record stored on the heap. As T-alloc strengthens each type with
NameFields , the type for y in T-rd contains the predicate νfi “ Fieldpν, fi q.
Any facts established for y are linked, in the refinement logic, with the original
record’s field: when a record field is mutated, a new type binding is created in
the heap, and each unmutated field is linked to the old record using Field.
Concretization. As heaps also contain bindings of names to types, it would
be tempting to add these bindings to the local environment to strengthen the
12

subtyping context. However, due to the presence of possibly null references,
adding these bindings would be unsound. Consider the program fragment:
     function f (){ return null ; }
     function g (){ var p = f (); assert ( false ) }
One possible type for f is pq{emp ñ D!ℓ. r : ?xℓy{ℓ ÞÑ x : tν : int | f alseu because
the location ℓ is unreachable. If we added the binding x : tν : int | f alseu to Γ
after the call to f, then the assert(false) in g would unsoundly typecheck!
    We thus require that in order to include a heap binder in a local context,
Γ , the location must first be made concrete, by checking that a reference to it
is definitely not null. Concretization of a location ℓ is achieved with the heap
annotation concrpxq. Given a non-null reference, T-concr transforms the local
context Γ and the heap Σ by (1) adding the binding y : Ty at the location ℓ to
Γ ; (2) adding a fresh binding z : Tz at ℓ that expresses the equality y “ z.
Unfold. T-unfold describes how a type constructor application Crαs may be
unfolded according to its definition. The context is modified to contain the new
heap locations corresponding to those mentioned in the type’s definition. The
rule assumes an α-renaming such that the locations and binders appearing in
the definition of C are fresh, and then instantiates the formal type variables α
with the actual T . The environment is strengthened using the thus-instantiated
measure bodies.
Fold. Folding a set of heap bindings into a data structure is performed by T-
fold. Intuitively, to fold a heap into a type application of C, we ensure that it
is consistent with the definition of C. Note that the rules assume an appropriate
α-renaming of the definition of C. Simply requiring that the heap-to-be-folded
be a subtype of the definition’s heap is too restrictive. Consider the first fold in
absL in Fig. 3. As we have reached the end of the list xn “ null we need to fold
              &x ÞÑ x1 : xdata : nat, next: ?x&tyy ˚ &t ÞÑ t0 : listrints
into &x ÞÑ x2 : listrnats. An application of heap subtyping, i.e. requiring that the
heap-to-be-folded is a subtype of the body of the type definition, would require
that &t ÞÑ listrints ĺ &t ÞÑ listrnats, which does not hold! However, the fold is
safe, as the next field is null, rendering &t unreachable. We observe that it is
safe to fold a heap into another heap, so long as the sub-heap of the former that
is reachable from a given type is subsumed by the latter heap.
    Our intuition is formalized by the relation Γ, Σ $ x : T1 {Σ1 ✄ x : T2 {Σ2 , which
is read: “given a local context Γ, Σ, the type T1 and the heap Σ1 may be folded
into the type T2 and heap Σ2 .” F-base defines the ordinary case: from the point
of view of a type T , any heap Σ1 may be folded into another heap Σ2 . On the
other hand, if T1 is a reference to a location ℓ, then F-ref additionally requires
the folding relation to hold at the type bound at ℓ in Σ1 .
    F-?ref splits into two cases, depending on whether the reference is null
or not. The relation is checked in two strengthened environments, respectively
assuming the reference is in fact null and non-null. This strengthening allows
the subtyping judgement to make use reachability. Recall the first fold in absL
that happens when xn “ null. To check the fold(&x), the rule requires that the
                                                                                 13


CGen : FunEnv ˆ TypeEnv ˆ HeapEnv ˆ Stmt Ñ {Constr} ˆ TypeEnv ˆ HeapEnv
CGen(Φ,Γ ,Σ,s) = match s with
...
 | y = x.f Ñ let ℓ = loc(Γ (x)) in ({Γ $ Γ pxq ĺ xℓy}, y:TypeAt(Σ,ℓ);Γ ,Σ)
 | x. f = e Ñ let (cs, t)     = CGEx(Γ ,Σ,e)
                   ℓ          = Loc(t)
                   (y:Ty , z) = (Σ(ℓ), FreshId())
                   ht         = NameFields(z, Ty [f : Shape(t) [ (v = e)])
              in (cs Y {Γ $ t ĺ xℓy}, Γ , Σ[ℓ ÞÑz:ht])

                      Fig. 9: Statement constraint generation
problematic heap subtyping Γ $ &t ÞÑ listrints ĺ &t ÞÑ listrnats only holds
when x.next is non-null, i.e. when Γ is
           xn : tν : ?x&ty | ν “ x2 .nextu, xn “ null, x2 .next ‰ null
This heap subtyping reduces to checking the validity of the following, which
holds as the antecedent is inconsistent:
             xn “ x2 .next ^ xn “ null ^ x2 .next ‰ null ñ 0 ď ν.

3.2   Refinement Inference
In the definition of the type system we assumed that type refinements were given.
In order to infer the refinements, we replace each refinement in a program with
a unique variable, κi , that denotes the unknown refinement. More formally, let
Φ̂ denote a function environment as before except each type appearing in Φ̂
is optionally of the form tν : τ | κi u, i.e. its refinement has been omitted and
replaced with a unique κ variable. Given a set of function definitions p and
a corresponding environment of unrefined function signatures Φ̂, to infer the
refinements denoted by each κ we extract a system of Horn clause constraints C.
The constraints, C, are satisfiable if there exists a mapping of K of κ-variables to
refinement formulas such each implication in KC, i.e. substituting each κi with
its image in K, is valid. We solve the constraints by abstract interpretation in the
predicate abstraction domain generated from user-supplied predicate templates.
For more details, we refer the reader to [31]. We thus infer the refinements missing
from Φ̂ by finding such a solution, if it exists.
Constraint Generation. Constraint generation is carried out by the proce-
dure CGen which takes a function environment (Φ), type environment (Γ ), heap
environment (Σ), and statement (s) as input, and ouputs (1) a set of Horn con-
straints over refinement variables κ that appear in Φ, Γ , and Σ; (2) a new type-
and heap-environment which correspond to the effect (or post-condition) after
running s from the input type and heap environment (pre-condition).
     The constraints output by CGen correspond to the well-formedness con-
straints, Γ, Σ $ T , and subtyping constraints, Γ $ T ĺ T 1 , defined by the
type system. Base subtyping constraints Γ $ tν : b | pu ĺ tν : b | qu correspond
to the (Horn) Constraint J Γ K ñ p ñ q, where J Γ K is the conjunction of all of
the refinements appearing in Γ [31]. Heap Subtyping constraints Γ $ Σ ĺ Σ 1 are
14

decomposed via classical subtyping rules into base subtyping constraints between
the types stored at the corresponding locations in Σ and Σ 1 . This step crucially
allows the predicate abstraction to sidestep reasoning about reachability and the
heap, enabling inference.
    CGen proceeds by pattern matching on the statement to be typed. Each
FreshType() or Fresh() call generates a new κ variable which may then appear
in subtyping constraints as described previously. Thus, in a nutshell, CGen cre-
ates Fresh templates for unknown refinements, and then performs a type-based
symbolic execution to generate constraints over the templates, which are solved
to infer precise refinements summarizing functions and linked structures. As an
example, the cases of CGen corresponding to T-rd and T-wr are show in Fig. 9.


3.3   Soundness

The constraints output by CGen enjoy the following property. Let (C,Γ 1 ,Σ 1 ) be
the output of CGen(Φ̂,Γ ,Σ,s). If C is satisfiable, then there exists some solution
K such that K Φ̂, KΓ, KΣ $ s :: KΓ 1 {KΣ 1 [31], that is, there is a type derivation
                                                                                   .
using the refinements from K. Thus K yields the inferred program typing Φ “
K Φ̂, where each unknown refinement has been replaced with its solution, such
that Φ $ f :: Φpf q for each f defined in the program p.
    To prove the soundness of the type system, we translate types, environments
and heaps into separation logic assertions and hence, typing derivations into
proofs by using the interpretation function J ¨ K. We prove (§ § C) the following:


Theorem 1. [Typing Translation]
‚ If Φ, Γ, Σ $ s :: Γ 1 {Σ 1 then J Φ K $ tJ Γ, Σ Ku s tJ Γ 1 , Σ 1 Ku
‚ If Φ $ f :: S then J Φ K $ tPrepSqu Body pf q tPost pSqu
PrepSq, Post pSq and Bodypf q are the translations of the input and output types
of the function, the function (body) statement. As a corollary of this theorem,
our main soundness result follows:
Corollary 1. [Soundness] If Φ, ∅, emp $ s :: Γ {Σ, then J Φ K $ ttrueu s ttrueu
If we typecheck a program in the empty environment, we get a valid separation
logic proof of the program starting with the pre-condition true. We can encode
programmer-specified asserts as calls to a special function whose type encodes
the assertion. Thus, the soundness result says that if a program typechecks then
on all executions of the program, starting from any input state: (1) all memory
accesses occur on non-null pointers, and (2) all assertions succeed.


4     Experiments

We have implemented alias refinement types in a tool called Art. The user pro-
vides (unrefined) function signatures, and Art infers (1) annotations required
                                                                                      15

Data Structure Properties                 Procedures                          LOC      T
Singly linked list   Len, Keys          append, copy, del, find, insBack,        73    2
                                        insFront, rev
Doubly linked list Len, Keys            append, del, delMid, insBack,            90 16
                                        insMid, insFront
Cyclic linked list Len, Keys            delBack, delFront, insBack,              49    2
                                        insFront
Sorted linked list Len, Keys, Sort      rev, double, pairwiseSum,               135 10
                                        insSort, mergeSort, quickSort
Binary Tree        Order, Keys          preOrder, postOrder, inOrder             31 2
Max heap           Heap, Keys           heapify                                  48 27
Binary search tree BST, Keys            ins, find, del                          105 11
Red-black tree     Red-black, BST, Keys ins, del                                322 213
                     Table 1: Experimental Results (Expressiveness)


for alias typing, and (2) refinements that capture correctness invariants. We eval-
uate Art on two dimensions: the first demonstrates that it is expressive enough
to verify a variety of sophisticated properties for linked structures; the second
that it provides a significant automation over the state-of-the-art, represented
by the SMT-based VCDryad system. VCDryad has annotations comparable
to other recent tools that use specialized decision procedures to discharge Sepa-
ration Logic VCs [10]. Our benchmarks are available at [1].
Expressiveness. Table 1 summarizes the set of data structures, procedures,
and properties we used to evaluate the expressiveness of Art. The user provides
the type definitions, functions (with unrefined type signatures), and refined type
specifications to be verified for top-level functions, e.g. the top-level specification
for insertSort. LOC is lines of code and T, the verification time in seconds.
    We verified the following properties, where applicable: [Len] the output data
structures have the expected length; [Keys] the elements, or “keys” stored in each
data structure [Sort] the elements are in sorted order [Order] the ouput elements
have been labeled in the correct order (e.g. preorder) [Heap] the elements sat-
isfy the max heap property [BST] the structure satisfies the binary search tree
property [Red-black] the structure satisfies the red-black tree property.
Automation. To demonstrate the effectiveness of inference, we selected bench-
marks from Table 1 that made use of loops and intermediate functions requiring
extra proof annotations in the form of pre- and post-conditions in VCDryad,
and then used type inference to infer the intermediate pre- and post-conditions.
The results of these experiments is shown in Table 2. We omit incomparable
benchmarks, and those where the implementations consist of a single top-level
function. We compare the number of tokens required to specify type refinements
(in the case of Art) and pre- and post-conditions (for VCDryad). The table
distinguishes between two types of annotations: (1) those required to specify
the desired behavior of the top-level procedure, and (2) additional annotations
required (such as intermediate function specifications). Our results suggest that
it is possible to verify the correctness of a variety of data-structure manipulating
algorithms without requiring many annotations beyond the top-level specifica-
16

                                             ART                   VCDryad
 Data Structure     Procedure
                                   Specification Annotation Specification Annotation
 Singly Linked List (definition)        34           -          31           -
                    rev                  5          0           11          15
 Sorted Linked List (definition)        38           -          50           -
                    rev                 11           9          17          15
                    double               0           4           7          54
                    pairwiseSum          0           4          13          75
                    insSort              5           0          20          17
                    mergeSort            5          18          18          79
                    quickSort            5          18          11          140
 Binary Search Tree (definition)        58           -          55           -
                    del                  7          32          20          33
                           Total       168          63          253         428
Table 2: Experimental results (Inference). For each procedure listed we compare the
number of tokens used to specify: ART Type refinements for the top-level procedure in
Art; ART Annot manually-provided predicate templates required to infer the neces-
sary types [31]; VCDryad Spec pre- and post-conditions of the corresponding top-level
VCDryad procedure; and VCDryad Annot loop invariants as well as the specifications
required for intermediate functions in VCDryad. Art Annot totals include only unique
predicate templates across benchmarks.


tion. On the benchmarks we examined, overall annotations required by Art were
about 34% of those required by VCDryad. Focusing on intermediate function
specification, Art required about 21% of the annotation required by VCDryad.
Limitations. Intuitively, Art is limited to “tree-like” ownership structures:
while sharing and cycles are allowed (as in double- or cyclic-lists), there is a
tree-like backbone used for traversal. For example, even with a singly linked list,
our system will reject programs that traverse deep into the list, and return a
pointer to a cell unboundedly deep inside the list. We believe it is possible to
exploit the connection made between the SL notion of “magic wands” and the
type-theoretic notion of “zippers” [17] identified in [33] to enrich the alias typing
discipline to accommodate such access patterns.


5    Related Work

Physical Type Systems. Art infers logical invariants in part by leveraging
the technique of alias typing [37,2], in which access to dynamically-allocated
memory is factored into references and capabilities. In [7,28], capabilities are
used to decouple references from regions, which are collections of values. In
these systems, algebraic data types with an ML-like “match” are used to discover
spatial properties, rather than null pointer tests. fold & unfold are directly
related to roll & unroll in [37]. These operations, which give the program access
to quantified heap locations, resemble reasoning about capabilities [34,28]. These
systems are primarily restricted to verifying (non-)aliasing properties and finite,
non-relational facts about heap cells (i.e. “typestates”), instead of functional
                                                                                   17

correctness invariants. A possible avenue of future work would be to use a more
sophisticated physical type system to express more data structures with sharing.

Logical Type Systems. Refinement types [38,24,19], encode invariants about
recursive algebraic data types using indices or refinements. These approaches
are limited to purely functional languages, and hence cannot verify properties
of linked, mutable structures. Art brings logical types to the imperative setting
by using [37] to structure and reason about the interaction with the heap.

Interactive Program Logics. Several groups have built interactive verifiers
and used them to verify data structure correctness [40,11]. These verifiers require
the programmer write pre- and postconditions and loop invariants in addition
to top-level correctness specifications. The system generates verification condi-
tions (VCs) which are proved with user interaction. [18] uses symbolic execution
and SMT solvers together with user-supplied tactics and annotations to prove
programs. [23,9] describe separation logic frameworks for Coq and tactics that
provide some automation. These are more expressive than Art but require non-
trivial user assistance to prove VCs.

Automatic Separation Logics. To automate the proofs of VCs (i.e. entail-
ment), one can design decision procedures for various fragments of SL, typically
restricted to common structures like linked lists. [3] describes an entailment pro-
cedure for linked lists, and [13,15,5] extend the logic to include constraints on list
data. [20,4,26,27] describe SMT-based entailment by reducing formulas (from a
list-based fragment) to first-order logic, combining reasoning about shape with
other SMT theories. The above approaches are not extensible (i.e. limited to list-
segments); other verifiers support user defined, separation-logic predicates, with
various heuristics for entailment [8,10]. Art is related to natural proofs [29,25]
and the work of Heule et al. [16], which instantiate recursive predicates using
the local footprint of the heap accessed by a procedure, similar to how we insert
fold and unfold heap annotations, enabling generalization and instantiation of
structure properties. Finally, heap binders make it possible to use recursive func-
tions (e.g. measures) over ADTs in the imperative setting. While our measure
instantiation [19] requires the programmer adhere to a typing discipline, it does
not require us to separately prove that the function enjoys special properties [35].

Inference. The above do not deal with the problem of inferring annotations
like the inductive invariants (or pre- and post- conditions) needed to generate
appropriately strong VCs. To address this problem, there are several abstract
interpreters [21] tailored to particular data structures like list-segments [39],
lists-with-lengths [22]. Another approach is to combine separate domains for
heap and data with widening strategies tailored to particular structures [14,6].
These approaches conflate reasoning about the heap and data using monolithic
assertions or abstract domains, sacrificing either automation or expressiveness.

Acknowledgement. This work was supported by NSF grants CCF-1422471,
C1223850, CCF-1218344, and a generous gift from Microsoft Research.
18

References

 1. https://github.com/UCSD-PL/nano-js/tree/vmcai_2016/tests/eval.
 2. Amal Ahmed, Matthew Fluet, and Greg Morrisett. L3 : a linear language with
    locations. Fundamenta Informaticae, 77(4):397–449, June 2007.
 3. J. Berdine, C. Calcagno, and P.W. Ohearn. Smallfoot: Modular automatic assertion
    checking with separation logic. In FMCO, pages 115–137. Springer, 2006.
 4. M. Botinčan, M. Parkinson, and W. Schulte. Separation logic verification of c
    programs with an smt solver. ENTCS, 254:5–23, 2009.
 5. A. Bouajjani, C. Drăgoi, C. Enea, and M. Sighireanu. Accurate invariant checking
    for programs manipulating lists and arrays with infinite data. In ATVA, 2012.
 6. B. E. Chang and X. Rival. Relational inductive shape analysis. In POPL, 2008.
 7. Arthur Charguéraud and François Pottier. Functional translation of a calculus of
    capabilities. In James Hook and Peter Thiemann, editors, Proceeding of the 13th
    ACM SIGPLAN international conference on Functional programming (ICFP’08),
    pages 213–224. ACM, 2008.
 8. W-N. Chin, C. David, H. Nguyen, and S. Qin. Automated verification of shape, size
    and bag properties via user-defined predicates in separation logic. Sci. Comput.
    Program., 77(9), 2012.
 9. A. Chlipala. Mostly-automated verification of low-level programs in computational
    separation logic. In PLDI. ACM, 2011.
10. Duc-Hiep Chu, Joxan Jaffar, and Minh-Thai Trinh. Automatic induction proofs of
    data-structures in imperative programs. In Proceedings of the 36th ACM SIGPLAN
    Conference on Programming Language Design and Implementation, Portland, OR,
    USA, June 15-17, 2015, pages 457–466, 2015.
11. E. Cohen, M. Dahlweid, M. A. Hillebrand, D. Leinenbach, M. Moskal, T. Santen,
    W. Schulte, and S. Tobies. VCC: A practical system for verifying concurrent C.
    In TPHOLs, 2009.
12. D. Detlefs, G. Nelson, and J. B. Saxe. Simplify: a theorem prover for program
    checking. J. ACM, 52(3), 2005.
13. K. Dudka, P. Peringer, and T. Vojnar. Predator: A practical tool for checking
    manipulation of dynamic data structures using separation logic. In CAV, 2011.
14. S. Gulwani, B. McCloskey, and A. Tiwari. Lifting abstract interpreters to quantified
    logical domains. In POPL, pages 235–246, 2008.
15. C. Haase, S. Ishtiaq, J. Ouaknine, and M. J. Parkinson. Seloger: A tool for graph-
    based reasoning in separation logic. In CAV, 2013.
16. Stefan Heule, Ioannis T Kassios, Peter Müller, and Alexander J Summers. Ver-
    ification condition generation for permission logics with abstract predicates and
    abstraction functions.
17. Gérard P. Huet. The zipper. J. Funct. Program., 7(5):549–554, 1997.
18. B. Jacobs, J. Smans, P. Philippaerts, F. Vogels, W. Penninckx, and F. Piessens.
    Verifast: A powerful, sound, predictable, fast verifier for c and java. In NASA
    Formal Methods, pages 41–55. 2011.
19. M. Kawaguchi, P. Rondon, and R. Jhala. Type-based data structure verification.
    In PLDI, 2009.
20. S. K. Lahiri and S. Qadeer. Back to the future: revisiting precise program verifi-
    cation using smt solvers. In POPL, 2008.
21. T. Lev-Ami and S. Sagiv. TVLA: A system for implementing static analyses. In
    SAS. 2000.
                                                                                     19

22. S. Magill, M-H. Tsai, P. Lee, and Y-K. Tsay. Thor: A tool for reasoning about
    shape and arithmetic. In CAV, 2008.
23. A. Nanevski, G. Morrisett, A. Shinnar, P. Govereau, and L. Birkedal. Ynot: Rea-
    soning with the awkward squad. In ICFP, 2008.
24. N. Nystrom, V. Saraswat, J. Palsberg, and C. Grothoff. Constrained types for
    object-oriented languages. In OOPSLA. ACM, 2008.
25. Edgar Pek, Xiaokang Qiu, and P Madhusudan. Natural proofs for data structure
    manipulation in c using separation logic. In Proceedings of the 35th ACM SIGPLAN
    Conference on Programming Language Design and Implementation, page 46. ACM,
    2014.
26. J.A. Navarro Pérez and A. Rybalchenko. Separation logic+ superposition calcu-
    lus= heap theorem prover. In PLDI, 2011.
27. R. Piskac, T. Wies, and D. Zufferey. Automating separation logic using SMT. In
    CAV, 2013.
28. F. Pottier and J. Protzenko. Programming with permissions in mezzo. In ICFP,
    2013.
29. X. Qiu, P. Garg, A. Stefanescu, and P. Madhusudan. Natural proofs for structure,
    data, and separation. In PLDI, 2013.
30. J. C. Reynolds. Separation logic: A logic for shared mutable data structures. In
    LICS, 2002.
31. P. Rondon, M. Kawaguchi, and R. Jhala. Liquid types. In PLDI, 2008.
32. P. Rondon, M. Kawaguchi, and R. Jhala. Low-level liquid types. In POPL, 2010.
33. Malte Schwerhoff and Alexander J. Summers. Lightweight support for magic wands
    in an automatic verifier. In 29th European Conference on Object-Oriented Program-
    ming, ECOOP 2015, July 5-10, 2015, Prague, Czech Republic, pages 614–638, 2015.
34. J. Sunshine, K. Naden, S. Stork, J. Aldrich, and E. Tanter. First-class state change
    in plaid. In OOPSLA, 2011.
35. Philippe Suter, Mirco Dotta, and Viktor Kuncak. Decision procedures for algebraic
    data types with abstractions. In POPL, 2010.
36. N. Vazou, P. Rondon, and R. Jhala. Abstract refinement types. In ESOP, 2013.
37. D. Walker and J.G. Morrisett. Alias types for recursive data structures. In Types
    in Compilation. 2000.
38. H. Xi and F. Pfenning. Dependent types in practical programming. In POPL,
    1999.
39. H. Yang, O. Lee, J. Berdine, C. Calcagno, B. Cook, D. Distefano, and P. W.
    O’Hearn. Scalable shape analysis for systems code. In CAV, pages 385–398, 2008.
40. K. Zee, V. Kuncak, and M. C. Rinard. Full functional verification of linked data
    structures. In PLDI, pages 349–361, 2008.
20

A     Imp with Annotations

A.1   Annotation Elaboration
In § D we state that our soundness proof relies on a semantics-preserving elab-
oration step that inserts assignments to ghost variables. More formally, we can
take a typing derivation for a program in Imp as presented in § 3 and produce
an elaborated source with an almost identical derivation. These elaborations
amount to making assignments to ghost variables to correspond to locations and
heap binders, and are thus semantics preserving because the ghost variables do
not appear in the original program. The type judgements for the elaborated
code are used in the soundness proof. The syntax of Imp with ghost variable an-
notations is given in Fig. 10. Statement typing judgements with ghost variable
annotations are given in Fig. 12.


Expressions e ::“ n | true | false | null | rℓ | x | e ‘ e
Statements s ::“ s; s | x “ e | y “ x.f | x.f “z e | if e then s else s
                  | return e | x “z allocℓ tf : eu | x “ f peq
                  | unfoldpℓ, yq | foldpℓ, xq | concrpx, yq | padpℓ, xq
Programs    p ::“ function f pxq {s}
Primitive Types b ::“ int | bool | α | null | xℓy | ?xℓy
Types             τ ::“ b | CrT s | xf : T y
Refined Types     T ::“ tν : τ | pu
                                .
Type Definition C ::“ Crαs “ D! Σ. x : xf : T y
Contexts          Γ ::“ H | x : T ; Γ | e; Γ
Heaps             Σ ::“ emp | Σ ˚ ℓ ÞÑ x : CrT s | Σ ˚ ℓ ÞÑ x : xf : T y
Function Types S ::“ @ℓ, α. px : T q{Σ ñ D!ℓ1 . x1 : T 1 {Σ 1

                    Fig. 10: Syntax of Imp programs and types




B     Well Formedness and Expression Typing
Well-formedness rules are given in this section. Expression typing judgements
are given in Fig. 18.
                                                                                                    21




Subtyping                                                               Γ $ T1 ĺ T2 , Γ $ Σ ĺ Σ 1

                              ValidpJ Γ K ñ J p K ñ J p1 Kq
                                                                    ĺ-b
                              Γ $ tν : b | pu ĺ tν : b | p1 u
                                                      1
                                    Γ $T ĺT
                            ValidpJ Γ K ñ J p K ñ J p1 Kq
                                                             1
                                                                         ĺ-app
                        Γ $ tν : CrT s | pu ĺ tν : CrT s | p1 u
                                 1
                    Γ $T ĺT              Valid pJ Γ K ñ J p K ñ J p1 Kq
                                                                             ĺ-rec
                      Γ $ tν : xf : T y | pu ĺ tν : xf : T 1 y | p1 u
                    ValidpJ Γ K ñ J p K ñ J p1 ^ ν ‰ null Kq
                                                                           ĺ-down
                         Γ $ tν : ?xℓy | pu ĺ tν : xℓy | p1 u

   Valid pJ Γ K ñ J p K ñ J p1 Kq                         Valid pJ Γ K ñ J p K ñ J p1 Kq
                                     1
                                           ĺ-up1                                                ĺ-up2
 Γ $ tν : xℓy | pu ĺ tν : ?xℓy | p u                  Γ $ tν : null | pu ĺ tν : ?xℓy | p1 u

                                              Γ $ Σ ĺ Σ1 Γ $ T ĺ T 1
                            ĺ-emp                                                       ĺ-heap
      Γ $ emp ĺ emp                        Γ $ Σ ˚ ℓ ÞÑ x : T ĺ Σ 1 ˚ ℓ ÞÑ x : T 1

Heap Folding                                                              Γ $ x : T1 {Σ1 ✄ x : T2 {Σ2

                    locspT1 q X DompΣ1 q “ H Γ $ T1 ĺ T2
                                                                            F-base
                             Γ $ x : T1 {Σ1 ✄ x : T2 {Σ2

                   Σ1 “ Σ11 ˚ ℓ ÞÑ x : T Σ2 “ Σ21 ˚ ℓ ÞÑ x : T 1
                 Γ $ tν : xℓy | pu ĺ T2 Γ $ x : T {Σ11 ✄ x : T 1 {Σ21
                                                                                F-ref
                        Γ $ y : tν : xℓy | pu{Σ1 ✄ y : T2 {Σ2
                                Γ $ tν : ?xℓy | pu ĺ T2
                    Σ1 “ Σ11 ˚ ℓ ÞÑ y : T Σ2 “ Σ21 ˚ ℓ ÞÑ y : T 1
              x : tν : ?xℓy | p ^ ν ‰ nullu; Γ $ y : T {Σ11 ✄ y : T 1 {Σ21
              x : tν : ?xℓy | p ^ ν “ nullu; Γ $ y : T {Σ11 ✄ y : T 1 {Σ21
                                                                                 F-?ref
                         Γ $ x : tν : ?xℓy | pu{Σ1 ✄ x : T2 {Σ2
                             Γ $ x : Ti {Σ1 ✄ x : Ti1{Σ2
                                                                        F-heap
                       Γ $ y : xfi : Ti y{Σ1 ✄ y : xfi : Ti1 y{Σ2

              Fig. 11: Subtyping, heap subtyping, and heap folding rules
22

Statement Typing                                                                  Φ, Γ, Σ $ s :: Γ 1 {Σ 1

                                Γ, Σ $ e : tν : τ | pu
                                                                           T-assgn
                      Φ, Γ, Σ $ x “ e :: x : tν : τ | ν “ eu; Γ {Σ

                    Φ, Γ, Σ $ s1 :: Γ 1 {Σ 1 Φ, Γ 1 , Σ 1 $ s2 :: Γ 2 {Σ 2
                                                                            T-seq
                                Φ, Γ, Σ $ s1 ; s2 :: Γ 2 {Σ 2
                             Γ $ Σ ˚ ℓ ÞÑ x : T ℓ, x fresh
                                                                        T-pad
                         Φ, Γ, Σ $ padpℓ, xq :: Γ {Σ ˚ ℓ ÞÑ x : T
      Γ, Σ $ e : bool Φ, e; Γ, Σ $ s1 :: Γ1 ; Γ {Σ1 Φ, e; Γ, Σ $ s2 :: Γ2 ; Γ {Σ2
                    Γ $ Σ 1 Γ1 ; Γ $ Σ 1 ĺ Σ 1 Γ2 ; Γ $ Σ 2 ĺ Σ 1
           for each xi P Γ1 X Γ2 , Γ1 ; Γ, Σ1 $ xi : Ti Γ2 ; Γ, Σ2 $ xi : Ti
                          xi : Ti ; Γ, Σ 1 $ Ti xi : Ti ; Γ $ Σ 1
                                                                                                      T-if
                      Φ, Γ, Σ $ if e then s1 else s2 :: xi : Ti ; Γ {Σ 1
                             Γ $ x : xℓy ℓ ÞÑ z : xfi : Ti y P Σ
                                                                        T-rd
                             Φ, Γ, Σ $ y “ x.fi :: y : Ti ; Γ {Σ
                        Γ $ x : xℓy Γ $ e : tν : τ | pu
          Tr “ NameFieldspz, xf0 : T0 , . . . , fi : tν : τ | ν “ eu, . . .yq     z fresh
                                                                                               T-wr
               Φ, Γ, ℓ ÞÑ y : xfj : Tj y ˚ Σ $ x.fi “z e :: Γ {ℓ ÞÑ z : Tr ˚ Σ

       for each ef , Γ, Σ $ ef : Tf      T “ NameFieldspz, xf : T yq            ℓ, z fresh
                                                                                               T-alloc
             Φ, Γ, Σ $ x “z allocℓ tf : ef u :: x : xℓy; Γ {ℓ ÞÑ z : T ˚ Σ

        Γ, Σ $ x : xℓy Ty “ tν : τ | pu Tz “ tν : τ | ν “ yu z fresh
                                                                             T-concr
          Φ, Γ, ℓ ÞÑ y : Ty ˚ Σ $ concrpx, zq :: y : Ty ; Γ {ℓ ÞÑ z : Tz ˚ Σ
                                                                  .
                Γ $ Crαs “ D! Σc . xc : Tc Crαs $M mpxq “ em
                                        1
   Σ “ ℓ ÞÑ x : tν : CrT s | qu ˚ Σ0 Σ “ ℓ ÞÑ xc : rT {αsTc ˚ rT {αsΣc ˚ Σ0
          Γ, Σ $ T Γ, Σ 1 $ Σ 1 DompΣc q, BinderspΣc q, xc fresh
                                                                                  T-unfold
  Φ, Γ, Σ $ unfoldpℓ, xc ¨ DompΣc q ¨ BinderspΣc qq :: p mpxq “ em q; Γ {Σ 1
                                                              Ź
                                                                   m

                               Γ $ Crαs “ D! Σc . x : Tc
     Γ $ x : Tx {Σx ✄ x : rT {αsTc {rT {αsΣc Γ $ Źℓ ÞÑ y : Ty ˚ Σ 1 Γ $ Σ ĺ Σ 1
                            .
         Crαs $M mpxq “ em Ty “ tν : CrT s | m mpνq “ em u y fresh
                                                                                                  T-fold
             Φ, Γ, ℓ ÞÑ x : Tx ˚ Σx ˚ Σ $ foldpy, ℓq :: Γ {ℓ ÞÑ y : Ty ˚ Σ 1
          R “ xR : TR {ΣR P Γ         Γ $ e : re{xR sTR       Γ $ Σ ĺ re{xR sΣR
                                                                                              T-ret
                               Φ, Γ, Σ ˚ Σ 1 $ return e :: H
           Φ $ f :: S Γ, Σ $ pxj : Tj q{Σi ñ xo : To {Σo “ InstpS, ℓ, T q
                θ “ rej {xs py : Ty , Σo1 q “ AddHeappxo : To ; Γ, Σo q
               for each j, Γ, Σu ˚ Σm $ ej : θTj Γ $ Σm ĺ θΣi
                                                                                             T-call
                Φ, Γ, Σu ˚ Σm $ x “ f pej q :: x : θTo ; Γ {Σu ˚ θΣo

Fig. 12: Annotated Statement Typing Rules. In T-call, S is α-renamable. Note that
the well-formedness check requires all output binders to be fresh in the calling context.
We assume that type definitions (and, hence, measures over these definitions) Γ $
Crαs “ D! Σ. x : T are α-convertible.
                                                                                               23


Well Formed Types                                                                       Γ, Σ $ T

    FVppq Ď FVpν : b; Γ q Y FVpΣq p is well-sorted in ν : b; Γ and Σ
                                                                                  WF-prim
                             Γ, Σ $ tν : b | pu
                          .
                    Crαs “ D! Σ. x : xf : T y Γ, Σ $ q
          lengthpαq “ lengthptν : bi | pi uq Γ, Σ $ tν : bi | pi u
                                                                               WF-app
                         Γ, Σ $ tν : Crtν : bi | pi us | qu
              Γ, Σ $ tν : bi | pi u   Γ, Σ $ q       fi “ fi1 ñ i “ i1
                                                                            WF-rec
                        Γ, Σ $ tν : xfi : tν : bi | pi uy | qu

                               Fig. 13: Well Formed Types


Well Formed Type Definitions                                                                $C

                     Σ $ T x : tν : xf : T y | pu, Σ $ Σ
       x R FVpΣq     TypeVarspΣq Y TypeVarsptν : xf : T y | puq Ď α
                              .                                                  WF-def
                      $ Crαs “ D! Σ. x : tν : xf : T y | pu


                        Fig. 14: Well Formed Type Definitions


Well Formed Heaps and Worlds                            Γ $Σ      Γ, Σ $ Σ 1    Γ, Σ $ x : T {Σ 1

                                          Γ, Σ $ T Γ, Σ $ Σ 1
                                ℓ R DompΣ q x R BinderspΣ 1 q Y BinderspΓ q
                                              1
                WF-emp                                                                    WF-bind
 Γ, Σ $ emp                                       Γ, Σ $ ℓ ÞÑ x : T ˚ Σ 1
                                   Γ, Σ $ Σ
                                                  WF-heap
                                    Γ $Σ
                            x R Γ x : T ; Γ, Σ $ T
                               x : T ; Γ, Σ $ Σ 1
                                                      WF-wld
                                 Γ $ x : T {Σ 1

                       Fig. 15: Well Formed Heaps and Worlds


Well Formed Schemas                                                                     Γ, Σ $ S

           for each j, xj R FVpΓ q Y FVpΣq and xj : Tj ; Γ, Σi $ Tj
     xj : Tj ; Γ, Σ $ Σi xj : Tj ; Γ $ xo : To {Σo xo R FVpΓ q Y FVpΣq
                          FVpΣo q Ę FVpΓ q Y FVpΣq
                                                                                  WF-fun
                Γ, Σ $ @ℓ, α. pxj : Tj q{Σi ñ D!ℓo . xo : To {Σo


                             Fig. 16: Well Formed Schemas
24



Well Formed Measures                                                        Crαs $M mpxq “ e

        c P T˚          x : x. . . f : Tf . . .y P Γ       f : T ñ T 1 P Γ Γ $M e : T
      Γ $M c : T ˚          Γ $M x.f : Tf                         Γ $M fpeq : T 1

                 ‘ : T ˆ T 1 ñ T 2 P Γ Γ $M e : T Γ $M e1 : T 1
                                  Γ $M e ‘ e1 : T 2
                     Γ $M e : bool Γ $M e1 : T Γ $M e2 : T
                            Γ $M if e then e1 else e2 : T
                             .
                     $ Crαs “ D! Σ. x : T Tv “ SnapTypepT, Σq
                m : Tv ñ T P Γ x : Tv $M e : T x : null $M e : T
                                 Crαs $M mpxq “ e

                           Fig. 17: Well Formed Measures




Expression Typing                                                                   Γ, Σ $ e : T

                                                           x : tν : τ | pu P Γ
                                         T-int                                       T-var
      Γ, Σ $ n : tν : int | ν “ nu                     Γ, Σ $ x : tν : τ | ν “ xu
                                                                   T-null
                     Γ, Σ $ null : tν : null | ν “ nullu
                        Γ, Σ $ e1 : int Γ, Σ $ e2 : int
                                                                      T-op
                     Γ, Σ $ e1 ‘ e2 : tν : int | ν “ e1 ‘ e2 u
                         Γ, Σ $ e : tν : xℓy | pu
                                                       T-ref-inv
                   Γ, Σ $ e : tν : xℓy | p ^ ν ‰ nullu
                  Γ, Σ $ e : T1 Γ $ T1 ĺ T2 Γ, Σ $ T2
                                                           T-sub
                                Γ, Σ $ e : T2

                          Fig. 18: Expression Typing Rules




Function Typing                                                                       Φ $ f :: S

                  ℓ “ dompΣi q ℓo “ dompΣo qzdompΣi q
             H, emp $ S “ @ℓ. @α. px : T q{Σi ñ D!ℓo . xo : To {Σo
                       pΓ, Σq “ AddHeappx : T , Σi q
                     Φ, R “ xo : To {Σo ; Γ, Σ $ s :: H
                                                                             T-fun
                                Φ $ f :: S


                           Fig. 19: Function Typing Rules
                                                                                                       25




Substitution of Heap Binders
                                          #
                                           x1      ℓ ÞÑ x : T P Σ and ℓ ÞÑ x1 : T 1 P Σ 1
Subst pΣ, Σ 1 q “ θΣ 1   where     θx “
                                           x       otherwise

Fresh Renaming of Worlds

FreshSubst px : T {Σq                    “ FreshSubst’px, T, Σ, empq
FreshSubst’px, T, emp, θq                “ rx1 {xs ¨ θ x fresh
FreshSubst’px, T, ℓ ÞÑ y : Ty ˚ Σ, Σ 1 q “ FreshSubst’px, T, Σ, rℓ1 {ℓs ¨ ry 1 {ys ¨ θq     ℓ1 , y 1 fresh

Strengthening Field Names

NameFieldsptν : xf : tνf : τf | pf uy | puq “ tν : xf : tνf : τf | pf ^ νf “ fieldpν, f quy | pu


Function Instantiation
Instp@ℓ. S, ℓ1 ¨ L, T q “ Inst prℓ1 {ℓsS, L, T q
Instp@α. S, ǫ, T ¨ T q “ Inst prT {αsS, ǫ, T q
InstpS, ǫ, ǫq “ S

Local Context Strenghtening
                $
                ’
                ’pΓ, Σq                                              Σ “ emp
                &py : T ; Γ 1 , ℓ ÞÑ z : tν : τ | ν “ yu ˚ Σ 1 q
                ’
                                                                     Σ “ ℓ ÞÑ y : tν : τ | pu ˚ Σ0 ,
AddHeappΓ, Σq “
                ’
                ’
                ’                                                    x : xℓy P Γ, and z fresh
                 pΓ 1 , Σ 1 q                                        otherwise
                %

                 where     pΓ 1 , Σ 1 q “ AddHeappΓ, Σ0 q


                                   Fig. 20: Helper Functions
26

C     Soundness of ART

D     Soundness
We translate types, environments and heaps into separation logic assertions and
hence, typing derivations into separation logic proofs. We illustrate the transla-
tion by example and present the key theorems; see § C for details.

D.1    Translation
We define a translation J ¨ K from types, contexts, and heaps to assertions in sep-
aration logic. We translate a typing context Γ, Σ by conjoining the translations
of Γ and Σ. Next, we illustrate the translation of local contexts Γ and heaps Σ
using the insert function from Fig. 4. When we describe e.g. a Γ at a program
point, we are referring to the Γ before that program point’s execution.
Local Contexts We translate contexts Γ into a conjunction of pure, i.e. heap
independent, assertions. The context Γ0 before A contains two assumptions: (1) x
is a possibly null reference to &x and (2) x is definitely null. Note that &x does
not denote the application of a function called &; it is a distinct location named
&x. We translate Γ0 by conjoining the translations of these contents. Note that
translation states that if x is not null, then x refers to &x.
        .                                .
     Γ0 “ x : ?x&xy, x “ null     J Γ0 K “ px ‰ null ñ x “ &xq ^ px “ nullq
Heaps We interpret heaps as (separated) conjunctions of impure (i.e., heap-
dependent assertions) and pure assertions corresponding to the types of the
values stored in each location. The heap before A states that if the location
exists on the heap, then it refers a valid list, described by listpA, &x, xo q.
           .                                 .
       Σ0 “ &x ÞÑ x0 : listrAs       J Σ0 K “ p&x ‰ nullq ñ listpA, &x, x0 q (8)
Type Predicates We translate the definition of the listrAs type into a sepa-
ration logic assertion that characterizes the part of the heap where a listrAs is
stored. For example, for the list type from Fig. 4 we define the type predicate
as:
                 .
  listpA, ℓ, xq “ Snapshotpℓ, xq ^ Dh, t, ℓt . hdpA, ℓ, h, ℓt q ˚ ppℓt ‰ nullq ñ listpA, ℓt , tqq
                 .
hdpA, ℓ, h, ℓt q “ J ℓ ÞÑ h : xdata : A, next : ?xℓt yy K
Intuitively, the conjuncts of the assertion listpA, ℓ, xq say: (1) the snapshot x is a
pure value comprising all the records (data and references) that are transitively
reachable on the heap starting at ℓ, and (2) the heap satisfies the “shape” invari-
ants defined by the recursive alias type listrAs. We prove that each well-formed
type definition has a translation analagous to the above, allowing us translate
heap-locations mapped to recursive types in a manner analagous to eq. (8).
Records The other case is for heap-locations that are mapped to plain records.
At B, insert has allocated a record to which y refers. There, we have
      .                        .
  Γ1 “ Γ0 , y : &y (9) J Γ1 K “ J Γ0 K ^ py ‰ null ñ y “ &yq ^ py ‰ nullq (10)
                                                                                   27



i.e. the binding for y is translated to the assertion for a maybe-null pointer
plus the fact that y is not-null. The heap before executing B is translated:
                   .
            J Σ1 K “ J Σ0 K ˚ p&y ÞÑ y0 ^ y0 “ xdata: k, next: nullyq        (11)

D.2    Soundness Theorem
We prove soundness by showing that a valid typing of a statement s under given
contexts can be translated into a valid separation logic proof of s under pre-
and post-conditions obtained by translating the contexts. Note that there an
(semantics-preserving) elaboration step that, for clarity, we defer to § C which
inserts ghost variables to name locations and heap binders.
Theorem 1. [Typing Translation]
‚ If Φ, Γ, Σ $ s :: Γ 1 {Σ 1 then J Φ K $ tJ Γ, Σ Ku s tJ Γ 1 , Σ 1 Ku
‚ If Φ $ f :: S then J Φ K $ tPrepSqu Body pf q tPost pSqu
   PrepSq, Post pSq and Body pf q are the translations of the input and output
types of the function, the function (body) statement. By virtue of how contexts
are translated, the result of the translation is not a vacuous separation logic
proof. As a corollary of this theorem, our main soundness result follows:
Corollary 1. [Soundness] If Φ, ∅, emp $ s :: Γ {Σ, then J Φ K $ ttrueu s ttrueu
If we typecheck a program in the empty environment, we get a valid separation
logic proof of the program starting with the pre-condition true. We can encode
programmer-specified asserts as calls to a special function whose type encodes
the assertion. Thus, the soundness result says that if a program typechecks then
on all executions of the program, starting from any input state: (1) all memory
accesses occur on non-null pointers, and (2) all assertions succeed.
    The soundness proof proceeds by induction on the typing derivation. We show
that the typing rules correspond to separation logic proofs using the appropriate
proof rule. The critical parts of the proof are lemmas that translte the rules for
subtyping and folding recursive type definitions into separation logic entailments:
Lemma 1. [Folding] If Γ $ x : T1 {Σ1 ✄ x : T2 {Σ2 then
  J Γ K ñ J ℓ ÞÑ x : T1 ˚ Σ1 K ñ DFVpΣ2 q. J ℓ ÞÑ x : T2 ˚ Σ2 K ^ Dy. Snapshotpℓ, yq

Lemma 2. [Subtyping]
‚ If    Γ $ T1 ĺ T2      then     J Γ K ñ J T1 K ñ J T2 K
‚ If    Γ $ Σ1 ĺ Σ2       then     J Γ K ñ J Σ1 K ñ J Σ2 K
These lemmas effectively translate fold, unfold, and subtyping (Fig. 11) into a
combination of “skip” statements and the consequence rule of separation logic.
    For example, at B, insert is about to return the list that y points to (at
location &y). At this point the context is given by the Γ1 and Σ1 from eqs. (9)
28

and (11). Art checks that the context satisfies the output type of insert i.e.
that &y is the root of a valid list whose length equals one greater than (the
snapshot of) the input x. It uses subtyping and T-fold to obtain at C:
            .                                 .
        Γ2 “ Γ1 , lenpy1 q “ 1 ` lenpnullq Σ2 “ Σ0 ˚ &y ÞÑ y1 : listrAs
Using lemma 1 and lemma 2 we have: J Γ1 , Σ1 K ñ J Γ2 , Σ2 K In particular, note
that y1 names the snapshot value corresponding to the (single-celled) list referred
to by y, and the measure instantiation due to T-fold states that the length of
the snapshot is 1 greater than the length of the tail null. The implication follows
from the definitions of the length measure, the snapshot predicate and the type
predicate. We then use the implication in an instance of the consequence rule.
    Soundness of Art follows from the following: (1) data type definitions cor-
respond to an inductively defined set of pure snapshot values; (2) heap binders
correspond to snapshot values; (3) no data structure is modified without first
unfolding it, ensuring that each “snapshot” (or “version”) receives a fresh name.

D.3     Assertion language
Values in Imp are records, integers (which are also used as addresses), the con-
stant null, or products of integers and records. We assume an intuitionistic
interpretation of assertions (and thus p ˚ true ô p).
                Value “ Z Y O Y tnullu
                    O “ Records
                    Z “ Integers (and addresses)
                    S“ZˆO
Expressions E ::“ ¨ ¨ ¨
                | xf : Ey record constant
                | fpEq    UIF application

Assertions P ::“ ¨ ¨ ¨
               | emp    empty heap
               | E ÞÑ E singleton heap
               | P ˚ P separating conjunction
     With the following axiom:
                   py “ x. . . f : e . . .yq ñ pP ô rfieldpy, f q{esP q       (12)

D.4     Imp Proof Rules
In addition to the standard frame rule and consequence rule, we assume the
following axioms:
    Proof Rules                                             F $ tP u s tQu
Concretization
                            z R FVpeq x, z distinct
                     $ tx ÞÑ eu concrpx, zq tx ÞÑ e ^ z “ eu
                                                                                         29

Unfolding
                               $ tDx. P u unfoldpℓ, xq tP u
Folding
                              x does not appear free in P
                                $ tDx. P u foldpℓ, xq tP u
Padding
                                    ℓ, x distinct
                  $ tempu padpℓ, xq temp ^ ℓ “ null ^ x “ nullu
Assignment
                                       x R FVpeq
                                  $ tempu x “ e tx “ eu
Conditional
                    F $ tB ^ P u s1 tQu F $ t B ^ P u s2 tQu
                        F $ tP u if B then s1 else s2 tQu
Allocation
                                         x, z R FVpeq
      $ tempu x “z alloc tf : eu tx “ ℓ ^ ℓ ‰ null ^ x ÞÑ z ^ z “ xf : eyu
Access
                                     a, v distinct vars
                    $ ta ÞÑ xf : eyu v “ a.fi ta ÞÑ xf : ey ^ v “ ei u
Mutation
                                           z R FVpvq
           $ ta ÞÑ x. . . fi : ´ . . .yu a.fi “z v ta ÞÑ z ^ z “ x. . . fi : v . . .yu
Sequence
                            F $ tP u s tRu F $ tRu s1 tQu
                                  F $ tP u s; s1 tQu
Procedure Call
                                              .
                              gpx1 . . . xm q “ s; return xo
                  tP u gpx1 . . . xm q tQu, F $ tP u s; return xo tQu
                       F $ tP u x “ gpx1 . . . xm q tx “ xo ^ Qu
Return
                                $ tre{xo sP u return e tP u

D.5    Definitions
Definition 1 (Base type translation).
J x : int K        “ intpxq
J x : null K “ px “ nullq
J x : xℓy K        “ ppx “ ℓq ^ px ‰ nullqq
J x : ?xℓy K       “ pJ x : xℓy K _ J x : null K
J x : xfi : Ti y K “ px “ xfi : fieldpx, fi qy
30

Definition 2 (Local type binding translation).
J x : tν : b | pu K          “ rx{νsp ^ J x : b K
J x : tν : CrT s | pu K “ rx{νsp
                                                             Ź
J x : tν : xfi : Ti y | pu K “ rx{νsp ^ J x : xfi : Ti y K ^   J fieldpx, fi q : Ti K
                                                           fi:Ti Pτ


Definition 3 (Heap type binding translation).
     J ℓ ÞÑ x : tν : CrT s | pu K      “ ppℓ ‰ nullq ñ pJ x : tν : CrT s | pu Kq ˚ cpT, ℓ, xqq
                                       ^ ppℓ “ nullq ñ px “ nullqq
     J ℓ ÞÑ x : tν : xfi : Ti y | pu K “ ppℓ ‰ nullq ñ pJ x : tν : τ | pu K ˚ ℓ ÞÑ xq
                                       ^ ppℓ “ nullq ñ px “ nullqq

Definition 4 (Free Variables of Γ ,Σ).
                             FVpHq                “H
                             FVpx : ?xℓy; Γ q     “ tℓu Y FVpΓ q
                             FVpx : xℓy; Γ q      “ tℓu Y FVpΓ q

                             FVpempq            “H
                             FVpℓ ÞÑ x : T ˚ Σq “ tℓ, xu Y FVpΣq

Definition 5 (Pure Value Types). In order to show measure well formed-
ness, we extend the language of types with products (T ˆ T 1 ) and unions with
null (T ` null), and define:
                          SnapType : Type ˆ Heap Ñ Type
                                 #
                                  xℓy ˆ SnapTypepT, Σq ℓ ÞÑ x : T P Σ
             SnapTypepxℓy, Σq “
                                  xℓy                    ℓ R DompΣq
             SnapTypep?xℓy, Σq “ SnapTypepxℓy, Σq ` SnapTypepnull, Σq
             SnapTypepT, Σq “ T

Definition 6 (Pure Values from Type Definitions). For each type T we
denote the pure values associated with that type as T ˚ , which we define induc-
tively:
                                       ePZ        e P Value
                    null P null˚      e P int˚     e P α˚
                                                                      ˚
                              ePZ          e P null˚         e P xℓy
                                    ˚              ˚                   ˚
                             e P xℓy       e P ?xℓy         e P ?xℓy

         e ” xfi : Ti y   e P Ti ˚    e1 P T 1 ˚ e2 P T 2 ˚   e P T1 ˚ _ e P T2 ˚
                                ˚                           ˚                 ˚
           xfi : ei y P xfi : Ti y   pe1 , e2 q P pT1 ˆ T2 q    e P pT1 ` T2 q
                                             .
                                     Crαs “ D! Σ. x : T
                                                                   ˚
                         e P pSnapTypeprTα {αsT, rTα{αsΣq ` nullq
                                                       ˚
                                           e P CrTα s
                                                                                           31

Definition 7 (Constraints from Pure Values). We consider elements of C ˚
as “snapshots” of some heap. We “restore” these snapshots by mapping them to
assertions with the functions
                       Snapshot : Z ˆ Value Ñ Prop
                        Walk : Value Ñ Value ˆ PpZ ˆ Valueq
                           .
            Snapshotpℓ, xq “ ppℓ ‰ nullq ñ pℓ ÞÑ e fpℓ1 ,e1 qPh ℓ1 ÞÑ e1 qq
                where pe, hq “ Walkpxq
and where Walk is defined as follows:
                                    ď
         Walkpxf : eyq “ pxf : e1 y, hq            where       pe1 , hq “ Walkpeq
         Walkppe1 , e2 qq “ pe1 , tpe1 , e3 qu Y hq      where      pe3 , hq “ Walkpe2 q
              Walkpeq “ pe, Hq
Definition 8 (Assertions from Type Definitions). Given the definition
        .
Crαs “ D! Σ. x : T , define the assertion
             .
cpTα , ℓ, xq “ pDxc , FVpΣq. pℓ ÞÑ xc ^ J xc : rTα {αsT Kq ˚ J rTα {αsΣ K ^ Snapshotpℓ, xq
                                                                          .
Definition 9 (Interpretation of Measures). Let mpx : Crαsq “ e and s be a
                                                            .
mapping from variables to values. Define J mpxq Kexp “ J e Kexp where
                       J v Kexp psq “ v
                    J x.f Kexp psq “ spxq.f
                    J fpeq Kexp psq “ f pJ e Kexp psqq
                J e1 ‘ e2 Kexp psq “ J e1 Kexp psq ‘ J e2 Kexp psq
                               ‘ P t`, ´, . . .u
                                  #
                                    J e1 Kexp psq        J e Kexp psq “ true
J if e then e1 else e2 Kexp psq “
                                    J e2 Kexp psq        otherwise


Definition 10 (Interpretation of type contexts/worlds).
                          ľ ľ            ľ
                   JΓ K “   e    J x:T K  J type t “ T K
                                  ePΓ x:T PΓ         type¨¨¨PΓ

                         JΣ K “       ˚       J ℓ ÞÑ x : T K
                                  ℓÞÑx:T PΣ
                      J Γ, Σ K “ J Γ K ^ J Σ K
Definition 11 (Interpretation of procedure declarations). Assume that
      .
f pxq “ s. Given S “ @ℓ. @α. px : T q{Σi ñ D!ℓo . xo : To {Σo ,
 PrepSq “ J x : T K ^ J Σi K
Post pSq “ J xo : To K ^ J Σo K
Body pf q “ s
and the variables appearing in Post pSq and not PrepSq are considered to be
modified by f .
32

Definition 12 (Interpretation of procedure contexts).
J f : S; Φ K “ tPrepSqu Body pf q tPost pSqu; J Φ K

D.6    Type Soundness
We assume the following:
 1. The set of program variables (x,y, etc.) is disjoint from the set of symbols
    used to denote locations (ℓ, ℓ1 , etc.).
 2. All programs are in single static assignment form. The only variables which
    have more than one static assignment are “phi” variables which are assigned
    once in each branch of an “if” statement.
Lemma 3. If for every x : T P Γ , Γ $ T , then the only symbols that appear
in J Γ K are variables (x, y), arithmetic and equality symbols and uninterpreted
functions, and no variable appears bound twice.
Proof. By induction on the type well-formedness judgement.
Corollary 2. The location ℓ only appears in J Γ K if there exists x : T P Γ and
T “ tν : xℓy | pu or T “ tν : ?xℓy | pu.
Lemma 4. If Γ $ Σ, then for each ℓ ÞÑ x : T P Σ:
1. No binding x : T 1 appears in Γ .
2. J Σ K contains exactly one sub-assertion of the form ℓ ÞÑ x.
Proof. By definition of J Σ K and induction on the well-formedness judgement.
Lemma 5. If Γ, Σ $ S, then the formal arguments or free variables of the
output world of S do not appear free in Γ or Σ.
Proof. By the assumptions of WF-fun
Corollary 3. The location ℓ only appears in J Σ K if there exists ℓ1 ÞÑ x : T P Σ
and ℓ1 “ ℓ or T “ tν : xℓy | pu or T “ tν : ?xℓy | pu.
                                  .
Lemma 6. If $M mpx : Crαsq “ e, and v P C ˚ pAq, then J rv{xse Kexp P Values.
Proof. By induction on the Γ $M e : T judgement.
Lemma 7. [Subtyping]
‚ If    Γ $ T1 ĺ T2       then    J Γ K ñ J T1 K ñ J T2 K
‚ If    Γ $ Σ1 ĺ Σ2        then    J Γ K ñ J Σ1 K ñ J Σ2 K
Proof. By induction on the subtyping derivation.

Case Γ $ tν : τ | pu ĺ tν : τ | p1 u
   By assumption.
                                                                                   33

                                           1
Case Γ $ tν : CrT s | pC u ĺ tν : CrT s | p1C u
   By assumption,
                                        J Γ K ^ pC ñ p1C
   and
                                  J Γ K ^ J ν :T K ñ J ν :T 1 K
                   1
   for each T , T . By hypothesis and the definition of J ¨ K, and by the form
   of each T , each p only occurs positively in cptν : τ | pu, ℓ, xq. Destructing
   T as tν : τ | pu and T 1 as tν : τ | p1 u:
                                                .
                      J ν : tν : CrT s | pC u K “ pC ^ Dℓ. cpT , ℓ, νq
                                                ñ p1C ^ Dℓ. cpT 1 , ℓ, νq
                                                ô J ν : tν : CrT 1 s | p1C u K


Case Γ $ tν : xf : T y | pu ĺ tν : xf : T 1 y | p1 u
   Unfolding the definition of J ¨ K,
                     J ν : tν : xf : T y | pu K “ p ^ ν “ xf : fieldpf, νqy
                                                    ^ J fieldpν, f q : T K
    By hypothesis,
                                J Γ K ñ J ν :T K ñ J ν :T 1 K
                    1
    for each T , T , and applying eq. (12) gives us
                       J Γ K ñ J fieldpv, f q : T K ñ J fieldpv, f q : T 1 K
    Now,                                                ľ
                  J ν : T1 K “ p ^ xf : fieldpν, f qy ^     J fieldpν, f q : T K
                                                           f:T
    so, combined with the assumption that J Γ K ñ p ñ p1 ,
                                                  ľ
                 J Γ K ñ p ^ xf : fieldpν, f qy ^  J fieldpν, f q: T 1 K
                                                        f:T 1

    which is equivalent to tν : xf : T 1 y | p1 u


Case Γ $ tν : ?xly | pu ĺ tν : xly | p1 u
   By assumption,
                                  J Γ K ñ p ñ pp1 ^ ν ‰ nullq
   By definition,
              J ν : tν : ?xly | pu K “ p ^ pν “ l ^ ν ‰ nullq _ pν “ nullq
   and thus, combined with the assumption,
                            J Γ K ñ p ñ pp1 ^ ν “ l ^ ν ‰ nullq
   which implies
                         J ν : tν : xly | p1 u K “ p1 ^ ν “ l ^ ν ‰ null
34

Case Γ $ tν : xly | pu ĺ tν : ?xly | p1 u
   By assumption,
                             J Γ K ñ p ñ pp1 ^ ν ‰ null ^ ν “ lq
     and thus
                    J Γ K ñ p ñ pp1 ^ ppν ‰ null ^ ν “ lq _ ν “ nullqq
     which is equivalent to J ν : tν : ?xly | p1 u K.


Case Γ $ tν : null | pu ĺ tν : ?xly | p1 u
   By assumption,
                            J Γ K ñ p ñ pp1 ^ ν “ nullq
     and thus
                    J Γ K ñ p ñ pp1 ^ ppν ‰ null ^ ν “ lq _ ν “ nullqq
     which is equivalent to J ν : tν : ?xly | p1 u K.


Case Γ $ emp ĺ emp
   The heaps are equivalent and their domains are empty, so the conclusion is
   trivially true.


Case Γ $ Σ ˚ ℓ ÞÑ x : T ĺ Σ 1 ˚ ℓ ÞÑ x : T 1
   By the inductive hypothesis,
                                     J Γ K ñ J Σ K ñ J Σ1 K
     and by assumption and the definition of J ¨ K,
                             J Γ K ñ J ℓ ÞÑ x : T K ñ J ℓ ÞÑ x : T 1 K
     hence,
                      J Γ K ñ J ℓ ÞÑ x : T K ˚ J Σ K ñ J ℓ ÞÑ x : T 1 KJ Σ 1 K
     and thus,
                        J Γ K ñ J ℓ ÞÑ x : T ˚ Σ K ñ J ℓ ÞÑ x : T 1 ˚ Σ 1 K
                                                                                 \
                                                                                 [

As a consequence of our interpretation of typing contexts, the following lemma
immediately follows:

Lemma 8. Assume that Φ, Γ , and Σ are (respectively) well formed global, local,
and heap contexts. We may then write the denotation of these typing contexts in
the following way:
                              J Γ, Σ K “ G ˚ H
where the following hold:

 1. G is pure.
                                                                                   35

2. G is a conjunction of the assertions
                                       .
                                   Gx “ J x : T K
   for each x : T P Γ . G may thus be written ¨ ¨ ¨ ^ Gx ^ ¨ ¨ ¨ for each such binding
   in Γ .
3. H is a conjunction (via ˚) of the assertions
                                .
                            Hℓ “ pℓ “ nil _ J ℓ ÞÑ x : T Kq
   for each ℓ ÞÑ x : T P Σ. G may thus be written ¨ ¨ ¨ Hℓ ¨ ¨ ¨ for each such binding
   in Σ.

Proof. Follows immediately from the definition of J ´ K.

Lemma 9.
   If     Γ, Σ $ e : T
Then      J Γ, Σ K “ G ˚ H
such that
1. G is pure.
2. G ñ J e : T K

Proof. By induction on the expression typing judgment. In particular, we make
use of the fact that the typing and subtyping rules for pure expressions only
depend on Γ . Subsumption requires application of lemma 7.

Lemma 10. Suppose that Γ, Σ $ x : xℓy and that Γ $ Σ “ Σ0 ˚ ℓ ÞÑ y : T . It
then follows that J Γ, Σ K “ G ˚ H ˚ Hℓ where G is pure and:
  (i) G ñ px “ ℓ ^ x ‰ nullq
 (ii) H “ H 1 ˚ Hℓ ˚ H 2 such that
                                     G ˚ Hℓ ñ J x ÞÑ y : T K
        and furthermore, if T is a record type,
                                G ˚ J x ÞÑ y : T K ˚ Hℓ ñ x ÞÑ y
        equivalently:
                         G ˚ J x ÞÑ y : T K ˚ Hℓ ñ x ÞÑ xfi : fieldpy, fi qy

Proof. Follows from lemma 4 and the definition of J ´ K.

Lemma 11. [Folding] If Γ $ x : T1 {Σ1 ✄ x : T2 {Σ2 then
  J Γ K ñ J ℓ ÞÑ x : T1 ˚ Σ1 K ñ DFVpΣ2 q. J ℓ ÞÑ x : T2 ˚ Σ2 K ^ Dy. Snapshotpℓ, yq

Proof. By induction on the judgement derivation.

Case F-base
   By the subtyping hypothesis,
                             J Γ K ^ J ℓ ÞÑ x : Ta K ñ J ℓ ÞÑ x : T2 K
36

     And thus, by letting every other ℓ P DompΣ2 q “ null,
                                 DFVpΣ2 q. J ℓ ÞÑ x : T2 ˚ Σ2 K.
     Since T1 contains no pointers, and since we are assuming the satisfiability of
     J x : T1 K, we can construct y from the base type of T1 and its refinement.


Case F-ref
   By the subtyping hypothesis, where T1 “ tν : xℓ1 y | pu,
                                  J Γ K ñ J x : T1 K ñ J x : T2 K
     And by the inductive hypothesis,
     J Γ K ñ J ℓ1 ÞÑ x : T ˚ Σ11 K ñ DFVpΣ21 q. J ℓ1 ÞÑ x : T 1 ˚ Σ21 K ^ Ds. Snapshotpℓ1 , eq
     Combining the two gives us
                                 DFVpΣ2 q. J ℓ ÞÑ y : T2 ˚ Σ2 K.
                                                    ˚
     We construct y “ pℓ , sq so that y P xℓ1 y to yield
                            1

                                         Snapshotpℓ, yq


Case F-?ref
   By hypothesis,
                  ppx ‰ nullq ^ J Γ, ℓ ÞÑ x : T ˚ Σ11 Kq ñ
                    pDFVpΣ21 q. J ℓ ÞÑ x : T 1 ˚ Σ21 K ^ Dy 1 . Snapshotpℓ, y 1 qq
                  ppx “ nullq ^ J Γ, ℓ ÞÑ x : T ˚ Σ11 Kq ñ
                    pDFVpΣ21 q. J ℓ ÞÑ x : T 1 ˚ Σ21 K ^ Dy 1 . Snapshotpℓ, y 1 qq
     In the first case, px ‰ nullq we let
                                           y “ pℓ, y 1 q.
     In the second case,
                                            y “ null.
     We combine both hypotheses and y constructions to conclude:
                                 DFVpΣ2 q. J ℓ ÞÑ x : T2 ˚ Σ2 K.
     and, by definition, Snapshotpℓ, yq,


Case F-heap By hypothesis,
                  J Γ, ℓ ÞÑ x : T ˚ Σ1 Kq ñ
                     pDFVpΣ2 q. J ℓ ÞÑ x : T ˚ Σ2 K ^ Dxi . Snapshotpℓ, xi qq
     for each fieldpx, fi q in T1 . If we substitute fieldpx, fi q for x in each conclusion,
     we conclude
                                        J ℓ ÞÑ x : T2 ˚ Σ2 K
     and we construct y “ xfi : xi y.
                                                                                         37

                                                                                         \
                                                                                         [

Lemma 12. Given the definition
                                        .
                                   Crαs “ D! Σ. x : T ,
and the set of corresponding pure values, C ˚ pAq:
                  Snapshotpℓ, xf q ^ J ℓ ÞÑ x : T ˚ Σ K ñ xf P C ˚ pAq
                                                    ˚
Proof. By contrapositive. Assume xf R CpAq . Then
                                xf R PureC pA, C ˚ , T qΣ.
The proof is by induction on the derivation of xf R PureC pA, C ˚ , T q. The base
case starts with the root of Snapshotpℓ, xf q
                             Snapshotpℓ, xf q “ ℓ ÞÑ e ˚ ¨ ¨ ¨
                     ˚
If xv R PureC pA, C , T qΣ then either e is not a record value, trivially showing
  J ℓ ÞÑ x : T ˚ Σ K, or xv contains some field f with value ef such that.

  (i) f : Tf P T ;
 (ii) and ef R PureC pA, C ˚ , Tf qΣ

Assuming ef ‰ pℓ1 , e1 q, if ef R PureC pA, C ˚ , Tf qΣ, then the assertion in Snapshotpℓ, xf q,
ℓ ÞÑ x. . . f : ej . . .y, must not satisfy the corresponding J ℓ ÞÑ x : T K (by the defini-
tion of PureC pA, C ˚ , T qΣ. If ef “ pℓ1 , e1 q for some ℓ1 , e1 , then e1 R PureC pA, C ˚ , Tf qΣ
However, by the same reasoning as above, Snapshotpℓ1 , e1 q must not be equisat-
isfiable with J ℓ ÞÑ x : T ˚ Σ K

Theorem 2. [Statement Typing] If Φ, Γ, Σ $ s :: Γ 1 {Σ 1                    then J Φ K $
tJ Γ, Σ Ku s tJ Γ 1 , Σ 1 Ku

Proof. By induction on the typing derivation of s.

Case x “ e:
   By assumption, x does not appear in Γ . Since e is well-typed, x R FVpeq. By
   the frame rule, since x R Γ and x R Σ, we derive the following rule:

                            $ tJ Γ, Σ Ku x “ e tJ Γ, Σ K ˚ x “ eu
    We then perform the deduction by the definition of J ¨ : ¨ K:
                                                 (
                          J Γ, Σ K ^ px “ eq
                                                             (
                          J Γ, Σ K ^ J x : tν : τ | ν “ eu K
                                                        (
                          J x : tν : τ | ν “ eu; Γ, Σ K



Case s; s1
   By hypothesis,
                                Φ $ tJ Γ, Σ Ku s1 tJ Γ 1 , Σ 1 Ku
38

     and
                                Φ $ tJ Γ 1 , Σ 1 Ku s2 tJ Γ 2 , Σ 2 Ku
     By straightforward application of the sequence rule, we immediately conclude
                               Φ $ tJ Γ, Σ Ku s1 ; s2 tJ Γ 2 , Σ 2 Ku



Case if e then s1 else s2 :
   By hypothesis:
                           Φ $ te ^ J Γ, Σ Ku s1 tJ Γ1 ; Γ, Σ1 ˚ Σ11 Ku
     and
                         Φ $ t e ^ J Γ, Σ Ku s2 tJ Γ2 ; Γ, Σ2 ˚ Σ21 Ku
     For each xi , by lemma 7
                      J Γ1 ; Γ K ñ J xi : T 1 K and     J Γ2 ; Γ K ñ J xi : T 1 K
     and by lemma 7
               J Γ1 ; Γ K ñ J Σ1 K ñ J Σ 1 K and        J Γ2 ; Γ K ñ J Σ2 K ñ J Σ 1 K
     Combining these facts allows us to conclude,
           J Γ1 ; Γ, Σ1 K ñ J xi : Ti ; Γ, Σ 1 K and    J Γ2 ; Γ, Σ2 K ñ J xi : Ti ; Γ, Σ 1 K
     and thus, by consequence,
                             Φ $ te ^ J Γ, Σ Ku s1 tJ xi : Ti ; Γ, Σ 1 Ku
     and
                           Φ $ t e ^ J Γ, Σ Ku s2 tJ xi : Ti ; Γ, Σ 1 Ku
     hence, by the conditional rule,
                   Φ $ tJ Γ, Σ Ku if e then s1 else s2 tJ xi : Ti ; Γ, Σ 1 Ku



Case concr (x,z):
   Letting J Γ, Σ K “ G ˚ H by lemma 8, by assumption
                                           (
                                    G˚H
     By hypothesis and lemma 10,
                                                                             (
                          G ˚ H ˚ px “ ℓ ^ ℓ ‰ nullq ˚ J ℓ ÞÑ y : Ty K
     By consequence, assuming without loss of generality that Ty is a record type,
     substitution on the rule for concr, and applying the frame rule,
                                                                 (
                G ˚ H ˚ px “ ℓ ^ ℓ ‰ nullq ˚ x ÞÑ y ˚ J y : Ty K
                concrpx, zq
                                                                          (
                  G ˚ H ˚ px “ ℓ ^ ℓ ‰ nullq ˚ x ÞÑ y ˚ J y : Ty K ^ z “ y ,
                                                                                     39

   since z is a fresh variable. By definition of J ´ K and Ty1 , since z does not
   appear free in G, H or Ty ,
                             J y : Ty ; Γ, ℓ ÞÑ z : Tz ˚ Σ 1 K
                                                               (




Case padpℓ, xq
   Beginning with the proof rule for padpℓ, xq,
                     $ tempu padpℓ, xq temp ^ ℓ “ null ^ x “ nullu
   By hypothesis, neither ℓ nor x appear in Γ or Σ, and thus do not appear in
   J Γ, Σ K, so we can apply the frame rule:
                 $ tJ Γ, Σ Ku padpℓ, xq tJ Γ, Σ K ˚ pℓ “ null ^ x “ nullqu
   By consequence,
                       $ tJ Γ, Σ Ku padpℓ, xq tJ Γ, Σ K ˚ J ℓ ÞÑ x : T Ku
   And thus,
                         $ tJ Γ, Σ Ku padpℓ, xq tJ Γ, Σ ˚ ℓ ÞÑ x : T Ku



Case unfoldpℓ, zq
   Letting J Γ, Σ K “ G ˚ H ˚ J ℓ ÞÑ x : CrT s K by lemma 8 and by assumption,
                                                                           (
         G ˚ H ˚ pppℓ ‰ nullq ñ cpT , ℓ, xqq ^ ppℓ “ nullq ñ px “ nullqqq
   First, assume ℓ “ null. Then,
                                                                  (
                              G ˚ H ˚ pℓ “ null ^ x “ nullq
   And by lemma 6,
                                                  ľ                    (
                       G ˚ H ˚ px “ nullq ^        J mpnullq Kexp “ em
                                                     m
   Quantifying over x allows us to complete the proof via consequence and the
   frame rule:
                 (
        J Γ, Σ K
                                                   ľ                      (
        DFVp...q. G ˚ H ˚ pℓ “ null ^ x “ nullq ^     J mpnullq Kexp “ em
                                                            m
       unfoldpℓ, y ¨ yq
                                                 ľ                    (
         G ˚ H ˚ pℓ “ nullx “ nullq ^             J mpnullq Kexp “ em
                                                 m
             ľ
                                        1
                                             (
         J       J mpyq Kexp “ em ; Γ, Σ K
             m

   Next, we assume ℓ ‰ null. By definition,
                                                                                 (
                 G ˚ H ˚ Dxc . DFVpΣc q. J ℓ ÞÑ xc : Tc ˚ Σ K ^ Snapshotpℓ, xq
40

     By hypothesis, xc and the free variables of J Σc K have been α-renamed and
     do not appear in J Γ K or J Σ K. By the unfold axiom and the frame rule,
                                                                                   (
        G ˚ H ˚ Dxc . DFVpΣc q. J ℓ ÞÑ xc : rT {αsTc ˚ rT {αsΣc K ^ Snapshotpℓ, xq
      unfoldpℓ, xc ¨ DompΣc q ¨ BinderspΣc qq
                                                                    (
        G ˚ H ˚ J ℓ ÞÑ xc : rT {αsTc ˚ rT {αsΣc K ^ Snapshotpℓ, xq
     where x P C ˚ . Therefore, by lemma 6, each well-formed measure on Crαs,
     m, is defined on x and we strengthen:
                                                                   ľ                 (
      G ˚ H ˚ J ℓ ÞÑ xc : rT {αsTc ˚ rT {αsΣc K ^ Snapshotpℓ, xq ^  J mpxq Kexp “ em
                                                                                      m
     Which is, by definition
                                     ľ
                                         J mpxq Kexp “ em ; Γ K ^ J Σ 1 K
                                                                                  (
                                 J
                                     m



Case x “z alloc tf : ef u
   By assumption, x does not appear bound in Γ and ℓ does not appear in
   J Γ, Σ K. Applying the frame rule to the rule for alloc gives us the precon-
   dition
                                               (
                                      J Γ, Σ K
     and the postcondition
                                                                                           (
                       J Γ, Σ K ˚ x “ ℓ ^ ℓ ‰ null ^ x ÞÑ z ^ z “ xf : ey
     Rearranging and by consequence:
                                                                                               (
             J Γ, Σ K ˚ x “ ℓ ^ ℓ ‰ null ^ pℓ ‰ null ñ ℓ ÞÑ z ^ z “ xf : eyq
     By the typing hypotheses and lemma 9,
                                             J Γ K ñ J e : Tf K
                                                                                                        (
       J Γ, Σ K ˚ x “ ℓ ^ ℓ ‰ null ^ pℓ ‰ null ñ ℓ ÞÑ z ^ z “ xf : ey ^ J e : Tf Kq
     so eq. (12) and the definition of J ¨ K imply,
                                                                    (
                                            J Γ, Σ ˚ ℓ ÞÑ z : T K


Case y “ x.fi
   By hypothesis, lemma 8 and lemma 10, we let
                      J Γ, Σ K “ G ˚ H ˚ J ℓ ÞÑ z : x. . . fi : fieldpz, fi q . . .y K
     and by consequence,
                                                                                           (
                       G ˚ H ˚ J z : xf : Ti y K ˚ x ÞÑ x. . . fi : fieldpz, fi q . . .y
     By the frame rule:
                                                                              (
          G ˚ H ˚ J z : xf : Ti y K ˚ x ÞÑ x. . . fi : fieldpz, fi q . . .y
        y “ x.fi
                                                                                                    (
          G ˚ H ˚ J z : xf : Ti y K ˚ x ÞÑ x. . . fi : fieldpz, fi q . . .y ^ py “ fieldpz, fi qq
                                                                                             41

   Unfolding the definition of J ¨ K and by consequence (using the equality y “
   fieldpz, fi q),
                                                                                              (
               G ˚ H ˚ J z : xf : Ti y K ˚ x ÞÑ x. . . fi : fieldpz, fi q . . .y ^ J Ti : y K
   And hence, by definition and consequence (to weaken the mapping of x and
   applying the equality x “ ℓ),
                                                    (
                                  J y : Ti ; Γ, Σ K



Case x.fi “z e:               (
   Starting from      J Γ, Σ K , by lemmas 8 and 10, we deduce by consequence,
                                                                                                (
     pG ˚ px “ ℓ ^ ℓ ‰ nullq ˚ H ˚ J y : xfj : tν : τj | pj uy K ˚ x ÞÑ xfj : fieldpy, fj qyq
   Thus, by the frame rule,
                                                                                                (
     pG ˚ px “ ℓ ^ ℓ ‰ nullq ˚ H ˚ J y : xfj : tν : τj | pj uy K ˚ x ÞÑ xfj : fieldpy, fj qyq
    x.fi “z e
                                                                                                        (
     pG ˚ px “ ℓ ^ ℓ ‰ nullq ˚ H ˚ J y : xfj : tν : τj | pj uy K ˚ x ÞÑ z ^ z “ x. . . fi : e . . .yq
   By consequence and lemma 9,
                  pG ˚ J e : tν : τ | pu K ˚ px “ ℓ ^ ℓ ‰ nullq ˚ H
                                                                                         (
                  ˚ J y : xfj : tν : τj | pj uy K ˚ x ÞÑ z ^ z “ x. . . fi : e . . .yq
   Unfolding the definition of J ¨ K, this expands to
                  pG ˚ J e : tν : τ | pu K ˚ px “ ℓ ^ ℓ ‰ nullq ˚ H
                                                 ľ
                   ˚ y “ xfj : fieldpy, fj qy ^     J fieldpy, fj q : Tj K
                                                  fj:Tj
                                                                                         (
                  ˚ J y : xfj : tν : τj | pj uy K ˚ x ÞÑ z ^ z “ x. . . fi : e . . .yq
   By eq. (12),
                       pG ˚ J e : tν : τ | pu K ˚ px “ ℓ ^ ℓ ‰ nullq ˚ H
                                                      ľ
                        ˚ y “ xfj : fieldpy, fj qy ^     J fieldpy, fj q : Tj K
                                                          fj:Tj

                        ˚ J y : xfj : tν : τj | pj uy K ˚ x ÞÑ z
                        ^ z “ xf0 : fieldpy, f0 q . . . fi : fieldpz, fi q . . .y
                                                  (
                        ^ pfieldpz, fi q “ eq
   By definition of J ¨ K,
                       pG ˚ J e : tν : τ | pu K ˚ px “ ℓ ^ ℓ ‰ nullq ˚ H
                                                      ľ
                        ˚ y “ xfj : fieldpy, fj qy ^     J fieldpy, fj q : Tj K
                                                          fj:Tj
                                                                            (
                        ˚ J y : xfj : tν : τj | pj uy K ˚ J ℓ ÞÑ z : Tr K
42

     and thus, by definition,
                                              (
                                   J Γ, Σ K
                                 x.fi “ e
                                                            (
                                   J Γ, ℓ ÞÑ z : Tr ˚ Σ K


Case foldpℓ, zq
                 .
   Given Crαs “ D! Σ. x : T ,
                   .
     cpTα , ℓ, yq “ pDx, FVpΣq. J ℓ ÞÑ x : rTα {αsT ˚ rTα {αsΣ K ^ Snapshotpℓ, yq
   By lemma 11 applied to the type judgement folding assumption we deduce
     DFVpΣc q. J ℓ ÞÑ x : θTc ˚ θΣc K ^ Dy. Snapshotpℓ, yq where θ “ rT {αs
   and, by the definition of cpT , ℓ, xq:
                                      Dy. cpT , ℓ, yq
   Applied to the rule for fold (ℓ,y), since by assumption y is a fresh variable,
                       $ tDy. cpT , ℓ, yqu foldpℓ, yq tcpT , ℓ, yqu
                             ˚
     By lemma 12, x P CrT s , so by lemma 6, each well-formed measure on Crαs,
     m, is defined on y. By the form of Tc and the definition of Snapshot, for any
     field of x fieldpy, f q “ fieldpx, f q and we thus strengthen the postcondition:
                                                 ľ            (
                                   cpT , ℓ, yq ^   mpyq “ em .
                                              m
     Applying the frame rule and consequence with the definition of Ty and
     lemma 7 applied to Σ 1 ,
           Φ $ tJ Γ, ℓ ÞÑ x : Tx ˚ Σx ˚ Σ Ku foldpℓ, yq tJ Γ, ℓ ÞÑ y : Ty ˚ Σ 1 Ku


Case xr “ f pxq
   Assuming f : S and
                  S “ @ℓ. @α. px : T q{Σi ˚ Σi1 ñ D!ℓo . xo : To {Σo
   let P “ PrepSq and Q “ Post pSq. We apply the substitution θ “ rej {xj s to
   obtain:
                           θP “ J ej : θTj K ^ J θΣi K
                           θQ “ J xo : θTo K ^ J θΣo K
   By lemmas 7 and 8,
                            J Γ K ñ J ej : θTj K
                                 J Γ K ñ J Σm K ñ J θΣi K
     and thus
                        J Γ K ñ J Σu ˚ Σm K ñ J Γ K ^ θP ˚ Σu
     Which gives us, by consequence, and framing of Γ and Σu , and unfolding
     the definition of Q,
                    Φ $ tJ Γ, Σm ˚ Σu Ku x “ f pej q tJ Γ, Σu ˚ θΣo Ku
                                                                             43

                                                                              \
                                                                              [

Theorem 3. [Procedure Typing]
If Φ $ f :: S then J Φ K $ tPrepSqu Bodypf q tPost pSqu.

Proof. Let
               P “ PrepSq “ J x : T K ^ J Σi K
               Q “ Post pSq “ J xo : To K ^ J Σo K
                                                                 .
By inversion on the judgement, we must have typed a statement s1 “ return e
for some expression, or a sequence of statements ending in a return. By the
statement typing theorem,
                            Φ $ tPrepSqu s tJ Γs , Σs Ku
Applying lemma 9 and lemma 7 to the hypotheses of the return typing rule, we
determine
                            J Γs , Σs K ñ re{xo sJ xo : To K
                            J Γs , Σs K ñ re{xo sJ Σo K.
and thus
                        Φ $ tJ Γs , Σs Ku return e tPost pSqu.
By the sequence rule,
                        Φ $ tPrepSqu s; return e tPost pSqu.
                                                                              \
                                                                              [

Corollary 4. [Soundness] If Φ, ∅, emp $ s :: Γ {Σ, then J Φ K $ ttrueu s ttrueu


E    Heap Annotation Inference

Up until this point, our presentation has assumed that the annotations concr,
unfold, and fold have already been inserted into the source file. To alleviate
this burden, Art automatically inserts these annotations at critical locations
in the input program. To be sure, the soundness of the type system does not
depend on any particular algorithm for inferring these locations. In fact, while
the algorithm we will present was sufficient for the benchmarks we used to test
Art, it would be entirely feasible to swap our algorithm for another. In this
section, we will describe the simple source elaboration that preceeds refinement
type checking and inference.
Annotation inference. To formalize our method of inferring annotation loca-
tions, we define a function F with type:
                    F : Statement ˆ S Ñ Statement ˆ PpUq
                     .
                   S “ Type Bindings ˆ Heap ˆ Function ˆ U
                     .
                   U “ Location ˆ Type Constructor
44

Thus, F ps, pΓ, Σ, f, Uqq transforms the statement s yielding a new (possibly com-
pound, i.e. comprising several sequenced statements) statement and a new set of
unfolded locations. The input to F is s, the statement to be transformed; Γ , con-
taining physical type information for local variables; Σ, containing physical heap
type information; f , the physical specification of the function containing s; and
U, a set of pℓ, Cq pairs that denote unfolded locations and the type constructor
that was unfolded.
     Because this step preceeds refinement type checking, the only type informa-
tion that is available is base type information – i.e. all types are of the form
tν : τ | trueu. Definitions for F on the statements that may possibly generate
annotations are given in Fig. 21, with some helper functions given in Fig. 22.
Function Declarations. F transforms programs function by function. Thus it
simply calls F recursively on the function body, querying the type system to
determine Γ and Σ with Envpf q and HeapInpf q.
Field Access and Mutation. On a field read or write, Art computes the
set of locations that must be unfolded, using the UnfoldList helper. UnfoldList
computes this list by (1) consulting Γ and heap to determine if x points to a
location that is folded up; and (2) subtracting from this list all locations that
are already unfolded . Art inserts unfold calls for these locations before the
field access.
    Art also optimistically inserts a concr before a field access. The concr will
type check exactly when the field access type checks.
Function Return. At function returns, Art must take care to ensure that Σ
agrees with the current function’s specified heap with respect to which locations
folded. If a location in the function’s schema is unfolded, it must first be folded
up. At a return statement in a function, f , Art computes these locations by
comparing the current heap, Σ with f ’s specified heap. Given a “current” heap
Σ and a “target” heap Σ 1 , FoldList computes the set of locations in Σ that must
be folded up. These locations may depend on each other, so FoldList orders these
fold calls using the FoldOrder function.
Function Calls. With respect to folds, function calls behave exactly like func-
tion returns.
Example. Revisiting abslist, consider the following:
 var l1 = { data:0, next:null };
 var l2 = { data:1, next:l1   };
 absList(l2);
FoldList determines that the locations (and their associated types) that must be
folded up before calling abslist are (&l2, List[number]) and (&l1, List[number]).
However, &l2 depends on &l1. FoldOrder realizes this dependency with the cor-
rect ordering fold(&l1); fold(&l2);. The code is annotated with fold and
concr calls are as follows:
 var l1 = { data:0, next:null };
 var l2 = { data:1, next:l1   };
 //: fold(&l1);
                                                                                 45

 //: fold(&l2);
 absList(l2);
If Statements. To annotate if statements, Art calls F on the statements
in the “then” and “else” branches. To determine which statements must be
folded, F calculates three sets. L1 and L2 are the sets of unfolded locations that
were previously folded before the if statement. Additionally, F queries the type
checker to get heaps Σ1 and Σ2 that are returned from type checking s1 and
s2 , respectively. These heaps are used to determine Lalias , by calling Alias. This
procedure determines if a location ℓ would cause any references to become aliased
(and thus eventually fail to type check). Using the same ordering as in function
returns and function calls, Art calls FoldOrder to determine the sequence of
folds that need to occur in both the “then” and “else” branches.
Example. In the following, suppose x is a pointer to a list. The code
 var d = x.data;
 if (d > 0) {
   x.next = { data: 1, next: null };
 } else {
   x.next = { data: -1, next: null };
 }
would thus be annotated
 //: unfold(&x)
 var d = x.data;
 if (d > 0) {
   x.next = { data: 1, next: null };
   //: fold(&x)
 } else {
   x.next = { data: -1, next: null };
   //: fold(&x)
 }
because the next fields of x.next at the end of either branch point to different
locations. Folding &x ensures a consistent view of the heap after the control flow
join.
Padding Whenever a heap subtyping occurs, it is possible that the sub-heap has
fewer locations than the super-heap. However, the heap subtyping judgements
requires the sub-heap and super-heap to have equivalent domains. We insert pad
statements at these locations when the physical type checker determines that the
sub-heap’s domain is too small.
46




                  Fpfunction f pxq {s}, Sq “ pfunction f pxq {s1 }, Hq
                                where ps1 , ´q “ Fps, pEnvpf q, HeapInpf q, f, Hqq


                   Fpy “ x.fi , pΓ, Σ, f, Uqq “ pconcrpxq; u; y “ x.fi , U 1 q
                                where pu, U 1 q “ UnfoldListpx, Γ, Σ, Uq


                   Fpx.fi “ e, pΓ, Σ, f, Uqq “ pconcrpxq; u; x.fi “ e; concrpxq, U 1 q
                                where pu, U 1 q “ UnfoldListpx, Γ, Σ, Uq


                   Fpx “ gpeq, pΓ, Σ, f, Uqq “ pw; p; x “ gpeq, U 1 q
                                      where p “ PadLocspΣ, HeapOut pgqq
                                       pw, U 1 q “ FoldListpΣ, HeapOut pgq, Uq


                  Fpreturn e, pΓ, Σ, f, Uqq “ pw; p; return e, Hq
                                      where p “ PadLocspΣ, HeapOut pf qq
                                       pw, U 1 q “ FoldListpΣ, HeapOut pf q, Uq


Fpif e then s1 else s2 , pΓ, Σ, f, Uq as Sq “ pif e then s11 ; w1 ; p1 else s12 ; w2 ; p2 , UzLalias q
                                    where p1 “ PadLocspΣ1 , Σ2 q
                                              p2 “ PadLocspΣ2 , Σ1 q
                                        1
                                      ps1 , U1 q “ Fps1 , Sq
                                      ps12 , U2 q “ Fps2 , Sq
                                     pΣ1 , Σ2 q “ pHeapAfter ps1 q, HeapAfter ps2 qq
                                        Lalias “ tpℓ, Cq | Aliaspℓ, Σ1 , Σ2 q ^ pℓ, Cq P Uu
                                     pL1 , L2 q “ pU1 zU, U2 zUq
                                           w1 “ FoldOrderptfoldpℓq | pℓ, Cq P L1 Y Lalias u, Σq
                                           w2 “ FoldOrderptfoldpℓq | pℓ, Cq P L2 Y Lalias u, Σq


                          Fig. 21: Statement annotation insertion
                                                                                                 47




UnfoldListpx, Γ, Σ, Uq “ pU, L Y Uq
                 where U “ tunfoldpℓq | pℓ, Cq P LzUu
                          L “ tpℓ, Cq | ℓ P TypeLocspΓ, xq ^ pℓ ÞÑ y : Crτ sq P Σu



FoldList pΣ, Σ 1 , Uq “ pW, L X Uq
           where W “ FoldOrderptfoldpℓq | pℓ, Cq P L1 zLu, Σq
               pL, L1 q “ pWoundLocspΣq, WoundLocspΣ 1 qq



Aliaspℓ, Σ1 , Σ2 q “ ℓ ÞÑ x1 : x. . . f : τ1 . . .y P Σ1 ^ ℓ ÞÑ x2 : x. . . f : τ2 . . .y P Σ2
                       ^ |locspτ1 q Y locspτ2 q| ą 1



TypeLocspΓ, xq “ tlocspτ q | Γ $ x : τ u



WoundLocs pΣq “ tpℓ, Cq | ℓ ÞÑ x : Cr´s P Σu


PadLocspΣ, Σ 1 q “ tpadpℓq          mod ℓ P DompΣ 1 qzDompΣqu


                         Fig. 22: Annotation insertion helper functions
