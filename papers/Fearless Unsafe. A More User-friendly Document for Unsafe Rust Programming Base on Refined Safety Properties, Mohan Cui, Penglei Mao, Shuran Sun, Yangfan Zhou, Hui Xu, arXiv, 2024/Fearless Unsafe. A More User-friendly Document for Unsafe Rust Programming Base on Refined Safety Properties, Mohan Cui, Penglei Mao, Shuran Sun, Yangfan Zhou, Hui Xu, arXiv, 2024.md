                                         Fearless Unsafe. A More User-friendly Document for Unsafe
                                         Rust Programming Base on Refined Safety Properties.
                                         MOHAN CUI, School of Computer Science, Fudan University, China
                                         PENGLEI MAO, School of Computer Science, Fudan University, China
arXiv:2412.06251v2 [cs.SE] 19 Dec 2024




                                         SHURAN SUN, School of Computer Science, Fudan University, China
                                         YANGFAN ZHOU, School of Computer Science, Fudan University, China
                                         HUI XU∗ , School of Computer Science, Fudan University, China
                                         Rust, a popular systems-level programming language, has garnered widespread attention due to its features of
                                         achieving run-time efficiency and memory safety. With an increasing number of real-world projects adopting
                                         Rust, understanding how to assist programmers in correctly writing unsafe code poses a significant challenge.
                                         Based on our observations, the current standard library has many unsafe APIs, but their descriptions are
                                         not uniform, complete, and intuitive, especially in describing safety requirements. Therefore, we advocate
                                         establishing a systematic category of safety requirements for revising those documents.
                                            In this paper, we extended and refined our study in ICSE 2024. We defined a category of Safety Properties
                                         (22 items in total) that learned from the documents of unsafe APIs in the standard library. Then, we labeled all
                                         public unsafe APIs (438 in total) and analyzed their correlations. Based on the safety properties, we reorganized
                                         all the unsafe documents in the standard library and designed a consultation plugin into rust-analyzer as a
                                         complementary tool to assist Rust developers in writing unsafe code. To validate the practical significance, we
                                         categorized the root causes of all Rust CVEs up to 2024-01-31 (419 in total) into safety properties and further
                                         counted the real-world usage of unsafe APIs in the crates.io ecosystem.
                                         CCS Concepts: • Software and its engineering → General programming languages; Development
                                         frameworks and environments.
                                         Additional Key Words and Phrases: Unsafe Rust, Safety Property, Document, Rust Analyzer
                                         ACM Reference Format:
                                         Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu. 2024. Fearless Unsafe. A More User-friendly
                                         Document for Unsafe Rust Programming Base on Refined Safety Properties.. In . ACM, New York, NY, USA,
                                         22 pages. https://doi.org/10.1145/nnnnnnn.nnnnnnn

                                         1   INTRODUCTION
                                         Rust is a popular system programming language designed for achieving memory safety and ef-
                                         ficiency [32, 40]. This is attributed to extensive static analysis during compilation [19]; various
                                         zero-cost abstractions collectively provide those guarantees [74], and the typical examples are own-
                                         ership and generics [31]. Limited by using static analysis in the compiler, programmers must invest
                                         significant effort in writing code that can satisfy the syntax requirement to pass the compilation,
                                         leading to a steep learning curve [19]. However, due to the enticing rewards [33], Rust has attracted
                                         numerous real-world projects to code translations, especially for the system programs [35, 36, 51].
                                         Since 2016, Rust has consistently been the most popular programming language in the open-source
                                         community [42–48].
                                            As more programs employ Rust, correctly writing unsafe code becomes crucial for the safety
                                         promise [5]. Safety isolation is one of the innovations introduced by Rust [50]. It segregates parts
                                         where the compiler can ensure memory safety into Safe Rust and uses unsafe keyword as a superset
                                         that is not fully constrained by the compile-time check [32, 49]. Under this isolation, the code
                                         containing unsafe operations must be encapsulated within an unsafe block; otherwise, it will fail
                                         to compile. Due to the absence of strict compiler checks within the unsafe scope, developers may
                                         ∗ Corresponding author.



                                                                                                1
arxiv, 2024,                                                     Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu


                               Listing (1) Source code of ManuallyDrop::take in Rust std.
1    // impl<T> ManuallyDrop<T>
2    pub unsafe fn take(slot: &mut ManuallyDrop<T>) -> T {
3        // SAFETY: we are reading from a reference, which is
4        // guaranteed to be valid for reads.
5        unsafe { ptr::read(&slot.value) }
6    }


                               Listing (2) Document of ManuallyDrop::take in Rust 1.75.
1    Takes the value from the ManuallyDrop<T> container out.
2    This method is primarily intended for moving out values in drop. Instead of using ManuallyDrop
          ::drop to manually drop the value, you can use this method to take the value and use it
          however desired.
3    Whenever possible, it is preferable to use into_inner instead, which prevents duplicating the
          content of the ManuallyDrop<T>.
4    Safety
5    This function semantically moves out the contained value without preventing further usage,
          leaving the state of this container unchanged. It is your responsibility to ensure that
          this ManuallyDrop is not used again.



Fig. 1. Example of an unsafe API in Rust std. Listing 1 provides the source code of an unsafe method of
struct ManuallyDrop<T>. Listing 2 extracts the document in Rust 1.75. This document introduces the usage,
functionality, and safety requirements to comply with by using a section labeled Safety.

Table 1. A list of APIs with the same side effects and their document slices in Rust 1.75. These APIs input
mutable pointers and return a typed owner. In previous research, it has been reported that misuse of these
APIs can incur double free. The Safety section is highlighted, the description of the safety requirement is
underlined, and the side effect is bolded.

      Implemented Type                       Unsafe Method                      Safety Description Slices in API Documents.
                                                                                read creates a bitwise copy of T, regardless of whether T is Copy. If T
                                                                                is not Copy, using both the returned value and the value at *src can
    impl<T: ?Sized> *mut T                  fn read(self) -> T
                                                                                violate memory safety. Note that assigning to *src counts as a use
                                                                                because it will attempt to drop the value at *src.
                                                                                Safety: This function semantically moves out the contained value with-
                                                                                out preventing further usage, leaving the state of this container un-
 impl<T> ManuallyDrop<T>         fn take(&mut ManuallyDrop<T>) -> T
                                                                                changed. It is your responsibility to ensure that this ManuallyDrop is
                                                                                not used again.
                                                                                This function is unsafe because improper use may lead to memory
    impl<T: ?Sized> Box<T>            fn from_raw(*mut T) -> Self               problems. For example, a double-free may occur if the function is
                                                                                called twice on the same raw pointer.
                                                                                The raw pointer must have been previously returned by a call to
                                                                                Rc<U>::into_raw where U must have the same size and alignment
    impl<T: ?Sized> Rc<T>             fn from_raw(*const T) -> Self
                                                                                as T. The user of from_raw has to make sure a specific value of T is
                                                                                only dropped once.
                                                                                The raw pointer must have been previously returned by a call to
                                                                                Arc<U>::into_raw where U must have the same size and alignment
    impl<T: ?Sized> Arc<T>            fn from_raw(*const T) -> Self
                                                                                as T. The user of from_raw has to make sure a specific value of T is
                                                                                only dropped once.
                                                                                Safety: This should only ever be called with a pointer that was earlier
                                                                                obtained by calling CString::into_raw. Other usage (e.g., trying to take
         impl CString               fn from_raw(*mut c_char) -> Self
                                                                                ownership of a string that was allocated by foreign code) is likely to
                                                                                lead to undefined behavior or allocator corruption.
                                                                                Safety: The ownership of ptr is effectively transferred to the Vec<T>
                                                                                which may then deallocate, reallocate or change the contents of memory
       impl<T> Vec<T>        fn from_raw_parts(*mut T, usize, usize) -> Self
                                                                                pointed to by the pointer at will. Ensure that nothing else uses the
                                                                                pointer after calling this function.
                                                                                Safety: The ownership of buf is effectively transferred to the String
                                                                                which may then deallocate, reallocate or change the contents of memory
         impl String         fn from_raw_parts(*mut u8, usize, usize) -> Self
                                                                                pointed to by the pointer at will. Ensure that nothing else uses the
                                                                                pointer after calling this function.



                                                                       2
Fearless Unsafe. A More User-friendly Document for Unsafe Rust Programming Base on Refined Safety Properties.
                                                                                                      arxiv, 2024,


perceive unsafe code as a backdoor to resolve the compiler error, which is error-prone to incurring
undefined behavior (UB).
   In this paper, we extended and refined our study in ICSE 2024. To study this topic, the standard
library, which has a diverse collection of unsafe APIs and comprehensive documents, stands out as
an ideal target [25]. Each unsafe API in std-lib has one section named Safety that outlines its safety
requirements. As shown in Figure 1, ManuallyDrop::take [58] specifies that users cannot reuse the
container after calling this function. Table 1 presents our observations that the safety requirements
are neither uniform nor complete. Recent studies revealed misusing a set of unsafe APIs that would
cause double free [6, 11, 72], as listed in Table 1. Despite having the same safety requirements and
side effects, the documents do not exhibit significant uniformity. Also, the descriptions are not
complete, only Box<T> explicitly mentioning the risk for double free.
   Another observation is the lack of intuitiveness. Utilizing the Safety section to enumerate safety
requirements aligns with intuition. The majority of APIs listed adheres to this standard, such as
String, Vec<T>, CString, and Box<T> in Table 1. However, Rc<T> and Arc<T> miss the Safety
section, and issues arising from ptr::read [62] are stated in an external section: Ownership of
the Returned Value. Simultaneously, multi-level jumps require users to click hyperlinks frequently.
As seen in Listing 3, readers of the documentation for impl *const T: read need to navigate to
ptr::read; in Listing 4, the definition of valid pointer is documented in another lengthy page,
demanding users to invest significant effort in reading them.
   We advocate for the Rust community to develop a unified, complete, intuitive, and well-categorized
document system for unsafe APIs to help users write unsafe code correctly. Specifically, this paper
aims to address the following research questions (RQs):
• RQ-1. How to summarize finer-grained safety properties (requirements) that should be satisfied
  in Unsafe Rust? (§3)
• RQ-2. If the safety properties can be used to provide user-friendly documents for Unsafe Rust
  programmers? (§4)
• RQ-3. Can those safety properties cover the root causes of the existing program vulnerabilities
  caused by Unsafe Rust? (§5)
   For each RQ, we designed different experiments centered around unsafe documents. This paper
