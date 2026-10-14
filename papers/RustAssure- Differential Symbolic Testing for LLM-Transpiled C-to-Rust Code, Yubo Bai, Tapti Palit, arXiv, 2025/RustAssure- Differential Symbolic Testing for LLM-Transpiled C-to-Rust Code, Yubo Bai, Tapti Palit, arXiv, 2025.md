                                                RustAssure: Differential Symbolic Testing for
                                                     LLM-Transpiled C-to-Rust Code
                                                                       1st Yubo Bai                                            2nd Tapti Palit
                                                            Department of Computer Science                           Department of Computer Science
                                                             University of California, Davis                          University of California, Davis
                                                                      Davis, USA                                               Davis, USA
                                                                  gabbai@ucdavis.edu                                       tpalit@ucdavis.edu



                                           Abstract—Rust is a memory-safe programming language that             To mitigate these challenges, we present RustAssure—a sys-
arXiv:2510.07604v1 [cs.SE] 8 Oct 2025




                                        significantly improves software security. Existing codebases writ-   tem that uses Large Language Models (LLMs) to transpile C
                                        ten in unsafe memory languages, such as C, must first be             code into Rust and establishes the semantic similarity between
                                        transpiled to Rust to take advantage of Rust’s improved safety
                                        guarantees. RustAssure presents a system that uses Large Lan-        the original and transpiled code using differential symbolic
                                        guage Models (LLMs) to automatically transpile existing C code-      testing. Unlike dynamic testing approaches such as unit or fuzz
                                        bases to Rust. RustAssure uses prompt engineering techniques         testing, where the transpiled Rust function is executed with
                                        to maximize the chances of the LLM generating idiomatic and          concrete inputs, RustAssure symbolically executes both the
                                        safe Rust code. Moreover, because LLMs often generate code           original C and LLM-transpiled Rust code to detect functional
                                        with subtle bugs that can be missed under traditional unit or
                                        fuzz testing, RustAssure performs differential symbolic testing      divergence between the original C and Rust code. Unlike
                                        to establish the semantic similarity between the original C and      dynamic testing which is input-specific, symbolic execution
                                        LLM-transpiled Rust code. We evaluated RustAssure with five          can explore all paths, thus proving that all inputs produce
                                        real-world applications and libraries, and showed that our system    equivalent outputs and guaranteeing correctness, while differ-
                                        is able to generate compilable Rust functions for 89.8% of all       ential testing can only show that the behavior is the same for
                                        C functions, of which 72% produced equivalent symbolic return
                                        values for both the C and Rust functions.                            the executed input. Furthermore, by detecting the divergence at
                                                                                                             the symbolic level, RustAssure avoids false positives stemming
                                                               I. I NTRODUCTION                              from differences in the runtime environment, such as memory
                                           Rust is a memory-safe programming language that is in-            layout and heap addresses.
                                        creasingly gaining popularity. Automatically transpiling code-          RustAssure first transpiles the C code to Rust using Large
                                        bases written in memory-unsafe languages such as C, to Rust,         Language Models (LLMs). Multiple factors must be consid-
                                        can significantly improve software security. Previous syntax-        ered when using LLMs to transpile C code to Rust. First, the
                                        directed and program analysis-driven methods [1], [2], [3]           LLM-based transpiler must ensure that the C code is tran-
                                        have achieved limited success, correctly transpiling only a          spiled to safe Rust to the greatest extent possible. To provide
                                        fraction of the C code to safe Rust. Moreover, the Rust code         programmers with more flexibility, Rust provides an “escape-
                                        generated by these approaches is difficult to read and often         hatch” that relaxes certain memory safety rules if the code is
                                        does not follow idiomatic Rust conventions [4]. More re-             enclosed in an unsafe block. Unsafe Rust code introduces
                                        cently, Large language models (LLMs) have shown significant          potential memory corruption vulnerabilities in the program,
                                        promise in code completion [5], code generation [6], [7], [8],       therefore, the amount of unsafe Rust code generated by the
                                        and code transpilation [4]. However, LLMs are not guaranteed         LLM must be minimized. RustAssure uses various prompt-
                                        to always generate correct code [9]. Therefore, it is essential      engineering techniques to ensure that the code generated by
                                        to verify the functional correctness of LLM-generated code.          the LLM compiles successfully, and also minimizes the use
                                           Existing approaches for testing LLM-transpiled Rust code          of unsafe Rust.
                                        suffer from various limitations. Approaches based on unit test-         After the LLM generates compilable Rust code, RustAssure
                                        ing inherently suffer from code coverage issues, especially for      performs differential symbolic testing on the original C and
                                        large complex applications, leading to significant portions of       LLM-transpiled Rust code. RustAssure contains a Semantic
                                        the code remaining untested. Approaches based on differential        Similarity Checker that symbolically executes individual C
                                        fuzzing [4] compare the test case outputs for the original           functions and their LLM-transpiled Rust counterparts, deriving
                                        and transpiled code. However, the exact return values of the         symbolic values for all implicit and explicit return variables
                                        C and Rust functions can differ due to runtime differences.          of the function. RustAssure then compares the symbolic value
                                        For example, the values of pointers returned by the functions        for each return value of the function and reports a Semantic
                                        would differ across different language runtime environments.         Similarity Score (S3 score) for the Rust function. Moreover,
                                        Therefore, a mismatch in the concrete runtime values do not          differential symbolic testing can not only identify which return
                                        necessarily indicate an error.                                       values diverge, but also how they diverge, making it easier for
the programmer to pinpoint the bug.                                      system to identify the semantic similarity between the
    RustAssure’s symbolic execution is composable. RustAs-               original C and LLM-transpiled Rust code.
sure can analyze each Rust function individually and determine        • Three patterns for reconciling the type differences be-
if it is semantically equivalent to the original C function. If         tween C and Rust that make it possible to compare the
the Rust function being analyzed invokes another function,              symbolic return values in C and Rust code.
RustAssure abstracts away the implementation of that function         • Evaluation of RustAssure using five real-world libraries
and only ensures that the called function returns symbolic               that demonstrate RustAssure’s bug-finding capabilities,
values. This allows the caller function to be symbolically               and comparisons against the CROWN [13] and FLUO-
tested even if the called function does not compile or link              RINE [4] C-to-Rust toolchains.
successfully with the rest of the LLM-transpiled Rust code.
                                                                    Our toolchain can be found at https://github.com/davsec-lab/
As a result, the programmer can test each LLM-transpiled
                                                                    rustassure.
Rust function for semantic equivalence and improve their
confidence in the LLM-produced code, even if a few LLM-                              II. M OTIVATING E XAMPLE
generated Rust functions do not successfully compile. In fact,
from our experience even with state-of-the-art LLM models              Code generated by Large Language Models (LLMs) often
such as GPT-4o [10], only 89.8% of all transpiled C functions       contain subtle bugs. Consider the simplified code snippet
successfully compile without user intervention. RustAssure is       for the function u8next_ from the u8c library, shown in
particularly useful in such scenarios.                              Figure 1. The original C function takes as arguments an input
    Establishing semantic equivalence using symbolic return         UTF-8-encoded string, txt, and an output argument, ch.
values across different languages is not trivial. Often, Rust       It returns the number of bytes encoding the first Unicode
code uses types that are missing in C completely. For example,      codepoint of the string txt, and stores the converted Unicode
safe Rust code does not allow explicit NULL values but              codepoint in ch. If the encoding is not valid, it returns -1 and
requires wrapping values that can potentially be NULL in an         stores the first byte of the input string in ch.
Option enum type. Accurate extraction and comparison of                To perform the conversion, the function maintains a state
symbolic values across different languages requires aligning        machine, as shown in lines 6-23 in the original C code. The
these differing C and Rust types correctly. RustAssure iden-        LLM-transpiled Rust code contains a subtle bug in this state
tifies three such commonly occurring patterns and maps the          machine code. When the input is not a valid UTF string and
Rust type correctly to the C type, thus facilitating the symbolic   contains an invalid byte in any of the non-first byte offsets, the
value comparison of the return values.                              functionalities of the original C and the LLM-transpiled Rust
                                                                    functions diverge. For example, consider the two character
    We used RustAssure to transpile five C real-world codebases
                                                                    input sequence {0xC2, 0x41}. The first byte, 0xC2 is valid,
to Rust, and used the Semantic Similarity Checker to compute
                                                                    but the second byte, 0x41, is invalid. When executed with this
the Semantic Similarity Score (S3 score) for the transpilations.
                                                                    byte sequence, the C program will return the original first byte,
These libraries had a total of 176 functions, of which 158,
                                                                    which is 0xC2, but the transpiled Rust program will return an
146, 124, and 85 functions were compiled successfully by the
                                                                    intermediate decoding state, specifically, the bit-masked value
GPT-4o, GPT-4o-mini, GPT-3.5-turbo [10], [11] and Claude-
                                                                    0x02. This occurs because the generated Rust code is missing
