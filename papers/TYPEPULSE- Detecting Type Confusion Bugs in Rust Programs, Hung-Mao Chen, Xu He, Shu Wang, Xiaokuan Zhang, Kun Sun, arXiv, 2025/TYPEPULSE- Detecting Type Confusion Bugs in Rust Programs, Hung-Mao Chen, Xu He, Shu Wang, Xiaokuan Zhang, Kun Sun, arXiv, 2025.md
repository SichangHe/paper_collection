                                                       T YPE P ULSE: Detecting Type Confusion Bugs in Rust Programs

                                                              Hung-Mao Chen∗ , Xu He∗ , Shu Wang∗† , Xiaokuan Zhang∗ , Kun Sun∗
                                                                                 ∗ George Mason University
                                                                                    † Palo Alto Networks
arXiv:2502.03271v1 [cs.CR] 5 Feb 2025




                                                                 Abstract                                     Rust is fundamentally divided into two separate sub-
                                        Rust supports type conversions and safe Rust guarantees the        languages: safe Rust and unsafe Rust [62]. Safe Rust enforces
                                        security of these conversions through robust static type check-    strict compile-time checks to maintain memory safety and
                                        ing and strict ownership guidelines. However, there are in-        type safety. However, these checks can be excessively re-
                                        stances where programmers need to use unsafe Rust for cer-         strictive, blocking some essential but risky operations like
                                        tain type conversions, especially those involving pointers.        accessing raw pointers. To address this, Rust introduces the
                                        Consequently, these conversions may cause severe memory            unsafe keyword for such situations. When employing unsafe
                                        corruption problems. Despite extensive research on type con-       Rust, it falls upon the programmer to uphold memory safety
                                        fusion bugs in C/C++, studies on type confusion bugs in Rust       since the typical compile-time checks are circumvented.
                                        are still lacking. Also, due to Rust’s new features in the type       Similar to traditional programming languages such as
                                        system, existing solutions in C/C++ cannot be directly applied     C/C++, Rust also supports type conversions [43], where a
                                        to Rust. In this paper, we develop a static analysis tool called   variable is initially converted from type A to type B and sub-
                                        T YPE P ULSE to detect three main categories of type confusion     sequently accessed as type B. Safe Rust guarantees the secu-
                                        bugs in Rust including misalignment, inconsistent layout, and      rity of these conversions through robust static type checking
                                        mismatched scope. T YPE P ULSE first performs a type conver-       and strict ownership guidelines. Rust automatically infers the
                                        sion analysis to collect and determine trait bounds for type       types of variables and expressions from their context and use.
                                        pairs. Moreover, it performs a pointer alias analysis to resolve   Also, the ownership feature helps ensure memory and concur-
                                        the alias relationship of pointers. Following the integration of   rency safety by tracking the lifetime and borrowing at compile
                                        information into the property graph, it constructs type patterns   time [28]. Nevertheless, there are instances where program-
                                        and detects each type of bug in various conversion scenar-         mers need to use unsafe Rust for certain type conversions,
                                        ios. We run T YPE P ULSE on the top 3,000 Rust packages            especially those that involve pointers. For instance, since di-
                                        and uncover 71 new type confusion bugs, exceeding the total        rect reference conversions are not allowed, conversions must
                                        number of type confusion bugs reported in RUSTSEC over             be first made at the raw pointer level and then converted back
                                        the past five years. We have received 32 confirmations from        to references using unsafe Rust. Consequently, these conver-
                                        developers, along with one CVE ID and six RUSTSEC IDs.             sions may cause severe memory corruption problems similar
                                                                                                           to those found in C/C++ [36–38]. In the last five years, RUST-
                                        1   Introduction                                                   SEC [10] has reported 32 type confusion bugs that can lead to
                                                                                                           various memory-safety issues such as data leaks, uninitialized
                                        Rust [42] is an emerging programming language known by its         memory, and Out-Of-Bounds (OOB) memory access.
                                        strict enforcement of type safety and memory safety through           Despite extensive research on type confusion bugs in C
                                        compile-time checking, without sacrificing runtime perfor-         and C++ [18, 21, 26, 29], studies on type confusion bugs in
                                        mance. Since memory safety issues in unsafe languages such         Rust are still lacking due to three significant challenges. First,
                                        as C and C++ have been known to lead to catastrophic con-          the conversion of data types between functions complicates
                                        sequences, Rust has become an appealing solution to re-            type analysis, and this complexity cannot be addressed us-
                                        place C and C++, and it has been adopted in major open-            ing traditional interprocedural analysis. For instance, when
                                        sourced projects such as the Linux kernel [65] and the Firefox     a type constructor function creates an instance of a type that
                                        browser [35]. Recently, the White House also calls for adop-       is then handed off to another function for an unsafe type con-
                                        tion of memory-safe programming languages such as Rust to          version, traditional interprocedural analysis fails to track the
                                        secure the cyberspace [23].                                        constructor function as it is absent from the conventional call
graph [31]. Therefore, a new call graph is needed to identify        of developer-enforced check, which is manually implemented
this type of interprocedural type conversion.                        by developers to prevent the type confusion bugs. After veri-
   Second, predicting all possible concrete types that can re-       fication, the bug report will be delivered with the unsafe type
place a generic type in Rust is inherently challenging. Unlike       conversion and type access highlighted.
C and C++, Rust uses trait bounds [12] to constrain generic             We implement a prototype of T YPE P ULSE with 5249 lines
types, ensuring they conform to specific behaviors and ca-           of Rust. To assess T YPE P ULSE’s effectiveness in bug identifi-
pabilities. It adds complexity since trait bounds can have           cation, we first execute it on the type confusion bugs reported
implicit and recursive dependencies on other traits. Moreover,       to RUSTSEC from 2019 to 2024. The findings show that
concrete types may encompass composite types like struct.            T YPE P ULSE can successfully identify all reported type con-
As a result, a method of generic type resolution that adheres        fusion bugs. Next, we perform a large-scale study by running
to the trait bounds is needed.                                       T YPE P ULSE on the top 3,000 popular packages ranked on
   Third, identifying type confusion bugs requires establishing      crates.io and GitHub. We detect 71 new type confusion
whether the pointer alias remains valid after type conversion,       bugs and report all of them to their package developers. We
which is essential for our bug verification process. However,        receive 32 confirmations on the reported bugs at the time of
the ownership and lifetime features in Rust increases the com-       writing. The new bugs occur in many high-profile reposito-
plexity when undertaking pointer analysis. In C++, existing          ries. For example, we demonstrate that the type confusion bug
techniques primarily address the issue of pointer access via         within the pprof package can cause the downstream applica-
alias analysis [20, 30, 32]. Nevertheless, traditional alias anal-   tions to crash (e.g., GreptimeDB with 4.2k stars on GitHub).
ysis needs modification to accommodate the pointer variable
                                                                     Contributions. This paper makes the following contribu-
ownership and lifetime in Rust. For example, when ownership
                                                                     tions:
is transferred to another pointer or the pointer is automatically
                                                                     • We analyze all type confusion bugs in RUSTSEC in the last
deallocated, the original pointer variable becomes invalid,
                                                                        five years and identify the three most prevalent categories
which cannot be detected by existing techniques.
                                                                        of type confusion bugs, namely, misalignment, inconsistent
   To tackle these challenges, we develop T YPE P ULSE, a
                                                                        layout, and mismatched scope.
static analysis tool to detect type confusion bugs in Rust
applications. It consists of two main components, namely,            • We design and implement the first static analysis tool
Property Graph Constructor and Bug Detector. By examining              (T YPE P ULSE) to detect type confusion bugs in Rust, ad-
each function within the crate, property graph constructor             dressing the challenges of interprocedural type conversion,
creates a new call graph that helps identify the type construc-        generic type resolution, and alias analysis due to the unique
tor functions, addressing the first challenge. Property graph          features of Rust.
constructor performs type conversion analysis and pointer            • We evaluate T YPE P ULSE on the top 3,000 Rust pack-
alias analysis. Type conversion analysis is conducted to col-          ages and identify 71 new type confusion bugs which we
lect type pairs (i.e., <source type, destination type>) and trait      have manually confirmed, surpassing the total number of
bounds for generic types through dependency resolution. It is          bugs reported in RUSTSEC in the last five years. We also
employed to address the second challenge. Pointer alias anal-          run T YPE P ULSE on existing type confusion bugs and it
ysis will construct a new alias graph, representing the alias          achieves 100% accuracy, demonstrating the robustness of
relationship of the pointers. When ownership is transferred or         T YPE P ULSE.
dropped, property graph constructor updates the alias graph
to reflect the node connections, which can solve the third chal-
                                                                     2     Background
lenge. As the final output, each function in the property graph
is associated with type pairs, trait bounds, and the pointer alias
graph. The property graph will be utilized by bug detector to
                                                                     2.1    Rust Basics
analyze and verify the type confusion bugs.                          Generic Types and Traits. Rust provides the flexibility of
   Next, bug detector utilizes the property graph to perform         code reuse and type safety with generic types and traits [4,50].
type conversion checks and access checks. First, type con-           By writing code in a type-agnostic manner, generic types al-
version checks are used to identify if the type conversion           low functions, methods, or data structures (e.g., struct) to
creates an invalid type pointer. Second, access checks will          operate on multiple types, which are represented by the place-
be performed to analyze if the invalid type pointer can be           holder (e.g., T, U). Since the generic types will be replaced by
accessed. Via analyzing the type pairs and trait bounds, we          the actual types at the compile-time (i.e., monomorphization),
summarize three patterns of type confusion bugs, namely, mis-        it can prevent the type confusion bugs at run-time. In addition,
alignment, inconsistent layout, and mismatched scope, to help        traits can be used to specify the constraints on generic types.
locate invalid type pointers. When performing access checks,         By applying a trait to a generic type, Rust ensures that the
bug detector will first traverse the alias graph to determine if     type used to replace the generic type should also implement
the invalid type pointer is accessible, then verify the absence      the required methods or characteristics defined by the trait.
For example, the function fn display<T: Copy>(input:
                                                                   1 fn main () {
T) ensures that only the type implementing the Copy trait can      2   let source_ty : u8 = 1;
be initialized as the argument input.                              3   // compile error : non - primitive cast
                                                                   4   let dest_ty = & source_ty as & u32 ;
Safe vs. Unsafe Rust. The central concept of safe Rust is to       5   // Alternative 1: as
                                                                   6   let tmp_ty = & source_ty as *const u8 as *const u32 ;
confirm memory ownership during compilation, where the             7   let dest_ty = unsafe {&* tmp_ty };
compiler checks both the access and the lifetime of memory-        8   // Alternative 2: transmute
                                                                   9   let dest_ty = unsafe {
allocated objects (or values). Moreover, safe Rust permits the    10      transmute :: <& u8 , &u32 >(& source_ty )
borrowing of a value (i.e., making a reference to it) through-    11   };
                                                                  12 }
out the lifetime of the owner variable. In contrast, unsafe is
used to highlight code segments that perform tasks that are not   Listing 1: Type conversion between pointers in unsafe code.
ensured by the compiler, placing the responsibility on devel-
opers to prevent memory safety issues. In Rust, there are five
specific actions necessitating the unsafe keyword [63]: deref-
erencing raw pointers, invoking unsafe functions, altering or     type conversions, including conversions between basic data
accessing mutable static variables, defining unsafe traits, and   types and raw pointers. The use of as generally involves
executing inline assembly. Each of these actions could breach     straightforward bit manipulations or adjustments in values.
Rust’s safety assurances. Unsafe Rust is crucial because it       For example, when an f32 is converted to an i32, the frac-
allows developers to interface with low-level system APIs,        tional component of the floating point number is removed.
libraries written in other languages, or hardware directly.       Consequently, using as can result in data truncation or loss.
Undefined Behaviors. Undefined behavior (UB) refers to the        It’s important to note that under the stringent regulations es-
program whose outcome is not prescribed by the language’s         tablished by rustc, as can be employed in the safe code.
specification, which means that the language standard does        Transmute Operation. Compared to as, the transmute
not define what should happen if the UB occurs. In most cases,    function facilitates more intricate and dangerous transforma-
the result can only be decided by hardware and architectures,     tions. Essentially, transmute performs a bitwise copy from
leading to inconsistent consequences in different environ-        one type to another without altering the bit pattern of the
ments. The outcomes of UB are unpredictable, ranging from         value. However, it modifies the interpretation of these bits by
security vulnerabilities to incorrect compiler optimization and   rustc. For instance, it allows for the direct conversion of an
code generation. The backend of the compiler might perform        i32’s bit pattern to an f32, despite their fundamentally dif-
the optimization based on the assumption that the UB will         ferent representations. The validity of the original bit pattern
not occur. Therefore, we should prevent UB from happening.        in the new type is not assured, making transmute extremely
Rust clearly defines scenarios that might trigger undefined       risky and prone to causing undefined behaviors. Consequently,
behaviors [64], such as dereferencing null pointers, accessing    transmute necessitates the use of unsafe code.
out-of-bounds array elements, and data races when mutating
shared data without synchronization. The design of unsafe         Type Conversion between Pointers. In Rust, pointer-type
help us narrow down the culprit of UB to the code related to      conversions can be achieved through casting and the use of
unsafe code.                                                      transmute operations. However, Rust imposes various restric-
                                                                  tions depending on the pointer types involved, meaning that
                                                                  some conversions are safely handled by Safe Rust, while
