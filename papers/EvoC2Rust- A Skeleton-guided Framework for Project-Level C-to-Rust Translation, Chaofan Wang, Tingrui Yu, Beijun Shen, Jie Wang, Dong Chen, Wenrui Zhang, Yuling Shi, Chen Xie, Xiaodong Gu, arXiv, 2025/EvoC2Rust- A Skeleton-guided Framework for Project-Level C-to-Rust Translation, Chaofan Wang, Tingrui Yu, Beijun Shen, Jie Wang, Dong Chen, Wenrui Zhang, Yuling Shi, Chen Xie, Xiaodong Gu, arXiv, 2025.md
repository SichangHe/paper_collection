                                              EvoC2Rust: A Skeleton-guided Framework for Project-Level
                                                                C-to-Rust Translation
                                                           Chaofan Wang                                                 Tingrui Yu                                    Beijun Shen∗
                                                  Shanghai Jiao Tong University                             Shanghai Jiao Tong University                   Shanghai Jiao Tong University
                                                        Shanghai, China                                           Shanghai, China                                 Shanghai, China
                                                     chaofwang@sjtu.edu.cn                                       hzfsls@sjtu.edu.cn                             bjshen@sjtu.edu.cn

                                                                Jie Wang                                                Dong Chen                                   Wenrui Zhang
                                                  Huawei Technologies Co., Ltd                              Huawei Technologies Co., Ltd                     Huawei Technologies Co., Ltd
                                                        Beijing, China                                            Beijing, China                                   Beijing, China
                                                   wangjie451@huawei.com                                     chendong108@huawei.com                          zhangwenrui8@huawei.com
arXiv:2508.04295v4 [cs.SE] 13 Jan 2026




                                                               Yuling Shi                                                Chen Xie                                    Xiaodong Gu
                                                  Shanghai Jiao Tong University                             Shanghai Jiao Tong University                   Shanghai Jiao Tong University
                                                        Shanghai, China                                           Shanghai, China                                 Shanghai, China
                                                     yuling.shi@sjtu.edu.cn                                    dindin_xc@sjtu.edu.cn                          xiaodong.gu@sjtu.edu.cn

                                         Abstract                                                                                CCS Concepts
                                         Translating legacy C codebases to Rust is increasingly demanded                         • Software and its engineering → Source code generation; •
                                         for building safety-critical systems. While various approaches have                     Computing methodologies → Machine translation.
                                         emerged for this task, they face inherent trade-offs: rule-based
                                         methods often struggle to satisfy code safety and idiomaticity re-                      Keywords
                                         quirements, while LLM-based methods frequently fail to generate                         C-to-Rust Translation, Complete Project Conversion, Skeleton Guided,
                                         semantically equivalent Rust code, due to the heavy dependencies                        Feature Mapping, Large Language Models
                                         of modules across the entire codebase. Recent studies have revealed
                                         that both solutions are limited to small-scale programs. In this paper,                 ACM Reference Format:
                                         we propose EvoC2Rust, an automated framework for converting                             Chaofan Wang, Tingrui Yu, Beijun Shen, Jie Wang, Dong Chen, Wen-
                                         complete C projects to equivalent Rust ones. EvoC2Rust employs                          rui Zhang, Yuling Shi, Chen Xie, and Xiaodong Gu. 2026. EvoC2Rust: A
                                         a skeleton-guided translation strategy for project-level translation.                   Skeleton-guided Framework for Project-Level C-to-Rust Translation. In 2026
                                                                                                                                 IEEE/ACM 48th International Conference on Software Engineering (ICSE-SEIP
                                         The pipeline consists of three stages: 1) it first decomposes the
                                                                                                                                 ’26), April 12–18, 2026, Rio de Janeiro, Brazil. ACM, New York, NY, USA,
                                         C project into functional modules, employs a feature-mapping-                           12 pages. https://doi.org/10.1145/3786583.3786856
                                         enhanced LLM to transform definitions and macros, and generates
                                         type-checked function stubs, which form a compilable Rust skele-
                                         ton; 2) it then incrementally translates functions, replacing the                       1    Introduction
                                         corresponding stub placeholders; 3) finally, it repairs compilation                     The translation of legacy C code to Rust is gaining significant at-
                                         errors by integrating LLM and static analysis. Through evolutionary                     tention in software engineering, spurred by critical memory safety
                                         augmentation, EvoC2Rust combines the advantages of both rule-                           concerns [7, 25]. Such vulnerabilities constitute the most preva-
                                         based and LLM-based solutions. Our evaluation on open-source                            lent category of critical security defects in production C systems,
                                         benchmarks and six industrial projects demonstrates the superior                        accounting for approximately 70% of high-severity vulnerabilities
                                         performance of EvoC2Rust in project-level C-to-Rust translation.                        in industry reports from Google and Microsoft [28]. This has ac-
                                         The results show that our approach outperforms the strongest LLM-                       celerated a paradigm shift toward compile-time safety guarantees
                                         based baseline by 17.24% in syntax accuracy and 14.32% in semantic                      through safe programming languages [33]. In response, Rust has
                                         accuracy, while also achieving a 43.59% higher code safety rate than                    emerged as a leading alternative that offers memory safety by en-
                                         the best rule-based tool.                                                               forcing a strict ownership and borrowing model [45].
                                                                                                                                    Recent work proposes rule-based tools [1, 15, 51], which convert
                                         ∗ Corresponding author.
                                                                                                                                 C code to Rust using primarily syntax-based transformations on
                                                                                                                                 a terse intermediate representation of compilation. Such transla-
                                                                                                                                 tion inherently generates non-idiomatic Rust code with low-level
                                                                                                                                 constructs and may also contain semantic inaccuracies. [35]. An-
                                                                                                                                 other line of work proposes LLM-based techniques [12, 26, 31, 48]
                                         This work is licensed under a Creative Commons Attribution 4.0 International License.   to utilize the code comprehension capability of code LLMs. Due to
                                         ICSE-SEIP ’26, Rio de Janeiro, Brazil                                                   the lack of parallel C-Rust training data and significant linguistic
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM ISBN 979-8-4007-2426-8/2026/04                                                      differences, these approaches often fail to produce semantically
                                         https://doi.org/10.1145/3786583.3786856                                                 equivalent Rust code [34].
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                              Wang et al.



                  Skeleton Construction                                                                        Post-Generation Repair
                                                                       Rust Compiler


                                     MetaData              MetaData
                   C Project                                          Rust Project
       C         Decomposition               Transformation            Assembly       Rust       Initial   Bracket Repair        LLM Refinement      Rust
     Project                                                                         Skeleton Rust Project                                          Project


                                         Module Translation
                      Macro                                                  Macro                                    Rule-based Repair
                     Definition                                             Definition

                     Function
                     Function                  Code Translation             Dummy
                     Signature                                              Function

                       Body
                                                                                           Filling
                                                                            Function
                                                                            Function
                                              Feature Mappings                                                            Rust Compiler

                   C Modules                                             Rust Modules


                                                              Figure 1: Overview of EvoC2Rust.


   While automated code translation has been extensively inves-                          and decomposes the project into functional modules, generating
tigated [9, 20, 36, 41, 49, 53], the translation of C-to-Rust projects                   a compilable Rust skeleton with placeholder functions. Next, it
poses special challenges:                                                                incrementally translates these stubs using LLMs augmented with
   Challenge-1: Substantial linguistic discrepancies for ensur-                          the predefined feature mappings. Finally, it combines LLMs with
ing safety. C and Rust differ fundamentally in their safety models.                      static analysis to iteratively repair compilation errors and refine the
C permits loose type checking, unrestricted pointer arithmetic,                          output. This evolutionary process effectively blends the strengths
and manual memory management, whereas Rust enforces strict                               of rule-based and learning-based approaches, striking a practical
compile-time type safety, ownership-based memory guarantees,                             balance between correctness and safety in automated C-to-Rust
and disciplined reference usage through its borrowing rules. Ex-                         migration.
isting rule-based translators often compromise safety by relying                            We evaluate EvoC2Rust using an open-source benchmark Vivo-
on raw pointers, unsafe blocks, or external C functions [35]. While                      Bench [42] and a self-collected dataset of six industrial projects. Ex-
LLM-based approaches can generate code with improved safety,                             perimental results demonstrate that EvoC2Rust significantly out-
they often lack sufficient context understanding (e.g., variable scope                   performs existing baselines in project-level C-to-Rust translation.
or pointer lifetimes), potentially leading to logical errors or memory                   In comparison with LLM-based approaches, EvoC2Rust improves
safety violations in the translated Rust code [40]. As a result, nei-                    the compilation pass rate by 17.24–50.84% and the line acceptance
ther rule-based nor LLM-based methods alone reliably meet Rust’s                         rate by 14.32–44.79%, while also achieving marginally better code
stringent safety requirements.                                                           safety. When compared to rule-based methods, EvoC2Rust attains
   Challenge-2: Project-level code dependence. Translating                               a 43.59–96.79% higher code safety rate, while maintaining competi-
