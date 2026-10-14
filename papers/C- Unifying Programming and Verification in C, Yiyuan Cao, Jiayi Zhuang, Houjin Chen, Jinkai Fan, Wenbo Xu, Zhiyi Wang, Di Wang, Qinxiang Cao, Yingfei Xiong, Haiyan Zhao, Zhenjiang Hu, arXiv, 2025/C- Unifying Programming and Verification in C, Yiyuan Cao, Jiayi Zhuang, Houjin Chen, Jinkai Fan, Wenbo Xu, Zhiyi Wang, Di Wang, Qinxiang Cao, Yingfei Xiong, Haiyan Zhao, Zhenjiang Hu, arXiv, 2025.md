                                        C★: Unifying Programming and Verification in C
                                        YIYUAN CAO, Peking University, China
                                        JIAYI ZHUANG, Peking University, China
                                        HOUJIN CHEN, Peking University, China
arXiv:2504.02246v1 [cs.PL] 3 Apr 2025




                                        JINKAI FAN, Peking University, China
                                        WENBO XU, Peking University, China
                                        ZHIYI WANG, Peking University, China
                                        DI WANG, Peking University, China
                                        QINXIANG CAO, Shanghai Jiao Tong University, China
                                        YINGFEI XIONG, Peking University, China
                                        HAIYAN ZHAO, Peking University, China
                                        ZHENJIANG HU, Peking University, China
                                        Ensuring the correct functionality of systems software, given its safety-critical and low-level nature, is a
                                        primary focus in formal verification research and applications. Despite advances in verification tooling,
                                        conventional programmers are rarely involved in the verification of their own code, resulting in higher
                                        development and maintenance costs for verified software. A key barrier to programmer participation in
                                        verification practices is the disconnect of environments and paradigms between programming and verification
                                        practices, which limits accessibility and real-time verification.
                                           We introduce C★, a proof-integrated language design for C programming. C★ extends C with verification
                                        capabilities, powered by a symbolic execution engine and an LCF-style proof kernel. It enables real-time
                                        verification by allowing programmers to embed proof-code blocks alongside implementation code, facilitating
                                        interactive updates to the current proof state. Its expressive and extensible proof support allows users to build
                                        reusable libraries of logical definitions, theorems, and programmable proof automation. Crucially, C★ unifies
                                        implementation and proof code development by using C as the common language.
                                           We implemented a prototype of C★ and evaluated it on a representative benchmark of small C programs and
                                        a challenging real-world case study: the attach function of pKVM’s buddy allocator. Our results demonstrate
                                        that C★ supports the verification of a broad subset of C programming idioms and effectively handles complex
                                        reasoning tasks in real-world scenarios.

                                        Additional Key Words and Phrases: software verification, real-time verification, C programming, LCF-style
                                        theorem proving, separation logic, symbolic execution

                                        1   INTRODUCTION
                                           Background. Systems software forms the infrastructure of modern computing, providing the
                                        low-level foundation on which all higher-level applications operate. Given its critical role, recent
                                        years have seen considerable advances in the formal verification of systems software components [2,
                                        8, 16, 22, 24–27, 33, 36, 40, 41].
                                           In this paper, we focus on the verification of software implemented in the C programming
                                        language, which remains widely used due to its predictable performance, fine-grained control over
                                        system resources, and the vast amount of existing critical code written in it. Significant progress has
                                        been made in verification frameworks and toolchains for C programs [3, 9, 14, 15, 20, 21, 26, 28, 34,
                                        35, 39, 42]. The substantial progress in the development of formally verified software components
                                        and verification tools has demonstrated the feasibility of large-scale verification, and has brought
                                        us closer to the vision where all critical software should be verified [19].
                                           Despite these successes, formally verified software projects remain costly, in the sense that they
                                        require specialized teams with significant expertise, and usually need person-years to complete [22,
                                        26]. For the wider adoption of verification practices, the development and maintenance costs for

                                                                                               1
                                                                                             Trovato et al.


verified software must be reduced. One significant source of the high costs arises from the lack
of involvement from programmers, who carry out most of the implementation work yet rarely
participate in the verification of their own code.
   Existing approaches. One reason for the lack of programmer involvement is that the verification
of C programs typically requires an external environment, e.g., an interactive theorem prover such
as Coq, which demands programmers to learn a significantly different proving paradigm from the C
programming experience. Examples in this category include AutoCorres [13], VST [3] and its recent
variant in Iris [28], as well as the Live Verification framework [15]. The first three translate existing
C programs into certain logical representations in the meta-logic (a monadic shallow embedding or
a deep embedding) and then require programmers to conduct proofs around these representations
in their underlying theorem prover. The Live Verification framework chooses another approach by
composing the program lazily and incrementally along the proof process, relying on the specific
mechanism of existential meta-variables in Coq to represent a partially constructed program.
   To encourage more involvement from programmers, other C verification tools provide language-
level integration of programming and verification to make the verification process more accessible
to programmers. There are two main categories: (i) assertion-based verifiers such as Frama-C [21]
and VST-A [42], and (ii) advanced-type-based verifiers such as RefinedC [39] and CN [35]. These tools
allow programmers to annotate a C program with intermediate assertions (e.g., loop invariants)
or advanced types (e.g., ownership and refinement types) apart from the specifications to guide
the verification process. These tools are usually (semi-)automated, in the sense that they employ
an assertion or type checker to automatically verify if the program conforms to the specifications
with the help of the programmer-provided annotations. However, when automation falls short,
programmers again need to switch to an external theorem proving environment to complete
the verification (e.g., in Coq [35, 39, 42]). To mitigate the issue, VeriFast [20]—an assertion-based
automated verifier for C programs—provides limited proof support such that programmers can
annotate the program with a fixed set of proof commands and write ghost lemma functions to
perform certain forms of inductive reasoning. However, VeriFast lacks the expressiveness and
extensibility in proof support required for the collaborative verification of low-level systems
software between programmers and proof experts.
  Our goal. As discussed above, there is no satisfactory verification tooling for conventional
systems programmers. In this paper, we aim to design and implement a new C verification tool
that satisfies the following two criteria:
  • it should provide language-level integration of programming and verification; and
  • it should provide comprehensive proving capabilities within C’s programming paradigm.
To further enhance the usability of the C verification tool, we consider one more criterion:
  • it should provide support for real-time verification, i.e., the tool should be able to provide a
    static summary of the program state at every program point and allow programmers to inspect
    every intermediate proof state inside a proof.
   Our approach. In this paper, we propose C★, a proof-integrated language that embeds full-
fledged verification and proving capabilities in C. We highlight the three key designs of C★ below.
  • We adapt the assertion-based design by allowing programmers to annotate a program with
    separation-logic assertions and incorporating forward symbolic execution, which abstracts the
    complexities of concrete semantics and maintains a static summary of the symbolic program
    state after processing a program fragment.
  • We integrate the C programming language with LCF-style proof support for higher-order
    logic, which provides a comprehensive and extensible interface for programming formal

                                                   2
C★: Unifying Programming and Verification in C


      proofs and transforming symbolic states, facilitating the development of high-level reasoning
      abstractions—as proof support libraries—using the full power of C.
    • With the previous two designs, C★ is ready to support real-time verification: forward symbolic
      execution provides a summary of the symbolic program state at every program point, and the
      LCF-style proof support allows programmers to inspect and manipulate the proof state using
      the familiar programming constructs of C.
  We implemented a prototype of C★ and evaluated it on a suite of C programs to demonstrate
C★’s practicality for the development of verified programs. Specifically, our evaluation shows that
C★ (i) supports systems programming idioms and a large subset of C language features, (ii) provides
sufficient expressiveness for advanced ownership and functional reasoning, and (iii) is capable of
verifying realistic C programs.
    Contributions. In this paper, we make the following contributions:
    • We propose a proof-integrated language design that embeds specifications and proof code in C
      programs, provides comprehensive reasoning capabilities within C’s programming paradigm,
      and thus make formal verification practices accessible to programmers.
    • We implemented our design as the C★ toolchain by extending C with two well-established
      components: a symbolic-execution engine and an LCF-style proof kernel, interfacing both to
      create a lightweight yet powerful verification workflow.
    • We evaluated our implementation of C★ on a suite of benchmark programs from the literature
      and a realistic case study to show it is effective in developing verified C programs with the
      help of C★’s standard proof-support library.

2     A GUIDED TOUR OF C★
In this section, we present a guided tour for developing a verified C program in C★. We take the
clear function shown in Listing 1 as the running example, whose desired functionality is to reset
len contiguous bytes that start from a base address to. The implementation code of clear consists of
lines 3, 6, 8, 10, 17, 19, 20, 22, and 24; others are verification-specific code. In the implementation
code, the programmer declares a local variable i in line 8, followed by a loop from line 10 to line 22,
where each loop iteration sets the i-th byte from the base address to to zero and increments i by
one until i reaches the function parameter len.
   We explain the verification-specific code in a way that guides the reader through the incremental
development process following C★’s workflow. Our explanation will follow the three criteria
mentioned in §1: §2.1 for language-level integration of programming and verification, e.g., how the
user writes specifications and assertions about clear; §2.2 for comprehensive proving capabilities via
C programming, e.g., how the user proves the implementation of clear comforms to its specification;
and §2.3 for real-time program verification, e.g., how C★ aids the user during the incremental
development.

2.1    Language-level Integration of Programming and Verification
The first thing to do for verifying a program is correct is to specify how it is supposed to be correct.
It is a common practice to specify a function’s expected behavior by formulating its pre- and
post-conditions, i.e., the expected program states before calling the function and after returning
from it. For the desired functionality of clear, the pre-condition could be that the function parameter
len is non-negative and the other parameter to is a base address that points to a memory chunk of
at least len contiguous bytes. The corresponding post-condition would be that len contiguous bytes
starting from the address to are set to zero. To formally formulate such conditions for low-level
heap-manipulating programs such as clear, we adapt separation logic in C★’s design.

                                                   3
                                                                                                       Trovato et al.


      1  #include "cstarlib.h"
      2  #include "clear.h"
       3 void clear(void *to, int len)
       4     [[require(`fact(len >= 0) ** undef_array_at(to, Tchar, len)`)]]
       5     [[ensure(`array_at(to, Tchar, replicate(len, 0))`)]]
       6 {
       7     « term params = `data_at(&"to", Tptr, to) ** data_at(&"len", Tint, len)`; »
       8     int i = 0;
       9     « /* proof: establish invariant */ »
      10     while (i < len)
      11         [[invariant(`∃(i:integer).
      12             fact(0 <= i && i <= len) **
      13             data_at(&"i", Tint, i) ** ${params:hprop} **
      14             array_at(to, Tchar, replicate(i, 0)) **
      15             undef_array_at(to + i * sizeof(Tchar), Tchar, len - i)
      16         `)]]
      17     {
      18         « single_out_location(); »
      19         *((char *)to + i) = (char) 0;
      20         i = i + 1;
      21         « /* proof: re-establish invariant */ »
      22     }
      23     « /* proof: establish post-condition */ »
      24 }

                                 Listing 1. An example verified C program in C★.



  Background (Separation Logic). The development of separation logic [31, 37] is driven by the
