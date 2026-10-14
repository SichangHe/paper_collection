                                         Translating C To Rust: Lessons from a User Study†

                                                               Ruishi Li*                                         Bo Wang*                                  Tianyu Li
                                                       liruishi@u.nus.edu                                bo wang@u.nus.edu                            tianyuli@u.nus.edu
                                                National University of Singapore                    National University of Singapore            National University of Singapore
                                                            Singapore                                         Singapore                                    Singapore

                                                                                  Prateek Saxena                                              Ashish Kundu
                                                                             prateeks@comp.nus.edu.sg                                      ashkundu@cisco.com
                                                                          National University of Singapore                                    Cisco Research
arXiv:2411.14174v2 [cs.SE] 6 Dec 2024




                                                                                     Singapore                                              San Jose, CA, USA


                                             Abstract—Rust aims to offer full memory safety for programs,                      A different approach has been to write secure code which
                                        a guarantee that untamed C programs do not enjoy. How difficult                    is free of memory safety bugs from the ground up. The idea is
                                        is it to translate existing C code to Rust? To get a complementary                 to have a stricter language and compiler that forces developers
                                        view from that of automatic C to Rust translators, we report on a                  to rewrite unsafe code to use safe patterns everywhere. The
                                        user study asking humans to translate real-world C programs to                     advantage is that full memory safety can be achieved mostly
                                        Rust. Our participants are able to produce safe Rust translations,
                                                                                                                           statically, while a few runtime checks incur low overheads.
                                        whereas state-of-the-art automatic tools are not able to do so. Our
                                        analysis highlights that the high-level strategy taken by users                        Designing safe C dialects with that goal has a long history.
                                        departs significantly from those of automatic tools we study. We                   These dialects largely aim to retain low-level features of C for
                                        also find that users often choose zero-cost (static) abstractions                  compatibility, making it difficult to move away from unsafe C
                                        for temporal safety, which addresses a predominant component of
                                                                                                                           patterns entirely while keeping overheads low [34], [45]. More
                                        runtime costs in other full memory safety defenses. User-provided
                                        translations showcase a rich landscape of specialized strategies                   recent designs aim for better compatibility by allowing mixed
                                        to translate the same C program in different ways to safe Rust,                    (statically) safe and unsafe C [22], but when temporal memory
                                        which future automatic translators can consider.                                   safety is desired in them, overheads can exceed 30% [40].
                                                                                                                               Rust is an alternative mainstream language that offers
                                                                     I.    Introduction                                    low-level control over memory, while providing full memory
                                                                                                                           safety. It has a growing ecosystem and increasing support from
                                            Memory safety vulnerabilities in C programs are still a                        commodity OSes. It departs from the conventional approaches
                                        prominent category of CVEs reported in commodity software,                         to safe C dialects in that it largely abandons the programming
                                        and number in thousands each year [29]. Several approaches                         abstractions in C, such as the use of unchecked raw pointers
                                        to secure such unsafe code are being investigated.                                 and unsafe type casts. It is natural to ask: How difficult is it
                                                                                                                           to translate existing C code to Rust then?
                                            Full memory safety through runtime checks inserted by
                                        compiler instrumentation is achievable. However, it incurs high                        In the last few years, automatic techniques to translate
                                        performance overhead (≥ 50%) and is often not deployed in                          C code to Rust have started to emerge. There are two main
                                        production [43], [44]. Instead, partial memory safety defenses                     approaches, one based on compiler-based analysis [24], [33]
                                        which have overheads below 20% have found deployment [53].                         and another based on large language models (LLMs) [25], [58].
                                        Emerging hardware features can reduce performance over-                            But both approaches have had very limited effectiveness so
                                        heads of partial safety techniques, but even then, faulty pro-                     far, even on small programs of about 100 lines of code. For
                                        grams that will often ungracefully abort in production systems                     example, Emre et. al. report that only about 11% of raw C
                                        have limited appeal. Similarly, automatic patching techniques                      pointers can be converted to safe Rust references through static
                                        that can localize bugs and suggest fixes for them are being                        analysis [24]. Similarly, recent work on Flourine [25] reports
                                        developed [28], [32], [49], [50]. But these approaches do not                      that less than half of the small C programs they consider can
                                        aim to rule out the existence of memory safety bugs altogether.                    be auto-translated to Rust using LLM-based repair.
                                          *                                                                                     It is unclear what strategies, if any, enable a successful
                                             Contributed equally to this work.                                             search for C to Rust translations. In order to gain a com-
                                           †
                                             This is the extended version of the paper. The definitive Version of Record   plementary perspective, in this paper, we study how human
                                        is to be published in NDSS 2025.
                                                                                                                           users approach the C to Rust translation task. We conducted
                                                                                                                           a user study in which we asked undergraduate students taking
                                                                                                                           a course in computer security to translate a given set of real-
                                        Network and Distributed System Security (NDSS) Symposium 2025                      world C programs to safe Rust. Our participants are familiar
                                        24-28 February 2025, San Diego, CA, USA
                                        ISBN 979-8-9894372-8-3                                                             with C and memory safety issues, but have minimal prior
                                        https://dx.doi.org/10.14722/ndss.2025.241407                                       exposure to Rust. To the best of our knowledge, this is the
                                        www.ndss-symposium.org                                                             first such analysis of a user study on C to Rust translation.
                                                                          1   fn change_buf(i: usize) {
    33 of our user study participants consented to their trans-                                                                     Ownership
                                                                          2      let mut buf: Vec<i32> = vec![0; 2];
lated programs being analyzed and reported on. Most of the                3      let a: &Vec<i32> = &buf;    Immutable Borrow (a)
users succeed in providing reasonable translations of our C               4      let a1: &i32 = &buf[1];              Immutable Borrow (a1)
benchmark to Rust, whereas state-of-the-art automatic C to                5      println!("a[0]: {:?}, a1: {:?}", a[0], a1);
Rust translation tools are ineffective. Analyzing how users               6      println!("a[{:}]: {:?}", i, a[i]);
succeed is our main goal. We highlight several high-level                 7      // Runtime bounds check: The above line might panic
principles and strategies that are common across the user trans-          8
                                                                          9       let x: &mut Vec<i32> = &mut buf; Mutable Borrow (x)
lations, which could be useful for future automatic translators.
                                                                         10       x[0] = 1;
                                                                         11       let x0: &mut i32 = &mut (*x)[0];         Re-Borrow (x0)
    First, we find that all user-provided Rust translations se-          12       *x0 = 2;
mantically lift from the low-level abstractions used in the C            13       x.clear();
code to re-express the logic in Rust, rather than trying to mimic        14       // *x0 = 3; // cannot use `x0` anymore
the original program and data-flow structure too closely. This           15       use_buf(buf); // fn use_buf(buf: Vec<i32>) {...}
                                                                                                                                     Transferred
approach helps break free of the low-level constraints present           16   }                                                      to use_buf
in the original C code, which would violate the strict rules             Fig. 1: A Rust code example showing the concepts of owner-
in Rust if preserved. Rust enforces stricter rules on pointer            ship transfer, mut./immut. borrowing, and reference lifetime.
aliasing than C. Users decomposed the object lifetimes in
different ways that are specialized to access patterns used
for the object to satisfy Rust rules. This shows that there are
multiple strategies to translate the same C program to safe                                       II.   Background
Rust, with room for context-specific translation strategies.
                                                                           Rust allows programs to have fine-grained control over
    Second, we find that resulting Rust translations often               memory but with spatial and temporal memory safety.
contain zero-cost statically-checked safety abstractions. Tem-
poral memory safety, which is a source of significant runtime            A. A Tour of Safe Rust
overhead in many prior defenses [40], [44], is achieved mostly
statically. The resulting Rust programs have comparable per-               We briefly explain Rust design principles for achieving full
formance to C, and rarely more than 20% slower than the                  memory safety with a running example shown in Figure 1.
corresponding C code, even though our participants are not               Ownership. Rust ensures that each data object has an exclu-
explicitly asked to optimize for performance. At the same                sive owner at any given program point [18]. When the variable
time, known spatial and temporal vulnerabilities in our C                owning an object goes out of scope, the compiler automatically
benchmarks are eliminated in the translated Rust code. This              deallocates the object. The single-owner principle ensures that
suggests that C to Rust translation is worth it, as the trade-off        the object is deallocated only once, avoiding double-free bugs
between performance and security we observe in translations              prevalent in C programs. The compiler knows the scope of
by non-expert Rust users is desirable.                                   all objects in the program. Stack variables have statically
                                                                         determined block/function scope, and so do globals. Objects
    Third, nearly all Rust translations have functional discrep-         can be owners of other objects, creating a transitive chain of
ancies compared with the corresponding C code. These dis-                ownership. The chain starts with a stack/global variable, so the
crepancies are easy to find with fuzzing and Rust translations           compiler can track ownership of all objects.
of the same C program have correlated failures, i.e., they often
fail the same tests. Some of these discrepancies are expected                 Ownership can not be duplicated but only transferred
since undefined behavior present in C programs are handled               between variables through assignment or parameter passing.
differently by different users. But, several others are logical          The Rust compiler, therefore, tracks the unique owner of every
errors, suggesting a “last mile” phenomenon at play: While               object at every program point. For example, the buf variable
users find it feasible to convert most C functionality to its Rust       in the example of Figure 1 is on the stack and encapsulates
counterpart, making a 100% correct translation is tedious.               a (smart) pointer to Vec object allocated on the heap. The
                                                                         object allocated on Line 2 in Figure 1 has a unique owner
    Lastly, in order to examine the broader validity of our              buf from Line 2-14, after which the ownership transfers to the
observations, we perform a post-hoc investigation of a mature            first parameter of use_buf() . The object will be deallocated
open-source Rust project that mirrors the functionality of a set         when the new owner goes out of scope, i.e., at the end of the
of popular C programs. Several findings from our user study,             function scope of use_buf() .
which involves non-experts, are also seen in the open-source             Borrowing. Exclusive ownership, by itself, disallows all alias-
project maintained by more experienced Rust developers.                  ing altogether, which is too restrictive. Rust relaxes this restric-
                                                                         tion by introducing a borrowing mechanism. It allows creating
Contribution. We report on the lessons garnered from the                 references (also called borrows) to temporarily access the data
first user study on translating real-world C programs to Rust            value without transferring the ownership. References a , a1 ,
by non-expert Rust users. Our work sheds light on strategies             and x borrow from the owner buf , whereas x0 reborrows
and policy decisions that users have to make, which are com-             from x in the example. This allows limited forms of aliasing.
plementary to automatic mechanisms. We highlight the end
gains in user-provided translations, such as the ubiquitous use          Lifetime. With borrowed references, it becomes essential to
of zero-cost temporal safety abstractions, elimination of unsafe         ensure that a reference never points to an object that has been
code patterns, and the trade-offs with functional correctness.           deallocated. The Rust compiler statically tracks the lifetime of

                                                                     2
variables: the region of code that the variable must be valid            internal use of unsafe Rust and have been proven sound [36].
for. Rust enforces that the lifetime of all references is a strict       Mutable pointers are particularly common in multi-threaded
subset of the lifetime of the owner statically. Since the object         code, and in fact, concurrent C code is notoriously difficult to
will be deallocated only when the lifetime of the owner expires,         analyze for memory safety bugs. The Rust compiler enforces
all live references point to valid objects, eliminating use-after-       that concurrent access or data copying across threads will never
free vulnerabilities that arise in C programs. The example in            result in memory safety violations. Thus, when Rust allows
Figure 1 creates multiple references to an array object. The             relaxations to the AXM principle, runtime checks are used for
variable buf gets ownership of the heap-allocated array on               memory safety. We will refer to all such references that carry
Line 2. There are four borrowed references created directly or           dynamic checks as dynamic references to avoid confusion with
indirectly from buf on lines 3, 4, 9, and 11. Their lifetimes are        regular Rust references that obey the AXM principle.
enforced to be smaller than that of buf and are highlighted.
The object is automatically deallocated only when the lifetime           Spatial Bounds Checking. The Rust compiler aims to ensure
of the owner buf ends, thereby ensuring that all references              that the accesses by owners or references to the referent
point to valid memory throughout their lifetime.                         are within spatial bounds. For several types of objects, the
                                                                         compiler can do so statically, but when it cannot, it adds
Aliasing Xor Mutability (AXM). Aliasing references can up-               runtime bounds checks. In line 6 of Figure 1, a[i] operation is
date the object storage, possibly moving them, and associated            checked to see if i is within the boundary of buf . If passing 3
allocation metadata (e.g. size, internal pointers) can become            to i, the Rust code would abort the execution of the program.
inconsistent. When multiple references are pointing to the               Type Safety. Rust is a type-safe language and supports safe
same object (e.g. a vector type) to insert/delete elements or            type casting among data types using APIs provided in the
change its capacity, the location of its internal buffer and size        standard library. All type casts guarantee that the converted
metadata might change. Consequently, this will invalidate other          values are within the legal range of the target type. Safe Rust
references to the same object, including iterators and references        disallows direct reinterpretation of memory to an unsafe type.
to its elements. Memory-unsafe languages like C leave careful            For example, the conversion between pointers ( void*), non-
management of aliased pointers to the programmer, which                  primitives ( struct , union, etc.) and primitives (bool , enum ,
has been a source of mistakes. To avoid this, Rust proposes              etc.) can cause memory errors in C, but safe Rust forbids them.
Aliasing Xor Mutability (AXM) principle. First, references are
divided into two types: mutable ( &mut) and immutable ( & ).
Mutable references can read and write the referent object,               B. Existing Automatic C to Rust Translation
while immutable ones have read-only access. Second, the                      There have been 2 main approaches to automatic C-to-Rust
Rust compiler enforces that either only one mutable reference            translation: One based on compiler or static analysis, while the
or multiple (aliasing) immutable references are active at a              other using large language models (LLMs) for code synthesis.
program point. Mutable aliased references can not be active
at the same program point. The AXM principle eliminates the              Compiler-based Approach. Most of the work in this direction
need for careful pointer invalidation by the programmer and              decomposes the code translation problem into two stages: (1) C
helps memory safety in concurrent code as well.                          to unsafe Rust, and (2) unsafe Rust to safe Rust [23], [24], [60].
                                                                         A mature tool called c2rust performs a robust line-by-line
    Specifically in the example of Figure 1, Lines 3-6 have              syntactic translation from C to corresponding unsafe Rust
