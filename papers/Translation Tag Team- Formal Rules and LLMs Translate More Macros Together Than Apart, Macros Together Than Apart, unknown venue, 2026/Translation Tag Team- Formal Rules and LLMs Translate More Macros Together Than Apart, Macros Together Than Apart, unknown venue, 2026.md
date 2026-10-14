                                            Translation Tag Team: Formal Rules and LLMs Translate More
                                                            Macros Together Than Apart
                                                                     Brent Pappas✉                                                         Joseph Zalusky
                                                              University of Central Florida                                         University of Central Florida
                                                                     Orlando, USA                                                          Orlando, USA
                                                                brent.pappas@ucf.edu                                                  josephzalusky@ucf.edu

                                                                   Zachary Burkett                                                          Paul Gazzillo
                                                              University of Central Florida                                         University of Central Florida
                                                                     Orlando, USA                                                          Orlando, USA
                                                               zachary.burkett@ucf.edu                                                 paul.gazzillo@ucf.edu

                                         Abstract                                                                    ACM Reference Format:
                                         Modern critical software infrastructure is largely written in C. Since      Brent Pappas, Joseph Zalusky, Zachary Burkett, and Paul Gazzillo. 2026.
                                                                                                                     Translation Tag Team: Formal Rules and LLMs Translate More Macros
                                         C lacks memory safety, researchers are investigating automatic
                                                                                                                     Together Than Apart. In Proceedings of the 41st IEEE/ACM International
                                         translation of C to safer languages like Rust. But real-world C soft-
arXiv:2608.06705v2 [cs.SE] 10 Aug 2026




                                                                                                                     Conference on Automated Software Engineering (ASE ’26), October 12–16,
                                         ware consists of more than just C code, often using named code              2026, Munich, Germany. ACM, New York, NY, USA, 13 pages. https://doi.
                                         fragments called macros which are not part of the C language                org/10.1145/3832783.3837412
                                         proper. State-of-the-art techniques avoid translating macros by
                                         preprocessing C code first before translating it. But this approach         1    Introduction
                                         produces translations that are dissimilar to the original C code,           Modern critical software infrastructure is largely written in C. Since
                                         because preprocessing inlines all macro definitions. To preserve            C lacks memory safety [6, 13, 74], researchers are investigating au-
                                         macro usage in translated code, we study the language features              tomatic translation of C to safer languages like Rust [5, 7, 15, 32, 34,
                                         that macros and C share and distill them into the first formally-           64]. However, real-world C code heavily uses [16, 54] macros [21],
                                         specified translator, MerC. To evaluate MerC, we introduce the first        which are named code fragments and not part of the C language
                                         macro translation benchmark, MacroBench, with test cases based              proper [27, 38, 51, 66]. Instead, the C preprocessor replaces macros
                                         on macros randomly sampled from real-world C programs. We find              in source code with their defined code fragments to produce pure
                                         that MerC supports 50% of MacroBench’s macro test cases. We also            C code. C tools have long-struggled with macros [27, 38, 51, 66],
                                         use MacroBench to evaluate how effective large language models              and translators are no exception [8–10, 33]. State-of-the-art C trans-
                                         (LLMs) are at performing the previously-unstudied task of macro             lators avoid macros by preprocessing first, then translating the
                                         translation. LLMs translate 22% to 77% more of MacroBench than              resulting pure C code [8, 35, 65]. But this approach emits transla-
                                         MerC, but with 8% and 28% of these translations being incorrect             tions which inline all macros and lose their abstractions.
                                         translations requiring additional validation by developers. In con-            The problem is that by expanding macros first, translators end up
                                         trast, MerC only produces correct translations. Our key insight is          translating a version of C code different from the original, and emit
                                         that running MerC first then using LLMs on the remainder reaps              translated code that lacks the original code’s macro abstractions.
                                         greater benefits than using either technique alone. This tag team           For example, the code below is from the Linux kernel source1 :
                                         approach has an average failure rate 32% lower than that of LLMs,
                                                                                                                          gen6_pte_t pte = GEN6_GTT_ADDR_ENCODE(addr) | GEN6_PTE_VALID;
                                         while also translating an average of 51% more test cases than MerC.
                                                                                                                     Syntactically, GEN6_GTT_ADDR_ENCODE(addr) resembles a C func-
                                         CCS Concepts                                                                tion call and GEN6_PTE_VALID a C variable, but both are actually
                                                                                                                     macros. After preprocessing, the macros are inlined, producing the
                                         • Software and its engineering → Preprocessors; Semantics;
                                                                                                                     following C code:
                                         Automated static analysis.
                                                                                                                          gen6_pte_t pte = ((addr) | (((addr) » 28) & 0xff0)) |
                                                                                                                              ((u32)(((((1UL))) « (0)) + ((int)(sizeof(struct {
                                         Keywords                                                                               int : (-!!((sizeof(int) ==
                                                                                                                                  sizeof(*(8 ? ((void *)((long)(0) * 0l)) :
                                         macros, C, program translation, program analysis
                                                                                                                                    (int *)8))) && ((0) < 0 || (0) > 31)));})))));

                                                                                                                     This barely-recognizable C code, which lacks the original pro-
                                                                                                                     grams’s macros, is what translators ultimately end up translating to
                                                                                                                     a new language, because they preprocess macros first. Macros are
                                         This work is licensed under a Creative Commons Attribution-NonCommercial-   very common in real-world source code: Linux has over 50 thou-
                                         NoDerivatives 4.0 International License.
                                         ASE ’26, Munich, Germany                                                    sand macro definitions and 500 thousand macro invocations, and C
                                         © 2026 Copyright held by the owner/author(s).                               programs average one invocation every four lines of code [16].
                                         ACM ISBN 979-8-4007-2882-2/2026/10
                                         https://doi.org/10.1145/3832783.3837412                                     1 linux-v6.2-rc2/drivers/gpu/drm/i915/gt/intel_gtt.h
ASE ’26, October 12–16, 2026, Munich, Germany                                               Brent Pappas, Joseph Zalusky, Zachary Burkett, and Paul Gazzillo


    There is little prior research on preprocessor macro translation.      The presence of incorrect translations means that developers vali-
Mennie and Clarke describe a translation technique [45] for a re-          date all LLM translations to find correct ones, a substantial task for
stricted set of macros that act like C variables, omitting commonly-       large codebases like the Linux kernel which contains thousands of
used function-like macros, but lack a rigorous evaluation or bench-        macros. In contrast, MerC’s semantics-aware translation rules only
mark, and their translator’s code is publicly unavailable. Visual          produce correct translations, obviating substantial validation.
Studio supports translating macros to C++ constant expression dec-            We show that using MerC to translate macros first, and then
larations [57], but lacking semantic analysis [54] gets translations       “tagging in” LLMs to translate the remaining macros, reaps greater
wrong [59] and is designed for C++, not C. LLMs are potentially            benefits than using either technique alone. We observe an 18% to
viable for macro translation [19, 29, 47, 52, 65] and some are specif-     45% lower failure rate for this tag team approach than using LLMs
ically designed for code translation [28, 48]. But to the best of          alone and 30% to 80% more translations than using MerC alone.
our knowledge, there is no prior study of their ability to trans-          Counterintuitively, although LLMs have a much higher average
late macros. Moreover, there are no published macro translation            failure rate on the remaining macros not supported by MerC (38%
benchmarks that would enable evaluating different translators.             vs. 17%), it is less costly in both overall translation time and post-
    We introduce the first formally-specified, semantics-aware macro       translation validation effort to reserve LLMs for these harder cases,
translator. The key challenge is that while macro usage appears            rather than treating LLMs as all-purpose translators.
syntactically like C functions, their semantics can differ greatly [54];      We make the following contributions:
translators cannot in general treat them like C functions and expect             • A comparison of macro and C semantics and a set of formal
to produce equivalent code. The key insight to our approach is that                translation rules for common macro usage (Section 2).
by identifying those macro usages that behave like C functions, we               • MerC, an implementation our translation rules (Section 3).
can transform such macros to true C functions. The benefit is that               • MacroBench, the first benchmark specifically focused on
existing C translators can then translate them like any other C func-              preprocessor macro translation (Section 4).
tion without special support for macros. Moreover, downstream C                  • An evaluation and comparison of the macro translation ca-
translators can convert C-translated macros into compile-time ab-                  pabilities of MerC and several popular LLMs (Section 5).
stractions, e.g., Rust inline functions [61] or even Rust macros [62],
to translate macros in a way that does not sacrifice performance.            The anonymized, publicly-available artifact2 includes MerC, Mac-
We study macro and C language features and identify the specific           roBench, experimental scripts, and data.
conditions under which macros match the behavior of C functions,
variables, or enums. We define seven formal translation rules that         2     Translating Macros with MerC
capture these conditions and implement them in a new tool called           We present formal translation rules specifying how and when to
MerC.                                                                      convert macro definitions into C definitions, and give examples of
    With no published benchmark designed for evaluating macro              how MerC follows these rules to translate macros. We designed
translation, we introduce a new benchmark suite called MacroBench          MerC’s translation rules by studying the C preprocessor’s ISO
sampled randomly from real-world C programs, independent from              specifications [36, 37], its usage in large open source projects, and
our formal translation rule specifications. MacroBench is a statisti-      analyses of it in prior work [14, 16, 54].
cally significant (95% confidence level, 5% margin of error) random
sample of 398 macro test cases stratified over 23 real-world C pro-        2.1        Macro Definitions
grams used in prior studies of C and macros [16, 27, 38, 54]. Each         Each macro definition has a C identifier as a name, and a possi-
test case focuses on the translation of a single macro and contains        bly empty sequence of C tokens as a body. Function-like macro
its surrounding language context. MacroBench also contains more            definitions also have a parenthesized, comma-separated list of C
than one thousand real translations of its test cases produced during      identifiers as arguments. Object-like macros do not. For example:
the evaluation in this paper. We semi-automatically checked each                  1   # define PI                 3.14
translation to record the translation’s correctness, what language                2   # define ADD (a , b )       a + b
construct the tool attempts to translate each macro to, why each                  3   PI * ( ADD ( PI , 2))
tool failed for incorrect translations, timings, and other metadata.       Lines 1 and 2 define the object-like macro PI and the function-like
    We then use MacroBench to evaluate how effective popular large         macro ADD(). Line 3 preprocesses to 3.14 * (3.14 + 2).
language models (LLMs) [29, 47, 48] are at translating macros, and            A macro invocation need not expand to a complete C statement:
compare them to MerC. We specifically compare MerC to LLMs,
                                                                                  1   # define MY_IF ( X )   if ( X )
and no other rule-based tools, because to the best of our knowledge               2   MY_IF ( x > 0) { ... }
MerC is the first publicly-available semantics-aware macro-to-C
translator. Other rule-based tools either ignore macro semantics                 Listing 1: MY_IF() macro definition and invocation.
and emit incorrect translations [57], lack a publicly-available im-        Line 2 preprocesses to if (x > 0), a fragment of a C if statement.
plementation [45], or do not translate macros to C [40, 44]. MerC
translates all MacroBench’s test cases in 37 seconds and produces          2.2        Determining Translatability
no incorrect translations, but only emits translations for 50% of          Figure 1 presents a six-way Venn diagram comparing the C and C
MacroBench’s test cases. Meanwhile, LLMs emit translations for             preprocessor semantic features MerC uses to decide which macro
22% to 77% more test cases than MerC, but spend 45 minutes to
2.5 hours on translation, and get 8% to 28% of translations wrong.         2 https://doi.org/10.5281/zenodo.21798007
Translation Tag Team: Formal Rules and LLMs Translate More Macros Together Than Apart                                                                                   ASE ’26, October 12–16, 2026, Munich, Germany


