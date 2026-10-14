                                            Is unsafe an Achilles’ Heel? A Comprehensive Study of Safety
                                                     Requirements in Unsafe Rust Programming
                                                                         Mohan Cui                                                            Suran Sun
                                                                  School of Computer Science,                                        School of Computer Science,
                                                                       Fudan University                                                   Fudan University

                                                                          Hui Xu∗                                                          Yangfan Zhou
                                                                  School of Computer Science,                                        School of Computer Science,
                                                                       Fudan University                                                   Fudan University
arXiv:2308.04785v1 [cs.SE] 9 Aug 2023




                                        ABSTRACT                                                                           Listing (1) Source code of ManuallyDrop::take in Rust std.
                                        Rust is an emerging, strongly-typed programming language fo-                   1    // impl<T> ManuallyDrop<T>
                                        cusing on efficiency and memory safety. With increasing projects               2    pub unsafe fn take(slot: &mut ManuallyDrop<T>) -> T {
                                                                                                                       3        // SAFETY: we are reading from a reference, which is
                                        adopting Rust, knowing how to use Unsafe Rust is crucial for Rust              4        // guaranteed to be valid for reads.
                                        security. We observed that the description of safety requirements              5        unsafe { ptr::read(&slot.value) }
                                        needs to be unified in Unsafe Rust programming. Current unsafe                 6    }

                                        API documents in the standard library exhibited variations, includ-
                                        ing inconsistency and insufficiency. To enhance Rust security, we                  Listing (2) Document of ManuallyDrop::take in Rust 1.70.
                                        suggest unsafe API documents to list systematic descriptions of                1    Takes the value from the ManuallyDrop<T> container out.
                                        safety requirements for users to follow.                                       2    This method is primarily intended for moving out values in
                                                                                                                                  drop. Instead of using ManuallyDrop::drop to manually
                                           In this paper, we conducted the first comprehensive empirical                          drop the value, you can use this method to take the
                                        study on safety requirements across unsafe boundaries. We studied                         value and use it however desired.
                                        unsafe API documents in the standard library and defined 19 safety             3    Whenever possible, it is preferable to use into_inner
                                                                                                                                  instead, which prevents duplicating the content of the
                                        properties (SP). We then completed the data labeling on 416 unsafe                        ManuallyDrop<T>.
                                        APIs while analyzing their correlation to find interpretable results.          4    Safety
                                        To validate the practical usability and SP coverage, we categorized            5    This function semantically moves out the contained value
                                                                                                                                  without preventing further usage, leaving the state of
                                        existing Rust CVEs until 2023-07-08 and performed a statistical                           this container unchanged. It is your responsibility to
                                        analysis of std unsafe API usage toward the crates.io ecosystem.                          ensure that this ManuallyDrop is not used again.
                                        In addition, we conducted a user survey to gain insights into four
                                        aspects from experienced Rust programmers. We finally received
                                        50 valid responses and confirmed our classification with statistical         Figure 1: Example of an unsafe API in Rust std. Listing 1 pro-
                                        significance.                                                                vides the source code of an unsafe method of struct Manual-
                                                                                                                     lyDrop<T>. Listing 2 extracts the document in Rust 1.70. The
                                        CCS CONCEPTS                                                                 document introduces the usage, functionality, and safety re-
                                                                                                                     quirements to comply with by using a section labeled Safety.
                                        • Software and its engineering → General programming lan-
                                        guages; Development frameworks and environments.

                                        KEYWORDS                                                                     zero-cost abstractions [32] to transform data without sacrificing
                                        Unsafe Rust, Safety Property, Rustdoc, CVE, User Survey, Undefined           performance [33] (e.g., generic types). Although Rust has a steep
                                        Behavior                                                                     learning curve [18], it has attracted many programmers due to its
                                                                                                                     safety and efficiency [34]. Since 2016, Rust has been the most popu-
                                        ACM Reference Format:
                                        Mohan Cui, Suran Sun, Hui Xu, and Yangfan Zhou. 2023. Is unsafe an
                                                                                                                     lar programming language in the open-source community [43–49],
                                        Achilles’ Heel? A Comprehensive Study of Safety Requirements in Unsafe       with many projects refactoring code in Rust [36, 37, 52].
                                        Rust Programming. In Proceedings of arxiv pre-print versions (arxiv). ACM,      As Rust continues to evolve, knowing how to use Unsafe Rust is
                                        New York, NY, USA, 12 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn         essential for Rust security [5]. Safety isolation is one of the revolu-
                                                                                                                     tionary innovations introduced by Rust [51]. It divides the portions
                                        1    INTRODUCTION                                                            the compiler can ensure safety into Safe Rust and adds the unsafe
                                        Rust is an emerging system programming language focusing on                  keyword as the superset [33]. The primary document defines Un-
                                        memory safety and efficiency [41]. It provides memory-safe guar-             safe Rust as a keyword and a set of operations [50]. Any code with
                                        antees via compile-time checks [18]; consequently, programmers               unsafe operations must be wrapped in an unsafe block. If not, pro-
                                        must adhere to various syntactic constraints to satisfy the verifica-        grammers will trigger compilation errors. Without strict compiler
                                        tion [71]. As a system programming language, it employs several              checks in the unsafe scope, Rust developers may become insensitive
                                                                                                                     to satisfying safety requirements, which is error-prone to causing
                                        ∗ Corresponding author.                                                      undefined behavior (UB).
arxiv, 2023,                                                                                                                                                       Cui et al.


Table 1: A list of APIs with similar side effects and their document slices in Rust 1.70. These APIs accept mutable pointers as
input and return a typed owner. In previous research, it has been reported that misuse of these APIs may result in double-free
issues. The consistency and clarity of these documents need improvement: Related descriptions are not always located within
the Safety section, and the description of the safety requirement (underlined) or side effect (bolded) is insufficient. We expect a
specific error type to be defined.

       Implemented Type                       Unsafe Method                      Safety Description Slices in API Documents.
                                                                                 read creates a bitwise copy of T, regardless of whether T is Copy. If T is not Copy, using
     impl<T: ?Sized> *mut T                  fn read(self) -> T                  both the returned value and the value at *src can violate memory safety. Note that
                                                                                 assigning to *src counts as a use because it will attempt to drop the value at *src.
                                                                                 This function semantically moves out the contained value without preventing further
  impl<T> ManuallyDrop<T>         fn take(&mut ManuallyDrop<T>) -> T             usage, leaving the state of this container unchanged. It is your responsibility to ensure
                                                                                 that this ManuallyDrop is not used again.
                                                                                 This function is unsafe because improper use may lead to memory problems. For
    impl<T: ?Sized> Box<T>             fn from_raw(*mut T) -> Self               example, a double-free may occur if the function is called twice on the same raw
                                                                                 pointer.
                                                                                 The raw pointer must have been previously returned by a call to Rc<U>::into_raw
     impl<T: ?Sized> Rc<T>             fn from_raw(*const T) -> Self             where U must have the same size and alignment as T. The user of from_raw has to
                                                                                 make sure a specific value of T is only dropped once.
                                                                                 This should only ever be called with a pointer that was earlier obtained by calling
           impl CString              fn from_raw(*mut c_char) -> Self            CString::into_raw. Other usage (e.g., trying to take ownership of a string that was allo-
                                                                                 cated by foreign code) is likely to lead to undefined behavior or allocator corruption.
                                                                                 The ownership of ptr is effectively transferred to the Vec<T> which may then deallocate,
        impl<T> Vec<T>        fn from_raw_parts(*mut T, usize, usize) -> Self    reallocate or change the contents of memory pointed to by the pointer at will. Ensure
                                                                                 that nothing else uses the pointer after calling this function.
                                                                                 The ownership of buf is effectively transferred to the String which may then deallocate,
           impl String        fn from_raw_parts(*mut u8, usize, usize) -> Self   reallocate or change the contents of memory pointed to by the pointer at will. Ensure
                                                                                 that nothing else uses the pointer after calling this function.



   How does Rust document safety requirements for unsafe opera-                    • RQ-1. What finer-grained safety properties (requirements) should
tions? We observed that most safety requirements are specified on                    be satisfied across the Unsafe Rust boundary? (§3)
a Safety label in Rust std. The Rust standard library [26] provides                • RQ-2. Can those safety properties cover existing vulnerabilities
documents for unsafe APIs that are relatively comprehensive. As                      caused by Unsafe Rust? (§4)
shown in Figure 1, we chose one API as the typical example. When                   • RQ-3. How helpful are those safety properties for real-world
calling ManuallyDrop::take [55], it has a safety requirement to                      Unsafe Rust programming? (§5)
be manually reviewed: Users cannot use this container again. Oth-
erwise, it would trigger undefined behavior. Its implementation                       For each RQ, our study introduces several sub-experiments. To
calls unsafe function ptr::read [59] (line 5), prompting us to think               answer RQ1, we extracted all public unsafe APIs within the Rust
they may have analogous safety descriptions.                                       standard library [26] and manually audited the document. We cat-
   Unfortunately, Unsafe Rust does not provide developers with                     egorized the safety requirements across the unsafe boundary as
unified safety descriptions or systemic safety requirements. Recent                Safety Properties (SPs). We completed the data labeling for those
research found that misusing several unsafe APIs may result in                     APIs and then conducted a correlation analysis to find interpretable
memory-safety issues [69], where overlapped owners can be created                  results. To answer RQ2, we examined all Rust CVEs [19] until 2023-
and cause double free [6, 11], such as ManuallyDrop::take and                      07-08 and filtered through the root causes by misusing unsafe code,
*mut T::read. Table 1 lists them with documents in Rust 1.70.                      categorizing them according to Safety Properties to validate our
Like ManuallyDrop::take, using a Safety label to start the safety                  classification. Then, we collected and analyzed the distribution of
description is intuitive. The majority of the listed APIs adhere to this           unsafe APIs within the crates.io [21] ecosystem. To answer RQ3, we
criterion, such as implementations for String, Vec<T>, CString,                    surveyed experienced Rust developers. We provided participants
and Box<T>. However, the Rc<T> lacks the Safety section, and the                   with the definition of each SP and its minimal Proof of Concept
related issue caused by read is described in the outer section. At last,           (PoC). We studied whether the developers acknowledged our cat-
the texts of side effects exhibit differences: Only Box<T> explicitly              egorization and whether each Safety Property was beneficial for
states the potential double-free that may arise.                                   unsafe programming.
   The unsafe API documents should systematically classify safety                     Reviewing documents of unsafe APIs in Rust std, we performed
