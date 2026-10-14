                                         From C to Idiomatic Rust: A Ship-of-Theseus Agentic Translation
                                                                                                                 Vasily A. Sartakov)
                                                                                         Huawei Technologies Research & Development (UK) Ltd
                                                                                                     Cambridge, United Kingdom
                                                                                                    vasily.sartakov@huawei.com

                                         Abstract                                                                                programming because of its standardisation, portability, and effi-
                                         C underpins operating systems, embedded platforms, and network                          cient implementation across a wide range of hardware platforms.
                                         infrastructure as its abstractions map directly to machine behaviour.                       C’s enduring popularity largely stems from its language abstrac-
                                         Its explicit memory model, predictable data representations, and                        tions, which closely reflect the underlying machine architecture.
                                         minimal runtime allow compilers to generate fast, deterministic                         The language employs an explicit memory model, provides straight-
arXiv:2607.28835v2 [cs.SE] 29 Aug 2026




                                         code. These properties also leave correctness and memory safety                         forward procedural control-flow constructs, and defines data repre-
                                         entirely to the programmer, making undefined behaviour, pointer                         sentations that are largely predictable within the constraints of the
                                         misuse, and lifetime errors persistent sources of defects and secu-                     target platform Application Binary Interface (ABI). Consequently,
                                         rity vulnerabilities in long-lived C codebases. Rust eliminates most                    source-level constructs can be related directly to machine-level op-
                                         failure modes through a static ownership and borrowing model                            erations, enabling efficient implementation and optimisation when
                                         that enforces memory safety and aliasing constraints at compile                         execution time, memory consumption, or hardware interaction are
                                         time. However, mature C systems cannot be translated directly:                          important. Together with a compact language definition, a stable
                                         implicit layout assumptions, aliasing patterns, and undefined be-                       standardisation process, and mature compilers such as GCC and
                                         haviour must be reconstructed before safe Rust can be produced.                         Clang/LLVM, these characteristics make C particularly suitable for
                                            This paper presents a migration methodology that first gener-                        systems software and other performance-critical applications that
                                         ates a semantics-preserving, non-idiomatic Rust baseline and then                       require predictable execution costs [5, 9].
                                         incrementally rewrites it into idiomatic Rust using agentic AI, val-                        Despite its strengths, C provides relatively few language-level
                                         idating each step through compilation and behavioural testing. Ap-                      guarantees for memory safety or program correctness. The lan-
                                         plied to iodine, a real-world DNS tunnel, the approach demonstrates                     guage permits unrestricted pointer arithmetic and direct manip-
                                         that reliable C-to-Rust migration is a structured transformation                        ulation of memory, placing responsibility for maintaining object
                                         workflow rather than a single translation step.                                         lifetimes, array bounds, and pointer validity entirely on the pro-
                                                                                                                                 grammer. As a result, many classes of programming errors are not
                                         CCS Concepts                                                                            detected either by the compiler or at runtime.
                                                                                                                                     Common sources of software defects include use-after-free er-
                                         • Software and its engineering → Software evolution; Software
                                                                                                                                 rors, out-of-bounds memory accesses, double-free errors, integer
                                         verification and validation; Automatic programming.
                                                                                                                                 overflow, null-pointer dereferences, and the use of uninitialised
                                                                                                                                 memory. Such errors usually result in Undefined Behaviour (UB),
                                         Keywords                                                                                meaning that the C standard imposes no requirements on the out-
                                         C-to-Rust migration, Rust, agentic translation                                          come of program execution. UB enables aggressive compiler opti-
                                                                                                                                 misation but also complicates debugging, testing, and formal rea-
                                         ACM Reference Format:
                                         Vasily A. Sartakov. 2026. From C to Idiomatic Rust: A Ship-of-Theseus Agen-             soning about program correctness. In security-critical software, vi-
                                         tic Translation. In Proceedings of the 2nd International Workshop on AI for             olations of memory safety remain among the most common causes
                                         Software Modernization (AISM ’26), October 12–16, 2026, Munich, Germany.                of exploitable vulnerabilities, including arbitrary code execution,
                                         ACM, New York, NY, USA, 8 pages. https://doi.org/10.1145/3843775.3844544                privilege escalation, and information disclosure.
                                                                                                                                     These limitations have motivated extensive research on static
                                                                                                                                 analysis, dynamic analysis, formal verification, and runtime instru-
                                         1    Introduction
                                                                                                                                 mentation techniques for C programs. Widely adopted tools, in-
                                         C remains one of the most influential and widely deployed pro-                          cluding AddressSanitizer, UndefinedBehaviorSanitizer, Valgrind,
                                         gramming languages. It provides the implementation foundation                           and numerous static analysers, aim to detect memory errors and
                                         for operating systems, embedded systems, networking infrastruc-                         UB during development. More recently, memory-safe programming
                                         ture, databases, language runtimes, and many other long-lived soft-                     languages have been proposed to reduce the prevalence of these
                                         ware systems. Since its development at Bell Laboratories in the                         vulnerabilities whilst preserving the performance characteristics
                                         early 1970s, C has remained a fundamental language for systems                          required for systems programming.
                                                                                                                                     Rust has emerged as a modern systems programming language
                                                                                                                                 designed to address many of the memory-safety limitations asso-
                                                                                                                                 ciated with C whilst retaining comparable performance character-
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.
                                         AISM ’26, Munich, Germany                                                               istics. Unlike C, Rust introduces a strict ownership and borrow-
                                         © 2026 Copyright held by the owner/author(s).                                           ing model that enables compile-time verification of memory ac-
                                         ACM ISBN 979-8-4007-2987-4/2026/10                                                      cess patterns, object lifetimes, and data sharing without relying
                                         https://doi.org/10.1145/3843775.3844544
AISM ’26, October 12–16, 2026, Munich, Germany                                                                                Vasily A. Sartakov


