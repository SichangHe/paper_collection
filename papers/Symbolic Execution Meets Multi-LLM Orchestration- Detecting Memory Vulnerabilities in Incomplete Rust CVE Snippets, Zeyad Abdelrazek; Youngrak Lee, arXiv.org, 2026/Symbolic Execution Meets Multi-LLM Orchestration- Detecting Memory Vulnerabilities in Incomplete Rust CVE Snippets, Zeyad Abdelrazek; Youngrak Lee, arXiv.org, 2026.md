                                           Symbolic Execution Meets Multi-LLM Orchestration: Detecting
                                             Memory Vulnerabilities in Incomplete Rust CVE Snippets
                                                                         Zeyad Abdelrazek∗                                                                         Young Lee
                                                                   zgad01@jaguar.tamu.edu                                                                   ylee@tamusa.edu
                                                              Texas A&M University–San Antonio                                                      Texas A&M University–San Antonio
                                                                   San Antonio, Texas, USA                                                               San Antonio, Texas, USA
                                         Abstract                                                                                        Keywords
                                         This paper presents a system combining symbolic execution (KLEE)                                Rust, symbolic execution, KLEE, large language models, multi-agent
                                         with a 4-agent multi-LLM architecture for detecting memory vul-                                 systems, memory safety, vulnerability detection, graph database
arXiv:2605.00034v1 [cs.CR] 28 Apr 2026




                                         nerabilities in Rust unsafe code. A central challenge we address
                                         is the incomplete-code problem: CVE database entries provide only                               ACM Reference Format:
                                         isolated code snippets that lack struct definitions, imports, and                               Zeyad Abdelrazek and Young Lee. 2026. Symbolic Execution Meets Multi-
                                         Cargo manifests, causing all existing formal verification tools to                              LLM Orchestration: Detecting Memory Vulnerabilities in Incomplete Rust
                                                                                                                                         CVE Snippets. In Proceedings of the 6th International Workshop on Software
                                         fail at compilation with zero output. Our system resolves this
                                                                                                                                         Security Engineering (SSE ’26), co-located with EASE 2026, June 9–12, 2026,
                                         through four specialized agents—an Oracle/Validator for strate-                                 Glasgow, Scotland, United Kingdom. ACM, New York, NY, USA, 11 pages.
                                         gic planning, a Safety Checker for vulnerability analysis, a Code                               https://doi.org/10.1145/XXXXXXX.XXXXXXX
                                         Specialist for FFI wrapper generation, and a Fast Filter for execution
                                         optimization—that collaboratively synthesize KLEE-compatible har-
                                         nesses from otherwise uncompilable fragments. KLEE’s output is                                  1    Introduction
                                         then ingested by graph_klee.py, which constructs a Graph Data-
                                                                                                                                         Rust is one of the fastest-growing systems programming languages,
                                         base linking CVE files, CWE categories, error types, and symbolic
                                                                                                                                         valued for its ownership-based memory safety guarantees [19].
                                         execution paths as typed nodes and labelled edges, enabling struc-
                                                                                                                                         Yet these guarantees do not extend to unsafe code blocks, which
                                         tured cross-CVE vulnerability queries. We evaluated our system
                                                                                                                                         are necessary for low-level operations and Foreign Function Inter-
                                         on 31 real-world Rust CVEs spanning 11 CWE categories, achiev-
                                                                                                                                         faces (FFI) but introduce the same class of memory errors—buffer
                                         ing 90.3% wrapper compilation success where all state-of-the-art
                                                                                                                                         overflow, use-after-free, double-free—that plague C and C++. The
                                         formal verification tools achieve 0%. Our system detected 1,206
                                                                                                                                         practical consequence is a growing catalogue of Rust CVEs whose
                                         critical errors across 26 files (83.9% detection rate), compared to
                                                                                                                                         unsafe code contains real, exploitable memory faults.
                                         14 warnings across 11 files for Clippy (35.5%) and generic labels
                                                                                                                                            A critical and largely overlooked challenge compounds this
                                         for Miri. The 4-agent architecture reduced wrapper compilation
                                                                                                                                         problem: CVE database entries provide only isolated code snip-
                                         failures from 42% (single-agent baseline) to 9.7% and increased
                                                                                                                                         pets stripped of struct definitions, trait implementations, imports,
                                         detected errors from 487 to 1,206, confirming that role specializa-
                                                                                                                                         and Cargo manifests. This incomplete-code problem creates a hard
                                         tion and structured context passing produce measurably better
                                                                                                                                         barrier for every existing tool. KLEE [3] operates on LLVM bitcode
                                         results than a single general-purpose model. Our replication pack-
                                                                                                                                         from C/C++ and requires a compiled FFI harness that Rust snippets
                                         age is publicly available at https://github.com/Zeyad-Ab/Symbolic-
                                                                                                                                         cannot provide. Clippy [15] matches syntactic patterns and misses
                                         Execution-with-Multi-LLM-Architecture-for-Rust-Security.
                                                                                                                                         path-dependent bugs entirely. Formal tools (Kani [26], Prusti [1],
                                                                                                                                         Creusot [10], Haybale [2]) require a complete Cargo project with
                                         CCS Concepts
                                                                                                                                         resolved type information—applied to CVE snippets, all fail at com-
                                         • Security and privacy → Vulnerability management; Soft-                                        pilation with zero output. The result is that no automated tool
                                         ware security engineering; Memory safety; • Software and its                                    today can perform deep, execution-level vulnerability analysis on
                                         engineering → Software testing and debugging; Source code                                       the incomplete Rust code CVE databases actually contain.
                                         generation; • Computing methodologies → Large language                                             This paper closes that gap. We introduce a 4-agent multi-LLM
                                         models; Multi-agent systems.                                                                    pipeline that transforms an incomplete Rust CVE snippet into a
                                         ∗ Corresponding author.
                                                                                                                                         KLEE-compatible FFI harness, runs symbolic execution, and con-
                                                                                                                                         structs a Graph Database from the results. To the best of our
                                                                                                                                         knowledge, this is the first system to enable symbolic execu-
                                         Permission to make digital or hard copies of all or part of this work for personal or
                                         classroom use is granted without fee provided that copies are not made or distributed           tion on incomplete, context-free Rust CVE snippets without
                                         for profit or commercial advantage and that copies bear this notice and the full citation       manual intervention, achieving 90.3% wrapper compilation suc-
                                         on the first page. Copyrights for components of this work owned by others than the              cess where every existing formal tool achieves 0%.
                                         author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
                                         republish, to post on servers or to redistribute to lists, requires prior specific permission      This paper addresses the following research questions:
                                         and/or a fee. Request permissions from permissions@acm.org.                                        RQ1: Can symbolic execution, enabled by LLM-generated FFI wrap-
                                         SSE ’26, Glasgow, Scotland, United Kingdom                                                      pers, detect memory vulnerabilities in incomplete Rust CVE snippets?
                                         © 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM ISBN 978-1-4503-XXXX-X/26/06                                                                Specifically, we ask whether KLEE can flag at least one critical error
                                         https://doi.org/10.1145/XXXXXXX.XXXXXXX                                                         in each CVE file across 11 CWE categories.
SSE ’26, June 9–12, 2026, Glasgow, Scotland, United Kingdom                                                        Zeyad Abdelrazek and Young Lee


                        Agent 1               Agent 2            Agent 3                      Agent 4
   Rust CVE                                                                     C Wrapper                        KLEE                 JSON
                        Oracle             Safety Checker     Code Specialist                Fast Filter
    .rs file                                                                    Generation                    Symbolic Exec.       Vuln. Report
                       GPT-4 Turbo           Claude Opus        Claude Sonnet                 GPT-4o-mini



                                                                                C Wrapper
                      Analysis Plan        Risk Assessment      FFI Wrapper                  KLEE Params
                                                                                   (.c)                                             Graph DB
                        (JSON)                  (JSON)              (.rs)                      (JSON)
                                                                                                                                    graph_klee.py



