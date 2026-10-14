                                         SafeFFI: Efficient Sanitization at the Boundary Between Safe and Unsafe Code in
                                                              Rust and Mixed-Language Applications

                                               Oliver Braunsdorf1 , Tim Lange1 , Konrad Hohentanner2 , Julian Horsch2 , and Johannes Kinder1
                                                                                             1
                                                                                              LMU Munich, Germany
                                                                                        2
                                                                                            Fraunhofer AISEC, Germany
arXiv:2510.20688v1 [cs.PL] 23 Oct 2025




                                                                  Abstract                                      vice versa—via a foreign function interface (FFI). In this situ-
                                                                                                                ation, the safety guarantees of Rust may be compromised by
                                            Unsafe Rust code is necessary for interoperability with
                                                                                                                unsafe operations in foreign code.
                                         C/C++ libraries and implementing low-level data structures,
                                                                                                                   But even pure Rust code may contain unsafe code, marked
                                         but it can cause memory safety violations in otherwise
                                                                                                                via the unsafe keyword, allowed to violate the strict typing
                                         memory-safe Rust programs. Sanitizers can catch such mem-
                                                                                                                rules for implementing efficient algorithms and data structures
                                         ory errors at runtime, but introduce many unnecessary checks
                                                                                                                or hardware interactions. Thus, be it from foreign functions
                                         even for memory accesses guaranteed safe by the Rust type
                                                                                                                or explicitly marked unsafe code regions, Rust bears the risk
                                         system. We introduce SafeFFI, a system for optimizing mem-
                                                                                                                of memory-safety violations originating in unsafe code that
                                         ory safety instrumentation in Rust binaries such that checks
                                                                                                                potentially affect the whole code base, even safe code [26].
                                         occur at the boundary between unsafe and safe code, handing
                                         over the enforcement of memory safety from the sanitizer to               Both C/C++ and unsafe Rust code can be protected from
                                         the Rust type system. Unlike previous approaches, our design           exploitation by applying memory-safety sanitizers [40, 42]
                                         avoids expensive whole-program analysis and adds much less             to the whole code base, which transparently introduce run-
                                         compile-time overhead (2.64× compared to over 8.83×). On               time checks for memory operations. While sanitizers such
                                         a collection of popular Rust crates and known vulnerable Rust          as AddressSanitizer (ASan) [37] and Hardware-assisted Ad-
                                         code, SafeFFI achieves superior performance compared to                dressSanitizer (HWASan) [38] do not require any source code
                                         state-of-the-art systems, reducing sanitizer checks by up to           changes and can achieve thorough memory safety guaran-
                                         98%, while maintaining correctness and flagging all spatial            tees [42], they introduce a significant run-time overhead by
                                         and temporal memory safety violations.                                 inserting checks for every pointer dereference in the code.
                                                                                                                Many of these checks are unnecessary, however: a pointer
                                                                                                                dereference in Rust is guaranteed safe as long as the pointer
                                         1   Introduction                                                       is safe and cannot be affected by unsafe code. Previous so-
                                                                                                                lutions for selective sanitization of Rust code [5, 26] use
                                         Memory corruptions caused by unsafe programming lan-                   whole-program static points-to analysis to classify pointers
                                         guages such as C and C++ remain a major source of crit-                as provably safe or potentially unsafe and then elide checks
                                         ical software vulnerabilities. Memory bugs regularly take              for an under-approximation of safe pointers. While theoret-
                                         top spots in the lists of most dangerous [28] and known ex-            ically sound, this approach incurs significant compile-time
                                         ploited weaknesses [27], and studies by Google [11, 41] and            overhead and misses optimization opportunities. In contrast,
                                         Microsoft [25] indicate that around 70% of their severe bugs           our approach relies on efficient local reasoning about pointer
                                         are caused by memory unsafety.                                         types and their safety guarantees.
                                            In recent years, the Rust programming language has gained              In this paper, we present SafeFFI, a new approach to reduce
                                         traction as a safe-by-construction solution for newly devel-           the overhead of memory-safety sanitizers in Rust applications
                                         oped software. Securing existing C/C++ programs by rewrit-             and MLAs consisting of C and Rust code. SafeFFI utilizes
                                         ing them in safe languages requires substantial development            the fact that Rust’s strong type system enforces guarantees
                                         effort, however. Despite recent efforts to translate legacy code       for pointer types such as reference types (&T) and box types
                                         bases to Rust [39, 47], we can expect C/C++ code to be relied          (Box<T>), while raw pointers (*const T ) are unchecked.
                                         on for the foreseeable future. Thus, in practice, Rust applica-           A key insight in our work is that the cast from a raw
                                         tions may actually be mixed language applications (MLAs),              pointer type to a safe pointer type forms the boundary between
                                         where the Rust application is linked against C/C++ code—or             sanitizer-enforced memory safety and type-system-enforced


                                                                                                            1
memory safety. SafeFFI hoists and bundles checks into a sin-            Interception and is especially helpful for sanitizing 3rd-party
gle dynamically-checked precondition, which is propagated               libraries without recompiling. Sanitizers use different types of
statically through the type system. This way, we free the               metadata to track memory state and detect violations, typically
memory sanitizer from checking every pointer dereference,               categorized as being either object-based [4, 12, 19, 22, 37, 38]
including from checking dereferences of potentially unsafe              or pointer-based [14, 17, 30, 33]. Object-based metadata, such
pointers. Therefore, for most patterns of Rust programs, we             as redzones [37] or memory tags [38], is associated with mem-
can elide more sanitizer checks than previous approaches,               ory allocations and mark memory regions as valid or invalid.
leading to better run-time performance.                                 In contrast, pointer-based metadata augments pointers with
   Because our check placement enforces memory-safety                   additional information, such as bounds [30, 33] and refer-
across function calls, we only require local reasoning to en-           ences to temporal metadata [31]. Since they are associated
sure memory-safety across the whole application. Hence, we              with pointers, they can track the validity of memory accesses
avoid expensive whole-program static analysis leading to bet-           based on the pointer’s state, e.g., enabling also sub-object
ter compile-time performance and enabling SafeFFI to scale              bounds tracking [33].
well on large software projects. In summary, we make the                   Two widely used memory-safety sanitizers are ASan [37]
following contributions:                                                and HWASan [38], available in LLVM and GCC. ASan instru-
   • A novel concept and algorithm for combining sanitizers             ments code to place red zones in shadow memory, catching
      for unsafe languages and type information from strongly-          out-of-bounds and use-after-free errors; it also poisons freed
      typed languages to enforce memory safety in mixed code.           memory and delays reuse, improving detection at the cost
      Our algorithm avoids expensive whole-program static               of higher memory overhead. HWASan reduces overhead by
      analysis and exposes bugs early by placing checks at the          using tagged pointers and memory tags (typically 16:1 gran-
      location where the type system expects safety guarantees          ularity). Each block carries a tag in shadow memory, and
      to hold (§4).                                                     the upper pointer bits hold a matching tag; a mismatch sig-
   • An architecture based on a modified Rust compiler that             nals a violation. Retagging freed memory improves temporal
      allows for analyses across multiple intermediate repre-           detection, while spatial detection remains probabilistic and
      sentations of Rust and LLVM to implement the concept,             depends on tag size. On ARM, HWASan commonly lever-
      including an efficient algorithm for finding potentially          ages top-byte-ignore (TBI) to store tags in the pointer’s top
      deallocating functions (§5).                                      byte, improving compatibility with non-instrumented code
   • A systematic evaluation using LLVM’s widely-used                   and avoiding address-translation issues.
      HWASan on popular Rust crates, known vulnerable Rust
      code, and a set of microbenchmarks. Compared to the
      state of the art, we demonstrate that SafeFFI signifi-
      cantly reduces the compile time (2.64× compared to                2.2    Memory Safety and Rust
      over 8.83×), increases the rate of elided checks (up to
      98%), and consequently reduces the run-time overhead              Rust is a modern systems programming language that aims to
      (from 3.22× to 2.51× on average) (§6).                            eliminate memory safety bugs through a strong static type sys-
                                                                        tem. This type system is built on the principles of ownership,
2     Background                                                        borrowing, and lifetimes [16] which guarantee spatial and
                                                                        temporal memory safety for safe pointer-like types. Spatial
We now introduce the necessary background on memory                     safety in Rust is enforced either at run-time or at compile-time.
safety in C/C++ and existing methods for runtime sanitization           For statically-sized memory objects, the size of the memory
(§2.1), followed by revisiting the memory safety guarantees             object is known at compile-time. The Rust compiler tracks
in Rust and the impact of unsafe code (§2.2).                           the object’s type and its corresponding size for every safe
                                                                        pointer derived from the memory object. Thus, it can stati-
                                                                        cally verify that a pointer dereference is within the bounds of
2.1    Memory Safety and C/C++
                                                                        the pointed-to memory object. For dynamically-sized types,
C and C++ remain widely used in security-critical software              the compiler generates runtime bounds checks when indexing
but inherently lack memory safety. Memory safety violations             or dereferencing through a safe pointer. Temporal safety is
are classified into spatial (e.g., buffer overflows) and temporal       guaranteed by the type system which enforces that each value
(e.g., use-after-free) errors. To catch memory safety bugs, san-        is owned by exactly one variable. The compiler takes care
itizers [40, 42] typically instrument code at compile time with         of generating code for the deallocation of the value at the
additional check logic to detect violations at runtime. Fur-            location where this owning variable goes out of scope which
thermore, sanitizers often use symbol interposition to redirect         prevents double-free errors. Lifetimes tracked statically by
function calls to instrumented versions of a library function,          the compiler ensure that references to a value do not outlive
e.g., for malloc, free, or memcpy. This technique is called             the owner, hence preventing Use-After-Free (UAF) errors.


                                                                    2
                         Call Graph Generation (modular)

                                                                                Sanitizer Pass
                                       Dealloc Annotation
                                           (modular)        Annotated
                                                             LLVM IR                                   Protected
                                                                                 isSafePtr(p)
                                                                                                       Optimized
         Rust                             Pointer Type
                              MIR                                                                       Binary
         Code                              Annotation                                                                  Link    Protected
                                                                                    Check                                     Optimized
                                          Pointer Cast                             Hoisting                                   Executable
                                                                                                      Sanitizer
                                           Detection                             Pointer Type         Runtime
                                         MIR Lowering                             Analysis          safeffi_ensure()
          C           rustc                                 LLVM IR              SafeFFI Lib
         Code
                                     clang                                   LLVM Instrumentation


Figure 1: SafeFFI Architecture Overview. Rust and C/C++ are compiled to LLVM IR, a common intermediate representation for
sanitizer instrumentation. The orange boxes depict our extensions to rustc and LLVM in this compilation workflow.


Safe Pointer-Like Types. The Rust language provides a                   scenarios, the Rust compiler offers the possibility of using
set of safe pointer-like types that are subject to the borrow           memory-safety sanitizers (see §2.1). However, these sanitiz-
checker and lifetime analysis. These include:                           ers lack awareness of Rust’s static guarantees and therefore
   • &T – shared, immutable reference                                   redundantly check even safe Rust code. This motivates our
   • &mut T – exclusive, mutable reference                              approach to combine Rust’s compile-time guarantees with
   • Box<T> – owning pointer to heap-allocated data                     selective run-time checks of sanitizers.
   • [T; N] – statically sized array
   • &[T], &str – dynamically sized slice/string                        Memory Safety in Mixed-Language Applications. A typ-
   • &dyn Trait – trait object reference, a pointer to an ob-           ical scenario of using unsafe code in Rust is the invocation
     ject whose type is only known at runtime                           of foreign functions written in other languages like C/C++.
   • Function pointers and closures                                     Rust provides a feature called Foreign Function Interface
