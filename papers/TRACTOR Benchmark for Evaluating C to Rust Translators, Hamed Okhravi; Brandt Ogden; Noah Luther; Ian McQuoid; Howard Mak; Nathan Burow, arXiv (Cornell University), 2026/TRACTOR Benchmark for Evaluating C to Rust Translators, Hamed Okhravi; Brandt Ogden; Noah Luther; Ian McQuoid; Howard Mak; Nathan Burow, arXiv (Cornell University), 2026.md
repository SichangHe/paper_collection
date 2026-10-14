                                                      Massachusetts Institute of Technology
                                                              Lincoln Laboratory




                                         TRACTOR Benchmark for Evaluating C to Rust Translators
arXiv:2609.25121v1 [cs.SE] 20 Sep 2026




                                                                 Hamed Okhravi
                                                                 Brandt Ogden
                                                                  Noah Luther
                                                                  Ian McQuoid
                                                                  Howard Mak
                                                                 Nathan Burow
  DISTRIBUTION STATEMENT A. Approved for public release.                 Distribution is
  unlimited.


  This material is based upon work supported by the Under Secretary of Defense
  for Research and Engineering under Air Force Contract No.        FA8702-15-D-0001 or
  FA8702-25-D-B002. Any opinions, findings, conclusions or recommendations expressed
  in this material are those of the author(s) and do not necessarily reflect the views of
  the Under Secretary of Defense for Research and Engineering.


  ©2026 Massachusetts Institute of Technology.


  Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS
  Part 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice, U.S.
  Government rights in this work are defined by DFARS 252.227-7013 or DFARS
  252.227-7014 as detailed above. Use of this work other than as specifically authorized
  by the U.S. Government may violate any copyrights that exist in this work.




Lexington                                                                  Massachusetts




                                            ii
This page intentionally left blank.




                iii
This page intentionally left blank.




                iv
                       TABLE OF CONTENTS

                                                   Page


1.   INTRODUCTION                                     1


2.   EVALUATION METRICS AND MEASUREMENT APPROACH      5
     2.1  Functional Correctness                      5
     2.2  Safety                                      8
     2.3  Idiomaticity                                9
     2.4  Performance                                23


3.   BENCHMARK BATTERIES AND MILESTONE PROJECTS      25
     3.1 Battery 01 Benchmark                        25
     3.2 Milestone Projects 00 and 01 Benchmarks     26
     3.3 Battery 02 Benchmark                        26
     3.4 Milestone Project 02 Benchmark              28
     3.5 Evaluation Infrastructure                   28


4.   CONCLUSION                                      31
     References                                      33




                                  v
This page intentionally left blank.




                vi
                                    1. INTRODUCTION

       Grace Hopper famously warned that “the most dangerous phrase in the language is: ’We’ve
always done it this way.’ ” Nowhere is this observation more relevant than in the construction of
critical software.
      For decades, many of the world’s most important software systems have been implemented
in memory-unsafe languages such as C and C++ [1]. These languages underpin operating systems,
communication stacks, cryptographic libraries, embedded controllers, and a wide range of safety-
and mission-critical applications. Their performance characteristics and low-level control made
them compelling historical choices. Yet their weaknesses are equally well understood [2]. Undefined
behavior, memory corruption, buffer overflows, and use-after-free errors remain among the most
common and most damaging sources of software vulnerabilities [3]. Despite this persistent risk, vast
legacy codebases, performance sensitivities, certification constraints, and ecosystem dependencies
have rendered wholesale rewrites largely impractical. As a result, many high-risk systems remain
anchored to decades-old implementation decisions.
       The urgency of addressing memory safety is not new [4]. For more than twenty years, re-
searchers, security practitioners, and industry leaders have repeatedly identified memory-unsafe
languages as a systemic root cause of exploitable vulnerabilities [5]. Academic studies, breach
analyses, and exploit campaigns have consistently traced failures back to memory corruption and
undefined behavior [6]. What is unusual about the present moment is not recognition of the prob-
lem, but the breadth of agreement about its implications. Technical agencies such as the NSA and
CISA [7], national policy bodies [8], and even consumer advocacy organizations [9] have converged
on a similar conclusion: incremental mitigation is insufficient, and structural change at the language
level is required [10].
      The software ecosystem has also explored large-scale language modernization before. Efforts
such as IBM’s Cobol-to-Java modernization work more than two decades ago [11] demonstrated
the feasibility of large-scale translation, but they operated in a very different technical and policy
environment. Those efforts focused primarily on platform modernization and maintainability rather
than on eliminating systemic security vulnerabilities at their root.
      Indeed, over the intervening decades, the community invested heavily in attempting to com-
pensate for memory-unsafe languages without abandoning them. Compiler-based mitigations such
as stack canaries, address space layout randomization, and control-flow integrity [12–14] were intro-
duced to detect or constrain exploitation. Dynamic defenses such as sandboxing and runtime in-
strumentation were deployed to limit damage [15]. Static analysis tools, verification techniques [16],
hardened allocators [17], and secure coding standards such as MISRA and CERT were developed
to reduce such vulnerabilities [18, 19]. Each of these advances improved resilience in specific con-
texts. Yet none eliminated the underlying classes of vulnerabilities. Memory corruption continues
to appear across browsers, operating systems, network services, and embedded platforms [20]. In
this sense, the shift toward memory-safe languages is not a first attempt at remediation, but the
culmination of repeated partial solutions that have not fundamentally resolved the problem [21].




                                                  1
      In recent years, however, a qualitatively different path has emerged. Advances in safe program-
ming languages, language tooling, and artificial intelligence have opened the possibility of automated
or semi-automated translation of legacy code into safer languages with strong correctness and se-
curity guarantees, most notably Rust [22–29]. Rather than rewriting systems from scratch, these
approaches aim to mechanically transform existing implementations while preserving behavior and
strengthening safety properties. This line of work draws on static and dynamic program analysis,
formal methods, program synthesis, and increasingly large language models. Together, these tech-
niques offer a path to scale beyond what manual refactoring or isolated rewrites can realistically
achieve.
      Rust [30] occupies a uniquely attractive niche within this modernization landscape. Un-
like managed languages that depend on garbage collection, Rust enforces memory safety through
compile-time ownership and borrowing rules without imposing runtime GC overhead, preserving
deterministic performance characteristics required in systems and real-time domains. It interop-
erates directly with C and C++ through stable foreign function interfaces, enabling incremental
migration rather than all-or-nothing rewrites. It delivers performance comparable to C and C++,
in part because it leverages the same LLVM compiler infrastructure and provides explicit control
over memory layout and representation. These properties make Rust not merely a safe language
for new development, but a technically viable and strategically compelling target for large-scale
automated translation.
      This broader shift has increasingly been reflected in national policy. In 2024, the White House
Office of the National Cyber Director issued Back to the Building Blocks: A Path Toward Secure and
Measurable Software, explicitly encouraging the adoption of memory-safe languages and reduction
of reliance on inherently memory-unsafe ones [8]. In 2025, the NSA and CISA jointly released
Memory Safe Languages: Reducing Vulnerabilities in Modern Software Development, emphasizing
the role of language-level safety in improving software resilience and outlining practical pathways for
adoption [7]. These statements build upon years of technical consensus and frame memory safety
as a national security priority rather than merely a best practice [21].
      Against this backdrop, the DARPA TRACTOR program [31] represents a concerted research
effort to fundamentally change how legacy, memory-unsafe software is modernized. TRACTOR
seeks to develop scalable, automated techniques for translating large C codebases into memory-
safe Rust. Although fully automated translation is an aspirational goal, experience suggests that
human judgment remains essential. The program therefore frames modernization as a repeatable,
measurable, and security-driven process that incorporates human oversight when necessary to ensure
correctness and security. Its goals extend beyond functional correctness to include strengthened
safety guarantees, competitive performance, and code quality suitable for long-term maintenance
and evolution. In doing so, TRACTOR directly addresses the longstanding technical challenge—and
growing policy imperative—of reducing systemic dependence on memory-unsafe software.
     MIT Lincoln Laboratory serves as the independent test and evaluation (T&E) organization for
the TRACTOR program and is responsible for developing the program’s evaluation methodology,
benchmarks, metrics, and supporting infrastructure. A central component of this effort is the




                                                  2
development and periodic release of standardized benchmark batteries for evaluating C-to-Rust
translation tools.
      Each battery consists of tens of C test cases curated or synthesized by MIT LL to systemati-
cally exercise specific C language features and translation challenges. The batteries are designed to
increase in complexity over time, with each release introducing additional features and interactions
that translation tools must address. This structure provides a common and progressively challeng-
ing benchmark for assessing C-to-Rust translators across functional correctness, safety, idiomaticity,
and performance.
      The program also includes milestone projects that are substantially larger and more complex
than the individual test cases. These projects approximate realistic legacy software components,
stressing translation systems in ways smaller examples cannot.
      This report describes the TRACTOR benchmark for C-to-Rust translation, developed by MIT
