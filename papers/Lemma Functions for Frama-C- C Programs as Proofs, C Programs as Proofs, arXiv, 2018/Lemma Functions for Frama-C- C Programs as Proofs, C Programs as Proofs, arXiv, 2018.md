                                                                  Lemma Functions for Frama-C:
                                                                     C Programs as Proofs
                                                 Grigoriy Volkov                            Mikhail Mandrykin                              Denis Efremov
                                           Faculty of Computer Science          Software Engineering Department           Faculty of Computer Science
                                           National Research University Ivannikov Institute for System Programming of the National Research University
                                            Higher School of Economics            Russian Academy of Sciences              Higher School of Economics
                                                 Moscow, Russia                          Moscow, Russia                         Moscow, Russia
                                               gdvolkov@edu.hse.ru                     mandrykin@ispras.ru                      defremov@hse.ru
arXiv:1811.05879v1 [cs.SE] 14 Nov 2018




                                            Abstract—This paper describes the development of             to additionally specify loop invariants and termination
                                         an auto-active verification technique in the Frama-C            expression (loop variants) in case the function under
                                         framework. We outline the lemma functions method                analysis contains loops. Then the verification instrument
                                         and present the corresponding ACSL extension, its
                                         implementation in Frama-C, and evaluation on a set              generates verification conditions (VCs), which can be
                                         of string-manipulating functions from the Linux kernel.         separated into categories: safety and behavioral ones.
                                         We illustrate the benefits our approach can bring con-          Safety VCs are responsible for runtime error checks for
                                         cerning the effort required to prove lemmas, compared           known (modeled) types, while behavioral VCs represent
                                         to the approach based on interactive provers such as            the functional correctness checks. All VCs need to be
                                         Coq. Current limitations of the method and its imple-
                                         mentation are discussed.                                        discharged in order for the function to be considered fully
                                            Index Terms—formal verification, deductive verifi-           proved (totally correct). This can be achieved either by
                                         cation, Frama-C, auto-active verification, lemma func-          manually proving all VCs discharged with an interactive
                                         tions, Linux kernel                                             prover (i. e., Coq, Isabelle/HOL or PVS) or with the help
                                                                                                         of automatic provers.
                                                               I. Introduction                              It is well known that most problems related to verifying
                                                                                                         the conformance between some code in basically any
                                            Deductive verification is one of the most “heavyweight” practical programming language and its formal specification
                                         static techniques of formal reasoning about software prop- in any sufficiently expressive specification language are
                                         erties. It requires manual annotation of source code with undecidable in general. The situation when an automatic
                                         formal specifications and manual or semi-automatic proof prover cannot discharge a verification condition is common.
                                         of conformance between code and specifications. Deductive This may be due to various reasons: limited time or
                                         verification is applied in areas where the cost of error can memory resources for the prover, an error in the code,
                                         be too high. The main benefit of this approach is that an incorrect formal specification, an incomplete formal
                                         it can mathematically guarantee that code is free from specification, an incapacity of the prover to finish the proof.
                                         particular error classes.                                       The specifications debugging is hard. Despite the modern
                                            In the toolsets based on the Hoare logic (such as Frama- advances [5]–[7] in the field, the whole situation is still
                                         C [1], VeriFast [2], Dafny [3], GNATprove [4]), in order to poor when specifications become complex.
                                         verify the correctness of a function, the verification engineer    As it can be seen the whole process of deductive verifica-
                                         is required to define a precondition — a predicate that tion requires a significant manual effort from a verification
                                         should hold in order for the following code to be functionally engineer. This implies that practically all verification
                                         correct and contain no runtime errors (i. e., models of tools have some capabilities for user interaction beyond
                                         undefined behavior that are known to the verification tool), simply supplying the program and its specification. This
                                         a postcondition — a predicate that should hold after a additional user interaction required to eventually prove
                                         function execution and describe what this code should act the correspondence between the code and its specification
                                         like to be functionally correct. Pre- and postconditions is usually called the proof overhead. This overhead can
                                         form the function’s contract. Frame-conditions or effects significantly depend on the way the user interaction is
                                         are sometimes viewed as a separate entity in the contract, accomplished in a particular verification tool. Even though
                                         but typically they present a type of postcondition that these ways can generally be very diverse, for simplicity we
                                         restrict the memory state of a program. A formal contract dare to speculatively group them into the following three
                                         is required to reason about the function’s correctness.         major categories:
                                            Given a formal contract, an engineer can try to prove that      ∙ External provers. The vast majority of verification
                                         a function conforms to its specification. To do this one needs        tools support this approach to user interaction at
     some point, be it as a part of a standard workflow or      the project is to develop the correct and detailed ACSL [14]
     as a last resort. The essence is that the verification     specifications and fully prove these functions with the
     conditions (VCs) produced by the tool are translated       Frama-C framework. Thus, evaluating the toolset (Frama-
     into the native language of some interactive proof         C + AstraVer Plugin (a fork of Jessie) + Why3 + Solvers)
     assistant, e. g., Coq, Isabelle/HOL or PVS. Then the       on the real code (not artificial examples) and highlighting
     resulting theorems are proved using the capabilities of    C idioms that are hard to describe with ACSL specification,
     the prover, sometimes with some extensions provided        not possible to model with the deductive verification plugin,
     by the verification tool, e. g., custom tactics. This      or just giving the right direction for the tools development.
     approach is often both simple and efficient, but for          ACSL is a Behavioral Interface Specification Language
     some use cases, it has significant drawbacks such as       (BISL) [16] implemented in Frama-C. At the same time,
     the ones we describe in this paper.                        many higher-level formalisms for efficient specification
   ∙ Interactive proof editors. Some verification tools such    and verification of heap-manipulating or parallel programs
     as WP plugin for Frama-C, Why3 verification plat-          such as dynamic frames, separation logic, permissions,
     form or KIV [8] verification system go further and         rely/guarantee reasoning (e. g., ownership methodology),
     implement their own custom interactive proof manage-       specification refinement (e. g., function contract inclusion)
     ment facilities such as tactics, transformations, and      or auto-active verification are not included in ACSL.
     strategies. This is a hard yet powerful approach with      Therefore ACSL is not tightly bound to any particular
     its own advantages and shortcomings. One of its major      verification methodology and support for its features can
     disadvantages especially relevant to our particular case   significantly vary in tools.
     is a high implementation overhead, which prevents
     tentative adoption and quick preliminary evaluation        A. Verification Approach
     of the results.                                               Specifications development is an iterative process. It
   ∙ Auto-active proofs. One of the possible techniques         cannot be broadly described in the general case. Every
     to reduce and automate the manual work and make            algorithm requires its own approach [17]–[20] with separate
     deductive verification more suitable for such meth-        axiomatizations fitting each particular case and implemen-
     ods as continuous verification [9]–[11] is auto-active     tation. A common way to write formal specifications is
     verification. The general idea is to express the proofs    to factor out the most complex logical statements into
     in the same input language as the program and its          theorems and lemmas so that the provers can discharge
     specification themselves relying on the Curry-Howard       the rest of the verification conditions automatically. The
     correspondence between the programs and the proofs.        theorems and lemmas are then proved manually with an
     This approach is quite widely applied in particular        interactive prover. The main benefits of this approach are
     in such verification tools as Dafny [3], VeriFast [2],     the following:
     GNATprove [12], and Why3 [13]. This is the approach           ∙ Lemmas are formulated in a more general way so
     that we pursue and evaluate in this paper.                      that they contain less implementation context specific
   In this paper, we present our experience with integra-            details (e. g., the assertion in a particular function).