3.5-Sonnet [12] models, respectively. Across all of these LLM
                                                                    the operation that resets the variable val to the first character
models, RustAssure’s S3 metric allowed us to find 12 complex
                                                                    of the input string txt (line 19, in the C code). The variable
semantic bugs, along with 13 simple bugs. Because these
                                                                    val is finally copied to the ch argument, resulting in the
12 and 13 bugs are present in more than one LLM model,
                                                                    functional divergence. Thus, the C and Rust API semantically
the total number of buggy functions detected are 20 and
                                                                    diverge, and if the users of the Rust API are not aware of this
17, for semantic and simple bugs, respectively. Moreover, we
                                                                    change they may misinterpret error conditions or incorrectly
computed the average precision of the S3 score, across all
                                                                    assume behavior consistent with the C API.
LLM models to be 85.7% and 88.2%, for the libcsv and u8c
                                                                       Detecting this bug requires knowledge of Unicode/UTF-
codebases, respectively, while the average recall was 100%
                                                                    8 semantics, which traditional fuzzers lack, limiting their
for both codebases. An end-to-end comparison shows that
                                                                    effectiveness. Moreover, the unit test cases provided for the
RustAssure can generate code with 72% fewer raw pointers
                                                                    u8c library do not verify the returned byte in the ch output
than the state-of-the-art syntax-directed C-to-Rust transpilation
                                                                    argument when an invalid UTF string is provided, and only
toolchain, CROWN [13], and find 11 semantic bugs that the
                                                                    focuses on the explicit return value for checking error con-
testing framework, FLUORINE [4], is unable to find.
                                                                    ditions. Because the RustAssure toolchain relies on symbolic
    In summary, we make the following contributions—                execution, it can correctly identify this semantic divergence.
  • RustAssure, an LLM-based pipeline for transpiling C
    code to safe Rust. The pipeline uses various prompt                                       III. D ESIGN
    engineering techniques to assist the LLM in generating             Figure 2 shows RustAssure’s two major components—the
    safe Rust code.                                                 LLM Invoker and the Symbolic Analyzer. The LLM Invoker is
  • Semantic Similarity Checker, a symbolic execution-based         responsible for invoking the LLM model for the transpilation
                               Original C code                                                     LLM-transpiled Rust Code
 1. int u8next_(const char *txt, int *ch){                           1. fn u8next_(txt: *const u8, ch: &mut i32) -> i32{
 2.   unsigned char *s = (unsigned char *)txt;                       2.   let mut s = txt;
 3.   char first = *s;                                               3.   let first = unsafe { *s };
 4.   if (first) {                                                   4.   if first != 0 {
 5.      val = first;                                                5.     val = first as i32;
 6.      goto fsm_state_START; {                                     6.     'fsm_state_start: loop {
 7.        fsm_state_START : {                                       7.         if unsafe { *s } <= 0xDF {
 8.          if (*s <= 0xDF) {                                       8.           val &= 0x1F;
 9.            val &= 0x1F;                                          9.           'fsm_state_len2_0: loop {
10.            s++;                                                 10.             s = unsafe { s.add(1) };
11.            if ( *s < 0x80 || 0xBF < *s) {                       11.             if unsafe { *s } < 0x80 || 0xBF < unsafe { *s } {
12.              goto fsm_state_invalid;                            12.               len = -1;
13.            }                                                    13.               break 'fsm_state_start;
14.          }                                                      14.             }
15.          //decode...                                            15.             //decode...
16.        }                                                        16.           }
17.        //other state...                                         17         }
18.        fsm_state_invalid : {                                    18.         //...other state
19.          val = first; //Missing in Rust code
                                                                    19.       }
20.          len = -1;                                              20.   }
21.        }                                                        21.   *ch = val;
22.    }                                                            22.   len
23. }                                                               23.}
24. if (ch) *ch = val;
25. return len;
26.}



Fig. 1. Bug detected by RustAssure. When executed with an invalid UTF string, the LLM-generated Rust code returns an incorrect intermediate state instead
of a pointer to the start of the input string, which is the expected functionality.


                                                       Large Language Model
       LLM Invoker                Struct Field                                    CC                      Symbolic Analyzer
                                                                                   RS
                                Usage Analyzer
                                                          Context Window                                  Language-aware      Graph Edit Distance
                                                                                            Symbolizer
             CC                                              Manager                                      Graph Converter         Calculator
               C                            Struct                            Rust Source
                       Preprocessor
                                          Transpiler                           Code Files                              Semantic
          C Source                                                                           Symbolic
                                                       Feedback Generator                                           Similarity Score
          Code Files                                                                         Executor


                                                        Fig. 2. RustAssure transpiler toolchain.



task, followed by the Symbolic Analyzer performing differen-                   have a fixed context window [14] that limits the amount
tial symbolic testing to identify functional divergences.                      of input it can process at a time. Therefore, RustAssure’s
                                                                               LLM Invoker includes only the essential macro expansions,
A. LLM Invoker                                                                 typedef instructions, and struct and function defini-
  RustAssure’s LLM Invoker is responsible for taking a C                       tions in the LLM request. This contextual information helps
codebase, preprocessing it, and invoking the configured LLM                    the LLM produce accurate transpilations.
model for transpilation.                                                       Struct Transpiler. Multiple functions, whose transpilation
Header File Preprocessor. We observed that naively sending                     spreads out over multiple LLM invocations can use the same
the code in the C source code files (.c files) to the Large                    struct type. We observed that due to the inherent non-
Language Model for transpilation is not adequate. This code                    determinism and randomness [15] of LLM models these
often lacks much of the contextual information that is essential               different invocations can sometimes generate slightly different
for the correct transpilation of each function in the source                   Rust struct definitions for the same C types. For example,
code file, such as, struct definitions, function declarations,                 the names of certain transpiled struct fields can differ
preprocessor macros, and typedef aliases, which are defined                    between different LLM invocations. These differing defini-
in .h header files.                                                            tions cause linkage issues when the transpiled Rust functions
   However, when the C preprocessor processes the .c file,                     are linked together to build the final executable. To avoid
it naively adds all contents of all header files included by the               such linkage issues, the LLM Invoker first extracts all C
.c file, even if the content is not actually used by the C code.               struct definitions and invokes the LLM to pre-translate
Therefore, including all output produced by the C preprocessor                 them. These Rust transpilations of struct types are stored in
in the LLM request is unnecessary. Moreover, LLM models                        a Struct Transpilation Cache. Then, for each function that uses
these struct types, the pre-generated struct definition             execute the function under test. If the function takes pointer
is provided along with the C function as the prompt, and            arguments or arguments of struct type, the Symbolizer
the LLM is instructed to use the pre-generated definition.          ensures that symbolic memory regions are allocated for each
This ensures consistent transpilation of struct types across        pointer and struct field. Pointer type arguments and fields
different functions.                                                can be nested to arbitrary levels. For example, an argument of
Struct Field Usage Analyzer. In many cases, the correct Rust        struct type can contain a pointer field pointing to another
type for a variable depends on the usage of the corresponding       struct object. The Symbolizer symbolizes nested pointers
C variable. For example, in C/C++, struct fields of char*           and nested struct fields up to a configurable nesting limit.
type can be used to store both null-terminated strings, or arrays   For our evaluation, we use a maximum limit of 10.
of characters. The usage of the char* field must be analyzed           The Symbolizer also instruments the function execution
to determine whether it is used as a string or an array. In         completion with a function epilogue to log the symbolic values
fact, without such analysis, from our experience, LLM models        of the explicit return value and output parameters. For complex
transpile such struct fields into Rust raw pointers, such as        types such as struct and array types, the Symbolizer logs
                                                                    the symbolic values for each field or element. If these fields or
*mut T, and enclose any code using these pointers fields with
unsafe blocks. To limit the amount of unsafe Rust code, the         elements are pointers, the Symbolizer recursively traverses the
LLM Invoker extracts all uses of such char* fields and adds         symbolic object pointed to by its pointer, and logs its symbolic
them to the LLM request, when pre-translating the struct            values. The Symbolizer tracks which fields of struct type
types, and instructs the LLM to consider these field usages for     output parameters were modified and logs the symbolic values
the transpilation task.                                             of only those fields. This selective logging ensures that only
                                                                    meaningful symbolic state changes are reported.
Context Window Manager. While LLM context window
                                                                       The Symbolizer also instruments any external function calls
sizes are ever increasing, many LLM models, such as GPT-
                                                                    to return symbolic values, ensuring that symbolic execution
3.5-turbo [10] and Mistral 7B [16] have smaller context
                                                                    can proceed without requiring concrete results from unknown
windows of 16K tokens. When using these models, a single
                                                                    or unanalyzed functions. By replacing the outputs of external
large function can exceed the context window length. To
                                                                    function with symbolic expressions, our analysis remains fully
support these models, the LLM Invoker automatically chunks a
                                                                    composable, and each function can be symbolically executed