requirements for users to comply with. This paper comprehensively                  an audit on 416 unsafe APIs. As a result, we identified and defined
categorizes fine-grained safety requirements when crossing unsafe                  19 safety properties (SP), categorized into two major categories:
boundaries. In general, this paper seeks to address the following                  precondition and postcondition. Subsequently, we completed the
research questions (RQs):                                                          SP labeling for all unsafe APIs, creating two datasets for correlation
                                                                                   analysis. The results revealed six crucial SPs that users need to
                                                                                   satisfy when dereferencing. Next, we classified the existing Rust
Is unsafe an Achilles’ Heel? A Comprehensive Study of Safety Requirements in Unsafe Rust Programming                                              arxiv, 2023,


CVEs based on safety properties, with 196 of 404 resulting from                       2) Call unsafe functions; 3) Implement unsafe traits; 4) Mutate static
unsafe code. Notably, 86.73% of these errors were attributable to                     variables; and 5) Access fields of unions [25]. These operations pro-
misuse of the standard library. Therefore, we conducted a statistical                 vide flexibility but come with the responsibility of the users to
analysis of std unsafe API usage for the Rust ecosystem, which                        manually ensure correctness and safety.
included 103,516 libraries on crates.io. Finally, we conducted user                      Recent empirical research [71] suggests that Rust’s safety mech-
surveys targeting developers with over one year of Rust experience,                   anisms could be more learner-friendly. This study explored the
having written over 5,000 lines of code and using over 1,000 lines                    learning challenges of its safety mechanisms by analyzing Stack
of unsafe code. The evaluations for each SP were rated on four                        Overflow comments and conducting user surveys, but it is restricted
dimensions: precision, significance, usability, and frequency. We                     to Safe Rust. Instead, learning and utilizing Unsafe Rust is a prereq-
received 50 valid responses and conducted data analysis on them.                      uisite for advanced Rust developers.
   Our main contributions are listed as follows:
• We performed the first empirical study by learning unsafe API                       2.2     Undefined Behavior in Rust
  documents from the standard library to classify safety require-                     The undefined behavior in Rust is limited to include [23]:
  ments across unsafe Rust boundaries.                                                • Dereferencing (using the * operator on) dangling or unaligned
• We classified 19 safety properties into two categories. All std-                      raw pointers.
  unsafe APIs were audited and labeled with safety properties. The                    • Breaking the pointer aliasing rules. References and boxes must
  labeled data were evaluated via correlation analysis, yielding                        not be dangling while they are alive.
  interpretable results.                                                              • Calling a function with the wrong call ABI or unwinding from a
• We categorized all Rust CVEs based on safety properties, form-                        function with the wrong unwind ABI.
  ing a collection of related issues that can serve as a benchmark.                   • Executing code compiled with platform features that the current
  Unsafe API usage statistics are collected within crates.io to un-                     thread of execution does not support.
  derstand the usage frequency of unsafe APIs.                                        • Producing invalid values, as explained in Table 2, even in private
• We conducted an online survey and confirmed our categorization                        fields and locals.
  of safety properties with statistical significance.                                 • Mutating immutable data. All data inside a const item, reached
                                                                                        through a shared reference or owned by an immutable binding,
2 BACKGROUND                                                                            is immutable.
2.1 Working with Unsafe Rust                                                          • Causing data races.
                                                                                      • Invoking undefined behavior via compiler intrinsics.
Rust is subdivided into Safe Rust and Unsafe Rust, with Unsafe
                                                                                      • Incorrect use of inline assembly.
Rust being a superset [51]. Safe Rust ensures type and memory
safety, preventing undefined behavior [5]. However, it lacks low-                        This categorization is based on the side effects introduced by
level controls over implementation details (e.g., manual memory                       unsafe code. Since no formal model of Rust’s semantics defines
management). Unsafe Rust is an essential design feature to achieve                    precisely what is and is not permitted in unsafe code [23], additional
low-level control at the system level [25]. It is employed if it has per-             behavior may be deemed vulnerable. In this paper, we additionally
formance requirements or needs to interact with operating systems,                    introduce the following issues as program vulnerabilities if they
hardware, or other programming languages.                                             are triggered by unsafe code:
unsafe Keyword. unsafe keyword can be used in declarations and                        • Causing a memory leak and exiting without calling destructors.
code blocks. The first scenario indicates that the functions cannot                   • Triggering an unreachable path then aborting (or panicking).
be called in the safe code. Misuse may trigger undefined behavior. In                 • Arithmetic overflow.
code blocks, it signifies the scope that may violate safety guarantees
                                                                                         These undefined behavior and vulnerabilities serve as the basis
without compiler-time checks, and the code requires manual audit-
                                                                                      for classifying safety requirements. Other errors fall outside the
ing to ensure safety. This keyword acts as a railing, separating the
                                                                                      scope (e.g., deadlocks and logic errors).
safe and unsafe portions: All unsafe parts are encapsulated within
this scope. The trust relationship between safe and unsafe parts is
                                                                                      3     STUDYING UNSAFE DOCUMENTS IN STD
asymmetric [25]. When using an unsafe block, careful inspection
is required to ensure that the data from the safe portion adheres                     This section presents how we extract and define systematic safety
to the contracts of the unsafe APIs. Conversely, when writing safe                    requirements as Safety Properties (SP) from the existing unsafe
code, it is assumed that the unsafe code is correct and would not                     documents in the standard library [26]. Our classification allows
trigger undefined behavior.                                                           us to clarify the primary conditions and constraints necessary for
unsafe Operations. Safe Rust and Unsafe Rust are designed for dif-                    Unsafe Rust, hence answering RQ1.
ferent scenarios. Safe Rust is a safe programming language designed
for tasks that do not require low-level interactions. Contrariwise,                   3.1     Preprocess on Rust Documents
Unsafe Rust fully leverages the capabilities of a systems-level pro-                  Rustdoc [24] is the document system for the Rust programs, which
gramming language. Unlike languages such as C/C++, which are                          enables the description of functionalities, requirements, expected
inherently unsafe, Unsafe Rust still requires adherence to certain                    results, and sample code snippets for APIs and crates. Intuitively,
contracts from the safe portion, such as ownership. The main dif-                     input requirements and side effects within an unsafe API must be
ferences in Unsafe Rust are that you can 1) Dereference raw pointers;                 explicitly specified in Rustdoc. We found that the document in
arxiv, 2023,                                                                                                                                 Cui et al.


Table 2: Invalid value for Rust types, alone or as a field of a                performed the following preprocessing for all unsafe APIs within
compound type, will trigger undefined behavior.                                std/core/alloc in Rust 1.70, including stable and nightly channels:
                                                                                 FILTER 3.1. For the methods exposed by both core and std, we
       Rust Type     Invalid Value
                                                                               kept only one of them.
          !          Invalid for all values.
        bool         Not 0 or 1 in bytes.                                        FILTER 3.2. For methods belonging to similar numeric types, we
        char         Outside [0x0, 0xD7FF] & [0xE000, 0x10FFFF].               kept only one implementation.
         str         Has uninitialized memory.
  numeric i*/u*/f*   Reads from uninitialized memory.                             FILTER 3.3. For compiler intrinsics, we retained only those with
        enum         Has an invalid discriminant.                              no stable counterpart.
     reference       Dangling, unaligned, or pointing to an invalid value.
                                                                                  As a result, we obtained a collection of unsafe APIs comprising
    raw pointer      Reads from uninitialized memory.
         Box         Dangling, unaligned, or pointing to an invalid value.     416 unsafe methods, with 127 being folded as 11 unique APIs by Fil-
     fn pointer      NULL.                                                     ter 3.2 (e.g., unchecked_mul::<u8>/::<u16> [63, 64] are merged).
                     Has invalid metadata. dyn Trait is invalid if it is not   By applying the preprocessing step, we aimed to streamline and
                     a pointer to a vtable for Trait that matches the actual   consolidate an unsafe API collection for further analysis and inves-
    wide reference
                     dynamic trait the pointer or reference points to, and
                     slice is invalid if the length is not a valid usize.
                                                                               tigation.
     custom type     Has one of those custom invalid values.
                                                                               3.2    What Safety Properties Should We Satisfy?
                                                                               A code audit of all API documents within the collection was con-
the standard library is one of the most comprehensive resources                ducted to determine what safety properties correspond with the
for safety annotations within the Rust ecosystem. We thus audited              design goals. As shown in Table 3, we divided all safety properties
documents of all public unsafe methods within the standard library             into two main categories with 19 subdivisions.
as the knowledge base.
                                                                               3.2.1 Working Procedure. We simultaneously studied documents,
3.1.1 Design Goals. Table 1 reveals that even in the standard li-              defined safety properties, and labeled APIs. Regarding methodology,
brary: (i) the expression of the same safety requirement is not                we performed two rounds of audits, with double-checking from
universally consistent; (ii) the enumeration of the safety require-            the first and second authors. During the audit of each API, we
ments and side effects is not always sufficient. Thus, we manually             focused on five sections: the functionality description, the safety
categorize and define a series of finer-grained safety requirements            description, the subchapters (including outer sections), the example
as Safety Properties (SP), which need to satisfy the following                 code snippets, and the source code with its comments.
design goals:                                                                     First Round: Initial Establishment. We labeled each std unsafe API
                                                                               with SPs that previously existed. The initial set of safety properties
    GOAL 3.1. Generality: SP abstracts safety requirements not spe-
                                                                               was empty. A new SP item was established if a safety requirement
cific to one particular API’s intricacies.
                                                                               emerged and was not recorded in the current set. Therefore, any
  GOAL 3.2. Unambiguous: SP intends to adopt the existing ter-                 newly identified SP should be introduced for the first time dur-
minology and explanations as much as feasible in Rust.                         ing the first-round audit. If there are overlapped SPs, we merged
                                                                               them and re-checked related APIs to determine if they could be
  GOAL 3.3. Nonoverlapping: SP does not overlap, although they
                                                                               consolidated.
