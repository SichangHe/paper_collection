                                         SmartC2Rust: Iterative, Feedback-Driven C-to-Rust Translation
                                            via Large Language Models for Safety and Equivalence
                                                       Momoko Shiraishi                                                Yinzhi Cao                           Takahiro Shinagawa
                                                    The University of Tokyo                                   Johns Hopkins University                      The University of Tokyo
                                                          Tokyo, Japan                                             Baltimore, USA                                Tokyo, Japan
                                                 shiraishi@os.is.s.u-tokyo.ac.jp                                 yinzhi.cao@jhu.edu                         shina@is.s.u-tokyo.ac.jp

                                        Abstract                                                                                1   Introduction
                                        Memory safety vulnerabilities remain prevalent in today’s software                      Memory safety vulnerabilities, despite their long history, continue
                                        systems and one promising solution to mitigate them is to adopt                         to pose significant threats to software systems written in unsafe
                                        memory-safe languages such as Rust. Due to legacy code written                          languages such as C, leading to many critical security flaws [27]. A
arXiv:2409.10506v3 [cs.SE] 1 Dec 2025




                                        in memory unsafe C, there is strong motivation to translate legacy                      promising solution for mitigating such vulnerabilities is to build
                                        C code into Rust. Prior works have already shown promise in using                       software systems using memory-safe languages such as Rust. Since
                                        Large Language Models (LLMs) for such translations. However, sig-                       many legacy software systems are still written in the C language, a
                                        nificant challenges persist for LLM-based translation: the translated                   natural research problem is translating legacy C code into Rust to
                                        code often fails to compile, let alone reduce unsafe statements and                     enhance security [19].
                                        maintain the semantic functionalities due to inherent limitations                          Existing translation approaches can be broadly categorized
                                        of LLMs such as limited token size and inconsistent outputs.                            into two types: rule-based and large language model (LLM)-based.
                                           In this paper, we design an automated C-to-Rust translation                          Rule-based approaches [23, 24, 28, 29, 32], e.g., C2Rust [32], rely
                                        system, called SmartC2Rust, to segment and convert the C code                           on predefined translation mapping rules, such as rewriting raw
                                        to Rust with memory safety and semantic equivalence. The key                            pointers and unsafe blocks into safer Rust alternatives. However,
                                        insight is to iteratively refine the output Rust code with addi-                        one-to-one conversion has limitations in accurately describing
                                        tional feedback, e.g., compilation errors, segmentation contexts,                       countless mappings and selecting the appropriate translations
                                        semantic discrepancies, and memory unsafe statements. Such                              based on context. As a result, these approaches often still produce
                                        feedback will gradually improve the quality of generated Rust code,                     non-idiomatic and unsafe Rust code [41]. In contrast, LLM-based
                                        thus mitigating unsafety, inconsistency, and semantic issues. Our                       translations [25, 39, 54], show promise in generating more idiomatic
                                        evaluation shows that SmartC2Rust significantly decreases the                           and safer Rust code with minimal reliance on unsafe constructs,
                                        unsafe statements and outperforms prior works in security and                           potentially producing better, more secure code efficiently. However,
                                        semantic equivalence.                                                                   LLM-based translation is still in its early stages and faces several
                                                                                                                                challenges:
                                        CCS Concepts                                                                            • Memory Safety. The translated Rust code needs to eliminate
                                        • Software and its engineering → Source code generation;                                   unsafe C features, instead of relying on unsafe blocks or raw
                                        Software testing and debugging; Maintaining software; Software                             pointers. However, prior works [25, 39] often fail to remove such
                                        maintenance tools; • Security and privacy → Software security                              features, undermining Rust’s memory safety improvements.
                                        engineering.                                                                            • Semantic Equivalence. The translated Rust code is expected
                                                                                                                                   to preserve the functionality of the original C code. However,
                                                                                                                                   existing approaches often fail to even compile or to pass the
                                        Keywords                                                                                   test cases accompanying the original C program, resulting in
                                        C-to-Rust Translation, Large Language Models, Memory Safety                                semantic inequivalence. Several prior works [25, 54] have shown
                                                                                                                                   that LLMs struggle to generate compilable Rust code even small-
                                        ACM Reference Format:                                                                      scale C programs with fewer than 100 lines of code.
                                        Momoko Shiraishi, Yinzhi Cao, and Takahiro Shinagawa. 2026. SmartC2Rust:                • Macro Translation. Translating C macros to Rust is challenging:
                                        Iterative, Feedback-Driven C-to-Rust Translation via Large Language                        Existing approaches often alter semantics by expanding macros
                                        Models for Safety and Equivalence. In 2026 IEEE/ACM 48th International
                                                                                                                                   in the C code for translation [42], which disables conditional
                                        Conference on Software Engineering (ICSE ’26), April 12–18, 2026, Rio de
                                                                                                                                   compilation and reduces code portability across different systems
                                        Janeiro, Brazil. ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/
                                        3744916.3773259                                                                            or environments.
                                                                                                                                • Limited LLM Context Windows [6]. Modern LLMs have a
                                                                                                                                   limited context window, restricting the number of tokens they
                                                                                                                                   can process at once. Previous studies [15, 35] have also shown
                                                                                                                                   that performance accuracy decreases as token count increases,
                                        This work is licensed under a Creative Commons Attribution 4.0 International License.      even with 2,000-3,000 input tokens.
                                        ICSE ’26, Rio de Janeiro, Brazil                                                           In this paper, we design an automated C-to-Rust translation
                                        © 2026 Copyright held by the owner/author(s).
                                        ACM ISBN 979-8-4007-2025-3/26/04                                                        system, called SmartC2Rust, to achieve memory safety and semantic
                                        https://doi.org/10.1145/3744916.3773259                                                 equivalence under the constraint of limited LLM context windows.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                               Momoko Shiraishi, Yinzhi Cao, and Takahiro Shinagawa


The high-level idea is to iteratively refine the Rust code generated      1   char * url_get_protocol ( char * url ) {
                                                                          2     char * protocol = malloc ( URL_PROTOCOL_MAX_LENGTH *
by LLMs with additional information related to memory safety                          sizeof ( char ) ) ; // allocate a memory
or semantics until it passes the test. Accordingly, SmartC2Rust           3     if (! protocol ) return NULL ;
prompts the LLM to fix the generated Rust code based on feedback,         4     sscanf ( url , " %[^://] " , protocol ) ; // risk of overflow
                                                                          5     if ( url_is_protocol ( protocol ) ) return protocol ;
such as compilation errors and differences in test case results           6     return NULL ;
between the C and Rust code. To address the aforementioned                7   }
challenges, SmartC2Rust employs the following techniques:
                                                                                   Listing 1: An Example of Unsafe C Function
• Code Refinement for Improved Security. SmartC2Rust detects
   unsafe translations by identifying insecure features such as raw       1   use url :: Url ;
                                                                          2   pub fn rust_url_get_protocol ( url : & str ) ->
   pointers and unsafe blocks. It then prompts the LLM to refine                     Option < String > {
   the translation by eliminating these features.                         3     let parsed = Url :: parse ( url ) . ok () ?; // parsing
• Localization of Functional Error. SmartC2Rust runs both the             4     let protocol = parsed . scheme () . to_string () ;
                                                                          5     if rust_url_is_protocol (& protocol ) {
   original C code and the translated Rust code using test cases to       6          return Some ( protocol ) ;
   validate semantic correctness. It compares execution traces, such      7     }
   as call stack traces and outputs like return values, to localize       8     None
                                                                          9   }
   potential translation errors. SmartC2Rust then prompts the LLM
   to fix these errors using the identified code snippets and observed         Listing 2: Rust Code Translated with SmartC2Rust.
   output differences.
• Semantic Preservation of C Macros. SmartC2Rust preserves
   the semantics of C macros where possible by detecting and              1   #[ no_mangle ]
                                                                          2   pub unsafe extern " C " fn url_get_protocol (
   transforming them without expansion. In addition to constants          3          mut url : * mut libc :: c_char ,
   and functions defined with #define, SmartC2Rust transforms             4   ) -> * mut libc :: c_char {
   conditional compilation using #ifdef blocks into Rust’s cfg            5     let mut protocol : * mut libc :: c_char = malloc (
                                                                          6     (16 as libc :: c_int as libc :: c_ulong )
   attribute [43], enabling the translated Rust code to support a         7       . wrapping_mul (:: core :: mem :: size_of :: < libc :: c_char >()
   single codebase without requiring developers to manage multiple                      as libc :: c_ulong ) ,
                                                                          8     ) as * mut libc :: c_char ;
   separate versions for different configurations.                        9     if protocol . is_null () {
• Modular Segmentation with Translation Contexts. SmartC2Rust            10           return 0 as * mut libc :: c_char ;
   segments C code into smaller fragments and supplements the            11     }
                                                                         12     sscanf ( url , b " %[^://]\0 " as * const u8 as * const
   translation of each fragment with relevant context, such as                         libc :: c_char , protocol ) ; // still uses sscanf ()
   metadata from previous translations, to enhance consistency           13     if url_is_protocol ( protocol ) {
                                                                         14           return protocol ;
   and accuracy. For example, SmartC2Rust stores translated Rust         15     }
   function signatures along with their corresponding C function         16     return 0 as * mut libc :: c_char ;
   names and locations in a compressed database, ensuring consis-        17   }
   tent naming across translations of different fragments.                        Listing 3: Rust Code Translated with C2Rust.
   We provide artifacts of SmartC2Rust at this repository [2]
and an online demonstration at this URL [1]. We compared
SmartC2Rust against state-of-the-art rule- and LLM-based trans-
                                                                         fixed-size memory buffer at Line 2, but sscanf() at Line 4 can
lation tools, including C2Rust [32], Crown [59], Laertes [23], and
                                                                         copy an arbitrarily long protocol name into the protocol buffer,
C2SaferRust [39]. We evaluated SmartC2Rust against 21 programs
                                                                         exceeding the allocated size and causing a heap buffer overflow.
up to approximately 3,000 lines of code, and our evaluation shows
                                                                         Second, the allocated memory buffer may not be freed, leading to a
that SmartC2Rust outperforms prior works in reducing unsafe
                                                                         memory leak and potentially leaving a dangling pointer.
statements by 99.4%, improving test case pass rates by 11.25%, and
                                                                            Listing 2 shows the correctly translated Rust code of this function
achieving 85.2 % preservation of the semantic meaning of C macros.
                                                                         using SmartC2Rust. First, sscanf() is replaced with the parse()
                                                                         method from Rust’s standard Url parsing library [22], eliminating