Figure 1: 4-Agent Pipeline Overview. The pipeline proceeds left to right through six stages. (1) A Rust CVE snippet (incomplete
source file) is fed to Agent 1 (Oracle/Validator, GPT-4 Turbo), which identifies likely vulnerability types and produces a
structured JSON analysis plan—constraining all downstream agents to the relevant vulnerability classes. (2) Agent 2 (Safety
Checker, Claude Opus) receives the snippet and the plan, performs deep security analysis, assigns a risk score (0–10), and
annotates critical lines. (3) Agent 3 (Code Specialist, Claude Sonnet) uses all prior outputs to generate a complete, compilable
Rust FFI wrapper that replicates the vulnerability class in KLEE-compatible types; an automated step then synthesizes the
corresponding C harness. (4) Agent 4 (Fast Filter, GPT-4o-mini) selects optimal KLEE parameters (search strategy, time/memory
limits, fork depth) from the risk score. (5) KLEE performs symbolic execution on the compiled wrapper and emits a structured
JSON vulnerability report. (6) graph_klee.py ingests the JSON report and constructs a Graph Database in which nodes represent
CVE files, CWE categories, error types, and symbolic paths, and edges encode the relationships between them—enabling
cross-CVE vulnerability queries, pattern clustering, and structured export for downstream analysis. Dashed arrows show
intermediate artifacts persisted to disk for reproducibility.


    RQ2: To what extent can LLM-generated FFI wrappers bridge the        • Graph Database post-processing. A graph_klee.py compo-
incomplete-code gap and enable symbolic execution on isolated Rust          nent that automatically ingests any KLEE output directory and
CVE snippets? We measure compilation success rate compared to               constructs a Graph Database in which CVE files, CWE categories,
0% for formal verification tools.                                           error types, and symbolic execution paths are represented as
    RQ3: Does a specialized 4-agent LLM architecture outperform a           typed nodes and labelled edges—enabling structured cross-CVE
single-agent approach in vulnerability detection rate, wrapper compi-       vulnerability queries, CWE-level pattern clustering, and export
lation success, and error count?                                            for downstream security analysis.
    Our system employs four distinct agents: an Oracle Validator         • Memory-safety CVE subset and replication package. A fil-
(GPT-4-Turbo) for strategic planning, a Safety Checker (Claude              tered subset of 31 memory-safety CVEs drawn from the publicly
Opus 4.5) for deep security analysis, a Code Specialist (Claude Son-        available HALURust dataset [18], annotated with ground-truth
net 4.5) for generating FFI wrappers, and a Fast Filter (GPT-4o-mini)       CWE labels, together with all generated FFI wrappers, KLEE out-
for optimizing KLEE parameters. A post-processing component,                puts, Graph DB exports, and replication scripts released publicly.
graph_klee.py, then constructs a Graph Database from KLEE’s
output to enable structured cross-CVE vulnerability queries. Our         2 Motivating Example
replication dataset, CVE files, generated wrappers, and experiment
scripts are available at https://github.com/Zeyad-Ab/Symbolic-Execution- 2.1 The Vulnerability: CVE-2020-35904
with-Multi-LLM-Architecture-for-Rust-Security.                           Consider CVE-2020-35904, a confirmed memory-corruption vulner-
Contributions. This paper makes the following contributions:             ability in the concurrent-queue crate (CWE-131: Incorrect Calcu-
                                                                         lation of Buffer Size). The CVE database provides the snippet shown
• First incomplete-code symbolic execution pipeline for Rust.
                                                                         in Listing 1: a drop implementation that reconstructs a Vec with
   To our knowledge, this is the first automated system capable of
                                                                         length=0 while passing the actual capacity, causing the allocator
   running KLEE symbolic execution on isolated Rust CVE snip-
                                                                         to free an incorrectly sized region. The unsafe block on the final
   pets that lack struct definitions, imports, and Cargo context—
                                                                         line is the root cause—but to understand why it is dangerous, an
   achieving 90.3% compilation success where all state-of-the-art
                                                                         analysis tool must be able to execute or symbolically explore the
   formal verification tools achieve 0% and no prior system has
                                                                         function. As we show next, no existing tool can do this without
   reported any success.
                                                                         help.
• First multi-agent LLM architecture for Rust CVE analysis.
   A coordinated 4-agent pipeline in which role-specialized models
                                                                         Listing 1: CVE-2020-35904 as it appears in the vulnerability
   collaboratively synthesize KLEE-compatible FFI wrappers from
                                                                         database. The struct fields (self.head, self.cap, self.buffer)
   uncompilable Rust fragments—reducing wrapper compilation
                                                                         and the Ordering import are absent, causing immediate com-
   failures from 42% (single-agent) to 9.7%, a combination not previ-
                                                                         pilation failure in all existing tools.
   ously attempted in the literature.
                                                                         fn drop(&mut self) {
• Empirical evaluation on real-world CVEs. A systematic study                 // self.head undefined -- struct not present
   on 31 real-world Rust CVEs spanning 11 CWE categories, detect-             let hix = self.head.load(Ordering::Relaxed)
   ing 1,206 critical errors at an 83.9% detection rate—26.8× more                        & (self.one_lap - 1);
   issues than Miri and Clippy combined, with zero false negatives            for i in 0..self.len() {
   relative to Clippy.                                                             let index = if hix + i < self.cap {
Symbolic Execution Meets Multi-LLM Orchestration: Detecting Memory Vulnerabilities in Incomplete Rust CVE Snippets
                                                                                                           SSE ’26, June 9–12, 2026, Glasgow, Scotland, United Kingdom


              hix + i                                                                 complete type information. Prusti [1] relies on deductive verifica-
          } else { hix + i - self.cap };                                              tion through manual specifications, requiring developers to anno-
          unsafe {                                                                    tate code with pre- and post-conditions—a process that is fundamen-
              let slot = &mut *self.buffer.add(index);                                tally incompatible with automated CVE triage. While Creusot [10]
              let value = &mut *slot.value.get();                                     leverages the Why3 platform, it explicitly rejects unsafe code blocks,
              value.as_mut_ptr().drop_in_place();
                                                                                      which is precisely where most Rust memory vulnerabilities occur.
          }
      }                                                                               Haybale [2] provides symbolic execution on LLVM IR but requires
      // BUG: length=0 causes incorrect deallocation                                  the program to be compiled to bitcode first, which is impossible
      unsafe { Vec::from_raw_parts(self.buffer, 0, self.cap);                         without a complete, buildable Rust project. Our testing on our 31
        }                                                                             CVE dataset resulted in a 0% success rate across all four tools.
}                                                                                         Lightweight tools like Miri [20] and Clippy are more compat-
                                                                                      ible with fragmented code but lack depth. Miri identified unde-
                                                                                      fined behavior in all 31 files but provided only generic error clas-
                                                                                      sifications without specific vulnerability details or concrete coun-
2.2     Why KLEE Cannot Analyze This Directly
                                                                                      terexample inputs. Clippy [15] reached a 35.5% detection rate by
KLEE operates on LLVM bitcode compiled from C/C++ and has no                          matching syntactic patterns but missed 15 files where our sys-
native Rust support [3]. Applying KLEE to a Rust function requires                    tem found critical vulnerabilities—precisely because those files
two preconditions: the code must compile with rustc to LLVM bit-                      contained path-dependent bugs requiring execution-level analysis.
code, and a C FFI harness must exist calling klee_make_symbolic()                     cargo-geiger [16] tracks unsafe code usage at the crate level but
on all inputs. Neither is met here. The fields self.head, self.cap,                   functions as a risk indicator rather than a vulnerability detector.
and self.buffer belong to a struct entirely absent from the snip-
pet; Ordering is unimported. Running rustc produces immediate
                                                                                      3.2      Symbolic Execution and LLM-Driven
