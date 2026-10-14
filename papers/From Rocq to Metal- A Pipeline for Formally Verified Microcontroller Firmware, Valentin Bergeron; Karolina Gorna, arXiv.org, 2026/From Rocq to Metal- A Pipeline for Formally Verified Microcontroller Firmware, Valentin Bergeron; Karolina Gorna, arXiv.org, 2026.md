                                             From Rocq to Metal: A Pipeline for Formally
                                                  Verified Microcontroller Firmware

                                                             Valentin Bergeron1 and Karolina Gorna2
                                                                       1
                                                                        Ledger, Paris, France
                                                                  valentin.bergeron@ledger.fr
                                                         2
                                                           Telecom Paris and Ledger Donjon, Paris, France
arXiv:2606.02651v2 [cs.PL] 21 Sep 2026




                                                           karolina.gorna@[telecom-paris,ledger].fr



                                               Abstract. Enforcing invariants in safety-critical firmware is increasingly
                                               urgent as generated code becomes widespread, but standard extraction
                                               targets for proof assistants require runtimes too large for many embedded
                                               devices. We present a pipeline for running formally verified Rocq firmware
                                               logic on Cortex-M microcontrollers. The pipeline extracts Gallina to
                                               Scheme, compiles it with Encore!, a bare-metal Continuation Passing Style
                                               (CPS) bytecode virtual machine, and embeds the result in no_std Rust
                                               firmware. We structure applications as pure state-transition functions,
                                               so the business logic is proved in Rocq while the event/effect boundary,
                                               host callbacks, compiler, and VM remain explicit trusted components.
                                               On ST33-class targets with a 50 KB RAM lower bound, Encore! executes
                                               Rocq-extracted code end-to-end, stays within the target memory budget
                                               on our benchmarks, and validates a transaction-signing application on
                                               physical Ledger Flex hardware.

                                               Keywords: formal verification · Rocq · Gallina · microcontrollers ·
                                               firmware · CPS · proof extraction


                                         1   Introduction

                                         Generated code is changing how software is written, including firmware. For
                                         safety-critical devices, lower code-generation cost increases the amount of code
                                         that must be reviewed, while the required assurance level remains high. Formal
                                         verification has already demonstrated its value at the systems level — seL4 [10]
                                         gives a machine-checked proof of OS kernel correctness — and similar rigour is
                                         increasingly sought for firmware. Formal specifications offer a scalable response:
                                         generated implementations can be checked against theorem statements, and proof
                                         obligations become part of the development interface.
                                             However, the hardware constraints of embedded firmware prevent straightfor-
                                         ward use of standard specification language extraction. The runtimes required
                                         to execute extracted code exceed the resource budget of most microcontrollers.
                                         Standard practice is therefore to translate specifications into the host language,
                                         automate that translation, or use host-language extensions, weakening the con-
                                         nection to the proof assistant.
2         V. Bergeron and K. Gorna

    We built Encore! [2] to close this gap. Encore! is a bare-metal CPS bytecode
VM written in no_std Rust that executes Rocq-extracted Scheme on microcon-
trollers. The pipeline is end-to-end: write firmware logic and prove it correct in
Rocq, extract to Scheme, compile with Encore!, and deploy. What runs on the
MCU is directly derived from the Rocq source, though the compiler, VM, host
callbacks, and device I/O remain trusted.
    We first present an architecture for structuring firmware so its core is fully
verifiable, illustrated on a concrete transaction-signing application. We then
survey the landscape of extraction paths from theorem provers to embedded
targets, and characterize why executing this class of code on microcontrollers
is non-trivial. Next, we introduce Encore! and show how it addresses these
challenges. Finally, we present experimental results and outline remaining steps
toward extending trust further up the toolchain.
    This work makes three contributions:

    – We show that code extracted from Rocq can run on Cortex-M microcontrollers,
      by choosing Scheme as the extraction target and building a purpose-built
      bare-metal runtime.
    – We present Encore!, a no_std CPS bytecode VM in Rust that fits within the
      resource budget of ST33-class hardware and executes Rocq-extracted Scheme
      end-to-end.
    – We introduce a firmware architecture structured as a pure state-transition
      function, making the business-logic core fully provable in Rocq while keeping
      the unverified TCB constant regardless of firmware complexity.


2      An Architecture for Verified Firmware

This section answers what to run on the MCU and how to structure it so
correctness is fully provable in Rocq.


2.1     The State Transition Model

In order to maximize the area that can be proven, we choose to model the
application as a pure state transition function, effectively treating the whole
embedded device as a state machine.
   Before diving into the modeling details, we assume that a Scheme VM is