multiple immutable references to buf, and Lines 9-13 have                code blocks [33]. The use of unsafe{...} keyword allows
one mutable reference at each point, created using &mut type             bypassing the Rust safety checks mentioned above in the en-
declaration. The compiler can statically infer the lifetime of x         closed code block. The resulting Rust translation can thus rely
and other mutable references that may alias it, such as x0 . It          on raw pointers ( mut* ), C-compatible data types, and foreign
automatically splits their range of legal use such that there will       function calls to C libraries (extern "C" fn). The second
be a single mutable reference to the object active in scope at           stage of the translation is where the bulk of the challenges lie.
each statement, i.e, x is permitted on Line (9 − 10, 13) and x0          The goal of prior automatic tools is to refactor the unsafe
on Lines 11-12. The compiler would forbid using x0 on or                 Rust code into safe Rust and reduce unsafe code. Laertes
after line 13 as it would create two mutable references to the           proposed a trial-and-error approach leveraging Rust compiler
vector elements, highlighted by commented code on Lines 14               feedback to lift a certain subset of raw pointers into safer Rust
for illustration. In the equivalent C code, dereferencing x0 on          references [24]. However, a later work reports that the majority
Line 14 would be legal and lead to undefined behavior, since             of raw pointers (79% in their benchmarks) cannot be translated
x0 refers to a vector whose underlying elements were cleared             to safe references via such techniques [23]. Crown proposed
(possibly deallocated) via x on Line 13. This can result in out-         improvements using ownership analysis based on constraint
of-bound access due to a dangling dereference. Such memory               generation and SAT-solving, for a subset of pointer types such
errors are disallowed by the AXM principle in Rust.                      as Box<T> [60]. We present an evaluation of these state-of-
                                                                         the-art tools later and find that a majority of C pointers are
Runtime AXM and Thread Safety. The AXM principle                         not lifted into safe Rust abstractions by present tools.
can be too restrictive in certain circumstances. When multiple
mutable references are necessary, Rust programs can resort               LLM-based Approach. Another line of work uses LLMs to
to runtime borrow checks and reference counting for memory               translate C programs to Rust [25], [58]. The LLM-guided
safety, through the use of data types such as RefCell<T> and             approach tends to produce code that is much more readable
Rc<T> for single-thread synchronization [10] and Mutex<T>                and idiomatic. Modern LLMs can suggest safe Rust data types,
and Arc<T> for multi-thread synchronization. These generic               APIs, and coding conventions to use. However, LLM-based
types are implemented in the Rust standard library with                  translation is often difficult to control as LLMs can make

                                                                     3
semantic mistakes [15]. One of the most recent tools called                                      TABLE I: C Benchmarks for the User Study.
Flourine, reports that with current LLMs (GPT-4, claude3,
and so on), less than 20% for C programs longer than 150                                           Prog. Name        LoC     Description
lines of code can be satisfactorily translated to Rust [25]. We                                    csplit (bsd3 )    322     Split files based on patterns
                                                                                                   expr (bsd)        451     Evaluate expressions
evaluate Flourine as well, and we have similar findings.                                           fmt (bsd)         415     Format text files
                                                                                                   join (bsd)        472     Join lines of two files
    In summary, existing automatic techniques are insufficient                                     printf (bsd)      375     Print formatted text
to translate even small C programs of about 200 LoC to Rust.                                       test (bsd)        536     Check file attributes and values
                                                                                                   shoco             388     String Data Compression
Our observations from the user study hope to offer a holistic                                      urlparser         437     Parse URLs
perspective on how users get past the inherent challenges.

                                                                                        chose 6 C programs3 from the BSDCoreUtils [41] collection
                             III.   User Study                                          of system utilities and 2 libraries, i.e., shoco and urlparser.
    Prior literature has taken a bottom-up approach to the                                  All of the chosen programs (Table I) are self-contained,
problem of C to Rust translation, aiming to show how au-                                requiring only the C standard library as a dependency. Four
tomatic tools can address particular sub-problems encountered                           programs—csplit, fmt, join, and test—perform file pro-
in translation. Our study offers a complementary perspective                            cessing. The expr and printf are pure computation utilities
on how human users approach the same task. This gives us                                for strings and numbers. The shoco library is for data com-
a top-down view of the problem: We can see what common                                  pression, and the urlparser library parses URL strings.
strategies do users use and what challenges remain thereafter.
                                                                                        Task Requirements. Each individual participant is tasked to
    Our participants are undergraduate students enrolled in                             translate the assigned C program into safe Rust, satisfying two
a course on computer security. All participants are familiar                            requirements, i.e., safety and functional correctness.
with memory safety errors in C/C++ programs and were
given an introduction to Rust1 . The task, which is part of a                            1) Safety. The translated program must be written in safe
graded course project, is to translate 8 real-world C programs                              Rust only. The use of keyword unsafe is strictly for-
we collected into safe Rust. Each participant is randomly                                   bidden. For dependencies, only the Rust standard library
assigned one out of 8 such C programs and is asked to provide                               should be used by default. When that is insufficient to
a translated program in safe Rust within 20 days2 . The C                                   implement certain functionalities, additional third-party
programs are taken from GitHub and are small due to the                                     dependencies can be used if they are well-maintained.
20-day time limit, with lengths varying from 322 to 536 LoC.                             2) Functional correctness. The translated Rust program
The participants were permitted to consult the web freely and                               should have the equivalent external behavior to the C
use any existing tools, for example, c2rust and LLMs.                                       source program. Since most of the chosen C programs do
                                                                                            not come with high-quality unit tests by default, we asked
Ethical Concerns. This study has been granted an IRB exemp-                                 the participants to write their own tests with line coverage
tion from the NUS School of Computing DERC (Department                                      aiming for at least 85% on the original C program to
Ethics Review Committee). We followed the procedure advised                                 test correctness. If the source program and the translation
by the IRB to protect the privacy of the participants and avoid                             behave the same (i.e., output, return code, effects on the
bias. 73 undergraduate students who undertook the study were                                file system, etc.) on those tests, we say that the translated
initially invited to give consent towards the use of their sub-                             program is correct if it passes all test cases created
missions. 33 participants gave their consent and only their data                            by users. Besides the final version of their translated
is included in this study. The participant data was anonymized                              program, we also asked the participants to submit an
and kept confidentially on our research infrastructure, without                             initial version of the translation that could compile before
being hosted on third-party cloud services. Aggregate statistics                            they developed tests, so we could analyze the changes.
are reported here as far as possible, and wherever code snippets
are shown for illustration of a concept, they are constructed                           Collected Translations. The 33 participants provided 31 final
synthetically by retaining the high-level patterns seen in user                         translations that can compile and achieved 70% to 98% line
submissions (not replicated). Analysis of the participants’ data                        coverage on the C program under their respective tests. 26
was conducted only after grades were finalized to avoid any                             of the 31 translations pass tests that reach 85% coverage and
influence resulting from the study on the grades.                                       nearly all of them4 have coverage above 80%. All of the 31
Benchmarks. Table I shows the C programs we collected                                   final translations are written in pure safe Rust, without the use
for the user study. These programs are representative of C                              of unsafe . They form the main target of our analysis. 17
programs that implement lower-level functionality and self-                             participants also submitted their compilable initial versions.
manage memory where memory safety errors arise. Such                                    Our Goal. We analyze these 31 final translations to gain
functionalities are often implemented in C and used by higher-                          insights into the following research questions:
level software systems. We also considered the translation                              RQ1. Is there a set of common strategies that users used for
difficulty and chose programs between 300 and 600 LoC,                                  successful translation?
considering the time and effort of the participants. Thus, we                           RQ2. How is the security-performance trade-off in the Rust
                                                                                        translation?
   1 The content described in Section II-A with example exercises constitutes