2.2    Type Conversion in Rust                                    others require the use of the unsafe keyword. For example,
                                                                  in Listing 1, Safe Rust prohibits direct conversion between
Type conversion from the source type (src_ty) to the desti-       reference types (line 3), forcing developers to resort to two
nation type (dst_ty) consists of two steps: 1 Conversion,         methods within unsafe code. The first method involves con-
which involves altering or reinterpreting the bit pattern of a    verting the reference of the original type to a raw pointer,
variable from one type (src_ty) to a new type (dst_ty), and       followed by its conversion to another raw pointer (line 5).
 2 Access, which involves accessing the variable as the new       To acquire a reference of the new type, developers must first
type (dst_ty). rustc limits developers to performing only         dereference the raw pointer and then form a new reference
explicit type conversions to maintain safety with compile-        (line 6). As dereferencing a raw pointer is not allowed in Safe
time verifications. These conversions can be implemented          Rust, the use of unsafe code becomes unavoidable. Alterna-
through type casting, transmute operations, and traits [50].      tively, the transmute function can be used directly to convert
Given that traits are typically handled by casting and trans-     references (line 9), which must be used with the unsafe key-
mute methods, our discussion will focus solely on casting and     word due to its inherent risks. Such conversions in Unsafe
transmute operations.                                             Rust are prone to type conversion errors because the memory
Casting Operation. The type-casting operation depends on          address remains the same for both pointers (&src_ty and
the keyword as, which is mainly used for secure and direct        &dst_ty), while only the interpretation of the type changes.
Table 1: The details of 32 reported Type Confusion Bugs on             1 #[ cfg ( any ( target_arch = " x86 " ,
                                                                       2    target_arch = " x86_64 "))]
RustSec advisories (2019-2024).                                        3 fn fill_bytes (&mut self, dest : &mut [ u8 ]) {
                                                                       4    // ...
      Year    Type I       Type II     Type III      Others            5
                                                                       6   while filled < end_direct {
      2019   2019-0035       -        2019-0028         -
                                                                       7      let dest_u32 : &mut R :: Results = unsafe {
                         2020-0029                                     8          &mut *( dest [ filled ..]. as_mut_ptr () as
                         2020-0078                 2020-36317          9          *mut <R as BlockRngCore >:: Results ) };
             2020-0035                2020-0029
      2020               2020-0079                  2020-0073         10      self. core . generate ( dest_u32 );
             2020-0050                2020-0165                       11      filled += self. results . as_ref () . len () * 4;
                         2020-0080                  2020-0164
                         2020-0081                                    12      self. index = self. results . as_ref () . len () ;
                                                                      13    }
             2021-0120                                                14    // ...
                         2021-0021    2021-0019
      2021   2021-0121                             2021-0044          15 }
                         2021-0035    2021-0089
             2021-0145
      2022   2022-0041
                         2022-0052
                                      2022-0092
                                                   2022-0034          Listing 2: A misalignment bug in rand_core that casts bytes
                         2022-0074                 2022-0078          slices to integer slices (RUSTSEC-2019-0035 [54]).
                                      2023-0015
      2023       -            -                         -
                                      2023-0055
      2024       -       2024-0347    2024-0001         -

                                                                      4 bytes, leading to the misaligned pointer dereference. Note
                                                                      that developers of rand_core consider that the issue could be
3     Overview                                                        avoided by limiting the target architectures to x86 or x86_64
                                                                      only since these architectures are designed to tolerate mis-
3.1     Motivating Examples                                           aligned memory access. However, the alignment requirement
                                                                      is enforced by the compiler instead of these target architec-
We investigate all bug reports related to type confusion bugs         tures. Once the Rust compiler verifies that safe code adheres
in the RUSTSEC advisories in the last five years [10]. There          to alignment rules, it generates optimized machine code based
are 32 reports but only 26 type confusion bugs; The remaining         on this assurance. However, if unsafe code violates these rules,
six bugs are out of consideration because they are related to         it can cause undefined behavior or crash the program.
other memory safety problems, such as Use-After-Free, which
can be handled by existing tools [15, 17, 33, 44]. The Bug IDs        Type II: Inconsistent Layout Bug. The second type of bug
are listed in Table 1. We categorize the 26 bugs into three           occurs when src_ty and dst_ty have different memory lay-
types based on their root causes, which are misalignment,             outs. In Listing 3, the method as_ref allows casting between
inconsistent layout, and mismatched scope. All 26 bugs are            Table and TableSlice and returns the reference to the new
related to pointer type conversion (i.e., references and raw          type (line 20). However, when the struct type in Rust inher-
pointers) in Unsafe blocks. In this section, we introduce the         its the default representation (e.g. repr(Rust)), the compiler
three bug types and their security impacts.                           may reorder the memory layout, such as the fields of struct.
                                                                      The results of GDB show that after the raw pointer to Table
Type I: Misalignment Bug. The first type of bug occurs
                                                                      is converted to the TableSlice, the fields rows of Table and
when the type is converted to another type leading to align-
                                                                      one of TableSlice point to different memory addresses (line
ment violation. The alignment of a type specifies the valid
                                                                      26 and line 28), leading to inconsistent lengths of rows (line
memory address at which the type should be stored. Given
                                                                      27 and line 29). It could impact applications that rely on the
the alignment value as n, the type must be stored only at the
                                                                      value (e.g., rows.length). For example, when applications
address of a multiple of n. Some types have a fixed alignment
                                                                      plan to print all the data stored in table format to the termi-
regardless of the target architectures, while others could be
                                                                      nal, the API (TableSlice::print_tty) converts Table to
platform-specific. For example, the type of i32 has both 4-
                                                                      TableSlice first and iterates the data stored in rows. Since
byte alignments on the 32-bit or 64-bit target. In contrast, the
                                                                      iterating slice relies on the length (line 29) while the number
types of usize and isize are aligned to 4 bytes on the 32-bit
                                                                      of elements is actually only one (line 27), printing table leads
target and 8 bytes on the 64-bit target. The alignment require-
                                                                      to invalid memory access and segmentation fault, which has
ment can be easily violated with pointer-type conversion since
                                                                      been reported in RUSTSEC-2022-0074.
two pointers remain in the same memory address. Although
the memory address is aligned for src_ty, it might not be             Type III: Mismatched Scope Bug. The third type of bug
aligned for dst_ty if not handled carefully. In the Listing 2,        occurs when we break the invariant by creating an invalid
the method fill_bytes allows the slice of u8 to be cast onto          bit pattern or modifying the mutability of types. In List-
the slice of u32 (line 9). Since u8 is aligned to 1 byte, the slice   ing 4, the trait ComponentBytes is designed to provide a
of dest can be stored at the arbitrary memory address. When           method as_bytes_mut to modify the type T as byte slice.
it turns out to be accessed as u32, it is not guaranteed that the     The type T could be any type that implements the traits
memory address can be multiple of 4 since u32 is aligned to           Copy, Send, Sync, and lifetime bound static. However,
 1   pub struct Table {                                               1   pub trait ComponentBytes <T: Copy+Send+Sync+’static>
 2     format : Box< TableFormat >,                                   2     where Self: ComponentSlice <T > {
 3     titles : Box<Option<Row >>,                                    3     fn as_bytes_mut (&mut self) -> &mut [ u8 ] {
 4     rows : Vec<Row >,                                              4       let slice = self. as_mut_slice () ;
 5   }                                                                5       unsafe {
 6                                                                    6         slice :: from_raw_parts_mut (
 7   pub struct TableSlice <’a > {                                    7           slice . as_mut_ptr () as *mut _ , ..)
 8     format : &’a TableFormat ,                                     8       }
 9     titles : &’a Option<Row >,                                     9     }
10     rows : &’a [ Row ],                                           10   }
11   }                                                               11
12                                                                   12   impl<T > ComponentSlice <T > for [RGB <T >] { .. }
13   impl<’a > AsRef < TableSlice <’a >> for Table                   13
14   fn as_ref (&self) -> & TableSlice <’a > {                       14   impl<T > RGB <T > {
15     unsafe {                                                      15     pub const fn new (r: T , g: T , b: T) -> Self {
16       let s = &mut *(                                             16       Self {b , g , r}
17          (self as *const Table ) as *mut Table                    17     }
18       );                                                          18   }
19       s. rows . shrink_to_fit () ;                                19
20                                                                   20   // exploit for type III bug
             &*(self as *const Table as *const TableSlice <’a >)     21   let component : &’static str = " Hello , World !";
21       }                                                           22   let new_rgb = RGB :: new ( component , .. , ..) ;
22   }                                                               23   let mut rgb_arr = [ new_rgb ; 3];
23                                                                   24   let bytes = rgb_arr . as_bytes_mut () ;
24   // From GDB results                                             25   bytes [0] += component . len () as u8 ;
25   // $8 as & Table , $7     as & TableSlice                       26   // now , we can modify static memory
26   p & $8 . rows        //   0 x7ff ..82 f0                        27   println !( " {} " , rgb_arr [0]) ;
27   p & $8 . rows . len  //   1
28   p & $7 . rows        //   0 x7ff ..82 e0                        Listing 4: A mismatched scope bug in rgb that allows
29   p $7 . rows . length //   93825009397280!
                                                                     viewing and modifying data of any type wrapped in
Listing 3: An inconsistent layout bug in prettytable-rs              ComponentSlice<T> as bytes (RUSTSEC-2020-0029 [55]).
that casts a &Vec to &[T] (RUSTSEC-2022-0074 [56]).


                                                                     3.2     Challenges and Insights
                                                                     The Rust type system’s features, such as ownership, trait
                                                                     bounds, and generic types, present challenges that cannot
the trait and lifetime bounds here cannot prevent the issues         be directly addressed using existing methods in C and C++.
caused by the problematic type conversion implemented                We use the example of the mismatched scope bug to illustrate
in as_bytes_mut. It allows casting between mutable raw               the three challenges.
pointers (slice.as_mut_ptr() as *mut u8) to create an
invalid state for types since two pointers are pointing to over-     Interprocedural Type Conversion. In Listing 4, T YPE -
lapping memory. Safe Rust enforces aliasing rules, where             P ULSE identifies that the as_bytes_mut function performs a
mutable and immutable references can not exist simultane-            risky type conversion from a generic type to u8 on line 7, po-
ously, while unsafe Rust allows the rule to be bypassed, as          tentially leading to a type confusion bug. To confirm the pres-
shown in the exploit (line 21 - 27). The attacker creates an         ence of this bug, T YPE P ULSE must determine if the type is
immutable reference pointing to the static string as the type T.     converted between functions. Line 3 indicates that type self
With as_bytes_mut, the mutable raw pointer to the slice of           is initialized by a constructor function then passed to the cur-
string casts to the mutable raw pointer of u8 type. Since the        rent function. However, finding the constructor is a challeng-
function returns a mutable reference to a slice of u8, the at-       ing problem that traditional call graphs cannot address. For
tacker is allowed to modify any values in the slice of u8. How-      instance, the type of [RGB<T>] implements ComponentSlice
ever, the mutable reference bytes and immutable reference            (refer to line 12) but must be initialized via the new function
component point to the same data, breaking the aliasing rules        shown on line 15. Traditional call graphs can locate callers
of safe Rust. While the attacker modifies the value in bytes,        of as_bytes_mut, but the type constructor is not typically a
he also changes the value of component, which should not be          direct caller (see lines 22 and 24). To address this issue, we
mutated originally. One security consequence of modifying            identify the constructor by matching converted types to the
immutable data is data races. In a multi-threaded environment,       return types of external functions via a new data structure
if the immutable object can be modified through a mutable ref-       called Property Graph.
erence while other threads are reading it, the outcome could be      Generic Type Resolution. To predict the concrete types that
unpredicted or even lead to a program crash. In addition, appli-     can initialize generic type T, we first analyze trait bounds.
cations usually rely on the static variable for security checks or   The generic type T is constrained by four trait bounds:
maintaining a global state, which means that mutating the im-        Copy, Send, Sync, and ’static. Suppose we only enumer-
mutable data can also help attackers bypass security checks.         ate the types directly involved in these trait bounds; we only
get some internal types, such as RGB<ComponentType> and                           Peoperty Graph Constructor              Bug Detector
BGR<ComponentType>. Since ComponentBytes is a public                                                           Type Conversion   Invalid
trait, the user can initialize it with external user-defined types,               Pointer Alias
                                                                                    Analysis
                                                                                                                    Check            Access Check
