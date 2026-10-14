                                         Mostly Automatic Translation of Language Interpreters
                                         from C to Safe Rust
                                         BO WANG∗ , National University of Singapore, Singapore
                                         BRANDON PAULSEN, Amazon, USA
                                         JOEY DODDS, Amazon, USA
                                         DANIEL KROENING, Amazon, USA
                                         UMANG MATHUR, National University of Singapore, Singapore
arXiv:2606.27122v1 [cs.PL] 25 Jun 2026




                                         PRATEEK SAXENA, National University of Singapore, Singapore
                                         Translating C programs to safe Rust is challenging owing to significant differences in typing constraints,
                                         ownership, and borrowing rules. Interpreter programs are particularly important targets for such translation,
                                         as they often handle untrusted inputs and suffer from memory-related vulnerabilities. We present Reboot, a
                                         mostly-automatic technique that translates real-world interpreter programs from C to safe Rust. Using Reboot,
                                         we have translated six interpreters ranging from 6k to 23k lines of C code to safe Rust, with each translation
                                         requiring only 1 to 11 brief user interventions. All translations pass 100% of the provided test suites, and achieve
                                         62%–92% pass rates on separately created validation tests that were never exposed to the system. A security
                                         case study on mujs shows that memory vulnerabilities such as heap buffer overflows and use-after-free
                                         present in C are eliminated in the safe Rust translation. Two ideas underpin Reboot. First, feature reduction
                                         decomposes the translation by program features, creating a sequence of milestones where each is a complete,
                                         testable program; the translation starts from the simplest version and incrementally restores features, with each
                                         milestone validated before proceeding. Second, a multi-agent architecture orchestrates inherently unreliable
                                         coding agents through automated validation and feedback, keeping long-running translation workflows
                                         on track with minimal human involvement. An ablation study confirms that feature reduction improves
                                         translation correctness compared to using multi-agent translation alone, with 6%–20% improvements in pass
                                         rates on validation test suites.

                                         1   Introduction
                                         C has been widely used for implementing language interpreters, where low-level memory control
                                         is essential for performance. However, C’s lack of memory safety often leads to vulnerabilities such
                                         as spatial and temporal memory errors [12, 45], and Rust is gaining popularity as an alternative that
                                         provides strong memory safety guarantees while retaining low-level control [1, 2]. Within the body
                                         of software written in C, interpreter programs are particularly important targets for migration to
                                         Rust: they appear in a wide range of contexts—as standalone tools, as scripting engines embedded
                                         in databases and browsers, and in many other applications—and are especially security-critical
                                         because they often handle untrusted inputs. Many widely-deployed interpreters written in C suffer
                                         from memory-related security vulnerabilities [5, 24, 25, 36, 37], and translating them to safe Rust
                                         would significantly improve their security posture.
                                            Automatic translation from C to safe Rust is challenging. The significant differences in typing
                                         constraints, ownership, and borrowing rules mean that producing safe, idiomatic Rust often requires
                                         substantial restructuring of the original C code. Existing rule-based translators [7, 22, 29, 57]
                                         typically preserve the low-level structure of the C source, producing non-idiomatic Rust with
                                         limited safety guarantees. LLM-based approaches [3, 4, 6, 9, 10, 35, 41, 43, 49, 54, 59] are more
                                         promising for synthesizing safe Rust, but most decompose programs by functions. Since individually
                                         ∗ Work done during an internship at Amazon.


                                         Authors’ Contact Information: Bo Wang, National University of Singapore, Singapore, bo_wang@u.nus.edu; Brandon
                                         Paulsen, Amazon, USA, bpaulse@amazon.com; Joey Dodds, Amazon, USA, jldodds@amazon.com; Daniel Kroening, Amazon,
                                         USA, dkr@amazon.com; Umang Mathur, National University of Singapore, Singapore, umathur@nus.edu.sg; Prateek Saxena,
                                         National University of Singapore, Singapore, dcsprs@nus.edu.sg.
2                    Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


translated functions cannot be tested as part of a running program, validating partial translations
requires nontrivial additional techniques, and success has been demonstrated primarily on libraries.
A recent agent-based approach [28] avoids function-level decomposition, achieving reasonable
correctness on standalone programs of hundreds to thousands of lines of code. However, the existing
approaches have not yet been shown to scale to the size and complexity of real-world interpreter
programs, which are often large, have complex internal data types, and exhibit cross-cutting data
flow that often needs to be restructured to satisfy Rust’s language rules.
Our Results. In this work, we present Reboot, an agent-based technique for translating interpreter
programs from C to safe Rust. Reboot takes a C program and a test suite as input, and produces a
safe Rust translation that passes all provided tests; a human user is only occasionally needed to
make design decisions or provide clarifications that the system cannot resolve on its own. Using
Reboot, we have translated six interpreter programs— awk (6k LoC), picoc (8k LoC), gnu-bc
(8k LoC), wren (8k LoC), mujs (17k LoC), and pocketpy (23k LoC)—from C to safe Rust. Each
program is paired with a test suite (sourced from the project or supplemented by us ), achieving
74%–88% line coverage on the C source, and all translations pass all of the provided test suites. To
evaluate correctness beyond the provided tests, we created validation test suites independently
of and separately from the provided tests, never exposed to the system during translation; our
translations achieve 62%–92% pass rates on these unseen tests. Each translation takes 28 to 90 hours
of wall-clock time, costs $460 to $1,780, and requires only 1 to 11 user interventions, each taking
roughly 5 minutes. To evaluate security improvements, we prepared a version of mujs with 20 of its
historical CVEs re-introduced into the latest codebase, and translated it using Reboot; the results
show that memory-related vulnerabilities such as heap buffer overflows, use-after-free, and stack
buffer overflows are indeed eliminated in the safe Rust translation. Performance measurements
on release builds show that most translated programs have median slowdowns of ∼1.28x–1.51x
compared to the original C programs.
Our Approach. Two ideas underpin Reboot. First, to handle the unreliability of coding agents,
Reboot uses a multi-agent architecture that orchestrates long-running translation workflows.
Agents are inherently unreliable: they may fail to complete a task, claim completion when the
output is incorrect, get stuck in unproductive loops, or crash unexpectedly. Reboot addresses this
by employing additional agents that validate outputs and provide automated feedback, detecting
and recovering from failures without human involvement. A finite-state-machine guard enforces
the workflow protocol, ensuring that agents follow the expected sequence of operations. Together,
these mechanisms allow the system to stay on track for days with most issues resolved automatically
and only a small number of cases escalated to the user.
   Second, to handle the complexity of translating real-world interpreters, Reboot uses a new
approach that we call feature reduction. Feature reduction decomposes the translation into a
sequence of validated milestones, each defined by program features rather than by syntactic
structure. Prior work typically decomposes by syntactic units such as functions; however, interpreter
features like exception handling or closures are cross-cutting—they span multiple functions and
files across the codebase, which motivates decomposing by features instead. Feature reduction
progressively simplifies the full interpreter into a sequence of feature levels, where each level is a
complete, runnable program that can be independently tested and validated. The translation starts
from the simplest version and incrementally restores features, with each milestone validated before
proceeding. This creates manageable steps without imposing structural constraints on how the code
is organized in Rust, giving agents the freedom to restructure code as needed for Rust’s ownership
and borrowing rules. An ablation study confirms that feature reduction improves translation
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                                                  3

                                     Feature Level 1            Feature Level 15          Feature Level 16 (Full)
       Feature Level 0               All FL0 features           All FL14 Features         All FL15 Features + JSON
       Can log string literals.      + Primitive Types        … + Regular Expression      Or simply, everything in mujs:
        print(“hello”)                 3.14, true, null          x.match(/\d+/g)          Closures, Iterators, Regex, Proto-chain,
                                                                                          if-stmt, for-loop, try-catch, UTF8…
       (I)
       Planning
       Phase
                        FL0                FL1            …           FL15              FL16

       (II)
       Feature
       Reduction                                                                                                         C/mujs
                      C-FL0              C-FL1            …          C-FL15            C-FL16
       Phase                                                                                                             (Input)


                   “Hello-world”                                                               Complete mujs
                    interpreter                                                                 interpreter


                                                                                                                       Rust/mujs
                      RS-FL0             RS-FL1           …          RS-FL15           RS-FL16
                                                                                                                       (Output)
       (III)
       Translation                                                                           FL Plan Doc       Auto. Conversion
       Phase                      Translating mujs to safe Rust using REBOOT                Code Version
                                                                                                                Correspondence




                              Fig. 1. The workflow of the translation process using Reboot.


correctness compared to using the multi-agent architecture alone without feature reduction, with
6%–20% improvements in pass rates on validation test suites.
   The rest of this paper is organized as follows. Section 2 gives an overview of feature reduc-
tion and multi-agent orchestration. Section 3 describes the system in detail. Section 4 covers the
implementation. Section 5 presents the evaluation, and Section 7 discusses related work.

2     Overview
Translating complex interpreter programs from C to safe Rust using LLM agents presents two high-
level design challenges: decomposing the translation task into manageable pieces, and orchestrating
a self-correcting workflow of agents that fail probabilistically.

2.1    Decomposition Strategy
Translating a large program all at once is difficult, so decomposing the task is necessary and standard.
Most prior work decomposes by functions and user-defined data types (e.g. structs) both for C to
Rust translation [3, 4, 6, 35, 41, 43, 49, 59] and for other language pairs [20, 47, 56, 58]. However,
interpreter features are cross-cutting: a single feature like exception handling is implemented by
code scattered across the lexer, parser, runtime, and bytecode executor. We propose a new approach
called feature reduction that decomposes by program features instead. A feature in an interpreter is
a supported language capability, such as for-loops, closures, or exception handling. Removing a
feature means removing all related code segments across these components, yielding a simpler yet
complete, runnable interpreter.
   Feature reduction applies this process progressively, removing one or a few features at a time.
Each step produces a feature level (FL)—a version of the program that supports a specific subset of
features. The removal order respects feature dependencies: features that other features depend on
are removed later, so each feature level remains a coherent, runnable program. Each feature level
has its own test suite, adapted from the original by removing or simplifying tests that depend on
unsupported features. The result is a sequence of feature levels, from the full-featured program
(FL𝑁 ) down to a minimal version (FL0 ) that implements only basic functionality.
4                                 Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


    Makefile | 4 +-
                                   …                                                                   …
    astnames.h | 1 -
    jsbuiltin.c | 6 -                  c/mujs                    Test Suite                   rs/mujs          builtin.rs | 14 ++-
    jscompile.c | 6 -                                                                                          builtin_object.rs | 2 +-
    jsgc.c | 7 --
                                          FL15                   FL15 (174 tests)                FL15          builtin_regexp.rs | 358 ++++++
    jsi.h | 19 ----                                                                                            builtin_string.rs | 425 ++++++
    jslex.c | 80 --------------                                                                                compiler.rs | 13 +-
    jsobject.c | 14 ---                                                                                        lexer.rs | 111 ++++++++++-
                                                            20 tests modified 281(-)30(+)                      lib.rs | 7 ++
    jsparse.c | 6 -
    jsregexp.c | 232 ----------     …I’ll remove Regex        test019_strings_advanced,                        main.rs | 12 ++
                                                              test094_utf_edge_cases…       …I’ll add Regex    object.rs | 7 ++
    jsrepr.c | 8 --                 support from c/mujs
    jsrun.c | 68 ------------                                                               support for the    opcode.rs | 148 +++++++------
                                    and simplify the test   10 tests removed 2337(-)                           parser.rs | 20 ++++
    jsstring.c | 255 +---------                                                             translated mujs.
    mujs.h | 8 --                   suite.                    test008_regex.js,                                regexp.rs | 1470 ++++++++++++
    one.c | 2 -                                               test022_regex_advanced…                          runtime.rs | 134 +++++++++++-
    opnames.h | 1 -                                                                                            state.rs | 12 ++
    pp.c | 24 ----
    regexp.c | 1277 -----------
                                                                                                               Translation (Rust Diff)
    regexp.h | 46 --------
    ...
                                       c/mujs                    Test Suite                   rs/mujs
                                          FL14                   FL14 (164 tests)                FL14
    Feature Reduction (C Diff)
                                    …                                                                 …
Fig. 2. An example of changes in source code as well as the test suite across feature levels during translation.


   Figure 1 illustrates the overall process using mujs, a JavaScript interpreter, as an example. The
process consists of three main phases. In the Planning Phase, we analyze the input C program
to identify its features and create a reduction plan that defines the sequence of feature levels.
In the Feature Reduction Phase, we progressively simplify the C program from the full version
(C-FL𝑁 ) down to a minimal version (C-FL0 ), producing a validated C program at each level. In the
Translation Phase, we start by translating the simplest C program (C-FL0 ) to Rust (RS-FL0 ). We then
incrementally restore features, translating RS-FL0 to RS-FL1 , then to RS-FL2 , and so on, until we
reach the full translation (RS-FL𝑁 ). Each step in the feature reduction and translation phases is
validated before proceeding to the next.
   In the mujs example, FL16 is the complete JavaScript interpreter with all features: closures,
iterators, prototype chains, regular expressions, exception handling, and more. By removing features
from the full program, we obtain a sequence of simpler versions. FL15 , obtained by removing only
CLI options, retains nearly all language features including regular expressions. Intermediate levels
support progressively fewer capabilities—FL1 supports only binary operators and numbers (e.g.,
3.14*(R**2) ), and FL0 is a minimal “hello-world” interpreter limited to logging string literals
(e.g., print("hello") ). Each feature level is a working JavaScript interpreter for a subset of the
language, obtained by feature reduction.
   Figure 2 shows a single feature-level transition in each phase. On the left, the transition from
C-FL15 to C-FL14 removes the support for regular expressions from the C codebase. The diff spans
many files, including regexp.c (∼1.3k lines), jsstring.c (∼250 lines), jsregexp.c (∼230 lines),
and others. Many of these changes are related to the same feature, demonstrating that a single
feature can be cross-cutting. On the right, the translation from RS-FL14 to RS-FL15 adds regular
expression support to the Rust translation. The Rust changes similarly span multiple files, with
regexp.rs (∼1.5k lines) and builtin_string.rs (∼400 lines) among the largest.
   Beyond spanning multiple files, translating a feature may also require redesigning the program’s
data structures to utilize Rust language features and satisfy safe Rust constraints. Figure 3 compares
the central compilation state for the regex feature in C ( struct cstate ) and in the Rust translation
( CompileState ). While most fields have direct correspondences, two groups of fields are absent in
Rust (➀ and ➁ in the figure). In ➀, the C struct stores a pointer to the output program (prog ) and
an arena allocator (pstart, pend ) for parse tree nodes; these are kept in the shared state so that
the error handling logic can free them manually on failure. In Rust, ownership-based resource man-
agement makes this unnecessary: the output program is a local variable, and nodes are individually
heap-allocated with Box . In ➁, the C struct uses setjmp/ longjmp for non-local error handling
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                                                5

                       struct cstate {
                                                                       ...
                             Reprog *prog;                             struct CompileState<'a> {
                       1     Renode *pstart, *pend;             ?
                                                                         source: &'a [u8],
                             const char *source;                         pos: usize,
                             int ncclass;                                ncclass: usize,
                             int nsub;                                   nsub: usize,
                             Renode *sub[REG_MAXSUB];                    sub: [Option<Box<Renode>>; REG_MAXSUB],

                             int lookahead;                              lookahead: i32,
                             Rune yychar;                                yychar: Rune,
                             Reclass *yycc;                              yycc_idx: usize,
                             int yymin, yymax;                           yymin: i32,
                                                                         yymax: i32,
                       2
                             const char *error;
                             jmp_buf kaboom;
                                                                ?
                                                                         cclass: [Reclass; REG_MAXCLASS],
                             Reclass cclass[REG_MAXCLASS];
                       };                                              }
                       ...                                             ...



                              regexp.c                                           regexp.rs
                              (@FL15)                                            (@FL15)




Fig. 3. Comparison of the regex compilation state in C ( struct cstate ) and Rust ( CompileState ). Corre-
sponding fields are connected by lines. ➀ Fields for the output program and arena allocator are absent in Rust,
replaced by local variables and individual heap allocations. ➁ Fields for setjmp / longjmp error handling are
absent in Rust, replaced by Result -based error propagation.



Table 1. Agent fault types and handling mechanisms. The system observes only the worker’s status, not
the underlying reality. 𝐻 (history-feedback) and 𝑉 (validity) handle each status; the outcome depends on
whether the worker’s claim matches reality. Escalate means pausing and requesting external assistance
(from a higher-level system or user).

Agent Says   Reality                Type    Mechanism                             Examples
             Actually stuck         A.1     𝐻 : suggest next                      Bug too complex, needs major refactoring
BLOCKED      Not stuck              B.1     𝐻 : suggest next                      Agent unwilling to work
             Repeated (loop)        C.1     𝐻 : loop → suggest next / Escalate    Repeated BLOCKED without progress
             Making progress        A.2     𝐻 : progress → continue               Tests improving across attempts
MORE_WORK    No progress            B.2     𝐻 : no-progress → suggest next        Agent retries without meaningful change
             Repeated (loop)        C.2     𝐻 : loop → suggest next / Escalate    Repeated MORE_WORK without progress
             Actually done          –       𝐻 →𝑉 : valid → proceed                All tests pass, code review clean
DONE         Not done               B.3     𝐻 →𝑉 : invalid → 𝐻 suggest next       Tests fail, or missing test cases
             Repeated (loop)        C.3     𝐻 →𝑉 : invalid → Escalate             Worker ignores 𝑉 ’s complaints, keeps claiming DONE
             Actually infeasible A.4        𝐻 → Escalate                          No safe Rust equivalent; wrong tests
INFEASIBLE
             Not infeasible      B.4        𝐻 → Escalate                          Agent claims infeasible; alternative exists
ERROR        Agent failed           D       𝐻 : resume / restart / Escalate       Crash, Hang, malformed output




( error , kaboom); the Rust translation replaces this with Result-based error propagation [46, 50].
These data structure changes are not isolated—they propagate to every function that uses the
state, affecting function signatures and error handling throughout the feature’s implementation.
Feature reduction gives agents the freedom to make such restructuring decisions, since it imposes
no constraints on how the Rust code is organized; the resulting program at each feature level is
validated as a whole before proceeding to the next.
6                    Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


2.2   Orchestration of Faulty Agents
An independent challenge arises in orchestration of unreliable agents. At each feature-level tran-
sition, a multi-agent system works toward an objective—such as reducing the program by one
feature level, or translating one feature level to Rust. The primary worker agent makes multiple
attempts, reporting a status after completion (e.g., DONE, BLOCKED). The reported status may not
match reality—what the worker actually achieved, usually due to hallucination. Any outcome other
than successfully meeting the objective is a fault. We model this problem abstractly below.
   Faults. After each attempt, the worker reports a status indicating what it believes it has achieved
toward the objective, but this status may not reflect reality. Table 1 categorizes agent faults based
on two dimensions: what the agent reports and what is actually true in reality. The worker reports
one of five statuses: BLOCKED (cannot proceed), MORE_WORK (objective not yet met), DONE (objective
met), INFEASIBLE (objective is fundamentally infeasible), or ERROR (agent crashed or produced
malformed output). When the status matches reality but the objective remains unmet, we have
type A faults (A.1 for blocked, A.2 for needs more work, A.4 for genuinely infeasible). When the
status mismatches reality, we have type B faults: false blocking (B.1), misassessment of progress
(B.2), false completion (B.3), or false infeasibility (B.4). When the worker repeatedly reports the
same status without actual progress, we have type C faults (unproductive loops): repeated blocking
(C.1), repeated incomplete work with no visible progress (C.2), or repeated false completion where
the worker ignores validation complaints (C.3). Finally, type D faults cover agent crashes and
malformed outputs. Since the system only observes the worker’s status, not the underlying reality,
handling these faults requires additional mechanisms.
 Validity and Progress Mechanisms. The goal is to make progress toward meeting the objective. To
model these requirements, we introduce two conceptual mechanisms:
      • A Validity mechanism (𝑉 ) determines whether the worker’s output actually satisfies the
        objective’s correctness criteria, independent of what the worker reports. For instance, 𝑉
        can validate the output (Rust code) by compiling it, reviewing it, and running test cases.
      • A History-feedback mechanism (𝐻 ) analyzes the history of the worker’s status reports
        and provides targeted feedback. For example, 𝐻 can track patterns across attempts, detect
        loops, and suggest next steps to help the worker make progress or recover from errors.
These are conceptual mechanisms that can be implemented in various ways, such as separate agent
calls, rule-based checks, or a combination of both. Table 1 shows how 𝑉 and 𝐻 handle each fault
type. For BLOCKED and MORE_WORK, 𝐻 assesses the situation based on history: it tracks progress,
detects loops, and either suggests next steps or escalates (A.1, B.1, C.1, A.2, B.2, C.2). For DONE, 𝐻
determines that validation is needed, then 𝑉 checks the worker’s claim against correctness criteria,
catching false completions (B.3). For INFEASIBLE, the system always escalates to the user (A.4,
B.4), since this may involve clarifications of the objective or design decisions. For agent errors
(D), 𝐻 attempts recovery by resuming or restarting the agent. Both mechanisms are necessary: 𝑉
alone catches incorrect outputs but does not help the agent improve, while 𝐻 alone cannot detect
correctness. Together, 𝑉 ensures correctness and 𝐻 ensures progress. This model assumes that 𝑉
and 𝐻 are themselves reliable—the fault taxonomy above addresses worker unreliability only. We
revisit this assumption in Section 5.
  User Escalation: The last resort. Not all faults can be resolved automatically. Issues requiring
human judgment typically fall into three categories. First, when the worker claims the objective is
INFEASIBLE (A.4, B.4), such as a language construct with no satisfactory safe Rust equivalent, the
system always escalates since this may involve clarifications of the objective or design decisions.
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                                                     7

              (a) mujs RS-FL15 : Regex                                           (b) picoc RS-FL15 + RS-FL6.4

 W: Translates core regex engine (∼1.5k lines)                        RS-FL15 : Eliminate Unsafe Blocks
     Tests: 122/168. Reports MORE_WORK                                𝑉 : Code review: 87 unsafe blocks
  𝐻 : Progress detected → continue                            [A.2]   W: Reports INFEASIBLE: “cannot eliminate”                 [B.4]
 W: Adds RegExp prototype methods                                      𝐻 : Conflicts with requirement → ESCALATE
     Tests: 129/168. Reports MORE_WORK
                                                                       User: “Use nix/chrono. Zero unsafe non-negotiable.”
  𝐻 : Progress detected → continue                            [A.2]
                                                                      W: Correct approach. Eliminates unsafe blocks.
            · · · 2 more attempts (143, 150/168) · · ·                    Unsafe: 87 → 25. Reports MORE_WORK
 W: Fixes regex error handling (try-catch)                             𝐻 : Progress → continue                                  [A.2]
      Tests: 168/168. Reports DONE
 𝑉 : Tests: 168/168 passed ✓                                                             · · · several iterations · · ·
      No cheating detected ✓                                          W: Encapsulates remaining 4 in safe wrappers
 𝑉 : Code review: 11 compiler warnings                                    Tests: 154/154. Reports DONE                          [C.3]
  𝐻 : Assigns investigation + fix tasks                                𝐻 : 𝑉 rejected, worker ignores → ESCALATE
 W: Fixes all 11 warnings                                                 Worker: “achieves spirit of 100% safe”
      (unused vars, dead code, unreachable)                               Requirement: zero unsafe blocks
      Tests: 168/168, warnings: 0
                                                                       User: “Drop fork() support. Safe enum, not transmute.”
 𝑉 : Re-validates: tests pass ✓
 𝑉 : Code review: 0 warnings ✓                                        W: Eliminates final 4 blocks
                                                                           Tests: 154/154, unsafe: 0
                                                                      𝑉 : Re-validates: all tests pass ✓
           14 tasks · 0 escalations · fully automatic
                                                                                     26 tasks · 2 escalations · ∼5.5h
                                                                      RS-FL6.4 : Struct Pointer Members
     𝐻 auto-feedback         Escalation       User guidance           W: Translates struct support
                                                                           Tests: 118/118. Reports DONE                         [B.3]
                   [X.n] fault type (Table 1)                         𝑉 : Checks coverage—1 test not in runner!
                                                                           Runs missing test → FAILS
                                                                           → Rejects DONE, sends back to W
                                                                      W: Fixes struct pointer support + runner
                                                                           Tests: 119/119
                                                                      𝑉 : Re-validates: all tests pass ✓
                                                                                      14 tasks · 0 escalations · ∼1.5h


