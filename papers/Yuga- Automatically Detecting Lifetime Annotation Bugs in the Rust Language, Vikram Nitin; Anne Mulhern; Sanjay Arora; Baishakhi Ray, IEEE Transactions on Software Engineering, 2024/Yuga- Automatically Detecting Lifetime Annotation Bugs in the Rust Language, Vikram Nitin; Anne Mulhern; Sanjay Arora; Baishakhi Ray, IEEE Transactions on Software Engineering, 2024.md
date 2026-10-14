                                                        Y UGA: Automatically Detecting Lifetime
                                                        Annotation Bugs in the Rust Language
                                                                   Vikram Nitin , Anne Mulhern , Sanjay Arora , and Baishakhi Ray



                                                                                                                       ✦



                                                                                                                           associated memory are owned by exactly one identifier at
arXiv:2310.08507v3 [cs.SE] 24 Jan 2025




                                         Abstract—The Rust programming language is becoming increasingly
                                         popular among systems programmers due to its efficient performance                any point in the program. Modern programming languages
                                         and robust memory safety guarantees. Rust employs an ownership                    handle memory usage during execution in different ways—
                                         model to ensure these guarantees by allowing each value to be owned               some rely on garbage collection (e.g., Java) and others on
                                         by only one identifier at a time. It uses the concept of borrowing and
                                                                                                                           manual allocation and deallocation (e.g., C). Rust takes an
                                         lifetimes to enable other variables to temporarily borrow values.
                                               Despite its benefits, security vulnerabilities have been reported
                                                                                                                           alternative approach with the concept of ownership, rein-
                                         in Rust projects, often attributed to the use of ”unsafe” Rust code.              forced by compiler-verified rules. Yet, none of these rules
                                         These vulnerabilities, in part, arise from incorrect lifetime annotations         significantly slow down the run-time of Rust programs.
                                         on function signatures. However, existing tools fail to detect these bugs,            However, the strict ownership policy—each value
                                         primarily because such bugs are rare, challenging to detect through               owned by only one identifier at any given time, is of-
                                         dynamic analysis, and require explicit memory models.                             ten overly limiting. Thus, Rust allows Borrowing—another
                                               To overcome these limitations, we characterize incorrect lifetime
                                                                                                                           identifier may temporarily borrow a value under certain
                                         annotations as a source of memory safety bugs and leverage this under-
                                                                                                                           conditions by creating a reference to that value. Consider
                                         standing to devise a novel static analysis tool, Y UGA, to detect potential
                                         lifetime annotation bugs. Y UGA uses a multi-phase analysis approach,             the statement a = &b, here a is borrowing the value b.
                                         starting with a quick pattern-matching algorithm to identify potential            Rust further introduces the concept of Lifetimes to restrict
                                         buggy components and then conducting a flow and field-sensitive alias             a borrow’s scope—a lifetime is a region of the source code
                                         analysis to confirm the bugs. We also curate new datasets of lifetime             in which the borrowing identifier is live; the borrowing
                                         annotation bugs. Y UGA successfully detects bugs with good precision on           identifier must not outlive the borrowed value (e.g., a
                                         these datasets, and we make the code and datasets publicly available.             cannot outlive b in the above example).
                                                                                                                               The Rust compiler, specifically its Borrow Checker, ensures
                                         Index Terms—Rust, Lifetimes, Static analysis
                                                                                                                           the validity of all borrows by tracking variable lifetimes.
                                                                                                                           Often the checker can infer the lifetime of a variable with-
                                                                                                                           out assistance. However, for certain cases related to inter-
                                         1    I NTRODUCTION
                                                                                                                           procedural reasoning, the compiler requires explicit lifetime
                                         The Rust programming language is gaining increasing pop-                          annotations on function signatures to guide the Borrow
                                         ularity among systems programmers for its efficient perfor-                       Checker. For example, the type &’a i32 denotes a borrow
                                         mance while providing strong memory safety, thread safety,                        to an integer value, where the lifetime of the borrow is
                                         and type checking. It uses a C-like syntax that allows low-                       parameterized by the lifetime annotation ’a. These annota-
                                         level access, enabling it to be used on embedded devices,                         tions on the function signature provide valuable information
                                         to write kernel code, to build performance-critical systems,                      to the compiler, enabling it to verify certain memory safety
                                         and so on. At the same time, it ameliorates many of the                           properties without even looking at the function body.
                                         pitfalls of C, like pointer errors and concurrency errors.
                                         For these reasons, Google recently extended support for                           Violation of memory safety guarantees. Despite the strong
                                         developing the Android OS in Rust [1], and Rust is officially                     safety guarantees promised by Rust, an increasing num-
                                         supported in the Linux kernel as of Linux 6.1 [2].                                ber of security vulnerabilities have been reported in Rust
                                                                                                                           projects. The number of vulnerabilities reported to the
                                         Rust memory safety model. While working within the
                                                                                                                           RUSTSEC Database [3] during 2018 was only 22; in 2022,
                                         secure confines of Rust, we enjoy robust safety guarantees.
                                                                                                                           there were 91. The majority of these vulnerabilities arise
                                         Central to these assurances is Rust’s Ownership model—a
                                                                                                                           from the use of a language feature called unsafe Rust [4]—
                                         set of rules dictating memory management within a Rust
                                                                                                                           Rust’s memory safety guarantees can be too restrictive for
                                         program. Ownership guarantees that each value and its
                                                                                                                           some applications, so Rust provides an “escape hatch” in
                                                                                                                           the form of unsafe Rust, which allows writing code that
                                         •   Vikram Nitin and Baishakhi Ray are with the Department of
                                                                                                                           bypasses some memory safety checks. The added flexibility
                                             Computer Science, Columbia University, New York, USA. E-mail:
                                             vikram.nitin@columbia.edu, rayb@cs.columbia.edu                               comes at the cost of potential memory safety-related bugs.
                                         •   Anne Mulhern and Sanjay Arora are with RedHat Research, USA. E-                   Thus, while using unsafe Rust, it is the developer’s
                                             mail: {amulhern, saarora}@cs.columbia.edu
                                                                                                                           responsibility to ensure the code is correct—a single mistake

                                                                                                                       1
                Move:         Heap:xxxx   1. let a = String::from("Hello");                                       Heap:xxxx   1. let a = String::from("Hello");
    Transfer Ownership                                                                    b is borrowing w/o
                              Heap:xxxx   2. let b = a;                               transferring ownership      Heap:xxxx   2. let b = &a;
      a is no longer valid;                                                                         a is valid;
                              Heap:xxxx   3. println!("{ }",a);                                                   Heap:xxxx   3. println!("{ }",a);
    this is a compile error                                                                this does compile

 (a) Ownership. The read of a at Line 3 causes the program to not (b) Borrowing. When the String is borrowed by b (Line 2), a still
 compile because b has taken ownership of the String value and so retains ownership of the String and so of the heap region XXXX
 a is not live.                                                   which the String owns.

              Fig. 1: Ownership and Borrowing. The color of an identifier indicates the color of the heap region it owns.


may jeopardize the whole program’s safety guarantees and                          analyzing relationships between program variables through
introduce vulnerability. One of the causes of such vulner-                        nested pointers and structures. When a mismatch is found,
abilities is incorrect lifetime annotations (LAs) on function                     Y UGA flags the corresponding pairs of values as potentially
signatures. Deciding the correct LAs for a variable is non-                       buggy. In the third stage, Y UGA conducts a flow and field-
trivial—it requires expert knowledge of how the value                             sensitive alias analysis to confirm the interactions between
will propagate to subsequent borrows and pointers, often                          the source and target, further validating the presence of
through deeply nested structures and function calls. Fur-                         bugs. Up to this point, the analysis is intra-procedural.
ther, lifetimes in Rust are a non-intuitive concept even for                      In the final stage, Y UGA employs specific shallow filters
experienced programmers, as there is no analogous concept                         based on common inter-procedural knowledge to reduce
in any other popular programming language (to the best of                         false positives, improving the overall precision.
our knowledge). A one-token mistake in specifying correct                             Results. We evaluate Y UGA using a dataset of known
LAs can lead to security vulnerabilities[5], as we see from a                     security vulnerabilities, and a synthesized vulnerability
manual inspection of reported Rust security vulnerabilities.                      dataset. We find that Y UGA can detect LA bugs with 87.5%
    Limitation of Existing Approaches. Checking the safety                        precision on this dataset of known vulnerabilities. None of
of unsafe Rust is an active area of research [6], [7], [8],                       the existing static analysis tools we evaluated could detect
[9], [10], [11], with multiple reported vulnerabilities [3], [4],                 any of these vulnerabilities. We also ran Y UGA on 372 Rust
and automated tools that perform static [12], [13], [14], [15],                   libraries, and Y UGA generated 85 reports. Of these, 3 were
and dynamic [16], [17] analysis to check for vulnerabilities.                     confirmed to be exploitable vulnerabilities, and the rest were
However, none of these existing tools can detect memory-                          “code smells” that are not exploitable but indicate potential
safety bugs due to incorrect LAs. First of all, LA bugs are                       for a vulnerability to arise in future development.
rare and typically only surface during execution in specific                          Contributions: Our contributions in this paper are:
edge cases. Thus, detecting them through dynamic analysis                         1) We are the first to characterize incorrect lifetime annota-
is non-trivial. Additionally, they tend to be deeply embed-                       tions that can lead to memory safety bugs.
ded within a program, and analyzing them requires accurate                        2) We propose Y UGA, a novel static analysis technique, that
modeling of program memory. Thus, it becomes challenging                          can automatically scan Rust projects at scale and detect
to study using standard static analyzers or symbolic execu-                       potential LA bugs that can lead to vulnerabilities.
tion tools. Even, more mature hybrid vulnerability detection                      3) We evaluate Y UGA in a variety of settings and show that
tools designed for other languages like C/C++ cannot be                           it can successfully detect LA bugs with good precision. To
applied here as LA is a new concept introduced in Rust.                           the best of our knowledge, there are no existing baseline
    To this end, we propose a novel static analysis tool to                       static analyzers that can find these bugs.
check correct memory usage in unsafe Rust code. In par-                           4) We contribute two new datasets of lifetime annota-
ticular, we focus on detecting incorrect lifetime annotations                     tion bugs, one created from Rust security vulnerabilities,
(LAs) as they often lead to security vulnerabilities.                             and the other synthetic. We make the code and dataset
    Our approach: We have developed and implemented a                             publicly available at https://github.com/vnrst/Yuga, and
novel static analysis tool called Y UGA, capable of detect-                       https://github.com/vnrst/rust-lifetime-bugs respectively.
ing incorrect LA bugs. We employ a multi-phase analysis                               The rest of the paper is structured as follows. In Sec-
approach that starts with a pattern-matching algorithm to                         tion 2, we discuss the features of Rust and lifetime annota-
quickly identify the potential buggy components. Subse-                           tions. Then, we define three patterns of lifetime annotation
quently, we perform a flow and field-sensitive alias anal-                        bugs in Section 3.1. Section 3.2 presents the design of Y UGA,
ysis, focusing only on the potential buggy components to                          our tool to detect lifetime annotations bugs. We evaluate the
confirm the bugs. By adopting this multi-phase analysis, we                       performance of Y UGA in Sections 4 and 5, present related
effectively address the well-known scalability challenges as-                     work in Section 7, and conclude in Section 8.
sociated with alias analysis, while still achieving reasonably
high precision.
                                                                                  2    BACKGROUND
    In particular, Y UGA operates in four stages. First, it prop-