such as str for the generic type (line 21). To address such an                                                   Misalignment
                                                                                                   Property                       Accessed
                                                                                                    Graph        Inconsistent
issue, we extend type conversion analysis to resolve the trait         Crate                                        Layout            Developer-         Bug
                                                                                 Type Conversion                                                        Report
bounds. First, if these traits are also bounded by other traits,                     Analysis                    Mismatched          Enfored Check
                                                                                                                    Scope                      No Check
we need to parse the dependencies recursively. Second, if the
function is public, we must consider all the primitive types
and composite types that external users could initialize. There-                     Fig. 1: An overview of T YPE P ULSE.
fore, we collect traits and primitive types defined in standard
libraries. For the composite types, we build the struct type
from primitive fields. Finally, bug detector can leverage the         4        T YPE P ULSE
trait bounds to generate a type set. The type set includes all
possible types that may be implicitly implemented and satisfy         To facilitate the detection of type confusion bugs, we design
the trait bounds.                                                     and implement a static analysis tool called T YPE P ULSE. This
                                                                      tool consists of two main components: Property Graph Con-
Alias Analysis. To verify the existence of the bug, it is crucial     structor and Bug Detector (see Figure 1). Given the Rust
for us to determine whether the pointer alias remains valid af-       code, property graph constructor first utilizes the compiler to
ter the type conversion (whether we can access rgb_arr after          translate the source code into the MIR. It then performs type
line 24). The pointer type conversion on line 7 is translated to      conversion analysis and pointer alias analysis to construct
_8 = move _9 as *mut u8 (PtrToPtr) in the Mid-level                   property graph. The property graph includes the type conver-
Intermediate Representation (MIR [6]) of the Rust compiler.           sion pairs and the pointer alias graph. Besides, trait bounds
move represents the transfer of ownership of a value to               are provided to bug detector for generic type resolution. Given
another, which means _9 is not accessible anymore. However,           the type conversion pairs, bug detector first performs the type
the previous alias of _9 still point to the same memory               conversion check with three different patterns to capture the
address. Therefore, slice on line 4 is still accessible after the     invalid type pointer, Then, the access check is run to deter-
ownership of its mutable pointer (_9) is transferred, leading         mine whether the invalid type pointer can be accessed through
to mismatched scope bug when accessing rgb_arr[0] (line               the alias graph. Finally, bug detector verifies if there are any
27). To precisely identify the alias relationship between             developer-enforced checks implemented to handle the invalid
the pointers, we analyze whether the pointer’s ownership              type pointer. If no, T YPE P ULSE produces a bug report with
is transferred based on different forms of instruction in the         the problematic type conversion highlighted.
Rust program. In the Listing 4, pointer alias analysis helps
us verify that the parameter (&mut self) points to the same           4.1       Property Graph Constructor
memory location as the u8 pointer (&mut [u8]), and whether
the parameter remains accessible after returning.                     The goal of property graph constructor is to collect the re-
                                                                      quired information and then integrate them into the property
                                                                      graph, which can accelerate the interprocedural analysis of
                                                                      bug detector. In addition to the results of type conversion
                                                                      analysis (§4.1.1) and pointer alias analysis (§4.1.2), each func-
                                                                      tion is associated with its return types, assisting in finding
3.3    Detection Scope                                                the type constructor functions. For example, given a func-
                                                                      tion new_as_slice, it calls the type constructor function new
                                                                      and passes the constructed type to the function as_slice as
We target the type confusion bug arising from the pointer type        src_ty. To obtain new function, we match src_ty with the
conversions and specify the type conversion behavior to be            return types of other functions in our property graph, which
implemented with as and transmute operations, represent-              could find all potential type constructors. After that, we can
ing the most fundamental ways to conduct type conversion              further analyze the type conversion across the functions. In
in Rust. In particular, T YPE P ULSE focuses on the three most        addition to return types, the function including unsafe code
prevalent bug types mentioned in §3.1. We do not consider the         will be marked for analysis in bug detector.
type conversion performed on non-pointer types, so the bugs
such as integer overflow [57, 58] arising from downcast are
                                                                      4.1.1      Type Conversion Analysis
excluded. Errors arising from foreign function interfaces [3]
are also out of scope, as addressing them would require de-           The type conversion analysis has three steps, namely, analyz-
veloping a system that is compatible with other programming           ing if type conversion includes any generic type, determining
languages’ compilers.                                                 if generic type is converted across functions, and resolving
Algorithm 1 get_trait_bounds()                                       types implementing these traits (trait_map), we utilize them
Input : f n, trait_map, visible                                      as the endpoint of the traversal, effectively tackling the issue
Output :trait_bounds                                                 of implicit dependencies. For each trait bound, property graph
trait_bounds ← HashSet::new();
foreach trait_bnd ∈ f n.get_bnd_by_sig() do
                                                                     constructor first checks whether the trait is defined in the trait
     if trait_bnd ∈ trait_map then                                   set. If not defined, property graph constructor then checks
           trait_bounds.insert(trait_bnd);                           whether the trait has dependencies (has_supertraits()).
     end
     else
                                                                     The output of this step also generates the type conversion pairs
           if trait_bnd.has_supertraits()&&visible then              including generic type and associated with the trait bounds.
                 // call get_trait_bounds() on supertraits again
           end
           else
                                                                     4.1.2   Pointer Alias Analysis
                 trait_bounds.insert(trait_bnd);
           end                                                       Pointer alias analysis is used to construct an alias graph, which
     end                                                             helps us determine the relation between pointers and how
end                                                                  the pointer can be accessed (see algorithm 2). The analy-
return trait_bounds;                                                 sis is performed in MIR for semantic information [6], e.g.,
                                                                     whether a value is moved or borrowed and if the value is dead.
                                                                     The nodes in the alias graph are collected from the Local in
the dependencies to collect the trait bounds on generic types.       the MIR, which refers to the "variables and temporary val-
In the first step, property graph constructor directly keeps the     ues in the scope of function" [51]. The edges between the
concrete type pair if no generic type is included. It starts with    nodes are updated when the MIR statement is in the forms of
visiting the MIR’s statements [52] and finding the ones of           StorageDead and Assign form, where Rvalue is assigned
type conversion. Rust’s MIR is a simplified version of the           to Lvalue. Based on the kinds of Rvalue appearing in the
Abstract Syntax Tree (AST) used for optimization. It con-            statement of Assign, pointers have different alias relation-
sists of statements and terminators [53]. Statements represent       ships.
intermediate operations such as assignments and variable ini-
tialization, and terminators define control flow decisions such                   a = Ref(b)
as conditions or function calls. In the statement of type con-                      = RawPtr(b)
version (src_ty, dst_ty), if both src_ty and dst_ty are                                                                            (1)
                                                                                    = Cast::(PtrToPtr, Operand(b))
the concrete types, property graph constructor will keep the
type pair directly. If one of the (src_ty, dst_ty) is a generic                     = Cast::(Transmute, Operand(b))
type, property graph constructor will move on to the second              In Equation 1, when the kind of Rvalue is Ref or RawPtr,
step, which is visibility analysis.                                  which means a new reference or raw pointer a is created and
Visibility Analysis. The visibility of a function decides how        points to the same memory location as b. If the kind of Rvalue
external users can call the function. In Rust, functions and         is Cast, especially on the pointers, a also points to the same
methods are both blocks of reusable code. The difference             location as b. In our alias graph, we will create the edge from
between a function and a method is that the method is as-            a to b to represent the alias relationship, where they are both
sociated with a particular type or defined within a trait. It is     local. However, we disconnect the edge from a to b when
typically called using the "." operator on the type instance. If     the kind of Operand in Cast is Move. The operand of Move
the generic type conversion occurs in the method, we should          means that the ownership of b is transferred to a, and b will no
determine whether the associated types can only be initialized       longer be accessible, so we disconnect the edge. In addition
by type constructor functions. In such cases, we analyze the         to the statement in the Assign form, we also disconnect the
visibility of all associated types and recursively traverse the      edge in the form of StorageDead. Given StorageDead(a),
types fields if it is a struct type. The visibility result repre-    it is used to mark that the ownership of a is transferred and all
sents if the type can be initialized by external users or limited    pointers of a become invalid. Therefore, we delete all edges
by constructor functions. If visible, trait bound analysis will be   created from a in our alias graph.
conducted to collect the type constraints for the generic type.
                                                                                  a = Call(Fn, args<Operand(b)>, ..)               (2)
Trait Bound Analysis. We collect a set of traits from stan-
dard libraries, which are implemented by all primitive types in         Equation 2 presents a function call in MIR, where args
Rust, indicating the potential concrete types to replace generic     works as a list of arguments that are passed to the function
types (see algorithm 1). We also extract certain traits from         and a holds the return value. For each argument in args, we
external libraries used to prevent type confusion bugs, helping      create the edge from a to b, but disconnect the edge if the
to reduce false alarms in bug detection. For example, the trait      operand on the argument is Move. In bug detector, the con-
plain [40] is always used to ensure that the memory layout           nection of a and b in the alias graph is leveraged to perform
is stable and initialized. As we have confirmed the specific         interprocedural alias analysis. , the alias_graph is constructed
Algorithm 2 get_alias_graph()                                            4.2.1   Type Conversion Check
Input : f n
Output :alias_graph                                                      We categorize the type conversion (src_ty, dst_ty)into three
foreach st ∈ f n.statements do                                           possible scenarios: (Con → Con), (Con → Gen), and (Gen
     if st ∈ Assign then                                                 → Con). The conversion between (Gen → Gen) is excluded
           (lval, rval) ← (st.lvalue(), st.rvalue());
           op ← rval.get_operand();                                      since we observe that such a conversion would be rejected by
           kind ← st.rvalue().kind();                                    the TypeId check [13]. The check strictly requires two types
           if kind ∈ Re f |RawPtr|Cast :: PtrToPtr|Transmute then        sharing the same layout. When generic type conversion errors
                 // insert rval.id() to alias_graph[lval.id()]
                 if op == Move then                                      are identified, the trait bounds linked to the generic type are
                       // delete rval.id() from alias_graph[lval.id()]   mapped to the ty_set, which has been verified to implement
                 end                                                     these traits in property graph constructor. The detection logic
           end                                                           for each bug type and each scenario is shown in Table 2.
     end
     else if st ∈ StorageDead then                                       Misalignment Detector (Type I). Misalignment detector can
           rval ← st.rvalue();                                           easily compute the alignments to identify the bugs; however,
           // delete all elements from alias_graph[rval.id()]
     end                                                                 it is not possible to predict the alignment of generic types that
end                                                                      depend on runtime input. To solve the challenge, we will use
foreach tm ∈ f n.terminators do                                          ty_set to simulate the input to generic types.
     kind ← tm.kind();                                                   Bug Definition. When src_ty’s alignment is not a multiple of
     if kind == Call(func, args, dest) then
           foreach arg ∈ args do                                         dst_ty’s alignment, it will create a misaligned pointer.
                 // insert arg.id() to alias_graph[dest.id()];           Type Conversion. In the scenario of (Con → Con), mis-
                 op ← arg.get_operand();                                 alignment detector directly locates the type conversion by
                 if op == Move then
                       // delete arg.id() from alias_graph[dest.id()]    computing the violation of alignment requirements (i.e.,
                 end                                                     src_ty.align % dst_ty.align != 0), and then we
           end                                                           will mark the dst_ty’s pointer as an invalid type pointer. In
     end                                                                 the scenario of (Con → Gen), we need to traverse all candi-
end
return alias_graph
                                                                         date types in ty_set to ensure each type obeys the alignment
                                                                         requirements. If any candidate type violates the requirement,
                                                                         we mark it as an invalid pointer. When ty_set is empty, it
                                                                         means that the generic type can be initialized with arbitrary
