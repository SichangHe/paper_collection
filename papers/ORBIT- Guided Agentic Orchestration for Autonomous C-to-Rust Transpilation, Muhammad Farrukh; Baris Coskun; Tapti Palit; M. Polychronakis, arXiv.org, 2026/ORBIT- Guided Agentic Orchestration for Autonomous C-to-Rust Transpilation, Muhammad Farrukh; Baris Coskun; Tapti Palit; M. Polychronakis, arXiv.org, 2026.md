                                                      ORBIT: Guided Agentic Orchestration for Autonomous
                                                                    C-to-Rust Transpilation
                                                                    Muhammad Farrukh                                                    Baris Coskun∗
                                                                   Stony Brook University                                            Amazon Web Services
                                                                       New York, USA                                                    New York, USA
                                                                mufarrukh@cs.stonybrook.edu                                          barisco@amazon.com

                                                                             Tapti Palit                                         Michalis Polychronakis
                                                                University of California, Davis                                    Stony Brook University
                                                                         Davis, USA                                                    New York, USA
arXiv:2604.12048v1 [cs.SE] 13 Apr 2026




                                                                     tpalit@ucdavis.edu                                           mikepo@cs.stonybrook.edu

                                         Abstract                                                                 and the Great Refactor [6] reflect a systematic community effort
                                         Large-scale migration of legacy C code to Rust offers a promising        to address this challenge at scale. Automated C-to-Rust transla-
                                         path toward improving memory safety, but LLM-based C-to-Rust             tion offers a promising path toward this goal, enabling large-scale
                                         translation remains challenging due to limited context windows and       modernization without requiring complete manual rewriting.
                                         hallucinations. Prior approaches are evaluated primarily on small            Earlier automated approaches adopted predefined rule-based
                                         programs or datasets skewed toward small codebases, providing            transpilation techniques [7–11] that scale to large codebases with-
                                         limited insight into scalability on real-world systems. They also rely   out incurring model inference costs. However, these methods pro-
                                         on static context construction, which breaks down in the presence        duce unsafe and unidiomatic Rust code that is difficult to maintain
                                         of complex cross-module dependencies and often requires manual           and forfeits the safety guarantees that motivate migration in the
                                         intervention. Recent coding agents offer a promising alternative         first place. Recent work has therefore shifted towards leveraging
                                         through dynamic codebase navigation and context curation. When           large language models (LLMs) as the primary translation engine,
                                         used out of the box, however, they frequently produce incomplete         owing to their ability to generate idiomatic and safe code. Despite
                                         translations that appear superficially correct.                          their impressive abilities, LLM-based approaches face two principal
                                             We present ORBIT, an autonomous agentic framework for                challenges: (i) semantic correctness, which recent studies address
                                         project-level C-to-Rust translation that combines dynamic context        through various verification and repair techniques [12–16]; and
                                         collection with dependency-guided orchestration and iterative ver-       (ii) limited context window, which restricts the amount of code that
                                         ification. ORBIT constructs a dependency-aware translation graph,        can be translated in a single inference call. A substantial body
                                         generates Rust interfaces, maps C functions to Rust counterparts,        of work [17–20] has addressed the limitation of context, yet two
                                         and coordinates multiple specialized agents. We evaluate ORBIT           significant gaps remain.
                                         on 24 programs from CRUST-Bench, with 91.7% of the programs                  Limited evaluation scale. Although recent tools [18, 21–23]
                                         exceeding 1,000 lines of code. ORBIT achieves 100% compilation           claim to handle larger C programs (>500 LoC), their evaluation
                                         success and 91.7% test success in both expert-interface and auto-        benchmarks consist predominantly of small programs, with only a
                                         matically generated-interface settings, substantially outperforming      small fraction exceeding 1,000 LoC. Table 1 provides a comprehen-
                                         C2Rust and CRUST-Bench, while reducing unsafe Rust code blocks           sive comparison across tools, showing that most prior works oper-
                                         to nearly zero. We further evaluate ORBIT on challenging cases           ate on datasets with median program sizes well below 1K LoC. Some
                                         from the DARPA TRACTOR benchmark, where it achieves compet-              tools do not report dataset sizes explicitly, therefore we only present
                                         itive performance relative to participating systems.                     those for which we can provide best-effort approximations. We ex-
                                                                                                                  clude LLM-based approaches that refine C2Rust output [17, 24],
                                         1    Introduction                                                        because the resulting translation still contains a large amount of
                                                                                                                  unsafe code blocks compared to approaches that directly start with
                                         The widespread use of legacy C code continues to expose critical sys-    LLM output, and Tymcrat [25], which targets large repositories but
                                         tems to memory safety vulnerabilities. Microsoft has reported that       performs type migration on function subsets rather than complete
                                         70% of CVEs originate from memory corruption [1], and decades            translation. Such evaluations fail to capture the structural complex-
                                         of effort to integrate memory safety mechanisms into C/C++ have          ity and cross-module dependencies of real-world codebases.
                                         failed to achieve broad adoption due to performance and compati-             Complex static analysis for program decomposition. To
                                         bility constraints. In contrast, Rust is a modern systems language       address the context window limitation, several approaches employ
                                         that enforces memory safety at compile time through its owner-           static analysis to curate the dependencies of translation units, (e.g.,
                                         ship and borrowing model, with a growing effort to make it secure        helper functions, type definitions, and macros) and perform incre-
                                         and mature from industry and academia [2–4]. This has motivated          mental translation in dependency order. However, Li et al. [26]
                                         significant interest in migrating critical software systems from C to    report that VERT [15] and Flourine [13] required substantial man-
                                         Rust. Recent initiatives such as DARPA’s TRACTOR program [5]             ual effort to produce an initial translation on a new dataset. Sim-
                                         ∗ This work does not relate to Baris Coskun’s position at Amazon.        ilarly, several works [18, 23, 27] require human intervention to
resolve complex dependencies or struct types. Beyond that, the                Table 1: Comparison of datasets used in prior C-to-Rust trans-
use of complex techniques to aid the LLM during translation, such             lation works.
as lifetime dependency tracking, pointer aliasing, and ownership
analysis, struggle due to the inherent complexities of static analysis.           Tool               Dataset                   #Prog   %>1K    Med     Mean
These limitations reflect a broader challenge: context construc-                  RustMap [23]       Rosetta Code, Bzip2        126    ∼1%     ∼80     ∼145
                                                                                  Syzygy [18]        Zopfli, URL parser          2     50%     2700    2700
tion is largely static and predetermined prior to translation, leaving            EvoC2Rust [22]     C2R-Bench,        Vivo-    25     ∼8%     ∼400    ∼600
systems unable to adapt when the initially curated context is incom-                                 Bench
                                                                                  RustAssure [16]    5 C Libs                    5     20%     405     ∼900
plete or misaligned with the translation task. Effective C-to-Rust                SmartC2Rust [21]   GitHub, Prior Studies      21     ∼24%    502     ∼1000
translation therefore requires not only context-aware generation,                                    Data
                                                                                  VERT [15]          TransCoder-IR, Prior       534     0%     ∼100    ∼120
but also the ability to dynamically acquire, validate, and refine                                    Studies
context during execution.                                                         ORBIT              CRUST-Bench                24     91.7%   1,354   1,603
   Recent advances in coding agents provide a natural abstraction
for addressing both gaps. Modern agentic systems such as GitHub
Copilot, Codex, and Claude Code have become deeply integrated                 • We present ORBIT, a fully autonomous agentic framework for
into the software development lifecycle [28–31]. By enabling tool               translating large-scale C projects into functional and memory-
interaction and feedback-driven refinement, agentic systems can dy-             safe Rust, requiring no manual intervention in the translation
namically gather missing context, resolve dependencies, and adapt               process.
translation strategies based on intermediate failures. However, in            • We present the first rigorous evaluation of an LLM-based C-to-
our preliminary experiments we observed that vanilla coding agents              Rust translation tool on a benchmark where over 90% of the
used in a single-shot setting frequently produce incomplete transla-            programs exceed 1,000 LoC, demonstrating scalability to real-
tions while misleadingly reporting success—as shown in Section 4.3,             world codebases.
the base agent achieves build and test success while covering only            • We systematically demonstrate that vanilla coding agents yield
64.4% of functions and 3.0% of test cases. This behavior is particu-            incomplete translations that appear correct under standard build
larly pronounced in open-source models. Furthermore, even when                  and test metrics, exposing a critical gap between superficial
agents do produce translations, Khatry et al. [32] report that agents           correctness and true functional completeness.
perform a disproportionately large number of codebase navigation
steps, suggesting that careful orchestration is required to unlock
                                                                              2     ORBIT Overview
their potential as autonomous translation systems.
   In this paper, we present ORBIT, an agentic framework for C-               In this section, we describe the architectural details of ORBIT. The
to-Rust translation that addresses these limitations. Unlike prior            primary design goal of ORBIT is to leverage the capabilities of
approaches that rely on complex static analysis for context con-              coding agents to abstract away the engineering complexities of
struction, ORBIT employs lightweight call-site analysis for ordering          automated translation, while decomposing the translation task into
and delegates context curation to the agent itself, allowing the sys-         a structured, multi-stage format. ORBIT consists of four main com-
tem to dynamically adapt to intermediate failures. ORBIT supports             ponents as illustrated in Figure 1: (i) Sorted Dependency Graph
both expert-provided Rust interfaces and interfaces generated au-             Generator, which parses C source code into a dependency graph
tomatically via Agentic Iterative Scaffolding, making it applicable           and produces a topologically sorted ordering at both the module
without manual input.                                                         and function levels; (ii) Agentic Iterative Scaffolding, which creates
   We evaluate ORBIT on a benchmark of 24 programs derived                    a memory-safe Rust project skeleton corresponding to a given C