may be correlated.
                                                                                  Second Round: Cross Checking. We observed that the API descrip-
  GOAL 3.4. Composability: An Unsafe API’s safety requirements                 tions exhibited variations, including inconsistency and insufficiency.
can comprise several SPs.                                                      In the first round, 19 SPs were finally defined. In the second round,
                                                                               we focused on cross-checking and ensured that all unsafe APIs
  GOAL 3.5. Essentiality: Failure to comply with any SP would
                                                                               were appropriately labeled. We have paid particular attention to
cause undefined behavior or additional vulnerabilities.
                                                                               identifying any missing SP labels for each API that were not initially
   GOAL 3.6. Practicality: SP is valuable and needs to be seriously            captured in the first round.
considered in real-world programming scenarios.                                   In summary, the first round of auditing ensured the complete-
                                                                               ness of SP categorization, while the second round enhanced the
   GOAL 3.7. Unilingual: SP disregards the Foreign Function In-
                                                                               completeness of the required SP labels for each unsafe API.
terface (FFI) and the intrinsic requirements of other programming
languages.                                                                     3.2.2 Categories. We have divided the safety properties into two
                                                                               categories based on the state of the function execution as in program
   By adhering to these principles, the extracted safety properties
                                                                               testing [7], with no overlap between the sub-items.
aim to provide a comprehensive and practical understanding of the
                                                                                  Precondition Safety Property (PRE-SP). The precondition assumes
safety considerations associated with Unsafe Rust. It maintains com-
                                                                               that if the input values do not satisfy the safety requirements, the
patibility with Rust’s existing terminology and avoids unnecessary
                                                                               function call will trigger undefined behavior or additional vulner-
complexities related to FFI.
                                                                               abilities in Section 2.2. Thus, any given API can be regarded as a
3.1.2 Preprocessing. We noticed the redundancy in the standard                 black box for single-step execution [66] at the call site, regardless
library, such as std and core having an intersection. Thus we                  of its internal implementation. PRE-SP complies with the initial
Is unsafe an Achilles’ Heel? A Comprehensive Study of Safety Requirements in Unsafe Rust Programming                                                                                                          arxiv, 2023,


Table 3: Safety properties learned from unsafe API documents in Rust standard library. Precondition and postcondition are two
primary categories, and they have 19 subitems in total. We present the sum of the labeled unsafe API for each safety property
and provide a detailed definition. Each safety requirement was also given a typical unsafe API as an example. Note that each SP
may contain various sub-scenarios.

    Safety Property (SP)                SUM       Definition and the safety requirement of each Safety Property.                                                                       Unsafe API Example
                                                                                              Precondition Safety Property
                                                  Relational operations allow for compile-time determination of the constant numerical
   Const-Numeric Bound                   72                                                                                                         impl<T: ?Sized> *mut T::offset_from
                                                  boundaries on one side of an expression, including overflow check, index check, etc.
                                                  Relational operations involve expressions where neither side is a constant numeric, in-
 Relative-Numeric Bound                 114                                                                                                                 trait Allocator::grow
                                                  cluding address boundary check, overlap check, size check, variable comparison, etc.
                                                  Encoding format of the string, includes valid UTF-8 string, valid ASCII string (in bytes),
            Encoding                     16                                                                                                          impl String::from_utf8_unchecked
                                                  and valid C-compatible string (nul-terminated trailing with no nul bytes in the middle).
                                                  Value stored in the allocated memory, including data in the valid stack frame and allocated
            Allocated                   134                                                                                                    impl<T: Sized> NonNull<T>::new_unchecked
                                                  heap chunk, which cannot be NULL or dangling.
                                                  Value that has been initialized can be divided into two scenarios: fully initialized and
           Initialized                   59                                                                                                       impl<T> MaybeUninit<T>::assume_init
                                                  partially initialized. The initialized value must be valid at the given type (a.k.a. typed).
                                                  The memory range of the given size starting at the pointer must all be within the bounds
        Dereferencable                   96                                                                                                           impl<T: ?Sized> *const T::as_ref
                                                  of a single allocated object.
                                                  Value is properly aligned via a specific allocator or the attribute #[repr], including the
             Aligned                     67                                                                                                            impl<T: ?Sized> *mut T::swap
                                                  alignment and the padding of one Rust type.
                                                  Restriction on Type Layout, including 1) The pointer’s type must be compatible with the
                                                  pointee’s type; 2) The contained value must be compatible with the generic parameter
      Consistent Layout                 110                                                                                                             impl<T: ?Sized> *mut T::read
                                                  for the smart pointer; and 3) Two types are safely transmutable: The bits of one type can
                                                  be reinterpreted as another type (bitwise move safely of one type into another).
                                                  Specific value will trigger unreachable data flow, such as enumeration index (variance),
          Unreachable                     9                                                                                                      impl<T> Option<T>::unwrap_unchecked
                                                  boolean value, closure and etc.
                                                  Restrictions on Exotically Sized Types (EST), including Dynamically Sized Types (DST)
   Exotically Sized Type                 24       that lack a statically known size, such as trait objects and slices; Zero Sized Types (ZST)             trait GlobalAlloc::alloc
                                                  that occupy no space.
                                                  Variables related to the system IO depends on the target platform, including TCP sockets,
           System IO                     25                                                                                                           trait FromRawFd::from_raw_fd
                                                  handles, and file descriptors.
                                                  Types that can be transferred across threads (Send) or types that can be safe to share
             Thread                       3                                                                                                                   std::marker::Sync
                                                  references between threads (Sync), respectively.
                                                                                             Postcondition Safety Property
                                                  Multiple owners (overlapped objects) that share the same memory in the ownership
          Dual Owner                     31                                                                                                                                  impl<T: ?Sized> Box<T>::from_raw
                                                  system by retaking the owner or creating a bitwise copy.
                                                  Aliasing and mutating rules may be violated, including 1) The presence of multiple
                                                  mutable references; 2) The simultaneous presence of mutable and shared references, and
    Aliasing & Mutating                  30                                                                                                                                             impl CStr::from_ptr
                                                  the memory the pointer points to cannot get mutated (frozen); 3) Mutating immutable
                                                  data owned by an immutable binding.
                                                  Arbitrary lifetime (unbounded) that becomes as big as context demands or spawned
            Outliving                    28                                                                                                                                impl<T: ?Sized> *const T::as_uninit_ref
                                                  thread, may outlive the pointed memory.
                                                  Value may not be in the initialized state, or the byte pattern represents an invalid value
            Untyped                      20                                                                                                                                              core::mem::zeroed
                                                  of its type.
              Freed                      17       Value may be manually freed or released by automated drop() instruction.                                               impl<T: ?Sized> ManuallyDrop<T>::drop
             Leaked                      13       Value may be leaked or escaped from the ownership system.                                                                   impl<T: ?Sized> *mut T::write
             Pinned                       5       Value may be moved, although it ought to be pinned.                                                                     impl<P: Deref> Pin<P>::new_unchecked
  1 Send [53] and Sync [54] are unsafe traits (markers) that are automatically implemented by the compiler when it determines that they are required. Therefore, they lack associated methods.
  2 The difference between DualOwner and AliasingMutating is that DualOwner only focuses on objects instead of pointers and references.




characteristic of unsafe function (i.e., it cannot ensure safety for                                                       The PRE-SP items are not nonoverlapping within POS-SPs through
arbitrary inputs). In Table 3, we summarize 12 PRE-SPs. For exam-                                                       this separation. It can be verified by a Rust design, where creating
ple, swap [60] has the description "Both x and y must be properly                                                       raw pointers is always safe, but dereferencing them is unsafe [23].
aligned.", thus categorized into Aligned.                                                                               Similarly, we assume that PRE-SPs only affect the safety of function
   Postcondition Safety Property (POS-SP). The previous assumption                                                      calls, while POS-SPs focus on the subsequent usage of inputs and