tion of support for auto-active verification in ACSL [14],           This eases the process of their manual proving and
Frama-C, and AstraVer deductive verification tool and                allows one to reuse them in multiple proofs of VCs
applying this approach to our existing set of specified              and other lemmas.
string-manipulating functions from the Linux kernel. We            ∙ In this case, lemmas are “aside from code”, thus
demonstrate that integration of auto-active proofs to ACSL           making formal specifications more maintainable and
and Frama-C is both beneficial and promising approach to             tolerable to small code changes because they rarely
automated deductive verification that significantly reduces          provoke changes in general statements.
manual proof overhead.                                          The VerKer project adheres to this approach in the
   This paper is organized as follows. In Section II we give    ACSL specifications. The project currently contains 26
an overview of the VerKer project and its specifications        fully proved functions from Linux kernel library folder,
and describe the problems we are solving by applying auto-      16 functions among them are string related (i. e., have
active verification to this project. Next, in Section III we    the str* prefix and perform operations on strings), and
present the implementation of the technique in the Frama-       7 are memory related (i. e., have mem* prefix). Only 9
C framework and the AstraVer plugin. In Sections IV and V       functions (see Table I) contain in its formal specification a
we describe the obtained result and discuss future work on      logical function with lemmas formulated on it. The formal
open issues.                                                    contracts are written in a way to prove correspondence
                                                                between logical functions and C functions. The lemmas are
                  II. VerKer Project                            excessive, and provers sometimes can automatically prove
                                                                the correctness of a lemma based on other lemmas.
  The VerKer project [15] consists of standard library             In the paper [15] it is claimed that the functions are
functions taken from the Linux kernel. The main idea of         fully-proved but lemmas are not proved (only automatic
      Function     Number of       Proved       Unproved
       Name         Lemmas      Automatically                      provers, e. g., SMT-solvers since the VCs should remain
  check_bytes8         3             3             0               manageable by different tools that apply different
  strlen              10             4             6               tactics or decision procedures. In particular, while
  skip_spaces          7              1            6               SMT solvers efficiently handle large ground (quantifier-
  strchr               7             4             3
  strchrnul            7             5             2               free) formulas modulo theories, most interactive tools
  strspn               8             5             3               are much more suitable to handle smaller formulas in
  strcspn              5             2             3               higher-order logic.
  strnlen             17             11            6
  strpbrk              5             2             3             ∙ External proofs introduce additional problems of proof

  Total               69             37            32              location and sharing when the same lemma is included
                                                                   or imported in several source code files.
                        TABLE I
              Lemmas in the VerKer project


checks for contradiction was performed). The proving of                      III. Auto-active Proofs
all lemmas in the project considered as a future work in
the paper.

B. Shortcomings and limitations                                   According to its original definition in [21], auto-active
                                                               verification is any verification technique where user input
  Thus we can found the following limitations of the
                                                               is supplied before VC generation. The user input can