agates the LAs from a function parameter to internal refer-                          This section provides an overview of Rust’s ownership
ences, pointers, and fields, using an AST-like representation.                    model and the memory safety properties associated with it.
In the second stage, it identifies any potential mismatches                       Section 2.1 explains how Rust ensures memory safety via its
in LAs between the function arguments and return values.                          ownership model. Section 2.2 discusses how Rust can be
These first two steps are challenging since they involve                          used in an unsafe manner.

                                                                              2
                                                             1   let b : &i32;                     1   let mut a = 5;
                 1 fn foo() {                                2   {   let a : i32 = 5;              2   let ref1 = &a;
                 2 let a = String::from("Hello");            3       b = &a;                       3   let ref2 = &mut a;
           b's   3 let b = &a;                    a's        4   } println!("{}", b);              4   println!("{}", ref1);
     lifetime    4 println!("b: { }", b);         lifetime
                 5 println!("a: { }", a);
                 6 }                                         (b) The compiler will reject this     (c) The compiler will reject this pro-
                                                             program since b’s lifetime ex-        gram because the lifetimes of im-
     (a) The lifetime of the borrow, i.e., b’s lifetime,     tends till Line 4, but a’s life-      mutable borrow ref1 (Lines 2-4) and
     must not extend beyond the lifetime of the              time is terminated by the closing     mutable borrow ref2 (Line 3) are not
     borrowed value a.                                       brace on Line 3.                      disjoint.

                                                             Fig. 2: Lifetimes in Rust.


2.1      Rust Memory Safety Model                                            1 helps prevent some common memory errors as use-after-
                                                                             free and double-free. Rule 2 promotes thread safety by pre-
1)     Ownership.
                                                                             venting concurrent writes and deadlocks. It further allows
Rust’s ownership model ensures that a memory location has                    the compiler to perform numerous low-level optimizations,
exactly one owner at any point in the program, and the                       e.g., eliminating unnecessary reads from memory.
associated memory is freed when the owner goes out of                             Figure 2 illustrates the concept of lifetimes. In Figure 2a,
scope. For example, in Figure 1a, at Line 1, the identifier a                a owns the String while b borrows it. By Rule 1, it is
is assigned a String value. The characters of the String                     essential that a outlives b, and this is satisfied. In contrast,
are stored on the heap, and a takes ownership of this heap-                  in Figure 2b, b’s lifetime extends until line 4, but a’s lifetime
allocated memory. At Line 2, a is assigned to b. This move                   extends only until line 3. So the Borrow Checker rejects this
transfers the ownership of the heap-allocated memory to                      program. In Figure 2c the lifetime of ref2 (Line 3), which
b. Once b takes ownership of this memory, Rust no longer                     borrows a mutably, is not disjoint from the lifetime of ref1
considers a use of a to be valid, as a memory location must                  (Line 2-4) which also borrows a. So the Borrow Checker will
have exactly one owner. So the print statement on Line 3                     reject this program by Rule 2.
will result in a compile error.                                              Lifetime Annotations on Functions. So far, we have discussed
                                                                             how the compiler infers lifetimes when a reference is as-
2)     Borrowing.                                                            signed directly to an identifier, like b = &a. Now con-
                                                                             sider a function call where a parameter or return type
A value can be borrowed by creating a reference to that
                                                                             is a reference. In the simple case of a function with
value using the ‘&’ symbol. A reference can be mutable
                                                                             one reference parameter and one returned reference, e.g.,
or immutable, depending on whether one can modify the
                                                                             fn foo(x: &String) -> &String, the lifetimes of the
borrowed value through the reference or not, respectively.
                                                                             argument and the returned reference are calculated as if the
Mutable references are denoted as &mut. Figure 1b illus-
                                                                             invocation of the function is just a use of the argument. So,
trates borrowing. At Line 1, String "Hello" is assigned
to an identifier a, and a takes ownership of the String. At                    let b = String::from("Hello");
Line 2, b merely borrows the String (i.e., it does not take                    let a = foo(&b);
ownership) by taking a reference to a. a retains ownership                   is equivalent to
of the heap-allocated memory associated with the String.
Consequently, the compiler does not reject the use of a at                     let b = String::from("Hello");
                                                                               let a = &b;
Line 3, and the program compiles.
                                                                             for the purpose of inferring lifetimes. In both cases, the
3)     Lifetimes.                                                            lifetime of a is considered as the lifetime of the borrow, and
                                                                             b must outlive a. Consider, however, a function that takes
A Rust lifetime is similar to a scope—it is a statically                     more than one parameter.
determined region of a program. However, it is not always
defined by a lexical marker such as a closing curly brace                      fn foo(x: &String, y: &String) -> &String
[18]. For example, in Figure 2a, b’s lifetime is just Lines 3-4.             The returned reference must not outlive the value that it’s
     If a reference is assigned to an identifier, e.g., b = &a,              borrowing, by Rule 1. But it’s not clear what that borrowed
then the lifetime of the identifier is called the lifetime of the            value is. It could be derived from any one of the two
borrow. Two rules constrain the lifetimes of borrows:                        input arguments. In this situation, the compiler requires the
Rule 1: The lifetime of a borrow must not extend beyond the                  developer to add LAs.
lifetime of the borrowed value. In other words, the borrowed value
                                                                               fn foo<'a,'b>(x: &'a String, y: &'b String)
must “outlive” the borrow.
                                                                                         -> &'b String { y }
Rule 2: If there are multiple borrows to the same value, every
mutable borrow must have a lifetime which is disjoint from that              Here, ’a and ’b are lifetime annotations (LAs) that rep-
of every other borrow, whether mutable or immutable.                         resent the actual lifetimes of the two input borrows. In
     Rust’s Borrow Checker ensures that these rules are not                  this example, the developer has chosen to declare that the
violated. The Borrow Checker must assign a lifetime to each                  returned reference derives from the second argument, by
identifier such that the assignment satisfies these rules. Rule              placing the lifetime parameter ’b on second parameter and

                                                                         3
                                                                             1   let v1 = "Hello".to_string();
                                                                             2   let v2 = "World".to_string();
   struct Foo<'a> {                                                          3   let bar_obj = bar(&v1, &v2);
       x: *const String,                                                     4   drop(v2);                  v2 is borrowed
       ..                                                                    5   // Code that uses bar_obj    only till here
   }                                                    bar_obj is
   fn bar<'a,'b>(arg1: &’a String, arg2: &'b String)   used till here
           -> Foo<’a> {
                                                     Code compiles, but potential memory safety error!
       Foo{x: arg2 as *const String, ..}
   }
                                                                 (b) The string v2 is dropped on Line 4, and bar_obj will
   (a) The function returns a pointer that derives from          contain a pointer to freed memory. This can cause a use-after-
   arg2, but the annotation indicates that it uses arg1.         free error.

                    Fig. 3: Incorrect lifetime annotations on functions can cause memory safety errors.


on the return type. The compiler will reject the function if         obey. For example, one can have mutable and immutable
the returned reference is not a reference to some part of y.         raw pointers to the same location. The memory location it
    LAs are only a syntactic representation of a concrete            points to need not live as long as a raw pointer itself, which
lifetime, i.e., a region of code. However for conciseness, we        means that a raw pointer is not guaranteed to point to valid
shall sometimes use expressions like “the lifetime ’a” to            memory. A raw pointer type does not allow LAs. Although
mean “the lifetime associated with the LA ’a”.                       creating and manipulating a raw pointer is permitted in safe
Lifetime Annotations on Structures. LAs can be used only in          Rust, any dereference of a raw pointer must be done in an
two specific contexts - the first is in function signatures,         unsafe block or function.
as shown above, and the second is in the declaration of
algebraic data types like structures. If a structure con-            3)    Unsafe Code and Lifetime Annotations.
tains a reference as one of its fields, then that reference
                                                                     Although raw pointers themselves don’t have LAs, they
must have an associated LA. Further, that same annotation
                                                                     can be contained within structure objects, and these structure
must appear as part of the structure type. For example,
                                                                     objects can have associated LAs. In Figure 3a, function bar
struct Foo<'a>{x: &'a i32} is a structure Foo containing
                                                                     returns a structure containing a raw pointer. In bar’s signa-
a reference with LA’a, so <’a> is part of its type. The
                                                                     ture the placement of the LA ’a in x: &’a and Foo<’a>
significance of this annotation is that ’a is the lifetime of
                                                                     informs the compiler that the structure object is tied to the
the borrow, so the structure object must not outlive ’a.
                                                                     lifetime of x.
                                                                          Although the code in the example contains no unsafe
2.2   Unsafe Rust                                                    regions, it still contains a bug which the compiler did not
The framework discussed above guarantees memory                      detect; the LA on the result type should be b, not a, because
safety [12], [19]. However, these guarantees are inherently          it is y, not x, which is assigned to the inner field of the
conservative and prevent access to many useful constructs            returned structure. This can pose a problem as shown in Fig
often required for systems programming, like low-level               3b. The borrow lifetime ’a is tied to bar_obj, and extends
memory manipulation, external function calls, etc. To sup-           till Line 5. But the borrow lifetime ’b extends only till line 3,
port such functionalities, Rust has an extended language             and so v2 is no longer borrowed after line 3. It can be dropped
called unsafe Rust, which allows some additional features            on Line 4 without a compile error. Now the inner field of
that bypass some of the safety guarantees of safe Rust.              bar_obj points to freed memory, and will result in a use-
In this connection, we discuss the unsafe keyword, raw               after-free error if dereferenced in an unsafe block.
pointers, and lifetime annotation. Evans et al. [20] provide a            At a high level, our analysis deals with raw pointers and
more comprehensive discussion of unsafe Rust.                        references, and tries to identify situations where the values
                                                                     that they point to get freed. Raw pointers go hand-in-hand
1) The unsafe Keyword.                                               with unsafe code, because most operations involving raw
The unsafe keyword is used to distinguish regions con-               pointers, like dereferencing and freeing, require unsafe.
taining unsafe Rust from the rest of a program. If a function
is marked unsafe then the body of the function may use
unsafe Rust and a function caller must treat the function            3     M ETHODOLOGY
as unsafe. If a block within a function is marked unsafe,            First we describe our process of classifying and characteriz-
then the developer must ensure the the function provides             ing LA bugs in Section 3.1. Then we use these patterns to
the same guarantees of safe Rust when it is used. Just one           develop Y UGA, as described in Section 3.2.
function that violates this contract may introduce errors that
break the memory safety guarantees of the entire program.
                                                                     3.1    Characterizing Lifetime Annotation Bugs
2) Raw Pointers.                                                     Within a function, some values may be transferred between
Raw pointers are similar to pointers in C - they obey none           two arguments (arg-arg) or between an argument and re-
of the guarantees that references in Rust are expected to            turned value (arg-return). When the transfer of a value

                                                                 4
happens, the LAs on the target of the transfer should be con-           TABLE 1: Lifetime Annotation Bugs of Different Types. The
sistent with the source of the transferred value. Otherwise, it         incompatible lifetime annotations are highlighted in red.
leads to a LA bug.
                                                                           Example 1. RUSTSEC-2021-0130: UAF bug in the lru crate
     Arguments and return types are the only places where                  caused by assigning a value from an argument to return (arg-
LAs can occur in a function signature. Therefore, all LA                   return)
bugs fall into one of two categories: (i) mismatched arg-arg or
(ii) mismatched arg-return. This claim is validated by an initial
                                                                          1   pub struct LruEntry<K, V> {
study of LA bugs reported to the RustSec Security Advisory                2       next: *mut LruEntry<K, V>, ..
Database (see Section 5 for details). Such incorrect LAs may              3   }
                                                                          4   pub struct LruCache<K, V> {
lead to memory safety bugs, like:                                         5       head: *mut LruEntry<K, V>, ..
1) Use-after-free (UAF): Such bugs occur when we attempt                  6   }
                                                                          7   pub struct Iter<'a, K: 'a, V: 'a> {