Name                                             Condition checked
                                                                                                                                                                     𝑝 0 · · · 𝑝𝑛
DefinedGlobally(name)                            name is defined outside a function.                                                                          𝑉0 · · · 𝑉𝑛 ⊢ 𝐴 { 𝐵
CalledByName(𝜄)                                  𝜄 uses call-by-name semantics.                                                    Where 𝑝 0 · · · 𝑝𝑛 are premises that must all be true for the rule to
CapturesEnv(𝜄)                                   𝜄 accesses caller’s environment.                                                  apply, 𝑉0 · · · 𝑉𝑛 are context variables necessary for evaluating the
IsConstExpr(𝜄)                                   𝜄 is a constant C expression.                                                     rule’s premises, and 𝐴 and 𝐵 are source and target syntax.
IsExpression(𝜄)                                  𝜄 is a C expression.                                                                 Rules may use any of the four context variables M, Γ, A, and
IsICE(𝜄)                                         𝜄 is a compile-time constant (ICE).                                               Δ. M and Γ map each macro’s name to its set of invocations and
IsStatement(𝜄)                                   𝜄 is a not an expression.                                                         the types of the C expressions it expands to, respectively. A and Δ
AddressReqired(𝜄)                                𝜄 must be an addressable expression.                                              map each pair of macro name and argument name to the set of the
SizeReqired(𝜄)                                   𝜄 must be an expression with a size.                                              argument’s expansions and the types of the C expressions it expands
ConstExprReqired(𝜄)                              𝜄 must be a compile-time constant.                                                to, respectively. A macro or macro argument that expands to a non-
IsMeta(𝜄)                                        𝜄 manipulates tokens.                                                             expression C statement maps to void in Γ or Δ, respectively.
Table 1: Informal function definitions for Figure 2. Each func-                                                                       Rule premises use helper functions typeset in SmallCaps font.
tion accepts either a macro name, or an invocation or argu-                                                                        Table 1 defines each function informally. All premises and functions
ment expansion 𝜄, as input, and outputs a boolean.                                                                                 expect named macros expanding to whole C statements, and MerC
                                                                                                                                   does not translate macros like MY_IF() (Listing 1) that expand to C
                                                                                                                                   syntax fragments, or variadic macros. To compute these functions
                                                                                                                                   in practice, MerC uses an existing macro analyzer named Maki [54],
                                                  Variables                                                                        which works by first hooking into the Clang preprocessor and
                                                                                                                                   abstract syntax tree (AST) to determine which macro invocations
                                                                                      Function
                          Enums                                                      arguments                                     align with AST nodes. Maki then performs semantic analysis on the
                                                                      Variable            Call-by-
                                                                                                                Macro
                                                                                                                                   AST-aligned invocations to compute for each of them the functions
                                                                                           value
                                                           Local
                                                          scoping
                                                                     expression
                                                                    initialization       semantics
                                                                                                              arguments
                                                                                                                                   shown in Table 1 as a set of Boolean properties.
                                                                                                              Call-by-name
        Macros                                                                                                 semantics
                                                   Constant

  Environment
                                                  expression
                                                 initialization
                                                                                                                                   2.3        Translating Object-like Macros
    capture             Compile-
                          time                                                                                                     Rules I and II (Figure 2) translate to variables and enums, respec-
  Polymorphism          constant                                                                 Statement
                                                                                                 definition            Functions   tively, macros whose semantics match the rules’ premises. For ex-
                                                                                                                                   ample, the object-like macro QUIT, which expands to the character
             Meta-
          programming
                                                  Monomorphism
                                                                                                                                   ‘q’, satisfies Rule I’s conditions for translation to a C variable:
                                                                            Global                                                        1   # define QUIT 'q '
                                                                           scoping
                                                                                                                                          2   void check_quit ( void ) {
                                                Memory                                                                                    3        if ( QUIT == getch () ) exit (0) ;
                                    Memory
                                                 sizing
                                                                                                                                          4   }
                                   addressing
                                                                                                                                       Listing 2: QUIT macro definition and invocation.
                                                                                                                                      Premise 1 checks that QUIT is defined outside of function bound-
                                                                                                                                   aries, so that translating it to a C variable will not limit it to a
                                                                                                                                   specific scope. Premise 2 collects all QUIT’s invocations, in this case
                                                                                                                                   the one invocation on Line 3, into a set 𝜇. Premises 3 and 4 check
                                                                                                                                   that QUIT does not capture identifiers from its caller’s environ-
  Figure 1: Semantics available to C and macro constructs.                                                                         ment nor performs metaprogramming actions like token-pasting or
                                                                                                                                   stringification [22], as C variables lack these features. QUIT satisfies
                                                                                                                                   these premises, because it expands to the literal ‘q’. Premises 5
definitions are translatable to C variable, enum, and function defi-                                                               and 6 verify the macro is not used with the address-of (&) or sizeof
nitions, and which macro arguments are translatable to C function                                                                  operators, because differences between macro and C scoping rules
arguments. A macro that only uses the semantic features of a C                                                                     mean that variables in macro expansions and function bodies have
construct can be safely translated to a definition of that construct,                                                              different memory addresses and sizes.
without needing to change the macro’s callsites. For instance, a                                                                      Premise 7 validates that QUIT is not used where a compile-time
macro that only uses features in Figure 1’s overlapping regions                                                                    constant is required (e.g., in a case label), because C variables are
between macros and enums would be safe to turn into a C enum                                                                       not compile-time constants3 . QUIT satisfies Premise 7 because it
by swapping its macro definition with an enum definition, without                                                                  expands in an if condition (Line 3) where compile-time constants
changing its callsites. This enables downstream C translators to                                                                   are not required. Premise 8 ensures that QUIT’s definition is a con-
translate C code while preserving macro abstractions, and helps                                                                    stant expression, since it will be translated to a global variable, per
remove needless macros from programs like the Linux kernel that                                                                    Premise 1, and C requires global initializers to be constant. QUIT
have guidelines to prefer functions over macros when possible [68].                                                                satisfies Premise 8 because it expands to the character literal ‘q’.
   Figure 1 is formalized in Figure 2 as a set of inference rules for
translating macros to C code. Each rule has the form:                                                                              3 C23, finalized Oct. 2024, permits compile-time constant variables with constexpr [37].
ASE ’26, October 12–16, 2026, Munich, Germany                                                     Brent Pappas, Joseph Zalusky, Zachary Burkett, and Paul Gazzillo



Rule I: Object-like macro to global variable
                    (1)    DefinedGlobally(name)                       (5)    ∀𝜄 ∈ 𝜇 : ¬AddressReqired(𝜄)              (9)    𝛾 = Γ(𝑛𝑎𝑚𝑒)
                    (2)    𝜇 = 𝑀 (𝑛𝑎𝑚𝑒)                                (6)    ∀𝜄 ∈ 𝜇 : ¬SizeReqired(𝜄)                 (10)   |𝛾 | = 1
                    (3)    ∀𝜄 ∈ 𝜇 : ¬CapturesEnvironment(𝜄)            (7)    ∀𝜄 ∈ 𝜇 : ¬ConstExprReqired(𝜄)            (11)   𝑡𝑦𝑝𝑒 ∈ 𝛾
                    (4)    ∀𝜄 ∈ 𝜇 : ¬IsMeta(𝜄)                         (8)    ∀𝜄 ∈ 𝜇 : IsConstExpr(𝜄)                  (12)   𝑡𝑦𝑝𝑒 ∉ {void}
                                             M, Γ ⊢ #define name body { static const type name = body ;
Rule II: Object-like macro to enum
           (13)     DefinedGlobally(name)                      (17)     ∀𝜄 ∈ 𝜇 : ¬AddressReqired(𝜄)          (21)     |𝛾 | = 1
           (14)     𝜇 = 𝑀 (𝑛𝑎𝑚𝑒)                               (18)     ∀𝜄 ∈ 𝜇 : ¬SizeReqired(𝜄)             (22)     𝑡𝑦𝑝𝑒 ∈ 𝛾
           (15)     ∀𝜄 ∈ 𝜇 : ¬CapturesEnvironment(𝜄)           (19)     ∀𝜄 ∈ 𝜇 : IsICE(𝜄)                    (23)     SizeOf(𝑡𝑦𝑝𝑒) ≤ SizeOf(int)
           (16)     ∀𝜄 ∈ 𝜇 : ¬IsMeta(𝜄)                        (20)     𝛾 = Γ(𝑛𝑎𝑚𝑒)
                                                 M, Γ ⊢ #define name body { enum { name = body };
Rule III: Function-like macro to non-void function
          (24)    DefinedGlobally(name)                       (29)     ∀𝜄 ∈ 𝜇 : ¬SizeReqired(𝜄)                (34)     𝑡𝑦𝑝𝑒 ∈ 𝛾
          (25)    𝜇 = 𝑀 (𝑛𝑎𝑚𝑒)                                (30)     ∀𝜄 ∈ 𝜇 : ¬ConstExprReqired(𝜄)           (35)     𝑡𝑦𝑝𝑒 ∉ {void}
          (26)    ∀𝜄 ∈ 𝜇 : ¬CapturesEnvironment(𝜄)            (31)     ∀𝜄 ∈ 𝜇 : IsExpression(𝜄)                (36)     name, A, Δ ⊢ 𝑎𝑟𝑔𝑠 { 𝑎𝑟𝑔𝑠 ′
          (27)    ∀𝜄 ∈ 𝜇 : ¬IsMeta(𝜄)                         (32)     𝛾 = Γ(𝑛𝑎𝑚𝑒)
          (28)    ∀𝜄 ∈ 𝜇 : ¬AddressReqired(𝜄)                 (33)     |𝛾 | = 1
                                M, Γ, A, Δ ⊢ #define name ( args ) body { static type name ( args’ ) { return body ; }
Rule IV: Function-like macro to void function
   (37)     DefinedGlobally(name)                      (42)    ∀𝜄 ∈ 𝜇 : ¬SizeReqired(𝜄)                               (47)    𝑡𝑦𝑝𝑒 ∈ 𝛾
   (38)     𝜇 = 𝑀 (𝑛𝑎𝑚𝑒)                               (43)    ∀𝜄 ∈ 𝜇 : ¬ConstExprReqired(𝜄)                          (48)    𝑡𝑦𝑝𝑒 ∈ {void}
   (39)     ∀𝜄 ∈ 𝜇 : ¬CapturesEnvironment(𝜄)           (44)    ∀𝜄 ∈ 𝜇 : IsExpression(𝜄) ∨ IsStatement(𝜄)              (49)    name, A, Δ ⊢ 𝑎𝑟𝑔𝑠 { 𝑎𝑟𝑔𝑠 ′
   (40)     ∀𝜄 ∈ 𝜇 : ¬IsMeta(𝜄)                        (45)    𝛾 = Γ(𝑛𝑎𝑚𝑒)
   (41)     ∀𝜄 ∈ 𝜇 : ¬AddressReqired(𝜄)                (46)    |𝛾 | = 1
                                   M, Γ, A, Δ ⊢ #define name ( args ) body { static void name ( args’ ) { body ; }
                        Rule V: Empty macro argument list             Rule VI: Non-empty macro argument list
                                                                       (50)    name, A, Δ ⊢ 𝑎𝑟𝑔 { 𝑎𝑟𝑔′      (51)      name, A, Δ ⊢ 𝑎𝑟𝑔𝑠 { 𝑎𝑟𝑔𝑠 ′
                              name, A, Δ ⊢        {
                                                                                       name, A, Δ ⊢ 𝑎𝑟𝑔, 𝑎𝑟𝑔𝑠 { 𝑎𝑟𝑔′ , 𝑎𝑟𝑔𝑠 ′
Rule VII: Non-empty macro argument
                 (52)     𝛼 = A(𝑛𝑎𝑚𝑒, 𝑎𝑟𝑔)                           (56)     ∀𝜄 ∈ 𝛼 : ¬SizeReqired(𝜄)                (60)    𝛿 = Δ(𝑛𝑎𝑚𝑒, 𝑎𝑟𝑔)
                 (53)     ∀𝜄 ∈ 𝛼 : ¬CapturesEnvironment(𝜄)           (57)     ∀𝜄 ∈ 𝛼 : ¬ConstExprReqired(𝜄)           (61)    |𝛿 | = 1
                 (54)     ∀𝜄 ∈ 𝛼 : ¬IsMeta(𝜄)                        (58)     ∀𝜄 ∈ 𝛼 : ¬CalledByName(𝜄)               (62)    𝑡𝑦𝑝𝑒 ∈ 𝛿
                 (55)     ∀𝜄 ∈ 𝛼 : ¬AddressReqired(𝜄)                (59)     ∀𝜄 ∈ 𝜇 : IsExpression(𝜄)                (63)    𝑡𝑦𝑝𝑒 ∉ {void}
                                                              name, A, Δ ⊢ 𝑎𝑟𝑔 { 𝑡𝑦𝑝𝑒 𝑎𝑟𝑔

                                      Figure 2: Formal rules for MerC’s translation of macros to C code.


   Finally, MerC checks Premises 9-12 to ensure that the macro’s                       Note that no other parts of the C source code change. MerC’s
type is not void—valid only for functions, not variables—and that                   specification ensures that identical syntax can be used at macro
the macro is monomorphic, i.e., all its expansions have the same type,              invocation sites and the rewritten C variables, functions, or enums,
since C variables are monomorphic. Expanding only to a character                    e.g., Line 3’s usage of QUIT.
type (char), QUIT satisfies these premises. Since QUIT satisfies all                   Rule II identifies macro-to-enum translations. Unlike Rule I, it
premises, MerC can follow Rule I’s conclusion to correctly rewrite                  identifies invocations used where only compile-time constant ex-
the macro definition on Line 1 to a global C variable definition.                   pressions are permitted (Premise 19).
      1   static const char QUIT = ’q’;
      2   void check_quit ( void ) {                                                2.4   Translating Function-like Macros
      3        if ( QUIT == getch () ) exit (0) ;
      4   }                                                                         Rules III and IV translate function-like macros to functions that
                                                                                    do and do not return a value (void functions), respectively. Re-
                                                                                    turning value affects function call site semantics. To demonstrate
Translation Tag Team: Formal Rules and LLMs Translate More Macros Together Than Apart                                              ASE ’26, October 12–16, 2026, Munich, Germany


Rule III, consider the function-like macro MUL(),- which
                                                   C languageexpands         to Public
                                                               icon: ElodinKaldwin,
                                                   domain, via Wikimedia Commons
the expression ((n)) * ((m)):                   - Other images: Flaticon.com
                                                                                                                                  MerC
           1   # define MUL (X , Y ) (( X ) *( Y ) )  - Circle: Input / output
           2   int * new_matrix ( int n , int m ) { - Rectangle: Tool                                                                         Macro translator
                                                      - Yellow: Existing work
           3        return calloc ( MUL (n , m ) , sizeof  ( int
                                                      - Green       ) ) ;Contributions of this paper
                                                                and blue:                                 C code                                                   Translated
           4   }                                                                                       with macros                                                   C code

      Listing 3: MUL() macro definition and invocation.
    Premises 24-30 are the same as those for object-like macros
(Premises 1-7) explained above in Section 2.3.                                                                                     Macro
                                                                                                          Maki
    Premise 31 verifies that MUL() is an expression, because C func-                                                   Macro      analyzer   Translatable macros

tion calls and their return values must be expressions. MUL() sat-                                                   properties

isfies Premise 31 because it expands to an arithmetic expression.
Premises 32-35 check that MUL() has a monomorphic type, since C                                   Figure 3: MerC architecture diagram. Circles are data. Dark
functions are monomorphic. MUL() satisfies premises 32-35 since                                   gray rectangles are novel contributions. Maki is prior work.
its one invocation expands to a single integer type.
    Premise 36 uses Rules VII-VI to translate untyped macro argu-
ments to typed C function arguments. Rules V and VI translate lists                               c2rust). By studying what correct translations checked for, and
of arguments, and Rule VII translates individual arguments. For                                   what incorrect translations failed to consider, we arrived at the
instance, MUL()’s first argument, X. Rule VII first uses Premise 52 to                            set of overlapping features between macros and C code shown in
collect X’s expansions. Premise 53 ensures that X, like C function ar-                            Figure 1. On top of this, we also checked the C preprocessor’s ISO
guments, does not capture identifiers from its caller’s environment.                              specification and user manual to obtain a complete view of all the
X satisfies Premise 53 because it only refers to n, which is passed as                            features macros can exhibit. These overlapping features were then
MUL()’s X argument (Listing 3, Line 3). Like C variables, C function                              used to create the translation rule premises in Figure 2.
arguments lack preprocessor metaprogramming capabilities, and
C function arguments behave differently from macro arguments                                         Correctness. MerC accounts for all possible macros when per-
when used with address-of (&) or size-of operators (Section 2.3).                                 forming its translation, leaving none unconsidered, and only trans-
Premises 55-57 specify these conditions.                                                          lates macros satisfying all the premises of one of Figure 2’s rules.
    Premise 58 validates that the argument does not use call-by-                                  To check these premises for all macros, MerC uses the seman-
name semantics, as function arguments are call-by-value. Call-by-                                 tic Boolean properties returned by the macro analyzer Maki [54],
name semantics evaluate an argument and its side-effects each                                     which has a test suite of 95 tests verifying its accuracy [55]. Maki’s
time it is used in the macro’s body, which may be many, or not                                    semantic properties cover all macros, ensuring that macros unsup-
at all if the macro appears in the unevaluated branch of a short-                                 ported by Figure 2’s rules are left untranslated, while only those
circuiting operation such as logical and (&&). In contrast, call-by-                              matching a rule’s premises are converted to a C construct. MerC’s
value semantics evaluate functions’ arguments exactly once at their                               translation rules guarantee that at most a single translation will
callsites. X satisfies Premise 58 because the first argument to the                               apply to a macro, preventing the inadvertent translation of unsup-
call to MUL() on Line 3 of Listing 3 does not have side-effects, and                              ported macros, with all the MerC translations analyzed in Section 5
MUL()’s definition does not use X in a short-circuiting operation.                                being correct.
    Finally, Premise 59 ensures X is monomorphic, which X is because
it expands to the integer expression n. Satisfying Rule VII’s premises,
                                                                                                  3      MerC Implementation
both macro arguments X and Y can be translated following the                                      Figure 3 shows the architecture of MerC, which inputs unprepro-
rewrite rule to int X and int Y, respectively. Since MUL() and its                                cessed C source code and emits unpreprocessed C source with
arguments satisfy Rule III, the macro can be translated to:                                       supported macros translated to C constructs. MerC is implemented
                                                                                                  in 952 source lines of Python code.
      1   static inline int MUL(int X, int Y) { return ((X)*(Y)); }
                                                                                                     MerC works by first using the macro analyzer Maki [54] to com-
      2   int * new_matrix ( int n , int m ) {
      3        return calloc ( MUL (n , m ) , sizeof ( int ) ) ;                                  pute, for all AST-aligned macro invocations, a set of fine-grained
      4   }                                                                                       Boolean properties about the macro’s semantics. The artifact 2 file
                                                                                                  macros.py then maps these Boolean properties to the functions
   As with object-like macros, this translation is a drop-in replace-                             in Table 1. These helper functions are used by predicates/inter-
ment for the macro and requires no changes to the macro’s callsites.                              face_equivalent.py to implement Figure 2’s rule premises for
MerC also makes MUL()’s translation inline to inline its callsites                                choosing which translation rule, if any, to apply to a given macro.
at compile-time, preserving the original macro’s performance.                                     Finally, the file macrotranslator.py implements each translation
                                                                                                  rule’s conclusion to conduct the actual translation of each macro.
2.5       Derivation and Correctness of Rules                                                        Because MerC’s translation rules preserve the same syntax of
   Derivation. The rules in Figure 2 were derived from studying                                   macro callsites, MerC only ever needs to modify the definitions
prior work on translating C preprocessor usage to C code. We                                      of supported macros to translate them to C constructs. Moreover,
studied translations that were correct but limited (mennie) in scope,                             MerC retains macros’ performance benefits by translating macros to
and translations that were more complete, but unreliable (vs code,                                inline functions. Downstream translators can then convert these
ASE ’26, October 12–16, 2026, Munich, Germany                                                             Brent Pappas, Joseph Zalusky, Zachary Burkett, and Paul Gazzillo


inline functions to compile-time functions in the target language,                             Focus. MacroBench is designed to specifically measure macro
such as Rust’s own macros or #[inline] functions.                                          translation capacity, without penalizing tools for lack of whole
                                                                                           program translation or build system analysis. In particular, LLMs’
4     Macro Translation Benchmark                                                          limited context windows and cloud service input token limits pre-
We introduce MacroBench, the first benchmark specifically focused                          clude prompting them with entire programs, which may comprise
on macro translation. MacroBench is designed to be realistic, varied,                      millions of lines of code, only to evaluate macro translation capacity.
focused, and usable. We constructed MacroBench by randomly                                 Similarly, C programs use build automation to set compiler flags
sampling macro usage from widely-varying, real-world C programs                            and use header files to share common macro definitions across C
to ensure representativeness, independence from any particular                             files. To evaluate macro translation with whole program transla-
translation techniques, and statistical significance.                                      tion would require a tool to handle these pragmatic issues in order
                                                                                           to even observe macro usage. In contrast, MacroBench enables a
4.1      Design Principles                                                                 baseline comparison of macro translation in isolation from whole
                                                                                           program translation pragmatics. To accomplish this, we hand-slice
We adhered to the following principles when creating MacroBench.
                                                                                           the macro definition and invocations into a single C file per macro,
   Realism. MacroBench’s test cases should reflect real-world macro                        preserving any local language usage that surrounds the macro and
usage to best represent a translator’s performance on C code. For                          is used within the macro to retain its semantic context.
realism we base MacroBench on the 26 real-world programs studied
in the seminal work on macro analysis [16], removing 8 programs                               Usability. MacroBench is made to be readily accessible and usable
that use C++ or whose dependencies are no longer available4 . We                           for other researchers to evaluate macro translation to C or other
compensate for the removed programs by adding 5 modern ones:                               languages. We organize MacroBench’s test cases into directories
Linux, Lua, Python, SQLite, and FFMpeg, for a total of 23 programs,                        based on the programs we sampled them from and include build
increasing the benchmark to 100,711 macro definitions5 .                                   automation that researchers and tool designers can use to integrate
   We sample macros with stratified random sampling, where the                             and automate their tool’s translation of the benchmark. We make
strata are the source programs. We calculate the number of macros                          each test case a single file so that AI researchers may directly prompt
sampled from each program based on its number of definitions,                              models to perform translations without also providing header files,
so that all programs contribute at least one macro to MacroBench.                          or whole programs as inputs. Finally, we include the evaluated
Otherwise, small programs would likely contribute no macros, and                           tools’ translations (Section 5) along with the semi-automatically
large programs like the Linux kernel would dominate. To ensure                             validated results of the evaluation, including which translations are
representativeness, we choose a statistically-significant sample size                      correct or incorrect, failure type, locations, descriptions, and other
of 398, for a 95% confidence level and 5% margin of error.                                 metadata, so that future researchers developing macro translations
   Macros in real-world code do not appear in isolation, but are sur-                      have a baseline for comparison. MacroBench is available publicly
rounded by declarations, statements, and expressions. MacroBench                           and is included in the accompanying artifact2 for review.
preserves this context by including the declarations of any variables,
functions, types, or other symbols the sampled macro references,
along with expressions or statements invoking the sampled macro.                           4.2    Benchmark Creation Procedure
                                                                                           We used the following procedure to convert each sampled macro
    Variety. MacroBench’s test cases should contain diverse macro                          into a MacroBench test case. For each test case we created one C
usage to evaluate a translator’s ability to handle the many kinds of                       source file, and copied into it a single sampled macro’s definition
macros real-world C uses. To achieve variety, we sample macros                             and invocation sites. Most macros were only invoked a handful of
from a selection of C software spanning diverse software categories,                       times, and for these test cases we included all invocations. But a
including databases, programming languages, and window manage-                             small number (12%) of macros were invoked thousands of times
ment. Furthermore, by stratifying macros by their source programs                          across many C files, and to include them all would produce a file
we ensure MacroBench includes macros from all programs, even                               too large for input to LLMs. So for these macros, we used a random
small ones, since simple random sampling would likely exclude                              number generator to select a random sample of the macros invo-
macros from small programs altogether. After sampling, we ver-                             cations, and copied these into the test case file. Each such case is
ified by hand that MacroBench contains myriad types of macros                              described in the macro benchmark listing in the accompanying ar-
that have been previously documented by researchers [45], includ-                          tifact2 . For macros invoked within C functions or other constructs,
ing named constants, function name aliases, generic functions,                             to maintain realistic semantics we copied the macro’s surrounding
and metaprogramming macros. 22% are function-like and 78% are                              language constructs, along with any types, variables, additional
object-like, reflecting the distribution found by prior research [16].                     macros, and other symbols that the benchmark macro relies on.
Additionally, we check for diverse semantics [16, 40, 54], such as                         We included context recursively; if a macro depends on the decla-
variable capture, token-pasting, control-flow modifications, and                           ration of some type A that itself depends on type B, we included
more. The complete listing of macros, originating programs, and                            declarations of both A and B in the benchmark. Similarly, since
additional metadata can be found in our accompanying artifact2 .                           macros may be called within other macros, we preserve the calling
4 gcc, gnuchess, gs, mosaic, plan, rasmol, workman, and zephyr.                            context of nested benchmark macros by partially expanding all
5 See the file programs.txt in our public artifact for a listing of each program’s name,   macro invocations until reaching the sampled benchmark macro,
version, source lines of code, and number of invoked and sampled macro definitions.        so that the benchmark macro’s invocation is explicit.
Translation Tag Team: Formal Rules and LLMs Translate More Macros Together Than Apart                                 ASE ’26, October 12–16, 2026, Munich, Germany


5     Evaluation                                                                        MerC, we instrumented MacroBench’s build system to run MerC
We investigate these six research questions about MerC and LLMs.                        on each source file and record the time taken on each test case.
                                                                                           LLM translations were run once per test case. Temperature set-
RQ1 How many translations do tools attempt?
                                                                                        tings used for GPT-4o and Claude 3.5 Sonnet were the default
RQ2 How many translations are failures?
                                                                                        provided by the Copilot VS Code extension since Copilot provided
RQ3 How fast are translations?
                                                                                        no way to change that setting at the time our evaluation was con-
RQ4 How fast and effective are MerC-LLM Tag Teams?
                                                                                        ducted [71]. To remain fair and consistent with using the default
RQ5 What are LLMs’ translations failures?
                                                                                        temperature setting for GPT-4o and Claude 3.5 Sonnet, we used the
RQ6 How does prompting strategy affect LLM translations?
                                                                                        default temperature setting for o1 Preview as well.
                                                                                           We began checking the correctness of all translations by auto-
5.1     LLM Selection                                                                   matically checking for compile-time correctness with GCC. Most
We chose the following LLMs: GPT-4o [47] because it is popular and                      translation failures, 80%, were compile-time errors found using
likely to be used by developers in practice; Claude 3.5 Sonnet [29]                     automated checking with GCC. The remaining 20% of failures not
because it is designed for solving coding tasks [28]; and o1 Pre-                       suffering from compile-time errors were checked (RQ2) and la-
view [48] for its focus on reasoning [49]. We use the GitHub Copilot                    beled (RQ5) by a team of students trained by a co-author. The same
Visual Studio Code extension [30] to translate macros with GPT-                         co-author then validated all results, so that each translation was
4o and Claude 3.5 Sonnet, because Copilot is a popular tool that                        checked at least twice. When a labeling discrepancy arose between
reflects developer LLM usage. GPT-4o is its current default model.                      student and co-author opinion, the co-author had the final say;
Copilot recently added support for Claude 3.5 Sonnet, a model that                      though the number of such discrepancies was small. All our analy-
reportedly “excels at coding tasks” [28]. Since macro translation is                    ses can be found in the accompanying artifact2 .
a coding task, we also use Copilot with Claude 3.5 Sonnet. Finally,
we include o1 Preview6 to represent LLMs with reportedly superior                       5.3    RQ1: How Many Translations do Tools
reasoning [49]. Copilot currently imposes strict daily usage limits                            Attempt?
on this model [31], so we use OpenAI’s own API [50] to evaluate it.
                                                                                        The attempt rate is how many MacroBench test cases a tool at-
                                                                                        tempted to translate, regardless of correctness. We consider a trans-
5.2     Experimental Setup and Methods                                                  lation attempted when the tool translates the macro definition into
We performed the LLM translations using cloud services (Copilot                         a C declaration (variable, function, etc.). For instance, an LLM may
and OpenAI’s) and performed MerC translations on an off-the-shelf                       refuse to translate or leave the input unchanged.
laptop with an 8-core Intel i7-11857G processor and 16GB of RAM.                           Figure 4a is the total number and percent of attempted transla-
   We performed LLM translations following these steps: (1) start a                     tions for each tool. GPT-4o has the greatest attempt rate of 88%,
new chat with the model, (2) prompt the model to translate a test                       while MerC has the lowest attempt rate, 50%. Claude 3.5 Sonnet and
case, (3) record the translation time, and (4) save the translation in                  o1 Preview, designed for better coding and reasoning tasks [28, 49],
a new file. All LLMs were given the same zero-shot [67] prompt:                         have attempt rates between that of GPT-4o and MerC, attempting
 translate this code to pure C, translating the macro MACRO_NAME                        61% and 70% of test cases, respectively. While all LLMs emit more
 to an enum, function, or variable without changing program se-                         translations than MerC, their translations are not always correct.
 mantics or callsites. You are NOT ALLOWED to change the call-
 sites of the macro or create any new macros. Therefore, if it is not                     RQ1: All LLMs attempt more translations than MerC, but their
 possible to translate the macro without preserving the callsites                         correctness is not guaranteed.
 and semantics, do not perform any translation. Report a confi-
 dence level in percentage in the accuracy of the translation in a                      5.4    RQ2: How Many Translations are Failures?
 comment at the end within the code.
                                                                                        A failure is a translation that produces invalid or semantically
 CODE
                                                                                        different C code. The failure rate is the percentage of attempted
MACRO_NAME and CODE are replaced with the name of the macro                             translations that fail. A perfectly accurate translation would attempt
to translate and the code (wrapped in backticks) containing the                         all translations (100% attempt rate) without failures (0% failure rate).
macro from MacroBench, respectively. We developed the prompt                                Figure 4b shows failure rates for each tool on MacroBench. MerC
iteratively, asking LLMs to translate Maki’s [54] macro analysis                        attempts the fewest translations, 198, but emits no incorrect trans-
unit tests and picking the one that worked best. We chose zero-                         lations, for a failure rate of 0%. In contrast, all LLMs emit many
shot prompting because it is a popular prompting strategy [63]                          wrong translations, between 8% and 28%. GPT-4o in particular has
that developers are likely to use in practice due to its ease-of-use                    the highest failure rate of 28%, with 97 of its 350 translations be-
and flexibility [43]. We determined the elapsed translation time for                    ing incorrect. The reasoning-style LLMs (Claude 3.5 Sonnet and
GPT-4o and Claude 3.5 Sonnet from Copilot’s debugging output,                           o1 Preview) have lower failure rates than GPT-4o (13% and 8%,
subtracting the time the model received the request from the time                       respectively), but also attempt fewer translations than GPT-4o as
it finished responding to it. For o1 Preview, we instrumented the                       well (241 and 279 translations, respectively).
request script to collect wall-clock time. To translate test cases with                     The downside of any non-zero failure rate, no matter how small,
                                                                                        is that developers need to validate all LLM translations, even the
6 The full o1 release occurred after we started experiments.                            correct ones, to ensure the correctness of the results, because LLMs
ASE ’26, October 12–16, 2026, Munich, Germany                                                                                                                                                              Brent Pappas, Joseph Zalusky, Zachary Burkett, and Paul Gazzillo


                               398     350 (88%)                                                                  100%                                                                                                                                     150




                                                                                                                                                                                                                           Total translation time (min)
                                                               279 (70%)                                                                                                                                                                                                                                    146




                                                                                       Translation failure rate
      Attempted translations




                               299                 241 (61%)                                                      75%
                                                                           198 (50%)                                                                                                                                                                       100
                               199                                                                                50%                                                                                                                                                                       93

                                                                                                                                    13%                                                                                                                     50
                               100                                                                                25%                         8%                                                                                                                             48
                                                                                                                          28%                                                             0%                                                                                                                                1
                                 0                                                                                 0%                                                                                                                                            0
                                        GPT-4o     Claude 3.5 o1 Preview    MerC                                         GPT-4o   Claude 3.5    o1                       MerC                                                                                              GPT-4o        Claude 3.5 o1 Preview             MerC
                                                    Sonnet                                                                         Sonnet    Preview                                                                                                                                      Sonnet


                                     (a) Attempted translations.                                                    (b) Translation failure rates.                                                                                                        (c) Total translation times (minutes).

 Figure 4: Attempt rates, failure rates, and translation times for LLMs and MerC when translating MacroBench’s test cases.


do not distinguish correct from incorrect translations in their output.
                                                                                                                                                                                                     398
Although we prompted LLMs to report their confidence in the                                                                                                                                                                                                350       356                    Correct formal translations

translation, they almost always reported a high confidence level,                                                                                                                                                                                                                            Hand-validated LLM translations

                                                                                                                                                                                                                                                                                             Incorrect LLM translations
even for incorrect translations. Finally, 30 macros from MacroBench                                                                                                                                                                                                  80
                                                                                                                                                                                                                                                           97                                                        285
                                                                                                                                                                                                                                                                                                             279
were never translated by any approach. These macros use features                                                                                                                                                                                                                             258                     20
                                                                                                                                                                                                                                                                                                             22
like token-pasting [20] that lack a direct C equivalent.                                                                                                                                                                                                                             241
                                                                                                                                                                                                                                                                                                 17
                                                                                                                                                                                                                                                                     78                                              67
                                                                                                                                                                                                                                                                                     31       43
                                                                                                                                                                                                               198




                                                                                                                                                   Translations
                                                                                                                                                                                                     199
  RQ2: MerC had no failures but translates only those macros
  for which it is specifically designed. In contrast, all LLMs made
  more translations but always produced some incorrect ones,                                                                                                                                                                                               253                                              257

  forcing developers to manually verify all translations.                                                                                                                                                      198                                                   198
                                                                                                                                                                                                                                                                                     210
                                                                                                                                                                                                                                                                                             198                     198




5.5                            RQ3: How Fast Are Translations?                                                                                                                                       0
                                                                                                                                                                                                                                                                     With                   With                    With
Figure 4c presents the total time each tool spent translating all test                                                                                                                                         Alone                                      Alone
                                                                                                                                                                                                                                                                     MerC
                                                                                                                                                                                                                                                                                    Alone
                                                                                                                                                                                                                                                                                            MerC
                                                                                                                                                                                                                                                                                                            Alone
                                                                                                                                                                                                                                                                                                                    MerC
cases. Figure 4c shows that, despite running on a personal laptop,                                                                                                                                             MerC                                         GPT-4o                   Claude 3.5              o1 Preview

MerC is orders of magnitude faster than all LLMs, performing all
translations in less than a minute. In contrast, GPT-4o takes 48
minutes to perform all translations, while the more accurate model,                                                                       Figure 5: Types of translations performed by MerC, LLMs,
Claude 3.5 Sonnet, takes an hour and a half, and o1 Preview, the                                                                          and MerC-LLM tag teams.
most accurate model, spends the most time at two and a half hours.
                                                                                                                                                                                                         146
                                                                                                                                                                  Total translation time (minutes)




  RQ3: The rule-based MerC is orders of magnitude faster than                                                                                                                                                            Alone                              Tag team with MerC


  LLMs (seconds vs. hours).                                                                                                                                                                                                                                                                           146
                                                                                                                                                                                                         73
                                                                                                                                                                                                                                                                                    93
                                                                                                                                                                                                                                                                                                              80
                                                                                                                                                                                                                                                             48                             48
                                                                                                                                                                                                           0         1                                                 30
5.6                            RQ4: How Fast and Effective are MerC-LLM                                                                                                                                          MerC                                            GPT-4o             Claude 3.5        o1 Preview

                               Tag Teams?
Neither MerC or LLMs are better in both number of translations                                                                            Figure 6: Total translation times for MerC, LLMs, and tag
and failure rate. But they have complementary strengths: MerC is                                                                          teams. Lower is better. MerC’s 37 seconds rounds to 1 minute.
fast and perfectly accurate while LLMs make more translations. We
unite these complementary strengths into a translation tag team that
first translates with MerC then “tags in” an LLM for the remaining                                                                           Figure 5 compares MerC and the LLMs’ attempts and failures to
macros MerC does not support. The tag team approach reaps greater                                                                         those of MerC-LLM tag teams. Because MerC only produces correct
benefits than either technique alone, decreasing translation time                                                                         translations, the tag team approach only has an average 13% failure
while increasing both the number and accuracy of translations.                                                                            rate (7% to 22%), a 32% reduction in failures compared to using LLMs
    The tag team works better than MerC or LLMs alone, because                                                                            alone. Moreover, since the tag team approach supplements MerC’s
LLMs incorrectly translate some macros that fall within MerC’s                                                                            198 translations with extra LLM translations, the total number of
rules for common macro cases (there are 28 macros that MerC gets                                                                          attempted translations is on average 51% higher (30% to 80%) than
right that at least one LLM tool gets wrong). By avoiding LLM                                                                             MerC’s 198, with an average of 32% more correct translations to
translation of macros that MerC already supports, developers need                                                                         boot. Finally, by translating 198 macros correctly with MerC first
validate fewer translations for correctness. And by using LLMs to                                                                         before using LLMs to translate the remaining MacroBench macros,
translate the remaining macros that MerC does not support, the                                                                            the number of LLM translations needing hand-validation drops by
tag team approach translates more macros overall.                                                                                         66% on average for tag teams compared to using LLMs alone.
Translation Tag Team: Formal Rules and LLMs Translate More Macros Together Than Apart                                  ASE ’26, October 12–16, 2026, Munich, Germany


   Similarly, MerC is orders of magnitude faster than LLMs, translat-                                                     static inline unsigned
                                                                                          #define FRAME_VISIBLE_P(f)
ing 50% of the benchmark in under a minute. Therefore, restricting                            (f)->visible                FRAME_VISIBLE_P(struct frame *f) {
LLM use to a subset of macros greatly reduces overall run-time.                                                               return f->visible;
                                                                                                                          }
Figure 6 shows the total time each LLM spent translating the test                         struct frame {                  struct frame {
cases not first translated by MerC. The MerC-LLM tag teams run                                unsigned visible : 2;           unsigned visible : 2;
in nearly half the time as the LLMs in isolation, with LLMs alone                         };                              };
taking 48 minutes to 2.5 hours, and the MerC-LLM tag teams taking                         Listing            4:           Listing 5: Failed o1 Preview
only 30 minutes to 1.3 hours.                                                             FRAME_VISIBLE_P().              translation.
   We also characterize the gap between what macros MerC cor-
rectly translates and the macros that LLMs correctly translate. There                      The translated code fails to compile because the function trans-
were 103 macros (69 object-like, 34 function-like) correctly trans-                     lation of FRAME_VISIBLE_P() references the struct type frame,
lated by LLMs, but not attempted by MerC. MerC did not attempt                          which is not declared until later in the program. Macros may be
these macros because it failed to find an abstraction-preserving                        defined before any types they reference because macros are dy-
translation. To determine why, we took a random sample of 20 of                         namically scoped, but C functions, being statically scoped, must be
these 103 macros (10 object-like, 10 function-like).                                    defined after any types they reference.
   5 of the 20 sampled macros referenced a symbol declared after
                                                                                           Runtime behavior. All the translated macro’s invocations must
the macro’s definition, meaning that in order to translate the macro,
                                                                                        produce the same result as the original test case before transla-
a developer would need to rearrange the order of definitions in their
                                                                                        tion. We compared each macro to its translated counterpart, and
code, which MerC considers as an abstraction-breaking translation
                                                                                        marked changes in macro behavior (e.g., changes to side-effects)
since it requires more work than simply replacing a macro’s defini-
                                                                                        as failures. For instance, GPT-4o’s translation of the Emacs macro
tion with its translated definition. 4 of the 20 sampled macros were
                                                                                        Vafter_delete changes the macro’s runtime behavior by turning
invoked in a short-circuiting expression (e.g., || or &&), precluding
                                                                                        the macro into a completely new variable, whereas the original
MerC translation because in the general case macros invoked in
                                                                                        macro aliased an existing one (identifiers shortened for space):
such expressions cannot be translated to function calls without
possibly breaking program semantics due to differences between                            #define Vafter_delete \              struct emacs_globals {
function call-by-value and macro call-by-name calling conventions.                           globals.f_Vafter_delete              Lisp_Object f_Vafter_delete;
                                                                                          struct emacs_globals {               };
3 of the 20 sampled macros were not translated because of limita-                            Lisp_Object f_Vafter_delete;
tions with MerC’s implementation: these macros made nested calls                          };                                   extern struct emacs_globals
to other macros, which is a feature that MerC’s underlying macro                          extern struct emacs_globals            globals;
                                                                                             globals;                          Lisp_Object Vafter_delete;
analyses engine, Maki, does not fully support. 2 of the 20 sampled
macros were object-like macros defined to a construct other than a                        Listing   6:    Original             Listing 7: Failed GPT-4o
constant C expression, preventing MerC from translating them in                           Vafter_delete macro.                 translation.
an abstraction-preserving way to variables or enums, but still allow-                      The translation fails to preserve the original program’s behav-
ing for LLMs to translate these macros to functions. The remaining                      ior because the translation of Vafter_delete no longer aliases
macros were not translated, because they were metaprogramming                           globals.f_Vafter_delete, but is rather an entirely new variable.
macros, were used in a preprocessor conditional, or expanded to a
C declaration rather than a C value.                                                       Non-functional behavior. The translated macro must preserve
                                                                                        the program’s memory layout and preprocessor semantics. For in-
                                                                                        stance, translations that alter #ifdef behavior or mutate unions to
  RQ4: Using both MerC and LLMs averages 32% fewer failures                             structs fail to preserve non-functional program behavior, although
  than LLMs alone and 51% more translations than MerC alone.                            these only represent a minority of failures (15% of all LLM fail-
                                                                                        ures). For example, Claude 3.5 Sonnet’s translation of the FFmpeg
                                                                                        macro CONFIG_MOV_MUXER converts a macro used in a preprocessor
                                                                                        conditional into a C enum, changing the conditional’s output:
5.7     RQ5: What Are LLMs’ Translation Failures?
                                                                                          #define CONFIG_MOV_MUXER 1          enum { CONFIG_MOV_MUXER = 1 };
We semi-automatically checked the correctness of each LLM and                             #if CONFIG_MOV_MUXER // true        #if CONFIG_MOV_MUXER // false
MerC translation along the following criteria, recording the first                        const FFOutputFormat                const FFOutputFormat
error found.                                                                              ff_mov_muxer = {                    ff_mov_muxer = {
                                                                                              .p.name = "mov"                     .p.name = "mov"
                                                                                          };                                  };
                                                                                          #endif                              #endif
   Compile-time behavior. Translated code must compile success-
fully without syntax or type errors. We automatically test for com-                       Listing   8:   Original             Listing 9: Failed Claude
pilation errors with gcc, marking translations that fail to com-                          CONFIG_MOV_MUXER macro.             translation.
pile as compile-time failures. For example, consider o1 Preview’s                          The translated code alters the original program’s non-functional
translation of the Emacs macro FRAME_VISIBLE_P(), which fails                           behavior because it moves CONFIG_MOV_MUXER from the preproces-
to compile because the translated version of FRAME_VISIBLE_P()                          sor namespace into the C namespace, altering the output of the pro-
references the struct frame before it is declared:                                      gram’s #if. Since the original program defines CONFIG_MOV_MUXER
ASE ’26, October 12–16, 2026, Munich, Germany                                                                                                                     Brent Pappas, Joseph Zalusky, Zachary Burkett, and Paul Gazzillo


                                                          Not attempted translations    Failed translations      Successful translations           the task to solve [24], while few-shot CoT also adds explanations
                                                    30
                                                                        22                                                                         of the reasoning steps followed in the examples [25]. We evaluate
          Original Zero-shot Translation Failures




                                                                        22                       22                           22
                                                                                                                                                   prompt engineering on o1 Preview specifically. Since it showed the
                                                                        22                        9                           8
                                                    20
                                                                                                                                                   best accuracy (RQ2) and has a reportedly high reasoning capac-
                                                                                                                              5
                                                                                                                                                   ity [49], it stands to benefit the most from prompt engineering [39].
                                                                                                  5
                                                    10                                                                                             The few-shot and CoT prompt templates can be found in our ac-
                                                                                                                              9

                                                                         0
                                                                                                  8
                                                                                                                                                   companying artifact2 in macrobench/prompt_templates.txt.
                                                     0
                                                                    Zero-shot                 Few-shot           Few-shot Chain of Thought
                                                                                                                                                      Figure 7 compares the number of o1 Preview translation failures
                                                                                                                                                   with a zero-shot prompting strategy to the number of translation
                                                                                                                                                   failures under few-shot and few-shot CoT prompting strategies.
Figure 7: Comparison of the number of o1 Preview’s failed                                                                                          o1 Preview made 22 incorrect (out of 279 attempted) test case trans-
translations under various prompting strategies.                                                                                                   lations with the zero-shot prompt (Section 5.4). With few-shot,
                                                                                                                                                   o1 Preview correctly translated eight of these cases, still incorrectly
to 1, the conditional will evaluate to true and declare the variable                                                                               translated five of them, and did not attempt the remaining nine.
ff_mov_muxer. But because the translated code converts the macro                                                                                   Few-shot CoT was similar, only correctly translating one additional
to an enum, which is not a preprocessor symbol, the #if will eval-                                                                                 case that was not attempted with the few-shot prompt. While the
uate to false, and ff_mov_muxer will never be declared.                                                                                            prompting strategies helped reduce failed translations they also
                                                                                                                                                   made o1 Preview more selective in avoiding translation altogether.
                                                                      MerC             GPT-4o                 Claude 3.5              o1 Preview     RQ6: Few-shot and few-shot CoT reduced failed translations
  Compile Time                                                               0           76                       26                         18      but also resulted in fewer attempts on prior failed translations.
  Runtime                                                                    0           4                        2                          2
  Non-functional                                                             0           17                       3                          2
                                                                                                                                                   6 Threats to Validity
  Total                                                                      0           97                       31                         22
                                                                                                                                                   6.1 Internal Threats
                                                         Table 2: Types of failed translations.
                                                                                                                                                      MerC translation scope. MerC only translates macros expanding
                                                                                                                                                   to complete C constructs, and not those expanding to C syntax
                                                                                                                                                   fragments. However, users can translate nested macro invocations
   Table 2 presents the number of test cases that each tool trans-                                                                                 by repeatedly running MerC on its own output to “peel back” layers
lated incorrectly. MerC had no failures. For LLMs, the majority of                                                                                 of nested macro usage until no more translations occur.
translation failures were compile-time errors. Roughly half of all
                                                                                                                                                       LLM selection. Section 5’s results on how well LLMs translate
compile-time errors for GPT-4o and Claude 3.5 Sonnet were due to
                                                                                                                                                   macros should represent real-world developer LLM usage. To this
the use of non-constant values where constant values were required.
                                                                                                                                                   end, we evaluate GPT-4o because it is popular, Claude 3.5 Sonnet
This reflects a misunderstanding of C semantics and the common
                                                                                                                                                   because it is designed for coding tasks [28], and o1 Preview [49] for
use of macros to define constants: macros get expanded before C
                                                                                                                                                   its focus on reasoning. To further reflect developer LLM usage, we
compilation, so they can be used where C variables cannot.
                                                                                                                                                   evaluate GPT-4o and Claude 3.5 Sonnet with the GitHub Copilot
   For o1 Preview, however, the majority of compile-time errors (14
                                                                                                                                                   Visual Studio Code Extension [30]. Although Copilot also supports
out of 18) were due to type errors, specifically undeclared references.
                                                                                                                                                   o1 Preview, it currently imposes strict daily usage limits on the
On one hand, this indicates that o1 Preview is better at avoiding
                                                                                                                                                   model [31], so we use OpenAI’s own API [50] to evaluate it6 .
syntactic errors, but on the other it also suggests that the model
misunderstands how the preprocessor interacts with C’s typing                                                                                         LLM prompting. To ensure Section 5 evaluates LLMs with a qual-
rules. For example, Listing 5 presents an o1 Preview-translated                                                                                    ity prompt, we designed our prompt iteratively by asking LLMs to
macro argument which suffers a type error because it references a                                                                                  translate small random samples of macros from Maki’s [54] macro
type declared later in the program. MerC avoids compile-time errors                                                                                analysis test cases until all LLMs performed the task as instructed.
because its translation rules encode both C syntax and semantics.
                                                                                                                                                      LLM performance results. To ensure Section 5.5 accurately por-
  RQ5: MerC correctly translates all attempted test cases, while                                                                                   trays LLM performance on macro translation, we ran the LLMs us-
  LLMs’ failed translations typically have compile-time errors.                                                                                    ing cloud services, since real developers are likely to lack dedicated
                                                                                                                                                   AI machines, and instead use LLMs directly from their providers.

5.8     RQ6: How Does Prompting Strategy Affect                                                                                                      Independence of the benchmark. To prevent biasing MacroBench
        LLM Translations?                                                                                                                          towards MerC, we designed the benchmark independently from
                                                                                                                                                   MerC’s translation rules, with randomly selected test cases to avoid
All LLM translations were conducted using a zero-shot prompt (Sec-
                                                                                                                                                   even inadvertently specializing MerC to MacroBench. MacroBench
tion 5.2). To evaluate whether a different prompting strategy would
                                                                                                                                                   was created after MerC was developed, and by a separate author.
improve on failed LLM translations, we evaluated two additional
popular prompting strategies, few-shot [4] and few-shot chain-of-                                                                                    Inter-rater agreement. We did not use a formal inter-rater agree-
thought (CoT) [73]. Few-shot prompts include example solutions of                                                                                  ment metric when identifying and classifying failed translations in
Translation Tag Team: Formal Rules and LLMs Translate More Macros Together Than Apart                                 ASE ’26, October 12–16, 2026, Munich, Germany


Section 5. To address this threat, a student and a co-author checked                    7    Related Work
each translation, and then met to resolve discrepancies and arrive                         Translating C preprocessor macros. Mennie and Clarke described
at a final mutually agreed label for each translation. Afterwards, the                  the first automated macro translation tool in 2004 [45]. Their tool
same co-author verified that all translation labels were consistent.                    is not publicly available, and only translates constant object-like
                                                                                        macros into C variables and enums, whereas MerC also translates
                                                                                        function-like macros into C functions. Macroscope [44] translates C
6.2     External Threats                                                                preprocessor code to ASTEC code, but fails to help translate macro-
  Benchmark representativeness. To ensure Section 5’s findings                          laden C code to safer languages since ASTEC is itself a preprocess-
about macro translation generalize to real developer scenarios, we                      ing language. Kumar et al. discussed “rejuvenating” C++ programs
draw MacroBench’s test cases from the 23 programs described in                          by translating C preprocessor macros to C++ [40]. Unlike MerC,
Section 4, which vary in size, complexity, and application domains.                     their translation is not fully automatic, translates to C++ instead of
                                                                                        C, and is sometimes incorrect because it ignores macro invocation
                                                                                        semantics. C2rust can translate some C preprocessor macros to
   Translation of macros from compile-time to run-time abstractions.                    Rust [11], but this feature has correctness issues [12, 60]. Visual Stu-
By translating macros to C, MerC gives downstream translators                           dio can refactor certain macro definitions into constant expression
the ability to choose how to translate each macro in a way that                         declarations [57], but this feature has bugs [59]. Macroni [53, 69]
best preserves its abstraction. But translating macros into func-                       translates C preprocessor macros to LLVM MLIR [41], but not to C.
tions threatens to reduce program performance, since macros are
                                                                                            Translating C preprocessor conditionals. Tools exist for translating
compile-time abstractions, and functions are run-time abstractions.
                                                                                        C preprocessor conditionals [26, 42, 56, 58, 70], but they do not
MerC mitigates this threat by converting all C macros into inline
                                                                                        translate macros, and therefore suffer the same issues as other C
functions, which are expanded at their callsites by the compiler to
                                                                                        translators. Such tools expand macros in C code before translating
remove the overhead associated with entering and exiting func-
                                                                                        it, preventing downstream C translators from preserving macros
tion calls. Downstream translation tools can then convert these
                                                                                        in their translations. MerC could be used to translate macros first
inline functions into compile-time constructs in the target language
                                                                                        before translating preprocessor conditionals to enable macro-aware
to not only preserve the original macro’s abstraction, but also its
                                                                                        variability analysis and verification.
performance. For example, in order to preserve runtime perfor-
mance, c2rust could convert MerC-translated macros into inline                             Analyzing C preprocessor usage. Badros and Notkin presented
Rust functions [61], or even Rust macros [62].                                          the first preprocessor-aware C source code analyzer, Pcp3 [2], in
                                                                                        2000. Ernst et al. used PCp3 to conduct the first empirical study
                                                                                        of C preprocessor usage [16]. Although they found 75% of macros
   Translating whole programs. MacroBench represents real-world                         to be constants or expressions, this provides an incomplete pic-
macro translation tasks, but factors out practical challenges of                        ture of macro translatability since their analysis only considered
whole program translation so as to enable evaluating LLMs, whose                        macro definitions, and ignored invocation semantics. Dietrich pre-
limited input windows do not support large C programs as trans-                         sented CppSig for inferring macros’ function signatures from their
lation inputs. In contrast, although MerC is designed to translate                      invocations [14], and inferred return types and argument types for
single compilation units and not whole programs, it can be applied                      over 50% of Linux kernel macro definitions. Pappas and Gazzillo
to whole programs by translating each of their compilation units                        constructed a framework of 26 Boolean properties for measuring
individually. We use this strategy to explore how well MerC trans-                      macro portability, and built on CppSig to implement it as a tool
lates macros appearing organically in the 23 real-world C programs                      called Maki [54]. MerC in turn uses Maki’s properties as input for
from which MacroBench was drawn. Translations were run in par-                          deciding if and how to translate macros to C language constructs.
allel on a server with 2x AMD EPYC 7742 64-Core and 512GB RAM.
MerC took 9.5 days to analyze all programs, most of which was                              Translating code with LLMs. There exist many code-generating
spent on the Linux kernel, which required 8.5 days. The median                          LLMs [1, 17, 18, 29, 46, 48, 72, 75], with some models designed specif-
analysis time was about 2 minutes per program. After analysis,                          ically for translation [76]. Pan et al. compared the effectiveness of
MerC took 2 minutes to convert all 8,211 macros, with a median                          seven models for translating code in seven datasets spanning four
translation time of 1 second. We check correctness by compiling                         programming languages [52], and found GPT-4o to emit the great-
the translated programs and running their built-in test suites. All 23                  est percentage of correct translations. Section 5.4 shows that the
successfully compile and pass tests after MerC translation. Out of                      newer Claude 3.5 Sonnet and o1 Preview models boast even lower
100,711 total invocations, MerC finds and translates 8,211 of them                      translation failure rates than GPT-4o, demonstrating how these
(8%). This percentage is low partly because some macro definitions                      more recent models improve on prior ones.
are defined in header files shared across compilation units, and so
can’t be translated without additional specifications for the seman-                    Acknowledgments
tics of whole program macro usage. Another reason is that MerC                          This work is supported in part by the National Science Foundation
only translates macros that are not called within other macros; this                    under grant CCF-1941816. We thank Adam Betinsky, Kenneth Val-
limitation can be overcome by repeatedly using MerC to translate                        ladares, and Ehigie Ekata for helping check and label the macro
programs until no more translations occur. This approach would                          translations in Section 5. We thank the anonymous reviewers for
always terminate, as macros have bounded recursion [23].                                their feedback, which helped improve the paper’s quality.
ASE ’26, October 12–16, 2026, Munich, Germany                                                              Brent Pappas, Joseph Zalusky, Zachary Burkett, and Paul Gazzillo


Data-Availability Statement                                                              [21] Free Software Foundation, Inc. 2025. Macros (The C Preprocessor). https://gcc.
                                                                                              gnu.org/onlinedocs/cpp/Macros.html.
We make MerC, MacroBench, and our experimental scripts and re-                           [22] Free Software Foundation, Inc. 2025. Stringizing (The C Preprocessor). https:
sults publicly available in our anonymized artifact [3]. The artifact                         //gcc.gnu.org/onlinedocs/cpp/Stringizing.html.
                                                                                         [23] Free Software Foundation, Inc. 2025. Stringizing (The C Preprocessor). https:
contains all macros used to create MacroBench, their originating                              //gcc.gnu.org/onlinedocs/cpp/Self-Referential-Macros.html.
programs, how many of their invocations are included in Mac-                             [24] Vrunda Gadesha. 2024. What is few shot prompting? https://www.ibm.com/
roBench, and additional metadata. This metadata includes each                                 think/topics/few-shot-prompting.
                                                                                         [25] Vrunda Gadesha and Eda Kavlakoglu. 2024. What is chain of thoughts (CoT)?
tool’s translation speed, whether it translated each macro correctly,                         https://www.ibm.com/think/topics/chain-of-thoughts.
reasons why failed macro translations were unsuccessful, and what                        [26] Florian Garbe. 2017. Performance Measurement of C Software Product Lines.
C constructs each tool attempted to translate each macro to. The                              Master’s thesis. University of Passau. https://www.se.cs.uni-saarland.de/theses/
                                                                                              FlorianGarbeMA.pdf
artifact also provides our zero-shot, few-shot and chain-of-thought                      [27] Paul Gazzillo and Robert Grimm. 2012. SuperC: Parsing All of C by Taming the
prompt templates in macrobench/prompt_templates.txt.                                          Preprocessor. SIGPLAN Not. 47, 6 (June 2012), 323–334. doi:10.1145/2345156.
                                                                                              2254103
                                                                                         [28] GitHub. 2024.      Bringing developer choice to Copilot with Anthropic’s
References                                                                                    Claude 3.5 Sonnet, Google’s Gemini 1.5 Pro, and OpenAI’s o1-preview.
 [1] Loubna Ben Allal, Raymond Li, Denis Kocetkov, Chenghao Mou, Christopher                  https://github.blog/news-insights/product-news/bringing-developer-choice-
     Akiki, Carlos Munoz Ferrandis, Niklas Muennighoff, Mayank Mishra, Alex Gu,               to-copilot/#anthropics-claude-3-5-sonnet.
     Manan Dey, Logesh Kumar Umapathi, Carolyn Jane Anderson, Yangtian Zi,               [29] GitHub. 2024.        Claude 3.5 Sonnet is now available in public pre-
     Joel Lamy Poirier, Hailey Schoelkopf, Sergey Troshin, Dmitry Abulkhanov,                 view. https://github.blog/changelog/2024-11-01-claude-3-5-sonnet-is-now-
     Manuel Romero, Michael Lappert, Francesco De Toni, Bernardo García del                   available-to-all-copilot-users-in-public-preview/.
     Río, Qian Liu, Shamik Bose, Urvashi Bhattacharyya, Terry Yue Zhuo, Ian Yu,          [30] GitHub. 2025. GitHub Copilot. https://marketplace.visualstudio.com/items?
     Paulo Villegas, Marco Zocca, Sourab Mangrulkar, David Lansky, Huu Nguyen,                itemName=GitHub.copilot.
     Danish Contractor, Luis Villa, Jia Li, Dzmitry Bahdanau, Yacine Jernite, Sean       [31] GitHub. 2025. Prototyping with AI models. https://docs.github.com/en/github-
     Hughes, Daniel Fried, Arjun Guha, Harm de Vries, and Leandro von Werra.                  models/prototyping-with-ai-models#rate-limits.
     2023. SantaCoder: don’t reach for the stars! arXiv:2301.03988 [cs.SE] https:        [32] Jaemin Hong and Sukyoung Ryu. 2024. Type-migrating C-to-Rust translation
     //arxiv.org/abs/2301.03988                                                               using a large language model. Empirical Softw. Engg. 30, 1 (Oct. 2024), 38 pages.
 [2] Greg Badros and David Notkin. 2000. A Framework for Preprocessor-Aware C                 doi:10.1007/s10664-024-10573-2
     Source Code Analyses. Software Prac. Experience 30 (July 2000). doi:10.1002/        [33] Immunant. 2018. c2rust. https://github.com/immunant/c2rust/issues/16.
     (SICI)1097-024X(20000710)30:8<907::AID-SPE324>3.3.CO;2-9                            [34] Immunant inc. 2023. c2rust. https://github.com/immunant/c2rust.
 [3] Brent Pappas, Joseph Zalusky, Zachary Burkett and Paul Gazzillo. 2026. Arti-        [35] Immunant inc. 2023. c2rust. https://github.com/immunant/c2rust/tree/
     fact for Translation Tag Team: Formal Rules and LLMs Translate More Macros               3e0183e4d56f9d4d003f1ea2e9a814648debf307.
     Together than Apart. https://doi.org/10.5281/zenodo.21798007.                       [36] ISO/IEC JTC 1. 2024. Information technology – Programming languages – C.
 [4] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan,                  Standard 9899:1990. International Organization for Standardization. https://
     Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda               www.iso.org/standard/17782.html
     Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan,       [37] JTC1/SC22/WG14. 2024. Information technology – Programming languages –
     Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter,               C. Standard 9899:2024. International Organization for Standardization. https:
     Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin          //www.iso.org/standard/82075.html
     Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya           [38] Christian Kästner, Paolo G. Giarrusso, Tillmann Rendel, Sebastian Erdweg, Klaus
     Sutskever, and Dario Amodei. 2020. Language models are few-shot learners. In             Ostermann, and Thorsten Berger. 2011. Variability-Aware Parsing in the Presence
     Proceedings of the 34th International Conference on Neural Information Processing        of Lexical Macros and Conditional Compilation. In Proceedings of the 2011 ACM
     Systems (Vancouver, BC, Canada) (NIPS ’20). Curran Associates Inc., Red Hook,            International Conference on Object Oriented Programming Systems Languages and
     NY, USA, Article 159, 25 pages.                                                          Applications (Portland, Oregon, USA) (OOPSLA ’11). Association for Computing
 [5] Elliot Chance. 2021. c2go. https://github.com/elliotchance/c2go.                         Machinery, New York, NY, USA, 805–824. doi:10.1145/2048066.2048128
 [6] CISA. 2023. The Case for Memory Safe Roadmaps. https://www.cisa.gov/sites/          [39] KratosLab. 2025. Prompt Engineering for OpenAI’s O1 and O3-mini Reason-
     default/files/2023-12/The-Case-for-Memory-Safe-Roadmaps-508c.pdf.                        ing Models. https://kratoslab.com/prompt-engineering-for-openais-o1-and-o3-
 [7] Correct Computation Inc. 2021. 3C. https://github.com/correctcomputation/                mini-reasoning-models/.
     checkedc-clang/.                                                                    [40] Aditya Kumar, Andrew Sutton, and Bjarne Stroustrup. 2012. Rejuvenating C++
 [8] Correct Computation Inc. 2021. 3C. https://github.com/correctcomputation/                programs through demacrofication. In 2012 28th IEEE International Conference on
     checkedc-clang/issues/400.                                                               Software Maintenance (ICSM). Institute of Electrical and Electronics Engineers,
 [9] Correct Computation Inc. 2021. 3C. https://github.com/correctcomputation/                445 Hoes Ln, Piscataway, NJ 08854, United States, 98–107. doi:10.1109/ICSM.2012.
     checkedc-clang/issues/40.                                                                6405259
[10] Correct Computation Inc. 2021. 3C. https://github.com/correctcomputation/           [41] Chris Lattner, Mehdi Amini, Uday Bondhugula, Albert Cohen, Andy Davis,
     checkedc-clang/issues/439.                                                               Jacques Pienaar, River Riddle, Tatiana Shpeisman, Nicolas Vasilache, and Olek-
[11] Stephen Crane. 2020. Document and (potentially) stabilize –translate-const-              sandr Zinenko. 2021. MLIR: scaling compiler infrastructure for domain spe-
     macros. https://github.com/immunant/c2rust/issues/304.                                   cific computation. In Proceedings of the 2021 IEEE/ACM International Sympo-
[12] Stephen Crane. 2023. long double #defines incompatible with –translate-const-            sium on Code Generation and Optimization (Virtual Event, Republic of Korea)
     macros. https://github.com/immunant/c2rust/issues/829.                                   (CGO ’21). IEEE Press, 445 Hoes Ln, Piscataway, NJ 08854, United States, 2–14.
[13] DARPA. 2024. Translating All C TO Rust (TRACTOR). https://sam.gov/opp/                   doi:10.1109/CGO51591.2021.9370308
     1e45d648886b4e9ca91890285af77eb7/view.                                              [42] Alex Lazar and Jean Melo. 2017. C Reconfigurator. https://github.com/itu-
[14] Christian Dietrich. 2021. CppSig: Extracting Type Information for C-Preprocessor         square/c-reconfigurator.
     Macro Expansions. Association for Computing Machinery, New York, NY, USA,           [43] Yinheng Li. 2023. A Practical Survey on Zero-shot Prompt Design for In-context
     62–68. https://doi.org/10.1145/3477113.3487268                                           Learning. In Proceedings of the Conference Recent Advances in Natural Language
[15] Mehmet Emre, Ryan Schroeder, Kyle Dewey, and Ben Hardekopf. 2021. Trans-                 Processing - Large Language Models for Natural Language Processings (RANLP).
     lating C to Safer Rust. Proc. ACM Program. Lang. 5, OOPSLA, Article 121 (Oct.            INCOMA Ltd., Shoumen, BULGARIA, Shoumen, Bulgaria, 641–647. doi:10.26615/
     2021), 29 pages. doi:10.1145/3485498                                                     978-954-452-092-2_069
[16] Michael D. Ernst, Greg J. Badros, and David Notkin. 2002. An Empirical Analysis     [44] Bill McCloskey and Eric Brewer. 2005. ASTEC: A New Approach to Refactoring C.
     of C Preprocessor Use. IEEE Trans. Softw. Eng. 28, 12 (Dec. 2002), 1146–1170.            SIGSOFT Softw. Eng. Notes 30, 5 (Sept. 2005), 21–30. doi:10.1145/1095430.1081712
     doi:10.1109/TSE.2002.1158288                                                        [45] Christopher A. Mennie and Charles L. A. Clarke. 2004. Giving meaning to macros.
[17] Mark Chen et al. 2021. Evaluating Large Language Models Trained on Code.                 Proceedings. 12th IEEE International Workshop on Program Comprehension, 2004.
     arXiv:2107.03374 [cs.LG] https://arxiv.org/abs/2107.03374                                12 (2004), 79–85. https://api.semanticscholar.org/CorpusID:26483462
[18] Raymond Li et al. 2023.           StarCoder: may the source be with you!            [46] Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou,
     arXiv:2305.06161 [cs.CL] https://arxiv.org/abs/2305.06161                                Silvio Savarese, and Caiming Xiong. 2023. CodeGen: An Open Large Language
[19] Dwayne Forde. 2024. Working with AI (Part 2): Code Conversion. https://blog.             Model for Code with Multi-Turn Program Synthesis. arXiv:2203.13474 [cs.LG]
     withmantle.com/code-conversion-using-ai/                                                 https://arxiv.org/abs/2203.13474
[20] Free Software Foundation, Inc. 2025. Concatenation (The C Preprocessor). https:
     //gcc.gnu.org/onlinedocs/cpp/Concatenation.html.
Translation Tag Team: Formal Rules and LLMs Translate More Macros Together Than Apart                                        ASE ’26, October 12–16, 2026, Munich, Germany


[47] OpenAI. 2024. Hello GPT-4o. https://openai.com/index/hello-gpt-4o/.                      https://arxiv.org/abs/2406.06608
[48] OpenAI. 2024. Introducing OpenAI o1-preview. https://openai.com/index/              [64] Jamey Sharp. 2017. Corrode. https://github.com/jameysharp/corrode/tree/
     introducing-openai-o1-preview/.                                                          84c6d7b5dedb32093ada9420ebd9f020828af6c5.
[49] OpenAI. 2024. Learning to reason with LLMs. https://openai.com/index/learning-      [65] Momoko Shiraishi and Takahiro Shinagawa. 2024. Context-aware Code
     to-reason-with-llms/.                                                                    Segmentation for C-to-Rust Translation using Large Language Models.
[50] OpenAI. 2024. Overview - OpenAI API. https://platform.openai.com/docs/                   arXiv:2409.10506 [cs.SE] https://arxiv.org/abs/2409.10506
     overview.                                                                           [66] Diomidis Spinellis. 2003. Global Analysis and Transformations in Preprocessed
[51] Yoann Padioleau. 2009. Parsing C/C++ Code without Pre-Processing. In Pro-                Languages. IEEE Trans. Softw. Eng. 29, 11 (Nov. 2003), 1019–1030. doi:10.1109/
     ceedings of the 18th International Conference on Compiler Construction: Held             TSE.2003.1245303
     as Part of the Joint European Conferences on Theory and Practice of Software,       [67] Vrunda Gadesha Meredith Syed. 2025. What is zero-shot prompting? https:
     ETAPS 2009 (York, UK) (CC ’09). Springer-Verlag, Berlin, Heidelberg, 109–125.            //www.ibm.com/think/topics/zero-shot-prompting.
     doi:10.1007/978-3-642-00722-4_9                                                     [68] The Linux Kernel. 2024. Linux kernel coding style. https://github.com/torvalds/
[52] Rangeet Pan, Ali Reza Ibrahimzada, Rahul Krishna, Divya Sankar, Lam-                     linux/blob/master/Documentation/process/coding-style.rst#12-macros-enums-
     bert Pouguem Wassi, Michele Merler, Boris Sobolev, Raju Pavuluri, Saurabh                and-rtl. Section 12, Macros, Enums and RTL.
     Sinha, and Reyhaneh Jabbarvand. 2024. Lost in Translation: A Study of Bugs          [69] Trail of Bits. 2023. Macroni. https://github.com/trailofbits/macroni.
     Introduced by Large Language Models while Translating Code. In Proceedings          [70] Alexander von Rhein, Thomas Thüm, Ina Schaefer, Jörg Liebig, and Sven Apel.
     of the IEEE/ACM 46th International Conference on Software Engineering (Lisbon,           2016. Variability encoding: From compile-time to load-time variability. Journal of
     Portugal) (ICSE ’24). Association for Computing Machinery, New York, NY, USA,            Logical and Algebraic Methods in Programming 85, 1, Part 2 (2016), 125–145. doi:10.
     Article 82, 13 pages. doi:10.1145/3597503.3639226                                        1016/j.jlamp.2015.06.007 Formal Methods for Software Product Line Engineering.
[53] Brent Pappas. 2023. Holy Macroni! A recipe for progressive language en-             [71] vs-code-engineering. 2025. Temperature Setting · Issue #258748 · microsoft-
     hancement. https://blog.trailofbits.com/2023/09/11/holy-macroni-a-recipe-for-            /vscode — github.com. https://github.com/microsoft/vscode/issues/258748#
     progressive-language-enhancement/.                                                       issuecomment-3662247602. [Accessed 19-06-2026].
[54] Brent Pappas and Paul Gazzillo. 2024. Semantic Analysis of Macro Usage for          [72] Yue Wang, Weishi Wang, Shafiq Joty, and Steven C. H. Hoi. 2021. CodeT5:
     Portability. In 2024 IEEE/ACM 46th International Conference on Software Engineer-        Identifier-aware Unified Pre-trained Encoder-Decoder Models for Code Un-
     ing (ICSE). Association for Computing Machinery, 1601 Broadway, 10th Floor               derstanding and Generation. In Proceedings of the 2021 Conference on Empir-
     New York, NY 10019-7434, 229–240. doi:10.1145/3597503.3623323                            ical Methods in Natural Language Processing, Marie-Francine Moens, Xuanjing
[55] Brent Pappas, Joseph Zalusky, Zachary Burkett, and Donovan Reynolds. 2026.               Huang, Lucia Specia, and Scott Wen tau Yih (Eds.). Association for Compu-
     Macros. https://github.com/appleseedlab/maki. [Accessed 07-09-2026].                     tational Linguistics, Online and Punta Cana, Dominican Republic, 8696–8708.
[56] Zachary Patterson, Zenong Zhang, Brent Pappas, Shiyi Wei, and Paul Gazzillo.             doi:10.18653/v1/2021.emnlp-main.685
     2022. SugarC: scalable desugaring of real-world preprocessor usage into pure        [73] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei
     C. In Proceedings of the 44th International Conference on Software Engineering           Xia, Ed Chi, Quoc V Le, and Denny Zhou. 2022. Chain-of-Thought Prompting
     (Pittsburgh, Pennsylvania) (ICSE ’22). Association for Computing Machinery,              Elicits Reasoning in Large Language Models. In Advances in Neural Information
     New York, NY, USA, 12 pages. doi:10.1145/3510003.3512763                                 Processing Systems, S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and
[57] Augustin Popa. 2018. Convert Macros to Constexpr. https://devblogs.microsoft.            A. Oh (Eds.), Vol. 35. Curran Associates, Inc., 57 Morehouse Ln, Red Hook, NY
     com/cppblog/convert-macros-to-constexpr/.                                                12571, United States, 24824–24837. https://proceedings.neurips.cc/paper_files/
[58] H. Post and C. Sinz. 2008. Configuration Lifting: Verification meets Software            paper/2022/file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf
     Configuration. In Proceedings of the 23rd IEEE/ACM International Conference on      [74] White House Office of the National Cyber Director. 2024.                     Back
     Automated Software Engineering (ASE ’08). IEEE Computer Society, USA, 347–350.           to the Building Blocks: A Path Toward Secure and Measurable Soft-
     doi:10.1109/ASE.2008.45                                                                  ware. https://www.whitehouse.gov/wp-content/uploads/2024/02/Final-ONCD-
[59] Sanjeev Reddy. 2018.        Auto refactor of a macro followed by a com-                  Technical-Report.pdf.
     ment to a constexpr put the semicolon after the comment.                   https:   [75] Frank F. Xu, Uri Alon, Graham Neubig, and Vincent Josua Hellendoorn. 2022. A
     //developercommunity.visualstudio.com/t/auto-refactor-of-a-macro-followed-               systematic evaluation of large language models of code. In Proceedings of the 6th
     by-a-comment-to/354205.                                                                  ACM SIGPLAN International Symposium on Machine Programming (San Diego,
[60] Remmirad. 2023. Problematic macro translation with –translate-const-macros.              CA, USA) (MAPS 2022). Association for Computing Machinery, New York, NY,
     https://github.com/immunant/c2rust/issues/803.                                           USA, 1–10. doi:10.1145/3520312.3534862
[61] Rust Team. 2026. Code Generation Attributes. https://doc.rust-lang.org/             [76] Qinkai Zheng, Xiao Xia, Xu Zou, Yuxiao Dong, Shan Wang, Yufei Xue, Lei
     reference/attributes/codegen.html#the-inline-attribute. [Accessed 07-09-2026].           Shen, Zihan Wang, Andi Wang, Yang Li, Teng Su, Zhilin Yang, and Jie Tang.
[62] Rust Team. 2026. Macros. https://doc.rust-lang.org/book/ch20-05-macros.html.             2023. CodeGeeX: A Pre-Trained Model for Code Generation with Multilingual
     [Accessed 07-09-2026].                                                                   Benchmarking on HumanEval-X. In Proceedings of the 29th ACM SIGKDD Con-
[63] Sander Schulhoff, Michael Ilie, Nishant Balepur, Konstantine Kahadze, Amanda             ference on Knowledge Discovery and Data Mining (Long Beach, CA, USA) (KDD
     Liu, Chenglei Si, Yinheng Li, Aayush Gupta, HyoJung Han, Sevien Schul-                   ’23). Association for Computing Machinery, New York, NY, USA, 5673–5684.
     hoff, Pranav Sandeep Dulepet, Saurav Vidyadhara, Dayeon Ki, Sweta Agrawal,               doi:10.1145/3580305.3599790
     Chau Pham, Gerson Kroiz, Feileen Li, Hudson Tao, Ashay Srivastava, Hevan-
     der Da Costa, Saloni Gupta, Megan L. Rogers, Inna Goncearenco, Giuseppe             Received 2026-03-09; accepted 2026-06-18
     Sarli, Igor Galynker, Denis Peskoff, Marine Carpuat, Jules White, Shyamal Anad-
     kat, Alexander Hoyle, and Philip Resnik. 2025. The Prompt Report: A Sys-
     tematic Survey of Prompt Engineering Techniques. arXiv:2406.06608 [cs.CL]