deployed as part of what we call a Formal Software Development Kit (FSDK),
that bridges the virtual machine and the host device. The FSDK contains both
host code (it is the real firmware that gets deployed) and Rocq code to provide
the necessary bridge abstractions.
   With this in mind, we define the state transition function as:

                  step : State × Event → State × list Effect.

      Given the types:
                                                                                From Rocq to Metal                          3

State represents the application state. This will depend on what problem the
    application is solving, independently from the FSDK.
Event is an incoming event from the device. Device events are linked to the
    underlying hardware and can be network packets, user interface signals such
    as pressed buttons or specific touch screen positions, etc.
Effect is the description of an effectful computation that needs to be interpreted
    to be realized. A critical part of the FSDK is then to interpret the effects to
    perform them.
    This model applies two key functional programming principles, copying instead
of mutating and describing effects rather than performing them directly, to
firmware code, effectively maximizing the provable business logic part.
    The remaining parts, the Event poller and the Effect interpreter, form the
trusted computing base (TCB). Their size is independent of firmware complexity
unless new hardware operations and capabilities are added. The verified core
grows with the application; the unverified boundary stays fixed.
    Moreover, in a VM-based deployment the application logic can be fully
specified in the VM input code, allowing the same carefully reviewed base
firmware to host custom, verified business logic, which is a particularly powerful
combination for safety-critical devices.

2.2      Admitted Axioms and the Trust Chain
Some operations are observationally pure from Rocq’s perspective but will be
extremely impractical to implement fully from a business point of view. For
instance, hash functions, polynomial operations (CRC), and more generally any
finite field operation involved in cryptographic algorithms.
    Rather than relying on an Effect/Event pair with little added value, we choose
to admit them in Rocq as axioms and provide them as host callbacks before the
application run loop starts. Additionally, VM primitive operations such as raw
byte operations (bytes_len, bytes_concat, etc.) are abstracted via a typeclass
admitted in the extraction context. The FSDK bridges the typeclass and the
concrete VM-provided implementations via Rocq extraction directives.
Si−1                                        Si                         Si+1                                           Si+2


       Ei−1                Fi−1                    Ei            Fi                        Ei+1                Fi+1
···           step i − 1          perform   poll        step i        perform       poll          step i + 1          ···



Fig. 1. Formal SDK generic app loop over two consecutive steps. S: State, E: Event,
F : Effects list. Ellipses denote the unbounded continuation of the loop.



2.3      Trust Assumptions
The verified part of the system is the Rocq model of the application logic and
its stated properties. The trusted computing base includes the Rocq kernel and
extraction mechanism, the extracted Scheme frontend, the Encore! compiler
     4      V. Bergeron and K. Gorna

     and VM, the Rust compiler, host callbacks implementing admitted axioms,
     and the event poller/effect interpreter supplied by the device firmware. This
     boundary is deliberate: application growth extends the proved step function and
     its lemmas, whereas the unverified boundary changes only when new hardware
     actions, externs, or runtime primitives are added. The current work therefore
     establishes verified firmware logic running on bare metal; proving the compiler
     or VM is future work, discussed in Sect. 6.

     2.4   Concrete Example: Transaction Signing Application
     As a concrete example, we built a Ledger Flex transaction-signing app with
     Encore!.
         LedgerOS provides us with higher level primitives we used as our Event
     Poller and our Effect Handler. We tailored the component we called FSDK
     to the particular use cases of this app for the sake of simplicity. In a real
     implementation of a Formal SDK for this class of Ledger device and OS, the list
     of events and effects is expected to be much longer.
         The device receives raw Application Protocol Data Unit (APDU) bytes over
     USB, parses them into structured fields, displays them for user approval, then
     signs and returns the result. The app is a toy: it is not tied to any real crypto
     protocol.
1 (* Application specific state *)
2 Inductive State : Type :=
3   | InitialState
4   | PendingTx ( tx : Bytes ) .
5

6    (* Formal SDK - truncated *)
7

8  Inductive Event : Type :=
9    | InApdu ( bytes : Bytes )
10   | ApprovedTx
11   | RejectedTx .
12

13 Inductive Effect : Type :=
14   | OutApdu     ( bytes : Bytes )
15   | DisplayProps ( to : Bytes ) ( value : Bytes ) .

        Parser correctness is where formal verification pays off most directly. Two
     properties are proven for our app:
1 Theorem d e s e r i a l i z e _ p r e s e r v e s _ d a t a : forall data tx ,
2   de s er ia li z e_ tr a ns ac ti o n data = inr tx ->
3   tx_nonce tx ++ tx_to tx ++ tx_value tx ++ tx_memo tx = data
         .
4

5 Theorem check_encoding_spec : forall memo ,
6   check_encoding memo = true <->
7   ( forall b , In b memo -> b <= MAX_ASCII ) .
                                                      From Rocq to Metal         5

    deserialize_preserves_data guarantees no bytes are dropped or reordered