on a garbage collector. This approach eliminates many common            and verification problem than as a single code-generation task, en-
classes of vulnerabilities, including use-after-free errors, double-    abling gradual replacement of legacy C constructs with idiomatic
free errors, and data races, whilst preserving low-level control over   Rust whilst preserving system correctness.
memory layout and execution behaviour.
   Rust’s main advantage is the ability to provide stronger safety      2 Background
guarantees before program execution. The compiler performs ex-          C and Rust follow fundamentally different programming paradigms.
tensive static analysis and rejects programs that violate ownership     C relies on manual memory management and unrestricted low-
or borrowing rules, shifting error detection from runtime to com-       level access, whilst Rust enforces memory safety and concurrency
pilation. This design improves reliability for security-critical and    guarantees through its ownership model. This division defines the
performance-sensitive software, particularly in areas traditionally     technical and conceptual challenges involved in translating soft-
dominated by C, such as operating systems, embedded platforms,          ware from one language to another. Table 1 summarises the key
and network infrastructure.                                             ones.
   Despite advantages, Rust also introduces additional complex-
ity. The ownership and borrowing model requires programmers             Memory safety. C permits arbitrary pointer arithmetic: a func-
to adopt new concepts and can increase initial development effort       tion receiving char *buf, int len can conceptually read or write
compared with conventional C programming. However, the safety           buf[len+1] or buf[-1]. Rust’s slice type &[u8] combines a pointer
guarantees provided by Rust create a strong motivation for migrat-      with its length, and all accesses are bounds-checked at runtime.
ing parts of existing C infrastructure. Replacing memory-unsafe         Out-of-bounds access in C results in UB and may not trigger a
components with safe implementations could significantly reduce         memory protection fault, whereas in Rust it is guaranteed in safe
vulnerabilities whilst maintaining the performance characteristics.     code. Consequently, a Rust program requires well-defined bounds,
Such a transition could be particularly valuable in security-critical   which are not always recoverable from C.
domains where long-lived C codebases continue to represent a sig-       Type safety. The void* type in C performs type erasure in the
nificant source of memory-related defects.                              sense that C retains no type information at runtime: a function
   Nevertheless, migration from C to Rust is not a simple trans-        taking void *data operates on untyped memory, and the actual
lation problem. A direct conversion process cannot preserve the         type must be coordinated by convention between caller and callee.
behaviour of a mature C codebase whilst simultaneously guaran-          Rust has no analogue to void. Its generics use parametric polymor-
teeing Rust safety properties. Existing C programs often depend         phism, preserving type information for the compiler and enabling
on implicit assumptions about memory layout, pointer manipula-          static checking (fn<T>(x: &T)). Translating uses of void therefore
tion, object lifetimes, and aliasing patterns that are not explicitly   requires reconstructing the intended types, which is a semantic task
represented in the source code. In addition, undefined behaviour,       rather than a syntactic one.
manual resource management, compiler-specific extensions, and           Initialisation. C considers uninitialised memory a valid program
hardware-dependent optimisations are common in low-level C soft-        state. Reading an uninitialised variable is UB, but the compiler
ware and may require substantial redesign when expressed in Rust.       does not prevent it. Rust, in turn, requires every variable to be ini-
The difference between the two programming models means that            tialised before use, and the compiler rejects code paths that might
successful migration requires analysis and transformation of pro-       read uninitialised memory. For translation, it is a data-flow anal-
gram structure rather than a purely syntactic conversion.               ysis problem: it must identify which C variables are definitely ini-
   Recent advances in large language models have demonstrated           tialised before the first use.
strong capabilities for code generation and refactoring, making
                                                                        Resource management. Rust offers an ownership system that
them a promising technology for C-to-Rust migration. However,
                                                                        encodes allocation lifetime in the type: every value has exactly
most existing approaches formulate migration as direct translation
                                                                        one owner, and the compiler inserts deallocation at the end of the
from C to idiomatic Rust, placing both semantic recovery and lan-
                                                                        owner’s scope. C uses manual allocation and deallocation using
guage transformation into a single step. For realistic systems soft-
                                                                        malloc/free — a source of UB caused by use-after-free or double
ware, this objective remains difficult to achieve reliably.
                                                                        free. Translating manual memory to ownership requires inferring
   This paper adopts a different perspective. Rather than translat-
                                                                        the lifetime of each allocation and goes beyond tracing the life-
ing C directly into idiomatic Rust, we treat migration as the trans-
                                                                        cycle of allocated memory: it must reconstruct how resources flow
formation of a semantics-preserving but non-idiomatic Rust pro-
                                                                        through pointers, aliases, and calling conventions, and map these
gram into an idiomatic one. We define explicit idiomaticity crite-
                                                                        behaviours onto Rust’s stricter ownership and borrowing rules.
ria and present a methodology that incrementally replaces non-
idiomatic components using agentic AI whilst preserving a con-          Nullability. Every C pointer can be NULL. A function accepting
tinuously executable hybrid codebase. Each transformation is vali-      char *s must check for NULL; otherwise, dereferencing it results
dated through compilation and behavioural testing before becom-         in UB. Rust separates nullable from non-nullable references at the
ing the basis for subsequent migration.                                 type level: &T is guaranteed non-null; Option<&T> explicitly repre-
   The proposed methodology is implemented as an integrated tool-       sents a value that may be absent. Translating C pointers requires
chain and evaluated on iodine, a production-quality DNS tunnel          determining whether NULL is a valid input, which is another se-
comprising approximately 12.5 kSLOC of C code. The study demon-         mantic challenge.
strates that large-scale migration is better approached as a tooling    String model. C represents strings as char* terminated by a NUL
                                                                        byte (\0). String length is computed at runtime via str(n)len,