is an extended version of our conference paper "Is unsafe an Achilles’ Heel? A Comprehensive
Study of Safety Requirements in Unsafe Rust Programming" [12]. To answer RQ1, we reviewed
all public unsafe APIs from the standard library [25]. We refined our safety properties defined
in the previous work, labeled the involved APIs, and conducted correlation analysis. To answer
RQ2, we revised the unsafe documents in the standard library, grouping the document slice, safety
property, and parameter into triplets. We integrated the revised documents into rust-analyzer as
a complementary plugin for users. To answer RQ3, we examined all Rust CVEs up to 2024-01-31
from CVEmitre [20], filtered them based on the root causes, and classified them according to the
violated safety properties. Subsequently, we analyzed the distribution of unsafe APIs within the
crates.io [21].
   We finally reviewed 438 unsafe APIs and defined 13 safety properties with 22 sub-properties,
categorizing them into preconditions or postconditions. We conducted the correlation analysis
on the labeled APIs and the result demonstrated the safety properties for dereferencing. Next, we
reorganized all the documents by analyzing the parameters corresponding to safety properties and
document slices. The revised documents have been incorporated into rust-analyzer, and it can assist
users by displaying a detailed list of the triplets while hovering over the source code. Finally, we
classified current CVEs based on safety properties, with 198 out of 419 originating from misusing
unsafe code. Notably, 86.36% of these errors were attributed to misuse of std APIs. Therefore, we

                                                        3
arxiv, 2024,                                     Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu


                            Listing (3) Document of *const T::read in Rust 1.75.
 1    Primitive Type pointer
 2    pub const unsafe fn read(self) -> T
 3
 4    Reads the value from self without moving it. This leaves the memory in self unchanged.
 5    See ptr::read for safety concerns and examples.


                               Listing (4) Document of ptr::read in Rust 1.75.
 1    std::ptr::read
 2    pub const unsafe fn read<T>(src: *const T) -> T
 3
 4    Reads the value from src without moving it. This leaves the memory in src unchanged.
 5
 6    Safety
 7    Behavior is undefined if any of the following conditions are violated:
 8        src must be valid for reads.
 9        src must be properly aligned. Use read_unaligned if this is not the case.
10        src must point to a properly initialized value of type T.
11    Note that even if T has size 0, the pointer must be non-null and properly aligned.



Fig. 2. Two instances of non-intuitiveness in the std unsafe documents. These two functions are named read,
with identical functionality and signature. The document in List 3 requires a jump to List 4. However, List 4
contains a hyperlink leading to a secondary jump toward the informal definition of valid pointer.


conducted a statistical analysis of std unsafe API usage within the Rust ecosystem, comprising
103,516 libraries on crates.io.
  Our main contributions are listed as follows:
• We conducted the empirical study by analyzed unsafe API documents from the standard library
  to establish a systematic categorization of safety requirements for Unsafe Rust.
• We summarized 13 safety properties with 22 sub-properties and labeled all unsafe APIs through
  this criteria, and the labeled data were evaluated via correlation analysis.
• We reorganized all documents of the unsafe functions in the standard library and integrated
  them into the rust-analyzer, making it open source.
• We categorized all Rust CVEs based on safety properties, forming a collection that can serve as a
  benchmark, and we collected API usage statistics within crates.io to understand the frequency.

2     BACKGROUND
2.1    Safety Isolation in Rust
Unsafe Rust is a superset of Safe Rust [50]. Safe Rust employed static analysis to guarantee memory
safety. Thus, undefined behavior cannot be triggered solely using Safe Rust [5]. Consequently,
it cannot be a system programming language due to the lack of low-level controls (e.g., manual
memory management). Unsafe Rust is an essential design to compensate for this weakness [24]. It is
used if users need to interact with OS, hardware, or other programming languages to achieve better
performance. A recent empirical study investigated the learning challenges of safety mechanisms
via Stack Overflow and user surveys [74]. It was reported that Rust’s safety mechanisms could be
more learner-friendly but are restricted to Safe Rust. Instead, learning and utilizing Unsafe Rust
may be a prerequisite for advanced Rust developers, especially for system programming.

                                                     4
Fearless Unsafe. A More User-friendly Document for Unsafe Rust Programming Base on Refined Safety Properties.
                                                                                                      arxiv, 2024,


2.1.1 unsafe Keyword. unsafe keyword is allowed to be used as a prefix for different contexts.
The first scenario marks definitions with extra safety conditions (e.g., unsafe fn, unsafe trait). It
indicates safety requirements the callers or implementations must uphold, which the compiler
does not check. The second scenario marks code that needs to satisfy extra safety conditions (e.g.,
unsafe { }, unsafe impl.). It signifies the requirements that the programmers should be seriously
examined to satisfy the safety conditions inside the block. unsafe keyword states that all unsafe
operations must be encapsulated within unsafe scope. Notably, the trust between safe and unsafe
parts is asymmetric [24]. Manual inspection is required to ensure the safe portion’s data adheres to
the unsafe operations’ contracts. Conversely, the safe code should keep the unconditional belief
that the unsafe part is always correct.

2.1.2 unsafe Operations. Safety isolation is designed for different aims. Safe Rust is a safe pro-
gramming language for tasks that do not require low-level interactions. Contrariwise, Unsafe Rust
fully leverages the capabilities of a system programming language. Unlike C/C++, Unsafe Rust
still requires adherence to certain contracts from the safe portion, such as ownership. The main
differences are five unsafe operations are allowed to be used only in unsafe blocks: (1) Dereference
raw pointers; (2) Call unsafe functions; (3) Implement unsafe traits; (4) Mutate static variables;
and (5) Access fields of unions [24]. These operations provide flexibility but come with the risk of
incurring undefined behavior and the responsibility of the users to review the correctness.

2.2    Undefined Behavior in Rust
The undefined behavior in Rust is listed below. It is limited because this categorization targets the
side effects of unsafe operations. Since no formal model of Rust’s semantics defines precisely what
is and is not permitted in unsafe code [22], additional behavior may be deemed vulnerable. In this
paper, we add the underlined issues as program vulnerabilities if they are triggered by unsafe code:
• Dereference (using the * operator on) dangling or unaligned raw pointers.
• Break the pointer aliasing rules. References and boxes must not be dangling while they are alive.
• Call a function with the wrong call ABI or unwinding from a function with the wrong unwind
  ABI.
• Execute code compiled with platform features that the current thread of execution does not
  support.
• Produce invalid values, as explained in Table 2, even in private fields and locals.
• Mutate immutable data. All data inside a const item, reached through a shared reference or owned
  by an immutable binding, is immutable.
• Cause data races.
• Invoke undefined behavior via compiler intrinsics.
• Use inline assembly incorrect.
• Cause a memory leak and exiting without calling destructors.
• Trigger an unreachable path then aborting (or panicking).
• Arithmetic overflow.
   These undefined behaviors serve as the basis for classifying safety requirements. Other errors
fall outside the scope (e.g., deadlocks and logic errors).

3     REVIEWING RUST DOCUMENTS
To answer RQ1, this section defines a systematic procedure of extracting the categorization of
safety requirements named Safety Properties, which is learned from the documentation of unsafe
API in the standard library [25].

                                                        5
arxiv, 2024,                                      Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu


               Table 2. Invalid value for Rust types, alone or as a field of a compound type.

      Rust Type      Invalid Value
          !          Invalid for all values.
        bool         Not 0 or 1 in bytes.
        char         Outside [0x0, 0xD7FF] & [0xE000, 0x10FFFF].
         str         Has uninitialized memory.
  numeric i*/u*/f*   Reads from uninitialized memory.
        enum         Has an invalid discriminant.
     reference       Dangling, unaligned, or pointing to an invalid value.
    raw pointer      Reads from uninitialized memory.
         Box         Dangling, unaligned, or pointing to an invalid value.
     fn pointer      NULL.
                     Has invalid metadata. dyn Trait is invalid if it is not a pointer to a vtable for Trait that
    wide reference   matches the actual dynamic trait the pointer or reference points to, and slice is invalid if
                     the length is not a valid usize.
      custom type    Has one of those custom invalid values.


3.1    Where to Obtain Safety Requirements?
Rustdoc [23] is the official document system embedded in Rust programs. Programmers can use it
to document the functionalities, calling requirements, side effects, and sample snippets in different
scales. As for unsafe APIs, the safety requirements of arguments and return values must be explicitly
specified in the document. Considering the quality of the documents in the ecosystem, we utilized
the unsafe APIs within the standard library as our learning sample.
3.1.1 Design Goals. Table 1 reveals the lack of uniformity, completeness, and intuitiveness even
in the standard library. Thus, we set the following goals to establish a systematic categorization
of finer-grained safety requirements for Rust documents. The safety properties aim to provide a
comprehensive and practical understanding of the safety considerations associated with Unsafe
Rust.
   GOAL 3.1. Generality: SP is not specific to one particular API’s intricacies.
   GOAL 3.2. Unambiguous: SP adopts Rust’s existing terminology and explanations.
   GOAL 3.3. Nonoverlapping: SP does not overlap, although they may be correlated.
   GOAL 3.4. Composability: An Unsafe API’s safety requirements can comprise several SPs.
   GOAL 3.5. Essentiality: Failure to comply with any SP would cause undefined behavior.
   GOAL 3.6. Practicality: SP must be seriously considered in real-world programming scenarios.
   GOAL 3.7. Unilingual: SP disregards FFI and the requirements of other programming languages.
3.1.2 Pre-filtering. The Rust standard library is a wide concept; it has several namespaces, including
core, std, and alloc. The functions have redundancy in those namespaces, e.g., std and core are
overlapping. Thus, we performed a pre-filtering for all unsafe APIs within std/core/alloc in Rust
1.75, considering both stable and nightly channels:
   FILTER 3.1. For the methods exposed by both core, std and alloc, we kept only one of them.
   FILTER 3.2. For methods belonging to similar numeric types, we kept only one implementation.
   FILTER 3.3. For compiler intrinsics, we retained only those with no stable counterpart.

                                                       6
Fearless Unsafe. A More User-friendly Document for Unsafe Rust Programming Base on Refined Safety Properties.
                                                                                                      arxiv, 2024,


   We finally obtained an unsafe API collection comprising 438 unsafe functions, with 127 being
