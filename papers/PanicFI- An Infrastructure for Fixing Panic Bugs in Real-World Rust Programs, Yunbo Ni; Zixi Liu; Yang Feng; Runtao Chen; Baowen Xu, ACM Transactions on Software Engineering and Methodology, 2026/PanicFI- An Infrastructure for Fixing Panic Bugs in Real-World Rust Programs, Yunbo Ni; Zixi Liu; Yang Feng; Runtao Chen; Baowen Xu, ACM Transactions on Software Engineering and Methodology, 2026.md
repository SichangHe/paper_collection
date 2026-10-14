                                        PanicFI: An Infrastructure for Fixing Panic Bugs in
                                        Real-World Rust Programs
                                        YUNBO NI, State Key Laboratory for Novel Software Technology
                                        Nanjing University, China
arXiv:2408.03262v2 [cs.SE] 4 Nov 2024




                                        YANG FENG, State Key Laboratory for Novel Software Technology
                                        Nanjing University, China
                                        ZIXI LIU, State Key Laboratory for Novel Software Technology
                                        Nanjing University, China
                                        RUNTAO CHEN, State Key Laboratory for Novel Software Technology
                                        Nanjing University, China
                                        BAOWEN XU, State Key Laboratory for Novel Software Technology
                                        Nanjing University, China
                                        The Rust programming language has garnered significant attention due to its robust safety features and
                                        memory management capabilities. Despite its guaranteed memory safety, Rust programs suffer from runtime
                                        errors that are unmanageable, i.e., panic errors. Notably, traditional memory issues such as null pointer
                                        dereferences, which are prevalent in other languages, are less likely to be triggered in Rust due to its strict
                                        ownership rules. However, the unique nature of Rust’s panic bugs, which arise from the language’s stringent
                                        safety and ownership paradigms, presents a distinct challenge. Over half of the bugs in rustc, Rust’s own
                                        compiler, are attributable to crash stemming from panic errors. However, addressing Rust panic bugs is
                                        challenging and requires significant effort, as existing fix patterns are not directly applicable due to the design
                                        and feature of Rust language. Therefore, developing foundational infrastructure, including datasets, fixing
                                        patterns, and automated repair tools, is both critical and urgent.
                                           This paper introduces a comprehensive infrastructure, namely PanicFI, aimed at providing supports for
                                        understanding Rust panic bugs and developing automated techniques. In PanicFI, we construct a dataset,
                                        Panic4R, comprising 102 real panic bugs and their fixes from the top 500 most-downloaded open-source crates.
                                        Then, through an analysis of the Rust compiler implementation , we identify Rust-specific patterns for fixing
                                        panic bugs, providing insights and guidance for generating patches. Moreover, we develop PanicKiller, the first
                                        automated tool for fixing Rust panic bugs, which has already contributed to the resolution of 28 panic bugs in
                                        open-source projects. The practicality and efficiency of PanicKiller confirm the effectiveness of the patterns
                                        mined within PanicFI. Furthermore, Panic4R serves as a benchmark for evaluating APR tools focused on Rust
                                        panic bugs. We believe the construction and release of PanicFI could enable the expansion of automated repair
                                        research tailored specifically to Rust programs, addressing unique challenges and contributing significantly to
                                        advancements in this field.
                                        Authors’ addresses: Yunbo Ni, yunboni@smail.nju.edu.cn, State Key Laboratory for Novel Software Technology
                                        Nanjing University, Nanjing, China; Yang Feng, fengyang@nju.edu.cn, State Key Laboratory for Novel Software Technology
                                        Nanjing University, Nanjing, China; Zixi Liu, zxliu@smail.nju.edu.cn, State Key Laboratory for Novel Software Technology
                                        Nanjing University, Nanjing, China; Runtao Chen, 211220018@smail.nju.edu.cn, State Key Laboratory for Novel Software
                                        Technology
                                        Nanjing University, Nanjing, China; Baowen Xu, bwxu@nju.edu.cn, State Key Laboratory for Novel Software Technology
                                        Nanjing University, Nanjing, China.

                                        Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                        provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the
                                        full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored.
                                        Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
                                        prior specific permission and/or a fee. Request permissions from permissions@acm.org.
                                        © 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                        XXXX-XXXX/2024/11-ART $15.00
                                        https://doi.org/XXXXXXX.XXXXXXX


                                                                                                           , Vol. 1, No. 1, Article . Publication date: November 2024.
2                                                             Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu


Additional Key Words and Phrases: Rust, program repair, fault localization

ACM Reference Format:
Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu. 2024. PanicFI: An Infrastructure for Fixing Panic
Bugs in Real-World Rust Programs. 1, 1 (November 2024), 22 pages. https://doi.org/XXXXXXX.XXXXXXX


1   INTRODUCTION
As a statically typed programming language, Rust has gained popularity for its well-known memory
safety guarantees and high performance. Recently, the White House Office of the National Cyber
Director also emphasized the necessity of using programming languages that have fewer memory
safety vulnerabilities [7], and nominating Rust as an example of a memory-safe programming
language. The foundational principles of Rust, including ownership, borrowing, and lifetimes,
enable developers to implement secure and efficient programs. Rust’s emphasis on zero-cost
abstractions and fearless concurrency has significantly contributed to its popularity in systems
programming [15, 30, 31, 34]. This design has led to an increase in the development of widely
recognized software projects written in Rust [3–6, 20].
   Although Rust boasts security features and significantly reduce common bugs such as null
pointer dereference, uninitialized variables, and data races, it could suffer from panic errors, which
are caused by a Rust-specific error-handling mechanism. The severity of the panic is evident from
its typical consequences—program crashes or terminations that may lead to the improper handling
of resources, such as unclosed file descriptors or network connections [68]. Unlike Java’s structured
exception handling framework that manages routine errors, Rust’s panic mechanism is designed for
unrecoverable situations, significantly impacting program stability. Moreover, the Rust compiler,
rustc, written in Rust, also exhibits vulnerabilities to panic bugs. Over half of the issues in Rust
language’s official GitHub repository are categorized as Internal Compiler Errors (ICE) [1], primarily
caused by panic bugs in rustc. Therefore, understanding and resolving panic bugs in Rust is crucial
for ensuring the reliability and stability of Rust programs.
   However, the infrastructure and toolchain supporting the Rust language are not yet as mature as
those for other languages. Most existing code fix datasets and automated program repair (APR) tools
are designed for languages like Java and C/C++. These tools can be challenging to adapt to Rust
due to significant differences in language mechanisms, which may lead to violations of ownership
rules or even failing to compile. For instance, commonly used strategies for fixing null pointer
errors in Java are entirely inapplicable in Rust, as Rust’s language design inherently disallows null
values. Similarly, repair patterns for memory and pointer errors in C/C++ are not transferrable
to handling panic-related bugs in Rust, as Rust’s safety guarantees prevent such memory errors
from occurring. In addition, Rust’s unique memory management model and lifetime rules leads to
a steep learning curve, highlighting the urgent need for infrastructure to support panic bug fixes,
particularly in complex, large-scale and real-world Rust programs.
   Due to the lack of mature infrastructure, such as datasets and repair patterns, fixing panic bugs
can be a tedious and challenging task for Rust developers. Recently, a few program repairing tools
have been proposed for Rust, yet they are insufficient to address the most severe panic-related bugs.
Rust-lancet [65] was developed to tackle bugs related to violations of ownership rules through three
specific strategies. However, these strategies are tailored exclusively to Rust’s ownership rules,
which are verified prior to runtime, making them unsuitable for addressing panic bugs. Similarly,
Ruxanne [50] and RustAssistant [22] focus on common compilation issues, such as incorrect data
types, but these patterns do not effectively mitigate panic bugs.
   To overcome the aforementioned challenges and fill the program understanding gap, in this
paper, we design and implement the first infrastructure PanicFI aiming at automatically fixing

, Vol. 1, No. 1, Article . Publication date: November 2024.
PanicFI: An Infrastructure for Fixing Panic Bugs                                                                3


panic bugs for real-world Rust programs. We have constructed a dataset Panic4R, containing more
than 100 panic bug instances and corresponding fix patches, derived from open source projects in
the ecosystem. Referring to the Rust implementation code, we further perform fix pattern mining
with Rust-specific syntactic features to provide a reference for the community to better understand
panic bugs and fixing strategies. Further, we implement an automated fixing tool for panic bugs,
namely PanicKiller, which first applies dependency analysis for cross-file level error localization,
then combines it with semantic information of the reported errors for fix pattern matching, and
finally outputs sorted patches with scores and descriptions.
   To evaluate the effectiveness of PanicKiller, we conducted extensive experiments on Panic4R.
For fault localization, PanicKiller has achieved high accuracy at different granularities. We also
compared PanicKiller to the LLM-based ChatGPT-4.0, employing both single and multi-round
conversations as baselines. Results demonstrate that PanicKiller outperforms ChatGPT-4.0 in fault
localization and patch generation, highlighting its practicality and reliability. Moreover, PanicKiller
has effectively resolved issues in open-source Rust projects, with 28 panic bug fixes validated and
merged by developers. In summary, the contributions of this work are as follows:
    • Dataset. We constructed the first public dataset for Rust panic bugs, named Panic4R, which
      comprises 102 real bugs and their corresponding fixes from PR records of the top 500 most
      downloaded Rust crates. Each bug-fix pair is meticulously organized and has undergone
      thorough manual verification, facilitating future research.
    • Patterns. We mined a series of fix patterns for panic bugs compliant with Rust syntax. The
      potential application for these mined patterns could be developing automated repair tools,
      providing references for developers, serving as a dataset for fine-tuning LLMs, etc.
    • Tool. We introduced PanicKiller, an automated repair tool specifically for Rust panic bugs,
      designed to address issues in real-world and large-scale Rust programs. Our experiment
      results show that PanicKiller is more efficient than commercial LLM-based tools and has
      successfully resolved 28 open issues in Rust projects on GitHub.

2   PRELIMINARY AND MOTIVATION
Rust language leverages ownership mechanism to manage memory safety and thus naturally
prevent common errors like null pointer errors. This language mechanism enforces strict rules at
compile-time that manage memory usage and ownership, effectively eliminating common memory
issues such as dangling pointers and data races. Rust language present panic mechanism for
unrecoverable errors that signal bugs or critical conditions where continuing execution is not safe.
This mechanism is different from the error handling approaches of many other languages, such as
Java, C, and Python, which allow programs to catch errors and potentially recover from them.
   For example, consider the code
snippet presented in Figure 1, where      1 fn main() {
line 2 declares a variable named name     2    let name: Option<String> = Some(String::from("Alice"));
                                          3    let no_name: Option<String> = None;
of type Option<String>. This type         4    let greeting = match name {
encapsulates a String object and em-      5       Some(n)=>format!("Hi, {}", n), //ownership transferred
                                          6       None => "Hi, guest".to_string(),
ploys Option, a Rust-specific data        7    };
structure designed to handle poten-       8    //  name.unwrap(); // compilation error
                                          9    no_name.unwrap(); // PANIC
tially null values. It uses Some to indi- 10 }
cate the presence of a specific value                  Fig. 1. An example of Rust program.
and None to represent the absence of
any value, as demonstrated in line 3. In the subsequent match expression, the scenarios of Some
and None for name are addressed separately. If name contains a value, this value is assigned to the

                                                       , Vol. 1, No. 1, Article . Publication date: November 2024.
4                                                             Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu


variable n, which is then utilized to construct a new string. During this process, the ownership of n
is transferred from name, rendering name subsequently null. As a result, in line 5, the ownership of
name has been transferred to greeting via the match expression. Consequently, name is now None.
Attempting to unwrap it in line 8 will trigger a compile-time error due to the ownership transfer.
Also, as shown in line 9, calling unwrap() without checking the null value will result in a runtime
error, i.e., panic error, and the program terminates because it cannot handle the exception.
   Motivation. The distinctive memory checking mechanism and stringent ownership transfer rules
