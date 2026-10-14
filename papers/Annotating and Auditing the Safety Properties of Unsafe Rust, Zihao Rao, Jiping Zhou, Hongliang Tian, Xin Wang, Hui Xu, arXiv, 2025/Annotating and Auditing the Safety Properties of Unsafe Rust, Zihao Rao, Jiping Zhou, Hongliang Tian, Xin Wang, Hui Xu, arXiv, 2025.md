                                         Annotating and Auditing the Safety Properties of Unsafe Rust
                                         ZIHAO RAO, Fudan University, China
                                         JIPING ZHOU, Independent Researcher, China
                                         HONGLIANG TIAN, Ant Group, China
                                         XIN WANG, Fudan University, China
                                         HUI XU∗ , Fudan University, China
                                         In Rust, unsafe code is the sole source of potential undefined behaviors. To avoid misuse, Rust developers should
arXiv:2504.21312v2 [cs.PL] 25 Apr 2026




                                         clarify the safety properties for each unsafe API. However, the community currently lacks a key standard for
                                         safety documentation: existing safety comments in the source code and safety documentation can be ad hoc
                                         and incomplete. This paper presents a tag-centric methodology for auditing the consistency and completeness
                                         of safety documentation. We first derive a taxonomy of Safety Tags to formalize natural-language requirements.
                                         Second, because API soundness frequently relies on struct invariants, we propose a set of empirical rules to
                                         systematically audit the structural consistency of safety documentation. We implemented this methodology in
                                         safety-tool, a static linter that automatically enforces structural consistency between local safety annotations
                                         and callee requirements. Our approach was applied to the Rust standard library, fixing documentation issues
                                         on 27 APIs with 61 safety tags and identifying safety tags that are applicable to 96.1% of the public unsafe APIs
                                         in libstd. Furthermore, we have formalized the tagging idea through a Rust RFC to the wider community. We
                                         believe that the approach establishes a standardized practice of safety documentation and helps significantly
                                         reduce safety perils.
                                         Additional Key Words and Phrases: Rust, unsafe code, safety property

                                         1   Introduction
                                         Rust is a systems programming language with strong memory-safety guarantees. Nevertheless,
                                         low-level operations such as raw-pointer dereference and unchecked memory manipulation remain
                                         unavoidable in systems software, and they continue to be an important source of safety bugs [27,
                                         35, 45]. Rust prevents undefined behavior as long as programmers remain within Safe Rust, where
                                         ownership, borrowing, and lifetime rules are enforced statically [50]. By design, the Rust compiler
                                         withholds its safety guarantees within unsafe blocks; therefore, the burden of upholding safety
                                         invariants shifts primarily to the developer when using unsafe code [34]. While guidelines such as
                                         the Rustonomicon [34] exist, achieving sound encapsulation is still prone to errors, as it requires
                                         that developers carefully reason about subtle safety invariants across usage boundaries. As a result,
                                         unsoundness often lurks in functions that contain internal unsafe code, making it a characteristic
                                         Rust-specific bug class. [38, 50]. Such issues could undermine Rust’s memory safety feature if they
                                         are not properly addressed. Therefore, the memory safety of Rust ultimately depends on the correct
                                         usage of unsafe code.
                                            In this setting, safety documentation plays a critical role: each unsafe API should clearly specify
                                         its safety requirements in its documentation. Auditing such documentation is therefore essential
                                         for identifying missing or misstated requirements. In practice, however, both establishing correct
                                         safety documentation and maintaining it over time remain difficult for three main reasons. First,
                                         this audit is non-trivial because the relevant requirements are often not presented in a formal,
                                         uniform, and directly checkable form. Instead, they may be scattered across comments, cross-
                                         references, and side-effect warnings [10], and similar requirements may be expressed differently
                                         ∗ Corresponding author


                                         Authors’ Contact Information: Zihao Rao, zhrao25@m.fudan.edu.cn, Fudan University, China; Jiping Zhou, zjp1137967378@
                                         gmail.com, Independent Researcher, China; Hongliang Tian, tate.thl@antgroup.com, Ant Group, China; Xin Wang, xinw@
                                         fudan.edu.cn, Fudan University, China; Hui Xu, xuh@fudan.edu.cn, Fudan University, China.


                                                                                                            , Vol. 1, No. 1, Article . Publication date: April 2026.
2                                                          Zihao Rao, Jiping Zhou, Hongliang Tian, Xin Wang, and Hui Xu


across APIs. Auditors therefore often need to reconstruct the intended contract before they can
assess whether the documentation is correct and complete. Second, the safety requirements that
should be documented for an API are not always determined locally. For example, the soundness of a
safe method may depend on struct invariants established by constructors, and an unsafe constructor
may therefore need to document the conditions required to establish or preserve those invariants.
Auditing the documentation thus often requires tracing safety obligations across multiple functions
and data structures rather than examining each API in isolation. Third, even after an audit has
been completed, software evolution can introduce new safety requirements or alter existing ones,
creating hidden risks for downstream users. When the safety contract of an internal unsafe API
changes, its downstream callers may also adapt accordingly. Because Rust’s type signatures do not
encode such documentation-level obligations, and the compiler provides no warning when they
change, downstream code may remain unaware of newly introduced requirements and omit the
corresponding checks, ultimately leading to undefined behavior.
   To address these challenges, we propose an auditing methodology that combines human semantic
judgment with automated structural analysis1 . The methodology comprises three core components:
(1) a taxonomy of safety tags for representing safety requirements; (2) structural dependency
extraction for APIs that should be audited together; and (3) safety-tool for checking whether
the resulting documentation remains consistent as the code evolves. Together, these components
define a four-phase workflow: deriving safety tags, identifying structurally related APIs, auditing
their documentation with explicit rules, and continuously checking documentation consistency.
   We begin by introducing an annotation language that translates informal safety comments in the
Rust standard library into machine-checkable safety tags. While contract-based approaches [1, 22,
23] offer one path toward formalizing safety obligations, they are typically designed for automated
proving rather than lightweight documentation. In our framework, each safety requirement is
defined as a parameterized tag, tag(args) ↦→ expression(args) (Table 2), together with an
explicit contractual role such as precondition, hazardous state, or optional condition. Based on
Rust’s UB documentation [34, 39], we derive 21 primitive safety tags across five categories: layout,
pointer validity, content, alias, and contextual. These tags cover 96.1% of public unsafe APIs in the
Rust standard library, excluding platform-specific intrinsics that lack generalizable requirements.
   We then extract structural dependencies to assemble Audit Units, each centered on a target
API and its associated constructors. This allows auditors to track how safety tags are handled,
delegated, and maintained across call chains and object construction. Within each audit unit, we
apply empirical audit rules to check documentation consistency at three layers: immediate call-site
logic, invariant initialization, and state exposure.
   To maintain audit validity as the software evolves, we developed safety-tool, an IDE-integrated
static linter. This tool can expand structured safety tags into human-readable documentation and
check consistency between caller annotations and callee requirements. Furthermore, we have
submitted a Rust RFC [43] to push these annotations toward ecosystem-wide standardization and
tool support.
   We evaluate the methodology through an empirical audit of the Rust standard library. We
translate informal safety comments into formal tags, extract structural dependencies to infer the
safety obligations in the source code, and compare these inferred obligations with the existing
documentation to identify inconsistencies. This process uncovers 27 APIs with 61 defective safety
tags. To date, the official Rust project has already confirmed and merged our fixes for all of these
tags.
   In summary, this paper makes the following contributions.

1 https://github.com/safer-rust/safety-tags



, Vol. 1, No. 1, Article . Publication date: April 2026.
Annotating and Auditing the Safety Properties of Unsafe Rust                                                         3


• We derive a taxonomy of 21 safety tags from the Rust standard library and propose empirical audit
  rules that use these tags to check the consistency and completeness of API safety documentation.
• We implement safety-tool, a static linter that enforces tag consistency between caller annotations
  and callee requirements, and submit a formal Rust RFC to integrate the system into the Rust
  ecosystem.
• We audit the Rust standard library, identify documentation defects in 27 APIs involving 61 safety
  tags, and contribute fixes that have all been merged into the official Rust project, reducing the
  potential for unsafe API misuse in practice.

2     Safety Promise and Unsafety Perils of Rust
2.1    Memory Safety of Rust
As a system language, Rust facilitates fine-grained memory management and efficiency with raw
pointers and low-level controls. Their full elimination is impossible by design in unsafe blocks,
which allow developers to bypass the compiler’s checks. Moreover, the undecidability of precise
pointer analysis makes mechanical verification of unsafe code extremely difficult [18, 21]. Rust’s
safety promise is that “the program should not exhibit undefined behaviors if developers do not use
unsafe code” [50]. This safety model relies on the interplay between two modes: Safe Rust and
Unsafe Rust.

2.1.1 Safe and Unsafe Rust. Safe Rust achieves the promise of safety through several novel features,
including ownership and lifetimes. In safe Rust, each value has an owner, and ownership can be
borrowed either mutably or immutably. The compiler mandates exclusive mutability: if a value has
a mutable reference, it cannot be aliased. It can avoid the tricky pointer analysis problems but at
the cost of flexibility. For instance, implementing a doubly linked list in safe Rust is challenging
because it requires multiple mutable references to the same node.
   To regain flexibility, Rust permits developers to bypass safety rules via unsafe code. Common
unsafe operations include dereferencing raw pointers, calling unsafe functions, accessing mutable
static variables, and accessing union fields. Notably, implementing an unsafe trait is different
because it signifies that the implementation must maintain extra invariants [7]. Since the compiler
does not guarantee memory safety in unsafe blocks, developers bear the responsibility for potential
risks. Unsafe Rust thus complements safe Rust by enabling low-level control and interoperability
in systems contexts such as embedded systems [45] and OS development [35, 36, 48].

2.1.2 Unsafe Code Encapsulation. As unsafe code is often unavoidable, encapsulating it is es-
sential to limit risk propagation. The Rust community advocates hiding unsafe code behind safe
abstractions [2, 34, 35], a practice known as interior unsafe [37, 38] where a safe function contains
unsafe code and manages all potential undefined behaviors internally. For example, in Figure 1, the
method St2::get() is safe despite calling the unsafe slice::from_raw_parts() inside, because
St2’s unsafe constructor functions must be ensured to uphold safety for themselves and the safe
St2::get(). This pattern prevents unsafety from leaking and is widely used in Rust libraries.

2.1.3 Modularized Safety. Rust provides visibility control to prevent unauthorized access [40]. A
data structure or module is considered to be sound if using its public APIs without unsafe code
does not cause undefined behavior. Accessing public fields should therefore be conducted with
caution, so as not to cause undefined behavior in methods or compromise module safety. Unsafe
fields [41] are an effort to enhance the safety of field access within or across modules.

                                                               , Vol. 1, No. 1, Article . Publication date: April 2026.
