                                              Raw Pointer Rewriting with LLMs for Translating C to Safer Rust

                                                              Yifei Gao1 , Chengpeng Wang1 , Pengxiang Huang2 ,
                                                                Xuwei Liu1 , Mingwei Zheng1 , Xiangyu Zhang1
                                                                 1
                                                                   Purdue University 2 University of Rochester
                                                       {gao749, wang6590, liu2598, zheng618, xyzhang}@purdue.edu
                                                                       pengxiang.huang@rochester.edu



                                                               Abstract                          lacking strict compile-time checks for resource
                                                                                                 management.
                                             There has been a growing interest in translat-
arXiv:2505.04852v3 [cs.SE] 18 Apr 2026




                                                                                                    Driven by the need to eliminate dangerous mem-
                                             ing C code to Rust due to Rust’s robust mem-        ory handling issues, many developers have turned
                                             ory and thread safety guarantees. Tools such
                                                                                                 to Rust, a systems programming language that en-
                                             as C2RUST enable syntax-guided transpila-
                                             tion from C to semantically equivalent Rust         forces strict memory and type safety guarantees.
                                             code. However, the resulting Rust programs          Rust’s ownership model imposes tight constraints
                                             often rely heavily on unsafe constructs, partic-    on resource allocation and deallocation (Matsakis
                                             ularly raw pointers, which undermines Rust’s        and Klock, 2014), while its borrow checker pre-
                                             safety guarantees. This paper aims to improve       vents various memory errors at compile time.
                                             the memory safety of Rust programs gener-           These safety features allow Rust to deliver per-
                                             ated by C2RUST by eliminating raw pointers.
                                                                                                 formance on par with C, while significantly reduc-
                                             Specifically, we propose a raw pointer rewrit-
                                             ing technique that lifts raw pointers in individ-   ing memory-related vulnerabilities. Consequently,
                                             ual functions to appropriate Rust data struc-       many projects (e.g., s2n-tls) are migrating legacy
                                             tures. Technically, PR2 employs decision-tree-      C codebases to Rust, enhancing the security and
                                             based prompting to guide the pointer lifting        longevity of critical software.
                                             process. It also leverages code change analysis        Unfortunately, translating C code to Rust is chal-
                                             to guide the repair of errors introduced during     lenging. Tools like C2Rust (Galois and Immunant,
                                             rewriting, effectively addressing errors encoun-    2025) can achieve syntax-level transpilation but
                                             tered during compilation and test case execu-
                                                                                                 often rely on raw pointers and unsafe functions,
                                             tion. We implement PR2 and evaluate it using
                                             gpt-4o-mini on 28 real-world C projects. It is      which bypasses Rust’s safety mechanisms, still in-
                                             shown that PR2 successfully eliminates 18.57%       troducing memory risks in the Rust code. To gen-
                                             of local raw pointers across these projects, sig-   erate safer Rust code, existing studies (Emre et al.,
                                             nificantly enhancing the safety of the trans-       2021, 2023; Zhang et al., 2023; Hong and Ryu,
                                             lated Rust code. On average, PR2 completes          2024) have explored transforming raw pointers into
                                             the transformation of a project in 5.02 hours,      references or other data structures. For example,
                                             at a cost of $1.13. Our code is available at
                                                                                                 Laertes (Emre et al., 2021) and its enhanced ver-
                                             https://github.com/bhcsayx/PR2.
                                                                                                 sion (Emre et al., 2023) use pointer analysis to rea-
                                         1   Introduction                                        son about value lifetimes, enabling conversion to
                                                                                                 references, while a recent study eliminates output
                                         C has long been a dominant language for system          parameters by introducing additional return val-
                                         and application software, powering critical infras-     ues (Hong and Ryu, 2024). However, these static
                                         tructure like operating systems, embedded devices,      analysis techniques are rule-based, limiting their
                                         and security libraries. However, its lack of built-in   ability to handle all raw pointers, as will be shown
                                         memory (van Oorschot, 2021, 2023; Lord, 2023)           in the motivating example.
                                         and type safety (Yang et al., 2018; Turner, 2014;          Recent advances in large language models
                                         Avots et al., 2005) has led to significant vulnera-     (LLMs) have impacted programming, showing
                                         bilities. A notable example is the Heartbleed bug,      strong abilities in code comprehension (Cui et al.,
                                         an out-of-bounds read in OpenSSL caused by im-          2024; Nam et al., 2024; Zheng et al., 2025) and
                                         proper memory handling, which led to large-scale        transformation (Yang et al., 2024b; Yuan et al.,
                                         privacy leaks, highlighting the risks of C language     2024; Yin et al., 2024). Particularly, these mod-
Figure 1: A motivating example of eliminating raw pointers in the tool C2RUST generated Rust program by
rewriting them with Rust data structures, namely a Option of a Box and a slice. (a) The program generated by
C2RUST from a C program; (b) A safer Rust program after raw pointer rewriting.

els can help translate C code into safer Rust by        translation to safer Rust. (2) We develop decision
understanding high-level memory usage intentions        tree-based prompting to lift raw pointers into ap-
hard to obtain through static analysis, guiding the     propriate Rust data structures, and employ code
conversion of raw pointers to safer structures like     change analysis to guide program repair in response
slices. For example, an LLM can recognize one raw       to compilation errors and test case failures. (3) We
pointer used to traverse a memory region and con-       implement PR2 and evaluate it on 28 real-world
vert it to a slice in Figure 1(a). Additionally, LLMs   programs ranging from 437 to 136k LOC. Utilizing
have shown promise in program repair, fixing bugs       gpt-4o-mini, it eliminates 2,255 local raw point-
from compilation errors or test failures, providing a   ers, 3.46 times more than existing techniques, while
degree of correctness assurance for generated Rust      preserving program semantics in all manually sam-
code (Xia and Zhang, 2024; Bouzenia et al., 2024;       pled cases, with an average time cost of 5.02 hours
Kulsum et al., 2024).                                   and an average financial cost of $1.13 per project.
   Based on the above insights, we propose PR2 , a
novel C-to-Rust transpilation technique that com-       2   Related Work
bines C2RUST for syntax-level translation with          Rust’s compile-time memory safety has motivated
LLMs to eliminate raw pointers, eventually produc-      extensive work on automating C-to-Rust transla-
ing safer Rust code. With the guidance of a deci-       tion, broadly divided into two categories. Specif-
sion tree, PR2 prompts LLMs for the pointer lifting,    ically, the first line of research directly translates
which replaces the low-level raw pointers with safer    C into unsafe but functionally equivalent Rust.
Rust constructs, such as Option, Vec, Box, slices,      C ORRODE (Sharp, 2025) was an early attempt
and references. Besides, PR2 iteratively repairs        focusing on module-level semantic preservation.
the statements that use the newly introduced Rust       C2RUST (Galois and Immunant, 2025) remains
data structures if the rewrite is wrong, ensuring the   the most advanced industrial-grade transpiler, of-
generated Rust code can pass the memory safety          fering automated refactoring and cross-checking.
check during the compilation and passes the test        C ITRUS (Citrus-rs, 2025) provides syntax-based
cases at runtime. Particularly, we perform the code     translation for manual refactoring despite limited
change analysis in the repair stage, which helps        semantic preservation. Recent LLM-based ap-
direct the LLMs to focus on the statements most         proaches (Yang et al., 2024a; Shetty et al., 2024)
likely responsible for errors. While PR2 doesn’t        generate multiple candidate translations and use
eliminate all raw pointers, it significantly reduces    test cases to select correct outputs. The second cate-
reliance on them and thus improves memory safety.       gory begins with a semantics-preserving Rust base-
   In summary, the contributions of this work in-       line and incrementally enhances memory safety
