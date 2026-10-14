                                         Rust’s Type Checker Implementation Is Unsound: An
                                         Empirical Study on Soundness Bugs in rustc
                                         YUSUNG SIM, KAIST, Republic of Korea
                                         SUKYOUNG RYU, KAIST, Republic of Korea
                                         JAEMIN HONG, UNIST, Republic of Korea and Yale University, USA
                                         Rust is claimed to be a type-sound language capable of preventing various undesirable behaviors, including
                                         memory bugs. However, rustc, the official Rust compiler, is not immune to defects; it contains soundness bugs,
arXiv:2608.28713v1 [cs.SE] 28 Aug 2026




                                         where the compiler accepts programs that should be rejected during type checking. In this work, we present
                                         an empirical study of 30 issues that report potential soundness bugs in rustc, collected from the GitHub issue
                                         tracker between January 1, 2022 and September 1, 2025. We analyze each issue in depth, focusing on its affected
                                         feature, symptom (how the feature is mishandled), consequence (the resulting undesirable behavior), triggering
                                         features, community consensus regarding whether it is a bug, and lifecycle, including introduction, discovery,
                                         and fix. Furthermore, we investigate existing artifacts, including implementations such as AddressSanitizer,
                                         Miri, Chalk, and a-mir-formality, alongside documentation such as the Rust Reference, the FLS, and Rust RFCs
                                         to assess their potential as oracles for testing the type soundness of rustc. Our key findings indicate that: (1)
                                         Certain soundness bugs, typically triggered by implied bounds or trait objects, compromise memory safety.
                                         (2) Sound type checking is challenged by edge cases involving associated types and the interaction between
                                         lifetimes and traits. (3) Most bugs persist from the initial introduction of the relevant features and require
                                         significant time to be discovered. (4) While AddressSanitizer and Miri can detect soundness bugs that lead
                                         to memory bugs, a-mir-formality and Chalk are currently immature despite their potential to identify other
                                         bug categories. (5) Existing documentation frequently fails to provide precise explanations of the language
                                         semantics.
                                         CCS Concepts: • Software and its engineering → Compilers; Software defect analysis; Empirical software
                                         validation; • Theory of computation → Type theory.
                                         Additional Key Words and Phrases: Rust, type system, compiler bugs, empirical study, rustc
                                         ACM Reference Format:
                                         Yusung Sim, Sukyoung Ryu, and Jaemin Hong. 2026. Rust’s Type Checker Implementation Is Unsound: An
                                         Empirical Study on Soundness Bugs in rustc. Proc. ACM Softw. Eng. 3, ISSTA, Article ISSTA129 (October 2026),
                                         24 pages. https://doi.org/10.1145/3832220

                                         1   Introduction
                                         Rust [36] is designed to be a type-sound language, aiming to prevent various undesirable behaviors,
                                         including memory bugs like use-after-free, at compile time through type checking [27]. Recognizing
                                         this benefit, researchers and practitioners have adopted Rust for systems programming to enhance
                                         software reliability. Operating systems, web browsers, and network stacks have been developed
                                         in Rust [5, 7, 10, 11, 13, 24, 25, 30, 32, 38, 42, 48]; legacy systems, including Linux, have begun
                                         integrating Rust [1, 3, 26, 34]; and techniques to translate legacy code into Rust have been extensively
                                         Authors’ Contact Information: Yusung Sim, KAIST, Daejeon, Republic of Korea, yusungsim@kaist.ac.kr; Sukyoung Ryu,
                                         KAIST, Daejeon, Republic of Korea, sryu.cs@kaist.ac.kr; Jaemin Hong, UNIST, Ulsan, Republic of Korea, jaemin.hong@
                                         unist.ac.kr and Yale University, New Haven, USA, jaemin.hong@yale.edu.




                                         This work is licensed under a Creative Commons Attribution 4.0 International License.
                                         © 2026 Copyright held by the owner/author(s).
                                         ACM 2994-970X/2026/10-ARTISSTA129
                                         https://doi.org/10.1145/3832220


                                                                     Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
ISSTA129:2                                                               Yusung Sim, Sukyoung Ryu, and Jaemin Hong


studied [8, 16–23, 65, 67, 72–75]. All these lines of work rely on the fundamental assumption that
the Rust type checker is sound.
   Unfortunately, rustc, the official Rust compiler, is not free from defects. Liu et al. [35] recently
demonstrated that the compiler suffers from various bugs, including crashes, miscompilations, and
improper diagnostic messages. While all bugs warrant attention, soundness bugs, where the type
checker accepts a program that should be rejected, are especially critical, as they undermine Rust’s
core value of type soundness guarantee. Notably, among the 301 rustc bugs collected by Liu et al.,
22 were identified as soundness bugs.
   Despite their importance, soundness bugs in the rustc implementation have not yet been studied
in depth. For instance, it remains unclear which language features are most prone to soundness bugs,
even though such insights would allow researchers to prioritize specific features when developing
testing techniques or formalizing the type system. While Liu et al. analyzed rustc bugs and provided
valuable insights, their study encompassed all bug categories rather than focusing specifically on
soundness bugs. We believe that an in-depth study dedicated to soundness bugs can benefit the
community and complement existing work.
   In this work, we study 30 soundness issues collected from the rustc GitHub issue tracker, each
representing a case where a developer reported that the compiler accepted code that should not
pass type checking. We analyze each issue in depth to characterize the following: the affected
feature, the symptom (i.e., how the feature is erroneously handled), the consequence (i.e., the specific
undesirable behavior enabled by the issue), the features that trigger the issue, the consensus of the
community regarding whether it is indeed a bug, and the lifecycle of the issue, encompassing its
introduction, discovery, and fix.
   Furthermore, we investigate artifacts that can aid in testing the type soundness of rustc. Liu
et al.’s study showed that existing testing tools for rustc [6, 14, 29, 43, 49, 64, 68] revealed crash
bugs but failed to identify a single soundness bug. A primary reason for this is the absence of a test
oracle capable of determining whether a given program should be accepted or rejected. To address
this, RustSmith [49] employs differential testing, comparing results across different rustc versions
and configurations. However, its effectiveness is limited because most soundness issues persist
across multiple versions and settings, as we observe in our study. This underscores the necessity of
a test oracle tailored to type soundness.
   For this reason, we study the following implementations, which serve as potential test oracles:
AddressSanitizer [47] (a memory bug detector), Miri [28, 59] (a Rust interpreter for detecting
undefined behavior), Chalk [57] (an implementation of the Rust trait system based on a logic
solver), and a-mir-formality [56] (an executable model of the Rust type system). We assess their
effectiveness by checking whether they can determine that the programs from the collected issues
should be rejected.
   In addition, we study existing documentation that explains the semantics of Rust. Previous
research has demonstrated that mechanized specifications [40, 69] can serve as effective test oracles
for language implementations, detecting numerous bugs in JavaScript engines and transpilers [39,
41, 46] and WebAssembly engines [70], as well as soundness bugs in the P4 type checker [31].
Although Rust currently lacks a full specification [2], documents such as the Rust Reference [60],
the FLS [58], and Rust RFCs [62] provide explanations of the semantics. Therefore, we investigate
the current state of this documentation and assess whether these explanations are sufficiently clear
to develop test oracles for type soundness.
   Contributions. Overall, our contributions are as follows:

• We construct a three-and-a-half-year dataset of 30 soundness issues in rustc (§3).

Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
 Rust’s Type Checker Implementation Is Unsound: An Empirical Study on Soundness Bugs in rustc                ISSTA129:3


 • We conduct an empirical study of the soundness issues across multiple dimensions, including
   their affected features, symptoms, consequences, triggers, consensus, and lifecycles (§4).
 • Based on our analysis, we summarize key findings and provide actionable suggestions for
   researchers and rustc developers to better detect and mitigate soundness bugs (§5).
 • We assess existing artifacts that could potentially serve as oracles for testing type soundness,
   discussing their current capabilities and providing guidelines for their use (§6).
   Summary of Findings. We summarize our key findings as follows:
 • Certain soundness bugs lead to memory bugs; specifically, implied bounds and trait objects are
   critical triggering features that can compromise memory safety.
 • Associated types frequently serve as a mechanism for exploiting edge cases in other features, and
   the interaction between lifetimes and traits poses challenges for sound type checking.
 • Many bugs have persisted since the initial introduction of the relevant features, typically requiring
   a long time to discover and remaining present across multiple compiler versions.
 • AddressSanitizer and Miri can detect soundness bugs that manifest as memory bugs; other bug
   categories could be identified by a-mir-formality and Chalk in the future, but they are currently
   immature.
 • Existing documents are often unclear, and constructing a mechanized specification for Rust
   cannot be achieved simply by collecting them.

 2     Background: Language Features of Rust
 In this section, we provide a brief overview of the language features of Rust that commonly appear
 in the soundness issues we collected.

 2.1     Lifetimes
In Rust, a reference is a pointer with a static guarantee that it points to a valid value. Each reference
has a lifetime, which specifies the duration for which the reference is valid. Lifetimes are key to
ensure memory safety; for instance, the compiler ensures that a lifetime ends before the referenced
value goes out of scope. A reference has a type &’a T, where ’a is the lifetime and T is the type of
the value.
   Functions can have lifetime parameters to express the relationship between the lifetimes of the
parameters and the return value. For example, the following function with two lifetime parameters
’a and ’b takes two references to integers (i32) and returns the first one, specifying that the lifetime
of the return value is the same as that of the first parameter:
1 fn   foo < 'a , 'b >( v : & ' a i32 , u : & ' b i32 ) -> & 'a i32 { v }
    When a lifetime ’a is longer than or equal to another lifetime ’b, i.e., ’a outlives ’b, a reference
 of lifetime ’a can be used where a reference of lifetime ’b is expected. By default, different lifetime
 parameters are not considered to outlive each other, but programmers can introduce lifetime bounds
 of the form ’a: ’b, implying ’a outlives ’b, as shown below:
1 fn foo < 'a ,    'b >( v : & ' a i32 ) -> & ' b i32 { v } // error
2 fn bar < ' a :   'b , 'b >( v : & ' a i32 ) -> & ' b i32 { v } // ok
3 fn baz () {      let p ; { let v = 0; p = bar (& v ) ; } * p ; } // error
4 fn qux () {      let v = 0; let p = bar (& v ) ; * p ; } // ok
 In foo, returning v is disallowed because there is no guarantee that ’a outlives ’b; in bar, ’a: ’b
 allows it. The compiler checks whether the specified lifetime bounds are satisfied at each call site:
 baz is rejected because p is used after v goes out of scope, while qux is accepted.
    Since a value must remain valid while its reference is live, a type &’a T is considered well-formed
 only when every lifetime appearing in T outlives ’a. For example, &’a &’b i32 is well-formed only
 if ’b: ’a holds.

                             Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
 ISSTA129:4                                                               Yusung Sim, Sukyoung Ryu, and Jaemin Hong


   To reduce the burden of stating lifetime bounds, Rust supports implied bounds, which auto-
 matically introduce lifetime bounds deduced from the well-formedness of the types used in each
 definition (e.g., the parameter and return types of a function). In the following example, foo passes
 type checking due to the implied bound ’b: ’a and is equivalent to bar:
1 fn   foo < 'a , 'b >( v : & ' a & ' b i32 ) {}
2 fn   bar < 'a , 'b : 'a >( v : & ' a & ' b i32 ) {}
 Note that implied bounds are distinct from Rust’s lifetime elision, which allows programmers to
 omit explicit lifetime annotations (e.g., writing &i32 instead of &’a i32), not lifetime bounds, which
 the compiler then infers based on fixed syntactic patterns.
    So far, the names of lifetimes have been explicitly introduced by lifetime parameters, but there is
 one exception: the special lifetime ’static denotes the entire duration of the program and does not
 need to be defined as a lifetime parameter. By definition, ’static outlives any lifetime. A reference
 to a global variable or a constant has the ’static lifetime.

 2.2     Traits
 A trait represents a set of types, similar to abstract classes or interfaces in object-oriented languages
 and type classes in Haskell. Consider the following example:
1 trait  X { fn foo ( self ) ; }
2 struct   S ; impl X for S { fn foo ( self ) { println !(" S ") ; } }
3 fn bar < T : X >( v : T ) { v . foo () ; }
4 fn baz <T >( v : T ) where T : X { v . foo () ; }
5 fn qux ( v : impl X ) { v . foo () ; }

 Here, X denotes a set of types that implement the method foo (line 1), and S belongs to X, i.e., S
 implements X (line 2). The function bar takes a value of any type T that implements X and calls foo
 (line 3). In bar, X is a trait bound of T. Trait bounds can also be specified in a where clause (line 4). In
 addition, instead of introducing a type parameter and its bound, we can use an impl trait type, such
 as impl X, as a parameter type (line 5). This use of an impl trait type is called an argument-position
 impl trait (APIT). All the functions bar, baz, and qux are equivalent, representing the same set of
 possible arguments with different syntax.
    It is possible to implement a trait for multiple types using a single impl, as shown below:
1 struct    S ; struct R ; struct Q ; trait X {} impl X for S {} impl X for R {}
2 trait    Y {} impl < T : X > Y for T {} trait Z {} impl <T > Z for T {}
 S and R implement X, but Q does not (line 1). Since Y is implemented for all types that implement
 X, both S and R implement Y, but Q does not; on the other hand, Z is implemented for all types,
 including S, R, and Q (line 2).
   Traits can require types not only to provide particular methods but also to specify associated
 types, as in the following example:
1 trait X {    type A ; fn foo ( self ) -> Self :: A ; }
2 struct S ;   impl X for S { type A = i32 ; fn foo ( self ) -> Self :: A { 0 } }
3 struct R ; impl X for R { type A = f32 ; fn foo ( self ) -> Self :: A { 0.0 } }
4 fn bar < T : X >( v : T ) -> T :: A { v . foo () }
5 fn baz < T : X >( v : T ) -> <T as X >:: A { v . foo () }
6 fn qux < T : X < A = i32 > >( v : T ) -> i32 { v . foo () }

 A type implementing X must specify an associated type A, and its method foo must return a value
 of type A (line 1). Both S and R implement X, defining different types for A (lines 2 and 3). The
 function bar returns the value from foo, whose type is denoted T::A (line 4). We can also write <T
 as X>::A to disambiguate which trait declares the associated type (line 5), which is useful when
 multiple traits define an associated type with the same name. Additionally, to specify a set of types
 implementing a trait with a specific associated type, we can use a trait bound like X<A = i32>; this
 allows S to be passed to qux, but not R (line 6).

 Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
 Rust’s Type Checker Implementation Is Unsound: An Empirical Study on Soundness Bugs in rustc                 ISSTA129:5


    Traits are also used to hide the concrete return type of a function by specifying the return type
 as impl X, called a return-position impl trait (RPIT). Consider the example below:
1 trait X {  fn foo ( self ) ; }
2 struct S ; impl X for S { fn foo ( self ) {} } impl S { fn bar ( self ) {} }
3 fn baz () -> impl X { S }
4 fn qux () { let v = baz () ; v . foo () ; /* ok */ v . bar () ; /* error */ }

 S defines two methods foo and bar, while only foo is part of the trait X (lines 1 and 2). The
 function baz returns S, but it hides this information from callers, revealing only that the return type
 implements X (line 3). Therefore, qux can call foo on the returned value, but not bar (line 4). Note
 that the purpose of an RPIT is not to allow returning values of different types. Even when using an
 RPIT, a single underlying return type must exist. For instance, the following code is rejected even
 though both S and R implement X:
1 trait X {} struct        S ; impl X for S {} struct R ; impl X for R {}
2 fn foo ( v : i32 ) ->    impl X { if v == 0 { S } else { R } } // error

   To enable returning values of different types, Rust supports trait objects, which accompany
 values with virtual tables for dynamic dispatch. The type of a trait object is dyn X, where X is the
 implemented trait, as in the following example:
1 fn   foo ( v : i32 ) -> & ' static dyn X { if v == 0 { & S } else { & R } } // ok

 Note that a trait object is dynamically sized, i.e., its size is unknown at compile time, because values
 of different types can be stored. It is thus typically placed behind a pointer.

 2.3     Higher-Rank Polymorphism
 Rust supports rank-1 type polymorphism (e.g., generic functions), but not higher-rank type poly-
 morphism (e.g., functions that take generic functions). However, it supports higher-rank lifetime
 polymorphism because it is extremely useful when dealing with function pointers:
1 fn   foo < 'a >( v : & ' a i32 ) -> i32 { * v }
2 fn   bar < 'a >( f : fn (& ' a i32 ) -> i32 ) {{ let v =0; f (& v ) ;} { let u =1; f (& u ) ;}} // error
3 fn   baz ( f : for < 'a > fn (& ' a i32 ) -> i32 ) {{ let v =0; f (& v ) ;} { let u =1; f (& u ) ;}} // ok

 The function foo takes a reference of any lifetime (line 1). Another function may want to take a
 function pointer to foo and call it on references with different lifetimes. This cannot be achieved
 with rank-1 polymorphism: bar takes a function that accepts a reference of some lifetime, failing to
 pass both &v and &u (line 2). With higher-rank polymorphism, baz takes a function that accepts a
 reference of any lifetime, allowing both calls (line 3).
    Higher-rank polymorphism is also useful when reference types implement traits:
1 trait X { fn foo ( self ) ; }
2 fn bar <T >( mut v : T ) where for < 'a >
                                          &'a T: X {
3   { let u = v ; (& u ) . foo () ; v = u ;
                                          } { let w = v ; (& w ) . foo () ; } }
4 struct S ; impl < 'a > X for & ' a S { fn foo ( self ) {} } fn baz () { bar ( S ) ; }

 Using a higher-rank trait bound (HRTB), the function bar requires the type parameter T to satisfy
 the condition that &’a T implements X for any lifetime ’a (line 2). This allows the function body to
 call the method foo, which is provided by X, using references of different lifetimes (line 3). Since
 &’a S implements X for any lifetime ’a, baz can pass S to bar (line 4).

 3     Collecting Soundness Issues
 We collected rustc’s soundness issues reported between January 1, 2022, and September 1, 2025,
 focusing on issues pertinent to recent compiler releases. This timeframe aligns with the two most
 recent editions (boundaries for introducing backward-incompatible changes) of the language: Rust
 2021, released on October 21, 2021, and Rust 2024, released on February 20, 2025. Consequently,

                              Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
ISSTA129:6                                                               Yusung Sim, Sukyoung Ryu, and Jaemin Hong


our target timeframe encompasses over three and a half years, corresponding to the active use of
the Rust 2021 and 2024 editions.
   Since the issue tracker of the official GitHub repository for rustc contains various kinds of issues,
we filtered for soundness issues through automatic filtering based on the labels assigned to each
issue and manual inspection. We initially collected issues related to type checking by utilizing the
area labels (prefixed with “A-”), which indicate the issue-relevant compiler area, component, or
language feature. Specifically, we retained issues with the fourteen labels classified as type-related
ones by previous work [35]: A-type-system, A-inference, A-closures, A-coercions, A-const-generics,
A-DSTs, A-zst, A-trait-system, A-impl-trait, A-trait-objects, A-auto-traits, A-implied-bounds, A-
coinduction, and A-coherence. This yielded 969 issues.
   Since this set still includes issues other than soundness (e.g., bugs in documentation or non-bugs
like feature proposals), we further refined the dataset using two criteria. First, we kept only issues
marked with either C-bug or I-unsound, which signifies that the issue is a bug report or related to
type soundness. Second, we filtered out issues marked with specific labels indicating irrelevance to
soundness, which we categorize as follows:
• Documentation and tool issues: A-docs, A-rustdoc, A-rustdoc-json, A-rustdoc-ui, T-rustdoc, and
  A-clippy, which represent wrong documentation or issues in external tools.
• Diagnostics issues: A-diagnostics, A-suggestion-diagnostics, NLL-diagnostics, and const-generics-
  bad-diagnostics, which are pertinent to the quality of error messages.
• Alternative symptoms: I-crash, I-ICE, I-hang, I-compilemem, I-compiletime, and A-codegen,
  which represent symptoms like compiler crashes or performance issues.
• Non-bugs: C-tracking-issue, C-feature-request, and C-enhancement, which track discussions on
  certain features or represent feature proposals.
• Feature-gated features: labels prefixed with “F-,” which designate issues relevant only to language
  features guarded by feature gates.
This filtering process reduced the initial dataset to 320 issues.
   Then, we manually investigated each issue to determine whether it is a soundness issue based
on two criteria. First, we retained an issue only if it contained a Rust code snippet that the reporter
claimed the compiler should reject. Second, we excluded issues where the buggy behavior was not
caused by the compiler, e.g., those caused by breaking changes in the standard library. Through
this manual inspection, we identified 27 soundness issues.
   Finally, we checked whether each issue was a duplicate of another based on discussions among
rustc developers in the issue tracker. We identified 4 issues as duplicates of others already within our
dataset and subsequently excluded them. Additionally, 2 issues were duplicates of issues reported
before 2022; we chose to retain these, as their inclusion does not introduce redundancy within our
specific timeframe (see Table 4 for these issues and their original issue numbers). This resulted in a
dataset of 23 unique soundness issues.
   After the collection, we compared our dataset with that of Liu et al. [35], which classifies 22
issues as soundness issues. Our inspection shows that only 4 issues overlap across the two datasets,
while 19 are unique to ours and 18 are unique to the previous study. Among the 19 issues unique to
ours, 4 fall outside the timeframe of the previous study, 2 were classified under other bug categories,
3 were treated as duplicates, and 10 were excluded, although we could not find the reasons for
their exclusion in their paper or artifact. This shows that our study provides a more comprehensive
view of soundness issues, beyond an incremental contribution. Among the 18 issues unique to the
previous study, 8 have type-unrelated area labels, 1 lacks both C-bug and I-unsound labels, 8 have
“F-” labels, and 1 is a duplicate. We investigated the 9 issues (8 with type-unrelated labels and 1
with no C-bug/I-unsound label) and found that 7 satisfy our manual inspection criteria (a Rust code

Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
Rust’s Type Checker Implementation Is Unsound: An Empirical Study on Soundness Bugs in rustc                             ISSTA129:7


               Table 1. Classification of affected features and symptoms of soundness issues
          Affected feature         Symptoms
          Lifetimes                Missing lifetime checks, Anonymous lifetimes allowed
          Traits                   Overlapping impls, Missing dyn-compat checks, Orphan impls, Incorrect trait solving
          Type inference           Arbitrary type argument selection, Arbitrary hidden type selection
          Type well-formedness     Missing well-formedness checks
          Type cast                Incorrect type cast allowed

                          Table 2. Classification of consequences of soundness issues
               Consequence            Description
               Memory bug             A memory bug can occur at run time
               Breaking change        A benign change in a library can lead to a compilation error in a client code
               Inconsistency          A code snippet passes type checking while similar ones are rejected
               Misleading behavior    The run-time behavior could be misleading

                                 Table 3. Classification of status of soundness issues
             Status       Description
             Fixed        The compiler has been fixed, and the code snippet is rejected by the latest release (1.93.0)
             Confirmed    The C-bug or I-unsound label has been assigned to by a person other than the reporter
             Reported     The issue is open but not fixed or confirmed yet
             Non-bug      The issue has been closed without being fixed or confirmed

snippet that is claimed the compiler should reject, and buggy behavior caused by the compiler).
Therefore, we complemented our dataset with these 7 issues, resulting in the final dataset of 30
issues. See Table 4 for the issues that overlap with or were added from the previous study.