From C to Idiomatic Rust: A Ship-of-Theseus Agentic Translation                                      AISM ’26, October 12–16, 2026, Munich, Germany


                               Table 1: Key differences between C and Rust relevant to automated translation.

Dimension                         C                                                 Rust
Memory safety                     No bounds checking, UB on overflow                Bounds-checked slices, overflows panic
Type safety                       void* erases types, implicit casts                No void*, no implicit conversions
Initialisation                    Uninitialised reads are UB                        All values initialised before first use
Resource mgmt                     Manual malloc/free, leak/double-free              Ownership RAII, compiler-enforced drop
Nullability                       Every pointer may be NULL                         Option<T>, &T never null
String model                      NUL-terminated char*, strlen scans                &str/&[u8], length in type
Global state                      static mutable, no synchronisation                static mut needs unsafe, Mutex


which scans until it finds the terminator or hits the limit. Rust        but bounds are not introduced as this information is not available
distinguishes UTF-8 strings (&str) from arbitrary byte sequences         to the transpiler. As a result, functions become unsafe by default.
(&[u8]), with length encoded in the type. A translator must decide,      Ultimately, the transpiler just generates C code in Rust syntax, but
per buffer, whether it holds a C string (NUL-terminated, possibly        it is a crucial step for the translation.
UTF-8) or a byte array (length-known, arbitrary content). Conse-
quently, translating C strings requires inferring the intended string
semantics, not merely the memory layout.                                 2.2    Translation Challenges in Action
Global state. C static variables are mutable by default, and the         Let us consider a simplified version of a code ported in this project.
const qualifier is optional and frequently omitted. Unsynchronised       It represents typical programming approaches for system software:
access to a shared state across threads is a data race, and C offers     a buffer manipulation function that decodes a DNS name from wire
no language-level support to enforce correct synchronisation. Id-        format. Figure 1 shows the same function in three forms: the orig-
iomatic Rust models shared state explicitly, using Atomic* types         inal C, the c2rust version, and the final idiomatic Rust after the
for scalar concurrency primitives and Mutex<T> for compound data.        porting. They illustrate four patterns that resist mechanical trans-
A translator must therefore classify each global according to its ef-    lation:
fective access pattern: (1) read-only (eligible for const), (2) atomic   1. Pointer arithmetic as cursor. The C code uses **src (double
scalar, or (3) shared mutable state requiring Mutex. Therefore, map-     indirection) to implement a mutable cursor into a buffer. The caller
ping of C unconstrained global mutability onto Rust’s structured         owns the buffer whilst the cursor tracks a position within it. c2rust
concurrency model requires reconstructing the program’s intended         preserves this as *mut *mut c_char: an unchecked raw pointer.
sharing discipline, rather than translating the declarations.            The idiomatic version replaces this with &mut usize, translating
   These dimensions define the gap that any C-to-Rust translation        the index into a &[u8] slice. The translation requires recognising
approach must bridge, and most of them are semantic: they re-            that *mut *mut c_char is not a generic pointer-to-pointer, but a
quire preserving the intended behaviour of the C code rather than        specific cursor pattern.
merely transforming its syntax. As it will be shown in the next
                                                                         2. Implicit length through pointer difference. C code passes
section, with proper automation and translation methodology, the
                                                                         packet and packetlen separately and computes &packet+ptr via
gap can be bridged with modern Large Language Models.
                                                                         pointer arithmetic. c2rust translates this to packet.offset(ptr
                                                                         as isize), which is not checked against bounds, and relies on
2.1     The c2rust Transpiler                                            the caller to provide a valid offset. The idiomatic version fuses the
                                                                         pointer and length into a single &[u8] slice, eliminating the out-of-
As will be shown in Section 3.2, the ultimate approach for the trans-
                                                                         bounds class of bugs at the type level. Such an operation requires
lation from C to Rust is, in fact, a transition from non-idiomatic
                                                                         analyses of the API and propagation of the bounds.
Rust to the idiomatic one. This is possible because of lossless trans-
lation from pure C to non-idiomatic Rust at Clang Abstract Syntax        3. Manual memory copy via memcpy. The C code uses mem-
Tree (AST) level, with further iterative modification of software        cpy to copy label bytes. c2rust preserves this as an FFI call to libc,
components on a per-function basis.                                      which preserves all risks associated with unsafe memory modifica-
   The c2rust [10] transpiler deals with the AST of compiling C          tion. The idiomatic version uses copy_from_slice, which panics
functions. It translates the C code into Clang’s internal represen-      on overflow rather than producing UB.
tation, translates the C AST into the Rust one, and then emits the       4. Null-terminated strings. The C code writes dst[len] = '\0'
Rust code for the corresponding AST. The transpiler preserves the        and relies on the caller to provide a large enough buffer. c2rust
control flow graph, the data flow, and the memory model of the           translates this to *dst.offset(len as isize) = 0 with no
original C: (1) functions are declared as extern "C" ABI, (2) global     checks. The idiomatic version handles the NUL terminator explic-
variables become static mut, (3) the pointer arithmetic is possible      itly within the slice, and callers must account for it. This snippet
via .offset(), and (4) the C standard library is called via libc FFI.    also represents the challenges of UTF-8 strings: DNS names are
   The transpiled code does not introduce any safety. For example,       non-UTF-8, thus &[u8] is used rather than &str.