clude: (1) We introduce the raw pointer rewriting       by rewriting raw pointers. L AERTES (Emre et al.,
technique systematically eliminating raw pointers       2021) optimistically rewrites pointers into refer-
in Rust programs translated from C, facilitating        ences, while its enhanced version (Emre et al.,
                                        Figure 2: The workflow of PR2

2023) applies more precise pointer analysis, al-          ically, PR2 attempts to eliminate raw pointers
beit risking dynamic semantic changes. N OP -             in single functions by using Rust data structures
CRAT (Hong and Ryu, 2024) and T YMCRAT (Hong              (Phase 1) and repairs the usage of the introduced
and Ryu, 2025) focus on refining function param-          Rust data structures (Phase 2) to ensure that the
eters into safe constructs like Option and Result.        generated Rust code can be compiled successfully
Although the semantic equivalence can be guaran-          and pass the test cases. If the data structure usage
teed, existing techniques only support rewriting a        repair fails a specific number of times, denoted by
restrictive form of raw pointers, leaving numerous        N , PR2 gives up replacing the raw pointer. In our
raw pointers not rewritten in the Rust code.              implementation, we set N to five by default. The
   With the rapid development of generative AI,           details of raw pointer rewriting and data structure
LLMs have greatly advanced cross-language code            usage repair are demonstrated in Section 3.1 and
translation by enabling functionality-preserving          Section 3.2, respectively.
conversions. However, LLM-generated transla-
tions often suffer from syntax errors and seman-          3.1     Raw Pointer Rewriting
tic inconsistencies, limiting their practical reliabil-   This section presents the details of rewriting raw
ity. To mitigate this, many approaches incorpo-           pointers using Rust data structures. Specifically,
rate test cases to detect errors and iteratively refine   we introduce two important stages, i.e., pointer
outputs. For example, U NI T RANS (Yang et al.,           lifting and statement refactoring, in Section 3.1.1
2024b) generates and executes test cases to vali-         and Section 3.1.2, respectively.
date translations across languages, using feedback
for refinement. C OT RAN (Jana et al., 2024) goes         3.1.1    Pointer Lifting
further by fine-tuning an LLM with reinforcement          Existing techniques (Emre et al., 2021, 2023;
learning for Java–Python translation, using com-          Zhang et al., 2023; Hong and Ryu, 2024) primar-
piler feedback and symbolic execution to ensure           ily focus on replacing raw pointers with references
semantic equivalence. Despite these advances, C-          based on the results of pointer analysis. However,
to-Rust translation poses unique challenges. Rust’s       due to challenges in analyzing the semantics of
strict ownership, borrowing, and lifetime rules re-       complex program constructs, such as loops and
quire fundamental changes in memory manage-               library function calls, these approaches often fail
ment and pointer handling, unlike C++, Java, or           to identify opportunities to refactor raw pointers
Python. A recent work (Hong and Ryu, 2025) tack-          into more expressive Rust data structures, such as
les signature-level type migration by converting C        Vec and slices. This limitation degrades the overall
function signatures into idiomatic Rust, but it is        effectiveness of these methods, resulting in many
limited to interfaces and still reports compiler and      raw pointers being retained in the translated Rust
semantic errors, highlighting the insufficiency of        programs.
LLMs alone for Rust’s strict type system.                    To enable the rewriting of raw pointers using a
                                                          wider range of Rust data structures, we leverage the
3   Approach
                                                          LLMs’ capability to understand program semantics,
This section presents technical details of PR2 , of       that is, the LLMs can act as a flexible program ana-
which the workflow is shown in Figure 2. Specif-          lyzer when guided by a well-crafted prompt. To this
                                                                                      Refactor: Please rewrite `Raw pointer` in `Function` below using given `Data
                                     Owning?
                                                        No                            structure` and refactor relevant statements using the constructors and other
                       Yes                                                            APIs offered by the data structure

                                                                                      Function: [FUNC] Raw pointer: [POINTER] Data structure: [Data structure]
                 Individual/                        Individual/
                   Array?                             Array?
                                                                                      Here are two important hints:
   Individual                                                                         1) You may need to utilize the constructors of the data structure to replace
                      Array           Individual                   Array
                                                                                      the declaration of the raw pointer for data structure initialization.
                                                                                      2) You need to conduct the alias analysis to identify all the use-sites of the
                                                                                      raw pointers and refactor the statements.
 Option<Box>         Option<Vec>
                                            Written?              Written?
                                                                                      Here are some examples: [EXAMPLES]
                               Yes                                           No
                                                   No         Yes
                                                                                     Figure 5: The prompt template for statement refactoring
                Option<&mut T>          Option<&T>           &mut [T]        & [T]
                                                                                     the data structure as an immutable slice.
Figure 3: The decision tree used for the pointer lifting                                In contrast to rule-based symbolic static analy-
                                                                                     sis approaches, our decision tree-based prompting
 Analysis: Here is a Rust function translated from C code and contains a raw         strategy enables the LLMs to leverage its semantic
 pointer:
 Function: [FUNC]         Raw pointer: [POINTER]                                     understanding and creativity to identify more ex-
 You need to conduct the following three analyses upon the raw pointer:              pressive patterns of raw pointer manipulation, such
 1) Analyze whether the raw pointer owns the memory.
 2) Analyze the shape of the memory, i.e., whether it is a singleton or array.       as those involving loops and library function calls,
 3) Analyze memory read/write operations using the raw pointer.
                                                                                     which are typically difficult for traditional sym-
 Based on the analysis results, please follow the decision tree [DECISION TREE
 LOGIC] to determine an appropriate data structure to replace the raw pointer.
                                                                                     bolic analysis to handle. Moreover, our approach
                                                                                     is easily extensible: by designing more sophisti-
 Expected Output Format: Return ONLY one of the following six candidates:
 `Option<Box<TYPE>>`, `Option<Vec<TYPE>>`, `Option<&mut TYPE>`,                      cated decision trees and corresponding prompts,
 `Option<&TYPE>`,
 `&mut [TYPE]`, `&[TYPE]`                                                            we can support more complex data structures. In
                                                                                     this work, we focus on sequential data structures for
Figure 4: The prompt template used in the pointer lifting                            non-singleton values. As one of the future works,
                                                                                     we plan to extend PR2 to support additional collec-
end, we introduce a decision tree-based prompting
                                                                                     tion types, such as sets and maps.
strategy that directs the LLMs to perform semantic
analysis on raw pointers. This analysis helps the                                    3.1.2       Statement Refactoring
LLMs identify suitable safe Rust data structures for
replacement. As illustrated in Figure 3, we enforce                                  Based on the result of pointer lifting, we proceed
the LLMs to reason about three key properties of                                     to replace the raw pointer with the suggested data
each raw pointer: ownership, the shape of the mem-                                   structure. This process involves refactoring both
ory buffer (i.e., singleton or array), and memory                                    the declaration of the raw pointer and all statements
access (i.e., read/write behavior). These proper-                                    that make use of it. As illustrated by the prompt
ties collectively determine whether and how a raw                                    template in Figure 5, we provide two key hints to
pointer can be replaced with a specific data struc-                                  the LLMs. First, we instruct the LLMs to replace
ture. Concretely, the ownership property helps de-                                   the declaration of the raw pointer with a constructor
termine whether the pointer can be refactored into                                   of the suggested data structure. Second, we enforce
a reference, Box, or Vec; the shape property indi-                                   the LLMs to reason about the aliasing facts of the
cates whether the pointer corresponds to a single                                    raw pointer in order to locate all potential use-sites,
value or a collection (e.g., Vec or slice); and the                                  and refactor them using the appropriate APIs pro-
memory-access property informs whether the re-                                       vided by the data structure. Notably, the statement
sulting data structure should be mutable or im-                                      refactoring leverages two core capabilities of the
mutable. Since raw pointers can be null, we conser-                                  LLMs, including analyzing semantic properties of
vatively wrap all inferred data structures in Option.                                the program (e.g., alias analysis) and its ability to
Following this decision tree, we can instantiate the                                 generate code (e.g., rewriting statements accord-
prompt template shown in Figure 4 to generate a                                      ingly), as shown in Figure 1(b).
concrete prompt that guides the LLMs in lifting the
                                                                                     3.2     Data Structure Usage Repair