to access memory that has been freed or de-allocated.                     8       ptr: *const LruEntry<K, V>, ..
2) Non-exclusive mutability (NEM): These occur when                       9   }
                                                                         10   impl<K, V, S> LruCache<K, V, S> {
two mutable borrows co-occur within the same lifetime.                   11       ...
We describe these bugs in the rest of the section in detail.             12     pub fn iter<’a>(&’_ self) -> Iter<’a, K, V> {
                                                                         13           Iter {
1) Use-after-free Bugs                                                   14               ptr: unsafe { (*self.head).next },
                                                                         15               ..
Let’s say a function takes a value that is associated with               16           }
a borrow lifetime ’a and assigns it to a location where it is            17       }
                                                                         18   }
associated with a borrow lifetime ’b. If ’b is longer than ’a,
a UAF error could occur (violation of Rule 1 in Section 2.1.3).
This can be caused by arg-arg or arg-return assignment.
                                                                           Example 2. RUSTSEC-2021-0128: UAF bug in the rusqlite
Arg-Return Assignment: Example 1 in Table 1 shows an                       crate caused by assigning a value from one argument to another
example of a real-world UAF bug caused by arg-return as-                   argument (arg-arg).
signment. On Line 12, the function iter, takes an argument
self, and by following the fields of each structure, we see               1   pub struct InnerConnection {
that (*self.head).next is a raw pointer to a value of type                2     db: *mut ffi::sqlite3,
LruEntry, and it is associated with the LA ’_. On Line 14,                3     ..
                                                                          4   }
it is assigned to the ptr field of the returned Iter object,              5   pub struct Connection {
where it is associated with the LA ’a on Iter<’a, ..>.                    6     db: RefCell<InnerConnection>
                                                                          7   }
The LAs do not correctly specify the relationship between                 8   impl Connection {
the lifetimes of the two values, so the compiler will accept              9        ..
a program that uses the returned Iter object even after                  10     pub fn update_hook<’c,F>(&’c self,hook:Option<F>)
                                                                         11        where
(*self.head).next has been freed, leading to a UAF.                      12        F: .. + ’c
Arg-Arg Assignment: There is a subtle difference in check-               13     {
ing LAs for arg-arg assignments. In Example 2 in Table 1,                14       self.db.borrow_mut().update_hook(hook);
                                                                         15     }
for every call of the update_hook function, hook must live               16   }
at least as long as self. However, the LAs do not enforce
this requirement and could lead to a UAF. Both hook and
self have the same LA ’c, which means that they both live                  Example 3. RUSTSEC-2020-0023: NEM bug in the rulinalg
at least as long as ’c. But this does not mean that hook lives             crate caused by assigning a value from an argument to return
as long as self.                                                           (arg-return)


2) Non-Exclusive Mutability Bugs                                          1   pub struct MatrixSliceMut<'a, T: 'a> {
                                                                          2       ptr: *mut T, ..
Incorrect LAs can allow the lifetimes of multiple mutable                 3   }
borrows to overlap (i.e., violate Rule 2 in Section 2.1.3),               4   pub struct RowMut<'a, T: 'a> {
                                                                          5       row: MatrixSliceMut<'a, T>
leading to NEM. This kind of error can be caused by arg-                  6   }
return or arg-arg assignment. However, in our empirical                   7   impl<'a, T: 'a> RowMut<’a, T> {
analysis (as we shall describe in Section 4.2.3), we did not              8     /// Returns the row as a slice.
                                                                          9     pub fn raw_slice_mut(&’_ mut self)->&’a mut [T] {
observe any NEM bugs caused by arg-arg assignment. We
                                                                         10       unsafe { from_raw_parts_mut(self.row.ptr, ..) }
therefore exclude them from the scope of this paper, and                 11     }
leave it to future work.                                                 12   }
Example 3 in Table 1 shows a real-world example of a
NEM bug caused by arg-return assignment. On Line 9,
raw_slice_mut, takes a mutable borrow to self. The mu-
table pointer self.row.ptr of type *mut T is re-borrowed                3.2   Algorithm Design
for the lifetime ’_. This same value is then returned through
a borrow with lifetime ’a. It is possible for ’a to be                  In this subsection, we present Y UGA, a tool to automatically
longer than ’_, so raw_slice_mut can be called multi-                   detect incorrect LAs on function signatures in Rust projects.
ple times to create multiple mutable borrows to the same                An overview of the entire system is shown in Figure 5. The
*(self.row.ptr) value.                                                  input to Y UGA is the source code of a Rust project, and the

                                                                    5
           struct Foo<'a> { x: *mut String,
                            w: &'a mut i32 }                            RUST Source               High-level IR                     Mid-level IR
           struct Bar { y: String,
                        z: *mut i32 }                                                                                          Func body
                                                                         fn abc(&'a foo: Foo<'b>)-> &'b Bar
                                                                                                                                                 Report   Step IV
                                                                                                                Function              Step III
           fn bar<'a,'b>(arg1: &'a mut i32,                                                                                                                Filter
                                                                              Step I                            signature         Alias analysis
                         arg2: &'b mut Bar)
                                                                         Get lifetimes for
                   -> Foo<'a> {
                                                                          each (nested)                                         Step II
               let ret = Foo{ x: &mut (*arg2).y,                               value               Bar.x : 'b
                                                                                                                     Match lifetime bug patterns           Warning!
                              w: arg1 };                                                           Barfoo.x   : 'a
                                                                                                                                                              --
                                                                                                    *(foo.y) : 'b
               ret                                                                                                   Pattern     Pattern       Pattern
                                                                                                                                                             ----
                                                                                              Borrow                   1           2               N
           }
                                                                                             Lifetimes
            Value           Type       Borrowed For
           arg1        &’a mut i32         None                                                      Fig. 5: Y UGA workflow.
           *arg1           i32              ’a
            arg2          &’b Bar          None
           *arg2             Bar            ’b                       rules follows from this assumption. For a formal definition
         (*arg2).y         String           ’b
         (*arg2).z       *mut i32           ’b                       of these rules, please refer to the supplementary material.
         *(*arg2).z         i32             ’b                           Given a function argument or return type, we extract
            ret          Foo<’a>           None                      lifetimes for each nested value as follows:
           ret.w       &’a mut i32         None                      1) If a value is borrowed with LA’b, then the value and all
         *(ret.w)           i32             ’a                       its fields must outlive ’b, as per Rule1 in Section 2.1.3. For
           ret.x       *mut String         None
         *(ret.x)         String            ’a                       example, in Figure 4, *arg2 is borrowed with lifetime ’b,
                                                                     so *arg2 and (*arg2).y must outlive ’b.
Fig. 4: Motivating example. We calculate borrow lifetimes            2) If a value is pointed by a raw pointer and the raw pointer
for each value and look for lifetime bug patterns. The               is contained inside a structure with LA’a, then ’a is the
arrows ←→ show pairs of values associated with potential             lifetime of the structure, and the value must outlive ’a.
violations, and the corresponding rows are shaded in gray.           For example, in Figure 4, ret.x is a raw pointer inside a
We then use Alias Analysis to filter these violations, leaving       structure with LA’a, so *(ret.x) must outlive ’a.
only the one shown with a red arrow ←→.                              3) If a value is pointed by a raw pointer and the raw
                                                                     pointer is contained inside a structure with no LA, then
                                                                     this value must outlive any lifetime that the structure object
output is a list of functions with potential LA errors. At a         must outlive. For example, in Figure 4, (*arg2).z is a raw
high level, Y UGA works in four steps.                               pointer in a structure object *arg2 with no LA. But we
• Step-I. Y UGA extracts lifetimes from each type of a func-         derived that *arg2 must outlive ’b. So *(*arg2).z must
   tion signature.                                                   also outlive ’b.
• Step-II. Next, Y UGA uses these lifetimes to check for
   the LA bug patterns identified in Section 3.1 and marks           2) Step-II. Check for Lifetime Bug Patterns
   potential buggy functions.                                        After we derive lifetimes for each value, we iterate through
• Step-III. The potential buggy functions are then sent to           these lifetimes and look for potential violations. As we
   an alias analyzer to check whether values are actually            discussed in Section 3.1, there are two main causes of bugs
   transferred between the locations with LAs.                       - assignment from an argument to the returned value (arg-
• Step-IV. Finally, Y UGA filters out some common patterns           return), or from an argument to another argument (arg-arg).
   of false positives due to intra-procedural alias analysis.        Arg-Return: We iterate through all the values in the argu-
     We now discuss each step of our system in de-                   ments, and pair them against all the returned values. We
tail and refer Figure 4 as a motivating example to                   consider only the cases where at least one of the two values
illustrate the steps. In Figure 4, the function sig-                 is held by a raw pointer, because Rust will automatically
nature is: fn bar<’a,’b>(arg1: &’a mut i32, arg2:                    infer the lifetimes in all other cases. The patterns that we
&’b mut Bar) -> Foo<’a>. This means that bar is a                    look out for are:
function name, and ’a,’b are LAs associated with the                 1) Use-after-free: If the types match, and the lifetime of
function bar. The function takes a parameter arg1, which is          the returned value can be longer than the lifetime of the
a mutable reference with borrow lifetime a to an i32 value,          value in the argument, then this is a potential violation (see
and another parameter arg2, which is a mutable borrow                Rule1 in Section 2.1.3). For example, in Figure 4, (*arg2).y
with lifetime ’b to a structure of type Bar. The function’s          and *(ret.x) have the same type String, but different
return type is Foo<’a>, which is a structure containing a            lifetimes ’b and ’a. This is a potential violation.
reference with borrow lifetime ’a.                                   2) Non-exclusive Mutability: If one value is of type *mut
                                                                     T or &mut T, and the other value is of type T for some
1) Step-I: Get Borrow Lifetimes                                      type T, then the lifetime of the latter cannot be longer than
Our rules for assigning “outlives” lifetimes to values are a         the lifetime of the former (see Rule2 in Section 2.1.3). For
generalization of the Rust typing rules for borrows, to raw          example, in Figure 4, (*arg2).z and *(ret.w) have types
pointers. We propose to treat a raw pointer as though it is          *mut i32, and i32, but different lifetimes ’b and ’a. This
“owned” by the structure that it is contained in. Each of our        is a potential violation.

                                                                 6
Arg-Arg: We only focus on use-after-free bugs caused by                 remain valid. However in certain cases, memory is “leaked”
assignments from argument to argument. We take the two                  and is never freed. This means there is no scope for a use-
arguments at a time, and iterate through all the pairs of               after-free vulnerability. A memory leak is not considered an
values in these arguments. We ignore cases where both                   exploitable vulnerability or undefined behavior in Rust.
values are behind immutable references because an assign-                Hence we implement a simple inter-procedural check. If
ment can only be performed if one value is mutable. If                  the value being re-assigned is behind a raw pointer in both
the types of the two values match, then we report this as               the source as well as the target structures, then we only
a bug. The actual borrow lifetimes do not matter, as we                 mark this as a violation if either of those structures has a
discussed in Section 3.1.1. For example, in Figure 4, *arg1             custom Drop implementation. A custom Drop implementa-
and *(*arg2).z have the same type i32, and are mutable.                 tion would usually involve cleaning up memory, and this
So this is a potential violation.                                       means that when that structures gets dropped, the data
                                                                        value might be freed.
3) Step-III. Perform Alias Analysis                                       Filter Common Patterns of False Positives: There are
The previous steps give us a list of pairs of values such that          certain common traits in Rust that rely on the semantic
it would be dangerous to perform an assignment between                  correctness of their implementation to ensure their safety.
them. For instance, in Figure 4, if the value in (*arg2).y              One such example is the IteratorMut trait, specifically its
becomes the value in *(ret.x), then this could lead to a                next and next_back methods [23].
use-after-free.                                                            There are three specific functions from trait im-
     This is the problem of alias analysis, or determin-                plementations that we filter out - Iterator::next,