complete C projects poses greater challenges than translating iso-                       tive performance in terms of compilation and line acceptance rates.
lated functions because the translated Rust project must preserve                        Furthermore, at the module level, EvoC2Rust achieves a 92.25%
cross-module dependencies and consistent project-level structure [37,                    compilation success rate and an 89.53% test pass rate on industrial
39]. Code LLMs often struggle with such large-scale context [50],                        projects.
leading to broken references, inconsistent APIs, or incorrect mod-                          The contributions of our work are summarized as follows:
ule boundaries [35, 43]. Consequently, existing approaches tend to                           • We propose a novel skeleton-guided framework that over-
perform well only on small-scale programs (e.g., ≤100 LoC) [11, 12],                           comes the barrier of inter-module dependencies to enable the
and fall short in real-world project settings.                                                 translation of complete C projects into Rust.
   In this work, we propose EvoC2Rust, an automated frame-                                   • We define safety-preserving mappings between core linguistic
work for translating complete C projects into equivalent Rust code.                            features of C and Rust to enhance LLMs’ safety awareness.
To address the linguistic gap and ensure safety (Challenges 1),                              • We evaluate EvoC2Rust on both open-source and industrial
EvoC2Rust enhances LLMs with safety-preserving mappings across                                 scenarios. Experimental results show that EvoC2Rust out-
seven core linguistic features, including types, macros, functions,                            performs existing baselines, effectively translating C projects
operators, syntax structures, globals, and variadic arguments. To en-                          to correct and safe Rust code.
able project-level translation (Challenge 2), EvoC2Rust introduces                          Our source code and experimental data are publicly available at
a skeleton-guided translation strategy that proceeds in three stages.                    https://github.com/bbzswcf/EvoC2rust.
First, it analyzes the input C project to extract high-level metadata
EvoC2Rust: A Skeleton-guided Framework for Project-Level C-to-Rust Translation                            ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil


                                                     Table 1: Type Mappings between C and Rust

 Type                      C Type        C Example                               Rust Type          Rust Example
 Array                     int[N]        int a[3] = {1, 2, 3}                    Array<i32, N>      let mut a: Array<i32,3> = arr![1,2,3]
 Pointer                   int *         int *a = &b                             Ptr<i32>           let mut a: Ptr<i32> = c_ref!(b)
 String                    char *        char *c = "Hello World!"                Ptr<u8>            let mut c=cstr!("Hello World!")
                                         typedef     int     (*MyFunc)                              pub type MyFunc=FuncPtr<fn(Ptr<Void>,
 Function Pointer          (*func)                                               FuncPtr
                                         (const void *, const void *)                               Ptr<Void>) -> i32>
 File                      FILE *        FILE *f = fopen(name, "rb")             FilePtr            let mut f=c_fopen!(name, cstr("rb"))
 Variadic Argument         va_list       va_start(arg_ptr, prev)                 VaList             (. . . , prev: . . . , arg_ptr: VaList)


2     Approach                                                                   errors, enabling a seamless and scalable translation process even
Figure 1 illustrates the architecture of EvoC2Rust. It contains three            for large-scale projects with complex interactions.
key steps: (1) Skeleton Construction decomposes the C project into
modules and constructs a Rust project skeleton to assemble the Rust
modules (Section 2.1); (2) Module Translation incrementally converts             2.2    Module Translation with Safety-preserving
definitions, macros, and functions using safety-preserving linguistic                   Mapping
mappings (Section 2.2); and (3) Post-Generation Repair combines                  EvoC2Rust employs an LLM to automatically translate C modules
LLM-based refinement with static analysis for code optimization                  into Rust constructs, converting definitions, macros, and function
(Section 2.3).                                                                   signatures to assemble the skeleton, and then transforming func-
                                                                                 tion bodies to populate the placeholder dummy functions within
                                                                                 the skeleton. To preserve safety and semantic alignment during
2.1     Project Skeleton Construction                                            translation, EvoC2Rust augments the LLM with a comprehensive
A straightforward idea of project-level code translation is to trans-            set of linguistic mappings across seven key categories:
late each function individually and assemble them into a project.                    1) Type Mapping. Each C type is associated with a semantically
However, naively aggregating translated functions often leads to                 consistent Rust counterpart, as summarized in Table 1. For example,
cascading interdependency errors. To address this, EvoC2Rust em-                 to represent C-style strings, we introduce a cstr!() macro in Rust
ploys a skeleton-guided translation strategy, which first constructs             that guarantees null termination, thereby avoiding inconsistencies
a compilable Rust project skeleton based on project metadata and                 in downstream operations such as encryption and compression.
then incrementally populates it with translated function implemen-               Beyond simple type correspondences, we also capture the oper-
tations.                                                                         ational semantics of C types. Since C pointers permit arithmetic
    Given a C project, EvoC2Rust first parses the source code us-                (e.g., addition, subtraction), the address-of operator, and array-style
ing Tree-sitter [3] to extract key syntactic elements and abstract               subscripting, we implement equivalent traits in Rust to mirror these
them into a unified project metadata representation. This meta-                  behaviors. Likewise, to model the implicit decay of C arrays into
data captures structural information including filenames, include                pointers, we provide an explicit cast() method. Together, these
statements, macro definitions, type declarations, global identifiers,            mappings reduce the complexity of translating raw C pointers by
function signatures, and a mapping table between identifier decla-               supplying direct Rust equivalents for a wide range of pointer classes
rations to source files. They are then systematically transformed                and operations.
into Rust equivalents via rule-based conversion. For instance, C                     2) Type Conversion. We introduce a custom CastIntoTyped trait
include dependencies are transformed to Rust use imports, and                    to handle type conversions in Rust, supporting both integer-to-
identifier declarations are converted into Rust pub use statements               integer and pointer-to-pointer conversions. For safety, pointer-to-
(e.g., pub use {Rust_filename}::{identifier_name}) using the                     integer casts are allowed, but integer-to-pointer casts are strictly
declaration-to-file table.                                                       disallowed. For instance, the C expression ‘a = (uint16_t) b’ is
    Using the converted metadata, EvoC2Rust constructs a Rust                    translated as ‘a = b.cast::<u16>()’, and ‘pi = (int*)pu’ be-
project skeleton—comprising Rust constructs automatically trans-                 comes ‘pi = pu.cast::<Ptr<i32>>()’. To simulate C’s implicit
lated from C definitions, macros, and function signatures—that accu-             conversion semantics in Rust’s type-inferred context, we also pro-
rately preserves the structural organization of the original C project.          vide a typeless cast() method. This proves particularly effective
Each C function is assigned a type-checked dummy counterpart                     during the repair phase, where it substantially increases the success
in Rust using its translated signature and the unimplemented!()                  rate of LLM-driven optimization by efficiently resolving type errors
macro. These placeholders serve as safe stand-ins, allowing the                  stemming from implicit conversions in the original C code.
project to compile successfully even before the actual function                      3) Macro/Function Mapping. We provide Rust counterparts for
bodies are translated.                                                           native C macros such as NULL and LINE, as well as for common C
    The skeleton provides a stable framework that allows function                library functions including malloc, free, and memcpy. These im-
bodies to be translated and integrated incrementally. This ensures               plementations prioritize safe abstractions over direct invocations
each addition is contextually correct and free from dependency                   of unsafe primitives. For example, rather than relying on the unsafe
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                Wang et al.


       Table 2: An Example of Transformation Patterns                    model the VaList type in Rust as a Slice of references to values
                                                                         implementing the Display trait. To support formatting operations,
   Pattern Name:                                                         we provide a va_format!() macro, which in turn enables Rust
     Variadic Argument Mapping                                           implementations of variadic C functions such as snprintf.
                                                                            These feature mappings are formulated as transformation pat-
   Motivation:                                                           terns, each specifying the motivation, consequence, solution, and
     Rust does not support C-style variadic functions (e.g., va_list).   corresponding code examples, as illustrated in Table 2. By distilling
                                                                         expertise from senior practitioners, these patterns encode tacit pro-
   Consequence:                                                          fessional knowledge into explicitly reusable C-to-Rust migration
     Current LLMs cannot directly translate C’s variadic features.       guidelines.
                                                                            To steer the LLM toward accurate and idiomatic translations,
   Solution:                                                             we retrieve the most relevant patterns based on the input C code.
      Define a VaList type and va_format! macro:                         Specifically, we encode both the code snippet and pattern examples
      pub type VaList<’a> = &’a [&’a dyn Display];
                                                                         into dense vectors, compute cosine similarity, and select the top-K
      macro_rules! va_format { . . . }
                                                                         matching patterns. These retrieved patterns are then injected into
   Example:                                                              the LLM prompt using the following structured template.
   C Code:                                                                     Prompt Template for Translating C Modules to Rust
     int snprintf(char *str, size_t size, const char *format, . . . )
     { ... }                                                                   Translate the C [macro/definition/function] to Rust.
   Rust Code:                                                                  Patterns: {retrieved transformation patterns}
     pub fn snprintf(mut buf: Ptr<u8>, size: usize, format: Ptr<u8>,
      va: VaList) -> i32 {                                                     Demonstrations: {paired C-to-Rust examples}
        let mut fmt = format.to_string(); . . .                                C Source Code: {input source code}
        return length; }

                                                                         2.3     Post-Generation Repair