approach based on external provers:
                                                               be given in various forms including but not limited to:
  ∙ The use of external interactive proof assistants or
                                                               auxiliary annotations such as verifier pragmas, triggers,
    proof editors requires the users to get accustomed to ad-hoc lemma instantiations, ghost code, and lemma
    at least two different specification representations, cor- functions. Among those, lemma functions are a primary tool
    responding languages and tools. This makes it harder intended to convey proofs of user-defined auxiliary lemmas.
    for the users to employ their skills acquired during The proofs are expressed as ordinary pure (i. e., without
    the process of specification within one verification side-effects) total (i. e., always successfully terminating)
    environment (e. g., the deductive verification plugin) imperative functions. Though the execution of pure total
    later in the process of proof within the other one imperative code does not produce any observable effects
    (e. g., the Coq proof assistant). In particular, the range with respect to the programming language semantics, when
    of supported language constructs can significantly dif- interpreted by the verification tool the instructions of the
    fer. Many ACSL constructs such as pointer dereference code can produce a substantial effect on its internal state
    do not have direct counterparts in the language of the or the internal state of the automatic theorem prover. In
    interactive prover.                                        particular, through the process of VCs generation, the
  ∙ The reproduction of external proofs requires the use of
                                                               proof-carrying code can determine the fragment of current
    external tools that work on their own representations proof context that is explicitly known to the verifier or the
   — yet the translations performed by the verification prover versus the fragment that is only known implicitly as
    tool in order to obtain the external representations can a set of derivable inferences. As most of the logic relevant
    cause various surprising instabilities, where the proof to deductive verification is generally undecidable, neither
    suddenly fails after small supposedly irrelevant changes the verifier nor the prover can ever explore all propositions
    are made to program source code or specifications. derivable in the current context. The code of the lemma
    This is especially well demonstrated by the pervasive functions thus serves as a guide for the verification tool
    problem of generating unique, stable and predictable that efficiently indicates the relevant parts of the search
    names for various program and specification entities space. One of the most significant cases where verification
    such as variables and lemmas. For instance, when tools need such a guide is with inductive proofs as they
    a lemma or variable is renamed, the proofs have to have very limited support in automatic provers.
    be adjusted accordingly, yet the relation between the
    names used in the original program and the names
    used in the proofs can be quite complex.                      Consider the following inductive proof expressed as a
  ∙ The external proofs are kept separately from the           lemma function:
    specifications and are therefore not directly available
    to the reader of the verified program. This can make it
    harder to estimate the effort needed for modification of            logic char * strchrnul(char * 𝑠, char 𝑐) =
    certain parts of the program or specification or to keep              *𝑠 ≡ 𝑐 ? 𝑠 :
    the proofs in sync with the program and specification.                *𝑠 ≡ ′ ∖0′ ? 𝑠 :
  ∙ The use of external interactive provers prevents an ap-                  𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙(𝑠 + 1, 𝑐);
    plication of various encodings optimized for automatic              ...
 /*@ ghost                                                     lemma function into ACSL in particular. We first present
   @ /@ lemma                                                  our existing approach and current results that we obtained
   @ @ requires 𝑣𝑎𝑙𝑖𝑑_𝑠𝑡𝑟(𝑠);                                  by using it, and then we discuss some of its limitations and
   @ @ decreases 𝑠𝑡𝑟𝑙𝑒𝑛(𝑠);                                    possible directions of future developments.
   @ @ ensures 𝑠 ≤ 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙(𝑠, 𝑐) ≤ 𝑠𝑡𝑟 + 𝑠𝑡𝑟𝑙𝑒𝑛(𝑠);
   @ @/                                                        A. Integrating Lemma Functions Into ACSL/Frama-C
   @ void 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙_𝑖𝑛_𝑟𝑎𝑛𝑔𝑒(char * 𝑠, char 𝑐)
                                                                  In our fork of the Frama-C platform developed as
   @{
                                                               part of the AstraVer toolset, we implemented relatively
   @ if (*𝑠 ! = ′ ∖0′ && *𝑠 ! = 𝑐)
                                                               simple support for lemma functions as a special case of
   @ 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙_𝑖𝑛_𝑟𝑎𝑛𝑔𝑒(𝑠 + 1, 𝑐);
                                                               total pure ghost functions. Both ACSL specification and
   @}
                                                               its implementation in mainline Frama-C provide support
   @*/
                                                               for ghost functions. Meanwhile, the AstraVer plugin is
The lemma and its proof are expressed within a single          able to generate VCs to check ACSL assigns, allocates,
recursive function definition 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙_𝑖𝑛_𝑟𝑎𝑛𝑔𝑒. The          decreases and terminates clauses of function contracts.
induction here is simple as it exactly follows the recursive   So the only missing part to provide basic support for lemma
definition of the logic function 𝑠𝑡𝑟𝑐ℎ𝑛𝑢𝑙. The pre-condition   functions was the automatic generation of lemmas and their
of the function requires the parameter string 𝑠 to be a        implicit importing in all the code functions located further
valid C string so that it has a well-defined finite length.    in the source code.
Then the if statement in the function body splits between         More concretely, in order to allow lemma functions to
the base and inductive cases. In the base cases *𝑠 == ′ ∖0′    be used in a similar way to regular ACSL lemmas (which
and *𝑠 == 𝑐 the post-condition trivially follows from the      can only be written in logic), we introduced a new lemma
definition of the function 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙. In the inductive case,   keyword for C function specifications.
which corresponds to the body of the if statement, the            Our modified version of Frama-C processes it in the
post-condition follows from the inductive assumption for       following way:
strings of a smaller length and an additional instance            ∙ For a function contract of the form
of a lemma about the length of the string 𝑠 + 1 that                    /@ requires 𝑅(𝑝1 , . . . , 𝑝𝑛 , 𝑔1 , . . . , 𝑔𝑛 );
is implicitly present in the proof context (this lemma is                @ ensures 𝐸(𝑝1 , . . . , 𝑝𝑛 , 𝑔1 , . . . , 𝑔𝑛 , ∖𝑟𝑒𝑠𝑢𝑙𝑡);
actually also proved by a lemma function that is provided                @/,
earlier in the code). The recursion is well-founded since in        where 𝑝1 , . . . , 𝑝𝑛 are function parameters, 𝑔1 , . . . , 𝑔𝑛
the only recursive call the value of the variant 𝑠𝑡𝑟𝑙𝑒𝑛(𝑠)          are global variables and the special variable ∖𝑟𝑒𝑠𝑢𝑙𝑡 de-
specified in the decreases clause is strictly smaller than          notes the return value of the function, a corresponding
that in the caller function. With the AstraVer plugin, the          axiom is generated, that is, an axiom of the form
correctness of the function 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙_𝑖𝑛_𝑟𝑎𝑛𝑔𝑒 can be                      ∀typeof(𝑝1 ) 𝑝1 , . . . , typeof(𝑝𝑛 ) 𝑝𝑛 ,
verified automatically by discharging all the VCs using an                   typeof(𝑔1 ) 𝑔1 , . . . , typeof(𝑔𝑛 ) 𝑔𝑛 ;
SMT solver such as Alt-Ergo or CVC4. The automatic                             ∃typeof(∖𝑟𝑒𝑠𝑢𝑙𝑡) ∖𝑟𝑒𝑠𝑢𝑙𝑡;
proofs require no induction and only a few quantifier                               𝑅(𝑝1 , . . . , 𝑝𝑛 , 𝑔1 , . . . , 𝑔𝑛 ) =⇒
instantiations, while all the necessary terms are explicitly                            𝐸(𝑝1 , . . . , 𝑝𝑛 , 𝑔1 , . . . , 𝑔𝑛 , ∖𝑟𝑒𝑠𝑢𝑙𝑡);
present in the VCs. So in either solver, the verification         ∙ All logic definitions such as functions, predicates, ax-
takes far less than a second.                                       ioms, and lemmas in ACSL are grouped into axiomatic
   Now since the function 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙_𝑖𝑛_𝑟𝑎𝑛𝑔𝑒 is proved              blocks. The generated axiom is placed in a new ax-