ing whether two pointers point to the same memory                       Iterator::next_back, Clone::clone. It is true that
location[21]. Our algorithm works by computing a “points-               there can be potential flaws in their implementations, which
to” set of values that each pointer may point to. It has the            is why the shallow filter is the last stage of our analysis, and
following properties:                                                   a user has the option of turning it off.
• Intra-procedural: We perform our analysis on each function
body individually, treating function calls as opaque.
• Field-sensitive: We treat each field of a structure separately.
                                                                        4     E XPERIMENTAL S ETUP
• Flow-sensitive: We consider the program statements in                 4.1   Implementation
order and compute points-to sets at each program point.                 When Rust code is compiled, it goes through several inter-
This is usually infeasible for whole program analysis, but              mediate representations (IRs), two of which are the High-
becomes feasible for intra-procedural analysis.                         level IR (HIR) and the Mid-level IR (MIR). The HIR is a tree
     We follow a similar setup to Andersen’s analysis[22],              representation of the program that is similar to an Abstract
where we update points-to sets in different ways depending              Syntax Tree (AST). The MIR represents each function as a
on the type of assignment statement, for example, if we have            control-flow graph of basic blocks, with each basic block
a = b then we merge b’s points-to set into a’s. However,                consisting of a number of statements. MIR boils the different
our algorithm is flow-sensitive because we process each                 kind of statements occurring in a program down to a core
statement just once in order, unlike Andersen’s analysis                set of statement types like assignments, memory allocation,
which is flow-insensitive and iterates over the statements              and memory de-allocation. We use a hybrid approach that
till convergence.                                                       combines information from the HIR and the MIR. We use
     For a function call, we simply assume all types of assign-         the HIR to get struct definitions and function signatures,
ment statements between all pairs of function arguments                 and use the MIR to perform alias analysis.
and fields therein. For example, if we have foo(a, b),                      We implement our system Y UGA in Rust as a fork of
we separate it into a = b, a = b, *b = a, and so on. We                 the Rudra [12] project. We use the nightly-2022-11-18
provide pseudocode and more details about our algorithm                 version of rustc and cargo, and run our tool on Rust
in the supplementary material.                                          projects as a cargo subcommand.
     While implementing field sensitivity, we make a delib-
erate choice to ignore “unknown” fields in function calls.
                                                                        4.2   Study Subject
For example, if we have foo(a, b), and a has a field a.x,
then we don’t make a connection between a.x and b unless                We evaluate Y UGA in three different settings: (i) 23 real-
a.x is already “known” to our pointer analysis, i.e., it has            world vulnerable functions curated from 9 crate libraries,
been used previously. As we will show in Section 5.2, we                (ii) a synthetic vulnerability dataset, and (iii) running Y UGA
empirically found that this eliminates false positives and              across 372 popular Rust crate libraries. This section de-
increases precision.                                                    scribes each setting in detail.

4) Step-IV. Apply Shallow Filter                                        1) Curating bugs from Vulnerability Reports.
Our shallow filter is designed to filter out false positives,           A library crate (or crate for short) in Rust is a project
based on some primitive inter-procedural analysis, as well              that provides functionality that can be used in other Rust
as knowledge of common patterns of false positives. We                  projects. This is similar to a package or library in other pro-
provide a brief overview here; for more details, please refer           gramming languages. Rust hosts a community crate registry
to the supplementary material.                                          at crates.io, and any project can add a library crate from
 Filter based on Drop Implementations: Y UGA detects vio-               this registry as its dependency. Adding a crate as a project
lations based on assumptions about how long memory must                 dependency allows one to use APIs from that crate in the

                                                                    7
project. The RustSec Security Vulnerability Database[3] is            TABLE 2: Running Y UGA on Rustsec vulnerabilities due to LA
                                                                      bugs. FN=False Negatives, FP=False Positives
a collection of security vulnerability reports in Rust crates.
We manually inspected each report in the RustSec database
                                                                                         Error   #Vulnerable
[3], looking for issues related to incorrect LA. We found 9               RustSec ID     Type      Funcs         #Detected     #FP     #FN
vulnerabilities that matched this pattern. These are shown                 2018-0020     UAF         1 + 2*           2         0       1
in Table 4. Each of these corresponds to one crate contain-                2020-0023     NEM           2              2         0       0
ing one or more buggy functions. There are a total of 23                   2020-0060     UAF           1              0         0       1
functions with bugs across the 9 vulnerabilities.                          2021-0128     UAF           7              7         2       2
                                                                           2021-0130     UAF         2 + 3*           5         0       0
                                                                           2022-0028     UAF           2              0         0       2
2)    Creating a Synthetic Bug Dataset.                                    2022-0040     UAF           1              0         0       1
                                                                           2022-0070     UAF           1              0         0       1
In addition to evaluating Y UGA on the bugs from vulnerabil-               2022-0078     UAF           1              0         0       1
ity reports, we would like to check whether it can generalize                Total                    23             16         2       9
to similar patterns of bugs. To do this, we prepared a
                                                                          The asterisk * denotes newly exposed bugs that weren’t part of the
synthetic bug dataset based on the above 9 vulnerability                                            initial report.
reports in three steps, as follows.
• Program Slicing and Simplification. Each of the 9 reports
contains one or more functions with a LA bug. We selected             4.4     Baselines
one function from each report, isolated the structures and            We evaluate against the following baselines:
functions responsible for the bug, and rewrote them in a              • Rudra[12]: Rudra is a static analyis based bug detector
minimal form. This gave us a list of 9 synthetic bugs.                that detects certain kinds of errors in unsafe Rust.
• Program Transformations. For each of the 9 synthetic bugs           • MirChecker[13]: MirChecker is a static analysis based
from the previous step, we manually applied a variety of              analyzer that can detect certain categories of undefined
transformations to them that retain the semantics of the code         behavior, like overflows and out-of-bounds accesses.
but change the high level structure. For instance, we wrap            • Miri[16]: Miri is a dynamic analysis tool that interprets
borrows in structures or enums, change concrete types into            one MIR instruction at a time and detects memory errors.
generic types, change datatypes, add more dummy borrows
with different lifetime annotations, etc. We transformed the
9 bugs in two different ways each by applying selected                5     R ESEARCH Q UESTIONS
transformations, to get a total of 27 synthetic bugs.                 We aim to answer the following research questions:
• Exploit Construction. For each synthetic bug, we con-               • RQ1: Effectiveness of our tool. We evaluate the effective-
struct an “exploit” function that showcases the vulnerability         ness of Y UGA in three settings: 1) Can Y UGA detect reported
present in it and triggers undefined behavior.                        Rust security vulnerabilities that result from incorrect LAs?
                                                                      2) How does Y UGA generalize to the synthetic bug dataset
3)    Scanning Crates from the Registry                               that we curated? 3) How does Y UGA perform when we run
                                                                      it on a large set of real-world Rust crates?
We also use our tool to scan crates from the crates.io reg-
                                                                      • RQ2: Impact of Design Choices. How do the different
istry. We pick the top 2000 most downloaded crates as of
                                                                      model components of Y UGA impact its performance on
November 15th, 2022, and filter out those which do not use
                                                                      vulnerabilities and synthesized bugs?
unsafe code or lifetime annotations. This leaves us with 372
                                                                      • RQ3: Existing tools. Are there any existing tools that can
crates. We download the original source for each of them
                                                                      detect incorrect lifetime annotations?
using the cargo-download tool. Our tool is implemented
as a cargo subcommand, and we run this subcommand on
the downloaded source folders.                                        5.1     RQ1: Effectiveness of our Tool
                                                                      This research question is structured as follows. First, we
                                                                      shall evaluate the performance of Y UGA by running it on
4.3    Evaluation and Metrics                                         the 23 functions from 9 crates from RustSec vulnerabilities.
To evaluate Y UGA, we first define a “ground truth” bug. For          Then, we will measure the ability of Y UGA to generalize by
the RustSec and Synthetic bug dataset, we know by con-                running it on our synthetic bug dataset of 27 bugs. Finally,
struction that each of the functions reported in the security         we run Y UGA on a large set of real-world Rust crates.
vulnerability are confirmed bugs. For all other functions that
our tool marks as potential bugs, we manually inspect each            1) Evaluation on RustSec Vulnerabilities
one. We classify a reported bug as genuine only if we are             We run Y UGA on the 9 crates from RustSec vulnerabilities,
able to clearly exploit the vulnerability to cause undefined          containing 21 buggy functions. Its performance is summa-
behavior. If we are uncertain or unable to cause undefined            rized in Table 2. Overall, the precision is 87.5%, and the
behavior, we classify this as a false positive.                       recall is 60.9%.
     We assess Y UGA’s ability to identify lifetime annotation        Detected bugs: Y UGA generates 16 vulnerability reports
bugs using precision and recall metrics. In a given dataset,          from 3 crates. 2 of these reports are NEM bugs, and the other
if the bugs detected by Y UGA are denoted by SY UGA , and the         14 are UAF. The 3 bugs in Table 1 are among the vulnerable
ground truth bugs are denoted by SGT , the precision and              functions that Y UGA is able to detect correctly.
recall of Y UGA can be defined as |SGT ∩ SY UGA |/|SY UGA | and       New bugs exposed: For RUSTSEC-2021-0130 correspond-
|SGT ∩ SY UGA |/|SGT | respectively.                                  ing to the lru-rs crate, the report had only 2 functions

                                                                  8
listed as bugs. However, our tool detected 3 additional               it is an external dependency. So our tool ignores this. 4 out
functions as potential bugs - peek_lru, get_or_insert,                of the 9 false negatives are because of hidden raw pointers.
get_or_insert_mut. When we looked at the commit his-                  We discuss more about this limitation in Section 6.
tory on GitHub[24], it turned out that these functions had            2) Type conversion: To increase precision, Y UGA checks if the
been subsequently identified as memory safety bugs.                   types of the source and target values match. But that can
  In the pulse-binding crate corresponding to the vul-                also be too restrictive, as Listing 2 shows:
nerability RUSTSEC-2018-0020, Y UGA flags two additional               1   pub struct InnerConnection {
functions as potential bugs. We have corresponded with the             2       pub db: *mut ffi::sqlite3, ...
developer[25] regarding these functions, and these seem to             3   }
                                                                       4   pub struct Connection {
be genuine vulnerabilities that can be exploited with appro-           5       db: RefCell<InnerConnection>, ...
priate driver code to cause runtime errors with Valgrind.              6   }
The fact that Y UGA was able to detect these bugs despite              7   impl Connection {
them not being explicitly labeled is a strong validation of            8       pub fn create_aggregate_function<A, D, T>(
                                                                       9           &self, ...,
our tool and approach.                                                10           aggr: D,
False Positives: In the rusqlite crate, Y UGA flags two               11       ) -> Result<()>
additional functions as potential bugs, however these are             12       where
                                                                      13           A: RefUnwindSafe + UnwindSafe,
not exploitable vulnerabilities. Listing 1 shows one of them:         14           D: Aggregate<A, T>,
 1   pub struct InnerConnection {                                     15       ...
 2       pub db: *mut ffi::sqlite3,
 3       interrupt_lock: Arc<Mutex<*mut ffi::sqlite3>>, ...
                                                                      Listing 2: False negative in the rusqlite crate correspond-
 4   }                                                                ing to RUSTSEC-2021-0128
 5   impl InnerConnection {
 6       #[inline]                                                    Here, the type of the raw db pointer on line 2 is
 7       pub fn get_interrupt_handle(&self)->InterruptHandle
 8       {   InterruptHandle {                                        ffi::sqlite3, and the type of aggr on line is a generic
 9               db_lock: Arc::clone(&self.interrupt_lock),           type D. Y UGA would filter this out because the types do not
10           }
11       }                                                            match, but in fact, D is converted to a c_void pointer which
12       pub fn close(&mut self) -> Result<()> {                      is then attached to the db using a C foreign function call
13           ...
14           let mut shared_handle = self.interrupt_lock              (not shown in the snippet). This kind of type conversion is
15                                       .lock().unwrap();            difficult to reason about. 2 of the 9 false negatives are due to
16           ...
17
                                                                      type conversion.
                 *shared_handle = ptr::null_mut();
18               ...                                                  Of the remaining 3, one is due to LAs on the arguments of
19       }                                                            a closure, which is something that we do not reason about.
20   }
21   impl InterruptHandle {                                           One is due to a shortcoming of alias analysis, and the last
22       pub fn interrupt(&self) {                                    one is due to a complex indirect lifetime semantics where
23           let db_handle = self.db_lock.lock().unwrap();
24           if !db_handle.is_null() {                                one value acts as a drop guard for another value.
25               unsafe{ffi::sqlite3_interrupt(*db_handle)}
26           }                                                        2) Evaluating Generalizability using Synthetic Dataset.
27       }
28   }                                                                We run Y UGA on the 27 synthetic bugs curated. For each
Listing 1: False positive in the rusqlite crate correspond-           of the 9 original RustSec vulnerability reports, we derive 3
ing to RUSTSEC-2021-0128                                              synthetic bugs. The three synthetic bugs derived from the
                                                                      n-th RustSec report are denoted by n.1, n.2 and n.3.