std::ptr::copy to implement memmove, we employ a safer alter-            Finally, EvoC2Rust refines the translated Rust code through a
native. By explicitly incorporating these mappings into the prompt,      compilation-driven, cascading repair process that combines syntac-
we guide the LLM to apply them consistently, enabling systematic         tic rules with LLM-based correction. For each problematic snippet,
translations such as converting the C function name() into the Rust      it generates multiple repair candidates based on compiler feed-
macro c_name!().                                                         back, retaining only those that reduce error counts until no further
   4) Syntax Structure Mapping. Certain C control flow constructs        improvements are possible.
lack direct semantic equivalents in Rust, posing a risk of logical          While rule-based techniques efficiently resolve trivial and well-
errors if translated literally. Specifically, Rust’s for loop operates   defined errors, LLMs excel at addressing complex semantic issues.
differently from C’s, C’s do while has no native counterpart, and        A hybrid strategy—applying rules first, followed by LLM refine-
switch statements are not fully aligned with Rust’s match. To en-        ment—yields the best results. We observe, however, that persistent
sure semantic fidelity, we implement dedicated macros—c_for,             low-level syntax errors such as bracket mismatches significantly
c_do, and c_switch—that replicate the exact behavior of their C          impede both repair methods, particularly rule-based correction. To
counterparts. These are introduced to the LLM via targeted prompts,      mitigate this, our approach prioritizes bracket repair before other
ensuring the original syntax is replaced with the appropriate macro      fixes, ensuring that basic syntax errors are resolved prior to se-
calls.                                                                   mantic analysis. This allows the Rust compiler to provide clearer
   5) Operator Mapping. We provide Rust equivalents for C-specific       diagnostic information for subsequent repair stages.
operators such as ++, --, &, and sizeof. The sizeof operator is             Specifically, EvoC2Rust implements a three-step repair chain:
mapped to two distinct macros: c_sizeof!() and c_sizeofval!().              1) Bracket Repair: An LLM analyzes compiler outputs and error
The increment and decrement operators (++, --) are implemented           messages to correct mismatched brackets and similar syntax issues.
as four generic functions to handle both prefix and postfix forms        The prompt includes instructions, exemplar fault-correction pairs,
for all integer and pointer types. Notably, the address-of operator &    the erroneous Rust snippet, and corresponding compilation errors.
is not translated to Rust’s reference operators (& or &mut), but to a          Prompt Template for Bracket Repair
dedicated c_ref!() macro that correctly obtains a pointer to the               Fix the compilation bugs in the following Rust code with the pro-
value.                                                                         vided compilation error messages, possibly because of mismatched
   6) Global Variable Mapping. Because mutable global variables                parentheses. Only correct lines that have unmatched parentheses
(static mut) are inherently unsafe in Rust, we introduce a Global<T>           bugs; do not modify any other code.
wrapper type to manage them safely. This wrapper employs an                    Demonstrations: {example pairs of incorrect/correct Rust code}
internal Mutex to ensure thread safety, thereby avoiding the need              Rust Source Code: {input source code}
                                                                               Compilation Error Messages: {input error messages}
for unsafe code blocks. To further simplify usage, we provide a
global!() macro that supports lazy initialization of global vari-           2) Rule-Based Repair: We define a set of syntax repair rules as
ables.                                                                   regex-based transformation patterns to address common syntax-
   7) Variadic Argument Mapping. Since variadic arguments in C           level issues. These include adjusting misplaced derive macros,
are most commonly used for logging and string formatting, we             removing redundant cast() operations, and resolving problematic
EvoC2Rust: A Skeleton-guided Framework for Project-Level C-to-Rust Translation                              ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil


                                                             Table 3: Statistics of the Datasets

                Dataset           Projects        Files      LoC        Functions    Macros (Functions)       Definitions         Test Cases
                Vivo-Bench        19 projects      38       80∼917         200               29                   95                 113
                                  avl               9         836           29               29                    9                 121
                                  bzp              18        2258           92               82                   14                  17
                                  md5               2         324           8                20                    1                  37
                C2R-Bench         sha256            2         280           9                11                    2                  12
                                  rapidlz           7         748           28               38                   10                  12
                                  cmptlz           25        3724          122              166                   27                  23
                                  Total            63        8170          288              346                   63                 222


array access patterns such as s[s.i], which can cause simultaneous                     • C2SaferRust [30]: a hybrid technique built on C2Rust, aug-
mutable and immutable borrow conflicts.                                                  mented with LLM-based post-processing and test-driven opti-
   3) LLM Refinement: In the final step, the LLM addresses residual                      mization to enhance the safety and idiomaticity of the trans-
semantic discrepancies and intricate compilation errors, such as                         lated Rust code. We follow the original configuration and use
type inconsistencies, unidiomatic usage, or structural mismatches.                       5 optimization iterations.
The prompt incorporates guidelines, fault-correction examples,                         • Self-Repair [23]: a multi-agent self-repair framework for
the erroneous Rust translation, and relevant compilation feedback.                       project-level C-to-Rust translation. It incrementally performs
These exemplar pairs, which are manually crafted by Rust experts                         file translation and uses iterative compilation and testing feed-
and refined through iterative experimentation, cover common re-                          back to correct errors automatically. We adopt the default
curring errors to enable the LLM to generalize effective correction                      setting of 3 self-repair rounds per task.
strategies (see our repository for detailed examples).                                 • Tymcrat [19]: a project-level translation method that im-
                                                                                         proves translation quality through type migration. It gen-
      Prompt Template for LLM Refinement                                                 erates multiple candidate Rust signatures and refines them
      Fix the compilation bugs in the following Rust code according to                   iteratively using compiler feedback. We use the default config-
      the compilation information.                                                       uration, which generates 4 candidate signatures per function.
      Instruction: {refinement guidelines}
                                                                                       • Direct Prompting: a baseline that applies zero-shot LLM
      Demonstrations: {example pairs of incorrect/correct Rust code}
                                                                                         prompting for direct C-to-Rust translation. To address its
      Rust Source Code: {input source code}
      Compilation Information: {input compilation feedback}                              limitations in preserving project-wide consistency and resolv-
                                                                                         ing dependencies, we integrate it within our project skeleton
                                                                                         framework.
3     Experimental Setup
We conduct experiments to evaluate the effectiveness of EvoC2Rust,                  3.2    Datasets
aiming to answer the following research questions.
                                                                                    We evaluate EvoC2Rust using two benchmarks: the open-source
    • RQ1: How effectively does our method translate complete C                     Vivo-Bench [42], and our newly introduced C2R-Bench, which
      projects to equivalent safe Rust code?                                        comprises six industrial projects.
    • RQ2: What is the module conversion accuracy achieved by                           Vivo-Bench is a collection of 19 algorithmic C projects from
      our method?                                                                   the 2025 Vivo C-to-Rust Innovation Competition, each containing
    • RQ3: To what extent do key components contribute to the                       1–3 files (33–630 LoC per file). Two senior engineers produced
      overall performance of our method?                                            the reference Rust translations with LLM assistance. Subsequently,
    • RQ4: How does our method scale to large projects in terms                     they validated the translations by adding tests to achieve complete
      of accuracy, safety, and efficiency?                                          function coverage, resulting in a total of 113 top-level test cases.
                                                                                        To assess translation performance in industrial settings, we con-
                                                                                    structed C2R-Bench using six production projects from Huawei’s
3.1     Comparison Methods
                                                                                    software ecosystem. These are single-threaded user-space appli-
We compare EvoC2Rust against three categories of C-to-Rust trans-                   cations using only standard C libraries, characterized by complex
lation methods: rule-based (C2Rust), LLM-based (Self-Repair and                     multi-file architectures (280–3,724 LoC per file) and extensive cross-
Tymcrat), and hybrid techniques (C2SaferRust). We also incorpo-                     file dependencies. Three senior engineers produced the reference
rate a direct LLM prompting baseline that translates code without                   Rust implementations via LLM-assisted translation, which were
repository context. Specifically, the baseline methods evaluated in                 validated using 222 top-level test cases.
our study are as follows:                                                               Each project in both Vivo-Bench [42] and C2R-Bench provides
    • C2Rust [1]: a rule-based C-to-Rust translator that converts                   four artifacts: the original C source code, C test cases, the refer-
      C code to Rust via AST analysis and manually defined trans-                   ence Rust translation, and corresponding Rust test cases. Table 3
      formation rules.                                                              summarizes the dataset statistics.
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                             Wang et al.