leads to the deduction that the function can be safely called if the                                                    return values. Furthermore, POS-SPs are only considered under
proper inputs are supplied. However, this assurance only concerns                                                       the premise that all PRE-SPs are satisfied. Specifically, we merged
the current program point. POS-SP focuses on the potential safety                                                       Aliasing and Mutating based on the ground truth that all relevant
issues that may arise from the subsequent operations, assuming that                                                     APIs shared the same labels in these items. We empirically inferred
the input values satisfy all PRE-SPs needed. In Table 3, we finally                                                     that the primary side effect of breaking Aliasing rules is erro-
summarize 7 POS-SPs. For example, zeroed [56] has the description                                                       neously Mutating immutable data. We empirically inferred that
"There is no guarantee that an all-zero byte-pattern represents a valid                                                 the primary side effect of breaking Aliasing rules is erroneously
value of some type T.", thus categorized into Untyped.                                                                  Mutating immutable data.
arxiv, 2023,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      Cui et al.




         ConstBound 1.00                                                                                                                               0.26
                                                                                                                                                                                                                                                                 1.0         ConstBound 1.00
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  1.0
      RelativeBound                   1.00                       0.48                      0.24                                                                                                                                                                           RelativeBound                1.00                       0.43                      0.36 0.32 0.31                                                                         0.22                                       0.30
           Encoding                                   1.00                                                                                                                                                                                                       0.9           Encoding                                1.00                                                                                                                                                                                                       0.9
          Allocated                   0.48                       1.00                      0.57 0.40 0.49                                                                         0.31                                       0.21              0.20                           Allocated                0.43                       1.00                      0.65 0.50 0.67                                                                         0.39                                       0.28              0.23
                                                                             1.00                           0.31 0.28                                                    0.20 0.24 0.22 0.24                                                                                                                                                  1.00                                                                                        0.23                                    0.20
        Initialized
                                                                                                                                                                                                                                                                 0.8        Initialized
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0.8
    Dereferencable                    0.24                       0.57                      1.00 0.56 0.54                                                                         0.27 0.33 0.35 0.29                                          0.26                      Dereferencable                0.36                       0.65                      1.00 0.49 0.48                                                                0.21 0.25 0.26 0.30 0.35                                              0.25
               Aligned                                           0.40 0.31 0.56 1.00 0.69                                                                                         0.45 0.51 0.54 0.35                                                                           Aligned                0.32                       0.50                      0.49 1.00 0.67                                                                         0.52 0.39 0.44 0.39
  ConsistentLayout                                               0.49 0.28 0.54 0.69 1.00                                                                                         0.40 0.39 0.37 0.26                                          0.25              0.7   ConsistentLayout                0.31                       0.67                      0.48 0.67 1.00                                                                         0.43 0.32 0.29 0.28                                          0.23              0.7
        Unreachable                                                                                                                      1.00                                                                                                                               Unreachable                                                                                                                   1.00
                   EST 0.26                                                                                                                            1.00                                                                            0.23                      0.6                EST                                                                                                                                 1.00                                                                            0.24                      0.6
           SystemIO                                                                                                                                           1.00                                                                                                             SystemIO                                                                                                                                        1.00
                Thread                                                       0.20                                                                                        1.00                                                                                                    Thread                                                       0.23 0.21                                                                                   1.00                 0.25 0.27
                                                                                                                                                                                                                                                                 0.5                                                                                                                                                                                                                                                              0.5
          DualOwner                                              0.31 0.24 0.27 0.45 0.40                                                                                         1.00                                       0.36                                             DualOwner                0.22                       0.39                      0.25 0.52 0.43                                                                         1.00                                       0.41
  AliasingMutating                                                           0.22 0.33 0.51 0.39                                                                                              1.00 0.92                                                                AliasingMutating                                                                     0.26 0.39 0.32                                                                0.25                 1.00 0.86
          Outliving                                                          0.24 0.35 0.54 0.37                                                                                              0.92 1.00                                                          0.4          Outliving                                                       0.20 0.30 0.44 0.29                                                                         0.27                 0.86 1.00                                                          0.4
               Untyped                                           0.21                      0.29 0.35 0.26                                                                         0.36                                       1.00              0.28                             Untyped                0.30                       0.28                      0.35 0.39 0.28                                                                         0.41                                       1.00              0.27
                 Freed                                                                                                                                 0.23                                                                            1.00                      0.3              Freed                                                                                                                                 0.24                                                                            1.00                      0.3
                Leaked                                           0.20                      0.26                       0.25                                                                                                   0.28              1.00                              Leaked                                           0.23                      0.25                       0.23                                                                                                   0.27              1.00
                Pinned                                                                                                                                                                                                                                  1.00                     Pinned                                                                                                                                                                                                                                  1.00
                                                                                                                                                                                                                                                                 0.2                                                                                                                                                                                                                                                              0.2
                         ConstBound
                                      RelativeBound
                                                      Encoding
                                                                 Allocated




                                                                                                                                                       EST
                                                                             Initialized


                                                                                                            Aligned
                                                                                           Dereferencable


                                                                                                                      ConsistentLayout
                                                                                                                                         Unreachable


                                                                                                                                                              SystemIO
                                                                                                                                                                         Thread
                                                                                                                                                                                  DualOwner


                                                                                                                                                                                                                 Outliving
                                                                                                                                                                                                                             Untyped
                                                                                                                                                                                                                                       Freed
                                                                                                                                                                                                                                               Leaked
                                                                                                                                                                                                                                                        Pinned
                                                                                                                                                                                              AliasingMutating




                                                                                                                                                                                                                                                                                          ConstBound
                                                                                                                                                                                                                                                                                                       RelativeBound
                                                                                                                                                                                                                                                                                                                       Encoding
                                                                                                                                                                                                                                                                                                                                  Allocated




                                                                                                                                                                                                                                                                                                                                                                                                                        EST
                                                                                                                                                                                                                                                                                                                                              Initialized


                                                                                                                                                                                                                                                                                                                                                                             Aligned
                                                                                                                                                                                                                                                                                                                                                            Dereferencable




                                                                                                                                                                                                                                                                                                                                                                                                          Unreachable


                                                                                                                                                                                                                                                                                                                                                                                                                               SystemIO
                                                                                                                                                                                                                                                                                                                                                                                                                                          Thread
                                                                                                                                                                                                                                                                                                                                                                                                                                                   DualOwner


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  Outliving
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              Untyped
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        Freed
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                Leaked
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Pinned
                                                                                                                                                                                                                                                                                                                                                                                       ConsistentLayout




                                                                                                                                                                                                                                                                                                                                                                                                                                                               AliasingMutating
      (a) Correlation analysis results on the large dataset (original).                                                                                                                                                                                                   (b) Correlation analysis results on the small dataset (filtered).

Figure 2: Correlation matrices for both the large and small datasets. Each figure only includes the sections with weak correlation
and above (correlation greater than 0.2).


3.3      Correlation Analysis on Safety Properties                                                                                                                                                                                                                       • Functions with the same name implemented for different types
We obtained a valuable dataset after completing the labeling for                                                                                                                                                                                                           within the same namespace.
unsafe API collection. Although one of our design goals focuses                                                                                                                                                                                                          • Encapsulation of intrinsic functions.
on nonoverlapping, it is still necessary to investigate potential
correlations between different SPs. This notion is from the empirical                                                                                                                                                                                                    3.3.2 Correlation Matrix. As depicted in Figure 2, we built cor-
intuition that data satisfying Dereferenceable should always meet                                                                                                                                                                                                        relation matrices for both the large and small datasets, retaining
Allocated.                                                                                                                                                                                                                                                               only the elements with moderate correlation and above (correlation
                                                                                                                                                                                                                                                                         coefficient > 0.20). The large dataset has a higher susceptibility to
3.3.1 Methodology. We conducted a correlation analysis based on                                                                                                                                                                                                          interference from redundant APIs. For example, there are 30 im-
two datasets, and their results demonstrate the anticipated differ-                                                                                                                                                                                                      plementations of the trait SliceIndex<[T]> [62], all of which are
ences. We will explain their characteristics first and then discuss                                                                                                                                                                                                      labeled with RelativeBound and Allocated only. The correlation
the results of both datasets.                                                                                                                                                                                                                                            between them is thus higher in the large dataset, changing from 0.43
    Large Dataset. The large dataset directly uses the original collec-                                                                                                                                                                                                  to 0.48. In the small dataset, the diverse functionality among APIs
tion with labeled data, which includes the entire set of unsafe APIs.                                                                                                                                                                                                    is more likely to result in the loss of pertinent data that could affect
The labels of functionally related APIs may be similar. The intent                                                                                                                                                                                                       correlations. For example, the small dataset’s correlation between
of keeping a large dataset is to emphasize the quantity, as having                                                                                                                                                                                                       Aligned and AliasingMutating decreases from 0.51 to 0.39. At
adequate data can expose potential correlations.                                                                                                                                                                                                                         last, Encoding, Unreachable, SystemIO, and Pinned achieve the
    Small Dataset. The small dataset is created by applying additional                                                                                                                                                                                                   best independence, as they have no substantial correlation with
filter (Filter 3.4) to the large dataset. This is done to counteract                                                                                                                                                                                                     any other SPs in both matrices.
the potential bias from excessive similar APIs. The small dataset                                                                                                                                                                                                           Case Study. Based on two diagrams in Figure 2, we extracted all
intends to eliminate the redundancy of potentially irrelevant data                                                                                                                                                                                                       the pairs with at least a moderate CC, as listed in Table 4. Among
and concentrate on diversity.                                                                                                                                                                                                                                            the six pairs with no POS-SPs, we empirically found that they are
                                                                                                                                                                                                                                                                         related to dereferencing operations. Although dereferencing was
  FILTER 3.4. APIs must have the same labels and satisfy at least
                                                                                                                                                                                                                                                                         not considered a distinct item in the SP category, such operations
one of the following requirements:
                                                                                                                                                                                                                                                                         are pervasive in the inner code of unsafe methods. We inferred
• Implementations of the same method with different mutability.                                                                                                                                                                                                          knowledge about safety requirements for dereferencing that was
• Implementations of the same trait for different types, including                                                                                                                                                                                                       not explicitly categorized: The first-class SP for a valid pointer with
  mono-morphizations in the trait or struct definitions.                                                                                                                                                                                                                 the highest priority is Allocated, followed by Dereferencable,
Is unsafe an Achilles’ Heel? A Comprehensive Study of Safety Requirements in Unsafe Rust Programming                                                                arxiv, 2023,


Table 4: SP pairs with correlation coefficients (CC) greater
                                                                                          Listing (3) Source code of CVE-2021-45709 in the crypto2 crate
than 0.4 both in the large and small dataset correlation ma-                              through 2021-10-08 for Rust.
trices.
                                                                                           1     #[inline]
      SP1              SP2         AVG-CC           SP1              SP2        AVG-CC     2     fn xor_si512_inplace(a: &mut [u8], b: &[u32; Chacha20::
                          Precondintion Safety Properties ONLY                                         STATE_LEN]) {
   Allocated      RelativeBound     0.455        Allocated     Dereferencable    0.615     3         unsafe {
   Allocated     ConsistantLayout   0.580        Allocated         Aligned       0.450     4             let d1 = core::slice::from_raw_parts_mut(a.
 Dereferencable      Aligned        0.525     Dereferencable ConsistantLayout    0.510
                                                                                                       as_mut_ptr() as *mut u32, Chacha20::STATE_LEN);
    Aligned      ConsistantLayout   0.685
           Precondintion Safety Properties with Postcondition Safety Properties
                                                                                           5             for i in 0..Chacha20::STATE_LEN {
  DualOwner          Aligned        0.485       DualOwner     ConsistantLayout   0.415     6                 d1[i] ^= b[i];
   Outliving         Aligned        0.490        Outliving    AliasingMutating   0.895     7             }
                                                                                           8         }
                                                                                           9     }


ConsistentLayout, and Aligned. RelativeBound should be con-
                                                                                               Listing (4) Description documented in RUSTSEC-2021-0121.
sidered if it has pointer arithmetic. Even though Initialized is
                                                                                           1     Description
not stated in Table 4, we still view it as a prerequisite for derefer-                     2     The implementation does not enforce alignment requirements
encing, as Rust’s undefined behavior has explicit requirements for                         3     on input slices while incorrectly assuming 4-byte alignment
valid values of raw pointers. In this paper, we advocate for the safe                      4     through an unsafe call to std::slice::from_raw_parts_mut,
                                                                                           5     which breaks the contract and introduces undefined behavior.