folded as 11 unique APIs by Filter 3.2 (e.g., unchecked_mul::<u8>/<u16> [66, 67] are merged). We
streamlined an unsafe API queue for further analysis by applying the pre-filtering step.

3.2   How to Extract Safety Properties?
We performed a code review for all APIs in this collection to summarize what safety properties
correspond with our design goals. Five rounds of code review finally constructed a set of safety
properties with two categories and 22 items; the whole collection is shown in Table 3. For each
API, we audited five sections: functional descriptions, safety requirements, subchapters, example
snippets, and source code with comments.
3.2.1 First Round. R1: SP Construction. We constructed a safety property category for API labeling
in the first round. All the authors participated in the construction procedure. We adopted a sequential
process by using a queue of API that requires auditing. For 30 APIs as a batch, the first author
extracts potentially unrevealed safety properties, and the other authors verify them, which forms
an assembly line. The first author cannot start a new batch unless the verification is completed.
SP Creation. The category started as an empty set. The first author creates safety properties that
others can modify. A new item will be defined whenever a safety description cannot be categorized
under the existing scheme. Whenever the author suggests creating a new item, the decision is
reached through a joint review. The names of safety properties are summarized from the document
slices; only DualOwned is the novel concept introduced in this paper.
SP Modification. The author can submit a pull request to modify any safety properties (including
the definition refinement, merging, splitting, or deleting items), and the approval is contingent
on the joint review. For example, OverflowCheck and IndexCheck have been merged into Bounded.
Another example is splitting DualOwned from Aliased because they focused on objects and pointers,
respectively.
3.2.2 Second & Third Round. After categorizing safety properties, the second and third rounds are
dedicated to labeling the corresponding safety properties for each unsafe API. Since our labeling
method employs a referenced table, which includes the definition and the document examples as
the ground truth, conflicts during the labeling process are few.
R2: API Labeling. The second round created the initial labels for unsafe APIs. The first and second
authors audited concurrently for all unsafe APIs in this round. Both authors conducted parallel
reviews until all APIs were completed, then resolved conflicts in safety property labels.
R3: Labeling Review. The process and conflict resolution in the third round of the audit are com-
pletely the same as in the second round. It serves solely for the secondary confirmation, correction,
and supplementation of safety property labels.
3.2.3 Fourth & Fifth Round. 19 safety properties have been defined until R3 is completed. Our
previous work conducted a user survey to determine safety properties regarding precision, sig-
nificance, usability, and frequency [12]. As for precision, we found that safety properties defined
with longer narratives generally had lower scores, especially for Consistent Layout and Aliasing &
Mutating. In this paper, we revised the safety properties, refining their contents.
R4: SP Revision. The SP revision involved changes to the whole categorization and labels, following
the guidelines in R1-R3. This resulted in 13 safety properties comprising 22 sub-classes, with more
detailed reasons for the change described in Section 4.2.
R5: Document Revision. We revised the documents based on safety properties after getting the final
categorization. The revised document connected the document slices with safety properties and
corresponding arguments in the signature, forming a more formal version.

                                                        7
arxiv, 2024,                                             Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu


Conflict Resolution. In cases of conflicts in SP creation (R1), SP modification (R1, R4), and SP labeling
(R2, R3, R4), a joint review is initiated. It involves all the authors voting together; the action is
implemented only if all the authors vote in agreement for SP creation or SP modification and more
than three authors vote in agreement for SP labeling. Otherwise, the original decision is retained.

4     CLASSIFYING SAFETY REQUIREMENTS
To answer RQ2, this section gives the classification of safety properties. We also elaborate on
the refinement of the classification defined in our previous paper [12]. Then we present how we
reorganize the unsafe documents, building upon the safety properties. Finally, we introduce our
plugin’s framework that can help write unsafe code.

4.1    What Safety Properties Should We Satisfy?
We divided the safety properties into two categories based on the state of the function execution as
in formal methods [7], with no overlap between the sub-properties.
4.1.1 Pre-condition Safety Property (PRE-SP). The PRE-SP defines an assumption that if the input
values do not satisfy any safety requirement, the function call will trigger undefined behavior in
the current program point. Thus, any unsafe API can be considered a black box in the single-step
execution at the call site, ignoring its implementation [69]. PRE-SP aligns with the characteristic of
unsafe function, i.e., it cannot ensure safety for arbitrary inputs. In Table 3, we define 7 PRE-SPs
with 14 sub-properties in total. For example, ptr::swap [63] has a description in the document
slices - "Both x and y must be properly aligned." , thus categorized into Layout (Aligned).
4.1.2 Post-condition Safety Property (POS-SP). The previous assumption leads to the deduction
that the function can be safely called if the proper inputs are supplied. However, this assurance
only concerns the safety of the calling site. POS-SP focuses on the safety issues that may arise
from the subsequent operations, assuming that the input values satisfy all PRE-SPs. Table 3 gives 6
POS-SPs with 8 sub-properties. For example, mem::zeroed [59] has a description in the document
slices - "There is no guarantee that an all-zero byte-pattern represents a valid value of some type T." ,
thus categorized into Untyped.
4.1.3 Isolation. Our assumption established an isolation to improve the soundness of safety prop-
erties. It separates the side effects triggered in current call sites or subsequent program points and
dissolves the ambiguity - the invalid input will generate the invalid output. Hence, the POS-SP can
be the superset of PRE-SP. Benefiting from this isolation, PRE-SPs and POS-SPs are not overlapping.
It can be verified by a Rust design, where creating raw pointers is always safe, but dereferencing
them is unsafe [22]. Similarly, we assume that PRE-SPs only affect the safety of function calls, while
POS-SPs focus on the subsequent usage of inputs and return values. Furthermore, POS-SPs are only
considered under the premise that all PRE-SPs are satisfied.
4.1.4 Corner Cases. The standard library lists unsafe APIs that cannot be categorized into our
current safety properties. We open-sourced the API labels that can be used for indexing 1 and
additional clarifications listed below, which fall into the following categories:
• FFI functions with no safety requirements (2), e.g., VaListImpl<’f>::arg [52].
• Compilation procedure: codegen, intrinsic, and LLVM tag (6), e.g., breakpoint [53].
• Numerical conversions without an accurate, identifiable boundary (4), e.g., nearbyintf32 [54].
• Lacking any explanation of why they are considered unsafe (1), e.g., pref_align_of [55].

1 https:https://github.com/Artisan-Lab/rustsp_analyzer



                                                             8
Fearless Unsafe. A More User-friendly Document for Unsafe Rust Programming Base on Refined Safety Properties.
                                                                                                      arxiv, 2024,


Table 3. Safety properties learned from unsafe API documents in Rust standard library. Pre-condition and
post-condition are two primary categories, and they have 13 items in total. We present the sum of the labeled
unsafe API for each safety property and provide a detailed definition. Each safety requirement was also given
a typical unsafe API as an example. Note that each SP may contain various sub-classes. The symbols ▲ and ▼
represent the satisfaction of hierarchy between the superclass and subclass.

 Safety Property          #     Definition and the safety requirement of each Safety Property.                                                    Unsafe API Example
                                                                           Precondition Safety Property
                                Non-Null ▲: A null pointer is never valid, not even for accesses of size zero. impl<T: Sized> NonNull<T>::new_unchecked
                                Non-Dangling ▼: The value must not be pointing to the deallocated memory
   Allocated ▲          172
                                even for operations of size zero, including data stored in the stack frame and     trait SliceIndex<T: ?Sized>::get_unchecked
                                heap chunk.
                                Numerical: The relationship expressions based on numerical operations ex-
                                hibit clear numerical boundaries. The terms of the expressions can be constants,
                                                                                                                       impl<T: ?Sized> *mut T::offset_from
                                variables, or the return values of function calls. There are six relational opera-
   Bounded ▼            141
                                tors including EQ, NE, LT, GT, LE, and GE.
                                Dereferencable: The memory range of the given size starting at the pointer
                                                                                                                       impl<T: ?Sized> *mut T::copy_from
                                must all be within the bounds of a single allocated object.
                                Initialized ▲: The value that has been initialized can be divided into two
                                                                                                                     impl<T> MaybeUninit<T>::assume_init
                                scenarios: fully initialized and partially initialized.
                                Typed ▼: The bit pattern of the initialized value must be valid at the given
                                                                                                                            impl<T: ?Sized> *mut T::read
  Initialized ▼         104     type and uphold additional invariants for generics.
                                Encoded ▼: The encoding format of the string includes UTF-8 string, ASCII
                                string (in bytes), and C-compatible string (nul-terminated trailing with no nul         impl String::from_utf8_unchecked
                                bytes in the middle).
                                Sized ▲: The restrictions on Exotically Sized Types (EST), including Dynami-
                                cally Sized Types (DST) that lack a statically known size, such as trait objects               core::mem::size_of_raw
                                and slices; and Zero Sized Types (ZST) that occupy no space.
      Layout ▼          109     Aligned ▲: The value is properly aligned via a specific allocator or the attribute
                                                                                                                           impl<T: ?Sized> *mut T::swap
                                #[repr], including the alignment and the padding.
                                Fitted ▼: The layout (including size and alignment) must be the same layout
                                                                                                                              trait GlobalAlloc::dealloc
                                that was used to allocate that block of memory.
                                The variable is related to the system IO and depends on the target platform,
      SystemIO           26                                                                                               trait FromRawFd::from_raw_fd
                                including TCP sockets, handles, and file descriptors.
                                Send: The type can be transferred across threads.                                                core::marker::Send
       Thread             2
                                Sync: The type can be safe to share references between threads.                                  core::marker::Sync
                                The specific value will trigger unreachable data flow, such as enumeration
  Unreachable             5                                                                                         impl<T> Option<T>::unwrap_unchecked
                                index (variance), boolean value, etc.
                                                                          Postcondition Safety Property
                                Aliased ▲: The value may have multiple mutable references or simultaneously
                                                                                                                                           impl<T: ?Sized> *mut T::as_mut
                                have mutable and shared references.
                                Mutated ▼: The value, which is owned by an immutable binding or pointed
      Aliased            32                                                                                                                impl<T: ?Sized> *const T::as_ref
                                by shared reference, may be mutated.
                                Outlived ▼: The arbitrary lifetime (unbounded) that becomes as big as context
                                                                                                                                                   impl CStr::from_ptr
                                demands may outlive the pointed memory.
                                It may create multiple overlapped owners in the ownership system that share
  DualOwned              46                                                                                                              impl<T: ?Sized> Box<T>::from_raw
                                the same memory via retaking the owner or creating a bitwise copy.
                                The value may not be in the initialized state, or the byte pattern represents an
      Untyped            37                                                                                                                         core::mem::zeroed
                                invalid value of its type.
        Freed            19     The value may be manually freed or automated dropped.                                                impl<T: ?Sized> ManuallyDrop<T>::drop
       Leaked            35     The value may be leaked or escaped from the ownership system.                                             impl<T: ?Sized> *mut T::write
       Pinned             5     The value may be moved, although it ought to be pinned.                                               impl<P: Deref> Pin<P>::new_unchecked
 1 Send [56] and Sync [57] are unsafe traits (markers) that are automatically implemented by the compiler when it determines that they are required. Therefore, they lack associated methods.
 2 The difference between DualOwned and Aliased is that DualOwned only focuses on objects instead of pointers and references.




   No API has all safety property labels in the standard library. While it is theoretically feasible to