3.3     Evaluation Strategy and Metrics                                   outperforms all baseline methods across both datasets, achieving
Our evaluation assesses C-to-Rust translation performance at two          the highest overall performance in terms of compilation success,
granularities: project-level and module-level, each employing a           line acceptance, and code safety.
tailored strategy and specific metrics.                                      EvoC2Rust demonstrates a significant advantage in generat-
   Project-level Evaluation. We benchmark the translation of              ing memory-safe Rust code compared to rule-based and hybrid
complete software projects under realistic conditions, where ref-         baselines. Although C2Rust and C2SaferRust achieve near-perfect
erence implementations are unavailable. This strategy employs             compilation pass rates (e.g., 100% on Vivo-Bench), their safety per-
incremental compilation: we construct a skeleton with placeholder         formance is considerably lower. C2Rust exhibits code safety rates of
modules and iteratively replace them with translated code, revert-        only 0% and 1.83% on the two datasets, while C2SaferRust, despite
ing any modules that cause compilation failures. We employ three          LLM-enhanced optimization, reaches merely 60% and 48.24%. This
metrics to quantify project-level performance:                            confirms that syntactic translation, even with LLM post-processing,
                                                                          fails to reliably meet Rust’s safety requirements. In contrast, our
    • Incremental Compilation Pass Rate (ICompRate): The
                                                                          method proactively prevents unsafe code by leveraging safety-
      proportion of translated modules that compile successfully
                                                                          guaranteed feature mappings.
      when integrated step-wise into the project skeleton, measur-
                                                                             Among LLM-based approaches, EvoC2Rust demonstrates con-
      ing syntactic correctness [39].
                                                                          sistent superiority. On Vivo-Bench, it surpasses all baselines by
    • Line Acceptance Rate (AccRate) [54]: This metric evaluates
                                                                          12.65% to 64.51% in compilation success and 7.57% to 46.30% in
      the fidelity of the initial translation by comparing it to the
                                                                          line acceptance using DeepSeek-V3, while maintaining a 98% code
      manually corrected version. Precision captures the percentage
                                                                          safety rate. The performance gap widens on the complex C2R-
      of correct lines in the initial output, while Recall measures
                                                                          Bench, where it achieves 93.84% compilation success (21.82%-44.63%
      their preservation in the final code.
                                                                          higher than baselines) and over 97% line acceptance. This trend
    • Code Safety Rate (SafeRate) [27]: The proportion of gen-
                                                                          is also observed with the Qwen3-32B model, highlighting the ef-
      erated Rust code that is memory-safe, i.e., free of unsafe
                                                                          fectiveness of our skeleton-guided, feature mapping-augmented
      functions or blocks.
                                                                          translation paradigm.
   Module-level Evaluation. For a finer-grained analysis, we as-             Specifically, EvoC2Rust improves compilation success by 44.63%
sess translation accuracy at the module level using a fill-in-the-        and line acceptance by 54.38% over Self-Repair on C2R-Bench with
blank strategy. Given a C module and its reference Rust implemen-         DeepSeek-V3 (42.95%/55.66% with Qwen3-32B). Self-Repair’s file-
tation, we remove the latter, translate the C module, and insert the      level processing often exceeds LLM context limits, leading to code
result into the project to check compilation and test outcomes. Two       truncation. Compared to Tymcrat, EvoC2Rust achieves a 21.82%
metrics are used for this assessment:                                     higher compilation rate on C2R-Bench with DeepSeek-V3 (11.79%
    • Fill-in Compilation Pass Rate (FCompRate): The per-                 with Qwen3-32B). While Tymcrat employs diverse signature gen-
      centage of generated modules that compile correctly upon            eration and context enrichment to reduce initial errors, its lack
      integration.                                                        of expert-derived structured translation guidance ultimately con-
    • Test Pass Rate (TestRate) [23]: The percentage of generated         strains its effectiveness in complex scenarios. Direct Prompting
      modules that pass all associated unit tests.                        performs poorest, with a 38.42% average compilation success and
                                                                          low line acceptance (39.13% precision, 40.64% recall). This is pri-
3.4     Implementation Details                                            marily due to the inherent linguistic gaps between C and Rust.
We implement EvoC2Rust using DeepSeek-V3 [8] and Qwen3-                         Answer to RQ1. EvoC2Rust surpasses all baseline meth-
32B [4] as the foundation models. Translation tasks use greedy                  ods in project-level C-to-Rust translation, demonstrating the
decoding with max_tokens set to 4096. We leverage Tree-sitter                   highest overall performance across compilation success, line
v0.22.3 [3] for C code parsing, the standard rustc [2] for compi-               acceptance, and code safety on both open-source and indus-
lation, and the BGE-M3 model [32] to generate embeddings and                    trial benchmarks.
retrieve the top-10 most relevant patterns based on cosine similar-
ity. Iteration limits are enforced to ensure practicality: 5 rounds for
                                                                          4.2     Module Translation (RQ2)
bracket repair and 3 rounds for LLM refinement.
   We established verified ground-truth implementations to eval-          We further evaluate the module translation accuracy of EvoC2Rust,
uate the line acceptance rate metric. For each project, we first          which serves as its core technical component. As shown in Table 5,
translated the code using the target methods. The resulting Rust ar-      EvoC2Rust exhibits strong performance at the module level. Using
tifacts were then iteratively compiled and tested. Any compilation        DeepSeek-V3, it achieves 100% compilation and 99.07% test pass
or test failures were manually repaired by three senior engineers         rates on Vivo-Bench, while maintaining robust results on C2R-
with assistance from Claude Sonnet 4 [5] until all tests passed.          Bench (92.25% compilation, 89.53% test pass). Even with the smaller
                                                                          Qwen3-32B model which has 20× fewer parameters, EvoC2Rust
4 Results and Analysis                                                    still delivers competitive performance (80.63% compilation, 77.91%
                                                                          test pass), demonstrating its model-agnostic applicability.
4.1 Main Results (RQ1)                                                        A notable observation is the strong correlation between test
EvoC2Rust demonstrates superior performance in project-level              pass rates and compilation success: modules that compile correctly
C-to-Rust translation, as summarized in Table 4. It consistently          generally also pass functional tests. This consistency results from
EvoC2Rust: A Skeleton-guided Framework for Project-Level C-to-Rust Translation                                       ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil


                          Table 4: Performance of Various Methods in Translating Complete C Projects to Rust

                                                                                                            AccRate
                   Dataset                 Method                           ICompRate                                                     SafeRate
                                                                                                     Precision      Recall
                                           Rule-based and Hybrid Tools
                                           C2Rust [1]                   100                              100              100             0
                                           C2SaferRust [30]             100                              100              100             60.00
                                           LLM-based Methods (DeepSeek-V3)
                                           Self-Repair [23]            84.21                            92.08            89.24            87.60
                                           Tymcrat [19]                87.35                            92.11            92.44            97.88
                   Vivo-Bench              Direct Prompting            35.49                            55.15            51.95            77.09
                                           EvoC2Rust (Ours)             100                             99.83            99.86            98.00
                                           LLM-based Methods (Qwen3-32B)
                                           Self-Repair [23]            52.63                            33.12            38.36            77.57
                                           Tymcrat [19]                81.76                            76.82            74.47            87.11
                                           Direct Prompting            26.23                            21.72            27.51            89.81
                                           EvoC2Rust (Ours)            87.65                            87.92            83.45            98.22
                                           Rule-based and Hybrid Tools
                                           C2Rust [1]                  99.28                            98.99            98.98            1.83
                                           C2SaferRust [30]            99.28                            97.47            97.68            48.24
                                           LLM-based Methods (DeepSeek-V3)
                                           Self-Repair [23]            49.21                            72.35            13.79            83.92
                                           Tymcrat [19]                72.02                            77.82            74.94            95.92
                   C2R-Bench               Direct Prompting            56.67                            55.65            52.70            82.43
                                           EvoC2Rust (Ours)            93.84                            97.56            97.34            97.41
                                           LLM-based Methods (Qwen3-32B)
                                           Self-Repair [23]            39.40                            45.38            10.65            87.15
                                           Tymcrat [19]                70.56                            66.72            65.91            82.75
                                           Direct Prompting            35.29                            24.01            30.41            93.63
                                           EvoC2Rust (Ours)            82.35                            85.75            82.59            97.40
               * Bold and underline denote the best and second-best results, respectively.


