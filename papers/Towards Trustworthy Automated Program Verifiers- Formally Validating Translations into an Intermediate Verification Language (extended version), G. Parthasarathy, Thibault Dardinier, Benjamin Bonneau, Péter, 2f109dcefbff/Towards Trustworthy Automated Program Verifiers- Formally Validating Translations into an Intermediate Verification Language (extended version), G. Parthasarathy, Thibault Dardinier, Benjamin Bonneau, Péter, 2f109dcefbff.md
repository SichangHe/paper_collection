                                        Towards Trustworthy Automated Program Verifiers:
                                        Formally Validating Translations into an Intermediate
                                        Verification Language (extended version)
arXiv:2404.03614v2 [cs.PL] 9 May 2024




                                        GAURAV PARTHASARATHY, Department of Computer Science, ETH Zurich, Switzerland
                                        THIBAULT DARDINIER, Department of Computer Science, ETH Zurich, Switzerland
                                        BENJAMIN BONNEAU, Université Grenoble Alpes - CNRS - Grenoble INP - VERIMAG, France
                                        PETER MÜLLER, Department of Computer Science, ETH Zurich, Switzerland
                                        ALEXANDER J. SUMMERS, University of British Columbia, Canada
                                        Automated program veriﬁers are typically implemented using an intermediate veriﬁcation language (IVL),
                                        such as Boogie or Why3. A veriﬁer front-end translates the input program and speciﬁcation into an IVL
                                        program, while the back-end generates proof obligations for the IVL program and employs an SMT solver
                                        to discharge them. Soundness of such veriﬁers therefore requires that the front-end translation faithfully
                                        captures the semantics of the input program and speciﬁcation in the IVL program, and that the back-end
                                        reports success only if the IVL program is actually correct. For a veriﬁcation tool to be trustworthy, these
                                        soundness conditions must be satisﬁed by its actual implementation, not just the program logic it uses.
                                           In this paper, we present a novel validation methodology that, given a formal semantics for the input
                                        language and IVL, provides formal soundness guarantees for front-end implementations. For each run of
                                        the veriﬁer, we automatically generate a proof in Isabelle showing that the correctness of the produced IVL
                                        program implies the correctness of the input program. This proof can be checked independently from the
                                        veriﬁer, in Isabelle, and can be combined with existing work on validating back-ends to obtain an end-to-end
                                        soundness result. Our methodology based on forward simulation employs several modularisation strategies
                                        to handle the large semantic gap between the input language and the IVL, as well as the intricacies of prac-
                                        tical, optimised translations. We present our methodology for the widely-used Viper and Boogie languages.
                                        Our evaluation shows that it is eﬀective in validating the translations performed by the existing Viper imple-
                                        mentation.
                                        CCS Concepts: • Software and its engineering → Formal software veriﬁcation; Semantics; • Theory of
                                        computation → Program veriﬁcation.
                                        Additional Key Words and Phrases: Software Veriﬁcation, Intermediate Veriﬁcation Languages, Formal Se-
                                        mantics, Proof Certiﬁcation

                                        1 INTRODUCTION
                                        Program veriﬁers are tools that try to automatically establish the correctness of an input program
                                        with respect to a speciﬁcation. A standard approach for achieving automation is to reduce the
                                        input program and speciﬁcation to a set of ﬁrst-order formulas whose validity implies the correct-
                                        ness of the input program; the validity of formulas is automatically checked using an SMT solver.
                                        Instead of directly producing logical formulas, many program veriﬁers are translational veriﬁers:
                                        they translate an input program and speciﬁcation into a program in an intermediate veriﬁcation
                                        language (IVL); we call this a front-end translation. An IVL comes with its own back-end veriﬁer that
                                        ultimately reduces IVL programs to logical formulas. This translational approach via an IVL allows
                                        for the reuse of the IVL’s back-end technology across multiple front-end veriﬁers, and makes for a

                                        Authors’ addresses: Gaurav Parthasarathy, Department of Computer Science, ETH Zurich, Zurich, Switzerland, gaurav.
                                        parthasarathy@inf.ethz.ch; Thibault Dardinier, Department of Computer Science, ETH Zurich, Zurich, Switzerland,
                                        thibault.dardinier@inf.ethz.ch; Benjamin Bonneau, Université Grenoble Alpes - CNRS - Grenoble INP - VERIMAG, Greno-
                                        ble, France, Benjamin.Bonneau@univ-grenoble-alpes.fr; Peter Müller, Department of Computer Science, ETH Zurich,
                                        Zurich, Switzerland, peter.mueller@inf.ethz.ch; Alexander J. Summers, University of British Columbia, Vancouver, Canada,
                                        alex.summers@ubc.ca.
208:2         Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


more understandable target representation than direct mappings to logical formulas, simplifying
the development of state-of-the-art program veriﬁers.
   A very wide variety of practical program veriﬁers are translational veriﬁers; e.g. Corral [26],
Dafny [29], SMACK [7], SYMDIFF [25], and Viper [34] target the imperative Boogie IVL [28],
while Creusot [10] and Frama-C [23] translate to the functional Why3 IVL [17]. Multiple layers of
front-end translations and IVLs can also be composed (e.g. Prusti [2] builds on Viper as an IVL).
   To ensure that successful veriﬁcation indeed implies that the input program satisﬁes its spec-
iﬁcation, any translational veriﬁer must meet two soundness conditions: (1) Front-end soundness:
the translation into the IVL is faithful, i.e. correctness of the produced IVL program implies cor-
rectness of the input program, and (2) IVL back-end soundness: if the back-end IVL veriﬁer reports
success, the IVL program is correct. Trustworthiness of program veriﬁers requires formal guaran-
tees for both soundness conditions. It is not suﬃcient to prove soundness of the program logics
they employ in principle: automated veriﬁers are complex systems, and it is essential that formal
guarantees also cover their actual implementations, where soundness bugs can and do arise.
   Existing work on ensuring front-end soundness is based on idealised implementations that are
formalised on paper or in an interactive theorem prover. In practice, practical front-end transla-
tions are implemented in eﬃcient mainstream programming languages, use diverse libraries and
programming paradigms, and include subtle optimisations omitted from idealised implementa-
tions; there is a very large gap between the translations proved correct and the actual translations
used in practice. In this paper, we bridge this gap for the ﬁrst time, developing an approach to
formally validate the front-end soundness of translations used in existing, practical veriﬁer im-
plementations. IVL back-end veriﬁer soundness, which includes the soundness of the underlying
SMT solver, is a better-studied and orthogonal concern; our results can be combined with work in
that area to obtain end-to-end guarantees for an entire veriﬁcation toolchain [5, 16, 18, 19, 38].
   Proving front-end soundness once and for all for a realistic veriﬁer implementation is practically