during parsing, exactly what a hardware wallet must ensure before signing.
check_encoding_spec gives a machine-checked certificate that memo content is
valid ASCII. Note that neither property is expressible as a Rust type.
    This structure also suits code generation: a candidate step function is checked
immediately by Rocq, and theorem statements make the expected behavior
explicit. LLM-assisted proof synthesis [4] can be used in this workflow, but the
assurance argument relies on the Rocq kernel and stated lemmas rather than on
the generator.


3     Related Work
We investigated the feasibility of running proved logic on resource-constrained
microcontrollers (MCUs), targeting the ST33K1M5 and the tighter ST33J2M0
budget in Table 1. The ST33J2M0, with 50 KB of RAM, sets the binding
constraint.
            Table 1. Hardware specifications of the MCUs considered.

                   Metric      ST33K1M5        ST33J2M0
                   ISA         ARM+Thumb2 ARM+Thumb2
                   Flash       1.5 MB     2 MB
                   RAM         64 KB      50 KB
                   Clock speed 70 MHz     60 MHz
                   Cache       2 KB       None

   Any attached runtime must therefore be lean: applications on this class of
MCU often ship with no runtime, and the code cannot rely on libc, libm, or the
Rust standard library. This excludes many otherwise attractive proof-to-code
paths.

3.1   Lean 4
Lean 4 [6] has mature native code generation and an active proof ecosystem,
but its runtime assumes C++ library support, reference counting with cycle
collection, tasks, and hosted IO. Prior reports confirm that more constrained
targets than a Raspberry Pi require substantial runtime work [8]; the known
ESP32-C3 port needed a patched libc++/picolibc stack on a device with 384 KB
of RAM [13]. The Lean FRO roadmap [14] does not currently target bare-metal
embedded deployment.

3.2   Rocq Extraction to OCaml
Rocq extraction to OCaml [16, 17] is mature, but the OCaml runtime requires a
generational GC, libc/libm support, and native-code assumptions mismatched
with Cortex-M object formats. A native OCaml Cortex-M experiment required
6       V. Bergeron and K. Gorna

assembly patching, a custom linker script, and standard-library stubs on a larger
target [7]. OMicroB [21] is closer in spirit, but supports AVR and PIC32; the
Cortex-M0 port discussed in prior work [22] remains unmerged, and our Cortex-
M35P targets require full Thumb-2 support.

3.3   CertiRocq
CertiRocq [1] is the most principled Rocq compilation path: it compiles Gallina
to Clight through a largely verified compiler chain. Its runtime story is nev-
ertheless conditional for our targets. The generated Clight allocates inductive
values, and correctness is stated against a GC-aware heap predicate full_gc
[11]; replacing the runtime on Cortex-M therefore requires either proving a new
collector or restricting programs to bounded allocation. Moreover, CertiRocq
does not apply the standard extraction mechanism that maps Peano nat to ma-
chine arithmetic, so arithmetic-heavy programs may become infeasible without
source-level representation changes.

3.4   Usage of Scheme Extraction
Rocq also supports extraction to Scheme [17]. Although less mature than OCaml
extraction, Scheme has compact semantics and no mandatory hosted runtime.
Small Scheme systems such as Ribbit [23] and PICOBIT [20] show that complete
implementations can fit microcontroller budgets. We therefore evaluate Chibi
Scheme [19], Ribbit, CertiRocq, and our purpose-built runtime.
    Verified compilers such as CompCert [15] and CakeML [12] demonstrate that
strong compiler-correctness stories are possible. Encore! is not yet in that class:
its contribution is the systems path that makes Rocq-extracted logic executable
on the target hardware, with the remaining compiler/VM verification gap made
explicit in Sect. 2.3.


4     The Encore! VM and Compiler
The purpose of Encore! is to tailor a Scheme runtime which is efficient, lightweight
and safe to execute. First we will describe the compilation pipeline and design,
then dive into the specifics of the Encore! virtual machine.
    The key design decision relative to the Encore! toolchain comes from the
realization that most of the Scheme emitted by the Rocq extraction is both
heavily curried and mostly already present in suitable form to undergo CPS
rewrite, which is extremely well suited to implement functional languages on top
of register-based virtual machines.
    The CPS rewrite eliminates the call stack semantically while the register
VM eliminates it physically, leaving no hidden control flow and no stack frame
management at runtime. Register allocation also maps naturally to CPS, since
every intermediate value is named and data flow is made explicit. GC root
discovery similarly becomes trivial: every active register is a root, and CPS
                                                       From Rocq to Metal        7