during the transpiling, the C ptr[n] and ptr + n become Rust                 These four examples are endemic to C systems software. Next,
ptr.offset(n as isize). The pointer arithmetic is preserved,             we consider our methodology to resolve issues one by one.
AISM ’26, October 12–16, 2026, Munich, Germany                                                                                       Vasily A. Sartakov


      C (original)                                c2rust output                                  Idiomatic Rust
      int readname(                               pub unsafe extern "C" fn                       pub fn readname(
          char *packet,                           readname(                                           packet: &[u8],
          int packetlen,                               packet: *mut c_char,                           src_pos: &mut usize,
          char **src,                                  packetlen: c_int,                              dst: &mut [u8],
          char *dst,                                   src: *mut *mut c_char,                         length: usize)
          int length)                                  dst: *mut c_char,                           -> i32
      {                                                length: c_int)                            {
          int len = **src;                          -> c_int                                          let mut src = *src_pos;
          if (len > 63) {                         {                                                   let c = packet[src];
              int ptr = (len & 0x3f)                   let len = **src as c_int;                      src += 1;
                         << 8                          if len > 63 {                                  if c & 0xc0 == 0xc0 {
                         | *(*src + 1);                    let ptr = ...;                                 let offset = ...;
              return readname(                             return readname(                               let mut dummy = offset;
                  packet, packetlen,                           packet, packetlen,                         return readname_loop(
                  &packet + ptr,                               packet.offset(                                  packet, &mut dummy,
                  dst, length);                                     ptr as isize),                             &mut dst[..],
          }                                                    dst, length);                                   length, 10);
          memcpy(dst, *src + 1, len);                  }                                              }
          *src += len + 1;                             memcpy(dst as *mut _,                          let n = c as usize;
          dst[len] = '\0';                                    (*src).offset(1)                        dst[..n].copy_from_slice(
          return len;                                             as *const _,                            &packet[src..src + n]);
      }                                                       len as size_t);                         src += n;
                                                       *src = (*src).offset(                          *src_pos = src;
                                                           (len + 1) as isize);                       n as i32
                                                       *dst.offset(                              }
                                                           len as isize) = 0;
                                                       len
                                                  }


Figure 1: Three versions of the same DNS name decoding function. The c2rust version preserves C’s raw pointer semantics and
FFI dependencies; the idiomatic version uses slices, safe indexing, and zero unsafe.


3     Methodology                                                           C2: Slice-based buffer access. Buffer parameters must use &[u8]
We consider the translation of C to idiomatic Rust as a tooling             or &mut [u8] instead of raw C pointers such as const c_char or
problem of translation from non-idiomatic Rust to the idiomatic             mut c_char. Encoding length in the type eliminates the need for
one. Therefore, we introduce criteria to define the idiomatic Rust,         manual bounds management and prevents out-of-bounds access at
and assume that a program is properly implemented if it passes              the call site.
all functionality tests: produces the same output for the same in-          C3: No static mut. Global mutable state must not rely on static
put as the original program. The tooling component of the sys-              mut, which is incompatible with Rust’s aliasing and concurrency
tem works as a trial-and-error loop where the translating code-             guarantees. Simple global scalars use atomic types, for example
base always satisfies the functionality correctness criteria, whilst        AtomicUsize, whilst compound global state is wrapped in syn-
its components are replaced one-by-one on a per-function basis              chronisation primitives such as Mutex<T>. This removes a major
using LLM-powered reimplementation to satisfy the idiomaticity              source of UB inherited from C.
criteria.                                                                   C4: No extern "C" on internal functions. Only functions that
   The loop is agentic: the LLM system proposes an implementa-              participate directly in the FFI boundary (e.g., callbacks invoked
tion, compiles it, runs the runtime tests, and revises its own candi-       from C) may use the extern "C" ABI. All internal Rust functions
date from the feedback (compiler errors or trace divergence) with-          use the Rust ABI, preserving type checking and calling conven-
out per-step human action. Human involvement is confined to or-             tions within the Rust portion of the codebase.
chestration: the next migration unit and the architectural policy.
                                                                            C5: No C string or memory functions. C library routines such
                                                                            as strlen, strcpy, memcpy, malloc, and free are replaced with
                                                                            Rust standard library abstractions. String data is represented as
3.1     Criteria for Idiomatic Rust                                         &str when UTF-8 validity is guaranteed, or as &[u8] when arbi-
We define idiomatic Rust along five criteria. These serve as the ref-       trary byte sequences are required. This removes unchecked pointer
erence point for evaluating our methodology and its ability to pro-         arithmetic and manual memory management from safe code.
duce Rust code that aligns with established language practices.                These five criteria are not exhaustive, but they capture the essen-
                                                                            tial properties that distinguish idiomatic Rust from mechanically
C1: Zero unsafe in function signatures. A function’s type signa-            translated c2rust output. A codebase satisfying all five is safe by
ture must not expose unsafe to the caller. Localised unsafe {...}           construction in its safe regions, with unsafe confined to the FFI
blocks remain acceptable for operations that inherently require             boundary where it is unavoidable.
them (e.g., FFI calls), but the function must present a safe inter-
face. This ensures that safety invariants are enforced at the API
boundary rather than delegated to the caller.
From C to Idiomatic Rust: A Ship-of-Theseus Agentic Translation                                                                       AISM ’26, October 12–16, 2026, Munich, Germany



                           Verified                Leaf-based                   Gate A                   pass        Gate B             pass     Next Unit
                           Baseline                 Analysis        revise    Compilation                           Runtime                      or Phase



                                                                Agentic LLM                                                    fail
                                                            describe + implement
                                                                 revise + fix


                                                                                   Divergence
                                                                                                                Trace: old vs. new



Figure 2: Each transformation passes through two gates: compilation (A) and runtime verification (B). When Gate B fails, the
diagnostic loop traces old and new implementations and feeds the divergence back to the language model for revision.


3.2     Translation Stages                                                                  Two-phase separation. Due to the complexity of the translation
The pipeline comprises three components: (1) an automatic tran-                             processes and limits of language models, any complex modification
spiler (c2rust) that produces compilable but non-idiomatic Rust                             should be split into a set of basic, atomic steps: ultimately, we con-
from C source, (2) a language model that performs per-function                              sider translation as a tooling problem. We separate the translation
code transformations, and (3) an infrastructure that provides auto-                         into two phases.
mated gates, runtime tests, and trace-based diagnostics (Figure 2).                            Phase 1 targets function bodies and type signatures, addressing
                                                                                            criteria C1, C2, C4, and C5: removing unsafe from function types
