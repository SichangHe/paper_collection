                                         First-Class Refinement Types for Scala
                                         MATT BOVEL✉ , EPFL, Switzerland
                                         VIKTOR KUNČAK, EPFL, Switzerland
                                         MARTIN ODERSKY, EPFL, Switzerland
                                         Refinement types—types qualified with logical predicates—have proven effective for lightweight verification
                                         in languages like Liquid Haskell, F*, and Dafny. However, in these systems refinements are either written in a
                                         separate specification language or treated as second-class annotations, disconnected from the host language’s
arXiv:2605.08369v2 [cs.PL] 25 Sep 2026




                                         type system. This disconnect creates usability barriers: programmers must maintain two mental models, and
                                         refinements cannot interact with features like type inference, subtyping, or overloading.
                                            We present the design of first-class refinement types for Scala 3, where refinements are ordinary types
                                         that participate in subtyping, inference, and pattern matching alongside existing language features. We prove
                                         type soundness of a core, pure calculus mechanized in Rocq, combining dependent function types, bounded
                                         polymorphism, positive equi-recursive types, union and intersection types, and refinement types, using a fuel-
                                         bounded definitional interpreter and semantic typing. A distinctive design choice is our partial-correctness
                                         semantics: predicates are arbitrary terms that may diverge, and type soundness requires no termination
                                         assumptions. Finally, we implement our design as a prototype extension of the Scala 3 compiler with a
                                         lightweight e-graph-based solver for predicate entailment.
                                         CCS Concepts: • Software and its engineering → Compilers; Formal software verification; Data types
                                         and structures; • Theory of computation → Type theory; Program semantics.
                                         Additional Key Words and Phrases: Refinement Types, Scala, Definitional Interpreter, Semantic Types, Rocq
                                         ACM Reference Format:
                                         Matt Bovel, Viktor Kunčak, and Martin Odersky. 2026. First-Class Refinement Types for Scala. Proc. ACM
                                         Program. Lang. 10, OOPSLA2, Article 409 (October 2026), 29 pages. https://doi.org/10.1145/3839541

                                         1   Introduction
                                         A refinement type restricts a base type to values satisfying a logical predicate. For example, the
                                         type {𝑥 : Int | 𝑥 > 0} denotes the positive integers. Logical refinements as subsets of values have a
                                         long history [20], going back at least to Cartwright [6]. Freeman and Pfenning [12] coined the term
                                         refinement types for a more restricted mechanism distinguishing subtypes of algebraic datatypes
                                         by constructor structure. Flanagan [11] returned to general predicate refinements, checking them
                                         statically when possible and dynamically otherwise (hybrid type checking). Rondon et al. [33] then
                                         made predicate refinements more practical with Liquid Types, which automatically infer refinements
                                         via predicate abstraction and discharge proof obligations with SMT solvers. Systems built on these
                                         ideas such as Liquid Haskell [44], F* [39], and Dafny [27] have since verified properties ranging from
                                         safe array indexing [33] to the functional correctness of production cryptographic libraries [50].
                                            The appeal of refinement types is that refinements are just types: they are checked statically,
                                         composed through ordinary type constructors, and propagated by standard typing rules. For
                                         instance, retrieving an element from a list of non-empty strings yields a non-empty string by
                                         Authors’ Contact Information: Matt Bovel, EPFL, Lausanne, Switzerland; Viktor Kunčak, EPFL, Lausanne, Switzerland;
                                         Martin Odersky, EPFL, Lausanne, Switzerland.




                                         This work is licensed under a Creative Commons Attribution 4.0 International License.
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM 2475-1421/2026/10-ART409
                                         https://doi.org/10.1145/3839541


                                                                  Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:2                                                                 Matt Bovel, Viktor Kunčak, and Martin Odersky


parametric polymorphism alone. More fundamentally, refinement types can be seen as [19] a
generalization of Floyd-Hoare logic in which invariants are attached to types rather than program
points, delegating abstraction and instantiation to the type system using subtyping and type
inference. In practice, programmers can specify and verify properties using the type system they
already know, with the same error messages, IDE support, and mental model.
   However, these benefits are often diminished because existing refinement type systems process
refinements in a separate phase, disconnected from the host language’s type checker. In Liquid
Haskell, for instance, refinements are written inside special comments and verified by an external
tool. Note how the type of x is declared twice in the following snippet: once as Int for the Haskell
type checker, and once as {v:Int | v mod 2 == 0} for Liquid Haskell:
{-@ x :: {v:Int | v mod 2 == 0 } @-}
let x = 42 :: Int in ...
As a result, refinement types are not “just types”: programmers must maintain two mental models,
one for the host type system and one for the refinement layer, with separate error messages, separate
IDE support, and limited ability to debug failures across the boundary. A recent usability study
by Gamboa et al. [14] confirms this: one participant observed that “comments are usually seen as
just optional information in the code and not something that is directly used by the compiler,” and
another remarked, “It’s sort of like you’re doing two things at once because you’re implementing
in Haskell. But you’re also talking to GHC, but you’re also talking to LiquidHaskell.”
   The consequences of this separation run deeper than usability. Because the refinement checker
operates after or alongside the host type checker, it must duplicate much of the host’s type infer-
ence machinery, an engineering burden that also limits expressiveness. Schmid and Kunčak [35]
implemented qualified types for an earlier version of the Scala compiler (Dotty) with a refinement
checker “largely independent of Scala’s own type checker.” This architecture meant refinement
types could not interact with Scala’s type inference (they could not be inferred as type arguments
in generic code) and required a separate qualifier inference algorithm that proved difficult to scale.
   Userland Scala libraries such as Iron [18] and Refined [41] take a different trade-off: they encode
refinement-like checks using opaque types and implicit evidence, benefiting from Scala’s own type
inference and tooling, but at the cost of expressiveness; refinement proofs are limited to what
Scala’s implicit resolution can discharge, ruling out dedicated efficient decision procedures for
equality, arithmetic, ordering, or other domain-specific theories.

1.1     First-class Refinement Types
We show that refinement types can be first-class types in a mainstream programming language.
Rather than adding a separate refinement layer, we extend the Scala 3 type checker itself so
that refinement types are ordinary Scala types, checked during the initial type-checking phase
and flowing naturally through subtyping and type inference. The Liquid Haskell example above
becomes:
val x: (Int with x % 2 == 0) = 42
Here, Int with x % 2 == 0 is a regular Scala type: it participates in subtyping, generics, pattern
matching, type bounds, overloading, and implicits, eliminating the two-mental-models problem.
There is one type system, one set of error messages, and one inference algorithm.
  Integrating refinement types into the host language’s type system is not entirely new: Dafny [27]
and F* [39] already treat refinement types as first-class citizens of their type checkers, and use
subtyping to relate a refinement type to its base type. However, these languages were designed from
the ground up around verification. To our knowledge, ours is the first integration of refinement

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                          409:3


types into a pre-existing language where subtyping is central and pervasive, relied upon by classes,
traits, mixin composition, path-dependent types, bounded polymorphism, overloading, and implicit
resolution, while preserving the type system’s existing behavior.
   As a concrete example, consider Scala’s bounded type polymorphism. In the snippet below,
the ordering is defined for Int only, yet maximum applied to even numbers should return Even;
this challenge motivated abstract refinements [43]. In our system, bounded polymorphism and
subtyping suffice: List(2, 4, 6) is typed as List[2 | 4 | 6], type inference instantiates T to Int,
whose Ordering instance performs the comparisons, and U to 2 | 4 | 6, and the result checks
against Even since each literal satisfies the predicate:

def maximum[T: Ordering, U <: T](xs: List[U]): U = xs.reduce(max)
type Even = {v: Int with v % 2 == 0}
def example1: Even = maximum(List(2, 4, 6))
                   Fig. 1. A refinement type interacting with bounded type polymorphism.

  As another example, consider overload resolution, a feature characteristic of object-oriented
languages. Below, we define two overloads of min: one for sorted lists and one for arbitrary lists.
Because refinement types participate in overload resolution, the compiler dispatches min(l) to the
more specific overload when l is known to be sorted:

def min(l: List[Int] with l.isSorted): Int = l.head // O(1)
def min(l: List[Int]): Int = l.min // O(n)
def example2(l: List[Int] with l.isSorted): Int = min(l) // calls the first overload
                               Fig. 2. Overload resolution with refinement types.

1.2   Contributions
These examples illustrate a broader point: when refinement types are first-class, they compose
freely with existing language features rather than requiring bespoke extensions for each interaction.
We demonstrate this idea end-to-end, through the following contributions:
  • We present the design of first-class refinement types in Scala 3: their syntax, semantics, and
    interaction with Scala’s existing type system, including subtyping, type inference, bounded poly-
    morphism, overloading, and implicits (§2). A distinctive design choice is a partial-correctness
    semantics for predicates: predicates are ordinary, possibly diverging pure terms whose meaning
    is defined operationally rather than by translation into a classical logic. A refinement holds if
    its predicate evaluates to true whenever it terminates (§2.3).
 • We prove type soundness of a core, pure calculus capturing the essential features of our design,
   mechanized in Rocq [40] (§3). The operational semantics is given by a fuel-bounded definitional
   interpreter, and soundness is established via semantic typing, where types are interpreted as
   predicates on values. To our knowledge, this is the first mechanized soundness proof that
   combines refinement types with union and intersection types, bounded polymorphism (with
   lower and upper bounds), and positive equi-recursive types, a combination needed to model
   Scala’s type system but not covered by prior mechanizations [3, 16, 38].
 • We describe a prototype implementation in the Scala 3 compiler (Dotty), showing that
   refinement types can be added to an industrial-strength compiler with modest changes to its
   architecture (§4). We also present a lightweight e-graph-based solver for predicate entailment
   and evaluate our system on a suite of benchmarks (§4.4).

                         Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:4                                                                 Matt Bovel, Viktor Kunčak, and Martin Odersky


2     Design
In this section, we present the syntax (§2.1), define the predicate language and its purity restrictions
(§2.2), discuss the partial-correctness semantics (§2.3), explain how expressions are given refinement
types through equality facts and selfification (§2.4), and describe run-time checks (§2.5).

2.1     Syntax
We illustrate the syntax with the classic length-indexed vectors (Figure 3).

type Vec[T]
object Vec:
  def fill[T](n: Int, v: T): {r: Vec[T] with r.len == n} = ???
extension [T](a: Vec[T])
  def len: Int = ???
  def concat(b: Vec[T]): {r: Vec[T] with r.len == a.len + b.len} = ???
  def zip[S](b: Vec[S] with b.len == a.len): {r: Vec[(T, S)] with r.len == a.len} = ???
def example3(n: Int, m: Int): {r: Vec[(String, Int)] with r.len == m + n} =
  val v1 = Vec.fill(n, 0)
  val v2 = Vec.fill(m, 1)
  val v3 = v1.concat(v2)
  val mPlusN = m + n // inferred as Int
  Vec.fill(mPlusN, "").zip(v3)
                            Fig. 3. Length-indexed vectors using refinement types.


  A refinement type has two syntactic forms: a long form with an explicit binder, and a short form
that reuses a name from context.
  Long form. The long form {x: T with p(x)} introduces an explicit binder x for the refined value.
This is necessary when no name is already available, such as the return type of fill in Figure 3.
The curly braces and explicit binder mirror set-builder notation and are visually consistent with
other brace-delimited constructs in Scala.
   Short form. When the refined value already has a name, as in a val or parameter declaration (as
for the b parameter of zip in Figure 3), the binder can be omitted. The short form T with p reuses
the enclosing binding’s name and desugars to the long form:
val x: (Int with x % 2 == 0) = 42
// desugars to:
val x: {v: Int with v % 2 == 0} = 42

    Grammar. Refinement types extend Scala’s type grammar [7, §13] with two productions:
Type                ::= ...
                      | InfixType `with' PostfixExpr         -- short form
SimpleType          ::= ...
                      | `{' id `:' InfixType `with' Expr `}' -- long form
  Notably, predicates reuse Scala’s existing expression syntax: they are syntactically ordinary
expressions, though subject to semantic restrictions (§2.2). The base type is an InfixType, which
excludes complex type forms such as match types without parentheses.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                                 409:5


2.2    Purity
Predicates are restricted to a pure fragment of Scala’s expression language: constants, stable iden-
tifiers (references to val bindings and parameters), field selections over val fields, term and type
applications, constructors of case classes without initializers, boolean connectives (&&, ||, !), com-
parison operators, and arithmetic. This is the subset of Scala formalized in §3; the implementation
checks that predicates stay within this fragment. Importantly, predicates may refer to free variables
from the enclosing scope, enabling dependent refinements such as the b.len == a.len predicate in
the zip signature of Figure 3.
   Predicates must be pure: deterministic and side-effect-free1 . For instance, a mutable variable cannot
appear in a predicate, and equality in predicates is structural, not referential:
var x = 3
val y: (Int with y == x) = 3 // rejected because x is mutable
class Box(val value: Int)
val b: (Box with b == Box(3)) = Box(3) // rejected because Box has reference equality
We do not currently enforce purity of called functions: our solver assumes all functions are pure, so
using an impure function in a predicate is a silent logical error. This unsafe default is a deliberate
choice to simplify gradual adoption without imposing a large upfront annotation burden.
   A concrete path toward enforcing purity is offered by capture checking [48], a new, experimental
extension of the Scala 3 compiler.2 It tracks capabilities: references that confer the authority to
perform effects, such as file-system or network access. The types of values and methods record
which capabilities they capture or use; a pure function is one that captures nothing. Three further
extensions—Stateful Capabilities, separation checking [49], and safe mode [29]—together extend
this accounting to mutable state: reads and writes are tracked as capability uses, written state is
exclusive and un-aliased, and escape hatches such as unchecked casts and reflection are closed, so
that no effect or mutation goes untracked.
   With these checks in place, purity checking of predicates reduces to a simple condition: reject
any predicate that references a capability, calls a method that uses one, or reads a mutable variable.
Weaker checks are also conceivable: tracking the read set of each predicate (the read-only capabilities
it uses) and invalidating established refinement facts whenever an element of that set is written to.
Separation checking would make such invalidation sound, as all writes are explicit and un-aliased.
Similar ideas underpin refinement type systems for Rust, where ownership likewise guarantees
exclusive access to written state (§5). We leave these integrations to future work.

2.3    Non-termination and Partial Correctness
Our system uses a partial-correctness semantics: a term e has type {x: T with p(x)} if, whenever e
terminates with a value v, the predicate p(v) holds. No termination guarantee is required for typing.
Formally, the term interpretation EJ𝐴K (§3.3) asserts that if a term evaluates to a value, that value
satisfies the type’s interpretation. This is a key difference from prior systems, designed around
termination: System FR [16] enforces total correctness and requires termination proofs for all
recursive functions, Liquid Haskell requires termination of functions reflected into refinements [44],
and F* [39] and Dafny [27] require specification-level computation to terminate.
   Since predicates are ordinary pure terms (§2.2), they may themselves diverge. The termination