Lincoln Laboratory, and covers both the test batteries and milestone projects. It will be updated
as new batteries and milestone projects are released. As of September 2026, two batteries (Battery
01 and Battery 02) and three milestone projects (Project 00, Project 01, and Project 02) have been
released.
     All TRACTOR test batteries and milestone projects are publicly available at: https://
github.com/DARPA-TRACTOR-Program/PUBLIC-Test-Corpus.
     This report also gives an overview of the infrastructure and metrics used to evaluate translators
against the benchmark. All associated infrastructure scripts, metrics, and automated evaluation
containers are publicly released at:
https://github.com/DARPA-TRACTOR-Program/PUBLIC-aws-translate.
      This report does not include evaluation results; it is intended as a reference for C-to-Rust
translator developers. Evaluation results for TRACTOR performers are available at: https://
www.ll.mit.edu/tractor.




                                                  3
This page intentionally left blank.




                4
      2. EVALUATION METRICS AND MEASUREMENT APPROACH

     The metrics described here are intended to capture the key dimensions relevant to evaluating
a C-to-Rust translation. These dimensions include functional correctness, safety, performance, and
idiomaticity, listed in approximate order of importance.


2.1 FUNCTIONAL CORRECTNESS
      A Rust translation is functionally correct if it produces the same observable input/output
behavior as the original C program on all test vectors: matching standard output, standard error,
return code, and—for library targets—the expected output state exposed through the C ABI. This
is an empirical, test-based notion of correctness, not a formal one; we make no claim of semantic
equivalence in the logical or proof-theoretic sense, and correctness is bounded by the coverage of
the test suite.
       Undefined behavior (UB) in C complicates this definition. The C standard permits a compiler
to do anything when UB is encountered, so there is no single “correct” output to match. Nevertheless,
for the purposes of this evaluation we treat correctness as behavioral fidelity to the compiled C binary:
if the C code, as compiled by clang/LLVM on the evaluation platform, deterministically produces
a specific output for a given input—even when that output arises from UB—we expect the Rust
translation to produce that same output. In other words, C means what LLVM does: the reference
behavior is not the abstract C standard but the concrete execution produced by the LLVM toolchain
on the test system. A translation that silently changes the observable output is considered incorrect
for the purposes of this metric; conversely, a translation that preserves the UB-derived output is
considered correct. Test vectors that exercise known UB are currently excluded from automated
scoring (has_ub flag), and their handling is assessed separately and informally; improved automated
characterization of UB is planned for future evaluation cycles.
      To evaluate functional correctness, we curated test cases—C programs/projects collectively
referred to as our test corpus—in two ways. Our first method was isolating smaller parts of larger
organic projects to evaluate translators on a real-world C code. The second was generating (either
by hand or with the help of a Large Language Model (LLM)) generated synthetic projects to test
certain features that could not be easily found or replicated in real-world programs. Test cases are
further divided between public and hidden, where public tests cases were released to performers
6 months before the evaluation, and hidden test cases were held back and the performers had no
advanced knowledge of.
       Another important distinction between test cases is the split between those which generate
executables vs. a shared library (.so file). Test cases meant to produce a shared library are marked
with _lib at the end of their name to signify this. The split is important because each lends itself
to a certain style of translation. Executable test cases allow for heavier optimizations, allowing
them to refactor function signatures and the structure of the project, with the only requirement
to maintain the input/output (I/O) behavior present in the original C executable. A library test
is slightly different as it requires the preservation of symbols and signatures present in the original
C library. This makes optimizations more difficult and requires the use of unsafe, but allows the




                                                   5
Rust library to be a drop-in replacement of the C library—an important property for a gradual
translation from C to Rust.
      To accompany each test case we generated (either by hand or with the help of a LLM) test
vectors that represent the I/O behavior that both the C and Rust projects must adhere to. This
necessitated the creation of a specialized JavaScript Object Notation (JSON) schema designed to
capture everything involved with a running executable or library. Table 1 outlines each field in
the schema, along with its purpose (is it used for executables, libraries, or both). stdout and
stderr allow for more permissive matching using regular expressions if specified (e.g., floating point
comparisons).


                                               TABLE 1

                                       Test vector schema

        Field               Description                                   Purpose
        argv                command-line arguments                        executable
        stdin               input provided to program                     executable/library
        env                 environment variables passed to program       executable/library
        stdout              expected output from program                  executable/library
        stderr              expected output to standard error             executable/library
        rc                  expected return code                          executable
        lib_state_in        provided input state (see Cando)              library
        lib_state_out       expected output state (see Cando)             library
        has_ub              description of undefined behavior             executable/library


     In addition to the simpler JSON format, we have a second expanded form of a test vector
meant to handle filesystem state equivalence. Our evaluation infrastructure allows both the new
and old formats, and is meant to evolve as the notion of ”equivalence“ expands as we introduce more
complicated features, particularly networking.
    It is a directory in the following form:
  <test vector name>/
     cando_vector.json
     setup
     resources/
     file_changes.tar.gz
      cando_vector.json is simply the exact JSON specification defined above. setup is an arbi-
trary script that can do any setup that is required for a test vector to run. It can do anything from




                                                   6
creating files/directories, repositories, or setting up network interfaces. Additionally, it can set a
working directory that the test vector will be run from. resources is a directory that holds test
resources that can be accessed from the setup script. file_changes.tar.gz is a tar archive that
contains the files that have been created, modified, or deleted during the run of that test vector.
This expanded definition of a test vector allows us to define equivalence between a C and Rust
program in a more robust way, that is able to evolve as the scope of translations do too.
      To facilitate automated function equivalence evaluation we developed two tools, Test Runner1
and Cando 2 . Test Runner facilitates the higher-level orchestration of Cando, manages filesystem
state equivalence, and handles reporting, while cando evaluates functional equivalence at the test
vector level utilizing the JSON test vector defined above.


      Cando For library tests, Cando uses the lib_state_in and lib_state_out fields of the
schema to represent the state to pass into, and expect out of the library, respectively. These are
used by the dedicated harness (or runner ) for each library test case that defines how their elements
are used. For example, they could be function arguments, return values, or anything else that is
used by the harness that could define equivalence. The harness specifies the shared library (a .so)
file—generated either by C or Rust—and a symbol (function) to call that should exhibit such I/O
behavior. For binary tests, there is a single harness that is used for all binary tests that uses the
same JSON specification. The current implementation skips any test vector marked with has_ub,
though better automatic characterization of UB will be a future improvement.


      Test Runner This is a Python project that is used both to ensure that the test vectors
we generate actually match the I/O behavior of the C test cases we produce (run with Continuous
Integration (CI) on every PR), and runs on Rust projects to check if they conform to the I/O
behavior of the original C (to the extent that the test vectors cover all possible program states).
The following gives a high level overview of what the Test Runner is responsible for:

      • Discover the C or Rust projects

      • Build those projects

      • Build the runners/harnesses needed to run them

      • Start Falco [32], a runtime security tool that we use to track file changes

      • Starting and managing test vector containers

      • Within those containers running the setup script, Cando, and using the file changes from
        Falco to evaluate filesystem state equivalence
  1
     Publicly released at https://github.com/DARPA-TRACTOR-Program/PUBLIC-Test-Corpus/tree/main/tools/
test_runner
   2
     Publicly released at https://github.com/DARPA-TRACTOR-Program/PUBLIC-Test-Corpus/tree/main/tools/
cando2




                                                    7
   • Handling any errors that may occur throughout the run, and report the results to the console
     and/or to a file as JUnit XML


2.2 SAFETY
      Safety is a complimentary goal to functionality in that neither is complete without the other.
While it is important for a C-to-Rust translation to be functionally equivalent to the original C
program, it is also important for that translation to add additional security guarantees that are
typical from a native Rust program. A primary goal for the TRACTOR program is to produce
maximally-safe Rust programs, and simply translating C into entirely unsafe Rust to evade the
borrow checker does not yield any additional safety benefits. We evaluate Rust translations for
safety in two ways, the use of the unsafe keyword, and undefined behavior (UB).


      Unsafety Usefully analyzing and quantifying the use of unsafe constructs within Rust code
is a subtle question. We capture the amount of unsafety semantically, or based on the operations
that actually require an unsafe context as opposed to simply being in an unsafe block. Our semantic
analysis3 instruments the Rust compiler to produce a report of these operations that include calls
to unsafe functions, use of inline assemble and mutable statics, raw pointer dereferences, and more.
       Even this instrumentation is unable to perfectly capture unsafety. While we can capture