from CRUST-Bench [32], with 91.7% of them exceeding 1,000 LoC                 repository containing translated data types, interfaces, and test
(Table 1), using two state-of-the-art agents: Opencode with Qwen3-            suites; (iii) Function Mapper, which takes the sorted C modules
Coder-480B and Codex with GPT-5.2-Codex. When run with Qwen,                  and functions alongside Rust interfaces to establish a correspon-
which is less capable than GPT-Codex, ORBIT achieves 100% com-                dence between them, used subsequently during translation; and
pilation success and 91.7% test success on all 24 CRUST-Bench pro-            (iv) Translation Orchestrator, which coordinates multiple specialized
grams in both interface configurations, substantially outperforming           agents and performs deterministic verification on agent-generated
C2Rust (62.5% compilation, 20.8% test success) and CRUST-Bench                outputs.
(45.8% compilation, 25.0% test success). On the safety dimension,
ORBIT reduces the average number of unsafe lines of code to 0.06%             2.1     Sorted Dependency Graph Generator
and 0.11% under the two interface configurations, compared to                 Given a source C repository, ORBIT employs a parser built on Tree-
69.6% for C2Rust. We further evaluate ORBIT on the DARPA TRAC-                sitter [33] to generate an Abstract Syntax Tree (AST) for each .c
TOR benchmark, achieving a pass rate of ∼70% (9/13) on the hardest            and .h file in the codebase. Rather than tracking all source code
programs in the battery, placing it competitively within the range            constructs such as variables, structs, and type definitions, the parser
of six performer systems.                                                     focuses exclusively on two primary entity types: (1) Function Nodes,
   In summary, our main contributions are as follows:                         encompassing standard function signatures, macro-wrapped names,
                                                                              and static inline functions; and (2) Include Nodes, which capture
                                                                              file-level dependencies. From these entities, ORBIT constructs a
                                                                              dual-layered dependency graph comprising two sub-graphs: (a) an
                                                                              Intra-Module Graph, which captures local dependencies between
                                                                          2
                                                        User Provided


                                                                                                       Rust
                                                      Agentic Iterative                             Interfaces
                                                        Scaffolding

                                                                                                                                        Function Mapper
                                                                                        0 < c_module, c_function >

                                                                                                                                            Mapping
                                                                                        1 < c_module, c_function >
                                                                                                                                            Resolved
               C Source
                                                                                        2 < c_module, c_function >                                              Mapping Agent
               Repository                  C Parser             Dependency Graph                                       Static Search




                 <C> [Module, Function]



               <Rust> [Module, Function]                 Translator           Implementation             Compiler                        Refactor      Verifier Agent
                                                           Agent                 Checker                  Agent          Compilable       Agent                           Verified
                                                                                                                         Rust Project                                   Rust Project




                                                                              Translation Orchestrator


                                                                          Figure 1: Overview of the ORBIT.


functions within the same source or header file (module); and                                             files with non-declaration content are preserved with a _h suffix.
(b) an Inter-Module Graph, which tracks high-level dependencies                                           Type Translation (Lines 4–6): C type definitions (struct, union,
between Module Groups, defined as logical groupings of related                                            enum, macros, primitives) are mapped into the corresponding Rust
.c and .h files. To ensure that foundational entities are processed                                       modules. Function Signature Resolution (Lines 7–10): Rust function
before those that depend on them (a requirement for both correct                                          signatures are generated for each C function, with bodies stubbed as
translation order and successful compilation) ORBIT applies Kahn’s                                        unimplemented!(), producing a structurally complete skeleton for
algorithm [34] in two stages:                                                                             downstream mapping. Safety Refactoring (Lines 11–15): Raw pointer
• Intra-Module Sort: Functions within a single file are ordered                                           signatures and unsafe constructs are iteratively refactored towards
  such that callees precede their callers wherever the dependency                                         safe Rust abstractions. Test Suite Translation (Lines 16–18): The C
  structure permits.                                                                                      test suite is translated into Rust #[test] functions and integrated
• Inter-Module Sort: Modules are ordered according to the inter-                                          into the cargo test harness. Verification (Lines 19–20): A final
  module dependency graph, ensuring that base libraries and util-                                         Verify&Repair pass resolves residual structural errors, yielding a
  ity headers are processed prior to the higher-level logic that                                          type-checked skeleton R.
  depends on them.
   This two-stage sorting establishes a dependency-aware trans-
lation order and lays the groundwork for constructing C-to-Rust
function mappings in subsequent stages. Since C projects frequently                                       2.3        Function Mapper
contain circular dependencies, ORBIT detects such cycles and groups                                       Establishing a precise correspondence between C functions and
the involved entities into a single translation unit, preserving cor-                                     their Rust counterparts is non-trivial due to the fundamental id-
rectness while maintaining translation progress.                                                          iomatic differences between the two languages. The Translation
                                                                                                          Orchestrator requires an exact, unambiguous mapping from every
2.2    Agentic Iterative Scaffolding                                                                      C function to its corresponding Rust stub in the skeleton, as this
This component is responsible for generating a type-checked Rust                                          mapping instructs the translation agent precisely which stub to
project skeleton, which serves as a precursor to the main translation                                     implement at each step. Without it, the agent has no well-defined
loop. Rather than relying on complex static analysis to discover                                          target and risks missing function implementations.
translation units, such as global variables and type definitions,                                            This challenge is most pronounced when using manually cu-
ORBIT employs an off-the-shelf coding agent to perform the scaf-                                          rated Rust skeletons. Figure 2 illustrates an example using both
folding directly. Recent advancements in coding agents enable them                                        auto-generated and manually curated Rust stubs derived from a
to automatically curate the necessary context based on the task at                                        C function in the LTRE program from CRUST-Bench [32]. In the
hand. However, they remain prone to failure when presented with                                           manually curated interface, the C function nfa_get_size (which
a single large monolithic task. Therefore, ORBIT relies on a multi-                                       operates on a struct) is lifted into an associated method Nfa::len,
stage iterative process to guide the agent through the scaffolding                                        fundamentally reorganising the function structure. In such cases,
incrementally. Algorithm 1 outlines the key steps in this process:                                        string-matching heuristics fail to recover the correct correspon-
   Project Skeleton Initialization (Lines 1–3): ORBIT runs cargo new                                      dence or lead to false positives. As a secondary concern, surface-
and creates Rust modules mirroring each C source file; header                                             level naming inconsistencies compound the problem further. For
                                                                                                    3
       Algorithm 1: Agentic Iterative Scaffolding
    Input: C : C repository; A : coding agent; 𝑁 : max repair attempts; 𝐾 : max refactor attempts;
          𝑇𝑜𝑢𝑡 : stage timeout
    Output: R : compilable Rust skeleton
 1: R ← ∅ ;
 2: R ← CargoNew ( C, A, 𝑇𝑜𝑢𝑡 ) ;
 3: R ← Compile&Repair ( R, A, 𝑁 , 𝑇𝑜𝑢𝑡 ) ;
 4: while A identifies 𝑡 ∈ C𝑡 𝑦𝑝𝑒𝑠 ∧ ¬TimedOut (𝑇𝑜𝑢𝑡 ) do
 5:      R ← R ∪ { MapType (𝑡 ) } ;
 6: R ← Compile&Repair ( R, A, 𝑁 , 𝑇𝑜𝑢𝑡 ) ;
 7: while A identifies 𝑓 ∈ C𝑓 𝑛𝑠 ∧ ¬TimedOut (𝑇𝑜𝑢𝑡 ) do
 8:     𝑠𝑖𝑔 𝑓 ← MapSignature ( 𝑓 ) ;
 9:      R ← R ∪ {𝑠𝑖𝑔 𝑓 ⇒ unimplemented!() } ;
