                                         BeePL: Correct-by-compilation kernel extensions
                                         SWARN PRIYA, Virginia Tech, USA
                                         FRÉDÉRIC BESSON, Inria, France
                                         CONNOR SUGHRUE, Virginia Tech, USA
                                         TIM STEENVOORDEN, Open Universiteit of the Netherlands, Netherlands
                                         JAMIE FULFORD, University of Illinois Urbana-Champaign, USA
                                         FREEK VERBEEK, Open Universiteit of the Netherlands, Netherlands and Virginia Tech, USA
                                         BINOY RAVINDRAN, Virginia Tech, USA
arXiv:2507.09883v1 [cs.PL] 14 Jul 2025




                                         eBPF (extended Berkeley Packet Filter) is a technology that allows developers to safely extend kernel function-
                                         ality without modifying kernel source code or developing loadable kernel modules. Since the kernel governs
                                         critical system operations and enforces isolation boundaries between user space and privileged data, any
                                         mechanism that modifies its behavior must meet the highest standards of safety and correctness. To this end,
                                         the eBPF toolchain includes a verifier, which statically checks safety properties such as memory access validity,
                                         bounded loops, and type correctness before loading the program into the kernel. However, several recent
                                         studies have demonstrated that the existing verifier is both overly conservative in some cases—rejecting valid
                                         programs—and unsound in others, permitting unsafe behavior that violates the intended semantics of the
                                         kernel interface.
                                            To address these challenges, we introduce BeePL, a domain-specific language for eBPF with a formally
                                         verified type system. The BeePL type system, along with the language design, statically enforces key safety
                                         properties such as type-correct memory access, safe pointer usage, absence of unbounded loops, and structured
                                         control flow. These guarantees are backed by formal type soundness proofs, ensuring that well-typed programs
                                         satisfy the safety invariants required by the eBPF execution environment. BeePL also proves that well-typed
                                         source programs meet critical eBPF-specific properties related to memory safety, termination, and control
                                         flow, enabling high-level reasoning prior to compilation. For properties not fully enforceable statically—such
                                         as dynamic bounds and undefined behavior—BeePL inserts semantics-preserving runtime checks during
                                         compilation. We develop a verified compilation strategy that extends CompCert to generate BPF bytecode
                                         from BeePL programs, establishing a principled foundation for an end-to-end verifiable toolchain for safe
                                         kernel extensions.

                                         ACM Reference Format:
                                         Swarn Priya, Frédéric Besson, Connor Sughrue, Tim Steenvoorden, Jamie Fulford, Freek Verbeek, and Binoy
                                         Ravindran. 2026. BeePL: Correct-by-compilation kernel extensions. 1, 1 (July 2026), 45 pages. https://doi.org/
                                         XXXXXXX.XXXXXXX


                                         Authors’ Contact Information: Swarn Priya, Virginia Tech, Blacksburg, USA, swarnp@vt.edu; Frédéric Besson, Inria, Rennes,
                                         France, frederic.besson@inria.fr; Connor Sughrue, Virginia Tech, Blacksburg, USA, cpsughrue@vt.edu; Tim Steenvoorden,
                                         Open Universiteit of the Netherlands, Heerlen, Netherlands, tim.steenvoorden@ou.nl; Jamie Fulford, University of Illinois
                                         Urbana-Champaign, Urbana-Champaign, USA, jamiehf2@illinois.edu; Freek Verbeek, Open Universiteit of the Netherlands,
                                         Heerlen, Netherlands and Virginia Tech, Blacksburg, USA, freek@vt.edu; Binoy Ravindran, Virginia Tech, Blacksburg, USA,
                                         binoy@vt.edu.


                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the
                                         full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored.
                                         Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
                                         prior specific permission and/or a fee. Request permissions from permissions@acm.org.
                                         © 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM XXXX-XXXX/2026/7-ART
                                         https://doi.org/XXXXXXX.XXXXXXX


                                                                                                                   , Vol. 1, No. 1, Article . Publication date: July 2026.
2


1     Introduction
eBPF [16] is a revolutionary technology that enables safe, efficient, and dynamic instrumentation
of the Linux kernel without requiring modifications to the kernel source code or the use of loadable
kernel modules. It empowers developers to write user-defined programs that execute in kernel
space, extending the kernel’s capabilities in areas such as performance monitoring, network packet
filtering, system call tracing, and malware inspection. This flexibility has made eBPF a foundational
component in modern observability and security tooling. It underpins a wide range of high-
performance applications [17], including networking frameworks (such as Meta’s Katran [4]
and Google’s Cilium [20]), security enforcement platforms (like Cloudflare [14] and Falco [18]),
observability solutions (like Netflix [46]), and performance monitoring tools (deployed at AWS [52]).
Initially, eBPF programs were written in a restricted subset of C, but with increasing attention
from both industry and academia, support for writing eBPF programs in safer and more expressive
languages like Rust [30] has gained traction. To ensure safety and prevent buggy or malicious code
from compromising the kernel, the eBPF toolchain includes a critical static analysis component
known as the eBPF verifier. While there exists an informal specification for what constitutes a
safe eBPF program—covering properties like memory safety, bounded execution, control flow
integrity, valid helper usage, and safe pointer manipulation—this specification is neither formalized
nor explicitly documented. It is understood implicitly within the eBPF community. Currently, the
verifier enforces these checks, and only programs that pass are allowed to run in the kernel. Prior
research and CVEs (Common Vulnerabilities and Exposures) [41] show that it can both accept
unsafe programs and reject safe ones, revealing inconsistencies in its guarantees. These issues
highlight the need for a more rigorous, formal foundation for verifying eBPF programs.
    We formalize a set of key safety properties for eBPF programs and provide a trustworthy foun-
dation for building compliant kernel extensions. Our language enforces many of these properties
statically via its type system, while others—like dynamic memory safety—are ensured through
semantics-preserving transformations by a verified compiler. The properties we capture include
absence of uninitialized memory access, null dereferences, undefined behavior, guaranteed termi-
nation, memory bounds safety, and adherence to eBPF-specific typing rules.

1.1    Problem Statement
The existing eBPF ecosystem lacks a formally verified approach to guarantee the safety and security
of programs loaded into the kernel. Here, we outline the key problem statements we aim to address.
A detailed discussion of related efforts and prior work in these directions is provided in Section 5.

   The eBPF verifier is limited and unsound. One of the major drawback’s of the eBPF verifier is its
unsoundness. Several reports [26][44][58] have highlighted logical bugs in the verifier that lead to
false negatives, allowing unsafe programs to pass verification. This can have severe consequences,
including kernel memory corruption [28] and security vulnerabilities [36] [42]. The complexity of
a program depends not only on the number of instructions but also on the number of branching
instructions in the program. For each branch, the verifier needs to fork the state to produce two
states that need to be analyzed separately. The verifier has limited resources and can suffer from
state explosion.

  The absence of a type-safe language for eBPF development. Several approaches have explored
using strongly typed languages for writing eBPF and user-space programs, including Rust [30, 51],
Go [19, 47], Elixir [6] and Lua [29]. These languages aim to provide a safer and more accessible
programming experience, either through built-in safety features or by relying on the verifier for
enforcement.

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                                     3

                               eBPF Properties                                Languages
                           Checked at compile-time        C   Rust   Elixir    Go Python   Lua   BeePL
                                   Type safety            #
                                                          G    ✓       #
                                                                       G       ✓      ×     ×      ✓
                                  Termination             ×    ×       ✓        ×     ×     ×      ✓
                                   Stack usage            ×    #
                                                               G       ✓        ×     ×     ×      ×
                              Register state safety       ×    ✓       #
                                                                       G        ×     ×     ×      ✓
                                 Memory safety            ×    ✓       #
                                                                       G        ×     ×     ×      ✓
                             Helper functions safety      ×    #
                                                               G       #
                                                                       G        ×     ×     ×      #
                                                                                                   G
                          Absence of undefined behavior   ×    ✓       #
                                                                       G        ×     ×     ×      ✓
                              Certified compilation       #
                                                          G    ×       ×        ×     ×     ×      #
                                                                                                   G
                       Table 1. Languages and their support for properties of interest


   Table 1 compares several languages—C, Rust, Elixir, and Lua for eBPF programs, and Go and