the number of operations which require unsafety, we cannot determine whether that unsafety was
necessary to implement a particular feature. There are certain structures which require unsafe
contexts, including FFI boundaries and inline assembly. Library test case translations are required
to be ABI-compatible with the original C, which necessitates the inclusion of unsafety to expose the
required symbols. This is complicated by the fact that these exposed interfaces can be both imple-
mented directly as unsafe functions or as wrappers around safe internal functions. Determining the
difference between a “wrapper” that simply translates C types into native Rust types and calling an
internal safe function vs. also implementing program logic, is not something that can be automated
but instead requires higher-level reasoning. In at least one case, we observed a team produce a safe
internal function, and an unsafe wrapper which completely implemented that function and did not
actually call the internal safe function. On the other hand, binary tests have no such requirements
to use unsafety to maintain ABI-compatibility, but there still may remain reasonable or required
uses of usafe that we cannot differentiate between. In this report, we will report the raw unsafety
numbers alongside descriptions of the character of the unsafety present.


      Undefined Behavior Undefined behavior (UB) in C4 takes many forms, from classical
memory safety errors to more nuanced issues like the order arguments are evaluated in a function
call. For the purposes of this evaluation, we consider exploitable forms of undefined behavior, and
in particular focus on memory related issues. Removing vulnerabilities is a key motivation for
   3
     Publicly released at https://github.com/DARPA-TRACTOR-Program/PUBLIC-Test-Corpus/tree/main/tools/
rust_eval/unsafe_ops.
   4
     See the ISO WG14 report on UB [33].




                                                  8
translating to Rust, so here we assess how well translators are handling commonly exploited forms
of UB.
      To assess the handling of UB, we consider two key questions: whether a translator recognizes
the presence of UB and, if so, how it handles it. We break this question down into two parts.
The first is whether to preserve the application’s semantics, or alter them, e.g., by skipping inputs
that would result in a memory corruption, or by adding in manual error handling. The second key
decision is whether to translate to safe code or unsafe code. Safe code provides runtime checking
to detect UB — though some checks on arithmetic operations are only present when the code is
compiled in debug and not release mode5 . Unsafe code does not typically provide detection of UB.
      When evaluating whether semantics are preserved, the worst option is to silently change the
semantics of a function. While doing so would ideally be caught by correctness tests, it is nonetheless
dangerous. A better option is preserving the UB, which, while it decreases the safety gained from
translation, at least has the property of matching behavior. A competing approach is to add some
type of error handling – either explicitly in the code, likely resulting in an error message and a
crash, or relying on Rust’s built in error handling by translating to safe code. Overall, the best
way to handle UB is unclear, though changing the behavior of the application without developer
intervention seems to be the most dangerous option.


2.3 IDIOMATICITY
      Idiomaticity in Rust refers to the extent to which code follows established Rust conventions and
leverages the language’s intended abstractions, such as ownership and borrowing, pattern match-
ing, and standard library constructs. High idiomaticity is important because it improves readability,
maintainability, and safety, and it allows the code to better benefit from Rust’s compile-time guar-
antees and ecosystem tooling.
       While idiomaticity is inherently qualitative and can vary across reviewers, we ground our
evaluation rubric in established Rust practices and prior literature. The rubric combines automated
measures, including compiler diagnostics and Clippy [35] lints, with structured manual source-code
review. This combination is important because neither approach alone provides a sufficient measure
of idiomaticity. Manual code-quality assessments can exhibit reviewer inconsistency [36], while raw
linter counts and other static-analysis measures do not necessarily align with human judgments
of code quality. Weimer et al. [37], for example, report weak negative correlations between raw
linter warning counts and human rubric scores across four cohorts, and Dehghan et al. [38] similarly
caution against using Clippy counts alone to assess idiomaticity.
      We release the automated evaluation infrastructure alongside the benchmarks and document
the manual evaluation rubric in detail. Together, these resources provide benchmark users with a re-
producible framework for assessing the idiomaticity of C-to-Rust translations and for approximating
the evaluation methodology used by the TRACTOR Test & Evaluation team.
  5
      Tooling also exists to catch errors during intermediate stages of compilation, for instance Miri [34].




                                                            9
        2.3.1 Automated Idiomaticity Evaluation
     Our automated idiomaticity metrics6 use both rustc errors/warnings and clippy [35] lints.
rustc errors prevent a Rust program from compiling, which is already computed by our functional
equivalence metric, but the specific reasons for each error are captured here. Warnings represent
potential issues, but do not rise to the level of a failing compilation. These include unused variables,
dead code, and others, which are important for idiomatic Rust code.


Clippy clippy is a dedicated linter for Rust that provides additional best practices, code style,
and idiomatic usage recommendations beyond that of rustc. There are many different lints available
of which we utilize all in the 5 groups listed below. Each group has examples, though this list is far
from exhaustive.

      • Correctness: serious issues regarding correctness (either wrong or useless—no false positives)

          – approx_constant: floating point literals close to those already defined (e.g., 3.14)
          – infinite_iter: iteration that is guaranteed to be infinite

      • Suspicious: similar to correctness but possible weird construct is intentional

          – swap_ptr_to_ref: calls to core::mem::swap() with parameter derived from pointer
          – empty_line_after_outer_attr: empty lines between attribute (e.g., #[allow(dead_code)])
            and its corresponding function

      • Complexity: suggestions to simplify constructs (make them shorter and/or readable)

          – precedence: identifies operations where precedence is unclear (i.e., readability would be
            improved with parentheses)
          – unnecessary_cast: casts to same type, int/float literals to integer/float types

      • Perf: hints to increase performance

          – cmp_owned: conversion to owned value only for comparison
          – large_const_arrays: large const arrays that should be defined static

      • Style: subject style guides for idiomatic code

          – missing_safety_doc: missing doc comments for pub unsafe functions
          – needless_return: use of return at end of block
  6
     Publicly released at https://github.com/DARPA-TRACTOR-Program/PUBLIC-Test-Corpus/tree/main/tools/
rust_eval/static/static_evaluation.py.




                                                   10
1       // GATE-JUSTIFY(clippy::approx_constant): translation requires byte-identity to
2       // -O0 C with M_PI resolving to the glibc double macro (3.141592653589793); the
3       // literal is intentionally not ‘std::f32::consts::PI‘ because the C build
4       // evaluates angle math in f64. See q_math.rs module header.
5       #[allow(clippy::approx_constant)]
6       pub const M_PI: f32 = 3.14159265358979323846_f32;

       Listing 1: Acceptable use of #[allow(clippy::approx_constant)] to match C M_PI macro



    Clippy is not always right Clippy’s findings can be ignored by an in-source attribute both
    for a specific instance via #[allow(...)] and for many instances (e.g., across an entire file) via
    #![allow(...)]. The commonly accepted procedure for such overrides is to accompany each at-
    tribute with a justification comment explaining the reason for the violation similar to using safety
    comments when using unsafe.
          Listing 1 shows an example of an acceptable use of the #[allow(clippy::approx_constant)]
    attribute. However, we have also seen whole project allows that obscure clippy from reporting
    certain kinds of issues that would be relevant to the evaluation. Our current automated idiomaticity
    metric does not have a way to distinguish between these situations, and as such the actual number
    of relevant clippy lints can be ”gamed“ by overusing allow attributes. Our manual idiomaticity
    analysis (described below) takes this into account, and better automatic characterization of such
    instances will be improved in future evaluations.


    Cyclomatic Complexity Further, we use Lizard [39] to analyze the Cyclomatic Complexity
    (CCN) of both the original C and translator generated Rust. The CCN is a metric for understand-
    ing how many paths there are through each function. As such, it represents a reasonable proxy
    for complexity and readability. For example, a function with no control-flow structures (e.g., if
    statements, and for loops) have a CCN of 1. For each additional control-flow structure added to
    the function the, CCN increases by 1. We use the average CCN across all functions in the project
    under test.

         2.3.2 Manual Idiomaticity Evaluation Introduction
          As with any manual evaluation, idiomaticity assessment is subject to human error, ambiguity,
    and evaluator bias. To mitigate these effects, we recommend that evaluators first examine the
    original C code and establish a shared understanding of how a skilled Rust developer would translate
    it before independently assessing the resulting Rust translation. Evaluators should document the
    rationale for each score with specific observations from the source code and resolve significant scoring
    disagreements through discussion. This process is intended to promote consistent application of the
    rubric while preserving the expert judgment necessary to assess qualities that are difficult to capture
    through automated metrics alone.
          To introduce the notion of a manual evaluation, consider the figures below. Figure 1 shows
    three different hello world programs. Figure 1a, shows the C version that would be given to a




                                                      11
translator. Figure 1b shows the expected translation into Rust—what a skilled Rust developer
would do. This would get high scores across the board because it’s equally as readable as the
original C, uses Rust syntax (i.e., the println macro), and uses Rust types (i.e., a string literal) In
contrast, Figure 1c shows the output of C2Rust. This would score poorly in readability because it
turned what could’ve been accomplished in 3 lines into 11, doesn’t have use statements, and uses
unsafe, all of which obfuscate the intent of the program. Similarly, it would score poorly in both
syntax and types because it directly uses printf and the C types c_char and c_int, respectively.

     2.3.3 Manual Idiomaticity Evaluation Rubric
       We use a five-level Likert scale to provide sufficient differentiation among translations while
maintaining a consistent interpretation across idiomaticity dimensions. As shown in Table 2, levels
1, 3, and 5 serve as “anchor” levels corresponding to anti-idiomatic, developing, and idiomatic Rust,
respectively, while levels 2 (Novice) and 4 (Proficient) capture translations that fall between these
anchors. When a translation partially satisfies the descriptors of two adjacent anchor levels, the
corresponding intermediate level should be assigned rather than forcing the assessment to the nearest
anchor.
      Because idiomaticity requires human judgment, we define a structured rubric across six core
dimensions to make explicit what we mean by “idiomatic Rust” and to promote consistency across
evaluators. The five Likert levels intentionally use broad, common descriptors that can be applied
uniformly across all six dimensions, from ownership and data flow to project structure and API
design. The following sections refine these general descriptors for each dimension by identifying
characteristic anti-idioms, expected practices, and signals of highly idiomatic Rust. Together, these
dimensions provide a structured framework for assessing translation quality beyond what can be
captured through automated metrics alone.


D1 — Project Structure and Cargo Hygiene In dimension 1, we ask the question “Does the
translation look like a normal Rust project a maintainer would write?”.

  1. No hygiene, nothing pinned

        • No Cargo.toml, cargo fmt--check fails, clippy::correctness/clippy::suspicious
          fire
        • Monolithic file structure with no delineated boundaries
        • Unused dependencies present
        • No tests or trivial tests
        • Every item pub [40]

  2. Ad hoc

        • Builds but layout is ad hoc
        • Formatting inconsistent




                                                  12
     1   #include <stdio.h>
                                                        1    fn main() {
     2      int main() {
                                                        2       println!("Hello␣World");
     3      printf("Hello␣World\n");
                                                        3    }
     4   }

                     (a) Hello world in C                             (b) Hello world in Rust


1    #![allow(dead_code, mutable_transmutes, non_camel_case_types,
2    non_snake_case, non_upper_case_globals, unused_assignments, unused_mut)]
3    extern "C" {
4       fn printf(_: *const libc::c_char, _: ...) -> libc::c_int;
5    }
6    unsafe fn main_0() -> libc::c_int {
7       printf(b"Hello␣World\n\0" as *const u8 as *const libc::c_char);
8       return 0;
9    }
10   pub fn main() {
11      unsafe { ::std::process::exit(main_0() as i32) }
12   }

                                            (c) Hello world from C2Rust

                          Figure 1. Hello world examples of C-to-Rust translations




                                                   TABLE 2

                                       Idiomaticity Likert Scale