in Rust present significant challenges for understanding Rust programs and debugging them. Besides,
if a complex program encounters a panic bug at runtime, much effort is required to perform error
localization and determine the root cause. Although there have been many APR techniques practiced
on Java/C/C++, due to the unique design mechanics of Rust, most of the existing repair patterns
are not applicable to Rust programs. Specifically, Java uses null to represent a variable that points
to no object in memory. While convenient for indicating uninitialized states, this design often leads
to problems, with most of Java’s fix patterns addressing null pointer exceptions [23, 33, 35, 40, 41].
   For example, the function in Listing 2
tries to return a null value while the ex-        public static int test() {
pected return type is int. It would trig-             Integer value = null; // Not allowed in Rust
                                                  +   if (value == null) { // Existing fix pattern
ger a very common null pointer bug, and           +       return 0;
the existing APR tool generally adds an ex-       +   }
                                                      return value; // NullPointerException
tra condition to check if the value is null,      }
then return a random data that fits the type
requirement. However, conventional null Fig. 2. A minimized Java program triggering null pointer
pointer remediation strategies are largely exception and the corresponding fix patch.
ineffective in Rust due to the language’s rigorous handling of null values. As demonstrated in
Figure 1, Rust does not employ a direct equivalent of null. Instead, it utilizes the Option<T> data
type to explicitly manage scenarios where values might be absent. Data that could be null must be
encapsulated within an Option<T>, effectively preventing null pointer errors inherent to Rust’s
design. Consequently, traditional fix patterns that address null pointer issues do not apply to Rust
programs. Besides, we notice that the C/C++’s bug fixing dataset, CVE-Fixes [18, 24], covers a wide
variety of memory bugs such as improper restriction of operations within the bounds of a memory
buffer (CWE-119), out-of-bounds write (CWE-787), and null pointer dereference (CWE-476), etc.
However, these specific bug types are inherently untriggerable in safe Rust programs due to the
language’s stringent safety guarantees. Thus, the methods commonly applied in C/C++ contexts
are not transferable to Rust programs.
   Our work. To address the aforementioned challenges, we construct a systematic infrastructure
infra with dataset, fixing patterns and testing tools, the key components of which are illustrated
in Figure 3. Initially, we gather real-world panic bugs and their corresponding patches from
the ecosystem to construct a dataset, Panic4R, the specifics of which are detailed in Section 3.
Subsequently, referring to the implementation of Rust’s compiler rustc, and its standard libraries,
we identify panic-fix patterns, including abstract patches and natural language descriptions, as
elaborated in Section 4. Finally, we develop an automated fixing tool, PanicKiller, utilizing the
extracted patterns. PanicKiller conducts dependency analysis on source programs, organizes patch
priorities, and generates hybrid fixing suggestions, further explained in Section 5.

3   DATASET CONSTRUCTION
To build a dataset containing real-world panic bugs and their patches, we follow the construction
process of Defects4J [32], which is the most classic dataset in the APR task, and select the top
500 downloaded crates from the public repository of Rust crates [8] for real bugs and fix patches

, Vol. 1, No. 1, Article . Publication date: November 2024.
PanicFI: An Infrastructure for Fixing Panic Bugs                                                                                                                             5


    Dataset Construction: Panic4R                                                                    PanicKiller
                            1                       Rustc and Std Libs
                                                                                               Fix Pattern Mining                          Error             Index
    Real-world Projects            Fix Patch                                                                                              Handler           Checker
                                 Identification
                  Rust                                      Source Code
                                                                                                                                         Condition          Function
                 Crates     2     Real Bugs                                                                                             Expression            Call
                                 Reproduction
          Test Case &
                                                            Documentation               Root Causes
                                                                                        Classification
                                                                                                                    AST-level
                                                                                                                   Minimization
                                                                                                                                                    ……
           Messages         3     Real Bugs
                                   Isolation
                                                                                   Automated Panic Bugs Fixing Tool

                                                                 Rust
                                                                           Control & Data                      Pattern &             Validation      Output: Top-5
          - exp.unwrap()
          + exp.unwrap                                           HIR       Flow Analysis                     Prioritization
            _or_default()
          ……
                                                                                            CEDG
                                                   Panic                        Ordering            Localization              AST-level             Code       Textual
                                                  Program      Backtrace                           List & Scores           Patch Generation         Patch   Interpretation
            Fix Patches         Validation




                                Fig. 3. Key components of the proposed infrastructure PanicFI.


extraction, so as to construct a real dataset. Specifically, we manually employ the following workflow
to collect code and thus guarantee the quality and reliability of the dataset.
   (1) Identifying Real Fix Patches. For each target crate, we review the list of pull requests (PRs). If
a closed PR’s title or description contains keywords like “fixing/repairing panic," it is considered a
potentially valid fix patch. We also assess PRs linked to issues with keywords such as “panic/thread
panicked at...". Then, we further examine the content of the code changes corresponding to PRs and
their related PRs to ensure that they contain fixes for a panic bug. For example, PRs that merely
add or remove test cases without modifying the crate’s source code are not considered relevant to
our dataset. Similarly, changes to the API documentation for the crate are also outside the scope
of our dataset construction. We only select closed PRs to ensure that they are either approved by
developers or submitted by the developers themselves.
   (2) Reproducing Real Bugs. To ensure the reproducibility of panic bugs in each crate, which requires
specific versions, we download the source code for the corresponding commit IDs before and after
the PR commit. The two versions of the target crate are regarded as 𝑉𝑏𝑢𝑔 and 𝑉𝑓 𝑖𝑥 , respectively.
Then, we refer to the description in the PR or the code in the corresponding issue to minimize the
test case 𝑇𝑡𝑒𝑠𝑡 that triggers the bug, i.e., calling the API of the target crate. We ensure that 𝑇𝑡𝑒𝑠𝑡 can
trigger panic bugs and be compiled before and after switching versions, respectively.
   (3) Isolating Real Bugs. In the target crate’s repository, each PR commit may contain more than
one code change, such as adding other functional logic or modifying data structures for new
features, but not as a fix patch for panic. To ensure the accuracy of the fix patches in the dataset,
we manually verified code changes and kept only the patches used to fix the panic bug. If a PR
contains multiple fixes for panic bugs, we also split it into multiple code-fix pairs. As a result, the
patches for 𝑉𝑓 𝑖𝑥 versus 𝑉𝑏𝑢𝑔 have no irrelevant content and are the precise changes necessary to fix
the panic bug. To summarize, each of the real datasets we build contains two crate versions, 𝑉𝑏𝑢𝑔
and 𝑉𝑓 𝑖𝑥 , and a test case 𝑇𝑡𝑒𝑠𝑡 that triggers panic bugs on 𝑉𝑏𝑢𝑔 and is compilable on 𝑉𝑓 𝑖𝑥 . Table 1
shows the details of the real-world dataset Panic4R.

4 FIX PATTERN MINING
To comprehensively identify the causes and fix patterns for panic bugs in Rust programs, we
analyze and infer data from the Rust implementation code [2]. We avoid mining fix patterns solely
from Panic4R to ensure diversity and comprehensiveness in the repair patterns. The root causes
of panic errors in Panic4R may not be exhaustive; for instance, overflow issues may stem from
different operators, such as addition or subtraction, which could be impossible to cover fully through
real-world examples. In contrast, official implementation code includes all such cases and provides
concise examples, making it more suitable for our analysis and collection.

                                                                                    , Vol. 1, No. 1, Article . Publication date: November 2024.
6                                                             Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu


                           Table 1. Statistics of bugs and patches available in Panic4R.

Download         LoC Test LoC # Tests Coverage
         # Bugs                                                                       Crates Involved
Ranking         (Avg.) (Avg.) (Avg.)   (Avg.)
                                                                  syn, rand, regex, aho-corasick, num-traits, clap, serde_json,
     1-50        36     25,882     13.60     2137.2     79.90%
                                                                  strsim, time, idna, hashbrown, proc-macro2, smallvec
                                                                  percent-encoding, chrono, uuid, textwrap, nom, tokio, hy-
    51-100       35     25,988     13.58     409.2      86.50%
                                                                  per, futures, toml
                                                                  httparse, object, rustc-demangle, rustls, form_urlencoded,
    101-150      6      26,516     23.83     1578.6     90.20%
                                                                  gimli
    151-200      3      19,173     16.67      216       85.50%    reqwest, num-bignit, rayon
    201-250      6       3,616     9.70       27.5      80.80%    bumpalo, filetime, fixedbitset, phf, prost
    251-300      3      25,572     10.33       78       63.80%    pest, serde-yaml, libm
    301-350      2      44,882     10.50       17       79.10%    prettyplease, bytemuck
    351-400      2       1,853     12.00      34.5      86.40%    cargo_metadata, tinytemplate
    401-450      5       5,444     25.00      58.7      80.70%    tar, plotters, pretty_assertions, yansi
    451-500      4      28,760     23.25        6       36.50%    crossbeam, brotli-decompressor, indicatif, md5
     Total      102    21,805     15.87      456.27    76.94%                                 51



   In the Rust compiler source code, panic-related error messages are encapsulated within macros
such as panic_const!(). These macros and their accompanying messages provide the diverse types
of panics and their fundamental causes. We compile a summary of these categories and their
descriptions in Table 2. Following this categorization, we examine specific scenarios within each
category. Rust compiler developers mark each panic occurrence with the annotation # Panics,
which details the causes and circumstances of the panic. These annotations are often paired with #
Safety or # Examples, providing either fix strategies or bug-triggering examples. This annotated
information allows us to delineate code-level fix patterns for each panic type.

                  Table 2. Root causes of panic bugs derived from Rust compiler source code.

       Root Causes                           Code Examples
                                             let x: Option<i32> = None;
       Unwrap on None/Invalid value
                                             let y = x.unwrap(); // PANIC
                                             let x = Rc::new(RefCell::new(5));
       Mixed borrowing                       let borrow = x.borrow(); // immutable borrow
                                             let borrow_mut = x.borrow_mut(); // PANIC
                                             async fn my_async_function(cx: &mut Context<’_>) {
                                               let mut task = some_async_task(); // starts async task
       Async functions wrong resume            let result = ready!(task.poll(cx)); // waits until ready
                                               ready!(task.poll(cx)); // PANIC
                                             }
                                             let x: i32 = i32::MAX; // maximum i32 value
       Arithmetic overflow
                                             x + 1; // PANIC
                                             let array = [1, 2, 3, 4, 5];
       Index out of bounds
                                             array[5]; // PANIC
                                             let s = "™"; // a UTF8 string (3 bytes)
       Invalid UTF-8 boundary
                                             &s[1..]; // PANIC
                                             let a = 10; let b = 0;
       Division/Modulus by zero
                                             a / b; // PANIC
       Assertion failed                      assert!(1 == 0); // PANIC
       Unreachable code                      unreachable!(); // PANIC
       Others                                panic!("Here comes a panic!"); // PANIC



, Vol. 1, No. 1, Article . Publication date: November 2024.
PanicFI: An Infrastructure for Fixing Panic Bugs                                                                         7


   For example, Figure 4 showcases a Rust             /// # Panics: Panics if the value is currently
source code snippet annotated to indicate a           /// mutably borrowed. For a non-panicking variant,
                                                      /// use [`try_borrow`] (#method.try_borrow).
panic bug related to the ownership mechanism.
The annotation includes an example where              /// # Examples: An example of panic:
                                                      /// let c = RefCell::new(5);