function into multiple LLM requests if it does not fit within the
                                                                    independently.
LLM’s context window. The LLM’s response for each chunk
is then collected and assembled into the final Rust function.       Symbolic Executor. After the Symbolizer modifies the C
                                                                    and Rust functions, the Symbolic Executor performs the core
Feedback Generator. Like previous approaches [17], when
                                                                    symbolic execution process using the KLEE [18] symbolic
the LLM produces a transpilation that does not compile, Rus-
                                                                    execution engine. When the symbolic execution completes,
tAssure re-attempts the transpilation, by sending the compiler
                                                                    the function epilogue inserted by the Symbolizer is executed,
error message along with the original C function to the LLM,
                                                                    and the symbolic values of the function return values are
requesting a corrected translation. This approach leverages the
                                                                    printed. To facilitate the symbolic execution of both C and
precise and diagnostically rich error messages emitted by the
                                                                    Rust code using KLEE, we convert both the original C and
Rust compiler to provide feedback to the LLM, thus increasing
                                                                    the transpiled Rust code to an Intermediate Representation (IR)
the chances of it fixing the offending code. In addition to
                                                                    and symbolically execute this IR code. However, symbolically
compilation errors, if the LLM-transpiled Rust code contains
                                                                    executing the Rust-produced IR code adds Rust language-
any unsafe block, or invokes unsafe functions such as the
                                                                    specific artifacts to the symbolic return values. We discuss how
functions from the libc crate, the LLM Invoker requests
                                                                    we handle these language-specific artifacts in the symbolic
a re-translation up to a configurable number of times. Thus,
                                                                    values in §III-C.
each C function is transpiled using the LLM, maximizing the
possibility of safe Rust code.                                      C. Semantic Similarity Checker
B. Symbolic Analyzer                                                   The Semantic Similarity Checker compares the semantic
   After the LLM Invoker produces compilable Rust code,             equivalence between the original C code and the LLM-
RustAssure symbolically executes them to derive the symbolic        transpiled Rust code by comparing the symbolic return values
return values for each function. We note that C and Rust            of the corresponding C and Rust functions. The symbolic val-
functions will not be symbolically equivalent if the C code has     ues are represented by a Backus-Naur Form grammar, called
memory corruption bugs that are absent in Rust—a limitation         KQuery [19]. RustAssure processes these KQuery symbolic
that is present even when using concrete test cases. Such cases     values as discussed below.
can result in false positives.                                      Language-aware Graph Converter. The Language-aware
Symbolizer. The Symbolizer instruments the C and Rust coun-         Graph Converter component converts the symbolic values to a
terparts of each function with a prologue and an epilogue. The      graphical representation. In some cases, language differences
function prologue initializes the function arguments with sym-      between C and Rust can cause differences in symbolic rep-
bolic values, enabling the Symbolic Executor to symbolically        resentations between C and Rust, even when the high-level
                 Original C code                C Symbolic Return Value                IV. H ANDLING L ANGUAGE - LEVEL D IFFERENCES
int u8fold(int cp) {
  if (0x10400 <= cp && cp <= 0x10427) {               Add                            Fundamental differences between C and Rust often results
    cp += 40;                                                   Read              in a mismatch between types and object memory layout when
  }                                                                               variables are transpiled from C to Rust. To limit false positives,
  if (cp <= 0xFFFF) {                                                  cp
    cp = fold_search(cp);                                                         RustAssure aligns these mismatches as described below.
                                                                 40
  }
  return cp;                                                                      A. Aligning Memory Layout.
}
                                                                                     We observe that the memory layouts of complex types such
                                                Rust Symbolic Return Value
            LLM-transpiled Rust Code                                              as structs generated by C compilers, such as Clang [21],
fn u8fold(mut cp: i32) -> i32 {                  Extract
                                                                                  differ from the memory layouts generated by the Rust com-
  if (0x10400..=0x10427).contains(&cp) {                   Add
      cp += 40;
                                                                                  piler, rustc. By default, the Rust compiler aligns fields
  }                                                         Sign Extend           differently and adds additional padding in between different
  if cp <= 0xFFFF {                                                   Read        fields. Moreover, the Rust compiler often also reorders the
      cp = fold_search(cp);
                                                                             cp   struct fields for memory optimization. This differing memory
  }
                                                                 40
  cp                                                                              layout makes it challenging to compare the symbolic value of
}                                                           0
                                                                                  the original C objects and the transpiled Rust objects.
                                                                                     Fortunately, Rust allows the programmer to specify alterna-
                                                                                  tive data layout strategies. In particular, it provides the attribute
Fig. 3. C and Rust symbolic return values for the u8fold function. The red
boxes are language-specific artifacts added by the Rust compiler.
                                                                                  repr(C) to specify a C-like memory layout. Similarly, the
                                                                                  repr(packed) attribute instructs the compiler not to insert
                                                                                  any additional padding between the struct fields. Therefore,
                                                                                  RustAssure applies the #[repr(C, packed)] attribute
                                                                                  on every Rust struct type. This ensures that the compiler
semantics of the code remain the same. The graph represen-                        lays the struct fields out in memory exactly the way a C
tations allows us to easily apply normalization techniques on                     compiler would, keeping struct fields in order and using C-
the symbolic values due to such language-level differences.                       style alignment and padding. This simplifies the recovery of
                                                                                  the symbolic return values from these fields.
   Consider the C and transpiled Rust code, from the u8c
library, shown in Figure 3. The function u8fold maps a                            B. The Option type.
Unicode codepoint to its lowercase form. Although both the                            Unlike C, Rust does not support NULL values and instead
C and Rust code perform the same cp += 40 operation in                            uses the Option<T> enum to represent an optional value.
the first if block, the symbolic output graphs differ due to                      The Option<T> enum type can either contain a value of
Rust’s explicit type extension operations needed to support                       type T (Some(T)) or be empty (None). Thus, C pointer
integer overflow checks necessary for memory safety. These                        variables that can potentially be NULL, are wrapped in the
checks are completely missing in C. These additional nodes in                     Option<T> enum type in Rust. Therefore, the apparent type
Rust’s symbolic execution graph cause a mismatch even when                        of the C and transpiled Rust variable will not be the same.
the underlying operation is identical. To address these dif-                      This difference means that RustAssure cannot simply use the
ferences, the Language-aware Graph Converter applies graph                        return value types to retrieve and compare the symbolic values
normalization techniques to remove redundant type extension                       of the C and Rust variables. Additional processing is required
operations that do not affect program semantics, by removing                      to align the C and Rust types in such cases.
their corresponding nodes from the symbol graph.                                      However, in spite of the difference in the types of the
                                                                                  variables, when the Rust compiler lowers the Option enum
Graph Edit-distance Calculator. RustAssure uses the graph-                        type variable to the machine code, it treats the enum variable
edit distance between the corresponding graphical representa-                     simply as syntactic sugar around the inner object. The memory
tions of the symbolic return values of the C and Rust functions                   layout of the original C nullable pointer of type T and Rust’s
as the Semantic Similarity Score (S 3 score) between return                       Option wrapper around the type T are the same, assuming
values in the original C code and the LLM-transpiled Rust                         the requirements outlined in §IV-A are followed. The only
code. An edit distance of zero means that the Rust function                       special operations the Rust compiler inserts are NULL checks
returns the same symbolic return value as the original C                          that panic on failure. Therefore, when RustAssure’s Semantic
function. A higher edit distance implies a higher degree of                       Similarity Checker encounters a situation where a return value
semantic divergence. RustAssure uses a standard graph edit-                       or output parameter in Rust is of Option type, it simply casts
distance algorithm [20] to compute the edit distance between                      it to the underlying type to access its symbolic representation.
the return values. We used a graph edit-distance-based compar-
ison instead of SMT solving to simplify our implementation.                       C. String and Slice types.
In the future, we plan to explore using SMT solvers to establish                    The C language represents strings as null-terminated arrays
strict equivalence.                                                               of char type. The corresponding type in Rust is String. A
                  C code                       C Memory Layout           contains three fields, of which the first ptr field points to