desire to verify heap-manipulating low-level programs in a modular manner, especially for handling
the flexibility of aliasing. Its most salient features are (i) the introduction of a logical connective,
separating conjunction, expressing non-aliasing properties between heap fragments in a succinct
way, and (ii) a characterizing program proof rule, frame rule, extending the program locality of
Hoare logic rules with spatial locality when reasoning about heap-manipulating programs.
   Tab. 1 lists the concrete notations for some separation-logic predicates used in C★. The standard
proof-support library of C★ provides some other widely-used predicates for program verification
tasks. For example, array_at(p, ty, lst) represents a consecutive array of elements of C type ty
starting at the address p, where the 𝑛-th element of the array is represented by the 𝑛-th element in
the logic-level list lst. Another example undef_array_at(p, ty, len) represents an array starting at
address p with len undefined values, each of which is uninitialized or irrelevant to the verification.
With separation logic, the user can specify the pre- and post-conditions in lines 4 and 5, respectively:
   • C★ uses the C attribute syntax [[require]]1 to enclose a pre-condition. In line 4, the predicate
      fact(len >= 0) represents an empty heap with the condition that len is non-negative. The
      predicate undef_array_at(to, Tchar, len) represents a memory chunk of len continuous bytes,
      where Tchar is the logic-level representation of the C type char. Using separating conjunction
     ** to compose the two predicates yields a precise formulation of the intended pre-condition.
   • C★ uses [[ensure]] for post-conditions. In line 5, the predicate array_at(to, Tchar, replicate
      (len, 0)) represents a memory chunk of len continuous zeros, where the logic-level term

1 In actual code, all the attributes are prefixed with the [[cstar::]] namespace for disambiguation.



                                                            4
C★: Unifying Programming and Verification in C


               Table 1. Concrete notations for some separation-logic predicates used in C★.
     Separation-logic Predicate        Concrete Notation      (Simplified) Definition
     empty predicate                   emp                    𝜆ℎ. ℎ = ∅
                                       fact(p)                𝜆ℎ. ℎ = ∅ ∧ 𝑝
     embedded proposition
                                       pure(p)                𝜆ℎ. 𝑝
                                       data_at(x, ty, v)      𝜆ℎ. ℎ = (𝑥 ↦→ty 𝑣) ∧ 𝑣𝑎𝑙𝑖𝑑 ty (𝑥, 𝑣)
     singleton maps-to
                                       undef_data_at(x, ty)   𝜆ℎ. ℎ = (𝑥 ↦→ty _) ∧ 𝑣𝑎𝑙𝑖𝑑 ty (𝑥, _)
     separating conjunction            hp1 ** hp2             𝜆ℎ. ∃ℎ 1 ℎ 2 . ℎ 1 ⊎ ℎ 2 = ℎ ∧ ℎ𝑝 1 ℎ 1 ∧ ℎ𝑝 2 ℎ 2


     replicate(len, 0) creates a list of len zeros. This, again, precisely corresponds to the intended
      post-condition we discussed earlier.
   Readers may have noticed the uses of quotations `...` inside pre- and post-conditions. The
quotation mechanism allows the user to construct separation-logic predicates and other logic-
level terms using conventional concrete syntax, which is similar to existing assertion-based C
verifiers. But as we will show in §2.2, these terms are first-class values in C★: beyond being directly
written with quotations, they can be computed from expressions, stored in variables, passed as
arguments, and manipulated using the full capabilities of the C programming language. This is one
key difference between C★ and traditional assertion-based C verifiers.
   Writing pre- and post-conditions is far from completing the verification, because it is generally
intractable to have an algorithm to automatically verify the function body “transforms” the pre-
condition to the post-condition. Similar to many existing C verifiers, C★ adapts the assertion-based
design to enable a declarative style of verification:
   Principle (Declarative Style of Verification). The user annotates the program with
separation-logic assertions about the expected program states that hold at specific program points.
A particular important class of assertions are loop invariants. C★ also uses the C attribute [[invariant
]] to accompany a loop with its invariant, i.e., a separation-logic predicate that is expected to hold at
the beginning of each loop iteration. Lines 11–16 specify the loop invariant, which intuitively states
that at the i-th iteration, the value of i should be between zero and len (line 12), local variables
and parameters are stored properly in the memory with Tint being the logic-level representation
of the C type int (line 13), and the base address to points to a memory chunk that starts with i
zeros (line 14) followed by len - i unspecified bytes (line 15). Note that in line 13 the code uses an
anti-quotation ${params:hprop} to interpolate a predicate defined in line 7. This again indicates that
predicates are first-class values and we defer the discussion of anti-quotations to §2.2.
   With extra assertions including invariants, an assertion-based verifier usually splits the verifica-
tion into multiple sub-tasks, each of which corresponds to prove a Hoare triple for a straight-line
program segment. For example, to verify that the clear’s implementation code conforms to the pre-
and post-conditions, it is sufficient to complete three sub-tasks (i.e., verifying three Hoare triples):
   • prove the code in line 8 transforms the pre-condition to the loop invariant (line 9);
   • prove that the loop body (lines 19 and 20) re-establishes the loop invariant (line 21); and
   • prove that the loop invariant—with the loop condition (in line 10) being false—entails the
      post-condition (line 23).
Each sub-task, i.e., the proof of each Hoare triple { 𝑃 } 𝑆 { 𝑄 }, involves two parts: (i) reasoning
about semantics of the program 𝑆, i.e., finding the strongest post-condition 𝑄 sp of 𝑆 w.r.t. the
pre-condition 𝑃, and (ii) carrying out an entailment proof, i.e., proving that 𝑄 sp entails 𝑄. Instead
of employing automated provers for both parts—as many other assertion-based verifiers do—C★

                                                     5
                                                                                          Trovato et al.


adapts a predictable mechanism of automation by integrating forward symbolic execution to reason
about program semantics, i.e., part (i) of each verification sub-task.
   Background (Forward Symbolic Execution). Since the work of Berdine et al. [4], separation logic
has been effectively used as a sound foundation for forward symbolic execution, which closely
matches a programmer’s operational intuition about the effects of statements on program states,
while abstracting away concrete semantic details. It achieves this by providing a highly predictable
algorithm for automatically applying structural program logic rules for separation-logic predicates
in suitable forms, i.e., the symbolic heap fragment of separation logic [5].
  Using a symbolic-execution engine, C★ computes a symbolic state for each program point. The
symbolic state consists of the values of the program variables and the view of the heap fragments
that are worked on and owned by the program. For example, at the beginning of the function
body of clear (in line 6), symbolic execution uses the pre-condition annotated in line 4 to initialize
the symbolic state to be the same as the following separation-logic predicate, which additionally
consists of data_at predicates for the function parameters:
       fact(len >= 0) ** undef_array_at(to, Tchar, len) **
         data_at(&"to", Tptr, to) ** data_at(&"len", Tint, len)

Here Tptr is the logic-level representation of C’s pointer types.
   If symbolic execution were always successful, the remaining proof obligations for the user
would all be separation-logic entailments, i.e., part (ii) of each verification sub-task. In §2.2, we
will show C★’s capabilties in supporting the user to develop the logical proofs. On the other hand,
unfortunately, the price of having a predictable symbolic-execution engine is that it will not try to
automate the reasoning and transformations on the symbolic state that a user might find intuitive
to perform. For example, in line 19, the statement assigns to the address ((char *)to + i), but the
symbolic state—the loop invariant in this case—does not explicitly describe the memory cell pointed
by the address. As a result, C★’s symbolic-execution engine cannot (yet) automatically process
the assignment. In §2.2, nevertheless, we will show how C★’s proving capabilities provide an
operational style of verification, where users can convey and formalize their high-level intuitive
ideas on manipulating the symbolic state.

2.2   Comprehensive Proving Capabilities via C Programming
As discussed in §2.1, C★’s proving capabilities should support its users in the following two tasks:
  • developing logical proofs for entailments, and
  • manipulating symbolic states inside the implementation code.
In particular, C★’s support should satisfy a key criterion:
  • allow the user to programmably develop logical proofs and manipulate symbolic states, using
    C’s conventional programming constructs.
To achieve the aforementioned goals, we adapt LCF-style theorem proving in C★.
   Background (LCF-style Theorem Proving). The LCF architecture is a general technique for em-
bedding formal logics into a programming language. Pioneered by Robin Milner and colleagues
in the early work on the Edinburgh LCF theorem prover [12, 18], its descendants are still widely
used today [17, 30]. In LCF-style provers, a general-purpose programming language is used as the
meta-language to implement object logic entities such as terms, types, and theorems. These are rep-
resented as recursive data structures, making formal proof a programming process of constructing
theorems from a set of axioms using primitive inference rules. Specifically, the axioms are encoded

                                                  6
C★: Unifying Programming and Verification in C


as constants, and the inference rules are implemented as functions that take premises and return
conclusions as theorems if the rules can be successfully instantiated.
   In C★, we integrate an LCF-style proof kernel with higher-order logic as the object logic. The
kernel is wrapped by a C interface; in other words, the meta-language in C★’s design is the
standard C programming language. To distinguish the code for developing logical proofs and
manipulating symbolic states from ordinary implementation code, C★ introduces proof-code blocks
delimited by the «...» syntax.2 Arbitrary C code is allowed in proof-code blocks, with the ability
to introduce bindings and construct values of type term and thm, corresponding to object-logic
terms and theorems, respectively. Recall that we mentioned that in C★, separation-logic predicates
are first-class values. Indeed, they are just term values of object-logic type hprop (short for heap
propositions). The quotation and anti-quotation mechanisms are thereby introduced to conveniently
construct term values. For example, in line 7 of Listing 1, the code stores the data_at predicates
regarding ownership of the parameters—wrapped by a quotation `...`—in a variable called params.
In the following proof-code blocks and assertions (e.g., invariants), the user can use params as if it is
a normal program variable.3 In line 13, the code indeed uses it; combined with the anti-quotation
${params:hprop}, it reduces redundancy when writing the loop invariant.
   Because separation-logic predicates are just values in C★, it becomes natural to write C code to
manipulate symbolic states, which are special kinds of separation-logic predicates. Such capability
of C★ enables an operational style of verification:
   Principle (Operational Style of Verification). The user manipulates the symbolic state
using arbitrary C code, provided they can give justifications, i.e., theorems for the corresponding
separation-logic entailments, for the manipulations they made.
For example, the operational style of verification is applied in line 18. Here, the symbolic state—
computed by the symbolic-execution engine—is equivalent to the following predicate:
∃(i:integer). fact(i < len) ** fact(0 <= i && i <= len) **
  data_at(&"i", Tint, i) ** data_at(&"to", Tptr, to) ** data_at(&"len", Tint, len) **
  array_at(to, Tchar, replicate(i, 0)) ** undef_array_at(to + i * sizeof(Tchar), Tchar, len - i)
