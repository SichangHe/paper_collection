                                         Type Safety via Hoare Logic with Separation and Pure Types

                                         WENHUA LI            DARIUS FOO            QUANG TRUNG TA                 WEI-NGAN CHIN
                                         Type safety has traditionally rested on carefully crafted type systems, under the motto “well-typed programs
                                         cannot go wrong”. Modern demands push type systems past this basic guarantee: toward greater memory
                                         safety (e.g., Rust), stronger data-structure invariants (e.g., Haskell’s GADTs), and broader typability (e.g.,
                                         MLstruct). In principle the classic motto absorbs each such property by enlarging the set of states deemed
                                         “wrong”; but this collapses them into a single binary verdict, erasing the very distinctions that make them
                                         valuable. Heap ownership, flow-sensitive changes to a variable’s type, and the gap between a recoverable and
                                         a fatal error are relational, stateful facts about a program’s intermediate states, facts one “go wrong” verdict
                                         cannot tell apart. Worse, each new demand typically arrives as its own custom extension, making it hard to
                                         say what any one guarantees, whether two are compatible, or how they combine.
                                             What is missing is a single foundation in which such properties can be stated, compared, and combined;
                                         Floyd-Hoare logic supplies it. We present a framework for type-safety verification built from four ingredients:
                                         (i) case specifications for path-sensitive typing; (ii) separation types, inspired by separation logic, for flow-
                                         sensitive type mutation and must-aliasing; (iii) a disciplined distinction between Err (runtime error values
arXiv:2607.25262v1 [cs.PL] 28 Jul 2026




                                         our types track) and Abrt (compile-time errors), yielding the refined motto well-typed programs must never
                                         abort; and (iv) type predicates for rich data-structure invariants. All four are ordinary types in a single Boolean
                                         algebra rather than one-off extensions. The framework therefore subsumes both GADTs and liquid types
                                         within one type logic and spans a spectrum of guarantees: from weak specifications that tolerate Err values
                                         to strong ones that eliminate them entirely. The algebra also keeps checking tractable: subtyping reduces to
                                         a single decidable emptiness test, so one lightweight procedure serves the whole framework with no SMT
                                         oracle in its trusted base. We formalise the Hoare rules and prove soundness in a machine-checked Lean
                                         mechanisation; by proof reflection, the mechanisation itself yields a self-certifying type-checker, which we
                                         evaluate on a suite of benchmark programs.

                                         1   INTRODUCTION
                                         Type systems are being asked to do more than ever. Beyond the classic guarantee that well-
                                         typed programs do not go wrong, modern languages demand richer properties: memory safety
                                         through ownership and borrowing (Rust), stronger data structure invariants through generalised
                                         algebraic data types (GADTs in OCaml and Haskell), broader typability through semantic subtyping
                                         (MLsub [11], MLstruct [32]), and low-latency execution through modal resource management
                                         (OxCaml [28, 39]). Dynamically-typed languages face the same pressure from a different direction,
                                         as gradual typing retrofits (e.g. Hack [29] and Typed Racket [41]) attempt to recover static guarantees
                                         incrementally. Folding all of these into a single “go wrong” predicate blurs distinctions that matter
                                         about a program’s intermediate states: whether a heap location is owned, how a variable’s type
                                         evolves as the program runs, and whether an error is a recoverable Err to be tolerated or a fatal
                                         Abrt to be ruled out (Sec. 2.3). This last distinction is the one we lean on throughout. Meanwhile,
                                         the foundational framework has not kept pace: each such feature arrives as its own extension,
                                         leaving it unclear how the resulting guarantees relate or compose.
                                            In this paper, we argue that Floyd-Hoare logic provides exactly the right foundation for a unified
                                         treatment of type safety. Hoare logic is inherently modular: the type property of each function is
                                         captured by a pre/post specification that can be verified and reused independently. It is flow-sensitive
                                         by design, tracking how types evolve through a program rather than assigning a single static type to
                                         each variable. It is also expressive enough to accommodate both statically- and dynamically-typed
                                         programs within the same framework, by adjusting the strength of the specifications rather than
                                         changing the underlying logic. The key question is whether type signatures (the concise, familiar
                                         form of type information) can be faithfully and conveniently represented as Hoare-style pre/post
                                         Department of Computer Science, National University of Singapore. {liwenhua, dariusf, taqt, chinwn}@nus.edu.sg.
2                                                                                    Li, Foo, Ta, and Chin


specifications. We show that they can, and that the resulting framework supports strictly more than
standard type systems.
   We now illustrate these points through a series of examples, building from simple type signatures
to flow-sensitive specifications for heap-mutating programs. Consider two functions from an ML-
like language: a conversion function str_of_int from Int to its Str counterpart; and a polymorphic
(!) operator to dereference a mutable Ref.
         str_of_int : Int → Str
         (!)        : ∀T. Ref (T) → T
   While type signatures are concise, it is almost as easy to write their type specifications using
pre/postconditions in Hoare logic. For the above examples, we can obtain the corresponding type
specifications by suitably naming the inputs v∗ and output r of each function using the precondition
clause req[v∗ ] and the postcondition clause ens[r], respectively (their formal definition is given
in Sec. 3.2), as shown below.
    str_of_int : req [x] x: Int   ens [r] r: Str
    (!)        : ∀T. req [x] x: Ref (T)   ens [r] r:T
   For the examples above, each type signature of the form t1 → t2 can be directly translated into
a type specification of the form req[x] x:t1 ens[r] r:t2 , where x and r are freshly named. So far,
the gain over type signatures is mainly notational.
   The real advantage of Hoare logic emerges when type signatures fall short: a variable’s type may
change as the program runs, and the mutated location may be aliased. In the simplified program
below, a field is coerced in place from its raw Str form to an Int (as when normalising configuration
or JSON data). For instance, normalising a JSON record like {"port": "8080"} rewrites the string-
valued port field in place to the integer 8080, which downstream code then uses in arithmetic.
A mutable object is typically reached through several names – an earlier binding, a record field,
a captured variable, a function argument – so we use alias to illustrate an aliased reference.
The write goes through box, while alias (bound earlier) stays live and is read afterwards. No
mainstream type system tracks this combination of type mutation and aliasing soundly.
     coerce ( b )   = update (b , str_of_int (! b))           //   in - place type change
     caller ( box ) = let alias = box in                      //   alias , box : must - aliases
                      coerce ( box );                         //   box now stores an Int
                      ! alias + 1                             //   safe iff alias : Int

   To capture this kind of flow-sensitive type change, a pure type box:Ref(Any) is too weak: it fixes
a single stored type and loses the precise Str → Int change. We instead introduce the separation
type box↦→Ref(t1 ), which carries full ownership of the heap location at box and can be updated
to a different type box↦→Ref(t2 ) as the program evolves. The notation is inspired by separation
logic [36], but serves a different purpose. Separation logic reasons about functional correctness of
programs already assumed to be type-checked. By contrast, we aim to deliver stronger type-safety
guarantees, here soundly tracking the type of an aliased, mutable heap location. Coupled with
pre/post type specification, we can now provide a precise, flow-sensitive type specification for
coerce, and, more generally, for the update it calls, as shown below.
    coerce : req [b] b↦→ Ref ( Str ) ens [_] b↦→ Ref ( Int )
    update : ∀T . case [x ,u] { x: Ref (T) ∧ u :T ens [r] r :() ;
                                 x↦→ Ref (_) ∧ u: Any ens [r] x↦→ Ref ({ u }) ∧ r :() }

   Here case[v∗ ]{ g1 s1 ; . . . } names the inputs v∗ and lists guarded behaviours: when the pre-state
satisfies guard gi , the function behaves as si (an ens[r]-postcondition on the result r). The clauses,
Type Safety via Hoare Logic with Separation and Pure Types                                                         3


separated by ;, are pairwise disjoint, so at most one matches any call. (The separation type x↦→T
and the _ wildcard are introduced in Sec. 2.2.)
   For the update method, we use a case specification to capture both the flow-insensitive pure-type
scenario x:Ref(T), and the flow-sensitive separation-type scenario x↦→Ref(_). Which case applies at
a given call is determined by the caller’s static pre-state: the case whose guard the caller’s incoming
types satisfy is the one selected. Thus, in a pure-type context the first case applies, while a caller
holding full ownership x↦→Ref(_) selects the second. In that case’s postcondition x↦→Ref({u}), the
value argument u is used as the singleton type {u}, recording that the cell now stores exactly u. To
be explicit, we can write {u} to denote each singleton type u. Since pure and separation types are
disjoint (x:Ref(T) and x↦→Ref(_) can never hold at once), the two cases are mutually exclusive.
   Why this is beyond existing type systems. Trace the aliased coercion. The call coerce(box)
selects the separation case of update, rewriting box’s stored type from Str to Int; the post-state
records box↦→Ref(Int). The subtle point is alias: again using a variable as a singleton type, we
record the must-alias as alias:{box} (read alias=box). Our logic then propagates the change, so
alias↦→Ref(Int) holds afterwards and !alias + 1 type-checks. Type mutation and must-aliasing
are both essential: drop either and the program is wrongly rejected or unsoundly accepted. This is
precisely where existing systems fall short.
 • OCaml, Haskell. A mutable cell (′ a ref, IORef a) fixes its stored type at creation: only its value,
    never its type, may change, so the Str → Int update is inexpressible.
 • Rust, uniqueness/linear types. Strong updates are permitted, but only for unaliased locations; the
    live alias is rejected outright, so the safe program cannot be written without an unsafe or
    Rc<RefCell> escape hatch.
 • TypeScript (gradual). Control-flow narrowing may change box’s static type locally, but the
    refinement is discarded across the coerce call and never propagates to alias; the code type-
    checks only via an unchecked cast (!alias as Int) that silently escapes the type system.1
 • Python (dynamic). The mutation is permitted but wholly unchecked: if coerce is omitted or
    misordered, !alias + 1 raises a runtime TypeError, an Err our framework rules out statically.
No mainstream type system soundly tracks the stored type of an aliased heap location as it changes;
our separation types, combining full ownership with must-aliasing, close exactly this gap. This use
of a variable singleton to record aliasing is not itself new; it underpins Scala’s path-dependent types
and their formal calculus pDOT [35], where a singleton x.type states that two paths denote the
same object. There, however, singletons are confined to immutable (stable) paths, precisely because
a value’s type never changes, so they support only type-equality reasoning. We instead pair the
variable singleton with a separation type carrying full ownership, which licenses a type-changing
update of the aliased cell, the capability those systems by design cannot support.
   In this paper, we develop a Hoare logic framework for type safety in which separation types (with
must-aliasing) provide flow-sensitivity, while flow-insensitive pure types (with arbitrary aliasing)
are used whenever type mutation is not required.
   A further benefit of the distinct Err/Abrt hierarchy is more precise error reporting: an Err is a
recoverable value that may live in a well-typed program, whereas an Abrt marks a genuine type
error flagged as a compilation error, rather than collapsing both into a single opaque “type error”.
   Our main contributions are:
      • We propose a Floyd-Hoare logic approach to type-safety verification, and introduce sepa-
         ration types to support must-aliasing and flow-sensitive type mutation. Used with flow-
         insensitive pure types, these two provide a unified framework with wider coverage.
1 See e.g. TypeScript issues #35972 and #51851 on narrowing being lost across calls and bypassed under aliasing.
4                                                                                     Li, Foo, Ta, and Chin


     • Our approach supports path-sensitivity via case specifications, and strengthened precondi-
       tions via type predicates, subsuming GADTs and liquid types.
     • We distinguish recoverable runtime errors (Err) from compile-time errors (Abrt), absent in
       well-typed programs, and fold exceptions (Exc) as first-class types.
     • We design a small core language, define its operational semantics, and construct a single type
       logic in which separation types and pure types coexist as first-class citizens. Distinctively,
       the two are related by a controlled one-way conversion: a separation type can be weakened
       to its corresponding pure type (giving up heap ownership), but the weakening is irreversible,
       since ownership once released cannot be reclaimed.
     • We give a self-contained machine-checked soundness proof in Lean 4 (Sec. 7) across the
       pure, separation, and higher-order fragments, proving well-typed programs never abort.
     • Expressive, certified type-checking. From the mechanisation we obtain a self-certifying type-
       checker: a checker proved sound once against the Hoare rules, certifying each program
       by evaluation. One automatic checker covers both fast pure-type checking and expressive
       separation-type and predicate specs, so automation and expressiveness are not traded off.

   Positioning. Our framework occupies a deliberate point on two axes. On the automation versus
expressiveness axis it sits between automatic SMT-based separation-logic provers and interactive
program logics such as Iris. Like the former it is fully automatic and, in fact, needs no SMT solver
(entailment is a lightweight, custom procedure). Yet like the latter it carries a machine-checked
soundness proof, discharged once for the rule set (Sec. 7), not per program. On the property axis it
targets type safety (semantic subtyping, flow-sensitive type mutation, and the Err/Abrt distinction)
rather than arbitrary functional correctness; scoping to type properties is precisely what buys back
full automation. The payoff is a single checker that is at once automatic, SMT-free, and certified
sound, while reaching properties no mainstream type system offers: the coexistence of separation
and pure types under a one-way weakening, and the subsumption of GADTs and liquid types within
one type logic. Concretely, for the checking direction, this answers in the affirmative whether such a
logic could serve as the type system of a compiler that verifies well-typedness automatically. App. F
realises the equality fragment of a decidable core (App. B.3), and, for the mechanised SortedList
flagships’ obligations, the inequality fragment, as a machine-checked, executable checker that
certifies each program’s typing derivation by reflection (Sec. F.4, F.5). Deciding the inequality
fragment in general, and type inference, remain future work. Detailed comparisons appear in Sec. 5
(GADTs, liquid types) and Sec. 8 (related logics).

   Paper structure. The rest of our paper is organised as follows. Sec. 2 covers the novel aspects of
our type logic via examples and can be read independently as an overview. Sec. 3 presents a core
language and the type logic that supports expressive type specifications for both statically-typed
and dynamically-typed languages. Sec. 4 presents forward-style Hoare rules for type safety, building
on Sec. 3. Sec. 5 shows how our type predicate framework subsumes both GADTs and liquid types.
Sec. 6 defines the semantics of our type logic and establishes soundness of the Hoare rules. Sec. 7
presents the machine-checked Lean mechanisation. Sec. 8 discusses related work. The appendices
cover additional features and extensions.

2   IMPROVEMENTS TO TYPE-SAFETY VIA HOARE LOGIC
The following four sections introduce four novel ingredients of our proposal. Case specifications
(Sec. 2.1) give path-sensitivity. Separation types (Sec. 2.2) provide the expressive power needed
for flow-sensitive heap reasoning. The Err/Abrt error hierarchy (Sec. 2.3) makes error coverage
explicit, verifiable and customisable to the precision required by the caller. Type predicates (Sec. 2.4)
Type Safety via Hoare Logic with Separation and Pure Types                                           5


capture data structure invariants. Although independent contributions, all four compose coherently,
as we summarise at the end of Sec. 2.

2.1    Semantic Subtyping, Path-Sensitivity and Case Specifications
Semantic-based subtyping interprets each type t as a set of values, and defines subtyping t1 <:t2
via set containment Set(t1 )⊆Set(t2 ). This lets types be composed using a Boolean algebra:
                                      𝑡 := 𝑡 ∨ 𝑡 | 𝑡 ∧ 𝑡 | ¬𝑡 | ...
    Consider the ML-style function below. ML’s type system rejects it because unification fails when
it tries to combine the Int output of one branch with the Str output of the other:
      inc_if_int ( x ) = match x of { Int -> x +1;
                                      _   -> " Not supported !" }
  Semantic subtyping resolves this: one valid formulation assigns the output type as Int∨Str,
yielding the following type signature:
      inc_if_int :     Any → Int ∨ Str
   The most precise set-theoretic type is an intersection of arrow types, (Int→Int) ∧ (¬Int → Str)
[6], which our case specification below directly mirrors:
      inc_if_int : case [x] { x: Int           ens [r] r: Int ;
                              x:¬Int           ens [r] r: Str }
  Case specifications differ from intersection types in one crucial respect: disjointness is a verified
obligation, not a programmer convention. The type checker rejects any case specification whose
guards overlap, making the specification exhaustive and non-redundant by construction. A pro-
grammer writing the intersection type (Int→Int) ∧ (Any→Int ∨ Str) receives no such check:
the overlapping cases pass silently. This enforcement is what makes the otherwise clause and the
Abrt discipline of Sec. 2.3 well-defined.

2.2    Flow-Sensitivity and Separation Types
Many languages support pass-by-value-result parameters (e.g. inout parameters in Swift) that
allow variable arguments to be mutated by a method call. Dynamically-typed languages go further,
allowing the type of a variable to change arbitrarily, as follows:
        inc_transform ( inout x) = x := str_of_int (x +1)
   One might suggest Int∨Str → () as the type signature, but this is not type-safe. Standard type
systems (including Swift’s) are flow-insensitive, so the one type assigned to x must serve both as
the Int argument to (+) and as the Str value finally stored, and Int∨Str satisfies neither.
   To type such a program, we make the mutation explicit in the heap: the mutable parameter x is
modelled as a heap cell of type Ref(_), dereferenced by the body (!x), which writes back the string
form via a strong update.
        inc_transform (x) = let v = str_of_int (! x +1) in update (x ,v)
This write changes the cell’s type, not merely its value: x points to a Ref(Int) on entry and to a
Ref(Str) on exit, so a type system must support a flow-sensitive type change on a heap location.
Separation types capture exactly this, recording the owned cell’s type before and after the call:
      inc_transform : req [x] x↦→ Ref ( Int ) ens [_] x↦→ Ref ( Str )
The precondition owns x↦→Ref(Int) and the postcondition the strongly-updated x↦→Ref(Str), a
change that neither a single flow-insensitive type for x nor a plain Ref(Int∨Str) can express.
6                                                                                     Li, Foo, Ta, and Chin


   Where existing type systems stand. As the introduction’s comparison showed, existing systems
handle such type-changing updates only partially, if at all: none soundly tracks the stored type of a
heap location as it changes under aliasing. Closing this gap requires accounting for must-aliases
among heap locations. Linear (uniqueness) types sidestep it by guaranteeing a single reference
per location and no aliases at all, but thereby rule out programs where aliasing is intentional.
We instead introduce a separation type, written x↦→T, which carries full ownership of the heap
location at x while still tracking must-aliases (references guaranteed to point to the same location)
explicitly. Full ownership is what makes a strong update sound: every alias of an owned location is
a known must-alias, so all aliases observe the new type consistently. By contrast, pure types permit
arbitrary (unknown) aliasing and so forbid type mutation.
  Why must-aliasing matters: a preview. We first highlight the key feature that distinguishes
separation types from uniqueness types. Consider the swap function:
     swap (x , y ) = let v1 =! x in let v2 =! y in
                     update (x , v2 ); update (y , v1 )

The interesting case is when x and y must-alias the same location, making the swap a no-op:
uniqueness types cannot express it (they forbid aliasing), whereas separation types capture it via
the singleton y:{x} (meaning y=x). We give the full case specification below.
  Formal specifications. Separation types yield stronger, flow-sensitive specifications for the core
heap operations. We also introduce spatial conjunction ∗ for pairs of disjoint heap locations:
    mkRef : req [ x ] x:Any ens [r] r↦→ Ref (x)
    (!) : ∀T :AnyP ,Q:Any. case [m] { m: Ref (T) ens [r] r:T;
                                      m↦→ Ref (Q) ens [r] m↦→ Ref (Q) ∧ r:Q}
    update : ∀T :AnyP . case [m ,v] { m: Ref (T) ∧ v:T ens [r] r :() ;
                                      m↦→ Ref (_) ∧ v:Any ens [r] m↦→ Ref (v) ∧ r :() }

   Here Any is a top type, split into the pure types AnyP (arbitrary aliasing) and the separation types
AnyS (exclusive heap ownership, covering mutable data).
   Throughout, lowercase identifiers (x, y, u, v) denote value variables and single uppercase letters
(T, R, A) type variables. Accordingly, x:t is used in two ways: for a value variable x, it asserts x
has type t; for a type variable T, the bounded quantifier ∀T:R means T ranges over subtypes of R;
subtyping is otherwise written T<:R. Thus x:Ref(T) is a pure type assertion on a value. A reference
Ref(T) stores a value of type T; Ref(u) (as in x↦→Ref(u)) stores the specific value u, the singleton
Ref({u}), and x↦→Ref(y) asserts heap ownership where y is a type or singleton {v}. Predicate
membership x:P(. . .) uses the same colon: x is a value of the (inductive) predicate P(. . .) (Sec. 2.4).
   The precondition of mkRef is maximally weak (Any covers both pure and separation types), its
postcondition maximally strong. The two-case structure of update reflects the pure vs. separa-
tion distinction, made precise by Definitions 2.1 and 2.2 below: a pure m:Ref(T) permits only a
type-consistent write, returning () unchanged; owned m↦→Ref(_) permits type mutation, yielding
m↦→Ref(v). A single specification serves both regimes, the case guard selecting which applies.

   Definition 2.1 (Type-Consistent Mutation for Pure Types). A write update(x,v) to a location
x:Ref(T) in pre-state ∆ is type-consistent if v:T.

For pure types, changing the stored type (T to T2 ≠T) is disallowed: arbitrary aliasing would let
other references to x observe an inconsistent type.
Type Safety via Hoare Logic with Separation and Pure Types                                                7


   Definition 2.2 (Type Mutation for Separation Types). Type mutation at a location x↦→Ref(T)
