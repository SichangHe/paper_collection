                                               Overcoming Restraint: Composing Veriﬁcation of
                                                      Foreign Functions with Cogent
                                                          Louis Cheung                                        Liam O’Connor                          Christine Rizkallah
                                                   University of Melborune                                University of Edinburgh                   University of Melbourne
                                                 Melbourne, Victoria, Australia                            Edinburgh, Scotland                  Melbourne, Victoria, Australia
                                              lfcheung@student.unimelb.edu.au                              l.oconnor@ed.ac.uk                 christine.rizkallah@unimelb.edu.au

                                         Abstract                                                                         recursion or loops, which ensures totality, and its unique-
arXiv:2102.09920v4 [cs.PL] 21 Dec 2021




                                         Cogent is a restricted functional language designed to re-                       ness type system, which enforces a uniqueness invariant that,
                                         duce the cost of developing veriﬁed systems code. Because                        among other beneﬁts, guarantees memory safety.
                                         of its sometimes-onerous restrictions, such as the lack of                          Even in the restricted target domains of Cogent, real pro-
                                         support for recursion and its strict uniqueness type system,                     grams contain some amount of iteration, primarily over data
                                         Cogent provides an escape hatch in the form of a foreign                         structures such as buﬀers. This is achieved through Cogent’s
                                         function interface (FFI) to C code. This poses a problem when                    principled FFI: engineers provide data structures and their
                                         verifying Cogent programs, as imported C components do                           associated operations, including iterators, in a special di-
                                         not enjoy the same level of static guarantees that Cogent                        alect of C, and import them into Cogent, including in formal
                                         does. Previous veriﬁcation of ﬁle systems implemented in                         reasoning. This special C code, called template C, can refer
                                         Cogent merely assumed that their C components were cor-                          to Cogent data types and functions, and is translated into
                                         rect and that they preserved the invariants of Cogent’s type                     standard C along with the Cogent program by the Cogent
                                         system. In this paper, we instead prove such obligations. We                     compiler. As long as the C components respect Cogent’s for-
                                         demonstrate how they smoothly compose with existing Co-                          eign function interface — i.e., are correct, memory-safe and
                                         gent theorems, and result in a correctness theorem of the                        respect the uniqueness invariant — the Cogent framework
                                         overall Cogent-C system. The Cogent FFI constraints ensure                       guarantees that correctness properties proved on high-level
                                         that key invariants of Cogent’s type system are maintained                       specs also apply to the compiler output.
                                         even when calling C code. We verify reusable higher-order                           Two real-world Linux ﬁle systems have been implemented
                                         and polymorphic functions including a generic loop combi-                        in Cogent — ext2 and BilbyFs — and key operations of Bil-
                                         nator and array iterators and demonstrate their application                      byFs have been veriﬁed [3]. This prior work demonstrates
                                         to several examples including binary search and the BilbyFs                      Cogent’s suitability as a systems programming language and
                                         ﬁle system. We demonstrate the feasibility of veriﬁcation                        as a veriﬁcation framework that reduces the cost of veriﬁca-
                                         of mixed Cogent-C systems, and provide some insight into                         tion. The implementations of these ﬁle systems import an
                                         veriﬁcation of software comprised of code in multiple lan-                       external C library of data structures, which include ﬁxed-
                                         guages with diﬀering levels of static guarantees.                                length arrays and iterators for implementing loops, as well
                                                                                                                          as Cogent stubs for accessing a range of the Linux kernel’s
                                         Keywords: compilers, veriﬁcation, type-systems, language                         internal APIs. This library was carefully designed to ensure
                                         interoperability, data-structures                                                compatibility with Cogent’s FFI constraints, but was previ-
                                                                                                                          ously left unveriﬁed — only the Cogent parts of these ﬁle
                                         1     Introduction                                                               system operations were proven correct, and statements of
                                         Cogent [16] is a restricted purely functional language with a                    the underlying C correctness and FFI constraints deﬁning
                                         certifying compiler [16, 21] designed to ease creating veriﬁed                   Cogent-C interoperability were left as assumptions.
                                         operating systems components [3]. It has a foreign function                         To fully verify a system written in Cogent and C, one
                                         interface (FFI) that enables implementing parts of a system                      needs to provide manually-written abstractions of the C parts,
                                         in C. Cogent’s main restrictions are the purposeful lack of                      and manually prove reﬁnement through Cogent’s FFI. The
                                                                                                                          eﬀort required for this manual veriﬁcation remains substan-
                                         Permission to make digital or hard copies of part or all of this work for        tial, but the reusability of these libraries allows this cost to
                                         personal or classroom use is granted without fee provided that copies are
                                         not made or distributed for proﬁt or commercial advantage and that copies
                                                                                                                          be amortised across diﬀerent systems.
                                         bear this notice and the full citation on the ﬁrst page. Copyrights for third-      In this paper, we eliminate several of these assumptions
                                         party components of this work must be honored. For all other uses, contact       by verifying the array implementation and key iterators used
                                         the owner/author(s).                                                             in the BilbyFs ﬁle system (Section 3), and discharging the
                                         CPP ’22, January 17–18, 2022, Philadelphia, PA, USA                              conditions imposed by Cogent’s FFI (Section 5). We also ver-
                                         © 2022 Copyright held by the owner/author(s).                                    ify a generic-loop combinator (Section 4) and its application
                                         ACM ISBN 978-1-4503-9182-5/22/01.
                                         https://doi.org/10.1145/3497775.3503686
                                                                                                                          to binary search. This demonstrates that it is possible and
CPP ’22, January 17–18, 2022, Philadelphia, PA, USA                                           Louis Cheung, Liam O’Connor, and Christine Rizkallah


relatively straightforward for the C components of a real-                                type Array 𝑎
world Cogent-C system to satisfy Cogent’s FFI conditions.                                 length : (Array 𝑎)! → U32
The compiler-generated reﬁnement and preservation proofs                                  get : ((Array 𝑎)!, U32, a!) → 𝑎!
compose with manual C proofs at each intermediate level up                                put : (Array 𝑎, U32, a) → Array 𝑎
to Cogent’s generated shallow embedding, and verify some                                  map : (𝑎 → 𝑎, Array 𝑎) → Array 𝑎
example Cogent-C programs.                                                                fold : ((𝑎!, 𝑏) → 𝑏, 𝑏, (Array 𝑎)!) → 𝑏
   As arrays and loops are extremely common in Cogent pro-
gramming, our proofs are highly reusable for veriﬁcation of                               add : (U32, U32) → U32
any future Cogent-C system. In addition, our proofs con-                                  add (x , y) = x + y
nect C arrays to plain old Isabelle/HOL lists and loops to                                sum : (Array U32) ! → U32
an Isabelle/HOL repeat function that allows early termina-                                sum arr = fold (add, 0, arr )
tion. These proofs are reusable even beyond the context of
Cogent in veriﬁcation of C code. Our code and proofs are                       Figure 1. A Cogent sum program that makes use of an ab-
online [4].                                                                    stract array type and operations.
   Similar to many high-level languages, Cogent’s foreign
function interface connects a high-level language with strong
static guarantees to an unsafe imperative language. This work
provides our community with a case-study demonstrating                            A key part of the compiler certiﬁcate depends on Cogent’s
how to equip such a foreign function interface with proof re-                  uniqueness type system, which enforces that each mutable
quirements such that those static guarantees are maintained                    heap object has exactly one active pointer in scope at any
for the overall system. In particular, our work supports, and                  point in time. This uniqueness invariant allows modelling
is well-described by, Ahmed’s claim that:                                      imperative computations as pure functions: the allocations
    “Compositional compiler correctness is, in essence, a lan-                 and repeated copying commonly found in functional pro-
guage interoperability problem: for viable solutions in the long               gramming can be replaced with destructive updates, and the
term, high-level languages must be equipped with principled                    need for garbage collection is eliminated, resulting in pre-
foreign-function interfaces that specify safe interoperability                 dictable and eﬃcient code.
between high-level and low-level components, and between                          Well-typed Cogent programs have two interpretations: a
more precisely and less precisely typed code.” [1]                             purely functional value semantics, which has no notion of a
   Our approach to language interoperability does not rely                     heap and treats all objects as immutable values, and an im-
on how the reﬁnement theorems of the languages are ob-                         perative update semantics, describing the destructive muta-
tained nor on whether they are manually or automatically                       tion of heap objects. These two semantic interpretations cor-
proven. As such, we believe that this approach is likely reusable              respond (Section 2.5), meaning that any correctness proofs
in the context of veriﬁed compilers.                                           about the value semantics also apply to the update seman-
                                                                               tics. As we shall see, this correspondence further guarantees
                                                                               that well-typed Cogent programs are memory safe.
2    Cogent
The Cogent language [15–17] was originally designed for                        2.1 Language Design and Examples
the implementation of systems components such as ﬁle sys-
                                                                               Cogent has unit, numeric, and boolean primitive types, as
tems [3]. It is a purely functional language, but it is compiled
                                                                               well as functions, sum types (i.e., variants) and product types
into eﬃcient C code suitable for systems programming1 .
                                                                               (i.e., tuples and records). Users can declare additional ab-
   The Cogent compiler produces three artefacts: C code, a
                                                                               stract types in Cogent, and deﬁne them externally (i.e., in
shallow embedding of the Cogent code in Isabelle/HOL [14],
                                                                               C). Abstract and record types may be boxed, that is, stored
and a formal reﬁnement proof relating the two [16, 21]. The
                                                                               on the heap, in which case they are mutable and subject to
reﬁnement theorem and proof rely on several intermediate
                                                                               the uniqueness restrictions of Cogent’s type system. Cogent
embeddings also generated by the Cogent compiler, some
                                                                               does not support closures, so partial application via curry-
related through language level proofs, and others through
                                                                               ing is not common. Thus, functions of multiple arguments
translation validation phases (Section 2.5). The compiler cer-
                                                                               take a tuple or record of those arguments.
tiﬁcate guarantees that correctness theorems proven on top
                                                                                   Figure 1 includes an example of Cogent signatures for an
of the shallow embedding also hold for the generated C,
                                                                               externally-deﬁned array library interface, where array in-
which eases veriﬁcation, and serves as the basis for further
                                                                               dices and length are unsigned 32-bit integers (U32).
functional correctness proofs.
                                                                                   Like ML, Cogent supports parametric polymorphism for
                                                                               top-level functions, and implements it via monomorphisa-
1 While Cogent is ideally suited for applications that involve minimal shar-   tion. For imported code, the compiler generates specialised
ing and where eﬃciency matters, it is not speciﬁc to the systems domain.       C implementations from a polymorphic template, one for
Composing Verification of Foreign Functions with Cogent                             CPP ’22, January 17–18, 2022, Philadelphia, PA, USA


