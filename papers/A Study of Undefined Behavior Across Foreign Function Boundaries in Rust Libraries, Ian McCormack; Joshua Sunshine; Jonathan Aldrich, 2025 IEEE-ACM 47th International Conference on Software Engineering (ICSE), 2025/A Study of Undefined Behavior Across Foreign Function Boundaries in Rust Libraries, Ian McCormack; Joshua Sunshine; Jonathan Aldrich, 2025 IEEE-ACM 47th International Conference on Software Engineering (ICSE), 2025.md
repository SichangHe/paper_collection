                                             A Study of Undefined Behavior Across Foreign
                                                 Function Boundaries in Rust Libraries
                                                        Ian McCormack                            Joshua Sunshine                              Jonathan Aldrich
                                                   Carnegie Mellon University              Carnegie Mellon University                  Carnegie Mellon University
                                                      Pittsburgh, PA, USA                     Pittsburgh, PA, USA                          Pittsburgh, PA, USA
                                                     icmccorm@cs.cmu.edu                     sunshine@cs.cmu.edu                       jonathan.aldrich@cs.cmu.edu



                                           Abstract—Developers rely on the static safety guarantees of         •   RQ1: What types of errors occur in Rust libraries that
                                        the Rust programming language to write secure and performant
arXiv:2404.11671v8 [cs.SE] 2 Apr 2025




                                                                                                                   call foreign functions?
                                        applications. However, Rust is frequently used to interoperate
                                        with other languages which allow design patterns that conflict       The Rust community has proposed two aliasing models:
                                        with Rust’s evolving aliasing models. Miri is currently the only     Stacked Borrows [9] and Tree Borrows [10]. The goal of
                                        dynamic analysis tool that can validate applications against these   these models is to "strike a balance" [9] between performance
                                        models, but it does not support finding bugs in foreign functions,   and usability by providing a set of rules that developers must
                                        indicating that there may be a critical correctness gap across the
                                        Rust ecosystem. We conducted a large-scale evaluation of Rust
                                                                                                             follow to ensure that compile-time optimizations are applied
                                        libraries that call foreign functions to determine whether Miri’s    correctly [11]. Since Stacked Borrows and Tree Borrows both
                                        dynamic analyses remain useful in this context. We used Miri         provide rules of this kind, we ask a second research question:
                                        and an LLVM interpreter to jointly execute applications that
                                                                                                               •   RQ2: Which of Rust’s aliasing models permits more real-
                                        call foreign functions, where we found 46 instances of undefined
                                        or undesired behavior in 37 libraries. Three bugs were found               world programs with foreign function calls?
                                        in libraries that had more than 10,000 daily downloads on            To answer these questions, we created MiriLLI: a tool which
                                        average during our observation period, and one was found in          combines Miri with an LLVM interpreter to jointly exe-
                                        a library maintained by the Rust Project. Many of these bugs
                                        were violations of Rust’s aliasing models, but the latest Tree       cute programs and detect undefined behavior across foreign
                                        Borrows model was significantly more permissive than the earlier     function boundaries. We used MiriLLI to conduct a large-
                                        Stacked Borrows model. The Rust community must invest in             scale study of 9,130 test cases from 957 Rust libraries that
                                        new, production-ready tooling for multi-language applications to     call foreign functions. We identified 46 unique instances of
                                        ensure that developers can detect these errors.                      undefined or undesirable behavior from 37 libraries. Of the
                                           Index Terms—Rust, interoperation, undefined behavior, alias-
                                        ing, bugs, foreign functions                                         90 test cases that violated Stacked Borrows, 66% (59) did not
                                                                                                             violate Tree Borrows.
                                                                                                                Our results indicate that Rust’s restrictions on aliasing,
                                                              I. I NTRODUCTION
                                                                                                             mutability, and initialization make it easy to inadvertently
                                           The Rust programming language has become increasingly             introduce undefined behavior when calling foreign functions.
                                        popular due to its static safety guarantees, which provide           Developers can take immediate steps to avoid these errors by
                                        security benefits comparable to garbage collection without           auditing their use of certain types at foreign callsites. However,
                                        additional run-time overhead [1], [2]. However, Rust is also         the Rust Project must invest in new, production-ready tooling
                                        frequently used in interoperation with languages that do not         to ensure that these errors can be easily detected.
                                        provide similar assurances. To call foreign functions, devel-             Overview: In Section II, we compare Rust’s semantics
                                        opers must use a subset of unsafe features to bypass Rust’s          with C and C++, and we describe the resources and best
                                        restrictions. If these features are used incorrectly, they can       practices that Rust developers use to interoperate with these
                                        break Rust’s aliasing rules. The Rust compiler relies on these       languages. In Section III, we document our methodology for
                                        rules to optimize code. If they are broken, optimizations            sampling and evaluating test cases from Rust libraries that
                                        may be applied incorrectly, which can introduce security             call foreign functions, and we describe the challenges that
                                        vulnerabilities.                                                     we encountered when implementing MiriLLI. In Section IV,
                                           Miri [3] is a widely-used Rust interpreter that uses dy-          we describe each type of bug that we found. We discuss the
                                        namic analysis to detect violations of Rust’s aliasing model.        implications of our findings in Section V. We review prior
                                        A limitation of Miri is that it cannot detect these errors           work on Rust interoperation in Section VI, we discuss threats
                                        across foreign function boundaries. However, one of the most         to validity in Section VII, and we conclude in Section VIII.
                                        common reasons for using Rust’s unsafe features is to call           Our dataset, the Appendix, and the source for MiriLLI are
                                        foreign functions [4], [5], [6], [7], [8]. We seek to determine      available in our replication package1 .
                                        whether the differences between Rust and other languages are
                                        leading to errors in practice.                                         1 https://doi.org/10.5281/zenodo.12727039
                      II. BACKGROUND                                     Fig. 1: Minimal examples of the categories of Stacked and
   Rust’s safety restrictions begin at the level of a value, which       Tree Borrows violations that we observed in our evaluation.
is valid for a particular scope. A value’s type implements traits        Statements that trigger undefined behavior are highlighted in
that define how it behaves. For example, all types have move             red.
semantics by default, meaning that each value has a unique               (a) A minimal example of an expired permission error. The table on
owner. However, values with the Copy trait have no owner and             the righthand side shows the tree of permissions for the local variable
can be freely duplicated. Ownership can be transferred through           x before and after writing with y on line 5.
assignment or borrowed by creating a reference. References
                                                                           1   let mut x = 0;                            Active           x
are either mutable, taking the form &mut T, or immutable,                  2   let y = &mut x;
                                                                           3   let y = y as *mut _;           Reserved    →     Active     y
with the form &T. Mutable references have move semantics,                                                     Reserved    → Disabled       z
                                                                           4   let z = &mut x;
but immutable references can be copied. Each reference has                 5   unsafe { *y = 1; }
a lifetime, which is the portion of the program over which it              6   *z = 0;
will be used. Rust’s borrow checker statically enforces that the               (b) A minimal example of an insufficient permission error.
lifetime of a reference must not exceed the scope or lifetime
of the value that it borrows. A value can have a single mutable            1   let x = 0;
                                                                           2   ub(&x);
reference or many immutable references that are active within              3   fn ub(x: *const u8) {
a given context [12], but not both at the same time.                       4    let x = x as *mut _;
                                                                           5    unsafe { *x = 1 };
   These restrictions prevent safety issues, but they can also             6   }
make it impossible to implement certain design patterns. When
                                                                                (c) A minimal example of a protected permission error.
developers need to bypass Rust’s restrictions, they can use the
unsafe keyword to enable a set of additional features that are             1   unsafe fn free(x: &mut u8, layout: Layout) {
not restricted by the borrow checker. These features include               2     dealloc(x as *mut _, layout);
                                                                           3   }
dereferencing raw pointers, accessing the fields of union types,
modifying static mutable state, implementing unsafe traits,              (d) A minimal example of an access out-of-bounds error under
and calling unsafe functions—including those written in other            Stacked Borrows that is accepted under Tree Borrows.
languages [13]. The Rust compiler can assume that programs                 1   let x: &mut i32 = &mut (0, 0).0;
that use unsafe code will follow the rules of its aliasing model.          2   let x = (x as *mut i32).offset(1);
                                                                           3   unsafe { *x = 1 };
Programs that violate these rules have undefined behavior, so
they may be optimized incorrectly. This can lead to differences
in behavior that can cause security vulnerabilities [14] in
practice.
                                                                         of the model). Using one of these expired permissions is
A. Rust’s Aliasing Model                                                 undefined behavior. We provide a minimal example of this
   Rust developers can avoid these issues by ensuring that               in Figure 2, where the variable x is mutably borrowed twice;