raw pointer to an appropriate Rust data structure.
As an example, the LLMs can correctly infer the                                      This section presents data structure usage repair,
non-owning, array-like, and immutable properties                                     which consists of compilation error fixing (Sec-
of pointer q (Line 8 in Figure 1(a)) and determine                                   tion 3.2.1) and testcase error fixing (Section 3.2.2).
 Compilation Error:                                                                 Testcase Error :
     error[E0502]: cannot borrow `*group_slice` as immutable because it is          thread 'main' panicked at io.rs:540:18: index out of bounds: the
 also borrowed as mutable.      group_slice.len() tries an immutable borrow
                                                                                    len is 14 but the index is 14
 which is conflict with the “&mut group_slice[...]”.
 The Result of Code Change Analysis :
                                                                                    stack backtrace:
 -    let last_ptr = group_slice.offset(–1));                                           19: 0x557b240cfbda - core::slice::index_mut::... at
 -     (*last_ptr).args_processed = (*last_ptr).args_processed.wrapping_add(            /STD_PATH/core/src/slice/index.rs:29:9
 -                                ((*parser).state.next - index) as c_uint);            20: 0x557b240cfbda - <alloc::vec::Vec<T,A>
 -    len -= 1;                                                                         as ::index_mut::... at /STD_PATH/alloc/src/vec/mod.rs:2738:9
 +    group_slice = &mut group_slice[..group_slice.len() - 1];                          21: 0x557b240cc22c - c2rust_out::io::write_stream:: at
 +    (*group_slice.last_mut().unwrap()).args_processed =                               /PROG_PATH/io.rs:13:18
 +        ((*group_slice.last_mut().unwrap()).args_processed).wrapping_add(
 +            ((*parser).state.next - index) as c_uint);                             The Result of Code Change Analysis
 +    group_slice = &mut group_slice[..last_index];                                 - *p.offset(len as isize) = *tmp as i32 as std::os::raw::c_char;
                                                                                    + p_vec[len as usize] = *tmp as i32 as std::os::raw::c_char;
          (a) The compilation error and the result of code change analysis   Fix
                                                                                            (a) The testcase error and the result of code change analysis   Fix
      let last_index = group_slice.len() - 2;
      let last_group = &mut group_slice[last_index];
                                                                                    p_vec.push(*tmp as i32 as std::os::raw::c_char); // Use push
      last_group.args_processed =(last_group.args_processed).wrapping_add((
          (*parser).state.next - index) as c_uint);                                                  (b) The result of testcase error fixing
      group_slice = &mut group_slice[..last_index];

                      (b) The result of compilation error fixing
                                                                                         Figure 7: An example of testcase error fixing
     Figure 6: An example of compilation error fixing
                                                                                   the slice will raise an error as it needs to hold an
3.2.1      Compilation Error Fixing                                                immutable reference. To resolve this error, the fix
                                                                                   calls the API len before the mutable slice is cre-
As shown in Section 3.1, only the code within a
                                                                                   ated, and stores the length value in a new variable,
single function is modified during the raw pointer
                                                                                   avoiding the interleaving of references.
rewriting. This design implies that any resulting
compilation error must be introduced by the mod-                                   3.2.2     Testcase Error Fixing
ified statements within that function, enabling us
                                                                                   Once we obtain a Rust program with all compila-
to narrow down the scope of fixing to the function
                                                                                   tion errors fixed, we proceed to run the program’s
for the error fixing. However, a single function
                                                                                   test cases to uncover potential violations of the
may contain many raw pointers, most of which are
                                                                                   original input-output relationship. The overall de-
unrelated to the repair task. What is even worse,
                                                                                   sign of testcase error fixing closely follows that of
the function itself can be quite large (e.g., over one
                                                                                   compilation error fixing described in Section 3.2.1.
hundred lines), with the majority of statements not
                                                                                   Figure 7 shows a prompt template and an exam-
interacting with the memory addressed by the raw
                                                                                   ple of testcase error fixing. It is important to note
pointers. These unrelated raw pointers and state-
                                                                                   that passing all test cases which the original Rust
ments introduce irrelevant tokens as the noise into
                                                                                   program pass is a necessary condition for a valid
the repair context, which poses a significant chal-
                                                                                   translation, although it does not theoretically guar-
lenge for the LLMs, often leading to hallucinations
                                                                                   antee semantic equivalence. In practice, the validity
and repair failures.
                                                                                   of our approach depends on the quality of the avail-
   To enable more informed repairs using the
                                                                                   able testcases. While many real-world projects
LLMs, we filter out irrelevant tokens from the
                                                                                   include comprehensive test suites, there may be
repair context. Technically, we introduce code
                                                                                   corner cases not captured by the tests.
change analysis, which computes the difference be-
tween the function before and after the raw pointer                                4    Evaluation
rewriting. The resulting added, deleted, or modi-
fied statements are the most likely sources of com-                                We implemented PR2 as a prototype with 1,072
pilation errors. By feeding code changes along                                     lines of Rust and 1,187 lines of Python. It uses
with error messages into the LLMs, we can effec-                                   tree-sitter to extract raw pointers, struct defi-
tively guide the LLMs to focus its attention on                                    nitions, and global variables from translated Rust
the most relevant statements, improving its abil-                                  code. Pointer lifting, statement refactoring, and re-
ity to fix compilation errors. Due to space limit,                                 pair phases are powered by gpt-4o-mini, chosen
we do not show the prompt template in the paper                                    for its low cost (i.e., $0.150/M input tokens and
as the design is very standard based on the code                                   $0.600/M output tokens (OpenAI, 2025)), making
change analysis. Figure 6 shows an example of                                      it suitable for iterative transformation. To speed
using code change analysis to fix a conflicting im-                                up compilation during error fixing, we use cargo
mutable (group_slice.len()) and mutable (&mut                                      check, which performs type and borrow checking
group_slice) borrows error. Specifically, Rust                                     without linking. We allow up to five repair attempts
compiler allows only one mutable reference to a                                    per pointer (i.e., the value of N in Section 3 is five)
variable at any time, thus calling the API len to                                  and set the temperature to 0.0 for greedy decoding.
                                      Table 1: The main statistics of PR2

    ID   #ERP    #AF       RT(s)     CFT(s)      TFT(s)    TotalT(s)      #InTok    #OutTok      #P    Cost($)
    1        8      5      188.81      45.52       10.65      244.98       46,068     13,336      39    0.015
    2       10      9      305.84     123.32       20.46      449.61       81,371     27,257      89    0.029
    3        6      4      747.44     118.85      215.55    1,081.84      222,652     72,066      94    0.077
    4        6      5    1,263.03     161.50       45.86    1,470.39      318,859     57,769     125    0.082
    5       22     10    1,182.65     164.52       11.70    1,358.88      268,129     70,788     146    0.083
    6       11     10    1,150.23     264.11      349.21    1,763.55      392,429     87,263     252    0.111
    7       17     12    1,595.18     451.75       66.10    2,113.03      427,183    127,902     187    0.141
    8       18     15    1,809.05     537.59       31.19    2,377.83      436,328    123,892     253    0.140
    9       17     13    2,930.73     316.33      436.54    3,683.60      928,716    120,543     278    0.212
    10      16     11    2,839.98     330.11       14.17    3,184.26      610,139    112,067     206    0.159
    11      15     12    3,365.71     693.44      158.15    4,217.30    1,102,037    147,435     322    0.254
    12      12     12    4,873.78     491.10       75.06    5,439.94    2,010,145    160,203     363    0.398
    13      38     27    4,743.65     793.61      238.83    5,776.08    1,504,725    264,773     511    0.385
    14      53     43    8,951.85   2,658.11    1,037.37   12,647.33   14,008,537    418,288     920    2.352
    15      80     61    8,293.31   2,281.44      862.65   11,437.40    9,699,548    519,250   1,137    1.766
    16      87     70   12,463.53     650.76      319.79   13,434.08    2,651,673    234,328   1,004    0.538
    17      60     47    6,510.92     582.86      586.44    7,680.21      579,508    136,921     531    0.169
    18      99     80   16,218.48   4,631.28      622.08   21,471.84    4,546,460    952,967   1,980    1.254
    19      73     58   18,867.08   2,041.97    1,963.26   22,872.31    4,831,868    356,541   1,490    0.939
    20     249    132   16,791.45   2,422.30   12,365.05   31,578.80    5,352,697    881,196   1,541    1.332
    21     157    113   20,378.32   4,229.75    2,410.53   27,018.61    8,878,129    861,532   1,882    1.849
    22     194    158   19,006.08   8,199.58    2,640.55   29,846.22   10,299,083    960,924   2,039    2.121
    23     105     83   12,430.74   2,192.71    8,888.03   23,511.47   60,813,477    609,506   1,594    9.488
    24      84     68   29,406.70   1,595.97    6,008.53   37,011.20    9,507,522    442,569   2,225    1.692
    25     158    130   16,422.75   5,805.27    6,840.01   29,068.04    2,625,267    606,173   2,128    0.757
    26     175    152   41,537.59   3,229.05   38,712.37   83,479.01   17,347,685    662,482   3,114    3.000
    27     138    125   36,488.11   4,170.67   20,440.27   61,099.05    3,322,335    616,631   2,570    0.868
    28     347    257   51,822.16   5,775.61    2,837.01   60,434.78    5,344,925    973,554   3,621    1.386


  We evaluate the effectiveness and efficiency of          4.1   RQ1: Effectiveness and Efficiency