each concrete instantiation used in the Cogent code. Vari-         length : (Array 𝑎)! → U32
ables of polymorphic type are by default linear, which means       mapAccum : ((𝑎, 𝑏, 𝑐!) → (𝑎, 𝑏), 𝑏, (Array 𝑎)!, U32, U32, 𝑐!)
they must be used exactly once [22]. Thus a polymorphic                        → (Array 𝑎, 𝑏)
type variable may be instantiated to any type, including types     fold : ((𝑎, 𝑏, 𝑐!) → 𝑏, 𝑏, (Array 𝑎)!, U32, U32, 𝑐!)
that contain pointers, while preserving the uniqueness in-
variant.                                                           add : (U32, U32, ()) → U32
   As mentioned, types and functions provided in external          add (x , y, z ) = x + y
C code are called abstract in Cogent. The Cogent compiler          sum : (Array U32)! → U32
has infrastructure for linking the C implementations and the       sum arr = fold (add, 0, arr , 0, length arr , ())
compiled Cogent code. Users write template C code, that can
include embedded Cogent types and expressions via quasi-          Figure 2. The sum function now written against the inter-
quotation, and the Cogent compiler translates the template        ace from Cogent’s C library.
C into ordinary C that it links with the C code generated
from Cogent. To represent containers, abstract types may be
given type parameters. These parameterised types, as well         (of type c!). In addition, the function mapAccum is a gener-
as polymorphic functions, are translated into a family of au-     alised version of map, which allows threading an accumulat-
tomatically generated C functions and types; one for each         ing argument through the map function, similar to the same
concrete type used in the Cogent program.                         function in Haskell. We present the veriﬁcation of these it-
   Though the Array type interface may appear purely func-        erators in Section 3.
tional, Cogent assumes that all abstract types are by default
linear, ensuring that the uniqueness invariant applies to vari-   2.2 Dynamic Semantics
ables of type Array. Therefore, any implementation of the         Cogent’s big-step value semantics is deﬁned through the
abstract put function is free to destructively update the pro-    judgement 𝑉 ⊢𝑒 v 𝑣. This judgement states that the expres-
vided array, without contradicting the purely functional se-      sion 𝑒 under environment 𝑉 evaluates to the value 𝑣. The en-
mantics of Cogent.                                                vironment 𝑉 maps variables to their values. The imperative
   When functions only need to read from a data structure,        update semantics, which additionally may manipulate a mu-
uniqueness types can complicate a program unnecessarily           table store 𝜇, is deﬁned through the judgement𝑈 ⊢𝑒 |𝜇 u 𝑢|𝜇 ′ .
by requiring a programmer to thread through all state, even       This states that, starting with an initial store 𝜇 the expres-
unchanged state. The !-operator helps to avoid this by con-       sion 𝑒 will evaluate under the environment 𝑈 to a ﬁnal store
verting linear, writable types to read-only types that can be     𝜇 ′ and a result value 𝑢. Unlike the values in the value se-
freely shared or discarded. This is analogous to a borrow in      mantics, values in the update semantics may be pointers to
Rust. The length and get functions, presented in Figure 1,        locations in the store.
can read from the given array, but may not write to it.               Both of these semantics are further parameterised by ad-
   As Cogent does not support recursion, iteration is expressed   ditional functions and types of values that are provided ex-
using abstract higher-order functions, providing basic traver-    ternally to Cogent, to model the semantics of abstract func-
sal combinators such as map and fold for abstract types, as       tions and types. More formally, the value semantics is pa-
can be seen in Figure 1. Note that map is passed a function       rameterised by a function 𝜉 v : 𝑓id → (𝑣 → 𝑣) and the
of type 𝑎 → 𝑎. As such, map is able to destructively over-        update semantics by a function 𝜉 u : 𝑓id → (𝜇 × 𝑢 → 𝜇 × 𝑢).
write the array with the result of the function applied to        Both of these are essentially an environment providing a
each element.                                                     pure HOL function on Cogent values (and stores, for the up-
   While Cogent supports higher-order functions, it does          date semantics) for each abstract function. The deﬁnitions
not support nested lambda abstractions or closures, as these      of values in the value semantics (𝑣) and update semantics
can require allocation if they capture variables. Thus, to in-    (𝑢) are also extended with parameters 𝑎 v and 𝑎 u respectively
voke the map or fold functions, a separate top-level function     which represent values of abstract types.
must be deﬁned, such as add in our example.                           Along with C code for all abstract functions and types, the
   The array interface from Cogent’s C library used in the        user must also manually provide Isabelle/HOL abstractions
implementation of the Cogent ﬁle systems, part of which           of this C code to instantiate these environments.
is given in Figure 2, is more complex than that of Figure 1:          To verify Cogent systems, three main proof obligations
The higher-order functions are given two additional index         must be discharged: type preservation, which ensures the
parameters to operate over only a subsection of an array;         uniqueness invariant is maintained; the frame requirements,
and instead of relying on closure captures, which are not         which ensures that memory safety is maintained; and re-
available in Cogent, we provide alternative iterator func-        ﬁnement, which ensures that functional correctness theo-
tions which carry an additional observer read-only input          rems are preserved down to the C level via the provided
                                                                  abstractions. Cogent proves all three of these requirements
CPP ’22, January 17–18, 2022, Philadelphia, PA, USA                                Louis Cheung, Liam O’Connor, and Christine Rizkallah


automatically for Cogent code: both type preservation and          proof obligations on abstract types that must be discharged
the frame requirements are simple corollaries of the key se-       by the user. These requirements are outlined in Section 2.7.
mantic correspondence theorem (Theorem 2.5) that makes
up part of the Cogent reﬁnement chain. For linked C code,          2.4 Frame Requirements
however, the user must discharge these obligations manu-           In addition to type preservation, which ensures that each
ally. We discuss our veriﬁcation of these requirements for C       Cogent value is well-formed and does not contain internal
code in Section 3.                                                 aliasing, we must also show that the mutable store 𝜇 is in
                                                                   good order throughout evaluation — memory should not
2.3   Typing and Type Preservation                                 be leaked, and programs should not write to memory to
Cogent’s static semantics are deﬁned through a standard typ-       which they have no access. These memory safety require-
ing judgement 𝐴; Γ ⊢ 𝑒 : 𝜏, which states that 𝑒 has type 𝜏         ments are summed up by Cogent’s frame relation, which
under context Γ, with an additional context 𝐴 that tracks          describes how a program may aﬀect the store. Given an
assumptions about the linearity of type variables in 𝜏. To         input set of writable pointers 𝑤 𝑖 , an input store 𝜇𝑖 , an out-
accommodate abstract types, we allow the type system to            put set of pointers 𝑤𝑜 and an output store 𝜇𝑜 , the relation,
be extended with types A 𝜏 and (A 𝜏)!, referring to linear ab-     𝑤 𝑖 | 𝜇𝑖 frame 𝑤𝑜 | 𝜇𝑜 , ensures three properties for any pointer
stract types and read-only abstract types respectively, where      𝑝:
A is a type constructor parameterised by zero or more type                       inertia: 𝑝 ∉ 𝑤 𝑖 ∪ 𝑤𝑜 −→ 𝜇𝑖 (𝑝) = 𝜇𝑜 (𝑝)
parameters 𝜏.
   Dynamic values in the value semantics are typed by the                leak freedom: 𝑝 ∈ 𝑤 𝑖 −→ 𝑝 ∉ 𝑤𝑜 −→ 𝜇𝑜 (𝑝) = ⊥
simple judgement 𝑣 : 𝜏, whereas update semantics values               fresh allocation: 𝑝 ∉ 𝑤 𝑖 −→ 𝑝 ∈ 𝑤𝑜 −→ 𝜇𝑖 (𝑝) = ⊥
must be typed with the store 𝜇 to type the parts of the value      Inertia ensures that pointers not in the frame remain un-
that are stored there. Update semantics values are typed by        changed; leak freedom ensures that pointers removed from
the judgement 𝑢|𝜇 : 𝜏 [𝑟 ∗ 𝑤], which additionally includes         the frame no longer point to anything; and fresh allocation
the heap footprint, consisting of the sets of read-only (𝑟 ) and   ensures that pointers added to the frame were not already
writable (𝑤) pointers the value can contain. We use the same       used. The frame relation implies that any property of a given
notation for value typing on environments.                         value is unaﬀected by updates to unrelated parts of the heap.
   This heap footprint annotation is crucial to ensuring that      The frame relation holds for all Cogent computations, ensur-
Cogent maintains its uniqueness invariant, as it places con-       ing memory safety along with type safety:
straints on the footprints of subcomponents of a value to
rule out aliasing of live pointers. Thus, our theorem of type      Theorem 2.2 (Preservation and Frame Relation).
preservation across evaluation in the update semantics also         𝐴; Γ ⊢ 𝑒 : 𝜏 ∧ 𝑈 |𝜇 : Γ [𝑟 ∗ 𝑤] ∧ 𝑈 ⊢𝑒 |𝜇 u 𝑢|𝜇 ′ −→
shows that this invariant is preserved. More details on these          ∃𝑟 ′ 𝑤 ′ . 𝑟 ′ ⊆ 𝑟 ∧ 𝑤 |𝜇 frame 𝑤 ′ |𝜇 ′ ∧ 𝑢|𝜇 : 𝜏 [𝑟 ′ ∗ 𝑤 ′ ]
constraints are discussed in earlier work [16, 17]. When the
heap footprints are not relevant and merely existentially          This states that a well-typed program will evaluate in the
quantiﬁed, we shall omit them:                                     update semantics to a well-typed value, and that the frame
                                                                   relation holds between the writable pointers of the input
                𝑢|𝜇 : 𝜏 ≡ ∃𝑟 𝑤 . 𝑢|𝜇 : 𝜏 [𝑟 ∗ 𝑤]                   environment and the output value. Note that this theorem
Theorem 2.1 (Type Preservation). For both update and value         implies update semantics type preservation (Theorem 2.1),
semantics:                                                         because this theorem too is a simpliﬁcation of Theorem 2.5.

 • 𝐴; Γ ⊢ 𝑒 : 𝜏 ∧ 𝑈 |𝜇 : Γ ∧ 𝑈 ⊢𝑒 |𝜇 u 𝑢|𝜇 ′ −→ 𝑢|𝜇 ′ : 𝜏          2.5 Reﬁnement
 • 𝐴; Γ ⊢ 𝑒 : 𝜏 ∧ 𝑉 : Γ ∧            𝑉 ⊢𝑒 v 𝑣         −→ 𝑣 : 𝜏     The overall proof that the C code reﬁnes the purely func-
                                                                   tional shallow embedding in Isabelle/HOL is broken into
This states that the value typing relation for either seman-       a number of sub-proofs and translation validation phases.
tics is preserved across the evaluation relation for well-typed    Figure 3 gives an overview of Cogent’s reﬁnement theorems
expressions. Because the value typing relations of the up-         for a function 𝑓 (𝑥) applied to an argument 𝑎. The compiler
date and value semantics are later combined into one re-           generates four embeddings: a top-level shallow embedding
ﬁnement relation, which is shown to be preserved across            in terms of pure functions; a polymorphic deep embedding
evaluation in Theorem 2.5, type preservation is obtained by        of the Cogent program, which is interpreted using the value
simply erasing one of the semantics from Theorem 2.5.              semantics; a monomorphic deep embedding of the Cogent
   Because the set of types is extensible, the value-typing re-    program, which can be interpreted using either the value