undeclared type errors—no bitcode, no harness, no KLEE.
                                                                                               Security
2.3     Why Clippy Cannot Detect the Bug                                              Symbolic execution through KLEE [3] is a standard for high-coverage
                                                                                      testing, and recent work has targeted Rust-specific issues like un-
Clippy matches syntactic and type-based patterns—integer casts,                       recoverable panics [4]. Related tools such as S2E [7], SAGE [12],
unreachable code, suspicious pointer operations. The bug here                         DART [11], and CUTE [22] extend symbolic and concolic execu-
is semantic and path-dependent: Vec::from_raw_parts is called                         tion to larger systems, but all assume an executable binary—the
with length=0 instead of the actual length, which is only wrong                       precondition our approach eliminates. Techniques targeting use-
because of its pairing with cap. No lint rule can detect this without                 after-free [17] or using concretely mapped memory [23] still require
reasoning about the relationship between length and capacity at                       manually constructed harnesses, which our system generates auto-
runtime—precisely the kind of reasoning that requires execution-                      matically.
level analysis. Clippy reported zero warnings.                                           LLM integration has opened new avenues for test generation [5,
                                                                                      27]. Crabtree [14] uses LLMs to guide Rust fuzz driver generation
2.4     Why All Other Tools Fail on Incomplete                                        but requires a complete, buildable crate. AthenaTest [25], ChatU-
        Code                                                                          niTest [6], and TitanFuzz [9] similarly operate on complete code-
Beyond KLEE and Clippy, every Rust analysis tool requires complete,                   bases. Our work differs by targeting the incomplete-code regime
compilable code. Formal verification tools (Kani [26], Prusti [1],                    and using the LLM to generate the analysis harness itself rather
Creusot [10], Haybale [2]) each build on the Rust compiler pipeline                   than tests for existing code. LLMs have also been used to generate
and require a complete crate with a Cargo.toml—Creusot further                        symbolic execution inputs [31], but as inputs to existing harnesses
rejects unsafe blocks entirely. We submitted CVE-2020-35904 to all                    rather than as harness generators.
four; all failed immediately with missing-type errors and produced
zero output. Cargo ecosystem tools (cargo-audit, cargo-geiger,                        3.3      Multi-Agent Systems in Security
cargo-deny) operate at the manifest level and cannot parse a bare                     Multi-agent LLM systems are an active research area in software
.rs file. Miri requires a compilable, runnable program and fails at                   engineering [30]. ChatDev [21] simulates a complete software devel-
the same compilation step.                                                            opment company with role-assigned LLM agents communicating
   The pattern is universal: every existing Rust analysis tool is                     through a structured “chat chain”; MetaGPT [13] formalizes agent
designed for complete programs, not CVE snippets.                                     interactions through standardized role descriptions and structured
                                                                                      output schemas. Both demonstrate that role specialization improves
3 Related Work                                                                        output quality over single-model approaches—a finding our results
                                                                                      confirm in the security domain. In security applications, AutoAt-
3.1 Formal Verification and Practical Analysis                                        tacker [28] applies multi-agent LLMs for automated penetration
    in Rust                                                                           testing; PentestGPT [8] uses LLM reasoning to guide human pene-
Formal verification tools offer strong correctness guarantees but                     tration testers through structured decision trees. LLM4Vuln [24]
face significant limits for real-world CVE analysis. Kani [26] uses                   evaluates LLMs on vulnerability reasoning tasks, finding that mod-
bounded model checking but requires fully compilable code and                         els struggle with complex multi-step reasoning—a limitation our
SSE ’26, June 9–12, 2026, Glasgow, Scotland, United Kingdom                                                       Zeyad Abdelrazek and Young Lee


Oracle-led pipeline mitigates by decomposing the task across spe-         • Teal — memory deallocation calls (Vec::from_raw_parts used
cialized agents. VulnFix [29] uses symbolic execution for patch             as a dealloc trigger).
validation, complementing our use of symbolic execution for initial       • Red — the root-cause bug line: the hardcoded 0 length argument
detection.                                                                  that causes incorrect heap free.
                                                                          • Green — safe iteration context carrying no vulnerability (present
4 Methodology: 4-Agent Architecture                                         for reader orientation only).
4.1 System Overview
                                                                         Listing 2: Original CVE-2020-35904 (CWE-131) with se-
The system takes incomplete Rust CVE code as input and produces a
                                                                         mantic highlights. Green: safe iteration loop. Orange:
detailed vulnerability report. The process consists of four sequential
                                                                         unsafe block and raw pointer dereferences. Purple: pointer
stages: strategic planning by the Oracle/Validator, security anal-
                                                                         arithmetic (buffer.add(index)). Teal: deallocation call
ysis by the Safety Checker, FFI wrapper generation by the Code
                                                                         (Vec::from_raw_parts). Red: root-cause bug — length=0
Specialist, and parameter optimization by the Fast Filter, followed
                                                                         causes incorrect buffer free. Each colour reappears in the
by KLEE symbolic execution. Each agent is implemented using
                                                                         FFI wrapper (Listing 3) as a dedicated function.
a specific LLM chosen for its strengths in the assigned role. The
agents communicate through structured JSON outputs, where each           fn drop(&mut self) {
                                                                             let hix = self.head.load(Ordering::Relaxed)
result informs the subsequent stage to reduce hallucinations and
                                                                                       & (self.one_lap - 1);
focus the analysis context.                                                  for i in 0..self.len() {
                                                                              let index = if hix + i < self.cap { hix + i }
4.2     The Incomplete-Code Problem                                           else { hix + i - self.cap };
A central challenge—and a key reason existing tools fail—is that CVE             unsafe {
databases publish vulnerability snippets, not complete programs.                     let slot = &mut *self.buffer.add(index);
Table 1 summarizes the missing context observed across our 31                        let value = &mut *slot.value.get();
CVE files.                                                                           value.as_mut_ptr().drop_in_place();
                                                                                 }
Table 1: Types of missing context in the 31 CVE snippets.                    }
                                                                             // BUG: length=0 causes incorrect deallocation
All four categories cause immediate compilation failure in
                                                                             unsafe { Vec::from_raw_parts(self.buffer, 0, self.cap);
formal verification tools.                                                    }
                                                                         }
                   Missing Context              Files         %
                                                                            Agent 3 Code Specialist (Claude Sonnet 4.5) generates a
                   Struct/enum definitions        28    90.3%
                   Import statements              31    100%
                                                                         complete, compilable FFI wrapper preserving the vulnerability se-
                   Cargo.toml / dependencies      31    100%             mantics of the original CVE (max_tokens=2500; an earlier limit of
                   Trait implementations          19    61.3%            1500 caused a 42% failure rate). Listing 3 uses the same four-colour
                                                                         scheme as the CVE snippet: each function isolates one coloured
   Our Code Specialist addresses each category by generating self-       region (Orange → unsafe pointer dereference, Purple → pointer
contained FFI functions that inline necessary type representations       arithmetic, Teal → deallocation path, Red → root-cause size arith-
as raw pointers or primitive types, use only KLEE-compatible types       metic) and exposes it as a standalone symbolic path for KLEE. If
(*mut u8, usize, i32), and require no external crates.                   generated code fails to compile, the system falls back to a predefined
                                                                         template; 3 of 31 files (9.7%) required this.
4.3     Agent Roles and Specialization                                   Listing 3: FFI wrapper generated by Agent 3 for CVE-
Agent 1 Oracle/Validator (GPT-4 Turbo) acts as the strategic             2020-35904 (CWE-131), colour-matched to the CVE snippet.
coordinator. Given the input CVE snippet, it identifies potential        Orange (buffer_overflow_write): unsafe raw-pointer write
vulnerability types, estimates code complexity, and recommends           with no bounds check — mirrors the CVE’s unsafe deref-
the number of FFI functions to generate (typically 8–12).                erence block. Purple (offset parameter): symbolic offset
   Agent 2 Safety Checker (Claude Opus 4.5) performs deep                used in pointer arithmetic — mirrors buffer.add(index).