requirements of the systems above stem from their reading of predicates as formulas in a classical
1We conjecture that determinism alone is sufficient for soundness: benign side effects (e.g., logging) that do not affect the

predicate’s return value would be harmless. We leave formalizing this conjecture to future work.
2 The extensions are described in the Scala 3 documentation: https://nightly.scala-lang.org/docs/reference/experimental/

capture-checking/.


                           Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:6                                                                 Matt Bovel, Viktor Kunčak, and Martin Odersky


logic, typically that of an SMT solver. We instead define their meaning operationally: {𝑥 : 𝐴 | 𝑝}
contains those values of 𝐴 for which 𝑝 evaluates to true whenever it terminates. This mirrors
the semantics of run-time assertions: evaluating 𝑝 as a dynamic check—as refinement patterns
and .runtimeChecked do in practice (§2.5)—signals a violation only if 𝑝 evaluates to false, so a
diverging check never fails. Type soundness thus requires no termination assumptions; termination
resurfaces only when justifying individual entailment rules. Crucially, a diverging predicate is
vacuously satisfied: it behaves like true, and can never be used to prove false.
   Termination considerations are confined to a single judgment: the semantic implication judgment
Γ ⊨ 𝑝 1 ⇒ 𝑝 2 (§3.3), which the subtyping rule S-Refine (§3.5) uses to compare the predicates of two
refinement types. It reads both sides partially: in every well-formed environment, if 𝑝 1 evaluates
to true whenever it terminates, then so does 𝑝 2 . Thus, no type checking rule needs to refer to
termination; it is only needed to justify individual entailment rules, and only some of them. Here
and below, a term terminates in a given environment if its evaluation produces a value. For example,
dropping a trivially true conjunct needs no termination:3
   Lemma 2.1 (And-True). ∀Γ, 𝑡 . Γ ⊨ (𝑡 && true) ⇒ 𝑡.
Other rules genuinely do:
   Lemma 2.2 (And-False). ∀Γ, 𝑡 . 𝑡 terminates =⇒ Γ ⊨ (𝑡 && false) ⇒ false.
The termination hypothesis is necessary: writing “diverge” for a closed term that never terminates,
we have ¬ (∅ ⊨ (diverge && false) ⇒ false), since the left-hand side diverges and is vacuously
satisfied while false is not. The fact that a “morally false” predicate can be vacuously satisfied
may look alarming, but it does not impact soundness: a diverging predicate is indistinguishable
from true, not from false, and true proves nothing. Writing <:> for mutual subtyping, we have:
   Lemma 2.3 (Diverging predicates are vacuous).
   (1) ∀Γ, 𝐴. Γ ⊨ {𝑥 : 𝐴 | diverge} <:> {𝑥 : 𝐴 | true} <:> 𝐴.
   (2) ∀Γ, 𝑡, 𝐴. 𝑡 terminates =⇒ ¬ (Γ ⊨ 𝑡 : {𝑥 : 𝐴 | false}).
   (3) ¬ (∅ ⊨ {𝑥 : Unit | diverge} <: {𝑥 : Unit | false}).
A diverging term, by contrast, can be given the type {𝑥 : Unit | false}: the partial-correctness
interpretation is vacuous for terms that never produce a value. This is not unsound: by Lemma 2.3(2),
no computation that actually completes has this type, so any code path that would exploit such a
“proof of false” must first force the diverging computation, and therefore never runs. Unsoundness
would arise only if the computation were erased at compile time, allowing code to assume the
predicate without running it.
   Because the type system is sound without any termination assumption, termination can be
handled permissively, as a solver concern rather than a typing one. We therefore give the implication
judgment a semantic definition only, and leave developing a syntactic proof system for predicate
entailment as future work. In practice, few entailment rules are termination-sensitive: within the
checked predicate fragment (§2.2), every construct except function calls trivially terminates, and
termination only matters for specific rules, such as the simplification of 𝑡 &&false to false above, or
the use of a predicate from a called function’s result type. Even with a termination checker in place,
proofs would be required only for the specific functions those rules touch—never systematically
for every function used in a predicate. We believe this matters for adoption: Scala is a general-
purpose language, and systematically requiring termination proofs would create a significant
barrier. For now, our solver (§4.3) simply assumes termination of the functions called in predicates,
3 The lemmas in this subsection are proved in our Rocq mechanization, in the file ExamplesPartialSoundness.v.



Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                          409:7


as it does purity—a deliberately permissive first approximation. Verifying the termination-sensitive
entailment rules and adding a termination checker are future work.

2.4   Mixed-precision Type Inference
The previous sections describe how refinement types are written and what they mean. This section
addresses how expressions actually receive refinement types during type checking. A key design
goal is backward compatibility: enabling refinement types should not change the inferred types of
existing code.
   Why not always infer precise types? A natural approach would be to infer refinement
types everywhere. For example, systematically give val x = 1 + 2 its most precise type
{v: Int with v == 1 + 2} rather than Int. This is impractical for three reasons.
   First, backward compatibility. In Scala, types are not only descriptive—they drive program
elaboration. Implicit resolution and overload resolution both depend on the inferred types of
arguments. A more precise type can change which implicit instances are found or introduce
ambiguities between overloaded methods, breaking code that previously compiled.
   Second, performance. Carrying precise types for every intermediate expression increases the size
of types, leading to higher memory usage and slower type comparisons.
   Third, usability. Overly detailed inferred types—such as deeply nested unions of singleton types—
are harder to read and understand than simple approximations like Int.
  Our solution: equality facts and selfification. Instead of always inferring precise types, we keep
Scala’s existing widening behavior and recover precision on demand through two mechanisms,
both standard in refinement type systems [3, 16, 38].
  The first mechanism is the equality fact context. The T-Let typing rule (Figure 9) records an
equality fact 𝑥 ∼ 𝑒 1 between each binding 𝑥 and its definition 𝑒 1 , where ∼ denotes that two terms
evaluate to the same value:
                         Γ ⊢ 𝑒 1 : 𝑇1   Γ, 𝑥 : 𝑇1, 𝑥 ∼ 𝑒 1 ⊢ 𝑒 2 : 𝑇2
                                                                       (T-Let)
                           Γ ⊢ let 𝑥 = 𝑒 1 in 𝑒 2 : avoid(𝑇2, 𝑥)
The binding val mPlusN = m + n in Figure 3 is inferred as Int, but the equality mPlusN ∼ m + n is
recorded in the context. When mPlusN is later used where a refined type is expected, the system
can substitute m + n for mPlusN in predicates and verify the obligation. avoid is described in §3.4.
   The second mechanism is selfification (T-Self in Figure 9). When checking an expres-
sion e of type T against a refinement type, the compiler assigns it the self-referencing type
{x: T with x == e}, provided e is a valid predicate term. This lifts expressions into types on
demand without changing inference for unannotated code.

2.5   Run-time Checks
Refinement predicates are checked statically by default, but when the compiler cannot verify a
predicate, two run-time mechanisms are available.
  Pattern matching. A refinement type can be used as a pattern, branching on whether a value
satisfies the predicate at run time [2]:
type ID = {s: String with s.matches(idRegex)}

"a2e7-e89b" match
  case id: ID => ... // predicate holds, id has type ID
  case _      => ... // predicate does not hold

                         Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:8                                                                 Matt Bovel, Viktor Kunčak, and Martin Odersky


This integrates naturally with Scala’s existing pattern-matching infrastructure. Since Scala compiles
to the JVM, which erases type parameters at run time, matching against parameterized refinement
types such as List[ID] is not directly supported, though straightforward workarounds exist (e.g.,
filtering a collection with the dedicated method).

   Checked casts. When the programmer expects a predicate to hold but the solver cannot prove it
statically, .runtimeChecked [36] performs a dynamic check and throws an exception on failure:

val id: ID = "a2e7-e89b".runtimeChecked
// desugars to:
val id: ID =
  if ("a2e7-e89b".matches(idRegex)) "a2e7-e89b".asInstanceOf[ID]
  else throw new IllegalArgumentException()

As with other Scala types, .asInstanceOf can also be used directly to skip the check entirely, at
the programmer’s risk. Note that pattern matching on refinement types and .runtimeChecked only
works for first-order predicates that can be evaluated directly; higher-order values such as functions
cannot be checked eagerly, sidestepping the blame assignment problem [21] for now.

3     Metatheory
We prove type soundness for a core calculus that captures the essential features of our design. The
calculus extends System 𝐹 <:> (System 𝐹 <: [5] extended with lower bounds on type variables [1])
with booleans, ints, dependent function types, dependent pairs (sigma types), sum types, union and
intersection types, refinement types, loops, and positive equi-recursive types. The mechanization
is carried out in Rocq [40] using a fuel-bounded definitional interpreter [1] for the operational
semantics, and semantic typing [42] to prove type safety.
   To illustrate the scope of the calculus, Figure 4 shows a Scala function that collects elements
satisfying a predicate into a refined list, alongside its encoding in the core calculus. The function
exercises bounded polymorphism (𝑆 >: 𝑇 ), higher-order predicates (𝑝), refinement types (List [{𝑣 :
𝑇 | 𝑝 (𝑣)}]), equi-recursive types (the list itself, encoded as 𝜇𝑋 . Unit + (𝑇 × 𝑋 )), and tail-recursive
iteration (encoded as loop). The mechanization includes this encoding. Running it through the
interpreter for example verifies that applying it to [3, −1, 4, −1, 5] with 𝜆𝑥 . 𝑥 > 0 yields [3, 4, 5].

3.1     Language
The abstract syntax is given in Figure 5. Types and terms are mutually inductive, since refinement
types {𝑥 : 𝐴 | 𝑝} embed a term 𝑝 as a predicate.

  Naming convention. The mechanization uses de Bruijn indices throughout. For readability, the
paper presentation uses named variables and omits explicit shifts; all rules should be read modulo
𝛼-equivalence.

   Terms. Bounded type abstractions Λ(𝑋 :>𝐿<:𝑈 ). 𝑏 carry both a lower bound 𝐿 and an upper
bound 𝑈 , as in 𝐹 <:> , to model Scala’s bounded polymorphism.
   loop(𝑎) 𝑥 . 𝑏 is a limited form of general recursion that suffices to express tail recursion: the
initial state 𝑎 is bound to 𝑥 in the body 𝑏, which returns inl(𝑣 1 ) to continue with a new state, or
inr(𝑣) to exit with result 𝑣.
   Integer arithmetic uses signed 32-bit wrapping semantics (Int32) rather than mathematical
integers; this matches Scala’s runtime model and could in the future serve as a foundation for
proving the solver’s normalization rules correct. It otherwise has no impact on the formalization.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                          409:9

Scala source                                               Core calculus encoding

enum List[T]:                                              List [𝑇 ] ≜ 𝜇𝑋 . Unit + (𝑇 , 𝑋 )
  case Nil()
  case Cons(head: T, tail: List[T])
                                                           Λ(𝑇 :> ⊥ <: ⊤). Λ(𝑆 :> 𝑇 <: ⊤).
@tailrec def collect[T, S >: T](                             𝜆xs:List [𝑇 ].
  xs: List[T],                                               𝜆𝑝:(𝑆 → Bool).
                                                             𝜆acc:List [{𝑣 : 𝑇 | 𝑝 (𝑣)}].
  p: S => Boolean,
                                                               loop((xs, acc)) state.
  acc: List[{v: T with p(v)}]
                                                                  match state with (rem, cacc) ⇒
): List[{v: T with p(v)}] =                                          match rem with
  xs match                                                              inl(_) ⇒ inr(cacc)
    case Nil() => acc                                                | inr(𝑐) ⇒
    case Cons(x, xs1) =>                                                match 𝑐 with (hd, tl) ⇒
      if p(x)                                                               if 𝑝 hd
      then collect(xs1, p, Cons(x, acc))                                    then inl((tl, inr((hd, cacc))))
      else collect(xs1, p, acc)                                             else inl((tl, cacc))


Fig. 4. A collect function in Scala (left) and its encoding in the core calculus (right). The tail-recursive
loop becomes a loop combinator whose body returns inl(state′ ) to continue or inr(result) to break. Lists are
equi-recursive: inl(unit) represents the empty list and inr((hd, tl)) a cons cell.


  Values. As in other definitional interpreter developments [1, 31], values are distinct from terms:
while term lambdas 𝜆𝑥:𝐴. 𝑏 may have free variables, value closures ⟨𝜌, 𝜆𝑥 . 𝑏⟩ capture their envi-
ronment 𝜌 as a list of values. This separation reflects the big-step evaluation strategy: evaluation
produces values with closed environments, not terms.
  Types. The type language includes dependent function types Π𝑥:𝐴. 𝐵, dependent pairs Σ𝑥:𝐴. 𝐵,
bounded universal types ∀(𝑋 :>𝐿<:𝑈 ). 𝐴, sum types, union and intersection types, and refinement
types {𝑥 : 𝐴 | 𝑝} where the predicate 𝑝 is an arbitrary term. Refinement types can be nested, as in
the implementation.
  The base types include singleton types True and False rather than a single Bool because
this enables defining the refinement type interpretation succinctly: a value satisfies {𝑥 : 𝐴 | 𝑝}
when it belongs to VJ𝐴K and 𝑝 evaluates to true, which is exactly membership in EJTrueK. The
conventional Bool is recovered as True ∨ False.
  The type 𝜇𝑋 . 𝐴 denotes an equi-recursive type, interpreted as the intersection of all step-indexed
approximations (see §3.3). Unlike iso-recursive systems, no explicit fold/unfold terms are needed;
instead, the equivalence 𝜇𝑋 . 𝐴  𝐴[𝑋 ↦→ 𝜇𝑋 . 𝐴] is established via subtyping rules (§3.5).
   Contexts. A typing context Γ (Figure 5) contains three kinds of entries: term bindings 𝑥 : 𝐴,
type variable bounds 𝑋 :> 𝐿 <: 𝑈 , and equality facts 𝑎 1 ∼ 𝑎 2 . Equality facts record that two
terms evaluate to the same value. They are introduced by T-Let, which records that a let-bound
variable equals its definition, and by T-If, which records that the condition equals true or false in
the respective branches. These facts are used during subtyping to justify predicate entailment.

3.2   Operational Semantics
The rules for successful evaluation 𝜌 ⊢ 𝑎 ⇓ 𝑣 are given in Figure 6. Closures capture the environ-
ment at the point of creation: evaluating 𝜆𝑥:𝐴. 𝑏 under 𝜌 yields ⟨𝜌, 𝜆𝑥 . 𝑏⟩. Application evaluates the

                         Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:10                                                                   Matt Bovel, Viktor Kunčak, and Martin Odersky




                                                                     𝑣 :=                                         Value
          𝑐 := unit | true | false | 𝑧 ∈ Z Constant                          𝑐                                 constant
         op := == | != | < | <= | >= | >   Operation                         (𝑣 1, 𝑣 2 )                            pair
                 && | || | + | - | * | / | %                                 inl(𝑣)                        left injection