lation for both semantics must also be extensible. To ensure       or update semantics; and an Isabelle/HOL representation
that the user’s extensions to the value-typing relation do not     of the C code generated by the compiler, imported into Is-
violate the uniqueness invariant, Cogent places a number of        abelle/HOL by the C-parser [24] used in the seL4 project [8].
Composing Verification of Foreign Functions with Cogent                                     CPP ’22, January 17–18, 2022, Philadelphia, PA, USA


            𝑎s   ⊢ 𝑓s     s   𝑟s          Shallow HOL Embedding       Theorem 2.4 (Update ⇒ C reﬁnement). For any function
                 (Theorem 2.9)
                                                                      𝑓 (𝑥) with monomorphic Cogent embedding 𝑓m and C embed-
                                                                      ding 𝑓c , given an argument represented in the update seman-
     (𝑥 ↦→ 𝑎 p ) ⊢ 𝑓p     v   𝑟p    Value Semantics, Polymorphic      tics of Cogent as 𝑎 u and in C as 𝑎 c , we have:
                 (Theorem 2.7)
                                                                            V uc (𝑎 c , 𝑎 u ) ∧ H uc (𝜎, 𝜇) ∧ 𝑎 c ⊢ 𝜎 | 𝑓c c 𝑟 c | 𝜎 ′ −→
     (𝑥 ↦→ 𝑎 m ) ⊢ 𝑓m     v   𝑟 m Value Semantics, Monomorphic                 ∃𝑟𝑢 𝜇 ′ . (𝑥 ↦→ 𝑎 u ) ⊢ 𝑓m | 𝜇 u 𝑟 u | 𝜇 ′
                 (Theorem 2.5)                                                              ∧ V uc (𝑟 c, 𝑟 u ) ∧ H uc (𝜎 ′, 𝜇 ′ )
 (𝑥 ↦→ 𝑎 u ) | 𝜇 ⊢ 𝑓m     u   𝑟u | 𝜇′             Update Semantics
                                                                      This states that if the C embedding evaluates to a result, then
                 (Theorem 2.4)                                        the corresponding Cogent update semantics will, given cor-
        𝑎 c | 𝜎 ⊢ 𝑓c      c   𝑟c | 𝜎 ′                 AutoCorres C   responding input values and heaps, evaluate to correspond-
                                                                      ing output values and heaps.
Figure 3. Cogent’s semantic levels and reﬁnement theo-                2.5.2 Semantic Correspondence. For the second stage,
rems.                                                                 we must bridge the gap between the update semantics and
                                                                      value semantics. This is accomplished by Cogent’s proof for
The C-parser generates a deep embedding of C in Isabelle/HOL,         all well-typed programs that the two semantics correspond.
and, using AutoCorres [5, 6], is then abstracted to a corre-          As previously mentioned, this theorem combines both of the
sponding state-monadic embedding of the C code in HOL.                value typing relations from the two semantics 𝑣 : 𝜏 and 𝑢|𝜇 :
                                                                                                                   R
   Each of these semantic layers is connected by a reﬁne-             𝜏 [𝑟 ∗𝑤] into one one combined relation 𝑢|𝜇 ∼ 𝑣 : 𝜏 [𝑟 ∗𝑤]. In
ment proof by forward simulation: Given a reﬁnement rela-             addition to typing both values, 𝑢 and 𝑣, this relation also re-
tion that relates corresponding values between two layers,            quires that they represent the same conceptual value. Prior
we prove that if the more concrete (lower in the hierarchy)           work [16, 17] proves that the update semantics reﬁnes the
layer evaluates, then the more abstract (higher in the hierar-        value semantics by proving that this relation is preserved
chy) layer, given corresponding inputs, will also evaluate to         across the evaluation of both, and furthermore that evalua-
corresponding outputs. The composition of all these reﬁne-            tion in the update semantics implies the evaluation in the
ments means that any property preserved by reﬁnement,                 value semantics. As mentioned in Section 2.4, this also si-
such as functional correctness, proved about all executions           multaneously proves the frame requirements hold for Co-
of the most abstract embedding — the Shallow HOL embed-               gent code.
ding — will also apply to the most concrete embedding, i.e.
the C code.                                                           Theorem 2.5 (Value ⇒ Update reﬁnement). For any 𝑒 where
                                                                                            R
                                                                      𝐴; Γ ⊢ 𝑒 : 𝜏, if 𝑈 |𝜇 ∼ 𝑉 : Γ [𝑟 ∗𝑤] and 𝑈 ⊢ 𝑒 | 𝜇 u 𝑢 | 𝜇 ′ , then
2.5.1 Update to C Reﬁnement. In the ﬁrst stage, Cogent
                                                                      there exists a value 𝑣 and pointer sets 𝑟 ′ ⊆ 𝑟 and 𝑤 ′ such that
proves reﬁnement between the C implementation and the                                         R
deep embedding in the update semantics. AutoCorres im-                𝑉 ⊢ 𝑒 v 𝑣, and 𝑢|𝜇 ′ ∼ 𝑣 : 𝜏 [𝑟 ′ ∗𝑤 ′ ] and 𝑤 | 𝜇 frame 𝑤 ′ | 𝜇 ′ .
ports C as a nondeterministic state-monadic program shal-             This proof is parameterised by the assumption that the same
lowly embedded in Isabelle/HOL. To make our deﬁnitions                holds for abstract functions. We discuss how to discharge
more symmetrical with those of Cogent, we deﬁne a C eval-             this assumption in Section 3.
uation relation as follows:
                                                                      2.5.3 Monomorphisation. Recall that the Cogent com-
Deﬁnition 2.3 (C Evaluation Relation).
                                                                      piler eliminates polymorphism by monomorphising, that is,
       𝑎 c ⊢ 𝜎 | 𝑓c c 𝑟 c | 𝜎 ′ ≡                                     replacing polymorphic functions with specialised copies, one
           (𝑟 c, 𝜎 ′ ) ∈ results (𝑓c 𝑎 c 𝜎) ∧ ¬failed (𝑓c 𝑎 c 𝜎)      for each type used in the program. Using template C, the
This states that given an input 𝑎𝑐 and C heap 𝜎, the C func-          Cogent compiler can do the same for the user-supplied C
tion 𝑓𝑐 evaluates to 𝑟𝑐 and an output heap 𝜎 ′ and that no            code. To prove that this elimination of polymorphism pre-
undeﬁned behaviour occurred (indicated by ¬failed ).                  serves correctness we must show that the monomorphic
   The Cogent compiler additionally generates a value rela-           program reﬁnes the polymorphic program. This is accom-
tion V uc and a heap relation H uc , which together form the re-      plished by replicating the compiler’s monomorphisation op-
ﬁnement relation for this reﬁnement lemma. Using an auto-             erations in Isabelle/HOL as functions on deep embeddings:
mated technique described elsewhere [21], the Cogent proof            M𝑒 to monomorphise expressions and M 𝑣 to monomor-
then automatically discharges this proof obligation on a per-         phise values. Then, the reﬁnement relation is simply deﬁned:
program basis via translation validation, while leaving open          Deﬁnition 2.6 (Monomorphisation Relation).
proof obligations for the user to discharge for abstract func-
                                                                                        p
tions implemented in C.                                                               R m (𝑣 m, 𝑣 p ) ≡ (𝑣 m = M 𝑣 (𝑁 , 𝑣 p ))
CPP ’22, January 17–18, 2022, Philadelphia, PA, USA                                         Louis Cheung, Liam O’Connor, and Christine Rizkallah


where 𝑁 is a name mapping, supplied by the compiler, indi-               𝑎 m , 𝑎 p ,𝑎 s ; heap 𝜎 and store 𝜇, we show:
cating which set of monomorphic functions correspond to
                                                                          R sc (𝑎 c , 𝜎, 𝑎 u , 𝜇, 𝑎 m, 𝑎 p , 𝑎 s , 𝜏, 𝑟 , 𝑤) ∧ 𝑎 c ⊢ 𝑓c | 𝜎 c 𝑣 c | 𝜎 ′ −→
which polymorphic functions.
                                                                              ∃ 𝑟 ′ 𝑤 ′ 𝜇 ′ . 𝑟 ′ ⊆ 𝑟 ∧ 𝑤 |𝜇 frame 𝑤 ′ |𝜇 ′
Proving reﬁnement, then, proceeds on much the same lines                          ∧ ∃ 𝑣u 𝑣m 𝑣p 𝑣s.
as the other layers:                                                                   ∧ (𝑥 ↦→ 𝑎 u ) ⊢ 𝑓m |𝜇 u 𝑣 u |𝜇 ′
                                                                                       ∧ (𝑥 ↦→ 𝑎 m ) ⊢ 𝑓m v 𝑣 m
Theorem 2.7 (Polymorphic ⇒ Monomorphic reﬁnement).                                     ∧ (𝑥 ↦→ 𝑎 p ) ⊢ 𝑓p v 𝑣 p
For any function 𝑓 (𝑥) with a polymorphic embedding 𝑓p and                             ∧ 𝑎 s ⊢ 𝑓s s 𝑣 s
argument 𝑎 p , let 𝑓m = M𝑒 (𝑁 , 𝑓p ) and 𝑎 m = M 𝑣 (𝑎 p ). Then we                     ∧ R sc (𝑣 c, 𝜎 ′, 𝑣 u, 𝜇 ′, 𝑣 m, 𝑣 p, 𝑣 s, 𝜏 ′, 𝑟 ′, 𝑤 ′ )
have:                                                                    Because this theorem encompasses all levels of reﬁnement
         p
       R m (𝑎 m, 𝑎 p ) ∧ (𝑥 ↦→ 𝑎 m ) ⊢ 𝑓m v 𝑟 m −→                       as well as type preservation and the frame requirements, it
                                                      p
                    ∃𝑟 p . (𝑥 ↦→ 𝑎 p ) ⊢ 𝑓p v 𝑟 p ∧ R m (𝑟 m, 𝑟 p )      is suﬃcient to prove this theorem about (each embedding
                                                                         of) each abstract function, where the semantics of the deep
2.5.4 Shallow Embedding. Having reached the top of the                   embeddings 𝑓p and 𝑓m is given by the user-supplied envi-
reﬁnement tower, we must cross the bridge back to shallow                ronments 𝜉 𝑣 and 𝜉𝑢 . A proof of this theorem for an abstract
embeddings, i.e., our pure HOL functions that serve as an ex-            function is suﬃcient to integrate its veriﬁcation with the
ecutable speciﬁcation. Because this embedding is just pure               Cogent veriﬁcation chain.
functions, our “evaluation” relation is just function applica-
                                                                         2.7 Requirements on Abstract Types
tion:
                                                                         Theorem 2.11 encompasses all requirements the Cogent FFI