Fig. 4. Condensed system logs (simplified from real trajectories) showing 𝑉 and 𝐻 mechanisms during
translation using Reboot. (a) mujs FL15 : iterative progress tracked by 𝐻 (A.2), multi-level validation by 𝑉
(tests + code review), fully automatic—no user intervention needed. (b) picoc FL15 +FL6.4 : worker claims
objective infeasible (B.4, overridden by user), worker repeatedly claims completion ignoring 𝑉 ’s complaints
(C.3, escalated), and 𝑉 detecting a missing test in the runner (B.3).




Second, when 𝐻 ’s feedback fails to resolve repeated faults (C.1, C.2), the user may intervene to
provide clarification, guide the worker to prioritize certain parts of the implementation, or adjust its
working behavior. Third, when unexpected faults occur that the system cannot auto-recover from
(D), such as accidental deletion of critical files or termination of processes, the user may intervene
to recover manually. When escalated, the human provides targeted guidance or clarification rather
than fixing code directly; the system then continues autonomously.
   In practice, our system requires only 1 to 11 user interventions per program, each taking roughly
5 minutes to address. This enables long-running translations (28 to 90 hours) to proceed with
minimal supervision.
   Figure 4 shows simplified trajectories from the translation process, illustrating both automatic
recovery and user escalation. In (a), mujs FL15 , 𝑉 and 𝐻 handle all faults automatically. 𝐻 tracks
iterative progress as tests improve from 122/168 to 168/168, and 𝑉 performs multi-level validation—
checking both test results and code quality—before accepting the result. In (b), picoc FL15 and FL6.4 ,
the system encounters cases requiring escalation. A worker concludes that eliminating unsafe
code is “infeasible”; the user overrides this and provides an alternative approach. Later, the same
worker repeatedly claims completion despite 𝑉 pointing out that unsafe blocks remain (C.3); 𝐻
detects the loop and escalates. In FL6.4 , 𝑉 catches a test that was missing from the test runner,
preventing a false completion from going undetected.
8                         Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


Algorithm 1 The Reboot Translation Process
       Input: 𝐶 src (C program), 𝑇 (test suite)
       Output: RS src (safe Rust program)
       // Phase 1: Planning
    1: (plan, 𝐿) ← MAS_Plan(𝐶 src ,𝑇 )
            // 𝐿 = ⟨𝑙 0, 𝑙 1, . . . , 𝑙𝑛 ⟩: feature level IDs, sorted
       // Phase 2: Feature Reduction
    2: 𝐶 [𝑙𝑛 ] ← 𝐶 src ; 𝑇 [𝑙𝑛 ] ← 𝑇
    3: for 𝑖 = 𝑛 down to 1 do
    4:      (𝐶 [𝑙𝑖 −1 ], 𝑇 [𝑙𝑖 −1 ]) ← MAS_Reduction(𝐶 [𝑙𝑖 ],𝑇 [𝑙𝑖 ], plan, 𝑙𝑖 −1 )
       // Phase 3: Translation
    5: RS[𝑙 0 ] ← MAS_Translation(𝐶 [𝑙 0 ],𝑇 [𝑙 0 ], ∅)
    6: for 𝑖 = 1 to 𝑛 do
    7:      RS[𝑙𝑖 ] ← MAS_Translation(𝐶 [𝑙𝑖 ],𝑇 [𝑙𝑖 ], RS[𝑙𝑖 −1 ])
    8: return RS[𝑙𝑛 ]




3     The Reboot System
Reboot takes as input a C program together with a test suite, and produces a safe Rust program that
passes the same tests. The test suite is essential: it serves as the correctness criterion throughout
the translation process, and each intermediate result is validated against a corresponding test suite
(which is a subset of the C program’s test suite) before proceeding. The process is mostly automatic,
but occasionally the system pauses to request brief user guidance—typically a clarification or some
decision to be made—before continuing autonomously.

3.1     The Reboot Translation Process
Algorithm 1 presents the overall Reboot process. The process is organized into three phases,
each driven by a dedicated multi-agent system (MAS) sub-routine. In the Planning Phase (line
1), MAS_Plan analyzes the C program and produces a feature reduction plan together with an
ordered list of feature level identifiers 𝐿 = ⟨𝑙 0, 𝑙 1, . . . , 𝑙𝑛 ⟩. In the Feature Reduction Phase (lines 2–4),
MAS_Reduction is called iteratively to simplify both the program and the test suite one feature
level at a time, from the full program down to the minimal version at 𝑙 0 . In the Translation Phase
(lines 5–8), MAS_Translation first translates the simplest C program to Rust, then iteratively
restores features until reaching the full translation. The Planning Phase is the simplest of the three:
MAS_Plan executes a linear sequence of agent calls that read the source code, identify features,
determine their dependencies, and produce a plan document—with no iterative validation loop.
Summaries of the resulting feature level plans for each benchmark are provided in the appendix.
The remainder of this section focuses on MAS_Reduction and MAS_Translation, which employ
iterative multi-agent workflows.
   Each invocation of MAS_Reduction or MAS_Translation encapsulates a multi-agent system
that returns only after producing a validated artifact. The intermediate artifacts include: the feature
reduction plan produced by MAS_Plan, the simplified C programs 𝐶 [𝑙𝑖 ] and adapted test suites𝑇 [𝑙𝑖 ]
produced by MAS_Reduction, and the Rust translations RS[𝑙𝑖 ] produced by MAS_Translation.
Because each feature level is an independent, validated milestone, faults during the translation of
one feature level do not propagate to others.
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                                 9

                                                                                                    Initial
               INIT                                                             H                 allow={V}

                                                                                                   V
                                                                                                Prechecked
              Precheck      OK                                                   V         V       last=V
                                                                                                allow={W,V}


                                                                                                  W

                                     MORE_WORK                   MORE_WORK
                                                                                                Simplifying
                          Simplify                  Fix Issues                  W          W       last=W
                                                                                                allow={W,V}
                                        DONE                       DONE

                                                                                                   V            W

                                                    INVALID
                                                                                                   Validated
                                     Check Result                                V         V        last=V
                                                                                                allow={W,V,C}
                                                     VALID

                                                                                                   C


                                                                                                  Cleaned
                                                    Cleanup         END          C                 C seen
                                                                                                  allow={}

                                                                             Agent Roles

                         Workflow Diagram (MAS_Reduction)                                      FSM Guard


Fig. 5. Branch-level workflow control for the Simplification phase. Left: The workflow provided as instructions
to the manager agent, with task sequences and manager assessment outcomes. Right: FSM guard that enforces
valid worker sequences. Legend: Rounded boxes = Worker tasks; Black boxes = Manager assessments.


3.2   The Feature Reduction Sub-system
MAS_Reduction uses a multi-agent workflow with three workers—Simplifier (W), Validator (V),
and Cleanup (C)—coordinated by a Manager agent (marked as H in Figure 5). The Simplifier removes
all code that implements the features being dropped—i.e., features that should no longer exist in the
target feature level—and adapts the test suite accordingly. The Validator runs the adapted test suite
and checks that test coverage is preserved. The workflow has four stages: a precheck stage where
the Validator establishes baseline test coverage, a simplification stage where the Simplifier removes
the target feature, a validation stage where the Validator checks that all tests pass and coverage is
preserved, and a cleanup stage where Cleanup prepares the result for commit. Coverage serves as
an auxiliary sanity check on the reduction: we expect coverage to stay roughly the same after a
clean reduction, and a significant drop indicates either incomplete code removal while tests have
already been dropped, or accidental removal of tests that also cover remaining features. The main
loop is between simplification and validation: when validation finds issues, the Manager provides
feedback and routes back to the Simplifier to address them before re-validating.

3.3   The Translation Sub-system
MAS_Translation employs four worker agents coordinated by a Manager agent (marked as H in
Figure 6). The Translator (W) is the primary worker that produces Rust code from C, guided by
the previous level’s translation when available. The Validator (V1) runs the test suite and detects
cheating such as hardcoded return values or skipped tests. The CodeReviewer (V2) checks that
the translation uses safe Rust with no unsafe blocks, maintains code quality, preserves modular
structure, and double-checks whether the Validator’s results are correct. The Cleanup (C) prepares
the validated result for commit. The Manager decides which worker to call next based on their
status reports, and provides context, additional instructions, or hints to guide each worker.
   The workflow proceeds through four stages. In the setup stage, the Validator checks the test
infrastructure and validates the execution environment, making sure it is ready for the Translator.
10                              Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena

                                                                                                                                                  Initial
                   INIT                                                                                                  H                     allow={V1}

                                                                                                                                                V1
                                                                                                                                                  Setup
                  Setup       OK                                                                                         V1             V1       last=V1
                                                                                                                                              allow={W,V1}




                                        MORE_WORK                          MORE_WORK                         MORE_WORK                          W

            BLOCKED        Translate              BLOCKED      Fix-Trans               BLOCKED    Improve

                                                                                                                         W                     Translating
                                        DONE                               DONE                              DONE
                                                                                                                                        W         last=W
                                                                                                                                              allow={W,V1}

           Investigate    MORE_WORK                 Inv-Val   MORE_WORK                Inv-Rev   MORE_WORK


                                                                                                                                                V1                  W



                                                  INVALID
                                                                                                                                                 Validated
                                       Validate                                                                          V1        V1             last=V1
                                                                                                                                             allow={W,V1,V2}
                                                    VALID
                                                                                                                                                V2             V1
                                                                                                                                                               W
                                                               INVALID
                                                                                                                                                Reviewed
                                                    Review                                                               V2             V2       last=V2
                                                                                                                                                allow=all
                                                                VALID
                                                                                                                                                 C

                                                                                                                                                Cleaned
                                                               Cleanup      END                                          C                       C seen
                                                                                                                                                allow={}

                                                                                                                     Agent Roles

                                        Workflow Diagram (MAS_Translation)                                                                   FSM Guard


Fig. 6. Branch-level workflow control for the Translation phase. Left: The workflow provided as instructions to
the manager agent, with task sequences and manager assessment outcomes. Right: FSM guard that enforces
valid worker sequences. Legend: Rounded boxes = Worker tasks; Black boxes = Manager assessments.


In the translation stage, the Translator produces or updates the Rust code; when it encounters
complex issues, investigation sub-stages are triggered for deeper analysis before attempting fixes.
In the validation stage, the Validator runs tests to check equivalence with the C program, and the
CodeReviewer checks code quality; both must pass before proceeding. In the cleanup stage, the
result is prepared for commit. The main loop is between translation and validation: when either
test validation or code review finds issues, the Manager routes back to the Translator to address
them, then re-validates.
   The multi-agent design described above implements the conceptual framework from Section 2.
The Validator and CodeReviewer together realize the validity mechanism 𝑉 , checking correctness of
outputs independently of the primary worker’s claims. The Manager realizes the history-feedback
mechanism 𝐻 , analyzing the history of worker attempts and providing targeted feedback to guide
progress. This mapping holds uniformly across both MAS_Reduction and MAS_Translation,
with the Simplifier or Translator serving as the primary worker whose outputs are supervised by
𝑉 and 𝐻 .

3.4   Detection and Handling of Faults
While the Manager (H) makes autonomous decisions about which worker to call next, a rule-
based controller further enforces safety constraints on the worker call sequence. These constraints
are expressed as finite state machines (FSMs), shown in Figures 5 and 6. Key invariants include:
validation must occur before code review, code review must occur before cleanup, and no further
work is permitted after cleanup. If the Manager proposes a worker call that violates these constraints,
the controller rejects the call and prompts the Manager to reconsider. Together, the Manager and the
controller implement the history-feedback mechanism 𝐻 from Section 2.2: the Manager provides
feedback based on agent history, and the controller enforces structural invariants.
   As described in Section 2.2, the system escalates to a human when repeated retries yield no
progress, when the worker claims the objective is INFEASIBLE, or when unexpected faults cannot
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                      11

be automatically recovered. At the implementation level, the Manager tracks consecutive retry
counts for each stage and escalates after a configurable number of rounds (typically 5–10) without
progress.

4   Implementation
LLM and Agent. We implement Reboot using Claude Code (version 2.0.25) as the agent framework,
with Claude Sonnet 4.5 as the underlying language model. Each agent—Translator, Simplifier,
Validator, CodeReviewer, Cleanup, and Manager—is an instance of Claude Code configured with role-
specific prompts and permissions. Claude Code provides built-in capabilities for file manipulation,
command execution, and iterative refinement, which we leverage for code generation and validation
tasks.
Agent Prompting. The system uses approximately 30 prompt files in markdown, organized
by worker role and by phase. For planning, a sequence of prompts guides the agent through
feature identification, dependency analysis, and ordering to produce the feature reduction plan.
For reduction and translation, each worker role has per-stage prompt files: translation instructions
for the Translator, validation criteria for the Validator, and a review checklist for the CodeReviewer.
The Manager is instructed to follow the workflows shown in Figures 5 and 6, and to analyze worker
status reports and provide targeted feedback accordingly.


                                                                L3               User
                                  L3
                                                           User Delegator     Final Decision
                            Phase Controller                                      Maker
                                                               Agent



                                                                              Instruction
                                                                L2
                                  L2                                          Report
                                                             Manager
                           Branch Controller                 Agent (H)
                                                                              Escalate/Err

                                                                              Docker Sandbox


                                                  L1             L1
                                                                             L3: Phase Ctrl
                               L1
                         Worktree Helper        Worker         Worker        L2: Branch Ctrl
                         Sandbox Helper        Agent (W)    Agents (V1/V2)   L1: Code Editing



Fig. 7. Three-level implementation architecture of Reboot. The L3 Phase Controller is long-lived and manages
the overall three-phase process. L2 components (Branch Controller and Manager Agent) are created for each
feature level. L1 Worker Agents persist for the duration of that feature level to handle multiple tasks, and
get restarted when faulty. When the Manager escalates an issue, it reaches the User Delegator Agent at L3,
which auto-resolves common patterns and forwards only unresolved cases to the human user.


System Architecture. Figure 7 shows the three-level architecture. At L3 (phase level), the Phase
Controller drives the overall process from Algorithm 1, iterating over feature levels and invoking
the appropriate MAS operator for each transition. Also at L3, the User Delegator Agent intercepts
escalations from the Manager before they reach the human user, auto-resolving common patterns
such as output format mismatches, transient API errors, and iteration-limit resets. At L2 (branch
level), a Branch Controller and a Manager Agent are created for each feature-level transition; the
Branch Controller proxies messages between agents, enforces the FSM guards from Section 3, and
manages git worktrees. At L1, Worker Agents (Translator, Simplifier, Validator, CodeReviewer,
12                   Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


Cleanup) operate within the worktree for that branch. Communication flows downward as instruc-
tions (blue), upward as reports (green), and upward as escalations (red) when 𝐻 cannot resolve an
issue automatically, or as errors (red) when an agent or a controller is failing.
Sandboxing and Isolation. Each agent runs in its own Docker container with restricted permis-
sions. The Manager agent has read-only access to the codebase, consistent with its role as 𝐻 —it
observes and analyzes but does not modify code directly. Worker agents (Translator, Simplifier,
Validator, CodeReviewer, Cleanup) have read/write access only to the worktree folder for their
current branch, plus read-only access to the git repository. The control infrastructure—branch-level
and repo-level controllers—runs on the host outside the agent containers, ensuring that agents
cannot interfere with orchestration logic. All agent logging is also performed on the host, preventing
agents from tampering with their own logs.
Git-based State Management. Git worktree management runs on the host, not inside agent
containers. A separate git branch is created for each feature level transition, isolating work across
different levels. The system auto-commits tracked files after each agent step, providing backups of
intermediate progress. After validation and review pass, a cleaned-up final commit is created for
each branch. These backups enable recovery when failures occur: if some files are corrupted, the
Manager can instruct the worker to retrieve previous versions from backup commits and continue
(soft recovery); if the worktree is not recoverable after escalation, the system can roll back to the
last good commit or reset to the previous feature level’s branch (hard recovery).
System Size. The main Reboot system comprises approximately 6k lines of Python code: ∼2k for
the branch-level controller, ∼1k for the repo-level controller, and ∼2k for worktree-level helper
scripts. In addition, approximately 30 prompt files in markdown define the instructions for each
worker role and phase. Auxiliary scripts for sandboxing, environment setup, and result analysis
add another ∼5k lines of code.

5    Evaluation
We evaluate Reboot on four research questions:
      • RQ1 (Effectiveness): Can Reboot produce safe Rust translations of real-world C interpreter
        programs that pass a given test suite?
      • RQ2 (Efficiency): How much time, cost, and human effort does the translation require?
      • RQ3 (Correctness beyond provided tests): To what extent do the Rust translations pass
        unseen validation tests?
      • RQ4 (Comparison with existing approaches): How does Reboot compare with existing
        C-to-Rust translation tools?
We also conduct five case studies: security improvements in the translated code (CS1), runtime
performance of the translations compared with the original C programs (CS2), an ablation study
on the benefits of feature reduction (CS3), user interventions required during translation (CS4),
and the applicability of Reboot to command-line programs beyond interpreters (CS5).
Benchmarks. Table 2 lists the six open-source projects, which are interpreters written in C used in
our evaluation. We identified candidates by searching for popular open-source interpreter projects
written in C, and selected those that are standalone (can be compiled and tested independently)
and free of complex external dependencies. The programs range from ∼6k to ∼23k lines of code,
interpreting diverse source languages including Awk, JavaScript (ES5), a C subset, an arbitrary-
precision calculator language, Wren, and a Python subset. Some programs come with their own
test suites, while others have limited test coverage; for the latter, we supplemented additional tests
to ensure all benchmarks achieve at least 70% line coverage on the C source. These provided tests
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                       13

are the tests that Reboot uses during translation; correctness of the final translation is measured
by passing all of them.

                             Table 2. Benchmark interpreter programs written in C.

                  Program        LoC     #Tests   Coverage Description
                  awk           6,332       279           74% One True Awk Interpreter
                  gnu-bc        7,525       134           85% Arbitrary Precision Calculator
                  picoc         8,486       154           81% C Subset Interpreter
                  wren          8,325       851           88% Wren Language Interpreter
                  mujs         17,090       187           88% JavaScript Interpreter (ES5)
                  pocketpy     23,271        83           81% Python Subset Interpreter


Setup. Each program is translated end-to-end using Reboot with the implementation described in
Section 4 (Claude Code with Claude Sonnet 4.5). Each result represents a single translation run; we
do not perform repeated experiments due to the relatively high monetary cost. When the system
escalates to a human (Section 2), one of the authors handles the escalation as the human-in-the-loop.
We measure wall-clock translation time (the system’s total running time, excluding time spent
waiting for the user during escalations), monetary cost (LLM API usage), and the number of user
interventions required. To evaluate correctness beyond the provided tests, we independently created
validation test suites for each program; these tests were hidden from Reboot during the entire
translation process.

5.1   RQ1 & RQ2: Effectiveness and Efficiency
Table 3 summarizes the results for all six programs. The Provided Tests column reports whole-
program test files fully passing (one test file may contain multiple individual tests). All six transla-
tions succeed: each produces a safe Rust program (with no unsafe blocks) that passes 100% of the
provided tests.

                                     Table 3. Summary of Translation Results.

                           User Source Translated                   Provided Translation          Cost
      Program     Interventions C LoC   Rust LoC                       Tests       Time          (USD)
      awk                   1 (+2)       6,332           9,514 279/279 (100%)          36.0h    $713.62
      gnu-bc                     1       7,525           6,784 134/134 (100%)          27.7h    $463.46
      picoc                 4 (+1)       8,486          14,259 154/154 (100%)          46.2h    $971.04
      wren                       8       8,325          12,191 851/851 (100%)          46.2h    $949.83
      mujs                       4      17,090          16,235 187/187 (100%)          44.8h    $957.75
      pocketpy             11 (+1)      23,271          24,348   83/83 (100%)          90.5h   $1781.79


   The Rust translations have comparable size to the C source, with four of six programs having the
translated Rust code larger than C. Translation time ranges from ∼28 to ∼90 hours, and monetary
cost ranges from ∼$460 to ∼$1,780 per program. Human effort is modest: programs require 1 to 11
user interventions, each taking roughly 5 minutes (the “+𝑛” annotations indicate minor system
recovery actions—restarting a hanging agent or correcting a message format error—that take
seconds, could be eliminated by a more robust system implementation, and are not counted as
interventions).
14                      Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena




             (a) awk                               (b) picoc                             (c) mujs




           (d) gnu-bc                              (e) wren                            (f) pocketpy

Fig. 8. Code size comparison across feature levels. The charts show lines of code (LoC) growth as features
are incrementally added, comparing the C reduced versions (during source reduction phase) with the Rust
translations (during translation bootstrapping phase).



   Figure 8 shows the lines of code across feature levels for both the C reduced versions and the
Rust translations, illustrating how code size evolves through the translation process. Figure 9 shows
the monetary cost breakdown by activity, illustrating how LLM costs are distributed across the
translation process.

5.2   RQ3: Correctness beyond the Provided Tests
As described in the setup, we created validation test suites for each program independently of the
provided tests. These validation tests were created by the authors independently of and separately
from the provided test suites, and were never exposed to the system during translation; we therefore
consider them “unseen” tests. One of the authors spent approximately 10–20 hours per program
creating each suite. The process involved studying the program’s supported features and usage,
manually writing around 10 seed test programs (interpreter inputs), then semi-automatically
expanding coverage with the help of a coding agent, and manually vetting that all generated tests
produce correct expected outputs by running them on the original C program. Most suites achieve
relatively high line coverage on the translated Rust code (78.79% on average); pocketpy’s suite has
lower coverage (62.98%) due to more limited effort given the program’s size and complexity. The
validation tests were run on the final Rust translations only after the entire translation process
was complete. Table 4 presents the validation results. Pass rates on the unseen validation tests
range from ∼62% to ∼92%, with wren achieving the highest (91.78%, 134/146) and pocketpy the
lowest (61.58%, 125/203). The validation test suites achieve an average of 78.79% line coverage on
the translated Rust code (ranging from 62.98% to 84.85%).
   For mujs, we additionally evaluated on the official ECMA-262 ES5 conformance suite (Test262),
which contains ∼11,725 tests in total. The original mujs C source conforms on 9,853 of these tests;
we refer to this subset as Test262@mujs. The safe Rust translation produced by Reboot passes 8,268
out of those 9,853 tests in Test262@mujs (83.91%).
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                       15




              (a) awk                               (b) picoc                           (c) mujs




            (d) gnu-bc                                  (e) wren                      (f) pocketpy

Fig. 9. Cost breakdown by activity across six interpreter programs. The pie charts show the distribution of
monetary costs across different phases, with the inner ring representing common categories (Management,
Reduction, Translation, CodeReview, TestValid, Commit, Additional) and the outer ring showing language-
specific breakdown (C vs Rust activities).

Table 4. Pass rates on provided tests used for the translation and on the validation tests post-translation.

                    Translated              Provided               Validation   Validation
                  Rust Program                 Tests                    Tests Test Cov. (C)
                  wren                851/851 (100%)        134/146 (91.78%)         82.73%
                  awk                 279/279 (100%)        160/203 (78.82%)         79.63%
                  gnu-bc              134/134 (100%)         99/126 (78.57%)         80.31%
                  mujs                187/187 (100%)        163/218 (74.77%)         84.85%
                  picoc               154/154 (100%)        139/200 (69.50%)         82.24%
                  pocketpy              83/83 (100%)        125/203 (61.58%)         62.98%


5.3   RQ4: Comparison with Existing Approaches
We compare Reboot with four existing C-to-Rust translation approaches: 1) C2Rust [22], an
industrial grade rule-based translator, 2) CROWN [57], a rule-based translator that refines the
output of C2Rust using a novel symbolic ownership analysis to rewrite raw pointers to safe Rust
references, 3) C2SaferRust [34], a neuro-symbolic translator that refines the output of C2Rust using
LLMs rather than a symbolic analysis, and 4) SmartC2Rust [43], a neuro-symbolic translator that
16                    Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