correct for arbitrary values of its parameters, and since           iomatic block. AstraVer implements on-demand import
the function is pure and total, the statement about its             of all the definitions from axiomatic blocks based on
correctness with respect to the contract can be expressed           occurrences of symbols defined in the axiomatic. As
as the following lemma:                                             the axiom name cannot be directly used in an ACSL
        lemma 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙_𝑖𝑛_𝑟𝑎𝑛𝑔𝑒 :                                  specification, the axiom is not included in any proof
          ∀char * 𝑠, char 𝑐;                                        context until some other symbol in this new axiomatic
             𝑣𝑎𝑙𝑖𝑑_𝑠𝑡𝑟(𝑠) =⇒                                        is defined and later used in another specification (code
               𝑠 ≤ 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙(𝑠, 𝑐) ≤ 𝑠𝑡𝑟 + 𝑠𝑡𝑟𝑙𝑒𝑛(𝑠);               function or another axiomatic block). In particular,
This lemma can be automatically generated from the                  this approach removes the axiom from the context of
function contract and used in the proofs later in the               the lemma function itself, preventing the axiom from
program code, both explicitly by the user by calling                trivially proving the function’s verification conditions.
the function 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙_𝑖𝑛_𝑟𝑎𝑛𝑔𝑒 with some concrete                ∙ A dummy identically true predicate with a unique
arguments or implicitly by the SMT solver by instantiating          name is generated, and its definition is added into the
the lemma with some concrete terms.                                 new axiomatic block.
   This is the basic idea of lemma functions and their use.       ∙ A precondition requiring the dummy predicate from
Now let us consider our approach to the integration of              the new axiomatic block is inserted into the contracts
                                                                           Function        Number of       Number of
     of all function located after the currently processed                  Name             Ghost          Lemma
     lemma function, which causes the definitions from the                                 Functions       Functions
     axiomatic block (including the generated axiom) to                 strlen                4               2
     be imported into the proof context of these functions.             skip_spaces            1              3
                                                                        strchr                0               5
     As the dummy predicate is generated by the tool and                strchrnul             0               5
     has a unique name, the user cannot access it and thus              strspn                 1              5
     create any extra dependencies disrupting the ordering              strcspn               0               3
                                                                        strnlen               3               6
     of lemma proofs according to their code locations.                 strpbrk               0               2
   ∙ The lemma function itself gets some additional clauses             Total                 9               31
     inserted into its contract specification:
                                                                                          TABLE II
     – assigns ∖𝑛𝑜𝑡ℎ𝑖𝑛𝑔; allocates ∖𝑛𝑜𝑡ℎ𝑖𝑛𝑔 — to en-                                   Lemma functions
        sure the function is pure (i. e., it does not touch any
        global state);                                            custom tactics could potentially result in a much smaller
     – terminates ∖𝑡𝑟𝑢𝑒; – to prevent abrupt termination          number.
       (i. e., calls to exit(), abort() etc.) — loop and
        recursion termination is already required by default        However, in the context of our project, the use of lemma
        in the AstraVer plugin.                                   functions became a decisive choice that enabled complete,
  An alternative approach enforcing the topological or-           practical, stable and future-proof verification of auxiliary
dering of lemma functions has been considered: explicit           lemmas with minimal implementation effort. The ability to
removal of the axiom from the context of the functions            instantiate lemmas by explicitly calling the corresponding
located before the lemma body. This is possible to achieve        lemma functions and the availability of all general C
using the meta remove_prop pragma in the generated                constructs in the proof code provided the verification
Why3ML model. However, this would have required Frama-            engineer with sufficient control. By these means in our
C to track the connection between the function and the            examples we were able to reduce the verification time of
axiom explicitly, and the AstraVer plugin to use that             each lemma function (cumulative time of the solvers on all
connection to generate the meta statement in the WhyML            function’s VCs) to a few seconds.
output. A minimal implementation that fully translates
lemma functions into existing specification entities was
chosen in the end.                                                         V. Open Issues and Future Work

                       IV. Results
                                                               A. Logic types and expressions in code
   Even though at the previous stage of out project [15] we
ended up with 32 unproved lemmas, we did not attempt to
                                                                  Unlike many specification languages originally developed
match our lemma function proofs at this stage exactly with
                                                               with auto-active verification in mind, ACSL maintains a
the lemmas used at the previous stage. Instead, the goal was
                                                               clear distinction between code and specification languages.
to ensure all the code can be verified without resorting to
                                                               In particular, C and logic types as well as C and logic
any additional assumptions by completely replacing all the
                                                               expressions are represented entirely separately within the
lemmas involved with a minimum required set of lemma
                                                               Frama-C kernel and are only allowed in their respective
functions. Thus we ended up with 31 lemma functions
                                                               positions. Therefore lemma functions cannot be directly
required to fully prove the VCs for some code functions as
                                                               used to prove the lemmas with quantification over logic
presented in Table II.
                                                               types. This limitation can be overcome in individual cases of
   Unfortunately, a thorough comparison of the proof quantified logic variables ranging over the domains bounded
overhead between the interactive and auto-active proofs by C values.
turned out to be very hard. The current support for
interactive proofs that existed in AstraVer plugin was quite      For universal quantification of the form
basic, which resulted in considerably large manual proofs.
The reduction of these proofs seems only possible with very
                                                                              ∀ L 𝑣; 𝑣1 ≤ 𝑣 < 𝑣2 =⇒ 𝑃 (𝑣),
