                                                     Refactoring and Equivalence in Rust
                                         Expanding the REM Toolchain with a Novel Approach to Automated Equivalence
                                                                           Proofs


                                                                          Matthew Britton
                                                         School of Computing, Australian National University
                                                                    matthew.britton@anu.edu.au
                                                                             Sasha Pak
arXiv:2601.19207v1 [cs.PL] 27 Jan 2026




                                                         School of Computing, Australian National University
                                                                      sasha.pak@anu.edu.au
                                                                           Alex Potanin
                                                         School of Computing, Australian National University
                                                                     alex.potanin@anu.edu.au


                                                                                    Abstract

                                               Refactoring tools are central to modern software development, with extract-function
                                           refactorings used heavily in day-to-day work. For Rust, however, the combination of own-
                                           ership, borrowing, and advanced type system features makes automated extract-function
                                           refactoring particularly challenging. Existing tools, including the original Rusty Extrac-
                                           tion Maestro (REM) prototype, either rely on slow, compiler-based analysis, support only
                                           a restricted fragment of the language, or provide little assurance beyond “it still compiles”.
                                               This paper presents REM2.0, a new extract-function and verification toolchain for Rust.
                                           REM2.0 works on top of rust-analyzer as a persistent daemon, reusing its analysis in-
                                           frastructure to provide low-latency extract-function refactorings with a VSCode front-end.
                                           On top of this extraction engine, it adds a repairer that automatically adjusts lifetimes and
                                           function signatures when extraction exposes borrow-checker issues, and an optional verifi-
                                           cation pipeline that connects to CHARON and AENEAS to generate Coq proofs of equivalence
                                           between original and extracted functions for a supported subset of Rust.
                                               The architecture is evaluated on three benchmark suites. First, on the original REM
                                           artefact (being forty cases drawn from real projects like gitoxide), REM2.0 achieves 100%
                                           compatibility: it matches all original successes of the prototype and fixes several previous
                                           failures. It also reduces extraction latency from an average of around a thousand mil-
                                           liseconds to low single-digit milliseconds inside the daemon and well under a quarter of a
                                           second as perceived in the editor. Second, on a new corpus of forty feature-focused ex-
                                           tractions from twenty highly starred GitHub repositories, REM2.0 successfully handles the
                                           majority of examples involving async/await, const fn, non-local control flow, generics,
                                           and higher-ranked trait bounds, with remaining failures concentrated around dynamic trait
                                           objects and complex generic bounds. Third, on a set of twenty verification benchmarks, the
                                           CHARON/AENEAS pipeline is able to construct end-to-end equivalence proofs for those
                                           cases that fall within its current subset, at a significantly higher performance cost than
                                           extraction but with correspondingly stronger guarantees.


                                                                                         1
          Overall, the results show that a Rust Analyzer based design can provide fast, feature-rich
      extract-function refactoring for real Rust programs, while an opt-in verification pipeline can
      deliver machine-checked behaviour preservation for safety-critical refactorings. REM2.0 is
      therefore able to offer a highly practical path toward routinely verified refactoring in the
      Rust ecosystem.


1     Introduction
Rust is a modern systems language that combines low-level control with strong safety guar-
antees [1]. This is very different to previous norms, where a programmer had to make the
choice between low-level control (with languages such as C/C++) and memory safety (with
garbage collected languages such as Java). These guarantees, however, make automated refac-
toring—particularly “Extract Method”—far more complex than in garbage-collected languages.
Prior work such as Adventure of a Lifetime[2] and the Rusty Extraction Maestro (REM)
prototype[3] demonstrated that automated extraction in Rust is possible, but only within a
narrow fragment of the language and with heavy dependence on unstable tooling.

This project revisits the problem from first principles, redesigning REM into a standalone,
Rust-Analyzer (RA) driven toolchain capable of handling real-world Rust features such as
async/await, generics, trait objects, and const contexts, whilst also bringing the execution
time down by a factor of five. We also introduce an optional verification pipeline to check that
extractions preserve behaviour. Together, these contributions aim to make safe, semantics-
preserving extract-method refactoring practical for everyday Rust development rather than a
research prototype.
1.1   Context and Motivation
Modern software is rarely written from scratch. Instead, engineers spend much of their time
extending, adapting, and repairing existing codebases. As systems grow, crates gain more
responsibilities, functions become longer, and dependencies become more complex. Without
a deliberate effort to manage this complexity, technical debt rapidly accumulates and future
changes become increasingly costly. Refactoring, the task of restructuring a program’s internals
without altering its observable behaviour—is one of the main tools developers use to keep
codebases maintainable.

Empirical evidence suggests that refactoring is not an occasional clean-up, but a routine part
of development practice. A large-scale survey of 1,183 developers by JetBrains found that most
respondents refactor at least weekly, and many reported spending an hour or more in a single
refactoring session [4]. This indicates that refactoring is both widespread and potentially time-
consuming when performed manually, and that tool support plays an important role in enabling
small, safe transformations to be applied regularly.

Within the broad scope of refactorings, Extract Method is one of the most common operations.
Given a contiguous block of code (for example, the body of a loop), Extract Method moves
that block into a new function and replaces the original code with a call to that function. This
improves readability by assigning a descriptive name to a piece of logic and shortening long


                                                    2
functions, and, by isolating the codes behaviour, we enable reuse and targeted unit testing.
In garbage-collected languages such as Java or C#, performing Extract Method is relatively
straightforward: the tool identifies the free variables in the selected fragment, turns them into
parameters or return values, and relies on the runtime to manage object lifetimes and mem-
ory.

Rust, however, presents additional challenges. As a modern systems programming language,
Rust provides C-like control over memory and performance while garunteeing of memory safety
through its ownership and borrowing model [1]. Rather than relying on garbage collection, the
compiler enforces a static discipline: each value has a unique owner; borrows are restricted in
number and kind; and lifetimes are tracked to ensure that references never outlive the data they
point to. This eliminates broad classes of bugs, such as use-after-free and many data races, but
also tightly couples control-flow structure, data ownership, and aliasing patterns.

As a consequence, naı̈vely reusing Extract Method algorithms from garbage-collected languages
does not work in Rust. Moving code into a new function can change which scope owns a value
or how many mutable and immutable references to that value are simultaneously in play. A
transformation that appears harmless at the level of syntax may cause the borrow checker to
reject the program, or may alter which parts of the program are permitted to mutate shared
state. Even when behaviour is preserved, the transformed code may require explicit lifetime
parameters or more complex type signatures, making it harder for developers to read and
maintain.

Rust is increasingly used for performance-critical and safety-critical infrastructure. In these
domains, developers want both the maintainability benefits of refactoring and the safety guar-
antees that motivate the use of Rust. If refactoring tools frequently break compilation, produce
unreadable code, or fail to support common language features such as async/await , closures,
and generics, developers are less likely to rely on them and may instead resort to manual editing
or just ignoring the problem.

Prior work has shown that non-trivial Extract Method refactoring in Rust is possible. In par-
ticular, Adventure of a Lifetime (AoL) and the associated Rusty Extraction Maestro (REM)
prototype introduced a Rust-specific refactoring pipeline that explicitly reasons about owner-
ship, borrowing, and non-local control flow [2]. However, the original REM implementation is
tightly coupled to an outdated IntelliJ IDEA-based Rust frontend and heavily relies on highly
unstable rustc internals, which at best result in behaviour changes from one version of rustc
to the next. It also provides no guarantees of semantic preservation beyond the informal assur-
ance of passing tests. This project is motivated by the gap between the clear need for robust
refactoring support in real-world Rust development and the current lack of comprehensive,
lifetime-aware tools that integrate into modern Rust workflows.
1.2    Problem Statement
Current IDE support for Extract Method in Rust is adequate for simple cases, but limited
when code involves realistic borrowing patterns, complex generics, macros, or asynchronous
constructs. Tools such as RA and the IntelliJ-based plugins generally succeed on small, local


                                               3
fragments, but tend either to refuse more complex refactorings or to produce code that no
longer compiles. They also do not attempt to repair lifetimes or ownership, and they provide
no guarantees that the refactoring has preserved behaviour.

The Rusty Extraction Maestro (REM) prototype from Adventure of a Lifetime [2] addressed
some of these shortcomings by introducing Rust-specific analyses and, in particular, an auto-
mated lifetime and ownership repair loop. After applying an Extract Method transformation,
REM iteratively adjusts the extracted function’s signature in response to compiler feedback un-
til the borrow checker accepts it. To the best of our knowledge, this form of automated lifetime
repair is not available in any other refactoring tool for Rust. However, REM remains a research
prototype: it is tied to an obsolete IntelliJ-based frontend and fragile rustc internals, it incurs
substantial latency due to repeated cargo check invocations, and its support for advanced lan-
guage features such as async / await , closures, complex generics, macros, and partial moves of
struct fields is non-existent.

A further limitation, shared by both REM and IDE-native refactorings, is the lack of strong
guarantees that transformations preserve program behaviour. REM performs complex struc-
tural changes, including modifications to function boundaries and ownership patterns, and may
introduce auxiliary types or explicit lifetime parameters. Test suites can provide some assurance
that the refactored program behaves as intended, but they are necessarily incomplete and only
indicate that an error exists, not where it was introduced. For a refactoring tool intended to
operate on non-trivial Rust code, there is a clear need for an updated design that combines
REM’s advanced lifetime-repair capabilities with modern toolchain support and a lightweight
verification pipeline that offers stronger evidence of behaviour preservation.
1.3   Project Aims
This project aims to turn the original REM prototype into a practical tool for modern Rust
development. The first goal is to re-engineer REM as a standalone pipeline that no longer relies
on outdated IntelliJ-based infrastructure or fragile rustc internals, and to extend its Extract
Method capabilities to better handle modern Rust language features such as async / await ,
closures, macros, and more complex uses of generics.

The second goal is to connect our Extract Method refactorings to a equivalence checking path-
way that can provide stronger evidence of semantic preservation than tests alone. Specifically,
the project aims to integrate REM with existing verification-oriented toolchains (in particular
CHARON and AENEAS) so that refactorings can be translated into a form suitable for logical
reasoning about equivalence between the original and refactored code.

The third goal is to expose all of this new functionality through an interface that fits naturally
into existing workflows. This includes a command-line interface suitable for scripting and batch
evaluation, as well as a Visual Studio Code extension that allows developers to invoke REM
directly from the editor. A longer-term ambition, which is beyond the scope of this project, is
to explore integration with RA itself, for example by reusing its intermediate representations
more directly or embedding a subset of REM’s analysis into the language server.




                                                4
1.4   Key Contributions
To achieve these aims, this project makes the following contributions:

A re-engineered REM core for modern toolchains. The original REM implementation
has been refactored into a standalone Extract Method pipeline that decouples the analysis and
transformation logic from the obsolete IntelliJ-based frontend and fragile rustc internals. The
new daemon based approach is readily compatible with existing IDEs and workflows.
Integration with Rust Analyzer for fast, in-memory analysis. The project introduces
a new extraction engine that builds on RA’s semantic information and in-memory workspace
model. This gives REM2.0 a far deeper semantic understanding of code than previous AST-
based approaches.
Extended extraction coverage for modern Rust features. The Extract Method pipeline
has been extended to support a broad range of real-world Rust constructs including selected
uses of async/await, generics, non-local control flow, const evaluation, and higher-ranked trait
bounds.
Editor/IDE integration via rem-server and VSCode. The core implementation is ex-
posed as rem-server, a long-running JSON-RPC process suitable for integration with arbitrary
IDEs. A lightweight CLI and prototype VSCode extension demonstrate practical usage today.1
A prototype equivalence checking pipeline using CHARON and AENEAS. REM2.0
leverages recent advances in program verification to translate Rust into proof-oriented func-
tional languages such as Coq, enabling automated behavioural equivalence checking for Extract
Method refactorings.
An empirical evaluation on many real-world Rust projects. We evaluate the REM
pipeline across a suite of widely used Rust projects, measuring coverage, performance, and fail-
ure modes. This demonstrates that the new architecture preserves REM’s strengths—particularly
automated lifetime and ownership repair—while significantly improving practical applicability
and language coverage.
1.5   Method Overview and Scope
At a high level, this project constructs a multi-stage Extract Method pipeline for Rust and eval-
uates it on real-world codebases. The core extraction and analysis stages reuse RA’s in-memory
workspace and semantic information to identify candidate fragments and generate initial refac-
torings. A dedicated repairer then processes the extracted functions fixing lifetimes, and own-
ership patterns until the transformed code is valid Rust. For a selected subset of examples, the
original and refactored programs are translated via CHARON and AENEAS into verification-
oriented intermediate representations, enabling reasoning about semantic preservation. The
resulting toolchain is exposed through a JSON-RPC server (rem-server)2 , a lightweight CLI
(rem-cli)3 , and a Visual Studio Code extension, and is evaluated on a suite of open-source
Rust crates. The scope of this work is limited to Extract Method refactorings; other refactoring
operators are not considered. Support for macros and very complex generic patterns remains
partial, and the verification pipeline is applied only to representative case studies rather than
   1
     REM-VSCode is available on the VSCode marketplace, https://marketplace.visualstudio.com/items?
itemName=MatthewBritton.remvscode
   2
     https://crates.io/crates/rem-server
   3
     https://crates.io/crates/rem-command-line


                                                5
entire codebases. Full integration into RA itself is treated as a long-term direction rather than
an immediate goal.


2     Background
Rust’s ownership and borrowing discipline makes it possible to write memory-safe, data-race–free
systems code without a garbage collector, but it also raises the bar for both automated refactor-
ing and formal reasoning about program behaviour [1, 5]. This section surveys the background
needed for the rest of this report. We begin by reviewing refactoring and, in particular, the
Extract Method transformation. We then introduce Rust’s ownership, borrowing, lifetimes, and
control-flow features, and explain how they interact with Extract Method. Building on this, we
describe prior work on automated refactoring for Rust, with a focus on Adventure of a Lifetime
and the Rusty Extraction Maestro (REM) prototype [2, 3]. Finally, we outline relevant work
on verification and formal semantics of Rust, and briefly discuss existing tooling and IDE inte-
gration. Together, these sections position the contributions of this project within the current
state of the art in making Rust code easier to evolve and reason about.
2.1   Overview of Refactoring
Refactoring is the process of restructuring existing code to improve its internal structure without
changing its externally observable behaviour. It is a key practice for improving code maintain-
ability and controlling technical debt in large software projects [4]. Modern IDEs such as Eclipse
and IntelliJ IDEA provide a wide range of automated refactorings, allowing developers to apply
semantics-preserving transformations quickly and, in principle, safely [2, 6].

As discussed in Section 1.1, empirical studies show that refactoring is a routine part of profes-
sional development, but automated refactoring tools are not always used to their full potential.
Developers often prefer manual edits, either because they are unfamiliar with the available refac-
torings or because they are unsure whether the tool will preserve behaviour. This motivates
research into refactoring tools that are both more reliable (through stronger guarantees) and
more transparent in how they operate.

In this report we focus on the Extract Method refactoring, already introduced in Section 1.1. In
the refactoring space, Extract Method is often treated as a basic building block: a contiguous
block of code is moved into a newly created function, and the original code is replaced by a
call to that function. This is used to split long methods into smaller units, to isolate cohesive
behaviour, and as a stepping stone for more complex refactorings such as Extract Class or
Move Method [6]. In garbage-collected languages such as Java or C#, most implementations
are largely syntactic: they identify the free variables within the selected fragment, turn them
into parameters or return values, and rely on the runtime to manage object lifetimes and
memory.
                                                      1   // Before:
The Java example in Listing 1 illustrates this        2   public void doComplicatedWork(List<Integer> nums) {
style of transformation in a language where ex-       3       int sum = 0;
                                                      4       for (int n : nums) { // Consider this as a
plicit memory management is not a concern.
                                                      5           sum += n;        // Lengthy piece of
A long method containing, for instance, in-           6       }                    // Business logic


                                                  6
put validation and transformation logic can be              7       System.out.println("Sum is: " + sum);
                                                            8   }
refactored by selecting the validation block, ex-
                                                            9
tracting it into a dedicated method, and replac- 10             // After:
ing the original block with a call. The resulting       11      public void doComplicatedWork(List<Integer> nums) {
                                                        12          int sum = doSmallPartOfWork(nums); // Logic is
code is clearer, and the validation can be tested                    now reusable
in isolation without changing the behaviour of 13                   System.out.println("Sum is: " + sum);
                                                        14      }
the program.                                            15      // This function can be unit tested on its own
                                                        16      private int doSmallPartOfWork(List<Integer> nums) {
                                                        17          int sum = 0;
                                                        18          for (int n : nums) {
                                                        19              sum += n;
                                                        20          }
                                                        21          return sum;
                                                        22      }



                                                                Listing 1: Example of Extract Method refac-
                                                                toring in Java

In Rust, the high-level intent of Extract Method is the same, but the transformation interacts
with ownership, borrowing, and lifetimes in ways that do not arise in typical garbage-collected
languages. Understanding these language features is therefore essential before discussing auto-
mated Extract Method refactoring for Rust.
2.2    Rust’s Ownership Model & Semantics
Rust enforces memory safety through a static ownership and borrowing discipline. Each value
has a unique owner; when the owner goes out of scope, the value is dropped4 . Instead of
relying on a garbage collector, Rust uses the type system and a compile-time borrow checker to
prevent use-after-free, data races, and other common memory errors [1, 5, 8]. Similar ownership
disciplines have been explored in other languages, notably through generic ownership types for
Java [9, 10]. While these guarantees are attractive for systems programming, they complicate
both manual and automated program transformations, including Extract Method.




   4
     We recommend reading this section of Rust By Example [7] to better understand lifetimes if this is your first
encounter!
https://doc.rust-lang.org/rust-by-example/scope/lifetime.html


                                                        7
    2.2.1    Ownership and Moves
                                                            1    fn main() {
    At the core of Rust’s model is the idea that            2        let s1 = String::from("Hello");
    each value has a single owner. Assigning or             3        let s2 = s1; // Ownership of the string data
                                                                      moves to s2
    passing a value typically moves ownership to a
                                                            4        // The following line would be invalid if
    new variable or function, leaving the previous                    uncommented:
    binding invalid. Listing 2 on the right shows a         5        // println!("{}", s1);
                                                            6        // ^ value borrowed here after move
    simple example:                                         7        println!("{}", s2); // Prints "Hello"
                                                            8    }



                                                                    Listing 2: Ownership and moves in Rust

    In this example, the value is moved from s1 to s2, making s1 unusable afterwards. An Extract
    Method transformation that passes s1 into a new function by value may therefore change which
    scope owns the value or when it is dropped. Automated refactoring tools must account for these
    moves to avoid introducing subtle ownership bugs or compilation failures.

    2.2.2    Borrowing

    Instead of transferring ownership, Rust encourages passing references. A value can be borrowed
    immutably (using &T ) any number of times, or mutably (using &mut T ) exactly once at a time.
    The borrow checker enforces that mutable and immutable borrows do not conflict, preventing
    data races and many classes of aliasing bugs [11]. Listing 1 illustrates the basic patterns.

1   fn print_message(message: &str) {                   1       fn add_exclamation(message: &mut String) {
2       println!("{}", message);                        2           message.push(’!’);
3   }                                                   3       }
4                                                       4
5   fn main() {                                         5       fn main() {
6       let greeting = String::from("Hello, world!");   6           let mut greeting = String::from("Hello");
7       print_message(&greeting); // Borrows greeting   7           add_exclamation(&mut greeting); // Borrows
         immutably                                                   greeting mutably
8       println!("Still own greeting: {}", greeting);   8           println!("{}", greeting);       // Prints "
9   }                                                                Hello!"
                                                        9       }
     (a) Immutable borrow: many readers allowed
                                                                      (b) Mutable borrow: a single writer

                                        Listing 1: Borrowing in Rust


    When a block of code is extracted into a new function, the tool must decide for each captured
    variable whether to move it, borrow it immutably, or borrow it mutably. Poor choices can cause
    the borrow checker to reject the refactored program or force the tool to introduce unnecessary
    clones that change performance characteristics. This is one of the core challenges for designing
    an Extract Method algorithm in Rust.




                                                        8
2.2.3    Lifetimes and Inference

The Rust compiler tracks how long references remain valid using lifetime parameters. Many
simple cases do not require explicit annotations because the compiler can infer relationships
between input and output lifetimes. For example, the function in Listing 2 can be written
without explicit lifetime parameters:

fn echo(message: &str) -> &str { message }

                            Listing 2: How we as developers write Rust code

Conceptually, the compiler treats this as if the programmer had written Listing 3, introducing
an explicit lifetime ’a shared by the argument and result:

fn echo<’a>(message: &’a str) -> &’a str { message }

                          Listing 3: How the Rust compiler “sees” Rust Code
When code is extracted into a new function, however, the relationships between references can
become more complex, and the compiler may no longer be able to infer lifetimes automatically.
In such cases, explicit lifetime parameters are required on the extracted function. Automated
refactoring tools must therefore be prepared to introduce, propagate, and most importantly
simplify lifetime annotations as part of the transformation.