is the replacement of the stored type T with a distinct type T2 , effected by a write update(x, v) where
v:T2 . The postcondition reflects the updated type: x↦→Ref(T2 ).
This is sound because full ownership rules out any unknown alias of x in the pure heap.
  Irreversible weakening. Separation and pure types occupy two disjoint heap partitions. The
separation heap gives exclusive ownership x↦→T (full rights to read, mutate the type, and track
must-aliases); the pure heap gives only shared access x:T (no ownership, and type-consistent writes
only). Accordingly, a separation type x↦→T for heap memory is not a subtype of the corresponding
pure type x:T: the two are mutually disjoint, connected only by a one-way, irreversible weakening,
not by subtyping:
                               x↦→T ∧ T <: A ∧ A <: AnyP     ⇒𝑤𝑒𝑎𝑘𝑒𝑛    x:A
   Since this weakening is the sole crossing rule, a separation type may nest pure components but
never the reverse, so well-formedness holds by construction, with no separate check required. Once
ownership is surrendered via weakening, the right to type-mutate is permanently lost: r↦→Ref(T)
(from mkRef) can be weakened to r : Ref(T) when type mutation is no longer required. The reverse
is disallowed, since other aliases may already exist. This relationship is captured by the equivalences
below ( ⇔ is semantic equivalence); it differs for primitive and non-primitive types:
                 for a primitive p (e.g. Int, Str):              x↦→p ⇔ x : p
                 for a non-primitive heap T (e.g. Ref(. . .)):   x↦→T ∧ x : T ⇔ false
   Must-aliasing: the swap example. We can now give the case specification for swap:
    swap :∀T :AnyP ,A ,B:Any. case [x ,y] {
       x : Ref ( T ) ∧ y: Ref (T) ens [r] r :() ;
       x↦→ Ref ( A ) * y↦→ Ref (B) ens [r] x↦→ Ref (B) * y↦→ Ref (A) ∧ r :() ;
       x↦→ Ref ( A ) ∧ y :{ x} ens [r] x↦→ Ref (A ) ∧ r :() }
   The first case handles flow-insensitive pure-type access; the second, two distinct locations
(disjoint heap ownership) whose values are swapped. The third uses the singleton type y:{x} to
express that y must-alias x (i.e. y=x). Encoding the alias as a type rather than a separate equation
keeps must-alias reasoning within the type language, and swapping is then a no-op preserving the
separation type. This case is inexpressible with uniqueness types, confirming separation types are
strictly more expressive (see Appendix D.1).
   Remark 2.1 (Singleton types and aliasing). A singleton type {z} denotes the one-element set
{z} — the most precise type for a value, naming its exact witness. A singleton is itself pure ({z} <: AnyP )
— value equality needs no ownership, so a bare singleton never claims the heap; to combine the witness
with ownership, it appears as an owned cell’s exact content, x↦→Ref({z}). Aliasing consequences
follow the assertion’s precision: (i) x↦→Ref({z}) — full ownership, exact content named, no unknown
aliases, type mutation sound; (ii) x:{z} — witness known but pure heap, unknown aliases may mutate
independently, type mutation unsound; (iii) x:A with A <: AnyP — no witness named, arbitrary unknown
aliases, type mutation unsound. Yet (ii) is strictly more informative than (iii) — from x:{z} the verifier
knows x=z, supporting equality and must-alias reasoning.
   Remark 2.2 (Mixed scenarios via weakening). The spec omits mixed cases where one pa-
rameter is a pure type and the other a separation type, specifically: x:Ref(A) ∧ y↦→Ref(B) and
x↦→Ref(A) ∧ y:Ref(B). A caller willing to surrender ownership can apply the weakening lemma
to reduce to Case 1; otherwise the implicit otherwise clause applies, yielding Abrt.
8                                                                                     Li, Foo, Ta, and Chin


2.3   A Disciplined Error Hierarchy
We begin with a concrete example that motivates our error hierarchy before presenting it in full.
Consider the head function on lists:
         head : ∀T . List (T) → T
   Two distinct kinds of failure can arise. If head is called with the wrong argument type (say
an Int), the type checker can detect this statically and flag an Abrt error: a distinguished value
representing compile-time type-errors that must never appear in the postcondition of a well-typed
program. The program is not well-typed and must not be allowed to run.
   If head is called with a Nil value (the correct type, but an empty list), a runtime error occurs:
the program has gone wrong in a way that was not caught at compile time, and the result is best
represented by an Err value that propagates through subsequent computations.
   Traditional type systems (e.g. OCaml, Scala) conflate runtime errors with the bottom type ⊥,
treating them as outside the type system entirely. This conflation loses precision: ⊥ denotes non-
termination or unreachability: a function with postcondition r:⊥ is one that never returns. A
runtime error, by contrast, is a propagatable value that flows into subsequent computations. By
internalising runtime errors as the first-class value Err in our type lattice (Figure 1), our framework
can track where errors arise and propagate, something ⊥-based treatments cannot express.

  Three type specifications for head. Our framework allows the programmer to choose the level of
error specification appropriate for their context:
      head : ∀T . req [x] x: List (T) ens [r] r:T∨Err
      head : ∀T . case [x] { x: Cons (T ,_) ens [r] r:T;
                              x: Nil          ens [r] r: Err }
      head : ∀T . req [x] x: Cons (T ,_) ens [r] r:T
   The first two specifications treat head(Nil) as a
tracked runtime error; the third eliminates it as a                               ⊤
compile-time error. The first and second are compa-
rable: the second (case form) is strictly more precise                   Any
than the first, since on a Cons input it guarantees the
result is a T (never Err), whereas the first permits Err
                                                                  AnyP AnyS             Exc
on every input. The second and third, by contrast, are
not comparable in terms of strength: they make differ-
ent trade-offs between permissiveness and static guar-      Err                                        Abrt
antees (the case form tolerates Nil as a recoverable
Err, while the third rules Nil out as a compile-time                    UnExc          ChExc
error, and Err and Abrt are unrelated). Together, the
three specifications illustrate the range of expressive-               ⊥sys.err
ness available in our framework, a range that eludes
most traditional type systems without dependent types
or type qualifiers.                                                               ⊥

                                                                      Fig. 1. Lattice of Types
  Error hierarchy. Just above the empty type ⊥, the
node ⊥sys.err denotes runtime system errors (such as
out-of-memory or hardware faults) that lie beyond the
control of our type framework, and which we accordingly set aside in the discussion that follows.
The three error types we design are:
Type Safety via Hoare Logic with Separation and Pure Types                                             9


  • Err: a pure error value that may be passed as an argument to method calls. Subtypes include
    unDef (for uninitialised values) and null (for null pointer dereferences). These are tolerated
    in programs and do not trigger compile-time errors until they are actually used.
  • Exc: an exception, further split into ChExc (checked; must be tracked explicitly by our type
    system) and UnExc (unchecked; treated as a subtype of both AnyS and AnyP and may be omitted
    from specifications). Exception handling is discussed in Appendix C.
  • Abrt (and ⊤): a compile-time type error. Our type-safety verification framework must prove
    Abrt and ⊤ unreachable for any well-typed program.
  Consider map:
      map (f , xs ) = match xs of { Nil -> Nil ;
                                    Cons (y , ys ) -> Cons (f(y) , map (f , ys )) }
  Its type specification with case specs is:
      map : ∀A , B : AnyP . case [f , xs ] {
             f : Any ∧ xs : Nil ens [r] r: Nil ;
             f : A→B ∧ xs :Cons(A, List(A)) ens [r] r:Cons(B, List(B));
             _ ens [r] r:⊤ }
   The first two cases capture valid type specifications; the otherwise clause _ triggers a compile-
time error if the inputs f and xs do not match either case. Here _ is syntactic sugar for the negation of
all preceding guards. Explicitly specifying ⊤ or Abrt flags compile-time type errors. The disjointness
of case guards (Sec. 2.1) is essential here: an input satisfying multiple guards would induce an
intersection type, and without disjointness the verifier would need to perform a proof search to
determine which case applies. Enforced disjointness eliminates this need for proof search.
   An Err tolerated, then captured as Abrt: reading an uninitialised value. An Err is tolerated (it may
flow through the program freely) and becomes a captured Abrt only where a function demands its
validity. Consider an uninitialised memory slot, whose default contents are the zero word 0x0. We
type this as an Err (its unDef subtype), disjoint from every valid type:
     0 x0 : Err
As an Err, 0x0 is tolerated: bit-for-bit an ordinary word, it may be bound, copied, and passed
around freely. An Err faults only where validity is demanded, i.e. when it reaches a function whose
precondition requires a valid argument, such as use:
     use : req [ v ] v: Valid ens [_] ()
             def
Here Valid = Any ∧ ¬Err denotes the valid (non-error) types. The call use(0x0) cannot satisfy
v:Valid, so it is ill-typed and captured as Abrt, ruled out by our well-typedness requirement that
well-typed programs never abort. The same 0x0 is thus a harmless Err while in flight, but an Abrt
the instant it reaches use; keeping the two distinct is what rules the bug out by typing.
   Remark 2.3 (The ⊥ type and non-termination). Following standard convention, ⊥ denotes the
empty set of values and is a subtype of every type. As a postcondition, r:⊥ asserts that no value is ever
returned – the computation diverges. As a precondition, x:⊥ asserts that the input never exist, that is
unreachable false. Crucially, in our framework ⊥ is reserved for these two standard roles. Err is not
conflated with ⊥, as they are internalised as first-class values of the type Err, enabling precise error
tracking that ⊥-based treatments cannot provide. The fatal-error type Abrt is likewise distinct from ⊥,
and in a different way. ⊥ is uninhabited and is a legitimate specification outcome (divergence or an
unreachable input). By contrast, Abrt is an inhabited distinguished value marking a compile-time type
error; it is never a desired outcome and must be proven unreachable in any well-typed program. Since
10                                                                                   Li, Foo, Ta, and Chin


⊥ is a subtype of every type, we do formally have ⊥ <: Abrt; but this does not weaken the guarantee,
because ⊥ is uninhabited and so contributes no actual value to Abrt. As termination is undecidable,
the guarantee that well-typed programs never abort is accordingly a partial-correctness one: it ensures
that whenever a well-typed program does produce an outcome, that outcome is never Abrt. It does
not account for potential non-termination. For example, (req[x] x : Any ens[r] r:⊥) is the correct
specification of a diverging function that never returns.
   Remark 2.4 (UnExc and ⊥). UnExc should not be conflated with ⊥, since UnExc is inhabited (it
classifies untracked but raised exceptions), whereas ⊥ has no inhabitants and denotes non-termination.

2.4    Pure and Separation Type Predicates
Modern functional languages, such as ML and Haskell, support algebraic data types (ADTs). Four
simple examples are shown below.
      data   Color      =   Red    |   Black
      data   Nat        =   Zero   |   Succ ( Nat )
      data   List ( T ) =   Nil    |   Cons (T , List (T))
      data   Tree ( T ) =   Leaf   |   Node ( Color ,T , Tree (T) , Tree (T))
   We propose using type predicates to model algebraic data types. Like types, type predicates can
be recursive, but are strictly more expressive. Each ADT can be encoded as a pure type predicate,
as shown below.
      pred   x : List (T) = x: Nil ∨ ∃ r. x: Cons (T ,r)∧r: List (T)
      pred   n : Nat      = n: Zero ∨ ∃ r. n: Succ (r)∧r: Nat
      pred   x : Color    = x: Red ∨ x: Black
      pred   x : Tree (T) = x: Leaf ∨ ∃ c ,lt , rt . x: Node (c ,T ,lt , rt )
                                ∧c: Color∧lt : Tree (T)∧rt : Tree (T)
   Type predicates are interpreted inductively as least fixed points; their recursive unfolding is
assumed to terminate (well-foundedness), a condition stated precisely in Remark 3.1 at the end of
this section. (We assume here a strict language. If a lazy language is used, we will need to make use
of an interpretation via greatest fixed points.)
   To capture data structures with stronger invariant properties, Haskell and OCaml also support a
restricted form of dependent types known as Generalised Algebraic Data Types (GADTs). Here,
their type parameters may be separately instantiated, depending on the data constructors used, as
illustrated by the red/black balanced tree below.
      data RBTree :: Color → Nat → * → * where
        Leaf      :: RBTree Black Zero a
        RedNode   :: RBTree Black h a → a
                     → RBTree Black h a → RBTree Red h a
        BlackNode :: RBTree cl h a → a
                     → RBTree cr h a → RBTree Black ( Succ h) a
  Rather than adopting GADT data types, we propose that our framework use type predicates for
capturing data structures with strong invariant properties. Two examples are shown below.
      pred x : List (T ,s) = x: Nil ∧ s: Zero
             ∨ ∃ r ,m. x: Cons (T ,r)∧r: List (T ,m)∧s: Succ (m)
      pred x : RBTree (T ,c ,h) = x: Leaf∧c: Black∧h: Zero
             ∨ ∃ h1 ,lt , rt . x: Node (c ,T ,lt , rt )∧lt : RBTree (T ,_ , h1 )
                              ∧rt : RBTree (T ,_ , h1 )∧c: Black∧h: Succ ( h1 )
Type Safety via Hoare Logic with Separation and Pure Types                                             11


             ∨ ∃ r ,lt , rt . x: Node (c ,T ,lt , rt )∧lt : RBTree (T , Black ,h)
                              ∧rt : RBTree (T , Black ,h)∧c: Red
   The predicate x:List(T, s) uses an extra parameter s to track the length of the list. The predicate
x:RBTree(T, c, h) uses c to denote the colour of the red/black tree and h to capture its black-height,
and enforces that the black-height is always balanced. These richer predicates are related to their
base-type counterparts by the following lemmas.
     lemma ∀x, T. (∃n. x: List (T ,n))          ⇔    x: List (T)
     lemma ∀x, T, c, h. x: RBTree (T ,c ,h)     ⇒    x: Tree (T)

  Stable pure and separation types. With length-indexed predicates in hand, we now define stability
for pure types (Definition 3.1) and separation types (Definition 3.2). Stability of type predicates
themselves is deferred to Sec. 3.2, where the necessary formal vocabulary is introduced.
   Definition 2.3 (Stable Pure Type). A pure type t is stable under heap mutation if it cannot be
invalidated by any type-consistent mutation (Definition 2.1). Formally, for any heaps h, h′ related
by a type-consistent mutation with respect to the current pre-state ∆, s, h|=x : t implies s, h′ |=x : t.
Singleton types y:{x} (asserting y=x) [8, 32] are trivially stable: they live in the pure constraint 𝜋 and
express only an equality between program or logical variables (including existentially quantified ∃v∗
in ∆). This fact is independent of the heap and therefore unaffected by any heap mutation.
 Pure data types in strongly typed languages, like OCaml, are designed to be stable by default.
Moreover, GADTs are also stable with the use of immutable constructors.
   Definition 2.4 (Stable Separation Type). A separation type x↦→T is stable if the content type
T is a stable pure type. Full ownership of x is guaranteed by the separation type discipline itself, so
the non-trivial requirement is on the content type T. For example, x↦→Ref(Int∨Str) is stable because
Int∨Str is stable. By contrast, x↦→Ref(T2 ) may not be stable if T2 can be invalidated by aliased writes
to its fields. Unlike a stable pure type, a stable separation type additionally permits type mutation of
its content via an explicit update. This is safe because full ownership ensures no pure-heap alias to x
exists and every must-alias observes the updated type consistently.
  It is also possible to support richer data structures via separation type predicates which may
capture heap nodes exclusively owned by the predicates, such as x↦→MList(T):
     data MList ( T) = Nil | Cons (T , Ref ( MList (T)))
     pred x↦→MList(T) = x: Nil ∨ ∃ 𝑟, 𝑟 1 . x↦→Cons(T, r) ∗ r↦→Ref(r1 ) ∗ r1 ↦→MList(T)
   Such mutable lists can be used to construct fully owned mutable structures, including circular
and doubly-linked lists, a domain well covered by two decades of research in separation logic. In
particular, a pure type x:MList(_) cannot be used to guarantee the construction of such a circular
list: being freely aliasable and owning no cell, it cannot pin down the back-reference that closes
the cycle. This guarantee is attainable only with separation types and predicates, whose exclusive
ownership of the nodes lets the predicate tie the final tail back to an owned cell. We propose to
make these features available within the type system to support greater memory safety.
   Precise definitions of stable pure and separation type predicates, in terms of the formal type
logic, are deferred to Definitions 3.1 and 3.2 in Sec. 3.2, once the required vocabulary – immutable
constructors, heap assertions, ownership – has been formally established.
   The well-foundedness assumption underlying all type predicate definitions is stated formally as
Remark 3.1 in Sec. 3.2, once the formal vocabulary is in place.
   A more detailed comparison of type predicates with GADTs and liquid types is in Section 5.
12                                                                                   Li, Foo, Ta, and Chin


2.5    A Combined Example
We close with a single example exercising all four ingredients at once. Consider rm_head, which
dereferences a heap-allocated list reference, returns the head if non-empty, and Err otherwise:
      rm_head ( m ) = let xs = !m in
         match xs of { Nil -> err ;
                    Cons (y ,_) -> update (m , tail ( xs )); y }
We use the length-indexed predicate List(T, s), where s is a Nat tracking the length, to give a
precise three-case specification. s:Zero means the list is empty; s:Succ(s1 ) means it is non-empty.
      rm_head : ∀ T ,l ,s ,s 1 .
        case [ m ] {
          (* Case 1: pure - type access , possible runtime Err *)
          m : Ref ( l ) ∧ l: List (T) ens [r] r:T ∨ Err ;
          (* Case 2: sep type , empty list , rm_head returns Err *)
          m↦→ Ref ( l ) ∧ l: List (T ,s) ∧ s: Zero ens [r] m↦→ Ref (l) ∧ r: Err ;
          (* Case 3: sep type , non - empty list , flow - sensitive mutation *)
          m↦→ Ref ( l ) ∧ l: List (T ,s) ∧ s: Succ (s 1 ) ens [r] ∃ l 1 . m↦→ Ref (l 1 ) ∧ l 1 :
                List (T ,s 1 ) ∧ r:T }
This specification uses all four ingredients:
      • Case specifications (Sec. 2.1): three disjoint guards: pure-type access, and the empty- and
        non-empty-list separation cases.
      • Separation types (Sec. 2.2): Cases 2 and 3 use m↦→Ref(l) to own the heap location; Case 3’s
        postcondition reflects the flow-sensitive update, with m now pointing to the tail l1.
      • Error typing (Sec. 2.3): Case 1 tolerates a runtime Err via r : T ∨ Err; Case 2 returns Err
        precisely when the list is known empty, not conflating it with ⊥ or an unchecked exception.
      • Type predicates (Sec. 2.4): the length-indexed List(T, s) uses its Nat index s to distinguish
        Zero (empty) from Succ(s1 ) (non-empty), letting the verifier prove Cases 2 and 3 disjoint
        and track the length decrease in Case 3.
   Stability of type predicates. The example also pinpoints where pure-type stability holds and
breaks down. l:List(T, s) is stable: List is built from immutable Cons constructors, so the length
index s, fixed at construction, is observed identically by every alias. By contrast, m:Ref(List(T, s))
is not: any alias can update the Ref to a list of different length s′ , invalidating s. This is why Case
1 uses the weaker m:Ref(List(T)), the length being untrackable through a pure Ref under aliased
mutation. Cases 2 and 3 resolve this by taking full ownership via m↦→Ref(l) ∧ l:List(T, s): with no
pure-heap alias to m, the cell is fully owned, permitting the precise update in Case 3’s postcondition.
TypeHL checks the three cases independently, the separation type being consumed and re-emitted
by the Call rule (Sec. 4) so no ownership is lost across update.

3     CORE LANGUAGE AND A LOGIC FOR TYPES
This section has two parts. The first (Sec. 3.1) presents the syntax of the core language: a small
strict higher-order functional language with immutable constructors and a single mutable heap
type Ref. The second (Sec. 3.2) defines the type logic (the grammar of states, heap assertions, pure
constraints, and type specifications) that Sec. 4 uses to state and verify type-safety properties. The
notation req/ens used informally throughout Sec. 2 is given its formal definition here. The big-step
operational semantics of the core language, against which our soundness result (Sec. 6) is stated, is
given in Sec. E.
Type Safety via Hoare Logic with Separation and Pure Types                                                      13


3.1   Core Language
We consider a strict higher-order functional language with immutable data constructors with
the exception of the Ref type. The key design choices are as follows. To support both static and
dynamic typing, we organise data constructors and primitive types into a subtype lattice with
Any as the supertype of all valid types, covering both user-defined and primitive types. Each let
binding introduces an immutable variable. Functions and data constructors are always fully applied.
Function definitions and lambda abstractions are always given explicit type specifications. We
also provide an alternative style for function specifications, 𝜆 x∗ r . Φ[r], so that case and ens
constructs do not need to explicitly track the parameters/result. For simplicity, we omit inout
parameters and exception-handling constructs.
   The syntax is summarised in Figure 2. We briefly explain each syntactic category. A program