our method’s dual mechanisms. Feature mapping prevents semantic                              repair, rule-based repair, and LLM refinement. Each variant is eval-
errors, and compiler-guided repair maintains logically sound error                           uated on C2R-Bench benchmark using the DeepSeek-V3 model. In
correction.                                                                                  our cascaded repair chain, later repairs depend on the output of ear-
   Our analysis confirms that project complexity significantly im-                           lier steps. Removing an early component while keeping later ones
pacts translation quality. Complex projects with intricate control                           would thus propagate unresolved errors, preventing compilation or
flows and data dependencies consistently challenge LLM compre-                               testing and invalidating the assessment of downstream components.
hension capabilities. For instance, the cmptlz project, featuring                            To avoid this issue and ensure a meaningful evaluation, we remove
complex macros and dependencies, achieves test pass rates of 86.35%                          components in reverse order, beginning with the final step (LLM
and 70.79% across models. In contrast, the simpler sha256 project                            refinement).
attains optimal 100% pass rates.                                                                As illustrated in Table 6, every component in EvoC2Rust con-
                                                                                             tributes critically to its overall effectiveness. Among them, the
                                                                                             feature mapping mechanism is the most impactful component. By
      Answer to RQ2. Our method demonstrates robust perfor-
                                                                                             ablating this mechanism, both ICompRate and FCompRate drop
      mance in module-level translation, achieving 92.25%–100%
                                                                                             sharply from 74.29% to 56.67% and from 81.06% to 33%, respec-
      compilation success and 77.91%–99.07% test pass rates across
                                                                                             tively. The impact on semantic correctness is also substantial, with
      model scales, confirming its effectiveness in handling projects
                                                                                             TestRate decreasing from 79.91% to 30.27%. This result highlights
      of varying complexity.
                                                                                             the mechanism’s essential role in bridging C and Rust constructs
                                                                                             through predefined transformation patterns that map C idioms to
                                                                                             safe Rust equivalents where direct counterparts are absent.