the panic is triggered by a double borrowing          /// let m = c.borrow_mut();
of a RefCell parameter, which is a Rust smart         /// let b = c.borrow(); // this causes a panic
                                                      pub fn borrow(&self) -> Ref<'_, T> {...}
pointer facilitating internal mutability. To pre-
vent such panics, the annotation suggests us- Fig. 4. The implementation of borrow() function in Ref-
ing the try_borrow() method as an alternative Cell, including annotation about potential panics.
approach. By systematically reviewing all doc-
umented panic instances and their proposed resolutions in the Rust source code, we collect a
comprehensive list of fix strategies.
   To further delineate fix patterns, we convert code modifications into Abstract Syntax Trees (ASTs).
By omitting irrelevant tokens, such as variable names, we identify similar AST transformation
structures that reveal potential fixes for each identified root cause. In total, we identified 19 fix
patterns, which include 34 sub-patterns involving different replacement strategies on one binary
operator. A representative categorization along with corresponding examples is presented in Table 3.
The complete list of patterns and sub-patterns is available on our website.

5     AUTOMATED PANIC BUGS FIXING TOOL
Based on the mined fix patterns, we design a pattern-based automated panic bugs fixing tool, namely
PanicKiller. PanicKiller first locates suspicious expressions based on the stacktrace information
output by the compiler and the dependency flow analysis of the original program. Then, combined
with the semantic information of the errors, PanicKiller generates a series of patches for each fault
location. Finally, PanicKiller sorts all the patches with verification and matching scores calculation,
and outputs the top-5 ranked patches along with the corresponding natural language interpretation.

5.1    Fault Localization
When a panic occurs, Rust initiates the unwinding process, meticulously tracing back up the stack to
ensure the cleanup process. The error message is further supplemented with stacktrace information,
and based on it, PanicKiller initially extracts suspicious locations, including file paths, column and
row numbers. Considering that the precise locations of bugs might not be explicitly disclosed in the
stacktrace [52], prior research suggests that the actual buggy location is apt to exhibit structural
resemblances to the expressions detailed in the stacktrace. This indicates that the exact location
could be involved in other expressions and is dependent on those specified within the stacktrace.
   To capture the dependency relationship, we construct a Code Element Dependency Graph
(CEDG) by utilizing the High-level Intermediate Representation (HIR), which serves as one of
the intermediary forms during Rust’s compilation process. For the assignment statements or
expressions, the variables on the left-hand side values are dependent on the right-hand side values.
When it comes to function invocations, there may exist dependencies in the parameters of functions,
so we delve deeper into the function to uncover additional dependencies. Leveraging the transitivity
of the dependency relationship, we iteratively construct the CEDG. Then, based on the constructed
dependency relationship, we first define the confidence score of each localized element 𝑒𝑖 as follows:

                                              min(𝐷𝑖𝑠𝑡 (stacktrace, 𝑒𝑖 ), 𝜆)
                                 𝐶𝑜𝑛𝑖 = 1 −                                  ,   𝜆≥1                                    (1)
                                                           𝜆
   where 𝐷𝑖𝑠𝑡 (stacktrace, 𝑒𝑖 ) denotes the shortest distance on the dependency graph between
element 𝑒𝑖 and any of the elements in the stacktrace. A constant 𝜆 is used to normalize the

                                                                , Vol. 1, No. 1, Article . Publication date: November 2024.
8                                                                Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu


                    Table 3. Partial fix patterns derived from the Rust implementation code.

Fix Patterns                Code Changes                                      Interpretation Templates                  Example PRs
                            - x = exp.unwrap();                               When unwrapping on [value], add
                            + x = match exp.unwrap() {                        match arms to [variable] after un-
                                                                                                                        serde_json (PR 757)
Insert Match Unwrapper      +   Some(_) => { exp.unwrap() }                   wrapping to handle all possible cir-
                                                                                                                        nom (PR 1032)
                            +   _ => { return }                               cumstances to avoid panics caused by
                            + };                                              unwrapping on None/Invalid values.
                            // polling operation                              Advance the statement [state
                            + stmt1 // advance statement                      changer] to avoid incorrect state         futures (PR 2250)
Reorder State Changer
                            // other statements                               resumption after asynchronous             opendal (PR 4013)
                            - stmt1 // state changer                          functions have completed.
                                                                              Delete the second mutable borrow of
                            data.borrow() // immutable borrow                 [data] when there exists immutable        StackOverflow
Delete Second Borrow
                            - data.borrow_mut()                               borrow to avoid ownership violation       (SO 1)
                                                                              panics.
                                                                              Replace the [original handler] with
                            - x.expect() + x.unwrap()                         [new handler] to avoid panics caused
Mutate Error Handler                                                                                                    clap (PR 4480)
                            // or unwrap_or_default/else                      by incorrect error handling like [orig-
                                                                              inal handler].
                            - a op b
                                                                              Replace basic arithmetic operations
                            1. Mutate to wrapping/saturating function:                                                  regex (PR 996)
                                                                              [operator] with safer operations [call
                            + a.wrapping/saturating_op(b)                                                               chrono (PR 1294)
Mutate Binary Operator                                                        name] to handle arithmetic [operator]
                            2. Mutate to checked function:                                                              chrono (PR 1023)
                                                                              overflow panics. Note that [explana-
                            + a.checked_op(b).unwrap()                                                                  chrono (PR 686)
                                                                              tion].
                            // or unwrap_or_default/else
                            1. Check the index:
                            + if index > arr.len() { return }                 Implement range checking for the [in-
                            2. Check start/end of range if index is range:    dex] of indices [array name] to de-
                                                                                                                    idna (PR 658)
Insert Range Checker        + if end > x.len() { return } or                  termine whether [condition], avoid-
                                                                                                                    idna (PR 655)
                            + if start >= x.len() { return }                  ing index out of bounds or exceed the
                            3. Check whether start > end if index is range:   boundary.
                            + if start > end { return }
                                                                              Mutate [index] in indices [array
Mutate Index Expression - array[index1]         + array[index2]               name], avoiding index out of bounds       textwrap (PR 391)
                                                                              or exceeding the boundary.
                            - if cond1   + if cond2 && cond1                  Adjust conditions within if statements
Mutate Condition                                                                                                        idna (PR 865)
                            // add after if-let expression                    to check whether [condition].
                                                                              Insert an unsafe block when [precon-
                            // necessary condition
Insert Unsafe Block                                                           dition] is met to change the behaviour    nom (PR 370)
                            - exp1 + unsafe { exp2 }
                                                                              of [variable].
                                                                              Replace the original call [call name]
Mutate Method                                                                                                           hyper (PR 2410)
                            - x.y([params])      + x.z([params])              with another [new call name] with
Invocation                                                                                                              serde_json (PR 493)
                                                                              the same parameters.
                                                                              Add new method call [call name] to        chrono (PR 1254)
Insert Call Invocation      - x.y()    + x.y().z()
                                                                              [variable].                               nom (PR 1618)



confidence score thus ensuring it is scaled within a meaningful range. In our work, we set 𝜆 = 2
according to an existing study [44], which has proved that it has the optimal performance. It involves
incorporating both the precise locations and the code elements dependent on those identified,
ensuring a more comprehensive analysis.
   In addition to the confidence score, the presence of suspicious files within the stacktrace can also
impact fault localization. On the one hand, files that frequently appear in the stacktrace tend to be
more critical to the execution path leading to the error, making them more likely to be associated
with the fault. On the other hand, within an expanded stacktrace, a shallower depth suggests a
stronger connection to the error’s origin [61]. Thus, PanicKiller computes the suspicion score 𝐿𝑜𝑐𝑖
for each location as follows:

                                                  𝐿𝑜𝑐𝑖 = 𝑁 × (1/𝐷 + 𝐶𝑜𝑛𝑖 )                                                               (2)
  where 𝑁 denotes the number of times a particular file of 𝑒𝑖 occurs within the stacktrace, and 𝐷
represents the depth of the location in the stacktrace sequence. For each buggy source code and

, Vol. 1, No. 1, Article . Publication date: November 2024.
PanicFI: An Infrastructure for Fixing Panic Bugs                                                                                                                                           9


the corresponding stacktrace, PanicKiller calculates the score for each element 𝑒𝑖 after constructing
a dependency graph to determine the ranking of a suspect location.

5.2      Pattern-based Patch Generation
Based on the suspicious locations, PanicKiller iteratively attempts to match each location with
the mined fix patterns, which are illustrated in Section 4. Considering that there may be multiple
suspicious locations and matched patterns, resulting in multiple combinations of fixes, we sort
them based on validation.
   Patch validation. For the APR task, it is important to guarantee that the generated patches
repair the bug as well as do not affect the original semantics. In our work, we incorporate cargo-test,
a built-in tool in Rust’s package manager, to automate the execution of regression tests. After
performing the validation, the patches would have several cases: (1) The panic is eliminated and
all the test cases execute with the same result as before. Our goal is to generate these patches,
which indicate the most likely correct fix. (2) The panic is eliminated but the execution results of
some test cases are not consistent with the original program. This suggests that the patch may
have introduced logical modifications that cause the semantic inconsistency. (3) The panic is not
eliminated and we don’t evaluate the regression testing because it’s not a correct fix. By regression
testing, we can effectively filter out patches that might introduce new errors or exhibit overfitting
to test suites, thereby enhancing the reliability and robustness of fixing.
   Patch prioritization. For each suspicious location, PanicKiller iteratively employs the mined
fix patterns. If the corresponding AST has a structure that matches a specific pattern, it is applied
to generate a patch; otherwise, it is discarded. Note that even after a pattern has been applied to an
expression, additional patterns might be identified as one delves deeper into the AST. Consequently,
a suspicious location may correspond to more than one resulting patch. For all the generated
patches, PanicKiller combines the scores and validation results mentioned above to perform the
patch ordering. Specifically, patch prioritization is guided by three factors: (1) the confidence score
for fault localization 𝐶𝑜𝑛𝑖 , (2) the similarity score of the patch’s interpretation, the templates of
which are shown in Table 3, to the error messages, and (3) the results from the regression test
validation. PanicKiller ranks each patch based on the cumulative sum of the two scores. For patches
that achieve identical scores, preference is given to those that successfully pass regression testing.
   Finally, PanicKiller outputs a top-5 ranked list of mixed-form fixing recommendations. To address
patch interpretability issues [26], PanicKiller provides each code patch alongside its natural language
explanation, as detailed in Table 3. This description ensures developers receive a clear understanding
of the modifications and the patterns applied in each patch.

 1 arr[num1] = a.unwrap();                - arr[num1] = a.unwrap();                           arr[num1] = a.unwrap();                                  arr[num1] = a.unwrap();
 2 // ...                                 + arr[num1] = match a.unwrap() {                    // ...                                                   // ...
 3 // index out of bounds panic!          +      Some(_) => a.unwrap(),                       - if arr[num2] – num3 > 0 {                              + if num2 > arr.len() {
 4 if arr[num2] – num3 > 0 {              +      _ => return Error; };                        + if arr[num2].saturating_sub(num3) > 0 {                +      return Error; }
 5     return 0;                          // ...                                                   return 0;                                           if arr[num2] – num3 > 0
 6 }                                      if arr[num2] – num3 > 0 {return 0;}                 }                                                        { return 0; }
  (a) The panic bug-triggering example.      (b) Patch 1: Insert Match Unwrapper.                       (c) Patch 2: Mutate Binary Operator.          (d) Patch 3: Insert Range Checker.
                               Patch             Fix Pattern                    Score (Coni+Loci)                    Validation                Rank
                               Patch 1      Insert Match Unwarpper                1.1 (0.7 + 0.4)                        Test fail              3
                               Patch 2      Mutate Binary Operator                1.1 (1.0 + 0.1)                        Test pass              2
                               Patch 3       Insert Range Checker                 1.7 (1.0 + 0.7)                        Test pass              1
                                                                     (e) Prioritization results for the three patches.



                               Fig. 5. A panic bug-triggering example and its corresponding patches.
   A running example. Figure 5 (a) presents a code example that triggers a panic bug caused