security analysis using the Oracle’s plan. It identifies specific vul-   Teal (use_after_free_access): explicit dealloc then write —
nerability patterns, assigns a risk score (0–10), and marks critical     mirrors Vec::from_raw_parts deallocation. Red (base_size
lines for Agent 3 to target.                                             * multiplier): unchecked multiply as alloc size — mirrors
   To illustrate the translation process, Listing 2 shows the original   the root-cause length=0 arithmetic error. KLEE detected 752
CVE-2020-35904 snippet (CWE-131) with four semantic regions              critical errors from this wrapper.
colour-coded to match their counterparts in the generated FFI wrap-      // [ORANGE] Mirrors CVE unsafe block + raw pointer
per (Listing 3). The colour legend is:                                        dereference
                                                                         #[no_mangle]
  • Orange — unsafe block entry and raw pointer dereferences
                                                                         pub extern "C" fn buffer_overflow_write(
    (the region that bypasses Rust’s borrow checker).
                                                                          buffer: *mut u8, offset: usize, value: u8) -> i32 {
  • Purple — pointer arithmetic and index computation (the offset            unsafe { *buffer.add(offset) = value; } // no bounds
    buffer.add(index) pattern).                                               check
Symbolic Execution Meets Multi-LLM Orchestration: Detecting Memory Vulnerabilities in Incomplete Rust CVE Snippets
                                                                                                           SSE ’26, June 9–12, 2026, Glasgow, Scotland, United Kingdom


      0                                                                                   unsigned char *ptr, size_t size);
}                                                                                     extern int32_t integer_overflow_allocation(
                                                                                          size_t base_size, size_t multiplier);
// [TEAL] Mirrors Vec::from_raw_parts deallocation path
#[no_mangle]                                                                          int main() {
pub extern "C" fn use_after_free_access(                                                  size_t idx1, idx2;
 ptr: *mut u8, size: usize) -> i32 {                                                      unsigned char val1;
    unsafe {                                                                              unsigned char buffer[128];
        let layout = std::alloc::Layout
             ::from_size_align_unchecked(size, 1);                                          klee_make_symbolic(&idx1, sizeof(idx1), "idx1");
        std::alloc::dealloc(ptr, layout); // free the buffer                                klee_make_symbolic(&idx2, sizeof(idx2), "idx2");
        *ptr = 42; // write after free – UAF                                                klee_make_symbolic(&val1, sizeof(val1), "val1");
    }                                                                                       klee_make_symbolic(buffer, sizeof(buffer), "buffer");
    0
}                                                                                           klee_assume(idx1 < 10000);
                                                                                            klee_assume(idx2 < 10000);
// [RED] Mirrors root-cause: incorrect size arithmetic
#[no_mangle]                                                                                int path = klee_range(0, 4, "path");
pub extern "C" fn integer_overflow_allocation(
    base_size: usize, multiplier: usize) -> i32 {                                           if (path == 0) {
    unsafe {                                                                                    buffer_overflow_write(buffer, idx1, idx1, val1);
         let size = base_size *                                                             } else if (path == 1) {
      multiplier; // unchecked: overflow risk                                                   use_after_free_access(buffer, idx2);
         let layout = std::alloc::Layout                                                    } else if (path == 2) {
             ::from_size_align_unchecked(size, 8);                                              double_free_trigger(buffer, idx1);
         let ptr = std::alloc::alloc(layout);                                               } else if (path == 3) {
         *ptr = 0xAA;                                                                           integer_overflow_allocation(idx1, idx2);
         std::alloc::dealloc(ptr, layout);                                                  }
    }                                                                                       return 0;
    0                                                                                 }
}

    Agent 4 Fast Filter (GPT-4o-mini) uses the risk score and vul-
nerability patterns from Agent 2 to select optimal KLEE parameters:                   4.5     Graph Database Construction
search strategy (DFS, BFS, or random-path), time and memory lim-                              (graph_klee.py)
its, and maximum fork depth. Using GPT-4o-mini for this role keeps                    After KLEE completes symbolic execution, its raw output is a direc-
overhead low while providing adequate reasoning for parameter                         tory of typed error files (*.ptr.err, *.external.err, *.abort.err,
selection.                                                                            *.div.err, *.overflow.err) alongside test-case and statistics files.
                                                                                      While these files provide complete information, their flat, file-based
4.4       KLEE Integration                                                            structure makes cross-CVE querying and pattern aggregation diffi-
The generated FFI wrapper is compiled using rustc into LLVM                           cult. To address this, we developed graph_klee.py, a post-processing
bitcode. We then link this bitcode with an automatically generated                    component that automatically ingests any KLEE output directory
C harness that declares the FFI functions and creates symbolic vari-                  and constructs a Graph Database (Graph DB) from its contents.
ables for all parameters using klee_make_symbolic(). Listing 4                           The Graph DB represents the KLEE analysis as a typed property
shows the C wrapper generated for CVE-2020-35904.                                     graph with four categories of nodes:
                                                                                      • CVE nodes — one per analysed file, labelled with the CVE iden-
Listing 4: Auto-generated C wrapper for CVE-2020-35904
                                                                                        tifier and CWE category.
(CWE-131). klee_make_symbolic makes all inputs fully sym-
bolic; klee_assume bounds the symbolic indices; klee_range                            • ErrorType nodes — one per KLEE error class (ptr, external,
forks execution into one path per FFI function. This pro-                               abort, div, overflow), shared across all CVEs.
duced 752 critical errors.                                                            • SymPath nodes — one per unique KLEE test case, storing the
#include <klee/klee.h>                                                                  concrete symbolic input values and the associated stack trace.
#include <stdint.h>                                                                   • CWE nodes — one per CWE category, grouping all CVEs that
#include <string.h>                                                                     share a vulnerability class.
                                                                                         Edges encode the following relationships: HasError (CVE → Er-
extern int32_t buffer_overflow_write(
    unsigned char *buffer, size_t size,                                               rorType, weighted by error count), TriggeredBy (CVE → SymPath,
    size_t offset, unsigned char value);                                              linking a CVE to each concrete fault-inducing input), ClassifiedAs
extern int32_t use_after_free_access(                                                 (CVE → CWE, reflecting the vulnerability category assigned by
    unsigned char *ptr, size_t size);                                                 Agent 1), and SharedPattern (CVE → CVE, added when two files
extern int32_t double_free_trigger(                                                   share at least one symbolic path pattern across the same error type).
SSE ’26, June 9–12, 2026, Glasgow, Scotland, United Kingdom                                                        Zeyad Abdelrazek and Young Lee


   graph_klee.py accepts any KLEE output directory as input,             Write), and 12 files covering other memory-related categories. Crit-
making it applicable to any symbolic execution campaign that uses        ically, all files are incomplete code snippets extracted from vul-
KLEE—not only to the pipeline described in this paper. For our           nerability reports—exactly as published in the original HALURust
31-CVE dataset, the resulting Graph DB contains 31 CVE nodes, 5          dataset. Our filtered subset and all experiment artifacts are available
ErrorType nodes, 11 CWE nodes, and 1,206 SymPath nodes, con-             at https://github.com/Zeyad-Ab/Symbolic-Execution-with-Multi-
nected by 1,310 labelled edges. The Graph DB is serialised to JSON-      LLM-Architecture-for-Rust-Security.
LD for portability and included in our replication package, where it
can be imported directly into graph query environments for further       5.2    Baseline Tools
analysis.                                                                We compared against two groups. Formal verification tools (Kani
   Figure 2 shows the Graph DB visualisation produced by running         0.67.0, Prusti v-2023-08-22, Creusot, Haybale 0.7) achieved 0% suc-