PR2 by answering the four research questions:
                                                              Setup and Metrics. To quantify the effectiveness
• RQ1. How effectively and efficiently does PR2            of PR2 , we introduce the number of eliminated raw
  eliminate raw pointers in the Rust programs gen-         pointers as our main metric. Meanwhile, we collect
  erated by C2RUST?                                        the number of functions refactored during this pro-
                                                           cess. The eliminated raw pointers in these functions
• RQ2. How does PR2 compare with existing tech-
                                                           can improve the memory safety of the function us-
  niques that transform C to safer Rust programs?
                                                           age. To quantify the efficiency of PR2 , we measure
• RQ3. Which kinds of data structures are intro-           the time cost, input/output token costs, prompting
  duced by PR2 to replace raw pointers?                    rounds, and financial cost. Notably, we do not in-
                                                           clude the time overhead introduced by C2RUST, as
• RQ4. How do the decision tree-based prompt-              it is negligible compared to the overhead incurred
  ing and code change analysis contribute to the           during the rewriting and repair phases of PR2 .
  performance of PR2 ?
                                                              Results. Table 1 presents detailed evaluation
   Benchmark. We adopt C projects from the eval-           results of PR2 . The column #ERP shows the num-
uation set used in N OPCRAT (Hong and Ryu, 2024),          ber of eliminated raw pointers. The column #AF
comprising widely used real-world applications             indicates the number of affected functions. On av-
also used in prior C-to-Rust studies (Emre et al.,         erage, PR2 removes 18.57% of raw pointers and
2021, 2023). Of the original 55 programs, 26 lack          transforms 13.05% of functions into safer code. No-
test cases and 1 contains raw pointers only in func-       tably, it eliminates 34.3% of pointers in grep-3.11
tion parameters, which are outside our scope. We           (ID = 20), demonstrating the effectiveness of PR2
thus select the remaining 28 projects with test cases      when analyzing large projects.
as our benchmark, which are listed by Table 4 in              The columns RT, CFT, and TFT represent
Appendix A.1. Overall, the benchmark spans pro-            time spent on raw pointer rewriting, compiler er-
grams from a few hundred to 136K LOC and 17                ror fixing, and test case error fixing, respectively,
to 2,731 raw pointers, providing a diverse set for         with total time in TotalT. On average, PR2 takes
evaluating the effectiveness and scalability of PR2 .      5.02 hours per project, with the longest taking 28
hours. The bottleneck in time is rewriting, averag-
ing 74.26% of total time. Additionally, the columns
InTok, OutTok, and #P represent input/output to-
kens and prompt rounds during rewriting and repair.
The column Cost reflects total prompting expense.
Each successful rewrite requires 14 prompt rounds.
Across all 28 benchmarks, the total cost is $31.60,
averaging just $1.13 per project, highlighting the
high efficiency of PR2 .

4.2   RQ2: Comparison with Baselines                   Figure 8: The proportions of different data structures

   Setup and Metrics. We compare our approach          due to prompt-related overhead. However, with
with L AERTES (Emre et al., 2021), an automated        ongoing LLM performance improvements, PR2 is
tool that aims to convert raw pointers into safe       expected to become significantly faster over time.
references. Specifically, L AERTES applies an opti-
                                                       4.3   RQ3: Categorization of Data Structures
mistic rewriting strategy and iteratively addresses
lifetime inference and borrow-checking errors to        Setup and Metrics. To show the diversity of Rust
achieve a successful compilation. Another recent       data structures utilized by PR2 , we categorize Rust
work, N OPCRAT (Hong and Ryu, 2024), focuses on        data structures used by PR2 to uniquely eliminate
rewriting raw pointers in the parameters that prop-    rewritten raw pointers. This analysis is important
agate output values as side effects. However, due      because, unlike L AERTES, which primarily con-
to the difference in scope, the sets of raw pointers   verts raw pointers to references, PR2 supports a
eliminated by PR2 and N OPCRAT are disjoint thus       broader spectrum of Rust data structures, thereby
we do not include it in our comparative evaluation.    offering more improvements on memory safety.
   Results. Table 2 shows the comparison results          Results. Figure 8 shows the distribution of Rust
of PR2 and the baselines. The column ID lists          data structures used in pointer rewriting. Overall,
program identifiers (as in Table 4). In the column     singleton data structures, e.g., Box, Option<&T>,
L AERTES, the sub-column EL denotes the num-           and Option<&mut T>, account for the majority
ber of raw pointers eliminated by L AERTES, while      of rewritten raw pointers (74.8%). Meanwhile, a
the sub-column EL\P indicates the number of the        non-trivial portion (17.6%) of raw pointers are suc-
raw pointers L AERTES eliminates and PR2 does          cessfully rewritten into sequential data structures,
not eliminate. The sub-column T (s) indicates the      including Vec, &[T], and &mut [T]. In terms of
execution time of L AERTES. Similarly, the column      ownership, 41.6% of raw pointers are rewritten
PR2 includes the sub-column EP , which indicates       into Box and Vec which ensures that the lifetimes of
the number of pointers eliminated by PR2 , and         the wrapped values are properly bounded, thereby
EP \L , which indicates the number of raw pointers     preventing memory leaks. Lastly, 33.8% of the
eliminated by PR2 and not eliminated by L AERTES.      raw pointers are converted into read-only structures
Overall, PR2 removes 2,255 raw pointers, com-          (e.g., Option<&T>, &[T]), removing unnecessary
pared to 506 by L AERTES, and outperforms it on        mutability. We present a case demonstrating PR2 ’s
most projects. The size of the project buffer (ID      capability of leveraging Rust inherent APIs. We
= 2) is small, enabling L AERTES to infer lifetimes    provide a case study of data structure usage within
effectively and efficiently. Notably, PR2 uniquely     the generated Rust code in Appendix A.2.
eliminates 2,160 raw pointers (95.79% of its total),
indicating that most rewrites are beyond the reach     4.4   RQ4: Ablation Study
of the baseline L AERTES. In contrast, L AERTES           Setup and Metrics. To quantify how the tech-
only uniquely handles 438 raw pointers. Over-          nical designs of PR2 contribute to the rewriting
all, PR2 eliminates 3.46× more raw pointers than       results, we introduce two ablations: NT and NCC,
L AERTES, demonstrating its effectiveness.             which disable decision tree-based prompting and
   In terms of efficiency, L AERTES processes all 28   code change analysis in the pointer lifting and