usage of raw pointers by satisfying these 6 PRE-SPs.

4     VERIFYING REAL-WORLD UNSAFE CODE                                                   Figure 3: Example of the CVE classification. The buggy source
This section presents the practical usability of our classification                      code and description of CVE-2021-45709 (in RUSTSEC). This
in real-world scenarios and the frequency of unsafe API usage in                         CVE violates the safety requirement of Aligned and triggers
the Rust ecosystem. We classify existing CVEs [19] to validate SP                        UB when using the unsafe API slice::from_raw_parts_mut.
coverage and conduct a statistical analysis of unsafe API usage on
crates.io [21].                                                                                                                               70
                                                                                          70                                                                                 2023
4.1     Classifying Existing Unsafe CVEs                                                  60
                                                                                                                                                                             2022
4.1.1 Workflow. The workflow consists of two primary steps: Cre-                          50
ate a database of CVEs caused by misusing unsafe cust and classify                                                                                                           2021
them into safety properties by manual code review.                                        40
                                                                                                                   34                                                        2020
   CVE Set. We employed the CVE dataset from the CVE program                              30
(https://cve.mitre.org) and searched on the CVE list using the key-                                   23                                                                     2019
word "Rust". The results are sorted by CVE ID in chronological                            20
                                                                                                                            14                           12
order (i.e., submission date). The final CVE dataset ranged from                                                                 11                                          2018
                                                                                          10               8
                                                                                                               5                                   5 7        4
CVE-2017-20004 [12] to CVE-2023-30624 [14]. We initially filtered                                 2                     0             0 0 0                       0 0 0
CVE based on CVE descriptions, primarily retaining memory-safety                           0                                                                                 2017
                                                                                                           Aligned




                                                                                                 AliasingMutating
                                                                                                         Outliving
                                                                                                    RelativeBound
                                                                                                         Encoding
                                                                                                         Allocated
                                                                                                        Initialized
                                                                                                   Dereferencable


                                                                                                      Unreachable
                                                                                                                EST
                                                                                                         SystemIO




                                                                                                            Pinned
                                                                                                      ConstBound




                                                                                                            Thread
                                                                                                       DualOwner


                                                                                                          Untyped
                                                                                                             Freed
                                                                                                           Leaked
                                                                                                 ConsistentLayout




issues. Unrelated CVEs were removed, such as leaking sensitive
information. We filtered those CVEs triggered in the panic path
because this study does not specifically work for panic safety [25].
Additionally, the retained CVEs cannot be located in a deprecated
or yanked crate and should have a link to the source code to support
a code audit.
   CVE Audit. We performed a manual audit of error snippets that                         Figure 4: SP classification results and their duration on ex-
led to security issues. The first and second authors double-checked                      isting Rust CVEs. These CVEs are memory-safety issues re-
the results. We painstakingly investigated whether misusing unsafe                       sulting from misusing unsafe code and ignoring unrelated
code was the root cause of each CVE. Due to the short descriptions                       issues, such as leaking sensitive information.
provided on the CVE website, we utilized various sources, including
issues, pull requests, contributors (e.g., RUSTSEC [27]), and fixed
code, to pinpoint the source code related to each CVE. Any CVEs                             CVE Example. Figure 3 presents an example of a classified CVE
that did not satisfy the front criteria were removed from our dataset.                   derived from CVE-2021-45709 [2, 13]. Based on the explicit error
Around 86.73% of the 196 CVEs in the final dataset were attributed                       description in its issue, we were able to locate the buggy source
to misusing unsafe APIs from the standard library. In contrast, the                      code and confirm incorrect usage of from_raw_parts_mut [61].
remaining CVEs were caused by dereferencing raw pointers, using                          This API was annotated by the following SPs: ConstBound, Rela-
non-std unsafe functions, or outside FFI. Based on the descriptions                      tiveBound, Allocated, Dereferencable, Aligned, ConsistantLayout,
and code reviews, we further classified each CVE into the SPs it                         AliasingMutating, and Outliving. This CVE violates the requirement
violated.                                                                                of Aligned, leading to undefined behavior.
arxiv, 2023,                                                                                                                                      Cui et al.


Table 5: Open-source code analyzers that can detect specific               5k   4,924 159,755                                            crates contain 160k
SPs. Each static bug detection tool may not necessarily sup-                                                                             occurrences
port all scenarios related to the corresponding SP.                                                                                                     140k
                                                                           4k
                                                                                 111,223                                                                 120k
          Tool       Supported SPs of Each Static Analyzer
                                                                           3k         2,838                                                              100k
       Rudra [6]     Thread, DualOwner, Initialized
                                                                                                                                                         80k
    SafeDrop [11]    Allocated, DualOwner, Freed, Initialized              2k
                                                                                              2,070
                                                                                                      1,832                                              60k
                     Const-Numeric Bound, Relative-Numeric Bound,
                                                                                                              1,611 1,491
  MirChecker [38]
                     DualOwner                                                                 32,186                       1,183 1,168 1,030            40k
                                                                           1k
                                                                                                     21,270                                674     20k
  FFIChecker [39]    Allocated, Leaked (Rust/C FFI Only, based on LLVM)
                                                                                                                9,31911,7934,589 6,251 5,193
                                                                                                                                             1,575
     rCanary [3]     Leaked                                                 0                                                                            0




                                                                                      he ing



                                                                                       p_i oc

                                                                                                    e
                                                                                         fro e
                                                                                                 ptr

                                                                                      as roed

                                                                                          c t
                                                                               py _unc ed
                                                                             ge ove ked



                                                                                                  ut
                                                                                                   i




                                                                                               lac
                                                                                                  t




                                                                                    w_ _in
                                                                                              mu




                                                                                              _m

                                                                                    dro all
                                                                                                k
                                                                                             m_




                                                                                   nc pp
                                                                                   ge hec

                                                                                              c




                                                                                           n_p
                                                                                  ne ume
                                                                                            ze




                                                                                 _no he



                                                                                           ed
                                                                                           ns




                                                                                t_u rla
                                                                                        ck
                                                                          tra




                                                                                       un
                                                                                        s
4.1.2 Results and Benchmark. We conducted a study on 404 CVE




                                                                                     t
                                                                                    n
descriptions and performed a code review on the remaining 196
CVEs after filtering. We classified them based on SP categorization




                                                                            co
and analyzed their distribution. It has been manually verified that
the causes of these CVEs do not exceed our SP classification. Finally,    Figure 5: Statistics results on unfiltered strings (unsafe APIs)
we generated a benchmark encompassing the various SPs in the              in the crates.io ecosystem. The top ten most frequently used
identified CVEs.                                                          strings across all repositories and their source code occur-
    SP and Time-span Distribution. Figure 4 depicts the classification    rences sorted by the sum of crates.
results. RelativeBound, Initialized, and Thread had a signifi-
cant number of CVEs (at least 23). Following them, there are fewer
CVEs associated with Aligned, Outliving, ConsistentLayout,
                                                                          by specific bug patterns. This observation suggests that analyzers
and the other 6 SPs (ranging from 2 to 14). 7 SPs have no corre-
                                                                          designed for bug patterns may effectively identify vulnerabilities
sponding CVEs. Except for ConsistentLayout, ConstBound, and
                                                                          that violate specific SPs. On the other hand, many undiscovered
Allocated, the time span of CVEs for each SP ranges from as early
                                                                          vulnerabilities related to specific SP may not have been registered
as August 2019 to as late as December 2021 from a temporal per-
                                                                          on https://cve.mitre.org.
spective. This period contains approximately 91.84% of listed CVEs.
    Benchmark on SP. Our classification results provide a set of CVE
lists for each SP that can be used as a benchmark. This benchmark
                                                                          4.2    Statistics on crates.io Ecosystem
can be employed to evaluate the effectiveness of research prototypes      The findings from Section 4.1 indicate that 86.73% of the classified
or bug-detection tools designed for particular SPs. As far as we          CVEs were caused by misusing unsafe APIs in std. This observation
know, the Rust community needs a unified, ground-truth-supported          prompted us to conduct a statistical analysis of the usage of unsafe
benchmark to support effectiveness comparisons based on safety            APIs within the Rust ecosystem.
issues. We advocate for setting such a benchmark to serve as a basis
                                                                          4.2.1 Open-source Crates Database. As crates.io is the crate man-
for the community. We also list some open-source code detection
                                                                          agement platform in the Rust community, we used all its reposito-
tools for Rust programs, all of which serve for specific SPs, as shown
                                                                          ries to serve as a code database. To evaluate the frequency of unsafe
in Table 5.
                                                                          API usage, we matched regular expressions to source code without
    Case Study. The most CVEs were caused by Thread (70) viola-
                                                                          compilation. Using function name as the criterion, we merged iden-
tions. This is predominantly the result of user-defined types that        tical unsafe APIs, creating a dictionary of 140 unique unsafe API
unconditionally implement the Send [53]/Sync [54] traits or fail to       strings. Then we removed 20 strings that have the same name as
ensure that Send/Sync implementations have the correct bounds.            other safe functions in the std (e.g., add [57, 58]). To improve the
Such violations may result in data races and memory-safety issues         accuracy of the statistics, we only included per-file instances if the
across the thread boundaries. Initialized (37) was the second             unsafe keyword was used in the source code.
most common SP, and its typical scenarios are as follows: 1) Create
an uninitialized buffer and pass it to the user-defined Read [59]         4.2.2 Frequency Statistics. As of 2023-01-30, we mined all the lat-
implementation, allowing safe code to read uninitialized memory;          est crates from crates.io. The statistic indicates that 21,506 crates
2) Increase buffer length without reserving memory, causing write-        use Unsafe Rust among the 103,516 crates on crates.io (3,614 are
out-of-bound or dropping uninitialized memory issues; 3) Create           yanked). For each string, we collected a statistical summary, includ-
an uninitialized NonNull pointer.                                         ing the number of crates in which the string appears and the total
    Discussion. We observed that the statistic in Figure 4 may not        usage count of the string across all crates. The top ten most fre-