In the remainder of the paper, we will usually refer to these           (FFI) which allows declaring or exporting a function sym-
types summarily as safe pointers, in contrast to raw pointers.          bol from/to a foreign library which later is linked in by the
   For pointers of these types that originate in safe Rust code,        linker.Many real-world applications combine Rust with ex-
the Rust compiler ensures that they are non-null, properly              isting C or C++ code (or vice versa) this way – they are
aligned, and dereferenceable for the size of their pointee-             called Mixed-Language Applications (MLAs). Raw pointers
type [7]. When safe pointers are derived from raw point-                are used heavily to exchange data across the FFI boundary
ers, which may happen in unsafe code, Rust requires the                 because they have the same layout in Rust as in C/C++. Bugs
developer to guarantee those same memory safety properties.             in the FFI definition or in the C/C++ code parts of an MLA
                                                                        can undermine Rust’s guarantees and thus affect the safety
                                                                        of the whole application [20]. Even worse, cross-language
Raw Pointers and Unsafe Code. Rust also provides an-                    vulnerabilities can be vehicles for bypassing hardening mech-
other primitive pointer type, called the raw pointer: *const            anisms for C/C++ like Control-Flow Integrity (CFI) [24, 34].
T and *mut T. The raw pointer type is not subject to borrow             For MLAs, memory-safety sanitizers are applicable to protect
checking or lifetime tracking. It does not provide any memory           the whole application because Rust code and C/C++ code can
safety guarantees, thus it behaves exactly like a pointer in            both be compiled to LLVM IR code, which sanitizers like
the C/C++ and also has the same layout. Raw pointers may                ASan and HWASan can instrument.
only be dereferenced inside functions or code blocks that are
marked with the unsafe keyword in Rust.Besides dereferenc-
ing raw pointers, unsafe Rust code also enables the follow-             3   Overview
ing operations which can undermine Rust’s safety guarantees:
1. calling other unsafe functions or foreign functions, 2. ac-             Figure 1 shows an overview of SafeFFI’s architecture. It is
cessing mutable static variables, 3. accessing union fields,            implemented as an extension of the Rust compiler pipeline.
4. implementing unsafe traits. Those unsafe operations can              We extend the Rust compiler by an analysis of Rust’s Mid-
undermine Rust’s typesystem. Thus, within unsafe blocks, it             Level Intermediate Representation (MIR) to determine the
is the programmer’s responsibility to uphold Rust’s memory-             types of all pointers, locate pointer cast locations, and gen-
safety guarantees. Because programmers can make mistakes                erate corresponding annotations for the LLVM IR code that
in unsafe code, Rust programs might introduce memory-                   is lowered from the MIR. We extend LLVM by our new
safety violations despite Rust’s strong type system. For such           SafeFFI-Lib which consumes the pointer type annotation,


                                                                   3
   1   fn foo(p: &i32) {                      1   define @foo(ptr %p) {                 x    1   define @foo(ptr %p safePtrArg(4)) {
   2                                          2   start:                                     2   start:
   3       let n: i32 = *p;                   3    sanitizer_check(%p)                       3    %n = load i32, ptr %p
   4       let raw1: *mut SomeStruct =        4    %n = load i32, ptr %p                     4    %raw1 = call @c_create(i32 %n) !raw
   5         unsafe { c_create(n) };          5    %raw1 = call ptr @c_create(i32 %n)        5    %raw1_safe = call safeffi_ensure(ptr raw1,
   6       let safe1: &mut SomeStruct =       6                                                        i64 16) !safe
   7         unsafe { &mut *raw1 };           7    %a = GEP ptr %raw1, i64 8                 6    %a = GEP ptr %raw1_safe, i64 8
   8
                                              8    %b = GEP ptr %raw1, i64 12                7    %b = GEP ptr %raw1_safe, i64 12
   9       let a: &mut i32 = &mut safe1.a;    9    sanitizer_check(%a)                       8    %0 = load i32, ptr %a
  10       let b: &mut i32 = &mut safe1.b;   10    %0 = load i32, ptr %a                     9    %1 = load i32, ptr %b
                                                   sanitizer_check(%b)                            call @do_some(i32 %0, i32 %1)
           do_some(*a, *b);
                                             11                                             10
  11
                                             12    %1 = load i32, ptr %b                    11    br label %bb3
  12
                                             13    call @do_some(i32 %0, i32 %1)            12
  13
                                             14    br label %bb3                            13
  14
                                             15                                             14
  15       loop {
                                             16                                             15
  16         let c: &i32 = derive(a);
                                             17   bb3:
                                                                                        x   16   bb3:
  17         let d: &i32 = derive(b);
                                                   %c = call ptr @derive(ptr %0)                  %c = call ptr @derive(ptr %0) !safe
             if *c + *d == 85 {
                                             18                                             17
  18
                                             19    %d = call ptr @derive(ptr %1)            18    %d = call ptr @derive(ptr %1) !safe
  19             break;                      20    sanitizer_check(%c)                      19    %_14 = load i32, ptr %c
  20         }                               21    %_14 = load i32, ptr %c                  20    %_15 = load i32, ptr %d
  21       }                                 22    sanitizer_check(%d)                      21    %_13 = add i32 %_15, %_14
  22   }                                     23    %_15 = load i32, ptr %d                  22    %2 = icmp eq i32 %_13, 85
  23
                                             24    %_13 = add i32 %_15, %_14                23    br i1 %2, label %bb6, label %bb3
                                             25    %2 = icmp eq i32 %_13, 85                24

                   (a) Rust Code             26    br i1 %2, label %bb6, label %bb3         25
                                             27                                             26
                                             28   bb6:                                      27
                                             29     ret void                                28   bb6:
                                             30   }                                         29     ret void
                                             31                                             30   }
                                                                                            31

                                                   (b) LLVM IR with sanitizer checks
                                                                                            (c) Modified LLVM IR with sanitizer checks be-
                                                                                            ing hoisted by SafeFFI

           Figure 2: A simplified example that shows which sanitizer checks can be elided using our SafeFFI optimization


conducts a pointer type analysis on LLVM IR level, inserts                 10, two more safe pointers a and b are derived from safe1
additional sanitizer checks at the boundary between safe and               by taking the respective addresses of the fields defined in
unsafe pointer types, and provides a simple API for existing               SomeStruct. Both are then dereferenced in line 11 to pass
sanitizers to elide checks for provably safe pointer types. A              their pointee values to the function do_some(). Those deref-
more detailed description of the architecture is given in §5.              erence operations correspond to the load instructions in lines
                                                                           10 and 12 of Figure 2b. One can see how the sanitizer inserts
                                                                           sanitizer_check() calls before each load instruction. Be-
Example. We intuitively illustrate the effect of SafeFFI us-               cause Rust’s static type system guarantees that safe1 and its
ing the example in Figure 2, which contains Rust source code               derived pointers a and b only ever access the memory object
of a function foo, the corresponding LLVM code including                   within the bounds of the SomeStruct object, those sanitizer
sanitizer checks, and the same LLVM code after optimiza-                   checks can be elided. However, to be able to rely on the type
tion with SafeFFI. In its normal operation, the sanitizer inserts          system’s soundness, we have to ensure that its requirements
sanitizer_check() for the pointer operands in every LLVM                   are upheld when casting raw1 to safe1 by inserting a san-
load or store instructions. By using information from Rust’s               itizer check. This is depicted by the blue arrows: SafeFFI
typesystem, SafeFFI can deduce that pointers a, b, c, and d                removes the checks before the load instructions and instead
are all derived from a Rust reference safe1. The Rust type                 inserts the safeffi_ensure() call in line 5 of Figure 2c.
system is guaranteeing that all derived references only ever                  The safeffi_ensure() function takes the raw1 pointer
access memory within the bounds and lifetime of the object                 as input as well as the size of the SomeStruct type (in this
they are derived from. Therefore, if we can ensure that the                case 16) and internally uses a sanitizer check to validate that
requirements of Rust’s type system (see §2.2) are met for the              the memory object behind raw1 is still allocated, has at least
creation of the original safe pointer-like, then all subsequent            the expected size, and that the pointer has the correct prove-
sanitizer checks are obsolete and we can elide them.                       nance for this object. If the safeffi_ensure() check fails,
   In source line 7 of Figure 2a, the safe pointer                         we immediately abort the program, pointing the developer
safe1: &mut SomeStruct (a mutable reference) is created                    directly to the cast location. This is a specific advantage of
by casting from the raw pointer which has been returned from               SafeFFI: it can reveal a misuse of unsafe code or FFI code
calling the unsafe function c_create(). Later, in lines 9 and              much earlier compared to normal sanitizer operation. Regular


                                                                       4
sanitizers only fail at the dereference location which might          time of the cast and then continue to rely on the guarantees
happen much later, e.g., in a subsequent function call, making        statically enforced by the Rust compiler for the remaining
the error harder to debug.                                            lifetime of the safe pointer after the cast. Hence, we consider
   If the safeffi_ensure() succeeds then it returns a new             these cast operations to form the boundary between memory
LLVM value (%raw1_safe in the example) representing the               safety enforcement by the sanitizer and the Rust compiler.
casted safe version. Usually, the Rust compiler would only            Casts from raw to safe pointers are the central point of focus
generate one LLVM variable to represent both the raw and the          for SafeFFI, and in the following we show how to hoist the
safe pointer as an optimization, because they have the same           sanitizer checks for safe pointers by protecting this boundary
machine layout and carry the same value. SafeFFI allows us            with a specific sanitizer check.
instead to differentiate raw and safe pointers on LLVM IR
level and to elide sanitizer checks accordingly.
   In the following section, we give a detailed explanation of
                                                                      4.2    Local Type Analysis for Check Hoisting
our approach to determine in which cases sanitizer checks             The basic idea of SafeFFI’s optimizations is to use function-
can be elided and when the boundary between raw and safe              local pointer type information provided by annotation of local
pointers needs validation at run-time by inserting additional         variables, globals, and arguments to reduce the number of san-
sanitizer checks.                                                     itizer checks for safe pointers. Usually, the sanitizer inserts
                                                                      checks at every instruction that dereferences a pointer. For
4     Typesystem-Guided Sanitizer Checks                              raw pointers, we just keep all those checks in place. For safe
                                                                      pointers, we hoist the checks from the dereference location up