guarantees they are always contiguous, eliminating the need for unbounded stack
scanning.
    Also Rocq-extracted Scheme forms a very particular subset of Scheme that
presents particularities worth optimizing. The extracted code must load a specific
macros_extr.csm file, which contains primitives for curried function definition
and application, as well as constructor pattern matching. The goal of Encore! is
to trade off generic Scheme macro support by only implementing these as core
primitives of the target execution model.
    The only addition of Encore! to the Scheme grammar is the special define
extern hook in order to make external function definitions, used in the host,
possible. It allows the Rocq code to pose the external functions as axioms and
later reference them from the host.
    The binary format (ENCR magic, arity table, global thunk offsets, bytecode)
is compact and position-independent, with optional metadata sections appending
constructor and global names for the disassembler.


4.1   VM Internals

Encore! is a #![no_std] register-based bytecode interpreter with 256 registers
and no call stack. Every value is a packed 32-bit word encoding its type, metadata,
and either an inline payload (integers, code pointers) or a heap address (closures,
constructors, byte strings).
    The register file is divided between special registers (Current function SELF
0x00, Current Continuation CONT 0x01 and Nullary sentinel NULL 0xff), argu-
ment registers (0x02 -> 0x0b) and regular registers (0x0c -> 0xfe).
    The heap is a flat bump-allocated arena shared by closures, constructors,
and byte strings, with all objects prefixed by a GC header word. The garbage
collector is mark-compact (Lisp-2 style): when a bump allocation fails, it traces
from all 256 registers and all globals as roots, marks reachable objects via header
bits, computes forwarding addresses in a linear scan, rewrites all pointers (roots
and interior), then slides live objects down and resets the heap pointer. Because
all values are self-describing 32-bit words with a type byte, the GC can identify
pointer types without compiler-emitted maps.
    All function dispatch is reduced to a single opcode: ENCORE. It overwrites
SELF and CONT, resolves the callee’s code pointer (inline for bare functions,
from the heap header for closures), and jumps; it never returns. Contrary to most
VMs, there is no CALL/RET pair and no frame stack. Calling a continuation
is the same instruction as calling a function; the NULL register is passed as
the continuation argument when resuming a final continuation. FIN halts the
interpreter and returns a register’s value.
    All other control flow is data-driven: MATCH does an indexed jump on a
constructor tag, BRANCH is a two-way variant. The remaining opcodes provide
primitives for data movement and allocation, as well as specialized opcodes for
native integer handling and byte string manipulation.
8       V. Bergeron and K. Gorna

4.2   Compiler Pipeline

The compiler pipeline starts with a lexer/parser step, which identifies specific
Rocq-extracted Scheme macros and includes them in its intermediate representa-
tion (IR). Then the Scheme frontend Abstract Syntax Tree (AST) is transformed
into the first of Encore! ’s sub-IRs, DS (for Direct-Style).
    We choose to articulate the compilation pipeline to first further refine the
Scheme to have better CPS rewrite and optimization targets. The first transform
is to uncurry chains of application wherever they are complete. In typical code,
full application happens quite often and thus allows us to spare the closure
allocation and reduce GC pressure in such a constrained target.
    Next step is to convert the direct-style IR to a fully CPS-transformed, De
Bruijn-indexed IR. Then the IR is optimized in a tight loop combining shrinking
and expanding phases as described by Appel [3] and Kennedy [9]. Finally, this IR
is compiled to VM bytecode after register addressing. Post-emission high-value
optimisations are also performed.


4.3   Host–VM Interface

Encore! is designed for hosted deployment: the bytecode VM is a library embedded
inside a Rust application that retains full control of the execution context, memory
budget, and I/O.
    The interface is deliberately narrow. The VM exposes two entry points to the
host:

 1. Function call: the host invokes a named global or a closure handle with
    typed arguments and receives a typed result.
 2. Extern registration: the host registers typed callbacks that the VM may
    invoke via the EXTERN opcode.


Derive-Macro Code Generation for ADTs For algebraic data types
exchanged across the boundary, Encore! provides procedural macros #
[derive(ValueEncode)] and #[derive(ValueDecode)]. Each variant or
struct field must be annotated with #[ctor(tag)], where tag is a u8 constant
from the compiler-generated ctors module (Sect. 4.3).
    This design draws a clear boundary between host-side types (ordinary Rust
structs and enums), VM-side types (constructor tags and field layouts), and the
bijection between them (the derive macros). Neither side references the other’s
internal representation; the mapping is established once at compile time through
the shared tag constants.
    Additionally, VmList<T> and VmBytes provide type-safe handles to linked
lists and byte arrays in the VM heap. Both support lazy traversal and bounded
materialization into caller-supplied buffers, which is the only safe option in a
no-alloc context.
                                                          From Rocq to Metal     9