2     Overview                                                           the heap buffer overflow while preserving the original URL parsing
In this section, we first describe a motivating example of C and         functionality. Second, unused data is automatically deallocated
translated Rust code with translation challenges, and then give an       through Rust’s ownership and borrowing mechanism, preventing
overview of our solution.                                                memory leaks and other safety issues. Thus, the translated Rust code
                                                                         successfully eliminates both memory safety issues in the original C
2.1      A Motivating Example                                            implementation while maintaining semantic equivalence.
We present a motivating example in Listing 1, an unsafe C                   Such a C-to-Rust translation, albeit intuitively simple, is chal-
function, url_get_protocol(), from the real-world program                lenging for both rule-based and LLM-based approaches from the
urlparser [23]. The function extracts the protocol name, e.g., “http,”   following three aspects. First, translating a C program into Rust
“https,” and “ftp,” from a URL string into char *protocol. It then       code without using unsafe is not straightforward. For example,
returns the protocol if the extracted name is valid or NULL otherwise.   C2Rust [32], a state-of-the-art rule-based translator, converts
The function has two memory safety issues. First, it allocates a         the C code in Listing 1 into Rust code in Listing 3. This code
SmartC2Rust                                                                                          ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


retains sscanf() at Line 12 within an unsafe block and also uses           Finally, SmartC2Rust ensures consistency between translations
malloc() along with a Rust raw pointer to manage the protocol           by maintaining supplementary correspondence metadata. It first re-
buffer, failing to address any memory safety issues. Similarly,         orders code elements so that closely related code is placed together,
C2SaferRust [39], an existing LLM-based translator, generates code      making it easier to maintain context. Next, during translation, it
that calls C functions within an unsafe block. This occurs because      generates summary information, such as function signatures and
C2SaferRust relies on C2Rust for initial translation and then applies   data types, alongside the target C code to improve consistency.
an LLM for refinement, but the LLM fails to eliminate the unsafe        For example, SmartC2Rust provides the url_is_protocol()’s
code.                                                                   function signature in translating the code in Listing 1 so that the
    Second, maintaining semantic equivalence before and after trans-    translation can correctly capture the dependency.
lation is challenging. For example, the URL parsing functionality
is implemented using sscanf() and url_get_protocol() in the             3     Design
original C code, whereas the Rust code uses the corresponding           In this section, we describe the design of SmartC2Rust from its
Url::parse() method and rust_url_is_protocol(). Correctly               system architecture and three major stages.
translating such functions requires a deep understanding of the
semantics of both the original C code and the translated Rust code.     3.1    System Architecture
As with human developers, fully understanding the semantics solely      Figure 1 shows the architecture of SmartC2Rust, which has three
from the textual representation without executing them is not easy.     major stages: (i) pre-processing, (ii) translation and quality check,
    Third, maintaining translation consistency across the entire        and (iii) feedback-driven code repair. Our high-level idea is to
program is challenging. As previously mentioned, the LLM context        break down code into smaller parts with contexts from previous
window size limitation prevents the entire program from being           translations so that LLMs can provide more effective responses.
translated at once. Thus, the translation process is divided into           In Stage (i), SmartC2Rust merges C code from multiple files
smaller units, such as the code shown in Listing 1. However, this       into larger modules, reorders code elements, and segments the
often leads to inconsistencies between different translation units.     merged code into smaller translation units. It also parses each unit to
For example, when generating code to call another function that has     generate metadata, later used in prompts to supplement translation
already been translated in a separate unit, LLMs may fail to retain     context across runs. In Stage (ii), SmartC2Rust translates each C
information from previous translations, resulting in inconsistencies    unit into a corresponding Rust unit using LLMs, supplementing
in names, functionality, or other aspects.                              prompts with metadata from both C and Rust as context. It then
                                                                        refines the translated Rust code to improve idiomaticity. In Stage
                                                                        (iii), SmartC2Rust repairs the translated Rust code based on feedback
2.2    Overall Solution                                                 from compilation or test cases.

We now provide an overview of SmartC2Rust and describe how it           3.2    Stage (i): Pre-processing
addresses the three challenges using the same example.
                                                                        The goal of Stage (i) is to transform C code for better LLM
    First, SmartC2Rust ensures memory safety during translation
                                                                        comprehension. It consists of three steps: (1) merging C code into
through iterative refinement. LLMs often generate unsafe code even
                                                                        modules for information aggregation, (2) code reordering and macro
when explicitly instructed not to use it. Thus, SmartC2Rust first
                                                                        transformation to provide translation context, and (3) C module
identifies unsafe patterns, such as unsafe blocks and raw pointers,
                                                                        segmentation to fit LLM token limits.
as seen in Listing 3, in each translation. It then prompts the LLM to
refine the code until such patterns reduce.                             3.2.1 Merging C code into modules. SmartC2Rust analyzes the C
    Next, SmartC2Rust ensures semantic equivalence through exe-         target program to detect the locations of function declarations and
cution result comparison. That is, SmartC2Rust executes both the        definitions, and then merges them by copying the contents of the
original and translated code using test cases accompanied with the      included files into those containing the #include directives. To
original C code. Then, it compares the execution results, including     avoid conflicts, SmartC2Rust ensures that the namespaces of static
the call stack leading to the function, the inputs (e.g., the url       variables and functions are unique. It also allows LLMs to reference
variables at Line 1 of Listing 1 and Line 2 of Listing 2), and the      both declarations and definitions within their context windows,
return values (e.g., Line 5 of Listing 1 and Line 6 of Listing 2).      facilitating the generation of accurate Rust code. Since Rust does
If the input and output of the entry point function are identical,      not separate declarations into different files like C, the translated
SmartC2Rust considers them semantically equivalent. Otherwise,          Rust code can be used directly as a Rust module.
SmartC2Rust prompts the LLM to refine the translated code based            The rationale behind this merging step is to unify how func-
on the identified differences and the related function. Note that,      tions and types are referenced across files in C and Rust. In C,
while SmartC2Rust tracks the input and output of all functions as       declarations are typically separated from definitions: header files
supplementary information, it judges semantic equivalence using         contain function and type declarations, while source files hold their
only the entry point function rather than verifying unit tests for      definitions and implementations. In contrast, Rust uses the use
every function, recognizing that C and Rust functions may not           keyword to import modules, with functions and variables both
have a one-to-one correspondence. For example, for standalone           declared and defined within a single module file. The merging
programs, we implement end-to-end testing to verify semantic            step consolidates declarations and definitions in the C source code,
equivalence.                                                            facilitating subsequent translation to Rust.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                               Momoko Shiraishi, Yinzhi Cao, and Takahiro Shinagawa




                                                      Figure 1: Overview of SmartC2Rust.


3.2.2 Code Reordering and Macro Transformation. This step con-                  Table 1: Logic Block Definitions and Examples
sists of two sub-steps. First, SmartC2Rust reorders code elements,
such as functions and type definitions, in the merged module in                 Logic Blocks                               Example
topological order—that is, they appear before being referenced. This            Functions                    int add(int a, int b) { return a + b; }
improves name resolution and module importing, as all functions                 Global Variables              static char buffer[BUFFER_SIZE];
                                                                                Type Definitions               typedef struct { int x, y; } Point;
and types are already defined in C during translation and such                  Macro Functions             #define MAX(a, b) ((a) > (b) ? (a) : (b))
definitions can be provided as contextual metadata.                             Macro Variables                  #define BUFFER_SIZE 1024
   Second, SmartC2Rust detects all macros for conditional com-                  Preprocessor Conditionals           #ifdef DEBUG ... #endif
                                                                                Header Inclusions                      #include <stdio.h>
pilation in C without expanding them, and then asks the LLM to
determine whether the macro should be defined in Cargo.toml,
build.rs, lib.rs, or each module file. This analysis enables the         3.3    Stage (ii): Translation and Quality Check
C macros to be semantically preserved in the translated Rust code.
                                                                         In Stage (ii), SmartC2Rust translates each C unit and refines the
For example, #ifdef blocks are detected and predetermined to
                                                                         translated Rust code.
be used with the cfg attribute, and this analysis result is used
in translation. Note that macros are traditionally challenging in        3.3.1 Translation. This step translates a given C unit into Rust
translation, because they are processed by a preprocessor rather         using the translation prompt shown in Fig. 2. The prompt consists
than a compiler. C2Rust, a prior rule-based translation, expands all     of four parts: translation rules, contextual metadata, split responses,
macros into C, which may lead to semantic difference for different       and C source code. The contextual metadata is extracted during
environments if #ifdef is present.                                       segmentation in Stage (i) and updated in Stage (ii). Specifically, it
                                                                         is enriched using another LLM prompt that includes both the C
                                                                         and translated Rust code to incorporate Rust function signatures.
3.2.3 C Module Segmentation. This step consists of (1) segmen-           This enhancement of contextual metadata improves the quality and
tation and (2) contextual metadata extraction. First, SmartC2Rust        consistency of the Rust translation.
segments C code modules into smaller translation units. It includes         The response split handles the LLM output token size limit.
as much code as possible in each unit while preserving semantics to      SmartC2Rust instructs the LLM to split the response into multiple
improve translation efficiency. Specifically, SmartC2Rust maintains      parts if it exceeds the length limit. It preserves context from earlier
a counter to track included code and divides modules based on            parts and merges all responses into one.
logical blocks. A logical block refers to a semantically cohesive unit
in C, such as function or type definitions, with examples listed in      3.3.2 Quality Check. This step refines the translated Rust code to
Table 1. SmartC2Rust selects the closest logical block boundary          improve quality. The prompt in this step consists of three parts:
to a given line of code and segments the C module accordingly.           (1) Rust code, (2) refinement guidelines, and (3) self-evaluation
Functions with circular dependencies are treated as a single logical     rules. The refinement guidelines define rules for enhancing Rust
block to ensure LLMs can resolve function references correctly.          code quality, such as removing unsafe blocks and raw pointers
   Second, SmartC2Rust analyzes the original C translation units to      and avoiding static mut for global variables. The self-evaluation