4                                                                                            Zihao Rao, Jiping Zhou, Hongliang Tian, Xin Wang, and Hui Xu


    Challenge 1: Safety Requirements are Informal and Fragmented   Challenge 2: Safety Obligations Span Function Boundaries       Challenge 3: Safety Documentation Lacks Automated Enforcement


         API Safety Doc (std::slice::from_raw_parts)                                                                                crate v1.0                                 Downstream User

                                                                     1 use std::ptr::read_unaligned;                               /// # Safety:                              pub fn foo(bytes: &[u8]) {
                                                                     2 // use std::ptr::read;                                      /// `ptr` is valid for reads of 8 bytes.
                                                                                                                                                                                 let ptr = bytes.as_ptr();
                                                                     3                                                             /// The bytes at `ptr` are initialized.
                                                                                                                                                                                 if bytes.len() > 8{
                                                                     4 struct WordAt {                                             pub unsafe fn new_unchecked(
                                                                                                                                                                                    let wa = unsafe {
                                                                                                                                      p: *const u8) -> Self
                                                                     5   pub ptr: *const u8,                                                                                          WordAt::new_unchecked(ptr);
                                                                     6 }                                                           pub fn load_as_u64(&self) -> u64 {
                                                                                                                                                                                    }
               Pointer Validity Doc                                  7                                                                                                              let r = wa.load_as_u64();
                                                                                                                                      unsafe { read_unaligned(
                                                                                                                                                                                 }
                                                                     8 impl WordAt {                                                     self.ptr as *const u64)
                                                                                                                                                                                 ...
                                                                     9                                                                }
                                                                                                                                                                              }
                                                                    10   /// # Safety:                                             }
                                                                    11   /// `ptr` is valid for reads of 8 bytes.
                                                                    12   /// The bytes at `ptr` are initialized.
                                                                                                                                        v1.0->v2.0: switches to ‘ptr::read’
                                                                    13   pub unsafe fn new_unchecked (ptr: *const u8) -> Self {
                                                                    14      Self { ptr }
                   Pointer Provenance Doc
                                                                    15   }                              State Dependency
                                                                                                                                    crate v2.0                                 Downstream User
                                                                    16
                                                                    17   pub fn load_as_u64(&self) -> u64 {
                                                                    18      unsafe {                                               /// # Safety:                              pub fn foo(bytes: &[u8]) {
                                                                    19        read_unaligned(self.ptr as *const u64)               /// `ptr` is valid for reads of 8 bytes.
                                                                                                                                                                                 let ptr = bytes.as_ptr();
                      Allocation Doc                                                                                               /// The bytes at `ptr` are initialized.
                                                                    20      }                                                      /// ptr should be aligned to 8.               if bytes.len() > 8{
                                                                    21   }                                                         pub unsafe fn new_unchecked(                     let wa = unsafe {
                                                                                                                                      p: *const u8) -> Self                           WordAt::new_unchecked(ptr);
                                                                    22 }
                                                                                                                                                                                    }
                                                                                                                                   pub fn load_as_u64(&self) -> u64 {               let r = wa.load_as_u64();
                                                                                                                                      unsafe { read(                             }
                                                                                                                                         self.ptr as *const u64)                 ...
                                                                                                                                      }                                       }
                                                                                                                                   }




                                                           Fig. 1. Challenges of standard audit workflow.


2.2           Motivation: Audit Objectives and Challenges
As previously discussed, Rust allows unsafe blocks for low-level control, making it a focus for
system soundness. While existing research uses automated tools to analyze code logic [23, 47, 49],
verifying whether documentation matches code requirements still depends on manual auditing.
This section defines the objectives of documentation auditing and identifies three challenges in the
current workflow.
2.2.1 Audit Objective. The objective of documentation auditing is to check whether the safety
requirements are correct and complete. An unsafe API is sound if it prevents undefined behavior
when the caller meets its safety requirements. This requires checking both the code and the
safety documentation. The documentation serves to formalize and expose this underlying contract.
Incomplete documentation increases the risk of API misuse. Listing 1 demonstrates a sound example.
The soundness of create_non_null_ptr_unchecked is conditional: it guarantees safety only if
the caller strictly adheres to the documented contract that ptr must be non-null.
Listing 1. A simple case of unsafe API soundness. The unsafe function propagates the non-null requirement
to the caller.
     1     /// # Safety: `ptr` must be non-null.
     2     pub unsafe fn create_non_null_ptr_unchecked(ptr: *mut u8) -> NonNull<u8> {
     3         unsafe { NonNull::new_unchecked(ptr) }
     4     }



2.2.2 Challenges of Standard Audit. The standard auditing workflow requires auditors to exam-
ine internal unsafe operations within an API to determine the safety requirements. They must
then check whether the API satisfies these requirements internally or declares them in its public
documentation. However, as shown in Figure 1, this manual process faces three challenges.
   Challenge 1: Safety Requirements are Informal and Fragmented. The first challenge is that existing
safety documentation does not provide an immediate basis for determining whether an API’s
documented contract is correct and complete (Figure 1, left). This difficulty has two concrete
causes. First, relevant conditions are often distributed across safety comments, cross-references,
and other sections. For example, ambiguous phrases such as valid pointer in the documentation of
slice::from_raw_parts require auditors to follow chains of hyperlinks to recover the intended
constraints. Second, safety requirements are not documented in a uniform style [10]. Some APIs
state preconditions (e.g., non-null requirement in NonNull::new_unchecked ), while some merely

, Vol. 1, No. 1, Article . Publication date: April 2026.
Annotating and Auditing the Safety Properties of Unsafe Rust                                                         5


imply constraints through side-effect warnings (e.g., the double-free warning in Box::from_raw ).
This inconsistency makes auditors rely on subjective interpretation to reconstruct the contracts.
   Challenge 2: Safety Obligations Span Function Boundaries. The safety of an API often depends
on the internal state of its struct. As shown in Figure 1, WordAt::new_unchecked(ptr) only stores a
raw pointer, while the later safe method load_as_u64() internally calls read_unaligned(self.ptr
as *const u64). Therefore, the safety documentation of the constructor cannot be written
from the local code of new_unchecked alone. It should also cover the assumptions introduced by
load_as_u64(), such as that the 8 bytes at ptr are readable and initialized. In other words, when
auditing new_unchecked, auditors have to infer the obligations it should declare from later uses
of the stored state, rather than inspect the constructor in isolation. Because these obligations are
propagated through shared struct state, function-local inspection or call-graph analysis may not
fully recover the safety requirements of a single API.
   Challenge 3: Safety Documentation Lacks Automated Enforcement. The third challenge is that
changes in safety documentation are not flagged automatically. As shown in Figure 1, in crate v1.0,
load_as_u64() uses read_unaligned, so the documentation of new_unchecked(ptr) only needs
to state that the 8 bytes at ptr are readable and initialized. In crate v2.0, the API signature remains
unchanged, but the internal implementation switches to ptr::read. The constructor documentation
must therefore additionally require that ptr be 8-byte aligned. Both versions are reasonable:
the change comes from the evolution of the crate’s internal unsafe implementation. However,
downstream users may still keep the old wrapper. In Figure 1, foo still checks only bytes.len()
> 8 and does not enforce alignment. Since the compiler cannot detect such documentation-level
contract changes, this kind of mismatch can be easily missed during evolution.

3   Overview of Tag-Centric Audit Methodology
To address these challenges, we propose a tag-centric auditing methodology. In Rust, unsafe blocks
are the sole source of undefined behavior (UB) [17]. Therefore, the auditing task is to check how
the safety obligations are handled. An API must either encapsulate these obligations through
internal checks to remain safe, or explicitly annotate them through documentation. Based on this
principle, our approach introduces a four-step workflow (Figure 2) that combines manual semantic
analysis with automated dependency tracking. Specifically, it transforms informal documentation
into machine-checkable semantic tags and traces their propagation across the codebase to verify
that all safety obligations are correctly handled.
   Phase 1: Tag Derivation and Dependency Extraction. This phase prepares the semantic and
structural basis for the audit. First, we derive a taxonomy of safety tags from natural-language
documentation. This step transforms informal requirements into formal, parameterized tags. Second,
we extract structural dependencies from the source code, tracking call graphs and object flows to
guide the analysis.
   Phase 2: Audit Unit Construction. Based on the extracted dependencies, we group related
APIs to construct audit units. This defines the exact scope of documentation auditing. Concurrently,
we annotate unsafe APIs with the derived safety tags, turning abstract properties into concrete
audit targets in the source code.
   Phase 3: The Tag-Centric Auditing. In this phase, auditors examine each audit unit using
empirical rules. They verify whether the code logic internally satisfies the safety tags or correctly
delegates them to the caller’s documentation. Inconsistencies or missing documentation are then
reported and fixed.
   Phase 4: Automated Enforcement. To prevent documentation from becoming outdated as
software evolves, we introduce safety-tool as a static linter. It automatically verifies the safety

                                                               , Vol. 1, No. 1, Article . Publication date: April 2026.
6                                                                                             Zihao Rao, Jiping Zhou, Hongliang Tian, Xin Wang, and Hui Xu


     LEGEND:                Automated Analysis (Tool)               Semantic Judgment (Human)

                       Phase 1: Specify Tags &                  Phase 2: Segment Units &                   Phase 3: Tag-Centric                     Phase 4: Continuing
                        Extract Dependencies                         Annotate Tags                             Audit Loop                              Enforcement
    Tool Assistant




                                           Context Extractor                                  Assemble          Audit Unit
                                     ➢ Call Graph Extraction                                    Units            Target API                                 Safety-Tool
                                     ➢ Constructor Identification
                                                                               Structural                   Constructors (Option)
                                     ➢ Object Flow Analysis                                                                             Annotated
                                                                             Dependencies
                     Source Code                                                                                                          Code
                                                                                        Annotate
                                                                                       Unsafe API                                     #[safety::checked]
                                                                                                                                         …
    Human Effort




                                         Safety Tag Derivation                                                                                             Audited & Checkable
                                    ➢ Semantic Extraction and Decoupling                                                                                        Codebase

                                    ➢ Bottom-Up Synthesis                                                        Soundness
                                    ➢ Parameterized Specification                                                  Verdict
                                                                               Safety Tags
                        Safety                                                Specification                                         Bug Report /
                      Documents                                                                                                       Doc Fix




Fig. 2. General methodology of tag-centric audit. The methodology yields a safety tag set for the Rust
standard library and extracts structural dependencies to assemble audit units, with continuous enforcement
provided by safety-tool.


tags between callers and callees, ensuring continuous alignment between upstream documentation
and downstream code implementations.
  Roadmap. The remainder of this paper details the components of this methodology, using the
Rust standard library as a comprehensive case study. Section 4 defines the taxonomy of safety tags
derived from the standard library (challenge 1). Section 5 elaborates on the audit unit construction
and the empirical audit rules (challenge 2). Section 6 presents the tool implementation and the RFC
for community standardization (challenge 3). Finally, Section 7 evaluates the effectiveness of our
methodology through an empirical audit of the Rust standard library.

4                    Unsafety Genesis and Annotation
To formalize safety requirements, we analyze the official undefined behavior (UB) documentation
and the safety comments in the Rust standard library. Based on the UB rules, we derive 21 safety
tags across five categories to represent these requirements.