𝑎, 𝑏, 𝑓 , 𝑝 :=                                           Term                inr(𝑣)                    right injection
                 𝑐                                     constant              ⟨𝜌, 𝜆𝑥 . 𝑏⟩                         closure
                 𝑥                                     variable              ⟨𝜌, Λ𝑋 . 𝑏⟩                   type closure
                 𝜆𝑥:𝐴. 𝑏                            abstraction
                                                                   𝐴, 𝐵 :=                                        Type
                 𝑓 𝑎                                application
                                                                             𝑋                                  variable
                 Λ(𝑋 :>𝐿<:𝑈 ). 𝑏               type abstraction
                                                                             Unit | True | False | Int32     base types
                 𝑓 [𝐴]                         type application
                                                                             ⊤                                       top
                 let 𝑥:𝐴 = 𝑎 in 𝑏                            let
                                                                             ⊥                                   bottom
                 (𝑎 1, 𝑎 2 )                               pair
                                                                             Π𝑥:𝐴. 𝐵              dependent function
                                                    match pair
                                                                             ∀(𝑋 :>𝐿<:𝑈 ). 𝐴                 bounded ∀
                 match 𝑎 with (𝑥, 𝑦) ⇒ 𝑏
                                                                             Σ𝑥:𝐴. 𝐵                  dependent pair
                                                    match sum
                                                                             𝐴+𝐵                                    sum
                 match 𝑎 with inl(𝑥) ⇒ 𝑏𝑙 | inr(𝑦) ⇒ 𝑏𝑟
                                                                             {𝑥 : 𝐴 | 𝑝}                    refinement
                 inl[𝐴] 𝑎                         left injection             𝐴∨𝐵                                  union
                 inr[𝐴] 𝑎                        right injection             𝐴∧𝐵                            intersection
                 𝑎 op 𝑏                        binary operation              𝜇𝑋 . 𝐴                           recursive
                 if 𝑎 then 𝑏 1 else 𝑏 2             conditional
                                                                     Γ :=                                      Context
                 loop(𝑎) 𝑥 . 𝑏                             loop
                                                                             ∅                                    empty
         𝜌 :=                                   Environment                  Γ, 𝑥 : 𝐴                      term binding
                 ∅                                       empty               Γ, 𝑋 :> 𝐿 <: 𝑈           type var. bound
                 𝜌, 𝑥 ↦→ 𝑣                             binding               Γ, 𝑎 1 ∼ 𝑎 2                  equality fact
Fig. 5. Abstract syntax of the core calculus. Types and terms are mutually inductive; bindings use de Bruijn
indices.


function and argument, then evaluates the body in the closure’s environment extended with the argu-
ment. In rule E-BinOp, primitive operations are interpreted by the partial function evalop(op, 𝑣 𝑎 , 𝑣𝑏 )
(eval_bin_op in the mechanization), which is undefined for ill-typed combinations of operands,
making such applications stuck.
   Erased semantics. Types are erased at runtime, so they have no operational semantics. This is
reflected in the evaluation rules for type abstractions and applications, which simply ignore the
type arguments. This matches Scala’s runtime model, where types are erased on the JVM.
  Definitional interpreter. In the mechanization, evaluation is implemented as a fuel-bounded
definitional interpreter (Figure 7), following Amin and Rompf [1]. The interpreter is a recursive
Rocq function that returns a layered option type: None for timeout (fuel exhausted), Some None
for a stuck state, or Some (Some v) for successful evaluation to a value 𝑣. We write 𝜌 ⊢ 𝑎 ⇓? 𝑟

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                                       409:11


Big-step evaluation rules                                                                                                𝜌 ⊢𝑎⇓𝑣

                 𝜌 ⊢𝑐 ⇓𝑐                              (E-Const)                𝜌 ⊢ 𝑎 ⇓ 𝑣𝑎       𝜌 ⊢ 𝑏 ⇓ 𝑣𝑏
                                                                                 evalop(op, 𝑣 𝑎 , 𝑣𝑏 ) = 𝑟
                                                                                                                         (E-BinOp)
                𝑥 ↦→ 𝑣 ∈ 𝜌                                                            𝜌 ⊢ 𝑎 op 𝑏 ⇓ 𝑟
                                                           (E-Var)
                 𝜌 ⊢𝑥 ⇓𝑣
                                                                             𝜌 ⊢ 𝑎 ⇓ true         𝜌 ⊢ 𝑏1 ⇓ 𝑣
                                                                                                                        (E-IfTrue)
                                                                              𝜌 ⊢ if 𝑎 then 𝑏 1 else 𝑏 2 ⇓ 𝑣
        𝜌 ⊢ 𝜆𝑥:𝐴. 𝑏 ⇓ ⟨𝜌, 𝜆𝑥 . 𝑏⟩                          (E-Abs)
                                                                             𝜌 ⊢ 𝑎 ⇓ false         𝜌 ⊢ 𝑏2 ⇓ 𝑣
   𝜌 ⊢ Λ(𝑋 :>𝐿<:𝑈 ). 𝑏 ⇓ ⟨𝜌, Λ𝑋 . 𝑏⟩                      (E-TAbs)                                                      (E-IfFalse)
                                                                              𝜌 ⊢ if 𝑎 then 𝑏 1 else 𝑏 2 ⇓ 𝑣

         𝜌 ⊢ 𝑓 ⇓ ⟨𝜌 𝑓 , 𝜆𝑥 . 𝑏⟩                                                           𝜌 ⊢𝑎⇓𝑣
  𝜌 ⊢ 𝑎 ⇓ 𝑣𝑎     𝜌 𝑓 , 𝑥 ↦→𝑣 𝑎 ⊢ 𝑏 ⇓ 𝑣                                                                                      (E-Inl)
                                                           (E-App)                𝜌 ⊢ inl[𝐵] 𝑎 ⇓ inl(𝑣)
                𝜌 ⊢ 𝑓 𝑎⇓𝑣
                                                                                          𝜌 ⊢𝑎⇓𝑣
                                                                                                                            (E-Inr)
 𝜌 ⊢ 𝑓 ⇓ ⟨𝜌 𝑓 , Λ𝑋 . 𝑏⟩          𝜌𝑓 ⊢ 𝑏 ⇓ 𝑣                                       𝜌 ⊢ inr[𝐴] 𝑎 ⇓ inr(𝑣)
                                                          (E-TApp)
              𝜌 ⊢ 𝑓 [𝐴] ⇓ 𝑣
                                                                                         𝜌 ⊢ 𝑎 ⇓ 𝑣0
                                                                                  𝜌, 𝑥 ↦→ 𝑣 0 ⊢ 𝑏 ⇓ inr(𝑣)
   𝜌 ⊢ 𝑎 ⇓ 𝑣𝑎         𝜌, 𝑥 ↦→ 𝑣 𝑎 ⊢ 𝑏 ⇓ 𝑣                                                                             (E-LoopExit)
                                                           (E-Let)                𝜌 ⊢ loop(𝑎) 𝑥 . 𝑏 ⇓ 𝑣
       𝜌 ⊢ let 𝑥:𝐴 = 𝑎 in 𝑏 ⇓ 𝑣
                                                                        𝜌 ⊢ 𝑎 ⇓ 𝑣0     𝜌, 𝑥 ↦→ 𝑣 0 ⊢ 𝑏 ⇓ inl(𝑣 1 )
     𝜌 ⊢ 𝑎1 ⇓ 𝑣 1          𝜌 ⊢ 𝑎2 ⇓ 𝑣 2                                         𝜌 ⊢ loop(𝑣 1 ) 𝑥 . 𝑏 ⇓ 𝑣
                                                          (E-Pair)                                                   (E-LoopCont)
         𝜌 ⊢ (𝑎 1, 𝑎 2 ) ⇓ (𝑣 1, 𝑣 2 )                                            𝜌 ⊢ loop(𝑎) 𝑥 . 𝑏 ⇓ 𝑣

                                𝜌 ⊢ 𝑎 ⇓ (𝑣 1, 𝑣 2 )       𝜌, 𝑥 ↦→ 𝑣 1, 𝑦 ↦→ 𝑣 2 ⊢ 𝑏 ⇓ 𝑣
                                                                                                                     (E-MatchPair)
                                          𝜌 ⊢ match 𝑎 with (𝑥, 𝑦) ⇒ 𝑏 ⇓ 𝑣

                                         𝜌 ⊢ 𝑎 ⇓ inl(𝑣)      𝜌, 𝑥 ↦→ 𝑣 ⊢ 𝑏𝑙 ⇓ 𝑤
                                                                                                                 (E-MatchSumL)
                            𝜌 ⊢ match 𝑎 with inl(𝑥) ⇒ 𝑏𝑙 | inr(𝑦) ⇒ 𝑏𝑟 ⇓ 𝑤

                                     𝜌 ⊢ 𝑎 ⇓ inr(𝑣)          𝜌, 𝑦 ↦→ 𝑣 ⊢ 𝑏𝑟 ⇓ 𝑤
                                                                                                                 (E-MatchSumR)
                            𝜌 ⊢ match 𝑎 with inl(𝑥) ⇒ 𝑏𝑙 | inr(𝑦) ⇒ 𝑏𝑟 ⇓ 𝑤

     Fig. 6. Successful evaluation rules (𝜌 ⊢ 𝑎 ⇓ 𝑣), derived from the definitional interpreter (Figure 7).


when evaluation terminates with result Some 𝑟 (either stuck or a value), and 𝜌 ⊢ 𝑎 ⇓ 𝑣 for the
special case where 𝑟 = Some 𝑣. The big-step rules in Figure 6 show only successful evaluation; the
mechanization accounts for all three outcomes, as shown in Figure 7.
   Fuel bounds depth, not steps. The fuel parameter bounds the depth of evaluation, not the total
number of steps. When evaluating an application, for example, the argument, the function, and the
body are all evaluated with the same, decremented fuel. This follows Amin and Rompf [1], but differs
from approaches that decrement fuel at every reduction step [31, 32]: for an application 𝑓 𝑎, those
approaches partition the available fuel across the sub-evaluations (fuel 𝑓 + fuel𝑎 + fuel𝑏𝑜𝑑𝑦 ≈ fuel),
whereas ours passes the same decremented fuel to each (fuel 𝑓 = fuel𝑎 = fuel𝑏𝑜𝑑 𝑦 = fuel − 1). The
advantage is simplicity: depth-bounded fuel gives a natural termination measure for structural
induction. The disadvantage is that it does not provide a global step count that can be correlated

                              Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:12                                                                Matt Bovel, Viktor Kunčak, and Martin Odersky


Definitional interpreter (excerpt)                                                                    eval 𝑛 𝜌 𝑎

          Fixpoint eval (fuel: nat) (env: list Value) (t: Term)
              : option (option Value) :=
            match fuel with
            | 0 => None (* timeout *)
            | S fuel' =>
              match t with
              | tabs _ b => Some (Some (vabs env b))
              | tapp f a =>
                  match eval fuel' env f with
                  | None => None
                  | Some (Some (vabs envf b)) =>
                      match eval fuel' env a with
                      | Some (Some va) => eval fuel' (va :: envf) b
                      | o => o (* propagate timeout or stuck *)
                      end
                  | _ => Some None (* stuck *)
                  end
            ...
            end.

Termination                                                                                            𝜌 ⊢ 𝑎 ⇓? 𝑟


                                     𝜌 ⊢ 𝑎 ⇓? 𝑟 ≜ ∃𝑛. eval 𝑛 𝜌 𝑎 = Some 𝑟

Successful evaluation                                                                                   𝜌 ⊢𝑎⇓𝑣


                                           𝜌 ⊢ 𝑎 ⇓ 𝑣 ≜ 𝜌 ⊢ 𝑎 ⇓? Some 𝑣


Fig. 7. Fuel-bounded definitional interpreter, following Amin and Rompf [1]. The interpreter returns None
(timeout), Some None (stuck), or Some (Some 𝑣) (success).


with recursive-type unfoldings, a technique commonly used to prove soundness of equi-recursive
types via step-indexed logical relations [42]. We side-step this limitation by making our value
interpretation step-index-free (§3.3).

3.3      Interpretation
The semantic framework is given in Figure 8. We describe each component below.
  Value interpretation. The semantic approach to type soundness represents types as predicates
                                                                                       𝜌
on values: a semantic type is a function Value → Prop. The value interpretation VJ𝐴K𝛿 maps a
syntactic type 𝐴 to a semantic type, parameterized by a type variable assignment 𝛿 (mapping type
variables to semantic types) and a term variable assignment 𝜌 (mapping term variables to values).
The type variable assignment enables the interpretation of polymorphic types; the term variable
assignment enables the interpretation of dependent types and refinement predicates. Using an

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                        409:13


explicit term variable assignment rather than a closing substitution is less standard, but is a natural
fit for our environment-passing definitional interpreter.
   Base types are interpreted as expected: VJUnitK accepts only unit, VJTrueK and VJFalseK
accept the corresponding boolean values, and VJInt32K accepts any integer literal. A value satisfies
a function type Π𝑥:𝐴. 𝐵 if it is a closure ⟨𝜌 𝑓 , 𝜆𝑥 . 𝑏⟩ such that for every argument 𝑣 𝑎 satisfying
VJ𝐴K, the body 𝑏 evaluated in the closure’s environment 𝜌 𝑓 extended with 𝑣 𝑎 satisfies EJ𝐵K. Note
that the body is evaluated in the closure’s captured environment, not the caller’s. A refinement
type {𝑥 : 𝐴 | 𝑝} conjoins membership in VJ𝐴K with the predicate 𝑝 belonging to EJTrueK—
i.e., evaluating to true whenever it terminates. Union and intersection types are interpreted as
set-theoretic union and intersection, respectively.
   The recursive type 𝜇𝑋 . 𝐴 is interpreted as the intersection of all finite approximations ∀𝑛. 𝐹 𝑛 (𝑣),
                                         𝜌
where 𝐹 0 (𝑣) = ⊤ and 𝐹 𝑛+1 (𝑣) = VJ𝐴K𝛿 [𝑋 ↦→𝐹 𝑛 ] (𝑣). Intuitively, 𝐹 𝑛 captures the behavior of 𝜇𝑋 . 𝐴
up to 𝑛 unfoldings. A value inhabits the recursive type only if it satisfies all approximations. This
interpretation is step-index-free in the sense that the final semantic type VJ𝜇𝑋 . 𝐴K universally
quantifies over all approximation levels 𝑛, so it does not depend on any external step counter. The
step indexing is confined to the internal construction of the approximation sequence.
                                                             𝜌
   Term interpretation. The term interpretation EJ𝐴K𝛿 (𝑎) lifts the value interpretation to a predicate