As discussed above about symbolic execution, symbolically executing the next statement (in line
19) would fail, because the symbolic state does not explicitly describe the address ((char *)to + i).
Intuitively, the user should “transform” the symbolic state to some form containing undef_data_at(to
+ i * sizeof(Tchar), Tchar) as a separating conjunct, which represents the ownership of the memory
location being stored into. By inspecting the symbolic state, the user can see that a transformation
of the view of the heap is needed to satisfy the requirement: by splitting the undef_array_at predicate
into the separating conjunction of its head element (as an undef_data_at predicate) and the rest of
the slice (as an undef_array_at predicate with smaller length and starting at a bigger offset). The
split is valid due to the fact that i < len holds in current state, which entails the fact len - i > 0,
meaning the slice is non-empty. The corresponding justification—as proof code—for this intuitive
transformation is wrapped in the proof procedure single_out_location.
   The implementation of the proof procedure single_out_location is shown in Listing 2. It demon-
strates how C★ allows proving separation-logic entailments using conventional C programming
constructs and high-level derived rules from the proof-support libraries, making the intuitive
reasoning process easy to implement as proof code. Thanks to the LCF-style design, logical rules
are just C functions that return thm values, which represent proven theorems.
2 In actual code, we use the [[cstar::proof(...)]] attribute to embed proof-code blocks.
3 All proof blocks in a function body are in the same scope, and global proof-code blocks (that is outside of any function

body) are file-scoped. Local scopes can be created using C blocks {...}. See §4.1 for more details.


                                                            7
                                                                                                    Trovato et al.


      1  void single_out_location(void) {
      2      thm dest_undef_array =
       3         undef_array_at_select_first(`to + i * sizeof(Tchar)`, `Tchar`, `len - i`);
       4       /* len - i > 0 ==>
       5          undef_array_at(to + i * sizeof(Tchar), Tchar, len - i) |--
       6          undef_data_at(to + i * sizeof(Tchar), Tchar) **
       7          undef_array_at((to + i * sizeof(Tchar)) + sizeof(Tchar), Tchar, len - i - 1) */
       8     thm arith_facts[] = {
       9         arith_rule(`len - i > 0 <=> i < len`),
      10         arith_rule(`len - i - 1 == len - (i + 1)`),
      11         arith_rule(`(to + i * sizeof(Tchar)) + sizeof(Tchar) ==
      12                     to + (i + 1) * sizeof(Tchar)`), NULL };
      13     dest_undef_array = rewrite_rule_list(arith_facts, dest_undef_array);
      14       /* rewrite using linear arithmetic facts */
      15     thm final_thm = local_apply(get_symbolic_state(), dest_undef_array);
      16       /* perform local transformation with frame inferred from the symbolic state */
      17     set_symbolic_state(final_thm); /* update the symbolic state */
      18 }

             Listing 2. Proof procedure: single out the first element of the uninitialized slice.



  • Derive the transformation rule (lines 2–7). The undef_array_at_select_first theorem, from the
    proof-support library clear.h included by the C★ program in Listing 1, asserts that for any
    uninitialized array, we can single out the first element and treat the remainder as another
    uninitialized array, provided the length of the array is greater than zero. The resulting theorem
    from this derived-rule application is shown by the comment in lines 4–7, where ==> denotes
    standard logical implication and |-- denotes separation-logic entailment.
  • Rewrite using linear arithmetic facts (lines 8–14). The rewrite_rule_list function—from the stan-
    dard proof-support library cstarlib.h—takes an NULL-terminated array of equational theorems
    and another theorem, and rewrites the second argument using the equational theorems. It is
    used here to rewrite the theorem using linear arithmetic facts, which are derived automatically
    by calling the arith_rule function, to align with the predicates in the current symbolic state.
    The array-destructing theorem undef_array_at_destruct is re-assigned to the rewritten theorem
    by the statement in line 13.
  • Perform local transformation with frame inferred from the symbolic state (lines 15–17). The
    local_apply function is an important derived rule in cstarlib.h. It allows programmers to per-
    form a local transformation with the frame being inferred from the symbolic state. Specifically,
    it takes two arguments: the current symbolic state and a local-transformation theorem. In
    line 15, we fetch the current symbolic state using the built-in get_symbolic_state function,
    and use the local_apply function to perform a local transformation justified by the theorem
    dest_undef_array. The result of the transformation is then put back to the symbolic-execution
    engine using the built-in set_symbolic_state function in line 17.

2.3   Real-time Program Verification
In the previous two sections, we used the verification of the function clear to illustrate (i) how C★
incorporates separation logic and forward symbolic execution to provide language-level integration
of programming and verification, as well as (ii) how C★ integrates LCF-style proof support for
higher-order logic to provide comprehensive proving capabilities within C’s programming paradigm.

                                                      8
C★: Unifying Programming and Verification in C


In particular, separation-logic predicates are first-class values and proof-code blocks can manipulate
symbolic states and proof states.
   We claim that C★ achieves real-time program verification, i.e., the user can carry out verification
as they program the implementation code incrementally. It achieves this goal by orchestrating the
symbolic-execution engine and the LCF-style proof kernel together, creating a proof-supporting
runtime that runs proof-code blocks and symbolic execution of program segments in an interleaving
manner, and provides the symbolic state at every program point in implementation code as well as
the proof state in proof-code blocks.
   Firstly, C★ is capable of providing the symbolic state at every program point, given that (i) every
function has pre- and post-conditions, (ii) every loop has an invariant, and (iii) the required maps-to
predicates are present in the symbolic state before executing a primitive statement. This is achieved
by a combination of forward symbolic execution for separation logic and the ability to write
proof-code blocks to manipulate the symbolic state. The symbolic state in the symbolic-execution
engine is always represented as a separation-logic assertion in a canonical form, known as symbolic
heaps [4]. When a statement (e.g., an assignment) is symbolically executed, the symbolic-execution
engine requires the primitive maps-to predicate (i.e., data_at or undef_data_at) for the accessed
memory locations be present in the current symbolic heap as a separating conjunct; if so, the engine
modifies the symbolic heap locally [20]. For example, when executing the store statement *((char
*)to + i) = (char) 0 in line 19 of Listing 1, the symbolic-execution engine confirms that the current
symbolic heap contains the assertion `undef_data_at(to + i * sizeof(Tchar), Tchar)`, representing
the ownership of the memory location being stored into, and then substitutes the predicate with
`data_at(to + i * sizeof(Tchar), Tchar, 0)`, reflecting the effect of the store statement. The other
predicates in the symbolic heap are left unchanged, being justified by the frame rule of separation
logic. It is worth noting that for the symbolic-execution engine to achieve this, C★ needs to first
execute the proof-code block in line 18 of Listing 1 to transform the symbolic heap accordingly,
before symbolically executing the store statement.
   Secondly, C★’s runtime environment for running proof-code blocks is capable of providing
the proof state in proof-code blocks. The proof state records the concrete values of term and thm
variables declared in proof-code blocks, as well as proof functions and theorems included from
proof-support libraries. For example, when a user is developing the function clear and writes down
line 18 of Listing 1 to call single_out_location, the environment of the proof-supporting runtime
should be able to find the function definition of single_out_location in Listing 2. This ability comes
from the LCF-style theorem proving, where proofs are ordinary programs that manipulate terms
and theorems. Thus, C★ can assemble all the proof-code blocks inside a function and its dependent
proof-support functions together as a C program, compile it, and execute it to record the concrete
values of variables.

3 CORE DESIGN
In this section, we present the core design of C★ from two perspectives. Following the discussion
in §2.3, we explain C★’s internal mechanisms from the developer’s perspective in §3.1, i.e., C★’s
verification-specific workflow and its proof-supporting runtime. Following the guided tour in
§2.1 and §2.2, we describe C★’s language features from the user’s perspective in §3.2, i.e., C★’s
verification-specific interface and its proving capabilities.

3.1   Workflow of C★ Toolchain
The C★ toolchain consists of three components: the C★ compiler, the LCF-style proof kernel, and the
symbolic-execution engine. The interaction between these components during the proof-checking
phase of a C★ program is illustrated conceptually in Fig. 1. After proof checking, the deployment

                                                  9
                                                                                                                    Trovato et al.


                                                                           LCF-style
                                                                          Proof Kernel
                                                   Operational                                        Residual
                C★ Program                        Proof Program                                    Proof Program
                                         Slice
              Implementation Code                 Assertion-annotated               Generate          Veriﬁcation
                       &                            Code Segments                                     Conditions
                Speciﬁcations and                                       Symbolic
             Intermediate Assertions   Assemble                         Execution
                                                      Proof Code                                      Proof Code
               Proof-code Blocks


                                                                                         User

                   State I                                 State II                              State III
                 Translation                      Operational Proof Checking              Residual Proof Checking

                               Fig. 1. The ideal workflow of C★’s proof-checking phase.


phase becomes straightforward: because all verification-specific annotations are wrapped in C
attributes, the verified program can be compiled directly with C compilers such as gcc or clang.
    The proof-checking phase of a C★ program can be summarized as a three-stage process: the
translation stage, the operational proof checking stage, and the residual proof checking stage.
    Translation stage. In the first stage, the C★ compiler processes the input C★ program, and
produces an operational proof program. The input C★ program consists of three main components:
(i) implementation code, (ii) verification annotations including specifications (e.g., [[require]] and
[[ensure]] attributes) and intermediate assertions (e.g., [[invariant]] attributes), and (iii) embedded
proof-code blocks. During translation, the C★ compiler combines part (i) and part (ii) to form the
annotated C code, slices it into segments that are separated by proof-code blocks, and stores the
segments as serializable data structures in the proof code. For part (iii), i.e., the proof-code blocks,
the C★ compiler assembles them into the main code for execution. The compiler also handles
syntax extensions such as quotation and anti-quotation, translating them into applications of
term-constructing functions. Fig. 2 demonstrates C★’s workflow using the verification of the clear
function shown in §2. Note that here we reinterpret the commented-out proof-code blocks in lines 9,
21, and 23 of Listing 1 as they are not inserted into the implementation code. Fig. 2a is the assembled
operational proof program: lines 1–15 are three code segments split by proof-code blocks in lines 7
and 18 of Listing 1. In the main function, we use the built-in function feed_program_segment to feed a
code segment to the symbolic-execution engine, as we will explain below about the second stage.
   Remark 3.1 (Reversed role of verification-specific annotations). Whereas in the deployment phase
embedded proof-code blocks are ignored by the compiler, in the proof-checking phase, they play a
central role. Here, the proof code assembled from embedded proof blocks becomes the main code for
execution, while the annotated C code are sliced into segments and treated as serializable data, to be
fed to the symbolic-execution engine interactively.
   Operational proof checking stage. In the second stage, the C★ workflow executes the oper-