Deﬁnition 2.8 (Shallow Evaluation Relation).                             places on abstract functions, but users can also provide ab-
                                                                         stract types, extending the dynamic value typing rules as
                   𝑎 s ⊢ 𝑓s     s   𝑟 s ≡ (𝑓s 𝑎 s = 𝑟 s )                they see ﬁt. Therefore, Cogent imposes several constraints
                                                                         on the value typing judgements which ensure that key type
To show reﬁnement, the compiler must once again connect                  system invariants such as memory safety are maintained for
deep and shallow embeddings, just as with the Cogent to                  abstract types.
C reﬁnement (Theorem 2.4). Therefore, as with C, the com-                   Consider an abstract type of the form “A 𝜏”, where A is
piler automatically produces a proof of this theorem on a                the name of the abstract type and 𝜏 is a list a type parame-
per-program basis via translation validation. The compiler               ters. Because it is not surrounded with the !-operator, it is
generates a reﬁnement relation R sp for all types used in the            linear and therefore writable. The requirements of the user-
program, and then proves:                                                deﬁned value typing relation are as follows.
Theorem 2.9 (Shallow ⇒ Polymorphic reﬁnement). For any                   Deﬁnition 2.12 (Value Typing Requirements).
function 𝑓 (𝑥) with a shallow embedding 𝑓s and polymorphic
                                                                              bangv : 𝑣 : A 𝜏 −→ 𝑣 : (A 𝜏!)!
deep embedding 𝑓p , and arguments 𝑎 s and 𝑎 p respectively, we
have:                                                                        bangu : 𝑢|𝜇 : A 𝜏 [𝑟 ∗ 𝑤] −→ 𝑢|𝜇 : (A 𝜏!) [𝑟 ∪ 𝑤 ∗ ∅]
                                                                           no-alias: 𝑢|𝜇 : A 𝜏 [𝑟 ∗ 𝑤] −→ 𝑟 ∩ 𝑤 = ∅
        R sp (𝑎 p, 𝑎 s ) ∧ (𝑥 ↦→ 𝑎 p ) ⊢ 𝑓p v 𝑟 p −→
                              ∃𝑟 s . 𝑎 s ⊢ 𝑓s s 𝑟 s ∧ R sp (𝑟 p, 𝑟 s )         valid: 𝑢|𝜇 : A 𝜏 [𝑟 ∗ 𝑤] −→ ∀𝑝 ∈ 𝑟 ∪ 𝑤 . 𝜇(𝑝) ≠ ⊥
                                                                              frame: 𝑢|𝜇𝑖 : A 𝜏 [𝑟 ∗ 𝑤] −→ 𝑤 𝑖 |𝜇𝑖 frame 𝑤𝑜 |𝜇𝑜
2.6   Overall Reﬁnement                                                                    −→ (𝑟 ∪ 𝑤) ∩ 𝑤 𝑖 = ∅ −→ 𝑢|𝜇𝑜 : A 𝜏 [𝑟 ∗ 𝑤]
To combine all of these reﬁnement phases, we ﬁrst deﬁne a
                                                                         The bang rules ensure that abstract values respect the !-operator,
reﬁnement relation for all the layers of reﬁnement:
                                                                         i.e., when ! is applied to a value, the value becomes read-
Deﬁnition 2.10 (Combined Relation).                                      only; no-alias ensures that there is no aliasing of writable
                                                                         pointers by readable pointers within a value; valid enforces
                 R sc (𝑣 c, 𝜎, 𝑣 u, 𝜇, 𝑣 m, 𝑣 p, 𝑣 s, 𝜏, 𝑟 , 𝑤)          that all pointers are valid, i.e., point to values; and frame en-
                                                  p                      sures that an abstract value is unchanged if it is not part of
                         ≡ R sp (𝑣 p, 𝑣 s ) ∧ R m (𝑣 m, 𝑣 p )
                                    R                                    the store that is currently being modiﬁed. For a read-only
                        ∧ 𝑣 u |𝜇 ∼ 𝑣 m : 𝜏 [𝑟 ∗ 𝑤]                       type (A 𝜏)!, the requirements are the same, save that the
                        ∧ V uc (𝑣 c, 𝑣 u ) ∧ H uc (𝜎, 𝜇)                 writable pointer set 𝑤 must also be empty:

Theorem 2.11 (Combined Reﬁnement). Given a function                                read-only: 𝑢|𝜇 : (A 𝜏)! [𝑟 ∗ 𝑤] −→ 𝑤 = ∅
𝑓 (𝑥) with embeddings 𝑓c , 𝑓m , 𝑓p , 𝑓s ; argument value 𝑎 c , 𝑎 u ,
Composing Verification of Foreign Functions with Cogent                                 CPP ’22, January 17–18, 2022, Philadelphia, PA, USA


2.8    Summary of Requirements                                         lengths : [𝑎] → word32
As can be seen from the previous sections, proof engineers             lengths xs = of_nat (List.length xs)
must provide a number of implementations, abstractions,                gets : [𝑎] → word32 → 𝑎
and proofs for each function and type they import. We brieﬂy           gets xs i d = if unat i < List.length xs
summarise these here. For each abstract type imported from                          then xs ! (unat i) else d
C, the proof engineer simply needs to prove the require-               puts : [𝑎] → word32 → 𝑎 → [𝑎]
ments of Deﬁnition 2.12. For each imported foreign func-               puts xs i v = xs[unat i ≔ v ]
tion 𝑓 , proof engineers must deﬁne a version of the func-             folds : (𝑏 → 𝑎 → 𝑐 → 𝑏) → 𝑏 → [𝑎]
tion for all semantic levels in the Cogent hierarchy. That                  → word32 → word32 → 𝑐 → 𝑏
is, they must deﬁne a C implementation, an update seman-               folds f acc xs frm to obs =
tics (𝜉 u 𝑓 ), a monomorphic value semantics (𝜉 m 𝑓 ), a poly-            List.fold (𝜆acc el . f acc el obs) acc (slice frm to xs)
morphic value semantics (𝜉 p 𝑓 ), and a shallow embedding              mapAccums : (𝑏 → 𝑎 → 𝑐 → (𝑎, 𝑏)) → 𝑏 → [𝑎]
in HOL. Once all embeddings have been provided, overall                              → word32 → word32 → 𝑐 → ([𝑎], 𝑏)
reﬁnement (Theorem 2.11) must be proven for the foreign                mapAccums f acc xs frm to obs =
function 𝑓 , which necessitates proofs of all of our other preser-        let (xs ′, acc ′ ) = List.fold
vation and reﬁnement theorems:                                               (𝜆el (xs, acc). let (el ′ , acc ′ ) = f acc el obs
                                                                                                in (xs @ [el ′], acc ′ ))
      • Type preservation in the update semantics (Theorem 2.2):             (slice frm to xs) ([], acc)
        required by all functions that call 𝑓 to prove type preser-       in (take frm xs @ xs ′ @ drop (max frm to) xs, acc ′ )
        vation (Theorem 2.2), and by 𝑓 and all functions that
        call it to prove reﬁnement (Theorems 2.4 and 2.5).            Figure 4. Functional correctness speciﬁcation of the array
      • Type preservation in the monomorphic value seman-             operations in Isabelle/HOL.
        tics (Theorem 2.1): required by all functions that call
        𝑓 to prove type preservation (Theorem 2.1), and by 𝑓
        and all functions that call it to prove reﬁnement (The-
        orems 2.5 and 2.7).
      • Reﬁnement from the update semantics to C (Theorem 2.4):
        required by all functions that call 𝑓 to prove reﬁne-
                                                                      natural numbers, take 𝑛 𝑥𝑠 and drop 𝑛 𝑥𝑠 return and remove
        ment (Theorem 2.4).
                                                                      the ﬁrst 𝑛 elements of the list 𝑥𝑠 respectively, slice 𝑛 𝑚 𝑥𝑠 re-
      • Reﬁnement from the value semantics to the update se-
                                                                      turns the sublist that starts at index 𝑛 and ends at index 𝑚 of
        mantics (Theorem 2.5): required by all functions that
                                                                      the list 𝑥𝑠, ! returns the 𝑖 𝑡ℎ element of a list and @ appends
        call 𝑓 to prove reﬁnement (Theorem 2.5).
                                                                      two lists.
      • Reﬁnement from the polymorphic to monomorphic
                                                                         The operations get and mapAccum do not have straight-
        value semantics (Theorem 2.7): required by all func-
                                                                      forward analogues in the Isabelle library. mapAccum is not
        tions that call 𝑓 to prove reﬁnement (Theorem 2.7).
                                                                      part of the library at all, and must be implemented in terms
      • Reﬁnement from the shallow embedding to the poly-
                                                                      of fold, whereas get behaves diﬀerently to its corresponding
        morphic value semantics (Theorem 2.9): required by
                                                                      list operation: our implementation of get is not undeﬁned
        all functions that call 𝑓 to prove reﬁnement (Theo-
                                                                      when the given index is out of bounds, but instead returns
        rem 2.9).
                                                                      the provided default value.
                                                                         In Figure 5, we present a version of the template C im-
3     Arrays                                                          plementation of arrays with some syntactic simpliﬁcations
Arrays in Cogent are stored on the heap with elements hav-            for presentation. Quoted type parameters that are later in-
ing any unboxed type. Arrays of pointers are a separate data          stantiated to concrete Cogent types, such as T or O, are
structure in Cogent, as their interface is complicated by the         highlighted in blue. Generated C structure types for Cogent
uniqueness type system. We verify ﬁve array operations: the           records and tuples such as ArrayAcc, which normally have
length, get, and put functions in Figure 1, and the fold and          compiler-generated names, are written with human-friendly
mapAccum iterators in Figure 2.                                       names in grey. The dispatch functions highlighted in red are
                                                                      how Cogent deals with higher-order functions: Because the
