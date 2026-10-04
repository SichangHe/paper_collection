# Charon: An Analysis Framework for Rust

Son Ho<sup>1⊠</sup>, Guillaume Boisseau<sup>2</sup>, Lucas Franceschino<sup>3</sup>, Yoann Prak<sup>2</sup>, Aymeric Fromherz<sup>2</sup>, and Jonathan Protzenko<sup>4</sup>

Microsoft Azure Research, UK, t-sonho@microsoft.com, Inria Paris, France,

{guillaume.boisseau,yoann.prak,aymeric.fromherz}@inria.fr,

<sup>3</sup> Cryspen, France, lucas@cryspen.com,

**Abstract.** With the explosion in popularity of the Rust programming language, a wealth of tools have recently been developed to analyze, verify, and test Rust programs. Alas, the Rust ecosystem remains relatively young, meaning that every one of these tools has had to re-implement difficult, time-consuming machinery to interface with the Rust compiler and its cargo build system, to hook into the Rust compiler's internal representation, and to expose an abstract syntax tree (AST) that is suitable for analysis rather than optimized for efficiency.

We address this missing building block of the Rust ecosystem, and propose Charon, an analysis framework for Rust. Charon acts as a swiss-army knife for analyzing Rust programs, and deals with all of the tedium above, providing clients with an AST that can serve as the foundation of many analyses. We demonstrate the usefulness of Charon through a series of case studies, ranging from a Rust verification framework (Aeneas), a compiler from Rust to C (Eurydice), and a novel taint-checker for cryptographic code. To drive the point home, we also re-implement a popular existing analysis (Rudra), and show that it can be replicated by leveraging the Charon framework.

**Keywords:** Static Analysis · Formal Verification · Rust.

### 1 Introduction

Over the past decade, the Rust programming language has gained traction both in academia and in industry [11,2,12,30,4,21,41], consistently ranking as the most beloved language by developers [44,37] for the past 8 years. A large part of this success stems from several key features of the language: Rust provides both the high performance and low-level idioms commonly associated to C or C++, as well as memory-safety by default thanks to its rich, borrow-based type system. This makes Rust suitable for a wide range of applications: both Windows [42] and the Linux kernel [10] now support Rust, the latter marking the first time a language beyond C was ever approved for Linux. The safety guarantees of Rust are particularly appealing for security-critical systems: leading governments now also recommend Rust [43,27].

<sup>&</sup>lt;sup>4</sup> Microsoft Azure Research, USA, protz@microsoft.com

Of course, despite being safer than C or C++, Rust programs are not immune to bugs and vulnerabilities. Case in point, between January 1, 2024 and January 1, 2025, 137 security advisories against Rust crates were filed on RUSTSEC, a vulnerability database for the Rust ecosystem maintained by the Rust Secure Code working group. These vulnerabilities arose due to several reasons: runtime errors leading to aborted executions (panic in Rust, e.g., after an out-of-bounds array access), implementation or design flaws, or even memory vulnerabilities when using Rust's unsafe escape hatch, which allows the use of C-like, unchecked pointer operations when Rust's borrow-based type system is too restrictive.

To enforce those properties that fall outside the scope of Rust's borrowchecker, a vibrant ecosystem of static analyzers [\[30](#page-13-0)[,4,](#page-12-3)[26\]](#page-13-3), model checkers [\[19,](#page-13-4)[38\]](#page-14-5) and deductive verification tools [\[25](#page-13-5)[,11,](#page-12-0)[21,](#page-13-1)[18,](#page-13-6)[2,](#page-12-1)[3,](#page-12-5)[12,](#page-12-2)[17\]](#page-13-7) has been proposed to reason about and analyze Rust programs. However, developing a new tool targeting Rust currently requires an important engineering effort to meaningfully and efficiently interact with the Rust compiler, rustc. First, Rust is a complex language, and just like many C analyses plug into libclang, Rust analyses need to plug into rustc: reimplementing a Rust frontend from scratch would be a significant undertaking. Unfortunately, the various intermediate representations (IRs) in rustc are optimized for speed and efficiency, not ease of consumption by analysis tools. Specifically, rather than provide a fully decorated abstract syntax tree (AST) with all available information, rustc instead exposes queries to, e.g., obtain the type of an expression only when needed. While this design allows for efficient incremental compilation, it makes life harder for tool authors, since they have to deal with additional levels of indirection, and information scattered across multiple global tables and IRs; this style of APIs requires deep knowledge of the compiler internals. Additionally, while sufficient for compilation, the information provided by the compiler sometimes needs to be expanded for analysis purposes. For instance, querying the trait solver only gives partial information about the trait instances used at a point in the code. Reconstructing this information requires additional, error-prone work from tool authors. Finally, the Rust compiler itself is not invoked in isolation; any non-trivial Rust project uses the Cargo build system, which collects dependencies, synthesizes rustc invocations with suitable library and include paths, and generally drives rustc. A realistic analysis tool must therefore hook itself onto Cargo, a non-trivial endeavor that again requires deep knowledge of Cargo and rustc.