Now we explain our concept in detail. We begin by motivating          to the beginning of their scope, where they are created. Then,
pointer casts as logical boundaries for memory safety enforce-        based on the rules enforced by Rust’s type system, we can
ment (§4.1). We introduce our method for using function-local         safely elide all subsequent checks.
type information to hoist checks to casts while eliding sani-            We differentiate the following cases of how a safe pointer
tizer checks for safe pointers (§4.2) and discuss additional          can be created in the current function’s scope:
measures required for full temporal memory safety (§4.3).              (a) Allocating a new stack object. On LLVM-IR level this
Finally, we show how to leverage the Rust type system to                    corresponds to an alloca instruction which returns a
maintain memory-safety across function calls without expen-                 pointer variable.
sive whole-program analysis (§4.4). Note that this design              (b) Deriving a reference from a local stack object or from
includes full support for the presence of unsafe foreign code               another safe Rust reference.
in mixed-language scenarios.                                           (c) Casting a raw pointer to a reference via a Reborrow
                                                                            operation (safe_ptr: &T = &*raw_ptr) or to a Box
                                                                            via Box<T>::from_raw(raw_ptr). Although its syntax
4.1    Memory Safety Enforcement Boundaries
                                                                            looks like a dereference-and-take-address operation, a
Incorrect memory access through raw pointers can cause                      Reborrow just creates a reference that points to the same
memory bugs even in safe Rust [26]. Raw pointer derefer-                    memory object as pointer a1, without dereferencing.
ences are dangerous because Rust does not enforce any guar-            (d) Loading a safe pointer from memory, e.g., as a field of
antees for raw pointers. For safe pointers, however, the Rust               another object that resides in memory.
compiler provides the following memory-safety guarantees              In cases (a) and (b), Rust takes care of memory management
(see §2.2):                                                           through its lifetime and borrowing mechanics and no explicit
   • Spatial safety: every read or write through such a pointer       raw pointers are involved, so we can elide all checks. In case
     is guaranteed to only access memory inside the bounds            (c), we have to ensure the validity of the raw pointer before
     of its pointee type.                                             we can safely cast it to a safe pointer and rely on the Rust
   • Temporal safety: no safe pointer can exist outside the           compiler for memory safety. To check the validity of safe
     lifetime of its original pointed-to memory object.               pointers casted from raw pointers, SafeFFI emits a call to
There are multiple ways to create and derive safe pointers.           safeffi_ensure(), a custom dynamic check function using
All of them are checked by the Rust compiler, except for              sanitizer metadata to determine whether the object pointed
the cast from raw pointer to safe pointer. Casts from raw to          to by the raw pointer is still alive and is at least of the size
safe pointers can only happen in unsafe Rust code, where              of the pointee type T. For case (d), we also need to insert
the Rust compiler does not check that the raw pointer adheres         a sanitizer check. Since unsafe Rust or foreign code can
to the requirements of the safe pointer type. Thus, a cast            arbitrarily modify memory contents, pointers stored on either
of an invalid raw pointer can undermine the memory safety             heap or stack might be corrupted, so we must check their
guarantees of Rust’s type system.                                     validity when they are loaded into the current function scope.
   The key idea behind SafeFFI is that using sanitizer checks,           As a result, we elide sanitizer checks at dereference loca-
we can dynamically guarantee validity for a raw pointer at the        tions for safe pointers; if the pointer is not safe by construc-


                                                                  5
tion, we insert a sanitizer check at the creation site of the safe       number of instructions in the analyzed function. To determine
pointer, effectively combining and hosting the checks. This
is illustrated by the arrows in Figure 2. The run-time benefit            Algorithm 1: Insert additional heap checks for Free-
of removing the sanitizer checks is most pronounced when                  During-Scope violations.
checks can be hoisted out of loops.
                                                                            Input: A Rust function F and the set DeallocFns of
                                                                                   functions that may (transitively) lead to heap
Spatial Safety. The inserted sanitizer check enforces the                          deallocation
size requirement of the safe pointer type at the cast site.              1 foreach memInst ∈ MemoryInstructions(F) do
Once the safe pointer is created, we can rely on the Rust                2     foreach callInst ∈ memInst.operands() do
type system to ensure that all subsequent accesses through               3         if hasSafePointerOperand(memInst) then
the safe pointer in the current function are within the bounds           4             if callInst.callee() ∈ DeallocFns then
of the type, as explained above. Thus, SafeFFI ensures spatial           5                 if IsReachable(memInst, callInst) then
safety for the whole scope of the safe pointer (to the extent             6                     InsertCheckAt(memInst, callInst);
that the underlying sanitizer guarantees it).

Temporal Safety. For reasoning about temporal safety,
we distinguish Free-Before-Scope vulnerabilities from Free-              the set DeallocFns of functions that may transitively lead to a
During-Scope vulnerabilities. So far, we combined the Rust               heap deallocation, we develop an efficient and sound analy-
type system with dynamic sanitizer checks to ensure that any             sis for constructing the call-graph, which executes on-the-fly
safe pointer points to a memory object that is alive at the              during compilation (see §5.4 for a detailed description).
start of the pointer’s scope. Thus, SafeFFI always reliably                 In single-threaded applications, inserting additional
detects all temporal vulnerabilities where the memory ob-                safeffi_ensure() checks guarantees that each safe pointer
ject is deallocated before the start of the pointer’s scope, i.e.,       remains valid throughout its scope, allowing SafeFFI to reli-
Free-Before-Scope vulnerabilities. If the memory object is               ably detect Free-During-Scope violations. For Free-During-
deallocated during the safe pointer’s scope, e.g., through an            Scope violations, check hoisting is not thread-safe, however. A
alias pointer, this can cause a Free-During-Scope vulnera-               deallocation could occur concurrently between the check and
bility. To also catch these, SafeFFI provides the option for             the subsequent dereference, which could allow a Free-During-
further checks, as we explain in the next section.                       Scope violation to go undetected. Nevertheless, SafeFFI re-
                                                                         mains fully compatible with multi-threaded programs and is
4.3    Catching Free-During-Scope Violations                             guaranteed to detect spatial and Free-Before-Scope violations
                                                                         to the extent that the underlying sanitizer does.
For Free-During-Scope violations, we need to check that the
safe pointer remains valid until the end of its scope. SafeFFI
provides the option to detect Free-During-Scope violations               4.4    Interprocedural Memory Safety
which allows developers to trade safety for run-time and
compile-time performance.                                                Intraprocedurally, SafeFFI establishes a safety invariant for
   In Rust, memory may be deallocated either by popping a                every safe pointer created in each function: each safe
stack frame at the end of a function scope or by calling a               pointer created in the current function is guaranteed to be
heap deallocation function. We reason about a safe pointer’s             safe to dereference for its whole scope in the current function.
local scope within the current function—we will extend our               To guarantee whole-program memory safety, we also need to
reasoning across function calls in §4.4. Because the safe                ensure validity of safe pointers passed across function calls.
pointer’s scope is limited to the current function, this stack
frame is guaranteed to not be deallocated within the entire              Pointer Arguments. SafeFFI generates annotations for the
scope. Thus, only heap deallocations remain for potential                function signature during lowering from MIR to LLVM
Free-During-Scope violations.                                            IR, emitting attributes for pointer parameters (e.g., see the
   Heap deallocation requires calling __rust_dealloc() or                safePtrArg attribute in line 1 of Figure 2c for the parame-
libc::free(). Hence, a safe pointer can only become dan-                 ter p: &i32). When the currently analyzed Rust function is
gling within its scope in the current function if there is a call        called from another Rust function, the type system guarantees
to one of those deallocation functions in between. To detect             that the argument types in the call and the function signature
Free-During-Scope violations, SafeFFI inserts an additional              match, so functions with safe pointer arguments will only
safeffi_ensure() check for every dereference of the safe                 ever receive safe pointer values from the caller.
pointer that is reachable from a call to a potential deallocation           For Rust functions with external visibility, which can be
function. Algorithm 1 for inserting those heap checks can                called by foreign code, invalid data could be passed to a pa-
be implemented efficiently within LLVM and is linear in the              rameter of a safe pointer type, because linking foreign code


                                                                     6
requires only ABI compatibility and may ignore types. There-              1       // C code
fore, SafeFFI inserts an additional check in the prologue of the          2       void* c_derive(int* n) {
                                                                                    int* p = n;
callee to ensure that the safe pointer is indeed valid. Because           3
                                                                          4         ...
of our established memory safety invariant, we guarantee that             5         return p;
                                                                                  }
safe pointers are indeed safe to dereference for the remainder            6
                                                                          7