the introduction given, after the participants are familiar with C memory errors.         3 Obtained from the BSDCoreUtils [41] code repository (version d2b28e0).
   2 The participants conducted their work in April 2024.                                 4 Except for 2 translations with coverage less than 80%.




                                                                                    4
 1 static void center_stream(FILE *stream, const char *name)            1    fn center_stream<R: BufRead>(mut stream: R, _name: &str, config:
 2 {                                                                               &Config) {
 3     char *p1, *p2; // aliased pointers                               2        let mut p1 = String::new();
 4     size_t len; int w1, w2; wchar_t wc;                              3        while let Ok(bytes_read) = get_line(stream, &mut p1) {
 5     // ...                                                           4            if bytes_read == 0 { break; }
 6     while ((p1 = get_line(stream)) != NULL) {                        5            let len: usize = p1.trim().chars().map(|c| if c == ’\t’
 7         len = 0;                                                               { ’ ’ } else { c }).map(char::len_utf8).sum();
 8         for (p2 = p1; *p2 != ’\0’; p2 += w2) {                       6            let padding = (config.goal_length - len) / 2; //
 9             if (*p2 == ’\t’)                                                   Calculate padding to center the line
10                  *p2 = ’␣’;                                          7            for _ in 0..padding { print!("␣"); }
11             // ... skipped                                           8            println!("{}", p1.trim());
12             if (len == 0 && iswspace(wc)) p1 += w2;                  9        } ...
13             else len += w1;
14         }
15         while (l < goal_length) {                                   Fig. 3: A safe Rust translation of the C program (Version A)
16             putchar(’␣’);
17             len += 2;
18         }
19         puts(p1);
20     } ...                                                           TABLE II: Dissimilarities between source C programs and
21 }                                                                   Rust translations. Numbers are averaged over all translations.
  Example C Program (above) → c2rust Translation (below)                 Benchmark        #user-                 #function              #signature              #pointer decl.
 1 unsafe extern "C" fn center_stream(                                                 translations           (kept/rm./add.)         (sim./dissim.)              (kept/rm.)
 2   mut stream: *mut FILE, mut name: *const libc::c char)               csplit             5                     7/2/3                    5/2                   54% / 46%
 3 {                                                                     expr               2                    8 / 10 / 8                4/4                   61% / 39%
 4     let mut p1: *mut libc::c char = 0 as *mut libc::c char;           fmt                4                    10 / 2 / 2                6/5                   82% / 18%
 5     let mut p2: *mut libc::c char = 0 as *mut libc::c char;           join               2                    6 / 6 / 11                4/2                   70% / 30%
 6     let mut wc: wchar_t = 0; // ...                                   printf             3                    11 / 2 / 4                5/6                   71% / 29%
 7     loop {                                                            test               4                    16 / 2 / 3               10 / 6                 89% / 11%
 8         p1 = get_line(stream);                                        shoco              6                     6/0/2                    2/5                   72% / 28%
 9         if p1.is_null() { break; }                                    urlparser          5                    18 / 3 / 3               3 / 15                 79% / 21%
10         len = 0 as libc::c int as size_t;
11         p2 = p1;
                                                                                         Rust library types
12         while *p2 as libc::c int != ’\0’ as i32 {
                                                                                         Owned types               References                  Description
13             if *p2 as libc::c int == ’\t’ as i32 {                    C library
14                  *p2 = ’ ’ as i32 as libc::c char; }                pointer types     String               23   &String, &str         29    UTF8 string type

                                                                                         Option<String>        9   Option<&str>           3    Optional String
15             // ...                                                    char*
16             if len == 0 ... && iswspace(wc as wint_t) != 0 {                          Vec<String>          18   &Vec<String>, &[String] 6   Dynamically sized array
                                                                         int16_t*
17                  p1 = p1.offset(w2 as isize);                         int*
                                                                                         Mutex<String>         1   /                           Primitive for thread safety

18             } else { len = ...; }                                     size_t*
                                                                                         OnceCell<String>      1   /                           Write-once String

19             p2 = p2.offset(w2 as isize);                                              Vec<u8>               4   &Vec<u8>, &[u8]       19    Array of bytes
                                                                         FILE*
20         }                                                                             char                  0   &char                  2    A single Unicode scalar value
                                                                         int64_t*
21         while len < goal_length {                                                     [u8; N]               0   &[u8]                 17    Stack array
22             putchar(’ ’ as i32);                                      wchar_t*
                                                                                         [i16; N]              0   &[i16]                 6    Stack array
23             len = (len as libc::c ulong).wrapping_add(2) ...;                         i16 / usize           4   /                           Primitive types
24         }                                                                             File                  7   &File                  2    A file handle
25         puts(p1);
                                                                                         Box<dyn BufRead>      7   &mut dyn BufRead       7    Dynamic trait object
26     } ...
                                                                                         Long tail (30+ types)     …                           …

                                                                                         /                         /                           Eliminated

Fig. 2: (Top) An example of C program with aliasing pointers,
i.e., multiple pointers pointing to the same region of memory.         Fig. 4: Raw C pointers to Rust data types lifted in translations
(Bottom) A line-by-line translation by c2rust. Uses of unsafe          and the number of programs using each Rust type (in blue).
raw pointers and libc APIs/types are highlighted in red.

                                                                         b) even if there exists a way to replace all pointers with
RQ3. What are the common errors and correctness gaps in                     references, the resulting code will violate safe Rust rules.
translated Rust programs?
                                                                           In fact, for our shown example, there is no translation that
RQ4. How do the state-of-the-art automatic C to Rust trans-
                                                                       keeps the original control-flow structure as-is and maps all
lation tools perform on the same task?
                                                                       the original C pointers to Rust references. This is because
                                                                       preserving the original lifetime and read/write semantics of
          IV.   High-Level Approach Taken by Users                     the C variables in the Rust code will always violate the AXM
                                                                       principle, since p2 needs to be a mutable reference and remain
    Fig. 2 shows an example of C code from the fmt bench-
                                                                       alive from Lines 8-14, and that interferes with the use of p1 .
mark and the translation produced by the c2rust tool. The
latter is created by preserving the structure of the original              Despite this apparent challenge, there are ways out of
code, line-by-line and variable-to-variable, but contains unsafe       the quandary, and our participants translated such programs
Rust code blocks. The main challenge is to refactor the unsafe         correctly. We explain what strategies they used and how often.
code to safe Rust. A straightforward removal of the keyword
unsafe does not work as there are two immediate challenges:            A. Semantic Data Type Lifting
 a) the unsafe Rust code, much like the original C code,                  Several users recognize that the low-level char* pointers
    uses low-level raw pointers and C library calls that are           used in the example C code are semantically operating on
    disallowed in safe Rust; and                                       a higher-level data type and they lift the object’s type to a

                                                                   5
                                                    ●   Direct Mapping
 Direct Mapping (36.7%):   Map to Expr (39%):       ●   Map to Expression
                                                                                 1   fn center_stream<R: BufRead>(mut stream: R, name: &str) {
    isdigit                  fopen(file, "w+")      ●   API Emulation
                                                                                 2       // ...
    is_ascii_digit           File::options()        ●   Eliminated               3       while let p1: Vec<char> = get_line(stream) {
                           .read(true)              ●   3rd party APIs           4           for c in p1 { // implicit mutable borrow by the loop
 API Emulation (13.4%):    .write(true)                                          5               if c == ’\t’ {
                           .create(true)                                         6                   c = ’ ’;
    sscanf
                           .truncate(true)
    sscanf_before,                                                               7               } ...
                           .open(file)?;
 sscanf_after                                                                    8               if (l == 0 && isWhiteSpace(wc))
                                                                                 9                   p1.drain(..wcl); // AXM violation (FAIL!)
 Eliminated (7.6%):        3rd party APIs (3.3%):                               10               // ...
    malloc, free, fclose      geteuid                                           11           } ...
                              nix::unistd::get                                  12           println!("{:?}", p1);
                           euid                                                 13       } ...


Fig. 5: Breakdown of C library API translations with examples.                  Fig. 6: A Line-by-line Rust translation that fails to compile.



relevant Rust abstract data type. Figure 3 shows one such suc-                  initial version of Rust code, 10 refined or changed their initial
cessful translation that lifts the char* buffer in C to String                  types chosen to other ones in the final version.
type. The C code with library calls is replaced with invocations
to the Rust String methods. For example, the C code in                           User-provided translations break away from the low-level
Lines 6-20, which is responsible for counting the whitespace                     structure of the original C code by semantically mapping
characters and center-justifying the string, is implemented with                 C data types and APIs to similar ones in Rust. They often
safe Rust String methods in the translation. The result of                       refine their initial guess of such C to Rust mappings.
such type lifting is that the Rust code is less similar to the
original C code in the control-flow structure and variables used.
Table II summarizes the amount of dissimilarity we observe                      B. Dealing with Aliasing
in 31 final translations and their corresponding C code.
                                                                                    Fig. 6 shows another example of translation wherein, after
    Multiple choices for the Rust data types exist here. For                    data types have been lifted, the Rust compiler checks are
example, char* may be lifted to Rust String, Vec<u8> ,                          violated. This example illustrates a separate challenge: Users
Box<[u8]>, and so on. Figure 4 shows the top Rust data                          have to decide how each one of the original C pointers should
types that our participants lifted from C pointers across 8                     be mapped to Rust references while satisfying Rust borrowing
benchmarks in their final 31 translations. Note that there                      rules in the presence of aliases (borrows). Rust provides the
are subtle differences between the original C type and the                      option to use reference-counted dynamic references, which
corresponding lifted data type that the user chose. In Version A,               have accompanying runtime costs, but we see that users did
the code uses a String type, which does not support strings                     not use them for heap and stack data references. Instead, users
with invalid UTF-8 characters (unlike the original C code). The                 found 2 strategies, specialized to the access patterns used by
corresponding Rust translation elides that particular behavior                  the C program, that satisfy static checks of the Rust compiler.
present in the original C code. Section VI quantitatively
analyzes such semantic discrepancies in more detail.                            Strategy (a): Elision. When objects are lifted from C to Rust,
                                                                                many of the original C pointers do not need to be mapped to
    A different sub-challenge with type lifting is how to                       Rust references and can be elided in the translated code. For
translate operations on the original data type, which is often                  example, code in Version A (Figure 3) elides the C pointer
implemented with standard C library API, to corresponding                       p2 because its functionality is encapsulated by Rust String
Rust data type methods. Foreign function interface (or FFI)                     methods. Version A satisfies the Rust compiler checks.
calls to C libraries are disallowed in safe Rust. User transla-
tions used the strategies below to translate C library API calls:               Strategy (b): Cloning. The translation shown in Version
                                                                                B (Figure 7) embodies a different strategy. It satisfies the
(a) Direct Mapping to Safe Rust APIs. 36.7% of the API calls                    Rust borrow checking rules by separating the read and write
    are translated to single safe Rust method calls.                            accesses of the original object into two separate objects. In
(b) Translating to expressions. 39% of the API calls are                        Figure 6, the p1 reference and the iterator are simultaneously
    translated into expressions that make use of multiple Rust                  trying to modify the object, hence violating the AXM principle.
    methods and operators to achieve similar effects.                           In Version B, however, a new copy of the original String
(c) API Emulation. 13.4% of the API calls are translated into                   object is made. The p1 reference can thus remain immutable
    calls to user-implemented functions that emulate them.                      and refer to the original object, while all writes are made to the
(d) Elimination. 7.6% of the calls for manual memory and                        copy by the mutable reference ans. Later on, only the writable
    resource management are eliminated since Rust data types                    copy of the object is used. Such a rewrite mechanism satisfies
    can automatically achieve similar effects.                                  the borrow rules in safe Rust and compiles successfully.
(e) Third-party Libraries. 3.3% of the calls are translated to
    API calls provided by third-party libraries (crates).                           Two pointers to a read-only object can both access the
                                                                                object without any restriction in C. But in Rust, if one reference
The breakdown of these choices with examples is summarized                      is (re)borrowed from the other, it should have a statically
in Figure 5. As a result of the above challenges, we observed                   determined shorter lifetime than that of the other, which is
that the initial guess of the lifted data type chosen by a user                 more restrictive than C. The cloning strategy is thus also useful
was often not optimal. Of the 17 participants who shared their                  when translating C code with multiple immutable pointers. It

                                                                            6
 1 fn center_stream<T: BufRead>(&mut self, stream: T, name: &str) {
 2     for line in stream.lines() {
                                                                                   TABLE III: Temporal and spatial memory safety of data
 3         let p1 = match line {                                                   references used in Rust translations.
 4             Ok(line) => line, Err(e) => { ... }
 5         };                                                                            References   Fraction   Temporal Safety     Spatial Safety
 6         let mut ans = String::new();
 7         let mut len = 0;                                                                                      static   dynamic   static   dynamic
 8         for c in p1.chars() {
 9             // ... if c is a space, skip                                              Owning        49.2%     95.6%      4.4%    1.6%      98.4%
10             if c == ’\t’ {                                                             - stack      14.2%     100.0%     0.0%    12.7%    87.3%
11                 ans.push(’ ’);                                                         - heap       31.4%     100.0%     0.0%    0.0%     100.0%
12             } else {                                                                   - global      4.4%     45.9%     54.1%    0.0%     100.0%
13                 ans.push(c);                                                          Borrowing     50.8%     99.7%     0.3%     9.1%      90.9%
14             }                                                                           - mut.      11.6%     98.6%     1.4%     21.2%     78.8%
15             len += c.width().unwrap_or(1);                                              - immut.    39.2%     100.0%    0.0%     5.5%      94.5%
16         }
17         println!("{:>width$}", ans, width = ...);                                     Nullable      8.3%      100.0%    0.0%     10.8%     89.2%
18     ...
                                                                                         DST           79.7%     99.6%     0.4%     0.0%     100.0%
                                                                                           - string    62.5%     99.7%     0.3%     0.0%     100.0%
 Fig. 7: Possible translations of the C program (Version B)                                - buffer    16.4%     99.0%     1.0%     0.0%     100.0%
                                                                                           - poly.      0.8%     100.0%    0.0%     0.0%     100.0%



disentangles the lifetime of two immutable pointers referring                      global data (4.4%). Among borrowed references, 11.6% are
to an object by making a copy of it with the same value.                           mutable references, and 39.2% are immutable references.
How often are the above strategies used? Elision is the most
frequently used specialization strategy when translating code                      Spatial and Temporal Safety of References. All the refer-
fragments involving aliasing references. We find that it is used                   ences in safe Rust are strongly typed so that the Rust compiler
in 25 final translations. Cloning is used in 13 translations.                      can enforce certain safety invariants when using those types.
                                                                                   For temporal safety guarantees, most of the owning references
 Rust translations provided by users choose specialized                            (95.6%) and borrowing references (99.7%) are compile-time
 strategies to satisfy static Rust safety rules, rather than resort                checked, which are statically proven to be free of temporal
 to dynamic references (ref-counted), to handle aliasing.                          memory errors. This includes almost all of the stack and heap
                                                                                   data references. The remaining are dynamic references, which
                                                                                   involve either partial or full dynamic checks. Typical types
    V.    Security and Performance of User Translations                            in the translations include OnceCell<T> (runtime check on
    One of the most important motivations for translating C to                     the first write) and Mutex<T> (check on every code region
Rust is to guarantee full memory safety without sacrificing                        of access). Most of the dynamic references are for global
performance. Some Rust safety abstractions are completely                          variables. For spatial safety, most references used (90.9%) may
static, thereby having zero runtime costs, while others employ                     require runtime checks on access.
runtime checks. We analyze the usage of Rust abstractions in
the translations obtained in our study to understand how often                         Two sub-categories of references, i.e., nullable references
zero-cost safety abstractions are used. We then measure end-                       (8.3%) and references to dynamically-sized types (79.7%), af-
to-end performance of the Rust translations. We also highlight                     fect abort handling and performance and are worth mentioning.
prominent examples of code patterns known to be dangerous                          Nullable References. Nullable references are typically rep-
in C. These are forbidden in safe Rust, and we explain how                         resented by Option<T> , which piggybacks on static type
they were translated to safe Rust code by our participants.                        safety to separate the case where a reference is NULL from
                                                                                   when it is not. It is often a zero-cost abstraction when T
A. Breakdown of Safe Abstractions Used                                             is a non-null reference, while preventing ungraceful aborts.
    Rust offers smart references (pointers) and safe data type                     Usage of nullable references forces the developer to specify
abstractions which can replace raw pointers in C. We analyze                       how the code should handle null pointer deference, preventing
(1) how often the Rust translations use those data type abstrac-                   the software from aborting ungracefully when memory safety
tions that encapsulate pointers, and (2) whether the memory                        is violated. If the user does not want to specify how such
safety properties on those types are enforced at compile time                      exceptions should be handled, Rust gives a default way in
(statically) or run time (dynamically).                                            which the compiler inserts null checks. They result in runtime
                                                                                   panic on safety-violating inputs. It is explicitly reflected in the
Breakdown of Different Types of References. Table III                              syntax (e.g., unwrap(..) ). In the user translations, 63.1%
summarizes the different types of smart references and data                        of the accesses use such default null checks that may cause
types that our users used, along with their frequency of usage.                    runtime panic on null pointer access, while the other 37% use
There are 1261 explicitly declared reference-like variables                        of Option<T> are panic-free (not raising runtime aborts).
in the 31 final Rust translations in total. Those variables
can be classified into either owning references (49.2%)5 or                        Dynamically Sized Types. Dynamically sized types (DSTs)
borrowing references (50.8%). The owning references consist                        are useful to support strings, buffers, as well as runtime
of references of stack data (14.2%), heap data (31.4%), and                        polymorphism (e.g., Box<dyn T> ) [4]. References of DSTs
                                                                                   are typically “fat” pointers that store additional information
  5 We consider smart pointers (e.g., String and Vec ) as owning references.       to facilitates dynamic checks for spatial safety. In our Rust

                                                                               7
  translations, 79.7% of the variables are DST references.6                                                                                 with the highest test coverage as the main comparison baseline,
                                                                                                                                            tie-breaking in favor of the shorter translation. All the tests
           Temporal safety is achieved mostly statically (95.6%),                                                                           provided by all the participants for the C benchmarks are
           whereas spatial safety is mostly through runtime checks.                                                                         considered when computing the (line) coverage. This gives
                                                                                                                                            us 8 Rust translations, one for each C benchmark.
  Case Studies: Known Vulnerabilities Eliminated. It is
  evident, even in our small-scale user study, that C to Rust                                                                                   We report performance only on test cases for which the
  translation directly addresses the root cause of memory safety                                                                            Rust code and corresponding C have the same output and both
  vulnerabilities, namely insecure coding practices. 2 out of 8                                                                             exit normally8 , thereby eliminating unfair comparisons.
  of our benchmarks, shoco and urlparser, have 3 known
                                                                                                                                                The running time is calculated between the entry and exit
  vulnerabilities in our chosen versions. The data compression
                                                                                                                                            of the main function of the programs to exclude differences
  library shoco has one spatial memory vulnerability (CVE-
                                                                                                                                            in the load and initialization time9 . We report the average over
  2017-11367) on the access of an array called packs . All
                                                                                                                                            70 repeated trials, removing the first 10 rounds, which warm
  users who translated this benchmark eliminated the spatial
                                                                                                                                            up hardware and OS caches, as well as the fastest and slowest
  error and the out-of-bound is caught at runtime. Similarly, a
                                                                                                                                            10 rounds of the remaining. The ratio of running time Rust
  heap-buffer overflow on a string buffer in urlparser is caught
                                                                                                                                            compared to the corresponding C is given in Fig. 8. We have
  at runtime as well. The C char* pointers pointing to the string
                                                                                                                                            that for 5 out of the 8 C benchmarks, their most similar Rust
  are lifted into String, &str , or &String with spatial safety
                                                                                                                                            translations run faster. 6 out of 8 have corresponding Rust
  guarantees. For temporal safety, there is a use-after-free (UAF)
                                                                                                                                            translations well below 10% overheads, while the remaining 2
  vulnerability 7 in the urlparser C program when the input
                                                                                                                                            have about 10% and 40% overhead at -O3 optimization level.
  string to the parser does not live long enough before calling
  certain library APIs such as url_data_inspect. This bug is                                                                                  It is worth noting that our performance analysis is post-hoc.
  statically eliminated as the lifetime and borrowing rules in Rust                                                                         We did not ask users to measure or optimize for performance.
  forbid such code patterns. All participants created a copy of                                                                             We only specified correctness and safety as the objectives.
  the borrowed input string that needed to live longer than the
  original, thereby eliminating the vulnerable pattern in the C                                                                              For Rust translations most similar to the original C code,
  code. More details on the case studies are in the Appendix A.                                                                              the overhead is mostly within 20% and Rust is often faster.

           All the known memory safety vulnerabilities in C programs                                                                        C. Examples of Security-Enhancing Code Patterns
           are eliminated in each one of the Rust translations.
                                                                                                                                               Certain code patterns in C are considered unsafe and
  B. Performance Comparison                                                                                                                 are forbidden in safe Rust. However, there are often safe
                                                                                                                                            abstractions in Rust designed to achieve similar goals at low
                       2.0                                                                 2.0                                              cost. We focus on two kinds of patterns present in our C
Normalized Time Cost




                                                                    Normalized Time Cost




                       1.8                                                                 1.8                                              programs, including mutable globals and unions, to analyze
                       1.6                                                                 1.6
                       1.4                                                                 1.4                                              how users translate such code patterns into safe Rust.
                       1.2                                                                 1.2
                       1.0                                                                 1.0                                              Mutable Globals. Mutable global variables in C are prone to
                       0.8                                                                 0.8
                       0.6                                                                 0.6                                              be corrupted and exploited in real-world attacks due to their
                       0.4                                                                 0.4
                       0.2                                                                 0.2                                              extensive lifetime across many functions and relatively pre-
                       0.0                                                                 0.0                                              dictable address [35], [37]. Besides being a convenient target
                                lit r t in tf o st             er                                   lit r t in tf o st             er
                             csp exp fm jo prin shoc te rlpars                                   csp exp fm jo prin shoc te rlpars          for attackers, mutable globals are also sources of various hard-
                                                       u                                                                   u
                                                                                                                                            to-find temporal memory errors, and are thus discouraged by
                             (a) Compiled with -O2                                               (b) Compiled with -O3                      various coding guidelines [1], [5], [7]. Safe Rust forbids plain
                                                                                                                                            mutable globals because they violate the AXM principle even
  Fig. 8: Running time of the most similar Rust translation                                                                                 in single-threaded programs. Otherwise, different call frames
  compared to the original C at different optimization levels.                                                                              can obtain mutable references to globals with overlapping
  The time for the baseline C (dashed line) is normalized to 1.                                                                             lifetimes, leading to memory errors and incorrect optimizations
                                                                                                                                            in Rust. To translate C code using globals into safe Rust,
                                                                                                                                            we see that users devised several strategies using safe Rust
      We now turn to a comparison of performance overheads                                                                                  abstractions, which are listed below:
  introduced when one migrates the same C code to Rust. An
  issue here is that our user-provided translations do not have                                                                              A) From global to locals. A performant strategy is to identify
  the exact same behavior as the original C code on all inputs.                                                                                 where the global is used first and last in the program.
  Furthermore, there are multiple candidate translations for each                                                                               Then, one can replace the original global variable with a
  of 8 C benchmarks to compare with, each with differences                                                                                      local (stack or heap) object spanning the lifetime of actual
  from the original C code. To deal with these, we choose the                                                                                   use. A reference can be passed into functions that need
  Rust program which is most similar to the corresponding C                                                                                     them. When multiple mutable globals are transformed
  program on tests. Specifically, we select the Rust translation                                                                                this way, they can be grouped into a single struct
                                                                                                                                                object for better performance and to reduce code bloat.
     6 We count String and Vec as “references” to dynamically-sized types as                                                                    One reference to the grouped struct object with the
  well, even though those smart pointers themselves have fixed size.
     7 The fix commit changed the ownership from borrowing (line 100 of the                                                                   8 We do not measure performance on unit tests for error handling.

  left side) to owning (line 188-192 of the right side) in url.c .                                                                            9 We also measure end-to-end performance. Details are in the Appendix C.




                                                                                                                                        8
    original globals as fields at different offsets is sufficient.                                             all fail             2 fail                               1 fail              no fail
                                                                                              1.0                                                                1.0
    This optimizes for performance as it lowers the cost of




                                                                          Fraction of Tests




                                                                                                                                             Fraction of Tests
    parameter passing by reference for many moved globals                                     0.8                                                                0.8
    with similar lifetimes of use in the original C code.                                     0.6                                                                0.6
 B) Dynamic references. The fallback strategy is to create dy-                                0.4                                                                0.4
    namic references, declared either as thread locals or true                                0.2                                                                0.2
    globals in Rust. For thread-local variables, single-thread                                0.0                                                                0.0
    synchronization (e.g., RefCell) is still needed [11], but                                           co est oin xpr plit mt intf ser                                    co est ser mt plit oin intf xpr
                                                                                                     sho t j e cs f pr rlpar                                            sho t rlpar f cs j pr e
    multi-thread synchronization (e.g., Mutex) is not neces-                                                                      u                                              u
                                                                                                    all fail      2 fail   1 fail      no fail                         all fail     2 fail       1 fail      no fail
    sary. Such references incur some runtime costs.                                             (a) Greybox fuzzing tests                                              (b) User-provided tests
 C) Atomic integer types. For mutable global variables that are
    integers, dynamic references are not needed if declaring                  Fig. 9: Rust translations of the same C program all fail on a
    them as Atomic . For Atomic types, special APIs can                       large fraction of fuzz tests (Subfig (a)) and all pass on a large
    mutate their values without mutable references to them.                   fraction of user-provided tests (Subfig(b)).
   19 participants chose to move the globals to locally refer-