Build-Time Binding Generation The mapping between host identifiers and
VM tags is produced at Cargo build time by a build.rs script that runs the full
compiler pipeline and emits two artefacts into $OUT_DIR:
 – bytecode.bin: the ENCR binary, linked into the firmware as a static byte
   array via include_bytes!.
 – bindings.rs: a Rust source file declaring two constant modules: funcs,
   one GlobalAddress constant per top-level let definition; and ctors, one u8
   constant per constructor tag, likewise named.
   This build-time generation guarantees that host tag references cannot diverge
from the bytecode: there is no separate binding definition file to keep in sync.


5     Experimental Results
We validate the three contributions experimentally. First, we show that among all
extraction paths, only Encore! and CertiRocq are viable candidates for running
verified code on a Cortex-M MCU. Second, we show that Encore! ’s design is
better suited for embedded application development. Third, we demonstrate the
state-transition architecture on a real application.
    The software versions used for this section are listed in Table 2. Flash values
are measured from the linked bare-metal image, heap values are the minimum
configured heap that completes each benchmark without allocation failure, and
build time is wall-clock time for a clean benchmark build on the same host. Unless
otherwise stated, benchmark execution is on QEMU configured for the Cortex-M
target; the signing application is additionally validated on physical Ledger Flex
hardware.
                    Table 2. Software versions used in this article.

             Tool                  Version Notes
             Rocq              9.1.1       compiled with OCaml 4.14.3
             CertiRocq         0.9.1
             Rust              1.88
             QEMU              8.2.2
             arm-none-eabi-gcc 13.2.1
             Ribbit            1.0.0       compiled with Gambit v4.9.3
             Chibi-Scheme      0.12.0



5.1   Running Verified Code on a Microcontroller
The extraction survey identifies four candidate paths. Table 3 summarises their
compatibility with our hardware constraints.
    Lean 4 and OCaml are eliminated by their runtimes alone. CertiRocq is viable
only for programs with bounded allocation, where its GC can be replaced by a
static bump allocator; it remains conditional. Scheme extraction survives every
10       V. Bergeron and K. Gorna

      Table 3. Rocq extraction paths against embedded deployment constraints.

Extraction path   GC required          no_std viable Cortex-M viable Proof infra preserved
Lean 4           Ref-count + cycle GC No            No               None
OCaml / OMicroB Generational GC        No           No               None
CertiRocq        Conditional           Partial      Partial          Compiler chain
Scheme / Encore! Mark-compact, bounded Yes          Yes              Full



constraint, leaving Encore! and CertiRocq as the two candidates worth evaluating
on hardware.
   Among Scheme runtimes, we prototyped full deployment pipelines for Chibi,
Ribbit, and Encore! on QEMU. Table 4 summarises the outcome.
   Chibi. The Rocq sources are extracted via dune build to .scm files, then the
Chibi C runtime (about 50 files) is cross-compiled with custom POSIX stubs, the
Scheme sources are embedded as a C string literal, and the whole is linked into
a bare-metal binary. The entire Chibi interpreter runs on the MCU at runtime,
loading and evaluating the Scheme source on every boot. The resulting binary
exceeds the 256 KB flash budget.
    Ribbit. The Rocq sources are extracted to .scm files, then build.rs invokes
gsi rsc.scm to produce a C file in OUT_DIR, which is patched to use a static heap
and a semihosting shim before being cross-compiled for Cortex-M35P and linked
into the binary. Only the bytecode and the minimal Ribbit VM are embedded,
and the binary fits on target. However, this step uses hand-written Scheme
sources rather than the Rocq-extracted ones, because Ribbit does not support
quasiquote. The verified firmware logic does not execute on the device.
    Encore!. The Rocq sources are extracted to .scm files, then build.rs invokes
encore_scheme::parse and encore_compiler::compile as a Rust API, with
no intermediate files or external tool invocations. The encore_program! macro
links the resulting bytecode into the binary, and encore_vm runs it on the MCU as
a no_std Rust library. The bytecode is compiled directly from the Rocq-extracted
Scheme sources, end-to-end.

     Table 4. Scheme runtimes against Rocq extraction deployment requirements.

                                            Chibi       Ribbit    Encore!
              Runtime model              interpreter VM     VM
              Runs Rocq-extracted Scheme ✓           ×      ✓
              Fits 256 KB flash          ×           ✓      ✓
              Pipeline complexity        high        medium low
              Working bare-metal         ×           ✓      ✓


   Encore! is the only Scheme runtime that satisfies all four requirements.
Together with the CertiRocq path, viable for bounded-allocation programs, it is
one of two candidates for running verified code on the target hardware.
                                                      From Rocq to Metal         11