4     Soundness Issues in rustc
In this section, we classify the 30 soundness issues according to the affected feature and the
symptom and describe each category with simplified code snippets. When describing the issues,
we analyze the consequences, triggering features, and status as well. We identify five affected
features and ten symptoms, as shown in Table 1; we identify four consequences, as shown in
Table 2, and fourteen triggering features: implied bounds, associated types, impl traits (ITs),
RPITs, trait objects, higher-rank (HR) polymorphism, associated constants, function pointers (fn
ptrs), closures, recursive calls, asynchrony, try propagation, arrays, and enums (in tables, we
abbreviate them as shown in bold). Note that these affected/triggering features are not intended
to systematically enumerate all features in Rust; rather, they aid in understanding the soundness
issues we collected. We also classify status into four kinds, as shown in Table 3. Note that an issue
is considered fixed if the code given in the issue is rejected by the latest stable compiler, regardless
of its GitHub issue resolution status. We use this criterion because an issue may reveal multiple
compiler bugs and may not be closed even after the soundness bug has been fixed due to other
remaining bugs. Table 4 summarizes the characteristics of each issue. For the sake of brevity, we
only present code snippets for some issues; the omitted ones are available in our supplementary
material [52].

4.1    Lifetimes
4.1.1 Missing Lifetime Checks. In fourteen soundness issues, the compiler does not check lifetimes
properly. As explained in §2.1, a reference can be used wherever its lifetime outlives the expected
lifetime, and the compiler must check lifetimes when references are used to enforce this requirement.
If the compiler fails to check lifetimes, references may be used even after their lifetimes have ended,
incurring memory bugs like use-after-free. Among the fourteen issues, eight issues actually break
memory safety, while six issues do not result in such misuse of references despite missing lifetime
checks, only exhibiting inconsistent type checking results. We first discuss the memory-bug-
incurring issues and then the others.
    Issue 99158. In this issue, the compiler does not check implied bounds when coercing function
definitions to function pointers. In Listing 1, foo has the implied bound ’a: ’static due to its
second parameter (line 1). However, when bar assigns foo to f, this implied bound is not checked,

                            Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
ISSTA129:8                                                                             Yusung Sim, Sukyoung Ryu, and Jaemin Hong


                                               Table 4. Soundness issues in rustc
        Issue #     Affected Feature      Symptom                          Consequence           Triggers                 Status
        96460§      Type inference        Hidden type                      Inconsistency         RPIT                     Fixed
        96927       Type inference        Type argument                    Inconsistency         try                      Confirmed ¶
        98117§      Lifetimes             Missing lifetime checks          Memory bug            implied, tr obj          Fixed
        98543‡      Lifetimes             Missing lifetime checks          Memory bug            implied, assoc           Fixed
        99158∗      Lifetimes             Missing lifetime checks          Memory bug            implied, fn ptr          Confirmed
        99554       Traits                Orphan                           Breaking change assoc                          Fixed∗∗
        100051      Lifetimes             Missing lifetime checks          Memory bug            implied, assoc, HR       Reported
        104005§     Lifetimes             Missing lifetime checks          Memory bug            implied, tr obj          Fixed
        104763§     Lifetimes             Missing lifetime checks          Inconsistency         const                    Fixed
        104764§     Lifetimes             Missing lifetime checks          Inconsistency         assoc                    Fixed
        105251‡     Lifetimes             Missing lifetime checks          Inconsistency         assoc, RPIT              Fixed
        105787‡     Traits                Overlapping                      Inconsistency         assoc, HR                Fixed
        106040      Traits                Incorrect solving                Inconsistency         assoc                    Reported
        107268      Type inference        Type argument                    Inconsistency         assoc, fn ptr            Fixed
        108468      Lifetimes             Anonymous                        Inconsistency         IT, async                Reported
        109628      Lifetimes             Missing lifetime checks          Inconsistency         assoc                    Fixed
        110925      Type wf-ness          Missing wf-ness checks           Inconsistency         RPIT                     Reported
        111935‡     Type inference        Hidden type                      Inconsistency         RPIT, rec                Fixed
        112417      Lifetimes             Missing lifetime checks          Memory bug            implied, RPIT            Fixed
        114061      Traits                Overlapping                      Inconsistency         assoc, HR                Fixed
        114389†     Traits                Overlapping                      Memory bug            assoc, tr obj            Confirmed
        118876§     Lifetimes             Missing lifetime checks          Memory bug            implied, tr obj, HR, clo Fixed
        123312      Lifetimes             Missing lifetime checks          Inconsistency         clo                      Reported
        126079§     Traits                Missing dyn-compat checks Memory bug                   assoc, tr obj            Fixed
        133361      Traits                Overlapping                      Memory bug            assoc, tr obj            Fixed
        134311      Type inference        Hidden type                      Inconsistency         assoc, RPIT              Reported
        136508      Type cast             Incorrect cast                   Misleading            enum                     Reported
        139406      Type inference        Hidden type                      Inconsistency         RPIT, rec                Fixed
        141713      Lifetimes             Missing lifetime checks          Memory bug            assoc, HR, clo           Confirmed
        144045      Lifetimes             Missing lifetime checks          Inconsistency         arr                      Reported
                                           ∗ A duplicate of Issue 25860, which was reported in 2015.
                                           † A duplicate of Issue 57893, which was reported in 2019.
                                                    ‡ Overlaps between ours and Liu et al.’s.
                                                   § Added after comparison with Liu et al.’s.
¶ This issue was closed as a duplicate of Issue 94902, which is not itself a soundness issue but shares the same root cause. Since Issue 94902
                                  satisfies the “confirmed” criterion, Issue 96927 is classified as confirmed.
                                                   ∗∗ A warning occurs instead of an error.

and the assignment succeeds even though bar does not have ’a: ’static (line 3). By calling f,
bar can assign ’static to any reference; if this reference is not valid for the entire execution,
dereferencing it would lead to a memory bug. Note that explicitly adding the bound ’a: ’static to
foo causes the assignment to be rejected correctly.
   In six other issues, the compiler does not check implied bounds in other contexts and fails to
prevent memory bugs: it does not check implied bounds when a trait has a lifetime bound (Issue
98117), a self type (i.e., S in <S as X>::A) introduces implied bounds (Issues 98543 and 100051), an
implementing type in an impl introduces implied bounds (Issue 104005), an RPIT hidden type is
determined (Issue 112417), or a closure is coerced (Issue 118876).
   Issue 141713. In this issue, the compiler does not properly check the lifetime of the associated
type of an HRTB. In Listing 2, X<T> declares Fn() -> T as a supertrait, i.e., a type implementing X<T>
must also implement Fn() -> T (line 1). Fn() -> T is a built-in trait automatically implemented
by every closure that takes no parameters and returns T. It has an associated type named Output,
which is set to T. Additionally, every type implementing Fn() -> T also implements X<T> (line 2). In
foo, F has an HRTB, but it is unclear what F::Output denotes; the compiler allows using F::Output
as a reference with ’static in foo (line 3), while it allows using a reference with any lifetime as
F::Output in bar (line 4). Note that || &0 is a closure that takes no parameters and returns &0.
   Issue 144045. In this issue, the compiler does not check the lifetime of a length-0 array. In Listing 3,
foo returns [v; 1], which is a length-1 array with v as its element, and it is rejected because ’a does
not outlive ’static (line 1). On the other hand, bar is accepted, even though the only difference
from foo is that it returns [v; 0], which is a length-0 array (line 2). This issue does not cause
memory bugs because bar does not actually return any reference. Nevertheless, this behavior might

Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
 Rust’s Type Checker Implementation Is Unsound: An Empirical Study on Soundness Bugs in rustc                ISSTA129:9


1 fn   foo < 'a >( v : & ' a i32 , u : & ' static & ' a i32 ) -> & ' static i32 { v }
2 fn   bar < 'a >( v : & ' a i32 ) -> & ' static i32 {
3       let f : fn (& ' a i32 , _ ) -> & ' static i32 = foo ; f (v , &&0) }
                                               Listing 1. Issue 99158
1 trait   X <T >: Fn () -> T {}
2 impl <T , F : Fn () -> T > X <T > for F {}
3 fn foo <F >( v : F , u : F :: Output ) -> & ' static i32 where for < 'a > F : X <& ' a i32 >{ u }
4 fn bar < 'a >( v : & ' a i32 ) -> & ' static i32 { foo (|| &0 , v ) }

                                               Listing 2. Issue 141713
1 fn   foo ( v : & ' a i32 ) -> [& ' static i32 ; 1] { [ v; 1] } // error
2 fn   bar ( v : & ' a i32 ) -> [& ' static i32 ; 0] { [ v; 0] } // ok
                                               Listing 3. Issue 144045
1 trait  X <T > {}
2 fn foo ( v : impl X <& i32 >) {} // error
3 fn bar < 'a >( v : impl X <& ' a i32 >) {} // ok
4 async fn baz ( v : impl X <& i32 >) {} // ok

                                               Listing 4. Issue 108468

 seem surprising, as developers usually expect the type checking of array types to be independent
 of their lengths.
    Similarly, five other issues also reveal cases where the compiler does not check lifetimes but still
 prevents memory bugs. In particular, it does not check lifetimes when an associated constant or
 type is accessed (Issues 104763 and 104764), an RPIT has nested impl traits (Issue 105251), a type
 parameter’s associated type has a trait bound (Issue 109628), or a struct value is constructed inside
 a closure (Issue 123312).
 4.1.2 Anonymous Lifetimes Allowed. In one soundness issue, the compiler unexpectedly allows
 anonymous lifetimes. In Rust, when the compiler can automatically introduce necessary lifetime
 parameters according to predefined rules [61], programmers can use anonymous lifetimes. For
 example, foo and bar are equivalent in the following code:
1 fn   foo ( v : & i32 ) {} fn bar < 'a >( v : & ' a i32 ) {}
 However, anonymous lifetimes are explicitly disallowed in some contexts, and if the compiler
 allows them, it may be considered a soundness bug.
    Issue 108468. In this issue, using an async function causes the compiler to allow anonymous
 lifetimes. In Listing 4, the function foo is rejected because anonymous lifetimes must not occur
 in impl traits (line 2), while bar is accepted (line 3). However, the async function baz passes type
 checking even though it contains an anonymous lifetime in an impl trait (line 4).

 4.2     Traits
 4.2.1 Overlapping Implementations. In four soundness issues, the compiler allows overlapping
 impls, i.e., those implementing the same trait for the same type. Rust prohibits overlapping impls
 because they create ambiguity when deciding which impl to use during method resolution. For
 example, the following code is rejected:
1 trait    X { fn foo ( self ) -> i32 ; } struct S ;
2 impl    X for S { fn foo ( self ) -> i32 {0}} impl X for S { fn foo ( self ) -> i32 {1}} // error
 Therefore, if code with overlapping impls passes type checking, it can be considered a soundness
 bug. Among the four issues in this category, two lead to memory bugs, while two only cause
 inconsistency.
   Issue 114389. In this issue, the compiler allows a user-defined impl to overlap with a built-in
 impl—for every trait X, the type dyn X automatically implements X, called a built-in impl. In Listing 5,
 every type implements X, even including dynamically sized types due to the bound ?Sized on T

                             Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
 ISSTA129:10                                                              Yusung Sim, Sukyoung Ryu, and Jaemin Hong