enced objects. 11 of them also grouped multiple globals into
an aggregate struct object. 3 users kept mutable globals as                   the original C program and reported that their final Rust trans-
globals or thread-local variables through dynamic references.                 lations passed their tests. We analyze how many behavioral
4 used atomics for mutable globals.                                           differences are missed by tests self-created by participants.
C Unions. Unions in C allow overlapping objects of incompat-                      We employ automated fuzz-testing to check for behavioral
ible types. However, programmers are responsible for ensuring                 differences between Rust and the corresponding C source. We
that operations on unions are type safe. Otherwise, type safety               use AFL++ [26] to generate tests for each of the 8 C programs
violations can lead to both spatial and temporal memory                       for 1 hour per program. We then sample 300 distinct tests
errors [21]. In safe Rust, unions are not allowed, but various                per program, except for programs with less than 300 tests
abstractions can be used to achieve similar functionality. 2                  available, in which case we took all tests10 . On these tests, we
of the 8 C programs in our benchmarks use unions. Users                       compare each of the 31 Rust programs to its corresponding C
translated C unions depending on different use cases:                         program. We omit minor non-semantic discrepancies such as
                                                                              the error message format when computing the difference.
 A) Zero-cost type casting (type punning [12]). The string
    compression library shoco uses union to access integers                       We find that none of the 31 translations is fully equivalent
    as raw bytes. Its behavior depends on the endianness of                   to the original C code. Fig. 9 shows that 37%-100% (68% on
    the target architecture. Some users translate such code                   average) of the fuzz tests exhibit a discrepancy across different
    into safe Rust API calls (to(from)_le(be)_bytes ) that                    Rust translations of the same C program.
    convert between primitives and constant-size byte arrays.
                                                                              Many translations fail the same way. Given that all the trans-
    Note that the conversion is zero-cost since those APIs
                                                                              lations have behavioral differences from the corresponding C
    will be optimized away during compilation. They can also
                                                                              code, we examine whether their failures are correlated. We
    be used together with conditional compilation supported
                                                                              count how many translations for the same C program fail on
    in safe Rust to match the endianness of the architecture.
                                                                              the same test case. Fig. 9 shows that nearly all Rust translations
    Please see Fig. 21 in the Appendix D for examples.
                                                                              fail on about the same 38% tests on shoco, the same 50%
 B) Sum type (variant record). Another C program expr uses
                                                                              on test, and so on. We investigated some of the tests that
    unions to implement variant records (sum types). For such
                                                                              all translations failed, finding that they are often corner cases
    use cases, some users translate them into enum and access
                                                                              involving C library calls that are tedious to emulate in safe
    them using statically-checked match statements. Rust
                                                                              Rust, and hence missed by all translations. An illustrative
    enum is memory efficient, and the memory occupied by a
                                                                              example is provided in the Appendix B for interested readers.
    Rust enum depends on its largest discriminant, similar to
    unions in C. An example (Fig. 22) is in the Appendix D.                   Breakdown of Behavioral Differences. The behavioral dif-
                                                                              ferences can be classified into three categories, including:
For relevant use cases of unions, 3 users used zero-cost type
casting APIs in safe Rust, and 2 users used Rust enums.                             A) I/O encoding/decoding errors. Standard Rust APIs have
Another 3 users did not use those abstractions but emulated                            different I/O formatting and encoding behavior from
the C unions using structs and methods with higher overhead.                           similar C APIs. For example, the input arguments and
                                                                                       string APIs often assume UTF-8 encoding, which might
 Users often translate known unsafe C code patterns to                                 abort the program if the string buffer is not valid UTF-8.
 equivalent statically-checked low-cost safe Rust code.                             B) Runtime safety aborts. The Rust has runtime checks about
                                                                                       spatial errors and null pointer dereferences that safely
                                                                                       abort, while C may continue arbitrarily and crash.
           VI.   The Gap In Functional Correctness                                  C) Logical differences. Both C and Rust can finish the
                                                                                       execution and normally exit, but the output is different.
    As mentioned in Section III, each participant submitted
their final translation and tested it with test cases they created.              10 3 programs had fewer than 300 tests: shoco (200 tests), csplit (211
Most participants created tests that covered more than 85% of                 tests), and urlparser (22 tests)


                                                                      9
   urlparser-1
   urlparser-2
   urlparser-3
                                                                            None of the Rust translations is fully equivalent to the
   urlparser-4
   urlparser-5                                                              corresponding C, but some differences are due to Rust pro-
      shoco-1
      shoco-2
      shoco-3
                                                                            grammers handling safety aborts differently. Several logical
      shoco-4
      shoco-5
      shoco-6
                                                                            differences and incompatibilities in the external I/O remain.
         fmt-1
         fmt-2
         fmt-3
         fmt-4
      csplit-1
                                                                                VII.    Efficacy of State-of-the-art Automatic Tools
      csplit-2
      csplit-3
      csplit-4
      csplit-5                                                                 We evaluate 4 state-of-the-art C to Rust translation tools
        join-1
        join-2                                                             on our C benchmarks to analyze whether their approach is
      printf-1
      printf-2
      printf-3
                                                                           effective and, when not, where the immediate gaps are.
       expr-1
       expr-2
        test-1
        test-2
                                                                           A. Compiler-based Tools
        test-3
        test-4
                                                                               Both Laertes and Crown are compiler-based systems that
                 0     20          40          60          80   100
                                                                           post-process the unsafe Rust code produced by the c2rust
                       (percentage of fuzzer-generated tests)              compiler [33]. Our results, shown in Table IV, confirm that
Fig. 10: Behavioral differences across 31 translations with tests          while both tools can often produce Rust programs that compile,
from greybox fuzzing. Legends from left to right mean “equiv-              the generated code is still largely unsafe and far from safe Rust.
alent behaviors” (green), “I/O enc. errors” (gray), “Runtime               We summarize their missing features next.
safety aborts” (brown), and “Logical differences” (red).                       Fraction of Raw Pointers. The fraction of raw pointers that
                                                                           can be lifted by Laertes and Crown is limited. For Laertes,
                                                                           Most of the data references (95.3% on average) are still unsafe
                                                                           raw pointers12 . For Crown, the majority of the references are
Fig. 10 shows the distribution of category of differences for              also raw pointers, and safe Rust references account for less
each of the 31 translations. Nearly all translations (27/31)               than 3.1% averaged over all the benchmarks.
behave differently on more than half of the newly created tests
from fuzzing. Logical differences (category C) exist across all                Lifted Safe Rust Data Types. Both of the translation tools
translations, highlighting the gap in functional equivalence. I/O          have limited support for higher-level data types. Both Laertes
encoding/decoding errors (category A) are frequent in general,             and Crown are limited to three types of Rust references that
while safety-violating inputs (category B) are more frequent in            are closely related to C pointers. The three types include
translations of shoco and urlparser. Note that Category B                  Option<&T> (similar to const T* in C), Option<&mut T>
cases do not lead to undefined behavior in Rust due to runtime             (similar to T* ), and Option<Box<T>> (owning T* ) where
safety checks, but exhibit behavioral differences to C. These              T is a C-compatible type. Most of the higher-level smart
differences are to be expected—Rust is eliminating potentially             references that participants frequently use are out of the scopes
unsafe (undefined) behavior from untamed C code.                           of those tools, including String , &str , Vec<T>, BufRead ,
                                                                           and so on, which are shown in Fig. 4.
    Differences in I/O. Although the gap between the trans-
lations and full functional equivalence is non-negligible and                  Handling of C Library Calls. C library calls turn into FFI
common, we find that some of the differences may not matter                calls from Rust to C in the translation of both Laertes and
for many intended usage scenarios. One example is that the                 Crown. C library functions generally do not have direct safe
differences in I/O encoding/decoding behaviors are a major                 Rust mappings, and the translation is often not straightforward.
source of behavioral differences, as shown in the gray bars in             Calling C functions through FFI is easy, but such handling of
Fig. 10. Such differences may not matter if the intended inputs            library calls permits unsafety. Such operations are only allowed
to the programs are valid UTF-8 strings. The UTF-8 encoding                in unsafe Rust. At the same time, C APIs often require raw
is widely assumed in the Rust standard library on string-                  pointers as parameters, which may also constrain related Rust
related APIs. Those APIs provide convenient ways to work                   code to operate on raw pointers. In contrast, users in our study
with UTF-8 encoded strings compared with other encodings.                  addressed the API translation problem by utilizing safe Rust
If the intended use case requires processing other encodings,              code in creative ways, as shown previously in Fig. 5.
the same data types and APIs may no longer be useful.                          Dealing with Aliasing and Lifetimes. Aliasing references
Rewriting of related API functions or external emulation would             in Rust can frequently violate borrowing rules and thus can
be necessary, leading to a more verbose translation.                       be challenging to translate. Laertes and Crown aim to lift
    Panic-free Translations. 7 out of 8 C benchmarks have at               pointers to references while preserving the low-level control
least one user-provided Rust translation that is panic-free11 .            flow and data flow of the C program. The strategies highlighted
The urlparser benchmark is an example where we have                        in our work, for instance in Section IV-B, are not used by these
2 translations that do not have any runtime safety aborts                  tools. These prior tools do not aim to eliminate unsafe C code
(brown bar in Fig. 10), while the remaining 3 translations have            patterns such as mutable globals or unions that may be present
panics. On the contrary, the 2 panic-free translations avoid all           in the c2rust compiler output used as their first stage.
use of Option<T>::unwrap(). These differences across Rust                      Memory Safety. The end result of the code produced from
translations are only artifacts of how different users handle              prior compiler-based tools might be safer than C, but is not
safety aborts, arising out of undefined behavior in C.                     guaranteed to have full memory safety. Recall that there are 3
  11 Excluding the abort due to I/O encoding/decoding errors.                12 Excluding data references in helper functions injected by Laertes.




                                                                      10
                                       TABLE IV: Comparison of Existing Tools on Our Benchmarks
         Tools
                             Laertes                              Crown                               Flourine                             Vert
 Prog.
                           Safe Code (%)    Passed             Safe Code (%)     Passed             Safe Code (%)    Passed             Safe Code (%)    Passed
                 Compile                             Compile                              Compile                             Compile
                           #Line   #Ref.    Tests              #Line    #Ref.    Tests              #Line    #Ref.   Tests              #Line    #Ref.   Tests
 csplit            ✓       1.3%     3.2%    100%       ✓       1.8%     3.2%     100%        ✗      100%     100%      -        ✗       97.2% 100%         -
 expr              ✓       1.3%     5.0%    95.3%      ✗       1.8%     2.5%       -         ✗      85.3% 100%         -        ✗       98.8% 93.1%        -
 fmt               ✗       1.2%     3.0%      -        ✓       1.8%     3.0%     100%        ✗      73.1% 100%         -        ✗       60.1% 100%         -
 join              ✓       0.9%    14.3%    100%       ✗       1.4%     2.4%       -         ✗      74.3% 100%         -        ✗       94.3% 100%         -
 printf            ✓       1.4%     3.0%    100%       ✓       2.1%     3.0%     100%        ✗      77.1% 100%         -        ✗       95.9% 100%         -
 test              ✓       1.0%     9.5%    100%       ✓       1.6%     9.5%     100%        ✗      81.8% 88.2%        -        ✗       62.9% 84.6%        -
 shoco             ✓       1.2%      0%     100%       ✓       0.3%      0%      100%        ✗      96.3% 100%         -        ✗       99.4% 100%         -
 urlparser         ✓        0%       0%     100%       ✓       0.2%     1.3%     100%        ✗      100%     100%      -        ✗       84.1% 78.6%        -