4.1                   Characterizing Undefined Behaviors in Rust
According to the official Rust specification in the Rust Nomicon [34] and the Rust Reference [39],
programmers should avoid undefined behavior. If a program executes an undefined operation, the
compiler’s correctness guarantees become invalid. To establish a basis for our safety tag derivation,
we classify undefined behaviors from these specifications into four categories, each encapsulating
a core dimension of Rust’s safety model, as summarized in Table 1.
4.1.1 Memory and Pointer Safety. This category is the foundational layer of Rust’s safety model,
governing low-level memory accesses and pointer manipulations. Violations in this domain include
accessing dangling pointers or memory outside a single live allocation, performing misaligned
memory accesses, exceeding valid bounds during pointer arithmetic or collection indexing, and
permitting unsynchronized concurrent modifications that lead to data races in shared memory.
4.1.2 Aliasing Rule Violations. Aliasing Rule Violations target Rust’s unique ownership system,
which the compiler leverages to enable strong optimizations and safety guarantees. This encom-
passes breaches of the exclusivity guarantee for mutable references (&mut T) and the immutability
invariant for shared references (&T), except within the UnsafeCell.

, Vol. 1, No. 1, Article . Publication date: April 2026.
Annotating and Auditing the Safety Properties of Unsafe Rust                                                            7


                              Table 1. Taxonomy of Undefined Behaviors in Rust.

 Category                       Specific Behaviors
 Memory/Pointer Safety        Dangling and Illegal Access / Alignment Violation / Out-of-Bounds Access / Data Race
 Aliasing Rules               Pointer Aliasing Violation / Immutable Mutation
 Value Validity               Invalid Values / Uninitialized Memory
 Runtime/External Interaction FFI Violation / Platform Features / Runtime Violations / Inline Assembly



4.1.3 Invalid Value Production. Invalid Value Production addresses type-level validity invariants
that must be maintained throughout program execution. This includes creating values with illegal
bit patterns (such as invalid bool, char, or enum discriminants) and reading uninitialized memory
for types with restricted value sets.
4.1.4 Runtime and External Interaction. This category covers violations of the execution envi-
ronment’s contracts, including foreign function interface (FFI) conventions, compiler intrinsics,
platform-specific features, and runtime assumptions.

4.2   Derivation of Safety Tags
 Solution to Challenge 1 We introduce a tag-derivation workflow to extract safety tags from
natural-language documentation. This process uses manual semantic analysis to translate informal
comments into formal contracts based on Rust’s memory model.
4.2.1 Constraint Extraction and Decoupling. We reviewed the public unsafe API documentation in
the standard library. To resolve nested or implied constraints, we traced cross-references to their base
definitions. For example, the ambiguous phrase "pointer must be valid" resolves to dereferenceable
for non-zero-sized types. This property further breaks down into specific constraints like "must
not be dangling" and "must lie within the allocation range".
4.2.2 Taxonomy Mapping. We categorized these constraints based on the UB types they prevent
(Table 1). This resulted in a five-part taxonomy: Layout, Pointer, Content, Alias, and Contextual.
We separated Layout from Pointer for finer granularity, and aligned Content and Alias with
value validity and aliasing rules. Additionally, we introduced the Contextual category for state-
dependent invariants, replacing the rarely used external category.
4.2.3 Bottom-Up Synthesis. We grouped recurring constraints into unified safety tags by a bottom-
up analysis. For example, core::num::unchecked_add requires that self + rhs does not overflow,
while core::slice::from_raw_parts requires the slice size to not exceed isize::MAX. Since both
enforce numerical bounds, we represent them with a single ValidNum tag. All derived tags were
cross-validated by two authors to ensure consistency.
4.2.4 Parameterized Specification. Finally, we add context-specific arguments to the tags to de-
fine the exact safety requirements. To illustrate, the ValidNum tag can be parameterized as
ValidNum(self + rhs <= u8::MAX) and ValidNum(len * size_of::<T>() <= isize::MAX), codifying the
specific safety requirements in different contexts.

4.3   Taxonomy of Safety Tags
4.3.1 Layout. The Rust reference book introduces three key attributes related to layout.
   Alignment: While alignment violations are a form of pointer-related UB, we categorize alignment
here as it is an integral part of a type’s memory layout. An object of type T at address p is considered

                                                                  , Vol. 1, No. 1, Article . Publication date: April 2026.