Python for user-space tools—based on their ability to statically reason about eBPF properties.
Symbols denote whether a language cannot (×), can (✓), or partially (G    #) verify a given property
statically. C remains dominant for eBPF development due to its performance and integration with
Clang/LLVM, but its type system cannot reason about termination, stack usage, uninitialized
registers, or memory safety, and relies heavily on the eBPF verifier. Rust offers memory safety,
bounds checking, and safe map access, but lacks termination analysis and certified BPF compilation.
Honey Potion, an eBPF backend for Elixir, uses language features and code generation to reason
about termination and stack use, but lacks formal guarantees. Lua, Go, and Python provide high-
level abstractions but offer limited safety guarantees. The core challenge is the lack of a type system
and a formal approach that fully captures eBPF safety properties—a gap BeePL aims to fill.
   Lack of certified compilation. Ensuring eBPF safety properties at the source level alone is insuffi-
cient, as compiler optimizations can inadvertently break these guarantees when generating BPF
bytecode. For instance, while Rust can statically enforce several eBPF safety properties (as shown in
Table 1), there is no assurance that these properties are preserved in the compiled BPF bytecode due
to the lack of a formally verified, property-preserving compiler. The work in [21] highlights several
attack patterns that exploit the unsoundness of Rust’s compiler, demonstrating how “safe" Rust
can fail to uphold critical safety properties. Their analysis reveals vulnerabilities in Rust’s borrow
checker, type system, and lifetime inference, which can lead to violations of its safety guarantees.

1.2   Contributions
We present an end-to-end framework for building safe and secure eBPF programs using a strong
type system and certified compilation. Our toolchain automates safety enforcement through static
checks and runtime-preserving transformations, eliminating the need for manual formal reasoning.
The framework includes BeePL—a verification-friendly language with a rich type system and a
compiler that translates BeePL to C. The generated C code is subsequently compiled to BPF bytecode
using CompCert. We extend CompCert with a new backend that targets eBPF bytecode, and this
backend is formally verified in the Rocq theorem prover to ensure preservation of functional
correctness. BeePL enforces memory safety by disallowing unsafe pointer operations and requiring
null checks via option types and pattern matching. It supports structured memory access and
guarantees no out-of-bounds errors through safe byte-pattern matching. Control-flow safety is
ensured by only allowing terminating, bounded for-loops. By shifting safety checks to compile
time and using a verified compiler, BeePL reliably produces correct C and BPF bytecode.
   Contributions in nutshell
 • A language called BeePL, featuring a type system that reasons about side effects, unsafe pointer
   manipulations, termination, and type signatures of helper functions.
 • A compiler that translates BeePL to C while automatically enforcing safety properties through
   program transformations, without requiring manual checks.

                                                                               , Vol. 1, No. 1, Article . Publication date: July 2026.
  4


      • A CompCert extension for BPF bytecode generation, with mechanized proofs in Rocq ensuring
        preservation of functional correctness.
      • Formal pencil-and-paper proofs establishing the type soundness of the BeePL type system.
      • BeePL enforces a set of eBPF safety properties, supported by formal pencil-and-paper proofs.
      • A study illustrating how BeePL can eliminate several previously reported eBPF vulnerabilities.

  1.3     Motivating examples
  In this section, we present some motivating examples showcasing the features of BeePL language
  and its compiler. We examine a series of well-documented vulnerabilities and bug reports related to
  the eBPF verifier, many of which have led to critical security issues and assigned CVEs. We revisit
  some of these vulnerabilities and demonstrate how BeePL, by design, avoids these pitfalls through
  its strong type system and precise program transformations.
     CVE-2021-3600 [34] highlights a critical flaw in the eBPF verifier related to the incorrect handling
  of 32-bit division and modulo operations. Specifically, the verifier fails to properly account for
  the truncation of the source register when performing 32-bit div or mod operations, which can
  result in unexpected values being propagated. This misbehavior can lead to out-of-bounds memory
  accesses—both reads and writes—posing a serious threat to system integrity. Figure 1 shows the
  C representation of the eBPF bytecode [32] corresponding to the CVE-2021-3600 [34], where a
  division or modulo operation is performed with a divisor that may become zero due to truncation.
  In this example, the check in line 6 guards the 64-bit register r0, but the actual operation in line 4
  uses its truncated 32-bit counterpart w0. The verifier incorrectly assumes that the non-zero value
  of r0 ensures safety, but fails to account for the fact that truncating r0 to w0 yields zero, leading to
  a divide-by-zero error—an instance of undefined behavior.

1 SEC("xdp")                                                        1 #section "xdp"
2 int prog1(struct xdp_md ∗ctx) {                                   2 fun bprog1(option(struct xdp_md★) ctx) : int {
3    long r0 = 0x100000000; // 2^32 − 64 bits can fit, but not 32   3   let r0 : long = 0x100000000 in
4    int w0 = (int)r0; // truncates to 0 (lower 32 bits)            4      let w0 : int = (int)r0 in
5    int w1 = 3;                                                    5         let w1 : int = 3 in
6    if (r0 != 0) { w1 = w1 % w0; } // Dangerous: w0 == 0 :         6             if (r0 != 0) then let w1 = w1 % w0 in XDP_PASS else
         division/modulo−by−zero                                             XDP_PASS
7   return XDP_PASS;                                                7 }
8 }                                                                 8 char LICENSE[] #section "license" = "GPL";
9 char LICENSE[] SEC("license") = "GPL";                            9 // Division by zero eliminated due to program transformation done
                                                                             by BeePL compiler


  Fig. 1. eBPF program in C for CVE-2021-3600 (al-
  lows division or modulus by zero)                                           Fig. 2. BeePL program for CVE-2021-3600


     In contrast, Figure 2 presents the same logic written in BeePL. In BeePL, the compiler explicitly
  tracks truncation and enforces safety through a program transformation (done by BeePL compiler)
  that rewrites operations like w1 % w0 into a guarded conditional form: if w0 == 0 then 0 else w1
  % w0. This transformation ensures that unsafe modulo or division operations on zero are never
  emitted, effectively eliminating this entire class of verifier-bypass vulnerabilities.
     CVE-2020-8835 [33] reports a vulnerability where the eBPF verifier failed to properly track 32-bit
  register values used as shift operands. For example, an instruction like 𝑟 = 𝑟 >> 𝑟 , with 𝑟 initialized
  to 808464432 (a long), may result in undefined behavior if the shift amount is ≥64. The verifier
  should enforce an upper bound (i.e., ≤63 for 64-bit values), but in this case [27], it allowed the
  program to pass despite the unsafe operation. BeePL prevents such undefined behaviors through
  compile-time transformations. In particular, for shift operations, the BeePL compiler inserts explicit
  bounds checks to eliminate unsafe execution paths.

  , Vol. 1, No. 1, Article . Publication date: July 2026.
   BeePL: Correct-by-compilation kernel extensions                                                                                             5


       CVE-2022-23222 [35] exposes a critical flaw in the eBPF verifier’s handling of ∗ OR NULL
   pointers. These may be NULL or valid, and the verifier must ensure safety before any arithmetic.
   However, due to a missing sanity check in adjust ptr min max vals within kernel/bpf/verifier.c,
   it incorrectly allows pointer arithmetic on possibly NULL values, leading to out-of-bounds access
   and potential privilege escalation.

1 SEC("xdp")                                                 1   #section "xdp"
2 struct { ... } counter_table SEC(".maps");                 2   struct { ... } counter_table #section ".maps"
3 int cprog2(struct xdp_md ∗ctx) {                           3   fun bprog2(option(struct xdp_md★) ctx) : int {
4    long uid;                                               4      let uid : long★ = ref(0) in
5    long ∗p;                                                5         let _ = uid := bpf_get_current_uid_gid() & 0xFFFFFFFF in
6    uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;           6            let p : option(long∗) = bpf_map_lookup_elem(counter_table, uid) in
7    p = bpf_map_lookup_elem(&counter_table, (&uid));        7                (int)!p
8    return (int)∗p // Dangerous: dereferencing may be       8   }
          NULL                                               9   char LICENSE[] #section "license" = "GPL";
 9 }                                                        10   // Rejected by the BeePL type system as dereferencing(!) an option type is
10 char LICENSE[] SEC("license") = "GPL";                                not allowed



   Fig. 3. eBPF program in C for CVE-2022-                       Fig. 4. BeePL program for CVE-2022-23222 (safe BeePL is
   23222 (may lead to null pointer dereference)                  present in Figure 5)
      Figure 3 shows an eBPF program vulnerable to null pointer dereference. The helper function
   bpf map lookup elem returns a pointer to a map value or NULL if the key is not found. However,
   the returned pointer p is dereferenced without any null-check. This can lead to undefined behavior
   or a crash if p is NULL. This is the core issue behind CVE-2022-23222 [15] missing safety check before
   pointer dereference. Figure 4 shows the same logic written in BeePL. Here, bpf map lookup elem
   returns option(long★), making the possibility of a NULL value explicit in the type. The dereference
   !p is rejected by the type checker, as BeePL requires such operations to be guarded by pattern
   matching. Unlike C, all pointer-returning helper functions in BeePL return an option type, enabling
   null safety at the language level. During compilation, option types are translated back to regular
   pointers in C, with pattern matches ensuring that null dereferences cannot occur. This approach
   eliminates the need for manual null checks and ensures that programs like the one in Figure 4 are
   rejected by the type checker, preventing verifier bugs.

1 #section "xdp"                                                            1   SEC("xdp")
2 struct { ... } counter_table #section ".maps"                             2   struct { ... } counter_table #section ".maps";
3 fun bprog3(option(struct xdp_md★) ctx) : int {                            3   int cprog3(struct xdp_md ∗ctx) {
4    let uid : long★ = ref(0) in                                            4      long uid;
5       let _ = uid := bpf_get_current_uid_gid() & 0xFFFFFFFF in            5      long ∗p;
6          let p : option(long∗) = bpf_map_lookup_elem(counter_table,       6      long ∗p';
          uid) in                                                           7      uid = bpf_get_current_uid_gid() & 0xFFFFFFFF;
 7          match p with                                                    8      p = bpf_map_lookup_elem(&counter_table, (&uid));
 8           | pnone => −1                                                  9      if (p == (long ∗) 0) { return −1; }
 9           | psome p' => (int)!p'                                        10         else { p' = p;return (unsigned int) ∗p'; }
10 }                                                                       11   }
11 char LICENSE[] #section "license" = "GPL";                              12   char LICENSE[] SEC("license") = "GPL";



       Fig. 5. Safe BeePL program for CVE-2022-23222                            Fig. 6. Safe C program generated by BeePL com-
                                                                                piler for CVE-2022-23222
      Several CVEs involving NULL pointer dereference—CVE-2022-0433 [37], CVE-2022-3606 [38],
   CVE-2025-21852 [40], and CVE-2024-38566 [39]—can be eliminated using BeePL’s typechecker
   and program transformations performed by the compiler. Figure 5 shows the safe BeePL version
   of the unsafe program from Figure 4. Here, the possible null dereference is handled via a match
   expression (lines 6–8) on the option type. If p is Pnone, the function returns −1; otherwise, it
   safely dereferences the pointer inside Psome. This resolves the type checker error by ensuring

                                                                                    , Vol. 1, No. 1, Article . Publication date: July 2026.
6


dereferencing applies only to valid pointers. Additionally, no null check is needed on uid, as ref
guarantees non-null pointers. Figure 6 shows the generated C code, where an explicit null check
appears on line 9, inserted automatically by the BeePL compiler. This demonstrates how BeePL
enforces safe pointer usage and removes the burden of manual null checks.

      CVE-ID          Vulnerability                                                               BeePL   BeePL features
    CVE-2021-3600     Division/modulo with zero due to truncation of 64-bit to 32-bit               ✗              Program transformation
                                                                                                                        Type safety +
    CVE-2020-8835     Out-of-bounds reads and writes due to improper bound calculation in shift    ✗
                                                                                                                   Program transformation
                      operator
                                                                                                                        Type safety +
    CVE-2022-3606     Manipulation in the program operations leads to null pointer dereference     ✗
                                                                                                                   Program transformation
    CVE-2022-0433,
    CVE-2022-23222                                                                                                      Type safety +
                      Null pointer dereference flaw                                                ✗
    CVE-2025-21852,                                                                                                Program transformation
    CVE-2024-38566
                                                                                                                        Type safety +
    CVE-2021-3490     Improper ALU32 Bounds Tracking                                               ✗
                                                                                                                    No pointer arithmetic
    CVE-2021-31440,                                                                                                     Type safety +
                      Wrong assumption about bounds of 32-bit register values                      ✗
    CVE-2020-27194                                                                                                 Program transformation
                                     Table 2. CVE mitigated by BeePL’s verified compilation



   We examined a collection of known CVEs [41] related to the eBPF ecosystem to assess whether
BeePL can eliminate them through its design and guarantees. Table 2 summarizes these findings:
each CVE, its vulnerability type, a ✗ indicating vulnerabilities prevented by BeePL, and BeePL
features (type system, verified transformations) responsible for prevention. This case study shows
BeePL’s ability to eliminate critical bugs and highlights our goal to enable developers to safely
write eBPF programs without relying on the kernel verifier.

2      Formally verified end-to-end framework
Figure 7a presents an overview of our approach. We introduce BeePL, a programming language
designed with the expressive power necessary to write realistic eBPF programs. BeePL supports
multiple programming paradigms and features a type system that statically enforces key eBPF
properties—including type safety, termination, side effects, and correct usage of helper function
signatures—directly at the source level (see Table 1). BeePL also employs a range of program
transformations that eliminate undefined behavior and prevent out-of-bounds memory accesses.
The framework also includes a compiler that translates BeePL source code to C, which is then
compiled to BPF bytecode using CompCert [25].
   A key component of our framework is the formally verified BeePL compiler (Figure 7b), which
ensures that safe source programs compile to safe and secure target code. It parses BeePL source
into an AST, type-checks it, and compiles it to C, which is then compiled to BPF bytecode using
CompCert [25], a verified C-to-assembly compiler. The BeePL-to-C compiler is implemented in
the Rocq proof assistant, with passes extracted to OCaml. While the core compiler is verified
(BeePL using paper-based formal proofs and CompCert (with extension of eBPF backend) in Rocq),
the parser, lexer, and pretty-printer remain part of the trusted computing base. Our development
contributes 33,635 lines of Rocq code as a CompCert extension.

2.1       Formal specification for a set of eBPF properties
The primary objective behind the design of BeePL and its type system is to enable formal reasoning
about a well-defined set of safety properties critical to eBPF programs. We introduce a high-level
formal specification for a set of eBPF safety properties, and in Section 4.2, we prove that all
well-typed BeePL programs satisfy them. A program is considered eBPFsafe if it adheres to the
following properties (text shown in green highlights which specific component of the framework is

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                            7




                      (a) BeePL framework                                              (b) BeePL toolchain


responsible for enforcing each property). The formal specification provides a high-level judgment
involving a program 𝑃, an initial state 𝑠, a final state 𝑠 ′ , a result value 𝑣, and a step count 𝑛. It states
that if 𝑃 is well-typed and the initial state 𝑠 is well-formed, then the evaluation of 𝑃 transitions
from 𝑠 to 𝑠 ′ in 𝑛 steps, producing the value 𝑣. The detailed definitions of well-typed programs and
well-formed states are presented later in Section 3 and Section 4.
  • No uninitialized memory access (Language feature): All memory accesses involving point-
    ers (represented as location 𝑙 with offset 𝑜 in memory Θ and ! representing dereference)
    generated within BeePL are guaranteed to reference initialized memory locations.
                ∀𝑃, 𝑠, 𝑠 ′, 𝑣, 𝑛. ⊢ 𝑃 : well-typed ∧ well-formed(𝑠) ∧ 𝑠, 𝑃 ⇝𝑛 𝑠 ′, 𝑣 =⇒
                              ∀(𝑙, 𝑜), if !(𝑙, 𝑜) evaluated during execution, then ∃𝑖. 𝑠 Θ [𝑙, 𝑜] = 𝑖
 • No null pointer dereferences (Type system and runtime check): Every memory access is ensured to
   be safe using the type system and runtime checks, ruling out null pointer dereferences.
                   ∀𝑃, 𝑠, 𝑠 ′, 𝑣, 𝑛. ⊢ 𝑃 : well-typed ∧ well-formed(𝑠) ∧ 𝑠, 𝑃 ⇝𝑛 𝑠 ′, 𝑣 =⇒
                                 ∀(𝑙, 𝑜), if !(𝑙, 𝑜) evaluated during execution, then 𝑙 ≠ NULL
 • Memory bounds safety (Program transformation and runtime check): All memory accesses are verified
   to stay within bounds through program transformations and run-time checks, primarily for structured
   access patterns. Σ maps memory locations to their types and is used to compute type-specific sizes.
              ∀𝑃, 𝑠, 𝑠 ′, 𝑣, 𝑛, 𝑙, 𝑜, 𝜏 . ⊢ 𝑃 : well-typed ∧ well-formed(𝑠) ∧ 𝑠, 𝑃 ⇝𝑛 𝑠 ′, 𝑣 ∧
                                   struct of type 𝜏 is read at (𝑙, 𝑜) ⇒ 𝑜 + sizeof (𝜏) ≤ sizeof (Σ(𝑙))
 • Compliance on helper function signatures and section attributes (Type system): All helper function
   calls respect their declared signatures, ensuring correct usage and argument types. BeePL’s type system
   statically enforces that all global variables and eBPF functions are annotated with the appropriate section
   attributes. This ensures conformance with the kernel’s runtime placement and calling conventions.
 • Termination (Type system and language feature): Every program written in BeePL terminates, ruling
   out infinite loops or non-terminating behavior (ensuring no divergence effect in the inferred effect 𝜂 for
   the program P).
           ∀𝑃, 𝑠, 𝜂. ⊢ 𝑃 : well-typed ∧ well-formed(𝑠) =⇒ ∃𝑛, 𝑠 ′, 𝑣. 𝑠, 𝑃 ⇝𝑛 𝑠 ′, 𝑣 ∧ divergence ∉ 𝜂
 • Absence of undefined behavior (Type system and program transformation): Operations such as di-
   vision, modulo, or arithmetic on unbounded integers are assigned well-defined semantics. When their
   operands may lead to undefined behavior—such as division by zero or overflow—the BeePL compiler

                                                                      , Vol. 1, No. 1, Article . Publication date: July 2026.
8


     inserts guards and rewrites them into safe expressions. Any result outside the expected semantics is
     modeled as a special case called undef.
                ∀𝑃, 𝑠, 𝑠 ′, 𝑣, 𝑛.   ⊢ 𝑃 : well-typed ∧ well-formed(𝑠) ∧ 𝑠, 𝑃 ⇝𝑛 𝑠 ′, 𝑣 =⇒ 𝑣 ≠ undef

3    BeePL language and its type system
   Expressions. Expressions in BeePL (shown in Figure 8) are built from variables, constants, function
applications, operators, and let-bindings. The language includes control-flow constructs such as
conditionals and for-loops, supports external function calls, and allows initialization of user-defined
structs and fixed-size arrays. Pattern matching over optional values and binary data enables expres-
sive, type-safe deconstruction. The presence of the option type also facilitates pattern matching
over nullable references via the match construct, whose semantics and translation are described in
Section 3.2. This mechanism ensures that all cases—both Psome and Pnone—are explicitly handled,
further eliminating the possibility of undefined behavior due to null dereferencing. BeePL allows
the use of safe abstractions over direct pointer manipulations. By utilising the pattern matching
constructs, BeePL allows operations on packed data without relying on unsafe pointer arithmetic.
For instance, rather than casting raw pointers and adding offsets—a common practice in low-level
C code—BeePL code operates on bytes. Pattern matching on bytes in BeePL allows direct extrac-
tion of structured data from binary sequences. This enables precise control over byte alignment,
size, and type during parsing, without explicit pointer manipulation. Operators include standard
unary and binary forms, as well as primitive operators for mutable effects (e.g., ref, !, :=). A BeePL
program consists of a sequence of declarations—functions (local or external) and global variables.
Each function includes a signature specifying the return type, effects, parameters, local variables
(with types), and a body. A special flag field marks whether the function is an eBPF program,
enabling additional checks on section attributes and argument types to ensure consistency with
the associated eBPF hook. Both function and global variable declarations may include an optional
sec field for section attributes, which is None for regular functions.
   Types. BeePL features a rich type system that encompasses a diverse set of type constructs:
primitive types (𝜏𝑣 ), pointer types (𝜏∗), effectful function types (𝜏 →𝜂 𝜏), user-defined struct types
annotated with attributes (omitted in paper but incorporated in Rocq development), array types
(fixed-size, contiguous collections of elements of type 𝜏 and size 𝑛), a bytes type (representing
raw byte sequences that encapsulate data for structured access), and the unit type (indicating the
absence of meaningful data). The complete set of supported types is shown in Figure 9. Primitive
types (𝜏𝑣 ) capture low-level data representations, including booleans, integers parameterized by
bitwidth, signedness, and attributes, as well as long integers with similar qualifiers. Size is defined
as follows: 𝑠𝑧 ∈ isize ::= i8 | i16 | i32 and signedness as follows: 𝑠 ∈ sign ::= unsigned | signed .
   Pointer types (𝜏∗) denote memory references. In particular, 𝜏𝑏 ★ denotes a safe, statically trackable
reference to an allocated value (either local or global). References are introduced internally through
safe constructs like ref. This design is crucial in eBPF settings to differentiate between pointers
created inside the program and those originating externally. BeePL disallows returning the addresses
of local variables and it is ensured by the BeePL type system (present in Figure 12). option(𝜏∗)
represents references that may be null. This optional pointer type models a nullable reference—a
pointer that either refers to a valid value of type 𝜏, or denotes the absence of a value (i.e., null).
Such types are essential for capturing partiality, lookup failures, and conditionally available data in
low-level systems programming, especially in languages like C where nullability is pervasive but
not tracked by the type system.
   In BeePL, optional pointers play a crucial role in maintaining memory safety while enabling
expressive pointer usage. BeePL distinguishes between two sources of pointers: (1) those produced

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                                         9

    𝑒 ∈ expr ::= 𝑥                          variable                                 𝑜𝑝 ∈ op𝑝 ::= !         dereference
                | 𝑐                         constant                                             | :=       allocation
                | 𝑒 (𝑒 )                    application                                          | ref      reference
                | op(𝑒 )                    primitive operations                                 | uop      unary operation
                | let 𝑥 : 𝜏 = 𝑒 in 𝑒        let-binding                                          | bop      binary operation
                | if 𝑒 then 𝑒 else 𝑒        conditional
                | 𝑥 | (𝑓 , 𝑒 )              struct initialization                    𝑝 ∈ Pattern ::= pnone                None
                | 𝑒.𝑓                       field access                                            | psome 𝑥             Some
                | none                      none                                                    | (𝑥, 𝜏 ) : (𝑦, 𝜏 )   Bytes
                | some 𝑒                    some
                | match 𝑒 with 𝑝 → 𝑒        match                                  𝑐 ∈ Const ::= int             32-bit integers
                | for (𝑒 . . . 𝑒, 𝑑 ) 𝑒     for                                                 | long           64-bit integers
                | unit                      unit
                                                                                     𝑣 ∈ Value := unit           unit
                                                                                                 | bool          bool
     𝑓 𝑑𝑒𝑐𝑙 ∈ fundecl ::= ecall 𝑖𝑑 𝑒𝑠𝑔                                  external                 | int           int
                         | lcall 𝑖𝑑 𝑙𝑠𝑔                                 internal                 | long          long
    𝑔𝑑𝑒𝑐𝑙 ∈ globdecl ::= {gvar : (𝑥 : 𝜏, 𝑣); sec : option string}       global                   | (𝑙, 𝑛)        location
                                                                                                 | option 𝑣      option

    𝑒𝑠𝑔 ∈ sig ::= {argstype : 𝜏; restype : 𝜏; ef : 𝜂; cc : conv}
    𝑙𝑠𝑔 ∈ sig ::= {sec : option string; rt : 𝜏; ef : 𝜂; cc : conv; args : 𝑥, 𝜏; vars : 𝑦, 𝜏; body : 𝑒; flag : bool}

    𝑐𝑜 ∈ composite ::= 𝑥, 𝑦, 𝜏      composite definitions           P ∈ prog := {decl : fdecl | gdecl; cenv : 𝑐𝑜 } program

                                                   Fig. 8. Syntax of BeePL
   𝜏 ∈ type ::= 𝜏𝑣            prim type       𝜏𝑣 ∈ prim𝜏 ::= int 𝑠𝑧 𝑠       int           𝜏∗ ∈ ptr𝜏 ::= 𝜏𝑏 ★              ref type
               | 𝜏∗           pointer                       | long 𝑠        long                       | option(𝜏∗)       option type
               | 𝜏 →𝜂 𝜏       function                      | bool          boolean                    | ∗𝜏 →𝜂 𝜏          fun ptr
               | struct 𝑖𝑑    struct
               | 𝜏𝑣 [𝑛]       array           𝜏𝑏 ∈ basic𝜏 ::= 𝜏𝑣            value
               | bytes        bytes                          | struct 𝑖𝑑    struct
               | unit𝜏        unit                           | 𝜏𝑣 [𝑛]       array


                                             Fig. 9. Types supported by BeePL


by the ref expression, which allocates memory and returns a valid address, and (2) those obtained
from external functions. By design, the ref construct is guaranteed to allocate and return a valid
non-null pointer; thus, null-pointer checks are only necessary for external function calls that may
return invalid or null pointers. Unlike traditional C-style programming where null checks such as if
(p != NULL) are manually inserted and easy to forget, BeePL uses option(𝜏∗) to enforce nullability
at the type level. This approach enables the compiler—rather than the programmer—to insert
necessary null-pointer checks during translation to C, ensuring that no unchecked dereference
can occur. Moreover, the optional type clearly distinguishes between definitely valid pointers and
potentially null pointers, making pointer usage both explicit and verifiable.
   Extension of type system to capture effects. BeePL extends its type system with an effect system
(𝜂) to track the computational behavior of expressions, including allocation, reading, writing,
I/O, and divergence: 𝜂 ∈ effect ::= divergence | read | write | alloc | io. Each expression or
function is annotated with a list of effects summarizing its possible side effects. This allows the
compiler to enforce purity or track memory operations. Making effects explicit enables compile-
time reasoning about stateful or external operations, improving security and predictability. The
effect concatenation is written as ∔. Effects serve as a static approximation of runtime behavior

                                                                              , Vol. 1, No. 1, Article . Publication date: July 2026.
10


and align with operational semantics, where the tracked effects correspond to actual execution
steps. Currently, BeePL tracks abstract effects like read, write, alloc, and io. In future work, we plan
to extend this to richer properties—such as memory regions, access permissions, and data flow
tags—to support more precise analysis and modular safety reasoning.

3.1    Type System
Figure 10 presents the typing rules for BeePL. The typing judgment in BeePL is of the form
Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂, where Γ represents the typing environment that maps variables to their types,
and Σ denotes the store typing environment, which maps memory locations to their types. Π
denotes the struct environment, which encapsulates the type information associated with all struct
declarations in the program. This environment is consulted during type checking to validate the
use of struct expressions, such as field access and initialization, ensuring that the fields conform
to their declared types and attributes. On the other hand, Ψ represents the external function
signature environment. It records the expected type signatures of all external functions invoked
in the program, including eBPF helper functions. Instead of relying on standard BPF signature
files, we construct Ψ explicitly as a map within BeePL. This design choice is motivated by the fact
that the types of eBPF helper functions, as interpreted in BeePL, may differ from their low-level
C counterparts—particularly due to BeePL’s stricter typing and effect system. A more detailed
treatment of this distinction is provided in the subsequent discussion of the typing rules. Extensions
to the typing environment are denoted using the notation 𝑥 → 𝜏, Γ, where the first placeholder
represents the new variable, the second denotes its associated type, and the third refers to the
existing typing context being extended. Access to the typing environment is denoted by the notation
    = , where the first placeholder represents the typing environment, the second indicates the
variable or location being queried, and the third denotes the associated type. The operation yields
either Some 𝜏 if the variable or location exists in the context with type 𝜏, or None if it is not present.
   It is important to highlight that Σ is not required in the executable type checker, as BeePL’s
surface syntax does not permit programmers to write explicit memory locations. Concrete locations
are introduced only during the evaluation of expressions as part of intermediate computation steps.
Consequently, type information for these locations becomes relevant only during the reduction
phase and not during the initial type-checking phase. While the store typing environment is critical
for proving meta-theoretical properties such as progress and preservation, it is not involved in the
type-checking process for programs written by the user. BeePL disallows implicit casting, ensuring
that the type of a location is determined by its initial value at the time of allocation. This guarantees
that a location’s type remains fixed throughout execution, and thus, Σ—which maps each location
to its type—is sufficient for type-checking locations during evaluation.
   For clarity of presentation, we omit details such as size and signedness for primitive types like
int and long in the typing rules. The typing rule for variables retrieves the type of the variable 𝑥
from the typing context Γ and produces an empty effect 𝜙. Typing rules for values are generally
straightforward, with the exception of locations. In the case of locations, the type of a location 𝑙
is looked up in the store context Σ. The typing rule TAPP governs function application in BeePL,
covering both user-defined and external functions. The judgment Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏𝑒 , 𝜂 checks the
function expression’s type, while Γ, Σ, Π, Ψ ⊩ 𝑒 : 𝜏, 𝜂 ′ checks the argument expressions. A predicate
isExt(𝑒) distinguishes between internal and external functions. If 𝑒 refers to an external function,
its type is retrieved from the external environment Ψ and must match the inferred type 𝜏𝑒 . In
both cases, 𝑒 must have a function type 𝜏 →𝜂𝑒 𝜏𝑟 , denoting its argument type, effect, and return
type. The total effect of the application is the union of: 𝜂 (evaluating the function expression,
reducing to its declaration), 𝜂 ′ (evaluating the arguments), and 𝜂𝑒 (the function’s declared effect).
This rule ensures both type and effect safety, with explicit handling of external functions. While

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                                                11


                          Γ𝑥 =𝜏
           TVAR                                   TCONSI                                       TCONSL
                  Γ, Σ, Π, Ψ ⊢ 𝑥 : 𝜏, 𝜙                        Γ, Σ, Π, Ψ ⊢ 𝑖 : int, 𝜙                         Γ, Σ, Π, Ψ ⊢ 𝑙 : long, 𝜙

                                                                                                  Σ 𝑙 = 𝜏★
                           TCONSB                                            TLOC
                                            Γ, Σ, Π, Ψ ⊢ 𝑏 : bool, 𝜙                     Γ, Σ, Π, Ψ ⊢ (𝑙, 𝑜 ) : 𝜏 ★, 𝜙

                   Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏𝑏 , 𝜂        isBasic 𝜏b                        Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏𝑒 ∗, 𝜂       𝜏𝑒 ∗ ≠ option( ∗)
          TREF                                                        TDEREF
                  Γ, Σ, Π, Ψ ⊢ ref (𝑒 ) : 𝜏𝑏 ★, (alloc :: 𝜂 )                                Γ, Σ, Π, Ψ ⊢!𝑒 : 𝜏𝑒 , (read :: 𝜂 )

                                      Γ, Σ, Π, Ψ ⊢ 𝑒 1 : 𝜏1 ∗, 𝜂 1      𝜏1 ∗ ≠ option( ∗)         Γ, Σ, Π, Ψ ⊢ 𝑒 2 : 𝜏1 , 𝜂 2
                    TMASSGN
                                                     Γ, Σ, Π, Ψ ⊢ 𝑒 1 := 𝑒 2 : unit𝜏 , (𝜂 1 ∔ 𝜂 2 ∔ write)

                Γ, Σ, Π, Ψ ⊢ 𝑒 1 : 𝜏, 𝜂 1      Γ, Σ, Π, Ψ ⊢ 𝑒 2 : 𝜏, 𝜂 2    isPrim 𝜏                   Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂        isPrim 𝜏
        TBOP                                                                                 TUOP
                         Γ, Σ, Π, Ψ ⊢ bop(𝑜𝑝, 𝑒 1 , 𝑒 2 ) : 𝜏, 𝜂 1 ∔ 𝜂 2                                Γ, Σ, Π, Ψ ⊢ uop(𝑜𝑝, 𝑒 ) : 𝜏, 𝜂

                             Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂        Γ, Σ, Π, Ψ ⊢ 𝑒 1 : 𝜏 ′ , 𝜂 1   Γ, Σ, Π, Ψ ⊢ 𝑒 2 : 𝜏 ′ , 𝜂 2    isBool 𝜏
                TCOND
                                                  Γ, Σ, Π, Ψ ⊢ if 𝑒 then 𝑒 1 else 𝑒 2 : 𝜏,′ 𝜂 ∔ 𝜂 1 ∔ 𝜂 2

                                             Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏𝑒 , 𝜂            Γ, Σ, Π, Ψ ⊩ 𝑒 : 𝜏, 𝜂 ′
                           (if isExt e then (Ψ(𝑒 ) = 𝜏 𝑓 𝜏𝑒 = 𝜏 𝑓               𝜏𝑒 = 𝜏 →𝜂𝑒 𝜏𝑟 ) else 𝜏𝑒 = 𝜏 →𝜂𝑒 𝜏𝑟
                  TAPP
                                                        Γ, Σ, Π, Ψ ⊢ 𝑒 (𝑒 ) : 𝜏𝑟 , 𝜂 ∔ 𝜂 ′ ∔ 𝜂𝑒

                                            Γ, Σ, Π, Ψ ⊢ 𝑒 1 : 𝜏, 𝜂 1      (𝑥 → 𝜏, Γ), Σ, Π, Ψ ⊢ 𝑒 2 : 𝜏2 , 𝜂 2
                               TBIND
                                                    Γ, Σ, Π, Ψ ⊢ let 𝑥 : 𝜏 = 𝑒 1 in 𝑒 2 : 𝜏2 , 𝜂 1 ∔ 𝜂 2

                         Γ 𝑥 = struct 𝑖𝑑 ∗          Π 𝑖𝑑 = 𝑐𝑜      fields𝜏 (𝑐𝑜 ) = 𝜏𝑠        Γ, Σ, Π, Ψ ⊩ 𝑒 : 𝜏𝑠′ , 𝜂𝑠      𝜏𝑠 = 𝜏𝑠′
             TSINIT
                                                        Γ, Σ, Π, Ψ ⊢ 𝑥 | (𝑓 , 𝑒 ) : struct 𝑖𝑑 ∗, 𝜂𝑠

                           Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂       𝜏 = struct 𝑖𝑑 ∗ ∨struct 𝑖𝑑            Π 𝑖𝑑 = 𝑐𝑜        field𝜏 (𝑐𝑜, 𝑓 ) = 𝜏 𝑓
               TFIELD
                                                                 Γ, Σ, Π, Ψ ⊢ 𝑒.𝑓 : 𝜏 𝑓 , 𝜂

                 Γ, Σ, Π, Ψ ⊢ 𝑒 1 : 𝜏1 , 𝜂 1     Γ, Σ, Π, Ψ ⊢ 𝑒 2 : 𝜏2 , 𝜂 2 Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 𝜏1 = 𝜏2               𝜏1 ∈ {int, long}
                                                 fvar(𝑒 ) ∩ fvar(𝑒 1 ) = 𝜙 fvar(𝑒 ) ∩ fvar(𝑒 2 ) = 𝜙
         TFOR
                                                 Γ, Σ, Π, Ψ ⊢ for (𝑒 1 . . . 𝑒 2 , 𝑑 ) 𝑒 : 𝜏, 𝜂 1 ∔ 𝜂 2 ∔ 𝜂

                                                   Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂      Γ, Σ, Π, Ψ ⊩ 𝑒𝑠 : 𝜏𝑠 , 𝜂 ′
                                       TSEQ
                                                         Γ, Σ, Π, Ψ ⊩ 𝑒 :: 𝑒𝑠 : 𝜏 :: 𝜏𝑠 , 𝜂 ∔ 𝜂 ′



                                               Fig. 10. Typing rules for expressions.


isExt and the lookup in Ψ are typically resolved during elaboration or typechecking, we make them
explicit in the rule to clarify how external calls are integrated into the type system. For example,
in the BeePL function fun foo() : int, <alloc,read> { let x : int* = ref(2) in let r : int = !x + 1 in r;} the
function’s effect captures both the allocation from ref(2) and the read from dereferencing x.
    The rule TMASSGN defines the typing rule for memory assignment expressions of the form
𝑒 1 := 𝑒 2 . It ensures that 𝑒 1 is of a pointer type, which may originate either from within the BeePL
program via the ref operator or from external sources, such as pointers returned by eBPF helper
functions. fun bar() : int, <alloc,read,write,read> { let x : int* = ref(2) in let _ : _ in x := !x + 1 in !x;}.
The effect annotation associated with the function bar captures the effects produced by its body,
which includes the use of ref, dereferencing (!), and memory assignment (:=). The rule enforces
that the memory assignment expression has the unit type as its result, reflecting that the purpose
of the expression is to produce a side effect rather than a value.

                                                                                         , Vol. 1, No. 1, Article . Publication date: July 2026.
12


                                                                                        Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏∗, 𝜂
               TNONE                                                TSOME
                          Γ, Σ, Π, Ψ ⊢ None : option(𝜏∗), 𝜙                    Γ, Σ, Π, Ψ ⊢ Some 𝑒 : option(𝜏∗), 𝜂

                              Γ, Σ, Π, Ψ ⊢ 𝑚 : option(𝜏𝑚 ∗), 𝜂𝑚      𝑝, 𝑒 = { (Pnone, 𝑒 1 ), (Psome x, 𝑒 2 ), . . .}
                                           (𝑥 → 𝜏𝑚 ∗, Γ), Σ, Π, Ψ ⊩ 𝑒 : 𝜏𝑠 , 𝜂𝑠 ∀𝜏1 , 𝜏2 ∈ 𝜏𝑠 , 𝜏1 = 𝜏2
              TMATCHO
                                                 Γ, Σ, Π, Ψ ⊢ match 𝑚 with 𝑝 → 𝑒 : 𝜏, 𝜂𝑚 ∔ 𝜂𝑠

                                      Γ, Σ, Π, Ψ ⊢ 𝑚 : bytes, 𝜂𝑚 𝑝, 𝑒 = { ( (𝑥, 𝜏𝑥 ) : (𝑦, 𝜏 𝑦 ), 𝑒 1 ), . . .}
                                      (𝑥 → 𝜏𝑥 , 𝑦 → 𝜏 𝑦 , Γ), Σ, Π, Ψ ⊩ 𝑒 : 𝜏𝑠 , 𝜂𝑠 ∃𝜏𝑟 : ∀𝜏 ∈ 𝜏𝑠 , 𝜏𝑟 = 𝜏
                       TMATCHB
                                                Γ, Σ, Π, Ψ ⊢ match 𝑚 with 𝑝 → 𝑒 : 𝜏𝑟 , 𝜂𝑚 ∔ 𝜂𝑠


                                     Fig. 11. Typing rules for additional expressions.


   The typing rules for unary and binary operators (TUOP and TBOP) are straightforward. They
accumulate the effects produced during the evaluation of their operands and ensure that these
operations are performed only on primitive data types. In BeePL, pointer arithmetic is disallowed, so
such operators cannot be applied to pointer types. The typing rules for conditional and let-bindings
are also pretty straightforward. Type checking of struct initialization (TSINIT) ensures that all
fields are initialized with values matching their declared types and appear in the correct order as
defined in the struct environment Π (ensured by the function fields𝜏 ). For field access (TFIELD),
the type checker looks up the struct type in Π to verify that the accessed field exists and returns
the corresponding field’s type.
   The type checking rule TFOR for the for loop in BeePL ensures that the loop always terminates by
enforcing strict control over its structure and dependencies. The loop has the form for (𝑒 1 . . . 𝑒 2, 𝑑) 𝑒,
where 𝑒 1 and 𝑒 2 represent the lower and upper bounds, 𝑑 is the fixed direction (up or down), and 𝑒 is
the loop body. The typing rule requires that 𝑒 1 and 𝑒 2 are integer/long expressions, and that the loop
body 𝑒 does not reference any variables used in 𝑒 1 or 𝑒 2 . This is enforced by checking that the set of
free variables in the body is disjoint from those in the bounds. As a result, the number of iterations
is fixed and independent of the loop body, ensuring that the loop cannot introduce unbounded
behavior. Consider the following code snippet: fun loop() : int, <alloc,read,write,read> { let x : int
* = ref(2) in let _ = for(1 ... 5, Up) {x := !x + 1} in !x;}. The typing rule for the for loop captures the
effect of the loop body—for example, <read, write, read> for the expression like x := !x + 1—and also
tracks the free variables and constants involved (such as x, 1, and 5). This information is used to
ensure that the loop bounds remain independent of the body, allowing the type system to statically
guarantee the absence of the divergence effect. We conservatively include the per-iteration effect of
the loop body once in the overall effect. This ensures soundness without requiring static knowledge
of the number of iterations. Figure 11 presents additional typing rules emphasizing external calls
and match expressions. The typing rule for pattern matching on an option expression in BeePL
ensures that both the None and Some cases are handled explicitly and safely. Given an expression
𝑚 of type option 𝜏𝑚 ∗, the rule typechecks two branches: one for Pnone, which produces a result
of type 𝜏, and one for Psome 𝑥, where 𝑥 is bound to 𝜏𝑚 ∗, and the body is typechecked under this
binding to also yield type 𝜏. Both branches must return the same type, and the total effect includes
the effect of evaluating 𝑚 as well as those of both branches. This rule enforces that a potentially
null-like value must be explicitly unpacked before use, guaranteeing that no dereferencing occurs
unless the value is known to be present, thus eliminating null pointer dereference errors at the
type level.
   For example, the eBPF helper function bpf map lookup elem returns a pointer to a value as-
sociated with a key in the eBPF map, but this pointer may be NULL if the key is not found. To

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                                 13


model this uncertainty safely, BeePL wraps the return type of such functions in an option type.
The type system then enforces, through the match expression and the typing rule TMATCHO,
that any use of such a pointer must first explicitly pattern match on the result. This guaran-
tees that the Pnone case (corresponding to a null pointer) is handled before any dereferencing
can occur, ensuring memory safety through compile-time checks. Revisiting the typing rule for
function application, in the case of external function calls, BeePL uses the environment Ψ to
typecheck the call against the externally defined function signature. The environment Ψ maps
each external function to its type, including argument types, return type, and associated ef-
fects. For example, the signature of the helper function bpf map lookup elem is defined in Ψ as
(option(map∗), option(long∗)) →<read,io> option(long∗), indicating that it takes optional pointers
to a map (a pointer to a struct, which creates map in eBPF) and a key, may perform read and io
effects, and returns an optional pointer to a long integer. The io effect distinguishes operations that
involve interaction with the external environment, such as calls to external functions or system-
level resources. It allows the type system to clearly separate internal computation from externally
observable behavior. Similarly, the eBPF helper function bpf get current uid gid is assigned the
type () →<io> long in BeePL. This signature indicates that the function does not perform any
memory reads or writes, but it interacts with the external environment—such as querying kernel
state—which results in an io effect.
     The typing rule TMATCHB handles pattern matching on byte sequences when attempting to parse
structured data, such as C-style headers, from raw bytes. In a pattern of the form (𝑥, 𝜏𝑥 ) : (𝑦, 𝜏 𝑦 ),
the byte buffer m (e.g., a field like data in xdp md BPF structure, illustrated in the example present
in Figure 17) is being parsed into a structure of type 𝜏𝑥 (e.g.,eth), which is referred to by the variable
𝑥. The result of this parsing is a sequence of bindings represented by the list of fields y with types
𝜏 𝑦 , which correspond to the fields of the struct type 𝜏𝑥 . The rule first checks that 𝑚 has type bytes,
with effect 𝜂𝑚 . Then, each branch expression is typechecked in an extended typing context where
𝑥 is bound to the struct type 𝜏𝑥 and the individual field bindings in 𝑦 : 𝜏 𝑦 are available. All branch
expressions must return the same result type 𝜏𝑟 , and their effects are combined into 𝜂𝑠 . This rule
ensures that parsing raw bytes into a structured type is only allowed when it is type-safe, and that
all resulting fields are well-typed and locally available for use in the corresponding match branch.

                     𝑥 : 𝜏, 𝑦 : 𝜏, Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 ∧ rt = 𝜏 ∧ ef = 𝜂 ∧ ¬(𝜏∗) ∧ ∀𝑥 ∈ 𝑥 . section ok(𝜏, s)
           TFDECL
                     Γ, Σ, Π, Ψ ⊢ {sec : s; rt : 𝜏; ef : 𝜂; cc : conv; args : 𝑥, 𝜏; vars : 𝑦, 𝜏; body : 𝑒; flag : bool}

                           typeof (𝑣) = 𝜏 ∧ section ok(𝜏, s)                      𝑝 = id, decl ∧ ∀𝑑 ∈ decl. ⊢ 𝑑
              TGDECL                                                   TPROG
                         Γ, Σ, Π, Ψ ⊢ {gvar : (𝑥 : 𝜏, 𝑣); sec : 𝑠 }                        Γ, Σ, Π, Ψ ⊢ 𝑝


                                      Fig. 12. Typing rules for BeePL program.


   Figure 12 defines the typing rules for BeePL programs. It enforces that function declarations
must return non-pointer types—preventing functions from returning addresses—and ensures that
each argument’s type is compatible with the declared section attribute through the section ok
predicate. The typing environment Γ initially starts empty and is extended with function arguments
and local variables when checking the function body. The environment Ψ contains the signatures
of external functions, while Σ and Π track the store and global contexts, respectively. The predicate
section ok(𝜏, s) ensures that the type of a function argument is compatible with the section attribute
of the function. If no section is specified (s = None), no constraint is enforced. Otherwise, the
predicate checks that specific argument types (e.g., struct xdp md, struct sk buff) are only used

                                                                            , Vol. 1, No. 1, Article . Publication date: July 2026.
14


in functions annotated with the corresponding section (e.g., "xdp", "socket"). For all other types or
sections, the predicate defaults to allowing the combination.

3.2    Operational Semantics
The small-step operational semantics of expressions are defined over a state ≺ Δ, Ω, Θ ≻, where
Δ denotes global environment, comprising function definitions, global variable declarations, and
struct type definitions, Ω is the variable environment, mapping local variables to memory locations
and their respective types: (Ω := [𝑥 1 → (𝑙 1, 𝜏1 ), ..., 𝑥𝑛 → (𝑙𝑛 , 𝜏𝑛 )]), and Θ represents the memory
mapping from locations to values(Θ := [𝑙 1 → 𝑣 1, ..., 𝑙𝑛 → 𝑣𝑛 ]). BeePL uses the memory model of
CompCert [8]. We assume that dom(Ω) ∩ dom(Δ) = Φ, indicating that the domains of Ω and Δ are
disjoint—that is, no variable name appears in both the local environment and the global environment.
Access to environments is expressed using the notation [ ], where the outer component refers to
the environment or store, and the inner component denotes the key being looked up. Updates to
environments are denoted using the notation [ → ], which represents a mapping from a key to
a new value. New allocations in the environment are represented using the notation [| → |],
which depends on the type of the variable being allocated. Type information is crucial for reserving
the correct amount of memory. While types are omitted in the rules for clarity of presentation, they
are fully taken into account in the actual implementation. Each component of the program state is
accessed using a projection notation. For instance, 𝑠 Θ denotes the memory component of the state 𝑠.
This operational model supports effectful computation while preserving a clear separation between
name binding, memory layout, and program behavior, facilitating both reasoning and formal
verification. The operational semantics of the language is present in Figure 13. The evaluation of
a local or global variable in the state ≺ Δ, Ω, Θ ≻ proceeds by first resolving the variable 𝑥 to its
corresponding location 𝑙 in Ω (for local variables) or Δ (for global variables), and then dereferencing
𝑙 in memory Θ to obtain the associated value. Rule REFV and REF define the operational semantic
of ref construct. The construct ref in BeePL explicitly allocates a value to memory and returns the
new location. The programmers are not intended to write expressions involving explicit, concrete
locations: such expression will arise only as intermediate results during the operational semantics.
This ensures that all pointers originate from well-defined allocation sites within the program,
making them tractable and easier to reason about. Unlike C, where the address of any variable
can be taken arbitrarily, BeePL guarantees that every address corresponds to memory that has
been explicitly allocated. Similarly, the rules DEREF and DEREFV define the operational semantics
of the dereference construct !. They evaluate a pointer by locating the address 𝑙 with offset 𝑜 in
the memory Θ, and produce the value stored at that specific location. The memory assignment
construct 𝑒 1 := 𝑒 2 updates the value stored in the memory location pointed out by 𝑒 1 with the result
of the evaluation 𝑒 2 . Unlike let-binding, which introduces an immutable binding and does not alter
memory, := performs a side-effecting update, modifying the program state.
   Let-binding introduces an immutable variable bound to the result of evaluating an expression,
without performing memory updates—it simply extends the environment. Unlike :=, it is purely
functional and side-effect free. In let 𝑥 : 𝜏 = 𝑒 1 in 𝑒 2 , the result of 𝑒 1 is bound to 𝑥 in 𝑒 2 . Unary
and binary operators follow standard evaluation rules, but BeePL handles operations like division,
modulo, and shifts explicitly to avoid undefined behavior common in C. Division and modulo
return zero on division-by-zero or overflow; shift operations also return zero when exceeding
bit-width or on overflow. This ensures deterministic semantics. The rule BOPV uses an auxiliary
function unsafe to detect such cases based on the operator, operand values, and signedness. Struct
initialization (STRUCTV) allocates memory and assigns values to fields according to the struct
layout. Field access retrieves the value at the correct offset, determined using type information
from the global environment, even if types are not shown explicitly in the rule.

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                                                                                 15


                                  𝑠 Ω [𝑥 ] = 𝑙, 𝜏𝑥 ∧ 𝑠 Θ [𝑙 ] = 𝑣                              𝑥 ∉ 𝑑𝑜𝑚 (𝑠 Ω ) ∧ 𝑠 Δ [𝑥 ] = 𝑙 ∧ 𝑠 Θ [𝑥 ] = 𝑣
                       LVAR                                                          GVAR
                                            𝑠, 𝑥 → 𝑠, 𝑣                                                                   𝑠, 𝑥 → 𝑠, 𝑣
                                               ′      ′                                                   ′
                                   𝑠, 𝑒 → 𝑠 , 𝑒                                      fresh(𝑙 ) ∧ Θ = 𝑠 Θ [𝑙 → 𝑣 ] ∧ Σ[𝑙 → ∗typeof (𝑣) ]
                    REF                                                  REFV
                            𝑠, ref (𝑒 ) → 𝑠 ′ , ref (𝑒 ′ )                                            𝑠, ref (𝑣) →≺ 𝑠 Δ , Ω, Θ′ ≻, 𝑙

                                                                  𝑠, 𝑒 → 𝑠 ′ , 𝑒 ′                                  Θ[ (𝑙, o) ] = 𝑣
                                             DREF                            ′       ′
                                                                                               DREFV
                                                               𝑠, !(𝑒 ) → 𝑠 , !(𝑒 )                                𝑠, !(𝑙, o) → 𝑠, 𝑣

                𝑠, 𝑒 1 → 𝑠 , 𝑒 1′ ′                                                               ′
                                                                                         𝑠, 𝑒 → 𝑠 , 𝑒     ′
                                                                                                                                                           Θ′ = Θ[𝑙 → 𝑣 ]
MASSGN1                                                       MASSGN2                                                       MASSGNV
        𝑠, 𝑒 1 := 𝑒 2 → 𝑠 ′ , 𝑒 1′ := 𝑒 2                                                         ′
                                                                                 𝑠, 𝑙 := 𝑒 → 𝑠 , 𝑙 := 𝑒            ′
                                                                                                                                              𝑠, 𝑙 := 𝑣 →≺ 𝑠 Δ , 𝑠 Ω , Θ′ ≻, unit

                                                    𝑠, 𝑒 1 → 𝑠 ′ , 𝑒 1′                                                          𝑒 2 [𝑥 ← 𝑣 ] = 𝑒 2′
                   LET                                                                                        LETV
                          𝑠, let 𝑥 : 𝜏 = 𝑒 1 in 𝑒 2 → 𝑠 ′ , let 𝑥 : 𝜏 = 𝑒 1′ in 𝑒 2                                      𝑠, let 𝑥 : 𝜏 = 𝑣 in 𝑒 2 → 𝑠, 𝑒 2′

                  𝑠, 𝑒 → 𝑠 ′ , 𝑒 ′                                         uopsem (𝑜𝑝, 𝑣) = 𝑣 ′                                                     𝑠, 𝑒 1 → 𝑠 ′ , 𝑒 1′
UOP                           ′                ′
                                                               UOPV                                   ′        ′
                                                                                                                        BOP1
       𝑠, uop(𝑜𝑝, 𝑒 ) → 𝑠 , uop(𝑜𝑝, 𝑒 )                                   𝑠, uop(𝑜𝑝, 𝑣) → 𝑠 , 𝑣                                   𝑠, bop(𝑜𝑝, 𝑒 1 , 𝑒 2 ) → 𝑠 ′ , bop(𝑜𝑝, 𝑒 1′ , 𝑒 2 )

                             𝑠, 𝑒 2 → 𝑠 ′ , 𝑒 2′                                            𝑣 = if unsafe(𝑜𝑝, 𝑣1 , 𝑣2 , 𝑠 ) then 0 else bopsem (𝑜𝑝, 𝑣1 , 𝑣2 )
   BOP2                                                                          BOPV
            𝑠, bop(𝑜𝑝, 𝑣1 , 𝑒 2 ) → 𝑠 ′ , bop(𝑜𝑝, 𝑣1 , 𝑒 2′ )                                                            𝑠, bop(𝑜𝑝, 𝑣1 , 𝑣2 ) → 𝑠 ′ , 𝑣

                                                   𝑠, 𝑒 1 → 𝑠 ′ , 𝑒 1′
            COND                                                                                              CONDT
                       𝑠, if 𝑒 1 then 𝑒 2 else 𝑒 3 → 𝑠 ′ , if 𝑒 1′ then 𝑒 2 else 𝑒 3                                          𝑠, if true then 𝑒 2 else 𝑒 3 → 𝑠, 𝑒 2

                                                                                                                           ∀ 𝑒 ∈ 𝑒 : 𝑠, 𝑒 → 𝑠 ′ , 𝑒 ′
                      CONDF                                                                    STRUCT
                                      𝑠, if false then 𝑒 2 else 𝑒 3 → 𝑠, 𝑒 3                                           𝑠, 𝑥 | (𝜏, 𝑓 )𝑒 → 𝑠 ′ , 𝑥 | (𝜏, 𝑓 )𝑒 ′

                     𝜏 = struct 𝑠𝑖𝑑 ∧ ∗Δ[𝑠𝑖𝑑 ] = 𝑐𝑜 ∧ ∀ 𝑓 ∈ 𝑓 , fieldofs (Δ, 𝑓 , 𝑐𝑜 ) = [𝑜 1 , . . . , 𝑜𝑛 ] ∧ Ω[ |𝑥 → (𝑙, 𝑜 ) | ] = Ω ′
                                        ∧ Θ[ 𝑓1 , (𝑙 + 𝑜 + 𝑜 1 ) → 𝑣1 , . . . , 𝑓𝑛 , (𝑙 + 𝑜 + 𝑜𝑛 ) → 𝑣𝑛 ] = Θ′
      STRUCTV
                                                                          𝑠, 𝑥 | (𝑓 , 𝑣) →≺ 𝑠 Δ , Ω ′ , Θ′ ≻, (𝑙, 𝑜 )

                                  𝑠, 𝑒 → 𝑠 ′ , 𝑒 ′                                       𝜏 = struct id ∧ Δ[𝑖𝑑 ] = 𝑐𝑜 ∧ fieldofs (Δ, 𝑓 , 𝑐𝑜 ) = 𝑜 ′
               FACCESS                                             FACCESSV
                               𝑠, 𝑒.𝑓 → 𝑠 ′ , 𝑒.′ 𝑓                                                            𝑠, (𝑙, 𝑜 ).𝑓 → 𝑠, (𝑙, 𝑜 + 𝑜 ′ )

                                       𝑠, 𝑒 1 → 𝑠 ′ , 𝑒 1′                                                                           𝑠, 𝑒 2 → 𝑠 ′ , 𝑒 2′
        FOR1                                                                                  FOR2
                 𝑠, for (𝑒 1 . . . 𝑒 2 , 𝑑 ) 𝑒 → 𝑠 , for (𝑒 1′ . . . 𝑒 2 , 𝑑 ) 𝑒
                                                          ′
                                                                                                              𝑠, for (𝑣1 . . . 𝑒 2 , 𝑑 ) 𝑒 → 𝑠 ′ , for (𝑣1 . . . 𝑒 2′ , 𝑑 ) 𝑒

           range(𝑣1, 𝑣2, 𝑑 ) = 𝑛 ∧ 𝑠, (𝑒, . . . , 𝑒 )𝑛 = 𝑠 ′ , 𝑣                                       𝑠, 𝑒 1 → 𝑠 ′ , 𝑒 1′                             ∀𝑒 ∈ 𝑒, 𝑠, 𝑒 → 𝑠 ′ , 𝑒 ′
   FORV                                                                              APP1                                                  APP2
                     𝑠, for (𝑣1 . . . 𝑣2 , 𝑑 ) 𝑒 → 𝑠 ′ , 𝑣                                     𝑠, 𝑒 1 (𝑒 2 ) → 𝑠 ′ , 𝑒 1′ (𝑒 2 )                     𝑠, 𝑓 𝑛 (𝑒 ) → 𝑠 ′ , 𝑓 𝑛 (𝑒 ′ )

                         Δ[ 𝑓 𝑛] = 𝑓 𝑑 ∧ 𝑓 𝑑 = {sec := 𝑠𝑎; rt := 𝜏; ef := 𝜂; args := 𝑎𝑠; vars := 𝑣𝑠; body := 𝑒; flag := 𝑏 }
                                         ∧ 𝑎𝑠 ∩ 𝑣𝑠 = 𝜙 ∧ Ω[ |𝑙𝑠 ← 𝑎𝑠, 𝑙𝑠 ′ ← 𝑣𝑠 | ] = Ω ′ ∧ Θ[𝑙𝑠 → 𝑣 ]
               APP3
                                                                          𝑠, 𝑓 𝑛 (𝑣) →≺ 𝑠 Δ , Ω ′ , Θ′ ≻, 𝑒

                              Δ[ 𝑓 𝑛] = 𝑓 𝑑 ∧ 𝑓 𝑑 = {argtype := 𝜏; argtype := 𝜏𝑟 ; ef := 𝜂; cc := 𝑐𝑐 } ∧ 𝑓 𝑛 (𝑣) = 𝑣 ′ , 𝑠 ′
                    EAPP
                                                                                   𝑠, 𝑓 𝑛 (𝑣) → 𝑠 ′ , 𝑣 ′



                                                              Fig. 13. Semantics for expressions.



  The operational semantics of the for loop in the form for (𝑒 1 . . . 𝑒 2, 𝑑) 𝑒 define a bounded iteration
over a range of values determined by the evaluated results of 𝑒 1 , 𝑒 2 , and the direction 𝑑 (which
can be either increasing or decreasing). Both 𝑒 1 and 𝑒 2 are evaluated exactly once before the loop
begins and remain unchanged throughout the execution of the loop body 𝑒. This design guarantees

                                                                                                              , Vol. 1, No. 1, Article . Publication date: July 2026.
16


termination, as the number of iterations is fixed and entirely determined by the initial bounds. By
ensuring the immutability of the range and preventing the loop body from influencing the control
flow, the construct avoids common issues such as unintended infinite loops or mutation-induced
errors—offering a safer and more analyzable alternative to traditional C-style loops. The translation
of BeePL for-loop to C for-loop is discussed in Section 7. The operational semantics of function
application and external call is pretty straightforward.



                                                               𝑠, 𝑒 → 𝑠,′ 𝑒 ′
          NONE                                SOME                                        SOMEV
                   𝑠, None → 𝑠, None                   𝑠, Some 𝑒 → 𝑠,′ Some 𝑒 ′                      𝑠, Some 𝑣 → 𝑠, Some 𝑣
                                                                                ′ ′
                                                                    𝑠, 𝑒 → 𝑠, 𝑒
                                MATCH1
                                             𝑠, match 𝑒 with 𝑝 → 𝑒 → 𝑠,′ match 𝑒 ′ with 𝑝 → 𝑒

             isSome 𝑣 ∧ 𝑝, 𝑒 = { (Pnone, 𝑒 1 ), (Psome x, 𝑒 2 ), . . .}                   𝑝, 𝑒 = { (Pnone, 𝑒 1 ), (Psome 𝑥, 𝑒 2 ), . . .}
 MSOME                                                                          MNONE
                    𝑠, match 𝑣 with 𝑝 → 𝑒 → 𝑠, 𝑒 2 [𝑥 ← 𝑣 ]                                  𝑠, match None with 𝑝 → 𝑒 → 𝑠, 𝑒 1

                   typeof (𝑣) = bytes ∧ 𝑝, 𝑒 = { ( (𝑥, 𝜏𝑥 ) : (𝑦, 𝜏 𝑦 ), 𝑒 1 ), (𝑝 2 , 𝑒 2 ), . . .} ∧ length(𝑣) ≥ sizeof (𝜏𝑥 ) ∧
                                         extract(𝑣, 𝜏𝑥 ) = (𝑣𝑥 , {𝑦1 ↦→ 𝑣1 , . . . , 𝑦𝑛 ↦→ 𝑣𝑛 } )
       MBYTES
                                             𝑠, match 𝑣 with 𝑝 → 𝑒 → 𝑠 ′ , 𝑒 1 [𝑦𝑖 ↦→ 𝑣𝑖 , 𝑥 ↦→ 𝑣𝑥 ]

                       typeof (v) = bytes ∧ 𝑝, 𝑒 = { ( (𝑥, 𝜏 ) : (𝑦, 𝜏 ), 𝑒 1 ), (𝑝 2 , 𝑒 2 ), . . .} ∧ length(𝑣) < 𝑠𝑖𝑧𝑒𝑜 𝑓 (𝜏𝑥 )
         MBYTESF
                                                          𝑠, match 𝑣 with 𝑝 → 𝑒 → 𝑠, 𝑒 2

                                                           𝑠, 𝑒 → 𝑠,′ 𝑒 ′                             𝑠, 𝑒𝑠 ↣ 𝑠,′ 𝑒𝑠 ′
         EMPTY                           SEQH                        ′      ′
                                                                                       SEQT
                   𝑠, [::] ↣ 𝑠, [::]               𝑠, (𝑒 :: 𝑒𝑠 ) ↣ 𝑠, (𝑒 :: 𝑒𝑠 )                𝑠, (𝑣 :: 𝑒𝑠 ) ↣ 𝑠,′ (𝑣 :: 𝑒𝑠 )


                                       Fig. 14. Semantics for additional expressions.



   Figure 14 presents the additional operational semantics for pattern matching in BeePL. BeePL
supports three kinds of patterns, each serving a distinct purpose. Patterns over option types, such
as Pnone and Psome 𝑥, ensure that programmers explicitly handle cases where the evaluation of an
expression 𝑒 results in either None or Some. In the case of None, the semantics proceed with the
expression corresponding to the Pnone branch, closely resembling the handling of null pointers in C.
In the case of Some 𝑥, the value is extracted and execution continues with the expression associated
with the Psome branch. The MBYTES rule defines how BeePL evaluates pattern matching over byte
buffers. It checks that the value being matched is of type bytes and that the buffer is large enough
to hold a value of the target type 𝜏𝑥 . The pattern (𝑥, 𝜏𝑥 ) : (𝑦, 𝜏 𝑦 ) attempts to parse the byte buffer
into a value 𝑣 𝑥 of type 𝜏𝑥 , binding it to 𝑥. If 𝜏𝑥 is a struct, its individual fields are also extracted and
bound to variables 𝑦. The match succeeds if extraction is successful, and the body expression 𝑒 1 is
evaluated with all these bindings substituted in. This rule handles both flat and structured types
uniformly, ensuring that byte parsing is size-checked and safe before access. This form of pattern
matching enforces memory bounds checks directly from type information and safe-semantics
conditions, avoiding any reliance on low-level pointer arithmetic. The corresponding translation to
C is provided in Section 7. The EMPTY rule states that evaluating an empty sequence returns an
empty sequence without modifying the state. The SEQH rule evaluates the head of a non-empty
sequence if it is not yet a value, while the SEQT rule allows evaluation to proceed to the tail only
after the head has evaluated to a value.

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                                      17


4     Formally Verified Type System and the Compiler
This section presents the core formal foundations of BeePL, focusing on its type system and verified
compilation strategy. We first describe the type system that enforces key safety properties expected
by the eBPF runtime, such as memory safety, control-flow integrity, and termination. We then
provide formal proofs that well-typed BeePL programs satisfy a set of eBPF properties at the source
level. Finally, we describe the compilation process that translates BeePL programs to BPF bytecode
while preserving the functional correctness.

4.1     Formally Verified Type System
We start by proving some key properties related to the soundness of the type system. The BeePL
type system is sound: any program that typechecks is guaranteed to never reach a stuck state. That
is, every well-typed expression either evaluates to a value or can take a valid step in the operational
semantics.
   A well-typed BeePL program never reaches a stuck state: This property follows from the progress
lemma 19, which ensures that every well-typed expression is either a value or can take a reduction
step. Combined with preservation, this guarantees that the program maintains type correctness
throughout execution, ruling out runtime type errors.
   Since our operational semantics and typing rules involve various entities like local store, global
store, and memory, we need a definition about well-formedness of the state. A well-formed state is
defined as follow:
    Definition 4.1 (Well Formed State). A state 𝑠 is well-formed, written as well formed state, if:
                                                𝑥 ∈ 𝑑𝑜𝑚 (𝑠 Ω )
                                                                    ∃𝑙, 𝑣, 𝑜. 𝑠 Ω [𝑥 ] = (𝑙, 𝜏 ) ∧ Σ 𝑙 = 𝜏 ∧ 𝑠 Θ [𝑙, 𝑜 ] = 𝑣
            ∀𝑥, 𝜏 . Γ 𝑥 = Some 𝜏
          
                                                
          
          
          
          
                                                𝑥 ∉ 𝑑𝑜𝑚 (𝑠 Ω ) ∃𝑙, 𝑜, 𝑣. 𝑠 Δ [𝑥 ] = 𝑙 ∧ Σ 𝑙 = 𝜏 ∧ 𝑠 Θ [𝑙, 𝑜 ] = 𝑣
          
                                                
            ∀𝑥, 𝜏 . Σ 𝑥 = 𝜏
          
          
          
                                                isValidAccess(Θ, 𝑥, Freeable)
          
          
                                                 ∀𝜏 . Σ 𝑥 = 𝜏
          
           ∀𝑥 . isValidAccess(Θ, 𝑥, Freeable)
          
 ∀Γ, Σ, 𝑠
          
           ∀Π, Ψ.
          
                                                ∀𝑙, 𝜂, 𝜏𝑎 , 𝜂 ′ , 𝜏𝑟 , 𝜏𝑠 . Γ, Σ, Π, Ψ ⊢ 𝑙 : 𝜂, 𝜏𝑎 →𝜂 𝜏𝑟 ∧ Γ, Σ, Π, Ψ ⊩ 𝑒𝑠 : 𝜏𝑠 , 𝜂 ′
          
          
          
          
          
                                                ∃𝑓 . 𝑠 Δ [𝑙 ] = 𝑓 ∧ 𝑓 .(args) ∩ 𝑓 .(vars) = 𝜙 ∧ |args| = |𝑒𝑠 |
          
          
          
          
                                                ∧𝜏𝑠 = typeof (𝑓 .args) ∧ 𝜏𝑟 = 𝑓 .(rt)
          
          
           ∀Π.                                  ∀𝑥, 𝑖𝑑. Γ 𝑥 = struct 𝑖𝑑 ∗ ∧∃𝑐𝑜. Π 𝑖𝑑 = Some 𝑐𝑜
          
          

  The predicate well formed state characterizes when a memory store is consistent with a typing
context Γ and store typing environment Σ. It ensures that:
    • local variables in Γ point to valid locations in Ω, with well defined types in Σ;
    • global variables are absent from Ω but mapped in Δ with well defined types in Σ;
    • each location typed in Σ is accessible in Θ with Freeable permission, and all such accessible
      locations are well-typed;
    • functions in Δ match their type signatures and avoid variable name clashes;
    • struct variables must be declared in Π.
This invariant underpins type soundness: it guarantees progress by ruling out stuck states from
invalid memory access, and preservation by maintaining type consistency across evaluation steps.
   All lemmas are also established for lists of expressions; however, their statements are omitted
for brevity. The complete proofs are provided in Appendix.
  Progress. The progress lemma presents the progress property for BeePL’s expressions and ex-
pression sequences. It asserts that any well-typed expression or sequence of expressions is either a

                                                                             , Vol. 1, No. 1, Article . Publication date: July 2026.
18


value or can take a computational step, ensuring that well-typed programs do not get stuck during
execution.
     Lemma 1. [Progress]
                  ∀Γ, Σ, Π, Ψ, 𝑒, 𝜂, 𝜏, 𝑠.       Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠) =⇒
                                                 isVal 𝑒 ∨ ∃𝑠 ′, 𝑒 ′ . 𝑠, 𝑒 → 𝑠 ′, 𝑒 ′ ∧ well formed state(Γ, Σ, 𝑠 ′ )

     The complete proof is provided in Appendix 19.
   Preservation. The preservation lemma ensures that if a well-typed expression takes a step, the
resulting expression remains well-typed with the same type and possibly fewer effects. BeePL
infers effects conservatively—for example, if 𝑏 then ∗ 𝑝 else 0 may carry a read effect even if 𝑝 is
never dereferenced at runtime. Thus, preservation permits the resulting effects to be a subset of
the original.
     Lemma 2. [Preservation]
        ∀Γ, Σ, Π, Ψ, 𝑒, 𝑒 ′, 𝜂, 𝜏, 𝑠, 𝑠 ′ .   Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠) ∧ 𝑠, 𝑒 → 𝑠 ′, 𝑒 ′ =⇒
                                              ∃𝜂 ′ . Γ, Σ, Π, Ψ ⊢ 𝑒 ′ : 𝜏, 𝜂 ′ ∧ 𝜂 ′ ⊆ 𝜂 ∧ well formed state(Γ, Σ, 𝑠 ′ )

   The complete proof is provided in Appendix 20.
   To prove soundness we define a semantic closure for BeePL program defined in Figure 16 (present
in appendix). The soundness lemma states that if an expression (or sequence) is well-typed and the
state is well-formed, then its evaluation to a final expression (or sequence) must result in a value.

     Lemma 3 (Soundness).
         ∀Γ, Σ, Π, Ψ, 𝑒, 𝑒 ′, 𝑠, 𝑠 ′, 𝜂, 𝜏, 𝑛.    Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠)
                                                   ∧ 𝑠, 𝑒 ↠𝑛 𝑠 ′, 𝑒 ′ ∧ 𝑒 ′ ↛ =⇒ isVal 𝑒 ∧ ∃𝜂 ′ . Γ, Σ, Π, Ψ ⊢ 𝑒 ′ : 𝜏, 𝜂 ′
                                                   ∧ 𝜂 ′ ⊆ 𝜂 ∧ well formed state(Γ, Σ, 𝑠 ′ )

     The complete proof is provided in Appendix 21.