4.3     Ablation Study (RQ3)                                                                    The cascading repair chain also facilitates C-to-Rust translation.
To assess the contribution of each component in EvoC2Rust and                                Removing all three repairs (-w/o repair#1-3) results in considerable
validate our design choices, we perform an ablation study by incre-                          performance degradation, with ICompRate dropping by 19.55%,
mentally removing its key components: feature mapping, bracket                               FCompRate by 11.19%, and TestRate by 9.62%. Within this chain,
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                Wang et al.


Table 5: Effectiveness of EvoC2Rust in Module-Level C-to-                      By integrating results from all evaluated datasets (i.e., Vivo-
Rust Translation                                                            Bench, C2R-Bench, and RepoTransBench), we further analyze trans-
                                                                            lation performance across different project scales.
   Dataset                Project       FCompRate           TestRate           Translation Accuracy vs. Project Scale. As shown in Figure 2,
                                 DeepSeek-V3                                compilation success (ICompRate) exhibits a clear negative corre-
   Vivo-Bench             19 projects       99.07              98.50        lation with project size. While the rate declines gradually from
                          avl              100.00             92.53         100% for small projects (≤500 LoC) to approximately 69% for large
                          bzp               95.21             92.55         projects (>10,000 LoC), it does not collapse. This robustness to
                          md5               96.55             86.21         scaling is due to our skeleton-guided approach, which effectively
   C2R-Bench              sha256           100.00             100.00        manages complex inter-module dependencies.
                          rapidlz           96.05             92.11            Translation Safety vs. Project Scale. The SafeRate remains
                          cmptlz            86.98             86.35         consistently high (around 97%) across all project sizes, and even
                          Subtotal          92.25             89.53         exhibits a slight improvement in larger projects. We attribute this
                                                                            stability to our safety-guaranteed feature mappings, which encap-
                                  Qwen3-32B
                                                                            sulate low-level operations into a relatively fixed set of unsafe code
   Vivo-Bench             19 projects       87.65             84.57
                                                                            blocks. As project size increases, the proportion of such unsafe
                          avl               97.01             82.09         code naturally decreases, resulting in the observed improvement in
                          bzp               89.36             88.83         SafeRate.
                          md5               89.66             89.21            Translation Efficiency vs. Project Scale. Figure 3 presents
   C2R-Bench              sha256            90.91             90.91         the translation efficiency, quantified as seconds per line of code
                          rapidlz           78.95             77.63         (Sec/LoC), across projects of varying scales. The per-line translation
                          cmptlz            70.79             68.89         time ranges from approximately 0.35 to 0.85 seconds, averaging
                          Subtotal          80.63             77.91         0.63 seconds. Notably, for projects exceeding 5,000 LoC, efficiency
                                                                            stabilizes at approximately 0.55 Sec/LoC, demonstrating strong
                                                                            scalability of our method. These performance fluctuations show
                                                                            no correlation with code length and are instead determined by
rule-based repair (repair#2) contributes most significantly, raising
                                                                            project-specific characteristics. The primary factor influencing this
the compilation pass rate by 9.68% and the test pass rate by 4.45%
                                                                            variation is the number of LLM refinement iterations required,
on average. LLM refinement (repair#3) further enhances syntactic
                                                                            which depends directly on the inherent complexity of the code in
correctness by 4.27% and semantic correctness by 8.98%, without
                                                                            each project.
compromising code safety.
    Code safety remains consistently high (around 97%) across nearly
                                                                                  Answer to RQ4. Our method exhibits strong scalability
all ablation settings. This stability is attributable to the feature map-
                                                                                  on large-scale projects, maintaining resilient compilation
ping mechanism’s encapsulation of low-level operations within
                                                                                  rates, high safety guarantees, and stable efficiency without
verified safe constructs. Only when both feature mapping and re-
                                                                                  performance collapse.
pairs are disabled does safety drop sharply to 82.43%, demonstrating
the necessity of our integrated design.
                                                                            4.5     Case Study
      Answer to RQ3. Each component in EvoC2Rust plays a
      crucial role in its overall performance. The feature mapping          We present a case study on the rb_tree_rotate function, a core
      mechanism provides a safe and reliable basis by bridging              operation in a red-black tree implementation, to illustrate the effec-
      C-to-Rust semantic gaps, while the cascading repair chain             tiveness of EvoC2Rust (Figure 4). This function involves intricate
      fixes remaining errors to maximize syntactic and semantic             pointer manipulation, characteristic of low-level C code that is dif-
      correctness.                                                          ficult to translate into safe, idiomatic Rust. Its complexity exposes
                                                                            common limitations of existing translation approaches.
                                                                               As shown in Figure 4, baseline methods exhibit critical failures.
4.4     Scalability on Larger Projects (RQ4)                                Direct Prompting produces a project-level interface mismatch by
To evaluate the scalability and performance of our method on large-         passing a raw pointer (*mut) where a mutable reference (&mut)
 scale codebases, we conduct experiments on 10 larger projects (9,973       is required, revealing a lack of project-wide context awareness.
- 91,588 LoC) from RepoTransBench [44], a benchmark derived from            Moreover, its heavy use of raw pointers necessitates unsafe blocks,
 highly-starred GitHub repositories. During module translation, we          contradicting Rust’s memory safety goals. Self-Repair attempts a
 exclude functions that depend on third-party libraries, as our cur-        more idiomatic translation using Box<T>, but introduces a function-
 rent implementation primarily supports dependencies on the ISO             level ownership error (use of moved value), demonstrating the
 C standard library. Using DeepSeek-V3 as the backbone model,               difficulty of refactoring C-style memory management into safe Rust
 EvoC2Rust achieves acceptable performance, with an ICompRate               idioms without safety-guaranteed feature mappings.
 of 75.61% and a SafeRate of 96.20%. We do not report line acceptance          In contrast, EvoC2Rust generates a correct and safe translation.
 rates due to the prohibitive cost of manually creating verified Rust       This is achieved through our feature mapping mechanism, which
 references for projects at this scale.                                     employs a unified Ptr<T> smart pointer to preserve C-like pointer
EvoC2Rust: A Skeleton-guided Framework for Project-Level C-to-Rust Translation                                                    ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil


                                                       Table 6: Ablation Results on Key Components of EvoC2Rust

                                                                                               Project Translation                       Module Translation
                Variant
                                                                                  ICompRate                  SafeRate            FCompRate                    TestRate
                EvoC2Rust (Ours)                                                      93.84                    97.41                 92.25                      89.53
                -w/o Repair#3                                                     89.57 ( -4.27)           97.40 ( -0.01)        87.23 ( -5.02)             85.37 ( -4.16)
                -w/o Repair#2-3                                                   75.24 (-18.60)           97.46 ( +0.05)        82.21 (-10.04)             80.92 ( -8.61)
                -w/o Repair#1-3                                                   74.29 (-19.55)           97.21 ( -0.20)        81.06 (-11.19)             79.91 ( -9.62)
                -w/o Feature Mapping and Repair#1-3                               56.67 (-37.17)           82.43 (-14.98)        33.00 (-59.25)             30.27 (-59.26)
        * Repair#1: bracket repair; Repair#2: rule-based repair; Repair#3: LLM refinement.


                         100                                      ICompRate 100
                                                                  SafeRate                               support multiple language pairs, the current implementation specif-
         ICompRate (%)




                                                                                SafeRate (%)
                          90                                                 99                          ically targets C-to-Rust translation. Moreover, due to resource con-
                                                                                                         straints, our evaluation is limited to DeepSeek-V3 and Qwen3-32B.
                          80                                                 98                          These choices do not, however, affect the validity of our framework
                          70                                                 97                          evaluation, as the primary contribution lies in the architecture it-
                                                                                                         self rather than in model comparison. Extending the evaluation
                          60                                                 96
                               500   501-1000   1001-5000 5001-10000   >10000                            to include additional languages and models remains an important
                                          Code Length (LoC)                                              direction for future work. 2) Data leakage: Our method uses LLMs
                                                                                                         to translate C code to Rust. Since these models may have been pre-
Figure 2: Translation performance at different project scales.
                                                                                                         trained on public benchmarks, we mitigate this risk by including six
                                                                             1.0                         industrial projects alongside open-source datasets in our evaluation.
                         1.0
                                                                                                         3) Dataset characteristics: The current benchmarks are limited to
                         0.8                                                 0.8
                                                                                                         single-threaded, user-level C projects with ISO C standard library
                                                                                Placeholder
         Sec / LoC




                         0.6                                                 0.6                         dependencies. Future work should consider more complex settings
                         0.4                                                 0.4                         such as multithreading, third-party libraries, and kernel-level code.
                         0.2                                                 0.2
                         0.0
                               500   501-1000   1001-5000 5001-10000   >10000
                                                                             0.0                         6 Related Work
                                          Code Length (LoC)
                                                                                                         6.1 C-to-Rust Translation
    Figure 3: Translation time at different project scales.                                              Existing work for automatic C-to-Rust translation falls into three
                                                                                                         broad categories: rule-based, LLM-based, and hybrid techniques.
                                                                                                            Rule-based Methods rely on manually designed rules to trans-
semantics while ensuring project-wide type consistency. Combined                                         form C code into Rust. The C2Rust transpiler [1] exemplifies this
with a flexible .cast() method for type conversions, this approach                                       approach by using Clang’s AST to generate Rust code, though the
resolves both the interface mismatch and ownership issues that                                           output relies heavily on unsafe blocks. Subsequent work has aimed
cause other methods to fail. By abstracting low-level C operations                                       to improve safety and idiomaticity: Emre et al. [10, 11] used com-
into a safe Rust layer, EvoC2Rust succeeds where other techniques                                        piler feedback for pointer safety; Zhang et al. [51] applied static
fall short.                                                                                              ownership analysis; Ling et al. [27] and Hong et al. [15–18] focused
                                                                                                         on API safety and specific constructs; Larson et al. [24] proposed
5    Limitations and Threats to Validity                                                                 pointer derivation graphs to translate unsafe Rust to safer Rust;
We have identified the following limitations and potential threats                                       Wu et al. [46] retyped polymorphic C void pointers into uses of
to the validity of our method:                                                                           Rust generics. While effective, these methods require significant
   Internal Validity. The main internal threat comes from correct-                                       manual effort and often produce Rust code that is both unsafe and
ness verification, which currently relies on predefined test cases.                                      non-idiomatic.
Adopting more robust validation techniques like fuzzing [21] and                                            LLM-based Methods leverage LLMs to generate idiomatic Rust
self-debugging [22, 38] could enhance test coverage and uncover                                          code without relying on manually defined rules. Eniser et al. [12]
subtle semantic errors. For line acceptance rate measurement, we                                         introduced FLOURINE, which uses fuzz testing to validate semantic
use Claude-generated outputs verified by human experts as ground                                         equivalence between C and Rust code. Yang et al. [48] adapted
truth. While this manual validation ensures correctness beyond                                           MSWasm-based testing for multi-language translation to Rust. Luo
automated testing, it may not scale to larger datasets. Future work                                      et al. [29] proposed IRENE, an LLM-based framework that inte-
should explore semi-automated verification to balance accuracy                                           grates rule-augmented retrieval and structured summarization for
and efficiency.                                                                                          function-level translation. Nitin et al. [31] enhanced LLM transla-
   External Validity. Three primary threats affect external valid-                                       tion by integrating static specifications and I/O tests. Xu et al. [47]
ity: 1) Generalizability: While our translation pipeline is designed to                                  optimized type migration by leveraging data flow graphs. Farrukh
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                                                                                                Wang et al.


  Original C Code                                                                                         Direct Prompting
  static RBTreeNode*rb_tree_rotate(RBTree *tree, RBTreeNode *node, RBTreeNodeSide direction)
  {
    RBTreeNode*new_root;                                                                                  fn rb_tree_node_replace(tree: &mut RBTree, node1: &mut RBTreeNode, node2: Option<&mut RBTreeNode>) {
    /* The child of this node will take its place:                                                          //...
    for a left rotation, it is the right child,                                                           }
    and vice versa. */                                                                                    fn rb_tree_rotate(tree: &mut RBTree, node: *mut RBTreeNode, direction: RBTreeNodeSide) -> *mut RBTreeNode {
    new_root = node->children[1-direction];                                                                 let new_root = unsafe { (*node).children[1 - direction as usize] };

      /* Make new_root the root, update parent pointers. */                                                   rb_tree_node_replace(tree, node, new_root);
      rb_tree_node_replace(tree, node, new_root);                                                             // interface mismatch

      /* Rearrange pointers */                                                                                unsafe { // unsafe code
      node->children[1-direction] = new_root->children[direction];                                            (*node).children[1 - direction as usize] = (*new_root).children[direction as usize];
      new_root->children[direction] = node;                                                                   (*new_root).children[direction as usize] = node;
                                                                                                              (*node).parent = new_root;
      /* Update parent references */                                                                          if !(*node).children[1 - direction as usize].is_null() {
      node->parent = new_root;                                                                                  (*(*node).children[1 - direction as usize]).parent = node;
                                                                                                              }
      if (node->children[1-direction] != NULL) {                                                              }
        node->children[1-direction]->parent = node;                                                           new_root
      }                                                                                                   }
      return new_root;
  }

        Self-Repair                                                                                             EvoC2Rust

  impl RBTree {
    fn rotate(&mut self, node: &mut RBTreeNode, direction: RBTreeNodeSide) -> Option<Box<RBTreeNode>> {   pub fn rb_tree_rotate(mut tree: Ptr<RBTree>, mut node: Ptr<RBTreeNode>, mut direction: RBTreeNodeSide) -> Ptr<RBTreeNode> {
      let opposite = match direction {
        RBTreeNodeSide::Left => RBTreeNodeSide::Right,                                                        let mut new_root: Ptr<RBTreeNode>;
        RBTreeNodeSide::Right => RBTreeNodeSide::Left,
      };                                                                                                      new_root = node.children[1 - direction].cast();
      if let Some(mut new_root) = node.children[opposite as usize].take() {
        self.node_replace(node, Some(new_root.clone()));                                                      rb_tree_node_replace(tree.cast(), node.cast(), new_root.cast());
        node.children[opposite as usize] = new_root.children[direction as usize].take();                      // cast() ensures interface consistency
        if let Some(ref mut child) = node.children[opposite as usize] {
           child.parent = Some(Box::new((*node).clone()));                                                 node.children[1 - direction] = new_root.children[direction].cast();
        }                                                                                                  new_root.children[direction] = node.cast();
        new_root.children[direction as usize] = Some(Box::new((*node).clone()));                          node.parent = new_root.cast();
        node.parent = Some(new_root); // move occurs here
        Some(new_root) // value used after move                                                               if (node.children[1 - direction] != NULL!()).as_bool() {
        // Ownership Pitfall                                                                                     node.children[1 - direction].parent = node.cast();
      } else {                                                                                                }
          None                                                                                                return new_root.cast();
      }                                                                                                       // safe code
    }                                                                                                     }
  }




                                                                     Figure 4: A case study on translating the rb_tree_rotate function.


et al. [13] developed a multi-agent framework featuring iterative er-                                                  and self-repair techniques, yet rely on annotated Rust interfaces
ror correction. However, LLM-based translation suffers from lower                                                      rarely available in practice. Hong et al. [19] addressed this with
accuracy due to the lack of parallel C-Rust training data [34].                                                        Tymcrat, a type inference-based method for automating signature
   Hybrid Methods seek to combine the strengths of both paradigms.                                                     translation.