ational proof program obtained from the translation stage. As discussed in §2, C★ supports two
styles of program verification, namely declarative and operational:
   • In the declarative style, the user asserts expected symbolic states at specific program points.
     The symbolic-execution engine uses the asserted symbolic state for further execution and
     produce verification conditions as output. These verification conditions are gathered and will
     be proved in batch later in the residual proof checking stage.
   • In the operational style, the user directly manipulates the symbolic state through proof-
     code blocks, which are executed interactively with the symbolic execution. In this way, the

                                                                   10
    C★: Unifying Programming and Verification in C


1  code_segment_t seg1 = /*                                  1 term vc1 = /* establish invariant
2    void clear(void *to, int len)                           2   (line 9 of Listing 1) */;
 3     [[require(...)]]                                      3 term vc2 = /* re-establish invariant
 4     [[ensure(...)]]                                       4   (line 21 of Listing 1) */;
 5   { */;                                                   5 term vc3 = /* establish post-condition
 6 code_segment_t seg2 = /*                                  6   (line 23 of Listing 1) */;
 7     int i = 0;                                            7
 8     while (i < len)                                       8 thm proof1() {
 9       [[invariant(...)]]                                  9     /* user-provided proof code for vc1 */
10     { */;                                                10 }
11 code_segment_t seg3 = /*                                 11 thm proof2() {
12       *((char *)to + i) = (char) 0;                      12    /* user-provided proof code for vc2 */
13       i = i + 1;                                         13 }
14     }                                                    14 thm proof3() {
15   } */;                                                  15    /* user-provided proof code for vc3 */
16 int main(void) {                                         16 }
17     feed_program_segment(seg1);                          17
18     term params = ...; // line 7 of Listing 1            18 int main(void) {
19     feed_program_segment(seg2);                          19     assert_prove(proof1(), vc1);
20     single_out_location(); // line 18 of Listing 1       20     assert_prove(proof2(), vc2);
21     feed_program_segment(seg3);                          21     assert_prove(proof3(), vc3);
22 }                                                        22 }


                  (a) Operational Proof Program                         (b) Residual Proof Program
                     Fig. 2. Demonstration of C★’s workflow using the running example in §2.


          operational proof checking phase is naturally real-time: the proof-code blocks are executed
          interleaved with symbolic execution, feeding the annotated program segments incrementally
          to the symbolic-execution engine.
    More specifically, the C★ workflow handles the execution of each proof block as follows. First, the
    last annotated program segment—as some serializable data—is fed to the symbolic-execution engine.
    Next, the proof-code block, which is normal C code, is executed in the proof-supporting runtime
    (see Remark 3.2 below). Finally, the current symbolic state is updated according to the execution
    results of the proof-code block: recall that a proof-code block should fetch the symbolic state by
    calling get_symbolic_state, do transformations on it with proofs, and then call set_symbolic_state at
    the end to update the symbolic state in the symbolic-execution engine. The proof program shown
    in Fig. 2a implicitly calls these functions in the code of single_out_location, i.e., Listing 2.
       Remark 3.2 (Proof-supporting runtime). The proof programs are executed in C★’s proof-supporting
    runtime, which is the standard C runtime interfaced with the LCF-style proof kernel and the symbolic-
    execution engine. The LCF-style proof kernel implements the basic building blocks used in proof
    code. The symbolic-execution engine takes annotated C program segments as input (via the built-in
    function feed_program_segment), maintains the symbolic state of the current partial program internally
    (accessed and modified via the get_symbolic_state and set_symbolic_state built-in functions), and
    produces verification conditions as output when symbolic execution is completed.
      Residual proof checking stage. In the third stage, the C★ compiler collects the output of the
    symbolic-execution engine and creates the residual proof program, which is a C★ program purely
    consisting of global proof-code blocks. This program contains proof goals for every undischarged
    verification condition generated during symbolic execution, which are to be addressed in the

                                                       11
                                                                                             Trovato et al.


C★ proof environment, either by the programmers or with assistance from proof experts. Those
verification conditions arise from the declarative style of verification: recall that at each assertion
or invariant, it is obliged for C★ users to prove the entailment from the maintained symbolic
state (by the symbolic-execution engine) to the asserted state. Fig. 2b shows the residual proof
program for the running example in §2: lines 1–6 are three verification conditions generated by
the symbolic-execution engine, lines 8–16 are user-provided proof code for the three verification
conditions, respectively, and the main function executes the proof code the check if they indeed
prove the verification conditions.
   Remark 3.3 (C★ developer’s view). From the perspective of a developer, C★ can be seen as an LCF-
style higher-order-logic theorem prover embedded within C, tailored for C program verification. It
relies on a trusted symbolic-execution engine that serves as an oracle, which automatically derives
strongest post-conditions and generates verification conditions from C code segments annotated with
separation-logic assertions and specifications. Successfully executing the two proof programs, i.e.,
operaational and residual, is thereby equivalent to verifying the Hoare triple of the entire program,
which provides the correctness guarantee for the conformance with the program’s specification.

3.2   Interface for C★ Users
As overviewed in §2, C★ extends the C programming language with two categories of verification-
specific syntactic constructs: (i) specifications and intermediate assertions, and (ii) proof-code
blocks. Fig. 3 summarizes these constructs, providing an accessible interface for C★ users. In this
section, we explain our design of this interface and at the end exemplify C★’s extensibility in proof
support using the implementation of local_apply from C★’s standard proof-support library.

   Verification-specific attributes. C★ introduces attributes [[require]], [[ensure]], [[parameter]],
and [[argument]] concerning function specifications, [[assert]] and [[invariant]] for intermediate
assertions within implementation code, as well as [[proof]] for embedding proof-code blocks.
   The attributes [[require]] and [[ensure]] specify a function’s pre-condition and post-condition,
respectively, both containing C expressions that evaluate to a term value of object-logic type hprop,
i.e., a separation-logic predicate. Both the pre- and post-condition can reference function parameters,
and the post-condition can additionally reference the function’s returned value using the preserved
symbol __result. The attribute [[parameter(`var:type`)]] introduces a ghost parameter var of object-
logic type type that denotes a universally quantified logical variable for the function specification.
Correspondingly, the [[argument(`var=value`)]]—used before a function call—instantiates the ghost
variable with an object-logic term. Fig. 3 illustrates the usage of parameter and argument attributes
using a C function reverse that reverses a linked list in-place: the parameter l is a logic-level
integer list that encodes the content of the linked list pointed to by p, where the (user-defined)
separation-logic predicate ll_repr(p, l) expresses such encoding.
   Similar to [[require]] and [[ensure]], the [[assert]] and [[invariant]] attributes take a C expres-
sion as input, which evaluates to a separation-logic predicate. The [[assert]] attribute inserts a static
assertion about the symbolic state at a program point, supporting a declarative verification style: if
non-trivial reasoning is required to prove that the maintained symbolic state entails the asserted
state, a verification condition is generated by the symbolic-execution engine. We will explain this
workflow in detail in §3.1. After processing an assertion, the symbolic-execution engine will update
the symbolic state accordingly. The [[invariant]] attribute also inserts an assertion but it asserts
a symbolic state expected at the start of each loop iteration, hence its name invariant. Currently,
only while loops are supported, and using break or continue will lead the symbolic-execution engine
to generate additional verification conditions for the additional control-flow paths.

                                                   12