10: R ← Compile&Repair ( R, A, 𝑁 , 𝑇𝑜𝑢𝑡 ) ;
11: 𝑘 ← 0;
12: while ¬IsSafe ( R ) ∧ 𝑘 < 𝐾 do
13:      R ← Refactor ( R, A, 𝑇𝑜𝑢𝑡 ) ;
14:     𝑘 ← 𝑘 + 1;
15:   R ← Compile&Repair ( R, A, 𝑁 , 𝑇𝑜𝑢𝑡 ) ;
16:   while A identifies 𝜏 ∈ C𝑡𝑒𝑠𝑡𝑠 ∧ ¬TimedOut (𝑇𝑜𝑢𝑡 ) do
17:        R ← R ∪ { #[test] MapTest (𝜏 ) } ;
18: R ← Compile&Repair ( R, A, 𝑁 , 𝑇𝑜𝑢𝑡 ) ;
19: R ← Verify&Repair ( R, A, 𝑁 , 𝑇𝑜𝑢𝑡 ) ;
20: return R ;                                                                                             Figure 2: Two-tier function mapping strategy in ORBIT.
21: Function Compile&Repair ( R, A, 𝑁 , 𝑇𝑜𝑢𝑡 )
22:      𝑘 ← 0;
23:      while ¬IsCompilable ( R ) ∧ 𝑘 < 𝑁 do
24:            R ← Repair ( R, A, GetErrors ( R ), 𝑇𝑜𝑢𝑡 ) ;
25:            𝑘 ← 𝑘 + 1;
                                                                                                         counterparts, returning a structured JSON response identifying
26:       return R ;
                                                                                                         the matched rust_module and rust_function. In cases where no
                                                                                                         Rust equivalent exists, such as C deallocator functions that have no
                                                                                                         counterpart in Rust due to its built-in ownership and deallocation
      instance, in the same program, bitset_get is preserved in the auto-                                model, the Mapping Agent assigns null to the fields.
      generated interface but is renamed to bitset_test in the manual                                       Since LLMs are inherently prone to hallucination, every map-
      one.                                                                                               ping resolved by the Mapping Agent passes through a validation
          To handle both cases robustly without requiring any configura-                                 step before being committed. The validator confirms that both
      tion changes, ORBIT employs a two-tier mapping strategy: a fast,                                   the c_module and rust_module paths actually exist and that the
      deterministic static search as the primary tier, with a Mapping                                    mapped rust_function is present within the specified Rust file via
      Agent fallback invoked only when all static matching strategies                                    a targeted static search. This prevents hallucinated mappings from
      are exhausted. As illustrated in Figure 2, when the auto-generated                                 propagating into the translation phase. If validation fails, the Map-
      skeleton is used, the static search resolves nfa_get_size directly                                 ping Agent is reinvoked for up to a specified number of attempts.
      via exact-match lookup. When the manually curated skeleton is
      used, the same function cannot be resolved statically due to the                                   2.4    Translation Orchestrator
      free-function-to-method transformation, and the Mapping Agent                                      Since functions are translated incrementally in dependency order,
      is invoked to reason over the semantic correspondence between                                      each translation step must be verified before proceeding, partial
      nfa_get_size and Nfa::len. This design ensures that ORBIT is                                       failures must be recoverable, and the overall process must remain
      agnostic to the origin of the Rust skeleton, supporting both auto-                                 resilient to the non-deterministic behavior of coding agents. The
      generated and manually curated interfaces within a unified pipeline.                               decomposition of translation into distinct, specialized agents is
                                                                                                         motivated by prior work demonstrating that role-specialized multi-
      2.3.1 Tier 1: Static Search. For each (c_module, c_function) pair
                                                                                                         agent systems consistently outperform monolithic single-agent
      drawn from the sorted topology, ORBIT first attempts a grammar-
                                                                                                         approaches on complex software engineering tasks [35–37]. The
      based lookup using ripgrep against the Rust project. The search
                                                                                                         Translation Orchestrator addresses these concerns by imposing a
      applies a strict matching hierarchy: it first attempts an exact lit-
                                                                                                         structured, iterative execution loop over the function mappings
      eral match of the C function name against Rust fn declarations,
                                                                                                         produced by the Function Mapper, treating each (C function, Rust
      followed by a normalised match in which both names are lower-
                                                                                                         stub) pair as an independent translation unit.
      cased and stripped of underscores and hyphens prior to comparison.
                                                                                                            For each translation unit, the Translation Agent is invoked to
      Looser forms of matching such as substring or prefix matching are
                                                                                                         generate the Rust implementation of the target C function. The
      deliberately excluded to prevent false-positive mappings.
                                                                                                         agent is provided with a translation prompt, an AGENTS.md file, and
      2.3.2 Tier 2: Mapping Agent Fallback. If static search yields no                                   access to both the C and Rust projects. We observed that coding
      result, the Mapping Agent is invoked with a structured prompt                                      agents tend to perform actions beyond the scope of the prompt,
      containing the target C function signature and its source mod-                                     such as prematurely running tests before the implementation is
      ule, alongside with full access to C and Rust projects. The agent                                  complete. To mitigate this, we analyzed agent behaviour on a set of
      reasons over semantic correspondence, parameter count, param-                                      sample prompts and introduced explicit constraints into the prompt
      eter types, and return types to identify structurally transformed                                  to suppress such over-eager actions.
                                                                                                     4
   Once the agent completes the implementation, an Implemen-                Table 2: Benchmark statistics. Projects are sampled from the
tation Checker is invoked to verify that the target Rust func-              CRUST-Bench collection of 100 C repositories.
tion has been genuinely implemented. This checker uses static
analysis to confirm that the function body contains neither an                                Project      LoC    #Func    #Files   #Tests
unimplemented!() macro nor TODO comments. The rationale for                                   CB            213       11        2        18
this explicit verification step stems from an observed failure mode:                          S-Conf        719       51        4        41
                                                                                              VaultSync   1,121       41       20         4
when used with certain open-source models, agents would simply                                mvptree     1,121       27        2        26
remove the unimplemented!() macro and replace the function                                    RazzSim     1,145       45        5       138
                                                                                              Remimu      1,162        3        1         3
body with TODO comments, satisfying the surface form of the                                   libpgn      1,162       64       26       476
prompt without producing a valid implementation. If the Imple-                                LTRE        1,212       45        4       368
mentation Checker fails, the Translation Agent is reinvoked for up                            LC-Eval     1,264       70       15       101
                                                                                              jccc        1,310       60       22        23
to a specified number of attempts.                                                            libpsbt     1,331       60       11         9
   Once a function is successfully implemented, the Translation                               mdb         1,340       28        4        52
                                                                                              GNNSC       1,367       65       28        24
Orchestrator invokes the Compiler Agent to ensure that the Rust                               impcheck    1,397      105       27        83
project compiles successfully with the new implementation. If com-                            cfsm        1,446        4       13         5
pilation errors are detected, the Compiler Agent attempts to repair                           worsp       1,494       62        2        70
                                                                                              libutf      1,525       81       33        87
the code iteratively until the project compiles or the maximum                                KComp       1,589      136       12         2
number of repair attempts is reached. Upon successful compila-                                fslib       1,958      103       24        11
                                                                                              XOpt        2,113       25        3        18
tion, the Translation Orchestrator records the translation unit as                            RecMgr      2,400       82       16        24
completed and advances to the next.                                                           libm17      2,901       45       10        26
   After all translation units have been processed, a Refactoring                             tisp        3,562      100        9       378
                                                                                              Megalania   3,621      101       41        27
Agent is invoked to eliminate unsafe operations introduced during
                                                                            Name Abbreviations: CB: CircularBuffer; S-Conf: Simple-Config; RazzSim:
translation. When this agent returns, the Rust project is passed to         razz_simulation; LC-Eval: lambda-calculus-eval; GNNSC: Genetic-neural-network-for-
the Verifier Agent, which runs the test suite and repairs any failing       simple-control; KComp: kairoCompiler; RecMgr: recordManager.
test cases within the allotted number of attempts. The result is a
complete, verified Rust translation of the source C codebase.
   A key design principle of ORBIT is that all agents operating             Agents and LLMs. To demonstrate the extensibility and adapt-
under the Translation Orchestrator are paired with deterministic            ability of ORBIT, we employ two off-the-shelf coding agents: Open-
verification steps. Rather than accepting an agent’s output at face         code [39] and Codex [40]. Opencode is an open-source coding agent
value, ORBIT independently confirms the result using static analysis        compatible with over 75 LLM providers, making it a highly versatile
or toolchain checks. For instance, after the Compiler Agent reports a       choice. We configure it with Qwen3-Coder-480B, an open-source
successful compilation, the Translation Orchestrator independently          model specialized for coding tasks, accessed via AWS Bedrock.
runs cargo check to confirm the verdict. This dual-layer approach           While Codex (from OpenAI) supports both local LLMs and pro-
guards against agent hallucination and ensures that pipeline state          prietary models, our preliminary testing revealed frequent silent
reflects ground truth rather than agent self-report.                        failures and tool-calling issues when utilizing non-OpenAI models.
                                                                            We therefore use Codex with the GPT-5.2-Codex model.

                                                                            4     Experimental Evaluation
3   Experimental Setup                                                      In this section we present the results of our experimental evaluation,
                                                                            focusing on the following main research questions:
Benchmark. Table 2 summarizes key characteristics of the selected
benchmarks, including lines of code (LoC), number of functions              • RQ1: Effectiveness of ORBIT relative to existing approaches in
(#Func), number of files (#Files), and the number of test cases. Our          terms of correctness and safety.
primary dataset is based on CRUST-Bench [32], a benchmark of                • RQ2: Evaluation using the DARPA TRACTOR dataset.
100 C repositories paired with manually generated Rust interfaces.          • RQ3: Evaluation of individual ORBIT components towards trans-
We extract benchmark statistics directly from the original dataset,           lation success.
applying minor corrections to discrepancies in the reported test case
counts. We evaluate ORBIT on a subset of 24 programs, prioritizing          4.1     RQ1: Correctness and Safety
repositories larger than 1,000 LoC and including a few smaller              4.1.1 Correctness Evaluation. Table 3 presents the correctness re-
programs to preserve diversity across application types. We focus           sults of ORBIT alongside two baselines on compilation and test
on larger repositories because prior work [38] has shown that LLM-          success metrics: i) C2Rust [7]: a rule-based transpiler developed by
based translation techniques struggle as program size and structural        Immunant and Galois that converts C code to Rust without LLM
complexity increase. This design allows us to evaluate ORBIT on             assistance; ii) CRUST-Bench [32]: a multi-step self-repair framework
more challenging and realistic migration tasks.                             for project-level C-to-Rust translation that employs a repair feed-
   CRUST-Bench includes a broad range of real-world applications            back loop to automatically correct translation errors. The bottom
from several domains, including programming language infrastruc-            row of the table reports the overall success rate across all evaluated
ture, algorithmic libraries, and system utilities.                          tools.
                                                                        5