Verified baseline. The functional correctness is the fundamental
                                                                                            (C1), replacing raw pointers with slices (C2), eliminating extern
oracle against which every subsequent transformation is validated.
                                                                                            "C" on internal functions (C4), and replacing C string functions
The building infrastructure is responsible for compiling the project
                                                                                            with Rust standard library equivalents (C5). This phase is mechan-
in various configurations: baseline, c2rust version, intermediate
                                                                                            ical and high-leverage: it eliminates the majority of unsafe surface
step version, versions with instrumentation. The latter is important
                                                                                            area in a project and can proceed without reasoning about shared
to check the functional equivalence at the function level: producing
                                                                                            mutable state or concurrent access.
the same output and state modification for the same input.
                                                                                               Phase 2 targets global mutable state, addressing the C3 criteria.
Leaf-based ordering. The transition is performed on per-function                            In this phase, the system converts each static mut declaration
basis. A static analysis of the c2rust codebase produces a directed                         to an Atomic* or Mutex<T> wrapper. This phase is challenging
call graph in which we select functions with no internal depen-                             because it requires reasoning about lock ordering and potential
dencies – leaf nodes. The leaf functions carry minimal risk of unin-                        deadlocks. Within Phase 2, the system follows a risk-ascending pri-
tended side effects. However, the transition to idiomatic Rust im-                          ority: atomic scalars first (no lock nesting, C3 satisfied statically),
pacts the caller functions as arguments passed into leaf functions                          then counters (snapshot-after-increment semantics), then simple
may require bounds.                                                                         Mutex wrappers on single-path data, and finally complex Mutex
   Once all leaves in a given dependency tier are ported, the next                          wrappers on data shared across multiple execution paths. The ratio-
tier – functions whose callees now reside entirely in the safe subset                       nale is that simpler wrappers are mechanically checkable, whilst
– becomes available. This bottom-up ordering guarantees that each                           complex wrappers require full-system lock-order analysis. Com-
transformation rests on a foundation of already-verified safe code.                         pleting Phase 1 before Phase 2 keeps this analysis tractable: with
Candidate Implementation. We feed the leaf functions one by                                 all function signatures already safe (C1, C2, C4, C5 satisfied), the
one into the LLM system. The system should describe what a par-                             lock-wrapping problem (C3) becomes self-contained.
ticular function does, and then implement this functionality in id-
iomatic Rust. The context includes the criteria for idiomaticity, the                           4 Implementation
source code of the C and c2rust versions, and tests if available. The                       We apply the methodology to a concrete case: translating the io-
process is iterative and agentic, bound with Gate A.                                        dine1 DNS tunnel from C to idiomatic Rust. Iodine is a real-world
A and B gates. When the candidate function is implemented, the                              systems program of moderate size — approximately 12.5 kSLOC
project must compile with zero errors. Beyond type-level errors                             of C across 17 source files — large enough to exhibit structural
such as signature mismatches, missing imports, incorrect API us-                            complexity. It exercises the full range of C idioms that resist me-
age, Gate A enforces the idiomatic and safety criteria (Section 3.1)                        chanical translation: raw pointer arithmetic, static buffers, func-
as hard errors.                                                                             tion pointers stored in structs (via encoder_ops), global mutable
   The system must run under a realistic workload for a sustained                           state, and extensive use of C string and memory routines such as
period processing real data. If it fails, both the old and new im-                          strlen, strcpy, and memcpy. These are precisely the patterns that
plementations are instrumented with equivalent trace output, ex-                            c2rust preserves verbatim and that our methodology is designed to
ecuted on identical inputs, and compared. The trace divergence is                           eliminate. The system also has a multi-layer client-server architec-
fed back to the language model, which revises the transformation.                           ture: the client encodes and encapsulates traffic into DNS queries,
This loop repeats until Gate B passes.                                                      1
                                                                                                https://code.kryo.se/iodine/
AISM ’26, October 12–16, 2026, Munich, Germany                                                                                 Vasily A. Sartakov


whilst the server decodes and forwards it, with both sides organ-         names, whilst Rust treats separately generated structs as incom-
ised around a select()-based event loop.                                  patible types, which prevents replacing extern "C" declarations
   This section describes the target architecture, the project-specific   with use imports and thus blocks function porting. In iodine, sock-
challenges that emerged during porting and which helped to gener-         addr_storage appeared in six files, tun_user in two, and packet,
alise the methodology. We also provide quantitative metrics used          connection, and query in three each. These duplicates produced
to track progress of the translation.                                     a cascading dependency freeze: an unportable function blocks its
                                                                          callers, which in turn block their callers.
4.1     Iodine Architecture                                                  We resolved this by introducing a single canonical module, re-
Iodine is a DNS tunnel that encapsulates IP packets inside DNS            moving duplicate definitions, and adding use imports at call sites.
queries and responses, allowing IP traffic to traverse networks that      Deduplication must follow dependency order (leaf types first); thus,
only permit DNS. The system has two components, iodined (server)          dependent functions can be ported at the signature level. This type-
and iodine (client). Both endpoints create and configure a tun            level deduplication is a prerequisite to function porting and is not
device: the client captures outgoing IP packets on its local tun,         captured by the leaf-based ordering.
fragments and encodes them into DNS messages, and sends those             FFI adapter scaffolding. During incremental porting, we encoun-
messages into the DNS resolution path. The server receives the en-        tered a recurring intermediate state. Safe Rust implementations of
coded payloads (typically routed indirectly via recursive resolvers       functionality (for example base32::encode) existed, but existing
to the authoritative host), decodes and reassembles the IP packets,       callers still passed C function pointers through a C struct such as
and injects them into its own tun interface for forwarding.               encoder_ops, which requires signatures like *const encoder. To
   When the client sends an IP packet, iodine processes it through        bridge this mismatch, we introduced thin _ffi wrappers that ac-