extract contextual metadata. Specifically, it records the definitions    flag ensures that LLMs adhere to the instructions. The translation
and call sites of code elements in the source code, storing this         process repeats until all flags are set to true. The flags include:
data in JSON format. This metadata supplements context between           • "refined_completed": The Rust code has been successfully
translation units without overloading the context window, thereby           refined to proper Rust style, improving safety and adherence
improving translation accuracy.                                             to Rust principles.
SmartC2Rust                                                                                                            ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


  Translate the following C code into Rust by strictly following the rules below.         [ Expected C Program Flow ]
  ## Translation rules                                                                    ▶ main ( which . c :50)
 - Declare all items (structures, enums, functions, constants, etc.) using pub (public)       IN → ( argv :[ " ./ which " , " -- help " ])
  to allow importing.                                                                         ▶ uidget ( bash . c :30)
 - Avoid unsafe in external function calls by using safe equivalents from Rust’s                 OUT ← 0
  standard libraries or crates.                                                               ▶ path_search ( which . c :20)
  ## Contextual Metadata                                                                      IN → ( cmd : -- help , path_list : ...) // ... continues
 - The definitions of the elements used in the C code have been provided in Rust in
  other modules as follows.                                                               [ Current Rust Program Flow ]
  · pub fn quadtree_search(tree: &Quadtree, x: f64, y: f64) ->                            ▶ rust_main ( module1 / unit0 . rs :40)
  Option<&QuadtreePoint> (defined in crate::quadtree_0)                                       IN → ( args :[ " ./ which " , " -- help " ])
  · pub fn quadtree_node_isleaf(node: &QuadtreeNode) -> bool (defined in                      ▶ rust_uidget ( module4 / unit0 . rs :35)
  crate::quadtree_0)                                                                             OUT ← 0
  ...                                                                                         ▶ rust_path_search ( module4 / unit0 . rs :120)
  ## Split Response                                                                           IN → ( cmd : -- help , path_list : ...) // ... continues
 - If the answer exceeds the token size ...
  ## C source code:
  [Paste the C unit code]                                                                       Figure 3: An example of function execution flow.

            Figure 2: An Example Translation Prompt                                       (Lines 5-–12). In the algorithm, 𝐶_𝑈 𝑁 𝐼𝑇 and 𝑅_𝑈 𝑁 𝐼𝑇 denote a C or
                                                                                          Rust translation unit, respectively, and 𝑆 represents the translated
Algorithm 1 Feedback-driven Code Repair                                                   Rust program. SmartC2Rust iterates through all errors and attempts
Require: Input: 𝐶 _𝑈 𝑁 𝐼𝑇1 , 𝐶 _𝑈 𝑁 𝐼𝑇2 , . . . , 𝐶 _𝑈 𝑁 𝐼𝑇𝑛 , 𝐷𝑒𝑝𝐶 : C metadata          repairs until none remain (Lines 13–28 for compilation repair and
Ensure: Output: 𝑆 = {𝑅 _𝑈 𝑁 𝐼𝑇0 , 𝑅 _𝑈 𝑁 𝐼𝑇1 , 𝑅 _𝑈 𝑁 𝐼𝑇2 , . . . , 𝑅 _𝑈 𝑁 𝐼𝑇𝑛 }
  1: 𝑆 ← ∅ , where S: Translated Rust program                                             29–37 for semantic repair). We now describe two key steps in the
  2: 𝐶𝑂𝑀𝑃𝐼 𝐿𝐸 _𝑀𝐴𝑋 ← 𝑁                                                                    repair process: (1) error collection and (2) iterative repair.
  3: 𝑅𝐸𝑃𝐴𝐼𝑅 _𝑀𝐴𝑋 ← 𝑁 ′
  4: for 𝑖 ← 0 to 𝑛 do                                                                    3.4.1 Error Collection. SmartC2Rust repairs four types of errors:
  5:     if 𝑖 = 0 then
  6:         𝑅 _𝑈 𝑁 𝐼𝑇0 ← translate_state_macros (𝐷𝑒𝑝𝐶 )                                  • Syntactic Errors during Compilation. SmartC2Rust compiles
  7:     else
  8:         𝑅 _𝑈 𝑁 𝐼𝑇𝑖 ← translate (𝐶 _𝑈 𝑁 𝐼𝑇𝑖 , 𝐷𝑒𝑝𝐶 )                                     the translated Rust code and records compilation errors (com-
  9:          while not all evaluation flags are true do
 10:             𝑅 _𝑈 𝑁 𝐼𝑇𝑖 ← refine_quality (𝑅 _𝑈 𝑁 𝐼𝑇𝑖 )
                                                                                             pile_error in Algorithm 1). Raw compile error logs are directly
 11:          end while                                                                      included for later repairs.
 12:     end if
 13:    𝑆 ← 𝑆 ∪ {𝑅 _𝑈 𝑁 𝐼𝑇𝑖 }                                                             • Syntactic Errors during Runtime. SmartC2Rust runs test cases
 14:    𝑒𝑟𝑟𝑜𝑟 ← compile (𝑆 )                                                                 through the translated Rust code and records runtime errors
 15:    𝑐𝑜𝑚𝑝𝑖𝑙𝑒 _𝑐𝑜𝑢𝑛𝑡 ← 0
 16:     while 𝑐𝑜𝑚𝑝𝑖𝑙𝑒 _𝑒𝑟𝑟𝑜𝑟 ≠ ∅ and 𝑐𝑜𝑚𝑝𝑖𝑙𝑒 _𝑐𝑜𝑢𝑛𝑡 < 𝐶𝑂𝑀𝑃𝐼 𝐿𝐸 _𝑀𝐴𝑋 do                      (runtime_error in Algorithm 1). Examples of such errors are like
 17:         𝐷𝑒𝑝𝑅 ← parse (𝑆 ) , where 𝐷𝑒𝑝𝑅 : Rust metadata                                  array index out of bounds leading to a panick.
 18:         𝑀 ← ask_repair (𝑆, 𝐷𝑒𝑝𝑅 ) , where 𝑀 : Modification set
 19:          for (𝑅 _𝑈 𝑁 𝐼𝑇 , 𝑟𝑒𝑣𝑖𝑠𝑖𝑜𝑛 _𝑐𝑜𝑛𝑡𝑒𝑛𝑡 ) ∈ 𝑀 do                                 • Runtime Behavior Differences. SmartC2Rust runs test cases on
 20:             𝑆 ← apply_modification (𝑆, 𝑅 _𝑈 𝑁 𝐼𝑇 , 𝑟𝑒𝑣𝑖𝑠𝑖𝑜𝑛 _𝑐𝑜𝑛𝑡𝑒𝑛𝑡 )
 21:          end for
                                                                                             both the original C and translated Rust code to capture differ-
 22:         𝑐𝑜𝑚𝑝𝑖𝑙𝑒 _𝑒𝑟𝑟𝑜𝑟 ← compile (𝑆 )                                                   ences in runtime behavior. These discrepancies are represented
 23:         𝑐𝑜𝑚𝑝𝑖𝑙𝑒 _𝑐𝑜𝑢𝑛𝑡 ← 𝑐𝑜𝑚𝑝𝑖𝑙𝑒 _𝑐𝑜𝑢𝑛𝑡 + 1
 24:     end while                                                                           as function execution flow information, as shown in Fig. 3.
 25:     for 𝑅 _𝑈 𝑁 𝐼𝑇 ∈ 𝑀 do                                                             • Semantic Errors during Runtime. SmartC2Rust runs test cases
 26:         𝐷𝑒𝑝𝐶 ← map_correspondence (𝑅 _𝑈 𝑁 𝐼𝑇 , 𝐶 _𝑈 𝑁 𝐼𝑇 , 𝐷𝑒𝑝𝐶 )
 27:     end for                                                                             through the translated Rust code and records semantic (assertion)
 28: end for                                                                                 errors (semantic_error in Algorithm 1). Assertion error logs are
 29: while 𝑐𝑜𝑚𝑝𝑖𝑒 _𝑒𝑟𝑟𝑜𝑟 ≠ ∅ and 𝑠𝑒𝑚𝑎𝑛𝑡𝑖𝑐 _𝑒𝑟𝑟𝑜𝑟 ≠ ∅ and 𝑟𝑢𝑛𝑡𝑖𝑚𝑒 _𝑒𝑟𝑟𝑜𝑟 ≠ ∅ and
     𝑟𝑒𝑝𝑎𝑖𝑟 _𝑐𝑜𝑢𝑛𝑡 < 𝑅𝐸𝑃𝐴𝐼𝑅 _𝑀𝐴𝑋 do                                                          directly included for later repairs.
 30:     𝑀 ← ask_repair (𝑆 )
 31:     for (𝑅 _𝑈 𝑁 𝐼𝑇 , 𝑟𝑒𝑣𝑖𝑠𝑖𝑜𝑛 _𝑐𝑜𝑛𝑡𝑒𝑛𝑡 ) ∈ 𝑀 do                                      The compilation repair (Lines 13–28) fixes compilation errors after
 32:         𝑆 ← apply_modification (𝑆, 𝑅 _𝑈 𝑁 𝐼𝑇 , 𝑟𝑒𝑣𝑖𝑠𝑖𝑜𝑛 _𝑐𝑜𝑛𝑡𝑒𝑛𝑡 )                   each unit. The semantic repair (Lines 29–37) fixes all error types
 33:     end for
 34:    𝑐𝑜𝑚𝑝𝑖𝑙𝑒 _𝑒𝑟𝑟𝑜𝑟 ← compile (𝑆 )                                                     after all units are translated and tested.
 35:    𝑠𝑒𝑚𝑎𝑛𝑡𝑖𝑐 _𝑒𝑟𝑟𝑜𝑟, 𝑟𝑢𝑛𝑡𝑖𝑚𝑒 _𝑒𝑟𝑟𝑜𝑟 ← run_test (𝑆 )
 36:    𝑟𝑒𝑝𝑎𝑖𝑟 _𝑐𝑜𝑢𝑛𝑡 ← 𝑟𝑒𝑝𝑎𝑖𝑟 _𝑐𝑜𝑢𝑛𝑡 + 1                                                 3.4.2 Iterative Repair. The repair prompt contains the following
 37: end while
 38: return 𝑆                                                                             information: (1) response guidelines (i.e., rules for the repair), (2)
                                                                                          Rust Code, (3) syntactic or semantic errors, (4) directory structure,
                                                                                          and (5) dependencies (i.e., definitions of elements in other modules).
• "current_block_complete": The Rust code fully implements                                Additionally, for semantic repair, the prompt includes (6) function
  the functionality of the original C segment without mocking,                            execution flow information and (7) C code.
  simplifications, or placeholders.                                                          Each repair may span over multiple Rust translation units and
