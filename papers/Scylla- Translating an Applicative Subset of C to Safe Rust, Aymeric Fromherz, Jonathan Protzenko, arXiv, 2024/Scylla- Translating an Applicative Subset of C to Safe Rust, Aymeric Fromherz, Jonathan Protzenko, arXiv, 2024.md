                                         Scylla: Translating an Applicative Subset of C to Safe Rust
                                         AYMERIC FROMHERZ, Inria, France
                                         JONATHAN PROTZENKO, Google, USA
                                         The popularity of the Rust language continues to explode; yet, many critical codebases remain authored in
                                         C. Automatically translating C to Rust is thus an appealing course of action. Several works have gone down
                                         this path, handling an ever-increasing subset of C through a variety of Rust features, such as unsafe. While
                                         the prospect of automation is appealing, producing code that relies on unsafe negates the memory safety
arXiv:2412.15042v2 [cs.PL] 25 Feb 2026




                                         guarantees offered by Rust, and therefore the main advantages of porting existing codebases to memory-safe
                                         languages. We instead advocate for a different approach, where the programmer iterates on the original C,
                                         gradually making the code more structured until it becomes eligible for compilation to safe Rust. This means
                                         that redesigns and rewrites can be evaluated incrementally for performance and correctness against existing
                                         test suites and production environments.
                                            Compiling structured C to safe Rust relies on the following contributions: a type-directed translation from
                                         (a subset of) C to safe Rust; a novel static analysis based on “split trees” which allows expressing C’s pointer
                                         arithmetic using Rust’s slices and splitting operations; an analysis that infers which borrows need to be
                                         mutable; and a compilation strategy for C pointer types that is compatible with Rust’s distinction between
                                         non-owned and owned allocations. We evaluate our approach on real-world cryptographic libraries, binary
                                         parsers and serializers, and a file compression library. We show that these can be rewritten to Rust with small
                                         refactors of the original C code, and that the resulting Rust code exhibits similar performance characteristics
                                         as the original C code. As part of our translation process, we also identify and report undefined behaviors in
                                         the bzip2 compression library and in Microsoft’s implementation of the FrodoKEM cryptographic primitive.
                                         CCS Concepts: • Software and its engineering → Source code generation; Software maintenance tools.
                                         Additional Key Words and Phrases: Rust, Compilation, Semantics
                                         ACM Reference Format:
                                         Aymeric Fromherz and Jonathan Protzenko. 2026. Scylla: Translating an Applicative Subset of C to Safe Rust.
                                         Proc. ACM Program. Lang. 10, OOPSLA1, Article 121 (April 2026), 27 pages. https://doi.org/10.1145/3798229

                                         1   Introduction
                                         Despite decades of research, memory safety issues remain prevalent in industrial applications;
                                         recent studies by Google [49] and Microsoft [50] estimate that 70% of security vulnerabilities are
                                         related to incorrect memory handling. To tackle this issue, both companies and governments now
                                         advocate for the use of memory-safe languages for safety-critical systems, notably, Rust [29, 52, 53].
                                            Combining the high performance and low-level idioms commonly provided by languages like
                                         C and C++ with memory safety by design, the Rust programming language continues to enjoy
                                         record levels of popularity in industry, being ranked as the “most admired programming language”
                                         for the eighth year in a row [46, 56], leading several widely used projects to plan a transition to
                                         Rust [4, 20, 28, 45, 51]. However, while Rust offers clear benefits for new, clean-slate code, the value
                                         proposition is less clear for existing code. Indeed, it can be hard, especially in an industrial setting,
                                         to justify rewriting code that has been battle-tested, thoroughly debugged, and exhibits no glaring
                                         Authors’ Contact Information: Aymeric Fromherz, aymeric.fromherz@inria.fr, Inria, France; Jonathan Protzenko, protz@
                                         google.com, Google, USA.



                                         This work is licensed under a Creative Commons Attribution 4.0 International License.
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM 2475-1421/2026/4-ART121
                                         https://doi.org/10.1145/3798229


                                                                     Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:2                                                                      Aymeric Fromherz and Jonathan Protzenko


issues. In those situations, Rust is perceived as a “nice to have” and particularly useful to develop
new features, but certainly not a business priority [55].
   To help with the transition, several recent projects therefore propose to automatically translate C
code to Rust [10, 21, 44]. To support the entirety of the C language, and thus to be directly applicable
to existing, diverse codebases, these tools however target unsafe Rust, which allows the use of C-like
idioms such as unchecked pointers or casts between representations (“transmutations”, in Rust
lingo) at the cost of statically guaranteed memory safety, therefore defeating the purpose of using
safe languages. The intended workflow is to use the output of the translation as a starting point,
before iteratively rewriting generated Rust code into a safer version; several recent approaches
propose static analyses to assist with this process by, e.g., identifying raw pointers that can be
transformed into regular safe Rust borrows [7], or reconstructing native Rust abstractions out of
low-level representations [14, 16].
   Following this workflow however raises several challenges. First, tooling for refactoring translated
Rust code is lacking, and previously proposed analyses and refactoring passes are scattered across a
variety of standalone projects [6, 13–15, 17]. Case in point, even c2rust, one of the leading tools for
C to Rust translation, dropped support for its refactoring tool (c2rust refactor) in 20221 . Second,
refactoring generated code is complex and error-prone, oftentimes leading to deep structural
rewrites whose correctness may be hard to test in the new (Rust) environment. Indeed, battle-tested,
industrial C projects are commonly equipped with an extensive testing infrastructure, including
performance, compliance, and integration tests, which is a crucial part of software development
and refactoring processes. Modifying familiar C code is easier for developers, and a much less risky
proposition than whole-codebase refactoring of autogenerated unsafe Rust.
   In this paper, we advocate for a new approach, where the programmer incrementally rewrites
their C code to give it more structure, until such time as it becomes eligible to compilation to Rust.
Aiming to make our translation predictable and to generate Rust code close to the original C sources,
we focus on an applicative subset of C: we target code that manipulates and processes data, performs
pointer-arithmetic, has structured control-flow, and is portable. In particular, we do not support
codebases that rely on gotos, or that leverage object representation through integer-to-pointer
casts, pointer tricks, bitfields, or untagged unions.
   We start from Clang’s frontend AST, and translate it to a first language dubbed “Mini-C”. Doing
so, we resolve typical C subtleties, such as integer promotions, integer conversions, assignments-
as-expressions, post- vs. pre-increments, and so on. Then, we define a type-directed translation
from Mini-C to safe Rust, relying on a novel, type-directed approach to compile structured pointer
arithmetic to Rust slices and slice splitting, followed by several novel post-translation analyses to
soundly infer mutability quantifiers, derive traits, and other Rust-specific features.
   We implement our approach in a tool, Scylla (pronounced “C-like”), which relies on Clang to
consume existing C code and output safe Rust; we provide an overview of Scylla in Figure 1. To fit
the Mini-C subset and guide the tool, we propose the use of targeted rewritings and annotations on
the source C program, to, e.g., rewrite aliasing patterns incompatible with Rust’s borrow checker,
or inform Scylla that a tagged union should be translated to a high-level abstract data type (ADT).
   We finally evaluate our approach on several existing C projects, showcasing that our applicative
C subset covers several security-sensitive applications. Our case studies include parts of Windows’s
SymCrypt [26] and of the HACL★ [38] cryptographic libraries, the core part of the bzip2 compression
algorithm [48], binary parsers and serializers from the EverParse library [41] for the CBOR data
format [18], and a recent Microsoft implementation of the FrodoKEM post-quantum cryptographic


1 https://github.com/immunant/c2rust/releases/tag/v0.16.0



Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                       121:3


                               clang                   §2 Explicit Casts,
                 C Code                   C AST                              Mini-C AST
                                                       ADTs, Tuples, . . .
                                                                                    §3.2 Eliminating
                                                                                    Pointer Arithmetic
                                               §3.3 Mutability,
                 Rust Code                                                    Rust AST
                                             §3.4 Trait Inference


                                       Fig. 1. Overview of the Scylla Translation

primitive [27]. As part of the translation process, we also identify and report several undefined
behaviors present in the source C code of both bzip2 and FrodoKEM.

2     Formalizing Mini-C
We start this paper by formally presenting Mini-C, the language that we compile to safe Rust in
Section 3. We also describe how to obtain Mini-C from actual C (as parsed by Clang).

2.1    The Mini-C Language
Mini-C (Figure 2) shares many features with C: it contains standard control-flow constructs such
as branching and loops, and heavily relies on pointers and pointer operations, such as dereferences
or address-taking. However, unlike C, Mini-C has a “no-surprises” semantics. All integers have
a fixed width, and C concepts such as integer promotion or integer conversions are represented
explicity using casts. Untyped pointers (void *) are also not permitted. Another key distinction is
that Mini-C is an expression language, unlike C which distinguishes statements and expressions. A
concrete consequence is that assignments do not return a value in Mini-C – C constructs such as
e1 = e2 = e3, or p[i++] are all desugared in Mini-C. Finally, although we omit its typing rules, Mini-C
has proper handling of the bool type, meaning loops and conditionals expect test expressions at
type bool, instead of int like in C.
   Beyond these basic constructs, Mini-C also features high-level constructs such as tuples or ADTs
(abstract data types, also known as variant types), along with pattern-matching expressions to
destruct them. These can be synthesized via a mechanism of custom annotations which indicate
the intent of the original C program – we detail this in Section 2.4.
   We remark that making Mini-C an expression language incurs no loss of generality: a statement-
and-expression language can simply be seen as an expression language, where statements have
type unit, and where the ; operator has type unit -> 'a -> 'a. It does have the advantage, however,
of simplifying the formalism since there is only one syntactic category.

2.2    A Type-Directed Translation to Mini-C
We now aim to generate a Mini-C representation out of a C program. To do so, we first query the
clang compiler to extract the typed abstract syntax tree (AST) of a given compilation unit, which
we then translate to a Mini-C typed AST. For conciseness, we omit a formal presentation of actual
C syntax, which we expect is familiar to most readers.
   This translation to Mini-C is challenging for several reasons. First, as mentioned earlier, Mini-C
is stricter about typing: loop and conditional test expressions must be at type bool, and array indices
must be at type size_t. Second, we need to implement the rules of integer promotion and integer
conversion defined by the C standard in order to materialize all implicit casts. Finally, owing to
historical function prototypes in the C standard library, information provided by Clang is sometimes
partial. For instance, in uint32_t* x = malloc (4 * sizeof(uint32_t)), the right-hand side has type
void* according to the C standard, instead of the expected uint32_t* pointer type.


                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:4                                                                             Aymeric Fromherz and Jonathan Protzenko


                         𝑡 ::=   uint8_t, bool, . . .                     integers, booleans. . .
                                 unit                                     empty type
                                 size_t                                   pointer size
                                 𝑡∗                                       pointer type
                                 𝑡 (𝑡®)                                   function type
                                 struct 𝑠                                 struct type
                                 (𝑡®)                                     tuple type
                                 variant 𝑣                                variant type
                                         
                         𝑑 ::=   struct 𝑠 𝑡𝑖 𝑓𝑖 ; . . . 𝑡 𝑗 𝑓 𝑗 [𝑛 𝑗 ];   struct definition
                                 variant 𝑣 𝐶𝑖 : 𝑡®𝑖                       variant definition

                         𝑒 ::=   return 𝑒, if (𝑒) then 𝑒 else 𝑒,
                                 while (𝑒) 𝑒, continue, break             control-flow
                                 𝑥 =𝑒                                     assignment
                                 let 𝑡 𝑥 (= 𝑒)? in 𝑒                      variable declaration
                                 let 𝑡 𝑥 [𝑛] (= {®  𝑒 })? in 𝑒            array declaration
                                 match 𝑒 with 𝐶𝑖 𝑣®𝑖 → 𝑒𝑖                 pattern-matching
                                 𝑥                                        variable
                                 𝑒 ⊲⊳ 𝑒 with ⊲⊳ = +, −, ×, . . .          binary operators
                                 𝑒 [𝑒]                                    array indexing
                                 𝑒.𝑓                                      field selection
                                 𝑒.𝑖                                      tuple field selection
                                 𝑓 (®𝑒)                                   function call
                                 ∗𝑒                                       dereference
                                 malloc(𝑡, 𝑒)                             typed heap allocation
                                 &𝑒                                       address-taking
                                 𝐶 𝑒®                                     variant value
                                 (𝑡)𝑒                                     cast
                                 (𝑒 1, . . . , 𝑒𝑛 )                       tuple (𝑛 > 1)
                                 ()                                       unit value
                                 𝑛:𝑡                                      typed integer constant

Fig. 2. Grammar of Mini-C types, statements and expressions. We use 𝑒 1 ; 𝑒 2 as syntactic sugar for let _ =
𝑒 1 in 𝑒 2 . Declarations are optionally initialized.




   To address these issues, we introduce a type-directed translation from C to Mini-C, where each