8                                                                                   Zihao Rao, Jiping Zhou, Hongliang Tian, Xin Wang, and Hui Xu


                                                          Table 2. Primitive safety properties.

        Category          Safety Tag                                                 Expression                                                           Role
                              Align                               𝜌%align(𝜏) = 0 ∧ sizeof(𝜏)%align(𝜏) = 0                                          precondition
         Layout                Size                                            sizeof(𝜏) ∈ S                                                   precondition, option
                            !Padding                                          padding(𝜏) = 0                                                       precondition
                             !Null                                                 𝜌≠0                                                               precondition
                           Allocated                          ∀𝑖 ∈ [0, sizeof(𝜏) × 𝜆), allocator(𝜌 + 𝑖) = 𝛼                                          precondition
         Pointer
                            InBound                         mem[𝜌, 𝜌 + sizeof(𝜏) × 𝜆) ⊆ single_allocated_obj                                         precondition
                           !Overlap                                     |𝜌𝑑 − 𝜌𝑠 | > sizeof(𝜏) × 𝜆                                                   precondition
                           ValidNum                                  𝜖 ∈ 𝜚 ∧ no_overflow(𝜖)                                                        precondition
                         ValidString                                    mem[𝜚 𝑠 ] ⊆ UTF-8                                                         precond, hazard
                          ValidCStr                               mem[𝜌 + 𝜆, 𝜌 + 𝜆 + 1] = null                                                     precondition
         Content
                              Init             ∀𝑖 ∈ [0, 𝜆), mem[𝜌 + sizeof(𝜏) × 𝑖, 𝜌 + sizeof(𝜏) × (𝑖 + 1)) = valid(𝜏)                            precond, hazard
                            Unwrap                                        unwrap(𝜈) = 𝜏                                                            precondition
                             Typed                                       typeOf(∗𝜌) = 𝜏                                                            precondition
                             Owning                                             ownership(∗𝜌) = ∅                                                    precondition
           Alias             Alias                                                     𝜌1 = 𝜌2                                                          hazard
                             Alive                                               lifetime(∗𝜌) ≥ 𝜆𝑡                                                   precondition
                             Pinned                                       ∀𝑡 ∈ [0, 𝜆𝑡 ), &𝑡 (∗𝜌)0 = 𝜌                                                   hazard
                           !Volatile                               ∄ thread 𝜃, 𝜃 .write(𝜌, 𝜌 + sizeof(𝜏) × 𝜆)                                        precondition
       Contextual            Opened                                   ∃ openfile() { 𝜙 ∧ ∄ closefile(𝜙)                                              precondition
                             Trait                                              𝜒 ∈ traitimpl(𝜏)                                                        option
                          !Reachable                                        SAT(cond()) = false                                                      precondition
       Notation: 𝜌: pointer, 𝜏: type, 𝜎: size, 𝜆: length, 𝛼: allocator, 𝜖: expression, 𝜚 : value range, 𝜈: value, 𝜆𝑡 : lifetime, 𝜙: file descriptor, 𝜒: trait, N: number,
                 ⊥: unknown, ⊤: any, 𝜃 : thread, S: a subset of N



aligned if p % alignment(T) = 0, and sizeof(T) must be a multiple of its alignment. These
constraints are captured by the Align combined with arguments pointer p and type T.
   Size: The safety tag Size pertains to whether a type’s size is known at compile time. It can be
parameterized to specify further constraints. For instance, Sized(T, any) denotes a statically
sized type, while Sized(T, unknown) indicates a dynamically sized type. A common requirement
is that a type must not be a zero-sized type (ZST), as seen in NonNull::offset_from method. This
is expressed as Size(T, !0), or !ZST as a variant or shorthand.
   Padding: This property asserts that type T has no unused padding bytes and its safety tag can be
presented as !Padding. This is crucial for operations like raw_eq(), where padding contents could
otherwise affect the comparison result.
4.3.2 Pointer. This category concerns pointer validity. The !Null property asserts that a pointer
must not be null, a requirement for APIs like NonNull::new_unchecked. The Allocated property,
required by functions such as vec::from_raw_parts_in, ensures a pointer is not dangling and
points to a valid memory region of a specified size and it must be allocated by the specific allocator
A. The property InBound ensures that the memory space is not only allocated but allocated for the
same object’s memory boundary. Finally, the property !Overlap ensures that the two memory
spaces pointed to by dst and src do not overlap.
4.3.3 Content. This category ensures that memory contents adhere to type-specific invariants.
For instance, the generic-typed API, Box::assume_init(self) -> Box<[T], A> requires the
memory of the generic-typed value to be properly initialized before calling the method. For other
concrete types, there are specific properties:
   Valid Number: The ValidNum property ensures that the result of an arithmetic expression falls
within the valid range of its numeric type (e.g. isize, i32). This annotation also implies that no
intermediate computations overflow. In its usage, additional elements can be added to specify the
first parameter as an arithmetic expression, and the second as the valid value ranges.

, Vol. 1, No. 1, Article . Publication date: April 2026.
Annotating and Auditing the Safety Properties of Unsafe Rust                                                         9


   Valid String: The ValidString property requires a memory region to contain a valid UTF-8
sequence, upholding Rust’s string encoding invariants.
   Valid CStr: The ValidCStr property mandates that a sequence of bytes is a valid C-style string,
terminating with a null byte, as required by APIs like CStr::from_ptr.
   Furthermore, for enumerated types, the Unwrap safety tag specifies the variant required for a
safe unchecked unwrap. For instance, Option::unwrap_unchecked(self) can be annotated with
Unwrap(self, Some(T)). Finally, Typed means that the memory pointed by the pointer can be
used to create an object of type T. Rust has such safety requirements for several constructors named
from_raw, such as Rc::from_raw(ptr: *const T) -> Rc<T> which requires the pointers be
returned from an Rc object via the Rc::into_raw(this: Rc<T, A>) -> *const T method.

4.3.4 Alias. This category relates to the context of ownership, borrowing, and lifetime rules
enforced by the Rust compiler, which are fundamental to guaranteeing exclusive mutability. The
Owning property is a precondition for APIs like Box::from_raw that consume a raw pointer to
create an owned value. It asserts that the pointer has no other owners to prevent double-free
vulnerabilities [28, 50]. In contrast, the Alias property addresses potential violations of mutable
exclusivity, such as when converting a raw pointer to a reference like pointer::as_mut<’a>.
Unlike Owning, temporary violations of alias rules can be useful in certain scenarios (e.g., double-
linked list). Thus, we classify the safety property of Alias as a hazardous status, a post-requirement
rather than a precondition (We will elaborate more on the classifications in Section 4.4). Finally, we
use Alive to represent an object’s lifetime must outlive a specified lifetime parameter.

4.3.5 Contextual. This category covers safety properties tied to specific execution contexts or
semantic invariants. For instance, pinning is a characteristic that ensures that an object remains
at the same memory address after being created and cannot be moved. Rust provides this feature
via the Pin struct, and we annotate such a requirement for methods within this struct as Pinned.
Another property related to memory access is volatile, which indicates that the memory may be
subject to concurrent access and may change. In such cases, compilers should reload the value
from memory rather than using the previous copy. Read or write operations via pointers (e.g.,
ptr::read) generally require the memory to be non-volatile. Otherwise, developers should use
volatile methods. We represent this requirement with !Volatile. Opened is a precondition for I/O
operations, requiring an underlying resource (e.g., a file descriptor for a UdpSocket) to be in an
open state. While distinct from direct memory-related UB, we categorize this as a safety property
because it typifies a generalized class of system-level invariants and is an intentional design of Rust
(see RFC-3128 [8]). Additionally, we use Trait to specify the condition that a type T implements a
particular trait. Finally, !Reachable is a special requirement indicating that the current statement
should not be reached during execution. The function intrinsics::unreachable() requires the
safety property.

4.3.6 Compound Safety Properties. We define compound properties by combining primitive tags
to concisely express recurring, complex safety requirements found in the Rust standard library
documentation.
   Deref: This property guarantees the dereferencing of a pointer over a range from p to
p+Sizeof(T)*len is safe. It consists of Allocated and InBound.
   ValidPtr: This property represents a pointer that is valid for memory access, as defined in
libcore’s ptr module [11]. The criteria distinguish zero-sized types (ZSTs) from others. For ZSTs,
every pointer is valid. But for non-ZSTs, this requires the pointer to be dereferenceable, formulated
as ZST || (!ZST && Deref).

                                                               , Vol. 1, No. 1, Article . Publication date: April 2026.
10                                                         Zihao Rao, Jiping Zhou, Hongliang Tian, Xin Wang, and Hui Xu


   Ptr2Ref: This property specifies the requirements for safely converting a raw pointer to a
reference, and can be represented as Align && Deref && Alias.
   Layout: This property is used for memory allocation APIs (e.g., Global::alloc(&self, layout:
Layout) -> *mut u8). It combines ValidNum && Allocated to ensure a pointer is properly aligned
and allocated according to a Layout struct.

4.4    Role and Usage of Safety Properties
Beyond their taxonomy and semantic arguments, safety properties are assigned specific contractual
roles within an API’s specification:
   Precondition: A precondition is a safety property that constitutes a necessary condition for an
API call to be sound. The caller is obligated to satisfy all preconditions collectively to establish the
sufficient condition for avoiding UB. This is the most common role for safety properties.
   Hazardous status (hazard): A hazardous status (or hazard) denotes a persistent constraint imposed
by an API call that the caller must uphold throughout subsequent operations. It functions as a
post-requirement, distinct from a traditional postcondition which only denotes a condition that must
be true after the function call but does not require ongoing maintenance. For example, !Init can
describe a hazardous state after calling ptr::copy<T> when the source memory is uninitialized.
   Optional precondition (option): An optional precondition (option) represents a sufficient but not
necessary condition for safety. Satisfying it ensures the safety of calling an unsafe API, but it
is not mandatory. For example, Pin::new_unchecked(pointer: Ptr) is guaranteed safe if the
underlying type of the pointer implements the Unpin trait (Trait(T, Unpin)), but this is not
mandatory; if the type is not Unpin, the caller must instead uphold the Pinned hazardous state.
   Collectively, a full safety property comprises three elements: a tag name, its arguments, and its des-
ignated role. This separation provides flexibility for different analysis scenarios. In lightweight code
reviews, the tag name alone suffices to convey the core requirement. For more precise verification, ar-
guments can be instantiated with concrete program variables using the notations from Table 2, such
as Init(𝜌,𝜏,𝜆), which maintains readability by clarifying a constraint that the memory range, start-
ing at 𝜌 and spanning sizeof(𝜏)*𝜆 bytes, must be properly initialized. Furthermore, the role spec-
ifies whether this constraint must be verified before (Precondition), after (Hazard) or is optional
(Option). Thus, the initialization requirement for slice::from_raw_parts(data: *const T,
len: usize) can be annotated as #[safety::requires(precond.Init(data,T,len))], where
the prefix precond. is usually elided if it is the sole role of this property.

4.5    Practical Applicability of the Tag-based Representation
Programs have an infinite logic space, but any practical annotation system must be finite. Using a
limited set of tags to cover complex program logic works in practice because unsafe code has two
key characteristics: semantic recurrence and contractual abstraction.
   First, semantic recurrence means that while code varies, the safety conditions required by
low-level APIs frequently repeat standard patterns (such as pointer validity and alignment). This
repetition allows a small set of tags to cover most cases. As demonstrated by our 96.1% cov-
erage of the standard library in Section 7, a finite taxonomy is completely sufficient for real-
world auditing. Second, contractual abstraction separates high-level interface contracts from
complex implementation details. Safety tags formalize high-level interface contracts. For exam-
ple, to handle diverse unchecked operations, the ValidNum tag can express completely differ-
ent constraints simply by changing its parameters, e.g., ValidNum(self + rhs <= u8::MAX) and
ValidNum(len * size_of::<T>() <= isize::MAX). This parameterization makes safety requirements
generalizable across different APIs, keeping the tag taxonomy compact. Consequently, highly
specific, platform-dependent edge properties that defy such abstraction are intentionally excluded.

, Vol. 1, No. 1, Article . Publication date: April 2026.
Annotating and Auditing the Safety Properties of Unsafe Rust                                                        11


Sacrificing exhaustive coverage of these long-tail properties in favor of a compact and generalizable
tag system is a necessary trade-off for practical engineering.

5     Auditing Methodology for Safety Documentation
Building on the semantic foundation of safety tags, this section introduces a set of empirical rules
to audit the consistency and completeness of API safety documentation.

5.1    Motivating Example: Cross-Function Safety Dependencies
This section uses Box<T, A> to illustrate how cross-function safety dependencies manifest in
practice.
   As shown in Figure 3, drop is a safe function that calls the unsafe API Allocator::deallocate.
The specification requires that the memory being deallocated must have been allocated by the
specified allocator A (a requirement captured by the Allocated tag from Section 4). Since drop
performs no local validation, this requirement must be established at construction time.
   Box<T, A> has multiple construction paths. For example, the safe constructor new_in allocates
memory via A internally, satisfying this prerequisite. However, the unsafe constructor from_raw_in
accepts an externally provided raw pointer with no constraint on its allocator provenance, and its
documentation contains no declaration of this requirement. A caller can therefore pass a pointer
allocated by a different allocator through from_raw_in. When drop is subsequently triggered, the
call to deallocate on that pointer produces undefined behavior.
   This shows that safety requirements can span function boundaries. From a program analysis
perspective, this class of issues is conventionally attributed to the violation of struct invariants.
However, globally reasoning about struct invariants imposes substantial cost in large-scale audits.
We adopt a more operationally tractable perspective by reframing the audit as tracking how the
safety tags are propagated, discharged, or omitted along the call chain or struct . The following
sections classify APIs based on their roles in the object lifecycle and define empirical rules to review
the consistency and completeness of safety documentation across the entire state propagation
chain.

5.2    Audit Units
Because unsafe code is encapsulated within various functional and structural boundaries, track-
ing safety requirements requires well-defined audit scopes. We introduce three core concepts to
construct these boundaries.
  Definition 1 (Target API). A target API is defined as any function or method that is explicitly
marked unsafe or internally contains unsafe operations. It serves as the focal point for consistency
verification, where documented safety tags are compared against actual implementation constraints.
  Definition 2 (Constructor). A Constructor is a function that instantiates a struct and does not
consume an existing instance (i.e., no self parameter). Its return type logically instantiates the struct,
encompassing both direct types (e.g., Self) and smart pointers (e.g., Box<Self>). Constructors act as
the genesis of structural invariants.
   Definition 3 (Audit Unit). An Audit Unit is a minimal, self-contained scope designed to evaluate
the documentation consistency of a specific Target API. It consists of a target API and its associated set
of constructors.
  We classify Audit Units into two topological categories based on the presence of state coupling.
  Type I: Function-Level Unit. A function-level unit is formed when the target API is a standalone
function or a static method without a self reference. The audit task is to check whether the internal

                                                               , Vol. 1, No. 1, Article . Publication date: April 2026.
12                                                            Zihao Rao, Jiping Zhou, Hongliang Tian, Xin Wang, and Hui Xu



  1   + /// The pointer must point to the memory allocated by the global allocator.      Safety Annotated:{?}     Local Guarantee : {Allocator}
  2   pub unsafe fn from_raw(raw: *mut T) -> Box<T> {
                                                                                             from_raw_in         …     new_in
  3     unsafe {Self::from_raw_in(raw, Global)}
  4   }
  5
  6   + /// The pointer must point to the memory allocated by alloc.
  7   pub const unsafe fn from_raw_in(raw: *mut T, alloc: A) -> Box<T, A> {                                     drop
                                                                                                                             Local Guarantee:
  8     Box(unsafe {Unique::new_unchecked(raw)}, alloc)                                                                         {Layout}
  9   }
 10
 11   pub fn new_in<A: Allocator>(x: T, alloc: A) -> Self {                                      …          Allocator::deallocate
 12       let mut boxed = Self::new_uninit_in(alloc);
 13       boxed.write(x);                                                                               Safety Required: {Layout, Allocator}
 14       unsafe { boxed.assume_init() }                                                                        (i)
 15   }
 16
 17   fn drop(&mut self) {                                                                    Safety Annotated: {Alias,Owning} ∪ {?}
 18       let ptr = self.0;
                                                                                                          from_raw
 19       unsafe {
 20           let layout = Layout::for_value_raw(ptr.as_ptr());
 21           if layout.size() != 0 {
 22                self.1.deallocate(From::from(ptr.cast()), layout);                                    from_raw_in
 23           }
 24       }                                                                                   Safety Required : {Alias, Allocator,Owning}
 25   }                                                                                                         (ii)




Fig. 3. Motivating examples for safety documentation auditing and audit units in Box. (i) Method-level
unit: the unsafe constructor from_raw_in fails to document the Allocator requirement propagated from
drop. (ii) Function-level unit: from_raw fails to delegate this requirement from from_raw_in.


code behaviors of the caller (e.g., from_raw in Fig. 3) satisfies the safety demands of the unsafe
callees (e.g., from_raw_in), or whether it accurately propagates them to its own documented Safety
Tags.
   Type II: Method-Level Unit. A method-level unit is formed when the target API is an instance
method of a struct (e.g., drop). This unit exhibits state coupling, meaning the safety may rely on the
validity of the struct’s internal fields. Auditors should first examine whether the internal behaviors
of the method completely handle the safety requirements of callee (e.g., deallocate), followed by
checking whether all associated constructors (e.g., new_in and from_raw_in) satisfy any missing
safety requirements.

5.3    Audit Rules for Documentation Consistency
 Solution to Challenge 2 We introduce three progressive audit rules to check documentation con-
sistency in each audit unit: call-site check, constructor guarantee check, and state exposure check.
   We audit safety documentation by checking that every safety obligation is either handled
internally by code or explicitly documented for the user. We consider documentation correct if the
safety requirements are stated directly at the target API (Rule I) or guaranteed by its constructors
(Rule II). However, trusting constructor documentation requires the struct to protect its internal
state from outside interference (Rule III). Ultimately, we report a documentation defect in two cases:
a safety requirement is missing or incorrect from the docs, or the struct exposes its internal state,
making its documented guarantees useless.
Rule I: Call-Site Check Rule
   This rule examines the target API directly. Any safety demands originating from its internal
unsafe operations must be handled via internal code validation or explicitly declared in its public
documentation. If a safety demand is neither programmatically discharged nor documented, it con-
stitutes a documentation omission. For example, when auditing the function-level unit from_raw in
Fig. 3(ii), auditors identify that its internal callee (from_raw_in) inherently requires the Allocator

, Vol. 1, No. 1, Article . Publication date: April 2026.
Annotating and Auditing the Safety Properties of Unsafe Rust                                                        13


property. Because from_raw neither enforces this internally nor documents the Allocator tag for
its callers, it violates this rule.
Rule II: Constructor Guarantee Check Rule
   When a target method relies on struct-level state, the audit evaluates its associated constructors.
Every valid constructor must account for safety demands left unhandled or undocumented by the
method. Constructors achieve this by either safely initializing the state internally or documenting
the requirement for their own callers. If a method defers a safety obligation, and any constructor fails
to initialize the required state while also omitting the safety documentation, the safety requirements
are incomplete. For instance, in the method-level unit centered on drop in Fig. 3(i), the method calls
deallocate, which demands the Allocator tag. Because drop does not handle this locally, the
obligation transfers to the constructors. While the safe new_in internally satisfies this requirement
by allocating correctly, the unsafe from_raw_in neither enforces the allocator provenance nor
documents the Allocator tag, violating this rule.
Rule III: State Exposure Check Rule
   This rule evaluates whether internal states governing an API’s safety are exposed to external
modifications (e.g., via public fields). When a struct exposes such critical states, the responsibility
for maintaining safety invariants transfers to the caller. Thus, the exposed fields should explicitly
document the safety constraints that callers are obligated to uphold. Without these documented
restrictions, callers may inadvertently overwrite established invariants, rendering the struct’s
overall safety guarantees useless. For example, hypothetically assume Box<T, A> exposes its alloc
field publicly. An external caller could replace the original allocator with a different one. When drop
is subsequently invoked, it would attempt to deallocate the memory using the incorrect allocator,
violating the Allocator property.

6     Implementation
6.1    Operationalizing Safety Tags
 Solution to Challenge 3 To provide automated enforcement of safety tag consistency between
caller annotations and callee requirements, we developed safety-tool. This tool supports safety
comments with attributes: #[safety::requires] and #[safety::checked]. As illustrated in
Figure 4, safety-tool connects developer annotations, tag definitions, and API contracts.

6.1.1 Tag Definition and Configuration. A safety tag is an attribute applied to both the definition
and the call sites of unsafe functions. It corresponds to a single safety requirement consisting
of a property identifier, arguments, roles, description, formal expression, and URL. Common
properties are specified in a centralized TOML configuration file. The left side of Fig 4 shows the tag
specification of slice::from_raw_parts. The identifier names the requirement, while arguments
allow developers to plug in context-specific variables (e.g., self.ptr) to accurately express the
safety constraint.

6.1.2 Enforcement and Consistency. Operating as a static linter, safety-tool enforces consistency
between a caller’s annotations and the safety tags of its callees. When calling a tagged unsafe
function, the caller must provide corresponding #[safety::checked] and #[safety::requires]
tags that include all defined property identifiers, optionally with justifications, to fully discharge or
propagate the function’s safety requirements (see the right side of Fig 4). If any tags are missing, the
tool will report an error and explain the unhandled requirements. This mechanism is particularly
important for handling the evolution of external API safety contracts. For instance, if an updated
dependency introduces a new safety requirement, the tool automatically identifies the discrepancy

                                                               , Vol. 1, No. 1, Article . Publication date: April 2026.
14                                                                           Zihao Rao, Jiping Zhou, Hongliang Tian, Xin Wang, and Hui Xu


                   safety.toml                                # Safety
 [tag.NonNull]                                                /// pointer `self.ptr` must be    1 struct St1 { ptr: *mut u8, len: usize }
 args = [ "p" ]                                               valid for reading and writing     2 impl St1 {
 desc = "pointer `{p}` must not be null"                      the `sizeof(u8) * self.len` …
                                                                                                3     #[safety::requires {
 [tag.ValidPtr]                                                                                 4             ValidPtr(self.ptr, u8, self.len),
 args = [ "p", "T", "len" ]                                       Feature 1: Automated          5             Init(self.ptr, u8, self.len),
 desc = "pointer `{p}` must be valid for reading and
 writing the `sizeof({T})*{len}` memory from one single
                                                                  Documentation Expansion       6             Alive(self.ptr, _),
 allocation"                                                                                    7             Alias(self.ptr),
 [tag.Init]                                                                                     8             Align(self.ptr, u8),
 args = [ "p", "T", "len" ]                                                                     9             ValidNum(self.len*sizeof(u8),   [0, isize::MAX]),
 desc = "the memory range `[{p}, {p} + sizeof({T})
                                                           Safety-Tool                         10     }]
 *{len}]` must be fully initialized for type `{T}`"
                                                                                               11     pub unsafe fn get (&self) -> &[u8] {
 [tag.Alive]                                                                              12
 args = [ "p", "l" ]
                                                                  Feature 2:                              if !self.ptr.is_null {
 desc = "`{p}` must outlive the lifetime `{l}`"                   Consistency Enforcement 13                  #[safety::checked{NonNull(self.ptr)}]
                                                                                               14             unsafe { slice::from_raw_parts(self.ptr, self.len) }
 [tag.Alias]                                                                                   15         }
 args = [ "p" ]
                                                            Checked & Propageted Safety        16     }
 desc = "`{p}` must not have other aliases"
 types = [ "hazard" ]                                                                          17 }
 [tag.Align]                                                      Required Safety
 args = [ "p", "T" ]
 desc = "pointer `{p}` must be aligned for type `{T}`"

 [tag.ValidNum]                                            NonNull       ValidPtr    Init      Alive            Alias       Align     ValidNum        … CI/CD
 args = [ "exp", "range" ]
 desc = "the value of `{exp}` must lie within `{range}`”
                                                               pub const unsafe fn from_raw_parts<'a, T>(data: *const T, len: usize) -> &'a [T]
 ...




Fig. 4. The workflow and core features of safety-tool. The tool facilitates (1) Automated Documentation
Expansion, which transforms structured safety tags into standard human-readable documentation; and (2)
Consistency Enforcement, which statically verifies that the safety obligations of unsafe callees are strictly
discharged or propagated by the caller.


and issues an alert, allowing developers to catch latent safety regressions without manual re-
auditing.
6.1.3 Automated Documentation Expansion. The tool can also expand documentation automatically
by using a procedural macro to expand #[safety::requires] into standard #[doc] attributes. In-
stead of writing ad-hoc comments for an API, developers simply list the required tags (e.g., NonNull,
ValidPtr, Init). The tool combines these tags with the TOML definitions to generate standardized,
human-readable documentation directly in the source code. This ensures the documentation always
stays in sync with the actual safety contracts.
6.1.4 Implementation of safety-tool. The tool is implemented as a Rust compiler driver, extracting
attributes from unsafe functions and expressions. To enhance the developer experience, we also
provide LSP plugins for VSCode and Neovim, currently supporting autocompletion and hover
documentation for safety tags.

6.2      Integration with Rust Ecosystem
To bring our idea to the entire Rust ecosystem, we have submitted a formal RFC [43] titled "Safety
Tags" to the official Rust language repository. It pursues two concrete goals: (1) annotate every
public unsafe API in the standard library with safety tags, and (2) extend Clippy to verify the tags
and rust-analyzer to provide full language-server support for them. The RFC is presently under
active deliberation, having accumulated over 50 commits and 170 comments to date. Several Rust
projects have already shown initial interest in adopting safety tags (e.g., the Rust-for-Linux [44]
and Bevy game [4]).

7      Experiments with The Rust Standard Library
To evaluate our methodology, we conducted a comprehensive audit of the Rust standard library,
encompassing the core [31], alloc [30], and std [32] crates. The target Rust version is nightly
1.84.0. Two authors, with 3 and 6 years of Rust experience respectively, manually cross-reviewed the

, Vol. 1, No. 1, Article . Publication date: April 2026.
Annotating and Auditing the Safety Properties of Unsafe Rust                                                                        15


         10 3
                                                                                                                    std
                                                                                                                    std
                                                                                                                    alloc
                                                                                                                    alloc
                                                                                                                    core
                                                                                                                    core

         10 2




         10 1




         10 0
                    n   e   g   ll d   d  p        g   r  it   p  d g   s   e  d    e  d      it   e     r   f     t   p p
                  ig Siz din Nu ate un rla Num trin CSt In ra pe nin lia liv ne atil ne Tra abl idPt 2Re you _s _s
                Al            /
                                oc B
                                     o ve id                 w Ty w   A   A in ol pe             h   l    tr La tion tem
                        ad ll             l   S lid      Un                 P !V O           ac Va idP
                      !P !Nu All In !O Va alid Va                 O                         e          l         c
                                                                                                                n Sy s
                                            V                                            !R        Va        Fu




      Fig. 5. Quantity distribution of safety property tags identified in the Rust standard library.



APIs. To avoid redundancy, re-exported APIs were counted only once. In this section, we report the
coverage of safety tags and the patterns of audit units, and detail the documentation inconsistencies
identified during the audit.

7.1   Safety Profile of Rust Standard Library
Our audit of the Rust standard library identified 516 public unsafe APIs (excluding most intrinsic
functions). In total, our safety tags can express the safety properties for 96.1% of these APIs. The
remaining 3.9% pertain to system-level properties or functional correctness beyond the scope of
our annotation language (e.g., env::set_var()). We only focus on a subset of intrinsic functions,
excluding the majority whose safety (in terms of resolving to the correct linker symbols) is a
platform requirement, not one that can be guaranteed by the caller. More details are provided
in Section 7.2.2. The core, alloc, and std crates contain 414, 64, and 38 public unsafe APIs,
respectively. We achieved annotation coverage rates of 98.3%, 82.8%, and 84.2%, assigning a total
of 744, 105, and 44 safety tags to each crate, including both primitive and compound tags. The
coverage of alloc and std is relatively low because they contain a portion of unsafe APIs involving
function correctness and system properties.
   Figure 5 details the distribution of safety tags across the crates, plotted on a logarithmic scale
due to the substantially higher tag count in the core crate. The ValidNum tag is predominant,
reflecting its broad use in validating integer ranges (e.g., from isize::MIN to isize::MAX), indices,
and offsets. The distribution also reveals crate-specific characteristics: The alloc crate relies more
on Owning and function correctness (e.g., in collection types like BTreeMap), while the std crate is
more constrained by Opened and other system properties related to the runtime environment (e.g.,
the unsafe APIs in the env module).
   We further analyze the structural characteristics of unsafe code usage by extracting audit units
(Figure 6). The analysis yielded 1184 audit units for core, 269 for alloc, and 158 for std. Both alloc
and std contain a high proportion of method-level units. This reflects their roles in providing
high-level abstractions and complex data structures (e.g., Vec, Box). In sharp contrast, core is
dominated by function-level units (≈71.1%). This ratio is primarily driven by the large number of
primitive numeric APIs (e.g., for u8, u16) and intrinsic wrappers (e.g., add_unchecked). Crucially,

                                                                               , Vol. 1, No. 1, Article . Publication date: April 2026.
16                                                                Zihao Rao, Jiping Zhou, Hongliang Tian, Xin Wang, and Hui Xu

          Method-                                   Method-                                    Method-
         Level Unit                                Level Unit                                 Level Unit
          28.89%                                    37.92%                                     49.37%




                                 Function-                                       Function-                           Function-
                                 Level Unit                                      Level Unit                          Level Unit
                                  71.11%                                          62.08%                              50.63%


                      (a) core                                   (b) alloc                                 (c) std

             Fig. 6. Distribution of unit patterns for each crate of the Rust standard library.


this distribution serves as an indicator of audit complexity. Method-level units impose a higher
audit burden, as they demand a review of multiple APIs.

7.2    Tag-Based Safety Property Analysis
7.2.1 Inference Rules. Applying the audit rules from Section 5 requires significant manual effort.
To detect documentation defects at scale, our strategy is to filter APIs that show a high likelihood
of documentation omissions. We achieve this by comparing the actual safety tags present in the
documentation against an empirically derived set of expected tags.
   To generate these expectations, we leverage the consistent naming conventions, type signatures,
and interface patterns found in the Rust standard library. We implemented a script that codifies
these conventions into a set of heuristic inference rules. For a given API, these rules deduce a
predicted set of required safety obligations. A mismatch occurs when the inference rules demand a
safety tag that is absent from the actual documentation. We flag APIs with such mismatches as
highly suspicious candidates. We then manually investigate these candidates using our audit rules
to confirm whether a true documentation defect exists. This automated inference process does not
strive for absolute formal completeness. Its primary objective is to act as a filter that identifies clear
deviations from established ecosystem conventions.
   To ensure our inference rules remain concise, we introduce the following notations: 𝑓𝑢 denotes
an unsafe function/method; 𝑃 𝑓 , 𝑅 𝑓 , 𝑁 𝑓 , and 𝑀 𝑓 denote the parameter set, return type, name, and
module of function 𝑓 , respectively. To replace legacy terminology, we define T𝑟𝑒𝑞 (𝑓 ) as the set of
required safety tags (obligations delegated to the caller).
   Infer Safety Tags by API Signatures. By analyzing the functionality of Rust APIs in the standard
library, we observe that certain API signatures strongly correlate with underlying safety properties.
Furthermore, consistent naming conventions within crates can be leveraged to infer appropriate
safety tags.
Inference Rule 1. Bottom Annotation Rule. Any public unsafe API should specify a non-empty set
of safety tags to declare its baseline safety requirements.
                                                                 𝑓 is pub 𝑓𝑢
                                                                T𝑟𝑒𝑞 ( 𝑓 ) ≠ ∅

Inference Rule 2. Raw Pointer to Ownership. APIs that construct owned objects from raw pointers
should enforce alignment, allocation, bound, aliasing, and ownership constraints on the pointer.
                                  𝑓 is 𝑓𝑢 ∧ raw_ptr ∈ 𝑃 𝑓            𝑅 𝑓 is object ∨ "from_raw" ∈ 𝑁 𝑓
                                      T𝑟𝑒𝑞 ( 𝑓 ) ⊇ {Align, Allocated, InBound, Alias, Owning}

Inference Rule 3. Raw Pointer to Reference. APIs that convert raw pointers into references should
require the pointer to satisfy alignment, allocation, bound, and aliasing constraints.

, Vol. 1, No. 1, Article . Publication date: April 2026.
Annotating and Auditing the Safety Properties of Unsafe Rust                                                              17

                             𝑓 is 𝑓𝑢 ∧ raw_ptr ∈ 𝑃 𝑓       𝑅 𝑓 is reference ∨ "as_ref" ∈ 𝑁 𝑓
                                   T𝑟𝑒𝑞 ( 𝑓 ) ⊇ {Align, Allocated, InBound, Alias}
Inference Rule 4. Designated Allocator. APIs accepting a specific allocator parameter should mandate
that the underlying memory was originally allocated by that exact allocator.
                              𝑓 is 𝑓𝑢 ∧ Allocator ∈ 𝑃 𝑓         𝑅 𝑓 is object ∨ "_in" ∈ 𝑁 𝑓
                                               T𝑟𝑒𝑞 ( 𝑓 ) ⊇ {Allocated}
Inference Rule 5. Unchecked Operations. APIs performing "unchecked" operations deduce module-
specific safety tags, such as numerical validity, UTF-8 compliance, or boundary checks.
                                              𝑓 is 𝑓𝑢 ∧ "unchecked" ∈ 𝑁 𝑓
                                           
                                           
                                            {ValidNum}        if 𝑀 𝑓 ∈ integer modules
                                           
                                           
                               T𝑟𝑒𝑞 ( 𝑓 ) ⊇ {ValidString}      if 𝑀 𝑓 = str
                                           
                                            {InBound}
                                           
                                                               if 𝑀 𝑓 = slice
                                           
Inference Rule 6. Assume Init. APIs asserting memory initialization must explicitly require callers
to ensure the target memory region is fully initialized.
                                             𝑓 is 𝑓𝑢 ∧ "assume_init" ∈ 𝑁 𝑓
                                                   T𝑟𝑒𝑞 ( 𝑓 ) ⊇ {Init}
   Safety Tag Analysis For Function Calls. According to the principle of encapsulation, all safety
properties of unsafe callees must be either delegated or verified by the caller. Assuming a conserva-
tive approach where the caller verifies nothing, we establish the delegation rule:
Inference Rule 7. Delegation Rule for Function Calls. Under a conservative audit assumption, the
caller should delegate the required safety tags of all its unsafe callees to its documentation.
                                                   ∀𝑓𝑢 invoked by 𝑓
                                                            Ð
                                                T𝑟𝑒𝑞 ( 𝑓 ) ⊇ T𝑟𝑒𝑞 ( 𝑓𝑢 )
7.2.2 Identified Safety Issues. Overall, we have fixed the safety descriptions of 27 APIs, involving
61 safety tags. Table 3 lists all these APIs along with the detailed information.
   Issues Detected via Inference Process. We have corrected root safety annotations for 14 APIs with
30 safety tags by inference rules. These documentation omissions were identified by comparing
the APIs’ existing documentation against the expected baselines generated by our inference rules,
and subsequently applying the Audit Rule I. Three of these were derived via value validity re-
quirements. Two of them are named str::from_utf8_unchecked_mut, one a static function and
the other a method. The last one, str::from_boxed_utf8_unchecked, converts a slice into the
String type, which lacks a safety description that specifies that the input byte slice must contain
valid UTF-8 data. Five of these were detected based on Rust’s ownership model, mandating an
Alias tag when a raw pointer is converted into an owned object or a reference. For instance,
the API CString::from_raw constructs a CString from a raw pointer but previously omitted
the aliasing constraint. This annotation is necessary because using the raw pointer while the
CString is alive violates mutable exclusivity. The remaining ones were from six unsafe APIs in the
core::intrinsics module and were resolved using memory and pointer safety principles, such
as typed_swap_nonoverlapping. Beyond these, 171 public unsafe intrinsic APIs still lack safety
descriptions. They are marked as unsafe to prevent UB associated with compiler platform features.
These intrinsic APIs are generally annotated with #[rustc_intrinsic_must_be_overridden],
indicating that their implementations are not provided within the core crate so that they require
platform-specific linkers. Although we have reported such issues, they cannot be easily addressed
at this stage due to a lack of consensus on how to document their safety requirements or even
whether such documentation is necessary, since these intrinsic APIs are not intended for general
developer use.

                                                                     , Vol. 1, No. 1, Article . Publication date: April 2026.
18                                                                    Zihao Rao, Jiping Zhou, Hongliang Tian, Xin Wang, and Hui Xu


Table 3. Fixed safety issues in the Rust standard library. Allocator is a variant of Allocated with allocator
parameter specified; ZST is a zero-sized variant of Sized.

Type / Namespace   Function Signature                                               Fixed Tags                       Issue Type Aud. R.       Inf. R.
Arc<T>             from_raw(ptr: *const T) -> Self                                  Allocator                        Missing    Rule I        Rule 7
Arc<T>             increment_strong_count(ptr: *const T)                            Allocator & ValidNum & Aligned   Missing    Rule I        Rule 7
Arc<T>             decrement_strong_count(ptr: *const T)                            Allocator & ValidNum & Aligned   Missing    Rule I        Rule 7
Arc<T, A>          increment_strong_count_in(ptr: *const T, alloc: A)               ValidNum & Aligned               Missing    Rule I        Rule 7
Arc<T,A>           decrement_strong_count_in(ptr: *const T, alloc: A)               ValidNum & Aligned               Missing    Rule I        Rule 7
                                                                                    Allocator                        Missing                  Rule 7
Box<T>             from_raw(raw: *mut T) -> Self                                                                                Rule I
                                                                                    Alias                            Missing                  Rule 2
                                                                                    Allocator                        Missing                  Rule 7
Box<T>             from_non_null(ptr: NonNull) -> Self                                                                          Rule I
                                                                                    Alias                            Missing                  Rule 2
                                                                                    Allocator                        Missing                  Rule 4
Box<T, A>          from_raw_in(raw: *mut T, alloc: A) -> Self                                                                   Rule I & II
                                                                                    Alias                            Missing                  Rule 2
                                                                                    Allocator                        Missing                  Rule 4
Box<T, A>          from_non_null_in(raw: NonNull, alloc: A) -> Self                                                             Rule I & II
                                                                                    Alias                            Missing                  Rule 2
Weak<T>            from_raw(ptr: *const T) -> Self                                  Allocator                        Missing    Rule I        Rule 7
CString            from_raw(ptr: *mut c_char) -> CString                            Alias & Owning & Allocated       Missing    Rule I & II   Rule 2
std::str           from_boxed_utf8_unchecked(v: Box) -> Box                         ValidString                      Missing    Rule I & II Rule 5
Rc<T>              increment_strong_count(ptr: *const T)                            ValidNum & Aligned               Missing    Rule I        Rule 7
Rc<T>              decrement_strong_count(ptr: *const T)                            ValidNum & Aligned               Missing    Rule I        Rule 7
Rc<T, A>           increment_strong_count_in(ptr: *const T, alloc: A)               ValidNum & Aligned               Missing    Rule I        Rule 7
Rc<T, A>           decrement_strong_count_in(ptr: *const T, alloc: A)               ValidNum & Aligned               Missing    Rule I        Rule 7
std::ptr           read_unaligned(src: *constT) -> T                                !Null || ZST                     False      Rule I        Rule 7
std::ptr           write_unaligned(src: *const T) -> T                              !Null || ZST                     False      Rule I        Rule 7
intrinsics         typed_swap_nonoverlapping<T>(x: *mut T, y: *mut T) -> T          Typed & ValidPtr & Aligned       Missing    Rule I        Rule 1
                   volatile_copy_nonoverlapping_memory<T>                           !Volatile & ValidPtr & Align
intrinsics                                                                                                           Missing    Rule I        Rule 1
                   (dst: *mut T, src: *const T, count: usize)                       !Overlap & Alias & Trait
                                                                                    !Volatile & ValidPtr
intrinsics         volatile_set_memory<T>(x: *mut T, y: *mut T)                                                      Missing    Rule I        Rule 1
                                                                                    Typed & Align
intrinsics         va_copy<’f> ( dest: *mut VaListImpl<’f>, src: &VaListImpl<’f>)   !Null & Allocated & Alias        Missing    Rule I        Rule 1
intrinsics         va_arg<T>(ap: &mut VaListImpl<’_>)                               InBound & Typed & Init           Missing    Rule I & II   Rule 1
intrinsics         va_end<T>(ap: &mut VaListImpl<’_>)                               Allocated                        Missing    Rule I & II Rule 1
VaListImpl         arg(&mut self) -> T                                              InBound & Typed & Init           Missing    Rule I        Rule 7
str                from_utf8_unchecked_mut(v: &mut [u8]) -> &mut str                ValidString                      Missing    Rule I & II Rule 1
std::str           from_utf8_unchecked_mut(v: &mut [u8]) -> &mut str                ValidString                      Missing    Rule I & II   Rule 1




   Issues Detected via Call-Site and Constructor Checks. Our application of audit rules uncovered a
total of 29 safety property issues spanning 15 APIs. Two of these were identified and fixed via
the Audit Rule II (struct soundness and constructor consistency rules), which stipulate that safety
properties not fully encapsulated by a method must be enforced by all of its constructors. These
issues, detected in Box::from_raw_in and Box::from_non_null_in, originated from the audit
unit of Box<T,A>::drop (see Figure 3). The drop method calls A.deallocate, which requires
the memory is originally allocated by allocator A (i.e., the Allocator safety property). However,
the internal logic of drop does not enforce this property. To avoid the endogenous unsoundness,
relevant constraints must be imposed in endogenous regions. As the drop is declared safe, this
safety property must be propagated to the constructors. While the constructors such as new_in
establish the Allocator safety property in their internal code logic by allocating via A, from_raw_in
internally only calls Unique::new_unchecked() and a literal alloc assignment, without imposing
sufficient constraints. Therefore, the Allocator safety requirement must be explicitly annotated.
Our audit units also revealed 23 instances of insufficient safety property delegation across 11 APIs.
According to Audit Rule I, the safety properties of an unsafe callee should be delegated by its
caller if they are not verified in function calls. Most of the detected issues appear in four widely

, Vol. 1, No. 1, Article . Publication date: April 2026.
Annotating and Auditing the Safety Properties of Unsafe Rust                                                        19


used structs: Box, Rc, Arc and Weak. Figure 3 also demonstrates a sample issue in Box::from_raw,
which lacks the required Allocator safety property. The function internally passes the Global
allocator to Box::from_raw_in, implying a need for allocator consistency. The remaining one
is ffi::va_list::arg, which must uphold the safety properties of intrinsics::va_arg. In
addition to missing safety properties, we also identified two false annotations related to pointer
validity. Specifically, two unsafe APIs that read or write memory based on raw pointer input
unnecessarily require the !Null tag, even for pointers to zero-sized types. This requirement
contradicts the latest specification in the documentation of pointer validity. To fix this issue, the
pointer should either be non-null or point to a value of a zero-sized type.
   Issues Detected via State Exposure Checks. We found one issue by Audit Rule III. Overall, there
are 320 data structures, including 147 public ones and 173 private ones. Among them, 42 public data
structures have unsafe constructors, and 15 of these allow literal constructors. By applying Audit
Rule III, we identified that the struct Pin<T> exhibits a soundness issue related to allowing a literal
constructor. In particular, the data structure has an unsafe constructor, new_unchecked(pointer:
Ptr) -> Pin<Ptr>, which accepts a pointer to some data of a type that may or may not implement
the Unpin trait (a marker trait indicating that the data can be safely moved). The constructor
requires callers to uphold the associated safety property, i.e., either the pointed object implementing
Unpin or ensuring the pinned object is not moved afterward. However, the data structure contains
only a single pointer field, which is public, thereby enabling the use of a literal constructor. As a
result, it is possible to bypass the intended safety requirements through the literal constructor.
   We have reported the issue to the official Rust repository, but it remains unresolved and is
therefore omitted from the table 3. The literal constructor remains enabled because it is required
by the macro constructor pin!. Currently, two countermeasures have already been employed to
mitigate the misuse of the literal constructor. First, the pointer field is marked with #[doc(hidden)]
to hide it from doc rendering and discourage direct access, although it remains publicly accessible
if developers deliberately access it. Second, developers must enable the unsafe_pin_internals
feature to use the literal constructor directly. However, these restrictions can still be bypassed
through the macro constructor pin!. The issue also highlights the urgent need to establish a
well-documented policy to ensure API soundness. As the ecosystem continues to grow, relying on
ad hoc safety handling techniques can increase the risk of subtle, hard-to-detect vulnerabilities.

8     Related Work
8.1    Safety Mechanisms and Research Related to Unsafe Rust
To ensure safety, the Rust ecosystem employs Miri [47] for dynamic UB detection, though it is limited
by incomplete path coverage. Complementing this, compiler flags like sanitizer, ub-checks, and
contract-checks enable runtime monitoring. The Rust Foundation’s verify-rust-std project [29]
further instruments the standard library with formal verification tools to address 27 unsafe API
challenges. Kani is the well-established verifier in the project [49], owning 1369 harnesses and
thousands of autoharnesses. Verifiers such as ESBMC [14], VeriFast [19], and Flux [24] have also
been acknowledged for their reliability. In academia, research spans empirical studies on unsafe
code [2, 13] and memory safety bugs [27, 38, 50]. Technical approaches in this domain include static
analysis for bug detection [3, 9, 28] and formal verification for ensuring soundness [15, 20, 25, 33].

8.2    Specification Generation and Safety Property Analysis
Research in specification generation has transitioned from traditional rule-based methods to modern
LLM-driven approaches. Early efforts, such as Toradocu [16], JDoctor [6], and various NLP-based
tools [12, 54], focused on extracting functional constraints from documentation to synthesize test

                                                               , Vol. 1, No. 1, Article . Publication date: April 2026.
20                                                         Zihao Rao, Jiping Zhou, Hongliang Tian, Xin Wang, and Hui Xu


oracles for Java and C/C++. More recently, new frameworks like SpecRover [42] and LLMxCPG [26]
further integrate structured program analysis with LLM to enhance auditing dependability and
specification precision. Distinct from these functional-oriented works, this paper focuses on Rust’s
safety soundness by establishing a systematic safety tag taxonomy, providing a formal foundation
for future automated generation.
   Regarding safety property enforcement, typestate analysis [46] serves as a foundational technique
for verifying state-dependent properties, extending even to object protocols [5]. Besides, Xu et
al. [51] pioneered its application to untrusted machine code, ensuring memory safety by statically
tracking fine-grained states (e.g., initialized vs. uninitialized) and linear constraints. Alongside
graph-based vulnerability discovery methods like the code property graph (CPG) [52, 53], we
synthesize all these philosophies into our auditing methodology.

9    Conclusion
This work addresses the problem of auditing unsafe Rust code in a practical and effective way. To
tackle the challenge of analyzing safety properties of unsafe code, we present a novel unsafety
propagation approach, featuring hazardous states of calling unsafe APIs over traditional post-
conditions. Our experiment shows that 96.1% of unsafe APIs in the standard library are covered by
all identified tags, and safety documentation issues were fixed for 27 APIs. We also introduce an
auditor named safety-tool to formulate safety properties as structured, machine-readable comments
and enforce the corresponding checks. An RFC titled “Safety Tags” has been submitted to the
Rust project repository for official support and community review. Moreover, UPG analysis and
tag-based approach can be extended further: parameterized safety tags provide a ready springboard
for automated formal verification in the future.

References
 [1] Vytautas Astrauskas, Aurel Bílỳ, Jonáš Fiala, Zachary Grannan, Christoph Matheja, Peter Müller, Federico Poli, and
     Alexander J Summers. 2022. The prusti project: Formal verification for Rust. In NASA Formal Methods Symposium.
     Springer, Springer-Verlag, Berlin, Heidelberg, 88–108.
 [2] Vytautas Astrauskas, Christoph Matheja, Federico Poli, Peter Müller, and Alexander J Summers. 2020. How do
     programmers use unsafe Rust? Proceedings of the ACM on Programming Languages 4, OOPSLA (2020), 1–27.
 [3] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon Lim, and Taesoo Kim. 2021. Rudra: Finding memory safety bugs
     in Rust at the ecosystem scale. In Proceedings of the ACM SIGOPS 28th Symposium on Operating Systems Principles.
     Association for Computing Machinery, New York, NY, USA, 84–99.
 [4] Bevy Contributors. 2026. Bevy: A Data-Driven Game Engine Built in Rust. https://bevyengine.org/ Accessed:
     2026-04-22.
 [5] Kevin Bierhoff and Jonathan Aldrich. 2007. Modular typestate checking of aliased objects. ACM SIGPLAN Notices 42,
     10 (2007), 301–320.
 [6] Arianna Blasi, Alberto Goffi, Konstantin Kuznetsov, Alessandra Gorla, Michael D Ernst, Mauro Pezzè, and Sergio Del-
     gado Castellanos. 2018. Translating code comments to procedure specifications. In Proceedings of the 27th ACM SIGSOFT
     international symposium on software testing and analysis. 242–253.
 [7] Rust Book. 2025. Unsafe Rust. https://doc.rust-lang.org/book/ch20-01-unsafe-rust.html [Accessed: 2025-04-28].
 [8] Rust Community. 2026. IO Safety. https://rust-lang.github.io/rfcs/3128-io-safety.html [Accessed: 2026-02-01].
 [9] Mohan Cui, Chengjun Chen, Hui Xu, and Yangfan Zhou. 2023. SafeDrop: Detecting memory deallocation bugs of rust
     programs via static data-flow analysis. ACM Transactions on Software Engineering and Methodology 32, 4 (2023), 1–21.
[10] Mohan Cui, Shuran Sun, Hui Xu, and Yangfan Zhou. 2024. Is unsafe an Achilles’ Heel? A comprehensive study of
     safety requirements in unsafe Rust programming. In Proceedings of the IEEE/ACM 46th International Conference on
     Software Engineering. Association for Computing Machinery, New York, NY, USA, 1–13.
[11] Rust Documentation. 2025. Module ptr. https://doc.rust-lang.org/nightly/std/ptr/index.html [Accessed: 2025-02-01].
[12] Michael D Ernst, Jake Cockrell, William G Griswold, and David Notkin. 2001. Dynamically discovering likely program
     invariants to support program evolution. IEEE transactions on software engineering 27, 2 (2001), 99–123.
[13] Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa. 2020. Is Rust used safely by software developers?. In
     Proceedings of the ACM/IEEE 42nd International Conference on Software Engineering. Association for Computing


, Vol. 1, No. 1, Article . Publication date: April 2026.
Annotating and Auditing the Safety Properties of Unsafe Rust                                                                21


     Machinery, New York, NY, USA, 246–257.
[14] Mikhail R Gadelha, Felipe R Monteiro, Jeremy Morse, Lucas C Cordeiro, Bernd Fischer, and Denis A Nicole. 2018.
     ESBMC 5.0: An industrial-strength C model checker. In Proceedings of the 33rd ACM/IEEE International Conference on
     Automated Software Engineering. Association for Computing Machinery, New York, NY, USA, 888–891.
[15] Lennard Gäher, Michael Sammler, Ralf Jung, Robbert Krebbers, and Derek Dreyer. 2024. RefinedRust: A type system
     for high-assurance verification of Rust programs. Proceedings of the ACM on Programming Languages 8, PLDI (2024),
     1115–1139.
[16] Alberto Goffi, Alessandra Gorla, Michael D Ernst, and Mauro Pezzè. 2016. Automatic generation of oracles for
     exceptional behaviors. In Proceedings of the 25th international symposium on software testing and analysis. 213–224.
[17] Rust Group. 2025. Rust Glossary. https://rust-lang.github.io/unsafe-code-guidelines/glossary.html [Accessed:
     2025-09-17].
[18] Michael Hind. 2001. Pointer analysis: haven’t we solved this problem yet?. In Proceedings of the 2001 ACM SIGPLAN-
     SIGSOFT workshop on Program analysis for software tools and engineering. Association for Computing Machinery, New
     York, NY, USA, 54–61.
[19] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. VeriFast: A
     powerful, sound, predictable, fast verifier for C and Java. In NASA Formal Methods Symposium. Springer, Springer-Verlag,
     Berlin, Heidelberg, 41–55.
[20] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. RustBelt: Securing the foundations of
     the Rust programming language. Proceedings of the ACM on Programming Languages 2, POPL (2017), 1–34.
[21] William Landi. 1992. Undecidability of static analysis. ACM Letters on Programming Languages and Systems (LOPLAS)
     1, 4 (1992), 323–337.
[22] Andrea Lattuada, Travis Hance, Jay Bosamiya, Matthias Brun, Chanhee Cho, Hayley LeBlanc, Pranav Srinivasan,
     Reto Achermann, Tej Chajed, Chris Hawblitzel, et al. 2024. Verus: A practical foundation for systems verification. In
     Proceedings of the ACM SIGOPS 30th Symposium on Operating Systems Principles. Association for Computing Machinery,
     New York, NY, USA, 438–454.
[23] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno,
     and Chris Hawblitzel. 2023. Verus: Verifying Rust programs using linear ghost types. Proceedings of the ACM on
     Programming Languages 7, OOPSLA1 (2023), 286–315.
[24] Nico Lehmann, Adam T. Geller, Niki Vazou, and Ranjit Jhala. 2023. Flux: Liquid Types for Rust. Proc. ACM Program.
     Lang. 7, PLDI, Article 169 (2023), 25 pages. https://doi.org/10.1145/3591283
[25] Nico Lehmann, Adam T Geller, Niki Vazou, and Ranjit Jhala. 2023. Flux: Liquid types for rust. Proceedings of the ACM
     on Programming Languages 7, PLDI (2023), 1533–1557.
[26] Ahmed Lekssays, Hamza Mouhcine, Khang Tran, Ting Yu, and Issa Khalil. 2025. {LLMxCPG}:{Context-Aware}
     vulnerability detection through code property {Graph-Guided} large language models. In 34th USENIX Security
     Symposium (USENIX Security 25). 489–507.
[27] Hongyu Li, Liwei Guo, Yexuan Yang, Shangguang Wang, and Mengwei Xu. 2024. An empirical study of Rust-for-Linux:
     The success, dissatisfaction, and compromise. In 2024 USENIX Annual Technical Conference. USENIX Association, Santa
     Clara, CA, 425–443.
[28] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John CS Lui. 2021. MirChecker: detecting bugs in Rust programs
     via static analysis. In Proceedings of The 2021 ACM SIGSAC Conference on Computer and Communications Security.
     Association for Computing Machinery, New York, NY, USA, 2183–2196.
[29] Verify Rust Std Lib. 2025. The verify Rust standard library effort. https://model-checking.github.io/verify-rust-
     std/intro.html [Accessed: 2025-04-10].
[30] Rust Standard Library. 2025. The Rust core allocation and collections library. https://doc.rust-lang.org/nightly/alloc/
     index.html [Accessed: 2025-04-28].
[31] Rust Standard Library. 2025. The Rust core library. https://doc.rust-lang.org/nightly/core/index.html [Accessed:
     2025-04-28].
[32] Rust Standard Library. 2025. The Rust standard library. https://doc.rust-lang.org/nightly/std/index.html [Accessed:
     2025-04-28].
[33] Yusuke Matsushita, Xavier Denis, Jacques-Henri Jourdan, and Derek Dreyer. 2022. RustHornBelt: a semantic foundation
     for functional verification of Rust programs with unsafe code. In Proceedings of the 43rd ACM SIGPLAN International
     Conference on Programming Language Design and Implementation. Association for Computing Machinery, New York,
     NY, USA, 841–856.
[34] Rust Nomicon. 2025. Working with unsafe. https://doc.rust-lang.org/nomicon/working-with-unsafe.html [Accessed:
     2025-04-28].
[35] Yuke Peng, Hongliang Tian, Jinyi Xian, Shuai Zhou, Shoumeng Yan, and Yinqian Zhang. 2024. Framekernel: A safe and
     efficient kernel architecture via Rust-based intra-kernel privilege separation. In Proceedings of the 15th ACM SIGOPS


                                                                       , Vol. 1, No. 1, Article . Publication date: April 2026.
22                                                         Zihao Rao, Jiping Zhou, Hongliang Tian, Xin Wang, and Hui Xu


     Asia-Pacific Workshop on Systems. Association for Computing Machinery, New York, NY, USA, 31–37.
[36] Yuke Peng, Hongliang Tian, Junyang Zhang, Ruihan Li, Chengjun Chen, Jianfeng Jiang, Jinyi Xian, Xiaolin Wang,
     Chenren Xu, Diyu Zhou, Yingwei Luo, Shoumeng Yan, and Yinqian Zhang. 2025. ASTERINAS: a Linux ABI-compatible,
     rust-based framekernel OS with a small and sound TCB. (2025), 17 pages.
[37] Boqin Qin, Yilun Chen, Haopeng Liu, Hua Zhang, Qiaoyan Wen, Linhai Song, and Yiying Zhang. 2024. Understanding
     and detecting real-world safety issues in Rust. IEEE Transactions on Software Engineering 50, 6 (2024), 1306–1324.
[38] Boqin Qin, Yilun Chen, Zeming Yu, Linhai Song, and Yiying Zhang. 2020. Understanding memory and thread safety
     practices and issues in real-world Rust programs. In Proceedings of the 41st ACM SIGPLAN Conference on Programming
     Language Design and Implementation. Association for Computing Machinery, New York, NY, USA, 763–779.
[39] Rust reference. 2025. The Rust reference: Behavior considered undefined. https://doc.rust-lang.org/reference/behavior-
     considered-undefined.html [Accessed: 2025-04-28].
[40] Rust reference. 2025. The Rust reference: visibility and privacy. https://doc.rust-lang.org/reference/visibility-and-
     privacy.html [Accessed: 2025-04-28].
[41] Rust RFC. 2025. Unsafe fields. https://github.com/rust-lang/rfcs/pull/3458 [Accessed: 2025-09-17].
[42] Haifeng Ruan, Yuntong Zhang, and Abhik Roychoudhury. 2024. Specrover: Code intent extraction via llms. arXiv
     preprint arXiv:2408.02232 (2024).
[43] Rust Community. 2026. RFC: Safety Tags for Unsafe Code. https://github.com/rust-lang/rfcs/pull/3842. GitHub Pull
     Request #3842. Accessed: 2026-04-23.
[44] Rust-for-Linux Contributors. 2026. Rust for Linux. https://rust-for-linux.com/ Accessed: 2026-04-22.
[45] Ayushi Sharma, Shashank Sharma, Sai Ritvik Tanksalkar, Santiago Torres-Arias, and Aravind Machiry. 2024. Rust
     for Embedded Systems: Current State and Open Problems. In Proceedings of the 2024 on ACM SIGSAC Conference on
     Computer and Communications Security. Association for Computing Machinery, New York, NY, USA, 2296–2310.
[46] Robert E Strom and Shaula Yemini. 2012. Typestate: A programming language concept for enhancing software
     reliability. IEEE transactions on software engineering 1 (2012), 157–171.
[47] The Rust Team. 2025. Miri. https://github.com/rust-lang/miri [Accessed: 2025-04-10].
[48] Hongliang Tian, Yuke Peng, Yingwei Luo, Shoumeng Yan, and Yinqian Zhang. [n. d.]. Asterinas: A Rust-Based
     Framekernel to Reimagine Linux in the 2020s. ([n. d.]).
[49] Alexa VanHattum, Daniel Schwartz-Narbonne, Nathan Chong, and Adrian Sampson. 2022. Verifying dynamic trait
     objects in Rust. In Proceedings of the 44th International Conference on Software Engineering: Software Engineering in
     Practice. Association for Computing Machinery, New York, NY, USA, 321–330.
[50] Hui Xu, Zhuangbin Chen, Mingshen Sun, Yangfan Zhou, and Michael R Lyu. 2021. Memory-safety challenge considered
     solved? An in-depth study with all Rust CVEs. ACM Transactions on Software Engineering and Methodology (TOSEM)
     31, 1 (2021), 1–25.
[51] Zhichen Xu, Barton P Miller, and Thomas Reps. 2000. Safety checking of machine code. ACM SIGPLAN Notices 35, 5
     (2000), 70–82.
[52] Fabian Yamaguchi, Nico Golde, Daniel Arp, and Konrad Rieck. 2014. Modeling and discovering vulnerabilities with
     code property graphs. In 2014 IEEE symposium on security and privacy. IEEE, 590–604.
[53] Fabian Yamaguchi, Alwin Maier, Hugo Gascon, and Konrad Rieck. 2015. Automatic inference of search patterns for
     taint-style vulnerabilities. In 2015 IEEE symposium on security and privacy. IEEE, 797–812.
[54] Yu Zhou, Ruihang Gu, Taolue Chen, Zhiqiu Huang, Sebastiano Panichella, and Harald Gall. 2017. Analyzing APIs
     documentation and code to detect directive defects. In 2017 IEEE/ACM 39th International Conference on Software
     Engineering (ICSE). IEEE, 27–37.




, Vol. 1, No. 1, Article . Publication date: April 2026.