(Prog) is a sequence of definitions. Each definition (Defn) binds a function name to a body expression
together with a type specification 𝜆 x∗ r . Φ. The full expression language (Full) includes the standard
constructs (values, let-bindings, constructor applications, function calls, type casts (t)e, and match)
and is the language the programmer writes. The core expression language (Core) is the normalised
form used for Hoare-style reasoning: constructor arguments and function arguments are always
simple variables, and the match scrutinee is always a variable. Base types (Base) include singleton
types, primitive types, constructor types, predicate types, and the special types Err, Abrt, Any,
⊥, and ⊤. Types (Type) extend base types with separation types (↦→base), function types, and
Boolean combinations ∧, ∨, and ¬. The separation type ↦→base is a type in its own right. A variable
x of this type would be written x:↦→base, but for simplicity we omit the colon for separation types
and write x↦→base. Patterns (Pattern) mirror types and are used in match. Note that ⊤ and ⊥ are
excluded from patterns since the former trivially holds and testing for the latter is equivalent to
the halting problem.


       (Prog)      prog   ::=   def1 ; · · · ; defn
       (Defn)       def   ::=   f x1 · · ·xn = e where f::𝜆 x1 · · ·xn r . Φ[r]
       (Full)         e   ::=   val | let x:t = e1 in e2 | C(e1 . . .en ) | (f e1 · · ·en ) | (t) e
                                 | match e {p1 →e1 | · · · |pn →en }
       (Value)      val   ::=   x | c | err | abrt | 𝜆 x∗ . e :: 𝜆 x∗ r . Φ[r]
       (Core)         e   ::=   val | let x = e1 in e2 | C(x1 . . .xn ) | (f x1 · · ·xn ) | (t) x
                                 | match x {p1 →e1 | · · · |pn →en }
       (Base)      base   ::=   {x} | {c} | Bool | Int | Str | Ref(· · · ) | · · · | Err | Abrt | Any | ⊥ | ⊤
                                 | C(t1 . . .tn ) | pred(t1 . . .tn )
       (Type)        t    ::=   base | ↦→base | t1 →t2 | t1 ∧t2 | t1 ∨t2 | ¬t
       (Pattern)     p    ::=   c | Bool | Int | Str | · · · | Err | Abrt | Any | C(x1 . . .xn ) | pred(_)
                                 | _→_ | p1 ∧p2 | p1 ∨p2 | ¬p | _
                                c ∈ B∪Z∪···                           x, f, r ∈ vars

                          Fig. 2. Syntax of Full and Core Language with Types



  The Full ⇔ Core preprocessing works by inserting eager casts to Any at every constructor
argument, function argument, and match scrutinee. Any is the supertype of all normal runtime
types but does not include Abrt or ChExc. The casts are the propagation points. If any sub-expression
produces Abrt or ChExc, the cast short-circuits and propagates the exceptional value outward, so
the core let construct never needs to handle these cases directly. The preprocessing rules are:
14                                                                                             Li, Foo, Ta, and Chin



                      C(e1, · · · , en )    ⇔ let {xi :Any=ei }ni=1 in C(x1, · · · , xn )
                          f e1 · · · en     ⇔ let {xi :Any=ei }ni=1 in f x1 · · · xn
                      match e {. . .}       ⇔ let x:Any = e in match x {. . .}
                  let x:t = e1 in e2        ⇔ let x = (t) e1 in match x {Abrt→x | _ →e2 }
                                 (t) e      ⇔ let x = e in (let x1 = (t) x in x1 )
  Pattern overlap and desugaring. For ease of programming, we allow the patterns in each match
construct to overlap, relying on top-down processing to give an unambiguous semantics. Before
Hoare-style reasoning begins, overlapping patterns are desugared into disjoint form. For example,
match x {p1 →e1 | p2 →e2 | p3 →e3 } becomes match x {p1 →e1 | p2 ∧¬(p1 )→e2 | p3 ∧¬(p1 ∨p2 )→e3 }.
The Hoare rules can then deal with complex patterns formed from ∧, ∨, and ¬. To support efficient
runtime execution, complex type patterns are further translated to simpler patterns using the rules
below:
            match x {. . . | p1 ∨p2 → e | ..}      ⇔ match x {. . . | p1 → e | p2 → e | ..}
            match x {. . . | p1 ∧p2 →e | ..}       ⇔ match x {. . . | p1 →match x {p2 → e | ..} | ..}
            match x {. . . | ¬ p → e | ..}         ⇔ match x {. . . | p → match x {..} | _ → e}

3.2   Type Logic and Specifications
We now define the type logic that underpins the Hoare rules of Sec. 4. The central object is a
type state ∆, which pairs a heap assertion 𝜎 capturing ownership of heap locations with a pure
constraint 𝜋 capturing type and equality facts about variables. The grammar is given in Figure 3.

                  (State) ∆ ::=
                                     Ô𝑛       ∗
                                       𝑖=1 ∃𝑣 ·𝜎𝑖 ∧𝜋𝑖
                  (Heap) 𝜎 ::= emp | 𝑥↦→𝑡 | 𝜎1 ∗ 𝜎2
                  (Pure) 𝜋 ::= 𝑥:𝑡 | 𝑥 1 =𝑥 2 | 𝜋 1 ∧𝜋2 | 𝜋1 ∨𝜋2 | ¬𝜋 | ∃𝑣 ∗ ·𝜋
                  (Spec) Φ ::= ens[r] ∆ | case {∆1 Φ1 ; · · ·; ∆n Φn } | ∀𝑥 ∗ ·Φ

                                           Fig. 3. Type Logic Specification

  Each syntactic category plays a distinct role. A state ∆ is a disjunction of existentially quantified
heap-pure pairs; disjunction arises naturally from path-sensitive case analysis. A heap assertion
𝜎 is either empty (emp), a separation type x↦→t asserting full ownership of the location at x
with content type t, or a separating conjunction 𝜎1 ∗ 𝜎2 asserting disjoint ownership. A pure
constraint 𝜋 records type memberships x:t, equalities, and Boolean combinations thereof; it does
not assert ownership. Note that we support ∨, ∧, and ¬ in both the type and assertion languages,
with the union-type equivalence r:T1 ∨T2 ⇔ r:T1 ∨r:T2 holding as a derived rule. A specification
Φ is either a simple postcondition ens[r] ∆, a case specification with pairwise-disjoint guards
(∀i≠j. ∆i ∧∆j =false), or a universally quantified specification. The shorthand req ∆1 ens[r] ∆2
abbreviates case {∆1 ⇒ ens[r] ∆2 }, formalising the notation used throughout Sec. 2.
  For completeness, every case specification is implicitly extended with an otherwise clause
(_ ⇒ ens[r] r:⊤). This clause flags any input not covered by the stated cases as a compile-time
Abrt error. Its postcondition r:⊤ signals this because ⊤, unlike Any, admits Abrt values. This is
consistent with the disjointness discipline of Sec. 2.1: because the stated guards are pairwise disjoint,
the otherwise clause is well-defined and covers precisely the remaining inputs.
  Figure 3 establishes the vocabulary we now need: immutable constructors (types built by the
Base grammar that do not involve ↦→), pure sub-components (occurrences of 𝜋 in a state), and
ownership (heap assertions 𝜎). With these in hand, we can give the formal definitions of stable
type predicates that were deferred from Sec. 2.4.
Type Safety via Hoare Logic with Separation and Pure Types                                             15


  Definition 3.1 (Stable Pure Type Predicate). A pure type predicate x : P(v∗ ) is stable if (i) its
unfolding uses only pure types and immutable constructors (Base terms not involving ↦→), and (ii)
every Ref(T′ ) in the unfolding has T′ a stable pure type. Stability of recursive occurrences follows from
these two conditions by structural induction on the unfolding.
  A further refinement is needed for separation type predicates, since they may contain pure
sub-components that remain exposed to aliased mutation even though the separation part itself is
protected by heap assertion 𝜎. These pure sub-components must therefore themselves be stable.
   Definition 3.2 (Stable Separation Type Predicate). A separation type predicate x↦→P(v∗ )
is well-formed and stable if: (i) full ownership of x is maintained, guaranteed automatically by the
heap assertion x↦→ in Figure 3; and (ii) every pure sub-component in the unfolding of P is stable: bare
pure sub-components y:T must be stable pure types, and pure type predicate sub-components y:Q(v∗ )
must be stable pure type predicates in the sense of Definition 3.1. Unlike pure predicates, a stable
separation predicate additionally permits type mutation: the predicate may be updated to x↦→P′ (v∗ )
via an explicit update, tracked in the postcondition. Such an update is allowed provided the updated
predicate also satisfies conditions (i) and (ii).
  Definitions 3.1 and 3.2 require well-founded predicate unfoldings, as does Definition 2.3 for pure
types appearing inside them. We make this assumption explicit.
   Remark 3.1 (Well-foundedness and co-induction). As is standard in Hoare logic for strict
(eager) languages, all type predicates, both pure and separation, are assumed to be well-founded:
their recursive unfolding always terminates. For lazy languages, this assumption must be relaxed via
co-inductive reasoning. Extending our framework to lazy languages via co-inductive type predicates is
a direction for future work.
  The ⊢∧ operator, used in the Hoare rules of Figure 4, is a special conjunction that performs case
analysis on both separation and pure types. It refines a state by a pure constraint and, when heap
ownership is present, extracts a residual frame via bi-abductive entailment. This residual frame lets
the Frame rule of Sec. 4.1 thread ownership through function calls. We give its precise definition
where it is used, in Sec. 4.

4     HOARE LOGIC RULES FOR TYPE-SAFETY
This section presents the forward Hoare rules that constitute the core of our type-safety verification
framework. Sec. 4.1 introduces the two structural rules (𝐶𝑜𝑛𝑠𝑒𝑞 and 𝐹𝑟𝑎𝑚𝑒) and explains how a
type specification is composed with a program state via the (;) operator. Sec. 4.2 presents the rules
for each expression form. Sec. 4.3 gives a worked example showing how the rules interact.

4.1    Structural Rules and Specification Composition
We present a forward-style Hoare rule of the form { ∆pre } e { ens[r] ∆post }: given an input type
state ∆pre , the rule computes the strongest post-state ∆post resulting from evaluating e, binding
the result and its type to r. Two structural rules apply to every expression form. 𝐶𝑜𝑛𝑠𝑒𝑞 allows
the pre-state to be weakened and the post-state to be strengthened via entailment (⊢ denotes
intuitionistic implication). 𝐹𝑟𝑎𝑚𝑒 allows a disjoint heap context ∆ to be threaded through any
expression unchanged, provided the expression does not touch the locations asserted in ∆; this is
the separation logic frame rule lifted to our type logic.

       ∆1 ⊢ ∆3   { ∆3 } 𝑒 { ens[r] ∆4 } ∆4 ⊢ ∆2                     { ∆1 } 𝑒 { ens[r] ∆2 }
                                                𝐶𝑜𝑛𝑠𝑒𝑞                                         𝐹𝑟𝑎𝑚𝑒
                 { ∆1 } e { ens[r] ∆2 }                         { ∆1 ∗ ∆ } e { ens[r] ∆2 ∗ ∆ }
16                                                                                                Li, Foo, Ta, and Chin


   Specification composition. The Hoare rules for function calls rely on a type specification being
provided for each method, using f::𝜆 x∗ r . Φ. The specification must be in case-spec form and
is merged with the pre-state ∆ via the operator ∆ ; Φ, defined by the two reduction rules below.
Intuitively, ∆ ; Φ applies the specification Φ in the context of the current state ∆. For each case
guard ∆i , the operator uses ⊢∧ (Definition 4.1) to check how much of ∆ satisfies ∆i , and threads the
residual frame into that branch’s post-state. A branch whose guard is inconsistent with ∆ drops out
as vacuous. An Abrt outcome arises in one of two ways: where a branch’s postcondition explicitly
yields it, or from the implicit otherwise clause (Sec. 3.2) covering inputs that match no stated guard.

               ∆ ; case {∆1 Φ1 ; · · · ; ∆n Φn }   ⇒ ((∆ ⊢∧ ∆1 ) ; Φ1 ) ∨ · · · ∨ ((∆ ⊢∧ ∆n ) ; Φn )
                                ∆ ; ens[r] ∆2      ⇒ ∆ ∗ ∆2
  We introduce a special conjunction ⊢∧ that performs case analysis on both separation and pure
types, defined as follows.
   Definition 4.1 (Case conjunction ⊢∧). On pure types, ⊢∧ coincides with standard conjunction:
(∆ ⊢∧ 𝜋) ⇔ (∆ ∧ 𝜋). In the presence of a separation type 𝜎, it performs bi-abductive heap entailment
to extract a residual frame ∆s together with an abduced pure precondition 𝜋 0 :
                                              ∆ ∧ 𝜋 0 ⊢ 𝜎 ⇝ ∆𝑠
                                         ∆ ⊢∧ 𝜎 ∧ 𝜋 ⇔ ∆𝑠 ∧ 𝜋 ∧ 𝜋 0
   Example: specification composition. Consider a call (f x) where f has specification
Φ ≡ case[x] {x : Int ens[r] r : Int; x : ¬Int ens[r] r : Abrt}. If the pre-state is ∆ ≡ x:Int, then
∆; Φ yields x:Int∧r:Int (the first branch matches, the second is vacuous). If instead ∆ ≡ x:Any,
then ∆; Φ yields (x : Int∧r : Int) ∨ (x : (Any∧¬Int)∧r : Abrt), signalling a possible Abrt from
inputs not known to be Int.

4.2   Rules for Expression Forms
The remaining rules in Figure 4 handle each expression form in the core language. We describe
each rule in turn.

                                                                                      Ó
                   fresh r                              fresh r,𝑇1 ..𝑇𝑛 ∆1 ≡(∆ ∧ 𝑛𝑖=1 𝑥𝑖 :𝑇𝑖 )
                                   𝑉 𝑎𝑟                                                                𝐶𝑜𝑛𝑠𝑡𝑟
        { ∆ } 𝑥 { ens[r] ∆∧r:{x} }                   { ∆ } 𝐶 (𝑥 1 ..𝑥𝑛 ) { ens[r] ∆1 ∧r↦→C(T1 ..Tn ) }
               fresh 𝑟      𝑣 ::= 𝑐 | err | abrt                    fresh 𝑟 ∆ ⊢ 𝑓 ::𝜆 𝑥 ∗ 𝑟 . Φ
                                                 𝑉 𝑎𝑙                                              𝐶𝑎𝑙𝑙
                 { ∆ } 𝑣 { ens[r] ∆∧r:ty(v) }                      { ∆ } 𝑓 (𝑥 ∗ ) { ens[r] ∆ ; Φ }
                     fresh 𝑟       ∆1 ≡(∆ ∧ (𝑥:𝑡) ∧ 𝑟 :{𝑥 }) ∨ (∆ ∧ ¬(𝑥:𝑡) ∧ 𝑟 :Abrt)
                                                                                      𝐶𝑎𝑠𝑡
                                         { ∆ } (𝑡) 𝑥 { ens[r] ∆1 }

                           { ∆ } 𝑒 1 { ens[r1 ] ∆1 } { [r1 :=x]∆1 } 𝑒 2 { ens[r] ∆2 }
                                                                                      𝐿𝑒𝑡
                                       { ∆ } let x = e1 in e2 { ens[r] ∆2 }
           { ∆∧(x:p1 ∨x↦→p1 ) } 𝑒 1 { ens[r] ∆1 } · · · { ∆∧(x:pn ∨x↦→pn ) } 𝑒𝑛 { ens[r] ∆n }
                                                                                              𝑀𝑎𝑡𝑐ℎ
                         { ∆ } match x {p1 →e1 | · · · } { ens[r] ni=1 ∆i }
                                                                   Ô

                fresh f        𝑣 ∗ = 𝑣𝑎𝑟𝑠 (∆)−𝑣𝑎𝑟𝑠 (𝑒)∪{𝑥 ∗ } { ∃𝑣 ∗ . Pure(∆) } 𝑒 {↓ Φ}
                                                                                         𝐿𝑎𝑚𝑏𝑑𝑎
                            { ∆ } 𝜆 𝑥 ∗ . 𝑒 :: 𝜆 𝑥 ∗ 𝑟 . Φ { ens[f] ∆∧f::𝜆 x ∗ r . Φ }

                          Fig. 4. Forward Hoare Rules on Expressions for Type Safety
Type Safety via Hoare Logic with Separation and Pure Types                                             17


   Rule commentary. 𝑉 𝑎𝑟 records that the result r equals the variable x via the singleton type r:{x}.
𝐶𝑜𝑛𝑠𝑡𝑟 introduces fresh type variables T1 ..Tn for the field types and produces a separation type
r↦→C(T1 ..Tn ), giving the caller full ownership of the freshly allocated node. 𝑉 𝑎𝑙 handles literal
constants, err, and abrt, each assigned its canonical type via ty(v). 𝐶𝑎𝑙𝑙 applies specification
composition (∆; Φ) as described in Sec. 4.1. 𝐶𝑎𝑠𝑡 produces two branches: one where the cast succeeds
(x:t, result is x itself) and one where it fails ( ¬(x:t), result is Abrt); the preprocessing of Sec. 3.1
ensures Abrt propagates outward. 𝐿𝑒𝑡 threads the post-state of e1 (with r1 substituted by x) into e2 .
𝑀𝑎𝑡𝑐ℎ distributes the pre-state across branches by conjoining each pattern guard, collecting post-
states in disjunctive form. 𝐿𝑎𝑚𝑏𝑑𝑎 uses the auxiliary checking judgement { ∆ } e {↓ Φ} (Figure 5) to
verify that the body e satisfies the supplied specification Φ, then records the closure’s specification
in the post-state.

      { ∆ ∗ ∆1 } 𝑒 {↓ Φ1 } · · · { ∆ ∗ ∆𝑛 } 𝑒 {↓ Φ𝑛 }             { ∆ } 𝑒 { ens[r] ∆1 } ∆1 ⊢ ∆2
                                                      𝑆𝑝𝑒𝑐−𝐶𝑎𝑠𝑒                                 𝑆𝑝𝑒𝑐−𝐸𝑛𝑠
          { ∆ } 𝑒 {↓ case {∆1 Φ1 ; · · · ; ∆n Φn }}                    { ∆ } 𝑒 {↓ ens[r] ∆2 }

                              Fig. 5. Checking Hoare Rules for Type Specification

  The checking judgement { ∆ } e {↓ Φ} is used when processing lambda abstractions (𝐿𝑎𝑚𝑏𝑑𝑎
rule): the specification Φ is supplied as an input, and the rule verifies that the body e satisfies it.
𝑆𝑝𝑒𝑐−𝐶𝑎𝑠𝑒 dispatches on each case guard, prepending the guard ∆i to the pre-state and checking
the body against the corresponding Φi . 𝑆𝑝𝑒𝑐−𝐸𝑛𝑠 checks that the forward post-state ∆1 entails the
declared postcondition ∆2 .
  While we support higher-order functions in our Hoare rules, we currently restrict function
type parameters to flow-insensitive pure types, since we rely on a two-stage pre/post specification
without higher-order constraints. This allows such functions to be treated as pure functions
without any type mutation. Simple parameter variables are designated to carry singleton types (see
Appendix A.1), which reduces the use of quantified type variables.

4.3    Worked Example
To illustrate how the rules interact, we trace the derivation for the inc_transform function from
Sec. 2.2: inc_transform(x) = let v = str_of_int(!x + 1) in update(x, v), whose specification
is req[x] x↦→Ref(Int) ens[r] x↦→Ref(Str)∧r : (). Starting from pre-state ∆ ≡ x↦→Ref(Int), the
𝐿𝑒𝑡 rule sequences the two sub-expressions: the binding dereferences the cell (!x:Int), adds one,
and applies str_of_int to obtain v : Str, each step an intermediate 𝐶𝑎𝑙𝑙 applying the callee’s
specification via (∆; Φ). The body update(x, v) then strong-updates the cell through the 𝐶𝑎𝑙𝑙 rule,
consuming x↦→Ref(Int) and re-emitting x↦→Ref(Str). The resulting post-state x↦→Ref(Str)∧r : ()
matches the declared postcondition, so the specification is verified. The 𝐹𝑟𝑎𝑚𝑒 rule carries any
ownership disjoint from x across the sub-expressions unchanged.

5     TYPE PREDICATES SUBSUME GADTS AND LIQUID TYPES
This section compares our type predicate framework with two closely related approaches: Gener-
alised Algebraic Data Types (GADTs), which encode structural invariants into the type structure,
and liquid types, which refine base types with logical predicates. We show that pure type predicates
subsume both, and that separation type predicates go further still into heap ownership, a dimension
neither GADTs nor liquid types can reach.
   Pure type predicates are closely related to the recursive measures of Kawaguchi et al. [25]. These
measures encode structural invariants as terminating first-order functions over ADTs for use in
18                                                                                       Li, Foo, Ta, and Chin


liquid type refinements. Separation type predicates, in turn, are closely related to the user-defined
inductive heap predicates of separation logic verifiers such as HIP [9]. Our contribution unifies
both within a single type logic, as first-class types subject to the Boolean algebra of types, semantic
subtyping, and a stability analysis distinguishing which predicates survive aliased mutation.
   Table 1 places our framework alongside OCaml, Rust, and Liquid Haskell across nine capabilities
central to this paper; TypeHL is the only one that supports all nine. The rest of this section examines
the two closest approaches, GADTs and liquid types, in detail.

                   Table 1. Feature comparison: ✓ = full, ∼ = partial, × = no support.

                Feature                     TypeHL    OCaml      Rust    Liquid Haskell
                Pure types                    ✓          ✓         ✓            ✓
                GADTs                         ✓          ✓         ×            ✓
                Type Predicates               ✓          ×         ×            ✓
                Separation types              ✓          ×         ∼            ×
                Separation predicates         ✓          ×         ×            ×
                Flow-sensitive types          ✓           ×        ✓            ×
                Must-aliasing                 ✓           ×        ×            ×
                Path-sensitive type specs     ✓           ×        ×            ∼
                Err/Exc/Abrt as types         ✓           ×        ×            ×