their programs adhere to the rules of Rust’s aliasing model.             once by y and again by z. However, we also store a copy
The Tree Borrows [10] model provides the latest definition of            of y as a raw pointer (*mut). Rust’s borrow checker does
these rules. Under this model, each pointer has provenance that          not place aliasing restrictions on raw pointers, so it assumes
determines its permission to read or write to a location [15].           that z has exclusive, mutable access from when it is created
Each location is associated with a tree that tracks all valid per-       on line 4 until it is used on line 6. Writing through y on
missions to its contents. When a location is borrowed, a branch          line 5 breaks this assumption, so writing through z is now
is created in the tree that holds a new permission to access             undefined behavior. In terms of the model, the permissions
the location. When a pointer is used, its permission is checked          for y and z are children of the permission for x. Both receive
against the tree to ensure that it is valid and that it permits          a Reserved permission, which has the capability to become a
the kind of access that takes place. Each type of access will            unique Active permission for writing to x. When a Reserved
have a different effect on the tree depending on the position of         permission is used for a write access, it becomes an Active
each permission in the tree relative to the permission used for          permission, and all foreign Reserved permissions become
the access. With respect to a given permission, an access is             Disabled, canceling their reservations. Since z is adjacent to
considered a child access if it requires that permission or any          y, the write on line 5 is a foreign access.
of its descendants; otherwise, it is a foreign access. Accessing            The second category of undefined behavior is an insufficient
a location using an invalid permission is undefined behavior.            permission error. This type of error occurs when a reference
   There are three categories of aliasing violations under Tree          or pointer with a read-only permission is used to write to
Borrows that we observed in our investigation. Figure 1                  memory. This occurs in Figure 1b on line 5, where the function
provides minimal examples of each one. We refer to the first             ub writes through a pointer that was cast from an immutable
category as an expired permission error. Under Tree Borrows,             reference (&x) on line 2. Under Tree Borrows, this reference
writing to a memory location may cause other permissions                 is given a Frozen permission, which is read-only. Casting a
to that location to expire (or transition to Disabled, in terms          reference into a raw pointer does not change its permission,



                                                                     2
and neither does casting a pointer between const and mut.                  2) Aliasing & Mutability: Neither C nor C++ statically
   The third type of undefined behavior that we observed                restricts aliasing, but the standards for each language allow
is a protected permission error. We provide an example in               implementations to make type-directed assumptions about
Figure 1c, where the function free receives a mutable refer-            aliasing. In both languages, it is considered undefined behavior
ence. This reference encodes the promise that ownership will            for a pointer to one type to refer to a value of another
eventually be returned to the caller. However, this promise is          type if the two types differ.3 However, differences do not
broken when the reference is cast into a raw pointer and used           include qualifiers, so two parameters of types int * and
to free the underlying allocation. In terms of Tree Borrows,            const int * can alias.
when a reference-type value is passed as an argument to a                  In Rust, both variables and references have distinct, con-
function, it becomes protected, making it undefined behavior            nected capabilities for mutation. Variables are immutable by
for it to transition to Disabled—even if it is never accessed           default, only mutable variables can be mutably borrowed, and
after this point. When a function returns, the permissions of           only mutable references can be used for mutation. In C and
its arguments are no longer protected.                                  C++, variables are mutable by default, and the capability to
   1) Differences from Stacked Borrows: Tree Borrows re-                mutate memory is determined by the mutability of the object
places the Stacked Borrows [9] model, which uses a stack to             being pointed to, regardless of the pointer’s type.4 If a variable
track the active permissions to each location. Under Stacked            was declared as mutable, then a const pointer can be cast into
borrows, a reference cannot be offset and used to access                a mutable pointer and used to write to it.
locations outside of the range it originally borrowed. Figure 1d           3) Provenance: Both C and C++ allow pointers to be
shows an example of this access out-of-bounds error; the                converted to and from integers with a size equal to the word
dereference on line 3 is invalid, since x only borrowed the             size of the current architecture.5 Implementations may track
first element of the tuple. This pattern is allowed under Tree          the provenance, or origin of pointers to inform compile-time
Borrows; a valid permission can be used to access any location          optimizations [19]. However, neither of the current standards
within the bounds of its allocation. Tree Borrows also delays           for C or C++ defines if or how provenance should be preserved
asserting that the permission of a reference is valid until it is       across these conversions, though several models have been
used for the first time, whereas Stacked Borrows asserts that a         proposed [20]. Rust’s pointers have provenance [15], but the
reference is valid immediately when it is created. However,             specifics of Rust’s provenance model are undecided.
Tree Borrows is less permissive than Stacked Borrows for                   Miri has multiple methods for handling provenance across
certain aliasing patterns due to the semantics of its Reserved          pointer-to-integer conversion. By default, when a pointer is
permission, justifying our second research question.                    converted to an integer, its tag is added to a set of tags
B. Rust vs. C and C++                                                   that have been “exposed” by pointer-to-integer conversion.
                                                                        When integers are converted back into pointers, their allocation
   Rust shares several other categories of undefined behavior           identifier is reconstructed from their address, but they receive
with current C [16] and C++ [17] standards, such as accessing           a “wildcard” provenance value [21]. Under Stacked Borrows,
memory that has been freed, accessing beyond the bounds                 when a memory access occurs using a wildcard tag, Miri
of an allocation, creating a data race, reading uninitialized           eagerly interprets it as being equivalent to any tag in the stack
memory, and accessing a value at an unaligned address [18].             that permits the access. The current implementation of Tree
However, C and C++ have different rules related to initial-             Borrows does not support this behavior yet; all accesses with
ization, aliasing, and mutability that may conflict with Rust’s         wildcard tags are allowed and do not affect the state of the
expectations.                                                           tree. Alternatively, developers can enable strict provenance,
   1) Initialization: In both C and C++, accessing an unini-
                                                                        which treats integer-to-pointer conversion as an error.
tialized object produces an “indeterminate value”, which is
undefined behavior.2 However, there are a few exceptions.               C. Interoperation
Static and thread-local variables are initialized immediately at           Developers can access foreign functions and static variables
the beginning of their lifetime, and both the unsigned char             using Rust’s foreign function interface. Declarations, or “bind-
and byte types are allowed to store indeterminate values. It            ings,” for each of these objects are written in extern blocks,
is also safe to create a reference to an uninitialized value.           which take an optional qualifier to indicate the Application
   Rust’s borrow checker prevents variables from being used             Binary Interface (ABI) used by the foreign library. Developers
until they are initialized, and no primitive types tolerate             can also use the extern keyword to change the ABI of a
indeterminate values in safe contexts. However, Rust’s stan-            function defined in Rust so that it can be called from other
dard library provides MaybeUninit<T>, which represents                  languages. Only a subset of Rust’s types are guaranteed to be
an instance of T that may or may not be initialized. Once               compatible with foreign ABIs. Both structs and enums must
an instance has been fully initialized, the unsafe function             be annotated with the #[repr(C)] attribute to ensure that
MaybeUninit<T>::assume_init will unwrap the outer                       their layout is compatible with C. Bindings are not validated
struct to produce the value inside. It is undefined behavior
                                                                          3 C23 §6.5.7; C++23 §7.2.1.11
to call assume_init if T is not fully initialized.
                                                                          4 C23 §6.7.4.1.7; C++23 §9.2.9.2.3
  2 C23 §6.2.4.6-7; C++23 §6.7.4.1                                        5 C23 §6.3.2.3.5-6; C++23 §6.7.1.10.4-5




                                                                    3
against their definitions, but tools such as bindgen [22] and             3% (3,785) of crates with both unit tests and LLVM bitcode.
CXX [23] can automatically generate bindings from headers.                Then, we used an unmodified version of Miri to execute all of
   Several dynamic analysis tools can find undefined behavior             the unit tests from this subset of crates to determine which tests
in multi-language Rust applications. Valgrind [24] is capable             called foreign functions. Of the 88,637 tests that we identified,
of detecting spatial and temporal memory errors, as well as               53% (47,189) passed, 41% (36,766) failed, 4% (3,869) timed
incompatibilities with size and alignment. Many of the LLVM               out after five minutes, and 1% (1,178) had been manually
Project’s sanitizers are also compatible with Rust [25]. Each             disabled. Tests can be disabled using the #[ignore] attribute
of these tools is available as a plugin for Cargo, Rust’s build           or with conditional compilation directives.
tool. Miri can call foreign functions from natively compiled                 Of the tests that failed in Miri, 63% (23,116) failed due
shared libraries using libffi [26], but it does not support passing       to foreign function calls. We executed this subset under both
certain argument types to native functions, and it cannot find            Stacked and Tree Borrows using an initial build of our tool
undefined behavior that is triggered in foreign code.                     to determine which tests called foreign functions. Of all
                                                                          potentially viable test cases, 39% (9,130) called a foreign
                     III. M ETHODOLOGY                                    function we could execute. These tests originated from 25%
   We seek to determine whether the differences between Rust              (957) of the crates with both test cases and bitcode. Our