3.1    Speciﬁcation and Implementation                                C-parser semantics do not accommodate function pointers,
Our operations on arrays are speciﬁed as Isabelle functions           Cogent instead assigns a unique identiﬁer to each function
on lists. The speciﬁcation for the array functions presented          at compile time, and deﬁnes a dispatch function for each
in Figures 1 and 2 is provided in Figure 4. Most array oper-          function type. This function takes a function identiﬁer as
ations have obvious analogues in Isabelle/HOL’s list library.         an argument and calls the function that corresponds to that
The library functions unat and of-nat convert words and               identiﬁer.
CPP ’22, January 17–18, 2022, Philadelphia, PA, USA                                                          Louis Cheung, Liam O’Connor, and Christine Rizkallah

 struct WArrayT {
    u32 len;
                                                                                           input is a pair of the Cogent store before the array operation
    T* vals;                                                                               and the argument(s) to the function, and the output is a pair
 };
 u32 length ( WArrayT *arr ) { return arr →len; }
                                                                                           of the store after the operation is complete and the return
 T get ( WArrayT *arr , u32 i, T def ) {                                                   value.
    if ( i < arr →len ) { return arr →vals[i]; }
    return def ;                                                                              Note that the deﬁnitions for fold and mapAccum are re-
 }                                                                                         cursive in two ways. The most obvious is the direct struc-
 WArrayT *put ( WArrayT *arr , u32 i, T v ) {
    if ( i < arr →len ) { arr →vals[i] = v ; }
                                                                                           tural recursion on the array indices, which is straightfor-
    return arr ;                                                                           ward for Isabelle to show terminates. The other form of re-
 }
 A fold ( fid f , A acc, WArrayT *arr , u32 frm, u32 to, O obsv ) {
                                                                                           cursion is the mutual recursion with the Cogent semantics
    u32 i , e;                                                                             (note that fold and mapAccum invoke the Cogent semantics
    e = arr →len;
    if ( to < e) { e = to; }
                                                                                           to evaluate the argument function). This is because the Co-
    for ( i = frm; i < e; i++) { acc = dispatch_fold ( f , arr →vals[i], acc, obsv ) ; }   gent semantics is itself parameterised by an environment (𝜉𝑢
    return acc;
 }                                                                                         and 𝜉 𝑣 ) containing the abstractions we are currently deﬁn-
 ArrayAcc mapAccum ( fid f , A acc, WArrayT *arr , u32 frm, u32 to, O obsv ) {             ing. We cannot deﬁne these embeddings and the Cogent
    u32 i , e;
    e = arr ->len;
                                                                                           semantics simultaneously as is normally done for mutual
    if ( to < e) { e = to; }                                                               deﬁnitions, however, since our abstractions are deﬁned by
    for ( i = frm; i < e; i++) {
        ElemAcc ea = dispatch_mapAccum ( f , arr →vals[i], acc, obsv ) ;
                                                                                           users later in the process after the semantics of Cogent have
        arr →vals[i] = ea.elem;                                                            already been deﬁned. Thus, we cannot close the recursion
        acc = ea.acc;
    }                                                                                      before users have provided these deﬁnitions. Therefore we
    ArrayAcc ret = { .arr = arr , .acc = acc } ;                                           must impose an additional constraint2 that an 𝑛-order ab-
    return ret;
 }                                                                                         stract function can only call a function of an order less than
                                                                                           𝑛. This forces us to prove reﬁnement for all functions of or-
 Figure 5. C implementation of key operations on arrays.                                   der 𝑛 − 1 or less, before we can prove reﬁnement for an
                                                                                           abstract function of order 𝑛. By imposing this ordering, we
                                                                                           can iteratively build up these environments in a staged way.
3.2    Proving Reﬁnement                                                                   This constraint is not burdensome, and is already satisﬁed
As previously mentioned, to verify our abstract C library, we                              by all Cogent codebases (see Rizkallah et al. [21]).
must additionally provide Isabelle/HOL abstractions of our                                    Since Cogent supports polymorphism, we in fact need to
C implementation that can connect with the automatically-                                  provide two abstractions for our operations in the value se-
generated Cogent embeddings. Speciﬁcally, we must pro-                                     mantics corresponding to the two value semantics layers in
vide Isabelle/HOL abstractions for each abstract function                                  our reﬁnement chain, monomorphic and polymorphic. Be-
(i.e., put, get, etc.), as well as a combined value-update-type                            cause our abstractions (and even our implementation) are
correspondence relation, analogous to the reﬁnement rela-                                  entirely parametric in the element type, the abstractions that
tion for Theorem 2.5, for each abstract type (i.e., WArrayT).                              are shown in Figure 6b can be used for both the monomor-
                                                                                           phic and the polymorphic layers, which, as we will see, trivi-
3.2.1 Abstractions. We extend the deﬁnition of Cogent                                      alises the reﬁnement proof for the monomorphisation layer
values with a new constructor for arrays. In the update se-                                of the hierarchy.
mantics, arrays take the form UWA 𝜏 len p, where 𝜏 is the
type of the array elements, len is the length of the array,                                3.2.2 Value Typing. Unlike the approach for native Co-
and p is a pointer to the ﬁrst element of the array. This is                               gent values, where the value typing relations are deﬁned as
quite similar to the representation used in C, where a struct                              erasures of the value-update reﬁnement relation, we shall
containing the length and a pointer is used (see Figure 5).                                deﬁne individual value-typing relations for arrays in the two
We additionally store the type in the Cogent value so that                                 semantics, and then combine them into a reﬁnement rela-
the same form of Cogent value can be used for all the dif-                                 tion in Deﬁnition 3.5
ferent structs generated by the Cogent compiler from the C                                    We deﬁne these typing relations with two equations, one
template. In the value semantics, however, arrays take the                                 for the writable arrays Array 𝜏, and one for read-only ar-
form VWA 𝜏 xs, where xs is simply an Isabelle/HOL list of Co-                              rays (Array 𝜏)!. In the value semantics, these two types are
gent values, similar to the representation used in the shallow                             identical, merely requiring that the list elements are well-
embedding (see Figure 4).                                                                  typed:
   The various array function abstractions supplied to Co-
gent are deﬁned as input-output relations that are later inter-
preted as functions, as shown in Figure 6. These abstractions
are derived directly from the axiomatisation used in the ver-                              2 This constraint is not a proof obligation, but merely a requirement for our

iﬁcation of BilbyFs. In the update semantics (Figure 6a), the                              framework to work automatically.
Composing Verification of Foreign Functions with Cogent                                    CPP ’22, January 17–18, 2022, Philadelphia, PA, USA


 lengthu (𝜇, x ) (𝜇’, y) =
    ∃𝜏 len p. (𝜇 x = UWA 𝜏 len p) ∧ (y = len) ∧ (𝜇 = 𝜇’)                  lengthv x y =
 getu (𝜇, (x , i, d )) (𝜇 ′ , y) =                                           ∃𝜏 xs. (x = VWA 𝜏 xs) ∧ (List.length xs = unat y)
    ∃𝜏 len p. (𝜇 x = UWA 𝜏 len p)                                         getv (x , i) y =
      ∧ (i < len −→ 𝜇 (p+(size t )×i) = y)                                   ∃𝜏 xs. (x = VWA 𝜏 xs)
      ∧ (i ≥ len −→ y = d ) ∧ (𝜇 = 𝜇 ′ )                                       ∧ (unat i < List.length xs −→ xs ! i = y)
 putu (𝜇, (x , i, v )) (𝜇 ′ , y) =                                             ∧ (unat i ≥ List.length xs −→ y = 0)
    ∃𝜏 len p. (𝜇 x = UWA 𝜏 len p)                                         putv (x , i, v ) y =
      ∧ (i < len −→ 𝜇(p+(size 𝜏)×i ↦→ v ) = 𝜇 ′ )                            ∃𝜏 xs. (x = VWA 𝜏 xs) ∧ (y = VWA 𝜏 xs[unat i ≔ v ])
      ∧ (i ≥ len −→ 𝜇 = 𝜇 ′ ) ∧ (x = y)                                   foldv (f , acc, x , s, e, obs) y =
 foldu (𝜇1 , (f , acc, x , s, e, obs)) (𝜇3 , y) =                            ∃𝜏 xs. (x = VWA 𝜏 xs)
    ∃𝜏 len p. (𝜇1 x = UWA 𝜏 len p)                                             ∧ (unat s < List.length xs ∧ s < e −→
      ∧ (s < len ∧ s < e −→                                                       ∃v acc ′ . (xs ! s = v )
         ∃v acc ′ 𝜇2 . 𝜇1 (p+(size 𝜏)×s) = v                                          ∧ [𝑎 ↦→ (v, acc, obs)] ⊢ 𝑓 𝑎 v acc ′
            ∧ [𝑎 ↦→ (v, acc, obs)] ⊢ 𝑓 𝑎 | 𝜇1 u acc ′ | 𝜇2                            ∧ foldv (f , acc ′ , x , s+1, e, obs) y)
            ∧ foldu (𝜇2 , (f , acc ′ , x , s+1, e, obs)) (𝜇3 , y))             ∧ (unat s ≥ List.length xs ∨ s ≥ e −→ y = acc)
      ∧ (s ≥ len ∨ s ≥ e−→ 𝜇1 = 𝜇3 ∧ y = acc)                             mapAccumv (f , acc, x , s, e, obs) y =
 mapAccumu (𝜇1 , (f , acc, x , s, e, obs)) (𝜇4 , y) =                        ∃𝜏 xs. (x = VWA 𝜏 xs)
    ∃𝜏 len p. (𝜇1 x = UWA 𝜏 len p)                                             ∧ (unat s < List.length xs ∧ s < e −→
      ∧ (s < len ∧ s < e −→                                                       ∃v v ′ acc ′ x ′ . xs ! s = v
         ∃v v ′ acc ′ 𝜇2 𝜇3 . 𝜇1 (p+(size 𝜏)×s) = v                                   ∧ [𝑎 ↦→ (v, acc, obs)] ⊢ 𝑓 𝑎 v (𝑣 ′, acc ′ )
            ∧ [𝑎 ↦→ (v, acc, obs)] ⊢ 𝑓 𝑎 | 𝜇1 u (v ′, acc ′ ) | 𝜇2                    ∧ x ′ = VWA 𝜏 xs[unat s ≔ v ′ ]
            ∧ 𝜇3 = 𝜇2 (p+(size t )×s ↦→ v ′ )                                         ∧ mapAccumv (f , acc ′ , x ′ , s+1, e, obs) y)
            ∧ mapAccumu (𝜇3 , (f , acc ′ , x , s+1, e, obs)) (𝜇4 , y))         ∧ (unat s ≥ List.length xs ∨ s ≥ e −→ y = (x , acc))
      ∧ (s ≥ len ∨ s ≥ e−→ 𝜇1 = 𝜇4 ∧ y = (x , acc))
                                                                                    (b) C abstractions for the value semantics.
             (a) C abstractions for the update semantics.

                                Figure 6. Cogent-compatible abstractions of C operations on arrays

Deﬁnition 3.1 (Array: Value Semantics Value Typing).                     Deﬁnition 3.2 (Array: Update Semantics Value Typing).
                                                                          okay (UWA 𝜏 len 𝑝) ≡ (unat len × size 𝜏 ≤ max_word)
                                                                          ∧ (∀𝑖 < len. ∃𝑣. 𝜇 (𝑝 + size 𝜏 × 𝑖) = 𝑣 ∧ 𝑣 |𝜇 : 𝜏 [∅ ∗ ∅])
  VWA 𝜏 xs : Array 𝜏    ≡ (∀𝑖 < List.length xs. xs ! 𝑖 : 𝜏)               UWA 𝜏 len 𝑝 |𝜇 : (Array 𝜏)! [𝑟 ∗ 𝑤] ≡ okay (UWA 𝜏 len 𝑝)
  VWA 𝜏 xs : (Array 𝜏)! ≡ ((VWA 𝜏 xs) : Array 𝜏)                                              ∧ (𝑟 = {𝑝 + 𝑖 | ∀𝑖. 𝑖 < len } ∧ 𝑤 = ∅)
                                                                          UWA 𝜏 len 𝑝 |𝜇 : (Array 𝜏) [𝑟 ∗ 𝑤] ≡ okay (UWA 𝜏 len 𝑝)
                                                                                              ∧ (𝑤 = {𝑝 + 𝑖 | ∀𝑖. 𝑖 < len } ∧ 𝑟 = ∅)
   For the update semantics, we deﬁne an auxiliary predi-