1 trait    X { type A ; } impl < T : ? Sized > X for T { type A = & ' static i32 ; }
2 fn   foo < T : ? Sized >( v : <T as X >:: A ) -> & ' static i32 { v }
3 fn   bar < 'a >( v : & ' a i32 ) -> & ' static i32 { foo :: < dyn X < A = & ' a i32 > >( v ) }
                                                Listing 5. Issue 114389
 (line 1). In foo, since <T as X>::A and &’static i32 are the same type, it can return the given value
 as is (line 2). On the other hand, when bar calls foo, the type argument is dyn X<A = &’a i32>, so
 the parameter type <T as X>::A becomes &’a i32. Consequently, bar can use a value of &’a i32 as
 &’static i32 by passing it to foo (line 3). This issue arises because dyn X<A = &’a i32> has two
 overlapping impls of X: the one with A = &’static i32 defined in line 1 and the built-in impl with
 A = &’a i32.
    In another issue (Issue 133361), two user-defined impls for trait objects overlap and similarly
 incur memory bugs by setting the same associated type to two different types. In two other issues,
 the compiler fails to detect overlapping impls when higher-rank polymorphism is involved, but
 memory bugs do not occur because the compiler always selects one impl and ignores the other
 (Issue 105787), or when the associated type is used, the compiler recognizes that two different types
 are possible and rejects the code (Issue 114061).
 4.2.2 Missing Dyn-compatibility Checks. In one soundness issue (Issue 126079), the compiler
 does not check the dyn-compatibility of a trait. To use a type dyn T, the trait T must satisfy
 dyn-compatibility, which requires several conditions, such as not having a method return type
 containing Self. However, the compiler does not check dyn-compatibility when an associated type
 of a supertrait, referred to using Self, is used as a return type. This allows a single return type to
 be interpreted as two different types, leading to memory bugs.
 4.2.3 Orphan Implementations. In one soundness issue, the compiler allows orphan impls, i.e.,
 those implementing external traits for external types. In Rust, a crate is a compilation unit, and
 items defined in other crates are considered external. If orphan impls are allowed, a seemingly
 innocent change in a library can prevent a dependent program from compiling:
1 // crate a
2 trait X {}   struct S ;
3 // crate b   ( depends on crate a )
4 trait Y {}   struct R ;
5 impl a :: X for a :: S {} // error
6 impl a :: X for R {} impl Y for a :: S {} // ok

 While the crate a currently does not implement X for S, it can freely add an impl in the future. If the
 crate b is allowed to implement X for S, such an update in a becomes an abrupt breaking change,
 making b uncompilable due to two overlapping impls of X for S. To prevent this in advance, the
 orphan implementation is rejected (line 5), while implementing X for its own type R or its own
 trait Y for S is accepted (line 6). Therefore, the issue in this category leads to a failure in preventing
 future breaking changes.
    Issue 99554. In this issue, the compiler allows an orphan impl when an associated type is used. In
 Listing 6, a defines X (line 2). In b, implementing X for any type T that implements Y is considered
 orphan and correctly rejected, as such T can be external (line 5). However, writing <T as Y>::A,
 which is equivalent to T, causes the compiler to accept the impl (line 6).
 4.2.4 Incorrect Trait Solving. In one soundness issue, the compiler draws an incorrect conclusion
 in trait solving, i.e., deciding whether a given type implements a certain trait.
    Issue 106040. In this issue, trait solving succeeds despite the existence of cyclic requirements
 when associated types have trait bounds. In Listing 7, the compiler needs to determine whether S
 implements Unpin (line 4), where Unpin is a trait defined in the standard library. This requires S:
 X<A = S> (line 3), which in turn requires S: Unpin (line 2), forming a cycle. However, the compiler

 Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
 Rust’s Type Checker Implementation Is Unsound: An Empirical Study on Soundness Bugs in rustc             ISSTA129:11


1 //   crate a
2 trait X <T , U > {}
3 // crate b
4 struct S ; trait Y          { type A ; } impl <T > Y for T { type A = T ; }
5 impl < T :   Y > a :: X <S , T > for T {} // error
6 impl < T :   Y > a :: X <S , T > for <T as Y >:: A {} // ok
                                              Listing 6. Issue 99554
1 trait   X {    type A where Self : Unpin ; }
2 impl <T > X    for T { type A = T where T : Unpin ; }
3 struct S ;     impl Unpin for S where S : X < A = S > {}
4 fn foo < T :   Unpin >() {} fn bar () { foo :: <S >() }
                                              Listing 7. Issue 106040
1 fn foo <T >() -> Option <T > { None }
2 fn bar () -> Option < i32 > { foo () ; None } // error
3 fn baz () -> Option < i32 > { foo () ?; None } // ok

                                              Listing 8. Issue 96927
 concludes that S implements Unpin and accepts the entire program. This result can be considered
 inconsistent because the compiler successfully detects the cycle and rejects the code when the
 bound is directly applied to the type parameter, instead of the associated type, as follows:
2 impl < T :   Unpin > X for T { type A = T ; }


 4.3    Type Inference
 4.3.1 Arbitrary Type Argument Selection. In two soundness issues, the compiler arbitrarily chooses
 a type argument during type inference even when multiple types are possible. In Rust, type inference
 of a type argument should succeed only when the possible type is unique. In the following example,
 foo(0) is accepted because i32 is the only possible type, while baz() is rejected because any type
 would be valid:
1 fn   foo <T >( t : T ) {} fn bar () { foo (0) ; } // ok
2 fn   baz <T >() {} fn qux () { baz () ; } // error
 If the compiler arbitrarily chooses one among multiple possible types, it can be considered incon-
 sistent, and the run-time behavior may deviate from the developer’s expectation.
    Issue 96927. In this issue, type inference selects an arbitrary type when the try propagation
 operator (?) is used. In Listing 8, foo returns Option<T>, which expresses the optional existence
 of a value, allowing Some(v) for a value or None for no value (line 1). Since bar does not use the
 return value, the type argument can be any type, and type inference fails (line 2). On the other
 hand, baz uses ?, which immediately returns None if the result is None and extracts the inner value
 otherwise (line 3). The compiler still has no information about the type, but chooses an arbitrary
 one—! (signifying that the function never returns) in recent versions, or () (the empty tuple) in
 older versions—and accepts the code.
    In another issue (Issue 107268), the compiler chooses an arbitrary type as a type argument when
 a function with a lifetime parameter is coerced to a function pointer.
 4.3.2 Arbitrary Hidden Type Selection. In four soundness issues, type inference chooses an arbitrary
 type as the hidden type for an RPIT even when multiple types are possible. Such issues are also
 considered inconsistent and may lead to unexpected run-time behavior.
    Issue 139406. In this issue, type inference selects an arbitrary hidden type when recursive calls
 exist. The function foo passes the result of a recursive call to another recursive call (line 2). While
 both T and ! are valid choices, the compiler chooses T and accepts the code.
    In three other issues, the hidden type is arbitrarily selected when a built-in type PhantomData
 (Issue 96460), recursive calls (Issue 111935), or associated types (Issue 134311) are involved.

                            Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
    ISSTA129:12                                                              Yusung Sim, Sukyoung Ryu, and Jaemin Hong


1 trait       X {} impl <T > X for T {}
2 fn      foo <T >( v : T ) -> impl X { foo :: <T >( foo :: <T >( v ) ) }
                                                   Listing 9. Issue 139406
1 trait       X <T > {} impl <T > X <T > for i32 {} trait Y {} struct S < T : Y >( T ) ;
2 fn      foo () -> impl X <S < i32 > > { 0 } // ok
3 fn      bar ( v : impl X <S < i32 > >) {} // error
                                                  Listing 10. Issue 110925
1 enum E {        A } enum F { B ( i32 ) }
2 fn foo ()       { let x = E :: A as i32 ; // ok
3                   let y = F :: B (0) as i32 ; // error
4                   let z = F :: B as i32 ; } // ok
                                                  Listing 11. Issue 136508


    4.4     Type Well-formedness
    Issue 110925. In this issue, the compiler does not check the well-formedness of a type in an RPIT.
    In Listing 10, S<i32> is not well-formed because no type implements Y, while S<T> requires T: Y
    (line 1). However, foo is accepted despite using S<i32> in the RPIT (line 2). The compiler rejects
    the use of S<i32> in other contexts, including APITs (line 3). This inconsistency does not lead to
    memory bugs because a value of S<i32> cannot be constructed.

    4.5     Type Cast
    Issue 136508. This issue allows casting an enum constructor to an integer. In Rust, an enum consists
    of multiple variants, each of which may have associated data. In Listing 11, E has one variant A
    without data, and F has one variant B with an i32 value (line 1). Rust allows casting E::A, which
    has no data, to an integer (line 2), but disallows casting F::B(0), which contains data (line 3).
    Somewhat surprisingly, casting F::B to an integer is accepted (line 4). In fact, this behavior is
    intended according to the Rust Reference, as F::B is an enum constructor and treated as a function;
    casting it to an integer gives its address. However, the reporter of this issue claims that this behavior
    is misleading because a developer might attempt to cast F::B under the mistaken impression that it
    is a variant without data.

    5     Findings from Soundness Issues
    In this section, we discuss findings from the collected soundness issues by answering the following
    research questions:
    • RQ1. Symptoms and Consequences: What are the symptoms and consequences of soundness
      issues?
    • RQ2. Triggering Features: Which language features trigger soundness issues?
    • RQ3. Bug Consensus: For which soundness issues is there consensus that they are bugs?
    • RQ4. Issue Lifecycles: How long does it take to discover and fix soundness issues?

    5.1     RQ1. Symptoms and Consequences
    Table 5 shows the number of soundness issues per symptom and affected feature (the two rightmost
    columns), while also displaying how often each symptom leads to each consequence (the four
    middle columns). Lifetimes are the most frequently affected feature (15 issues), followed by traits (7
    issues) and type inference (6 issues). In terms of the symptoms, missing lifetime checks are the most
    common (14 issues), followed by overlapping impls (4 issues) and arbitrary hidden type selection (4
    issues). The issues mainly lead to inconsistencies (17 issues) and memory bugs (11 issues).

    Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
Rust’s Type Checker Implementation Is Unsound: An Empirical Study on Soundness Bugs in rustc                    ISSTA129:13


                           Table 5. Symptoms and consequences of soundness issues
                                                                         Consequence
                                                                                                            Total
                                                         Memory    Breaking Inconsistency     Misleading
                               Missing lifetime checks        8           0             6              0   14
                  Lifetimes                                                                                          15
                               Anonymous lifetimes            0           0             1              0    1
                               Overlapping impls              2           0             2              0    4
                               Missing dyn-cmpt checks        1           0             0              0    1
                  Traits                                                                                             7
      Symptom                  Orphan impls                   0           1             0              0    1
                               Incorrect trait solving        0           0             1              0    1
                               Type argument                  0           0             2              0    2
                  Inference                                                                                          6
                               Hidden type                    0           0             4              0    4
                  Wf-ness      Missing wf-ness checks         0           0             1              0    1        1
                  Cast         Incorrect cast                 0           0             0              1    1        1
                            Total                            11           1            17              1        30



                                 Table 6. Triggering features of soundness issues
                                                              Triggering Feature
                                                                                                            Total
                                    implied assoc IT RPIT tr obj HR const fn ptr clo rec async try arr enum
                      Lifetimes           7     6 1     2      3 3      1      1 3 0         1 0 1        0   15
                      Traits              0     7 0     0      3 2      0      0 0 0         0 0 0        0     7
        Affected      Inference           0     2 0     4      0 0      0      1 0 2         0 1 0        0     6
                      Wf-ness             0     0 0     1      0 0      0      0 0 0         0 0 0        0     1
                      Cast                0     0 0     0      0 0      0      0 0 0         0 0 0        1     1
                      Memory              7     6 0     1      6 3      0      1 2 0         0 0 0        0   11
                      Breaking            0     1 0     0      0 0      0      0 0 0         0 0 0        0     1
        Consequence
                      Inconsistency       0     8 1     6      0 2      1      1 1 2         1 1 1        0   17
                      Misleading          0     0 0     0      0 0      0      0 0 0         0 0 0        1     1
                  Total                   7    15 1     7      6 5      1      2 3 2         1 1 1        1   30



                                        Table 7. Status of soundness issues
                                                                    Status
                                                                                               Total
                                                    Fixed   Confirmed Reported      Non-bug
                                    Memory              7           3        1            0       11
                                    Breaking            1           0        0            0        1
                    Consequence
                                    Inconsistency      10           1        6            0       17
                                    Misleading          0           0        1            0        1
                                Total                  18           4        8            0       30




   Finding 1. The Rust compiler has soundness issues that lead to memory bugs, caused