and other languages lead to undefined behavior in practice.               sample only includes crates that statically link to foreign code
First, we analyzed all libraries published on crates.io—Rust’s            in their default configuration; it does not include crates that
central package repository—to find the subset with test cases             default to dynamic linking or statically link in non-default
that produce LLVM bitcode for C or C++ libraries during their             configurations. However, the 957 crates that we identified were
build process. We describe this stage in Section III-A. Then,             more than enough to find meaningful answers to our research
we created MiriLLI, which can run these test cases and detect             questions. We used this sample to conduct our final evaluation.
undefined behavior. MiriLLI extends Miri to interoperate with                We also partially measured the distribution of crates that
LLI [27], an LLVM interpreter. Both Miri and LLI are included             interact with foreign code. When we compiled each crate, we
within the Rust toolchain; LLI is part of the LLVM backend.               used an early lint pass to examine the abstract syntax tree
MiriLLI uses each interpreter to jointly execute programs                 and record the locations of all function declarations with a
defined across LLVM’s intermediate representation (LLVM                   foreign ABI. We used data from this pass to identify 2,516
IR) and Rust’s mid-level intermediate representation (MIR).               crates that declared a foreign function. This represents only
In Section III-B, we outline the architecture of our tool and             2.1% of all valid crates. However, 12,564 (10.4%) of all valid
describe how we resolved the differences in semantics between             crates had a version that directly depended on at least one prior
each interpreter. In Section III-C, we describe our method                version of a crate that declared a foreign function binding. The
for deduplicating test results to identify unique instances of            maximum number of dependents for any crate that declared
undefined behavior and our approach to reporting bugs.                    foreign functions was 6,411, with a mean of 11.0 dependents
                                                                          and a standard deviation of 171.8 dependents.
A. Sampling
   We evaluated our design on all compatible Rust libraries               B. Implementation
with test cases that called foreign functions. Rust libraries are            We illustrate the data flow between each of the core com-
referred to as “crates,” and they can be published at crates.io.          ponents of MiriLLI in Figure 2. As indicated at the bottom
We used a snapshot of the crates.io database taken on Septem-             of the Figure, MiriLLI requires Clang [28] to be set as the
ber 20th, 2023. It contained 125,804 unique crates, of which              default C and C++ compiler and configured to emit LLVM
96% (121,015) had at least one valid published version. We                bitcode during the build process for the library under test.
compiled each crate using version 1.74 (nightly-2023-09-25)               Other than this requirement, using MiriLLI is identical to using
of the Rust toolchain, matching the version used by MiriLLI.              an unmodified version of Miri.
This was necessary to ensure that we could use an unmodified                 When MiriLLI encounters a foreign function call in a Rust
version of Miri as a control to identify tests that would                 program, it looks for a corresponding definition in the LLVM
normally fail due to lack of support for foreign function calls.          module. After finding a definition, the function’s arguments
It would have been infeasible to maintain separate versions               are passed through a translation function, which lowers them
of MiriLLI for multiple toolchains without compromising the               into the representation used by LLI. There are two translation
consistency of our results, since Miri depends on APIs that               functions indicated by the arrows in the middle of Figure 2;
changed significantly throughout our evaluation. There is no              one from Miri’s representation to LLI’s (left) and another from
standard method for using a version of Miri compiled with                 LLI’s representation to Miri’s (right). Miri passes the translated
one toolchain to execute programs compiled with another                   arguments to LLI, which creates a new thread to execute the
toolchain, and there is no guarantee that Miri would behave               function. Then, Miri sets the current current Rust thread to join
as expected under these conditions.                                       on this new LLVM thread. After the LLVM thread terminates,
   Of all valid crates, 67% (84,106) compiled without inter-              its return value is passed back through the translation layer
vention. Of the crates that compiled, 36% (44,661) had unit               and given to the Rust thread, which continues to execute.
tests and 9% (11,120) produced LLVM bitcode files, leaving                A similar process is used when an LLVM thread calls a



                                                                      4
             Fig. 2: The architecture of MiriLLI.                       we could not rely on a function’s definition to have the same
                                                                        signature as its binding. However, foreign function bindings
                                                                        are also allowed to be incorrect, so we could not wholly trust
            Rust          Rust Compiler             Rust
           Source                                   MIR                 type information to guide our conversion, either. Additionally,
                                                                        neither Rust nor LLVM has a formal model of its ABI that
                                                                        we could use as an oracle. When implementing our value
                        Memory                                          translation functions, we settled on a conservative approach
                                           Thread
             Miri                                                       that supports the most common ABI differences while still
                         Shims            Manager
                                                                        being able to detect certain instances of incorrect bindings.
                                                                        We maintain the invariant that the size of a typed value on
                    Value Translation Functions
                                                                        one side of the boundary must be equal to the size of the type
                    Foreign Function Interface                          expected by the other side. We provide a formal model of
                                                                        our value conversion functions in Section 2 of the Appendix.
                                                                        It demonstrates that conversion will fail when a difference in
             LLI            LLVM Thread State                           size is detected, which we report as undefined behavior.
                                                                           Conversion is trivial for primitive types, since they have
                                                                        a canonical representation in Rust and LLVM. We also al-
                                                                        low implicit casts between pointers and integers at foreign
           C/C++              Clang               LLVM
           Source                                   IR                  boundaries, which was necessary for 526 test cases from
                                                                        70 crates. When aggregate types are passed by value, we
                                                                        require both the size and number of fields to match unless
                                                                        the aggregate is passed as an integer or by reference. However,
Rust function. Although Miri is single-threaded, it supports            we also frequently observed functions that expected individual
concurrency by non-deterministically stepping through multi-            aggregates to pass through multiple parameters, with one pa-
ple simulated “threads” of execution. LLI did not originally            rameter for each field. This occurred only with homogeneous
support any form of multithreading, but we modified it to be            aggregates, where every field is identical and lacks padding.
compatible with Miri’s implementation. We support calling               To accommodate this, we treat each field in a homogeneous
foreign functions from parallel Rust threads, but we do not             aggregate as a separate argument if the entire aggregate cannot
support multithreading within LLVM. We implemented the                  be passed as a single parameter. We apply this transformation
Rust interface to LLI as an extension of Inkwell: a high-level          only if the number of fixed parameters is greater than or equal
Rust encapsulation for LLVM [29].                                       to the number of remaining arguments plus the number of
   Nearly all of Miri’s mechanisms for detecting undefined              fields in the aggregate. This was necessary for 2% (156) of
behavior are built into the core functions of the interpreter           our test cases from 15% (140) of crates.
and do not require additional instrumentation of the source                Products lack a canonical form between Rust and LLVM,
program. However, to detect aliasing violations, Miri config-           so we do not support passing them as variadic arguments
ures the Rust compiler to insert “retag” instructions, which are        to LLVM or as arguments from LLVM to Miri’s shims for
used by its implementations of Stacked and Tree Borrows. We             system calls. Each of these types of functions lacks the type
did not need to insert these instructions into the LLVM IR of           information that we need to guide our conversion. When an
foreign functions, since we treat LLVM pointers as equivalent           opaque pointer from LLVM is passed to one of Miri’s shims,
to Rust’s raw pointers.                                                 we assign it the type *mut u8. However, if it points to stack or
   We enabled LLI to detect undefined behavior by replacing             static memory with a size equal to that of a primitive type, we
several of its core operations with foreign function calls that         assign it to point to that type. This may lead to false positive
use Miri to execute equivalent operations. As indicated by the          alignment errors when we cannot resolve an underlying type,
labels next to “Miri” in Figure 2, all operations related to            and Rust expects a type other than u8.
managing threads, accessing memory, and executing “shim”                      b) Initialization: Miri tracks which bits are initialized
implementations of intrinsics and system calls are handled              in each allocation and reports an error when uninitialized
by Miri—for both interpreters. LLI manages its own local                memory is read. However, LLVM will read uninitialized
state for LLVM threads and implements the interpretation                memory for the purpose of propagating undef and poison
functions for each instruction, but Miri controls the process of        values, which represent the result of an indeterminate or
taking a step for each thread. This architecture allowed us to          invalid computation. If a single bit needs to be set within an
extend Miri to detect errors in foreign function calls “for free”       uninitialized byte, instead of writing a zeroed byte with the
without having to reimplement its dynamic analyses within               individual bit set, LLVM will load the uninitialized byte, set
LLI. However, we had to address two additional difficulties to          only that bit, and then write it back [30], [31]. These accesses
increase test coverage.                                                 are considered undefined behavior by Miri, but we treat them
     a) Translation: Rust’s MIR uses different calling con-             as false positives. We implemented two modes that allow us