on terms. As described in §2.3, a term 𝑎 has type 𝐴 if, whenever evaluation of 𝑎 terminates with
                                                                        𝜌
a result 𝑟 (i.e., 𝜌 ⊢ 𝑎 ⇓? 𝑟 ), then 𝑟 must be a value 𝑣 satisfying VJ𝐴K𝛿 . This rules out stuck states:
if evaluation completes, it must produce a well-typed value. The statement is vacuously true for
diverging terms, making this a partial correctness property.

   Context well-formedness. The well-formedness predicate wf (𝛿, Γ, 𝜌) requires that the assign-
ments 𝛿 and 𝜌 are consistent with the context Γ. Concretely, it requires three conditions: (1) for
every term binding 𝑥 : 𝐴 in Γ, the value 𝜌 (𝑥) satisfies VJ𝐴K𝛿 ; (2) for every type variable bound
                                                                𝜌

𝑋 :> 𝐿 <: 𝑈 in Γ, the semantic type 𝛿 (𝑋 ) lies between VJ𝐿K and VJ𝑈 K; and (3) for every equality
fact 𝑎 1 ∼ 𝑎 2 in Γ, there exists a value 𝑣 such that both 𝑎 1 and 𝑎 2 evaluate to 𝑣. Condition (3) is
slightly simplified here: in the mechanization, each side of a fact carries a depth tag recording
how many bindings were in scope when the fact was introduced, and the term is evaluated in the
corresponding suffix of the environment. The simpler statement using the full environment can
be recovered up to captured environments in closures: evaluating a term in a longer environment
produces the same result, except that closures capture the environment available at their creation
point. This is the same subtlety addressed by the evaluation weakening lemma (Lemma 3.7).

  Semantic typing. The semantic typing judgment Γ ⊨ 𝑎 : 𝐴 universally quantifies over all type
variable assignments 𝛿 and term variable assignments 𝜌 that are well-formed with respect to Γ,
                      𝜌
and requires that EJ𝐴K𝛿 (𝑎) holds. In other words, in any environment consistent with the context,
whenever evaluation of 𝑎 terminates, the result is a value satisfying the type’s interpretation.

   Semantic subtyping. The semantic subtyping judgment Γ ⊨ 𝐴 <: 𝐵 similarly quantifies over all
                                               𝜌         𝜌
well-formed assignments and requires VJ𝐴K𝛿 ⊆ VJ𝐵K𝛿 , where semantic type inclusion 𝑆 1 ⊆ 𝑆 2 is
defined as pointwise implication: ∀𝑣. 𝑆 1 (𝑣) =⇒ 𝑆 2 (𝑣). In other words, every value that satisfies 𝐴
also satisfies 𝐵.

  Semantic implication. The semantic implication judgment Γ ⊨ 𝑝 1 ⇒ 𝑝 2 requires that, in any
well-formed environment, if 𝑝 1 evaluates to true (i.e., EJTrueK(𝑝 1 ) holds), then so does 𝑝 2 . This
judgment is used in the refinement subtyping rule S-Refine to compare predicates.

                         Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:14                                                                 Matt Bovel, Viktor Kunčak, and Martin Odersky

                                                                                                                      𝜌
Value interpretation                                                                                           VJ𝐴K𝛿 (𝑣)
                         𝜌
                   VJ𝑋 K𝛿 (𝑣) ≜ 𝛿 (𝑋 )(𝑣)
               VJUnitK𝛿 (𝑣) ≜ 𝑣 = unit
                         𝜌


               VJTrueK𝛿 (𝑣) ≜ 𝑣 = true
                         𝜌


              VJFalseK𝛿 (𝑣) ≜ 𝑣 = false
                         𝜌

                         𝜌
              VJInt32K𝛿 (𝑣) ≜ ∃𝑧. 𝑣 = 𝑧
                         𝜌
                   VJ⊤K𝛿 (𝑣) ≜ ⊤
                         𝜌
                   VJ⊥K𝛿 (𝑣) ≜ ⊥
                         𝜌                                               𝜌                  𝜌 [𝑥↦→𝑣𝑎 ]
            VJΠ𝑥:𝐴. 𝐵K𝛿 (𝑣) ≜ ∃𝜌 𝑓 , 𝑏. 𝑣 = ⟨𝜌 𝑓 , 𝜆𝑥 . 𝑏⟩ ∧ ∀𝑣 𝑎 . VJ𝐴K𝛿 (𝑣 𝑎 ) =⇒ EJ𝐵K𝛿 𝑓              (𝑏)
                                                                                                 𝜌𝑓
    VJ∀(𝑋 :>𝐿<:𝑈 ). 𝐵K𝛿 (𝑣) ≜ ∃𝜌 𝑓 , 𝑏. 𝑣 = ⟨𝜌 𝑓 , Λ𝑋 . 𝑏⟩ ∧ ∀𝑆. VJ𝐿K𝛿 ⊆ 𝑆 ⊆ VJ𝑈 K𝛿 =⇒ EJ𝐵K𝛿 [𝑋
                      𝜌                                                 𝜌                𝜌
                                                                                                    ↦→𝑆 ]
                                                                                                          (𝑏)
                      𝜌                                          𝜌           𝜌 [𝑥↦→𝑣1 ]
          VJΣ𝑥:𝐴. 𝐵K𝛿 (𝑣) ≜ ∃𝑣 1, 𝑣 2 . 𝑣 = (𝑣 1, 𝑣 2 ) ∧ VJ𝐴K𝛿 (𝑣 1 ) ∧ VJ𝐵K𝛿          (𝑣 2 )
                      𝜌                                       𝜌                                𝜌
            VJ𝐴 + 𝐵K𝛿 (𝑣) ≜ (∃𝑤 . 𝑣 = inl(𝑤) ∧ VJ𝐴K𝛿 (𝑤)) ∨ (∃𝑤 . 𝑣 = inr(𝑤) ∧ VJ𝐵K𝛿 (𝑤))
                      𝜌               𝜌                   𝜌 [𝑥↦→𝑣 ]
       VJ{𝑥 : 𝐴 | 𝑝}K𝛿 (𝑣) ≜ VJ𝐴K𝛿 (𝑣) ∧ EJTrueK𝛿                   (𝑝)
                      𝜌               𝜌                 𝜌
            VJ𝐴 ∨ 𝐵K𝛿 (𝑣) ≜ VJ𝐴K𝛿 (𝑣) ∨ VJ𝐵K𝛿 (𝑣)
                      𝜌               𝜌                 𝜌
            VJ𝐴 ∧ 𝐵K𝛿 (𝑣) ≜ VJ𝐴K𝛿 (𝑣) ∧ VJ𝐵K𝛿 (𝑣)
                      𝜌                                                              𝜌
            VJ𝜇𝑋 . 𝐴K𝛿 (𝑣) ≜ ∀𝑛. 𝐹 𝑛 (𝑣) where 𝐹 0 (𝑣) = ⊤, 𝐹 𝑛+1 (𝑣) = VJ𝐴K𝛿 [𝑋 ↦→𝐹 𝑛 ] (𝑣)

                                                                                                                      𝜌
Term interpretation                                                                                            EJ𝐴K𝛿 (𝑎)

                          EJ𝐴K𝛿 (𝑎) ≜ ∀𝑟 . 𝜌 ⊢ 𝑎 ⇓? 𝑟 =⇒ ∃𝑣. 𝑟 = Some 𝑣 ∧ VJ𝐴K𝛿 (𝑣)
                               𝜌                                                        𝜌


Context well-formedness                                                                                        wf (𝛿, Γ, 𝜌)

                          wf (𝛿, Γ, 𝜌) ≜ ∀(𝑥 : 𝐴) ∈ Γ. VJ𝐴K𝛿 (𝜌 (𝑥))
                                                               𝜌

                                         ∧ ∀(𝑋 :>𝐿<:𝑈 ) ∈ Γ. VJ𝐿K𝛿 ⊆ 𝛿 (𝑋 ) ⊆ VJ𝑈 K𝛿
                                                                      𝜌                     𝜌

                                         ∧ ∀(𝑎 1 ∼ 𝑎 2 ) ∈ Γ. ∃𝑣. 𝜌 ⊢ 𝑎 1 ⇓ 𝑣 ∧ 𝜌 ⊢ 𝑎 2 ⇓ 𝑣

Semantic typing                                                                                                  Γ⊨𝑎:𝐴
                                   Γ ⊨ 𝑎 : 𝐴 ≜ ∀𝛿, 𝜌. wf (𝛿, Γ, 𝜌) =⇒
                                                                             𝜌
                                                                         EJ𝐴K𝛿 (𝑎)

Semantic subtyping                                                                                             Γ ⊨ 𝐴 <: 𝐵
                             Γ ⊨ 𝐴 <: 𝐵 ≜ ∀𝛿, 𝜌. wf (𝛿, Γ, 𝜌) =⇒
                                                                          𝜌       𝜌
                                                                      VJ𝐴K𝛿 ⊆ VJ𝐵K𝛿

Semantic implication                                                                                       Γ ⊨ 𝑝1 ⇒ 𝑝2

                   Γ ⊨ 𝑝 1 ⇒ 𝑝 2 ≜ ∀𝛿, 𝜌. wf (𝛿, Γ, 𝜌) =⇒
                                                                    𝜌                       𝜌
                                                             EJTrueK𝛿 (𝑝 1 )   =⇒    EJTrueK𝛿 (𝑝 2 )

Semantic type inclusion                                                                                           𝑆1 ⊆ 𝑆2
                                          𝑆 1 ⊆ 𝑆 2 ≜ ∀𝑣. 𝑆 1 (𝑣) =⇒ 𝑆 2 (𝑣)


Fig. 8. Semantic framework. The value interpretation VJ·K maps syntactic types to predicates on values. The
term interpretation EJ·K lifts this to a partial correctness assertion on terms. Semantic typing and subtyping
quantify over all well-formed environments.



Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                        409:15


3.4   Typing
The semantic typing judgment Γ ⊨ 𝑎 : 𝐴 (Figure 8) requires that, in any well-formed environment,
EJ𝐴K holds for 𝑎—i.e., whenever evaluation terminates, the result is a value in VJ𝐴K. The typing
rules in Figure 9 are proven sound with respect to this judgment. Each rule corresponds to a proven
lemma. Noteworthy rules include:
 • T-Let records the equality 𝑥 ∼ 𝑎 in the context, enabling the body to use facts about the bound
   variable’s value. The result type uses avoid(𝐵, 𝑥) to remove references to the bound variable,
   which goes out of scope.
 • T-Self (selfification) refines a first-order value to a singleton type {𝑥 : 𝐴 | 𝑥 == 𝑎}. The
   firstorder(𝐴) check ensures that 𝐴 is a type for which equality comparison is defined—concretely,
   Unit, True, False, Int32, or a refinement of one of these. Functions, closures, and polymorphic
   values are excluded because they do not support runtime equality.
 • T-If adds equality facts 𝑎 ∼ true and 𝑎 ∼ false in the respective branches, and returns a union
   type 𝐵 1 ∨ 𝐵 2 of the two branches’ types.
 • T-Loop types a loop whose body returns 𝐴 + 𝐵: inl continues with a new accumulator of type 𝐴,
   inr exits with a result of type 𝐵. This rule allows recursion without typing a self-reference,
   avoiding the need for step-indexed reasoning that would typically be required for a general
   fixpoint combinator.

   ANF restriction. Several typing rules require certain subterms to be variables rather than arbitrary
expressions. In T-App, the argument must be a variable 𝑦, so that the substitution 𝐵 [𝑥 ↦→ 𝑦] in
the result type remains a syntactic type (substituting an arbitrary term could produce a type
containing a non-variable subterm, complicating the interpretation). Similarly, T-Pair requires the
first component to be a variable. This administrative normal form (ANF) restriction does not reduce
expressiveness: any argument expression can be let-bound first, with the let-bound variable used
as the argument. This is exactly what the implementation does via skolems (§4.2), which hoist
arguments to local bindings so that dependent result types can refer to them by name.

   Avoidance. The avoid(𝐴, 𝑥) operation removes occurrences of a bound variable 𝑥 from a type 𝐴,
producing a well-scoped result type. It traverses the type structurally, guided by a polarity flag that
flips at contravariant positions (the domain of Π and the upper bound of ∀). When a refinement
predicate mentions 𝑥, it is replaced by true in positive polarity (yielding a supertype) or false in
negative polarity (yielding a subtype). For recursive types 𝜇𝑌 . 𝐵, avoidance recurses into the body
only when spos(𝑌 , 𝐵) holds; otherwise it falls back to ⊤ or ⊥. The soundness of this operation is
established in Lemma 3.8.

3.5   Subtyping
The semantic subtyping judgment Γ ⊨ 𝐴 <: 𝐵 (Figure 8) requires that, in any well-formed en-
vironment, VJ𝐴K ⊆ VJ𝐵K. The subtyping rules in Figure 10 are proven sound with respect to
this judgment. Function types are contravariant in their domain and covariant in their codomain
(S-Fun); bounded universal types are covariant in the lower bound, contravariant in the upper
bound, and covariant in the body (S-Forall). Refinement types support two rules: S-RefineBase
drops the predicate (every refined type is a subtype of its base), and S-Refine compares both base
types and predicates, using the semantic implication judgment Γ ⊨ 𝑝 1 ⇒ 𝑝 2 to establish that the
predicate of the subtype entails the predicate of the supertype.
   The equi-recursive rules S-Mu-Fold and S-Mu-Unfold establish the isomorphism 𝜇𝑋 . 𝐴 
𝐴[𝑋 ↦→ 𝜇𝑋 . 𝐴], requiring that 𝑋 appears only in strictly positive positions in 𝐴, as defined by the

                         Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:16                                                                         Matt Bovel, Viktor Kunčak, and Martin Odersky