2.2.4    Non-local Control Flow

Rust allows return , break , and continue inside nested blocks and loops. Extracting a frag-
ment that contains such statements into a separate function changes the control-flow structure:
an early return from the original function becomes a return from the extracted function
instead. Any realistic Extract Method implementation for Rust must either forbid such cases
or explicitly encode and reconstruct non-local control flow. This point will be revisited in the
discussion of the REM tool in Section 2.3.2.

Overall, Rust’s ownership, borrowing, lifetimes, and control-flow constructs provide strong
safety guarantees but tightly couple data flow, control flow, and scope. This makes even seem-
ingly local refactorings, such as Extract Method, significantly more complex than in more
permissive, garbage-collected languages.
2.3     Automated Refactoring Techniques for Rust
2.3.1    Renaming and Simple Refactorings

One of the first efforts to build a Rust refactoring tool was by G. Sam et al. (2017), who
created a proof-of-concept refactoring framework utilizing the Rust compiler’s internal APIs.
The team partnered with Mozilla Research5 to be among the first to implement the Rust specific
refactorings of Lifetime Elision and Lifetime Reification. This allowed their program to introuce
explicit lifetime parameters in instances where the compiler was implicitly inferring them - a
  5
    Mozilla Research were the first major sponsors of the Rust project, and have been a driving force in its
development over the last ten years. [12].
https://blog.mozilla.org/en/mozilla/mozilla-welcomes-the-rust-foundation/


                                                     9
refactoring that was brand new to Rust. The challenges encountered illustrated how Rust’s
stricter scoping and shadowing rules required careful handling of name conflicts during renaming
(e.g. avoiding situations where renaming a variable could unintentionally shadow another) [5].
Additionally, the 2017 study concluded that many refactorings are possible with Rust’s compiler
infrastructure, but ensuring behavioural preservation (especially around ownership transfers)
requires additional static analyses not needed in langauges without Rust’s constraints. Their
work on Lifetime Elision has since formed part of the REM toolchain, where the rich feedback
from the Rust compiler is leveraged to ensure that the final transformation is both valid Rust
and as legible as possible [2], [3].

2.3.2   Extract Method (REM)

A major advance in automated refactoring for Rust came with the Rusty Extraction Maestro
(REM). Costea et al.’s Adventure of a Lifetime: Extract Method Refactoring for Rust [2] in-
troduced the theoretical framework, and Thy et al.’s Borrowing Without Sorrowing provided
a practical implementation as an IntelliJ plugin [3]. REM tackles Extract Method in Rust by
decomposing it into a sequence of transformations, each designed to address a specific aspect
of Rust’s ownership, borrowing, lifetimes, and control flow.

The process begins with a naı̈ve hoisting step that moves the selected block of code into a new
function and replaces the original fragment with a call. This initial transformation is rarely well-
typed. REM then applies a series of automated repairs guided by specialised analyses called
oracles. An ownership analysis determines, for each value crossing the new function bound-
ary, whether it should be passed by value, by shared reference ( &T ), or by mutable reference
( &mut T ). Other passes reify non-local control flow by encoding early return , break , and
continue statements into an auxiliary enum, allowing the caller to reconstruct the original
behaviour by pattern matching on the result. A final repair loop iteratively invokes the Rust
compiler, uses the borrow checker’s error messages as feedback, and introduces or refines lifetime
parameters until the extracted function type-checks.

Figure 2 (adapted from [2]) shows the overall REM pipeline. Each phase is deliberately simple,
but their composition yields a transformation that can handle (mostly) realistic Rust code. In
an evaluation on real-world projects, REM was able to perform extractions that IDE tools could
not handle, including cases involving multiple interacting borrows and nested lifetimes [2]. To
the best of our knowledge, REM’s automated lifetime and ownership repair loop remains unique
among refactoring tools for Rust.
Despite these strengths, the original REM prototype is tightly coupled to an outdated IntelliJ-
based Rust frontend and unstable rustc internals, as discussed in Section 1. This limits its
applicability in modern toolchains. Our project builds on the conceptual design of REM, par-
ticularly its lifetime and ownership repair capabilities, while re-engineering the implementation
around Rust Analyzer and a standalone daemon architecture to make Extract Method refac-
toring practical for contemporary Rust development.




                                                10
        Figure 2: Overview of the REM extract-method pipeline (after Costea et al. [2])


2.3.3    Automated Fixes for Ownership Errors

Another line of work relevant to Rust refactoring focuses on automatically repairing code that
violates ownership or borrowing rules—transforming non-compiling programs into compiling
ones without altering semantics. Rust-Lancet (Yang et al., ICSE 2024) targets exactly this
problem, aiming to fix ownership-rule violations while preserving behaviour. Given a Rust
file that fails to compile, Rust-Lancet analyses its AST using syn and quote, applies targeted
transformations, and repeatedly rechecks the program until the error is eliminated. Typical
repairs include inserting a clone() to satisfy ownership constraints or reordering statements
to avoid invalid borrows. Crucially, Rust-Lancet includes a behaviour-preservation check: it
validates that each proposed fix does not change observable program output, using a specialised
semantics for reasoning about programs that do not yet compile.

Across 160 real ownership violation cases, Rust-Lancet successfully repaired a large majority
with zero false positives—never introducing an incorrect fix—outperforming both compiler sug-
gestions and several LLM-based baselines. Although positioned as a bug-fixing tool rather
than a refactoring engine, its pipeline of semantics-preserving AST rewrites overlaps strongly
with automated refactoring. Their results highlight how Rust’s strict ownership model can
guide automated transformations: once the compiler accepts the repaired code and behaviour-
preservation checks succeed, the tool can be confident the patch is correct [13].
2.4     Verification and Formal Methods for Rust
Rust’s appeal for building reliable systems has driven a lot of active work and research into
formal semantics and verification. Traditional deductive verification and model checking must
be adapted to account for Rust’s ownership, lifetimes, and unsafe code, but Rust’s strong
static guarantees also make many verification tasks much more manageable when compare to
traditional approaches for C or C++.

2.4.1    RustBelt and Type-System Soundness

Jung et al.’s RustBelt gives the first machine-checked soundness proof for a realistic subset
of Rust’s type system [14]. By embedding a Rust-like calculus (λRust) in the Iris concurrent
separation logic and linking it to low-level memory models, RustBelt shows that well-typed safe
Rust code cannot exhibit undefined behaviour, even when using libraries that contain unsafe
internals. This foundational result allows later work to assume that safe Rust is memory and

                                               11
thread-safe and focus verification effort either on functional correctness or on carefully selected
unsafe fragments.

2.4.2     Verification via Functional Translation

A complementary approach is to translate Rust programs into pure functional languages that
work with existing proof assistants and verifiers. The CHARON6 /AENEAS7 toolchain follows
this strategy. CHARON translates Rust into an intermediate representation called Low-Level
Borrow Calculus (LLBC), which is related to Rust’s MIR but makes the ownership and bor-
rowing structure explicit. AENEAS then assigns a pure, value-based semantics to LLBC and
translates it into a lambda calculus suitable for verification in tools such as Coq or F* [15, 16].
This approach builds on a long tradition of encoding language semantics in proof assistants [17].
For a large class of Rust programs, this translation eliminates the need to reason about pointers
and heaps directly: proof engineers can work with a pure functional model, while the design
of CHARON/AENEAS guarantee that proved properties carry back to the original Rust code.
Indeed later in this report, (Section 4.4) we will rely on this guarantee to back our verification
pipeline.

More recently, Ho et al. introduced symbolic semantics for Rust and showed that they form a
sound abstraction of concrete heap-based execution for LLBC programs [16]. A key outcome
is a verified symbolic interpreter that can serve as a proven-correct borrow checker for LLBC.
This provides strong assurance that tools built on CHARON/AENEAS rest on a solid semantic
foundation and, crucially, the have established a bridge between Rust’s informal ownership
intuition and a mathematically precise model.

2.4.3     Static Analysers and Model Checkers

Beyond full functional verification, several tools provide lighter-weight guarantees for Rust.
Prusti translates annotated Rust code into the Viper verification language, using Rust’s own-
ership and lifetime information to encode permissions and prove user-specified pre- and post-
conditions and invariants [18, 19]. RefinedRust extends this idea with a refinement type system
for Rust, allowing rich safety and correctness properties to be expressed as types and discharged
in Coq, even for some unsafe code [20].

On the model-checking side, Kani is a bounded model checker for Rust that operates on MIR
and generates verification conditions for a SAT/SMT solver [21]. By working at the MIR
level, Kani can reason precisely about traits, generics, and dynamic trait objects [22], and
has been applied to critical components such as cryptographic libraries. Dynamic analysers
like Miri complement these tools by executing Rust programs in an interpreter that detects
undefined behaviour, providing strong testing-time checks even when full verification is not
attempted.

Together, RustBelt, CHARON/AENEAS, Prusti, RefinedRust, Kani, and Miri outline a rich
verification ecosystem. They demonstrate that Rust’s ownership discipline is not only a con-
straint
   6    but also a powerful abstraction layer that verification tools can exploit.
      https://github.com/AeneasVerif/charon/
  7
      https://github.com/AeneasVerif/aeneas



                                                12
2.5   Integration with IDEs and Langauge Servers
For refactoring and verification tools to be adopted in practice, they must integrate smoothly
into developers’ workflows. For Rust, this has centred on the compiler and the Language Server
Protocol (LSP). The original Rust Language Server (RLS) attempted to repurpose rustc’s
internals for IDE support, but struggled with performance and keeping pace with language
evolution. The community has since converged on Rust-Analyzer (RA), a language server that
maintains its own syntax trees and performs incremental type inference to answer editor queries
quickly [23]. RA exposes refactorings and code transformations as ”assists” that operate on its
internal representation; and these already include many common refactorings.

Industrial IDEs have also hosted Rust refactoring research. The original REM prototype was
implemented as an extension to the IntelliJ Rust plugin, showing that research-grade refactor-
ings can be prototyped on top of existing editor infrastructure [2, 3]. In practice, maintaining
such integrations is challenging: IDE APIs and Rust tooling both evolve rapidly. To miti-
gate this, some tools deliberately avoid rustc internals and instead rely on stable crates like
syn/quote for parsing and code generation, as in Lancet’s design [13].

At the compiler level, projects like rustfix show another style of integration: rustc emits
machine-applicable suggestions for certain errors and deprecations, which rustfix can apply
automatically across a codebase. While not a general refactoring engine, this mechanism enables
small-scale, behaviour-preserving edits (for example, updating deprecated syntax or inserting
missing lifetime specifiers) driven directly by the compiler. As Rust’s stable analysis APIs
mature and RA’s assist framework expands, there is increasing scope for external tools—such
as the rem-server daemon described in this report—to plug into these ecosystems and offer
more advanced, semantics-aware refactorings without being tied to a single IDE.
2.6   Related Work Beyond Rust
Many of the challenges and opportunities in Rust refactoring echo earlier work in other lan-
guages. Java and C# have long enjoyed mature IDE support for refactorings such as Rename,
Extract Method, and Extract Class, and this ecosystem has inspired a large body of research.
Beyond classic examples such as generic-aware refactoring [24], more recent work has focused
on systematic migration to new language features. Zhang et al.’s ReFuture tool, for example,
automatically refactors Java asynchronous code to use the modern CompletableFuture API
by combining static analyses (visitor patterns, alias analysis) with transformation rules, and has
been evaluated on large projects such as Hadoop and ActiveMQ [25]. In the mobile domain,
Lin et al.’s ASYNCDROID refactors problematic uses of Android’s AsyncTask into safer con-
structs such as IntentService , addressing common sources of leaks and UI bugs and showing
that domain-specific refactoring rules can be packaged as an IDE plugin [26].

Refactoring has also been studied in other paradigms and ecosystems. In Haskell, the HaRe
tool brought structured refactoring to a lazy, purely functional language, handling challenges
such as type classes and non-strict evaluation [27]. In dynamic languages like JavaScript and
Python, the lack of static types has led to refactoring approaches that rely on heuristics, runtime
analysis, or developer-guided transformations. Meanwhile, tools such as Facebook’s JSCodeshift


                                                13
and Python’s Bowler allow developers to script custom codemods over ASTs[28].

Finally, refactoring is closely linked to adjacent areas such as code smell detection, automated
program repair, and large-scale migrations. Some repair systems use refactoring-like transfor-
mations as behaviour-preserving steps to simplify buggy code before or after applying a fix,
and language servers increasingly act as a common backbone for these capabilities across many
editors [2]. The Rust work surveyed in this section fits into this broader landscape: it adapts
ideas from mature ecosystems (Java, Android, & Haskell) to a language whose ownership-based
semantics demand specialised analyses, but whose strong guarantees can in turn be exploited
by refactoring and verification tools.


3     Expanding the Capabilities of REM
Automated refactoring in Rust has long been constrained by the languages strict ownership,
borrowing and lifetime rules. Early prototypes of the Rusty Extraction Maestro demonstrated
that Extract Method refactorings could be made effective, but only within relatively narrow
limits. Complex language features, such as generic types and asynchronous code, were not
supported. Moreover, the entire toolchain was reliant on a fragile integration with IntelliJ,
which quickly became outdated. As a result, REM remained an academic proof-of-concept
rather than a tool developers could realistically adopt.

This section details how REM has evolved from a fragile prototype into a robust, modular, and
extensible system. At its core, REM2.0 now operates through a streamlined, multi-component
pipeline designed for speed, flexibility, and integration with modern Rust workflows.

The REM server orchestrates the entire process through a JSON-RPC interface, coordinating
extraction, repair, and equivalence checking processes (the latter discussed in Section 4). The
extraction tool, built directly on top of Rust Analyzer’s incremental analysis engine, performs
lightning-fast semantic extraction while integrating the capabilities of REM’s original controller
and borrower modules. The repairer tool, adapted from the original REM toolchain, continues
to play a key role in resolving lifetimes and other semantic inconsistencies that may arise during
refactoring.

Finally, a prototype Visual Studio Code (VSCode) extension connects with the REM server to
deliver near-instant feedback—typically around 200 ms end-to-end (see Section 5). Together,
these components transform REM into a practical refactoring system capable of integrating
into everyday Rust development while preserving its foundation as a platform for continued
research.
3.1   Motivation: Why REM needed to change
The original REM prototype demonstrated that automated extract-method refactoring for Rust
was possible, but its design also exposed several fundamental limitations. At its core, REM
relied on repeated invocations of cargo check and a set of highly unstable rustc internals, as
well as the IntelliJ IDEA Rust plugin, which has since been superseded by RustRover and was
never particularly stable during the lifetime of this project. As a consequence, the toolchain


                                               14
    was slow, fragile, and extremely sensitive to minor changes in both the Rust ecosystem and
    the underlying editor integration. Its viability as anything beyond a research prototype was
    effectively non-existent: before any new work could begin, it took over a month of effort just to
    restore the original implementation to a usable state.

    These architectural choices also severely constrained the kinds of Rust programs that REM
    could handle. Even small, modern Rust fragments routinely use language features that REM was
    simply unable to process. For example, REM could not extract from even minimal asynchronous
    functions:
1   async fn fetch() {
2       let v = client.get("/").await; // REM failed to recognise the ‘await‘
3   }


    nor could it handle functions involving generic parameters or bounds:
1   fn min<T: Ord>(a: T, b: T) -> T { /* ... */ }


    and it struggled with non-local control flow such as break or return inside loops:
1   for x in xs {
2       if x < 0 { break; } // difficult for REM to lift cleanly into a new function
3   }


    Language features that are now commonplace in production codebases—such as async/await,
    const evaluation, generics with non-trivial bounds, trait objects, higher-ranked trait bounds,
    and non-local control flow8 —lay entirely outside REM’s reliably supported fragment. Although
    the original codebase contained many scattered TODOs mentioning future support for generics
    or async, there was no coherent plan for how to integrate such features into the pipeline. In
    practice, this meant that REM could sometimes operate successfully on specific large projects
    such as gitoxide, but in our testing, it would frequently fail or time out when faced with
    more complex codebases like Deno, Tokio, or Vaultwarden, where these advanced features are
    pervasive.

    Perhaps most importantly, REM provided no formal safety net. Its extraction decisions were
    driven largely by syntactic AST rewriting rather than a deep semantic understanding of the pro-
    gram, and there was no verification pipeline to check that transformations preserved behaviour.
    A refactoring could silently change program semantics while still compiling, and the tool had
    no mechanism to detect or prevent such regressions. Together, these limitations motivated a
    complete redesign of the system: if extraction was to be useful for everyday Rust development,
    REM had to become faster, more robust, feature-complete, and semantically trustworthy.

    3.2    High Level Vision: What REM2.0 Needed to Achieve
    REM2.0 was designed in response to these shortcomings with a clear set of high-level goals.
    The first was performance: the roughly one-second turnaround time of the original REM after
       8
        Non-local control flow is supported by REM, but its implementation relies on one-off custom generics rather
    than the modern std::ops::ControlFlow abstraction.


                                                          15
IntelliJ performed the initial extraction was unacceptable for an interactive refactoring workflow.
To feel natural inside an IDE, extraction had to complete in well under a second, ideally within
the sub-500 ms range. Achieving this required abandoning the “re-run the compiler” model in
favour of a persistent semantic engine. At the same time, REM2.0 needed to move beyond the
restricted language subset of its predecessor and support essentially any piece of real Rust code.
This meant handling async functions, const evaluation, generics (including complex bounds),
trait objects, higher-ranked trait bounds, and non-local control flow as real language features
rather than TODOs in the source tree.

A second, equally important, goal was accessibility. The original REM existed primarily as
a research artefact and demanded significant effort to build, configure, and operate; very few
everyday developers could realistically benefit from it. REM2.0, by contrast, is intended as
a tool that can be adopted with minimal friction: it should integrate cleanly with common
development workflows, expose its functionality through a familiar VSCode interface, and have
no interaction with unstable compiler internals9 . Behind the straightforward interface, the
system must still uphold strong correctness guarantees. Refactorings are deterministic and
built on a stable representation designed for reliable transformation and verification. With
help from a correctness backend, the tool ensures not only safety but behavioural equivalence.
In short, REM 2.0 aims to be fast, compatible with modern Rust, and never silently break
code.
3.3     REM2.0 At a Glance: Core Contributions
Before delving into architecture and implementation details, it is useful to summarise the key
contributions of REM2.0 at a high level. Collectively, the below changes / upgrades transform
REM from a fragile research prototype into a practical, extensible refactoring toolchain for
modern Rust.

• Rust-Analyzer-backed extraction engine. REM 2.0 replaces direct dependence on rustc
  internals and editor-specific plugins with a new extraction engine that uses Rust-Analyzer as
  its backend. A custom “single-file workspace” abstraction allows us to run extract-method
  relative to the current file while still benefiting from Rust-Analyzer’s full semantic analysis
  capabilities.
• Full language-feature coverage for extraction. Building on Rust-Analyzer’s capabilities,
  REM2.0 supports extraction in the presence of async functions, const evaluation, generics
  (including complex bounds), trait objects, higher-ranked trait bounds, and non-local control
  flow, rather than restricting itself to a narrow, hand-picked fragment of Rust.
• Preservation and extension of REM’s lifetime repair. The new system maintains all
  core capabilities of the original REM, in particular its ability to repair lifetime annotations
  and placements after extraction, while integrating these repairs into a far more useful and
  usable pipeline. REM2.0 gives the developer the ability to pick and choose between maximum
  correctness, maximum responsiveness, or a combination of the two.
• Verification backend for behavioural equivalence. REM2.0 introduces an end-to-end
   9
    The version of these internals available to the installed program is entirely dependent on the compiler being
used by the developer, and thus the original REM could be completely incompatible with a codebase.


                                                       16
  verification pipeline that translates extracted code through Charon and LLBC to Aeneas
  and Coq, where equivalence between the original and refactored functions can be proved (or
  refuted) automatically. See Section 3.6.1 and Section 4 for a full explanation.
• VSCode integration for interactive refactoring. A new VSCode extension exposes
  REM 2.0 as an interactive refactoring tool, providing extract-method commands, preview
  and undo functionality, and surfacing verifier results directly to the developer.

Together, these contributions establish REM 2.0 as a fast, feature-complete, and semantically
aware extract-method toolchain that is suitable both for research and for everyday Rust devel-
opment.
3.4       Overview of the REM2.0 Architecture

                                                     VS Code Extension
                                                   (Interactive Frontend)




                                                     REM Server
                                               (JSON-RPC Orchestrator)




                                                                                Verification Pipeline
       Extraction Engine                              REM Repairer
                                                                            (CHARON + AENEAS + Coq)
(Rust Analyzer–backed, single-file)                    (Lifetimes)
                                                                                     (Section 4)


 Figure 3: High-level overview of the expanded REM architecture: VS Code communicates
 bidirectionally with the REM Server, which dispatches to the Extraction Engine, the REM
                         Repairer, and the REM Verification pipeline.