by missing lifetime checks or overlapping impls. Although not all soundness issues result
in memory bugs, 11 of them do. Among these, 8 are caused by missing lifetime checks, which
is expected as lifetimes are key to enforcing the valid use of pointers. On the other hand, 2 are
caused by overlapping impls, and 1 is caused by missing dyn-compatibility checks. The primary
role of traits is to enable polymorphism, which is not directly relevant to pointer usage. However,
overlapping impls and missing dyn-compatibility checks may allow a single type to be interpreted
as different types, and such type confusion can result in memory bugs. This shows that the research
community should recognize the importance of the trait system in ensuring memory safety, whereas
previous studies [27, 63] have mainly focused on formalizing the ownership and borrowing system,
including lifetimes.
   Finding 2. Rust programmers often believe that the compiler should ensure consistency
by rejecting even programs that do not incur memory bugs. For example, type inference
choosing an arbitrary type cannot cause memory bugs. Nevertheless, many developers expect the
compiler to reject such cases, following the consistent rule that inference should succeed only
when a unique valid type exists. Similarly, in Issue 144045, although empty arrays cannot carry
any pointers, which is a valid reason for lifetime checks to be exempted, developers may expect
them to be treated in a way consistent with non-empty arrays.

                            Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
ISSTA129:14                                                              Yusung Sim, Sukyoung Ryu, and Jaemin Hong


5.2   RQ2. Triggering Features
Table 6 shows the number of issues that require each feature as a trigger, grouped by affected
features (the upper five rows) and consequences (the lower four rows). Note that the rightmost
column does not show the sum of the numbers in the middle columns; it shows the number of issues
in each row, which is identical to the totals in Table 5. Associated types are the most frequently
involved feature (15 issues), followed by implied bounds (7 issues), RPITs (7 issues), and higher-rank
polymorphism (5 issues).
   Finding 3. Compiler developers should carefully handle associated types wherever they
can occur. Half of the issues require associated types as a trigger. However, it is relatively rare that
associated types alone cause soundness issues; rather, they often become a way to exploit edge
cases when using other features. For example, in Issue 99554, using an associated type instead of
the type itself causes the compiler to fail to detect an orphan impl. Therefore, developers should
consider the possibility of using associated types with caution.
   Finding 4. The interaction between orthogonal features, especially lifetimes and traits,
makes it difficult for type checking to be sound. Most issues that affect lifetimes require
trait-related features as triggers: associated types in 6 issues, impl traits in 1 issue, and RPITs in
2 issues. This shows that correctly implementing lifetime checks becomes especially challenging
when traits are involved. Therefore, future work is encouraged to study lifetimes and traits in a
unified manner, instead of treating them separately.
   Finding 5. Correct treatment of implied bounds and trait objects is extremely important
in ensuring memory safety. Implied bounds are involved in 7 issues, all of which lead to memory
bugs. Implied bounds are automatically introduced by the compiler; to retain memory safety,
rustc developers should carefully validate that all the implied bounds introduced at the definition
site are also checked at the use site. As existing formalizations of the borrowing system [27, 63]
do not include implied bounds, this result suggests that they should be considered in future
research. Similarly, trait objects trigger 6 issues, all of which lead to memory bugs. As trait objects
automatically introduce built-in impls, they make the detection of overlapping impls even more
challenging. Although Milewski [37]’s formalization of the trait system includes coherence rules,
the rules do not cover trait objects, necessitating future work to address this gap.
   Note that we do not claim that soundness issues involving specific features are necessarily
disproportionate. Lifetimes and traits are pervasively used in real-world Rust programs, which
may be one reason why they are prevalently involved in soundness issues. We believe this does
not undermine, but rather emphasizes, the importance of our findings; if they are frequently used,
related soundness issues are especially critical and require more attention.
   These findings are mostly specific to Rust, rather than applicable to programming languages in
general, due to Rust’s unique features. Notably, lifetimes have no equivalents in other mainstream
languages, and traits resemble type classes in Haskell but have no exact equivalents in object-
oriented languages. For example, bug categories from a study on compiler bugs in JVM-targeting
languages [9] include incorrect inference and incorrect coercion, but nothing corresponding to
lifetimes or traits.

5.3   RQ3. Bug Consensus
Table 7 shows the number of issues with a certain status per consequence. Overall, 18 have been
fixed, 4 have been confirmed, 8 have been reported, and none are non-bugs. Among 12 issues that
lead to memory bugs or breaking changes, 11 have been fixed or confirmed, indicating that they
are real bugs. This is not surprising because memory safety is the main goal of Rust, and breaking
changes are caused by a clear violation of orphan rules.

Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
Rust’s Type Checker Implementation Is Unsound: An Empirical Study on Soundness Bugs in rustc             ISSTA129:15


                Table 8. Statistics regarding the lifecycles of the soundness issues (in days)
                                                          All                            Fixed
                                   Testable-Introduced      Introduced-Discovery    Discovery-Fixed
                       Minimum                        0                         1                 2
                       Maximum                    2,813                     3,552               855
                       Median                       855                     1,079               345
                       Average                      866                     1,291               324




Fig. 1. Lifecycles of the soundness issues. Each row shows one issue: gray dashed lines indicate the period
before introduction, solid black lines indicate the period from introduction to fix or study end, red markers
indicate discovery dates, and the vertical dashed line marks the start of issue collection.

   Finding 6. The rustc developers are inclusive in discussing soundness issues even when
they do not lead to memory bugs. Among 18 issues that lead to inconsistencies and misleading
behavior, only 11 have been fixed or confirmed. Nevertheless, none of the remaining issues have
been classified as non-bugs. This may reveal the community’s inclusive nature in judging soundness
bugs. A notable example is Issue 136508, where an enum constructor can be cast to an integer. Even
though the Rust Reference explicitly describes this behavior and one developer clarified this point
in the discussion, the issue remains open, and another developer even added the T-lang, T-compiler,
and A-coercions labels.

5.4   RQ4. Issue Lifecycles
We analyze the lifecycle of each issue by identifying stable releases of rustc where it is testable,
introduced, or fixed. The earliest testable version is the one where the immediately preceding
version rejects the code with a message that a feature is unstable; the introduction version is the
earliest stable release in which the issue can be triggered. We tested each version of rustc against
each code snippet to find these versions. In addition, we determine the discovery date as the issue’s
creation date. A few exceptions to these criteria are: (1) Issues 96460 and 105251 are not reproducible
in stable releases, so we identify the nightly versions where the issue occurs; (2) Issues 99158 and
114389 are duplicates of 25860 and 57893, respectively, so we refer to the earlier ones to avoid
considering their discovery dates absurdly late.
   Table 8 summarizes the statistics regarding the lifecycles of the soundness issues. The two
middle columns present the statistics of the durations (in days) from the earliest testable version to
introduction and from introduction to discovery for all 30 issues. The rightmost column reports
the statistics for the durations from discovery to fix for the 18 fixed issues.
   Fig. 1 visualizes the lifecycles of the soundness issues. The x-axis represents time, starting from
the release of rustc 1.0.0, with the vertical dashed line at 2022 marking the beginning of our issue

                           Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
ISSTA129:16                                                              Yusung Sim, Sukyoung Ryu, and Jaemin Hong


collection period. For each issue arranged along the y-axis, gray dashed lines span the duration
from the earliest testable version to the introduction, and solid black lines span the duration from
the introduction to the fix or the end of the collection period. Finally, red vertical markers denote
the discovery dates.
   Finding 7. Soundness issues are typically discovered long after they are introduced,
persisting across multiple releases. The discovery of these issues took an average of 1,291 days,
with a maximum of 3,552 days. Soundness issues are particularly difficult to identify because they
often require peculiar combinations of multiple language features that developers rarely exercise
in practice, and allow compilation to succeed silently, not necessarily accompanied by immediately
observable problems. These results indicate a critical need for systematic testing techniques to
detect soundness issues in rustc.
   Finding 8. New features are often stabilized before undergoing sufficient testing. Seven
issues (96927, 98543, 100051, 106040, 107268, 108468, and 110925) were introduced simultaneously
with the stabilization of the features required to trigger them. Before stabilizing new features,
compiler developers must ensure the soundness of the type checker, specifically by investigating
potential interactions between the new feature and existing language constructs.
   We believe Findings 7 and 8 are general phenomena across different programming languages,
and our contribution is to empirically confirm that they also apply to Rust. These findings are
especially meaningful given Rust’s emphasis on type soundness.

6     Potential Oracles for Testing Type Soundness
6.1    Implementations
6.1.1 AddressSanitizer and Miri. AddressSanitizer [47] is a memory bug detector based on instru-
mentation, and Miri [28, 59] is a Rust interpreter designed to detect undefined behavior, including
memory bugs. They can serve as test oracles by checking whether a program that passes type
checking incurs a memory bug during execution. However, since type checking is outside their
scope, they cannot identify soundness bugs that do not manifest as undefined behavior.
   To empirically validate their effectiveness, we applied them to the code from the eleven soundness
issues that result in memory bugs. In our experiments, both AddressSanitizer and Miri successfully
detected memory bugs in all cases. Therefore, using AddressSanitizer or Miri as a test oracle is
a promising direction, although complementary tools are necessary to cover a broader range of
soundness bugs.
6.1.2 Chalk. Chalk [57] is an experimental trait solver that serves as a prototyping ground for
designing and improving the trait solver in rustc. It determines whether certain impls are overlap-
ping or orphan and whether a given type implements a specific trait. Chalk approaches these tasks
in a fundamentally different way from rustc; it models Rust declarations using logical predicates
and performs checks by solving logical formulas. Thus, it is reasonable to utilize Chalk as a test
oracle to discover trait-related soundness bugs. However, since Chalk targets only the trait system,
other type system features remain outside its scope.
   To assess its effectiveness, we applied the latest version (0.104.0) to the seven trait-affecting
issues (99554, 105787, 106040, 114061, 114389, 126079, and 133361). Unfortunately, Chalk currently
cannot express Issue 106040 because it does not support associated types with bounds in impls.
For the remaining issues, Chalk correctly identified the orphan impl in Issue 99554 and the dyn-
compatibility violation in Issue 126079; it also rejected Issue 105787, but the message incorrectly
cited an orphan impl rather than overlapping impls; it crashed on Issue 114061 and accepted Issues
114389 and 133361. Consequently, we conclude that Chalk is yet immature for use as a practical
test oracle.

Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
    Rust’s Type Checker Implementation Is Unsound: An Empirical Study on Soundness Bugs in rustc             ISSTA129:17