known vulnerabilities in our C benchmarks. The translation                           each can be independently translated and tested, since present
resulting from these tools eliminates 1 of these vulnerabilities,                    LLMs work reasonably well on small code fragments.
a read overflow of a global array, as shown in Fig. 11 in
the Appendix A. The original global array declaration in                                 The decomposition of C programs into such components
C is syntactically translated into an equivalent global array                        and merging of their Rust translations are not automated by
declaration in Rust. Access to such an array (rather than                            the tools. We encountered many difficulties when trying to em-
via a raw pointer) is bounds-checked automatically in Rust.                          ulate the decomposition strategies described in their respective
The remaining 2 vulnerabilities persist in the Rust translation                      works. These difficulties point to a broader technical challenge
produced by both these tools, one of which is a spatial violation                    that may be of independent interest for further research.
and the other temporal. Raw C pointers (not integers) are                                Decomposition Failures. 6 out of 8 of our C benchmarks
involved in the unsafe code in the 2 cases, and Laertes and                          are real-world standalone programs, and the remaining 2 are
Crown are not yet able to lift them to safe Rust references.                         libraries. Functions in standalone programs are connected by a
                                                                                     call graph. We find it difficult to decompose such functions into
 State-of-the-art compiler-based C to Rust tools output trans-
                                                                                     independently testable modules using the strategies described
 lations that extensively use unsafe Rust while rigidly retain-
                                                                                     in the works of Flourine or Vert. For example, if a function
 ing many structural similarities to the original C code.
                                                                                      f calls g, then the component containing f is required to
                                                                                     contain g since it is a dependency. This implies that on our
B. LLM-based Tools                                                                   standalone C program benchmarks, the function main depends
                                                                                     on all other functions and the component containing it includes
    There are 2 recent tools, Flourine and Vert, that are state-                     nearly the whole program, making it too large to obtain
of-the-art for C to Rust translation utilizing large language                        repairable translations from LLMs. The 2 library benchmarks
models (LLMs). We report on our experience in running them                           are marginally better since there is no main function, but the
on our 8 benchmark programs. Flourine explores 4 test-driven                         challenge persists in part here as well.
repair strategies in concert with LLMs. Vert uses a different
approach. It creates two translations of the given C program,                            We note that the decomposition strategy proposed in
one is unsafe Rust decompiled from WASM, and the other is                            Flourine or Vert can produce multiple translations of the same
an LLM-generated safe Rust code. Then, it uses fuzzing and,                          function that are inconsistent and cannot be merged into one.
if needed, model-checking techniques to find tests that exhibit                      Say we have two components, one containing function { f, g}
differences and subsequently run an automatic repair. The work                       and another containing function {h, g}. The two components are
on Vert claims that if their tool terminates normally, the                           translated independently and thus multiple Rust translations
resulting translation is expected to be functionally equivalent                      of the function g are obtained. We often find that these
to the C code. For evaluating Flourine, we choose their most                         translations have conflicting type definitions and incompatible
stable configuration with GPT-413 as the LLM backend. For                            types that are difficult to merge into a single translation.
evaluating Vert, we use Claude14 , which is reported to be the                           We are not aware of better ways to decompose our C
best-performing LLM backend for their artifact.                                      programs in components small enough to feed to Flourine
    We observe that code generated from these LLM-based                              or Vert. We fed the whole program to these tools and the
tools is more idiomatic and uses safe Rust abstractions more                         translated Rust code does not compile. We then experimented
often than compiler-based tools, and thus can serve the goal of                      with several versions manually to best split each function in a
useful translation aids for human developers on code snippets.                       separate component, while including only a minimal number of
However, neither tool generates a runnable translation for any                       dependencies, such that the size of component is small enough
of the C programs we consider, as shown in Table IV. This is                         to work with LLMs. We are able to produce Rust translations
because both tools have certain structural assumptions on the C                      reported in Table IV with some compilable components, but
code given to them as input. Specifically, both tools expect that                    unable to merge them back into a single compilable program.
the C program can be decomposed into components such that
                                                                                      State-of-the-art LLM-based C to Rust translators produce
  13 We use the model version gpt-4-0125.                                             idiomatic safe Rust snippets, but not safe Rust programs
  14 We use Claude 3.5 (claude-3-5-sonnet-20240620), which is the best                that compile. Existing tools share a common challenge in
available version of Claude at the time of our evaluation.                            devising workable decomposition strategies for long C code.


                                                                                11
C. Do existing LLMs help in user-provided translation?                             These types bridge the gap between platform-native strings
                                                                                   and Rust Strings and are useful for uutils/coreutils as
    We revisit whether LLMs, taken standalone, are helpful to                      it aims to be cross-platform. Our user study only specified the
users who followed their own translation strategies. Recall that                   requirements that the Rust code should work on Linux.
we placed no restrictions on the participants to employ external
tools. We asked our participants to specify which tools they                       Library API Calls. Recall that in our user study, users
used and provide qualitative feedback on their experience. In                      translate many C library API calls using various strategies
their feedback, 31 of the 33 participants reported that they tried                 listed in Fig. 5. We also investigate how library API calls in
to use LLMs for assistance. 14 users mentioned that LLMs are                       GNU C coreutils are expressed in the uutils programs. Due
helpful indirectly in the translation process, including tasks                     to a large number of library API calls (561 in total) and large
such as explaining the C code and suggesting Rust data types                       program dissimilarity, we focus on the top 10 frequently used
and APIs. However, most of the participants (20/31) reported                       APIs that covered 53% of all the API calls. We manually look
that the code generated by LLMs is error-prone and hard to                         into at least 5 call sites per API and check Rust code fragments
debug. 2 users reported that they abandoned LLMs for direct                        that implement corresponding functionalities. Most API calls
code translation and translated manually from scratch.                             in C can be mapped to safe Rust API calls and expressions.
                                                                                   Third-party crates are used for some APIs. One example is
     VIII.    Extensibility of Findings to Real-world Code                         the quote C API that handles special characters. The Rust
                                                                                   program implements the same functionality using quote API
    To test whether our findings generalize beyond our chosen                      provided by the Rust crate os_display . We find no API calls
programs or our user group, we conduct a post-hoc analysis                         handled using the API emulation strategy, however.
of a mature open-source Rust project uutils/coreutils 15
                                                                                   Dealing with Aliasing. Recall that users in our study use
(uutils), which mirrors the GNU coreutils written in C. The
                                                                                   strategies including (A) reference elision and (B) cloning to
uutils project aims for compatibility with GNU coreutils and
                                                                                   deal with aliasing (Section IV-B). For the uutils programs,
passing the same GNU test suite. The uutils Rust repository
                                                                                   we find C code locations involving aliasing pointers and then
has 17.6k Github stars and 5 of its most active contributors
                                                                                   check how a similar functionality is implemented in Rust. Due
have Rust experience of more than 2 years at the time of
                                                                                   to large dissimilarities from the C source, we manually check
this writing. We examine 6 uutils Rust programs that share
                                                                                   around 20 places in C and find 4 with clear matching code
names and functionality with the 6 BSDCoreUtils programs
                                                                                   fragments in Rust. Those code fragments are all examples of
in our benchmarks. Similar to our user study, we compare
                                                                                   reference elision, and one worth mentioning is the mapping of
those Rust programs to their C counterparts in GNU coreutils.
                                                                                   a linked list in C to a Vec in Rust in the csplit program. Such
Program Dissimilarity. Recall that the Rust translations in our                    type lifting eliminates code blocks with aliasing pointers that
user study are dissimilar from the C source (Sec. IV-A). We                        manipulate linked lists. We also find many instances of object
find that a larger dissimilarity between the structure of uutils                   cloning in Rust uutils to satisfy ownership constraints when
Rust programs and their corresponding GNU C programs                               calling functions. But none are specifically used for handling
compared with our user study is observed. We manually                              aliased references as was done in our user study.
checked 142 and 165 C and Rust functions, respectively, across                     Functional Equivalence. In Section VI, we reported that
the 6 programs. We were only able to find 9 pairs of functions                     user translations are not fully equivalent to the C source
semantically similar, and they were all relatively small.16                        and multiple differences are exposed by differential fuzzing.
Security-Enhancing Code Patterns. The code patterns in-                            The phenomenon is observed in the uutils project, which
volving mutable globals and unions in C are changed in Rust                        currently passes around 80% of the GNU test suite. We find
programs in our user study (Sec. V-C). It is the same for the                      that for 5 of the 6 uutils programs we investigated, there
uutils project. The original GNU C programs also have many                         are known correctness gaps with GNU Coreutils when using
global variables (on average 13.2 globals per program), and the                    its test results, as reported in the uutils repository17 . One
corresponding Rust programs in uutils avoid global variables                       program, test, seems to be close to functional equivalence
almost completely. These Rust programs group variables into                        since it passes the full GNU test suite. We further compare the
struct-typed objects (strategy A for globals in Sec. V-C),                         Rust version of test to the GNU C version using differential
more often than in our study. One program expr, which                              fuzzing in a setup similar to Section VI. Among 300 fuzzer-
involves unions in C, is implemented with Enum s in safe Rust.                     generated tests sampled, we find 50.6% test cases exhibit
                                                                                   different behaviors. With a deeper investigation, we find that at
Semantic Data Type Lifting. In our study, users lift raw point-                    least 23.6% of the tests reveal non-trivial logical differences.
ers into various safe Rust data types, as shown previously in                      More specifically, C and Rust programs have different results
Fig. 4. We find that Rust data types used in uutils programs                       (i.e., return code) on 2.3% tests and semantically different error
are similar to the types seen in this study. 83% of the data types                 messages on 21.3% tests. We observe no I/O encoding errors
in uutils programs also exist in translations by our users.                        or runtime safety aborts. We also find that the maintainers are
The most frequent Rust types in uutils programs are string-                        aware of several semantic differences that need to be fixed
related types such as String (18%), &str (14%), OsString                           according to comments in their additional test file.
(6%), and OsStr (4%). One difference is that OsString
and OsStr types do not exist in translations by our users.                         Use of Unsafe Rust. Among the 6 Rust programs, only
                                                                                   one program (test) has one line of unsafe Rust to call
  15 We download a version on Sept. 26th, 2024 with commit hash a0d258d.           libc::isatty . This C library call checks if the open file
   16 Such large dissimilarity may be due to the fact that uutils/coreutils
is re-implemented in Rust from scratch to avoid license issues.                      17 According to their gnu-full-result.json of commit a0d258d.




                                                                              12
descriptor is a terminal. It can perhaps be replaced with safe            (1) Refactoring Global Variables Through Lifetime and Def-
Rust APIs in third-party crates, such as atty or termion .                Use Analysis. Use of mutable globals differentiates C and safe
                                                                          Rust programs. As observed in our user study, many globals
 Most of the findings in our user study are also applicable to            are accessed within a thread and can be moved to the heap or
 a Rust project mirroring GNU Coreutils written by experts.               stack, possibly in grouped struct -typed objects for efficiency.
                                                                          Precise analysis of lifetime of globals is a promising next step.
                IX.   Discussion and Takeaways                            (2) Lifting Data Types Semantically Before Lifting References.
                                                                          Data type analysis directly impacts how references are lifted
    Our analysis of user-provided translations highlights sev-            to Rust. Code blocks and pointers in C can often be elided
eral points where automatic translation strategies deviate from           after type lifting, which is observed from both translations by
those taken by human users. We reflect on why there is such               our users and in our extensibility analysis on public code(e.g.,
a gap and summarize takeaways for automatic translation.                  Linked list pointer manipulations to Vec API calls). LLMs can
Separate Policy from Mechanism. Our observation is that                   be useful for pattern recognition tasks, according to qualitative
there are many choices to be considered when translating a                feedback received from our users, and it would be promising
C program to Rust, i.e., there is no one-size-fits-all strategy           to use them for type mapping suggestions of C objects to Rust.
to take. The resulting translations, while satisfying memory              (3) Lifting Unions. Automatic analysis to (a) tell apart different
safety, can have varying levels of functional correctness, per-           use cases of C unions and (b) associate tag values with valid
formance, and grace in handling runtime safety exceptions.                fields for variant records can help convert unions to enums.
The balance between them is a matter of policy. For example,              Threats to Validity. Our user study is with a relatively small
the level of functional equivalence to achieve is one crucial             number of users and on relatively small programs. These
policy decision. Full functional equivalence can require sig-             present limits are an artifact of time constraints and the
nificant effort and may even go against the purpose of code               inherent difficulty of the task at hand for users who have
migration [55]. To characterize what behaviors must be kept               limited prior experience with Rust. We point out that Rust has
and what behaviors can change in the translation, we may                  a relatively new developer community. A survey by JetBrains
need more thorough unit tests or other forms of specifications.           in 2023 involving over 26k developers worldwide reports the
Another example of an important policy decision is about the              majority of Rust developers (56%) have less than 6 months
data types and APIs to use, which can lead to multiple ways               of experience [3]. To partially assess which of our findings
of translating the same program with different trade-offs in              extend to code written by more experienced developers, we
performance, memory overhead, compatibility, and so on. In                reported on our post-hoc analysis on more mature real-world
summary, users may want explicit control over policy decisions            Rust programs mirroring GNU C coreutils in Section VIII.
even when using automatic tools.                                          Most of the key findings we highlight extend beyond our users.
Improving LLM-based Search for Translations. Once policy
decisions are clear, automatic mechanisms can enable search                                     X.   Related Work
for translations. Our observation is that there are several
                                                                              In practice, many motivations for code migration to new
immediate and open problems that, if addressed, can make
                                                                          languages exist, such as legacy code modernization, com-
C to Rust code automatic translator much more usable.
                                                                          patibility improvement with newer platforms, N-versioning
(1) Modeling of Data Types and APIs. So far, few of the                   for fault tolerance, and so on. Memory safety is a unique
previous work explicitly models data types and APIs in the                driver for C to Rust translation. For example, Mozilla Firefox
Rust standard library, such as the ones summarized in Fig. 4.             is actively migrating components written in C/C++ to Rust
We believe it is essential to overcome the language differences           with memory safety as a key consideration [8]. Towards
between C and Rust and move away from unsafe code.                        memory safety as a goal, a long line of memory defenses has
(2) Mergeable Decomposition. Finding the right way to de-                 been investigated. They achieve different trade-offs between
compose programs into smaller components is challenging but               performance, compatibility, and security.
appears necessary for LLMs with limited context windows. At
the same time, decomposition need not be one-shot. It is useful           Memory Safety in C/C++. SoftBound [43] and CETS [44]
to explore if it is possible to incrementally transform identified        are compiler-based solutions that provide full memory safety
components, such that a partial Rust translation can be used              in C. The performance overheads of enforcing full memory
alongside the untranslated part of C.                                     safety in software-based approaches are often reported to be
(3) The Last Mile Problem. Some users reported in their                   higher than 50%. In recent years, specialized hardware features
(optional) qualitative feedback about their experience. 10 users          have emerged to accelerate both spatial [39], [47], [56], [59]
reported that debugging was tedious in locating the root cause            and temporal checks [14], [59], but overheads below 10 − 20%
of certain semantic differences. 6 users mentioned that fixing            for full safety appear elusive. Runtime defenses for spatial
some semantic differences involving library calls (e.g., regex)           safety can be acceptably low [30], but complete temporal
is not easy. 14 users mentioned that LLMs are ineffective in              safety still bears a bulk of the runtime overheads. Languages
directly generating correct long code due to issues like type             like Rust can help developers explicitly manage object life-
inconsistency across functions and multiple inter-related errors.         times in a way that eliminates temporal memory management
4 participants who used LLMs for assistance reported that they            mistakes. In our user study, we see that users make heavy
often needed to restart with clean context to get better output.          use of zero-cost abstractions for temporal safety. Owing to the
                                                                          costs of full memory safety, partial safety defenses have been