Table 3: Correctness results on the 24 CRUST-Bench programs. For ORBIT, we distinguish two interface modes: ORBITExt uses
expert-written Rust interfaces provided by CRUST-Bench, while ORBITGen uses interfaces generated automatically by ORBIT.
✓ = success; ✗ = failure; – = not applicable. Abbreviated names: CB = CircularBuffer; S-Conf = Simple-Config; RazzSim =
razz_simulation; LC-Eval = lambda-calculus-eval; GNNSC = Genetic-neural-network-for-simple-control; KComp = kairoCom-
piler; RecMgr = recordManager.

                                          C2Rust                        CRUST-Bench                          ORBITExt                      ORBITGen
                             Trans.    Comp.                      Comp.                            Comp.                           Comp.
     Project         LoC                           Test Success                   Test Success                  Test Success                   Test Success
                             Success   Success                    Success                          Success                         Success
     CB                213     ✓          ✓             ✓           ✓                   ✓             ✓                 ✓              ✓              ✓
     S-Conf            719     ✗          –             –           ✓                   ✗             ✓                 ✓              ✓              ✓
     VaultSync       1,121     ✓          ✗             –           ✗                   –             ✓                 ✓              ✓              ✓
     mvptree         1,121     ✓          ✗             –           ✓                   ✓             ✓                 ✓              ✓              ✓
     RazzSim         1,145     ✓          ✓             ✗           ✓                   ✗             ✓                 ✓              ✓              ✓
     Remimu          1,162     ✓          ✓             ✓           ✗                   –             ✓                 ✓              ✓              ✓
     libpgn          1,162     ✓          ✓             ✗           ✓                   ✗             ✓                 ✗              ✓              ✓
     LTRE            1,212     ✓          ✗             –           ✓                   ✓             ✓                 ✓              ✓              ✗
     LC-Eval         1,264     ✓          ✓             ✓           ✓                   ✓             ✓                 ✓              ✓              ✓
     jccc            1,310     ✓          ✓             ✗           ✗                   –             ✓                 ✓              ✓              ✓
     libpsbt         1,331     ✓          ✓             ✗           ✗                   –             ✓                 ✓              ✓              ✓
     mdb             1,340     ✓          ✗             –           ✓                   ✓             ✓                 ✓              ✓              ✓
     GNNSC           1,367     ✓          ✗             –           ✗                   –             ✓                 ✓              ✓              ✓
     impcheck        1,397     ✗          –             –           ✗                   –             ✓                 ✗              ✓              ✓
     cfsm            1,446     ✓          ✓             ✓           ✓                   ✗             ✓                 ✓              ✓              ✓
     worsp           1,494     ✓          ✓             ✗           ✗                   –             ✓                 ✓              ✓              ✓
     libutf          1,525     ✓          ✓             ✗           ✗                   –             ✓                 ✓              ✓              ✓
     KComp           1,589     ✓          ✓             ✗           ✗                   –             ✓                 ✓              ✓              ✓
     fslib           1,958     ✓          ✓             ✗           ✗                   –             ✓                 ✓              ✓              ✓
     XOpt            2,113     ✓          ✗             –           ✓                   ✓             ✓                 ✓              ✓              ✓
     RecMgr          2,400     ✗          –             –           ✗                   –             ✓                 ✓              ✓              ✓
     libm17          2,901     ✓          ✓             ✗           ✓                   ✗             ✓                 ✓              ✓              ✓
     tisp            3,562     ✓          ✓             ✗           ✗                   –             ✓                 ✓              ✓              ✗
     Megalania       3,621     ✓          ✓             ✓           ✗                   –             ✓                 ✓              ✓              ✓
                              21/24      15/24         5/24        11/24               6/24          24/24          22/24           24/24         22/24
     Success Rate
                             (87.5%)    (62.5%)      (20.8%)      (45.8%)            (25.0%)        (100%)         (91.7%)         (100%)        (91.7%)



C2Rust. C2Rust successfully transpiles 21 out of 24 programs                  1   // Nested functions defined inside openTable ()
                                                                              2   int readIntFromHeader ( char ** hdr ) {
(87.5%), but its compilation success rate drops sharply to 15/24              3     int val = *( int *) (* hdr );
(62.5%), revealing that successful transpilation alone does not guar-         4     * hdr += sizeof ( int );
                                                                              5     return val ;
antee compilable output. Among the three transpilation failures,              6   }
one originates from a fundamental limitation of its Clang-based               7   void setSchemaAttributes (
                                                                              8        Schema *s , char ** hdr ) {
frontend: C2Rust cannot process GCC nested functions, a non-                  9     s -> numAttr = readIntFromHeader ( hdr );
                                                                             10     s -> keySize = readIntFromHeader ( hdr );
standard GCC extension [41] that permits function definitions to             11   }
appear inside other function bodies. In recordManager, the func-
tion openTable defines two nested helpers (readIntFromHeader                      Listing 1: GCC nested functions inside openTable
and setSchemaAttributes) directly within its body (Listing 1).                    (recordManager.c).
Since Clang rejects this GCC extension, C2Rust aborts at the tran-
spilation stage rather than producing incorrect output.                       1   // Closure inside open_table () captures         mutable offset
                                                                              2   let mut read_i32 =
   ORBIT resolves this by restructuring the nested functions as a             3     | data : &[ u8 ], off : & mut usize | -> i32   {
Rust closure captured within the enclosing function’s scope (List-            4        let v = i32 :: from_le_bytes (
                                                                              5           data [* off ..* off + 4]
ing 2). The closure read_i32 captures a mutable reference to the              6             . try_into () . unwrap ()
byte offset, producing semantically equivalent behaviour while                7        );
                                                                              8        * off += 4;
remaining fully safe Rust with no unsafe blocks. This example il-             9        v
                                                                             10     };
lustrates a broader advantage of agentic translation over rule-based         11   schema . num_attr = read_i32 ( header , & mut    offset );
transpilation: the LLM agent is not constrained by the syntactic             12   schema . key_size = read_i32 ( header , & mut    offset );
subset of C accepted by a particular compiler frontend, enabling it               Listing 2: ORBIT restructures nested functions as a closure
to produce idiomatic restructurings.                                              (Rust).
   Even among the 15 programs that compile successfully, C2Rust
achieves a test success rate of only 5/24 (20.8%), with runtime
crashes being the major reason.
CRUST-Bench. We run the CRUST-Bench pipeline with Qwen3-                          report that these configurations yield the best results [32]. CRUST-
Coder-480B under the default setting of three self-repair rounds per              Bench achieves a compilation success rate of 11/24 (45.8%) and a
task and a single-candidate greedy repair strategy, as the authors                test success rate of 6/24 (25.0%). The translations frequently contain
                                                                         6
unimplemented! macro invocations or incomplete fragments—a                                   in the source code that limit the LLM’s ability to generate safe code.
known limitation also reported by the original authors—that pre-                             For example, libm17 contains these global variables in both the
vent successful end-to-end execution. By contrast, ORBIT’s fine-                             original and the translated Rust version. For other programs with
grained control over the translation process eliminates such failures                        unsafe usage, the root cause varies between global variables (intro-
entirely, achieving 100% compilation success on all 24 programs.                             duced by the LLM later), raw pointer casting, or unsafe function
ORBIT. As described in Section 2, ORBIT supports both manually                               calls. On the 6 programs successfully compiled by all four tools,
provided and automatically generated Rust interfaces. To evaluate                            C2Rust averages 73.0% of unsafe lines of code, compared to 1.25%
each capability independently, we run ORBIT in two configurations:                           for CRUST-Bench, 0.00% for ORBITExt , and 0.10% for ORBITGen —a
ORBITExt and ORBITGen . The former uses expert-written Rust inter-                           reduction of 100% relative to C2Rust for ORBITExt , and over 98%
faces provided by CRUST-Bench. The latter employs Codex with                                 relative to CRUST-Bench.
GPT-5.2-Codex during the Agentic Iterative Scaffolding phase for                             ORBITExt . ORBITExt achieves zero lines of unsafe code in 19/24 pro-
interface generation, and it then switches to Opencode with Qwen3-                           grams, with an average %Unsafe of just 0.06%. Among the five
Coder-480B during translation orchestration, balancing translation                           programs with non-zero unsafe lines of code, the absolute counts
quality against cost.1                                                                       are negligible: mvptree, and impcheck contain at most 2 unsafe
   ORBITExt achieves 100% compilation success and a test success                             lines each, while KComp, RecMgr, and XOpt account for the ma-
rate of 22/24 (91.7%). ORBITGen , which generates interfaces automat-                        jority with maximum 16 unsafe lines, out of translation outputs
ically, matches the compilation success of ORBITExt at 24/24 (100%),                         exceeding 1,500 LoC. The raw pointer counts reflect the same pic-
and achieves an identical test success rate of 22/24 (91.7%), with                           ture: ORBITExt introduces only 35 raw pointer declarations and 5
failures on LTRE and tisp instead. The near-identical performance                            dereferences across all 24 programs, confirming that the agent con-
between the two modes demonstrates that ORBIT’s automatic inter-                             sistently eliminates the pervasive pointer arithmetic of the original
face generation is a viable substitute for manually crafted interfaces,                      C program and confines any residual unsafe code blocks to isolated
removing a significant practical barrier to adoption.                                        locations.
   Compared to both baselines, ORBIT substantially improves end-                             ORBITGen . ORBITGen achieves a comparable safety profile, achiev-
to-end correctness. Relative to C2Rust, ORBIT improves compilation                           ing zero lines of unsafe code in 21/24 programs, with an average
success from 58.3% to 100% and test-suite success from 20.8% to                              %Unsafe of 0.11%. ORBITGen eliminates unsafe code in two addi-
91.7%. Relative to CRUST-Bench, it improves compilation success                              tional programs compared to ORBITExt , though the programs that
from 45.8% to 100% and test-suite success from 25.0% to 91.7%. These                         retain residual unsafe lines are different (RazzSim (9 lines), KComp
improvements suggest that the main gains of ORBIT come from its                              (12 lines), and fslib (45 lines)), suggesting that automatic interface
modular and dependency aware agentic approach.                                               generation influences which pointer patterns the agent restruc-
                                                                                             tures rather than increasing overall unsafety. Raw pointer totals