ventions and represents values differently than LLVM IR, so             to identify true positive uninitialized reads of Rust-allocated



                                                                    5
memory in LLVM. By default, we allow load instructions                  outcomes based on exit codes, stack traces, and error logs to
to read uninitialized bytes. However, MiriLLI can also be               avoid filing redundant bug reports. Prior to deduplication, we
configured to treat uninitialized reads as errors while zero-           modified the error logs to remove unnecessary elements, such
initializing all LLVM-allocated stack and heap memory. Tests            as references to specific memory addresses. We also included
that read uninitialized memory must be run in each mode to              more or less detail in stack traces, depending on the location
ensure a complete evaluation. We cannot detect true positive            of an error. For foreign errors, we used the subset of the stack
uninitialized reads that occur outside of interactions with Rust,       trace up to the Rust boundary to avoid deduplicating errors
but these errors can be found with other tools [24], [32] and           that appeared to be identical but were caused by mistakes at
are beyond the scope of our evaluation.                                 different callsites. When an error occurred in Rust, we only
                                                                        used the first line of the stack trace, since few of these errors
C. Evaluation                                                           were caused by LLVM.
   We used MiriLLI to execute each of the 9,130 viable test                After deduplication, we had 394 errors to investigate. Mul-
cases that we identified in Section III-A. The version of               tiple factors lead to the number of bugs being significantly
MiriLLI at this point was based on the same version of the              smaller than the number of deduplicated test outcomes. Our
Rust’s nightly toolchain (1.74.0) that we used in earlier stages        method of deduplication was conservative, we ignored errors
of data collection. We set the global C and C++ compilers to            from crates that had been unpublished since the start of our in-
version 16 of Clang and disabled optimizations. We collected            vestigation, and we only reported Stacked Borrows violations
data using Amazon EC2 on-demand instances provisioned                   that were also Tree Borrows violations. We also observed false
through CloudBank [33]. We used c6a.2xlarge instances                   positives related to alignment and accesses through addresses
during the initial stages of data collection, but we switched           that we do not emulate (e.g., stdout). Additional manual
to c6a.xlarge instances when using MiriLLI. It is single-               investigation was necessary to fully diagnose certain aliasing
threaded, so fewer resources were necessary. All commands               bugs (e.g. #32), since MiriLLI currently does not record the
were executed in a Docker container running Ubuntu 23.04.               source locations of valid updates to the state of the borrow
      a) Executing Tests: We executed each viable test natively         tracker when they occur in LLVM. Miri typically provides a
and in MiriLLI under both Stacked Borrows and Tree Borrows.             trace of the history of each permission involved in a aliasing
We configured Tree Borrows to treat values of the Unique<T>             violation; only partial traces were available for certain bugs.
type as having the semantics of a mutable borrow. Without                    c) Reporting Errors: Not all errors are undefined behav-
this configuration option, only the values of type Unique<T>            ior, and not all instances of undefined behavior are readily
within Box<T> are treated this way. We disabled isolation               exploitable. However, we still attempted to follow ethical
to allow executing non-deterministic operations and enabled             vulnerability disclosure practices by reporting bugs privately
symbolic alignment checking. By default, Miri will report               via email before creating public reports. When we found a
an error if the address of a pointer is not a multiple of the           bug, we examined its crate’s Cargo.toml and the GitHub
requested alignment of the type of value being read or written          profile of its repository’s owner to find a way to contact its
through it. However, the base address of an allocation is not           maintainers privately. If we were unsuccessful, we logged a
guaranteed to be a multiple of the requested alignment, so it is        public issue. We also logged issues if we had not received a
possible for a misaligned pointer to be “aligned” by chance.            response after at least one month or if the type of error did
Symbolic checking avoids these false negatives by ensuring              not appear to be exploitable. Our reports typically included
that the pointer’s offset from the base address is a multiple of        a representative test case, the output from MiriLLI, and a
the alignment of the value being read and that the alignment of         minimal example where applicable. When a fix was trivial, we
the allocation is greater than the alignment of the value. We           also filed a pull request. Section 1 of our Appendix includes
ignored unaligned accesses in LLVM to prioritize detecting              metadata for each library and links to our contributions.
Rust-specific errors.
   On average, across each memory mode, 61% of tests                                             IV. R ESULTS
terminated due to an unsupported operation, 19% passed,                    We found 46 bugs in 37 crates. All appear to be new. As of
10% timed out, 1% failed, and 9% had a potential bug. A                 December 13th, 2024, 28 of the bugs have been confirmed and
“bug” includes both undefined behavior and other undesired              fixed, and none have been identified as security vulnerabilities.
behaviors, such as memory leaks. Of the 61% of unsupported              Bugs occurred slightly more frequently in LLVM than in Rust;
operations, 56% were dynamically linked functions and inline            23 occurred in LLVM, 17 occurred in Rust, and six were
assembly, which are out of scope. An additional 27% were                related to incorrect bindings. The majority (32) were found
atomic instructions and floating point types that LLI does not          in crates with less than 100 average daily downloads in the
implement, 12% were due to types that are not supported by              six months prior to our snapshot of crates.io. However, we
our value conversion layer (discussed in III-B), and 5% were            discovered three Tree Borrows violations in separate crates that
shims that Miri does not fully implement.                               each had more than 10,000 average daily downloads. We found
      b) Deduplicating Errors: We reason about bugs in terms            several additional errors that occurred in Rust and did not
of test outcomes, where an outcome includes the results of              meaningfully involve foreign code. These errors are excluded
a single test under both aliasing models. We deduplicated               from the counts here, but they appear in our raw dataset.



                                                                    6
TABLE I: Counts of each unique error grouped by category,                Fig. 3: A minimal example of Bug #32: an incorrect encap-
the location of the fix, and the location of the error.                  sulation of a self-referential pattern.
                                       Category
       Fix      Error     Allocation   Ownership   Typing   Total:        1   // Rust Encapsulation
     Binding   Binding         -            -        6        6           2   struct Alloc {
     Binding   LLVM            -            3         -       3           3   - cache: i32,
     LLVM      LLVM            -            3         -       3               + cache: UnsafeCell<i32>,
      Rust     LLVM           1            16         -      17           4     buffer: *mut i32,
      Rust      Rust          9             2        6       17           5   }
                 Total:       10           24        12      46           6   fn open(a: &mut Alloc 1 1 ) -> i32 {
                                                                          7   - let cache = &mut a.cache as *mut _; 2
                                                                              + let cache = a.cache.get(); 1
                                                                          8     a.buffer = cache;
   We found 90 tests from 37 crates where Stacked Borrows                 9     let b = &mut *a; 2 3
violations occurred in foreign code. However, 66% (59) of                10     unsafe {
                                                                         11       ffi::open(b.buffer 1 2 );
these tests passed or encountered an unsupported operation               12     - b.cache 3
under Tree Borrows. This is mainly because 50% (45) had                         + *b.cache.get() 2
invalid range errors similar to the minimal example shown                13     }
                                                                         14   }
earlier in Figure 1d. For example, we observed that slices of
an array would be cast into raw pointers, passed across the FFI,         15   // C API
and then offset beyond the range that they initially borrowed.           16   void open(int *buffer 1         2 ) { // ffi::open
                                                                         17     *buffer = 1;
This is considered undefined behavior under Stacked Borrows,             18   }
but it is valid under Tree Borrows. This provides our answer
to RQ2; Tree Borrows accepts more real-world programs that               (a) Tables illustrating the (simplified) subtree of permissions for
call foreign functions than Stacked Borrows due to differences           location of the field “a.cache” before (to the left of the arrow)
                                                                         and after (to the right of the arrow) the write access on line 17.
in handling pointer arithmetic.
   Now, we answer RQ1 by identifying three categories of                  Reserved   →    Active      1       Reserved∗   → Active       1
                                                                          Reserved   →    Active          2          Reserved∗               2
undefined or undesirable behavior that occur in Rust libraries
                                                                          Reserved   →   Disabled         3
that call foreign functions. We describe Ownership errors in
Section IV-A, which include all violations of Tree Borrows
and accesses out-of-bounds. We describe Typing errors in                 a minimal file system for embedded applications. It used
Section IV-B, which include incorrect foreign function bind-             separate structs to represent the state of the file system and
ings and uninitialized values. We describe Allocation errors             its configuration. The configuration held a mutable reference
in Section IV-C, which include both memory leaks and cross-              to the state, but both objects were contained in a parent struct
language deallocation. Table I shows the number of bugs in               representing the entire file system. Rust held a single mutable
each category, grouped by the location of the error and the              reference to the parent, which became invalid when the state
location where a fix would need to be applied. We refer to               was mutated through the configuration by a foreign function.
each bug using a unique numerical ID corresponding to tables                Figure 3 provides a minimal example of the bug and our
in Section 1 of the Appendix.                                            fix. Lines we removed are highlighted in red and marked with
                                                                         “-”, while lines we added are highlighted in green and marked