Promising Static or Dynamic Analysis. Based on our find-                  investigated and have a rich history [51]. Prominent among
ings, we foresee 3 program analyses as immediately useful:                these are CFI [53], ASLR [52], stack canaries [20], guard

                                                                     13
pages [17], and DEP [54] which have found wide deployments.             research is supported in part by the research funds of the
These defenses have good performance characteristics but do             Crystal Centre at the National University of Singapore and the
not rule out all memory safety errors. For example, exploits            Cisco University Research Program Fund, a corporate advised
that bypass these deployed defenses without violating control-          fund of Silicon Valley Community Foundation.
flow properties [6], [31] are known [13].
    Another approach is based on proactive discovery of bugs
and subsequent automatic repair at the source C code level.                                              References
Greybox fuzzing [26], [29], symbolic execution [16], [48], and           [1]   “C++          core        guidelines.”      [Online].     Available:
their combination [42] for finding security vulnerabilities is                 https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#
an active area of research. Automatic localization of buggy                    i2-avoid-non-const-global-variables
code [32], [49] and generation of suggestions for fixes are              [2]   “A command-line benchmarking tool.” [Online]. Available: https:
being actively explored [28], [50]. This find-and-fix approach                 //github.com/sharkdp/hyperfine
offers a continual process to improve software quality and               [3]   “Developer echosystem 2023: Rust.” [Online]. Available: https:
reduce patching effort once flaws are discovered.                              //www.jetbrains.com/lp/devecosystem-2023/rust/
                                                                         [4]   “Dynamically sized types.” [Online]. Available: https://doc.rust-lang.
Memory Safe Dialects for C. Writing code that is free of                       org/reference/dynamically-sized-types.html
memory safety bugs is a desirable goal. Several works focus on           [5]   “Google c++ style guide: Static and global variables.”
finding language subsets or extensions of C/C++ that are easier                [Online]. Available: https://google.github.io/styleguide/cppguide.html#
to statically analyze and dynamically retrofit safety checks                   Static and Global Variables
than untamed C. CCured explored spatial safety via “fat”                 [6]   “The heartblead bug (cve-2014-0160).” [Online]. Available: https:
pointers and relies on garbage collection for temporal memory                  //heartbleed.com/
safety [46]. Xu et. al achieved temporal memory safety using a           [7]   “Linux kernel coding style.” [Online]. Available: https://www.kernel.
global capability store instead of a garbage collector [57]. Cy-               org/doc/html/next/process/coding-style.html
clone has similar spatial safety mechanisms as CCured but uses           [8]   “Oxidation.” [Online]. Available: https://wiki.mozilla.org/Oxidation
memory regions for temporal safety [34]. Flow-sensitive type             [9]   “References    and     borrowing     -   the     rust    programming
qualifier analysis can leverage user-provided type annotations                 language.”   [Online].    Available:   https://doc.rust-lang.org/book/
                                                                               ch04-02-references-and-borrowing.html
for static analysis [27]. More recently, work on the Checked
C language [22] aims to enable mixed legacy C pointers                  [10]   “Thread local storage (rust).” [Online]. Available: https://doc.rust-lang.
                                                                               org/src/std/thread/local.rs.html#37
with safe ones for incremental migration, by allowing parts
                                                                        [11]   “Thread local storage (rust standard library).” [Online]. Available:
of the code to be type-annotated and proven safe. However,                     https://doc.rust-lang.org/src/std/thread/local.rs.html
it does not provide full memory safety. Efforts to dispatch
                                                                        [12]   “Type punning.” [Online]. Available: https://en.wikipedia.org/wiki/
more spatial safety statically at compile-time are underway,                   Type punning
which can further reduce costs of spatial safety [19], [38],            [13]   “”the web/local” boundary is fuzzy: A security study of chrome’s
[40]. There are also efforts to introduce temporal safety into                 process-based sandboxing,” Proceedings of the 2016 ACM SIGSAC
Checked C with runtime overheads of about 30% or more [61].                    Conference on Computer and Communications Security, 2016. [Online].
Overall, while designing safe C dialects continues to be a                     Available: https://api.semanticscholar.org/CorpusID:7573477
promising endeavor, low-overhead designs that eliminate all             [14]   “Arm MTE architecture: Enhancing memory safety,” 8 2019.
memory safety bugs have yet to be found.                                       [Online]. Available: https://community.arm.com/arm-community-blogs/
                                                                               b/architectures-and-processors-blog/posts/enhancing-memory-safety
Translating C to Rust. Safe Rust abstractions force develop-            [15]   “Lost in Translation: A Study of Bugs Introduced by Large Language
ers to move away from raw C pointers. The abstractions offered                 Models while Translating Code,” Jan. 2024, arXiv:2308.03109 [cs].
by safe Rust—lifetime [9], ownership [18], and the AXM                         [Online]. Available: http://arxiv.org/abs/2308.03109
principle [9]—force a significant departure from untamed C              [16]   C. Cadar, D. Dunbar, and D. R. Engler, “Klee: Unassisted and automatic
or C dialects in how programmers write code. In the previous                   generation of high-coverage tests for complex systems programs,” in
                                                                               USENIX Symposium on Operating Systems Design and Implementation,
sections, we have compared various previous work [24], [25],                   2008. [Online]. Available: https://api.semanticscholar.org/CorpusID:
[58], [60], and scalable solution is still an open challenge.                  2520229
                                                                        [17]   T. cker Chiueh and F.-H. Hsu, “Rad: a compile-time solution to
                       XI.   Conclusion                                        buffer overflow attacks,” Proceedings 21st International Conference
                                                                               on Distributed Computing Systems, pp. 409–417, 2001. [Online].
    We have presented the lessons learned from a user study                    Available: https://api.semanticscholar.org/CorpusID:32026510
on how users can translate C programs to safe Rust, with good           [18]   D. Clarke, J. Östlund, I. Sergey, and T. Wrigstad, “Ownership types: A
performance and security gains. Our analysis reveals that they                 survey,” in Aliasing in Object-Oriented Programming, 2013. [Online].
share a high-level approach and common specialized strategies                  Available: https://api.semanticscholar.org/CorpusID:15940253
to overcome the challenges that encumber automatic tools.               [19]   J. Condit, M. Harren, Z. Anderson, D. Gay, and G. C. Necula,
Zero-cost abstractions are ubiquitously used, significantly re-                “Dependent types for low-level programming,” in Proceedings of the
                                                                               16th European Symposium on Programming, ser. ESOP’07. Berlin,
ducing the costs of runtime temporal safety checks, which                      Heidelberg: Springer-Verlag, 2007, p. 520–535.
highlights why Rust offers a promising road ahead.
                                                                        [20]   C. Cowan, “Stackguard: Automatic adaptive detection and prevention
                                                                               of buffer-overflow attacks,” in USENIX Security Symposium, 1998.
                      Acknowledgment                                           [Online]. Available: https://api.semanticscholar.org/CorpusID:2358856
                                                                        [21]   G. J. Duck and R. H. C. Yap, “Effectivesan: type and memory
   We thank all the participants in this user study. We also                   error detection using dynamically typed c/c++,” SIGPLAN Not.,
thank the anonymous reviewers and our shepherd for giving                      vol. 53, no. 4, p. 181–195, Jun. 2018. [Online]. Available:
us valuable feedback on an earlier draft of this paper. This                   https://doi.org/10.1145/3296979.3192388


                                                                   14
[22]   A. S. Elliott, A. Ruef, M. W. Hicks, and D. Tarditi, “Checked c: Making           [43]   S. Nagarakatte, J. Zhao, M. M. K. Martin, and S. Zdancewic,
       c safe by extension,” 2018 IEEE Cybersecurity Development (SecDev),                      “Softbound: highly compatible and complete spatial memory safety
       pp. 53–60, 2018. [Online]. Available: https://api.semanticscholar.org/                   for c,” in ACM-SIGPLAN Symposium on Programming Language
       CorpusID:53413266                                                                        Design and Implementation, 2009. [Online]. Available: https://api.
[23]   M. Emre, P. Boyland, A. Parekh, R. Schroeder, K. Dewey, and B. Hard-                     semanticscholar.org/CorpusID:248719
       ekopf, “Aliasing limits on translating c to safe rust,” Proceedings of the        [44]   ——, “Cets: compiler enforced temporal safety for c,” in International
       ACM on Programming Languages, vol. 7, no. OOPSLA1, pp. 551–579,                          Symposium on Mathematical Morphology and Its Application to
       2023.                                                                                    Signal and Image Processing, 2010. [Online]. Available: https:
[24]   M. Emre, R. Schroeder, K. Dewey, and B. Hardekopf, “Translating c                        //api.semanticscholar.org/CorpusID:914358
       to safer rust,” Proceedings of the ACM on Programming Languages,                  [45]   G. C. Necula, J. Condit, M. Harren, S. McPeak, and W. Weimer,
       vol. 5, no. OOPSLA, pp. 1–29, 2021.                                                      “Ccured: Type-safe retrofitting of legacy software,” ACM Transactions
[25]   H. F. Eniser, H. Zhang, C. David, M. Wang, B. Paulsen, J. Dodds, and                     on Programming Languages and Systems (TOPLAS), vol. 27, no. 3, pp.
       D. Kroening, “Towards translating real-world code with llms: A study                     477–526, 2005.
       of translating to rust,” arXiv preprint arXiv:2405.11514, 2024.                   [46]   ——, “Ccured: type-safe retrofitting of legacy software,” ACM Trans.
[26]   A. Fioraldi, D. Maier, H. Eißfeldt, and M. Heuse, “Afl++: combining                      Program. Lang. Syst., vol. 27, pp. 477–526, 2005. [Online]. Available:
       incremental steps of fuzzing research,” in Proceedings of the 14th                       https://api.semanticscholar.org/CorpusID:8303920
       USENIX Conference on Offensive Technologies, ser. WOOT’20. USA:                   [47]   S. Park, S. Lee, W. Xu, H. Moon, and T. Kim, “libmpk: Software
       USENIX Association, 2020.                                                                abstraction for intel memory protection keys (intel {MPK}),” in 2019
[27]   J. S. Foster, T. Terauchi, and A. Aiken, “Flow-sensitive type qualifiers,”               USENIX Annual Technical Conference (USENIX ATC 19), 2019, pp.
       in Proceedings of the ACM SIGPLAN 2002 Conference on Program-                            241–254.
       ming language design and implementation, 2002, pp. 1–12.                          [48]   S. Poeplau and A. Francillon, “Symbolic execution with symcc: Don’t
[28]   X. Gao, Y. Noller, and A. Roychoudhury, “Program repair,” 2022.                          interpret, compile!” in USENIX Security Symposium, 2020. [Online].
       [Online]. Available: https://arxiv.org/abs/2211.12787                                    Available: https://api.semanticscholar.org/CorpusID:221178890
[29]   Google, “Oss-fuzz vulnerabilities github repository,” accessed: July,             [49]   S. Shen, A. Kolluri, Z. Dong, P. Saxena, and A. Roychoudhury,
       2024. [Online]. Available: https://github.com/google/oss-fuzz-vulns                      “Localizing vulnerabilities statistically from one exploit,” in
[30]   F. Gorter, T. Kroes, H. Bos, and C. Giuffrida, “Sticky tags: Efficient and               Proceedings of the 2021 ACM Asia Conference on Computer
       deterministic spatial memory error mitigation using persistent memory                    and Communications Security, ser. ASIA CCS ’21. New York,
       tags,” in 2024 IEEE Symposium on Security and Privacy (SP). IEEE                         NY, USA: Association for Computing Machinery, 2021, p. 537–549.
       Computer Society, 2024, pp. 217–217.                                                     [Online]. Available: https://doi.org/10.1145/3433210.3437528
[31]   H. Hu, S. Shinde, S. Adrian, Z. L. Chua, P. Saxena, and Z. Liang,                 [50]   Y. SONG, X. GAO, W. LI, W.-N. CHIN, and A. ROYCHOUDHURY,
       “Data-oriented programming: On the expressiveness of non-control data                    “Provenfix: Temporal property guided program repair,” 2024.
       attacks,” in 2016 IEEE Symposium on Security and Privacy (SP). IEEE,              [51]   L. Szekeres, M. Payer, T. Wei, and D. Song, “Sok: Eternal war in
       2016, pp. 969–986.                                                                       memory,” in 2013 IEEE Symposium on Security and Privacy. IEEE,
[32]   Z. Huang, D. Lie, G. Tan, and T. Jaeger, “Using safety properties                        2013, pp. 48–62.
       to generate vulnerability patches,” 2019 IEEE Symposium on
                                                                                         [52]   T. P. Team, “Address space layout randomization.” [Online]. Available:
       Security and Privacy (SP), pp. 539–554, 2019. [Online]. Available:
                                                                                                https://pax.grsecurity.net/docs/aslr.txt
       https://api.semanticscholar.org/CorpusID:106401501
[33]   Immunant, “c2rust: Migrate C code to Rust,” https://github.com/                   [53]   C. Tice, T. Roeder, P. Collingbourne, S. Checkoway, Ú. Erlingsson,
       immunant/c2rust, accessed: July 4, 2023.                                                 L. Lozano, and G. Pike, “Enforcing forward-edge control-flow integrity
                                                                                                in gcc & llvm,” in USENIX Security Symposium, 2014. [Online].
[34]   T. Jim, G. Morrisett, D. Grossman, M. W. Hicks, J. Cheney, and                           Available: https://api.semanticscholar.org/CorpusID:6034518
       Y. Wang, “Cyclone: A safe dialect of c,” in USENIX Annual
       Technical Conference, General Track, 2002. [Online]. Available:                   [54]   A. van de Ven and I. Molnar, “Exec shield,” 2004.
       https://api.semanticscholar.org/CorpusID:5958340                                  [55]   C. Verhoef and A. Terekhov, “The realities of language conversions,”
[35]   B. Johannesmeyer, A. Slowinska, H. Bos, and C. Giuffrida, “Practical                     IEEE Software, vol. 17, no. 6, pp. 111–124, Dec. 2000. [Online].
       {Data-Only} attack generation,” in 33rd USENIX Security Symposium                        Available: http://ieeexplore.ieee.org/document/895180/
       (USENIX Security 24), 2024, pp. 1401–1418.                                        [56]   R. N. M. Watson, J. Woodruff, P. G. Neumann, S. W. Moore,