4.1.2 Memory Safety Evaluation. Table 4 reports the memory                                   remain similarly low at 58 declarations and 6 dereferences. The
safety results across all four tools. We measure safety as the per-                          near-identical profile between the two configurations confirms that
centage of unsafe lines of code (%Unsafe) in the translated Rust                             automatic interface generation does not compromise safety, making
output, with lower values indicating a safer translation. Unlike prior                       ORBITGen a practical choice when manually written interfaces are
studies [32, 38, 44] that often perform aggregated memory safety                             unavailable.
analysis, ORBIT adopts a more granular, multi-dimensional safety
taxonomy: number of raw pointer declarations and dereferences,
along with total number of unsafe lines of code in relation to the                           4.2    RQ2: DARPA TRACTOR Dataset
total LoC, which complements the percentage unsafety. A dash                                 DARPA launched the TRACTOR program as a major research effort
(“–”) in the table indicates either that the tool fails the transpilation                    to develop scalable, automated techniques for translating large C
process, or its translation contains build failures.                                         codebases into memory-safe Rust [5]. As part of the program, a
Baselines. C2Rust produces translations that are unsafe through-                             test battery of 150 C programs was publicly released to evaluate
out, averaging 69.6% of unsafe lines of code across the 15 programs it                       the translation tools developed by the participating performers
successfully compiles, ranging from 20.4% (tisp) to 97.4% (Remimu).                          across a range of C features, accompanied by a detailed evaluation
This is expected, as C2Rust performs a structural one-to-one map-                            report [45] covering correctness and safety. We evaluate ORBIT on
ping of C constructs to Rust, preserving raw pointer arithmetic ver-                         this standard benchmark to understand how it performs compared
batim rather than reasoning about ownership. Since CRUST-Bench                               to the participants’ tools, and where it stands on challenging real-
translations include manually generated Rust Interfaces, this assists                        world programs.
the iterative repair loop to reduce unsafe code blocks substantially,                           The TRACTOR report presents aggregated results across per-
averaging 0.68% across the 11 programs it translates. However, three                         formers, covering overall failure rates and failure types, rather than
programs retain non-zero lines of unsafe code even after using safe                          fine-grained per-program, per-performer breakdowns. While this
interfaces: razz_simulation (1%), lambda-calculus-eval (2.5%),                               is sufficient to identify overall trends, it does not reveal which
and libm17 (4%). Despite the claim that CRUST-Bench provides                                 performer failed a given program or how many test vectors were
safe interfaces, we observed some instances of static mut usage                              missed, preventing a complete per-system comparison at the level
1 gpt-5.2-codex is significantly more expensive than qwen: input costs are approxi-
                                                                                             of individual programs and vectors. We therefore focus on the sub-
mately 3.89× higher ($1.75 vs. $0.45 per 1M tokens) and output costs are approximately       set of the most failure-prone programs identified in the evaluation.
7.78× higher ($14.00 vs. $1.80 per 1M tokens) [42, 43].                                      Since the TRACTOR test harness requires translations to be in a
                                                                                         7
Table 4: Safety analysis comparison across translation tools. ptr_d = raw pointer declarations; ptr_* = raw pointer dereferences;
uLoC = unsafe lines of code; %Unsafe = unsafe percentage of total LoC; LoC = total lines of code. “–” indicates the project was
either not translated or did not compile successfully for that tool. Highlighted rows (    ) denote programs where at least one
ORBIT configuration produced non-zero unsafe code.

                            C2Rust                             CRUST-Bench                          ORBITExt                     ORBITGen
 Project      ptr_d ptr_* uLoC %Unsafe          LoC ptr_d ptr_* uLoC %Unsafe LoC ptr_d ptr_* uLoC %Unsafe LoC ptr_d ptr_* uLoC %Unsafe LoC
 CB             171 100       530      82.3   644       0      0      0      0.0 292      0     0       0      0.0 273     0     0     0       0.0 259
 S-Conf           –    –        –         –     –       0      0      0      0.0 791      0     0       0      0.0 1074    0     0     0       0.0 1646
 VaultSync        –    –        –         –     –       –      –      –        –    –     0     0       0      0.0 959     0     0     0       0.0 1484
 mvptree          –    –        –         –     –       0      0      0      0.0 653      0     0       1      0.1 1147    0     0     0       0.0 2153
 RazzSim        391 211      1204      67.4 1787        2      0      6      1.0 607      0     0       0      0.0 1285    0     0     9       0.6 1572
 Remimu        1108 718      5258      97.4 5399        –      –      –        –    –     0     0       0      0.0 1318    0     0     0       0.0 1087
 libpgn         513 421      2006      75.0 2673        0      0      0      0.0 1246     0     0       0      0.0 2902    0     0     0       0.0 1952
 LTRE             –    –        –         –     –       0      0      0      0.0 1353     0     0       0      0.0 2827    0     0     0       0.0 1107
 LC-Eval       1004 350      2235      68.5 3264        0      0     26      2.5 1023     0     0       0      0.0 1501    0     0     0       0.0 1671
 jccc          1267 266      2131      64.2 3321        –      –      –        –    –     0     0       0      0.0 1662    0     0     0       0.0 1849
 libpsbt        645 328      1920      75.3 2550        –      –      –        –    –     0     0       0      0.0 1535   44     0     0       0.0 1578
 mdb              –    –        –         –     –       0      0      0      0.0 560      0     0       0      0.0 784     0     0     0       0.0 1596
 GNNSC            –    –        –         –     –       –      –      –        –    –     0     0       0      0.0 2145    0     0     0       0.0 2116
 impcheck         –    –        –         –     –       –      –      –        –    –     1     0       2      0.1 2193    0     0     0       0.0 2839
 cfsm           361 105      2203      86.0 2563        0      0      0      0.0   75     0     0       0      0.0 195     0     0     0       0.0 334
 worsp          696 879      2398      81.7 2936        –      –      –        –    –     0     0       0      0.0 2032    0     0     0       0.0 3581
 libutf         368 382      2441      82.8 2950        –      –      –        –    –     0     0       0      0.0 1656    1     0     0       0.0 2073
 KComp          952 236      2021      62.1 3253        –      –      –        –    –     8     1       4      0.2 1997   10     0    12       0.7 1668
 fslib         1269 734      4264      71.9 5928        –      –      –        –    –     0     0       0      0.0 3412    3     6    45       1.4 3197
 XOpt             –    –        –         –     –       6      0      0      0.0 837     20     4      16      1.0 1591    0     0     0       0.0 1789
 RecMgr           –    –        –         –     –       –      –      –        –    –     2     0       4      0.2 2450    0     0     0       0.0 3075
 libm17         240 242      1446      58.5 2473        0      0     49      4.0 1239     0     0       0      0.0 1141    0     0     0       0.0 1309
 tisp          1626 1189     5644      20.4 27741       –      –      –        –    –     0     0       0      0.0 3341    0     0     0       0.0 6906
 Megalania     1362 612      4186      51.2 8181        –      –      –        –    –     4     0       0      0.0 1725    0     0     0       0.0 2690


Table 5: Performance of ORBIT on the hardest TRACTOR                               which remain completely hidden from ORBIT during the translation
programs. Perf. Pass Rate denotes the number of performers                         process.
(out of six) that successfully translated each case. ORBIT                            Table 5 summarizes the performance of ORBIT across all selected
Result shows case-level outcome, and ORBIT Vec. Pass Rate                          programs. Overall, ORBIT achieves full correctness (“Pass”) on 9
denotes the percentage of test vectors passed.                                     out of the 13 programs (69.2%), and at least partial correctness on
                                                                                   11 of them (84.6%). When broken down by program type, ORBIT
  Type       Test Case
                                         Perf.       ORBIT      ORBIT Vec.         attains an 80% success rate on executable programs (4/5) and 62.5%
                                       Pass Rate     Result      Pass Rate         on library programs (5/8).
             016_switch-arith             3/6         Pass         100%               Despite the lack of per-performer results in the TRACTOR report,
             042_float_union              3/6         Pass         100%
  Exec       033_bitfield                 3/6         Pass         100%            a comparison at the aggregate level reveals that ORBIT performs
             030_int_underflow            2/6         Pass         100%            competitively with the six performers. The report identifies the av-
             002_stdin_echo               3/6        Partial       75%
                                                                                   erage performer pass rate across Battery 01 as 82.2% [45], with the
             read_scalefactors_lib        3/6         Pass         100%            top performer reaching 98.7% and the lowest reaching 48.0%. On the
             004_loop_lib                 2/6         Pass         100%
             read_side_info_lib           4/6         Pass         100%            13 programs we evaluated, the TRACTOR baseline pass rate (i.e., the
             wcscat_lib                   4/6         Pass         100%            fraction of performers that successfully translated each case) ranges
  Lib
             update_frame_header_lib      4/6         Pass         100%
             030_int_underflow_lib        2/6         Fail          0%             from 2/6 to 4/6, confirming these are among the most challenging
             contrast_ratio_lib           3/6        Partial       62.5%           programs in the battery. Against this backdrop, ORBIT achieves a
             hex2bin_lib                  2/6         Fail          0%
                                                                                   pass rate of ∼70% (9/13), which falls within the range of performers
                                                                                   on the full battery and notably surpasses the lowest-performing