Level       Label                Character
  1         Anti-idiomatic       Multiple documented Rust anti-idioms in this dimension. Would be
                                 out-right rejected in code review.
     2      Novice               Common Rust idioms attempted but misapplied at a structural level.
                                 A reviewer would ask for substantial rework rather than touch-ups.
     3      Developing           Correct application of the common Rust idioms. Occasional lapses
                                 that a code review would catch.
     4      Proficient           Fluent, consistent Rust with small, but not meaningful, lapses. Any
                                 deviations are justified in code or docs.
     5      Idiomatic            Could serve as a teaching exemplar. Reader learns the Rust idioms
                                 by reading the code.




                                                        13
       • Clippy warnings unaddressed
       • Tests exist but are all in main.rs or the top of a single file
       • Some todo! / dbg! in shipped code

  3. Standard layout

       • Standard cargo layout (src/lib.rs and/or src/main.rs, tests/ for integration, #[cfg(test)]
         mod tests for unit)
       • Cargo.toml has name and version
       • cargo fmt --check and cargo clippy -D warnings clean at the course lint level
       • README.md present with build/run instructions

  4. Deliberate structure

       • Lib + bin split where both apply (logic in lib.rs, thin main.rs)
       • [dev-dependencies] correctly separated
       • No unused deps (cargo machete and cargo udeps clean [41])
       • Module style (mod.rs vs foo.rs + foo/) consistent
       • pub(crate) / pub(super) narrow visibility
       • No residual dbg! / todo! / unimplemented! in shipped code
       • Cargo.lock handled per official guidance (included for bins, not for libs) integration tests
         use fixtures rather than duplicating setup [42]

  5. Template-quality

       • [features] used purposefully with an explicit default and dep: syntax for optional
         deps
       • Project layout and tooling could serve as a template for other Rust projects within the
         domain


D1 — Project Structure Anti-idioms Patterns in this category are signals of a level-1 or
level-2 translation

   • todo!() / unimplemented!() / dbg!() in shipped code [40]

   • Every item pub [40]

   • Unused dependencies




                                                14
D1 — Project Structure Idiomatic Signals Patterns in this category are signals of a level-4
or level-5 translation

   • Modules mirror the domain, not the file listing

   • pub(crate) and pub(super) used to narrow visibility

   • Unit tests live next to the code they test

   • integration tests are their own crate under tests/.

   • [features] used to gate optional deps, with a documented default


D2 — Ownership and Data Flow In dimension 2, we ask the question “Does the code work
with ownership rather than around it?”

  1. Fighting the borrow checker

        • Pervasive .clone() to appease the borrow checker [43]
        • String / Vec<T> / &Vec<T> / &String parameters where &str / &[T] would work
        • Arc<Mutex<..>> or RefCell reached for on first sign of sharing [44]
        • let mut on every binding
        • Explicit ’a on every reference
        • Occasional unsafe used to escape lifetime issues

  2. Cloning less, but still reflexively

        • Some cloning is justified but reflexive clones remain
        • Some &Vec<T> / &String in signatures
        • Interior-mutability primitives introduced without a stated invariant
        • Unnecessary mut scattered but not universal

  3. Borrows preferred, lifetimes parsimonious

        • Borrows preferred over clones
        • Parameter types use &str and &[T] idiomatically
        • Interior mutability appears only where justified with a comment
        • Lifetime annotations parsimonious
        • Occasional lapse (e.g. one .clone() where a borrow would have worked)

  4. Ownership expresses intent

        • Ownership expresses intent: move-by-value builders, Cow<’_, str> where the data flow
          is mixed borrowed/owned




                                                  15
        • No defensive cloning
        • Interior mutability is a documented deliberate choice
        • Lifetime bounds precise and elided where the compiler allows

  5. Ownership restructured to fit the problem

        • Ownership restructured to fit the problem rather than reaching for Arc<Mutex<..>>
          first [45]
        • Shared state minimised architecturally


D2 — Ownership Anti-idioms

   • Defensive .clone() to appease borrowck [40, 43]

        – Note that the anti-idiom is pervasive / reflexive cloning, not any clone

   • let mut on values never mutated [40]

   • Arc<Mutex<..» / RefCell as first reach for shared state [40, 44]

   • &Vec<T> or &String in parameter position

   • Explicit lifetimes where elision applies


D2 — Ownership Idiomatic Signals

   • Signatures use &str, &[T], and impl AsRef<...> where appropriate

   • Move-by-value builders (self not &mut self) [46]

   • Cow<’_, str> at API boundaries with mixed ownership

   • Interior mutability restricted to modules that document the invariant


D3 — Error Handling and Unsafe In dimension 3, we ask the question “Does the code fail
well and treat unsafe with the respect it deserves?”

  1. Panics and undocumented unsafe

        • .unwrap() / .expect() / panic! in normal execution paths [40, 47]
        • Magic sentinels (-1, usize::MAX) instead of Option / Result
        • Errors swallowed via .ok() or let _ = ...
        • unsafe present without // SAFETY: comments or beyond clear FFI need [48]




                                                16
       • Raw pointers used where references would work [49]
  2. Stringly-typed errors, unexplained unsafe
       • Result<_, String> in signatures [46]
       • Some ? propagation but mixed with .unwrap() in the same function
       • Unsafe blocks have brief comments but do not state the invariant being upheld
       • Interior-unsafe (unsafe hidden in a safe function) without a documented boundary [44]
  3. Propagation with typed errors, unsafe justified
       • ? used throughout for propagation
       • Typed error enum or thiserror in library code
       • .expect("...") only where an invariant holds and the message states it (the panic!()
         unreachable!() senses in Gerat’s Three Kinds of Unwrap taxonomy [47])
       • No .unwrap() outside #[cfg(test)]
       • unsafe blocks scoped narrowly and preceded by a // SAFETY: comment
  4. Errors compose, unsafe abstracted safely
       • Errors compose (From impls for conversion)
       • Diagnostic messages carry enough context to debug from a log line
       • unreachable!() reserved for truly-unreachable branches with prose justification
       • unsafe minimised and abstracted behind a safe API with invariants documented in the
         style of std
       • # Errors / # Panics doc sections cover every fallible / panicking public function
  5. Failure modes self-evident, unsafe audit-grade
       • Unsafe either absent or forensically documented such that preconditions, postconditions,
         and the safe-API boundary stated at the level of an external audit [48]
       • Error types educate the reader
       • The taxonomy of failure modes is self-evident from the public API