by an index out-of-bounds error. Assuming that PanicKiller has identified lines 1 and 4 as suspi-
cious locations, with confidence scores of 0.7 and 1, respectively, as determined by Equation 2.

                                                                                                    , Vol. 1, No. 1, Article . Publication date: November 2024.
10                                                            Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu


Subsequently, PanicKiller iteratively applies each pattern to these locations. For line 1, PanicKiller
identifies a method call of unwrap(), thus the Insert Match Unwrapper pattern is applied, and patch
1 is depicted in Figure 5 (b). For line 4, PanicKiller initially identifies a binary expression containing
a subtraction operator, and the Mutate Binary Operator pattern is employed, as illustrated as patch 2
in Figure 5 (c). Further, PanicKiller analyzes the deeper structure and identifies an index expression,
for which the Insert Range Checker pattern is applied to arr[num2]. Patch 3 is depicted in Figure 5
(d). The prioritization of patches is shown in Figure 5 (e). Patch 3 ranks first with the highest score
of 1.7, having passed the regression tests. Patch 2 is second because, although it scored the same as
patch 1, it passed the regression tests while patch 1 failed. Consequently, PanicKiller outputs this
ranked patch list with their interpretations, organized by scores and test results.

5.3    Tool Evaluation
To the best of our knowledge, there currently exists no dedicated tool for the automated repair
of Rust panic bugs. Therefore, we conducted an evaluation on the Panic4R dataset to validate the
effectiveness of PanicKiller. We mainly compare the effectiveness of PanicKiller with LLM-based
approaches. We follow a standardized process when applying ChatGPT 4.0 as a baseline method
for fault localization and program repair. For each target, we upload a zip archive containing the
entire Rust project, the test case triggering the panic, and relevant panic information. We then use
a consistent prompt template, as shown below:
     I have uploaded a source code package of a Rust crate [crate-name], [crate-zip]. When using this crate with the
 following test case: [main.rs], it went panic, the panic information is as follows: [panic_info].
     [Location Prompt] + Based on the locations, provide the top 5 fixing code to fix this panic. Don’t explain anything
 about code, just show me the suspicious locations and patches.

  As for the [Location Prompt], because we verify the correctness of the generated patches
with/without the correct error location, the template are specifically as follows:

 • Without Perfect Location: Please give me the top 5 suspicious fault locations in the crate, including their path,
    line number and column number.
  • With Perfect Location: The error location is: [perfect-location].

    Because ChatGPT may fail to produce bug localization or repair patches as instructed, we employ
a baseline involving multiple interactions with ChatGPT. Initially, we assess ChatGPT’s output for
completeness and iterate the query process up to three times, correcting for any missing information.
If, after three attempts, localization or repair details remain unattained, we classify the effort as a
ChatGPT repair failure. The inquiry prompts for missing information are as follows:

 • Localization: Please provide me directly with the exact file path, code line and column numbers where the error
    was located.
  • Fixing: Based on the mislocalization information you provided, please provide me with the specific code to fix it.


5.3.1 Effectiveness of Fault Localization. For the task of bug localization, while existing techniques
typically rely on additional natural language descriptions from bug reports or test suites [66], our
tool, PanicKiller, solely utilizes the error message from the Rust compiler and the accompanying
stacktrace information. The absence of extra data makes some existing techniques unsuitable as
baselines for our approach. Consequently, we select three categories of general methods as baseline
techniques to compare with the fault localization capabilities of PanicKiller.
   (1) Conventional Localization Approaches. When only error messages and stacktraces are
available, fault localization can be deduced from these elements[28, 44, 61].

, Vol. 1, No. 1, Article . Publication date: November 2024.
PanicFI: An Infrastructure for Fixing Panic Bugs                                                               11


    • Panic: When a panic occurs, the compiler outputs an error message indicating the specific
       line of code where the exception occurred. This line is then considered as the fault location.
    • Random: The compiler outputs stacktrace information that includes a list of suspicious code
       locations. From this list, a location is randomly selected as the detected fault location.
    • Similarity: We evaluate the textual error message and identify the fault location by finding
       the code line with the highest similarity score.
   (2) Spectrum-based Localization Approaches. Spectrum-based fault localization (SBFL) [11]
approaches analyze the execution traces of a program by examining which components of the
program were executed when a failure occurred and which were not. By applying statistical analysis
to these execution spectra, SBFL effectively pinpoints the components that are most likely to be
responsible for software failures. In our experiments, we collect test cases for each crate in Panic4R,
the majority of which passed; those that triggered a panic bug were classified as failed cases. Based
on the calculated scores from the spectral analysis, we sort all the lines of code and then select the
top 5 locations as the fault localization results.
    • Tarantula: The Tarantula method [29] calculates the suspicious location by comparing the
       ratios of passed to failed test cases that execute a given code line. A higher ratio of failed
       to total test executions in a component increases its likelihood of being faulty. We rank the
       ratio of each code line as the most likely fault candidates.
    • Ochiai: The Ochiai algorithm [43] applies the cosine similarity measure between failed test
       cases and the execution of given code lines. The score is derived from the intersection of
       failing test cases with the components they execute, normalized by the square root of the
       product of the total number of failures and the number of times a component is executed
       during those failures.
   (3) LLM-based Localization Approaches. It is feasible to directly submit source code, error
messages, and requirements to an LLM.
    • ChatGPT-4 (GPT-4): Due to ChatGPT-3.5’s limitations in handling files, we apply the most
       popular commercial software ChatGPT 4.0 as a baseline.
    • Multiple rounds of inquiries with ChatGPT-4 (GPT4-multi): When interacting with ChatGPT
       4.0, we inquire multiple rounds with additional questions manually.
   To comprehensively assess the effectiveness of fault localization through various techniques,
we employ three granularity levels for locating panics: file, statement, and expression levels. As
illustrated in Table 4, the localization accuracy of PanicKiller at all three granularities is higher
than the other baselines, which indicates the effectiveness of PanicKiller. In addition, all methods
perform better on the small-scale dataset compared with the large-scale dataset. This result is as
expected, because on large-scale projects, the stack unfolding information could be more complex
and harder to analyze the dependency for fault localization. The effectiveness of the random
method is relatively close to PanicKiller, especially on small-scale datasets and top-5 prediction
results, which suggests that if the localization is in the stack-expanded list, random selection can
be effective, but as soon as in-depth dependency analyses are required on large-scale dataset, the
random method fails outright. The similarity-based selection techniques are the least effective
in terms of fine-grained localization accuracy, implying that relying on natural language alone
does not accurately capture the semantic information of complex practical code, resulting in low
localization accuracy.
   As for comparing with LLM-based approaches, the localization accuracy of ChatGPT4 is basically
the same for single and multi-round conversations due to a limited understanding of an entire
Rust project. This limitation is evident in the significant drop in success rate as the size of the Rust
project increases. Throughout our experiments, we observed instances where ChatGPT failed to

                                                       , Vol. 1, No. 1, Article . Publication date: November 2024.
12                                                              Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu


parse files accurately, providing only general suggestions that are impractical for effective fault
localization. These observations highlight the inconsistency and limitations of relying on LLMs for
accurate bug localization in complex codebases.
   For spectrum-based methods, both Ochiai and Tarantula methods exhibited low accuracy, partic-
ularly within larger datasets, where Ochiai, for instance, showed zero accuracy in the top-1 ranking
across all levels. This may because that panic bugs in Rust program constitute a unique category of
errors, usually not originating from traditional issues in loops or conditional logic. The unit test
cases within each crate aim to validate logical functionality, thus testing pass and fail conditions
that may not align with detecting panic-related bugs. This mismatch could reduce the effectiveness
of spectrum-based techniques. In addition, facing with real-world and large-scale programs that
contain thousands of lines code, applying spectrum-based techniques incurs considerable time
overheads, further limiting their practicality. For example, calculating the spectrum score for a
project could takes more than 3 hours in average for the large-scale dataset, while PanicKiller takes
about 1 minute in average.

     Table 4. The correctness of tools on Panic4R datasets, with different granularities of error localization.

                               Panic4R-Small (61)                    Panic4R-Large (41)                    Total (102)
          Tool
                        File         Stmt       Expr          File         Stmt       Expr       File        Stmt          Expr
          panic    41 (67.2%)      30 (49.2%)   30 (49.2%) 22 (53.7%) 10 (24.4%) 10 (24.4%)   63 (61.8%)   40 (39.2%)    40 (39.2%)
         random    33 (54.1%)      14 (23.0%)   13 (21.3%) 14 (34.1%) 7 (17.1%)   6 (14.6%)   47 (46.1%)   21 (20.6%)    19 (18.6%)
        similarity 13 (21.3%)        0 (0%)       0 (0%)    7 (17.1%)  1 (2.4%)     0 (0%)    20 (19.6%)    1 (1.0%)       0 (0%)
          Ochiai     0 (0%)          0 (0%)       0 (0%)     0 (0%)     0 (0%)      0 (0%)      0 (0%)       0 (0%)        0 (0%)
 Top-1
        Tarantula   1 (1.6%)        1 (1.6%)     1 (1.6%)    0 (0%)     0 (0%)      0 (0%)     1 (1.0%)     1 (1.0%)      1 (1.0%)
          GPT-4    42 (68.9%)      28 (45.9%)   19 (31.1%) 10 (24.4%)  4 (9.8%)    3 (7.3%)   52 (51.0%)   32 (31.4%)    22 (21.6%)
       GPT4-multi 43 (70.5%)       28 (45.9%)   19 (31.1%) 10 (24.4%)  4 (9.8%)    3 (7.3%)   53 (52.0%)   32 (31.4%)    22 (21.6%)
       PanicKiller 45 (73.8%)      33 (54.1%)   32 (52.5%) 22 (53.7%) 13 (31.7%) 13 (31.7%)   67 (65.7%)   46 (45.1%)    45 (44.1%)
         random    46 (75.4%)      29 (47.5%)   29 (47.5%) 17 (41.5%) 8 (19.5%)   8 (19.5%)   63 (61.8%)   37 (36.3%)    37 (36.3%)
        similarity 21 (34.4%)       1 (1.6%)     1 (1.6%)  10 (24.4%)  1 (2.4%)     0 (0%)    31 (30.4%)    2 (2.0%)      1 (1.0%)
          Ochiai    3 (5.0%)        3 (5.0%)     3 (5.0%)    0 (0%)     0 (0%)      0 (0%)     3 (2.9%)     3 (2.9%)      3 (2.9%)
 Top-3 Tarantula    2 (3.3%)        2 (3.3%)     2 (3.3%)    0 (0%)     0 (0%)      0 (0%)     2 (2.0%)     2 (2.0%)      2 (2.0%)
          GPT-4    43 (70.5%)      29 (47.5%)   20 (32.8%) 12 (29.3%)  4 (9.8%)    3 (7.3%)   55 (53.9%)   33 (32.4%)    23 (22.5%)
       GPT4-multi 44 (72.1%)       29 (47.5%)   20 (32.8%) 12 (29.3%)  4 (9.8%)    3 (7.3%)   56 (54.9%)   33 (32.4%)    23 (22.5%)
       PanicKiller 49 (80.3%)      38 (62.3%)   37 (60.7%) 28 (68.3%) 19 (46.3%) 18 (43.9%)   77 (75.5%)   57 (55.9%)    55 (53.9%)
         random    48 (78.7%)      33 (54.1%)   33 (54.1%) 22 (53.7%) 13 (31.7%) 12 (29.3%)   70 (68.6%)   46 (45.1%)    45 (44.1%)
        similarity 25 (41.0%)        1 (1.6%)     1 (1.6%) 13 (31.7%)  1 (2.4%)    0 (0%)     38 (37.3%)    2 (2.0%)      1 (1.0%)
          Ochiai    9 (14.8%)       9 (14.8%)    9 (14.8%)   0 (0%)     0 (0%)     0 (0%)      9 (8.8%)     9 (8.8%)      9 (8.8%)
 Top-5 Tarantula     6 (9.8%)        6 (9.8%)     6 (9.8%)  1 (2.4%)   1 (2.4%)   1 (2.4%)     7 (6.9%)     7 (6.9%)      7 (6.9%)
          GPT-4    46 (75.4%)      30 (49.2%)   21 (34.4%) 14 (34.1%)  4 (9.8%)   3 (7.3%)    60 (58.8%)   34 (33.3%)    24 (23.5%)
       GPT4-multi 47 (77.0%)       30 (49.2%)   21 (34.4%) 14 (34.1%)  4 (9.8%)   3 (7.3%)    61 (59.8%)   34 (33.3%)    24 (23.5%)
       PanicKiller 49 (80.3%)      38 (62.3%)   37 (60.7%) 29 (70.7%) 20 (48.8%) 19 (46.3%)   78 (76.5%)   58 (56.9%)    56 (54.9%)