Semantic typing rules                                                                                               Γ⊨𝑎:𝐴

              Γ ⊨ unit : Unit                          (T-Unit)         Γ ⊨𝑦 :𝐴         Γ ⊨ 𝑎 2 : 𝐵 [𝑥 ↦→𝑦]
                                                                                                                      (T-Pair)
                                                                               Γ ⊨ (𝑦, 𝑎 2 ) : Σ𝑥:𝐴. 𝐵
              Γ ⊨ true : True                          (T-True)
                                                                             Γ⊨𝑎:𝐴     Γ ⊨𝑏 :𝐴
             Γ ⊨ false : False                        (T-False)                compat(op, 𝐴)
                                                                                                                    (T-BinOp)
                                                                            Γ ⊨ 𝑎 op 𝑏 : result(op, 𝐴)
               Γ ⊨ 𝑧 : Int32                             (T-Int)
                                                                              Γ ⊨ 𝑎 : True ∨ False
                 𝑥 :𝐴∈Γ                                                        Γ, 𝑎 ∼ true ⊨ 𝑏 1 : 𝐵 1
                                                         (T-Var)
                  Γ⊨𝑥 :𝐴                                                      Γ, 𝑎 ∼ false ⊨ 𝑏 2 : 𝐵 2
                                                                                                                        (T-If)
                                                                       Γ ⊨ if 𝑎 then 𝑏 1 else 𝑏 2 : 𝐵 1 ∨ 𝐵 2
               Γ, 𝑥 : 𝐴 ⊨ 𝑏 : 𝐵
                                                        (T-Abs)
           Γ ⊨ 𝜆𝑥:𝐴. 𝑏 : Π𝑥:𝐴. 𝐵                                                     Γ⊨𝑎:𝐴
                                                                                                                       (T-Inl)
                                                                               Γ ⊨ inl[𝐵] 𝑎 : 𝐴 + 𝐵
      Γ ⊨ 𝑓 : Π𝑥:𝐴. 𝐵         Γ ⊨𝑦 :𝐴
                                                        (T-App)
             Γ ⊨ 𝑓 𝑦 : 𝐵 [𝑥 ↦→𝑦]                                                     Γ⊨𝑎:𝐵
                                                                                                                       (T-Inr)
                                                                               Γ ⊨ inr[𝐴] 𝑎 : 𝐴 + 𝐵
           Γ, 𝑋 :> 𝐿 <: 𝑈 ⊨ 𝑏 : 𝐵
                                                       (T-TAbs)
Γ ⊨ Λ(𝑋 :>𝐿<:𝑈 ). 𝑏 : ∀(𝑋 :>𝐿<:𝑈 ). 𝐵                                  Γ⊨𝑎:𝐴           Γ, 𝑥 : 𝐴 ⊨ 𝑏 : 𝐴 + 𝐵
                                                                                                                     (T-Loop)
                                                                               Γ ⊨ loop(𝑎) 𝑥 . 𝑏 : 𝐵
           Γ ⊨ 𝑓 : ∀(𝑋 :>𝐿<:𝑈 ). 𝐵
         Γ ⊨ 𝐿 <: 𝐴      Γ ⊨ 𝐴 <: 𝑈                                        Γ⊨𝑎:𝐴          firstorder(𝐴)
                                                       (T-TApp)                                                       (T-Self)
           Γ ⊨ 𝑓 [𝐴] : 𝐵 [𝑋 ↦→𝐴]                                             Γ ⊨ 𝑎 : {𝑥 : 𝐴 | 𝑥 == 𝑎}

 Γ⊨𝑎:𝐴             Γ, 𝑥 : 𝐴, 𝑥 ∼ 𝑎 ⊨ 𝑏 : 𝐵                                  Γ⊨𝑎:𝐴           Γ ⊨ 𝐴 <: 𝐵
                                                         (T-Let)                                                      (T-Sub)
  Γ ⊨ let 𝑥:𝐴 = 𝑎 in 𝑏 : avoid(𝐵, 𝑥)                                                 Γ⊨𝑎:𝐵

                                   Γ ⊨ 𝑎 : Σ𝑥:𝐴. 𝐵        Γ, 𝑥 : 𝐴, 𝑦 : 𝐵 ⊨ 𝑏 : 𝐶
                                                                                                                (T-MatchPair)
                           Γ ⊨ match 𝑎 with (𝑥, 𝑦) ⇒ 𝑏 : avoid(avoid(𝐶, 𝑦), 𝑥)

         Γ ⊨ 𝑎 : 𝐴1 + 𝐴2          Γ, 𝑥 : 𝐴1, 𝑎 ∼ inl(𝑥) ⊨ 𝑏 1 : 𝐵 1     Γ, 𝑦 : 𝐴2, 𝑎 ∼ inr(𝑦) ⊨ 𝑏 2 : 𝐵 2
                                                                                                                (T-MatchSum)
             Γ ⊨ match 𝑎 with inl(𝑥) ⇒ 𝑏 1 | inr(𝑦) ⇒ 𝑏 2 : avoid(𝐵 1, 𝑥) ∨ avoid(𝐵 2, 𝑦)

          Fig. 9. Typing rules. All rules are proven sound with respect to the semantic typing judgment.



predicate spos(𝑋, 𝐴) (Figure 11). Strict positivity means 𝑋 never appears to the left of a function
arrow or in the bounds of a universal type. For union types, spos requires 𝑋 to be entirely absent;
this stronger condition is needed for a distributing lemma used in the fold/unfold proofs. Nested
recursive types 𝜇𝑌 . 𝐵 require both spos(𝑌 , 𝐵) and 𝑋 ∉ 𝐵: the latter prevents the outer variable from
leaking into the inner fixpoint’s approximation sequence.

3.6      Soundness and Main Lemmas
Each typing rule in Figure 9 and each subtyping rule in Figure 10 is individually proven sound
as a lemma about the semantic judgments Γ ⊨ 𝑎 : 𝐴 and Γ ⊨ 𝐴 <: 𝐵. Since these semantic
judgments directly assert that well-typed terms do not get stuck and that subtyping preserves value

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                               409:17


Semantic subtyping rules                                                                                        Γ ⊨ 𝐴 <: 𝐵

                Γ ⊨ 𝐴 <: 𝐴                         (S-Refl)                   Γ ⊨ 𝐴 ∧ 𝐵 <: 𝐵                      (S-AndR)

      Γ ⊨ 𝐴 <: 𝐵       Γ ⊨ 𝐵 <: 𝐶                                       Γ ⊨ 𝐶 <: 𝐴        Γ ⊨ 𝐶 <: 𝐵
                                                 (S-Trans)                                                         (S-And)
                Γ ⊨ 𝐴 <: 𝐶                                                    Γ ⊨ 𝐶 <: 𝐴 ∧ 𝐵

                Γ ⊨ 𝐴 <: ⊤                          (S-Top)                Γ ⊨ {𝑥 : 𝐴 | 𝑝} <: 𝐴             (S-RefineBase)
                Γ ⊨ ⊥ <: 𝐴                          (S-Bot)
                                                                    Γ ⊨ 𝐴 <: 𝐵       Γ, 𝑥 : 𝐴 ⊨ 𝑝 1 ⇒ 𝑝 2
                                                                                                                 (S-Refine)
Γ ⊨ 𝐵 1 <: 𝐴1       Γ, 𝑥 : 𝐴1 ⊨ 𝐴2 <: 𝐵 2                            Γ ⊨ {𝑥 : 𝐴 | 𝑝 1 } <: {𝑥 : 𝐵 | 𝑝 2 }
                                                    (S-Fun)
     Γ ⊨ Π𝑥:𝐴1 . 𝐴2 <: Π𝑥:𝐵 1 . 𝐵 2
                                                                             𝑋 :> 𝐿 <: 𝑈 ∈ Γ
                                                                                                            (S-TVar-Upper)
Γ ⊨ 𝐴1 <: 𝐵 1       Γ, 𝑥 : 𝐴1 ⊨ 𝐴2 <: 𝐵 2                                        Γ ⊨ 𝑋 <: 𝑈
                                                 (S-Sigma)
      Γ ⊨ Σ𝑥:𝐴1 . 𝐴2 <: Σ𝑥:𝐵 1 . 𝐵 2
                                                                             𝑋 :> 𝐿 <: 𝑈 ∈ Γ
            Γ ⊨ 𝐴 <: 𝐴 ∨ 𝐵                          (S-OrL)                      Γ ⊨ 𝐿 <: 𝑋
                                                                                                            (S-TVar-Lower)

            Γ ⊨ 𝐵 <: 𝐴 ∨ 𝐵                         (S-OrR)
                                                                                 spos(𝑋, 𝐴)
                                                                                                            (S-Mu-Unfold)
      Γ ⊨ 𝐴 <: 𝐶       Γ ⊨ 𝐵 <: 𝐶                                      Γ ⊨ 𝜇𝑋 . 𝐴 <: 𝐴[𝑋 ↦→ 𝜇𝑋 . 𝐴]
                                                        (S-Or)
            Γ ⊨ 𝐴 ∨ 𝐵 <: 𝐶
                                                                                 spos(𝑋, 𝐴)
                                                                                                               (S-Mu-Fold)
            Γ ⊨ 𝐴 ∧ 𝐵 <: 𝐴                        (S-AndL)             Γ ⊨ 𝐴[𝑋 ↦→ 𝜇𝑋 . 𝐴] <: 𝜇𝑋 . 𝐴

                   Γ ⊨ 𝐿1 <: 𝐿2        Γ ⊨ 𝑈 2 <: 𝑈 1       Γ, 𝑋 :> 𝐿2 <: 𝑈 2 ⊨ 𝐴 <: 𝐵
                                                                                                                 (S-Forall)
                              Γ ⊨ ∀(𝑋 :>𝐿1 <:𝑈 1 ). 𝐴 <: ∀(𝑋 :>𝐿2 <:𝑈 2 ). 𝐵

  Fig. 10. Subtyping rules. All rules are proven sound with respect to the semantic subtyping judgment.

Strict positivity                                                                                               spos(𝑋, 𝐴)

                                       spos(𝑋, 𝐴) ≜ True         if 𝐴 is a base type or type variable
                               spos(𝑋, Π𝑥:𝐴. 𝐵) ≜ 𝑋 ∉ 𝐴 ∧ spos(𝑋, 𝐵)
                      spos(𝑋, ∀(𝑌 :>𝐿<:𝑈 ). 𝐵) ≜ 𝑋 ∉ 𝐿 ∧ 𝑋 ∉ 𝑈 ∧ spos(𝑋, 𝐵)
                                  spos(𝑋, 𝜇𝑌 . 𝐴) ≜ spos(𝑌, 𝐴) ∧ 𝑋 ∉ 𝐴
                                spos(𝑋, Σ𝑥:𝐴. 𝐵) ≜ spos(𝑋, 𝐴) ∧ spos(𝑋, 𝐵)
                                  spos(𝑋, 𝐴 + 𝐵) ≜ spos(𝑋, 𝐴) ∧ spos(𝑋, 𝐵)
                             spos(𝑋, {𝑥 : 𝐴 | 𝑝}) ≜ spos(𝑋, 𝐴)
                                  spos(𝑋, 𝐴 ∨ 𝐵) ≜ 𝑋 ∉ 𝐴 ∧ 𝑋 ∉ 𝐵
                                  spos(𝑋, 𝐴 ∧ 𝐵) ≜ spos(𝑋, 𝐴) ∧ spos(𝑋, 𝐵)


Fig. 11. Strict positivity. spos(𝑋, 𝐴) holds when 𝑋 appears only in strictly positive positions in 𝐴: never to
the left of a function arrow, and never in the bounds of a universal type. Union types require 𝑋 to be entirely
absent (needed for the distributing lemma).


membership, any derivation composed from these rules inherits the safety guarantee. This is the
fundamental theorem of the logical relation.

                          Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:18                                                                    Matt Bovel, Viktor Kunčak, and Martin Odersky


  Adequacy. To provide a conventional syntactic interface, we also define inductive syntactic
typing and subtyping judgments that mirror the semantic rules of Figures 9 and 10. The adequacy
theorems show that these syntactic judgments imply their semantic counterparts. The proofs
proceed by straightforward induction on the derivation, applying the corresponding semantic
lemma at each constructor.
   Theorem 3.1 (Adeqacy of typing). If Γ ⊢ 𝑎 : 𝐴 then Γ ⊨ 𝑎 : 𝐴.
   Theorem 3.2 (Adeqacy of subtyping). If Γ ⊢ 𝐴 <: 𝐵 then Γ ⊨ 𝐴 <: 𝐵.
Note that the semantic implication judgment Γ ⊨ 𝑝 1 ⇒ 𝑝 2 has no syntactic counterpart: we do not
define inference rules for it. Instead, it remains an entirely semantic notion, used directly in the
subtyping rule S-Refine. This reflects the design of the implementation, where predicate entailment
is delegated to the solver (§4.3) rather than derived from syntactic rules. Syntactic entailment rules
could nonetheless be proved sound against the semantic judgment, just as the typing and subtyping
rules are; Lemmas 2.1 and 2.2 (§2.3) exemplify this, showing that some rules hold unconditionally
while others require termination assumptions.
   This separation between syntactic and semantic judgments allows us to state and use typing
rules in the familiar inductive style, while the soundness guarantee flows from the semantic
interpretation.
   Weakening and substitution for the interpretation. The semantic typing and subtyping proofs
require that the value interpretation is well-behaved under changes to the environment. The key
lemmas establish that the interpretation depends only on the variables the type mentions: extending
the environment with a fresh binding leaves it unchanged, and a variable can be substituted away
when the environment determines its value. We write FV(𝐴) for the free (term and type) variables
of 𝐴.4
                                                                            𝜌             𝜌 [𝑥↦→𝑣 ]
   Lemma 3.3 (Term weakening). If 𝑥 ∉ FV(𝐴), then VJ𝐴K𝛿 = VJ𝐴K𝛿                                       .
                                                                            𝜌 [𝑥↦→𝑣 ]                     𝜌
   Lemma 3.4 (Term substitution). If 𝜌 (𝑦) = 𝑣, then VJ𝐴K𝛿                              = VJ𝐴[𝑥 ↦→𝑦]K𝛿 .
                                                                           𝜌              𝜌
   Lemma 3.5 (Type weakening). If 𝑋 ∉ FV(𝐴), then VJ𝐴K𝛿 = VJ𝐴K𝛿 [𝑋 ↦→𝑆 ] .
                                                      𝜌                                       𝜌
   Lemma 3.6 (Type substitution). VJ𝐵K𝛿 [𝑋 ↦→ V J𝐴K𝜌 ] = VJ𝐵 [𝑋 ↦→𝐴]K𝛿
                                                                   𝛿

The mechanization proves more general versions for multi-element extensions, from which these
are derived. These lemmas are used pervasively—for instance, term substitution is needed for T-App
and T-Let, and type substitution for T-TApp and S-Mu-Fold/S-Mu-Unfold.
  Weakening and substitution for evaluation. The interpretation lemmas above reduce questions
about the semantic types to questions about evaluation under modified environments. These in
turn require corresponding lemmas about the evaluator. The difficulty is that evaluation results are
not preserved exactly: when the environment is extended, closures capture the larger environment,
producing structurally different values. To handle this, we define a compatibility relation 𝑟 1 ≈ 𝑟 2 on
results that relates first-order values to themselves and closures to closures with correspondingly
extended captured environments. The evaluation weakening lemmas then take the following
simulation-style form:

4 The mechanization states these lemmas in de Bruijn form, where extending the environment corresponds to an explicit

index shift on the type and the freshness side conditions are implicit.


Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                        409:19


  Lemma 3.7 (Evaluation weakening). Suppose 𝑥 ∉ FV(𝑎). If 𝜌 ⊢ 𝑎 ⇓? 𝑟 , then there exists 𝑟 ′ ≈ 𝑟