The pointer interrupt_lock is shared between the struc-                    Table 3 summarizes the result—Y UGA is able to detect
ture InnerConnection and InterruptHandle on line 9,                   16 out of 27 bugs, corresponding to a recall of 59.3%. There
and there is no LA on InterruptHandle to denote this. But             are some cases where Y UGA is unable to detect the bug in
the implementations of the close and interrupt functions              the original RustSec report, but is able to detect one or more
circumvent any vulnerability. The code sets the pointer to            of the corresponding bugs in the synthetic dataset. A few of
null on Line 17, and checks if it is null before dereferencing        the reasons for this are as follows:
it on line 24. This example illustrates how the difference            • We re-implement some external dependencies. For exam-
between safe code and a vulnerability can be very subtle. At          ple, Y UGA is unable to detect the bug in pub fn
the same time, because this is so subtle, this indicates a risk       waker<W>(wake: Arc<W>) -> Waker, because it does not
in the future development of this crate and can be termed             have access to the implementation of the Waker structure.
a “code smell”. We discuss more about these patterns in               But in our synthetic examples 3.1 and 3.2, we re-implement
Section 5.1.3.                                                        the Waker structure, and thus Y UGA is able to see that there
False Negatives: Our tool is unable to detect 9 of the func-          is a raw pointer inside.
tions. Some of the reasons are:                                       • Some types are simplified. For example in the 6th RustSec
1) “Hidden” Raw Pointers: Our tool reports violations only            report RUSTSEC-2022-0028, Y UGA is unable to detect a
in cases where there is a raw pointer involved. Sometimes,            raw pointer because it is “hidden” behind a chain of type re-
it is not easy to infer that a certain type contains a raw            definitions and imports. In our synthetic examples 6.1 and
pointer. pub fn waker<W>(wake: Arc<W>) -> Waker {                     6.2, the types are simplified and it detects the raw pointer.
... } is an example.                                                      Since we constructed this dataset ourselves, there aren’t
Here, Waker is a structure containing a raw pointer, but we           many functions apart those containing bugs. So our tool
don’t have access to the definition of this structure because         does not report any false positives on this dataset.

                                                                  9
     TABLE 3: Results of Y UGA on synthetic bug dataset.                 User-implemented Reference Counting: The developer
                                                                       has implemented their own system of reference counting
        Bug     Detected   Bug    Detected   Bug    Detected
                                                                       and memory management. Every time a pointer is du-
         1.1       No       4.1     Yes       7.1      No              plicated or dropped, an internal reference count within
         1.2       No       4.2     Yes       7.2      No
         1.3       No       4.3     No        7.3      No              the memory location is incremented or decremented. The
         2.1       Yes      5.1     Yes       8.1      No
                                                                       memory is freed only if the count has reached zero. If any
         2.2       Yes      5.2     Yes       8.2      Yes             of these increments, decrements or checks are omitted, this
         2.3       Yes      5.3     Yes       8.3      Yes             could result in a UAF or memory leak.
         3.1       Yes      6.1     Yes       9.1      Yes              Memory copy, not alias: Y UGA predicts that there could
         3.2       Yes      6.2     Yes       9.2      Yes             be a vulnerability if two pointers were aliased, however the
         3.3       No       6.3     No        9.3      No
                                                                       function actually copies the underlying memory of the first
                                                                       pointer to create the target of the second pointer.
      TABLE 4: Running Y UGA on real-world Rust crates                  Different field of structure: Y UGA predicts that there could
                                                                       be a vulnerability if two pointers were aliased, however the
           Category                Sub-category              #
                                                                       aliasing actually happens with a different field of a structure.
        Exploitable bugs                                     3
                                                                        Two lifetimes: The structure has two LAs, say ’a and ’b,
                               Freed ptr but no deref        14        corresponding to two raw pointers within the structure. One
                           User-implemented ref counting     30
          Code smells          Memory copy, not alias        21        of the raw pointers is returned as a borrow with annotation
                               Different field of struct     16        ’a. But this is only valid if the underlying memory actually
                              Two lifetime annotations        1
                                                                       outlives ’a, and not ’b. This relies on the semantics of the
               Total                                         85        functions that allocate memory for these pointers.
                                                                        Summary: We evaluate Y UGA in different settings. On the
                                                                        RustSec vulnerabilities, it achieves a precision of 87.5%
3)    Evaluation on Real World Rust Crates.
                                                                        and a recall of 60.9%. On our synthetic dataset, it achieves
We would like Y UGA to be able to quickly scan and flag                 a recall of 59.3%. Finally, we were able to use Y UGA to
potential bugs in Rust crates, and scale to the thousands               scan 357 Rust crates “in the wild” in under 2 hours. We
of crates in the Rust crate ecosystem. We run Y UGA on a                found 3 exploitable bugs and 82 code smell patterns.
filtered list of 372 Rust crates as described in Section 4.2.3.
Y UGA is able to scan these crates in just under 2 hours, and
flags 85 potential bugs from 27 crates.                                5.2     RQ2: Impact of Design Choices
 Each of these bugs was classified into two broad categories
                                                                       We investigate the effect of three design choices in Y UGA -
- bugs which can be exploited to cause undefined behav-
                                                                       the Alias Analysis module, our handling of unknown fields
ior, and “code smells”, i.e., code patterns that cannot be
                                                                       in Alias Analysis, and the Shallow Filter.
exploited, but could indicate potential for a vulnerability to
arise during future development. We have further grouped
the code smells into different patterns. The results are sum-          1)    Alias Analysis.
marized in Table 4. Here we discuss some of these patterns.            We investigate the effect of the alias analysis module by
For a complete discussion with examples, please refer to the           removing it entirely. As shown in in Table 5, the recall
supplementary material.                                                increases, but the precision drops tremendously from 87.5%
Exploitable Bugs: Y UGA finds 3 new bugs among these                   to 34.1%. This shows that simple pattern matching is not
crates that can be exploited to cause undefined behavior,              sufficient, and deeper pointer analysis is necessary.
despite the fact that these are within the top ∼1.5% most
popular crates, with tens of millions of downloads each.               2)    Unknown Fields in Alias Analysis.
This is in addition to the 2 new bugs from pulse-binding               In Section 3.2.3, we described how we made a choice to
described earlier. Listing 3 shows one from cslice:                    exclude “unknown” fields in function calls, while designing
 1    pub struct CMutSlice<'a, T> {                                    our Alias Analysis algorithm. Here we explore the impact
 2      base: *mut T, ...                                              of that choice. The results are shown in Table 5. We can see
 3    }                                                                that considering unknown fields increases the recall slightly,
 4    pub fn as_mut_slice(&mut self) -> &'a mut [T]
 5    {   unsafe { slice::from_raw_parts_mut(                          but the precision on RustSec falls from 87.5% to 46.9%.
 6                self.base, self.len)} }
                                                                       TABLE 5: Impacts of different design choices. The numbers
     Listing 3: A genuine bug that Y UGA found in cslice
                                                                       that are different from the original are shown in bold.
On line 4, the lifetime ’a doesn’t match with the lifetime
                                                                                                      RustSec          Synthetic
of the borrow &self which has an implicit anonymous
lifetime. So this allows aliased mutable references.                                              Recall    Prec.   Recall    Prec.
  Freed Pointer but no Deref: There is a pointer within a                     Original (Y UGA)    60.9%    87.5%    59.3%
structure that is freed, but all the methods that dereference                w/o Shallow Filter   60.9%    63.6%    59.3%
                                                                                                                               –
the pointer are either private or unsafe. A small modifica-                  w/ Unknown Fields    65.2%    46.9%    62.9%
tion like making the method public or removing the unsafe                    w/o Alias Analysis   65.2%    34.1%    74.1%
label could result in an exploitable vulnerability.

                                                                  10
               Tool             # Bugs   Tool detected   Y UGA detected            For each of the 27 synthetic bugs, we ran Miri directly
              Rudra              50            0              30               with the exploit function (see Section 4.2.2) that exposes
            MirChecker           27            0              16
      Miri (w/o exploit code)    27            0              16               the vulnerability. Miri detected a memory safety error in
       Miri (w. exploit code)    27           27              16               all 27 of the cases, but without the exploit function, Miri
                                                                               cannot detect any one of them. This shows that given a large
            TABLE 6: Comparison with existing tools                            enough test suite, Miri might be able to find these bugs, but
                                                                               constructing that test suite is non-trivial. We discuss more
3) Shallow Filter.
                                                                               about dynamic tools in Section 7.
Our shallow filter is used to filter out common patterns of
false positives that result from trait implementations. We                      Summary: Existing static analysis tools are not well-suited
run Y UGA on the 21 functions from RustSec reports. With                        to this problem. For instance, Rudra and MirChecker were
the filter, there were 2 false positives; without it, that number               unable to detect any of the lifetime annotation bugs. The
increases to 8. The precision drops from 87.5% to 63.6%.                        dynamic tool Miri, in contrast, was able to detect the bugs,
                                                                                but it requires manually crafted test cases, which is non-
 Summary: All three of the design choices we investigate                        trivial in real project settings.
 contribute significantly to the precision of Y UGA.

                                                                               6   T HREATS TO VALIDITY
5.3    RQ3: Comparison with existing tools
                                                                               Our dataset from vulnerability reports includes only 23
In this section, we aim to evaluate existing static analysis
                                                                               functions from 9 crates, potentially limiting generalizability.
tools for detecting memory safety bugs in Rust. Although
                                                                               To address this, we synthesized 27 vulnerable functions
none of these tools are designed specifically to detect LA
                                                                               with varied contexts and types. Although the synthetic data
bugs, we investigate if there is any overlap between LA
                                                                               involves some subjective decisions, the dataset is publicly
bugs and the patterns that these tools look for. This also
                                                                               available for inspection. Additionally, we analyzed Y UGA
highlights the point that LA bugs are not just generic
                                                                               on several popular Rust crates, evaluating a total of 50 vul-
memory safety bugs and require special treatment.
                                                                               nerable functions across more than 300 real Rust libraries.
1) Rudra[12]:                                                                      On the dataset of functions from vulnerability reports,
                                                                               Y UGA achieves a precision of 87.5% and a recall of 60.9%.
Rudra is a static analysis tool that identifies three types of
                                                                               There is a tradeoff between these metrics, as higher recall
potential memory and thread safety violations - panic safety,
                                                                               can be achieved at the expense of precision, as shown