be labeled with all safety properties, the probability is exceedingly low since many safety properties
are connected with particular types. For example, Bounded is associated with the numerical type.
It is incredibly challenging to introduce those complex inputs. However, users can construct an
excessively intricate function by hand that requires all safety requirements.

4.2      Changes in Safety Properties Revision
We conducted a supplementary revision of the safety properties, namely the fourth-round audit,
representing a major improvement. It serves as the foundation for reorganizing the documents.

                                                                                              9
arxiv, 2024,                                           Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu


Table 4. The former version of safety properties that have significant change introduced in the fourth round.
The new safety properties have decreased from 19 to 13 major categories, with the addition of secondary
subclasses. The safety properties in the gray-shaded text have been restructured in this paper.

      Safety Property      Definition and the safety requirement of each Safety Property.
                           Relational operations allow for compile-time determination of the constant numerical boundaries
   Const Numeric Bound
                           on one side of an expression, including overflow check, index check, etc.
                           Relational operations involve expressions where neither side is a constant numeric, including
 Relative Numeric Bound
                           address boundary check, overlap check, size check, variable comparison, etc.
                           The memory range of the given size starting at the pointer must all be within the bounds of a single
       Dereferencable
                           allocated object.
                           Value stored in the allocated memory, including data in the valid stack frame and allocated heap
          Allocated
                           chunk, which cannot be NULL or dangling.
                           Value that has been initialized can be divided into two scenarios: fully initialized and partially
         Initialized
                           initialized. The initialized value must be valid at the given type (a.k.a. typed).
                           Encoding format of the string, includes valid UTF-8 string, valid ASCII string (in bytes), and valid
          Encoding
                           C-compatible string (nul-terminated trailing with no nul bytes in the middle).
                           Restriction on Type Layout, including 1) The pointer’s type must be compatible with the pointee’s
                           type; 2) The contained value must be compatible with the generic parameter for the smart pointer;
     Consistent Layout
                           and 3) Two types are safely transmutable: The bits of one type can be reinterpreted as another type
                           (bitwise move safely of one type into another).
                           Value is properly aligned via a specific allocator or the attribute #[repr], including the alignment
           Aligned
                           and the padding of one Rust type.
                           Restrictions on Exotically Sized Types (EST), including Dynamically Sized Types (DST) that lack a
   Exotically Sized Type
                           statically known size, such as trait objects and slices; Zero Sized Types (ZST) that occupy no space.
                           Aliasing and mutating rules may be violated, including 1) The presence of multiple mutable refer-
    Aliasing & Mutating    ences; 2) The simultaneous presence of mutable and shared references, and the memory the pointer
                           points to cannot get mutated (frozen); 3) Mutating immutable data owned by an immutable binding.
                           Arbitrary lifetime (unbounded) that becomes as big as context demands or spawned thread, may
          Outliving
                           outlive the pointed memory.




The motivation stems from feedback obtained through user surveys, highlighting that lengthy
definitions are detrimental to understanding the safety requirements. The previous version needed
to be more competent to introduce subclasses, making it precise for document restructuring. A
comparison between the revised version and the earlier version is presented in Table 4, and this
section will elucidate the reasons for the adjustment.

4.2.1 New: Bounded. Bounded has two subclasses. The separation between Numerical and Deref-
erencable achieves better independence for numerical calculations and memory access. Numerical
arises from Const Numeric Bound and Relative Numeric Bound. In user surveys, participants pointed
out that this separation lacked significant differences because rearranging inequalities can result in
constant and non-constant boundaries. The merged definition focuses on relational expressions
with numerical boundaries, as most numerical conditions can be checked using assert!(). It also
expands the scope of terms, supporting constants, variables, and function calls in expressions.
Dereferencable is the second subclass. In the previous version, the scope among index check, address
boundary check, and overlap check were easily misunderstanding. They all regulate the valid offset
for the memory access but can be covered by Dereferencable.

4.2.2 New: Allocated. The official document gives the description of valid pointers (not strictly
defined), which is the basis of Allocated in both versions. The changes made to Allocated are minor,
primarily because Non-Null and Non-Dangling have a hierarchical relationship, where satisfying
Non-Null is a prerequisite for satisfying Non-Dangling. Many APIs accept pointers to be NULL or
dangling because it will be overwritten. For others, if they accept a non-null pointer, users must

                                                            10
Fearless Unsafe. A More User-friendly Document for Unsafe Rust Programming Base on Refined Safety Properties.
                                                                                                      arxiv, 2024,


ensure that it cannot be dangling, as the pointer may be used to access memory, which would result
in a memory safety issue.
4.2.3 New: Initialized. Initialized restructures from Initialized, Consistent Layout, and Encoding. It
results in three new subclasses: Initialized, Typed, and Encoded. They form a hierarchical relationship,
namely ensuring Typed must guarantee Initialized, and ensuring Encoded must guarantee Typed.
Since the initialization status is a fundamental prerequisite, the initialized value may not meet all
safety requirements for a specific type. It assesses whether the initialized bits can be translated
into a valid value for the given type. Consistent Layout highlights the type of the pointed-to region,
the generic parameters of containers, and the safe conversion of types—all of which are essentially
Typed problems. Encoded introduces a third level for string format, building on the prerequisites set
by Typed. We give a prominent example of converting Vec<u8> to String. It encompasses multiple
Initialized requirements, including initialized state, typed state, and string format.
4.2.4 New: Layout. Layout, being a consolidation of Aligned, and Exotically Sized Types (EST),
is unrelated to Consistent Layout. Consistent Layout emphasizes type, representing requirements
for initialized status and the ability to safely cast. Layout restricts adaptability to memory blocks,
specifying size and alignment for underlying data. Note that it is independent of types; it solely
considers allocated blocks’ size and alignment without considering whether the internal bits should
meet any type-specific requirements. This difference is also emphasized in contrast to Initialized.
Among the subclasses, Fitted needs to satisfy both size and alignment requirements, and Sized
focuses on restrictions for the ESTs.
4.2.5 New: Aliased. The changes to Aliased resulted from merging Aliasing & Mutating and
Outliving. In the previous version of API labels, we observed a high correlation between these
safety properties, often appearing together in labels. Similar to Consistent Layout, feedback from
survey participants on Aliasing & Mutating emphasized the description being overly lengthy,
prompting us to break it down. In the ownership model, Aliased, Mutated, and Outlived form a triple
restriction for memory-safe access. Aliased pertains to restrictions on the exclusiveness of access
permissions, Mutated involves limitations on access operations, and Outlived imposes constraints
on the legitimate program points for access actions. The subdivided classes align more closely with
the safety constraints of the ownership system.

4.3   Correlation Analysis on Labeled API
Although one of our design goals focuses on non-overlapping, it is necessary to investigate potential
correlations inside those safety properties. This notion is from the intuition that data satisfying
Dereferenceable in Bounded should always meet Allocated.
4.3.1 Methodology. We created two databases based on the labeled APIs in the different scales and
then conducted a correlation analysis. The analysis results demonstrate the anticipated differences.
Large Dataset. The large dataset adopts the original collection, including the entire set of unsafe APIs
with labels. The intent of keeping a large dataset is to emphasize the quantity because functionally
related APIs may have similar labels, and adequate data can expose potential correlations.
   FILTER 4.1. APIs must have the same labels and satisfy at least one of the following requirements:
• Implementations of the same method with different mutability.
• Implementations of the same trait for different types, including mono-morphizations in the trait or
  struct definitions.
• Functions with the same name implemented for different types within the same namespace.
• Encapsulation of intrinsic functions.

                                                        11
arxiv, 2024,                                                                                                                                             Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu




                                                                                                                                                         1.0                                                                                                                                                              1.0
     Bounded   1.00      0.59                      0.26                                                                                0.25                           Bounded   1.00      0.44                      0.22                                                                                0.28

               0.59      1.00                      0.46                                        0.32                                    0.30                                     0.44      1.00                      0.50                                        0.41                                    0.31
   Allocated
                                                                                                                                                         0.9        Allocated
                                                                                                                                                                                                                                                                                                                          0.9
 Initialized                         1.00                                                      0.26                                                             Initialized                           1.00                                                      0.28

      Layout   0.26      0.46                      1.00                                        0.34        0.33      0.46              0.38              0.8           Layout   0.22      0.50                      1.00                                        0.34        0.21      0.45              0.32              0.8

 Unreachable                                                1.00                                                                                                Unreachable                                                  1.00
                                                                                                                                                         0.7                                                                                                                                                              0.7
   System IO                                                              1.00                                                                                      System IO                                                              1.00

      Thread                                                                          1.00                                                               0.6           Thread                                                                          1.00                                                               0.6
   DualOwned             0.32        0.26          0.34                                        1.00                  0.32              0.31                         DualOwned             0.41        0.28          0.34                                        1.00                  0.23              0.25
                                                                                                                                                         0.5                                                                                                                                                              0.5
     Aliased                                       0.33                                                    1.00                                                       Aliased                                       0.21                                                    1.00

     Untyped                                       0.46                                        0.32                  1.00      0.24    0.53                           Untyped                                       0.45                                        0.23                  1.00      0.24    0.46
                                                                                                                                                         0.4                                                                                                                                                              0.4
       Freed                                                                                                         0.24      1.00                                     Freed                                                                                                         0.24      1.00

      Leaked   0.25      0.30                      0.38                                        0.31                  0.53              1.00              0.3           Leaked   0.28      0.31                      0.32                                        0.25                  0.46              1.00              0.3
      Pinned                                                                                                                                    1.00                   Pinned                                                                                                                                    1.00
                                                                                                                                                         0.2                                                                                                                                                              0.2
               Bounded

                         Allocated

                                     Initialized

                                                   Layout

                                                            Unreachable

                                                                          System IO

                                                                                      Thread

                                                                                               DualOwned

                                                                                                           Aliased

                                                                                                                     Untyped

                                                                                                                               Freed

                                                                                                                                       Leaked

                                                                                                                                                Pinned




                                                                                                                                                                                Bounded

                                                                                                                                                                                          Allocated

                                                                                                                                                                                                      Initialized

                                                                                                                                                                                                                    Layout

                                                                                                                                                                                                                             Unreachable

                                                                                                                                                                                                                                           System IO

                                                                                                                                                                                                                                                       Thread

                                                                                                                                                                                                                                                                DualOwned

                                                                                                                                                                                                                                                                            Aliased

                                                                                                                                                                                                                                                                                      Untyped

                                                                                                                                                                                                                                                                                                Freed

                                                                                                                                                                                                                                                                                                        Leaked

                                                                                                                                                                                                                                                                                                                 Pinned
  (a) Analysis results on the large dataset (original).                                                                                                             (b) Analysis results on the small dataset (filtered).