A. Ownership
                                                                         with a “+”. Tags within a circle indicate the state of the tree
   We found 24 Ownership bugs from 20 crates. These include              prior to the fix, while tags within a square represent the state
17 Tree Borrows violations and seven accesses out-of-bounds.             of the tree after the fix. When a tag is on a line, it indicates that
      a) Const-Correctness: We found 10 insufficient permis-             the pointer or reference on that line has a permission within
sion errors caused by incorrectly casting immutable references           the subtree corresponding to the tag. The tables at the bottom
to mutable raw pointers. In Bug #41, a chain of casts was used           display the state of the tree before and after the write access
to convert &self into a mutable raw pointer. This pointer                on line 17.
still had read-only Frozen permission, so mutating through it               The Rust encapsulation for open initializes the field buffer
across the FFI triggered an insufficient permission error. There         of the struct Alloc on line 8 with a mutable raw pointer cast
were seven bugs with equivalent errors. The remaining three              from a mutable reference to the field cache. The struct is
bugs occurred due to foreign function bindings that incorrectly          mutably borrowed again on line 9. Each of these borrows,
declared pointers as const instead of mut, leading developers            indicated by 2 and 3 , corresponds to an adjacent Reserved
to pass pointers derived from immutable references instead of            branch in the tree. The reference assigned to b, which has
mutable ones.                                                            permission 3 , is used to access the field buffer, which has
      b) Self-Reference: In Rust, it is possible, but nontrivial,        permission 2 . The pointer in this field is passed into the
to implement self-referential patterns using safe encapsulations         foreign function ffi::open. Across the FFI, a write access
of unsafe operations [34]. Bug #32 demonstrates how a self-              occurs on line 17 using permission 2 . This is a child access
referential pattern can be implemented incorrectly. We found             relative to 1 and 2 , so they transition to Active. However,
this bug in an encapsulation of a C library implementing                 it is foreign access relative to 3 , so this permission becomes



                                                                     7
Fig. 4: A minimal example of the incorrect encapsulations of              each other. Both are encapsulated in Rust by a Compression
cyclic aliasing patterns that we observed in Bugs #31 and #35.            object, which carries a heap-allocated instance of Stream
                                                                          within a Box. The Rust function new allocates memory for
 1   // Rust Encapsulation                                                a Stream object and passes a mutable reference carrying the
 2   impl Compression {
 3     fn new() -> Self {                                                 Reserved permission 1 to ffi::init. This foreign function
 4       let mut stream = Box::new(Stream::default());                    copies the pointer it receives to the Stream object into a
 5     + let stream = Box::into_raw(stream);
 6       unsafe {                                                         newly allocated State instance on line 22, creating a cyclic
 7       - ffi::init(stream.as_mut()); 1                                  structure. Later, when the function compress is called, it
         + ffi::init(stream); 1
 8       }                                                                creates an adjacent Reserved permission 2 . Mutating through
 9       Compression { stream }                                           this permission on line 14 causes 1 to become Disabled,
10     }
11                                                                        making it undefined behavior to read using 1 in the body of
12       fn compress(&mut self 2 2 ) {                                    ffi:compress on line 25.
13         unsafe {
14         - self.stream.data = 0; 2                                          To fix each error, we unwrapped the Box using into_raw
           + (*self.stream).data = 0; 1                                   and stored a raw pointer to the allocation within the
15         - ffi::compress(self.stream.as_mut()); 2                       Compression struct. We modified the API so that this
           + ffi::compress(self.stream); 1
16         }                                                              raw pointer would be used for every access to the alloca-
17       }                                                                tion, ensuring that the cyclic structure would remain valid.
18   }
                                                                          This corresponds to permission 1 in Figure 4, which re-
19   // C API                                                             mains Active through each access. We also had to mod-
20   void init(Stream* s 1 1 ) { // ffi::init                             ify Compression’s implementation of Drop to rewrap this
21     s->state = malloc(sizeof(State));
22     s->state->stream = s;                                              pointer using Box::into_raw to avoid a memory leak.
23   }
                                                                              Bug #33 also involved a mutable reference being copied into
24   void compress(Stream* s 2 1 ) { // ffi::compress
25     int data = s->state->stream->data; 1 1                             the foreign heap, but we needed a different approach to fix it.
26   }                                                                    It occurred in the same file system library as Bug #32, which
                                                                          avoided creating heap allocations in Rust as a constraint of
(a) Tables illustrating the (simplified) subtree of permissions for       the embedded application context. Instead of using a Box<T>
location of the field stream.data before (to the left of the arrow)       to allocate the equivalent of the Stream object in Figure 4,
and after (to the right of the arrow) the write access on line 14.
                                                                          the Rust encapsulation passed around a mutable reference
 Reserved   →   Disabled    1                Active           1           to a stack allocation. Similar to Bugs #31 and Bug #35,
 Reserved   →    Active     2     Reserved    → Disabled      2           once the reference was created, it was passed to a foreign
                                                                          initialization function that copied the reference into a foreign
                                                                          heap allocation. After the initialization function returned, the
Disabled. This leads to an expired permission error on line 12            mutable reference was moved into a RefCell<&mut T>. This
when 3 is used for a read access in Rust.                                 performed a reborrow, creating a new Reserved permission
    We fixed this bug by wrapping parts of the state in an                as a child of the Reserved permission held by the foreign
UnsafeCell, which can be mutated through shared refer-
                                                                          heap. Both of these permissions could be used interchangeably
ences. In Figure 3, we change the first field of Alloc to                 for read accesses but not for write accesses. If the foreign
UnsafeCell<i32> and replace the mutable borrow assigned
                                                                          parent permission was mutated first, it would invalidate the
to a.buffer with a.cache.get(). This expression does                      child permission. If the child permission was mutated first,
not perform a retag, so both a and cache share permission                 then both permissions would become Active, but the next
 1 . Since a contains an UnsafeCell, the mutable borrow                   mutation through the parent permission would cause the child
assigned to b on line 9 associates the tag 2 with a special               permission to become Frozen, making future write accesses
Reserved∗ permission that can tolerate foreign writes. Con-               through the child permission undefined behavior.
sequently, this permission is no longer disabled by the write
                                                                              To fix this error, we stored the mutable borrow as a
through 1 on line 17, so the read access on line 12 is valid.
                                                                          RefCell<*mut T>, which prevented new child permissions
      c) Multiple Mutable Aliasing: Expired permission errors
                                                                          from being created. However, the type T was a struct, and
occurred when pointers derived from mutable references were
                                                                          certain foreign functions required pointers to its members.
copied into the foreign heap. We found this type of bug in five
                                                                          Reborrowing is typically necessary to create a reference to a
separate libraries. The most notable examples were Bug #31
                                                                          member of a struct, but this creates a new permission, which
from bzip2 and Bug #35 from flate2, which are both
                                                                          we needed to avoid. Instead, we used Rust’s addr_of_mut!
popular compression libraries. In particular, flate2 is ac-
                                                                          macro, which creates a pointer to a location without borrowing
tively maintained by the Rust project and averaged more than
                                                                          it.6 Together, these two changes ensure that all memory ac-
130,000 downloads per day during our observation period.
                                                                          cesses on each side of the boundary use the same permission.
    Figure 4 shows a minimal example of the cyclic aliasing
pattern used by each library. We use the same notation as
Figure 3. The structs Stream and State carry pointers to                    6 Rust 1.82.0 provided native syntax: &raw   mut



                                                                      8
The authors of Tree Borrows [10] found an equivalent bug in            the encapsulation; it was possible to cause an access out-of-
test cases for the Rust toolchain and applied the same fix.            bounds error by passing a KeySize larger than the length of
      d) Protection: We found one protected permission error           either key. We did not propose a fix for this bug, as it could
equivalent to the example in Figure 1c. In Bug #25, a Rust             require significant changes to the API.
function attempted to use a foreign function to grow a heap-              Bug #22 involved a foreign function that expected to receive
allocated array of values. The foreign function was passed a           a pointer to a string with six characters. It was allocated
pointer derived from a reference-type argument to the Rust             with CString::new(Vec::with_capacity(6)), exposed
encapsulation. Similar to Figure 1c, when this pointer was             as a raw pointer using into_raw, and correctly deallocated
used to reallocate the array, its protected permission became          after the call using from_raw. However, the implementation
Disabled, which is undefined behavior. We fixed this bug by            of CString::new appends a null-terminator to the vector
changing the function to receive a raw pointer instead. Raw            and then converts it into a value of type Box<[u8]> using
pointers do not receive protectors, so they can be used for            into_boxed_slice, which shortens the capacity of a vector
deallocation.                                                          to be equal to its length. The intended capacity was six, but
      e) PhantomData: Rust’s PhantomData<T> behaves                    into_boxed_slice shortened it to one, appending a null-