5.2       Encore! Design Suitability

In order to run CertiRocq on such a constrained device, four surgical changes were
made in the CertiRocq runtime. The goal of these changes is to treat memory as
a static bump allocator, enabling us to compare the runtime behaviors in terms
of allocation rate and overall performance.

 1. Static nursery instead of malloc calls (gc_stack.c).
 2. Garbage collection aborts the program (gc_stack.c).
 3. Stub implementation for the remaining methods (gc_stack.c).
 4. Bare metal config to take the ARM embedded target into account (config.h
    and m.h).

    Table 5 compares Encore! against CertiRocq on seven standard benchmarks.
sum, fibonacci and gcd are simple arithmetic examples, fsm is a toy FSM
example, and rbtree is an implementation of a Red-Black tree on nat for different
tree sizes. Nodes from 1 to N are inserted then checked for membership.
Table 5. Encore! (E) vs CertiRocq (CR), all benchmarks (QEMU, Cortex-M). ratio is
CertiRocq / Encore!.

                    Flash (B)          Min heap (B)                 Build
Benchmark
                   CR     E ratio       CR      E ratio        CR           E ratio
                                           †
sum          2,480 14,340 0.17× ∼3,000 ≤50 ≥60× 1,145 ms 485 ms 2.4×
fibonacci    2,524 14,364 0.18× ∼3,000† ∼200 ∼15× 1,155 ms 499 ms 2.3×
gcd          2,948 16,252 0.18× ∼1,000 ≤50 ≥20× 1,208 ms 459 ms 2.6×
fsm          2,804 14,944 0.19×   ∼200 ∼200     1× 784 ms 488 ms 1.6×
rbtree-10    6,232 17,912 0.35×   1,624 471 3.4× 758 ms 573 ms 1.3×
rbtree-50   29,004 17,912 1.6× ∼21,720 2,022 10.7× 7,461 ms 539 ms 13.8×
rbtree-100 146,152 17,912 8.2×       –‡ 3,671    –     397 s 597 ms 665×

      †
      Peano nat stack depth, not heap, is the binding constraint for arithmetic.
      ‡
      CertiRocq rbtree(100) requires about 63 KB heap (O(N 1.56 ) growth),
exceeding the 50 KB RAM of the most constrained target (ST33J2M0), making
it infeasible regardless of configuration.
    Flash. CertiRocq is 5–6× smaller on arithmetic and FSM due to the direct
compilation into ARM assembly. The balance flips for the red-black tree: Cer-
tiRocq inlines literal list construction at compile time, so its binary grows from
6 KB at N = 10 to 146 KB at N = 100. Encore! stays constant at about 18
KB because construction is computed at runtime by the VM, with crossover at
N ≈ 40.
    Heap. Encore! needs less heap in every case except fsm. CertiRocq’s arith-
metic benchmarks require 1–3 KB despite producing no long-lived data. Peano
nat encoding materialises every intermediate value as a heap cell (ratio ≥ 20×
for sum and gcd). At large N , CertiRocq’s runtime-patched bump allocator can-
not reclaim intermediate nodes: rbtree(100) requires about 63 KB, physically
12      V. Bergeron and K. Gorna

exceeding the 50 KB RAM of the smallest target (ST33J2M0, Table 1). Encore! ’s
mark-compact GC keeps the requirement at 3.7 KB.
    Build time. Encore! rebuilds 1.3–2.6× faster on simple cases, as its pipeline is
a single Rust API call versus CertiRocq’s Rocq elaboration and C code generation.
The gap explodes to 665× on rbtree-100: gcc must optimise a 146 KB generated
C function with hundreds of intermediate variables.


5.3   State-Transition Architecture

The Ledger Flex transaction-signing app structures firmware as a pure step :
State * Event -> State * List Effect function. The verified Gallina core
(step, parser, helpers, and proofs) totals about 400 lines. Two non-trivial prop-
erties are machine-checked: deserialize_preserves_data (no bytes dropped
or reordered during parsing) and check_encoding_spec (memo ASCII valid-
ity). State-machine safety, signing only from PendingTx, follows by simpl;
discriminate.
    The unverified Rust layer is about 575 lines and is stable: adding new state
variants or event cases extends only the verified core. The TCB grows only if
new hardware operations are introduced, a structural guarantee rather than a
coincidence of the current implementation size.
    Whereas the benchmarks of Table 5 run on QEMU, this signing application
was validated end-to-end on physical Ledger Flex hardware: the Rocq-extracted,
Encore! -compiled firmware parses, displays, and signs data on the device.


6     Discussion

6.1   A Better GC for Embedded CertiRocq