5.3.2 Fixing Effectiveness. Referring to existing research on APR [49], we categorize the generated
patches into three types and verify their proportion: (1) panic-eliminated patches, where the panic
bug is resolved but some regression test cases fail; (2) plausible patches, where the panic bug
is successfully fixed and all test cases pass; and (3) correct patches, which are plausible patches
that have also been manually verified for semantic correctness. The evaluation results are shown
in Table 5. Overall, we can conclude that PanicKiller significantly surpasses the performance of
automated repairs conducted by GPT-4. Notably, within the large-scale dataset, GPT-4 fails to
generate any viable patches, the reason of which is closely tied to GPT-4’s challenges with fault
localization, as elaborated in Section 5.3.1. Moreover, we find that LLM-based methods frequently
overlooks the code context when generating patches, resulting in the generated program failing to
compile instead. For example, it may attempt to resolve panics by altering a method’s return type
directly or by incorporating new logic, which results in both compilation and semantic errors.

, Vol. 1, No. 1, Article . Publication date: November 2024.
PanicFI: An Infrastructure for Fixing Panic Bugs                                                                    13


         Table 5. The number of panic-eliminated/plausible/correct patches of different tools on Panic4R.

                        Panic4R-Small (61)           Panic4R-Large (41)               Total (102)
         Tool
                   Eliminated Plausible Correct Eliminated Plausible Correct Eliminated Plausible Correct
          GPT-4      6  9.8%    6 9.8% 0 0% 0      0%         0  0% 0 0%             6  5.9%       6 5.9% 0 0%
Top-1




        GPT4-multi 8 13.1%      8 13.1% 0 0% 0     0%         0  0% 0 0%             8  7.8%       8 7.8% 0 0%
        PanicKiller 29 47.5%   19 31.1% 4 6.6% 10 24.4%       7 17.1% 4 9.8%        39 38.2%      26 25.5% 8 7.8%
          GPT-4      6  9.8%    6 9.8% 1 1.6% 0      0%        0  0% 0 0%       6  5.9%            6 5.9% 1 1.0%
Top-3




        GPT4-multi 8 13.1%      8 13.1% 1 1.6% 0     0%        0  0% 0 0%       8  7.8%            8 7.8% 1 1.0%
        PanicKiller 32 52.5%   23 37.7% 12 19.7% 13 31.7%     10 24.4% 7 17.1% 45 41.1%           33 32.4% 19 18.6%
          GPT-4      7 11.5%    7 11.5% 1 1.6% 0     0%        0  0% 0 0%       7  6.9%            7 6.9% 1 1.0%
Top-5




        GPT4-multi 9 14.8%      9 14.8% 1 1.6% 0     0%        0  0% 0 0%       9  8.8%            9 8.8% 1 1.0%
        PanicKiller 35 57.4%   25 41.0% 12 19.7% 14 34.1%     10 24.4% 7 17.1% 49 48.0%           35 34.3% 19 18.6%



   As shown in Table 6, even with perfect location information, PanicKiller consistently outperforms
GPT-4. This indicates that PanicKiller’s patch generation capability is superior to that of GPT-4,
even after multiple iterations. Compared with the results in Table 5, PanicKiller only slightly
improves its fixing effectiveness with perfect location information. While it does generate new
plausible or correct patches, it sometimes fails to recreate some of its previous patches without
perfect locations. This is because some patches were applied at related but different locations,
such as within a method call hierarchy, and still effectively fixed the issue. However, the provided
location may interfere with the selection of fix patterns. As for ChatGPT, when provided with exact
fault locations, it can generate a few effective patches for large datasets, a stark improvement over
its complete failure without precise locations. This further underscores the deficiency in GPT-4’s
fault localization capabilities.

Table 6. The number of panic-eliminated/plausible/correct patches of different tools on Panic4R with perfect
locations.

                        Panic4R-Small (61)           Panic4R-Large (41)               Total (102)
         Tool
                   Eliminated Plausible Correct Eliminated Plausible Correct Eliminated Plausible Correct
          GPT-4      6  9.8%    4 6.6% 4 6.6% 3     7.3%     3 7.3% 3 7.3%          9  8.8%       7 6.9% 7 6.9%
Top-1




        GPT4-multi 6    9.8%    4 6.6% 4 6.6% 3     7.3%     3 7.3% 3 7.3%          9  8.8%       7 6.9% 7 6.9%
        PanicKiller 33 54.1%   24 39.3% 7 11.5% 10 24.4%     7 17.1% 4 9.8%        43 42.2%      31 30.4% 11 10.8%
          GPT-4      6  9.8%    5 8.2% 4 6.6% 3      7.3%     3 7.3% 3 7.3% 9     8.8%            8 7.8% 7 6.9%
Top-3




        GPT4-multi 6    9.8%    5 8.2% 4 6.6% 3      7.3%     3 7.3% 3 7.3% 9     8.8%            8 7.8% 7 6.9%
        PanicKiller 36 59.0%   27 44.3% 15 24.6% 13 31.7%    11 26.8% 9 22.0% 49 48.0%           38 37.3% 24 23.5%
          GPT-4      6  9.8%    5 8.2% 4 6.6% 4      9.8%     4 9.8% 4 9.8% 10 9.8%               9 8.8% 8 7.8%
Top-5




        GPT4-multi 6    9.8%    5 8.2% 4 6.6% 4      9.8%     4 9.8% 4 9.8% 10 9.8%               9 8.8% 8 7.8%
        PanicKiller 36 59.0%   27 44.3% 15 24.6% 13 31.7%    11 26.8% 9 22.0% 49 48.0%           38 37.3% 24 23.5%


  Regarding to the panic-eliminated and plausible patches, we believe that, when coupled with
the textual interpretations derived from our mined patterns, panic-eliminated patches can aid
developers repair their program efficiently. This is because the failure of some patches to pass
the regression tests may be attributed to additional logic after the patch is applied, which is
beyond APR tool’s capabilities. Such panic-eliminated fixes, with minimal manual oversight, can be
comprehensively resolved, thereby reducing the developers’ burden in understanding panic bugs
and evaluating alternative functions.

                                                            , Vol. 1, No. 1, Article . Publication date: November 2024.
14                                                              Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu


5.3.3 Efficiency. Fig 6 and Table 7 show the distribution of time spent on PanicKiller and manual
fixes. On average, PanicKiller requires about one minute to repair panics, whereas manual repairs
can take days. An interesting observation is that the average time of both PanicKiller and manual
repair are generally longer for smaller datasets. For PanicKiller, this extended time is mainly due to
the large test suites in some libraries, which lengthen the validation process. In terms of manual
repairs, one notable case involved a panic bug that took over two years to fix, largely due to delayed
maintenance by developers, resulting in a notably prolonged repair time for a smaller dataset.
   In examining real-world PRs, we found a few key
factors that potentially affect the bug-fixing time. De-                                 Median: 12.76 seconds
                                                                                                                                       Repair in practice



                                                                                                                             Median: 3.22 days

velopers often spend several days discussing issues Panic4R  (Small)
due to the need to comprehend error messages, un-                                            Median: 22.09 seconds
                                                                                                                               Median: 4.90 days
                                                            Panic4R
derstand collaborators’ code, and locate faults. Con- (Large)
versely, PanicKiller provides detailed explanations                    10   10   10  0     10
                                                                                  Time (second)
                                                                                               110   10      2       3   4             5



with fix patches to streamline the review process and           Fig. 6. Experiment results of efficiency.
improve developer understanding. Additionally, maintainers sometimes request multiple revisions
of a submitted fix, requiring different approaches and thus increasing time and effort. PanicKiller
addresses this by generating a range of patches, ranking them based on confidence scores and
validation results, thus offering a prioritized patch list.

                             Table 7. Time consuming for PanicKiller and actual fixes.
                                   Datasets    Approaches        Min      Max         Avg.
                                   Panic4R-     PanicKiller      0.51s    588.72s     65.77s
                                    Small         Actual         0.52h   807 days    76 days
                                   Panic4R-     PanicKiller      0.34s    425.32s     61.29s
                                    Large         Actual         0.42h   236 days    44 days


5.3.4 Case Study. The overall evaluation results on real-world projects are presented in Table 8,
showing that PanicKiller successfully resolved 28 of 41 open issues with varied root causes, with
all patches merged by developers. As for unsuccessful fixes, some patches were plausible; they
removed the panic but required further manual inspection and minor adjustments. In terms of
closed issues, PanicKiller successfully generates 9 out of 22 patches that are similar to official
patches. The proportion is not very high, largely due to differences in their repair locations. For
example, while the official approach might add a branch before the parameter call, PanicKiller tends
to insert it after creating the parameter. Nonetheless, both strategies achieve equivalent outcomes.

          Table 8. Distribution of panics in real-world crates and fixing effectiveness of PanicKiller.
                                                                     Open issues                Closed issues
                          Crates              Stars     LoC
                                                                  Total Confirmed              Total Similar
                        hifitime               315     10,762       28          21                 0                 -
                 unicode-segmentation          556      7,345       11          7                  1                 0
                        ratatui               9,086    41,534       1           0                  18                7
                      fancy-regex              409      5,557       1           0                  3                 2
                                    Total                           41          28                 22                9


  Below we illustrate some bug cases and their fixes.
  Bug Case1: Figure 7 (a) shows the resolution of an arithmetic overflow error, which is a proposed
patch of a closed issue for Rust crate ratatui [10]. Through fault localization, PanicKiller succeeded

, Vol. 1, No. 1, Article . Publication date: November 2024.
PanicFI: An Infrastructure for Fixing Panic Bugs                                                                                     15

                                                                         - let mut cur_item = self.items[cur_item_idx].unwrap();
    -   x: self.x + margin.horizontal,                                   + let mut cur_item = match self.items[cur_item_idx] {
    +   x: 0 + self.x.saturating_add(margin.horizontal),                 +    Some(item) => item,
        y: self.y + margin.vertical,                                     +    None => return Err(Errors::ParseError
                                                                         +                    (ParsingErrors::UnknownFormat)),
    (a) A generated patch for the crate ratatui that fixes a panic bug   + };
    caused by arithmetic overflow.                                       (b) A generated patch that fixes a panic bug in hifitime.

                            Fig. 7. Patches generated by PanicKiller have fixed real-world issues.