specific output format, we extended ORBIT to support this format.                  system on our selected subset. On the executable programs specifi-
From the top-15 hardest cases, we select 13 programs, excluding two                cally, ORBIT matches or exceeds the majority of performers: all five
long-running cases that require additional configuration changes.                  executable cases have a performer pass rate of only 2–3 out of 6, yet
The selected set covers both executable and library programs, allow-               ORBIT passes four of them outright and achieves 75% vector cover-
ing us to evaluate ORBIT under different interface and behavioural                 age on the fifth. Among the library programs, ORBIT fully passes
constraints. Since TRACTOR does not release test vectors to trans-                 five cases, including read_scalefactors_lib and 004_loop_lib,
lation systems, and ORBIT requires seed tests for its iterative repair             of which only 2 out of 6 performers translated 004_loop_lib suc-
process, we construct initial test vectors manually to enable trans-               cessfully, and 3 out of 6 translated read_scalefactors_lib. To
lation and ensure a fair comparison. Importantly, all final results                enable testing, the TRACTOR test harness imposes stricter require-
are computed using the official TRACTOR-provided test vectors,                     ments on ABI compatibility, state preservation, and FFI boundaries.
                                                                               8
However, ORBIT is primarily designed and optimized to avoid the             Table 6: Ablation results for Orbit on three benchmarks.
use of FFI and to perform translation testing using cargo test. This        Func. Coverage is the percentage of C functions fully im-
explains the comparatively lower success rate on library programs           plemented in Rust. Test Coverage is measured against the
relative to executable programs.                                            original C test logic. Build success denotes passing cargo
   Among the partial and failing cases, the root cause is of-               check; Test success denotes passing cargo test. (CB = Circu-
ten not a failure to model pointer semantics or Rust’s owner-               larBuffer)
ship system, but rather subtle behavioral differences between C
standard library functions and their closest Rust equivalents. In                Prog.      Mode
                                                                                                                  Func.               Test            Build     Test
contrast_ratio_lib, ORBIT selected f32::powf as the counter-                                                   Coverage (%)        Coverage (%)       Succ.     Succ.

part to C’s pow(), but C implicitly promotes float arguments to                             base                    100.0                 0.0           ✓         ✓
                                                                                            w/o interfaces          100.0                 90.9          ✓         ✓
double before the computation, performing the exponentiation at                  CB
                                                                                            w/o mapping             100.0                 −− ∗          ✓         ✓
64-bit precision before casting back. Rust’s f32::powf operates                             full                    100.0                 −− ∗          ✓         ✓
entirely in single precision, producing slightly different results on                       base                     64.4                 3.0           ✓         ✓
boundary-value inputs. Similarly, in 002_stdin_echo, write_all                              w/o interfaces           82.2                 12.2          ✓         ✓
                                                                                 LTRE
                                                                                            w/o mapping              93.3                 −−            ✓         ✓
is used as the natural counterpart to fputs, yet fputs silently trun-                       full                    100.0                 −−            ✓         ✗
cates the output at the first null byte whereas write_all writes                            base                     84.1                  0.0          ✗         ✗
the full byte slice. These failures highlight a remaining gap in LLM                        w/o interfaces          100.0                 100.0         ✓         ✓
                                                                                 libm17
knowledge of the precise behavioral contracts of C functions and the                        w/o mapping             100.0                  −−           ✓         ✓
                                                                                            full                    100.0                  −−           ✓         ✓
subtle ways their Rust counterparts diverge from them—a limitation
                                                                            ∗ Test Coverage is not applicable for w/o mapping and full as the Rust scaffold provides complete
of current LLM-based approaches that calls for deeper exploration.
                                                                                                                  test implementations.

4.3    RQ3: Ablation Study
To evaluate the contribution of the key components of ORBIT in              approach is viable for small, self-contained programs. However, it
overall translation success, we conduct an ablation study across            produces no translated tests (0.0% test coverage), meaning the test
four settings: i) full, which runs the complete pipeline; ii) base,         success rests entirely on three shallow unit tests written by the
which translates the entire project in a single prompt without              agent rather than a translation of the original C validation suite.
the dependency graph, Rust interfaces, and translation orchestra-           As program complexity increases, base degrades substantially. On
tor; iii) w/o interfaces, which retains the translation orchestra-          LTRE, functional coverage drops to 64.4%—seven functions are miss-
tor and dependency graph but removes the initial Rust scaffold              ing outright and six are stubs—while test coverage collapses to 3.0%
and function mappings, requiring the agent to construct the Rust            (12 Rust tests vs. ∼450 C cases), with several of those tests pass-
project structure from scratch; and iv) w/o mapping, which retains          ing only because they exercise incomplete code paths. On libm17,
both the dependency graph and Rust interfaces but removes ex-               base fails to compile entirely due to syntax errors, including type
plicit function-level target mappings, leaving the agent to identify        mismatches, and borrow checker violations, producing no tests.
Rust counterparts independently. All settings use the same Open-            4.3.2 Impact of Removing Interfaces ( W/O Interfaces). Remov-
code agent with the Qwen3-Coder-480B model. We perform our                  ing the initial Rust scaffold, which in the full ORBIT setting is
evaluation on three benchmarks of varying size and complexity:              constructed using Agentic Iterative Scaffolding, while retaining
CircularBuffer (213 LoC, 11 functions), LTRE (1,212 LoC, 45 func-           the translation orchestrator that performs incremental transla-
tions), and libm17 (2,901 LoC, 45 functions). Beyond build and test         tion using the dependency graph, produces mixed results. For
success, which can give a false sense of correctness, we introduce          CircularBuffer and libm17, the agent successfully constructs the
two additional metrics: (i) Functional Coverage (%), defined as             project structure from scratch, achieving 100% functional coverage
the percentage of C functions fully translated into Rust (exclud-           and passing all tests. For libm17 specifically, this setting produces
ing stubs, unimplemented!() placeholders, and missing functions),           the most comprehensive test suite of any non-full mode, as the
and (ii) Test Coverage (%), defined as the percentage of original           agent autonomously generates C test vectors to cross-verify its Rust
C test cases translated into the Rust test suite and executable via         implementation. This demonstrates that the agent’s self-directed
cargo test. These metrics are intentionally stricter than build             context curation can compensate for the absence of a predefined
and test success alone, as our manual audit revealed multiple cases         scaffold when the project structure is straightforward. However,
where a project was built and tested successfully despite missing           LTRE exposes the limits of this compensation: without a predefined
functionality, shallow test coverage, or translated test harnesses          interface structure, the agent leaves four critical functions as stubs
that were never executed. Table 6 reports our results across all            or incomplete, including nfa_clone and nfa_uncomplement, re-
above settings.                                                             sulting in 82.2% functional coverage and only 12.2% test coverage.
                                                                            The absence of a scaffold forces the agent to spend significant effort
4.3.1 Impact of Removing All Components ( Base). The single-
                                                                            on project initialization and macro visibility issues, leaving less
shot base setting reveals the limitations of vanilla coding agents
                                                                            capacity for logic translation.
in translating an entire project without structural guidance. On
CircularBuffer, where the entire codebase fits within a single              4.3.3 Impact of Removing Function Mappings ( W/O Mapping).
context window, base achieves full functional coverage, compiles            Providing the dependency graph and Rust interfaces but omit-
successfully and passes all tests, demonstrating that a single-prompt       ting explicit C-to-Rust function mappings consistently improves
                                                                        9
functional coverage over base and w/o interfaces for complex                  Consequently, test quality determines the upper bound on the equiv-
programs. Although LTRE reaches 93.3% functional coverage in                  alence that can be established between the C and Rust versions.
this setting—the highest of any non-full mode—and uniquely im-                A natural extension would be to harness the capabilities of cod-
plements functions absent in both other ablation modes, such                  ing agents to generate additional test cases that expose divergent
as dfa_serialize and dfa_deserialize, ORBIT still skips some                  behaviors, which we leave as future work. Although ORBIT’s mod-
functions; when run in full mode with mapping, LTRE reaches                   ular design improves the performance of open-source models and
up to 100% functional coverage. The predefined interface scaf-                can provide a cost benefit, optimizing the agentic pipeline for cost
fold provides a stable target structure, allowing the agent to fo-            and token consumption presents a distinct set of challenges or-
cus on logic translation rather than architectural decisions. For             thogonal to the goals of this work and is therefore not our focus.
CircularBuffer and libm17, the setting achieves full functional               Additionally, while ORBIT operates with full agent autonomy, we
and test coverage.                                                            observed instances where the agent oscillated between pursuing
   The contrasting results between LTRE and libm17 across all ab-             safe Rust alternatives and completing functionality, continuing un-
lation modes reflect fundamental differences in their structural              til the attempt limit was exhausted. This highlights the need for
complexity rather than program size alone. LTRE, despite being                mechanisms to detect and resolve such agent loops early. Finally,
smaller (1,212 LoC) in size, is structurally more difficult for trans-        the non-deterministic nature of LLMs poses a threat to validity, as
lation because its core functionality is organized as a tightly cou-          repeated runs may produce different results. To mitigate this, we
pled automata pipeline. Correct behavior depends on interactions              adopt a strict correctness criterion: a translation is marked as Test
among parsing, NFA construction, DFA compilation, DFA mini-                   Success only if it passes all available test cases.
mization, matching, and round-trip operations such as serialization
and decompilation. As a result, defects in one stage often invalidate
downstream behavior, and local fixes do not necessarily recover
global correctness. In contrast, libm17 is larger (2,901 LoC) but             6    Related Work
more decomposable. Many of its components, such as CRC com-                   Rule-based C-to-Rust Translation. Early automated C-to-Rust
putation, callsign encoding, and several math helpers, have strong            translation relied primarily on rule-based transpilation. C2Rust [7]
local specifications and can be validated independently with direct           is the most widely used tool in this category, applying predefined
test vectors. This makes iterative function-level translation more            and custom rewrite rules to produce Rust code. While it scales
effective despite the larger codebase.                                        to large codebases, the output is unidiomatic and saturated with
                                                                              unsafe blocks. Emre et al. [11] systematically characterize the