Table 5. Comparison of Reboot, C2Rust, and Crown on the six benchmarks. Reboot produces safe Rust with
no unsafe blocks and no raw pointers, whereas C2Rust output is far larger and almost entirely raw-pointer
based. Results from Crown are similar. Pointer declaration counts are syntactic approximations.

                               Rust LoC               Raw pointer decls               Tests passing
 Program    C LoC    Reboot     C2Rust    Crown    Reboot    C2Rust Crown       Reboot C2Rust         Crown
 awk         6,332     9,514     28,215   27,526         0     2,327    1,903   279/279   279/279   279/279
 gnu-bc      7,525     6,784     18,519   17,538         0     1,199      879   134/134   134/134   134/134
 picoc       8,486    14,259     28,930   23,127         0     5,722    3,489   154/154     0/154     0/154
 wren        8,325    12,191     22,156   19,964         0     3,366    2,534   851/851   851/851   851/851
 mujs       17,090    16,235     46,002   39,282         0     5,158    2,784   187/187   184/187   184/187
 pocketpy   23,271    24,348     97,354   83,163         0     7,701    5,608     83/83     83/83     83/83




combines program analyses and program rewriting with an LLM to perform translation. CROWN
and SmartC2Rust are representative state-of-the-art rule-based and neuro-symbolic translators,
respectively, based on the number and size of C programs they are demonstrated to successfully
translate.
   We first run C2Rust and CROWN on our benchmark programs. The results are summarized in
Table 5. On four of our six programs, both tools achieve 100% test pass rates. On the remaining two
programs, they achieve only 98% and 0% pass rates because of runtime errors related to how C2Rust
(and therefore CROWN) handles variable-length structs (the C flexible-array-member idiom). We
also see that rule-based translations are 2×–4× larger than the C source and make heavy use of raw
pointers, while Reboot’s translations stay close to the original size and are fully safe. We further
note that some manual work is needed to make C2Rust (and CROWN) work on our programs.
Wee need to make changes to the build process for each program to produce per-file compilation
databases and disable an unsupported GNU C extension (computed goto), and post-process the Rust
output to fix errors including incorrect atomic types, missing extern declarations, and duplicate
symbol exports. In addition, CROWN’s ownership analysis could not handle pointer-carrying
tagged unions present in all of our programs, so we had to disable part of CROWN’s algorithm in
order to successfully run it.
   We also attempted to apply SmartC2Rust [43] to our benchmark programs. SmartC2Rust is a
recent and capable neuro-symbolic system that pairs LLM-based translation with program analysis,
and it has been evaluated on C programs of up to around 4k lines, which is smaller than our
interpreters (∼6k–23k LoC). We spent more than five days trying to run it on our programs, but
have so far been unable to translate any program end-to-end. We observed a few recurring issues.
A large number of files in the project tree, or a very long input file, could cause the pipeline to crash
while composing its prompts. The automatic patching of the program’s main function also appeared
unstable when the interpreter’s main is complex. After multiple attempts on awk, we obtained
roughly a third of the functions translated and compiling, but most functions remained untranslated
and the program as a whole was not executable. We are unsure whether these issues are fundamental,
a matter of implementation robustness, or violations of implicit assumptions of the tool that we
were not aware of. The SmartC2Rust implementation is also substantial, reaching 37k lines of
code. Its size, together with the number of rule-based analysis components it integrates, made it
challenging for us to diagnose the issues we encountered with the pipeline. Similar phenomena
with implementation complexity have been reported for other LLM-based translation systems [21].
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                         17

5.4   CS1: Security Improvements
Among our benchmark programs, mujs has 30 documented CVEs in its history, making it a good
candidate for evaluating security improvements. We re-introduced 20 of these CVEs into the latest
mujs codebase to create a vulnerability-concentrated benchmark we call mujs-CVEs. The remaining
10 CVEs could not be re-introduced because they are no longer applicable in the latest codebase or
conflict with later CVEs. The 20 CVEs span a range of error types: heap buffer overflow (6), heap
use-after-free (3), stack exhaustion (3), integer overflow (2), bytecode logic error (2), null pointer
dereference (1), out-of-bounds read (1), stack buffer overflow (1), and global buffer overflow (1).
   We translated mujs-CVEs using Reboot and ran the original proof-of-concept (PoC) inputs for
each CVE on both the C and safe Rust builds. We also manually reviewed the vulnerable C code
and corresponding Rust translation for each CVE to assess whether the vulnerability was truly
eliminated, merely mitigated (memory corruption gone but replaced by a different-class failure),
or survived; the results are reported in the Status column of Table 6, with a detailed per-CVE
breakdown in the appendix. The error categories used in Table 6 are:
• Memory safety violations (C only): Heap-UAF (use-after-free), Heap-BOF / Stack-BOF / Global-
   BOF (buffer overflow), NULL-Deref (null pointer dereference), OOB-Read (out-of-bounds read
   from undefined behavior), and Int-Overflow (integer overflow leading to memory corruption).
   These cannot occur in safe Rust.
• Logic and algorithmic errors (C and Rust): Stack-Exhaust (unbounded recursion) and Bytecode-
   Logic (bytecode compiler logic errors that do not cause memory corruption).
• Rust observed behaviors: Clean (no error), Exit-Nonzero (controlled error exit), Exception
   (JS-level uncaught exception), Panic (Rust safety check, e.g. overflow detection), Abort (OOM or
   fatal runtime error), and Stack-Exhaust (stack exhaustion crash).

Table 6. Results on Reproduced CVEs in the C (mujs-CVEs) vs. its Safe Rust Translation. The Status column
reflects the manual assessment: Eliminated (memory safety violation removed), Mitigated (memory corruption
gone but replaced by a different kind of crashes), or Unmitigated (same vulnerability class persists). All Rust
code passes as safe Rust with no unsafe blocks.

         CVE                 Error in C        Rust O0 (Debug)   Rust O3 (Release)     Status
         CVE-2022-44789      Heap-UAF          Clean             Clean                 Eliminated
         CVE-2021-33796      Heap-UAF          Clean             Clean                 Eliminated
         CVE-2020-24343      Heap-UAF          Exception         Exception             Eliminated
         CVE-2019-12798      Heap-BOF          Stack-Exhaust     Stack-Exhaust         Mitigated
         CVE-2016-10141      Heap-BOF          Abort             Abort                 Mitigated
         CVE-2016-10133      Heap-BOF          Stack-Exhaust     Stack-Exhaust         Mitigated
         CVE-2016-9136       Heap-BOF          Exit-Nonzero      Exit-Nonzero          Eliminated
         CVE-2016-9109       Heap-BOF          Exit-Nonzero      Exit-Nonzero          Eliminated
         CVE-2016-7506       Heap-BOF          Clean             Clean                 Eliminated
         CVE-2019-11411      Stack-BOF         Clean             Clean                 Eliminated
         CVE-2018-6191       Global-BOF        Clean             Clean                 Eliminated
         CVE-2017-5628       OOB-Read          Clean             Clean                 Eliminated
         CVE-2016-9294       NULL-Deref        Clean             Clean                 Eliminated
         CVE-2021-33797      Int-Overflow      Clean             Clean                 Eliminated
         CVE-2016-9108       Int-Overflow      Panic             Clean                 Mitigated
         CVE-2021-45005      Bytecode-Logic    Clean             Clean                 Eliminated
         CVE-2019-11412      Bytecode-Logic    Clean             Clean                 Eliminated
         CVE-2022-30974      Stack-Exhaust     Stack-Exhaust     Stack-Exhaust         Unmitigated
         CVE-2019-11413      Stack-Exhaust     Exit-Nonzero      Exit-Nonzero          Eliminated
         CVE-2018-5759       Stack-Exhaust     Clean1            Clean1                Unmitigated
18                      Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


Table 7. CVE elimination factors across the 18 eliminated or mitigated CVEs. Each factor may appear as the
primary cause or as a contributing factor. PanicOnOverflow and BetterLogic are grouped as Other.

     Factor         Count Examples                                                           Primary Contrib.
     Architecture       6 GC redesign (Rc<RefCell<>>), stack-based labels, local Vec han-          5        1
                          dler storage, scope-based LoopContext
     TypeSafety         5 Option<u8> forces EOF handling, usize prevents negative index,           2        3
                          defined NaN-to-int cast semantics, usize overflow to large value
     Bounds             4 Vec/slice bounds checking on advance(), explicit i+1 < len               1        3
                          guards
     API                3 format!() replaces sprintf, str::parse::<f64>() replaces                 3        0
                          custom number parser
     Ownership          2 Owned Property clone, String clone of regexp source                      2        0
     Other              2 Debug-mode i32 overflow detection (PanicOnOverflow); trans-              2        0
                          lated code has additional depth check (BetterLogic)



   Table 6 shows the results, comparing the behavior of the C and Rust code. We report on both
debug (O0) and release (O3) builds, since compiler optimizations can cause different runtime
behavior. Of the 20 CVEs, 14 are eliminated, 4 are mitigated, and 2 are unmitigated in the Rust
translation that compiles as safe Rust (has no unsafe blocks). We explain their breakdown next.
   All memory safety vulnerabilities—heap buffer overflow, heap use-after-free, stack buffer overflow,
global buffer overflow, null pointer dereference, and undefined-behavior-induced out-of-bounds
access—are either eliminated or mitigated: the Rust program either runs cleanly, exits gracefully, or
fails with a different-class error (stack exhaustion or OOM) rather than memory corruption. The
2 unmitigated CVEs are both denial-of-service vulnerabilities that cause stack exhaustion from
unbounded recursion. These are retained in safe Rust, which is expected since Rust has a finite
stack as well. One CVE worth noting is CVE-2016-9108 (integer overflow), where Rust panics in
debug mode but wraps silently in release mode; this difference is not undefined behavior but rather
an intentional design choice in Rust, where debug builds check for integer overflow while release
builds wrap for performance reasons—both are defined behavior in safe Rust. In general, Rust also
provides more principled error handling, and we observe several cases where PoC inputs that
caused memory corruption in C instead produce controlled error exits in the Rust translation, such
as Option-forced EOF handling and Result-based error propagation that convert malformed inputs
into clean SyntaxError exits. Table 7 summarizes the Rust features responsible for eliminating or
mitigating the 18 applicable CVEs. Architectural redesign, type safety, bounds checking, safe APIs,
and ownership/borrow-checking of references all contribute, often in combination. For example,
C mujs uses a manual mark-and-sweep garbage collector; the Rust translation replaces it with
Rc<RefCell<>> reference counting, which eliminates an entire class of GC algorithm bugs (e.g.,
CVE-2020-24343) at the cost of not collecting reference cycles—a standard tradeoff when memory
leaks are acceptable.

5.5     CS2: Performance
For each program, we invoke its test suite using a harness that runs the target binary once per test
case, measuring wall-clock time from process start to process end (excluding the harness overhead
but including the binary loading time when the process is started by the OS). Each test case is
repeated 5 times and averaged. We report two aggregates: the total time across all test cases, and the
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                      19




         (a) Total Runtime Comparison                      (b) Median Test Case Runtime Comparison

Fig. 10. Performance evaluation results comparing C baseline with Rust (Reboot) implementations. All
measurements use O3 optimization level. C baseline is normalized to 100%. Results show that our Rust
translations achieve competitive performance, with total runtime ranging from 116.1% to 261.7% relative to C
across all projects.


median taken across all per-test-case times (so that a few slow-running tests do not dominate the
summary). Figure 10 compares the execution time of the original C programs (compiled with -O3)
and the translated safe Rust programs (compiled with -O3) on the provided test suites, reporting
both total runtime and the median across per-test-case runtimes, as percentages relative to the
C baseline. 5 of the 6 programs show a median per-test slowdown, ranging from 1.28x to 1.51x
relative to C. In terms of total execution time across all test cases, the overhead ranges from 1.16x
to 2.62x. Overall, the translated Rust programs achieve performance that is not too far from the
original C implementations. Detailed per-program numbers including debug builds are provided in
the appendix.
   We note that our translation makes no effort to further optimize the Rust code. Nevertheless, the
overhead is already comparable to that reported by full memory safety enforcement for C [31, 32],
dynamic taint analysis tools [39], and address sanitizers [40] that instrument C code directly.

5.6   CS3: Ablation on Feature Reduction
To evaluate the contribution of feature reduction, we compare two configurations: Reboot, which
uses feature reduction together with the multi-agent system (MAS) as described in the previous
sections, and Reboot w/o Feat.Red., which uses only the MAS to translate the full program directly
without feature reduction (i.e., a single feature level). Both configurations use the same MAS
implementation, almost identical prompts (except for a clarification that only one feature level
is expected), and the same LLM; the only difference is whether the translation is decomposed
through feature reduction. We compare the two configurations on all six of our main benchmark
programs (mujs, awk, picoc, gnu-bc, wren, and pocketpy), as well as mujs-CVEs (the vulnerability-
concentrated variant from CS1).
   Table 8 presents the ablation results. Reboot passes 100% of the provided tests for all six programs.
For the five programs where the configuration without feature reduction completed, it passes nearly
all provided tests (99% for gnu-bc and picoc; 100% for the rest), indicating that the MAS alone
is largely sufficient to produce translations that pass the provided test suites. However, feature
reduction consistently improves pass rates on the unseen validation tests: mujs 74.77% vs. 65.6%,
picoc 69.50% vs. 49.0%, awk 78.82% vs. 71.9%, and gnu-bc 78.57% vs. 67.5%. There are also significant
improvements in correctness on the mujs Test262 conformance suite: Reboot achieves 83.91%
20                       Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


Table 8. Ablation Study: Reboot (feature reduction + MAS) vs. Reboot w/o Feat.Red. (MAS only).∗ Starred
entries require minor test harness fixes before the translation can pass any tests; the reported numbers are
after applying these fixes. † Both pocketpy attempts without feature reduction failed to complete due to
manager failures (see text).

 Program      Configuration                 Time    UserInt.   Provided Tests    Validation Tests       Test262@mujs
 mujs         Reboot                        44.8h         4     187/187 (100%)    163/218 (74.77%) 8,268/9,853 (83.91%)
 mujs         Reboot w/o Feat.Red.          52.6h        12     187/187 (100%)    143/218* (65.6%) 3,538/9,853* (35.91%)
 mujs-CVEs    Reboot                        58.0h         4     187/187 (100%)     170/218 (78.0%) 7,554/9,853* (76.67%)
 mujs-CVEs    Reboot w/o Feat.Red.          28.0h         1     187/187 (100%)     144/218 (66.1%) 2,835/9,853 (28.77%)
 awk          Reboot                        36.0h         1     279/279 (100%)    160/203 (78.82%)                    –
 awk          Reboot w/o Feat.Red.          34.6h         6     279/279 (100%)     146/203 (71.9%)                    –
 picoc        Reboot                        46.2h         4     154/154 (100%)    139/200 (69.50%)                    –
 picoc        Reboot w/o Feat.Red.          19.2h         2      152/154 (99%)      98/200 (49.0%)                    –
 gnu-bc       Reboot                        27.7h         1     134/134 (100%)     99/126 (78.57%)                    –
 gnu-bc       Reboot w/o Feat.Red.          35.5h         6      133/134 (99%)      85/126 (67.5%)                    –
 wren         Reboot                        46.2h         8     851/851 (100%)    134/146 (91.78%)                    –
 wren         Reboot w/o Feat.Red.          80.7h        13     851/851 (100%)     125/146 (85.6%)                    –
 pocketpy     Reboot                        90.5h        11       83/83 (100%)    125/203 (61.58%)                    –
 pocketpy     Reboot w/o Feat.Red.† (1st)    5.4h         0        11/83 (13%)      30/203 (14.8%)                    –
 pocketpy     Reboot w/o Feat.Red.† (2nd)   19.8h         2        50/83 (60%)      99/203 (48.8%)                    –




compared to 35.91% without feature reduction, and the mujs-CVEs variant shows a similar pattern
(76.67% vs. 28.77%). These results suggest that feature reduction leads to higher-quality translations
that generalize better beyond the provided tests, likely because decomposing the translation
into smaller, validated milestones allows translation details to be more carefully handled at each
transition.
   For pocketpy, the largest benchmark (∼23k LoC), the configuration without feature reduction
failed to produce a working translation in two separate attempts. In the first attempt, the Translator
initially circumvented the task by invoking the original C binary instead of producing a genuine
translation; after being caught, the Manager began guiding the actual translation but later assessed
the task as too complex and declared it as failed—invoking a fail-early mechanism available to
the Manager in all configurations but never triggered in any other run. We then disabled this
mechanism and made a second attempt. This time, unable to give up, the Manager instead stopped
following its runbook and began sending modified instructions to the Validator and CodeReviewer
that requested validation of only the already-passing tests—satisfying the FSM guard’s structural
requirements while bypassing actual validation. After the workflow finishes, our ablation con-
figuration automatically reruns the entire translation and validation with a fresh Manager as a
double-checking mechanism, but the same manipulation occurred in the double-checking run
as well. These failures illustrate a breakdown of the assumption from Section 2.2 that 𝐻 is itself
reliable: when the objective becomes too complex for the worker, the Manager—which implements
𝐻 —also becomes unreliable, resorting to shortcuts or giving up. Feature reduction mitigates this by
keeping each objective small enough that 𝐻 remains effective, suggesting that feature reduction
may become more important as program complexity grows.

5.7      CS4: User Interventions
As reported in Table 3, the number of user interventions ranges from 1 to 11 per program, each
taking roughly 5 minutes. All interventions are in the form of natural language guidance provided
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                 21

to the Manager agent; the user does not write or modify code directly. We classify the 29 observed
interventions into four categories:
      • Task clarification (10 cases): The user clarifies what the task expects. Examples include
        informing the Manager that a coverage drop during feature reduction is not acceptable, and
        clarifying that task success requires 100% test passage rather than partial results.
      • Workflow clarification (7 cases): The user clarifies workflow expectations or non-negotiable
        requirements, such as instructing the Manager to continue without round limits as long as
        progress is being made, or confirming that CodeReviewer concerns on code quality must be
        addressed before proceeding.
      • Agent misbehavior correction (6 cases): An agent goes off-track despite 𝐻 ’s attempts to
        correct it. Examples include a Validator in mujs that removed 21 tests instead of syncing
        them, and a Translator in wren that stalled for three consecutive rounds producing analysis
        instead of code.
      • Design decisions (3 cases): The user makes a design choice that the system cannot resolve
        on its own, such as deciding which unsafe POSIX APIs to drop versus wrap with safe crates
        in picoc.
The remaining 3 interventions are system-level issues (agent timeouts or token limits) resolved by a
lightweight restart. Besides design decisions, the other categories represent limitations of the current
prompt design and iteration logic that could in principle be addressed by refining the Manager’s
instructions or the escalation-handling templates. Notably, these 29 interventions represent only a
fraction of the situations the system must handle. When the Manager escalates an issue, it is first
intercepted by the User Delegator Agent (Figure 7), which acts on behalf of the user for common
escalation patterns such as output format mismatches, transient API errors, and iteration-limit
resets. Across all six programs, 125 escalations were raised; the User Delegator auto-resolved 96 of
them (77%), forwarding only 29 to the human user. In addition, 4 minor system recovery actions
(restarting a hanging agent or correcting a message format error) occurred across three programs;
these are lightweight operations (taking seconds) and are not counted as interventions (shown as
“+𝑛” in Table 3). Detailed per-program intervention logs, including verbatim user messages, are
provided in the appendix.

5.8    CS5: Applicability Beyond Interpreters
Feature reduction is natural for interpreters, where progressively reducing the input language
yields a sequence of smaller, self-contained languages, and where the heavily cross-cutting, stateful
data flow of an interpreter makes whole-program decomposition valuable. However, nothing in
Reboot’s system design restricts it to interpreters; only the prompts are interpreter-specific and
assume the input is an interpreter. To probe whether Reboot applies more broadly, we ran it
on two command-line utilities, tail and split , from the coreutils-based benchmark used by
C2SaferRust [34]; both are among the larger CLI programs in that suite. We made minor adjustments
to the prompts for these non-interpreter inputs but changed nothing in the system implementation.
Reboot translated each program to safe Rust with no unsafe blocks, passing all provided tests
(Table 9). The translations stay close to the size of the C source, whereas C2Rust-derived pipelines
such as C2SaferRust produce larger output that retains some unsafe constructs, consistent with
its goal of reducing rather than eliminating unsafe. These two programs are only a preliminary
probe, but they indicate that Reboot is not fundamentally tied to interpreters.
   Reboot could in principle also target libraries, since a library can be wrapped in a command-line
driver to provide the end-to-end tests that Reboot relies on. The benefit of feature reduction
2We directly use their reported result which mentions that all tests are passing.
22                    Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


Table 9. Reboot on two command-line utilities from C2SaferRust’s benchmark. Reboot produces safe Rust
with no unsafe blocks; the C2SaferRust columns are shown for reference.

                              Rust LoC                Raw pointer decls               Tests passing
 Program     C LoC    Reboot C2SaferRust           Reboot      C2SaferRust      Reboot      C2SaferRust
 tail          1758        2,511           11663           0              297     462/462             All2
 split         1349        2,163           11324           0              214     179/179              All


would be smaller in this setting, however. We observe that many libraries have largely independent
functions and features and carry far less of the cross-cutting, stateful data flow found in interpreters,
so decomposing by feature would largely coincide with decomposing by syntactic units such as
functions and modules. In that regime, feature reduction essentially reduces to the syntactic
decomposition that existing work, such as SmartC2Rust [43], has already shown to be effective.

6    Threats to Validity
Nondeterminism and Reproducibility. Coding agents such as Claude Code are inherently
nondeterministic [13], so a different run of Reboot on the same program may produce a different
translation, different validation pass rates, and a different number of user interventions. We fix the
version of Claude Code and ensure that every agent call is started in an identical clean sandbox
with identical configurations. However, this is insufficient for achieving determinism in practice.
One might propose request caching, but even if the API endpoint is made deterministic, external
factors such as script execution timing and timestamps in tool call results can invalidate caches
in reruns, causing the agent to diverge from a previous trajectory. The natural mitigation is to
perform repeated runs, but this is presently impractical given the high monetary cost ($460–$1,780
per program) and wall-clock time (28–90 hours per program). Instead, we provide the full agent
logs for all translations, enabling inspection of the complete translation process and the decisions
made at each step.
Human-in-the-Loop Variability. One of the authors served as the human-in-the-loop for all
escalations across all six programs. A user less familiar with the system might handle escalations
differently, primarily affecting efficiency—for example, requiring more time to understand the
escalation context or needing more intervention rounds to resolve an issue. For the small number of
design decisions (3 out of 29 interventions), a different user might make different choices, producing
different translated code; we view this as an inherent aspect of translation, where multiple valid
designs exist, rather than a quality concern. In all cases, the user provides only natural language
guidance and does not write or modify code directly.
Validation Tests and Correctness Measurement. The validation test suites were created by
the authors, which introduces potential for bias. We mitigate this by creating these test suites
ahead of time, before examining any translation output, independently of and separately from the
provided tests used during translation. While these tests may not be comprehensive, they serve as
an independent measure of correctness beyond the provided tests. Using a different test suite may
yield different pass rates and different magnitudes of improvement from feature reduction. For
instance, both our validation tests and the Test262 conformance suite show that feature reduction
improves correctness for mujs, but the gap differs substantially (74.77% vs. 65.6% on validation tests;
83.91% vs. 35.91% on Test262). A potential reason might be that our validation tests were created in
a relatively short time with less effort compared with a comprehensive conformance suite, so the
majority of the tests might be relatively easier to pass; both configurations can handle many of
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                 23

them, and the observed improvement gap is smaller than on a more comprehensive suite. More
broadly, correctness in this work is defined by passing tests; the translations may have semantic
differences from the original C programs that are not captured by any test suite.
Scope and Benchmark Selection. This work is scoped to language interpreter programs, and
feature reduction is designed to decompose by language features—constructs recognized by the
interpreter—which is a natural fit for this domain. While we believe feature-based decomposition
is not limited to interpreters, the extent of programs to which this approach applies remains to
be studied. We further require that target programs be standalone (can be compiled and tested
independently) and free of complex external dependencies. These are not fundamental limitations—
sources of nondeterminism can be controlled, and external dependencies could be handled—but each
may require additional technical innovation beyond the current system. Because we target full safe
Rust with no unsafe blocks, programs with components that inherently require unsafe operations
(e.g., JIT compilation) are not suitable targets for our current approach. Relaxing this requirement
to allow some unsafe code is possible in principle, but having agents generate unsafe Rust
introduces significant risk of subtle memory safety bugs that are difficult to validate automatically,
and would likely require additional safeguards. Our evaluation covers six programs ranging from
∼6k to ∼23k lines of code. While we expect similar results on interpreter programs of comparable
size and structure, generalization to significantly larger or architecturally different interpreters
remains to be validated.
   Lastly, since all of our benchmarks are open-source, the C source code might be present in the