4.2     eBPF properties
In this section, we present formal proofs demonstrating how each of the aforementioned eBPF
safety properties defined in Section 2.1 is enforced by our framework.
   Lemma 4 ensures that any well-typed BeePL expression or list of expressions evaluates to a value
in finitely many steps if the initial state is well-formed. It also guarantees that the divergence effect
is not inferred, capturing both runtime termination and its sound reflection in the effect system.
     Lemma 4. [Termination]
                 ∀Γ, Σ, Π, Ψ, 𝑒𝑠, 𝜂𝑠 , 𝜏𝑠 , 𝑠.      Γ, Σ, Π, Ψ ⊩ 𝑒𝑠 : 𝜏𝑠 , 𝜂𝑠 ∧ well formed state(Γ, Σ, 𝑠) =⇒
                                                   ∃𝑛, 𝑠 ′, 𝑣𝑠. 𝑠, 𝑒𝑠 ⇝𝑛 𝑠 ′, 𝑣𝑠 ∧ isVal 𝑣𝑠 ∧ divergence ∉ 𝜂𝑠
                  ∧ ∀Γ, Σ, Π, Ψ, 𝑒, 𝜂, 𝜏, 𝑠.        Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠)
                                                   ∃𝑛, 𝑠 ′, 𝑣. 𝑠, 𝑒 ↠𝑛 𝑠 ′, 𝑣 ∧ isVal 𝑣 ∧ divergence ∉ 𝜂

   Proof. We proceed by mutual induction on the structure of the typing derivation for both