For instance, C2SaferRust [30] and PR2 [14] employ LLMs to refine                                                         Differing from existing approaches that translate modules se-
rule-based translations, improving safety and idiomaticity while                                                       quentially following dependency order and require full project con-
preserving functional equivalence through testing. SACTOR [52]                                                         texts, EvoC2Rust introduces a skeleton-guided strategy, which first
delegates different tasks to each paradigm, applying C2Rust for data                                                   constructs a compilable Rust skeleton and then executes incremen-
types and an LLM for global variables and functions. Our method                                                        tal function translation. Beyond enabling concurrent processing,
extends this direction with a two-stage framework: it first uses lin-                                                  this design also enhances correctness by isolating the LLM from
guistic feature mappings (i.e., transformation rules) to guide LLM                                                     cross-module dependencies.
translation, then applies a compilation-driven repair mechanism
combining LLM refinement with static analysis. It achieves an effec-                                                   7         Conclusion
tive balance between translation accuracy and safety in automated                                                      We present EvoC2Rust, a novel LLM-powered framework for au-
C-to-Rust migration.                                                                                                   tomated translation of complete C projects to Rust. By leveraging
                                                                                                                       feature mapping-enhanced LLMs, EvoC2Rust performs skeleton-
6.2            Project-level Code Translation with LLMs                                                                guided code translation, augmented with hybrid error correction
While most C-to-Rust translation methods target small code units,                                                      that combines LLM capabilities with static analysis. Extensive evalu-
recent work explores LLM-based project-level translation. These ap-                                                    ation on both open-source and industrial benchmarks demonstrates
proaches typically decompose a C project into dependency-ordered                                                       that EvoC2Rust consistently achieves superior overall performance
units, translate them sequentially, and reassemble the results.                                                        in syntax accuracy, semantic equivalence, and memory safety. Fu-
    Shiraishi et al. [39] pioneered this direction by using project                                                    ture work will extend the approach to more complex settings, in-
metadata to maintain consistency, though their method prioritizes                                                      cluding multithreading, third-party libraries, and kernel-level code
compilation success over functional correctness. Syzygy [37] and                                                       across diverse application domains.
RustMap [6] employ a strategy of translating both functions and
test cases while utilizing feedback mechanisms for repair. Neverthe-                                                   Acknowledgments
less, these approaches necessitate complete dependency contexts                                                        This research is funded by the National Key Research and Develop-
(occasionally through manual intervention) and exhibit limited scal-                                                   ment Program of China (Grant No. 2023YFB4503802), the National
ability when applied to complex industrial codebases. Khatry et                                                        Natural Science Foundation of China (Grant No. 62232003), and the
al. [23] and Ou et al. [34] introduced repository-scale benchmarks                                                     Natural Science Foundation of Shanghai (Grant No. 25ZR1401175).
EvoC2Rust: A Skeleton-guided Framework for Project-Level C-to-Rust Translation                                            ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil


References                                                                                 [29] Feng Luo, Kexing Ji, Cuiyun Gao, Shuzheng Gao, Jia Feng, Kui Liu, Xin Xia, and
 [1] 2025. C2Rust: Migrate C code to Rust. https://github.com/immunant/c2rust.                  Michael R Lyu. 2025. Integrating Rules and Semantics for LLM-Based C-to-Rust
 [2] 2025. The Rust Compiler (rustc). https://doc.rust-lang.org/rustc/.                         Translation. In 2025 IEEE International Conference on Software Maintenance and
 [3] 2025. Tree-Sitter: An incremental parsing system for programming tools. https:             Evolution (ICSME). IEEE.
     //tree-sitter.github.io/tree-sitter.                                                  [30] Vikram Nitin, Rahul Krishna, Luiz Lemos do Valle, and Baishakhi Ray. 2025.
 [4] Alibaba. 2025. Qwen3-32B Model. https://huggingface.co/Qwen/Qwen3-32B.                     C2SaferRust: Transforming C Projects into Safer Rust with NeuroSymbolic Tech-
 [5] Anthropic. 2024. Claude 4 Technical Report. https://www.anthropic.com/index/               niques. CoRR abs/2501.14257 (2025).
     claude-4.                                                                             [31] Vikram Nitin and Baishakhi Ray. 2024. SpecTra: Enhancing the Code Translation
 [6] Xuemeng Cai, Jiakun Liu, Xiping Huang, Yijun Yu, Haitao Wu, Chunmiao Li, Bo                Ability of Language Models by Generating Multi-Modal Specifications. CoRR
     Wang, Imam Nur Bani Yusuf, and Lingxiao Jiang. 2025. RustMap: Towards Project-             abs/2405.18574 (2024).
     Scale C-to-Rust Migration via Program Analysis and LLM. CoRR abs/2503.17741           [32] Beijing Academy of Artificial Intelligence. 2025. M3-Embedding: Multi-
     (2025).                                                                                    Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through
 [7] DARPA-SN-24-89. 2024. Translating All C TO Rust (TRACTOR). https://www.                    Self-Knowledge Distillation. https://huggingface.co/BAAI/bge-m3.
     darpa.mil/program/translating-all-c-to-rust.                                          [33] Office of the National Cyber Director. 2024. Back to the building blocks: A
 [8] DeepSeek-AI. 2025. DeepSeek-V3 Model. https://api.deepseek.com.                            path toward secure and measurable software. https://www.whitehouse.gov/wp-
 [9] Saman Dehghan, Tianran Sun, Tianxiang Wu, Zihan Li, and Reyhaneh Jabbarvand.               content/uploads/2024/02/Final-ONCD-Technical-Report.pdf.
     2025. Translating Large-Scale C Repositories to Idiomatic Rust. arXiv preprint        [34] Guangsheng Ou, Mingwei Liu, Yuxuan Chen, Xin Peng, and Zibin Zheng.
     arXiv:2511.20617 (2025).                                                                   2024. Repository-level Code Translation Benchmark Targeting Rust. CoRR
[10] Mehmet Emre, Peter Boyland, Aesha Parekh, Ryan Schroeder, Kyle Dewey, and                  abs/2411.13990 (2024).
     Ben Hardekopf. 2023. Aliasing Limits on Translating C to Safe Rust. Proc. ACM         [35] Rangeet Pan, Ali Reza Ibrahimzada, Rahul Krishna, Divya Sankar, Lam-
     Program. Lang. 7, OOPSLA1 (2023), 551–579.                                                 bert Pouguem Wassi, Michele Merler, Boris Sobolev, Raju Pavuluri, Saurabh
[11] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2021. Translat-                Sinha, and Reyhaneh Jabbarvand. 2024. Lost in Translation: A Study of Bugs
     ing C to safer Rust. Proc. ACM Program. Lang. 5, OOPSLA (2021), 1–29.                      Introduced by Large Language Models while Translating Code. In Proceedings of
[12] Hasan Ferit Eniser, Hanliang Zhang, Cristina David, Meng Wang, Maria Chris-                the 46th IEEE/ACM International Conference on Software Engineering, ICSE 2024,
     takis, Brandon Paulsen, Joey Dodds, and Daniel Kroening. 2024. Towards Trans-              Lisbon, Portugal, April 14-20, 2024. ACM, 82:1–82:13.
     lating Real-World Code with LLMs: A Study of Translating to Rust. CoRR                [36] Baptiste Rozière, Marie-Anne Lachaux, Lowik Chanussot, and Guillaume Lample.
     abs/2405.11514 (2024).                                                                     2020. Unsupervised Translation of Programming Languages. In Advances in Neu-
[13] Muhammad Farrukh, Smeet Shah, Baris Coskun, and Michalis Polychronakis.                    ral Information Processing Systems 33: Annual Conference on Neural Information
     2025. SafeTrans: LLM-assisted Transpilation from C to Rust. CoRR abs/2505.10708            Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual.
     (2025).                                                                               [37] Manish Shetty, Naman Jain, Adwait Godbole, Sanjit A. Seshia, and Koushik Sen.
[14] Yifei Gao, Chengpeng Wang, Pengxiang Huang, Xuwei Liu, Mingwei Zheng,                      2024. Syzygy: Dual Code-Test C to (safe) Rust Translation using LLMs and
     and Xiangyu Zhang. 2025. PR2: Peephole Raw Pointer Rewriting with LLMs for                 Dynamic Analysis. CoRR abs/2412.14234 (2024).
     Translating C to Safer Rust. CoRR abs/2505.04852 (2025).                              [38] Yuling Shi, Songsong Wang, Chengcheng Wan, and Xiaodong Gu. 2024. From
[15] Jaemin Hong and Sukyoung Ryu. 2023. Concrat: An Automatic C-to-Rust Lock                   code to correctness: Closing the last mile of code generation with hierarchical
     API Translator for Concurrent Programs. In 45th IEEE/ACM International Confer-             debugging. arXiv preprint arXiv:2410.01215 (2024).
     ence on Software Engineering, ICSE 2023, Melbourne, Australia, May 14-20, 2023.       [39] Momoko Shiraishi and Takahiro Shinagawa. 2024. Context-aware Code Seg-
     IEEE, 716–728.                                                                             mentation for C-to-Rust Translation using Large Language Models. CoRR