as a directed graph where the edge always starts from the                types since no trait bounds are found. In this case, we will
local in lvalue to the one in rvalue. inal When identify-                also mark dst_ty’s pointer as an invalid pointer. In the scenario
ing pointer aliasing, we will check whether two nodes have               of (Gen → Con), the detector follows the same logic as in
common descendents in alias_graph. Finding the common                    (Con → Gen) to mark the invalid pointer. The difference is
descendent represents that one alias of the src_ty’s pointer is          that dst_ty can not be aligned to only one byte even when the
aliased with the dst_ty’s pointer, then bug detector will col-           ty_set is empty. The reason is that any memory address can
lect all descendants while traversing the graph with breadth-            be a multiple of one where the misaligned pointer will not be
first search [66] from two nodes, then find whether there is an          created. In some cases, misalignment detector may fail since
intersection between two sets of descendants.                            the types are imported from external packages. To solve the
                                                                         challenge, we heuristically extract the information from the
                                                                         symbol names of types based on the cases we have studied
4.2     Bug Detector                                                     (e.g., extract u8 from external::u8_bytes). Since we only
                                                                         run our tool on the machine of 64-bit architecture; however,
Bug detector focuses on the marked functions in property                 some type’s alignment is platform-specific, where the value
graph (with unsafe), capturing type confusion bugs in three              changes based on different architectures. Take usize and
steps. First, given the pairs of type sets generated by type con-        isize for example, on a 32-bit target, they are aligned to 4
version analysis, type conversion check is performed to find             bytes while on a 64-bit target, they are aligned to 8 bytes. In
the invalid type pointer following three kinds of bug patterns.          Misalignment Detector, we will consider different alignment
Second, access check is used to find the alias of the invalid            values for these types in the type conversion.
type pointer based on pointer alias analysis. Based on the alias         Inconsistent Layout Detector (Type II). To detect the incon-
graph, it checks if the pointer is accessed in the function or           sistent layout bug, we define two type sets: unstable_ty and
accessible to the caller function. Third, verifying the absence          stable_ty. unstable_ty represents the type that can change the
of developer-enforced check helps reduce the false alarms                memory layout at runtime (e.g., struct, union, trait object),
of bugs. All three steps are combined with interprocedural               where the compiler preserves the rights to insert padding bytes
analysis based on property graph.                                        or reorder the fields. Another type set stable_ty consists of
                                                              Table 2: Type conversion checks.
 Bug Type      Con → Con‡                                       Con → Gen                                        Gen → Con

                                                                Input: src_ty, ty_set                            Input: dst_ty, ty_set
                                                                If ty_set.is_empty()                             If ty_set.is_empty() & dst_ty.align != 1
               Input: src_ty, dst_ty
                                                                      mark                                             mark
   Type I      If src_ty.align % dst_ty.align != 0
                                                                Else                                             Else If ty_set.not_empty()
                     mark
                                                                      replace dst_ty with each in ty_set               replace src_ty with each in ty_set
                                                                      run again in (Con → Con)                         run again in (Con → Con)
                                                                Input: src_ty, ty_set                            Input: dst_ty, ty_set
                                                                If ty_set.is_empty()                             If ty_set.is_empty()
               Input: src_ty, dst_ty
                                                                      If src_ty → unstable_ty                          If dst_ty → (stable_ty | unstable_ty’)
               If src_ty → unstable_ty
  Type II                                                                   mark                                            mark
                     If dst_ty → (stable_ty | unstable_ty’)
                                                                Else                                             Else
                          mark
                                                                      replace dst_ty with each in ty_set               replace src_ty with each in ty_set
                                                                      run again in (Con → Con)                         run again in (Con → Con)
                                                                Input: src_ty, ty_set                            Input: dst_ty, ty_set
                                                                If ty_set.is_empty()                             If ty_set.is_empty()
                                                                      If src_ty → weak_ty                              If dst_ty → strict_ty
               Input: src_ty, dst_ty
                                                                            mark                                             mark
               if src_ty → weak_ty
                                                                Else If src_ty → strict_ty && mut dst_ty               Else If dst_ty → weak_ty && mut dst_ty
                     If dst_ty → strict_ty
                                                                            mark                                             mark
  Type III                mark
                                                                Else                                             Else
               Else If src_ty → strict_ty
                                                                      replace dst_ty with each in ty_set               replace src_ty with each in ty_set
                     If dst_ty → mut weak_ty
                                                                      If (s,d)⋆ → (weak_ty, strict_ty)                 If (s,d) → (weak_ty, strict_ty)
                          mark
                                                                            mark                                             mark
                                                                      Else If (s,d) → (strict_ty, mut weak_ty)         Else If (s,d) → (strict_ty, mut weak_ty)
                                                                            mark                                             mark
   ‡ Con: concrete type; Gen: generic type; ⋆ (s,d): (src_ty, dst_ty).




scalar types (e.g., bool, char, integers). Inconsistent Layout                        has a weak constraint on its bit pattern, such as integer and
Detector will perform further analysis on the representation                          float type. In contrast, strict_ty means a strong limitation on
of types (e.g., repr(Rust), repr(transparent), repr(C)).                              the bit pattern, such as bool, string, and character. If the type
Any type conversion in unstable_ty set or across unstable_ty                          is found to be a composite type, which has multiple fields,
and stable_ty sets would be recognized as a problematic type                          mismatched scope detector will analyze each field and define
conversion and create an invalid type pointer. In addition, we                        it as strict_ty if one of the fields is included in strict_ty. The
need to combine with ty_set to extend the scenarios of generic                        type conversion between weak_ty and strict_ty can create a
type conversion.                                                                      type with an invalid bit pattern.
Bug Definition. When the layout of src_ty is not stable and
inconsistent to dst_ty, it will create an invalid type pointer.
                                                                                      Bug Definition. There are two patterns of conversion that can
Type Conversion. If the detector finds the conversion happens
                                                                                      create an invalid type: 1) src_ty belongs to weak_ty while
in (unstable_ty → stable_ty), it will mark the dst_ty’s pointer
                                                                                      dst_ty belongs to strict_ty. 2) src_ty and dst_ty are in strict_ty
as an invalid type pointer since the padding bytes can be
                                                                                      and weak_ty, while dst_ty’s pointer is mutable. In these two
exposed when we accessed them as a scalar type. The second
                                                                                      types of conversions, an invalid type pointer can be created.
pattern is (unstable_ty → unstable_ty), inconsistent layout
detector will further check if they follow the same Application
Binary Interface (ABI) [2], which determines if src_ty and
                                                                                      Type Conversion. If the detector finds the conversion in
dst_ty share same layout based on their symbol name of type.
                                                                                      (weak_ty → strict_ty), it will mark the dst_ty’s pointer as an
If they have different type symbol names, dst_ty’s pointer will
                                                                                      invalid type pointer since the bit pattern of src_ty could be in-
also be marked as an invalid type pointer. In the scenarios of
                                                                                      valid for dst_ty. When the conversion is found in (strict_ty →
(Con → Gen) and (Gen → Con), they follow the same logic
                                                                                      weak_ty), mismatched scope detector will take a further anal-
to check when the arbitrary types or the limited types in ty_set
                                                                                      ysis on whether the dst_ty is mutable since changing the bit
could make the type conversion match the two patterns above.
                                                                                      pattern of dst_ty can also make src_ty invalid. In the scenarios
Mismatched Scope Detector (Type III). In order to find the                            of (Con → Gen) and (Gen → Con), the detector follows the
bug efficiently, we define two type sets based on the scope of                        same logic to check whether the type conversion is performed
values: weak_ty and strict_ty. weak_ty represents the type that                       between weak_ty and strict_ty with mutability analysis.
4.2.2   Access Check                                                 check if the size of the struct type is 8 bytes, further ensuring
                                                                     that no padding bytes are inserted. The post type checks such
Access check is performed to analyze how the invalid type
                                                                     as ptr::write, which can be used to access the uninitialized
pointer captured by Type conversion check can be accessed.
                                                                     memory, will also be detected before T YPE P ULSE raises the
The analysis can be separated into two steps: 1) check whether
                                                                     alarms for the bugs. Detecting developer-enforced checks for
the pointer is accessed in the function, and 2) analyze whether
                                                                     scope mismatch bugs is challenging because developers often
the pointer is accessible for the caller function. As the first
                                                                     use runtime value comparisons.
step, to check whether dst_ty’s pointer is accessed in the func-
tion, we focus on the dereference in statements and the un-
safe function calls in the terminators of the MIR. For state-        4.2.4   Integration of Interprocedural Analysis
ments, we check whether dst_ty’s pointer is aliased with the
                                                                     Interprocedural analysis plays an essential role in confirming
dereferenced pointer. For unsafe function calls, we collect
                                                                     the presence of the type confusion bug. In this section, we
a list of unsafe functions that are widely used in the core li-
                                                                     describe how it is incorporated into bug detector.
braries of Rust, such as ptr::read/copy, ptr::as_ref, and
slice::from_raw_parts, which requires the pointer refers             Type Conversion Check. We can use it to identify type con-
to an aligned, consecutively initialized type. The access list for   versions between functions. For instance, consider (Con →
mismatched scope detector also includes other APIs such as           Con), where we notice an unsafe type casting from a u8
str::from_utf8_unchecked or CStr::from_ptr. These                    pointer to a u16. According to our misalignment bug criteria,
functions require types to be encoded with the specific bit          this should trigger an alert. Nevertheless, through interpro-
patterns. Access check will verify whether the pointer passed        cedural analysis, we identify a type conversion from a u16
in these unsafe functions is aliased with the dst_ty’s pointer.      pointer back to u8 in the caller function. As a result, the
   In the second step, to check whether dst_ty’s pointer is          src_ty should be u16 and properly aligned to two bytes,
accessible for the caller function, we analyze whether the           which means that there is no any misalignment. Considering
dst_ty’s is aliased with the return type only when the return        another case with generic type (Gen → Con) and type conver-
type is a reference. When the return type is a raw pointer,          sion being detected in a method, we leverage property graph
accessing it requires the unsafe block since Rust does not           to identify the type constructor function and analyze the type
guarantee the safety of the raw pointer. Since using unsafe          conversion pairs in the method.
highlights the responsibility for the bugs and we only consider      Access Check. Given that the type may not be accessible
the function that performs the problematic type conversion           within the current function, we also examine the callee func-
to be the culprit of bugs, we will set up the requirement for        tions, such as a raw pointer dereference. Additionally, we
the return type to be a reference in the second step. After          gather certain unsafe standard library functions, which in-
access check ensures that the pointer of invalid dst_ty can be       volve type access, accelerating the verification of type access.
accessed, the bug report will be generated as the output of
                                                                     Developer-Enforced Check Analysis. Developer-Enforced
bug detector.
                                                                     Check could also exist in external functions. In other words,
                                                                     it can be implemented in callers, type constructors, or callees.
4.2.3   Developer-Enforced Check Analysis                            Thus, T YPE P ULSE must analyze all reachable functions to
Developer-Enforced Check is usually used by the developers           locate the related type checks.
to prevent type confusion bugs manually. Through examining
these checks, we can confirm that the developer has handled          4.3     Implementation
the type conversion errors, further reducing the false alarms
of T YPE P ULSE. We categorize them into two scenarios: Pre          T YPE P ULSE is developed with 5249 lines of code in Rust,
Type Check and Post Type Check, where the check inserted             utilizing rustc and fully integrating with Cargo, Rust’s offi-
before and after type conversions, respectively.                     cial package manager. T YPE P ULSE focuses on target files
   We summarize various patterns of developer-enforced               that can be compiled into an executable or a library [48].
checks that address type confusion bugs individually. First,         Using Cargo, we address dependency issues prior to com-
the pre type checks used to prevent misalignment bugs include        pilation and identify all targets in the package suitable for
calling align_of and alloc, which are used to check and as-          analysis. Compilation of these target files is done through
sign memory layout before the type conversion. There is also         rustc. Upon completion, T YPE P ULSE is activated within the
a post type check that the developer uses to safely load the         after_analysis callback function of the rustc driver, which
misaligned type e.g., read_unaligned. Second, for the in-            is triggered by rustc following the generation of Rust com-
consistent layout bug, pre type check is used to guarantee the       piler’s MIR, allowing us to employ the resulting MIR data as
memory is completely initialized. The typical patterns include       input for property graph constructor to start the analysis.
using size_of to restrict the size at run-time. For example,            The workflow of T YPE P ULSE can be divided into two
if the struct contains two fields of u32 types, developers can       phases: 1) detecting if the type conversion generates a prob-
                                                                                                        1.0
Table 3: Bugs identified by T YPE P ULSE; note that we have
only listed the bugs that have been reported for over three
                                                                                                        0.8