accurately reflect the frequency of SP usage in the real world. For       quently used strings are listed in Figure 5, which depicts statistical
example, a significant portion of CVEs on Initialized (85.3%) and         results in two dimensions. We observed that the primary scenarios
Thread (92.9%) were discovered by the sslab-gatech using their            encompass type conversions (transmute), manual memory man-
static analyzer Rudra [6], which is designed to detect bugs inspired      agement (zeroed, alloc, drop_in_place), unsafe constructors
Is unsafe an Achilles’ Heel? A Comprehensive Study of Safety Requirements in Unsafe Rust Programming                                                                                                                      arxiv, 2023,


(new_unchecked), deferred initialization (assume_init), unsafe in-                                       Q1-Negative               Q2-Negative                          Q3-Negative                           Q4-Negative
                                                                                                         Q1-Neutral                Q2-Neutral                           Q3-Neutral                            Q4-Neutral
dexing (get_unchecked/mut), unsafe referencing (from_ptr), and                                           Q1-Positive               Q2-Positive                          Q3-Positive                           Q4-Positive
unsafe memory copies (copy_nonoverlapping). Note that the re-
                                                                                                9               15                 26        2                     20                              28
sults presented above do not account for filtered strings (e.g., read,                      6                 18                   26                     15                       17                     18
                                                                                                                                                                                                                    ConstBound

as_mut, from_raw, etc.).                                                                    6                 16               28                3             16                              31
                                                                                                                                                                                                                    RelativeBound
                                                                                         5                15                  30                         14                       16                     20

                                                                                            6                 16               28            2                16                               32
5     SURVEYING RUST PROGRAMMERS                                                         5                16                   29                    10                 10                         30
                                                                                                                                                                                                                    Encoding

In this section, we conducted an online survey on Goldendata [20]                           7                 16               27            2            12                                  36
                                                                                                                                                                                                                    Allocated
                                                                                        4                15                   31                 5                 15                              30
to evaluate the Safety Properties in precision, significance, usability,
                                                                                            7                 15               28                5                  18                              27
and frequency from the perspective of experienced Rust developers.                                                                                                                                                  Initialized
                                                                                         5                16                   29                    8                   17                         25

                                                                                         5                16                   29            2                14                              34
                                                                                                                                                                                                                    Dereferencable
5.1     Methodology                                                                         7              13                 30                         12                   16                        22

                                                                                                    14                   16             20           6                  18                          26
5.1.1 Recruitment. We require participants to be at least 18 years                              11                  16              23                        18                         20                    12
                                                                                                                                                                                                                    Aligned

old with a minimum of 1 year of experience in Rust programming                              7                   19                 24            4                 17                              29
                                                                                                                                                                                                                    ConsistentLayout
and to have written at least 5,000 lines of Rust code, including over                   4                  19                  27                        14                        18                     18

1,000 lines of unsafe code. We posted our survey on the Rust-related                            9             11              30                     7                   21                             22
                                                                                                                                                                                                                    Unreachable
                                                                                             8                     20               22                        20                         15                   15
community to recruit volunteers and emailed contributors from
                                                                                         5                    18               27            2                          26                              22
Rust-lang and the popular repositories on crates.io.                                    4                  19                  27                        14                         21                        15
                                                                                                                                                                                                                    EST

                                                                                            6             14                  30             2                 19                                  29
5.1.2 Procedure. We provide each defined SP with a representative                       4                     22                   24                    14                   13                        23
                                                                                                                                                                                                                    SystemIO

unsafe API for participants on each page. Note that the relationship                        7                  18                  25        1                18                               31
                                                                                                                                                                                                                    Thread
between API and SP is many-to-many. Hence, the given API only                            5                    20                   25                     16                       14                    20

targets one SP. For each API, we further supply a triplet (𝑆, 𝑃 1, 𝑃2 ),                        9                   20              21               7                  16                          27
                                                                                                                                                                                                                    DualOwner
                                                                                            7                      20               23                    16                       15                    19
containing a document slice 𝑆 for the current SP, a sound code
                                                                                            7                      22               21       2                      23                              25
snippet 𝑃1 , and a misused PoC 𝑃2 . 𝑃1 and 𝑃2 are carefully designed                        6                   21                  23                    16                       15                    19
                                                                                                                                                                                                                    AliasingMutating

to be short and easy to debug. 𝑃2 violates the safety requirements                          6             14                  30                 4             13                              33
                                                                                                                                                                                                                    Outliving
of the current SP, ensuring that all other SPs are satisfied. We link                       6                 16               28                        12                   17                         21

𝑆 to the online document for referencing, and both 𝑃 1 and 𝑃2 can                       4                  19                  27                4             14                              32
                                                                                                                                                                                                                    Untyped
                                                                                        3                 19                   28                        13                  12                     25
be redirected to the Rust Playground [22] for online execution.
                                                                                            6                 18                   26        1                18                               31
Furthermore, 18 out of 19 𝑃2 will trigger UB that can be captured                       3                16                   31                     8              12                             30
                                                                                                                                                                                                                    Freed

by Miri [9], making it easier for participants to understand issues.                        7             11                  32             0                20                                   30
                                                                                                                                                                                                                    Leaked
   Participants must read the definition and the triplet of each SP.                        6                 16               28                    8                  14                         28

Then we ask them four questions listed below:                                                   9                  17              24        2                15                               33
                                                                                                                                                                                                                    Pinned
                                                                                        3                     22                   25                    12                    19                        19

• Q1: We asked participants to rank the accuracy of SP definitions.
  Can the safety requirements of each SP be explained in a concise
  and precise definition?                                                             Figure 6: Survey results on Unsafe Rust programmers. Pre-
• Q2: We asked participants to rank the significance of each SP.                      cision, significance, usability, and frequency are the four
  Does violating each SP lead to unacceptable issues? Is it necessary                 dimensions rated for each SP. Positivity, neutrality, and neg-
  to document such requirements explicitly in Rustdoc?                                ativity are the options for each dimension.
• Q3: We asked participants to rank the usability of each SP. Should
  users consider the context of SP satisfaction in real-world unsafe
  programming? Does adhering to each SP help write sound code?                        response included excluding surveys with excessively short com-
• Q4: We asked participants to rank the frequency of each SP. How                     pletion times (less than 15 minutes), the same pattern throughout
  frequently do they encounter situations that require careful use of                 the entire survey, and responses inconsistent with Rust facts.
  this SP? Is it often considered when crossing unsafe boundaries?                       Q1: Precision Ratings. The results of Q1 illustrate participants’
                                                                                      comprehension and endorsement of SP definitions, providing an
   For each of the four questions, we have devised a [−1, 1] scoring
                                                                                      in-depth appraisal of Goal 3.1 to 3.4. The score distribution is
scale to represent negative, neutral, and positive responses. It is
                                                                                      [6, 25], with a mean of 19.3, a standard deviation of 4.8, and 16
crucial to note that these four questions have no objectively cor-
                                                                                      SPs scored greater than 15. We observed that SPs with brief descrip-
rect answers. The participants’ responses may vary based on their
                                                                                      tions tended to receive higher scores such as SystemIO (24) and
unique perspectives and experiences.
                                                                                      Leaked (25). Whereas SPs with subcategories had a lower score
                                                                                      due to the comprehension threshold, such as ConsistentLayout
5.2     Survey Results                                                                (17) and AliasingMutating (14). Participants exhibited a compar-
We distributed the survey between July 10 and July 25, 2023, and                      atively negative attitude toward unusual SPs, specifically Aligned
received 90 responses. After review by the first and second au-                       (6). They are also unclear about the newly introduced categories
thors, it was determined that 50 were valid. The criteria for a valid                 like DualOwner (12). In the optional supplementary comments, 4
arxiv, 2023,                                                                                                                             Cui et al.


participants emphasize the necessity for the document to highlight         various measures were implemented. First, we utilized multiple
the side effects caused by violating DualOwner.                            recruitment channels, such as private email invitations. Second,
   Q2: Significance Ratings. The results of Q2 indicate their perspec-     we clearly outlined the mandatory requirements for programming
tives on the safety issues caused by violating each SP, in accordance      experience. Third, the first and second authors manually verified
with Goal 3.5. The score distribution is [15, 34], with a mean of 26.3,    all the responses. Fourth, we imposed restrictions on the number
a standard deviation of 5.0, and 18 SPs scored greater than 20. We         of submissions from the same IP address.
noticed that participants tend to be positive concerning memory               For external validity threats, due to the ongoing development of
safety. Rust developers devote particular attention to memory safety       Rust, the programming style and usage of Unsafe Rust may evolve
and evince a predictable sensitivity to the safety requirements of         over time. Despite considering both stable and nightly channels,
unsafe code. However, an exception existed, which is Unreachable           future updates may introduce new unsafe APIs, modify API descrip-
(15). The majority of participants viewed Unreachable as an incon-         tions and implementations, or even deprecate some unsafe APIs. We
sequential problem and instinctively assumed that panic is always          also acknowledge the existence of uncommon safety descriptions
memory-safe, losing focus on potential threats to panic safety.            that cannot be classified based solely on the std unsafe documents
   Q3: Usability Ratings. The results of Q3 represent the sensitiv-        or existing CVEs because they have not been documented in any
ity to the context when crossing unsafe boundaries in real-world           std unsafe document or existing CVE.
unsafe programming, thus addressing Goal 3.6. The score distri-
bution is [12, 28], with a mean of 21.4, a standard deviation of 4.2,      7   RELATED WORK
and 15 SPs scored greater than 20. Notably, there is a significant         Empirical Studies on Rust Security. Researchers have conducted
correlation between the scores in Q2 and Q3. It can be explained by        empirical studies to understand how to use Unsafe Rust from real-
assuming that users may be less likely to check the requirements           world Rust Programs [5, 17, 50, 51, 70] and existing CVEs [69].
in real-world situations if they perceive one SP as insignificant.         They summarize valuable bug patterns and provide insights into
Conversely, if their programs are less affected by one SP in practice,     different aspects of safety guarantees. However, these studies do
they may perceive it as unimportant, which is consistent with their        not extract safety requirements from the safety descriptions in the
intuition. We observed that 89.4% of the Q2 scores are higher than         API documents. Several empirical studies focus on the Rust learn-
Q3, indicating that participants may have a higher awareness of            ing curve [1, 18] and the programming challenges introduced by
significance than programming habits in real-world practice.               compiler errors [71]. Researchers also leveraged Rust-related Stack
   Q4: Frequency Ratings. The results of Q4 reveal the frequency           Overflow data to understand real-world development problems [71].