1.void f(char *output,                               char*               the actual data buffer. The actual memory layout of the data
2.       int index,                                                      buffer referenced by the ptr field of Rust’s Vec object is the
                                                    output
3.       char val) {                                                     same as the layout of the C output variable. Therefore, for
4.    if (output) {// Non-null case}
5.    else {// Null case}
                                                                         the Rust code, RustAssure’s Semantic Similarity Checker just
                                            {sym1, sym2, ... symN}
6.}                                                                      dereferences the output variable to access the Vec object
                 Rust code                     Rust Memory Layout        and then accesses the symbolic contents pointed to by the ptr
1. fn f(output: &mut Option<Vec<u8>>,   Option<Vec<u8>>
                                                                         field pointer. These symbolic contents are compared against
2.       index: usize,                                                   those of the output variable in the original C program.
                                           output
3.         val: u8) {
4.    match output{                             Vec<u8>                                       V. I MPLEMENTATION
5.      Some(v) => {// Non-null case}
                                          ptr len capacity
6.      None => {// Null case}                                              RustAssure uses Clang 14 and Rustc v1.64 for compiling
7.    }                                                                  the C and transpiled Rust code. It interfaces with the LLM
8.}                                   {sym1, sym2, ... symN}             models using Python modules. Both Clang and Rustc uses
                                                                         the LLVM compiler to compile C and Rust code to ma-
                                                                         chine code, respectively. RustAssure leverages this common
Fig. 4. Differing memory layout between C and Rust. The argument input   compiler toolchain to compile both the C and the Rust code
is a char* array for which the transpiled Rust code uses Vec type.
                                                                         to LLVM Intermediate Representation (IR), facilitating the
                                                                         subsequent symbolic execution. RustAssure uses a sequence of
related Rust type is the slice type &str that represents an
                                                                         Clang tools, based on ASTMatchers [22], to statically analyze
immutable reference to a sequence of characters. Similar to
                                                                         and perform various preprocessing tasks on the C source code
string slices, Rust also allows slices of arrays. Both String
                                                                         files, such as expanding all header files, removing unused
and slice type variables are internally represented by struct
                                                                         typedef definitions, variable and struct definitions.
types by the Rust compiler. The first field of this struct is a
                                                                            RustAssure uses the KLEE v3.1 [18] symbolic execution
data pointer pointing to the array of char type, and the second
                                                                         engine to symbolically execute the LLVM IR code for both
field represents the length. Therefore, for return values of these
                                                                         the C and Rust code. While KLEE supports C standard
types, RustAssure’s Semantic Similarity Checker accesses the
                                                                         library functions, it lacks support for the Rust standard library.
first field of the struct type and casts it to char* before
                                                                         Therefore, we first compiled Rust’s standard library to obtain
comparing its symbolic values.
                                                                         its LLVM IR bitcode representation, and then linked it with the
   Internally, the Rust compiler initializes the slice types,
                                                                         bitcode of each function being symbolically executed. Finally,
&str and &[T] as arrays of initial length zero, indicating that
                                                                         we developed an Antlr [23] parser for KLEE’s Kquery gram-
their actual length is determined at runtime. When symbolizing
                                                                         mar and parsed the symbolic return values to produce symbolic
such slice types, RustAssure’s Symbolizer initializes these
                                                                         graphs represented in the GraphViz DOT format [24]. We used
slices to symbolic buffers of size 100 and explicitly initializes
                                                                         the networkx [25] library’s graph edit distance algorithm [26]
the len field of the struct to 100 to safely access its contents.
                                                                         function to compute the edit distance between the symbolic
D. The vector type.                                                      return values and obtain their S 3 score.
   C arrays are transpiled to Rust’s Vec type objects. Unlike                                   VI. E VALUATION
C arrays, Rust guarantees that any out-of-bounds accesses in a
Vec type will cause a panic at runtime. Similar to the String               We evaluated RustAssure with five C codebases—libcsv,
type, the Vec<T> type is represented by a struct type that               urlparser, optipng, libbmp, and u8c, with 405, 435, 3039,
contains three fields, a data pointer to the array of type T, a          287, and 334 lines of code, respectively. Our dataset con-
len field to represent the length of the array indicating the            sists of applications commonly used in previous works [1],
actual number of elements contained, and a capacity field                [27], [3], [28], [2], [29]. We selected the following LLM
to represent the capacity of the array. The semantic checker             models—OpenAI’s GPT-4o, GPT-4o-mini, GPT-3.5-turbo, and
directly accesses this field and compares the symbolic values            Anthropic’s Claude-3.5-Sonnet, for the evaluation.
of each array element in the Rust code with its C counterpart.
   When the String, str&, Vec are wrapped in an                          A. Compilation Results
Option, we extract and cast the inner value as explained in                Table I presents the compilation results for the five code-
§IV-B, before comparing the symbolic values. Figure 4 shows              bases for the four LLM models. GPT-4o outperformed all other
an example of a nullable array of characters, output, being              LLM models across all codebases, successfully transpiling
transpiled into a Rust Vec object, wrapped in an Option                  89.8% of all C functions into compilable Rust functions.
enum object. The figure also shows the C and Rust code                   GPT-4o-mini produced compilable transpilations for 83.0% of
used to access the respective objects, along with the objects’           C functions, while the GPT-3.5-turbo and Claude-3.5-Sonnet
memory layouts. As shown, the Rust variable output of                    models produced compilable Rust translations for 70.5% and
type Option<Vec<u8>> is a pointer to the Vec object that                 48.3% of all C functions.
                                                             TABLE I
              C OMPILATION AND SEMANTIC EQUIVALENCE STATISTICS . E Q . O UTPUT INDICATES RETURN VALUES WITH S 3 SCORE = 0.

  Codebase    LLM Model                            Functions                        Code             Return values and output parameters
                                  C functions   Rust compiled   Perc. compiled   Perc. unsafe   Output values   Eq. Output    % of Eq. Output      Bug
  libcsv      GPT-4o                      29              27            93.1%            3%               73             62                84.9%     5
              GPT-4o-mini                 29              23            79.3%           16%               66             55                83.3%     1
              GPT-3.5-turbo               29              25            86.2%           15%               59             35                59.3%     2
              Claude-3.5-Sonnet           29              15            51.7%           79%               48             35                72.9%     2
  urlparser   GPT-4o                      26              23            88.5%           10%               32             18                56.3%     1
              GPT-4o-mini                 26              24            92.3%           27%               35             20                57.1%     0
              GPT-3.5-turbo               26              15            57.7%           77%               24             20                83.3%     0
              Claude-3.5-Sonnet           26               9            34.6%           66%               15             13                86.7%     0
  optipng     GPT-4o                      86              75            87.2%           15%              162            108                66.7%     0
              GPT-4o-mini                 86              69            80.2%           18%              145            105                72.4%     1
              GPT-3.5-turbo               86              59            68.6%           28%              121             79                65.3%     0
              Claude-3.5-Sonnet           86              35            40.7%           61%               69             54                78.3%     1
  libbmp      GPT-4o                      16              16           100.0%            4%               38             35                92.1%     0
              GPT-4o-mini                 16              14            87.5%           10%               42             36                85.7%     0
              GPT-3.5-turbo               16              13            81.3%           12%               36             34                94.4%     0
              Claude-3.5-Sonnet           16              13            81.3%            5%               38             35                92.1%     0
  u8c         GPT-4o                      19              17            89.5%           20%               23             14                60.9%     7
              GPT-4o-mini                 19              16            84.2%           31%               22             14                63.6%     4
              GPT-3.5-turbo               19              12            63.2%           23%               13             12                92.3%     0
              Claude-3.5-Sonnet           19              13            68.4%           57%               17             13                76.5%     3



Unsafe Rust. Table I also presents the percentage of unsafe                           A) char* used as a buffer, transpiled as Vec<u8>
code across all five codebases. The average percentage of                        struct csv_parser {
unsafe code across all codebases is 13.05%, 20.88%, 31.03%,                         unsigned char * entry_buf;
                                                                                    size_t entry_pos;
and 59.10%, for the GPT-4o, GPT-4o-mini, GPT-3.5-turbo,                             size_t entry_size;
and Claude-3.5-Sonnet models, respectively. Similar to the                          size_t blk_size;
                                                                                    void *(*realloc_func)(void *, size_t);
compilation success results, GPT-4o generates transpiled Rust                    };
code with the least number of unsafe program statements. The
reduced percentage of Unsafe Rust code for the GPT-4o model                      int csv_increase_buffer(struct csv_parser *p) {
                                                                                   size_t to_add = p->blk_size;
derives from its superior idiomatic type mapping capabilities.                     void *vp;
                                                                                   while ((vp = p->realloc_func(...)) == ((void*)0)) {
Impact of LLM model. Our results show that some LLM                                  to_add /= 2;
                                                                                     if (!to_add) {
models are more effective in deriving idiomatic Rust types                             p->status = 2;
from C type usages. For example, the char* type variables                              return -1;
can either be used as a null-terminated string, or as an array of                    }
                                                                                   }
char type. Whether or not the variable should be translated                        p->entry_buf = vp;
to a Rust string type or a Vec type depends on how                                 p->entry_size += to_add;
it is used in the application. Consider the simplified code                        return 0;
                                                                                 }
snippet from the libcsv codebase shown in Figure 5. The
                                                                                         B) char* used as a string, transpiled as String
struct csv_parser contains a field unsigned char*
entry_buf. The libcsv codebase uses this field as a char                         url_data_t* url_parse (const char* url) {
                                                                                   url_data_t *data = (url_data_t *) calloc(...);
array. This is evidenced by the presence of functions such as                      if (!data) return NULL;
csv_increase_buffer which increases the buffer size                                char* p = strdup(url);
dynamically by using the realloc function, without con-                            // ... more code
                                                                                 }
sidering any null-termination logic. The GPT-4o model can
correctly analyze the uses of this struct field, provided by the
                                                                             Fig. 5. Type usage based transpilation. The GPT-4o model can correctly
Struct Field Usage Analyzer described in §III-A, and transpile               identify that the Vec<u8> type is more appropriate in the first case, and the
it to use the Vec<u8> type. However, the other models simply                 String type is correct for the second case.
translate this type as a raw pointer of type *mut u8.                        tions generated by the GPT-3.5-turbo and Claude-3.5-Sonnet
   Similarly, the urlparser codebase stores the URL string in a              models generate only one and zero variables of type String
char* variable. The GPT-4o model can correctly determine                     respectively, using raw pointers for the remaining variables.
that the type of the url argument should be mut String.
On the other hand, the GPT-3.5-turbo and Claude-3.5-Sonnet                   B. Semantic Similarity Score
LLM models transpile this argument as a raw pointer of type                    We symbolized all arguments for each C and Rust function
*const c_char In fact, across all five codebases, GPT-                       and symbolically executed them, with a timeout of 180 min-
4o model generates translated Rust variables of the idiomatic                utes. Table I shows the S 3 Score for the C and Rust return
String type for a total of nine times, whereas the transpila-                values. Across all return values for all applications, the LLM
                             TABLE II                                              by GPT-4o-mini and Claude-3.5-Sonnet, the next character is
        RUST I NSTRUCTION C OVERAGE ( FOR COMPILABLE CODE )                        consumed at the end of the iteration. Specifically, line 15
                                                                                   is missing in the Rust code, which results in the = symbol
    Codebase     Original     GPT-4o      GPT-4o-   GPT-3.5-     Claude-3.5-
                 C code                    mini      turbo         Sonnet          being appended to the option name, instead of being discarded.
    libcsv       94.59%       90.63%      88.89%     93.96%        89.92%          Therefore, for an input in the form option=value, Rust
    urlparser    82.01%       72.81%      76.94%     72.21%        94.02%          will return option= as the option name, indicating a bug.
    optipng      79.24%       78.08%      79.19%     76.51%        80.59%
    libbmp       83.59%       79.21%      88.08%     91.77%        75.07%          Symbolically analyzing the original C function and the Rust
    u8c          95.04%       89.46%      90.19%     94.62%        95.91%          function shows that the minimum symbolic return value is ptr
                                                                                   = ptr + 3 for the C function and ptr = ptr + 2. This
                          TABLE III                                                shows that there is a bug in the Rust function and identifies
S YMBOLIC EXECUTION TIME USING 8 CORES (F OR COMPILABLE CODE ).                    that a pointer increment operation is missing.

  Codebase      GPT-4o      GPT-4o-mini     GPT-3.5-turbo      Claude-3.5-Sonnet
                                                                                   Incorrect conditional check. A bug in the Rust code gen-
                                                                                   erated by the GPT-4o, for the libcsv codebase, is shown in
  libcsv          5h2m            5h2m               5h2m                  5h3m
  urlparser       5h4m            5h4m               5h1m                  5h2m    Figure 7. The original C code sets the blk_size field in
  optipng        15h5m          11h15m              7h20m                 7h42m    the csv_parser, as long as the pointer p is not NULL. The
  libbmp         6h14m           3h46m              1h33m                  2h0m
  u8c           11h56m            5h4m              5h39m                 6h55m    LLM-generated Rust code sets the blk_size field only if
                                                                                   the previous value of that field was not 0. Symbolic execution
                                                                                   captures this semantic divergence because of the additional
models—GPT-4o, GPT-4o-mini, GPT-3.5-turbo, and Claude-                             symbolic constraint p.blk_size != 0.
3.5-Sonnet, produced semantically equivalent Rust transpila-
                                                                                   D. Precision and Recall
tions for 72%, 74%, 71%, and 80% of all cases. As we
discussed in VI-A, although Claude-3.5-Sonnet has the highest                         Table V shows the precision and recall analysis for the S3
semantic similarity score, it can only compile 48.3% functions                     score. Since the recall computation requires manual verifica-
successfully, while GPT-4o can compile 89.8% functions.                            tion of the LLM-generated Rust code, we report these statistics
Considering the number of the functions that have been                             only for libcsv and u8c.
successfully compiled, GPT-4o provides the highest number                          Precision. The overall precision across all LLM models for
of semantically equivalent transpilations.                                         libcsv and u8c is 85.7% and 88.2%. Besides the semantic bugs
   Table II shows the symbolic execution instruction coverage.                     we report in Table I, the true positive category also includes
The instruction coverage for the C codebases ranges from                           LLM-generated functions that are trivially incorrect, such as
79.24% to 95.04%, while that of the Rust code ranges from                          empty functions. The false positives arise due to optimiza-
72.21% to 95.91%. This indicates a significant percentage                          tions KLEE performs when symbolically modeling arrays and
of code was tested for both C program and Rust program.                            aligning these differences is primarily an engineering effort.
Table III shows the total time taken to execute all functions
                                                                                   Recall. To compute the recall of the S3 score, we first
in each of the codebases symbolically using 8 cores. The
                                                                                   determine if our system has any false negatives with respect
Rust code symbolic execution for the GPT-4o model took the
                                                                                   to the test cases contained in the original C codebase. We
longest time because GPT-4o generated the highest number of
                                                                                   manually rewrote the existing test cases for libcsv and u8c,
compilable functions that could be symbolically executed.
                                                                                   and used them to test the LLM-transpiled Rust code. This
C. Selected Bugs                                                                   includes 39 tests for libcsv, and 5 tests consisting of 13 test
                                                                                   inputs for u8c. Our results showed that the existing test cases
  Table IV shows the semantic bugs found by RustAssure. We                         could not find any new bugs that RustAssure missed. Only
exclude trivial bugs, such as functions generated with empty                       the bug in the u8next_FAST code generated by GPT-4o-
bodies, and focus only on the semantic bugs. In this section,                      mini, that affects all inputs can be detected by the original
we will discuss two such semantic bugs.                                            end-to-end test cases.
Incorrect pointer increment. Figure 6 shows the simplified                           We also manually reviewed the generated Rust code for
snippet of the scan_option function from the libcsv code-                          these two codebases and did not find any bugs missed by
base. This function parses configuration options of the form                       our system. Finally, as we discuss in §VI-F, we also use
-option=value. The option name can be preceded by an                               FLUORINE[4] to test the transplilation results. Our experi-
arbitrary number of “-” characters. In the C code, the for loop                    ments showed that, due to various crashes, FLUORINE does
in lines 11-23 first scans the option name (lines 12-15). After                    not find any bugs that cannot be revealed by RustAssure.
the execution of line 15, ptr points to the next character to
be consumed. Then, in line 17, if it encounters a = character                      E. End-to-end Comparison against CROWN
indicating the separation between the option name and the                            CROWN [3] is a syntax-driven transpilation toolchain that
value, the C code increments the ptr pointer to consume                            performs ownership analysis to promote raw pointers to safe
and discard the ’=’ symbol, and then stores the value to the                       owned pointers. Table VI compares the translation results of
opt_arg_ptr pointer. However, in the Rust code generated                           RustAssure, using the best performing LLM model—GPT-4o,
                         Original C code                                                         LLM-transpiled Rust Code
 1. int scan_option(                                               1. fn scan_option(
 2.     const char *str,                                           2.    str: *const c_char,
 3.     char opt_buf[],                                            3.    opt_buf: *mut c_char,
 4.     size_t opt_buf_size,                                       4.    opt_buf_size: usize,
 5.     const char **opt_arg_ptr)                                  5.    opt_arg_ptr: *mut *const c_char,
 6.{                                                               6. ) -> i32 {
 7.    // ... skip any leading "-" in str                          7.    // ... some code ...
 8.    const char *ptr;                                            8.    let str = unsafe { CStr::from_ptr(str) }.to_str().unwrap();
 9.    opt_len = 0;                                                9.    let mut opt_len = 0;
10.    ptr = str + 1;                                             10.    let mut ptr = str[1..].trim_start_matches('-');
11.    for ( ; ; ) {                                              11.    for (i, c) in ptr.char_indices() {
12.       if (opt_len < opt_buf_size)                             12.        if opt_len < opt_buf_size {
13.             opt_buf[opt_len] = (char)tolower(*ptr);           13.             opt_buf[opt_len] = c.to_ascii_lowercase() as u8;
14.         ++opt_len;                                            14.        }
15.         ++ptr; // Missing in Rust code                        15.        opt_len += 1;
16.         // Code to handle end of string                       16.        // Code to handle end of string
17.         if (*ptr == '=') {                                    17.        if c == '=' {
18.          ++ptr;                                               18.           unsafe {
19.          *opt_arg_ptr = ptr;                                  19.              *opt_arg_ptr = ptr[i + 1..].as_ptr() as *const c_char;
20.           break;                                              20.           }
21.         }                                                     21.           break;
23.     }                                                         22.        }
24.     // ... more code                                          23.     // ... more code
25.}                                                              24. }




      Fig. 6. Bug detected by RustAssure. Rust code generated by Claude-3.5-Sonnet misses a pointer increment that results in an incorrect output.



                            Original C code                                  F. FLUORINE Comparison
1. struct csv_parser {
2.    size_t blk_size;                                                         FLUORINE [4] is an LLM-based transpiler toolchain that
3.    //... more fields                                                      uses differential fuzzing to test the transpilations. To facilitate
4. };
5. void
                                                                             fuzzing across C and Rust, the toolchain also requires a JSON
6. csv_set_blk_size(struct csv_parser *p, size_t size){                      data-exchange file, specifying critical information, such as the
7.    if (p) p->blk_size = size;                                             number of function arguments and their types.
8.}
                         LLM-transpiled Rust Code                            End-to-end Comparison. FLUORINE first extracts the indi-
1. struct CsvParser<'a> {                                                    vidual functions and their dependencies from the C codebase.
2.    blk_size: usize,                                                       However, the available artifact does not provide the source
3.    //... more fields                                                      code for this step. Instead, the artifact provides the extracted
4. }
                                                                             functions, along with their dependencies, and the JSON-
5. fn csv_set_blk_size(p: &mut CsvParser, size:usize) {
6.     if p.blk_size != 0 { // incorrect check                               mappings for 31 (out of 42) functions for the libopenaptx
7.        p.blk_size = size;                                                 library, along with their Rust transpilations generated using the
8.     }                                                                     GPT-4o model. We transpiled libopenaptx using RustAssure,
9.}                                                                          and performed the comparison against the results provided in
                                                                             FLUORINE’s artifact. Table VII shows the results of this com-
Fig. 7. Bug case detected by RustAssure. Rust code generated by GPT-4o
has a wrong conditional check that results in a failed assignment.
                                                                             parison. Out of the 31 compilable Rust functions generated by
                                                                             FLUORINE, only 10 pass FLUORINE’s differential fuzzing
                                                                             stage, due to crashes in the fuzzer, while RustAssure can
to those of CROWN. The overall compilation success rate for
                                                                             establish the semantic equivalence of 25 out of the 31 functions
RustAssure and CROWN is 89.8% and 97.3%, respectively.
                                                                             handled by FLUORINE, and 33 out of all 38 compilable
Since CROWN is based on syntactic translation, it has a
                                                                             functions generated by RustAssure. Because we manually
higher compilation success rate than RustAssure, and does
                                                                             verified the RustAssure transpilations, we did not fuzz them.
not have any runtime functional divergences, but it does not
                                                                             This is indicated by the N/A value in Table VII.
generate idiomatic Rust code. Across all codebases, RustAs-
sure and CROWN have 35 and 271 raw pointer declarations,                     Effectiveness on Bugs Found by RustAssure. We manually
and 72 and 258 raw pointer uses, respectively, showing that                  crafted the JSON data-exchange file for the 20 buggy functions
RustAssure provides more idiomatic Rust transpilations. Note                 generated by different LLM models, listed in Table IV, and
that opti_png declares 18 raw pointers of which 0 are                        found that only 1 of them can be detected by FLUORINE,
used within the codebase—the raw pointers are strictly passed                with the remaining functions failing to successfully execute to
to dependent libraries. Even for the remaining models, the                   completion.
average raw pointer declaration and use, normalized to the                      Across the 20 tested buggy functions, 14 failures are caused
total number of Rust pointers, is less than that of CROWN.                   by the fuzzer not supporting the argument data type. For
                                                                TABLE IV
             D ETAILS OF BUGS DETECTED BY RUSTA SSURE . N OTE THAT C LAUDE -3.5 INDICATES THE C LAUDE -3.5-S ONNET LLM MODEL

Codebase     LLM Model             Function Name         Bug Description
libcsv       GPT-4o,               csv write2          The C version writes the source string into a char* pointer, and the Rust version writes to a
             GPT-3.5-turbo,                            string slice &str. If the slice is empty, indicating zero capacity, the Rust code returns 0, whereas
             GPT-4o-mini                               the C version returns the length of the input string if the output buffer is NULL.
libcsv       GPT-4o                csv set blk size    The Rust code has an incorrect conditional check. We discuss this in §VI-C.
libcsv       GPT-4o                csv set delim       This function sets the delim_char field into the csv_parser struct. The Rust code has an
                                                       incorrect check where it skips assigning the input value to the field if the current delim_char
                                                       field is “\0”. The original C code simply overwrites the existing character even if it is “\0”.
libcsv       GPT-3.5-turbo         csv free            This function frees the char * field entry_buf inside csv_parser and sets entry_size
                                                       to 0. Rust code uses a raw pointer for entry_buf and contains an incorrect check where it sets
                                                       entry_size to 0 only if entry_buf is not NULL, whereas the original C code unconditionally
                                                       sets the entry_size variable to 0.
libcsv       GPT-4o,               csv fini            This function finalizes the CSV parsing by flushing the last field. The bug arises because in C
             Claude-3.5                                switch statements fall through, but in Rust the match statement does not. The LLM converts a
                                                       switch statement to a match statement, without accounting for the fall-through behavior.
urlparser    GPT-4o                scan decimal number This function scans a string and returns a pointer to the first non-digit character. The Rust code
                                                       returns the digit part instead of the non-digit part.
optipng      Claude-3.5,           scan option         The Rust code has a pointer increment bug. We discuss it in detail in §VI-C.
             GPT-4o-mini
u8c          GPT-4o                u8encode              This function converts a single Unicode code-point (ch) into its UTF-8 byte sequence. The
                                                         generated Rust code does not handle invalid Unicode sequences at all and ultimately tries to
                                                         prematurely add the terminator character at offset -1 of the output string slice, leading to a panic.
u8c          GPT-4o,               u8next                The generated Rust code returns an incorrect value when the input contains invalid Unicode
             GPT-4o-mini                                 sequences. We discuss this bug in detail in §II.
u8c          GPT-4o-mini           u8next FAST           The original C function traverses the raw UTF-8 byte stream one byte at a time and applies
                                                         bitmasks to individual bytes to reconstruct the correct Unicode code-point. The generated Rust
                                                         code applies the bitmasks on the individual codepoints in the already-decoded Unicode sequence,
                                                         instead of individual bytes, generating garbage values.
u8c          Claude-3.5            u8next FAST           When the input string is empty, the C code returns 0 in the output parameter ch*, but Rust does
                                                         not update it at all, leaving any garbage value in it intact.
u8c          GPT-4o,               u8strncpy             This function is a UTF-8 version of strncpy that copies at most n bytes from input to output and
             Claude-3.5                                  then trims any incomplete multibyte sequence at the end so the output will always end with a valid
                                                         UTF- 8 character. The Rust code sets the last byte of the buffer to 0 incorrectly, which will
                                                         overwrite the meaningful byte of the input.
u8c          GPT-4o,               u8strncat             This function appends characters from the source to the end of the target input string and trims any
             GPT-4o-mini                                 incomplete multibyte UTF-8 sequence. The Rust code performs the copy operation without
                                                         trimming the incomplete UTF-8 sequence.



                              TABLE V                                                                       TABLE VI
                  P RECISION AND RECALL ANALYSIS .                                    C OMPARISON OF RUSTA SSURE ( USING GPT-4 O ) VS CROWN.

  Codebase     Model                 TP        FP   FN   Precision   Recall       Codebase      Perc. compiled      Raw Pointer Decls.          Raw Pointer Uses
                                                                                                 Rust CROWN           Rust   CROWN                Rust CROWN
  libcsv       GPT-4o                  5        2    0       71%      100%
               GPT-4o-mini             7        1    0       88%      100%                     Assure               Assure                      Assure
               GPT-3.5-turbo          19        0    0      100%      100%        libcsv         93%        100%            8              23          2        13
               Claude-3.5-Sonnet       5        3    0       63%      100%        urlparser      88%         88%            5              69          1        90
  u8c          GPT-4o                  7        1    0       88%      100%        optipng        87%         98%           18             135          0        66
               GPT-4o-mini             4        1    0       80%      100%        libbmp        100%        100%            0              18          0        37
               GPT-3.5-turbo           0        0    0          -     100%        u8c            89%        100%            4              26         69        52
               Claude-3.5-Sonnet       4        0    0      100%      100%


                                                                                                           TABLE VII
example, for Option type function arguments, FLUORINE’s                         C OMPARISON OF RUSTA SSURE VS FLUORINE ( LIBOPENAPTX LIBRARY ).
fuzzer supports only owned values wrapped in Option<T>
types, and not borrowed references (Option<&T>). More-                            Method           Total    Compilation           Raw       Passes           Passes
                                                                                                Function       Success          Pointer    Fuzzing     Sym. Testing
over, the JSON-based argument mapper assumes that for
                                                                                  FLUORINE             31             31             0           10             25
struct arguments, the transpiled Rust struct definitions                          RustAssure           42             38             1          N/A             33
will have the same field names as their C counterparts, while
RustAssure does not have this restriction. This demonstrates
how FLUORINE requires case-by-case handling of all types.                       supported types. For example, owned values and references are
Ultimately, RustAssure can automatically handle a signifi-                      both mapped to the LLVM IR Pointer type. Moreover, the
cantly a larger set of types because the symbolic execution                     automatic handling of the language level differences, described
occurs at the LLVM IR level, which has a much smaller set of                    in §IV, facilitates the comparison of across different types.
                                                                  TABLE VIII
                        C OMPARISON OF C- TO -RUST TRANSLATION SYSTEMS , APPROACHES , STRATEGIES , AND TESTING METHODS .

System Name              Approach      Detailed Strategy                                                                          Testing Method
LAERTES[1]               Syntactic     Uses compiler feedback to progressively rewrite unsafe pointers to owned pointers          Comparison of dynamic
                         Translation   and references.                                                                            execution traces
CROWN[3]                 Syntactic     Uses novel ownership analysis to derive Rust ownerships and rewrite unsafe                 Existing concrete test cases
                         Translation   pointers to safe Rust.
Tymcrat[30]              LLM-based     Generates multiple Rust function signature candidates for each C function and uses         Manually checked
                                       the translated signatures of callee functions to guide idiomatic translation of callers.
C2SAFERRUST[31]          LLM-based     Analyzes file-level dependencies, providing them to the LLM, in an optimal order.          Existing concrete test cases
RustMap[32]              LLM-based     Decomposes large C projects into smaller units to simplify transpilation.                  Existing concrete test cases
Code Segmentation[33]    LLM-based     Performs code segmentation by organizing C functions in topological order.                 Existing concrete test cases
FLUORINE[4]              LLM-based     Provides translation feedback to LLM, using cross-language differential fuzzer.            Differential fuzzing
SACTOR[34]               LLM-based     Uses C2Rust[35] and LLMs to first translate C code to Rust and then refines                Existing concrete test cases
                                       pointers using ownership information from CROWN[3].
SYZYGY[36]               LLM-based     Uses dynamic analysis to augment LLM-based transpilation.                                  Existing concrete test cases
LAC2R[37]                LLM-based     Uses LLMs to transpile C code to Rust and also generate new test cases.                    LLM-generated test cases
VERT[28]                 LLM-based     Generates “oracle” Rust transpilation using rWASM.                                         Model checking against
                                                                                                                                  rWASM-based oracle.
PR2[29]                  LLM-based     Lifts raw pointers in C2rust [35] output to idiomatic Rust types using LLMs.               Existing concrete test cases.
RustAssure               LLM-          Uses preprocessing and replays already transpiled structs to improve                       Differential symbolic
                         based         compilation success.                                                                       testing.



                           VII. D ISCUSSION                                      approaches combine program analysis techniques, such as,
                                                                                 ownership analysis [34], type analysis [30], code-slicing [32],
Use Cases. RustAssure’s testing approach is not restricted                       code-segmentation [27], control and data flow analysis [31],
to LLM-generated code and can be generalized to codebases                        with LLM-based transpilation. PR2 [29] uses LLMs to perform
transpiled using any approach. As more teams adopt Rust for                      peephole optimization to rewrite raw pointers with idiomatic
its safety guarantees, having an automated checker to validate                   Rust types. Oxidizer [45] translates Go to Rust by combining
functional parity between legacy and rewritten components                        translation rules with LLMs. The benchmark suites [46], [47]
reduces both migration effort and operational risk.                              evaluate the effectiveness of C-to-Rust transpilers.
Enhancements. RustAssure can be improved with a feedback                         Testing and LLMs. Current approaches for testing LLM-
loop from the Semantic Checker that returns divergences to                       generated Rust code use existing test cases [32] and differential
the LLM for targeted re-transpilation. Integrating lightweight                   fuzzing [4]. Vert[28] uses property-based testing and bounded
static analysis to prioritize symbolic paths, improving sup-                     model-checking by compiling both the original C code and the
port for common third-party libraries, and caching partial                       LLM-generated Rust code to WASM [48]. Unlike RustAssure,
executions can improve the symbolic execution coverage.                          however, Vert does not handle any language level differences.
Additionally, reducing false positives by expanding the set                      HoHyun et al. [37] presents an LLM agent that performs a
of language-level normalization patterns can improve RustAs-                     fuzzing-based equivalence test to iteratively refine Rust code,
sure’s equivalence checking. Compositional symbolic execu-                       using LLMs to generate fuzzing inputs. Syzygy [36] combines
tion techniques [38][39] can improve its scalability.                            LLM-driven code and test generation with dynamic analysis.
                                                                                 Various works [49], [50], [51] have used LLMs to generate
                        VIII. R ELATED W ORK                                     new unit tests. These approaches can complement RustAssure.
C-to-Rust Transpilation Techniques. Table VIII provides a                        Symbolic execution. Differential Symbolic Execution [38] is
conceptual comparison with other key approaches. Various                         a technique for finding diverging behavior between different
analysis-based techniques [1], [2], [13], [40] transpile C to                    versions of the same program. RustAssure extends this concept
Rust using the intermediate unsafe Rust output of the C2Rust                     to a cross-language setting. Zhang et al. [52] created an
tool[35]. These approaches guarantee the correctness of the                      approach to automatically verify Rust programs with KLEE.
translation but can produce unidiomatic Rust code[4]. Concrat
[41] focuses on replacing C Lock API with Rust Lock API for                                                  IX. C ONCLUSION
concurrent programs. Hong and Ryu [42] focus on automat-                           We presented RustAssure—an LLM-based C-to-Rust tran-
ically replacing C pointer-based return arguments with Rust                      spiler, that performs differential symbolic testing on the tran-
tuples. GenC2Rust [43] translates C code into generic Rust                       spiled code. Across five C codebases, RustAssure generated
code through static analysis. Fromherz and Protzenko [44]                        compilable Rust functions for 89.8% of all C functions, of
focus on transpiling formally-verified C code to Rust. Various                   which 72% produced equivalent symbolic return values.
                               R EFERENCES                                           [28] A. Z. Yang, Y. Takashima, B. Paulsen, J. Dodds, and D. Kroening,
                                                                                          “Vert: Verified equivalent rust transpilation with large language models
 [1] M. Emre, R. Schroeder, K. Dewey, and B. Hardekopf, “Translating c to                 as few-shot learners,” arXiv preprint arXiv:2404.18852, 2024.
     safer rust,” Proceedings of the ACM on Programming Languages, vol. 5,           [29] Y. Gao, C. Wang, P. Huang, X. Liu, M. Zheng, and X. Zhang, “Pr2:
     no. OOPSLA, pp. 1–29, 2021.                                                          Peephole raw pointer rewriting with llms for translating c to safer rust,”
                                                                                          arXiv preprint arXiv:2505.04852, 2025.
 [2] M. Emre, P. Boyland, A. Parekh, R. Schroeder, K. Dewey, and B. Hard-
     ekopf, “Aliasing limits on translating c to safe rust,” Proceedings of the      [30] J. Hong and S. Ryu, “Type-migrating c-to-rust translation using a large
     ACM on Programming Languages, vol. 7, no. OOPSLA1, pp. 551–579,                      language model,” Empirical Software Engineering, vol. 30, no. 1, p. 3,
     2023.                                                                                2025.
 [3] H. Zhang, C. David, Y. Yu, and M. Wang, “Ownership guided c                     [31] V. Nitin, R. Krishna, L. L. d. Valle, and B. Ray, “C2saferrust: Trans-
     to rust translation,” in International Conference on Computer Aided                  forming c projects into safer rust with neurosymbolic techniques,” arXiv
     Verification. Springer, 2023, pp. 459–482.                                           preprint arXiv:2501.14257, 2025.
 [4] H. F. Eniser, H. Zhang, C. David, M. Wang, M. Christakis, B. Paulsen,           [32] X. Cai, J. Liu, X. Huang, Y. Yu, H. Wu, C. Li, B. Wang, I. N. B. Yusuf,
     J. Dodds, and D. Kroening, “Towards translating real-world code with                 and L. Jiang, “Rustmap: Towards project-scale c-to-rust migration via
     llms: A study of translating to rust,” arXiv preprint arXiv:2405.11514,              program analysis and llm,” arXiv preprint arXiv:2503.17741, 2025.
     2024.                                                                           [33] M. Shiraishi and T. Shinagawa, “Context-aware code segmentation
 [5] “Inside GitHub: Working with the LLMs behind GitHub Copilot,”                        for c-to-rust translation using large language models,” 2024. [Online].
     2024. [Online]. Available: https://github.blog/ai-and-ml/github-copilot/             Available: https://arxiv.org/abs/2409.10506
     inside-github-working-with-the-llms-behind-github-copilot/                      [34] T. Zhou, H. Lin, S. Jha, M. Christodorescu, K. Levchenko, and V. Chan-
                                                                                          drasekaran, “Llm-driven multi-step translation from c to rust using static
 [6] P. Vaithilingam, T. Zhang, and E. L. Glassman, “Expectation vs. experi-
                                                                                          analysis,” arXiv preprint arXiv:2503.12511, 2025.
     ence: Evaluating the usability of code generation tools powered by large
     language models,” in Chi conference on human factors in computing               [35] “C2rust,” 2024. [Online]. Available: https://github.com/immunant/c2rust
     systems extended abstracts, 2022, pp. 1–7.                                      [36] M. Shetty, N. Jain, A. Godbole, S. A. Seshia, and K. Sen, “Syzygy:
 [7] Y. Dong, X. Jiang, Z. Jin, and G. Li, “Self-collaboration code generation            Dual code-test c to (safe) rust translation using llms and dynamic
     via chatgpt,” ACM Transactions on Software Engineering and Method-                   analysis,” 2024. [Online]. Available: https://arxiv.org/abs/2412.14234
     ology, vol. 33, no. 7, pp. 1–38, 2024.                                          [37] H. Sim, H. Cho, Y. Go, Z. Fu, A. Shokri, and B. Ravindran, “Large
 [8] F. Mu, L. Shi, S. Wang, Z. Yu, B. Zhang, C. Wang, S. Liu, and Q. Wang,               language model-powered agent for c to rust code translation,” 2025.
     “Clarifygpt: A framework for enhancing llm-based code generation                     [Online]. Available: https://arxiv.org/abs/2505.15858
     via requirements clarification,” Proceedings of the ACM on Software             [38] S. Person, M. B. Dwyer, S. Elbaum, and C. S. Pǎsǎreanu, “Differential
     Engineering, vol. 1, no. FSE, pp. 2332–2354, 2024.                                   symbolic execution,” in Proceedings of the 16th ACM SIGSOFT Inter-
 [9] R. Pan, A. R. Ibrahimzada, R. Krishna, D. Sankar, L. P. Wassi,                       national Symposium on Foundations of software engineering, 2008, pp.
     M. Merler, B. Sobolev, R. Pavuluri, S. Sinha, and R. Jabbarvand, “Lost in            226–237.
     translation: A study of bugs introduced by large language models while          [39] P. Godefroid, “Compositional dynamic test generation,” in Proceedings
     translating code,” in Proceedings of the IEEE/ACM 46th International                 of the 34th annual ACM SIGPLAN-SIGACT symposium on Principles
     Conference on Software Engineering, 2024, pp. 1–13.                                  of programming languages, 2007, pp. 47–54.
[10] “Openai       models,”     2024.     [Online].     Available:     https : / /   [40] M. Ling, Y. Yu, H. Wu, Y. Wang, J. R. Cordy, and A. E. Hassan, “In
     platform.openai.com/docs/models                                                      rust we trust: a transpiler from unsafe c to safer rust,” in Proceedings of
                                                                                          the ACM/IEEE 44th international conference on software engineering:
[11] “Openai platform: Gpt 4.o mini,” 2024. [Online]. Available: https:
                                                                                          companion proceedings, 2022, pp. 354–355.
     //platform.openai.com/docs/models#gpt-4o-mini
                                                                                     [41] J. Hong and S. Ryu, “Concrat: An automatic c-to-rust lock api trans-
[12] “Meet claude          anthropic,” 2024. [Online]. Available: https:
                                                                                          lator for concurrent programs,” in 2023 IEEE/ACM 45th International
     //www.anthropic.com/claude
                                                                                          Conference on Software Engineering (ICSE). IEEE, 2023, pp. 716–728.
[13] C. D. Hanliang Zhang, Y. Yu, and M. Wang, “Ownership guided c to
                                                                                     [42] ——, “Don’t write, but return: Replacing output parameters with alge-
     rust translation.”
                                                                                          braic data types in c-to-rust translation,” Proceedings of the ACM on
[14] “OpenAI Models,” https://platform.openai.com/docs/models, 2024.                      Programming Languages, vol. 8, no. PLDI, pp. 716–740, 2024.
[15] “What is LLM Temperature?” https://www.ibm.com/think/topics/llm-                [43] X. Wu and B. Demsky, “ GenC2Rust: Towards Generating Generic
     temperature, 2025.                                                                   Rust Code from C ,” in 2025 IEEE/ACM 47th International Conference
[16] Mistral AI, “Mistral 7b,” https://mistral.ai/news/announcing-mistral-7b/.            on Software Engineering (ICSE). Los Alamitos, CA, USA: IEEE
[17] P. Deligiannis, A. Lal, N. Mehrotra, and A. Rastogi, “Fixing rust                    Computer Society, May 2025, pp. 664–664. [Online]. Available:
     compilation errors using llms,” arXiv preprint arXiv:2308.05177, 2023.               https://doi.ieeecomputersociety.org/10.1109/ICSE55347.2025.00127
[18] C. Cadar, D. Dunbar, D. R. Engler et al., “Klee: unassisted and automatic       [44] A. Fromherz and J. Protzenko, “Compiling c to safe rust, formalized,”
     generation of high-coverage tests for complex systems programs.” in                  2024. [Online]. Available: https://arxiv.org/abs/2412.15042
     OSDI, vol. 8, 2008, pp. 209–224.                                                [45] H. Zhang, C. David, M. Wang, B. Paulsen, and D. Kroening, “Scalable,
[19] “The reference manual for the KQuery language,” https://klee-se.org/                 validated code translation of entire projects using large language
     docs/kquery/, 2025.                                                                  models,” 2024. [Online]. Available: https://arxiv.org/abs/2412.08035
[20] Z. Abu-Aisheh, R. Raveaux, J.-Y. Ramel, and P. Martineau, “An exact             [46] G. Ou, M. Liu, Y. Chen, X. Peng, and Z. Zheng, “Repository-level
     graph edit distance algorithm for solving pattern recognition problems,”             code translation benchmark targeting rust,” 2025. [Online]. Available:
     in 4th International Conference on Pattern Recognition Applications and              https://arxiv.org/abs/2411.13990
     Methods 2015, 2015.                                                             [47] A. Khatry, R. Zhang, J. Pan, Z. Wang, Q. Chen, G. Durrett, and
[21] “Clang: a C language family frontend for LLVM,” https : / /                          I. Dillig, “Crust-bench: A comprehensive benchmark for c-to-safe-
     clang.llvm.org/, 2024.                                                               rust transpilation,” 2025. [Online]. Available: https://arxiv.org/abs/
[22] “AST       Matcher     Reference,”    https : / / clang.llvm.org / docs /            2504.15254
     LibASTMatchersReference.html, 2025.                                             [48] WebAssembly         Community      Group,      “WebAssembly,”       https :
[23] “ANTLR (ANother Tool for Language Recognition) ,” https : / /                        //webassembly.org/, 2025, official website, accessed 26 May 2025.
     github.com/antlr/antlr4, 2025.                                                  [49] J. Liu, C. S. Xia, Y. Wang, and L. Zhang, “Is your code generated by
[24] “GraphViz) ,” https://graphviz.org/, 2025.                                           chatgpt really correct? rigorous evaluation of large language models for
[25] “NetworkX - Network Analysis in Python ,” https://networkx.org/, 2025.               code generation,” Advances in Neural Information Processing Systems,
[26] A. Hagberg, P. J. Swart, and D. A. Schult, “Exploring network structure,             vol. 36, pp. 21 558–21 572, 2023.
     dynamics, and function using networkx,” Los Alamos National Labora-             [50] A. Nunez, N. T. Islam, S. K. Jha, and P. Najafirad, “Autosafecoder: A
     tory (LANL), Los Alamos, NM (United States), Tech. Rep., 2008.                       multi-agent framework for securing llm code generation through static
[27] M. Shiraishi and T. Shinagawa, “Context-aware code segmentation                      analysis and fuzz testing,” arXiv preprint arXiv:2409.10737, 2024.
     for c-to-rust translation using large language models,” arXiv preprint          [51] Y. Chen, Z. Hu, C. Zhi, J. Han, S. Deng, and J. Yin, “Chatunitest: A
     arXiv:2409.10506, 2024.                                                              framework for llm-based test generation,” in Companion Proceedings of
     the 32nd ACM International Conference on the Foundations of Software
     Engineering, 2024, pp. 572–576.
[52] Y. Zhang, P. Li, Y. Ding, L. Wang, D. Williams, and N. Meng,
     “Broadly enabling klee to effortlessly find unrecoverable errors in
     rust,” in Proceedings of the 46th International Conference on Software
     Engineering: Software Engineering in Practice, ser. ICSE-SEIP ’24.
     New York, NY, USA: Association for Computing Machinery, 2024, p.
     441–451. [Online]. Available: https://doi.org/10.1145/3639477.3639714