The expanded REM architecture is organised around a modular, service-oriented design that is
able to decouple the interactive editing from semantic analysis and its surrounding logic. Figure
3 illustrates the system’s structure at the highest level.

At the centre of the system is the REM server, a lightweight orchestrator that exposes a JSON-
RPC (Remote Procedure Call) interface to the VSCode extension. The server can also be
rexported as a CLI to be integrated into local programs 10 . The server is responsible for
coordinating all major operations - extraction, repair, and verification, for handling errors and
for providing immediate feedback as to whether an operation is possible. Crucially, the interface
is completely generic, and has been designed to be very easily adaptable to any other IDE.

The extraction engine (REM Extract) forms the analytical core of the new toolchain. Built di-
rectly atop of Rust Analyzer, its key innovation is being able to perform semantic extraction over
a single source file rather than an entire crate. This adaptation is key to REM’s speed: whereas
Rust Analyzer typically analyses entire projects to populate its HIR (High-Level Intermediate
Representation), our engine is able to leverage internal features and interfaces to perform anal-
ysis on a single file without needing to consider the wider module / crate context. Given an
  10
       https://crates.io/crates/rem-command-line


                                                          17
extraction request (file path, selection range, function name), the engine constructs a
minimal semantic model of the file, determines the precise boundaries of the selection, and
synthesises the extracted function and corresponding call-site edits. The engine is also capable
of returning extract semantic information up the chain depending on the mode in which it is
called and the requirements of the downstream elements.

Once extraction is complete‘, the resulting transformation is then (optionally) passed into REM
Repairer. The repairer is a direct descendant of the original REM prototype but re-engineered
for performance and modularity. Its task is to reify and correct any missing lifetimes (as guided
by cargo check), before applying a series of lifetime elision rules to attempt to bring the
resultant mess into a form that is (mostly) human readable. The main algorithm is still the
same as was discussed in Adventure of a Lifetime [2], so we have omitted a large discussion of
it from this report.

Finally, the VSCode extension provides the user-facing layer of the system. Acting as a thin
client, it serialises extraction requests to the REM server and applies the returned edits to the
open buffer. Bidirectional communication over JSON-RPC enables sub-200 ms round-trip times
from user action to visual feedback. From the user’s perspective, REM behaves like a native
IDE feature rather than an external tool.

3.5     Single-File Workspaces over Rust-Analyzer
A central constraint for REM2.0’s speed is the ability to run extract-method on demand, without
re-analysing an entire project, or even really having access to the entire project. Rust-Analyzer
(RA), however, is designed around crate-level workspaces: it expects a Cargo.toml, a depen-
dency graph, and a complete module tree before it will perform semantic analysis. To bridge
this mismatch, REM2.0 constructs a lightweight, synthetic “single-file workspace” in which the
file currently being refactored is treated as an isolated crate. This workspace contains only the
minimum metadata necessary for RA to parse, index, and type-check the file.

This abstraction gives us fast, incremental semantics while avoiding the cost of repeatedly
analysing a full repository. However, as we discovered, a single-file workspace lacks any knowl-
edge of the standard library: types available by default such as Vec<T> , Option<T> , String ,
or even Result<T,E> are not available unless for some reason they have been explicitly imported
by the user. Rust-Analyser therefore assigns placeholder types (internally represented as “ ” or
incomplete inference variables) whenever an extracted function must reference a std-provided
type.

Figure 4 highlights just how significant this limitation is. Extracting Listing 4a should produce
the fully inferred function in Listing 4c, but in a single-file workspace (without std / core
loaded), RA instead generates the incomplete signature shown in Listing 4b. Because this
placeholder type propagates into the call site and return position, the resulting code no longer
compiles.




                                               18