projects in 3,732.85 seconds (133.32 seconds per       data structure usage repair, respectively. Specifi-
project), while PR2 averages 5.02 hours per project    cally, the ablation NT enforces the LLM to directly
Table 2: The statistics of comparison with baseline                          view outputs from PR2 . Each independently evalu-
L AERTES and two ablations NT and NCC                                        ated 20 randomly selected raw pointer eliminations
 Id
           L AERTES                PR2               NT           NCC        (around 1% of all cases), using gpt-4o-mini ex-
      EL   EL\P       T(s)   EP     EP \L      ET     ET \L     EC    EC\L   planations and Rust documentation to judge seman-
 1     2      2      1.15      8           8     3          3    11     10   tic equivalence. Reviews took about 45 minutes
 2    27     17      2.41     10           0     8          2    12      1
 3     0      0      1.74      6           6     1          1     2      2   each, and all volunteers confirmed the rewritten
 4     5      2      1.44      6           3     5          3     4      2
 5     3      2      4.35     22          21     7          7    10     10
                                                                             code preserved original semantics. These results
 6     1      0      5.64     11          10     7          7     7      7   suggest PR2 is a practical tool for C-to-Rust trans-
 7     0      0      1.73     17          17     6          6     9      9
 8     4      2      4.11     18          15    11          9    16     13
                                                                             lation. While it lacks formal guarantees, it achieves
 9     2      2      7.11     17          17     7          6     0      0   strong empirical outcomes. With modest human
 10   12     11      7.74     16          15     8          6     8      7
 11    3      3     25.55     15          15     7          7     7      7
                                                                             effort, users can semi-automatically produce safer,
 12   14     12      5.54     12          10     2          2     4      3   idiomatic Rust code.
 13    5      3      4.25     38          35     8          7    15     15
 14    9      6    121.46     53          48    36         33    40     35
 15   14     12     46.22     80          77    45         41    61     56
 16    7      7     15.08     87          86    56         55    68     67
 17   12     12     42.42     60          58    54         52    62     60      Threats to Validity. The primary threat to in-
 18    2      1      90.6     99          98     0          0     0      0   ternal validity stems from the stochastic nature of
 19   28     28      18.2     73          73    91         85    71     69
 20   52     39     45.38    249         227    80         75    68     65   LLMs, which can yield nondeterministic outputs
 21   42     40     47.66    157         155    96         95    95     93   and affect reproducibility. As noted in Section 4.4,
 22   43     36     95.03    194         187   108        102   124    118
 23   37     24     35.06    105          88     0          0     0      0   two ablation settings slightly outperform the full-
 24   10     10     74.99     84          84     0          0    41     41   featured PR2 on tar-1.34 and glpk-5.0. To ad-
 25   58     53    713.13    158         153   142        132   177    168
 26   37     37    164.86    175         170   187        179   169    164   dress this, we fix the temperature to 0 for deter-
 27   40     40   1619.28    138         138    95         94   106    104
 28   37     37    530.72    347         346   138        138   393    392
                                                                             ministic behavior. External validity depends on
                                                                             test case quality, which influences both the elim-
choose a data structure from the six data struc-                             ination number and correctness. Our test-driven
tures shown in the leaf nodes in Figure 3, without                           approach reduces manual effort, and the user study
conducting semantic analyses. The ablation NCC                               confirms that PR2 preserves semantic equivalence.
feeds the functions before and after raw pointer                             Since broader test coverage could further improve
rewriting to the LLM along with error messages,                              rewriting quality, we calculated the coverage of
but without any code change information. We use                              test suites in our benchmark projects, observing
the number of raw pointers eliminated under differ-                          62.84% on average. We then focused on rewritten
ent ablations as the primary evaluation metric.                              pointers in functions not covered by existing test
   Results. Table 2 reports results for ablations NT                         suites and leveraged LLMs to synthesize test cases
and NCC. Under the column NT, the sub-columns                                and run them, in 59 total cases we found only 2 in-
ET and ET \L denote the total and uniquely elimi-                            correct pointer rewrites, corresponding to a 96.61%
nated pointers, respectively; NCC shows the same                             correctness rate among inspected cases, which fur-
for its setting. As shown, NT eliminates 1,208                               ther supports the correctness of our transforma-
pointers (46.43% fewer than the full PR2 ), and                              tion pipeline. Construct validity relates to LLM
NCC eliminates 1,580 (29.93% fewer). Removing                                choice. We use gpt-4o-mini, a cost-effective and
the decision tree prompt causes a 46.43% drop in                             widely available model, and validate our findings
unique eliminations; omitting code change analysis                           with Claude-3.5-Sonnet and Deepseek-v3.2 on
leads to a 29.93% drop. These results confirm the                            the top 10 projects in Table 1 with results demon-
importance of both components—especially the de-                             strated in Table 3, where ECl , EDp correspond
cision tree—in enhancing rewrite quality. Even in                            to pointers eliminated by Claude-3.5-Sonnet
reduced forms, both variants outperform L AERTES,                            and Deepseek-v3.2, and ECl \ El , EDp \ El
highlighting the robustness of LLM-driven rewrit-                            correspond to pointers uniquely eliminated by
ing. Appendix A.3 provides a case study that shows                           Claude-3.5-Sonnet and Deepseek-v3.2. Com-
an example handled by full-featured PR2 but not                              pared with gpt-4o-mini, Claude-3.5-Sonnet
addressed by its ablation NT.                                                and Deepseek-v3.2 demonstrate similar perfor-
                                                                             mance in most projects and significantly better per-
4.5   Discussion                                                             formance in some projects (1, 2, 8, 10). As LLMs
  User Study. To assess semantic correctness,                                advance and inference costs drop, the effectiveness
we recruited ten Rust-experienced volunteers to re-                          and efficiency of PR2 will continue to improve.
      Id   ECl    ECl \ EL   EDp    EDp \ EL            have low readability and maintainability, since cur-
       1   14        12       14      12
       2   11         1       29       1                rent efforts focus mainly on raw pointer elimina-
       3    4        4        10      10                tion. We plan to use LLMs in a post-processing
       4    6        5         6       5                phase to further refine and improve the quality of
       5   24        23       20      17
       6   20        19       24      23                the refactored Rust code.
       7   18        18       18      18
       8   42        41       34      33                Acknowledgement
       9   22        22       27      26
      10   32        31       21      18                We are grateful to the Center for AI Safety for pro-
Table 3: Additional LLM Pointer Elimination Results
                                                        viding computational resources. This work was
                                                        funded in part by the National Science Founda-
                                                        tion Awards SHF-1901242, SHF-1910300, Proto-