Our approach using a static bump allocator in place of the regular multi-
generational GC of CertiRocq was robust enough to validate the general design of
Encore! but it is too limiting for more ambitious programs. With care, one could
weave a classic mark-and-sweep algorithm or a Cheney semispace algorithm on
static buffers in order to provide this path the ability to run larger programs.


6.2   Verified Optimisation Passes

The Encore! compiler’s nine CPS optimisation passes are currently implemented
in Rust and trusted by construction. The next step is to port the compiler to
OCaml and prove each pass semantics-preserving, in the style of CompCert
[15]. The CPS intermediate representation is well-suited for this: equational
reasoning about λ-calculus reductions is standard, and the shrinking reductions
have textbook semantic preservation proofs. The growth-enabling passes (inlining,
hoisting, CSE, contification) are structurally similar to optimisations already
verified in Pilsner [18].
                                                         From Rocq to Metal        13

6.3   Ahead-of-Time Native Compilation

The AOT backend is fully designed. The implementation compiles CPS IR directly
to ARMv8-M Thumb-2 assembly, eliminating interpreter dispatch entirely. Six
virtual registers (SELF, CONT, A1, A2, X01–X04) are pinned to ARM hardware
registers; the rest spill to a shadow register file. Tail calls resolve through a
code-table index and a single BX, with no stack growth. Integer addition and
subtraction reduce to two ARM instructions by exploiting the packed value
representation; pattern matching compiles to a TBH jump table.


6.4   Verifying the VM with rocq-of-rust

encore_vm is no_std Rust with minimal unsafe and no trait objects. The
rocq-of-rust tool [5] translates Rust source to Rocq definitions, enabling cor-
rectness proofs of Rust programs inside Rocq. Applying it to encore_vm closes
the last gap in the trust chain: the same proof assistant that certifies the firmware
logic certifies the runtime executing it.
    The central theorem to establish is a simulation between the abstract CPS
operational semantics and the concrete interpreter: each step of the Rust dispatch
loop corresponds to a reduction in the Gallina model. Two components present the
main proof obligations. The mark-compact GC requires reasoning about pointer
aliasing and the preservation of the tag-byte invariant across every collection cycle,
since the compaction phase rewrites every live pointer in both the register file and
the heap interior. The ENCORE dispatch opcode must be shown to faithfully
resolve the callee’s code pointer and to preserve the register-file state prescribed
by the calling convention. The unsafe surface of encore_vm is intentionally small
and confined to these two subsystems, which keeps the verification perimeter
tractable and aligns naturally with how rocq-of-rust models Rust ownership
as Rocq separation-logic predicates.


7     Conclusion

We have shown that Rocq-proven firmware logic runs on a Cortex-M35P: extracted
to Scheme, compiled by Encore!, and deployed on a Ledger Flex hardware wallet.
The verified core remains the source of truth, while the runtime, compiler, host
callbacks, and device I/O are explicit trusted components.
    The architecture also scales. Structuring firmware as a pure state-transition
function decouples verification effort from hardware complexity: the verified step
grows freely with application logic while the unverified components size stays
constant.
    As code generation becomes cheaper, assurance cost only stays manageable if
verification is part of the architecture. Theorem signatures and Rocq checking
make that path natural for the firmware core.
    Engineering work remains, but the hard question is answered: proven logic
runs on bare metal, at scale, today.
14      V. Bergeron and K. Gorna

Acknowledgments
The authors thank Nicolas Iooss for their valuable contribution and the Ledger
Backend and Ledger Donjon teams for their support.


References
 1. Anand, A., Appel, A.W., Morrisett, G., Paraskevopoulou, Z., Pollack, R., Savary
    Belanger, O., Sozeau, M., Weaver, M.: CertiCoq: A verified compiler for Coq.
    In: Proceedings of the Workshop on Coq for Programming Languages (Co-
    qPL) (2017), https://www.cs.princeton.edu/~appel/papers/certicoq-coqpl.
    pdf, co-located with POPL 2017
 2. Anonymous: Encore!, https://anonymous.4open.science/r/encore-88E5, anony-
    mous repository, accessed 2026
 3. Appel, A.W.: Compiling with Continuations. Cambridge University Press (1992)
 4. Blaauwbroek, L., Urban, J., Geuvers, H.: The tactician: A seamless, interactive
    tactic learner and prover for Coq. In: Intelligent Computer Mathematics (CICM
    2020). Lecture Notes in Computer Science, vol. 12236, pp. 271–277. Springer (2020).
    https://doi.org/10.1007/978-3-030-53518-6_17
 5. Claret, G., contributors: rocq-of-rust: Formal verification of Rust programs in Rocq
    (2024), https://github.com/formal-land/rocq-of-rust
 6. de Moura, L., Ullrich, S.: The Lean 4 theorem prover and programming language.
    In: Automated Deduction – CADE 28. Lecture Notes in Computer Science, vol.
    12699, pp. 625–635. Springer (2021). https://doi.org/10.1007/978-3-030-79876-5_37
 7. Elvers, M.: Multi domain OCaml on Raspberry Pi Pico 2 microcontroller (Dec
    2025), https://www.tunbury.org/2025/12/31/ocaml-pico/, accessed: May 2026
 8. Hendrix, J.: System programming using Lean 4 (community discussion). Lean4
    Zulip Chat Archive (2021), https://leanprover-community.github.io/archive/
    stream/270676-lean4/topic/System.20programming.20using.20Lean.204.
    html, galois, Inc. Accessed: 2025
 9. Kennedy, A.: Compiling with continuations, continued. In: Proceedings of the 12th
    ACM SIGPLAN International Conference on Functional Programming (ICFP 2007).
    pp. 177–190. ACM (2007). https://doi.org/10.1145/1291151.1291179