D3 — Error Handling and Unsafe Anti-idioms

  • .unwrap() / .expect() in production paths [40, 47]
  • Result<_, String> in library signatures [46]
  • Magic sentinels instead of Option / Result [40]
  • unsafe without // SAFETY: [48]
  • Interior-unsafe with no marked boundary [44]
  • Raw pointers where references work [49]




                                              17
D3 — Error Handling and Unsafe Idiomatic Signals

   • ? chains with a project-wide error enum

   • // SAFETY: blocks that reference specific documented invariants

   • # Errors and # Panics sections on every public fallible/panicking fn

   • Custom error types implementing std::error::Error (thiserror is fine)

     Gate rule: Any clippy::correctness or clippy::suspicious finding, or any rapx UB-
adjacent finding, gates D3 to ≤ 2 (or 1 for UB) until resolved.


D4 — Types and Abstractions In dimension 4, we ask the question “Does the type system
carry the invariants, and are the abstractions earned?”

  1. The type system is invisible

       • bool and Option<bool> parameters where a purpose-built enum would read better
       • Magic numbers
       • Missing Debug / Clone on public types
       • Ad-hoc new_from_x / to_y methods duplicating what From / Into would give
       • Stringly-typed APIs (&str where an enum or newtype belongs)
       • C-style typedefs / integer flags where an enum belongs [40]

  2. Types attempted but not enforced

       • Some enums replace booleans
       • Some From impls present but manual conversion methods still dominate
       • Newtypes attempted but their invariants are not enforced by construction
       • Generics used defensively (“in case I need it later”)

  3. Types carry meaning

       • Enums replace flag booleans
       • Common derives present where they make sense
       • From and Into for cheap conversions [46]
       • Newtypes wrap values that carry useful invariants
       • Generics used only where actually generic

  4. Misuse tends toward a compile error




                                                18
        • Types encode invariants such that misuse is a compile error (typestate / phantom types
          where warranted)
        • TryFrom for fallible conversions
        • Abstractions justified by ≥ 2 uses with no premature generics, no dyn Trait for a single-
          implementor trait, no builder pattern on a two-field struct [45]
        • bitflags for flag sets

  5. Type-driven design is the point

        • The API is essentially incapable of being misused
        • Generics are elegant and their bounds are minimal [50]
        • A reader learns the domain by reading the types


D4 — Types and Abstractions Anti-idioms

   • Over-parameterised builders (FileBuilder<T: AsRef&str>, ’a>) [40]

   • Box<dyn Iterator> where impl Iterator fits [40]

   • Single-implementor traits introduced "just in case" [40]

   • Stringly-typed APIs [40]

   • Magic numbers, bool parameters [46]

   • Unsound generic bounds on unsafe wrappers [50]


D4 — Types and Abstractions Idiomatic Signals

   • Newtypes at construction time enforce the invariant the type name claims [46]

   • From / Into (or TryFrom for fallible) rather than named conversion methods

   • Trait bounds are tight and associated types are purposeful

   • No dyn Trait unless dispatch actually varies


D5 — Expression and Control Flow In dimension 5, we ask the question “Does the code read
the way experienced Rust reads?”

  1. C control flow in Rust

        • for i in 0..v.len() indexed loops with v[i] inside [40, 51]
        • Imperative accumulation where .map().sum() or .collect() would fit




                                                19
     • Nested match / if let pyramids
     • if x { true } else { false } (clippy needless_bool)
     • .unwrap() inside .map() / .and_then() closures
     • Wildcard _ => arms in matches on repo-owned enums
     • while used where for or an iterator adapter would express intent

2. Idioms appear but don’t dominate

     • Some iterator adapters used but for-index loops persist
     • Matches mostly exhaustive but wildcards silence variants the code should handle
     • Occasional needless_collect between adapter stages
     • Functions large but decomposable [37]

3. Idiomatic expression is the default

     • Iterator adapters used where they simplify
     • ? chains where they express intent
     • Pattern matching leveraged well (if let, let ...     else, exhaustive match)
     • Wildcards used only where the enum is open
     • Cognitive complexity in the neighbourhood of Ardito’s ~0.7/method idiomatic base-
       line [52]

4. Construct choice is deliberate

     • Appropriate blend of plain for loops when it reads better than a functional chain [45]
     • No needless .collect() between iterator stages
     • Destructuring in bindings and function arguments
     • matches! / let ...     else used exactly where they improve clarity, not because they
       exist
     • Macros used only for meta uses

5. Every construct legible as a choice

     • Reading the code is faster than reading its comments
     • Complex operations pipeline cleanly
     • The choice between imperative and functional shape is deliberate every time




                                             20
D5 — Expression and Control Flow Anti-idioms

  • Indexed loops [40, 51]

  • needless_bool, needless_collect, redundant_pattern_matching clippy warnings

  • .unwrap() in closures

  • Catch-all _ => arms in matches on enums we declared

  • Functions over 30 statements without decomposition [37]


D5 — Expression and Control Flow Idiomatic Signals

  • .iter().map(...).filter(...).collect() chains where they compose

  • for x in ... when a chain would obscure the shape

  • let Some(x) = ...        else   return ...    ; where a match would be better suited

  • Cognitive complexity ≤ 1.0 per method [52]


D6 — API, Naming, and Documentation In dimension 6, we ask the question “Would some-
one else be able to use this crate without reading its source?”

  1. Opaque without the source

       • get_foo()-style getters [46]
       • /// docs absent on pub items
       • Examples that use .unwrap() or that don’t compile
       • Missing # Errors / # Panics sections
       • Every item is pub [40]
       • Debug missing on public types

  2. Documented in places

       • Some public items documented but examples don’t run
       • Naming mostly follows RFC 430 but some abbreviations
       • # Errors sections missing on half of fallible functions
       • Ad-hoc conversion methods with unclear semantics

  3. Conventional and navigable

       • Collections expose iter / iter_mut / into_iter




                                                 21
      • as_ / to_ / into_ used per their cost conventions
      • /// docs on public items
      • # Errors / # Panics where applicable (# Panics when a panic is reachable under any
        input, instead of when a panic-macro token appears in the body
      • panic!() / unreachable!() in a branch the surrounding control flow proves unreachable
        does not require a # Panics section)
      • Examples use ?
      • pub(crate) used to narrow scope

  4. Guided use, runnable docs

      • Constructors are new
      • From / AsRef over inherent conversion methods
      • #[must_use] where a return is easy to drop by accident
      • Rustdoc examples runnable and present on the fallible/panicking public surface (cargo
        test --doc passes and covers more than a single trivial function)
      • Debug on public types
      • Struct fields private with accessors where invariants exist

  5. The API teaches its own use

      • The public API teaches its own use such that the docs are the mental model
      • Every export is intentional and its cost is stated
      • The crate could be released to crates.io without significant editing


D6 — API, Naming, and Documentation Anti-idioms

  • /// docs absent on pub items.

  • # Errors / # Panics missing on fallible / panicking public functions

  • get_foo() getters (Rust uses foo() and foo_mut()) [46]

  • Ad-hoc new_from_x / to_y methods where From / Into / AsRef fit

  • Everything pub [40]

  • Public types without Debug




                                              22
D6 — API, Naming, and Documentation Idiomatic Signals

   • Doctest examples that use ? and are runnable

   • #[must_use] on returns that carry meaning (e.g., Result, builders)

   • Public structs with private fields and constructor invariants

   • Module-level //! doc that states the invariant the module protects


2.4 PERFORMANCE
      Translation Throughput Translation throughput captures the rate at which a translator
can process C code and is an important consideration for practical adoption. We measure throughput
in thousands of lines of C code translated per hour (KLOC/hr). Throughput is measured at the
granularity of the complete AWS translation job rather than the translator’s internal processing
time. Consequently, the measurement includes standardized overhead associated with environment
setup and teardown and data transfer to and from S3. Because execution time in shared cloud
environments can vary due to factors outside the translator’s control, throughput measurements
should be interpreted with this inherent variability in mind.
      Runtime and memory overhead measurements are implemented in Cando and Test Runner.
We additionally provide a higher-level benchmarking script designed to reduce measurement bias
and variability. The script collects the relevant (translator, test case, test vector) tuples, randomizes
their execution order, executes a randomly selected subset as warm-up runs, and then performs and
reports the benchmark measurements. This methodology is intended to reduce systematic effects
from execution order, cache state, and other sources of measurement noise, thereby supporting more
reproducible comparisons across translators.


      Runtime Overhead Rust adopts the philosophy of zero-cost abstractions, or useful ab-
stractions that negligibly impact runtime. Successful translations into Rust should exploit this
principle to limit the increase—or even decrease—the time it takes to execute the same workload
in C. We evaluate this using perf-stat [53], a common tool for gathering performance statistics
for C and Rust programs. This captures several key statistics including, task clock, user, and total
runtime, instructions executed, CPU cycles, cach references/misses, among others that are relevant
to our evaluation.


      Memory Overhead Similarly—though not as important on modern hardware where mem-