expressions and expression sequences. Below, we present the proof for the case of a single expression.
The case for a sequence of expressions follows similarly, by applying the induction hypothesis
recursively at each step of the sequence. Induction on the structure of 𝑒 gives us different subgoals
for each expressions of BeePL. We discuss interesting cases here:
Var case. From the assumptions Γ, Σ, Π, Ψ ⊢ 𝑥 : 𝜏, 𝜙 and well formed state(Γ, Σ, 𝑠), we invoke the

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                       19


progress theorem to conclude that the variable 𝑥 evaluates to a value 𝑣 in one step, yielding a
resulting state 𝑠 ′ . That is, there exists 𝑛 = 1 such that 𝑠, 𝑥 ↠1 𝑠 ′, 𝑣. By applying the rule SMULTI, we
reduce the goal to proving 𝑠, 𝑥 → 𝑠 ′, 𝑣, which is discharged by the result of the progress theorem.
Since the evaluation yields a value and no further computation occurs, it terminates. Furthermore,
by applying the preservation theorem to the typing assumption Γ, Σ, Π, Ψ ⊢ 𝑥 : 𝜏, 𝜙, the well-
formedness of the state 𝑠, and the evaluation step 𝑠, 𝑥 → 𝑠 ′, 𝑣, we obtain that the resulting value 𝑣 is
well-typed with type 𝜏 and effect 𝜂 ′ , where 𝜂 ′ ⊆ 𝜙. This suffices to say that 𝜂 ′ = 𝜙, which trivially
excludes divergence.
   Constant and Values. The proof is trivial for these cases.
   Ref. We proceed by case analysis on the evaluation status of 𝑒 in ref 𝑒.

 • Case 1: For the case where 𝑒 is not a value, induction hypothesis guarantees that the evaluation
   of 𝑒 terminates. There exists a natural number 𝑛, a state 𝑠 ′ , and a value 𝑣 ′ such that: 𝑠, 𝑒 ↠𝑛
   𝑠 ′, 𝑣 ′ and divergence ∉ 𝜂 ′ . Typing rule TREF, justifies that the type of ref 𝑒 is 𝜏 ★ with effect
   alloc :: 𝜂 ′ . Since divergence ∉ 𝜂 ′ , implies divergence ∉ alloc :: 𝜂 ′ . After 𝑛 steps, the expression
   ref 𝑒 reduces to ref 𝑣 ′ in state 𝑠 ′ . We then apply the operational rule REFV, which allocates a
   fresh location 𝑙 and returns it as a value: 𝑠 ′, ref 𝑣 ′ → 𝑠 ′′, 𝑙 Applying the multi-step evaluation
   rule SMULTI, we conclude: 𝑠, ref 𝑒 ↠𝑛+1 𝑠 ′′, 𝑙, where 𝑙 is a value and 𝑠 ′′ is the resulting state
   after allocation. Thus, the full evaluation of ref 𝑒 terminates in 𝑛 +1 steps with a value result, and
   since memory allocation preserves the well-formedness of state (by Lemma 15), we conclude
   that termination holds.
 • Case 2: Suppose the expression 𝑒 has already reduced to a value 𝑣. Then, the full expres-
   sion becomes ref 𝑣. From the typing rule TREF, we know: Γ, Σ, Π, Ψ ⊢ ref 𝑣 : 𝜏 ★, alloc ::
   𝜂 and Γ, Σ, Π, Ψ ⊢ 𝑣 : 𝜏, 𝜂. From the well-formedness of state 𝑠, and by applying the oper-
   ational rule REFV, the expression ref 𝑣 allocates a new memory location 𝑙, stores 𝑣 at that
   location, and returns the location 𝑙. That is, we have:𝑠, ref 𝑣 → 𝑠 ′, 𝑙 using n = 1 for multi
   step. To prove absence of divergence, we now apply the preservation theorem 20 to this step:
   Γ, Σ, Π, Ψ ⊢ ref 𝑣 : 𝜏 ★, alloc :: 𝜂 ∧ 𝑠, ref 𝑣 → 𝑠 ′, 𝑙 → ∃𝜂 ′ . Γ, Σ, Π, Ψ ⊢ 𝑙 : 𝜏 ★, 𝜂 ′ ∧ 𝜂 ′ ⊆ alloc :: 𝜂.
   Because the result is a value 𝑙, and values carry no side-effect, we conclude 𝜂 ′ = 𝜙, and hence:
   divergence ∉ 𝜂 ′ . Thus, ref 𝑣 terminates in a single step to a value 𝑙, and the total effect is
   bounded by the original effect alloc :: 𝜂, which excludes divergence by assumption. Finally, we
   wrap this step using SMULTI to obtain: 𝑠, ref 𝑣 ↠1 𝑠 ′, 𝑙. Hence, termination holds for this case.

  Deref and Memory assignment. The proof for dereference and memory assignment follows in the
similar style as above.
  Let-binding. We proceed by case analysis on whether the expression 𝑒 1 in let 𝑥 : 𝜏 = 𝑒 1 in 𝑒 2 is a
value or not.

 • Case 1: 𝑒 1 is not a value. From the typing judgment Γ, Σ, Π, Ψ ⊢ let 𝑥 : 𝜏 = 𝑒 1 in 𝑒 2 : 𝜏 ′, 𝜂
   and the typing rule TLET, we know: Γ, Σ, Π, Ψ ⊢ 𝑒 1 : 𝜏, 𝜂 1 and 𝑥 ↦→ 𝜏, Γ, Σ, Π, Ψ ⊢ 𝑒 2 :
   𝜏 ′, 𝜂 2, with 𝜂 = 𝜂 1 ∔ 𝜂 2 . By the induction hypothesis on 𝑒 1 , there exists 𝑛, 𝑠 ′, 𝑣 1 such that
   𝑠, 𝑒 1 ↠𝑛 𝑠 ′, 𝑣 1 and divergence ∉ 𝜂 1 . After 𝑛 steps, the expression reduces to let 𝑥 : 𝜏 = 𝑣 1 in 𝑒 2 ,
   and applying rule LETV yields 𝑒 2 [𝑥 ← 𝑣 1 ]. Thus, 𝑠, let 𝑥 : 𝜏 = 𝑒 1 in 𝑒 2 ↠𝑛+1 𝑠 ′, 𝑒 2 [𝑥 ← 𝑣 1 ].
   To conclude, we must show that 𝑒 2 [𝑥 ← 𝑣 1 ] terminates. By Lemma 18 and preservation over
   𝑛 + 1 steps, we get: Γ, Σ, Π, Ψ ⊢ 𝑒 2 [𝑥 ← 𝑣 1 ] : 𝜏 ′, 𝜂 2′ with 𝜂 2′ ⊆ 𝜂 2, and 𝑠 ′ is well-formed. By
   applying the progress theorem to 𝑒 2 [𝑥 ← 𝑣 1 ], we conclude it either is a value or takes a step. In
   the latter case, we apply the IH for 𝑒 2 (on the substituted expression) to conclude termination,
   with divergence still excluded since divergence ∉ 𝜂 1 and divergence ∉ 𝜂 2 .

                                                                  , Vol. 1, No. 1, Article . Publication date: July 2026.
20


  • Case 2: 𝑒 1 is already a value 𝑣 1 . Then we apply rule LET directly: let 𝑥 : 𝜏 = 𝑣 1 in 𝑒 2 → 𝑒 2 [𝑥 ←
    𝑣 1 ]. The rest proceeds as in Case 1: we apply the substitution lemma, preservation, and the
    induction hypothesis to show that 𝑒 2 [𝑥 ← 𝑣 1 ] terminates.
  For loop The only form of looping permitted in BeePL is through the construct for (𝑒 1 . . . 𝑒 2, 𝑑) 𝑒.
The termination proof proceeds by analyzing the different cases of the operational semantics
associated with the for-loop.
  • Case 1: For the case where 𝑒 1 steps to 𝑒 1′ , the induction hypothesis ensures that 𝑒 1 evaluates to a
    value 𝑣 1 in 𝑛 1 steps with divergence ∉ 𝜂 1 , where 𝜂 1 is the effect from the typing of 𝑒 1 in the for-
    loop. Thus, 𝑠, for (𝑒 1 . . . 𝑒 2, 𝑑) 𝑒 ↠𝑛1 for (𝑣 1 . . . 𝑒 2, 𝑑) 𝑒, 𝑠 1 , and by preservation, 𝑣 1 is well-typed,
    𝑠 1 is well-formed, and 𝜂 1′ ⊆ 𝜂 1 . Similarly, by the induction hypothesis for 𝑒 2 , there exists 𝑛 2
    such that 𝑒 2 →𝑛2 𝑣 2 with divergence ∉ 𝜂 2 . Hence, 𝑠 1, for (𝑣 1 . . . 𝑒 2, 𝑑) 𝑒 ↠𝑛2 for (𝑣 1 . . . 𝑣 2, 𝑑) 𝑒, 𝑠 2 ,
    where 𝑣 2 is well-typed, 𝑠 2 is well-formed, and 𝜂 2′ ⊆ 𝜂 2 by preservation. Since 𝑣 1 and 𝑣 2 are
    numeric constants (either int or long per the TFOR rule), the loop range is computed, yielding
    a fixed number 𝑘 ∈ N of iterations, including the case 𝑘 = 0 when the body is skipped.
    We proceed by induction on 𝑘, the number of loop iterations.
       – Base Case (𝑘 = 0): In this case, the range is empty, so the loop body does not execute. The
          loop evaluates in one final step to a unit value: for (𝑣 1 . . . 𝑣 2, 𝑑) 𝑒 → Unit. This takes a
          bounded number of steps (𝑛 1 + 𝑛 2 + 1), and terminates in a value without divergence.
       – Inductive Case (𝑘 > 0): Since the loop body 𝑒 is independent of the loop index and executes
          identically each time, the loop can be treated as 𝑘 repetitions of 𝑒, where 𝑘 is determined
          by 𝑣 1 , 𝑣 2 , and direction 𝑑. By induction, 𝑒 terminates in value 𝑣𝑒 in at most 𝑛𝑒 steps, with
          divergence ∉ 𝜂𝑒 . Thus, the full loop runs 𝑘 independent executions of 𝑒, each taking up to
          𝑛𝑒 steps, and the total steps are bounded by 𝑛 1 + 𝑛 2 + 𝑘 · 𝑛𝑒 . As none of the components
          diverge, the loop terminates without divergence. To show divergence ∉ 𝜂, we note that
          it is absent from 𝜂 1 , 𝜂 2 , and 𝜂𝑒 . Since the typing rule gives 𝜂 = 𝜂 1 ∔ 𝜂 2 ∔ 𝜂𝑒 , we conclude
          divergence ∉ 𝜂, completing the proof.
       – Case 2: For all other cases where the expressions 𝑒 1 , 𝑒 2 , or 𝑒 are already values, we proceed
          in a similar manner as in Case 1. The proof follows the same structure but requires fewer
          evaluation steps, as some sub-expressions do not require further reduction.
    Hence, the full for-loop expression evaluates to a value in finite steps and terminates without
    divergence.
  Function application. The termination proof for function application uses the inductive hypothesis
on argument expressions to ensure their termination. We apply preservation inductively over the
argument list to establish state well-formedness and then instantiate the typing judgment for the
function body. Since BeePL only supports statically defined top-level functions (no closures or
dynamic creation), all invoked functions are guaranteed to be well-typed, and their termination is
analyzed structurally.
  Termination for other expressions—primitive operators, struct initialization, field access, and
pattern matching—is omitted as it follows the same structural induction strategy. For external
function calls, we assume they terminate and do not prove this within BeePL’s semantics.          □

   Lemma 5 states that if a unary or binary operator is well-typed and evaluated in a well-formed
state, the result is never undef. This is not guaranteed by the type system alone, but by a program
transformation performed by the BeePL compiler. While operators like division, modulo, and shifts
are partial in CompCert, BeePL compiler inserts default values in cases of undefined behavior to
ensure well-defined results.


, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                                     21


  Lemma 5. [Absence of undefined behavior]
                                         ∀Γ, Σ, Π, Ψ, 𝑠, 𝑒, 𝑒 1, 𝑒 2, 𝑛, 𝑣, 𝑠 ′ . well formed state(Γ, Σ, 𝑠) =⇒
                  Γ, Σ, Π, Ψ ⊢ bop(𝑜𝑝, 𝑒 1, 𝑒 2 ) : 𝜏, 𝜂 ∧ 𝑠, bop(𝑜𝑝, 𝑒 1, 𝑒 2 ) ↠𝑛 𝑠 ′, 𝑣 =⇒ 𝑣 ≠ undef ∧
                                Γ, Σ, Π, Ψ ⊢ uop(𝑜𝑝, 𝑒) : 𝜏, 𝜂 ∧ 𝑠, uop(𝑜𝑝, 𝑒) ↠𝑛 𝑠 ′, 𝑣 =⇒ 𝑣 ≠ undef

   Proof. The proof proceeds by destructing the goal, which gives us two sub-goals to prove-one
related to binary operator and the other related to unary operator.
  • bop case: 𝑠, bop(𝑜𝑝, 𝑒 1, 𝑒 2 ) ↠𝑛 𝑠 ′, 𝑣 gives two steps: 𝑠, bop(𝑜𝑝, 𝑒 1, 𝑒 2 ) ↠𝑛−1 𝑠 1, bop(𝑜𝑝, 𝑣 1, 𝑣 2 )
    and 𝑠 1, bop(𝑜𝑝, 𝑣 1, 𝑣 2 ) → 𝑠 ′, 𝑣. From BOPV, we get:
                             𝑣 = if unsafe(𝑜𝑝, 𝑣 1, 𝑣 2, 𝑠) then 0 else bopsem (𝑜𝑝, 𝑣 1, 𝑣 2 ).
   Case-split on the conditional: (i) if 𝑣 = 0, then 𝑣 ≠ undef trivially; (ii) if 𝑣 = bopsem (𝑜𝑝, 𝑣 1, 𝑣 2 ),
   apply Lemma 10 to typing Γ, Σ, Π, Ψ ⊢ bop(𝑜𝑝, 𝑒 1, 𝑒 2 ) : 𝜏, 𝜂 and well formed state(Γ, Σ, 𝑠) to
   show that 𝑣 ′ = bopsem (𝑜𝑝, 𝑣 1, 𝑣 2 ) with 𝑣 ′ ≠ undef.
 • uop case: 𝑠, uop(𝑜𝑝, 𝑒) ↠𝑛 𝑠 ′, 𝑣 gives 𝑠, uop(𝑜𝑝, 𝑒) ↠𝑛−1 𝑠 1, uop(𝑜𝑝, 𝑣 1 ) and 𝑠 1, uop(𝑜𝑝, 𝑣 1 ) →
   𝑠 ′, 𝑣. From UOPV, we get uopsem (𝑜𝑝, 𝑣 1 ) = 𝑣. Applying Lemma 9 to typing Γ, Σ, Π, Ψ ⊢ uop(𝑜𝑝, 𝑒) :
   𝜏, 𝜂 and well formed state(Γ, Σ, 𝑠) yields 𝑣 ′ = uopsem (𝑜𝑝, 𝑣 1 ) with 𝑣 ′ ≠ undef. Hence proved.
                                                                                                          □
  Lemma 6. [No uninitialized memory access]
       ∀Γ, Σ, Π, Ψ, 𝑠, 𝜏, 𝜂, 𝑣, 𝑠 ′′ .   Γ, Σ, Π, Ψ ⊢!𝑒 : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠) ∧ 𝑠, !𝑒 ↠𝑛 𝑠 ′′, 𝑣 =⇒
                                           ∃𝜂 ′, 𝑙, 𝑜, 𝑣, 𝑠 ′ . Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏 ★, 𝜂 ′ ∧ 𝜂 ′ ⊆ 𝜂 ∧ 𝑠, 𝑒 → 𝑠 ′, 𝑙 ∧ 𝑠 Θ
                                                                                                                        ′
                                                                                                                          [𝑙] = 𝑣

   Proof. In BeePL, memory locations may arise either through internal allocation via the ref
construct or from the external environment. Given the typing hypothesis Γ, Σ, Π, Ψ ⊢!𝑒 : 𝜏, 𝜂, we
know that the expression 𝑒 must have type 𝜏∗, i.e., a pointer to type 𝜏, and not an option type. Any
pointers originating from outside the program must be resolved using a match construct before
being safely dereferenced. For pointers generated internally within a BeePL program, we know
they are never null, as the semantics of the ref construct guarantees that a value is allocated in
memory and its address is returned.
   From the typing rule for dereferencing, the hypothesis Γ, Σ, Π, Ψ ⊢!𝑒 : 𝜏, 𝜂 implies the existence
of a subderivation Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏∗, 𝜂 ′ such that 𝜂 = read :: 𝜂 ′ . By the effect subsumption property,
we conclude that 𝜂 ′ ⊆ read :: 𝜂 ′ , and the typing goal is discharged accordingly. Now, from the multi-
step evaluation rule SMULTI, applied to the hypothesis 𝑠, !𝑒 ↠𝑛 𝑠 ′′, 𝑣, we obtain two intermediate
steps: 𝑠, !𝑒 ↠𝑛−1 𝑠 1, !𝑣 ′ and 𝑠 1, !𝑣 ′ → 𝑠 ′, 𝑣, where 𝑣 ′ = 𝑙 is a location. By the preservation lemma,
we know that this location 𝑙 remains well-typed in the state 𝑠 1 , and the state itself is well-formed.
This ensures that Σ(𝑙) = 𝜏. Moreover, since a value is always guaranteed to be present at location 𝑙,
we know that the memory access cannot be uninitialized. Finally, by applying Lemma 11, which
guarantees the safety of dereferencing any well-typed location in a well-formed state, we conclude
that there exists a value 𝑣 stored at location 𝑙 in memory 𝑠 ′ . Hence, dereferencing in this case is
always safe, and the proof is complete.                                                                  □
    Lemma 7 (No Null Pointer Dereference). Let Γ, Σ, Π, Ψ be a well-formed typing context, and
let 𝑠 be a well-formed state such that well formed state(Γ, Σ, 𝑠). Then, for any expression 𝑙 and type
𝜏𝑙 , if
                                            Γ, Σ, Π, Ψ ⊢ 𝑙 : 𝜏𝑙 , 𝜂
and 𝑙 is dereferenced (i.e., appears in a subterm of the form !𝑙), then one of the following holds:
  • 𝜏𝑙 = 𝜏 ★, in which case 𝑙 evaluates to a non-null location in memory

                                                                                , Vol. 1, No. 1, Article . Publication date: July 2026.
22


 • 𝜏𝑙 = option 𝜏∗, and the dereference of 𝑙 occurs only inside a match construct (match 𝑙 with Pnone ⇒
   𝑒 | Psome 𝑥 ⇒!𝑥), which ensures that the dereference is only performed in the Some branch,
   after checking for null.
Hence, in all well-typed programs, pointer dereferences are guaranteed to be safe: either the pointer is
guaranteed non-null, or a runtime match check eliminates the null case before dereferencing.
   Proof. Case 1: 𝜏𝑙 = 𝜏 ★. From the typing rule for dereferencing, we know that the judgment
Γ, Σ, Π, Ψ ⊢!𝑙 : 𝜏, read :: 𝜂 ′ is derivable only when 𝑙 has type 𝜏 ★. The typing rules for BeePL do not
permit dereferencing expressions of other types directly. Since Γ, Σ, Π, Ψ ⊢ 𝑙 : 𝜏 ★, 𝜂 ′ and the state
𝑠 is well-formed. From the typing rule of location TLOC, we know that Σ(ℓ) = 𝜏 ★. Moreover, in
BeePL, locations are only introduced via the ref construct, which allocates memory and ensures
that the location stores a value immediately. Therefore, dereferencing ℓ is safe and never accesses
null pointer.
   Case 2: 𝜏𝑙 = option 𝜏∗. By inversion on the typing rule, it is not possible to type !𝑙 directly if 𝑙 has
type option (𝜏∗). The only way a dereference can occur in this case is when 𝑙 is pattern matched
using a match construct: match 𝑙 with Pnone ⇒ 𝑒 1 | Psome 𝑥 ⇒!𝑥. By the typing rule for match,
both branches 𝑒 1 and !𝑥 should be type checked with the same type. Specifically, in the Psome 𝑥
branch, 𝑥 : 𝜏∗ is added to the context. Therefore, inside the Psome branch, dereferencing !𝑥 is
allowed as presence of 𝑥 ensures that 𝑙 is not null. Operationally, the semantics of BeePL guarantee
that only the branch corresponding to the runtime constructor is evaluated during pattern matching.
Hence, !𝑥 is only executed when 𝑙 evaluates to Psome ℓ for some valid memory location ℓ.
   In both cases, dereferencing is only performed on non-null pointers. Either the pointer has type
𝜏 ★ and is directly dereferenced, or it is an option type and pattern matched to safely isolate the Some
case before dereferencing. Therefore, null pointer dereferences cannot occur in any well-typed
BeePL program.                                                                                           □
    Lemma 8 (Memory Bounds Safety). Let Γ, Σ, Π, Ψ ⊢ match 𝑣 with 𝑝 → 𝑒 : 𝜏, 𝜂 and the evaluation
succeeds via the rule MBYTES (the success case), that is, 𝑠, match 𝑣 with 𝑝 → 𝑒 → 𝑠, 𝑒 1 [𝑦𝑖 ↦→ 𝑣𝑖 , 𝑥 ↦→
𝑣 𝑥 ]. Then, all accesses to the byte value 𝑣 during the pattern match are within bounds, i.e., the extraction
extract(𝑣, 𝜏𝑥 ) = (𝑣 𝑥 , {𝑦1 ↦→ 𝑣 1, . . . , 𝑦𝑛 ↦→ 𝑣𝑛 }) is defined only when length(𝑣) ≥ sizeof(𝜏𝑥 ), ensuring
no out-of-bounds memory access occurs.
   Proof. From the typing derivation Γ, Σ, Π, Ψ ⊢ match 𝑣 with 𝑝 → 𝑒 : 𝜏, 𝜂, we know:
  • 𝑣 is a value of type bytes,
  • the pattern includes a case of the form (𝑥, 𝜏𝑥 ) : (𝑦, 𝜏 𝑦 ) ⇒ 𝑒 1 ,
  • sizeof(𝜏𝑥 ) is defined and finite as it extends the context to type check 𝑒.
The result is a direct consequence of the operational semantics, as for match 𝑣 with 𝑝 → 𝑒 to
proceed with extraction and substitution, the check on the length of the buffer (length(𝑣) ≥
sizeof (𝜏𝑥 ) in this case) is necessary to hold. Hence this proves that extraction of a byte buffer 𝑣 in
some target of type 𝜏𝑥 is safe by construction according to the semantics of match (MBTYTES). If
the condition fails, evaluation proceeds via the fallback rule MBYTESF, which does not perform
any memory access. Hence, no out-of-bounds access can occur during evaluation of a match on
bytes. Hence, no rule in the semantics permits extraction from out-of-bounds memory, and all
memory accesses during match evaluation on byte values are within valid bounds.                        □

4.3    Formally verified compiler from BeePL to BPF bytecode
We implemented the BeePL compiler in the Rocq proof assistant. This compiler translates BeePL
expressions into Csyntax, the first intermediate representation used by the CompCert verified
C compiler. The translation preserves the semantics and structural discipline of BeePL while

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                        23


mapping its high-level constructs—such as function calls, control flow, structured data, and memory
operations—into the imperative syntax expected by CompCert. The resulting Csyntax program
is then compiled to BPF bytecode using the CompCert compilation pipeline. This end-to-end
path—from BeePL to BPF via C—enables the generation of safe and semantically sound BPF bytecode,
suitable for secure deployment in the kernel.
   We present the design, structure, and implementation of the BeePL compiler in the Appendix.
There, we detail the translation of key constructs such as ref, let-bindings, for-loops, and match
expressions. Cases with direct one-to-one mappings from BeePL expressions to C statements are
omitted for brevity. At a high level, we highlight how the translation of the for-loop preserves
termination, reflecting a deliberate design choice in the compiler. As detailed in Section 7, the
BeePL-to-C translation evaluates the loop bounds 𝑒 1 and 𝑒 2 once at the start and assigns them to
fresh variables 𝑙 and ℎ. Based on the specified direction (Up or Down), the translation introduces a
fresh loop index 𝑖, initialized to 𝑙, and updates it using either 𝑖++ or 𝑖−− in each iteration. The loop
executes only if the initial condition (𝑙 ≤ ℎ for upward traversal, 𝑙 ≥ ℎ for downward) is satisfied,
and this condition is checked before entering the loop. Since the bounds are fixed and the loop
index advances by exactly one in each iteration, it cannot overshoot or skip the endpoint. As a
result, the loop always makes progress and is guaranteed to terminate. The formal proof of the
compiler’s correctness is given in Lemma 23, which appears in the Appendix.
   Extension of CompCert for Verified Compilation to BPF Bytecode. CompCert already features back-
ends for classic Instruction Set Architectures (ISA), namely PPC, x86, ARM and RISCV. Compared
to those ISAs, eBPF has a very restricted instruction set. For instance, there is no support for signed
arithmetic or floating-point numbers. Our eBPF backend emulates signed arithmetic (notably signed
division) at instruction selection. Other signed operations e.g., a cast to a signed byte is encoded
using a left shift followed by an arithmetic right shift. Programs using floating-point numbers are
simply rejected at assembly generation. All the necessary code for performing and proving the
CompCert optimisation passes is borrowed from existing backends with little modifications.
   The handling of functions calls and return require more work because the eBPF semantics deviate
from what is usually implemented. In standard ISA (except x86), a call is a branch-and-link; the
function prologue allocates a new stack frame, updates the stack pointer 𝑠𝑝 and saves the stack
pointer of the caller and the return address (if needed). At function exit, the stack pointer 𝑠𝑝
is explicitly restored and control is given back to the caller. As soon as the Application Binary
Interface (ABI) is respected, the precise handling of the stack pointer is responsibility of the compiler.
Therefore, at function entry, CompCert sets the stack pointer at the bottom of the newly allocated
stack frame. As a result, within the function, stack accesses are of the form sp + ofs where ofs is a
positive offset.
   In eBPF, things are done differently. A deviation is that the stack register (R10) is documented
as read-only1 . Actually, this is the responsibility of the JIT compiler to update the stack register;
making sure that stack frames are allocated and restored but also to enforce calling-conventions
(callee-save registers are saved at function entry and restored at function exit). As a result, though
the eBPF program never explicitly updates R10, after a call, R10 points to the top of a newly allocated
stack frame. Unlike CompCert, stack accesses are of the form 𝑅10 − ofs. Moreover, the stack pointer
of the caller and the return address are not available. To give a semantics to this behaviour while
maintaining maximum compatibility with CompCert, we arrange the stack-frame layout as shown
in Figure 15.
   The left hand side of Figure 15 shows the layout of a stack frame of the Mach language which