1[    crate a { trait X < ty T , ty U > {} } ,
2     crate b { struct S {}
3               trait Y { type A : []; }
4               impl < ty T > Y for T { type A = T ; }
5               impl < ty T > X <S , T > for <T as Y >:: A where T : Y {} } ]
                                      Listing 12. Issue 99554 in a-mir-formality


       To facilitate its realistic use as an oracle for trait-related soundness bugs, we suggest improving
    its robustness and correctness by testing it with diverse inputs. As Chalk targets only the trait
    system, we do not consider it a general oracle that can cover all kinds of soundness bugs, and we
    do not suggest extending it to cover features irrelevant to traits.

    6.1.3 a-mir-formality. The a-mir-formality project [56] aims to develop an executable formal model
    of the Rust type system, which can decide whether a given program should pass type checking
    or not. As its scope is not limited to a specific part of the type system, we believe it has strong
    potential to become a comprehensive test oracle for type soundness.
       To validate its effectiveness, we applied a-mir-formality at commit ab4f18e to the collected
    soundness issues. As a-mir-formality defines its own syntax, we manually rewrote the code; for
    top-level items, its syntax is close to Rust’s; for function bodies, it follows MiniRust [54], which
    resembles the mid-level intermediate representation (MIR) used in rustc. For example, Listing 12
    shows the code for Issue 99554 rewritten in a-mir-formality, where a single program consists of a
    list of crates and a type parameter is introduced with the keyword ty. While rewriting the code, we
    found that it currently supports only a subset of Rust and MiniRust; it lacks support for implied
    bounds, impl traits, trait objects, function pointer types, closures, asynchrony, array types, and
    casts. Furthermore, the ? operator cannot be used because it exists only at the surface level and is
    desugared when code is lowered to MIR. As a result, we could express code snippets for only five
    issues (99554, 98117, 106040, 109628, and 114061). In our experiments, a-mir-formality rejected three
    (99554, 98117, and 109628) but accepted the others. Therefore, we conclude that a-mir-formality is
    also currently immature for practical use.
       To leverage its strong potential as an oracle, we suggest supporting more features. We believe
    important features to prioritize include implied bounds, impl traits, and trait objects.

    6.2   Documentation
    In this section, we describe holes in the existing documentation, focusing primarily on the Rust
    Reference [60] and the FLS [58], while also referring to Rust RFCs [62] where appropriate. Both the
    Reference and the FLS describe the syntax in BNF and provide brief explanations for each syntactic
    construct. While the Reference has been maintained as an official Rust project for many years, the
    FLS was initially developed by Ferrous Systems and AdaCore for use in safety-critical industries
    before being adopted as a Rust project in 2025 [12]. Although their explanations overlap in many
    areas, the level of detail provided for specific features often varies between them. On the other
    hand, RFCs comprise a collection of proposed changes to the language. As discussed below, certain
    features are explained in detail only within RFCs even after their stabilization. While investigating
    these documents, we reviewed all sections containing relevant keywords by utilizing the search
    functionality on their websites, avoiding incorrectly claiming that certain information is missing.
       Note that the purpose of this discussion is to demonstrate that constructing a mechanized
    specification for Rust cannot be achieved simply by collecting existing documents; rather, it requires
    significant effort to fill these holes. Our goal is not to criticize existing documents; they were not
    intended to serve as specifications and remain valuable for providing intuitive understanding. Since

                               Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
ISSTA129:18                                                              Yusung Sim, Sukyoung Ryu, and Jaemin Hong


we only aim to demonstrate that the current documentation contains some holes, our discussion
does not systematically cover every language feature.
    Implied bounds and well-formedness. The Reference explains implied bounds by stating that
“lifetime bounds required for types to be well-formed are sometimes inferred,” but it does not
define what well-formed types are. Similarly, the FLS does not provide a precise explanation
of implied bounds, stating only that “an implied bound is . . . the byproduct of relations between
lifetime parameters and function parameters . . . ” without further clarification on how such relations
introduce bounds as a byproduct. The definition of well-formedness exists only in RFCs, notably
RFC 1214 projections-lifetimes-and-wf [55]. This RFC defines well-formedness using inference
rules based on its own syntax for Rust types. Unfortunately, this syntax lacks several types present
in Rust, most notably impl trait types. Furthermore, some inference rules are unclear; e.g., one rule
includes the premise (’x: ’a) in Env, yet Env is never formally defined.
    Coercion. In Issue 99158, coercion from a function item to a function pointer breaks type soundness.
The Reference defines this kind of coercion vaguely, stating only that “coercion is allowed . . . [from]
function item types to fn pointers.” The explanation in the FLS is more refined, specifying that
coercion is permitted when “the source’s function signature is a subtype of the target’s function
signature.” The FLS further defines the subtyping of function pointer types (presumably including
function item signatures) using the standard notion of variance, where they are contravariant in
their parameter types and covariant in their return types. However, this definition does not cover
higher-rank cases, where functions have type or lifetime parameters, possibly accompanied by
bounds. Consequently, it remains unclear whether coercing generic functions to function pointers
requires specific checks for their bounds or permits the substitution of these parameters with
concrete types or lifetimes.
    HRTBs and associated types. In Issue 141713, the use of the type path F::Output triggers the
problem, where F has an HRTB. We searched the documentation using the keywords “higher-
rank,” “associated type,” and “type path” to determine how an associated type projected from a
type parameter with an HRTB should be interpreted. Unfortunately, we found explanations only
for HRTBs and associated types in isolation, with no documentation regarding their interaction.
Notably, the description of how a type path is resolved to a type is insufficient even when HRTBs
are not involved. The Reference defines the syntax of type paths in its “Paths” section but does
not explain their resolution process. The FLS includes an “Entities and Resolution” section, which
states that <S as T>::A “resolves to the associated type of S’s trait implementation of trait T.”
However, it provides no information regarding the resolution of type paths that lack such explicit
trait disambiguation.

7   Threats to Validity
The primary threat to external validity resides in the selection criteria and the representativeness
of the collected issues. We are certain that all 30 issues are indeed soundness issues because we
studied each in depth; readers can also validate this claim by reviewing the code snippets in our
supplementary material [52] or the issues themselves on GitHub, as the dataset size is manageable.
However, additional soundness issues may exist that were missed due to our conservative selection
criteria. The automatic filtering process relied on GitHub labels; although these labels are routinely
assigned by rustc developers, some issues might not have been properly labeled at the time of
collection. While we followed the classification used in prior work [35] to identify labels related
to type checking, other relevant labels might have been overlooked. Moreover, we filtered out
issues with labels that appeared irrelevant to soundness, but it is possible that a soundness issue
also revealed other problems and was thus excluded. Notably, as mentioned in §3, 7 issues in the
dataset of the previous work were excluded by our filtering due to their labels, confirming the

Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
Rust’s Type Checker Implementation Is Unsound: An Empirical Study on Soundness Bugs in rustc             ISSTA129:19


risk of missing soundness issues. Even though we complemented our dataset with these 7 specific
issues, other soundness issues might have been missed for the same reason. Finally, our manual
scan retained issues only if they provided clear evidence that the expected behavior was rejection,
which could exclude less-documented cases. Nevertheless, even if the dataset is not exhaustive, we
believe our findings remain valid as they are derived from actual soundness issues.
   Regarding this threat, we conducted a lightweight study of issues excluded due to the I-ICE label,
which indicates that the compiler crashes because of an internal compiler error (ICE). We found
that 181 excluded issues have the I-ICE label, while only one of them also has the I-unsound label.
As a soundness issue is not necessarily marked with I-unsound, this does not strictly mean that
all except one are not soundness issues. That said, we believe this result suggests that most I-ICE
issues are unlikely to be soundness issues. The primary reason is that an ICE prevents code from
compiling, while soundness issues require code that should not type-check to compile successfully.
   Another threat to external validity stems from the exclusion of issues related to feature-gated
features. Inspecting such issues would reveal additional soundness issues, especially considering
that unstable features likely have more compiler bugs than stable features. We found that among
223 issues excluded due to an “F-” label, 10 issues also have I-unsound, corroborating this expecta-
tion. However, we believe that focusing on soundness issues within stable features helps better
understand the severity of soundness issues in rustc.
   A threat to construct validity concerns the accuracy of our characterization of features, symptoms,
consequences, and bug status. The identification of these attributes is inherently susceptible to
researcher bias or human error. To mitigate this, we employed three strategies. First, two authors
independently investigated the issues and conducted extensive discussions to reach a consensus on
the characterization of each issue. Second, we cross-referenced each issue with multiple external
resources, including related issues, PRs, and discussions on the official Rust Zulip channels, as well
as documents such as the Reference, the FLS, and RFCs. Third, we designed objective criteria for
bug status and checked the status by type-checking each code using the latest rustc release and
inspecting issue labels and their assigners.
   Finally, a threat to conclusion validity lies in the small size of the dataset, which limits the
generalizability of our findings. Nevertheless, we believe our work provides value to the commu-
nity. Our main contribution is reporting that rustc has soundness bugs despite Rust’s emphasis
on type soundness, highlighting the urgent need for research community efforts. Our in-depth,
multidimensional analysis yields actionable insights that facilitate future research on testing the
Rust type checker and formalizing the type system.


8     Related Work
8.1    Studying Compiler Bugs
Previous work has investigated bugs in Rust compilers, analyzing a wide range of issues; in contrast,
this work focuses specifically on soundness bugs. Xia et al. [66] analyzed historical bugs in two
Rust compilers, rustc and rust-gcc [45]. They identified type checking as the most bug-prone
component in both compilers, along with method resolution and IR processing. Yu and Wang [71]
examined bug reports and their corresponding revisions in the rustc GitHub repository. They
found that traits and ownership are the primary Rust-specific features involved in compiler bugs.
Their analysis of bug symptoms revealed that internal compiler errors (ICEs) are the most prevalent,
with soundness issues ranking as the second most frequent occurrence. Liu et al. [35] investigated
rustc bugs across various compiler components. Their study identified type system errors as the
leading cause of bugs, with errors related to trait bounds and opaque types representing the largest


                           Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
ISSTA129:20                                                              Yusung Sim, Sukyoung Ryu, and Jaemin Hong


share. Furthermore, they found that a significant portion of bugs are correctness issues, including
completeness and soundness issues, which constitute the most frequent symptom after crashes.
   Researchers have also studied compiler bugs in domains other than Rust. Notably, they have
covered GCC and LLVM [53], WebAssembly [44], JVM-targeting languages, including Java, Scala,
Kotlin, and Groovy [9], Solidity [33], and deep learning compilers [15, 50].
   A notable previous study discovered new compiler bugs instead of analyzing bugs from pro-
grammers. Amin and Tate [4] presented soundness bugs in Java and Scala, where they utilized
null pointers with existential types to enable casting between arbitrary types without relying on
built-in downcasting. They noted that the identified unsoundness results from the interaction of
different language features, aligning with our findings.

8.2    Formalizing the Rust Type System
While this work investigates existing documents, including the Reference, the FLS, and RFCs,
researchers have formalized the type system for various subsets of Rust, which may aid the con-
struction of a mechanized specification in the future. Jung et al. [27] proposed RustBelt, formalizing
Rust’s ownership and borrowing type system by defining the core language 𝜆𝑅𝑢𝑠𝑡 and proved its
type soundness. Wagner et al. [63] proposed Borrow Calculus, which incorporates linearity and
borrowing, and proved its soundness. Additionally, Milewski [37] formalized the Rust trait system
by defining subsets of the language that include associated types, trait objects, and coherence
rules, and proved type soundness. However, none of these formalizations can represent any of the
soundness issues studied in this work. RustBelt and Borrow Calculus provide variants of lambda
calculus that express lifetimes but lack many high-level features, including implied bounds and
traits; Milewski’s languages focus only on traits, omitting lifetimes, and define coherence rules
only for limited language features, without encompassing associated types or trait objects. While
formalizing all language features would not be feasible, we suggest that covering implied bounds
and treating lifetimes and traits simultaneously should have the highest priority.

9     Conclusion
This work studies 30 soundness issues in rustc, analyzing their affected features, symptoms, conse-
quences, triggering features, community consensus, and lifecycles. We also investigate potential test
oracles, such as AddressSanitizer, Miri, Chalk, and a-mir-formality, and documents describing the
language semantics, such as the Rust Reference, the FLS, and Rust RFCs. We found that soundness
issues are often triggered by associated types and the interaction between lifetimes and traits,
while implied bounds and trait objects are especially relevant to memory bugs. Existing tools
are insufficient to serve as comprehensive test oracles, and a huge gap remains between existing
documentation and the requirements for a mechanized specification.

Acknowledgements
The Python scripts for the data collection in §3 and the visualization of Fig. 1 were developed with
assistance from Gemini 3 Flash. This material is based upon work supported in part by the Defense
Advanced Research Projects Agency (DARPA) under Agreement No. HR00112590130, the National
Research Foundation of Korea (NRF) (2021R1A5A1021944, 2022R1A2C2003660, and 2026-25549584),
and Institute of Information & Communications Technology Planning & Evaluation (IITP) grant
funded by the Korea government (MSIT) (2024-00337703). Any opinions, findings, and conclusions
or recommendations expressed in this material are those of the authors and do not necessarily
reflect the views of the funding agencies.

Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
Rust’s Type Checker Implementation Is Unsound: An Empirical Study on Soundness Bugs in rustc                    ISSTA129:21