Fig. 3. Correlation matrices for both the large and small datasets. Each figure only includes the sections with
weak correlation and above (correlation greater than 0.20).


Small Dataset. The small dataset is created by applying Filter 4.1 to the large dataset. This is done
to counteract the potential bias from excessive similar APIs. The small dataset intends to eliminate
the redundancy of irrelevant data and concentrate on diversity.
4.3.2 Correlation Matrix. In Figure 3, we built correlation matrices for two datasets, retaining the
elements with moderate correlation and above (correlation coefficient > 0.20). The large dataset has a
higher susceptibility to interference from redundant APIs. For example, there are 30 implementations
of the trait SliceIndex<[T]> [65], all of which are labeled with Bounded and Allocated only. The
correlation between them is higher in the large dataset, changing from 0.44 to 0.59. In the small
dataset, the diverse functionality is more likely to result in the loss of pertinent data that could
affect correlations. For example, the small dataset’s correlation between Allocated and DualOwned
changed from 0.32 to 0.41. At last, Unreachable, System IO, Thread and Pinned achieve the best
independence, as they have no substantial correlation with any other safety properties in both
matrices.
   New Findings in Correlation Matrix. Based on two diagrams in Figure 3, we extracted all the
pairs with at least a moderate CC, as listed in Table 5. Here, we will provide a more comprehensive
explanation of the improved correlations. It is evident that the new safety property classification
exhibits better independence. Notably, the pairs have significantly decreased, going from 11 to
4 pairs. The main reason is the reduction in major categories from 19 to 13 and the addition of
secondary subclasses.
   The case studies learned in the previous work are interpretable [12], which summarized six
requirements for dereferencing: Allocated, Relative Numeric Bound, Dereferencable, Consistent
Layout, Aligned, and Initialized. It can be inferred that the correlation between Allocated and
Bounded is due to the merging Relative Numeric Bound and Dereferencable into Bounded. Because
we remove memory range issues from Relative Numeric Bound, Allocated is highly correlated with
the subclass Dereferencable in Bounded. The correlation between Allocated and Layout is the result

                                                                                                                                                               12
Fearless Unsafe. A More User-friendly Document for Unsafe Rust Programming Base on Refined Safety Properties.
                                                                                                      arxiv, 2024,


Table 5. SP pairs with correlation coefficients (CC) greater than 0.4 in the large and small dataset correlation
matrices.

                              SP1        SP2     AVG-CC         SP1        SP2     AVG-CC
                           Allocated   Bounded     0.51      Allocated    Layout     0.48
                            Layout     Untyped     0.45       Leaked     Untyped     0.49


of merging Aligned into Layout. Therefore, transitioning to the new safety properties, the safety
requirements of dereferencing can be updated to include: Allocated, Bounded, Layout, and Initialized.
4.3.3 Hierarchical Relation. Hierarchical relationships were observed for both primary and sec-
ondary classes, as annotated by the dependency conditions in Table 3. It stems from expert experi-
ence and analysis results of the correlation matrix. At the primary level, Allocated is a first-class
member, which is necessary for three safety properties. Similarly, there exist hierarchical relation-
ships among sub-classes. For a pointer to be Non-Dangling, it must first satisfy the condition of
being Non-Null. Notably, the hierarchical relationships among subclasses do not propagate to the
parent classes, whereas the parent classes can propagate to subclasses.

4.4 Revising Safety Property Documents
After obtaining the refined safety property definitions and corresponding API labels, this section
aims to reorganize the Unsafe Rust documents based on the existing safety properties, providing
a developer-friendly form. An API was only marked as requiring or not requiring fulfillment of
specific safety properties in the previous work, disregarding further details [12]. In this paper, we
aim to break through this barrier. The process has the following goals:
  GOAL 4.1. Independence: Each unsafe API has a unique identifier maintained by one Safety
Property document.
  GOAL 4.2. Intuitiveness: Safety Property documents cannot contain hyperlinks referencing other
documents’ safety requirements.
   GOAL 4.3. Comprehensiveness: Safety requirements may be distributed across different locations;
efforts should be made to cover the entire native document and delete the irrelevant content.
  GOAL 4.4. Completeness: Incomplete safety descriptions within the native document should be
supplemented as much as possible.
  GOAL 4.5. Structurality: Safety requirements are enumerated in a structured manner and pre-
sented to users in a clear and logically organized format.
   We established a revision process driven by the above goals. We extract each API’s signature,
safety property labels, and native documents. Native documents encompass functional descriptions,
safety descriptions, and all subchapters. The revised document uses the online Rustdoc link as the
unique identifier, allowing each API to redirect to a distinct webpage. Given challenges such as
identical function names, methods in traits, and implementations for different mono-morphizations,
our identifiers provide better recognizability.
   For the native documents, we split the text into sentences and determine whether each sentence
can be included in the safety properties. If it can be included, we identify the related parameter
(return value), forming a triplet (i.e., parameter 𝑃, safety property 𝑆, document slice 𝐷). To achieve
Goal 4.2 to 4.4, we flatten the linked documents and manually supplement missing descriptions,
drawing from other slices in the standard library. Figure 4 illustrates the revision for ptr::read [62].
The safety property document, compared to the native document, exhibits a more structured format.

                                                        13
arxiv, 2024,                                     Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu


                           Listing (5) Native document of ptr::read in Rust 1.75.
 1    # Functionality Description
 2    Reads the value from src without moving it. This leaves the memory in src unchanged.
 3
 4    # Safety Description
 5    Behavior is undefined if any of the following conditions are violated:
 6    src must be valid for reads.
 7    src must be properly aligned. Use read_unaligned if this is not the case.
 8    src must point to a properly initialized value of type T.
 9    Note that even if T has size 0, the pointer must be non-null and properly aligned.
10
11    # Subchapter: Ownership of the Returned Value
12    read creates a bitwise copy of T, regardless of whether T is Copy. If T is not Copy, using both
            the returned value and the value at *src can violate memory safety. Note that assigning
           to *src counts as a use because it will attempt to drop the value at *src.
13    write() can be used to overwrite data without causing it to be dropped.
14    }


                       Listing (6) Safety property document of ptr::read in Rust 1.75.
 1    # SafetyProperty
 2    # Identifier: primitive.pointer.html#method.read
 3    # Type: *const T
 4    # Signature: fn read<T>(src: *const T) -> T
 5
 6    self: Allocated
 7    A null pointer is never valid, not even for accesses of size zero.
 8    Even for operations of size zero, the pointer must not be pointing to deallocated memory.
 9
10    self: Bounded
11    The memory range of the given size starting at the pointer must all be within the bounds of a
           single allocated object.
12
13    self: Initialized
14    self must point to a properly initialized value of type T.
15
16    self: Layout
17    self must be properly aligned.
18
19    retval: DualOwned
20    If T is not Copy, using both the returned value and the value at self can violate memory safety
           . Note that assigning to self counts as a use because it will attempt to drop the value at
            self.



Fig. 4. The example of a revised document compared with the native document for unsafe API ptr::read.
The safety property document has a unique identifier and matches the safety properties, parameters, and
native document slices, providing a more structured format. Additionally, it eliminates the secondary link
jumps, making it more intuitive.


4.5    Integrating Revised Documents into Rust Analyzer
rust-analyzer is a widely used Language Server Protocol (LSP) for the Rust programming language.
It communicates with VSCode through a background process to provide features such as code
completion and navigation. In real-world Rust programming, we have integrated safety property

                                                     14