[36]   R. Jung, J.-H. Jourdan, R. Krebbers, and D. Dreyer, “Rustbelt: Securing                  J. Anderson, D. Chisnall, N. H. Dave, B. Davis, K. Gudka,
       the foundations of the rust programming language,” Proceedings of the                    B. Laurie, S. J. Murdoch, R. M. Norton, M. Roe, S. D. Son,
       ACM on Programming Languages, vol. 2, no. POPL, pp. 1–34, 2017.                          and M. Vadera, “Cheri: A hybrid capability-system architecture
[37]   G. Li, H. Zhang, J. Zhou, W. Shen, Y. Sui, and Z. Qian, “A hybrid                        for scalable software compartmentalization,” 2015 IEEE Symposium
       alias analysis and its application to global variable protection in the                  on Security and Privacy, pp. 20–37, 2015. [Online]. Available:
       linux kernel,” in 32nd USENIX Security Symposium (USENIX Security                        https://api.semanticscholar.org/CorpusID:7346980
       23), 2023, pp. 4211–4228.                                                         [57]   W. Xu, D. C. DuVarney, and R. Sekar, “An efficient and backwards-
[38]   L. Li, Y. Liu, D. Postol, L. Lampropoulos, D. Van Horn, and M. Hicks,                    compatible transformation to ensure memory safety of c programs,” in
       “A formal model of checked c,” in 2022 IEEE 35th Computer Security                       Proceedings of the 12th ACM SIGSOFT twelfth international sympo-
       Foundations Symposium (CSF), 2022, pp. 49–63.                                            sium on Foundations of software engineering, 2004, pp. 117–126.
[39]   H. Liljestrand, T. Nyman, K. Wang, C. C. Perez, J.-E. Ekberg, and                 [58]   A. Z. H. Yang, Y. Takashima, B. Paulsen, J. Dodds, and D. Kroening,
       N. Asokan, “Pac it up: Towards pointer integrity using arm pointer                       “VERT: Verified Equivalent Rust Transpilation with Large Language
       authentication,” ArXiv, vol. abs/1811.09189, 2018. [Online]. Available:                  Models as Few-Shot Learners,” May 2024. [Online]. Available:
       https://api.semanticscholar.org/CorpusID:53721743                                        http://arxiv.org/abs/2404.18852
[40]   A. Machiry, J. Kastner, M. McCutchen, A. Eline, K. Headley, and                   [59]   J. Yu, C. Watt, A. Badole, T. E. Carlson, and P. Saxena, “Capstone:
       M. W. Hicks, “C to checked c by 3c,” Proceedings of the ACM on                           A capability-based foundation for trustless secure memory access
       Programming Languages, vol. 6, pp. 1 – 29, 2022. [Online]. Available:                    (extended version),” ArXiv, vol. abs/2302.13863, 2023. [Online].
       https://api.semanticscholar.org/CorpusID:247748774                                       Available: https://api.semanticscholar.org/CorpusID:257220126
[41]   D. Magdaleno, “Bsd coreutils is a port of many utilities from bsd                 [60]   H. Zhang, C. David, Y. Yu, and M. Wang, “Ownership guided c to rust
       to linux and macos,” accessed: April, 2024. [Online]. Available:                         translation,” arXiv preprint arXiv:2303.10515, 2023.
       https://github.com/DiegoMagdaleno/BSDCoreUtils                                    [61]   J. Zhou, J. Criswell, and M. W. Hicks, “Fat pointers for temporal
[42]   R. Majumdar and K. Sen, “Hybrid concolic testing,” 29th International                    memory safety of c,” Proceedings of the ACM on Programming
       Conference on Software Engineering (ICSE’07), pp. 416–426, 2007.                         Languages, vol. 7, pp. 316 – 347, 2022. [Online]. Available:
       [Online]. Available: https://api.semanticscholar.org/CorpusID:6760091                    https://api.semanticscholar.org/CorpusID:251903483


                                                                                    15
                                Appendix                                 (a) The source code related to a spatial memory issue
                                                                          1   static const Pack packs[PACK_COUNT] = { ... };
A. Case Studies with Memory Safety Vulnerabilities                        2
                                                                          3   size_t shoco_decompress(...) {
Case Studies. We took a closer look at the translations of                4       while (in < in_end) {
shoco and urlparser, which are the two C programs with                    5           if (mark < 0) { ... }
                                                                          6           else {
spatial and temporal memory errors. We investigate if the                 7               if (o + packs[mark]...) // Global buffer overflow!
memory errors are eliminated or detected at runtime in the                8           }
                                                                          9       }
Rust translation.                                                        10   }
Case Study 1: shoco library. The C string data compression               (b) Safe Rust translation of the above C code by our user
library shoco has one spatial memory vulnerability (CVE-
                                                                          1   const PACKS: [Pack; PACK_COUNT] = [ ... ];
2017-11367)18 . The global array packs will be overread when              2
the byte to be decompressed is malformed. In this case, the               3   fn shoco_decompress(...) {
                                                                          4       while in_index < in_end {
return value by the header decoding function will be larger               5            if mark < 0 { ... }
than the length of packs array. When the return value is                  6            else {
used to index packs, the global buffer overflow happens, as               7                if o_index + PACKS[mark as usize]... // BoF caught
                                                                                    by runtime check
highlighted in line 5 in Fig 11 (a).                                      8            }
                                                                          9       }
    This spatial memory issue is detected at runtime in all              10   }
Rust translations from our users. Since array packs is read-
only, most translations lift it to a constant global array with          (c) Rust translation by compiler-based tools (Laertes/Crown)
type [Pack; 3] . Rust’s spatial bounds checking on arrays                 1   static mut packs: [Pack; 3] = ...;
                                                                          2
ensures any out-of-bound array access will not happen. The                3   pub unsafe extern "C" fn shoco_decompress(...) {
Rust compiler inserts runtime checks before the index access              4      ...
PACKS[mark]. This is because it cannot statically infer the               5      while in_0 < in_end {
                                                                          6          mark = ...;
validity of this access since the value of mark is determined             7          if ... {}
by the input. Fig 11 (b) shows one translation, where the binary          8          else {
will panic if the buffer overflow is about to happen.                     9                 if o.offset(packs[mark as usize].bytes_unpacked as
                                                                                   size) > out_end ... // BoF caught by runtime check
                                                                         10          }
    It is worth noting that existing c2rust-based tools (in-             11      }
cluding Laertes and Crown) are also able to eliminate this               12   }
vulnerability. They perform the same syntactic transformation
in their first stage to convert the global array declaration in C        Fig. 11: Case Study 1: The spatial memory issue in the shoco
to an equivalent declaration in Rust. Such array declarations            library is detected in all Rust translations.
are bounds-checked on access. Since their translation of this
global array and the access are similar, we show one example
of the translated code snippet by their tools relevant to the
vulnerability in Fig. 11 (c).                                            the struct representing the parsing result can hold an owning
                                                                         reference to the string, as shown in Fig. 12 (b). This copy
Case Study 2: urlparser library. The urlparser C library
                                                                         is automatically deallocated when the lifetime of the parsing
(commit a65623ad) has multiple memory-related vulnerabil-
                                                                         result (i.e., UrlData ) ends.
ities, including a spatial memory vulnerability that causes
information leaks and a temporal memory vulnerability that               Spatial memory errors. This library can overread the input
can potentially cause programs using this library to crash. Both         string and print extra memory value if the input URL is
vulnerabilities have been fixed in their latest version.                 malformed. The root reason is that it directly increments
Temporal memory errors. This library aliases the input URL               the URL pointer to skip the scheme separator :// without
string pointer and stores it as a field in its custom structure          checking if the separator exists in the URL. When it does
when parsing this string. In addition to the parsing API, it             not exist, the pointer is incremented to be outside of the
offers APIs that read the parsing result, such as the inspect            input string buffer. This bug is caught at runtime by all Rust
API. This is problematic because this library does not own               translations. This pointer is lifted to &str or &String types,
the memory referred to by this aliased pointer. Use-after-free           which enforce spatial bounds checking on access. Several other
can happen if a program using this library calls the parse API           heap buffer overflow issues exist as well, all due to saving
providing a string that does not live long enough before calling         strings to allocated memory regions with insufficient space,
other APIs, such as inspect . Fig. 12 (a) shows the related              i.e., having an allocated size smaller than the string length.
source code and a small example program that triggers use-               Such spatial issues do not exist in safe Rust translations by
after-free. This issue has been fixed in commit 752635e.                 users due to automated memory management.

    This temporal issue is eliminated in all Rust translations
                                                                         B. Examples of Logical Translation Errors by Users
because of the temporal safety statically enforced by borrowing
rules and the String type. Any code pattern that can result                  Here we describe several logical translation errors we
in double-free or use-after-free cannot be compiled. To satisfy          observed in translations of fmt program, along with a possible
borrow rules, user translations copy the input string so that            fix for each.
  18 https://nvd.nist.gov/vuln/detail/CVE-2017-11367                     1) Logical Errors that Require More Thorough Testing

                                                                    16
(a) Code example related to the temporal memory issue                       Passing Test (Translation A)
 1   // urlparser.c                                                         Executed command : ./ fmt -c -w 10
 2   url_data_t *url_parse (char *url) {                                    Input : " Center "
 3     url_data_t *data = malloc(sizeof(url_data_t));                       C Output : " Center " // 2 leading padding spaces
 4     data->href = url; // Store the pointer
 5   }
                                                                            Rust Output : " Center " // same as C
 6   void url_data_inspect (url_data_t *data) {
 7     printf("#url␣=>\n");                                                 Failing Test 1
 8     printf("␣␣␣␣.href:␣\"%s\"\n", data->href); // use the pointer
 9   }
                                                                            Executed command : ./ fmt -c -w 10
10                                                                          Input : "z\ u00df \ u6c34 \ U0001d10b "
11   // poc.c                                                               C Output and Rust Output have different display
12   int main() {                                                               width
13       // our_url points to a URL string stored on the heap
14       url_data_t *parsed = url_parse(our_url);                           Failing Test 2
15       assert(parsed);
16       free(our_url);                                                     Executed command : ./ fmt -c -w 10
17       url_data_inspect(parsed); // Use-after-free here!                  Input : " Center *"
18   }                                                                      C Output : " Center *" // 2 leading padding spaces
                                                                            Rust Output : " Center *" // off -by -one error !
(b) One corresponding Rust translation of the above C code
 1 fn url_parse(url: &str) -> Option<UrlData> {                             The bugfix (Translation A)
 2     // data is a default UrlData instance
 3     data.href = Some(url.to_string());
                                                                            ...
 4     // href has Option<String> type
                                                                            + use unicode_width :: UnicodeWidthChar ;
                                                                            if bytes_read == 0 { break ; }
 5     // ...                                                               let len: usize = p1.trim (). chars ().map(
 6 }                                                                            |c| if c == ’\t’ { ’ ’ } else { c }
 7 fn url_data_inspect(data: &UrlData) {                                    - ).map(char :: len_utf8 ).sum ();
 8     println!("#url␣=>");                                                 + ).map (|c| c. width (). unwrap_or (1)).sum ();
 9     println!("␣␣␣␣.href:␣{:?}", data.href); // Owned String. No          let padding =
        temporal issue.                                                     - ( config . goal_length - len) / 2;
10 }                                                                        + ( config . goal_length - len + 1) / 2;
                                                                            ...
Fig. 12: Case Study 2: The temporal memory issue in the
urlparser library is eliminated in all Rust translations.                   Fig. 13: The Translation Version A wrongly computes the
                                                                            display width. Part (a): 1 passing and 2 failing tests when
                                                                            aligning the input centrally in a 10-byte line (executed com-
                                                                            mand: ./fmt -c -w 10 ). Part (b): Bugfix for two semantic
    The full program of the translation (Version A) we have                 discrepancies.
seen before (Fig. 3), although passing all tests with 85%
code coverage, has at least two more semantic discrepancies
from the source program. Surprisingly, the bugs are in code
lines covered by passing tests. We have two failing tests                       There is another difficult-to-fix semantic discrepancy that
demonstrating each of the translation bugs in Fig. 13. One bug              exists in all user translations for the fmt program. They all
is revealed when there are multi-byte characters rather than just           omit the functionality of replacing invalid Unicode characters
ASCII characters in the input. Another bug is revealed when                 with ?. With a deeper investigation, we find that this is not
there are odd numbers rather than even numbers of padding                   easy to fix due to various differences in data types and APIs
spaces. The unit tests written by the user miss those cases.                across the two languages.
    The first discrepancy is due to calling the wrong API when
                                                                                Fig. 14 highlighted the branch of the C code to handle
computing the display width of the characters. The translation
                                                                            this functionality, which was previously skipped in Fig. 2
used char::len_utf8 which computed the size in bytes of
                                                                            for simplicity. All users assigned to this program omit this
a Unicode character instead of display width. For the frequent
                                                                            functionality in their translation.
ASCII characters, the size in bytes happens to be 1, which
coincides with their display size. However, the failing input                   With closer examination, it turns out that this behavior
” z\u00df\u6c34\U0001d10b ” is an example where the size                    is not easily implementable when using the String type to
in bytes is different from the display width. It is not revealed            represent p1 . In Rust, characters stored in a String data
by the passing unit tests which only include ASCII characters.              type are limited to Unicode characters rather than arbitrary
The fix is to use the c.width method, as shown in Fig. 13.                  raw bytes. When using the Rust API read_line to read
    The second discrepancy is due to an off-by-one error in the             a String from the stream, it returns either a String
computation of padding spaces, making the Rust translation                  instance or a Err result if there are invalid characters. When
correct only when the number of spaces is even. The Rust                    returning an Err, there is no API to tell where the invalid
program uses a slightly different computation to split the                  characters are. With a more careful search, we find an API
padding spaces into leading and trailing ones, compared to                  from_utf8_lossy on the String type in Rust that is
the C program. While the C program behaves like a round-up                  closer to what we want. This API can create a String
division, the Rust program takes the floor division. The passing            from a buffer with each point of decoding error marked
test does not reveal this difference. The correct fix is shown              with ? . However, we soon realize that this API also does
in Fig. 13.                                                                 not bridge the semantic gap. The C code not only outputs
                                                                            ? at the position of invalid characters, but also outputs the
2) Semantic Differences that are Not Easy to Fix                            same number of ? as the number of invalid bytes. The

                                                                       17