of the scope of the caller function, which means they are also            8       // Rust code
                                                                          9       fn derive(_: &'a i32) -> &'a i32 {
valid for the whole scope of the callee. Hence, we can elide             10         let n = 42;
all sanitizer checks for safe parameters.                                11         // p points to n on the stack
                                                                         12         let p: *const i32 = unsafe { c_derive(&n as *const i32) };
                                                                         13         __safeffi_ensure(p, sizeof(i32));
                                                                         14         // at this point, *p is still valid, so cast check succeeds
Pointer Return Values. Similar to the previous case, we                  15         let p_safe: &i32 = unsafe { &*p };
can rely on the Rust type system to guarantee that the return            16         return p_safe;
value of a function call is of the correct type. Because of our          17         // n is deallocated here, so the p_safe pointer is now
                                                                                        dangling
invariant, we can guarantee that a safe pointer returned from            18       }
a function call is valid until the end of its scope in the callee.       19
                                                                         20       fn foo() {
And if the pointer is valid at the end of the callee, then it is         21         ...
also valid at the return in the caller—with one exceptional              22         let b: &i32 = derive(a);
                                                                         23         // additional check catches invalid pointer
case that needs special handling.                                        24         __safeffi_ensure(b, sizeof(i32));
                                                                         25
   Each return instruction is also the deallocation of the               26       }
callee’s stack frame. If the safe pointer is derived from a raw
pointer pointing to an object on that same stack frame, then
                                                                         Figure 3: Example of a stack temporal violation that SafeFFI
this creates a stack Use-After-Return (UAR) violation because
                                                                         catches by inserting an additional sanitizer check after the
by the time the safe pointer is received in the caller func-
                                                                         pointer returned in the caller function foo().
tion, the pointed-to memory object on the callee’s stack frame
is already deallocated. Figure 3 shows an example of such
a stack temporal violation. The call to function derive()                   The goal for our architecture was to make integra-
returns a safe pointer which has been derived from a raw                 tion with existing sanitizers as easy as possible by re-
pointer pointing to an object on the stack frame. Because the            quiring only minimal changes to the sanitizer: 1. query-
developer did not choose the correct lifetime for the returned           ing pointer types via is_safe_pointer(Value* ptr) in
pointer in the derive() signature and because foreign C code             SafeFFI-Lib, and 2. providing a run-time check implementa-
is involved, the Rust compiler has no chance at preventing this          tion safeffi_ensure(void* p, u64 size). This way, our
UAR violation. To catch such violations, SafeFFI inserts an              architecture increases the chance of adoption.
additional safeffi_ensure() check after every function call
that returns a safe pointer. Thus, we can now guarantee that
the safe pointer is valid for the scope in the caller function.          5.1          Pointer Type Annotation in MIR
                                                                         Our goal is to know the type of every pointer in LLVM IR,
                                                                         because for every pointer, the sanitizer can potentially request
5   SafeFFI’s Implementation                                             the type via the isSafePtr() API of SafeFFI-Lib. Thus we
                                                                         have to annotate local variables, function arguments, global
In this section, we describe the architecture and implemen-
                                                                         variables, and constants. We implement this by associating
tation details of our approach. We implemented SafeFFI as
                                                                         LLVM metadata nodes (MDNode) with the corresponding gen-
modifications to the Rust compiler version 1.52.0 and LLVM
                                                                         erated LLVM instructions and LLVM Attributes for func-
version 12. The blue boxes in Figure 1 highlight how SafeFFI
                                                                         tion parameter values.
integrates into the Rust and LLVM toolchain.
                                                                            For this we hook into the lowering process from MIR
   First, rustc lowers Rust source code to the Mid-Level In-
                                                                         to LLVM IR. The lowering process is implemented in
termediate Representation (MIR) which is where the Rust
                                                                         rustc via the visitor pattern: the rustc_codegen_ssa mod-
type system implements its static checks, aka. the Borrow
                                                                         ule visits MIR statements and calls the functions in
Checker. While MIR is then lowered to LLVM IR SafeFFI
                                                                         rustc_codegen_llvm (the LLVM backend interface) to gen-
attaches pointer type annotations and inserts sanitizer checks
                                                                         erate the corresponding LLVM IR. The challenge lies in the
for pointer casts. The LLVM IR is processed by standard
                                                                         loose connection between MIR symbols and corresponding
optimization and sanitizer passes, and finally linked with the
                                                                         LLVM symbols because the lowering of an MIR symbol
sanitizer runtime. In mixed-language applications, C code is
                                                                         depends on the target ABI of its type. The Rust compiler
compiled to LLVM IR and linked in the same way. Further
                                                                         differentiates between the following ABIs for any MIR type1 :
details on each component are described in the following
                                                                              1
subsections.                                                                      There is no official specification of Rust, thus we have to take the


                                                                     7
   • Uninhabited: a zero-sized type, that actually does not                 sequences of LLVM instructions like GEP, BITCAST, LOAD.
      exist in memory. No LLVM code will be generated for                   Since the Rust compiler does not track all LLVM instructions
      it, so there is nothing to annotate.                                  generated for a MIR value, SafeFFI annotates only the final
   • Scalar: a type that is represented by a single LLVM                    LLVM value representing the loaded MIR operand, lacking
     value. If this is a pointer type (also called thin pointer),           pointer type annotations for intermediate LLVM pointer val-
      then we annotate it accordingly. This is the case for                 ues. Thus, in SafeFFI-Lib, we implement an intra-procedural
      references and arrays, and raw pointers but it is also the            pointer type analysis that forwards the types (safe, raw, and
      case for all ADT types that are represented by a single               NOPTR) throughout each function. This analysis initializes a
      pointer value in LLVM IR, e.g. the Box<T> or any custom               map of pointer types using the annotations inserted by the
      arbitrarily nested struct that only has one field and that            Rust compiler for Alloca Instructions, Call/Invoke instruc-
      field is a pointer. A special case of this is Rust’s Union            tions, function parameters, and global variables. Then, for
      type. If it has a Scalar ABI, then we can only annotate               every remaining LLVM instruction that produces a pointer
      it as safe if all of its fields are safe pointers, otherwise          value (BITCAST, GEP, INTTOPTR, PHI), SafeFFI forwards
      the pointer value could be manipulated in an unsafe way               the type from the operands of the instruction to the resulting
      through another type representation like an integer or a              pointer based on the semantics of the instruction. The GetEle-
      raw pointer. We implemented a recursive type analysis                 mentPointer (GEP) instruction, which computes a derived
      to detect such cases.                                                 pointer by offsetting a base pointer, is handled more carefully:
   • ScalarPair: a type that is represented by two LLVM                     if the base pointer is raw, the result is always marked as raw.
      scalar values, mostly dynamically-sized types (e.g.                   If the base pointer is safe, we attempt to statically compute
      slices) which are lowered to fat pointers which contain               the offset and check whether it remains within the bounds
      a data pointer and a dynamic size value. As we cannot                 of the original allocation. If so, SafeFFI marks the result as
      reason about the dynamic size of such types, SafeFFI                  safe and otherwise conservatively downgrades it to raw.
      annotates them as raw. We leave it to future work to                      As a result, every pointer value in LLVM IR is classified as
      find further optimizations to elide checks for such types.            safe, raw, or NOPTR, enabling the sanitizer to reliably query
      However, in the case of Trait objects (&dyn Trait) the                pointer types via the isSafePtr() API.
      second value is a vtable pointer. Because it is lowered
      to a LLVM pointer, we need to annotate it too. Because
      the vtable pointer is not user-manipulated but generated              5.3    Pointer Cast Detection in MIR
      and managed by the compiler, we always annotate it as                 The goal of this component is to detect casts from raw pointers
      safe.                                                                 to safe pointers in MIR. Our definition of safe pointers dis-
   • Vector: those are only used for LLVM’s SIMD vector                     tinguishes 3 types of pointers: References, Boxes, and static
      types, which are not relevant for our approach.                       arrays. Raw pointers cannot be casted to static arrays (only to
   • Aggregate: a type that is represented by custom LLVM                   references to static arrays), thus, we only have to detect the
      structs. Those types are actually no pointers in MIR,                 following two cases. 1. Casting a raw pointer to a Box: This
      however, if a local variable of an Aggregate type is                  always has to happen through a call to Box::from_raw(p)
      allocated on the stack using a LLVM alloca instruction,               which is an explicit statement in MIR. 2. Casting a raw
      then a LLVM pointer is created to represent this variable.            pointer to a reference: This too is always an explicit statement
     We are annotating them with a NOPTR tag and treat them                 in MIR, because Rust does not allow implicit coercion in this
      as always safe because they cannot be user-manipulated                case [8]. In MIR this pattern looks like q = &*p, where &
      because they are compiler-generated pointers.                         denotes the creation of a reference and * denotes a derefer-
   The ABI of the type and the calling convention also dic-                 ence operation. Because the dereferenced p can be any kind
tate how a value is passed or returned as function argument                 of Rust pointer, we have to check if p actually has the raw
in a call. Fortunately, the Rust compiler already annotates                 pointer type to confirm this is a cast.
parameters of the function signature if they are safe to deref-                With both cast types, p can be a projection, e.g., the ac-
erence using LLVM’s dereferenceable(<size>) attribute                       cess of a field of a (nested) struct (&*a.b.c) or an array
from which we inherit our annotations.                                      (&*x[y][z]).SafeFFI determines whether the inner-most ele-
                                                                            ment is a raw pointer by iterating over the MIR projections
5.2    Pointer Type Analysis on LLVM IR                                     until we find the type of the accessed element.
                                                                               We implement the pointer cast detection by hooking into
A further challenge is that the ABI of MIR types also controls              the MIR visitor for Rvalues (right-hand-side values) of MIR
how values are loaded from memory. For example, access-                     Assign statements. During lowering of an RValue, the Rust
ing a MIR field (let a = safe1.a) can generate different                    compiler generates a series of LLVM IR instructions, the last
Rust compiler’s behaviour as reference: https://github.com/rust-lang/       of which producing an LLVM Value that corresponds to the
rust/blob/1.52.0/compiler/rustc_target/src/abi/mod.rs#L847                  MIR Rvalue. For each Rvalue, Rustc keeps a mapping from


                                                                        8
                     SCC Analysis                                         To address this, we implemented a call-graph-based heap
                                append                                 deallocation analysis in LLVM to determine whether a given
        Crate C
                                              funcC1()                 function may perform a deallocation. It analyzes bottom-up
                                 read         funcC2()
   depends                                                             over the call graph: functions without call instructions are
                                append
                                                                       visited first. The analysis is implemented as a LLVM SCC
                                              funcB1()
        Crate B                                                        (strongly connected components) pass because the call graph
                                              funcB2()
                                read                                   might contain cycles. A function is annotated as nofree if it
   depends                                Free Functions               does not contain any calls to: (i) known deallocation functions
                                                File
                                                                       (e.g., free() or __rustc_dealloc()), (ii) functions without
        Crate A
                                                                       a nofree annotation, or (iii) unknown callees. If any function
                                                                       within an SCC cannot proven to be nofree, then the entire
Figure 4: The NoFree SCC Analysis is performed on all                  SCC treated as potentially deallocating.
dependencies to determine possibly heap-deallocating func-                Another challenge is that deallocations can happen outside
tions.                                                                 the current compilation unit, e.g., in a Rust dependency or
                                                                       external C library, and thus are not visible to the current com-
                                                                       pilation process. To address this, we serialize the nofree anno-
the MIR Rvalue to the corresponding LLVM value. This is                tations to a persistent file after the analysis has finished for the
where SafeFFI inserts a sanitizer check for pointer casts by           current compilation unit. Subsequent compilation processes
extending the series of generated LLVM instructions with a             read in the serialized annotations and restore them before
call to the safeffi_ensure() function.                                 running the analysis. This compositional cross-crate analysis
   We show this effect in Figure 2. The raw pointer raw1               is illustrated in Figure 4. To support C/C++ dependencies, we
is lowered by generating a call to c_create() in Fig-                  provide build flags for clang to include our analysis. When
ure 2b line 5 and its returned LLVM value %raw1 is                     C dependencies are dynamically linked or precompiled, we
mapped for the Rvalue. For lowering the pointer cast                   conservatively assume all external C functions may perform
safe1 = unsafe &mut *raw1 the Rust compiler usually                    deallocations. bin
just maps the Rvalue to the same value as the raw pointer
because there is no difference in the LLVM representation of
a raw pointer and a safe pointer. Thus, in lines 7 and 8, the          6    Evaluation
LLVM value %raw1 is used to access the fields of the safe1
                                                                       We implemented SafeFFI on top of Rust nightly-2021-02-
reference. One can see how this is changed by SafeFFI in
                                                                       22, which corresponds to Rust compiler version 1.52.0 and
the Figure 2c lines 5-7. Our rustc modifications insert the
                                                                       LLVM version 12. We integrated SafeFFI into HWASan be-
safeffi_ensure() call and generate a new LLVM value
                                                                       cause it is the sanitizer with the best detection capabilities
%raw1_safe. SafeFFI then replaces the RValue mapping for
                                                                       under the maintained sanitizers [42]. Because HWASan uses
cast operation, now mapping to %raw1_safe. Thus, the sub-
                                                                       ARM-specifc hardware features, we ran all experiments with
sequent accesses of the fields behind the safe pointer safe1
                                                                       SafeFFI on a MacStudio M2 Ultra with 24 ARMv8 cores and
now use the LLVM value %raw1_safe.
                                                                       192 GB RAM running an Ubuntu 20.04 docker container on
   Generating a new LLVM value for the casted pointer has
                                                                       ASAHI Linux 6.12.0. To reproduce results of related work
the advantage that we can now differentiate between the raw
                                                                       as closely as possible and compare to them, we conducted
pointer and the safe pointer on LLVM IR level and separately
                                                                       experiments with ERASan [26] and RustSan [5] on a x86_64
reason about their safety guarantees at every subsequent loca-
                                                                       system—the architecture on which they were developed—
tion of use in LLVM IR. Moreover, our experiments showed
                                                                       running Ubuntu 24.04. We make all datasets, scripts, and
that implementing cast detection on MIR level is the most
                                                                       tools used in our evaluation available for reproduction.
reliable way to detect casts and insert sanitizer checks consis-
                                                                         In this section, we present our evaluation of SafeFFI an-
tently. Other attempts to detect casts by finding differences in
                                                                       swering the following research questions:
pointer type annotations at LLVM IR level have shown to be
                                                                       RQ1 How does SafeFFI affect the detection capabilities of
unstable because type annotations are transported via LLVM
                                                                            the sanitizer (§6.1)?
metadata nodes which can get lost or moved around during
                                                                       RQ2 How many sanitizer checks can SafeFFI reduce in san-
optimization passes in LLVM.
                                                                            itized programs (§6.2)?
                                                                       RQ3 How much can SafeFFI reduce the run-time of sani-
5.4    Callgraph-Based Deallocation Checking                                tized programs (§6.2)?
                                                                       RQ4 Is SafeFFI’s implementation robust in the presence of
As mentioned in §4.3, detecting Free-During-Scope temporal                  FFI interactions in MLAs (§6.3)?
vulnerabilities requires checking that a dereferenced pointer          RQ5 How much compile-time overhead does SafeFFI in-
has not become dangling since its creation.                                 cur (§6.4)?


                                                                   9
6.1       Correctness                                                                              Table 1: Vulnerability Detection




                                                                                                                 INTERCEPT
We answer RQ1 by testing SafeFFI on known real-world




                                                                                                                             HWASAN
memory safety vulnerabilities. We further include RustSan [5]




                                                                                                                                                                 ERASan
                                                                                                                                                       RustSan
                                                                                                                                      SafeFFI


                                                                                                                                                ASAN
and ERASan [26] as related work and ASan as a baseline for
                                                                                             ID
those two approaches. We assembled the dataset of known vul-
                                                                                      CVE-2017-1000430          ✓
nerabilities by merging and deduplicating the datasets used by                        CVE-2018-20991            ✗
ERASan and RustSan. Note that the authors of RustSan have                             CVE-2018-21000            ✓
                                                                                                                                            †
                                                                                      CVE-2019-15551            ✓
not provided their dataset, thus, we manually reconstructed it                        CVE-2019-16140            ✓
based on the RustSec advisories.                                                      CVE-2019-16882            ✓
                                                                                      CVE-2019-25009            ✓
   Table 1 shows the results of our evaluation on the dataset of                      CVE-2020-25574            ✓                           †
                                                                                                                                                       G
                                                                                                                                                       #
known vulnerabilities. # G indicates that the vulnerability was                       CVE-2020-25791            ✓                               #      #         #
                                                                                      CVE-2020-25792            ✓                               #      #         #
detected by the sanitizer, but with a different error message                         CVE-2020-25795            ✓                           †

than the baseline. For example, CVE-2021-30457 is both a                              CVE-2020-35858            ✗
use-after-free and later a double-free. The former is detected                        CVE-2020-35860            ✓
                                                                                      CVE-2020-35861            ✓
by instrumentation and susceptible to check elision while                             CVE-2020-35891            ✗                           †
                                                                                                                                                                 #
the latter is caught by the sanitizer’s interceptor of free().                        CVE-2020-35892            ✓                           †
                                                                                                                                            †
                                                                                      CVE-2020-35893            ✓
Segmentation faults and other signals are classified as not                           CVE-2020-35906            ✓
detected (#), as they imply that a memory error was not                               CVE-2020-36434            ✗
                                                                                                                                            †
                                                                                                                                                       #
                                                                                                                                                       G         #
                                                                                      CVE-2020-36464            ✗
caught by the sanitizer before leading to the crash. SafeFFI                          CVE-2020-36465            ✓
reports some vulnerabilities earlier at the root cause instead of                     CVE-2021-25900            ✓
                                                                                                                                            †
                                                                                      CVE-2021-26954            ✓                                                #
at the access location due to the hoisting of checks (cf. §4.2),                      CVE-2021-28028            ✓                           †
                                                                                                                                                                 #
these cases are classified as detected ( ).                                           CVE-2021-28031            ✓
                                                                                                                                            †
   The results show that SafeFFI catches all vulnerabilities                          CVE-2021-29933            ✓                                                #
                                                                                                                                            †
                                                                                      CVE-2021-30455            ✓
that HWASan detects. Due to hoisting checks to the memory                             CVE-2021-30457            ✗                           †
                                                                                                                                                                 G
                                                                                                                                                                 #
                                                                                                                                            †
safety boundary at the location of pointer casts, SafeFFI is                          CVE-2021-45694            ✗
                                                                                                                                            †
                                                                                                                                                                 #
                                                                                      CVE-2021-45713            ✗                                      #
                                                                                                                                                       G         #
able to report 21 vulnerabilities earlier than HWASan, increas-                       CVE-2021-45720            ✗                           †
                                                                                                                                                                 #
ing debuggability, and it detects one vulnerability where every                       RUSTSEC-2020-0061         ✗            #        #
                                                                                                                                      G         #      #         #
                                                                                                                                            †
other approach fails. Additionally, we have not encountered                           RUSTSEC-2020-0091         ✗                               #      #         #
                                                                                                                                            †
                                                                                      RUSTSEC-2020-0097         ✗                                      #
                                                                                                                                                       G         #
any false positives during the evaluation of the other research                       RUSTSEC-2020-0167         ✓
questions as shown in the following sections, which further                           RUSTSEC-2021-0003         ✓
                                                                                                                                            †
                                                                                      RUSTSEC-2021-0031         ✗
indicates that SafeFFI does not introduce false positives.                            RUSTSEC-2021-0033         ✓                           †
                                                                                                                                            †
   RustSan retains nearly all capabilities of ASan, performing                        RUSTSEC-2021-0039         ✓                                      #
                                                                                      RUSTSEC-2021-0047         ✓            #        #         #      #         #
                                                                                                                                                                 G
slightly worse than HWASan and SafeFFI in a few cases. In                             RUSTSEC-2021-0048         ✓
contrast, ERASan performs significantly worse than SafeFFI                            RUSTSEC-2021-0049         ✓                                                #
                                                                                      RUSTSEC-2021-0053         ✓
and RustSan. We investigated further and discovered that                              RUSTSEC-2022-0070         ✓                                                #
ERASan’s implementation does not properly annotate all un-                            RUSTSEC-2022-0078         ✓
                                                                                                                                            †
                                                                                      RUSTSEC-2023-0005         ✓
safe pointers and therefore removes checks that would have
been necess ary to detect the vulnerabilities. Yet, some vul-                                                                          †
                                                                                      Detected    # Different Error
                                                                                                  G                 # Not Detected       SafeFFI-specific Error
nerabilities are detected because ERASan keeps ASan’s inter-                                        INTERCEPT = Interception-based Detection
ceptors in place, e.g., for free() and memcpy(). We reached
out to the authors of ERASan to debug our findings but have
not received a response.2
                                                                                   same crates (Rust’s term for packages or libraries) as RustSan
                                                                                   for the evaluation. Note that for RustSan, neither the evalua-
6.2       Effectiveness                                                            tion scripts nor the tested versions of the crates are available,
In this section, we provide empirical evidence that SafeFFI is                     thus we chose a common version that both SafeFFI and Rust-
effective in reducing the number of HWASan checks (RQ2)                            San can compile with their respective tool chains. The crates
and, consequently, the run-time overhead of the sanitizer                          Rocket and RustPython are missing because they contain a
(RQ3). We further compare SafeFFI against RustSan. As                              compilation error in the version compatible with Rust 1.52.0
mentioned in §6.1, ERASan incorrectly removes necessary                            and we bundled the libstd tests into a single crate. Elided
checks, leading to a skewed number of elided checks. Thus,                         checks are measured at LLVM IR level. To prevent the stan-
we exclude ERASan from further comparisons. We use the                             dard library from overshadowing the results of smaller crates,
                                                                                   we only count checks outside the standard library and list the
   2
       Github link redacted for review, anonymized screenshot in Appendix B        standard library results separately.


                                                                              10
                     80%       SafeFFI: Unsafe Checks                   SafeFFI: Added Stack Checks                RustSan
                               SafeFFI: Added Cast Checks               SafeFFI: Added Heap Checks
  Remaining Checks



                     60%

                     40%

                     20%

                     0%
                                                                                                                                                       r
                              lib bat -find greptokio cker yper time uuid ronoadlere-xid se64 ageregex rder ytes json syn rand eammchrrown llvec ryumve trsim map teger url
                           Std     fd rip            c r a h sm        c h        o d b a im         t e o b                ss b e hb ma          s e  s dex -in
                                                fire       wa                uni
                                                                                 c                by                     cro m has s                     in num

Figure 5: Sanitizer checks after elision by SafeFFI and RustSan, respectively, as fractions of original checks for individual
packages. For SafeFFI, checks are subdivided into remaining unsafe checks and added cast, stack and heap checks.


Elided Checks. Figure 5 shows SafeFFI’s capability to                                                 runtime overhead of 3.22× (median: 3.03×) compared to
elide sanitizer checks. SafeFFI retains on average 7.38% of                                           an uninstrumented binary. SafeFFI without heap-temporal-
the HWASan checks because they vet an unsafe pointer. Then,                                           safety reduces this overhead to 2.12× (median: 2.06×) and
cast checks (cf. §4.1) and stack checks (cf. §4.4) are added                                          SafeFFI with full temporal-safety to 2.51× (median: 2.24×).
to ensure spatial and stack-temporal memory safety for safe                                           Considering each benchmark individually, SafeFFI improves
pointers. After these checks, on average 10.22% of the checks                                         the run-time by at least 10% across the board, except for four
remain. Adding the optional heap checks for Free-During-                                              crates. Base64 contains a lot of dynamic GEP instructions,
Scope vulnerabilities (cf. §4.3) increases the average number                                         which SafeFFI conservatively overapproximates, as explained
of remaining checks to 21.43%.                                                                        above. For json and hashbrown, the additional heap checks re-
   Compared to RustSan (blue bars in Figure 5), SafeFFI with                                          quired to detect Free-During-Scope vulnerabilities (see §4.3)
full temporal safety elides on weighted average 7.34% more                                            limit the achievable performance improvement, without added
checks, providing a significant improvement over the current                                          heap checks SafeFFI significantly reduces the run-time over-
state of the art. On closer examination, SafeFFI performs bet-                                        head. For regex, none of the added checks are proportionally
ter on 28 benchmarks and worse on 2 benchmarks, exceeding                                             bigger compared to other crates, therefore, we assume that
5% difference on 24 of 28 benchmarks and 1 of 2 bench-                                                some inserted checks are on hot paths in the benchmark exe-
marks respectively. We observe especially large difference                                            cution.
(> 20%) on bytes, ryu, indexmap (in favor of SafeFFI) and                                                Only base64 1/20 for SafeFFI None and 4/20 for SafeFFI
base64 (in favor of RustSan). bytes and indexmap are data                                             not exceeding a 10% improvement in overhead. Unfortunately,
structures with unsafe pointers that alias with safe views re-                                        we could not include benchmarking data for RustSan because
turned by the API. Similarly, in ryu crucial internal buffers                                         the cargo benchmark harness compiled with RustSan con-
make use of unsafe. In these cases, SafeFFI already performs                                          sistently raises segmentation faults during startup. As tar-
better in isolation and the advantage should even increase in                                         get versions and benchmarking scripts are not included in
dependents of these libraries. Furthermore, as ryu contains                                           RustSan’s published code, we also cannot perform a like-for-
no heap allocations, SafeFFI does not need to add any heap                                            like comparioson against the numbers reported in their paper.
checks, which further increases the savings. In contrast, on                                          Deducing from our comparison of elided checks with their
base64 SafeFFI performs significantly worse. The reason is                                            reported results, we suspect that they benchmarked without
that base64 is lowered into many dynamic GEP statements,                                              compiling an instrumented version of the Rust standard li-
which we conservatively overapproximate (cf. §5.2). Note                                              brary which could introduce false negatives and thus distorts
that SafeFFI and RustSan cannot operate in the exact same                                             the comparison.
environment—however, it is unlikely that the differences af-
fect elision rates.                                                                                   6.3   Robustness in MLA Scenarios
                                                                                                      Our experiments on correctness (§6.1) and effectiveness
Run-time Performance. We have shown that SafeFFI is                                                   (§6.2) contain real-world MLAs in the benchmark sets, e.g.,
superior in eliding checks. However, not all checks are equally                                       bat depending on libgit2, rusqlite (CVE-2021-45713) on lib-
important for the run-time, checks on hot paths through the                                           sqlite3, or xcb (RUSTSEC-2020-0097) on libxcb. Since we
program disproportionately impact the run-time [43]. There-                                           did not encounter FFI-related compilation issues nor false
fore, we also evaluate the run-time on several benchmarks.                                            positives/negatives during execution, this is evidence that
Figure 6 shows the run-time overhead of HWASan and                                                    SafeFFI works as designed in MLA scenarios. To be confi-
SafeFFI on the benchmarks. HWASan imposes an average                                                  dent in the robustness of SafeFFI, we created a systematic


                                                                                              11
                              HWASan         SafeFFI w/ heap checks        SafeFFI w/o heap checks
    Run-time Overhead
                        5x

                        4x

                        3x

                        2x

                        1x
                                d     o   er    e     4   ex
                             uui chron adl nicod base6 reg eord
                                                                 er ytes      jso
                                                                                 n       d
                                                                                      ran sbeam
                                                                                                        a    n
                                                                                                     ito row allve
                                                                                                                   c   ryu mver rsim map eger       url
                                                               t    b                      s              hb              se    st    ex    int
                                            u              b y                          co
                                                                                         r            has    s m                   ind num-

Figure 6: Run-time overhead of vanilla HWAsan, SafeFFI (including cast and stack checks), and SafeFFI with added heap checks
compared to baseline run-time without sanitizer.


test set of minimal test cases that cover all common FFI in-                                 commercially available). They elide software bounds checks
teractions between C and Rust that we could conceive of. It                                  emitted by the Rust compiler, but find little benefit due to
covers the following dimensions:                                                             compiler optimizations.
   1. Allocation: Global, C stack/heap, Rust stack/heap;                                        All three approaches annotate pointers during MIR lower-
   2. Deallocation: Global, C stack/heap, Rust stack/heap;                                   ing so that safe and raw pointers remain distinguishable at
   3. Pointer invalidation: pointer arithmetic, deallocation, in-                            the LLVM IR level, with the goal to elide checks for safe
      valid pointer crafting, or no invalidation (benign test);                              pointers. The key difference is that RustSan and ERASan
   4. Control flow permutation: interleaving of pointer casts,                               rely on whole-program static value-flow analysis to compute
      invalidations, and dereferences;                                                       points-to sets, while SafeFFI annotates function parameters
We evaluated SafeFFI on all meaningful combinations of                                       and return values with pointer types, allowing for efficient lo-
these dimensions leading to 45 distinct test cases (35 with                                  cal reasoning. This design significantly reduces compile-time
vulnerabilities, 10 without). All tests are included in the ar-                              overhead and scales better to large code bases.
tifact. SafeFFI is robust against all of those cases, meaning
                                                                                                Moreover, this difference makes SafeFFI significantly more
that it does not raise any false positives or false negatives.
                                                                                             effective at eliding checks. This happens not only because
                                                                                             the static analysis tends to overapproximate, but also for a
6.4                      Compile-Time Performance                                            fundamental reason: Rust code that interacts with unsafe
                                                                                             or foreign code often uses patterns where safe pointers are
Figure 7 shows the compile-time overhead of HWASan,                                          derived from raw pointers or vice versa. RustSan and ERASan
SafeFFI and RustSan, answering RQ5. Note that we chose the                                   need to insert checks for every pointer which shares the same
respective toolchain versions as a baseline for a fair compari-                              points-to set as the raw pointer, inhibiting the elision of checks
son. On average, HWASan induces a compile-time overhead                                      for safe pointers in this case. Our approach, on the other hand,
of 1.69× compared to the baseline. SafeFFI without heap-                                     benefits from the chance that the actual number of raw pointer
temporal-safety increases the overhead to 2.02×. SafeFFI                                     interactions might be small or just unidirectional, because
with full temporal-safety further increases the compile-time                                 SafeFFI just inserts a check at casts from raw pointers to
overhead to 2.64×. The compile-time memory overhead of                                       safe pointers. This makes SafeFFI especially suitable for
SafeFFI is reasonable, with an average of 1.14× compared to                                  scenarios involving unsafe code, e.g., fuzzing Rust crates
the baseline and within measurement deviation compared to                                    that implement efficient datastructures or protecting MLAs.
HWASan. RustSan adds a compile-time overhead of 8.83× on                                     While not explicitly stated, we deem RustSan’s and ERASan’s
average, with outliers reaching an overhead of up to 43.03×,                                 concept also to be applicable to MLAs.
because it performs a whole-program points-to analysis to
identify safe pointers that alias raw pointers. For the same                                    Our concept of hoisting checks to locations of casts and
reason, RustSan also induces a significant memory overhead                                   other safe pointer creations also leads to superior debuggabil-
during compilation of 9.95× on average because bigger crates                                 ity because SafeFFI fails earlier and points developers directly
like wasmtime consuming up to 59.03× more RAM.                                               to a violation of the Rust’s requirements for safe pointers
                                                                                             at the boundary to unsafe or foreign code. Theoretically,
                                                                                             our check hoisting concept introduces a risk of missing Free-
7                       Related Work                                                         During-Scope temporal vulnerabilities (see §4.3), an issue
                                                                                             for which we provide a solution for single-threaded programs
Run-time Check Reduction for Rust. Rust for                                                  by optionally inserting additional sanitizer checks at poten-
Morello [10] executes Rust programs on the CHERI-                                            tial heap deallocation operations. SafeFFI still outperforms
Architecture [44] for hardware-enforced memory safety (not                                   RustSan and ERASan on the evaluated metrics in most cases.


                                                                                      12
                          50x
  Compile-time Overhead

                                                                           HWASan             SafeFFI w/ heap checks         SafeFFI w/o heap checks            RustSan


                          10x
                           5x


                           1x
                                                                       n                       x                  u    r
                                bat -find grep tokio acker yper time sy rand rono beam se64rege mchr rown llvec ry emve trsim bytes map order teger    url uuid e-xid
                                  fd rip             cr   h sm             ch ross   ba         e shb ma          s      s        ex te in                    cod
                                               fir e       wa                c                m
                                                                                                 ha    s                       ind by num-                uni

Figure 7: Compilation-time overhead of vanilla HWAsan, SafeFFI (including cast and stack checks), and SafeFFI with added
heap checks compared to baseline compilation-time without sanitizer. Note that the scale is logarithmic to accommodate large
overheads of RustSan.


Those two approaches conceptually avoid this risk by retain-                                   to safe Rust code, SafeFFI prevents memory vulnerabilities in
ing all sanitizer checks at pointer dereference locations if the                               the first place and therefore enables better debugging, without
pointer might alias with a raw pointer.                                                        requiring source or OS changes.
   However, interestingly, RustSan and ERASan show worse
ability to retain the sanitizer’s detection capabilities on our                                Static Analyzers for Memory Safety in Rust. Tools like
tests with real-world vulnerabilities (Table 1). ERASan in                                     MIRChecker [21], Rudra [2], Yuga [32], and SafeDrop [6]
particular suffers from implementation bugs that cause false                                   use static analysis to detect memory bugs in Rust, while
negatives. Both implement a blacklist approach for identi-                                     FFIChecker [20] and CRust [13] focus on FFI safety. These
fying raw pointers, potentially leading to false negatives if                                  approaches suffer from false positives and excessive compile-
the type annotation is incomplete. SafeFFI uses a whitelist                                    time overhead, whereas SafeFFI is a dynamic analysis based
approach instead, validating that every pointer has a type and                                 on sanitizers resulting in high precision at the cost of run-time
overapproximating raw pointers where the implementation                                        overheads which SafeFFI significantly reduces for Rust code.
is incomplete—which should be accounted for because the
Rust compiler’s internals for lowering MIR to LLVM IR are
very complex. Overall, our implementation is more tightly                                      8      Conclusion
integrated with the Rust compilation toolchain without the
                                                                                               We presented SafeFFI, a novel approach to hoist sanitizer
need to link and analyze the program externally. This should
                                                                                               checks in Rust programs and MLAs to reduce the run-time
increase the chances of adoption.
                                                                                               overhead of sanitizers. Compared to existing approaches,
                                                                                               SafeFFI only uses funcion-local reasoning to hoist checks
General Sanitizer Optimizations. Prior work on C/C++                                           instead of depending on whole-program static points-to anal-
includes ASAP [43] which removes checks on hot paths, trad-                                    ysis which can be expensive and error-prone. Our approach
ing security for performance. Moll et al. [29], hoist bounds                                   for hoisting checks to locations of casts from raw pointers
checks in loops. ASan-- [46] uses lightweight static analysis                                  to safe pointers shows improved performance compared to
and SanRazor [45] a combination of static and dynamic anal-                                    existing methods, especially for Rust programs that frequently
ysis to reduce redundant checks. These are complementary                                       interact with unsafe code or FFI code. We showed practicality
to SafeFFI and could be applied to raw pointers in Rust or                                     and effectiveness in reducing the total number of sanitizer
C/C++ parts of MLAs.                                                                           checks for popular Rust libraries by 58% − 98%, resulting in
                                                                                               a reduction of the run-time overhead of HWASan from 3.22×
Runtime Isolation for Rust. Several proposed approaches                                        to 2.51× on average. Our experiments with existing real-
isolate safe Rust from unsafe code, e.g., Sandcrust [18], Fi-                                  world vulnerabilities show that SafeFFI not only maintains
delius Charm [1], XRust [23], relying on developer annota-                                     the sanitizer’s detection capabilities but also improves debug-
tions or hardware/OS support for process isolation. TRust [3],                                 gability by failing closer to the root cause of memory safety
PRKUSafe [15] and Gülmez et al. [9] instead use Intel’s Mem-                                   violations in the interaction between safe rust and unsafe Rust
ory Protection Keys (MPK) to separate safe and unsafe objects                                  or foreign code. We showed that SafeFFI can be implemented
in different memory regions. Galeed [35] and Omniglot [36]                                     in a very modular way such that in the future it can be adapted
explicitly address cross-language attacks [24] by isolating                                    for different memory sanitizers that choose different tradeoffs
Rust from C code, relying on hardware features for in-process                                  like SoftboundCETS [30, 31] for more security.
isolation. As opposed to those isolation approaches that only
inhibit the spread of memory vulnerabilities from unsafe code


                                                                                         13
Ethical Considerations                                                       33rd USENIX Security Symposium (USENIX Security
                                                                             24), pages 3729–3746, 2024.
SafeFFI is a purely defensive tool to improve the efficiency of
memory sanitizers in Rust programs. Enabling more software               [6] Mohan Cui, Chengjun Chen, Hui Xu, and Yangfan Zhou.
to run with memory sanitization should have a net benefit in                 Safedrop: Detecting memory deallocation bugs of rust
reducing vulnerabilities. A potential risk is that benign exe-               programs via static data-flow analysis. ACM Trans-
cutions could be terminated although the observed memory                     actions on Software Engineering and Methodology,
error would not have had negative effects, but we believe that               32(4):1–21, 2023.
this risk is outweighed by the benefits.
                                                                         [7] The Rust Project Developers. Primitive Type Ref-
   All vulnerabilities used for evaluation in this work (see
                                                                             erence - Safety. Section of "The Rust Standard Li-
Table 1) were already publicly known, and we did not try to
                                                                             brary" documentation. https://doc.rust-lang.org/
discover new vulnerabilities.
                                                                             std/primitive.reference.html#safety.

Open Science                                                             [8] The Rust Project Developers. Type Coercions. Section
                                                                             of "The Rust Reference". https://doc.rust-lang.
We comply with the open science policy by releasing the                      org/reference/type-coercions.html.
SafeFFI prototype as open source and for artifact evaluation.            [9] Merve Gülmez, Thomas Nyman, Christoph Baumann,
This includes our modifications to rustc and LLVM, test sets,                and Jan Tobias Mühlberg. Friend or foe inside? ex-
benchmarks and the corresponding scripts to build and exe-                   ploring in-process isolation to maintain memory safety
cute them with SafeFFI. An anonymized version for review                     for unsafe rust, 2023. https://arxiv.org/abs/2306.
can be found on Zenodo:                                                      08127.
https://tinyurl.com/safeffi-usenix
   The final version will be published on Github upon accep-            [10] Sarah     Harris, Simon         Cooksey, Michael
tance.                                                                       Vollmer, and Mark Batty.         Rust for Morello:
                                                                             Always-On Memory Safety, Even in Un-
                                                                             safe Code (Experience Paper).           In DROPS-
References                                                                   IDN/v2/Document/10.4230/LIPIcs.ECOOP.2023.39.
                                                                             Schloss-Dagstuhl - Leibniz Zentrum für Informatik.
 [1] Hussain MJ Almohri and David Evans. Fidelius Charm:
     Isolating Unsafe Rust Code. In Proceedings of the                  [11] Ben Hawkes. 0day “in the wild”, 2019. https://
     Eighth ACM Conference on Data and Application Secu-                     googleprojectzero.blogspot.com/p/0day.html.
     rity and Privacy, pages 248–255. ACM.
                                                                        [12] Konrad Hohentanner, Philipp Zieris, and Julian Horsch.
 [2] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon                          CryptSan: Leveraging ARM Pointer Authentication for
     Lim, and Taesoo Kim. Rudra: Finding Memory Safety                       memory safety in C/C++. In SAC. ACM, 2023.
     Bugs in Rust at the Ecosystem Scale. In Proceedings
     of the ACM SIGOPS 28th Symposium on Operating                      [13] Shuang Hu, Baojian Hua, Lei Xia, and Yang Wang.
     Systems Principles, SOSP ’21, pages 84–99. Association                  CRUST: towards a unified cross-language program anal-
     for Computing Machinery.                                                ysis framework for rust. In 22nd IEEE International
                                                                             Conference on Software Quality, Reliability and Secu-
 [3] Inyoung Bang, Martin Kayondo, HyunGon Moon, and                         rity, QRS 2022, Guangzhou, China, December 5-9, 2022,
     Yunheung Paek. {TRust}: A compilation framework for                     pages 970–981. IEEE, 2022.
     in-process isolation to protect safe rust against untrusted
     code. In 32nd USENIX Security Symposium (USENIX                    [14] Intel Corp.   Pointer checker, 2021.  https:
     Security 23), pages 6947–6964, 2023.                                    //www.intel.com/content/www/us/en/docs/
                                                                             cpp-compiler/developer-guide-reference/
 [4] Xingman Chen, Yinghao Shi, Zheyu Jiang, Yuan Li,                        2021-10/pointer-checker.html.
     Ruoyu Wang, Haixin Duan, Haoyu Wang, and Chao
     Zhang. MTSan: A feasible and practical memory sani-                [15] Paul Kirth, Mitchel Dickerson, Stephen Crane, Per
     tizer for fuzzing COTS binaries. In USENIX Security.                    Larsen, Adrian Dabrowski, David Gens, Yeoul Na, Stijn
     USENIX Association, 2023.                                               Volckaert, and Michael Franz. PKRU-safe: Automati-
                                                                             cally locking down the heap between safe and unsafe
 [5] Kyuwon Cho, Jongyoon Kim, Kha Dinh Duy, Ha-                             languages. In Proceedings of the Seventeenth Euro-
     jeong Lim, and Hojoon Lee. {RustSan}: Retrofitting                      pean Conference on Computer Systems, pages 132–148.
     {AddressSanitizer} for efficient sanitization of rust. In               ACM.


                                                                   14
[16] Steve Klabnik, Carol Nichols, and Chris Krycho. Un-              [27] MITRE Corp. 2024 CWE top 10 kev weaknesses,
     derstanding Ownership. Chapter 4 of "The Rust Pro-                    2024.   https://cwe.mitre.org/top25/archive/
     gramming Language". https://doc.rust-lang.org/                        2024/2024_kev_list.html.
     book/ch04-00-understanding-ownership.html.
                                                                      [28] MITRE Corp. 2024 CWE top 25 most dangerous soft-
[17] Taddeus Kroes, Koen Koning, Erik van der Kouwe, Her-                  ware weaknesses, 2024. https://cwe.mitre.org/
     bert Bos, and Cristiano Giuffrida. Delta pointers: Buffer             top25/archive/2024/2024_cwe_top25.html.
     overflow checks without the checks. In EuroSys. ACM,
                                                                      [29] Simon Moll, Henrique Nazaré, Gustavo Vieira Machado,
     2018.
                                                                           and Raphael Ernani Rodrigues. Bounds Check Hoist-
[18] Benjamin Lamowski, Carsten Weinhold, Adam Lack-                       ing for AddressSanitizer. In Fernando Magno Quin-
     orzynski, and Hermann Härtig. Sandcrust: Automatic                    tão Pereira, editor, Programming Languages, pages 47–
     sandboxing of unsafe components in rust. In Proceed-                  61. Springer International Publishing.
     ings of the 9th Workshop on Programming Languages
                                                                      [30] Santosh Nagarakatte, Jianzhou Zhao, Milo M. K. Martin,
     and Operating Systems, pages 51–57. ACM.
                                                                           and Steve Zdancewic. Softbound: Highly compatible
[19] Yuan Li, Wende Tan, Zhizheng Lv, Songtao Yang, Math-                  and complete spatial memory safety for C. In PLDI.
     ias Payer, Ying Liu, and Chao Zhang. PACMem: En-                      ACM, 2009.
     forcing spatial and temporal memory safety via ARM               [31] Santosh Nagarakatte, Jianzhou Zhao, Milo M.K. Mar-
     Pointer Authentication. In CCS. ACM, 2022.                            tin, and Steve Zdancewic. CETS: Compiler enforced
[20] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John                     temporal safety for C. In ISMM. ACM, 2010.
     C. S. Lui. Detecting Cross-language Memory Manage-               [32] Vikram Nitin, Anne Mulhern, Sanjay Arora, and
     ment Issues in Rust. In Vijayalakshmi Atluri, Roberto                 Baishakhi Ray. Yuga: Automatically detecting lifetime
     Di Pietro, Christian D. Jensen, and Weizhi Meng, edi-                 annotation bugs in the rust language. IEEE Trans. Softw.
     tors, Computer Security – ESORICS 2022, Lecture Notes                 Eng., 50(10):2602–2613, October 2024.
     in Computer Science, pages 680–700. Springer Nature
     Switzerland.                                                     [33] Benjamin Orthen, Oliver Braunsdorf, Philipp Zieris, and
                                                                           Julian Horsch. SoftBound+CETS revisited: More than
[21] Zhuohua Li, Jincheng Wang, Mingshen Sun, and                          a decade later. In EuroSec. ACM, 2024.
     John CS Lui. Mirchecker: detecting bugs in rust pro-
     grams via static analysis. In Proceedings of the 2021            [34] Michalis Papaevripides and Elias Athanasopoulos. Ex-
     ACM SIGSAC conference on computer and communica-                      ploiting mixed binaries. ACM Transactions on Privacy
     tions security, pages 2183–2196, 2021.                                and Security (TOPS), 24(2):1–29, 2021.

[22] Zhenpeng Lin, Zheng Yu, Ziyi Guo, Simone Campanoni,              [35] Elijah Rivera, Samuel Mergendahl, Howard Shrobe,
     Peter Dinda, and Xinyu Xing. CAMP: Compiler and                       Hamed Okhravi, and Nathan Burow. Keeping Safe Rust
     allocator-based heap memory protection. In USENIX                     Safe with Galeed. In Annual Computer Security Applica-
     Security. USENIX Association, 2024.                                   tions Conference, ACSAC, pages 824–836. Association
                                                                           for Computing Machinery.
[23] Peiming Liu, Gang Zhao, and Jeff Huang. Securing
     unsafe rust programs with XRust. In Proceedings of the           [36] Leon Schuermann, Jack Toubes, Tyler Potyondy, Pat
     ACM/IEEE 42nd International Conference on Software                    Pannuto, Mae Milano, and Amit Levy. Building bridges:
     Engineering, pages 234–245. ACM.                                      Safe interactions with foreign languages through om-
                                                                           niglot. In Lidong Zhou and Yuanyuan Zhou, editors,
[24] Samuel Mergendahl, Nathan Burow, and Hamed                            19th USENIX Symposium on Operating Systems Design
     Okhravi. Cross-Language Attacks. In Proceedings 2022                  and Implementation, OSDI 2025, Boston, MA, USA, July
     Network and Distributed System Security Symposium.                    7-9, 2025, pages 595–613. USENIX Association, 2025.
     Internet Society.
                                                                      [37] Konstantin Serebryany, Derek Bruening, Alexander
[25] Matt Miller. Trends, challenges, and strategic shifts                 Potapenko, and Dmitry Vyukov. AddressSanitizer: A
     in the software vulnerability mitigation landscape. In                fast address sanity checker. In USENIX ATC. USENIX
     BlueHat IL. Microsoft Security Response Center, 2019.                 Association, 2012.
[26] Jiun Min, Dongyeon Yu, Seongyun Jeong, Dokyung                   [38] Kostya Serebryany, Evgenii Stepanov, Aleksey Shlyap-
     Song, and Yuseok Jeon. ERASan: Efficient Rust Ad-                     nikov, Vlad Tsyrklevich, and Dmitry Vyukov. Memory
     dress Sanitizer. In 2024 IEEE Symposium on Security                   tagging and how it improves C/C++ memory safety.
     and Privacy (SP), pages 4053–4068.                                    arxiv:1802.09517, Google LLC, 2018.


                                                                 15
[39] Melih Sirlanci, Carter Yagemann, and Zhiqiang Lin.
     C2RUST-BENCH: A minimized, representative
     dataset for c-to-rust transpilation evaluation. CoRR,
     abs/2504.15144, 2025.
[40] Dokyung Song, Julian Lettner, Prabhu Rajasekaran,
     Yeoul Na, Stijn Volckaert, Per Larsen, and Michael
     Franz. SoK: Sanitizing for security. In S&P. IEEE,
     2019.
[41] The Chromium Developers. Memory safety. https:
     //www.chromium.org/Home/chromium-security/
     memory-safety/.
[42] Emanuel Vintila, Philipp Zieris, and Julian Horsch. Eval-
     uating the Effectiveness of Memory Safety Sanitizers.
     In 2025 IEEE Symposium on Security and Privacy (SP),
     pages 88–88, Los Alamitos, CA, USA, May 2025. IEEE
     Computer Society.
[43] Jonas Wagner, Volodymyr Kuznetsov, George Candea,
     and Johannes Kinder. High System-Code Security with
     Low Overhead. In 2015 IEEE Symposium on Security
     and Privacy, pages 866–879.

[44] Robert N.M. Watson, Jonathan Woodruff, Peter G. Neu-
     mann, Simon W. Moore, Jonathan Anderson, David
     Chisnall, Nirav Dave, Brooks Davis, Khilan Gudka, Ben
     Laurie, Steven J. Murdoch, Robert Norton, Michael Roe,
     Stacey Son, and Munraj Vadera. CHERI: A Hybrid
     Capability-System Architecture for Scalable Software
     Compartmentalization. In 2015 IEEE Symposium on
     Security and Privacy, pages 20–37.
[45] Jiang Zhang, Shuai Wang, Manuel Rigger, Pinjia He,
     and Zhendong Su. {SANRAZOR}: Reducing redun-
     dant sanitizer checks in {C/C++} programs. In 15th
     USENIX Symposium on Operating Systems Design and
     Implementation (OSDI 21), pages 479–494, 2021.
[46] Yuchen Zhang, Chengbin Pang, Georgios Portokalidis,
     Nikos Triandopoulos, and Jun Xu. Debloating address
     sanitizer. In 31st USENIX Security Symposium (USENIX
     Security 22), pages 4345–4363, 2022.

[47] Tianyang Zhou, Haowen Lin, Somesh Jha, Mihai
     Christodorescu, Kirill Levchenko, and Varun Chan-
     drasekaran. Llm-driven multi-step translation from C to
     rust using static analysis. CoRR, abs/2503.12511, 2025.




                                                                 16
A     Full Evaluation Results

A.1     Check Elision

                                                                                           SafeFFI                                                      RustSan
    Benchmark              # Sanitizer     Elided Checks        Added Cast      Added Stack        Savings w/o     Added Heap         Savings w/         Savings
                              Checks                               Checks           Checks        Heap Checks          Checks       Heap Checks
    Stdlib                    182 923            94.68%                446            5,085           91.66%            18,523             81.53%             72.40%
    bat                       492 479            93.41%              1,150           12,561           90.62%            69,765             76.46%             69.02%
    fd-find                   294 081            92.73%                690            8,536           89.59%            37,919             76.70%             66.69%
    ripgrep                   389 881            92.44%                897           11,761           89.20%            60,142             73.77%             67.80%
    tokio                      88 971            87.73%                597            4,400           82.11%            12,369             68.21%             59.92%
    firecracker                68 271            90.47%                134            3,734           84.81%            13,497             65.04%             54.30%
    hyper                     150 280            90.31%                543            6,495           85.63%            18,419             73.37%             67.44%
    wasmtime                1 084 685            92.62%              1,969           40,667           88.69%           153,911             74.50%             68.48%
    uuid                        1 207            96.44%                  2               86           89.15%               108             80.20%             74.12%
    chrono                     18 286            97.27%                  1              108           96.67%             1,741             87.15%             89.58%
    adler                         193            93.78%                  0                7           90.16%                17             81.35%             42.86%
    unicode-xid                    93            93.55%                  0                1           92.47%                 2             90.32%             44.28%
    base64                        649            83.67%                  0                9           82.28%                65             72.27%             82.21%
    image                     241 051            94.83%                433            4,397           92.82%            35,548             78.08%             74.34%
    regex                     214 812            92.28%                359            5,569           89.52%            27,261             76.83%             63.84%
    byteorder                       4           100.00%                  0                0          100.00%                 0            100.00%             41.95%
    bytes                       2 473            91.95%                 19               29           90.01%               218             81.20%             54.46%
    json                       10 119            95.67%                  6              105           94.57%             2,088             73.94%             69.12%
    syn-1.0.48                 49 678            93.38%                144            1,164           90.75%             7,125             76.40%             76.12%
    rand                       10 106            92.72%                  6              686           85.87%             1,165             74.34%             58.03%
    crossbeam                   3 179            89.34%                 17              103           85.56%               490             70.15%             58.67%
    memchr                    215 707            93.60%                738            6,567           90.21%            33,424             74.71%             67.17%
    hashbrown                     150            88.67%                  0                7           84.00%                19             71.33%             54.39%
    smallvec                       51            96.08%                  0                1           94.12%                 0             94.12%             20.00%
    ryu                           837            90.80%                  0               15           89.01%                 0             89.01%             34.52%
    semver                      3 251            95.54%                  2               31           94.52%               343             83.97%             76.09%
    strsim                      4 805            92.20%                  7              103           89.91%               608             77.25%             63.88%
    indexmap                      243            78.60%                  0                4           76.95%                46             58.02%             24.10%
    num-integer                 2 926            98.70%                  0                9           98.39%                64             96.21%             93.96%
    url                        25 365            95.23%                 12              264           94.14%             3,414             80.68%             73.62%




A.2     Compile-time Overhead

                                         Baseline                  HWASan            SafeFFI w/o heap checks     SafeFFI w/ heap checks             RustSan
      Benchmark               Time (s)      Memory (MB)        Time OH   Mem OH      Time OH         Mem OH      Time OH         Mem OH      Time OH     Mem OH
      bat                        45.32                584.27     1.90×       1.31×        3.27×         1.25×      3.86×          1.27×       17.43×      23.56×
      fd-find                    44.78                612.48     1.75×       1.35×        3.02×         1.33×      3.51×          1.30×       11.22×      17.10×
      ripgrep                    40.52                584.31     1.91×       1.34×        3.35×         1.36×      4.21×          1.36×       15.69×      21.03×
      tokio                      29.21                597.66     1.57×       1.29×        1.70×         1.26×      2.37×          1.12×        6.80×       7.84×
      firecracker-0.23.0         27.68                588.69     1.71×       1.31×        1.80×         1.33×      2.49×          1.28×        6.70×       8.48×
      hyper                      38.07                612.47     1.63×       1.24×        1.78×         1.18×      2.44×          1.07×        7.02×       9.50×
      wasmtime                  104.99              1,012.59     1.41×       1.75×        1.63×         1.69×      3.19×          1.04×       43.03×      59.03×
      syn-1.0.48                 25.79                616.94     1.63×       1.23×        1.76×         1.20×      2.34×          1.08×        6.61×       6.78×
      rand                       22.97                618.52     1.94×       1.24×        2.07×         1.21×      2.62×          1.07×        5.73×       5.23×
      chrono                     22.71                589.92     1.63×       1.32×        1.73×         1.28×      2.27×          1.11×        5.65×       5.36×
      crossbeam-0.8.0            20.75                615.67     1.65×       1.23×        1.79×         1.23×      2.32×          1.07×        5.95×       4.92×
      base64                     20.40                583.89     1.64×       1.35×        1.77×         1.24×      2.36×          1.14×        5.86×       4.84×
      regex-1.4.2                33.46                611.59     1.95×       1.73×        3.61×         1.71×      4.12×          1.70×       11.08×      13.14×
      memchr-2.3.4               33.31                613.22     1.75×       1.23×        1.89×         1.18×      2.64×          1.07×       10.65×      12.76×
      hashbrown-0.9.1            20.50                617.00     1.64×       1.23×        1.74×         1.22×      2.32×          1.07×        5.78×       4.87×
      smallvec-1.5.0             20.39                616.17     1.63×       1.23×        1.76×         1.20×      2.31×          1.07×        5.76×       4.80×
      ryu                        20.44                596.11     1.65×       1.29×        1.77×         1.21×      2.31×          1.12×        5.93×       4.88×
      semver                     20.55                606.83     1.67×       1.23×        1.79×         1.21×      2.32×          1.10×        5.79×       4.92×
      strsim                     20.56                610.05     1.67×       1.28×        1.80×         1.22×      2.35×          1.07×        5.91×       4.95×
      bytes                      20.66                616.00     1.64×       1.21×        1.78×         1.21×      2.33×          1.07×        5.82×       4.95×
      indexmap-1.6.0             20.76                616.83     1.62×       1.23×        1.73×         1.22×      2.29×          1.07×        5.75×       4.80×
      byteorder                  20.40                616.66     1.63×       1.26×        1.77×         1.18×      2.34×          1.06×        5.86×       4.83×
      num-integer                21.39                616.98     1.63×       1.23×        1.74×         1.17×      2.30×          1.06×        5.61×       4.88×
      url-2.2.0                  23.91                591.22     1.72×       1.24×        1.84×         1.25×      2.36×          1.12×        6.22×       5.61×
      uuid                       20.64                591.81     1.66×       1.25×        1.75×         1.27×      2.31×          1.11×        5.88×       4.85×
      unicode-xid-0.2.1          20.24                611.31     1.63×       1.22×        1.79×         1.27×      2.33×          1.08×        5.87×       4.81×




                                                                                     17
A.3    Run-time Overhead

                     Benchmark     Baseline (ns)   HWASan   SafeFFI w/o heap checks   SafeFFI w/ heap checks
                     uuid               881.02      3.37×                    1.90×                    2.01×
                     chrono           1,726.16      3.42×                    1.93×                    2.25×
                     adler              451.26      3.00×                    2.01×                    2.17×
                     unicode          5.82 · 105    3.73×                    1.79×                    2.18×
                     base64           6.01 · 105    1.41×                    1.87×                    1.83×
                     regex            6,430.57      2.76×                    2.51×                    3.31×
                     byteorder        1.33 · 106    4.40×                    2.79×                    2.77×
                     bytes            1,941.19      3.06×                    2.06×                    2.14×
                     json            14,969.95      3.49×                    2.44×                    3.47×
                     rand            11,795.64      2.56×                    1.49×                    1.67×
                     crossbeam          267.60      5.34×                    2.89×                    3.02×
                     itoa               165.65      2.77×                    2.11×                    2.23×
                     hashbrown        1.42 · 105    2.92×                    2.07×                    3.12×
                     smallvec           606.39      3.63×                    2.51×                    3.00×
                     ryu                264.85      2.64×                    1.94×                    2.23×
                     semver           1,225.26      2.79×                    2.06×                    2.35×
                     strsim          70,290.11      2.79×                    1.76×                    2.02×
                     indexmap         1.59 · 106    3.05×                    2.10×                    2.70×
                     num-integer     15,029.28      4.34×                    2.31×                    3.46×
                     url              9,972.00      3.00×                    1.81×                    2.15×




B     ERASan Issue




                                                             18