Fearless Unsafe. A More User-friendly Document for Unsafe Rust Programming Base on Refined Safety Properties.
                                                                                                      arxiv, 2024,



    Documents Revision

                              Identifier: Fn
                              P: Parameter
                              S: SafetyProperty
                              D: [DocumentSlice1,
                                DocumentSlice2, ..]
    Native Documents                                             SP Documents                       SP Documents
        Raw Texts                                                    TOML                               JSON


                                  self    Allocated       Even for operations of size zero ...               Parsing
                                          Initialized     The value `self` points to must ...
                                          Deferencable    The memory range of the given ...                        &
                                          Layout          `self` must be properly ...                       Serialized
                                          Freed           Executes the destructor ...


    fn main() {    User Snippet
    ...                                  Hovering                                    Deserialized
        unsafe{
        mem::drop_in_place(p);
        }
    ...                                                  Modified Plugin

Fig. 5. The workflow of the plugin. This tool implants safety property documents into the hover component
of the rust-analyzer, providing users with safety prompts when hovering over unsafe functions.


documents into rust-analyzer to assist users in reading and using unsafe functions more safely.
This section introduces the overall framework of our prototype.
   In Figure 5, the safety properties documents are encoded in a TOML file, using key-value pairs to
store the entire set. Each unsafe API has a unique identifier as the primary key, forming the basis
for document maintenance. The TOML file adopts the following recording method:
            Parameter.SafetyProperty.[ DocumentSlice1, DocumentSlice2, .. ]
Since one safety property may connect with several parameters, one parameter may have to satisfy
multiple safety properties, and one safety property for one parameter may correspond to various
document slices; the primary key is the parameter, the secondary key is safety property, and the
tertiary key is an array of document slices in the markdown format.
   We convert TOML into JSON, use an external program to parse it and serialize it in a specific
data structure. It records the mapping between API identifiers and safety property documents. The
analyzer can deserialize the mapping to avoid parsing overhead. In rust-analyzer, we customized
the hover component; the hover component can show additional information, such as the document
for a definition, when "focusing" code. Focusing is usually done by hovering with a mouse but
can also be triggered with a shortcut. When a user hovers over a function, we generate a link to
the webpage document for that function to match our identifier. If the database contains its safety
property document, we intercept the hover component, inject the safety property document, and
callback to the user.

5    VERIFYING REAL-WORLD PROGRAM VULNERABILITIES
To answer RQ3, this section presents the practical usability of safety properties in real-world
scenarios by analyzing the root cause of existing CVEs to validate SP coverage. It also surveys the
frequency of unsafe API in the Rust ecosystem by gathering the unsafe API usage on crates.io [21].

                                                            15
arxiv, 2024,                                     Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu


         Listing (7) Source code of CVE-2021-45709 in the crypto2 crate through 2021-10-08 for Rust.
1     #[inline]
2     fn xor_si512_inplace(a: &mut [u8], b: &[u32; Chacha20::STATE_LEN]) {
3         unsafe {
4             let d1 = core::slice::from_raw_parts_mut(a.as_mut_ptr() as *mut u32, Chacha20::
           STATE_LEN);
5             for i in 0..Chacha20::STATE_LEN {
6                 d1[i] ^= b[i];
7             }
8         }
9     }


                        Listing (8) Description documented in RUSTSEC-2021-0121.
1     Description
2     The implementation does not enforce alignment requirements on input slices while incorrectly
           assuming 4-byte alignment through an unsafe call to std::slice::from_raw_parts_mut, which
           breaks the contract and introduces undefined behavior.



Fig. 6. Example of the CVE classification. The buggy source code and description of CVE-2021-45709 (in
RUSTSEC). This CVE violates the safety requirement of Layout: Aligned and triggers UB when using the
unsafe API slice::from_raw_parts_mut.



5.1    Studying Root Causes of Rust CVEs
5.1.1 Workflow. We first create a database of existing CVEs filtered by misusing unsafe code and
then classify their root causes into safety properties by manual code review.
CVE Database. We utilized the CVEMitre [20] as the dataset. To retain Rust-related CVEs as many
as possible, we conducted searches by keyword "Rust". The results were sorted in reverse chrono-
logical order of CVE IDs, ranging from CVE-2017-20004 [13] to CVE-2024-21629 [15]. We filtered
them through the CVE descriptions to only include those involving memory safety issues, remov-
ing others such as information leaks. Additionally, we filtered CVEs with panic safety since the
security implications during stack unwinding are highly dependent on where the panic occurs [24].
Furthermore, retained CVEs should not be associated with deprecated or yanked crates and should
be linkable to source code for code audits.
CVE Audit. We conducted an in-depth analysis of the retained CVEs, utilizing manual code auditing
to determine whether the erroneous code segments were caused by misuse of unsafe code, further
analyzing whether they could be classified as violations of safety properties. The first and second
authors double-checked the results. Due to the concise descriptions provided on the CVEMitre, we
considered multiple sources, including issues, pull requests, and RUSTSEC [26]. All CVEs caused by
safe code were excluded, but not those originating from unsafe interiors. In the final dataset (198
CVEs in total), 86.36% of them were attributed to misuse of unsafe APIs within the standard library.
The remaining CVEs were caused by other unsafe operations (e.g., dereferencing raw pointers),
usage of unsafe functions outside the standard library, and issues occurring beyond Rust’s FFI
boundaries.
CVE Example.We present our analysis of a typical CVE. Figure 6 provides the necessary details for
auditing CVE-2021-45709 [2, 14]. Based on the explicit error description, we were able to locate the
defective source code and confirm the misuse of slice::from_raw_parts_mut [64]. Specifically,
it was found that the mismatch between the constraints of the parameter a (line 2) and the unsafe

                                                     16
Fearless Unsafe. A More User-friendly Document for Unsafe Rust Programming Base on Refined Safety Properties.
                                                                                                      arxiv, 2024,



                   70                                                                            70                                                                2024

                   60                                                                                                                                              2023

                   50                                                                                                                                              2022
                                                  46
                   40                                                                                                                                              2021

                   30      27                                                                                                                                      2020

                   20                                         20                                                       19                                          2019

                   10                                                                                                                                              2018
                                       5                                                                     5                    4        5
                    0                                                      0            0                                                          0        0      2017
                                   Allocated
                                               Initialized


                                                                      Unreachable



                                                                                                         DualOwned
                                                                                                                     Aliased
                         Bounded




                                                                                    System IO




                                                                                                                               Untyped



                                                                                                                                                          Pinned
                                                                                                Thread




                                                                                                                                         Freed
                                                                                                                                                 Leaked
                                                             Layout




Fig. 7. SP classification results and their duration on existing Rust CVEs. These CVEs are memory-safety issues
resulting from misusing unsafe code and ignoring unrelated issues, such as leaking sensitive information.


call (line 4) resulted in undefined behavior. In our labeled results, this API is marked with the
following safety properties: Allocated, Bounded, Initialized, Layout, and Aliased. This CVE violated
the requirement of Layout: Aligned, leading to undefined behavior.
5.1.2 Results. We screened 419 CVEs and conducted thorough code reviews on the remaining 198
CVEs after filtering. We categorized them based on the root causes, matching them with safety
properties, and analyzed their distribution. Manual validation confirmed that the root causes of
CVEs caused by unsafe Rust did not exceed the scope of safety properties we have defined.
Distribution. Figure 7 depicts the results: Thread (70), Initialized (46), and Bounded (27) has a
significant number. Following are Layout (20), Aliased (19), Allocated (5), and the other three safety
properties (ranging from 4 to 20). 4 safety properties have no corresponding CVEs. The period of
most CVEs is gathered from as early as August 2019 to as late as December 2021 in a temporal
perspective, which contains 91.84% of listed CVEs.
Case Study. The categorized results reveal that the highest proportion is caused by violations of
Thread (70). It caused by the incorrect Send/Sync [56, 57] implementations for the user-defined
types, without verifying whether each field meets the requirements of those traits, potentially
leading to data races and memory safety issues across thread boundaries. Initialized ranked second
(46), with scenarios summarized as follows: 1) creating uninitialized buffers and passing them as
parameters to custom Read [62] implementations, exposing uninitialized memory to safe code; 2)
modifying the field directly to increase buffer lengths in vectors, leading to out-of-bounds writes
and dropping uninitialized memory; 3) creating an uninitialized NonNull pointer, violating data
invariance.

5.2   Gathering Statistics on crates.io Ecosystem
Section 5.1 indicates that 86.36% of the retained CVEs bounded with safety properties were caused
by misusing unsafe APIs from the standard library. This observation prompted us to conduct a
statistical analysis of unsafe API usage within the Rust ecosystem.

                                                                                                   17
arxiv, 2024,                                            Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu


                  5k    4,924 159,755                                            crates contain 160k
                                                                                 occurrences
                                                                                                140k
                  4k
                         111,223                                                               120k
                  3k          2,838                                                            100k
                                                                                               80k
                  2k
                                      2,070
                                              1,832                                            60k
                                                      1,611 1,491
                                       32,186                       1,183 1,168 1,030          40k
                  1k
                                             21,270                                674     20k
                                                        9,31911,7934,589 6,251 5,193
                                                                                     1,575
                   0                                                                           0


                                                           he ing



                                                            p_i oc
                       te




                                              it




                                                                       e
                            ptr

                                      d



                                                    py _unc ed
                                                   ge ove ked



                                                                      ut


                                                                   lac
                                   roe

                                          _in
                       mu




                                                                  _m

                                                         dro all
                                                                    k
                            m_




                                                        nc pp
                                                ec

                                                                  c




                                                               n_p
                                       me
                                 ze




                                                      _no he



                                                               ed
                   ns




                                                     t_u rla
                        fro




                                               ch
                                      su




                                                             ck
                 tra




                                              un
                                   as
                                          w_

                                                          t
                                                         n
                                                ge
                                        ne

                                                   co




Fig. 8. Statistics on unfiltered strings (unsafe APIs) in the crates.io ecosystem. The top ten most frequently
used strings across all repositories and their source code occurrences are sorted by the sum of crates.


5.2.1 Crates.io Database. Crates.io is the package platform for Rust, where open-source libraries
can be published for users. We utilized all active repositories on this platform as our database and
employed regular expression matching on the source code to gather statistics, a process that does
not involve compilation to aviod overhead. Based on function names, we merged identically named
unsafe APIs, creating a dictionary containing 140 unique strings. We removed 20 strings that were
identical to other safe functions in the standard library (e.g., add [60, 61]). To enhance the accuracy,
we further filtered out cases where the unsafe keyword was not used in the source code.
5.2.2 Statistics. As of 2023-01-30, we mined all latest crates. The statistics indicate that 21,506
crates contain unsafe code among the 103,516 crates (3,614 are yanked). We generated a summary
for each string: the number of crates for the string appearance and the total usage across all
crates. The top ten most frequently used strings are shown in Figure 8, which depicts statistical
results in two dimensions. We observed that the primary scenarios encompass type conversions
(transmute), manual memory management (zeroed, alloc, drop_in_place), unsafe constructors
(new_unchecked), deferred initialization (assume_init), unsafe indexing (get_unchecked/mut),
unsafe referencing (from_ptr), and unsafe memory copying (copy_nonoverlapping).

6    THREATS TO VALIDITY
For internal validity threats, the standard library might not provide exhaustive coverage for investi-
gating the categories toward safety requirements. We validated the results based on the current CVE
to address this limitation. Based on expert knowledge, different programmers may hold divergent
views regarding which sub-properties of safety properties should be merged or separated; thus, no
fixed conclusion can be drawn. The primary contribution is to provide a method to extract safety
properties, label functions, and revise documents. There may be other methods besides ours, but
our research is the inaugural study to concentrate on categorizing safety requirements in Rust.
   For external validity threats, due to the ongoing development, the programming style and the
language standard may evolve. Future updates may introduce new unsafe APIs, deprecate old APIs,

                                                            18