Data Availability
The dataset and source code used for this study are available at https://doi.org/10.5281/zenodo.
20728406 [51].

References
 [1] 2021. Netstack3 - A Fuchsia Owned Rust Based Netstack. Accessed: 2026-01-23. https://fuchsia.dev/fuchsia-
     src/contribute/roadmap/2021/netstack3
 [2] 2025. Are We Spec Yet? No, Sadly. Accessed: 2026-01-23. https://arewespecyet.rs/
 [3] 2025. Ubuntu 25.10 Replaces GNU Coreutils with Rust Uutils. Accessed: 2026-01-23. https://www.altusintel.com/public-
     yych08
 [4] Nada Amin and Ross Tate. 2016. Java and Scala’s Type Systems are Unsound: The Existential Crisis of Null Pointers.
     In Proceedings of the 2016 ACM SIGPLAN International Conference on Object-Oriented Programming, Systems, Languages,
     and Applications (Amsterdam, Netherlands) (OOPSLA 2016). Association for Computing Machinery, New York, NY,
     USA, 838–848. doi:10.1145/2983990.2984004
 [5] Brian Anderson, Lars Bergstrom, Manish Goregaokar, Josh Matthews, Keegan McAllister, Jack Moffitt, and Simon
     Sapin. 2016. Engineering the Servo Web Browser Engine Using Rust. In Proceedings of the 38th International Conference
     on Software Engineering Companion (Austin, Texas) (ICSE ’16). Association for Computing Machinery, New York, NY,
     USA, 81–89. doi:10.1145/2889160.2889229
 [6] Langston Barrett. 2026. tree-splicer. Accessed: 2026-01-23. https://github.com/langston-barrett/tree-splicer
 [7] Kevin Boos, Namitha Liyanage, Ramla Ijaz, and Lin Zhong. 2020. Theseus: An Experiment in Operating System
     Structure and State Management. In Proceedings of the 14th USENIX Conference on Operating Systems Design and
     Implementation (OSDI’20). USENIX Association, USA.
 [8] Xuemeng Cai, Jiakun Liu, Xiping Huang, Yijun Yu, Haitao Wu, Chunmiao Li, Bo Wang, Imam Nur Bani Yusuf,
     and Lingxiao Jiang. 2026. RustMap: Towards Project-Scale C-to-Rust Migration via Program Analysis and LLM. In
     Engineering of Complex Computer Systems, Yuan Zhou, Sin G. Teo, Xiaofei Xie, Zuohua Ding, and Yang Liu (Eds.).
     Springer Nature Switzerland, Cham, 283–302. doi:10.1007/978-3-032-00828-2_16
 [9] Stefanos Chaliasos, Thodoris Sotiropoulos, Georgios-Petros Drosos, Charalambos Mitropoulos, Dimitris Mitropoulos,
     and Diomidis Spinellis. 2021. Well-typed programs can go wrong: a study of typing-related bugs in JVM compilers.
     Proc. ACM Program. Lang. 5, OOPSLA, Article 123 (Oct. 2021), 30 pages. doi:10.1145/3485500
[10] Xiangdong Chen, Zhaofeng Li, Jerry Zhang, Vikram Narayanan, and Anton Burtsev. 2025. Atmosphere: Practical
     Verified Kernels with Rust and Verus. In Proceedings of the ACM SIGOPS 31st Symposium on Operating Systems Principles
     (Lotte Hotel World, Seoul, Republic of Korea) (SOSP ’25). Association for Computing Machinery, New York, NY, USA,
     752–767. doi:10.1145/3731569.3764821
[11] Yu-Hsun Chiang, Wei-Lin Chang, Shih-Wei Li, and Jan-Ting Tu. 2024. Securing a Multiprocessor KVM Hypervisor with
     Rust. In Proceedings of the 2024 ACM Symposium on Cloud Computing (Redmond, WA, USA) (SoCC ’24). Association for
     Computing Machinery, New York, NY, USA, 650–667. doi:10.1145/3698038.3698562
[12] Travis Cross. 2025. Adopting the FLS. Accessed: 2026-01-23. https://blog.rust-lang.org/2025/03/26/adopting-the-fls
[13] Zhenyang Dai, Shuang Liu, Vilhelm Sjoberg, Xupeng Li, Yu Chen, Wenhao Wang, Yuekai Jia, Sean Noble Anderson, Laila
     Elbeheiry, Shubham Sondhi, Yu Zhang, Zhaozhong Ni, Shoumeng Yan, Ronghui Gu, and Zhengyu He. 2024. Verifying
     Rust Implementation of Page Tables in a Software Enclave Hypervisor. In Proceedings of the 29th ACM International
     Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2 (La Jolla, CA, USA)
     (ASPLOS ’24). Association for Computing Machinery, New York, NY, USA, 1218–1232. doi:10.1145/3620665.3640398
[14] Kyle Dewey, Jared Roesch, and Ben Hardekopf. 2015. Fuzzing the Rust Typechecker Using CLP (T). In 2015 30th
     IEEE/ACM International Conference on Automated Software Engineering (ASE). 482–493. doi:10.1109/ASE.2015.65
[15] Xiaoting Du, Zheng Zheng, Lei Ma, and Jianjun Zhao. 2021. An Empirical Study on Common Bugs in Deep Learning
     Compilers. In 2021 IEEE 32nd International Symposium on Software Reliability Engineering (ISSRE). 184–195. doi:10.
     1109/ISSRE52982.2021.00030
[16] Mehmet Emre, Peter Boyland, Aesha Parekh, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2023. Aliasing Limits
     on Translating C to Safe Rust. Proc. ACM Program. Lang. 7, OOPSLA1 (apr 2023). doi:10.1145/3586046
[17] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2021. Translating C to Safer Rust. Proc. ACM Program.
     Lang. 5, OOPSLA (oct 2021). doi:10.1145/3485498
[18] Jaemin Hong and Sukyoung Ryu. 2023. Concrat: An Automatic C-to-Rust Lock API Translator for Concurrent Programs.
     In Proceedings of the 45th International Conference on Software Engineering (ICSE ’23). IEEE Press, Melbourne, Victoria,
     Australia, 716–728. doi:10.1109/ICSE48619.2023.00069
[19] Jaemin Hong and Sukyoung Ryu. 2024. Don’t Write, but Return: Replacing Output Parameters with Algebraic Data
     Types in C-to-Rust Translation. Proc. ACM Program. Lang. 8, PLDI (jun 2024). doi:10.1145/3656406


                              Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
ISSTA129:22                                                                 Yusung Sim, Sukyoung Ryu, and Jaemin Hong


[20] Jaemin Hong and Sukyoung Ryu. 2024. To Tag, or Not to Tag: Translating C’s Unions to Rust’s Tagged Unions. In
     Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering (Sacramento, CA, USA)
     (ASE ’24). Association for Computing Machinery, New York, NY, USA, 40–52. doi:10.1145/3691620.3694985
[21] Jaemin Hong and Sukyoung Ryu. 2024. Type-migrating C-to-Rust Translation using a Large Language Model. Empirical
     Software Engineering 30, 1 (Oct. 2024). doi:10.1007/s10664-024-10573-2
[22] Jaemin Hong and Sukyoung Ryu. 2025. Automatically Translating C to Rust. Commun. ACM 68, 11 (Oct. 2025), 58–65.
     doi:10.1145/3737696
[23] Jaemin Hong and Sukyoung Ryu. 2025. Forcrat: Automatic I/O API Translation from C to Rust via Origin and
     Capability Analysis. In 2025 40th IEEE/ACM International Conference on Automated Software Engineering (ASE). 1541–
     1552. doi:10.1109/ASE63991.2025.00130
[24] Jaemin Hong, Sunghwan Shim, Sanguk Park, Tae Woo Kim, Jungwoo Kim, Junsoo Lee, Sukyoung Ryu, and Jeehoon
     Kang. 2024. Taming Shared Mutable States of Operating Systems in Rust. Science of Computer Programming 238 (2024),
     103152. doi:10.1016/j.scico.2024.103152
[25] Keyang Hu, Wang Huang, Lei Wang, Ce Mo, Runxiang Wang, Yu Chen, Ju Ren, and Bo Jiang. 2024. Unishyper: A
     Rust-based Unikernel Enhancing Reliability and Efficiency of Embedded Systems. Journal of Systems Architecture
     (2024), 103199. doi:10.1016/j.sysarc.2024.103199
[26] Sujay Jayakar. 2020. Rewriting the Heart of Our Sync Engine. Accessed: 2026-01-23. https://dropbox.tech/infrastructure/
     rewriting-the-heart-of-our-sync-engine
[27] Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, and Derek Dreyer. 2017. RustBelt: Securing the Foundations of
     the Rust Programming Language. Proc. ACM Program. Lang. 2, POPL (dec 2017). doi:10.1145/3158154
[28] Ralf Jung, Benjamin Kimock, Christian Poveda, Eduardo Sánchez Muñoz, Oli Scherer, and Qian Wang. 2026. Miri:
     Practical Undefined Behavior Detection for Rust. Proc. ACM Program. Lang. 10, POPL, Article 48 (Jan. 2026), 29 pages.
     doi:10.1145/3776690
[29] Matthias Krüge. 2024. icemaker. Accessed: 2026-01-23. https://github.com/matthiaskrgr/icemaker
[30] Stefan Lankes, Jonathan Klimt, Jens Breitbart, and Simon Pickartz. 2020. RustyHermit: A Scalable, Rust-Based Virtual
     Execution Environment. In High Performance Computing: ISC High Performance 2020 International Workshops, Frankfurt,
     Germany, June 21–25, 2020, Revised Selected Papers (Frankfurt am Main, Germany). Springer-Verlag, Berlin, Heidelberg,
     331–342. doi:10.1007/978-3-030-59851-8_22
[31] Jaehyun Lee, Seokhun Jeong, and Sukyoung Ryu. 2026. Failing with Purpose: Dangling Coverage-Guided Negative
     Test Generation from a Mechanized P4 Type System. Proc. ACM Softw. Eng. 3, FSE, Article FSE081 (June 2026), 21 pages.
     doi:10.1145/3797109
[32] Amit Levy, Bradford Campbell, Branden Ghena, Daniel B. Giffin, Pat Pannuto, Prabal Dutta, and Philip Levis. 2017.
     Multiprogramming a 64kB Computer Safely and Efficiently. In Proceedings of the 26th Symposium on Operating
     Systems Principles (Shanghai, China) (SOSP ’17). Association for Computing Machinery, New York, NY, USA, 234–251.
     doi:10.1145/3132747.3132786
[33] Lantian Li, Yue Pan, Dan Wang, Jingwen Wu, and Zhongxing Yu. 2025. Understanding Typing-Related Bugs in Solidity
     Compiler. arXiv:2512.18182 [cs.SE] https://arxiv.org/abs/2512.18182
[34] Zhaofeng Li, Vikram Narayanan, Xiangdong Chen, Jerry Zhang, and Anton Burtsev. 2024. Rust for Linux: Understanding
     the Security Impact of Rust in the Linux Kernel. In 2024 Annual Computer Security Applications Conference (ACSAC).
     548–562. doi:10.1109/ACSAC63791.2024.00054
[35] Zixi Liu, Yang Feng, Yunbo Ni, Shaohua Li, Xizhe Yin, Qingkai Shi, Baowen Xu, and Zhendong Su. 2025. An Empirical
     Study of Bugs in the rustc Compiler. Proc. ACM Program. Lang 9, OOPSLA2 (Oct. 2025). doi:10.1145/3763800