like an instance of T, but it can be created without                   terminator. The encapsulation did not validate that the length
providing a concrete value. However, a value of type                   of the CString instance was correct, leading to an access out-
PhantomData<UnsafeCell<T>> does not behave like an                     of-bounds when the C codebase read beyond the first character.
UnsafeCell<T>; it cannot be mutated through immutable                  We fixed this error by initializing the CString with a constant
references [35]. In Bug #30, the type Opaque was declared              of the correct length.
as an alias for PhantomData<UnsafeCell<* mut T>>. It
                                                                       B. Typing
was used to represent foreign types in Rust without having to
declare their layout on both sides of the FFI boundary. Since             We found 12 bugs from 12 crates that involved typing
Opaque did not contain a concrete instance of UnsafeCell,              or initialization. Some were caused by incorrect use of
raw pointers derived from &Opaque received a read-only                 MaybeUninit<T>, while others involved incorrect foreign
permission, leading to an insufficient permission error when           function bindings.
they were used for a write access in foreign code. We proposed               a) Incomplete Initialization: We found five bugs that
fixing this error by removing PhantomData, but other con-              involved partial initialization. In Bug #45, an uninitialized
tributors are still discussing the correct fix. The relationship       instance of a struct T containing an array of values was created
between PhantomData and UnsafeCell is not yet settled,                 using MaybeUninit<T> and passed across the FFI to be
so this pattern may be allowed in the future.                          initialized. The foreign call only initialized the first element
      f) Access Out-of-Bounds: We found seven access out-of-           of the array to zero. The remaining uninitialized elements
bounds errors in unique crates. Bugs #19 and #20 were found            would never be read by C, since every iteration stopped at the
in two encapsulations for libdecnumber, which is part of               null terminator. Miri reported these initialization patterns as
the GCC toolchain [36]. This library often used the following          an error when MaybeUninit<T>::assume_init was called.
pattern to iterate over arrays of integers:                            We fixed this bug by zero-initializing the entire array in Rust.
                                                                          Bug #46 seemed to involve an equivalent pattern;
  for (; *curr==0 && curr+3 < end;) curr+=4;
                                                                       MaybeUninit<T>::assume_init triggered an error for a
The first term in the conjunction will execute before the second       struct that was initialized by a foreign function. However,
term, but if the second term is false, then the first term is          the function properly zero-initialized the struct using memset.
an access out-of-bounds or an uninitialized read. This was             After examining the LLVM bytecode of the foreign function,
fixed by swapping the order of each term. Bug #23 was                  we found that all 88 bytes of the struct were initialized on
found in a disassembler that incorrectly implemented several           the LLVM stack, but only the first 80 bytes were copied back
instructions, leading to an access out-of-bounds into adjacent         into Rust. These missing bytes corresponded to padding fields,
static arrays. This error was fixed once the correct semantics         which were never directly accessed by the foreign library.
were implemented.                                                      Optimizations had been disabled, but LLVM still removed
   None of these errors meaningfully involve Rust. However,            this unnecessary write access. We fixed Bug #46 by zero-
the remaining errors were caused by Rust encapsulations                initializing the padding fields before calling assume_init.
that did not adequately enforce the preconditions of foreign                 b) Incorrect Bindings: We found six crates with one or
function calls. Bug #18 involved the following API, which              more incorrect foreign function bindings. All of these incorrect
redirected its arguments to foreign functions based on the value       bindings had been written manually. Three of these crates
of the parameter size:                                                 had bindings with missing return types. In Bug #5, a binding
  fn expand(ex_key: &mut [u8], key: &[u8], size: KeySize)
                                                                       was declared in a unit test without its 32-bit integer return
                                                                       type. The C implementation used this to return a status code
For example, passing KeySize::K128 would call a foreign                indicating if one of its integer parameters was within bounds.
function that assumed that ex_key and key would each be                The remaining three bugs involved bindings with incorrect
128 bytes long. However, this invariant was not enforced by            integer types, which led to incomplete initialization. In Bug #6,



                                                                   9
a function was declared to return a 32-bit integer, but its C           bug-finding tools, such as LLVM’s sanitizers or Valgrind,
implementation returned a boolean value. In Bug #4, the last            which can detect memory leaks (e.g #10) and accesses out-of-
parameter of a function was declared as a 32-bit integer, but           bounds (e.g. #23). Developers who maintain foreign function
the C implementation expected size_t. The width of size_t               bindings should consider that the infrequent cost of generating
is architecture-dependent, so this binding was only correct for         and committing bindings may be preferable to writing them by
32-bit architectures. To fix this bug, multiple prior releases          hand without assistance, which can lead to errors. When heap
needed to be patched to use Rust’s usize type, which has                objects are accessed on each side of the foreign boundary, it
similar semantics.                                                      is helpful to be aware of where each object is created, how
                                                                        many references it has, where these references are stored, and
C. Allocation                                                           what capabilities they require. Each of these attributes can
   We found 10 issues related to allocation in 10 distinct              influence the correct design for an encapsulation. For example,
libraries. These include nine memory leaks and one new cross-           Bug #33 was fixable by casting a reference into a pointer,
language deallocation bug.                                              while Bugs #35 and #31 required unwrapping a Box.
      a) Memory Leaks: Rust’s Box<T> and CString use                          b) For The Rust Project: The Rust community is in dire
similar APIs to encapsulate heap allocations. For each type,            need of a production-ready solution for finding aliasing bugs
the function into_raw consumes an instance and produces                 in multi-language applications. Although our approach was
a pointer to its interior heap allocation. To avoid a memory            capable of finding real-world bugs, its scalability is limited
leak, this pointer must be reconstituted in its wrapper type            due to the requirement of implementing shims for system
using the function from_raw. We found four leaks caused by              calls and the lack of a formal specification for the ABIs
calling into_raw on either Box<T> or CString without later              implemented by Rust, Clang, and LLVM. Instrumenting a
calling from_raw. Each type was used to allocate memory for             shared, intermediate format is likely to be the most effective
a foreign function call, and each bug was fixed by adding a             approach. The Krabcake project [37] (announced concurrently
call to from_raw after the function returned. The remaining             with MiriLLI) is developing an extension to Valgrind [24] that
five leaks were of memory that had been allocated by C. Most            will provide support for detecting aliasing violations, but it is
were caused by neglecting to call a destructor that had been            not yet capable of replicating our results. The Rust community
exposed by the C API. However, in Bug #10, the C API did                should invest resources into completing a prototype imple-
not expose a destructor, since it had been designed based on            mentation to evaluate in real-world applications. However,
the assumption that users would be able to call free. We                Valgrind can also incur significant runtime overhead. Our
could not use Rust’s allocator API to fix this, since that could        future work will involve creating an LLVM sanitizer that can
lead to invalid cross-language deallocation.                            detect aliasing violations, providing the performance necessary
      b) Cross-Language Deallocation: It is potentially unde-           to find these errors at scale with fuzzing tools. We also expect
fined behavior to free a pointer allocated by C in Rust, or             that sophisticated static analysis tools would help developers
vice versa, since each language’s binary may use a differ-              avoid undefined behavior at foreign boundaries by issuing
ent allocator. We found one new example of cross-language               warnings for functions that copy pointers or mutate through
deallocation. In Bug #1, a pointer to a heap-allocated string           pointers derived from immutable references.
was returned to Rust by a foreign function call and stored
as a Cow<&’static [u8]>, which will lazily clone its data                                    VI. R ELATED W ORK
when mutated. This wrapper type is an enumeration with two                 Foreign function calls are a common use case for unsafe
variants; Cow::Borrowed receives a reference to a value,                code, but they have been understudied in prior work.
while Cow::Owned takes ownership of a value, deallocating                    a) Surveys of the Rust Ecosystem: Studies that examine
it when it goes out of scope. When this Cow was dropped, it             how unsafe code is used in Rust libraries have consistently
deallocated the C heap memory using Rust’s allocator. There             found that foreign function calls are a significant use case for
was no immediate fix for this bug, since the C API did not              unsafe code [4], [5]. In particular, Evans et al. [4] surveyed all
expose a destructor.                                                    published crates in September of 2018 and found that 22.5%
                                                                        of all unsafe function calls were to foreign functions. Rust
                       V. D ISCUSSION                                   developers also view foreign function calls as a central use
   Our findings indicate that it is easy to inadvertently in-           case for unsafe code. Fulton et al. [6] interviewed 16 Rust