such that 𝜌 [𝑥 ↦→ 𝑣] ⊢ 𝑎 ⇓? 𝑟 ′ . Conversely, if 𝜌 [𝑥 ↦→ 𝑣] ⊢ 𝑎 ⇓? 𝑟 , then there exists 𝑟 ′ ≈ 𝑟 such that
𝜌 ⊢ 𝑎 ⇓? 𝑟 ′ .
This simulation-style argument is needed because the definitional interpreter uses closures rather
than substitution: evaluating a lambda under a longer environment produces a closure capturing
that longer environment. Analogous lemmas handle term substitution, with a corresponding
substitution compatibility relation.
   Avoidance. The avoid operation (§3.4) must preserve the subtyping relationship in the appropriate
direction. The key lemma establishes this for both polarities simultaneously:
    Lemma 3.8 (Avoidance soundness). For all 𝑣:
    (1) VJ𝐴K𝛿 (𝑣) =⇒ VJavoid(𝐴, 𝑥) + K𝛿 (𝑣) (positive: supertype)
            𝜌                         𝜌

    (2) VJavoid(𝐴, 𝑥) − K𝛿 (𝑣) =⇒ VJ𝐴K𝛿 (𝑣) (negative: subtype)
                         𝜌            𝜌


These are proven together by induction on 𝐴, flipping polarity at contravariant positions. The
avoid(𝐵, 𝑥) appearing in the typing rules (e.g., T-Let) uses positive polarity, avoid(𝐵, 𝑥) + , producing
a supertype of 𝐵.
   Positivity and fold/unfold. The fold and unfold rules for 𝜇𝑋 . 𝐴 require showing that the interpre-
tation of the recursive type coincides with its one-step unfolding: VJ𝜇𝑋 . 𝐴K = VJ𝐴[𝑋 ↦→ 𝜇𝑋 . 𝐴]K.
The key ingredients, adapted from Hamza et al. [16], are:
    Lemma 3.9 (Monotonicity). If spos(𝑋, 𝐴) and 𝑆 1 ⊆ 𝑆 2 , then VJ𝐴K𝛿 [𝑋 ↦→𝑆1 ] ⊆ VJ𝐴K𝛿 [𝑋 ↦→𝑆2 ] .
  Lemma 3.10 (Distribution). Let 𝑆 ∩ = 𝜆𝑤 . ∀𝑛. 𝑆𝑛 (𝑤). If spos(𝑋, 𝐴) and ∀𝑛. VJ𝐴K𝛿 [𝑋 ↦→𝑆𝑛 ] (𝑣),
then VJ𝐴K𝛿 [𝑋 ↦→𝑆∩ ] (𝑣).
Monotonicity says that the interpretation of a strictly positive type is monotone in the type
variable’s denotation. Distribution says that an intersection over a family of denotations can
be pushed inside the interpretation. Together, these establish that the approximation sequence
𝐹 0 ⊇ 𝐹 1 ⊇ · · · converges to a fixpoint, so ∀𝑛. 𝐹 𝑛 (𝑣) is equivalent to 𝐹 (𝜆𝑤 . ∀𝑛. 𝐹 𝑛 (𝑤)) (𝑣), which is
exactly VJ𝐴[𝑋 ↦→ 𝜇𝑋 . 𝐴]K(𝑣).

4     Implementation
We implement the design of §2 as a prototype extension of Dotty, the production Scala 3 compiler.
This section describes how refinement types integrate into the existing compiler architecture (§4.1),
how argument hoisting and skolems recover the ANF discipline assumed by the formalization
(§4.2), and the lightweight e-graph-based solver that discharges predicate entailment obligations
(§4.3). We evaluate compilation overhead on a suite of benchmarks in §4.4.

4.1    Integration
We implement refinement types in Dotty, the production Scala 3 compiler. The resulting change is
small. The bulk of the new code lives in a self-contained package and accounts for approximately
2 200 new lines, of which about 600 are for the solver (§4.3). Changes to existing compiler code are
limited to about 300 net lines. The main integration points are:
  • Type representation. Dotty provides a mechanism for defining custom types via type annotations,
    supporting arbitrary internal representations. We leverage this to attach predicates to types.
    These predicates are represented using a lightweight expression IR that captures only the subset
    of Scala expressions valid as predicates (§2.2). Crucially, the leaf nodes of this IR are Scala’s

                         Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:20                                                                Matt Bovel, Viktor Kunčak, and Martin Odersky


      existing path-dependent types, so the compiler’s existing substitution and dependent-type
      machinery is reused automatically.
 • Parsing. The parser is extended with the two grammar productions presented in §2.1.
 • Subtyping. A single case is added to the type comparer, corresponding to S-Refine (Figure 10):
   when the supertype is {𝑥 : 𝐴 | 𝑝}, the comparer checks <: 𝐴 and delegates predicate entailment
   to the solver (§4.3).
 • Adaptation. Dotty’s bidirectional type checker has a single point where a synthesized type is
   reconciled with an expected type. This point gains one new case: when the expected type is a
   refinement type, it attempts selfification (§2.4), wrapping the expression in {𝑥 : 𝑇 | 𝑥 == 𝑒}.
 • Branch and case facts. The typer records branch conditions (if) and pattern-match outcomes
   in the context, and propagates them to the solver. Unlike the formalization, which also stores
   equality facts for val bindings in the typing context (T-Let in Figure 9), the implementation
   does not need to: the compiler already links each symbol to its definition tree, so the solver can
   follow references in a predicate and recover definitions on demand, gathering only the facts
   relevant to the predicate being checked.
 • Argument hoisting. When a method signature contains refinement types that refer to other
   parameters, the corresponding arguments are lifted to local val bindings (§4.2). This is needed
   so that run-time checks can refer to the argument without re-evaluating it.
 • Recursive signatures. When a return type’s predicate refers to the method itself, the compiler
   pre-installs a provisional type without the qualifier to break the cyclic reference.
 • Run-time checks. The type-test lowering phase compiles pattern matches against {𝑥 : 𝐴 | 𝑝}
   into a type test against 𝐴 followed by a run-time evaluation of 𝑝 [2, 36].

4.2      Hoisting and Skolems
In the formalization (§3), T-App (Figure 9) requires the argument to be a variable 𝑦, so that the
return type 𝐵 [𝑥 ↦→ 𝑦] is a simple substitution of one variable for another. In practice, Scala allows
arbitrary expressions as arguments, so the implementation must recover this structure on demand
through two mechanisms.
   Argument hoisting. Consider a method def f(x: Int, y: {v: Int with v > x}): Unit. When
called as f(impure(), 3.runtimeChecked), the run-time check for the second argument must evalu-
ate impure() > 3—but impure() may have side effects and must not be evaluated twice. The compiler
detects that x is referenced from a qualifier in another parameter’s type and lifts the argument to a
local binding. This transformation is triggered whenever a parameter is referenced from a qualifier
in another parameter’s type or in the return type.
   Skolems as on-the-fly ANF. How to apply a dependent method f: (x: A) => B to an arbitrary
expression e? We cannot blindly substitute, because the return type 𝐵 [𝑥 ↦→ 𝑒] may not be defined
if e is outside of the predicate language fragment. This is a well-known problem in refinement
type systems. Borkowski et al. [3] solve it with term-level existential types, giving f(e) the type
∃𝑥 . 𝐴 ∧ 𝐵 [𝑥] (following Knowles and Flanagan [11]); Hamza et al. [16] use a “let-in-type” construct
let 𝑥 = 𝑒 in 𝐵.
   Our formalization takes a simpler route: T-App requires the argument to be a variable, which
is always valid in a predicate. In the implementation, we achieve the same effect using skolems:
special terms in predicates that refer to specific but unknown values. Each non-variable argument
is assigned a unique skolem ?k. The return type of f(e) is formed by substituting ?k for x in B. If e
happens to live in the supported fragment, an equality ?k == e is added to the equality context.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                        409:21


   For example, assume a case class Range(from: Int, until: Int) whose constructor returns the
selfified type {r: Range | r == Range(from, until)}. When Range(0, 10) appears as a receiver
(say, in Range(0, 10).foreach(...)), it is assigned a fresh skolem ?1, and foreach yields elements
of type {x: Int | ?1.from <= x && x < ?1.until}. The solver then gets ?1 == Range(0, 10) as an
assumption, allowing it to unfold ?1.from to 0 and ?1.until to 10, recovering the bounds needed
to verify body expressions like a(i).
   In effect, the skolem plays the role of the let-bound variable in the formalization: it names the
argument value, and the equality assumption carries the necessary fact. Like let bindings in the
formalization, skolems are removed from result types via the avoid operation (§3.4) when they
would escape their scope.

4.3   Solver
Rather than depending on an external SMT solver—which would add platform-specific binaries
and a large unowned dependency to the compiler—we built a self-contained solver (≈600 lines)
based on e-graphs, lightweight enough to run on every keystroke in an IDE.
  The solver decides predicate entailment 𝑃1 ⇒ 𝑃2 , with top-level case splitting for disjunctive
assumptions. It collects all relevant facts—qualifier predicates, val equalities, and branch conditions—
inserts them into an e-graph merged with true, and checks whether 𝑃 2 becomes equivalent to
true.

   Acyclic e-graph. Our e-graph implementation is similar to the acyclic e-graphs used in the Cranelift
compiler [9] and described by Zucker [51]: each equivalence class eagerly collapses to a single
canonical representative, rather than maintaining the set of all equivalent terms as in standard
e-graphs [47]. When two nodes are merged, an order function picks the representative (preferring
constants, then operations, then constructor applications, then lambdas), and all parent nodes are
re-canonicalized. This may trigger further merges—for example, merging 𝑥 ≡ 3 causes 𝑥 + 𝑦 to
re-canonicalize to 3 + 𝑦, which may match an existing node and cascade into another merge. This
repair loop is the core of congruence closure [28].
  Normalization. During canonicalization, the e-graph applies domain-specific rewrites:
 • Arithmetic. Integer sums and products are flattened using associativity, like-terms are grouped
   and constant-folded (2𝑥 + 3𝑥 → 5𝑥). Subtraction is rewritten to addition of a negated product
   (𝑎 − 𝑏 → 𝑎 + (−1) · 𝑏). Distribution is not applied, to avoid exponential blowup.
 • Boolean logic. Conjunction and disjunction short-circuit when one operand is a constant. Double
   negation is eliminated. When a conjunction is merged with true, each conjunct is individually
   merged with true; dually for disjunction and false. When an equality 𝑎 == 𝑏 is merged with
   true, the nodes 𝑎 and 𝑏 are themselves merged.
 • Beta reduction. Applying a lambda to arguments substitutes and re-canonicalizes.
 • Constructor–field reduction. Selecting a field from a constructor application returns the corre-
   sponding argument (Range(0, 10).from → 0). This is the mechanism that unfolds skolems in
   the Range example of §4.2.
 • Transitivity of <. When 𝑎 < 𝑏 becomes true, the solver derives 𝑎 < 𝑐 for all known 𝑐 with 𝑏 < 𝑐,
   and symmetrically for lower bounds.
  Binding. E-graph nodes may contain lambdas (for predicates passed to higher-order functions).
We represent bound variables with de Bruijn indices. When checking 𝑃1 ⇒ 𝑃2 , both predicates
are opened by substituting their outermost bound variable with a fresh free variable, akin to the
opening operation in locally-nameless representations. This is sound because bound variables are

                         Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:22                                                                Matt Bovel, Viktor Kunčak, and Martin Odersky


never merged with any other node—they remain fully abstract, only equal to themselves. Only
the opened free variable participates in merges. This approach avoids the complexity of slotted
e-graphs [37], which parameterize e-classes by their free variables to support full equality saturation
with binders—a generality we do not need.

   Trade-offs. This design is strictly more powerful than substitution alone: congruence closure
propagates equalities through containing expressions, and cascading repair discovers multi-step
simplifications that no single substitution pass would find. It is intentionally less complete than full
equality saturation [47]: the order function picks one representative per class, so if two equivalent
forms of a subexpression would trigger different simplifications, only one is explored. We believe
this is an acceptable trade-off for a type checker, where predictable performance matters more than
completeness.

4.4      Evaluation
We evaluate our implementation along two axes: compilation time overhead and expressiveness
compared to two existing systems for Scala—Schmid and Kunčak’s previous prototype [35] and the
Stainless verifier [16]. Stainless is not a refinement type system; it checks pre- and postconditions.
It is, however, the de facto tool for verifying Scala programs, even for lightweight properties that
refinement types could cover. This makes it a natural point of comparison for our system, on the
programs that both systems can verify.

   Compilation overhead. We measure single-shot compilation time on a suite of small benchmark
programs, comparing each system against its own baseline: the same programs without refinement
annotations, compiled with checking disabled. Where possible, we port the same program to
Schmid’s system and to Stainless. Baselines are per-system because the systems build on different
compiler versions and the ported programs differ slightly in code shape. Benchmarks run under JMH;
each benchmark is compiled with 150 single-shot warm-up iterations followed by 20 measurement
iterations, and the whole experiment is repeated in 10 independent runs. Each run is reduced
to the mean of its measurement iterations; Table 1 reports the mean of the per-run means with
95% confidence intervals (Student’s 𝑡), and the overhead Δ as the difference between checked and
baseline times.
   On our benchmarks, our system (labelled “First-class” in the table) adds modest overhead: 0–12%
of the baseline compilation time. This is consistently less than the two other systems: on the
benchmarks they support, Schmid’s system adds 20–38% and Stainless at least 56%.
   To gauge overhead on a realistic codebase, we applied our system to Fansi [17], a 1 000-line
terminal-color library. The only change was replacing three run-time require checks in a color-index
function with a refinement type alias:

type ChannelValue = {v: Int with 0 <= v && v < 256}
def trueIndex(r: ChannelValue, g: ChannelValue, b: ChannelValue)

All call sites already guard the arguments with the same bounds, so the refinement is verified
statically with no other code changes. The compilation time difference is within measurement
noise, confirming that the overhead is proportional to the number of refinement checks, not to the
size of the program. This experiment also illustrates a key advantage of first-class integration: our
system compiles unmodified Scala code without restriction, so refinement types can be introduced
incrementally into an existing codebase. By contrast, Stainless is limited to a specific fragment of
Scala and fails on code that falls outside its supported subset.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                           409:23


Table 1. Compilation time benchmarks (ms/op, single-shot). Each run (JMH fork) is reduced to its mean;
scores are the mean of the per-run means ± the 95% confidence interval across runs (Student’s 𝑡). Each
platform shows the unchecked baseline time and the absolute overhead of checking; the checked
                                                                                          √           time is