5   Conclusion                                          OKN 2333736, IIS2416835, DARPA VSPELLS -
                                                        HR001120S0058, ONR N00014-23-1-2081, and
This paper presents PR2 , a novel approach for trans-
                                                        Amazon. Any opinions, findings and conclusions
forming C programs into safer Rust programs by
                                                        or recommendations expressed in this material are
eliminating raw pointers using LLMs. Building on
                                                        those of the authors and do not necessarily reflect
syntax-guided C-to-Rust translation, we introduce
                                                        the views of the sponsors.
a raw pointer rewriting technique that targets raw
pointers within single functions and replaces them
with appropriate Rust data structures. Specifically,    References
PR2 employs LLMs to lift raw pointers to Rust data
                                                        Dzintars Avots, Michael Dalton, V Benjamin Livshits,
structures and iteratively repairs the transformed
                                                          and Monica S Lam. 2005. Improving software secu-
program by focusing on the changed code. Our              rity with a c pointer analysis. In Proceedings of the
evaluation on 28 real-world C programs demon-             27th international conference on Software engineer-
strates that PR2 , powered by gpt-4o-mini, elimi-         ing, pages 332–341.
nates a total of 2,255 raw pointers, with an average    Islem Bouzenia, Premkumar Devanbu, and Michael
processing time of 5.02 hours and a cost of $1.13          Pradel. 2024. Repairagent: An autonomous, llm-
per project. We hope that PR2 provides valuable            based agent for program repair. arXiv preprint
insights for advancing program translation tech-           arXiv:2403.17134.
niques aimed at improving system reliability.           Berkeley R. Churchill, Oded Padon, Rahul Sharma,
                                                          and Alex Aiken. 2019. Semantic program align-
6   Limitations                                           ment for equivalence checking. In Proceedings of
                                                          the 40th ACM SIGPLAN Conference on Program-
Although PR2 effectively refactors specific raw           ming Language Design and Implementation, PLDI
pointers using Rust data structures, it has several       2019, Phoenix, AZ, USA, June 22-26, 2019, pages
drawbacks. First, it performs raw pointer rewriting       1027–1040. ACM.
within individual functions, keeping type signa-        Citrus-rs. 2025. Citrus: Convert c to rust.
tures unchanged, as shown in Section 3.1.2. While
this conservative scope simplifies repairs, it misses   Jielun Cui, Yutong Zhao, Chong Yu, Jiaqi Huang,
chances to eliminate raw-pointer parameters, un-           Yuanyuan Wu, and Yu Zhao. 2024. Code comprehen-
                                                           sion: Review and large language models exploration.
like N OPCRAT (Hong and Ryu, 2024). Future work            In 2024 IEEE 4th International Conference on Soft-
could enable more expressive rewriting by modify-          ware Engineering and Artificial Intelligence (SEAI),
ing function signatures across call chains. Second,        pages 183–187. IEEE.
PR2 lacks a theoretical correctness guarantee; with-    Mehmet Emre, Peter Boyland, Aesha Parekh, Ryan
out strong or sufficient test coverage, raw pointer      Schroeder, Kyle Dewey, and Ben Hardekopf. 2023.
elimination can break functional equivalence de-         Aliasing limits on translating c to safe rust. Pro-
spite passing compilation and tests. Enhancements        ceedings of the ACM on Programming Languages,
                                                         7(OOPSLA1):551–579.
could involve synthesizing unit tests using LLMs
for differential testing (Zhou et al., 2025; Zhang      Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben
et al., 2025; Zheng et al.; Rao et al., 2024) and        Hardekopf. 2021. Translating c to safer rust. Pro-
applying verification techniques like relational ver-    ceedings of the ACM on Programming Languages,
                                                         5(OOPSLA):1–29.
ification (Unno et al., 2021; Churchill et al., 2019;
Zheng et al., 2024). Finally, the rewritten code may    Galois and Immunant. 2025. C2rust demonstration.
Jaemin Hong and Sukyoung Ryu. 2024. Don’t write, but         Paul C van Oorschot. 2021. Toward unseating the un-
   return: Replacing output parameters with algebraic          safe c programming language. IEEE Security & Pri-
   data types in c-to-rust translation. Proceedings of         vacy, 19(02):4–6.
   the ACM on Programming Languages, 8(PLDI):716–
   740.                                                      Paul C van Oorschot. 2023. Memory errors and memory
                                                               safety: C as a case study. IEEE Security & Privacy,
Jaemin Hong and Sukyoung Ryu. 2025. Type-migrating             21(2):70–76.
   c-to-rust translation using a large language model.
   Empirical Software Engineering, 30(1):3.                  Chunqiu Steven Xia and Lingming Zhang. 2024. Auto-
                                                               mated program repair via conversation: Fixing 162
Prithwish Jana, Piyush Jha, Haoyang Ju, Gautham                out of 337 bugs for $0.42 each using chatgpt. In Pro-
   Kishore, Aryan Mahajan, and Vijay Ganesh. 2024.             ceedings of the 33rd ACM SIGSOFT International
   Cotran: An llm-based code translator using reinforce-       Symposium on Software Testing and Analysis, ISSTA
   ment learning with feedback from compiler and sym-          2024, page 819–831, New York, NY, USA. Associa-
   bolic execution. In ECAI 2024, pages 4011–4018.             tion for Computing Machinery.
   IOS Press.
                                                             Aidan ZH Yang, Yoshiki Takashima, Brandon Paulsen,
Ummay Kulsum, Haotian Zhu, Bowen Xu, and Marcelo               Josiah Dodds, and Daniel Kroening. 2024a. Vert:
  d’Amorim. 2024. A case study of llm for automated            Verified equivalent rust transpilation with large lan-
 vulnerability repair: Assessing impact of reasoning           guage models as few-shot learners. arXiv preprint
  and patch validation feedback. In Proceedings of the         arXiv:2404.18852.
 1st ACM International Conference on AI-Powered
 Software, pages 103–111.                                    Gao Yang and 1 others. 2018. The source and ex-
                                                               ploitation of the program vulnerability. In 2018 3rd
Bob Lord. 2023. The urgent need for memory safety in           Joint International Information Technology, Mechan-
  software products. Cybersecurity & Infrastructure            ical and Electronic Engineering Conference (JIMEC
  Security Agency.                                             2018), pages 89–94. Atlantis Press.
Nicholas D Matsakis and Felix S Klock. 2014. The rust        Zhen Yang, Fang Liu, Zhongxing Yu, Jacky Wai Keung,
  language. In Proceedings of the 2014 ACM SIGAda              Jia Li, Shuo Liu, Yifan Hong, Xiaoxue Ma, Zhi Jin,
  annual conference on High integrity language tech-           and Ge Li. 2024b. Exploring and unleashing the
  nology, pages 103–104.                                       power of large language models in automated code
                                                               translation. Proceedings of the ACM on Software
Daye Nam, Andrew Macvean, Vincent Hellendoorn,
                                                               Engineering, 1(FSE):1585–1608.
  Bogdan Vasilescu, and Brad Myers. 2024. Using an
  llm to help with code understanding. In Proceedings
                                                             Xin Yin, Chao Ni, Tien N Nguyen, Shaohua Wang, and
  of the IEEE/ACM 46th International Conference on
                                                               Xiaohu Yang. 2024. Rectifier: Code translation with
  Software Engineering, pages 1–13.
                                                               corrector via llms. arXiv preprint arXiv:2407.07472.
OpenAI. 2025. Api pricing.
                                                             Zhiqiang Yuan, Weitong Chen, Hanlin Wang, Kai Yu,