four stages. First, the payload is compressed (zlib via compress2         cept raw pointers, convert them to Rust slices, invoke the safe Rust
and uncompress) to reduce size as DNS labels and names impose             routine, and write results back into C buffers. Each wrapper was
strict length limits compared to typical MTU sizes. Second, the           paired with a static mut global holding the function pointer table
compressed bytes may be encrypted using a Blowfish cipher keyed           and often duplicated the original C struct definitions across com-
by a pre-shared password. Third, the resulting bytes are encoded          pilation units. These adapters enable mixed c2rust and Rust execu-
into a DNS-safe alphabet (one of Base32, Base64, etc.), trading en-       tion and let individual functions be ported early. These temporary
coding overhead against compatibility with DNS character restric-         solutions were removed at later stages.
tions. Fourth, the encoded data is embedded in a DNS query name           Static mut elimination and deadlock hazards. Phase 2 con-
(e.g., encoded-data.topdomain) and sent into the DNS resolution           verts static mut declarations to Atomic* or Mutex<T> wrappers.
path. The server extracts the payload from incoming queries, re-          The prescribed order is atomics first, then mutexes, and each global
verses the encode/decrypt/decompress pipeline, and writes the re-         must be wrapped one at a time with full runtime verification af-
constructed IP packet to its tunnel device. The reverse direction         ter each change. In the iodine client, we wrapped 16 static mut
embeds downstream data in DNS response records (TXT, MX, SRV,             globals, applying 13 atomics followed by 3 Mutex<T> wrappers. An
CNAME, A, NULL), completing the bidirectional tunnel.                     attempt to wrap all three mutexes in a single batch produced a
State machine. Iodine operates in two principal states. In the hand-      live deadlock: the tunnel established but transfers stalled at zero
shake state, the client and server negotiate connection parameters:       bytes. Reverting to one-at-a-time wrapping with runtime tests ex-
authentication, protocol version, encoding codec, DNS query type,         posed two silent deadlock patterns that the compiler does not de-
tunnel MTU, and optional EDNS0 extensions. They use message               tect. Both patterns compile and pass static checks but fail only un-
exchanges with timeouts and retries for each stage. Once the hand-        der real traffic. The practical rule is strict: perform Phase 2 one
shake completes, the system transitions to the tunnel state, where        global at a time and run full runtime tests after each wrapping.
raw IP traffic flows bidirectionally: upstream from client to server      Unwrappable static mut from C state. POSIX getopt() com-
via DNS queries and downstream via DNS responses. Both direc-             municates via globals (optarg, optind, opterr, optopt), which
tions use a sliding-window fragmentation and reassembly proto-            appear in Rust as extern "C" { static mut optarg: *mut c_-
col, as individual packets may be split across multiple messages.         char; static mut optind: c_int; }. These extern statics can-
                                                                          not be converted to Atomic or Mutex<T> because writes originate
4.2     Porting Challenges                                                inside the C library and bypass any Rust-side wrapper. Demoting
The methodology presented in this work is a human-in-the-loop             static mut to immutable static is ineffective since extern static
translation pipeline developed and generalised during the trans-          access remains unsafe. The only sound solution is to remove the
lation of the iodine project: the per-function transformation and         C global state by replacing getopt() with a Rust argument parser
verification loop is automated and agentic, whilst a human pro-           (for example, iterating std::env::args() and parsing flags). This
vides strategic orchestration. In this section, we describe project-      is a structural refactor for both client and server entry points. We
specific challenges that emerged during this process. Most were           deferred it because the extern statics are confined to main(), used
orchestration-level tasks — type deduplication, lock-wrapping, and        single-threadedly, and present a small, auditable unsafe surface.
C-library globals — handled by humans as exceptions.                      In the future, this should affect the methodology to treat C library
c2rust duplicate struct definitions. c2rust translates each C trans-      globals as replacement tasks, not Phase 2 wrapping candidates.
lation unit independently. Therefore, structs defined in multiple .c
files become multiple, distinct Rust types. C linker matches struct
From C to Idiomatic Rust: A Ship-of-Theseus Agentic Translation                                              AISM ’26, October 12–16, 2026, Munich, Germany


         350                                                           Server                                 Client                Static-mut   100
                                                                       porting                               porting                   elim.EX
         300
                                                                                                                                          PA     80
         250                                                                                                                            SAFE%




                                                                                                                                                       Safety Score (%)
         200
                                                                                                                                        RUST%    60
 Count




         150                                                                                                                                     40
         100
                                                                                                                                                 20
          50
           0                                                                                                                                     0
               1                       10                         20                            30                             40
                                                                       Commit

                                 Figure 3: Evolution of the SAFE% and RUST% metrics over the commit history.


4.3        Evolution of Safety                                                   Validation. Functional equivalence was verified end-to-end: after
We track translation progress over the c2rust baseline using two                 each of the 168 function ports and each of the 37 static mut wrap-
measures, each defined as the share of initial C-origin artefacts                pings (16 client, 21 server), Gate B ran the tunnel against the public
eliminated. The first, SAFE%, removes the C ABI surface: unsafe                  resolver under real traffic for 30 s or more, verified curl down-
extern "C" fn declarations (EX) and #[no_mangle] annotations                     load and netperf through the tunnel, and passed a wire-format
(NM). The second, RUST%, removes C-style unsafe patterns in func-                integration test. This oracle caught what static checks missed: a
tion bodies: raw pointer arithmetic (PA) and deep unsafe operations              batch mutex wrap that compiled but deadlocked under load (two
such as copy_nonoverlapping and write_bytes (DU).                                silent lock-pattern defects), a NUL-termination bug in send_query,
   Subscript 0 denotes the initial count in the c2rust baseline, and             a codec-command mismatch in fragsize negotiation, and timeouts