4.3.4 Full Pipeline. The complete ORBIT pipeline achieves 100%                sources of unsafety in C2Rust translations and propose a compiler-
functional and test coverage on all three benchmarks. The one ex-             feedback-driven technique to refactor a class of raw pointers into
ception is LTRE’s test success, which fails not due to incomplete             safe Rust references. Building on C2Rust, CROWN [8] lifts raw
translation but due to the C-to-Rust semantic gap. To further under-          pointers to Rust references, though its scope is restricted to mutable,
stand the effectiveness of Function mapping beyond the mentioned              non-array pointer types. A parallel line of work targets narrower
metrics, we conducted a small controlled experiment: we directed              translation challenges: ConCrat [9] focuses on converting lock APIs,
a single coding agent to translate a single function (bitset_get)             while other tools [47, 48] address specific data type conversions.
from LTRE in isolation, once with explicit function mapping and               Collectively, these approaches demonstrate that rule-based transla-
once without. With mapping, the agent completed the translation in            tion can handle isolated syntactic patterns but struggles to produce
3 tool calls (two reads and one write). Without mapping, the agent            safe, idiomatic Rust at the whole-program level.
required 6 tool calls, of which 4 were codebase navigation steps to               LLM-based C-to-Rust Translation. Recent advances in large
locate the relevant C and Rust files. While this observation is based         language models (LLMs) have enabled their application across a
on a single function, it illustrates how function mappings eliminate          wide range of domains [49–57], including code generation and
navigation overhead that would otherwise compound across the                  program translation. Pan et al. [58] provide a comprehensive evalu-
hundreds of per-function translation steps in a full project.                 ation of LLM-based translation across multiple programming lan-
   Based on the above results, we conclude that each component of             guages, including C-to-Rust, and introduce a taxonomy of common
ORBIT contributes meaningfully to translation quality. The depen-             translation errors. To improve translation quality, several works
dency graph enables incremental translation that scales to complex            augment LLM-based approaches with program analysis for decom-
projects. Rust interfaces provide the structural scaffold that keeps          position [14, 17–19, 22, 59] and verification techniques such as
the agent focused on logic translation. Removing any single compo-            formal verification [15], fuzzing [13], and symbolic testing [16].
nent degrades either functional or test coverage. The base setting            Despite these advances, these approaches are typically evaluated
demonstrates that single-shot translation, while sufficient for small         on relatively small programs (e.g., under 600 LoC), limiting their
programs, is fundamentally inadequate for projects beyond a few               applicability to realistic codebases.
hundred lines of code.                                                            Agentic Approaches for Code Translation. In parallel, emerg-
                                                                              ing work explores the use of LLM-powered agents for translation
5   Threats to Validity                                                       and testing. However, these approaches are either restricted to CLI-
Like other LLM-based C-to-Rust translation approaches [21, 46],               based programs [44], focus primarily on refactoring C2Rust out-
ORBIT relies on the tests available with the source code to assess            puts [60], are limited to verification of the final translated code [61],
semantic equivalence between the source and translated programs.              or lack evaluation on diverse datasets [62].
                                                                         10
   In contrast, our work aims to address these gaps by providing                               [16] Yubo Bai and Tapti Palit. Rustassure: Differential symbolic testing for llm-
a fully autonomous agentic framework that is not restricted to                                      transpiled c-to-rust code. arXiv preprint arXiv:2510.07604, 2025.
                                                                                               [17] Vikram Nitin, Rahul Krishna, Luiz Lemos do Valle, and Baishakhi Ray.
specific classes of C applications. We exclude multi-threaded and                                   C2SaferRust: Transforming C projects into safer Rust with neurosymbolic tech-
GUI-based programs due to their inherent non-determinism and                                        niques. arXiv preprint arXiv:2501.14257, 2025.
                                                                                               [18] Manish Shetty, Naman Jain, Adwait Godbole, Sanjit A Seshia, and Koushik Sen.
the additional challenges they introduce for verification. We further                               Syzygy: Dual code-test C to (safe) Rust translation using LLMs and dynamic
evaluate our approach on a rigorous and diverse benchmark.                                          analysis. arXiv preprint arXiv:2412.14234, 2024.
                                                                                               [19] Momoko Shiraishi and Takahiro Shinagawa. Context-aware code segmenta-
                                                                                                    tion for C-to-Rust translation using large language models. arXiv preprint
7    Conclusion                                                                                     arXiv:2409.10506, 2024.
                                                                                               [20] Hanliang Zhang, Cristina David, Meng Wang, Brandon Paulsen, and Daniel
We presented ORBIT, an agentic framework for autonomous C-                                          Kroening. Scalable, validated code translation of entire projects using large
to-Rust translation that addresses key limitations of prior work,                                   language models. arXiv preprint arXiv:2412.08035, 2024.
including evaluation on small benchmarks and reliance on brittle                               [21] Momoko Shiraishi, Yinzhi Cao, and Takahiro Shinagawa. Smartc2rust: Iterative,
                                                                                                    feedback-driven c-to-rust translation via large language models for safety and
static analysis requiring human intervention. ORBIT decomposes                                      equivalence. arXiv preprint arXiv:2409.10506, 2024.
translation into coordinated stages with integrated verification                               [22] Chaofan Wang, Tingrui Yu, Chen Xie, Jie Wang, Dong Chen, Wenrui Zhang, Yul-
                                                                                                    ing Shi, Xiaodong Gu, and Beijun Shen. Evoc2rust: A skeleton-guided framework
to mitigate agent hallucination. ORBIT achieves 100% compilation                                    for project-level c-to-rust translation, 2025.
success and 91.7% test success, substantially outperforming C2Rust                             [23] Xuemeng Cai, Jiakun Liu, Xiping Huang, Yijun Yu, Haitao Wu, Chunmiao Li,
and the CRUST-Bench pipeline in correctness and memory safety.                                      Bo Wang, Imam Nur Bani Yusuf, and Lingxiao Jiang. Rustmap: Towards project-
                                                                                                    scale c-to-rust migration via program analysis and llm. In International Conference
Overall, our results suggest that agentic workflows are a promising                                 on Engineering of Complex Computer Systems, pages 283–302. Springer, 2025.
direction for applying LLMs to large-scale software modernization.                             [24] Yifei Gao, Chengpeng Wang, Pengxiang Huang, Xuwei Liu, Mingwei Zheng, and
                                                                                                    Xiangyu Zhang. Pr2: Peephole raw pointer rewriting with llms for translating c
                                                                                                    to safer rust. arXiv preprint arXiv:2505.04852, 2025.
8    Data Availability Statement                                                               [25] Jaemin Hong and Sukyoung Ryu. Type-migrating c-to-rust translation using a
                                                                                                    large language model. Empirical Software Engineering, 30(1):3, 2025.
Our source code and dataset are available at https://anonymous.                                [26] Ruishi Li, Bo Wang, Tianyu Li, Prateek Saxena, and Ashish Kundu. Translating
4open.science/r/orbit_c_rust_2026. The artifacts will be released                                   C to Rust: Lessons from a user study. arXiv preprint arXiv:2411.14174, 2024.
                                                                                               [27] Qingxiao Xu and Jeff Huang. Optimizing type migration for llm-based c-to-rust
publicly upon acceptance of the paper.                                                              translation: A data flow graph approach. In Proceedings of the 14th ACM SIGPLAN
                                                                                                    International Workshop on the State Of the Art in Program Analysis, page 8–14,
                                                                                                    New York, NY, USA, 2025. Association for Computing Machinery.
References                                                                                     [28] Romain Robbes, Théo Matricon, Thomas Degueule, Andre Hora, and Stefano
 [1] Gavin Thomas. A proactive approach to more secure code. Microsoft Security                     Zacchiroli. Agentic much? adoption of coding agents on github. arXiv preprint
     Response Center (MSRC) Blog, July 2019. Accessed: 2026-03-25.                                  arXiv:2601.18341, 2026.
 [2] Aleksandar Zeljic, Shaobo Taneja, and Aaron Tomb. Verify the safety of the Rust           [29] Hao Li, Haoxiang Zhang, and Ahmed E Hassan. The rise of ai teammates in
     standard library. AWS Open Source Blog, July 2022. Accessed: 2026-03-25.                       software engineering (se) 3.0: How autonomous coding agents are reshaping
 [3] Muhammad Hassnain and Caleb Stanford. Counterexamples in safe Rust. In                         software engineering. arXiv preprint arXiv:2507.15003, 2025.
     Proceedings of the 39th IEEE/ACM International Conference on Automated Software           [30] Zeerak Babar, Nafiz Imtiaz Khan, Muhammad Hassnain, and Vladimir Filkov.
     Engineering Workshops, pages 128–135, 2024.                                                    Open-source llms for technical q&a: Lessons from stackexchange. In Interna-
 [4] Muhammad Hassnain, Anirudh Basu, Ethan Ng, and Caleb Stanford. Cargo                           tional Conference on Software Engineering of Emerging Technology, pages 615–626.
     sherlock: An smt-based checker for software trust costs, 2026.                                 Springer, 2025.
 [5] Defense Advanced Research Projects Agency (DARPA). TRACTOR: Translating                   [31] Business Insider Staff. AI coding boom shifts software developers toward man-
     All C to Rust. https://www.darpa.mil/research/programs/translating-all-c-to-                   agement. Business Insider, March 2026. Accessed: 2026-03-25.
     rust, 2024. Accessed: 2026-03-20.                                                         [32] Anirudh Khatry, Robert Zhang, Jia Pan, Ziteng Wang, Qiaochu Chen, Greg
 [6] TRACTOR Program Developers. The great refactor: DARPA TRACTOR docu-                            Durrett, and Isil Dillig. Crust-bench: A comprehensive benchmark for c-to-safe-
     mentation and resources. https://www.thegreatrefactor.org/, 2024. Accessed:                    rust transpilation. arXiv preprint arXiv:2504.15254, 2025.
     2026-03-25.                                                                               [33] Tree-sitter. https://github.com/tree-sitter/tree-sitter, 2023. Accessed: March 14,
 [7] Immunant. C2Rust. https://github.com/immunant/c2rust, 2022. Accessed: [Insert                  2025.
     Date Here].                                                                               [34] Arthur B Kahn. Topological sorting of large networks. Communications of the
 [8] Hanliang Zhang, Cristina David, Yijun Yu, and Meng Wang. Ownership guided                      ACM, 5(11):558–562, 1962.
     C to Rust translation. In International Conference on Computer Aided Verification,        [35] Sirui Hong, Mingchen Zhuge, Jonathan Chen, et al. MetaGPT: Meta programming
     pages 459–482. Springer, 2023.                                                                 for a multi-agent collaborative framework. In International Conference on Learning
 [9] Jaemin Hong and Sukyoung Ryu. Concrat: An automatic C-to-Rust lock API                         Representations, 2024.
     translator for concurrent programs. In 2023 IEEE/ACM 45th International Confer-           [36] Dong Huang, Qingwen Bu, Jie M. Zhang, Michael Luck, and Heming Cui. Agent-
     ence on Software Engineering (ICSE), pages 716–728. IEEE, 2023.                                Coder: Multi-agent-based code generation with iterative testing and optimisation.