in pinpointing a list of potential fault locations, prioritizing src/layout.rs:233:20 as the top
candidate, which aligns exactly with the actual fix. Then, PanicKiller successfully generated 3
patches for this location. In this case, the fault was identified within a struct filed expression;
however, a closer inspection through iterative analysis revealed that this match expression included
a binary expression, making it suitable for applying the Mutate Binary Operator pattern. Finally,
we calculate the similarity score between the generated patch and the official patch, obtaining a
score of 0.95, indicating the correctness.
   Bug Case 2: The patch illustrated in Figure 7 (b), generated by PanicKiller, serves as an example
of addressing a panic bug that arises from unwrapping a None/invalid value. This bug comes
from an open issue of Rust crate hifitime [9], and our patch has been merged by developers.
PanicKiller employs the Insert Match Unwrapper pattern, specifically designed to mitigate problems
stemming from the misuse of unwrap. This approach transitions the unsafe usage of unwarp()
to pattern matching, which results in returning an error message rather than triggering a panic
error. Additionally, the patch created by PanicKiller takes into consideration the variable types to
ensure consistency with the code context, thereby guaranteeing that the modified program passes
regression testing.

6       DISCUSSION
This section discusses our infrastructure’s application scenarios, comparison with existing works,
and threats to validity.

6.1      Application Scenarios
This work establishes a systematic infrastructure that offers a diverse dataset and comprehensive
analysis of panic bugs specific to Rust projects. We now briefly discuss the application scenarios
and the potential future research directions.
   (1) Benchmark dataset for the Rust APR tools. The widely-used benchmark Defects4J has
been crucial and influential for APR research in Java [16, 17, 35, 40, 41, 59, 60, 62]. Given the current
limitations in the infrastructure for Rust program research, the dataset we propose, Panic4R, is
designed to serve as a robust and reliable benchmark for subsequent studies. It includes macro
switches and test case execution scripts, facilitating researchers to employ it as a benchmark dataset
in their evaluations.
   Panic4R offers detailed information for each case, encompassing the bug-triggering scenario
and the exact patch applied to address the specific bug. This setup facilitates easy reproduction of
the bug. Thus, Panic4R enables further analysis to uncover underlying patterns and common root
causes of panic bugs. This can lead to better insights into Rust’s common vulnerabilities and areas
where APR tools can focus or improve, ultimately contributing to the robustness of Rust codebases
and reducing the likelihood of runtime panics in production software. Moreover, it establishes a
uniform evaluation metric, allowing for more objective and comparable assessments of APR tool
effectiveness. Researchers and practitioners can measure improvements in patch accuracy, bug-fix
efficiency, and detection of bug patterns across different tools, fostering a clearer understanding of
APR advancements in the Rust ecosystem.

                                                                             , Vol. 1, No. 1, Article . Publication date: November 2024.
16                                                            Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu


  (2) Extendable dataset for Rust program repair. Rust, as an emerging language with signifi-
cant advantages in memory safety, increasingly research and approaches designed for Rust have
been proposed. In recent years, some of the existing tools [22, 50, 65] have been developed for fixing
unique bugs in Rust programs. However, due to the less mature infrastructure of Rust compared to
other mainstream languages, there has been a lack of structured and open-source datasets. This
gap has made it challenging to standardize testing, repairing, and verification processes, and the
collected datasets and code snippets are often not reusable for subsequent research.
  In our proposed PanicFI, the project structure and test scripts included in Panic4R are both
unified and highly extensible, including executable code snippets, test cases, and validation scripts.
Future studies that aim to incorporate new panic bug repair datasets can easily extend Panic4R
using a standardized format. Similarly, for other types of bug repair datasets, maintaining a similar
repository structure allows for quick adaptation to standardized dataset formats, minimizing
redundant and tedious work.
   (3) Templates for pattern-based APR tools development. Pattern-based (also known as
"template-based") APR tools was proved to be the most effective method compared to other ap-
proaches, such as search-based and constraint-based schemes [26]. After fault localization, the
pattern-based APR tool could target these defects to select the corresponding fix templates to gen-
erate candidate patches. The mined patterns in our proposed PanicFI, containing 34 sub-patterns
addressing 9 types of panic root causes, can serve as templates for pattern-based APR tools. Based
on this foundation, researchers can concentrate on developing improved techniques for fault
localization and pattern prioritization. For example, multiple potential patterns may match for
the identified fault locations, necessitating further research into efficient pattern selection and
validation. Additionally, ensuring the correctness of program semantics following the application
of these patterns merits deeper investigation.
   In this paper, we demonstrate the effectiveness and practicality of these mined patterns through
the implementation of PanicKiller. Future work could focus on developing more refined repair tools
based on these patterns, aimed at enhancing the accuracy of program semantics and improving
repair efficiency.
   (4) Dataset for fine-tuning large language models (LLMs). In recent years, several research
have employed deep learning models for automated program repair [19, 24, 62], and their results
have demonstrated the feasibility of using AI technologies to assist in fixing programs. However,
the effectiveness of these approaches is often constrained by several factors, such as the scale of
the datasets for model training, the risk of overfitting due to model fine-tuning, and the loss of
information associated with tokenizing unstructured data like code and text [67]. With the rapid
advancement of large-scale models, it is highly potential that program repair techniques based
on these LLMs will be implemented. This development could significantly enhance the precision
and efficiency of tradition learning-based automated repairs, mitigating current limitations and
opening new avenues for research in software maintenance.
   To support research in LLM-based program repair, high-quality datasets are essential [14, 25]. The
datasets and mined patterns included in our proposed PanicFI, are particularly well-suited for use as
training data for LLMs. Notably, the patterns we have identified are diverse, encompassing 34 sub-
patterns and covering 9 different root causes of panic errors. Moreover, our open-sourced patterns
feature various data structures, including source code, abstract AST structures, and corresponding
textual descriptions. These rich sources of information are highly beneficial for the learning and
evolution of LLMs, providing a robust foundation for developing more effective automated program
repair technologies.


, Vol. 1, No. 1, Article . Publication date: November 2024.
PanicFI: An Infrastructure for Fixing Panic Bugs                                                              17


   (5) Providing informative suggestions for users. Our observations during data collection
reveal that Rust developers, particularly beginners, often experience a sense of concern towards
panic bugs. Additionally, the complex stack traces provided by the compiler can be difficult to
understand. If tools were available to assist programmers in comprehending the causes of panic
bugs and offering relevant repair suggestions, it would significantly reduce the complexity of
understanding the program.
   In our PanicFI, PanicKiller produces a mix of suggestions—code patches and textual interpre-
tations—that are more informative than compiler raw output. Given the steep learning curve of
programs like Rust, we believe providing enhanced feedback is beneficial for developers. Such tools
could demystify the error handling process, enabling developers to more effectively address and
rectify issues, thereby enhancing their confidence and proficiency in using Rust.
   (6) Helpful for fixing real-world opening panic bugs. The infrastructure we propose, PanicFI,
is closely aligned with real-world application scenarios. The Panic4R is derived entirely from open-
source Rust projects within the ecosystem, ensuring its relevance and applicability. The patterns we
have mined originate from Rust’s official code implementations, further validating the authenticity
and utility of our infrastructure. Moreover, PanicKiller is capable of handling real, large-scale
Rust projects. Our experiment results have shown PanicKiller is much more efficient than manual
fixes, and PanicKiller has successfully resolved 28 panic bugs in real Rust crates, demonstrating its
practical effectiveness.
6.2   Comparison with Existing Code Patterns
Comparison with Java/C/C++ code patterns. Although numerous bug-fixing patterns oriented
towards Java, C, and C++ have been proposed to corresponding APR tools, the code patterns we
have identified are specific to Rust and are utilized for fixing panic bugs. Specifically, some of the
patterns, e.g., Reorder State Changer, are designed to handle concurrency panics unique to Rust.
The patterns such as Insert Unsafe Block are employed to address the unique unsafe features in
Rust. Additionally, unlike Java or C++, where safety rules such as ownership are not enforced
by the language, our proposed patterns carefully maintain these safety rules. This attention to
Rust’s unique ownership model ensures that the fixes not only resolve the bugs but also uphold the
language’s guarantees of memory safety and concurrency.
   Comparison with Rust-specific code patterns. To date, only a few fix patterns have been
specifically developed for Rust programs. Rust-lancet [65] and Ruxanne [50] are the primary studies
that have designed bug and fix code patterns uniquely for Rust. Unlike these studies, which focus
on ownership-related or other common bug types such as missing attributes, our infrastructure
addresses the most critical panic bugs in Rust. While bugs violating lifetime rules and other common
issues usually prevent compilation, offering error messages and corrective suggestions, panic bugs
manifest at runtime, causing abrupt program termination. These bugs, influenced by Rust’s distinct
memory and process management, render existing fix patterns inadequate for addressing panic
issues. This paper introduces the first infrastructure aimed at exploring Rust panic bugs, identifying
their root causes and developing specific repair patterns, significantly enhancing the understanding
and remediation of Rust programs.
6.3   Threats to Validity
One of the potential threats to validity concerns the representativeness of our collected dataset,
since all code and patches are sourced from open-source crates. However, we consider these crates
to be relatively complex and representative of large-scale Rust projects. Panic4R comprises the
top 500 most downloaded crates, reflecting the actual usage frequency and activity levels of these
programs. We have also modeled our data collection process after the Defects4J dataset to enhance

                                                      , Vol. 1, No. 1, Article . Publication date: November 2024.
18                                                            Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu


the reliability of our data. This adherence to proven methodologies in dataset construction supports
the validity of our research findings.
   Another potential threats lies in the incompleteness of the mined fixing patterns. In real-world
scenarios, specific bug triggers may have unique or diverse repair strategies. To enhance the
comprehensiveness of our mined patterns, we systematically explore and extract from Rust’s
official implementation code, which is considered to contain the most standard repair strategies.
Additional patterns that may emerge in the future can also be easily integrated into our released
PanicFI, further improving the effectiveness of pattern-based repair tools.

7    RELATED WORK
In this section, we compare our work with other APR approaches, as well as the testing and
analysing work for Rust program.
   Automated Program Repair. Automated Program Repair (APR) has witnessed significant
advancements in recent years. Most of methods [16, 17, 35, 39–41, 51, 59, 60, 62] are designed
for Java programs, with evaluated on Defect4J [32], a dataset of real bugs from open source
Java programs. A recent study [26] divides non-learning-based APR into three categories: search-
based [37, 48, 54, 58, 59], constraint-based [12, 16, 17, 42, 46, 47, 57] and template-based [36, 51, 56].
VarFix [60], a search-based way of observing which combinations of edit operations pass the test.
Constraint-based techniques like Nopol [64] and SemFix [45] transform the repair process into
a constraint solving problem, reducing the search space. kPAR [39] and AVATAR [41] generate
fix patterns collected by manual extraction and static violation analysis respectively, used by
iFixR [35]. TBar [40] is proposed to assess the qualitative and quantitative diversity of previous
repair templates. As for learning-based APR, AlaphaRepair [62] achieves state-of-the-art results on
both Java and Python programs via zero-shot learning. VulRepair [24] highlights the advancement
of NMT-based automated vulnerability repairs with pre-trained models.
   Different from existing APR tools that focus on Java and C programs [26], we represent the first
dedicated infrastructure PanicFI targeted at Rust panic bugs. Several tools [22, 50, 65] have been
proposed to address Rust compilation bugs. However, they are not specifically designed to target
panic bugs that occur during runtime. Considering the significant impact of Defects4J and the steep
learning curve associated with Rust, we believe PanicFI would serve as a foundational resource for
Rust’s research.
   Rust Program Testing and Analysing. Due to Rust’s innovative safety mechanism, new