10. Klein, G., Elphinstone, K., Heiser, G., Andronick, J., Cock, D., Derrin, P., Elkaduwe,
    D., Engelhardt, K., Kolanski, R., Norrish, M., Sewell, T., Tuch, H., Winwood, S.:
    seL4: Formal verification of an OS kernel. In: Proceedings of the 22nd ACM
    Symposium on Operating Systems Principles (SOSP 2009). pp. 207–220. ACM
    (2009). https://doi.org/10.1145/1629575.1629596
11. Korkut, J., Stark, K., Appel, A.W.: A verified foreign function inter-
    face between Coq and C. Proc. ACM Program. Lang. 9(POPL) (2025).
    https://doi.org/10.1145/3704854
12. Kumar, R., Myreen, M.O., Norrish, M., Owens, S.: CakeML: A verified im-
    plementation of ML. In: Proceedings of the 41st ACM Symposium on Prin-
    ciples of Programming Languages (POPL 2014). pp. 179–191. ACM (2014).
    https://doi.org/10.1145/2535838.2535841
13. Kurucz, G.: Porting Lean to the ESP32-C3 RISC-V microcontroller (Jul 2024),
    https://kuruczgy.com/blog/2024/07/31/lean-esp32/, accessed: 2025
14. Lean FRO: The Lean FRO year 3 roadmap (2025), https://lean-lang.org/fro/
    roadmap/y3, covering August 2025 – July 2026. Accessed: May 2026
                                                        From Rocq to Metal         15

15. Leroy, X.: Formal verification of a realistic compiler. Communications of the ACM
    52(7), 107–115 (2009). https://doi.org/10.1145/1538788.1538814
16. Letouzey, P.: A new extraction for Coq. In: Types for Proofs and Programs (TYPES
    2002). Lecture Notes in Computer Science, vol. 2646, pp. 200–219. Springer (2003).
    https://doi.org/10.1007/3-540-39185-1_12
17. Letouzey, P.: Extraction in Coq: An overview. In: Logic and Theory of Algorithms
    (CiE 2008). Springer (2008)
18. Neis, G., Hur, C.K., Kaiser, J.O., McLaughlin, C., Dreyer, D., Vafeiadis,
    V.: Pilsner: A compositionally verified compiler for a higher-order imperative
    language. In: Proceedings of the 20th ACM SIGPLAN International Confer-
    ence on Functional Programming (ICFP 2015). pp. 166–178. ACM (2015).
    https://doi.org/10.1145/2784731.2784764
19. Shinn, A.: Chibi-scheme, https://github.com/ashinn/chibi-scheme, accessed:
    2025
20. St-Amour, V., Feeley, M.: PICOBIT: A compact Scheme system for microcontrollers.
    In: Implementation and Application of Functional Languages (IFL 2009). Springer
    (2009)
21. Varoumas, S., Vaugon, B., Chailloux, E.: OMicroB: An OCaml generic virtual
    machine for microcontrollers, https://github.com/stevenvar/OMicroB, accessed:
    May 2026
22. Varoumas, S., Vaugon, B., Chailloux, E.: WCET of OCaml bytecode on micro-
    controllers. In: 19th International Workshop on Worst-Case Execution Time Anal-
    ysis (WCET 2019). Schloss Dagstuhl – Leibniz-Zentrum für Informatik (2019),
    https://drops.dagstuhl.de/opus/volltexte/2019/10770/
23. Yvon, S., Feeley, M.: A small scheme VM, compiler, and REPL in 4k. In:
    Proceedings of the 13th ACM SIGPLAN International Workshop on Virtual
    Machines and Intermediate Languages (VMIL 2021). pp. 14–24. ACM (2021).
    https://doi.org/10.1145/3486606.3486783