ory is plentiful—is the goal of a Rust program’s memory footprint to be comparable to the original
C. To support this we use another common program, valgrind [54]. Its tool massif gives a snapshot
of the number of bytes allocated to the heap, stack, and used as metadata for the memory allocator,
throughout the execution of a program. An important caveat to note is our use of valgrind can
not always capture memory usage information. Particularly, if a test vectors runs and finishes very
quickly, the IPC mechanisms we need to setup will sometimes not initialize fast enough to send




                                                   23
information back. However, this has not been observed very often, so is not a major limitation
affecting our data collection.




                                             24
       3. BENCHMARK BATTERIES AND MILESTONE PROJECTS

3.1 BATTERY 01 BENCHMARK
      The first test battery, B01, was designed to contain almost exclusively C programs which
can be represented easily within the Rust type system. In particular, it excludes programs which
store memory on the heap, excludes programs which exhibit parallel execution, and aims to exclude
programs which exhibit memory access patterns that are difficult to represent in Rust’s affine type
system (e.g., interior mutability).
     The explicit set of features included in B01 are:

   • Pointers to data on the stack or static
        – No malloc or void*
        – Static initialization/constants
        – Pointer arithmetic only:
            ∗ Into arrays
            ∗ Using argc to index/parse argv
        – Pass-by-reference for values/structs not involving pointer arithmetic
        – Scoped arrays
   • Error handling
        – errno.h
        – Functions that return Boolean or other values for success/failure, and put the result of
          computation into a referenced value
            ∗ Many libc functions do this, for instance
            ∗ Possibly including different references pointing to members of the same object (dif-
              ficult for Rust ownership)
   • Global state
        – Compile-time constants
        – Static variables (mutating during execution)
   • Simple data structs without recursion and with size known at compile time
   • Code using libc
        – Rust translations will require Foreign Function Interfaces (FFI) calling C unless they
          swap in a Rust library or attempt to translate referenced functions
        – Functions from libc should (mostly) have Rust analogues that map naturally
   • Library functions
        – C interface to test with (as a drop-in replacement)
        – This will require unsafe code to permit FFI from C




                                                25
3.2 MILESTONE PROJECTS 00 AND 01 BENCHMARKS
      To complement the B01 test battery, we include two milestone projects drawn from the open-
source community. These projects provide larger, more realistic translation targets that exercise the
C features represented in B01 while introducing the additional challenges associated with translating
complete software projects. The two projects included in this benchmark are:

  1. Milestone Project 0 (P00): A repository consisting of the Perlin noise library [55]. P00 is
     a compact but computation-heavy codebase that exercises floating-point arithmetic, array
     indexing, and performance-sensitive inner loops making it representative of numerical and
     signal-processing workloads commonly found in legacy C code.

  2. Milestone Project 1 (P01): A repository focusing on the SPHINCS+ cryptographic library [56],
     which is substantially larger and more complex than P00, and stresses translation tools with
     extensive bit-level manipulation, strict correctness requirements, and sensitivity to even minor
     semantic deviations. P01 additionally tests translation tools’ management of build systems
     producing multiple libraries and supporting multiple configurations.

Together, these milestones complement the test battery by introducing more realistic and domain-
specific translation challenges.
      Both projects were modified versions of open-source libraries with the original Perlin Noise
library authored by Sean Barrett [55] and the original SPHINCS+ implementation authored by Eyal
Ronen [57] leveraging the NIST Post-Quantum Cryptography reference implementation [58] along
with an implementation of the BLAKE hash function [59] taken from the SUPERCOP benchmark
framework [60]. The two projects were modified to only exercise a similar subset of C features
to those in B01; however P01 underwent a significant transformation to test the translation tools’
handling of C project structure and configurability.


3.3 BATTERY 02 BENCHMARK
      The second test battery, B02, was designed to admit new classes of C program which the
previous battery excluded as resistant to safe Rust representation. B01 largely confined itself to
programs expressible within Rust’s affine type system while B02 relaxes those restrictions one ring
outward by introducing heap-allocated state, shared mutable data, indirect dispatch, and manual
resource-cleanup control flow. These constructs are precisely those a translation tool must map onto
Rust’s ownership, borrowing, and trait machinery to achieve a fully safe translation as opposed to
simply producing a direct syntactic analogue. This being said, B02 remains a bounded battery and
programs were heavily edited to avoid C features that are out-of-bounds for the battery such as
inline assembly, cyclic ownership patterns, and concurrency.
     The explicit set of features introduced in B02 are:

   • Heap allocation and ownership




                                                 26
    – Dynamic allocation via malloc / calloc / and realloc with release through free
    – Transfer of ownership across function boundaries (“allocate-here, free-there” patterns)
    – void* payloads and buffers

• Mutable aliasing and interior mutability

    – Multiple live, mutable paths reaching the same object (difficult for Rust’s borrow checker)
    – Shared mutable state reached indirectly, including through function pointers

• Raw buffer manipulation with a focus on strings and the standard library

    – Pointer-and-length buffers with possible overlap (memcpy, memmove, and the mem*/str*
      family)
    – In-place editing, appending, and search/replace over byte and character buffers

• Indirect dispatch

    – Function pointers stored as data: operation tables, callback fields, and typed vtable-style
      backends
    – Function-pointer values punned through void*

• Simple generic containers

    – Type-erased hash maps and growable arrays, instantiated through macros (which may
      be expressed with generics or trait objects in Rust)

• Error handling via cleanup control flow

    – goto-based cleanup ladders (which may translated into Drop and the ? operator in Rust)

• Type punning

    – Reinterpretation of storage through union members and packed bit-fields
    – Reinterpreting casts between object representations, e.g. serializing structured data to
      and from byte buffers

• Data structures with structural indirection

• Program structure

    – Cross-translation-unit linkage: internal-linkage (static) symbols, extern redeclaration,
      static inline, and name reuse across units
    – Deep preprocessor composition (token pasting, stringization, multi-level, and recursive
      macro expansion)

• File and filesystem interaction




                                             27
          – File I/O through descriptors (open/read/write/close), directory traversal, and path ma-
            nipulation

      • Environment-driven state

          – Configuration read from the environment (getenv)

       The organic half of B02 is drawn from small third-party codebases rather than from single-
purpose fragments: a JSON parser exhibiting the goto-cleanup idiom throughout, two-dimensional
collision-detection and ray-casting primitives mirroring compact single-header game libraries stretchy-
buffer and hash-map macros, and image-decoding, inflate, and Base64/UTF-8 codecs. A small num-
ber of entries are drawn from the Underhanded C Contest [61] (years 2009 and 2015): programs
whose intended behavior is deliberately hard to read from the source, included to stress translation
fidelity rather than any single language feature. The synthetic half focuses on explicit features or
interfaces of multiple features as in the previous battery.


3.4 MILESTONE PROJECT 02 BENCHMARK
       As with Milestone Projects P00 (Perlin Noise) and P01 (SPHINCS+), a single open-source
project was chosen to combine the battery’s isolated features under one build. Milestone Project 2
(P02) is a heavily modified port of the libgit2 library [62], the linkable implementation of Git.
P02 is substantially larger than the earlier milestones at the order of 100-thousand lines of code
and was chosen to not only exercise the full B02 feature set at once, but was also chosen as an
intermediate point for principled ownership analysis as libgit2 relies on acyclic and reference-based
data structures after excision of the internal memory pool. In this sense, P02 is a capstone that
escalates the same battery to test the scaling complexity of translation tools and as a core method
of differentiating translation based on the Rust idioms or structures the translator chooses.
       Together, B02 and its milestone move the evaluation from feature coverage toward transla-
tion soundness. The constructs the battery introduces (including mutable aliasing, buffer overlap,
lifetime-bearing cleanup paths, indirect dispatch, and deliberately-subtle semantics) are exactly
those whose correct translation is hardest to establish by inspection of the source alone as they
enable properties that no single site makes locally visible. B02 and P02, therefore, make up the
initial evaluation in which a tool’s ability to preserve behavior, and not merely parse and re-emit
constructs, is placed under test.


3.5 EVALUATION INFRASTRUCTURE
      The test and evaluation infrastructure7 provides a standardized and reproducible environment
for executing C-to-Rust translators against the benchmark. The infrastructure is instantiated using
the AWS Cloud Development Kit (CDK) in Python and deploys translators as AWS Batch jobs on
Fargate. Each translator is packaged as a Docker container and executed within a common Virtual
  7
      Publicly released at https://github.com/DARPA-TRACTOR-Program/PUBLIC-aws-translate.




                                                    28
Private Cloud (VPC), with external connectivity available for translators that rely on LLM API
endpoints.
      Translator containers are provided read access to an S3 bucket containing the C benchmark