is the last CompCert intermediate language before assembly. We inherit from the CompCert
1 https://www.kernel.org/doc/html/v5.17/bpf/instruction-set.html



                                                                   , Vol. 1, No. 1, Article . Publication date: July 2026.
24


                                      RA                            RA
                                      SP                            SP
                                                                                 R10

                                      LV                            LV
                                                          sp                     BP

                         Fig. 15. Stack layout: Mach language (left), eBPF assembly (right)


infrastructure that the stack register 𝑠𝑝 points to the bottom of the stack frame. However, the
precise layout of the stack frame is architecture dependent. For the eBPF backend, we specify that
the return address RA and the stack pointer of the caller SP are saved at the top of the stack frame.
At assembly level (right hand side of Figure 15), the layout of the stack frame is the same with the
twist that the stack register 𝑅10 points at top of the stack frame just below SP.
   To facilitate the simulation proof, we introduce a (non-architectural) register BP (Base Pointer)
which simulates the Mach 𝑠𝑝 register. Within a function 𝑓 , the stack offset 𝛿 has value 𝑓 .𝑓 𝑛 𝑠𝑡𝑎𝑐𝑘𝑠𝑖𝑧𝑒−
2∗8 because SP and RA are 8 bytes i.e., 64 bits quantities and we have the invariant that 𝑅10 = 𝐵𝑃 +𝛿.
   In terms of assembly generation, there are several consequences that are worth mentioning. First
of all, every Mach stack access of the form 𝑠𝑝 + ofs is compiled into an eBPF access of the form
𝑅10 + (𝑜 𝑓 𝑠 − 𝛿). In our current backend, the Mach instuctions 𝑀𝑡𝑎𝑖𝑙𝑐𝑎𝑙𝑙 which performs a tail call
and 𝑀𝑔𝑒𝑡𝑝𝑎𝑟𝑎𝑚 which fetches arguments from the caller’s stack are not supported. For tailcalls,
the reason is that the classic assembly code sequence to model them consists in a explicit free of the
current stack frame followed allocation by a direct jump to the function entry. As eBPF stack frame
are implicitly handled by the runtime and because it is unclear how to semantically distinguish
between a recursive tailcall to the local function from a genuine local jump, we simply forbid this
construction. Another consequence of the fact that the stack frames are managed by the runtime is
that the eBPF calling conventions only allow parameter passing through registers. The rationale
being that the parent stack frame (the value of SP) is hidden to the callee. This explains why our
backend does not support the Mach instruction 𝑀𝑔𝑒𝑡𝑝𝑎𝑟𝑎𝑚 which fetches arguments from the
caller’s stack.
   Under these restrictions, our current eBPF backend is proved correct within the CompCert
infrastructure and therefore ensure semantics preservation down to eBPF assembly. The assembly
is thereafter compiled down to a loaded elf file using the existing eBPF assembler of the llvm
toolchain.

5    Related Work
   Verifier correctness. There have been promising efforts to enhance verifier correctness, for in-
stance, [9, 58] improve range analysis but do not cover memory safety or termination checks.
Although these works provide formal justifications, they lack machine-checked proofs and re-
main susceptible to state-explosion. Similarly, [44] employs scalable symbolic execution to verify
eBPF safety, but despite path-reduction optimizations, it still faces state-explosion and complex
constraint-solving issues. Another approach [45] ensures BPF Just-In-Time (JIT) compilation cor-
rectness through machine-checked proofs. However, it still relies on the verifier or advanced
symbolic execution tools like Serval for bytecode safety, focusing on preserving correctness in the
translation from BPF bytecode to native machine code rather than addressing verifier limitations.
   State Embedding [53] validates the Linux eBPF verifier by embedding runtime checks to detect
logic bugs, improving trust in existing infrastructure. In contrast, BeePL ensures safety by construc-
tion through a high-level language and a formally verified compiler, eliminating reliance on the

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                 25


kernel verifier. VEP [59] preserves annotations from C to bytecode to aid verification and improve
error messages, but its compiler’s preservation is not formally verified. In contrast, CompCert also
preserves annotations with formal guarantees in Rocq, while BeePL avoids reliance on annotations
altogether. Compilers like Jasmin [3] and CompCert [10] are formally verified to preserve a range of
properties. Unfortunately, these cannot be directly utilized to compile eBPF programs due to their
limitations at both the source and target levels. Neither compiler can reason about eBPF properties
at the source level or produce BPF bytecode as a target.
   Language features. Most BeePL language features on themselves are not unique. Provable ter-
minating loops are part of theorem provers like Rocq [7], Lean [43], Agda [11], and Idris [12]. All
use using structural recursion on algebraic data types to prove termination [1, 2],we use restricted
loop constructs and type-and-effect system to guarantee termination; no arbitrary recursion. Bit-
strings originate from Erlang [5], and are also part of other languages compiling to the BEAM, like
Elixir [57] and Gleam [50]. Preventing null pointer dereferencing using Option-types originates
from functional languages [49], and are part of multiple modern system languages, among others
Rust [23] and Swift [31]. These languages also prevent accessing uninitialised memory access
with flow analysis. To the best of our knowledge, we do not know of any language preventing
use-after-free bugs by prohibiting procedures to return pointer types. In a general purpose language,
this is a severe restriction. However, in a DSL like BeePL we think it is a reasonable trade-off. The
combination of the above language features and the certified pipeline make BeePL an appealing
source language to write verified eBPF kernel code.
   Safe programming languages. We would also like to highlight the scope of extending or reusing
other languages such as Koka [56], CakeML [24], and Cogent [48] for our purpose. While CakeML
features a fully verified compiler from a high-level functional language to machine code, it is
not well suited for writing eBPF programs due to its general-purpose design. In particular, it
does not target BPF bytecode and lacks support for the specific runtime conventions required by
the eBPF execution environment. The same limitations apply to Koka. Both languages assume
a general-purpose memory model that allows unrestricted use of dynamic memory allocation
(e.g., via malloc), and their standard libraries heavily rely on such capabilities. Adapting these
languages to target eBPF would require imposing the same constraints we enforce in BeePL, such as
a restricted memory model, precise effect tracking, and compatibility with the eBPF verifier, which
would entail substantial modifications and effort. Instead, we focused on adding a new front-end
to CompCert, allowing us to reuse its verified optimization and code generation passes without
having to reimplement/modify them.
   Cogent employs uniqueness typing to eliminate errors such as uninitialized memory access,
use-after-free bugs, and undefined behavior. It generates refinement obligations in Isabelle/HOL
that users must manually discharge to establish correctness relative to their specifications, though
its compiler remains part of the trusted base. In contrast, BeePL provides a formally verified
compilation toolchain, guaranteeing preservation of safety properties stated at the source level
without additional user effort.
   Fuzzing and testing. Previous works [13, 22, 26, 54, 55] have applied fuzzing techniques to detect
verifier bugs. While fuzzing is more effective than traditional testing, it lacks completeness, produces
false positives, and struggles with scalability in detecting logical or semantic issues. The work [26]
introduces a fuzzing method using a Bound-Violation Indicator (BVI) to find logical bugs in the eBPF
verifier. It detects inconsistencies in range analysis between the verifier and actual execution. This
exposes bugs that can lead to unsafe memory access. Syzkaller [55] is an automated fuzzer designed
to test the Linux kernel by generating syscall sequences that explore deep kernel paths. It uses

                                                            , Vol. 1, No. 1, Article . Publication date: July 2026.
26


coverage-guided fuzzing to find bugs like crashes, memory corruption, and security vulnerabilities.
BUZZER [13] is a fuzzer for the Linux kernel’s eBPF verifier that targets semantic bugs by solving
symbolic constraints to generate programs that bypass the verifier. It combines symbolic execution
with fuzzing to explore hard-to-reach verifier logic paths. The work [22] highlights that fuzzers
often fail to generate inputs that adhere to semantic specifications and necessary dependencies,
making them ineffective for detecting correctness bugs. Since fuzzer-generated programs do not
sufficiently trigger the verifier’s complex analyses [54], they mainly uncover simple memory issues
rather than deeper correctness flaws. Addressing such bugs requires stronger assertions at key
verification checkpoints.

6    Limitations and future work
Our framework does not currently analyze stack usage or enforce stack frame size limits, nor
does it perform detailed scope or liveness analysis. To ensure memory safety, we conservatively
disallow functions from returning the address of local variables, avoiding access to deallocated stack
memory. All eBPF helpers are currently treated as external calls with assumed correctness, placing
them in the trusted computing base (TCB). To reduce the TCB, we plan to formally specify and
verify commonly used helpers, either by modeling their behavior in our semantics or proving their
contracts. Future work includes integrating formal scope and liveness analysis to safely support
address-returning functions, extending the type system to track memory-region-based effects for
finer control over aliasing and lifetimes.

References
 [1] Andreas Abel. 2004. Termination checking with types. RAIRO-Theoretical Informatics and Applications 38, 4 (2004),
     277–319.
 [2] Andreas Abel and Thorsten Altenkirch. 2002. A predicative analysis of structural recursion. Journal of functional
     programming 12, 1 (2002), 1–41.
 [3] José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, Arthur Blot, Benjamin Grégoire, Vincent Laporte, Tiago Oliveira,
     Hugo Pacheco, Benedikt Schmidt, and Pierre-Yves Strub. 2017. Jasmin: High-Assurance and High-Speed Cryptography.
     In Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security (Dallas, Texas, USA)
     (CCS ’17). Association for Computing Machinery, New York, NY, USA, 1807–1823. doi:10.1145/3133956.3134078
 [4] Alok Tiagi, Hariharan Ananthakrishnan, Ivan Porto Carrero and Keerti Lakshminarayan. [n. d.]. Open-sourcing Katran,
     a scalable network load balancer. Available at https://netflixtechblog.com/how-netflix-uses-eBPF-flow-logs-at-scale-
     for-network-insight-e3ea997dca96. consulted July 2025.
 [5] Joe Armstrong. 2007. A history of Erlang. In Proceedings of the third ACM SIGPLAN conference on History of programming
     languages. 6–1.
 [6] Kael Soares Augusto, Vinícius Pacheco, Marcos A. Vieira, Rodrigo Geraldo Ribeiro, and Fernando Magno Quintão
     Pereira. 2025. Honey Potion: An eBPF Backend for Elixir. In Proceedings of the 23rd ACM/IEEE International Symposium
     on Code Generation and Optimization (Las Vegas, NV, USA) (CGO ’25). Association for Computing Machinery, New
     York, NY, USA, 660–674. doi:10.1145/3696443.3708923
 [7] Bruno Barras, Samuel Boutin, Cristina Cornes, Judicaël Courant, Yann Coscoy, David Delahaye, Daniel de Rauglaudre,
     Jean-Christophe Filliâtre, Eduardo Giménez, Hugo Herbelin, et al. 1999. The Coq proof assistant reference manual.
     INRIA, version 6, 11 (1999), 17–21.
 [8] Frédéric Besson, Sandrine Blazy, and Pierre Wilke. 2015. A Concrete Memory Model for CompCert. doi:10.1007/978-3-
     319-22102-1_5
 [9] Sanjit Bhat and Hovav Shacham. 2022. Formal Verification of the Linux Kernel eBPF Verifier Range Analysis. In
     Semantic Scholar (2022). https://api.semanticscholar.org/CorpusID:252564197
[10] Sandrine Blazy, Zaynah Dargaye, and Xavier Leroy. 2006. Formal verification of a C compiler front-end. In Proceedings
     of the 14th International Conference on Formal Methods (Hamilton, Canada) (FM’06). Springer-Verlag, Berlin, Heidelberg,
     460–475. doi:10.1007/11813040_31
[11] Ana Bove, Peter Dybjer, and Ulf Norell. 2009. A brief overview of Agda–a functional language with dependent types.
     In Theorem Proving in Higher Order Logics: 22nd International Conference, TPHOLs 2009, Munich, Germany, August 17-20,
     2009. Proceedings 22. Springer, 73–78.


, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                             27


[12] Edwin Brady. 2013. Idris, a general-purpose dependently typed programming language: Design and implementation.
     Journal of functional programming 23, 5 (2013), 552–593.
[13] Buzzer Developers. [n. d.]. Buzzer. Available at https://github.com/google/buzzer. consulted Feb 2025.
[14] Cloudflare [n. d.].           Cloudflare architecture and how BPF eats the world.                         Available at
     https://blog.cloudflare.com/cloudflare-architecture-and-how-bpf-eats-the-world/. consulted July 2025.
[15] Daniel Borkmann. [n. d.]. bpf: Undo incorrect reg bound offset32 handling. Available at https://git.kernel.org/pub/
     scm/linux/kernel/git/torvalds/linux.git/commit/?id=64620e0a1e712a778095bd35cbb277dc2259281f. Consulted May
     2025.
[16] eBPF. [n. d.]. eBPF official website. Available at https://eBPF.io/. consulted July 2025.
[17] eBPF Documentary. [n. d.]. eBPF Case Studies. Available at https://ebpf.io/case-studies/. consulted July 2025.
[18] Falco. 2025. Falco organization. https://falco.org/ Accessed February 2025.
[19] Go Developers. [n. d.]. Go. Available at https://go.dev/. consulted Feb 2025.
[20] Google [n. d.].      New GKE Dataplane V2 increases security and visibility for containers.                   Available
     at https://cloud.google.com/blog/products/containers-kubernetes/bringing-eBPF-and-cilium-to-google-kubernetes-
     engine. consulted July 2025.
[21] Muhammad Hassnain and Caleb Stanford. 2024. Counterexamples in Safe Rust. In Proceedings of the 39th IEEE/ACM
     International Conference on Automated Software Engineering Workshops (Sacramento, CA, USA) (ASEW ’24). Association
     for Computing Machinery, New York, NY, USA, 128–135. doi:10.1145/3691621.3694943
[22] Hsin-Wei Hung and Ardalan Amiri Sani. 2024. BRF: Fuzzing the eBPF Runtime. Proc. ACM Softw. Eng. 1, FSE, Article
     52 (July 2024), 20 pages. doi:10.1145/3643778
[23] Steve Klabnik and Carol Nichols. 2023. The Rust programming language. No Starch Press.
[24] Ramana Kumar, Magnus O. Myreen, Michael Norrish, and Scott Owens. 2014. CakeML: a verified implementation
     of ML. In Proceedings of the 41st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (San
     Diego, California, USA) (POPL ’14). Association for Computing Machinery, New York, NY, USA, 179–191. doi:10.1145/
     2535838.2535841
[25] Xavier Leroy. 2009. A Formally Verified Compiler Back-end. J. Autom. Reason. 43, 4 (Dec. 2009), 363–446. doi:10.1007/
     s10817-009-9155-4
[26] Youlin Li, Weina Niu, Yukun Zhu, Jiacheng Gong, Beibei Li, and Xiaosong Zhang. 2023. Fuzzing Logical Bugs in eBPF
     Verifier with Bound-Violation Indicator. In ICC 2023 - IEEE International Conference on Communications. 753–758.
     doi:10.1109/ICC45041.2023.10278676
[27] Linux [n. d.]. bpf: Undo incorrect reg bound offset32 handling. Available at https://git.kernel.org/pub/scm/linux/
     kernel/git/netdev/net-next.git/commit/?id=f2d67fec0b43edce8c416101cdc52e71145b5fef. Consulted May 2025.
[28] Linux 2023. Kernel: eBPF: insufficient stack type checks in dynptr. Available from Red Hat, Inc., CVE-ID CVE-2021-4159.
     https://www.cve.org/CVERecord?id=CVE-2023-39191
[29] Lua Developers. [n. d.]. Lua. Available at https://www.lua.org/. consulted Feb 2025.
[30] Aya maintainers. [n. d.]. Aya. Available at https://github.com/aya-rs/aya. consulted Feb 2025.
[31] Swift maintainers. 2025.         The Swift Programming Language.             Available at https://docs.swift.org/swift-
     book/documentation/the-swift-programming-language/. consulted July 2025.
[32] MITRE. [n. d.]. bpf: Fix 32 bit src register truncation on div/mod. Available at https://git.kernel.org/pub/scm/linux/
     kernel/git/torvalds/linux.git/commit/?id=e88b2c6e5a4d9ce30d75391e4d950da74bb2bd90. Consulted May 2025.
[33] MITRE. 2020. CVE-2020-8835. Available from Red Hat, Inc., CVE-ID CVE-2020-8835. https://nvd.nist.gov/vuln/detail/
     cve-2020-8835
[34] MITRE. 2021. CVE-2021-3600. Available from Red Hat, Inc., CVE-ID CVE-2021-3600. https://access.redhat.com/
     security/cve/cve-2021-3600
[35] MITRE. 2021. CVE-2022-23222. Available from Red Hat, Inc., CVE-ID CVE-2022-23222. https://access.redhat.com/
     security/cve/cve-2021-3600
[36] MITRE. 2022. CVE-2021-4159. Available from Red Hat, Inc., CVE-ID CVE-2021-4159. https://nvd.nist.gov/vuln/detail/
     CVE-2021-4159
[37] MITRE. 2022. CVE-2022-0433. Available from NVD, CVE-ID CVE-2022-0433. https://nvd.nist.gov/vuln/detail/CVE-
     2022-0433
[38] MITRE. 2024. CVE-2022-3606. Available from NVD, CVE-ID CVE-2022-3606. https://nvd.nist.gov/vuln/detail/CVE-
     2022-0433
[39] MITRE. 2024. CVE-2024-38566. Available from NVD, CVE-ID CVE-2024-38566. https://nvd.nist.gov/vuln/detail/cve-
     2024-38566
[40] MITRE. 2025. CVE-2025-21852. Available from NVD, CVE-ID CVE-2025-21852. https://nvd.nist.gov/vuln/detail/CVE-
     2025-21852



                                                                        , Vol. 1, No. 1, Article . Publication date: July 2026.
28


[41] MITRE. 2025. Existing CVE List for eBPF. Available at https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=BPF.
     Consulted February 2025.
[42] Mohamed Husain Noor Mohamed, Xiaoguang Wang, and Binoy Ravindran. 2023. Understanding the Security of Linux
     eBPF Subsystem. In Proceedings of the 14th ACM SIGOPS Asia-Pacific Workshop on Systems (Seoul, Republic of Korea)
     (APSys ’23). Association for Computing Machinery, New York, NY, USA, 87–92. doi:10.1145/3609510.3609822
[43] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 theorem prover and programming language. In Automated
     Deduction–CADE 28: 28th International Conference on Automated Deduction, Virtual Event, July 12–15, 2021, Proceedings
     28. Springer, 625–635.
[44] Luke Nelson, James Bornholt, Ronghui Gu, Andrew Baumann, Emina Torlak, and Xi Wang. 2019. Scaling symbolic
     evaluation for automated verification of systems code with Serval. In Proceedings of the 27th ACM Symposium on
     Operating Systems Principles (Huntsville, Ontario, Canada) (SOSP ’19). Association for Computing Machinery, New
     York, NY, USA, 225–242. doi:10.1145/3341301.3359641
[45] Luke Nelson, Jacob Van Geffen, Emina Torlak, and Xi Wang. 2020. Specification and verification in the field: Applying
     formal methods to BPF just-in-time compilers in the Linux kernel. In 14th USENIX Symposium on Operating Systems
     Design and Implementation (OSDI 20). USENIX Association, 41–61. https://www.usenix.org/conference/osdi20/
     presentation/nelson
[46] Nikita Shirokov, Ranjeeth Dasineni. [n. d.]. How Netflix uses eBPF flow logs at scale for network insight. Avail-
     able at https://engineering.fb.com/2018/05/22/open-source/open-sourcing-katran-a-scalable-network-load-balancer/.
     consulted July 2025.
[47] Cilium Organization. [n. d.]. Cilium. Available at https://github.com/cilium/eBPF. consulted Feb 2025.
[48] LIAM O’CONNOR, ZILIN CHEN, CHRISTINE RIZKALLAH, VINCENT JACKSON, SIDNEY AMANI, GERWIN KLEIN,
     TOBY MURRAY, THOMAS SEWELL, and GABRIELE KELLER. 2021. Cogent: uniqueness types and certifying compila-
     tion. Journal of Functional Programming 31 (2021), e25. doi:10.1017/S095679682100023X
[49] Benjamin C Pierce. 2002. Types and programming languages. MIT press.
[50] Louis Pilfold. 2025. The Gleam Programming Language. Available at https://tour.gleam.run. consulted July 2025.
[51] Rust Project Developers. [n. d.]. Rust. Available at https://www.rust-lang.org/. consulted Feb 2025.
[52] Shahar Azulay, Co-Founder at GroundCover. [n. d.]. Empowering Kubernetes Observability with eBPF on Amazon EKS.
     Available at https://aws.amazon.com/blogs/containers/empowering-kubernetes-observability-with-ebpf-on-amazon-
     eks/. consulted July 2025.
[53] Hao Sun and Zhendong Su. 2024. Validating the eBPF Verifier via State Embedding. In 18th USENIX Symposium
     on Operating Systems Design and Implementation (OSDI 24). USENIX Association, Santa Clara, CA, 615–628. https:
     //www.usenix.org/conference/osdi24/presentation/sun-hao
[54] Hao Sun, Yiru Xu, Jianzhong Liu, Yuheng Shen, Nan Guan, and Yu Jiang. 2024. Finding Correctness Bugs in eBPF
     Verifier with Structured and Sanitized Program. In Proceedings of the Nineteenth European Conference on Computer
     Systems (Athens, Greece) (EuroSys ’24). Association for Computing Machinery, New York, NY, USA, 689–703. doi:10.
     1145/3627703.3629562
[55] Syzkaller Developers. [n. d.]. Syzkaller - kernel fuzzer. Available at https://github.com/google/syzkaller. consulted Feb
     2025.
[56] Eran Tromer, Dag Arne Osvik, and Adi Shamir. 2010. Efficient Cache Attacks on AES, and Countermeasures. J.
     Cryptology 23 (07 2010), 37–71. doi:10.1007/s00145-009-9049-y
[57] José Valim. 2025. The Elixir Reference Manual. Available at https://elixir-lang.org. consulted July 2025.
[58] Harishankar Vishwanathan, Matan Shachnai, Srinivas Narayana, and Santosh Nagarakatte. 2023. Verifying the
     Verifier: eBPF Range Analysis Verification. In Computer Aided Verification: 35th International Conference, CAV 2023,
     Paris, France, July 17–22, 2023, Proceedings, Part III (Paris, France). Springer-Verlag, Berlin, Heidelberg, 226–251.
     doi:10.1007/978-3-031-37709-9_12
[59] Xiwei Wu, Yueyang Feng, Tianyi Huang, Xiaoyang Lu, Shengkai Lin, Lihan Xie, Shizhen Zhao, and Qinxiang Cao.
     2025. VEP: A Two-stage Verification Toolchain for Full eBPF Programmability. In 22nd USENIX Symposium on
     Networked Systems Design and Implementation (NSDI 25). USENIX Association, Philadelphia, PA, 277–299. https:
     //www.usenix.org/conference/nsdi25/presentation/wu-xiwei

7     Appendix
7.1    Auxillary Lemmas
Lemma 9 states that if a unary operation is applied to a well-typed value in a well-formed state,
then its evaluation will succeed and produce a defined result. It guarantees that no unary operation
will cause the program to get stuck.


, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                           29


  Lemma 9 (Progress for unary operators).
               ∀Σ, Γ, Π, Ψ, 𝑜𝑝, 𝑣. Γ, Σ, Π, Ψ ⊢ uop(𝑜𝑝, 𝑣) : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠) =⇒
                                                               ∃𝑣 ′, uopsem (𝑜𝑝, 𝑣) = 𝑣 ′ ∧ 𝑣 ′ ≠ undef

    Proof. The proof proceeds by performing a case analysis on the operator 𝑜𝑝, which yields
separate goals for each unary operator supported in BeePL. BeePL supports unary operators
such as boolean negation, integer complement, and unary negation. The semantics of unary
operators are closely tied to the type of their arguments and only fail when applied to values of
incorrect type. However, the typing rules in BeePL ensure that such ill-typed cases are ruled out
statically, preventing any undefined behavior at runtime. Also, BeePL type system ensures that
unary operators are only allowed on primitive types. Boolean negation case. From the hypothesis
(typing rule TUOP), we know that the type of the value 𝑣 is bool. Negating a boolean value
(i.e., true or false) always succeeds and returns its logical complement (false or true), which is
a well-defined value. Thus, this case is proven. Integer complement and negation case. From the
hypothesis (typing rule TUOP), we know that the type of the value 𝑣 is either int or long. We
consider each type separately. Based on the semantics of integer complement and unary negation,
both operations succeed on 32-bit and 64-bit integers and always produce defined results. Hence,
the goal follows.                                                                               □
   Lemma 10 states that if a binary operation is applied to a well-typed values in a well-formed
state, then its evaluation will succeed and produce a defined result. It guarantees that no binary
operation will cause the program to get stuck.

  Lemma 10 (Progress for binary operators).
           ∀Σ, Γ, Π, Ψ, 𝑜𝑝, 𝑣 1, 𝑣 2 . Γ, Σ, Π, Ψ ⊢ bop(𝑜𝑝, 𝑣 1, 𝑣 2 ) : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠) =⇒
                                                               ∃𝑣 ′, bopsem (𝑜𝑝, 𝑣 1, 𝑣 2 ) = 𝑣 ′ ∧ 𝑣 ′ ≠ undef

   Proof. The proof proceeds by performing a case analysis on the binary operator 𝑜𝑝, which yields
separate subgoals for each binary operator supported by BeePL. To ensure well-defined semantics,
we must guarantee that operators are applied to operands of appropriate types—a property enforced
by the typing rule (TBOP) for binary operators, as assumed in our hypothesis. The most interesting
cases arise with operators that may result in undefined behavior, such as division, modulo, and
shift. These operators are susceptible to runtime errors like division by zero or arithmetic overflow.
We illustrate the reasoning using the case of the division operator.
   The division operator in BeePL is categorized into signed and unsigned variants. For unsigned
division, undefined behavior may occur only when the divisor is zero. According to BeePL’s seman-
tics, an unsafe unsigned division is handled gracefully by producing a default value—specifically,
zero. In such cases, we apply the BOPV rule by constructing a value equal to 0 and discharging the
goal that requires proving unsafe(𝑜𝑝, 𝑣 1, 𝑣 2, 𝑠) = true. By definition, the unsafe predicate returns
true precisely when 𝑜𝑝 is an unsigned division and 𝑣 2 = 0. For the safe case, i.e., when unsafe
returns false, we appeal to the semantics of binary operations, which ensures that the function
bopsem produces a valid result.
   In the case of signed division, the semantics of unsafe are more involved, covering not only
division by zero but also arithmetic overflow conditions (e.g., dividing the most negative value by
−1 in two’s complement). Nevertheless, the proof strategy remains the same: distinguish between
the safe and unsafe cases using the unsafe predicate and construct the corresponding semantic
outcome. This approach generalizes naturally to other potentially unsafe operators such as modulo
and shift. In each case, the semantics ensure that well-typed expressions either evaluate to a
defined value or are handled explicitly through default values when unsafe conditions are detected.

                                                                      , Vol. 1, No. 1, Article . Publication date: July 2026.