[16] Jaemin Hong and Sukyoung Ryu. 2024. Don’t Write, but Return: Replacing                     abs/2409.10506 (2024).
     Output Parameters with Algebraic Data Types in C-to-Rust Translation. Proc.           [40] HoHyun Sim, Hyeonjoong Cho, Yeonghyeon Go, Zhoulai Fu, Ali Shokri, and
     ACM Program. Lang. 8, PLDI (2024), 716–740.                                                Binoy Ravindran. 2025. Large Language Model-Powered Agent for C to Rust
[17] Jaemin Hong and Sukyoung Ryu. 2024. To Tag, or Not to Tag: Translating C’s                 Code Translation. CoRR abs/2505.15858 (2025).
     Unions to Rust’s Tagged Unions. In Proceedings of the 39th IEEE/ACM International     [41] Qingxiao Tao, Tingrui Yu, Xiaodong Gu, and Beijun Shen. 2024. Unraveling the
     Conference on Automated Software Engineering, ASE 2024, Sacramento, CA, USA,               Potential of Large Language Models in Code Translation: How Far are We?. In
     October 27 - November 1, 2024. ACM, 40–52.                                                 31st Asia-Pacific Software Engineering Conference, APSEC 2024, Chongqing, China,
[18] Jaemin Hong and Sukyoung Ryu. 2025. Forcrat: Automatic I/O API Translation                 December 3-6, 2024. IEEE, 353–362.
     from C to Rust via Origin and Capability Analysis. CoRR abs/2506.01427 (2025).        [42] Vivo. 2025.        Benchmark for Vivo C-to-Rust Innovation Competition.
[19] Jaemin Hong and Sukyoung Ryu. 2025. Type-migrating C-to-Rust translation                   https://atomgit.com/vivoblueos2/vivo_blueos_contest2_c2rust/tree/master/01-
     using a large language model. Empir. Softw. Eng. 30, 1 (2025), 3.                          BlueOS2_Translation/Input/01-Primary.
[20] Mingsheng Jiao, Tingrui Yu, Xuan Li, Guanjie Qiu, Xiaodong Gu, and Beijun Shen.       [43] Chaofan Wang, Guanjie Qiu, Xiaodong Gu, and Beijun Shen. 2025. ApiRAT:
     2023. On the Evaluation of Neural Code Translation: Taxonomy and Benchmark.                Integrating Multi-source API Knowledge for Enhanced Code Translation with
     In 38th IEEE/ACM International Conference on Automated Software Engineering,               LLMs. In 49th IEEE Annual Computers, Software, and Applications Conference,
     ASE 2023, Luxembourg, September 11-15, 2023. IEEE, 1529–1541.                              COMPSAC 2025, Toronto, ON, Canada, July 8-11, 2025. IEEE, 1400–1405.
[21] Ismet Burak Kadron, Yannic Noller, Rohan Padhye, Tevfik Bultan, Corina S.             [44] Yanli Wang, Yanlin Wang, Suiquan Wang, Daya Guo, Jiachi Chen, John C. Grundy,
     Pasareanu, and Koushik Sen. 2024. Fuzzing, Symbolic Execution, and Expert                  Xilin Liu, Yuchi Ma, Mingzhi Mao, Hongyu Zhang, and Zibin Zheng. 2024. Repo-
     Guidance for Better Testing. IEEE Softw. 41, 1 (2024), 98–104.                             TransBench: A Real-World Benchmark for Repository-Level Code Translation.
[22] Sungmin Kang, Bei Chen, Shin Yoo, and Jian-Guang Lou. 2025. Explainable                    CoRR abs/2412.17744 (2024).
     automated debugging via large language model-driven scientific debugging.             [45] Alex Williams. 2024. Improving Memory Management, Performance with Rust:
     Empir. Softw. Eng. 30, 2 (2025), 45.                                                       Why Rust is becoming the programming language of choice for many high-level
[23] Anirudh Khatry, Robert Zhang, Jia Pan, Ziteng Wang, Qiaochu Chen, Greg                     developers. Commun. ACM 67, 9 (2024), 8–9.
     Durrett, and Isil Dillig. 2025. CRUST-Bench: A Comprehensive Benchmark for            [46] Xiafa Wu and Brian Demsky. 2025. GenC2Rust: Towards Generating Generic Rust
     C-to-safe-Rust Transpilation. CoRR abs/2504.15254 (2025).                                  Code from C. In 47th IEEE/ACM International Conference on Software Engineering,
[24] Per Larsen. 2024. Migrating C to Rust for Memory Safety. IEEE Secur. Priv. 22, 4           ICSE 2025, Ottawa, ON, Canada, April 26 - May 6, 2025. IEEE, 90–102.
     (2024), 22–29.                                                                        [47] Qingxiao Xu and Jeff Huang. 2025. Optimizing Type Migration for LLM-Based
[25] Ruishi Li, Bo Wang, Tianyu Li, Prateek Saxena, and Ashish Kundu. 2025. Translat-           C-to-Rust Translation: A Data Flow Graph Approach. In Proceedings of the 14th
     ing C to Rust: Lessons from a User Study. In 32nd Annual Network and Distributed           ACM SIGPLAN International Workshop on the State Of the Art in Program Analysis,
     System Security Symposium, NDSS 2025, San Diego, California, USA, February                 SOAP 2025, Seoul, Republic of Korea, 16 June 2025. ACM, 8–14.
     24-28, 2025. The Internet Society.                                                    [48] Aidan Z. H. Yang, Yoshiki Takashima, Brandon Paulsen, Josiah Dodds, and Daniel
[26] Xuan Li, Shuai Yuan, Xiaodong Gu, Yuting Chen, and Beijun Shen. 2024. Few-                 Kroening. 2024. VERT: Verified Equivalent Rust Transpilation with Few-Shot
     shot code translation via task-adapted prompt learning. J. Syst. Softw. 212 (2024),        Learning. CoRR abs/2404.18852 (2024).
     112002.                                                                               [49] Zhen Yang, Fang Liu, Zhongxing Yu, Jacky Wai Keung, Jia Li, Shuo Liu, Yifan
[27] Michael Ling, Yijun Yu, Haitao Wu, Yuan Wang, James R. Cordy, and Ahmed E.                 Hong, Xiaoxue Ma, Zhi Jin, and Ge Li. 2024. Exploring and Unleashing the Power
     Hassan. 2022. In Rust We Trust - A Transpiler from Unsafe C to Safer Rust. In              of Large Language Models in Automated Code Translation. Proc. ACM Softw.
     44th IEEE/ACM International Conference on Software Engineering: Companion Pro-             Eng. 1, FSE (2024), 1585–1608.
     ceedings, ICSE Companion 2022, Pittsburgh, PA, USA, May 22-24, 2022. ACM/IEEE,        [50] Shangbo Yun, Shuhuai Lin, Xiaodong Gu, and Beijun Shen. 2024. Project-specific
     354–355.                                                                                   code summarization with in-context learning. J. Syst. Softw. 216 (2024), 112149.
[28] Bob Lord. 2023. The Urgent Need for Memory Safety in Software Prod-                   [51] Hanliang Zhang, Cristina David, Yijun Yu, and Meng Wang. 2023. Ownership
     ucts. https://www.cisa.gov/news-events/news/urgent-need-memory-safety-                     Guided C to Rust Translation. In Computer Aided Verification - 35th International
     software-products.                                                                         Conference, CAV 2023, Paris, France, July 17-22, 2023, Proceedings, Part III (Lecture
ICSE-SEIP ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                                                     Wang et al.


     Notes in Computer Science, Vol. 13966). Springer, 459–482.                            Artificial Intelligence. AAAI Press, 11783–11790.
[52] Tianyang Zhou, Haowen Lin, Somesh Jha, Mihai Christodorescu, Kirill Levchenko,   [54] Albert Ziegler, Eirini Kalliamvakou, X. Alice Li, Andrew Rice, Devon Rifkin,
     and Varun Chandrasekaran. 2025. LLM-Driven Multi-step Translation from C to           Shawn Simister, Ganesh Sittampalam, and Edward Aftandilian. 2022. Productivity
     Rust using Static Analysis. CoRR abs/2503.12511 (2025).                               assessment of neural code completion. In MAPS@PLDI 2022: 6th ACM SIGPLAN
[53] Ming Zhu, Karthik Suresh, and Chandan K. Reddy. 2022. Multilingual Code               International Symposium on Machine Programming, San Diego, CA, USA, 13 June
     Snippets Training for Program Translation. In Thirty-Sixth AAAI Conference on         2022. ACM, 21–29.