C statement or expression translates to a typed Mini-C expression. Our judgments are of the form
Γ ⊢ e { 𝑒 : 𝑡 to model the translation of C expression e (in bold) to Mini-C expression 𝑒 (in regular
font) of type 𝑡. The judgment is overloaded to deal with both C expressions and lists of statements,
and produces Mini-C expressions in both cases. Since types are isomorphic and no meaningful
translation takes place, there is no t (in bold) and we simply write 𝑡 (in regular font) for both C
and Mini-C. Γ is a type environment: it maps variable (and function) names to their corresponding
types. We assume a special variable ret is in Γ to account for the return type of the current function.
   We sometimes need to perform type conversion to a prescribed type 𝑡, which we write Γ ⊢
e ⊳ 𝑡 { 𝑒. This serves two purposes: one, to implement C’s implicit promotion rules (which depend
on the type expected by the context); two, to adjust types when Mini-C enforces a stronger typing
discipline than C (e.g., loop conditionals). We explain promotion and conversion in Section 2.3.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                       121:5


   When the expected type 𝑡 is unit, we omit the : unit part altogether for a more concise judgement.
In practice, our judgment also contains a flag that indicates whether we are in a value-producing
context, to compile, e.g., i++, to either 𝑖 = 𝑖 + 1 (in statement position) or let 𝑖 0 = 𝑖 in 𝑖 = 𝑖 + 1; 𝑖 0 (in
array index position) – for simplicity, we omit these verbose, but straightforward rules.
   We present selected rules for the translation in Figure 3. Because C permits type aliases via
typedef, a preliminary phase in our implementation replaces typedefs with their definitions before
applying the rules from Figure 3. For brevity, we elide this phase, along with the translation of C
types to Mini-C types, which is straightforward. Suffices to say that, again, our translation is aware
of C’s subtleties, such as how void f(int x[4]) really means void f(int *x).
   We now review a few salient rules. VarDecl introduces a new variable in the context, then
translates the remaining C statements into an expression that forms the continuation of a let-
binding; ArrayDecl is identical, except it knows about C’s array decay, meaning references to 𝑥
have a C pointer type, not an array type. Ret leverages the special binding in the environment that
holds the return type of the current function. If and While enforce that conditions be booleans.
Malloc requires that the original C code be structured as to make the type of the elements apparent
– failure to do so triggers a warning in modern compilers anyhow. The resulting Mini-C malloc
construct is structured and contains a type, along with a number of elements (not bytes). In practice,
our implementation supports more than just this particular form of malloc; we omit extra rules.

2.3    Implicit Conversions and Integer Promotion
Conversions and integer promotions complicate the semantics of C programs. They are one of the
motivating factors behind the introduction of Mini-C, before actual translation to Rust. Conversions
change the type of an expression according to the context: for instance, in the right-hand side of
an assignment (type determined by the left-hand side), or as an argument to a function call (type
determined by the function prototype) [19, 6.3].
    In our judgments, ⊳ materializes conversions that are otherwise implicit in the C standard
(Conversion); if the synthesized (bottom-up) type differs from the expected (top-down) type, a cast
is inserted (ConvertNeq), otherwise, the expression remains as-is (ConvertEq). Further conversions
occur as part of the usual arithmetic conversions [19, 6.3.1.8]. We follow the pseudo-algorithm
outlined in the C standard, and our function promote returns the types that the operands should
be promoted to, along with the corresponding return type. Because we work with fixed-width
integers, we can slightly simplify the algorithm, as we do not need to deal with types like int and
long which may have the same size but not the same rank.
    We conclude with a brief remark: our translation assumes that the C code is portable and does
not rely on C’s data model (i.e., choice of widths for particular types). In other words, we expect
the code to have the same behavior regardless of whether long is 4 or 8 bytes. Our implementation
detects at configure-time the data model for the architecture the code is running on, then uses this
information to go from, e.g., unsigned int to uint32_t.

2.4    Synthesizing High-Level Constructs
Compared to C, Mini-C also provides higher-level program constructs, such as ADTs or tuples.
While several previous works investigated the automated detection and reconstruction of such
patterns [15, 16], we instead rely on user-provided annotations on type definitions to identify structs
that must be translated to, e.g., ADTs. We believe this yields a more predictable translation, along
with a better developer experience, since we can error out when the usage of a tagged union does
not follow the expected patterns, rather than silently fail to detect it. Leveraging these annotations,
we now describe how we perform the needed semantic reconstructions to obtain valid Mini-C.

                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:6                                                                                            Aymeric Fromherz and Jonathan Protzenko


                       Ret                                                   VarDecl
                         Γ ⊢ e ⊳ Γ(ret) { 𝑒                                  Γ⊢e ⊳ 𝑡 {𝑒                  Γ, 𝑥 : 𝑡 ⊢ ®s { 𝑒 2
                        Γ ⊢ return e { return 𝑒                                 Γ ⊢ t 𝑥 = e; ®s { let 𝑡 𝑥 = 𝑒 in 𝑒 2

                ArrayDecl                                                                    Seq
                  Γ ⊢ e𝑖 ⊳ 𝑡 { 𝑒𝑖                  Γ, 𝑥 : 𝑡∗ ⊢ ®s { 𝑒 2                      Γ ⊢ s { 𝑒1                Γ ′ ⊢ ®s { 𝑒 2
                Γ ⊢ t 𝑥 [𝑛] = {®e} ; ®s { let 𝑡 𝑥 [𝑛] = {®
                                                         𝑒 } in 𝑒 2                                   Γ ⊢ s; ®s { 𝑒 1 ; 𝑒 2

        If                                                                                   While
         Γ ⊢ e ⊳ bool { 𝑒                 Γ ⊢ s®1 { 𝑒 1         Γ ⊢ s®2 { 𝑒 2                Γ ⊢ e ⊳ bool { 𝑒 1                     Γ ⊢ ®s { 𝑒 2
          Γ ⊢ if (e) then s®1 else s®2 { if (𝑒) then 𝑒 1 else 𝑒 2                              Γ ⊢ while (e) ®s { while (𝑒 1 ) 𝑒 2

                     Assign                                        AddrOf                                   Deref
                      Γ ⊢ e ⊳ Γ(𝑥) { 𝑒                              Γ ⊢e{𝑒 :𝑡                                Γ ⊢ e { 𝑒 : 𝑡∗
                     Γ ⊢𝑥 =e {𝑥 =𝑒                                 Γ ⊢ &e { 𝑒 : 𝑡∗                           Γ ⊢ ∗e { ∗𝑒 : 𝑡

        Malloc                                                                    Index
                           Γ ⊢ e ⊳ size_t { 𝑒                                      Γ ⊢ e1 { 𝑒 1 : 𝑡∗              Γ ⊢ e2 ⊳ size_t { 𝑒 2
        Γ ⊢ malloc(e × sizeof (t)) { malloc(𝑡, 𝑒) : 𝑡∗                                             e1 [e2 ] { 𝑒 1 [𝑒 2 ] : 𝑡

                        PointerAdd
                        Γ ⊢ e1 { 𝑒 1 : 𝑡∗              Γ ⊢ e2 ⊳ size_t { 𝑒 2                           Var
                                                                                                       Γ ⊢ 𝑥 { 𝑥 : Γ(𝑥)
                                       Γ ⊢ e1 + e2 { 𝑒 1 + 𝑒 2 : 𝑡∗

   Call                                                                                                   Conversion
   Γ(𝑓 ) = 𝑡 ret (𝑡 1, . . . , 𝑡𝑛 )        Γ ⊢ e𝑖 ⊳ 𝑡𝑖 { 𝑒𝑖               Constant                              Γ ⊢ e { 𝑒 : 𝑡1
                                                                          Γ ⊢𝑛 :𝑡 {𝑛 :𝑡
          Γ ⊢ 𝑓 (e1, . . . , e𝑛 ) { 𝑓 (𝑒 1, . . . , 𝑒𝑛 )                                                   Γ ⊢ e ⊳ 𝑡 2 { convert(𝑒, 𝑡 1, 𝑡 2 )

                                                                                   ConvertNeq
                                      ConvertEq                                          𝑡 ≠ 𝑡′
                                      convert(𝑒, 𝑡, 𝑡) = 𝑒
                                                                                    convert(𝑒, 𝑡, 𝑡 ′ ) = (𝑡 ′ )𝑒

                        BinOp
                        Γ ⊢ e1 { 𝑒 1 : 𝑡 1             Γ ⊢ e2 { 𝑒 2 : 𝑡 2         (𝑡 1′ , 𝑡 2′ , 𝑡 ret ) = promote(⊲⊳, 𝑡 1, 𝑡 2 )
                                      Γ ⊢ e1 ⊲⊳ e2 { convert(𝑒 1, 𝑡 1, 𝑡 1′ ) ⊲⊳ convert(𝑒 2, 𝑡 2, 𝑡 2′ ) : 𝑡 ret

                                         Fig. 3. Translation from C to Mini-C, Selected Rules




   Tagged unions and ADTs. While the C language does not provide support for abstract data types,
a common pattern is to emulate them through the use of tagged unions. A tagged union is a struct
type that combines a union type, representing the payload of the structure, with a tag, commonly
represented as an integer, which tracks the current state of the union. Concretely, we consider
tagged unions of the shape { int tag; union { t0 case0; ...; tn caseN }}, and assume that the tag
ranges from 0 to N, and that tag values match the order of the union cases. We show an example of
our handling of tagged unions in Figure 4. For brevity, we omit the corresponding formal rules; in
practice, we carry a supplemental set of flow-sensitive equations (to keep track of tag values at a
given program point), and a supplemental set of tag mappings (to keep track of the correspondence
between tag values and C union cases).

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                       121:7

    1     #define CaseU8 0
    2     #define CaseU16 1
    3
    4     typedef struct
    5     __attribute__((annotate("scylla_adt")))
                                                              1    variant cases
    6     cases_s {
                                                              2      | case_uint8 (v: uint8_t)
    7       uint8_t tag;
                                                              3      | case_uint16 (v: uint16_t)
    8       union {
                                                              4
    9         uint8_t case_uint8;
                                                              5    unit f(cases s) {
10            uint16_t case_uint16;
                                                              6      match s with
11          };
                                                              7      | case_uint8 v -> let uint8_t x = v in ()
12        } cases;
                                                              8      | _ -> ()
13
                                                              9    }
14        void f(cases s) {
15          if (s.tag == CaseU8) {
16            uint8_t x = s.case_uint8;
17          }
18        }

                  Fig. 4. Example of tagged union translation from C (left) to Mini-C (right)

         cases s = {                                                  if (s.tag == CaseU8) {
           .tag = CaseU8, { .case_uint16 = 0 }                          uint16_t x = s.case_uint16;
         };                                                           } // Accessed payload does not match
         // Payload does not match the tag                            // the current union state

           Fig. 5. Examples of invalid usages of tagged unions, that will not be translated to Mini-C


   When annotated with the appropriate attribute (line 5, left), our tool translates this type definition
to a variant type with constructors Case0 t0, ..., CaseN tn (line 1-3, right). Creating a tagged union
value is straightforward: when translating a value {.tag = i, .casej = e }, we first, as a sanity-check,
ensure that the .casej field corresponds to the 𝑖-th constructor. If so, we translate expression 𝑒 with
type 𝑡 𝑗 to Mini-C expression 𝑒 ′ , and generate the value 𝐶 𝑗 𝑒 ′ .
   Translating accesses to a tagged union requires a bit more bookkeeping. To safely access field
casei of a tagged union variable 𝑥, it is necessary to know that the tag of 𝑥 is currently equal to 𝑖. This
is commonly checked through a conditional branching of the shape if (x.tag == i) { ... x.casei },
or a switch, as is shown on line 15 of our example. We therefore recognize these code patterns, and
translate them to standard pattern-matching match x with | Ci v -> .... We store and propagate
the state of tagged union 𝑥, and translate all occurrences of x.casei to the constructor payload 𝑣
inside the branch (line 7, right); accesses to different union cases are considered invalid and the
translation errors out.
   Tuples. Similarly to ADTs, we also offer attributes to translate annotated types to tuples. A
struct type with 𝑛 fields 𝑡𝑖 𝑥𝑖 translates to an n-ary tuple (𝑡 1, . . . , 𝑡𝑛 ); as part of the translation, we
keep track of which types are tuple types, and translate corresponding field accesses to tuple field
accesses at the appropriate index. This is useful for both code quality, and accepting a greater subset
of programs: because tuples are typed structurally, they benefit from mut-polymorphism, while
structs do not – we say more in §3.3.

3       Generating Safe Rust Code
Mini-C provides us with an explicit, entirely type-annotated representation of C programs. We
now show how to translate Mini-C programs to safe Rust. The chief difficulties are: compiling

                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:8                                                                      Aymeric Fromherz and Jonathan Protzenko


away C’s pointer arithmetic (Section 3.2), making mutability and aliasing explicit (Section 3.3), and
automatically providing idiomatic Rust constructs such as traits (Section 3.4).

3.1     Base Translation and Pointer Representation
We begin with the translation of Mini-C types to Rust types. The difficulty lies in translating pointer
types, because Rust differentiates between Box<T> (owned pointer to a heap-allocated T) and &T
(un-owned pointer, a.k.a. borrow). Furthermore, unlike C, Rust distinguishes between a pointer to
a single element (e.g. &T) and a pointer to multiple elements (e.g. &[T]). Finally, arrays in Rust are
values, and do not decay to pointers automatically – they must be explicitly converted.
   We adopt the following strategy. By default, every pointer type in C, be it to the stack or to
the heap, to a single element or to multiple elements, compiles to a slice borrow &[T] (we infer
mutability automatically in Section 3.3 and therefore ignore the mut qualifier for now). Concretely,
uint8_t x; uint8_t *y = &x; generates let y: &[u8] ... in Rust, and not &u8.
   Additionally, we provide heuristics as well as manual annotations to guide the translation towards
Box<T> instead of &[T] when judicious. Our tool performs a limited analysis, and can conclude that
a function T *create() that does not contain references to globals must be allocating a fresh T,
and therefore translates it to fn create() -> Box<T>. This analysis recurses (using a fixed-point
computation) within struct and variant definitions, to determine whether a pointer field becomes a
Box, or a borrow – the latter makes the struct parameterized over a lifetime.
   A consequence of this design choice is that our translation must be type-directed, in order to
insert coercions between arrays and slice borrows (since the former do not decay automatically in
Rust); and to reconcile between those two and instances of Box<T> introduced by either the user or
our heuristics. We omit the full syntax of Rust, for brevity, and instead focus on the salient parts of
our translation in Figure 6.
   Our rules have the form Γ ⊢ 𝑒 ⊳ 𝑇 ⇝ 𝐸 ⊣ Γ ′ , meaning that in Rust typing environment Γ, the
translation of Mini-C expression 𝑒 with expected Rust type 𝑇 yields Rust expression 𝐸 and an
updated Rust typing environment Γ ′ . The output environment serves to invalidate variables that
should no longer be used (we explain below). We use 𝑡 ↩→ 𝑇 to translate types from Mini-C to Rust.
   Coercions appear in E-Array-Slice, which introduces a borrow, thus turning the array into a
slice borrow; and in E-Box-Slice, which operates identically, but for boxed slices. Rules E-Slice-Box
and E-Array-Box are “reverse conversions”, which convert stack and unknown allocations into
heap ones. Finally, E-Var models the simple case where a variable does have the expected type. In
practice, some of the syntax introduced by the conversion rules is unnecessary, as the Rust compiler
is able to add auto-borrows and auto-derefs in many places. Our implementation is aware of this,
and features a nano-pass at the very end that removes superfluous &s and ∗s.
   The coercions introduced by conversion rules can however lead to subtle semantic differences,
specifically, those introduced for the “reverse conversions” E-Slice-Box and E-Array-Box. Consider
for instance the following (simplified) Rust program, where y must be translated as a Box<[T]>,
meaning the array 𝑥 is coerced to a boxed slice. In this program, the assertion does not hold, as the
call to Box::new creates a copy of x. In a C program however (left), both x and y would be the same
pointer, therefore the change to y on line 3 would also apply to x. (Generally, constructors that take
another data structure, or explicit conversions performed via .into() in Rust generate a copy.)
uint8_t x[1] = {0};                                        let x: [u8; 1] = [0; 1];
uint8_t *y = x;                                            let mut y: Box<[u8]> = Box::new(x);
*y = 1;                                                    y[0] = 1;
assert(*x == 1);                                           assert!(x[0] == 1)
   These copies cannot be avoided, as in our translation scheme, it might truly be the case that what
initially started as a stack allocation needs to be promoted to a heap allocation. Furthermore, Rust

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                             121:9


provides no way of “opting out” of the Copy trait for base types like arrays of integers, meaning that
Rust will silently perform a copy of 𝑥 into 𝑦, while allowing further modifications to 𝑥. We therefore
leverage our output environment Γ ′ and strip the original variables from Γ when performing the
conversion, thus forbidding any further usage of 𝑥. If the original C program further relies on x,
our translation will error out, and will ask the programmer to fix their source code. This is another
area where we adopt a “semi-active” approach, and declare that some patterns are poor enough,
even for C, that they ought to be touched up before the translation takes place.

           E-Index                                                                       E-Deref
           Γ ⊢ 𝑒 1 ⊳ &[𝑇 ] ⇝ 𝐸 1 ⊣ Γ ′        Γ ′ ⊢ 𝑒 2 ⊳ usize ⇝ 𝐸 2 ⊣ Γ ′′             Γ ⊢ 𝑒 ⊳ &[𝑇 ] ⇝ 𝐸 ⊣ Γ ′
                         Γ ⊢ 𝑒 1 [𝑒 2 ] ⊳ 𝑇 ⇝ 𝐸 1 [𝐸 2 ] ⊣ Γ ′′                           Γ ⊢ ∗𝑒 ⊳ 𝑇 ⇝ 𝐸 [0] ⊣ Γ ′

                                                          E-Stack
                  E-Var                                       𝑡 ↩→ 𝑇         Γ𝑖 ⊢ 𝑒𝑖 ⊳ 𝑇 ⇝ 𝐸𝑖 ⊣ Γ𝑖+1
                      𝑥 :𝑇 ∈ Γ                                 Γ𝑁 , 𝑥 : [𝑇 ; 𝑁 ] ⊢ 𝑒 ′ ⊳ 𝑇 ′ ⇝ 𝐸 ′ ⊣ Γ
                   Γ ⊢ 𝑥 ⊳𝑇 ⇝ 𝑥 ⊣ Γ                          Γ0 ⊢    let 𝑡 𝑥 [𝑁 ] = {®𝑒 } in 𝑒 ′ ⊳ 𝑇 ′
                                                              ⇝                            ® 𝐸 ′ ⊣ Γ \ {𝑥 }
                                                                     let 𝑥 : [𝑇 ; 𝑁 ] = [𝐸];

  E-Heap
                                       𝑡 ↩→ 𝑇                                                    E-Box-Slice
                        Γ, 𝑥 : Box⟨[𝑇 ]⟩ ⊢ 𝑒 ′ ⊳ 𝑇 ′ ⇝ 𝐸 ′ ⊣ Γ ′                                    𝑥 : Box⟨[𝑇 ]⟩ ∈ Γ
      Γ⊢    let 𝑡 ∗𝑥 = malloc(𝑡, 𝑁 ) in 𝑒 ′ ⊳ 𝑇 ′                                                Γ ⊢ 𝑥 ⊳ &[𝑇 ] ⇝ &𝑥 ⊣ Γ
      ⇝     let 𝑥 : Box⟨[𝑇 ]⟩ = vec![0; 𝑁 ].into_boxed_slice(); 𝐸 ′ ⊣ Γ ′ \ {𝑥 }

                 E-Array-Slice                                      E-Slice-Box
                      𝑥 : [𝑇 ; 𝑁 ] ∈ Γ                                 𝑥 : &[𝑇 ] ∈ Γ        Γ ′ = Γ \ {𝑥 }
                  Γ ⊢ 𝑥 ⊳ &[𝑇 ] ⇝ &𝑥 [..] ⊣ Γ                       Γ ⊢ 𝑥 ⊳ Box⟨[𝑇 ]⟩ ⇝ (∗𝑥).into() ⊣ Γ ′

                E-Array-Box                                                     E-AddrOf
                   𝑥 : [𝑇 ; 𝑁 ] ∈ Γ         Γ ′ = Γ \ {𝑥 }                       Γ ⊢ 𝑒 ⊳ [𝑇 ; 𝑁 ] ⇝ 𝐸 ⊣ Γ ′
                 Γ ⊢ 𝑥 ⊳ Box⟨[𝑇 ]⟩ ⇝ Box :: new(𝑥) ⊣ Γ ′                        Γ ⊢ &𝑒 ⊳ &[𝑇 ] ⇝ &𝐸 ⊣ Γ ′

                                     E-Call
                                     𝑓 : (𝑇®) → 𝑇 ∈ Γ         Γ𝑖 ⊢ 𝑒𝑖 ⊳ 𝑇𝑖 ⇝ 𝐸𝑖 ⊣ Γ𝑖+1
                                              Γ𝑛 , 𝑟 : 𝑇 ⊢ 𝑟 ⊳ 𝑇 ′ ⇝ 𝐸 ′ ⊣ Γ ′
                                             𝑒 ) ⊳ 𝑇 ′ ⇝ let 𝑟 = 𝑓 ( 𝐸);
                                     Γ0 ⊢ 𝑓 (®                       ® 𝐸 ′ ⊣ Γ ′ \ {𝑟 }


                              Fig. 6. Translation from Mini-C to Rust, Selected Rules



3.2    Compiling Pointer Arithmetic
We now reach the main difficulty of the translation, namely, handling pointer arithmetic. When
operating on arrays, C programs rarely perform accesses and updates via a single base pointer. A
common pattern is to instead divide the array into chunks, or iterate over the array elements by
keeping a local pointer to the current head of the iterator.
   Consider the following C example (Figure 7, left), inspired by an implementation of elliptic-curve
cryptography. The array abcd contains a large number (“bignum”), spread across four 64-bit (8 bytes)
limbs stored contiguously in memory. For field addition, a first order of business is to get pointers
to individual limbs, before performing pointwise addition. In other words, we want to perform

                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:10                                                                     Aymeric Fromherz and Jonathan Protzenko

  1      uint8_t abcd[32] = { 0 };                          1    let mut abcd = [0u8; 32];
  2                                                         2    let abcd: &mut [u8] = &mut abcd[..];
  3      uint8_t *a = abcd + 0;                             3    let (a_l, a_r) = abcd.split_at_mut(0);
  4      uint8_t *c = abcd + 16;                            4    let (c_l, c_r) = a_r.split_at_mut(16);
  5      uint8_t *b = abcd + 8;                             5    let (b_l, b_r) = c_l.split_at_mut(8);
  6      uint8_t *d = abcd + 24;                            6    let (d_l, d_r) = c_r.split_at_mut(8);
  7                                                         7    let (a, b, c, d) = (b_l, b_r, d_l, d_r)

Fig. 7. Example of pointer arithmetic translation as Rust splits. For readability, we destructure tuples instead
of using tuple variables and accessors as described in Figure 8.


pointer arithmetic to access chunks a, b, c, d, spanning intervals [0; 8), [8; 16), [16; 24) and [24; 32)
of the base pointer. Because C does not carry length information for pointers, neither at run-time
nor in the type system, we do not know that each pointer intends to span 8 bytes. Furthermore, we
cannot assume either that pointer arithmetic occurs in left-to-right order: Figure 7 illustrates this.
   This bit of C code cannot be trivially translated to Rust, because in order to guarantee memory
safety, Rust does not allow arbitrary pointer arithmetic. What Rust provides instead is a primitive
named split_at_mut (or split_at for immutable slices), which allows the programmer to relinquish
ownership of a slice, and obtain in exchange two sub slices that split the original slice at the
given index. This permits some restricted notion of pointer arithmetic, while preserving Rust’s
invariant that mutable data should have a unique owner: to regain ownership of the original slice,
the programmer must give up the sub slices. To reconcile C’s pointer arithmetic with Rust’s splitting
paradigm, we therefore propose a novel notion of split trees.
   Split Trees. Our compilation algorithm is described in Figure 8; we use Figure 7 as a supporting
example to illustrate how it works. When translating C’s pointer arithmetic to Rust, several
difficulties arise. First, because we do not have length information coming from the C side, we
need to assume that the chunks are not intended to be overlapping – if they were, this code would
simply be impossible to type-check, and the programmer would have to rewrite their C code to
make the intent more apparent, keeping in line with our semi-active approach to translating C
to Rust. Second, the translation needs to be predictable and understandable by the user, so that
translation failures can easily be matched with the location in the original C code that needs to be
rewritten. For those reasons, we want to avoid backtracking in our translation, and perform the
translation in a forward fashion. This means that we need a data structure that keeps the history of
the calls to split_at, for instance to know at line 5 that C index 8 lives in c_l, and at line 6 that C
index 24 lives in c_r, at Rust index 24 − 16 = 8. This data structure also must be attached to every
program point, so as to translate an access through a C pointer into an access (possibly with an
offset computation) through a Rust slice. For instance, a[0] would translate into a_r[0] after line 3,
but into c_l[0] after line 4, and so on.
   We solve these challenges with a data structure called a split tree, synthesized during our
translation: each C pointer maps to a (possibly singleton) split tree, which evolves in a flow-
dependent fashion. We present the split trees corresponding to abcd at different points of our
translation in Figure 9; the split tree initially only contains the root abcd.
   The first pointer addition defines a as a sub-array of abcd starting at index 0, whose intended
length is unknown. We thus split abcd at index 0, and keep this information, meaning indices
[0; 0) of abcd are in the left slice, a_l, and indices [0; 32) are in a_r (Figure 9a). The second pointer
addition on the same base pointer abcd triggers another split. At this program point, abcd is no longer
available, because it has been borrowed to construct (a_l, a_r). Splitting abcd directly would be a
mistake, because it would terminate these borrows, and render (a_l, a_r) unusable, thus making it

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                       121:11


  ⊲ When a new variable x enters the scope other than through let x = base + index (function parameter,
    stack or heap allocations, etc.): update environment                                                ⊳
  procedure init(x)
      Tree(x) ← Leaf
      Base(x) ← None
      Path(x) ← []
  ⊲ When compiling let x = base + index:                                                                                ⊳
  function new-split(x, base, index)
     ⊲ Locate the position where we need to split in the binary search tree for base                                    ⊳
     path, node ← Binary-Search(Tree(base), index)
     ⊲ Extend the split tree of base: a new sub-child is added to node.                                                 ⊳
     if index < node.index then
         suffix ← Left
     else
         suffix ← Right
     Tree(base)[node].suffix ← Node(index, Leaf, Leaf)
     ⊲ Fill out the environment:                                                                                        ⊳
     Tree(x) ← Leaf                                                                         ⊲ x itself has not been split
     Base(x) ← Some base                   ⊲ x now holds a sub-range of base, described in the split tree of base...
     Path(x) ← path ++ [ suffix ]                    ⊲ ... by the node found at the end of path, followed by suffix
     ⊲ To produce syntax for x, we need y, the variable in scope for its parent node. Note that y has a pair type. ⊳
     y ← find y in scope such that Base(y) = Some base and Path(y) = path
     ⊲ Moving right requires subtractions – see e.g. c_r in Figure 9c. We encapsulate this in Compute (elided) ⊳
     offset ← compute(Tree(base), path, index)
     ⊲ Return a Rust expression. field-of-suffix is 0 for Left, 1 for Right – this is Rust syntax for pair projections. ⊳
     return let x = y.field-of-suffix(suffix).split_at(offset);                             ⊲ Note that x is now a pair.
  ⊲ When compiling x (reference to variable x)                                                                 ⊳
  function var-lookup(x)
     if Base(x) = None then
         return x                  ⊲ This variable has not been subjected to splits – trivial compilation scheme
     else if Base(x) = Some base then
         y, suffix ← find nearest y, suffix in scope such that
                     Base(y) = base and Path(x) is-accessible-via Path(y) = Some suffix
         return y.field-of-suffix(suffix)
  function is-accessible-via(p1, p2)
     if p2 = p1 then
         ⊲ If no further split occurred, elements of interest are on the right                                          ⊳
         return Some Right                                                  ⊲ e.g., a is accessible via a_r in Figure 9a
     else if exists n >= 0 such that p2 = p1 ++ [ Right ] ++ repeat(Left, n) then
         ⊲ If a split occurred, move right (to get the elements of interest), then keep left (to avoid other variables) ⊳
         return Some Left                      ⊲ e.g., a is accessible via c_r in Figure 9b, and via d_l in Figure 9c
     else
         return None

 Fig. 8. An algorithm for reconstructing pointer arithmetic using split trees; [] is syntax for the empty list.


impossible to translate any further usage of C pointer a. Instead, we leverage the fact that our split
tree is a binary search tree, and discover that key 16 needs to be inserted as the right child of node
a, i.e., we must split a_r at index 16. At this stage, a use of C pointer a would trigger a search in the
binary tree, and would return c_l as the current slice through which a may be accessed (Figure 9b).

                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:12                                                                      Aymeric Fromherz and Jonathan Protzenko


                                                                           (abcd, 0)

                                         (abcd, 0)                a_l                   (a_r, 16)

                 (abcd, 0)         a_l         (a_r, 16)                        (c_l, 8)        (c_r, 8)

           a_l               a_r             c_l        c_r                   b_l      b_r    d_l       d_r
         (a) After translating a   (b) After translating c              (c) After translating b and d

Fig. 9. Successive split trees during C translation. Internal nodes of the form (x, i) have been subjected to a
split at Rust index i and are therefore borrowed at this program point. Leaf nodes are available.


The translation of b is similar. Finally, for d, we find that index 24 is to be found in c_r; because the
indices of the right subslice restart from 0, we must perform a subtraction to know that c_r needs
to be split at index 8 (Figure 9c).
   We generalize this mechanism to all variables in the environment, and equip it with a few more
bells and whistles (not depicted in Figure 8). First, any usage of abcd that is not pointer arithmetic
(e.g., f(abcd)) is taken to indicate that C variables a, b, c, and d are no longer useful and that the user
intends to perform a fresh set of pointer arithmetic computations. This allows the programmer to
insert, in the source code, calls to, e.g., (void)abcd to provide a hint that the split tree of abcd needs to
be reset, and that the corresponding Rust variables can go out of scope (i.e., their lifetimes can end).
Such calls are optimized away by the compiler, and therefore do not have any impact at runtime.
We leveraged this mechanism in numerous places in our HACL★ case study (Section 4.2.3). For
instance, in elliptic curve implementations, it is common to have a function be a series of calls to
ADD and MUL macros, each of which expands to operations that need their own split trees. Second, we
generalize the form of offsets to accept a more general language of expressions, described below.
   Symbolic Solver. The split trees we presented above operate over constant offsets – this allows
implementing a trivial order, which is required for the binary search tree structure. In real-world
examples, we commonly encountered more complex offset expressions, for instance n and n + 8
where n might be a parameter of the current function, whose value is therefore not statically known.
   To address this issue, our implementation relies on a simple, deterministic symbolic solver,
which is able to compare different kinds of arithmetic expressions containing symbolic variables,
e.g., to determine that n + 8 is greater than n. While this solver is not complete and does not rely
on contextual information to refine the analysis, it is sufficient to translate large case studies as
described in Section 4, and could be easily extended for further use-cases.
   Should the symbolic solver still fail to compare offsets, our implementation emits a warning,
along with the corresponding location. This allowed us to fix the source code in our case studies,
for instance, to replace 2*n with n+n. Should none of this work, our compiler then adopts a final
heuristic: that the offsets that occur along the control-flow are monotonically increasing, i.e., they
perform pointer arithmetic from left to right. Again, our semi-active translation approach means
that, in case the programmer’s intent is unclear, it is oftentimes worthwhile to rewrite the source,
rather than augment our solver with complex heuristics.
  Limitations. We now comment on this approach. If there is true aliasing, i.e., the C program
contains both a[8] and b[0] in our earlier example, the translated Rust code will perform an out-
of-bounds array access. In other words, we must assume the array chunks, in C, to be disjoint.
For overlap cases that can be distinguished statically (as above), we emit a compile-time error;

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                     121:13


otherwise, the Rust code will panic at runtime. We remark that we have not seen this pattern in
our case studies, so this has not been a problem in our experience. Should this turn out to be a
concern in the future, we envision either supplemental off-the-shelf static analyses to determine
slice lengths, or additional annotations in the source code to express intent more clearly.


3.3    Mutability Inference
To ensure memory safety, Rust relies on a principle called mutability XOR aliasing. Concretely, it
distinguishes between immutable borrows, of type &T, which can be freely shared and duplicated
but only allow to read the referenced memory, and mutable borrows, of type &mut T, which allow to
write memory, but require exclusive ownership, that is, no other reference to the same memory
region can be live at the same time. This is enforced by the Rust borrow-checker.
   The distinction between mutable and immutable borrows raises two conflicting problems. To
pass borrow-checking, one needs to provide mutability annotations, to ensure that memory being
modified is indeed mutably borrowed. Unfortunately, marking all borrows as mutable is not a
solution. Beyond being unidiomatic, a function requiring only mutable borrows is also restrictive,
as it prevents usages where aliasing would be safe, i.e., when arguments are only read.
   To reach a middle ground, our Rust translation generates immutable borrows by default, which
we now refine as-needed into mutable borrows through a custom mutability inference analysis. To
do so, we perform a backward analysis on all translated functions, identifying expressions that
perform memory updates, and backpropagating which program variables need to be mutable back
to their definition site, inserting mutable borrows along the way.
   Mutability rules are as follows in Rust. If x has array type [T; N] and x[i] = e occurs, then x must
be a mutable variable, i.e., declared as let mut x = .... If y has borrow type and y[i] = e occurs,
then y must be a mutable borrow; furthermore, one can only mutably borrow variables that are
themselves mutable, i.e., if let y: &mut [u8] = &mut z, then z itself must be declared as let mut z.
   We inductively define an analysis on the Rust syntax that is aware of the semantics above and
synthesizes two variable sets 𝑉 and 𝑅, where 𝑉 contains variables that must be mutable (i.e., x and
z, above), and 𝑅 contains variables that must have a mutable borrow type (i.e., y above). Applying
this analysis to the output of our translation yields a Rust program that has been annotated with
the minimum amount of mut qualifiers in variables, types, and function parameters, in order to type-
check. In practice, our analysis is more general, and can handle many more forms of assignments,
with combinations of fields, borrows, array indexing, and so on. Our implementation also computes
a third set 𝐹 , for fields of structs that ought to be mutable, and a fourth set 𝑃, for pattern variables
in matches that ought to be ref mut – we omit these details here for the sake of simplicity.
   We formally present our mutability inference analysis in Figure 10. Our rules are presented as the
                                          𝑉 ,𝑅
combination of a judgment Δ ⊢ 𝑒 ⇒ 𝑒 ′, 𝑉 ′, 𝑅 ′ , and a system of mutually-recursive equations over
                                          𝑀
Δ. The final output of our analysis is the least fixed point that satisfies the equations over Δ. The
𝑉 ,𝑅
⇒ judgment represents that Rust expression 𝑒 is transformed into expression 𝑒 ′ . This translation is
𝑀
performed with current sets 𝑉 , 𝑅, and returns new sets 𝑉 ′ and 𝑅 ′ , as the translation of 𝑒 might have
added variables to both sets. The mode 𝑀 ∈ {𝑚𝑢𝑡, 𝑖𝑚𝑚} indicates the expected borrow mutability
of the expression 𝑒, while Δ contains the function definitions, which are needed to retrieve the
expected mutability when performing function calls.
   Rules I-ImmVar and I-MutVar are straightforward: if the translation expects variable 𝑥 to be a
mutable borrow, then we add it to the set 𝑅 to backpropagate the information, otherwise, we
leave both sets invariant. Rules I-ImmBorrow and I-MutBorrow are similar, but operate directly on


                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:14                                                                                             Aymeric Fromherz and Jonathan Protzenko


I-ImmVar                     I-MutVar                                    I-ImmBorrow                          I-MutBorrow
         𝑉 ,𝑅                         𝑉 ,𝑅                                           𝑉 ,𝑅                                   𝑉 ,𝑅
Δ ⊢ 𝑥 ⇒ 𝑥, 𝑉 , 𝑅             Δ ⊢ 𝑥 ⇒ 𝑥, 𝑉 , 𝑅 ∪ {𝑥 }                     Δ ⊢ &𝑥 ⇒ &𝑥, 𝑉 , 𝑅                   Δ ⊢ &𝑥 ⇒ &𝑚𝑢𝑡 𝑥, 𝑉 ∪ {𝑥 }, 𝑅
         𝑖𝑚𝑚                          𝑚𝑢𝑡                                           𝑖𝑚𝑚                                     𝑚𝑢𝑡

    I-Let
                                                                            𝑉 ,𝑅
                                                             Δ ⊢ 𝑒 2 ⇒ 𝑒 2′ , 𝑉 ′, 𝑅 ′
                                                                            𝑀
                                                                                                                                   𝑉 ′ ,𝑅 ′
    𝑀 ′ = if (𝑥 ∈ 𝑅 ′ ) then 𝑚𝑢𝑡 else 𝑖𝑚𝑚                     𝐴 = if (𝑥 ∈ 𝑉 ′ ) then 𝑚𝑢𝑡 else ∅                         Δ ⊢ 𝑒 1 ⇒′ 𝑒 1′ , 𝑉 ′′, 𝑅 ′′
                                                                                                                                    𝑀
                                                                      𝑉 ,𝑅
                                             Δ ⊢ let 𝑥 = 𝑒 1 ; 𝑒 2 ⇒ let 𝐴 𝑥 = 𝑒 1′ ; 𝑒 2′ , 𝑉 ′′, 𝑅 ′′
                                                                   𝑀

                    I-Update-Borrow
                              𝑉 ,𝑅                                    𝑉 ,𝑅                                   𝑉 ,𝑅
                    Δ ⊢ 𝑒 1 ⇒ 𝑒 1′ , 𝑉 ′, 𝑅 ′             Δ ⊢ 𝑒 2 ⇒ 𝑒 2′ , 𝑉 ′′, 𝑅 ′′             Δ ⊢ 𝑒 3 ⇒ 𝑒 3′ , 𝑉 ′′′, 𝑅 ′′′
                              𝑚𝑢𝑡                                    𝑖𝑚𝑚                                     𝑖𝑚𝑚
                                                     𝑉 ,𝑅
                             Δ ⊢ 𝑒 1 [𝑒 2 ] = 𝑒 3 ⇒ 𝑒 1′ [𝑒 2′ ] = 𝑒 3′ , 𝑉 ′ ∪ 𝑉 ′′ ∪ 𝑉 ′′′, 𝑅 ′ ∪ 𝑅 ′′ ∪ 𝑅 ′′′
                                                      𝑀

                I-Call
                                                    Δ(𝑓 ) = (𝑥 1 : 𝑇1, . . . 𝑥𝑛 : 𝑇𝑛 ) → 𝑇
                                      𝑉 ,𝑅
                ∀𝑖, Δ ⊢ 𝑒𝑖             ⇒              𝑒𝑖′, 𝑉𝑖 , 𝑅𝑖           𝑇 ′ = if 𝑀 = 𝑚𝑢𝑡 then 𝑚𝑎𝑘𝑒_𝑚𝑢𝑡 (𝑇 ) else 𝑇
                             𝑖𝑠_𝑚𝑢𝑡𝑏𝑜𝑟𝑟𝑜𝑤 (𝑇𝑖 )
                                                                     𝑉 ,𝑅                     Ø          Ø
                                        Δ ⊢ 𝑓 (𝑒 1, . . . , 𝑒𝑛 ) ⇒ 𝑓 (𝑒 1′ , . . . , 𝑒𝑛′ ),       𝑉𝑖 ,       𝑅𝑖
                                                                     𝑀
                                                                                              𝑖          𝑖
                                                    Δ(𝑓 ) = (𝑥 1 : 𝑇1, . . . 𝑥𝑛 : 𝑇𝑛 ) → 𝑇 ′

            I-Sig
                                                                                                  ∅,𝑅
                          𝑅 = {𝑥𝑖 | 𝑖𝑠_𝑚𝑢𝑡𝑏𝑜𝑟𝑟𝑜𝑤 (𝑇𝑖 )}                            Δ⊢𝑒            ⇒               𝑒 ′, 𝑉 ′, 𝑅 ′
                                                                                         𝑖𝑠_𝑚𝑢𝑡𝑏𝑜𝑟𝑟𝑜𝑤 (𝑇 )
            ∀𝑖,𝑇𝑖′ = if (𝑥𝑖 ∈ 𝑅 ′ ) then 𝑚𝑎𝑘𝑒_𝑚𝑢𝑡 (𝑇𝑖 ) else 𝑇𝑖                          Δ(𝑓 ) = (𝑥 1 : 𝑇1, . . . , 𝑥𝑛 : 𝑇𝑛 ) → 𝑇 {𝑒}
                                                 Δ(𝑓 ) = (𝑥 1 : 𝑇1′, . . . , 𝑥𝑛 : 𝑇𝑛′ ) → 𝑇 {𝑒 ′ }

                                     Fig. 10. Mutability Inference Analysis, Selected Rules


borrows: if variable 𝑥 is borrowed and the expected type is a mutable borrow, then we replace the
immutable borrow by a mutable borrow, and indicate that variable 𝑥 must be mutable.
   Rule I-Let demonstrates the backward nature of the analysis. As the type of the expression
corresponds to the type of 𝑒 2 , we first translate 𝑒 2 with the same mode 𝑀, returning new sets 𝑉 ′
and 𝑅 ′ . We then rely on these sets to translate 𝑒 1 . If 𝑥 belongs to 𝑅 ′ , then it means that the rest
of the program expects it to have a borrow type, we thus translate its definition with mode 𝑚𝑢𝑡.
Finally, if 𝑥 is used mutably, i.e., belongs to 𝑉 ′ , we make its let-binding mut.
   Rule I-Update-Borrow presents the translation of a borrowed slice update, which introduces
the need for mutable borrows. Our translation from C to Mini-C guarantees that the left-hand
side has a pointer type (Index) which is then translated to a Rust slice borrow type. To satisfy the
borrow-checker, the expression 𝑒 1 being modified must thus become a mutable slice borrow. We
therefore translate with the 𝑚𝑢𝑡 mode. Conversely, both the index and the value being stored are
only read; they are translated with mode 𝑖𝑚𝑚.
   The translation of function calls is handled through rule I-Call. When calling a function 𝑓 , we
first retrieve the type signature of 𝑓 from the environment Δ. We then translate the expressions
corresponding to each function argument according to their expected mutability, computed through

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                     121:15


the function 𝑖𝑠_𝑚𝑢𝑡𝑏𝑜𝑟𝑟𝑜𝑤 (𝑇𝑖 ). This function returns 𝑚𝑢𝑡 if 𝑇𝑖 is of the shape &mut T, and 𝑖𝑚𝑚 in
all other cases. The translation of all arguments can be done in parallel with the initial sets 𝑉 , 𝑅.
To propagate the information acquired, we finally return the union of these sets; this faithfully
models that if an expression 𝑒𝑖 requires a variable 𝑥 to be mutable while 𝑒 𝑗 does not have this
requirement, then 𝑥 must indeed be mutable. A key feature of this rule is that it may modify the
definition environment Δ, and thus trigger further recomputations to reach the fixed-point of our
system of equations. Indeed, the context may force us to produce a mutable borrow, which can
only be achieved by forcing the return type of f itself to be a mutable borrow.
   To infer mutability information for an entire program, our analysis operates over top-level
function definitions in I-Sig. This rule can be seen as the entrypoint of our analysis. Given a
previous iteration of the analysis for 𝑓 , we compute the initial set 𝑅 of variables whose type is a
mutable borrow, based on the signature of 𝑓 . The translation of function body 𝑒 returns a new
function body 𝑒 ′ , as well as sets 𝑉 ′ and 𝑅 ′ . We update the definitions Δ with a new entry for 𝑓 ,
based on information inferred during the translation of 𝑒: if a function parameter 𝑥𝑖 belongs to the
set 𝑅 ′ , meaning it is expected to be a mutable borrow, then we modify its type 𝑇𝑖 accordingly.
   The presentation as a system of iterated equations alleviates the need for a topological sort of the
function definitions – there may simply be no such order, given mutually-recursive definitions in C
and Rust. The environment is initially populated with the output of our translation, meaning there
are no mut qualifiers anywhere. We then iterate the equations over Δ until a fixed point is reached.
There trivially exists such a fixed point: we only ever add mut qualifiers, meaning the number of
iterations is bounded by the numbers of function parameters across the whole program. In practice,
we of course do not do repeated iterations, and instead use an optimized fixed point library to
eliminate un-necessary recomputations [39].
   While Figure 10 presents the essence of our mutability inference algorithm, as mentioned earlier,
our implementation supports a much larger set of features, to translate our real-world case studies
(Section 4). Importantly, this analysis does not modify the Rust program; it only augments it with
additional mut qualifiers, meaning it can be validated a posteriori by the Rust compiler.

   Mutability in Structs and Tuples. We mentioned earlier that compiling some C structs to Rust
tuples was useful not just for code quality, but also for accepting more programs. We now explain
why. Consider a C program, equipped with a struct type t that holds two integer pointers, and two
functions t f(uint32_t *src) and t f_mut(uint32_t *src). If t compiles to a Rust struct, and if f_mut
returns pointers that are found to be &mut by our analysis, then our analysis will propagate this
information and make the two fields of t have type &'a mut u32; this, in turn, will force f to return
mutable pointers too.
   If instead t compiles to a Rust tuple, we can have both fn f(src: &[u32]) -> (&[u32], &[u32]) and
fn f_mut(src: &mut[u32]) -> (&mut[u32], &mut[u32]). Because the two tuple types are unrelated (we
say that they obey structural typing, as opposed to nominal typing like structs), making one mutable
does not affect the other and therefore avoids type-checking errors in f.

   Support for slices. Some C programs already manipulate the equivalent of a slice representation;
indeed, it is not uncommon, in security-sensitive contexts, to carry pointers along with their
lengths. Our implementation supports special annotations that designate such structs as officially
representing a slice, meaning occurrences of this struct compile directly to a Rust slice.

3.4    Automatically Deriving Traits Instances
A key component of the Rust language is its pervasive use of traits, which can be broadly seen as a
Rust-specific version of typeclasses [57]. Traits allow programmers to specify that a given type

                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:16                                                                     Aymeric Fromherz and Jonathan Protzenko


must implement certain features, for instance that it can be pretty-printed (Display trait), converted
from and to another type (From and Into traits), or that it allows deep copies (Clone trait).
   When defining a new type T, i.e., a new structure or enumeration, one can provide an implemen-
tation of a given trait 𝔗 by defining the methods corresponding to 𝔗 for type T, e.g., implementing
a fmt function that specifies how to pretty-print an element of type T allows to implement trait
Display for T. For some traits however, implementations can be automatically derived, using the
Rust #[derive(Trait)] attribute on the type definition, assuming that all fields of the structure or
enumeration do implement the trait.
   One trait of particular interest for our translation is the Copy trait. A common pattern in C is to
define a structure containing a pointer (e.g., a pointer to a string and the corresponding length), and
to pass the structure by value when calling functions. This leads to a mismatch with the Rust move
semantics. Rust implements an affine type system, meaning that, by default, values can be used at
most once: passing a value to a function, e.g., f(s), invalidates the value 𝑠, leading to compile-time
errors if s is further used in the program. To avoid this behavior, types can implement the Copy trait,
which instead performs a shallow copy of the value when passing it to a function.
   To avoid Rust compilation errors, we thus wish to automatically derive Copy when possible.
All basic Rust types (e.g., integers or booleans) and immutable borrow types &T implement Copy.
However, copying a mutable pointer (i.e., either &mut T or Box<T>) is not allowed; this would contradict
Rust’s guarantee that every piece of mutable data has a unique owner. To automatically add a
#[derive(Copy)] annotation on appropriate structure and enumeration type definitions, we traverse
all type definitions, and only derive the Copy trait if all fields are themselves Copy, that is, they are
neither a mutable borrow nor a box, and if they are a custom type, this type implements Copy itself.
The analysis is also performed through a fixpoint computation to handle (mutually) recursive
structs and enums.
   In addition to Copy, our analysis also automatically derives the PartialEq (allowing the use of the
== operator), and Clone traits when possible. Clone allows performing deep copies on a given value,
via an explicit call to the clone method. While our translation does not directly use this feature,
implementing Clone is a prerequisite to implement Copy (in Rust’s parlance, Copy has Clone as a parent
trait). Additionally, Clone is commonly used by library clients; we therefore strive to provide it as
much as possible to facilitate the adoption of the translated Rust library.

4     Evaluation
4.1      Implementation
We implement the compilation strategy described in this paper in a tool called Scylla. Scylla is
written in about 7,200 lines of OCaml, and took 1.5 person-year to author. For parsing actual C
code, Scylla relies on OCaml’s libclang bindings [25]; for compilation to Rust, Scylla relies on a
novel Rust representation in OCaml, complete with printer, visitors for optimization passes, and
the implementation of the various analyses and fixed-point computations we describe in this paper.
Finally, for Mini-C, Scylla relies on the existing KaRaMeL [40] project.
   Concerning the scope of modifications that were required for various projects to translate to
safe Rust, we estimate that no more than a few days of work were spent on each project. This also
includes fixing the proofs in HACL★. For all projects, we confirmed that the Scylla-translated Rust
code compiled and passed tests that we manually ported.

4.2      Case Studies
We evaluate our methodology on five real-world codebases that exemplify the kind of regular,
applicative C code that we can convert to safe Rust. For each of those, we first describe the

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                     121:17


     Table 1. Performance comparison. Results are normalized taking the original C code as a baseline.

                       Benchmark                              Original C   Rewritten C    Rust
                       SymCrypt SHA3-256                      1            1.00           1.00
                       SymCrypt SHA3-384                      1            1.00           1.01
                       SymCrypt SHA3-512                      1            1.00           1.00
                       Frodo640KEM KeyGen                     1            .98            .97
                       Frodo640KEM Encaps                     1            .99            .98
                       Frodo640KEM Decaps                     1            .99            .99
                       HACL★ Curve25519                       1            1.02           .99
                       HACL★ SHA2-256                         1            .99            1.05
                       HACL★ ChachaPoly-Enc                   1            1.00           .99
                       HACL★ ECDH-P256                        1            .98            .77
                       bzip2-compress                         1            .99            1.08
                       EverParse CBOR 2200                    1            1.00           .87
                       EverParse CBOR 1000                    1            1.00           1.21
                       EverParse CBOR 250                     1            1.00           1.22
                       EverParse CBOR 2200 (inline)           1            1.00           .65
                       EverParse CBOR 1000 (inline)           1            1.00           .91
                       EverParse CBOR 250 (inline)            1            1.00           .91

changes we had to enact to make the code eligible for translation. Then, we measure performance,
quantifying both the cost of restructuring the C code to fit Mini-C, and the performance impact of
switching to Rust. When comparing C and Rust, we use the clang and rustc compilers, and make
sure that the version of LLVM is identical for both.
   All experiments were run on a MacOS 15.5 machine with an ARM M3 Max processor and
96GB of RAM. Aiming for an apples to apples comparison, we compile the C code with the -O2
optimization level, while the Rust code is compiled in release mode, with opt-level set to 2. To
minimize the impact of differences in compilation toolchains, e.g., Rust treating an entire crate
as a single translation unit, which opens up tremendous optimization opportunities, we enable
link-time optimization (LTO) in both C and Rust. In C, we do this by passing the -flto option to
clang, while we set lto = "fat" in Rust.

4.2.1 SymCrypt. SymCrypt is the cryptographic library used in all Microsoft products and services.
It is written in C, and for a few years now, has been open-source [26]. We ran Scylla on its Keccak
implementation, which includes four variants of SHA3 [33] and two variants of SHAKE [33] and
CSHAKE [34]. After marking SymCrypt-specific helpers for endianness conversion as opaque (a
one-line change for about twenty helpers), the code was converted to safe Rust out of the box. For
code quality, we replaced C macros with static inline variants, which produced functions in Rust,
instead of translating the result of macro-expansion. Out of 1814 lines of C code, the diff utility
reports 91 insertions and 61 deletions for the Keccak-related files. 22 insertions correspond to the
straightforward addition of Scylla opaque annotations. The rest corresponds to the replacement
of 13 C macros by static inline functions. While each line of the macros needs to be modified
due to the C macro syntax requiring trailing \ characters compared to function bodies, therefore
increasing the number of lines modified, changes were completely mechanical.
    For performance benchmarking, we added FFI bindings to our Rust Keccak implementation that
had the exact same API as the original C code, down to the layout of the structs. We were then able
to use SymCrypt’s internal benchmarking utility to measure either the original C implementation,
or our own Rust implementation exposed through the same C ABI. Because we enacted no structural
changes on the source code, the performance is identical.

                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:18                                                                     Aymeric Fromherz and Jonathan Protzenko


4.2.2 FrodoKEM. We took the reference Microsoft C implementation of FrodoKEM [27], a post-
quantum key-exchange mechanism [24], and set out to translate it to Rust. This was perhaps our
most interesting example. First, we adopted a hybrid approach. FrodoKEM relies on two primitives:
AES [31] and SHA3 [33]. We chose to translate SHA3, but not AES, because none of the AES
variants packaged in FrodoKEM were eligible for translation. The pure C variant violates strict
aliasing, meaning it not only exercises undefined behavior, but is also ineligible for translation
to Scylla. The version that leverages hardware instructions is not supported by Scylla either, as
we do not yet compile compiler intrinsics to their Rust equivalents. We simply created a hybrid
build, where AES remains in C, and we wrote FFI bindings to allow our translated Rust code to call
the original AES. For a real-world scenario, we would simply “fill out” the AES implementation
using an existing crate. The second reason this example is of particular interest is that it uncovered
several cases of undefined behavior (UB) in the FrodoKEM implementation. Cryptographic code
oftentimes converts between char* and uintN_t*, which is legal in C, and which Scylla supports,
using a mechanism similar to the zerocopy crate [54]. However, compared to C, Rust checks such
conversions for proper alignment in debug builds. As it turns out, alignment was violated in Rust,
which we traced back to an alignment violation in C, which is UB. Furthermore, we also uncovered
a conversion between uint16_t* and uint32_t*, which we do not support in Scylla, because it is UB
in C. Both UBs were responsibly disclosed and reported upstream, along with a suggested fix.
   Beyond that, the bulk of our changes revolved around lifetimes: the code was written C89-style,
with all variables declared at the top of the function, which generated un-necessary long lifetimes
in Rust. We solved these by moving variable declarations closer to their use-site, or by using a
macro to replace a local variable with its definition when it is trivial, e.g. turn int *x = y + 3 into
#define x (y + 3). Out of 1451 lines of C code, the diff utility reports 5.5% of the source code impacted.
Most of these modifications were highly mechanical: moving variable declarations represents 75%
of these changes, while copying small arrays passed as function arguments to satisfy the Rust
borrow checker represents an additional 17%.
   The Rust code is slightly faster than the original C; the illegal cast from uint16_t* to uint32_t*
was intended to implement a memcpy, 4 bytes at a time. Our fix was to replace it with an actual memcpy
instruction, which probably allowed the compiler to optimize a little bit more.

4.2.3 HACL★. HACL★ is a verified cryptographic library [38], compiled to C from Low★ [40], a
low-level dialect of the F★ programming language [47]. Because Low★ contains very few constructs,
namely, arrays, machine integers, structures, pointer arithmetic, and primitive array operations
such as blit or fill, the resulting C code is very regular, and is a prime candidate for translation
to safe Rust. As part of our evaluation, we had to rewrite some code to make it eligible to Rust
translation. For this case study, we chose to modify the source Low★ code rather than the C that
is auto-generated from Low★. We did so for two reasons: first, we wanted to preserve the formal
guarantees of HACL★, rather than perform unverified edits on C code; second, we wanted to assess
how much harder verification would become if we rewrote parts of the library. We report that the
verification impact was negligible, and that our changes only incurred a few person-days of effort.
   We now report on our porting effort for the following algorithms: Chacha20Poly1305, Curve25519,
P256, SHA2, Poly1305, and supporting bignum libraries. These represent different flavors of code,
totalling 14,018 lines of C, and cover almost all usage patterns present in HACL★.
   Chacha20Poly1305 is an authenticated encryption algorithm [30]. Its HACL★ implementation
performs no heap allocation and offers a one-shot API. As such, we were able to translate it to Rust
with no modifications, except copying a temporary array to satisfy mutability constraints.
   The P256 elliptic curve [35] relies on a general-purpose bignum library for core field operations.
For benchmarking, we show a composite P256 benchmark that relies on the bignum library. P256 is

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                     121:19


authored in a style where arguments to core field operations may be disjoint or equal; in other words,
void fmul(uint32_t *dst, uint32_t *a, uint32_t *b), allows its dst and a arguments to potentially alias
one another; this is typical of cryptographic code. The main difficulty for P256 was to rewrite
such functions into two variants: one that takes disjoint arguments, and one that takes in-place
arguments, performing a copy in order to call the disjoint version. Using the equivalent of macros
in Low★ (helpers marked as inline_for_extraction), we were able to make this change transparent
from the verification perspective. We also had to enact several minor, local fixes, mostly to avoid
generating code that dereferences the state (which would generate a move), and instead reference
only fields of the state (which Rust can then auto-borrow). The Curve25519 elliptic curve [2]
relies on a custom bignum library just for this particular field. We encountered the same flavor of
problems as with P256; we followed the same methodology to allow the translation to proceed.
   The SHA2 family of hash algorithms [32] offer a “streaming” API that relies on long-lived heap-
allocated state, and non-trivial ownership patterns. The original code was written for C, not Rust,
meaning that the code and proofs leveraged aliasing relationships between local variables and
fields of the state. We performed a series of local, targeted rewritings to avoid a few patterns that
were incompatible with Rust.
   The Poly1305 message authentication code (MAC) algorithm [1] is also streaming, and further-
more manages ownership of a key throughout the lifetime of its state. Fortunately, the streaming
API of HACL★ is written and proven once [12], meaning that our changes above also benefitted
Poly1305; a few additional tweaks were needed for parts of the code that deal with the key.
   While close to being translatable to Rust, these algorithms still required some changes. Out
of 35,879 lines of (source, Low★) code for these algorithms, diff reports 1296 insertions, and 318
deletions, meaning 4.5% of the source code was affected. This diff also includes fixed proofs.
   For performance, we report individual numbers for each algorithm; performance is largely
identical, save for P256 that is significantly faster in Rust. We speculate that this may be due to
link-time optimizations, which are more aggressive in Rust than in C, and may allow bignum
operations to be composed more efficiently with the P256 code.
   Translating Verified Code. Given that HACL★’ C code already includes formal guarantees of
memory safety and functional correctness, one might wonder, what is the point of translating it to
safe Rust instead of using FFI bindings and encapsulating the library in a Rust crate? First, having
a library entirely written in Rust simplifies the build system, as it directly allows to use the Rust
ecosystem (cargo) instead of managing multi-language builds. More importantly, avoiding the use
of unsafe, needed to write bindings, increases the trust in the library and facilitates adoption of the
code: instead of trusting a (potentially) foreign language such as F★ or Rocq with the safety of their
code, users can rely on the more familiar rustc compiler.
4.2.4 The bzip2 compression library. All three examples above concern cryptographic libraries,
which fundamentally fit within the subset of code that Scylla was designed to translate (modulo small
edits). Going beyond cryptographic algorithms, we now study the bzip2 compression library [48].
This constitutes a relevant example for many reasons: first, the code is very low-level, meaning that
understanding it deeply enough to rewrite it in Rust manually requires considerable effort. Second,
the code has been hand-tuned and optimized, with a lot of accumulated knowledge – one corner
case, according to a comment, is triggered by compressing 48.5 million instances of the character
251. An automated translation will preserve these corner cases. Third, the code is security-critical,
and as such, is a prime candidate for conversion to a safe language.
   The library consists of three parts: compression, decompression, and orchestration. Of these
three, Scylla can only translate compression. Decompression is ineligible for translation to safe Rust,
since its main function uses unstructured control-flow in C, with a switch statement jumping to a

                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:20                                                                     Aymeric Fromherz and Jonathan Protzenko


label found within a for-loop. Orchestration interacts deeply with the operating system through file
streams, and would need to be rewritten in a Rust-idiomatic way. We thus focus on compression
only, representing 2969 lines of C code and 34% of the bzip2 source code (excluding tests and the
bzip2recover utility, which we did not attempt to translate).
   The bzip2 library is an old piece of code, written in the mid-90s. One particular difficulty was that
its state type contains multiple aliases towards the same piece of data, presumably to allow for direct
loads rather than forcing offset computations – perhaps this had a measurable performance impact
in the 1990s. In any case, this is exactly the type of pattern that is incompatible with Rust. This is
where our methodology shines: we were able to experiment with rewrites that eliminated those
aliases, while running the (comprehensive) bzip2 test suite to ensure the C code remained correct.
We removed those aliases, relying on macros to replicate the offset computations at use-site while
minimizing changes to the source. Other familiar issues cropped up: we had to shorten the lifetime
of several variables. In a hot loop, an alias to a mutable array was replaced by offset computations,
potentially generating an indirect load – again, this may have been important 30 years ago. We also
found one unncessary goto (unsupported) that could be replaced with a break (supported). Among
files related to compression, only 3.5% of the source code was impacted. Similarly to FrodoKEM,
the translation process unearthed two sources of undefined behaviors: an alignment issue and a
strict aliasing violation. We reported both issues upstream.
   Building bzip2 with our changes thus required a hybrid build, in which compression is in Rust,
but decompression and orchestration remain in C. This required adding a custom FFI to go back and
forth between both languages; furthermore, because the state type contains pointers, a conversion
between C state and Rust state was necessary, the former containing raw pointers and the latter
containing slices. This state conversion is non-trivial, as the state type contains 36 fields. In spite of
this, our benchmark, which compresses 100M random bytes, shows only a 8% overhead for our Rust
version – we posit that this overhead would be largely eliminated if we switched from a hybrid
build to a pure Rust build (thus eliminating state conversions).


4.2.5 EverParse. Finally, we turn our attention to another security-critical domain that would
benefit from conversion to safe Rust: parsers and serializers. For our final case study, we focus on
EverParse [41], a verified parsers and serializers library. We particularly focus on the CBOR-DET
parser [18] generated by EverParse. CBOR-DET is an ongoing IETF draft for a binary format akin
to JSON, and specifically, a deterministic variant of it. It consists of 4700 lines of C code.
   To translate CBOR-DET through Scylla, the key changes were to annotate several tagged union
datatypes to reconstruct them as Rust ADTs, and to reconstruct additional datatypes as tuples to
pass Rust’s mutability analysis. This required the addition of 19 lines of code. Additionally, we
needed to add default values for variables declared and later defined, but where the Rust compiler
was not able to statically determine that the variable was defined for all execution paths. This
typically occurred on patterns of the shape int x; if (...) { x = e } else { exit(...) }, where one
of the execution paths was an error, translated to a Rust panic. While pervasive (accounting for
about 4.1% of the codebase), these changes were however straightforward.
   On average, Scylla-generated code for CBOR is slower than its C counterpart. However, the
performance is highly sensitive to inlining annotations. Because this code is originally verified,
it tends to rely on a myriad of small helper functions (easier to verify) which get inlined away
by the compiler. Aggressively adding (by hand) inlining annotations makes our Rust version 22%
faster than the C version; however, inlining did not have a noticeable impact on the C code. This
suggests that the differences reflect diverging inlining strategies between the compilers, rather
than a fundamental limitation with either our approach or rustc.


Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
 Scylla: Translating an Applicative Subset of C to Safe Rust                                                     121:21

 pub fn chacha20_encrypt_block(ctx: &[u32], out: &mut [u8], incr: u32, text: &[u8]) {
   let mut k: [u32; 16] = [0u32; 16usize];
   chacha20_core(&mut k, ctx, incr);
   let mut bl: [u32; 16] = [0u32; 16usize];
   for i in 0u32..16u32 {
     let bj: (&[u8], &[u8]) = text.split_at(i.wrapping_mul(4u32) as usize);
     let u: u32 = load32_le(bj.1);
     let os: (&mut [u32], &mut [u32]) = bl.split_at_mut(0usize);
     os.1[i as usize] = u }
 }

 unsafe extern "C" fn chacha20_encrypt_block(
     mut ctx: *mut uint32_t, mut out: *mut uint8_t, mut incr: uint32_t, mut text: *mut uint8_t,
 ) {
   let mut k: [uint32_t; 16] = [0 as libc::c_uint, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,];
   chacha20_core(k.as_mut_ptr(), ctx, incr);
   let mut bl: [uint32_t; 16] = [0 as libc::c_uint, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,];
   let mut i: uint32_t = 0 as libc::c_uint;
   while i < 16 as libc::c_uint {
     let mut bj: *mut uint8_t = text.offset(i.wrapping_mul(4 as libc::c_uint) as isize);
     let mut u: uint32_t = load32_le(bj);
     let mut os: *mut uint32_t = bl.as_mut_ptr();
     *os.offset(i as isize) = u;
     i = (i as libc::c_uint).wrapping_add(1 as libc::c_uint) as uint32_t as uint32_t; }
 }

                  Fig. 11. Translation of encrypt_block with Scylla (top) and c2rust (bottom)


 4.3     Comparison with c2rust
 To conclude our evaluation, we now compare the output of Scylla with related tools; in practice,
 only c2rust can be successfully compiled from its repository; other tools mentioned in Section 6
 either do not build, cannot process our source code, or fail to detect any subset of the code that
 could be translated from unsafe Rust to Rust. For this comparison, we rely on the Chacha20
 implementation from HACL★, which we translate with both Scylla and c2rust. We present in
 Figure 11 the translations of the encrypt_block function (shortened for brevity), whose C version is
 shown below.
 1     void chacha20_encrypt_block(uint32_t *ctx, uint8_t *out, uint32_t incr, uint8_t *text) {
 2       uint32_t k[16U] = { 0U };
 3       chacha20_core(k, ctx, incr);
 4       uint32_t bl[16U] = { 0U };
 5       for (int i = 0; i < 16; i++) {
 6         uint8_t *bj = text + i * 4U;
 7         uint32_t u = load32_le(bj);
 8         uint32_t *os = bl;
 9         os[i] = u;
10     }
    While small, this function contains several representative features of C, including pointer arith-
 metic to retrieve a subslice (on line 6), structured control-flow, and array accesses and updates. As
 previously described, c2rust relies entirely on unsafe code, which allows the use of C-like pointers
 in Rust (e.g., *mut uint32_t). In contrast, Scylla relies on borrows (e.g., &[u32]), which come with
 static memory safety guarantees. Scylla’s mutability inference analysis also allows to mark several
 variables and arguments as immutable, while c2rust pervasively uses mut qualifiers. However,
 Scylla’s use of safe Rust restricts possible uses of the encrypt_block function: in C, this function

                              Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:22                                                                                  Aymeric Fromherz and Jonathan Protzenko


                                  F* extraction pipeline (prior work)




                         F*
                                                                F* IR                     Scylla
                                  Low*, Pulse…
                                                                                         (this work)




                         F*
                                                                F* IR           Scylla
                                  Low*, Pulse…
                                                                        (“alternative toolchain”)



                Fig. 12. General-purpose toolchain (above), and alternative toolchain (below)


allowed the use of in-place encryption, i.e., passing the same pointer for arguments out and text, as
out is only written after text has been read (omitted here). While allowed through the use of unsafe
in c2rust’s translation, the mutability xor aliasing rule of the Rust borrow-checker prevents this
for the Scylla safe version; providing in-place encryption would require a rewrite of the source
C program to expose an API with a single in/out argument. As shown in this example, Rust code
generated by Scylla aims to be readable and maintanable: names from the original C program
are preserved (modulo lexical conventions occasionally differing in C and Rust), and the use of
idiomatic Rust patterns simplifies maintaining and evolving translated codebases.

5   Alternative Toolchain
Some of our case studies involve the F★ language, and specifically, those of its DSLs that compile (a
subset of) F★ to C. Those are Low★ [40] (used by our HACL★ case study), Steel [9], and Pulse [5]
(used by our EverParse case study). In this paper, we presented a general-purpose toolchain that
consumes C code; for those case studies, this means that we directly consumed C code produced by
F★, relying on Scylla to parse it and translate it to Rust.
   As an experiment, we developed an alternative toolchain (Figure 12) that skips concrete C syntax,
and directly consumes F★’s intermediary representation (IR). F★’s IR is isomorphic to Mini-C,
meaning we can emit Rust code directly without going through the artifact of an actual C file.
   This alternative toolchain outputs identical Rust code, but operates more efficiently. In addition to
build simplification and usability improvements, the alternative toolchain relieves the programmer
of some of the annotation burden: because the F★ IR still has tuples, data types, and in some cases,
a model of slices, this means that the programmer need not provide annotations for those.
   This alternative toolchain was used for a new generation of parsers and serializers [42], and for
Bert13 [3], a formally verified implementation of TLS 1.3 which relies on HACL★ compiled straight
from F★ to Rust. Naturally, this toolchain has limited applicability, and we advocate for the usage
of Scylla, to be able to translate C code generally, regardless of whether it was generated from F★.

6   Related Work
Since this is such a high-value target, many attempts have been made to automatically translate C to
Rust. Historically, the first widespread tool for C to Rust translation is the aptly-named C2Rust [10],
which combines earlier attempts Citrus [21] and Corrode [44]. The tool translates C99 code to
unsafe Rust, leveraging Rust’s ability to manipulate raw, C-like pointers via the use of unsafe. The
tool accepts a large subset of C, and envisions a manual rewriting of the unsafe Rust into safe
Rust. Several tools were since then built atop C2Rust, trying to automate the rewriting process that
gradually removes unsafe in the translated Rust code.

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                     121:23


   Emre et al. [7] simply borrow-check the output of C2Rust, hijacking the Rust compiler in order
to see if any unsafe raw pointers actually do borrow-check. In the event that they do, the usage of
unsafe is removed, and the raw C pointers get promoted to regular, safe Rust borrows. Their analysis,
however, focuses on functions whose unsafety comes from usage of raw pointers only, meaning that
in their case study, libxml2, they rewrite 210 functions out of 3,029, but with a 97% success rate.
The rest of the functions remain unsafe.
   Zhang et al. [60] build a custom set of ownership- and mutability-based analyses that operate
post-C2Rust, again trying to limit the amount of unsafe pointers and unsafe code. The tool, dubbed
Crown, achieves greater unsafe reduction rates than Emre et al. [7].
   Emre et al. [6] later opt for an in-house analysis (rather than reusing the Rust compiler), which
allows for more functions to be successfully translated to safe Rust. This newer analysis may rewrite
programs (rather than simply turn raw pointers into borrows). Still, only a fraction of the functions
eventually make it to safe Rust. The authors share the issues with nominal struct types (§7.2) that
we describe in Section 3.3, but do not circumvent it through a translation to tuples like we do.
   Ling et al. [23] push the idea further, and use TXL, a programming language dedicated to source-
to-source transformations, to automate the rewriting of unsafe Rust into safe Rust even more. The
authors introduce “semantics-approximating” rules, which ultimately allow them to convert a large
fraction of unsafe functions into safe ones, although the preservation of semantics does not seem
to be guaranteed. Once again, this is seen as a stepping stone for engineers to tackle the migration
of a codebase, rather than a fully automated “fire and forget” translation approach.
   To support the translation of C code with unstructured control-flow, C2Rust relies on the Relooper
algorithm to translate gotos to structured control flow [43, 59]. While the resulting Rust code is
harder to match with the original C sources, we could implement this approach in Scylla to extend
the C subset we support.
   All of the works above aim to translate first into almost fully-unsafe Rust, then either manually
or automatically rewrite the code to pull it out of the unsafe subset, reaching for partial safety. We
advocate for a different approach: iterate on the C code until it successfully translates, keeping
existing integration, unit testing, or proofs to assess the validity and/or correctness of the rewrites.
Then, once the rewrite fits within our supported subset, proceed, and obtain fully safe code.
   A separate line of work takes a more focused approach and studies specific patterns that occur
in C to translate them to idiomatic Rust – this is a concern that goes beyond mere safety and
correctness. This line of work still builds atop C2Rust. Problems include: translating the Posix Lock
API of C to Rust’s native lock and ownership semantics [14]; replacing output parameters with
more Rust-native return values and algebraic data types through an abstract interpretation analysis
to infer what constitutes an output parameter [13, 15]; or reconstructing Rust enumerations from
C tagged unions [16]. Again, these all partially remove unsafe; furthermore, these target a more
systems-oriented subset of C, rather than the data-oriented subset we tackle.
   Li et al. [22] study the process of translating C code to Rust from a user perspective. They
particularly observe that manually translating the code is error-prone, and that it is important
to target idiomatic Rust code. Our approach aims to follow these guidelines; the readable code
outputted can also serve as a basis for further rewritings.
   With the explosion in popularity of LLMs, translating C to Rust with an LLM was inevitable.
Pan et al. [37] find that while GPT-4 generates code that is more idiomatic than C2Rust, only 61%
of it is correct (i.e., compiles and produces the expected result), compared to 95% for C2Rust. Hong
et al. [17] investigate how to mitigate errors introduced by LLMs in the translation process, while
Yang et al. [58] attempt to validate LLM-translated code using property-based testing and bounded
model checking. Nitin et al. [36] propose to rely on LLMs to make Rust code generated by C2Rust
both safer and more idiomatic. Their approach however only reduces the amount of unsafe code by

                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:24                                                                     Aymeric Fromherz and Jonathan Protzenko


up to 28%. These works tackle another problem area, where possibly-faulty translations might be
acceptable. We focus instead on critical applications, where having confidence in the safety of the
produced Rust code is paramount.
   Focusing on C++ instead, CRAM [11] advocates for an approach similar in spirit to ours: rewrite
the source C++ code to use abstractions that encode Rust’s borrow-checking discipline using
advanced C++ templates and type-system features; then, once the code has been sufficiently
refactored, translate it to Rust. Details on CRAM are scarce, as the tool appears to be closed-source,
and no publications are available. The translation is described as “provably safe”, which does not
conclusively indicate whether the produced code uses unsafe or not.
   The tool cpp2rust aims to produce safe Rust out of source C++; it does by producing reference-
counted Rust (i.e., code that uses RefCell). Subsequent static analyses rewrite the code, wherever
possible, to get rid of the uses of RefCell.

7   Conclusion
We presented a methodology that provides a predictable, deterministic and auditable translation
from a sizeable, data-oriented subset of C to safe Rust. Our methodology relies on an iterative
approach: rather than translate to unsafe Rust, we instead improve the C code until it has enough
structure that it becomes eligible for compilation to safe Rust. This allows leveraging existing
engineering processes, regression suites, and continuous integration, to ensure that the rewrites
cause no change of behavior. For security-critical code where even tiny mistakes may incur a very
high cost (e.g., cryptography), we believe this provides a more compelling approach than existing
LLM-based rewrites, or than toolchains that generate unsafe Rust.
   The subset of C we support is large enough to translate: cryptographic algorithms written in
different styles; parsers and serializers; and a large chunk of the well-known bzip2 compression
library. We provide readable, maintainable code, leveraging safe Rust abstractions such as slices,
enums and matches, rather than producing low-level C code disguised as unsafe Rust.
   Our experimental evaluation shows that the changes required to the original C code are small,
and that the performance of the resulting safe Rust code is almost always indistinguishable from
that of the original C. This provides, we believe, concrete evidence that our approach scales and
provides a pathway for high-assurance rewrites from C to Rust.
   While the various steps of our translation are formalized with pen-and-paper, and our case
studies empirically show that codebases translated by Scylla pass functional tests, we currently
do not have any formal guarantees about the correctness of the translation. We however hope to
mechanically formalize and prove the correctness of our scheme in future work, by framing it as a
semantic equivalence at the source level.

Acknowledgments
We thank Guillaume Boisseau and Son Ho for several discussions about the Rust semantics and
borrow-checker, Tahina Ramananandro for invaluable help with understanding EverParse and the
CBOR-DET implementation, and the anonymous reviewers for valuable feedback about earlier
versions of this draft. This work benefited from funding managed by the French National Research
Agency under the France 2030 programme with the reference ANR-22-PECY-0006.

  Data-Availability. Our tool is open-source, and publicly available on Github. Additionally, to
foster reproducibility, we provide an artifact available on Zenodo which contains the version of
Scylla described in this paper, as well as the experimental evaluation [8].

Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                             121:25


References
 [1] Daniel J Bernstein. 2005. The Poly1305-AES message-authentication code. In International workshop on fast software
     encryption. Springer, 32–49.
 [2] Daniel J. Bernstein. 2006. Curve25519: New Diffie-Hellman Speed Records. In Proceedings of the IACR Conference on
     Practice and Theory of Public Key Cryptography (PKC).
 [3] Karthikeyan Bhargavan, Lasse Letager Hansen, Franziskus Kiefer, Jonas Schneider-Bensch, and Bas Spitters. 2025.
     Formal Security and Functional Verification of Cryptographic Protocol Implementations in Rust. In Proceedings of the
     ACM Conference on Computer and Communications Security (CCS). https://eprint.iacr.org/2025/980
 [4] Kees Cook. 2022. [GIT PULL] Rust introduction for v6.1-rc1. https://lore.kernel.org/lkml/202210010816.1317F2C@
     keescook/.
 [5] Gabriel Ebner, Guido Martínez, Aseem Rastogi, Thibault Dardinier, Megan Frisella, Tahina Ramananandro, and
     Nikhil Swamy. 2025. PulseCore: An Impredicative Concurrent Separation Logic for Dependently Typed Programs. In
     Proceedings of the Conference on Programming Language Design and Implementation (PLDI).
 [6] Mehmet Emre, Peter Boyland, Aesha Parekh, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2023. Aliasing limits
     on translating C to Safe Rust. Proceedings of the ACM on Programming Languages 7, OOPSLA1 (2023), 551–579.
 [7] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2021. Translating C to safer Rust. Proceedings of the
     ACM on Programming Languages 5, OOPSLA (2021), 1–29.
 [8] Aymeric Fromherz and Jonathan Protzenko. 2026. Scylla: Translating an Applicative Subset of C to Safe Rust (Artefact).
     doi:10.5281/zenodo.18498233
 [9] Aymeric Fromherz, Aseem Rastogi, Nikhil Swamy, Sydney Gibson, Guido Martínez, Denis Merigoux, and Tahina
     Ramananandro. 2021. Steel: Proof-Oriented Programming in a Dependently Typed Concurrent Separation Logic. In
     Proceedings of the International Conference on Functional Programming (ICFP). doi:10.1145/3473590
[10] Galois and Immunant. 2019. C2Rust: Migrating Legacy Code to Rust. https://github.com/immunant/c2rust.
[11] GrammaTech. 2024. CRAM: C++ to Rust Assisted Migration. https://www.grammatech.com/cyber-security-solutions/
     migration-to-memory-safe-code/
[12] Son Ho, Aymeric Fromherz, and Jonathan Protzenko. 2023. Modularity, Code Specialization, and Zero-Cost Abstractions
     for Program Verification. In Proceedings of the International Conference on Functional Programming (ICFP). doi:10.1145/
     3607844
[13] Jaemin Hong. 2023. Improving Automatic C-to-Rust Translation with Static Analysis. In 2023 IEEE/ACM 45th Interna-
     tional Conference on Software Engineering: Companion Proceedings (ICSE-Companion). IEEE, 273–277.
[14] Jaemin Hong and Sukyoung Ryu. 2023. Concrat: An automatic C-to-Rust lock API translator for concurrent programs.
     In 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE). IEEE, 716–728.
[15] Jaemin Hong and Sukyoung Ryu. 2024. Don’t Write, but Return: Replacing Output Parameters with Algebraic Data
     Types in C-to-Rust Translation. Proceedings of the ACM on Programming Languages 8, PLDI (2024), 716–740.
[16] Jaemin Hong and Sukyoung Ryu. 2024. To Tag, or Not to Tag: Translating C’s Unions to Rust’s Tagged Unions. arXiv
     preprint arXiv:2408.11418 (2024).
[17] Jaemin Hong and Sukyoung Ryu. 2025. Type-migrating C-to-Rust translation using a large language model. Empirical
     Software Engineering 30, 1 (2025), 3.
[18] Internet Engineering Task Force. 2020. Concise Binary Object Representation (CBOR) - RFC 8949. https://datatracker.
     ietf.org/doc/rfc8949/.
[19] ISO. 2011. ISO/IEC 9899:2011 C standard. https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf.
[20] Sylvestre Ledru. 2025. Extending the Coreutils project - Rewriting base tools in Rust. https://uutils.github.io/blog/2025-
     02-extending/.
[21] Kornel Lesinski. 2017. Citrus: Convert C to Rust. https://gitlab.com/citrus-rs/citrus.
[22] Ruishi Li, Bo Wang, Tianyu Li, Prateek Saxena, and Ashish Kundu. 2025. Translating C To Rust: Lessons from a User
     Study. In Proceedings of the Network and Distributed System Security Symposium (NDSS).
[23] Michael Ling, Yijun Yu, Haitao Wu, Yuan Wang, James R. Cordy, and Ahmed E. Hassan. 2022. In rust we trust: a
     transpiler from unsafe C to safer rust (ICSE ’22). Association for Computing Machinery, New York, NY, USA, 354–355.
     doi:10.1145/3510454.3528640
[24] Patrick Longa, Joppe W Bos, Stephan Ehlen, and Douglas Stebila. 2025. FrodoKEM: Learning With Errors Key
     Encapsulation. https://datatracker.ietf.org/doc/draft-longa-cfrg-frodokem/00/.
[25] Thierry Martinez. [n. d.]. Clangml, OCaml bindings for Clang. https://github.com/ocamllibs/clangml.
[26] Microsoft. 2016. SymCrypt: Cryptographic Library. https://github.com/microsoft/SymCrypt.
[27] Microsoft. 2025. FrodoKEM: Learning With Errors Key Encapsulation. https://github.com/microsoft/PQCrypto-
     LWEKE.
[28] Mozilla Hacks. 2024. Porting a cross-platform GUI application to Rust. https://hacks.mozilla.org/2024/04/porting-a-
     cross-platform-gui-application-to-rust/.


                              Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
121:26                                                                         Aymeric Fromherz and Jonathan Protzenko


[29] National Security Agency. 2022. Software Memory Safety. https://media.defense.gov/2022/Nov/10/2003112742/-1/-
     1/0/CSI_SOFTWARE_MEMORY_SAFETY.PDF.
[30] Yoav Nir and Adam Langley. 2015. ChaCha20 and Poly1305 for IETF protocols. https://datatracker.ietf.org/doc/html/
     draft-irtf-cfrg-chacha20-poly1305-10.
[31] NIST. 2001. Advanced Encryption Standard (AES). http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf.
[32] NIST. 2015. Secure Hash Standard (SHS). https://csrc.nist.gov/pubs/fips/180-4/upd1/final.
[33] NIST. 2015. SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions. https://csrc.nist.gov/pubs/
     fips/202/final.
[34] NIST. 2016. SHA-3 Derived Functions: cSHAKE, KMAC, TupleHash, and ParallelHash. https://csrc.nist.gov/pubs/sp/
     800/185/final.
[35] NIST. 2023. Digital Signature Standard (DSS). https://csrc.nist.gov/pubs/fips/186-5/final.
[36] Vikram Nitin, Rahul Krishna, Luiz Lemos do Valle, and Baishakhi Ray. 2025. C2saferrust: Transforming c projects into
     safer rust with neurosymbolic techniques. arXiv preprint arXiv:2501.14257 (2025).
[37] Rangeet Pan, Ali Reza Ibrahimzada, Rahul Krishna, Divya Sankar, Lambert Pouguem Wassi, Michele Merler, Boris
     Sobolev, Raju Pavuluri, Saurabh Sinha, and Reyhaneh Jabbarvand. 2024. Lost in translation: A study of bugs introduced
     by large language models while translating code. In Proceedings of the IEEE/ACM 46th International Conference on
     Software Engineering. 1–13.
[38] Marina Polubelova, Karthikeyan Bhargavan, Jonathan Protzenko, Benjamin Beurdouche, Aymeric Fromherz, Natalia
     Kulatova, and Santiago Zanella-Béguelin. 2020. HACLxN: Verified Generic SIMD Crypto (for All Your Favourite
     Platforms). In Proceedings of the ACM Conference on Computer and Communications Security (CCS).
[39] François Pottier. 2009. Lazy least fixed points in ML. Unpublished. Manuscript available at http://gallium. inria. fr/˜
     fpottier/publis/fpottier-fix. pdf (2009).
[40] Jonathan Protzenko, Jean-Karim Zinzindohoué, Aseem Rastogi, Tahina Ramananandro, Peng Wang, Santiago Zanella-
     Béguelin, Antoine Delignat-Lavaud, Catalin Hritcu, Karthikeyan Bhargavan, Cédric Fournet, and Nikhil Swamy.
     2017. Verified Low-Level Programming Embedded in F*. In Proceedings of the International Conference on Functional
     Programming (ICFP).
[41] Tahina Ramananandro, Antoine Delignat-Lavaud, Cédric Fournet, Nikhil Swamy, Tej Chajed, Nadim Kobeissi, and
     Jonathan Protzenko. 2019. EverParse: Verified Secure Zero-Copy Parsers for Authenticated Message Formats.. In
     Proceedings of the USENIX Security Symposium.
[42] Tahina Ramananandro, Gabriel Ebner, Guido Martínez, and Nikhil Swamy. 2025. Secure Parsing and Serializing with
     Separation Logic Applied to CBOR, CDDL, and COSE. arXiv:2505.17335 [cs.CR] https://arxiv.org/abs/2505.17335
[43] Norman Ramsey. 2022. Beyond Relooper: recursive translation of unstructured control flow to structured control flow
     (functional pearl). Proc. ACM Program. Lang. 6, ICFP, Article 90 (Aug. 2022), 22 pages. doi:10.1145/3547621
[44] Jamey Sharp. 2020. Corrode: Automatic semantics-preserving translation from C to Rust. https://github.com/
     jameysharp/corrode.
[45] Signal Messenger. 2020. libsignal-protocol-rust. https://github.com/signalapp/libsignal-protocol-rust.
[46] StackOverflow. 2023. 2023 Developer Survey. https://survey.stackoverflow.co/2023/#section-admired-and-desired-
     programming-scripting-and-markup-languages.
[47] Nikhil Swamy, Catalin Hritcu, Chantal Keller, Aseem Rastogi, Antoine Delignat-Lavaud, Simon Forest, Karthikeyan
     Bhargavan, Cédric Fournet, Pierre-Yves Strub, Markulf Kohlweiss, Jean-Karim Zinzindohoué, and Santiago Zanella-
     Béguelin. 2016. Dependent Types and Multi-Monadic Effects in F*. In Proceedings of the ACM Symposium on Principles
     of Programming Languages (POPL).
[48] The bzip2 contributors. [n. d.]. bzip2. https://gitlab.com/bzip2/bzip2.
[49] The Chromium Project. 2020. Memory Safety. https://www.chromium.org/Home/chromium-security/memory-safety/.
[50] The MSRC Team. 2019. A Proactive Approach to More Secure Code. https://msrc.microsoft.com/blog/2019/07/a-
     proactive-approach-to-more-secure-code/.
[51] The Register. 2022. In Rust We Trust: Microsoft Azure CTO shuns C and C++. https://www.theregister.com/2022/09/
     20/rust_microsoft_c/.
[52] The Register. 2023. Microsoft is busy rewriting core Windows code in memory-safe Rust. https://www.theregister.
     com/2023/04/27/microsoft_windows_rust/.
[53] The White House. 2024. Back to the Building Blocks: a Path Toward Secure and Measurable Software. https:
     //www.whitehouse.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf.
[54] The zerocopy Contributors. [n. d.]. Crate zerocopy. https://docs.rs/zerocopy/latest/zerocopy/.
[55] Jeff Vander Stoep and Alex Rebert. 2024. Eliminating Memory Safety Vulnerabilities at the Source. https://security.
     googleblog.com/2024/09/eliminating-memory-safety-vulnerabilities-Android.html.
[56] Sara Verdi. 2023. Why Rust is the most admired language among developers. https://github.blog/2023-08-30-why-
     rust-is-the-most-admired-language-among-developers/.


Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
Scylla: Translating an Applicative Subset of C to Safe Rust                                                         121:27


[57] Philip Wadler and Stephen Blott. 1989. How to make ad-hoc polymorphism less ad hoc. In Proceedings of the ACM
     Symposium on Principles of Programming Languages (POPL).
[58] Aidan ZH Yang, Yoshiki Takashima, Brandon Paulsen, Josiah Dodds, and Daniel Kroening. 2024. VERT: Verified
     equivalent rust transpilation with large language models as few-shot learners. arXiv preprint arXiv:2404.18852 (2024).
[59] Alon Zakai. 2011. Emscripten: an LLVM-to-JavaScript compiler. In Proceedings of the ACM SIGPLAN Conference on
     Object-Oriented Programming, Systems, Languages and Applications (OOPSLA).
[60] Hanliang Zhang, Cristina David, Yijun Yu, and Meng Wang. 2023. Ownership guided C to Rust translation. In
     International Conference on Computer Aided Verification. Springer, 459–482.




                             Proc. ACM Program. Lang., Vol. 10, No. OOPSLA1, Article 121. Publication date: April 2026.