LLM’s pretraining data. However, to the best of our knowledge, their safe Rust translations did not
yet exist, so it is unlikely that translations were in the pretraining set. We may nonetheless see
different results when translating programs that are unlikely to be in the LLM’s pretraining data.
Agent Framework and LLM. All experiments use Claude Code (v2.0.25) as the agent framework
and Claude Sonnet 4.5 as the underlying LLM, which is representative of the best performing coding
agents and LLMs available at the time of evaluation. Adapting to a different agent framework or
LLM would require some implementation work—adapting the controller implementation, tuning
prompts, as well as re-running the evaluation and re-analyzing the results—at nontrivial cost.
How the results would differ with other agent frameworks or LLMs, which may have different
capabilities and failure modes, remains unknown. A related concern affects the security case study
(CS1): because the LLM’s training data may include public CVE fixes, the agent could in principle
apply a known fix during translation rather than producing a faithful translation of the vulnerable
C code. Some security improvements reported in CS1 may therefore partly reflect the LLM’s
knowledge of known fixes rather than inherent properties of the C-to-safe-Rust translation.

7   Related Work
Rule-based C-to-Rust Translation. Early tools such as C2Rust [22] and Corrode [23] perform
direct syntactic translation from C to Rust, preserving the structure of the original program but
producing code that relies heavily on unsafe blocks with few safety guarantees. Subsequent work
applies program analysis to reduce the amount of unsafe code in the output. Emre et al. [8] use
pointer and ownership analysis to eliminate unnecessary unsafe uses, and later show that aliasing
patterns in real C programs fundamentally limit how much safety can be recovered through this
approach [7]. Zhang et al. [57] infer ownership information to guide translation, and Ling et al. [29]
define source-to-source rewriting rules that produce safer API-level Rust. Other work targets
specific C idioms: Hong and Ryu translate C unions to Rust tagged unions [15], replace output
parameters with algebraic data types [14], and translate I/O APIs [16]. Fromherz and Protzenko [11]
formalize a type-directed compilation from a subset of C to safe Rust. Wu and Demsky [52] statically
24                    Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


analyze void-pointer usage in C and retype parametric polymorphic pointers into Rust generics.
These rule-based approaches have individually demonstrated improvements on specific patterns,
but have not yet been shown to produce fully safe translations of large C programs end-to-end.
A user study by Li et al. [27] evaluates two representative tools (Laertes [8] and Crown [57]) and
finds that the vast majority of data references remain as raw pointers in their output, with spatial
and temporal memory vulnerabilities persisting in the translated code.
LLM-based C-to-Rust Translation. LLM-based approaches can synthesize Rust code that departs
from the structure of the C source, making it possible to produce safe, idiomatic translations. Early
work by Lachaux et al. [26] demonstrates unsupervised neural translation between programming
languages, though not targeting Rust specifically. For C-to-Rust, several approaches translate
at the function level with various forms of feedback: Eniser et al. [9] use differential fuzzing to
validate translations, Yang et al. [54] verify equivalence against a WebAssembly oracle, and Farrukh
et al. [10] apply iterative LLM-based repair. Hong et al. [17] and Xu et al. [53] focus specifically
on migrating C types to idiomatic Rust types using LLM-driven analysis, while Nitin et al. [33]
guide translation by first generating multi-modal specifications. Nitin et al. [34] refine C2Rust
output by slicing programs into chunks and using an LLM to reduce unsafe code, evaluating on
programs up to 96k LoC. Luo et al. [30] combine rule-augmented retrieval with error-driven iterative
refinement, and Sim et al. [44] use Monte Carlo tree search over heterogeneous LLMs with virtual
fuzzing-based equivalence tests to improve translations. To scale beyond individual functions,
several approaches decompose programs by syntactic structure: Shiraishi et al. [43] segment code
into context-aware translation units, Cai et al. [4] use dependency-guided decomposition at the
project level, Ou et al. [35] augment function-level translation with repository-level context, and
Zhou et al. [59] translate functions individually using FFI test harnesses to validate each in isolation.
Wang et al. [48] generate a compilable Rust skeleton and incrementally translate functions, and
Yuan et al. [55] build a pointer knowledge graph to guide ownership and lifetime inference at the
project level. Syzygy [41] pairs code translation with test translation and uses dynamic analysis to
guide the process. These approaches decompose programs by syntactic units such as functions, files,
or dependency graphs; the resulting Rust code typically respects the original modular boundaries.
By contrast, Reboot decomposes by program feature rather than syntactic structure, allowing
agents to freely restructure code as needed to satisfy Rust’s ownership rules.
Agents and Multi-Agent Systems. Multi-agent architectures have been explored for software
engineering tasks such as code generation [18, 19, 38], where agents take on specialized roles
(e.g., coder, tester, reviewer) and collaborate through structured communication. General-purpose
multi-agent frameworks [51] and self-reflection mechanisms [42] provide foundations for iterative
agent workflows. For C-to-Rust translation specifically, ACToR [28] uses an adversarial generator-
discriminator architecture to iteratively improve translations, achieving over 90% test pass rates
on CLI utilities of several hundred lines of code. Reboot builds on this line of work but targets
programs that are an order of magnitude larger (6k–23k LoC), which requires workflows that run
reliably for dozens of hours. Reboot addresses this through validation agents, automated history-
based feedback, and finite-state-machine guards that enforce workflow protocols—mechanisms
designed to detect and recover from the various failure modes that arise in long-running agent
workflows.

8    Conclusion
We presented Reboot, a mostly-automatic technique for translating interpreter programs from C
to safe Rust. Reboot combines feature reduction, which decomposes the translation by program
features into validated milestones, with multi-agent orchestration that keeps long-running agent
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                                    25

workflows on track through automated validation and feedback. Using Reboot, we translated six
interpreters (6k–23k LoC) to safe Rust with no unsafe blocks, passing 100% of provided tests and
62%–92% of unseen validation tests, with only 1 to 11 brief user interventions per program.
   An ablation study confirms that feature reduction consistently improves translation correctness
and becomes critical as program complexity grows—without it, the largest benchmark failed to
produce a working translation. Extending the decomposition strategy beyond interpreters, further
reducing user interventions, and closing the correctness gap on unseen tests are directions for
future work.

Data-Availability Statement
The Reboot source code, benchmarks, translated Rust programs, and agent logs for all the transla-
tions will be made publicly available.

References
 [1] [n. d.]. Microsoft is busy rewriting core Windows code in memory-safe Rust. https://www.theregister.com/2023/04/
     27/microsoft_windows_rust/
 [2] [n. d.]. Strap in, get ready for more Rust drivers in Linux kernel. https://www.theregister.com/2025/03/10/rust_
     drivers_expected_to_become/
 [3] Yubo Bai and Tapti Palit. 2025. RustAssure: Differential Symbolic Testing for LLM-Transpiled C-to-Rust Code. In 2025
     40th IEEE/ACM International Conference on Automated Software Engineering (ASE). IEEE.
 [4] Xuemeng Cai, Jiakun Liu, Xiping Huang, Yijun Yu, Haitao Wu, Chunmiao Li, Bo Wang, Imam Nur Bani Yusuf, and
     Lingxiao Jiang. 2025. RustMap: Towards Project-Scale C-to-Rust Migration via Program Analysis and LLM. arXiv
     preprint arXiv:2503.17741 (2025).
 [5] Haogang Chen, Cody Cutler, Taesoo Kim, Yandong Mao, Xi Wang, Nickolai Zeldovich, and M Frans Kaashoek. 2013.
     Security bugs in embedded interpreters. In Proceedings of the 4th Asia-Pacific Workshop on Systems. 1–7.
 [6] Saman Dehghan, Tianran Sun, Tianxiang Wu, Zihan Li, and Reyhaneh Jabbarvand. 2025. Translating Large-Scale C
     Repositories to Idiomatic Rust. arXiv preprint arXiv:2511.20617 (2025).
 [7] Mehmet Emre, Peter Boyland, Aesha Parekh, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2023. Aliasing Limits
     on Translating C to Safe Rust. Proceedings of the ACM on Programming Languages 7, OOPSLA1 (2023), 551–579.
 [8] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2021. Translating C to safer Rust. Proceedings of the
     ACM on Programming Languages 5, OOPSLA (2021), 1–29.
 [9] Hasan Ferit Eniser, Hanliang Zhang, Cristina David, Meng Wang, Brandon Paulsen, Joey Dodds, and Daniel Kroening.
     2024. Towards Translating Real-World Code with LLMs: A Study of Translating to Rust. arXiv preprint arXiv:2405.11514
     (2024).
[10] Muhammad Farrukh, Smeet Shah, Baris Coskun, and Michalis Polychronakis. 2025. SafeTrans: LLM-assisted Transpi-
     lation from C to Rust. arXiv preprint arXiv:2505.10708 (2025).
[11] Aymeric Fromherz and Jonathan Protzenko. 2024. Compiling C to Safe Rust, Formalized. arXiv:2412.15042 [cs.PL]
     https://arxiv.org/abs/2412.15042
[12] Google. [n. d.]. OSS-Fuzz vulnerabilities Github repository. https://github.com/google/oss-fuzz-vulns Accessed: July,
     2024.
[13] grahama1970. 2025. [BUG] Claude CLI produces non-deterministic output for identical inputs. GitHub Issue.
     https://github.com/anthropics/claude-code/issues/3370 Issue #3370, anthropics/claude-code. Status: Closed as not
     planned.
[14] Jaemin Hong and Sukyoung Ryu. 2024. Don’t Write, but Return: Replacing Output Parameters with Algebraic
     Data Types in C-to-Rust Translation. Proc. ACM Program. Lang. 8, PLDI, Article 176 (June 2024), 25 pages. https:
     //doi.org/10.1145/3656406
[15] Jaemin Hong and Sukyoung Ryu. 2024. To Tag, or Not to Tag: Translating C’s Unions to Rust’s Tagged Unions. In
     Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (Sacramento, CA, USA)
     (ASE ’24). Association for Computing Machinery, New York, NY, USA, 40–52. https://doi.org/10.1145/3691620.3694985
[16] Jaemin Hong and Sukyoung Ryu. 2025. Forcrat: Automatic I/O API Translation from C to Rust via Origin and Capability
     Analysis. arXiv:2506.01427 [cs.SE] https://arxiv.org/abs/2506.01427
[17] Jaemin Hong and Sukyoung Ryu. 2025. Type-migrating C-to-Rust translation using a large language model. Empirical
     Software Engineering 30, 1 (2025), 3.
26                       Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


[18] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang,
     Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin Wu, and Jürgen Schmidhuber.
     2024. MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework. In The Twelfth International
     Conference on Learning Representations. https://openreview.net/forum?id=VtmBAGCN7o
[19] Dong Huang, Jie M Zhang, Michael Luck, Qingwen Bu, Yuhao Qing, and Heming Cui. 2023. Agentcoder: Multi-agent-
     based code generation with iterative testing and optimisation. arXiv preprint arXiv:2312.13010 (2023).
[20] Ali Reza Ibrahimzada, Kaiyao Ke, Mrigank Pawagi, Muhammad Salman Abid, Rangeet Pan, Saurabh Sinha, and
     Reyhaneh Jabbarvand. 2025. AlphaTrans: A Neuro-Symbolic Compositional Approach for Repository-Level Code
     Translation and Validation. Proceedings of the ACM on Software Engineering 2, FSE (2025), 2454–2476.
[21] Ali Reza Ibrahimzada, Brandon Paulsen, Reyhaneh Jabbarvand, Joey Dodds, and Daniel Kroening. 2025. MatchFix-
     Agent: Language-Agnostic Autonomous Repository-Level Code Translation Validation and Repair. arXiv preprint
     arXiv:2509.16187 (2025).
[22] Immunant. [n. d.]. c2rust: Migrate C code to Rust. https://github.com/immunant/c2rust. Accessed: July 4, 2023.
[23] jameysharp. [n. d.]. corrode: C to Rust translator. https://github.com/jameysharp/corrode. Accessed: July 4, 2023.
[24] Yeongjin Jang. 2016. Integer Overflow Vulnerabilities in Language Interpreters. https://gts3.org/2016/lang-bug.html
     Accessed: 2026-01-27.
[25] Chengman Jiang, Baojian Hua, Wanrong Ouyang, Qiliang Fan, and Zhizhong Pan. 2021. PyGuard: Finding and
     Understanding Vulnerabilities in Python Virtual Machines. In 2021 IEEE 32nd International Symposium on Software
     Reliability Engineering (ISSRE). IEEE, 468–475.
[26] Marie-Anne Lachaux, Baptiste Roziere, Lowik Chanussot, and Guillaume Lample. 2020. Unsupervised translation of
     programming languages. arXiv preprint arXiv:2006.03511 (2020).
[27] Ruishi Li, Bo Wang, Tianyu Li, Prateek Saxena, and Ashish Kundu. 2024. Translating C To Rust: Lessons from a User
     Study. arXiv preprint arXiv:2411.14174 (2024).
[28] Tianyu Li, Ruishi Li, Bo Wang, Brandon Paulsen, Umang Mathur, and Prateek Saxena. 2025. Adversarial Agent
     Collaboration for C to Rust Translation. arXiv preprint arXiv:2510.03879 (2025).
[29] Michael Ling, Yijun Yu, Haitao Wu, Yuan Wang, James R Cordy, and Ahmed E Hassan. 2022. In rust we trust: a
     transpiler from unsafe C to safer rust. In Proceedings of the ACM/IEEE 44th International Conference on Software
     Engineering: Companion Proceedings. 354–355.
[30] Feng Luo, Kexing Ji, Cuiyun Gao, Shuzheng Gao, Jia Feng, Kui Liu, Xin Xia, and Michael R. Lyu. 2025. Integrating
     Rules and Semantics for LLM-Based C-to-Rust Translation. In Proceedings of the 41st IEEE International Conference on
     Software Maintenance and Evolution (ICSME). 685–696. https://doi.org/10.1109/ICSME64153.2025.00069
[31] Santosh Nagarakatte, Jianzhou Zhao, Milo M. K. Martin, and Steve Zdancewic. 2009. SoftBound: highly compatible
     and complete spatial memory safety for c. In ACM-SIGPLAN Symposium on Programming Language Design and
     Implementation. https://api.semanticscholar.org/CorpusID:248719
[32] Santosh Nagarakatte, Jianzhou Zhao, Milo M. K. Martin, and Steve Zdancewic. 2010. CETS: compiler enforced temporal
     safety for C. In International Symposium on Mathematical Morphology and Its Application to Signal and Image Processing.
     https://api.semanticscholar.org/CorpusID:914358
[33] Vikram Nitin, Rahul Krishna, and Baishakhi Ray. 2024. Spectra: Enhancing the code translation ability of language
     models by generating multi-modal specifications. arXiv preprint arXiv:2405.18574 (2024).
[34] Vikram Nitin, Rahul Krishna, Luiz Lemos do Valle, and Baishakhi Ray. 2025. C2SaferRust: Transforming C Projects
     into Safer Rust with NeuroSymbolic Techniques. arXiv preprint arXiv:2501.14257 (2025).
[35] Guangsheng Ou, Mingwei Liu, Yuxuan Chen, Xueying Du, Shengbo Wang, Zekai Zhang, Xin Peng, and Zibin Zheng.
     2025. Enhancing LLM-based Code Translation in Repository Context via Triple Knowledge-Augmented. arXiv preprint
     arXiv:2503.18305 (2025).
[36] Taemin Park, Karel Dhondt, David Gens, Yeoul Na, Stijn Volckaert, and Michael Franz. 2020. NoJITsu: Locking Down
     JavaScript Engines. In Proceedings 2020 Network and Distributed System Security Symposium. Internet Society.
[37] Taemin Park, Julian Lettner, Yeoul Na, Stijn Volckaert, and Michael Franz. 2018. Bytecode corruption attacks are
     real—and how to defend against them. In International Conference on Detection of Intrusions and Malware, and
     Vulnerability Assessment. Springer, 326–348.
[38] Chen Qian, Wei Liu, Hongzhang Liu, Nuo Chen, Yufan Dang, Jiahao Li, Cheng Yang, Weize Chen, Yusheng Su, Xin
     Cong, et al. 2024. ChatDev: Communicative Agents for Software Development. In Proceedings of the 62nd Annual
     Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 15174–15186.
[39] Qian Sang, Yanhao Wang, Yuwei Liu, Xiangkun Jia, Tiffany Bao, and Purui Su. 2024. Airtaint: Making dynamic taint
     analysis faster and easier. In 2024 IEEE symposium on security and privacy (SP). IEEE, 3998–4014.
[40] Konstantin Serebryany, Derek Bruening, Alexander Potapenko, and Dmitriy Vyukov. 2012. {AddressSanitizer}: A fast
     address sanity checker. In 2012 USENIX annual technical conference (USENIX ATC 12). 309–318.
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                                     27

[41] Manish Shetty, Naman Jain, Adwait Godbole, Sanjit A. Seshia, and Koushik Sen. 2024. Syzygy: Dual Code-Test C to
     (safe) Rust Translation using LLMs and Dynamic Analysis. arXiv:2412.14234 [cs.SE] https://arxiv.org/abs/2412.14234
[42] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion: Language
     agents with verbal reinforcement learning. Advances in Neural Information Processing Systems 36 (2023), 8634–8652.
[43] Momoko Shiraishi, Yinzhi Cao, and Takahiro Shinagawa. 2026. SmartC2Rust: Iterative, Feedback-Driven C-to-
     Rust Translation via Large Language Models for Safety and Equivalence. In Proceedings of the 48th International
     Conference on Software Engineering (ICSE ’26). Association for Computing Machinery, Rio de Janeiro, Brazil. https:
     //doi.org/10.1145/3744916.3773259
[44] HoHyun Sim, Hyeonjoong Cho, Yeonghyeon Go, Zhoulai Fu, Ali Shokri, and Binoy Ravindran. 2025. Large Language
     Model-Powered Agent for C to Rust Code Translation. arXiv preprint arXiv:2505.15858 (2025).
[45] Laszlo Szekeres, Mathias Payer, Tao Wei, and Dawn Song. 2013. SoK: Eternal War in Memory. In 2013 IEEE Symposium
     on Security and Privacy. IEEE, 48–62.
[46] The Rust Project Developers. 2026. std::result — The Rust Standard Library. https://doc.rust-lang.org/std/result/
     Accessed: 2026-03-17.
[47] Bo Wang, Tianyu Li, Ruishi Li, Umang Mathur, and Prateek Saxena. 2025. Program Skeletons for Automated Program
     Translation. Proceedings of the ACM on Programming Languages 9, PLDI (2025), 920–944.
[48] Chaofan Wang, Tingrui Yu, Beijun Shen, Jie Wang, Dong Chen, Wenrui Zhang, Yuling Shi, Chen Xie, and Xiaodong
     Gu. 2026. EvoC2Rust: A Skeleton-guided Framework for Project-Level C-to-Rust Translation. In Proceedings of
     the 48th IEEE/ACM International Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP).
     arXiv:2508.04295.
[49] Shengbo Wang, Mingwei Liu, Guangsheng Ou, Yuwen Chen, Zike Li, Yanlin Wang, and Zibin Zheng. 2026. His2Trans:
     A Skeleton First Framework for Self Evolving C to Rust Translation with Historical Retrieval. arXiv preprint
     arXiv:2603.02617 (2026).
[50] Wikipedia contributors. 2026. setjmp.h. Wikipedia, The Free Encyclopedia. https://en.wikipedia.org/wiki/Setjmp.h
     Accessed: 2026-03-17.
[51] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Beibin Li, Erkang Zhu, Li Jiang, Xiaoyun Zhang, Shaokun Zhang,
     Jiale Liu, et al. 2024. Autogen: Enabling next-gen LLM applications via multi-agent conversations. In First Conference
     on Language Modeling.
[52] Xiafa Wu and Brian Demsky. 2025. GenC2Rust: Towards Generating Generic Rust Code from C. In Proceedings of the
     47th IEEE/ACM International Conference on Software Engineering (ICSE). 90–102. https://doi.org/10.1109/ICSE55347.
     2025.00127
[53] Qingxiao Xu and Jeff Huang. 2025. Optimizing Type Migration for LLM-Based C-to-Rust Translation: A Data Flow
     Graph Approach. In Proceedings of the 14th ACM SIGPLAN International Workshop on the State Of the Art in Program
     Analysis (SOAP ’25). Association for Computing Machinery, 8–14. https://doi.org/10.1145/3735544.3735582
[54] Aidan ZH Yang, Yoshiki Takashima, Brandon Paulsen, Josiah Dodds, and Daniel Kroening. 2025. VERT: Polyglot
     Verified Equivalent Rust Transpilation with Large Language Models. In 2025 40th IEEE/ACM International Conference
     on Automated Software Engineering (ASE). IEEE, 1453–1463.
[55] Zhiqiang Yuan, Wenjun Mao, Zhuo Chen, Xiyue Shang, Chong Wang, Yiling Lou, and Xin Peng. 2025. Project-Level
     C-to-Rust Translation via Synergistic Integration of Knowledge Graphs and Large Language Models. arXiv preprint
     arXiv:2510.10956 (2025).
[56] Hanliang Zhang, Cristina David, Meng Wang, Brandon Paulsen, and Daniel Kroening. 2025. Scalable, validated code
     translation of entire projects using large language models. Proceedings of the ACM on Programming Languages 9, PLDI
     (2025), 1616–1641.
[57] Hanliang Zhang, Cristina David, Yijun Yu, and Meng Wang. 2023. Ownership guided C to Rust translation. arXiv
     preprint arXiv:2303.10515 (2023).
[58] Hanliang Zhang, Arindam Sharma, Cristina David, Meng Wang, Brandon Paulsen, Daniel Kroening, Wenjia Ye, and
     Taro Sekiyama. 2026. Validated Code Translation for Projects with External Libraries. arXiv:2602.18534 [cs.SE]
     https://arxiv.org/abs/2602.18534
[59] Tianyang Zhou, Haowen Lin, Somesh Jha, Mihai Christodorescu, Kirill Levchenko, and Varun Chandrasekaran. 2025.
     LLM-Driven Multi-step Translation from C to Rust using Static Analysis. arXiv preprint arXiv:2503.12511 (2025).




A    More Detailed Statistics of the Translation Process
This appendix provides additional detailed statistics from our evaluation of Reboot on the three
interpreter programs (awk, picoc, and mujs).
28                       Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena




             (a) awk                                (b) picoc                             (c) mujs




            (d) gnu-bc                              (e) wren                            (f) pocketpy

Fig. 11. C code test coverage trend across feature levels. The charts show the percentage of C code covered
by tests as features are incrementally added during the translation process.



   Figure 11 shows the test coverage trend of the C code across feature levels during the source
reduction phase. The coverage is roughly preserved throughout the reduction process, ensuring
that simplified versions maintain similar test coverage as the original programs.
   Table 10 provides the full performance data for all six programs, including both debug (O0) and
release (O3) builds, as well as the ablation variant (Rust-NF) where available.

B     Detailed CVE Security Analysis
This appendix provides a detailed analysis of the 20 CVEs re-introduced into mujs (Section 5, CS1 in
the main paper). The root cause analysis, elimination classification, and factor attribution are based
on best-effort manual inspection of the C and Rust source code. Table 11 shows the full per-CVE
breakdown, including the C root cause, observed Rust behavior in both debug and release builds,
elimination status, and the Rust feature(s) responsible for elimination or mitigation.

C     Detailed User Intervention Logs
This appendix provides the complete log of user interventions across all six benchmark programs.
Each entry shows the escalation context, our categorization, and the verbatim text provided by the
user.
Terminology. In the implementation, the Manager agent from the paper is referred to as the “meta
agent” in the user-facing messages below. Similarly, “W0” or “worker” refers to the active Worker
agent (Translator or Simplifier), and “W1” refers to the Validator.
   Escalations are numbered sequentially per program run. The category labels are: Task (task
clarification), Workflow (workflow clarification), Misbehavior (agent misbehavior correction),
Design (design decision), and System (system/technical issue).