Fearless Unsafe. A More User-friendly Document for Unsafe Rust Programming Base on Refined Safety Properties.
                                                                                                      arxiv, 2024,


Table 6. Open-source code analyzers that can detect specific safety properties. Each static bug detection tool
may not necessarily support all scenarios related to the corresponding safety property.

                    Static Analyzer     Supported Safety Properties
                       Rudra [6]        Initialized, Thread, DualOwned
                    SafeDrop [11]       Allocated, Initialized,DualOwned, Freed
                  MirChecker [37]       Bounded, DualOwned
                   FFIChecker [38]      Allocated, Leaked (Rust/C FFI only, based on LLVM)
                     rCanary [3]        Leaked




or modify them. We acknowledge the existence of uncommon safety descriptions that cannot be
classified based solely on the standard library or CVEs because they have not been documented yet.

7   RELATED WORK
Empirical Studies on Rust. Empirical studies focus on how developers write unsafe code in
real-world programs [5, 18, 49, 50, 73] or existing CVEs [72]. They summarize bug patterns and
insights into different aspects of safety guarantees. However, these studies do not classify the
safety descriptions through the documents. Several empirical studies focus on the Rust learning
curve [1, 19] and the programming challenges introduced by compiler errors [74]. Researchers
also leveraged the Stack Overflow comment to understand real-world development problems [74].
However, we are more concerned with experienced system engineers who are proficient than Rust
beginners. They need Unsafe Rust to achieve low-level control and better understand the safety
requirements when writing unsafe code.
Bug Detections in Rust. Researches use different methods to find bugs in Rust programs, including
formal verification [4, 10, 16, 27, 28, 30, 31, 34, 41, 71], symbolic execution [8, 39], model checking [6,
11, 37, 68, 70], interpreter [9], and fuzzing [17, 29]. Some of the above approaches provide bug
patterns corresponding to safety properties, as listed in Table 6. For example, a significant portion of
CVEs on Initialized (85.3%) and Thread (92.9%) were found by Rudra [6]. This observation suggests
that analyzers designed for bug patterns may effectively identify vulnerabilities that violate specific
safety properties. Many bugs related to safety properties may have yet to be discovered, as shown
in Figure 7.
Benefiting Rust Community. CVE classification provides a set of CVE lists for each safety property
that can be used as a benchmark. This benchmark can be employed to evaluate the effectiveness of
research prototypes or bug-detection tools designed for particular safety properties (e.g., SafeDrop
and Rudra). As far as we know, the Rust community needs a unified, ground-truth-supported
benchmark to support effectiveness comparisons based on safety issues. We advocate for setting
such a benchmark to serve as a basis for the SE community.

8   CONCLUSION
With increasing system programs adopting Rust, understanding the safety requirements when writ-
ing unsafe code is crucial, particularly with well-defined categorization. To this end, we conducted a
comprehensive empirical study on safety requirements through the unsafe boundary. In this paper,
we extended and refined our study in ICSE 2024. We focus on unsafe API documents in the standard
library to infer safety properties and then categorize unsafe APIs and existing CVEs. Furthermore,
we completely revised the native documents and integrated them into the rust-analyzer. This tool

                                                        19
arxiv, 2024,                                            Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu


prompts users with safety requirements when invoking unsafe APIs. Through these efforts, we aim
to promote the standardization of systematic documents for Unsafe Rust in the Rust community.

ACKNOWLEDGMENTS
This work is supported by the National Natural Science Foundation of China (No. 62372304).

REFERENCES
 [1] Parastoo Abtahi and Griffin Dietz. 2020. Learning Rust: How Experienced Programmers Leverage Resources to Learn
     a New Programming Language. In Extended Abstracts of the 2020 CHI Conference on Human Factors in Computing
     Systems. 1–8. doi:10.1145/3334480.3383069.
 [2] RUSTSEC-2021-0121: Non aligned u32 read in Chacha20 encryption and decryption. 2021. https://rustsec.org/advisories/
     RUSTSEC-2021-0121.html (Accessed on 01/11/2024).
 [3] arXiv. 2023. rCanary: Detecting Memory Leaks Across Semi-automated Memory Management Boundary in Rust. In
     arXiv.
 [4] Vytautas Astrauskas, Aurel Bílỳ, Jonáš Fiala, Zachary Grannan, Christoph Matheja, Peter Müller, Federico Poli, and
     Alexander J Summers. 2022. The prusti project: Formal verification for rust. In NASA Formal Methods Symposium.
     Springer, 88–108. doi:10.1145/3547647.
 [5] Vytautas Astrauskas, Christoph Matheja, Federico Poli, Peter Müller, and Alexander J Summers. 2020. How do
     programmers use unsafe rust? Proceedings of the ACM on Programming Languages 4, OOPSLA (2020), 1–27.
     doi:10.1145/3334480.3383069.
 [6] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon Lim, and Taesoo Kim. 2021. Rudra: finding memory safety bugs
     in rust at the ecosystem scale. In Proceedings of the ACM SIGOPS 28th Symposium on Operating Systems Principles.
     84–99. doi:10.1145/3477132.3483570.
 [7] Josh Berdine, Cristiano Calcagno, and Peter W O’hearn. 2005. Symbolic execution with separation logic. In Programming
     Languages and Systems: Third Asian Symposium, APLAS 2005, Tsukuba, Japan, November 2-5, 2005. Proceedings 3. Springer,
     52–68. doi: 10.1007/11575467_5.
 [8] MIRAI Contributors. 2024. MIRAI: Rust mid-level IR Abstract Interpreter. https://github.com/facebookexperimental/
     MIRAI (Accessed on 01/11/2024).
 [9] Miri Contributors. 2024. Miri: An interpreter for Rust’s mid-level intermediate representation. https://github.com/rust-
     lang/miri (Accessed on 01/11/2024).
[10] Will Crichton, Marco Patrignani, Maneesh Agrawala, and Pat Hanrahan. 2022. Modular information flow through
     ownership. In Proceedings of the 43rd ACM SIGPLAN International Conference on Programming Language Design and
     Implementation. 1–14. doi:10.1145/3519939.3523445.
[11] Mohan Cui, Chengjun Chen, Hui Xu, and Yangfan Zhou. 2023. SafeDrop: Detecting memory deallocation bugs of rust
     programs via static data-flow analysis. ACM Transactions on Software Engineering and Methodology 32, 4 (2023), 1–21.
     doi:10.1145/3542948.
[12] Mohan Cui, Shuran Sun, Hui Xu, and Yangfan Zhou. 2024. Is unsafe an Achilles’ Heel? A Comprehensive Study of
     Safety Requirements in Unsafe Rust Programming. In Proceedings of the IEEE/ACM 46th International Conference on
     Software Engineering. 1–13. doi:10.1145/3597503.3639136.
[13] CVE-2017-20004. 2017. https://www.cve.org/CVERecord?id=CVE-2017-20004 (Accessed on 01/11/2024). In the standard
     library in Rust before 1.19.0, there is a synchronization problem in the MutexGuard object. MutexGuards can be used
     across threads with any types, allowing for memory safety issues through race conditions.
[14] CVE-2021-45709. 2021. https://www.cve.org/CVERecord?id=CVE-2021-45709 (Accessed on 01/11/2024). In the standard
     library in Rust before 1.19.0, there is a synchronization problem in the MutexGuard object. MutexGuards can be used
     across threads with any types, allowing for memory safety issues through race conditions.
[15] CVE-2024-21629. 2024. https://www.cve.org/CVERecord?id=CVE-2024-21629 (Accessed on 01/11/2024). Rust EVM is
     an Ethereum Virtual Machine interpreter. In rust-evm, a feature called record_external_operation was introduced,
     allowing library users to record custom gas changes. This feature can have some bogus interactions with the call
     stack.
[16] Hoang-Hai Dang, Jacques-Henri Jourdan, Jan-Oliver Kaiser, and Derek Dreyer. 2019. RustBelt meets relaxed memory.
     Proceedings of the ACM on Programming Languages 4, POPL (2019), 1–29. doi:10.1145/3371102.
[17] Kyle Dewey, Jared Roesch, and Ben Hardekopf. 2015. Fuzzing the Rust typechecker using CLP (T). In 2015 30th
     IEEE/ACM International Conference on Automated Software Engineering (ASE). IEEE, 482–493. doi:10.1109/ASE.2015.65.
[18] Ana Nora Evans, Bradford Campbell, and Mary Lou Soffa. 2020. Is Rust used safely by software developers?. In Proceed-
     ings of the ACM/IEEE 42nd International Conference on Software Engineering. 246–257. doi:10.1145/3377811.3380413.


                                                             20
Fearless Unsafe. A More User-friendly Document for Unsafe Rust Programming Base on Refined Safety Properties.
                                                                                                      arxiv, 2024,


[19] Kelsey R Fulton, Anna Chan, Daniel Votipka, Michael Hicks, and Michelle L Mazurek. 2021. Benefits and drawbacks of
     adopting a secure programming language: Rust as a case study. In Seventeenth Symposium on Usable Privacy and Security
     (SOUPS 2021). USENIX Association, 597–616. https://www.usenix.org/conference/soups2021/presentation/fulton
[20] CVE Group. 2024. The CVE Program. https://www.cve.org (Accessed on 01/11/2024).
[21] Rust Group. 2024. The Rust community’s crate registry. https://crates.io (Accessed on 01/11/2024).
[22] Rust Group. 2024. The Rust Reference. https://doc.rust-lang.org/reference (Accessed on 01/11/2024).
[23] Rust Group. 2024. The rustdoc book. https://doc.rust-lang.org/rustdoc (Accessed on 01/11/2024).
[24] Rust Group. 2024. The Rustonomicon. https://doc.rust-lang.org/nomicon (Accessed on 01/11/2024).
[25] Rust Group. 2024. TheRustStandardLibrary. https://doc.rust-lang.org/std (Accessed on 01/11/2024).
[26] Rust Secure Code Working Group. 2024. RUSTSEC: A vulnerability database for the Rust ecosystem. https://rustsec.org
     (Accessed on 01/11/2024).
[27] Florian Hahn. 2016. Rust2Viper: Building a static verifier for Rust. Master’s thesis. doi:10.3929/ethz-a-010669150 .
[28] Son Ho and Jonathan Protzenko. 2022. Aeneas: Rust verification by functional translation. Proceedings of the ACM on
     Programming Languages 6, ICFP (2022), 711–741. doi:10.1145/3547647.