graph_klee.py on klee_output/cwe-131-cve-2020-35904. Teal                cess because they could not compile the incomplete code. Practical
nodes represent vulnerability functions generated by the Code            tools (Miri 0.1.0, Clippy 0.1.93, cargo-geiger 0.13.0) were tested with
Specialist (e.g., data_race_incr..., out_of_bound...); yellow            Clippy given minimal Cargo project wrappers. Miri detected generic
nodes represent the concrete KLEE error files they trigger (e.g.,        undefined behavior in all 31 files; Clippy produced 14 warnings
test001079.exter..., test000009.ptr.er...). Each directed                across 11 files.
Triggers edge connects a function to a specific fault-inducing test
case, concisely capturing the many-to-one relationship between           5.3    Single-Agent Baseline
symbolic execution paths and the underlying vulnerability func-
                                                                         To validate the multi-agent architecture (RQ3), we implemented a
tions.
                                                                         single-agent baseline using Claude Sonnet 4.5 alone, without the
                                                                         Oracle’s planning step or the Fast Filter’s parameter optimization,
                                                                         operating with max_tokens=1500.

                                                                         5.4    Evaluation Metrics and Implementation
                                                                         We measure compilation success rate (RQ2), vulnerability detection
                                                                         rate and critical error count (RQ1), and multi-agent vs. single-agent
                                                                         comparison (RQ3).
                                                                            Our implementation runs on macOS darwin 25.2.0 using KLEE
                                                                         version 3.1_5 and LLVM 16.0.6_1. We use the stable Rust toolchain
                                                                         and access LLM APIs from OpenAI (GPT-4 Turbo, GPT-4o-mini)
                                                                         and Anthropic (Claude Opus 4.5, Claude Sonnet 4.5).

Figure      2:    Graph       DB      visualisation     for              5.5    Replication
klee_output/cwe-131-cve-2020-35904        (CVE-2020-35904,               Full replication instructions, pre-generated FFI wrappers, and KLEE
CWE-131 Incorrect Buffer Size Calculation), produced by                  outputs for all 31 CVEs are available at https://github.com/Zeyad-
graph_klee.py. Teal nodes are vulnerability functions; yel-              Ab/Symbolic-Execution-with-Multi-LLM-Architecture-for-Rust-Security.
low nodes are concrete KLEE error files. Directed Triggers
edges link each function to the test cases that exposed a                6 Evaluation
fault. data_race_incr... triggers four .external.err paths;
out_of_bound... triggers one .ptr.err—the pointer fault                  6.1 RQ1: Vulnerability Detection via Symbolic
that produced the highest-confidence detection signal for                    Execution
this CVE.                                                                KLEE detected at least one critical error in 26 of 31 files (83.9%),
                                                                         directly answering RQ1: symbolic execution can detect Rust mem-
                                                                         ory vulnerabilities across all major CWE categories. Of the 31 files,
5 Experimental Setup                                                     28 (90.3%) compiled successfully; the remaining 3 used the fallback
                                                                         template. Across the 26 detected files, KLEE produced 1,206 critical
5.1 Dataset                                                              errors: 124 pointer errors (*.ptr.err) and 1,082 external/panic
Our evaluation uses 31 Rust CVE files drawn from the publicly            errors (*.external.err). The three colour-annotated functions in
released dataset of Luo et al. [18], who introduced HALURust—a           Listing 3 account for 752 of those errors in CVE-2020-35904 alone.
benchmark of Rust CVEs collected from the NVD and crates.io                  Table 2 summarizes detection results by CWE category, and
security advisories for studying LLM-based vulnerability detec-          Figure 3 visualizes error counts.
tion. From their full dataset we selected the subset of CVEs whose           The per-CVE breakdown in Table 3 reveals two important pat-
vulnerability class involves a memory safety issue (e.g., buffer over-   terns. First, the error distribution is highly skewed: the top two
flow, use-after-free, integer overflow leading to memory corrup-         CVEs (CVE-2020-35904 and CVE-2022-36008) account for 1,133
tion), yielding 31 files spanning 11 CWE categories: 5 files for         of the 1,206 total errors (93.9%), while the remaining 24 detected
CWE-119 (Buffer Overflow), 8 for CWE-416 (Use-After-Free), 3 for         files contribute 73 errors combined. This skew reflects KLEE’s
CWE-125 (Out-of-Bounds Read), 3 for CWE-787 (Out-of-Bounds               path-explosion behaviour: files whose FFI wrappers expose many
Symbolic Execution Meets Multi-LLM Orchestration: Detecting Memory Vulnerabilities in Incomplete Rust CVE Snippets
                                                                                                           SSE ’26, June 9–12, 2026, Glasgow, Scotland, United Kingdom


Table 2: Detection results by CWE category (4-agent approach,                                             generic lint patterns rather than the specific memory-safety vi-
31 CVEs). Nine of eleven categories achieved 100% detection.                                              olations KLEE confirmed—reinforcing the qualitative difference
CWE-190 and CWE-416 show lower rates due to lifetime-                                                     between lint-based and symbolic-execution-based detection.
dependent vulnerability semantics.                                                                           Nine of eleven CWE categories achieved a 100% detection rate.
                                                                                                          The two categories with partial detection are CWE-190 (Integer
 CWE                     Category                           Files          Det.       Rate    Errors      Overflow, 1/3 files) and CWE-416 (Use-After-Free, 6/9 files). CWE-
 119                     Buffer Overflow                          5          5        100%          12    416’s lower rate reflects that use-after-free bugs depend on specific
 125                     OOB Read                                 3          3        100%          11    object deallocation sequences that are difficult to reproduce with-
 131                     Incorrect Calc.                          1          1        100%         752
 134                     Format String                            1          1        100%           1    out the original surrounding struct. Despite the lower file-level
 190                     Integer Overflow                         3          1         33%         381    rate, CWE-131 produced the highest single-category error count
 191                     Integer Underflow                        1          1        100%           6    (752 errors from one file), driven by KLEE exploring hundreds of
 415                     Double Free                              2          2        100%          18
 416                     Use-After-Free                           9          6         67%          19    symbolic paths through incorrect buffer-size arithmetic.
 787                     OOB Write                                3          3        100%           3       Table 4 directly compares compilation and detection success
 824                     Uninit. Pointer                          1          1        100%           1
 908                     Uninit. Resource                         2          2        100%           2
                                                                                                          across all evaluated tools, answering RQ2. The 90.3% compilation
                                                                                                          success of our system compared to 0% for all formal verification
 Total                                                          31          26       83.9%        1,206
                                                                                                          tools demonstrates that LLM-generated FFI wrappers can bridge
                                                                                                          the incomplete-code gap to a degree not achievable by any existing
                                  KLEE Critical Errors by CWE Category                                    automated tool.

                 800                  752                                                                 Table 4: Compilation and detection success across all eval-
                                                                                                          uated tools on 31 Rust CVEs. All formal verification tools
                                                                                                          achieve 0% because they cannot process incomplete code. Our
                 600
   KLEE Errors




                                                                                                          4-agent system achieves 90.3% compilation success (RQ2).
                                              381
                 400                                                                                           Tool                    Type              Compile       Detect    Issues
                                                                                                               Kani 0.67.0             Formal verif.            0%          0%   0
                 200                                                                                           Prusti 2023-08-22       Formal verif.            0%          0%   0
                                                                                                               Creusot                 Formal verif.            0%          0%   0
                                                                                                               Haybale 0.7             Symbolic exec.           0%          0%   0
                         12    11                     6    18         19         3     1      2
                  0                                                                                            Miri 0.1.0              Runtime check           N/A      100%     Generic
                         119 125 131 190 191 415 416 787 824 908                                               Clippy 0.1.93           Static lint             N/A      35.5%    14 warn.
                                                                                                               cargo-geiger            Unsafe tracker          N/A         0%    0
                                       CWE Category
                                                                                                               Single-Agent            LLM+KLEE               58%       51.6%    487
                                                                                                               4-Agent (Ours)          LLM+KLEE             90.3%       83.9%    1,206
Figure 3: Critical errors detected by KLEE per CWE cate-
gory. CWE-131 produces 752 errors from a single file due to
KLEE exploring hundreds of symbolic paths through incor-
                                                                                                                                                Detection Rate Comparison (%)
rect buffer-size arithmetic.

                                                                                                          4-Agent (Ours)                                                                  83.9
Table 3: Top-10 CVEs by KLEE critical error count. ptr =
pointer/memory faults; ext = external/panic faults. Clippy
column shows warnings on the same file.                                                                     Single-Agent                                             51.6

                   CVE                 CWE          ptr    ext        Total          Clippy                       Clippy                                35.5
                   CVE-2020-35904           131     48     704             752         0
                   CVE-2022-36008           190     12     369             381         0
                   CVE-2021-31162           415      9       9              18         0                     Formal tools          0
                   CVE-2021-28875           119      4       8              12         1
                   CVE-2021-25902           416      3       6               9         0
                   CVE-2020-35861           416      2       7               9         0                     cargo-geiger          0
                   CVE-2021-28878           125      3       5               8         2
                   CVE-2021-28877           125      2       3               5         1                                       0           20            40         60               80          100
                   CVE-2021-28876           125      2       3               5         0                                                                Detection Rate (%)
                   CVE-2021-29939           191      1       5               6         0
                   Top-10 total                     86    1,119       1,205            4
                                                                                                          Figure 4: Detection rate comparison across evaluated tools.
                                                                                                          Our 4-agent system achieves 83.9% with 1,206 typed, action-
symbolic branch conditions produce exponentially more error re-                                           able error reports—compared to 0% for all formal verification
ports than files with simpler control flow. Second, Clippy detected                                       tools and 35.5% for Clippy.
warnings in only 4 of the top-10 files, and those warnings were
SSE ’26, June 9–12, 2026, Glasgow, Scotland, United Kingdom                                                          Zeyad Abdelrazek and Young Lee


6.2     RQ3: Multi-Agent vs. Single-Agent                                   6.4    KLEE Error Analysis
        Performance                                                         KLEE produces typed error files ending in .err. Pointer errors
Table 5 compares the 4-agent pipeline against the single-agent              (*.ptr.err) are emitted when KLEE finds a memory access viola-
baseline, answering RQ3.                                                    tion at the LLVM level. External/panic errors (*.external.err)
                                                                            are emitted when KLEE encounters a call it cannot model internally—
Table 5: Multi-agent vs. single-agent comparison on 31 CVEs.                in Rust FFI code, this corresponds to Rust’s runtime panic handler
The 4-agent system outperforms the single-agent baseline                    inside unsafe blocks.
across all metrics, confirming the value of role specialization
(RQ3).                                                                      Listing 5: Pointer error from CVE-2021-31162
                                                                            (CWE-415). KLEE identifies the faulting function
           Metric                     Single-Agent     4-Agent (Ours)       (test_out_of_bounds_slice_manipulation), confirms inputs
           Wrapper compile rate              58.0%              90.3%
                                                                            are fully symbolic (write_index=symbolic, value=symbolic),
           Fallback template rate            42.0%               9.7%       provides a concrete example address, and delimits the
           Detection rate (files)            51.6%              83.9%       exploitable memory range (9,872 bytes).
           Total critical errors               487              1,206
           Avg. time per file              4.2 min            6.8 min       Error: memory error: out of bound pointer
                                                                            Stack:
   The 4-agent system reduces the fallback rate from 42% to 9.7%              #0 in test_out_of_bounds_slice_manipulation(
and nearly doubles the detection rate. The modest time overhead                    data=1636382539776,
                                                                                   write_index=symbolic,
(6.8 vs. 4.2 minutes) delivers a 2.5× increase in detected errors. The
                                                                                   value=symbolic)