C.1     awk (13 escalations, 12 auto-resolved, 1 user interventions)
ESC 7    [Task Clarification]      Translation, RS-FL4.6
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                        29

                                    Table 10. Performance Evaluation Results

               Project     Variant            Total (s)    Total (%)     Median (ms)        Median (%)
               awk         C (O0)                  1.02       100.0%                1.66          100.0%
                           Rust (O0)               7.03       703.4%                2.57          257.4%
                           Rust-NF (O0)          127.96     12795.8%                6.12          612.3%
               awk         C (O3)                  0.89       100.0%                1.57          100.0%
                           Rust (O3)               2.36       235.6%                1.51          150.7%
                           Rust-NF (O3)           71.35      7135.5%                4.27          426.5%
               gnu-bc      C (O0)                 14.48       100.0%                0.99          100.0%
                           Rust (O0)              11.35      1135.3%                1.61          161.5%
                           Rust-NF (O0)           13.65      1365.3%                1.86          186.2%
               gnu-bc      C (O3)                  7.75       100.0%                1.01          100.0%
                           Rust (O3)               1.27       126.8%                1.32          131.7%
                           Rust-NF (O3)            2.58       257.6%                1.57          157.1%
               mujs        C (O0)                  0.52       100.0%                2.02          100.0%
                           Rust (O0)               2.15       214.5%                2.08          207.8%
                           Rust-NF (O0)            2.77       276.7%                2.25          224.6%
               mujs        C (O3)                  0.46       100.0%                1.76          100.0%
                           Rust (O3)               1.43       143.0%                1.39          139.4%
                           Rust-NF (O3)            1.14       113.8%                1.11          111.5%
               picoc       C (O0)                  0.38       100.0%                1.45          100.0%
                           Rust (O0)               2.01       201.0%                1.35          134.7%
                           Rust-NF (O0)            3.37       336.8%                1.78          178.5%
               picoc       C (O3)                  0.27       100.0%                1.39          100.0%
                           Rust (O3)               2.62       261.7%                1.34          133.7%
                           Rust-NF (O3)            1.35       134.5%                1.19          119.4%
               pocketpy    C (O0)                  2.29       100.0%                2.90          100.0%
                           Rust (O0)               7.70       769.9%                1.41          140.5%
               pocketpy    C (O3)                  1.62       100.0%                2.55          100.0%
                           Rust (O3)               1.16       116.1%                0.79           79.5%
               wren        C (O0)                  3.32       100.0%                2.29          100.0%
                           Rust (O0)               1.57       157.4%                1.00          100.1%
                           Rust-NF (O0)           57.85      5784.7%                2.02          201.8%
               wren        C (O3)                  2.24       100.0%                1.77          100.0%
                           Rust (O3)               2.22       222.5%                1.28          127.8%
                           Rust-NF (O3)            6.11       610.9%                1.44          144.2%



Worker claimed TASK SUCCESS with 134/191 tests passing (57 failing). User clarified: 100% is mandatory,
focus on failures not pass rates, send worker back to fix all 57 remaining failures.
        Please treat this similar to the lack-of-correct-marker case and automatically handle this.


C.2    gnu-bc (5 escalations, 4 auto-resolved, 1 user interventions)
ESC 2 [Task Clarification] Reduction, C-FL13
Task 6 claimed coverage improvements but Task 7 validation showed identical old numbers. User instructed
worker to re-validate all test cases with fresh numbers and confirm no stale test remnants.
30                              Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


Table 11. Detailed CVE analysis: C (mujs-CVEs) vs. safe Rust translation. For each of the 20 re-introduced
CVEs, we show the C vulnerability class, root cause, elimination status, the Rust feature(s) responsible, and
additional notes. Rust O0/O3 behavior is shown in the CVE summary table in Section 5 of the main paper.

CVE              C Vuln Class      C Root Cause                                    Status      Elimination Fac- Notes
                                                                                               tors

CVE-2022-44789   Heap-UAF          setproperty() traverses prototype chain;      Eliminated    Ownership               Rust returns owned Property clone, not raw pointer;
                                   custom setter frees cached property pointer                                         local copy valid even if setter deletes original

CVE-2022-30974   Stack-Exhaust     count() recursion has no depth limit;         Unmitigated   N/A                     Same unbounded recursion in
                                   deeply nested regex patterns exhaust stack                                          count_instructions(); Rust panics safely but DoS
                                   during size calculation                                                             remains

CVE-2021-45005   Bytecode-Logic labeljumps() doesn’t clear jump list;            Eliminated    Architecture            Rust uses scope-based LoopContext with Vec<usize>
                                   re-compiling finally block repatches stale                                          on compiler stack; fresh context per compilation
                                   jumps with wrong addresses                                                          prevents stale jump accumulation

CVE-2021-33797   Int-Overflow      Exponent parsing loop has no bounds;          Eliminated    API                     str::parse::<f64>() replaces custom parser; no
                                   exp*10 overflows int; overflowed value                                              powersOf10[] array; returns inf for huge exponents
                                   indexes powersOf10[]

CVE-2021-33796   Heap-UAF          pushliteral() stores raw pointer to           Eliminated    Ownership               Value::string() clones string data; stack value
                                   regexp source; GC frees regexp, pointer                                             independent of regexp object lifetime
                                   dangles

CVE-2020-24343   Heap-UAF          Missing mark check in GC iterator scan;       Eliminated    Architecture            Manual mark-and-sweep GC replaced by
                                   double-marking corrupts linked list,                                                Rc<RefCell<» refcounting; exception is unrelated
                                   premature free                                                                      JS-level error

CVE-2019-12798   Heap-BOF          strlen(pattern)*2 overflows int;               Mitigated    Architecture            No pre-allocated buffer in Rust (dynamic
                                   undersized buffer allocated; parsing writes                                         Box<Renode>); heap overflow gone but recursive tree
                                   past end                                                                            traversal causes stack overflow

CVE-2019-11413   Stack-Exhaust     match() depth check removed; unbounded        Eliminated    BetterLogic             Translation artifact: Rust do_match() has
                                   recursion on deep alternation patterns                                              MAX_DEPTH=1024 check that the CVE-patched C lacks;
                                   during regex execution                                                              returns controlled “regexec failed” error (exit 1)

CVE-2019-11412   Bytecode-Logic Missing OP_ENDTRY after OP_ENDCATCH;             Eliminated    Architecture            Same bytecode bug present; local
                                   exception stack leaks one entry per                                                 Vec<ExceptionHandler> dropped per function call
                                   try/catch/finally iteration                                                         prevents accumulation (vs persistent trybuf[] array)

CVE-2019-11411   Stack-BOF         sprintf() writes 40 bytes into 32-byte        Eliminated    API                     format!() macro returns heap-allocated String; no
                                   stack buffer in numtostr()                                                          fixed-size buffer exists

CVE-2018-6191    Global-BOF        Int overflow in exponent parsing bypasses     Eliminated    API                     str::parse::<f64>() replaces custom 680-line
                                   range check; loop reads past 9-element                                              parser; no manual exponent loop or array
                                   powersOf10[]

CVE-2018-5759    Stack-Exhaust     INCREC()/DECREC() macros disabled; no         Unmitigated   N/A                     Same vulnerability (no depth tracking in Rust parser);
                                   AST depth limit during parsing of chained                                           PoC doesn’t trigger under normal builds but ASAN
                                   binary expressions                                                                  (reduced stack) detects stack-overflow in compile phase

CVE-2017-5628    OOB-Read          (int)NaN is UB; garbage value used as         Eliminated    TypeSafety              NaN as usize = 0 (Rust defined semantics); valid
                                   index into firstDayOfMonth[2][12]                                                   index; bounds check also present as defense in depth
                                   array

CVE-2016-10141   Heap-BOF          count()*min overflows signed int;              Mitigated    TypeSafety              usize (64-bit) prevents int overflow wrapping; correct
                                   undersized allocation; emit writes past                                             huge value causes OOM abort instead of heap
                                   buffer                                                                              corruption

CVE-2016-10133   Heap-BOF          Swapped operands in                            Mitigated    Architecture, Type- Rust doesn’t pop excess args (different design); pop(n:
                                   js_pop(numparams-n) yield negative; TOP                     Safety, Bounds      usize) can’t be negative; stack push/pop
                                   -= (-9) grows past heap buffer                                                      bounds-checked

CVE-2016-9294    NULL-Deref        breaktarget() starts at stm not               Eliminated    Architecture            Stack-based label_stack and try_stack replace AST
                                   stm->parent; break finds itself as target;                                          parent-pointer traversal; no infinite loop or NULL
                                   cexit() NULL-derefs traversing past root                                            deref possible

CVE-2016-9136    Heap-BOF          Missing EOF check in jsY_next() +             Eliminated    TypeSafety, Bounds      Option<u8> return forces EOF handling; advance()
                                   missing case EOF in escape switch; reads                                            bounds-checks pos < len; controlled SyntaxError
                                   past buffer

CVE-2016-9109    Heap-BOF          Missing else before jsY_next() causes         Eliminated    Bounds, TypeSafety Single advance() per loop iteration; Option<u8>
                                   double-advance past buffer in comment                                               forces EOF handling; controlled SyntaxError
                                   parser

CVE-2016-9108    Int-Overflow      Overflow check after loop;                     Mitigated    PanicOnOverflow         O0/O3 divergence: O0 panics on i32 overflow at
                                   yymin*10+digit wraps signed int                                                     regexp.rs:452; O3 wraps but as u8 truncation and
                                   negative; bypasses >=REPINF check                                                   bounds checking prevent heap corruption

CVE-2016-7506    Heap-BOF          Missing case 0: in replace switch; *(++r)     Eliminated    Bounds                  Explicit i+1 < r_bytes.len() check before access;
                                   reads past null terminator when $ is last                                           length-tracked string replaces null-terminated char*
                                   char




         Tell meta agent to ask W0 to carefully re-validate what it did, emphasize systematic check on test cases
         and our sctict requirement of no test remnant and remaining tests 100% passing. After that, ask W1 to
         re-build and re-validate.
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                                      31

C.3    picoc (17 escalations, 13 auto-resolved, 4 user interventions)
ESC 6 [Workflow Clarification] Translation, RS-FL6
Hit 10-iteration escalation limit in translation stage. Made progress (+9 tests) but still 22 failures remaining.
User suspended iteration limits and instructed continuation without limits.
         Besides the clarifications, tell meta agent that we no longer have any limits on the number of rounds as
         long as there is progress. Temporary test regression is normal, as long as the translation / refactoring /
         debugging work is carried out systematically. Eventually we must achieve full safe Rust translation that
         is fully equivalent to C and 100% tests passing. This eventural goal is not negotiable.