significant implementation effort including implementation
of relevant custom tactics and optimizing the VC generation
for manual proofs. For the reference, we provide an where 𝑣1 and 𝑣2 are C values of type C a proof can be
illustrative comparison of an interactive auto-active proof of accomplished through the use of an auxiliary lemma
a single lemma in Figure 1 as it can be performed with the
current implementation. This example shows the reduction                   aux: ∀ C 𝑣; 𝑣1 ≤ 𝑣 < 𝑣2 =⇒ 𝑃 (𝑣),
in proof overhead of more than tenfold, yet a different
more optimized manual proof augmented with appropriate which can then be generalized using a dummy proof of the
                                                                          ⎫
  1 Theorem Strchr_skipped :                                              ⎪
                                                                          ⎪
  2 ∀ voidP_str_0_30_alloc_table_at_L: alloc_table voidP,
                                                                          ⎪
                                                                          ⎪
  3 ∀ charP_charM_str_0_30_at_L : map (pointer voidP) Int8.t,
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
  4 ∀ str_0_0 : pointer voidP,
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
  5 ∀ c_1_0 : Int8 . t ,
                                                                          ⎪
                                                                          ⎪
  6 ∀ i_0_0 : Uint64. t ,
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
  7    valid_str
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
  8       str_0_0
                                                                          ⎪
                                                                          ⎪
  9
                                                                          ⎪
          voidP_str_0_30_alloc_table_at_L
                                                                          ⎪
                                                                          ⎪
10        charP_charM_str_0_30_at_L ∧
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
 11    strchr
                                                                          ⎪
                                                                          ⎪
12
                                                                          ⎪




                                                                              Generated by Why3
          str_0_0
                                                                          ⎪
                                                                          ⎪
13        c_1_0
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
14        charP_charM_str_0_30_at_L ̸=(null : pointer voidP) ∧
                                                                          ⎪
                                                                          ⎪
15
                                                                          ⎪
       Uint64. infix_lseq (Uint64. of_int 0%Z) i_0_0 ∧
                                                                          ⎪
                                                                          ⎪
16     (Uint64. to_int i_0_0 < sub_pointer
                                                                          ⎪
                                                                          ⎬
17                                   (strchr
18                                       str_0_0                          ⎪
19                                       c_1_0
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
20                                       charP_charM_str_0_30_at_L)
                                                                          ⎪
                                                                          ⎪
21
                                                                          ⎪
                                       str_0_0))%Z →
                                                                          ⎪
                                                                          ⎪
22     get
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
23        charP_charM_str_0_30_at_L
                                                                          ⎪
                                                                          ⎪
24
                                                                          ⎪
          (shift str_0_0 (Uint64.to_int i_0_0)) ̸= c_1_0.
                                                                          ⎪
                                                                          ⎪
25 (* Why3 intros
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
26     voidP_str_0_30_alloc_table_at_L
                                                                          ⎪
                                                                          ⎪
27
                                                                          ⎪
       charP_charM_str_0_30_at_L
                                                                          ⎪
                                                                          ⎪
28     str_0_0 c_1_0 i_0_0
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
29     ( h1,( h2,( h3,( h4, h5)))). *)
                                                                          ⎪
                                                                          ⎪