static void                                                                      As a result, we can consider refining the choice of Rust
center_stream (FILE *stream , const char *name)
{                                                                            data types for p1 . The type of p1 should carry sufficient
    char *p1 , *p2;                                                          information and support APIs to identify (1) the locations of
    wchar_t wc;
    size_t len; /* Display width of the line. */                             invalid characters, and (2) the number of invalid bytes at each
    int w1;      /* Display width of one character . */
    int w2;      /* Length in bytes of one character . */                    location.
    while ((p1 = get_line ( stream )) != NULL) {                                 Many Rust data types can represent a string but not all
        len = 0;
          for (p2 = p1; *p2 != ’\0 ’; p2 += w2) {                            of them can meet our requirements. One possible choice is
              // ... omitted                                                 std::ffi::OsString , which is a platform-native string type
               if (( w2 = mbtowc (&wc ,p2 , MB_CUR_MAX ))== -1) {            that may hold invalid UTF-8 characters. Vec<u8> is another
                   (void) mbtowc (NULL ,NULL , MB_CUR_MAX );                 choice that can store invalid Unicode characters and supports
                   *p2 = ’?’;
                   w2 = 1;                                                   per-byte control. Here we use Vec<u8> as an example.
                   w1 = 1;
               } else if (( w1 = wcwidth (wc)) == -1)                            Now the question is about how to use Vec<u8> to achieve
                   w1 = 1;
                                                                             the intended program behavior, i.e., to parse Unicode charac-
            // ... omitted
        }                                                                    ters and replace invalid ones with the correct number of ques-
        // ... print whitespace padding                                      tion marks. One option is to use std::str::Utf8Chunks
        puts(p1);
    }                                                                        structure from the Rust standard library. This structure allows
    // ...
}                                                                            iteratively check u8 bytes referred by an immutable slice and
                                                                             convert them to Unicode characters if valid. Fig. 15 shows
Fig. 14: A highlighted block of code of the C example program                the fixed version of Translation A with the correct Unicode
(fmt) that deals with invalid characters (previously omitted for             character parsing logic when using Vec<u8> type for p1 .
simplicity).                                                                 Because of this new choice of type, the original code to read
                                                                             lines and parse characters needs to be updated accordingly. We
                                                                             update multiple lines in the method calls on stream to read
                                                                             the input and iteratively save the line-separated input into a
 1 use unicode_width::UnicodeWidthChar;                                      Vec<u8> . The eventually fixed translation (shown in Fig. 15)
 2 fn center_stream<R: BufRead>(mut stream: R, _name: &str, config:
         &Config) {                                                          can pass the tests (behave the same as the C program) on the
 3     let mut p1: Vec<u8> = vec![];                                         aforementioned invalid byte sequence.
 4     while let Ok(bytes) = stream.read_until(b’\n’, &mut p1) {
 5         if bytes == 0 { break; }
 6                                                                           C. End-to-End Performance Results of User Translations
 7         let mut res = String::new();
 8         let mut idx = 0;                                                      Besides the performance results explained in Sec. V-B,
 9         loop {                                                            we also measure the end-to-end performance on tests using
10             let remain: &[u8] = &p1[idx..];
11             match remain.utf8_chunks().next() {                           hyperfine [2], which considers the load/start-up time of pro-
12                 Some(s) => {                                              grams, in addition to the execution of the main functionality.
13                     let valid = s.valid();
14                     if valid.is_empty() {
                                                                             The average overhead is around 13% across the eight Rust
15                          res.push_str("?");                               translations. Details of the performance measure for each
16                          idx += 1;                                        program are shown in Fig. 16. This measure might not reflect
17                     } else {
18                          res.push_str(valid);                             the performance we care about since initialization costs are
19                          idx += valid.len();                              usually amortized for long-running programs and libraries.
20                     }
21                 },
                                                                                                  2.0                                                                 2.0
22                 None => {
                                                                           Normalized Time Cost




                                                                                                                                               Normalized Time Cost




                                                                                                  1.8                                                                 1.8
23                     break;                                                                     1.6                                                                 1.6
24                 }                                                                              1.4                                                                 1.4
25             }                                                                                  1.2                                                                 1.2
26         }                                                                                      1.0                                                                 1.0
27         let len = ...;                                                                         0.8                                                                 0.8
                                                                                                  0.6                                                                 0.6
28         // ... remaining lines omitted                                                         0.4                                                                 0.4
29     }                                                                                          0.2                                                                 0.2
30 }                                                                                              0.0                                                                 0.0
                                                                                                           lit r t in tf o st             er                                   lit r t in tf o st             er
                                                                                                        csp exp fm jo prin shoc te rlpars                                   csp exp fm jo prin shoc te rlpars
                                                                                                                                  u                                                                   u
Fig. 15: The fixed Translation A where the data type of p1
is refined from String to Vec<u8> . The code to parse the                                               (a) Compiled with -O2                                               (b) Compiled with -O3
Unicode character is updated accordingly.
                                                                             Fig. 16: End-to-end running time measured by hyperfine [2]
                                                                             of the most similar Rust translation compared to the original
                                                                             C at different optimization levels. The time for the baseline C
from_utf8_lossy API is not behaving the same way as                          (dashed line) is normalized to 1.
the corresponding C code—it replaces each chunk of invalid
bytes as one ?. For example, for the invalid byte sequence
"\x7a\xc3\x9f\xe6\xb0\xc3\xf0\x9d\x84\x8b" ,           the
                                                                             D. Details of Code Patterns involve Globals and Unions
Rust String API from_utf8_lossy outputs a string with two
"?" while the C code outputs three "?" . In summary, we                      Translating Mutable Globals. There are four strategies ob-
cannot find APIs on String to preserve the same semantics.                   served from the user translations on the translation of global,

                                                                      18
as previously explained in Sec. V-C. Here, we show a code                    declares what is equivalent to such a cursor on the stack ( argv
example for each strategy.                                                   and idx). The Rust code passes them by reference to the
                                                                             function that needs to access them (i.e., getchr).
Translating Mutable Globals (Strategy A)
 1   // printf.c                                                                 When there are many global variables, globals that are used
 2   char **gargv;                                                           together with similar lifetimes can be grouped into structs.
 3   static int getchr(void)                                                 Fig. 18 shows a piece of code from the fmt program in our
 4   {
 5       if (!*gargv)                                                        benchmark that uses more than ten mutable global variables for
 6           return((int)’\0’);                                              sharing states between functions. A user translation (bottom of
 7       return((int)**gargv++);
 8   }
                                                                             Fig. 18) groups the relevant global variables that are accessed
 9   ...                                                                     together into a struct named TextInfo. Operations on those
                                                                             global variables (such as the new_paragraph function) are
 1   // printf.rs                                                            turned into methods implemented on the struct TextInfo.
 2   fn getchr(argv: &Vec<String>, idx: &mut usize) -> char {
 3       if *idx >= argv.len() {
 4           return ’\0’;                                                    Translating Mutable Globals (Strategy B)
 5       }
                                                                              1   // csplit.c
 6       let c: char = argv[*idx]...; // access argv
                                                                              2   long      nfiles;
 7       *idx += 1; // change idx (equivalent to incrementing gargv)
                                                                              3   void cleanup(void)
 8       return c;
                                                                              4   {
 9   }
                                                                              5        char fnbuf[PATH_MAX];
10   int main() {
                                                                              6        for (i = 0; i < nfiles; i++) {
11       let mut argv: Vec<String> = env::args().collect();
                                                                              7            snprintf(fnbuf, ...) // details omitted
12       let mut idx: usize = 1; // globals moved to stack
                                                                              8            unlink(fnbuf);
13       // ...
                                                                              9        }
14       let c: char = getchr(&argv, &mut idx); // passing references
                                                                             10   }
15   }
                                                                             11   ...
16   ...

                                                                              1   // csplit.rs
Fig. 17: (Top) A part of the printf C program with a mutable                  2   static FILES: Lazy<Arc<Mutex<Vec<String>>>> = Lazy::new(|| ...);
gargv. (Bottom) A Rust translation using strategy A: Moving                   3   // ref-counted with lock
                                                                              4   fn cleanup() -> io::Result<()> {
globals to locals.                                                            5       let mut files = FILES.lock().unwrap();
                                                                              6       for file in files.iter() {
                                                                              7           fs::remove_file(file)?;
                                                                              8       }
Translating Mutable Globals (Strategy A + Structs)                            9       files.clear();
                                                                             10       Ok(())
 1   // fmt.c                                                                11   }
 2   static int centerP = 0;                                                 12   ...
 3   static size_t x;
 4   // ... 15 globals in total
 5   static void new_paragraph(size_t indent)                                Fig. 19: (Top) A part of the csplit C program with mutable
 6   {
 7       // ... modifying 4 globals                                          globals. (Bottom) A Rust translation using strategy B: dynamic
 8       x = indent;                                                         references.
 9   }
10   ...

 1   // fmt.rs                                                                   (B) Dynamic References. Fig. 19 shows an example where
 2   pub struct TextInfo {                                                   global mutable variables are translated into dynamic refer-
 3       center: bool, // globals become struct fields                       ences. The top of Fig. 19 is a piece of the csplit C
 4       x: usize,
 5       // ... other semantically related fields                            program. The cleanup is a function to be called as a signal
 6   }                                                                       handler. A user translation (bottom of Fig. 19) uses a dynamic
 7   impl TextInfo {
 8       pub fn new_paragraph(&mut self, indent: usize) {
                                                                             reference Arc<Mutex<T>> to implement this global variable.
 9           // ... modifying multiple fields in &mut self                   Correspondingly, the Rust translation uses lock().unwrap()
10           self.x = indent;                                                to guard the access to the content of the variable. It is
11           ...
12       }                                                                   worth noting that while signal handlers, in general, need
13   }                                                                       synchronization, it is not necessary in this specific program
14   ...                                                                     considering its possible behaviors.
Fig. 18: (Top) A part of the fmt C program with mutable                          (C) Atomics. Fig. 20 shows a different Rust translation
globals. (Bottom) A Rust translation using strategy A and                    from Strategy (C) of the same piece of code in csplit. This
group globals into structs.                                                  time, the code is leveraging an AtomicU32 type declared as
                                                                             a mutable global variable. A nice property of Atomic types
                                                                             is that “immutable” references to it (from the perspective of
    (A) From Globals to Locals. Fig. 17 shows an example                     the Rust language) allow both read and write access to the
where globals are moved to stack. The top of Fig. 17 shows                   variable in safe Rust using specific APIs, similar to the interior
a piece of code from the printf C program that declared a                    mutability pattern. Thus, every function can freely obtain
mutable global variable named gargv. This variable is used as                “immutable” references and write to Atomic types without
a cursor that shifts around to access arguments ( argv ) passed              violating borrowing rules. At the same time, the runtime cost
to the main function. A Rust translation by our user simply                  is also potentially lower than that of locks.

                                                                        19
Translating Mutable Globals (Strategy C)                                   Translating Unions as Enum
 1   // csplit.c                                                            1    // expr.c
 2   long      nfiles;                                                      2    struct val {
 3   const char *prefix;                                                    3        enum { integer, string } type;
 4   void cleanup(void)                                                     4        union {
 5   {                                                                      5             char    *s;
 6        char fnbuf[PATH_MAX];                                             6             int64_t i; } u;
 7        ...                                                               7    };
 8        for (i = 0; i < nfiles; i++) {                                    8    int is_zero_or_null(struct val *vp)
 9            snprintf(fnbuf, ..., prefix, ...);                            9    {
10            unlink(fnbuf);                                               10        if (vp->type == integer)
11        }                                                                11             return vp->u.i == 0;
12   } ...                                                                 12        else
                                                                           13             return *vp->u.s == 0 ||
                                                                           14               (to_integer(vp, NULL) && vp->u.i == 0);
 1   // csplit.rs
                                                                           15    } ...
 2   static COUNT: AtomicU32 = AtomicU32::new(0);
 3   static PREFIX: OnceCell<String> = OnceCell::new();
 4   fn clean_up_handler() -> io::Result<()> {                              1    // expr.rs
 5       ...                                                                2    enum Val {
 6       let count = COUNT.load(Ordering::Acquire);                         3      Integer(i64),
 7       let pref = PREFIX.get().unwrap();                                  4      String(String),
 8       for i in 0..count {                                                5    }
 9           let filename = format!("{}...", pref, ...);                    6    impl Val {
10           let _ = fs::remove_file(...);                                  7      fn is_zero_or_null(&self) -> bool {
11       }                                                                  8        match self {
12       Ok(())                                                             9           Val::Integer(i) => *i == 0,
13   } ...                                                                 10           Val::String(s) => s.is_empty() || s.parse::<i64>().map_or(
                                                                                       false, |i| i == 0),
                                                                           11        }
Fig. 20: (Top) A part of the csplit C program with mutable                 12      } ...
globals. (Bottom) A Rust translation using strategy C: atomics.
                                                                           Fig. 22: (Top) A part of the expr C program that uses tagged
Translating Unions as Enum
                                                                           unions. (Bottom) A Rust translation that translates tagged
                                                                           union into enum.
 1   // shoco.c
 2   union Code {
 3      uint32_t word;
 4      char bytes[4];
 5   };                                                                    ( [u8; 4]). The choice of API is guarded by a compile-time
 6   size_t shoco_compress(...) {
 7      union Code code;                                                   constant cfg!(target_endian = "big") that is similar to
 8      while // ...                                                       conditional compilation in C (such as #ifdef). The type
 9        // ... code lines modifying code.word                            conversion and the if branch in the Rust code have zero
10        for (unsigned int i=0; i<packs[pack_n].bytes_packed; ++i)
11          o[i] = code.bytes[i];                                          cost when optimization is turned on. Moreover, the differ-
12        // ...                                                           ences between the to_le_bytes and to_be_bytes are also
13   } ...
                                                                           small after optimization. On x64 architecture (little endian),
 1 // shoco.rs
                                                                           to_be_bytes will result in code with just one more bswap
 2 pub fn shoco_compress(...) {                                            instruction.19
 3     let mut code: u32;
 4     while // ...                                                            (B) Variant Record. Fig. 22 shows an example of using
 5         // ... code lines modifying code                                tagged unions in C. The top of Fig. 22 shows a slice of the
 6         for i in 0..packs[pack_n].bytes_packed {
 7             if cfg!(target_endian = "little") {                         expr C program that declares a variant record (val) and code
 8                  out[out_index + i] = code.to_le_bytes()[i];            accessing the field u which is a union. From the code, we can
 9             } else {                                                    infer that semantically there is a mapping between the value of
10                  out[out_index + i] = code.to_be_bytes()[i];
11             }                                                           tag type and the valid field in the union u . Such a mapping is
12         } ...                                                           an important type-safety invariant, but it is not explicit in the
13 } ...
                                                                           type system of C. The Rust translation, shown at the bottom
                                                                           of Fig. 22, implements the same functionality with statically
Fig. 21: (Top) A part of the shoco C program that uses tagged              enforced type safety. The code implements the variant record
unions. (Bottom) A Rust translation that translates tagged                 using enum in Rust, which explicitly associates tag values to
union into enum.                                                           valid fields in the record. Code accessing an enum in Rust is
                                                                           checked statically, preventing type safety violations as well as
                                                                           logical errors such as missing the handling of certain tags.
Translating Unions. There are two different use cases of C
union observed in our benchmarks, including (A) type punning
and (B) variant record. One example of each is shown here.
   (A) Type Punning. Fig. 21 shows an example of type
punning in the shoco C program. The C union Code is
used to access bytes of an integer (uint32_t). An example
Rust translation (bottom of Fig. 21) uses to_le_bytes and
to_be_bytes that convert an integer (u32) into a byte array                     19 Tested with rustc 1.81.0 with option -C opt-level=2 .




                                                                      20