with which Rust developers encounter each SP in unsafe program-            However, we are more concerned with experienced system engi-
ming. The score distribution is [−6, 25], with a mean of 8.6 and a         neers who are proficient than Rust beginners. They need Unsafe
standard deviation of 8.8. These responses further validated the           Rust to achieve low-level control and better understand the safety
results in Section 4.2, which measured the frequency of unsafe             requirements when crossing unsafe boundaries.
API usage in crates.io. We found significant discrepancies in the          Bug detection methods in Rust. As a strongly typed program-
score distribution for this question. It shows that Allocated (25),        ming language, formal verifications for Rust have received con-
Freed (22), Leaked (20), and Initialized (17) are encountered              siderable attention [4, 10, 15, 28, 29, 31, 32, 35, 42, 68]. Existing
more frequently in Unsafe Rust. We infer that these SPs are tightly        studies also employ static or dynamic analysis to detect bugs in
connected with common scenarios, including manual memory man-              Rust programs, including symbolic execution [8, 40], model check-
agement and deferred initialization. As for Encoding (20), users           ing [6, 11, 38, 65, 67], interpreter [9], and fuzzing [16, 30]. We have
may use it frequently to interact with C code in unsafe contexts.          discovered that some of the above prototypes analyze errors based
For SPs with lower or even negative scores, we suggest that the            on bug patterns corresponding to our SP categorization. Table 5
Rust developers and community may need to pay more attention               illustrates the relationship between the relevant tools and their
to avoid misusing them.                                                    supported SPs. At last, we believe this paper will encourage re-
   The survey results confirmed our classification of safety proper-       searchers and developers to focus on diverse safety requirements
ties with statistical significance. It is necessary to define a systemic   when handling unsafe boundaries. In the future, more testing tools
classification, as experienced Rust programmers highly care about          can be developed to aid in the detection of safety violations for
memory safety issues caused by unsafe code. At last, it also reveals       different SPs.
a significant variation in the occurrence frequency of different SPs
in real-world Rust programs.
                                                                           8   CONCLUSION
                                                                           As Rust is a system programming language, Unsafe Rust is integral
6     THREATS TO VALIDITY                                                  to achieving low-level control over implementation details. With
For internal validity threats, using std unsafe documents as our           increasing system software adopting Rust, understanding the safety
knowledge base might not provide exhaustive coverage for investi-          requirements when crossing unsafe boundaries is crucial, particu-
gating the categories toward security requirements. We adopted a           larly with well-defined categorization. To this end, we conducted
validation based on the CVE classification to address this limitation.     the first comprehensive empirical study on safety requirements
Also, survey participants might not be representative enough; some         across the unsafe boundary. We focus on unsafe API documents
might be malicious respondents, cheat on the programming expe-             in the standard library to infer safety properties, then categorize
rience, or send multiple submissions. To ensure internal validity,         unsafe APIs and existing CVEs. Additionally, we conducted a user
Is unsafe an Achilles’ Heel? A Comprehensive Study of Safety Requirements in Unsafe Rust Programming                                                                      arxiv, 2023,


survey to gain insights into four aspects of these safety properties                         [22] Rust Group. 2023. The Rust Playground. https://play.rust-lang.org (Accessed on
from experienced Rust developers. Through these efforts, we aim                                   07/25/2023).
                                                                                             [23] Rust Group. 2023. The Rust Reference. https://doc.rust-lang.org/reference (Ac-
to promote the standardization of systematic documents for Unsafe                                 cessed on 07/25/2023).
Rust in the Rust community.                                                                  [24] Rust Group. 2023. The rustdoc book. https://doc.rust-lang.org/rustdoc (Accessed
                                                                                                  on 07/25/2023).
                                                                                             [25] Rust Group. 2023. The Rustonomicon. https://doc.rust-lang.org/nomicon (Ac-
                                                                                                  cessed on 07/25/2023).
REFERENCES                                                                                   [26] Rust Group. 2023. TheRustStandardLibrary. https://doc.rust-lang.org/std (Ac-
 [1] Parastoo Abtahi and Griffin Dietz. 2020. Learning Rust: How Experienced Pro-                 cessed on 07/25/2023).
     grammers Leverage Resources to Learn a New Programming Language. In Ex-                 [27] Rust Secure Code Working Group. 2023. RUSTSEC: A vulnerability database for
     tended Abstracts of the 2020 CHI Conference on Human Factors in Computing                    the Rust ecosystem. https://rustsec.org (Accessed on 07/25/2023).
     Systems. 1–8. doi:10.1145/3334480.3383069.                                              [28] Florian Hahn. 2016. Rust2Viper: Building a static verifier for Rust. Master’s thesis.
 [2] RUSTSEC-2021-0121: Non aligned u32 read in Chacha20 encryption and decryp-                   doi:10.3929/ethz-a-010669150 .
     tion. 2021. https://rustsec.org/advisories/RUSTSEC-2021-0121.html (Accessed             [29] Son Ho and Jonathan Protzenko. 2022. Aeneas: Rust verification by functional
     on 07/25/2023).                                                                              translation. Proceedings of the ACM on Programming Languages 6, ICFP (2022),
 [3] arXiv. 2023. rCanary: Detecting Memory Leaks Across Semi-automated Memory                    711–741. doi:10.1145/3547647.
     Management Boundary in Rust. In arXiv.                                                  [30] Jianfeng Jiang, Hui Xu, and Yangfan Zhou. 2021.                RULF: Rust library
 [4] Vytautas Astrauskas, Aurel Bílỳ, Jonáš Fiala, Zachary Grannan, Christoph Math-              fuzzing via API dependency graph traversal. In 2021 36th IEEE/ACM Inter-
     eja, Peter Müller, Federico Poli, and Alexander J Summers. 2022. The prusti project:         national Conference on Automated Software Engineering (ASE). IEEE, 581–592.
     Formal verification for rust. In NASA Formal Methods Symposium. Springer, 88–                doi:10.1109/ASE51524.2021.9678813.
     108. doi:10.1145/3547647.                                                               [31] Ralf Jung, Hoang-Hai Dang, Jeehoon Kang, and Derek Dreyer. 2019. Stacked
 [5] Vytautas Astrauskas, Christoph Matheja, Federico Poli, Peter Müller, and                     borrows: an aliasing model for Rust. Proceedings of the ACM on Programming
     Alexander J Summers. 2020. How do programmers use unsafe rust? Pro-                          Languages 4, POPL (2019), 1–32. doi:10.1145/3371109.
     ceedings of the ACM on Programming Languages 4, OOPSLA (2020), 1–27.                    [32] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. Rust-
     doi:10.1145/3334480.3383069.                                                                 Belt: Securing the foundations of the Rust programming language. Proceedings of
 [6] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon Lim, and Taesoo Kim. 2021.                    the ACM on Programming Languages 2, POPL (2017), 1–34. doi:10.1145/3158154.
     Rudra: finding memory safety bugs in rust at the ecosystem scale. In Proceedings        [33] Steve Klabnik and Carol Nichols. 2019. The Rust Programming Language (Covers
     of the ACM SIGOPS 28th Symposium on Operating Systems Principles. 84–99.                     Rust 2018). No Starch Press.
     doi:10.1145/3477132.3483570.                                                            [34] Nick Kolakowski. 2019. Fastest-Growing Programming Languages on GitHub.
 [7] Josh Berdine, Cristiano Calcagno, and Peter W O’hearn. 2005. Symbolic execution              https://insights.dice.com/2019/11/11/10-github-programming-languages (Ac-
     with separation logic. In Programming Languages and Systems: Third Asian Sym-                cessed on 07/25/2023).
     posium, APLAS 2005, Tsukuba, Japan, November 2-5, 2005. Proceedings 3. Springer,        [35] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe,
     52–68. doi: 10.1007/11575467_5.                                                              Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel. 2023. Verus: Verifying
 [8] MIRAI Contributors. 2023. MIRAI: Rust mid-level IR Abstract Interpreter. https:              rust programs using linear ghost types. Proceedings of the ACM on Programming
     //github.com/facebookexperimental/MIRAI (Accessed on 07/25/2023).                            Languages 7, OOPSLA1 (2023), 286–315. doi:10.1145/3586037.
 [9] Miri Contributors. 2023. Miri: An interpreter for Rust’s mid-level intermediate         [36] Amit Levy, Bradford Campbell, Branden Ghena, Daniel B Giffin, Shane Leonard,
     representation. https://github.com/rust-lang/miri (Accessed on 07/25/2023).                  Pat Pannuto, Prabal Dutta, and Philip Levis. 2017. The tock embedded operating
[10] Will Crichton, Marco Patrignani, Maneesh Agrawala, and Pat Hanrahan. 2022.                   system. In Proceedings of the 15th ACM Conference on Embedded Network Sensor
     Modular information flow through ownership. In Proceedings of the 43rd ACM                   Systems. 1–2. doi:10.1145/3131672.3136988.
     SIGPLAN International Conference on Programming Language Design and Imple-              [37] Amit Levy, Bradford Campbell, Branden Ghena, Daniel B Giffin, Pat Pannuto, Pra-
     mentation. 1–14. doi:10.1145/3519939.3523445.                                                bal Dutta, and Philip Levis. 2017. Multiprogramming a 64kb computer safely and
[11] Mohan Cui, Chengjun Chen, Hui Xu, and Yangfan Zhou. 2023. SafeDrop: De-                      efficiently. In Proceedings of the 26th Symposium on Operating Systems Principles.
     tecting memory deallocation bugs of rust programs via static data-flow analysis.             234–251. doi:10.1145/3132747.3132786.
     ACM Transactions on Software Engineering and Methodology 32, 4 (2023), 1–21.            [38] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John CS Lui. 2021. MirChecker:
     doi:10.1145/3542948.                                                                         detecting bugs in Rust programs via static analysis. In Proceedings of the 2021