30


Hence, we conclude that all well-typed binary operations in BeePL have a well-defined semantics,
ensuring progress and safety even in the presence of operations that are typically prone to undefined
behavior.                                                                                           □

     Lemma 11 (Safe dereference for valid pointers).
              ∀Σ, 𝑙, 𝑠, 𝜏 . Σ 𝑙 = 𝜏 ∗ ∧isValidAccess(𝑠 Θ, 𝑙, Freeable) =⇒ ∃ 𝑣, 𝑠 Θ [𝑙] = 𝑣 ∧ typeof(𝑣) = 𝜏

   Proof. From the hypothesis, we know that the location 𝑙 is well-typed in the store typing
environment Σ. Such a location appears in the store context only if it was freshly allocated using
the ref construct or produced during the evaluation of an expression. If 𝑙 was created via ref, then
a value has already been stored at that location, making dereferencing safe. If 𝑙 originates from the
external environment, its use is always guarded by a match construct that rules out null pointers,
ensuring safety before dereferencing. Additionally, the hypothesis and the definition of valid access
confirm that the address 𝑙 is allocated in memory Θ and has Freeable permission. According to the
CompCert memory model, this level of permission allows all memory operations, including reads.
Thus, a load from 𝑙 is guaranteed to succeed and return a value 𝑣. It remains to show that the value
𝑣 has the expected type. Since Σ 𝑙 = 𝜏∗, the location 𝑙 was allocated with type 𝜏, and only values of
type 𝜏 can be stored at 𝑙 (due to the type preservation invariant of the CompCert memory model).
Hence, the type of the value 𝑣 loaded from 𝑙 is indeed 𝜏, i.e., typeof(𝑣) = 𝜏.                      □

     Lemma 12 (Safe assignment for valid pointers).
                   ∀Γ, Σ, 𝑙, 𝑠, 𝑣, 𝜏 . Σ 𝑙 = 𝜏 ∗ ∧typeof (𝑣) = 𝜏 ∧ isValidAccess(𝑠 Θ, 𝑙, Freeable) =⇒
                                   ∃ Θ′, 𝑠 Θ [𝑙 → 𝑣] = Θ′ ∧ well formed store(Γ, Σ, ≺ 𝑠 Δ , 𝑠 Ω , Θ′ ≻)

   Proof. From the hypothesis, we know that the location 𝑙 is well-typed in the store typing
environment Σ. This location may either result from a fresh allocation using the ref construct
or originate from the external environment. In the case of ref, the location is guaranteed to be
valid, and the hypothesis ensures that the value being assigned is compatible with the pointer
type associated with 𝑙, thereby making the assignment safe. For locations obtained from the
external environment, the language enforces that any assignment must be wrapped in a match
construct. This discipline ensures that assignments are only performed on valid, non-null locations,
preventing unsafe memory updates. Finally, we show that the updated state ≺ 𝑠 Δ, 𝑠 Ω , Θ′ ≻ remains
well-formed. Here, Θ′ is the updated memory obtained by assigning the value 𝑣 to the location 𝑙.
Since the assignment respects the expected type of 𝑙, the location remains well-typed in the context
Σ. Moreover, the memory invariant isValidAccess(Θ′, 𝑙, Freeable) continues to hold: the original
memory Θ guaranteed valid access to 𝑙, and the assignment does not alter memory permissions.
Hence, the updated state preserves all well-formedness invariants.                                □
  Lemma 13 ensures that memory allocation always succeeds and yields an updated memory that
remains well-formed, provided the initial state was well-formed.

     Lemma 13 (well formed allocation).
            ∀Γ, Σ, 𝑠, 𝑙𝑜, ℎ𝑖.well formed state(Γ, Σ, 𝑠) =⇒
                            ∃Θ′, 𝑙, 𝑣, alloc(𝑠 Θ, 𝑙𝑜, ℎ𝑖) = (Θ′, 𝑙) ∧ well formed store(Γ, Σ, ≺ 𝑠 Δ , 𝑠 Ω , Θ′ ≻)

   Proof. The proof follows from the properties of the alloc function. In CompCert, memory
allocation is defined as a total function that always succeeds, assuming an infinite memory model at
the source level. BeePL adopts this allocation model and adapts it to its own type system by wrapping
CompCert’s memory primitives around BeePL-specific types. The allocation is parameterized by
the bounds 𝑙𝑜 and ℎ𝑖, which determine the size of the memory block to be allocated. From the

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                             31


hypothesis, we know that the initial state 𝑠 is well-formed. The allocation operation modifies only
the memory component 𝑠 Θ of the state, producing an updated memory Θ′ and a fresh location 𝑙.
The updated memory Θ′ is also well-formed. This is because allocation does not interfere with
existing locations—it guarantees that the new location 𝑙 is fresh and does not overlap with any
location already present in Θ. According to the CompCert memory model, 𝑙 becomes valid only
in Θ′ and not in the original memory Θ. Furthermore, all locations that were valid in Θ remain
valid in Θ′ due to the monotonicity properties of memory allocation in CompCert. As a result, the
invariant of well-formedness is preserved across the allocation, completing the proof.           □

  Lemma 14 (ext well formed).
   ∀ Γ, Σ, 𝑠, 𝑥, 𝑙, 𝜏 .   well formed state(Γ, Σ, 𝑠) ∧ Γ(𝑥) = None ∨ (∃ 𝜏 ′ . Γ(𝑥) = Some 𝜏 ′ ∧ 𝜏 ′ = 𝜏) ⇒
                                                                                                        

                          well formed store(Γ, Σ, ≺ 𝑠 Δ , 𝑠 Ω [𝑥 ↦→ (𝑙, 𝜏)], Θ′ ≻)

    Proof. We proceed by considering an arbitrary variable 𝑥 ′ such that Γ(𝑥 ′ ) = 𝜏𝑥 for some type
𝜏𝑥 . Our goal is to show that in the extended variable map 𝑠 Ω [𝑥 ↦→ (𝑙, 𝜏)], the value assigned to 𝑥 ′ is
a pair (𝑙 ′, 𝜏 ′ ) such that 𝜏 ′ = 𝜏 and the location 𝑙 ′ is well-typed in memory. The proof proceeds by
case analysis on whether 𝑥 ′ is the newly added variable: Case 1: 𝑥 ′ = 𝑥. Since Γ(𝑥 ′ ) = 𝜏𝑥 , it follows
that 𝑥 is already present in the typing environment. By our assumption, we have 𝜏 = 𝜏𝑥 and the
memory location 𝑙 is well-typed for type 𝜏. Therefore, in the extended store 𝑠 Ω [𝑥 ↦→ (𝑙, 𝜏)], the
binding for 𝑥 ′ satisfies the well-formedness condition. Case 2: 𝑥 ′ ≠ 𝑥. In this case, the extended
variable map does not modify the binding for 𝑥 ′ , i.e.,
                                          𝑠 Ω [𝑥 ↦→ (𝑙, 𝜏)] (𝑥 ′ ) = 𝑠 Ω (𝑥 ′ ).
Since the original store 𝑠 Ω was well-formed, and the binding for 𝑥 ′ is unchanged, the well-
formedness condition continues to hold. Thus, in both cases, the extended store preserves the
well-typedness of the state.                                                                □
   Lemma 15 states that if the state 𝑠 is well-typed and a value 𝑣 has type 𝑡, then we can always
allocate fresh memory for 𝑡, store 𝑣 in it, and the resulting state will still be well-typed.

  Lemma 15 (ref allocation succeeds).
∀Γ, Σ, 𝑠, 𝑣, 𝑡 .well formed state(Γ, Σ, 𝑠) ∧ typeof(𝑣) = 𝜏 =⇒
            ∃Θ′, 𝑙, 𝑣, alloc(𝑠 Θ, size(𝜏)) = (Θ′, 𝑙) ∧ Θ′ [𝑙 → 𝑣] = Θ′′ ∧ well formed store(Γ, Σ, ≺ 𝑠 Δ , 𝑠 Ω , Θ′′ ≻)

   Proof. From the hypothesis, we know that the store 𝑠 is well-formed and the value 𝑣 has type
𝜏. Let 𝑠𝑧 denote the size computed from 𝜏 using the function size, representing the number of
bytes required to allocate a value of type 𝜏 in memory 𝑠 Θ . The allocation range is defined with
a lower bound of 0 and an upper bound of 𝑠𝑧. In CompCert, the function alloc is total: it always
returns a newly allocated memory block along with an updated memory state. The underlying
memory model is assumed to be unbounded at a high level, and the function succeeds as long as the
constraint 𝑙𝑜 ≤ ℎ𝑖 holds—in our case, 0 ≤ 𝑠𝑧. This is also ensured by the Lemma 13. To guarantee
that storing the value 𝑣 in memory succeeds, we must ensure that the address being written to is
valid, the memory block has sufficient space to hold the value, and the location has appropriate
write permissions. The allocation performed by alloc ensures these conditions by returning a fresh
location 𝑙 with a valid offset range [0, 𝑠𝑧] and assigning it the Freeable permission. This permission
level allows the memory to be read, written, and later deallocated safely.
   The well-typedness of the value, captured by the hypothesis typeof(𝑣) = 𝜏, guarantees that
the value is semantically consistent with the allocated memory layout and can be safely stored
at the target location. Lastly, we prove that the update state≺ 𝑠 Δ, 𝑠 Ω , Θ′′ ≻ is also well formed.
The memory Θ′ differs from Θ only at location 𝑙, which is freshly allocated and therefore not

                                                                        , Vol. 1, No. 1, Article . Publication date: July 2026.
32


present in Γ or 𝑠 Ω . Since all three constructors of well formed store quantify only over variables
and locations already present in Γ and Σ, and all such blocks are unchanged in Θ′ and Θ′′ , the
original well-formedness proof for 𝑠 still applies to ≺ 𝑠 Δ, 𝑠 Ω , Θ′′ ≻.                         □

   Lemma 16 states that if we begin with a well-formed state 𝑠 and allocate a list of variables denoted
by 𝑥, then there exists an updated state in which all variables have been successfully allocated, and
this new state remains well-formed.

     Lemma 16 (Var allocation succeeds).
∀Γ, Σ, 𝑠, 𝑥 . well formed state(Γ, Σ, 𝑠) ∧ unique 𝑥 =⇒
            ∃Ω ′, Θ′, alloc(𝑠 Θ, size(𝜏𝑖 )) = (Θ′, 𝑙) ∧ 𝑠 Ω [𝑥 → 𝑙𝑖 , 𝜏𝑖 ] = Ω ′ ∧ well formed store(Γ, Σ, ≺ 𝑠 Δ , Ω ′, Θ′ ≻)

   Proof. The proof proceeds by induction on the list of variables 𝑥. Base case. When the list is
empty, the result is immediate. Since there are no variables to allocate, the original state is returned
unchanged, and well-formedness follows directly from the hypothesis. Inductive case. Suppose the
list is of the form (𝑥 1, 𝜏1 ) :: (𝑥𝑖 , 𝜏𝑖 ). By the induction hypothesis, allocating the remaining variables
(𝑥𝑖 , 𝜏𝑖 ) yields a new state that is well-formed, assuming the list contains no duplicates. For the
head element (𝑥 1, 𝜏1 ), we apply Lemma 13, which guarantees that allocation always succeeds and
produces a well-formed memory state. We use this result to instantiate the induction hypothesis
on the tail (𝑥𝑖 , 𝜏𝑖 ), using the updated memory obtained by allocating space for 𝑥 1 starting at offset
0 with size of 𝜏1 , resulting in the final memory state Θ′ . Finally, Lemma 14 ensures that extending
the variable environment with the new bindings 𝑠 Ω [𝑥 → 𝑙𝑖 , 𝜏𝑖 ] preserves well-formedness. Thus,
the extended state remains well-formed after allocating all variables in the list.                         □

  Lemma 17 states that if we begin with a well-formed state 𝑠 and bind the variables 𝑥 with values
𝑣 where the length of 𝑥 is same as length of 𝑣, then there exists an updated state in which all
variables have been successfully assigned the values, and this new state remains well-formed.

     Lemma 17 (bind variables succeeds).
                      ∀Γ, Σ, 𝑠. well formed state(Γ, Σ, 𝑠) ∧ |𝑥 | = |𝑣 | =⇒
                                ∃Θ′, 𝑠 Θ [𝑥 → 𝑣] = Θ′ ∧ well formed store(Γ, Σ, ≺ 𝑠 Δ , 𝑠 Ω , Θ′ ≻)

   Proof. The proof proceeds by induction on the lists 𝑥 and 𝑣. Base case. If both lists are empty,
then there are no variable-value bindings to perform. The state 𝑠 remains unchanged, and the result
follows immediately from the assumption that 𝑠 is well-formed. Inductive case. Suppose the lists
are of the form 𝑥 = 𝑥 1 :: 𝑥𝑛 and 𝑣 = 𝑣 1 :: 𝑣𝑛 . By the well-formedness of the state 𝑠 =≺ 𝑠 Δ, 𝑠 Ω , Θ ≻,
we know that there exists a location 𝑙 and a type 𝜏1 such that 𝑠 Ω [𝑥 1 ] = (𝑙, 𝜏1 ), Σ 𝑙 = 𝜏1 , and the
memory Θ allows a valid write access at location 𝑙. Therefore, assigning 𝑣 1 to location 𝑙 yields an
updated memory Θ1 , which remains well-formed due to the assumptions on the typing and access
validity of 𝑙. We now apply the induction hypothesis to the remaining lists 𝑥𝑛 and 𝑣𝑛 , using the
intermediate well-formed state ≺ 𝑠 Δ, 𝑠 Ω , Θ1 ≻. This yields a final store Θ′ obtained by assigning the
remaining values 𝑣𝑛 to the corresponding variables 𝑥𝑛 , such that the resulting state ≺ 𝑠 Δ, 𝑠 Ω , Θ′ ≻
is well-formed. Therefore, after successively updating the memory for all variable-value pairs, we
obtain a final memory Θ′ such that the entire state remains well-formed.                                □

  Lemma 18 states that substitution of a value 𝑣 for a variable 𝑥 in the expression 𝑒 preserves the
type and subsumption rule for the effects. It is important to observe that substitution semantics
accounts for the effect associated with the expression 𝑒. However, when e evaluates to a value
prior to substitution, its effect is no longer present in the substituted expression. As a result, the

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                                33


conclusion must allow for a potential drop in effects, and we apply a subsumption rule on effects
rather than requiring exact equality.


   Lemma 18 (subst preserve typing).
               ∀Γ, Σ, 𝑥, 𝑒, 𝑒 ′, 𝜏, 𝜂, 𝜏 ′, 𝜂 ′ . (𝑥 → 𝜏, Γ), Σ, Π, Ψ ⊢ 𝑒 ′ : 𝜏 ′, 𝜂 ′ ∧ Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 =⇒
                                            ∃𝜂 ′′, Γ, Σ, Π, Ψ ⊢ 𝑒 ′ [𝑥 ← 𝑒] : 𝜏 ′, 𝜂 ′′ ∧ 𝜂 ′′ ⊆ (𝜂 ∔ 𝜂 ′ )

    Proof. The proof follows by doing induction on the structure of e. We discuss interesting cases
in detail.
    Var case. (i) 𝑥 = 𝑦. In this case, the variable 𝑦 is substituted with the value 𝑣. From the assumptions,
we have Γ ⊢ 𝑣 : 𝜏, and the typing environment includes 𝑥 : 𝜏. The expression 𝑦 typechecks in
the extended environment (𝑥 → 𝜏, Γ), which implies that 𝑦 has type 𝜏 ′ = 𝜏, since 𝑥 = 𝑦. After
substitution, the resulting expression is 𝑣, which has type 𝜏 ′ as required. For the effects, since 𝑣 is
a value, we instantiate 𝜂 ′′ with the empty effect 𝜙, and since the empty effect is a subeffect of all
other effects, we conclude that 𝜂 ′′ ⊆ (𝜂 ∔ 𝜂 ′ ). Thus, the substitution preserves both typing and
effects. (ii) 𝑥 ≠ 𝑦. In this case, no substitution occurs, and the resulting expression remains 𝑦. From
the assumption, we know that Γ ⊢ 𝑦 : 𝜏 ′ . Therefore, the type of the substituted expression is still 𝜏 ′ .
The effect 𝜂 ′′ is instantiated as 𝜂 ′ , and by the definition of effect subsetting, 𝜂 ′ ⊆ (𝜂 ∔ 𝜂 ′ ). Hence,
typing and effect preservation hold in this case as well.
    Function application In the case of function application 𝑓 𝑛(𝑒𝑠), we first apply the induction
hypothesis to show that substitution preserves the typing of each argument in the list 𝑒𝑠. Using
these results, along with the typing rule for function application, we conclude that the entire
expression 𝑓 𝑛(𝑒𝑠) remains well-typed after substitution.
    Ref, Deref and Memory assignment case. The proof proceeds by applying the induction hypothesis
and appropriately instantiating the effect 𝜂 ′′ : with alloc :: 𝜂 ′ in the case of ref, read :: 𝜂 ′ in the case
of deref, and 𝜂 ′ :: alloc in memory assignment, ensuring that the resulting effect annotations are
correctly preserved. Uop, Bop, and Cond case. The proof is trivial and utilizes induction hypothesis.
    Let-binding case. For the let-binding expression let 𝑦 : 𝜏 = 𝑒 1 in 𝑒 2 , corresponding to the typing
rule TLET, the proof proceeds in a manner similar to the variable case. We perform a case analysis
on whether 𝑦 = 𝑥 or 𝑦 ≠ 𝑥. In both cases, we apply the induction hypothesis to the subexpressions
𝑒 1 and 𝑒 2 as needed. The effect 𝜂 ′′ is instantiated with the appropriate effect composition for the
TLET rule. This ensures that the substituted expression remains well-typed.
    Field access. In the case of field access 𝑒.𝑓 , substitution only applies to the subexpression 𝑒. By
applying the induction hypothesis to 𝑒, and reapplying the typing rule TFIELD, we conclude that
the substituted expression 𝑒 [𝑥 ← 𝑠𝑒].𝑓 remains well-typed, with the effect preserved as a subeffect
of the original.
    Struct initialization. In the case of struct initialization 𝑦|(𝑓 , 𝑒), we proceed by case analysis on
whether 𝑦 = 𝑥 or 𝑦 ≠ 𝑥.Case 𝑦 = 𝑥: The variable 𝑦 bound in the struct initialization shadows
the variable 𝑥 targeted by the substitution. Therefore, no substitution takes place within the list
of expressions 𝑒. Since the original typing derivation holds and substitution does not alter the
expression, the type is preserved. The effect is instantiated with the effect of the field initializers 𝑒,
and the typing follows by applying the rule TSINIT. Case 𝑦 ≠ 𝑥: In this case, substitution proceeds
recursively into each initializer 𝑒𝑖 ∈ 𝑒. By applying the induction hypothesis to each 𝑒𝑖 , we obtain
the corresponding typing and effect preservation. Reapplying the rule TSINIT to the substituted
list establishes the preservation of the overall expression.
    For-loop Substitution is applied to all three subexpressions 𝑒 1, 𝑒 2, 𝑒 of a for-loop for (𝑒 1 . . . 𝑒 2, 𝑑) 𝑒,
and the direction 𝑑 variable is assumed not to interfere with the substitution variable 𝑥. By applying

                                                                           , Vol. 1, No. 1, Article . Publication date: July 2026.
34


the induction hypothesis to 𝑒 1 , 𝑒 2 , and 𝑒, we obtain that each substituted subexpression is well-
typed with preserved or reduced effects. Reapplying the typing rule TFOR, we conclude that the
substituted loop remains well-typed, and the total effect is preserved under subsumption rule for
effects. None and Some case For the None case, the substitution has no effect; hence type and effects
are preserved. For the Some case, the induction hypothesis and the rule TSOME is used to discharge
the goal.
   Match case We consider the expression match 𝑒 with 𝑝 1 ⇒ 𝑒 1 | . . . | 𝑝𝑛 ⇒ 𝑒𝑛 , with typing
judgment Γ, 𝑥 : 𝜏 ⊢ match 𝑒 with 𝑝 1 ⇒ 𝑒 1 | . . . | 𝑝𝑛 ⇒ 𝑒𝑛 : 𝜏𝑟 , 𝜂. Let the effect be 𝜂 = 𝜂𝑒 ∔𝜂 1 ∔· · ·∔𝜂𝑛 ,
where: Γ, 𝑥 : 𝜏 ⊢ 𝑒 : option 𝜏 ′, 𝜂𝑒 . For each branch 𝑖, Γ𝑖 = Γ, 𝑥 : 𝜏 ∪ binds(𝑝𝑖 ) ⊢ 𝑒𝑖 : 𝜏𝑟 , 𝜂𝑖 We proceed
by case analysis on whether the pattern 𝑝𝑖 binds 𝑥.(i) Apply the induction hypothesis to the matched
expression 𝑒. We obtain: Γ ⊢ 𝑒 [𝑥 ← 𝑠𝑒] : option 𝜏 ′, 𝜂𝑒′ with 𝜂𝑒′ ⊆ 𝜂𝑒 ∔ 𝜂𝑠𝑒 (ii) For each branch
𝑖, we consider the pattern 𝑝𝑖 and the branch body 𝑒𝑖 . If 𝑥 ∉ binds(𝑝𝑖 ), we apply the induction
hypothesis: Γ ∪ binds(𝑝𝑖 ) ⊢ 𝑒𝑖 [𝑥 ← 𝑠𝑒] : 𝜏𝑟 , 𝜂𝑖′ with 𝜂𝑖′ ⊆ 𝜂𝑖 ∔ 𝜂𝑠𝑒 If 𝑥 ∈ binds(𝑝𝑖 ), then 𝑥 is
shadowed, and substitution does not apply in 𝑒𝑖 , so: Γ ∪ binds(𝑝𝑖 ) ⊢ 𝑒𝑖 : 𝜏𝑟 , 𝜂𝑖 ⇒ 𝜂𝑖′ = 𝜂𝑖 (iii) By
reapplying the TMATCH rule, we derive:Γ ⊢ match 𝑒 [𝑥 ← 𝑠𝑒] with 𝑝 1 ⇒ 𝑒 1′ | . . . | 𝑝𝑛 ⇒ 𝑒𝑛′ : 𝜏𝑟 , 𝜂 ′
where 𝜂 ′ = 𝜂𝑒′ ∔ 𝜂 1′ ∔ · · · ∔ 𝜂𝑛′ , and by construction:𝜂 ′ ⊆ (𝜂𝑒 ∔ 𝜂 1 ∔ · · · ∔ 𝜂𝑛 ) ∔ 𝜂𝑠𝑒 = 𝜂 ∔ 𝜂𝑠𝑒 Thus,
substitution preserves both typing and effects.                                                              □

     Lemma 19. [Progress]
             ∀Γ, Σ, Π, Ψ, 𝑒𝑠, 𝜂𝑠 , 𝜏𝑠 , 𝑠.   Γ, Σ, Π, Ψ ⊩ 𝑒𝑠 : 𝜏𝑠 , 𝜂𝑠 ∧ well formed state(Γ, Σ, 𝑠) =⇒
                                             isVal 𝑒𝑠 ∨ ∃𝑠 ′, 𝑒𝑠 ′ . 𝑠, 𝑒𝑠 ↣ 𝑠 ′, 𝑒𝑠 ′ ∧ well formed state(Γ, Σ, 𝑠 ′ )
              ∧ ∀Γ, Σ, Π, Ψ, 𝑒, 𝜂, 𝜏, 𝑠.     Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠) =⇒
                                             isVal 𝑒 ∨ ∃𝑠 ′, 𝑒 ′ . 𝑠, 𝑒 → 𝑠 ′, 𝑒 ′ ∧ well formed state(Γ, Σ, 𝑠 ′ )

  Proof. The proof proceeds by mutual induction on the structure of expressions and expression
sequences, considering each form of expression and demonstrating that they either are values
or can progress to the next state. Below, we present the proof for the case of a single expression.
The case for a sequence of expressions follows similarly, by applying the induction hypothesis
recursively at each step of the sequence.
Variable case When evaluating a variable expression 𝑥, we distinguish between two cases based
on the scope of the variable: local and global. From the typing rule (TVAR), we know that the
environment Γ maps 𝑥 to a type 𝜏, i.e., Γ(𝑥) = 𝜏. The well-formedness of the state 𝑠 ensures that
the variable 𝑥 appears either in the local environment Ω or in the global environment Δ.
  • If 𝑥 ∈ dom(Ω), then there exists a location 𝑙 such that Ω(𝑥) = (𝑙, 𝜏), and by the well-formedness
    of memory, we have Σ(𝑙) = 𝜏 and 𝑠 Θ [𝑙, 𝑜] = 𝑣 for some offset 𝑜 and value 𝑣 with typeof (𝑣) = 𝜏.
  • If 𝑥 ∉ dom(Ω), then 𝑥 must be a global variable, and we have Δ(𝑥) = 𝑙 for some location 𝑙. By
    well-formedness, Σ(𝑙) = 𝜏 and there exists 𝑜 and 𝑣 such that 𝑠 Θ [𝑙, 𝑜] = 𝑣 and typeof (𝑣) = 𝜏.
In both cases, the evaluation of 𝑥 yields the value 𝑣 without modifying the state 𝑠, and the resulting
state remains well-formed. The proof for constant expressions is straightforward, as constants
evaluate to themselves with the same type and do not affect the state.
Ref Case. The evaluation of the expression ref 𝑒 proceeds by a case analysis:
  • Value case: If the inner expression of ref 𝑒 has reduced to a value 𝑣, then by the typing rule
    (TREF) and the well-formedness of the current state 𝑠, Lemma 15 ensures that a fresh memory
    location 𝑙 is successfully allocated and it is safe to store the value 𝑣 at 𝑙. Moreover, Lemma 15
    guarantees that the resulting state 𝑠 ′ , obtained after allocation, remains well-formed. Therefore,
    the expression ref 𝑣 steps to a location 𝑙, as captured by the semantic rule (REFV). The subgoals

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                    35


    arising from this rule—such as memory consistency and typing of the allocated location—are
    discharged using the guarantees provided by Lemma 15.
  • Step case: By the induction hypothesis, the evaluation step 𝑒 → 𝑒 ′ preserves the well-formedness
    of the state. By the semantic rule (REF), we have: ref 𝑒 → ref 𝑒 ′ and the resulting state remains
    well-formed.