1    fn main() {                      1   fn main() {                      1    fn main() {
2    //Rust-Analyzer(single-file) can’t
                                      2       let v = build_vec();         2        let v = build_vec();
3    //know what ‘Vec‘ is here.       3       println!("{:?}", v);         3        println!("{:?}", v);
4    //Even if ‘Vec‘ was strong typed 4   }                                4    }
5        let mut v = Vec::<i32>::new();
                                      5                                    5
6        for i in 0..10 {             6   //Rust-Analyzer’s *generated*     6   //With std in scope,
7            v.push(i);               7   //signature uses a placeholder    7   //This return type can be
8        }                            8   //as it can’t find ‘Vec‘          8   //Correctly inferred
9                                     9   fn build_vec() -> _ {             9   fn build_vec() -> Vec<i32> {
10        println!("{:?}", v);       10       let mut v = Vec::<i32>::new();
                                                                           10       let mut v = Vec::<i32>::new();
11   }                               11       for i in 0..10 { v.push(i); }11       for i in 0..10 { v.push(i); }
12   //                              12       v                            12       v
13   //                              13   }                                13   }


             (a) Original Code                 (b) Failed Extraction                 (c) Correct Extraction
                                               As std is out of scope               Now that std is in scope

       Figure 4: Comparison of an extraction prior to the std and core fixes and after. Before we
     return a ‘ ’ as a placeholder, as Rust-Analyzer is unable to infer the type without the semantic
                                        information provided by std.

     To address this problem, REM 2.0 constructs a second, persistent workspace containing the
     complete set of standard crates and their dependency graph. This workspace is initialised once
     when the VSCode extension starts (a one-time expensive step) and is assumed to remain stable
     across refactorings. During extraction, REM merges the semantic graphs of the std workspace
     and the single-file workspace, producing an “effective” workspace with full knowledge of both
     user code and the standard library. With this view, RA regains the ability to infer types such
     as Vec<T> correctly, restoring the fully inferred extraction shown in Listing 4c. The complete
     set of standard crates imported into this persistent workspace is shown alongside.
     To address this problem, REM2.0 constructs crate Idx::<CData>(0) -> core
     a second, persistent workspace containing the crate Idx::<CData>(1) -> compiler_builtins
                                                               crate Idx::<CData>(2) -> alloc
     complete set of standard crates and their de-
                                                               crate Idx::<CData>(3) -> panic_abort
     pendency graph. This workspace is initialised             crate Idx::<CData>(4) -> libc
     once when the VSCode extension starts (a one-             crate Idx::<CData>(5) -> unwind
     time expensive step) and is assumed to remain             crate Idx::<CData>(6) -> panic_unwind
                                                               crate Idx::<CData>(7) -> std_detect
     stable across refactorings. During extraction,
                                                               crate Idx::<CData>(8) -> cfg_if
     REM merges the semantic graphs of the std                 crate Idx::<CData>(9) -> hashbrown
     workspace and the single-file workspace, pro-             crate Idx::<CData>(10) -> rand_core
     ducing an “effective” workspace with full knowl-          crate Idx::<CData>(11) -> rand
                                                               crate Idx::<CData>(12) -> rand_xorshift
     edge of both user code and the standard library.
                                                               crate Idx::<CData>(13) -> rustc_demangle
     With this view, RA regains the ability to infer           crate Idx::<CData>(14) -> std
     types such as Vec<T> correctly, restoring the             crate Idx::<CData>(15) -> rustc_literal_escaper
     fully inferred extraction shown in Listing 4c.            crate Idx::<CData>(16) -> proc_macro
     The complete set of standard crates imported              crate Idx::<CData>(17) -> getopts
                                                               crate Idx::<CData>(18) -> test
     into this persistent workspace is shown along-
     side.                                                        Listing 4: Crates in the std workspace




                                                          19
3.5.1    Leveraging Rust-Analyzer’s Extract Method

With the effective workspace in place, REM2.0 relies directly on RA’s built-in Extract Function
assist. Instead of re-implementing extraction logic, REM2.0 issues the same internal request
that a client editor would send to RA: the file contents, the selected range, and a desired function
name. RA then returns a structured edit describing (1) a new function with fully inferred types,
generics, lifetimes, and where-clauses, and (2) a rewritten call site at the extraction point.

This delegation is critical. RA already contains sophisticated logic for name resolution, trait
and impl lookup, async/await de-sugaring, const evaluation, higher-ranked trait bounds, and
non-local control flow analysis. By using its extract-method implementation as the semantic
source of truth, REM2.0 inherits support for the full Rust language surface—including features
that would be prohibitively difficult or brittle to handle manually. It also allows REM2.0 to
fully benefit from years of active development in this space, allowing us to focus on expanding
the capability of the whole REM2.0 toolchain rather than attempting to rewrite something that
already exists. We are also able to query the semantic analysis returned by RA to improve the
repair and verification stages that come next.

REM 2.0 treats the edits returned by RA as a semantic blueprint, adapting them only as needed
for lifetime repair, call-site updates, and optional verification. Rather than maintaining its own
parallel program state, REM is able to query RA directly for any additional type or lifetime
information, allowing it to build on RA’s mature transformations while adding its own layers
of structure and correctness checking.
3.6     VSCode Integration and the REM Daemon
To make extraction accessible to everyday Rust developers, REM2.0 is exposed through a
dedicated VSCode extension backed by a persistent “REM daemon.” The daemon runs as a
long-lived process and communicates with the extension over a lightweight JSON-RPC protocol
via stdin/stdout, enabling the lightning fast refactorings without the overhead of repeated
process launches. On startup, the extension performs an environment check to ensure that the
Daemon, CHARON, AENEAS and Coqc are available; if not, it presents targeted installation
instructions directly in the editor. From the user’s perspective, extraction appears as a standard
VSCode code action: selecting a region triggers a panel, options for naming the new function,
and (when equivalence checking is enabled) clear feedback on whether the refactoring preserves
semantics. This architecture provides a seamless and familiar developer experience while hiding
the complexity of the underlying pipeline. Figure 5 below is the list of options presented to the
developer, and they can also be given keyboard shortcuts for ease of use.




                                                 20
          Figure 5: Options presented to the user when they have selected a region to extract.

3.6.1        Preparing Refactorings for Verification

Although the verification pipeline is described in detail in Section 4, with specific implementation
details in Section 4.5, REM2.0 performs a small amount of preparation at extraction time
to ensure that refactorings can be checked efficiently. For each extraction, REM2.0 captures
both the original function body and the newly generated function in isolated “virtual crates”,
preserving the exact syntax and inferred types returned by RA. These crates form the minimal
input required by CHARON and allow the verifier to compare only the code relevant to the
transformation, rather than the surrounding project.


4         Automatic Equivalence Proofs for Refactored Code
In the strictest sense, refactoring is defined as a behaviour-preserving code transformation.
In practice, refactoring is only valuable if it preserves the original program’s behaviour. In
Rust, where ownership and lifetimes enforce strict invariants, the mere fact that refactored
code compiles does not guarantee equivalence. Additionally, because REM2.0 performs com-
plex, compiler-guided repairs as part of its extraction process [2], there is an increased risk of
introducing subtle changes in program behaviour. Subtle shifts in aliasing or lifetime structure
can produce programs that pass the compiler yet diverge semantically from their originals [29].
Additionally, as Section 5.4.3 shows, automated extract method tooling can produce incorrect
extractions that still compile. For high-assurance domains, this risk is unacceptable: automated
tools must not only generate compiling code but also provide evidence that transformations are
correct.

This section introduces a novel equivalence proof pipeline that extends REM2.0 with automatic,
annotation-free proofs of equivalence between original and refactored code. Our approach com-
bines the existing formal methods toolchains - CHARON 11 , which translates Rust into an
ownership-explicit intermediate from, and AENEAS 12 , which then generates Coq code equiva-
lent to the original Rust source through a pure λ-calculus based intermediary. We then use this
Coq code to formally prove that the refactored code is equivalent to the original. The result
is an end-to-end system in which the Extract → Repair cycle is followed by a Verify phase,
discharging proofs in seconds with no additional burden on the developer. By embedding auto-
mated equivalence proofs directly into the refactoring process, we provide developers with the
    11
         More information accessible from their GitHub, https://github.com/AeneasVerif/charon
    12
         More information accessible from their GitHub, https://github.com/AeneasVerif/aeneas



                                                       21
    option to move beyond compilation success to true semantic assurance, whilst also bridging the
    gap between theory and practical developer tools.

    Throughout this section (and previously) we do occasionally refer to the equivalence checker as
    a “verifier”. We acknowledge that the work it performs isn’t verification in the strictest sense
    of the word, but it suits the language much better.

    4.1    What if Extraction Goes Wrong?
    Automated extraction is not infallible: incorrect handling of ownership or mutation can silently
    alter program semantics. To demonstrate the reason why we have built the verifier, and its
    role in REM2.0, we consider a trivial but illustrative example where the extractor mishandles a
    mutable binding13 . The verifier correctly identifies the non-equivalence and reports the failure
    to the developer through the VSCode extension interface, offering an option to automatically
    revert to the previous state. Figure 6 shows the case we are working with, along with a correct
    extraction (passing the mutable reference to x, &mut x ), and an incorrect extraction (passing
    a cloned ‘x’ instead x.clone() ). This error sidesteps Rusts safety guarantees as the com-
    piler cannot prove what x is at compile time, and thus we get a runtime crash as shown by
    Listing5.

1   fn main() {                        1   fn main() {                        1   fn main() {
2       let mut x = 0;                 2       let mut x = 0;                 2       let mut x = 0;
3       x = 3;                         3       mutate_x(&mut x);              3       mutate_x(x.clone());
4       assert!(x == 3);               4       assert!(x == 3);               4       assert!(x == 3);
5   }                                  5   }                                  5   }
6   //                                 6                                      6
7   //                                 7   fn mutate_x(x: &mut i32) {         7   fn mutate_x(mut x: i32) {
8   //                                 8       *x = 3;                        8       x = 3;
9   //                                 9   }                                  9   }


            (a) Original Code                   (b) Correct Extraction                (c) Incorrect Extraction

          Figure 6: Comparison of the original program, a correct extraction, and an incorrect
                        extraction that clones rather than mutably borrows.


1   thread ’main’ (543251) panicked at src/main.rs:6:5:
2   assertion failed: x == 3
3   note: run with ‘RUST_BACKTRACE=1‘ environment variable to display a backtrace


      Listing 5: Terminal output from running the incorrect extraction. The program crashes at
                                    runtime, not at compile time.

    From here, we generate a semantically equivalent file, but in the Coq proof assistant language.
    In Figure 7 below, we list the important parts of these translations. Other aspects (e.g. the
    complex definitions that translate Rust types to Coq types) have been ignored and will be
    covered later in Section 4.5. Also note that rustc has performed some static optimisations on
      13
         Our extraction pipeline does not perform this extraction incorrectly, but previous tools, especially the ones
    evaluated against in Adventure of a Lifetime could make similar mistakes. This example is a demonstration of
    such a failed extraction.



                                                           22
    the code before translation, at this stage there is no way to disable them within CHARON so
    Listing 7a is visually different to the rust implementation.

1   (** [orig::main]:                1   Definition mutate_x (x : i32) :   1   Definition mutate_x (x : i32) :
2       Source: ’src/main.rs’, lines          result i32 :=                         result unit :=
         1:0-5:1 *)                  2     Ok 3%i32.                       2     Ok tt.
3   Definition main : result unit := 3                                     3
4     massert (3%i32 s= 3%i32).      4   Definition main : result unit := 4    Definition main : result unit :=
5   (* *)                            5     x <- mutate_x 0%i32; massert (x5      let i :=
6   (* *)                                     s= 3%i32).                            core_clone_impls_CloneI32_clone
7   (* *)                            6   (* *)                                       0%i32 in
8   (* *)                            7   (* *)                            6      _ <- mutate_x i;
9   (* *)                            8   (* *)                            7      massert (0%i32 s= 3%i32).


           (a) Original Code                  (b) Correct Extraction               (c) Incorrect Extraction

         Figure 7: Comparison of the original program, a correct extraction, and an incorrect
                       extraction that clones rather than mutably borrows.


    Having obtained the AENEAS-generated Coq representations of both the correct and incorrect
    extractions, we now perform an automated equivalence check. This step constitutes a concrete
    implementation of the proof obligations described in Section 4.4. In essence, the verifier con-
    structs and discharges a proof showing that, for all possible inputs to the caller function, the
    original and refactored programs produce identical results. Because the verification operates
    within Coq’s pure, functional semantics—free from hidden side effects or mutable state—the
    resulting proof provides strong assurance of behavioural equivalence.




                                                        23
 1   (** EquivCheck.v Autogenerated by REM-verification    1   (** EquivCheck.v Autogenerated by REM-verification
          **)                                                       **)
 2   Require Import Primitives.                            2   Require Import Primitives.
 3   Import Primitives.                                    3   Import Primitives.
 4   Require Import Orig.                                  4   Require Import Orig.
 5   Require Import Good.                                  5   Require Import Bad.
 6   Local Open Scope Primitives_scope.                    6   Local Open Scope Primitives_scope.
 7                                                         7
 8                                                         8
 9   Lemma main_equiv_check :                              9   Lemma main_equiv_check :
10       Orig.main = Good.main.                           10   Orig.main = Bad.main.
11       Proof.                                           11   Proof.
12       intros.                                          12   intros.
13       unfold Orig.main.                                13   unfold Orig.main.
14       unfold Good.main.                                14   unfold Bad.main.
15       reflexivity.                                     15   reflexivity.
16       Qed.                                             16   Qed.


        (a) Equivalence Check (Correct Extraction)               (b) Equivalence Check (Incorrect Extraction)

 1   COQ_PROJECT: cases/4.1_examples/good_verif/           1   COQ_PROJECT: cases/4.1_examples/bad_verif/
          _CoqProject                                               _CoqProject
 2   EQUIVCHECK: cases/4.1_examples/good_verif/            2   EQUIVCHECK: cases/4.1_examples/bad_verif/EquivCheck
          EquivCheck.v                                              .v
 3   PRIMITIVES: cases/4.1_examples/good_verif/            3   PRIMITIVES: cases/4.1_examples/bad_verif/Primitives
          Primitives.v                                              .v
 4   SUCCESS: true                                         4   SUCCESS: false
 5   OUTPUT_END                                            5   OUTPUT_END


           (c) Verifier Output (Correct Extraction)               (d) Verifier Output (Incorrect Extraction)

     Figure 8: Comparison of equivalence checking results for the correct and incorrect extractions.
       The verifier confirms semantic equivalence in the first case and correctly rejects the cloned
                                       variant as non-equivalent.


     In this example, the incorrectly extracted version introduces a cloned value ( x.clone() ) in
     place of a mutable borrow, thereby altering the program’s semantics while still producing com-
     pilable Rust code. Through the equivalence checks shown in Figure 8, the equivalence checker
     detects this discrepancy by symbolically comparing the Coq representations of both versions
     and rejecting the transformed function as non-equivalent. Within the REM2.0 workflow, this
     failure is brought directly to the developer via the VSCode extension as a clear error message,
     accompanied by an option to automatically revert to the pre-extraction state.
     4.2     Demonstrating Non-Trivial Verification
     The previous section showcased a deliberately trivial case to serve as an introduction to the con-
     cept, and to illustrate how the equivalence checker guards against obvious semantic breakages.
     In contrast, real refactorings can involve nested loops, const generics, ownership subtleties, and
     type-level invariants that interact in ways which are far less visible in the surface syntax. In this
     section we examine a more realistic example, inspired by an incorrect extraction found in the
     Vaultwarden code base, where the refactoring compiles, typechecks, and appears superficially
     reasonable, yet silently changes the program’s behaviour. The aim here is to demonstrate that
     the verifier is not merely checking syntactic structure nor trivially returning success, but is able
     to detect subtle semantic divergences that Rust’s type system alone cannot rule out.

                                                          24
1    pub fn bump<const N: usize>(                            1    fn bump_extracted<const N: usize>(
2        arr: &mut [i32; N],                                 2        mut arr: [i32; N], i: usize, mut mark: bool
3        k: usize,                                           3    ) where [i32; N]: Copy, {
4        mark: &mut bool,                                    4        if arr[i] == 0 {
5    ) where [i32; N]: Copy, {                               5            mark = true;
6        let mut i = 0;                                      6        }
7        let limit = if k < N { k } else { N };              7        arr[i] = arr[i] + 1;
8        while i < limit {                                   8    }
9            if arr[i] == 0 {                                9    pub fn bump<const N: usize>(
10               *mark = true;                              10        arr: &mut [i32; N],
11           }                                              11        k: usize,
12           arr[i] = arr[i] + 1;                           12        mark: &mut bool,
13           i += 1;                                        13    ) where [i32; N]: Copy, {
14       }                                                  14        let mut i = 0;
15   }                                                      15        let limit = if k < N { k } else { N };
16   fn main() {                                            16        while i < limit {
17       let mut a = [0, 0, 5, 9];                          17            bump_extracted::<N>((*arr).clone(), i, *
18       let mut touched_zero = false;                                 mark);
19       bump(&mut a, 3, &mut touched_zero);                18            i += 1;
20       assert_eq!(a, [1, 1, 6, 9]);                       19        }
21       assert!(touched_zero);                             20    }
22   }                                                      21    fn main() {
23   //                                                     22        let mut a = [0, 0, 5, 9];
24   //                                                     23        let mut touched_zero = false;
25   //                                                     24        bump(&mut a, 3, &mut touched_zero);
26   //                                                     25        assert_eq!(a, [1, 1, 6, 9]); // fails: a: [0,
27   //                                                                0, 5, 9]
                                                            26        assert!(touched_zero); // fails
                                                            27    }
                      (a) Original Code

                                                                               (b) Incorrect Extraction

        Figure 9: Original Function and Incorrect Extraction produced by the Engine. Example
                    inspired by the failed Vaultwarden extraction, see Section 5.4.3


     At a glance, the incorrect extraction appears harmless: the loop structure is preserved, the
     in-place update remains nested within an iterator, and Rust’s type system accepts the trans-
     formation due to the array’s Copy bound. However, because the extracted function takes its
     array by value rather than by mutable reference, it mutates a temporary copy and discards it.
     This subtle deviation is difficult to detect manually and impossible for the compiler to reject.
     The equivalence checker, however, detects the mismatch by comparing the Coq translations of
     both versions and identifying that the caller’s array is unchanged in the transformed program.
     As shown in Figure 10, the equivalence check on the incorrect extraction fails14 , and REM2.0
     is capable of passing this failure directly to the developer, preventing the silently incorrect
     refactoring from being applied.
      14
         The assertions in listing 9b also fail at runtime, they are used here to allow us to demonstrate the failure in
     Rust, and imitate a unit test.




                                                             25
 1   Definition bump                                     1    Definition bump
 2     {N : usize} (coremarkerCopyArrayI32NInst :        2      {N : usize} (coremarkerCopyArrayI32NInst :
          core_marker_Copy (array i32 N))                           core_marker_Copy (array i32 N))
 3     (arr : array i32 N) (k : usize) (mark : bool) :   3      (arr : array i32 N) (k : usize) (mark : bool) :
 4     result ((array i32 N) * bool)                     4      result ((array i32 N) * bool)
 5     :=                                                5      :=
 6     if k s< N then bump_loop0 k arr mark 0%usize else 6      if k s< N
           bump_loop1 arr mark 0%usize                   7      then (
 7   .                                                   8         _ <- bump_loop0 coremarkerCopyArrayI32NInst arr
 8                                                                   k mark 0%usize;
 9   (* *)                                                9        Ok (arr, mark))
10   (* *)                                               10     else (
11   (* *)                                               11        _ <- bump_loop1 coremarkerCopyArrayI32NInst arr
12   (* *)                                                           mark 0%usize;
13   (* *)                                               12        Ok (arr, mark))
14   (* *)                                               13   .
15   (* *)                                               14
16   (* *)                                               15   Definition bump_extracted
17   (* *)                                               16     {N : usize} (coremarkerCopyArrayI32NInst :
18   (* *)                                                         core_marker_Copy (array i32 N))
19   (* *)                                               17     (arr : array i32 N) (i : usize) (mark : bool) :
20   (* *)                                               18     result unit
21   (* *)                                               19     :=
22   (* *)                                               20     i1 <- array_index_usize arr i;
23   (* *)                                               21     if i1 s= 0%i32
24   (* *)                                               22     then (_ <- i32_add i1 1%i32; _ <-
25   (* *)                                                         array_index_mut_usize arr i; Ok tt)
26   (* *)                                               23     else (_ <- i32_add i1 1%i32; _ <-
27   (* *)                                                         array_index_mut_usize arr i; Ok tt)
28   (* *)                                               24   .


                     (a) Original Code                                     (b) Incorrect Extraction

 1   COQ_PROJECT: cases/4.3_examples/verif/_CoqProject
 2   EQUIVCHECK: cases/4.3_examples/verif/EquivCheck.v
 3   PRIMITIVES: cases/4.3_examples/verif/Primitives.v
 4   SUCCESS: false
 5   OUTPUT_END


                               (c) Terminal output showing the verification failure

      Figure 10: Coq Translation and output of REM2.0’s equivalence checker. // Note that some
        of Coq translation has been omitted for brevity. See Appendix F for the full translation.

     Together, these results demonstrate that the equivalence checker performs genuinely non-trivial
     reasoning: it succeeds only when two programs are behaviourally identical, and it rejects trans-
     formations that break behavioural equivalence even when the compiler accepts them and the
     syntactic structure appears valid. This establishes that the equivalence stage is a substantive
     correctness guarantee rather than a superficial or always-succeeding check.
     4.3     Handling of Likely Edge Cases
     While the previous section(s) have demonstrated the need for the equivalence checker, going
     into examples in depth, this section aims to show how we handle likely boundary conditions that
     do arise as a result of using the extraction engine. Out goal is to show that: (i) invalid patterns
     are rejected early by rustc (and surfaced into REM2.0 as actionable diagnostics), (ii) well-typed
     but “degenerate” shapes (no params, unit return, locally inferred             ) translate cleanly through

                                                         26
    CHARON/AENEAS and verify as expected, and (iii) known limitations (e.g. ! ) are identified
    and cannot result in spurious “success”. The below table demonstrates each such edge case and
    what we expect to happen:

Case               Minimal Example          Rustc /         Translate   Equivalence Outcome / Notes
                                            Cargo
No input           fn ping() { /* ...       OK              OK          Proof engine capable of unfolding
arguments, Unit    */ }                                                 functions without a forall clause.
return or Both     fn reset(x: &mut                                     Reflexivity guarantees equivalence.
                   i32) { *x = 0; }
Unit return        fn touch(x:&mut          OK              OK          Equivalence checked via identical
(explicit or       i32){ *x += 1; }                                     post-state; return value is unit.
inferred)          fn f()->() { }                                       Side-effect modelling preserved.
  in parameter     fn g(x: )-> i32 {        Error           N/A         Rejected upstream by the compiler.
or return type     x+1 }                    (invalid                    No translation or proof attempted.
                   fn h(x:i32)-> { x*2      signa-
                   }                        tures)
  in local         let x:    = 42; let y    OK              OK          Type is concretised before/at MIR;
binding (within    = x+1;                                               Coq has a concrete integer type.
body)                                                                   Verifier succeeds as usual.
! (never) return   fn abort()->! {          OK              Fails       Excluded from verification set. REM
type               panic!("fail") }                                     2.0 reports an unsupported-feature
                                                                        diagnostic; extraction may proceed
                                                                        but is not verified.
Non-local          break/continue inside    OK              OK          Control flow reified as
control flow in    loop body                                            std::ops::ControlFlow. Verifier
extracted region                                                        checks pattern-match and proves
                                                                        behavioural equivalence.

            Table 1: Edge-case coverage for extraction and verification. ”Translate” refers to
                      CHARON/AENEAS; ”Verifier” to the equivalence checker.


    Taken together, these cases show that the pipeline neither devolves into trivial proofs, nor
    silently accepts unsupported constructs. Invalid signatures involving      are blocked by rustc and
    surfaced to the user; structurally simple but well-typed shapes (no params, unit return, local      )
    translate cleanly and verify; and known limitations (e.g., ! ) are explicitly reported and excluded
    from proof. This provides broad coverage over edge conditions while keeping the verifier’s
    guarantees meaningful and trustworthy. Whilst the design specifications and implementation
    are detailed in Section 4.5 and Appendix H, what we have demonstrated here reflects a core
    philosophy of the equivalence checker: to the best of its capacity, it must never report that two
    pieces of code are equivalent when they are not.
    4.4    Proof Obligations
    In the final stage of the verification pipeline, we discharge a formal equivalence obligation inside
    Coq. Intuitively, we must show that the refactored program behaves identically to the original
    program for all valid inputs. The central idea is functional equivalence: the observable outputs
    of the two programs must match.



                                                       27
4.4.1   Simplified Obligation

We write Jf K for the semantic interpretation (meaning) of the function f as produced by the
AENEAS translation into Coq. Simply put, the obligation can be stated as:
                                  ∀x ∈ Dom(f ). Jf K(x) = Jf ′ K(x)
Where f is the original function and f ′ is its refactored counterpart. This expresses that for
every possible construct of inputs x, the translated functions return identical results. In practice,
this is the form we attempt to discharge automatically, as shown in Figure 8a.

4.4.2   Whole-Program Context

For a more complete characterisation, we must acknowledge that functions are never executed
in isolation, but as part of the enclosing program. Thus the obligation can be strengthened to
whole-program equivalence:
                                  ∀x ∈ Dom(f ). Jf K(x) = Jf ′ K(x)
Where P is the original program and P ′ is the refactored program, differing only in that f is
replaced by f ′ . This captures the fact that equivalence must hold regardless of how the function
is used internally. An equivalent way to phrase this is through contextual equivalence:
                                  ∀x ∈ Dom(f ). Jf K(x) = Jf ′ K(x)
where C[·] denotes an arbitrary program context. This emphasises that the replacement of f by
f ′ preserves behaviour under any calling environment. This is only true within the side-effect
free functional environment that we translate into.

4.4.3   Relation to Prior Work

Earlier work on AENEAS stated equivalence in a deliberately general form, including precon-
ditions Φ(x), effect traces τ , and projections obs(τ ) onto observable behaviours. These factors
were necessary to account for impure features, partial programs, and richer effect semantics.
In contrast, our pipeline deliberately restricts attention to a simpler setting. REM2.0 produces
well-typed, borrow-checked Rust fragments, and AENEAS is applied to safe Rust code without
interior mutability or concurrency. Hence:

• Preconditions can be dropped, as REM ensures typing and borrow safety.
• Effect traces can be omitted, as our fragments are side-effect free modulo return values.
• Observable projections reduce to plain equality of results.
• AENEAS guarantees that its transformations map directly back to the Rust source. If some-
  thing holds in AENEAS’s translation, it holds in Rust[15, 16]. Hence no extra proof work is
  required (on our end) to uphold this

This simplification yields an obligation that is easier to state and automate, while still capturing
the core requirement that refactoring preserves behaviour.
4.4.4   Practical Implications

The simplified obligation highlights a guiding design principle: the pipeline is intended to
complement the extraction algorithm rather than over-approximate it. It is therefore preferable

                                                 28
to fail early when unsupported constructs and language features are encountered, rather than
risk certifying programs incorrectly. AENEAS reports unsupported features (e.g. closures
or nested borrows) as translation failures, while the Coq implementation clearly distinguishes
between an unprovable equivalence and an unsupported fragment. This separation ensures that
developers never receive a false positive: code is either successfully verified, or it fails explicitly
with a clear diagnostic. This leads naturally to the question of coverage: which Rust features
are currently supported by AENEAS, and which remain open problems? We address this in
the final section of this section, Section 4.6.
4.5     Implementation of the Equivalence Pipeline
The design of REM2.0’s automated equivalence checking is guided by two principles: (1) it
must require no additional annotations or input from the developer, and (2) it must complete
quickly to fit into interactive IDE workflows. To achieve this, the pipeline translates both
the original program P and the refactored program P ′ through a sequence of more structured
semantic representations, culminating in a machine-checked proof of observational equivalence.
For brevity, this section only gives a very high-level overview of the architecture; Appendix H
contains the full technical details and examples.

At a high level, the pipeline consists of five stages: Extraction, REM repairs, CHARON
translation, AENEAS functionalisation, and Coq verification. Each stage builds on the
previous one, progressively exposing the semantics of the refactored code until we obtain a pure,
functional model of both versions in Coq.
4.5.1    Extraction and Repair

The pipeline starts from REM2.0’s extraction engine. Given a user selection, the extractor lifts
the region into a new function and replaces it with a callsite adaptor. The extractor is unable
to finalise lifetimes and thus it delegates these to REM’s post-extraction repair phase. REM
then performs lifetime repair to bring the extracted program P ′ into agreement with the Rust
borrow checker. It treats the compiler as an “oracle”, iteratively repairing lifetimes until the
program compiles, and applying lifetime elision where possible to recover idiomatic types and
make the output as “readable” as possible. The result is a repaired, compiling version of the
program.
4.5.2    Translation via CHARON and AENEAS

The next stages translate the Rust programs into a verification-oriented representation. CHARON
takes the compiled MIR for both P and P ′ and produces LLBC (Low-Level Borrow Calculus), a
machine only readable form in which all behinds the scenes logic of rust are made 100% explicit.
To keep this process stable with respect to edits in the user’s workspace, REM2.0 constructs
temporary “virtual” crates, which are memory isolated replicas of the original crate but with
either the original or refactored function present. They are required to allow us to begin running
CHARON.

AENEAS then transforms LLBC into a purely functional model, removing explicit stack and
heap operations while preserving the semantics of the Rust program. In this form, programs
are expressed as total functions over values rather than mutating references, which is far better


                                                  29
suited to proof assistants. In our pipeline, AENEAS targets Coq, but in principle it can also
emit encodings for other systems such as Lean, HOL4, or F*.
4.5.3    Equivalence Checking in Coq
The final stage assembles a Coq project containing the functional encodings of P and P ′ (pro-
duced by AENEAS) together with a generated module EquivCheck.v. This module instantiates
the two versions, generates the equivalence theorem described in Section 4.4, and invokes the
necessary automation to show that they produce the same observable results for all inputs.
Once the Coq project is compiled, the equivalence check is fully automatic: if the proof suc-
ceeds, we obtain a machine-checked guarantee that the refactoring preserved behaviour. The
underlying Coq infrastructure, alternative backends, and example proof scripts and much more
are discussed in extensive detail in Appendix H.
4.6     Limitations of Current Verification
At present, the verification guarantees supported by our pipeline are constrained by the subset
of Rust that AENEAS can translate. AENEAS is designed to operate on safe Rust; programs
that make use of unsafe constructs fall outside its scope. While this excludes some low-level
systems code, the restriction is deliberate: safe Rust already captures the majority of idiomatic
Rust usage, and the long-term plan is to integrate AENEAS with complementary tools that
target unsafe code. The current support landscape is summarised in Table 2.

 Feature                                         Status
 Safe Rust                                       Fully supported (excluding where mentioned in this table)
 Unsafe Rust                                     Not supported (out of scope of AENEAS)
 Loops                                           Supported (no nested loops)
 Function pointers / Closures                    Not supported (work in progress)
 Traits                                          Supported
 Type parametricity                              Limited: type parameters with borrows not supported
 Nested borrows in function signatures           Not supported (work in progress)
 Interior mutability (Cell, RefCell, etc.)       Not supported (planned via ghost states)
 Concurrency                                     Out of scope (long-term research goal)

                      Table 2: Current AENEAS support for Rust features

Within safe Rust, several technical limitations remain. Loops are supported only in restricted
forms (no nested loops), though this is under active development. Function pointers and closures
are not yet available, although trait-based abstractions are supported and ongoing work aims
to extend this to first-class functions. Type parametricity is limited: currently, it is not possible
to instantiate a generic type parameter with a type that itself contains a borrow. Similarly,
function signatures cannot yet contain nested borrows, though this too is being addressed.
Interior mutability is another open challenge; the current plan is to capture its effects using
ghost states. Finally, concurrent execution is out of scope: AENEAS models sequential Rust
programs only, with parallelism considered a long-term research goal.

It is important to emphasise that the verification pipeline is designed to complement the ex-
traction algorithm. As such, it is preferable for verification to fail early when encountering
unsupported features rather than risk certifying code incorrectly. A failed verification due to
unsupported language constructs is reported differently to the developer than a failed proof



                                                 30
obligation. This distinction ensures that false positives—cases where unverifiable code would
otherwise appear verified—are avoided..

In summary, the present pipeline is best understood as an equivalence framework for sequential,
safe Rust programs without features such as nested borrows, closures, or concurrency. These
restrictions reflect the state of AENEAS rather than fundamental barriers, and ongoing work is
progressively extending the supported subset. As AENEAS development progresses, we expect
the equivalence checker to be able to handle complete crates. A complete discussion of the
limitations, and the current expected use case of the full REM2.0 pipeline have been deferred
to Section 6.


5     Evaluation and Experimental Results
This section evaluates the new REM2.0 in two separate directions: its ability to perform extract-
function refactorings on realistic Rust code, and its ability to verify that those refactorings
preserve behaviour. We first describe the benchmark corpora and experimental setup, then
define the metrics and criteria we use to judge success. We then present results for the ex-
traction pipeline and, subsequently, for the optional verification pipeline built on CHARON and
AENEAS, highlighting both the gains over the original REM prototype and the remaining limi-
tations.
5.1     Evaluation Goals and Research Questions
The overall goal of the evaluation is to determine how REM2.0 behaves on realistic Rust code:
both as a fast, everyday extract-function refactoring tool, and as an optional source of formal
guarantees when paired with the verification pipeline. In particular, we are interested in charac-
terising its correctness, feature coverage, and performance, and in understanding the trade-offs
introduced by the verifier. We frame this in terms of the following research questions:

• RQ1 (Extraction correctness and coverage). How accurately does the new extraction
    toolchain preserve typing and behaviour on the original REM benchmark suite, and are there
    any they both fail on?

• RQ2 (New feature support). How does the new extraction engine extend coverage to mod-
    ern Rust features—such as async / await , const fn , generics, higher-ranked trait bounds,
    dynamic trait objects, and non-local control flow—and what patterns of success and failure
    emerge across these features?

• RQ3 (Performance). What extraction latencies does the new architecture achieve on real-
    istic projects, and how do these compare quantitatively with the original REM prototype?

• RQ4 (Verification). Within the subset of Rust currently supported by CHARON and AENEAS,
    how effective is the verification pipeline at establishing equivalence, and what are its perfor-
    mance characteristics?

Subsections 5.2–5.4 primarily address RQ1–RQ3 through extraction-focused experiments, while
Subsection 5.5 answers RQ4 by evaluating the optional verification pipeline on a curated set of

                                                 31
trivial and real-world cases.
5.2     Benchmark Corpora and Experimental Setup
This subsection describes the benchmark corpora and experimental setup used to evaluate
the extraction and verification components of REM2.0. We first give a high-level overview of
the experiments, then introduce the three corpora used in the remainder of the section: the
original REM benchmark suite, a new set of real-world feature-focused cases, and a verification
benchmark tailored to the current capabilities of CHARON and AENEAS.

5.2.1    Overview of Experiments

To cover both backwards compatibility and new functionality, we designed three complementary
experiments:

1. Original REM cases (baseline extraction). We re-run the new extraction pipeline on
   the full suite of benchmark cases used in the evaluation of the original REM prototype. This
   experiment is primarily used to answer RQ1 and RQ3 by comparing correctness and latency
   against the baseline design.

2. New real-world feature cases (extended extraction). We construct a new corpus of
   forty extraction sites drawn from large, actively maintained Rust repositories. Each case is
   chosen because it exercises at least one modern Rust feature that the original REM could
   not reliably support. This experiment targets RQ2 and RQ3.

3. Verification benchmark (equivalence checking). We assemble a set of twenty exam-
   ples for the verification pipeline: ten small “trivial” programs that isolate core correctness
   properties, and ten simple but real-world functions drawn from open-source code. These are
   selected to fall within the fragment of Rust currently supported by CHARON and AENEAS, and
   are used to answer RQ4.

5.2.2    Original REM Benchmark suite

To provide a baseline for comparison, we re-used the full suite of extraction cases from the orig-
inal REM evaluation.15 Each case consists of a Rust project containing an annotated source file,
where the intended extraction region is marked by either line comments ( // START SELECTION //
and // END SELECTION // ) or block comments ( /* START SELECTION */ and /* END SELECTION */ ).

Each benchmark case is defined by the selection markers in the original REM artefact, which
we reuse to ensure that both the original prototype and the new extraction pipeline are run
on exactly the same inputs. One case in the original suite (case #16) contained no selection
markers and is therefore excluded from our quantitative comparison; outcomes and timings for
the remaining cases are reported in Table 4.

5.2.3    New Real-World Cases

To evaluate the new extraction engine on patterns that arise in modern Rust code “in the wild”,
we constructed a second corpus of forty extraction sites drawn from large, popular open-source
  15
    The test repositories were copied directly from the artefact published by the VerseLab group at https:
//github.com/verse-lab/rem.


                                                   32
projects. The goal of this corpus is to stress language features that the original REM prototype
could not support, while ensuring that as many examples as possible reflect extractions that
developers actually performed (or could plausibly have performed) in practice.

We began by selecting a sample of the most highly starred Rust repositories, using the GitHub
rankings maintained by Evan Li [30] as our baseline. A summary of the selected repositories
(including stars, forks, and open issues at the time of sampling) is provided in Appendix B,
Table 8.

For each repository in this group, we performed a scan of its Git history to locate commits
likely related to method or function extraction. The automated scan searched commit mes-
sages for characteristic phrases such as extract, extract method, factor out, and refactor:
extract, and then used a combination of regular expressions and git grep queries to flag any
candidate files. We limited the depth of this search to at most 100 commits across the three
most active branches per repository. This heuristic process inevitably produced false positives
(for example, commits mentioning “extract” in an unrelated context), but provided an efficient
starting point. We then manually inspected each flagged commit/file for suitable extraction
sites and annotated the regions with the selection markers described earlier.

The full list of identified commits, along with per-repository details, appears in Appendix B.
The complete set of extraction outcomes and timing results for these cases is later on in this
report, in Table 5, Subsection 5.4.2.

5.2.4   Verification Benchmarks

The third corpus targets the verification pipeline, which builds on CHARON and AENEAS to prove
that an extracted function is behaviourally equivalent to its original version. Since these tools
currently support only a subset of Rust, we deliberately construct a small benchmark set that
fits within their supported fragment while still exercising non-trivial reasoning. See Subsec-
tion 4.6 for the complete set of limitations. From there, the verification corpus comprises
twenty examples split into two groups:

• Trivial/targeted cases (10 examples). Small, self-contained Rust functions that isolate
  core properties such as pure computations on integers, simple mutation through references,
  or basic control-flow patterns without heap allocation or complex borrowing. These examples
  are designed to expose bugs in the translation or proof generation pipeline, rather than in
  the extraction engine itself.

• Simple real-world cases (10 examples). We wrote a new crate that emulates real-
  istic business-logic style Rust code. The functions operate over multiple layered structs,
  rely on trait implementations, and approximate production patterns while remaining within
  the subset of Rust currently supported by AENEAS. This did require some additional scaf-
  folding—such as manual implementations of PartialEq . Crucially, this crate has external
  dependencies, including smallvec and anyhow.

For each verification benchmark, we run the full pipeline on the original and extracted functions:


                                               33
 Experiment       Objective                           Evaluation Criteria
 Original         Establish correctness and           • Extraction success rate on the original REM
 Cases            performance of the new ex-            benchmark suite.
                  tractor relative to the original    • Match or improvement in compilation outcomes
                  REM prototype (RQ1, RQ3).             compared to the prototype.
                                                      • Reduction in extraction latency.
 New Feature      Characterise support for            • Extraction success rate per feature category
 Cases            modern Rust features previ-           (GEN, ASYNC, CONST, NLCF, HRTB, DTO).
                  ously unsupported or poorly         • Compilation outcome of extracted code, with
                  supported by REM (RQ2,                failures classified by root cause.
                  RQ3).                               • Extraction latency on large real-world projects
                                                        and its variation across features.
 Verification     Assess the effectiveness and        • Fraction of cases for which verification is at-
 Pipeline         cost of the equivalence-              tempted and successfully completed.
                  checking pipeline on sup-           • Consistency of proofs with intended semantics
                  ported    Rust     fragments          (no spurious successes; failures explained by tool
                  (RQ4).                                limits or program in-equivalence).
                                                      • End-to-end verification time, broken down into
                                                        LLBC translation, Coq conversion, and proof
                                                        parsing/construction/checking.

            Table 3: Summary of experimental objectives and evaluation criteria.


translating to Low-Level Borrow Calculus (LLBC) via CHARON, generating Coq proof obligations
via AENEAS, and then checking the resulting proof. We record whether verification was attempted
and whether it succeeded, along with timings for each stage. These results are reported in
Table 7 in Subsection 5.5.2.
5.3   Metrics and Evaluation Criteria
Across all three experiments we measure: (i) correctness and coverage (whether extraction or
verification succeeds, and how often failures occur), (ii) compilation behaviour (whether the
refactored code compiles and how this compares to the original), and (iii) performance (end-
to-end latency, and for verification, the cost of individual stages). RQ1 and RQ2 are primarily
concerned with correctness, coverage, and compilation; RQ3 focuses on extraction latency; and
RQ4 considers both the success rate and performance of the verification pipeline. Table 3
summarises how these requirements are determined for each experiment.
5.4   Extraction Evaluation
This subsection addresses RQ1—RQ3 for the extraction pipeline. We ask three concrete ques-
tions: (i) whether REM2.0 is at least as correct and robust as the original REM prototype
on the original benchmark suite (RQ1), (ii) how far its coverage extends to modern Rust fea-
tures such as async , const fn , generics, HRTBs, dynamic trait objects, and non-local control
flow (RQ2), and (iii) what latency profile it achieves in practice, and when the separate REM-
Repairer stage is required to obtain a compiling result (RQ3). We first compare directly against
the original REM artefact, then turn to the new real-world feature corpus, and finally summarise
the quantitative behaviour and remaining limitations.




                                                     34
5.4.1   Baseline Comparison with the Original REM

                  Project         Outcome                 Time (ms)         Repairer
           #
                  (LOC)        REM REM2.0          REM      Raw     User    Needed
           1                    ✓       ✓           370     3.511 184.32       ✗
           2                    ✓       ✓          1020     3.753 217.91       ✗
           3                    ✓       ✓          1470     2.166 231.08       ✓
                  petgraph
           4                    ✓       ✓          1700     3.337 196.77       ✗
                  (20,157)
           5                    ✓       ✓           850     2.018 128.54       ✗
           6                    ✓       ✓           980     2.148 142.66       ✗
           7                    ✗       ✓           550     2.030 255.19       ✓
           8                    ✓       ✓           930     2.851 199.45       ✗
           9                    ✓       ✓          1240     3.240 173.82       ✓
           10                   ✓       ✓           640     2.823 208.37       ✗
           11                   ✓       ✓           810     2.991 244.68       ✗
           12                   ✓       ✓           810     3.282 188.05       ✗
           13                   ✓       ✓           860     2.995 163.49       ✗
           14                   ✓       ✓           690     5.345 226.91       ✗
           15                   ✓       ✓           680     5.468 203.74       ✗
           16     gitoxide      ✓    No Data        540     N/A     N/A        ✗
           17     (20,211)      ✓       ✓          1200     3.283 179.40       ✓
           18                   ✓       ✓           920     5.241 210.62       ✓
           19                   ✓       ✓          2320     3.283 226.46       ✓
           20                   ✗       ✓          1150     5.430 192.92       ✓
           21                   ✓       ✓           690     3.396 123.84       ✗
           22                   ✓       ✓           640     2.984 264.15       ✗
           23                   ✓       ✓           700     3.153 132.97       ✗
           24                   ✓       ✓           640     3.230 147.53       ✗
           25                   ✓       ✓           720     3.457 221.84       ✗
           26                   ✓       ✓          1030     3.802 185.09       ✗
           27                   ✓       ✓          1010     8.557 237.26       ✗
                   kickoff
           28                   ✓       ✓           910     7.365 168.44       ✗
                   (1,502)
           29                   ✓       ✓           980     4.864 206.59       ✗
           30                   ✓       ✓           790     4.191 257.31       ✗
           31                   ✓       ✓          1040     7.288 121.06       ✗
           32                   ✗       ✓           760     5.674 195.22       ✓
           33                   ✓       ✓          1010     4.439 172.80       ✗
           34                   ✓       ✓           980     3.602 234.13       ✗
                  sniffnet
           35                   ✓       ✓          1060     3.265 141.95       ✗
                  (7,304)
           36                   ✓       ✓          1000     3.507 260.42       ✗
           37                   ✓       ✓          1060     4.147 209.61       ✗
           38                   ✓       ✓          1080     4.284 187.32       ✗
           39                   ✓       ✓          1060     4.273 149.40       ✗
           40   beerus (302)    ✓       ✓          1070     5.158 224.75       ✗

Table 4: Comparison of REM2.0 to the original REM toolchain against the same cases. Raw
times are strictly for the extraction, user times indicate overall system latency as reported by
                                             VSCode.

Table 4 compares the behaviour of the original REM prototype with REM2.0 on the full bench-
mark suite described in Subsubsection 5.2.2. Excluding case #16, which is missing its selection
markers and therefore cannot be evaluated, the new extractor succeeds on all 39 remaining
cases. By contrast, the original REM prototype fails on three of these (cases #7, #20, and
#32), whereas REM2.0 extracts all three. Crucially, there are no regressions—we did not
observe any case where REM succeeded but REM2.0 failed.

                                              35
The timing columns succinctly demonstrate the performance impact of the new architecture.
The original REM pipeline required between a few hundred and a few thousand milliseconds
per extraction (averaging roughly 1000 ms). In contrast, the “Raw” REM2.0 times—measured
inside the daemon, from the extraction request to the application of edits—lie consistently in the
low single-digit milliseconds (approximately 2 ms to 9 ms across all cases). The “User” column
adds the Repairer (where it was called) and VSCode overheads, but still yields user-perceived
latencies in the 120 ms–260 ms range, which, given that the human response time to visual
stimuli is somewhere between 200 ms to 250 ms [31], is more than acceptable. A more detailed
latency distribution is provided in the histogram in Appendix E.

The final column reports how often REM-Repairer is needed to restore a compiling program.
Out of the forty original REM cases it is invoked in seven, in exactly the same examples as
in the original REM evaluation (those with tighter lifetime constraints). This indicates that,
although the new extractor often produces compiling code on its own, the repairer remains a
crucial component of the toolchain rather than a purely optional add-on.

5.4.2   New Language Feature Coverage

We now look at the new corpus introduced in Subsubsection 5.2.3, which is designed to test
against advanced Rust features that the original REM prototype could not handle. Each extrac-
tion is classified into one or more feature categories: generics (GEN), async/await (ASYNC),
const evaluation (CONST), non-local control flow (NLCF), higher-ranked trait bounds (HRTB),
and dynamic trait objects (DTO). These categories directly correspond to cases that generally
tend to stretch type inference, lifetime reasoning, or control-flow reconstruction in real-world
Rust code. Any mark in any feature column of Table 5 indicates that said example contains that
construct within the selected region. Representative listings for each category, along with a brief
explanation of what we expect the extractor to preserve, are provided in Appendix G.

Across the forty new extraction cases, REM2.0 is able to successfully extract (and result in a
compiling program for) thirty-three, yielding an overall success rate of roughly 83%. Looking
the established categories, we see that most of the modern constructs are handled robustly:
all but one ASYNC case succeed (7/8), CONST extractions succeed in almost all examples
(10/11), and NLCF is correctly reified into std::ops::ControlFlow in the majority of cases
(11/13). Higher-ranked trait bounds are also handled reasonably well (6/8), with failures mostly
due to the more complex combinations of generics and control flow. Generic functions them-
selves succeed in most examples (11/14), with the remaining failures arising from incomplete
reconstruction of generic bounds.

The main weakness in the current extractor is dynamic dispatch. Only one out of four DTO
cases succeeds; in the remaining three, the inferred signature collapses to an underspecified
form (e.g., using   or overly weak trait bounds), which then prevents the code from compiling.
One particularly illustrative case is failure #4, where an argument of type AsRef<[u8]> is
incorrectly generalised to ?Sized , losing the relationship between the trait and the concrete slice
type. We cover these failure modes in more detail in the following subsubsection: 5.4.3.



                                                36
               Project                      Code Features                                  Time
        #                                                                        Res
               (LOC)       GEN    ASYNC     CONST NLCF          HRTB     DYN                (ms)
         1                                    ✓                                  ✓         5.882
         2                                             ✓                   ✓     ✗(1)       N/A
                deno
         3                                             ✓                         ✓         4.346
              (359996)
         4                  ✓                          ✓                         ✓         9.685
         5                           ✓                                           ✓         2.910
         6    fuel-core                                  ✓                       ✓         6.736
         7     (78921)               ✓                                           ✓         2.999
         8                  ✓                                                    ✓         4.363
         9                  ✓                                     ✓              ✓         12.071
             meilisearch
        10                  ✓                                     ✓              ✗(2)       N/A
              (186553)
        11                                      ✓                                ✓         3.071
        12                                      ✓                                ✓         3.852
        13    ripgrep       ✓                            ✓                       ✓         3.117
        14    (40453)                                    ✓                       ✓         2.089
        15    starship                                   ✓                       ✓         1.955
        16    (37225)       ✓                                                    ✓         1.866
        17                                      ✓                                ✓         4.802
                sway
        18                                      ✓                                ✓         3.073
              (108725)
        19                  ✓                                     ✓              ✓         2.365
        20                  ✓                                     ✓              ✓         1.183
        21      tauri       ✓                            ✓                       ✓         8.565
        22     (83582)                                   ✓                       ✓         3.054
        23                                               ✓                       ✓         5.346
        24                           ✓                            ✓              ✓         3.175
        25      union                           ✓                                ✓         2.864
        26    (514914)               ✓                   ✓        ✓              ✗(3)       N/A
        27                                                                 ✓     ✗(4)       N/A
        28                                      ✓                                ✓         16.703
        29       uv         ✓                            ✓        ✓              ✓         6.451
        30    (321584)                          ✓                                ✓         2.873
        31                  ✓                                                    ✗(5)       N/A
        32                                      ✓        ✓                       ✓         5.134
             vaultwarden
        33                           ✓                                           ✓         3.057
               (29937)
        34                  ✓                   ✓                                ✗(6)        NA
        35                                                                 ✓     ✗(7)       N/A
        36                           ✓                                     ✓     ✓         7.383
        37       zed                            ✓                                ✓         2.062
        38    (888269)      ✓        ✓                            ✓              ✓         3.667
        39                  ✓                                                    ✓         1.959
        40                           ✓                                           ✓         1.853

Table 5: Results of extracting previously unavailable / incompatible language features. More
                       detail on reasons for failure available in Table 6

              #   Reason
              1   Unable to infer (part of) function signature
              2   Unable to infer (entire) return type
              3   Unable to identify correct extraction bounds (no extraction attempted)
              4   AsRef<[u8]> in caller incorrectly mapped to ?Sized in callsite
              5   Return signature of instead of Result<S::Ok, S::Error>
              6   Failed to copy any generic bounds to new sig
              7   Unable to infer (part of) function signature

        Table 6: Reasons why the extraction was a failure for failure cases from Table 5


5.4.3    Failure Cases and Limitations
The seven failures in Table 5 fall into a small number of recurring patterns, summarised in
Table 6. Broadly speaking, they stem from limitations in how the extraction engine generates


                                                 37
function signatures from local information, rather than from the moving of the selected code
into a new function body.

A first class of failures stems from incomplete type inference for return types or parameter
lists (failure examples #1, #2, and #7). In these cases, RA is able to type-check the original
code, but the information available at the extraction boundary is not sufficient to synthesise a
concrete function signature. The resulting placeholder types (e.g.      for a return type) are not
accepted by the compiler, and the extraction is recorded as a failure. However, in all of these
instances, the compiler was able to suggest a suitable return signature, so a potential future
improvement to REM-Repairer is to extend it to handle these cases.

The second class of failures involves generic bounds and trait information (examples #4, #5,
and #6). Here the extractor identifies the correct high-level shape of the signature, but either
drops necessary bounds (e.g. missing where -clauses or trait constraints on type parameters)
or over-generalises a concrete trait application. The AsRef<[u8]> to ?Sized mis-translation
in failure #4 is a representative example: the new signature no longer captures the intended
relationship between the argument and the slice type, which propagated to many downstream
errors. In this instance, the Rust compiler was unable to suggest a suitable fix.

These patterns were common for the DTO cases, where the type information needed to re-
construct a precise dyn Trait (or similar dyn signature) often lives outside the current file
or depends on non-trivial where-clauses. Because REM2.0 currently uses a (mostly) single-file
view of the program, a fully elaborated crate graph and other expensive dependencies for raw
speed, it does not always have enough global information to resolve these traits in the way
rustc would. Closing this gap will likely require importing more context from the surrounding
crate—for example, by following trait definitions and associated types across modules—so that
the extractor can reconstruct signatures with the same fidelity as the compiler.
5.5     Verification Evaluation
The extraction experiments in Subsection 5.4 have shown that REM2.0 can perform refactor-
ings quickly and with a broad coverage of language features. This subsection will evaluate the
verification stage that sits on top of that pipeline. Our goal is to understand, for code within the
current CHARON/AENEAS fragment, how often the verifier can establish equivalence between the
original and extracted functions, what performance cost this incurs, and what kinds of failures
or limitations arise in practice. We first outline the verification goals and benchmark setup,
then present quantitative results and performance measurements, before briefly examining rep-
resentative case studies and failure modes.

5.5.1    Verification Goals and Setup

The verification experiment addresses RQ4: for code within the supported subset, can we
feasibly verify equivalence between original and extracted functions? In REM2.0, the verifier is
an optional high-assurance mode: developers are able to refactor using the fast extract + repair
pipeline and then can selectively invoke verification for critical functions in crates that AENEAS
can support. Our evaluation will therefore ask (i) how often the pipeline can produce a successful
equivalence proof for realistic examples, and (ii) what latency overhead this introduces


                                                38
To stay within the current capabilities of AENEAS, we have assembled a benchmark suite of
twenty cases (See Subsubsection 5.2.4). The first ten are deliberately simple, and drawn from
internal RA tests for extract method (EX in Table 7. The remaining ten are “simple real-world”
functions drawn from the same or related repositories as our extraction benchmarks, manually
filtered to avoid features that the verification tools cannot yet handle (RW in Table 7. For each
benchmark, REM2.0 runs extraction and then feeds both versions into the verification toolchain.
CHARON first translates the relevant crate to LLBC, AENEAS then generates Coq definitions, and
finally REM2.0 invokes a proof generator that produces and checks an equivalence lemma in
Coq. We record whether verification was attempted and succeeded, and we break total latency
into LLBC conversion, Coq translation, and proof construction/checking times, as reported
in Table 7. All experiments share the same machine, toolchain versions, and a fixed per-
case timeout of 10 seconds. We count timeouts and AENEAS conversion as attempted but
unsuccessful proofs, and failures to convert to LLBC as neither.

5.5.2   Verification Results and Performance

Table 7 summarises the verification outcomes and timings for our twenty benchmarks. All ten
basic cases (EX) successfully produce equivalence proofs within roughly 1.7–2.2 seconds end-
to-end. The majority of this time is spent in proof checking (under the hood coqc is called on 3
separate files regardless), with LLBC conversion accounting for only a few hundred milliseconds
per run. If charon cargo has been run before, we see that with most of the intermediate results
cached in the target, the LLBC generation takes approximately 66% as long.

For the ten real-world benchmarks (RW), the picture is similar but scaled up. Successful cases
complete in approximately 3.8–4.4 seconds, but with a far more equal split of the total time.
We can also see that caching is far more important: a fresh LLBC translation takes on the order
of 9–15 seconds, whereas reusing cached LLBC reduces this to roughly 1.6–1.9 seconds. A big
portion of this is dependencies that only need to be compiled once (either by charon cargo or
cargo. This means that once a crate has been translated once (or even just compiled once),
subsequent verification runs on the same crate fall comfortably within a few seconds. Overall,
the results indicate that for code within the supported fragment, REM2.0 can routinely obtain
machine-checked equivalence proofs, but at a cost that is one to two orders of magnitude higher
than extraction alone.

For robustness, we also reran the verification pipeline on deliberately incorrect refactorings. For
each benchmark, we manually modified either the extracted function or its call site to introduce
a small behavioural change while keeping the Rust code type-correct. In all cases where the
original verification attempt succeeded (i.e. excluding case #20, which already fails to verify),
the modified version caused the equivalence proof to be rejected: Coq was unable to prove the
generated lemma, and the verifier reported failure. This backs up our claim that within its
supported fragment, the pipeline is highly sensitive to real semantic differences.

5.5.3   Case Studies

To further explain what the equivalence checker results mean, we briefly examine two represen-
tative cases: one synthetic example and one real-world function.

                                                39
                     Size (LOC)                            Time (ms)
        #    Type
                                     LLBC      LLBC        Coq     Proof Creation
                     CLR     CLE                                                     Total
                                   FRESH      CACHE      Convert & Verification
        1    EX        4       4    293.04      198.4    308.25       1361.46       1868.11
        2    EX        5       3    318.51     211.99    324.04       1638.93       2174.96
        3    EX        5       3      275      175.96     295.95      1493.59        1965.5
        4    EX        7       3    333.63     236.36    331.67       1314.47        1882.5
        5    EX        5       3    289.29     176.14    326.38       1274.78        1777.3
        6    EX        7       4    289.88     194.97    316.42       1268.78       1780.17
        7    EX        3       4    272.51     170.92    294.54       1267.48       1732.94
        8    EX        7       7    308.61     211.39    321.55       1216.28       1749.22
        9    EX        8       6    269.91     192.37    325.98       1298.64       1816.99
        10   EX        4       3    349.53     242.97    327.96       1363.15       1934.08
        11   RW        4      10   15154.38   1666.14    1260.24      1383.22       4309.60
        12   RW       11       4    9406.05   1671.70    1194.65      1340.72       4207.08
        13   RW       14       5    9288.67   1763.12    1088.14      1168.97       4020.23
        14   RW        5      44    9202.97   1746.28    1228.37      1313.29       4287.94
        15   RW       24      12    9506.05   1618.23    1042.66      1202.97       3863.86
        16   RW        6       7    9535.96   1748.76    1050.50      1185.17       3984.43
        17   RW       13      22    9836.45   1650.95    1194.40      1514.83       4360.18
        18   RW       29       7   10579.37   1710.06    1086.26      1200.34       3996.67
        19   RW       26      11    9318.42   1680.40    1316.54      1328.94       4325.88
        20   RW       17       5    9337.03   1880.03    1166.90        0.00          N/A

                            Table 7: Equivalence Results and Timings
                           Total time is shortest of FRESH and CACHE


The EX benchmarks are deliberately small but structurally non-trivial: several include loops,
conditionals, and updates to a mutable accumulator, mirroring the kind of code that developers
routinely extract into helper functions. For these cases, REM2.0 successfully generates Coq
developments in which the original and extracted functions are related by an automatically
produced equivalence lemma. An example of such a lemma and its proof can be found in the
listing 32 in Appendix I).

The RW benchmarks show that the same approach applies to short functions taken from real
projects, not just hand-crafted examples. After extraction, these functions sometimes gain
additional parameters (from moved-out locals) but otherwise preserve their original structure,
and Coq is still able to check the generated equivalence proofs within a few hundred to a
thousand milliseconds once translation is complete. The form of the proof is identical, but as
listing 33 (Appendix I) shows, the underlying datatypes in Coq are vastly more complex.

Together, these examples show that the equivalence checking pipeline is able to produce proofs
for non-trivial refactorings, with the same underlying proof structure being able to comfortably
scale from very simplistic (or even unitless) function definitions to substantially richer datatypes
and modules.

5.5.4   Failure Modes of the Verifier

Despite the generally positive results, a few benchmarks highlight current limitations of the
verification pipeline and of CHARON/AENEAS.

The most obvious failure is case #20 in Table 7, a “real-world” example that computes the total
backoff delay. The original (Rust)function maintains a counter attempts , a mutable delay ,


                                                40
and a running total inside a while attempts < cfg.max attempts loop. However, after
the translation, AENEAS produced a recursive Coq Fixpoint where termination is expressed in
terms of an attempts parameter. coqc then erorred with “Cannot guess decreasing argument of
fix”. Intuitively, we know that the Rust code terminates because the loop counter is incremented
and compared against a fixed bound, but the way that AENEAS generated a recursive definition
of this function resulted in this decrease not being syntactically obvious to Coq’s termination
checker. As a result, the entire Coq development for this benchmark fails to compile.

More broadly, several potential benchmarks had to be excluded earlier in the pipeline because
they rely on language features that AENEAS does not yet support. These include certain core
intrinsics, derived Eq / PartialEq implementations, and macro expansions such as matches! .
When such constructs appear, the translation step fails before Coq code is generated, and
no proof attempt is possible. In our current experiment design, we designed the real-world
benchmarks to avoid these constructs, but this filtering necessarily hides some of the friction
that developers would encounter in unrestricted code.

In the short term, the most realistic mitigation is to give developers better guidance about when
they can expect verification to succeed. As a follow-on to this work, we plan to extend REM2.0
with a lightweight “AENEAS-able” checker that can quickly test whether a given function lies
inside the current verified fragment and report obvious blockers (unsupported intrinsics, traits,
or control-flow patterns). This checker is not available at the time of writing, but is planned
for shortly after the completion of this project.
5.6     Discussion and Threats to Validity
5.6.1     Discussion

The extraction experiments show that embedding REM2.0 into RA’s infrastructure meets the
main design goals from Section 3. On the original REM benchmarks, it is strictly better
than the prototype—it covers all 39 available cases, and does so with a latency that would
be undetectable to developers. On the new set of cases, it handles most examples involving
async / await , const fn , NLCF, generics, and HRTBs, but also exposes a set of failures
around DTOs and some of the more complex generic bounds. Taken together, these results
support RQ1 and RQ2: REM2.0 is at least as capable as the original tool and substantially
more expressive in the Rust features it can refactor.

For performance (RQ3), the contrast is highly impressive. The original REM pipeline had
extraction times in the hundreds to thousands of milliseconds, likely not including the work
done by IntelliJ. By reusing RA’s analysis in a persistent daemon, REM2.0 reduces the raw
extraction costs to a few milliseconds and user-experienced latency to well under a quarter of a
second.

The verification results offer a new perspective (RQ4). For code within the subset supported by
CHARON and AENEAS, the verifier is capable of producing end-to-end equivalence proofs between
original and extracted functions. This is orders of magnitude slower than extraction and re-
stricted to a subset of Rust, but provides a much stronger guarantee. In practice, this suggests
that there is going to be a two-tier workflow: developers use REM2.0’s fast extraction by de-


                                                41
fault and selectively invoke the repairer or the verification pipeline for safety-critical code, tricky
lifetime patterns, or APIs with strong behavioural contracts that need to be upheld.

Finally, the usage profile of REM-Repairer confirms its role as a targeted component of the
toolchain. It is still essential for cases with tight lifetime constraints, but most extractions
can succeed without it. However, as shown above, the large latency introduced with VSCode’s
overhead more than outweighs the call to the Repairer, and thus we have made the Extract +
Repair pathway the default option inside our VSCode extension.
5.6.2    Threats to Validity

As with any empirical study, our evaluation is subject to several threats to validity:

Internal validity. Timing measurements for RQ3 and RQ4 are affected by system noise,
caching, and warm-up behaviour in RA and the OS. Although we did our best to use a controlled
environment and consistent configurations, individual runs may vary slightly, so the numbers
should be read as relative trends rather than precise bounds.

External validity. Our benchmarks, while drawn from real projects, are limited by necessity.
The original REM suite captured a specific snapshot of Rust code and the new corpus focuses
on large, popular GitHub repositories with manually curated extraction sites. This biases the
evaluation toward more ”mainstream” code and as such cannot cover domains such as embedded
no std crates or highly specialised libraries.

Construct validity. We treat compilation success and, where applicable, successful CHARON/AENEAS
proofs as proxies for refactoring correctness (RQ1, RQ2, RQ4). In practice, we can only have
a superficial understanding of each example and largely rely on the Rust compiler and (where
possible) the verification pipeline to detect problems. While the type system and borrow checker
catch many errors, subtle behavioural changes (e.g. performance, logging, concurrency effects)
may still go unnoticed.

Tool ecosystem stability. REM2.0 depends on internal APIs of RA and on external verifi-
cation tools (CHARON, AENEAS) that are under active development16 . Future changes may alter
behaviour, performance, or supported features, so our results capture a particular point in the
evolution of this tool stack.

5.7     Summary
This section has evaluated REM2.0 against the four research questions posed at the start of this
section. The extraction experiments show that REM2.0 matches and extends the capabilities
of the original REM prototype (RQ1, RQ2), while the new architecture delivers interactive,
IDE-like latency by reusing RA’s incremental analysis in a persistent daemon (RQ3). For code
within the currently supported CHARON/AENEAS fragment, the verification pipeline can further
certify behavioural equivalence between original and extracted functions, at substantially higher
performance cost but with correspondingly stronger guarantees (RQ4).
  16
    specifically the internal APIs of RA are designed entirely for use within RA, and do break often. Our
toolchain is built on version 0.0.262, but with weekly releases the API is already up to version 0.0.3XX. Whilst
there has been no update to the major components we rely on, a brief attempt to migrate was quickly disbanded


                                                      42
Overall, the results indicate that REM2.0 provides a practical extract-function refactoring for
modern Rust, with a fast default path and targeted support for both automated repair and
optional formal verification when additional assurance is required.


6     Conclusions and Future Work
6.1     Revisiting Aims and Research Questions
The aim of this project was to design, implement, and evaluate a practical extract-function
refactoring toolchain for Rust that can handle modern language features and, where possible,
provide stronger correctness guarantees than “it still compiles”. Concretely, the work set out
to build a new version of REM that integrates with rust-analyzer, supports contemporary
Rust language features such as async / await and const fn , and connects to a verification
pipeline for equivalence checking.

Section 5 framed this aim in terms of four research questions:

• RQ1 – Does the new toolchain match or exceed the original REM on the existing benchmark
    suite?
• RQ2 – To what extent can the new extraction pipeline handle modern Rust features ( async ,
     const fn , generics, higher-ranked trait bounds, dynamic trait objects, and non-local control
    flow)?
• RQ3 – What extraction latencies are achievable when we reuse rust-analyzer as a persistent
    analysis daemon, and how does this impact the user experience?
• RQ4 – For code within the supported subset, can we feasibly verify equivalence between
    original and extracted functions using CHARON and AENEAS?

The evaluation results give us clear answers. For RQ1, REM2.0 achieves strict parity with
the original REM on the original benchmark suite and additionally succeeds on several cases
that previously failed. For RQ2, it handles the majority of feature-focused examples involving
async , const , NLCF, generics, and HRTBs, with remaining weaknesses concentrated around
DTOs and intricate generic bounds. For RQ3, the new architecture reduces extraction latency
from hundreds or thousands of milliseconds to a few milliseconds internally and to well under a
quarter of a second as observed in the editor. For RQ4, the verification pipeline can construct
end-to-end equivalence proofs for a non-trivial fragment of Rust, although at substantially
higher performance cost and with a restricted language subset.

6.2     Summary of Contributions
Against this backdrop, the paper makes several technical and empirical contributions.
6.2.1    A RA based architecture for extraction.

The first contribution is the design and implementation of REM2.0 as a long-lived daemon built
on top of RA. Instead of repeatedly invoking the Rust compiler on whole crates, REM2.0 reuses
RA’s analysis and exposes a JSON-RPC interface that can be driven from a VSCode extension
or command-line client. This extension is currently available on the VSCode marketplace.


                                                43
6.2.2    A feature-rich extraction engine.

Second, the project develops an extraction engine that supports a much broader range of
Rust features than the original REM prototype.       It operates correctly in the presence of
async / await , const fn , HRTBs, generics with multiple trait constraints, and NLCF, using
std::ops::ControlFlow to standardise return s, break , and continue . It still struggles on
DTO-heavy cases, which remain the most complex feature class and a clear area for continued
research.
6.2.3    A repairer for lifetimes and type signatures.

Third, the work refines and reuses REM-Repairer as a post-processing step that automatically
adjusts extracted function signatures and lifetime annotations when the original extraction
creates borrow-checker errors. Empirically, the repairer is needed in the same kinds of cases
as in the original evaluation—those with tight lifetime constraints—and thus remains a crucial
component of the overall toolchain rather than a mere convenience.
6.2.4    Integration with verification tooling.

Fourth, we prototyped a verification pipeline that connects REM2.0 to AENEAS. For functions
within the supported fragment, this pipeline is able to translate original and extracted code to
Coq definitions and construct proofs that the two versions are behaviourally equivalent. This
provides a path from ordinary refactoring to machine-checked correctness guarantees for selected
cases, building on the broader vision of correct-by-construction programming [32].
6.2.5    Empirical evaluation on real Rust projects.

Finally, the project contributes a large empirical study across three benchmark corpora. These
experiments demonstrated that the architecture scales to realistic workloads, quantify the la-
tency improvements, and characterise the strengths, direct improvements, and failure modes of
REM2.0.

6.3     Limitations and Open Challenges
Despite these contributions, REM2.0 has clear limitations that draw a line in the sand as to
where it can be relied upon today and where further work is needed.

On the language-feature side, DTOs and complex generic bounds are the biggest current weak-
nesses. Several failure cases arose when the extractor could not reconstruct a precise function
signature, falling back to unspecified types or dropping bounds. This is closely related to the
second limitation: REM2.0 mostly operates with a modified single-file view based on RA’s crate
graphs, which makes it difficult to discover constraints defined in modules we do not explicitly
trace and import.

The verification pipeline is similarly constrained by the subset that is supported by AENEAS.
Many real-world functions make use of features that lie outside this subset, and even when
verification is possible, it incurs significantly higher cost than extraction. As a result, the
verifier cannot yet be applied indiscriminately to arbitrary refactorings and is best seen as an
optional, high-assurance mode.


                                              44
Finally, the evaluation focuses on correctness and performance, not on user experience. We
have not performed a study to assess how developers actually adopt the tool, how often they
invoke verification, or how much they trust the results. Understanding these human factors is
an important but out-of-scope challenge.

6.4   Future Directions
Several areas of future work follow directly from the limitations and from our broader vision of
provably correct refactorings.

A first direction is deeper integration with RA. By drawing on more global crate-graph infor-
mation, REM2.0 should be able to extract richer trait and where-clause information, closing
many of the gaps we have seen with DTOs and complex generic bounds. This may involve ex-
tending internal APIs or contributing changes upstream. Although unlikely due to its reliance
on cargo check, integrating the repairer into RA remains a long term engineering goal of this
project.

A second direction is to extend the equivalence fragment. As CHARON and AENEAS improve, there
is scope to support a larger subset of Rust—with interior mutability being a major feature
to look forward to. At the same time, a deeper understanding of the LLBC (and potential
integration with the polonius borrow checker) could be used to substantially increase how much
of the original rust we can directly reason about without needing to perform the functional
translation.

Third, there is room for smarter repair and analysis heuristics. REM-Repairer could be up-
graded to infer missing bounds or function annotations from the compiler feedback it already
collects, or by learning patterns from previously successful repairs. Static checks that predict
whether a given extraction is likely to be verifiable could help developers decide when it is worth
paying the verification cost.

Finally, complex ownership cases remain an important open challenge. Developers routinely
work around borrow-checker rejections by introducing selective clone s, passing individual fields
instead of whole structs, or using interior mutability. These borrow checking issues are some-
thing that the Polonius project aims to rectify. At present, REM2.0 treats such situations as
hard failures as we rely on the Rust compiler which is unable assist us with. A natural direction
for future work is to recognise and apply a small catalogue of semantics-preserving “borrow
repair” patterns, so that more extractions can be automatically reshaped into forms that sat-
isfy the borrow checker without changing the intended behaviour. A potential advancement
from there will be utilising the Polonius borrow checker or reaching into the LLBC semantics
to further improve the original extraction.

6.5   Broader Outlook
Stepping back, this paper sits at an intersection of refactoring tools, modern language servers,
and formal verification. Rust is a demanding testbed for safe automated refactoring: its owner-
ship and lifetime system make entire classes of bugs unpresentable, but as we and many others



                                                45
    have discovered, those guarantees make naı̈ve extractions impossible and well intentioned ones
    incredibly difficult.

    REM2.0 shows that a RA-based design can deliver extract-function refactorings that are both
    fast enough for everyday use and expressive enough to handle a wide range of contemporary Rust
    language features. The addition of a repair stage and a verification pipeline demonstrates that
    we can go beyond compilation as our only correctness source, and selectively obtain machine-
    checked evidence that a refactoring preserves behaviour.

    If such tools become commonplace, they could change how developers think about the large-
    scale evolution of Rust code: many refactorings would remain cheap, interactive, and IDE-
    driven, while critical feature changes could be escalated to formally justified transformations
    with minimal disruption to the developer’s workflow. More broadly, the work suggests a path
    toward refactoring tools that treat correctness as their main concern rather than an afterthought.
    In this sense, REM2.0 is not just a faster extract-function command for Rust, but an early
    step toward a generation of refactoring tools that integrate verification into everyday software
    engineering practice.


    A     Appendix 1: Passing by Value and Reference
    This appendix provides three short, self-contained examples of “naı̈ve” function hoisting in Rust.
    In each example, we will define a function that is getting refactored, and we will demonstrate
    the case where the arguments to the function are passed by value and the case where they
    are passed by reference. To achieve this, we are imagining an automated refactoring tool that
    initially takes an inline block of code and moves it into a new function. The compilation errors
    (if any) guide a subsequent ownership analysis, which deduces how each variable should be
    passed: by value ( T ), by shared reference ( &T ), or by mutable reference ( &mut T ).

    A.1    Example 1: Passing by Value
    Original Code (inline)
1   fn main() {
2       let x = 42;
3       let y = x * 2;
4       println!("y is {}", y);
5   }


                                  Listing 6: Passing by value: Original

    Naı̈ve Hoisted Code (before fixes)

    Suppose an automated refactoring tool decides to “hoist” the multiplication logic into a new
    function:


1   fn hoisted_block(x: i32) {


                                                   46
2          let y = x * 2;
3          println!("y is {}", y);
4    }
5

6    fn main() {
7        let x = 42;
8        hoisted_block(x);
9    }


                              Listing 7: Passing by value: Naı̈ve extraction

     In this example, no errors occur because after calling hoisted block(x) , we do not need x
     again in main , so moving (passing ownership) is safe. The automated repair analysis detects
     that x is no longer needed in main and decides it can be passed by value.

     A.2     Example 2: Passing by Shared Reference
     Original Code (inline)
1    fn main() {
2        let text = String::from("Hello world!");
3        let length = text.len();
4

5          // Some inline block that only reads from ‘text‘:
6          println!("First word is: {}", get_first_word(&text));
7          println!("Total length is: {}", length);
8    }
9

10   fn get_first_word(s: &str) -> &str {
11       s.split_whitespace().next().unwrap_or("")
12   }


                             Listing 8: Passing by shared reference: Original

     Naı̈ve Hoisted Code (before fixes)

     Let’s say the refactoring tool decides to hoist the usage of get first word (or a bit more logic
     around it) into a new helper function:
1    fn main() {
2        let text = String::from("Hello world!");
3        let length = text.len();
4

5          // Some inline block that only reads from ‘text‘:
6          println!("First word is: {}", get_first_word(&text));
7          println!("Total length is: {}", length);
8    }
9

10   fn get_first_word(s: &str) -> &str {


                                                   47
11         s.split_whitespace().next().unwrap_or("")
12   }


                          Listing 9: Passing by shared reference: Naı̈ve extraction

     This version won’t compile as expected if the function print first word block takes text
     by value. Once text is moved into print first word block , we can no longer use text
     afterward in main . The compiler will complain that text is moved, thus invalidating the line
     println!("Total length is:          ", length); if we needed text for anything else.

     Automated Repair Yields
1    fn print_first_word_block(text: &String) {
2        // Only reads from ‘text‘, so it only needs a shared reference.
3        println!("First word is: {}", get_first_word(text));
4    }
5

6    fn main() {
7        let text = String::from("Hello world!");
8        let length = text.len();
9

10         print_first_word_block(&text); // Pass a shared reference
11         println!("Total length is: {}", length);
12   }


                        Listing 10: Passing by shared reference: Automated Repair

     What’s going on?

         • Read-only usage: The function print first word block just needs to read the string
            (in order to print the first word).

         • Shared reference: Because the string must remain valid afterward in main , the owner-
            ship analysis decides that passing by shared reference ( &String ) is correct.

     A.3     Example 3: Passing by Mutable Reference
     Original Code (inline)
1    fn main() {
2        let mut values = vec![1, 2, 3];
3

4          // Some inline block that mutates ‘values‘:
5          values.push(4);
6          println!("Values are now: {:?}", values);
7    }


                             Listing 11: Passing by mutable reference: Original



                                                     48
     Naı̈ve Hoisted Code (before fixes)

     Hoisting the push operation into a new function could look like this:
 1   fn push_block(values: Vec<i32>) {
 2       let mut v = values;
 3       v.push(4);
 4       println!("Values are now: {:?}", v);
 5   }
 6

 7   fn main() {
 8       let mut values = vec![1, 2, 3];
 9       push_block(values);
10       println!("Final values: {:?}", values); // error: ‘values‘ was moved
11   }


                        Listing 12: Passing by mutable reference: Naı̈ve extraction

     Here, we have a compilation error similar to Example 2: once values is passed by value,
     ownership is transferred, and we cannot use values again in main . However, in this case, we
     truly do need to mutate values , and we want main to see the updated vector.

     Automated Repair Yields
 1   fn push_block(values: &mut Vec<i32>) {
 2       values.push(4);
 3       println!("Values are now: {:?}", values);
 4   }
 5

 6   fn main() {
 7       let mut values = vec![1, 2, 3];
 8       push_block(&mut values);
 9       println!("Final values: {:?}", values); // Now values is still in scope and
         updated
10   }


                     Listing 13: Passing by mutable reference: Automated Repair

     What’s going on?

        • Mutation required: The code needs to modify the original vector.

        • Mutable reference: By passing &mut Vec<i32> , the function can mutate values in
          place, and main retains ownership of values to use afterward.




                                                    49
B    Appendix 2: Details of each Repository
            Ranking            Project Repo           Stars    Forks   Open Issues
               2               denoland/deno          105077    5768      2384
               3             rustdesk/rustdesk        102158   14993       61
               4              tauri-apps/tauri         98717    3155      1161
               5              unionlabs/union          74500    3835      155
               6                 astral-sh/uv          72353    2212      2136
               7            zed-industries/zed         69398    5885      3054
               8               FuelLabs/sway           62106    5428      862
               9             alacritty/alacritty       60977    3227      323
              10            rust-lang/rustlings        60569   10978       46
              11            FuelLabs/fuel-core         57463    2856      149
              12            BurntSushi/ripgrep         57159    2304       85
              13            topjohnwu/Magisk           56856   15853       36
              14                sharkdp/bat            55755    1409      318
              15         meilisearch/meilisearch       54438    2254      221
              16              lencx/ChatGPT            54214    6192      856
              17       rust-unofficial/awesome-rust    53670    3064       10
              18             starship/starship         52113    2284      762
              19         dani-garcia/vaultwarden       50694    2374       17
              20                openai/codex           50131    6215      1164
              21                 types/typst           47876    1305      1007

Table 8: Brief summary of the 20 repositories searched to find real-world examples. #1 is the
                                    Rust project itself.




                                               50
#    Name                URL
1    denoland/           https://github.com/denoland/deno/commit/
     deno                104514b06dfbbb899235fb1147aa1fa62477a6d5
 2   FuelLabs/           https://github.com/FuelLabs/fuel-core/commit/
     fuel-core           ed92738280e068475682e220b93921bbbfebfdd7
 3   meilisearch/        https://github.com/meilisearch/meilisearch/commit/
     meilisearch         31142b36635ba062184b7d42f2e86021b11e911c
 4   BurntSushi/         https://github.com/BurntSushi/ripgrep/commit/
     ripgrep             7534d5144f5c5e89d67c791e663cdc0bee069b0e
 5   starship/           https://github.com/starship/starship/commit/
     starship            9093891acbe2c86b1615c37386dadbb0cc632199
 6   FuelLabs/           https://github.com/FuelLabs/sway/commit/
     sway                cdfc56c700ab32eefb84f75ed3048bd2a0ea22d2
 7   tauri-apps/         https://github.com/tauri-apps/tauri/commit/
     tauri               658e5f5d1dc1bd970ae572a42447448d064a7fee
 8   unionlabs/          https://github.com/unionlabs/union/commit/
     union               9b01ce6d75b84f049c1ede75750d33ce26ae73d9
 9   astral-sh/          https://github.com/astral-sh/uv/commit/
     uv                  9af989e30c86391767830aa588c32fcb7c9a76b5
10   dani-garcia/        https://github.com/dani-garcia/vaultwarden/commit/
     vaultwarden         952992c85bdf3147ddb8e663538e29c748b71f94
11   zed-                https://github.com/zed-industries/zed/commit/
     industries/zed      d00ad02b05981c79942b3bdff957e2384e68b89f

Table 9: Details of each repository in the evaluation, with the specific commit hash that we
                          found examples from / evaluated against




                                            51
     C       Appendix 3: GitOxide Example in Detail
     The following diff shows how the ‘if add path‘ block was refactored into the new helper method
     extract include path.
 1   -         if add_path {
 2   -             if let Some(body) = target_config.sections.get(&id) {
 3   -                 let paths = body.values(&Key::from("path"));
 4   -                 let paths = paths.iter().map(|path| values::Path::from(path.clone()))
         ;
 5   -                 include_paths.extend(paths);
 6   -             }
 7   -         }
 8             // Some specifics ommited for simplicity
 9   +         if add_path {
10   +             extract_include_path(target_config, &mut include_paths, id)
11   +         }


     And here is the new method in full:
 1   fn extract_include_path<’a>(
 2       target_config: &mut File<’a>,
 3       include_paths: &mut Vec<values::Path<’a>>,
 4       id: SectionId
 5   ) {
 6       if let Some(body) = target_config.sections.get(&id) {
 7           let paths = body.values(&Key::from("path"));
 8           let paths = paths.iter().map(|path| values::Path::from(path.clone()));
 9           include_paths.extend(paths);
10       }
11   }


                                   Listing 14: Full gitoxide method




                                                  52
     D     Appendix 4: Complete MIR from H.3
1    // WARNING: This output format is intended for human consumers only
2    // and is subject to change without notice. Knock yourself out.
3    fn main() -> () {
4        let mut _0: ();
5        let _1: std::vec::Vec<i32>;
6        let mut _2: std::boxed::Box<[i32]>;
7        let mut _3: usize;
8        let mut _4: usize;
9        let mut _5: *mut u8;
10       let mut _6: std::boxed::Box<[i32; 3]>;
11       let _8: &i32;
12       let mut _9: &std::vec::Vec<i32>;
13       let _10: ();
14       let mut _11: std::fmt::Arguments<’_>;
15       let _12: &[&str; 2];
16       let _13: &[core::fmt::rt::Argument<’_>; 1];
17       let _14: [core::fmt::rt::Argument<’_>; 1];
18       let mut _15: core::fmt::rt::Argument<’_>;
19       let _16: &&i32;
20       let mut _17: *const [i32; 3];
21       let mut _18: *const ();
22       let mut _19: usize;
23       let mut _20: usize;
24       let mut _21: usize;
25       let mut _22: usize;
26       let mut _23: bool;
27       scope 1 {
28           debug v => _1;
29           let _7: &i32;
30           scope 2 {
31               debug x => _7;
32           }
33       }
34

35       bb0: {
36           _3 = SizeOf([i32; 3]);
37           _4 = AlignOf([i32; 3]);
38           _5 = alloc::alloc::exchange_malloc(move _3, move _4) -> [return: bb1, unwind continue];
39       }
40

41       bb1: {
42           _6 = ShallowInitBox(move _5, [i32; 3]);
43           _17 = copy (((_6.0: std::ptr::Unique<[i32; 3]>).0: std::ptr::NonNull<[i32; 3]>).0: *
         const [i32; 3]);
44           _18 = copy _17 as *const () (PtrToPtr);
45           _19 = copy _18 as usize (Transmute);
46           _20 = AlignOf([i32; 3]);
47           _21 = Sub(copy _20, const 1_usize);
48           _22 = BitAnd(copy _19, copy _21);
49           _23 = Eq(copy _22, const 0_usize);



                                                   53
50           assert(copy _23, "misaligned pointer dereference: address must be a multiple of {} but
         is {}", copy _20, copy _19) -> [success: bb10, unwind unreachable];
51       }
52

53       bb2: {
54            _9 = &_1;
55            _8 = <Vec<i32> as Index<usize>>::index(move _9, const 0_usize) -> [return: bb3, unwind:
           bb8];
56       }
57

58       bb3: {
59           _7 = copy _8;
60           _12 = const main::promoted[0];
61           _16 = &_7;
62           _15 = core::fmt::rt::Argument::<’_>::new_display::<&i32>(copy _16) -> [return: bb4,
         unwind: bb8];
63       }
64

65       bb4: {
66           _14 = [move _15];
67           _13 = &_14;
68           _11 = Arguments::<’_>::new_v1::<2, 1>(copy _12, copy _13) -> [return: bb5, unwind: bb8
         ];
69       }
70

71       bb5: {
72           _10 = _print(move _11) -> [return: bb6, unwind: bb8];
73       }
74

75       bb6: {
76           drop(_1) -> [return: bb7, unwind continue];
77       }
78

79       bb7: {
80           return;
81       }
82

83       bb8 (cleanup): {
84           drop(_1) -> [return: bb9, unwind terminate(cleanup)];
85       }
86

87       bb9 (cleanup): {
88           resume;
89       }
90

91       bb10: {
92           (*_17) = [const 1_i32, const 2_i32, const 3_i32];
93           _2 = move _6 as std::boxed::Box<[i32]> (PointerCoercion(Unsize, Implicit));
94           _1 = slice::<impl [i32]>::into_vec::<std::alloc::Global>(move _2) -> [return: bb2,
         unwind continue];
95       }
96   }



                                                    54
 97

 98   const main::promoted[0]: &[&str; 2] = {
 99       let mut _0: &[&str; 2];
100       let mut _1: [&str; 2];
101

102       bb0: {
103           _1 = [const "", const "\n"];
104           _0 = &_1;
105           return;
106       }
107   }


                                   Listing 15: Complete MIR from H.3




                                                  55
E    Appendix 5: Plotted Extraction time data




Figure 11: Execution time breakdown by pipeline stage for each test case. Times are reported
                     in seconds (derived from nanosecond timing data).




                                            56
                       Load the   Analysis   Get the   Filter For   Apply EF
       Case                                                                    Remaining    Total
                       Analysis   Loaded     Assists   EF Assist      Assist
beerus-ext-com1        9285       86226      2120      2060529      2476       5371        2166007
gitoxide-ext-com1      307613     128739     2785      2887546      2574       7746        3337003
gitoxide-ext-com2      10238      100897     2468      1872872      2692       28872       2018039
gitoxide-ext1          454708     90926      2210      1583716      3171       13176       2147907
gitoxide-ext2          468576     99266      2948      1449459      3634       6355        2030238
gitoxide-ext3          593338     121557     2593      2098630      4041       30428       2850587
gitoxide-ext4          387921     109024     2798      2715010      3668       21512       3239933
gitoxide-ext5          520525     101651     2508      2183887      2948       11685       2823204
gitoxide-ext6          529156     104946     2568      2342050      2513       10251       2991484
gitoxide-ext7          290983     101383     2307      2869735      5587       11670       3281665
gitoxide-inline-ext1   376787     96027      2954      2508828      3532       6906        2995034
gitoxide-inline-ext2   496737     105101     2427      4729361      3486       8189        5345301
gitoxide-inline-ext3   488481     122647     3248      4827718      4000       21855       5467949
gitoxide-inline-ext4   495756     121965     3684      3281795      5483       15325       3924008
gitoxide-inline-ext5   495051     112329     2474      2657133      2991       12808       3282786
gitoxide-inline-ext6   622550     107609     2873      4480736      3848       22912       5240528
gitoxide-inline-ext7   403207     96122      2356      2769977      2617       8734        3283013
kickoff-ext1           494546     112377     3619      2768148      2671       14533       3395894
kickoff-ext2           398752     124576     2850      2443569      2733       11091       2983571
kickoff-ext3           492629     110374     2586      2531962      2069       13516       3153136
kickoff-ext4           578567     108555     2736      2514134      3164       22551       3229707
kickoff-inline-ext1    520277     126225     2583      2793580      2920       11691       3457276
petgraph-ext1          374755     105993     2342      3306952      3347       9064        3802453
petgraph-ext2          929776     181024     3519      7384406      4936       53650       8557311
petgraph-ext3          881791     149205     2483      6287406      2447       42136       7365468
petgraph-ext4          671999     123294     3069      4046105      3188       16542       4864197
petgraph-ext5          400859     86750      2658      3688382      3107       9421        4191177
petgraph-ext6          853792     154358     3156      6198179      2902       75377       7287764
petgraph-inline-ext1   550082     114773     3004      4988262      3287       14740       5674148
sniffnet-ext1          318576     89782      3191      4012997      2925       11313       4438784
sniffnet-ext2          521024     108808     2324      2959298      2719       7431        3601604
sniffnet-ext3          491132     114474     2420      2639553      2501       14870       3264950
sniffnet-ext4          289206     104857     2458      3087829      3184       19270       3506804
sniffnet-ext5          451829     112413     2904      3560519      2571       16898       4147134
sniffnet-ext6          665962     163596     5027      3423886      2428       22809       4283708
sniffnet-ext7          610395     115393     3062      3518957      6090       19601       4273498
sniffnet-inline-ext1   606027     117642     2553      4392070      8793       30967       5158052
sniffnet-inline-ext2   830359     110345     3269      1060569      7246       13375       2025163

       Table 10: Raw timing data for the various extractions. Times are all in nanoseconds




                                                       57
     F       Appendix 6: (Almost) Complete Coq Translations
     Some of the Coq boilerplate has been removed to make these inclusions sensible. Still it is clear
     how massive the translation can get for even a small example.
1    Definition bump
2      {N : usize} (coremarkerCopyArrayI32NInst : core_marker_Copy (array i32 N))
3      (arr : array i32 N) (k : usize) (mark : bool) :
4      result ((array i32 N) * bool)
5      :=
6      if k s< N then bump_loop0 k arr mark 0%usize else bump_loop1 arr mark 0%usize
7    .
8
9    (* *)
10   (* *)
11   (* *)
12   (* *)
13   (* *)
14   (* *)
15   (* *)
16   (* *)
17   (* *)
18   (* *)
19   (* *)
20   (* *)
21   (* *)
22   (* *)
23   (* *)
24   (* *)
25   (* *)
26   (* *)
27   (* *)
28   (* *)



                         Listing 16: Original Coq translation, less some boilerplate




                                                         58
1    Definition bump
2      {N : usize} (coremarkerCopyArrayI32NInst : core_marker_Copy (array i32 N))
3      (arr : array i32 N) (k : usize) (mark : bool) :
4      result ((array i32 N) * bool)
5      :=
6      if k s< N
7      then (
8        _ <- bump_loop0 coremarkerCopyArrayI32NInst arr k mark 0%usize;
9        Ok (arr, mark))
10     else (
11       _ <- bump_loop1 coremarkerCopyArrayI32NInst arr mark 0%usize;
12       Ok (arr, mark))
13   .
14
15   Definition bump_extracted
16     {N : usize} (coremarkerCopyArrayI32NInst : core_marker_Copy (array i32 N))
17     (arr : array i32 N) (i : usize) (mark : bool) :
18     result unit
19     :=
20     i1 <- array_index_usize arr i;
21     if i1 s= 0%i32
22     then (_ <- i32_add i1 1%i32; _ <- array_index_mut_usize arr i; Ok tt)
23     else (_ <- i32_add i1 1%i32; _ <- array_index_mut_usize arr i; Ok tt)
24   .



              Listing 17: Coq translation of the Incorrect Extraction, less some boilerplate




                                                         59
    G      Appendix 7:              New Extraction Feature Categories in De-
           tail
    In this appendix we give concrete (although somewhat small) examples for each of the feature
    categories introduced in Section 5.4.2. The examples are drawn from the repositories listed in
    Section 5.2.3, or are lightly simplified variants of patterns we observed there, and are designed
    to isolate the behaviour of the extractor in the presence of a particular construct. In addition
    to asynchronous functions, const evaluation, generics, dynamic trait objects, and higher-ranked
    trait bounds, we include several instances of non-local control flow. Although the original REM
    toolchain could already handle some non-local control-flow refactorings, the new extraction
    engine implements them via the (now) standard std::ops::ControlFlow variants rather than
    custom enums, and we therefore evaluate them separately. Together, these examples characterise
    the kinds of advanced language mechanics that the original REM could not support and that the
    new toolchain is explicitly designed to handle, allowing us to check that it preserves semantics,
    typing, and compilation validity in each case.

    G.0.1     Generics (GEN)

    This case targets a generic function with multiple trait bounds, verifying that these are copied
    exactly to the extracted function. The extractor must not monomorphise or omit generic
    parameters, as doing so would restrict the function’s polymorphism and likely fail type checking.
    Additionally, if only a subset of the caller functions trait bounds apply to the callee (e.g. it only
    takes one of many generic arguments), then we would expect just the applicable trait bounds
    to be copied).

1   fn min_of<T: Ord + Copy>(a: T, b: T) -> T {         1    fn min_of<T: Ord + Copy>(a: T, b: T) -> T {
2       // EXTRACT START                                2        choose_min(a, b)
3       if a < b { a } else { b }                       3    }
4       // EXTRACT END                                  4
5   }                                                   5    fn choose_min<T: Ord + Copy>(a: T, b: T) -> T
                                                                   {
                                                        6        if a < b { a } else { b }
     Listing 18: Generics Example: Before               7    }



                                                                 Listing 19: Generics Example: After

    G.0.2     Async and Await (ASYNC)

    This case targets extraction from within an async fn , where the inserted boundaries must
    remain within the compiler-generated state machine 17 .The extractor must correctly preserve the
    asynchronous context and the Result return type implied by ? , while ensuring that lifetimes
    and borrows are not widened across the await suspension point. If the lifetimes produced by
    the extraction engine are incorrect, we expect REM-Repairer to correct them.
      17
         rustc automatically generates a struct that acts as a state machine, with an internal state variable and a
    poll method. Each await point becomes a place where the state machine can pause, return Poll::Pending , and
    be resumed later by the runtime without losing its state.




                                                            60
1   async fn fetch_and_tag(client: &Client, id:      1    async fn fetch_and_tag(client: &Client, id:
         u64) -> Result<String, Error> {                       u64) -> Result<String, Error> {
2       // EXTRACT START                             2        fetch_and_tag_inner(client, id).await
3       let body = client.get(id).await?;     //     3    }
         await inside block                          4
4       let tagged = format!("[#{}] {}", id, body    5    async fn fetch_and_tag_inner(client: &Client,
         );                                                     id: u64) -> Result<String, Error> {
5       // EXTRACT END                               6        let body = client.get(id).await?;
6       Ok(tagged)                                   7        let tagged = format!("[#{}] {}", id, body
7   }                                                          );
                                                     8        Ok(tagged)
                                                     9    }
       Listing 20: Async Example: Before

                                                              Listing 21: Async Example: After

    G.0.3    Constant declarations (CONST)

    This case covers extraction within a const fn , which must remain evaluable at compile time
    under Rust’s const-checking rules. Thus the extraction engine must identify const contexts, and
    where possible, propagate the const qualifier to the new function to maintain those guarun-
    tees.

1   // A const function that can be evaluated at     1    // A const function that can be evaluated at
         compile time                                          compile time
2   const PREFIX: u32 = 10;                          2    const PREFIX: u32 = 10;
3   const fn compute_total(a: u32, b: u32) -> u32    3    const fn compute_total(a: u32, b: u32) -> u32
          {                                                     {
4       // EXTRACT START                             4        compute_total_inner(a, b)
5       PREFIX + a + b                               5    }
6       // EXTRACT END                               6
7   }                                                7    // Extracted function still marked as const
                                                     8    const fn compute_total_inner(a: u32, b: u32)
                                                               -> u32 {
     Listing 22: CONST Example: Before               9        PREFIX + a + b
                                                    10    }



                                                              Listing 23: CONST Example: After

    G.0.4    Non Local Control Flow (NLCF)

    This case covers all aspects of NLCF, being return , break , and continue in Rust. NLCF
    objects cannot cross function boundaries, and as such the extraction engine must reify control
    flow into a return value, using std::ops::ControlFlow variants to communicate termination
    or continuation back to the caller. As mentioned previously, this differs from REM’s original
    insertion of custom enums to outline control flow handling, as we rely on the extraction engine
    to provide this information rather than REM-Controller.




                                                         61
 1   fn sum_until_negative(xs: &[i32]) -> i32 {      1    use std::ops::ControlFlow;
 2       let mut sum = 0;                            2    use std::ops::ControlFlow::{Break, Continue};
 3       for &x in xs {                              3    fn sum_until_negative(xs: &[i32]) -> i32 {
 4           // EXTRACT START                        4        let mut sum = 0;
 5           if x < 0 { break; }   // non-local ‘    5        for &x in xs {
          break‘                                     6             match step_sum_cf(x) {
 6           sum += x;                               7                 Break(()) => break,
 7           // EXTRACT END                          8                 Continue(delta) => sum += delta,
 8       }                                                     } }
 9       sum                                         9        sum
10   }                                              10    }
                                                    11    fn step_sum_cf(x: i32) -> ControlFlow<(), i32
                                                               > {
       Listing 24: NLCF Example: Before             12        if x < 0 { Break(()) }
                                                    13        else { Continue(x) }
                                                    14    }



                                                              Listing 25: NLCF Example: After

     G.0.5    Higher Ranked Trait Bounds (HRTB)

     This case examines extraction from functions parameterised by higher-ranked trait bounds
     such as for<’a> Fn(&’a T) -> &’a T . These bounds are not inferred implicitly and must be
     explicitly copied to the new function signature to maintain lifetime correctness. Again, REM-
     Repairer is expected to be called here to either a) verify that the lifetimes are correct, and / or
     b) fix the incorrect lifetime bounds.

 1   fn apply_str<F>(f: F) -> &’static str           1    fn apply_str<F>(f: F) -> &’static str
 2   where                                           2    where
 3       F: for<’a> Fn(&’a str) -> &’a str,          3        F: for<’a> Fn(&’a str) -> &’a str,
 4   {                                               4    {
 5       let s = "hello";                            5        call_higher(f)
 6       // EXTRACT START                            6    }
 7       f(s)                                        7
 8       // EXTRACT END                              8    fn call_higher<F>(f: F) -> &’static str
 9   }                                               9    where
                                                    10        F: for<’a> Fn(&’a str) -> &’a str,
                                                    11    {
       Listing 26: HRTB Example: Before             12        let s = "hello";
                                                    13        f(s)
                                                    14    }



                                                              Listing 27: HRTB Example: After

     G.0.6    Dynamic Trait Objects (DTO)

     Here we isolate extraction involving a &dyn Trait parameter to test the extraction engines
     preservation of dynamic dispatch and object safety.            The extractor must retain the trait
     object type and avoid replacing it with a generic bound, which would alter runtime be-
     haviour. The category also includes cases where a function’s arguments implement a trait,
     e.g. fn ident(s:       impl Into<String> -> ... .




                                                         62
1   use std::fmt::Display;                       1   use std::fmt::Display;
2                                                2
3   fn show_twice(d: &dyn Display) -> String {   3   fn show_twice(d: &dyn Display) -> String {
4       // EXTRACT START                         4       show_twice_inner(d)
5       format!("{} | {}", d, d)                 5   }
6       // EXTRACT END                           6
7   }                                            7   fn show_twice_inner(d: &dyn Display) ->
                                                          String {
                                                 8       format!("{} | {}", d, d)
       Listing 28: DTO Example: Before           9   }



                                                          Listing 29: DTO Example: After




                                                     63
H       Appendix 8: Implementation of the Verification Pipeline
This appendix contains a much more thorough dive into all of the implementation details behind
the equivalence proover. It is intended to be read alongside the source code, and will in places
contain duplicate information from Section 4.5.

The design of REM2.0’s equivalence checking is
                                                                       1. Extraction
guided by two principles: (1) verification must re-
quire no additional annotations or input from the
developer, and (2) it must complete quickly enough
to fit into interactive IDE workflows. To achieve                    2. REM Repairs
this, the pipeline translates both the original pro-
gram P and the refactored program P ′ into progres-
sively more structured semantic representations, cul-
                                                                  3. CHARON (LLBC)
minating in a machine-checked proof of observational
equivalence.
At a high level, the pipeline consists of five stages:
Extraction, REM repairs, CHARON transla-                     4. AENEAS (Functionalisation)
tion, AENEAS functionalisation, and Coq ver-
ification. Each stage builds on the previous one,
gradually exposing the semantics of the refactored
                                                                    5. Coq Verification
code, before we end up with the pure, functional
model in Coq. Figure 12 provides an overview of               Figure 12: Overview of the
the entire process. We will only very briefly cover off    verification pipeline: from source
on extraction and lifetime repairing in this section,         code extraction to proof of
please refer to Section 3 for the full scope.              observational equivalence in Coq.

H.1     Extraction
Extraction lifts a user-selected region into a new function and replaces the selection with a call
at the original site. As detailed in Section 3.5, this step is powered by a Rust-Analyzer (RA)
backed engine that performs single-file incremental analysis. It resolves the selection’s AST and
symbol information in memory and synthesises a function skeleton together with the call-site
edit.
The extraction result is returned as a deterministic set of edits (a patch) and a machine-readable
summary for downstream stages. By design, the extractor does not attempt to finalise lifetimes
or advanced ownership modes—that responsibility is delegated to REM’s repair phase. This
separation keeps extraction millisecond fast and predictable, and completely independent of
crate size, while ensuring a stable interface for the later verification.

H.2     REM
REM performs post-extraction semantic repair to attempt to bring the extracted code back
into alignment with Rust’s ownership and lifetime rules. Whilst much of the original REM
toolchain’s efforts have been integrated into the extraction process, we still rely heavily on the
most complex part of REM’s analysis: the Lifetime reification. We introduce, propagate, and

                                                 64
constrain lifetime parameters to satisfy the borrow checker, generalising where necessary.
As detailed earlier, REM treats the compiler as an oracle: it iterates repairs until the program
compiles, and then attempts to apply lifetime elision to produce a human-readable signature
(where practical) and a function body that aligns as closely as possible to idiomatic Rust. The
output of REM is thus the repaired program P ′ , which is then passed onto CHARON to begin
the process of discharging equivalence obligations.

H.3     CHARON
The first (new) stage of our verification pipeline is translation from Rust into a lower-level,
verification-friendly form. This role is performed by CHARON, a Rust to LLBC (Low-Level
Borrow Calculus) translator. CHARON accepts Rust source code (or more precisely, its compiler
intermediate representation MIR) 18 . CHARON’s main task is to extract complex semantic
information from rustc and produce a machine readable output containing said information.
Up until this point, we have been working with / reasoning about a single file. Whilst this kept
extraction lightning fast, CHARON’s support for single file conversion is limited at best19 .
Thus at this stage, we construct two “virtual” crates within the users temporary directory
( std::env::temp() ). The advantages of this approach are:
   1. Any changes the user makes to their source code whilst we are performing the later stages
       of analysis will not get passed down to us (potentially introducing half written words or
       other bugs that would fail immediately)
   2. We do not require a file lock on the users code, so they can continue work
   3. We can safely abstract away the creation / deletion of the virtual crates, and have them
       live for only so long as the equivalence engine runs for, using a custom implementation of
       the Drop trait.
   4. We can limit the data passing over the JSON-RPC bridge to just the original and extracted
       code for the file the user is working in.
CHARON then performs several non-trivial transformations:
    • Structured control flow. MIR is a control-flow graph with arbitrary goto s; CHARON
       reconstructs this into structured if , match , and loop constructs, or preserves the raw
       form with the --ullbc option.
    • Trait and type resolution.                Explicitly records how trait bounds are proven, nor-
       malises default methods, and can transform associated types into explicit parameters
       (--remove-associated-types).
    • Lifetime handling. Hides the distinction between early- and late-bound variables and
       makes implied bounds explicit, simplifying reasoning about generic functions.
    • Closures and vtables. Represented as ordinary structs implementing the relevant Fn*
       traits, making them accessible to later verification steps.
    • Noise reduction.            Options such as --hide-marker-traits remove built-in traits
       ( Sized , Send , etc.) that would otherwise clutter the output.
  18
     Even more precisely, the tool itself accepts Rust code, but its initial steps rely on a complex interaction with
rustc to acquire the MIR
  19
     CHARON can convert just a single file, but it relies on rustc to do so, and as such the single file must be
self contained, which we cannot guarantee



                                                         65
    The result is a cleaned, semantically faithful program in LLBC form. Unlike raw MIR, which is
    compiler-oriented, LLBC is designed for verification: ownership and borrowing are represented
    directly, trait resolution is explicit, and control flow is structured. A sample program and small
    portion of its MIR are shown below. However, the output of CHARON is not designed for
    human readability, and even the tiny program in Figure 13 produces over 140,000 characters
    of LLBC. This (very verbose) explicitness is what enables the subsequent translation into pure
    functional code for verification.

1   fn main() {                                         1   bb2: {
2       let v = vec![1, 2, 3];                          2       _9 = &_1;
3       let x = &v[0];                                  3       _8 = <Vec<i32> as Index<usize>>::
4       println!("{}", x);                              4           index(move _9, const 0_usize);
5   }                                                   5   }
                                                        6
                                                        7   bb3: {
              Listing 30: Rust source                   8       _7 = copy _8;
                                                        9       _16 = &_7;
                                                      10        _15 = core::fmt::rt::Argument::<’_>::
                                                      11            new_display::<&i32>(copy _16);
                                                      12    }


                                                               Listing 31: Excerpt of MIR (rustc)

       Figure 13: Illustration of CHARON’s role. While only Rust and MIR are shown here,
    CHARON translates the MIR into LLBC. The LLBC is only designed to be machine readable,
                                     and as such is ommitted


    H.4    AENEAS
    With the program translated into LLBC by CHARON, the next stage of the pipeline is han-
    dled by AENEAS. AENEAS takes the borrow- and lifetime–explicit LLBC and translates
    it into a purely functional form, stripping away low-level memory operations while preserving
    the program’s semantics. This functionalisation step is what makes the program suitable for
    downstream reasoning in Coq: instead of reasoning about references and loans, we can reason
    about values and functions. Currently AENEAS supports translation into Coq, Lean, HOL4,
    and F*.
    In practice, AENEAS acts as the bridge between compiler-level detail and proof-level abstrac-
    tion. CHARON ensures that all the complexities of lifetimes, loads, and trait resolution are
    made explicit; AENEAS then packages these into a form where correctness properties can be
    stated and proved without touching the borrow checker or the stack/heap. Within the context
    of our pipeline, this is the point where Rust code “stops being Rust” and becomes a functional
    program whose equivalence can be checked in Coq.

    H.5    Coq
    AENEAS translates the LLBC into a purely functional form, targeting Coq. The final stage
                                                                         ′ ), together with all
    of the pipeline then combines the two generated Coq files (Pcoq and Pcoq
    auxiliary information needed to automatically verify the equivalence between the original and
    refactored Rust programs. A key challenge at this stage is the verbosity of the generated Coq


                                                   66
code (as illustrated in Listing 10b), which led us to implement a custom Coq tokeniser and
parser tailored to the format emitted by AENEAS.
In parallel with these translations, the equivalence prover’s main task is to produce the
EquivCheck.v file. This module instantiates both the original and refactored definitions and
generates an equivalence theorem, which is a Coq encoding of the obligation(s) described in
Section 4.4. In practice, this means the Coq project is set up so that it automatically checks
that the two versions produce the same results for all inputs. We defer the details of the proof
obligations to that section; the key point here is that the generated Coq project is self-contained:
once compiled, the equivalence is verified without further user intervention.

What is Coq?

Coq is an interactive theorem prover and proof assistant built on a dependently typed functional
language. It allows developers to define mathematical objects, programs, and logical proposi-
tions, and to construct machine-checked proofs about them. Every proof is validated by Coq’s
small, trusted kernel, giving very high assurance of correctness. Coq has a long history of use in
large-scale verification projects—such as CompCert (a verified C compiler) and formally verified
operating systems—making it a natural fit for reasoning about the safety and correctness of
Rust programs.

Why Coq?

Coq was selected over alternatives such as HOL4, Lean, or F* for three main reasons:
• Mature ecosystem Decades of development have produced robust tooling, extensive li-
  braries, and a stable kernel.
• Direct integration AENEAS already targets Coq, whereas HOL4 and Lean would require
  substantial new backends for compatibility.
• Automation Coq’s tactic language and SMT integrations allow many routine proofs— such
  as equivalence checks—to be discharged automatically.
Lean and HOL4 both provide highly expressive grammars, but at the cost of significant engineer-
ing effort to integrate with AENEAS 20 . Whilst F* would require the least additional infrastruc-
ture, the platform is not that mature mature and would also duplicate existing functionality.
Coq therefore offers the best combination of maturity, automation, and direct compatibility
with our pipeline.




 20
      They both require even more additional supporting architecture on top of the current pipeline


                                                       67
     I   Appendix 9:            EquivCheck.v Lemmas from the Extraction
         Evaluation

 1   (** EquivCheck.v Autogenerated by REM-verification **)
 2   Require Import Primitives.
 3   Import Primitives.
 4   Require Import Input.
 5   Require Import Out.
 6   Local Open Scope Primitives_scope.
 7
 8   Lemma foo_equiv_check :
 9       Input.foo = Out.foo.
10   Proof.
11       intros.
12       unfold Input.foo.
13       unfold Out.foo.
14       reflexivity.
15   Qed.


                 Listing 32: EqivCheck.v file from one of the simple verification cases


 1   (** EquivCheck.v Autogenerated by REM-verification **)
 2   Require Import Primitives.
 3   Import Primitives.
 4   Require Import BusinessLogic.
 5   Require Import BusinessLogicRefactored.
 6   Local Open Scope Primitives_scope.
 7
 8   Lemma example5_config_normalise_config_equiv_check : forall (raw :
         example5_config_RawConfig_t),
 9        BusinessLogic.example5_config_normalise_config raw = BusinessLogicRefactored.
         example5_config_normalise_config raw.
10   Proof.
11       intros raw.
12       unfold BusinessLogic.example5_config_normalise_config.
13       unfold BusinessLogicRefactored.example5_config_normalise_config.
14       reflexivity.
15   Qed.


                Listing 33: EqivCheck.v file from one of the complex verification cases



     References
      [1] Nicholas D. Matsakis and Felix S. Klock. The rust language. Ada Lett., 34(3):103–104,
         October 2014. ISSN 1094-3641. doi: 10.1145/2692956.2663188. URL https://doi.org/
         10.1145/2692956.2663188.

      [2] Sewen Thy, Andreea Costea, Kiran Gopinathan, and Ilya Sergey. Adventure of a lifetime:
         Extract method refactoring for rust. Proc. ACM Program. Lang., 7(OOPSLA2), October
         2023. doi: 10.1145/3622821. URL https://doi.org/10.1145/3622821.

                                                  68
 [3] Sewen Thy. Borrowing without sorrowing: Implementing extract method refactoring for
    rust. 2023. URL https://verse-lab.github.io/papers/Sewen-Thy-Capstone.pdf.

 [4] Yaroslav Golubev, Zarina Kurbatova, Eman Abdullah AlOmar, Timofey Bryksin, and
    Mohamed Wiem Mkaouer. One thousand and one stories: a large-scale survey of soft-
    ware refactoring.   In Proceedings of the 29th ACM Joint Meeting on European Soft-
    ware Engineering Conference and Symposium on the Foundations of Software Engineer-
    ing, ESEC/FSE 2021, pages 1303–1313, New York, NY, USA, 2021. Association for
    Computing Machinery.      ISBN 9781450385626.      doi: 10.1145/3468264.3473924.     URL
    https://doi.org/10.1145/3468264.3473924.

 [5] Garming Sam, Nick Cameron, and Alex Potanin. Automated refactoring of rust programs.
    In Proceedings of the Australasian Computer Science Week Multiconference, ACSW ’17,
    New York, NY, USA, 2017. Association for Computing Machinery. ISBN 9781450347686.
    doi: 10.1145/3014812.3014826. URL https://doi.org/10.1145/3014812.3014826.

 [6] Alejandra Garrido and Jose Meseguer. Formal specification and verification of java refac-
    torings. In 2006 Sixth IEEE International Workshop on Source Code Analysis and Manip-
    ulation, pages 165–174, 2006. doi: 10.1109/SCAM.2006.16.

 [7] RustLang Team. Rust by example. https://doc.rust-lang.org/rust-by-example, n.d.
    Accessed: 2025-04-15.

 [8] Twain Byrnes, Yoshiki Takashima, and Limin Jia. Automatically enforcing rust trait
    properties. In Verification, Model Checking, and Abstract Interpretation: 25th Interna-
    tional Conference, VMCAI 2024, London, United Kingdom, January 15-16, 2024, Pro-
    ceedings, Part II, pages 210–223, Berlin, Heidelberg, 2024. Springer-Verlag. ISBN 978-
    3-031-50520-1. doi: 10.1007/978-3-031-50521-8 10. URL https://doi.org/10.1007/
    978-3-031-50521-8_10.

 [9] Alex Potanin, James Noble, Dave Clarke, and Robert Biddle. Generic ownership for generic
    java. In Proceedings of the ACM International Conference on Object-Oriented Program-
    ming, Systems, Languages, and Applications (OOPSLA 2006), pages 311–324. ACM, 2006.
    doi: 10.1145/1167473.1167500.

[10] Yoav Zibin, Alex Potanin, Paley Li, Mahmood Ali, and Michael D. Ernst. Ownership
    and immutability in generic java. In Proceedings of the ACM International Conference on
    Object-Oriented Programming, Systems, Languages, and Applications (OOPSLA 2010),
    pages 598–617. ACM, 2010. doi: 10.1145/1869459.1869509.

[11] Yoav Zibin, Alex Potanin, Mahmood Ali, Shay Artzi, Adam Kieżun, and Michael D.
    Ernst. Object and reference immutability using java generics. In 6th Joint Meeting of
    the European Software Engineering Conference and the ACM SIGSOFT Symposium on
    the Foundations of Software Engineering (ESEC/FSE 2007), pages 75–84. ACM, 2007.
    doi: 10.1145/1287624.1287637. Distinguished Paper Award.




                                             69
[12] Wikipedia contributors. Rust (programming language). https://en.wikipedia.org/
    wiki/Rust_(programming_language), 2025. Accessed: 2025-11-15.

[13] Wenzhang Yang, Linhai Song, and Yinxing Xue.          Rust-lancet: Automated Ownership-
    Rule-Violation Fixing with Behavior Preservation . In 2024 IEEE/ACM 46th International
    Conference on Software Engineering (ICSE), pages 1034–1046, Los Alamitos, CA, USA,
    April 2024. IEEE Computer Society. URL https://doi.ieeecomputersociety.org/.

[14] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. Rustbelt: se-
    curing the foundations of the rust programming language. Proc. ACM Program. Lang.,
    2(POPL), December 2017.       doi: 10.1145/3158154.      URL https://doi.org/10.1145/
    3158154.

[15] Son Ho and Jonathan Protzenko. Aeneas: Rust verification by functional translation.
    Proc. ACM Program. Lang., 6(ICFP), August 2022. doi: 10.1145/3547647. URL https:
    //doi.org/10.1145/3547647.

[16] Son Ho, Aymeric Fromherz, and Jonathan Protzenko. Sound borrow-checking for rust via
    symbolic semantics. Proc. ACM Program. Lang., 8(ICFP), August 2024. doi: 10.1145/
    3674640. URL https://doi.org/10.1145/3674640.

[17] Julian Mackay, Hannes Mehnert, Alex Potanin, Lindsay Groves, and Nicholas Cameron.
    Encoding featherweight java with assignment and immutability using the coq proof as-
    sistant. In Workshop on Formal Techniques for Java-like Programs (FTfJP 2012), pages
    11–19. ACM, 2012. doi: 10.1145/2318202.2318205.

[18] Stef Gijsberts. Prusti in Practice, A case sttudy of using the Prusti auto-active program
    verifyer for Rust. PhD thesis, 03 2023.

[19] Vytautas Astrauskas, Aurel Bı́lý, Jonáš Fiala, Zachary Grannan, Peter Müller, Federico
    Poli, and Alexander Summers. The Prusti Project: Formal Verification for Rust, pages
    88–108. 05 2022. ISBN 978-3-031-06772-3. doi: 10.1007/978-3-031-06773-0 5.

[20] Lennard Gäher, Michael Sammler, Ralf Jung, Robbert Krebbers, and Derek Dreyer.
    Refinedrust: A type system for high-assurance verification of rust programs.          Pro-
    ceedings of the ACM on Programming Languages, 8:1115 – 1139, 2024. URL https:
    //api.semanticscholar.org/CorpusID:270398597.

[21] Alexa VanHattum, Daniel Schwartz-Narbonne, Nathan Chong, and Adrian Sampson.
    Verifying dynamic trait objects in rust.       2023.   URL https://www.amazon.science/
    publications/verifying-dynamic-trait-objects-in-rust.

[22] Isaac Oscar Gariano, Marco Servetto, Alex Potanin, and Hrshikesh Arora. Iteratively com-
    posing statically verified traits. Electronic Proceedings in Theoretical Computer Science,
    299:7, 2019. doi: 10.4204/EPTCS.299.7.

[23] Dorian Schiedt. Improving “extract function” in rust analyzer, Aug 2022. URL https:



                                              70
    //dorianlistens.com/2022/07/improving-extract-function-in-rust-analyzer/#:
    ~:text=According%20to%20the%20official%20Rust,Analyzer%20website.

[24] Raul Marticorena, Carlos López, Yania Crespo, and F. Javier Pérez. Refactoring generics in
    java: A case study on extract method. pages 212–221, 2010. doi: 10.1109/CSMR.2010.38.

[25] Yang Zhang, Zhaoyang Xie, Yanxia Yue, and Lin Qi. Automatic refactoring approach for
    asynchronous mechanisms with completablefuture. Applied Sciences, 14(19), 2024. ISSN
    2076-3417. doi: 10.3390/app14198866. URL https://www.mdpi.com/2076-3417/14/19/
    8866.

[26] Yu Lin, Semih Okur, and Danny Dig. Study and refactoring of android asynchronous
    programming (t). pages 224–235, 2015. doi: 10.1109/ASE.2015.50.

[27] Huiqing Li, Simon Thompson, and Claus Reinke. The haskell refactorer, hare, and its api.
    Electr. Notes Theor. Comput. Sci., 141:29–34, 12 2005. doi: 10.1016/j.entcs.2005.02.053.

[28] URL https://pybowler.io/.

[29] David Young, Ziyi Yang, Ilya Sergey, and Alex Potanin. Higher-order specifications for
    deductive synthesis of programs with pointers. In 38th European Conference on Object-
    Oriented Programming (ECOOP 2024), volume 313 of LIPIcs, pages 45:1–45:26. Schloss
    Dagstuhl - Leibniz-Zentrum für Informatik, 2024. doi: 10.4230/LIPIcs.ECOOP.2024.45.

[30] Evan Li.    Github ranking:     Top 100 stars in rust.       https://evanli.github.io/
    GithubRanking/Top100/Rust.html, 11 2025.

[31] Aditya Jain, Ramta Bansal, Avnish Kumar, and K. D. Singh. A comparative study of
    visual and auditory reaction times on the basis of gender and physical activity levels of
    medical first year students. International Journal of Applied & Basic Medical Research, 5
    (2):124–127, May–Aug 2015. ISSN 2229-516X. doi: 10.4103/2229-516X.157168.

[32] Tobias Runge, Tabea Bordis, Alex Potanin, Thomas Thüm, and Ina Schaefer. Flexible
    correct-by-construction programming. Logical Methods in Computer Science, 19(2):16:1–
    16:36, 2023. doi: 10.46298/lmcs-19(2:16)2023.




                                               71