cate okay (UWA 𝜏 len 𝑝) which states that each of the values             where max_word is 232 − 1 (as we are using 32-bit pointers).
in the array (located at successive pointers starting at 𝑝) is
                                                                         Recall that these the value typing relations for abstract types
well typed, as well as a necessary condition on len to ensure
                                                                         must satisfy the constraints of Deﬁnition 2.12. Because ar-
that our pointer arithmetic will not result in overﬂow. This
                                                                         rays only have elements which are of unboxed types, these
predicate is used in the typing relation for both the writable
                                                                         constraints are trivial to discharge.
and read-only array types. The heap footprint [𝑟 ∗ 𝑤] must
consist of not just the pointer 𝑝 but all of the successive              3.2.3 Reﬁnement Relations. Just as Cogent’s typing re-
pointers to each array element, because all of these memory              lations and semantics are extended by our rules for arrays,
locations are contained in the array, and ownership of all of            so too are the various reﬁnement relations in each layer of
them is passed along with the array. Because the array con-              the semantics. Because, as previously mentioned, the C im-
tains only unboxed types, we know that there are no other                plementation of our arrays bears a strong resemblance to
pointers in the heap footprint. For the read-only array type,            our update semantics values, and our value semantics val-
𝑟 contains the heap footprint and 𝑤 is empty, and vice versa             ues bear a strong resemblance to our Isabelle/HOL list rep-
for the writable array type.                                             resentation, the value relations V uc and R sp for arrays are
                                                                         very simple. In the former, the two a related if the length
                                                                         values and the pointer values are equal. In the latter, the
CPP ’22, January 17–18, 2022, Philadelphia, PA, USA                                            Louis Cheung, Liam O’Connor, and Christine Rizkallah


two are related if the length of the lists are the same and the              Proof. Recall that the argument to put for arrays of 32-bit
elements are pairwise related.                                               words is a tuple that contains an index, the array, and a 32-
                                                                             bit word to write to it. We take cases on the index. In the
Deﬁnition 3.3 (U32 Array: Update ⇒ C Value Relation).
                                                                             case that the index is out of bounds, both the abstraction
V uc (𝑥 c, UWA U32 len u 𝑝 u ) ≡ (len u = lenc 𝑥 c ∧ 𝑝 u = arrc 𝑥 c )        (Figure 6a) and the implementation (Figure 5) return the ar-
where lenc and arrc are the struct projections generated                     ray unmodiﬁed with the store unmodiﬁed as well, and so
by AutoCorres for the array type.                                            the theorem is trivial. In the case where the index is within
                                                                             bounds, our value relation V uc on the arguments implies
Deﬁnition 3.4 (Array: Shallow ⇒ Polymorphic Relation).                       that the two argument words and indices are the same. Writ-
        R sp (𝑥 s, VWA 𝜏 xs p ) ≡ (length xs p = length 𝑥 s )                ing the same value to the same index within bounds only
               ∧ (∀𝑖 < length xs p . R sp (𝑥 s ! 𝑖, xs p ! 𝑖))               writes corresponding values to the same store locations, so
                                                                             it follows that our heap relation H uc is preserved. As it is de-
Because we use the same abstractions for both monomor-                       structively updated, the actual location of the array in mem-
                                                        p
phic and polymorphic layers, the reﬁnement relation R m is                   ory is not changed, so the relation V uc is trivially preserved
just equality and its reﬁnement theorem is trivial.                          to the output array.                                           
   Lastly, it remains to deﬁne the value relation for arrays
between the two Cogent semantics, update and value. As
previously mentioned, we make use of the two value typing                    For the next level up in the reﬁnement hierarchy, we must
relations here with additional conditions to pairwise relate                 show reﬁnement from our value semantics abstraction (Fig-
the corresponding elements of the two values:                                ure 6b) to our update semantics abstraction (Figure 6a). Even
                                                                             though this reﬁnement step is below monomorphisation in
Deﬁnition 3.5 (Array: Value (Mono) ⇒ Update Relation).
                                                                             our hierarchy, our abstractions for put are agnostic to the
                          R
   UWA 𝑡 len u 𝑝 u | 𝜇 ∼ VWA 𝑡 xs m : 𝜏 [𝑟 ∗ 𝑤] ≡                            element type of the array, so we can generalise the proof to
        (unat len u = length xs m )                                          arrays of any element type. The theorem resembles Theo-
     ∧ (∀𝑖 < len u . ∃vu . 𝜇(𝑝 u + (size 𝑡) × 𝑖) = vu                        rem 2.5, but with the Cogent semantics replaced with our
                        R
              ∧ vu | 𝜇 ∼ (xs m ! unat 𝑖) : 𝑡 [∅ ∗ ∅])                        supplied abstractions in 𝜉 v and 𝜉 u .
     ∧ (VWA 𝑡 xs m : 𝜏) ∧ (UWA 𝑡 len u 𝑝 u | 𝜇 : 𝜏 [𝑟 ∗ 𝑤])
                                                                             Theorem 3.7 (Verifying put: Value ⇒ Update reﬁnement).
Note the heap footprints of elements are always empty, as                                                           R
                                                                             For an element type 𝑡, if 𝑎 u |𝜇 ∼ 𝑎 m : (Array 𝑡, U32, 𝑡) [𝑟 ∗𝑤]
the array can only contain unboxed values.                                   and 𝜉 u (put𝑡 ) (𝜇, 𝑎 u ) = (𝜇 ′, 𝑣 u ), then there exists a value 𝑣 m and
3.2.4 Reﬁnement. Now that we have all our abstractions,                      pointer sets 𝑟 ′ ⊆ 𝑟 and 𝑤 ′ such that 𝜉 v (put𝑡 ) (𝑎 m ) = 𝑣 m , and
                                                                                      R
value typing and reﬁnement relations, we have all the ingre-                 𝑣 u |𝜇 ′ ∼ 𝑣 m : Array 𝑡 [𝑟 ′ ∗ 𝑤 ′ ] and 𝑤 | 𝜇 frame 𝑤 ′ | 𝜇 ′ .
dients we need to prove reﬁnement for our array operations.
   The theorems structurally resemble the reﬁnement theo-                    Proof. We also prove this by cases on the index. In the case
rems presented in Section 2.5. For ﬁrst order functions length,              where the index is out of bounds, we trivially have corre-
get and put, the proofs tend to follow easily from the deﬁni-                spondence. In the case where the index is within bounds, we
tion of their abstractions, implementation, reﬁnement rela-                  prove that modifying the element at the given index from
tion and value typing relation — the creativity is largely in                the pointer on the store is equivalent to modifying the ele-
the deﬁnitions, not the proofs. This is because we want the                  ment at the given index in the corresponding list. To prove
proofs to be easily automatable in future. Nonetheless we                    this, we need to show that there is a one-to-one mapping be-
shall sketch the proofs for our put operation, speciﬁcally                   tween store addresses of elements to list indices. This is why
for arrays of U32, as an illustrative example.                               we include in our typing relation that the array element ad-
   We ﬁrst show that the update semantics abstraction is re-                 dresses do not overﬂow the heap (Deﬁnition 3.2). Since this
ﬁned by the embedding of the C implementation that is au-                    tells us the array cannot wrap around itself, each element in
tomatically generated by AutoCorres. This appears similar                    the array has a unique address, giving us our mapping. We
to Theorem 2.4, but instead of invoking the Cogent update                    also need to show that that the frame conditions are satis-
semantics we instead appeal to our abstract function from                    ﬁed, but because our implementation is memory safe, these
the environment 𝜉 u (putU32 ):                                               follow easily from our deﬁnitions.                           
Theorem 3.6 (Verifying put: Update ⇒ C reﬁnement).
Where the C embedding of putU32 is put c :                                   Next, we must show reﬁnement from the polymorphic layer
    V uc (𝑎 c , 𝑎 u ) ∧ H uc (𝜎, 𝜇) ∧ 𝑎 c ⊢ 𝜎 | put c c      𝑟c   | 𝜎 ′ −→   to the monomorphic layer, but because put is a ﬁrst-order
          ∃ 𝜇 ′ 𝑟 u . 𝜉𝑢 (putU32 ) (𝜇, 𝑎 u ) = (𝜇 ′, 𝑟 u )                   function (neither taking functions as arguments nor return-
                    ∧ V uc (𝑟 c, 𝑟 u ) ∧ H uc (𝜎 ′, 𝜇 ′ )                    ing them), the value relations for its arguments and return
Composing Verification of Foreign Functions with Cogent                                         CPP ’22, January 17–18, 2022, Philadelphia, PA, USA


values simplify to equality. Furthermore, as our Cogent ab-                      repeats : nat → (𝑎 → 𝑏 → bool) → (𝑎 → 𝑏 → 𝑎)
stractions for monomorphic and polymorphic layers are iden-                           →𝑎 →𝑏 →𝑎
tical, the proof of reﬁnement is trivialised to showing that                     repeats 0 _ _ acc _ = acc
identical functions will give equal results given equal inputs.                  repeats (Suc n) f g acc obsv = if (f acc obsv )
   Monomorphisation thus easily dispatched, we must now                            then acc else repeats n f g (g acc obsv ) obsv
make the ﬁnal shift to the speciﬁcation level (Figure 4). We
must prove a theorem analogous to Theorem 2.9. Note that                          Figure 7. Shallow embedding of the generic loop
this theorem is also generic for any element type:

Theorem 3.8 (Verifying put: Shallow ⇒ Polymorphic Value).                   maintaining Cogent’s invariants is even more straightfor-
The shallow embedding of put is called puts . Given arguments               ward than for other higher-order functions such as mapAc-
𝑎 s and 𝑎 p , we have:                                                      cum, as here we do not even need to consider custom data
                                                                            structures such as arrays. This means that we can even de-
       R sp (𝑎 p, 𝑎 s ) ∧ 𝜉 v (put) (𝑎 p ) = 𝑟 p −→                         ﬁne a polymorphic abstraction of the C code compatible
                               ∃𝑟 s . 𝑎 s ⊢ puts s 𝑟 s ∧ R sp (𝑟 p, 𝑟 s )   with AutoCorres, enabling us to prove the entire reﬁnement
                                                                            chain polymorphically and thereby largely eliminate the boil-
Proof. Follows from the deﬁnitions of putv (in 𝜉 v ) and puts ,             erplate of multiple type instantiations.
as well as the value relation from Deﬁnition 3.4.          
                                                                            5 Composing Veriﬁcation of Cogent and C