[36] Nicholas D. Matsakis and Felix S. Klock. 2014. The Rust Language. In Proceedings of the 2014 ACM SIGAda Annual
     Conference on High Integrity Language Technology (Portland, Oregon, USA) (HILT ’14). Association for Computing
     Machinery, New York, NY, USA, 103–104. doi:10.1145/2663171.2663188
[37] Jonatan Milewski. 2015. Formalizing Rust traits. Master’s thesis. University of British Columbia. doi:10.14288/1.0220521
[38] Vikram Narayanan, Tianjiao Huang, David Detweiler, Dan Appel, Zhaofeng Li, Gerd Zellweger, and Anton Burtsev.
     2020. RedLeaf: Isolation and Communication in a Safe Operating System. In Proceedings of the 14th USENIX Conference
     on Operating Systems Design and Implementation (OSDI’20). USENIX Association, USA.
[39] Jihyeok Park, Seungmin An, Dongjun Youn, Gyeongwon Kim, and Sukyoung Ryu. 2021. JEST: N+1-Version Differential
     Testing of Both JavaScript Engines and Specification. In 2021 IEEE/ACM 43rd International Conference on Software
     Engineering (ICSE). IEEE, 13–24. doi:10.1109/icse43902.2021.00015
[40] Jihyeok Park, Jihee Park, Seungmin An, and Sukyoung Ryu. 2021. JISET: JavaScript IR-based Semantics Extraction
     Toolchain. In Proceedings of the 35th IEEE/ACM International Conference on Automated Software Engineering (Virtual
     Event, Australia) (ASE ’20). Association for Computing Machinery, New York, NY, USA, 647–658. doi:10.1145/3324884.
     3416632



Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
Rust’s Type Checker Implementation Is Unsound: An Empirical Study on Soundness Bugs in rustc                    ISSTA129:23


[41] Jihyeok Park, Dongjun Youn, Kanguk Lee, and Sukyoung Ryu. 2023. Feature-Sensitive Coverage for Conformance
     Testing of Programming Language Implementations. Proc. ACM Program. Lang. 7, PLDI (June 2023). doi:10.1145/3591240
[42] Yuke Peng, Hongliang Tian, Jinyi Xian, Shuai Zhou, Shoumeng Yan, and Yinqian Zhang. 2024. Framekernel: A Safe
     and Efficient Kernel Architecture via Rust-based Intra-kernel Privilege Separation. In Proceedings of the 15th ACM
     SIGOPS Asia-Pacific Workshop on Systems (Kyoto, Japan) (APSys ’24). Association for Computing Machinery, New York,
     NY, USA, 31–37. doi:10.1145/3678015.3680492
[43] David Renshaw. 2025. Fuzz Rustc. Accessed: 2026-01-23. https://github.com/dwrensha/fuzz-rustc
[44] Alan Romano, Xinyue Liu, Yonghwi Kwon, and Weihang Wang. 2021. An Empirical Study of Bugs in WebAssembly
     Compilers. In 2021 36th IEEE/ACM International Conference on Automated Software Engineering (ASE). 42–54. doi:10.
     1109/ASE51524.2021.9678776
[45] Rust-GCC. [n. d.]. GitHub - Rust-GCC/gccrs: GCC Front-End for Rust. https://github.com/Rust-GCC/gccrs
[46] Sukyoung Ryu and Jihyeok Park. 2024. JavaScript Language Design and Implementation in Tandem. Commun. ACM
     67, 5 (May 2024), 86–95. doi:10.1145/3624723
[47] Konstantin Serebryany, Derek Bruening, Alexander Potapenko, and Dmitry Vyukov. 2012. AddressSanitizer: a fast
     address sanity checker. In Proceedings of the 2012 USENIX Conference on Annual Technical Conference (Boston, MA)
     (USENIX ATC’12). USENIX Association, USA, 28.
[48] Guangyong Shang, Guangpeng Qi, Jianing Ren, Xianqi Jin, Wanjiang Shen, Junchao Li, Xiuzhen Cheng, and Runyu Pan.
     2025. LwRustIP: Memory-safe and efficient embedded networking stack with ownership semantics. High-Confidence
     Computing (2025), 100351. doi:10.1016/j.hcc.2025.100351
[49] Mayank Sharma, Pingshi Yu, and Alastair F. Donaldson. 2023. RustSmith: Random Differential Compiler Testing for
     Rust. In Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Testing and Analysis (Seattle, WA,
     USA) (ISSTA 2023). Association for Computing Machinery, New York, NY, USA, 1483–1486. doi:10.1145/3597926.3604919
[50] Qingchao Shen, Haoyang Ma, Junjie Chen, Yongqiang Tian, Shing-Chi Cheung, and Xiang Chen. 2021. A comprehensive
     study of deep learning compiler bugs. In Proceedings of the 29th ACM Joint Meeting on European Software Engineering
     Conference and Symposium on the Foundations of Software Engineering (Athens, Greece) (ESEC/FSE 2021). Association
     for Computing Machinery, New York, NY, USA, 968–980. doi:10.1145/3468264.3468591
[51] Yusung Sim, Sukyoung Ryu, and Jaemin Hong. 2026. Rust’s Type Checker Implementation is Unsound: An Empirical
     Study on Soundness Bugs in rustc (Artifact). doi:10.5281/zenodo.20728406
[52] Yusung Sim, Sukyoung Ryu, and Jaemin Hong. 2026. Supplementary Material for “Rust’s Type Checker Implementation
     Is Unsound: An Empirical Study on Soundness Bugs in rustc”. doi:10.5281/zenodo.21452140
[53] Chengnian Sun, Vu Le, Qirun Zhang, and Zhendong Su. 2016. Toward understanding compiler bugs in GCC and
     LLVM. In Proceedings of the 25th International Symposium on Software Testing and Analysis (Saarbrücken, Germany)
     (ISSTA 2016). Association for Computing Machinery, New York, NY, USA, 294–305. doi:10.1145/2931037.2931074
[54] The MiniRust Project. 2026. MiniRust: A Precise Specification for “Rust Lite / MIR Plus”. https://github.com/minirust/
     minirust. Accessed: 2026-01-23.
[55] The Rust Project. 2015. The Rust RFC Book: 1214-projections-lifetimes-and-wf. Accessed: 2026-01-23. https://rust-
     lang.github.io/rfcs/1214-projections-lifetimes-and-wf.html
[56] The Rust Project. 2026. a-mir-formality: A model of MIR and the Rust Type System. https://github.com/rust-lang/a-
     mir-formality. Accessed: 2026-01-23.
[57] The Rust Project. 2026. Chalk: An Implementation of the Rust Trait System Using a Prolog-like Logic Solver. https:
     //github.com/rust-lang/chalk. Accessed: 2026-01-23.
[58] The Rust Project. 2026. FLS. Accessed: 2026-01-23. https://rust-lang.github.io/fls
[59] The Rust Project. 2026. Miri: An interpreter for Rust’s Mid-level Intermediate Representation. https://github.com/rust-
     lang/miri. Accessed: 2026-01-23.
[60] The Rust Project. 2026. The Rust Reference. Accessed: 2026-01-23. https://doc.rust-lang.org/reference
[61] The Rust Project. 2026. The Rust Reference: Lifetime Elision. Accessed: 2026-01-23. https://doc.rust-lang.org/reference/
     lifetime-elision.html
[62] The Rust Project. 2026. The Rust RFC Book. Accessed: 2026-01-23. https://rust-lang.github.io/rfcs
[63] Andrew Wagner, Olek Gierczak, Brianna Marshall, John M. Li, and Amal Ahmed. 2025. From Linearity to Borrowing.
     Proc. ACM Program. Lang. 9, OOPSLA2 (Oct. 2025). doi:10.1145/3764117
[64] Qian Wang and Ralf Jung. 2024. Rustlantis: Randomized Differential Testing of the Rust Compiler. Proc. ACM Program.
     Lang. 8, OOPSLA2, Article 340 (Oct. 2024), 27 pages. doi:10.1145/3689780
[65] Xiafa Wu and Brian Demsky. 2025. GenC2Rust: Towards Generating Generic Rust Code from C. In 2025 IEEE/ACM
     47th International Conference on Software Engineering (ICSE). IEEE Computer Society, Los Alamitos, CA, USA, 664–664.
     doi:10.1109/ICSE55347.2025.00127
[66] Xinmeng Xia, Yang Feng, and Qingkai Shi. 2023. Understanding Bugs in Rust Compilers. In 2023 IEEE 23rd International
     Conference on Software Quality, Reliability, and Security (QRS). 138–149. doi:10.1109/QRS60937.2023.00023


                              Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
ISSTA129:24                                                                Yusung Sim, Sukyoung Ryu, and Jaemin Hong


[67] Qingxiao Xu and Jeff Huang. 2025. Optimizing Type Migration for LLM-Based C-to-Rust Translation: A Data Flow
     Graph Approach. In Proceedings of the 14th ACM SIGPLAN International Workshop on the State Of the Art in Program
     Analysis (Seoul, Republic of Korea) (SOAP ’25). Association for Computing Machinery, New York, NY, USA, 8–14.
     doi:10.1145/3735544.3735582
[68] Wenzhang Yang, Cuifeng Gao, Xiaoyuan Liu, Yuekang Li, and Yinxing Xue. 2024. Rust-twins: Automatic Rust Compiler
     Testing through Program Mutation and Dual Macros Generation. In Proceedings of the 39th IEEE/ACM International
     Conference on Automated Software Engineering (Sacramento, CA, USA) (ASE ’24). Association for Computing Machinery,
     New York, NY, USA, 631–642. doi:10.1145/3691620.3695059
[69] Dongjun Youn, Wonho Shin, Jaehyun Lee, Sukyoung Ryu, Joachim Breitner, Philippa Gardner, Sam Lindley, Matija
     Pretnar, Xiaojia Rao, Conrad Watt, and Andreas Rossberg. 2024. Bringing the WebAssembly Standard up to Speed
     with SpecTec. Proc. ACM Program. Lang. 8, PLDI (June 2024). doi:10.1145/3656440
[70] Dongjun Youn, Wonho Shin, and Sukyoung Ryu. 2025. WEST: Specification-Based Test Generation for WebAssembly.
     In 2025 40th IEEE/ACM International Conference on Automated Software Engineering (ASE). 1403–1414. doi:10.1109/
     ASE63991.2025.00119
[71] Sijie Yu and Ziyuan Wang. 2024. An Empirical Study on Bugs in Rust Programming Language. In 2024 IEEE 24th
     International Conference on Software Quality, Reliability and Security (QRS). 296–305. doi:10.1109/QRS62785.2024.00037
[72] Hanliang Zhang, Cristina David, Meng Wang, Brandon Paulsen, and Daniel Kroening. 2025. Scalable, Validated
     Code Translation of Entire Projects using Large Language Models. Proc. ACM Program. Lang. 9, PLDI (June 2025).
     doi:10.1145/3729315
[73] Hanliang Zhang, Cristina David, Yijun Yu, and Meng Wang. 2023. Ownership Guided C to Rust Translation. In
     Computer Aided Verification, Constantin Enea and Akash Lal (Eds.). Springer Nature Switzerland, Cham, 459–482.
     doi:10.1007/978-3-031-37709-9_22
[74] Ruxin Zhang, Shanxin Zhang, and Linbo Xie. 2025. A Systematic Exploration of C-to-Rust Code Translation Based on
     Large Language Models: Prompt Strategies and Automated Repair. Automated Software Engineering 33, 1 (Oct. 2025).
     doi:10.1007/s10515-025-00570-0
[75] Han Zhou, Yu Luo, Mengtao Zhang, and Dianxiang Xu. 2025. C2RustTV: An LLM-based Framework for C to Rust
     Translation and Validation. In 2025 IEEE 49th Annual Computers, Software, and Applications Conference (COMPSAC).
     1254–1259. doi:10.1109/COMPSAC65507.2025.00158

Received 2026-01-30; accepted 2026-06-25




Proc. ACM Softw. Eng., Vol. 3, No. ISSTA, Article ISSTA129. Publication date: October 2026.