challenges have been posed in its testing and analyzing. RustSmith [53] employs random program
generation to test the Rust compiler. As for RULF [27] and SyRust [55], they concentrate on
testing Rust crates by generating API sequences. In the realm of Rust program analysis, RUPTA [38]
introduces a context-sensitive pointer analysis framework for Rust, successfully applied to construct
call graphs. Additionally, through static analysis, tools like SafeDrop [21] and Rudra [13] detect
memory safety issues in large-scale Rust programs, contributing to enhanced program robustness.
In contrast, RustCheck [63] employs dynamic analysis techniques to uncover memory safety
vulnerabilities.
   Different from existing testing approaches, our work proposed the first APR tool specifically
tailored to address errors related to Rust’s panic mechanism, and we focused on fixing the practical
panic bugs. Besides, we have constructed a real-world code dataset and fix patterns, which serves
as an infrastructure for Rust program comprehension and repair.
8    CONCLUSION
In this paper, we introduce an infrastructure PanicFI designed to support fixing panic bugs of
real-world Rust programs. We construct the first Rust program’s fixing dataset, Panic4R, containing

, Vol. 1, No. 1, Article . Publication date: November 2024.
PanicFI: An Infrastructure for Fixing Panic Bugs                                                                           19


102 real-world panic bugs and their patches. Additionally, we conduct pattern mining based on
Rust compiler source code to identify Rust-specific fixing patterns. We also introduce an APR tool,
PanicKiller, which effectively localizes faults and generates patches, outperforming commercial
LLM-based tools. Moreover, PanicKiller has successfully resolved 28 open issues related to panics,
all of which have been confirmed and merged by developers.
DATA AVAILABILITY
The dataset, mined patterns, the source code of PanicKiller, and experiment results can be found at:
https://sites.google.com/view/panickiller/home.

REFERENCES
 [1] [n. d.]. Issues · rust-lang/rust. https://github.com/rust-lang/rust/labels/I-ICE. (Accessed on 04/12/2024).
 [2] [n. d.]. rust-lang/rust: Empowering everyone to build reliable and efficient software. https://github.com/rust-lang/rust.
     (Accessed on 07/19/2024).
 [3] 2023. Redox - Your Next(Gen) OS - Redox - Your Next(Gen) OS. https://www.redox-os.org/. (Accessed on 12/06/2023).
 [4] 2023. Servo, the embeddable, independent, memory-safe, modular, parallel web rendering engine. https://servo.org/.
     (Accessed on 12/06/2023).
 [5] 2023. Stratis Storage. https://stratis-storage.github.io/. (Accessed on 12/06/2023).
 [6] 2023. TiKV is a highly scalable, low latency, and easy to use key-value database. https://tikv.org/. (Accessed on
     12/06/2023).
 [7] 2023FixMiner: Mining relevant fix patterns for automated program repair. White House urges developers to dump C and
     C++ | InfoWorld. https://www.infoworld.com/article/3713203/white-house-urges-developers-to-dump-c-and-c.html.
     (Accessed on 03/17/2024).
 [8] 2024. crates.io: Rust Package Registry. https://crates.io/. (Accessed on 04/03/2024).
 [9] 2024. hifitime: a powerful Rust and Python library designed for time management. https://github.com/nyx-space/
     hifitime. (Accessed on 29/07/2024).
[10] 2024. ratatui: Rust library that’s all about cooking up terminal user interfaces (TUIs). https://github.com/ratatui-
     org/ratatui. (Accessed on 29/07/2024).
[11] Rui Abreu, Peter Zoeteweij, and Arjan J.C. van Gemund. 2007. On the Accuracy of Spectrum-based Fault Localization.
     In Testing: Academic and Industrial Conference Practice and Research Techniques - MUTATION (TAICPART-MUTATION
     2007). 89–98. https://doi.org/10.1109/TAIC.PART.2007.13
[12] Afsoon Afzal, Manish Motwani, Kathryn T. Stolee, Yuriy Brun, and Claire Le Goues. 2021. SOSRepair: Expressive
     Semantic Search for Real-World Program Repair. IEEE Transactions on Software Engineering 47, 10 (2021), 2162–2181.
     https://doi.org/10.1109/TSE.2019.2944914
[13] Yechan Bae, Youngsuk Kim, Ammar Askar, Jungwon Lim, and Taesoo Kim. 2021. Rudra: Finding Memory Safety
     Bugs in Rust at the Ecosystem Scale (SOSP ’21). Association for Computing Machinery, New York, NY, USA, 84–99.
     https://doi.org/10.1145/3477132.3483570
[14] Berkay Berabi, Jingxuan He, Veselin Raychev, and Martin Vechev. 2021. TFix: Learning to Fix Coding Errors with
     a Text-to-Text Transformer. In Proceedings of the 38th International Conference on Machine Learning (Proceedings of
     Machine Learning Research, Vol. 139), Marina Meila and Tong Zhang (Eds.). PMLR, 780–791. https://proceedings.mlr.
     press/v139/berabi21a.html
[15] William Bugden and Ayman Alahmar. 2022. Rust: The programming language for safety and performance. arXiv
     preprint arXiv:2206.05503 (2022).
[16] Liushan Chen, Yu Pei, and Carlo A. Furia. 2017. Contract-based program repair without the contracts. In 2017 32nd
     IEEE/ACM International Conference on Automated Software Engineering (ASE). 637–647. https://doi.org/10.1109/ASE.
     2017.8115674
[17] Liushan Chen, Yu Pei, and Carlo A. Furia. 2021. Contract-Based Program Repair Without The Contracts: An Extended
     Study. IEEE Transactions on Software Engineering 47, 12 (2021), 2841–2857. https://doi.org/10.1109/TSE.2020.2970009
[18] Zimin Chen, Steve Kommrusch, and Martin Monperrus. 2023. Neural Transfer Learning for Repairing Security
     Vulnerabilities in C Code. IEEE Transactions on Software Engineering 49, 1 (2023), 147–165. https://doi.org/10.1109/
     TSE.2022.3147265
[19] Jianlei Chi, Yu Qu, Ting Liu, Qinghua Zheng, and Heng Yin. 2022. SeqTrans: Automatic Vulnerability Fix via Sequence
     to Sequence Learning. arXiv:2010.10805 [cs.CR] https://arxiv.org/abs/2010.10805
[20] Cloudflare. 2023. Cloudflare - The Web Performance & Security Company. https://www.cloudflare.com/. (Accessed on
     12/06/2023).


                                                                  , Vol. 1, No. 1, Article . Publication date: November 2024.
20                                                             Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu


[21] Mohan Cui, Chengjun Chen, Hui Xu, and Yangfan Zhou. 2023. SafeDrop: Detecting Memory Deallocation Bugs of
     Rust Programs via Static Data-flow Analysis. ACM Trans. Softw. Eng. Methodol. 32, 4, Article 82 (may 2023), 21 pages.
     https://doi.org/10.1145/3542948
[22] Pantazis Deligiannis, Akash Lal, Nikita Mehrotra, and Aseem Rastogi. 2023. Fixing Rust Compilation Errors using
     LLMs. arXiv:2308.05177 [cs.SE] https://arxiv.org/abs/2308.05177
[23] Thomas Durieux, Benoit Cornu, Lionel Seinturier, and Martin Monperrus. 2017. Dynamic patch generation for null
     pointer exceptions using metaprogramming. In 2017 IEEE 24th International Conference on Software Analysis, Evolution
     and Reengineering (SANER). 349–358. https://doi.org/10.1109/SANER.2017.7884635
[24] Michael Fu, Chakkrit Tantithamthavorn, Trung Le, Van Nguyen, and Dinh Phung. 2022. VulRepair: a T5-based
     automated software vulnerability repair (ESEC/FSE 2022). Association for Computing Machinery, New York, NY, USA,
     935–947. https://doi.org/10.1145/3540250.3549098
[25] Rahul Gupta, Soham Pal, Aditya Kanade, and Shirish Shevade. 2017. DeepFix: fixing common C language errors by
     deep learning. In Proceedings of the Thirty-First AAAI Conference on Artificial Intelligence (San Francisco, California,
     USA) (AAAI’17). AAAI Press, 1345–1351.
[26] Kai Huang, Zhengzi Xu, Su Yang, Hongyu Sun, Xuejun Li, Zheng Yan, and Yuqing Zhang. 2023. A Survey on Automated
     Program Repair Techniques. arXiv:2303.18184 [cs.SE]
[27] Jianfeng Jiang, Hui Xu, and Yangfan Zhou. 2022. RULF: rust library fuzzing via API dependency graph traversal. In
     Proceedings of the 36th IEEE/ACM International Conference on Automated Software Engineering (Melbourne, Australia)
     (ASE ’21). IEEE Press, 581–592. https://doi.org/10.1109/ASE51524.2021.9678813
[28] Shujuan Jiang, Wei Li, Haiyang Li, Yanmei Zhang, Hongchang Zhang, and Yingqi Liu. 2012. Fault Localization for Null
     Pointer Exception Based on Stack Trace and Program Slicing. In 2012 12th International Conference on Quality Software.
     9–12. https://doi.org/10.1109/QSIC.2012.36
[29] J.A. Jones, M.J. Harrold, and J. Stasko. 2002. Visualization of test information to assist fault localization. In Proceedings
     of the 24th International Conference on Software Engineering. ICSE 2002. 467–477. https://doi.org/10.1145/581396.581397
[30] Ralf Jung. 2020. Understanding and evolving the Rust programming language. (2020).
[31] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2021. Safe systems programming in Rust.
     Commun. ACM 64, 4 (2021), 144–152.
[32] René Just, Darioush Jalali, and Michael D. Ernst. 2014. Defects4J: a database of existing faults to enable controlled
     testing studies for Java programs. In Proceedings of the 2014 International Symposium on Software Testing and Analysis
     (San Jose, CA, USA) (ISSTA 2014). Association for Computing Machinery, New York, NY, USA, 437–440. https:
     //doi.org/10.1145/2610384.2628055
[33] Dongsun Kim, Jaechang Nam, Jaewoo Song, and Sunghun Kim. 2013. Automatic patch generation learned from
     human-written patches. In 2013 35th International Conference on Software Engineering (ICSE). 802–811. https://doi.org/
     10.1109/ICSE.2013.6606626
[34] Steve Klabnik and Carol Nichols. 2023. The Rust programming language. No Starch Press.
[35] Anil Koyuncu, Kui Liu, Tegawendé F. Bissyandé, Dongsun Kim, Martin Monperrus, Jacques Klein, and Yves Le Traon.
     2019. iFixR: bug report driven program repair. In Proceedings of the 2019 27th ACM Joint Meeting on European Software
     Engineering Conference and Symposium on the Foundations of Software Engineering (Tallinn, Estonia) (ESEC/FSE 2019).
     Association for Computing Machinery, New York, NY, USA, 314–325. https://doi.org/10.1145/3338906.3338935
[36] Xuan Bach D. Le, David Lo, and Claire Le Goues. 2016. History Driven Program Repair. In 2016 IEEE 23rd International
     Conference on Software Analysis, Evolution, and Reengineering (SANER), Vol. 1. 213–224. https://doi.org/10.1109/SANER.
     2016.76
[37] Claire Le Goues, ThanhVu Nguyen, Stephanie Forrest, and Westley Weimer. 2012. GenProg: A Generic Method for
     Automatic Software Repair. IEEE Transactions on Software Engineering 38, 1 (2012), 54–72. https://doi.org/10.1109/TSE.
     2011.104