C★: Unifying Programming and Verification in C



           Veri cation-speci c                                                Speci cations &
                Attributes                                                Intermediate Assertions
     /* function specification */                                             Separation-logic Predicates
     struct ll_node *reverse(struct ll_node *p)             /* object-logic type: hprop */
       [[parameter(`l:int_list`)]]                          emp                               // empty heap
       [[require(`ll_repr(p, l)`)]]                         fact(&1 > &0)                     // embedded proposition
       [[ensure(`ll_repr(__result, rev(l))`]]               pure(&1 > &0)                     // embedded proposition
     ;                                                      data_at(&"x", Tint, &42)          // singleton maps-to
                                                            undef_data_at(&"y", Tint)         // singleton maps-to
     struct ll_node *q;                                     data_at(...) ** data_at(...)      // separating conjunction
     [[argument(`l=cons(&1,nil())`)]]                       exists (n:integer). fact(n >= &0) // existential quantifier
     q = reverse(p);
                                                            /* object-logic type: bool */
     /* intermediate assertion */                           &1 > &0        // comparison true || false // disjunction
     int n = 42;                                            true && false // conjunction false ==> true // implication
     while (n > 0)                                          fact(x > y) |-- emp // separation-logic entailment
       [[invariant(`exists (n:integer).
                    fact(n >= &0) **                        /* object-logic type: integer */
                    data_at(&"n", Tint, n)`)]]              &"var"       // address of a variable    &42 // integer literal
     { n = n - 1; }                                         sizeof(Tint) // size of a C-type
     [[assert(`data_at(&"n", Tint, &0)`)]];
                                                            /* object-logic type: ctype */
     /* proof-code block */                                 Tint // C-type: int         Tchar // C-type: char
     [[proof(                                               Tptr // C-type: pointer
       thm th = arith_rule(                                                      otation & Anti-quotation
                  `n > &0 ==> n - &1 >= &0`);
     )]];                                                   /* quotation */            /* anti-quotation */
                                                            term exp = `&21 + &21`;    term eqn = `&42 == ${exp:integer}`;

                                        Proof-code Interface (Symbolic Execution)
                /* retrieve symblic state */               /* transform symbolic state */
                term pre_state = get_symbolic_state();     thm th = axiom(`${pre_state:hprop} |-- ${new_state:hprop}`);
                                                           set_symbolic_state(th);


                                    Proof-code Interface (LCF-style Proof Kernel)
                  Term-speci c Utilities                                      HOL Rules (Selected)
    /* constructor */                                    axiom(`&0 == &1`)                       // |- &0 == &1
    term conj = `emp ** emp`;                            assume(`&0 == &1`)                      // &0 == &1 |- &0 == &1
                                                         disch(assume(`x > &0`), `x > &0`)       // |- x > &0 ==> x > &0
    /* destructor */                                     undisch(axiom(`p ==> q`))               // p |- q
    term left = left_of_sep(conj); // emp                mp(axiom(`p ==> q`), axiom(`p`))        // |- q
    term right = right_of_sep(conj); // emp              conjunct(axiom(`p`), axiom(`q`))        // |- p && q
                                                         conjunct1(axiom(`p && q`))              // |- p
    /* discriminator */                                  disj_cases(axiom(`p || q`),
    if (is_sep(conj)) { ... }                                       undisch(axiom(`p ==> r`)),
                                                                    undisch(axiom(`q ==> r`))) // |- r
    /* equality checker */                               refl(`x`)                               // |- x == x
    if (equals_term(left, right)) { ... }                trans(axiom(`x == y`), axiom(`y == z`)) // |- x == z
                                                         symm(axiom(`x == y`))                   // |- y == x
                                                         arith_rule(`i < &2 ==> i < &3`)         // |- i < &2 ==> i < &3
                      eorem-speci c Utilities
    thm th = undisch(axiom(`i < &2 ==> i < &3`));
                                                                         Seperation-logic Rules (Selected)
    /* get the conclusion */                               hentail_refl(`data_at(&"x", Tint, &0)`)
    term concl = conclusion(th); // i < &3                     // |- data_at(&"x", Tint, &0) |-- data_at(&"x", Tint, &0)
                                                           hentail_trans(axiom(`hp1 |-- hp2`), axiom(`hp2 |-- hp3`))
    /* get the n-th hypothesis */                              // |- hp1 |-- hp3
    term hyp = nth_hypth(th, 0); // i < &2                 hsep_assoc1(axiom(`hp |-- (hp1 ** hp2) ** hp3`))
                                                               // |- hp |-- hp1 ** (hp2 ** hp3)
                 De nitional Mechanisms                    hsep_comm(axiom(`hp |-- hp1 ** hp2`))
    /* inductive type */                                       // |- hp |-- hp2 ** hp1
    indtype int_list =                                     hsep_monotone(axiom(`hp1 |-- hp3`), axiom(`hp2 |-- hp4`))
      define_type("int_list =                                  // |- hp1 ** hp2 |-- hp3 ** hp4
                     nil | cons integer int_list");        hfact_intro(axiom(`p`), axiom(`hp1 |-- hp2`))
                                                               // |- hp1 |-- fact(p) ** hp2
    /* recursive function */                               hfact_elim(axiom(`p ==> (hp1 |-- hp2)`))
    thm nth =                                                  // |- fact(p) ** hp1 |-- hp2
      define(`nth(cons(h,t)),0) == h &&                    hsep_hfact1(axiom(`hp |-- (fact(p) ** hp1) ** hp2`))
              nth(cons(h,t)),SUC(n)) == nth(t,n)`);            // |- hp |-- fact(p) ** (hp1 ** hp2)
 Qu
 Th fi   fifi    fi    fi          fi




                      Fig. 3. A summary of the verification-specific interface that C★ provides to users.


  The [[proof]] attribute wraps a proof-code block. Proof-code blocks may contain arbitrary C
code, having access to the LCF-style proof kernel and the symbolic-execution engine. There are

                                                                 13
                                                                                             Trovato et al.


two kinds of proof-code blocks: (i) local proof blocks, used within implementation code (e.g., inside
a function body), primarily for operational verification and symbolic-state transformation, and (ii)
global proof blocks, used outside any implementation code, typically for defining common proof
functions or theorems. Typically, all code in a proof-support library (e.g., cstarlib.h) is within global
proof blocks. Within a local proof block, the user can reference bindings declared in prior proof
blocks in the same function body, as well as bindings declared in global proof blocks.
   Specifications and intermediate assertions. Inside the verification-specific attributes, C★
provides a quotation syntax (delimited by `...`). It allows the user to construct object-logic terms
using concrete syntax representations and avoid the verbosity of calling term constructors explicitly.
Inside quotations, the user can use the anti-quotation mechanism (escaped using ${var:type}) for
splicing in computed sub-terms stored in program variables. Together, these two syntax extensions
offer a simple yet expressive way to build object-logic terms. Fig. 3 summarizes the concrete syntax
for separation-logic predicates and other frequently used object-logic terms and types. There are a
few unsual notational conventions, which arise from the LCF-style proof kernel employed by C★.
In the object logic, integer literals (i.e., terms of object-logic type integer) take the form &n, where
n is a natural number. The logic-level representation of an address is an integer value, e.g., &"x"
denotes the address of the program variable named x. We reuse C’s && and || operators to encode
logic-level conjunction an disjunction, respectively, and use ==> for standard logical implication.
Separation-logic entailments are treated as propositions (i.e., terms of object-logic type bool): the
binary operator |-- takes two separation-logic predicates hp1 and hp2 and produces a proposition
hp1 |-- hp2, whose meaning is that if a heap satisfies hp1, then it also satisfies hp2.
   In C★, separation-logic predicates in specifications and intermediate assertions must adhere to a
specific form to enable automated symbolic execution. This specific form is known as the symbolic
heaps [4], and has the following structure:
                             ∃𝑥 1, . . . , 𝑥𝑘 . (𝑃1 ∧ · · · ∧ 𝑃𝑚 ) ∧ (𝑄 1 ∗ · · · ∗ 𝑄𝑛 ) ,    (SymHeap)
where 𝑥𝑖 ’s are existentially quantified logical variables, ∧ denotes non-separating conjunction, i.e.,
standard logical conjunction, and ∗ represents separating conjunction. The 𝑃𝑖 ’s are pure facts—
expressions in the form of pure(p) that state properties about the global heap. The 𝑄 𝑗 ’s, known as
spatial facts, consist of either primitive maps-to predicates (i.e., data_at or undef_data_at) which are
visible to the symbolic-execution engine, or user-defined predicates (e.g., array_at) whose internal
structure can be arbitrary and are opaque to the symbolic-execution engine. These spatial facts
represent separately-owned local fragments of the heap. We often use the derived form fact(p) =
pure(p) && emp to describe pure properties. The derived form satisfies that pure(p) && H = fact(p) * H.
This formulation allows symbolic heaps to be uniformly represented as separating conjunctions of
pure and spatial facts, avoiding the need for non-separating conjunction.
   Before symbolically executing any primary program statement, the symbolic-execution engine
verifies that the current symbolic state includes the necessary primitive maps-to predicates for all
accessed memory locations. Once this requirement is satisfied, the engine updates the symbolic
state as needed, preserving the symbolic form, and possibly generates side conditions to guarantee
safe execution, i.e., no runtime error or undefined behavior.
   In addition to the primitive predicates and predicates provided in the standard library, C★ users
can derive and use their customized predicates. For instance, the hiter function in the standard
proof-support library, defined in object-logic as hiter hps = fold_right (**) hps emp using the higher-
order function fold_right, takes a list of separation-logic predicates hps and returns their iterated
separating conjunction. We will explain how to implement derived predicates later in this section.
  Proof-code interface with symbolic execution. In C★, a local proof-code block for performing
operational verification retrieves the current symbolic state from the symbolic-execution engine

                                                   14
C★: Unifying Programming and Verification in C


hsep-comm                    hsep-assoc                                 hsep-cancel-right        hexists-monotone
                                                                            𝐻 1 ⊢ 𝐻 1′              ∀𝑥 . (𝐻 ⊢ 𝐻 ′ )
𝐻 1 ∗ 𝐻 2 ⊢⊢ 𝐻 2 ∗ 𝐻 1       (𝐻 1 ∗ 𝐻 2 ) ∗ 𝐻 3 ⊢⊢ 𝐻 1 ∗ (𝐻 2 ∗ 𝐻 3 )   𝐻 1 ∗ 𝐻 2 ⊢ 𝐻 1′ ∗ 𝐻 2   (∃𝑥 . 𝐻 ) ⊢ (∃𝑥 . 𝐻 ′ )

                         Fig. 4. Selected separation-logic rules for structural manipulations.



by calling a built-in function get_symbolic_state(). For example, the initial symbolic state can
be obtained with term pre_state = get_symbolic_state(). At the end of the proof-code block, the
symbolic state can be updated using a call to set_symbolic_state(th), where th is a theorem proving
the separation-logic entailment from the current symbolic state (pre_state) to a new state (new_state).
This updated state new_state is then set as the current symbolic state. Recall Listing 2 in §2 for an
example of using the interface to do local transformations on the symbolic state.
   Proof-code interface with LCF-style proof kernel. In an LCF-style proof environment like that
in C★, two fundamental types are provided for logical reasoning: term, representing terms in the
object logic, and thm, denoting proven theorems. These types are treated as abstract types in C★,
ensuring that users can only manipulate them through the library functions provided by the LCF
proof kernel, forbidding direct access to internal data structures.
   As summarized in Fig. 3, to work with term values, the proof kernel offers a set of functions
acting as constructors, destructors, discriminators, and equality checkers, among other utilities.
For thm values, the kernel provides the primitive rules needed to prove theorems. These rules
encompass both separation-logic entailment rules and higher-order logic rules for general reasoning.
Additionally, functions for checking if a proof goal is achieved and for accessing the hypotheses
and conclusion of a theorem are available.
   The programmability of C★’s LCF-style proof kernel allows users to extend its functionality by
defining customized derived rules or proof-search routines as C functions on top of the primitive
proof rules. Furthermore, besides the built-in types such as ctype and hprop, as well as standard
functions like sizeof, the kernel’s definitional mechanism enables users to define new (inductive)
types, e.g., int_list in Fig. 3, as well as (recursive) functions, e.g., nth in Fig. 3. Such definitional
mechanism is also used to define new sepeartion-logic predicates, such as hiter mentioned earlier
in this section. This flexibility makes C★ expressive for a wide range of verification needs.
   Extensible and programmable proof support. With the programmability of LCF-style proof
support, proof experts can develop custom proof libraries to simplify common proof patterns,
offering high-level derived proof rules and collections of frequently used mathematical properties.
   For example, a typical task in operational-style verification is justifying local transformations
performed on the symbolic state. By local transformations, we mean picking out specific conjuncts
from a symbolic heap, applying a proved-correct separation-logic entailment to these conjuncts, and
leaving the rest of the symbolic heap unchanged. Separation logic inherently supports such local
transformations; however, using only primitive rules of separation logic—some of which are listed
in Fig. 4— requires manually lifting affected conjuncts through layers of separating conjunctions
and specifying frames for each transformation. This can be tedious and lead to proof code cluttered
with structural manipulations, which detract from the intuitive reasoning process.
   To alleviate the need for manually performing such structural manipulations, we implemented
a derived rule called local_apply in our standard proof-support library cstarlib.h. Considers the
simple case where only one conjunct is affected by the transformation, the automation process of
local_apply can be described in four steps as follows.

 (i) Repeatedly destruct existential binders in the symbolic heap of the form (SymHeap).

                                                                15
                                                                                            Trovato et al.


       1 thm sep_lift_one(term target, term septerm)
       2     /* assume target is primitive and septerm is a right-associated symbolic heap */
       3 {
       4     thm lift_to_left = hsep_move(target);
       5     /* ∀ (hp1:hprop) (hp2:hprop).
       6          hp1 ** ${target:hprop} ** hp2 -|- ${target:hprop} ** hp1 ** hp2 */
       7
       8       if (is_sep(septerm)) {
       9           term l = left_of_sep(septerm), r = right_of_sep(septerm);
      10           if (equals_term(target, l)) { return rewrite(lift_to_left, septerm); }
      11           else {
      12               if (is_sep(r)) {
      13                   thm step1 = rewrite(sep_lift_one(target, r), septerm);
      14                   thm step2 = rewrite(lift_to_left, consequent(conclusion(step1)));
      15                   return trans(step1, step2);
      16               } else if (equals_term(target, r))
      17                   return rewrite(symm(hsep_comm(target)), septerm);
      18           }
      19       } else if (equals_term(target, septerm)) { return refl(septerm); }
      20       return NULL; /* fail if target isn't found */
      21   }
                                    Listing 3. C★ code of sep_lift_one.



 (ii) Find the affected conjunct and lift it to the far-left side of the symbolic heap by using the
      hsep-comm and hsep-assoc rules repeatedly.
(iii) Apply the hsep-cancel-right rule with other conjuncts to the right as the frame.
(iv) Repeatedly add back existential binders using the hexists-monotone rule.
As a concrete code example, we present the proof function sep_lift_one for performing the second
step in Listing 3. It assumes the input symbolic heap septerm is a right-associated separating con-
junction. It first calls the derived rule hsep_move, getting a generalized equality theorem lift_to_left
(line 4) for moving the target conjunct out to the left for one layer when it is in the left position of
the inner symbolic heap, in one step. It then tries to find the target conjunct recursively:
  (i) If the target conjunct is never found, it returns NULL.
 (ii) If the target conjunct is at the far-right position, it rewrites it using the hsep-comm rule.
(iii) Otherwise, it uses the equality theorem lift_to_left to move the target conjunct out to the left
      for one layer. The lifting steps work in bottom-up way during unwinding the recursive calls.

4     IMPLEMENTATION AND EVALUATION
In this section, we describe our prototype implementation of C★ and our evaluation of it. In §4.1,
we discuss some aspects of our prototype C★ implementation diverged from the core design in
§3. In §4.2, we present an empirical evaluation of our prototype implementation on a suite of C
benchmark programs and report some interesting findings on using C★ for program verification.

4.1    Implementation Notes
Following the workflow described in §3.1, our implementation consists of three main components:
the C★ compiler, the LCF-style proof kernel, and the symbolic-execution engine.

                                                    16
C★: Unifying Programming and Verification in C


   Implementing the C★ compiler. The C★ compiler, implemented in OCaml, processes C code
with C★-specific attributes, managing syntax extensions (quotation and anti-quotation) and trans-
lating them to invocations of term-parsing functions and substitution primitives. The compiler also
assembles code in the proof blocks to form a proof program that executes in the proof-supporting
runtime. Note that the proof program is a C program. Specifically, global proof blocks are moved to
the beginning of the generated C program, and each function in the implementation code creates a
proof function, with local proof blocks appended in the order of their appearance. It also aligns the
concrete annotation syntax (and separation-logic assertion syntax) used in C★ with the external
symbolic execution-engine.
   Reusing HOL Light proof kernel. In the implementation of C★, we reuse the LCF-style proof
kernel of the HOL Light prover [17], a minimal implementation of higher-order logic in OCaml. This
avoids the need to build a new LCF-style kernel from scratch in C, while leveraging the extensive
libraries available in HOL Light for mathematical reasoning. To support separation-logic entailment
proofs needed in program verification, we axiomatize a separation logic theory in HOL Light with
a concrete memory model in mind, interpreting the heap as a finite mapping from addresses to
bytes and treating integers and pointers the same in higher-order logic.
   Interfacing with the symbolic execution engine. In the ideal workflow illustrated in
Fig. 1, proof programs communicate with the symbolic-execution engine via functions like
get_symbolic_state(), set_symbolic_state(th), and feed_program_segment(prog). However, we currently
lack access to the internal states of the external symbolic-execution engine, making it challenging
to implement this interactive workflow directly. Consequently, we currently rely on the annotations
that the symbolic-execution engine supports for communication. To simulate the interleaving
execution pattern in the ideal workflow, we need to run the symbolic-execution engine twice for
each proof block: once for getting the symbolic state and once for setting it after running the proof
code. This is done manually for now.

4.2   Empirical Evaluation
To evaluate the effectiveness of our prototype implementation of C★, we selected a suite of small
C programs as benchmarks and verified their functional correctness using C★. Most examples are
adapted from the VeriFast repository [20], while the buddy allocator example is drawn from CN [35].
Some additional examples were crafted manually to test C★’s handling of complex control-flow
structures. This benchmark allows us to (i) test the functionality of the C★ toolchain, including its
frontend parser, proof-supporting runtime, and the translation phase, (ii) assess the expressiveness
of C★’s reasoning capabilities, and (iii) evaluate the usability of C★’s hybrid operational and
declarative proof approach.
   A complete list of the benchmark is shown in Tab. 2 and the source code of all benchmark
programs is included in the Supplementary Material. We chose these programs to encompass a
broad spectrum of reasoning patterns, including shared memory access (#1), control-flow constructs
(#2), dynamic memory management and interaction with external functions (#3), complex model-
level reasoning (#4), and a real-world case study (#5). Tab. 2 presents statistics regarding the
code size of each benchmark program. The column “#Line of Impl” lists the number of lines of
implementation code. The total number of lines in each benchmark program is significantly larger
due to the inclusion of proof code, whose statistics is given in the column “#Line of Proof,” as well
as specifications and assertions, whose statistics is given in the column “#Line of Spec/Assertion.”
We also include (i) the number of proof blocks for the operational style of verification and (ii) the
number of verification conditions for the declarative style of verification.

                                                 17
                                                                                                    Trovato et al.


Table 2. Evaluation of C★. “Impl” is short for “Implementation Code.” “PB” is short for “Proof Block.” “VC” is
short for “Verification Condition.” “Spec” is short for “Specficiation.” “Assert” is short for “Assertion.”

 Class    Name                   #Line of Impl     #PB    #VC     #Line of Proof     #Line of Spec/Assert
          address_of_local             32           4       0            14                    10
   #1     globals                      18           3       0            20                    4
          swap                         15           0       0             0                    7
          multi_branch                 24           10      0           102                    25
   #2     mutually_recursive           17            2      6           69                     13
          no_return                    15            1      0            4                     9
   #3     malloc_free                   9           1       0            9                      8
          clear                         9           7       0           120                    11
   #4     forall                       10           7       0           153                    13
          reverse                      18           7       1           375                    58
   #5     attach_page                  57           6       3          1616                   451


   Coverage of C language features. The evaluation demonstrates C★’s support for core C features,
especially those that create flexible aliasing patterns and complex control flow structures:
   • Control-flow constructs, including multiple branching (if...else if...), (mutually) recur-
     sive functions, break and continue, and (early) return. Benchmark programs address_of_local,
     multi_branch, mutually_recursive, and no_return use some of these constructs.
   • Shared memory access, covering global variables, arrays, addressable local variables, and
     (multi-level) pointer indirections. Benchmark programs address_of_local, globals, and swap
     make use of shared memory access.
   • Dynamic memory management and interaction with (formally specified) external functions,
     tested via malloc and free. The benchmark program malloc_free demonstrate those features.
Currently, our prototype implementation does not support switch statement, goto, or other looping
constructs (i.e., for and do while). We leave supporting those features for future work.
   Complex logical reasoning. The benchmarks also illustrate C★’s capability for performing
complex logic-level reasoning. The expressiveness of higher-order logic used in C★ enables users
to define functional models (as inductive data types, e.g., lists or trees) and also (well-founded)
recursive functions that operate on these models (e.g., reversing a list), using high-level definitional
mechanisms. Users can also define recursive representation predicates to link the entry points of
concrete memory structures to their functional models, a technique typical of separation-logic-based
program reasoning [6]. In several instances within our benchmark, we leveraged the pre-existing
proof libraries of HOL Light, thereby reducing the effort required for model-level reasoning.
Nonetheless, for the benchmark program reverse, we proved four logic-level reasoning lemmas and
two ownership-related reasoning lemmas, which are reusable for reasoning about linked lists.
   The proof code in those benchmark programs extensively uses C★’s standard proof-support
library. In addition to local_apply described in §3.2, our proof-support library includes other
reusable derived rules. For example, sep_normalize(t) transforms a heap proposition into a canoni-
cal form, sep_lift(l,t) lifts a sub-part of the heap proposition t to the far-left side, generalizing
the sep_lift_one function in Listing 3, and sep_reorder(t1,t2) verifies if two heap propositions are
reorderings of each other (modulo 𝛼-renaming of bound variables).
   A real-world case study: buddy allocator. Inspired by CN [35], we applied C★ to a more
challenging real-world case study: the attach function of the buddy allocator used in pKVM [32]. A

                                                     18
C★: Unifying Programming and Verification in C


struct hyp_page *__hyp_vmemmap;                [[invariant(`
static void attach_page(                       exists buddy_v bi inv_l inv_dl inv_hl i order_v
  struct hyp_pool *pool, struct hyp_page *pg        pg_v.
) {                                              data_at(&"max_order", Tuchar, &max_order) **
  struct hyp_page *buddy = NULL;                 data_at(&"order", Tuchar, &order_v) **
  u8 order = pg->order;                          data_at(&"pg", Tptr, pg_v) **
  pg->order = (u8)HYP_NO_ORDER;                  data_at(&"buddy", Tptr, buddy_v) **
  u8 max_order_ = pool->max_order;               data_at(&"pool", Tptr, pool_pre) **
  memset_page_zero(pg,order);                    data_at(&"__hyp_vmemmap", Tptr, vmemmap) **
  buddy = __find_buddy_avail(pool,pg,order);     (dlist_head_repr pool_pre 0 max_order inv_hl) **
  while ((order + 1) < max_order_ &&             (free_area_repr
         buddy != NULL) {                          (is_free_1st inv_l) start end inv_l) **
    page_remove_from_list_pool(pool,buddy);      (free_area_head_repr
    buddy->order = (u8)HYP_NO_ORDER;               (is_free_1st inv_l) start end inv_dl) **
    pg = min(pg, buddy);                         (store_pageinfo_array vmemmap start end inv_l) **
    order = order + 1;                           (store_zero_array
    buddy = __find_buddy_avail(pool,pg,order);     (i2vaddr i) 0 (PAGE_SIZE * (2 EXP order_v))
  }                                                (PAGE_SIZE * (2 EXP order_v))) **
  pg->order = order;                             ${other_facts_and_representation_predicates:hprop
  page_add_to_list_pool(pool,pg,order);             }
}                                              `)]]

           (a) The implementation code.                           (b) The invariant of the loop.
                                       Fig. 5. The attach_page function.


buddy allocator manages memory in blocks of size 2𝑜 × 4 KB, where 𝑜 ∈ 0, 1, . . . , max_order − 1
denotes the order of the block. Each block is aligned according to its size, maintaining an invariant
about the alignment for all blocks.
   Two blocks are called buddies if they (i) are adjacent, (ii) have the same order, and (iii) can be
merged into a larger block of the next order while preserving alignment. Allocatable memory is
divided into pools, each representing a contiguous range of pages. Every pool maintains a doubly-
linked list of free blocks for each order, and the allocator searches these lists for a free block of the
required size during memory allocation. Readers may refer to [35] for further details on the data
structures and helper functions used in this case study.
   We verified the attach_page function, shown in Fig. 5a, from the implementation of the buddy
allocator. This function operates by receiving a released block, identifying any adjacent free buddy
block in the pool, and merging them to form a larger free block. This merging process continues
iteratively until no more free buddies are found or the maximum order is reached. The resulting
block is then added back to the pool. The loop invariant of the while loop in the implementation
code is shown in Fig. 5b. An interesting finding during verification was that the specifications in
CN [35] were not sufficient to guarantee that all free blocks are present in a doubly-linked list.
Despite this, we adhered to these weaker specifications for simplicity in our verification efforts.
  Experience report. The experience of two undergraduate students in using C★ for benchmark
evaluation reveals several usability issues of the current prototype implementation:
  • IDE support. The lack of an IDE that shows symbolic states alongside code was a major pain
    point. Currently, users must run the symbolic execution engine manually and inspect symbolic
    states from its lengthy output, which interrupts the workflow. Developing an IDE for C★, e.g.,
    as an editor plugin, is left for future work.

                                                      19
                                                                                         Trovato et al.


    • Proof automation. C★ lacks automation for discharging trivial facts, making simple proofs
      time-consuming. This is partly due to the absence of solver-aided proof automation, heavily
      relied on by tools like CN [35] and VeriFast [20]. Looking forward, we plan to provide C★ an
      interface to encode and delegate proof obligations to external automated theorem provers or
      frameworks such as Z3 [10] and Why3 [11].
    • Proof-support library. Writing separation-logic entailment proofs in C★ currently requires
      considerable boilerplate code, leading to long and repetitive proof code. This issue arises
      because C★ lacks a rich set of derived rules for handling separation-logic reasoning, unlike
      mature frameworks such as Iris [23], VST [5], or CFML [7]. In our future work, we expect that
      expanding C★’s proof support libraries with more derived rules could improve the conciseness
      of proof code and developer productivity.

5    RELATED WORK
    Live Verification framework. The Live Verification framework [15] is a recently proposed
framework with a similar goal of enabling its users to verify their low-level code as they write
it. The framework is embedded in the Coq proof assistant and provides real-time display of the
symbolic state at the cursor position in the goal panel. After a function has been given a prototype
with formal specifications, users develop the function body incrementally by either writing the
next line of implementation code, or writing Ltac proof scripts to shift the view on the symbolic
state or discharge generated side conditions. When this derivation process is finished, a correctness
proof is produced alongside the assembled implementation code. With some clever tricks, these
Ltac source files can also be viewed as ordinary C code (with Ltac proof scripts in comments) and
compiled directly with C compilers.
    A key difference between C★ and the Live Verification framework is C★’s focus on accessibility
for conventional programmers. In the Live Verification framework, proof development and cus-
tomization of proof automation require proficiency in Coq’s Ltac tactic language, which diverges
from the imperative programming experience familiar to programmers. In contrast, C★ allows
proof code to be written directly in the same language as the implementation code, making it more
approachable for conventional programmers.
   VeriFast. VeriFast [20] is a state-of-the-art symbolic execution and separation logic-based auto-
mated verification tool for C and Java. It has a custom specification language that allows users to
define inductive data types, structurally recursive functions, and recursive representation pred-
icates. VeriFast emphasizes predictable automation: during symbolic execution, users manually
unfold and fold predicates using the proof commands open and close. A restricted form of existential
quantification is supported in the form of pattern matching, and reasoning on first-order values are
delegated to the SMT solver. When inductive reasoning is required, it supports user-written ghost
lemma functions, which are verified like the implementation code but require proof of termination
and must be observationally pure. VeriFast can handle a substantial subset of C features.
   The primary distinction between C★ and VeriFast lies in the extensibility of their proof support.
In VeriFast, proof support is limited to a fixed set of built-in ghost statements and basic induction
capabilities using lemma functions. On the other hand, C★ enables users to develop custom proof
rules and automation functions, offering greater flexibility and expressiveness for complex verifica-
tion tasks. Also, this extensibility allows experts to create high-level reasoning abstractions that
are accessible to programmers.
  CN. CN [35] is an ownership and refinement type system for C, targeting the verification of
real-world systems software. CN aims for predictable proof automation, employing the Liquid

                                                 20
C★: Unifying Programming and Verification in C


types [38] approach for decidable automation using an SMT backend, with heuristics for instan-
tiating quantifiers. It supports sound ownership reasoning at the type level using idea similar to
capabilities [1], split the type of a heap fragment into a linear capability type and an unrestricted
pointer type for flexible aliasing commonly found in real-world code. Additionally, CN is grounded
on a realistic semantics, Cerberus [29], which accurately models a large fragment of ISO C.

6   CONCLUSION
In this paper, we presented C★, a new system and language design for verified programming in
C. C★ provides three key features: (i) language-level integration supporting both declarative and
operational styles of verification, (ii) comprehensive reasoning capabilities within an expressive
logic using C’s programming paradigm, and (iii) support for real-time verification. It builds upon the
established techniques of separation logic-based symbolic execution for modular program reasoning,
as well as the LCF-style approach to programming proofs. We implemented a prototype of C★ and
evaluated its effectiveness by developing verified C programs using a suite of benchmark programs.
In the future, we plan to develop an IDE for C★ to enable interactive program verification, interface
C★ with solved-aided proof automation to reduce proof efforts, and develop more proof-support
libraries for C★.

REFERENCES
 [1] Amal Ahmed, Matthew Fluet, and Greg Morrisett. 2007. L3 : A Linear Language with Locations. Fundam. Informaticae
     77, 4 (2007), 397–449. http://content.iospress.com/articles/fundamenta-informaticae/fi77-4-06
 [2] Sidney Amani, Alex Hixon, Zilin Chen, Christine Rizkallah, Peter Chubb, Liam O’Connor, Joel Beeren, Yutaka
     Nagashima, Japheth Lim, Thomas Sewell, Joseph Tuong, Gabriele Keller, Toby C. Murray, Gerwin Klein, and Gernot
     Heiser. 2016. CoGENT: Verifying High-Assurance File System Implementations. In Proceedings of the Twenty-First
     International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2016,
     Atlanta, GA, USA, April 2-6, 2016, Tom Conte and Yuanyuan Zhou (Eds.). ACM, 175–188. https://doi.org/10.1145/
     2872362.2872404
 [3] Andrew W. Appel. 2011. Verified Software Toolchain - (Invited Talk). In Programming Languages and Systems - 20th
     European Symposium on Programming, ESOP 2011, Held as Part of the Joint European Conferences on Theory and Practice
     of Software, ETAPS 2011, Saarbrücken, Germany, March 26-April 3, 2011. Proceedings (Lecture Notes in Computer Science,
     Vol. 6602), Gilles Barthe (Ed.). Springer, 1–17. https://doi.org/10.1007/978-3-642-19718-5_1
 [4] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2005. Symbolic Execution with Separation Logic. In
     Programming Languages and Systems, Third Asian Symposium, APLAS 2005, Tsukuba, Japan, November 2-5, 2005,
     Proceedings (Lecture Notes in Computer Science, Vol. 3780), Kwangkeun Yi (Ed.). Springer, 52–68. https://doi.org/10.
     1007/11575467_5
 [5] Qinxiang Cao, Lennart Beringer, Samuel Gruetter, Josiah Dodds, and Andrew W. Appel. 2018. VST-Floyd: A Separation
     Logic Tool to Verify Correctness of C Programs. J. Autom. Reason. 61, 1-4 (2018), 367–422. https://doi.org/10.1007/
     S10817-018-9457-5
 [6] Arthur Charguéraud. 2016. Higher-order representation predicates in separation logic. In Proceedings of the 5th ACM
     SIGPLAN Conference on Certified Programs and Proofs, Saint Petersburg, FL, USA, January 20-22, 2016, Jeremy Avigad
     and Adam Chlipala (Eds.). ACM, 3–14. https://doi.org/10.1145/2854065.2854068
 [7] Arthur Charguéraud. 2020. Separation logic for sequential programs (functional pearl). Proc. ACM Program. Lang. 4,
     ICFP (2020), 116:1–116:34. https://doi.org/10.1145/3408998
 [8] Haogang Chen, Daniel Ziegler, Tej Chajed, Adam Chlipala, M. Frans Kaashoek, and Nickolai Zeldovich. 2015. Using
     Crash Hoare logic for certifying the FSCQ file system. In Proceedings of the 25th Symposium on Operating Systems
     Principles, SOSP 2015, Monterey, CA, USA, October 4-7, 2015, Ethan L. Miller and Steven Hand (Eds.). ACM, 18–37.
     https://doi.org/10.1145/2815400.2815402
 [9] Ernie Cohen, Markus Dahlweid, Mark A. Hillebrand, Dirk Leinenbach, Michal Moskal, Thomas Santen, Wolfram
     Schulte, and Stephan Tobies. 2009. VCC: A Practical System for Verifying Concurrent C. In Theorem Proving in Higher
     Order Logics, 22nd International Conference, TPHOLs 2009, Munich, Germany, August 17-20, 2009. Proceedings (Lecture
     Notes in Computer Science, Vol. 5674), Stefan Berghofer, Tobias Nipkow, Christian Urban, and Makarius Wenzel (Eds.).
     Springer, 23–42. https://doi.org/10.1007/978-3-642-03359-9_2


                                                            21
                                                                                                              Trovato et al.


[10] Leonardo Mendonça de Moura and Nikolaj S. Bjørner. 2008. Z3: An Efficient SMT Solver. In Tools and Algorithms
     for the Construction and Analysis of Systems, 14th International Conference, TACAS 2008, Held as Part of the Joint
     European Conferences on Theory and Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008.
     Proceedings (Lecture Notes in Computer Science, Vol. 4963), C. R. Ramakrishnan and Jakob Rehof (Eds.). Springer,
     337–340. https://doi.org/10.1007/978-3-540-78800-3_24
[11] Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3 - Where Programs Meet Provers. In Programming
     Languages and Systems - 22nd European Symposium on Programming, ESOP 2013, Held as Part of the European Joint
     Conferences on Theory and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013. Proceedings (Lecture
     Notes in Computer Science, Vol. 7792), Matthias Felleisen and Philippa Gardner (Eds.). Springer, 125–128. https:
     //doi.org/10.1007/978-3-642-37036-6_8
[12] Mike Gordon. 2000. From LCF to HOL: a short history. In Proof, Language, and Interaction, Essays in Honour of Robin
     Milner, Gordon D. Plotkin, Colin Stirling, and Mads Tofte (Eds.). The MIT Press, 169–186.
[13] David Greenaway, June Andronick, and Gerwin Klein. 2012. Bridging the Gap: Automatic Verified Abstraction of
     C. In Interactive Theorem Proving - Third International Conference, ITP 2012, Princeton, NJ, USA, August 13-15, 2012.
     Proceedings (Lecture Notes in Computer Science, Vol. 7406), Lennart Beringer and Amy P. Felty (Eds.). Springer, 99–115.
     https://doi.org/10.1007/978-3-642-32347-8_8
[14] David Greenaway, Japheth Lim, June Andronick, and Gerwin Klein. 2014. Don’t sweat the small stuff: formal verification
     of C code without the pain. In ACM SIGPLAN Conference on Programming Language Design and Implementation, PLDI
     ’14, Edinburgh, United Kingdom - June 09 - 11, 2014, Michael F. P. O’Boyle and Keshav Pingali (Eds.). ACM, 429–439.
     https://doi.org/10.1145/2594291.2594296
[15] Samuel Gruetter, Viktor Fukala, and Adam Chlipala. 2024. Live Verification in an Interactive Proof Assistant. Proc.
     ACM Program. Lang. 8, PLDI (2024), 1535–1558. https://doi.org/10.1145/3656439
[16] Ronghui Gu, Zhong Shao, Hao Chen, Xiongnan (Newman) Wu, Jieung Kim, Vilhelm Sjöberg, and David Costanzo.
     2016. CertiKOS: An Extensible Architecture for Building Certified Concurrent OS Kernels. In 12th USENIX Symposium
     on Operating Systems Design and Implementation, OSDI 2016, Savannah, GA, USA, November 2-4, 2016, Kimberly Keeton
     and Timothy Roscoe (Eds.). USENIX Association, 653–669. https://www.usenix.org/conference/osdi16/technical-
     sessions/presentation/gu
[17] John Harrison. 2009. HOL Light: An Overview. In Theorem Proving in Higher Order Logics, 22nd International Conference,
     TPHOLs 2009, Munich, Germany, August 17-20, 2009. Proceedings (Lecture Notes in Computer Science, Vol. 5674), Stefan
     Berghofer, Tobias Nipkow, Christian Urban, and Makarius Wenzel (Eds.). Springer, 60–66. https://doi.org/10.1007/978-
     3-642-03359-9_4
[18] John Harrison, Josef Urban, and Freek Wiedijk. 2014. History of Interactive Theorem Proving. In Computational Logic,
     Jörg H. Siekmann (Ed.). Handbook of the History of Logic, Vol. 9. Elsevier, 135–214. https://doi.org/10.1016/B978-0-
     444-51624-4.50004-6
[19] C. A. R. Hoare, Jayadev Misra, Gary T. Leavens, and Natarajan Shankar. 2009. The verified software initiative: A
     manifesto. ACM Comput. Surv. 41, 4 (2009), 22:1–22:8. https://doi.org/10.1145/1592434.1592439
[20] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. Ver-
     iFast: A Powerful, Sound, Predictable, Fast Verifier for C and Java. In NASA Formal Methods - Third Interna-
     tional Symposium, NFM 2011, Pasadena, CA, USA, April 18-20, 2011. Proceedings (Lecture Notes in Computer Science,
     Vol. 6617), Mihaela Gheorghiu Bobaru, Klaus Havelund, Gerard J. Holzmann, and Rajeev Joshi (Eds.). Springer, 41–55.
     https://doi.org/10.1007/978-3-642-20398-5_4
[21] Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris Yakobowski. 2015. Frama-C: A software
     analysis perspective. Formal Aspects Comput. 27, 3 (2015), 573–609. https://doi.org/10.1007/S00165-014-0326-7
[22] Gerwin Klein, June Andronick, Kevin Elphinstone, Toby C. Murray, Thomas Sewell, Rafal Kolanski, and Gernot Heiser.
     2014. Comprehensive formal verification of an OS microkernel. ACM Trans. Comput. Syst. 32, 1 (2014), 2:1–2:70.
     https://doi.org/10.1145/2560537
[23] Robbert Krebbers, Amin Timany, and Lars Birkedal. 2017. Interactive proofs in higher-order concurrent separation
     logic. In Proceedings of the 44th ACM SIGPLAN Symposium on Principles of Programming Languages, POPL 2017, Paris,
     France, January 18-20, 2017, Giuseppe Castagna and Andrew D. Gordon (Eds.). ACM, 205–217. https://doi.org/10.1145/
     3009837.3009855
[24] Ramana Kumar, Magnus O. Myreen, Michael Norrish, and Scott Owens. 2014. CakeML: a verified implementation of
     ML. In The 41st Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL ’14, San
     Diego, CA, USA, January 20-21, 2014, Suresh Jagannathan and Peter Sewell (Eds.). ACM, 179–192. https://doi.org/10.
     1145/2535838.2535841
[25] Dirk Leinenbach and Thomas Santen. 2009. Verifying the Microsoft Hyper-V Hypervisor with VCC. In FM 2009:
     Formal Methods, Second World Congress, Eindhoven, The Netherlands, November 2-6, 2009. Proceedings (Lecture Notes in
     Computer Science, Vol. 5850), Ana Cavalcanti and Dennis Dams (Eds.). Springer, 806–809. https://doi.org/10.1007/978-


                                                            22
C★: Unifying Programming and Verification in C


     3-642-05089-3_51
[26] Xavier Leroy. 2009. Formal verification of a realistic compiler. Commun. ACM 52, 7 (2009), 107–115. https:
     //doi.org/10.1145/1538788.1538814
[27] Shih-Wei Li, Xupeng Li, Ronghui Gu, Jason Nieh, and John Zhuang Hui. 2021. A Secure and Formally Verified Linux
     KVM Hypervisor. In 42nd IEEE Symposium on Security and Privacy, SP 2021, San Francisco, CA, USA, 24-27 May 2021.
     IEEE, 1782–1799. https://doi.org/10.1109/SP40001.2021.00049
[28] William Mansky and Ke Du. 2024. An Iris Instance for Verifying CompCert C Programs. Proc. ACM Program. Lang. 8,
     POPL (2024), 148–174. https://doi.org/10.1145/3632848
[29] Kayvan Memarian, Justus Matthiesen, James Lingard, Kyndylan Nienhuis, David Chisnall, Robert N. M. Watson, and
     Peter Sewell. 2016. Into the depths of C: elaborating the de facto standards. In Proceedings of the 37th ACM SIGPLAN
     Conference on Programming Language Design and Implementation, PLDI 2016, Santa Barbara, CA, USA, June 13-17, 2016,
     Chandra Krintz and Emery D. Berger (Eds.). ACM, 1–15. https://doi.org/10.1145/2908080.2908081
[30] Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. 2002. Isabelle/HOL - A Proof Assistant for Higher-Order
     Logic. Lecture Notes in Computer Science, Vol. 2283. Springer. https://doi.org/10.1007/3-540-45949-9
[31] Peter W. O’Hearn. 2019. Separation logic. Commun. ACM 62, 2 (2019), 86–95. https://doi.org/10.1145/3211968
[32] Android Open Source Project. 2024. Android Virtualization Architecture. Avaiable on https://source.android.com/
     docs/core/virtualization/architecture.
[33] Jonathan Protzenko, Bryan Parno, Aymeric Fromherz, Chris Hawblitzel, Marina Polubelova, Karthikeyan Bhargavan,
     Benjamin Beurdouche, Joonwon Choi, Antoine Delignat-Lavaud, Cédric Fournet, Natalia Kulatova, Tahina Ramananan-
     dro, Aseem Rastogi, Nikhil Swamy, Christoph M. Wintersteiger, and Santiago Zanella Béguelin. 2020. EverCrypt: A
     Fast, Verified, Cross-Platform Cryptographic Provider. In 2020 IEEE Symposium on Security and Privacy, SP 2020, San
     Francisco, CA, USA, May 18-21, 2020. IEEE, 983–1002. https://doi.org/10.1109/SP40000.2020.00114
[34] Jonathan Protzenko, Jean Karim Zinzindohoué, Aseem Rastogi, Tahina Ramananandro, Peng Wang, Santiago Zanella
     Béguelin, Antoine Delignat-Lavaud, Catalin Hritcu, Karthikeyan Bhargavan, Cédric Fournet, and Nikhil Swamy.
     2017. Verified low-level programming embedded in F*. Proc. ACM Program. Lang. 1, ICFP (2017), 17:1–17:29. https:
     //doi.org/10.1145/3110261
[35] Christopher Pulte, Dhruv C. Makwana, Thomas Sewell, Kayvan Memarian, Peter Sewell, and Neel Krishnaswami.
     2023. CN: Verifying Systems C Code with Separation-Logic Refinement Types. Proc. ACM Program. Lang. 7, POPL
     (2023), 1–32. https://doi.org/10.1145/3571194
[36] Tahina Ramananandro, Antoine Delignat-Lavaud, Cédric Fournet, Nikhil Swamy, Tej Chajed, Nadim Kobeissi, and
     Jonathan Protzenko. 2019. EverParse: Verified Secure Zero-Copy Parsers for Authenticated Message Formats. In
     28th USENIX Security Symposium, USENIX Security 2019, Santa Clara, CA, USA, August 14-16, 2019, Nadia Heninger
     and Patrick Traynor (Eds.). USENIX Association, 1465–1482. https://www.usenix.org/conference/usenixsecurity19/
     presentation/delignat-lavaud
[37] John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In 17th IEEE Symposium on
     Logic in Computer Science (LICS 2002), 22-25 July 2002, Copenhagen, Denmark, Proceedings. IEEE Computer Society,
     55–74. https://doi.org/10.1109/LICS.2002.1029817
[38] Patrick Maxim Rondon, Ming Kawaguchi, and Ranjit Jhala. 2008. Liquid types. In Proceedings of the ACM SIGPLAN
     2008 Conference on Programming Language Design and Implementation, Tucson, AZ, USA, June 7-13, 2008, Rajiv Gupta
     and Saman P. Amarasinghe (Eds.). ACM, 159–169. https://doi.org/10.1145/1375581.1375602
[39] Michael Sammler, Rodolphe Lepigre, Robbert Krebbers, Kayvan Memarian, Derek Dreyer, and Deepak Garg. 2021.
     RefinedC: automating the foundational verification of C code with refined ownership types. In PLDI ’21: 42nd ACM
     SIGPLAN International Conference on Programming Language Design and Implementation, Virtual Event, Canada, June
     20-25, 2021, Stephen N. Freund and Eran Yahav (Eds.). ACM, 158–174. https://doi.org/10.1145/3453483.3454036
[40] Runzhou Tao, Jianan Yao, Xupeng Li, Shih-Wei Li, Jason Nieh, and Ronghui Gu. 2021. Formal Verification of a
     Multiprocessor Hypervisor on Arm Relaxed Memory Hardware. In SOSP ’21: ACM SIGOPS 28th Symposium on
     Operating Systems Principles, Virtual Event / Koblenz, Germany, October 26-29, 2021, Robbert van Renesse and Nickolai
     Zeldovich (Eds.). ACM, 866–881. https://doi.org/10.1145/3477132.3483560
[41] Fengwei Xu, Ming Fu, Xinyu Feng, Xiaoran Zhang, Hui Zhang, and Zhaohui Li. 2016. A Practical Verification
     Framework for Preemptive OS Kernels. In Computer Aided Verification - 28th International Conference, CAV 2016,
     Toronto, ON, Canada, July 17-23, 2016, Proceedings, Part II (Lecture Notes in Computer Science, Vol. 9780), Swarat
     Chaudhuri and Azadeh Farzan (Eds.). Springer, 59–79. https://doi.org/10.1007/978-3-319-41540-6_4
[42] Litao Zhou, Jianxing Qin, Qinshi Wang, Andrew W. Appel, and Qinxiang Cao. 2024. VST-A: A Foundationally Sound
     Annotation Verifier. Proc. ACM Program. Lang. 8, POPL (2024), 2069–2098. https://doi.org/10.1145/3632911

Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009



                                                           23