30 intros                                                                                               1 /*@ ghost
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
31     voidP_str_4_82_alloc_table_at_L                                                                  2   @ /@ lemma
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
32     charP_charM_str_4_82_at_L                                                                        3   @ @ requires 𝑣𝑎𝑙𝑖𝑑_𝑠𝑡𝑟(𝑠𝑡𝑟);
                                                                          ⎪
                                                                          ⎪
33
                                                                          ⎪
       str_4 c_4_0 i_1                                                                                  4   @ @ requires 𝑠𝑡𝑟𝑐ℎ𝑟(𝑠𝑡𝑟, 𝑐) ̸= ∖𝑛𝑢𝑙𝑙;
                                                                          ⎪
                                                                          ⎭
34     (h1,( h2,( h3,( h4,h5)))).                                                                       5   @ @ requires 0 ≤ 𝑖 < 𝑠𝑡𝑟𝑐ℎ𝑟(𝑠𝑡𝑟, 𝑐) − 𝑠𝑡𝑟;
35
                                                                                                        6   @ @ decreases 𝑖;
36 Definition P (i : int ) :=
                                                                          ⎫
37     ∀ a : alloc_table voidP,                                           ⎪                             7   @ @ ensures 𝑠𝑡𝑟[𝑖] ̸= 𝑐;
                                                                                                        8   @ @/
                                                                          ⎪
38     ∀ m : map (pointer voidP) Int8 . t ,
                                                                          ⎪
                                                                          ⎪
                                                                                                        9   @ void strchr_skipped ( char ∗ str , char c ,
                                                                          ⎪
39     ∀ s : pointer voidP,
                                                                          ⎪
                                                                          ⎪
40                                                                                                     10   @                          size_t i )
                                                                          ⎪
       ∀ c : Int8 . t ,                                                   ⎪
                                                                          ⎪
41        valid_str s a m ∧                                                                            11   @ {
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
42        strchr s c m ̸=(null : pointer voidP) ∧                                                      12   @   i f ( i > 0 && ∗ s t r != ’ \0 ’ && ∗ s t r != c )
                                                                          ⎪
                                                                          ⎪
43
                                                                          ⎪
          (0 ≤ i )%Z ∧                                                    ⎪
                                                                          ⎪                            13   @      strchr_skipped ( s t r + 1 , c , i − 1 ) ;
44        (i < sub_pointer (strchr s c m) s)%Z →
                                                                          ⎪
                                                                                                       14   @ }
                                                                          ⎪
                                                                          ⎪
45        get m (shift s i ) ̸= c.
                                                                          ⎪
                                                                                                       15   @∗/
                                                                          ⎪
46 specialize Wf_Z.natlike_rec3 with (P := P) as Ind.
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
47 assert (P 0) as Base.
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
48     unfold P.
                                                             ⎫            ⎪
                                                                          ⎪
49
                                                                          ⎪
       intros a m s c Valid .
                                                             ⎪
                                                             ⎪            ⎪
                                                               13 lines




                                                                          ⎪
50
                                                             ⎪
       unfold not.
                                                                              93 lines of user proof




                                                             ⎪
                                                             ⎬            ⎪
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
       ...                                                                ⎪
                                                                          ⎪
                                                                          ⎪
 58
                                                                          ⎪
          rewrite First in Valid .
                                                           ⎪⎪             ⎪
                                                                          ⎪
                                                            ⎪
 59       rewrite Sub_pointer_self in Valid .
                                                            ⎪
                                                            ⎭             ⎪
                                                                          ⎬
 60       omega.
 61     assert (∀ z : int , (0 < z)%Z → P (Z.pred z) → P z) as
                                                            ⎫Step.        ⎪
 62       intros z Gt0 Pred.
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
 63       unfold P.
                                                            ⎪
                                                            ⎪             ⎪
                                                                          ⎪
                                                               55 lines




 64
                                                            ⎪             ⎪
          intros a m s c Valid .
                                                            ⎪
                                                            ⎬             ⎪
                                                                          ⎪
                                                                          ⎪
       ...
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
114       apply Strchr_same_block with                    ⎪⎪              ⎪
                                                                          ⎪
                                                          ⎪               ⎪
115          (voidP_s_4_26_alloc_table_at_L := a).
                                                          ⎪
                                                          ⎭               ⎪
                                                                          ⎪
116       tauto .
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
 117    assert (∀ z : int , (0 ≤ z)%Z → P z) as Lemma.
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
118       apply Ind. 1,2: tauto .
                                                                          ⎪
                                                                          ⎪
119     unfold P in Lemma.
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
120     apply Lemma with (a := voidP_str_4_82_alloc_table_at_L).
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
121       unfold Uint64. infix_lseq in h3.
                                                          ⎫               ⎪
                                                                          ⎪
122
                                                               8 lines




          rewrite Uint64. Of_int in h3.
                                                          ⎪               ⎪
                                                                          ⎪
                                                          ⎬               ⎪
                                                                          ⎪
       ...                                                                ⎪
                                                                          ⎪
                                                                          ⎪
                                                                          ⎪
127     unfold Uint64. in_bounds. omega.
                                                           ⎪
                                                           ⎭              ⎪
                                                                          ⎪
128
                                                                          ⎭
        tauto .
129 Qed.
              Fig. 1. Proofs of lemma strchr_skipped. Coq proof on the left. Auto-active proof with lemma function on the right.
form                                                               grouped into axiomatic blocks. Ultimately, instead of
   /@ lemma                                                        choosing between the declaration and the definition points
    @ ensures ∀ L 𝑣; 𝑣1 ≤ 𝑣 < 𝑣2 =⇒ 𝑃 (𝑣);                         to be used for topological ordering, we propose including
    @/                                                             the lemma function definitions (bodies) into the axiomatic
   void gen() {                                                    blocks directly. The ordering then can be retained as in
     /@ loop invariant 𝑣1 ≤ 𝑖 ≤ 𝑣2 ;                               the current implementation. However, this would be a
      @ loop invariant ∀ C 𝑗; 𝑣1 ≤ 𝑗 < 𝑖 =⇒ 𝑃 (𝑗);                 significant change to the ACSL specification.
      @/
     for (C i = v1; i < v2; i++)                                   C. Proof reuse and higher-order logic
       𝑎𝑢𝑥(𝑖);
                                                                  Careful consideration of the resulting auto-active proofs
   }
                                                               from our study reveals that many of them are very
  For logic expressions 𝑙(𝑢) ranging over the C values
                                                               similar to each other and represent instances of some more
𝑣1 ≤ 𝑙(𝑢) < 𝑣2 , where 𝑢 are C expressions, a proxy C
                                                               general proof patterns. In general, it is natural to express
function can be introduced:
                                                               such more general lemmas and their proofs using higher-
                /*@ ensures ∖𝑟𝑒𝑠𝑢𝑙𝑡 ≡ 𝑙(𝑢);                    order logic (HOL). However, the support for higher-order
                   @ assigns ∖𝑛𝑜𝑡ℎ𝑖𝑛𝑔;                         reasoning in SMT-based deductive verification tools such
                   @*/                                         as Jessie or AstraVer is usually very limited due to the
                C 𝑝𝑟𝑜𝑥𝑦(𝑢);                                    inherent incompleteness of decision procedures for HOLs.
                                                               An alternative solution to direct support for HOL would be
Note that 𝑙(𝑢) may contain logic constructs that are thus
                                                               a stratified solution, where the core specification language
encapsulated by the proxy. In general, proxies should
                                                               does not support any HOL constructs, but a separate
be introduced carefully as their post-conditions are not
                                                               higher-level language such as the language of modules does
checked and may introduce inconsistencies, but in some
                                                               provide constructs that can be used to express and prove
cases, the proxy can be given an implementation (definition)
                                                               higher-order propositions. This approach is already used
that satisfies the corresponding specification. In our proofs,
                                                               in Why3ML specification language. Let us illustrate this
we only introduced proxies with definitions.
                                                               approach on two example lemmas from our study:
   Ultimately, the proper support for logic types and
                                                                       logic char * strchr(char * 𝑠, char 𝑐) =
expressions in the ghost code should be added to ACSL
                                                                          *𝑠 ≡ 𝑐 ? 𝑠 :
specification and implemented in Frama-C to fully support
                                                                          *𝑠 ≡ ′ ∖0′ ? (char*)∖𝑛𝑢𝑙𝑙 : 𝑠𝑡𝑟𝑐ℎ𝑟(𝑠 + 1, 𝑐);
auto-active proofs with lemma functions.
                                                                       lemma strchr_skipped :
B. Lemma functions and axiomatics                                         ∀char * 𝑠, 𝑐, size_t 𝑖;
                                                                             valid_str(𝑠) ∧
   Normally, lemmas in ACSL are grouped into axiomatic
                                                                             strchr(𝑠, 𝑐) ̸≡ ∖𝑛𝑢𝑙𝑙 ∧
blocks. However, axiomatic blocks cannot include code.
                                                                             0 ≤ 𝑖 < strchr(𝑠, 𝑐) − 𝑠 =⇒
Therefore, lemma functions cannot be directly grouped
                                                                             𝑠[𝑖] ̸≡ 𝑐;
into axiomatic blocks. Moreover, allowing lemma functions
                                                                       ...