To address these limitations, we present Charon, a Rust analysis framework providing an analysis-oriented interface to the Rust compiler and tooling, which allows tool authors to focus on the core of their analysis, rather than on mundane details of the Rust compiler internals. Our contributions are as follows. Through the development of a variety of tools atop rustc, we are of the opinion that many of MIR's design choices are unsuitable for analysis, such as: low-level patternmatching that switches over the enumeration tag; encoding bounds-checks semantics with assertions; a precompiled representation of constants as byte arrays; and many more. Our first contribution is thus the design of ULLBC (Unstructured Low-Level Borrow Calculus) and LLBC (Low-Level Borrow Calculus), two dual views over Rust's internals that offer a control-flow graph (CFG) and an AST respectively. Both preserve the low-level MIR semantics of moves, copies, and explicit borrows and reborrows, but reconstruct constants, shallow pattern matches, and checked operations, so as to provide a semantically simple view of MIR that is suitable for further analyses. LLBC is obtained from ULLBC via a Relooper-like control-flow reconstruction [\[33](#page-13-8)[,31\]](#page-13-9). Our second contribution is the engineering of Charon itself, and the accompanying ecosystem integration. We write a standalone, reusable infrastructure that allows a client to integrate cleanly with Cargo's build system. Furthermore, to expose clean ULLBC and LLBC representations (above), we hide away the complexity of querying the Rust compiler internals, thus offering usable APIs without the incidental complexity. Our third and final contribution is a series of case studies that not only informed the design of LLBC and ULLBC, but also served as an experimental validation of their wide-ranging applicability. We thus provide empirical evidence that the design choices of Charon are suitable for a wide variety of use-cases, supporting our claim that Charon is the swiss-army knife of Rust analysis.

Data-Availability. Charon is developed publicly on Github [\[8\]](#page-12-6) and released under an open-source license; to foster reproducibility, an artifact is available online [\[9\]](#page-12-7).

### 2 The Charon Framework

We now describe the architecture of both the Rust compiler and the Charon framework; Figure [1](#page-2-0) recaps the various steps in visual form.

![](_page_2_Figure_6.jpeg)

<span id="page-2-0"></span>Fig. 1. Architectural diagram of the Charon framework, its relationship to the Rust compiler, and to consumers.

#### 2.1 Background: the Rust Compiler

The Rust compiler pipeline relies on three ASTs after initial parsing: HIR ("Highlevel IR"), THIR ("Typed HIR"), and MIR ("Mid-level IR"). HIR is the result of expanding macros and resolving names. Then, in THIR, all type information is filled, and a first round of desugaring is performed, notably for reborrows, as well as automatic borrowing and dereferencing. At this stage, many fine points of semantics are still implicit: moves, copies, drops, control-flow of patterns, and many more, do not appear in this AST. MIR is where all these semantic details are made explicit. MIR is a CFG with a limited set of statements and terminators, making the semantics lower-level than in HIR and THIR. The Rust compiler features nearly 60 compilation passes [\[34\]](#page-13-10) operating on the MIR AST – a standard design choice, where in practice several phases rely on different subsets of MIR. The final step, after all optimizations have been run on MIR, consists in emitting LLVM bitcode, then handing off the rest of the compilation pipeline to LLVM itself. We now review our design choices, and explain how they facilitate the task of developing analyses for Rust.

#### 2.2 Charon Overview

As MIR explicits many fine points of semantics that make Rust hard to accurately model, it is a common starting point for verification tools [\[11,](#page-12-0)[19,](#page-13-4)[4,](#page-12-3)[29\]](#page-13-11), as well as compiler analyses such as borrow-checking, which were too error-prone on THIR [\[1,](#page-12-8)[24\]](#page-13-12). In particular, moves, copies, (re)borrows, and drops, the core of Rust's semantics, are all explicit in MIR: for instance, let x = &mut y; f(x) becomes, in MIR, let x = &mut y; f(move &mut(\*x)), so as to avoid invalidating x itself via a move-out. Other desugarings, e.g., for pattern-matches, which have a highly non-trivial semantics in THIR, also appear explicitly in MIR only. To allow a precise analysis of Rust programs, Charon therefore also operates on MIR.

ULLBC. From the MIR representation, Charon constructs a cleaned-up, decorated view called ULLBC. ULLBC is, like MIR, a CFG; but unlike MIR, ULLBC offers immediate contextual and semantic information ([§2.4\)](#page-4-0), and hides implementation-specific details ([§2.5\)](#page-6-0), while nevertheless exposing the entire Rust language. In particular, rather than have the user query rustc, e.g., to get type information about auxiliary data structures or to invoke the trait solver, ULLBC has all of this critical information directly attached to the CFG.

Additionally, ULLBC features several clean-up transformation passes that offer a more structured, semantic view of MIR. These passes, e.g., simplify patternmatching operating on low-level representation to replace them with high-level, ML-style pattern matches; transform a variety of desugarings of panic! to a single, unified statement, or pack dynamic checks for integer overflows with their corresponding arithmetic operation to simplify the semantics. We envision that consumers of ULLBC ultimately will decide whether these passes are fit for them; for instance, specific consumers might want to see explicit assertions for checked operations. Should they do so, we envision a general API where they can manually choose which reconstruction passes to enable.

LLBC. Charon then applies a control-flow reconstruction algorithm on a ULLBC CFG to generate an LLBC AST that materializes structured loops and branching. In practice, we reverse-engineer rustc's CFG construction, and recreate loops, conditionals, etc. out of the MIR basic blocks.

#### 2.3 Limitations

Charon already supports a sizable subset of Rust, as evidenced by our evaluation ([§3\)](#page-9-0). However some less-central features are not supported, which consist of: dynamic trait dispatch (dyn Trait), generic associated types, trait aliases, async, and impls in the return type of functions. To support analyzing crates that use such features, Charon was designed to be robust: a declaration that cannot be translated is marked as missing and the rest of the crate is translated as usual, resulting in a well-formed (if incomplete) (U)LLBC. So far, none of these missing features have impeded our case studies.

#### <span id="page-4-0"></span>2.4 Reconstructing Compiler Information

When operating on rustc, retrieving information needed for program analysis is tricky for two reasons. First, instead of exposing a fully-decorated representation, rustc relies on (poorly documented) lazy computations to query the compiler internals. One thus has to skim through the code of rustc itself to find which auxiliary function, given a program node, may retrieve the desired information. Second, and more importantly, some information can be partial or missing.

As an example, consider a Rust trait method call; to analyze it, we first need the instance of the corresponding Rust trait with its proper arguments (i.e., the instantiated impl), and the reference to the method including its arguments (in case the method is generic). Unfortunately, the concrete trait instance is not directly available in MIR. For instance, consider the snippet of code below.

```
fn clone_vec<T>(v : &Vec<T>) -> Vec<T> where T:Clone { v.clone() }
```

When compiling this code, rustc needs to assess that it is legal to call the clone method by querying the trait solver to find an instance of Clone for Vec<T>; in our case, this instance is the standard library Clone implementation for Vec<T : Clone> (which we will call CloneVec), composed with the local instance T : Clone received as input (which we will call CloneT).

The trait solver only needs to assess that there exists such an instance. However, when analyzing this code, we might want more precise information, namely that v.clone() uses exactly the implementation CloneVec composed with CloneT. Unfortunately, retrieving this information from rustc requires several non-trivial steps. First, we need to query the trait solver; to do so, one needs to handle several complex rustc concepts, such as its internal representation for binders or late-bound and early-bound regions. Worse, the information given by the trait solver is partial. The solver only tells us that v.clone() uses CloneVec composed with some instance of T : Clone which can be derived from the local where clauses of the function, without exhibiting this derivation. Reconstructing it is a non-trivial problem in general especially as some trait instances can be implied by other trait clauses in the presence of super traits.

Another issue stems from the input parameters given to function and method calls. Consider the following snippet of code.

```
fn f<V>(x : V);
fn g<V>(x : V) { f::<V>(x); }
trait Trait<U> { fn f<V>(x : V); }
fn h<T,U,V>(x:V) where T:Trait<U> { (T as Trait<U>)::f::<V>(x) }
```

When retrieving the list of generic parameters received by the call to the function f in g, rustc gives us V. However, when querying the parameters given to the method call Trait::f in h, rustc concatenates the parameters of the trait instance with the parameters given to the method itself, yielding T (for the implicit Self parameter), U, and V, where one only expects V. This confusing behavior is error-prone; as a consequence Charon retrieves and truncates the list of parameters through the following boilerplate code, which itself relies on several (omitted) auxiliary helpers that we introduced for this purpose (in red).

```
let (gens, source) = // Is this a function or method call?
 if let Some(assoc) = tcx.opt_associated_item(id) { ... // Omitted
  match assoc.container { // Trait "decl" or impl method call?
   AssocItemContainer::TraitContainer => { // Trait "decl" method call
    let num_cont_gens = tcx.generics_of(cont_id).own_params.len();
    let impl_expr = self_clause_for_item(s, &assoc, gens).unwrap();
    let method_gens = &gens[num_cont_gens..];
    (method_gens.sinto(s), Some(impl_expr)) }
   AssocItemContainer::ImplContainer => { // Trait impl method call
    let cont_gens = tcx.generics_of(cont_id);
    let cont_gens = gens.truncate_to(tcx, cont_gens);
    let mut comb_trait_refs = solve_req_traits(s, cont_id, cont_gens);
    comb_trait_refs.extend(std::mem::take(&mut trait_refs));
    trait_refs = comb_trait_refs;
    (gens.sinto(s), None) } } } else {(gens.sinto(s), None)}; // Fun call
```

There are many other technicalities to consider leading to boilerplate code; for instance retrieving the trait instances alone requires more than 600 lines of code. In contrast, Charon provides the following LLBC datatype, which directly exposes all relevant trait information with the properly truncated list of parameters. The information includes support for type and trait polymorphism, at the heart of Rust's generic programming facilities, whose representation relies on a novel, abstract language of trait clauses, parent clauses, self types and trait bounds. For instance, a trait might refer to a top-level implementation but also a local where clause (e.g., T : Clone), or a trait implied by an associated type (e.g., IntoIterator contains an associated type IntoIter : Iterator<...>).

```
struct FnPtr {
func: FunIdOrTraitMethodRef, // Function identifier
generics: GenericArgs, } // Generic parameters
enum FunIdOrTraitMethodRef {
Fun(FunId), // Top-level function
Trait(TraitRef, TraitItemName, ...), } // Trait method
struct TraitRef { kind: TraitRefKind, ... }
enum TraitRefKind {
TraitImpl(TraitImplId, GenericArgs), // Top-level impl
Clause(ClauseId), // Local where clause
ItemClause(Box<TraitRefKind>, ...), // Implied by assoc. type
```

Beyond trait resolution, Charon also reconstructs the control-flow by applying a Relooper-like algorithm, packages crates into easy-to-use structures, and optionally lifts trait associated types into type parameters while normalizing types which are known to be equal (because, e.g., of a clause T::Item = u32).

#### <span id="page-6-0"></span>2.5 Simplifying Representations

To efficiently compile Rust projects, rustc stores program information in a variety of representations, sometimes too low-level to be directly usable for analysis purposes. In particular, in MIR, constants are already compiled, meaning that instead of a struct value, one may be simply provided with an array of bytes already laid out. For instance, let us describe the process of retrieving the highlevel representation of an enumeration value which got compiled to a constant. We start from a mir::Const enumeration, over which we match, retrieving either a ty::Const if the constant is used in a type (e.g., it is used to instantiate a const generic), or a ConstValue if it doesn't. Diving further, from a ty::Const, in one case (there are many other cases) we get a ValTree; by using the type of the constant we learn that, as it is an abstract data type (ADT), we should call a specific rustc helper to turn it into a DestructuredConst (below), from which we can recursively reconstruct our enumeration value.

```
struct DestructuredConst<'tcx> {
  variant: Option<VariantIdx>,
  fields: &'tcx [ty::Const<'tcx>], }
```

The other cases are similarly complex, with many corner cases. In constrast, Charon provides the following unified, high-level representation for constants.

```
enum ConstantKind {
  Adt(Option<VariantId>, Vec<Constant>), ... /* Omitted */ }
struct Constant { value: ConstantKind, ty: Ty, }
```

Beyond constants, Charon also transforms other low-level representations into high-level, functional datatypes. This includes, e.g., simplifying the representation of names, reconstructing span information, removing the uses of the Steal datastructure which allows rustc to update definitions in-place through the compilation process at the cost of making some definitions unavailable if they are accessed in the wrong order, clarifying the use of binders by using an explicit and uniform treatment of parameters rather than, e.g., what rustc dubs "early bound" and "late bound" region variables, or simplifying trait implementations by turning default methods into regular methods.

#### 2.6 A Primer of LLBC

In the previous sections we presented the transformations performed by Charon to make the MIR easier to consume; let us now have a quick overview of the output of Charon, focusing on LLBC. In LLBC, a crate (TranslatedCrate, below) contains a crate name, the content of the source files, and the declarations, where each declaration is uniquely identified (with an id of type, e.g., TypeDeclId). We also compute the groups of mutually recursive declarations (not shown here) that we order topologically, as it is useful both for analysis and compilation purposes.

```
struct TranslatedCrate {
  crate_name: String, files: Vector<FileId, File>,
  type_decls: Vector<TypeDeclId, TypeDecl>,
  fun_decls: Vector<FunDeclId, FunDecl>, ... /* omitted */ }
```

Function declarations and signatures are straightforward. Function declarations contain a unique identifier, metadata for the declaration name, the span and the attributes, a signature, and an optional body which is omitted if Charon encountered an error or if the function was marked with the #[charon::opaque] attribute. Signatures simply contain the generic parameters, the list of input types, and the output type.

```
struct FunDecl {
 id: FunDeclId, meta: ItemMeta,
 signature: FunSig,
 body: Result<Body, Opaque>,
 ... /* omitted */ }
                                   struct FunSig {
                                    ... /* omitted */ ,
                                    generics: GenericParams,
                                    inputs: Vec<Ty>,
                                    output: Ty, }
```

Importantly, the generic parameters (GenericParams) contain all the information related to the bound variables (region variables, type variables, etc.) and the where clauses in a simple and explicit format. This type gathers in one place information which otherwise requires querying rustc several times, and is uniformly used by all the definitions (functions, types, traits declarations, etc.).

```
struct GenericParams {
 regions: Vector<RegionId, RegionVar>,
 types: Vector<TypeVarId, TypeVar>,
 const_generics: Vector<ConstGenericVarId, ConstGenericVar>,
```

```
trait_clauses: Vector<TraitClauseId, TraitClause>, // T : Clone
regions_outlive: Vec<RegionBinder<RegionOutlives>>, // 'a : 'b
types_outlive: Vec<RegionBinder<TypeOutlives>>, // T : 'a
trait_type_constraints: ..., } // T::Item = u32
```

The other definitions for types, traits, etc., all follow a similar model by containing a unique identifier, metadata (i.e., ItemMeta), generic parameters and an optional body; we omit them here. Skipping the definition of function bodies, which store the list of local variables as well as a block of statements, let us now look at the definition of LLBC statements. Statements have the expected kinds such as: assignments, function calls, returns, or loops. The Switch enumeration (not shown here) distinguishes if then elses, switches over integers, and matches over enumerations. We also preserve code spans and user comments.

```
enum StatementKind {
 Assign(Place, Rvalue),
 Call(Call),
 Abort(AbortKind), // panic
 Switch(Switch), Loop(Block),
 Return, Nop, Drop(Place),
 Break(usize), Continue(usize),
 ... /* omitted */ }
                                   struct Statement {
                                    span: Span,
                                    kind: StatementKind,
                                    comments: Vec<String>, }
                                   struct Block {
                                    span: Span,
                                    statements: Vec<Statement>, }
```

We finish this quick overview with function calls. We carefully wrote the Call structure so that all cases are grouped in one definition and are easy to distinguish. The important field is FnOperand, which covers the different cases, that is: the use of top-level functions, of trait methods, and of function pointers stored in local variables (e.g., because of the use of a anonymous functions).

```
struct Call {
 func: FnOperand,
 args: Vec<Operand>,
 dest: Place, }
enum FnOperand {
 Regular(FnPtr),
 Move(Place), }
                        struct FnPtr {
                         func: FunIdOrTraitMethodRef,
                         generics: GenericArgs, }
                        enum FunIdOrTraitMethodRef {
                         Fun(FunId), // top-level function
                         TraitMethod(...), // trait method }
```

When FnOperand refers to a top-level function or a trait method, it uses a FnPtr to bundle a function identifier with its generic arguments. When the FnPtr itself identifies a top-level function, it directly refers to its unique identifier, that we can use to, e.g., lookup the function definition from the TranslatedCrate shown above. When the FnPtr identifies a trait method call, it bundles a trait instance given by a TraitRef (see § [2.4\)](#page-4-0) together with the name of the method which is actually called.

We end our overview of LLBC here. The omitted parts of the AST follow a similar logic: we attempt to factor out definitions, store as much information as we can, including metadata, and make all information explicit.

#### 2.7 Interacting with the Rust Ecosystem

The build system of Rust, cargo, takes care of fetching dependencies, at the correct revision; building them recursively; and finally, invoking rustc on the current crate with include and library paths for all the required dependencies. To seamlessly integrate with existing Rust projects, Charon therefore directly reuses the cargo infrastructure.

To do so, the charon executable first invokes cargo; thanks to a special environment variable, cargo can be made to either call vanilla rustc (for dependency analysis), or our own variant of rustc, dubbed charon-driver, which we instrumented with additional hooks into the compiler. When run, charon-driver drives rustc, replacing the final compilation step to LLVM with a program analysis step, i.e., the Charon framework. From a user perspective, all these lowlevel implementation details are hidden, and all is needed is to call the charon executable from the root of the project (a.k.a. crate).

At the difference of cargo build, which produces an executable, calling charon produces a .(u)llbc file containing a straightforward serialization (currently in JSON) of the (U)LLBC. Any further analyses are to be performed off of those files; should the analysis itself be written in Rust, we engineered Charon so that the part that links against rustc lives in a separate crate from the rest (cleanups, CFG and AST representations, serialization and deserialization), avoiding the need for analysis tools to include the whole compiler toolchain.

We can also auto-generate (U)LLBC type declarations and deserializers for other languages beyond Rust; right now, we provide charon-ml, an OCaml library that can read back .(u)llbc files. OCaml is particularly-well suited to AST manipulations, and comes with convenient facilities, such as automatic visitors generation, which accelerates development of analysis tools. Adding support for a different language would only require a modicum of work.

#### 2.8 Implementing Charon

Our toolchain is made up of two parts: the Charon codebase itself, totaling 18kLoC excluding whitespace and comments, which constructs (U)LLBC and performs additional transformation passes, and the hax-frontend-exporter crate, developed in collaboration with the hax project [\[6\]](#page-12-9) and totaling 9kLoC, which directly consumes the output of rustc and performs most queries, as well as our constant simplification and custom trait resolution, which operate on both MIR and THIR, and which we believe to be useful independently of Charon as a companion to the compiler and thus package separately. The effort to write this whole project spanned 2 person-years.

### <span id="page-9-0"></span>3 Case Studies

Static Analyses. We implemented two static analyses on top of Charon. First, we ported Rudra, a recent static analyzer that detects potential memory safety issues in unsafe Rust programs by looking for a set of well-identified bug patterns [\[4\]](#page-12-3), so that it uses Charon rather than directly interacting with rustc. The port took us one day of work, confirming in particular that ULLBC provides all the needed information; to validate the analysis, we reran our port of Rudra on versions of crates used in the original paper's evaluation. Several of these crates do not compile anymore, due to the Rust ecosystem evolving and the projects not including .lock files, but we were nevertheless able to analyze 6 of the most popular crates considered in the initial paper, reidentifying vulnerabilities previously discovered.

We also implemented an analyzer to detect constant-time violations in cryptographic code through a flow-, field-, and context-sensitive taint analysis operating on LLBC. We ran our analysis on implementations from several cryptographic crates, including RustCrypto [\[35\]](#page-13-13), a port to safe Rust of the formally verified HACL<sup>⋆</sup> library [\[32,](#page-13-14)[39\]](#page-14-6), and an implementation of the recently standardized post-quantum ML-KEM [\[28\]](#page-13-15) cryptographic primitive in the libcrux formally verified cryptographic library [\[22\]](#page-13-16), totalling 88k LoC. Our taint analysis successfully shows that the considered implementations do not suffer from constant-time violations, as expected from widely-used or verified libraries, and rediscovers the KyberSlash timing attack in an earlier, unverified version of ML-KEM [\[5,](#page-12-10)[7\]](#page-12-11).

Deductive Verification. Aeneas [\[17,](#page-13-7)[16\]](#page-12-12) is a framework for verifying safe Rust programs, which works by generating models of Rust programs which are exported to a range of theorem provers. Aeneas relies on Charon to obtain the LLBC code and was the original motivation for implementing Charon; after realizing that many other tools were each reimplementing their own logic for interacting with rustc, we felt strongly that packaging and releasing a reusable component for this task would help current and future Rust tool authors.

Transpilation to C. Eurydice[5](#page-10-0) is a transpiler from Rust to C whose main motivation is to allow engineers to develop new code in Rust while still being able to deliver C code for legacy reasons. It is made up of about 5000 lines of OCaml code, including whitespace and comments, and consumes Rust code via Charon, translating LLBC into C. Eurydice particularly benefits from LLBC's design: the AST is small and structured, simplifying the translation, and move and copy operations, needed to correctly match the C semantics, are explicit.

Running Charon over Charon. We mentioned earlier that Charon exposes its (U)LLBC representations in a reusable format for use in other languages; the Charon codebase itself maintains an OCaml library to manipulate this format, used in Eurydice and Aeneas. Rather than author this library manually, we instead run Charon on itself to inspect the definitions of the LLBC and ULLBC type definitions written in Rust, and output appropriate OCaml type definitions, visitors and deserializers to read and manipulate (U)LLBC.

<span id="page-10-0"></span><sup>5</sup> <https://github.com/AeneasVerif/eurydice>

Third-Party Uses of Charon. While Charon is still recent, we can already report third-party uses of the framework. The Kani model checker [\[19\]](#page-13-4) recently added a backend that generates ULLBC so as to leverage Charon's control-flow reconstruction pass. RaRust [\[40\]](#page-14-7) is a linear resource bound analysis for Rust which uses (an earlier version of) Charon to retrieve the LLBC of Rust programs.

## 4 Related Work

To the best of our knowledge, the only other project that aims to provide a view over MIR suitable for a variety of tooling is Stable-MIR [\[36\]](#page-14-8). Much like Charon, Stable-MIR has its own representation of important Rust constructs and features strongly-typed identifiers. Unlike Charon, Stable-MIR is not in itself a standalone rustc driver; it is instead closer to a toolkit to write rustc drivers. While it does considerably simplify the interactions with the compiler by providing appropriate methods instead of out-of-band queries and hiding away the driver details, it is by design a thin wrapper over compiler internals. As such, it does not intend to clean up or reconstruct the CFG into an AST nor does it try to simplify constants or resolve traits as we do. Both projects have similar goals however, and may fruitfully collaborate in the future.

The Charon project is collaborating with other projects that have similar needs. For instance, hax [\[6\]](#page-12-9) and Charon share important components including their trait resolution system and simplification of constants, while Kani [\[19\]](#page-13-4) recently added a backend that generates ULLBC so as to leverage Charon's control-flow reconstruction pass. Generally, for historical reasons, many of the existing verifiers and/or Rust-based tools maintain their own equivalent functionality, in a less general form and more tailored to their own needs. We hope for the adoption of Charon to continue and plan to formalize a roadmap, governance model, and community, to make sure more tools and clients can rely on Charon.

Beyond Rust, several efforts have proposed intermediate representations that other tools can either target or consume. Most famously, the LLVM toolchain provides a common substrate for many source languages, usable for many analyses [\[14,](#page-12-13)[15,](#page-12-14)[13](#page-12-15)[,46\]](#page-14-9). While LLVM was initially intended as a compilation framework [\[20\]](#page-13-17), it now includes building blocks that significantly reduce the effort needed to develop new analyses, e.g., libraries for dominators or alias analysis; we intend to provide similar features for (U)LLBC. Runtimes for managed languages like the JVM and the .NET CLR have been targeted by many languages (e.g., Scala, Clojure, F#), and have in turn created a foundation for generalpurpose analyses (e.g., CLR Profiler, Abstract Interpretation for Java [\[23\]](#page-13-18)). Similarly to Charon, Emscripten, the LLVM backend for WASM, also performs some cleanups to reconstruct structured control flow with the Relooper algorithm, so as to target the more structured semantics of WASM [\[45\]](#page-14-10).

Acknowledgments. This work received funding from the France 2030 programs managed by the French National Research Agency under grant agreements ANR-22-PTCC-0001 and ANR-22-PETQ-0008 PQ-TLS.

### References

- <span id="page-12-8"></span>1. Github tracking issue for bugs fixed by the MIR borrow checker or NLL. [https:](https://github.com/rust-lang/rust/issues/47366) [//github.com/rust-lang/rust/issues/47366](https://github.com/rust-lang/rust/issues/47366)
- <span id="page-12-1"></span>2. Astrauskas, V., Müller, P., Poli, F., Summers, A.J.: Leveraging Rust types for modular specification and verification. In: Proceedings of the ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages and Applications (OOPSLA) (2019)
- <span id="page-12-5"></span>3. Ayoun, S.É., Denis, X., Maksimović, P., Gardner, P.: A hybrid approach to semiautomated rust verification. arXiv preprint arXiv:2403.15122 (2024)
- <span id="page-12-3"></span>4. Bae, Y., Kim, Y., Askar, A., Lim, J., Kim, T.: Rudra: finding memory safety bugs in rust at the ecosystem scale. In: Proceedings of the ACM SIGOPS 28th Symposium on Operating Systems Principles. pp. 84–99 (2021)
- <span id="page-12-10"></span>5. Bernstein, D.J., Bhargavan, K., Bhasin, S., Chattopadhyay, A., Chia, T.K., Kannwischer, M.J., Kiefer, F., Paiva, T., Ravi, P., Tamvada, G.: KyberSlash: Exploiting secret-dependent division timings in kyber implementations. Cryptology ePrint Archive, Paper 2024/1049 (2024), <https://eprint.iacr.org/2024/1049>
- <span id="page-12-9"></span>6. Bhargavan, K., Franceschino, L., Hansen, L.L., Kiefer, F., Schneider-Bensch, J., Spitters, B.: Hax - Enabling High Assurance Cryptographic Software. RustVerify (2024), [https://github.com/hacspec/hacspec.github.io/](https://github.com/hacspec/hacspec.github.io/blob/master/RustVerify24.pdf) [blob/master/RustVerify24.pdf](https://github.com/hacspec/hacspec.github.io/blob/master/RustVerify24.pdf)
- <span id="page-12-11"></span>7. Bhargavan, K., Kiefer, F., Tamvada, G.: Verified ML-KEM (kyber) in rust. [https:](https://cryspen.com/post/ml-kem-implementation/) [//cryspen.com/post/ml-kem-implementation/](https://cryspen.com/post/ml-kem-implementation/)
- <span id="page-12-6"></span>8. Charon Team: Charon github repository (2025), [https://github.com/](https://github.com/AeneasVerif/charon) [AeneasVerif/charon](https://github.com/AeneasVerif/charon)
- <span id="page-12-7"></span>9. Charon Team: Charon zenodo artifact (2025), [https://zenodo.org/records/](https://zenodo.org/records/15314373) [15314373](https://zenodo.org/records/15314373)
- <span id="page-12-4"></span>10. Cook, K.: [GIT PULL] Rust introduction for v6.1-rc1. [https://lore.kernel.](https://lore.kernel.org/lkml/202210010816.1317F2C@keescook/) [org/lkml/202210010816.1317F2C@keescook/](https://lore.kernel.org/lkml/202210010816.1317F2C@keescook/)
- <span id="page-12-0"></span>11. Denis, X., Jourdan, J.H., Marché, C.: Creusot: a foundry for the deductive verification of rust programs. In: International Conference on Formal Engineering Methods. pp. 90–105. Springer (2022)
- <span id="page-12-2"></span>12. Gäher, L., Sammler, M., Jung, R., Krebbers, R., Dreyer, D.: RefinedRust: A type system for high-assurance verification of Rust programs. Proceedings of the ACM on Programming Languages 8(PLDI), 1115–1139 (2024)
- <span id="page-12-15"></span>13. Grech, N., Georgiou, K., Pallister, J., Kerrison, S., Morse, J., Eder, K.: Static analysis of energy consumption for llvm ir programs. In: Proceedings of the 18th International Workshop on Software and Compilers for Embedded Systems. pp. 12–21 (2015)
- <span id="page-12-13"></span>14. Gritti, F., Pagani, F., Grishchenko, I., Dresel, L., Redini, N., Kruegel, C., Vigna, G.: Heapster: Analyzing the security of dynamic allocators for monolithic firmware images. In: In Proceedings of the IEEE Symposium on Security & Privacy (S&P) (May 2022)
- <span id="page-12-14"></span>15. Gurfinkel, A., Navas, J.A.: Abstract interpretation of llvm with a region-based memory model. In: International Workshop on Numerical Software Verification. pp. 122–144. Springer (2021)
- <span id="page-12-12"></span>16. Ho, S., Fromherz, A., Protzenko, J.: Sound borrow-checking for Rust via symbolic semantics. Proceedings of the ACM on Programming Languages 8(ICFP), 426–454 (2024)

- <span id="page-13-7"></span>17. Ho, S., Protzenko, J.: Aeneas: Rust verification by functional translation. Proceedings of the ACM on Programming Languages 6(ICFP), 711–741 (2022). <https://doi.org/10.1145/3547647>
- <span id="page-13-6"></span>18. Jung, R., Jourdan, J.H., Krebbers, R., Dreyer, D.: Rustbelt: Securing the foundations of the Rust programming language. In: Proceedings of the ACM Symposium on Principles of Programming Languages (POPL) (2018)
- <span id="page-13-4"></span>19. Kani Contributors: The Kani Rust Verified. [https://github.com/](https://github.com/model-checking/kani) [model-checking/kani](https://github.com/model-checking/kani)
- <span id="page-13-17"></span>20. Lattner, C., Adve, V.: LLVM: A compilation framework for lifelong program analysis & transformation. In: Proceedings of the International Symposium on Code Generation and Optimization (CGO) (2004)
- <span id="page-13-1"></span>21. Lattuada, A., Hance, T., Cho, C., Brun, M., Subasinghe, I., Zhou, Y., Howell, J., Parno, B., Hawblitzel, C.: Verus: Verifying Rust programs using linear ghost types. In: Proceedings of the ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages and Applications (OOPSLA) (2023). <https://doi.org/10.1145/3586037>
- <span id="page-13-16"></span>22. libcrux Contributors: libcrux - the formally verified crypto library. [https://](https://github.com/cryspen/libcrux/) [github.com/cryspen/libcrux/](https://github.com/cryspen/libcrux/)
- <span id="page-13-18"></span>23. Marx, S., Erdweg, S.: Abstract interpretation of java bytecode in sturdy. In: Proceedings of the 26th ACM International Workshop on Formal Techniques for Javalike Programs. pp. 17–22 (2024)
- <span id="page-13-12"></span>24. Matsakis, Niko: Introducing MIR. [https://blog.rust-lang.org/2016/04/19/](https://blog.rust-lang.org/2016/04/19/MIR.html) [MIR.html](https://blog.rust-lang.org/2016/04/19/MIR.html)
- <span id="page-13-5"></span>25. Merigoux, D., Kiefer, F., Bhargavan, K.: Hacspec: succinct, executable, verifiable specifications for high-assurance cryptography embedded in Rust. Technical report, Inria (Mar 2021), <https://inria.hal.science/hal-03176482>
- <span id="page-13-3"></span>26. Miri Contributors: Miri, an Undefined Behavior detection tool for Rust. [https:](https://github.com/rust-lang/miri) [//github.com/rust-lang/miri](https://github.com/rust-lang/miri)
- <span id="page-13-2"></span>27. National Security Agency: Software memory safety. [https://media.defense.gov/](https://media.defense.gov/2022/Nov/10/2003112742/-1/-1/0/CSI_SOFTWARE_MEMORY_SAFETY.PDF) [2022/Nov/10/2003112742/-1/-1/0/CSI\\_SOFTWARE\\_MEMORY\\_SAFETY.PDF](https://media.defense.gov/2022/Nov/10/2003112742/-1/-1/0/CSI_SOFTWARE_MEMORY_SAFETY.PDF) (2022)
- <span id="page-13-15"></span>28. NIST: Module-lattice-based key-encapsulation mechanism standard. [https://](https://csrc.nist.gov/pubs/fips/203/final) [csrc.nist.gov/pubs/fips/203/final](https://csrc.nist.gov/pubs/fips/203/final) (2024)
- <span id="page-13-11"></span>29. Nitin, V., Mulhern, A., Arora, S., Ray, B.: Yuga: Automatically detecting lifetime annotation bugs in the rust language (2023), <https://arxiv.org/abs/2310.08507>
- <span id="page-13-0"></span>30. Nitin, V., Mulhern, A., Arora, S., Ray, B.: Yuga: Automatically detecting lifetime annotation bugs in the rust language. IEEE Transactions on Software Engineering (2024)
- <span id="page-13-9"></span>31. Peterson, W.W., Kasami, T., Tokura, N.: On the capabilities of while, repeat, and exit statements. Communications of the ACM 16(8), 503–512 (1973)
- <span id="page-13-14"></span>32. Polubelova, M., Bhargavan, K., Protzenko, J., Beurdouche, B., Fromherz, A., Kulatova, N., Zanella-Béguelin, S.: HACLxN: Verified generic SIMD crypto (for all your favourite platforms). In: Proceedings of the ACM Conference on Computer and Communications Security (CCS) (2020)
- <span id="page-13-8"></span>33. Ramsey, N.: Beyond relooper: recursive translation of unstructured control flow to structured control flow (functional pearl). Proceedings of the ACM on Programming Languages 6(ICFP), 1–22 (2022)
- <span id="page-13-10"></span>34. Rust Compiler Team: Implementors of MirPass. [https://doc.rust-lang.org/](https://doc.rust-lang.org/nightly/nightly-rustc/rustc_mir_transform/pass_manager/trait.MirPass.html#implementors) [nightly/nightly-rustc/rustc\\_mir\\_transform/pass\\_manager/trait.MirPass.](https://doc.rust-lang.org/nightly/nightly-rustc/rustc_mir_transform/pass_manager/trait.MirPass.html#implementors) [html#implementors](https://doc.rust-lang.org/nightly/nightly-rustc/rustc_mir_transform/pass_manager/trait.MirPass.html#implementors) (2024)
- <span id="page-13-13"></span>35. RustCrypto maintainers: Rust Crypto - cryptographic algorithms written in pure rust. <https://github.com/RustCrypto>

- <span id="page-14-8"></span>36. Stable MIR contributors: Stable MIR: Define a compiler intermediate representation usable by external tools. [https://github.com/rust-lang/](https://github.com/rust-lang/project-stable-mir) [project-stable-mir](https://github.com/rust-lang/project-stable-mir)
- <span id="page-14-2"></span>37. StackOverflow: 2023 developer survey. [https://survey.stackoverflow.co/2023/](https://survey.stackoverflow.co/2023/#section-admired-and-desired-programming-scripting-and-markup-languages) [#section-admired-and-desired-programming-scripting-and-markup-languages](https://survey.stackoverflow.co/2023/#section-admired-and-desired-programming-scripting-and-markup-languages) (2023)
- <span id="page-14-5"></span>38. Stateright Contributors: Stateright, a model-checker for implementing distributed systems. <https://github.com/stateright/stateright>
- <span id="page-14-6"></span>39. The HACL\* Team: A preliminary version of HACL\* extracted to \*safe\* Rust. <https://github.com/hacl-star/hacl-star/pull/918>
- <span id="page-14-7"></span>40. The RaRust Development Team: Rarust (2025), [https://github.com/Mepy/](https://github.com/Mepy/rarust-oopsla25) [rarust-oopsla25](https://github.com/Mepy/rarust-oopsla25)
- <span id="page-14-0"></span>41. The Register: In Rust we trust: Microsoft Azure CTO shuns C and C++. [https:](https://www.theregister.com/2022/09/20/rust_microsoft_c/) [//www.theregister.com/2022/09/20/rust\\_microsoft\\_c/](https://www.theregister.com/2022/09/20/rust_microsoft_c/) (2022)
- <span id="page-14-3"></span>42. The Register: Microsoft is busy rewriting core Windows code in memory-safe Rust. [https://www.theregister.com/2023/04/27/microsoft\\_windows\\_rust/](https://www.theregister.com/2023/04/27/microsoft_windows_rust/) (2023)
- <span id="page-14-4"></span>43. The White House: Back to the Building Blocks: a Path Toward Secure and Measurable Software. [https://www.whitehouse.gov/wp-content/uploads/2024/02/](https://www.whitehouse.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf) [Final-ONCD-Technical-Report.pdf](https://www.whitehouse.gov/wp-content/uploads/2024/02/Final-ONCD-Technical-Report.pdf)
- <span id="page-14-1"></span>44. Verdi, S.: Why rust is the most admired language among developers. [https://github.blog/](https://github.blog/2023-08-30-why-rust-is-the-most-admired-language-among-developers/) [2023-08-30-why-rust-is-the-most-admired-language-among-developers/](https://github.blog/2023-08-30-why-rust-is-the-most-admired-language-among-developers/) (2023)
- <span id="page-14-10"></span>45. Zakai, A.: Emscripten: an llvm-to-javascript compiler. In: Proceedings of the ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages and Applications (OOPSLA) (2011)
- <span id="page-14-9"></span>46. Zhao, J., Nagarakatte, S., Martin, M.M., Zdancewic, S.: Formalizing the llvm intermediate representation for verified program transformations. In: Proceedings of the 39th annual ACM SIGPLAN-SIGACT symposium on Principles of programming languages. pp. 427–440 (2012)