higher order safety invariant, and Send/Sync variance. It
                                                                               in 5.2. Note that, this is a challenging problem, and no
is not explicitly designed to detect LA bugs; however, we
                                                                               other tool can handle such bugs. We believe our precision
would like to check if there is any overlap between Rudra’s
                                                                               is comparable to or better than other Rust static analysis
bug categories and LA bugs.
                                                                               tools; for example, Rudra has a precision of 11.05%, and
We run Rudra on the 23 RustSec bugs and our synthetic
                                                                               MirChecker has 4.9%.
bug dataset of 27 bugs. We found that Rudra was unable to
                                                                                   Our implementation uses the HIR for identifying error
detect any of these 50 bugs. This indicates that there is no
                                                                               patterns and the MIR for alias analysis. However, the HIR
overlap between Rudra’s bug patterns and LA bugs..
                                                                               does not contain definitions of structures from external
2) MirChecker[13]:                                                             crates and dependencies. This causes a loss of precision or
                                                                               recall. In theory, one could re-implement our tool entirely at
MirChecker is a static analysis tool for the Rust MIR based
                                                                               the MIR level and have access to all external dependencies;
on the theory of Abstract Interpretation. It forms a control-
                                                                               however this would come with its own set of challenges
flow graph (CFG) of the program, defines a transfer function
                                                                               since a lot of the source information is lost in the MIR. We
for each value and statement, and propagates these values
                                                                               plan to address this in future work.
across the CFG to reach a fixed point. It then uses these                          More broadly speaking, Y UGA is a tool with a single
values to detect potential vulnerabilities in Rust code.                       specific use-case, i.e.,, detecting bugs in unsafe Rust arising
    This project is old and not compatible with the toolchains
                                                                               due to lifetime annotation errors. It does not generalize to,
used by most current Rust projects, but we were able to run
                                                                               or provide insights for, other kinds of unsafe Rust analysis.
it on our synthetic bug dataset. MirChecker was unable to
detect any of the 27 bugs. This shows that MirChecker will
also not be able to detect other more complicated bugs.                        7   R ELATED W ORK
                                                                               Dynamic testing of Rust code: Miri [16] is an interpreter
3) Miri[16]:                                                                   to detect invalid memory accesses or memory leaks (see
Miri is an interpreter for the Rust MIR. It emulates the                       Section 5.3). Stacked Borrows[26] (incorporated into Miri)
execution of each line of code using a virtual address space,                  develops a “stack” model to reason about borrows without
and can detect memory leaks, out of bounds accesses, and                       explicitly using lifetimes. Fuzzing with an address sani-
other potential vulnerabilities. This is a dynamic tool, and                   tizer is another way to detect potential errors, but existing
deals with actual vulnerabilities that arise when Rust code                    Rust fuzzers [27], [17] are not well suited to our prob-
is run. In contrast, Y UGA deals with potential vulnerabilities                lem. cargo-fuzz [17] is a fuzzing tool for Rust that uses
that could arise when a function is called in a certain context.               libFuzzer [28] as a backend. However, it is restricted to
So we expect Miri to detect LA bugs if and only if the exploit                 fuzzing functions that only accept input strings of a fixed
code is also provided.                                                         format and type.

                                                                          11
    Static analysis for detecting bugs in Rust: MirChecker                      [9]  J. Toman, S. Pernsteiner, and E. Torlak, “Crust: a bounded verifier
[13] and SafeDrop [14] are static analyzers on the Rust MIR                          for rust (n),” in 2015 30th IEEE/ACM International Conference on
                                                                                     Automated Software Engineering (ASE). IEEE, 2015, pp. 75–80.
that detect certain memory safety errors. However, these                        [10] H. M. Almohri and D. Evans, “Fidelius charm: Isolating unsafe
approaches tend to have high false negatives. Rudra [12]                             rust code,” in Proceedings of the Eighth ACM Conference on Data and
identifies three categories of bugs arising from unsafe code,                        Application Security and Privacy, 2018, pp. 248–255.
and scans the entire Rust crate ecosystem for these bug                         [11] E. Rivera, S. Mergendahl, H. Shrobe, H. Okhravi, and N. Burow,
                                                                                     “Keeping safe rust safe with galeed,” in Annual Computer Security
patterns. Rudra is the closest work to ours in the sense                             Applications Conference, 2021, pp. 824–836.
that it uses static analysis to identify potential memory                       [12] Y. Bae, Y. Kim, A. Askar, J. Lim, and T. Kim, “Rudra: finding
safety violations. However, Rudra can handle only three                              memory safety bugs in rust at the ecosystem scale,” in Proceedings
specific kinds of errors, and cannot detect memory safety                            of the ACM SIGOPS 28th Symposium on Operating Systems Principles,
                                                                                     2021, pp. 84–99.
bugs caused by incorrect lifetime annotations.
                                                                                [13] Z. Li, J. Wang, M. Sun, and J. C. Lui, “Mirchecker: detecting bugs
    Empirical analysis of unsafe Rust: Recent works [29],                            in rust programs via static analysis,” in Proceedings of the 2021 ACM
[20], [30], [4] characterize how developers use unsafe code                          SIGSAC Conference on Computer and Communications Security, 2021,
in Rust, and build an empirical understanding of bugs.                               pp. 2183–2196.
    Formal semantics of Rust: Patina [31] formalizes the                        [14] M. Cui, C. Chen, H. Xu, and Y. Zhou, “Safedrop: Detecting
                                                                                     memory deallocation bugs of rust programs via static data-flow
type system of Rust. FR [32] is a lightweight formalism                              analysis,” arXiv preprint arXiv:2103.15420, 2021.
of Rust that captures type checking and borrow checking.                        [15] Clippy     Contributors,     “Rust-clippy,”     https://github.com/
Oxide [33] models Rust code with non-lexical lifetimes [18]                          rust-lang/rust-clippy, 2022.
and a syntax close to safe surface Rust. However, these                         [16] Miri contributors, “Miri,” https://github.com/rust-lang/miri,
                                                                                     2022.
methods do not model unsafe code. RustBelt [34] develops                        [17] Rust team, “cargo fuzz,” https://github.com/rust-fuzz/
a comprehensive formal semantics based on lifetimes for                              cargo-fuzz, 2022.
a realistic subset of Rust including unsafe code. However,                      [18] N. D. Matsakis, “Non-lexical lifetimes: introduction,”
this cannot scale to larger codebases and crates. Verifying                          http://smallcultfollowing.com/babysteps/blog/2016/04/27/
                                                                                     non-lexical-lifetimes-introduction/, 2016.
the safety of a given library with RustBelt involves writing                    [19] R. Team, “The rustonomicon: The dark arts of unsafe rust,” 2018.
proofs with the Coq proof assistant [35], which requires                             [Online]. Available: https://doc.rust-lang.org/nomicon/
considerable expertise and effort.                                              [20] A. N. Evans, B. Campbell, and M. L. Soffa, “Is rust used safely
                                                                                     by software developers?” in 2020 IEEE/ACM 42nd International
                                                                                     Conference on Software Engineering (ICSE). IEEE, 2020, pp. 246–
8     C ONCLUSION                                                                    257.
In this paper, we investigate memory safety bugs arising                        [21] W. Landi, “Undecidability of static analysis,” ACM Letters on
from incorrect lifetime annotations in the Rust language.                            Programming Languages and Systems (LOPLAS), vol. 1, no. 4, pp.
                                                                                     323–337, 1992.
We demonstrate how such bugs can arise, and characterize                        [22] L. O. Andersen, “Program analysis and specialization for the c
bug patterns. Leveraging these patterns, we design Y UGA to                          programming language,” Ph.D. dissertation, Citeseer, 1994.
detect incorrect lifetime annotations in Rust. We show that                     [23] R. Team, “Rustonomicon - splitting borrows,” 2023. [Online].
Y UGA is able to effectively detect bugs in real-world Rust                          Available: https://doc.rust-lang.org/nomicon/borrow-splitting.
                                                                                     html
projects, compared to existing approaches which are unable                      [24] Lru Cache contributors, “Lru cache,” https://github.com/
to detect any of these bugs. Future work could involve                               jeromefroe/lru-rs/, 2023.
making the static analysis framework more precise, and                          [25] vnrst, “Possible ub in get api function,” 2023. [Online]. Available:
including other kinds of bugs in unsafe Rust.                                        https://github.com/jnqnfe/pulse-binding-rust/issues/53
                                                                                [26] R. Jung, H.-H. Dang, J. Kang, and D. Dreyer, “Stacked borrows: an
                                                                                     aliasing model for rust,” Proceedings of the ACM on Programming
R EFERENCES                                                                          Languages, vol. 4, no. POPL, pp. 1–32, 2019.
[1]   Google, “Rust in the Android platform,” 4 2021.                           [27] Loı̈c Lecrenier, “Fuzzcheck,” https://github.com/loiclec/
      [Online]. Available: https://security.googleblog.com/2021/04/                  fuzzcheck-rs, 2022.
      rust-in-android-platform.html                                             [28] L. Team, “libfuzzer – a library for coverage-guided fuzz testing,”
[2]   S. Vaughan-Nichols, “Linus Torvalds: Rust will go into Linux                   2023. [Online]. Available: https://llvm.org/docs/LibFuzzer.html
      6.1,” 9 2022. [Online]. Available: https://www.zdnet.com/article/         [29] B. Qin, Y. Chen, Z. Yu, L. Song, and Y. Zhang, “Understanding
      linus-torvalds-rust-will-go-into-linux-6-1/                                    memory and thread safety practices and issues in real-world rust
[3]   Rust developers, “Rust security advisory database,” 2022.                      programs,” in Proceedings of the 41st ACM SIGPLAN Conference on
      [Online]. Available: https://rustsec.org/advisories/                           Programming Language Design and Implementation, 2020, pp. 763–
[4]   H. Xu, Z. Chen, M. Sun, and Y. Zhou, “Memory-safety challenge                  779.
      considered solved? an empirical study with all rust cves,” arXiv          [30] V. Astrauskas, C. Matheja, F. Poli, P. Müller, and A. J. Summers,
      preprint arXiv:2003.03296, 2020.                                               “How do programmers use unsafe rust?” Proceedings of the ACM
[5]   R. Team, “Fix ub due to missing ’static on task::waker,” 2020.                 on Programming Languages, vol. 4, no. OOPSLA, pp. 1–27, 2020.
      [Online]. Available: https://github.com/rust-lang/futures-rs/             [31] E. Reed, “Patina: A formalization of the rust programming lan-
      pull/2206/files                                                                guage,” University of Washington, Department of Computer Science
[6]   M. Baranowski, S. He, and Z. Rakamarić, “Verifying rust programs              and Engineering, Tech. Rep. UW-CSE-15-03-02, p. 264, 2015.
      with smack,” in International Symposium on Automated Technology           [32] D. J. Pearce, “A lightweight formalism for reference lifetimes and
      for Verification and Analysis. Springer, 2018, pp. 528–535.                    borrowing in rust,” ACM Transactions on Programming Languages
[7]   Y. Matsushita, T. Tsukada, and N. Kobayashi, “Rusthorn: Chc-                   and Systems (TOPLAS), vol. 43, no. 1, pp. 1–73, 2021.
      based verification for rust programs,” ACM Transactions on Pro-           [33] A. Weiss, O. Gierczak, D. Patterson, and A. Ahmed, “Oxide: The
      gramming Languages and Systems (TOPLAS), vol. 43, no. 4, pp. 1–54,             essence of rust,” arXiv preprint arXiv:1903.00982, 2019.
      2021.                                                                     [34] R. Jung, J.-H. Jourdan, R. Krebbers, and D. Dreyer, “Rustbelt:
[8]   Y. Matsushita, X. Denis, J.-H. Jourdan, and D. Dreyer, “Rusthorn-              Securing the foundations of the rust programming language,”
      belt: a semantic foundation for functional verification of rust                Proceedings of the ACM on Programming Languages, vol. 2, no. POPL,
      programs with unsafe code,” in Proceedings of the 43rd ACM                     pp. 1–34, 2017.
      SIGPLAN International Conference on Programming Language Design           [35] Coq team, “The coq proof assistant,” https://coq.inria.fr, 2022.
      and Implementation, 2022, pp. 841–856.

                                                                           12
A PPENDIX A                                                             12        }
                                                                        13    }
B UG R EPORTS FROM C RATES
                                                                                  Listing 6: A code smell pattern in wasmi
In Section 5.1.3, we presented the results of running Y UGA
on some of the most frequently downloaded Rust crates.                  The Vec<UntypedValue> on line 2 is converted into a
Here we discuss these results in more detail, with examples:            raw pointer on line 11. Once the Vec is dropped, the raw
                                                                        pointer within the FrameRegisters struct will point to
A.1   Exploitable Bugs:                                                 freed memory. However, all the associated methods of the
Y UGA finds 3 exploitable bugs, 2 from cslice, and 1 from               FrameRegisters struct that dereference this pointer are
bv. We presented one from cslice in the main text; here                 marked unsafe, which means that this vulnerability is not
are both. We have reported these bugs to the developer1 .               exploitable and can only be triggered with unsafe code.
                                                                        Nevertheless, a small change to one of those methods could
 1    pub struct CMutSlice<'a, T> {
 2      base: *mut T, ...
                                                                        break this.
 3    }
 4    pub fn as_slice(&mut self) -> &'a mut [T]
 5    {   unsafe { slice::from_raw_parts(                               A.3   User-implemented Reference Counting
 6                self.base, self.len)} }                               These are cases where the developer has bypassed the
 7
 8    pub fn as_mut_slice(&self) -> &'a [T]
                                                                        Rust lifetime ownership system in favour of implementing
 9    {   unsafe { slice::from_raw_parts_mut(                           their own system of reference counting and memory man-
10                self.base, self.len)} }                               agement. Every time a pointer is duplicated or dropped,
          Listing 4: Two exploitable bugs in cslice                     an internal reference count within the memory location is
                                                                        incremented or decremented. The memory is freed only
   Here is one from bv, that we have reported to the                    if the count has reached zero. If any of these increments,
developer2 .                                                            decrements or checks are omitted, this could result in a use-
 1    impl<'a, Block: BlockType> BitSliceMut<'a, Block> {               after-free or memory leak. Here is an example from dbus.
 2      /// Creates a `BitSliceMut` from a mutable
                                                                         1    pub struct Message {
 3      /// array slice of blocks.
                                                                         2      msg: *mut ffi::DBusMessage,
 4      /// ...
                                                                         3    }
 5      pub fn from_slice(blocks: &mut [Block]) -> Self {
                                                                         4    impl Message {
 6        BitSliceMut {
                                                                         5      pub fn new_method_return(m: &Message) -> Option<Message>{
 7          bits:   blocks.as_mut_ptr(),
                                                                         6        let ptr = unsafe { ffi::dbus_message_new_method_return(m.msg) }
 8          span:   SliceSpan::from_block_len::<Block>
                                                                         7        if ptr.is_null() { None } else { Some(Message { msg: ptr} ) }
 9                                       (blocks.len()),
                                                                         8      }
10          marker: PhantomData,
                                                                         9    }
11        }
                                                                        10    impl Drop for Message {
12      }
                                                                        11      fn drop(&mut self) {
13      ...
                                                                        12        unsafe {
14    }
                                                                        13          ffi::dbus_message_unref(self.msg);
             Listing 5: An exploitable bug in bv                        14        }
                                                                        15      }
                                                                        16    }
    This creates a mutable pointer into the slice, but the slice
itself can be dropped while the pointer is still accessible.                          Listing 7: A code smell pattern in dbus
The lifetime annotation ’a on line 1 is unrelated to the
                                                                        The pointer msg: *mut ffi::DBusMessage is duplicated
anonymous annotation ’_ on line 5.
                                                                        between two different Message structures, but the
    In both the issues that we have filed, we have included
                                                                        duplication increments a reference counter through
code that exploits the vulnerability, verified with Miri[16].
                                                                        ffi::dbus_message_new_method_return,               and      the
                                                                        Drop implementation decrements this counter within
A.2   Freed Pointer but no Deref                                        ffi::dbus_message_unref. This balance ensures that the
These are cases where there is a pointer within a struc-                pointer never becomes invalid while it is still accessible.
ture that is freed, but all the methods that dereference the
pointer are either private or unsafe. A small modification              A.4   Memory copy, not alias
like removing the unsafe label or making the method private
could result in an exploitable vulnerability. This is one such          Y UGA predicts that there could be a vulnerability if two
example from wasmi.                                                     pointers were aliased, however the function actually copies
                                                                        the underlying memory of the first pointer to create the
 1    pub struct ValueStack {
 2        values: Vec<UntypedValue>,
                                                                        target of the second pointer. Here is one such function from
 3        sp: usize,                                                    the napi crate.
 4        max_sp: usize,
 5    }                                                                  1    pub struct $name {
 6    pub struct FrameRegisters {                                        2      data: *mut $rust_type,
 7        ptr: *mut UntypedValue,                                        3      ...
 8    }                                                                  4    }
 9    impl ValueStack {                                                  5    impl $name {
10        pub fn root_stack_ptr(&mut self) -> FrameRegisters{            6      pub fn with_data_copied<D>(data: D) -> Self
11            FrameRegisters::new(self.values.as_mut_ptr())              7      where
                                                                         8        D: AsRef<[$rust_type]>,{
                                                                         9        let mut data_copied = data.as_ref().to_vec();
  1. https://github.com/dherman/cslice/issues/5                         10        let ret = $name {
  2. https://github.com/tov/bv-rs/issues/16                             11          data: data_copied.as_mut_ptr(),

                                                                   13
12               ...                                                     1   pub struct InOutBuf<'inp, 'out, T> {
13            };                                                         2     pub(crate) in_ptr: *const T,
14            mem::forget(data_copied);                                  3     pub(crate) out_ptr: *mut T,
15            ret                                                        4     pub(crate) len: usize,
16        }                                                              5     pub(crate) _pd: PhantomData<(&'inp T, &'out mut T)>,
17    }                                                                  6   }
                                                                         7   impl<'inp, 'out, T> InOutBuf<'inp, 'out, T> {
               Listing 8: A code smell pattern in napi                   8     pub fn into_out(self) -> &'out mut [T]{
                                                                         9       unsafe { slice::from_raw_parts_mut(self.out_ptr, self.len) }
                                                                        10     }
The type D is a reference to a slice of some type $rust_type.           11   }
This underlying memory is then copied by the function
as_ref() on line 9, and a raw pointer to this copied
memory is then transferred into the newly created structure.
Y UGA sees the as_ref() function as opaque, so it thinks                         Listing 10: A code smell pattern in inout
that it is plausible that it is an alias, not a copy. However
this does indicate a need for caution in the future develop-
ment of this code. If the portion .as_ref().to_vec() is
removed from line 9, the memory would not be copied and
this would be an exploitable vulnerability.


A.5   Different field of structure
Y UGA predicts that there could be a vulnerability if two
pointers were aliased, however the aliasing actually hap-                   The structure has two associated LAs, ’inp and ’out,
pens with a different field of a structure. All such examples           corresponding to two raw pointers in_ptr and out_ptr
from Y UGA reports are fairly complicated to describe and in-           within the structure. The raw pointer out_ptr is returned
volve nested structures, nevertheless we attempt to present             as a borrow with annotation ’out. But this is only valid if
one example from the rio crate.                                         the underlying memory actually outlives ’out, and not ’in.
 1    pub struct Uring {                                                This relies on the semantics of the functions that allocate
 2      sq: Mutex<Sq>,                                                  memory for these pointers. In this case, that looks like this:
 3      ...
 4    }
 5    impl Uring {
 6      pub fn connect<'a, F>(
 7              &'a self,
 8              socket: &'a F,
 9              address: &std::net::SocketAddr,
10              order: Ordering,
11          ) -> Completion<'a, ()>                                      1   impl<'inp, 'out, T> From<(&'inp T, &'out mut T)>
12          where                                                        2                         for InOut<'inp, 'out, T> {
13              F: AsRawFd,                                              3     #[inline(always)]
14      ...                                                              4     fn from((in_val, out_val): (&'inp T, &'out mut T))
15    }                                                                  5                                              -> Self {
16    pub(crate) struct Sq {                                             6       Self {
17      khead: *mut AtomicU32,                                           7         in_ptr: in_val as *const T,
18      ...                                                              8         out_ptr: out_val as *mut T,
19      array: &'static mut [AtomicU32],                                 9         _pd: Default::default(),
20    }                                                                 10       }
21    pub struct Completion<'a, C: FromCqe> {                           11     }
22      ...                                                             12   }
23      uring: &'a Uring,
24    }

                Listing 9: A code smell pattern in rio
                                                                        Listing 11: How memory is allocated for the raw pointers
                                                                        from the previous example
Y UGA predicts that there could be a potential vulnera-
bility because *(*(self).sq.0.khead) outlives ’a, and
it might be returned as *(*(ret.uring).sq.0.array),
where it is supposed to live for the entire lifetime of the pro-
gram (’static). There is actually no connection between
these two fields, which means that this is not a vulnerability.
However the types of the two fields match, and it is not
implausible that there could be an incorrect implementation
of this function that connects these two fields, leading to an
exploitable vulnerability.
                                                                        Notice on line 4 that the first borrowed value outlives ’inp
                                                                        and the second value outlives ’out. This is enforced when
A.6   Two Lifetime Annotations                                          the structure is created, and is assumed to be still true when
Here is one example of this pattern from the inout crate. It            the into_out function above is called. Developers must be
was the only one of its kind from the 85 reports that Y UGA             careful to preserve this guarantee in all structure methods
generated.                                                              that manipulate these memory locations.

                                                                   14
A PPENDIX B                                                              But raw pointers break that guarantee. A structure can have
E XTRACTING L IFETIME B OUNDS                                            lifetime annotation <’a>, but the thing pointed to by the
                                                                         raw pointer can live shorter than that. We want to enforce
B.1   Notation
                                                                         these guarantees. We extend our rules as follows:
1) Grammar                                                               • If a structure with no lifetime annotations contains a
Figure 6 are the types that we work with, and lifetime                   raw pointer, then the pointed-at type acts as though it
annotations.                                                             is owned by the structure object (raw-lifetime and
This surface syntax is almost identical to Rust. One impor-              raw-mut-lifetime).
tant difference is that we assume that all borrow lifetimes are          • If a structure with a lifetime annotation <’a> contains a
explicitly specified, whereas Rust allows some lifetimes to              raw pointer, then the data that it points to must outlive ’a
be inferred or elided. Further, we’ve deliberately considered            (raw-owned and raw-mut-owned).
only structures with one lifetime annotation for simplicity,
whereas Rust can have multiple.                                          A PPENDIX C
2) Judgements                                                            C HECKING V IOLATIONS
Figure 7 show the different kinds of judgements. Broadly,                C.1    Arg-Return Use-after-free
we want to process a value of a certain type and extract                 Suppose an argument and return type are of types T1 and T2
values of various subtypes from them. A key point is that                respectively. Then for all L1 , L2 such that T1 → T ′ : L1 and
we abstract away the details of the values themselves, and retain        T2 → T ′ : L2 , if T1 → L1 : L2 is not true, this is potentially
just their type information. So a judgement like T → T ′ : ϵ             Undefined Behavior (UB). In notation,
would be interpreted as “There is a value of type T ′ that
is reachable from the value of type T , and this value is                      T1 → T ′ : L1   T2 → T ′ : L2    T1 ↛ L1 : L2
owned by the parent value”. The actual details of which                                             UB                         uaf1
values these are are irrelevant to our analysis.
                                                                                       T1 → T ′ : L1     T2 → T ′ : ϵ
                                                                                                    UB                  uaf2