to be declared as lemmas in axiomatic blocks introduces a
                                                                       logic char * strchrnul(char * 𝑠, char 𝑐) =
problem with ordering of proofs. To be well-founded, the
                                                                          *𝑠 ≡ 𝑐 ? 𝑠 :
lemma functions should be split into strongly connected
                                                                          *𝑠 ≡ ′ ∖0′ ? 𝑠 : 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙(𝑠 + 1, 𝑐);
components and topologically ordered. However, unlike
                                                                       lemma strchrnul_skipped :
code functions that can only be called explicitly, lemmas
                                                                          ∀char * 𝑠, 𝑐, size_t 𝑖;
can be instantiated implicitly, provided they are preset in
                                                                             valid_str(𝑠) ∧
the proof context. When each lemma function has just a
                                                                             0 ≤ 𝑖 < strchrnul(𝑠, 𝑐) − 𝑠 =⇒
single definition, the definition order of lemma functions
                                                                             𝑠[𝑖] ̸≡ 𝑐;
can serve as their required topological order, with an only
                                                               Currently, the lemmas have to be proved as two separate
additional restriction that mutually recursive functions
                                                               lemma functions. Though there is a single generic function
should be somehow declared simultaneously. However, when
                                                               that suits both cases, its definition makes use of higher-
lemma functions are allowed to have separate declarations
                                                               order features :
and definitions, the ordering of lemma functions becomes
                                                                 logic char * strchrcomb(boolean 𝑐𝑜𝑛𝑑(char * 𝑠, char 𝑐),
generally unspecified. In the current implementation, the
lemma functions are allowed to have separate declarations,                                       char * 𝑑𝑓 𝑡(char * 𝑠),
but they are later grouped into strongly connected com-                                          char * 𝑠, char 𝑐) =
                                                                                          ′    ′
ponents, and the definition of the first function in the         𝑐𝑜𝑛𝑑(𝑠,  𝑐) ? 𝑠   : *𝑠 ≡   ∖0   ? 𝑑𝑓 𝑡(𝑠, 𝑐) : 𝑠𝑡𝑟𝑐ℎ𝑟𝑐𝑜𝑚𝑏(𝑠 + 1, 𝑐);
component is then used for topological ordering. This Within the stratified approach, this function should be
essentially simulates simultaneous definitions. However, this placed in a separate module alongside the functions cor-
approach is completely ignorant of the lemma declarations responding to its parameters, auxiliary definitions, and
appropriate lemmas:                                            [5] F. Rothenberger, “Integration and analysis of alternative SMT
 predicate 𝑐𝑜𝑛𝑑(char * 𝑠, char 𝑐) reads * 𝑠;                       solvers for software verification,” Master’s thesis, ETH-Zürich,
                                                                   2016.
 logic char * 𝑑𝑓 𝑡(char * 𝑠);                                  [6] G. Petiot, N. Kosmatov, B. Botella, A. Giorgetti, and
 predicate 𝑑𝑓 𝑡_𝑠𝑎𝑚𝑒 = ∀char * 𝑠; 𝑑𝑓 𝑡(𝑠) ≡ 𝑠;                     J. Julliand, “How testing helps to diagnose proof failures,”
 predicate 𝑑𝑓 𝑡_𝑛𝑢𝑙𝑙 = ∀char * 𝑠; 𝑑𝑓 𝑡(𝑠) ≡ ∖𝑛𝑢𝑙𝑙;                 Formal Aspects of Computing, Jun 2018. [Online]. Available:
                                                                   https://doi.org/10.1007/s00165-018-0456-4
 logic char * 𝑠𝑡𝑟𝑐ℎ𝑟𝑐𝑜𝑚𝑏(char * 𝑠, char 𝑐) =                   [7] M. Hentschel, R. Bubel, and R. Hähnle, “The symbolic execution
    𝑐𝑜𝑛𝑑(𝑠, 𝑐) ? 𝑠 :                                               debugger (SED): a platform for interactive symbolic execution,
    *𝑠 ≡ ′ ∖0′ ? 𝑑𝑓 𝑡(𝑠) :                                         debugging, verification and more,” International Journal on
                                                                   Software Tools for Technology Transfer, 2018. [Online]. Available:
       𝑠𝑡𝑟𝑐ℎ𝑟𝑐𝑜𝑚𝑏(𝑠 + 1, 𝑐);                                       https://doi.org/10.1007/s10009-018-0490-9
 lemma 𝑠𝑡𝑟𝑐ℎ𝑟𝑐𝑜𝑚𝑏_𝑠𝑘𝑖𝑝𝑝𝑒𝑑 :                                    [8] W. Reif, “The KIV-approach to software verification,” in KO-
    ∀char * 𝑠, 𝑐, size_t 𝑖;                                        RSO: Methods, Languages, and Tools for the Construction of
                                                                   Correct Software. Springer, 1995, pp. 339–368.
       𝑣𝑎𝑙𝑖𝑑_𝑠𝑡𝑟(𝑠) ∧                                          [9] C. Calcagno, D. Distefano, J. Dubreil, D. Gabi, P. Hooimeijer,
       (𝑑𝑓 𝑡_𝑠𝑎𝑚𝑒 ∨ 𝑑𝑓 𝑡_𝑛𝑢𝑙𝑙 ∧ 𝑠𝑡𝑟𝑐ℎ𝑟𝑐𝑜𝑚𝑏(𝑠, 𝑐) ̸≡ ∖𝑛𝑢𝑙𝑙) ∧       M. Luca, P. O’Hearn, I. Papakonstantinou, J. Purbrick, and
       0 ≤ 𝑖 < strchrcomb(𝑠, 𝑐) − 𝑠 =⇒                             D. Rodriguez, “Moving fast with software verification,” in NASA
                                                                   Formal Methods, K. Havelund, G. Holzmann, and R. Joshi, Eds.
       !𝑐𝑜𝑛𝑑(𝑠 + 𝑖, 𝑐);                                            Cham: Springer International Publishing, 2015, pp. 3–11.