inputs and write access to a separate S3 bucket for their generated Rust translations. Each input
archive contains the C source code and the materials necessary to build it, but does not include the
benchmark test vectors (i.e., sample inputs and expected outputs). Each test case provides either a
top-level CMakeLists.txt or CMakePresets.json specifying how the original C program should be
built. For translators that rely on external LLM services, API credentials can be securely provided
through AWS Secrets Manager. Together, this infrastructure enables researchers to execute and
evaluate translators under a common environment while reproducing the benchmark methodology
independently.




                                                29
This page intentionally left blank.




                30
                                      4. CONCLUSION

      The transition from legacy C software to memory-safe Rust presents both a significant oppor-
tunity and a difficult technical challenge. Successful translation requires substantially more than
producing Rust code that compiles or reproduces the behavior of a C program. A useful translation
must simultaneously preserve functional behavior, reduce reliance on unsafe constructs, maintain ac-
ceptable performance, and produce idiomatic Rust that can be understood, maintained, and evolved
by developers. The TRACTOR benchmark is designed to evaluate these dimensions together rather
than treating translation as a purely syntactic transformation.
      To support this goal, the benchmark combines progressively challenging test batteries with
larger milestone projects. Battery 01 establishes a foundation around C constructs that map rela-
tively naturally into Rust’s type and ownership systems, while Battery 02 introduces substantially
harder challenges such as dynamic allocation, mutable aliasing, indirect dispatch, type erasure,
cleanup control flow, and complex program structure. The milestone projects complement these
targeted tests by evaluating whether translation techniques scale to realistic software, culminating
in P02, a substantially larger codebase that stresses both translation scale and the ability to reason
about ownership and behavior across program boundaries.
      Equally important, the benchmark defines a reproducible methodology for determining what
constitutes a successful translation. Functional correctness is evaluated through observable behav-
ioral equivalence; safety considers both semantic uses of ‘unsafe‘ and the treatment of undefined
behavior; idiomaticity combines automated analysis with a structured manual rubric; and perfor-
mance captures translation throughput as well as runtime and memory overhead. Together, these
metrics recognize that no single measure adequately captures translation quality.
      The benchmark and its associated evaluation infrastructure are intended to evolve alongside
C-to-Rust translation technology. As increasingly difficult batteries and milestone projects are in-
troduced, the evaluation can expand to cover additional language features, system interactions, and
notions of behavioral equivalence. By publicly releasing the benchmarks, metrics, and supporting
infrastructure, the TRACTOR program provides a common basis for measuring progress and com-
paring approaches. Ultimately, the objective is not simply to demonstrate that C can be translated
into Rust, but to establish whether such translation can be performed correctly, safely, efficiently,
and at the scale necessary to make memory-safe modernization of legacy software practical.




                                                 31
This page intentionally left blank.




                32
                                      REFERENCES

 [1] TechRepublic, “Tiobe index for february 2026:        Top 10 most popular program-
     ming languages,” TechRepublic (2026), URL https://www.techrepublic.com/article/
     news-tiobe-index-language-rankings/, according to the TIOBE Programming Community
     Index, C and C++ consistently rank among the top programming languages worldwide.

 [2] L. Szekeres, M. Payer, T. Wei, and D. Song, “Sok: Eternal war in memory,” in 2013 IEEE
     Symposium on Security and Privacy (SP), IEEE (2013), pp. 48–62, URL https://ieeexplore.
     ieee.org/document/6547101/.

 [3] H. Okhravi, “Memory safety,” IEEE Security & Privacy 22(4), 13–15 (2024).

 [4] E.A.O. Levy, “Smashing the stack for fun and profit,” Phrack Magazine Issue 49 (1996), URL
     https://phrack.org/issues/49/14.html.

 [5] Microsoft Corporation, “Trends, challenges, and strategic shifts in the software vul-
     nerability mitigation landscape,” Microsoft, Technical report (2019), URL https:
     //github.com/microsoft/MSRC-SecurityResearch/blob/master/presentations/2019_
     02_BlueHatIL/2019_01%20-%20BlueHatIL%20-%20Trends%2C%20challenge%2C%20and%
     20shifts%20in%20software%20vulnerability%20mitigation.pdf, microsoft® presentation
     at BlueHat IL 2019 on software vulnerability trends.

 [6] SOC Prime, “Cve-2026-20700:    Apple patches zero-day exploited in sophisticated
     cyber attacks,” SOC Prime blog post (2026), URL https://socprime.com/blog/
     cve-2026-20700-vulnerability/.

 [7] National Security Agency and Cybersecurity and Infrastructure Security Agency, “Mem-
     ory safe languages: Reducing vulnerabilities in modern software development,” NSA and
     CISA, Technical rep. (2025), URL https://www.cisa.gov/resources-tools/resources/
     memory-safe-languages-reducing-vulnerabilities-modern-software-development,
     joint cybersecurity information sheet highlighting benefits of memory safe languages.

 [8] Office of the National Cyber Director, “Back to the building blocks: A path to-
     ward secure and measurable software,” The White House, Technical rep. (2024),
     URL          https://bidenwhitehouse.archives.gov/oncd/briefing-room/2024/02/26/
     memory-safety-fact-sheet/, technical report advocating adoption of memory safe program-
     ming languages.

 [9] Consumer Reports Advocacy, “Future of memory safety: Challenges and recommendations,”
     Consumer Reports Advocacy report (2023), URL https://advocacy.consumerreports.org/
     wp-content/uploads/2023/11/ConsumerReportsonmemorysafety.pdf.

[10] Cybersecurity and Infrastructure Security Agency and Federal Bureau of Inves-
     tigation, “Secure by design alert:     Eliminating buffer overflow vulnerabilities,”
     Threat advisory (2025), URL https://www.cisa.gov/resources-tools/resources/
     secure-design-alert-eliminating-buffer-overflow-vulnerabilities.




                                              33
[11] A.A. Terekhov and C. Verhoef, “The realities of language conversions,” IEEE Software 17(6),
     111–124 (2000), URL https://doi.org/10.1109/52.895180, discusses practical challenges
     and limitations of automated language converters for legacy code.

[12] C. Cowan, M. Barringer, C. Beattie, G. Kroah-Hartman, M. Frantzen, and P. Lokier, “Stack-
     guard: Automatic adaptive detection and prevention of buffer-overflow attacks,” in Proceed-
     ings of the 7th USENIX Security Symposium, USENIX Association (1998), pp. 63–78, presents
     StackGuard, an early and influential stack canary based defense against stack buffer overflows.

[13] H. Shacham, M. Page, B. Pfaff, E.J. Goh, N. Modadugu, and D. Boneh, “On the effectiveness
     of address-space randomization,” in Proceedings of the 11th ACM Conference on Computer and
     Communications Security (CCS), ACM (2004), pp. 298–307.

[14] N. Burow, S.A. Carr, J. Nash, P. Larsen, M. Franz, S. Brunthaler, and M. Payer, “Control-
     flow integrity: Precision, security, and performance,” ACM Computing Surveys 50(1), 16:1–
     16:33 (2017), survey of control-flow integrity mechanisms and their security and performance
     characteristics.

[15] H. Lefeuvre, N. Dautenhahn, D. Chisnall, and P. Olivier, “Sok: Software compartmentaliza-
     tion,” in Proceedings of the 46th IEEE Symposium on Security and Privacy (S&P’25), IEEE
     (2025), pp. 3107–3126.

[16] D. Song, J. Lettner, P. Rajasekaran, Y. Na, S. Volckaert, P. Larsen, and M. Franz, “Sok:
     Sanitizing for security,” in Proceedings of the 2019 IEEE Symposium on Security and Privacy,
     IEEE (2019), pp. 1275–1295.

[17] A. Reitz, A. Fromherz, and J. Protzenko, “Starmalloc: Verifying a modern, hardened memory
     allocator,” in Proceedings of the 2024 ACM SIGPLAN Conference on Systems, Programming,
     Languages, and Applications: Software for Humanity (OOPSLA) (2024), verified, concurrent,
     security-oriented memory allocator intended to harden against heap exploits and memory cor-
     ruption attacks.

[18] MISRA, MISRA C:2012 — Guidelines for the Use of the C Language in Critical Systems,
     Motor Industry Software Reliability Association (2012), a comprehensive set of guidelines to
     improve safety, portability, and reliability of C code, widely adopted in safety-critical industries.

[19] R.C. Seacord, The CERT® C Coding Standard: 98 Rules for Developing Safe, Reliable, and
     Secure Systems, Addison-Wesley Professional (2014), a comprehensive secure coding standard
     for C that identifies common coding errors, including those that lead to memory corruption
     and other vulnerabilities.

[20] Google Project Zero, “Google project zero: Security research team focused on zero-day vul-
     nerabilities,” Online security research initiative (2014), URL https://projectzero.google/,
     project Zero is a Google security research team dedicated to finding and publicly reporting
     zero-day vulnerabilities in software and hardware systems to improve overall security.




                                                   34