• "no_omission": The Rust code contains no omissions and can                              affect configuration files. Since the error log (e.g., a compilation
  be executed as-is.                                                                      error) contains the paths to the files with errors, SmartC2Rust
                                                                                          localizes all affected files and asks the LLM to repair them with the
3.4     Stage (iii): Feedback-driven Code Repair                                          corresponding contextual metadata.
   Stage (iii) repairs the Rust code output from Stage (ii) by
addressing syntactic and semantic errors. Algorithm 1 outlines this                       4   Implementation and Experimental Setup
repair process, integrated with translation and quality refinement                        This section describes the implementation and experimental setup.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                    Momoko Shiraishi, Yinzhi Cao, and Takahiro Shinagawa


Table 2: Statistics of our benchmark dataset, intermediate                                    To implement the semantic equivalence described above, for
results (# Units and Unit size), testcases, and the Rust code                              programs that are not standalone, we rewrite the developer-written
translated by SmartC2Rust. Note that although time contains                                test cases even if they exist. Specifically, the method involves three
20,436 Lines of Code (LoC), only 2,007 LoC are active code                                 steps: (i) generates a C test program that calls the (library) function
and others are dead code, e.g., .h files that are never included.                          and displays the result. (ii) Translates both the library function and
                                                                                           the test program to Rust. (iii) Uses the shell script to compare the
Program                                       C Stat.                         Rust Stat.   outputs of both versions. In SmartC2Rust, tests are executed not
                        LoC # Logic # Units        Unit Size # Test   Type          LoC    by the LLM itself, but by the software program of SmartC2Rust.
                             Blocks                                                        Therefore, print funcatations are needed to inform the LLM of the
bst                        100    10     4 143.00 ± 0.00         4 Built-in          130   execution results.
buffer                     527    59     8 255.50 ± 5.50        17 Built-in          741
ht                         717    95    36 97.22 ± 50.53         6 Built-in          632   Setup.      Our experiment is conducted on an Azure Stan-
urlparser                  469    38     8 270.00 ± 170.00      41 Built-in          497   dard_L8as_v3 virtual machine with 512 GB of memory running
SipHash [47]             3,189    63    23 406.12 ± 362.83      20 Created           671
sds [44]                 1,943   117    15 245.50 ± 173.08      24 Built-in        1,662   Ubunutu 22.04 LTS. In our experiment, the default segment size
rgba                       497    33     8 241.50 ± 159.50       5 Built-in          747   parameter is set as 400 lines. Note that since segmentation is done
quadtree                   513    42     8 188.00 ± 84.00        4 Built-in          515   without breaking logical boundaries, not all unit sizes are exactly
qsort                       69    14     8 59.50 ± 29.50        20 Provided          164
mark-sweep [37]            244    25     4 266.00 ± 0.00         5 Built-in          381   400 lines. To reduce probabilistic behavior, the temperature [9] is set
avl                        181    13     4 278.00 ± 0.00         2 Built-in          297   to 0, and max_tokens parameter [9], which indicates the maximum
which                    3,530   442    30 343.78 ± 340.85      20 Created         2,234
Tinyhttpd [52]             418    39     8 234.50 ± 196.50       3 Built-in          354
                                                                                           output tokens, is set to 8,192.
tiny-AES-c [51]            719    65     8 419.50 ± 119.50       3 Built-in          738   Dataset. Table 2 shows our curated dataset of 21 C programs:
time                    20,436   812    80 90.05 ± 101.74        3 Built-in        1,913
c4 [13]                    502    12     4 325.00 ± 0.00         2 Built-in          990   10 from top GitHub repositories (100–2,000 lines, 500+ stars,
yank [56]                  465    45     4 496.00 ± 0.00        22 Provided          578   non-interactive) and 11 from prior works [23, 29, 45, 59]. The
su-exec [48]               130    12     4 114.00 ± 0.00        20 Created           213   GitHub programs are: SipHash, sds, mark-sweep, Tinyhttpd,
FastestWebsiteEver [26]    188    21     4 162.00 ± 0.00         5 Built-in          129
mcrcon [38]                717    50     4 664.00 ± 0.00        30 Created           589   FastestWebsiteEver, c4, yank, su-exec, tiny-ASE-c, and
zopfli                   3,545   464    44 271.53 ± 227.24      20 Created         4,131   mcrcon. “# Logic Blocks” denotes the number of parsed elements,
                                                                                           “# Units” the number of translation units, “# Unit Size” the average
                                                                                           size of the units, and “# Test” the number of test cases (based
                                                                                           on the number of assertions). Test “Type” indicates the source:
Implementation. Our implementation contains 38,341 Lines                                   “built-in” (from original repository), “created” (manually developed
of Python Code. The default LLM is based on Claude 3.7 Son-                                with expected values/behaviors), or “provided” (from third-party
net (claude-3-7-sonnet-20250219) [8]. SmartC2Rust’s parser uses                            repositories1 ). Note that when verifying non-standalone Rust
libclang [16], a C interface to the Clang compiler and provides                            programs using C test cases, rewriting is necessary regardless of
access to Abstract Syntax Tree (AST) of the target C code.                                 whether LLMs are used, so that the translated Rust program can be
   Response guidelines specify the format for LLM responses. To                            built and tested. In this situation, we have two choices: performing
enable autonomous corrections, we define an API with three modes,                          rewriting like Laertes, or excluding such programs from the target
requiring the LLM to select one in each response: (i) read_data:                           and testing only command line tools instead, as C2SaferRust does.
reads the content of specified files. If necessary, specific line ranges                   We adopt the former approach to enable comparison with previous
can be designated, (ii) modify_data : modifies or deletes line ranges                      studies.
in specified files, and (iii) execute_command : executes shell                             Baselines. In the evaluation, we adopt the following four
scripts or other commands.                                                                 baselines as a comparison with SmartC2Rust.
   Our evaluation procedure includes two shell scripts to automate                         • C2Rust [32]. C2Rust is a rule-based approach developed by
building and test execution in a feedback loop. These scripts consist                        Galois and Immunant for C-to-Rust translation.
of: (1) a script for building the translated Rust program, and (2) a
                                                                                           • Crown [59]. Crown is a rule-based ownership analysis tool for
script for running tests and validating semantic equivalence. The
                                                                                             unsafe Rust code with the functionality of refactoring.
shell script for verifying semantic equivalence in (2) records the
                                                                                           • C2SaferRust [39]. C2SaferRust is a tool combining the strengths
results from the C golden implementation in advance and compares
                                                                                             of both rule- and LLM-based approaches. It first adopts C2Rust
them with the actual execution results of the Rust program. This
                                                                                             for conversion and then utilizes LLMs for refinement.
approach is adopted due to two considerations. First, executing tests
                                                                                           • Laertes [23]. Laertes is a rule-based translation tool focusing
directly within the C program would necessitate FFI calls to invoke
                                                                                             on raw pointers in translated Rust code.
Rust functions from C, resulting in C-ish type representations for
the translated Rust functions. Second, this external verification                             Additionally, Syzygy [45] performs C-to-Rust translation using
approach enables LLMs to provide feedback during the repair                                LLMs with formal equivalence verification methods. Although
cycle based on a formalized response format. The shell script is                           Syzygy did not publicly release their translation code itself, the
specifically designed to display test numbers, execution results,                          translated Rust code for their target program (zopfli) is available.
and expected values in a structured manner, allowing LLMs to                               1 E.g., qsort tests: https://github.com/bradtraversy/traversy-js-challenges/blob/main/
address multiple test cases sequentially rather than attempting to                         09-sorting-algorithms/11-quick-sort-implementation/quick-sort-test.js; yank tests:
fix multiple failed tests simultaneously.                                                  https://formulae.brew.sh/formula/yank
SmartC2Rust                                                                                                               ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