B.2   Rules for Decomposing a Type
We want to take a type T and extract all of its contained                   Here we abuse notation by using judgement T1 ↛ L1 :
types with their associated lifetimes. We will do this using             L2 to mean that we cannot extract L1 : L2 from T1 . We
the rules in Figure 8.                                                   do not check if T2 ↛ L1 : L2, because we can only infer
• The simplest case - any owned type contains itself and                 constraints from the arguments we are given. We impose
owns itself (contains-self).                                             constraints on the return types.
• If there is a borrow to an owned type, then it has to live                We report violations to our alias analysis module that
at least as long as the lifetime of that borrow (borrow and              checks if there is actually a transfer of a value of type T ′
mut-borrow).                                                             between T1 and T2 .
• If a structure has a field of type T , then anything that
can be extracted from that T can also be extracted from the              C.2    Arg-Arg Use-after-free
structure (field and field-eps).                                         Suppose two arguments are of types T1 and T2 . Then, the
• If an extracted type already has an associated lifetime,               rules for checking Arg-Arg Use-after-free violations are:
then any outer borrow lifetime does not attach to it
(inner-lifetime).                                                         T1 → T ′ : L1    T2 → T ′ : L2    T1 ↛ L1 : ’static
• Any outer borrow lifetime must be shorter than an inner                                           UB                            uaf3
borrow lifetime (B-inner-longer).
• We can always conclude that a lifetime outlives itself
                                                                             Any non-static lifetime being assigned to another life-
(B-reflexive).                                                           time, between matching types, gets flagged as a violation,
                     3
• The static lifetime always outlives any other lifetime
                                                                         to be taken care of by the alias analyzer.
(B-static).
• Lifetime bounds can also be extracted from inner types
                                                                         C.3    Arg-Return Non-Exclusive Mutability
(B-extract-inner1 and B-extract-inner2).                                 Suppose an argument and return type are of types T1 and
                                                                         T2 respectively. Then, the rules for checking Non-Exclusive
B.3   In the Presence of Raw Pointers                                    Mutability (NEM) violations are:
In an ideal world, we want a structure’s annotation to be
representative of what it holds.                                          T1 → T ′ : L1    T2 → &mut T ′ : L2      T1 ↛ L1 : L2
                                                                                                    UB                            nem1
• If a structure is annotated with lifetime <’a>, then we
would like everything accessible from the structure to out-               T1 → T ′ : L1    T2 → *mut T ′ : L2      T1 ↛ L1 : L2
live ’a.                                                                                            UB                            nem2
• If a structure has no lifetime annotation, then we would
like everything accessible from the structure to be owned by              T1 → *mut T ′ : L1     T2 → T ′ : L2     T1 ↛ L1 : L2
                                                                                                    UB                            nem3
the structure object.

   3. https://doc.rust-lang.org/rust-by-example/scope/lifetime/           T1 → &mut T ′ : L1      T2 → T ′ : L2    T1 ↛ L1 : L2
static lifetime.html                                                                                UB                            nem4

                                                                    15
                   T :: &L mut T                                                A mutable borrow to some type
                       | &L T                                               An immutable borrow to some type
                       |O                                                        A structure or a primitive type
                       | *const | *mut                                    (Im)mutable raw pointer to some type
                   O :: S                                   A struct or primitive type not containing borrows
                       | S <L>                                                     A struct containing borrows
                   L :: ’id | ’static                                                           Lifetime names
                   S :: id                                                                     Identifier names

                                                  Fig. 6: Our grammar for types


                    O{T }                                  “O contains a value of type T as one of its fields”
                    T → T′ : L                          “T contains another type T’ that outlives lifetime L”
                    T → T′ : ϵ                                             “T contains another owned type T ′ ”
                    T → L1 : L2                             “From T , we can infer that L1 is longer than L2 ”

                                                         Fig. 7: Judgements


                                                    T → T1 : ϵ                           T → T1 : ϵ
                      contains-self                             borrow                                  mut-borrow
          O→O:ϵ                                    &LT → T1 : L                       &L mut T → T1 : L

    O{T } T → T1 : L                      O{T } T → T1 : ϵ                          T → T1 : L1
                     field                                 field-eps                             inner-lifetime
       O → T1 : L                            S → T1 : ϵ                            &LT → T1 : L1

        S{*const T }                           S{*mut T }                              S <L>{*const T }
                     raw-owned                            raw-mut-owned                                 raw-lifetime
         S→T :ϵ                                S→T :ϵ                                    S <L> → T : L
     S <L>{*mut T }                                    T → T1 : L1
                    raw-mut-lifetime                               B-inner-longer                             B-reflexive
     S <L> → T : L                                    &LT → L1 : L                                T →L: L
                                                               T → T1 : L T1 → L1 : L2
                                      B-static                                         B-extract-inner1
                 T → ’static : L                                    T → L1 : L2
                                        T → T1 : ϵ T1 → L1 : L2
                                                                B-extract-inner2
                                             T → L1 : L2

Fig. 8: Rules for Extracting Lifetime Relationships. The first 6 rules deal with derivation of type-lifetime relationships for
borrows and structures; the next 4 (starting with raw-) are a generalization of the type-lifetime rules for borrows, to raw
pointers; the next 5 (starting with B-) deal with the calculation of implicit lifetime-lifetime relationships.


   Again, we report violations to our alias analysis module
that checks if there is actually a transfer of a value of type T ′
between T1 and T2 .




                                                                     16
A PPENDIX D
A LIAS A NALYSIS
This section describes our alias analysis in more detail. For a
variable a, we denote its
                       S points-to set by Sa . For dereferenc-
ing, we define ∗Sa = x∈Sa Sx . We process each statement
in order, and for each type of assignment statement, like a
= b, a = *b, etc, we update the points-to sets accordingly.
If there is a function call, then we consider all possible
kinds of assignments and dereferences between the function
arguments, like arg1 = *arg2, **arg1 = arg2, etc. The
pseudocode is shown in Algorithm 1. Note that this is a
simplified version that does not include field sensitivity. For
the full algorithm, please refer to our code on GitHub.

Algorithm 1 Alias Analysis
 1   input: body
 2   input: source, target
 3
 4   source_val := alloc()
 5   Ssource := { source_val }
 6
 7   for basic_block in reverse_postorder(body):
 8       for statement in basic_block.statements:
 9           match statement
10               [a = b] =>
11                   Sa := Sa ∪ Sb
12
13               [*a = b] =>
14                   if Sa is empty:
15                       Sa := { alloc() }
16                   for x ∈ ∗Sa :
17                       Sx := Sx ∪ Sb
18
19               [a = *b] =>
20                   if Sb is empty:
21                       Sb := { alloc() }
22                   for x ∈ ∗Sb :
23                       Sa := Sa ∪ Sx
24
25               [a = &b] =>
26                   Sa := Sa ∪ { b }
27
28               [ret = f(args)] =>
29                   for a, b ∈ choose(args, 2):
30                       for x ∈ (Sa ∪ ∗Sa ∪ ∗ ∗ Sa ...):
31                            for y ∈ (Sb ∪ ∗Sb ∪ ∗ ∗ Sb ...):
32                                 Sx := Sx ∪ Sy
33                                 Sy := Sx ∪ Sy
34                   for a in args:
35                       Sret := Sret ∪ Sa ∪ ∗Sa ∪ ∗ ∗ Sa ...
36
37   if source_val ∈ Starget :
38       return True // May Alias
39   else:
40       return False // Not Aliased




                                                                  17
A PPENDIX E                                                              1   impl<'a, K, V> Iterator for IterMut<'a, K, V> {
S HALLOW F ILTER                                                         2     type Item = (&'a K, &'a mut V);
                                                                         3
In this section, we describe some details about our shal-                4       fn next(&mut self) -> Option<(&'a K, &'a mut V)> {
                                                                         5         // Returns a reference to value at index
low filter. This is based on some primitive inter-procedural             6         // Moves pointer ahead by 1
analysis, as well as knowledge of common patterns of false               7       }
positives.                                                               8   }
                                                                        Listing 13: An example from lru showing a common pat-
E.1   Filter based on Drop Implementations                              tern of false positive.
Consider the hypothetical function to_bar shown in Listing
12.
 1    pub struct Foo {                                                  moves to the next value and there is no way to “rewind”
 2        data: *const i32                                              the iterator to point back to the previous value. If we had
 3    }                                                                 another function rewind() that moves the pointer back
 4    pub struct Bar {
 5        data: *const i32                                              by one entry, then we could use rewind() and next()
 6    }                                                                 together to create two aliased mutable references as follows:
 7    impl Foo {
                                                                         1   let (k1, v1) = iter.next();
 8        pub fn new(val: i32) -> Foo {
                                                                         2   iter.rewind(); // Moves pointer back by 1
 9            Foo{data: Box::leak(Box::from(val))}
                                                                         3   let (k2, v2) = iter.next();
10        }
                                                                         4   // v1 and v2 would be aliased mutable references
11        pub fn to_bar(&self) -> Bar {
12            Bar{data: self.data}
                                                                            However the rewind() function doesn’t exist, and so
13        }
14        pub fn get_val(&self) -> &i32 {                               the next() function can always be called safely. There is no
15            unsafe{&*self.data}                                       way to predict this without reasoning about the semantic
16        }                                                             properties of the code.
17    }
                                                                            The Iterator trait is implemented for different types in
Listing 12: Example to illustrate filtering based on absence            many crates, and in each of these, the next function bears
of Drop implementations.                                                a similar signature and implementation semantics. Y UGA
                                                                        flags this as a potential violation in several of these cases.
Consider the function to_bar. Our analysis would derive
                                                                        To remedy this problem, our shallow filter simply ignores
that self.data must outlive the anonymous lifetime on
                                                                        implementations of Iterator::next altogether.
&self, and when it is transferred over to the returned Bar
                                                                            There are three specific functions from trait im-
structure, it is valid for as long as the receiver (the function
                                                                        plementations that we filter out - Iterator::next,
caller) holds on to it. This would be marked as a potential
                                                                        Iterator::next_back, Clone::clone. It is true that
error, because our analysis cannot assume that self.data
                                                                        there can be potential flaws in these implementations, which
will be valid for the entire lifetime of the program. However,
                                                                        is why the shallow filter is the last stage of our analysis, and
in this program, that memory is leaked and doesn’t ever
                                                                        a user has the option of turning it off.
get freed. A memory leak is not considered an exploitable
vulnerability or undefined behavior in Rust.
Hence we implement a simple inter-procedural check. If the
value being re-assigned is behind a raw pointer in both
the source as well as the target structures, then we only
mark this as a violation if either of those structures has a
custom Drop implementation. A custom Drop implementa-
tion would usually involve cleaning up memory, and this
means that when that structures gets dropped, the data
value might be freed.

E.2   Filter Common Patterns of False Positives
There are certain common traits in Rust that rely on the
semantic correctness of their implementation to ensure their
safety. One such example is the IteratorMut trait, specif-
ically its next and next_back methods [23]. Listing 13
shows an example from the lru crate.
    This is a mutable iterator which allows mutable access to
the elements of a cache. The lifetime of the returned value
(&’a mut V) and the lifetime of &mut self are unrelated,
which means that it is possible to call next() multiple times
to get multiple mutable references to elements of the cache.
However, the semantics of the function ensure that each
of these returned references always points to a different
cache element. Once a value has been returned, the iterator

                                                                   18