base + Δ. Since the baseline and checked samples are independent, the overhead interval is 𝑒𝑏2 + 𝑒𝑐2 , where
𝑒𝑏 and 𝑒𝑐 are the baseline and checked intervals.

                                 First-class                    Schmid                     Stainless
         Benchmark       LoC    Base (ms)      Δ (ms)   LoC   Base (ms)   Δ (ms)   LoC   Base (ms)     Δ (ms)
         arrfold          20       94 ± 1       3±2      20      88 ± 2   30 ± 2    —           —           —
         collect          15      103 ± 2       4±3      —           —        —     —           —           —
         fansi           530      187 ± 3      −1 ± 3    —           —        —     —           —           —
         fibMemo          15      104 ± 1       7±2      —           —        —     —           —           —
         hof1              5       75 ± 2       3±2       5      77 ± 1   18 ± 1    —           —           —
         hof2              8       77 ± 1       2±1       8      77 ± 1   20 ± 1    —           —           —
         intarray         11       94 ± 1       3±1      11      75 ± 1   19 ± 2    14      68 ± 1      45 ± 2
         list1             5       95 ± 1       3±2       5      83 ± 2   17 ± 2    —           —           —
         list2             5       95 ± 1       2±2       5      83 ± 2   17 ± 3    —           —           —
         matrix           51      101 ± 2      11 ± 2    —           —        —     —           —           —
         matrixDims       13       94 ± 2       4±2      13      75 ± 2   31 ± 2    21      66 ± 1      93 ± 1
         max               4       70 ± 1       5±2       4      74 ± 1   25 ± 2     6      49 ± 1      56 ± 2
         maxGen           11      103 ± 1       2±2      —           —        —     —           —           —
         maxGenBig        15      109 ± 2      14 ± 2    —           —        —     —           —           —
         mergeSort        29       95 ± 1      11 ± 2    —           —        —     53      62 ± 2     648 ± 4
         postuple          4       71 ± 2       6±2       4      73 ± 1   18 ± 2     9      68 ± 1      36 ± 1
         range            19       99 ± 1       4±2      —           —        —     —           —           —
         rational          6       71 ± 1       5±2       6      75 ± 1   26 ± 1    10      67 ± 1      47 ± 1
         sqrt              9       74 ± 1       7±2       9      77 ± 1   25 ± 1    14      49 ± 1      66 ± 2
         sumnat           10       69 ± 1       6±1      10      74 ± 1   21 ± 2    —           —           —
         vec              12       74 ± 2       6±2      —           —        —     20      56 ± 1     136 ± 2



   Impact on code that does not use the feature. Because refinement checking is integrated into
the compiler rather than layered on top, a natural concern is whether it affects existing code. To
assess this, we run the full Dotty continuous-integration suite with the feature enabled. It passes
unchanged: this includes compiling the Scala compiler itself (∼200 000 lines of code), its ∼10 000
compilation tests (∼300 000 lines), and a community build of 50 open-source projects (∼700 000
lines), indicating that the extension introduces no backward incompatibility. On the official Scala
compiler benchmark suite,5 enabling the feature slows compilation by at most 4% with the current
prototype, on both the 11 “Big” benchmarks, which compile real-world libraries totalling ∼70 000
lines, and the 20 “Small” benchmarks. In short, when the feature is unused, it changes no behavior
and adds only a small compilation-time overhead.
   Expressiveness. The three systems differ in which programs they can express. Schmid’s qualifier
inference operates in a separate phase from Scala’s type checker, so refinements do not participate
in type-argument inference: generic data structures can be instantiated with qualified types only by
writing the type arguments explicitly, and inferred instantiations such as the one in Figure 1 are out
of reach. Stainless supports richer specifications through require and ensuring clauses with a full
SMT backend, but refinements are not types: they do not compose with bounded polymorphism,
type inference, or pattern matching. Our system integrates with all of these by construction, since
refinement types are ordinary Scala types.
5 https://lampepfl.github.io/scala3-benchmarks/



                          Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:24                                                                Matt Bovel, Viktor Kunčak, and Martin Odersky


  On the other hand, both Schmid’s system and Stainless have substantially more powerful solvers.
Both use SMT-backed solvers that are complete for linear integer arithmetic, algebraic data types,
equality, and first-order logic—theories for which our lightweight e-graph solver offers no decision
procedure. As a consequence, several of Schmid’s benchmarks that require linear arithmetic rea-
soning (e.g., sumnat, arrfold) cannot be verified by our solver, and Stainless can verify functional
correctness properties well beyond what refinement types alone can express.

5   Related Work
   Mechanized refinement type systems. Hamza et al. [16] mechanize System FR, a dependently-
typed calculus with refinement types, polymorphism, recursive types, and dependent pairs, serving
as a foundation for the Stainless verifier. Their system is the closest to ours in ambition and was a
major inspiration, particularly for the positivity-based treatment of recursive types. Key differences
are: (1) System FR enforces total correctness, requiring termination proofs for all recursive functions,
while our partial-correctness approach avoids this burden; (2) System FR uses dependent pairs as
existentials to handle variables going out of scope, while we use avoidance; and (3) System FR uses
index-guarded recursive types Rec(𝑛) (𝛼 ⇒ 𝜏), while we use equi-recursive types with fold/unfold
subtyping. Borkowski et al. [3] mechanize a refinement type system extending System F in Liquid
Haskell. They restrict refinements to base types (no nested refinements), use well-formedness
conditions and existential types rather than avoidance, and elegantly axiomatize the implication
judgment as eleven abstract properties that an SMT oracle must satisfy for soundness, without
committing to a specific solver. We instead leave implication fully semantic (§3.6). Sun et al. [38]
mechanize RFJ, a refinement type system for a Featherweight Java-like language, in Coq. They
provide both type soundness and logical soundness (characterizing which formulas are valid). Their
system lacks parametric polymorphism but handles selfification and class-based subtyping in an
object-oriented setting.
   Definitional interpreters and semantic soundness. Our mechanization builds on Amin and
Rompf’s [1] technique of proving type safety via a fuel-bounded definitional interpreter. One
of their key insights is that big-step semantics sidesteps the “bad bounds” problem that plagues
small-step proofs for languages with type members. However, their development proves syntactic
type safety (progress and preservation) rather than defining semantic types. Owens et al. [31]
introduced functional big-step semantics, and Paraskevopoulou et al. [32] use a similar interpreter-
based approach with step-indexed logical relations for multi-pass compiler verification. In both
systems, fuel is consumed at every evaluation step, whereas ours bounds evaluation depth (§3.2).
Semantic typing, interpreting types as predicates or relations on values, has a long history in
logical relations [42]. Giarrusso et al. [15] develop a semantic model for DOT, with subtyping and
recursive types using step-indexed logical relations and a “later” modality in the type syntax. We
avoid step-indexing entirely by requiring strict positivity for recursive type binders (following
Hamza et al. [16]), enabling a direct fixpoint construction via intersected approximations (§3.6).
   Refinement types in other languages. We reviewed the history of refinement types in the in-
troduction. Flanagan’s hybrid type checking [11] introduced the idea of automatically inserting
run-time checks when the static system cannot discharge a refinement obligation. In our sys-
tem, run-time checks are not inserted automatically: the programmer explicitly requests them via
.runtimeChecked or pattern matching (§2), which the type system treats as an ordinary conditional
branch, so no special rules are needed for the static/dynamic boundary. Moreover, our run-time
checks are restricted to first-order predicates, which avoids the blame assignment problem that
arises when monitoring higher-order contracts [21]: since functions cannot be checked eagerly, a
violation detected at a later call site must be attributed to the party at fault.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                        409:25


   Liquid Haskell [44, 45] brings refinement types to Haskell as a separate plugin, with refinement
inference running apart from GHC’s own type checking, whereas our refinements are typed and
inferred by the compiler itself. Termination also plays a different role: Liquid Haskell by default
requires every function to be proven terminating, while we need termination only in the solver, to
justify certain normalization and unfolding rules (§2.3). Finally, Liquid Haskell discharges obligations
with an SMT solver over decidable theories, while our solver (§4.3) combines e-graphs with
normalization rules: it forgoes arithmetic decision procedures, but natively performs beta reduction
and limited higher-order reasoning over predicate lambdas. The recent PLEX extension [10] adds
normalization—eta-expansion, beta-reduction, and dependent pattern matching—to Liquid Haskell’s
Proof by Logical Evaluation layer, precisely to recover higher-order reasoning over a first-order
SMT solver.
   In the systems programming space, refinement types have been combined with mutation, where
the central difficulty is deciding when established predicates must be invalidated: a refinement
of a mutable location can be treated as an invariant that every write must preserve, or as a flow-
sensitive fact that a write updates or invalidates. Under aliasing, knowing which writes affect
which facts is itself hard. Refinement type systems for Rust lean on the ownership discipline:
Flux [25] permits strong updates, changing a location’s refinement, through exclusively owned
pointers, but only invariant-preserving weak updates through mutable borrows, while Thrust [30]
and RefinedRust [13] type a borrow as its current value paired with a prophecy variable for its
final value. RefinedC [34] and RefinedRust come with foundational soundness proofs in the Iris
separation logic, and Verus [24] provides SMT-based verification for Rust using linear ghost types;
these systems target memory safety and low-level invariants. Generic refinement types [26] add
refinement polymorphism to Flux. The separation checking sketched in §2.2 would give Scala a
similar handle on invalidation: like ownership, capabilities [48] with separation checking [49] make
writes explicit and un-aliased, identifying the facts a write can invalidate. For TypeScript, Refined
TypeScript [46] sidesteps invalidation by allowing refinements to mention object state only through
immutable fields, and recovers flow-sensitive reasoning for local variables via an SSA translation.
   The Checker Framework [8] brings user-defined pluggable type qualifiers to Java: like refinement
types, qualifiers attach additional information to types, and like the separate-phase systems above,
the checkers run as compiler plugins over Java’s annotation syntax, outside the language’s own type
system. Qualifiers are drawn from a fixed vocabulary and checked by dataflow analysis rather than
a solver, a trade-off that scales to large codebases and many practical properties, such as verifying
array indexing [22], at the cost of expressiveness. Lanzinger et al. [23] blur the line between the
two approaches by combining pluggable type qualifiers with deductive verification, discharging
obligations that the type checker cannot prove with a program verifier.

6   Conclusion
We have shown that refinement types can be integrated as first-class citizens into the type system of
a mainstream programming language. By extending the Scala 3 compiler directly, refinement types
interact naturally with subtyping, bounded polymorphism, type inference, and pattern matching,
avoiding the two-mental-models problem of separate-phase approaches.
   On the theoretical side, we provide the first mechanized soundness proof that combines re-
finement types with union and intersection types, bounded polymorphism with lower and upper
bounds, and positive equi-recursive types. The proof uses a fuel-bounded definitional interpreter
with semantic typing in Rocq, and establishes partial-correctness type safety for a core calculus
that captures key features of Scala’s type system. On the practical side, the prototype adds refine-
ment types to an industrial-strength compiler with modest changes (≈2 500 lines), a self-contained
e-graph solver requiring no external dependencies, and compilation overhead that remains low.

                         Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:26                                                                   Matt Bovel, Viktor Kunčak, and Martin Odersky


Data-Availability Statement
The accompanying artifact [4] contains:
 • Mechanization. The Rocq formalization of the type system, with its soundness proof.
 • Implementation. The source of our Dotty extension, also published on Maven and usable
   from any SBT project with:
    scalaOrganization := "ch.epfl.lara"
    scalaVersion := "3.10.0-RC1-bin-20260720-5f1bae1-NIGHTLY"
    scalacOptions ++= Seq("-language:experimental.qualifiedTypes")

 • Benchmarks. The JMH benchmark suites used for the evaluation, compiling similar programs
    with our Dotty fork, Schmid’s prototype, and Stainless, together with scripts to run them and
    collect results.
  The same material, with its continued development, is available in the project’s public repository:
https://github.com/mbovel/first-class-refinement-types-in-scala.

AI-Usage Statement
AI tools were used in the preparation of this paper and its artifacts, primarily Claude Code (Opus
4.5 and 4.6, Fable 5). Theorem and lemma statements were written by the authors, while many
proof bodies were generated with AI assistance. The core implementation predates widespread
agentic AI tools, but recent bug fixes and refactorings were AI-assisted (AI-assisted commits are
explicitly marked in the git history with Co-authored-by: Claude *). GitHub Copilot was also
used for code autocompletion, and Google and ChatGPT for general research questions.

Acknowledgments
We thank the LAMP and LARA teams at EPFL for insightful discussions and the prior work that
laid the foundation for this paper, and in particular Sébastien Doeraene and Guillaume Martres for
their valuable feedback on the Dotty implementation.

References
 [1] Nada Amin and Tiark Rompf. 2017. Type soundness proofs with definitional interpreters. SIGPLAN Not. 52, 1 (Jan.
     2017), 666–679. doi:10.1145/3093333.3009866
 [2] Quentin Bernet. 2024. Syntax and Runtime Checks for Qualified Types in Scala 3. Master’s thesis. École Polytechnique
     Fédérale de Lausanne (EPFL), Lausanne, Switzerland.
 [3] Michael H. Borkowski, Niki Vazou, and Ranjit Jhala. 2024. Mechanizing Refinement Types. Proc. ACM Program. Lang.
     8, POPL, Article 70 (Jan. 2024), 30 pages. doi:10.1145/3632912
 [4] Matt Bovel, Viktor Kunčak, and Martin Odersky. 2026. First-Class Refinement Types in Scala — Artifact. doi:10.5281/
     zenodo.21737784
 [5] Luca Cardelli, Simone Martini, John C. Mitchell, and Andre Scedrov. 1991. An extension of system F with subtyping. In
     Theoretical Aspects of Computer Software, Takayasu Ito and Albert R. Meyer (Eds.). Springer Berlin Heidelberg, Berlin,
     Heidelberg, 750–770.
 [6] Robert Cartwright. 1976. User-Defined Data Types as an Aid to Verifying LISP Programs. In Third International
     Colloquium on Automata, Languages and Programming, University of Edinburgh, UK, July 20-23, 1976, S. Michaelson
     and Robin Milner (Eds.). Edinburgh University Press, 228–256.
 [7] École Polytechnique Fédérale de Lausanne. 2024. The Scala 3 Language Specification, Version 3.4. §13: Syntax Summary.
     Retrieved July 21, 2026 from https://www.scala-lang.org/files/archive/spec/3.4/, archived at [https://perma.cc/ENJ6-
     7FAR]
 [8] Werner Dietl, Stephanie Dietzel, Michael D. Ernst, Kıvanç Muşlu, and Todd W. Schiller. 2011. Building and Using
     Pluggable Type-Checkers. In Proceedings of the 33rd International Conference on Software Engineering (ICSE ’11).
     Association for Computing Machinery, New York, NY, USA, 681–690. doi:10.1145/1985793.1985889
 [9] Chris Fallin. 2023. Cranelift’s Acyclic Egraph implementation. Rust crate documentation. Retrieved July 21, 2026
     from https://docs.rs/cranelift-egraph/latest/cranelift_egraph/, archived at [https://perma.cc/T7YL-6QEX]

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                               409:27