Then the lemmas can be proved in the general case as usual, [10] A. Chudnov, N. Collins, B. Cook, J. Dodds, B. Huffman,
e. g., by using lemma-functions. The resulting module can          C. MacCárthaigh, S. Magill, E. Mertens, E. Mullen, S. Tasiran,
                                                                   A. Tomb, and E. Westbrook, “Continuous formal verification
be instantiated by providing concrete definitions for logic        of Amazon s2n,” in Computer Aided Verification, H. Chockler
functions 𝑐𝑜𝑛𝑑 and 𝑑𝑓 𝑡 to obtain both logic functions 𝑠𝑡𝑟𝑐ℎ𝑟      and G. Weissenbacher, Eds.        Cham: Springer International
and 𝑠𝑡𝑟𝑐ℎ𝑟𝑛𝑢𝑙. Upon instantiation, their corresponding             Publishing, 2018, pp. 430–446.
                                                              [11] P. W. O’Hearn, “Continuous reasoning: Scaling the impact of
lemmas do not have to be proven, and they can be safely            formal methods,” in Proceedings of the 33rd Annual ACM/IEEE
instantiated directly into axioms.                                 Symposium on Logic in Computer Science, ser. LICS ’18. New
                                                                              York, NY, USA: ACM, 2018, pp. 13–25. [Online]. Available:
                       VI. Conclusion                                         http://doi.acm.org/10.1145/3209108.3209109
                                                                         [12] C. Dross and Y. Moy, “Auto-active proof of red-black trees in
                                                                              SPARK,” in NASA Formal Methods, C. Barrett, M. Davies, and
   In this paper we propose the implementation of auto-                       T. Kahsai, Eds. Cham: Springer International Publishing, 2017,
active proofs technique in the Frama-C framework and                          pp. 68–83.
AstraVer plugin, evaluate our implementation on VerKer                   [13] J.-C. Filliâtre and A. Paskevich, “Why3 — where programs
                                                                              meet provers,” in Proceedings of the 22nd European Symposium
project specifications by proving all string-related lemmas,                  on Programming, ser. Lecture Notes in Computer Science,
and demonstrate the benefits of the approach by comparing                     M. Felleisen and P. Gardner, Eds., vol. 7792. Springer, Mar.
it with manual lemma proofs in Coq.                                           2013, pp. 125–128.
   The results of the work are publicly available. The                   [14] P. Baudin, P. Cuoq, J.-C. Filliâtre, C. Marché, B. Monate,
                                                                              Y. Moy, and V. Prevosto, “ACSL: ANSI/ISO C Specification
source code with specifications and verification protocols                    Language,” CEA LIST and INRIA, Tech. Rep. 1.12, March 2017.
are available as a part of the VerKer project. The proofs                [15] D. Efremov, M. Mandrykin, and A. Khoroshilov, “Deductive
are easy reproducible since there is a configuration of a                     Verification of Unmodified Linux Kernel Library Functions,” in
                                                                              Leveraging Applications of Formal Methods, Verification and
continuous integration system. The modified toolset is                        Validation. Verification, T. Margaria and B. Steffen, Eds. Cham:
available on the AstraVer project page.                                       Springer International Publishing, 2018, pp. 216–234.
   The obtained results show the approach is very promising              [16] J. Hatcliff, G. T. Leavens, K. R. M. Leino, P. Müller, and
                                                                              M. Parkinson, “Behavioral interface specification languages,”
and should be adopted in the mainline of AstraVer toolset.                    ACM Comput. Surv., vol. 44, no. 3, pp. 16:1–16:58, Jun. 2012.
Auto-active verification in Frama-C ease the work of a ver-                   [Online]. Available: http://doi.acm.org/10.1145/2187671.2187678
ification engineer, make specifications more maintainable                [17] J.-C. Filliâtre, “Verifying two lines of C with Why3: an
                                                                              exercise in program verification,” in Proceedings of the 4th
and potentially can lower the cost of deductive verification.                 International Conference on Verified Software: Theories,
                                                                              Tools, Experiments, ser. VSTTE’12.           Berlin, Heidelberg:
                          References                                          Springer-Verlag, 2012, pp. 83–97. [Online]. Available: http:
                                                                              //dx.doi.org/10.1007/978-3-642-27705-4_8
 [1] F. Kirchner, N. Kosmatov, V. Prevosto, J. Signoles, and             [18] A. Tafat and C. Marché, “Binary heaps formally verified in
     B. Yakobowski, “Frama-C: A software analysis perspective,”               Why3,” INRIA, Research Report 7780, Oct. 2011, http://hal.
     Formal Aspects of Computing, vol. 27, no. 3, pp. 573–609, May            inria.fr/inria-00636083/en/.
     2015. [Online]. Available: https://doi.org/10.1007/s00165-014-      [19] A. Blanchard, N. Kosmatov, and F. Loulergue, “Ghosts for
     0326-7                                                                   Lists: A Critical Module of Contiki Verified in Frama-C,”
[2] B. Jacobs, J. Smans, P. Philippaerts, F. Vogels, W. Penninckx,            in Tenth NASA Formal Methods Symposium - NFM 2018,
     and F. Piessens, “VeriFast: A powerful, sound, predictable, fast         Newport News, United States, Apr. 2018. [Online]. Available:
     verifier for C and Java,” in NASA Formal Methods Symposium.              https://hal.inria.fr/hal-01720401
     Springer, 2011, pp. 41–55.                                          [20] J. Burghardt, R. Clausecker, J. Gerlach, and H. Pohl, “ACSL
[3] K. R. M. Leino, “Dafny: An automatic program verifier for                 By Example,” Fraunhofer Institute for Open Communication
     functional correctness,” in International Conference on Logic for        Systems, Tech. Rep., 2017.
     Programming Artificial Intelligence and Reasoning. Springer,        [21] K. R. M. Leino and M. Moskal, “Usable auto-active verification,”
     2010, pp. 348–370.                                                       2010.
[4] B. Carré and J. Garnsworthy, “SPARK — an annotated ada
     subset for safety-critical programming,” in Proceedings of the
     conference on TRI-ADA’90. ACM, 1990, pp. 392–402.