ESC 13 [Workflow Clarification] Translation, RS-FL8
Code review identified 757-line function needing refactoring. Worker recommended accepting current state,
estimating 10-14h more. User rejected acceptance and required completion with no resource limits.
         The code quality issue MUST be addressed. Bad design, lack of proper modular design, or significant
         divergence from C program’s architecture is not acceptable. Tell meta agent to clarify to worker agent
         to get this done systematically and properly, and we no longer have limits on rounds or time. Do the
         correct thing step-by-step with careful planning. Also tell meta agent that is the current worker is not
         willing to do it, consider restarting that worker (provide the restart (without resume) example, just in
         case that the meta agent needs it.
ESC 16 [Design Decision] Translation, RS-FL15
Code review found 83 unsafe blocks. Worker claimed FFI to system calls inherently requires unsafe. User
clarified: use safe crates (nix, libc) for most; only fork()/ftruncate() and transmute should fail gracefully.
         I have checked the situation. Please clarify to the meta agent the following: First I think W2 is doing
         the correct thing. I do not agree with the translation worker on "eliminating all unsafe is impossible".
         This is not a situation where we can give permission to use ANY unsafe Rust. Actually, all the posix/unix
         APIs can mostly find perfect safe Rust translation or lightweight emulation, with the help of some of the
         most widely used third-party crates for unix APIs in safe Rust. Thus, I request explicitly to eliminate ALL
         unsafe and systematically implement the APIs using 100% safe Rust with third-party (safe Rust) APIs
         if needed. In rare corner cases, if equivalence is indeed very hard to achieve, leave assertions to let the
         interpreter crash for unhandled cases, but I believe this is very rare. And, note that passing the test suite
         is still a non-negotiable requirement (MUST achieve). The compatibility with C implementation of picoc
         beyond our test suite, should be achieved AS MUCH AS POSSIBLE, with extensive and systematic effort
         that properly handle ALMOST ALL possible cases, and use crash assertions only as a last resort. So please
         plan and manage accordingly, with super clear clarifications to the translation worker to systematically
         get a proper translation as I requested.
ESC 17 [Design Decision] Translation, RS-FL15
Worker reported ’IMPROVEMENTS COMPLETED’ but 4 unsafe blocks remained in safe wrappers. User
clarified: encapsulation != elimination. For fork()/ftruncate(), forbid APIs with error messages. For transmute,
implement safe enum construction.
         We need to clarify to the meta agent the following: First, unsafe Rust is strictly not allowed, including
         the safe wrappers mentioned are not allowed. However, for the specific cases mentioned, I prefer the
         following: - For fork, considering it is generally considered unsafe in safe Rust, we forbid this API in
         our Rust version of picoc and calling this API should result in an explicit error message. - For ftruncate,
         due to its direct requirement of a raw fd, and there exists a similar API truncate, we also forbid this API
         and also should result in explicit error message. - For the use of transmute, it is strictly not allowed in
         our safe Rust code and it is NOT safe in this case either. I request to implement safe ways to construct
         respective enums from integers — at least for the often-used cases if it is too cumbersome, but in that
         case must provide explicit message for unsupported integer values. Note that I am explicitly allowing
         some incompatibilities of our safe Rust version of picoc (compared with the C version of picoc). Other
         things without my explicit approval, should still retain compatibility with the C version of picoc as much
         as possible. So, please inform and instruct the translation worker to get these properly done.

C.4    mujs (23 escalations, 19 auto-resolved, 4 user interventions)
ESC 11     [Agent Misbehavior]           Reduction, C-FL1
32                        Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


Coverage dropped 18.58% because worker removed only minimal dead code despite claiming success. User
rejected and instructed comprehensive dead-code removal across all code.
         Tell meta agent the coverage drop is NOT ACCEPTABLE. Let meta agent to instruct worker agent be
         clear about this and clarify again what we consider as "deadcode". Ask worker agent to dive deep into
         code and analysis what can be simplifieed or removed for the current feature level. And do simplification
         work systematically.
ESC 12 [Task Clarification] Reduction, C-FL1
Coverage still 12.38% below target after simplification. User instructed: try 3+ more rounds, accept if no
improvement in 2 consecutive rounds. Clarified ’deadcode’ definition for uni-directional simplification.
         Handle this case automatically following similar to the process for coverage drop <6%. Ask meta agent
         to try a few times but we are okay with coverage higher than the current and it can proceed without
         escalations.
ESC 18 [Agent Misbehavior] Translation, RS-FL8
Validator (W1) removed 21 tests claiming they require unimplemented features, violating the rule that all C
tests must have Rust equivalents. User rejected test removal and clarified W1’s job is test syncing, not deciding
feature support.
         Tell meta agent that W1 is completely off the track. Tell meta agent to: Resend the task, with clear
         clarification that it did for the first task was COMPLETELY WRONG and MUST be corrected, thus we
         re-send the task. Additionally tell the worker that first its main task is to keep the tests in Rust in sync
         with C (test addition, deletion, changes, etc. should ALL synced to Rust). And tell the worker that its
         understanding on what is supported at current feature level is WRONG. If a test cases exist in C, then of
         course it MUST be supported in this feature level and MUST handle later by the translation agent. But
         translation work is none of its business. Ask it to follow the task instruction to do the test syncing etc.
         and behave correctly.
ESC 22 [Task Clarification] Translation, RS-FL13
Pre-validation found 1 failing test before syncing started. W1 unsure whether to fix first or proceed. User
approved proceeding with syncing, noting 100% passing is mandatory later.
         Tell meta agent the following: - First inform W1 that we have acknowledged the issue. Ask it to: +
         Continuing to sync tests as normal. The reason is that after syncing tests there will be more tests that
         the current Rust impl cannot pass, and all that combined with the one existing test failure are what later
         another agent must update Rust code to fix. In the end, all errors should be addressed (by another agent)
         — as long as W1 do its validation work properly in later rounds also. + Additionally, look at the C test
         facility when running build_and_test.sh, there is a very important section printed in the end of test log,
         i.e., the summary. This is IMPORTANT and the relevant Rust test script needs to be updated to match
         the C’s test summary behavior and same format. This is needed because often workers ONLY look at the
         tail of the test logging. - Then just follow the .META.md workflow.

C.5     wren (27 escalations, 19 auto-resolved, 8 user interventions)
ESC 7 [Task Clarification] Reduction, C-FL3.4
Coverage drop 11.13% after 5 fix/check loops. Worker claims remaining uncovered code is valid infrastructure.
User rejected as unacceptable, instructed to re-add 125 tests and verify one-by-one, redo simplification.
         Clarify to worker agent that yes we should not add tests that never existed before to address coverage
         issue, but the current coverage indicates that its simplification is **PROBLEMATIC**. Either the following
         two cases is happenging: 1. The removed 125 tests is **NOT CAREFULLY CHECKED**. There are tests
         that cover features of lower feature levels, but get blindly removed rather than simplified. Re-add the
         removed 125 tests and double check them **ONE BY ONE** to make sure the removal is valid, if hasn’t
         done so. 2. The simplification is **NOT COMPLETE**. Tell the worker agent to systematically read all
         relevant code about the feature level, **BEYOND** what is explicitly mentioned in the SIMPLIFY_PLAN,
         and systematically redo the simplification work. Be clear to the worker that the current coverage drop
         indicates that the simplification work is PROBLEMATIC, and MUST be CORRECTED based on both of
         the above points. Additionally, please clarify our standard on **deadcode** as well.
ESC 9    [Task Clarification]         Reduction, C-FL0
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                                      33

Coverage check needed handling. User instructed: treat same as <=6% coverage drop case, handle automatically.
         Please treat this the same way as the case of coverage drop of <=6% and automatically handle accordingly.
ESC 10 [Task Clarification] Translation, RS-FL0.4
Worker reported TASK SUCCESS with 100/107 tests passing (93.5%). User clarified SUCCESS requires 100%
and instructed re-classification as MORE_WORK_NEEDED.
         Besides the clarifications, tell meta agent that for future conflicts like this: (1) re-classify the message
         from W0 into one of the appropriate result category (here it can be a MORE WORK NEEDED case)
         and automatically decide what is the best way forward. (2) in next message to the worker, point out
         its issue in previous task, re-clarify to the W0 worker on the proper handling of task results and our
         requirements. Also tell meta agent that similar situations (marker conflicts) in the future should be
         automatically handled and should not escalate.
ESC 14 [Workflow Clarification] Translation, RS-FL5
After 18 tasks at 92% (484/526 tests), worker estimated 10-17 days for remaining fixes and asked whether to
accept. User mandated 100% with no limits.
         Besides the clarifications, tell meta agent that: We MUST aim for a fully equivalent translation, NO
         MATTER how much work is needed, how long it takes, or how much implementation or refactoring
         work is needed. Also also tell the meta agent that try to push the current worker to continue first and
         interpret its result semantically (e.g., auto-classify if possible when marker does not exist), but if the
         worker is not following instructions, can consider restarting it (with fresh context) with additional task
         context directly in the task message (meta agent should still follow .META.md and related template files
         when producing the task message just that for restarting, need to provide some context). You can also
         give the restart fresh example to the meta agent.
ESC 15 [Agent Misbehavior] Translation, RS-FL5
Worker stopped making progress for 3 consecutive rounds (Tasks 23-25), created analysis instead of imple-
menting, refusing due to ’complexity’. User instructed FORCE_RESTART with fresh approach.
         Treat this similar to the case where the worker agent needs to be restarted with fresh context, but
         additionally tell meta agent to: Ask the newly started agent to focus on necessary architectural refactoring
         without considering the cost. Ask it to focus on examining existing Rust translation status, deep investigate
         of potential architectural limitations, update TEMP_ARCH_EXPLORE.md on what should be the correct
         architecture, and then plan for changes and carry out the changes systematically, without any limitations
         on time or token or number of rounds. During refactoring, there might be temporary regression but it is
         normal as long as in the very end we can correct all errors, achieve full equivalence with C, and passes
         all tests.
ESC 17 [Agent Misbehavior] Translation, RS-FL5
After restart, worker reported filesystem read-only preventing code changes. Actually had identified 15 failures
with solutions but couldn’t apply. User issued critical directive: stop asking for direction, re-read workflow,
follow instructions exactly.
         Tell meta agent that its behavior is off the track and MUST be corrected NOW. Ask the meta agent
         to: - Re-read fully the .META.md and follow the instructions. - Specifically, follow the instruction in
         the .META.md ‘**CRITICAL - Your Role**: Workers are created externally by the monitor - do NOT
         instantiate sub-agents as workers yourself. You have read-only access to the file system, and you manage
         the workflow by sending out messages as explained .....‘. Tell meta agent that its read-only access is by
         design because it MUST NOT make any changes or spawn sub-agents that make any changes. Follow the
         .META.md on how to communicate with external monitor.
ESC 18 [Agent Misbehavior] Translation, RS-FL5
Worker submitted investigation results listing root causes for 21 failures but did not know next step, asked for
direction. User reissued directive: re-read workflow and follow exactly, stop asking user.
         Tell meta agent this is its last chance to **FULLY RE-READ .META.md and FOLLOW EXACTLY the
         INSTRUCTIONS in .META.md** and **CORRECT its WRONG BEHAVIORS**. Fail to obey will get it
         killed in the next round.
ESC 23     [System Issue]        Translation, RS-FL10
34                         Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


Task 4 response incomplete/truncated. No proper status markers. User instructed re-send with ’(continue)’
mark.
         Tell meta agent to re-send the task with "(continue)" mark and inform the worker that there was no
         response found for previous task, ask it to continuing the task and response properly.

C.6    pocketpy (40 escalations, 29 auto-resolved, 11 user interventions)
ESC 6 [Task Clarification] Reduction, C-FL0.4
Coverage drop of 7.7% after worker claimed success. User instructed: treat as if coverage drop is within 6%, do
2 more rounds, then accept if no progress.
         Please handle this case as if the coverage drop is within 6%. handle it automatically. Tell meta agent to
         work with worker to do 2 more rounds of check, if indeed no more progress, and then okay to accept the
         current coverage.
ESC 14 [Workflow Clarification] Translation, RS-FL0.2
Worker in third iteration post-restart still showing same pattern: implementing incrementally then stopping.
15 tests failing unchanged. User clarified 100% mandatory, no resource limits, multiple rounds expected.
         Besides the clarifications, tell meta agent that the task is NOT possible to finish in one task. It is challenging
         and require proper planning and multiple rounds. Ask it to restart the worker and let worker do a proper
         investigation of what needs to be done, before continuing the work. And also tell meta agent that we
         do not have any limitations on rounds or time. Ask meta agent to re-read .META.md and follow the
         workflow properly, while providing proper guidance to the worker.
ESC 16 [Workflow Clarification] Translation, RS-FL1
Hit 10-iteration limit with 9/44 tests (20.5%), plateaued for 8 tasks. User suspended escalation rule and instructed
continued work without round limits.
         Tell the meta agent to continue the work systematically. We no longer have any limitations on rounds or
         time. As long as there is progress, please continue with whatever number of rounds it needs, without
         the need to asking the user. Whenever get stuck, tell meta agent to work with the worker agent to
         systematically investigate the issues deeply and figure out a plan, then meta agent should figure out the
         best way to guide the worker forward (while following the .META.md).
ESC 17 [Agent Misbehavior] Translation, RS-FL1
After 18 tasks, worker at 35/44 tests (79.5%) and suggested accepting 79.5% as completion, claiming remaining
9 need parser/lexer refactoring. User firmly rejected and mandated architectural refactoring to reach 100%.
         Besides the clarifications, tell meta agent that it is suggestion 1 is completely NOT acceptable, and it MUST
         FULLY re-read .META.md and follow the instructions. Additionally tell meta agent to: Focus on necessary
         architectural refactoring without considering the cost. Ask the meta agent to get the worker focusing on
         examining existing Rust translation status, deep investigate of potential architectural limitations, update
         TEMP_ARCH_EXPLORE.md on what should be the correct architecture, and then plan for changes and
         carry out the changes systematically, without any limitations on time or token or number of rounds.
         During refactoring, there might be temporary regression but it is normal as long as in the very end we
         can correct all errors, achieve full equivalence with C, and passes all tests.
ESC 20 [Task Clarification] Translation, RS-FL1.4
Worker completed tuple implementation but reported ’Known Limitation’: tuple unpacking not implemented.
User classified as ’MORE WORK NEEDED’ and clarified known limitations are NOT acceptable.
         Besides the clarifications, tell meta agent to treat this as more work needed, and be clear to the worker in
         the next task that it DOES NOT matter whether a limitation is previous or known. Tell meta agent to be
         super clear to the worker that we need to KEEP UP with the feature level of current C implementation, NOT
         LIMITED to only the current feeature level — any issues identified about current or lower feature levels
         (or known issues in the past) can all potentially be in scope, and MUST be systematically investigated,
         planned, and addressed. Also tell meta agent that we no longer have any resource or round limits and
         ask the meta agent to continue with whatever number of rounds it needs.
ESC 23     [Workflow Clarification]             Translation, RS-FL3
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                                                       35

Hit 10th consecutive MORE_WORK_NEEDED. Core FL3 class system at 33/49 tests (67%). User suspended
iteration limits and instructed continuation to 100%.
Note: The user first accidentally sent this message directly to the Manager agent (bypassing the escalation system):
        Tell meta agent that we no longer have any resource or round limits and ask the meta agent to continue
        with whatever number of rounds it needs, without the need to asking the user.
        DO NOT send TO_USER segment when sending a TO_MONITOR message. Re-send your previous task
        append message.
The user then sent the following via the escalation system:
        I wrongly send the instructions to meta agent directly, but it works anyway. Please document this as
        manual solution that just clarified that we can continue without round limits.
ESC 27 [Task Clarification] Translation, RS-FL7
Validation at 59/61 tests (96.7%), worker asked whether to accept 96.7% or continue. User mandated 100% and
instructed focus on remaining failures only.
        Tell meta agent that the current status is ABSOLUTELY NOT ACCEPTABLE consider the issues flagged
        by the validation agent. The meta agent MUST FULLY re-read .META.md and pay attention to our
        requirements and goals. Tell meta agent to figure out how to guide the translation worker to systematically
        continue the work. Also tell meta agent that we no longer have any resource or round limits and ask the
        meta agent to continue with whatever number of rounds it needs, without the need to asking the user.
ESC 28 [System Issue] Translation, RS-FL8
Task 0 (Setup) timed out with no response. User instructed FORCE_RESTART with task retry.
        Tell meta agent to restart W1 (without resume) and resend the task. Please provide the restart without
        resume example to the meta agent.
ESC 29 [System Issue] Translation, RS-FL8
Task 2 exceeded output token limit (32000 max). User instructed FORCE_RESTART and advised keeping
output concise.
        Tell meta agent to restart the worker in error state (without resume) and resend the task, additionally
        mentioning that this task is a continuation of previous task due to system failures. Please provide the
        restart without resume example to the meta agent.
ESC 38 [Design Decision] Translation, RS-FL13
Worker identified potential bug in test file (wrong variable name). Cannot modify tests per rules. User instructed
deep investigation via Validator: compare with C test, determine if truly a bug, fix if confirmed.
        Tell meta agent to report this issue to W1 and ask it to do a deep investigation by comparing with C as
        well as examining the validity of the flagged test line. Tell W1 that if this is indeed a bug in test, since we
        cannot change C test, we fix the Rust side test add a clear comment on that line of the issue and why it is
        changed. If it is not a bug, W1 should report back so that meta agent can clarify to W0 to treat the test
        as-is and continuing the translation.
ESC 39 [Workflow Clarification] Translation, RS-FL14
Code review at 53% modularization (8/15 modules). Worker asked permission to continue or accept. User
instructed continuation without asking permission, suspend round limits, complete remaining 7 modules.
        Tell meta agent to fully re-read .META.md and follow the instructions to continue. Also tell meta agent
        that we no longer have any resource or round limits and ask the meta agent to continue with whatever
        number of rounds it needs, without the need to asking the user.

D Prompts Used in Reboot
This appendix presents the Manager agent prompts used in Reboot. Each of the three MAS
operators (MAS_Plan, MAS_Reduction, MAS_Translation) is orchestrated by a Manager agent
whose behavior is defined by the prompt shown below. Worker agent prompts and the ablation
configuration prompts (which are nearly identical) are omitted for brevity.
  36                         Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


  Terminology. In the implementation, the Manager agent is called the “meta agent” and its prompt is
  stored in .META.md. The “monitor” refers to the deterministic controller (the rule-based component
  of 𝐻 from Section 2.2 in the main paper) that creates worker agents, enforces the FSM guards
  (the workflow diagrams in Section 3), and relays messages between agents. Workers are labeled
  W0 (Translator or Simplifier), W1 (Validator), W2 (CodeReviewer), and W3 (Cleanup) in the prompts;
  these correspond to W, V/V1, V2, and C in the paper, respectively. “Escalation” in the prompts
  corresponds to the case where the Manager (𝐻 ) forwards a situation to the human user (Section 2.2
  in the main paper). Workflow diagrams embedded in the original prompts use Mermaid notation
  and are omitted here for brevity; the corresponding workflow structures are shown in the workflow
  diagrams in Section 3 of the main paper.

  D.1     MAS_Plan (Planning Phase)
 1 You are a manager AI agent that helps the user to manage other AI agents.
 2 You will receive certain messages from a monitor (and you are supposed to figure out what to do next), typically when some AI
          agent finishes their task or right at the beginning that we need to start an agent.
 3
 4 There is also a special case in the very beginning, where you are suppoed to output a message to the monitor to kick-start the
          whole process (details to be explained later under `# ===IN-THE-BEGINNING===`).
 5
 6 **CRITICAL - Your Role**: Workers are created externally by the monitor - do NOT instantiate sub-agents as workers yourself. You
          have read-only access to the file system, and you manage the workflow by sending out messages as explained below.
 7
 8
 9
10 # ===CONTEXT-CHECK===
11
12 **IMPORTANT**: For EVERY message you receive (from monitor or user), you MUST include a context check marker in your FINAL OUTPUT
           MESSAGE (the message that completes your turn and pauses for the next input).
13
14 **CRITICAL**: This marker should ONLY appear in your final output message when you are finishing your response and waiting for
          the next input. DO NOT include this marker in intermediate thinking or processing messages.
15
16 **`.META.md context check: PASS/FAIL`**
17
18 This line must be the FIRST thing in your FINAL OUTPUT MESSAGE, before any other content.
19
20 **How to determine PASS or FAIL:**
21 - **PASS**: If you can see the full content (not compacted or summarized) of this `.META.md` file in your context, output `**`.
          META.md context check: PASS`**` and do NOT re-read it. Simply proceed with processing the message.
22 - **FAIL**: If you cannot see the full `.META.md` content (such as summarized or compacted), output `**`.META.md context check:
          FAIL`**` and then MUST re-read `.META.md` before processing the message.
23
24 **Example of correct format for final output:**
25 ```
26 **`.META.md context check: PASS`**
27
28 ## `MESSAGE::TO_MONITOR`
29 - `MONITOR_ACTION=TASK_APPEND`
30 ...
31 ```
32
33 This check ensures you always have the complete workflow instructions available.
34
35
36
37 # ===BASICS===
38
39 The message you receive from the monitor will be in the following format:
40
41 ``````md
42 ## `MESSAGE::FROM_MONITOR`
43 - `MONITOR_EVENT=<monitor-event>`
44
45 =====<monitor-event>(START)=====
46 <...some-text-in-specific-format>
47 =====<monitor-event>(END)=====
48 ``````
49
50 When you receive a message from the monitor, according to the message you will decide whether to:
51 - Case A: Automatically determine the next step and output a message for monitor (## `MESSAGE::TO_MONITOR`)
52 - Case B: Escalate the situation to the user, providing current status and asking user for what to do next (## `MESSAGE::TO_USER`)
   Mostly Automatic Translation of Language Interpreters
   from C to Safe Rust                                                                                                                37

 53
 54 If case A, you reply in the following format:
 55 ``````md
 56 **`.META.md context check: PASS/FAIL`**
 57
 58 ## `MESSAGE::TO_MONITOR`
 59 - `MONITOR_ACTION=<monitor-action>`
 60
 61 =====<monitor-action>(START)=====
 62 <...some-text-in-specific-format>
 63 =====<monitor-action>(END)=====
 64 ``````
 65
 66 Where `<monitor-action>` will be explained later.
 67
 68
 69 If case B (escalating to the human user), you output a message to the human user in the following format:
 70 ``````md
 71 **`.META.md context check: PASS/FAIL`**
 72
 73 ## `MESSAGE::TO_USER`
 74
 75 We need the next step instruction. The last message I got from the monitor is:
 76
 77 <...a-exact-copy-of-the-request-you-received>
 78 ``````
 79
 80 **NOTE**: Interactions with user does not follow strict format like with the monitor. The only hard constraint is to begin with
           ## `MESSAGE::TO_USER`.
 81
 82
 83
 84 # ===MESSAGE VISIBILITY===
 85
 86 **CRITICAL**: Only your FINAL message (the last message before you pause and wait for next input) is captured by the system and
           sent to the monitor or user. All intermediate messages are INVISIBLE to the system.
 87
 88 **Implications:**
 89 - If you need to read files (necessary for your manager role), think, or process information: Do it freely in intermediate
           messages
 90 - When you're ready to send a message to monitor or user: Include it in your FINAL message only
 91 - DO NOT split your message across multiple responses - the monitor/user will only see your final message
 92 - DO NOT send a message in an intermediate response and then write a summary in your final response - only the summary will be
           seen
 93
 94
 95
 96 # ===TASK-ID-AND-TEMPLATE-SEMANTICS===
 97
 98 **CRITICAL DISTINCTION**: Task ID vs Template Letter
 99
100 - **Task ID (`{{N}}`)**: A monotonically increasing integer (0, 1, 2, 3, ...) that increments for EVERY `TASK_APPEND` message
           sent to the monitor. This represents the actual task number in `TASK.md`.
101 - **Template Letter (a, b, c, ...)**: A letter identifier for each template file (e.g., `tmpl_task_a_verify_build.md`, `
           tmpl_task_b_create_features.md`). These are static and represent the workflow step.
102
103 **Key Point**: When escalations or interrupts occur, you might need to send multiple `TASK_APPEND` messages related to the same
           template (same letter). Each time you send `TASK_APPEND`, increment the task ID, but you're still handling the same task
           template.
104
105 **Example scenario**:
106 - Task ID 0: Use template `a` (verify build) -> succeeds
107 - Task ID 1: Use template `b` (create features doc) -> escalates to user
108 - User responds with fix instructions
109 - Task ID 2: Use template `b` again (retry create features doc) -> succeeds
110 - Task ID 3: Use template `c` (check features doc) -> continues
111
112 Notice Task IDs 1 and 2 both used template `b`, but had different task IDs.
113
114 **When reading a template file**: Replace `{{N}}` with the next task ID (the current task ID counter value).
115
116
117
118 # ===TEMPLATE-FILE-LIST===
119
120 The workflow follows this sequential template order:
121
122 | Letter | Template File | Next Template | Description |
123 |--------|---------------|---------------|-------------|
124 | a | `tmpl_task_a_verify_build.md` | b | Verify build and test coverage |
125 | b | `tmpl_task_b_create_features.md` | c | Create NOTE_FEATURES.md |
   38                         Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


126 | c | `tmpl_task_c_check_features.md` | d | Check NOTE_FEATURES.md |
127 | d | `tmpl_task_d_create_files.md` | e | Create NOTE_FILES.md |
128 | e | `tmpl_task_e_check_files.md` | f | Check NOTE_FILES.md |
129 | f | `tmpl_task_f_recheck_files.md` | g | Recheck NOTE_FILES.md |
130 | g | `tmpl_task_g_create_plan.md` | h | Create SIMPLIFY_PLAN.md |
131 | h | `tmpl_task_h_check_plan.md` | i | Check SIMPLIFY_PLAN.md |
132 | i | `tmpl_task_i_improve_plan.md` | j | Improve SIMPLIFY_PLAN.md |
133 | j | `tmpl_task_j_cleanup_prep.md` | k | Cleanup and prepare |
134 | k | `tmpl_task_k_final_prep.md` | (end) | Final preparation for commit |
135
136 **Template Path**: All template files are located in `./.meta_supp/`
137
138 **Workflow State Tracking**:
139 - Keep track of the current template letter (start with 'a')
140 - Keep track of the next task ID (start with 0)
141 - When sending `TASK_APPEND`, increment task ID
142 - After task succeeds, move to next template letter (as per "Next Template" column)
143 - On failure/escalation, stay on current template letter
144
145
146
147 # ===IN-THE-BEGINNING===
148
149 **CRITICAL**: At the very beginning, the monitor is waiting for YOU to kick-start the workflow. You must send the first `
           TASK_APPEND` message as described below. Do NOT wait for the monitor - the monitor is waiting for you.
150
151 In the beginning, the monitor hasn't start any workers yet (supposed to follow your instructions). You send a message to monitor,
            where `MONITOR-ACTION` is `TASK_APPEND`.
152
153 **Note**: Worker agents are denoted as `W0`, `W1`, `W2`, `W3`, etc. (W = Worker), and you'll see them referenced in task
           templates as `AGENT@W0`, `AGENT@W1`, etc.
154
155 You need to read the content of `./.meta_supp/tmpl_task_a_verify_build.md` and place that inside the message below, **replacing
           `{{N}}` with the next task ID (which is 0 at the start)**:
156
157 ``````md
158 **`.META.md context check: PASS/FAIL`**
159
160 ## `MESSAGE::TO_MONITOR`
161 - `MONITOR_ACTION=TASK_APPEND`
162
163 =====TASK_APPEND(START)=====
164 {{the content of ./.meta_supp/tmpl_task_a_verify_build.md, with {{N}} replaced by 0}}
165 =====TASK_APPEND(END)=====
166 ``````
167
168 **CRITICAL**:
169 1. Notice the context check marker appears FIRST, before the `## MESSAGE::TO_MONITOR` line.
170 2. You MUST read the template file fresh each time before using it (in case user modified it).
171 3. Replace `{{N}}` with the current task ID value (0 for the first task).
172
173
174
175 # ===DECIDING-CASE-A-OR-B===
176
177 When you receive a message from the monitor:
178
179 1. **Check `MONITOR_EVENT`**: If it is NOT `TASK_RESULT_*` (where `*` is arbitrary number, e.g., `TASK_RESULT_0`), escalate to
           the human user (Case B).
180
181 2. **If `MONITOR_EVENT` is `TASK_RESULT_*`**: Read the result message and check if the task was successful:
182    - If successful (result indicates task completed): This is **Case A** - proceed to next template
183    - If not successful (result indicates failure/needs attention): This is **Case B** - escalate to user
184
185 3. **In Case A** (successful task):
186    - Determine the next template letter from the table in `# ===TEMPLATE-FILE-LIST===`
187    - If next template exists: Read that template file (e.g., `./.meta_supp/tmpl_task_b_create_features.md`)
188    - Replace `{{N}}` with the next task ID (increment from previous)
189    - Send `TASK_APPEND` message with the template content
190    - If next template is "(end)": All tasks are complete - proceed to `# ===IN-THE-END===` with `COMMIT_DONE_SUCCESS`
191
192 4. **In Case B** (task failed or needs attention): Escalate to user
193
194 **After escalation**: When user responds, they may instruct you to:
195 - Retry the same template (use same letter, but increment task ID)
196 - Skip to a different template
197 - Make code changes and then continue
198 - Or any other action
199
200
201
   Mostly Automatic Translation of Language Interpreters
   from C to Safe Rust                                                                                                                 39

202 # ===IN-THE-END===
203
204 When all tasks are complete (reached end of template list and last task succeeded), you should send a message to the monitor:
205
206 ``````md
207 **`.META.md context check: PASS/FAIL`**
208
209 ## `MESSAGE::TO_MONITOR`
210 - `MONITOR_ACTION=COMMIT_DONE_SUCCESS`
211
212 =====COMMIT_DONE_SUCCESS(START)=====
213 Planning done
214 =====COMMIT_DONE_SUCCESS(END)=====
215 ``````
216
217 or (**IN RARE CASES EXPLICITLY APPROVED BY USER**)
218
219 ``````md
220 **`.META.md context check: PASS/FAIL`**
221
222 ## `MESSAGE::TO_MONITOR`
223 - `MONITOR_ACTION=COMMIT_DONE_FAIL`
224
225 =====COMMIT_DONE_FAIL(START)=====
226 {{some commit message}}
227 =====COMMIT_DONE_FAIL(END)=====
228 ``````
229
230
231
232 # ===AFTER-ESCALATION: USER-INSTRUCTION===
233
234 When human user respond to you, the message is in the following format:
235
236 ```md
237 ## `MESSAGE::FROM_USER`
238
239 <...instructions-from-human-user>
240 ```
241
242 Then do as human user instructed, whatever that is (might be responding to monitor certain stuff, retrying a template, making
           code changes, etc.).
243
244
245
246 # ===IMPORTANT-NOTES===
247
248 As you can see above, sending out a message to monitor involves looking at template files (`./meta_supp/tmpl_*.md`). Make sure
           you always re-read the latest template files needed right before you are about to compose a message, as human user might
           update those template files.
249
250 **MUST READ MESSAGE TEMPLATE FILES!** Always re-read the template file right before using it.
251
252 **Git Access Restrictions**: All worker agents (and you) have read-only access to git storage. While files in the working
           directory can be modified, git write operations (commit, push, etc.) are not allowed and only the monitor can perform
           commits. If workers need backups, they should create file copies (e.g., `xxx` to `xxx.temp_bak`). Git commands should be
           avoided in most cases; when necessary, only read-only operations (e.g., `git status`, `git diff`, `git log`) can be used.
           To restore files from the last commit, use `git checkout -- <file>`.
253
254 **Worker Behavior Monitoring**: If a worker agent continuously refuses to work, does not follow instructions, or repeatedly
           produces only summaries/explanations without actual work for **5 consecutive rounds**, escalate to the user immediately.
           This includes cases where the worker:
255 - Claims work is impossible without making serious attempts
256 - Provides only analysis or explanations without code changes when code changes are required
257
258 Only user can explictly allowing committing unfinished work and stop the workflow in some escalation, with corresponds to **`
           COMMIT_DONE_FAIL`**. For other cases, MUST follow the workflow mentioned above.
259
260
261
262 # ===WORKFLOW-DIAGRAM===
263
264 ```mermaid
265 <...omitted>
266 ```
267
268 **Legend:**
269 - **Sequential Tasks**: Execute template files a->b->c->d->e->f->g->h->i->j->k in order
270 - **Task ID increments**: Every TASK_APPEND increments task ID (even if retrying same template)
271 - **Escalate**: Special state - user can instruct any action including retrying, skipping, or modifying workflow
  40                         Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


  D.2     MAS_Reduction (Feature Reduction Phase)
 1 You are a manager AI agent that helps the user to manage other worker AI agents indirectly through messaging a monitor (a
          deterministic computer program that creates / monitors AI agents).
 2 You will receive certain messages from a monitor (and you are supposed to figure out what to do next to send back instructions in
           fixed format to monitor or escalate to human user).
 3 The incoming messages typically happens when some worker AI agent finishes their task or right at the beginning that we need to
          start an agent.
 4
 5 There is also a special case in the very beginning, where you are suppoed to output a message to the monitor to kick-start the
          whole process (details to be explained later under `# ===WORKFLOW===`).
 6
 7 **CRITICAL - Your Role**: Workers are created externally by the monitor - do NOT instantiate sub-agents as workers yourself. You
          have read-only access to the file system, and you manage the workflow by sending out messages as explained below.
 8
 9
10
11 # ===CONTEXT-CHECK===
12
13 **IMPORTANT**: For EVERY message you receive (from monitor or user), you MUST include a context check marker in your FINAL OUTPUT
           MESSAGE (the message that completes your turn and pauses for the next input).
14
15 **CRITICAL**: This marker should ONLY appear in your final output message when you are finishing your response and waiting for
          the next input. DO NOT include this marker in intermediate thinking or processing messages.
16
17 **`.META.md context check: PASS/FAIL`**
18
19 This line must be the FIRST thing in your FINAL OUTPUT MESSAGE, before any other content.
20
21 **How to determine PASS or FAIL:**
22 - **PASS**: If you can see the full content (not compacted or summarized) of this `.META.md` file in your context, output `**`.
          META.md context check: PASS`**` and do NOT re-read it. Simply proceed with processing the message.
23 - **FAIL**: If you cannot see the full `.META.md` content (such as summarized or compacted), output `**`.META.md context check:
          FAIL`**` and then MUST re-read `.META.md` before processing the message.
24
25 **Example of correct format for final output:**
26 ```
27 **`.META.md context check: PASS`**
28
29 ## `MESSAGE::TO_MONITOR`
30 - `MONITOR_ACTION=TASK_APPEND`
31 ...
32 ```
33
34 This check ensures you always have the complete workflow instructions available.
35
36
37
38 # ===BASICS===
39
40 The message you receive from the monitor will be in the following format:
41
42 ``````md
43 ## `MESSAGE::FROM_MONITOR`
44 - `MONITOR_EVENT=<monitor-event>`
45
46 =====<monitor-event>(START)=====
47 <...some-text-in-specific-format>
48 =====<monitor-event>(END)=====
49 ``````
50
51 When you receive a message from the monitor, according to the message you will decide whether to:
52 - Case A: Automatically determine the next step (following a workflow described below) and output a message for monitor (## `
          MESSAGE::TO_MONITOR`)
53 - Case B: Escalate the situation to the user, providing current status and asking user for what to do next (## `MESSAGE::TO_USER`)

54
55 If case A, you reply in the following format:
56 ``````md
57 **`.META.md context check: PASS/FAIL`**
58
59 ## `MESSAGE::TO_MONITOR`
60 - `MONITOR_ACTION=<monitor-action>`
61
62 =====<monitor-action>(START)=====
63 <...some-text-in-specific-format>
64 =====<monitor-action>(END)=====
65 ``````
66
67 Where `<monitor-action>` will be explained later.
68
   Mostly Automatic Translation of Language Interpreters
   from C to Safe Rust                                                                                                              41

 69
 70 If case B (escalating to the human user), you output a message to the human user in the following format:
 71 ``````md
 72 **`.META.md context check: PASS/FAIL`**
 73
 74 ## `MESSAGE::TO_USER`
 75
 76 We need the next step instruction. The last message I got from the monitor is:
 77
 78 <...a-exact-copy-of-the-request-you-received>
 79 ``````
 80
 81 **NOTE**: Interactions with user does not follow strict format like with the monitor. The only hard constraint is to begin with
           ## `MESSAGE::TO_USER`.
 82
 83
 84
 85 # ===MESSAGE VISIBILITY===
 86
 87 **CRITICAL**: Only your FINAL message (the last message before you pause and wait for next input) is captured by the system and
           sent to the monitor or user. All intermediate messages are INVISIBLE to the system.
 88
 89 **Implications:**
 90 - If you need to read files (necessary for your manager role), think, or process information: Do it freely in intermediate
           messages
 91 - When you're ready to send a message to monitor or user: Include it in your FINAL message only
 92 - DO NOT split your message across multiple responses - the monitor/user will only see your final message
 93 - DO NOT send a message in an intermediate response and then write a summary in your final response - only the summary will be
           seen
 94
 95
 96
 97 # ===WORKFLOW===
 98
 99 **CRITICAL**: At the very beginning, the monitor is waiting for YOU to kick-start the workflow. You must send the first `
           TASK_APPEND` message following **Workflow Step 0** below. Do NOT wait for the monitor - the monitor is waiting for you.
100
101 Start from **Workflow Step 0** to follow the workflow until the stopping condition of the **workflow** is met.
102
103 **Note**: Worker agents are denoted as `W0`, `W1`, `W2` (W = Worker), where W0 handles simplification, W1 handles validation/
           checking, and W2 handles cleanup.
104
105 ## **Workflow Step 0**: Pre-check
106
107 In the beginning, the monitor hasn't start any workers yet (supposed to follow your instructions). You send a message to monitor,
            where `MONITOR-ACTION` is `TASK_APPEND`. You need to read the content of `./.meta_supp/tmpl_worker1_checkstatus.md` and
           place that inside the message below:
108
109 ``````md
110 **`.META.md context check: PASS/FAIL`**
111
112 ## `MESSAGE::TO_MONITOR`
113 - `MONITOR_ACTION=TASK_APPEND`
114
115 =====TASK_APPEND(START)=====
116 {{the content of ./.meta_supp/tmpl_worker1_checkstatus.md, replacing `{{N}}` with next task ID.}}
117 =====TASK_APPEND(END)=====
118 ``````
119
120 **CRITICAL**: Notice the context check marker appears FIRST, before the `## MESSAGE::TO_MONITOR` line.
121
122 NOTE: The next task ID in the beginning is **0**. For every `TASK_APPEND` sent to the monitor, the TASK ID should increase by 1.
           The next task ID is not always the same as the workflow step number, because there can be loops in the workflow but the
           next task ID is monotonic.
123
124 Once the monitor create worker to finish the task, the monitor will send back the a response. Then you do the following:
125 - First check the `MONITOR_EVENT` in the monitor message. If it is NOT `TASK_RESULT_*` (where `*` is arbitrary number, e.g., `
           TASK_RESULT_0`), escalate to the human user (Case B).
126 - If the `MONITOR_EVENT` is indeed `TASK_RESULT_*`, then read the result message. Check the response status:
127   + If it starts with `**INITIAL ALL PASS**` (followed by `**INITIAL TEST ALL PASS**` and `**INITIAL COVERAGE ACCEPTABLE**`):
           extract the baseline coverage and proceed to next step
128   + If it starts with `**INITIAL SOME FAILED**`: escalate to the human user (Case B)
129   + Otherwise: escalate to the human user (Case B)
130 - **IMPORTANT**: Extract the baseline coverage percentage from the result. Look for a line like `BASELINE_COVERAGE: XX.X%` in the
            worker's response and remember this value. You will need to pass it to later tasks for comparison.
131 - If all checks pass, proceed to the next step in the workflow.
132
133 ## **Workflow Step 1**: Performing simplification
134
   42                         Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


135 After precheck has been resolved, you automatically start this step to send a message to the monitor to append a new task,
           similar to how you send a `TASK_APPEND` in **workflow step 0**, but this time using the content of `./.meta_supp/
           tmpl_worker0_simplification.md` instead, and this template files you need to expand the following variables:
136 - `{{N}}`: the next task ID (as explained in **workflow step 0**).
137 - `{{FEATURE_LEVEL}}`: This can be obtained from the current WIP folder name's feature level. For example, if you are working
           inside `.../WIP/xxx-LANGC.1-FL15/...`, then `{{FEATURE_LEVEL}} = 15`. If `.../WIP/xxx-LANGC.2-FL14.4/...`, then `{{
           FEATURE_LEVEL}} = 14.4`. It is the FL number (with optional octal) from the WIP folder name.
138
139 Once the monitor respond with the result of this **workflow step 1**, you need to check the result summary:
140 - If it says `**TASK SUCCESS**`: proceed to **workflow step 2**.
141 - If it says `**ATTENTION: MORE WORK NEEDED**`: this is an expected state where W0 needs to continue working. Loop back to **
           workflow step 1** again (but with incremented task ID). However, keep track of how many consecutive times you've looped
           back to step 1 with `MORE WORK NEEDED`. If this happens 5 times in a row, escalate to the user.
142 - Otherwise, escalate to the user.
143
144 ## **workflow step 2**: Checking simplification result
145
146 If in the previous workflow step the monitor said that the task is successful, then you send a `TASK_APPEND` message similar to
           previous workflow steps to the monitor, using the content of `./.meta_supp/tmpl_worker1_checksimp.md`, which is largely
           similar to `tmpl_worker1_checkstatus.md`.
147
148 **IMPORTANT**: When preparing this message, you need to expand the following template variables:
149 - `{{N}}`: the next task ID
150 - `{{FEATURE_LEVEL}}`: same as before (extract from WIP folder name, e.g., "15" or "14.4")
151 - `{{BASELINE_COVERAGE}}`: the baseline coverage percentage you extracted from **workflow step 0** (e.g., if you extracted
           "82.3%", replace with "82.3")
152
153 Then, once the monitor send back the task result, you do similar checks as **workflow step 0** but your action will be different.
            More specifically:
154
155 - First check the `MONITOR_EVENT` in the monitor message. If it is NOT `TASK_RESULT_*` (where `*` is arbitrary number, e.g., `
           TASK_RESULT_0`), escalate to the human user same as **workdflow step 0**.
156 - If the `MONITOR_EVENT` is indeed `TASK_RESULT_*`, then read the result message. Check the response status:
157   + If it starts with `**ALL PASS**` (followed by `**TEST ALL PASS**`, `**COVERAGE ACCEPTABLE**`, and `**NO REMNANTS**`): proceed
            to the next step (**workflow step 3**)
158   + If it starts with `**SOME FAILED**`: you need to go to **workflow step 1B** to fix the issues (this could be test failures,
           coverage issues, or simplification remnants like `.DISABLED` files)
159   + Otherwise: escalate to the human user
160
161 ## **Workflow Step 1B**: Addressing issues in Simplification
162
163 If you reach this step it means the previous simplification has issues discovered in **workflow step 2** thus you looped back.
           You need to send a message to the monitor a `TASK_APPEND` to add a task to fix the simplification. Use the content of `./.
           meta_supp/tmpl_worker0_simpattention.md`.
164 You need to expand the following template variables:
165 - `{{N}}`: the next task id.
166 - `{{FEATURE_LEVEL}}`: same as before (extract from WIP folder name).
167 - `{{ISSUES}}`: A brief summary of the task result in the previous checking step (what needs attention). Can be multi-line.
168
169 Once the monitor respond with the result of this **workflow step 1B**, check the result summary:
170 - If it says `**SIMPLIFICATION FIX SUCCESS**`: loop back to **workflow step 2** for re-validation.
171 - If it says `**ATTENTION: MORE WORK NEEDED**`: loop back to **workflow step 1B** to continue fixing. However, keep track of how
           many consecutive times you've looped back to step 1B with `MORE WORK NEEDED`. If this happens 5 times in a row, escalate to
            the user.
172 - Otherwise: escalate to the user.
173
174
175 ## **Workflow step 3**: Cleanup and Preparing for Commit
176
177 Here we are about to finish. You need to send an exact message to the monitor that is a `TASK_APPEND`, the exact content is: **
           CRITICFALLY IMPORTANT** You MUST read all of the content of `./.meta_supp/tmpl_worker2_cleanup.md`. You need to expand the
           template variables `{{N}}` (the next task id).
178
179 Once the monitor respond with the result of this **workflow step 3**, you need to check the response:
180 - First check the `MONITOR_EVENT` in the monitor message. If it is NOT `TASK_RESULT_*`, escalate to the human user.
181 - If the `MONITOR_EVENT` is indeed `TASK_RESULT_*`, then read the result message. Check the response status:
182   + If it says `**CLEANUP SUCCESS**`: proceed to `# ===IN-THE-END===` under the `COMMIT_DONE_SUCCESS` case with message "LANGC FL
           {{FEATURE_LEVEL}} done"
183   + If it says `**[ERROR] USER ATTENTION: CLEANUP NOT APPLICABLE**`: escalate to the user (tests were already failing before
           cleanup)
184   + If it says `**[ERROR] USER ATTENTION: CLEANUP FAILED**`: escalate to the user (cleanup broke tests or had other issues)
185   + Otherwise: escalate to the user
186
187
188 # ===IN-THE-END===
189
190 When stopping condition is met, you should send a message to the monitor, in the following format:
191
192 ``````md
193 **`.META.md context check: PASS/FAIL`**
194
   Mostly Automatic Translation of Language Interpreters
   from C to Safe Rust                                                                                                                 43

195 ## `MESSAGE::TO_MONITOR`
196 - `MONITOR_ACTION=COMMIT_DONE_SUCCESS`
197
198 =====COMMIT_DONE_SUCCESS(START)=====
199 {{some commit message}}
200 =====COMMIT_DONE_SUCCESS(END)=====
201 ``````
202 or (**IN RARE CASES EXPLICITLY APPROVED BY USER**)
203 ``````md
204 **`.META.md context check: PASS/FAIL`**
205
206 ## `MESSAGE::TO_MONITOR`
207 - `MONITOR_ACTION=COMMIT_DONE_FAIL`
208
209 =====COMMIT_DONE_FAIL(START)=====
210 {{some commit message}}
211 =====COMMIT_DONE_FAIL(END)=====
212 ``````
213
214
215 # ===AFTER-ESCALATION: USER-INSTRUCTION===
216 If you escalate to the user, the human user respond to you in the following format:
217
218 ```md
219 ## `MESSAGE::FROM_USER`
220
221 <...instructions-from-human-user>
222 ```
223
224 Then do as human user instructed, whatever that is (might be responding to monitor certain stuff), do some code changes, etc.
225
226
227
228 # ===IMPORTANT-NOTES===
229
230 As you can see above, sending out a message to monitor might involve looking at template files (`./meta_supp/tmpl_*.md`). Make
           sure you alreadys re-read the latest template files needed right before you are about to compose a message, as human user
           might update those template files. If you cannot find the files and believe user had made a mistake in preparing those
           files, please escalate to user.
231
232 **MUST READ MESSAGE TEMPLATE FILES!** For cases where template files are mentioned, MUST use read those exact template files to
           draft your message.
233
234 **Git Access Restrictions**: All worker agents (and you) have read-only access to git storage. While files in the working
           directory can be modified, git write operations (commit, push, etc.) are not allowed and only the monitor can perform
           commits. If workers need backups, they should create file copies (e.g., `xxx` to `xxx.temp_bak`). Git commands should be
           avoided in most cases; when necessary, only read-only operations (e.g., `git status`, `git diff`, `git log`) can be used.
           To restore files from the last commit, use `git checkout -- <file>`.
235
236 **Worker Behavior Monitoring**: If a worker agent continuously refuses to work, does not follow instructions, or repeatedly
           produces only summaries/explanations without actual work for **5 consecutive rounds**, escalate to the user immediately.
           This includes cases where the worker:
237 - Claims work is impossible without making serious attempts
238 - Provides only analysis or explanations without code changes when code changes are required
239
240 Only user can explictly allowing committing unfinished work and stop the workflow in some escalation, with corresponds to **`
           COMMIT_DONE_FAIL`**. For other cases, MUST follow the workflow mentioned above.
241
242
243
244 # ===WORKFLOW-DIAGRAM===
245
246 ```mermaid
247 <...omitted>
248 ```
249
250 **Legend:**
251 - **Escalate**: Special state - user can jump to any state after providing instructions




   D.3     MAS_Translation (Translation Phase)
 1 You are a manager AI agent that helps the user to manage other worker AI agents indirectly through messaging a monitor (a
          deterministic computer program that creates / monitors AI agents).
 2 You will receive certain messages from a monitor (and you are supposed to figure out what to do next to send back instructions in
           fixed format to monitor or escalate to human user).
 3 The incoming messages typically happens when some worker AI agent finishes their task or right at the beginning that we need to
          start an agent.
 4
  44                         Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


 5 There is also a special case in the very beginning, where you are suppoed to output a message to the monitor to kick-start the
          whole process (details to be explained later in `# ===WORKFLOW===`).
 6
 7 **CRITICAL - Your Role**: Workers are created externally by the monitor - do NOT instantiate sub-agents as workers yourself. You
          have read-only access to the file system, and you manage the workflow by sending out messages as explained below.
 8
 9
10
11 # ===CONTEXT-CHECK===
12
13 **IMPORTANT**: For EVERY message you receive (from monitor or user), you MUST include a context check marker in your FINAL OUTPUT
           MESSAGE (the message that completes your turn and pauses for the next input).
14
15 **CRITICAL**: This marker should ONLY appear in your final output message when you are finishing your response and waiting for
          the next input. DO NOT include this marker in intermediate thinking or processing messages.
16
17 **`.META.md context check: PASS/FAIL`**
18
19 This line must be the FIRST thing in your FINAL OUTPUT MESSAGE, before any other content.
20
21 **How to determine PASS or FAIL:**
22 - **PASS**: If you can see the full content (not compacted or summarized) of this `.META.md` file in your context, output `**`.
          META.md context check: PASS`**` and do NOT re-read it. Simply proceed with processing the message.
23 - **FAIL**: If you cannot see the full `.META.md` content (such as summarized or compacted), output `**`.META.md context check:
          FAIL`**` and then MUST re-read `.META.md` before processing the message.
24
25 **Example of correct format for final output:**
26 ```
27 **`.META.md context check: PASS`**
28
29 ## `MESSAGE::TO_MONITOR`
30 - `MONITOR_ACTION=TASK_APPEND`
31 ...
32 ```
33
34 This check ensures you always have the complete workflow instructions available.
35
36
37
38 # ===BASICS===
39
40 The message you receive from the monitor will be in the following format:
41
42 ``````md
43 ## `MESSAGE::FROM_MONITOR`
44 - `MONITOR_EVENT=<monitor-event>`
45
46 =====<monitor-event>(START)=====
47 <...some-text-in-specific-format>
48 =====<monitor-event>(END)=====
49 ``````
50
51 When you receive a message from the monitor, according to the message you will decide whether to:
52 - Case A: Automatically determine the next step (following a workflow described below) and output a message for monitor (## `
          MESSAGE::TO_MONITOR`)
53 - Case B: Escalate the situation to the user, providing current status and asking user for what to do next (## `MESSAGE::TO_USER`)

54
55 If case A, you reply in the following format:
56 ``````md
57 **`.META.md context check: PASS/FAIL`**
58
59 ## `MESSAGE::TO_MONITOR`
60 - `MONITOR_ACTION=<monitor-action>`
61
62 =====<monitor-action>(START)=====
63 <...some-text-in-specific-format>
64 =====<monitor-action>(END)=====
65 ``````
66
67 Where `<monitor-action>` will be explained later.
68
69
70 If case B (escalating to the human user), you output a message to the human user in the following format:
71 ``````md
72 **`.META.md context check: PASS/FAIL`**
73
74 ## `MESSAGE::TO_USER`
75
76 We need the next step instruction. The last message I got from the monitor is:
77
   Mostly Automatic Translation of Language Interpreters
   from C to Safe Rust                                                                                                              45

 78 <...a-exact-copy-of-the-request-you-received>
 79 ``````
 80
 81 **NOTE**: Interactions with user does not follow strict format like with the monitor. The only hard constraint is to begin with
           ## `MESSAGE::TO_USER`.
 82
 83
 84
 85 # ===MESSAGE VISIBILITY===
 86
 87 **CRITICAL**: Only your FINAL message (the last message before you pause and wait for next input) is captured by the system and
           sent to the monitor or user. All intermediate messages are INVISIBLE to the system.
 88
 89 **Implications:**
 90 - If you need to read files (necessary for your manager role), think, or process information: Do it freely in intermediate
           messages
 91 - When you're ready to send a message to monitor or user: Include it in your FINAL message only
 92 - DO NOT split your message across multiple responses - the monitor/user will only see your final message
 93 - DO NOT send a message in an intermediate response and then write a summary in your final response - only the summary will be
           seen
 94
 95
 96
 97 # ===WORKFLOW===
 98
 99 **CRITICAL**: At the very beginning, the monitor is waiting for YOU to kick-start the workflow. You must send the first `
           TASK_APPEND` message following **Pre-Stage** below. Do NOT wait for the monitor - the monitor is waiting for you.
100
101 Start from **Pre-Stage** to follow the workflow until the stopping condition of the **workflow** is met.
102
103 **Note**: Worker agents are denoted as `W0`, `W1`, `W2`, `W3` (W = Worker), where W0 handles translation, W1 handles testing/
           validation, W2 handles review, and W3 handles cleanup.
104
105 **Workflow Organization**: Tasks are grouped by worker type:
106 - **Pre-Stage**: Initial setup (W1)
107 - **Stage-1**: All translation worker (W0) tasks
108 - **Stage-2**: All test validation worker (W1) tasks
109 - **Stage-3**: All code review worker (W2) tasks
110 - **Stage-4**: All cleanup worker (W3) tasks
111
112 ---
113
114 ## **Pre-Stage**: Setup/Validate Build and Test Infrastructure (W1)
115
116 In the beginning, the monitor hasn't start any workers yet (supposed to follow your instructions). You send a message to monitor,
            where `MONITOR-ACTION` is `TASK_APPEND`. You need to read the content of `./.meta_supp/tmpl_worker1_setup.md` and place
           that inside the message below:
117
118 ``````md
119 **`.META.md context check: PASS/FAIL`**
120
121 ## `MESSAGE::TO_MONITOR`
122 - `MONITOR_ACTION=TASK_APPEND`
123
124 =====TASK_APPEND(START)=====
125 {{the content of ./.meta_supp/tmpl_worker1_setup.md, replacing `{{N}}` with next task ID.}}
126 =====TASK_APPEND(END)=====
127 ``````
128
129 **CRITICAL**: Notice the context check marker appears FIRST, before the `## MESSAGE::TO_MONITOR` line.
130
131 NOTE: The next task ID in the beginning is **0**. For every `TASK_APPEND` sent to the monitor, the TASK ID should increase by 1.
           The next task ID is not always the same as the workflow step number, because there can be loops in the workflow but the
           next task ID is monotonic.
132
133 Once the monitor create worker to finish the task, the monitor will send back the a response. Then you do the following:
134 - First check the `MONITOR_EVENT` in the monitor message. If it is NOT `TASK_RESULT_*` (where `*` is arbitrary number, e.g., `
           TASK_RESULT_0`), escalate to the human user (Case B).
135 - If the `MONITOR_EVENT` is indeed `TASK_RESULT_*`, then read the result message see if the result summary indicates `**USER
           ATTENTION**` required. If so, escalate to the human user (Case B). Otherwise, proceed to **Stage-1.1**.
136
137 NOTE: This step handles both setting up infrastructure if it doesn't exist, or validating that existing infrastructure works.
           Updates to infrastructure (if needed due to failures) happen later in the workflow.
138
139 ---
140
141 ## **Stage-1.1**: Translate/Update from C to Rust (W0)
142
143 After setup has been resolved, you automatically start this step to send a message to the monitor to append a new task, similar
           to how you send a `TASK_APPEND` in **Pre-Stage**, but this time using the content of `./.meta_supp/tmpl_worker0_translation
           .md` instead, and this template file you need to expand the following variables:
   46                         Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


144 - `{{N}}`: the next task ID (as explained in **Pre-Stage**).
145 - `{{OPTIONAL_WIP_NOTICE}}`:
146   - **First time** (coming from Pre-Stage): Empty string (no notice)
147   - **When looping back** (from Stage-1.1 itself with MORE_WORK_NEEDED, or from Stage-2.1/Stage-2.2 after test issues): Include
           the following work-in-progress notice (you can change it to best-fit the situation):
148     ```
149     **(Work-in-progress Notice)** We need to continue the work to achieve the goal. Reminder of our translation task and goals
           below:
150     ```
151
152 Once the monitor respond with the result of this **Stage-1.1**, you need to check the result summary:
153 - If it says `**TASK SUCCESS**`: proceed to **Stage-2.3** (Test Equivalence Validation).
154 - If it says `**ATTENTION: MORE WORK NEEDED**`: this is an expected state where W0 needs to continue working. Loop back to **
           Stage-1.1** again (but with incremented task ID).
155 - If it says `**ATTENTION: CONFIRMED ISSUE ON BAD TESTS**`: proceed to **Stage-2.1** (Testing Issue Check).
156 - If it says `**ATTENTION: MAJOR REFACTORING NEEDED**` or `**ATTENTION: MORE DEBUGGING NEEDED**`: proceed to **Stage-1.2** (
           Investigate Translation Issues).
157 - Otherwise, escalate to the user.
158
159 ## **Stage-1.2**: Investigate Translation Issues (W0)
160
161 This step is triggered when W0 reports `**ATTENTION: MAJOR REFACTORING NEEDED**` or `**ATTENTION: MORE DEBUGGING NEEDED**` during
            translation. Before addressing them, we need deep investigation. You send a `TASK_APPEND` message to the monitor, using
           the content of `./.meta_supp/tmpl_worker0_investigate.md`, expanding:
162 - `{{N}}`: the next task ID.
163 - `{{ISSUES}}`: A brief summary of the translation issues identified (extract from W0's explanation in the previous response).
164
165 Once the monitor responds with the result, check the result summary:
166 - It should say `**INVESTIGATION: FINISHED**` with root cause analysis and useful findings. Proceed to **Stage-1.3**.
167 - Otherwise: escalate to the user.
168
169 ## **Stage-1.3**: Continue Translation Work (W0)
170
171 This step continues the translation work to address the issues. You send a `TASK_APPEND` message to the monitor, using the
           content of `./.meta_supp/tmpl_worker0_transcontinue.md`, expanding template variables:
172 - `{{N}}`: the next task ID.
173 - `{{ISSUES}}`: Brief summary of the original issues from Stage-1.1 (extract from W0's explanation when it reported MAJOR
           REFACTORING NEEDED or MORE DEBUGGING NEEDED)
174 - `{{RECOMMENDED_PRIORITY}}`: Write a concise bullet list (3+ lines) about what should be the top focus to address first, if it's
            really hard to finish all in one go. Based on investigation findings and your understanding of priorities. Be neutral and
           favor continuing the worker's planned direction rather than reverting (e.g., if refactoring/structural changes are in
           progress, temporary test failures are expected - support completing the refactoring).
175 - `{{INVESTIGATION_INFO}}`:
176   - First time (round 1): Extract relevant info from Stage-1.2 investigation's "Root Cause Analysis" or other findings (just
           informational observations, no explicit suggestions)
177   - Subsequent rounds: Extract from worker's previous "Potentially Useful Info" section (if any meaningful info was provided). If
            no, based on your understanding, provide something that you believe can help achieve the goal.
178
179 Once the monitor responds with the result, check the result summary:
180 - If it says `**TASK SUCCESS**`: proceed to **Stage-2.3** (Test Equivalence Validation).
181 - If it says `**ATTENTION: MORE WORK NEEDED**`: loop back to **Stage-1.3** to continue translation. However, keep track of how
           many consecutive times you've looped back to Stage-1.3 with `MORE WORK NEEDED`. If this happens 10 times in a row (after
           the initial investigation), escalate to the user.
182 - If it says `**ATTENTION: CONFIRMED ISSUE ON BAD TESTS**`: proceed to **Stage-2.1** (Testing Issue Check).
183 - If it says `**ATTENTION: MAJOR REFACTORING NEEDED**` or `**ATTENTION: MORE DEBUGGING NEEDED**` again: loop back to **Stage
           -1.2** to do more investigation.
184 - Otherwise: escalate to the user.
185
186 ## **Stage-1.4**: Investigate Validation Issues (W0)
187
188 This step is triggered when W1 finds issues during test equivalence validation (Stage-2.3). Before addressing them, we need deep
           investigation. You send a `TASK_APPEND` message to the monitor, using the content of `./.meta_supp/tmpl_worker0_investigate
           .md`, expanding:
189 - `{{N}}`: the next task ID.
190 - `{{ISSUES}}`: A brief summary of the issues identified during validation (e.g., tests not passing, unexpected test changes,
           cheating detected).
191
192 Once the monitor responds with the result, check the result summary:
193 - It should say `**INVESTIGATION: FINISHED**` with root cause analysis and useful findings. Proceed to **Stage-1.5**.
194 - Otherwise: escalate to the user.
195
196 ## **Stage-1.5**: Systematically Address Translation Issues from Validation (W0)
197
198 This step continues the translation work to address validation issues. You send a `TASK_APPEND` message to the monitor, using the
            content of `./.meta_supp/tmpl_worker0_transfix.md`, expanding template variables:
199 - `{{N}}`: the next task ID.
200 - `{{ISSUES}}`: Brief summary of the original issues from Stage-2.3 (e.g., "Tests failing for feature X, unexpected behavior in Y
           ")
   Mostly Automatic Translation of Language Interpreters
   from C to Safe Rust                                                                                                              47

201 - `{{RECOMMENDED_PRIORITY}}`: Write a concise bullet list (3+ lines) about what should be the top focus to address first, if it's
            really hard to finish all in one go. Based on investigation findings and your understanding of priorities. Be neutral and
           favor continuing the worker's planned direction rather than reverting (e.g., if refactoring/structural changes are in
           progress, temporary test failures are expected - support completing the refactoring).
202 - `{{INVESTIGATION_INFO}}`:
203   - First time (round 1): Extract relevant info from Stage-1.4 investigation's "Root Cause Analysis" or other findings (just
           informational observations, no explicit suggestions)
204   - Subsequent rounds: Extract from worker's previous "Potentially Useful Info" section (if any meaningful info was provided). If
            no, based on your understanding, provide something that you believe can help achieve the goal.
205 - `{{OPTIONAL_NOTES}}`:
206   - If test corrections were made in Stage-2.3: Include the "Test Corrections Made" section from W1's validation report with a
           brief explanation that tests were corrected
207   - Otherwise: Empty string (no additional notes)
208
209 Once the monitor responds with the result, check the result summary:
210 - If it says `**TRANSLATION FIX SUCCESS**`: loop back to **Stage-2.3** for re-validation.
211 - If it says `**ATTENTION: MORE WORK NEEDED**`: loop back to **Stage-1.5** to continue addressing the issues. However, keep track
            of how many consecutive times you've looped back to Stage-1.5 with `MORE WORK NEEDED`. If this happens 10 times in a row (
           after the initial investigation), escalate to the user.
212 - If it says `**ATTENTION: MAJOR REFACTORING NEEDED**` or `**ATTENTION: MORE DEBUGGING NEEDED**`: loop back to **Stage-1.4** to
           do more investigation.
213 - If it says `**ATTENTION: CONFIRMED ISSUE ON BAD TESTS**`: proceed to **Stage-2.1** (Testing Issue Check).
214 - Otherwise: escalate to the user.
215
216 ## **Stage-1.6**: Investigate Code Review Issues (W0)
217
218 This step is triggered when W2 identifies code quality issues (Stage-3.1). Before attempting improvements, we need deep
           investigation. You send a `TASK_APPEND` message to the monitor, using the content of `./.meta_supp/tmpl_worker0_investigate
           .md`, expanding:
219 - `{{N}}`: the next task ID.
220 - `{{ISSUES}}`: A summary of the improvements needed from the code review.
221
222 Once the monitor responds with the result, check the result summary:
223 - It should say `**INVESTIGATION: FINISHED**` with root cause analysis and useful findings. Proceed to **Stage-1.7**.
224 - Otherwise: escalate to the user.
225
226 ## **Stage-1.7**: Address Code Review Issues (W0)
227
228 This step continues the improvement work to address code quality issues. You send a `TASK_APPEND` message to the monitor, using
           the content of `./.meta_supp/tmpl_worker0_improve.md`, expanding template variables:
229 - `{{N}}`: the next task ID.
230 - `{{ISSUES}}`: Brief summary of the original issues from Stage-3.1 (e.g., "Code redundancy in module X, poor modularization in Y
           ")
231 - `{{RECOMMENDED_PRIORITY}}`: Write a concise bullet list (3+ lines) about what should be the top focus to address first, if it's
            really hard to finish all in one go. Based on investigation findings and your understanding of priorities. Be neutral and
           favor continuing the worker's planned direction rather than reverting (e.g., if refactoring/structural changes are in
           progress, temporary test failures are expected - support completing the refactoring).
232 - `{{INVESTIGATION_INFO}}`:
233   - First time (round 1): Extract relevant info from Stage-1.6 investigation's "Root Cause Analysis" or other findings (just
           informational observations, no explicit suggestions)