troduce undefined behavior in Rust libraries that call foreign          developers and surveyed 178 developers, finding that nearly
functions. The errors we found can be prevented with careful            half of their participants used foreign function calls. Both
auditing, but it seems likely that many will persist until              Höltervennhoff et al. [7] and McCormack et al. [8] focused
the Rust community develops a production-ready method for               specifically on Rust developers who use unsafe code, and each
finding aliasing violations in multi-language applications. We          found that the majority of participants used Rust’s FFI.
provide the following recommendations:                                       b) Types of Bugs & Undefined Behavior: Prior studies
     a) For Rust Developers: Awareness is key to avoiding               have examined open source contributions to categorize errors
improper use of unsafe features. Developers who depend on               caused by unsafe code. Most considered foreign function calls
foreign code should validate their tests with language-agnostic         to be out of scope, and none described aliasing violations in



                                                                   10
terms of Stacked or Tree Borrows. Both Qin et al. [38] and                    External Validity: Crates that could not compile with our
Xu et al. [39] examined bug and vulnerability reports from               nightly toolchain were excluded from our evaluation, even if
open source projects and found examples of allocation and                they would have otherwise been compatible with MiriLLI.
typing errors that are similar to the ones that we discovered.           Limited support for certain features, such as dynamically
Xu et al. [39] did encounter errors related to foreign function          linked libraries, also prevented us from achieving high test
calls, but they were primarily “straightforward” issues related          coverage; 61% of tests terminated due to an unsupported oper-
to application-specific invariants, layout, and alignment. Cui et        ation and 10% timed out. Additionally, the majority of libraries
al. [40] evaluated a taxonomy of 19 safety properties required           we examined linked against C, and not C++. Crates that failed
by unsafe functions, but they made it an explicit design goal            to compile using our nightly toolchain were excluded from
to exclude foreign functions.                                            the evaluation, as well as crates that overrode the system’s
      c) Bug-finding Tools & Verifiers: Prior approaches to              default C and C++ compiler. However, these limitations did not
static analysis [41], [38], [42], [43] have found a wide variety         prevent us from answering our research questions. Our goal
of bugs caused by improper use of unsafe code, but few                   was not to create a production-ready tool, but to understand
approaches scale beyond Rust. Li et al. [44] applied dataflow            the types of errors that can occur in Rust libraries that call
analysis on LLVM IR and detected several memory leaks                    foreign functions. The bugs that occur in general may differ
and cross-language deallocation errors in Rust libraries. We             in unexpected ways from those found with our setup.
replicated several of the bugs they encountered. Hu et al. [45]
                                                                                                 VIII. C ONCLUSION
modified several existing Rust analysis tools, including Miri,
to analyze multi-language programs defined in a custom                      We conducted a large-scale evaluation to investigate the
intermediate representation. However, they did not consider              types of undefined behavior that occur in Rust libraries that
aliasing violations. Lei et al. [46] took a similar approach             call foreign functions. We created MiriLLI—a dynamic analy-
using WebAssembly as the target language, but their evaluation           sis tool that combines two existing interpreters—and we used
did not use Miri or consider aliasing issues, either. Recent             it to find 46 bugs in 37 libraries. Though many of these bugs
deductive verifiers based on the RustBelt [47] model have                were aliasing violations, Rust’s Tree Borrows aliasing model
used compositional verification [48] and automated proof                 was more permissive in this context than the earlier Stacked
search [49] to verify unsafe code, but none of these approaches          Borrows model. To ensure that these errors are easy to detect,
reason about Stacked or Tree Borrows or have explicit support            the Rust project should invest in new dynamic analysis tools
for foreign function calls.                                              that can accommodate multi-language applications.
                                                                                                 ACKNOWLEDGMENT
                VII. T HREATS TO VALIDITY
                                                                            We thank Tomas Dougan for contributing to the implemen-
     Construct Validity: We disabled compile-time optimiza-              tation of MiriLLI. This material is based on work supported
tions in both Rust and LLVM to avoid missing bugs. However,              by the Department of Defense and the National Science Foun-
we did not evaluate whether optimization would have had any              dation under Grant Nos. CCF-1901033, DGE1745016, and
effect on our results, and we did not determine whether any              DGE2140739. Results presented in this paper were obtained
of the bugs that we found had an effect on native execution.             using CloudBank [33], which is supported by the National
     Internal Validity: We did not use the same hardware                 Science Foundation under Grant No. CNS-1925001. Any
when investigating the source of each bug as we did for                  opinions, findings, conclusions, or recommendations expressed
large-scale data collection. Our value translation layer cannot          in this material are those of the authors and do not necessarily
detect when a binding uses an incorrect type that happens to             reflect the views of the Department of Defense or the National
have the correct layout, which may have caused us to miss                Science Foundation.
bugs. Errors in Miri or other components of Rust’s nightly
toolchain may have affected the correctness of our results.                                           R EFERENCES
Since we manually investigated each bug, we have no reason                [1] Stack Overflow. (2024, Jul.) Stack Overflow developer survey 2024.
to believe that these errors and their fixes are specific to any              [Online]. Available: https://survey.stackoverflow.co/2024/
                                                                          [2] R. Pereira, M. Couto, F. Ribeiro, R. Rua, J. Cunha, J. P. Fernandes,
particular version of Rust’s toolchain, with the exception of                 and J. Saraiva, “Energy efficiency across programming languages: how
Tree Borrows violations. The model was still evolving during                  do energy, time, and memory relate?” in Proceedings of the 10th ACM
our evaluation.                                                               SIGPLAN International Conference on Software Language Engineering,
                                                                              ser. SLE ’17.     New York, NY, USA: Association for Computing
   Several of our bug reports are still pending responses,                    Machinery, 2017, p. 256–267.
so we cannot be entirely certain that all of our results are              [3] Rust Community. Miri. [Online]. Available: https://github.com/rust-lan
novel or true positives. However, we did exclude bugs from                    g/miri
                                                                          [4] A. N. Evans, B. Campbell, and M. L. Soffa, “Is Rust used safely by
our evaluation that had already been reported. We did not                     software developers?” in Proceedings of the ACM/IEEE 42nd Interna-
independently confirm that these bugs were absent from test                   tional Conference on Software Engineering, ser. ICSE ’20. New York,
cases that did not call foreign functions, but we have no reason              NY, USA: ACM, 2020, p. 246–257.
                                                                          [5] V. Astrauskas, C. Matheja, F. Poli, P. Müller, and A. J. Summers,