infeasible, since such implementations are large (e.g. 17.2 KLOC and 8.5 KLOC for the Dafny-to-
Boogie and Viper-to-Boogie front-ends, respectively) and are typically written in languages that
lack a full formalisation (C# and Scala, in the examples above). Instead, we develop a translation
validation approach that, given a formal semantics for the input language and IVL, automatically
generates a formal proof on every run of the veriﬁer via an instrumentation of the existing imple-
mentation. Our proofs are expressed in the Isabelle theorem prover [35], and thus can be checked
independently, eﬀectively removing the (substantial) front-end translation from the trusted code
base of the veriﬁer.

   Challenges. Formally validating front-end translations is challenging for three main reasons:
   1. Semantic gap: There is a large semantic gap between a front-end language and an IVL, which
concerns the state model (e.g. neither Boogie nor Why3 have a heap, but most front-end languages
do), the execution model (e.g. Viper heap accesses are partial operations that must be guarded by se-
mantic conditions ultimately checked by veriﬁcation, while Boogie and Why3 use syntactic checks
to guard state accesses such as disallowing global variables in Boogie axioms and restricting alias-
ing between mutable variables in Why3), and the program logics used to reason about programs
(e.g. front-ends use complex logics, such as dynamic frames [22] in Dafny, a ﬂavour of separation
logic [36, 40] in Viper, and prophetic reasoning in Creusot [10], whereas Boogie and Why3 do
not have built-in support for such logics). To bridge the semantic gap, front-ends translate input
programs into a complex combination of low-level operations and background logical axiomati-
sations of input language concepts; validation needs to precisely account for the combination of
these ingredients, while allowing the separation of translation aspects for the sake of modularity
and maintainability.
Formally Validating Translations into an Intermediate Verification Language                      208:3


   2. Diverse translations: Practical front-end translations are diverse in the sense that they use
multiple alternative translations for the same feature, e.g. more eﬃcient translations that are sound
only in certain cases. These translations also evolve frequently over time, as new techniques and
features are developed or optimised; ideally a formal approach to validation should provide means
of minimising the impact of the exchange of one translation for another.
   3. Non-locality: The soundness of the translation of a fragment of the input program may depend
on several checks that are performed at diﬀerent places in the IVL program. For instance, the
translation of a procedure call might be sound only because well-formedness of the procedure
speciﬁcation has been checked elsewhere in the generated IVL code. Such non-local checks are
commonly used to speed up veriﬁcation, for instance, to check well-formedness conditions once
and for all rather than each time a speciﬁcation is used. However, they complicate the soundness
argument, which needs to somehow track the dependencies on properties checked elsewhere.

   This paper. We present the ﬁrst approach for enabling automatic formal validation for existing
implementations of the front-end translations employed in many practical program veriﬁers. This
validation guarantees front-end soundness and, thus, makes automated program veriﬁers substan-
tially more trustworthy.
   The core of our approach is a general methodology for generating forward simulations [32] be-
tween the statements of the input and the IVL program in a modular way. Our methodology pro-
vides solutions to the three challenges above. It (1) bridges the semantic gap with a novel approach
by which the simulation proof is split into smaller simulations, (2) supports diverse translations
by expressing simulations abstractly, and (3) handles non-locality by systematically and formally
tracking dependencies during a simulation proof.
   For concreteness, we present our methodology for the translation from a core fragment of Viper
to Boogie, as implemented in an existing and actively-used veriﬁcation tool [12]. This translation
is signiﬁcant because it exhibits all of the challenges discussed above and because both Viper and
Boogie are widely used. For instance, Viper is used in Gobra (Go) [46], Prusti (Rust) [2], Nagini
(Python) [14], VerCors (Java) [4], and Gradual C0 [13]. The soundness of each of these tools relies
on the Viper veriﬁers being sound. Note that these tools use Viper as an IVL, but for the purpose of
this paper, we will treat it as a front-end language that is translated to Boogie. While our method-
ology is phrased in terms of Viper and Boogie, we have designed our approach, which solves the
key challenges above, to generalise to other front-end translations (e.g. the Dafny-to-Boogie trans-
lation).

  Contributions. We make the following technical contributions:
      • We develop a general methodology for the automatic validation of front-end translations
        based on forward simulation proofs. We present this methodology for the translation from
        Viper to Boogie. As a foundation for the proofs, we formalise a semantics for a core subset
        of Viper in Isabelle and connect this with an existing Isabelle formalisation for Boogie [38].
      • We instrument the existing Viper-to-Boogie implementation such that, for a subset of Viper,
        it automatically generates an Isabelle proof justifying the soundness of the translation.
        These generated proofs can be checked independently in Isabelle, which ensures front-end
        soundness of the Viper veriﬁer.
      • Our evaluation on a diverse set of Viper programs demonstrates our approach’s eﬀective-
        ness: we were able to generate proofs and check them in Isabelle fully automatically in all
        cases.
      • As part of justifying the axioms used in Boogie programs, we provide the ﬁrst approach to
        formally deal with a restricted version of Boogie’s (impredicatively-)polymorphic maps [30].
208:4             Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


    VExpr ∋ 𝑒 ::= 𝑥 | lit | 𝑒.𝑓 | 𝑒 bop 𝑒 | uop(𝑒)      VAssert ∋ 𝐴 ::= 𝑒 | acc (𝑒.𝑓 , 𝑒) | 𝐴 ∗ 𝐴 | 𝑒 ⇒ 𝐴 | 𝑒 ? 𝐴 : 𝐴
    VStmt ∋ 𝑠 ::= 𝑥 := 𝑒 | 𝑒.𝑓 := 𝑣 | 𝑦® := 𝑚 (𝑥)     ® | var 𝑥 : 𝜏 | inhale 𝐴 | exhale 𝐴 | assert 𝐴 |
                                               ® | 𝑚 (𝑥)
                    𝑠; 𝑠 | if (𝑒) {𝑠 } else {𝑠 }

     BExpr ∋ 𝑒𝑏 ::= 𝑥 | lit𝑏 | 𝑒𝑏 bop 𝑒𝑏 | uop(𝑒𝑏 ) | 𝑓 [®     𝑒𝑏 ) | ∀𝑥 : 𝜏𝑏 . 𝑒𝑏 | ∃𝑥 : 𝜏𝑏 . 𝑒𝑏 | ∀ty 𝑡 . 𝑒𝑏 | ∃ty 𝑡 . 𝑒𝑏
                                                         𝜏𝑏 ] (®
     BSimpleCmd ∋ 𝑐 ::= assume 𝑒 | assert 𝑒 | 𝑥 := 𝑒 | havoc 𝑥
                        𝑏                 𝑏              𝑏          𝑏                 BStmtBlock ∋ 𝑏 ::= →𝑏      𝑐− ; if
                                                                                                                  𝑏   𝑏
                                                                                                        →
                                                                                                        −
     BIfOpt ∋ if𝑏 ::= if (𝑒𝑏 ) {𝑠𝑏 } else {𝑠𝑏 } | if (∗) {𝑠𝑏 } else {𝑠𝑏 } | 𝜖            BStmt ∋ 𝑠𝑏 ::= 𝑏𝑏


Fig. 1. The syntax of our formalised Viper subset (top, blue keywords) and corresponding Boogie subset
(bottom, with subscript 𝑏, orange keywords) without top-level declarations. 𝜏 (𝜏𝑏 ), bop, and uop denote types,
binary and unary operations, respectively.



  Outline. Sec. 2 provides the necessary background on Viper and Boogie. Sec. 3 introduces our
forward simulation methodology for relating Viper and Boogie statements. Sec. 4 presents how
we formally validate the existing Viper-to-Boogie implementation using our forward simulation
methodology. Sec. 5 evaluates the proofs generated by our instrumentation. Sec. 6 presents related
work and Sec. 7 concludes. Our publicly-available artifact [37] contains the Isabelle formalisation
for Sec. 2, Sec. 3, and Sec. 4, our proof-producing Viper-to-Boogie implementation, and the exam-
ples used for the evaluation. Further details are available in the appendix.

2    VIPER AND BOOGIE: BACKGROUND AND SEMANTICS
In this section, we present the necessary background on the Viper and Boogie languages. We
introduce our supported Viper subset and the corresponding Boogie subset targeted by the pre-
existing Viper-to-Boogie implementation (Sec. 2.1), give an overview of the semantics of Boogie
(Sec. 2.2) and Viper (Sec. 2.3), and ﬁnally show an example of the translation used by the Viper-to-
Boogie implementation (Sec. 2.4).

2.1 The Viper and Boogie Languages
Viper programs in the subset considered here consist of a set of top-level declarations of ﬁelds
(reference-ﬁeld pairs are used to access the heap) and methods. Boogie programs consist of a set of
top-level declarations of global variables, constants, uninterpreted (polymorphic) functions, type
constructors, axioms (which constrain the constants and functions), and procedures. Both lan-
guages are imperative and separate statements from expressions (whose evaluation have no side-
eﬀects). Viper additionally has separate assertions. The body of each Viper method and Boogie
procedure is a statement. Viper methods have pre- and post-conditions (assertions); method calls
are veriﬁed modularly against these assertions.1 In Viper, scoped variables can be declared within
statements; Boogie procedures declare all variables upfront. Our supported Viper and Boogie state-
ments, assertions, and expressions are shown in Fig. 1. Both languages have the same control ﬂow
elements and have some built-in types in common (e.g. Booleans and integers). Viper additionally
provides a single reference type, and supports reading from and writing to heap locations via a
ﬁeld access e.f, where e is a reference expression and f a ﬁeld.


1 Boogie supports pre-/post-conditions and procedure calls, but they are not used by the Viper-to-Boogie implementation.
Formally Validating Translations into an Intermediate Verification Language                                          208:5


   Our validation generates proofs that connect the abstract syntax tree (AST) of a Viper program
(as represented by the Viper veriﬁer) with the AST of the corresponding Boogie program (as rep-
resented by the Boogie veriﬁer).2 Proof generation is complicated by the fact that the Viper and
Boogie ASTs are structured diﬀerently. As shown in Fig. 1, the Viper AST uses a standard sequential
composition 𝑠 1 ; 𝑠 2 , whereas a Boogie statement is given by a list of statement blocks. Each statement
block →𝑐−𝑏 ; if𝑏 consists of a list of simple commands (i.e. no control ﬂow), followed by either an if-
statement or an empty statement (𝜖).
   As is typical for veriﬁers for higher-level languages, Viper’s veriﬁcation methodology employs
a custom advanced program logic, in this case based on a ﬂavour of separation logic (SL) called
implicit dynamic frames (IDF) [36, 40] which reasons about the heap via permissions. Viper’s asser-
tions include the accessibility predicate acc(e.f,p), which represents a resource (a logical notion
which can be neither freely fabricated nor duplicated): the fractional (p) amount of permission
to access heap location e.f.3 Fractional permission amounts [6] range between 0 and 1; nonzero
permission is required to read heap locations and full (1) permission is required to write to heap
locations. 𝐴 ∗ 𝐵 expresses the separating conjunction from SL, which speciﬁes that the permissions
in 𝐴 and 𝐵 must sum up to an amount currently held. One diﬀerence between IDF and SL is that
IDF (and thus, Viper) supports general heap-dependent expressions such as x.val = 5 or x.f.f,
whose evaluation is partial (only allowed with suitable permissions); this necessitates a notion of
well-deﬁnedness checks on expressions (see Sec. 2.3). Boogie does not provide built-in heap rea-
soning, and uses a much simpler program logic: its assertions are (total) formulas in ﬁrst-order
logic.
   The presence of a heap in Viper also results in a very diﬀerent state model. A Viper state con-
sists of a variable store, a heap (mapping heap locations to current values) and a permission mask
(mapping heap locations to current permission amounts); a Boogie state is simply a variable store.
   The main Viper features not included in our subset are loops, more-complex resource asser-
tions (predicates, magic wands, iterated separating conjunctions), heap-dependent functions, and
domains. Adding support for loops is straightforward: their semantics can be desugared via their
invariant, in a pattern similar to method calls that we already support. For other features more
work would be required, but we are conﬁdent that these extensions would ﬁt within our general
methodology.

2.2 Boogie Semantics
We extend our existing operational Boogie semantics formalised in Isabelle [38] to support the
statements in Fig. 1, and reuse many components including the state model and the semantics of
simple commands. The semantics of Boogie statements is expressed via program executions. A
ﬁnite program execution has one of three outcomes: (1) it fails, because an assert 𝑒 command is
reached in a state that does not satisfy the Boolean expression 𝑒, (2) it stops, because an assume 𝑒
command is reached in a state that does not satisfy the Boolean expression 𝑒, or (3) it succeeds,
because neither of the ﬁrst two situations occur. The three outcomes are represented formally
via: (1) a failure outcome F, (2) a magic outcome M for when the execution stops, and (3) a nor-
mal outcome N(𝜎𝑏 ) in all other cases, where 𝜎𝑏 is the resulting Boogie state, which is given by a
mapping from variables to values. Assignments and havoc commands always succeed; havoc 𝑥
nondeterministically assigns a value of 𝑥’s declared type to 𝑥.

2 The Viper-to-Boogie implementation passes the Boogie program to the Boogie veriﬁer via a text ﬁle. Targeting the Boogie

AST as represented by the Boogie veriﬁer in the proof avoids the need to trust the Boogie parser, and also generalises to
veriﬁer implementations that directly target the Boogie veriﬁer’s AST such as Dafny.
3 For readers familiar with separation logics, this is analogous to a fractional points-to assertion in a separation logic.
208:6           Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


   Formally, executions of Boogie statements are expressed via a small-step semantics. The judge-
ment Γ𝑏 ⊢ (𝛾, N(𝜎𝑏 )) →∗b (𝛾 ′ , 𝑟𝑏 ) expresses a ﬁnite execution w.r.t. Boogie context Γ𝑏 that takes 0
or more steps starting from the program point 𝛾 and Boogie state 𝜎𝑏 , and ending in the program
point 𝛾 ′ and outcome 𝑟𝑏 . A Boogie context includes the interpretation of uninterpreted types and
functions, and the types of declared variables. A program point is given by a pair of the currently
active statement block 𝑏 and the continuation representing the statement to be executed after 𝑏.
A continuation is either the empty continuation (i.e. nothing to execute) or a sequential continua-
tion (i.e. a statement block followed by a continuation). A continuation-based small-step semantics
avoids the need for local search rules commonly required in a small-step semantics [1].

2.3     Viper Semantics
To our knowledge, there is no mechanised semantics for any fragment of the Viper language;
we outline the main points of the one we have formalised here. We give a big-step operational
semantics to Viper statements via program executions again with three possible outcomes for ﬁnite
executions: failure F, magic M, and normal outcomes N(𝜎 𝑣 ) where 𝜎 𝑣 is a Viper state. A Viper state
𝜎 𝑣 comprises a local variable mapping st(𝜎 𝑣 ), a heap ℎ(𝜎 𝑣 ) (a total mapping from heap locations to
values), and a permission mask 𝜋 (𝜎 𝑣 ) (a total mapping from heap locations to permission amounts).
The judgement Γ𝑣 ⊢ h𝑠, 𝜎 𝑣 i →v 𝑟 𝑣 holds if in the Viper context Γ𝑣 (ﬁxing the declarations of methods,
ﬁelds and local variables) the execution of statement 𝑠 in the state 𝜎 𝑣 terminates with outcome 𝑟 𝑣 .
Determining the outcome of a Viper execution is more involved than for Boogie as we will see
below for the inhale and exhale operations. Our semantics takes care that all Viper states are
consistent, i.e. have consistent permission masks (mapping each location to values between 0 and
1); executions that would produce inconsistent states in this sense are pruned by going to M.
    Formalising expression evaluation requires care for Viper, since, in a given state, not even all
type-correct expressions are well-deﬁned: in our subset this can be either because of (1) division by
zero, or (2) dereferencing a heap location for which no permission is held (subsuming null derefer-
ences). In our semantics, evaluating an ill-deﬁned expression causes execution to fail (in contrast
to Boogie, where expression evaluation cannot fail). Our judgement h𝑒, 𝜎 𝑣 i ⇓ V(𝑣) expresses that
expression 𝑒 evaluates to a value 𝑣 in state 𝜎 𝑣 (in particular, 𝑒 is well-deﬁned in 𝜎 𝑣 ) and h𝑒, 𝜎 𝑣 i ⇓
expresses that 𝑒 is ill-deﬁned in 𝜎 𝑣 .
    Viper uses two main primitives to encode separation logic reasoning: (1) inhale 𝐴 adds the
permissions speciﬁed by assertion 𝐴 to the state, and stops any execution where either a logi-
cal constraint in 𝐴 does not hold (these are assumed) or the added permissions would yield an
inconsistent state. (2) exhale 𝐴 removes the permissions speciﬁed by 𝐴, and fails if either insuﬃ-
cient permissions are held or if a constraint in 𝐴 does not hold; for any heap locations to which all
permission was removed, an exhale also non-deterministically assigns arbitrary values.4 This non-
deterministic assignment reﬂects the fact that, while our Viper states employ total heaps (typical
for IDF [36]), the values stored in heap locations without permission should be unconstrained.
    inhale and exhale operations are typically used in Viper to encode external or more-complex
operations [34]. For instance, a Viper method call is expressed by exhaling the precondition and
then inhaling the postcondition of the callee; the nondeterministic assignments made by the exhale
model possible side eﬀects of the call. We present here some of the key rules for exhale, which
will be used later in this paper. Additional rules for inhale are presented in the appendix (App. A);
the complete rules are included in our Isabelle formalisation.


4 For separation-logic-versed readers, the Hoare triples {𝑅 } inhale 𝐴 {𝑅 ∗ 𝐴} and {𝑅 ∗ 𝐴} exhale 𝐴 {𝑅 } reﬂect this

behavior (assuming the expressions in 𝐴 and 𝑅 are well-deﬁned).
Formally Validating Translations into an Intermediate Verification Language                                                 208:7


      𝜎 𝑣 ⊢ h𝐴, 𝜎 𝑣 i →rc N(𝜎 𝑣′ )                                     𝜎 𝑣 ⊢ h𝐴, 𝜎 𝑣 i →rc F
         nonDet(𝜎 𝑣 , 𝜎 𝑣′ , 𝜎 𝑣′′ )                                                                 (exh-fail)
                                             (exh-succ)           Γ𝑣 ⊢ hexhale 𝐴, 𝜎 𝑣 i →v F
 Γ𝑣 ⊢ hexhale 𝐴, 𝜎 𝑣 i →v N(𝜎 𝑣′′ )

  𝜎 𝑣0 ⊢ h𝐴, 𝜎 𝑣 i →rc N(𝜎 𝑣′ )                               h𝑒, 𝜎 𝑣0 i ⇓ V(𝑟 ) h𝑒𝑝 , 𝜎 𝑣0 i ⇓ V(𝑝)
      𝜎 𝑣0 ⊢ h𝐵, 𝜎 𝑣′ i →rc 𝑟 𝑣                      𝑟 𝑣 = if exhAccSucc(𝑟 , 𝑝, 𝜎 𝑣 ) then N(𝜎 𝑣𝑅 ) else F
                                     (rc-sep)                                                                      (rc-acc)
   𝜎 𝑣0 ⊢ h𝐴 ∗ 𝐵, 𝜎 𝑣 i →rc 𝑟 𝑣                                𝜎 𝑣0 ⊢ hacc (𝑒.𝑓 , 𝑒𝑝 ), 𝜎 𝑣 i →rc 𝑟 𝑣

                                 st(𝜎 𝑣′′ ) = st(𝜎 𝑣′ ) ∧ 𝜋 (𝜎 𝑣′′ ) = 𝜋 (𝜎 𝑣′ ) ∧
 nonDet(𝜎 𝑣 , 𝜎 𝑣′ , 𝜎 𝑣′′ ) ,
                                 ∀𝑙 . (𝜋 (𝜎 𝑣 ) (𝑙) = 0 ∨ 𝜋 (𝜎 𝑣′ ) (𝑙) > 0) ⇒ ℎ(𝜎 𝑣′′ ) (𝑙) = ℎ(𝜎 𝑣′ ) (𝑙)
 exhAccSucc(𝑟 , 𝑝, 𝜎 𝑣 ) , 𝑝 ≥ 0 ∧ (𝑟 = null ? 𝑝 = 0 : 𝜋 (𝜎 𝑣 ) (𝑟 .𝑓 ) ≥ 𝑝)                  𝜎 𝑣𝑅 , rem(𝜎 𝑣 , 𝑟 , 𝑓 , 𝑝)

Fig. 2. A subset of the rules for the formal semantics of exhale. rem(𝜎𝑣 , 𝑟, 𝑓 , 𝑝) is the state 𝜎𝑣 where permis-
sion 𝑝 is removed from 𝑟 .𝑓 .


   An exhale 𝐴 must cause the loss of heap value information (via non-deterministic assignments)
in general, but also needs to check that logical constraints were true when the exhale started. Our
semantics for exhale 𝐴 ﬁrst removes the permissions and checks the constraints speciﬁed in 𝐴
without changing the heap yet via an intermediate operation remcheck 𝐴; only then does it apply
nondeterministic assignments. The inference rule exh-succ in Fig. 2 formalises this behaviour for
the case when exhale 𝐴 succeeds. The big-step judgement 𝜎 𝑣 ⊢ h𝐴, 𝜎 𝑣 i →rc N(𝜎 𝑣′ ) deﬁnes the
successful execution of a remcheck 𝐴 operation from 𝜎 𝑣 to 𝜎 𝑣′ . nonDet speciﬁes the nondetermin-
istic assignment for all heap locations for which remcheck 𝐴 removed all permission. The case
when remcheck 𝐴 (and thus exhale 𝐴) fails, is captured by the rule exh-fail.
   Our semantics for remcheck 𝐴 decomposes the assertion 𝐴 from left to right: That is, remcheck
𝐴 ∗ 𝐵 ﬁrst executes remcheck 𝐴 and then remcheck 𝐵 (rule rc-sep formalises the case when
remcheck 𝐴 succeeds; if remcheck 𝐴 fails, then remcheck 𝐴 ∗ 𝐵 also fails). However, we need to
also take care that the removal of permissions on-the-ﬂy doesn’t cause subexpressions to be con-
sidered ill-deﬁned, e.g. for the subexpression 𝑥 .𝑓 == 1 in remcheck acc (𝑥 .𝑓 , 1) ∗ 𝑥 .𝑓 == 1 which
comes after the permission to 𝑥 .𝑓 is removed. Thus, our judgement carries both an expression eval-
uation state (𝜎 𝑣0 in rc-sep) in which expressions are evaluated and a reduction state (𝜎 𝑣 and 𝜎 𝑣′ in rc-
sep) from which permissions are removed. Rule rc-acc for remcheck acc (𝑒.𝑓 , 𝑒𝑝 ) models remov-
ing 𝑒𝑝 permission for heap location 𝑒.𝑓 . The operation succeeds (expressed by exhAccSucc(𝑟 , 𝑝, 𝜎 𝑣 ))
iﬀ (1) the to-be-removed permission is nonnegative and, (2) there is suﬃcient permission. Rule rc-
acc is applicable only if 𝑒 and 𝑒𝑝 are well-deﬁned; there is a separate rule (not shown here) ex-
pressing that remcheck acc (𝑒.𝑓 , 𝑒𝑝 ) fails if 𝑒 or 𝑒𝑝 are ill-deﬁned.

2.4    Example Viper-to-Boogie Translation
To give a ﬂavour of a translation of a Viper statement into a Boogie statement, consider Fig. 3,
which shows a simpliﬁed translation used by the existing Viper-to-Boogie implementation. The
Viper statement ﬁrst adds permission to x.f, then updates y.g, and ﬁnally removes the added
permission to x.f and checks that y.g is greater than x.f. This sequence of operations occurs,
for instance, when verifying a method with the permission to x.f as precondition, the ﬁeld update
as method body, and the exhaled assertion as postcondition.
   The corresponding Boogie program is signiﬁcantly larger. The inhale is encoded on lines 1-
4, the assignment is encoded on lines 5-7, and the exhale is encoded on lines 8-18. The Boogie
208:8            Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


                                                       1   tmp := q; assert tmp >= 0;
                                                       2   assume tmp > 0 ==> x != null;
                                                       3   M[x,f] += tmp;
                                                       4   assume GoodMask(M);
                                                       5   assert M[x,f] > 0; assert M[y,g] == 1;
                                                       6   H[y,g] := H[x,f]+1;
                                                       7   assume GoodMask(M);
                                                       8   WM := M;
  inhale acc(x.f, q)
                                                           tmp := q; assert tmp >= 0;
  y.g := x.f+1                                    { 9
                                                      10   if(tmp != 0) {
  exhale acc(x.f, q) * y.g > x.f
                                                      11     assert M[x,f] >= tmp;
                                                      12   }
                                                      13   M[x,f] -= tmp;
                                                      14   assert WM[y,g] > 0; assert WM[x,f] > 0;
                                                      15   assert H[y,g] > H[x,f];
                                                      16   havoc H'; assume idOnPositive(H,H',M);
                                                      17   H := H';
                                                      18   assume GoodMask(M);

Fig. 3. A Viper statement (on the left) and the corresponding (simplified) Boogie statement (on the right)
that is emitted by the current Viper-to-Boogie implementation.


program uses map-typed variables H and M to model the heap and permissions, respectively.5 The
uninterpreted function GoodMask expresses when a permission mask is consistent; an axiom con-
strains the function correspondingly. The permission mask of the expression evaluation state dur-
ing the remcheck operation is captured by the auxiliary variable WM (line 8). All locations in the
assertion are checked to have positive permission w.r.t. WM. The corresponding nondeterministic
assignment of heap values is performed on lines 16-17, where a heap H' is nondeterministically ob-
tained via havoc H' and then constrained to match the original heap H on all locations where there
is positive permission (w.r.t. M) via the assume statement; an axiom constrains the uninterpreted
function idOnPositive correspondingly. Note that this Boogie encoding overapproximates the
nondeterministic assignment speciﬁed by the Viper semantics: assigning new values to all loca-
tions without permission, rather than only those newly without permission. Even this tiny snippet
of code illustrates the explosion in concerns, complexity and the inobvious mapping between con-
cepts in one language and the other, all of which must be taken care of in a formal validation
approach.

3 A FORWARD SIMULATION METHODOLOGY FOR FRONT-END TRANSLATIONS
A front-end translation is sound iﬀ the correctness of an input program is implied by the correct-
ness of the correspondingly-translated IVL program. In our setting: a Viper program (resp. a Boogie
program) is correct if each of its methods (resp. procedures) is correct. At a high level (details in
Sec. 4.5), a method (resp. procedure) is correct if its body has no failing executions. Thus, proving
soundness of the Viper-to-Boogie translation boils down to proving that if the Viper program has
a failing execution, then the translated Boogie program has one also.
   We generate such proofs automatically via a novel general methodology for proving forward
simulations [32] between source and IVL target statements. We observed early on that generating
5 The notation m[a] is syntactic sugar here. We describe in Sec. 5 how maps are represented using the subset from Fig. 1.
Formally Validating Translations into an Intermediate Verification Language                    208:9


such proofs directly based on knowledge of the entire translation would require handling the entire
semantic gap between the source and target languages monolithically in one result, which would
be both infeasible to automate eﬀectively and highly-brittle to any changes in the translation.
   Instead, our methodology employs a combination of key strategies that work together to achieve
reliable and robust automation of our formal simulation results: (1) syntactic and semantic de-
compositions into smaller and more-focused simulation sub-results that are easier to automate,
(2) generic simulation judgements which can be instantiated to obtain the diverse simulation no-
tions we require, (3) generic composition lemmas which factor out common idioms arising in di-
verse facets of the translation, and (4) contextual hypotheses which can be injected into simulation
proofs to handle non-locality of certain translation checks. We present these key ingredients of
our methodology in this section. We illustrate them for Viper and Boogie, but they can be naturally
ported to other front-end translations if one provides a formal semantics for the input language
and IVL, because they are designed to abstract over states, relations and statements employed in
a translation.

3.1   Focusing Forward Simulation Proofs by Decomposition
Intuitively, a forward simulation between a Viper and a Boogie statement shows that for any
execution of the Viper statement, there exists a corresponding execution of the Boogie statement
that simulates it. By deﬁning the simulation such that a failing Viper execution is simulated only
by failing Boogie executions, a forward simulation implies our desired result in particular.
   To tackle the complexity of automatically (and reliably) generating simulation proofs in gen-
eral for the Viper-to-Boogie translation, we employ a variety of strategies for aggressively decom-
posing the desired simulation result into smaller and simpler sub-goals that are themselves still
simulation results. These decompositions are sometimes intuitive based on the syntax: for exam-
ple, in the case of decomposing simulation of a Viper sequential composition into simulations for
its constituent statements. However, we go further than the syntax, decomposing across diﬀerent
semantic concerns for the same Viper statement, into what we call Viper eﬀects.
   For example, we discussed in Sec. 2.3 that the semantics of exhale consists of two eﬀects,
remcheck and a nondeterministic assignment. The simulation proofs for each of these Viper ef-
fects are made separately, and then composed for a simulation proof for the primitive statement as
a whole; this would in turn be composed with simulation proofs for other sequentially-composed
statements, and so on. Note in particular, that simulation proofs may need to relate only a part of
the semantics of a Viper statement to some appropriate Boogie code, a technicality which requires
special care when tracking the relations between corresponding states in the two programs.
   Via our decompositions, each resulting simulation proof focuses on a diﬀerent speciﬁc semantic
concern with respect to the translation in question; these proofs can be made simple enough to
discharge automatically, optionally with tailored tactics. However without care, our decomposi-
tion approach could lead easily to an explosion of ad hoc simulation judgements with disparate
forms and parameters. Instead, our simulation methodology deﬁnes a single, generic simulation
judgement which can be instantiated appropriately to deﬁne each particular simulation judge-
ment required. We design our generic judgements to support instantiations which reﬂect not only
the semantics of the particular eﬀect in isolation, but to optionally include additional contextual
information to be propagated to specialise and aid the simulation proof itself.

3.2   One Simulation Judgement to Rule Them All
Our generic forward simulation judgement sim is deﬁned in Fig. 4. All concrete forward simula-
tions (e.g. for statements, well-deﬁnedness checks, etc.) are instantiations of this judgement. As
well as aiding understanding, this approach enables both tactics which manipulate this generic
208:10            Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers



  simΓ𝑏 (𝑅in, 𝑅out , Succ, Fail, 𝛾 in, 𝛾 out ) , ∀𝜏, 𝜎𝑏 . 𝑅in (𝜏, 𝜎𝑏 ) =⇒
                                                                                                     
         ∀𝜏 ′ . Succ(𝜏, 𝜏 ′ ) =⇒ ∃𝜎𝑏′ . Γ𝑏 ⊢ (𝛾 in, N(𝜎𝑏 )) →∗b (𝛾 out , N(𝜎𝑏′ )) ∧ 𝑅out (𝜏 ′ , 𝜎𝑏′ ) ∧ (Success case)
                                                          
         Fail(𝜏) =⇒ ∃𝛾 ′ . Γ𝑏 ⊢ (𝛾 in, 𝜎𝑏 ) →∗b (𝛾 ′, F)                                                 (Failure case)

  stmSimΓ𝑣 ,Γ𝑏 (𝑅, 𝑅 ′ , 𝑠, 𝛾, 𝛾 ′ ) ,
    simΓ𝑏 (𝑅, 𝑅 ′ , 𝜆𝜎 𝑣 𝜎 𝑣′ . Γ𝑣 ⊢ h𝑠, 𝜎 𝑣 i →v N(𝜎 𝑣′ ), 𝜆𝜎 𝑣 . Γ𝑣 ⊢ h𝑠, 𝜎 𝑣 i →v F, 𝛾, 𝛾 ′ )
                                                                                                                     
                                                𝑅, 𝑅 ′ , (𝜆𝜎 𝑣 𝜎 𝑣′ . 𝜎 𝑣 = 𝜎 𝑣′ ∧ ∃𝑣𝑠. h𝑒𝑠, 𝜎 𝑣 i[⇓]V(𝑣𝑠)),
  wfSimΓ𝑏 (𝑅, 𝑅 ′ , 𝑒𝑠, 𝛾, 𝛾 ′ ) , simΓ𝑏
                                                (𝜆𝜎 𝑣 . h𝑒𝑠, 𝜎 𝑣 i[⇓] ),𝛾, 𝛾 ′
                                                                                                                                   
               ′           ′                   𝑅, 𝑅 ′ , (𝜆(𝜎 𝑣0, 𝜎 𝑣 ) (𝜎 𝑣1, 𝜎 𝑣′ ). 𝜎 𝑣0 = 𝜎 𝑣1 ∧ 𝜎 𝑣0 ⊢ h𝐴, 𝜎 𝑣 i →rc N(𝜎 𝑣′ )),
  rcSimΓ𝑏 (𝑅, 𝑅 , 𝐴, 𝛾, 𝛾 ) , simΓ𝑏
                                               (𝜆(𝜎 𝑣0 , 𝜎 𝑣 ). 𝜎 𝑣0 ⊢ h𝐴, 𝜎 𝑣 i →rc F), 𝛾, 𝛾 ′

Fig. 4. The definition of the generic forward simulation judgement and three common instantiations. The
judgement h𝑒𝑠, 𝜎𝑣 i[⇓]𝑟 lifts the evaluation of an expression (see Sec. 2.3) to a list of expressions 𝑒𝑠.


judgement directly, and generic composition proof rules which embody recurring proof idioms in a
way which is again parametric with the speciﬁc simulations in question (Sec. 3.3).
    sim is deﬁned in terms of multiple parameters: (1) the Boogie context Γ𝑏 , (2) an input relation 𝑅in
and an output relation 𝑅out on Viper and Boogie states, (3) a success predicate Succ characterising
the set of input and output Viper state pairs (𝜏, 𝜏 ′ ) for which there is a successful Viper execution
from 𝜏 to 𝜏 ′ , (4) a failure predicate Fail characterising the set of input Viper states that result in
a failing execution, (5) input and output Boogie program points 𝛾 in and 𝛾 out where the Boogie
executions are expected to start and end, respectively. The success and failure predicate together
abstractly describe the set of Viper executions that must be shown to be simulated.
    simΓ𝑏 (𝑅in , 𝑅out , Succ, Fail, 𝛾 in, 𝛾 out ) holds iﬀ for any Viper and Boogie input states related by 𝑅in ,
the following two conditions hold: (1) for any successful Viper execution from the input Viper state
to an output Viper state 𝜏 ′ , there must be a Boogie execution from program point 𝛾 in and the input
Boogie state to program point 𝛾 out and some output Boogie state that is related to 𝜏 ′ by 𝑅out , and (2)
if the Viper execution fails in the input state, then there must be a failing Boogie execution from
𝛾 in and the input Boogie state (the reached Boogie program point need not be 𝛾 out ). The second
condition is the end goal that we need to show soundness of the Viper-to-Boogie translation. The
ﬁrst condition is needed in order to derive sim compositionally; it guarantees, for example, that
not all Boogie executions for a successful Viper execution produce a magic outcome.
    Three important instantiations of sim that we use are shown at the bottom of Fig. 4. stmSim is
the forward simulation for Viper statements, where the success and failure predicates are instan-
tiated to be a successful and a failing Viper statement reduction, respectively. Thus, the resulting
failure case in sim directly gives us the key property to show the soundness of a Viper-to-Boogie
translation. wfSim is the forward simulation for the well-deﬁnedness check of a list of Viper expres-
sions. Here, the instantiation of the success predicate explicitly expresses that the Viper state does
not change during the evaluation of expressions. rcSim is the forward simulation for remcheck.
Here, the instantiation makes use of the fact that the generic simulation judgement sim is in fact
also (implicitly, here) parametric with the notions of states employed: the “Viper state” is in fact
instantiated to be a pair of standard Viper states in this case, where the ﬁrst Viper state repre-
sents the expression evaluation state and the second Viper state represents the reduction state
(see Sec. 2.3 for this distinction). The success predicate expresses that the expression evaluation
state does not change during a remcheck operation. These three common instantiations are all
Formally Validating Translations into an Intermediate Verification Language                                                      208:11


                    simΓ𝑏 (𝑅, 𝑅 ′ , 𝑆 1, 𝐹 1, 𝛾, 𝛾 ′ )
                                                                                         bSimΓ𝑏 (𝑅, 𝑅1 , 𝛾, 𝛾 1 )
                  simΓ𝑏 (𝑅 ′ , 𝑅 ′′ , 𝑆 2, 𝐹 2, 𝛾 ′ , 𝛾 ′′ )
                                                                                      simΓ𝑏 (𝑅1, 𝑅2, 𝑆, 𝐹, 𝛾 1, 𝛾 2 )
       ∀𝜏, 𝜏 . 𝑆 (𝜏, 𝜏 ′′ ) ⇒ ∃𝜏 ′ . 𝑆 1 (𝜏, 𝜏 ′ ) ∧ 𝑆 2 (𝜏 ′, 𝜏 ′′ )
             ′′
                                                                                        bSimΓ𝑏 (𝑅2, 𝑅 ′ , 𝛾 2, 𝛾 ′ )
        ∀𝜏 . 𝐹 (𝜏) ⇒ 𝐹 1 (𝜏) ∨ ∃𝜏 ′ . 𝑆 1 (𝜏, 𝜏 ′ ) ∧ 𝐹 2 (𝜏 ′ )                                                           (bprop)
                                       ′′            ′′
                                                                         (comp)        simΓ𝑏 (𝑅, 𝑅 ′ , 𝑆, 𝐹, 𝛾,𝛾 ′ )
                       simΓ𝑏 (𝑅, 𝑅 , 𝑆, 𝐹, 𝛾, 𝛾 )

        stmSimΓ𝑣 ,Γ𝑏 (𝑅, 𝑅 ′ , 𝑠 1, 𝛾, 𝛾 ′ )                                    bSimΓ𝑏 (𝑅, 𝑅 ′ , 𝛾,𝛾 ′ ) ,
      stmSimΓ𝑣 ,Γ𝑏 (𝑅 ′ , 𝑅 ′′ , 𝑠 2, 𝛾 ′ , 𝛾 ′′ )                      where
                                                     (seq-sim)                  simΓ𝑏 (𝑅, 𝑅 ′ , 𝜆𝜏 𝜏 ′ . 𝜏 = 𝜏 ′ , 𝜆_. ⊥, 𝛾, 𝛾 ′ )
 stmSimΓ𝑣 ,Γ𝑏 (𝑅, 𝑅 ′′ , (𝑠 1 ; 𝑠 2 ), 𝛾, 𝛾 ′′ )

Fig. 5. The instantiation-independent rules comp and bprop and the concrete rule for the simulation of 𝑠 1 ; 𝑠 2 .




expressed directly via the Viper reduction judgements introduced in Sec. 2.3. Like the generic sim-
ulation judgement, the three instantiations are themselves generic, abstracting away how the Viper
and Boogie states are related by taking the input and output state relations as parameters. As we
will show in Sec. 3.4, we also use instantiations that do not just use Viper reduction judgements
(e.g. to express the non-deterministic assignment of heap values in remcheck).

3.3      Instantiation-Independent Rules
Many simulation idioms arise repeatedly in a complex translation. Notions of sequential composi-
tion, conditional evaluation, stuttering steps are all good examples, which require a certain stylised
formal justiﬁcation to reason about. Our generic simulation judgement allows us to identify and
formalise these idioms once and for all, providing, for example, generic composition lemmas that
can be proved once and instantiated for diﬀerent purposes. In this subsection, we present these id-
ioms as inference rules, but in our formalisation they are expressed and proved as regular lemmas.
   For example, we prove a single general composition rule from which we derive concrete rules to
combine (1) simulations of 𝑠 1 and 𝑠 2 to a simulation of 𝑠 1 ; 𝑠 2 , (2) simulations of remcheck 𝐴1 and
remcheck 𝐴2 to remcheck 𝐴1 ∗ 𝐴2 , (3) simulations of inhale 𝐴1 and inhale 𝐴2 to inhale 𝐴1 ∗
𝐴2 . The general composition rule comp in Fig. 5 captures the composition of two, possibly diﬀerent,
instantiations of sim, where the output relation and Boogie program point of the ﬁrst instantiation
match the input relation and program point of the second one. The two ﬁnal premises constrain
the resulting success and failure predicates. In particular, the composed Viper execution should fail
only if either the ﬁrst instantiation fails or if the second instantiation fails in a state successfully
reached by the ﬁrst one. The rule seq-sim in Fig. 5 shows the concrete composition rule for 𝑠 1 ; 𝑠 2 ,
which is derived from comp. Note that seq-sim does not impose any constraints on the Boogie
program points, which is crucial to handle Viper’s and Boogie’s disparate ASTs (see Sec. 2.1). We
will discuss in Sec. 4.3 how we deal with the AST mismatch when automating proofs.
   As a second example, the notion of simulation stuttering steps also arises in many ways, when-
ever some auxiliary Boogie code is generated that does not fully correspond to a step in the Viper
source. This includes initialisations of auxiliary variables, or Boogie assume statements for prop-
erties from the current simulation state relation. This idiom is captured by the Boogie propagation
rule bprop in Fig. 5, in which bSim expresses simulations in which the Viper state remains un-
changed, and thus only the Boogie state may change (causing adjustment to the state relations).
208:12            Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


      rcSimΓ𝑏 ( [𝜆(𝜎 𝑣0 , 𝜎 𝑣 ) 𝜎𝑏 . 𝜎 𝑣0 = 𝜎 𝑣 ∧ 𝑅(𝜎 𝑣 , 𝜎𝑏 )], 𝑅 ′ , 𝐴, 𝛾, 𝛾 ′ ) (sim. of remcheck 𝐴)
        simΓ𝑏 (𝑅 ′ , [𝜆(_, 𝜎 𝑣 ) 𝜎𝑏 . 𝑅 ′′ (𝜎 𝑣 , 𝜎𝑏 )], Succ 2, 𝜆_. ⊥, 𝛾 ′, 𝛾 ′′ ) (non-det. selection)
                                                                                                           (exh-sim)
                                 stmSimΓ𝑣 ,Γ𝑏 (𝑅, 𝑅 ′′ , exhale 𝐴, 𝛾, 𝛾 ′′ )

  Succ 2 , 𝜆(𝜎 𝑣0, 𝜎 𝑣 ) (_, 𝜎 𝑣′ ). nonDet(𝜎 𝑣0 , 𝜎 𝑣 , 𝜎 𝑣′ ) ∧ 𝜎 𝑣0 ⊢ h𝐴, 𝜎 𝑣0 i →rc 𝜎 𝑣

             Fig. 6. Rule for the simulation of exhale 𝐴. The definition of nonDet is given in Fig. 2.


3.4 Examples: Generic Decomposition in Action
As outlined above, the general strategy for our simulation methodology is to decompose our simu-
lation goals as far as possible, while leaving as many parameters generic as we can to enable maxi-
mal reuse of our results and composition lemmas. While decomposition handles the semantic gap,
our use of generic parameterisation provides the abstraction to address the diverse translations
used in practical translational veriﬁers. In the following, we showcase our methodology on one
rule, but the same ideas apply to all our formal rules (see a second example in App. B).
   Consider the rule exh-sim for the simulation of exhale 𝐴 in Fig. 6. The ﬁrst premise is expressed
as a simulation of the ﬁrst eﬀect, remcheck, which we can express via the rcSim instantiation
(see Fig. 4). The second premise models nondeterministic assignment, which is captured by the
ﬁrst conjunct nonDet of the corresponding success predicate and by the failure predicate, which
reﬂects that the nondeterministic assignment cannot fail.
   By modularly abstracting over the details of these premises, and the precise deﬁnitions of the
states and state relations (e.g. the intermediate relation 𝑅 ′ in this rule), we obtain robustness to
diverse translations: our rules do not constrain which exact Boogie statements correspond to a
Viper eﬀect. For example, the Viper-to-Boogie implementation establishes the nondeterministic
heap assignment premise in exh-sim in two diﬀerent ways depending on whether the assertion
contains an accessibility predicate acc (𝑒.𝑓 , 𝑝) or not; if not, then the implementation does not
emit any Boogie code for the nondeterministic assignment, which is sound, since no permission
is removed.
   Note that this genericity does not prevent the rule from exploiting contextual information.
For example, the input state relation of the ﬁrst premise speciﬁes that at the beginning of the
remcheck 𝐴 eﬀect the expression evaluation state and the reduction state are the same. This
property does not hold in general for executions of remcheck (e.g. it might not hold when exe-
cuting the second conjunct of a separating conjunction), but it does hold here, at the beginning of
an exhale. The second premise’s success predicate includes the fact that the current Viper state
was reached via remcheck 𝐴. This allows us, for example, to conclude that the nondeterministic
assignment has no eﬀect if remcheck 𝐴 removes no permissions, which is required to justify the
case when the implementation does not emit Boogie code for the nondeterministic assignment.

3.5      Injecting Non-Local Hypotheses into Simulation Proofs
Our rules are designed to be parametric in the state relation between the Viper and Boogie state
and permit adjusting this state relation at diﬀerent points in the simulation proof (e.g. via the
Boogie propagation rule bprop in Fig. 5). In principle, this allows the injection of arbitrary non-
locally-justiﬁed hypotheses into all of our simulation judgements. However, automating the usage
of general logical assumptions embedded into our state relations can become a challenge in itself.
   For example, the Viper-to-Boogie implementation omits the well-deﬁnedness checks of expres-
sions in the translation of remcheck 𝐴 and inhale 𝐴 in certain cases (as we will discuss in
Formally Validating Translations into an Intermediate Verification Language                                           208:13


                              𝑄                                    𝑄
                    rcInvSimΓ𝑏 (𝑅, 𝑅 ′ , 𝐴1, 𝛾, 𝛾 ′ ) rcInvSimΓ𝑏 (𝑅 ′ , 𝑅 ′′ , 𝐴2 , 𝛾 ′ , 𝛾 ′′ )
                                                                                                             
                                             𝑄 (𝐴1 , (𝜎 𝑣0, 𝜎 𝑣 )) ∧
 ∀𝜎 𝑣0 , 𝜎 𝑣 . 𝑄 (𝐴1 ∗ 𝐴2, (𝜎 𝑣0, 𝜎 𝑣 )) ⇒
                                             ∀𝜎 𝑣′ . 𝜎 𝑣0 ⊢ h𝐴1 , 𝜎 𝑣 i →rc N(𝜎 𝑣′ ) ⇒ 𝑄 (𝐴2 , (𝜎 𝑣0, 𝜎 𝑣′ ))
                                             𝑄                                                                    (rsep-sim)
                                  rcInvSimΓ𝑣 (𝑅, 𝑅 ′′ , (𝐴1 ∗ 𝐴2 ), 𝛾, 𝛾 ′′ )
           𝑄
rcInvSimΓ𝑏 (𝑅, 𝑅 ′ , 𝐴, 𝛾, 𝛾 ′ ) , rcSimΓ𝑏 ((𝜆𝜏, 𝜎𝑏 . 𝑅(𝜏, 𝜎𝑏 ) ∧ 𝑄 (𝐴, 𝜏)), 𝑅 ′ , 𝐴, 𝛾, 𝛾 ′ )

Fig. 7. The instantiation for simulating remcheck 𝐴 with assertion predicate 𝑄 (bottom) and the correspond-
ing rule for the separating conjunction (top).


Sec. 4.2). This is justiﬁed, because 𝐴 is checked to be well-formed non-locally in those cases, but
to use this additional hypothesis requires propagating and adjusting it through the cases of the
deﬁnition of remcheck 𝐴 and inhale 𝐴.
   As a ﬁnal ingredient of our methodology, to avoid these recurring adaptations and proof steps,
we allow specialised instantiations of the generic forward simulation judgement sim that encapsu-
late these extra hypotheses as additional premises. Thus, applications of the rule can work with a
ﬁxed state relation and replace recurring proof steps by the justiﬁcation of an additional premise.
   For example, Fig. 7 shows (at the bottom) an instantiation of sim that expresses the simulation
of remcheck 𝐴, parameterised with a predicate 𝑄 on assertions. Its deﬁnition in terms of rcSim
requires 𝑄 (𝐴, 𝜏) to hold as part of the input state relation. The specialised rule rsep-sim (top of
Fig. 7) for remcheck 𝐴1 ∗ 𝐴2 decomposes the simulation into simulations for 𝐴1 and 𝐴2 .6 Both
sub-simulations use the same predicate 𝑄, such that applications of the rule do not need to adjust
the state relations explicitly to reﬂect that, for example, 𝑄 holds for 𝐴1 and 𝐴2 in the respective
states. This property is ensured by the third premise. In practice, for a speciﬁc 𝑄, we prove the third
premise once and for all for all assertions 𝐴1 and 𝐴2 , which avoids the recurring proof steps that
would be necessary without the specialised rule. Note that the same parameter can be instantiated
in many ways to capture diﬀerent non-local hypotheses for diﬀerent applications of the same rule.

   In summary, our methodology solves all three challenges outlined in the introduction. The large
semantic gap between the input language and the IVL is handled by decomposing the statements
of the input language into smaller eﬀects and deﬁning for each of them instantiations of a generic
forward simulation relation. The parameterisation of this relation allows us, in particular, to cap-
ture information about the context in which the eﬀects are executed. This parameterisation also
supports diverse translations by abstracting from the details of the translation. Finally, non-locality
is handled by capturing properties checked elsewhere in the state relations, and by devising spe-
cialised rules that simplify the proof generation. All of these ideas are needed to validate the exist-
ing Viper-to-Boogie translation, but apply equally to other front-end translations.

4   PUTTING THE METHODOLOGY TO WORK
This section presents ideas for applying the methodology from Sec. 3 to concrete front-end transla-
tions. In particular, the section presents our instantiation of the state relation (Sec. 4.1), a concrete
instance of non-local reasoning (Sec. 4.2), and how our proof automation works (Sec. 4.3). Finally,
the section discusses the background theory for Boogie (Sec. 4.4), which includes polymorphic
maps, and shows how to use forward simulation proofs to generate the ﬁnal theorem (Sec. 4.5).
6 rsep-sim can be derived from the instantiation-independent composition rule (Fig. 5) and consequence rule cons (App. C).
208:14           Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


4.1 State Relation
Our rules for deriving forward simulation judgements (Sec. 3) allow us to adjust state relations as
needed during a simulation proof. We use this ﬂexibility in many ways, e.g. when (1) a scoped Viper
variable is introduced, (2) a new auxiliary Boogie variable is introduced, (3) the Boogie variables
tracking the Viper state are changed. To facilitate proof automation for handling such adjustments,
we build in a stylised form for expressing state relations for this translation via two parameters: a
partial auxiliary variable map from auxiliary Boogie variables to logical conditions they each satisfy,
and a translation record specifying how key Viper components are represented in the Boogie state;
the scenarios above are all handled by adjusting one of these two parameters. Translation records
comprise: (1) a mapping var (Tr) from Viper variables to their Boogie counterparts, (2) the Boogie
variables representing the Viper heap H (Tr) and permission mask M (Tr) (and whenever we use
a separate expression evaluation state, the corresponding variables representing the heap H 0 (Tr)
and mask M 0 (Tr)) and (3) a mapping ﬁeld (Tr) from Viper ﬁelds to corresponding Boogie constants.
   The following deﬁnition shows a simpliﬁed excerpt of our state relation instantiation SR for
translation record Tr and auxiliary variable map AV , where 𝜎 𝑣 and 𝜎𝑏 are the Viper and Boogie
states, and 𝜎 𝑣0 is a distinguished Viper expression evaluation state (if there is none, then 𝜎 𝑣 = 𝜎 𝑣0 ):
SRTr,AV
  Γ𝑏    ((𝜎 𝑣0, 𝜎 𝑣 ), 𝜎𝑏 ) , consistent(𝜎 𝑣0 ) ∧ consistent(𝜎 𝑣 ) ∧
fieldRelΓ𝑏 (ﬁeld (Tr), 𝜎𝑏 ) ∧ (∀𝑥, 𝑃. AV (𝑥) = 𝑃 ⇒ 𝑃 (𝜎𝑏 (𝑥))) ∧
stRelΓ𝑏 (var (Tr), 𝜎 𝑣 , 𝜎𝑏 ) ∧ hmRelΓ𝑏 (H (Tr), M (Tr), 𝜎 𝑣 , 𝜎𝑏 ) ∧ hmRelΓ𝑏 (H 0 (Tr), M 0 (Tr), 𝜎 𝑣0, 𝜎𝑏 ) ∧ ...
The ﬁrst line ensures that the Viper states are consistent. The second line ensures that the Viper
ﬁelds are represented in the Boogie state (fieldRel) and that for each (𝑥, 𝑃) in the auxiliary variable
map, 𝑃 holds for the value of 𝑥. The third line ensures that the Boogie state correctly captures the
Viper state: both in terms of its variable store (stRel) and heap and permission mask (hmRel).

4.2      Non-Locality
For most occurrences of remcheck 𝐴, the Viper-to-Boogie implementation generates well-
deﬁnedness checks in the Boogie program corresponding to expressions evaluated in 𝐴. However,
speciﬁcally when executing the exhale of a method call’s precondition, the translation omits
these well-deﬁnedness checks for the corresponding remcheck operation. This is justiﬁed by a
non-local check: the Boogie code for the callee’s translation checks that the callee’s speciﬁcation
is well-formed, which implies that expressions evaluated in the precondition will always be well-
deﬁned.7
   Given Viper’s semantics, our standard simulation proof for remcheck 𝐴 would fail if we did
not reﬂect the consequences of this non-local guarantee in a way that is used automatically during
the proof. We instantiate the general strategy outlined in Sec. 3.5 for this purpose, which allows
us to choose a predicate 𝑄 pre on assertions that will be applied throughout the simulation proof
for remcheck 𝐴. Our strategy requires us to ﬁnd 𝑄 pre such that (a) it is implied by the non-local
check elsewhere, and (b) it can be propagated identically to sub-assertions of 𝐴 during the proof
(e.g. satisfying the third premise of rsep-sim in Fig. 7, and similarly for other connectives).
   In this case, we instantiate the predicate in our strategy with the following deﬁnition:
                𝑄 pre (𝐴, 𝜎 𝑣0, 𝜎 𝑣 ) , consistent(𝜎 𝑣0 ) ∧ ∃𝜎 𝑣i . 𝜎 𝑣 ⊕ 𝜎 𝑣i  𝜎 𝑣0 ∧ ¬h𝐴, 𝜎 𝑣i i →inh F
Here, h𝐴, 𝜎 𝑣 i →inh 𝑟 𝑣 holds iﬀ Γ𝑣 ⊢ hinhale 𝐴, 𝜎 𝑣 i →v 𝑟 𝑣 , and ⊕ and  (and later, ⊖) have
standard pointwise meanings on permission masks, leaving heaps and stores identical. This pred-
icate expresses that possibly after restoring some permissions (in 𝜎 𝑣i ) that we had at the start of
7 There is an analogous non-local check for 𝑚’s postcondition that we do not discuss here for simplicity of presentation.
Formally Validating Translations into an Intermediate Verification Language                                           208:15



                           Proof P2 (hint 3)                   Proof P3 (no hint)
Proof Tree 𝑇 :       rcSimΓ𝑏 (𝑅2, 𝑅2, 𝐴1 , 𝛾 1, 𝛾 2 )      rcSimΓ𝑏 (𝑅2, 𝑅2, 𝐴2, 𝛾 2, 𝛾 3 )
                                                                                             (rsep2-sim)
                                     rcSimΓ𝑏 (𝑅2, 𝑅2, 𝐴1 ∗ 𝐴2 , 𝛾 1, 𝛾 3 )
  Proof P1 (hint 2)
bSimΓ𝑏 (𝑅1, 𝑅2, 𝛾, 𝛾 1 )      (Proof Tree 𝑇 )                           Proof P4 (hints 4 and 5)
                                                  (rcprop)
       rcSimΓ𝑏 (𝑅1, 𝑅2, 𝐴1 ∗ 𝐴2 , 𝛾, 𝛾 3 )                         simΓ𝑏 (𝑅2 , 𝑅3, Succ 2 , 𝜆_. ⊥, 𝛾 3, 𝛾 ′ )
                                                                                                                (exh-sim)
                                stmSimΓ𝑣 ,Γ𝑏 (𝑅, 𝑅, exhale 𝐴1 ∗ 𝐴2 , 𝛾, 𝛾 ′ )                                    | {z }
                                                                                                                  hint 1

𝐴1 , acc ( x.f, q) 𝐴2 , y.g > x.f 𝑅 , 𝜆(𝜎 𝑣 , 𝜎𝑏 ). SRTr,AV     Γ𝑏 ((𝜎 𝑣 , 𝜎 𝑣 ), 𝜎𝑏 ) 𝑅3 , 𝜆(_, 𝜎 𝑣 ) 𝜎𝑏 . 𝑅(𝜎 𝑣 , 𝜎𝑏 )
𝑅1 , 𝜆(𝜎 𝑣0, 𝜎 𝑣 ) 𝜎𝑏 . 𝜎 𝑣0 = 𝜎 𝑣 ∧ 𝑅(𝜎 𝑣 , 𝜎𝑏 ) 𝑅2 , SRTr
                                                         Γ𝑏
                                                            1 ,AV
                                                                   Tr 1 , Tr (M 0 ↦→ WM)

Fig. 8. Proof tree constructed by our proof automation for the simulation of exhale acc ( x.f, q) ∗ y.g > x.f
via the Boogie statement in Fig. 3 on lines 8-18. The automation uses generated hints for the application
of rule exh-sim, and for proofs at the leaves (P𝑖 ; left abstract here). The Boogie program points 𝛾, 𝛾 1 , 𝛾 2 ,
𝛾 3 , and 𝛾 ′ are the points in Fig. 3 starting on lines 8, 9, 14, 16, and 18, respectively. SR is our state relation
instantiation introduced in Sec. 4.1. Succ 2 is defined in Fig. 6 (where the assertion is 𝐴1 ∗ 𝐴2 ). Rules rcprop
and rsep2-sim are derived from bprop (Fig. 5) and rsep-sim (Fig. 7), respectively.


the exhale, at least an inhale of 𝐴 would not fail (i.e. expressions evaluated within 𝐴 will be
well-deﬁned). The non-local check of the method precondition, which eﬀectively checks that an
inhale would not fail starting from an empty state (i.e. no permissions), implies the predicate
for an empty 𝜎 𝑣i . Showing formally that 𝑄 pre can be propagated over connectives occurring in 𝐴
requires in particular a technical lemma stating a partial inversion property between remcheck
and inhale:
    Lemma 4.1. Let 𝐴 be an assertion and 𝜎 𝑣0 , 𝜎 𝑣′ , 𝜎 𝑣𝑖 , 𝜎 𝑣𝑠 be Viper states, where 𝜎 𝑣𝑠 = 𝜎 𝑣𝑖 ⊕ (𝜎 𝑣 ⊖ 𝜎 𝑣′ ) and
𝜎 𝑣 is consistent. If 𝜎 𝑣0 ⊢ h𝐴, 𝜎 𝑣 i →rc N(𝜎 𝑣′ ) and ¬h𝐴, 𝜎 𝑣i i →inh F holds, then h𝐴, 𝜎 𝑣i i →inh N(𝜎 𝑣𝑠 ).
  𝑠

  We prove this result by induction on the reduction of remcheck. The lemma essentially states
that the permissions that get removed by remcheck 𝐴 (expressed by 𝜎 𝑣 ⊖ 𝜎 𝑣′ ) are exactly those
that will be added by a corresponding (non-failing) inhale 𝐴 operation.

4.3    Proof Automation
We have extended the Viper-to-Boogie implementation to automatically generate an Isabelle proof
relating the Viper and Boogie programs. To make this automatic generation possible, we instru-
ment less than 500 lines of the existing implementation to produce hints, which provide extra
information about the Boogie encoding. A core component of our proof automation is an Isabelle
tactic that uses these hints to automatically prove forward simulations. The tactic applies the rules
provided by our methodology (Sec. 3) to decompose simulations into smaller ones and generates
proofs for atomic simulations that are not further decomposed. Our instrumentation generates two
kinds of hints for the tactic: (1) hints indicating which candidate of multiple diverse translations
is used, and (2) hints specifying how to instantiate parameters and discharge premises of a rule.
   As a concrete example, consider Fig. 8, which shows the proof generated by our tactic (repre-
sented via a proof tree) for the forward simulation of exhale acc ( x.f, q) ∗ y.g > x.f via the
Boogie statement in Fig. 3 on lines 8-18. Hints 1 and 4 in Fig. 8 are hints of the ﬁrst kind. Hint
208:16           Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


1 speciﬁes that well-deﬁnedness checks are not omitted in the translation of remcheck; as a re-
sult, the tactic applies exh-sim, which does not track a separate predicate 𝑄 on assertions for the
remcheck simulation (see Sec. 3.5). Hint 4 speciﬁes that the nondeterministic heap assignment is
not omitted in the Boogie code (see Sec. 3.4 for when it is omitted), which directs the tactic to use
a speciﬁc rule (not shown in the ﬁgure). Hints 2, 3, and 5 in Fig. 8 are hints of the second kind.
Each of them provides information on temporary Boogie variables (name and lemma showing the
declared type is the expected one) in Fig. 3. The temporary variables here are (1) WM to set up the
expression evaluation state on line 8 (hint 2), which results in a change of the translation record in
𝑅2 (see Sec. 4.1), (2) tmp to store the permission on line 9 (hint 3), which is used to adjust the aux-
iliary variable map (see Sec. 4.1) in proof P2 , and (3) H’ to perform the nondeterministic selection
on line 16 (hint 5).
   After decomposing the simulation, our tactic must automatically prove the atomic simulations.
In Fig. 8, P1 and P4 are such proofs. P2 and P3 further decompose the simulation before reach-
ing atomic simulations (P2 does so via the rule shown in App. B). We use two main automation
approaches for atomic simulations. Firstly, we prove (once and for all) simple lemmas about the
behaviours of small sequences of simple Boogie commands; these are applied (and their hypothe-
ses discharged) automatically when needed. These lemmas are used for only small parts of the
overall translation. Secondly, we prove (once and for all) lemmas that capture eﬀects simulated
by assume and assert statements for arbitrary expressions. This generality enables a tactic to
automatically prove Viper eﬀects that are simulated via a combination of these two statements.
   Our tactic uses both of these approaches for the example in Fig. 8. Proof P2 uses the second
approach for justifying the nonfailure check for remcheck acc (𝑒.𝑓 , 𝑝) shown on lines 9-12 in
Fig. 3.8 Proofs P1 and P4 use the ﬁrst approach. As part of proof P4 , we use a lemma of the
following form proved once and for all (K is a continuation and the free variables are universally
quantiﬁed):

     Lemma 4.2. If (1) SRTr,AV
                           Γ𝑏       ((𝜎 𝑣 , 𝜎 𝑣 ), 𝜎𝑏 ), (2) nonDet(𝜎 𝑣0, 𝜎 𝑣 , 𝜎 𝑣′ ), (3) ℎ = H (Tr) ∧ 𝑚 = M (Tr), and
(4) ... then there is a state 𝜎𝑏′ such that Γ𝑏 ⊢ (( havoc ℎ ′ :: assume 𝑓 (ℎ, ℎ ′ , 𝑚) :: ℎ := ℎ ′ ::
                           𝑐 ; if , K), N(𝜎𝑏′ )) and SRTr,AV
𝑐®; if , K), N(𝜎𝑏 )) →∗b ((®                                  Γ𝑏 ((𝜎 𝑣′ , 𝜎 𝑣′ ), 𝜎𝑏′ ).

   This lemma captures that a havoc-assume-assignment sequence simulates the nondeterminis-
tic heap assignment w.r.t. our state relation instantiation (see Sec. 4.1). The fourth premise (not
shown here) includes constraints on 𝑓 ’s interpretation and on ℎ ′ .9
   A general challenge when the tactic applies the rules from Sec. 3 is that the Viper and Boogie
ASTs are structured diﬀerently (see Sec. 2.1). Thus, the automatic selection of Boogie program
points in the premises of rules is not immediate. For example, when applying rule exh-sim in Fig. 8,
the tactic cannot easily choose the intermediate program point 𝛾 3 by inspecting the initial program
point 𝛾. Instead, the tactic starts proving the ﬁrst premise with an existentially quantiﬁed 𝛾 3 . Once
the proof reaches the goal of proof P1 (i.e. the ﬁrst atomic simulation), it becomes clear how to
advance the program point 𝛾 and, by the end of the proof of the ﬁrst premise of exh-sim, the choice
of 𝛾 3 becomes clear. This strategy is enabled by our routine use of schematic variables in Isabelle
(evars in other tools), for postponing the choice of witnesses for existentially-quantiﬁed values.


8 The approach is designed to work without any changes to the tactic even if the expressions in the two assert statements

were changed to be syntactically diﬀerent.
9 If the implementation changed the translation for the nondeterministic heap assignment, then we would have to adjust

only the tactic’s proof strategy for this assignment via a new lemma (i.e. proof P4 in Fig. 8); the rest remains unchanged.
Formally Validating Translations into an Intermediate Verification Language                                  208:17



  Correct𝐺
         𝑏 (𝑝) , ∀T , F , 𝜎𝑏 . [DeclsWf𝐺,𝑝 (T , F ) ∧ AxiomSat𝐺 (T , F , 𝜎𝑏 )] =⇒
                          ∀𝛾 ′ , 𝑟𝑏′ . initCtxt𝐺                                    ∗   ′ ′          ′
                                               𝑏 (𝑝, T , F ) ⊢ (init𝑏 (𝑝), N(𝜎𝑏 )) →b (𝛾 , 𝑟 𝑏 ) ⇒ 𝑟 𝑏 ≠ F

  Correct𝐹𝑣 ,𝑀 (𝑚) ,
     ∀𝜎 𝑣 . (∀𝑙 .𝜋 (𝜎 𝑣 ) (𝑙) = 0) =⇒
         ∀𝑟 𝑣 . initCtxt𝑀,𝐹
                        𝑣 (𝑚) ⊢ hinhale pre(𝑚); body(𝑚); exhale post(𝑚), 𝜎 𝑣 i →v 𝑟 𝑣 ⇒ 𝑟 𝑣 ≠ F


Fig. 9. The correctness definitions for a Boogie procedure 𝑝 (top) and Viper method 𝑚 (bottom). We ignore
the restriction on well-typed states here, but include the restriction in the Isabelle formalisation.


4.4 Background Theory and Polymorphic Maps
Boogie does not have any notion of a heap location or a Viper state. Such Viper (and other front-
end) constructs are translated using particular global declarations in Boogie. A subset of the Boogie
declarations always emitted by the Viper-to-Boogie implementation is given by:
      • Uninterpreted types bref and bfield to model references and ﬁelds. bfield takes one
        type argument indicating the type of the corresponding Viper ﬁeld.10
      • An uninterpreted function GoodMask that maps a permission map to a Boolean and an ax-
        iom restricting this function to return true only if the permission map models a consistent
        Viper permission mask.
      • Global variables H and M to model the heap and permission mask, respectively. H[x,f]
        stores the heap value for heap location x.f and M[x,f] stores the permission value for
        x.f. The types of both variables are represented via Boogie’s impredicatively-polymorphic
        maps [30], which we explain below.
The correctness of a Boogie procedure guarantees no failing executions of the procedure’s body
for any interpretation of the uninterpreted types and functions (1) that is well-formed (e.g. the
function interpretation respects the declared function signatures), and (2) for which all the Boogie
axioms in the Boogie program are satisﬁed in the initial Boogie state. The formal correctness deﬁni-
tion for a Boogie procedure 𝑝 reﬂects this directly (a simpliﬁed version is shown at the top of Fig. 9).
T and F are the interpretations of uninterpreted types and functions, respectively. 𝐺 denotes the
global declarations in the Boogie program. init𝑏 (𝑝) is the initial Boogie program point in the pro-
cedure 𝑝. initCtxt𝐺𝑏 (𝑝, T , F ) constructs a Boogie context from the provided parameters. Thus, to
use the correctness of a Boogie procedure, we must choose a type and function interpretation that
satisfy the required conditions. The main challenge here is formally expressing interpretations
that deal with polymorphic Boogie maps, as we discuss next.
   Polymorphic maps. The heap and permission maps are represented (via the Viper-to-Boogie
translation) using Boogie’s polymorphic maps; this choice is not unusual (e.g. the Dafny-to-Boogie
implementation also currently uses polymorphic maps with similar polymorphic map types as the
ones used by the Viper-to-Boogie implementation). The Boogie maps used to model Viper heaps
have the polymorphic map type <T>[bref, bfield T]T: a total map storing, for any type T,
values of type T given (as key) a reference and ﬁeld with type argument T.
   To our knowledge, there exists no formal model for Boogie’s polymorphic maps. Providing a
general model is challenging: in particular, Boogie’s polymorphic maps are impredicative: a map
𝑚 of type <T>[T]T’ permits any value as a key, including the map 𝑚 itself! Instead of providing a
10 In practice, bfield takes one more type argument that we ignore for the sake of presentation.
208:18        Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


formal model for polymorphic maps in general, we provide one tailored to those that the Viper-to-
Boogie implementation uses. To aid the incorporation of our model, we adjust the implementation
to represent a polymorphic map via an uninterpreted type (e.g. HType for the heap), polymorphic
functions for reading from and updating a polymorphic map (e.g. read and upd), and two axioms
that express the relationship between the two functions. The only change in the translation itself is
to simply rewrite heap and mask lookups and updates into calls to these functions; everything else
remains identical. Then, we provide interpretations of the types and functions, and automatically
prove that the axioms hold for these interpretations for any state that maps constants to their
deﬁned values; the same approach could be used for e.g. the Dafny-to-Boogie translation.
   What remains for our simulation proofs is to provide interpretations for these new components
(e.g. HType, read, and upd for the heap) such that the axioms are fulﬁlled. The challenge here
is avoiding circularities: e.g. if the ﬁeld provided to read has type parameter HType, then the
instantiation of read must itself return a heap; to construct an initial heap, we already need a
heap of the same type. To break this circularity, we instantiate HType as a partial mapping from
reference and ﬁelds to values, and allow the empty map to be of type HType, which provides us
with a concrete heap. read is deﬁned to return a default value for reference and ﬁeld pairs that
are not in the domain of the partial map; for heaps the default value is the empty map. This is
suﬃcient to prove the axioms, since in practice the axioms only require read returning speciﬁc
values when those values were previously inserted by upd.

4.5 Generating A Proof of the Final Theorem
We will now discuss, given a Viper program and its Boogie translation, how forward simulation
proofs can be used to generate a proof of the ﬁnal theorem justifying the soundness of the trans-
lation: The correctness of the Boogie program (i.e. the correctness of all contained Boogie pro-
cedures) implies the correctness of the Viper program (i.e. the correctness of all contained Viper
methods).
   We decompose the proof of the ﬁnal theorem into smaller parts. At a high level, the Viper-to-
Boogie translation works as follows. Let 𝐹 and 𝑀 be the set of Viper ﬁelds and methods in the
Viper program, respectively. The Viper-to-Boogie translation (1) emits global Boogie declarations
𝐺 (see Sec. 4.4) and (2) generates a separate Boogie procedure 𝑝 (𝑚) for every Viper method 𝑚
in 𝑀. The intended relation between 𝑚 and 𝑝 (𝑚) is given by Rel𝐺𝐹,𝑀 (𝑚, 𝑝 (𝑚)) in Fig. 10, which
states that the correctness of 𝑝 (𝑚) w.r.t. 𝐺 guarantees two things: (C1) the well-formedness of 𝑚’s
speciﬁcation, and (C2) the correctness of 𝑚 w.r.t. 𝐹 and 𝑀 if the speciﬁcations of all methods in
the Viper program are well-formed. The reason that the correctness of 𝑚 is not implied directly is
due to the optimised translation of method calls (as explained in Sec. 4.2).
   Fig. 10 shows how we generate the proof of the desired theorem in two steps. First, for each Viper
method 𝑚 and its translated Boogie procedure 𝑝 (𝑚), we generate a proof for Rel𝐺𝐹,𝑀 (𝑚, 𝑝 (𝑚)),
explained next. Second, we obtain the desired theorem directly from these per-method relational
proofs, since the correctness of all Boogie procedures implies that all Viper method speciﬁcations
are well-formed using (C1), which implies that each Viper method is correct using (C2).
   Next, we turn the focus to our strategy for proving Rel𝐺𝐹,𝑀 (𝑚, 𝑝 (𝑚)). For the sake of presentation,
we focus on the proof of (C2) (correctness of 𝑚), and omit the proof of (C1) (well-formedness
of 𝑚’s speciﬁcation). Intuitively, to prove that 𝑚 is correct, we have to show that for any state
that satisﬁes 𝑚’s precondition, executing 𝑚’s body in this state results in a state that satisﬁes
𝑚’s postcondition. The correctness deﬁnition for a Viper method (shown at the bottom of Fig. 9)
expresses this by requiring that any execution starting in a state 𝜎 𝑣 with no permissions that
inhales the precondition, then executes the body, and ﬁnally exhales the postcondition, cannot
Formally Validating Translations into an Intermediate Verification Language                                       208:19


               Translation                      Relational proofs                           Final proof
        method 𝑚 1 { proc 𝑝 1                    Rel𝐺𝐹,𝑀 (𝑚 1, 𝑝 1 )                   (∀𝑝 ∈ 𝑃. Correct𝐺
                                                                                                       𝑏
                                                                                                          (𝑝))
        ···                                      ···                                             =⇒
        method 𝑚𝑛 { proc 𝑝 𝑛                     Rel𝐺𝐹,𝑀 (𝑚𝑛 , 𝑝𝑛 )                    ∀𝑚 ∈ 𝑀. Correct𝐹𝑣 ,𝑀 (𝑚)
    𝑀 = {𝑚 1, 𝑚 2 , ..., 𝑚𝑛 }    𝑃 = {𝑝 1 , ..., 𝑝𝑛 }                                        
    Rel𝐺𝐹,𝑀 (𝑚, 𝑝) , Correct𝐺 𝑏
                                (𝑝) ⇒ SpecWf(𝑚) ∧ (∀𝑚 ′ ∈ 𝑀. SpecWf(𝑚 ′ )) ⇒ Correct𝐹𝑣 ,𝑀 (𝑚)
                                        | {z } |                    {z                       }
                                                (C1)                                         (C2)


Fig. 10. Proof strategy for the Viper-to-Boogie translation. First, a proof is generated relating each Viper
method with the corresponding Boogie procedure. Second, the final proof is deduced. 𝐹 denotes the Viper
fields, 𝐺 denotes the global constants, variables, Boogie axioms, and functions emitted by the translation.



fail. As planned, we obtain this result via a forward simulation proof between the executed Viper
statement and 𝑝 (𝑚)’s procedure body using our presented methodology. Formally, we show:

                                     ∃𝑅 ′ , 𝛾 ′ . stmSimΓ𝑣0 ,Γ0 (𝑅0 , 𝑅 ′ , 𝑠 𝑣0, init𝑏 (𝑝 (𝑚)), 𝛾 ′ )
                                                               𝑏

                         where 𝑠 𝑣0 , inhale pre(𝑚); body(𝑚); exhale post(𝑚)

In the statement above, Γ𝑣0 , initCtxt𝑀,𝐹                                           0
                                           𝑣 (𝑚) is the initial Viper context. Γ𝑏 is a Boogie context
that is deﬁned in terms of our chosen type and function interpretation (see Sec. 4.4). 𝑅0 is an
instantiation of the state relation shown in Sec. 4.1. init𝑏 (𝑝 (𝑚)) is the initial Boogie program point
in 𝑝 (𝑚). The output state relation and output Boogie program point are irrelevant, since we care
only about the simulation of failing Viper executions here. To complete the proof, we choose an
initial Boogie state 𝜎𝑏 such that 𝑅0 (𝜎 𝑣 , 𝜎𝑏 ). As a result, if a Viper execution 𝐸 𝑣 of statement 𝑠 𝑣0 in
𝜎 𝑣 fails, the forward simulation provides us with a failing Boogie execution 𝐸𝑏 of 𝑝 (𝑚). Using the
correctness of 𝑝 (𝑚), we conclude that 𝐸𝑏 cannot fail, and thus conclude that 𝐸 𝑣 cannot fail, which
concludes the proof of Rel𝐺𝐹,𝑀 (𝑚, 𝑝 (𝑚)).

5   IMPLEMENTATION AND EVALUATION
We instrumented the existing Viper veriﬁer implementation to automatically produce an Isabelle
proof justifying the soundness of its translation to Boogie, and evaluated this validation on a di-
verse set of Viper benchmarks.

   Implementation. Even though Viper passes the generated Boogie program to Boogie as a text
ﬁle, our soundness proof directly connects the input Viper AST to the internal AST representation
of the Boogie veriﬁer. Therefore, we do not have to trust the Boogie parser.
   We make the following four adjustments to the Viper veriﬁer implementation. First, we desugar
the uses of polymorphic maps as described in Sec. 4.4, since there is no formal model for polymor-
phic maps. Second, we adjust the implementation to not emit Boogie declarations or commands
that are used only for features outside of our subset (the implementation always emits those with-
out checking whether the corresponding features are actually used). Third, we switch oﬀ simple
syntactic transformations that the Viper veriﬁer applies to the produced Boogie program (e.g. con-
stant folding, elimination of if-statements with no branches), since we do not support them yet;
justifying those transformations should be straightforward and is orthogonal to our work. Fourth,
we introduce a havoc statement in the Boogie program at the point when a scoped Viper variable
208:20           Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


Table 1. Overview of benchmarks and results. For each test suite, we report the number of Viper files, the
total number of Viper methods contained in those files, as well as the mean number of non-empty lines of
code for the Viper files, Boogie files, and produced Isabelle proofs. We measured the mean and median time
it took to check the Isabelle proofs in seconds.


    Test suite     Files   Methods          Viper          Boogie        Isabelle         Proof Check
                     no.        no.     Mean [LoC]      Mean [LoC]     Mean [LoC]      Mean [s] Median [s]
    Viper            34          105              33            298            1719         33.8          23.8
    Gobra            17           65              60            287            1937         32.7          25.3
    VerCors          18          116              63            332            2930         43.1          40.9
    MPP               3           13             206           1060            5164        109.0          46.2
    Overall          72          299              54            335            2217         39.0          32.9




is introduced, which faithfully models the semantics of such a variable. The original Viper imple-
mentation instead just introduces a fresh Boogie variable at the beginning of the Boogie procedure.
Proving the equivalence of both translations is straightforward.

   Evaluation. Our evaluation answers the questions: (RQ1) Does our implementation generate
proofs that Isabelle can check successfully for a diverse set of examples? (RQ2) Does Isabelle
check the generated proofs in reasonable time (e.g. feasible as part of continuous integration)?
   To obtain a diverse set of representative examples, we considered the Viper test suite as well as
the test suites of three tools that produce Viper code: Gobra [46] (for Go), VerCors [4] (for Java),
and MPP [15] (a tool performing a modular product transformation on Viper programs). To elim-
inate trivial translations, we focused on Viper programs that use the heap, as indicated by the
occurrence of at least one accessibility predicate. Out of those, we included all Viper programs
that fall into our supported Viper subset. We followed diﬀerent strategies to systematically obtain
additional examples from the diﬀerent test suites. For Viper and MPP, we additionally included all
ﬁles that have an old-expression (by manually removing the corresponding assertion, i.e. verify-
ing weaker postconditions) or a new statement (by manually desugaring the allocation primitive
into our subset). Moreover, we made sure that each argument to a method call is a variable (e.g.
we rewrote m(i+1) to var t := i+1; m(t)), since we currently support only variables as ar-
guments. For Gobra and VerCors, we removed boilerplate code that is emitted for each ﬁle and
then followed the same process as for Viper and MPP. Moreover, we additionally included ﬁles
generated by Gobra that had at most two occurrences of features outside of our subset if those
could be desugared into our subset (e.g. by eliminating a function by inlining its body).
   As summarised in Tab. 1, we collected a total of 72 Viper ﬁles (containing 299 methods), with a
mean of 54 and maximum of 414 non-empty lines of code. We ran our implementation on all 72
Viper ﬁles to generate the Boogie translations and the Isabelle proofs, and measured the time it
took for Isabelle to check the generated proofs (the mean of ﬁve repetitions). The measurements
were run on a ThinkPad X1 Yoga Gen 5 on Ubuntu 20.04 with 16 GB RAM and i7-10510U @ 1.8 GHz
(scaled up to 4.9 GHz using Turbo Boost). The generated Boogie translations are on average 6.2x
larger (335 non-empty LoC on average), illustrating the semantic gap between Viper and Boogie.
   Isabelle successfully checked the generated proofs for all Viper ﬁles, including the Viper pro-
grams automatically generated by other tools. This shows that our approach is eﬀective for practi-
cal veriﬁers and answers RQ1 positively. The resulting Isabelle proofs have on average over 2000
lines and are checked in less than a minute.
Formally Validating Translations into an Intermediate Verification Language                                        208:21


Table 2. Detailed results of our evaluation for a selection of files showing the number of methods, the
nonempty lines of code for the Viper program, Boogie program, and produced Isabelle proof, and the time
it took to check the proof in seconds.


      Test suite   File                    Methods          Viper        Boogie         Isabelle   Proof Check
                                                no.    Total [LoC]   Total [LoC]     Total [LoC]       Total [s]
      Viper        testHistoryProcesses           13           205            1711         7035            126.3
      Gobra        defer-simple-02                 9           211             853         4717             60.6
      VerCors      inv-test-fail2                  5            92             514         2596             56.5
      MPP          banerjee                        8           414            2014         9545            242.4
      MPP          darvas                          2            91             582         2800             38.4
      MPP          kusters                         3           112             583         3146             46.2



   Tab. 2 shows the results for a selection of examples (the detailed results for each test suite are
shown in App. D): All three examples from MPP, as well as the largest example (in terms of lines of
Viper code) from each of the other test suites. The three MPP examples are drawn from diﬀerent
research papers and show that our tool can certify challenging programs.
   For this selection, the times to check the proofs range from 38 seconds to 4 minutes. No ﬁle
in any of the 72 ﬁles takes longer than 4 minutes to check. These times are acceptable, since we
expect the validation to be performed occasionally (in particular, before the veriﬁed program is
released or as part of continuous integration), but not on every run of the veriﬁer. Thus, we answer
RQ2 positively for the considered 72 ﬁles. To obtain additional representative ﬁles from the test
suites, we would need to extend the supported Viper subset. Moreover, most of our proofs are not
yet optimised to make proof checking faster. For example, ﬁeld and variable accesses currently
result in an overhead in the proof that is proportional to the number of ﬁelds and active variables,
respectively. This could be improved by constructing and updating lookup tables eﬃciently.

6   RELATED WORK
Various works prove the soundness of front-end translations once and for all. For instance, Lehner
and Müller [27] prove a simpliﬁed translation from Java Bytecode to Boogie, and Vogels et al. [43]
target a translation from a toy object-oriented programming language to Boogie. Both proofs are
done on paper and do not consider an actual implementation of the translation. Backes et al. [3]
prove a translation sound from the Dminor data processing language to the Bemol IVL in Coq.
They do not provide a proof connecting the formalised translation to their F# implementation.
Herms [21] proves a translation from C to the WhyCert IVL (inspired by the Why3 IVL) sound in
Coq, which they then turn into an executable tool via Coq’s extraction to OCaml. The resulting tool
has similarities to the Jessie Frama-C implementation [33], which translates C programs to Why3;
Herms [21] discusses mismatches between their mechanisation and the Jessie implementation.
In contrast, our certiﬁcation applies to existing front-end implementations, which are typically
implemented in eﬃcient mainstream programming languages, use diverse libraries, and include
subtle optimisations omitted from idealised implementations. Smans et al. [40] prove soundness
of a veriﬁcation condition generator for a language with implicit dynamic frames (IDF) assertions
once and for all on paper without using an IVL. They also implement a prototype, but do not
formally connect the proof to the implementation. We also applied our methodology to a veriﬁer
based on IDF, but validate an actual implementation.
   Many veriﬁers perform a series of program transformations, e.g. by translating programs to
a lower-level IVL or internally without changing the language (e.g. monomorphisation). Our ap-
proach can in principle be applied to both kinds of transformations, but is tailored towards the
208:22        Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


former, where the semantic gap is large, non-local checks arise, and diverse translations are used.
Existing work for the validation of internal transformations does not provide solutions for these
challenges. For instance, our prior work [38] validates the veriﬁcation condition (VC) generation
implementation of Boogie programs (also via a proof-producing instrumentation), which includes
internal Boogie-to-Boogie transformations. In these transformations, the semantic gap is small
(the source and target constructs are largely the same), and thus the decomposition into smaller
problems is immediate, while in this paper the decomposition is a challenge. Moreover, our prior
work need not deal with non-local checks and diverse translations. Our prior work uses diﬀerent
kinds of simulations; it would be interesting future work to apply our methodology to these. Be-
sides internal transformations, our prior work connects the VC and a Boogie program; this paper
considers only program-to-program transformations. Our prior work can in principle be combined
with this paper to enable end-to-end soundness guarantees for Viper, but requires extending the
Boogie veriﬁer validation to more internal Boogie transformations and to a larger Boogie subset.
   Validation has also been used to obtain formal guarantees for implementations of other veriﬁers,
but none of the existing works target front-end translations and the challenges they entail. Lin et al.
[31] and Wils and Jacobs [44] validate veriﬁers obtained via the K framework and VeriFast, respec-
tively. These veriﬁers use symbolic execution, which requires a fundamentally diﬀerent validation
approach. Garchery [19] validates certain logical transformations in Why3. Cohen and Johnson-
Freyd [9] also prove such logical transformations, but do so once and for all in Coq to demonstrate
their Why3 mechanisation. Neither of the two consider the actual VC generation.
   Multiple works also embed programs in an interactive theorem prover (ITP) and then automate
forward simulation proofs. Rizkallah et al. [39] deﬁne a reﬁnement calculus for the Cogent com-
piler to automatically prove a forward simulation in Isabelle for a Cogent expression and its C
translation. Their calculus includes syntax-directed rules for deriving simulation judgements, but
these rules do not provide the abstraction we needed to handle diverse translations. The compiler
was developed with validation in mind, which simpliﬁes, for instance, the treatment of optimisa-
tions. In contrast, our goal was to validate existing veriﬁer implementations with all their intrica-
cies. The veriﬁcation of the seL4 kernel includes two large forward simulation proofs in Isabelle,
for which proof automation was developed [8, 24, 45]. This automation reduces the manual proof
overhead, but still requires user interaction. In contrast, our validation proofs are generated and
checked completely automatically. Like us, they prove rules to decompose the simulation for com-
posite statements syntactically but, contrary to us, do not decompose statements semantically into
smaller simulations. They turn certain simulation judgements into Hoare triples for which they
have separate automation.
   Formal translation validation approaches for compilers express a per-run validator in an ITP [20,
41, 42], prove it correct once and for all, and then extract executable code (the extraction must be
trusted). For many of these validators, the source and target languages are similar. It would be in-
teresting to test the feasibility of such approaches for front-end translations, where the semantic
gap between the languages is large. Another diﬀerence is that front-end translations incorporate
reasoning steps, such as assumptions and proof obligations prescribed by a program logic. This
encoding is achieved via components not present in executable languages such as assume state-
ments, havoc statements, and axiomatisations. Moreover, front-end translations emit code that
checks nontrivial properties that are then relied upon in other parts of the encoding.
   Zimmerman et al. [47] deﬁne a formal Viper semantics for a Viper subset in order to prove
formal results for the gradual veriﬁer Gradual C0 that uses Viper. However, in contrast to ours,
their formalisation is not mechanised. Boogie developers have added an option to monomorphise
polymorphic maps in Boogie programs via non-polymorphic maps [11]. This option provides an
alternative to ours for desugaring polymorphic maps, which, in the case of Viper, circumvents
Formally Validating Translations into an Intermediate Verification Language                                         208:23


the circularity challenge discussed in Sec. 4.4, since Viper does not permit storing heaps in ﬁelds.
However, in general, front-ends may permit storing heaps in ﬁelds.

7   CONCLUSION
We presented a methodology for the validation of the front-end translations implemented in prac-
tical automated program veriﬁers. We demonstrated that it handles the complexity and intricacies
of the Viper-to-Boogie translation as implemented in the Viper tool. To the best of our knowledge,
this is the ﬁrst formal soundness guarantee for a practical front-end translation. Together with
existing work on back-end (and SMT) validation, our work provides a path towards trustworthy
automated veriﬁers. Two fundamental requirements of our approach are the existence of a formal
semantics for the input language and IVL, and the ability to instrument the veriﬁer implementa-
tion. As future work, we plan to extend the supported Viper subset and to apply our methodology
to veriﬁers that target Viper as an IVL and that verify, for instance, concurrent or object-oriented
programs.

ACKNOWLEDGMENTS
We thank Aleksandar Hubanov for work on embedding the Boogie AST in Isabelle, Marco Eilers for
helping with the modular product program tool, João C. Pereira and Felix A. Wolf for helping with
the Gobra veriﬁer, Xavier Denis for clariﬁcations on Why3 and Michael Sammler for feedback on
our formalisation. We thank the anonymous reviewers for their comments. This work was partially
funded by the Swiss National Science Foundation (SNSF) under Grant No. 197065.

DATA AVAILABILITY STATEMENT
Our publicly-available artifact [37] contains:
   (1) an Isabelle formalisation for the technical results in Sec. 2, Sec. 3, and Sec. 4.
   (2) our proof-producing Viper-to-Boogie implementation, which generates, on every run of
       the veriﬁer, an Isabelle proof showing that the correctness of the input Viper program is
       implied by the correctness of the corresponding Boogie translation.
   (3) the examples used in the evaluation, and scripts for the benchmark selection and evaluation
       results (Sec. 5).

REFERENCES
 [1] Andrew W. Appel and Sandrine Blazy. 2007. Separation Logic for Small-Step cminor. In Theorem Proving in
     Higher Order Logics, 20th International Conference, TPHOLs 2007, Kaiserslautern, Germany, September 10-13, 2007,
     Proceedings (Lecture Notes in Computer Science, Vol. 4732), Klaus Schneider and Jens Brandt (Eds.). Springer, 5–21.
     https://doi.org/10.1007/978-3-540-74591-4_3
 [2] Vytautas Astrauskas, Peter Müller, Federico Poli, and Alexander J. Summers. 2019. Leveraging Rust Types
     for Modular Speciﬁcation and Veriﬁcation. Proc. ACM Program. Lang. 3, OOPSLA, Article 147, 30 pages.
     https://doi.org/10.1145/3360573
 [3] Michael Backes, Catalin Hritcu, and Thorsten Tarrach. 2011. Automatically Verifying Typing Constraints for a
     Data Processing Language. In Certiﬁed Programs and Proofs (CPP), Jean-Pierre Jouannaud and Zhong Shao (Eds.).
     https://doi.org/10.1007/978-3-642-25379-9_22
 [4] Stefan Blom, Saeed Darabi, Marieke Huisman, and Wytse Oortwijn. 2017. The VerCors Tool Set: Veriﬁcation of
     Parallel and Concurrent Software. In Integrated Formal Methods (IFM), Nadia Polikarpova and Steve Schneider (Eds.).
     https://doi.org/10.1007/978-3-319-66845-1_7
 [5] Sascha Böhme and Tjark Weber. 2010. Fast LCF-Style Proof Reconstruction for Z3. In Interactive Theorem Proving
     (ITP), Matt Kaufmann and Lawrence C. Paulson (Eds.). https://doi.org/10.1007/978-3-642-14052-5_14
 [6] John Boyland. 2003. Checking Interference with Fractional Permissions. In Static Analysis (SAS), Radhia Cousot (Ed.).
     55–72. https://doi.org/10.1007/3-540-44898-5_4
 [7] Montgomery Carter, Shaobo He, Jonathan Whitaker, Zvonimir Rakamaric, and Michael Emmi. 2016. SMACK software
     veriﬁcation toolchain. In Proceedings of the 38th International Conference on Software Engineering, ICSE 2016, Austin,
208:24          Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


     TX, USA, May 14-22, 2016 - Companion Volume, Laura K. Dillon, Willem Visser, and Laurie A. Williams (Eds.). ACM,
     589–592. https://doi.org/10.1145/2889160.2889163
 [8] David A. Cock, Gerwin Klein, and Thomas Sewell. 2008. Secure Microkernels, State Monads and Scalable Reﬁnement.
     In Theorem Proving in Higher Order Logics (TPHOLS), Otmane Aït Mohamed, César A. Muñoz, and Soﬁène Tahar
     (Eds.). https://doi.org/10.1007/978-3-540-71067-7_16
 [9] Joshua M. Cohen and Philip Johnson-Freyd. 2024. A Formalization of Core Why3 in Coq. Proc. ACM Program. Lang.
     8, POPL, Article 60 (jan 2024), 30 pages. https://doi.org/10.1145/3632902
[10] Xavier Denis, Jacques-Henri Jourdan, and Claude Marché. 2022. Creusot: A Foundry for the Deductive Veriﬁcation
     of Rust Programs. In International Conference on Formal Engineering Methods (ICFEM), Adrián Riesco and Min Zhang
     (Eds.), Vol. 13478. 90–105. https://doi.org/10.1007/978-3-031-17244-1_6
[11] Boogie       developers.    2022.              Monomorphization       of    polymorphic    maps      and    binders.
     https://github.com/boogie-org/boogie/pull/669 Accessed March 19, 2024.
[12] Viper developers. 2024. Viper-to-Boogie implementation. https://github.com/viperproject/carbon Accessed April 4,
     2024.
[13] Jenna DiVincenzo, Ian McCormack, Hemant Gouni, Jacob Gorenburg, Mona Zhang, Conrad Zimmerman, Joshua
     Sunshine, Éric Tanter, and Jonathan Aldrich. 2022. Gradual C0: Symbolic Execution for Eﬃcient Gradual Veriﬁcation.
     CoRR abs/2210.02428 (2022). https://doi.org/10.48550/ARXIV.2210.02428 arXiv:2210.02428
[14] Marco Eilers and Peter Müller. 2018. Nagini: A Static Veriﬁer for Python. In Computer Aided Veriﬁcation (CAV), Hana
     Chockler and Georg Weissenbacher (Eds.). https://doi.org/10.1007/978-3-319-96145-3_33
[15] Marco Eilers, Peter Müller, and Samuel Hitz. 2018. Modular Product Programs. In European Symposium on Program-
     ming (ESOP), Amal Ahmed (Ed.). https://doi.org/10.1007/978-3-319-89884-1_18
[16] Burak Ekici, Alain Mebsout, Cesare Tinelli, Chantal Keller, Guy Katz, Andrew Reynolds, and Clark W. Barrett. 2017.
     SMTCoq: A Plug-In for Integrating SMT Solvers into Coq. In Computer Aided Veriﬁcation (CAV), Rupak Majumdar
     and Viktor Kuncak (Eds.). https://doi.org/10.1007/978-3-319-63390-9_7
[17] Jean-Christophe Filliâtre and Andrei Paskevich. 2013.                 Why3 — Where Programs Meet Provers.
     In European Symposium on Programming (ESOP), Matthias Felleisen and Philippa Gardner (Eds.).
     https://doi.org/10.1007/978-3-642-37036-6_8
[18] Mathias Fleury and Hans-Jörg Schurr. 2019. Reconstructing veriT Proofs in Isabelle/HOL. In Workshop on Proof
     eXchange for Theorem Proving (PxTP), Giselle Reis and Haniel Barbosa (Eds.). https://doi.org/10.4204/EPTCS.301.6
[19] Quentin Garchery. 2021. A Framework for Proof-carrying Logical Transformations. In Workshop on Proof eXchange
     for Theorem Proving (PxTP), Chantal Keller and Mathias Fleury (Eds.). https://doi.org/10.4204/EPTCS.336.2
[20] Léo Gourdin, Benjamin Bonneau, Sylvain Boulmé, David Monniaux, and Alexandre Bérard. 2023. Formally Verifying
     Optimizations with Block Simulations. Proc. ACM Program. Lang. 7, OOPSLA2, Article 224 (oct 2023), 30 pages.
     https://doi.org/10.1145/3622799
[21] Paolo Herms. 2013.         Certiﬁcation of a Tool Chain for Deductive Program Veriﬁcation. (Certiﬁcation d’une
     chaine de vériﬁcation déductive de programmes). Ph. D. Dissertation. University of Paris-Sud, Orsay, France.
     https://tel.archives-ouvertes.fr/tel-00789543
[22] Ioannis T. Kassios. 2006. Dynamic Frames: Support for Framing, Dependencies and Sharing Without Restrictions. In
     Formal Methods (FM), Jayadev Misra, Tobias Nipkow, and Emil Sekerinski (Eds.). https://doi.org/10.1007/11813040_19
[23] Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris Yakobowski. 2015.
     Frama-C: A software analysis perspective.                Formal Aspects of Computing 27, 3 (2015), 573–609.
     https://doi.org/10.1007/s00165-014-0326-7
[24] Gerwin Klein, Thomas Sewell, and Simon Winwood. 2010. Reﬁnement in the Formal Veriﬁcation of the seL4 Micro-
     kernel. In Design and Veriﬁcation of Microprocessor Systems for High-Assurance Applications, David S. Hardin (Ed.).
     Springer, 323–339. https://doi.org/10.1007/978-1-4419-1539-9_11
[25] Shuvendu K. Lahiri, Chris Hawblitzel, Ming Kawaguchi, and Henrique Rebêlo. 2012. SYMDIFF: A Language-Agnostic
     Semantic Diﬀ Tool for Imperative Programs. In Computer Aided Veriﬁcation - 24th International Conference, CAV 2012,
     Berkeley, CA, USA, July 7-13, 2012 Proceedings (Lecture Notes in Computer Science, Vol. 7358), P. Madhusudan and
     Sanjit A. Seshia (Eds.). Springer, 712–717. https://doi.org/10.1007/978-3-642-31424-7_54
[26] Akash Lal and Shaz Qadeer. 2014. Powering the static driver veriﬁer using corral. In Proceedings of the 22nd
     ACM SIGSOFT International Symposium on Foundations of Software Engineering, (FSE-22), Hong Kong, China, No-
     vember 16 - 22, 2014, Shing-Chi Cheung, Alessandro Orso, and Margaret-Anne D. Storey (Eds.). ACM, 202–212.
     https://doi.org/10.1145/2635868.2635894
[27] Hermann Lehner and Peter Müller. 2007. Formal Translation of Bytecode into BoogiePL. Electronic Notes in Theoretical
     Computer Science 190, 1 (2007), 35–50. https://doi.org/10.1016/j.entcs.2007.02.059 Workshop on Bytecode Semantics,
     Veriﬁcation, Analysis and Transformation (Bytecode 2007).
Formally Validating Translations into an Intermediate Verification Language                                          208:25


[28] K. Rustan M. Leino. 2008.                       This is Boogie 2. (2008).                             Available from
     http://research.microsoft.com/en-us/um/people/leino/papers/krml178.pdf .
[29] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Veriﬁer for Functional Correctness. In Logic for
     Programming, Artiﬁcial Intelligence, and Reasoning (LPAR), Edmund M. Clarke and Andrei Voronkov (Eds.).
     https://doi.org/10.1007/978-3-642-17511-4_20
[30] K. Rustan M. Leino and Philipp Rümmer. 2010. A Polymorphic Intermediate Veriﬁcation Language: Design and
     Logical Encoding. In Tools and Algorithms for the Construction and Analysis of Systems (TACAS), Javier Esparza and
     Rupak Majumdar (Eds.). https://doi.org/10.1007/978-3-642-12002-2_26
[31] Zhengyao Lin, Xiaohong Chen, Minh-Thai Trinh, John Wang, and Grigore Rosu. 2023. Generating Proof Certiﬁ-
     cates for a Language-Agnostic Deductive Program Veriﬁer. Proc. ACM Program. Lang. 7, OOPSLA1 (2023), 56–84.
     https://doi.org/10.1145/3586029
[32] Nancy A. Lynch and Frits W. Vaandrager. 1995. Forward and Backward Simulations: I. Untimed Systems. Inf. Comput.
     121, 2 (1995), 214–233. https://doi.org/10.1006/inco.1995.1134
[33] Claude Marché and Yannick Moy. 2018.                The Jessie plugin for Deductive Veriﬁcation in Frama-C.
     http://krakatoa.lri.fr/jessie.pdf
[34] Peter Müller, Malte Schwerhoﬀ, and Alexander J. Summers. 2016. Viper: A Veriﬁcation Infrastructure for Permission-
     Based Reasoning. In Veriﬁcation, Model Checking, and Abstract Interpretation (VMCAI), Barbara Jobstmann and K. Rus-
     tan M. Leino (Eds.). https://doi.org/10.1007/978-3-662-49122-5_2
[35] Tobias Nipkow, Lawrence C. Paulson, and Markus Wenzel. 2002. Isabelle/HOL - A Proof Assistant for Higher-Order
     Logic. Lecture Notes in Computer Science, Vol. 2283. Springer. https://doi.org/10.1007/3-540-45949-9
[36] Matthew J. Parkinson and Alexander J. Summers. 2012. The Relationship Between Separation Logic and Implicit
     Dynamic Frames. Logical Methods in Computer Science 8, 3:01 (2012), 1–54. https://doi.org/10.2168/LMCS-8(3:1)2012
[37] Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers. 2024. Towards
     Trustworthy Automated Program Veriﬁers: Formally Validating Translations into an Intermediate Veriﬁcation Language
     – Artifact. https://doi.org/10.5281/zenodo.10802176
[38] Gaurav Parthasarathy, Peter Müller, and Alexander J. Summers. 2021. Formally Validating a Practical Veriﬁcation
     Condition Generator. In Computer Aided Veriﬁcation (CAV) (LNCS, Vol. 12760), Alexandra Silva and K. Rustan M.
     Leino (Eds.). 704–727. https://doi.org/10.1007/978-3-030-81688-9_33
[39] Christine Rizkallah, Japheth Lim, Yutaka Nagashima, Thomas Sewell, Zilin Chen, Liam O’Connor, Toby C. Mur-
     ray, Gabriele Keller, and Gerwin Klein. 2016. A Framework for the Automatic Formal Veriﬁcation of Reﬁnement
     from Cogent to C.. In Interactive Theorem Proving (ITP), Jasmin Christian Blanchette and Stephan Merz (Eds.).
     https://doi.org/10.1007/978-3-319-43144-4_20
[40] Jan Smans, Bart Jacobs, and Frank Piessens. 2012. Implicit Dynamic Frames. Transactions on Programming Languages
     and Systems (TOPLAS) 34, 1, Article 2 (May 2012), 58 pages. https://doi.org/10.1145/2160910.2160911
[41] Jean-Baptiste Tristan and Xavier Leroy. 2008. Formal veriﬁcation of translation validators: a case study on instruction
     scheduling optimizations. In Principles of Programming Languages (POPL), George C. Necula and Philip Wadler (Eds.).
     https://doi.org/10.1145/1328438.1328444
[42] Jean-Baptiste Tristan and Xavier Leroy. 2009. Veriﬁed validation of lazy code motion. In Programming Language
     Design and Implementation (PLDI), Michael Hind and Amer Diwan (Eds.). https://doi.org/10.1145/1542476.1542512
[43] Frédéric Vogels, Bart Jacobs, and Frank Piessens. 2009. A Machine Checked Soundness Proof for an Intermedi-
     ate Veriﬁcation Language. In Theory and Practice of Computer Science, Conference on Current Trends in Theory and
     Practice of Computer Science (SOFSEM) (Lecture Notes in Computer Science, Vol. 5404), Mogens Nielsen, Antonín
     Kucera, Peter Bro Miltersen, Catuscia Palamidessi, Petr Tuma, and Frank D. Valencia (Eds.). Springer, 570–581.
     https://doi.org/10.1007/978-3-540-95891-8_51
[44] Stefan Wils and Bart Jacobs. 2023. Certifying C program correctness with respect to CH2O with VeriFast. CoRR
     abs/2308.15567 (2023). https://doi.org/10.48550/ARXIV.2308.15567 arXiv:2308.15567
[45] Simon Winwood, Gerwin Klein, Thomas Sewell, June Andronick, David A. Cock, and Michael Norrish. 2009. Mind
     the Gap. In Theorem Proving in Higher Order Logics (TPHOLS), Stefan Berghofer, Tobias Nipkow, Christian Urban, and
     Makarius Wenzel (Eds.). https://doi.org/10.1007/978-3-642-03359-9_34
[46] Felix A. Wolf, Linard Arquint, Martin Clochard, Wytse Oortwijn, João Carlos Pereira, and Peter Müller. 2021. Gobra:
     Modular Speciﬁcation and Veriﬁcation of Go Programs. In Computer Aided Veriﬁcation (CAV), Alexandra Silva and
     K. Rustan M. Leino (Eds.). https://doi.org/10.1007/978-3-030-81685-8_17
[47] Conrad Zimmerman, Jenna DiVincenzo, and Jonathan Aldrich. 2024. Sound Gradual Veriﬁcation with Symbolic
     Execution. Proc. ACM Program. Lang. 8, POPL (2024), 2547–2576. https://doi.org/10.1145/3632927
208:26            Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


                                                      h𝑒, 𝜎 𝑣 i ⇓ V(𝑟 ) h𝑒𝑝 , 𝜎 𝑣 i ⇓ V(𝑝)
                                                                 𝑝 < 0 ⇒ 𝑟𝑣 = F
         h𝐴, 𝜎 𝑣 i →inh 𝑟 𝑣
                                  (inh)        𝑝 ≥ 0 ⇒ 𝑟 𝑣 = if inhSucc(r, p) then N(𝜎 𝑣′ ) else M
Γ𝑣 ⊢ hinhale 𝐴, 𝜎 𝑣 i →v 𝑟 𝑣                              𝜎 𝑣′ = addperm(𝜎 𝑣 , 𝑟 , 𝑓 , 𝑝)
                                                                                                            (inh-acc)
                                                            hacc (𝑒.𝑓 , 𝑒𝑝 ), 𝜎 𝑣 i →inh 𝑟 𝑣

 h𝐴, 𝜎 𝑣 i →inh N(𝜎 𝑣′ )                                                              h𝐴, 𝜎 𝑣 i →inh F
   h𝐵, 𝜎 𝑣′ i →inh 𝑟 𝑣                                                                                     (inh-sep-f)
                              (inh-sep-s)                                           h𝐴 ∗ 𝐵, 𝜎 𝑣 i →inh F
 h𝐴 ∗ 𝐵, 𝜎 𝑣 i →inh 𝑟 𝑣


                inhSucc(𝑟 , 𝑝) , (𝑝 > 0 ⇒ 𝑟 ≠ null) ∧ (𝑟 ≠ null ⇒ 𝑝 + 𝜋 (𝜎 𝑣 ) (𝑟 , 𝑓 ) ≤ 1)

Fig. 11. A subset of the rules for the formal semantics of inhale. addperm(𝜎𝑣 , 𝑟, 𝑓 , 𝑝) denotes the state 𝜎𝑣
where permission 𝑝 has been added to (𝑟, 𝑓 ).


A INHALE SEMANTICS
The reduction of inhale 𝐴 for an assertion 𝐴 from state 𝜎 𝑣 to outcome 𝑟 𝑣 is expressed via the
judgement h𝐴, 𝜎 𝑣 i →inh 𝑟 𝑣 . The rule inh in Fig. 11 converts such a judgement into the standard
statement reduction judgement. The rules for the separating conjunction and the accessibility
predicate (when the receiver and permission are well-deﬁned) are shown in Fig. 11. In the case
of the accessibility predicate, there is an additional rule where the inhale fails if 𝑒 or 𝑒𝑝 are not
well-deﬁned, which is not shown in the ﬁgure.
    The accessibility predicate rule inh-acc shown in Fig. 11 expresses that if the added permission
is negative then the operation fails. If the permission is nonnegative, then the operation succeeds
if (1) the receiver is non-null if 𝑝 > 0, and (2) the added permission does not yield an inconsistent
state (i.e. does not result in more than 1 permission for (𝑟 , 𝑓 )). Otherwise, the operation stops
(denoted by outcome M). If the operation succeeds, then the new state additionally contains the
added permission 𝑝 at location (𝑟 , 𝑓 ).

B ANOTHER SIMULATION RULE EXAMPLE
Consider the rule racc-sim in Fig. 12, which decomposes the simulation of remcheck acc (𝑒.𝑓 , 𝑒𝑝 )
(ignore the universal quantiﬁers for now) into the simulation of three separate Viper eﬀects: (1) the
check of well-deﬁnedness of the receiver 𝑒 and permission expression 𝑒𝑝 (via the wfSim instan-
tiation from Fig. 4), (2) a check exhAccSucc ensuring that the operation will not fail (from the
semantics; see Fig. 2), and (3) the actual update of the Viper state, which removes the permission.
   The second premise includes contextual information, namely the conjunct wfAccSucc express-
ing that 𝑒 and 𝑒𝑝 are well-deﬁned (which is ensured by the ﬁrst premise) and evaluate to the
reference value 𝑟 and permission value 𝑝. The third premise modelling the removal of the permis-
sion includes the same conjunct and that the operation will succeed (exhAccSucc). Without the
latter, we could in general not prove that the resulting Boogie state satisﬁes crucial invariants, for
instance, that none of the permissions stored in the Boogie state are negative. Again, we are ag-
nostic as to syntactically how this is achieved by this check: our rule does not require the Boogie
program to emit an explicit Boogie assert command checking that the permission is nonnegative.
This is important, since the implementation omits such a command, for example, if the permission
is the literal 1.
Formally Validating Translations into an Intermediate Verification Language                                              208:27


       ∀𝜎 𝑣 . wfSimΓ𝑏 (𝑅ˆ (𝜎 𝑣 ), 𝑅ˆ𝐴 (𝜎 𝑣 ), [𝑒, 𝑒𝑝 ], 𝛾, 𝛾 1 ) (subexpression well-deﬁnedness)
       ∀𝑟 , 𝑝. simΓ𝑏 (𝑅𝐴 , 𝑅𝐵 (𝑟 , 𝑝), Succ𝐴 (𝑟 , 𝑝), Fail𝐴 (𝑟 , 𝑝), 𝛾 1, 𝛾 2 ) (non-failure check)
              ∀𝑟 , 𝑝. simΓ𝑏 (𝑅𝐵 (𝑟 , 𝑝), 𝑅 ′ , Succ 𝐵 (𝑟 , 𝑝), (𝜆_. ⊥), 𝛾 2, 𝛾 ′ ) (state update)
                                                                                                                  (racc-sim)
                                    rcSimΓ𝑏 (𝑅, 𝑅 ′ , acc (𝑒.𝑓 , 𝑒𝑝 ), 𝛾, 𝛾 ′ )

    ˆ 𝑣 ) , 𝜆𝜎 𝑣0 𝜎𝑏 . 𝑅((𝜎 𝑣0 , 𝜎 𝑣 ), 𝜎𝑏 ) 𝑅ˆ𝐴 (𝜎 𝑣 ) , 𝜆𝜎 𝑣0 𝜎𝑏 . 𝑅𝐴 ((𝜎 𝑣0, 𝜎 𝑣 ), 𝜎𝑏 )
    𝑅(𝜎
                                                                                                        
                         0              1 ′     exhAccSucc(𝑟 , 𝑝, 𝜎 𝑣 ) ∧ (𝜎 𝑣0, 𝜎 𝑣 ) = (𝜎 𝑣1, 𝜎 𝑣′ ) ∧
    Succ𝐴 (𝑟 , 𝑝) , 𝜆(𝜎 𝑣 , 𝜎 𝑣 ) (𝜎 𝑣 , 𝜎 𝑣 ).
                                                wfAccSucc(𝑒, 𝑒𝑝 , 𝑟 , 𝑝, 𝜎 𝑣0 )
    Fail𝐴 (𝑟 , 𝑝) , 𝜆(𝜎 𝑣0, 𝜎 𝑣 ). ¬exhAccSucc(𝑟 , 𝑝, 𝜎 𝑣 ) ∧ wfAccSucc(𝑒, 𝑒𝑝 , 𝑟 , 𝑝, 𝜎 𝑣0 )
                                                                                                           
                                                  𝜎 ′ = rem(𝜎 𝑣 , 𝑟 , 𝑓 , 𝑝) ∧ 𝜎 𝑣0 = 𝜎 𝑣1 ∧
    Succ𝐵 (𝑟 , 𝑝) , 𝜆(𝜎 𝑣0, 𝜎 𝑣 ) (𝜎 𝑣1 , 𝜎 𝑣′ ). 𝑣
                                                  exhAccSucc(𝑟 , 𝑝, 𝜎 𝑣 ) ∧ wfAccSucc(𝑒, 𝑒𝑝 , 𝑟 , 𝑝, 𝜎 𝑣0 )
    wfAccSucc(𝑒, 𝑒𝑝 , 𝑟 , 𝑝, 𝜎 𝑣0 ) , h𝑒, 𝜎 𝑣0 i ⇓ V(𝑟 ) ∧ h𝑒𝑝 , 𝜎 𝑣0 i ⇓ V(𝑝)

Fig. 12. Rule for the simulation of remcheck acc (𝑒.𝑓 , 𝑒𝑝 ). The definition of exhAccSucc is given in Fig. 2.


                                               simΓ𝑏 (𝑅0′ , 𝑅1′ , 𝑆 ′ , 𝐹 ′, 𝛾, 𝛾 ′ )
                 ∀𝜎 𝑣 𝜎𝑏 . 𝑅0 (𝜎 𝑣 , 𝜎𝑏 ) ⇒ 𝑅0′ (𝜎 𝑣 , 𝜎𝑏 ) (weaker input state relation)
                   ∀𝜎 𝑣 𝜎 𝑣′ . 𝑆 (𝜎 𝑣 , 𝜎 𝑣′ ) ⇒ 𝑆 ′ (𝜎 𝑣 , 𝜎 𝑣′ ) (weaker success predicate)
                          ∀𝜎 𝑣 . 𝐹 (𝜎 𝑣 ) ⇒ 𝐹 ′ (𝜎 𝑣 ) (weaker failure predicate)
              ∀𝜎 𝑣 𝜎 𝑣 𝜎𝑏 . (∃𝜎𝑏 . 𝑅0 (𝜎 𝑣 , 𝜎𝑏 )) ⇒ 𝑅1′ (𝜎 𝑣′ , 𝜎𝑏′ ) ⇒ 𝑆 (𝜎 𝑣 , 𝜎 𝑣′ ) ⇒ 𝑅1′′ (𝜎 𝑣′ , 𝜎𝑏′ )
                     ′  ′
                                                                                                                (cons)
                                             simΓ𝑏 (𝑅0, 𝑅1′′ , 𝑆, 𝐹, 𝛾, 𝛾 ′ )

    Fig. 13. An instantiation-independent consequence rule for the generic forward simulation judgement.



   The ﬁrst universal quantiﬁer is technically motivated: it expresses that the simulation must hold
for any reduction state. The other quantiﬁers over reference values 𝑟 and permission values 𝑝 make
the rule more powerful and reusable. They permit the relation 𝑅𝐵 to directly talk about the values
that 𝑒 and 𝑒𝑝 evaluate to as speciﬁed by the success and failure predicates. This is particularly
useful for justifying cases where the simulation of the non-failure check establishes a property on
𝑟 or 𝑝, which is then used in the simulation of the state update. For example, the Viper-to-Boogie
translation stores 𝑝 into an auxiliary variable that is used for both the non-failure check and the
state update.

C     INSTANTIATION-INDEPENDENT CONSEQUENCE RULE
The rule cons in Fig. 13 shows an instantiation-independent consequence rule for the generic
forward simulation judgement. The rule enables proving a simulation judgement by proving a
diﬀerent simulation judgement in the premise where the input state relation, success predicate,
and failure predicate are weakened. The output state relation is potentially adjusted in the premise
as well. Additionally, the ﬁnal premise expresses a condition ensuring that the output state relation
𝑅1′′ in the conclusion will be established for the output states if the initial state relation holds for
the initial states, the adjusted output relation holds on the output states, and the Viper execution
is successful.
208:28          Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


           Table 3. Detailed results of our evaluation for the files from the test suite of Gobra.


         File                 Methods        Viper         Boogie        Isabelle       Proof Check
                              no.            Total [LoC]   Total [LoC]   Total [LoC]    Total [s]
         concurrency          2              24            164           1153            25.3
         defer-simple-01      6              142           639           3344            49.6
         defer-simple-02      9              211           853           4717            60.6
         perm-fail1           15             165           661           6392            66.5
         perm-simple1         9              131           622           4221            50.7
         fail1                3              44            283           1574            31.6
         fail3                2              19            116           1044            23.6
         simple1              2              30            237           1210            28.4
         simple2              1              10            90            672             21.4
         simple3              1              17            186           801             24.6
         global-const-8       6              49            206           2510            33.8
         pointer-identity     1              30            158           731             23.0
         pointer-identity     1              30            158           731             23.1
         000008               1              10            85            672             21.4
         000009               1              16            98            679             21.3
         000039               3              49            178           1410            26.8
         000155               2              39            152           1075            24.3


           Table 4. Detailed results of our evaluation for the files from the test suite of MPP.


            File          Methods      Viper           Boogie        Isabelle       Proof Check
                          no.          Total [LoC]     Total [LoC]   Total [LoC]    Total [s]
            banerjee      8            414             2014          9545            242.4
            darvas        2            91              582           2800            38.4
            kusters       3            112             583           3146            46.2


D DETAILED RESULTS OF THE EVALUATION
The detailed results of the evaluation are shown separately for each of the ﬁles in Tab. 3 (Gobra),
Tab. 4 (MPP), Tab. 5 (VerCors), and Tab. 6 (Viper).
Formally Validating Translations into an Intermediate Verification Language                               208:29


            Table 5. Detailed results of our evaluation for the files from the test suite of VerCors.


          File                  Methods      Viper           Boogie           Isabelle      Proof Check
                                no.          Total [LoC]     Total [LoC]      Total [LoC]   Total [s]
          BasicAssert-e1        6            41              197              2589          35.0
          BasicAssert           6            41              193              2589          35.0
          DafnyIncr             8            60              265              3419          41.6
          DafnyIncrE1           8            57              220              3340          40.2
          permissions           5            39              208              2270          33.1
          inv-test-fail1        5            90              510              2589          55.5
          inv-test-fail2        5            92              514              2596          56.5
          inv-test              5            90              510              2589          55.1
          SwapIntegerFail       8            79              429              3645          49.8
          SwapIntegerPass       8            81              469              3688          53.0
          SwapLong              6            57              277              2725          36.7
          SwapLongTwice         8            81              469              3688          52.1
          SwapLongWrong         8            79              429              3645          48.9
          frame-error-1         5            35              173              2191          32.8
          refute3               6            49              246              2662          34.5
          refute4               6            54              258              2676          35.9
          refute5               6            50              253              2662          35.9
          demo1                 7            60              347              3185          44.6
208:30       Gaurav Parthasarathy, Thibault Dardinier, Benjamin Bonneau, Peter Müller, and Alexander J. Summers


          Table 6. Detailed results of our evaluation for the files from the test suite of Viper.


 File                               Methods      Viper          Boogie         Isabelle       Proof Check
                                    no.          Total [LoC]    Total [LoC]    Total [LoC]    Total [s]
 0004                               1            6              100            729             21.7
 0004-CPG1                          1            6              95             704             21.6
 0005                               1            4              78             665             21.1
 0008                               2            12             241            1396            26.8
 0011                               5            63             902            3284            55.7
 0015                               1            6              92             709             21.4
 0052                               1            7              100            719             21.5
 0063                               6            34             180            2595            35.2
 0072                               1            8              112            770             22.4
 0073                               1            10             132            737             22.2
 0088-1                             1            9              115            751             21.9
 0094                               1            6              91             679             21.2
 0152                               2            14             139            1137            24.5
 0157                               8            47             354            3508            45.1
 0159                               2            13             120            1083            23.8
 0170                               1            8              84             665             21.1
 0177-1                             1            10             102            665             21.4
 0222                               2            13             118            1054            23.9
 0227                               1            5              85             683             21.4
 0324                               1            7              104            704             21.2
 0345                               3            21             165            1463            24.4
 0384                               1            11             127            709             22.0
 assert                             1            7              92             693             21.5
 negative-amounts                   3            21             155            1517            27.4
 old                                6            38             318            2805            37.9
 swap                               2            16             177            1239            25.6
 test                               1            6              81             663             20.9
 testHistoryProcesses               13           205            1711           7035            126.3
 testHistoryProcessesPVL            13           204            1711           7035            116.3
 testHistoryProcessesPVL-CPG1       4            56             490            2304            46.1
 testHistoryThreadsProcessesPVL     4            56             490            2304            45.7
 test-example1                      4            57             374            2152            37.0
 test-example3                      5            74             430            2634            39.3
 test-example4                      5            71             451            2645            42.7