[29] Jianfeng Jiang, Hui Xu, and Yangfan Zhou. 2021. RULF: Rust library fuzzing via API dependency graph tra-
     versal. In 2021 36th IEEE/ACM International Conference on Automated Software Engineering (ASE). IEEE, 581–592.
     doi:10.1109/ASE51524.2021.9678813.
[30] Ralf Jung, Hoang-Hai Dang, Jeehoon Kang, and Derek Dreyer. 2019. Stacked borrows: an aliasing model for Rust.
     Proceedings of the ACM on Programming Languages 4, POPL (2019), 1–32. doi:10.1145/3371109.
[31] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. RustBelt: Securing the foundations
     of the Rust programming language. Proceedings of the ACM on Programming Languages 2, POPL (2017), 1–34.
     doi:10.1145/3158154.
[32] Steve Klabnik and Carol Nichols. 2019. The Rust Programming Language (Covers Rust 2018). No Starch Press.
[33] Nick Kolakowski. 2019. Fastest-Growing Programming Languages on GitHub. https://insights.dice.com/2019/11/11/10-
     github-programming-languages (Accessed on 01/11/2024).
[34] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell, Bryan Parno,
     and Chris Hawblitzel. 2023. Verus: Verifying rust programs using linear ghost types. Proceedings of the ACM on
     Programming Languages 7, OOPSLA1 (2023), 286–315. doi:10.1145/3586037.
[35] Amit Levy, Bradford Campbell, Branden Ghena, Daniel B Giffin, Shane Leonard, Pat Pannuto, Prabal Dutta, and Philip
     Levis. 2017. The tock embedded operating system. In Proceedings of the 15th ACM Conference on Embedded Network
     Sensor Systems. 1–2. doi:10.1145/3131672.3136988.
[36] Amit Levy, Bradford Campbell, Branden Ghena, Daniel B Giffin, Pat Pannuto, Prabal Dutta, and Philip Levis. 2017.
     Multiprogramming a 64kb computer safely and efficiently. In Proceedings of the 26th Symposium on Operating Systems
     Principles. 234–251. doi:10.1145/3132747.3132786.
[37] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John CS Lui. 2021. MirChecker: detecting bugs in Rust programs
     via static analysis. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security.
     2183–2196. doi:10.1145/3460120.3484541.
[38] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John CS Lui. 2022. Detecting cross-language memory management
     issues in rust. In European Symposium on Research in Computer Security. Springer, 680–700. doi:10.1007/978-3-031-
     17143-7_33.
[39] Marcus Lindner, Jorge Aparicius, and Per Lindgren. 2018. No panic! Verification of Rust programs by sym-
     bolic execution. In 2018 IEEE 16th International Conference on Industrial Informatics (INDIN). IEEE, 108–114.
     doi:10.1109/INDIN.2018.8471992.
[40] Nicholas D Matsakis and Felix S Klock. 2014. The rust language. ACM SIGAda Ada Letters 34, 3 (2014), 103–104.
     doi:10.1145/2692956.2663188.
[41] Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. 2021. RustHorn: CHC-based verification for Rust programs.
     ACM Transactions on Programming Languages and Systems (TOPLAS) 43, 4 (2021), 1–54. doi:10.1145/3462205.
[42] Stack Overflow. 2016. Stack Overflow Developer Survey 2016. https://insights.stackoverflow.com/survey/2016#
     technology-most-loveddreaded-and-wanted (Accessed on 01/11/2024).
[43] Stack Overflow. 2017. Stack Overflow Developer Survey 2017. https://insights.stackoverflow.com/survey/2017#
     technology-most-loveddreaded-and-wanted (Accessed on 01/11/2024).
[44] Stack Overflow. 2018. Stack Overflow Developer Survey 2018. https://insights.stackoverflow.com/survey/2018#
     technology-most-loveddreaded-and-wanted (Accessed on 01/11/2024).
[45] Stack Overflow. 2019. Stack Overflow Developer Survey 2019. https://insights.stackoverflow.com/survey/2019#
     technology-most-loveddreaded-and-wanted (Accessed on 01/11/2024).
[46] Stack Overflow. 2020. Stack Overflow Developer Survey 2020. https://insights.stackoverflow.com/survey/2020#
     technology-most-loveddreaded-and-wanted (Accessed on 01/11/2024).


                                                           21
arxiv, 2024,                                               Mohan Cui, Penglei Mao, Shuran Sun, Yangfan Zhou, and Hui Xu


[47] Stack Overflow. 2021. Stack Overflow Developer Survey 2021. https://insights.stackoverflow.com/survey/2021#
     technology-most-loveddreaded-and-wanted (Accessed on 01/11/2024).
[48] Stack Overflow. 2022. Stack Overflow Developer Survey 2022. https://survey.stackoverflow.co/2022 (Accessed on
     01/11/2024).
[49] Alex Ozdemir. 2019. Unsafe in Rust: Syntactic Patterns. (2019), (Accessed on 01/11/2024). https://cs.stanford.edu/
     ~aozdemir/blog/unsafe-rust-syntax
[50] Boqin Qin, Yilun Chen, Zeming Yu, Linhai Song, and Yiying Zhang. 2020. Understanding memory and thread safety
     practices and issues in real-world Rust programs. In Proceedings of the 41st ACM SIGPLAN Conference on Programming
     Language Design and Implementation. 763–779. doi:10.1145/3385412.3386036.
[51] Youren Shen, Hongliang Tian, Yu Chen, Kang Chen, Runji Wang, Yi Xu, Yubin Xia, and Shoumeng Yan. 2020. Occlum: Se-
     cure and efficient multitasking inside a single enclave of intel sgx. In Proceedings of the Twenty-Fifth International Confer-
     ence on Architectural Support for Programming Languages and Operating Systems. 955–970. doi:10.1145/3373376.3378469.
[52] std::ffi::VaListImpl::arg. 2024. https://doc.rust-lang.org/std/ffi/struct.VaListImpl.html#method.arg (Accessed on
     01/11/2024).
[53] std::intrinsics::breakpoint. 2024. https://doc.rust-lang.org/std/intrinsics/fn.breakpoint.html (Accessed on 01/11/2024).
[54] std::intrinsics::nearbyintf32. 2024.       https://doc.rust-lang.org/std/intrinsics/fn.nearbyintf32.html (Accessed on
     01/11/2024).
[55] std::intrinsics::pref_align_of. 2024. https://doc.rust-lang.org/std/intrinsics/fn.pref_align_of.html (Accessed on
     01/11/2024).
[56] std::marker::Send. 2024. https://doc.rust-lang.org/std/marker/trait.Send.html (Accessed on 01/11/2024).
[57] std::marker::Sync. 2024. https://doc.rust-lang.org/std/marker/trait.Sync.html (Accessed on 01/11/2024).
[58] std::mem::ManuallyDrop::take. 2024. https://doc.rust-lang.org/std/mem/struct.ManuallyDrop.html#method.take (Ac-
     cessed on 01/11/2024).
[59] std::mem::zeroed. 2024. https://doc.rust-lang.org/std/mem/fn.zeroed.html (Accessed on 01/11/2024).
[60] std::ops::Add. 2024. https://doc.rust-lang.org/std/ops/trait.Add.html (Accessed on 01/11/2024).
[61] std::ptr::add. 2024. https://doc.rust-lang.org/std/primitive.pointer.html#method.add (Accessed on 01/11/2024).
[62] std::ptr::read. 2024. https://doc.rust-lang.org/std/ptr/fn.read.html (Accessed on 01/11/2024).
[63] std::ptr::swap. 2024. https://doc.rust-lang.org/std/ptr/fn.swap.html (Accessed on 01/11/2024).
[64] std::slice::from_raw_parts_mut. 2024. https://doc.rust-lang.org/std/slice/fn.from_raw_parts_mut.html (Accessed on
     01/11/2024).
[65] std::slice::SliceIndex. 2024. https://doc.rust-lang.org/std/slice/trait.SliceIndex.html (Accessed on 01/11/2024).
[66] std::u16::unchecked_mul. 2024. https://doc.rust-lang.org/std/primitive.u16.html#method.unchecked_mul (Accessed on
     01/11/2024).
[67] std::u8::unchecked_mul. 2024. https://doc.rust-lang.org/std/primitive.u8.html#method.unchecked_mul (Accessed on
     01/11/2024).
[68] John Toman, Stuart Pernsteiner, and Emina Torlak. 2015. Crust: a bounded verifier for rust (N). In 2015 30th IEEE/ACM
     International Conference on Automated Software Engineering (ASE). IEEE, 75–80. doi:10.1109/ASE.2015.77.
[69] Gert-Jan Van Rootselaar and Bart Vermeulen. 1999. Silicon debug: scan chains alone are not enough. In International
     Test Conference 1999. Proceedings (IEEE Cat. No. 99CH37034). IEEE, 892–902. doi:10.1109/TEST.1999.805821.
[70] Alexa VanHattum, Daniel Schwartz-Narbonne, Nathan Chong, and Adrian Sampson. 2022. Verifying dynamic trait
     objects in Rust. In Proceedings of the 44th International Conference on Software Engineering: Software Engineering in
     Practice. 321–330. doi:10.1145/3510457.3513031.
[71] Fabian Wolff, Aurel Bílỳ, Christoph Matheja, Peter Müller, and Alexander J Summers. 2021. Modular specification
     and verification of closures in Rust. Proceedings of the ACM on Programming Languages 5, OOPSLA (2021), 1–29.
     doi:10.1145/3485522.
[72] Hui Xu, Zhuangbin Chen, Mingshen Sun, Yangfan Zhou, and Michael R Lyu. 2021. Memory-safety challenge considered
     solved? An in-depth study with all Rust CVEs. ACM Transactions on Software Engineering and Methodology (TOSEM)
     31, 1 (2021), 1–25. doi:10.1145/3466642.
[73] Zeming Yu, Linhai Song, and Yiying Zhang. 2019. Fearless concurrency? understanding concurrent programming
     safety in real-world rust software. arXiv preprint arXiv:1902.01906 (2019). arXiv:arXiv:1908.06849
[74] Shuofei Zhu, Ziyi Zhang, Boqin Qin, Aiping Xiong, and Linhai Song. 2022. Learning and programming challenges of
     rust: A mixed-methods study. In Proceedings of the 44th International Conference on Software Engineering. 1269–1281.
     doi:10.1145/3510003.3510164.




                                                                22