months as of January 1, 2025.
 Package           Version       Stars   Bug Types‡ and Numbers              Status∗   Patched†
                                                                                                        0.6
 candle-core          0.4.1      13.2k   Con → Gen: I:3 (as)                              -




                                                                                                  CDF
 py-spy              0.3.14        11k   Con → Con: I:1 (as)                     #        -
                                         Con → Gen: I:1 (as)
 fyrox-core          0.27.0       7.1k                                                    ✓             0.4
                                         Gen → Con: II:4 (as), III:2 (as)
 gfx-backend-gl       0.9.0       5.2k   Con → Gen: I:1 (as)                              -
 silicon              0.5.2       3.1k   Con → Con: II:1 (as)                    #        -
                                                                                                        0.2
 webrender           0.61.0         3k   Con → Con: I:2 (as)                              -
 spl-token-swap       3.0.0       2.3k   Con → Gen: I:1 (as), III:1 (as)                  -
 scryer-prolog        0.9.4       1.9k   Con → Con: I:6 (transmute)                       -
                                                                                                        0.0
 libafl              0.10.1       1.6k   Con → Con: I:3 (as), III:4 (as)                  ✓
 mesalink             1.1.0       1.5k   Gen → Con: II:1 (as)                    #        -                   0      20       40              60              80   100   120
                                                                                                                                   Execution Time (seconds)
 fontdue              0.8.0       1.2k   Gen → Con: I:1 (transmute)                       -
                                         Con → Con: II:1 (as)
 pprof               0.13.0        1k                                                     ✓
                                         Con → Gen: I:1 (as)
 rendy-core           0.5.1       814    Gen → Con: II:2 (as)                    #
                                                                                 G        -
 rendy-util           0.4.1       814    Gen → Con: II:2 (as)                    #
                                                                                 G        -
 sciter-rs           0.5.58       784    Gen → Con: I:1 (as)                              -
                                                                                                                  Fig. 2: Detection time of T YPE P ULSE.
 rosrust             0.9.11       728    Gen → Con: II:3 (as) III:1 (as)         #
                                                                                 G        -
 cortex-m             0.7.7       669    Gen → Con: II:1 (as)                             ✓
 rafx-base           0.0.15       574    Gen → Con: II:2 (as)                    #
                                                                                 G        -
 xous                0.9.50       500    Con → Gen: I:2 (as), III:2 (as)                  ✓       5.1         Bug Detection Results
    ∗ Bug status: #: Reported;    : Confirmed by Vendors; #G: Verified by PoC.
    † Patch status: ✓: already patched; -: unpatched.                                             First, we ran T YPE P ULSE on the RUSTSEC dataset of ex-
    ‡ Bug type: Con: concrete type; Gen: generic type; [I, II, III]: bug type.
                                                                                                  isting type confusion bugs as of September 1, 2024 (see Ta-
                                                                                                  ble 1). T YPE P ULSE is capable of detecting all existing type
                                                                                                  confusion bugs of three types. Second, we ran T YPE P ULSE
lematic dst_ty, and 2) checking if the problematic type is                                        with 16-thread to scan the 3,000 packages. It ran 18 hours
accessed. With pairs of type sets generated by type conver-                                       in total; the majority of time was spent on resolving depen-
sion analysis, we can find a problematic type conversion even                                     dencies and compilation. The detection time only took about
when a generic type is involved. With the alias graph built                                       80 mins and 94 bugs were reported. For the 3,000 packages,
by pointer alias analysis, we can track how the pointer can                                       618 (20.6%) failed due to compiler version, 37 (1.2%) did
be accessed. The type conversion pairs and alias graph are                                        not have proper cargo metadata, and 309 (10.3%) failed with
stored in property graph, which accelerates the interprocedu-                                     custom build options, which cannot be resolved automatically
ral analysis to obtain the information of external functions.                                     and required manual work. All the remaining 2,036 pack-
For interprocedural analysis, we introduced a depth limitation                                    ages (67.9%) could successfully compile within 20 minutes.
to avoid the path explosion problem. We set the path length                                       Among them, 282 did not have /bin or /lib targets for de-
to 1 (tracing only the immediate caller or callee function),                                      tection, so TypePulse did not execute on them. For 1,754
aligning with that in Rupta [31].                                                                 packages that TypePulse ran detection on, the average detec-
                                                                                                  tion time was 1.71s. Among the 1,754 packages, 1,483 were
                                                                                                  completed within 1s; 1,652 were completed within 5s; only
5      Evaluation                                                                                 59 needed more than 10s to complete; 5 packages did not
                                                                                                  finish execution within 2 minutes. The CDF figure of the de-