Dereference case. The evaluation of the expression !𝑒 proceeds by case analysis. From the typing
rule (TDEREF), we know that the type of 𝑒 must be of the form 𝜏∗, i.e., a pointer to type 𝜏, where
the pointer may originate either from the BeePL program or from the external environment. In
both cases, 𝑒 denotes a memory location 𝑙, and from the typing rule (TLOC) we obtain the judgment
Σ 𝑙 = 𝜏, ensuring that the location is well-typed in the store typing context Σ. Furthermore, from
the structure of the typing derivation using (TDEREF), it follows that the type of 𝑒 cannot be an
option type; such cases must be eliminated by a pattern match before dereference is allowed.
  • Value case: Inner expression of !𝑒 has reduced to a location 𝑙. We invoke Lemma 11, which,
    under the assumption that the state 𝑠 is well-formed, guarantees the existence of a value 𝑣
    such that 𝑠 Θ [𝑙] = 𝑣 and typeof(𝑣) = 𝜏. Thus, 𝑠, !𝑒 → 𝑠, 𝑣 via the semantic rule (DEREFV). Since
    dereferencing does not modify the state, we have 𝑠 ′ = 𝑠, and the well-formedness of the state is
    preserved.
  • Step case: By the induction hypothesis, the evaluation step 𝑒 → 𝑒 ′ preserves the well-formedness
    of the state. Applying the semantic rule (DEREF), we derive that 𝑠, !𝑒 → 𝑠 ′, !𝑒 ′ , and since the
    well-formedness is preserved in the step from 𝑒 to 𝑒 ′ , it follows that the overall evaluation of !𝑒
    maintains the invariant that the state remains well-formed.
   Memory assignment case. The proof for memory assignment proceeds in a similar manner, using
Lemma 12 to handle the case where both 𝑒 1 and 𝑒 2 in the assignment expression 𝑒 1 := 𝑒 2 have been
reduced to values. And for the case where they are not values, we utilize the induction hypothesis.
   Unary operators case. The proof for unary operations relies on Lemma 9, which handles the
case where the operand of the operator has already reduced to a value. According to this lemma,
a well-typed unary operation always makes progress. Moreover, since unary operations do not
modify the program state, the well-formedness of the state is preserved after evaluation. For the
case where the operand has not yet reduced to a value, we apply the induction hypothesis to
complete the proof.
   Binary operator case. The proof for binary operations relies on Lemma 10, which handles the
case where the operands of the operator has already reduced to a value. According to this lemma,
a well-typed binary operation always makes progress. Moreover, since binary operations do not
modify the program state, the well-formedness of the state is preserved after evaluation. For the
case where the operands have not yet reduced to values, we apply the induction hypothesis to
complete the proof.
   Let-binding case. We consider the expression let 𝑥 : 𝜏 = 𝑒 1 in 𝑒 2 . The evaluation proceeds by case
analysis on whether 𝑒 1 is a value.
  • Case 1: 𝑒 1 = 𝑣 for some value 𝑣. In this case, the evaluation rule (LETV) applies, and the let-
    binding expression reduces as follows: let 𝑥 : 𝜏 = 𝑣 in 𝑒 2 → 𝑒 2 [𝑥 ← 𝑣]. By unfolding the
    definition of substitution, we obtain the resulting expression 𝑒 2′ := 𝑒 2 [𝑥 ← 𝑣], which serves as
    the witness for the progress step. Since the substitution does not alter the memory state, we
    have 𝑠 ′ = 𝑠, and the well-formedness of the state is preserved.
  • Case 2: 𝑒 1 → 𝑒 1′ . By the induction hypothesis applied to 𝑒 1 , there exists an expression 𝑒 1′ and a
    state 𝑠 ′ such that:(𝑠, 𝑒 1 ) → (𝑠 ′, 𝑒 1′ ) and well formed state(Γ, Σ, 𝑠 ′ ) We then apply the semantic
    rule (LET) to conclude:𝑠, let 𝑥 : 𝜏 = 𝑒 1 in 𝑒 2 → 𝑠 ′, let 𝑥 : 𝜏 = 𝑒 1′ in 𝑒 2 Hence, the let-binding
    expression makes progress, and the resulting state remains well-formed.

                                                               , Vol. 1, No. 1, Article . Publication date: July 2026.
36


    Cond case. The typing rule TCOND ensures that the condition expression has type bool and that
both branches have the same type, preserving type consistency. The proof involves three cases.
The first two cases correspond to when the condition has already reduced to a boolean value: If the
condition 𝑒 1 has evaluated to true, then the conditional expression if 𝑒 1 then 𝑒 2 else 𝑒 3 reduces to
𝑒 2 by applying the rule CONDT. If 𝑒 1 has evaluated to false, the expression reduces to 𝑒 3 using the
rule CONDF. In both cases, the program state remains unchanged, and thus the well-formedness
of the state is preserved. The third case addresses when the condition 𝑒 1 has not yet reduced to a
value. In this case, the expression takes a step to if 𝑒 1′ then 𝑒 2 else 𝑒 3 by applying the rule COND,
where 𝑒 1′ is obtained from the induction hypothesis. By the induction hypothesis, we know that the
state after evaluating 𝑒 1 remains well-formed.
    Function application case. The proof for function application proceeds by considering following
cases.
  • Case 1: The function 𝑓 𝑛 is applied to a list of fully evaluated values 𝑣. From the typing rule
    TAPP, we know that the function 𝑓 𝑛 has an arrow type. Moreover, from the definition of
    well-formedness of the state 𝑠 (as specified in Definition 4.1), a well-typed function must be
    declared in the environment Δ. The number of arguments provided in the application must
    match the number declared in the function signature, and their types must align with the
    expected parameter types. In this case, the function application reduces to the function body, as
    specified in the declaration of 𝑓 𝑛. This transition is captured by the rule APP3, which produces
    several subgoals related to memory allocation for local variables and binding of parameters
    to the argument values. These subgoals are discharged using Lemma 16, which ensures that
    the allocation of function-local variables preserves well-formedness, and Lemma 17, which
    guarantees that binding argument values to parameters results in a well-formed store.
  • Remaining cases: If some of the arguments to the function application are not yet fully evaluated,
    we use the induction hypothesis to show that the evaluation of these arguments progresses,
    preserving the well-formedness of the state.
     Struct initialization and field access case.We consider two subcases for struct initialization.
  • Case 1: All expressions 𝑒 to be assigned to the struct fields are fully evaluated to values
    𝑣. From the well-formedness condition of the state, we know that every well-typed struct
    variable must be declared in the environment Π. Using this fact, we extract the field layout
    information—specifically, the memory location and offset associated with each field name—and
    assign each value 𝑣𝑖 ∈ 𝑣 to the corresponding memory position. By Lemma 12, we ensure that
    each write to memory is safe and that the resulting state 𝑠 ′ remains well-formed.
  • Case 2: Some expressions 𝑒𝑖 ∈ 𝑒 have not yet reduced to values.
    In this case, we apply the induction hypothesis to show that each such 𝑒𝑖 can take a step 𝑒𝑖 → 𝑒𝑖′
    in a well-formed state. By applying the evaluation rule for struct initialization and appealing to
    the preservation of well-formedness under expression evaluation, we discharge the subgoal.
   Struct Field Access. To access a field 𝑓 of a struct variable 𝑥, we use the typing judgment to
establish that 𝑥 is well-typed and declared in the environment Π. By the well-formedness of the
state, we extract the memory location and offset of field 𝑓 . Then, by applying Lemma 11, we read
the value at the specified location and offset, guaranteeing that the operation is safe and that the
state remains well-formed.
   For-loop case. We consider the evaluation of the expression For(𝑒 1 . . . 𝑒 2, 𝑑) 𝑒 by performing case
analysis on the evaluation status of the bound expressions 𝑒 1 and 𝑒 2 .
  • Case 1: 𝑒 1 is not a value. From the typing rule (TFOR), we know that 𝑒 1 is well-typed with type
    𝜏 ∈ {int, long}. By the induction hypothesis, the expression 𝑒 1 satisfies progress; hence, there

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                                      37


     exists 𝑒 1′ and an updated state 𝑠 ′ such that:𝑠, 𝑒 1 → 𝑠 ′, 𝑒 1′ Applying the evaluation rule (FOR1),
     we derive:𝑠, For(𝑒 1 . . . 𝑒 2, 𝑑) 𝑒 → 𝑠 ′, For(𝑒 1′ . . . 𝑒 2, 𝑑) 𝑒
  • Case 2: 𝑒 1 is a value, but 𝑒 2 is not. From the typing derivation, we similarly know that 𝑒 2 is well-
     typed. By the induction hypothesis, 𝑒 2 satisfies progress, so there exists 𝑒 2′ and an updated state
     𝑠 ′ such that:𝑠, 𝑒 2 → 𝑠 ′, 𝑒 2′ . Applying the evaluation rule (FOR2), we derive:𝑠, For(𝑣 1 . . . 𝑒 2, 𝑑) 𝑒 →
     𝑠 ′, For(𝑣 1 . . . 𝑒 2′ , 𝑑) 𝑒 In both cases, the updated state 𝑠 ′ remains well-formed by the induction
     hypothesis.
  • Case 3: Both 𝑒 1 and 𝑒 2 are values. Let 𝑣 1 = 𝑒 1 , 𝑣 2 = 𝑒 2 , and consider the expression:For(𝑣 1 . . . 𝑣 2, 𝑑) 𝑒
     From the typing rule (TFOR), we have typeof(𝑣 1 ) = typeof(𝑣 2 ) = 𝜏, where 𝜏 ∈ {int, long}, and
     that the loop body 𝑒 is well-typed independently of 𝑒 1 and 𝑒 2 . Specifically, the rule enforces:
     fvar(𝑒) ∩ fvar(𝑒 1 ) = 𝜙 and fvar(𝑒) ∩ fvar(𝑒 2 ) = 𝜙 ensuring that the loop bounds do not
     appear free in the loop body. Thus, the evaluation of 𝑒 is unaffected by the values of 𝑣 1 and
     𝑣 2 , and once the bounds are fully evaluated, the loop can be unrolled. Let range(𝑣 1, 𝑣 2, 𝑑) = 𝑛
     denote the total number of iterations, and let repeat(𝑒, 𝑛) = 𝑒 ′ denote the sequential unrolling
     of 𝑒 repeated 𝑛 times. The evaluation proceeds via the rule (FOR3):For(𝑣 1 . . . 𝑣 2, 𝑑) 𝑒 −→ 𝑒 ′
   None and Some case. The proof for the None and Some 𝑣 case is straight-forward as it does not
alter the state and is a value; hence preserves the well-formedness of the state. For the case where
𝑒 in Some 𝑒 steps to 𝑒 ′ , the proof follows from the induction hypothesis.
   Match case. We proceed by case analysis on the structure of the expression 𝑒 0 in the match
expression match 𝑒 0 with 𝑝 → 𝑒. If 𝑒 0 is not a value, then by the induction hypothesis, there
exists 𝑒 0′ and 𝑠 ′ such that 𝑠, 𝑒 0 → 𝑠 ′, 𝑒 0′ . In this case, we apply rule Match1 to conclude that
𝑠, match 𝑒 0 with 𝑝 → 𝑒 → 𝑠 ′, match 𝑒 0′ with 𝑝 → 𝑒.
   If 𝑒 0 is a value, we proceed by analyzing its form. If 𝑒 0 = Some 𝑣, then since isSome(𝑣) holds and
the pattern list contains a clause of the form (Psome 𝑥, 𝑒 2 ), rule MSOME applies, and we take the
step to 𝑠, 𝑒 2 [𝑥 ← 𝑣]. If 𝑒 0 = None, and the pattern list contains a clause (Pnone, 𝑒 1 ), we apply rule
MNONE to step to 𝑠, 𝑒 1 .
   If 𝑒 0 = 𝑣 and typeof(𝑣) = bytes, we further distinguish based on the size of the byte sequence. If
length(𝑣) ≥ sizeof (𝜏𝑥 ), and the pattern list contains a clause ((𝑥, 𝜏𝑥 ), 𝑒 1 ), then the byte extraction
succeeds, and by rule MBYTES, we step to (𝑒 1 [𝑦𝑖 ↦→ 𝑣𝑖 , 𝑥 ↦→ 𝑣 𝑥 ], 𝑠). Otherwise, if length(𝑣) <
sizeof (𝜏𝑥 ), rule MBYTESF applies, and the evaluation steps to the fallback clause 𝑒 2 , yielding 𝑠, 𝑒 2 .
This completes the case analysis for all possible forms of the match expression. In each case, we
have shown that the expression either takes a step or is already a value (which does not apply for
match), thereby establishing the progress property.
   This completes the case analysis for all expression forms in the language. In each case, we have
shown that a well-typed expression is either a value or can take a step according to the operational
semantics, and that the state remains well-formed. Therefore, the progress property holds for all
well-typed expressions of BeePL.                                                                                    □
   Lemma 20. [Preservation]
   ∀Γ, Σ, Π, Ψ, 𝑒𝑠, 𝑒𝑠 ′, 𝜂𝑠 , 𝜏𝑠 , 𝑠, 𝑠 ′ .   Γ, Σ, Π, Ψ ⊩ 𝑒𝑠 : 𝜏𝑠 , 𝜂𝑠 ∧ well formed state(Γ, Σ, 𝑠) ∧ 𝑠, 𝑒𝑠 ↣ 𝑠 ′, 𝑒𝑠 ′ =⇒
                                               ∃𝜂𝑠′ . Γ, Σ, Π, Ψ ⊩ 𝑒𝑠 ′ : 𝜏𝑠 , 𝜂𝑠′ ∧ 𝜂𝑠′ ⊆ 𝜂𝑠 ∧ well formed state(Γ, Σ, 𝑠 ′ )
     ∧ ∀Γ, Σ, Π, Ψ, 𝑒, 𝑒 ′, 𝜂, 𝜏, 𝑠, 𝑠 ′ .     Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠) ∧ 𝑠, 𝑒 → 𝑠 ′, 𝑒 ′ =⇒
                                               ∃𝜂 ′ . Γ, Σ, Π, Ψ ⊢ 𝑒 ′ : 𝜏, 𝜂 ′ ∧ 𝜂 ′ ⊆ 𝜂 ∧ well formed state(Γ, Σ, 𝑠 ′ )

   Proof. The proof follows by doing induction on the typing derivation Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 of
expression. Below, we present the proof for the case of a single expression. The case for a sequence
of expressions follows similarly, by applying the induction hypothesis recursively at each step of
the sequence. We discuss some of the interesting cases here:

                                                                                 , Vol. 1, No. 1, Article . Publication date: July 2026.
38


   Var case. The semantics of variable access distinguishes between local and global variables. This
distinction determines how the variable 𝑥 is looked up—either in the local environment 𝑠 Ω or the
global environment 𝑠 Δ —to retrieve the memory location 𝑙 to which it is bound. Once the location 𝑙
is obtained, the variable is dereferenced to retrieve the corresponding value 𝑣 from the memory
state 𝑠 Θ , i.e., 𝑠 Θ [𝑙] = 𝑣 By the property of well-typed dereferencing (as guaranteed by the typing
rule (TVAR) and the store typing context Σ), we have Σ(𝑙) = 𝜏 and typeof(𝑣) = 𝜏. Therefore, the
resulting expression has type 𝜏. The effect associated with variable access is 𝜙, and since 𝜙 ⊆ 𝜂 for
any effect 𝜂, subsumption holds. Furthermore, the operational semantics for variable access does
not modify the state:𝑠 ′ = 𝑠 and hence, the well-formedness of the state is preserved.
   Ref case. Consider the expression ref 𝑒 and the typing rule (TREF), which assigns it the type 𝜏∗,
assuming that 𝑒 has type 𝜏. We proceed by case analysis on the evaluation of 𝑒.
  • Case 1: 𝑒 → 𝑒 ′ . By the induction hypothesis, we obtain:Γ, Σ, Π, Ψ ⊢ 𝑒 ′ : 𝜏, 𝜂 ′ with 𝜂 ′ ⊆ 𝜂 and the
     updated state 𝑠 ′ satisfies well formed state(Γ, Σ, 𝑠 ′ ). We then reapply the typing rule (TREF)
     to derive:Γ, Σ, Π, Ψ ⊢ ref 𝑒 ′ : 𝜏∗, alloc :: 𝜂 ′ which establishes the preservation of typing for ref 𝑒 ′
     under evaluation.
  • Case 2: 𝑒 = 𝑣, where 𝑣 is a value. In this case, by the operational semantics rule (REFV), the expres-
     sion ref 𝑣 allocates a fresh memory location 𝑙, initializes it with the value 𝑣, and yields:ref 𝑣 → 𝑙.
     We solve this goal by applying the rule (TLOC), which generates the subgoal: Σ(𝑙) = 𝜏. From the
     assumption that the original state 𝑠 is well-formed, and by the semantics of ref, we know that
     𝑙 is a newly allocated and initialized location. This means isValidAccess(𝑠 Θ, 𝑙, Freeable) holds.
     By the third clause of the well-formedness definition (Definition 4.1), such valid allocations
     are properly reflected in Σ, ensuring: Σ(𝑙) = 𝜏. Moreover, by Lemma 15, the updated state 𝑠 ′ ,
     after allocation, remains well-formed. Hence, preservation holds in this case as well. In terms
     of effect, location does not produce any effect; hence it will always be sub-effect of the effect
     associated with original ref construct.
   Deref case. Consider the dereference expression !𝑒. We proceed by case analysis on the evaluation
of 𝑒.
  • Case 1: 𝑒 → 𝑒 ′ . By the induction hypothesis, there exists an updated state 𝑠 ′ such that: 𝑠, 𝑒 →
     𝑠 ′, 𝑒 ′ and Γ, Σ, Π, Ψ ⊢ 𝑒 ′ : 𝜏 ∗, 𝜂 ′ with 𝜂 ′ ⊆ 𝜂, and well formed state(Γ, Σ, 𝑠 ′ ). Applying the rule
     (TDEREF), we obtain:Γ, Σ, Π, Ψ ⊢!𝑒 ′ : 𝜏, read :: 𝜂 ′ Since 𝜂 ′ ⊆ 𝜂, we conclude: read :: 𝜂 ′ ⊆ read :: 𝜂.
     Thus, preservation holds in this case.
  • Case 2: 𝑒 = 𝑙, where 𝑙 is a valid memory location, and !𝑒 → 𝑣. By the operational semantics of
     dereferencing, the value stored at 𝑙 is retrieved: 𝑠 Θ [𝑙] = 𝑣. By Lemma 11 and the well-formedness
     of the state 𝑠, we have: Σ(𝑙) = 𝜏 and typeof (𝑣) = 𝜏 Hence, Γ, Σ, Π, Ψ ⊢ 𝑣 : 𝜏, 𝜙 Since 𝜙 ⊆ read ::𝜂,
     the effect condition is satisfied. Furthermore, since dereferencing does not modify the memory:
     𝑠 ′ = 𝑠, well formed state(Γ, Σ, 𝑠 ′ )is preserved.
   Memory assignment. Preservation for memory assignment expressions of the form 𝑒 1 := 𝑒 2
follows a similar structure. In cases where 𝑒 1 and 𝑒 2 are not yet fully evaluated, the proof proceeds
analogously to Case 1 of the deref and ref constructs, relying on the induction hypothesis for the
subexpressions. When 𝑒 1 evaluates to a location 𝑙 1 and 𝑒 2 evaluates to a value 𝑣 2 , the resulting
expression is unit. Type preservation holds in this case as well, since the type of the entire assignment
expression 𝑒 1 := 𝑒 2 is unit𝜏 , matching the type of the result. The effect will be 𝜙, which is a subeffect
of the original effect. The well-formedness of the updated state is guaranteed through lemma 12.
   Let-binding. For the case, where 𝑒 1 is not yet a value and can still take a reduction step, we
proceed exactly as in the earlier cases, invoking the induction hypothesis to obtain the desired
preservation properties. For the case, where 𝑒 1 is fully evaluated and has reduced to a value 𝑣
in let 𝑥 : 𝜏 = 𝑒 1 in 𝑒 2 . According to the semantic rule LETV, let-binding steps to 𝑒 2 [𝑥 ← 𝑣]. By

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                    39


applying the lemma Subst preserve typing 18 to the original typing derivation, we obtain that
the substituted expression 𝑒 2 [𝑥 ← 𝑣] is also well-typed. Because this reduction leaves the store
unchanged, the well-formedness of the current state is preserved.
  For loop. For the case of for-loop for (𝑒 1 . . . 𝑒 2, 𝑑) 𝑒, we discuss the whole proof in two categories:
 • Sub-expressions are not fully evaluated. If one of the subexpressions has not reduced to a value, we
   invoke the induction hypothesis for that sub-expression, exactly as in the let-binding and other
   structural cases, to obtain both subject reduction and preservation of state well-formedness.
 • All control parameters are values. if 𝑒 1 and 𝑒 2 has reduced to 𝑣 1 and 𝑣 2 , the semantic rule
   FORV ensures range(𝑣 1, 𝑣 2, 𝑑) = 𝑛 ∧ 𝑠 , repeat(𝑒, 𝑛) → 𝑠 ′, 𝑣. The premise 𝑠, repeat(𝑒, 𝑛) → 𝑠 ′, 𝑣
   together with the induction hypothesis for the body 𝑒 (applied 𝑛 times) implies that 𝑣 has type
   𝜏 and the final store 𝑠 ′ is well formed.
   Struct Initialization and Field Access. For both struct initialization and field access, the key invariant
rely on is the well-formedness of struct declarations. By the definition of state well-formedness
(Definition 4.1), any struct used in a program must be declared in the composite environment Π,
and its declaration must type check under the typing context Γ (as stated in the last clause of the
definition). This ensures that the types of all struct fields are known and consistent throughout the
program. As a result:
 • Struct Initialization. The initialization of a struct preserves the type, since it simply associates
   values with the statically declared field types and does not modify the declared structure or
   type. The initialization of a struct’s fields results in updates to memory. Since the struct is
   already declared in the composite environment Π, the corresponding memory locations for its
   fields are guaranteed to be valid. By Lemma 12, any assignment to a valid memory location
   succeeds and preserves state well-formedness. Therefore, the field-wise initialization of the
   struct not only succeeds but also results in a well-formed updated state.
 • Field Access. Accessing a field reduces the expression to the value stored in the corresponding
   field of the struct. The field’s type must match the declaration in Π, ensuring that the result is
   well-typed. Field access does not change the state; hence the well-formedness of the state is
   preserved.
     Match. For the match case, where the sub-expressions are not fully reduced to value, we invoke
the induction hypothesis for that sub-expression, exactly as in the other structural cases, to obtain
both subject reduction and preservation of state well-formedness.
     For the case where 𝑒 has reduced to Some 𝑣, match 𝑒 with 𝑝 → 𝑝𝑒, we know according to the
rule MSOME that it reduces to 𝑒 2 [𝑥 ← 𝑣], where 𝑒 2 is the corresponding follow-up expression
for the pattern Psome. By applying the lemma Subst preserve typing 18 to the original typing
derivation, we obtain that the substituted expression 𝑒 2 [𝑥 ← 𝑣] is also well-typed. Because this
reduction leaves the store unchanged, the well-formedness of the current state is preserved. For the
case where 𝑒 evaluates to None, the evaluation of match 𝑒 with 𝑝 → 𝑝𝑒 proceeds to the expression
𝑒 1 , which is the follow-up expression for the pattern Pnone. We use the inductive hypothesis
corresponding to 𝑒 1 to discharge the goal.
     For the case where the type of 𝑒 in match 𝑒 with 𝑝 → 𝑝𝑒 in bytes and is reduced to a value 𝑣,
we have two cases to consider:
 • Given that typeof(𝑣) = bytes and its length is sufficient, the matched pattern (𝑥, 𝜏𝑥 ) : (𝑦, 𝜏 𝑦 )
   extracts values 𝑣 𝑥 and {𝑦𝑖 ↦→ 𝑣𝑖 }. The expression 𝑒 1 is typed under a context extended with
   𝑥 : 𝜏𝑥 , 𝑦𝑖 : 𝜏 𝑦 . By multiple applications of the substitution lemma, the substituted expression is
   well-typed. The state update is identity (𝑠 ′ = 𝑠), so it remains well-formed.

                                                               , Vol. 1, No. 1, Article . Publication date: July 2026.
40


 • The length check fails, so the fallback branch 𝑒 2 is selected. Since 𝑒 2 is one of the match branches,
    it is well-typed. No substitution or state update occurs, so both typing and well-formedness are
    preserved.
  For the match construct, we carefully instantiate the effect corresponding to the selected branch.
Since the typing rules ensure that each branch is typed with an effect that is no greater than the
overall effect of the match expression, the instantiated effect is guaranteed to be a sub-effect of the
original. Thus, effect subsumption holds by construction.                                               □
     To prove soundness we define a semantic closure for BeePL program as follows:

                                                     𝑠, 𝑒 → 𝑠, 𝑒                  𝑠, 𝑒 ↠𝑛 𝑠 ′ , 𝑒 ′ ∧ 𝑠 ′ , 𝑒 ′ → 𝑠 ′′ , 𝑒 ′′
                                      SZERO                           SMULTI
                                                     𝑠, 𝑒 ↠0 𝑠, 𝑒                           𝑠, 𝑒 ↠𝑛+1 𝑠 ′′ , 𝑒 ′′

                                               𝑠, 𝑒𝑠 ↣ 𝑠, 𝑒𝑠                      𝑠, 𝑒𝑠 ⇝𝑛 𝑠 ′ , 𝑒𝑠 ′ ∧ 𝑠 ′ , 𝑒𝑠 ′ ↣ 𝑠 ′′ , 𝑒𝑠 ′′
                               SZEROS                                SMULTIS
                                               𝑠, 𝑒𝑠 ⇝0 𝑠, 𝑒𝑠                                𝑠, 𝑒𝑠 ⇝𝑛+1 𝑠 ′′ , 𝑒𝑠 ′′


                                                     Fig. 16. Semantics closures for expressions.


   The relation ↠ and ⇝ defines the multi-step evaluation (semantic closure) of expressions and
expression lists, parameterized by a natural number 𝑛 that records the number of steps taken to
reach the final state. The rules SONE and SONES capture a single-step evaluation, while SMULTI
and SMULTIS recursively compose multiple steps, incrementing 𝑛 to reflect the total number of
steps.
   The soundness lemma 21 states that if an expression (or sequence) is well-typed and the state