[10] Alessio Ferrarini, Niki Vazou, and Wouter Swierstra. 2026. PLEX: Normalization for Refinement Types. Proc. ACM
     Program. Lang. 10, OOPSLA1 (April 2026), 1321–1347. doi:10.1145/3798248
[11] Cormac Flanagan. 2006. Hybrid type checking. SIGPLAN Not. 41, 1 (Jan. 2006), 245–256. doi:10.1145/1111320.1111059
[12] Tim Freeman and Frank Pfenning. 1991. Refinement types for ML. SIGPLAN Not. 26, 6 (May 1991), 268–277. doi:10.
     1145/113446.113468
[13] Lennard Gäher, Michael Sammler, Ralf Jung, Robbert Krebbers, and Derek Dreyer. 2024. RefinedRust: A Type System
     for High-Assurance Verification of Rust Programs. Proc. ACM Program. Lang. 8, PLDI, Article 192 (June 2024), 25 pages.
     doi:10.1145/3656422
[14] Catarina Gamboa, Abigail Reese, Alcides Fonseca, and Jonathan Aldrich. 2025. Usability Barriers for Liquid Types.
     Proc. ACM Program. Lang. 9, PLDI, Article 224 (June 2025), 26 pages. doi:10.1145/3729327
[15] Paolo G. Giarrusso, Léo Stefanesco, Amin Timany, Lars Birkedal, and Robbert Krebbers. 2020. Scala step-by-step:
     soundness for DOT with step-indexed logical relations in Iris. Proc. ACM Program. Lang. 4, ICFP (2020), 114:1–114:29.
     doi:10.1145/3408996
[16] Jad Hamza, Nicolas Voirol, and Viktor Kunčak. 2019. System FR: formalized foundations for the stainless verifier. Proc.
     ACM Program. Lang. 3, OOPSLA, Article 166 (Oct. 2019), 30 pages. doi:10.1145/3360592
[17] Li Haoyi. 2016. Fansi: Scala library for manipulating Fancy Ansi colored strings. Retrieved July 21, 2026 from
     https://github.com/com-lihaoyi/fansi
[18] Iltotore. 2021. Iron: A compile-time and runtime refinement library for Scala 3. Retrieved July 21, 2026 from
     https://github.com/Iltotore/iron
[19] Ranjit Jhala. 2019. Why Refinement Types? Retrieved July 21, 2026 from https://ucsd-progsys.github.io/liquidhaskell/
     blogposts/2019-10-20-why-types.lhs/, archived at [https://perma.cc/7PMH-598D]
[20] Ranjit Jhala and Niki Vazou. 2021. Refinement Types: A Tutorial. Found. Trends Program. Lang. 6, 3–4 (Oct. 2021),
     159–317. doi:10.1561/2500000032
[21] Matthias Keil and Peter Thiemann. 2015. Blame assignment for higher-order contracts with intersection and union.
     SIGPLAN Not. 50, 9 (Aug. 2015), 375–386. doi:10.1145/2858949.2784737
[22] Martin Kellogg, Vlastimil Dort, Suzanne Millstein, and Michael D. Ernst. 2018. Lightweight Verification of Array
     Indexing. In Proceedings of the 27th ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA
     2018). Association for Computing Machinery, New York, NY, USA, 3–14. doi:10.1145/3213846.3213849
[23] Florian Lanzinger, Alexander Weigl, Mattias Ulbrich, and Werner Dietl. 2021. Scalability and Precision by Combining
     Expressive Type Systems and Deductive Verification. Proc. ACM Program. Lang. 5, OOPSLA (Oct. 2021), 1–29.
     doi:10.1145/3485520
[24] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno,
     and Chris Hawblitzel. 2023. Verus: Verifying Rust Programs using Linear Ghost Types. Proc. ACM Program. Lang. 7,
     OOPSLA1, Article 85 (April 2023), 30 pages. doi:10.1145/3586037
[25] Nico Lehmann, Adam T. Geller, Niki Vazou, and Ranjit Jhala. 2023. Flux: Liquid Types for Rust. Proc. ACM Program.
     Lang. 7, PLDI, Article 169 (June 2023), 25 pages. doi:10.1145/3591283
[26] Nico Lehmann, Cole Kurashige, Nikhil Akiti, Niroop Krishnakumar, and Ranjit Jhala. 2025. Generic Refinement Types.
     Proc. ACM Program. Lang. 9, POPL (Jan. 2025), 1446–1474. doi:10.1145/3704885
[27] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Verifier for Functional Correctness. In Logic for Programming,
     Artificial Intelligence, and Reasoning, Edmund M. Clarke and Andrei Voronkov (Eds.). Springer Berlin Heidelberg,
     Berlin, Heidelberg, 348–370. doi:10.1007/978-3-642-17511-4_20
[28] Greg Nelson and Derek C. Oppen. 1980. Fast Decision Procedures Based on Congruence Closure. J. ACM 27, 2 (April
     1980), 356–364. doi:10.1145/322186.322198
[29] Martin Odersky, Yaoyu Zhao, Yichen Xu, Oliver Bračevac, and Cao Nguyen Pham. 2026. Tracking Capabilities for
     Safer Agents. arXiv:2603.00991 [cs.AI] https://arxiv.org/abs/2603.00991
[30] Hiromi Ogawa, Taro Sekiyama, and Hiroshi Unno. 2025. Thrust: A Prophecy-Based Refinement Type System for Rust.
     Proc. ACM Program. Lang. 9, PLDI, Article 230 (June 2025), 29 pages. doi:10.1145/3729333
[31] Scott Owens, Magnus O. Myreen, Ramana Kumar, and Yong Kiam Tan. 2016. Functional Big-Step Semantics. In
     Proceedings of the 25th European Symposium on Programming Languages and Systems - Volume 9632. Springer-Verlag,
     Berlin, Heidelberg, 589–615. doi:10.1007/978-3-662-49498-1_23
[32] Zoe Paraskevopoulou, John M. Li, and Andrew W. Appel. 2021. Compositional optimizations for CertiCoq. Proc. ACM
     Program. Lang. 5, ICFP, Article 86 (Aug. 2021), 30 pages. doi:10.1145/3473591
[33] Patrick M. Rondon, Ming Kawaguci, and Ranjit Jhala. 2008. Liquid types. SIGPLAN Not. 43, 6 (June 2008), 159–169.
     doi:10.1145/1379022.1375602
[34] Michael Sammler, Rodolphe Lepigre, Robbert Krebbers, Kayvan Memarian, Derek Dreyer, and Deepak Garg. 2021.
     RefinedC: automating the foundational verification of C code with refined ownership types. In Proceedings of the 42nd
     ACM SIGPLAN International Conference on Programming Language Design and Implementation (Virtual, Canada) (PLDI


                          Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
409:28                                                                    Matt Bovel, Viktor Kunčak, and Martin Odersky


     2021). Association for Computing Machinery, New York, NY, USA, 158–174. doi:10.1145/3453483.3454036
[35] Georg Stefan Schmid and Viktor Kuncak. 2016. SMT-based checking of predicate-qualified types for Scala. In Proceedings
     of the 2016 7th ACM SIGPLAN Symposium on Scala (Amsterdam, Netherlands) (SCALA 2016). Association for Computing
     Machinery, New York, NY, USA, 31–40. doi:10.1145/2998392.2998398
[36] Valentin Schneeberger. 2024. Runtime Checks for Qualified Types in Scala 3. Bachelor’s thesis. École Polytechnique
     Fédérale de Lausanne (EPFL), Lausanne, Switzerland.
[37] Rudi Schneider, Marcus Rossel, Amir Shaikhha, Andrés Goens, Thomas Kœhler, and Michel Steuwer. 2025. Slotted
     E-Graphs: First-Class Support for (Bound) Variables in E-Graphs. Proc. ACM Program. Lang. 9, PLDI, Article 223 (June
     2025), 23 pages. doi:10.1145/3729326
[38] Ke Sun, Di Wang, Sheng Chen, Meng Wang, and Dan Hao. 2024. Formalizing, Mechanizing, and Verifying Class-Based
     Refinement Types. In 38th European Conference on Object-Oriented Programming (ECOOP 2024) (Leibniz International
     Proceedings in Informatics (LIPIcs), Vol. 313), Jonathan Aldrich and Guido Salvaneschi (Eds.). Schloss Dagstuhl –
     Leibniz-Zentrum für Informatik, Dagstuhl, Germany, 39:1–39:30. doi:10.4230/LIPIcs.ECOOP.2024.39
[39] Nikhil Swamy, Cătălin Hriţcu, Chantal Keller, Aseem Rastogi, Antoine Delignat-Lavaud, Simon Forest, Karthikeyan
     Bhargavan, Cédric Fournet, Pierre-Yves Strub, Markulf Kohlweiss, Jean-Karim Zinzindohoue, and Santiago Zanella-
     Béguelin. 2016. Dependent types and multi-monadic effects in F*. SIGPLAN Not. 51, 1 (Jan. 2016), 256–270. doi:10.
     1145/2914770.2837655
[40] The Rocq Development Team. 2025. The Rocq Prover. https://rocq-prover.org/
[41] Frank S. Thomas. 2015. refined: Refined is a Scala library for refinement types. Retrieved July 21, 2026 from
     https://github.com/fthomas/refined
[42] Amin Timany, Robbert Krebbers, Derek Dreyer, and Lars Birkedal. 2024. A Logical Approach to Type Soundness. J.
     ACM 71, 6, Article 40 (Nov. 2024), 75 pages. doi:10.1145/3676954
[43] Niki Vazou, Patrick M. Rondon, and Ranjit Jhala. 2013. Abstract refinement types. In Proceedings of the 22nd European
     Conference on Programming Languages and Systems (Rome, Italy) (ESOP’13). Springer-Verlag, Berlin, Heidelberg,
     209–228. doi:10.1007/978-3-642-37036-6_13
[44] Niki Vazou, Eric L. Seidel, Ranjit Jhala, Dimitrios Vytiniotis, and Simon Peyton-Jones. 2014. Refinement types for
     Haskell. SIGPLAN Not. 49, 9 (Aug. 2014), 269–282. doi:10.1145/2692915.2628161
[45] Niki Vazou, Anish Tondwalkar, Vikraman Choudhury, Ryan G. Scott, Ryan R. Newton, Philip Wadler, and Ranjit Jhala.
     2017. Refinement reflection: complete verification with SMT. Proc. ACM Program. Lang. 2, POPL, Article 53 (Dec. 2017),
     31 pages. doi:10.1145/3158141
[46] Panagiotis Vekris, Benjamin Cosman, and Ranjit Jhala. 2016. Refinement Types for TypeScript. In Proceedings of the
     37th ACM SIGPLAN Conference on Programming Language Design and Implementation (Santa Barbara, CA, USA) (PLDI
     ’16). Association for Computing Machinery, New York, NY, USA, 310–325. doi:10.1145/2908080.2908110
[47] Max Willsey, Chandrakana Nandi, Yisu Remy Wang, Oliver Flatt, Zachary Tatlock, and Pavel Panchekha. 2021.
     egg: Fast and extensible equality saturation. Proc. ACM Program. Lang. 5, POPL, Article 23 (Jan. 2021), 29 pages.
     doi:10.1145/3434304
[48] Yichen Xu, Oliver Bračevac, Cao Nguyen Pham, and Martin Odersky. 2025. What’s in the Box: Ergonomic and
     Expressive Capture Tracking over Generic Data Structures. Proc. ACM Program. Lang. 9, OOPSLA2, Article 334 (Oct.
     2025), 28 pages. doi:10.1145/3763112
[49] Yichen Xu, Oliver Bračevac, Cao Nguyen Pham, Yaoyu Zhao, and Martin Odersky. 2026. System Capybara: Tracking
     Capabilities for Separation and Freshness (Extended Version). arXiv:2607.09383 [cs.PL] https://arxiv.org/abs/2607.09383
[50] Jean-Karim Zinzindohoué, Karthikeyan Bhargavan, Jonathan Protzenko, and Benjamin Beurdouche. 2017. HACL*:
     A Verified Modern Cryptographic Library. In Proceedings of the 2017 ACM SIGSAC Conference on Computer and
     Communications Security (Dallas, Texas, USA) (CCS ’17). Association for Computing Machinery, New York, NY, USA,
     1789–1806. doi:10.1145/3133956.3134043
[51] Philip Zucker. 2024. Acyclic Egraphs and Smart Constructors. Retrieved July 21, 2026 from https://www.philipzucker.
     com/smart_constructor_aegraph/, archived at [https://perma.cc/3X86-XKRU]

Received 2026-03-23; accepted 2026-08-06




Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
First-Class Refinement Types for Scala                                                                        409:29


A    More examples

// Example 3: Matrix operations with checked dimensions
case class Matrix(width: Pos, height: Pos):
  private val size = width * height
  private val data = CheckedArray(size.runtimeChecked)
  def index(i: Pos with i < height,
            j: Pos with j < width): {res: Pos with res < data.size} =
    (i * width + j).runtimeChecked
  def apply(i: Pos with i < height, j: Pos with j < width): Double =
    data(index(i, j))
  def update(i: Pos with i < height, j: Pos with j < width, x: Double): Unit =
    data(index(i, j)) = x
  def transpose(): {v: Matrix with v.width == height && v.height == width} = ???
  def mul(that: Matrix with that.height == width):
    {v: Matrix with v.width == that.width && v.height == height}
  =
    val res = Matrix(that.width, height)
    forRange(0, height): i =>
      forRange(0, that.width): j =>
        var sum = 0.0
        forRange(0, width): k =>
          sum = sum + this(i, k) * that(k, j)
        res(i, j) = sum
    res
def matricesExample =
  val m1 = Matrix(2, 3)
  val m2 = Matrix(3, 2)
  m1.mul(m2)
  val m1T = m1.transpose()
  m1T.mul(m1)

// Example 4: Memoized Fibonacci with a dependent map
case class DepMap[K, V](p: (K, V) => Boolean):
  def put(n: K, v: V with p(n, v)): Unit = ???
  def get(n: K): Option[{res: V with p(n, res)}] = ???
def fib(n: Int): {r: Int with r == (if n <= 1 then 1 else fib(n - 1) + fib(n - 2))} =
  if n <= 1 then 1 else fib(n - 1) + fib(n - 2)
val cache: (DepMap[Int, Int] with (cache == DepMap[Int, Int]((k, v) => v == fib(k)))) =
  DepMap[Int, Int]((k, v) => v == fib(k))
def fibMemo(n: Int): {res: Int with res == fib(n)} =
  cache.get(n) match
    case Some(res) => res
    case None =>
      val res: (Int with (res == fib(n))) =
        if n <= 1 then 1 else fibMemo(n - 1) + fibMemo(n - 2)
      cache.put(n, res)
      res

                         Proc. ACM Program. Lang., Vol. 10, No. OOPSLA2, Article 409. Publication date: October 2026.