both measures report percentages of that count:                                  on non-UTF-8 hostnames — each diagnosed from runtime diver-
                                                                                 gence and revised within the loop, reverting to the last verified
                                                                                 state where needed. Client porting and static-mut elimination cut
                        EX + NM                      PA + DU
SAFE% = 100(1 −                  ), RUST% = 100(1 −           )                  the client’s unsafe blocks from roughly 86 to 40.
                       EX0 + NM0                    PA0 + DU0
                                                                                 Models. The proposed methodology does not require long con-
   We omit the raw unsafe count: porting moves unsafe from                       text, because it is based on iterative re-initialisation of the context
function declarations into narrow blocks around FFI calls, so count-             for each new function. For each function identified at the current
ing it would penalise correct refactoring.                                       leaf level, we create new context filling the precise and short de-
   Figure 3 plots the two measures per commit (each commit ports                 scription of the task. We performed translation using subscription-
one to ten functions, always from the same functional component).                based plans and the OpenCode-based infrastructure, enhanced by
The c2rust baseline holds 178 EX, 73 NM, 319 PA, and 144 DU. Server              the rtk and OAC. That a particular model choice does not materi-
porting (commits 1–31) lifts SAFE% to 72% and RUST% to 47%; client               ally affect the outcome is itself evidence of the loop’s autonomy: be-
porting (commits 32–41) completes all 168 signatures at SAFE%=95%;               cause Gates A and B drive revision from compiler and runtime feed-
static-mut elimination (commits 39–45, extending to the end of his-              back, the migration is steered by the loop rather than by the model;
tory) wraps the 37 static mut globals (16 client, 21 server) in                  the best result (fewest iterations) was achieved with Qwen3.6-27B.
atomics or mutexes, lifting RUST% to its final 57%.
   The steep rise at commit 15 is a type-level refactor — the Codec
                                                                                 5 Related Work
enum replacing four duplicated C function-pointer structs and eight
FFI adapter wrappers — rather than incremental function porting.                 Rule-based C-to-Rust translation. Compiler-based approaches
The plateaus are structural: the residual SAFE% gap is the five signal-          translate C to Rust using deterministic analyses and transforma-
handler EX type aliases and six #[no_mangle] entry-point annota-                 tions. c2rust [10] provides the canonical transpilation pipeline by
tions, and the un-recovered RUST% is 99 PA and 99 DU uses confined               preserving the original program structure and generating function-
to the FFI boundary adapters (tun-device and socket I/O; roughly                 ally equivalent Rust. Subsequent work extends this through own-
75 of the PA sites in iodined.rs), where raw pointers are inherent               ership inference [14], alias analysis [3], and specialised transfor-
to interacting with C: indexing the C-allocated per-user struct ar-              mations for challenging C constructs including output parameters,
ray via USERS.offset(i) and skipping bytes in DNS wire buffers.                  unions, and C I/O APIs [6–8]. These techniques improve the safety
   The final codebase is approximately 10.3 kSLOC of idiomatic                   and idiomaticity of generated code by addressing specific language
Rust across 16 files, translated from an original 12.5 kSLOC C code-             features whilst preserving program behaviour. Nevertheless, these
base, with no unsafe extern "C" function declarations and no                     remain compiler-driven, isolated transformations targeting specific
static mut left in the evaluated code. The translation took 37                   translation problems rather than end-to-end migration. We use
developer-hours over four working days — 4.5 functions and roughly               c2rust as a lossless translation stage, producing a functionally equiv-
278 lines per hour.                                                              alent but non-idiomatic Rust baseline for refinement.
AISM ’26, October 12–16, 2026, Munich, Germany                                                                                              Vasily A. Sartakov


LLM-based C-to-Rust translation. Recent work employs large               reactive. Combining runtime testing with static analysis, symbolic
language models to generate idiomatic Rust directly from C source        execution, or automated test generation could provide stronger
code. Existing systems improve translation quality through iter-         correctness guarantees and reduce manual oversight required.
ative generation, compilation feedback, repair loops, and valida-           Third, although many functions can be migrated independently,
tion [4, 11, 13, 15]. Compared with compiler-based approaches,           architectural changes — such as redesigning shared state or replac-
these methods often produce more natural Rust by leveraging se-          ing C-specific libraries — require reasoning across the entire code-
mantic reasoning. Nevertheless, they primarily frame migration as        base. Repository-level information, including dependency graphs
a code generation problem, with the model synthesising a correct         and commit history, may help recover developer intent and guide
Rust implementation from the original C program. In contrast, we         these broader transformations. This information was not needed in
frame migration as a verified refactoring problem: starting from         our study, but may be important for full-project migration. Fourth,
a mechanically translated Rust, we incrementally transform indi-         the orchestration itself must scale: from a single human steering
vidual functions into idiomatic Rust whilst preserving behavioural       the loop to systems that plan, verify, and coordinate large num-
equivalence through compilation and runtime verification.                bers of incremental transformations whilst keeping the software
Project-level migration. Recent research extends C-to-Rust trans-        continuously functional.
lation beyond individual functions by incorporating repository con-
text, dependency information, build systems, and incremental com-        Acknowledgements
pilation. RustMap [1], repository-level translation frameworks [2],      ChatGPT and Copilot were used to proofread sections of this work.
and EvoC2Rust [12] demonstrate that exploiting project-level in-
formation substantially improves compilation success and scala-          References
bility for large codebases. Some of these approaches further sug-         [1] Xuemeng Cai, Jiakun Liu, Xiping Huang, Yijun Yu, Haitao Wu, Chunmiao Li,
                                                                              Bo Wang, Imam Nur Bani Yusuf, and Lingxiao Jiang. 2025. RustMap: Towards