[38] Wei Li, Dongjie He, Yujiang Gui, Wenguang Chen, and Jingling Xue. 2024. A Context-Sensitive Pointer Anal-
     ysis Framework for Rust and Its Application to Call Graph Construction. In Proceedings of the 33rd ACM SIG-
     PLAN International Conference on Compiler Construction (<conf-loc>, <city>Edinburgh</city>, <country>United
     Kingdom</country>, </conf-loc>) (CC 2024). Association for Computing Machinery, New York, NY, USA, 60–72.
     https://doi.org/10.1145/3640537.3641574
[39] Kui Liu, Anil Koyuncu, Tegawendé F. Bissyandé, Dongsun Kim, Jacques Klein, and Yves Le Traon. 2019. You Cannot
     Fix What You Cannot Find! An Investigation of Fault Localization Bias in Benchmarking Automated Program Repair
     Systems. In 2019 12th IEEE Conference on Software Testing, Validation and Verification (ICST). 102–113. https://doi.org/
     10.1109/ICST.2019.00020
[40] Kui Liu, Anil Koyuncu, Dongsun Kim, and Tegawendé F. Bissyandé. 2019. TBar: revisiting template-based automated
     program repair. In Proceedings of the 28th ACM SIGSOFT International Symposium on Software Testing and Analysis
     (Beijing, China) (ISSTA 2019). Association for Computing Machinery, New York, NY, USA, 31–42. https://doi.org/10.


, Vol. 1, No. 1, Article . Publication date: November 2024.
PanicFI: An Infrastructure for Fixing Panic Bugs                                                                         21


     1145/3293882.3330577
[41] Kui Liu, Anil Koyuncu, Dongsun Kim, and Tegawende F. Bissyandè. 2019. AVATAR: Fixing Semantic Bugs with Fix
     Patterns of Static Analysis Violations. In 2019 IEEE 26th International Conference on Software Analysis, Evolution and
     Reengineering (SANER). 1–12. https://doi.org/10.1109/SANER.2019.8667970
[42] Sergey Mechtaev, Jooyong Yi, and Abhik Roychoudhury. 2015. DirectFix: Looking for Simple Program Repairs. In 2015
     IEEE/ACM 37th IEEE International Conference on Software Engineering, Vol. 1. 448–458. https://doi.org/10.1109/ICSE.
     2015.63
[43] Andréia da Silva Meyer, Antonio Augusto Franco Garcia, Anete Pereira de Souza, and Cláudio Lopes de Souza Jr. 2004.
     Comparison of similarity coefficients used for cluster analysis with dominant markers in maize (Zea mays L). Genetics
     and Molecular Biology 27 (2004), 83–91.
[44] Laura Moreno, John Joseph Treadway, Andrian Marcus, and Wuwei Shen. 2014. On the Use of Stack Traces to Improve
     Text Retrieval-Based Bug Localization. In 2014 IEEE International Conference on Software Maintenance and Evolution.
     151–160. https://doi.org/10.1109/ICSME.2014.37
[45] Hoang Duong Thien Nguyen, Dawei Qi, Abhik Roychoudhury, and Satish Chandra. 2013. SemFix: Program repair via
     semantic analysis. In 2013 35th International Conference on Software Engineering (ICSE). 772–781. https://doi.org/10.
     1109/ICSE.2013.6606623
[46] Yu Pei, Carlo A. Furia, Martin Nordio, Yi Wei, Bertrand Meyer, and Andreas Zeller. 2014. Automated Fixing of Programs
     with Contracts. IEEE Transactions on Software Engineering 40, 5 (2014), 427–449. https://doi.org/10.1109/TSE.2014.
     2312918
[47] Yu Pei, Yi Wei, Carlo A. Furia, Martin Nordio, and Bertrand Meyer. 2011. Code-based automated program fixing.
     In 2011 26th IEEE/ACM International Conference on Automated Software Engineering (ASE 2011). 392–395. https:
     //doi.org/10.1109/ASE.2011.6100080
[48] Yuhua Qi, Xiaoguang Mao, and Yan Lei. 2013. Efficient Automated Program Repair through Fault-Recorded Testing
     Prioritization. In 2013 IEEE International Conference on Software Maintenance. 180–189. https://doi.org/10.1109/ICSM.
     2013.29
[49] Zichao Qi, Fan Long, Sara Achour, and Martin Rinard. 2015. An analysis of patch plausibility and correctness for
     generate-and-validate patch generation systems. In Proceedings of the 2015 International Symposium on Software Testing
     and Analysis (Baltimore, MD, USA) (ISSTA 2015). Association for Computing Machinery, New York, NY, USA, 24–36.
     https://doi.org/10.1145/2771783.2771791
[50] Mohammad Robati Shirzad and Patrick Lam. 2024. A study of common bug fix patterns in Rust. Empirical Softw. Engg.
     29, 2 (feb 2024), 34 pages. https://doi.org/10.1007/s10664-023-10437-1
[51] Seemanta Saha, Ripon k. Saha, and Mukul r. Prasad. 2019. Harnessing Evolution for Multi-Hunk Program Repair. In 2019
     IEEE/ACM 41st International Conference on Software Engineering (ICSE). 13–24. https://doi.org/10.1109/ICSE.2019.00020
[52] A. Schroter, A. Schröter, N. Bettenburg, and R. Premraj. 2010. Do stack traces help developers fix bugs?. In 2010 7th
     IEEE Working Conference on Mining Software Repositories (MSR 2010). IEEE Computer Society, Los Alamitos, CA, USA,
     118–121. https://doi.org/10.1109/MSR.2010.5463280
[53] Mayank Sharma, Pingshi Yu, and Alastair F. Donaldson. 2023. RustSmith: Random Differential Compiler Testing
     for Rust. In Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Testing and Analysis (<conf-
     loc>, <city>Seattle</city>, <state>WA</state>, <country>USA</country>, </conf-loc>) (ISSTA 2023). Association for
     Computing Machinery, New York, NY, USA, 1483–1486. https://doi.org/10.1145/3597926.3604919
[54] Stelios Sidiroglou-Douskos, Eric Lahtinen, Fan Long, and Martin Rinard. 2015. Automatic error elimination by
     horizontal code transfer across multiple applications. SIGPLAN Not. 50, 6 (jun 2015), 43–54. https://doi.org/10.1145/
     2813885.2737988
[55] Yoshiki Takashima, Ruben Martins, Limin Jia, and Corina S. Păsăreanu. 2021. SyRust: automatic testing of Rust
     libraries with semantic-aware program synthesis. In Proceedings of the 42nd ACM SIGPLAN International Conference
     on Programming Language Design and Implementation (Virtual, Canada) (PLDI 2021). Association for Computing
     Machinery, New York, NY, USA, 899–913. https://doi.org/10.1145/3453483.3454084
[56] Shin Hwei Tan and Abhik Roychoudhury. 2015. relifix: Automated Repair of Software Regressions. In 2015 IEEE/ACM
     37th IEEE International Conference on Software Engineering, Vol. 1. 471–482. https://doi.org/10.1109/ICSE.2015.65
[57] Yi Wei, Yu Pei, Carlo A. Furia, Lucas S. Silva, Stefan Buchholz, Bertrand Meyer, and Andreas Zeller. 2010. Automated
     fixing of programs with contracts. In Proceedings of the 19th International Symposium on Software Testing and Analysis
     (Trento, Italy) (ISSTA ’10). Association for Computing Machinery, New York, NY, USA, 61–72. https://doi.org/10.1145/
     1831708.1831716
[58] Westley Weimer, Zachary P. Fry, and Stephanie Forrest. 2013. Leveraging program equivalence for adaptive program
     repair: Models and first results. In 2013 28th IEEE/ACM International Conference on Automated Software Engineering
     (ASE). 356–366. https://doi.org/10.1109/ASE.2013.6693094



                                                                 , Vol. 1, No. 1, Article . Publication date: November 2024.
22                                                            Yunbo Ni, Yang Feng, Zixi Liu, Runtao Chen, and Baowen Xu


[59] Ming Wen, Junjie Chen, Rongxin Wu, Dan Hao, and Shing-Chi Cheung. 2018. Context-aware patch generation
     for better automated program repair (ICSE ’18). Association for Computing Machinery, New York, NY, USA, 1–11.
     https://doi.org/10.1145/3180155.3180233
[60] Chu-Pan Wong, Priscila Santiesteban, Christian Kästner, and Claire Le Goues. 2021. VarFix: balancing edit expressive-
     ness and search effectiveness in automated program repair. In Proceedings of the 29th ACM Joint Meeting on European
     Software Engineering Conference and Symposium on the Foundations of Software Engineering (Athens, Greece) (ESEC/FSE
     2021). Association for Computing Machinery, New York, NY, USA, 354–366. https://doi.org/10.1145/3468264.3468600
[61] Chu-Pan Wong, Yingfei Xiong, Hongyu Zhang, Dan Hao, Lu Zhang, and Hong Mei. 2014. Boosting Bug-Report-
     Oriented Fault Localization with Segmentation and Stack-Trace Analysis. In 2014 IEEE International Conference on
     Software Maintenance and Evolution. 181–190. https://doi.org/10.1109/ICSME.2014.40
[62] Chunqiu Steven Xia and Lingming Zhang. 2022. Less training, more repairing please: revisiting automated pro-
     gram repair via zero-shot learning. In Proceedings of the 30th ACM Joint European Software Engineering Con-
     ference and Symposium on the Foundations of Software Engineering (<conf-loc>, <city>Singapore</city>, <coun-
     try>Singapore</country>, </conf-loc>) (ESEC/FSE 2022). Association for Computing Machinery, New York, NY, USA,
     959–971. https://doi.org/10.1145/3540250.3549101
[63] Lei Xia, Yufei Wu, and Baojian Hua. 2023. Rustcheck: Safety Enhancement of Unsafe Rust via Dynamic Program
     Analysis. In 2023 IEEE 23rd International Conference on Software Quality, Reliability, and Security Companion (QRS-C).
     871–872. https://doi.org/10.1109/QRS-C60940.2023.00102
[64] Jifeng Xuan, Matias Martinez, Favio DeMarco, Maxime Clement, Sebastian Lamelas Marcote, Thomas Durieux, Daniel
     Le Berre, and Martin Monperrus. 2017. Nopol: Automatic Repair of Conditional Statement Bugs in Java Programs.
     IEEE Trans. Softw. Eng. 43, 1 (jan 2017), 34–55. https://doi.org/10.1109/TSE.2016.2560811
[65] Wenzhang Yang, Linhai Song, and Yinxing Xue. 2024. Rust-lancet: Automated Ownership-Rule-Violation Fixing with
     Behavior Preservation (ICSE ’24). Association for Computing Machinery, New York, NY, USA, Article 85, 13 pages.
     https://doi.org/10.1145/3597503.3639103
[66] S. Yoo and M. Harman. 2012. Regression testing minimization, selection and prioritization: a survey. Softw. Test. Verif.
     Reliab. 22, 2 (mar 2012), 67–120. https://doi.org/10.1002/stv.430
[67] Quanjun Zhang, Chunrong Fang, Yuxiang Ma, Weisong Sun, and Zhenyu Chen. 2023. A Survey of Learning-based
     Automated Program Repair. ACM Trans. Softw. Eng. Methodol. 33, 2, Article 55 (dec 2023), 69 pages. https://doi.org/10.
     1145/3631974
[68] Xiaoye Zheng, Zhiyuan Wan, Yun Zhang, Rui Chang, and David Lo. 2023. A Closer Look at the Security Risks in the
     Rust Ecosystem. ACM Trans. Softw. Eng. Methodol. 33, 2, Article 34 (dec 2023), 30 pages. https://doi.org/10.1145/3624738




, Vol. 1, No. 1, Article . Publication date: November 2024.