The above theorems are all we need to compose the correct-                  Now that we have demonstrated how to prove the obliga-
ness of put with Cogent’s reﬁnement hierarchy. For higher-                  tions placed on C code, we shall illustrate how to integrate
order functions fold and mapAccum the proofs are broadly                    these proofs with proofs about Cogent code. Firstly, as a sim-
similar, but slightly complicated by the presence of func-                  ple example, we return to the sum function presented in Fig-
tions as arguments. Our theorems assume that type preser-                   ure 2.
vation and reﬁnement hold for all of their argument func-                      After compiling this program and linking it to our C li-
tions — an assumption that is discharged by the Cogent com-                 brary, the compiler produces a reﬁnement theorem similar
piler (for Cogent functions) or by manual proofs (for C func-               to Theorem 2.11, however the phases that are generated per-
tions). As always with looping functions, the majority of the               program via translation validation such as the ﬁnal reﬁne-
proof eﬀort was concentrated on proving that loop invari-                   ment to C leave open proof obligations for the user to dis-
ants are maintained, and not on any aspect of the Cogent                    charge about abstract functions3 . In our sum example, Co-
framework.                                                                  gent will generate obligations about length and about fold.
                                                                            The obligation about length is exactly our C reﬁnement the-
4    Generic Loops                                                          orem for length (the length analogue of Theorem 3.6), and
Aside from arrays and their associated iterators and opera-                 the obligation for fold is an instance of our theorem for fold:
tions, the most commonly used library functions in BilbyFs                  the obligation requires showing reﬁnement under the as-
are generic loop functions. These are used to write loops                   sumption that the argument function is add, whereas our
that do not simply iterate over a particular data structure,                theorem is generically proven for any function that main-
and are often used to accommodate non-standard search                       tains Cogent’s invariants and reﬁnement. Because add is de-
patterns over data structures. For example, in Section 5.2                  ﬁned in Cogent, Cogent generates the required theorem for
we shall use such a function in a binary search.                            the argument function for us, allowing us to easily discharge
   We shall verify the function repeat, which is given the                  this obligation.
following type signature in Cogent:                                            We additionally must instantiate our sets of abstract val-
                                                                            ues and types with arrays, and the environments 𝜉 v and 𝜉 u
    repeat : (U32, (𝑎, 𝑏!) → Bool, (𝑎, 𝑏!) → 𝑎, 𝑎, 𝑏!) → 𝑎                  with our abstractions from Figure 6. This instantiation re-
                                                                            quires us to additionally provide proofs similar to that of
The expression repeat n stop step acc obs operates on some
                                                                            Theorem 3.7 for each function, as well as proofs that all the
mutable state acc (of linear type) and some observer data
                                                                            type conditions from Section 2.7. These proofs ultimately
obs (of read-only type), and runs the loop body step on it at
                                                                            connect our C code to the generated shallow embedding,
most 𝑛 times, or until stop returns true. Figure 7 gives the
                                                                            which strongly resembles the original Cogent code:
Isabelle/HOL shallow embedding and Figure 8 gives the tem-
plate C implementation. Figure 9 gives the Cogent-compatible                          adds 𝑥 𝑦 = 𝑥 + 𝑦
embeddings for the environments 𝜉𝑢 and 𝜉 v . Note that these                          sums xs = folds adds 0 xs 0 (length𝑠 xs) ()
must invoke the Cogent semantics twice, once to evaluate                    3 At the time of writing, Cogent’s shallow phase (Theorem 2.9) implicitly
each of the argument functions. Discharging the required                    assumes abstract function correctness rather than doing so explicitly as
proof obligations connecting all of these embeddings and                    done in other phases. So for now, we just copy and discharge these.
CPP ’22, January 17–18, 2022, Philadelphia, PA, USA                              Louis Cheung, Liam O’Connor, and Christine Rizkallah


       A repeat(u32 n, fid f , fd g, A acc, O obsv ) {            valid, i.e., the array’s size (in bytes) is less than the size of
         for(u32 i = 0; i < n; i++)                               memory (232 bytes) and is well-formed, and same (𝜎, 𝜎 ′, arr )
           if (dispatch_f (f , acc, obsv )) break;                be the predicate that states that an array is the same for the
           else acc = dispatch_g(g, acc, obsv );                  given C heaps:
         return acc;                                               sorted xs ∧ valid (𝜎, arr ) ∧
       }                                                           (arr, v ) ⊢ 𝜎 | binary-searchc c 𝑖 | 𝜎 ′ −→
                                                                      valid (𝜎 ′, arr ) ∧ same (𝜎, 𝜎 ′ , arr ) ∧
      Figure 8. C implementation of the generic loop.                 (unat i < length xs −→ xs ! (unat i) = v ) ∧
                                                                      (¬ unat i < length xs −→ v ∉ set xs)
With all of these proofs in place, we get a reﬁnement theo-       This theorem depends on no additional assumptions about
rem like Theorem 2.11 for the function sum, which leaves no       any functions or any other part of the Cogent framework.
function unveriﬁed. This reﬁnement theorem allows us to           With this, we have shown that the Cogent framework en-
prove properties of sums just by equational reasoning, and        ables the veriﬁcation of combined Cogent-C systems.
have these proofs also apply to the C implementation.
                                                                  6 Related Work
5.1 Verifying C Parts of BilbyFs                                     Compiler Correctness. Patterson and Ahmed [18] have
As mentioned, the previous veriﬁcation of the functional          deﬁned a spectrum of compiler veriﬁcation theorems focus-
correctness of key operations in BilbyFs [3] simply assumed       ing on compositional compiler correctness, extensible through
the correctness of abstract functions, including an axioma-       linking. Cogent’s certifying compiler does not neatly fall on
tisation of array operations [2]. We removed the axiomati-        this spectrum as the compiler itself does the linking of the
sation for the ﬁve core array operations that we veriﬁed,         Cogent-C system, and we are linking with manually veriﬁed
and were able to show that the functional correctness proofs      C rather than other compiler outputs.
compose for the combined system. The array operations that           Like Cogent, the Cito language [23] allows cross-language
remain unveriﬁed are functions like create, set, copy, cmp,       linking and combined veriﬁcation in a proof assistant. Un-
that depend on platform-speciﬁc functions such as malloc.         like Cogent, Cito is a low-level C-like language without a so-
                                                                  phisticated type system, so there are no FFI requirements to
                                                                  enforce static guarantees. Pit-Claudel et al. [19] use Cito as a
5.2 Binary Search                                                 target for veriﬁed compilation of relational queries, and sup-
Figure 10 gives the Cogent code for binary search using our       port linking with foreign assembly code, but do not compose
previously deﬁned and veriﬁed array functions and repeat.         veriﬁcation across languages for reﬁnement from a common
Note that while we specify the maximum number of iter-            high-level spec, as we do.
ations to repeat as the length of the array, the algorithm           An important part of veriﬁed compilation is how the se-
is still O(log 𝑛) as it will always exit early from the stop      mantics of linking is deﬁned for the source language. The
condition. This fuel argument is an easy way to ensure that       simplest way to deﬁne linking on the source language is to
Isabelle is convinced that our functions terminate.               require that a program may only be linked if it reﬁnes a pro-
   We ﬁrstly prove that the generated shallow embedding,          gram deﬁnable in the source language. SepCompCert [7]
which strongly resembles the Cogent code, is correct:             and Pilsner [13] take this approach. This approach is suit-
                                                                  able for languages which, unlike Cogent, are expressive enough
Theorem 5.1 (Correctness of Cogent binary search). Let i=
                                                                  to encompass all programs, but we require C functions to
unat (binary-searchs (xs, v )) in
                                                                  reﬁne more expressive speciﬁcations than what is deﬁnable
 sorted xs ∧ length xs < 232 −→
                                                                  natively in Cogent. The Cogent compiler instead generates
    (i < length xs −→ xs ! i = v )
                                                                  shallow embeddings of Cogent programs in Isabelle/HOL,
   ∧ (¬ i < length xs −→ v ∉ set xs)
                                                                  that enable linking at the Isabelle speciﬁcation level. Hence,
where length, set, and sorted are Isabelle’s list library func-   Cogent supports source-independent linking insofar as we
tions that return the length of a list, turn a list to a set,     can embed all source languages inside Isabelle/HOL.
and check whether a list is sorted, respectively. We denote
                                                                     Veriﬁcation Approach. Arrays are widely used data struc-
search failure by returning an index that is out of bounds.
                                                                  tures, particularly in low level systems programming. Auto-
   From our overall reﬁnement theorem (Theorem 2.11), we
                                                                  Corres [5, 6] simpliﬁes the veriﬁcation of C code by abstract-
can easily conclude that the C implementation is correct and
                                                                  ing it into a monadic embedding of C in Isabelle/HOL. The
remove any reference to Cogent:
                                                                  Cogent compiler further simpliﬁes reasoning about the Co-
Corollary 5.2 (Correctness of the C binary search).               gent parts of a system by abstracting AutoCorres’ monadic
Let xs be the list abstraction of the array arr for C heap 𝜎,     C into a purely functional Cogent embedding in Isabelle/HOL.
valid (𝜎, arr ) be the predicate that states that the array is    For foreign functions, abstraction from AutoCorres’ monadic
Composing Verification of Foreign Functions with Cogent                                            CPP ’22, January 17–18, 2022, Philadelphia, PA, USA


 repeatu (𝜇 1 , (n, f , g, acc, obs)) (𝜇 3 , y) =                               repeatv (n, f , g, acc, obs) y =
   (n > 0 −→                                                                      (n > 0 −→
        ∃b. [𝑎 ↦→ (acc, obs)] ⊢ 𝑓 𝑎 | 𝜇 1 u b) | 𝜇 1 ∧                                 ∃b. [𝑎 ↦→ (acc, obs)] ⊢ 𝑓 𝑎 v b) ∧
          (b −→ 𝜇 1 = 𝜇 3 ∧ y = acc) ∧                                                   (b −→ y = acc) ∧
          (¬b −→ ∃𝜇 2 acc ′ .                                                            (¬b −→ ∃acc ′ .
                 [𝑎 ↦→ (acc, obs)] ⊢𝑔 𝑎 | 𝜇 1 u acc ′ | 𝜇 2 ∧                                   [𝑎 ↦→ (acc, obs)] ⊢𝑔 𝑎 v acc ′ ∧
                 repeatu (𝜇 2 , (n-1, f , g, acc ′ , obsv )) (𝜇 3 , y))) ∧                      repeatv (n-1, f , g, acc ′ , obsv ) y)) ∧
   (n = 0 −→ 𝜇 1 = 𝜇 3 ∧ y = acc)                                                 (n = 0 −→ y = acc)
            (a) C abstractions for the update semantics.                                   (b) C abstractions for the value semantics.

                                       Figure 9. Cogent-compatible abstraction for the generic loop.

 type Range = (U32, U32, Bool)                                                 arrays as built in types in Cogent and extending the com-
 stop : (Range, ((Array U32)!, U32)) → Bool                                    piler certiﬁcate to account for a number of array operations.
 stop ((l , r , b), (arr , v )) = 𝑏 ∨ 𝑙 ≥ 𝑟                                    Even then, we believe that the language interoperability ap-
 search : (Range, ((Array U32)!, U32)) → Range
                                                                               proach presented in this paper remains valuable. It serves
 search ((l , r , b), (arr , v )) =
   let m = l + (r - l ) ÷ 2 and
                                                                               as a reference for how Cogent users and system develop-
       x = get (arr , m, 0)                                                    ers can contribute their own additional data structures with
   in if | x < v → (m+1, r , b)                                                their preferred implementation to Cogent rather than re-
           | x > v → (l , m, b)                                                lying solely on Cogent developers to extend the language
           | else → (m, r , True)                                              with each desired additional data structure and data struc-
 binary-search : ((Array U32)!, U32) → U32                                     ture operation. Moreover, operations that are directly imple-
 binary-search (arr , v ) =                                                    mented in C and called through the FFI may occasionally
   let len = length arr and                                                    be implemented more eﬃciently than if they were directly
       (l , r , b) = repeat (len, stop, search, (0, len, False), (arr , v ))   implemented in Cogent. This is because users can escape
   in if b then l else → len                                                   the Cogent type system when implementing operations in
                                                                               C and for instance use internal aliasing within a function’s
    Figure 10. The binary search algorithm in Cogent.                          implementation as long as they can prove that the overall C
                                                                               implementation respects the frame invariant.