5.1   Comparison with GADTs
Type predicates in our framework strictly subsume GADTs in two important respects.
   First, type predicates can express relational index constraints that GADTs cannot. GADT type
parameters can only be equated to specific constructor-determined types; they cannot express
inequalities or arithmetic relations between indices.
   For example, a sorted list predicate with bounds:
      pred x : SortedList (T ,lo , hi ) = x: Nil ∨ ∃ v ,r.
             x : Cons (v ,r)∧v:T∧lo≤v∧v≤hi∧r: SortedList (T ,v , hi )
requires the relational constraint lo≤v≤hi between index values, something GADTs cannot express
without full dependent types (e.g. Agda or Idris). Type predicates in our framework express this
naturally as a logical formula.
   Second, and more practically, type predicates do not require a new algebraic data type for each
new invariant. With GADTs, every new invariant demands a completely new data type definition
with new constructors encoding the invariant into the type structure. In our framework, the same
underlying data representation, the same Cons and Nil constructors, can be given progressively
richer type predicates without any change to the data definition itself:
      pred x : List (T)               = ... (* plain list *)
      pred x : List (T ,n)            = ... (* length - indexed *)
      pred x : SortedList (T ,lo , hi ) = ... (* sorted , with bounds *)
All three predicates describe values built from the same constructors. This separation between
data representation and type invariant means that existing code and data structures need not be
refactored when a stronger invariant is required; only the specification changes. Separation type
predicates (e.g. x↦→List(T)) extend this further to heap ownership and spatial conjunction, which
are entirely outside the scope of GADTs.
Type Safety via Hoare Logic with Separation and Pure Types                                                               19


5.2     Comparison with Liquid Types
Pure type predicates are also closely related to liquid types (as in Liquid Haskell), which refine base
types with logical predicates, for example, {v : Int|v > 0} denotes positive integers. Like liquid
types, our solution via type predicates attaches logical invariants to values as formulas rather
than encoding them into the type structure as GADTs do. Both approaches also allow the same
underlying data representation to carry progressively stronger specifications without changing the
data definition. There are, however, three important differences.
        • Liquid types refine base types with first-order predicates over primitive values (integers,
          booleans); our pure type predicates are recursive, handling arbitrary inductively defined
          data structures such as lists, trees, and GADTs.
        • Liquid types are restricted to decidable refinement logics (typically linear arithmetic) to
          keep SMT solving tractable; our predicates are not confined to a decidable fragment and
          can express arbitrary relational and structural invariants.
        • Liquid types have no counterpart to separation type predicates: there is no notion of heap
          ownership or spatial conjunction in Liquid Haskell2 . Pure type predicates thus generalise
          liquid types from flat refinements over base values to recursive predicates over inductively
          defined structures. Separation type predicates extend this further to heap ownership, co-
          existing with pure types, a dimension outside the scope of liquid types.
   Though type predicates are not constrained to a decidable fragment, it is nevertheless quite easy
to impose a set of restrictions that can guarantee decidability for type-checking. Appendix B.3
outlines restrictions that can be imposed on type predicates to support decidable type-checking.

6     SOUNDNESS OF OUR TYPE SPECIFICATION FRAMEWORK
This section presents the soundness theorem for the Hoare rules of Sec. 4 and establishes the
connection between Hoare triples and standard function types. Sec. 6.1 defines the semantics of
the type logic. Sec. 6.2 states and proves the main soundness theorem.

6.1     Semantics of the Type Logic
We define the semantics of our Hoare logic with pure and separation types to ensure type safety,
and prove its soundness.
    The semantics is given by a logical relation (Figure 6). In keeping with semantic subtyping,
types are shallowly embedded as predicates of type val→Prop, so proving a type assertion v:t
amounts to proving the proposition t(v) by semantic reasoning. This shallow embedding means
logical connectives for building types are lifted directly from their propositional counterparts, and
subtyping reduces to implication: t1 <: t2 ≡ ∀v.v : t1 ⇒ v : t2 . The encoding supports dependent
singleton types (Appendix A.1) and (co)inductive type predicates. Step-indexing is not required
because the encoding is stateless and involves no non-(co)inductive types.
    Several clauses deserve comment. The clause for 𝜎∧𝜋 splits the heap into two disjoint parts
ℎ 1 and ℎ 2 : ℎ 1 satisfies the heap assertion 𝜎 (ownership) and ℎ 2 satisfies the pure constraint 𝜋 (no
ownership). The clause for l↦→C(. . .) requires ℎ to consist of exactly the single cell l, reflecting full
ownership. By contrast, l:C(. . .) only requires l to point to a C-node somewhere in ℎ, permitting
aliasing. This is the semantic counterpart of the syntactic distinction between separation types and
pure types established in Sec. 2.2. The clause for pred unfolds the predicate definition, connecting
type predicates (Sec. 2.4) to their set-theoretic meaning.

2 Nevertheless, there is a recent retrofit of liquid types to Rust [27] which uses the ownership and borrowing mechanisms of

Rust.
20                                                                                                     Li, Foo, Ta, and Chin


               𝑠, ℎ |= x:{c}                iff 𝑠 (x)=c               𝑠, ℎ |= x1 :{x2 } iff 𝑠 (x1 )=𝑠 (x2 )
               𝑠, ℎ |= x1 =x2               iff ∃ 𝑙 ·𝑠 (x1 )=𝑠 (x2 )=l
               𝑠, ℎ |= ∆1 ∨ ∆2              iff 𝑠, ℎ |= ∆1 or 𝑠, ℎ |= ∆2
               𝑠, ℎ |= 𝜎 ∧ 𝜋                iff ∃ℎ 1, ℎ 2 ·ℎ=ℎ 1 oℎ 2 ∧ 𝑠, ℎ 1 |= 𝜎 ∧ 𝑠, ℎ 2 |= 𝜋
               𝑠, ℎ |= 𝜎1 ∗ 𝜎2              iff ∃ℎ 1, ℎ 2 ·ℎ=ℎ 1 oℎ 2 ∧ 𝑠, ℎ 1 |= 𝜎1 ∧ 𝑠, ℎ 2 |= 𝜎2
               𝑠, ℎ |= 𝜋1 ∨ 𝜋 2             iff 𝑠, ℎ |= 𝜋1 or 𝑠, ℎ |= 𝜋2
               𝑠, ℎ |= 𝜋1 ∧ 𝜋 2             iff 𝑠, ℎ |= 𝜋1 and 𝑠, ℎ |= 𝜋2
               𝑠, ℎ |= ¬𝜋                   iff not (𝑠, ℎ |= 𝜋)
               𝑠, ℎ |= ∆1 ∗ ∆2              iff 𝑠, ℎ |= (𝜎1 ∗ 𝜎2 ) ∧ (𝜋 1 ∧ 𝜋 2 ) 𝑤ℎ𝑒𝑟𝑒 ∆i = 𝜎i ∧ 𝜋 i
               𝑠, ℎ |= x:t                  iff ∃l · 𝑠 (x)=l and 𝑠, ℎ |= l:t
               𝑠, ℎ |= l:prim               iff l ∈ prim 𝑤ℎ𝑒𝑟𝑒 prim = Int | Str | Err | · · ·
               𝑠, ℎ |= l↦→C(t1, .., tn )    iff ℎ = {l↦→C(l1, .., ln )} and ∧ni=1𝑠, ℎ |= li :ti
               𝑠, ℎ |= l:C(t1, .., tn )     iff ℎ(l) = C(l1, .., ln ) and ∧ni=1𝑠, ℎ |= li :ti
               𝑠, ℎ |= l:pred(t∗ )          iff l:pred(t∗ ) = ∆ and 𝑠, ℎ |= ∆
               𝑠, ℎ |= l:¬t                 iff not (𝑠, ℎ |= l:t)
               𝑠, ℎ |= l:t1 →t2             iff ∀v · (𝑠, ℎ |= v:t1 → 𝑠, ℎ |= l(v):t2 )

                                     Fig. 6. Semantics of Type Logic Formulae