Dataset Collection. We gathered packages from crates.io,                                          tection time is shown in Figure 2. We manually verified these
the Rust community’s crate registry. To ensure comprehensive                                      bug reports and confirmed that 71 of them were true positive,
bug detection, The dataset consists of the packages ranked                                        indicating an overall precision of 75.5%. The information on
by download counts and the number of GitHub stars (as of                                          packages and bugs that have either been confirmed or reported
September 1, 2024), and each of them has more than 500 stars.                                     for over three months is provided in Table 3. Many bugs we
Regarding package size, the largest package contains 510k                                         detected are not trivial. Among the 71 type confusion bugs
LoC, with an average package size of 9k LoC.                                                      detected by T YPE P ULSE, there are 50 bugs found in packages
Experiment Setup. We built T YPE P ULSE and conducted                                             with more than 1,000 stars on GitHub. These packages are
experiments on a server with 48-core Intel Xeon CPU ES-                                           well known in the Rust community and are usually maintained
2630 and 256 GB memory. The server was deployed with                                              well by professional teams. For example, candle-core [25]
Ubuntu 22.04 and rustc 1.72.0-nightly. For each package, we                                       is developed by a famous AI company (Hugging Face) [24].
set the preparation (dependencies resolution and compilation)                                     Therefore, our results suggest that even domain experts may
time threshold to 20 minutes and T YPE P ULSE detection time                                      write error-prone code in Rust.
threshold to 2 minutes. We ran T YPE P ULSE on the 3,000                                          Capability to Find New Bugs. To facilitate the resolution of
packages for detection.                                                                           these bugs, we also created a Proof of Concept (PoC) to report
  Table 4: The results of detectors on top 3,000 packages.          1 impl<const N: usize > String<N > {
                                                                    2   pub fn new () -> String<N > {
                                      Bug Types                     3     String { bytes : [0; N], len : 0 }
      Detector     Metrics                               Overall
                                 I        II      III               4   }
                      TP           32       24      15       71     5   pub fn to_str (&self) -> & str {
      TypePulse       FP            6        4      13       23     6     unsafe {
                                                                    7     str :: from_utf8_unchecked (&self. bytes [0..]) }
                   Precision   84.2%   85.7%    53.6%    75.5%
                                                                    8   }
                      TP           32       24      13       69     9   pub fn push (&mut self, ch : char ) -> Result<.. > {
      TypePulse
                      FP           11        6      13       30    10     match ch . len_utf8 () {
      w/o IPA                                                      11
                   Precision   74.4%     80%      50%    69.7%              1 => { ... }
                                                                   12       _ => {
       IPA: Interprocedural Analysis.                              13          let mut bytes : usize = 0;
                                                                   14          let mut data : [ u8 ; 4] = [0; 4];
                                                                   15          let subslice = ch . encode_utf8 (&mut data );
                                                                   16          // ...
identified issues to package maintainers, which requires locat-
ing undefined behaviors in packages based on the diagnostic        Listing 5: The false positive case of Mismatched Scope bug.
information produced by T YPE P ULSE. To trigger potential
bugs, we need to create the appropriate src_ty and dst_ty be-
fore invoking the problematic conversion. We consider two
                                                                   developer-enforced check in future work.
distinct scenarios. First, when the source and destination vari-
ables are openly accessible, such as through public members
within a class, we can directly create these variables. Second,    5.3    Impacts of Interprocedural Analysis
when the source and destination variables are private and not
directly accessible, a constructor is required to initialize the   We conduct an ablation study to demonstrate T YPE P ULSE’s
variables. Additionally, T YPE P ULSE helps find feasible con-     capabilities in reducing false positives by disabling interpro-
structor functions, which also accelerates the PoC generation.     cedural analysis (refer to the second row in Table 4). T YPE -
   At the time of writing, we have documented all the issues       P ULSE reduces 6 more false positives and detects 2 more true
(71) that we have manually confirmed, and 32 of these have re-     positives with interprocedural analysis enabled. Scanning
ceived acknowledgment responses from the package maintain-         3k packages, T YPE P ULSE obtains the results with precision
ers. After notifying the maintainers, we further reported these    75.5%, consisting of 71 True Positives and 23 False Positives.
issues to the RUSTSEC advisories and CVE database. So far,         After disabling the interprocedural analysis, T YPE P ULSE’s
we have received six RUSTSEC IDs and one CVE ID, and are           precision is reduced to only 69.7%, consisting of 69 True
awaiting confirmation and releases for the remaining ones.         Positives and 30 False Positives. This comparison result high-
                                                                   lights that interprocedural analysis can significantly enhance
5.2      False Positive Analysis                                   precision by analyzing the context across functions. First, it
                                                                   can detect the positive cases relying on external functions
According to Table 4, there are 23 instances of false posi-        to decide the bit patterns – 2 more mismatched scope bugs
tives. There are 2 arising from misidentifying function visibil-   were detected. Second, it can reduce the false alarms in cases
ities and 3 from developers’ tricks to prevent invalid pointer     with developer-enforced checks – 7 more False Positives were
exposure. Here we investigate the remaining 18 cases that          reduced. For example, in the package of arrow-buffer, dis-
arise from misinterpretation during the developer-enforced         abling interprocedural analysis will cause four more false
check analysis. It shows that T YPE P ULSE cannot understand       positive cases of misalignment bugs. The Listing 6 shows
complex condition semantics in checks, especially when the         a false positive case mitigated by interprocedural analysis.
check is implemented in an unusual way. Considering Listing        T YPE P ULSE first locates suspicious type conversion at line
5 for example, T YPE P ULSE considers the method to_str            20 since it finds that the pointer of buffer is cast to arbi-
could construct an illegal string from an array of u8, which       trary generic type. However, the generic type cannot be con-
might contain a non-utf8 character. After manually studying        trolled by attackers since as_slice is a method relying on
the type constructor function (new) and the method used to         BufferBuilder and casting MutableBuffer to generic type.
insert characters into the string (push), we find that the char-   The constructor function of MutableBuffer cannot be lo-
acters in the string are restricted to be utf8 by the encoding     cated by traditional interprocedural analysis because it is not
at line 15 (encode_utf8). This complex encoding makes it           the caller of the method. T YPE P ULSE implements the func-
difficult for T YPE P ULSE to avoid false alarms in detecting      tionality to find out the constructor functions by matching the
Mismatched Scope Bugs. So far, T YPE P ULSE can only de-           type to the ones returned from other functions. In this exam-
tect standard developer-enforced check patterns and several        ple, T YPE P ULSE locates the function with_capacity, which
unsafe APIs with clear safety documentation. It is challeng-       returns MutableBuffer as the constructor function. After an-
ing for T YPE P ULSE to understand such encoding operations.       alyzing the constructor function, T YPE P ULSE finds that the
We will extend the capability of T YPE P ULSE to interpret         constructor function already guarantees the alignment of type
 1   impl MutableBuffer {                                                   Table 5: Comparison with Clippy and Rudra.
 2     #[ inline ]
 3     pub fn with_capacity ( capacity : usize ) -> Self {                   Detector     Type I   Type II   Type III   Overall
 4       let layout = Layout ::
 5          from_size_align ( capacity , ALIGNMENT ). unwrap () ;
                                                                              Clippy       10        0         0          10
 6       let data = match layout . size () {                                  Rudra         0         0        0          0
 7          0 => dangling_ptr () ,                                         T YPE P ULSE    32        24        15         71
 8          _ => {
 9            let raw_ptr = unsafe {
10               std :: alloc :: alloc ( layout )
11            };
12        // ...                                                    Clippy’s limitation as follows. Firstly, Clippy fails to iden-
13       Self { data , len : 0, layout }                            tify potential bugs involving generic types, as the two lint
14   // ...
15   impl<T: ArrowNativeType > BufferBuilder <T > {                 checks are only carried out when both the source type and
16     #[ inline ]                                                  dest type are concrete. Secondly, Clippy does not have a
17     pub fn as_slice (&self) -> &[ T] {
18        // ...                                                    comprehensive approach to identifying type conversion er-
19       unsafe { std :: slice :: from_raw_parts (                  rors. It is observed that Clippy’s checks vary between as
20          self. buffer . as_ptr () as _ , self. len ) }
21   // ...                                                         and transmute; misalignment checks are applied to as but
                                                                    omitted for transmute. For inconsistent layout bugs, checks
Listing 6: The false positive case resolved by interprocedural      are conducted exclusively on transmute. Furthermore, upon
analysis.                                                           reviewing developer comments, it is observed that developers
                                                                    often disregard the warnings due to their belief that Clippy
                                                                    generates a significant number of false positive cases.
with Layout::from_size_align; therefore, this should be             Comparison with Rudra. Rudra [15] is the bug detector
a false alarm. Without interprocedural analysis, T YPE P ULSE       that can be used to capture memory safety bugs from Rust
cannot detect the developer-enforced check implemented in           packages. We compared T YPE P ULSE with Rudra for two
the constructor function.                                           reasons. First, Rudra is the state-of-the-art memory safety
                                                                    bug detector, reporting 51.6% of all memory safety bugs.
                                                                    Second, Rudra claims it can find the bugs of uninitialized
5.4     Comparison with Existing Tools
                                                                    memory exposure, which is the result of inconsistent layout
To the best of our knowledge, T YPE P ULSE is the first bug         bugs. Our evaluation results show that Rudra can find five
detection tool to systematically detect type confusion bugs         bugs of uninitialized memory. However, none of them occurs
in Rust, so we are unable to find similar tools to perform          in the type conversion process, which means it is not effective
an apple-to-apple comparison. We choose the tools that are          in detecting type confusion bugs. The main reason is that,
able to partially detect type confusion bugs for comparison:        for the patterns of type conversion, Rudra only detects the
Clippy [9] and Rudra [15]. We run them on the packages              terminators at the MIR level. Unfortunately, transmute has
listed in Table 3 and compare the results. The comparison           been translated to statements rather than terminators since
results are shown in Table 5. Additionally, we compare the          2021. Moreover, Rudra implements the dataflow checker of
performance of T YPE P ULSE to the Rust’s type system on            transmute but excludes as. As a result, Rudra is not able to
the existing type confusion bugs in RUSTSEC dataset (see            detect type confusion bugs effectively.
Table 1).                                                           Comparison with Rust Type System. We also conduct the
Comparison with Clippy. Clippy is a static analysis                 experiment to elaborate if the existing Rust type system can ef-
tool that implements more than 650 types of lints [67]              fectively detect type confusion bugs in unsafe code regions.
to detect common errors in the Rust program. Clippy                 We compare the positive cases of type confusion bugs de-
supports 2 types of lints to find the unsound usages of             tected by T YPE P ULSE and the Rust type system. Since Rust
as and transmute. First, it can check whether as can                considers unsafe keyword to be required for raw pointer
lead to a misaligned pointer (cast_ptr_alignment [1]).              dereferences and unsafe APIs, removing unsafe will intro-
Second, it can check whether transmute occurs between               duce syntax errors. For the purpose of calculating the pre-
types of different Application Binary Interfaces (ABIs)             cision, we count these unremovable unsafe as positive bug
(unsound_collection_transmute [2]). The version of                  detections by Rust type system. If there are multiple unsafe
Clippy with which we compare is 0.1.72, and Table 5 re-             blocks in a single function, we count it as one. In other words,
veals that Clippy identifies only 10 relevant bugs, all of which    the functions with unsafe but no type confusion bugs being
are misalignment issues (Type I) restricted to Con → Con            reported should be considered as false positive cases. We use
(21 bugs in total). Regarding the remaining 11 misalignment         all vulnerable files including the 32 existing bugs (Table 1) as
bugs, one warning is intentionally suppressed by develop-           the benchmark and find that both T YPE P ULSE and the type
ers, four arise from overlooking variations in ABIs, and six        system can detect all the existing type confusion bugs; how-
involve transmute. We summarize two main reasons for                ever, the type system produces 116 false positive cases while
                                                                    UnresolvedFrames is a representation of an event backtrace,
 1 impl<’a , T > Iterator for TempFdArrayIterator <’a , T > {
 2   type Item = &’a T;                                             and it is a self-defined struct type with fields of u64, usize,
 3   fn next (&mut self) -> Option<Self:: Item > {                  an array of u8. Since the file_vec is aligned to 1 byte, any
 4     // ...
 5     let length = self. file_vec . len () / size_of :: <T >() ;   type that has a larger alignment than 1 byte can lead to the
 6     let ts = unsafe {                                            misalignment bug and crash here.
 7       slice :: from_raw_parts (
 8          self. file_vec . as_ptr () as *const T ,                   Famous Rust-based applications like GreptimeDB [5] (4.1k
 9          length )                                                stars on GitHub) are affected by this bug. GreptimeDB, a time
10       };
11                                                                  series database storing logs, events, and CPU usage, crashes
12 pub fn build (&self) -> Result< Report > {                       when calling pprof (report::ReportBuilder::build) to
13     let mut hash_map = HashMap :: new () ;
14     match self. profiler . write () . as_mut () {                build reports. This panic can obstruct queries or data writes,
15       Err( err ) => {...}                                        causing real-time network monitoring applications to miss
16       Ok( profiler ) => {
17          profiler . data . try_iter () ?                         identifying high CPU usage, leading to network performance
18             . for_each (entry { .. }                             decline. For example, given a GreptimeDB-based public net-
                                                                    work server that provides the interface of event backtrace,
  Listing 7: Misaligned bug found in the pprof package.
                                                                    the attacker could initialize the data T with the type aligned
                                                                    to 2 bytes, causing the network server panic and rendering
                                                                    it unavailable to users. After reviewing related GitHub is-
T YPE P ULSE only produces 3.                                       sues, we traced the ReportBuilder::build code pattern
Summary. Our evaluation confirms that T YPE P ULSE is the           and searched on GitHub. Over 230 code files show similar
most effective tool to detect type confusion bugs in Rust. Ex-      patterns and may be affected.
isting state-of-the-art Rust bug detection tools such as Clippy
and Rudra are not as effective, since they are not designed
for detecting type confusion bugs. Our experiment also ex-          6   Discussion
plains that the current Rust type system is not sufficient to
check the unsafe type conversion, highlighting the necessity        Rust vs. C++ on Type Confusion Bugs. The distinction of
of T YPE P ULSE.                                                    compiler features, type systems, and memory management in
                                                                    Rust and C++ lead to different types of type confusion bugs
                                                                    and new challenges in detecting them. First, while pointer-
5.5    Impacts of Type Confusion Bugs
                                                                    type conversion is the primary cause of bugs in both lan-
Memory errors might occur due to type confusion bugs, es-           guages, the inconsistent layout bug and the mismatched scope
pecially if the target type allows access to memory that the        bug mentioned in this paper do not occur in C++. This is
source type cannot reach. The type confusion bugs discovered        because the C++ compiler does not rearrange the memory lay-
by T YPE P ULSE have different security implications. Among         out of composite types by default (thus no unstable_ty), and it
them, 28 trigger panics, 24 cause uninitialized memory ac-          also does not impose strict requirements on the bit-pattern as
cess, 8 lead to out-of-bounds access, 7 construct illegal types,    Rust does. From a different angle, type confusion bugs in C++,
and 4 can generate data race issues. Using case studies of the      which consistently occur when downcasting an object from
pprof package [7], a popular Rust-based CPU profiler with           a parent class to a child class, does not exist in Rust. This is
1.3k stars on Github and 159 crates.io dependents, we show          because Rust lacks the object characteristics needed for such
the impacts of bugs and how it helps diagnose Rust perfor-          issues. Rust introduces the concept of a trait object [45], com-
mance bottlenecks. The bug was reported and confirmed by            parable to C++ objects, to define shared behaviors. However,
the developers on Github. Besides, we also provide other case       since trait objects do not involve inheritance, they prevent
studies and corresponding PoCs in Appendix A.                       object-based type confusion bugs. Second, before resolving
Misalignment Bugs. As shown in Listing 7, T YPE P ULSE              generic types, extracting traits completely is more difficult in
detects a misalignment bug (line 8) in the next function            Rust since Rust’s traits can be implicitly bounded while C++’s
implemented on TempFdArrayIterator. When the unsafe                 concept must be explicit. Lastly, Rust’s implicit memory man-
slice::from_raw_parts is called (line 11), it assumes the           agement brings convenience to developers by avoiding man-
caller meets safety contracts. The raw pointer must be aligned,     ual management. However, it actually makes pointer alias
non-null, and point to length bytes of initialized values [11].     analysis harder. To verify whether the pointer is still valid, the
Violating these safety contracts causes a panic. One way            detector must ensure whether the memory is automatically
to invoke the next function is to build reports from a run-         dropped or the ownership is transferred.
ning profiler; it will iterate each entry to process the data       Complementing Rust type system. T YPE P ULSE is neces-
and write them into reports (line 12). The generic type T           sary since expanding the type system protection from Safe
in TempFdArrayIterator is decided by the item stored in             Rust to include unsafe is insufficient, as shown in §5.4. The
the profiler.data (line 17), which is UnresolvedFrames.             type system’s safety assurances are not derived from execut-
ing type checks. Rather, Safe Rust prevents the presence of an      be used in critical security scenarios.
invalid type right from the beginning. Consider the example of
a misaligned pointer: Safe Rust prevents developers from con-
verting a pointer to one aligned with larger byte sizes (refer to   7   Limitations and Future Work
Listing 1). Due to this stringent rule, the compiler confidently
                                                                    As detailed in §5.2, T YPE P ULSE has limitations in accurately
assumes that misaligned pointers are not present in Safe Rust.
                                                                    interpreting different implementations of developer-enforced
Consequently, optimizations and code generation within the
                                                                    checks, leading to false positive cases. Some check patterns
compiler’s backend are carried out based on this assumption.
                                                                    are inherently implicit and difficult to formalize. For example,
A pointer generated within unsafe is the only entity capable
                                                                    calling size check functions but actually examining padding
of circumventing these rules. Even if the pointer from unsafe
                                                                    bytes. Understanding this intricacy requires a deep contextual
is converted to a reference, the compiler will still treat this
                                                                    insights. Additionally, assessing the value within the check
reference as reliable. This flawed assumption can result in
                                                                    condition is particularly challenging when relying solely on
undefined behavior. Therefore, a tool like T YPE P ULSE that
                                                                    static tools. Without incorporating dynamic analysis, assuring
aids in identifying an invalid type becomes essential for Rust
                                                                    the accuracy of security checks becomes difficult, especially
developers.
                                                                    in large software projects. In future work, we aim to integrate
Mitigations of Type Confusion Bugs. We summarize com-               symbolic execution in access checks, such as implementing
mon ways to fix the bugs detected by T YPE P ULSE.                  constraints to confirm that a pointer’s memory address can-
Type I: misalignment bugs. Misaligned references are pro-           not be a multiple of the type size before T YPE P ULSE flags
hibited in safe code, but the safety of misaligned raw point-       misalignment issues. Furthermore, with a path limitation of
ers depends on access methods. We propose two strate-               1 for interprocedural analysis, TypePulse struggles to grasp
gies to prevent misalignment issues before dereferencing:           the context in extended call chains, which we aim to address
(1) use read_unaligned [8] or write_unaligned [14],                 in future work.
which handle misaligned pointers, or (2) create a new
aligned pointer. Most functions require aligned pointers;
read_unaligned creates an aligned duplicate by copying              8   Related Work
data (copy_nonoverlapping) and casting to u8. Alterna-
tively, developers can manually create a new pointer by adding      Research on type confusion bugs in C++/Javascript. In
an offset (ptr.add) to align the address.                           other programming languages, there are a large number of
Type II: inconsistent layout bugs. To avoid the inconsistent        existing works focusing on type confusion bugs. For instance,
layout bug, we need to ensure the type’s memory layout is           C++ supports implicit type conversion which can lead to
consistent and stable. If dst_ty is a primitive type with ini-      significant issues; thus, numerous scholars have developed
tialized memory in consecutive bytes, src_ty must not have          various methods to identify the type confusion bugs [18, 21,
uninitialized bytes. Although most code avoids inconsistent         26, 29]. Given that C++ includes diverse type casting abilities
type conversion, it can occur during generic type conversion.       and runtime polymorphism, detectors for such bugs must
To prevent bugs in generic types, we can apply trait bounds         integrate runtime analysis techniques while also managing
— list the types that can be legally converted and implement        performance overhead. To enhance performance, TypeSan
the trait on them. This ensures callers use only the defined        [21] developed a framework capable of efficiently monitoring
types as parameters. A well-known trait implementing this           memory allocation details. There are also several research
concept is bytemuck::Pod [49]. For struct-to-struct con-            works focusing on type confusion bugs in Javascript [16, 41,
versions, developers often wrongly assume stable memory             59]. Type-related issues in C++ are deemed more severe as
layout. To ensure stability, developers need to annotate types      they directly contribute to memory safety problems, whereas
for conversion with repr(C) or repr(transparent) [46].              Javascript typically operates within constrained settings like
Type III: mismatched scope bugs. Such bugs often oc-                web browsers. Although Rust is engineered with improved
cur in exposed APIs with generic type conversion. De-               type-safety compared to C++ and Javascript, our research
velopers should limit types and use trait bounds to re-             shows that type-related errors can still occur in Rust.
strict conversion and validate values before converting. Li-        Research on unsafe Rust. A substantial body of research ex-
braries provide unsafe APIs like from_*_unchecked (e.g.,            plores how the use of unsafe can compromise the integrity of
str::from_utf8_unchecked [61]) for type conversion,                 Rust programs [19,27,34,39,44,47,68,69]. Xu et al. analyzed
whose safety must be ensured by callers. Callers must validate      hundreds of memory-safety issues, determining that safety
that source type values are appropriate for destination types.      assurances can be violated by unsafe code [68], while other
For instance, str::from_utf8_unchecked requires UTF-                works study how to protect the Rust program [27, 47]. Addi-
8 valid input, unlike the safe std::from_utf8 [60], which           tionally, some scholars have investigated both memory-safety
checks this. Developers often use from_utf8_unchecked               and concurrency issues, assessing the effects of eliminating
over from_utf8 to avoid overhead, but safe functions should         unsafe code [44]. Rudra [15] and MirChecker [33] are specif-
ically designed to target functions that incorporate unsafe         RUSTSEC-2023-0047, RUSTSEC-2024-0408, RUSTSEC-
code and detect memory-safety issues. Observations from our         2024-0424, RUSTSEC-2024-0426, RUSTSEC-2024-0431;
research also suggest a significant correlation between type        The CVE ID is currently in the reserved status at the time
confusion bugs in Rust and the use of unsafe code.                  of writing and will be released later.

9   Conclusion                                                      References
In this paper, we develop T YPE P ULSE, the first static analysis
                                                                     [1] Clippy lints - cast pointer alignment. https:
tool for detecting type confusion bugs in Rust. T YPE P ULSE
                                                                         //rust-lang.github.io/rust-clippy/master/
focuses on detecting the three most common categories of
                                                                         index.html#/cast_ptr_alignment.
type confusion bugs— misalignment, inconsistent layout, and
mismatched scope. T YPE P ULSE detected 71 previously un-            [2] Clippy lints - unsound collection transmute. https:
known bugs from the top 3,000 Rust packages. This number                 //rust-lang.github.io/rust-clippy/master/
surpasses the number of type confusion bugs documented in                index.html#/unsound_collection_transmute.
the last five years in RustSec, which shows the effectiveness
of T YPE P ULSE. The identified bugs were reported to the de-        [3] Foreign function interface - the rustonomicon. https:
velopers, who have confirmed 32 of these issues. We also                 //doc.rust-lang.org/nomicon/ffi.html.
compare T YPE P ULSE with existing Rust bug detection tools,
and perform case studies to demonstrate the security implica-        [4] Generic data types - the rust programming lan-
tions of the identified bugs. T YPE P ULSE will be open-sourced          guage.       https://doc.rust-lang.org/book/
to facilitate future research.                                           ch10-01-syntax.html.

                                                                     [5] Greptime. https://greptime.com/.
Acknowledgment
                                                                     [6] The mir (mid-level ir) - rust compiler development
We thank our shepherd and the reviewers for their insightful
                                                                         guide.    https://rustc-dev-guide.rust-lang.
feedback. This work is partially supported by ONR grant
                                                                         org/mir/index.html.
N00014-23-1-2122 and the IDIA P3 Faculty Fellowship from
George Mason University.
                                                                     [7] pprof. https://crates.io/crates/pprof.

Open Science                                                         [8] read_unaligned in std::ptr - rust.    https:
                                                                         //doc.rust-lang.org/nightly/std/ptr/fn.
To promote transparency and reproducibility in our research,             read_unaligned.html.
the data artifacts of this paper will be made publicly avail-
able, including source code, detected bugs, and related github       [9] rust-lang/rust-clippy: A bunch of lints to catch com-
issues we reported. We disclose only those issues that have              mon mistakes and improve your rust code. book:
been acknowledged and resolved by developers. Issues that                https://doc.rust-lang.org/clippy/. https://github.
remain unresolved at the time of writing are not included in             com/rust-lang/rust-clippy/tree/master.
detail. All data is available on Zenodo: https://zenodo.
org/records/14750104.                                               [10] Rustsec: The rust security advisory database. https:
                                                                         //rustsec.org/advisories/.

Ethics Considerations                                               [11] std::slice::from_raw_parts. https://doc.rust-lang.
                                                                         org/std/slice/fn.from_raw_parts.html.
We take ethics seriously in this project. All Rust repositories
we tested in the paper are publicly accessible on Github. Dur-      [12] Trait and lifetime bounds - the rust reference.
ing evaluations of our work, T YPE P ULSE identified several             https://doc.rust-lang.org/reference/
previously unknown type confusion vulnerabilities in widely              trait-bounds.html.
used software. In each case, we followed a responsible dis-
closure policy, and reported our discovered vulnerabilities to      [13] Typeid in std::any - rust. https://doc.rust-lang.
the developers. We also submitted our findings to the CVE                org/stable/std/any/struct.TypeId.html.
program and the RustSec Advisory Database. We did not dis-
close those issues to anyone else. All the examples mentioned       [14] write_unaligned in std::ptr - rust.   https:
in the paper are the issues that have been acknowledged and              //doc.rust-lang.org/stable/std/ptr/fn.
fixed. The RustSec IDs issued are: RUSTSEC-2023-0046,                    write_unaligned.html.
[15] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon                    of type confusion errors for c++. In Proceedings of
     Lim, and Taesoo Kim. Rudra: Finding memory safety                 the 2017 ACM SIGSAC Conference on Computer and
     bugs in rust at the ecosystem scale. In Proceedings of the        Communications Security, pages 2373–2387, 2017.
     ACM SIGOPS 28th Symposium on Operating Systems
     Principles, SOSP ’21, page 84–99, New York, NY, USA,         [27] Paul Kirth, Mitchel Dickerson, Stephen Crane, Per
     2021. Association for Computing Machinery.                        Larsen, Adrian Dabrowski, David Gens, Yeoul Na, Stijn
                                                                       Volckaert, and Michael Franz. Pkru-safe: Automatically
[16] Fraser Brown, Shravan Narayan, Riad S. Wahby, Daw-                locking down the heap between safe and unsafe lan-
     son Engler, Ranjit Jhala, and Deian Stefan. Finding               guages. In Proceedings of the Seventeenth European
     and preventing bugs in javascript bindings. In 2017               Conference on Computer Systems, pages 132–148, 2022.
     IEEE Symposium on Security and Privacy (SP), pages
     559–578, 2017.                                               [28] The Rust Programming Language.      What is
                                                                       ownership?  https://doc.rust-lang.org/book/
[17] Mohan Cui, Chengjun Chen, Hui Xu, and Yangfan Zhou.               ch04-01-what-is-ownership.html.
     Safedrop: Detecting memory deallocation bugs of rust
     programs via static data-flow analysis. ACM Trans.           [29] Byoungyoung Lee, Chengyu Song, Taesoo Kim, and
     Softw. Eng. Methodol., 32(4), may 2023.                           Wenke Lee. Type casting verification: Stopping an
                                                                       emerging attack vector. In 24th USENIX Security Sym-
[18] Gregory J Duck and Roland HC Yap. Effectivesan: type
                                                                       posium (USENIX Security 15), pages 81–96, 2015.
     and memory error detection using dynamically typed
     c/c++. In Proceedings of the 39th ACM SIGPLAN Con-           [30] Tuo Li, Jia-Ju Bai, Yulei Sui, and Shi-Min Hu. Path-
     ference on Programming Language Design and Imple-                 sensitive and alias-aware typestate analysis for detecting
     mentation, pages 181–195, 2018.                                   os bugs. In Proceedings of the 27th ACM International
[19] Ana Nora Evans, Bradford Campbell, and Mary Lou                   Conference on Architectural Support for Programming
     Soffa. Is rust used safely by software developers? 2020           Languages and Operating Systems, ASPLOS ’22, page
     IEEE/ACM 42nd International Conference on Software                859–872, New York, NY, USA, 2022. Association for
     Engineering (ICSE), pages 246–257, 2020.                          Computing Machinery.

[20] Xiaokang Fan, Zeyu Xia, Sifan Long, Chun Huang, and          [31] Wei Li, Dongjie He, Yujiang Gui, Wenguang Chen, and
     Canqun Yang. Accelerating type confusion detection                Jingling Xue. A context-sensitive pointer analysis frame-
     with pointer analysis. IAENG International Journal of             work for rust and its application to call graph construc-
     Computer Science, 20:664–671, 2020.                               tion. In Proceedings of the 33rd ACM SIGPLAN Interna-
                                                                       tional Conference on Compiler Construction, CC 2024,
[21] Istvan Haller, Yuseok Jeon, Hui Peng, Mathias                     page 60–72, New York, NY, USA, 2024. Association
     Payer, Cristiano Giuffrida, Herbert Bos, and Erik                 for Computing Machinery.
     Van Der Kouwe. Typesan: Practical type confusion
     detection. In Proceedings of the 2016 ACM SIGSAC             [32] Xuejian Li and Zhengguang Zhu. Software defect detec-
     Conference on Computer and Communications Security,               tion based on feature fusion and alias analysis. In 2023
     pages 517–528, 2016.                                              IEEE International Test Conference in Asia (ITC-Asia),
                                                                       pages 1–6, 2023.
[22] Valerii Hiora. lmdb-rs: Rust bindings for lmdb. https:
     //crates.io/crates/lmdb-rs.                                  [33] Zhuohua Li, Jincheng Wang, Mingshen Sun, and
                                                                       John C.S. Lui. Mirchecker: Detecting bugs in rust pro-
[23] The White House.      Future software should
                                                                       grams via static analysis. In Proceedings of the 2021
     be memory safe.      https://www.whitehouse.
                                                                       ACM SIGSAC Conference on Computer and Communi-
     gov/oncd/briefing-room/2024/02/26/
                                                                       cations Security, CCS ’21, page 2183–2196, New York,
     press-release-technical-report/.
                                                                       NY, USA, 2021. Association for Computing Machinery.
[24] The HuggingFace. The ai community building the fu-
     ture. https://huggingface.co/.                               [34] Samuel Mergendahl, Nathan Burow, and Hamed
                                                                       Okhravi. Cross-language attacks. In NDSS, 2022.
[25] The HuggingFace. Candle - minimalist ml frame-
     work for rust. https://github.com/huggingface/               [35] Mozilla. Mozilla firefox. https://www.mozilla.
     candle.                                                           org/en-US/firefox/new/.

[26] Yuseok Jeon, Priyam Biswas, Scott Carr, Byoungyoung          [36] NIST. Nvd - cve-2023-3079. https://nvd.nist.
     Lee, and Mathias Payer. Hextype: Efficient detection              gov/vuln/detail/CVE-2023-3079.
[37] NIST. Nvd - cve-2023-4762. https://nvd.nist.             [52] rustc_middle. rustc_middle::mir::statement. https:
     gov/vuln/detail/CVE-2023-4762.                                //doc.rust-lang.org/nightly/nightly-rustc/
                                                                   rustc_middle/mir/struct.Statement.html.
[38] NIST. Nvd - cve-2024-1939. https://nvd.nist.
     gov/vuln/detail/CVE-2024-1939.                           [53] rustc_middle. rustc_middle::mir::terminator::terminator.
                                                                   https://doc.rust-lang.org/nightly/
[39] Michalis Papaevripides and Elias Athanasopoulos. Ex-          nightly-rustc/rustc_middle/mir/terminator/
     ploiting mixed binaries. ACM Transactions on Privacy          struct.Terminator.html.
     and Security (TOPS), 24(2):1–29, 2021.
                                                              [54] RUSTSEC. Rustsec-2019-0035. https://rustsec.
[40] Plain. Trait plain - doc.rs. https://docs.rs/plain/
                                                                   org/advisories/RUSTSEC-2019-0035.html.
     latest/plain/trait.Plain.html.
                                                              [55] RUSTSEC. Rustsec-2020-0029. https://rustsec.
[41] Michael Pradel, Parker Schuh, and Koushik Sen.
                                                                   org/advisories/RUSTSEC-2020-0029.html.
     Typedevil: Dynamic type inconsistency analysis for
     javascript. In 2015 IEEE/ACM 37th IEEE International     [56] RUSTSEC. Rustsec-2022-0074. https://rustsec.
     Conference on Software Engineering, volume 1, pages           org/advisories/RUSTSEC-2022-0074.html.
     314–324. IEEE, 2015.
                                                              [57] RUSTSEC. Rustsec-2024-0016. https://rustsec.
[42] The Rust Project. Rust Programming Language. https:
                                                                   org/advisories/RUSTSEC-2024-0016.html.
     //www.rust-lang.org/.
                                                              [58] RUSTSEC. Rustsec-2024-0338. https://rustsec.
[43] The Rust Project. Type conversions - the rusto-
                                                                   org/advisories/RUSTSEC-2024-0338.html.
     nomicon. https://doc.rust-lang.org/nomicon/
     conversions.html.                                        [59] Lili Sun, Chenggang Wu, Zhe Wang, Yan Kang, and
[44] Boqin Qin, Yilun Chen, Zeming Yu, Linhai Song, and            Bowen Tang. Kop-fuzzer: A key-operation-based fuzzer
     Yiying Zhang. Replication package for article: Under-         for type confusion bugs in javascript engines. In 2022
     standing memory and thread safety practices and issues        IEEE 46th Annual Computers, Software, and Applica-
     in real-world rust programs. Artifact Digital Object          tions Conference (COMPSAC), pages 757–766, 2022.
     Group, 2020.                                             [60] The Rust Team.     from_utf8 in std::str - Rust.
[45] The Rust Reference.   Trait objects. https:                   https://doc.rust-lang.org/stable/std/str/
     //doc.rust-lang.org/reference/types/                          fn.from_utf8.html.
     trait-object.html.
                                                              [61] The Rust Team.      Function from_utf8_unchecked
[46] The Rust Reference. Type layout. https://doc.                 in std::str - Rust. https://doc.rust-lang.org/
     rust-lang.org/reference/type-layout.html.                     stable/std/str/fn.from_utf8_unchecked.html.

[47] Elijah Rivera, Samuel Mergendahl, Howard Shrobe,         [62] The Rust Team. Meet safe and unsafe. https://doc.
     Hamed Okhravi, and Nathan Burow. Keeping safe rust            rust-lang.org/nomicon/meet-safe-and-unsafe.
     safe with galeed. In Proceedings of the 37th Annual           html#meet-safe-and-unsafe.
     Computer Security Applications Conference, pages 824–
     836, 2021.                                               [63] The Rust Team.   unsafe - rust. https://doc.
                                                                   rust-lang.org/std/keyword.unsafe.html.
[48] Rust.      Cargo targets - the cargo book.
     https://doc.rust-lang.org/cargo/reference/               [64] The Rust Reference.  Behavior considered unde-
     cargo-targets.html.                                           fined. https://doc.rust-lang.org/reference/
                                                                   behavior-considered-undefined.html.
[49] Rust.   Pod in bytemuck.   https://docs.rs/
     bytemuck/latest/bytemuck/trait.Pod.html.                 [65] Linus Torvalds and thousands of contributors. The linux
                                                                   kernel. https://www.kernel.org/.
[50] Rust.   Traits.  https://doc.rust-lang.org/
     reference/items/traits.html.                             [66] Wikipedia.  Breadth-first search. https://en.
                                                                   wikipedia.org/wiki/Breadth-first_search.
[51] rustc_middle. rustc_middle::mir::local. https:
     //doc.rust-lang.org/nightly/nightly-rustc/               [67] Wikipedia. Lint (software). https://en.wikipedia.
     rustc_middle/mir/struct.Local.html.                           org/wiki/Lint_(software).
 1   // lmdb - rs / src / traits . rs                                 1   #[ repr ( align (2) )]
 2   impl FromMdbValue for $t {                                       2   #[ derive (Copy, Clone , Debug )]
 3     fn from_mdb_value ( value : & MdbValue ) -> $t {               3   struct Padding { a: u8 , b: u16 , c: u8 }
 4        unsafe { * transmute ( value . get_ref () ) }               4   fn main () {
 5      }                                                             5     let la = Padding { a: 10 , b: 11 , c: 12 };
 6   }                                                                6     let mdbval = MdbValue :: new_from_sized (& la );
 7   // lmdb - rs / src / core . rs                                   7     let res = i32 :: from_mdb_value (& mdbval );
 8   #[ inline ]                                                      8      println !( " {:?} " , res );
 9   pub fn new_from_sized <T >( data : &’a T) -> MdbValue <’a > {    9   }
10     unsafe { MdbValue :: new ( transmute ( data ) ,
11                  size_of :: <T >() )}                                       Listing 10: Exploit that trigger bug type II.
12   }

     Listing 8: The vulnerabilities in lmdb-rs package [22].

                                                                     convert it into i64 using from_mdb_value defined in List-
                                                                     ing 8, which would cause the misalignment issue. The data is
 1 fn main () {
 2   let a: i32 = 3;                                                 aligned only if it is stored at an address that is a multiple of the
 3   let mdbval = MdbValue :: new_from_sized (& a);                  type’s alignment bytes. Most primitive types (e.g., u8 and u32
 4   let res = i64 :: from_mdb_value (& mdbval );
 5   println !( " {:?} " , res );                                    in this case) are aligned to their size. For example, a 32-bit
 6 }                                                                 integer (i32) should be stored at the memory address that is
                                                                     a multiple of 4. However, the starting address of i32 may
            Listing 9: Exploit that trigger bug type I.
                                                                     not be a multiple of 4, hence accessing a misaligned object
                                                                     can results in undefined behavior. In this case, a misaligned
                                                                     pointer dereference (Line 5 in Listing 8) would cause runtime
[68] Hui Xu, Zhuangbin Chen, Mingshen Sun, Yangfan Zhou,             panic. Generally, such undefined behaviors in architectures
     and Michael R. Lyu. Memory-safety challenge consid-             that do not support unaligned access (e.g., before ARMv5)
     ered solved? an in-depth study with all rust cves. ACM          would cause the program to crash.
     Trans. Softw. Eng. Methodol., 31:3:1–3:25, 2020.
                                                                     Type II: Inconsistent layout bug. In Listing 10, the second
                                                                     type of bug occurs when reinterpreting the uninitialized area
[69] Yuchen Zhang, Yunhang Zhang, Georgios Portokalidis,
                                                                     of the source object in memory. We define a struct Padding
     and Jun Xu. Towards understanding the runtime perfor-
                                                                     (line 3) and instantiate an object la (line 5), and then convert
     mance of rust. In Proceedings of the 37th IEEE/ACM
                                                                     it into an i32 primitive object res. It looks like the source
     International Conference on Automated Software Engi-
                                                                     and target objects share the same size (u8+u16+u8=i32), but
     neering, pages 1–6, 2022.
                                                                     there will be padding bits among each member variable in the
                                                                     struct for alignment. In this case, member b’s size is 16 bits
A      Bugs Due to Generic Type Conversion                           (u16); thus, there will be 8-bit padding for both a and c. These
                                                                     paddings are uninitialized areas in memory, which would trig-
We demonstrate these three types of type conversion bugs             ger the undefined behavior when transmute() accesses them.
using an example. The bugs are discovered from lmdb-rs               Besides, a further dangerous issue is the unknown padding
package [22], which is a package providing API bindings              layout in Rust. Different from the struct padding rule in C (i.e.,
to the LMDB (Lightning Memory-Mapped Database) li-                   repr(c)), which usually adds padding bits at the end of the
brary. In Listing 8, we showcase an implementation of                struct, Rust has no guarantees of data layout made by the de-
from_mdb_value function defined in the FromMdbvalue                  fault representation (repr(rust)). That means the compiler
trait. The primary functionality of this code snippet is to con-     can do whatever it wants to reorder fields based on access
vert a reference of MdbValue into another type $t. The type          patterns. A possible rule in practice is to organize by field
conversion is performed using transmute at line 4, which is          size to minimize padding. Therefore, the location of padding
included in unsafe. The function new_from_size (line 9) is           is random and may cause data exposure.
used to create a new object MdbValue from the reference of           Type III: Mismatched scope bug. The third bug type hap-
generic type T. Therefore, the users of the package can create       pens when the value of the source object exceeds the bit-
input for from_mdb_value with new_from_size function.                pattern range of the target type. The bit pattern refers to the
All type conversion bugs occur in from_mdb_value function            raw binary representation of data in memory. In the case of
because of the problematic type conversion.                          Listing 11, we convert an i32 variable into the bool type.
Type I: Misalignment bug. The first type of bug occurs               However, the i32 has 232 bit-patterns while the boolean type
when reinterpreting the type of the source object in memory          has only 2 bit-patterns (false/true). The value false has
to another type with a larger alignment. In the exploit code         the bit pattern 0x00 and the value true has the bit pattern
of Listing 9, we define and initialize an i32 variable a, and        0x01. Hence, an undefined behavior would occur if an bool
                                                                   we find that developers have tried to limit the input types
 1 fn main () {
 2   let a: i32 = 3;                                               by adding the size check, ensuring the memory layout to
 3   let mdbval = MdbValue :: new_from_sized (& a);                be stable. However, the size check is not sufficient to check
 4   let res = bool :: from_mdb_value (& mdbval );
 5   println !( " {:?} " , res ); // illegal boolean type          the alignment and the validity of types. Nevertheless, we still
 6                                                                 consider that the developers of the top 3,000 packages provide
 7   let arr = [1 u8 ; 2];
 8   println !( " {:?} " , arr [ res as usize ]) ; // OOB index    more protection in this type conversion, leading to the least
 9 }                                                               number (14) of bugs compared to the others (37 in Con →
                                                                   Con and 21 in Gen → Con).
         Listing 11: Exploit that trigger bug type III.
                                                                    1 Conversion. For the methods used for type conversion,
                                                                   we find that developers make more mistakes with as than
                                                                   transmute. We assume that developers tend to use as more
object represents any other bit pattern. Moreover, even the con-   commonly since transmute is a unsafe function itself while
version between same-sized types may suffer such an issue.         as is not, but they are not aware that as can also create prob-
For example, the string type in Rust only supports UTF-8           lematic types, even if it is a safe function. Since we find
encoding that includes (28 − 2) unit characters. When we con-      fewer numbers of mismatched scope bugs than the other two
vert an u8 (28 bit-patterns) into string type, the undefined       types of bugs, we consider that the maintainers of the top
behavior can also be triggered if the value of source object is    3,000 packages are more experienced in avoiding this kind of
254 or 255. The third bug can also be exploited to trigger the     bug. To support our conjecture, we randomly pick 10 more
Out-Of-Bound memory access (OOB). Originally, the com-             packages that are not ranked in the top 3,000 and find 6 more
piler always inserts the bound check to protect us from the        mismatched scope bugs. The bug discovered in lmdb-rs pack-
OOB vulnerability. When the compiler assumes that type has         age is one of the examples (see Appendix A).
legal value and removes the unnecessary bound check, OOB
can be triggered (see line 8).                                      2 Access. We also study the unsafe usages of problematic
                                                                   types which could trigger the bugs, and separate them into
                                                                   three categories. First, type conversion can cause bugs when
B    Root Cause of Type Confusion Bugs                             developers try to build a slice or vector with unsafe functions
                                                                   such as from_raw_parts. Second, dest is a raw pointer type,
Based on Table 3, we summarize the root cause of type confu-       and the developers try to dereference the raw pointer. The
sion bugs we have found in two phases: First, we discuss how       purpose of raw pointer dereference can be separated into two
developers make mistakes based on type conversion patterns.        kinds: a) overwrite the value stored at the memory address
Second, we study the error-prone methods of 1 Conversion           and b) dereference the raw pointer to rebuild the reference.
and 2 Access, specifically on usages of unsafe functions.          Third, developers try to use transmute between references,
Con → Con. TypePulse identifies more type confusion bugs           which is dangerous and might break the safety guarantee of
in the concrete type conversion from the top 3,000 packages.       reference.
In concrete type conversion, we highlight the causes of mis-
alignment bugs since its number (21) is much more than the
others (10 on inconsistent layout bugs and 6 on mismatched
scope bugs). We consider the root cause to be the lack of
alignment awareness. We can also find that developers sup-
press the warnings of alignment from Clippy [9]. While some
developers consider the impacts of misalignment are minor
since most operating systems nowadays can tolerate the un-
aligned memory access, we have discovered an issue that can
cause to crash (see §5.5).
Gen → Con. In the type conversion Gen → Con, we have
discovered more inconsistent layout bugs (15) than the others
(2 on misalignment bugs and 4 on mismatched scope bugs).
Based on our observation, the developers usually consider
the input types that initialize the generic type have a stable
memory layout and consequently initialized. For example,
the function as_byte_slice is always used to convert the
generic type into the slice of u8, leading to uninitialized mem-
ory exposure.
Con → Gen. For bugs related to type conversion Con → Gen,