to believe that any would have been detected by an unmodified                 “How do programmers use unsafe Rust?” Proceedings of the ACM on
version of Miri at the time of our evaluation.                                Programming Languages, vol. 4, no. OOPSLA, Nov. 2020.




                                                                    11
 [6] K. R. Fulton, A. Chan, D. Votipka, M. Hicks, and M. L. Mazurek,                  [31] J. Lee, Y. Kim, Y. Song, C.-K. Hur, S. Das, D. Majnemer, J. Regehr,
     “Benefits and drawbacks of adopting a secure programming language:                    and N. P. Lopes, “Taming undefined behavior in LLVM,” SIGPLAN Not.,
     Rust as a case study,” in Seventeenth Symposium on Usable Privacy                     vol. 52, no. 6, p. 633–647, Jun. 2017.
     and Security, ser. SOUPS ’21. USENIX Association, Aug. 2021, pp.                 [32] LLVM Project. LLVM documentation. [Online]. Available: https:
     597–616.                                                                              //llvm.org/docs/index.html
 [7] S. Höltervennhoff, P. Klostermeyer, N. Wöhler, Y. Acar, and S. Fahl,             [33] M. Norman, V. Kellen, S. Smallen, B. DeMeulle, S. Strande, E. La-
     ““I wouldn’t want my unsafe code to run my pacemaker”: An interview                   zowska, N. Alterman, R. Fatland, S. Stone, A. Tan, K. Yelick,
     study on the use, comprehension, and perceived risks of unsafe Rust,”                 E. Van Dusen, and J. Mitchell, “CloudBank: Managed services to
     in Proceedings of the 32nd USENIX Security Symposium, ser. USENIX                     simplify cloud access for computer science research and education,”
     Security ’23. Anaheim, CA: USENIX Association, Aug. 2023, pp.                         in Practice and Experience in Advanced Research Computing 2021:
     2509–2525.                                                                            Evolution Across All Dimensions, ser. PEARC ’21. New York, NY,
 [8] I. McCormack, T. Dougan, S. Estep, H. Hibshi, J. Aldrich, and                         USA: Association for Computing Machinery, 2021.
     J. Sunshine, “A mixed-methods study on the implications of unsafe                [34] M. Goregaokar. (2022, Aug.) Not a yoking matter (zero-copy #1).
     Rust for interoperation, encapsulation, and tooling,” arXiv preprint                  [Online]. Available: https://manishearth.github.io/blog/2022/08/03/zero
     arXiv:2404.02230 [cs.SE], 2024.                                                       -copy-1-not-a-yoking-matter/
 [9] R. Jung, H.-H. Hostert, JoDang, J. Kang, and D. Dreyer, “Stacked                 [35] R. Jung. (2020, Jun.) Stacked Borrows: How precise should UnsafeCell
     Borrows: An aliasing model for Rust,” Proceedings of the ACM on                       be tracked? [Online]. Available: https://github.com/rust-lang/unsafe-c
     Programming Languages, vol. 4, no. POPL, Dec. 2019.                                   ode-guidelines/issues/236
[10] N. Villani, J. Hostert, D. Dreyer, and R. Jung. (2024, Nov.) Tree                [36] GNU Project. GCC, the GNU compiler collection. [Online]. Available:
     Borrows. [Online]. Available: https://perso.crans.org/vanille/treebor/au              https://gcc.gnu.org/
     x/preprint.pdf                                                                   [37] F. S. Klock and B. Garza, “Krabcake: A Rust UB detector,” in
[11] R. Jung. (2021, Nov.) Undefined behavior deserves a better reputation.                Proceedings of the 3rd Rust Verification Workshop., ser. RW2023, Apr.
     [Online]. Available: https://blog.sigplan.org/2021/11/18/undefined-beh                2023. [Online]. Available: https://pnkfx.org/presentations/krabcake-rus
     avior-deserves-a-better-reputation/                                                   t-verification-2023-april.pdf
[12] W. Crichton, “The usability of ownership,” in Proceedings of the 1st             [38] B. Qin, Y. Chen, Z. Yu, L. Song, and Y. Zhang, “Understanding memory
     Workshop on Human Aspects of Types and Reasoning Assistants., ser.                    and thread safety practices and issues in real-world Rust programs,” in
     HATRA ’20, 2020. [Online]. Available: https://arxiv.org/abs/2011.06171                Proceedings of the 41st ACM SIGPLAN Conference on Programming
[13] S. Klabnik, C. Nichols, and the Rust Community. The Rust programming                  Language Design and Implementation, ser. PLDI ’20. New York, NY,
     language. https://doc.rust-lang.org/book/.                                            USA: ACM, Jun. 2020, p. 763–779.
[14] G. Vranken and A. Crichton. (2023, Apr.) CVE-2023-30624. [Online].               [39] H. Xu, Z. Chen, M. Sun, Y. Zhou, and M. R. Lyu, “Memory-safety
     Available: https://www.cve.org/CVERecord?id=CVE-2023-30624                            challenge considered solved? an in-depth study with all Rust CVEs,”
[15] R. Jung. (2024, Jan.) Rust has provenance. [Online]. Available:                       ACM Transactions on Software Engineering and Methodology, no. 1,
     https://github.com/rust-lang/rfcs/pull/3559                                           Sep. 2021.
[16] ISO/IEC, “Information technology – Programming languages – C,”                   [40] M. Cui, S. Sun, H. Xu, and Y. Zhou, “Is unsafe an achilles’
     International Organization for Standardization; International Elec-                   heel? a comprehensive study of safety requirements in unsafe rust
     trotechnical Commission, Geneva, CH, Standard, Apr. 2024. [Online].                   programming,” in Proceedings of the IEEE/ACM 46th International
     Available: https://open-std.org/JTC1/SC22/WG14/www/docs/n3220.pdf                     Conference on Software Engineering, ser. ICSE ’24. New York, NY,
[17] ——, “Working draft, standard for programming language C++,” Inter-                    USA: Association for Computing Machinery, 2024. [Online]. Available:
     national Organization for Standardization; International Electrotechnical             https://doi.org/10.1145/3597503.3639136
     Commission, Geneva, CH, Standard, May 2023. [Online]. Available:                 [41] Z. Li, J. Wang, M. Sun, and J. C. Lui, “MirChecker: Detecting bugs
     https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4950.pdf                    in Rust programs via static analysis,” in Proceedings of the 2021 ACM
[18] Rust Community. (2024, Feb.) The Rust reference - behavior considered                 SIGSAC Conference on Computer and Communications Security, ser.
     undefined. https://doc.rust-lang.org/reference/behavior-considered-und                CCS ’21. New York, NY, USA: ACM, 2021, p. 2183–2196.
     efined.html.                                                                     [42] M. Cui, C. Chen, H. Xu, and Y. Zhou, “SafeDrop: Detecting memory
[19] C. D. Feather. (2004) DR260 - indeterminate values and identical                      deallocation bugs of Rust programs via static data-flow analysis,” ACM
     representations. [Online]. Available: https://www.open-std.org/jtc1/sc22              Transactions on Software Engineering and Methodology, vol. 32, no. 4,
     /wg14/www/docs/dr_260.htm                                                             May 2023.
[20] K. Memarian, V. B. F. Gomes, B. Davis, S. Kell, A. Richardson, R. N. M.          [43] Y. Bae, Y. Kim, A. Askar, J. Lim, and T. Kim, “RUDRA: Finding
     Watson, and P. Sewell, “Exploring c semantics and pointer provenance,”                memory safety bugs in Rust at the ecosystem scale,” in Proceedings of
     Proceedings of the ACM on Programming Languages, vol. 3, no. POPL,                    the ACM SIGOPS 28th Symposium on Operating Systems Principles,
     Jan. 2019.                                                                            ser. SOSP ’21.       New York, NY, USA: Association for Computing
[21] R. Jung. (2022, May) The plan for provenance. [Online]. Available:                    Machinery, 2021, p. 84–99.
     https://github.com/rust-lang/miri/issues/2133                                    [44] Z. Li, J. Wang, M. Sun, and J. C. S. Lui, “Detecting cross-language
[22] Rust Community. The bindgen user guide. https://rust-lang.github.io/ru                memory management issues in Rust,” in Computer Security – ESORICS
     st-bindgen/.                                                                          2022, V. Atluri, R. Di Pietro, C. D. Jensen, and W. Meng, Eds. Cham:
[23] ——. CXX – safe interop between Rust and C++. https://cxx.rs/.                         Springer Nature Switzerland, 2022, pp. 680–700.
[24] J. Seward and N. Nethercote, “Using Valgrind to detect undefined value           [45] S. Hu, B. Hua, L. Xia, and Y. Wang, “CRUST: Towards a unified cross-
     errors with bit-precision,” in 2005 USENIX Annual Technical Confer-                   language program analysis framework for Rust,” in 2022 IEEE 22nd
     ence, ser. USENIX ATC ’05. Anaheim, CA: USENIX Association,                           International Conference on Software Quality, Reliability and Security
     Apr. 2005.                                                                            (QRS), 2022, pp. 970–981.
[25] Rust Community. The Rust unstable book - sanitizer. [Online].                    [46] L. Xia, B. Hua, and Y. Wang. (2023) ACORN: Towards a
     Available: https://doc.rust-lang.org/beta/unstable-book/compiler-flags/s              holistic cross-language program analysis for Rust. [Online]. Available:
     anitizer.html                                                                         https://csslab-ustc.github.io/publications/2023/acorn.pdf
[26] A. Green and libffi Contributors. libffi. [Online]. Available: https:            [47] R. Jung, J.-H. Jourdan, R. Krebbers, and D. Dreyer, “RustBelt: Securing
     //sourceware.org/libffi/                                                              the foundations of the Rust programming language,” in Proceedings
[27] LLVM Project. (2024, Mar.) lli - directly execute programs from LLVM                  of the 44th ACM SIGPLAN Symposium on Principles of Programming
     bitcode. https://llvm.org/docs/CommandGuide/lli.html.                                 Languages, ser. POPL ’17, vol. 2. New York, NY, USA: ACM, 2017.
[28] ——. Clang: a C language family frontend for LLVM. https://clang.ll               [48] S. Élie Ayoun, X. Denis, P. Maksimović, and P. Gardner, “A hy-
     vm.org/.                                                                              brid approach to semi-automated Rust verification,” arXiv preprint
[29] D. Kolsoi and Inkwell Contributors. Inkwell. [Online]. Available:                     arXiv:2403.15122 [cs.PL], 2024.
     https://github.com/TheDan64/inkwell                                              [49] L. Gäher, M. Sammler, R. Jung, R. Krebbers, and D. Dreyer, “Refine-
[30] J. McIver. (2022, Jan.) Load instruction: Uninitialized memory                        dRust: A type system for high-assurance verification of Rust programs,”
     semantics. [Online]. Available: https://discourse.llvm.org/t/rfc-load-ins             Proceedings of the ACM on Programming Languages, vol. 8, no. PLDI,
     truction-uninitialized-memory-semantics/67481/1                                       Jun. 2024.




                                                                                 12