Nikitha Rao, Elizabeth Gilbert, Tahina Ramananandro,           Xin Peng, and Yiling Lou. 2024. Transagent: An
  Nikhil Swamy, Claire Le Goues, and Sarah Fakhoury.           llm-based multi-agent system for code translation.
  2024. Diffspec: Differential testing with llms using         arXiv preprint arXiv:2409.19894.
  natural language specifications and code artifacts.
  arXiv preprint arXiv:2410.04249.                           Hanliang Zhang, Cristina David, Yijun Yu, and Meng
                                                               Wang. 2023. Ownership guided c to rust translation.
Jamey Sharp. 2025. Corrode: Automatic semantics-               In International Conference on Computer Aided Ver-
  preserving translation from c to rust.                       ification, pages 459–482. Springer.

Manish Shetty, Naman Jain, Adwait Godbole, Sanjit A          Yixuan Zhang, Ningyu He, Jianting Gao, Shangtong
 Seshia, and Koushik Sen. 2024. Syzygy: Dual code-             Cao, Kaibo Liu, Haoyu Wang, Yun Ma, Gang Huang,
 test c to (safe) rust translation using llms and dynamic      and Xuanzhe Liu. 2025. Drwasi: Llm-assisted dif-
 analysis. arXiv preprint arXiv:2412.14234.                    ferential testing for webassembly system interface
                                                               implementations. ACM Transactions on Software
Stephen Turner. 2014. Security vulnerabilities of the top      Engineering and Methodology.
   ten programming languages: C, java, c++, objective-
   c, c#, php, visual basic, python, perl, and ruby. Jour-   Mingwei Zheng, Qingkai Shi, Xuwei Liu, Xiangzhe
   nal of Technology Research, 5:1.                            Xu, Le Yu, Congyu Liu, Guannan Wei, and Xiangyu
                                                               Zhang. 2024. Pardiff: Practical static differential
Hiroshi Unno, Tachio Terauchi, and Eric Koskinen.              analysis of network protocol parsers. In Proc. ACM
  2021. Constraint-based relational verification. In           Program. Lang., OOPSLA ’24, pages 1208–1234.
  Computer Aided Verification - 33rd International             ACM.
  Conference, CAV 2021, Virtual Event, July 20-23,
  2021, Proceedings, Part I, volume 12759 of Lecture         Mingwei Zheng, Danning Xie, Qingkai Shi, Cheng-
  Notes in Computer Science, pages 742–766. Springer.          peng Wang, and Xiangyu Zhang. Validating network
  protocol parsers with traceable rfc document inter-           Table 4: The statistics of benchmark programs
  pretation. In Proceedings of the 34th ACM SIGSOFT        ID     Project Name       C Size   Rust Size     #F    #RP
  International Symposium on Software Testing and
  Analysis, ISSTA 2025.                                    1      quadtree              437      1,180       31      17
                                                           2      buffer                452      1,111       40      30
Mingwei Zheng, Danning Xie, and Xiangyu Zhang.             3      genann                690      2,325       27      30
  2025. Large language models for validating network       4      libtree             1,412      2,617       32      41
  protocol parsers. arXiv preprint arXiv:2504.13515.       5      urlparser             440      1,380       21      52
                                                           6      ed-1.19             2,584      5,462      137      80
Shiyao Zhou, Jincheng Wang, He Ye, Hao Zhou, Claire        7      mcsim-6.2.0        20,033     35,558      506      80
  Le Goues, and Xiapu Luo. 2025. Lwdiff: An llm-           8      hello-2.12.1       37,192     10,372      176      88
  assisted differential testing framework for webassem-    9      indent-2.2.13      20,927     15,066      128     100
                                                           10     pth-2.0.7           8,797     12,649      235     102
  bly runtimes. In 2025 IEEE/ACM 47th International
                                                           11     gzip-1.12          53,751     21,463      244     122
  Conference on Software Engineering (ICSE), pages
                                                           12     pexec-1.0rc8        5,684     12,027      158     156
  769–769. IEEE Computer Society.                          13     units-2.22          7,253     11,188      144     185
                                                           14     patch-2.7.6        54,350    114,076      601     361
                                                           15     cpio-2.14          71,819     84,012      707     431
                                                           16     cflow-1.7          45,223     25,467      480     476
                                                           17     enscript-1.6.6     38,424     78,159      259     523
                                                           18     libosip2-5.3.1     18,848     34,195      726     628
                                                           19     rcs-5.10.1         63,254     35,811      496     664
                                                           20     grep-3.11         117,416     84,706      867     725
                                                           21     diffutils-3.10    112,943     96,418      853     760
                                                           22     findutils-4.9.0   136,421    143,361    1,232     835
                                                           23     sed-4.9            91,818     66,580      675     835
                                                           24     make-4.4.1         31,866     35,395      445     997
                                                           25     wget-1.21.4       136,566    189,761    1,355   1,320
                                                           26     tar-1.34          102,864    137,655    1,669   1,399
                                                           27     gawk-5.2.2         65,617    134,098    1,450   1,792
                                                           28     glpk-5.0           77,420    138,372    1,523   2,731


                                                          A      Appendix
                                                          A.1     Details of Experimental Subjects
                                                          The details of the experimental subjects are shown
                                                          in Table 4. Specifically, the columns C Size
                                                          and Rust Size report the sizes of the original
                                                          and C2RUST-translated code, respectively. The
                                                          columns #F and #RP show the number of func-
                                                          tions and raw pointers in the Rust output, respec-
                                                          tively. The benchmark spans programs from a few
                                                          hundred to 136K LOC and 17 to 2,731 raw point-
                                                          ers, providing a diverse set for evaluating PR2 ’s
                                                          effectiveness and scalability.

                                                          A.2     An Example of Rust Data Structures
                                                          We present a case study demonstrating how PR2
                                                          effectively transforms C code into safer and more
                                                          idiomatic Rust by leveraging Rust’s data structures
                                                          and APIs. As shown in Figure 9, the code snip-
                                                          pet is derived from a variant of the C standard
                                                          library function strtoull, which parses C strings
                                                          into integer values based on a specified numeric
                                                          base. Specifically, the original Rust program gen-
                                                          erated by the tool C2RUST, which is shown in
                                                          Figure 9(a), contains unreachable branches caused
                                                          by the unsatisfiable conditions at lines 5 and 7.
                                                          Meanwhile, it relies on raw pointer arithmetic via
1 let mut s: *const c_char = nptr;                                               1 pub unsafe extern "C" fn DoOptimalDesign(mut panal: PANALYSIS) {
2 if (base == 0 as c_int || base == 16 as c_int)                                 2     let mut nDesignPts: c_long = 0;
3                                                                                3     let mut piDesign_mask: *mut c_int = 0 as *mut c_int;
     && ({
4                                                                                4     while i < dim {
        let mut __res: c_int = 0;
5                                                                                5         ...
        if ::std::mem::size_of::<c_uchar>() as c_ulong > 1 {
6                                                                                6         j = 0 as c_int as c_long;
7          if 0 != 0 {...}
                                                                                 7         while j < nDesignPts {
8       } else {
                                                                                 8             if *piDesign_mask.offset(j as isize) == … {...}
9          __res = toupper(*s.offset(1 as isize) as c_int);                      9             j += 1;
10      }                                                                        10        }
11      __res                                                                    11        *piDesign_mask.offset(iBest as isize) =
12
     }) == 'X' as i32                                                            12            (*piDesign_mask.offset(iBest as isize) == 0) as c_int;
13
   {                                                                             13        i += 1;
14
      s = s.offset(2 as c_int as isize);                                         14    }
15
          base = 16 as c_int;                                                    15    free(piDesign_mask as *mut c_void);
16
                                                                                 16    CloseOptFiles(panal);
17 }                              (a) Before rewrite
                                                                                 17 }