Oracle’s structured JSON plan constrains the Code Specialist to the           #1 in main()
correct vulnerability class, reducing hallucinated generic code; the        Info:
Safety Checker’s risk score directs generation toward the highest-            address: (Add w64 1636382539776
severity lines; and the Fast Filter allocates KLEE exploration time                     (ReadLSB w64 0 idx5))
proportionally to risk.                                                       example: 1636382539904
                                                                              range:   [1636382539904, 1636382549775]
6.3     Comparison with Clippy
Our approach uniquely detected vulnerabilities in 15 files where              The error reports the exact vulnerable function (test_out_of_bounds_slice_m
Clippy reported zero warnings, producing 417 critical errors                confirms that inputs are symbolic (write_index, value), provides a
Clippy missed entirely. In 11 files both tools flagged issues; in 5 files   concrete example address, and delimits the exploitable range—9,872
neither detected anything. There were zero files where only Clippy          bytes of memory that could be corrupted.
detected an issue—demonstrating our approach subsumes Clippy’s
detection while finding substantially more.                                 7 Discussion
                                                                            7.1 Why Multi-Agent Coordination Improves
Table 6: Per-file detection classification: 4-Agent vs. Clippy
(31 CVEs).                                                                      Detection
                                                                            Our results demonstrate that dividing analysis among four special-
                                                                            ized agents produces more reliable results than any single-model
  Category             Files   Description
                                                                            approach (RQ3). The key benefit is focused context: each agent
  Only 4-Agent           15    4-agent ≥1 error, Clippy = 0 warnings        receives only information relevant to its role, reducing prompt com-
  Only Clippy             0    Clippy ≥1 warning, 4-agent = 0 errors        plexity and the probability of hallucination. The Oracle’s JSON plan
  Both                   11    Both ≥1 detection                            constrains the Safety Checker to the specific vulnerability types
  Neither                 5    Both reported 0                              present in the code; the Safety Checker’s risk score and critical-line
  Total                  31                                                 annotations guide the Code Specialist toward generating functions
                                                                            that target the most dangerous code paths; and the Fast Filter uses
                                                                            the risk score to allocate more KLEE exploration time to complex,
Table 7: Detection volume: 4-Agent vs. Clippy. Our system                   high-risk files.
produces 86× more issues with concrete symbolic counterex-                     A key observation from our ablation is that the Oracle’s planning
amples.                                                                     step accounts for the largest share of the improvement over the
                                                                            single-agent baseline. When a single model is given the CVE snippet
             Tool         Det. Rate       Issues          Type              and asked simultaneously to assess the vulnerability and generate
             Clippy      35.5% (11/31)        14      Lint warnings         an FFI wrapper, it tends to produce generic wrapper structures that
             4-Agent     83.9% (26/31)     1,206     Concrete errors        do not faithfully reflect the CWE category of the original snippet.
                                                                            By separating these concerns—having the Oracle first identify the
   Notable examples where only our approach detected vulner-                vulnerability class and then constraining the Code Specialist to
abilities include CVE-2022-36008 (381 critical errors, Clippy: 0),          that class via structured JSON—we reduce the probability that the
CVE-2020-35861 (9 errors, Clippy: 0), and CVE-2021-25902 (9 errors,         Code Specialist generates a buffer-overflow wrapper for a use-after-
Clippy: 0).                                                                 free CVE, or vice versa. This separation of concerns drives the
Symbolic Execution Meets Multi-LLM Orchestration: Detecting Memory Vulnerabilities in Incomplete Rust CVE Snippets
                                                                                                           SSE ’26, June 9–12, 2026, Glasgow, Scotland, United Kingdom


32-percentage-point improvement in detection rate (51.6% to 83.9%)                    7.4      Limitations of the FFI Approximation
between the single-agent and 4-agent approaches.                                      The Code Specialist generates FFI wrappers that approximate the
   This design also provides graceful degradation via a retry loop:                   vulnerability class of the original CVE rather than precisely repli-
when the Code Specialist’s generated code fails to compile, the                       cating its exploitation path. This is inherent to the incomplete-code
exact compiler error is fed back for up to two self-correcting at-                    problem: without the original struct definitions, trait implementa-
tempts before the fallback template is triggered. Only 3 of 31 files                  tions, and calling context, no automated tool can reconstruct the
(9.7%) required the fallback, compared to 42% with the single-agent                   exact program state that produced the vulnerability. Our approach
baseline.                                                                             accepts this approximation deliberately—the goal is to generate
                                                                                      a compilable, KLEE-analyzable artifact that preserves the class of
                                                                                      memory error rather than the exact exploit.
                                                                                         This explains the lower detection rates for CWE-416 (Use-After-
7.2     The Incomplete-Code Breakthrough                                              Free, 6/9 files) and CWE-190 (Integer Overflow, 1/3 files). Use-after-
A defining contribution of this work is enabling vulnerability anal-                  free vulnerabilities depend on specific object lifetime sequences
ysis on code that no existing tool can even compile. Every formal                     across multiple function calls, which are difficult to reproduce faith-
verification tool in our baseline requires a complete, self-contained                 fully in a standalone FFI function. Improving detection for these
Rust program with a Cargo manifest—CVE snippets never satisfy                         classes would likely require richer context extraction—retrieving
this. Our Code Specialist sidesteps this constraint by generating                     the full source file from the CVE repository rather than relying
a new, compilable artifact that encodes the vulnerability class in                    on the snippet alone—or a specialized agent trained on lifetime-
KLEE-compatible types. This is semantic approximation rather than                     dependent vulnerability patterns.
code repair: the generated FFI wrapper does not reconstruct the
original program but instead creates a symbolically equivalent rep-                   8 Threats to Validity
resentation of the fault class. A struct-dependent use-after-free                     8.1 Internal Validity
becomes an explicit dealloc followed by a pointer write; an in-
teger overflow becomes an unchecked multiplication used as an                         LLM Non-Determinism. All four agents use default API tem-
allocation size. The 90.3% compilation success rate versus 0% for                     perature settings, so two runs on the same CVE file may produce
all formal tools is the empirical measure of this architectural shift.                different FFI wrappers, risk scores, and KLEE parameters. We miti-
                                                                                      gate this by storing all generated artifacts in our replication package
                                                                                      so results can be inspected without re-querying the APIs.
                                                                                         FFI Semantic Fidelity. Generated wrappers approximate the
                                                                                      vulnerability class rather than its precise exploitation path. A wrap-
7.3     Interpretation of KLEE Error Types                                            per misclassified as buffer-overflow for a use-after-free CVE pro-
Pointer errors (*.ptr.err, 124 total) are the strongest signal: KLEE                  duces real KLEE errors of the wrong class. The Oracle’s JSON plan
directly observed an invalid memory access at the LLVM IR level—a                     constrains the Code Specialist to the correct CWE category and par-
null dereference, out-of-bounds write, or use-after-free—and pro-                     tially mitigates this risk, though the constraint is enforced through
duced a concrete symbolic input reproducing the fault. These rep-                     prompt engineering rather than formal verification.
resent exploitable memory-corruption conditions with high confi-                         KLEE Parameter Sensitivity. Detection coverage depends on
dence and should be treated as confirmed vulnerability indicators.                    the search strategy (DFS, BFS, random-path), time limit, memory
   External/panic errors (*.external.err, 1,082 total) require more                   limit, and fork depth—all set by Agent 4. We record all parameter
careful interpretation. When KLEE calls a Rust FFI function and the                   choices in the replication package to enable reproducible reruns.
Rust runtime invokes core::panicking::panic or __rust_dealloc,
KLEE cannot model the call symbolically and records it as an exter-                   8.2      External Validity
nal error. In CVE-specific functions such as use_after_free_access
                                                                                      Dataset Source and Diversity. Our 31 CVE files are the memory-
(CVE-2020-35904), the __rust_dealloc external error directly re-
                                                                                      safety subset of HALURust [18], not a stratified sample of all Rust
flects a memory deallocation violation tied to the original CVE class.
                                                                                      CVEs. Certain CWE categories (CWE-416 with 9 files) are better
However, in generic fallback functions such as test_division, the
                                                                                      represented than others (CWE-134 with 1 file), limiting per-category
panic from a zero denominator is an artifact of the generated wrap-
                                                                                      generalisation. A larger, stratified benchmark is needed for broader
per rather than a path from the original CVE code.
                                                                                      claims.
   The ratio of pointer errors to external errors varies significantly
                                                                                         Model Availability and Versioning. Our system relies on GPT-
by CWE category. CWE-119 (Buffer Overflow) and CWE-787 (Out-
                                                                                      4 Turbo, GPT-4o-mini, Claude Opus 4.5, and Claude Sonnet 4.5.
of-Bounds Write) produce a higher proportion of pointer errors
                                                                                      Model updates may alter wrapper compilation rates; exact versions
because the violations manifest as direct invalid memory accesses at
                                                                                      are documented in our replication package.
the LLVM level. CWE-416 (Use-After-Free) and CWE-415 (Double
Free) tend to produce more external errors because the deallocation
violations surface through Rust’s runtime allocator. Practitioners                    8.3      Construct Validity
should weight pointer errors at higher confidence than external                       Error Count as a Proxy. KLEE’s critical error count measures sym-
errors, and discriminate between external errors arising in CVE-                      bolic path coverage, not distinct vulnerability instances. A single
specific functions versus generic fallback patterns.                                  root cause may produce hundreds of errors from different symbolic
SSE ’26, June 9–12, 2026, Glasgow, Scotland, United Kingdom                                                                                 Zeyad Abdelrazek and Young Lee


inputs. We treat pointer errors as higher-confidence signals than                        [2] James Bornholt. 2020. Haybale: Symbolic Execution of Rust Programs. https:
external/panic errors, and recommend inspecting individual error                             //github.com/PLSysSec/haybale.
                                                                                         [3] Cristian Cadar, Daniel Dunbar, and Dawson Engler. 2008. KLEE: Unassisted and
files rather than relying on aggregate counts alone.                                         Automatic Generation of High-Coverage Tests for Complex Systems Programs.
    Miri Comparison. Miri’s “100% detection” reflects generic undefined-                     In Proceedings of the 8th USENIX Symposium on Operating Systems Design and
                                                                                             Implementation (OSDI). 209–224.
behavior labels that do not discriminate by CWE category, provide                        [4] Jia Chen et al. 2023. Detecting Rust Unrecoverable Panics via Symbolic Execution.
no symbolic counterexamples, and identify no specific lines. Our                             In Proceedings of the International Symposium on Software Testing and Analysis.
system produces typed, location-specific errors with concrete ex-                            ACM.
                                                                                         [5] Mark Chen et al. 2021. Evaluating Large Language Models Trained on Code.
ample inputs—qualitatively more actionable for triage despite the                            arXiv preprint arXiv:2107.03374 (2021).
lower headline rate.                                                                     [6] Yinghao Chen et al. 2023. ChatUniTest: A Framework for LLM-Based Test
                                                                                             Generation. In Proceedings of the 32nd ACM International Symposium on Software
                                                                                             Testing and Analysis (ISSTA).
9    Conclusion                                                                          [7] Vitaly Chipounov, Volodymyr Kuznetsov, and George Candea. 2011. S2E: A
                                                                                             Platform for In-Vivo Multi-Path Analysis of Software Systems. In Proceedings
This paper presented a 4-agent multi-LLM pipeline combined with                              of the 16th International Conference on Architectural Support for Programming
KLEE symbolic execution for detecting memory vulnerabilities in                              Languages and Operating Systems (ASPLOS).
                                                                                         [8] Gelei Deng et al. 2024. PentestGPT: A GPT-Empowered Automatic Penetration
Rust unsafe code. Our central contribution is solving the incomplete-                        Testing Tool. In Proceedings of the 33rd USENIX Security Symposium.
code problem: real-world CVE database entries consist of isolated                        [9] Yinlin Deng et al. 2023. TitanFuzz: Black-Box Fuzzing of Deep-Learning Libraries
code snippets that lack the struct definitions, import statements,                           via Large Language Models. Proceedings of the 45th International Conference on
                                                                                             Software Engineering (ICSE) (2023).
and Cargo manifests required by every existing formal verification                      [10] Xavier Denis, Jacques-Henri Jourdan, and Claude Marché. 2022. Creusot: A
tool. All four formal tools evaluated—Kani, Prusti, Creusot, and                             Foundry for the Deductive Verification of Rust Programs. Lecture Notes in Com-
                                                                                             puter Science 13047 (2022), 90–105.
Haybale—achieved 0% compilation success on our 31-file dataset.                         [11] Patrice Godefroid, Nils Klarlund, and Koushik Sen. 2005. DART: Directed Au-
Our system achieved 90.3% by having a role-specialized Code Spe-                             tomated Random Testing. In Proceedings of the ACM SIGPLAN Conference on
cialist generate self-contained, KLEE-compatible FFI wrappers that                           Programming Language Design and Implementation (PLDI). 213–223.
                                                                                        [12] Patrice Godefroid, Michael Y Levin, and David Molnar. 2008. Automated White-
preserve the vulnerability class without requiring original program                          box Fuzz Testing. In Proceedings of the 15th Network and Distributed System
context.                                                                                     Security Symposium (NDSS).
    Evaluated across 31 real-world Rust CVEs spanning 11 CWE cat-                       [13] Sirui Hong et al. 2023. MetaGPT: Meta Programming for a Multi-Agent Collabo-
                                                                                             rative Framework. arXiv preprint arXiv:2308.00352 (2023).
egories, our system detected 1,206 critical errors in 26 files (83.9%                   [14] Bo Jiang et al. 2024. Crabtree: LLM-Guided Fuzz Driver Generation for Rust. In
detection rate), compared to 14 warnings across 11 files for Clippy                          Proceedings of the 33rd USENIX Security Symposium.
                                                                                        [15] Steve Klabnik and Carol Nichols. 2019. The Rust Programming Language. No
(35.5%) and generic labels for Miri. There were zero files where                             Starch Press.
Clippy detected a vulnerability that our system missed, demon-                          [16] Martin Larsson. 2019. cargo-geiger: Detects unsafe Rust Code. https://github.
strating that our approach fully subsumes pattern-based linting                              com/rust-secure-code/cargo-geiger.
                                                                                        [17] Peng Liu et al. 2020. Targeted Symbolic Execution for Use-After-Free Detection. In
while finding substantially more path-dependent bugs. The 4-agent                            Proceedings of the 35th IEEE/ACM International Conference on Automated Software
architecture reduced wrapper compilation failures from 42% (single-                          Engineering.
agent baseline) to 9.7%, and increased detected errors from 487 to                      [18] Yu Luo, Han Zhou, Mengtao Zhang, Dylan De La Rosa, Hafsa Ahmed, Weifeng
                                                                                             Xu, and Dianxiang Xu. 2025. HALURust: Exploiting Hallucinations of Large
1,206, confirming that role specialization and structured context                            Language Models to Detect Vulnerabilities in Rust. arXiv:2503.10793 [cs.CR]
passing produce measurably better results than a single general-                             https://arxiv.org/abs/2503.10793
                                                                                        [19] Nicholas D Matsakis and Felix S Klock. 2014. The Rust Programming Language.
purpose model.                                                                               ACM SIGAda Ada Letters 34, 3 (2014), 103–104.
    These results answer our three research questions affirmatively:                    [20] Scott Olson, Oliver Günther, et al. 2018. Miri: An Interpreter for Rust’s Mid-level
symbolic execution can detect Rust memory vulnerabilities across                             Intermediate Representation. https://github.com/rust-lang/miri.
                                                                                        [21] Chen Qian et al. 2024. ChatDev: Communicative Agents for Software Develop-
all major CWE categories (RQ1); LLM-generated FFI wrappers can                               ment. In Proceedings of the 62nd Annual Meeting of the Association for Computa-
bridge the incomplete-code gap at 90.3% success where formal                                 tional Linguistics.
tools achieve 0% (RQ2); and a 4-agent coordinated architecture does                     [22] Koushik Sen, Darko Marinov, and Gul Agha. 2005. CUTE: A Concolic Unit Testing
                                                                                             Engine for C. In Proceedings of the 13th ACM SIGSOFT Symposium on Foundations
outperform a single-agent approach across all measured dimensions                            of Software Engineering. 263–272.
(RQ3).                                                                                  [23] Yan Shoshitaishvili, Ruoyu Wang, Christopher Hauser, Christopher Kruegel, and
                                                                                             Giovanni Vigna. 2015. Concretely Mapped Memory for Symbolic Execution. In
    For future work, we plan to extend the dataset to a larger, strat-                       Proceedings of the 22nd ACM SIGSAC Conference on Computer and Communications
ified sample of Rust CVEs, improve detection rates for lifetime-                             Security.
dependent vulnerability classes (CWE-416, CWE-190) by incorpo-                          [24] Yuqiang Sun et al. 2024. LLM4Vuln: A Unified Evaluation Framework for Decou-
                                                                                             pling and Enhancing LLMs’ Vulnerability Reasoning. In Proceedings of the 33rd
rating richer source context from CVE repositories, and explore                              USENIX Security Symposium.
fine-tuned models for the Code Specialist role to reduce the 9.7%                       [25] Michele Tufano et al. 2022. AthenaTest: Unit Test Generation Using LLMs. In
fallback rate further. We also intend to investigate bidirectional                           Proceedings of the 30th ACM Joint European Software Engineering Conference and
                                                                                             Symposium on the Foundations of Software Engineering.
feedback between KLEE error traces and the agent pipeline, en-                          [26] Alexa VanHattum, Daniel Schwartz-Narbonne, Nathan Chong, and Adrian Samp-
abling the system to refine FFI wrappers based on which symbolic                             son. 2022. Kani: Catching Bugs, Automatically, in Safe Rust. In Proceedings of the
                                                                                             International Conference on Software Engineering: Software Engineering in Practice.
paths produced the most informative errors.                                                  ACM, 138–149.
                                                                                        [27] Junjie Wang et al. 2023. A Survey on Large Language Models for Software Testing.
                                                                                             arXiv preprint arXiv:2307.07221 (2023).
References                                                                              [28] Zhun Xu et al. 2024. AutoAttacker: A Large Language Model Guided System to
 [1] Vytautas Astrauskas, Christoph Matheja, Federico Poli, Peter Müller, and Alexan-        Implement Automatic Cyber-attacks. In Workshop on Large Language Models for
     der J Summers. 2019. Leveraging Rust Types for Modular Specification and                Code at ICLR.
     Verification. In Proceedings of the ACM on Programming Languages, Vol. 3. ACM,     [29] He Ye, Matias Martinez, and Martin Monperrus. 2022. VulnFix: Fast Patch Vali-
     1–30.                                                                                   dation via Symbolic Execution. In Proceedings of the 37th IEEE/ACM International
Symbolic Execution Meets Multi-LLM Orchestration: Detecting Memory Vulnerabilities in Incomplete Rust CVE Snippets
                                                                                                           SSE ’26, June 9–12, 2026, Glasgow, Scotland, United Kingdom


     Conference on Automated Software Engineering.                                     [31] Yaojie Zheng et al. 2023. Large Language Models for Test Input Generation in
[30] Jian Zhang et al. 2024. Multi-Agent Software Engineering: A Survey. In Proceed-        Symbolic Execution. In Proceedings of the 38th IEEE/ACM International Conference
     ings of the ACM/IEEE International Conference on Software Engineering. ACM.            on Automated Software Engineering.