Table 3: [RQ1] Comparison of SmartC2Rust with baseslines on safety-related metrics (uLoC (↓): Unsafe Lines of Code, #RawDecl
(↓): Number of Raw Pointer Declarations, and #RawDeref (↓): Number of Raw Pointer Dereferences). The numbers under
#RawDecl and #RawDeref have the format of N (M), where N is the output from the raw pointer counter of C2SaferRust, and M
is the output from the counter of Crown. Note that “-” means that the code cannot be complied and thus C2SaferRust fails to
count the number of raw pointer declarations or references. The light blue highlighting ( ) denotes the lowest value.

                             C2Rust                         Crown                       Laertes                       C2SaferRust                    SmartC2Rust
 Program
                   uLoC #RawDecl #RawDeref uLoC #RawDecl #RawDeref uLoC #RawDecl #RawDeref uLoC #RawDecl #RawDeref uLoC #RawDecl #RawDeref
 bst                  96     10(9)     29 (26)     61      4(4)       7(7)      106    10(10)      29(29)      68       9(9)     26(26)       0        0(0)        0(0)
 buffer             1,006    61(39)    82(56)     780     19(57)     19(70)     816      (58)       (70)      410      41(38)    47(36)       0        0(0)        0(0)
 ht                 1,117    77(32)   126(31)     178      (19)       (43)     1,017   77(77)      120(87)    773      55(28)    85(22)       0        0(0)        0(0)
 urlparser          1,035    79(22)    60(42)    1,967     (78)       (42)     1,924   74(79)       2(60)     633      81(20)     51(1)       0        0(0)        0(0)
 SipHash             598     12(0)      70(0)     598      12(0)     70(0)     1,318   12(12)       70(0)     516       12(0)     55(0)       0        0(0)        0(0)
 sds                2,271   142(89)   209(22)    2,276     (74)       (20)     2,270    (130)       (86)        -         -         -         0        0(0)        0(0)
 rgba                994     21(21)    78(64)     604     16(21)     66(64)     573    21(21)      78(64)     263       5(5)      8(6)        0        0(0)        0(0)
 quadtree            905     47(38)   209(104)   1,664    33(47)    114(156)    905    47(38)     209(104)    387      35(35)    106(73)      0        0(0)        0(0)
 qsort               156     4(11)      10(8)     156      (11)        (8)      131     2(13)       6(8)       19       1(1)      6(0)        0        0(0)        0(0)
 mark-sweep          278     27(24)    64(49)     278      (21)       (38)      278    27(24)      64(49)     130      20(20)    44(42)       0        0(0)        0(0)
 avl                 159     17(16)    83(75)      84      5(13)     8(50)      215    17(17)      83(79)     159      16(16)    80(74)       0        0(0)        0(0)
 which              1,666     (68)       (81)    1,669     (29)       (47)     1,666       -          -         -         -         -        24        0(0)        0(0)
 Tinyhttpd          1,742    13 (3)    16 (0)    1,742      (3)        (0)     1,180   12(12)       16(7)    1,520      10(1)     13(0)       0        0(0)        0(0)
 tiny-AES-c         1,522    36(36)   126(100)   1,517    30(30)     47(20)    1,176   36(36)     126(100)    791      14(14)    35(10)       0        0(0)        0(0)
 time               1,313    59(49)   171(97)    1,313     (21)       (86)     1,234     (55)       (97)      941      45(33)    140(66)     121       0(0)        0(0)
 c4                 1,685    41(9)     319(9)    1,681      (9)        (9)     1,690     (34)       (60)     1,727     48(45)    214(69)      0        0(0)        0(0)
 yank                770     14(9)      47(8)     764       (6)        (8)      729      (12)       (11)      709       11(6)     39(0)      26        0(0)        0(0)
 su-exec             145      9(0)      15(0)     145       (0)        (0)      119      9(9)       15(8)     134       9(0)      15(0)       0        0(0)        0(0)
 FastestWebsiteEver 203       5(1)       9(1)     203       (1)        (1)      173       (5)        (7)      197       6(2)      8(2)        0        0(0)        0(0)
 mcrcon            12,981    21(15)    33(17)    12,981     (5)       (14)     1,325   21(21)      33(24)    8,648     15(15)    28(24)       0        0(0)        0(0)
 Δ C2Rust            -         -         -       +0.1%    (-8.6%)   (-13.5%)   -38.5% (+48.9%)    (+30.5%)   -43.8%    -37.7%     -43.1%    -99.4%   -100.0%     -100.0%



Therefore, we also conduct additional comparisons with Syzygy                          5.1       RQ1: Memory Safety
for zopfli.                                                                            Table 3 presents the result of safety metrics for each program.
Evaluation Metrics. We compare SmartC2Rust with baselines                              The bottom row (Δ C2Rust) shows the average change rate from
based on two metrics, safety and semantic equivalence.                                 C2Rust. SmartC2Rust shows significant improvements over existing
   First, the safety metric adopts three sub-metrics: (i) UnSafe Line                  methods. Compared with C2Rust, on average, it reduces unsafe
of Code (uLoC), which measures the lines of code inside unsafe                         LoC from 1,550 to 8.14 (a 99.4 % reduction), and raw pointer
blocks and functions, (ii) Number of raw pointer declarations                          declarations and dereferences are significantly reduced across all
(#RawDecl), i.e., the frequency of *mut T and *const T raw pointer                     programs. This already outperforms Crown, which achieves -0.1%,
type declarations, and (iii) Number of raw pointer dereferences                        8.6%, 13.5% reductions, Laertes, which manages 38.5%, -48.9%, and
(#RawDeref), i.e., the count of operations where raw pointers are                      -30.5% reductions, and C2SaferRust, which achieves 43.8%, 37.7 %,
dereferenced. We use counters from both C2SaferRust (counts                            43.1 % reductions respectively. We observed that in Crown, Laertes,
mutable and immutable pointers in compilable code) and Crown                           and C2SaferRust, the metrics increased rather than decreased for
(counts only mutable pointers) for comprehensive comparison.                           several programs. SmartC2Rust demonstrates a reduction in all
   The semantic equivalence metric adopts three sub-metrics: (i)                       metrics across every program, and even when unsafe lines are exist,
number of errors during the compilation stage, (ii) test case pass                     it is limited to just 8.14 lines on average.
rate and (iii) ratio of C macros remaining in the translated code.                         We also measured unsafe LoC for the moment before the LLM
Specifically, we measure the number of Rust variables which are                        self-refines the code in stage (ii). We then observed that the
originally C macro variables, Rust macro functions, and macros                         unsafe LoC is decreased in 11.8% on average (standard deviation
used for conditional compilation.                                                      93.9%) at the moment when the LLM quality-refines its code. For
                                                                                       7 programs (which, ht, sds, time, FastestWebsiteEver, mcrcon
5   Evaluation                                                                         and su-exec), the uLoC decreases. For example, the uLoC of which
Our evaluation aims to address the following research questions:                       decreased from 843 to 53, and that of FastestWebsiteEver fell
                                                                                       from 97 to 0 - all showing reduction rates exceeding 90%. In
• RQ1 [Safety]: How is SmartC2Rust effective compare to existing                       SmartC2Rust, although we instruct the LLM to generate safe code
  translation approaches in terms of safety?                                           from the very beginning of the translation process, some unsafe
• RQ2 [Semantics]: How does SmartC2Rust compare with prior                             operations still appear in the initial output. However, these unsafe
  works in terms of semantic equivalence?                                              operations are largely eliminated through the quality-refinement
• RQ3 [Performance+Cost]: What is the performance and cost                             process.
  overhead of SmartC2Rust?                                                                 The safety improvements of SmartC2Rust over C2Rust, Laertes,
• RQ4 [Ablation Study]: How does each strategy of SmartC2Rust                          Crown, and C2SaferRust stem from four concrete advances: (1)
  contribute to the translation success?
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                           Momoko Shiraishi, Yinzhi Cao, and Takahiro Shinagawa


 1 char * pathname = malloc ( sizeof ( char ) ) ;                                     Table 5: [RQ2] Breakdown of semantics-related metrics
 2 // ...                                                                             for SmartC2Rust (#Errors: Number of intermediate errors,
 3 sscanf ( tmp_path , " %[^?|^#] " , pathname ) ; // buf overflow
 4 // ...
                                                                                      Passed: Whether test cases are passed, and %Marco: Percent-
 5 char * tmp_url = strdup ( URL ) ;                                                  age of marcos preserved).
 6 char * protocol = url_get_protocol ( tmp_url ) ;
 7 data -> protocol = protocol ;
 8 // ...                                                                                                         # Intermediate Errors.       Passed   %Macro
                                                                                       Program
 9 free ( tmp_url );
                                                                                                             Compile (%)       Semantic (%)
Listing 4: A snippet of C code with memory safety issues in                            bst                   0       (0.00%)    0    (0.00%)     ✓       100.0%
urlparser [23]                                                                         buffer               99       (0.80%)    24   (0.20%)     ✓       75.0%
                                                                                       ht                   64       (0.82%)    14   (0.18%)     ✓       100.0%
                                                                                       urlparser            48       (0.23%)   158   (0.77%)     ✓       100.0%
 1 fn new ( url : & str ) -> Option < Self > {                                         SipHash               2       (0.20%)    8    (0.80%)     ✓       71.4%
 2   let parsed_url = Url :: parse ( url ) . ok () ?;                                  sds                  78       (0.69%)    35   (0.31%)     ✓       79.2%
 3   // Safe pathname extraction                                                       rgba                 16       (0.80%)    4    (0.20%)     ✓       100.0%
 4   let pathname =                                                                    quadtree             55       (0.90%)    6    (0.10%)     ✓       100.0%
           parsed_url . path () . split ( '? ') . next () ?. to_string () ;            qsort                 6       (1.00%)    0    (0.00%)     ✓          -
 5   // Safe protocol extraction                                                       mark-sweep            2       (0.40%)    3    (0.60%)     ✓       100.0%
 6   let protocol = parsed_url . scheme () . to_string () ;                            avl                   1       (0.07%)    13   (0.93%)     ✓          -
 7                                                                                     which                79       (0.68%)    37   (0.32%)     ✓       33.3%
 8   Some ( Self { // All fields have independent ownership                            Tinyhttpd             0       (0.00%)    4    (1.00%)     ✓       100.0%
 9        pathname ,                                                                   tiny-AES-c           53       (0.90%)    6    (0.10%)     ✓       61.5%
10        protocol , // ... Other fields                                               time                 133      (0.25%)   399   (0.75%)     ✓       61.0%
11   })                                                                                c4                   73       (0.53%)    65   (0.47%)     ✓       100.0%
12 }                                                                                   yank                 101      (0.89%)    12   (0.11%)     ✓       91.7%
                                                                                       su-exec              31       (0.91%)    3    (0.09%)     ✓          -
Listing 5: The safe translation of Listing 4 with SmartC2Rust                          FastestWebsiteEver    3       (0.38%)    5    (0.62%)     ✓       100.0%
                                                                                       mcrcon               74       (0.00%)    2    (1.00%)     ✓       90.9%
                                                                                       zopfli               122      (0.78%)    34   (0.21%)     ✓       68.9%
Table 4: [RQ2] Comparison of semantics-related metrics                                 Total                1,040       -      832         -   20/20      85.2%
(#Errors: total number of compilation errors, %Tests: average
percentage of passed test cases, and %Marco: average percent-
age of correctly translated macros. Values in parentheses                             byte for pathname and performs unbounded writes, preserving the
indicate standard deviation).                                                         buffer overflow risk. It also maintains the same pointer dependency
 Metric         C2Rust       Crown        Laertes     C2SaferRust SmartC2Rust
                                                                                      pattern that leads to use-after-free issues when tmp_url is freed
                                                                                      but protocol continues to be referenced. In contrast, Listing 5
 #Errors (↓)     9          253         13                  9              0
 %Tests (↑) 80 (± 30) % 35 (± 47) % 80 (± 30) %        80 (± 30) %    100 (± 0) %     shows the translation by SmartC2Rust: parsed_url.path() and
 %Marco (↑) 0 (± 0) %    0 (± 0) %   0 (± 0) %          0 (± 0) %    85.2(± 18.6) %   parsed_url.scheme() return string slices (&str type) and the
                                                                                      to_string() method automatically allocates exactly the right
precise C-to-Rust type mapping that preserves safety guarantees,                      amount of memory. The use-after-free issue is eliminated by creat-
(2) flexible replacement of unsafe external functions with safe                       ing independent string values with their own memory allocations.
alternatives, (3) careful management of global variables to prevent
memory violations, and (4) strategic selection of Rust standard                       5.2      RQ2: Semantic Equivalence
libraries that maximize safety while maintaining functionality.                       Table 4 shows the result of semantic-related metrics compared with
    In comparison with Syzygy, their publicly available zopfli code                   baselines for all programs. All Rust code produced by SmartC2Rust
has no unsafe or raw pointers, compiles without errors, and passes                    are error-free, both in terms of compilation and semantics, resulting
all test cases. Regarding macros, SmartC2Rust retains 68 % macros,                    in 0 compilation errors and 100 % passing rate. In contrast, baseline
while Syzygy does not handle macro transformations because they                       approaches have difficulty in compilation and running tests. In
use the unifdef tool to expand conditional macros. While they                         Crown, 10 programs failed to compile, and 2 programs (sds,
show comparable results on some metrics, the authors acknowledge                      which) did not compile with any baseline approaches. C2SaferRust
several limitations that require manual intervention, as discussed                    encountered compilation errors and fixed them during rewriting
in their challenges and future work section. Specifically, struct                     unsafe statements using LLMs, but it is basically relied on the output
definitions and their field relationships must be manually translated                 of C2Rust and does not fix programs that initially fail to compile
due to the need for global program context. Additionally, when                        with C2Rust. For macros, since all of the baseline methods simply
validation tests fail, their approach requires manual edits to the                    expand them, there is no equivalent of them in the translated output.
translated codebase. The authors recognize these limitations and                      On the contrary, in SmartC2Rust, on average, 85.2 % of the original
identify developing more systematic LLM-guided repair techniques                      C macros remain in the transformed Rust code.
as future work. By contrast, SmartC2Rust distinguishes itself by
                                                                                      5.2.1 Fixing Compilation Errors. While SmartC2Rust ultimately
generating the resulting Rust code through LLM-driven automated
                                                                                      generates error-free Rust code, it resolved a total of 1,040 compile
translation and repair.
                                                                                      errors and 832 semantic errors during the iterative repair loop.
5.1.1 A Case Study. Listing 4 shows a case study of memory safety                     Table 5 presents the number of fixed errors for each program.
issues in existing translation works. C2Rust still allocates just one                 While the prevalence of compile errors versus semantic errors
SmartC2Rust                                                                                                    ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


Table 6: [RQ2] Breakdown of encountered compilation errors                         1 # if ( defined ( CBC ) && ( CBC == 1) ) || ( defined ( CTR ) &&
during iterative refinement                                                                ( CTR == 1) )
                                                                                   2 void AES_init_ctx_iv ( struct AES_ctx * ctx , const
                                                                                           uint8_t * key , const uint8_t * iv ) {
    Error Type (Rust’s Error Codes Index)                     Percentage           3    KeyExpansion ( ctx - > RoundKey , key ) ;
                                                                                   4    memcpy ( ctx - > Iv , iv , AES_BLOCKLEN ) ;
    E0308: Type mismatches                                        19.13%           5 }
    E0425: Use of undeclared names                               17.44 %           6 # endif
    E0609: Access to nonexistent fields                           7.47 %
    E0432: Unresolved imports                                     7.21 %           Listing 6: A snippet of tiny-AES-c with conditional
    E0433: Problems with importing named elements                 6.67%
    Others*                                                                        compilation (only SmartC2Rust translates correctly).
    * E0599 (5.60%), E0502 (4.36%), E0616 (3.56%), E0597 (3.11%), E0061 (3.02%),
    E0277 (3.02%), E0428 (2.67%), E0015 (2.31%), E0382 (1.87%), E0106 (1.33%),     1 #[ cfg ( any ( feature = " cbc " , feature = " ctr " ) ) ]
    E0252 (1.33%), E0659 (1.25%), E0119 (1.07%), E0499 (0.89%), E0761 (0.89%),     2 pub fn init_ctx_iv ( ctx : & mut AES_ctx , key : &[ u8 ], iv :
    E0282 (0.71%), E0596 (0.71%), E0560 (0.62%), E0716 (0.62%), E0107 (0.53%),             &[ u8 ]) {
    E0603 (0.36%), E0605 (0.27%), E0505 (0.27%), E9 (0.27%), E0614 (0.18%),        3    key_expansion (& mut ctx . round_key , key ) ;
    E0412 (0.18%), E0506 (0.18%), E0583 (0.18%), E0515 (0.18%), E0658 (0.18%),     4    ctx . iv . copy_from_slice ( iv ) ;
    E0133 (0.18%), E0507 (0.18%)                                                   5 }

                                                                                   Listing 7: Correct translations of Listing 6 by SmartC2Rust.
varies by program, compile errors are on average 1.2 times more
common because modifications made to address semantic issues
can sometimes introduce new compilation errors.                                    correctly include guards and macros purely used for conditional
   Table 6 shows a breakdown of the type of encountered and                        compilation. However, for several cases, we observed inappropriate
fixed compilation errors. The errors are categorized according to                  translation. For example, the LLM interpreted HAVE_CONFIG_H as a
Rust’s error codes index [34]. The vast majority of the errors are                 Cargo feature flag. Since HAVE_CONFIG_H is specifically tied to C’s
related to dependencies. We observed that LLMs tend to initially                   Autoconf/Automake system [49, 50] for checking the presence of
follow instructions less often even when dependency summary                        config.h, and Rust’s build system takes a fundamentally different
information is included in the instruction. In fact, on average, 52.13%            approach to configuration management, the flag seems unnecessary.
of all errors are resolved in the very first iteration, which means                We also observed that C macro functions are replaced with either
the number of errors decreases significantly after the first iteration.            Rust macro functions, ordinary functions or Rust standard library
 This is likely because the first translation instructions contain                 functions.
many translation rules and response guidelines, making it difficult
to follow each rule individually. Since SmartC2Rust consistently                   5.2.4 A Case Study. Listing 6 shows another case study of semantic
provide dependency information within the iterative loop, the LLM                  equivalence issues, especially about macro transformation in
begins to focus on dependency information and utilizes them once                   existing translations. All existing works, including C2Rust, Crown,
the errors occurred. As a result, it prevents repeated compilation                 Laertes, and C2SaferRust, adopts a preprocessor for processing
fails.                                                                             macros, which removed the #if condition at Line 1 of Listing 6,
                                                                                   violating the semantics of the code. Instead, Listing 7 shows the
5.2.2 Fixing Semantics-related Errors. Semantics-related errors                    correct translation by SmartC2Rust, which consolidates the pre-
vary depending on each program, such as incorrect borrowing                        processor conditions using Rust’s #[cfg] attributes. SmartC2Rust
syntax or improper parsing methods, which cause tests to fail.                     enables this conditioned translation because it recognizes macros
SmartC2Rust has the LLM response with the reasoning behind                         (CBC and CBC) during pre-processing of SmartC2Rust scheme, and
the correction method, and we observed that LLMs methodically                      the LLM determines to handle these macros as Cargo features and
address each test case step by step to implement the necessary                     set in Cargo.toml at the very beginning of the translation. During
corrections. By repeating such iterative corrections, SmartC2Rust                  the translation of each unit, SmartC2Rust then applies these feature
eventually achieves test pass rate of 100 % for all the programs.                  flags to the appropriate code sections.
5.2.3 Macro Preservation. Table 5 also shows the percentage of
macros that are correctly translated. We handled a total of 1,061 C                5.3    RQ3: Overhead
macros. Out of these, 50 are macro functions, and 164 are macros                   We evaluate two types of overhead: (1) performance in time
used for conditional compilation. The two GNU packages, which                      (seconds), iterations, and number of tokens and chats, and (2) cost
and time contain a large number of conditional macros (88 and 47                   in US dollars. Table 7 shows the performance and cost for each
respectively) due to their emphasis on portability.                                program.
   C macro variables are correctly replaced with Rust const vari-                  Performance. As shown in the table, on average, SmartC2Rust
ables. Of the conditional macros, 26% are replaced with Rust Cargo                 requires a total of 187 user and LLM chats, 10,456 K input tokens,
macros. Then, we observed that 29% of conditional macros have no                   116 K output tokens, and 2,637 seconds to translate. This is
corresponding equivalents in Rust. The representative is include                   because SmartC2Rust employs an interactive approach where the
guards of C macros. For header guards, these guards can typically                  LLM selects the mode type and iteratively refines the code, which
be identified heuristically through naming conventions (ending in                  inherently demands a moderate number of chat interactions and
_H) [12], as there is no strict definition to distinguish them from                processing time. The input tokens are particularly long because
other conditional directives using #ifndef. The LLM identified                     SmartC2Rust sends back the file that the LLM requests to modify
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                               Momoko Shiraishi, Yinzhi Cao, and Takahiro Shinagawa


          Table 7: [RQ3] Performance overhead and cost                                     it with unimplemented()!, or assumes it exists in an external
                                                                                           package. Such bold code generation ultimately leads to a problem
Program               #Chats
                                  #Iterations
                                                      Time [s]
                                                                 #Token [K]        Cost    where errors are repeated and compilation fails to converge.
                                Comp. Semant.                         In    Out [USD]      Contextual Dependency Summarization. In this study, we
bst                        19        1           1    149.19    182.19 17.75    0.81       omitted these contextual summaries from our translation process
buffer                    103        6           3 1,106.81 3,899.12 78.51 12.87           and Table 8 shows that the success rate dropped to just 32.3%. The
ht                        265      140           4 1,984.37 8,597.70 147.71 28.01          Rust compiler primarily reveals dependency-related errors (E0308,
urlparser                 112        7          11     1,263 4,454.94 62.98 14.31
SipHash                   177       50           0 1,623.81 6,679.59 184.40 22.80          E0599, E0425, E0432) and field access violations (E0609, E0616).
sds                       243       15           7 2,789.64 21,361.38 91.06 65.45          Without contextual dependency feedback, translators are difficult
rgba                      127       15           6 1,402.35 4,655.77 74.98 15.09
quadtree                  447       17          93 10,235.62 41,768.83 213.45 128.51
                                                                                           to identify and resolve interface inconsistencies within the limited
qsort                      20        5           0 2,380.37     183.81 13.93    0.76       number of compilation attempts.
mark-sweep                 47        1           3    325.12 1,046.67 25.82     3.53       Mode-based API. In this study, we let the conversion to be
avl                       113        6          12 1,250.81 5,503.83 70.22 17.56
which                     472      141          19 4,014.03 24,989.98 306.60 79.57         performed sequentially in segments without modifying the other
Tinyhttpd                  62        5           4    463.66 1,112.14 36.80     3.89       units/files. Table 8 shows that the compilation success rate is 12.4%.
tiny-AES-c                118       15           0 3,702.23 8,308.98 136.60 26.98          The most critical case where compilation becomes impossible is
time                      697      448          89 10,621.62 35,032.16 358.88 110.48
c4                        100        3           0 1,178.09 6,122.78 103.65 19.92          when the LLM needs external crates by modifying Cargo.toml.
yank                       98       16           0 1,229.34 9,757.17 72.83 30.36           The crates are for example, lazy_static [17] and once_cell [18].
su-exec                    36        6           0    261.93    909.18 18.96    3.01
FastestWebsiteEver         26        3           0    154.95    400.36 16.15    1.44
                                                                                           If flexible modifications for these other units/files are not permitted,
mcrcon                     74        6           1    613.12 2,737.58 51.62     8.99       the errors will permanently remain unresolved.
zopfli                    590       42          23 8,642.67 31,886.72 358.88 101.04        Flow-based Localization in Semantic Repair. In this study, we
Average                187.90     45.14     13.14      2,637.75 10,456.71 116.27   33.12   omitted function execution flow feedback. Table 8 shows that the
                                                                                           average semantic equivalence success rate is 23%. LLMs with poor
                     Table 8: [RQ4] Ablation study                                         localization abilities repeat the same code fixes in modify_data
                                                                                           mode when handling compile/semantic errors, or misdiagnose
                                                                                           problems as permission/lock file issues, proposing cleanup and
   Strategy                       Compilation Success %            Test Case Pass %
                                                                                           rebuild commands in execute_command mode instead of addressing
   Random Order                                          28.5%                     -
   w/o Contextual Summary                                32.3%                     -
                                                                                           actual code defects.
   Fixed File Modification                               12.4%                     -       Other LLMs beyond Claude. We also tested the programs using
   w/o Flow comparison                                       -                 23.3%       GPT-4o (gpt-4o-2024-08-06) [4] and Gemini Pro 1.5 (gemini-pro) [3].
   SmartC2Rust                                         100.0 %              100.0 %        GPT-4o achieved a compilation success rate of 34.3 %, while
                                                                                           Gemini Pro 1.5 had a lower rate of 12.4 %. GPT-4o typically
                                                                                           demonstrates consistent error patterns, whereas Gemini Pro 1.5
when making corrections, along with line number information to                             frequently produces inappropriately formatted responses. This
ensure that the LLM correctly identifies the range to be revised.                          performance discrepancy can be attributed to the differing levels
Cost. Claude 3.7 Sonnet’s pricing is based on token usage. The                             of coding proficiency among LLMs, where Claude is superior to its
cost for processing input tokens is 3 US dollars per million tokens                        competitors [5]. Open-source smaller LLMs usually have even more
(MTok), while the cost for output tokens is 15 US dollars per million                      constrained context window sizes, making them prone to exceeding
tokens (MTok) [7]. Therefore, as shown in Table 7, the target                              the context limit. We would expect to reduce SmartC2Rust’s
program size relates with the cost, but it also correlates with the                        context window and increase the iterations to work with smaller
number of chat requests/responses and iteration count. On average,                         open-source models. We will leave this as our future work.
the translation requires 33 USD. It is reasonable considering that
users get high-quality Rust code without any unsafe statements.                            6    Discussions and Limitations
5.4      RQ4: Ablation Study                                                               We discuss a few commonly issues and SmartC2Rust’s limitations.

We conducted an ablation study to understand different strategy                            Scalability. We also tested a large program with 12,256 lines
adopted by SmartC2Rust. We use three C programs, urlparser,                                of code [14]. It compiled successfully, but the semantic repair
sds, and which. Our evaluation is based on the following two                               encountered an infinite loop undetectable by the iterative process.
metrics: (i) compilation success percentage (%), i.e., the average                         Note that the compilation repair required 4,213 chats, costing 1,451
percentage of LoC that successfully compiled out of the total LoC,                         USD and taking 27 hours. After manual fixes and LLM iterations,
and (ii) test case pass rate, i.e., the average proportion of successful                   24 % of the test cases passed, but we observed that it remains
test cases out of all test cases.                                                          challenging to push forward because the LLM is simplifying and
Definition-Order Translation. In this study, we make the                                   rewriting the code just to make the test cases pass. As a future
order of the files translation as random. Table 8 shows that                               work, it is important to design instructions that do not oversimplify
in the random order, the success rate is 28.5%. When an LLM                                during semantic repair.
calls a function without knowing its definition, we observed that                          Testing of different macro combinations. Regarding condi-
it takes one of three approaches. The LLM either guesses the                               tional compilation with macros, SmartC2Rust does not cover all
implementation based on the function name and context, replaces                            the combination of macro definitions. For instance, with n macro
SmartC2Rust                                                                                                 ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


variables MACRO1, MACRO2, ..., MACRO_n, there are numerous possible       though the authors identify developing more systematic techniques
states depending on whether each macro is defined and what values         for LLM-guided translation and repair as future work.
they hold. However, this limitation exists in the original C code as         LLM-based translation for other language pairs. Some
well—even with available macros, developers rarely test all possible      LLM-based translators [10, 20, 31, 53, 55, 57] other than C to Rust
conditional compilation paths. Nevertheless, testing compile and          have been proposed. For example, Ibrahimzada [31] suggested a
semantic repair under key macro condition combinations would              method-level, partial translation approach from Python to Java code
generate more sustainable Rust code.                                      that takes into account the size limit of context windows. Zhang
LLM’s awareness of the target C program during training.                  et al. [58] converts Go code to Rust, which involves different lan-
SmartC2Rust instructs LLMs to translate only within the provided C        guage paradigms and safety considerations compared to C-to-Rust
code range, even if they recognize the entire program. This restric-      translation. These concurrent works, while relevant to the broader
tion maintains our segmented translation approach but may prevent         domain of automated language translation, tackle distinct problems
optimizations that could benefit from the LLM’s whole-program             with different technical constraints and evaluation methodologies
understanding. Future work should explore methods to harness              than SmartC2Rust approach.
LLMs’ broader knowledge while preserving consistency across code          Rule-based C-to-Rust translation. A representative rule-based
segments.                                                                 translation tool is the C2Rust Transpiler [32], which uses predefined
Adaptation for languages other than C. Although substantial               rules to automatically translate C code into Rust. However, C2Rust
engineering work remains, the core principles of our methodol-            generates code with excessive unsafe and unidiomatic Rust code.
ogy—code segmentation and feedback-driven iterative loops—are             It struggles with pointer handling, external libraries, and perfor-
language-agnostic and can be extended to other programming                mance optimization, requiring significant manual refactoring. Thus,
languages to tackle similar fundamental challenges, including             several rule-based translation methods [23, 24, 28, 29] have been
LLM context window constraints, syntactic error resolution, and           proposed to achieve better conversions beyond C2Rust, such as
semantic correctness verification.                                        replacing unsafe raw pointers with safe references [23, 24, 28],
                                                                          handling lock APIs [28], and focusing on tuples and Option/Result
7   Related Work                                                          types [29]. Specific targets can be reliably transformed using the
LLM-based C-to-Rust translation. Pan et al. [41] analyzed trans-          translation mapping, but the translated code still contains various
lation patterns of LLMs across multiple language pairs, including C       unsafe. Moreover, context-dependent translation is not feasible.
to Rust. They demonstrated that compilation errors persist even in        Program repair. Many studies proposed LLM-based program
attempts to translate small C programs. Yang et al. [54] presented a      repair schemes [11, 21, 33, 46, 60]. Particularly, Deligiannis et
formal verification framework for validating semantic equivalence         al. [21] demonstrated an approach for fixing Rust compilation
following the translation of target C programs via LLMs. Eniser           errors using formatted logs. While they have a similar iterative
et al. [25] also utilized LLMs for translation and applied fuzzing        correction process, SmartC2Rust distinctively supports multi-file
techniques to verify equivalence. However, both approaches can            modifications through LLM mode selection and incorporates
convert only C programs consisting of several hundred lines of code       additional data retrieval and command execution capabilities.
into compilable Rust code: Yang et al. [54] fails to compile code
with 158 lines and Eniser et al. [25] can handle only code between        8    Conclusion
150 and 597 lines. Li et al. [36] investigated translation patterns       This paper proposes a method, called SmartC2Rust, for translating C
among human participants, LLM-based translators, and rule-based           code into Rust using a large language model (LLM). Our key insight
translators. They found the state-of-the-art LLM-based translators        is an iterative refinement process in which LLMs progressively
produce idiomatic safe Rust snippets yet fail to generate compilable      improve Rust code by incorporating feedback on semantic and mem-
code due to type inconsistencies when merging independently               ory safety issues until the code successfully passes test cases. We
translated functions.                                                     evaluated SmartC2Rust against 21 programs up to approximately
   C2SaferRust [40] translated 7 real-world programs by using an          3,000 lines of code and showed that SmartC2Rust outperforms
LLM to eliminate unsafe statements created by C2Rust. However,            prior works, including C2Rust, Crown, Laertes, and C2SaferRust
this approach exhibits two main limitations: it cannot translate          in terms of memory safety, i.e., reducing unsafe statements by
non-function code elements such as structure definitions, nor             99.4%, and semantic equivalence, i.e., improving test case pass rates
can it substitute C FFI function calls with safe Rust equivalents.        by 11.25%. SmartC2Rust also achieves 85.2% preservation of the
Consequently, in some cases, the translator output may have more          semantic meaning of C macros.
unsafe lines of code or raw pointers compared to C2Rust.
   Hong et.al [30] translated C function signatures into Rust using       References
LLMs, but only fixed type compilation errors, excluding functions          [1] 2025. smartC2Rust Demo server. https://github.com/momo-trip/SmartC2Rust/
with large bodies from translation. Other compilation errors remain            tree/main/demo.
                                                                           [2] 2025. smartC2Rust repository. https://github.com/momo-trip/SmartC2Rust.
uncorrected, and the semantic equivalence is not resolved.                 [3] Google AI. 2025. Gemini 2.0 Pro. https://deepmind.google/technologies/gemini/
   While Syzygy [45] also translated C code to Rust, it has limita-            pro/.
tions including lack of iterative repair process, translation of struct    [4] Open AI. 2025. Hello GPT-4o. https://openai.com/index/hello-gpt-4o/.
                                                                           [5] aider. 2025. Aider LLM Leaderboards. https://aider.chat/docs/leaderboards/.
definitions, and support for macro translation. These functions            [6] Anthropic. 2024. Context window. https://support.anthropic.com/en/articles/
are currently implemented manually in the translated Rust code,                7996848-how-large-is-claude-s-context-window.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                    Momoko Shiraishi, Yinzhi Cao, and Takahiro Shinagawa


 [7] Anthropic. 2025. Anthropic API Pricing. https://www.anthropic.com/                    [39] Vikram Nitin, Rahul Krishna, Luiz Lemos do Valle, and Baishakhi Ray. 2025.
     pricing#anthropic-api.                                                                     C2SaferRust: Transforming C Projects into Safer Rust with NeuroSymbolic
 [8] Anthropic. 2025.         Claude 3.7 Sonnet and Claude Code.                https://        Techniques. arXiv:2501.14257 [cs.SE] https://arxiv.org/abs/2501.14257
     www.anthropic.com/news/claude-3-7-sonnet.                                             [40] Vikram Nitin, Rahul Krishna, Luiz Lemos do Valle, and Baishakhi Ray. 2025.
 [9] Anthropic. 2025. Strengthen guardrails. https://docs.anthropic.com/en/docs/test-           C2SaferRust: Transforming C Projects into Safer Rust with NeuroSymbolic
     and-evaluate/strengthen-guardrails/reduce-latency.                                         Techniques. arXiv preprint arXiv:2501.14257 (2025).
[10] Manish Bhattarai, Javier E Santos, Shawn Jones, Ayan Biswas, Boian Alexandrov,        [41] Rangeet Pan, Ali Reza Ibrahimzada, Rahul Krishna, Divya Sankar, Lam-
     and Daniel O’Malley. 2024. Enhancing Code Translation in Language Models                   bert Pouguem Wassi, Michele Merler, Boris Sobolev, Raju Pavuluri, Saurabh
     with Few-Shot Learning via Retrieval-Augmented Generation. arXiv preprint                  Sinha, and Reyhaneh Jabbarvand. 2024. Lost in translation: A study of bugs
     arXiv:2407.19619 (2024).                                                                   introduced by large language models while translating code. In Proceedings of
[11] Islem Bouzenia, Premkumar Devanbu, and Michael Pradel. 2024. Repairagent: An               the IEEE/ACM 46th International Conference on Software Engineering. 1–13.
     autonomous, llm-based agent for program repair. arXiv preprint arXiv:2403.17134       [42] Brent Pappas and Paul Gazzillo. 2024. Semantic Analysis of Macro Usage for
     (2024).                                                                                    Portability. In Proceedings of the 46th IEEE/ACM International Conference on
[12] c-code style. 2025. Recommended C style and coding rules. https://github.com/              Software Engineering. 1–12.
     MaJerle/c-code-style/blob/main/README.md#headersource-files.                          [43] The Rust Reference. 2025. Conditional compilation. https://doc.rust-lang.org/
[13] c4. 2025. c4. https://github.com/rswier/c4.                                                reference/conditional-compilation.html.
[14] cflow. 2025. cflow. https://www.gnu.org/software/cflow/.                              [44] sds. 2025. sds. https://github.com/antirez/sds.
[15] Lingjiao Chen, Matei Zaharia, and James Zou. 2023. Frugalgpt: How to use large        [45] Manish Shetty, Naman Jain, Adwait Godbole, Sanjit A Seshia, and Koushik Sen.
     language models while reducing cost and improving performance. arXiv preprint              2024. Syzygy: Dual Code-Test C to (safe) Rust Translation using LLMs and
     arXiv:2305.05176 (2023).                                                                   Dynamic Analysis. arXiv preprint arXiv:2412.14234 (2024).
[16] clang 20.0.0git. 2025. libclang: C Interface to Clang. https://clang.llvm.org/        [46] André Silva, Sen Fang, and Martin Monperrus. 2023. Repairllama: Efficient
     doxygen/group__CINDEX.html.                                                                representations and fine-tuned adapters for program repair. arXiv preprint
[17] crates.io. 2025. lazy_static v1.5.0. https://crates.io/crates/lazy_static.                 arXiv:2312.15698 (2023).
[18] crates.io. 2025. once_cell v1.21.1. https://crates.io/crates/once_cell.               [47] SipHash. 2025. SipHash. https://github.com/veorq/SipHash.
[19] United States Cybersecurity, Infrastructure Security Agency, United States Na-        [48] su exec. 2025. su-exec. https://www.anthropic.com/pricing#anthropic-api.
     tional Security Agency United States Federal Bureau of Investigation, Australian      [49] GNU Operating System. 2025. Autoconf. https://www.gnu.org/software/
     Signals Directorate’s Australian Cyber Security Centre, Canadian Centre for                autoconf/.
     Cyber Security, United Kingdom National Cyber Security Centre, New Zealand            [50] GNU Operating System. 2025. Automake. https://www.gnu.org/software/
     National Cyber Security Centre, and Computer Emergency Response Team New                   automake/.
     Zealand. 2003. The Case for Memory Safe Roadmaps: Why Both C-Suite                    [51] tiny AES-c. 2025. tiny-AES-c. https://github.com/kokke/tiny-AES-c.
     Executives and Technical Experts Need to Take Memory Safe Coding Seriously.           [52] Tinyhttpd. 2025. Tinyhttpd. https://github.com/EZLippi/Tinyhttpd.
[20] Matthew T Dearing, Yiheng Tao, Xingfu Wu, Zhiling Lan, and Valerie Taylor.            [53] Min Xue, Artur Andrzejak, and Marla Leuther. [n. d.]. An interpretable error
     2024. LASSI: An LLM-based Automated Self-Correcting Pipeline for Translating               correction method for enhancing code-to-code translation. In The Twelfth
     Parallel Scientific Codes. arXiv preprint arXiv:2407.01638 (2024).                         International Conference on Learning Representations.
[21] Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, and Aseem Rastogi. 2023. Fixing     [54] Aidan ZH Yang, Yoshiki Takashima, Brandon Paulsen, Josiah Dodds, and Daniel
     rust compilation errors using llms. arXiv preprint arXiv:2308.05177 (2023).                Kroening. 2024. Vert: Verified equivalent rust transpilation with few-shot learning.
[22] Docs.rs. 2025. Crate url. https://docs.rs/url/latest/url/.                                 arXiv preprint arXiv:2404.18852 (2024).
[23] Mehmet Emre, Peter Boyland, Aesha Parekh, Ryan Schroeder, Kyle Dewey, and             [55] Zhen Yang, Fang Liu, Zhongxing Yu, Jacky Wai Keung, Jia Li, Shuo Liu, Yifan
     Ben Hardekopf. 2023. Aliasing limits on translating c to safe rust. Proceedings of         Hong, Xiaoxue Ma, Zhi Jin, and Ge Li. 2024. Exploring and unleashing the power
     the ACM on Programming Languages 7, OOPSLA1 (2023), 551–579.                               of large language models in automated code translation. Proceedings of the ACM
[24] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2021. Trans-                   on Software Engineering 1, FSE (2024), 1585–1608.
     lating C to safer Rust. Proceedings of the ACM on Programming Languages 5,            [56] yank. 2025. yank. https://github.com/mptre/yank.
     OOPSLA (2021), 1–29.                                                                  [57] Xin Yin, Chao Ni, Tien N Nguyen, Shaohua Wang, and Xiaohu Yang. 2024. Recti-
[25] Hasan Ferit Eniser, Hanliang Zhang, Cristina David, Meng Wang, Brandon                     fier: Code Translation with Corrector via LLMs. arXiv preprint arXiv:2407.07472
     Paulsen, Joey Dodds, and Daniel Kroening. 2024. Towards Translating Real-World             (2024).
     Code with LLMs: A Study of Translating to Rust. arXiv preprint arXiv:2405.11514       [58] Hanliang Zhang, Cristina David, Meng Wang, Brandon Paulsen, and Daniel
     (2024).                                                                                    Kroening. 2025. Scalable, validated code translation of entire projects using large
[26] FastestWebsiteEver. 2025. FastestWebsiteEver. https://github.com/diracdeltas/              language models. Proceedings of the ACM on Programming Languages 9, PLDI
     FastestWebsiteEver.                                                                        (2025), 1616–1641.
[27] Zach Hanley. 2023. Rust Won’t Save Us: An Analysis of 2023’s Known Exploited          [59] Hanliang Zhang, Cristina David, Yijun Yu, and Meng Wang. 2023. Ownership
     Vulnerabilities. https://www.horizon3.ai/attack-research/attack-blogs/analysis-            guided C to Rust translation. In International Conference on Computer Aided
     of-2023s-known-exploited-vulnerabilities/                                                  Verification. Springer, 459–482.
[28] Jaemin Hong and Sukyoung Ryu. 2023. Concrat: An automatic C-to-Rust lock              [60] Quanjun Zhang, Chunrong Fang, Yang Xie, YuXiang Ma, Weisong Sun, and Yun
     API translator for concurrent programs. In 2023 IEEE/ACM 45th International                Yang Zhenyu Chen. 2024. A Systematic Literature Review on Large Language
     Conference on Software Engineering (ICSE). IEEE, 716–728.                                  Models for Automated Program Repair. arXiv preprint arXiv:2405.01466 (2024).
[29] Jaemin Hong and Sukyoung Ryu. 2024. Don’t Write, but Return: Replacing Output
     Parameters with Algebraic Data Types in C-to-Rust Translation. Proceedings of
     the ACM on Programming Languages 8, PLDI (2024), 716–740.
[30] Jaemin Hong and Sukyoung Ryu. 2025. Type-migrating C-to-Rust translation
     using a large language model. Empirical Software Engineering 30, 1 (2025), 3.
[31] Ali Reza Ibrahimzada. 2024. Program Decomposition and Translation with Static
     Analysis. In Proceedings of the 2024 IEEE/ACM 46th International Conference on
     Software Engineering: Companion Proceedings. 453–455.
[32] Immunant. 2022. C2Rust. https://github.com/immunant/c2rust.
[33] Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press,
     and Karthik R Narasimhan. 2024. SWE-bench: Can Language Models Resolve
     Real-world Github Issues?. In The Twelfth International Conference on Learning
     Representations. https://openreview.net/forum?id=VTF8yNQM66
[34] Rust Programming Language. 2025. Rust error codes index. https://doc.rust-
     lang.org/error_codes/error-index.html.
[35] Mosh Levy, Alon Jacoby, and Yoav Goldberg. 2024. Same task, more tokens: the
     impact of input length on the reasoning performance of large language models.
     arXiv preprint arXiv:2402.14848 (2024).
[36] Ruishi Li, Bo Wang, Tianyu Li, Prateek Saxena, and Ashish Kundu. 2024.
     Translating c to rust: Lessons from a user study. arXiv preprint arXiv:2411.14174
     (2024).
[37] mark sweep. 2025. mark-sweep. https://github.com/munificent/mark-sweep.
[38] mcrcon. 2025. mcrcon. https://github.com/Tiiffi/mcrcon.