C embedding to a purely functional embedding is manu-
ally veriﬁed through intermediate Cogent embeddings. Au-                       7 Conclusion
toCorres comes with a number of examples including binary
                                                                               We have demonstrated our cross-language approach to prov-
search and QuickSort on 32-bit word arrays which use the
                                                                               ing software correct. Our systems mix Cogent, a safe func-
get and put operations. Their proofs for these operations
                                                                               tional language with a compiler that proves most of the re-
(roughly 250 lines) are about half the size of ours but ours
                                                                               quired theorems automatically, and C, an unsafe imperative
are reusable for arrays with elements of any unboxed type.
                                                                               language with few guarantees. Speciﬁcally, we veriﬁed the
   If we were only concerned with proving functional cor-
                                                                               array implementation and general loop iterators provided in
rectness of an array implementation, we could have taken a
                                                                               Cogent’s ADT library, which were used the implementation
top down approach, i.e., generate an implementation from
                                                                               of real-world ﬁle systems, and we showed that they main-
the speciﬁcation, using existing tools or frameworks [9–11],
                                                                               tain the invariants required by Cogent. This enabled us to
rather than prove that an implementation reﬁnes its speciﬁ-
                                                                               eliminate some key assumptions in the pre-existing veriﬁca-
cation. While a top down approach would likely lessen the
                                                                               tion of the BilbyFs ﬁle system in Cogent. These case-studies
veriﬁcation burden, our approach allows for more control
                                                                               demonstrate that manual C veriﬁcation can be straightfor-
over the implementation and is suitable for cases where an
                                                                               wardly composed with Cogent’s reﬁnement chain, leading
implementation already exists, as is the case for BilbyFs.
                                                                               to a top-level shallow embedding that can be seamlessly con-
   As mentioned in the introduction, Cogent purposely lacks
                                                                               nected with functional correctness speciﬁcations to ensure
recursion and iteration in order to ensure totality. There
                                                                               the correctness of an overall Cogent-C system.
is an ongoing eﬀort to add a limited form of recursion to
Cogent [12] while retaining totality through a termination
checker [12, 20]. Extending the proof infrastructure of Co-
gent to support recursive types and to certify termination                     Acknowledgments
for functions that pass the termination checker is non-trivial                 This research is partially supported by an Australian Gov-
and still remains open. Additionally, we are exploring adding                  ernment Research Training Program (RTP) Scholarship.
CPP ’22, January 17–18, 2022, Philadelphia, PA, USA                                              Louis Cheung, Liam O’Connor, and Christine Rizkallah


References                                                                          Gerwin Klein. September 2016.
 [1] Amal Ahmed. Compositional Compiler Veriﬁcation for a Multi-               [17] Liam O’Connor, Zilin Chen, Christine Rizkallah, Vincent Jackson, Sid-
     Language World. In Delia Kesner and Brigitte Pientka, editors, 1st             ney Amani, Gerwin Klein, Toby Murray, Thomas Sewell, and Gabriele
     International Conference on Formal Structures for Computation and De-          Keller. Cogent: Uniqueness types and certifying compilation. Journal
     duction (FSCD 2016), volume 52 of Leibniz International Proceedings in         of Functional Programming, 31:E25, 2021.
     Informatics (LIPIcs), pages 1:1–1:1, Dagstuhl, Germany, 2016. Schloss     [18] Daniel Patterson and Amal Ahmed. The next 700 compiler cor-
     Dagstuhl–Leibniz-Zentrum fuer Informatik.                                      rectness theorems (functional pearl). Proc. ACM Program. Lang.,
 [2] Sidney Amani. A Methodology for Trustworthy File Systems. PhD the-             3(ICFP):85:1–85:29, 2019.
     sis, University of New South Wales, Sydney, Australia, August 2016.       [19] Clément Pit-Claudel, Peng Wang, Benjamin Delaware, Jason Gross,
 [3] Sidney Amani, Alex Hixon, Zilin Chen, Christine Rizkallah, Peter               and Adam Chlipala. Extensible extraction of eﬃcient imperative
     Chubb, Liam O’Connor, Joel Beeren, Yutaka Nagashima, Japheth Lim,              programs with foreign functions, manually managed memory, and
     Thomas Sewell, Joseph Tuong, Gabriele Keller, Toby Murray, Gerwin              proofs. In Nicolas Peltier and Viorica Sofronie-Stokkermans, editors,
     Klein, and Gernot Heiser. Cogent: Verifying high-assurance ﬁle sys-            Automated Reasoning, pages 119–137, Cham, 2020. Springer Interna-
     tem implementations. In International Conference on Architectural              tional Publishing.
     Support for Programming Languages and Operating Systems, pages            [20] Lucy Qiu. Termination checker for recursive types in Cogent, 2020.
     175–188, Atlanta, GA, USA, April 2016. Association for Computer Ma-       [21] Christine Rizkallah, Japheth Lim, Yutaka Nagashima, Thomas Sewell,
     chinery.                                                                       Zilin Chen, Liam O’Connor, Toby Murray, Gabriele Keller, and Ger-
 [4] Cogent FFI examples (code and proofs), 2021.                                   win Klein. A framework for the automatic formal veriﬁcation of
 [5] David Greenaway, June Andronick, and Gerwin Klein. Bridging the                reﬁnement from Cogent to C. In International Conference on Inter-
     gap: Automatic veriﬁed abstraction of C. In International Conference           active Theorem Proving, pages 323–340, Nancy, France, August 2016.
     on Interactive Theorem Proving, pages 99–115, Princeton, New Jersey,           Springer, Cham.
     USA, August 2012. Springer Berlin Heidelberg.                             [22] Philip Wadler. Linear types can change the world! In Programming
 [6] David Greenaway, Japheth Lim, June Andronick, and Gerwin Klein.                Concepts and Methods. North, 1990.
     Don’t sweat the small stuﬀ: Formal veriﬁcation of C code without the      [23] Peng Wang, Santiago Cuellar, and Adam Chlipala. Compiler veriﬁca-
     pain. In ACM SIGPLAN Conference on Programming Language Design                 tion meets cross-language linking via data abstraction. In Andrew P.
     and Implementation, pages 429–439, Edinburgh, UK, June 2014. ACM.              Black and Todd D. Millstein, editors, Proceedings of the 2014 ACM In-
 [7] Jeehoon Kang, Yoonseung Kim, Chung-Kil Hur, Derek Dreyer, and                  ternational Conference on Object Oriented Programming Systems Lan-
     Viktor Vafeiadis. Lightweight veriﬁcation of separate compilation. In          guages & Applications, OOPSLA 2014, part of SPLASH 2014, Portland,
     Proceedings of the 43rd Annual ACM SIGPLAN-SIGACT Symposium on                 OR, USA, October 20-24, 2014, pages 675–690. ACM, 2014.
     Principles of Programming Languages, POPL ’16, page 178–190, New          [24] Simon Winwood, Gerwin Klein, Thomas Sewell, June Andronick,
     York, NY, USA, 2016. Association for Computing Machinery.                      David Cock, and Michael Norrish. Mind the gap: A veriﬁcation frame-
 [8] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick,                work for low-level C. In S. Berghofer, T. Nipkow, C. Urban, M. Wenzel,
     David Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt,                  editor, International Conference on Theorem Proving in Higher Order
     Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and               Logics, pages 500–515, Munich, Germany, August 2009. Springer.
     Simon Winwood. seL4: Formal veriﬁcation of an OS kernel. In ACM
     Symposium on Operating Systems Principles, pages 207–220, Big Sky,
     MT, USA, October 2009. Association for Computer Machinery.
 [9] Peter Lammich. Generating veriﬁed LLVM from Isabelle/HOL. In
     John Harrison, John O’Leary, and Andrew Tolmach, editors, 10th In-
     ternational Conference on Interactive Theorem Proving, ITP 2019, Sep-
     tember 9-12, 2019, Portland, OR, USA, volume 141 of LIPIcs, pages 22:1–
     22:19, Portland, 2019. Schloss Dagstuhl - Leibniz-Zentrum für Infor-
     matik.
[10] Peter Lammich. Reﬁnement to imperative HOL. Journal of Automated
     Reasoning, 62(4):481–503, Apr 2019.
[11] Peter Lammich and Andreas Lochbihler. The Isabelle collections
     framework. In Matt Kaufmann and Lawrence C. Paulson, editors,
     Interactive Theorem Proving, pages 339–354, Berlin, Heidelberg, 2010.
     Springer Berlin Heidelberg.
[12] Emmet Murray.                Recursive types for Cogent, 2019.
     https://github.com/emmet-m/thesis. Accessed November 2021.
[13] Georg Neis, Chung-Kil Hur, Jan-Oliver Kaiser, Craig McLaughlin,
     Derek Dreyer, and Viktor Vafeiadis. Pilsner: A compositionally veri-
     ﬁed compiler for a higher-order imperative language. In Proceedings
     of the 20th ACM SIGPLAN International Conference on Functional Pro-
     gramming, ICFP 2015, page 166–178, New York, NY, USA, 2015. Asso-
     ciation for Computing Machinery.
[14] Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. Is-
     abelle/HOL - A Proof Assistant for Higher-Order Logic, volume 2283
     of Lecture Notes in Computer Science. Springer, 2002.
[15] Liam O’Connor. Type Systems for Systems Types. PhD thesis, Univer-
     sity of New South Wales, 2019.
[16] Liam O’Connor, Zilin Chen, Christine Rizkallah, Sidney Amani,
     Japheth Lim, Toby Murray, Yutaka Nagashima, Thomas Sewell, and