[12] allowing for memory safety issues through race conditions. CVE-2017-20004: In                ACM SIGSAC Conference on Computer and Communications Security. 2183–2196.
     the standard library in Rust before 1.19.0, there is a synchronization problem in the        doi:10.1145/3460120.3484541.
     MutexGuard object. MutexGuards can be used across threads with any types. 2017.         [39] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John CS Lui. 2022. Detecting
     https://www.cve.org/CVERecord?id=CVE-2017-20004 (Accessed on 07/25/2023).                    cross-language memory management issues in rust. In European Symposium on
[13] allowing for memory safety issues through race conditions. CVE-2021-45709: In                Research in Computer Security. Springer, 680–700. doi:10.1007/978-3-031-17143-
     the standard library in Rust before 1.19.0, there is a synchronization problem in the        7_33.
     MutexGuard object. MutexGuards can be used across threads with any types. 2021.         [40] Marcus Lindner, Jorge Aparicius, and Per Lindgren. 2018. No panic! Verification of
     https://www.cve.org/CVERecord?id=CVE-2021-45709 (Accessed on 07/25/2023).                    Rust programs by symbolic execution. In 2018 IEEE 16th International Conference
[14] 7.0.1 CVE-2023-30624: Wasmtime is a standalone runtime for WebAssembly. Prior                on Industrial Informatics (INDIN). IEEE, 108–114. doi:10.1109/INDIN.2018.8471992.
     to versions 6.0.2, such as tables 8.0.1, Wasmtime’s implementation of managing          [41] Nicholas D Matsakis and Felix S Klock. 2014. The rust language. ACM SIGAda
     per-instance state, and contains LLVM-level undefined behavior. memories. 2023.              Ada Letters 34, 3 (2014), 103–104. doi:10.1145/2692956.2663188.
     https://www.cve.org/CVERecord?id=CVE-2023-30624 (Accessed on 07/25/2023).               [42] Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. 2021. RustHorn:
[15] Hoang-Hai Dang, Jacques-Henri Jourdan, Jan-Oliver Kaiser, and Derek Dreyer.                  CHC-based verification for Rust programs. ACM Transactions on Programming
     2019. RustBelt meets relaxed memory. Proceedings of the ACM on Programming                   Languages and Systems (TOPLAS) 43, 4 (2021), 1–54. doi:10.1145/3462205.
     Languages 4, POPL (2019), 1–29. doi:10.1145/3371102.                                    [43] Stack Overflow. 2016. Stack Overflow Developer Survey 2016. https://insights.
[16] Kyle Dewey, Jared Roesch, and Ben Hardekopf. 2015. Fuzzing the Rust type-                    stackoverflow.com/survey/2016#technology-most-loveddreaded-and-wanted
     checker using CLP (T). In 2015 30th IEEE/ACM International Conference on Auto-               (Accessed on 07/25/2023).
     mated Software Engineering (ASE). IEEE, 482–493. doi:10.1109/ASE.2015.65.               [44] Stack Overflow. 2017. Stack Overflow Developer Survey 2017. https://insights.
[17] Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa. 2020. Is Rust used                    stackoverflow.com/survey/2017#technology-most-loveddreaded-and-wanted
     safely by software developers?. In Proceedings of the ACM/IEEE 42nd International            (Accessed on 07/25/2023).
     Conference on Software Engineering. 246–257. doi:10.1145/3377811.3380413.               [45] Stack Overflow. 2018. Stack Overflow Developer Survey 2018. https://insights.
[18] Kelsey R Fulton, Anna Chan, Daniel Votipka, Michael Hicks, and Michelle L                    stackoverflow.com/survey/2018#technology-most-loveddreaded-and-wanted
     Mazurek. 2021. Benefits and drawbacks of adopting a secure programming                       (Accessed on 07/25/2023).
     language: Rust as a case study. In Seventeenth Symposium on Usable Privacy and          [46] Stack Overflow. 2019. Stack Overflow Developer Survey 2019. https://insights.
     Security (SOUPS 2021). USENIX Association, 597–616. https://www.usenix.org/                  stackoverflow.com/survey/2019#technology-most-loveddreaded-and-wanted
     conference/soups2021/presentation/fulton                                                     (Accessed on 07/25/2023).
[19] CVE Group. 2023. The CVE Program. https://www.cve.org (Accessed on                      [47] Stack Overflow. 2020. Stack Overflow Developer Survey 2020. https://insights.
     07/25/2023).                                                                                 stackoverflow.com/survey/2020#technology-most-loveddreaded-and-wanted
[20] Golendata Group. 2023. Golendata. https://www.jinshuju.net (Accessed on                      (Accessed on 07/25/2023).
     07/25/2023).                                                                            [48] Stack Overflow. 2021. Stack Overflow Developer Survey 2021. https://insights.
[21] Rust Group. 2023. The Rust community’s crate registry. https://crates.io (Accessed           stackoverflow.com/survey/2021#technology-most-loveddreaded-and-wanted
     on 07/25/2023).                                                                              (Accessed on 07/25/2023).
arxiv, 2023,                                                                                                                                                            Cui et al.


[49] Stack Overflow. 2022. Stack Overflow Developer Survey 2022. https://survey.          [62] std::slice::SliceIndex. 2023. https://doc.rust-lang.org/std/slice/trait.SliceIndex.
     stackoverflow.co/2022 (Accessed on 07/25/2023).                                           html (Accessed on 07/25/2023).
[50] Alex Ozdemir. 2019. Unsafe in Rust: Syntactic Patterns. (2019), (Accessed on         [63] std::u16::unchecked_mul. 2023. https://doc.rust-lang.org/std/primitive.u16.html#
     07/25/2023). https://cs.stanford.edu/~aozdemir/blog/unsafe-rust-syntax                    method.unchecked_mul (Accessed on 07/25/2023).
[51] Boqin Qin, Yilun Chen, Zeming Yu, Linhai Song, and Yiying Zhang. 2020. Un-           [64] std::u8::unchecked_mul. 2023. https://doc.rust-lang.org/std/primitive.u8.html#
     derstanding memory and thread safety practices and issues in real-world Rust              method.unchecked_mul (Accessed on 07/25/2023).
     programs. In Proceedings of the 41st ACM SIGPLAN Conference on Programming           [65] John Toman, Stuart Pernsteiner, and Emina Torlak. 2015. Crust: a bounded
     Language Design and Implementation. 763–779. doi:10.1145/3385412.3386036.                 verifier for rust (N). In 2015 30th IEEE/ACM International Conference on Automated
[52] Youren Shen, Hongliang Tian, Yu Chen, Kang Chen, Runji Wang, Yi Xu, Yubin                 Software Engineering (ASE). IEEE, 75–80. doi:10.1109/ASE.2015.77.
     Xia, and Shoumeng Yan. 2020. Occlum: Secure and efficient multitasking inside        [66] Gert-Jan Van Rootselaar and Bart Vermeulen. 1999. Silicon debug: scan chains
     a single enclave of intel sgx. In Proceedings of the Twenty-Fifth International           alone are not enough. In International Test Conference 1999. Proceedings (IEEE Cat.
     Conference on Architectural Support for Programming Languages and Operating               No. 99CH37034). IEEE, 892–902. doi:10.1109/TEST.1999.805821.
     Systems. 955–970. doi:10.1145/3373376.3378469.                                       [67] Alexa VanHattum, Daniel Schwartz-Narbonne, Nathan Chong, and Adrian Samp-
[53] std::marker::Send. 2023. https://doc.rust-lang.org/std/marker/trait.Send.html             son. 2022. Verifying dynamic trait objects in Rust. In Proceedings of the 44th
     (Accessed on 07/25/2023).                                                                 International Conference on Software Engineering: Software Engineering in Practice.
[54] std::marker::Sync. 2023. https://doc.rust-lang.org/std/marker/trait.Sync.html             321–330. doi:10.1145/3510457.3513031.
     (Accessed on 07/25/2023).                                                            [68] Fabian Wolff, Aurel Bílỳ, Christoph Matheja, Peter Müller, and Alexander J
[55] std::mem::ManuallyDrop::take. 2023. https://doc.rust-lang.org/std/mem/struct.             Summers. 2021. Modular specification and verification of closures in Rust.
     ManuallyDrop.html#method.take (Accessed on 07/25/2023).                                   Proceedings of the ACM on Programming Languages 5, OOPSLA (2021), 1–29.
[56] std::mem::zeroed. 2023. https://doc.rust-lang.org/std/mem/fn.zeroed.html (Ac-             doi:10.1145/3485522.
     cessed on 07/25/2023).                                                               [69] Hui Xu, Zhuangbin Chen, Mingshen Sun, Yangfan Zhou, and Michael R Lyu.
[57] std::ops::Add. 2023. https://doc.rust-lang.org/std/ops/trait.Add.html (Accessed           2021. Memory-safety challenge considered solved? An in-depth study with all
     on 07/25/2023).                                                                           Rust CVEs. ACM Transactions on Software Engineering and Methodology (TOSEM)
[58] std::ptr::add. 2023. https://doc.rust-lang.org/std/primitive.pointer.html#method.         31, 1 (2021), 1–25. doi:10.1145/3466642.
     add (Accessed on 07/25/2023).                                                        [70] Zeming Yu, Linhai Song, and Yiying Zhang. 2019. Fearless concurrency? un-
[59] std::ptr::read. 2023. https://doc.rust-lang.org/std/ptr/fn.read.html (Accessed on         derstanding concurrent programming safety in real-world rust software. arXiv
     07/25/2023).                                                                              preprint arXiv:1902.01906 (2019). arXiv:arXiv:1908.06849
[60] std::ptr::swap. 2023. https://doc.rust-lang.org/std/ptr/fn.swap.html (Accessed on    [71] Shuofei Zhu, Ziyi Zhang, Boqin Qin, Aiping Xiong, and Linhai Song. 2022. Learn-
     07/25/2023).                                                                              ing and programming challenges of rust: A mixed-methods study. In Proceed-
[61] std::slice::from_raw_parts_mut. 2023. https://doc.rust-lang.org/std/slice/fn.from_        ings of the 44th International Conference on Software Engineering. 1269–1281.
     raw_parts_mut.html (Accessed on 07/25/2023).                                              doi:10.1145/3510003.3510164.