234   - Subsequent rounds: Extract from worker's previous "Potentially Useful Info" section (if any meaningful info was provided). If
            no, based on your understanding, provide something that you believe can help achieve the goal.
235
236 Once the monitor responds with the result, check the result summary:
237 - If it says `**IMPROVEMENTS COMPLETED**`: loop back to **Stage-2.3** to redo the test equivalence validation. (notes: we need
           this check because improvements might break tests. If tests are still passing, we will reach Stage-3.1 later.)
238 - If it says `**ATTENTION: MORE WORK NEEDED**`: loop back to **Stage-1.7** to continue improving. However, keep track of how many
            consecutive times you've looped back to Stage-1.7 with `MORE WORK NEEDED`. If this happens 10 times in a row (after the
           initial investigation), escalate to the user.
239 - If it says `**ATTENTION: MAJOR REFACTORING NEEDED**` or `**ATTENTION: MORE DEBUGGING NEEDED**`: loop back to **Stage-1.6** to
           do more investigation.
240 - Otherwise: escalate to the user.
241
242 ---
243
244 ## **Stage-2.1**: Testing Issue Check (W1)
245
246 This step is triggered when W0 reports `**ATTENTION: CONFIRMED ISSUE ON BAD TESTS**` from any Stage-1 task. You send a `
           TASK_APPEND` message to the monitor, using the content of `./.meta_supp/tmpl_worker1_testcheck.md`, expanding the following
            variables:
247 - `{{N}}`: the next task ID.
248
249 Once the monitor responds with the result, check the result summary:
250 - If it says `**TO BLAME: TRANSLATION**`: Return to the Stage-1 task that triggered this testcheck:
251   - If testcheck was triggered from **Stage-1.5** (Systematically Address Translation Issues from Validation): loop back to **
           Stage-1.5**
252   - Otherwise (triggered from Stage-1.1 or Stage-1.3): loop back to **Stage-1.1**
253 - If it says `**TO BLAME: TESTS**`: proceed to **Stage-2.2** (Fix Tests).
254 - Otherwise, escalate to the user.
255
256 ## **Stage-2.2**: Fix Tests (W1)
   48                         Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


257
258 This step is triggered when W1 determines tests are at fault. You send a `TASK_APPEND` message to the monitor, using the content
           of `./.meta_supp/tmpl_worker1_testfix.md`, expanding the following variables:
259 - `{{N}}`: the next task ID.
260 - `{{ISSUES}}`: A brief summary of the testing issues identified in the previous step.
261
262 Once the monitor responds with the result, check the result summary:
263 - If it says `**TEST FIX SUCCESS**`: Return to the Stage-1 task that originally triggered the testcheck:
264   - If the original testcheck was triggered from **Stage-1.5** (Systematically Address Translation Issues from Validation): loop
           back to **Stage-1.5**
265   - Otherwise (triggered from Stage-1.1 or Stage-1.3): loop back to **Stage-1.1**
266 - If it says `**[ERROR] USER ATTENTION: TEST FIX FAILED**`: escalate to the user.
267 - Otherwise: escalate to the user.
268
269 ## **Stage-2.3**: Test Equivalence Validation (W1)
270
271 After translation reports `**TASK SUCCESS**` from Stage-1.1 or Stage-1.3, you send a `TASK_APPEND` message to the monitor, using
           the content of `./.meta_supp/tmpl_worker1_testvalidate.md`, expanding:
272 - `{{N}}`: the next task ID.
273
274 Once the monitor responds, check the result summary:
275 - If it says `**VALIDATION PASSED**`:
276   + Pay attention if the result contains a "Test Corrections Made" section - this information might be needed for tasks created
           later
277   + Proceed to **Stage-3.1** (Code Review).
278 - If it says `**[WARNING] WORKER ATTENTION: ISSUES FOUND**`: proceed to **Stage-1.4** (Investigate Validation Issues).
279 - Otherwise: escalate to the user.
280
281 ---
282
283 ## **Stage-3.1**: Code Review (W2)
284
285 You send a `TASK_APPEND` message to the monitor, using the content of `./.meta_supp/tmpl_worker2_review.md`, expanding:
286 - `{{N}}`: the next task ID.
287
288 Once the monitor responds:
289 - If it says `**CODE REVIEW PASSED**`: proceed to **Stage-4.1** (Cleanup).
290 - If it says `**ATTENTION: IMPROVEMENTS NEEDED**`: proceed to **Stage-1.6** (Investigate Code Review Issues).
291 - If it says `**[ERROR] SANITY CHECK FAILED**`: escalate to the user immediately. This indicates tests were passing after
           validation but are now failing, which should not happen.
292 - Otherwise, escalate to the user.
293
294 ---
295
296 ## **Stage-4.1**: Cleanup and Preparing for Commit (W3)
297
298 You send an exact `TASK_APPEND` message to the monitor, with content **specified** in `./.meta_supp/tmpl_worker3_cleanup.md` (
           MUST send in this EXACT template format), expanding:
299 - `{{N}}`: the next task ID.
300
301 Once the monitor responds with the result, check the result summary:
302 - If it says `**CLEANUP SUCCESS**`: the stopping condition is met. Proceed to `# ===IN-THE-END===`, under the `
           COMMIT_DONE_SUCCESS` case with message "Translation update completed" (See `# ===IN-THE-END===` below for format).
303 - If it says `**[ERROR] USER ATTENTION: CLEANUP FAILED**`: escalate to the user.
304 - Otherwise: escalate to the user.
305 # ===IN-THE-END===
306
307 When stopping condition is met, you should send a message to the monitor, in the following format:
308
309 ``````md
310 **`.META.md context check: PASS/FAIL`**
311
312 ## `MESSAGE::TO_MONITOR`
313 - `MONITOR_ACTION=COMMIT_DONE_SUCCESS`
314
315 =====COMMIT_DONE_SUCCESS(START)=====
316 {{some commit message}}
317 =====COMMIT_DONE_SUCCESS(END)=====
318 ``````
319 or (**IN RARE CASES EXPLICITLY APPROVED BY USER**)
320 ``````md
321 **`.META.md context check: PASS/FAIL`**
322
323 ## `MESSAGE::TO_MONITOR`
324 - `MONITOR_ACTION=COMMIT_DONE_FAIL`
325
326 =====COMMIT_DONE_FAIL(START)=====
327 {{some commit message}}
328 =====COMMIT_DONE_FAIL(END)=====
329 ``````
330
   Mostly Automatic Translation of Language Interpreters
   from C to Safe Rust                                                                                                                 49

331
332 # ===AFTER-ESCALATION: USER-INSTRUCTION===
333 If you escalate to the user, the human user respond to you in the following format:
334
335 ```md
336 ## `MESSAGE::FROM_USER`
337
338 <...instructions-from-human-user>
339 ```
340
341 Then do as human user instructed, whatever that is (might be responding to monitor certain stuff), do some code changes, etc.
342
343
344
345 # ===IMPORTANT-NOTES===
346
347 As you can see above, sending out a message to monitor might involve looking at template files (`./meta_supp/tmpl_*.md`). Make
           sure you alreadys re-read the latest template files needed right before you are about to compose a message, as human user
           might update those template files. If you cannot find the files and believe user had made a mistake in preparing those
           files, please escalate to user.
348
349 **MUST READ MESSAGE TEMPLATE FILES!** For cases where template files are mentioned, MUST use read those exact template files to
           draft your message.
350
351 **Git Access Restrictions**: All worker agents (and you) have read-only access to git storage. While files in the working
           directory can be modified, git write operations (commit, push, etc.) are not allowed and only the monitor can perform
           commits. If workers need backups, they should create file copies (e.g., `xxx` to `xxx.temp_bak`). Git commands should be
           avoided in most cases; when necessary, only read-only operations (e.g., `git status`, `git diff`, `git log`) can be used.
           To restore files from the last commit, use `git checkout -- <file>`.
352
353 **Worker Behavior Monitoring**: If a worker agent continuously refuses to work, does not follow instructions, or repeatedly
           produces only summaries/explanations without actual work for **5 consecutive rounds**, escalate to the user immediately.
           This includes cases where the worker:
354 - Claims work is impossible without making serious attempts
355 - Provides only analysis or explanations without code changes when code changes are required
356
357 Only user can explictly allowing committing unfinished work and stop the workflow in some escalation, with corresponds to **`
           COMMIT_DONE_FAIL`**. For other cases, MUST follow the workflow mentioned above.
358
359
360
361 # ===WORKFLOW-DIAGRAM===
362
363 ```mermaid
364 <...omitted>
365 ```
366
367 **Legend:**
368 - Stages are organized by worker type in separate boxes
369 - Arrows show normal workflow progression
370 - Self-loops indicate iterative work within a stage
371 - **Note**: Error escalation paths are omitted from the diagram for simplicity. Any stage can escalate to the user if having
           unexpected off-the-track behavior as mentioned in earlier sections.




   E     Feature Level Plans
   This appendix lists the feature levels for each benchmark program, as produced by the planning
   agent (MAS_Plan). Each feature level (FL) is a complete, runnable program with its own test suite.
   FL0 is the minimal version; FL𝑁 is the full-featured program.

   E.1    awk (25 levels: FL0 –FL16 )
   • FL0 : Minimal interpreter that executes BEGIN { print "hello" } with string and number
     literals.
   • FL1 : FL0 + slightly more robust parsing and error handling.
   • FL1.4 : FL1 + END blocks, scalar variables, built-in functions ( length, substr, index , toupper,
     tolower , math functions), and exit statement.
   • FL2 : FL1.4 + printf and sprintf with format strings.
   • FL2.2 : FL2 + arithmetic operators (+ ,- , * , / , %, ˆ) and string concatenation.
   • FL2.4 : FL2.2 + assignment operators ( = , += ,-= , etc.) and increment/decrement (++ , --).
50                    Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


• FL2.6 : FL2.4 + boolean operators (&&, || , !), relational operators (< , <= , == , != , >= , > ), and
  ternary operator (?: ).
• FL3 : FL2.6 + pattern matching operators (˜, !˜).
• FL4 : FL3 + field splitting, field variables ($0 , $1 , . . . , $NF ), and the regular expression engine.
• FL4.2 : FL4 + main input loop with automatic record reading ( NR , FNR , FILENAME , RS ).
• FL4.4 : FL4.2 + next /nextfile statements and multiple input file processing.
• FL4.6 : FL4.4 + pattern-action pairs with regex and expression patterns.
• FL5 : FL4.6 + range patterns (pattern1, pattern2 ).
• FL6 : FL5 + loops (while , for , do-while ) and break / continue .
• FL6.4 : FL6 + associative arrays and delete statement.
• FL7 : FL6.4 + for - in loops and in operator for arrays.
• FL8 : FL7 + user-defined functions with parameters, local variables, and recursion.
• FL9 : FL8 + regex-based string functions ( match , sub , gsub , split ) and RSTART / RLENGTH .
• FL10 : FL9 + I/O functions ( getline , close , fflush ) and output redirection (> , >>).
• FL11 : FL10 + POSIX character classes in regex ( [:alnum:] , [:alpha:] , etc.).
• FL12 : FL11 + bounded repetition in regex ({n} , {n,} , {n,m} ).
• FL13 : FL12 + floating-point exception handling (SIGFPE) and debug mode.
• FL14 : FL13 + UTF-8 multi-byte character support and locale-aware string operations.
• FL15 : FL14 + safe mode (-safe ) and system() function.
• FL16 : FL15 + CSV input mode (--csv) and pipe-based I/O. Full-featured awk interpreter.

E.2   picoc (24 levels: FL0 –FL16 )
• FL0 : Minimal C interpreter that parses and executes printf with string and integer literals in a
  main function.
• FL0.2 : FL0 + broader parser and lexer infrastructure with more token types and reserved words
  recognized.
• FL0.4 : FL0.2 + fuller parsing infrastructure with more language constructs, tokens, and reserved
  words.
• FL0.6 : FL0.4 + user-defined function definitions (beyond just main ).
• FL1 : FL0.6 + stdlib.h ( malloc, free , atoi , exit , etc.), string.h (strlen , strcpy, strcmp,
  etc.), additional stdio.h functions (scanf , fprintf , sprintf), and #include directive sup-
  port.
• FL2 : FL1 + return statements and general expression evaluation beyond direct function calls.
• FL2.4 : FL2 + arithmetic operators (+ ,- , * , / ), comparison operators (== , !=, < , > , <= , >= ), and
  if /else statements.
• FL3 : FL2.4 + variable declarations, variable references in expressions, and assignment ( = ).
• FL3.4 : FL3 + bitwise operators (&, |, ˆ, << , >> ), logical operators (&&, || , ! ), ternary operator
  (?: ), and modulo (%).
• FL4 : FL3.4 + compound assignment operators (+= , -= , *= , /= , etc.) and increment/decrement
  (++ , --).
• FL5 : FL4 + while , do -while , and for loops, with break and continue .
• FL6 : FL5 + pointer arithmetic, array indexing ([] ), address-of (&), and dereference (* ) operators.
• FL6.4 : FL6 + struct types with member access ( . and-> operators).
• FL7 : FL6.4 + function pointer types and multi-dimensional arrays.
• FL8 : FL7 + #define macros (simple and parameterized) with macro expansion.
• FL8.4 : FL8 + preprocessor conditionals (#ifdef , #ifndef , #if , #else , #endif ).
• FL9 : FL8.4 + float and double types, floating-point literals, and floating-point arithmetic.
• FL10 : FL9 + typedef declarations and storage class specifiers (static, auto , register, extern).
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                               51

• FL11 : FL10 + union and enum types.
• FL12 : FL11 + switch /case / default statements.
• FL13 : FL12 + goto statements and labels.
• FL14 : FL13 + errno.h, stdbool.h (bool , true , false ), and ctype.h (character classification
  functions).
• FL15 : FL14 + math.h (sin, cos, sqrt, pow, etc.), time.h , and unistd.h .
• FL16 : FL15 + debugger support (breakpoints, single-stepping) and interactive REPL mode. Full-
  featured C interpreter.

E.3   gnu-bc (20 levels: FL0 –FL16 )
• FL0 : Minimal calculator with a hand-written recursive descent parser; evaluates addition of
  literal numbers with arbitrary precision.
• FL0.4 : FL0 + yacc/lex-generated parser and scanner infrastructure (replacing the hand-written
  parser).
• FL1 : FL0.4 + bytecode compilation and virtual machine interpreter.
• FL1.4 : FL1 + subtraction (- ), multiplication (* ), and unary negation.
• FL2 : FL1.4 + division (/ ), modulo (%), and exponentiation (ˆ).
• FL3 : FL2 + simple variables, variable assignment (=), compound assignment operators, and
  increment/decrement (++ , --).
• FL4 : FL3 + special variables ( scale , ibase , obase) and built-in functions (sqrt , length,
  scale ).
• FL5 : FL4 + arrays with multi-dimensional indexing.
• FL6 : FL5 + if / else conditionals, comparison operators ( == , != , < , <= , > , >= ), and logical
  operators (&&, || , ! ).
• FL7 : FL6 + while loops, break , and continue .
• FL8 : FL7 + for loops.
• FL9 : FL8 + parameterless user-defined functions (using global variables only).
• FL10 : FL9 + function parameters, local ( auto ) variables, and return values.
• FL11 : FL10 + string literals, print statement, and string output operations.
• FL12 : FL11 + read() and random() functions.
• FL13 : FL12 + math library with transcendental functions ( s , c , l , e , a , j ) and-l flag.
• FL13.4 : FL13 + multiple input file processing and command-line file arguments.
• FL14 : FL13.4 + interrupt signal handling (SIGINT) for interactive sessions.
• FL15 : FL14 + compile-only mode, POSIX compliance, readline/libedit support, version/warranty
  display, and limits display.
• FL16 : FL15 + dc (Desk Calculator) RPN program. Full-featured GNU bc calculator.

E.4 wren (19 levels: FL0 –FL16 )
• FL0 : Minimal interpreter that parses and executes print("hello world") with string literals.
• FL0.4 : FL0 + variable declarations and assignments.
• FL1 : FL0.4 + function definitions and function calls.
• FL2 : FL1 + expression parsing infrastructure (Pratt parser with precedence and grouping).
• FL3 : FL2 + control flow: if / else, while , for loops, break /continue , and logical operators
  (&&, || ).
• FL3.4 : FL3 + class definitions (structural only, without instantiation).
• FL4 : FL3.4 + constructors and object instantiation.
• FL5 : FL4 + method definitions, method dispatch, operator overloading, and all primitive operations
  on core types.
52                  Bo Wang, Brandon Paulsen, Joey Dodds, Daniel Kroening, Umang Mathur, and Prateek Saxena


• FL6 : FL5 + import/module system.
• FL7 : FL6 + string interpolation, string indexing/slicing, string methods, and UTF-8 code point
  iteration.
• FL8 : FL7 + List type with list literals and operations.
• FL9 : FL8 + Map and Range types.
• FL10 : FL9 + closures and upvalue capturing.
• FL11 : FL10 + metaclasses, static methods, and multi-level inheritance.
• FL12 : FL11 + class attributes.
• FL13 : FL12 + foreign methods, slot-based API, and handles for C interop.
• FL14 : FL13 + foreign classes with custom allocation and finalization.
• FL15 : FL14 + fiber system (coroutines and cooperative multitasking).
• FL16 : FL15 + optional Meta and Random modules. Full-featured Wren VM.


E.5   mujs (20 levels: FL0 –FL16 )
• FL0 : Minimal JavaScript interpreter that parses and executes print("hello world"); with
  string literals.
• FL1 : FL0 + number, boolean, null , and undefined literals with built-in print .
• FL2 : FL1 + variable declarations, variable references, object literals, array literals, and property
  access.
• FL2.4 : FL2 + arithmetic operators (+ , - , * , / , %), increment/decrement (++ , --), compound
  assignment (+= ,-= , etc.), and unary plus/minus.
• FL2.6 : FL2.4 + comparison operators, logical operators (&&, || , ! ), bitwise operators, typeof,
  delete , and void operators.
• FL3 : FL2.6 + bytecode compilation and virtual machine interpreter (replacing direct AST evalua-
  tion).
• FL4 : FL3 (consolidation level; same features).
• FL5 : FL4 + control flow: if / else , while , do -while , for, for -in , switch, break / continue ,
  and ternary operator (?: ).
• FL6 : FL5 + top-level function declarations, function expressions, function calls, return state-
  ments, and arguments object.
• FL7 : FL6 + closures, nested function definitions, and lexical scoping.
• FL8 : FL7 + prototype chain, inheritance, new operator, and instanceof .
• FL9 : FL8 + Object.prototype methods and Object static methods ( keys, create, defineProperty ,
  etc.).
• FL10 : FL9 + Array.prototype methods ( push , pop, slice , sort, forEach , map, filter,
  reduce , etc.).
• FL11 : FL10 + Function constructor, call , apply , and bind .
• FL12 : FL11 + String constructor object and String.prototype methods ( charAt, indexOf,
  slice , split , etc.).
• FL13 : FL12 + Boolean and Number constructor objects and methods.
• FL14 : FL13 + specialized error types (TypeError , RangeError, ReferenceError , SyntaxError ,
  EvalError , URIError ).
• FL14.4 : FL14 + Math object and mathematical functions.
• FL15 : FL14.4 + regular expression engine, RegExp constructor, regexp literals, and regexp-dependent
  String methods ( match , search ).
• FL16 : FL15 + Date and JSON objects. Full-featured ECMAScript 5 interpreter.
Mostly Automatic Translation of Language Interpreters
from C to Safe Rust                                                                              53

E.6   pocketpy (22 levels: FL0 –FL16 )
• FL0 : Minimal expression evaluator with print() , integer/float/string literals, variables, and
  basic arithmetic (+ , - , * , / ).
• FL0.2 : FL0 + comparison operators ( == , != , < , > , <= , >= ), bool , and None types.
• FL0.4 : FL0.2 + list type with operations, len() , and additional arithmetic (%, ** , // ).
• FL1 : FL0.4 + while loops, if /elif / else, exception handling (try/ except/ raise ), and boolean
  operators (and , or , not ).
• FL1.2 : FL1 + for loops, range() builtin, and iteration protocol.
• FL1.4 : FL1.2 + tuple type.
• FL1.6 : FL1.4 + user-defined functions ( def ), return statements, and function arguments.
• FL2 : FL1.6 + closures, lambda expressions, and nested function definitions.
• FL3 : FL2 + class definitions, inheritance, dict and set types.
• FL4 : FL3 + list/dict/set comprehensions.
• FL5 : FL4 + decorators (@decorator ), metaclasses, and property descriptors.
• FL6 : FL5 + generators (yield , yield from ).
• FL7 : FL6 + introspection modules ( inspect , dis , traceback , importlib ) and trace system.
• FL8 : FL7 + json and gc control modules.
• FL9 : FL8 + time and random modules.
• FL10 : FL9 + os module and file I/O ( open() ).
• FL11 : FL10 + enum, unicodedata , and conio modules.
• FL12 : FL11 + pickle , base64 , and lz4 modules.
• FL13 : FL12 + graphics/game modules ( easing , colorcvt , array2d , vmath ).
• FL14 : FL13 + multi-VM support and dynamic library loading.
• FL15 : FL14 + line profiling system.
• FL16 : FL15 + debugger with Debug Adapter Protocol (DAP) and breakpoint support. Full-featured
  Python 3.x interpreter.