[10] Jaemin Hong and Sukyoung Ryu. To tag, or not to tag: Translating C’s unions to                 arXiv preprint arXiv:2312.13010, 2023.
     Rust’s tagged unions. In Proceedings of the 39th IEEE/ACM International Conference        [37] Chen Qian, Wei Liu, Hongzhang Liu, et al. ChatDev: Communicative agents for
     on Automated Software Engineering, pages 40–52, 2024.                                          software development. In Proceedings of the Annual Meeting of the Association
[11] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. Translating C                      for Computational Linguistics, 2024.
     to safer Rust. Proc. ACM Program. Lang., 5(OOPSLA), oct 2021.                             [38] Muhammad Farrukh, Smeet Shah, Baris Coskun, and Michalis Polychron-
[12] Zhen Yang, Fang Liu, Zhongxing Yu, Jacky Wai Keung, Jia Li, Shuo Liu, Yifan                    akis. Safetrans: Llm-assisted transpilation from c to rust. arXiv preprint
     Hong, Xiaoxue Ma, Zhi Jin, and Ge Li. Exploring and unleashing the power of                    arXiv:2505.10708, 2025.
     large language models in automated code translation. Proceedings of the ACM on            [39] Anomaly Co. Opencode: The open-source AI coding agent. https://opencode.ai/,
     Software Engineering, 1(FSE):1585–1608, 2024.                                                  2025. Accessed: 2026-03-23.
[13] Hasan Ferit Eniser, Hanliang Zhang, Cristina David, Meng Wang, Maria Chris-               [40] OpenAI. Codex: An AI coding partner. https://openai.com/codex/, 2021. Accessed:
     takis, Brandon Paulsen, Joey Dodds, and Daniel Kroening. Towards translat-                     2026-03-23.
     ing real-world code with LLMs: A study of translating to Rust. arXiv preprint             [41] Free Software Foundation. GNU C Compiler Extensions: Nested Functions. Free
     arXiv:2405.11514, 2024.                                                                        Software Foundation, 2024. Accessed: 2025.
[14] Vikram Nitin, Rahul Krishna, and Baishakhi Ray. Spectra: Enhancing the code               [42] OpenAI. Api pricing. https://developers.openai.com/api/docs/pricing, 2026.
     translation ability of language models by generating multi-modal specifications.               Accessed: 2026-03-18.
     arXiv preprint arXiv:2405.18574, 2024.                                                    [43] Amazon Web Services. Amazon bedrock pricing. https://aws.amazon.com/
[15] Aidan ZH Yang, Yoshiki Takashima, Brandon Paulsen, Josiah Dodds, and Daniel                    bedrock/pricing/, 2026. Accessed: 2026-03-18.
     Kroening. Vert: Verified equivalent Rust transpilation with large language models         [44] Tianyu Li, Ruishi Li, Bo Wang, Brandon Paulsen, Umang Mathur, and Prateek
     as few-shot learners. arXiv preprint arXiv:2404.18852, 2024.                                   Saxena. Adversarial agent collaboration for c to rust translation. arXiv preprint
                                                                                          11
     arXiv:2510.03879, 2025.                                                                        2025.
[45] DARPA TRACTOR Program. First TRACTOR Evaluation Report. Evaluation                        [54] Muhammad Talha, Jingchuan Shi, and Ahmed Qureshi. Extending the cognitive
     report, Defense Advanced Research Projects Agency (DARPA), 2024. Available                     domain of bloom’s taxonomy using machine learning. Research Square (Preprint),
     via the official TRACTOR Program GitHub repository.                                            2026.
[46] Tianyang Zhou, Haowen Lin, Somesh Jha, Mihai Christodorescu, Kirill Levchenko,            [55] Ranjan Sapkota, Shaina Raza, Maged Shoman, Achyut Paudel, and Manoj Karkee.
     and Varun Chandrasekaran. Llm-driven multi-step translation from c to rust                     Image, text, and speech data augmentation using multimodal LLMs for deep
     using static analysis. arXiv preprint arXiv:2503.12511, 2025.                                  learning: A survey. arXiv preprint arXiv:2501.18648, 2025.
[47] Jaemin Hong and Sukyoung Ryu. Don’t write, but return: Replacing output                   [56] Muhammad Muzammil, Abisheka Pitumpe, Xigao Li, Amir Rahmati, and Nick
     parameters with algebraic data types in C-to-Rust translation. Proceedings of the              Nikiforakis. The Poorest Man in Babylon: A Longitudinal Study of Cryptocur-
     ACM on Programming Languages, 8(PLDI):716–740, 2024.                                           rency Investment Scams. In Proceedings of The Web Conference (WWW), 2025.
[48] Jaemin Hong. Improving automatic C-to-Rust translation with static analysis. In           [57] Hamed Jelodar, Mohammad Meymani, and Roozbeh Razavi-Far. Large language
     Proceedings of the 45th IEEE/ACM International Conference on Software Engineering              models (LLMs) for source code analysis: applications, models and datasets. arXiv
     (ICSE), pages 273–277, 2023.                                                                   preprint arXiv:2503.17502, 2025.
[49] Rasha Ahmad Husein, Hala Aburajouh, and Cagatay Catal. Large language                     [58] Rangeet Pan, Ali Reza Ibrahimzada, Rahul Krishna, Divya Sankar, Lam-
     models for code completion: A systematic literature review. Computer Standards                 bert Pouguem Wassi, Michele Merler, Boris Sobolev, Raju Pavuluri, Saurabh
     & Interfaces, 92:103917, 2025.                                                                 Sinha, and Reyhaneh Jabbarvand. Lost in translation: A study of bugs introduced
[50] HanXiang Xu, ShenAo Wang, Ningke Li, Kailong Wang, Yanjie Zhao, Kai Chen,                      by large language models while translating code. In Proceedings of the IEEE/ACM
     Ting Yu, Yang Liu, and HaoYu Wang. Large language models for cyber security:                   46th International Conference on Software Engineering, pages 1–13, 2024.
     A systematic literature review. arXiv preprint arXiv:2405.04760, 2024.                    [59] Ali Reza Ibrahimzada, Kaiyao Ke, Mrigank Pawagi, Muhammad Salman Abid,
[51] Efe Bozkir, Süleyman Özdel, Ka Hei Carrie Lau, Mengdi Wang, Hong Gao, and                      Rangeet Pan, Saurabh Sinha, and Reyhaneh Jabbarvand. Alphatrans: A neuro-
     Enkelejda Kasneci. Embedding large language models into extended reality: Op-                  symbolic compositional approach for repository-level code translation and vali-
     portunities and challenges for inclusion, engagement, and privacy. In Proceedings              dation. Proceedings of the ACM on Software Engineering, 2(FSE):2454–2476, 2025.
     of the 6th ACM Conference on Conversational User Interfaces, pages 1–7, 2024.             [60] HoHyun Sim, Hyeonjoong Cho, Yeonghyeon Go, Zhoulai Fu, Ali Shokri, and
[52] Yoonsang Kim, Zainab Aamir, Mithilesh Singh, Saeed Boorboor, Klaus Mueller,                    Binoy Ravindran. Large language model-powered agent for c to rust code trans-
     and Arie E. Kaufman. Explainable XR: Understanding user behaviors of XR                        lation, 2025.
     environments using LLM-assisted analytics framework. IEEE Transactions on                 [61] Ali Reza Ibrahimzada, Brandon Paulsen, Reyhaneh Jabbarvand, Joey Dodds, and
     Visualization and Computer Graphics, 2025.                                                     Daniel Kroening. Matchfixagent: Language-agnostic autonomous repository-
[53] Muhammad Talha, Abdullah Mohiuddin, Sehrish Javed, and Ahmed Qureshi.                          level code translation validation and repair. arXiv preprint arXiv:2509.16187,
     Lowering barriers to cad adoption: A comparative study of augmented reality-                   2025.
     based cad (ar-cad) and a traditional cad tool. In International Design Engineering        [62] Chen Wang, Yujun Huang, Peng Li, Lina Gong, and Fei Wu. Rustify: Towards
     Technical Conferences and Computers and Information in Engineering Conference,                 repository-level c to safer rust via workflow-guided multi-agent transpiler.
     volume 89206, page V02AT02A018. American Society of Mechanical Engineers,




                                                                                          12