1    let s: &[std::os::raw::c_char] = if nptr.is_null() {                                                  (a) Before rewrite
2         &[]
3
     } else {                                                                    1 pub unsafe extern "C" fn DoOptimalDesign(mut panal: PANALYSIS) {
4
          let mut len = strlen(nptr);                                            2     let mut nDesignPts: c_long = 0;
5
6         std::slice::from_raw_parts(nptr, len as usize)                         3     let mut piDesign_mask: Vec<c_int> =
7    };                                                                          4         match nDesignPts > 0   {
8    if s[index] as c_int == '0' as i32 {                                        5              True => vec![0; nDesignPts as usize],
9         if (base == 0 as c_int || base == 16 as c_int) &&                      6              False => Vec::new()
10               s.get(index + 1).map_or(false, |&x| x as c_int == 'X' as i32)   7         };
11                                                                               8     while i < dim {
          {
12                                                                               9         ...
                index += 2;
13                                                                               10        j = 0 as c_int as c_long;
14              base = 16;
                                                                                 11        while j < nDesignPts {
15        }
                                                                                 12            if piDesign_mask[j as usize] == … {...}
16   }                                                                           13            j += 1;
17                                 (b) After rewrite
                                                                                 14        }
                                                                                 15        piDesign_mask[iBest as usize] =
Figure 9: An example of rewriting a raw pointer with a                           16            (piDesign_mask[iBest as usize] == 0) as c_int;
                                                                                 17        i += 1;
slice and utilizing Rust inherent APIs                                           18    }
                                                                                 19    CloseOptFiles(panal);
                                                                                 20 }
offset, further introducing potential invalid mem-                                                          (b) After rewrite
ory operations. After the raw pointer rewriting and
                                                                                 Figure 10: An example of a raw pointer eliminated by
data structure usage repair, PR2 replaces the raw
                                                                                 the full-featured PR2 but not by the ablation NT
pointer s with a Rust slice (declared and initialized
at line 5) and utilizes the API get to safely access                             to lift the pointer to a Vec, following the decision
elements by index, returning an Option instead of                                tree defined in the tree in Figure 3. In contrast,
performing unchecked access. PR2 also employs                                    without decision tree-based prompting, the LLM
the API map_or, which allows the program to ap-                                  fails to identify this rewriting opportunity within
ply a closure to the retrieved character if it exists,                           the allowed rewriting budget.
or return a default value false when the index is
out of bounds. This effectively eliminates the need
for fragile conditional logic and pointer arithmetic.
This case illustrates the empirical benefit of PR2 in
semantically understanding the original C logic and
intelligently selecting Rust data structures as the
abstractions of raw pointers through pointer lifting.

A.3        An Example of Ablation Study
Figure 10 presents an example that is success-
fully handled by the full-featured PR2 but not by
the ablation NT. For illustration, we show only a
partial snippet of the function DoOptimalDesign,
which in its entirety spans 208 lines—posing sub-
stantial challenges for the LLM to reason about
raw pointer usage. Guided by the prompt struc-
ture shown in Figure 4, PR2 is able to identify
the ownership property, the buffer shape, and the
memory read/write operations of the raw pointer
piDesign_mask. These analyses enable the model
A.4    Full Prompts of PR2
In this section we present prompts of PR2 .

  Full prompts for pointer lifting
  Here is a Rust function translated from C code and a raw pointer in it:
  Function: #FUNCTION_CONTEXT#
  Raw pointer: #POINTER_DECLARATION#
  Please give a retype option for the pointer based on the following decision tree:
 (0) Is this pointer belonging to one of the following cases: a. A pointer with a type of void, which means this pointer may
  have variable type; b. A pointer that points to pointers(double pointer or higher level pointers); If this pointer belongs to
  above cases, return with “CANNOT_REWRITE”, otherwise, jump to (1)
 (1) Is the memory value represented by right hand side(RHS) will be owned by this pointer? Typically, if RHS statements
  are function calls(could be GNU C library functions or other functions seen previously in this program) allocating memory
  region or initializing objects or arrays, it is regarded as owning pointers, otherwise the pointers should be considered as
  non-owning, If owning, jump to (2), non-owning, jump to (3)
 (2) Is the memory an individual region or an array? individual then jump to (4), array jump to (5).
 (3) Is the memory is an individual region or an array? individual then jump to (6), array jump to (7).
 (4) This is a final state of the decision tree, The pointer seems to be proper to convert to Option<Box<ORIG_TY>> by
  Box::from_raw, and if this pointer is returned, use Box::into_raw to convert back.
 (5) This is a final state of the decision tree, The pointer seems to be proper to convert to Option<Vec<ORIG_TY>>.
 (6) Will the memory region be written in this function? Yes, jump to (8), No jump to (9)
 (7) Will the memory region be written in this function? Yes, jump to (10), No jump to (11)
 (8) This is a final state of the decision tree, The pointer seems to be proper to convert to
  Option<&mut ORIG_TY>
 (9) This is a final state of the decision tree, The pointer seems to be proper to convert to
  Option<&ORIG_TY>
 (10) This is a final state of the decision tree, The pointer seems to be proper to convert to
 &mut [ORIG_TY]
 (11) This is a final state of the decision tree, The pointer seems to be proper to convert to
 &[ORIG_TY]
 You are expected to ONLY return one of following 6 candidates: ‘Option<Box<ORIG_TY>>’, ‘Option<Vec<ORIG_TY>>’,
 ‘Option<&mut ORIG_TY>’, ‘Option<&ORIG_TY>’, ‘&mut [ORIG_TY]’, ‘&[ORIG_TY]’, DO NOT rewrite the function
  now before more examples given.


  Full prompts for statement refactoring
 Good, now based on previous analysis, please rewrite “Raw pointer” in “Function” below to safe structure you found just
 now. If the pointer is null, use None or zero length slice to rewrite.
 Function: #FUNCTION_CONTEXT#
 Raw pointer: #POINTER_DECLARATION#
 Here are some examples that may be helpful: #EXAMPLES#
 Following are some struct definitions and types of static variables that may be useful(DO NOT MODIFY ANYTHING IN
 THEM):
 Structs: #STRUCTS_USED#
 Statics: #STATICS_USED#
 Format instructions:
 1) Your response should include a rust code snippet starting with ˋˋˋrust and ending with ˋˋˋ, which contains the rewritten
 function inside.
 2) When rewriting, please DO NOT change types of function parameters or return values or struct field definitions.
 3) Only generate rewritten function and DO NOT generate any Rust ‘use xxx;’ statements outside rewritten function.
 4) NEVER omit any lines in “Function” even if they remain unchanged.
 5) DO NOT omit any variable type annotations.


  Prompts for syntax error fixing
 Please fix the syntax error called “#ERROR_DESCRIPTION#”, the error is reported at site
 #ERROR_SITE#. Also, do not generate any explanations besides fixed code. If you cannot fix it due to constraints, response
 with CANNOT_FIX. the key context snippet around the error is: Snippet: #FOCUS_SNIPPET# You need to fix the error in
 “Snippet” and return the revised snippet. DO NOT return full function.


  Prompts for testcase error fixing
  Good. Previous rewrite has passed the compiler checks successfully, but it failed to pass test cases provided in the program
  with following stack traces:
  Backtrace: #EXEC_LOG#
Current state of the key function in this error is shown below:
line #START_LINE#: #REWRITTEN_CODE#
Originally this function is: #ORIGINAL_CODE#
The diff of function: #DIFF_LOG#
Can you try to fix this given error without introducing new raw pointers? Your response should only be a revised version
of “Current Function”. If you think the semantics cannot be rewritten without introducing raw pointers, reply with
CANNOT_FIX.