[21] R.N. Watson, J. Baldwin, D. Chisnall, T. Chen, J. Clarke, B. Davis, N. Filardo, B. Gutstein,
     G. Jenkinson, B. Laurie, et al., “It is time to standardize principles and practices for software
     memory safety,” Communications of the ACM (2025).

[22] S. Klabnik and C. Nichols, The Rust Programming Language, No Starch Press (2019), URL
     https://doc.rust-lang.org/book/, 2nd edition.

[23] M. Emre, R. Schroeder, K. Dewey, and B. Hardekopf, “Translating c to safer rust,” Proc. ACM
     Program. Lang. 5(OOPSLA), 121 (2021).

[24] M. Ling, Y. Yu, H. Wu, Y. Wang, and J.R. Cordy, “In rust we trust: A transpiler from unsafe
     c to safer rust,” (2022), available at research.cs.queensu.ca.

[25] A. Fromherz and J. Protzenko, “Compiling c to safe rust, formalized,” (2024).

[26] R. Li, B. Wang, T. Li, P. Saxena, and A. Kundu, “Translating c to rust: Lessons from a user
     study,” in NDSS Symposium 2025 (2025).

[27] M. Farrukh, S. Shah, B. Coskun, and M. Polychronakis, “Safetrans: Llm-assisted transpilation
     from c to rust,” (2025).

[28] Y. Gao, C. Wang, P. Huang, X. Liu, M. Zheng, and X. Zhang, “Pr2: Peephole raw pointer
     rewriting with llms for translating c to safer rust,” (2025).

[29] T. Zhou, Z. Zhang, H. Lin, S. Jha, M. Christodorescu, K. Levchenko, and V. Chandrasekaran,
     “Sactor: Llm-driven correct and idiomatic c to rust translation with static analysis and ffi-based
     verification,” (2025), URL https://arxiv.org/abs/2503.12511.

[30] S. Klabnik and C. Nichols, The Rust Programming Language, No Starch Press (2018), URL
     https://doc.rust-lang.org/book/.

[31] Defense Advanced Research Projects Agency, “Tractor: Translating all c to rust program,” Pro-
     gram overview on DARPA.mil (2024), URL https://www.darpa.mil/research/programs/
     translating-all-c-to-rust, describes the TRACTOR initiative aimed at automating the
     translation of legacy C code to Rust to eliminate memory safety vulnerabilities.

[32] “Falco,” URL https://falco.org.

[33] E.S. Hald, “Educational undefined behavior technical report,” URL https://www.open-std.
     org/JTC1/sc22/wg14/www/docs/n3308.pdf.

[34] R. Jung, B. Kimock, C. Poveda, E.S. Muñoz, O. Scherer, and Q. Wang, “Miri: Practical
     undefined behavior detection for rust,” Proceedings of the ACM on Programming Languages
     10(POPL), 1383–1411 (2026).

[35] The Rust Project, “Clippy lints documentation,” https://doc.rust-lang.org/clippy/.

[36] M. Messer, N.C.C. Brown, M. Kölling, and M. Shi, “How consistent are humans when grading
     programming assignments?” ACM Transactions on Computing Education (2025).




                                                  35
[37] J. Perretta, W. Weimer, and A. DeOrio, “Human vs. automated coding style grading in comput-
     ing education,” in 2019 ASEE Annual Conference & Exposition, Tampa, FL (2019), computers
     in Education Division, paper ASEE19CIE.

[38] Dehghan et al., “Rustine:     Translating large-scale C repositories to idiomatic Rust,”
     arXiv:2511.20617 (2025).

[39] T. Yin and contributors, “Lizard: A simple code complexity analyser,” https://github.com/
     terryyin/lizard.

[40] M. Endler, “The four horsemen of bad Rust code,” Talk, FOSDEM 2024 (Rust devroom), Brus-
     sels (2024), slides at sources/talks/four-horsemen.pdf; repo https://github.com/corrode/four-
     horsemen-talk.

[41] K.R. Fulton, A. Chan, D. Votipka, M. Hicks, and M.L. Mazurek, “Benefits and drawbacks of
     adopting a secure programming language: Rust as a case study,” in Seventeenth Symposium on
     Usable Privacy and Security (SOUPS 2021), USENIX Association (2021), pp. 597–616, URL
     https://www.usenix.org/conference/soups2021/presentation/fulton.

[42] S.H. Edwards and M.A. Perez-Quinones, “Web-cat: automatically grading programming as-
     signments,” in Proceedings of the 13th Annual Conference on Innovation and Technology in
     Computer Science Education, New York, NY, USA: Association for Computing Machinery
     (2008), ITiCSE ’08, p. 328, URL https://doi.org/10.1145/1384271.1384371.

[43] M. Robati Shirzad and P. Lam, “A study of common bug fix patterns in Rust,” Empirical
     Software Engineering 29 (2024).

[44] B. Qin, Y. Chen, Z. Yu, L. Song, and Y. Zhang, “Understanding memory and thread safety
     practices and issues in real-world Rust programs,” in Proceedings of the 41st ACM SIGPLAN
     Conference on Programming Language Design and Implementation (PLDI 2020) (2020).

[45] corrode.dev, “Be simple,” https://corrode.dev/blog/simple/.

[46] The Rust Project, “Rust API guidelines checklist,”         https://rust-lang.github.io/
     api-guidelines/checklist.html.

[47] S. Gerat, “Three kinds of unwrap,” https://zkrising.com/writing/three-unwraps/ (2024).

[48] V. Astrauskas, C. Matheja, F. Poli, P. Müller, and A.J. Summers, “How do programmers use
     unsafe Rust?” Proceedings of the ACM on Programming Languages 4(OOPSLA), 1–27 (2020).

[49] M. Emre, R. Schroeder, K. Dewey, and B. Hardekopf, “Translating C to safer Rust,” Proceedings
     of the ACM on Programming Languages 5(OOPSLA) (2021).

[50] H. Xu, Z. Chen, M. Sun, Y. Zhou, and M.R. Lyu, “Memory-safety challenge considered solved?
     an in-depth study with all Rust CVEs,” ACM Transactions on Software Engineering and
     Methodology 31(1) (2021).




                                               36
[51] A. Birillo, I. Vlasov, A. Burylov, V. Selishchev, A. Goncharov, E. Tikhomirova, N. Vyahhi,
     and T. Bryksin, “Hyperstyle: A tool for assessing the code quality of solutions to programming
     assignments,” in Proceedings of the 53rd ACM Technical Symposium on Computer Science
     Education (SIGCSE 2022) (2022), pp. 307–313.

[52] L. Ardito, L. Barbato, R. Coppola, and M. Valsesia, “Evaluation of Rust code verbosity, un-
     derstandability and complexity,” PeerJ Computer Science 7, e406 (2021).

[53] “perf-stat(1)—linux   manual    page,”    URL     https://man7.org/linux/man-pages/man1/
     perf-stat.1.html.

[54] N. Nethercote and J. Seward, “Valgrind: a framework for heavyweight dynamic binary in-
     strumentation,” in Proceedings of the 28th ACM SIGPLAN Conference on Programming Lan-
     guage Design and Implementation, New York, NY, USA: Association for Computing Machinery
     (2007), PLDI ’07, p. 89–100, URL https://doi.org/10.1145/1250734.1250746.

[55] S. Barrett, “stb_perlin: Public domain perlin noise implementation,” https://github.com/
     nothings/stb (2017), single-file public domain library, stb_perlin.h.

[56] D.J. Bernstein, A. Hülsing, S. Kölbl, R. Niederhagen, J. Rijneveld, and P. Schwabe, “The
     sphincs+ signature framework,” in Proceedings of the 2019 ACM SIGSAC Conference on Com-
     puter and Communications Security, New York, NY, USA: Association for Computing Machin-
     ery (2019), CCS ’19, p. 2129–2146, URL https://doi.org/10.1145/3319535.3363229.

[57] E. Ronen, “splincsplusc: Sphincs+c,” https://github.com/eyalr0/sphincsplusc (2022).

[58] “SPHINCS+: The stateless hash-based signature scheme,” https://sphincs.org/, accessed:
     2026-09-06.

[59] J.P. Aumasson, L. Henzen, W. Meier, and R.C.W. Phan, “Sha-3 proposal blake,” Submission
     to NIST (2008), URL http://ehash.iaik.tugraz.at/uploads/0/06/Blake.pdf.

[60] D.J. Bernstein and T. Lange, “SUPERCOP: System for unified performance evaluation re-
     lated to cryptographic operations and primitives,” https://bench.cr.yp.to/supercop.html,
     accessed: 2026-09-06.

[61] “The underhanded c contest,” http://www.underhanded-c.org/, accessed: 2026-07-16.

[62] libgit2 contributors, “libgit2: A cross-platform, linkable library implementation of git,” https:
     //libgit2.org (2026), URL https://github.com/libgit2/libgit2, accessed: 2026-07-16.




                                                 37
This page intentionally left blank.




                38