is well-formed, then its evaluation to a final expression (or sequence) must result in a value. This
guarantees that well-typed programs do not get stuck during execution.

     Lemma 21 (Soundness).
     ∀Γ, Σ, Π, Ψ, 𝑒𝑠, 𝑒𝑠 ′ , 𝑠, 𝑠 ′ , 𝜂𝑠 , 𝜏𝑠 , 𝑛.    Γ, Σ, Π, Ψ ⊩ 𝑒𝑠 : 𝜏𝑠 , 𝜂𝑠 ∧ well formed state(Γ, Σ, 𝑠 ) ∧ 𝑠, 𝑒𝑠 ⇝𝑛 𝑠 ′ , 𝑒𝑠 ′ ∧ 𝑒𝑠 ′ ↣
                                                                                                                                           ̸
                                                =⇒ isVal 𝑒𝑠 ′ ∧ ∃𝜂𝑠′ . Γ, Σ, Π, Ψ ⊩ 𝑒𝑠 ′ : 𝜏𝑠 , 𝜂𝑠′ ∧ 𝜂𝑠′ ⊆ 𝜂𝑠 ∧ well formed state(Γ, Σ, 𝑠 ′ )

     ∀Γ, Σ, Π, Ψ, 𝑒, 𝑒 ′ , 𝑠, 𝑠 ′ , 𝜂, 𝜏, 𝑛.    Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠 ) ∧ 𝑠, 𝑒 ↠𝑛 𝑠 ′ , 𝑒 ′ ∧ 𝑒 ′ ↛
                                                        =⇒ isVal 𝑒 ′ ∧ ∃𝜂 ′ . Γ, Σ, Π, Ψ ⊢ 𝑒 ′ : 𝜏, 𝜂 ′ ∧ 𝜂 ′ ⊆ 𝜂 ∧ well formed state(Γ, Σ, 𝑠 ′ )

   Proof. The proof follows by doing induction on the number of steps 𝑛.
  • n = 0: By definition of multi-step evaluation SZERO, we know 𝑠 = 𝑠 ′ and 𝑒 = 𝑒 ′ . Given:
    Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 and well formed state(Γ, Σ, 𝑠), we invoke the progress lemma 19, which
    states that either: isVal(𝑒) or there exists 𝑠 1 and 𝑒 1 to which it steps to. If 𝑒 is already a value, the
    result follows directly by instantiating 𝜂 ′ = 𝜂, and the type and well-formedness is preserved
    as the state does not change. Otherwise, if 𝑒 can step, then we contradict the assumption
    𝑠, 𝑒 ↠0 𝑠, 𝑒, which disallows any step. Thus only the first case applies, and the base case holds.
  • 𝑛 = 𝑆 𝑛 ′ : By the definition of multi-step evaluation SMULTI, we know that there exist in-
    termediate state 𝑠 1 and expression 𝑒 1 such that: 𝑠, 𝑒 ↠𝑛 𝑠 1, 𝑒 1 and 𝑠 1, 𝑒 1 → 𝑠 ′, 𝑒 ′ . Now we
    apply preservation theorem inductively over each step in 𝑛 to obtain the two key results:
    Γ, Σ, Π, Ψ ⊢ 𝑒 1 : 𝜏, 𝜂 1 and well formed state(Γ, Σ, 𝑠 1 ). Applying the termination lemma 4 on the
    typing derivation of 𝑒 and well-formedness of the initial state 𝑠, we know that there exists 𝑚,
    such that 𝑠, 𝑒 ↠𝑚 𝑠 ′, 𝑒 ′ and 𝑒 ′ is a value. We show that 𝑚 = 𝑛 + 1 and conclude that 𝑒 ′ is a value.
    Now applying the preservation lemma Γ, Σ, Π, Ψ ⊢ 𝑒 1 : 𝜏, 𝜂 1 , well formed state(Γ, Σ, 𝑠 1 ) and
    𝑠 1, 𝑒 1 → 𝑠 ′, 𝑒 ′ , we conclude the typing derivation and well-formedness of the resultant state

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                              41


      𝑠 ′ after 𝑛 + 1 steps. From the transitivity relation over the effects 𝜂 ′ ⊆ 𝜂 1 (𝜂 1 is obtained after
      applying preservation for n steps) and 𝜂 1 ⊆ 𝜂 (𝜂 1 is obtained for the last step), we conclude
      that 𝜂 ′ ⊆ 𝜂.
                                                                                                           □

  Lemma 22 (Safe Read).
      ∀Γ, Σ, Π, Ψ, 𝑒, 𝜏, 𝜂, 𝑠, 𝑠 ′, 𝑣, 𝑛. Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠) ∧ 𝑠, 𝑒 ⇝𝑛 𝑠 ′, 𝑣 ∧ Read ∈ 𝜂
                                     =⇒ ∃𝜂 ′ . Alloc ∈ 𝜂 ′ ∧ 𝜂 ′ ⊆ 𝜂

   Proof. We proceed by induction on the structure of the typing derivation Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂
   Var case. From the typing rule for variables, we have: Γ(𝑥) = 𝜏 ⇒ Γ, Σ, Π, Ψ ⊢ Var 𝑥 𝜏 : 𝜏, {Read}.
Since the expression produces a read effect, and the variable 𝑥 must be present in the typing context
Γ, the well-formedness of the state well formed state(Γ, Σ, 𝑠) ensures that 𝑥 must be allocated in
memory. Therefore, the allocation must have occurred prior to this point and be tracked in the
effect list. So we conclude that there exists 𝜂 ′ ⊆ 𝜂 such that alloc ∈ 𝜂 ′ .
   Let-binding case. From the typing derivation:Γ, Σ, Π, Ψ ⊢ 𝑒 1 : 𝜏, 𝜂 1, and(𝑥 → 𝜏, Γ), Σ, Π, Ψ ⊢ 𝑒 2 :
𝜏2, 𝜂 2 ⇒ Γ, Σ, Π, Ψ ⊢ let 𝑥 : 𝜏 = 𝑒 1 in 𝑒 2 : 𝜏2, 𝜂 1 ∔ 𝜂 2 .
   From the hypothesis, read ∈ 𝜂 1 ∔ 𝜂 2 . We consider two cases:
  • If read ∈ 𝜂 1 , we apply the induction hypothesis to 𝑒 1 . This gives 𝜂 1′ ⊆ 𝜂 1 such that alloc ∈ 𝜂 1′ ,
      and thus 𝜂 1′ ⊆ 𝜂 1 ∔ 𝜂 2 .
  • If read ∈ 𝜂 2 , then the read occurs in the body 𝑒 2 under the extended context. If the read depends
      on the variable 𝑥, then 𝑥 must have been allocated during the evaluation of 𝑒 1 , so alloc ∈ 𝜂 1 . If
      the read is on another variable from Γ, then well formed state(Γ, Σ, 𝑠) ensures it was allocated
      already. In either case, the corresponding Alloc appears in 𝜂 1 or 𝜂 2 and hence in 𝜂.
All other expression forms (e.g., App, Prim, Cond, Sfield, Match, etc.) either preserve or combine
effects from subexpressions. If read ∈ 𝜂, it must have originated from some subexpression with its
own typing derivation. The inductive hypothesis applies, so the required alloc ∈ 𝜂 ′ for some 𝜂 ′ ⊆ 𝜂.
By structural induction on the typing derivation, any presence of read in the effect set implies a
prior alloc also appears in a subset of the effect list.                                                 □

7.2     BeePL Compiler
In this section, we describe how the BeePL compiler translates high-level BeePL constructs into C,
highlighting key program transformations that ensure memory and type safety in the generated
code. We focus only on the most interesting cases that illustrate how the compilation process
enforces safety through careful code generation.
   Translation of BeePL ref construct to C. The BeePL compiler first translates the inner expression 𝑒
that will be stored in the reference. It then introduces a fresh local variable to hold this value and
generates code to assign the value to that variable. Finally, it returns the address of the variable,
effectively modeling the behavior of ref as a pointer in C. This allows BeePL’s reference semantics
to be represented using local variable allocation and address-taking in the CompCert C syntax.
                             (
                               i = ce; J𝑒K = 𝑐𝑒 ∧ fresh 𝑖 ∧ typeof 𝑖 = Jtypeof 𝑒K𝜏
                   Jref 𝑒K =
                               &i
   Translation of BeePL for-loop to C. A for loop in BeePL is translated into imperative C-style code
with explicit loop bounds and direction-aware control flow. The source-level loop is of the form:
for (𝑒 1 . . . 𝑒 2, 𝑑) {𝑒}, where 𝑒 1 and 𝑒 2 specify the lower and upper bounds, 𝑑 denotes the direction
(Up or Down), and 𝑒 is the loop body.

                                                                         , Vol. 1, No. 1, Article . Publication date: July 2026.
42


  • The expressions 𝑒 1 and 𝑒 2 are compiled to C expressions 𝑐𝑒 1 and 𝑐𝑒 2 , which are stored in fresh
    local variables l and h.
  • A fresh variable i is introduced to serve as the loop index.
  • Depending on the direction:
      – If 𝑑 = Up, the generated code is: if (l <= h) for (i = l; i <= h; i++) { ce }
      – If 𝑑 = Down, the generated code is: if (l >= h) for (i = l; i >= h; i–) { ce }
  • If the guard condition is false (i.e., the range is empty), the entire loop reduces to Skip.
This transformation ensures that BeePL’s high-level iteration is compiled into safe, structured
loops in C. Since the loop bounds are computed before iteration starts, and the index progresses
monotonically in the specified direction, the resulting loop is guaranteed to terminate, provided
that the subexpressions 𝑒 1 , 𝑒 2 , and 𝑒 themselves terminate. This structure allows the BeePL compiler
to preserve termination guarantees at the C level.
                               
                               
                                l = ce1 ;h = ce2 ;                     Dir == Up ∧ fresh l, fresh h, fresh i ∧ Je1 K = ce1
                               
                                 if (l <= h)                            ∧Je2 K = ce2 ∧ JeK = ce
                               
                               
                               
                               
                               
                                 then   for(i = l; i <= h; i + +){ce}
                               
                               
                               
                               
                               
                                 else Skip
                               
                               
                               
                               
                               
                               
                               
                               
Jfor (𝑒 1 . . . 𝑒 2, 𝑑) 𝑒K =
                               
                               
                                l = ce1 ;h = ce2 ;                     Dir == Down ∧ fresh l, fresh h, fresh i ∧ Je1 K = ce1
                               
                               
                               
                               
                                if (l >= h)                            ∧Je2 K = ce2 ∧ JeK = ce
                               
                               
                               
                                then for(i = l; i >= h; i − −){ce}
                               
                               
                               
                               
                                else Skip
                               
                               
                               
                               
   Translation of BeePL let-binding to C. The let-binding construct in BeePL, written as let 𝑥 : 𝑡 = 𝑒 in 𝑒 ′ is
translated as follows:
  • It first compiles the continuation 𝑒 ′ into a C code fragment 𝑐𝑒 ′ .
  • It then examines the structure of 𝑒:
      – If 𝑒 is a statement-level construct (such as an assignment, for-loop, struct initialization, or a nested
          Bind), it is compiled into a statement 𝑐𝑒 and simply sequenced before 𝑐𝑒 ′ as 𝑐𝑒; 𝑐𝑒 ′ .
      – If 𝑒 is a pure expression, it is compiled into a C expression 𝑐𝑒, and the compiler emits a local variable
          assignment x = ce; followed by 𝑐𝑒 ′ .
  • This translation preserves the evaluation order of BeePL and ensures that side effects in 𝑒 occur before
    evaluating 𝑒 ′ , as required by the semantics.
This strategy ensures that the generated C code faithfully reflects the sequential and scoping behavior of
BeePL’s let-bindings, preserving both value and effect ordering as in the source program. It also distinguishes
between expression-level and statement-level forms to enable correct and structured code generation.
                                         (
                                          𝑐𝑒; 𝑐𝑒 ′    J𝑒 ′ K = 𝑐𝑒 ′ ∧ J𝑒K = 𝑐𝑒 ∧ 𝑒 ∈ {let, :=, for, sinit}
               Jlet 𝑥 : 𝑡 = 𝑒 in 𝑒 ′ K =
                                          𝑥 = 𝑐𝑒; 𝑐𝑒 J𝑒 ′ K = 𝑐𝑒 ′ ∧ J𝑒K = 𝑐𝑒 ∧ 𝑒 ∉ {let, :=, for, sinit}
                                                    ′

   Translation of BeePL match constructs to C. The BeePL match expression on an option type get translated to
a NULL check in C. If J𝑒K = NULL (i.e., None), it evaluates to J𝑒 1 K. Otherwise, for Some 𝑥, it binds 𝑥 = 𝑐𝑒 and
evaluates J𝑒 2 K. This ensures safe and direct handling of optional pointers.

                                                 
                                                 
                                                 𝑐𝑒 1            p1 == None ∧ p2 == Some x ∧ typeof 𝑒 = option(𝜏∗)
                                                 
                                                 
                                                 
                                                                 J𝑒 1 K = 𝑐𝑒 1 ∧ J𝑒 2 K = 𝑐𝑒 2 ∧ J𝑒K = 𝑐𝑒 ∧ 𝑐𝑒 = NULL
 Jmatch 𝑒 with 𝑝 1 ⇒ 𝑒 1 | 𝑝 2 ⇒ 𝑒 2 K =
                                                 
                                                 
                                                  𝑥 = 𝑐𝑒; 𝑐𝑒 2   p1 == None ∧ p2 == Some x ∧ typeof 𝑒 = option(𝜏∗)
                                                 
                                                 
                                                                 J𝑒 1 K = 𝑐𝑒 1 ∧ J𝑒 2 K = 𝑐𝑒 2 ∧ J𝑒K = 𝑐𝑒 ∧ 𝑐𝑒 ≠ NULL


, Vol. 1, No. 1, Article . Publication date: July 2026.
     BeePL: Correct-by-compilation kernel extensions                                                                                       43


 1   #section "xdp"                                                            1   SEC("xdp_drop")
 2   fun bprog4(option(struct xdp_md★) ctx) : int {                            2   int cprog4(struct xdp_md ∗ctx)
 3     match ctx.data with                                                     3   {
 4        | eth, struct ethhdr: (h_proto, uint16) =>                           4      void∗ data_end = (void star)(long)ctx−>data_end;
 5           if (h_proto == htons(ETH_P_IPV6))                                 5      void∗ data = (void star)(long)ctx−>data;
 6           then XDP_DROP                                                     6      struct ethhdr ∗eth = data;
 7           else XDP_PASS                                                     7      uint16 h_proto;
 8        | _ => XDP_DROP                                                      8      if (data + sizeof(struct ethhdr) > data_end)
 9   }                                                                         9          return XDP_DROP;
10   char LICENSE[] SEC("license") = "GPL";                                   10      h_proto = eth−>h_proto;
                                                                              11      if (h_proto == htons(ETH_P_IPV6))
                                                                              12          return XDP_DROP;
                                                                              13      return XDP_PASS;
     Fig. 17. BeePL program using the match construct to                      14   }
     ensure safe memory access within bounds                                  15   char LICENSE[] SEC("license") = "GPL";



                                                                                   Fig. 18. C program obtained after compiling
                                                                                   bprog4 using the BeePL compiler

        The BeePL match expression on Pbytes (illustrated in Figure 17) is translated to C (illustrated in Figure 18)
     by first evaluating the expression 𝑒 to obtain a byte range ce of type bytes t defined as struct bytes t {unsigned
     char *start; unsigned char* end}, where the fields start and end represent the lower and upper bounds of the
     byte range, respectively.. The generated C code includes a conditional check:
                                                       if (ce.start + sizeof(struct s) > ce.end)
     to ensure there is enough memory to safely read a struct s from the byte stream. If the check fails, the fallback
     branch 𝑒 2 is evaluated. Otherwise, the code casts the byte pointer to a struct s*, extracts fields into variables
     (e.g., 𝑥 .𝑓𝑖 := tmp → 𝑓𝑖 ), updates ce.start, and continues with 𝑒 1 . This strategy prevents out-of-bounds memory
     access by ensuring that field accesses only occur within valid memory bounds. We focus here on the case of
     reading a struct from the buffer, though the approach generalizes to all supported types. However, if a struct
     field is itself a pointer, additional care is required. In such cases, simply verifying the bounds of the enclosing
     buffer is insufficient—we must also reason about the memory region pointed to by that field. One way to
     handle this safely is to disallow pointer fields during deserialization, or alternatively, to require an additional
     match expression to validate the bounds of the pointed-to memory region before accessing it. Without such
     precautions, the safety guarantees provided by the initial match on the enclosing struct could be compromised.
     At this moment, we focus only on structs whose fields are of non-pointer types.
                                                                  
                                                                  
                                                                   J𝑒K = ce, ce : bytes t
                                                                  
                                                                  
                                                                    if (ce.start + sizeof(struct 𝑠) > ce.end)
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                   J𝑒 2 K
                                                                  
                                                                  
                                                                  
                                                                  
                                                                    else {
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                 Jmatch 𝑒 with Pbytes(𝑥, 𝑠, {𝑓𝑖 : 𝜏𝑖 }) ⇒ 𝑒 1 K =       struct 𝑠* tmp = (struct 𝑠*) ce.start;
                               | ⇒ 𝑒2
                                                                  
                                                                  
                                                                  
                                                                   for each 𝑓𝑖 : 𝑥 .𝑓𝑖 := tmp → 𝑓𝑖
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  
                                                                       ce.start += sizeof(struct 𝑠);
                                                                  
                                                                  
                                                                  
                                                                   J𝑒 1 K
                                                                  
                                                                  
                                                                  
                                                                  
                                                                  }
                                                                  
        To prove the compiler correctness, we first define the equivalence relation between the BeePL and C state:
                                                                                                             
                               ´𝐵 = ´𝐶 ∧ ˙𝐵 = ˙𝐶 ∧ ˆ𝐵 = ˆ𝐶 ∧
              𝑠𝐵 ≈ 𝑠𝐶 ≜
                               ∀𝑙, 𝑜, 𝜏𝐵 . Σ𝐵 (𝑙) = 𝜏𝐵 =⇒ ∃𝜏𝐶 . J𝜏𝐵 K𝜏 = 𝜏𝐶 ∧ Θ𝐶 [𝜏𝐶 , 𝑙, 𝑜] = Θ𝐵 [𝜏𝐵 , 𝑙, 𝑜]
     The equivalence relation ≈ asserts that BeePL and C program states are identical in their memory representa-
     tion—both use the same variable map (Ω), global environment (Δ), and memory (Θ), since BeePL and CompCert

                                                                                       , Vol. 1, No. 1, Article . Publication date: July 2026.
44


are built on a common implementation of these components. The only distinction lies in their type systems. A
memory access at (𝑙, 𝑜) yields the same value in both languages, provided the BeePL type 𝜏𝐵 translates to the
corresponding C type J𝜏𝐵 K𝜏 .


   Lemma 23 (Compiler Correctness: BeePL to Csyntax).
  ∀Γ, Σ, Π, Ψ, 𝑒, 𝑒 ′, 𝑠, 𝑠 ′, 𝜏, 𝜂, 𝑛, 𝑐, 𝑣𝑐 , 𝑣𝑏 , 𝑐𝑠 , 𝑐𝑠′ . Γ, Σ, Π, Ψ ⊢ 𝑒 : 𝜏, 𝜂 ∧ well formed state(Γ, Σ, 𝑠) ∧ J𝑒K = 𝑐 ∧
                                                      𝑠, 𝑒 ↠𝑛 𝑠 ′, 𝑣𝑏 ∧ 𝑠 ≈ 𝑐𝑠 ∧ 𝑐𝑠 , 𝑐 ⇓ 𝑐𝑠′ , 𝑣𝑐 =⇒
                                                      𝑣𝑏 = 𝑣𝑐 ∧ 𝑠 ′ ≈ 𝑐𝑠′

    Proof. We discuss the proofs for the translations of the ref, for-loop, and match expressions as defined
above. For the remaining expressions, the proof proceeds in a similar style. In particular, several expres-
sions—such as constants, variables, and binary operations—have direct one-to-one mappings to Csyntax,
making their correctness proofs straightforward. Other expressions involving memory or control flow are
handled analogously using the inductive hypothesis and consistent memory manipulations.
    ref 𝑒: In BeePL, evaluating ref 𝑒 proceeds by first evaluating 𝑒 (𝑠, 𝑒 ↠𝑛1 𝑠 1, 𝑣), then allocating a fresh memory
location ℓ and storing 𝑣 at ℓ and finally returning the location ℓ as the result Thus, 𝑠, ref 𝑒 ↠𝑛1 +1 𝑠 ′, ℓ, where
𝑠 ′ is 𝑠 1 extended with the binding ℓ ↦→ 𝑣, ℓ is fresh and 𝑠 1 is the intermediate state.
    The BeePL compiler translates ref 𝑒 to: Jref 𝑒K = i = J𝑒K; &i, where i is a fresh local variable in C syntax, and
the expression returns its address. The compiled C program performs evaluation of compiled C expression: 𝑐𝑠 ,
J𝑒K ⇓ 𝑐𝑠′ , 𝑣𝑐 , followes by storing 𝑣𝑐 in a fresh local variable i, and finally returning &i. So, the final result is the
address of i holding 𝑣𝑐 , and the final C state 𝑐𝑠′ contains this binding.
    By inductive hypothesis on the evaluation of 𝑒:

                                  𝑠, 𝑒 ↠𝑛1 𝑠 1, 𝑣𝑏 ∧ 𝑐𝑠 , J𝑒K ⇓ 𝑐𝑠1, 𝑣𝑐 ⇒ 𝑣𝑏 = 𝑣𝑐 ∧ 𝑠 1 ≈ 𝑐𝑠1

After this step:
  • BeePL allocates a fresh location ℓ and binds ℓ ↦→ 𝑣𝑏
  • C creates a fresh local variable i and stores 𝑣𝑐 into it
By the freshness condition and we know that the BeePL’s and C’s environments grow consistently, we extend
the relation: 𝑠 ′ ≈ 𝑐𝑠′ , where 𝑠 ′ extends 𝑠 1 with ℓ ↦→ 𝑣𝑏 , and 𝑐𝑠′ extends 𝑐𝑠1 with i holding 𝑣𝑐 . Finally, the result
values: 𝑣𝑏 = ℓ and 𝑣𝑐 = &i are considered equal under the equivalence relation: ℓ ≈ &i. Thus, both BeePL and
C perform the same evaluation steps, allocate storage, store the result, and return a pointer to it. The resulting
states and values remain related:𝑣𝑏 = 𝑣𝑐 ∧ 𝑠 ′ ≈ 𝑐𝑠′ as required.
    for(𝑒 1 ; 𝑒 2 ; 𝑑; 𝑒): In BeePL, the loop expression evaluates the bounds 𝑒 1 and 𝑒 2 to values 𝑣 1 and 𝑣 2 respectively:
𝑠, 𝑒 1 ↠𝑛1 𝑠 1, 𝑣 1 and 𝑠 1, 𝑒 2 ↠𝑛2 𝑠 2, 𝑣 2 . Then, depending on the direction 𝑑, the loop body 𝑒 is evaluated iteratively:
  • If 𝑑 = Up and 𝑣 1 ≤ 𝑣 2 , the loop runs from 𝑣 1 to 𝑣 2
  • If 𝑑 = Down and 𝑣 1 ≥ 𝑣 2 , the loop runs from 𝑣 1 down to 𝑣 2
producing a final state 𝑠 ′ and result 𝑣: 𝑠, for(𝑒 1 ; 𝑒 2 ; 𝑑; 𝑒) ↠𝑛 𝑠 ′, unit.
    By inductive hypotheses: 𝑠, 𝑒 1 ↠𝑛1 𝑠 1, 𝑣 1 ∧ 𝑐𝑠 , 𝑐𝑒 1 ⇓ 𝑐𝑠1, 𝑣 1 ⇒ 𝑠 1 ≈ 𝑐𝑠1 and 𝑠 1, 𝑒 2 ↠𝑛2 𝑠 2, 𝑣 2 ∧ 𝑐𝑠1, 𝑐𝑒 2 ⇓
𝑐𝑠2, 𝑣 2 ⇒ 𝑠 2 ≈ 𝑐𝑠2 . Then, for each iteration: 𝑠𝑖 , 𝑒 ↠𝑛𝑖 𝑠𝑖+1, 𝑣 ∧ 𝑐𝑠𝑖 , 𝑐𝑒 ⇓ 𝑐𝑠𝑖+1 , 𝑣 ⇒ 𝑠𝑖+1 ≈ 𝑐𝑠𝑖+1
    Thus, state equivalence is preserved throughout the loop. Hence; we conclude: 𝑣𝑏 = 𝑣𝑐 ∧ 𝑠 ′ ≈ 𝑐𝑠′ as required.
    Match on Bytes. We proceed by case analysis on the runtime check generated by the compiler from the
BeePL expression:
                                   match 𝑒 with Pbytes(𝑥, 𝑠, {𝑓𝑖 : 𝜏𝑖 }) ⇒ 𝑒 1 |         ⇒ 𝑒2
   Let J𝑒K = 𝑐𝑒, and suppose it evaluates in both BeePL and C to a byte region ce = (start, end). The compiler
translates this expression into the following C code:

                                if (ce.start + sizeof(struct 𝑠) > ce.end) J𝑒 2 K else {...; J𝑒 1 K}

     We analyze the two branches of this conditional.

, Vol. 1, No. 1, Article . Publication date: July 2026.
BeePL: Correct-by-compilation kernel extensions                                                                           45


   Case 1: ce.start + sizeof(struct s) > ce.end. In this case, the BeePL semantics selects the fallback branch 𝑒 2 .
Formally, we have: 𝑠, 𝑒 ↠𝑛1 𝑠 1, ce and 𝑠 1, 𝑒 2 ↠𝑛2 𝑠 ′, 𝑣𝑏 and by assumption,
𝑐 = Jmatch 𝑒 with ...K evaluates in C as 𝑐𝑠 , 𝑐 ⇓ 𝑐𝑠′ , 𝑣𝑐 Since the compiled C code takes the same branch (the
condition fails), it executes J𝑒 2 K, producing 𝑣𝑐 and ending in state 𝑐𝑠′ . By the inductive hypothesis on 𝑒 2 , and
since 𝑠 1 ≈ 𝑐𝑠′′ for some intermediate C state 𝑐𝑠′′ , we get:
                                               𝑣𝑏 = 𝑣 𝑐   and 𝑠 ′ ≈ 𝑐𝑠′
   Case 2: ce.start + sizeof(struct s) ≤ ce.end. Here, BeePL succeeds in extracting a struct of type 𝑠 from the
byte buffer. The semantics proceeds by casting start to a struct 𝑠 and then binding the corresponding parts to
their respective fields. After successful copying of the buffer, the pointer is updated and the corresponding
follow-up expression 𝑒 1 is evaluated in the extended state. In C, the compiler emits the same logic as explained
in the translation of match construct over bytes. By the inductive hypothesis applied to 𝑒 1 , and assuming that
field access and pointer arithmetic behave consistently in BeePL and C (as guaranteed by 𝑠 ≈ 𝑐𝑠 ), we conclude:
                      𝑠, 𝑒 ↠𝑛1 𝑠 1, ce,   start′ = start + sizeof (struct s),   𝑠 1′ , 𝑒 1 ↠𝑛2 𝑠 ′, 𝑣𝑏
and similarly, 𝑐𝑠 , 𝑐 ⇓ 𝑐𝑠′ , 𝑣𝑐 , where 𝑐𝑠′ reflects updated start and same field bindings
   Therefore: 𝑣𝑏 = 𝑣𝑐 and 𝑠 ′ ≈ 𝑐𝑠′ . In both cases, the BeePL and C semantics agree on the branch taken, the
fields extracted, and the pointer updates. The evaluation of the continuation expression (𝑒 1 or 𝑒 2 ) is correct by
the inductive hypothesis. Hence, the compiled C code produces the same result as the BeePL code, and the
final states remain related.
                                                                                                                   □




                                                                      , Vol. 1, No. 1, Article . Publication date: July 2026.