6.2   Soundness Theorem
The connection between Hoare triples and standard function types is established by a modified
function arrow →′ , defined via Hoare triples, coinciding with the standard arrow:
               { ∆1 } 𝑒 { ens[r] ∆2 }        iff                   (∆1 =⇒ ∀𝑟, 𝑒 { 𝑟 =⇒ 𝑟 |= ∆2 )                         (1)
                                     ′
                             𝑓 :𝑡 1 → 𝑡 2    iff                        ∀𝑣, { 𝑣:𝑡 1 } 𝑓 (𝑣) { ens[r] r:t2 }              (2)
  Defining a modified function arrow →′ in terms of a standard Hoare triple (which is also defined
extensionally, using a big-step relation), we can see that it is equivalent (a lifting of ⇐⇒ ) to the
regular function arrow from Fig. 6.
    Lemma 6.1 (Agreement between function arrows). 𝑡 1 → 𝑡 2 ≡ 𝑡 1 →′ 𝑡 2 .
    This lemma shows that the behaviours of well-typed programs are exactly those of programs
specified by Hoare triples: the two notions of function type are definitionally equivalent. It is proved
by unfolding both definitions and using the big-step operational semantics.
    The soundness of the Hoare rules is stated as follows.
    Theorem 6.2 (Soundness). Given { ∆1 } 𝑒 { ens[r] ∆2 }, ∀𝑠, ℎ, 𝑠 ′, ℎ ′, 𝑣 if 𝑠, ℎ |= ∆1 holds and
𝑠, ℎ, 𝑒 { 𝑠 ′, ℎ ′, 𝑣, then 𝑠 ′ +[(𝑟, 𝑣)], ℎ ′ |= ∆2 .
    Proof. The proof proceeds by induction on the derivation of the Hoare triple, with a compati-
bility lemma for each rule in Figure 4. The use of big-step semantics in Theorem 6.2 is deliberate:
big-step semantics guarantees that if an expression terminates it reaches its postcondition, and
non-terminating expressions satisfy the postcondition vacuously. This means a single theorem
simultaneously captures both type preservation (the type of the result matches the postcondition)
and progress (no well-typed, terminating expression gets stuck). Traditional type systems typically
require two separate theorems (preservation and progress) using small-step semantics.
                                                                                                       □
    Definition 6.3 (Well-typed programs never abort). 𝑒 is well-typed under satisfiable ∆1 if and only
if { ∆1 } 𝑒 { ens[r] ∆2 } and ∆2 does not contain Abrt.
Type Safety via Hoare Logic with Separation and Pure Types                                         21


  This definition formalises the refined motto of Sec. 2.3: well-typed programs must never abort.
Note that Err (runtime errors) may appear in ∆2 ; they are tolerated. Only Abrt is forbidden, since
Abrt represents a compile-time type error that the verification framework must rule out entirely.

7   META-THEORY AND EVALUATION VIA LEAN
We have produced a fully machine-checked mechanisation of the meta-theory of TypeHL in the
Lean 4 proof assistant; and, from it, an executable, self-certifying type-checker (App. F; machin-
ery detailed in App. G). The development is self-contained: it depends on no external library
such as mathlib. Every theorem is proved without sorry or admit. The meta-theorems, and
the soundness proofs of the checker itself, depend only on the standard classical axiom base
{propext, Classical.choice, Quot.sound}; individual examples checked at a ground instantiation
additionally carry a compiler-reduction axiom in their own footprint, while the symbolic certificates
— those quantified over open types or heights, including the flagship red-black insert — are fully
axiom-clean. It comprises roughly 78,400 lines: three layers, each a sound type system covering
the paper’s central ingredients, plus certified index engines (about 14,700 lines) and, per layer, the
reflective type-checker.
   Three layers. (i) The pure fragment (heap-free) formalises semantic subtyping as a Boolean
algebra of types, path-sensitive case specifications with the implicit _ r:⊤ clause, the Err/Abrt
discipline, and the forward Hoare rules as an inductive derivation relation; it establishes soundness
(Theorem 6.2) and well-typed programs never abort (Definition 6.3). (ii) The separation layer adds
imperative Ref cells and separation types x↦→t, with allocating constructors, strong update, a
relational big-step semantics, the Frame rule, and soundness over it. (iii) The higher-order layer
adds first-class (environment-capturing, multi-argument) closures, the lambda/checking rules, and
the agreement lemma relating the type arrow to the Hoare-triple arrow.
  Key meta-theoretic choices. Several decisions are worth highlighting, as they are exactly the
points where the mechanisation is delicate.
 • Soundness by rule induction. The Hoare rules are the constructors of an inductive relation, and
   soundness is a single theorem proved by induction over a derivation. In the pure layer this
   is a total, recursion-bounded big-step semantics (so recursion is sound and a single theorem
   subsumes preservation and progress); the separation layer uses a relational one.
 • Types interpreted by recursion on the type, not the heap. A type is a predicate on values; for heap
   types the interpretation looks through the heap but recurses only on the (finite) type structure.
   Consequently cyclic Ref heaps pose no well-foundedness problem and no step-indexing is
   required, avoiding the circularity noted in Sec. 6.1.
 • Relational allocation enables Frame. Allocation chooses some fresh location rather than a deter-
   ministic one; this makes the heap-locality (callee-footprint) lemma underlying the Frame rule
   provable. It holds over the full language, including function calls and match.
 • Shallow, registry-based type predicates. Recursive type predicates are well-founded Lean defini-
   tions, each carrying its own termination proof, side-stepping a generic termination check.
 • Stratification for higher-order types. The behavioural function type refers to evaluation, while
   the cast rule must decide types; we break the apparent circularity by a structural decision
   procedure for casts and a semantic interpretation for arrows, bridged by an agreement lemma.
  Flagship developments. Beyond the core meta-theory, the development mechanises
four case-study families, each with honest boundaries. (i) Red-black balancing. The five-
function Okasaki insert is verified at every height, insert : ∀ℎ. (Int, RBTree(Int, 𝑐, ℎ)) ⇒
RBTree(Int, Black, ℎ) ∨ RBTree(Int, Black, ℎ+1), with a recursive member. Balancing needs
22                                                                                  Li, Foo, Ta, and Chin


colour-correlated child types to survive pattern matches (each match branch gets one disjunct per
node package) and a sorted quantifier for the height index (both part of the mechanised rule set,
not ad-hoc lemmas). It is later discharged automatically by the reflective checker (App. F). (ii) Heap
predicates and a typed queue. The separation layer registers inductive heap predicates with exact
footprints (list segments and a packed two-pointer queue), closing the last coverage gap of App. G.
On top sit ghost-free packed preconditions: a caller sees one opaque invariant atom, unfolded through
registered templates. Both enqueue and dequeue are certified against the bare invariant, dequeue
with the honest Err ∨ Int postcondition covering empty and non-empty cases. (iii) Frame over heap
predicates. The Frame rule extends to the new heap-predicate atoms on the match-free fragment
(SemValid.frame_matchfree), with two flagships: a disjoint packed queue framed across enqueue,
and a content-carrying cell framed across a strong update. A locality countermodel shows the match
restriction is essential (an aliased content atom can flip a match from abort to normal execution),
while the corresponding semantic-triple question remains open and documented. (iv) Sized types
on a certified arithmetic engine. Sized-list and sized-tree specifications (List(𝑇 , 𝑛); trees sized
1+𝑎+𝑏) are registered over a general affine-equality index engine. Two sized-list flagships are
checker-certified end-to-end for all integers: append : List(𝑇 , 𝑛) × List(𝑇 , 𝑚) ⇒ List(𝑇 , 𝑛+𝑚)
and exact-length length : List(𝑇 , 𝑛) ⇒ {𝑛} (uninhabited at 𝑛<0, content at 𝑛, 𝑚 ≥ 0). A sized-tree
node’s child sizes are not fixed by the parent’s: an existential decomposition (𝑠 = 1+𝑎+𝑏) no
single-pair match expresses; a declared-post frame gate crosses this wall, certifying size and
mirror (size-preserving destruction and reconstruction) end-to-end. There is no remaining
documented index-language boundary. A companion inequality-fragment engine (a certified
unit-Farkas procedure) checker-certifies sorted insertion on the paper’s SortedList(𝑇 , 𝑙𝑜, ℎ𝑖)
predicate, insert : (Int, SortedList(Int, 𝑙𝑜, ℎ𝑖)) ⇒ SortedList(Int, 𝑙𝑜, ℎ𝑖), with head and
member via a bespoke ∀-element destruction rule.

   Correspondence with the paper. The principal results are mechanised as follows (Lean identifiers
in typewriter).

Paper result                                          Lean theorem
Soundness (Theorem 6.2)                               Pure.soundness, Sep.soundness, HO.soundness
Well-typed programs never abort (Def. 6.3)            Pure.never_abort
Agreement between function arrows (Lemma)             HO.agreement
Frame rule                                            Sep.SemValid.frame (via
                                                      Sep.BigStep.frame_fwd_typed)
Irreversible weakening (Sec. 2.2)                     Sep.sep_weakens_to_pure
Flagship developments
Red-black insert balanced at every height             rbInsert_semvalid,
                                                      rbInsert_semvalid_reflective
Typed queue, ghost-free packed preconditions          enqueue_semvalid_packed,
                                                      dequeue_semvalid_packed
Frame over heap-predicate atoms (match-free)          SemValid.frame_matchfree
Sized-list append/length, ∀ integers                  append_semvalid, length_semvalid
(checker-certified)
Sized-tree destruction/reconstruction preserve size   size_semvalid, mirror_semvalid (semantic form:
(checker-certified)                                   streeAt_mirrorV)
Sorted insertion over SortedList(T, lo, hi)           insert_semvalid, head_semvalid,
(checker-certified)                                   member_semvalid
Type Safety via Hoare Logic with Separation and Pure Types                                        23


Beyond these and the flagship developments above, the development mechanises type-variable
polymorphism (e.g. id:∀T. T→T instantiated at multiple types, and length:∀T. List(T)→Int), user-
definable recursive predicates (a Tree predicate defined entirely in the registry), multi-argument
functions, environment-capturing multi-argument closures, and pure higher-order functions rang-
ing over recursive-predicate data (map, filter, and fold_left over List(T)). Each layer ships
machine-checked example programs together with a non-vacuity audit: concrete operational ex-
ecutions witness that the evaluator produces real results and that the soundness statements are
not vacuously satisfied. The Lean sources, a theorem index, and build instructions accompany the
artifact. App. G details the machinery (proof-script sizes, checking times, and standard benchmark
and library coverage), while App. F describes the reflective, self-certifying type-checker.

Evaluation
The checker checks a suite of examples reflectively, by layer; none needs a hand-written proof. At
a ground type this covers the M1 arithmetic examples, the separation programs including strong-
update assign, and the M3 higher-order examples. For eight higher-order functions (the recursive
list functions map, filter, fold_left, append, rev and the three Option functions) we discharge
the whole-program WFEnv obligation and lift it to full semantic validity. All eight, plus pure id,
length, and nth, are additionally certified polymorphic in their element types by the native-free
symbolic mode. The flagship result is RBTree_insert: the whole five-function Okasaki insert is
discharged symbolically for every height (∀ℎ), end-to-end axiom-clean with no native_decide
and no SMT, on a certified successor index sub-fragment. The typed two-pointer Queue is likewise
certified reflectively, down to a ghost-free packed precondition.
   In sum, the result is a type-checker fully automatic on its reflective suite for expressive type
specifications. Its central strength is not speed but trust and reach: a single checker handles pure-
type checking automatically (at native speed for ground programs) and extends unchanged to the
expressive specifications of separation types and recursive/sized predicates (balanced trees, sized
lists, a typed queue). Every verdict is certified sound against the Hoare rules rather than trusted.

8   RELATED WORK
   Semantic Subtyping. Semantic-based subtyping interprets each type as the set of values inhabiting
it: t1 <: t2 holds when Set(t1 ) ⊆ Set(t2 ). The advantages of semantic subtyping have been
explored in [5, 7, 15], and subsequent work extended it from several perspectives: subtyping
relation computation [4], decidability [18], and application to other programming paradigms [1, 33].
Singleton, union, and intersection types have received further attention through their set-based
interpretation [10, 12]. MLstruct [32] uses a Boolean algebra of types to infer principal types
with union and intersection for an ML-like language, handling subtyping that traditional Hindley-
Milner inference avoids. This approach was later extended to dynamically-typed languages [8].
Gradual typing offers a complementary route to combining static and dynamic typing, including
under parametric polymorphism [21]; we instead span this spectrum by adjusting the strength of
specifications rather than by inserting run-time casts.
  Hoare Logic for Type Safety. Hoare logic has also been used to ensure type safety in selected
domains: typed assembly for operating systems [20, 44] and dynamically-typed programs [13, 14].
These works extract type information from the precondition and reduce type safety to verifying the
Hoare triple {p}e{true}. Our work greatly expands on this approach, extending it with separation
types, type predicates, case specifications, and a disciplined error hierarchy.
  Type Systems for Memory and Resource Safety. Sub-structural type systems have been developed to
reason about system resources such as memory, files, and locks [34]. The most prominent example
24                                                                                  Li, Foo, Ta, and Chin


is Rust, which uses ownership and borrowing to ensure memory safety. OxCaml, a variant of
OCaml, has similarly been extended with a linear type system to reason about affinity, uniqueness,
and locality of resources, supporting both memory safety and data race freedom [17, 28]. Our goal
is similar, but our approach differs: rather than designing a new type discipline, we leverage the
expressivity of Hoare logic to reason about memory and resource properties through separation
types and flow-sensitivity. Closest in mechanised guarantee, the foundational verifiers RefinedC
[37] and RefinedRust [16] check C and Rust code against refined ownership types with Iris-based,
machine-checked proofs. They target full functional correctness through a separation-logic backend,
whereas we target type safety through a solver-free, self-certifying checker.
   From Uniqueness to Separation Type. Resource and ownership types for strong aliasing and flow-
sensitivity have a rich prior art. A recent work [2] related frame rules in uniqueness type systems
to separation logic via an FFI. Earlier, [38, 43] used alias types in typed assembly to describe heap
shapes. Ownership types were subsequently used to support strong updates in refinement type
systems [42]. Kloos et al. [26] combine liquid types with concurrent separation logic to track heap
ownership across asynchronous tasks, supporting strong updates to heap location types. Similarly,
Flux [27] lifts liquid-style refinements to Rust by exploiting Rust’s ownership mechanisms to
enable strong updates. Closest in spirit is Mezzo [3], whose permission types control aliasing and
mutation of heap memory, with a machine-checked proof that well-typed programs do not go
wrong. Permission-based reasoning of this kind also underpins verification infrastructures such as
Viper [30]. We introduce ownership in the sequential setting, enabling flow-sensitive type mutation.
Rather than relying on a host language’s borrow checker, we use first-class logical assertions
together with type predicates. This makes our approach applicable to languages without built-in
ownership, and additionally supports must-aliasing via singleton types. Our wider contribution
is to unify these ideas within a single Hoare logic framework, increasing coverage of type-safety
scenarios compared to any individual prior system.
  Mechanised and logical type soundness. Our Lean development establishes soundness in the
semantic, logical-relations style rather than by a purely syntactic progress-and-preservation argu-
ment, in the tradition of Iris [24] and Timany et al.’s logical approach to type soundness [40] (which
RustBelt [23] applies to justify Rust’s ownership discipline). We share their reading of a type as a
predicate on values, but interpret heap types by recursion on the (finite) type structure rather than
through a step-indexed model, so no step-indexing is required. From the same mechanisation we
additionally extract an executable, self-certifying type-checker.
   Stability and Rely-Guarantee. The stability condition on pure type predicates (Definition 3.1) is
the sequential counterpart of interference freedom in Owicki and Gries’s proof system for concur-
rent programs [31], and of stability under the rely relation in Jones’s rely-guarantee framework
[22]. The closest type-system counterpart is the rely-guarantee reference system of [19], which en-
forces stability of refinement predicates over aliased mutable data via per-reference rely/guarantee
annotations. Our notion of stable pure type achieves the same guarantee in the sequential setting
without such annotations.

9    CONCLUSION
This paper has presented a Hoare logic framework for type-safety verification that unifies separation
types, case specifications, type predicates, and a disciplined error hierarchy. Building on semantic
subtyping, we have extended the logic of types with: separation types that support flow-sensitive
type mutation and must-aliasing; a comprehensive error hierarchy distinguishing Err (runtime
errors), Exc (checked and unchecked exceptions), and Abrt (compile-time errors); path-sensitive
Type Safety via Hoare Logic with Separation and Pure Types                                                                25


and flow-sensitive type specifications via case specifications; and type predicates that subsume
GADTs and liquid types. We have formalised the Hoare rules in Lean 4 and proved soundness,
obtained from it a self-certifying type-checker by proof reflection, and evaluated it on a benchmark
suite demonstrating cases that standard type systems such as OCaml cannot handle.

ACKNOWLEDGMENTS
This research is supported by the Ministry of Education, Singapore, under its MOE Academic
Research Fund Tier 3 (RIE2025) (MOE Award No: MOE-MOET32021-0001), and under the Academic
Research Fund Tier 1 (FY2023) (Project Title: Automated Verification for Imperative Higher-Order
Programs).

REFERENCES
 [1] Davide Ancona and Andrea Corradi. Semantic subtyping for imperative object-oriented languages. In Proceedings of
     the 2016 ACM SIGPLAN International Conference on Object-Oriented Programming, Systems, Languages, and Applications,
     OOPSLA 2016, pages 568–587. ACM, 2016.
 [2] Pilar Selene Linares Arévalo, , Arthur Azevedo de Amorim, Vincent Jackson, Liam O’Connor, Peter Schachte, and
     hristineRizkallah. Memory safety: Uniqueness as separation. In Programming Languages and Systems - 23rd Asian
     Symposium, APLAS 2025, volume 16201 of Lecture Notes in Computer Science, pages 3–21. Springer, 2025.
 [3] Thibaut Balabonski, François Pottier, and Jonathan Protzenko. The design and formalization of Mezzo, a permission-
     based programming language. ACM Transactions on Programming Languages and Systems, 38(4), 2016.
 [4] Gavin M. Bierman, Andrew D. Gordon, Catalin Hritcu, and David E. Langworthy. Semantic subtyping with an SMT
     solver. In Proceeding of the 15th ACM SIGPLAN international conference on Functional programming, ICFP 2010, pages
     105–116. ACM, 2010.
 [5] Giuseppe Castagna. Semantic subtyping: Challenges, perspectives, and open problems. In Theoretical Computer Science,
     9th Italian Conference, ICTCS 2005, volume 3701 of Lecture Notes in Computer Science, pages 1–20. Springer, 2005.
 [6] Giuseppe Castagna. Programming with union, intersection, and negation types. In Bertrand Meyer, editor, The French
     School of Programming, pages 309–378. Springer, 2024.
 [7] Giuseppe Castagna and Alain Frisch. A gentle introduction to semantic subtyping. In Proceedings of the 7th International
     ACM SIGPLAN Conference on Principles and Practice of Declarative Programming, pages 198–199. ACM, 2005.
 [8] Giuseppe Castagna, Mickaël Laurent, and Kim Nguyen. Polymorphic type inference for dynamic languages. Proc.
     ACM Program. Lang., 8(POPL):1179–1210, 2024.
 [9] Wei-Ngan Chin, Cristina David, Huu Hai Nguyen, and Shengchao Qin. Automated verification of shape, size and bag
     properties via user-defined predicates in separation logic. Science of Computer Programming, 77:1006–1036, 2012.
[10] Bruno C. d. S. Oliveira, Zhiyuan Shi, and João Alpuim. Disjoint intersection types. In Proceedings of the 21st ACM
     SIGPLAN International Conference on Functional Programming, ICFP 2016, pages 364–377. ACM, 2016.
[11] Stephen Dolan and Alan Mycroft. Polymorphism, subtyping, and type inference in MLsub. In Proceedings of the 44th
     ACM SIGPLAN Symposium on Principles of Programming Languages, POPL 2017, pages 60–72. ACM, 2017.
[12] Jana Dunfield. Elaborating intersection and union types. In Peter Thiemann and Robby Bruce Findler, editors, ACM
     SIGPLAN International Conference on Functional Programming, ICFP’12, Copenhagen, Denmark, September 9-15, 2012,
     pages 17–28. ACM, 2012.
[13] Björn Engelmann and Ernst-Rüdiger Olderog. A sound and complete Hoare logic for dynamically-typed, object-
     oriented programs. In Theory and Practice of Formal Methods - Essays Dedicated to Frank de Boer on the Occasion of His
     60th Birthday, volume 9660 of Lecture Notes in Computer Science, pages 173–193. Springer, 2016.
[14] Björn Engelmann, Ernst-Rüdiger Olderog, and Nils Erik Flick. Closing the gap - formally verifying dynamically typed
     programs like statically typed ones using Hoare logic - extended version. CoRR, abs/1501.02699, 2015.
[15] Alain Frisch, Giuseppe Castagna, and Véronique Benzaken. Semantic subtyping. In Proceedings 17th Annual IEEE
     Symposium on Logic in Computer Science, pages 137–146. IEEE, 2002.
[16] Lennard Gäher, Michael Sammler, Ralf Jung, Robbert Krebbers, and Derek Dreyer. RefinedRust: A type system for
     high-assurance verification of Rust programs. Proc. ACM Program. Lang., 8(PLDI), 2024.
[17] Aïna Linn Georges, Benjamin Peters, Laila Elbeheiry, Leo White, Stephen Dolan, Richard A. Eisenberg, Chris Casinghino,
     François Pottier, and Derek Dreyer. Data race freedom à la mode. Proc. ACM Program. Lang., 9(POPL):656–686, 2025.
[18] Nils Gesbert, Pierre Genevès, and Nabil Layaïda. A logical approach to deciding semantic subtyping. ACM Trans.
     Program. Lang. Syst., 38(1):3:1–3:31, 2015.
[19] Colin S. Gordon, Michael D. Ernst, and Dan Grossman. Rely-guarantee references for refinement types over aliased
     mutable data. In Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation
26                                                                                                    Li, Foo, Ta, and Chin


     (PLDI), pages 73–84, Seattle, WA, USA, June 2013. ACM.
[20] Nadeem Abdul Hamid and Zhong Shao. Interfacing Hoare logic and type systems for foundational proof-carrying
     code. In Theorem Proving in Higher Order Logics, 17th International Conference, TPHOLs 2004, volume 3223 of Lecture
     Notes in Computer Science, pages 118–135. Springer, 2004.
[21] Yuu Igarashi, Taro Sekiyama, and Atsushi Igarashi. On polymorphic gradual typing. Proc. ACM Program. Lang.,
     1(ICFP):40:1–40:29, 2017.
[22] Cliff B. Jones. Development methods for computer programs including a notion of interference. Technical Report
     PRG-25, Oxford University Computing Laboratory, 1981.
[23] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. Rustbelt: securing the foundations of the rust
     programming language. Proc. ACM Program. Lang., 2(POPL):66:1–66:34, 2018.
[24] Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Aleš Bizjak, Lars Birkedal, and Derek Dreyer. Iris from the ground
     up: A modular foundation for higher-order concurrent separation logic. Journal of Functional Programming, 28, 2018.
[25] Ming Kawaguchi, Patrick Maxim Rondon, and Ranjit Jhala. Type-based data structure verification. In Proceedings of
     the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI), pages 304–315, Dublin,
     Ireland, June 2009. ACM.
[26] Johannes Kloos, Rupak Majumdar, and Viktor Vafeiadis. Asynchronous liquid separation types. In 29th European
     Conference on Object-Oriented Programming (ECOOP 2015), pages 396–420. Schloss Dagstuhl–Leibniz-Zentrum für
     Informatik, 2015.
[27] Nico Lehmann, Adam T. Geller, Niki Vazou, and Ranjit Jhala. Flux: Liquid types for Rust. Proceedings of the ACM on
     Programming Languages, 7(PLDI):169, June 2023.
[28] Anton Lorenzen, Leo White, Stephen Dolan, Richard A. Eisenberg, and Sam Lindley. Oxidizing OCaml with modal
     memory management. Proc. ACM Program. Lang., 8(ICFP):485–514, 2024.
[29] Meta. The Hack programming language. https://hacklang.org, 2014.
[30] Peter Müller, Malte Schwerhoff, and Alexander J. Summers. Viper: A verification infrastructure for permission-based
     reasoning. In Verification, Model Checking, and Abstract Interpretation (VMCAI), volume 9583 of Lecture Notes in
     Computer Science, pages 41–62. Springer, 2016.
[31] Susan S. Owicki and David Gries. An axiomatic proof technique for parallel programs I. Acta Informatica, 6(4):319–340,
     1976.
[32] Lionel Parreaux and Chun Yin Chau. MLstruct: principal type inference in a boolean algebra of structural types. Proc.
     ACM Program. Lang., 6(OOPSLA2):449–478, 2022.
[33] Tommaso Petrucciani, Giuseppe Castagna, Davide Ancona, and Elena Zucca. Semantic subtyping for non-strict
     languages. In 24th International Conference on Types for Proofs and Programs, TYPES 2018, volume 130 of LIPIcs, pages
     4:1–4:24. Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 2018.
[34] Benjamin C. Pierce. Advanced Topics in Types and Programming Languages. MIT Press, 2004.
[35] Marianna Rapoport and Ondřej Lhoták. A path to DOT: Formalizing fully path-dependent types. Proc. ACM Program.
     Lang., 3(OOPSLA), 2019.
[36] John C. Reynolds. Separation logic: A logic for shared mutable data structures. In 17th IEEE Symposium on Logic
     in Computer Science (LICS 2002), 22-25 July 2002, Copenhagen, Denmark, Proceedings, pages 55–74. IEEE Computer
     Society, 2002.
[37] Michael Sammler, Rodolphe Lepigre, Robbert Krebbers, Kayvan Memarian, Derek Dreyer, and Deepak Garg. RefinedC:
     automating the foundational verification of C code with refined ownership types. In PLDI, pages 158–174, 2021.
[38] Frederick Smith, David Walker, and J. Gregory Morrisett. Alias types. In Gert Smolka, editor, Programming Languages
     and Systems, 9th European Symposium on Programming, ESOP 2000, Held as Part of the European Joint Conferences on
     the Theory and Practice of Software, ETAPS 2000, Berlin, Germany, March 25 - April 2, 2000, Proceedings, volume 1782 of
     Lecture Notes in Computer Science, pages 366–381. Springer, 2000.
[39] Jane Street. OxCaml. https://oxcaml.org/, 2025.
[40] Amin Timany, Robbert Krebbers, Derek Dreyer, and Lars Birkedal. A logical approach to type soundness. J. ACM,
     71(6):40:1–40:75, 2024.
[41] Sam Tobin-Hochstadt and Matthias Felleisen. The design and implementation of Typed Scheme. In Proceedings of the
     35th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL), pages 395–406. ACM, 2008.
[42] John Toman, Ren Siqi, Kohei Suenaga, Atsushi Igarashi, and Naoki Kobayashi. Consort: Context-and flow-sensitive
     ownership refinement types for imperative programs. In ESOP, volume 20, pages 684–714, 2020.
[43] David Walker and J. Gregory Morrisett. Alias types for recursive data structures. In Robert Harper, editor, Types in
     Compilation, Third International Workshop, TIC 2000, Montreal, Canada, September 21, 2000, Revised Selected Papers,
     volume 2071 of Lecture Notes in Computer Science, pages 177–206. Springer, 2000.
[44] Jean Yang and Chris Hawblitzel. Safe to the last instruction: automated verification of a type-safe operating system.
     In Proceedings of the 2010 ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI 2010,
Type Safety via Hoare Logic with Separation and Pure Types                                    27


    pages 99–110. ACM, 2010.
The accompanying Lean mechanization (the full sources, theorem index, and build instructions) is
provided in the ancillary files (anc/lean-supplement.zip).
28                                                                                  Li, Foo, Ta, and Chin


A     BASIC FEATURES OF TYPES
A.1    Wider Usage of Singleton Types
Recently, singleton types were used in [8, 32] for constant literals of the form c, such as 3 or “hi”.
Whenever a variable v is bound to a constant c, we use the type notation v:{c} to state that v has
singleton type c.
   In Scala, a singleton object class is essentially a class with a single instance. In this paper, we
define a singleton type as a type containing only a single value. We extend singleton types to
include parameter (input) variables such as x, using the annotation r:{x} to denote that result r has
singleton type x. In Hoare logic terms, r:{x} is equivalent to r=x, since any output r with singleton
type x has the same value as x.
   An example is the identity function:
       id x = x

Using the singleton type, we write id : (x:Any→r:{x}), where the input has type Any and the
output has singleton type x. This requires fewer universally quantified type variables than
the principal type id : (∀a. a→a). One can verify that id : (x:Any→r:{x}) is equivalent to
id : (∀a. a→a); the former has fewer quantified variables and is therefore easier to apply during
type-checking (requiring fewer existential instantiations). In Hoare logic notation, this corresponds
to id :: (𝜆 x r. req true ens[r] r:{x}).
   As a second example, consider (𝜆x. x x), where the parameter x is applied to itself. Using single-
ton types, its function type is ∀b. (x:{x}→b)→b, which uses one fewer quantified variable than
the ∀a, b. (a∧a→b)→b formulation of [8]. Fewer quantified variables simplify existential instanti-
ation for polymorphic method calls. Using our formulation, one can prove (𝜆x. x x) (𝜆x. x x) : ⊥
and (𝜆x. x x) (𝜆x. x) : (x:Any→r:{x}), both of which are beyond the reach of [8]. The application
(𝜆x. x x) (3) is correctly rejected as untypeable by both [8] and our framework. We currently restrict
singleton types to variables and function-call arguments; field positions use type variables instead.

A.2    Constructors and Type Predicates
In statically-typed languages such as OCaml, algebraic data types are standard. Using the polymor-
phic list type from Sec. 1, the type annotation for length is:
       (* Type signature and implementation of length *)
       length : ∀T. List (T) → Int
       length ( xs ) = match xs of
                    { Nil -> 0;
                      Cons (y , ys ) -> 1 + length ( ys )}

Our framework supports types that are more fine-grained than declared algebraic data types. The
type List(T) is semantically equivalent to the recursive predicate:
       r : List ( T ) ≡ r: Nil ∨ r: Cons (T , List (T))

Under semantic subtyping, Nil and Cons are subtypes of List and can appear directly in specifica-
tions. A more precise specification for length is:
       (* Type specification of length *)
     length : ∀T . case [ xs ]
             { Nil ens [r] r :0;
               Cons (T , List (T)) ens [r] r: Int }
Type Safety via Hoare Logic with Separation and Pure Types                                      29


  Here r:0 is a singleton type, since Set({0})⊂Set(Int). Singleton return types enable more infor-
mative specifications for path-sensitive code, particularly when values with distinct constructors
produce different outcomes.
  Recursive type predicates support algebraic data types in static typing scenarios and can be
extended to GADTs (Sec. 2.4) and type classes (Appendix B.1).
  Although recursive predicates define stronger types, they may appear incompatible with
dynamically-typed programs that rely on runtime type testing. For complex types such as
List(List(T)), we propose using the unnested form List(_) for runtime testing. Concretely,
List(_) abbreviates Nil∨Cons(_, _), as described next.

A.3    Combining Type Testing with Pattern-Matching
Statically-typed languages use pattern-matching; dynamically-typed languages rely on type-testing.
Recent proposals, including C#, attempt to unify both. We achieve this integration via an enhanced
match construct that supports both pattern-matching and structural type-testing.
   The function length_generic dispatches the length computation based on the runtime type of
its argument. Its case specification is:
     (* Type spec and code of length *)
     length_generic : ∀T. case [ xs ]
                   { xs : Int ens [r] r :1;
                     xs : Str ens [r] r: Int ;
                     xs : List (T) ens [r] r: Int }
     length_generic xs = match xs of
                 { Int -> 1;
                   Str -> length_of_str ( xs );
                   List (_) -> length ( xs )}
  Recall that List(_)≡Nil∨Cons(_, _). The case specification with singleton type 1 for the Int
branch is strictly more precise than the intersection type:
       length_generic : (∀T. List (T) → Int ) ∧
            ( Int → Int ) ∧ ( Str → Int )
    The method length was already defined in Sec. A.2.

B     ADVANCED TYPES
B.1    Support for Type Classes
We describe how our framework supports type classes, as adopted by Haskell and Scala for ad hoc
polymorphism. The Num type class supports generic numeric operations:
        + : ∀T · Num (T) ⇒ T→T→T
  Using pre/post type specifications, we encode this with a type-class predicate Num(T) built from
the instance declarations of Num:
       Num ( T :*) ≡ (T= Int ) ∨ (T= Float ) ∨ ...
    This predicate appears as a precondition constraint on overloaded operations:
       + :: 𝜆 x y r · ∀ T · req [x ,y] x:T ∧ y:T
                  ∧ Num (T) ens [r] r:T
    Higher-order type classes are supported similarly. For the Functor class:
30                                                                                  Li, Foo, Ta, and Chin


       class Functor (F :*→*) {
        map : ∀A , B · (A→B) → F(A) → F(B)
     the specification for map is:
       map :: 𝜆 f xs r · ∀ F :*→*,A ,B ·
        req [f , xs ] f :( A→B) ∧ xs :F(A) ∧ Functor (F)
        ens [ r ] r : F (B)
       Functor ( F :*→*) ≡ (F= List ) ∨ (F= Option ) ∨ ...
  Type classes may be organised in an inheritance hierarchy. For example, since Monad extends
Functor, we have the lemma ∀F:(∗→∗). Monad(F)⇒Functor(F). Note that type-class predicates
such as Num(_) and Functor(_) may not be used for runtime type-testing, since they range over
types rather than values.

B.2     Gradual Typing for Dynamic Languages
Although our expressive specifications capture many dynamically-typed programs as statically
safe, some examples remain outside the current framework. Consider:
        f (x , y ) = if x >5 then !y else y +1
For this to be statically type-safe, the precondition would need y:Ref(T)∧Int, which reduces to
y:⊥, making the precondition unsatisfiable. Gradual typing addresses this via a special family of
pure types ?t, allowing runtime casts. We permit y:?(Ref(T)∨Int) in specifications:
                               req[x, y] x:Int ∧ y:?(Ref(T)∨Int)
                               ens[r] (y:Ref(T) ∧ r:T) ∨ (y:Int ∧ r:Int)
Runtime casts are inserted into the program body to enforce the chosen branch:
        f (x , y ) = if x >5 then let z = (? Ref (_)) y in !z
                             else let z = (? Int ) y in z +1
Such programs are gradually typed: some execution paths may produce a runtime abort. The
runtime cast (?p) v is defined as:
        (? p ) v = match v of { p -> v; _ -> abort }
The Hoare rule for runtime cast ignores abort, treating it as a runtime error rather than a compile-
time error:
                     fresh 𝑟    ∆ ⊢ 𝑥:?(_) ∆1 ≡(∆ ∧ (𝑥:𝑝) ∧ 𝑟 :{𝑥 })
                                                                        𝑅−𝐶𝑎𝑠𝑡
                                { ∆ } (?𝑝) 𝑥 { ens[r] ∆1 }

B.3     Restrictions to Support Decidability
In their full generality, type predicates are not decidable: arbitrary recursive predicates with
unrestricted quantification and negation quickly exceed the reach of automated verification. In
practice, decidability can be recovered by imposing the following five restrictions, which together
cover the vast majority of data structure predicates that arise in verification.
     • Structural recursion only. Predicates must unfold only on the direct sub-components of
        a constructor: no mutual recursion through non-structural positions. This makes well-
        foundedness syntactically checkable and ensures unfolding always terminates.
     • Linear arithmetic for index constraints. Restricting index constraints to linear arithmetic over
        integers (e.g. n = m + 1, lo≤v) reduces subtyping obligations to linear arithmetic validity,
        decidable by standard SMT solvers via the theory of linear integer arithmetic (LIA) — our
        Lean mechanisation decides the equality fragment of this theory with a certified, solver-free
Type Safety via Hoare Logic with Separation and Pure Types                                          31


       in-checker procedure, and, for the mechanised SortedList flagships’ proof obligations,
       the inequality fragment as well, via a certified unit-Farkas decision procedure (App. F),
       reserving SMT for general linear-arithmetic inequality reasoning beyond those obligations.
       Non-linear arithmetic or quantifier alternation would push into undecidability.
     • Restricted existential quantification. Existentials in predicate bodies must be eliminable: ei-
       ther by unification during unfolding, or by bounding them over finite domains. Unrestricted
       nested existentials can render subtyping undecidable.
     • Negation-free or negation at base types only. Boolean combinations ∨ and ∧ are decidable
       provided sub-predicates are decidable. However, negation (¬) of recursive predicates in-
       troduces co-inductive reasoning and is generally undecidable. Restricting negation to base
       types only preserves decidability.
     • Symbolic heap fragment for separation predicates. Full separation logic with arbitrary
       recursive heap predicates is undecidable. The symbolic heap fragment recovers decidability
       by restricting the form of inductive predicate definitions rather than banning recursion
       itself: each predicate case must be expressed using only points-to assertions, separating
       conjunctions, inductive predicate calls, and pure linear arithmetic side conditions — with no
       negation and no non-separating disjunction at the heap level. Recursive inductive predicates
       such as x↦→List(T), x↦→Tree(T), and list segment predicates are fully expressible within
       this fragment, and bi-abduction over such predicates is decidable, as exploited by tools such
       as Smallfoot.
   These five restrictions together form the practical sweet spot adopted by most separation
logic verifiers: structural recursion, linear arithmetic indices, eliminable existentials, negation-
free recursive predicates, and symbolic heap separation. This covers List(T, n), RBTree(T, c, h),
SortedList(T, lo, hi) and the data structure predicates that arise throughout this paper, while keep-
ing verification tractable via SMT solving. In the Lean mechanisation, List(T, n), RBTree(T, c, h),
and size-indexed trees (nodes of size 1+𝑎+𝑏) are now checker-certified end-to-end: their index con-
straints are affine equalities, decided by a certified, solver-free in-checker procedure (App. F), with
no SMT call — including the existential child-size decomposition (𝑠 = 1+𝑎+𝑏, with the children’s
sizes not individually determined by 𝑠) that sized-tree destruction requires, previously the one
remaining checker boundary, now crossed by a declared-post frame gate. SortedList(T, lo, hi)
needs the index inequality fragment (</≤); this fragment is decided too, for the proof obligations of
three checker-certified flagships over SortedList(T, lo, hi) (sorted insert, head, and member) by
a certified, solver-free unit-Farkas procedure, again with no SMT call (App. F). Every data-structure
predicate class in this paper now has at least one checker-certified flagship obligation discharged
this way. General completeness of the underlying decision procedures stays future work, in the
disclosed, restricted form documented alongside each engine (App. F): the affine-equality com-
parators are sound but not proved complete beyond the sums the mechanised predicates exercise,
and the unit-Farkas inequality procedure does not derive coefficient-scaled or equality-tightened
consequences.

C   EXCEPTION HANDLING
The Abrt or ⊤ types are nearly always avoided in the result type of our functions, as any encounter
with abort will cause our program to fail immediately. Case specification is the only type specifica-
tion which allows Abrt or ⊤ to appear in the ens clauses of the otherwise (i.e. _) clause, due to the
need for completeness in case specifications.
   Runtime errors are often modelled as exceptions that could be handled by suitable error recovery
routines. In some languages, such as Java, they are further classified as checked exceptions which
32                                                                                Li, Foo, Ta, and Chin


must be flagged by the type system or unchecked exceptions whose occurrences can be ignored by
the type system.
  In our solution, we would classify checked exceptions (denoted by ChExc) and unchecked
exceptions (denoted by UnExc) as subtypes of Exc:
                                 ⊥ <: {ChExc, UnExc} <: Exc <: ⊤
  Additionally, UnExc is a subtype of valid types and ChExc is disjoint from both Any and Abrt:
                                   UnExc <: {..valid types..}∧
                              ((ChExc ∧ Any) = (ChExc ∧ Abrt) = ⊥)
  In this way, checked exceptions will always be carefully tracked by our type system, while
unchecked exceptions are considered as a subtype of both type universes, AnyP and AnyS , and can
be omitted in our type specifications.
  Try-catch handling can now be implemented via a let-binding, followed by type testing. Raised
exceptions that pass type-casting are propagated outwards via match construct, as illustrated by
the second translation rule below.

                                try e1 catch Exc -> e2
                          ⇔     let x = e1 in match x {Exc -> e2 | _ -> x}

                                let x:t = e1 in e2
                          ⇔     let x = (t ∨ Exc) e1 in
                                match x {Abrt ∨ Exc -> x | _ -> e2 }

D     MORE ON SEPARATION TYPES
D.1    Uniqueness vs Separation Type
Each uniqueness type x↦→T@U is mutually disjoint from both the separation type x↦→T and the
pure type x:T, as the following contradictions show ( ⇔ denotes logical equivalence):
                 x↦→T@U ∧ x:T ⇔ x↦→T ∧ x:T ⇔ x↦→T ∗ x↦→T@U ⇔ false
This design choice ensures each type form has distinct capabilities. Uniqueness and separation
types are interconvertible via the following equivalences:
                        x↦→T@U                 ⇔     x↦→T ∧ NoAlias(x)
                        NoAlias(x) ∧ x=y       ⇔     false
Every uniqueness type converts to a separation type; each separation type converts to a uniqueness
type by dropping all aliases of the form x=y.
  As type-safety is based on over-approximation, the following weakening lemmas apply:
                              x↦→T@U ∧ T<:A      ⇒𝑤𝑒𝑎𝑘𝑒𝑛    x↦→A@U
                              x↦→T ∧ T<:A        ⇒𝑤𝑒𝑎𝑘𝑒𝑛    x↦→A
                              x↦→T               ⇒𝑤𝑒𝑎𝑘𝑒𝑛    x:T
Types are always initialised as strong as possible and weakened only when necessary. Separation and
uniqueness types are assigned at construction and may be irreversibly weakened to flow-insensitive
pure types (last lemma above).
   Both allow type mutation for flow-sensitivity; however, separation types additionally permit
must-aliases, whereas uniqueness types allow only a single reference, making separation types
strictly more expressive. For example, uniqueness types cannot handle swap(m, m) since the two
arguments must be unaliased.
Type Safety via Hoare Logic with Separation and Pure Types                                            33


D.2    Separation Type for Mutable Data Structure
For pure types, inductive predicates capture the weakest property guaranteed for a given algebraic
data type. For List(T):
                      r:List(T) ⇔ r:Nil ∨ (∃𝑞. r:Cons(T, q) ∧ q:List(T))
This predicate is stable for every pure List(T) value. Both acyclic and cyclic lists are instances:
                         x:Cons(T, y) ∧ y:Cons(T, z) ∧ z:Nil ⊢ x:List(T)
                         x:Cons(T, y) ∧ y:Cons(T, z) ∧ z:{x} ⊢ x:List(T)
  Using separation types, acyclic and cyclic lists can be distinguished by the following separation
predicates:
              x↦→AList(T) ⇔ x:Nil ∨ ∃𝑞. x↦→Cons(T, q) ∗ q↦→AList(T)
              x↦→CList(T) ⇔ x↦→Cons(T, q) ∗ q↦→LSeg(T, x)
             x↦→LSeg(T, p) ⇔ x:{p} ∨ ∃𝑞. x↦→Cons(T, q) ∗ q↦→LSeg(T, p) ∧ x:¬{p}
The list-segment predicate x↦→LSeg(T, p) captures an incoming pointer x and an outgoing pointer
p, enabling circular list support. These predicates yield the following provable and disprovable
assertions:
                      x↦→Cons(T, y) ∗ y↦→Cons(T, z) ∧ z:Nil ⊢ x↦→AList(T)
                      x↦→Cons(T, y) ∗ y↦→Cons(T, z) ∧ z:{x} ⊢ x↦→CList(T)
                      x↦→Cons(T, y) ∗ y↦→Cons(T, z) ∧ z:Nil ⊬ x↦→CList(T)
                      x↦→Cons(T, y) ∗ y↦→Cons(T, z) ∧ z:{x} ⊬ x↦→AList(T)
  Separation predicates are flow-sensitive and express data structure invariants that type-safe
verification must maintain. We propose guaranteeing these invariants via pre/post conditions
expressed with appropriate separation predicates.

D.3    Separation Type for Data Race Freedom
A concurrent program has a data race if two threads access the same shared data, at least one access
is a write, and there is no synchronisation ordering between them. One way to ensure race freedom
is to guarantee disjoint memory access, expressed via separation types at field-level granularity.
   Consider a mutable Pair(X, Y) with fields of types X and Y and the following two concurrent
threads:
      p . Pair .1 := " hi "   ||   p. Pair .2 := p. Pair .2+1
Although both threads write to p, they access disjoint fields. The following field-splitting lemma
supports this:
                       p↦→Pair(X, Y) ⇔ p.Pair.1↦→X ∗ p.Pair.2↦→Y
A pair p↦→Pair(X, Y) can be split into disjoint field ownership p.Pair.1↦→X ∗ p.Pair.2↦→Y. Type-safe
verification then proceeds as follows:
      // p - > Pair ( Any , Int )
      // p . Pair .1 - > Any * p. Pair .2 - > Int
      p . Pair .1 := " hi " || p. Pair .2 := p. Pair .2+1
      // p . Pair .1 - > Str * p. Pair .2 - > Int
      // p - > Pair ( Str , Int )
34                                                                                    Li, Foo, Ta, and Chin


  To ensure data race freedom, only separation types (not pure types) may be used in concurrent
threads unless the data structure is immutable: pure types permit arbitrary aliases that other threads
could mutate independently. When concurrent threads require write access to shared heap memory,
the framework can be extended with a locking mechanism over separation-typed data structures.

E    OPERATIONAL SEMANTICS
To facilitate the following soundness proofs, we define a big-step reduction relation with judgments
𝑒, ℎ, 𝑆 {𝑅𝑒 , ℎ 1, 𝑆 1 . Program states consist of a heap ℎ and store 𝑆, like in Sec. 6. Outcomes are
𝑅𝑒 ::= 𝑁𝑜𝑟𝑚(v) | Abrt where 𝑁𝑜𝑟𝑚(v) captures the valid values and Err values which could occur
during the run-time but do not terminate the programs. The Abrt represents a failure which will
immediately kill the process. In the 𝑀𝑎𝑡𝑐ℎ case, we assume there is an implicit case that handles a
match failure. If the process cannot find a case to match, it will terminate the program with Abrt.

                                                      𝑁 𝑖𝑙, 𝐶𝑜𝑛𝑠𝑡, 𝐿𝑎𝑚𝑏𝑑𝑎
                                 v, ℎ, 𝑆 {v, ℎ, 𝑆
                                                                         𝐶𝑜𝑛𝑠
                                 x1 ::x2, ℎ, 𝑆 {𝑆 (x1 )::𝑆 (x2 ), ℎ, 𝑆

                                                                 𝑉 𝑎𝑟
                                         x, ℎ, 𝑆 {𝑆 (x), ℎ, 𝑆
                                       𝑡𝑦𝑝𝑒 (𝑆 (x)) <: t
                                                            𝐶𝑎𝑠𝑡
                                     (t (x)), ℎ, 𝑆 {x, ℎ, 𝑆

                                       𝑡𝑦𝑝𝑒 (𝑆 (x)) ≮: t
                                                             𝐶𝑎𝑠𝑡
                                   (t (x)), ℎ, 𝑆 {Abrt, ℎ, 𝑆

                        e1, ℎ, 𝑆 {v, ℎ 1, 𝑆 1  e2, ℎ 1, 𝑆 1 [x:=v]{v1, ℎ 2, 𝑆 2
                                                                                𝐿𝑒𝑡
                              (let x = e1 in e2 ), ℎ, 𝑆 {v1, ℎ 2, 𝑆 2 \{x}

                                𝑆 (f) = 𝜆 x∗ . Φe      𝑆 (x∗ ) = v∗
                                      ∗   ∗
                                    [x :=v ]e, ℎ, 𝑆 {v2, ℎ 1, 𝑆 1
                                                                    𝐴𝑝𝑝
                                      f(x∗ ), ℎ, 𝑆 {v2, ℎ 1, 𝑆 1
                                           x1 ∈ dom(ℎ)
                                                                         𝐴𝑠𝑠𝑖𝑔𝑛
                           (x1 := x2 ), ℎ, 𝑆 {(), ℎ[𝑆 (x1 ):=𝑆 (x2 )], 𝑆

                                                                  𝐷𝑒𝑟𝑒 𝑓
                                     !x, ℎ, 𝑆 {ℎ(𝑆 (x)), ℎ, 𝑆
                                            ℓ ∉ dom(ℎ)
                                                                  𝑅𝑒 𝑓
                                   ref x, ℎ, 𝑆 {ℓ, ℎ[ℓ:=𝑆 (x)], 𝑆

                              𝑆 (x)⊆pi         ei, ℎ, 𝑆 {v, ℎ𝑖 , 𝑆𝑖
                                                                             𝑀𝑎𝑡𝑐ℎ
                       (match x {p1 →e1 | · · · |pn →en }), ℎ, 𝑆 {v, ℎ𝑖 , 𝑆𝑖

F    THE LEAN TYPE-CHECKER
The Lean development additionally yields a reflective, self-certifying type-checker. Where the deriva-
tions of Sec. 7 are built by hand (or by the small forward tactic), the checker turns the meta-theory
into an executable decision procedure and lets each program discharge its own typing derivation
by computation.
Type Safety via Hoare Logic with Separation and Pure Types                                           35


F.1   A checker proved sound once
For each layer we implement the forward rules as computable functions: an algorithmic subtyp-
ing subTyAlg, a state-entailment test entailsAlg, and a recursive checkExpr over expressions
(checkSep in the separation layer M2; checkHO in the higher-order layer M3), and prove once that
each is sound against the inductive derivation relation Deriv:
                       checkExpr Γ Δ 𝑒 𝑟 = some Δ′ =⇒ Deriv Γ Δ 𝑒 𝑟 Δ′ .
Each soundness theorem is itself axiom-clean ({propext, Classical.choice, Quot.sound}). Given it,
an individual program’s typing derivation follows purely by computation, with no per-example
proof. The checker is deliberately sound but incomplete: it checks a program against a supplied
specification rather than inferring one. Its architecture is sketched next, and the machinery behind
the red-black, heap-atom, and packed-precondition developments is detailed in Appendix G.

F.2   Checker architecture
Three design choices make the checker both executable and extensible.
   Law registries. The registry-based type predicates of Sec. 7 are consumed by the checker through
per-predicate law rows: a fold row (how a constructor application folds back into the predicate),
cover rows (which constructors a predicate can exhibit), and disjointness rows. Extending coverage
to a new data structure means registering its laws; the checker itself, and its soundness proof, are
untouched. The red-black development registers three such predicates; the sized-list and sized-tree
predicates of the arithmetic engine below are two more.
   Disjunctive states with certified pruning. Checker states are disjunctions of conjunctive typing
contexts. A match splits the state per pattern package, entailments are checked per disjunct, and
infeasible disjuncts are discharged by covers-based refutation: a certified unsatisfiability test prunes
branches whose recorded facts contradict the registered cover laws. This is the mechanism behind
path-sensitive matches and the red-black colour analysis.
   Heap-atom entailment and unfolding (the separation layer). State entailment over heaps is a
goal-directed atom-cover procedure: each goal atom must be covered by a premise atom under
a small set of certified rows (identity, alias redirection, weakening, and per-predicate fold rows);
leftover premise atoms are framed away. Packed preconditions are handled by registered unfold
templates, justified once per predicate by a store-extension lemma.
   Quantified families by reflection. Three wrappers turn one symbolic checker run into a theorem
quantified over a family: element-type polymorphism (∀𝑇 , the polyReduce symbolic-reduction
macro), successor height indices (∀ℎ, the sorted quantifier), and affine index valuations (∀𝜌, the
allIdx wrapper of the arithmetic engine below).

F.3   Two discharge modes
Typing derivations are obtained by computation in one of two modes. (i) At a ground instantiation,
checkExpr_reflect(bynative_decide) runs the compiled checker and lifts its Boolean result
through the soundness theorem, with no per-example lemmas. The one price is that native_decide
adds a compiler-reduction axiom to that example’s footprint — the only departure from the devel-
opment’s otherwise minimal axiom base; the checkers’ soundness proofs themselves do not use it.
(ii) Results quantified over open types (∀𝑇 ) cannot use native_decide, which needs a closed term;
they are discharged by symbolic reduction of the checker (the polyReduce macro), feeding the
per-type-variable leaf facts as hypotheses. These polymorphic theorems are therefore native-free
and fully axiom-clean. The two modes differ in cost by orders of magnitude, for a reason com-
plementary to their trust. native_decide compiles the checker and runs it as machine code on
packed runtime data (with in-place update and machine integers), taking exactly one branch at
36                                                                                      Li, Foo, Ta, and Chin


each ground match. Symbolic mode instead reduces the checker by the kernel’s own definitional
computation over Expr terms: unary/constructor-encoded data, copying substitution, no sharing,
and, because the type or height variable stays open, simp-driven case-splitting rather than a single
concrete branch. The resulting proof is then re-checked by the kernel. Millisecond ground runs
thus become multi-minute symbolic ones; the price buys a minimal, oracle-free trusted base.

F.4   Certified linear arithmetic for sized types
Beyond the successor fragment used by the red-black development, the checker carries a general
affine-equality linear-arithmetic engine, realising the equality part of the decidable fragment
outlined in App. B.3 with no SMT oracle (consistent with Sec. 1). Index expressions are reified
into a canonical form (an integer constant plus a sorted list of variable coefficients), and index
equalities and disequalities are decided by a single sound Boolean procedure (idxEqB/idxNeqB;
the equality test’s soundness proof is axiom-free, and completeness is deliberately not claimed).
Sized predicates (𝐿𝑖𝑠𝑡 (𝑇 , 𝑛), and size-indexed trees with 1+𝑎+𝑏 at each node) are registered as
law rows over this engine, and ∀-index families are certified by one Boolean run through the
allIdx reflect wrapper. The “one Boolean run per ∀-index family” description is exactly true of this
call-site reflect wrapper; the flagships’ own well-formedness ∀𝜌 obligation instead closes via a small
by_cases family (3 cases) of symbolic checker runs, not a single uniform run. Two further flagships
are checker-certified end-to-end on this engine, both native-free and axiom-clean: sized append
(𝐿𝑖𝑠𝑡 (𝑇 , 𝑛)×𝐿𝑖𝑠𝑡 (𝑇 , 𝑚) ⇒ 𝐿𝑖𝑠𝑡 (𝑇 , 𝑛+𝑚), for all integers 𝑛, 𝑚) and exact-length length (𝐿𝑖𝑠𝑡 (𝑇 , 𝑛) ⇒
{𝑛}). In each, the sized-list precondition is uninhabited at 𝑛 < 0, so the semantic content lives
at 𝑛, 𝑚 ≥ 0; append is witnessed at 𝑛 = 2, 𝑚 = 1. Their sized-list entailments run through per-
disjunct certifiers such as slMemOkB, rather than one uniform entailsAlg run. A sized-tree node
cons(l, r) : ST(T, {s}) decomposes existentially as 𝑠 = 1+𝑎+𝑏, with the children’s sizes 𝑎, 𝑏 not
determined by 𝑠 — a decomposition no single-pair match field slot can express directly. A declared-
post frame gate (checkSTMatchTo, paralleling the SortedList gate below) crosses this wall instead,
and two further flagships are checker-certified end-to-end on it, both native-free and axiom-clean:
size (double-rebound destruction through both children; the result is the size itself) and mirror
(destruction and reconstruction — the rebuilt node’s commuted child order 1+𝑏+𝑎 is reconciled
against the destructed 1+𝑎+𝑏 by a dedicated semantic bridge, mirror_consEntails). This closes
the sized-tree case; the semantic-only certificate from an earlier iteration (streeAt_mirrorV, proved
directly over the tree’s value-level semantics) survives unchanged, as a complementary account.
Table 4 records both new flagships.

F.5   Certified linear arithmetic for the inequality fragment
On top of the affine-equality engine, the checker also carries a certified inequality decision procedure.
Index expressions are compared by idxLeB, a sound unit-Farkas worklist procedure that saturates
hypothesis differences by unit-coefficient subtraction and accepts once some saturated difference
closes to a nonnegative constant; its soundness proof is clean (the classical axiom base, rather
than axiom-free, since it also needs genuine Int order reasoning). Completeness is deliberately
not claimed: coefficient scaling (e.g. deriving 2𝑥≤𝑎+𝑏 from 𝑥≤𝑎 ∧ 𝑥≤𝑏) and equality-tightening
lie outside the unit-Farkas fragment. A closed-only assertion atom idxLe mirrors the existing
index-singleton semantics, and a comparison-derivation refinement of < on index-typed operands
(Deriv.binopLtIdx) packages each branch’s guard into a negation-normalised idxLe atom feeding
this engine.
   On this footing the checker certifies a SortedList(T, lo, hi) predicate (a structural fold on the
tail whose lower bound is rebound at each matched element), together with a bespoke ∀-element
destruction rule (Deriv.matchSortedCons) that universally quantifies the cons premise over the
Type Safety via Hoare Logic with Separation and Pure Types                                          37


matched element’s value, closing every emitted index atom at that value. Three flagships are
checker-certified end-to-end on it, all native-free and axiom-clean: head (the shared post collapses
to a scalar range-validity atom, so the per-element bound is instead certified in the destruction
rule’s own side-condition witness; partial correctness on the cons case — the nil arm is deliberately
evaluation-stuck, so nothing is claimed on empty input), member (an honest Bool post via rebound
recursion and a double-< comparison encoding), and, as the campaign’s capstone, sorted insert
((𝐼𝑛𝑡, 𝑆𝑜𝑟𝑡𝑒𝑑𝐿𝑖𝑠𝑡 (𝐼𝑛𝑡, 𝑙𝑜, ℎ𝑖)) ⇒ 𝑆𝑜𝑟𝑡𝑒𝑑𝐿𝑖𝑠𝑡 (𝐼𝑛𝑡, 𝑙𝑜, ℎ𝑖), a genuine end-to-end sorted insertion). As
with the sized-list rows, the vacuity corners are stated honestly: insert’s closed precondition
is uninhabited outside 𝑙𝑜≤𝑥≤ℎ𝑖 and head’s exactly at 𝑙𝑜>ℎ𝑖 (the semantic content lives inside
the range, witnessed at concrete values), while member’s precondition carries no range atom and
is satisfiable broadly. Each flagship’s ∀-element cons-branch premise is discharged by a named
semantic side condition (SoConsObligation) rather than by the structural checker gate directly:
the declared-post frame gate used by construction flagships such as insert deliberately does not
re-run the cons branch at its reserved index variable, an honest, disclosed checker incompleteness
that costs nothing, since the real premise is supplied by the side condition instead. As with the
equality engine, no completeness claim is made anywhere, for the engine or for the checker. Table 4
lists all three flagships under the inequality-fragment group.
   With the two sized-tree flagships above, the checker now discharges every index-language
construct the paper’s data-structure predicates use: there is no remaining documented index-
language boundary. What remains are limits on the completeness of the certified procedures
themselves, not on coverage. The comparators idxEqB (affine equality) and idxLeB (affine inequal-
ity) are both sound but not claimed complete: idxLeB decides only the unit-coefficient Farkas
fragment, and coefficient scaling or equality-tightening lie outside it (App. B.3). The declared-
post frame gates checkSTMatchTo and checkSortedMatchTo each deliberately omit re-running
their ∀-child/∀-element destruction premise at its own reserved index variable, discharging it
instead through a named semantic side condition — an honest, disclosed incompleteness that
costs nothing, since the real premise is supplied that way regardless. The sized-tree predicate’s
element type, like SortedList’s, is carried shape-only (semantically inert). And every flagship’s
vacuity corner is disclosed per instance: both size and mirror are vacuous at 𝑠<0 (formalised as
mirrorPre_vacuous).

G    DETAILS OF LEAN MACHINERY
   Proof size and checking time. Table 2 reports, for each machine-checked example, the size of
its Lean script (the program, its type specification, and the proof, in lines) and the time Lean
takes to elaborate and kernel-check it. These are proof-assistant elaboration times for the meta-
level derivations, and are mostly small: the bulk of the examples check in under a second (tens
to a few hundred milliseconds); the heaviest are the typed-queue pair (≈4.9 s and ≈3.7 s) and
the five-function Okasaki RBTree_insert, whose full colour/black-height derivation takes about
15 s, bringing the whole suite to about 39 s. The proof-script size is the more informative fig-
ure, reflecting the effort to construct each typing derivation and instantiate soundness; it is a
one-time meta-theoretic cost, not paid again when the TypeHL verifier checks user programs.
The M1 proofs are written with a small forward-reasoning tactic (forward/ml_side/ml_entail)
that applies the Hoare rules and discharges the decidable side conditions automatically: it makes
the scripts more compact at a modest cost in elaboration time, since the generic tactics per-
form broader simp/decide search than the hand-written proofs they replace. The suite spans
the paper’s worked examples (path-sensitive accessors and type-dispatch of Sec. 2, function com-
position) together with a representative selection of standard benchmarks and standard-library
functions. These include type-dispatch (shape_funs), list construction (List.append, List.rev),
38                                                                                   Li, Foo, Ta, and Chin


a colored red-black tree with a full balancing predicate (both a recursive search, RBTree_member,
and a verified Okasaki insert, RBTree_insert, over RBTree(Int, c, h)), reference swap with must-
aliasing, a separation-typed Queue, and the higher-order standard-library functions List.map,
List.filter, and List.fold_left. Adding swap and the operational Queue demo to the separa-
tion layer required no new rule, while the fully typed Queue.enqueue/Queue.dequeue rows are
enabled by the inductive heap-predicate layer and exact-content strong-update rules described
below; append/rev, which construct lists, are enabled by a data-constructor rule added to the
pure layer. The map/filter/fold_left examples exercise a genuine integration. The higher-order
layer, which already has closures, application, and the behavioural function type, is extended
with the recursive List(T) predicate (its interpretation, a data-constructor typing rule, and match
field-type propagation). A pure function parameter may then be applied elementwise across a
list under a recursive specification: e.g. map at type (𝐴→𝐵, 𝐿𝑖𝑠𝑡 (𝐴))⇒𝐿𝑖𝑠𝑡 (𝐵) and fold_left at
((𝐴𝑐𝑐, 𝐴)→𝐴𝑐𝑐, 𝐴𝑐𝑐, 𝐿𝑖𝑠𝑡 (𝐴))⇒𝐴𝑐𝑐. The suite’s newest addition is a general linear-arithmetic
culminating example. Two sized-list flagships — append (𝐿𝑖𝑠𝑡 (𝑇 , 𝑛) × 𝐿𝑖𝑠𝑡 (𝑇 , 𝑚) ⇒ 𝐿𝑖𝑠𝑡 (𝑇 , 𝑛+𝑚),
for all integers 𝑛, 𝑚; at 𝑛 < 0 the sized-list precondition is uninhabited, so the semantic content
lives at 𝑛, 𝑚 ≥ 0, witnessed at 𝑛 = 2, 𝑚 = 1) and exact-length length (𝐿𝑖𝑠𝑡 (𝑇 , 𝑛) ⇒ {𝑛}, same
vacuity at 𝑛 < 0) — are checker-certified end-to-end on a general affine-equality index engine
(Sec. B.3). Two sized-tree flagships, size (destruction through both children; the result is the size)
and mirror (destruction and reconstruction, the commuted child order reconciled by a dedicated
semantic bridge), are checker-certified end-to-end too, via a declared-post frame gate that crosses
the existential child-size decomposition a single-pair match cannot express — mirror upgraded
from the semantic-only certificate of an earlier iteration, and there is no remaining documented
index-language boundary. A companion inequality-fragment engine (a certified unit-Farkas decision
procedure) checker-certifies a SortedList(T, lo, hi) predicate and, through a bespoke ∀-element
destruction rule, three further flagships end-to-end: head, member, and, as the campaign’s capstone,
sorted insert ((𝐼𝑛𝑡, 𝑆𝑜𝑟𝑡𝑒𝑑𝐿𝑖𝑠𝑡 (𝐼𝑛𝑡, 𝑙𝑜, ℎ𝑖)) ⇒ 𝑆𝑜𝑟𝑡𝑒𝑑𝐿𝑖𝑠𝑡 (𝐼𝑛𝑡, 𝑙𝑜, ℎ𝑖)).
Table 2. Lean examples: proof-script size (program + spec + proof, in lines) and elaboration time (ms).
† composition-level figure (see below).



 Example                   Feature exercised                                 Proof (lines)   Lean (ms)
 M1 — pure fragment
 id                        result / singleton type                                     61            85
 tail                      path-sensitivity, Err on Nil                               241           328
 length                    recursion                                                  201           227
 fst                       Cons field-type propagation                                257           350
 length (on List(Int))     recursive List predicate                                   271           310
 id (∀𝑇 . 𝑇 →𝑇 )           type-variable polymorphism                                  98           163
 length                    polymorphic recursion                                      260           475
 (∀𝑇 . 𝐿𝑖𝑠𝑡 (𝑇 )⇒𝐼𝑛𝑡)
 treeSize                  user-defined predicate (Tree)                              265           370
 constFst                  multi-argument function                                    104           137
 head                      path-sensitive accessor, Err on Nil                        210           381
 shape                     type-dispatch, union result Int∨Str                        232           416
 append                    list construction + recursion                              283           640
 rev                       accumulator recursion + construction                       277           614
 member                    colored-shape tree predicate demo (registry)               262           383
 M1 + integer arithmetic
 inc                       base-type arrow, Int closure                               127           206
 plus                      binary Int operator                                         93           153
 List.nth                  polymorphic path-sensitive Err case spec                   762          1316
Type Safety via Hoare Logic with Separation and Pure Types                                                39


Example                   Feature exercised                                       Proof (lines)   Lean (ms)
str_of_int                digit-match, div/mod, string concat, recursion                    558        1192
M1 + balancing predicate
RBTree_member             recursive search over balanced RBTree(Int, c, h)                  960       1019
RBTree_insert             Okasaki insert; ∀ℎ spec states result colour and black-         5090       15034
                          height
M2 — separation / Ref heaps
assign (strong update) flow-sensitive mutation, Frame                                       255        105
+ Frame
Frame across a call       callee-footprint Frame                                            213        169
Frame across a match      Frame over match                                                  199        132
weakening x↦→t⇒x:t        irreversible weakening                                             62         20
g(x, y)=mkref x           multi-argument heap function                                      163        193
swap                      Ref exchange, must-alias, framed update                           247        142
Queue                     separation, front/rear must-alias (operational demo)              147        134
M2 + inductive heap predicates
Queue.enqueue             typed two-pointer enqueue; heap-content strong up-                907       4862
                          date
Queue.dequeue             Err on empty via must-alias; element typing via eq-             1162        3722
                          slot match
M3 — higher-order
apply                     higher-order application                                           85        116
𝜆𝑥 . 𝑦                    environment-capturing closure                                     114        132
pickFst(𝑥, 𝑦)             multi-argument top-level function                                 132        191
𝜆(𝑥, 𝑦). 𝑥                multi-argument closure                                            102        144
compose                   function composition 𝑔◦𝑓 (𝐼𝑛𝑡→𝑆𝑡𝑟 →𝐵𝑜𝑜𝑙)                          192        170
M3 + recursive List(T) predicate
map                       HO map, list construction + recursion                             365        799
fold_left                 HO fold, 𝑛-ary function parameter                                 344        588
filter                    HO filter, nested boolean match                                   456        856
append                    list concatenation over List(T)                                   292        456
rev                       accumulator reversal over List(T)                                 301        442
M3 + Option constructors
Option.get                path-sensitive case spec, Err on None                             297        313
Option.map                HO map over Option(T), two-case spec                              372        474
Option.bind               HO bind, Option(T)-returning parameter                            341        404
M1 + sized predicates (LIA)
append                    sized-list append, 𝐿𝑖𝑠𝑡 (𝑇 , 𝑛) × 𝐿𝑖𝑠𝑡 (𝑇 , 𝑚)      ⇒             252        87†
                          𝐿𝑖𝑠𝑡 (𝑇 , 𝑛+𝑚), all integers (𝑛<0 vacuous pre, content
                          at 𝑛, 𝑚≥0), general affine-equality engine
length                    exact length, 𝐿𝑖𝑠𝑡 (𝑇 , 𝑛) ⇒ {𝑛}, general affine-                 244        77†
                          equality engine
size                      sized-tree destruction, 𝑆𝑇 (𝑇 , {𝑠}) ⇒ {𝑠}, double-               351        54†
                          rebound recursion through both children, result IS
                          the size (checker-certified)
mirror                    sized-tree destruction + reconstruction, size 1+𝑎+𝑏               406        55†
                          preserved ∀𝑠 under the commuted reassembly
                          (checker-certified; upgraded from a semantic-only
                          certificate)
M1 + SortedList (inequality fragment)
head                      SortedList destruction; per-element bound certi-                  180        10†
                          fied in the ∀-element side-condition witness
40                                                                                         Li, Foo, Ta, and Chin


 Example                  Feature exercised                                        Proof (lines)   Lean (ms)
 member                   comparison traversal, rebound recursion, honest                    302        197†
                          Bool post
 insert                   end-to-end          sorted        insertion,      post            986           62†
                          𝑆𝑜𝑟𝑡𝑒𝑑𝐿𝑖𝑠𝑡 (𝐼𝑛𝑡, 𝑙𝑜, ℎ𝑖) (vacuous pre outside 𝑙𝑜≤𝑥≤ℎ𝑖)
 Total                                                                                   20081         38905


   Measurement. Times are Lean’s internal elaboration timings (Lean 4.30.0, Intel Xeon E-2278G),
excluding the fixed per-file import overhead; the typed Queue.enqueue/Queue.dequeue rows use
the same single-threaded profiler (async elaboration disabled, per-entry sum) as App. F, while
the earlier Queue row is the operational demo. The RBTree_insert/RBTree_member rows cover
the full colour/black-height balancing development (a five-function Okasaki insert; the shared
RBTree(Int, c, h) family is counted with RBTree_member). † The append/length/size/mirror and
SortedList rows report a composition-level figure: the elaboration time of the flagship’s own
top-level theorem(s), composing cached per-branch bodyChecks/obligation lemmas rather than a
full from-scratch proof-script; the dominant cost is the checker suite’s own elaboration (App. F).
The size and mirror rows are both checker-certified end-to-end (App. F); mirror upgrades the
semantic-only certificate of an earlier iteration, which survives unchanged as a complementary
account (streeAt_mirrorV).
   Coverage and modeling boundaries. Table 3 maps a suite of standard benchmarks and standard-
library functions to their status in the mechanisation. The GADT-style balancing example of
Sec. 2.4 is now mechanised: the indexed predicate RBTree(T, c, h) is registered semantically (its
interpretation rbAt pins the root colour c and black-height h, unfolding to the leaf/black/red
disjuncts with colour-correlated children), and the spec-level sorted quantifier ∀ℎ:Nat realises the
black-height parameter of that predicate: instantiated at integer singletons, with recursive calls
at ℎ−1 (and, for a red parent, at ℎ). On this footing the recursive RBTree_member search and the
five-function Okasaki RBTree_insert both check, the latter against ∀ℎ. (𝐼𝑛𝑡, RBTree(𝐼𝑛𝑡, 𝑐, ℎ)) ⇒
RBTree(𝐼𝑛𝑡, Black, ℎ) ∨ RBTree(𝐼𝑛𝑡, Black, ℎ+1): the postcondition states the result’s exact colour
and black-height: black, at height ℎ or ℎ+1 (the latter when blackening a red root), exactly as
red-black insertion behaves. As in Sec. 2.4’s definition, the predicate constrains colour and black-
height only; key ordering is not part of it, so the spec makes no BST claim. The mechanisation
also instantiates the decidability recipe of Sec. B.3: rbAt is structurally recursive and its index
constraints (ℎ = ℎ 1 +1, equal sibling heights) stay within linear integer arithmetic. These are dis-
charged here once, inside the kernel-checked unfold/fold lemmas, and are now also implemented as
a certified successor sub-fragment inside the reflective checker itself (App. F), rather than by an SMT
solver, consistent with the solver-free positioning of Sec. 1. The checker’s general affine-equality
index engine, which certifies the sized-list flagships of Table 2 below, is a separate, now-landed
capability described under Table 4’s LIA rows in App. F. The typed Queue is now mechanised as
well, closing the last open row: every Sec.-evaluation benchmark and standard-library entry of
Table 3 is machine-checked. The mechanisation adds an inductive heap-predicate layer over M2.
An exact-footprint list-segment predicate realises the paper’s LSeg, and the paper’s correspondence
𝑥↦→List(𝑇 ) ⇔ 𝑥↦→LSeg(𝑇 , Nil) holds; in this encoding it is definitional (the list predicate unfolds
to the nil-terminated segment, proved as hlist_iff_lseg_nil). A heap-content strong-update rule
(assignExact) types a pointer write together with the structural content of the cell it overwrites,
carrying no content-type side condition: the separating-conjunction split of the precondition does
the work. The empty-queue case of dequeue realises the paper’s front/rear must-alias as ghost
sharing (both pointer cells are owned through one shared ghost) and returns Err structurally on
Type Safety via Hoare Logic with Separation and Pure Types                                             41


the sentinel. What remains are honest modeling boundaries, not coverage gaps. First, the queue
theorems are body-level ghost-parameterized SemValid triples, since M2’s spec discipline keeps
function specifications heap-free (the same claim form as every existing M2 heap example). Sec-
ond, on the match-free fragment (straight-line code and calls with match-free bodies) the Frame
rule now also covers these heap-predicate atoms (hpred/ptsEq/ptsCon), with no FrameNoCon
side-condition there (SemValid.frame_matchfree); the flagships are enqueue_frames_queue (a
disjoint packed queue framed across enqueue, NATIVE-FREE, clean-3) and ptsCon_frame (an
exact Cons cell framed across a strong update). Across a match the FrameNoCon side-condition
remains, and is essential to the operational-locality theorem (frameNoCon_essential, a formal
countermodel: a frame-owned con can flip a match’s outcome from abort to normal termination);
the analogous question at the SemValid level is left open, since its abort-permissive arm makes
that flip invisible there. Third, the balancing predicate constrains colour and black-height only,
so no BST key-ordering claim is made (as above). The reflective checker of App. F now auto-
mates the inductive heap-predicate atoms of the Queue layer too: all three queue theorems —
enqueue_semvalid_reflective (at the fixed ghost names f/ga/gb) and the two dequeue twins
dequeue_semvalid_empty_reflective/dequeue_semvalid_cons_reflective (each certifying
the exact SAME closed SemValid proposition as its hand twin) — are discharged by the M2 checker
via native_decide, folding/packing the exact heap atoms through the heapLawsEnv registry.
Both the red-black rows and the queue rows are thus now also checked automatically by that
reflective checker (the hand derivations here remain the derivation-effort record; see App. F).
The checker’s coverage goes further still: a packed-precondition wrapper unfolds the opaque
hpred queue invariant itself at the point a triple is checked, so enqueue_semvalid_packed and
dequeue_semvalid_packed certify both operations directly from a single ghost-free hpred pre-
condition (dequeue’s post the honest disjunction of its two arms), each by one native_decide call
(App. F). None of these is a soundness obstacle.

Status                                     Benchmark / stdlib function
mechanised (M1)                            tail, length, length_generic, singleton_type, shape_funs
mechanised (M1 + arith)                    inc, (+), str_of_int (i.e. basic), List.nth
mechanised (M1 + balancing predicate)      RBTree_insert, RBTree_member
mechanised (M1 + LIA)                      append (sized), length (sized, exact), size/mirror (sized tree,
                                           checker-certified)
mechanised (M1 + inequality LIA)           SortedList.insert, SortedList.head, SortedList.member
mechanised (M2)                            stateful_funs, refs_pure, refs_sep, swap_pure, swap_sep
mechanised (M2 + heap predicates)          Queue.enqueue, Queue.dequeue
mechanised (M3 + List)                     map, List.map, List.filter, List.fold_left, List.append,
                                           List.rev, List.length
mechanised (M3 + Option)                   Option.map, Option.bind, Option.get
Table 3. Status of a suite of standard benchmarks and standard-library functions in the Lean mechanisation.




   The reflective type-checker: architecture. This section details the reflective, self-certifying type-
checker of App. F. The checker (about 20,600 lines beyond the derivations, atop a further ≈14,700
lines of certified index engines) is a per-layer computable forward checker. For each layer we
implement the forward rules as functions — an algorithmic subtyping subTyAlg, a state-entailment
test entailsAlg, and a recursive checkExpr over expressions in the pure layer M1 (checkSep
in M2; subTyAlgHO/entailsAlgHO/checkHO in M3) — and prove once that each is sound with
42                                                                                         Li, Foo, Ta, and Chin


respect to the inductive derivation relation Deriv (theorems checkExpr_sound, checkSep_sound,
checkHO_sound), each itself axiom-clean ({propext, Classical.choice, Quot.sound}).
   Decision devices. Behind the two modes the checker settles the decidable side conditions of
the rules with a small library of provably sound decision procedures: list-/Bool-exhaustiveness
laws (listCoversB, boolCoversB); unsatisfiable-disjunct detection (pureUnsat, findNegMem); pos-
itive type-disjointness (tyDisjB, M3, which refutes the vacuous otherwise and mismatched
branches of the two-case Option specs); equality-aware membership with binder projection
(sProject); polymorphic-call instantiation inference (inferInst, M1) and let-result-variable align-
ment (letResVar, M1); and a bounded coverage decision procedure (coversB/coverUnsat with
pureDisjoint, tautNegUnsat, varPost, M1). This last procedure refutes the recursive-call cover-
age tail ctx ∧ ¬(𝑔1 ∨ · · · ∨𝑔𝑘 ) by case-splitting each list context into its precise Nil∨Cons unfold
and each guard singleton by excluded middle, until every leaf is subsumed. In the symbolic mode
each type parameter flows through only at opaque leaves, guarded by decidable side conditions
(subTyAlgTT, tyEqBTT, findNegMem . . . = none) that are genuinely necessary: a closure-singleton
type, for instance, is not reflexively a subtype of itself. The algorithmic subtyping and entailment
are deliberately sound but incomplete (function types are compared reflexively, heap entailment by
separating-conjunct matching), mirroring a practical analyser.
   Automatic examples (Table 4). The pure and higher-order checkers cover all forward rules,
so the paper’s worked examples check reflectively without hand-written proofs. In M1 this
includes integer/string arithmetic (concat/div/mod) so that str_of_int and monomorphic
nth check, and polymorphic-function calls (the instantiation inferred by inferInst). In M3 it
includes closure application and List(T) field-type propagation, so that the map, filter, and
fold_left bodies check; the separation checker covers the heap-manipulating rules including
strong-update assign. For eight higher-order functions we go further and discharge the
whole-program well-formedness obligation WFEnv by native_decide, then lift each through
HO.soundness to a full semantic-validity statement: the five recursive list functions map,
filter, fold_left, append, rev and the three Option functions Option.get, Option.map,
Option.bind, certifying specifications such as map : (𝐼𝑛𝑡→𝐵𝑜𝑜𝑙, 𝐿𝑖𝑠𝑡 (𝐼𝑛𝑡))⇒𝐿𝑖𝑠𝑡 (𝐵𝑜𝑜𝑙) and
Option.get : 𝑂𝑝𝑡𝑖𝑜𝑛(𝐼𝑛𝑡)⇒𝐼𝑛𝑡∨Err. All eight are additionally proved polymorphic in their
element/accumulator types (map : ∀𝐴 𝐵. (𝐴→𝐵, 𝐿𝑖𝑠𝑡 (𝐴))⇒𝐿𝑖𝑠𝑡 (𝐵), and so on) by the native-free
symbolic mode; and in the pure layer id, length, and nth likewise check for all element types
𝑇 (nth : ∀𝑇 . (𝐿𝑖𝑠𝑡 (𝑇 ), 𝐼𝑛𝑡)⇒𝑇 ∨Err, native-free), nth’s three-case path-sensitive specification
additionally exercising the coverage decision procedure above.
Table 4. Reflective-checker results by layer. Mode: native_decide (ground, +axiom) or symbolic (native-
free); elaboration ms; † composition-level.

What is certified                                                               Mode                Time (ms)
  M1 — pure fragment
ground reflective programs (16)                                                 native_decide             ≲100
(inc, +, div, mod, concat, str_of_int, mono nth, id/length poly-calls)
id : ∀𝑇 . 𝑇 ⇒𝑇 (type-variable polymorphism)                                     symbolic                  1346
length : ∀𝑇 . 𝐿𝑖𝑠𝑡 (𝑇 )⇒𝐼𝑛𝑡 (polymorphic recursion)                             symbolic                  1426
nth : ∀𝑇 . (𝐿𝑖𝑠𝑡 (𝑇 ), 𝐼𝑛𝑡)⇒𝑇 ∨Err (path-sensitive spec + coverage procedure)   symbolic                  2706
  M1 — red-black balancing (reflective)
RBTree_member : (𝐼𝑛𝑡, RBTree(𝐼𝑛𝑡, 𝐵𝑜𝑜𝑙, 𝐼𝑛𝑡))⇒𝐵𝑜𝑜𝑙 (recursive search)           native_decide             ≲100
Type Safety via Hoare Logic with Separation and Pure Types                                                      43


What is certified                                                                        Mode            Time (ms)
RBTree_insert : ∀ℎ. (𝐼𝑛𝑡, RBTree(𝐼𝑛𝑡, 𝑐, ℎ))⇒                                            symbolic         ≈15 min
RBTree(𝐼𝑛𝑡, Black, ℎ)∨RBTree(𝐼𝑛𝑡, Black, ℎ+1) (five-function)
  M1 — general affine-equality LIA (reflective)
append : ∀𝑛 𝑚. (𝐿𝑖𝑠𝑡 (𝑇 , 𝑛), 𝐿𝑖𝑠𝑡 (𝑇 , 𝑚))⇒𝐿𝑖𝑠𝑡 (𝑇 , 𝑛+𝑚) (sized-list append, all in-   symbolic              87†
tegers — 𝑛<0 vacuous pre, content at 𝑛, 𝑚≥0; no per-size checker surgery)
length : ∀𝑛. 𝐿𝑖𝑠𝑡 (𝑇 , 𝑛)⇒{𝑛} (exact-length post = the size itself; same 𝑛<0 vacu-       symbolic              77†
ity as append)
size : ∀𝑠. 𝑆𝑇 (𝑇 , 𝑠)⇒{𝑠} (sized-tree destruction via a declared-post frame gate,        symbolic              54†
double-rebound recursion through both children; result IS the size itself; vacuous
pre at 𝑠<0)
mirror : ∀𝑠. 𝑆𝑇 (𝑇 , 𝑠)⇒𝑆𝑇 (𝑇 , 𝑠) (sized-tree destruction AND reconstruction; size      symbolic              55†
1+𝑎+𝑏 preserved under the commuted reassembly 1+𝑏+𝑎, reconciled by the
semantic bridge mirror_consEntails — upgraded from a semantic-only cer-
tificate; vacuous pre at 𝑠<0, formalised as mirrorPre_vacuous; no remaining
documented index-language boundary)
  M1 — SortedList (inequality fragment, reflective)
head : 𝑆𝑜𝑟𝑡𝑒𝑑𝐿𝑖𝑠𝑡 (𝐼𝑛𝑡, 𝑙𝑜, ℎ𝑖), shared post = range-validity 𝑙𝑜≤ℎ𝑖 (per-element         symbolic              10†
bound certified in the ∀-element side-condition witness; partial correctness on
cons)
member : (𝐼𝑛𝑡, 𝑆𝑜𝑟𝑡𝑒𝑑𝐿𝑖𝑠𝑡 (𝐼𝑛𝑡, 𝑙𝑜, ℎ𝑖))⇒𝐵𝑜𝑜𝑙 (honest Bool post; rebound recur-          symbolic             197†
sion, double-< encoding)
insert : (𝐼𝑛𝑡, 𝑆𝑜𝑟𝑡𝑒𝑑𝐿𝑖𝑠𝑡 (𝐼𝑛𝑡, 𝑙𝑜, ℎ𝑖))⇒𝑆𝑜𝑟𝑡𝑒𝑑𝐿𝑖𝑠𝑡 (𝐼𝑛𝑡, 𝑙𝑜, ℎ𝑖)                        symbolic              62†
(end-to-end sorted insertion; ∀-element cons premise via the SoConsObligation
semantic side condition; vacuous outside 𝑙𝑜≤𝑥≤ℎ𝑖)
  M2 — separation / Ref heaps
separation programs (8) + pipeline                                                       native_decide       ≲100
(mkref, constr, deref, cast, let, strong-update assign, match, call)
Queue_enqueue : enqueue triple at fixed ghosts (typed two-pointer queue)                 native_decide       ≲100
Queue_dequeue_empty : dequeue triple, res : Err (empty must-alias case)                  native_decide       ≲100
Queue_dequeue_cons : dequeue triple, res : Int (non-empty case)                          native_decide       ≲100
Queue_enqueue_packed : opaque hpred atom + v : int                                       native_decide       ≲100
(ghost-free packed precondition)
Queue_dequeue_packed : bare hpred atom, disjunctive post                                 native_decide       ≲100
(ghost-free packed precondition)
  M3 — higher-order
core HO + list whole-programs (11)                                                       native_decide       ≲200
(apply/closures/compose; map, filter, fold_left, append, rev WFEnv)
Option whole-programs (3) (Option.get/map/bind WFEnv, two-case tyDisjB)                  native_decide        537
map : ∀𝐴 𝐵. (𝐴→𝐵, 𝐿𝑖𝑠𝑡 (𝐴))⇒𝐿𝑖𝑠𝑡 (𝐵) (polymorphic whole-program)                         symbolic            1966
fold_left : ∀𝐴𝑐𝑐 𝐴. ((𝐴𝑐𝑐, 𝐴)→𝐴𝑐𝑐, 𝐴𝑐𝑐, 𝐿𝑖𝑠𝑡 (𝐴))⇒𝐴𝑐𝑐                                    symbolic            2308
(polymorphic whole-program)
filter : ∀𝐴. (𝐴→𝐵𝑜𝑜𝑙, 𝐿𝑖𝑠𝑡 (𝐴))⇒𝐿𝑖𝑠𝑡 (𝐴) (polymorphic whole-program)                     symbolic            1214
append : ∀𝑇 . (𝐿𝑖𝑠𝑡 (𝑇 ), 𝐿𝑖𝑠𝑡 (𝑇 ))⇒𝐿𝑖𝑠𝑡 (𝑇 ) (polymorphic whole-program)               symbolic            2854
rev : ∀𝑇 . (𝐿𝑖𝑠𝑡 (𝑇 ), 𝐿𝑖𝑠𝑡 (𝑇 ))⇒𝐿𝑖𝑠𝑡 (𝑇 ) (polymorphic whole-program)                  symbolic            1519
Option.get : ∀𝑇 . 𝑂𝑝𝑡𝑖𝑜𝑛(𝑇 )⇒𝑇 ∨Err (polymorphic two-case spec)                          symbolic            1232
Option.map : ∀𝐴 𝐵. (𝐴→𝐵, 𝑂𝑝𝑡𝑖𝑜𝑛(𝐴))⇒𝑂𝑝𝑡𝑖𝑜𝑛(𝐵)                                            symbolic            3165
(polymorphic whole-program)
Option.bind : ∀𝐴 𝐵. (𝐴→𝑂𝑝𝑡𝑖𝑜𝑛(𝐵), 𝑂𝑝𝑡𝑖𝑜𝑛(𝐴))⇒𝑂𝑝𝑡𝑖𝑜𝑛(𝐵)                                   symbolic            3392
(polymorphic whole-program)
44                                                                                 Li, Foo, Ta, and Chin


    Reflective red-black balancing (Table 4). The colour/black-height RBTree/Node development of
Table 5 (once hand-derived only) now also checks reflectively, through three additions to the checker.
(i) A per-predicate law registry predLaws (a record of subTy/fold/pkg/covers/disj devices,
dispatched from subTyAlg with recursion kept inside subTyAlg by a tySize-guarded conjunction),
whose predLawsEnv registers the three indexed families: RBTree(T, c, h), its one-taller successor
RBTree+ , and the almost-balanced ART used as ins’s intermediate invariant — each backed by a once-
proved soundness family (predLawsEnv_subTy_sound/_covers_sound/_disj_sound/_pkg_sound).
(ii) A core amendment realising the Hoare disjunction rule (∨Γ), Deriv.disj/Deriv.disjList,
letting checkExpr split a match branch’s multi-disjunct pre-state into singletons at branch entry
and rejoin the posts, a general completeness upgrade reaching beyond RBTree. (iii) A certified
successor sub-fragment of the linear-integer index recipe of Sec. B.3: the index shifts (ℎ ↦→ ℎ+1,
equal sibling heights) are now decided inside the checker (hsSucc/inferNat), ground index
computation plus open-height 𝑛/𝑛±1 reasoning, with no SMT oracle (consistent with Sec. 1);
RBTree_insert itself needs nothing beyond this fragment. The checker’s general affine-equality
linear-arithmetic engine is a separate, now-landed capability (the LIA rows of Table 4; Sec. B.3),
certifying the sized-list append/length flagships and, via a declared-post frame gate crossing
the existential child-size decomposition, the sized-tree size/mirror flagships too, all four
checker-reflectively, no remaining documented index-language boundary. On this footing Table 4
gains two rows certifying the same specifications as the hand rows of Table 5: RBTree_member
(rbmember_semvalid), the wide (𝐼𝑛𝑡, RBTree(𝐼𝑛𝑡, 𝐵𝑜𝑜𝑙, 𝐼𝑛𝑡))⇒𝐵𝑜𝑜𝑙 search run at a ground type by
native_decide; and the flagship RBTree_insert (rbInsert_semvalid_reflective), the whole
five-function Okasaki insert discharged symbolically for every height (∀ℎ); its WFEnv obligation
and all five ∗_bodyChecks_reflect runs are native-free, so the end-to-end certificate is fully
axiom-clean ({propext, Classical.choice, Quot.sound}, no native_decide, no SMT). That last row
is by far the most expensive symbolic example in Table 4, the price of a fully symbolic ∀ℎ WFEnv
over a five-function program.

   The hand breakdown (Table 5) and the completed boundary. Table 5 retains the by-hand
red-black balancing development of Table 2 as a derivation-effort record, broken down
by component: the shared predicate family and its lemma suite; the recursive member
search; the two Okasaki rebalancers balanceL/balanceR; the height-indexed ins; the
blacken/insert wrappers with the WFEnv assembly; and the top-level insert certificate
against ∀ℎ. (𝐼𝑛𝑡, RBTree(𝐼𝑛𝑡, 𝑐, ℎ))⇒RBTree(𝐼𝑛𝑡, Black, ℎ) ∨ RBTree(𝐼𝑛𝑡, Black, ℎ+1), whose
postcondition states the result’s exact colour and black-height (black, at height ℎ or ℎ+1). The
predicate constrains colour and black-height only, so the spec makes no key-ordering (BST)
claim. The reflective checker now certifies these same two specifications automatically (the
two RBTree rows of Table 4), and (as described next) the M2 heap-atom layer behind the typed
Queue now checks reflectively too, including a further packed-precondition layer that unfolds the
opaque hpred queue atom itself at the point a triple is checked, certifying both queue operations
ghost-free directly from that single atom. The reflective checker’s inequality-fragment engine (a
certified unit-Farkas decision procedure) now closes the paper’s SortedList(T, lo, hi) boundary
as well: a bespoke ∀-element destruction rule universally quantifies each cons premise over the
matched element’s value, and three checker-certified flagships — head, member, and the campaign’s
capstone sorted insert — are added to Table 4’s inequality-fragment group (Sec. B.3, App. F). The
sized-tree destruction that a reflective mirror needs (once the one remaining boundary) is now
also checker-certified, via a declared-post frame gate and the size/mirror flagships of Table 4’s
LIA group: there is no remaining documented index-language boundary (Sec. B.3). What remains
are limits on the completeness of the certified decision procedures, not on coverage.
Type Safety via Hoare Logic with Separation and Pure Types                                           45


        Component                                                            Lines Lean (ms)
        RBTree(Int, c, h) predicate family + unfold/fold lemma suite           328          316
        member — recursive search (program, derivation, witnesses)             632          703
        balanceL — body, ∀ℎ spec, per-height derivation (+ combinators)       1606         5004
        balanceR — mirror of balanceL                                         1158         4636
        ins — height-ledger bodyChecks (red-root & black-root cases)          1277         3579
        ins/blacken/insert bodies + program; blacken/insert bodyChecks         899          745
        WFEnv + insert (∀ℎ rbInsert_semvalid) + eval witnesses & audits        150         1070
        Total                                                                6050        16053
Table 5. The hand-mechanised red-black balancing development, broken down by component — the two
RBTree rows of Table 2 (RBTree_member 960/1019, RBTree_insert 5090/15034). Lines are exact source spans;
times use the same profiler method as Table 2.



   Reflective heap-atom checking (Table 4). The exact-content heap-predicate layer behind the typed
Queue (once hand-derived only) now also checks reflectively, through three additions to the M2
checker SepCheck. (i) An atom-cover entailment atomWeakenB letting the exact atoms ptsEq/ptsCon
weaken to the ordinary typed cells (ptsx(Reft)/ptsx(conc . . .)) they cover. (ii) A fold registry
heapLawsEnv, dispatched by foldRowB, that builds a registered heap-predicate atom by consuming
pool atoms up to the pure eq-closure: the list-segment LSegR (id 0) by peeling one link/node pair at
a time, and the two-pointer queuePred (id 1) by packing front/rear pointer cells, an owned sentinel,
and an LSegR segment — folding only, in the pack direction. (iii) Binder-exit field-slot inference:
matchE’s Cons arm infers an all-.eqv FieldSlot list from the scrutinee’s owned ptsCon cell, naming
each bound field by an existing variable rather than by type alone. On this footing, Table 4 gains three
rows certifying the typed two-pointer queue: Queue_enqueue (enqueue_semvalid_reflective),
proved at the fixed ghost names f/ga/gb — unlike the ∀ℎ RBTree_insert row, this is a ground result,
not a ∀-ghost one — and the two dequeue arms Queue_dequeue_empty/Queue_dequeue_cons
(dequeue_semvalid_empty_reflective/dequeue_semvalid_cons_reflective), each certifying
the exact same closed SemValid proposition as its hand-derived twin. All three are native_decide
rows run at ground ghost names; unlike the native-free symbolic RBTree_insert row, each carries
its own per-declaration compiler axiom.
   Packed-precondition unfolding (Table 4). Both queue operations admit a still-leaner statement:
instead of the fully unpacked enqueuePre/deqEmptyPre/deqConsPre states above, the precondi-
tion is just the single opaque hpred1[t] [f, r] atom — plus, for enqueue, the pure v : int conjunct
— GHOST-FREE, with no hand-written link or element names at all. A new registry unfoldRows
supplies, per registered predicate id, one-step unfolding templates: for the queue (id 1) a COARSE
alternative (the pointer-cell shape enqueue needs) and a SPLIT alternative (empty/Cons, the shape
dequeue needs), each introducing a Boolean-checked-fresh set of ghost names (ghostsOkB). The
wrapper checkSepPacked picks an alternative and Boolean-checks the body against every one
of its unfolded cases via checkSepConseq. Its soundness lemma checkSepPacked_sound — itself
NATIVE-FREE (clean-3) — reflects each case to a Deriv, lifts it to SemValid, combines the SPLIT
cases with SemValid_disj_pre, and transports the result back across the fresh-ghost extension via
a new store-extension lemma SemValid_unpack. That lemma’s adequacy over the packed/unpacked
boundary is discharged once per unfolding row (queue_unfold_coarse/queue_unfold_split),
and it rests on a fully general big-step store-agreement theorem BigStep_agree, which holds
for every expression, calls included, with no call-free restriction. On this footing Table 4 gains
two more rows: Queue_enqueue_packed (enqueue_semvalid_packed), whose ghost-free packed
precondition needs only v : int beyond the opaque atom and whose post is the same enqueuePost
46                                                                                  Li, Foo, Ta, and Chin


as Queue_enqueue; and Queue_dequeue_packed (dequeue_semvalid_packed), whose precondi-
tion is the bare atom (no pure conjunct at all) and whose post is the honest two-arm disjunction
deqEmptyPost∨deqConsPost. Each theorem is exactly one native_decide call through the native-
free checkSepPacked_sound wrapper. The unfold fires only at this packed-precondition entry point;
it is not a general heap-predicate rule usable anywhere a hpred atom occurs.
   Reflective inequality-fragment checking: SortedList (Table 4). Beyond the general affine-equality
engine above, the checker carries a certified inequality decision procedure: a sound unit-Farkas
worklist over the same reified index form, deciding </≤ constraints with no SMT call (App. F details
the procedure and its documented incompleteness on coefficient scaling). On this footing the checker
registers a SortedList(T, lo, hi) predicate (a structural fold rebinding the tail’s lower bound at each
matched element) together with a bespoke ∀-element destruction rule (Deriv.matchSortedCons):
unlike the ordinary match rule, its cons premise is universally quantified over the matched element’s
value, closing every emitted index atom at that value rather than at a symbolic placeholder. Three
flagships are checker-certified end-to-end on this fragment, all native-free and axiom-clean, and
gain three rows in Table 4: head (the shared post collapses to a scalar range-validity atom; the
per-element bound is instead certified in the destruction rule’s own side-condition witness), member
(an honest Bool post via rebound recursion and a double-< comparison encoding), and, as the
campaign’s capstone, sorted insert (post res : 𝑆𝑜𝑟𝑡𝑒𝑑𝐿𝑖𝑠𝑡 (𝐼𝑛𝑡, 𝑙𝑜, ℎ𝑖), a genuine end-to-end sorted
insertion). In each case the ∀-element cons-branch premise is discharged by a named semantic side
condition (SoConsObligation) rather than by the structural checker gate directly; the declared-
post frame gate used by construction flagships such as insert deliberately does not re-run the
cons branch at its reserved index variable, an honest, disclosed checker incompleteness that costs
nothing, since the real premise is supplied by the side condition instead. As with the equality
engine, no completeness claim is made for the inequality engine or the checker.