gest that repository evolution, such as commit history, may pro-              project-scale C-to-Rust migration via program analysis and LLM. In Interna-
vide additional semantic context during translation. Our work is              tional Conference on Engineering of Complex Computer Systems. Springer, 283–
complementary to these efforts. Rather than focusing on enrich-               302.
                                                                          [2] Saman Dehghan, Tianran Sun, Tianxiang Wu, Zihan Li, and Reyhaneh Jabbar-
ing the translation context, we study the migration workflow itself:          vand. 2025. Translating Large-Scale C Repositories to Idiomatic Rust. arXiv
dependency-aware function ordering, explicit idiomaticity criteria,           preprint arXiv:2511.20617 (2025).
                                                                          [3] Mehmet Emre, Peter Boyland, Aesha Parekh, Ryan Schroeder, Kyle Dewey, and
incremental replacement of non-idiomatic components, and ver-                 Ben Hardekopf. 2023. Aliasing limits on translating C to safe Rust. Proceedings
ification gates that ensure the translated system remains contin-             of the ACM on Programming Languages 7, OOPSLA1 (2023), 551–579.
uously executable throughout the migration process. In our case           [4] Hasan Ferit Eniser, Hanliang Zhang, Cristina David, Meng Wang, Maria Chris-
                                                                              takis, Brandon Paulsen, Joey Dodds, and Daniel Kroening. 2025. Towards
study, repository history was not required to perform the migra-              Translating Real-World Code with LLMs: A Study of Translating to Rust.
tion, suggesting that continuous verification and dependency-aware            arXiv:2405.11514 [cs.SE] https://arxiv.org/abs/2405.11514
orchestration can be sufficient without historical development con-       [5] Jens Gustedt. 2019. Modern C (2 ed.). Manning Publications.
                                                                          [6] Jaemin Hong and Sukyoung Ryu. 2024. Don’t write, but return: Replacing output
text, but conceptually can be combined.                                       parameters with algebraic data types in C-to-Rust translation. Proceedings of the
                                                                              ACM on Programming Languages 8, PLDI (2024), 716–740.
                                                                          [7] Jaemin Hong and Sukyoung Ryu. 2024. To tag, or not to tag: Translating C’s
6    Conclusion                                                               unions to Rust’s tagged unions. In Proceedings of the 39th IEEE/ACM International
C remains the foundation of much deployed systems software, but               Conference on Automated Software Engineering. 40–52.
                                                                          [8] Jaemin Hong and Sukyoung Ryu. 2025. Forcrat: Automatic I/O API Trans-
its unchecked pointer arithmetic, manual memory management,                   lation from C to Rust via Origin and Capability Analysis. arXiv preprint
and unconstrained global state make long-term maintenance and                 arXiv:2506.01427 (2025).
                                                                          [9] Brian W. Kernighan and Dennis M. Ritchie. 1988. The C Programming Language
security difficult. Rust offers stronger safety guarantees, yet mi-           (2 ed.). Prentice Hall.
grating existing C codebases is hard because idiomatic Rust re-          [10] Erik Kristensen, Peter Korley, Anders Andersen, Zvonimir Pavlinovic, Thomas
quires semantic information that C does not encode.                           Wies, and Shuvendu K. Lahiri. 2022. C2Rust: A Tool for Migrating C Code to
                                                                              Rust. In Proceedings of the 44th International Conference on Software Engineering:
   In this paper, we present a translation pipeline that treats C             Software Engineering in Practice (ICSE-SEIP). ACM.
to Rust migration as a sequence of correctness-preserving, per-          [11] Momoko Shiraishi, Yinzhi Cao, and Takahiro Shinagawa. 2024. SmartC2Rust:
function replacements. Starting from a lossless c2rust baseline, we           Iterative, Feedback-Driven C-to-Rust Translation via Large Language Models
                                                                              for Safety and Equivalence. arXiv preprint arXiv:2409.10506 (2024).
use an agentic loop that rewrites functions into idiomatic Rust          [12] Chaofan Wang, Tingrui Yu, Beijun Shen, Jie Wang, Dong Chen, Wenrui Zhang,
whilst enforcing behavioural equivalence through runtime gates.               Yuling Shi, Chen Xie, and Xiaodong Gu. 2025. EvoC2Rust: A skeleton-guided
                                                                              framework for project-level C-to-Rust translation. (2025).
                                                                         [13] Zhen Yang, Fang Liu, Zhongxing Yu, Jacky Wai Keung, Jia Li, Shuo Liu, Yifan
7    Future Work                                                              Hong, Xiaoxue Ma, Zhi Jin, and Ge Li. 2024. Exploring and unleashing the power
                                                                              of large language models in automated code translation. Proceedings of the ACM
This work will be extended in four directions: generalisation, veri-          on Software Engineering 1, FSE (2024), 1585–1608.
fication-driven translation, whole-project reasoning, and migration      [14] Hanliang Zhang, Cristina David, Yijun Yu, and Meng Wang. 2023. Ownership
                                                                              guided C to Rust translation. In International Conference on Computer Aided Ver-
orchestration. First, we will generalise the methodology beyond               ification. Springer, 459–482.
the iodine case study. Iodine is a single, moderate-size systems         [15] Han Zhou, Yu Luo, Mengtao Zhang, and Dianxiang Xu. 2025. C2RustTV:
program, so we will apply the loop to a broad range of C projects             An LLM-based Framework for C to Rust Translation and Validation. In 2025
                                                                              IEEE 49th Annual Computers, Software, and Applications Conference (COMPSAC).
spanning different sizes, domains, and concurrency profiles (de-              1254–1259. doi:10.1109/COMPSAC65507.2025.00158
vice drivers and OS components). Demonstrating transfer across
these projects will establish generalisability. Second, compilation      Received 2026-08-11; accepted 2026-08-23
and behavioural testing validate each step, but the process is largely
