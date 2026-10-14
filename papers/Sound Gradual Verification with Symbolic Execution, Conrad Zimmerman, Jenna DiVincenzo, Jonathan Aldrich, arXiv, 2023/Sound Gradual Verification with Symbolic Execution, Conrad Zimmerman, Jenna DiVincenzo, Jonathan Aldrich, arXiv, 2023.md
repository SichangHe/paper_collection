                                         Sound Gradual Verification with Symbolic Execution∗
                                         CONRAD ZIMMERMAN, Brown University, USA
arXiv:2311.07559v1 [cs.PL] 13 Nov 2023



                                         JENNA DIVINCENZO, Purdue University, USA
                                         JONATHAN ALDRICH, Carnegie Mellon University, USA
                                         Gradual veriﬁcation, which supports explicitly partial speciﬁcations and veriﬁes them with a combination of
                                         static and dynamic checks, makes veriﬁcation more incremental and provides earlier feedback to developers.
                                         While an abstract, weakest precondition-based approach to gradual veriﬁcation was previously proven sound,
                                         the approach did not provide suﬃcient guidance for implementation and optimization of the required run-
                                         time checks. More recently, gradual veriﬁcation was implemented using symbolic execution techniques, but
                                         the soundness of the approach (as with related static checkers based on implicit dynamic frames) was an open
                                         question. This paper puts practical gradual veriﬁcation on a sound footing with a formalization of symbolic
                                         execution, optimized run-time check generation, and run time execution. We prove our approach is sound;
                                         our proof also covers a core subset of the Viper tool, for which we are aware of no previous soundness result.
                                         Our formalization enabled us to ﬁnd a soundness bug in an implemented gradual veriﬁcation tool and describe
                                         the ﬁx necessary to make it sound.
                                         Additional Key Words and Phrases: gradual veriﬁcation, symbolic execution, static veriﬁcation, implicit dy-
                                         namic frames, soundness proof

                                         1   INTRODUCTION
                                         Static veriﬁcation technology based on Hoare-logic-styled pre- and postconditions [Hoare 1969]
                                         has come a long way in the last few decades. Such tools can now support the modular veriﬁca-
                                         tion of data structures that manipulate the heap [Reynolds 2002; Smans et al. 2012] and are re-
                                         cursive [Parkinson and Bierman 2005]. However, veriﬁcation is expensive, requiring many auxil-
                                         iary speciﬁcations such as loop invariants and lemmas, and often costing an order of magnitude
                                         more human eﬀort than development alone. In response, Bader et al. [2018] introduced the idea
                                         of gradual veriﬁcation, which supports the incremental speciﬁcation and veriﬁcation of code by
                                         seamlessly combining static and dynamic veriﬁcation. A developer can now write partial, imprecise
                                         speciﬁcations—formulas such as ? ∗ 𝑥 .𝑓 == 2—backed by run-time checking. During static veriﬁca-
                                         tion, imprecise speciﬁcations are strengthened in support of proof goals when it is necessary and
                                         non-contradictory to do so. Then, corresponding dynamic checks are inserted to ensure soundness.
                                         As a result, gradual veriﬁcation allows users to specify and verify only the properties and compo-
                                         nents of their system that they care about, and incrementally increase the scope of veriﬁcation as
                                         necessary.
                                            Based on this early idea, Wise et al. [2020] and DiVincenzo et al. [2022] extended gradual veri-
                                         ﬁcation to support recursive heap data structures. Wise et al. [2020] presented the ﬁrst theory of
                                         gradual veriﬁcation for implicit dynamic frames (IDF) [Smans et al. 2012], a variant of separation
                                         logic [Reynolds 2002], and abstract predicates [Parkinson and Bierman 2005]. Their design, cor-
                                         responding theory, and proofs rely heavily on the backward-reasoning technique called weakest
                                         liberal preconditions (WLP), and on inﬁnite sets that are not easy to approximate in ﬁnite form. Ad-
                                         ditionally, Wise et al. [2020]’s design checks all proof obligations at run-time, even when some
                                         obligations have been discharged statically. Therefore, it remained unclear how to implement
                                                                                                                                                                   111
                                         ∗ This version contains supplementary material for the paper of the same name accepted for publication by Principles of

                                         Programming Languages (2024).

                                         Authors’ addresses: Conrad Zimmerman, conrad_zimmerman@brown.edu, Brown University, USA; Jenna DiVincenzo,
                                         Purdue University, USA, jennad@purdue.edu; Jonathan Aldrich, Carnegie Mellon University, USA, jonathan.aldrich@cs.
                                         cmu.edu.
111:2                                                           C. Zimmerman, J. DiVincenzo, and J. Aldrich


gradual veriﬁcation and whether gradually-veriﬁed programs could achieve good performance.
Fortunately, in follow-up work, DiVincenzo et al. [2022] implemented and empirically evaluated
Gradual C0, the ﬁrst gradual veriﬁer that can be used on real programs. Gradual C0 is based on
symbolic execution, a forward-reasoning technique which is routinely used in static veriﬁers such
as Viper [Müller et al. 2016], and optimizes run-time checks with statically available information
to improve run-time performance. DiVincenzo et al. [2022] showed that this improvement over
prior work yields signiﬁcant performance boosts.
   Technically, Gradual C0 is built on top of Viper [Müller et al. 2016], which is a static veriﬁcation
infrastructure and tool that facilitates the development of program veriﬁers supporting IDF and
recursive abstract predicates. Viper also uses symbolic execution at its core. Besides Gradual C0,
an array of widely-used veriﬁers have been built on top of Viper, including Prusti [Astrauskas et al.
2022] for Rust, Nagini [Eilers and Müller 2018] for Python, and VerCors [Blom et al. 2017] for
Java. However, despite its prominence, Viper has not been proven sound; nor have, to our knowl-
edge, other symbolic execution-based methods for verifying IDF logics. Thanks to the complex-
ities of symbolic execution and Viper’s support for practical but advanced veriﬁcation features,
Schwerhoﬀ [2016]’s speciﬁcation of Viper is full of implementation details that make it diﬃcult to
formally state and prove soundness. Since Gradual C0 is built on Viper, this problem carries over
to Gradual C0’s speciﬁcation in DiVincenzo et al. [2022] and is made worse by the combination
of static and dynamic checking. Thus DiVincenzo et al. [2022] does not contain a proof of sound-
ness for Gradual C0. Furthermore, since Gradual C0 uses symbolic execution instead of WLP and
optimizes run-time checks, Wise et al. [2020]’s proof is also not applicable. This is problematic,
because the intricate interactions of static and dynamic checking in gradual veriﬁcation can easily
lead to subtle soundness bugs in gradual veriﬁers like Gradual C0, as we will show in §8.
   Therefore, this paper presents a formal statement and proof of soundness for Gradual C0 and its
underlying core subset of Viper. We formalize Gradual C0’s symbolic execution algorithm in sets of
inference rules, rather than the CPS-style speciﬁcation in DiVincenzo et al. [2022] and Schwerhoﬀ
[2016], to enable abstractions that improve the readability of the design and make it easier to state
and prove soundness. The level of abstraction we use is far closer to the implementation of Grad-
ual C0 than Wise et al. [2020]’s formal system, but slightly more abstract than DiVincenzo et al.
[2022]’s CPS-style speciﬁcation, which is littered with implementation details. Reaching the right
level of abstraction for our goals took some trial and error. We reﬂect on this process, including
our missteps, in this paper as well. Our approach is inspired by the formal system for a basic
type checker combined with symbolic execution in Khoo et al. [2010]. However, we separate the
rules into several types of judgements to reﬂect the architecture of DiVincenzo et al. [2022] and
Schwerhoﬀ [2016] and deal with the complexities of IDF and gradual veriﬁcation. Given an ini-
tial symbolic state, the rules compute a next possible state (of which many may exist), and a set
of run-time checks required for this transition when optimism is relied upon. That is, our rules
are non-deterministic, but only in regards to the multiple execution paths explored by symbolic
execution at program points like if statements, while loops, and logical conditionals.
   Furthermore, we clearly separate the cases required to support imprecise speciﬁcations from
those dealing with the underlying veriﬁcation algorithm supporting only complete static speciﬁ-
cations. Therefore, our formal system is a conservative extension of a core calculus of Viper; and
so, by formalizing Gradual C0 and proving it sound, we have also formalized the core of Viper and
proved it sound. To make it easier for readers of this paper to take advantage of our formal state-
ment and proof of soundness for Viper for their own uses, we present ﬁrst a core language, which
we call SVLC0 , along with veriﬁcation rules modeling Gradual C0’s underlying static veriﬁcation
algorithm. We then deﬁne GVLC0 , which extends SVLC0 to include gradual speciﬁcations and cor-
responds to the full language used by Gradual C0. We also formally deﬁne static veriﬁcation for
Sound Gradual Verification with Symbolic Execution                                              111:3


GVLC0 , modeling the veriﬁcation algorithm of Gradual C0. We hope this separation provides a
solid foundation for future proof endeavors of other static veriﬁers based on symbolic execution.
   In order to fully deﬁne the behavior of GVLC0 and its subset SVLC0 , we specify its dynamic
semantics, which combines the semantics of C0 [Arnold 2010] with the dynamic semantics of
GVLRP , the language used to deﬁne the theory of gradual veriﬁcation with recursive predicates in
Wise et al. [2020]. The C0 programming language is a core, safe variant of the C language intro-
duced for education [Arnold 2010] and is also supported by Gradual C0. C0 allows speciﬁcation
of the pre- and post-conditions of methods, but does not include constructs necessary for static
veriﬁcation using IDF. Thus we add the dynamic semantics from Wise et al. [2020] for IDF spec-
iﬁcations, recursive predicates, and imprecise speciﬁcations. These semantics assert the validity
of every speciﬁcation at run-time, ensuring both memory safety and functional correctness of
programs. Thus these semantics provide a foundation against which we can establish the sound-
ness of Gradual C0’s symbolic execution algorithm. That is, we prove that when all run-time
checks produced by the symbolic execution algorithm are satisﬁed, then the program is guaran-
teed to dynamically execute successfully. A tricky part of this proof is deﬁning a valuation function
[Khoo et al. 2010], which is a partial function mapping symbolic values from symbolic execution to
their concrete values for a speciﬁc execution trace from program execution. This function is used
to state the correspondence between symbolic and concrete execution states. While we start with
Khoo et al. [2010]’s simplistic valuation function, we end up with one that is far more complex as
it additionally connects isorecursive symbolic predicates from static veriﬁcation with their equire-
cursive counterparts in dynamic veriﬁcation and handles global invariants such as separation and
access permissions from IDF. This proof technique allows our formal system and reasoning to
match the implementation more closely than other techniques such as the evidence calculus used
in Garcia et al. [2016]. This enables us to explore future developments using either the implemen-
tation or formalization, and easily update the other to ensure we remain both implementable and
sound.
   Finally, we present and discuss a soundness bug we found in Gradual C0 during our proof work
and have since communicated to DiVincenzo et al. [2022]. The bug is a speciﬁc interaction caused
by reducing run-time checks using statically available information in isorecursive predicates, and
then checking the remaining run-time checks using equirecursive predicates. This bug could not
have arisen in Wise et al. [2020]’s work as their gradual veriﬁcation approach checks all proof
obligations at run time. We explore several options for addressing this soundness bug, explain our
chosen method in detail, and discuss an implementation ﬁx. Despite DiVincenzo et al. [2022]’s
thorough empirical evaluation and testing of Gradual C0, this bug was never discovered in their
testing. This is likely due to the subtle, intricate interactions between veriﬁcation technologies in
gradual veriﬁcation that are hard to test. This demonstrates the value of formally proving sound-
ness in the case of gradual veriﬁcation, and we hope this paper serves as a basis for similar future
work.
To summarize, this paper makes the following contributions:
 • Formalization and proof of soundness for Gradual C0, the ﬁrst gradual veriﬁer for recursive
    heap data structures that is based on symbolic execution [DiVincenzo et al. 2022]. The level
    of abstraction chosen for this proof work improves the readability of Gradual C0’s design and
    makes adapting this work to prove other symbolic execution-based gradual veriﬁers sound
    much easier.
 • Formalization of a core subset of the Viper static veriﬁer, which is based on symbolic execution
    and supports IDF. This work provides the ﬁrst solid foundation for proof work on static veriﬁers
    that use symbolic execution and IDF.
111:4                                                                     C. Zimmerman, J. DiVincenzo, and J. Aldrich


 • A reﬂection on the trial and error of picking the right level of abstraction for our proof work
   in this paper.
 • Demonstration of a soundness bug we found in Gradual C0 during our work and have since
   communicated to DiVincenzo et al. [2022]. We also provide several options for addressing this
   bug and advise on how to implement one of our solutions.

2 SVLC0
We ﬁrst introduce SVLC0 and a corresponding static veriﬁcation algorithm. Since it does not in-
clude imprecise speciﬁcations, SVLC0 can be veriﬁed by existing static veriﬁcation tools such as
Viper [Müller et al. 2016]. The veriﬁcation algorithm corresponds to the core algorithm of Viper,
which is the foundation for static veriﬁcation in Gradual C0. We illustrate how our formalism and
soundness result can be applied to Viper. In later sections we extend SVLC0 ’s veriﬁcation algorithm
to support the veriﬁcation of gradually-speciﬁed GVLC0 programs.

2.1     Definition
We deﬁne an abstract syntax for SVLC0 in Figure 1. Its form is similar to the language of Viper,
which is intended for use as a generic backend for multiple frontend languages; however, we use
the syntax of C0 .
   Programs consist of struct, predicate, and method1 deﬁnitions, and an entry statement. Struct
deﬁnitions contain a list of ﬁelds, predicate deﬁnitions contain a parameter list and a formula (the
predicate body), and method deﬁnitions contain a parameter list, a return type, a pre-condition (de-
noted by requires), a post-condition (denoted by ensures), and a statement (the method body).
The entry statement represents the body of the main method in traditional C programs. Statements
in SVLC0 follow C conventions, except for while, alloc, and return. All while statements specify
a formula called a loop invariant, which states the properties preserved by the loop during execu-
tion. An alloc statement allocates new memory on the heap, initializes it with a default value,
and updates the variable on the left-hand side to contain a reference to the newly allocated value.
This matches C0 semantics, except C0 returns a pointer, not a reference, and thus the type of the
variable is written diﬀerently. We omit return statements; instead, the method body must assign
to a special result variable, whose value is then returned after executing the method body. This
reﬂects the behavior of Gradual Viper which also does not have a return statement. Additionally,
we simplify several statements to make formal deﬁnitions and proofs easier. For example, assign-
ment only occurs to a variable or a ﬁeld of a variable; statements such as x.y.z = 1 are not
permitted. We also omit void method calls, since these do not diﬀer meaningfully from calls to
value-returning methods.
   Like Gradual C0 [DiVincenzo et al. 2022], SVLC0 does not support arrays. Verifying non-trivial
properties of programs that use arrays would require signiﬁcant extensions to existing gradual
veriﬁcation theory – for example, quantiﬁed formulas. These extensions are left to future work.
However, we can verify recursive data structures such as linked lists with abstract predicates. Note
that Viper does support quantiﬁed formulas and arrays, thus further work is necessary to formally
prove soundness of these capabilities.
   We make several simplifying assumptions for SVLC0 programs. All variables are initialized be-
fore they are used, and every execution path for a method body assigns the result variable at its
end. Every program is well-typed; that is, expressions used in if conditions or as boolean operands
will evaluate to bool values, all arguments passed to method parameters will match the deﬁned
1 To distinguish them from pure functions (which are used in the speciﬁcation language of similar veriﬁcation tools) we

use method to refer to any potentially impure function.
Sound Gradual Verification with Symbolic Execution                                                                             111:5


     𝑥 ∈ Var                         Variable names                        Φ ::= requires 𝜙 ensures 𝜙
     𝑓 ∈ Field                             Field names                     𝑇 ::= 𝑆 | int | bool | char
     𝑝 ∈ Predicate                   Predicate names                       𝑠 ::= 𝑠; 𝑠 | skip | 𝑥 = 𝑒 | 𝑥 = alloc(𝑆 ) |
     𝑚 ∈ Method                       Method names                               𝑥 = 𝑚 (𝑒 ) | assert 𝜙 | fold 𝑝 (𝑒 ) |
     𝑆 ∈ Struct                        Struct names                                 unfold 𝑝 (𝑒 ) | if 𝑒 then 𝑠 else 𝑠 |
     𝑛∈Z                                         Integers                           while 𝑒 invariant 𝜙 do 𝑠
                                                                           𝑒 ::= 𝑙 | 𝑥 | 𝑒.𝑓 | 𝑒 ⊕ 𝑒 | 𝑒 || 𝑒 | 𝑒 && 𝑒 | ! 𝑒
      Π ::= S P M 𝑠
                                                                            𝑙 ::= 𝑛 | null | true | false
      S ::= struct 𝑆 { 𝑇 𝑓 }
                                                                           ⊕ ::= + | - | / | * | == | != | <= | >= | < | >
      P ::= 𝑝 (𝑇 𝑥 ) = 𝜙                                                   𝜙 ::= 𝜙 ∗ 𝜙 | 𝑝 (𝑒 ) | 𝑒 | acc(𝑒.𝑓 ) |
     M ::= 𝑇 𝑚 (𝑇 𝑥 ) Φ { 𝑠 }                                                       if 𝑒 then 𝜙 else 𝜙

                                                  Fig. 1. Abstract syntax for SVLC0


parameter type, and the value assign to result has type equal to the method’s return type. Fi-
nally, all speciﬁcations (predicate bodies, loop invariants, and method pre- and post-conditions)
are self-framed, which is a special well-formedness condition from IDF that we deﬁne later.
2.1.1 Formulas. Formulas (speciﬁcations) in SVLC0 are written in the logic of IDF [Smans et al.
2012] and recursive predicates [Parkinson and Bierman 2005]. Thus formulas may contain expres-
sions as well as abstract predicates and accessibility predicates from IDF; formulas may be joined
by the separating conjunction ∗ [Smans et al. 2012]. An accessibility predicate acc(𝑒.𝑓 ) requires
access to the heap location 𝑒.𝑓 . A predicate instance 𝑝 (𝑒) applies the boolean predicate 𝑝 to the ar-
guments 𝑒. An expression 𝑒 requires that 𝑒 evaluates to true. A separating conjunction, as in 𝜙 1 ∗𝜙 2 ,
acts like a logical AND for 𝜙 1 and 𝜙 2 , but also requires the heap locations speciﬁed by predicates
and accessibility predicates in 𝜙 1 to be disjoint from those speciﬁed in 𝜙 2 , e.g. acc(𝑥 .𝑓 ) ∗ acc(𝑦.𝑓 )
implies 𝑥 != 𝑦. A conditional formula if 𝑒 then 𝜙 1 else 𝜙 2 denotes the validity of 𝜙 1 when 𝑒
evaluates to true; otherwise it denotes the validity of 𝜙 2 .
   Formulas in IDF, and thus in SVLC0 , must be self-framed [Smans et al. 2012], which requires per-
missions for all heap locations used in a formula to also be in that formula. For example, x.value
== 0 is not self-framed since it references the heap location x.value, but does not assert acces-
sibility of the ﬁeld x.value. However, acc(x.value) ∗ x.value == 0 is self-framed. We specify
rules for framing and self-framing in §4.3.
   Static veriﬁcation of predicates is done isorecursively [Summers and Drossopoulou 2013], thus
predicate instances must be explicitly folded before they can be asserted. Similarly, predicate bodies
must be explicitly unfolded before asserting the implications of a predicate. This enables static
veriﬁcation of recursive predicates and simpliﬁes reasoning about the veriﬁer’s behavior.

2.2 Representation
In this section, we formally deﬁne the data structures used during static veriﬁcation of SVLC0
programs.
 • A symbolic value 𝜈 ∈ SValue is an abstract value representing an unknown value, such as an
    integer or object reference. We leave the concrete type of SValue undeﬁned, but assume that
    an inﬁnite number of distinct new values can be produced by a fresh function.
 • A symbolic expression 𝑡 ∈ SExpr is a symbolic or literal value, or is composed of other symbolic
    expressions and operators.
                           𝑡   ::=     𝜈     |     𝑙    |   !𝑡   |   𝑡1 && 𝑡2   |      𝑡1 || 𝑡2   |   𝑡1 ⊕ 𝑡2
111:6                                                                  C. Zimmerman, J. DiVincenzo, and J. Aldrich


 • A path condition 𝑔 ∈ SExpr is a symbolic expression composed of conjuncts identifying a
   particular execution path. Conjuncts are added at every conditional branch during symbolic
   execution.
 • A ﬁeld chunk h𝑓 , 𝑡, 𝑡 ′ i ∈ SField represents, in the symbolic heap, the ﬁeld 𝑓 of an object refer-
   ence 𝑡 containing a value 𝑡 ′ . A heap chunk is roughly approximate to the points to construct in
   separation logic [Reynolds 2002]. A predicate chunk h𝑝, 𝑡 i ∈ SPredicate represents an isore-
   cursive instance of a predicate 𝑝 with arguments 𝑡. Together, ﬁeld chunks and predicate chunks
   are called heap chunks.
 • A symbolic heap H ∈ P (SField ∪ SPredicate) is a ﬁnite set of heap chunks. All heap chunks
   that it contains must represent distinct locations in the heap at run time.
 • A symbolic state 𝜎 ∈ SState is a tuple containing a path condition (referenced by 𝑔(𝜎)), a
   symbolic heap (referenced by H(𝜎)), and a symbolic environment (referenced by 𝛾 (𝜎)). A sym-
   bolic state stores all values for a particular point during symbolic execution. The symbol 𝜎empty
   represents an empty symbolic state, i.e. 𝑔(𝜎empty ) = true and H(𝜎empty ) = 𝛾 (𝜎empty ) = ∅.
 • A veriﬁcation state Σ represents a particular point during static veriﬁcation. It is either a special
   symbol or a triple h𝜎, 𝑠, 𝜙i ˜ consisting of a symbolic state 𝜎, a statement 𝑠 that remains to be
   executed, and a formula 𝜙˜ that must be asserted after executing 𝑠. 𝜎 (Σ), 𝑠 (Σ), and 𝜙˜ (Σ) are
   used to reference a speciﬁc component of Σ when Σ is not a symbol.
                                  Σ   ::=   init   |   final   |   h𝜎, 𝑠, 𝜙˜ i

 • A valuation 𝑉 : SValue → Value is a mapping from symbolic values to concrete values
   (deﬁned in §4.1). Valuations are implicitly extended to be deﬁned for all SExpr, following the
   structure of symbolic expressions.
   A symbolic expression 𝑡 implies the symbolic expression 𝑡 ′ (written 𝑡 =⇒ 𝑡 ′ ) if, for all valua-
   tions 𝑉 , 𝑉 (𝑡) = true =⇒ 𝑉 (𝑡 ′ ) = true. For example, 𝑡 1 && 𝑡 2 =⇒ 𝑡 2 . A symbolic expression
   𝑡 is satisﬁable, denoted sat(𝑡), if 𝑉 (𝑡) = true for some valuation 𝑉 .

2.3     Evaluating expressions
Symbolic execution evaluates an expression 𝑒 to a symbolic value 𝑡 using the symbolic state 𝜎,
and is denoted by the judgement 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ . It also yields a new symbolic state 𝜎 ′ which
may contain a more speciﬁc path condition if this particular evaluation short-circuits a boolean
operator. Selected formal rules for symbolic evaluation are given in Figure 2. Literals are evaluated
to themselves and variables are evaluated to the corresponding value in the symbolic store. Some
operators, such as negation and arithmetic operators, are directly translated into a symbolic ex-
pression using the respective operator. In contrast, boolean operators are short-circuiting: when
evaluating 𝑒 1 && 𝑒 2 , if 𝑒 1 evaluates to false, then 𝑒 2 is never evaluated (in this case, 𝑒 1 == false
is added to the path condition). We deﬁne two non-deterministic rules for each binary boolean
operator—SEvalAndA represents the short-circuiting case just described, while SEvalAndB rep-
resents the non-short-circuiting case where 𝑒 1 is true, so 𝑒 2 must also be evaluated to determine the
result. Finally, ﬁeld references are evaluated to the symbolic value contained in their correspond-
ing ﬁeld chunk in the symbolic heap. Note, a heap chunk for the ﬁeld reference must be in the
heap, otherwise evaluation fails (and ultimately static veriﬁcation as well), thus the ﬁeld reference
must be framed by the current state.
   We also deﬁne a judgment of the form 𝜎 ⊢ 𝑒 ↓ 𝑡 which symbolically evaluates an expression
𝑒 to a symbolic expression 𝑡 without short-circuiting. Thus the judgment is deterministic and
does not update the path condition. Instead, logical operators such as && are encoded directly
in the symbolic expression (compare SEvalPCAnd with SEvalAndA/SEvalAndB in Figure 2).
This results in a less speciﬁc path condition, but reduces the number of execution paths during
Sound Gradual Verification with Symbolic Execution                                                                                  111:7


                                                           SEvalNeg                     SEvalAndA
  SEvalLiteral              SEvalVar                         𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎′                           𝜎 ⊢ 𝑒1 ⇓ 𝑡1 ⊣ 𝜎 ′
  𝜎 ⊢𝑙 ⇓𝑙 ⊣𝜎                𝜎 ⊢ 𝑥 ⇓ 𝛾 (𝜎 ) (𝑥 ) ⊣ 𝜎        𝜎 ⊢ ! 𝑒 ⇓ ! 𝑡 ⊣ 𝜎′           𝜎 ⊢ 𝑒1 && 𝑒2 ⇓ 𝑡1 ⊣ 𝜎 ′ [𝑔 = 𝑔 (𝜎 ′ ) && ! 𝑡1 ]
 SEvalAndB                                        SEvalField
             𝜎 ⊢ 𝑒1 ⇓ 𝑡1 ⊣ 𝜎 ′                    𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′         𝑔 (𝜎 ′ ) =⇒ 𝑡𝑒 == 𝑡𝑒′        SEvalPCAnd
 𝜎 ′ [𝑔 = 𝑔 (𝜎 ′ ) && ! 𝑡1 ] ⊢ 𝑒2 ⇓ 𝑡2 ⊣ 𝜎 ′′                h𝑡𝑒′ , 𝑓 , 𝑡 i ∈ H(𝜎 ′ )                    𝜎 ⊢ 𝑒1 ↓ 𝑡1       𝜎 ⊢ 𝑒2 ↓ 𝑡2
         𝜎 ⊢ 𝑒1 && 𝑒2 ⇓ 𝑡2 ⊣ 𝜎 ′′                               𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′                       𝜎 ⊢ 𝑒1 && 𝑒2 ↓ 𝑡1 && 𝑡2 ⊣ 𝜎 ′′


                                            Fig. 2. Selected symbolic evaluation rules



symbolic execution. This matches the evaluation method described in DiVincenzo et al. [2022] for
evaluation in formulas, while the former style is used for evaluation in imperative code.

2.4    Consuming formulas
Given a symbolic state 𝜎 and formula 𝜙, consuming a formula 𝜙 ﬁrst asserts that 𝜙 is established
by 𝜎, and second removes the heap chunks in 𝜎 corresponding to permissions (predicates and
accessibility predicates) in 𝜙. The judgment 𝜎 ⊢ 𝜙 ⊲ 𝜎 ′ denotes consumption; i.e., 𝜙 is consumed
from 𝜎, resulting in the new symbolic state 𝜎 ′ . See Figure 3 for selected rules.
   Consuming an accessibility predicate such as acc(𝑒.𝑓 ) ﬁrst asserts the predicate has a corre-
sponding ﬁeld chunk in the heap, and second removes the chunk from the heap (SConsumeAcc).
Consuming a predicate similarly looks for and removes the corresponding predicate chunk from
the heap (SConsumePredicate). If any of the chunks are missing from the heap, then veriﬁcation
fails. Expressions must evaluate to true in the current symbolic execution path. That is, the current
path condition must imply the symbolic value of the expression (SConsumeValue). As mentioned
previously and seen in the aforementioned rule, expressions in formulas are evaluated with the
deterministic evaluation judgment (i.e., not the short-circuiting one), which matches the behav-
ior described in DiVincenzo et al. [2022] and reduces the number of branches generated during
symbolic execution. This diﬀers from Viper, which uses a single, short-circuiting eval algorithm
everywhere, including in consume. A separating conjunction, such as 𝜙 1 ∗ 𝜙 2 , is consumed left-
to-right, i.e. 𝜙 1 is consumed and then 𝜙 2 is consumed (SConsumeConjunction). This enforces
the separation of permissions between the two conjuncts – heap chunks necessary to satisfy the
permissions asserted in 𝜙 1 will be removed before consuming 𝜙 2 , so, if they overlap, consumption
of 𝜙 2 will fail. Finally, we deﬁne consumption of logical conditionals, like if 𝑒 then 𝜙 1 else 𝜙 2 ,
in two non-deterministic rules. In SConsumeConditionalA, 𝑒 is assumed to be true in the path
condition and 𝜙 1 is consumed. Likewise, in SConsumeConditionalB, 𝑒 is assumed to be false in
the path condition and 𝜙 2 is consumed.
   Note, as we saw in §2.3, evaluation of a ﬁeld access in an expression requires the state to contain
a heap chunk for the ﬁeld. But consume removes heap chunks from the state in a left-to-right
manner thanks to rules SConsumeAcc and SConsumeConjunction. For example, we may want
to consume the formula acc(𝑒.𝑓 ) ∗ 𝑒.𝑓 == 0. First, a heap chunk for acc(𝑒.𝑓 ) is found and removed
from the heap. Then, the resulting state is used to frame and evaluate 𝑒.𝑓 == 0 in the next consume
step. However, the heap chunk for 𝑒.𝑓 was removed from the state so evaluation fails when it
shouldn’t since the original state contained the heap chunk. To solve this issue, we deﬁne consume
using an underlying judgment, denoted 𝜎, 𝜎𝐸 ⊢ 𝜙 ⊲ 𝜎 ′ , which asserts and removes permissions
from 𝜎 while evaluating expressions with the unchanging reference state 𝜎𝐸 . The state 𝜎𝐸 is the
symbolic state before consumption. The rule SConsume deﬁnes the top-level consume judgment
using this new underlying judgment.
111:8                                                                                  C. Zimmerman, J. DiVincenzo, and J. Aldrich


                                                   SConsumeAcc
                            SConsumeValue                    𝜎𝐸 ⊢ 𝑒 ↓ 𝑡𝑒                        SConsumePredicate
 SConsume                     𝜎𝐸 ⊢ 𝑒 ↓ 𝑡                𝑔 (𝜎 ) =⇒ 𝑡𝑒 == 𝑡𝑒′                     𝜎𝐸 ⊢ 𝑒 ↓ 𝑡    𝑔 (𝜎 ) =⇒ 𝑡 == 𝑡 ′
 𝜎, 𝜎 ⊢ 𝜙 ⊲ 𝜎 ′              𝑔 (𝜎 ) =⇒ 𝑡             H(𝜎 ) = { h𝑓 , 𝑡𝑒′ , 𝑡 i } ⊎ H′                H(𝜎 ) = { h𝑝, 𝑡 ′ i } ⊎ H′
   𝜎 ⊢ 𝜙 ⊲ 𝜎′               𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎           𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 [H = H′ ]                     𝜎, 𝜎𝐸 ⊢ 𝜎 [H = H′ ]
   SConsumeConjunction                      SConsumeConditionalA                             SConsumeConditionalB
            𝜎, 𝜎𝐸 ⊢ 𝜙 1 ⊲ 𝜎 ′                 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡        𝑔′ = 𝑔 (𝜎 ) && 𝑡               𝜎𝐸 ⊢ 𝑒 ↓ 𝑡       𝑔′ = 𝑔 (𝜎 ) && ¬𝑡
   𝜎 ′ , 𝜎𝐸 [𝑔 = 𝑔 (𝜎 ′ ) ] ⊢ 𝜙 2 ⊲ 𝜎 ′′     𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 1 ⊲ 𝜎 ′            𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 2 ⊲ 𝜎 ′
        𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ⊲ 𝜎 ′′            𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲ 𝜎 ′             𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲ 𝜎 ′


                                               Fig. 3. Selected consume rules


  Our consume judgment represents the core functionality of DiVincenzo et al. [2022] and Schwerhoﬀ
[2016]’s consume algorithms. We, of course, ignore unnecessary implementation details like snap-
shots, which preserve certain portions of the state that are removed during consume.

2.5 Producing formulas
Given an initial state 𝜎 and formula 𝜙, producing 𝜙 adds the information in 𝜙 into the symbolic state
𝜎, resulting in a new state 𝜎 ′ . The judgment for 𝜎 ⊢ 𝜙 ⊳ 𝜎 ′ denotes production; i.e., 𝜙 is produced
into the state 𝜎, resulting in 𝜎 ′ . In particular, produce adds heap chunks representing predicates
in 𝜙 to the symbolic heap and symbolic expressions representing constraints from boolean expres-
sions in 𝜙 to the path condition in a left-to-right manner. Note, each symbolic heap chunk repre-
sents a distinct region of memory at run-time, an invariant that we later prove. Thus overlapping
heap chunks may only occur in symbolic states which represent an unreachable dynamic state
and can safely be ignored. When producing formulas, we use deterministic symbolic evaluation
for expressions, but we introduce separate execution paths for conditionals (similar to §2.4).
   Formal rules are given in §C.8. These rules capture the functionality of the produce algorithm
speciﬁed in DiVincenzo et al. [2022] and Schwerhoﬀ [2016]. As noted in the previous section,
Schwerhoﬀ [2016] uses short-circuiting evaluation in all places, while we use deterministic evalu-
ation.

2.6     Executing statements
Now that we have formally deﬁned symbolic execution of expressions and formulas, we can put
the pieces together to deﬁne symbolic execution of program statements.
   We represent the symbolic execution of program statements as small-step execution rules de-
noted by the judgment 𝜎 ⊢ 𝑠 → 𝑠 ′ ⊣ 𝜎 ′ , where the initial statement 𝑠 is symbolically executed with
the initial state 𝜎, resulting in the state 𝜎 ′ , and then transitions to the next statement 𝑠 ′ with the
new state 𝜎 ′ . Selected formal rules are shown in Figure 4. Executing a variable assignment updates
the symbolic store (SExecAssign); while executing a ﬁeld assignment ﬁrst consumes acc(𝑥 .𝑓 ), and
then adds a new heap chunk for 𝑥 .𝑓 to the heap that contains 𝑥 .𝑓 ’s new symbolic value after the
write (SExecAssignField). An alloc(𝑆) statement adds a heap chunk for each ﬁeld in 𝑆 to the
symbolic heap. The new object reference is a fresh value but the new ﬁeld chunks are each initial-
ized with default values, which reﬂects the behavior of C0 (SExecAlloc). Execution rules for if
statements are non-deterministic: given a statement if 𝑒 then 𝑠 1 else 𝑠 2 , SExecIfA adds 𝑒 to the
path condition and continues execution with 𝑠 1 , while SExecIfB adds ! 𝑒 to the path condition and
continues execution with 𝑠 2 .
   Symbolic execution of method calls is modular; i.e., the behavior of the method call is repre-
sented by the method’s pre- and post-conditions (SExecCall). First, the method’s arguments are
Sound Gradual Verification with Symbolic Execution                                                                                          111:9


                                                                                SExecAssignField
              SExecAssign                                                       𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎′  𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ⊲ 𝜎 ′′
              𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎′         𝛾 ′ = 𝛾 (𝜎 ) [𝑥 ↦→ 𝑡 ]                       H = H(𝜎 ) ∪ { h𝑓 , 𝛾 (𝜎 ′′ ) (𝑥 ), 𝑡 i }
                                                                                   ′        ′′

                  𝜎 ⊢ 𝑥 = 𝑒; 𝑠 → 𝑠 ⊣ 𝜎 ′ [𝛾 = 𝛾 ′ ]                                  𝜎 ⊢ 𝑥 .𝑓 = 𝑒; 𝑠 → 𝑠 ⊣ 𝜎 ′′ [H = H′ ]
                                                                         SExecCall
                                                                                  𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎′        𝑥 = params(𝑚)
         SExecAlloc                                                                𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡 ] ] ⊢ pre(𝑚) ⊲ 𝜎 ′′
             𝑡 = fresh     𝑇 𝑓 = struct(𝑆 )                                       𝑡 ′ = fresh    𝛾 ′ = 𝛾 (𝜎 ′ ) [𝑦 ↦→ 𝑡 ′ ]
           H′ = H(𝜎 ) ∪ { h𝑓 , 𝑡, default(𝑇 ) i }                        𝜎 ′′ [𝛾 = [𝑥 ↦→ 𝑡, result ↦→ 𝑡 ′ ] ] ⊢ post(𝑚) ⊳ 𝜎 ′′′
         𝜎 ⊢ 𝑥 = alloc(𝑆 ); 𝑠 → 𝑠 ⊣ 𝜎 [H = H′ ]                                  𝜎 ⊢ 𝑦 = 𝑚 (𝑒 ); 𝑠 → 𝑠 ⊣ 𝜎 ′′′ [𝛾 = 𝛾 ′ ]
         SExecIfA                                                             SExecIfB
         𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎′        𝜎 ′′ = 𝜎 ′ [𝑔 = 𝑔 (𝜎 ′ ) && 𝑡 ]                𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎′            𝜎 ′′ = 𝜎 ′ [𝑔 = 𝑔 (𝜎 ′ ) && ! 𝑡 ]
                                                           ′′
          𝜎 ⊢ if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠 → 𝑠 1 ; 𝑠 ⊣ 𝜎                          𝜎 ⊢ if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠 → 𝑠 2 ; 𝑠 ⊣ 𝜎 ′′
              SExecWhile
              𝜎 ⊢ 𝜙 ⊲ 𝜎′          𝑥 = modiﬁed(𝑠 )               𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ fresh] ] ⊢ 𝜙 ⊳ 𝜎 ′′         𝜎 ′′ ⊢ 𝑒 ↓ 𝑡
                                                                          ′      ′      ′′         ′′
                            𝜎 ⊢ while 𝑒 invariant 𝜙 do 𝑠; 𝑠 → 𝑠 ⊣ 𝜎 [𝑔 = 𝑔 (𝜎 ) && ! 𝑡 ]


                                         Fig. 4. Selected symbolic execution rules


evaluated to symbolic values. Then the pre-condition is consumed using a special environment
containing the argument values. A fresh symbolic value is added to represent the return value of
the method, and then the post-condition of the method is produced. The special environment is
then replaced by the original environment, with the addition of the result’s symbolic value. Loops
(i.e while statements) are executed similarly: the loop invariant is consumed, variables modiﬁed
by the loop body are set to fresh values in the symbolic store, the loop invariant is produced, and
the negated loop condition is added to the path condition (SExecWhile). Execution of the fold
and unfold statements is also similar to loops and method calls: fold consumes the predicate
body and adds a representative predicate chunk to the symbolic heap, while unfold consumes the
predicate instance (thus removing the predicate chunk from the heap) and produces the predicate
body.

2.7 Modularly verifying programs
We now deﬁne veriﬁcation of entire programs. We start by deﬁning what a program Π is; it is
a quadruple h𝑠, 𝑀, 𝑃, 𝑆i where 𝑠 is the entry statement of the program, 𝑀 is the set of method
names, 𝑃 is the set of predicate names, and 𝑆 is the set of struct names in the program. Then, we
deﬁne the judgment Π ⊢ Σ → Σ′ that speciﬁes all possible symbolic execution steps that occur
during veriﬁcation of Π. Selected rules are given in Figure 5.
   A veriﬁcation state Σ is reachable from program Π if Σ = init or Π ⊢ Σ0 → Σ for some reachable
Σ0 . The latter judgement only holds when Σ0 is itself reachable.
   This judgement includes rules for modular veriﬁcation. From init, we can begin veriﬁcation of
the entry statement (SVerifyInit) or of any method (SVerifyMethod). When verifying a method,
the method’s post-condition is used as the formula of the veriﬁcation state. After completely ex-
ecuting the method’s body, i.e. having reached skip, we consume the formula contained in the
veriﬁcation state (SVerifyFinal), which is the method’s post-condition.
   We modularly verify loop bodies following a similar pattern. As described in §2.6, symbolic
execution steps over loop bodies in the same way it steps over method calls. However, we introduce
a veriﬁcation rule (SVerifyLoopBody) that allows symbolic execution of a loop body, beginning
with a new symbolic state. We reuse the symbolic store from the initial symbolic state, except
111:10                                                                               C. Zimmerman, J. DiVincenzo, and J. Aldrich


                                                                    SVerifyMethod
                                                                             𝑚∈𝑀          𝑥 = params(𝑚)
           SVerifyInit                                                  𝜎empty [𝛾 = [𝑥 ↦→ fresh] ] ⊢ pre(𝑚) ⊳ 𝜎
           h𝑠, 𝑀, 𝑃, 𝑆 i ⊢ init → h𝜎empty , 𝑠, truei                 h𝑠, 𝑀, 𝑃, 𝑆 i ⊢ init → h𝜎, body(𝑚); 𝑠, post(𝑚) i
   SVerifyLoopBody                                                  SVerifyLoop
   Π ⊢ _ → h𝜎0 , while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ , 𝜙˜0 i                Π ⊢ _ → h𝜎0 , while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ , 𝜙˜0 i
     h⊥, 𝛾 (𝜎0 ) [𝑥 ↦→ fresh], ∅, ∅, 𝑔 (𝜎0 ) i ⊢ 𝜙˜ ⊳ 𝜎             𝜎0 ⊢ 𝜙˜ ⊲ 𝜎0′ , _   𝜎0′ [𝛾 = 𝛾 (𝜎0 ) [𝑥 ↦→ fresh] ] ⊢ 𝜙˜ ⊳ 𝜎0′′
          𝑥 = modiﬁed(𝑠 )           𝜎 ⊢𝑒 ↓𝑡 ⊣ R                                          𝑥 = modiﬁed(𝑠 )
    Π ⊢ h𝜎0 , while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ , 𝜙˜0 i →                  Π ⊢ h𝜎0 , while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ , 𝜙˜0 i →
             h𝜎 [𝑔 = 𝑔 (𝜎 ) && 𝑡 ], 𝑠; skip, 𝜙˜ i                            h𝜎0 , while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ , 𝜙˜0 i
               SVerifyStep                                                 SVerifyFinal
               Π ⊢ _ → h𝜎, 𝑠, 𝜙 i         𝜎 ⊢ 𝑠 → 𝑠′ ⊣ 𝜎′                  Π ⊢ _ → h𝜎, skip, 𝜙 i         𝜎 ⊢ 𝜙 ⊲ 𝜎′,
                                               ′    ′
                      Π ⊢ h𝜎, 𝑠, 𝜙 i → h𝜎 , 𝑠 , 𝜙 i                               Π ⊢ h𝜎, skip, 𝜙 i → final


                                                   Fig. 5. Selected verification rules

   1   struct List { int value ; List next }                     13 List append ( List l , int value )
   2                                                             14   requires acyclic ( l ) * l != NULL
   3   predicate acyclic ( List l ) =                            15   ensures acyclic ( result ) * result != NULL
   4     acc ( l . value ) * acc ( l . next ) *                  16 {
   5     ( if l . next == NULL then true                         17   unfold acyclic ( l );
   6       else acyclic ( l . next ))                            18   if ( l. next == NULL )
   7                                                             19       n = singleton ( value );
   8   List singleton ( int value )                              20   else
   9     requires true                                           21       n = append ( l . next , value );
  10     ensures ( acyclic ( result ) *                          22   l . next = n ;
  11               result != NULL )                              23   fold acyclic ( l );
  12   { ··· }                                                   24   result = l ;
                                                                 25 }


                 Fig. 6. Code and supporting declarations for appending to an acyclic linked list


that all variables modiﬁed by the loop body are replaced by fresh values. Veriﬁcation proceeds
similar to method veriﬁcation, except that we use the loop invariant for the formula of the new
veriﬁcation state—we produce the loop invariant, symbolically execute the loop body, and ﬁnally
consume the loop invariant. Thus symbolic execution, which steps over the loop, ensures that
the loop invariant holds for the initial iteration, while this veriﬁcation rule ensures that the loop
invariant is preserved after every iteration.
   We also include another veriﬁcation rule for loops, SVerifyLoop, in order to match the behavior
of Gradual C0. This rule and its correspondence with Gradual C0 is described further in §7.2.
   Statements are executed by symbolic execution as described in §2.6. Given a reachable veriﬁca-
tion state h𝜎, 𝑠, 𝜙i and the symbolic execution 𝜎 ⊢ 𝑠 → 𝑠 ′ ⊣ 𝜎 ′ , the state h𝜎 ′ , 𝑠 ′ , 𝜙i is reachable,
i.e. Π ⊢ h𝜎, 𝑠, 𝜙i → h𝜎 ′ , 𝑠 ′, 𝜙i.

2.8 Example
We now illustrate veriﬁcation of the append method deﬁned in Figure 6, which appends a given
value to the end of a list using recursion. The append method is ensured to be memory safe and
preserve acyclicity of the list through veriﬁcation. We begin with an empty state and initialize all
parameters with fresh values:
𝜎1 = h∅, 𝛾, true i 𝛾 = [ l ↦→ 𝜈1 , v ↦→ 𝜈2 ]
     Sound Gradual Verification with Symbolic Execution                                                                                111:11


     Then the pre-condition acyclic(l) * l != NULL is produced:
     𝜎2 = h { h acyclic, 𝜈1 i }, 𝛾, 𝜈1 != null i

     Unfolding acyclic(l) (line 17) consumes the predicate from the state and produces its body. The
     body of acyclic(l) contains a logical conditional resulting in two possible execution paths for
     produce – one where 𝜈 4 is null and one where 𝜈 4 is not null, where 𝜈 4 is the symbolic value for
     l.next:
17 unfold acyclic ( l );
     𝜎𝐴3 = h { h value, 𝜈1, 𝜈3 i, h next, 𝜈1, 𝜈4 i }, 𝛾, 𝜈1 != null && 𝜈4 == null i
     𝜎𝐵3 = h { h value, 𝜈1, 𝜈3 i, h next, 𝜈1, 𝜈4 i, h acyclic, 𝜈4 i }, 𝛾, 𝜈1 != null && 𝜈4 != null i

     We follow both execution paths, using color-coding to distinguish them. Next, when executing the
     if statement (line 18), we ﬁrst evaluate the condition. Since l.next is framed by the state, evalu-
     ation of the condition succeeds and execution branches along the if. We ﬁrst consider executing
     the then branch of the if, where 𝜈 4 == null is added it to the path condition:
18 if ( l . next == NULL )
           𝜎𝐴4 = h· · · , · · · , 𝜈1 != null && 𝜈4 == null && 𝜈4 == null i
           𝜎𝐵4 = h· · · , · · · , 𝜈1 != null && 𝜈4 != null && 𝜈4 == null i

     However, the path condition 𝜈 1 != null && 𝜈 4 != null && 𝜈 4 == null is unsatisﬁable, thus we
     can safely prune this execution path and only continue with the ﬁrst. We proceed to symbolically
     execute the call to singleton (line 19) by consuming the (empty) pre-condition, and producing
     the post-condition. The result is represented by a fresh symbolic value 𝜈 5 :
19        n = singleton ( value );
           𝜎𝐴5 = h { h value, 𝜈1, 𝜈3 i, h next, 𝜈1, 𝜈4 i, h acyclic, 𝜈5 i }, 𝛾 [ n ↦→ 𝜈5 ], 𝜈1 != null && 𝜈4 == null && 𝜈5 != null i

     Symbolic execution of this path then jumps to line 22, but to preserve code order we now demon-
     strate veriﬁcation of the else branch (line 20). To do this, we use states 𝜎𝐴3 and 𝜎𝐵3 , and add the
     negation of the condition to verify the else body:
20 else
            ′ = h· · · , · · · , 𝜈 != null && 𝜈 == null && 𝜈 != null i
           𝜎𝐴4                    1            4            4

            ′ = h { h value, 𝜈 , 𝜈 i, h next, 𝜈 , 𝜈 i, h acyclic, 𝜈 , } i, 𝛾, 𝜈 != null && 𝜈 != null i
           𝜎𝐵4                1 3              1 4                 4           1            4

     Here again this results in an unsatisﬁable path condition 𝜈 1 != null&&𝜈 4 == null&&𝜈 4 != null, so
     we prune that path. We continue with the other path and execute the recursive call to append (line
     21), which consumes the pre-condition (removing hacyclic, 𝜈 4 i) and produces the post-condition,
     using the fresh value 𝜈 6 to represent the result (adding hacyclic, 𝜈 6 i):
21        n = append ( l . next , value );
            ′ = h { h value, 𝜈 , 𝜈 i, h next, 𝜈 , 𝜈 i, h acyclic, 𝜈 i }, 𝛾 [ n ↦→ 𝜈 ], 𝜈 != null && 𝜈 != null && 𝜈 != null i
           𝜎𝐵5                1 3              1 4                 6               6    1            4            6

     Now we have completed verifying both branches of the if statement. Note that we do not actually
     join execution at this point; instead, we jump to line 22 immediately after executing the program
                     ′ along both paths. We follow both of these paths for the rest of veriﬁcation. The
     up to 𝜎𝐴5 and 𝜎𝐵5
     ﬁeld assignment on line 22 consumes acc(l.next) and produces a new corresponding heap chunk
     with n’s value:
22 l . next = n ;
     𝜎𝐴6 = h { h value, 𝜈1, 𝜈3 i, h next, 𝜈1, 𝜈5 i, h acyclic, 𝜈5 i }, 𝛾 [ n ↦→ 𝜈5 ], 𝜈1 != null && 𝜈4 == null && 𝜈5 != null i
      ′ = h { h value, 𝜈 , 𝜈 i, h next, 𝜈 , 𝜈 i, h acyclic, 𝜈 i }, 𝛾 [ n ↦→ 𝜈 ], 𝜈 != null && 𝜈 != null && 𝜈 != null i
     𝜎𝐵6                1 3              1 6                 6               6    1            4            6

     Folding acyclic results in twice the number of execution paths since it consumes acylic(l)’s
     body, which includes an logical conditional. However, again, information from the path conditions
                 ′ allow us to prune some of these paths. We elide these pruned paths and only show
     in 𝜎𝐴6 and 𝜎𝐵6
   111:12                                                                                     C. Zimmerman, J. DiVincenzo, and J. Aldrich


   the taken ones. After consuming acyclic(l)’s body, execution produces acyclic(l) into the
   state:
23 fold acyclic ( l );
    𝜎𝐴7 = h { h acyclic, 𝜈1 i }, 𝛾 [ n ↦→ 𝜈5 ], 𝜈1 != null && 𝜈4 == null && 𝜈5 != null i
     ′ = h { h acyclic, 𝜈 i }, 𝛾 [ n ↦→ 𝜈 ], 𝜈 != null && 𝜈 != null && 𝜈 != null i
    𝜎𝐵7                  1               6    1            4            6

24 result = l ;
    𝜎𝐴8 = h { h acyclic, 𝜈1 i }, 𝛾 [ n ↦→ 𝜈5 , result ↦→ 𝜈1 ], 𝜈1 != null && 𝜈4 == null && 𝜈5 != null i
     ′ = h { h acyclic, 𝜈 i }, 𝛾 [ n ↦→ 𝜈 , result ↦→ 𝜈 ], 𝜈 != null && 𝜈 != null && 𝜈 != null i
    𝜎𝐵8                  1               6             1    1            4            6

                             ′ , we can consume the post-condition acyclic(result) * result
   Finally, in both 𝜎𝐴8 and 𝜎𝐵8
   != NULL. Therefore, we have veriﬁed all possible symbolic execution paths of append’s body, and
   thus veriﬁed append.

   3 GVLC0
   SVLC0 reﬂects the core components of Viper—eval, consume, produce, and exec. We now formally
   deﬁne GVLC0 , an extension of SVLC0 which supports gradual speciﬁcations. We then deﬁne static
   veriﬁcation for GVLC0 that allows optimistic assumptions to satisfy proof goals and generates
   checks to be veriﬁed at run time to cover these assumptions as in DiVincenzo et al. [2022].
      Note, the syntax of GVLC0 diﬀers slightly from that of GVC0 (the frontend for Gradual C0),
   particularly with its omission of C-style pointers. However, due to the restrictions of C0 , all usages
   of pointers in C0 can be translated to use object references. This and other translations are done by
   Gradual C0 during its conversion to an intermediate language Gradual Viper, which is used in the
   backend veriﬁer. In order to simplify our model, GVLC0 is very similar to the language of GVC0,
   but incorporates elements of the Gradual Viper language when this simpliﬁes the deﬁnition of our
   veriﬁcation algorithm.

   3.1 Gradual formulas
   We ﬁrst extend the syntax of our language to include imprecise formulas—formulas of the form
   ? ∗ 𝜙. An imprecise formula may represent any logically consistent strengthening of the precise
   portion 𝜙 [Wise et al. 2020]. For example, the imprecise formula ?∗𝑥 > 0 consistently implies 𝑥 ==2,
   but does not consistently imply 𝑥 == 0. Then, a gradual formula 𝜙˜ may be precise or imprecise,
   and gradual programs are programs that contain gradual formulas. The abstract syntax of GVLC0
   extends SVLC0 ’s syntax with gradual formulas:
      P ::= 𝑝 (𝑇 𝑥 ) = 𝜙˜                                                𝑠 ::= · · · | while 𝑒 invariant 𝜙˜ do 𝑠
       Φ ::= requires 𝜙˜ ensures 𝜙˜                                     𝜙˜ ::= 𝜙 | ? ∗ 𝜙

   Note, imprecise formulas are always considered self-framed, because they can always be strength-
   ened to be self-framing. Therefore we require all method pre- and postconditions, loop invariants,
   and predicate bodies to be speciﬁcations—formulas which are either imprecise or self-framed.
     Also, note that IDF is particularly well-suited for gradual speciﬁcations, in comparison to sep-
   aration logic [Reynolds 2002], since IDF allows separately specifying access permission and heap
   values. This allows speciﬁcation of heap values while leaving more complex accessibility assertions
   unspeciﬁed, as in the formula ? ∗ x.f != null.

   3.2 Representation
   In this section we extend the data structures from §2.2 to support imprecise states—states in which it
   is permissible to make optimistic assumptions—and deﬁne our representation of run-time checks.
Sound Gradual Verification with Symbolic Execution                                              111:13


 • A symbolic state 𝜎 is now a quintuple h𝜄, H, H, 𝛾, 𝑔i where 𝜄 is an imprecise ﬂag, H is a precise
   heap, H is an optimistic heap, 𝛾 is the symbolic store, and 𝑔 is the path condition. As before, we
   use the notation 𝜄 (𝜎), H(𝜎), etc. to reference speciﬁc components of a symbolic state. 𝛾 and 𝑔
   are deﬁned in §2.2 but we redeﬁne the other components.
 • An imprecise ﬂag 𝜄 ∈ {⊤, ⊥} is a ﬂag indicating whether a symbolic state is imprecise (⊤)
   or precise (⊥). 𝜄 (𝜎) denotes that 𝜄 (𝜎) = ⊤ (and thus 𝜎 is an imprecise state), while ¬𝜄 (𝜎)
   denotes that an 𝜄 (𝜎) = ⊥ (and thus 𝜎 is precise). Imprecise states are produced by consuming
   or producing an imprecise speciﬁcation. Once imprecise, a state always remains imprecise.
 • A precise heap H is a symbolic heap as described in section 2.2. Thus it is a ﬁnite set of heap
   chunks where all heap chunks represent distinct locations in the heap at run time.
 • An optimistic heap H is a ﬁnite set of ﬁeld chunks. Field chunks contained in the optimistic
   heap may represent the same location in the heap at run time, i.e. the optimistic heap does not
   preserve the separation invariant like the precise heap. The optimistic heap of a well-formed
   symbolic state must be empty unless it is an imprecise state.

3.3 Run-time checks
A run-time check 𝑟 ∈ SCheck denotes an assertion that validates assumptions made during static
veriﬁcation of imprecise programs. It is a symbolic expression, symbolic permission, pair of sym-
bolic permission sets, or ⊥:
                                  𝑟   ::=   𝑡   |    𝜃   |   sep(Θ1 , Θ2 )   |   ⊥

A set of run-time checks is denoted R ∈ P (SCheck). In a run-time check, a symbolic expres-
sion 𝑡 asserts that the value represented by 𝑡 at run time is true, a symbolic permission 𝜃 asserts
ownership of a ﬁeld or a predicate instance, and a pair sep(Θ1 , Θ2 ) asserts that the sets of permis-
sions represented by Θ1 and Θ2 are disjoint. ⊥ represents a static veriﬁcation failure. We represent
static veriﬁcation failure as an unsatisﬁable run-time check, instead of failing veriﬁcation entirely,
to accommodate imprecision.
   Note that our run-time checks contain symbolic values. This is unlike Gradual C0 [DiVincenzo et al.
2022], where checks produced have their symbolic values replaced by corresponding program vari-
ables. This replacement is needed to support the implementation of run-time checks and adds a
signiﬁcant amount of complexity to their algorithms. Fortunately, as we will see later, we can ab-
stract away this connection of symbolic values to program variables (aka. concrete values) using
valuations; and so we can produce abstracted checks here, avoiding additional complexity in our
formalism. Additionally, at each branch point DiVincenzo et al. [2022] check whether all possible
branches fail and, if so, halt static veriﬁcation. We do not specify this behavior; however, this is
possible by checking for ⊥ ∈ R at each step of symbolic execution.

3.4   Evaluating expressions
We now extend our previous judgement for symbolic evaluation from §2.3 to allow optimistic
symbolic evaluation of expressions. We specify a set R of run-time checks necessary for a given
evaluation, thus our judgement is now 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R.
   Field chunks may be referenced in the optimistic heap by SEvalFieldOptimistic in Figure 7.
These ﬁeld chunks have already been validated, thus we do not need additional run-time checks.
A ﬁeld may also be optimistically evaluated by SEvalFieldImprecise, even if it does not exist in H
or H . This adds a new ﬁeld chunk with a fresh value to H . This requires a run-time check which
asserts permission to access the ﬁeld. Finally, SEvalFieldFailure applies in a precise state when a
ﬁeld is referenced but no matching heap chunk exists. This results in a failure of static veriﬁcation,
represented by ⊥, for that execution branch.
111:14                                                                                      C. Zimmerman, J. DiVincenzo, and J. Aldrich


         SEvalFieldOptimistic                                             SEvalFieldImprecise
                          𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R                                            𝜄 (𝜎 )    𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R
                    ′
           h𝑓 , 𝑡𝑒 , 𝑡 i ∈ H(𝜎 ′ ) : 𝑔 (𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒                       ′
                                                                           h𝑓 , 𝑡𝑒 , 𝑡 i ∈ H(𝜎 ) ∪ H (𝜎 ′ ) : 𝑔 (𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒
                                                                                                 ′

         h𝑓 , 𝑡𝑒′ , 𝑡 i ∈ H (𝜎 ′ )     𝑔 (𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒                     𝑡 = fresh         H ′ = H (𝜎 ) ∪ { h𝑓 , 𝑡𝑒 , 𝑡 i }
                       𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′ , R                                    𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′ [ H = H ′ ], R ∪ { h𝑡𝑒 , 𝑓 i }
                    SEvalFieldFailure
                    ¬𝜄 (𝜎 )   𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R              h𝑓 , 𝑡𝑒′ , 𝑡 i ∈ H(𝜎 ′ ) ∪ H (𝜎 ′ ) : 𝑔 (𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒
                                                        𝜎 ⊢ 𝑒.𝑓 ⇓ fresh ⊣ 𝜎 ′ , {⊥}


                             Fig. 7. Selected rules for evaluation during gradual verification


   We also modify the existing set of rules described in §2.3 to collect run-time checks from recur-
sive evaluations. Likewise, we modify the deterministic evaluation judgement to add similar rules
as those described above, allowing it to also generate run-time checks, thus its form is 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ R.

3.5 Consuming formulas
We extend our previous judgment for consuming formulas from §2.4 to handle imprecise formulas
and imprecise states. As in §3.4, we add a parameter R to the consume judgments. Additionally, we
collect all permissions for the given formula into a set of symbolic permissions Θ so that separation
checks may be added where necessary. Thus the new judgments are of the form 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R
and 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R, Θ; these two forms are related by SConsume and correspond to the forms
described in §2.4. We list selected rules in Figure 8.
   Consuming an imprecise formula empties the precise and optimistic heaps (SConsumeImprecise).
This is because the imprecision may represent access to arbitrary ﬁelds. For example, a method
with an imprecise precondition could modify any ﬁeld that the callee owns, thus we cannot make
any assumptions about ﬁeld permissions or values after the method returns. Consuming an impre-
cise formula results in an imprecise state, thus removed ﬁeld chunks can be referenced optimisti-
cally, with the possible addition of a run-time check.
   We must also consider the case of consuming an imprecise formula in a precise state. Since
optimistic assumptions are not permitted in a precise state, we cannot assume any of the assertions
contained in the imprecise formula. However, the imprecise formula may reference ﬁelds without
a corresponding accessibility predicate. Thus, when consuming an imprecise formula, we use an
imprecise state as the symbolic state for evaluation, but use the original (possibly precise) state for
assertions.
   In an imprecise state we may optimistically consume an expression, even if it is not implied by
the current path condition. We then add the value as a run-time check to be asserted at run-time.
   Consumption of accessibility predicates must be modiﬁed to handle imprecise states, where ﬁeld
chunks in H may overlap with ﬁeld chunks in H. We must remove all ﬁelds that may represent
the same heap reference when removing a ﬁeld chunk from H. To do this, we use the helper
functions remfp and remf . remfp is used when removing heap chunks from the precise heap. For
precise states, remfp removes the ﬁeld chunk that coincides exactly with the heap location being
consumed (thus computing the same result as the rules in §2.4). For imprecise states, it also removes
all ﬁeld chunks that could possibly coincide with the speciﬁed heap location. remf is used when
removing chunks from the optimistic heap and behaves similarly, but also removes all predicate
chunks, since predicates occurring in the precise heap could overlap with heap chunks in the
imprecise heap. Some optimizations could be made – for instance, if a predicate’s unfolding will
never reference a ﬁeld 𝑓 , we could preserve an instance of this predicate when consuming acc(𝑒.𝑓 ).
However, we leave such optimizations to future work.
Sound Gradual Verification with Symbolic Execution                                                                               111:15


                    SConsume                                   SConsumeImprecise
                    𝜎, 𝜎𝐸 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R, Θ                           𝜎, 𝜎𝐸 [𝜄 = ⊤] ⊢ 𝜙 ⊲ 𝜎 ′ , R, Θ
                       𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R                         𝜎, 𝜎𝐸 ⊢ ? ∗ 𝜙 ⊲ h⊤, 𝑔 (𝜎 ′ ), 𝛾 (𝜎 ′ ), ∅, ∅i, R, Θ
            SConsumeValueImprecise                                         SConsumeValueFailure
             𝜄 (𝜎 ) 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R              𝑔 (𝜎 ) =⇒
                                                        Y 𝑡                ¬𝜄 (𝜎 ) 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R               𝑔 (𝜎 ) =⇒
                                                                                                                        Y 𝑡
             𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎 [𝑔 = 𝑔 (𝜎 ) && 𝑡 ], R ∪ {𝑡 }, ∅                             𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎, {⊥}, ∅
                                                                          SConsumeAccOptimistic
              SConsumeAcc                                                  𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R               𝑔 (𝜎 ) =⇒ 𝑡𝑒′ == 𝑡𝑒
              𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R           𝑔 (𝜎 ) =⇒ 𝑡𝑒′ == 𝑡𝑒                 h𝑓 , 𝑡𝑒′ , 𝑡 i ∈ H(𝜎 ) : 𝑔 (𝜎 ) =⇒ 𝑡𝑒′ == 𝑡𝑒
                         h𝑓 , 𝑡𝑒′ , 𝑡 i ∈ H(𝜎 )                                           h𝑓 , 𝑡𝑒′ , 𝑡 i ∈ H (𝜎 )
                    H′ = remfp (H(𝜎 ), 𝜎, 𝑡𝑒 , 𝑓 )                                  H′ = remf (H(𝜎 ), 𝜎, 𝑡𝑒 , 𝑓 )
                    H ′ = remf ( H (𝜎 ), 𝜎, 𝑡𝑒 , 𝑓 )                               H ′ = remf ( H (𝜎 ), 𝜎, 𝑡𝑒 , 𝑓 )
                    𝜎 ′ = 𝜎 [H = H′ , H = H ′ ]                                     𝜎 ′ = 𝜎 [H = H′ , H = H ′ ]
               𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 ′ , R, { h𝑡𝑒 , 𝑓 i }                    𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 ′ , R, { h𝑡𝑒 , 𝑓 i }
SConsumeAccImprecise
                         𝜄 (𝜎 )  𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R                                SConsumeAccFailure
        h𝑓 , 𝑡𝑒′ , 𝑡 i ∈ H(𝜎 ) ∪ H (𝜎 ) : 𝑔 (𝜎 ) =⇒ 𝑡𝑒′ == 𝑡𝑒                                  ¬𝜄 (𝜎 )   𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R
𝜎 ′ = 𝜎 [H = remf (H(𝜎 ), 𝜎, 𝑡𝑒 , 𝑓 ), H = remf ( H (𝜎 ), 𝜎, 𝑡𝑒 , 𝑓 ) ]         h𝑓 , 𝑡𝑒′ , 𝑡 i ∈ H(𝜎 ) ∪ H (𝜎 ) : 𝑔 (𝜎 ) =⇒ 𝑡𝑒′ == 𝑡𝑒
       𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 ′ , R ∪ { h𝑡𝑒 , 𝑓 i }, { h𝑡𝑒 , 𝑓 i }                    𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎, {⊥}, { h𝑡𝑒 , 𝑓 i }


                                 Fig. 8. Selected rules for consuming gradual formulas


   We can also optimistically assume an accessibility predicate in an imprecise state, even if a
matching ﬁeld chunk does not exist in H or H . Since this assumes ownership of the ﬁeld, we
add the corresponding symbolic permission to R. Finally, like accessibility predicates, we allow
optimistic consumption of predicate instances. In this case the symbolic permission representing
the predicate instance is added as a run-time check.
   When consuming any accessibility predicate or predicate instance, the symbolic permission
is always added to a set Θ. This allows speciﬁcation of checks for separation. When consuming
acc(𝑥 .𝑓 ) ∗ acc(𝑦.𝑓 ), if acc(𝑥 .𝑓 ) is optimistically assumed while acc(𝑦.𝑓 ) is statically veriﬁed, the
run-time check for acc(𝑥 .𝑓 ) does not imply that its permission is disjoint from that of 𝑦.𝑓 . There-
fore additional checks for separation are added when consuming a separating conjunction such
as 𝜙 1 ∗ 𝜙 2 . If no run-time check for permissions exists, all permissions must have been consumed
from H or H and thus separation may be assumed. However, if a symbolic permission is contained
in R we can no longer assume separation. Thus we add a run-time check sep(Θ1 , Θ2 ) where Θ1 is
the set of symbolic permissions collected while consuming 𝜙 1 and likewise for Θ2 and 𝜙 2 .

3.6   Producing formulas
Since a formula is only produced when we can assume its validity, producing a gradual formula
does not require any optimistic assumptions, thus we do not need to calculate any run-time checks.
When producing an imprecise formula, we produce the precise portion and set 𝜄 = ⊤. All other
rules from §2.5 are left unchanged.

3.7   Executing statements
All rules from §2.6 are left unchanged. While it may seem natural to calculate run-time checks
while determining execution transitions (as in the exec algorithm of DiVincenzo et al. [2022]),
we found that this unnecessarily complicates statements of soundness since symbolic execution
steps are not equivalent to dynamic execution steps. For example, a method call occurs in one step
during symbolic execution but may never complete during dynamic execution, therefore it may be
111:16                                                                               C. Zimmerman, J. DiVincenzo, and J. Aldrich


                                        SGuardAssignField                                 SGuardCall
SGuardAssign                                       𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎′, R                      𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R       𝑥 = params(𝑚)
      𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎′, R                        𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ⊲ 𝜎 ′′ , R ′              𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡 ] ] ⊢ pre(𝑚) ⊲ 𝜎 ′′ , R ′
h𝜎, 𝑥 = 𝑒; 𝑠, 𝜙˜ i ⇀ 𝜎 ′ ⊣ R, ∅         h𝜎, 𝑥 .𝑓 = 𝑒; 𝑠, 𝜙˜ i ⇀ 𝜎 ′′ ⊣ R ∪ R ′ , ∅              h𝜎, 𝑦 = 𝑚 (𝑒 ); 𝑠, 𝜙˜ i ⇀ 𝜎 ′′ ⊣
                                                                                                 R ∪ R ′ , rem(𝜎 ′′ , pre(𝑚) )
                                 
                                 
                                  ∅                                                 if 𝜙˜ is completely precise
                                 
                                 
                            ˜
                    rem(𝜎, 𝜙 ) := { h𝑝, 𝑡 i : h𝑝, 𝑡 i ∈ H(𝜎 ) } ∪
                                 
                                 
                                  { h𝑡, 𝑓 i : h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎 ) ∪ H (𝜎 ) }      otherwise
                                 


                                                    Fig. 9. Selected guard rules

   1 List append ( List l , int value )                         7   else
   2   requires ? * true                                        8       n = append ( l . next , value );
   3   ensures ? * acyclic ( result )                           9   l . next = n ;
   4 {                                                         10   result = l ;
   5   if ( l . next == NULL )                                 11 }
   6     n = singleton ( value );


                              Fig. 10. GVLC0 code for appending to an acyclic linked list


impossible to determine which symbolic execution step applies. However, assertion of run-time
checks must occur before a dynamic execution step may proceed. Therefore we cleanly delineate
between symbolic execution transitions, speciﬁed by the judgement 𝜎 ⊢ 𝑠 → 𝑠 ′ ⊣ 𝜎 ′ , and the
calculation of run-time checks.

3.8 Guarding execution
As described above, we must the assert run-time checks before the corresponding dynamic execu-
tion step occurs. Therefore we deﬁne guard judgements to calculate run-time checks which ensure
that execution can safely proceed. A guard for a method call calculates the checks necessary to
ensure that the method’s pre-condition is satisﬁed, while a guard for a ﬁeld assignment calculates
the checks necessary to ensure permission to access the assignee and evaluate the value to be
stored.
   A guard judgement Σ ⇀ 𝜎 ′ ⊣ R, Θ denotes that, at the execution state represented by Σ, when
the execution path matches the path condition in 𝜎 ′ , the run-time checks R must be checked.
Selected guard rules are deﬁned in Figure 9.
   In a guard judgement, Θ determines the exclusion frame—a set of permissions which must not
escape the executing method’s context. Its necessity and behavior is explained in §8.

3.9      Example
We now illustrate veriﬁcation of the gradually-speciﬁed method in Figure 10. We assume the def-
inition of List and acyclic from Figure 6. The gradual speciﬁcation of append ensures that all
returned lists are acyclic.
Symbolic states are tuples of the form h𝜄, H, H, 𝛾, 𝑔i. As in §2.8, we begin veriﬁcation of append
by assigning fresh symbolic values to all parameters and producing the pre-condition ? ∗ true,
which results in an imprecise state:
𝜎1 = h⊤, ∅, ∅, 𝛾, true i 𝛾 = [ l ↦→ 𝜈1, v ↦→ 𝜈2 ]

At each statement we compute the guard to ﬁnd the necessary run-time checks. The guard for
the if statement at line 5 evaluates l.next == NULL. A heap chunk for l.next is optimistically
    Sound Gradual Verification with Symbolic Execution                                                111:17


    added to H with a fresh value 𝜈 3 . This also results in a run-time check for the symbolic permission
    h𝜈 1, nexti.
    The next state 𝜎𝐴2 is computed by symbolic execution. This again evaluates l.next == NULL
    in the state 𝜎1 , which again requires the addition of an optimistic heap chunk. Since 𝜈 3 was not
    previously used in 𝜎1 it can be used again as a fresh value for symbolic execution.
     R = { h𝜈1, next i }
5 if ( l . next == NULL )
          𝜎𝐴2 = h⊤, ∅, { h next, 𝜈1 , 𝜈3 i }, 𝛾, 𝜈3 == null i

    The guard for line 6 consumes the pre-condition of singleton, which requires no run-time checks.
    Symbolic execution consumes the same pre-condition and produces the post-condition; here we
    use the fresh value 𝜈 4 for the returned value:
          R=∅
6        n = singleton ( value );
          𝜎𝐴3 = h⊤, { h acyclic, 𝜈4 i }, { h next, 𝜈1, 𝜈3 i }, 𝛾 [ n ↦→ 𝜈4 ], 𝜈3 == null i

    As in §2.8, we follow code order, instead of following each execution path individually, and dis-
    tinguish separate execution paths with color-coding. The guard at line 5 computes the checks for
    both branches of if, thus the guard is not computed at line 7. We can symbolically execute the
    else branch by adding the negation of the path condition we used previously:
7 else
          𝜎𝐵2 = h⊤, ∅, { h next, 𝜈1, 𝜈3 i }, 𝛾, 𝜈3 != null i

    The guard for line 8 consumes the pre-condition of append, which is ? ∗ true. Since the body
    of this imprecise formula is only true, no run-time checks are necessary. However, since this is
    an imprecise formula, we clear the precise and optimistic heaps (SConsumeImprecise in Figure
    8). Symbolic execution then produces the post-condition; here we use the fresh value 𝜈 5 for the
    returned value:
          R𝐵 = ∅
8        n = append ( l . next , value );
          𝜎𝐵3 = h⊤, { h acyclic, 𝜈5 i }, ∅, 𝛾 [ n ↦→ 𝜈5 ], 𝜈3 != null && 𝜈5 != null i

    We resume symbolic execution of both paths at line 9. Executing l.next = n in the state 𝜎𝐴3 does
    not require any run-time checks since it contains the heap chunk representing l.next. However,
    executing the same statement in 𝜎𝐵3 requires optimistic assumption of the symbolic permission
    hnext, 𝜈 1 i which requires a run-time check and removes the predicate instance. DiVincenzo et al.
    [2022] describe the implementation of such conditional run-time checks, but here we represent it
    with separate symbolic execution paths:
     R𝐴 = ∅ , R𝐵 = { h next, 𝜈1 i }
9 l . next = n ;
    𝜎𝐴4 = h⊤, { h acyclic, 𝜈4 i }, { h next, 𝜈1, 𝜈4 i }, 𝛾 [ n ↦→ 𝜈4 ], 𝜈3 == null i
    𝜎𝐵4 = h⊤, { h next, 𝜈1, 𝜈5 i }, ∅, 𝛾 [ n ↦→ 𝜈5 ], 𝜈3 != null && 𝜈5 != null i
     R𝐴 = ∅ , R 𝐵 = ∅
10 result = l ;
    𝜎𝐴5 = h⊤, 𝜈3 == null, { h acyclic, 𝜈4 i }, { h next, 𝜈1, 𝜈4 i }, 𝛾 [ n ↦→ 𝜈4 , result ↦→ 𝜈1 ] i
    𝜎𝐵4 = h⊤, 𝜈3 != null && 𝜈5 != null, { h next, 𝜈1, 𝜈5 i }, ∅, 𝛾 [ n ↦→ 𝜈5, result ↦→ 𝜈1 ] i

    Finally, the applicable guard at line 11 consumes the post-condition acyclic(result). Since nei-
    ther state contains a matching predicate instance, in both paths a run-time check is added for the
    symbolic permission hacyclic, 𝜈 1 i:
     R𝐴 = { h acyclic, 𝜈1 i } , R𝐵 = { h acyclic, 𝜈1 i }
  111:18                                                             C. Zimmerman, J. DiVincenzo, and J. Aldrich


11 }

  Now we have veriﬁed the method and computed all necessary run-time checks.

  4 EXECUTING GVLC0
  Since soundness of static veriﬁcation requires speciﬁcation of program execution, we deﬁne execu-
  tion semantics for GVLC0 programs (including SVLC0 programs, which are a subset). This includes
  dynamic semantics for formulas, and execution semantics which dynamically assert the validity
  of every speciﬁcation. Therefore, these semantics deﬁne valid execution for GVLC0 programs.
     As explained in §1, execution semantics are based on those of C0 [Arnold 2010], while the
  semantics of formulas are based on those of GVLRP [Wise et al. 2020].

  4.1      Representation
  In this section, we formally deﬁne the data structures used during execution of GVLC0 programs:
       • A value 𝑣 ∈ Value is an integer, boolean, or object reference.
       • An object reference ℓ ∈ Ref is an identiﬁer for a particular object. As with symbolic values, we
         assume that an inﬁnite number of distinct values can be generated by the fresh function. The
         type of value represented by fresh is disambiguated by its usage.
       • An environment 𝜌 is a partial function mapping variable names to values, i.e. 𝜌 : Var ⇀ Value.
       • A heap 𝐻 : Ref × Field → Value is a function mapping object reference and ﬁeld pairs to
         values. We assume that the heap function is total, i.e. all reference and ﬁeld pairs have some
         corresponding value, but heap access is restricted during execution by a set of access permissions
         𝛼 ∈ P (Ref × Field). This reﬂects the semantics of IDF [Smans et al. 2012]. A heap location
         hℓ, 𝑓 i is owned if it is contained in the currently-applicable set of access permissions.
       • A stack frame is a triple h𝛼, 𝜌, 𝑠i containing of a set of owned permissions 𝛼, a local environ-
         ment 𝜌, and a statement 𝑠. A stack S is a list of stack frames – either h𝛼, 𝜌, 𝑠i · S for some
         other S, or the empty stack, denoted nil. For a non-empty stack S, 𝛼 (S), 𝜌 (S), and 𝑠 (S) refer
         to their respective components of the head element.
       • A dynamic state Γ may be a symbol init or final, or pair h𝐻, Si containing a heap 𝐻 and a non-
         empty stack S. 𝐻 (Γ) and S(Γ) reference individual components of Γ when Γ is not a symbol,
         while 𝛼 (Γ), 𝜌 (Γ), and 𝑠 (Γ) reference a component of the head element of S(Γ). 𝛼 (init) and
         𝐻 (init) are deﬁned to be ∅.

  4.2      Evaluating expressions
  Given a heap 𝐻 and environment 𝜌, the evaluation of expression 𝑒 to a value 𝑣 is represented by
  a judgement of the form h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣. This follows standard evaluation rules—variables are
  evaluated to the corresponding value in 𝜌 and ﬁeld references are evaluated to the corresponding
  value in 𝐻 . The boolean operators && and || are short-circuiting—when evaluating 𝑒 1 && 𝑒 2 , 𝑒 2 is
  only evaluated when 𝑒 1 is not true.

  4.3      Asserting formulas
  A judgement of the form h𝐻, 𝛼, 𝜌i  𝜙˜ denotes that a gradual formula 𝜙˜ is satisﬁed given a heap
  𝐻 , a set of accessible permissions 𝛼, and an environment 𝜌. Selected rules are shown in Figure 11.
  Boolean expressions are satisﬁed when they evaluate to true. An accessibility predicate acc(𝑒.𝑓 )
  is satisﬁed when the ﬁeld referenced by 𝑒.𝑓 is in the set of accessible permissions. A predicate
  instance 𝑝 (𝑒) is satisﬁed when the predicate body is satisﬁed using an environment mapping each
  predicate parameter 𝑥 to the corresponding argument 𝑒. A separating conjunction 𝜙 1 ∗𝜙 2 is satisﬁed
  when 𝜙 1 is satisﬁed using a permission set 𝛼 1 and 𝜙 2 is satisﬁed using a permission set 𝛼 2 , where
Sound Gradual Verification with Symbolic Execution                                                111:19


𝛼 1 and 𝛼 2 are disjoint subsets of 𝛼. Finally, an imprecise formula ? ∗ 𝜙 is satisﬁed exactly when 𝜙
is satisﬁed.
   A judgement of the form h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 denotes that the expression 𝑒 is framed by the given
set of permission 𝛼. This denotes that all heap locations necessary to evaluate 𝑒 are included in 𝛼.
Selected rules are shown in Figure 11.
   Note that a predicate instance 𝑝 (𝑒) is satisﬁed iﬀ the predicate body is satisﬁed. Thus dynamic ex-
ecution of GVLC0 uses equirecursive semantics for predicates [Summers and Drossopoulou 2013].
We also deﬁne equirecursive framing of formulas by the judgement h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙.      ˜ A formula is
equirecursively framed if its unrolling, the recursive expansion of referenced predicate bodies, is
framed.
   A formula 𝜙˜ is self-framed if ∀ 𝐻, 𝛼, 𝜌 : h𝐻, 𝛼, 𝜌i  𝜙˜ =⇒ h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙.     ˜ As speciﬁed in
§3.1, a speciﬁcation is a formula which is imprecise or self-framed.

4.4 Footprints
The footprint of a formula is the set of permissions necessary to assert a formula [Reynolds 2002].
There are two types of footprints for gradual formulas:
   The exact footprint of a formula is the minimal set of permissions necessary to assert and frame
a formula. Given a heap 𝐻 and environment 𝜌, T𝜙U      ˜ h𝐻, 𝜌 i denotes the exact footprint of a formula
 ˜
𝜙.
   The maximal footprint (often abbreviated to footprint) of a formula contains the exact footprint
and all permissions that are consistently implied by the formula. The maximal footprint of a com-
pletely precise formula is its exact footprint, but the maximal footprint of an imprecise formula
contains all accessible permissions. Given a heap 𝐻 , set of owned permissions 𝛼, and environment
     ˜ h𝐻, 𝛼, 𝜌 i denotes the maximal footprint of a formula 𝜙.
𝜌, ⌊𝜙⌋                                                           ˜

4.5   Executing statements
We represent the dynamic execution of program statements as small-step execution semantics
denoted by the judgement h𝐻, Si, 𝛼ˆ → h𝐻, Si, where the statement 𝑠 is executing with the initial
state h𝐻, Si, and then transitions to the next statement 𝑠 ′ with the new state h𝐻, Si. 𝛼ˆ speciﬁes
the exclusion frame, which is described below. Selected rules are shown in Figure 11. Execution
will be stuck (i.e., no further derivation will apply) when an error is encountered. For example,
execution is stuck when a formula is not satisﬁed or if some expression is not framed.
   A method call is executed by evaluating all arguments, asserting the pre-condition, and adding
a new stack frame containing the footprint of the pre-condition and the method body. After the
method body is completely executed, the post-condition is asserted and the result value in the
callee’s environment is passed to the caller’s environment.
   A loop is executed similarly to a method, but uses the loop invariant instead of a method contract.
When the loop condition is true, an iteration is executed by asserting the invariant and adding
a new stack frame for the loop body. When the body is complete, we return to the original loop
statement, allowing further iterations as long as the condition remains true. When the condition is
false, the invariant is still asserted but execution skips over the statement. These rules are speciﬁed
in §B.7.
   𝛼ˆ speciﬁes the exclusion frame – a set of permissions which may not be passed to the callee
or loop body. It is used only for executing method calls and loops. We later explain why this is
necessary for soundness in §8.
   fold and unfold statements are ignored at run-time. Explicit folding and unfolding of predicate
instances is not required because the run-time uses equirecursive semantics for predicates.
111:20                                                                                 C. Zimmerman, J. DiVincenzo, and J. Aldrich


                   AssertImprecise                                                 AssertAcc
                   h𝐻, 𝛼, 𝜌 i  𝜙  h𝐻, 𝛼, 𝜌 i ⊢frmE 𝜙                              h𝐻, 𝜌 i ⊢ 𝑒 ⇓ ℓ        hℓ, 𝑓 i ∈ 𝛼
                              h𝐻, 𝛼, 𝜌 i  ? ∗ 𝜙                                       h𝐻, 𝛼, 𝜌 i  acc(𝑒.𝑓 )
            AssertPredicate                                                    AssertConjunction
            𝑥 = predicate_params (𝑝 )      h𝐻, 𝜌 i ⊢ 𝑒 ⇓ 𝑣                     h𝐻, 𝛼 1 , 𝜌 i  𝜙 1 h𝐻, 𝛼 2 , 𝜌 i  𝜙 2
                  h𝐻, 𝛼, [𝑥 ↦→ 𝑣 ] i  predicate(𝑝 )                              𝛼1 ∩ 𝛼2 = ∅      𝛼1 ∪ 𝛼2 ⊆ 𝛼
                            h𝐻, 𝛼, 𝜌 i  𝑝 (𝑒 )                                             h𝐻, 𝛼, 𝜌 i  𝜙 1 ∗ 𝜙 2
      ExecAssignField
      h𝐻, 𝜌 i ⊢ 𝑥 ⇓ ℓ h𝐻, 𝜌 i ⊢ 𝑒 ⇓ 𝑣             h𝐻, 𝛼, 𝜌 i  acc(𝑥 .𝑓 )          h𝐻, 𝛼, 𝜌 i ⊢frm 𝑒         𝐻 ′ = 𝐻 [ hℓ, 𝑓 i ↦→ 𝑣 ]
                                                                               ′
                                     h𝐻, h𝛼, 𝜌, 𝑥 .𝑓 = 𝑒; 𝑠 i · Si, 𝛼ˆ → h𝐻 , h𝛼, 𝜌, 𝑠 i · Si
           ExecCallEnter
                                 𝑥 = params(𝑚)      h𝐻, 𝜌 i ⊢ 𝑒 ⇓ 𝑣                h𝐻, 𝛼, 𝜌 i ⊢frm 𝑒
                        𝜌 ′ = [𝑥 ↦→ 𝑣 ]           ˆ 𝜌 ′ i  pre(𝑚)
                                          h𝐻, 𝛼 \ 𝛼,                               𝛼 ′ = ⌊pre(𝑚) ⌋ h𝐻, 𝛼 \𝛼,
                                                                                                          ˆ 𝜌i
           h𝐻, h𝛼, 𝜌, 𝑦 = 𝑚 (𝑒 ); 𝑠 i · Si, 𝛼ˆ → h𝐻, h𝛼 ′ , 𝜌 ′ , body(𝑚); skipi · h𝛼 \ 𝛼 ′ , 𝜌, 𝑦 = 𝑚 (𝑒 ); 𝑠 i · Si
               ExecCallExit
               h𝐻, 𝛼 ′ , 𝜌 ′ i  post (𝑚)      𝜌 ′′ = 𝜌 [𝑦 ↦→ 𝜌 ′ (result) ]          𝛼 ′′ = 𝛼 ∪ ⌊post(𝑚) ⌋ h𝐻, 𝛼 ′ , 𝜌 ′ i
                                 ′    ′
                         h𝐻, h𝛼 , 𝜌 , skipi · h𝛼, 𝜌, 𝑦 = 𝑚 (𝑒 ); 𝑠 i · Si, 𝛼ˆ → h𝐻, h𝛼, 𝜌, 𝑠 i · Si


                         Fig. 11. Selected formal rules for dynamic semantics of GVLC0 .



   The entire set of possible execution steps for a program Π is determined by judgements of the
form Π ⊢ Γ, 𝛼ˆ → Γ ′ , which denote that execution transitions from Γ to Γ ′ , using the exclusion
frame 𝛼.
       ˆ From the init state, execution may only step to the entry statement, and then execution
follows the rules described above.

5     CORRESPONDENCE
Before formalizing soundness, we must specify the correspondence between veriﬁcation and dy-
namic states. We include invariants which depend on concrete values, such as separation, in this
correspondence relation. Finally, we specify the behavior of run-time checks in a dynamic state.

5.1      State correspondence
A dynamic environment 𝜌 models a symbolic store 𝛾 via a valuation 𝑉 when 𝜌 𝑉 𝛾. This denotes
that ∀ 𝑥 ↦→ 𝑡 ∈ 𝛾 : 𝑥 ↦→ 𝑉 (𝑡) ∈ 𝜌.
   A heap 𝐻 and set of permissions 𝛼 model a precise heap H when h𝐻, 𝛼i 𝑉 H. This denotes that
for all ﬁeld chunks h𝑓 , 𝑡, 𝑡 ′ i ∈ H, 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ) and h𝑉 (𝑡), 𝑓 i ∈ 𝛼. Also, for all predicate
chunks h𝑝, 𝑡i, the corresponding predicate body is true using given arguments 𝑉 (𝑡). Additionally,
the footprint represented by each heap chunk must be disjoint.
   The footprint of a heap chunk, given valuation 𝑉 and heap 𝐻 , is denoted 𝑉 LℎM𝐻 . The footprint of
a ﬁeld chunk h𝑓 , 𝑡, 𝑡 ′ i is {h𝑉 (𝑡), 𝑓 i}. The footprint of a predicate chunk h𝑝, 𝑡 i is the exact footprint
of the predicate when applied to the arguments 𝑉 (𝑡).
   𝐻 and 𝛼 model an optimistic heap H when h𝐻, 𝛼i 𝑉 H . This has the same requirements as
that for H, except that heap chunks are allowed to overlap.
   𝐻 , 𝛼, and 𝛼 model a symbolic state when h𝐻, 𝛼, 𝜌i 𝑉 𝜎. This denotes that 𝐻 and 𝛼 model both
H(𝜎) and H (𝜎), 𝜌 models 𝛾, and the path condition is true—𝑉 (𝑔(𝜎)) = true.
   We also refer to these relations as correspondence—h𝐻, 𝛼, 𝜌i 𝑉 𝜎 denotes that the symbolic
state 𝜎 corresponds to 𝐻 , 𝛼, and 𝜌.
Sound Gradual Verification with Symbolic Execution                                                            111:21


                                                                           h𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡 ) ] i  predicate(𝑝 )
    𝑉 (𝑡 ) = true       h𝑉 (𝑡 ), 𝑓 i ∈ 𝛼       𝑉 LΘ1 M𝐻 ∩ 𝑉 LΘ2 M𝐻 = ∅          𝑥 = predicate_params(𝑝 )
    h𝐻, 𝛼 i ⊢𝑉 𝑡       h𝐻, 𝛼 i ⊢𝑉 h𝑡, 𝑓 i      h𝐻, 𝛼 i ⊢𝑉 sep(Θ1 , Θ2 )              h𝐻, 𝛼 i ⊢𝑉 h𝑝, 𝑡 i


                                   Fig. 12. Rules for run-time check assertions




   Finally, a veriﬁcation state Σ corresponds to a dynamic state Γ with valuation 𝑉 if Σ = Γ (i.e., Σ
and Γ are the same symbol), or h𝐻 (𝐻 ), 𝛼 (Γ), 𝜌 (Γ)i 𝑉 𝜎 (Σ) and 𝑠 (Γ) = 𝑠 (Σ). In other words, the
heap and head stack frame of Γ model the symbolic state of Σ, and the statement in the head stack
frame is syntactically the same statement as that of Σ.

5.2 Run-time checks
We also deﬁne the semantics of run-time checks using valuations. The judgement h𝐻, 𝛼i ⊢𝑉 𝑟
denotes the assertion of a run-time check 𝑟 , given a valuation 𝑉 , a heap 𝐻 , and a set of owned
permissions 𝛼. Likewise, h𝐻, 𝛼i ⊢𝑉 R denotes the assertion of all run-time checks contained in R.
Formal rules are given in Figure 12.

6     SOUNDNESS
We can now state the soundness of our static veriﬁer. We slightly modify a traditional progress/p-
reservation statement of soundness in order to accommodate run-time checks.

6.1     Corresponding valuations
For most symbolic execution judgements, we deﬁne a corresponding valuation, inspired by the
valuations used in Khoo et al. [2010]. This deﬁnes how symbolic values used in the judgement
are mapped to concrete values. To calculate the corresponding valuation we require an initial
valuation, which deﬁnes the valuation for all symbolic values contained by the input symbolic state,
and a dynamic heap, which deﬁnes the valuation for optimistically-added ﬁelds. A corresponding
valuation 𝑉 ′ must extend the initial valuation 𝑉 , i.e. 𝑉 ′ (𝑡) = 𝑉 (𝑡) for all 𝑡 ∈ dom(𝑉 ).
   We denote the corresponding valuation for a judgement J , initial valuation 𝑉 , and heap 𝐻 by
𝑉 [J | 𝐻 ]. The deﬁnition for each judgement type is deﬁned in the appendix which contains the
corresponding proofs for that judgement. Each corresponding valuation is deﬁned by induction
on the judgement derivation, specifying the corresponding valuation for each derivation rule. The
judgment is nondeterministic if only the input state is considered, but knowing the output state
resolves this nondeterminism. When the judgement and heap are clear from context, we simply
reference the corresponding valuation extending 𝑉 .

6.2     Valid states
A valid state is a dynamic state which is completely characterized by veriﬁcation states. If Γ = init
this is trivially true. For a dynamic state h𝐻, Si, we require that the head stack frame corresponds
to a reachable veriﬁcation state. We also require that all other stack frames are partially validated
by some reachable veriﬁcation state.
   If a stack frame is executing a method call, partial validation is characterized by the stack frame
and heap modeling a reachable symbolic state for that program point, with the callee’s precondi-
tion consumed. For the full deﬁnition refer to deﬁnition 32.
111:22                                                           C. Zimmerman, J. DiVincenzo, and J. Aldrich


6.3 Progress and preservation
Our statement of progress is split into two parts. First, theorem 1 states that if Γ is a valid state and
Γ satisﬁes the run-time checks calculated by a guard with a path condition that matches the current
dynamic state, then dynamic execution proceeds. Second, theorem 2 states that we can always ﬁnd
the guard necessary to apply theorem 1—a guard whose path condition matches. Thus, theorem 2
represents completeness of symbolic execution with respect to possible dynamic execution paths.
Together these theorems show that, in a valid state, the only possible way for execution to be stuck
is when the run-time checks cannot be asserted.
Theorem 1 (Progress part 1). For some program Π, let Γ be some dynamic state validated by Σ
and 𝑉 . If Σ ⇀ 𝜎 ⊣ R, Θ, 𝑉 ′ is the corresponding valuation extending 𝑉 , 𝑉 ′ (𝑔(𝜎)) = true, and
h𝐻, 𝛼 (Γ)i ⊢𝑉 ′ R, then Π ⊢ Γ, 𝑉 ′ LΘM𝐻 (Γ) → Γ ′ for some Γ ′ .
Theorem 2 (Progress part 2). For some program Π, let Γ be some dynamic state validated by Σ
and 𝑉 . Then Σ ⇀ 𝜎 ⊣ R, Θ for some 𝜎, R, and Θ such that 𝑉 ′ (𝑔(𝜎)) = true where 𝑉 ′ is the
corresponding valuation extending 𝑉 .
   Finally, our statement of preservation (theorem 3) assumes the antecedent and conclusion of
theorem 1—the initial state is valid and satisﬁes the run-time checks of some matching guard—
as well as a dynamic execution step to Γ ′ . By theorem 2, we know that there is such a guard
statement; i.e., we can always ﬁnd the necessary set of run-time checks. Then preservation states
that the resulting dynamic state Γ ′ is also valid.
Theorem 3 (Preservation). For some program Π, let Γ be some dynamic state validated by Σ and 𝑉 .
If Σ ⇀ 𝜎 ⊣ R, Θ, 𝑉 ′ is the corresponding valuation extending 𝑉 , 𝑉 ′ (𝑔(𝜎)) = true, h𝐻, 𝛼 (Γ)i ⊢𝑉 ′
R, and Π ⊢ Γ, 𝑉 ′ LΘM𝐻 (Γ) → Γ ′ , then Γ ′ is a valid state.
   Note that our assumptions for preservation require dynamic execution to not only assert the
run-time checks represented symbolically by R, but also respect the exclusion frame represented
symbolically by Θ. The necessity and implications of this requirement are discussed in §8.
   Taken together, these theorems demonstrate that dynamic execution will never be stuck as long
as the run-time checks calculated by static veriﬁcation succeed. Further, it shows that we calculate
run-time checks for all possible execution paths. Since the dynamic execution semantics ensures all
necessary speciﬁcations are satisﬁed, this implies that the calculated run-time checks are suﬃcient.

7     CHALLENGES TO FORMALISM OF STATIC VERIFICATION
Our speciﬁcation of static veriﬁcation in §2 and §3 is formalised using non-deterministic inference
rules. This diﬀers greatly from the speciﬁcations of Schwerhoﬀ [2016] and DiVincenzo et al. [2022],
which both use a CPS-style deﬁnition for algorithms. The latter form is useful when specifying
an implementation, but makes it diﬃcult to formulate a syntactic soundness proof. Furthermore,
operational semantics allow a higher level of abstraction than pseudo-code deﬁnitions. However,
we must carefully consider whether our operational semantics represent the system which is im-
plemented.

7.1      Previous approaches
During development of our soundness proof, we attempted several formulations of soundness.
Initially we abstractly deﬁned a symbolic stack—a list of symbolic states with the form of a dynamic
stack. This approach allowed us to easily state correspondence of the entire dynamic state—each
dynamic stack frame models a corresponding symbolic stack frame.
   We found it challenging, however, to prove that this correspondence is maintained. When the
dynamic stack takes a step, we must verify that there is a corresponding symbolic stack. To address
Sound Gradual Verification with Symbolic Execution                                            111:23


this issue, we deﬁned an execution semantics for symbolic stacks. Unfortunately, this increased
the distance between our formalism and implementation, and now we also need to show that
all symbolic states are reachable during static veriﬁcation. Perhaps due to the complexity of this
approach, the proof of correspondence remained quite diﬃcult even after deﬁning this execution
semantics.
   Instead, we deﬁned a valid state primarily by the correspondence of the currently executing
dynamic stack frame with some reachable symbolic state—a symbolic state which is computed
during static veriﬁcation, with no input from dynamic execution. This resulted in a much simpler
deﬁnition of valid state.
   However, in order to completely prove preservation, we also must specify the behavior of in-
termediate stack frames – frames contained in the dynamic stack below the currently-executing
frame. Thus we provide a recursive deﬁnition for a valid partial state. For intermediate frames
containing a method call that is waiting to complete, this requires the frame to model a symbolic
state that results from consuming the callee method’s pre-condition from a reachable veriﬁcation
state. We use this to prove that the dynamic state after the method returns models the symbolic
state after symbolically executing the method call.

7.2 Verification of loops
Almost all of our symbolic execution rules are ﬁnitely non-deterministic. That is, given an input
state, there are a ﬁnite number of derivations that can apply. This is necessary since all possible
states must be computed during static veriﬁcation.
   While this property matches the ﬁnite branching of symbolic execution, we make an excep-
tion in the case of loops—speciﬁcally, the SVerifyLoop rule (Figure 5). It consumes the loop pre-
condition, havocs all variables modiﬁed by the loop body (i.e., replaces them with fresh values),
and produces the loop post-condition. Thus it replaces all symbolic values that could be modiﬁed
by the loop body with fresh values. The loop is left in place, which means that the rule can be
immediately applied again to derive yet another state. However, this is harmless because repeated
applications of this rule result in isomorphic symbolic states—states which represent the same state
but with diﬀerent symbolic values. Since the exact symbolic values do not matter, these are equiva-
lent states from the perspective of static veriﬁcation. Therefore, even though we allow unbounded
non-determinism, an implementation such as Gradual C0 can compute all possible states (as deter-
mined by our formal model) up to this equivalence. In other words, unbounded non-determinism
is an artifact of our formalization that does not aﬀect an implementation.
   This exception is motivated by a disconnect between our formal model and the implementa-
tion of Gradual C0 [DiVincenzo et al. 2022]. In our formalism, run-time checks are computed as
symbolic values and lack a representation in terms of the source. Furthermore, we interpret these
run-time checks by means of the valuation function, which we only extend with fresh values as
dynamic execution proceeds. Therefore, the references in a run-time check are ﬁxed – for example,
the validity of a check does not change when the heap is updated, since the heap reference has
already been fully evaluated against the symbolic heap.
   Consider the example in Figure 13. A new object reference ℓ1 is allocated by create at line 9.
Then we consume the loop pre-condition ? ∗ true, which results in an imprecise state with empty
symbolic heaps. Thus we cannot statically assert access to x.value in the loop body (line 11). How-
ever, we optimistically assume access and produce a run-time check representing acc(x.value).
In our formalism, x is symbolically evaluated to a symbolic value 𝜈 1 and the corresponding val-
uation contains the mapping 𝜈 1 ↦→ ℓ1 . Thus the symbolic run-time check is h𝜈 1, valuei, which
succeeds since the dynamic state owns hℓ1 , valuei. This permission is then lost when consume is
111:24                                                               C. Zimmerman, J. DiVincenzo, and J. Aldrich


   1   Cell create ()                                8 int main () {
   2   requires true ensures ?                       9   x = create ();
   3   { result = alloc ( Cell ); }                 10   while ( true ) invariant ? * true {
   4                                                11     x . value = 1;
   5   int consume ( Cell c)                        12     consume ( x );
   6   requires acc ( c . value ) ensures true      13     x = create ();
   7   { ··· }                                      14   }
                                                    15   result = 0;
                                                    16 }


                     Fig. 13. Example illustrating the neccessity of the SVerifyLoop rule.



executed (line 12), but a new reference ℓ2 is allocated at line 13, and the dynamic environment is
updated with x ↦→ ℓ2 .
   During the next iteration of the loop, if we directly applied the same run-time check, this would
again require the run-time check h𝜈 1 , valuei. However, this would fail since the dynamic state no
longer owns hℓ1 , valuei. But the run-time check should reference ℓ2 , since the check is intended
to represent acc(x.value), and x ↦→ ℓ2 in the dynamic state.
   This contrasts with the implementation of run-time checks in Gradual C0, which translates the
symbolic checks into source expressions. For the example described, Gradual C0 directly inserts
the assertion acc(x.value). The expression x.value is then re-evaluated every time this assertion
is checked.
   SVerifyLoop ﬁxes this mismatch by allowing our formal model to be updated with new sym-
bolic values. With this rule, we can continue execution using a new symbolic state where we havoc
x, since it is modiﬁed by the loop body, and consume the loop invariant ? ∗ true again. Thus we
begin with a symbolic state with empty symbolic heaps and a symbolic store containing x ↦→ 𝜈 2 ,
where 𝜈 2 is a fresh value. We deﬁne a new valuation 𝑉 ′ where new symbolic values are mapped
to the current dynamic state, i.e. 𝑉 ′ (𝜈 2 ) = ℓ2 since x ↦→ ℓ2 in the dynamic state. The new symbolic
state is isomorphic to the state used during the initial symbolic execution, since it also began ex-
ecution of the body with empty symbolic heaps. We will again optimistically evaluate x.value,
which produces a new run-time check for the symbolic permission h𝜈 2, valuei, thus we will check
access to hℓ2 , valuei, and therefore our run-time checks succeed.
   Finally, since this rule introduces more symbolic states in our formal model, this means that our
soundness theorems are stronger than they would be otherwise; i.e., the soundness result holds
for strictly more cases. As our example demonstrates, we want to consider these additional cases
since they are already permitted by Gradual C0 due to its source-level run-time checks. Therefore,
this additional rule allows us to abstract away the re-evaluation of source-level checks, allowing
us to reason with ﬁxed symbolic values.

8 UNSOUNDNESS OF GRADUAL C0
While attempting to prove the soundness of Gradual C0, we discovered that its implementation
[DiVincenzo et al. 2022] allows unsound behavior, and have communicated this to the authors.
This unsoundness results from the combination of imprecise speciﬁcations, static veriﬁcation with
isorecursive predicates, and run-time checking with equirecursive predicates.

8.1 Example
  We show an example which exhibits this behavior in Figure 14. At line 14 imprecise() is folded,
thus ? ∗ true is consumed, and the predicate chunk is added to the symbolic heap. At this point
Sound Gradual Verification with Symbolic Execution                                                           111:25


                                                         10 int test ()
   1   struct Cell { int value ; }
                                                         11   requires true
   2   predicate imprecise () = ? * true
                                                         12   ensures result == 0
   3   void set ( Cell c , int v )
                                                         13 {
   4     requires imprecise ()
                                                         14   fold imprecise ();
   5     ensures true
                                                         15   Cell c = alloc ( Cell );
   6   {
                                                         16   c . value = 0;
   7     unfold imprecise ();
                                                         17   set (c , 1);
   8     c . value = v ;
                                                         18   result = c . value ;
   9   }
                                                         19 }


                     Fig. 14. Example exhibiting unsoundness of DiVincenzo et al. [2022].2


H = {himprecisei}. In lines 15-16 a new Cell is allocated and its value is initialized to 0. At this
point H = {himprecisei, hvalue, 𝑡 1 , 0i}, where c ↦→ 𝑡 1 .
   At line 17, the set method is called. Thus the precondition—imprecise()—is consumed, result-
ing in H = {hvalue, 𝑡 1, 0i}. The postcondition—true—is then produced, which does not change
the symbolic state. In this symbolic state c.value ↦→ 0. Then line 18 adds the mapping result ↦→ 0
to the symbolic store, which allows the postcondition result == 0 to be consumed successfully.
Now test is valid and no run-time checks are required in its body. Symbolic execution of the set
method shows that this method is also valid but requires a check representing acc(c.value) at
line 16.
   Now we consider dynamic execution of the test method. We ﬁrst use no exclusion frame (i.e.
using ∅ for every occurrence of 𝛼ˆ in the rules).
   The fold at line 14 is ignored, a new Cell is allocated and initialized at lines 15-16, and the
set method is called at line 17. The formula imprecise() is not completely precise, therefore
⌊imprecise()⌋ h𝐻, 𝛼, 𝜌 i = 𝛼. Thus all of the caller’s owned permissions are passed to set. The as-
sertion for imprecise() succeeds since its equirecursive unrolling is simply ? ∗ true. Likewise,
the assertion for acc(c.value) when executing line 8 also succeeds since the required permis-
sions were passed from test. After returning from set, c.value ↦→ 1 in the dynamic state, thus
result ↦→ 1 after executing line 18. However, the postcondition result == 0 cannot be asserted,
therefore execution is stuck.
   Since DiVincenzo et al. [2022] does not implement an exclusion frame, execution proceeds as
described above, except that only the calculated run-time checks are asserted. Therefore the test
method returns 1, which contradicts its contract. Wise et al. [2020] follows the dynamic execution
behavior described above, but since it checks every assertion at run-time, execution halts and
soundness is preserved.

8.2 Diagnosis
As described above, the caller’s permissions are passed to set, thus the set of permissions owned
by test is empty during execution of set. But we calculated that after consuming pre(set) the
symbolic heap still contains the ﬁeld chunk representing c.value. Therefore heap chunks which
are included in the frame of set during dynamic execution are not removed by consume during
symbolic execution, thus symbolic execution does not accurately represent dynamic execution.

8.3 Possible solutions
At ﬁrst this appears to be an error of static veriﬁcation, and thus we could address this by making
static veriﬁcation more conservative. More speciﬁcally, we could require a stronger invariant of
2 void methods are used for clarity since they can be trivially translated to the formally deﬁned grammar.
111:26                                                         C. Zimmerman, J. DiVincenzo, and J. Aldrich


the precise heap: the maximal footprint represented by predicate chunks cannot overlap. This
contrasts with our current deﬁnition, where the exact footprint represented by a predicate chunk
must be disjoint from that of all other predicate chunks.
   For example, we could clear the symbolic heaps when consuming any formula that is not com-
pletely precise (i.e., the recursive unfolding contains an imprecise formula). When this occurs, we
would also need to use an imprecise state, so that the existence of the removed permissions can
be optimistically assumed. This would result in empty symbolic heap after line 17 in Figure 14,
and a run-time check for the value of result would be required before returning from test, thus
soundness is preserved.
   This would allow maximal footprints of predicate chunks to overlap in the symbolic heap, but
when consuming a predicate instance, all potentially overlapping predicate chunks would be re-
moved. Thus, after some predicate instance is consumed, its maximal footprint would not overlap
with any permission represented by a heap chunk contained in the symbolic heap.
   Alternatively, we could achieve soundness by removing any predicate instance that is not com-
pletely precise when additional permissions are added to the precise heap. Similar to the previous
option, we would also need to use an imprecise state when this occurs. In the example, that would
(perhaps unintuitively) remove the imprecise() predicate when adding permissions for the alloc
statement. This would ensure that the maximal footprint of heap chunks in the symbolic heap
never overlap.
   Unfortunately, both of these options reduce the number of assertions that can be statically dis-
charged when verifying gradual programs, thus more run-time checks would be necessary. Fur-
thermore, the run-time checks require checking a predicate instance, which can be quite costly
since this traverses the entire unfolding of the predicate.
   Furthermore, allowing the predicate instance folded at line 14 to aﬀect permissions allocated
afterward, at line 15, seems counter-intuitive. This invalidates the intuitive assumption that the
set of permissions represented by a folded predicate instqance will not change while it remains
folded. Furthermore this behavior breaks the semantics of ?, as speciﬁed in Wise et al. [2020], since
no logically consistent strengthening of the imprecise predicate allows it to include permissions
allocated after its body is folded.
   This indicates that the semantics of dynamic execution should be modiﬁed to exclude access
permission for c.value, which is allocated after imprecise() is folded, from being passed to
set, which is a precise formula that only requires imprecise(). Then execution would fail at
line 8 in Figure 14. To accomplish this, we have introduced the concept of an exclusion frame –
a set of permissions which cannot be passed to a callee. This exclusion frame is calculated by
symbolic execution, and passed to dynamic execution in much the same way as run-time checks.
It is represented by Θ in the guard judgement (§9), which also calculates R, and is translated to
dynamic permissions using a valuation.
   The guard rules in Figure 9 calculate the exclusion frame by the rem helper function, after con-
suming the pre-condition of a method. If the pre-condition is completely precise, then Θ = ∅, thus
execution of an SVLC0 program is not aﬀected. Otherwise, Θ contains all permissions currently
contained in the symbolic heaps. In Figure 14, since the pre-condition of set is not completely
precise, Θ = {h𝑡 1 , valuei} when calculating the guard statement at line 17. At run-time this is
translated to 𝛼ˆ = {hℓ, valuei} where c ↦→ ℓ. Then all permissions except hℓ, valuei are passed to
set. Thus the run-time check for acc(c.value) at line 8 cannot be asserted.
   This addresses the intuitive and semantic problems described above. The isorecursive instance
of imprecise referenced in the pre-condition of set should not represent access to c.value since
it was folded before c was allocated. Under this interpretation we would expect a failure at line
8, since set does not require the necessary permissions. This also matches the semantics of ?,
Sound Gradual Verification with Symbolic Execution                                            111:27


as deﬁned in [Wise et al. 2020], since the predicate instance folded at line 14 cannot consistently
imply access to the heap location allocated at line 15.


8.4   Implementation
There are important implementation challenges that must be addressed before this change can
be implemented in Gradual C0 [DiVincenzo et al. 2022]. Currently, Gradual C0 constructs sets
of permissions at run-time—before calling a method, for example—by recursively unfolding the
neccessary speciﬁcation and collecting all permissions. However, this method cannot be used to
create the exclusion frame, since these permissions are not necessarily represented by a speciﬁca-
tion. But we expect that a translation algorithm can be developed which generates the source code
necessary to compute the exclusion frame at run time. This is similar to the existing translation
algorithm described by DiVincenzo et al. [2022], which translates symbolic run-time checks into
source code that implements the desired assertion.
   Also, note that we calculate the exclusion frame using information from symbolic execution of
a particular statement. In other words, if method m calls m′ , we can calculate the exclusion frame
necessary for calling m′ without considering the exclusion frame used to call m. This implies that
exclusion frames can be dropped when entering a completely precise method, and then instanti-
ated again when a precise method calls an imprecise method. This is similar to how Gradual C0
does not pass permission sets to precise methods, but reconstructs the permissions when a precise
method calls an imprecise methods. Applying this technique to exclusion frames, as described,
would ensure that exclusion frames do not aﬀect the run-time performance of methods that are
speciﬁed with completely precise speciﬁcations.


9 FUTURE WORK
There are many possible directions in which this work can be extended. We have not yet proven
the gradual guarantees for gradual veriﬁcation, as formalized in Wise et al. [2020]. These guaran-
tees formalize the notion that, given a valid program, gradual speciﬁcations may be used in place
of all static speciﬁcations without introducing errors (both during veriﬁcation and at run time).
This ensures that any errors do not arise from imprecision, but rather from an invalid program or
speciﬁcation, or (for precise speciﬁcations) from incompleteness of veriﬁcation. Our formalization
appears to satisfy this since, as described in §3, we extend the underlying static veriﬁcation algo-
rithm mainly by adding optimistic capabilities while leaving the bulk of static veriﬁcation intact.
However, we have not completed a formal proof.
   Our formalization could also be used to extend gradual veriﬁcation. Notably, gradual veriﬁcation
has not been implemented for quantiﬁed speciﬁcations or concurrent programs. Ghost code/pa-
rameters (i.e., code only necessary for supporting logical proofs) is also not supported in gradual
veriﬁcation, since the “ghost” code could be necessary for run-time checks. Our high-level deﬁni-
tion of the gradual veriﬁer could enable further development to support these techniques. Likewise,
our formalization does not capture several important concepts in Viper such as domains, fractional
permissions, and joining of symbolic execution paths. Formalizing the usage of these techniques
in Viper and proving their soundness would provide further assurance of the correctness of Viper
and provide a starting point for integrating these techniques with gradual veriﬁcation. Our for-
malization provides a basis for formally proving properties of veriﬁcation techniques (in our case,
gradual veriﬁcation) with a model that closely resembles the implementation (in our case, Grad-
ual C0). Thus modiﬁcations to our formal model can be more easily implemented and used, while
modiﬁcations to the implementation can be reﬂected in the formal model and proven sound.
111:28                                                         C. Zimmerman, J. DiVincenzo, and J. Aldrich


10 RELATED WORK
As mentioned previously, implementations of veriﬁcation using symbolic execution, such as Viper
[Schwerhoﬀ 2016], Gradual C0 [DiVincenzo et al. 2022], Smallfoot [Berdine et al. 2005], Chalice
[Leino et al. 2009], and jStar [Distefano and Parkinson 2008], often lack formal soundness proofs.
A notable exception is VeriFast [Jacobs et al. 2011], which implements veriﬁcation using symbolic
execution. The core of its veriﬁer was proven sound in Vogels et al. [2015]. This soundness proof
utilizes techniques from abstract interpretation, which may simplify proofs of veriﬁers using sym-
bolic execution. However, VeriFast uses separation logic instead of IDF.
   Several previous veriﬁers using WLP or veriﬁcation condition generation (VCG) have been di-
rectly proven sound [Herms et al. 2012; Smans et al. 2012; Vogels et al. 2009, 2010]. Several similar
veriﬁers produce a proof during veriﬁcation which may be checked to the validate soundness of
an individual veriﬁcation result [Filliâtre and Paskevich 2013; Parthasarathy et al. 2021].
   Viper [Müller et al. 2016] and Gradual C0 [DiVincenzo et al. 2022] rely on an SMT solver to im-
plement their veriﬁcation algorithms. While we have proved soundness of our formal model, this
soundness is contingent on the soundness of the SMT solver. Other work has extended soundness
to include soundness of the entire veriﬁcation system. Notably, VeriSmall [Keuchel et al. 2022], Di-
aframe [Mulder et al. 2022], and ReﬁnedC [Sammler et al. 2021] are all encoded in Iris/Coq, making
them either foundational or self-verifying.
   As described before, soundness of gradual veriﬁcation based on WLP has been proven in both
Wise et al. [2020] and Bader et al. [2018]. However, Wise et al. [2020] depends on dynamically
checking all assertions, while Bader et al. [2018] does not handle abstract heap predicates.

11 CONCLUSION
The recent implementation of gradual veriﬁcation in DiVincenzo et al. [2022] promises a dramatic
reduction in the eﬀort required to verify programs. However, this requires conﬁdence in the cor-
rectness of their gradual veriﬁcation system, Gradual C0, as well as its underlying static veriﬁcation
system, Viper. In this work, we formalized symbolic execution in (a subset of) Viper and proved it
sound, in addition to formalizing gradual veriﬁcation in Gradual C0 and proving it sound. During
this work we found a soundness bug in Gradual C0, which we communicated to DiVincenzo et al.
[2022] along with possible solutions. This illustrates that, while correctness in gradual veriﬁers
can be guaranteed, it should not be assumed without rigorous proof. There are a few interesting
directions we could take this work: (1) proving that Gradual C0 adheres to the gradual guarantee
as formalized by Wise et al. [2020], which is a very important property of gradual veriﬁers that
should be straightforward to prove with our formal system, and (2) using our formalism to explore
new directions in gradual veriﬁcation like quantiﬁcation or concurrency, and prove systems utiliz-
ing them sound. In general, we hope that this work serves as a strong basis for future proof work
in static and gradual veriﬁcation when using symbolic execution.

ACKNOWLEDGMENTS
We thank Jana Dunﬁeld for her helpful feedback.
   This work was supported by the National Science Foundation under Grant No. CCF-1901033
(https://www.nsf.gov/awardsearch/showAward?AWD_ID=1901033) and a Google PhD Fellowship.
Sound Gradual Verification with Symbolic Execution                                                                     111:29


REFERENCES
Rob Arnold. 2010.                  C0, an Imperative Programming Language for Novice Computer Sci-
   entists.           Master’s thesis. Department of Computer Science, Carnegie Mellon University.
   http://reports-archive.adm.cs.cmu.edu/anon/anon/usr/ftp/home/ftp/2010/CMU-CS-10-145.pdf
Vytautas Astrauskas, Aurel Bílý, Jonás Fiala, Zachary Grannan, Christoph Matheja, Peter Müller, Federico Poli,
   and Alexander J. Summers. 2022. The Prusti Project: Formal Veriﬁcation for Rust. In NASA Formal Methods
   - 14th International Symposium, NFM 2022, Pasadena, CA, USA, May 24-27, 2022, Proceedings (Lecture Notes in
   Computer Science, Vol. 13260), Jyotirmoy V. Deshmukh, Klaus Havelund, and Ivan Perez (Eds.). Springer, 88–108.
   https://doi.org/10.1007/978-3-031-06773-0_5
Johannes Bader, Jonathan Aldrich, and Éric Tanter. 2018. Gradual Program Veriﬁcation. In Veriﬁcation, Model Check-
   ing, and Abstract Interpretation - 19th International Conference, VMCAI 2018, Los Angeles, CA, USA, January 7-9,
   2018, Proceedings (Lecture Notes in Computer Science, Vol. 10747), Isil Dillig and Jens Palsberg (Eds.). Springer, 25–46.
   https://doi.org/10.1007/978-3-319-73721-8_2
Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2005. Smallfoot: Modular Automatic Assertion Checking
   with Separation Logic. In Formal Methods for Components and Objects, 4th International Symposium, FMCO 2005,
   Amsterdam, The Netherlands, November 1-4, 2005, Revised Lectures (Lecture Notes in Computer Science, Vol. 4111),
   Frank S. de Boer, Marcello M. Bonsangue, Susanne Graf, and Willem P. de Roever (Eds.). Springer, 115–137.
   https://doi.org/10.1007/11804192_6
Stefan Blom, Saeed Darabi, Marieke Huisman, and Wytse Oortwijn. 2017. The VerCors Tool Set: Veriﬁcation of Parallel
   and Concurrent Software. In Integrated Formal Methods - 13th International Conference, IFM 2017, Turin, Italy, September
   20-22, 2017, Proceedings (Lecture Notes in Computer Science, Vol. 10510), Nadia Polikarpova and Steve A. Schneider (Eds.).
   Springer, 102–110. https://doi.org/10.1007/978-3-319-66845-1_7
Dino Distefano and Matthew J. Parkinson. 2008. JStar: Towards Practical Veriﬁcation for Java. SIGPLAN Not. 43, 10 (oct
   2008), 213–226. https://doi.org/10.1145/1449955.1449782
Jenna DiVincenzo, Ian McCormack, Hemant Gouni, Jacob Gorenburg, Mona Zhang, Conrad Zimmerman, Joshua Sun-
   shine, Éric Tanter, and Jonathan Aldrich. 2022. Gradual C0: Symbolic Execution for Eﬃcient Gradual Veriﬁcation.
   arXiv:2210.02428 [cs.LO]
Marco Eilers and Peter Müller. 2018. Nagini: A Static Veriﬁer for Python. In Computer Aided Veriﬁcation - 30th International
   Conference, CAV 2018, Held as Part of the Federated Logic Conference, FloC 2018, Oxford, UK, July 14-17, 2018, Proceedings,
   Part I (Lecture Notes in Computer Science, Vol. 10981), Hana Chockler and Georg Weissenbacher (Eds.). Springer, 596–603.
   https://doi.org/10.1007/978-3-319-96145-3_33
Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3 - Where Programs Meet Provers. In Programming
   Languages and Systems - 22nd European Symposium on Programming, ESOP 2013, Held as Part of the European
   Joint Conferences on Theory and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013. Proceedings
   (Lecture Notes in Computer Science, Vol. 7792), Matthias Felleisen and Philippa Gardner (Eds.). Springer, 125–128.
   https://doi.org/10.1007/978-3-642-37036-6_8
Ronald Garcia, Alison M. Clark, and Éric Tanter. 2016.                 Abstracting Gradual Typing.           (2016), 429–442.
   https://doi.org/10.1145/2837614.2837670
Paolo Herms, Claude Marché, and Benjamin Monate. 2012. A Certiﬁed Multi-prover Veriﬁcation Condition Generator. In
   Veriﬁed Software: Theories, Tools, Experiments - 4th International Conference, VSTTE 2012, Philadelphia, PA, USA, January
   28-29, 2012. Proceedings (Lecture Notes in Computer Science, Vol. 7152), Rajeev Joshi, Peter Müller, and Andreas Podelski
   (Eds.). Springer, 2–17. https://doi.org/10.1007/978-3-642-27705-4_2
C. A. R. Hoare. 1969. An Axiomatic Basis for Computer Programming. Commun. ACM 12, 10 (oct 1969), 576–580.
   https://doi.org/10.1145/363235.363259
Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens. 2011. Ver-
   iFast: A Powerful, Sound, Predictable, Fast Veriﬁer for C and Java. In NASA Formal Methods - Third Interna-
   tional Symposium, NFM 2011, Pasadena, CA, USA, April 18-20, 2011. Proceedings (Lecture Notes in Computer Science,
   Vol. 6617), Mihaela Gheorghiu Bobaru, Klaus Havelund, Gerard J. Holzmann, and Rajeev Joshi (Eds.). Springer, 41–55.
   https://doi.org/10.1007/978-3-642-20398-5_4
Steven Keuchel, Sander Huyghebaert, Georgy Lukyanov, and Dominique Devriese. 2022. Veriﬁed Symbolic Execution with
   Kripke Speciﬁcation Monads (and No Meta-Programming). Proc. ACM Program. Lang. 6, ICFP, Article 97 (aug 2022),
   31 pages. https://doi.org/10.1145/3547628
Yit Phang Khoo, Bor-Yuh Evan Chang, and Jeﬀrey S. Foster. 2010. Mixing Type Checking and Symbolic Exe-
   cution. In Proceedings of the 31st ACM SIGPLAN Conference on Programming Language Design and Implementa-
   tion (Toronto, Ontario, Canada) (PLDI ’10). Association for Computing Machinery, New York, NY, USA, 436–447.
   https://doi.org/10.1145/1806596.1806645
111:30                                                                        C. Zimmerman, J. DiVincenzo, and J. Aldrich


K. Rustan M. Leino, Peter Müller, and Jan Smans. 2009.                Veriﬁcation of Concurrent Programs with Chalice.
   In Foundations of Security Analysis and Design V, FOSAD 2007/2008/2009 Tutorial Lectures (Lecture Notes in
   Computer Science, Vol. 5705), Alessandro Aldini, Gilles Barthe, and Roberto Gorrieri (Eds.). Springer, 195–222.
   https://doi.org/10.1007/978-3-642-03829-7_7
Ike Mulder, Robbert Krebbers, and Herman Geuvers. 2022. Diaframe: Automated Veriﬁcation of Fine-Grained Concurrent
   Programs in Iris. In Proceedings of the 43rd ACM SIGPLAN International Conference on Programming Language Design
   and Implementation (San Diego, CA, USA) (PLDI 2022). Association for Computing Machinery, New York, NY, USA,
   809–824. https://doi.org/10.1145/3519939.3523432
Peter Müller, Malte Schwerhoﬀ, and Alexander J. Summers. 2016. Viper: A Veriﬁcation Infrastructure for Permission-Based
   Reasoning. In Veriﬁcation, Model Checking, and Abstract Interpretation - 17th International Conference, VMCAI 2016, St.
   Petersburg, FL, USA, January 17-19, 2016. Proceedings (Lecture Notes in Computer Science, Vol. 9583), Barbara Jobstmann
   and K. Rustan M. Leino (Eds.). Springer, 41–62. https://doi.org/10.1007/978-3-662-49122-5_2
Matthew Parkinson and Gavin Bierman. 2005. Separation Logic and Abstraction. SIGPLAN Not. 40, 1, 247–258.
   https://doi.org/10.1145/1047659.1040326
Gaurav Parthasarathy, Peter Müller, and Alexander J. Summers. 2021. Formally Validating a Practical Veriﬁcation Con-
   dition Generator. In Computer Aided Veriﬁcation - 33rd International Conference, CAV 2021, Virtual Event, July 20-23,
   2021, Proceedings, Part II (Lecture Notes in Computer Science, Vol. 12760), Alexandra Silva and K. Rustan M. Leino (Eds.).
   Springer, 704–727. https://doi.org/10.1007/978-3-030-81688-9_33
John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In 17th IEEE Symposium on Logic
   in Computer Science (LICS 2002), 22-25 July 2002, Copenhagen, Denmark, Proceedings. IEEE Computer Society, 55–74.
   https://doi.org/10.1109/LICS.2002.1029817
Michael Sammler, Rodolphe Lepigre, Robbert Krebbers, Kayvan Memarian, Derek Dreyer, and Deepak Garg. 2021. ReﬁnedC:
   Automating the Foundational Veriﬁcation of C Code with Reﬁned Ownership Types. In Proceedings of the 42nd ACM
   SIGPLAN International Conference on Programming Language Design and Implementation (Virtual, Canada) (PLDI 2021).
   Association for Computing Machinery, New York, NY, USA, 158–174. https://doi.org/10.1145/3453483.3454036
Malte Schwerhoﬀ. 2016. Advancing Automated, Permission-Based Program Veriﬁcation Using Symbolic Execution. Ph. D.
   Dissertation. ETH Zurich, Zürich, Switzerland. https://doi.org/10.3929/ETHZ-A-010835519
Jan Smans, Bart Jacobs, and Frank Piessens. 2012. Implicit Dynamic Frames. ACM Trans. Program. Lang. Syst. 34, 1, Article
   2 (may 2012), 58 pages. https://doi.org/10.1145/2160910.2160911
Alexander J. Summers and Sophia Drossopoulou. 2013. A Formal Semantics for Isorecursive and Equirecursive State
   Abstractions. In ECOOP 2013 - Object-Oriented Programming - 27th European Conference, Montpellier, France, July
   1-5, 2013. Proceedings (Lecture Notes in Computer Science, Vol. 7920), Giuseppe Castagna (Ed.). Springer, 129–153.
   https://doi.org/10.1007/978-3-642-39038-8_6
Frédéric Vogels, Bart Jacobs, and Frank Piessens. 2009. A Machine Checked Soundness Proof for an Intermediate Veriﬁca-
   tion Language. In SOFSEM 2009: Theory and Practice of Computer Science, 35th Conference on Current Trends in Theory
   and Practice of Computer Science, Spindleruv Mlýn, Czech Republic, January 24-30, 2009. Proceedings (Lecture Notes in
   Computer Science, Vol. 5404), Mogens Nielsen, Antonín Kucera, Peter Bro Miltersen, Catuscia Palamidessi, Petr Tuma,
   and Frank D. Valencia (Eds.). Springer, 570–581. https://doi.org/10.1007/978-3-540-95891-8_51
Frédéric Vogels, Bart Jacobs, and Frank Piessens. 2010. A Machine-Checked Soundness Proof for an Eﬃcient Veriﬁcation
   Condition Generator. In Proceedings of the 2010 ACM Symposium on Applied Computing (Sierre, Switzerland) (SAC ’10).
   Association for Computing Machinery, New York, NY, USA, 2517–2522. https://doi.org/10.1145/1774088.1774610
Frédéric Vogels, Bart Jacobs, and Frank Piessens. 2015. Featherweight VeriFast. Log. Methods Comput. Sci. 11, 3 (2015).
   https://doi.org/10.2168/LMCS-11(3:19)2015
Jenna Wise, Johannes Bader, Cameron Wong, Jonathan Aldrich, Éric Tanter, and Joshua Sunshine. 2020. Gradual Veri-
   ﬁcation of Recursive Heap Data Structures. Proc. ACM Program. Lang. 4, OOPSLA, Article 228 (nov 2020), 28 pages.
   https://doi.org/10.1145/3428296
Sound Gradual Verification with Symbolic Execution            111:31


                                                 Appendices
   A    Grammar                                                  32
   B    Run-time Semantics                                       32
   B.1    Deﬁnitions                                             32
   B.2    Evaluation                                             33
   B.3    Formulas                                               34
   B.4    Footprints                                             34
   B.5    Framing                                                35
   B.6    Assertions                                             37
   B.7    Execution                                              38
   B.8    Reachable transitions                                  39
   C    Symbolic Execution                                       40
   C.1    Deﬁnitions                                             40
   C.2    Valuations                                             41
   C.3    Footprints                                             41
   C.4    Correspondence                                         42
   C.5    Run-time checks                                        42
   C.6    Evaluation                                             42
   C.7    Deterministic evaluation                               44
   C.8    Produce                                                45
   C.9    Consume                                                45
   C.10   Execute                                                47
   C.11   Veriﬁcation states                                     48
   C.12   Guards                                                 49
   C.13   Valid states                                           50
   D    Soundness                                                51
   D.1    Cross-cutting lemmas                                   51
   D.2    Evaluation                                             59
   D.3    Deterministic Evaluation                               63
   D.4    Produce                                                67
   D.5    Consume                                                71
   D.6    Progress                                               80
   D.7    Preservation                                           86
111:32                                                      C. Zimmerman, J. DiVincenzo, and J. Aldrich


A GRAMMAR
  program F S P M s                                Program deﬁnition
  S           F 𝑆{T 𝑓 }                            Struct deﬁnition
  P           F 𝑝 (T x) = 𝜙˜                       Predicate deﬁnition
  M           F 𝑇 𝑚(𝑇 𝑥) Φ 𝑠                       Method deﬁnition
  Φ                          ˜
              F requires 𝜙 ensures 𝜙   ˜           Method contract
  T           F 𝑆 | int | bool | char Type
  s           F s; s                               Statement sequence
               | skip                              No-op
               | 𝑥 =𝑒                              Variable assignment
               | 𝑥 .𝑓 = 𝑒                          Field assignment
               | 𝑥 = alloc(𝑆)                      Allocation
               | 𝑥 = 𝑚(𝑒)                          Method invocation
               | assert 𝜙˜                         Assertion
               | if 𝑒 then 𝑠 else 𝑠                Conditional
               | while 𝑒 invariant 𝜙˜ do 𝑠         Loop
               | fold 𝑝 (𝑒)                        Fold predicate
               | unfold 𝑝 (𝑒)                      Unfold predicate
  e           F 𝑙 | 𝑥 | 𝑒.𝑓 | 𝑒 ⊕ 𝑒                Expression
               | 𝑒 || 𝑒 | 𝑒 && 𝑒 | ! 𝑒
  x           F result | 𝑖𝑑                        Variable
  l           F 𝑛 | 𝑐                              Value
               | null | true | false
  𝜙˜          F ?∗𝜙 | 𝜙                            Gradual formula
  𝜙           F 𝜙 ∗ 𝜙 | 𝑝 (𝑒) | 𝑒                  Precise formula
               | if 𝑒 then 𝜙 else 𝜙
               | acc(𝑒.𝑓 )
    Where 𝑛 ∈ Z, 𝑐 ∈ Char, 𝑖𝑑 ∈ Identifier, 𝑓 ∈ Field, 𝑚 ∈ Method, 𝑝 ∈ Predicate, ⊕ ∈ {+, −, <
, >, ≤, ≥, =}
Deﬁnition 1. A program is well-formed if all the following requirements are satisiﬁed:
 • It is properly typed.
 • All loop invariants, method pre-conditions, and method post-conditions are speciﬁcations (def-
   inition 4).
 • The free variables of any method are a subset of its parameters.
 • The special variable result is not a free variable of any method.
 • No parameters appear on the left side of a variable assignment.
 • Formulas in pre-conditions only reference parameters.
 • Formulas in post-conditions only reference parameters and the special variable result.
 • If a pre-condition is imprecise, the post-condition is also imprecise.

B RUN-TIME SEMANTICS
B.1 Definitions
The rules in the following section reference an ambient program with elements denoted as follows:
 • Predicates: 𝑝 ∈ Predicate
 • Methods: 𝑚 ∈ Method
 • Structs: 𝑆 ∈ Struct
Sound Gradual Verification with Symbolic Execution                                         111:33


 • Types: 𝑇 ∈ Type
 • Variables: 𝑥 ∈ Var
 • Field identiﬁers: 𝑓 ∈ Field
 • Locations (opaque values): ℓ ∈ Location
 • Literals (integers, characters, booleans, null): 𝑙 ∈ Literal
 • Values: 𝑣 ∈ Value = Location ∪ Literal
 • Gradual formulas: 𝜙˜ ∈ F̃ormula
 • Precise formulas: 𝜙 ∈ Formula
 • Statements: 𝑠 ∈ Stmt
 • Heap: 𝐻 : Location × Field → Value
 • Permissions: 𝛼 ∈ P (Location × Field)
 • Environment: 𝜌 : Var ⇀ Value
  The following functions are deﬁned to access elements in the program:
 • default : Type → Value – Gets the default value of the given type (0, null, etc.)
 • pre : Method → F̃ormula – Gets the precondition from the declaration of the speciﬁed
   method.
 • post : Method → F̃ormula – Gets the postcondition from the declaration of the speciﬁed
   method.
 • body : Method → Stmt – Gets the body from the declaration of the speciﬁed method.
 • params : Method → Var – Gets the list of parameters from the declaration of the speciﬁed
   predicate.
 • predicate : Predicate → F̃ormula – Gets the body from the declaration of the speciﬁed
   predicate.
 • predicate_params : Predicate → Var – Gets the list of parameters from the declaration of
   the speciﬁed predicate.
 • struct : Struct → Field – Gets the list of ﬁelds from the declaration of the speciﬁed struct.

B.2    Evaluation
The relation
                                                 h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣
denotes the evaluation of an expression 𝑒 ∈ Expr to a value 𝑣 ∈ Value where 𝐻 : Value×Field →
Value represents the heap, and 𝜌 : Var ⇀ Value represents the local variable environment.

                                                EvalLiteral

                                                 h𝐻, 𝜌i ⊢ 𝑙 ⇓ 𝑙
                                              EvalVar

                                              h𝐻, 𝜌i ⊢ 𝑥 ⇓ 𝜌 (𝑥)
                                         EvalAndA
                                             h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false
                                          h𝐻, 𝜌i ⊢ 𝑒 1 && 𝑒 2 ⇓ false
                                 EvalAndB
                                  h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true        h𝐻, 𝜌i ⊢ 𝑒 2 ⇓ 𝑣 2
                                            h𝐻, 𝜌i ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑣 2
111:34                                                                  C. Zimmerman, J. DiVincenzo, and J. Aldrich

                                       EvalOrA
                                           h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true
                                        h𝐻, 𝜌i ⊢ 𝑒 1 || 𝑒 2 ⇓ true


                              EvalOrB
                              h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false         h𝐻, 𝜌i ⊢ 𝑒 2 ⇓ 𝑣 2
                                         h𝐻, 𝜌i ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑣 2


                                EvalOp
                                 h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ 𝑣 1      h𝐻, 𝜌i ⊢ 𝑒 2 ⇓ 𝑣 2
                                       h𝐻, 𝜌i ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑣 1 ⊕ 𝑣 2


                                           EvalNeg
                                             h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣
                                            h𝐻, 𝜌i ⊢ ! 𝑒 ⇓ ¬𝑣


                                         EvalField
                                              h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ
                                         h𝐻, 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝐻 (ℓ, 𝑓 )

B.3 Formulas
Formula is the set of all 𝜙 elements in the grammar, while F̃ormula is the set of all 𝜙˜ elements in
the grammar.

Deﬁnition 2. An imprecise formula 𝜙˜ is any formula in F̃ormula of the form ? ∗ 𝜙 where
𝜙 ∈ Formula.
  Otherwise, a formula 𝜙 is precise and 𝜙 ∈ Formula.

Deﬁnition 3. A formula 𝜙˜ is completely precise if there is no 𝐻, 𝛼, 𝜌 such that AssertImprecise
                                                      ˜
applies at some step in the derivation of h𝐻, 𝛼, 𝜌i  𝜙.
  In other words, a completely precise formula is precise and all predicate bodies referenced in its
equi-recursive unrolling are also precise.

Deﬁnition 4. A formula 𝜙˜ is a speciﬁcation if either 𝜙˜ is imprecise or 𝜙˜ is precise and self-framed
(deﬁnition 7).

B.4      Footprints
Deﬁnition 5. The exact footprint of a formula 𝜙˜ ∈ F̃ormula, denoted T𝜙U          ˜ h𝐻, 𝜌 i , or of an ex-
pression 𝑒, denoted T𝑒U h𝐻, 𝜌 i , is the set of permissions that must be accessed when asserting 𝜙˜ or
evaluating 𝑒.
   By lemmas 4 and 11, if 𝜙˜ is a speciﬁcation, this set is the lower bound of permissions that satisfy
 ˜
𝜙.
Sound Gradual Verification with Symbolic Execution                                                          111:35


  The calculation of exact footprints is deﬁned as follows:
                             T𝑙U h𝐻, 𝜌 i := ∅
                            T𝑥U h𝐻, 𝜌 i := ∅
                          T𝑒.𝑓 U h𝐻, 𝜌 i := T𝑒U h𝐻, 𝜌 i ; hℓ, 𝑓 i                            if h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ
                     T𝑒 1 ⊕ 𝑒 2 U h𝐻, 𝜌 i := T𝑒 1 U h𝐻, 𝜌 i ∪ T𝑒 2 U h𝐻, 𝜌 i
                    T𝑒 1 || 𝑒 2 U h𝐻, 𝜌 i := T𝑒 1 U h𝐻, 𝜌 i                             if h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true
                    T𝑒 1 || 𝑒 2 U h𝐻, 𝜌 i := T𝑒 1 U h𝐻, 𝜌 i ∪ T𝑒 2 U h𝐻, 𝜌 i           if h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false
                    T𝑒 1 && 𝑒 2 U h𝐻, 𝜌 i := T𝑒 1 U h𝐻, 𝜌 i                            if h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false
                    T𝑒 1 && 𝑒 2 U h𝐻, 𝜌 i := T𝑒 1 U h𝐻, 𝜌 i ∪ T𝑒 2 U h𝐻, 𝜌 i            if h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true
                          T! 𝑒U h𝐻, 𝜌 i := T𝑒U h𝐻, 𝜌 i
                       T? ∗ 𝜙U h𝐻, 𝜌 i := T𝜙U h𝐻, 𝜌 i
                     T𝜙 1 ∗ 𝜙 2 U h𝐻, 𝜌 i := T𝜙 1 U h𝐻, 𝜌 i ∪ T𝜙 2 U h𝐻, 𝜌 i
                        T𝑝 (𝑒)U h𝐻, 𝜌 i := Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑣 ] i ∪         if 𝑥 = predicate_params(𝑝)
                                            Ø
                                                T𝑒U h𝐻, 𝜌 i                               and h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣
    Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i := T𝑒U h𝐻, 𝜌 i ∪ T𝜙 1 U h𝐻, 𝜌 i                   if h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true
    Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i := T𝑒U h𝐻, 𝜌 i ∪ T𝜙 2 U h𝐻, 𝜌 i                  if h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false
                  Tacc(𝑒.𝑓 )U h𝐻, 𝜌 i := T𝑒U h𝐻, 𝜌 i ; hℓ, 𝑓 i                               if h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ
Deﬁnition 6. The maximal footprint of a formula, denoted ⌊𝜙⌋         ˜ h𝐻, 𝛼, 𝜌 i , is the set of all permis-
sions that 𝜙˜ may represent in the context of a heap 𝐻 , permission set 𝛼, and variable environment
𝜌.
   The footprint of a completely precise formula (deﬁnition 3) is its exact footprint, while the
footprint of a formula which is not completely precise is the current set of permissions.
                                        (
                                            ˜            ˜
                         ˜ h𝐻, 𝛼, 𝜌 i := T𝜙U h𝐻, 𝜌 i if 𝜙 is completely precise
                       ⌊𝜙⌋
                                          𝛼          otherwise

B.5 Framing
The relation h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 denotes that 𝑒 ∈ Expr is framed by the permissions contained in
𝛼 ∈ P (Perm).

                                                    FrameLiteral

                                                     h𝐻, 𝛼, 𝜌i ⊢frm 𝑙
                                                    FrameVar

                                                    h𝐻, 𝛼, 𝜌i ⊢frm 𝑥
                                  FrameField
                                   h𝐻, 𝛼, 𝜌i ⊢frm 𝑒            h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 )
                                                   h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.𝑓
                                    FrameOp
                                     h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1           h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2
                                                h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 ⊕ 𝑒 2
111:36                                                              C. Zimmerman, J. DiVincenzo, and J. Aldrich

                            FrameOrA
                             h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true        h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1
                                        h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2
                 FrameOrB
                 h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false        h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1       h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2
                                        h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2
                            FrameAndA
                            h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false         h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1
                                        h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 && 𝑒 2
                 FrameAndB
                  h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true       h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1        h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2
                                        h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 && 𝑒 2
                                          FrameNeg
                                           h𝐻, 𝛼, 𝜌i ⊢frm 𝑒
                                       h𝐻, 𝛼, 𝜌i ⊢frm ! 𝑒
   The relation h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙 denotes that 𝜙 ∈ Formula is framed by the permissions in
𝛼 ∈ P (Perm) using an iso-recursive interpretation of predicates (i.e., without unrolling predicate
instances).

                                          IFrameExpression
                                           h𝐻, 𝛼, 𝜌i ⊢frm 𝑒
                                           h𝐻, 𝛼, 𝜌i ⊢frmI 𝑒
                             IFrameConjunction
                             h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙 1       h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙 2
                                        h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙 1 ∗ 𝜙 2
                                         IFramePredicate
                                           h𝐻, 𝛼, 𝜌i ⊢frm 𝑒
                                         h𝐻, 𝛼, 𝜌i ⊢frmI 𝑝 (𝑒)
                  IFrameConditionalA
                  h𝐻, 𝜌i ⊢ 𝑒 ⇓ true        h𝐻, 𝛼, 𝜌i ⊢frm 𝑒         h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙 1
                               h𝐻, 𝛼, 𝜌i ⊢frmI if 𝑒 then 𝜙 1 else 𝜙 2
                 IFrameConditionalB
                  h𝐻, 𝜌i ⊢ 𝑒 ⇓ false        h𝐻, 𝛼, 𝜌i ⊢frm 𝑒         h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙 2
                               h𝐻, 𝛼, 𝜌i ⊢frmI if 𝑒 then 𝜙 1 else 𝜙 2
                                      IFrameAcc
                                           h𝐻, 𝛼, 𝜌i ⊢frm 𝑒
                                     h𝐻, 𝛼, 𝜌i ⊢frmI acc(𝑒.𝑓 )
   Deﬁne the relation h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 denotes that 𝜙 ∈ Formula is framed by the permissions
in 𝛼 ∈ P (Perm) using an equi-recursive interpretation of predicates (i.e., unrolling predicate in-
stances).

                                          EFrameExpression
                                           h𝐻, 𝛼, 𝜌i ⊢frm 𝑒
                                          h𝐻, 𝛼, 𝜌i ⊢frmE 𝑒
Sound Gradual Verification with Symbolic Execution                                                      111:37

                                 EFrameConjunction
                                 h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1          h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 2
                                             h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1 ∗ 𝜙 2
       EFramePredicate
                                            h𝐻, 𝛼, 𝜌i ⊢frm 𝑒
       h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣        𝑥 = predicate_params(𝑝)       h𝐻, 𝛼, [𝑥 ↦→ 𝑣]i ⊢frmE predicate(𝑝)
                                              h𝐻, 𝛼, 𝜌i ⊢frmE 𝑝 (𝑒)
                    EFrameConditionalA
                     h𝐻, 𝜌i ⊢ 𝑒 ⇓ true            h𝐻, 𝛼, 𝜌i ⊢frm 𝑒       h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1
                                      h𝐻, 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2
                    EFrameConditionalB
                    h𝐻, 𝜌i ⊢ 𝑒 ⇓ false             h𝐻, 𝛼, 𝜌i ⊢frm 𝑒       h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 2
                                      h𝐻, 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2
                                            EFrameAcc
                                                  h𝐻, 𝛼, 𝜌i ⊢frm 𝑒
                                            h𝐻, 𝛼, 𝜌i ⊢frmE acc(𝑒.𝑓 )
Deﬁnition 7. A self-framed formula is a precise formula 𝜙 ∈ Formula such that for all 𝐻, 𝛼, 𝜌,
                                      h𝐻, 𝛼, 𝜌i  𝜙 =⇒ h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙 .

B.6 Assertions
The relation h𝐻, 𝛼, 𝜌i  𝜙˜ denotes the validity of 𝜙˜ ∈ F̃ormula for the state represented by
h𝐻, 𝛼, 𝜌i.

                                      AssertImprecise
                                       h𝐻, 𝛼, 𝜌i  𝜙       h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙
                                                  h𝐻, 𝛼, 𝜌i  ? ∗ 𝜙
                                               AssertValue
                                               h𝐻, 𝜌i ⊢ 𝑒 ⇓ true
                                                    h𝐻, 𝛼, 𝜌i  e
                                      AssertIfA
                                      h𝐻, 𝜌i ⊢ 𝑒 ⇓ true        h𝐻, 𝛼, 𝜌i  𝜙 1
                                        h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2
                                  AssertIfB
                                      h𝐻, 𝜌i ⊢ 𝑒 ⇓ false        h𝐻, 𝛼, 𝜌i  𝜙 2
                                        h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2
                                          AssertAcc
                                          h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ        hℓ, 𝑓 i ∈ 𝛼
                                              h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 )
                AssertConjunction
                 h𝐻, 𝛼 1 , 𝜌i  𝜙 1       h𝐻, 𝛼 2, 𝜌i  𝜙 2      𝛼1 ∪ 𝛼2 ⊆ 𝛼        𝛼1 ∩ 𝛼2 = ∅
                                               h𝐻, 𝛼, 𝜌i  𝜙 1 ∗ 𝜙 2
         AssertPredicate
         𝑥 = predicate_params(𝑝)              h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣          h𝐻, 𝛼, [𝑥 ↦→ 𝑣]i  predicate(𝑝)
                                                  h𝐻, 𝛼, 𝜌i  𝑝 (𝑒)
111:38                                                                               C. Zimmerman, J. DiVincenzo, and J. Aldrich


B.7 Execution
Deﬁnition 8. A stack S is a list of the form
                                          h𝛼𝑛 , 𝜌𝑛 , 𝑠𝑛 i · . . . · h𝛼 1 , 𝜌 1, 𝑠 1 i · nil
where 𝑛 ≥ 1, 𝛼𝑛 , · · · , 𝛼 1 are permission sets, 𝜌𝑛 , · · · , 𝜌 1 are variable environments, and 𝑠𝑛 , · · · , 𝑠 1
are statements.
  𝛼 (S), 𝜌 (S), and 𝑠 (S) may be used to denote the values 𝛼𝑛 , 𝜌𝑛 , and 𝑠𝑛 , respectively.
Deﬁnition 9. An exclusion frame 𝛼ˆ a set of permissions that may not be transferred to a callee
stack frame. This is necessary to ensure that the permissions represented by the imprecise speci-
ﬁcations of a callee cannot overlap with some predicate instance that is owned by the caller.
   Small-step execution is denoted by the judgement
                                                  h𝐻, Si, 𝛼ˆ → h𝐻 ′ , S ′ i
for stacks S, S ′ , heap 𝐻 , and exclusion frame 𝛼.
                                                 ˆ

                               ExecSeq

                                   h𝐻, h𝛼, 𝜌, skip; 𝑠i · Si, 𝛼ˆ → h𝐻, h𝛼, 𝜌, 𝑠i · Si
                          ExecAssign
                                         h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣             h𝐻, 𝛼, 𝜌i ⊢frm 𝑒
                           h𝐻, h𝛼, 𝜌, 𝑥 = 𝑒; 𝑠i · Si, 𝛼ˆ → h𝐻, h𝛼, 𝜌 [𝑥 ↦→ 𝑣], 𝑠i · Si
         ExecAssignField
                                                   h𝐻, 𝜌i ⊢ 𝑥 ⇓ ℓ
         h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣            h𝐻, 𝛼, 𝜌i  acc(𝑥 .𝑓 )   h𝐻, 𝛼, 𝜌i ⊢frm 𝑒                     𝐻 ′ = 𝐻 [hℓ, 𝑓 i ↦→ 𝑣]
                              h𝐻, h𝛼, 𝜌, 𝑥 .𝑓 = 𝑒; 𝑠i · Si, 𝛼ˆ → h𝐻 ′ , h𝛼, 𝜌, 𝑠i · Si
         ExecAlloc
         ℓ = fresh       𝑇 𝑓 = struct(𝑆)             𝐻 ′ = 𝐻 [hℓ, 𝑓 i ↦→ default(𝑇 )]                𝛼 ′ = 𝛼 ∪ {hℓ, 𝑓 i}
                     h𝐻, h𝛼, 𝜌, 𝑥 = alloc(𝑆); 𝑠i · Si, 𝛼ˆ → h𝐻 ′ , h𝛼 ′ , 𝜌 [𝑥 ↦→ ℓ], 𝑠i · Si
   ExecCallEnter
                                        𝑥 = params(𝑚)       h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣
    h𝐻, 𝛼, 𝜌i ⊢frm 𝑒           𝜌 ′ = [𝑥 ↦→ 𝑣]            ˆ 𝜌 ′ i  pre(𝑚)
                                                 h𝐻, 𝛼 \ 𝛼,                                     𝛼 ′ = ⌊pre(𝑚)⌋ h𝐻, 𝛼 \𝛼,ˆ 𝜌 ′ i
                                            h𝐻, h𝛼, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠i · Si, 𝛼ˆ
                                                          →
                          h𝐻, h𝛼 ′ , 𝜌 ′, body(𝑚); skipi · h𝛼 \ 𝛼 ′ , 𝜌, 𝑦 = 𝑚(𝑒); 𝑠i · Si
         ExecCallExit
         h𝐻, 𝛼 ′ , 𝜌 ′ i  post(𝑚)        𝜌 ′′ = 𝜌 [𝑦 ↦→ 𝜌 ′ (result)]                 𝛼 ′′ = 𝛼 ∪ ⌊post(𝑚)⌋ h𝐻, 𝛼 ′, 𝜌 ′ i
                  h𝐻, h𝛼 , 𝜌 , skipi · h𝛼, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠i · Si, 𝛼ˆ → h𝐻, h𝛼 ′′ , 𝜌 ′′, 𝑠i · Si
                          ′    ′

                              ExecAssert
                                               h𝐻, 𝛼, 𝜌i  ? ∗ 𝜙
                                                ˜ 𝑠i · Si, 𝛼ˆ → h𝐻, h𝛼, 𝜌, 𝑠i · Si
                              h𝐻, h𝛼, 𝜌, assert 𝜙;
                   ExecIfA
                                       h𝐻, 𝜌i ⊢ 𝑒 ⇓ true               h𝐻, 𝛼, 𝜌i ⊢frm 𝑒
                     h𝐻, h𝐻, 𝜌, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠i · Si, 𝛼ˆ → h𝐻, h𝐻, 𝜌, 𝑠 1 ; 𝑠i · Si
Sound Gradual Verification with Symbolic Execution                                                            111:39

                 ExecIfB
                                  h𝐻, 𝜌i ⊢ 𝑒 ⇓ false           h𝐻, 𝛼, 𝜌i ⊢frm 𝑒
                 h𝐻, h𝐻, 𝜌, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠i · Si, 𝛼ˆ → h𝐻, h𝐻, 𝜌, 𝑠 2 ; 𝑠i · Si
        ExecWhileEnter
        h𝐻, 𝜌i ⊢ 𝑒 ⇓ true          h𝐻, 𝛼, 𝜌i ⊢frm 𝑒                 ˆ 𝜌i  𝜙˜
                                                            h𝐻, 𝛼 \ 𝛼,           𝛼 ′ = ⌊𝜙⌋ ˜ h𝐻, 𝛼 \𝛼,ˆ 𝜌 i
                            h𝐻, h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠 ′ ; 𝑠i · Si, 𝛼ˆ
                                                          →
                h𝐻, h𝛼 ′ , 𝜌, 𝑠 ′ ; skipi · h𝛼 \ 𝛼 ′ , 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠 ′ ; 𝑠i · Si
               ExecWhileSkip
                     h𝐻, 𝜌i ⊢ 𝑒 ⇓ false   h𝐻, 𝛼, 𝜌i ⊢frm 𝑒                  ˆ 𝜌i  𝜙˜
                                                                    h𝐻, 𝛼 \ 𝛼,
                h𝐻, h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠 ′ ; 𝑠i · Si, 𝛼ˆ → h𝐻, h𝛼, 𝜌, 𝑠i · Si
                   ExecWhileFinish
                                 h𝐻, 𝛼 ′ , 𝜌 ′ i  𝜙˜               ˜ h𝐻, 𝛼 ′, 𝜌 ′ i
                                                       𝛼 ′′ = 𝛼 ∪ ⌊𝜙⌋
                   h𝐻, h𝛼 ′ , 𝜌 ′, skipi · h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠 ′ ; 𝑠i · Si, 𝛼ˆ
                                                       →
                             h𝐻, h𝛼 ′′ , 𝜌 ′, while 𝑒 invariant 𝜙˜ do 𝑠 ′ ; 𝑠i · Si
                           ExecFold

                           h𝐻, h𝛼, 𝜌, fold 𝑝 (𝑒); 𝑠i · 𝑆i, 𝛼ˆ → h𝐻, h𝛼, 𝜌, 𝑠i · 𝑆i
                         ExecUnfold

                         h𝐻, h𝛼, 𝜌, unfold 𝑝 (𝑒); 𝑠i · 𝑆i, 𝛼ˆ → h𝐻, h𝛼, 𝜌, 𝑠i · 𝑆i

B.8 Reachable transitions
Deﬁnition 10. An execution state Γ is either one of the abstract symbols final or init, or a pair
h𝐻, Si of a heap 𝐻 and a stack S.
Deﬁnition 11. An execution state Γ is well-formed if Γ is either one of the abstract symbols init
or final, or of the form h𝐻, h𝛼𝑛 , 𝜌𝑛, 𝑠𝑛 i · . . . · h𝛼 1 , 𝜌 1, 𝑠 1 i · nili and
 • 𝛼𝑖 ∩ 𝛼 𝑗 = ∅ for all 1 ≤ 𝑖 < 𝑗 ≤ 𝑛.
 • 𝑠𝑛 = 𝑠; skip for some statement 𝑠 or 𝑠𝑛 = skip.
 • For all 1 ≤ 𝑖 < 𝑛, 𝑠𝑖 = 𝑠; 𝑠 ′ ; skip or 𝑠𝑖 = 𝑠; skip for some statements 𝑠 and 𝑠 ′ where 𝑠 is of the
    form 𝑚(𝑒) for some 𝑚, 𝑒 or while 𝑒 invariant 𝜙˜ do 𝑠𝑏𝑜𝑑 𝑦 for some 𝑒, 𝜙,       ˜ 𝑠𝑏𝑜𝑑 𝑦 .

   Examining the execution rules shows that well-formedness of states is preserved by the execu-
tion rules deﬁned above.
   A dynamic execution transition Γ → Γ ′ is reachable under a program Π, using the exclusion
frame 𝛼,
       ˆ when the following judgement holds:
                                                   Π ⊢ Γ, 𝛼ˆ → Γ ′
                                ExecInit

                                 h𝑠, 𝑀, 𝑃, 𝑆i ⊢ init, _ → h∅, h∅, ∅, 𝑠i · nili
                             ExecStep
                              Π ⊢ _, _ → h𝐻, Si            h𝐻, Si, 𝛼ˆ → h𝐻 ′ , S ′ i
                                           Π ⊢ h𝐻, Si, 𝛼ˆ → h𝐻 ′ , S ′ i
                                    ExecFinal

                                    Π ⊢ h_, h_, _, skipi · nili, _ → final
111:40                                                                       C. Zimmerman, J. DiVincenzo, and J. Aldrich


Deﬁnition 12. An execution state Γ is reachable from program Π if Γ = init or Π ⊢ _, _ → Γ.

C    SYMBOLIC EXECUTION
C.1 Definitions
Deﬁnition 13. A symbolic value 𝜈 ∈ SValue is an abstract value that represents an unknown
character, boolean, integer, or location value. We leave the concrete type of SValue undeﬁned, but
assume that an inﬁnite number of distinct new values can be produced by the fresh function.
Deﬁnition 14. A symbolic expression 𝑡 ∈ SExpr is a symbolic value or symbolic expressions
combined using operators. Note that the binary operators ⊕ are the same as in §A.
                   𝑡 ::= 𝜈   | 𝑙    |   !𝑡       |       𝑡 1 && 𝑡 2   |   𝑡 1 || 𝑡 2       |   𝑡1 ⊕ 𝑡2
Deﬁnition 15. A path condition 𝑔 ∈ SExpr is a symbolic expression consisting of conjuncts
added at every branch point during a particular symbolic execution path.
Deﬁnition 16. An imprecise ﬂag 𝜄 ∈ {⊤, ⊥} is a ﬂag that indicates whether a state is imprecise.
Deﬁnition 17. A symbolic evironment 𝛾 : Var ⇀ SExpr is a partial function mapping variable
names to symbolic expressions.
Deﬁnition 18. A ﬁeld chunk h𝑓 , 𝑡, 𝑡 ′ i ∈ SField denotes the mapping of the ﬁeld 𝑓 of instance
𝑡 to the value 𝑡 ′ .
Deﬁnition 19. A predicate chunk h𝑝, 𝑡i ∈ SPredicate represents an isorecursive predicate 𝑝
with symbolically-evaluated arguments 𝑡.
Deﬁnition 20. A heap chunk ℎ ∈ SField ∪ SPredicate is either a ﬁeld chunk or a predicate
chunk.
Deﬁnition 21. A precise symbolic heap (usually abbreviated as precise heap) H ∈ P (SField ∪
SPredicate) is a set of heap chunks where all heap chunks must occupy distinct heap locations
at run time.
Deﬁnition 22. An optimistic symbolic heap (usually abbreviated as optimistic heap) H ∈
P (SField) is a set of ﬁeld chunks where distinct chunks may coincide on the heap at run time (i.e.
object references that are distinct symbolic expressions may be represent the same object value at
run time).
Deﬁnition 23. A symbolic permission 𝜃 ∈ SPerm represents a particular heap location or
predicate instance.
                                     𝜃 ::= h𝑓 , 𝑡i | h𝑝, 𝑡i
A set of symbolic permissions is denoted by Θ.
Deﬁnition 24. A run-time check 𝑟 ∈ SCheck is a symbolic value that must be asserted at
run time, a symbolic permission whose access must be asserted at run time, a set of symbolic
permissions whose disjointness must be asserted at run time, or an unsatisﬁable check.
                              𝑟 ::= 𝑡   |    𝜃       |      sep(Θ1 , Θ2 )      |       ⊥
A set of run-time checks is denoted by R.
Deﬁnition 25. A symbolic state 𝜎 ∈ SState consists of an imprecise ﬂag, a path condition, a
precise heap, an optimistic heap, and a symbolic environment.
                                        𝜎 ::= h𝜄, 𝑔, H, H, 𝛾i
𝜄 (𝜎), 𝑔(𝜎), H(𝜎), H (𝜎), and 𝛾 (𝜎) each denote a reference to the respective component of 𝜎.
Sound Gradual Verification with Symbolic Execution                                                       111:41


C.2 Valuations
In order to prove soundness with respect to the dynamic semantics, we must ﬁrst deﬁne a corre-
spondence between the two representations.


Deﬁnition 26. A valuation 𝑉 : SValue ⇀ Value is a partial function mapping symbolic values
to concrete values.


  A base valuation 𝑉 : SValue ⇀ Value is implicitly extended to 𝑉 : SExpr ⇀ Value for all
possible symbolic expressions composed of literals and symbolic values in the domain of 𝑉 :



                               𝑉 (𝑙) := 𝑙
                        𝑉 (𝑡 1 + 𝑡 2 ) := 𝑉 (𝑡 1 ) + 𝑉 (𝑡 2 )
                        𝑉 (𝑡 1 - 𝑡 2 ) := 𝑉 (𝑡 1 ) − 𝑉 (𝑡 2 )
                        𝑉 (𝑡 1 * 𝑡 2 ) := 𝑉 (𝑡 1 ) · 𝑉 (𝑡 2 )
                                          𝑉 (𝑡 1 )
                        𝑉 (𝑡 1 / 𝑡 2 ) :=
                                          𝑉 (𝑡 2 )
                                          (
                                            true         if 𝑉 (𝑡 1 ) = 𝑉 (𝑡 2 )
                       𝑉 (𝑡 1 == 𝑡 2 ) :=
                                            false        otherwise
                                          (
                                            true         if 𝑉 (𝑡 1 ) = false
                             𝑉 (! 𝑡) :=
                                            false        otherwise
                                          (
                                            true         if 𝑉 (𝑡 1 ) = true or 𝑉 (𝑡 2 ) = true
                       𝑉 (𝑡 1 || 𝑡 2 ) :=
                                            false        otherwise
                                          (
                                            true         if 𝑉 (𝑡 1 ) = true and 𝑉 (𝑡 2 ) = true
                       𝑉 (𝑡 1 && 𝑡 2 ) :=
                                            false        otherwise


Deﬁnition 27. A symbolic expression 𝑡 1 implies another symbolic expression 𝑡 2 (denoted 𝑡 1 =⇒
𝑡 2 ) if, for all valuations for which 𝑉 (𝑡 1 ) and 𝑉 (𝑡 2 ) are deﬁned, (𝑉 (𝑡 1 ) = true) =⇒ (𝑉 (𝑡 2 ) = true).


C.3    Footprints
𝑉 L𝜃 M𝐻 and 𝑉 LΘM𝐻 denote the footprint (i.e. set of permissions) necessary to satisfy the given sym-
bolic permission or symbolic permission set, respectively, given some heap 𝐻 .



                                 𝑉 Lh𝑓 , 𝑡iM𝐻 := h𝑉 (𝑡), 𝑓 i
                                  𝑉 Lh𝑝, 𝑡 iM𝐻 := Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 (𝑡 ) ] i
                                                  Ø
                                      𝑉 LΘM𝐻 :=      𝑉 L𝜃 M𝐻
                                                      𝜃 ∈Θ
111:42                                                               C. Zimmerman, J. DiVincenzo, and J. Aldrich


C.4      Correspondence
The relations h𝐻, 𝛼i 𝑉 H, h𝐻, 𝛼i 𝑉 H , 𝜌              𝑉
                                                          𝛾, and h𝐻, 𝛼, 𝜌i      𝑉
                                                                                    𝜎 denote correspondence
between symbolic states and run-time states:
                              def
               h𝐻, 𝛼i 𝑉 H ⇐⇒ (∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ )) ∧
                                    (∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H : h𝑉 (𝑡), 𝑓 i ∈ 𝛼) ∧
                                                                                                             (1)
                                    (∀ h𝑝, 𝑡i ∈ H : h𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝)) ∧
                                    (∀ℎ 1 , ℎ 2 ∈ H2 : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 Lℎ 1 M𝐻 ∩ 𝑉 Lℎ 2 M𝐻 = ∅)
                              def
              h𝐻, 𝛼i 𝑉 H ⇐⇒ (∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ )) ∧
                                                                                                             (2)
                                    (∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H : h𝑉 (𝑡), 𝑓 i ∈ 𝛼)
                              def
                     𝜌 𝑉 𝛾 ⇐⇒ ∀ 𝑥 ∈ dom(𝛾) : 𝜌 (𝑥) = 𝑉 (𝑡)                                                   (3)
                              def
             h𝐻, 𝛼, 𝜌i 𝑉 𝜎 ⇐⇒ (h𝐻, 𝛼i 𝑉 H(𝜎)) ∧
                                    (h𝐻, 𝛼i 𝑉 H (𝜎)) ∧
                                                                                                             (4)
                                    (𝜌 𝑉 𝛾 (𝜎)) ∧
                                    (𝑉 (𝑔(𝜎)) = true)

C.5      Run-time checks
The judgement h𝐻, 𝛼i ⊢𝑉 𝑟 denotes that a symbolic runtime check 𝑟 ∈ SCheck is satisﬁed at run
time by a heap 𝐻 and permission set 𝛼 through a valuation 𝑉 . Note that there is no rule for ⊥; by
design it can never be satisﬁed.
                                              CheckValue
                                               𝑉 (𝑡) = true
                                               h𝐻, 𝛼i ⊢𝑉 𝑡
                                            CheckAcc
                                              h𝑉 (𝑡), 𝑓 i ∈ 𝛼
                                             h𝐻, 𝛼i ⊢𝑉 h𝑓 , 𝑡i
                CheckPred
                 𝑥 = predicate_params(𝑝)              h𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝)
                                             h𝐻, 𝛼i ⊢𝑉 h𝑝, 𝑡i
                                        CheckSep
                                        𝑉 LΘ1 M𝐻 ∩ 𝑉 LΘ2 M𝐻 = ∅
                                         h𝐻, 𝛼i ⊢𝑉 sep(Θ1 , Θ2 )
   This judgement is naturally extended for a set of runtime checks R:
                                                def
                              h𝐻, 𝛼i ⊢𝑉 R ⇐⇒ ∀ 𝑟 ∈ R : h𝐻, 𝛼i ⊢𝑉 𝑟

C.6 Evaluation
The judgement
                                            𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R
Sound Gradual Verification with Symbolic Execution                                                                    111:43


denotes the evaluation of the expression 𝑒 ∈ Expr in the symbolic state 𝜎 ∈ SState. It yields the
symbolic expression 𝑡 ∈ SExpr, a new symbolic state 𝜎 ′ which must be satisﬁed to produce the
resulting value, and a set of run-time checks R ∈ P (SCheck).
   Note that for any given 𝜎, there may be multiple values of 𝑡, 𝜎 ′, R for which the relation is
satisﬁed. Therefore, the path condition of 𝜎 ′ must be satisﬁed before assuming that 𝑡 corresponds
to an actual value.
   Also note that unsatisﬁable paths are not pruned during evaluation. These paths may be pruned
by checking the satisﬁability of 𝑔(𝜎 ′ ).
   For a list of expressions 𝑒, 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R represents a sequence of judgements
                                𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, , · · · , 𝜎𝑛−1 ⊢ 𝑒𝑛 ⇓ 𝑡𝑛 ⊣ 𝜎𝑛 , R𝑛
where 𝜎0 = 𝜎, 𝑒 1 , · · · , 𝑒𝑛 = 𝑒, and R = R 1 ∪ · · · ∪ R𝑛 .

                                                     SEvalLiteral

                                                      𝜎 ⊢ 𝑙 ⇓ 𝑙 ⊣ 𝜎, ∅
                                                SEvalVar

                                                 𝜎 ⊢ 𝑥 ⇓ 𝛾 (𝜎) (𝑥) ⊣ 𝜎, ∅
                               SEvalOrA
                               𝜎 ⊢ 𝑒 1 ⇓ 𝑡1 ⊣ 𝜎 ′, R           𝜎 ′′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡 1 ]
                                                𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′ , R
                     SEvalOrB
                     𝜎 ⊢ 𝑒 1 ⇓ 𝑡1 ⊣ 𝜎 ′, R1           𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡 1 ] ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 2
                                          𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 1 ∪ R 2
                              SEvalAndA
                              𝜎 ⊢ 𝑒1 ⇓ 𝑡1 ⊣ 𝜎 ′, R           𝜎 ′′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡 1 ]
                                                𝜎 ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′ , R
                      SEvalAndB
                      𝜎 ⊢ 𝑒1 ⇓ 𝑡1 ⊣ 𝜎 ′, R1            𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡 1 ] ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 2
                                          𝜎 ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 1 ∪ R 2
                                 SEvalOp
                                 𝜎 ⊢ 𝑒 1 ⇓ 𝑡1 ⊣ 𝜎 ′, R1           𝜎 ′ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 2
                                        𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑡 1 ⊕ 𝑡 2 ⊣ 𝜎 ′′ , R 1 ∪ R 2
                                                  SEvalNeg
                                                     𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R
                                                  𝜎 ⊢ ! 𝑒 ⇓ ! 𝑡 ⊣ 𝜎 ′, R
                     SEvalField
                     𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R          𝑔(𝜎 ′ ) =⇒ 𝑡𝑒 == 𝑡𝑒′            h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎 ′ )
                                                   𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′ , R
   SEvalFieldOptimistic
                                                  𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R
    𝑡𝑒′ , 𝑡 : h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) ∧ 𝑔(𝜎 ′ )   =⇒ 𝑡𝑒′ == 𝑡𝑒     h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H (𝜎)              𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒
                                                   𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′ , R
111:44                                                                    C. Zimmerman, J. DiVincenzo, and J. Aldrich

         SEvalFieldImprecise
         𝜄 (𝜎)   𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R   𝑡𝑒′ , 𝑡 : h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) ∪ H (𝜎) ∧ 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒
                             𝑡 = fresh    𝜎 ′′ = 𝜎 ′ [H = H (𝜎 ′ ); h𝑓 , 𝑡𝑒 , 𝑡i]
                                          𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′′ , R; h𝑡𝑒 , 𝑓 i
    SEvalFieldFailure
                                                            ¬𝜄 (𝜎)
    𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R        𝑡𝑒′ , 𝑡 : h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) ∪ H (𝜎) ∧ 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒        𝑡 = fresh
                                                               ′
                                             𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 , {⊥}

C.7 Deterministic evaluation
We also deﬁne separate evaluation semantics for evaluation when branching is unwanted. This is
denoted by the judgement
                                          𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ R.
  This operation mirrors the behavior of pc-eval, and as such, does not modify the symbolic state.
Logical operations are not short-circuited as in the previous section; instead, they are formally
encoded as conjuncts of a single SExpr.

                                                SEvalPCLiteral

                                                 𝜎 ⊢𝑙 ↓𝑙 ⊣ ∅
                                              SEvalPCVar

                                              𝜎 ⊢ 𝑥 ↓ 𝛾 (𝜎) (𝑥) ⊣ ∅
                                    SEvalPCOr
                                    𝜎 ⊢ 𝑒1 ↓ 𝑡1 ⊣ R1         𝜎 ⊢ 𝑒2 ↓ 𝑡2 ⊣ R2
                                       𝜎 ⊢ 𝑒 1 || 𝑒 2 ↓ 𝑡 1 || 𝑡 2 ⊣ R 1 ∪ R 2
                                    SEvalPCAnd
                                    𝜎 ⊢ 𝑒1 ↓ 𝑡1 ⊣ R1         𝜎 ⊢ 𝑒2 ↓ 𝑡2 ⊣ R2
                                       𝜎 ⊢ 𝑒 1 && 𝑒 2 ↓ 𝑡 1 && 𝑡 2 ⊣ R 1 ∪ R 2
                                    SEvalPCOp
                                    𝜎 ⊢ 𝑒1 ↓ 𝑡1 ⊣ R1         𝜎 ⊢ 𝑒2 ↓ 𝑡2 ⊣ R2
                                       𝜎 ⊢ 𝑒1 ⊕ 𝑒2 ↓ 𝑡1 ⊕ 𝑡2 ⊣ R1 ∪ R2
                                                SEvalPCNeg
                                                  𝜎 ⊢𝑒 ↓𝑡 ⊣ R
                                                𝜎 ⊢ !𝑒 ↓ !𝑡 ⊣ R
                      SEvalPCField
                      𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R         𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒            h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎)
                                                 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R
    SEvalPCFieldOptimistic
                                               𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R
     𝑡𝑒 , 𝑡 : h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) ∧ 𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒    𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒                h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H (𝜎)
                                                 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R
                 SEvalPCFieldImprecise
                                               𝜄 (𝜎)    𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R
                   𝑡𝑒 , 𝑡 : h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) ∪ H (𝜎) ∧ 𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒           𝑡 = fresh
                                            𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R; h𝑡𝑒 , 𝑓 i
Sound Gradual Verification with Symbolic Execution                                                 111:45

                 SEvalPCFieldMissing
                                              ¬𝜄 (𝜎)   𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R
                  𝑡𝑒 , 𝑡 : h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) ∪ H (𝜎) ∧ 𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒           𝑡 = fresh
                                              𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R; ⊥

C.8 Produce
The produce operation adds the information contained in a formula 𝜙˜ to the symbolic state 𝜎,
resulting in a new symbolic state 𝜎 ′ . This is denoted by the judgement
                                                     𝜎 ⊢ 𝜙 ⊳ 𝜎′.

                                              SProduceImprecise
                                              𝜎 [𝜄 = ⊤] ⊢ 𝜙 ⊳ 𝜎 ′
                                                𝜎 ⊢ ? ∗ 𝜙 ⊳ 𝜎′
                                  SProduceExpr
                                  𝜎 ⊢𝑒 ↓𝑡 ⊣_            𝜎 ′ = 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡]
                                                     𝜎 ⊢ 𝑒 ⊳ 𝜎′
                                SProducePredicate
                                𝜎 ⊢𝑒 ↓𝑡 ⊣_            𝜎 ′ = 𝜎 [H = H(𝜎); h𝑝, 𝑡 i]
                                                 𝜎 ⊢ 𝑝 (𝑒) ⊳ 𝜎 ′
                     SProduceField
                      𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ _       𝑡 = fresh         𝜎 ′ = 𝜎 [H = H(𝜎); h𝑓 , 𝑡𝑒 , 𝑡i]
                                              𝜎 ⊢ acc(𝑒.𝑓 ) ⊳ 𝜎 ′
                                        SProduceConjunction
                                        𝜎 ⊢ 𝜙1 ⊳ 𝜎 ′        𝜎 ′ ⊢ 𝜙 2 ⊳ 𝜎 ′′
                                               𝜎 ⊢ 𝜙 1 ∗ 𝜙 2 ⊳ 𝜎 ′′
                               SProduceIfA
                               𝜎 ⊢𝑒 ↓𝑡 ⊣_            𝜎 [𝑔 = 𝑔(𝜎) && 𝑡] ⊢ 𝜙 1 ⊳ 𝜎 ′
                                       𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊳ 𝜎 ′
                              SProduceIfB
                              𝜎 ⊢𝑒 ↓𝑡 ⊣_             𝜎 [𝑔 = 𝑔(𝜎) && ! 𝑡] ⊢ 𝜙 2 ⊳ 𝜎 ′
                                       𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊳ 𝜎 ′

C.9    Consume
The consume operation checks whether a formula 𝜙˜ is established by the symbolic state, collects
                                                         ˜ and removes permissions asserted in
runtime checks that are minimally suﬃcient to establish 𝜙,
 ˜
𝜙 from the symbolic state. This is denoted by the judgement
                                             𝜎, 𝜎𝐸 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R, Θ
where 𝜎 is the symbolic state containing the currently remaining permissions during consume,
and 𝜎𝐸 is the symbolic state containing the original permissions which may used for evaluating
expressions.
  Note that consume does not branch on operations such as && that are normally short-circuiting.
This is because the evaluation operation ↓ does not modify the path condition but keeps track of
logical operators as symbolic values. Values in speciﬁcations must be framed anyway (explicitly
111:46                                                                      C. Zimmerman, J. DiVincenzo, and J. Aldrich


or inferred), so we must always have the permissions necessary (whether statically or dynamically
checked) for evaluating all branches.

                                    SConsumeImprecision
                                               𝜎, 𝜎𝐸 [𝜄 = ⊤] ⊢ 𝜙 ⊲ 𝜎 ′ , R, Θ
                                    𝜎, 𝜎𝐸 ⊢ ? ∗ 𝜙 ⊲ h⊤, 𝑔(𝜎 ′ ), 𝛾 (𝜎 ′ ), ∅, ∅i, R, Θ
                                           SConsumeValue
                                           𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R        𝑔(𝜎) =⇒ 𝑡
                                                   𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎, R, ∅
                                      SConsumeValueImprecise
                                       𝜄 (𝜎)      𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R             Y 𝑡
                                                                       𝑔(𝜎) =⇒
                                        𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡], R; 𝑡, ∅
                                      SConsumeValueFailure
                                      ¬𝜄 (𝜎)       𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R              Y 𝑡
                                                                         𝑔(𝜎) =⇒
                                                  𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎, {⊥}, ∅
                        SConsumePredicate
                        𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R            𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ H(𝜎) = H′ ; h𝑝, 𝑡 ′ i
                                                                  Ø
                              𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ⊲ 𝜎 [H = H′ , H = ∅],   R, {h𝑝, 𝑡i}
                   SConsumePredicateImprecise                         Û
                   𝜄 (𝜎)      𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R      h𝑝, 𝑡 ′ i ∈ H(𝜎) :    𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′
                                                               Ø
                           𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ⊲ 𝜎 [𝐻 = ∅, H = ∅],      R; h𝑝, 𝑡i, {h𝑝, 𝑡i}
                  SConsumePredicateFailure                                     Û
                  ¬𝜄 (𝜎)       𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R            h𝑝, 𝑡 ′ i ∈ H(𝜎) :       𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′
                                           𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ⊲ 𝜎, {⊥}, {h𝑝, 𝑡i}
            SConsumeAcc
                                       𝜎 𝐸 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R   𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒
             h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎)          ′
                                         H = remfp (H(𝜎), 𝜎, 𝑡𝑒 , 𝑓 ) H ′ = remf (H (𝜎), 𝜎, 𝑡𝑒 , 𝑓 )
                            𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 [H = H′ , H = H ′ ], R, {h𝑡𝑒 , 𝑓 i}
   SConsumeAccOptimistic
                                                  𝜎 𝐸 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R
   𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒           h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎)       𝑡𝑒′ , 𝑡 : h𝑓 , 𝑡𝑒 , 𝑡i ∈ H(𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 )
                            ′
                           H = remf (H(𝜎), 𝜎, 𝑡𝑒 , 𝑓 )       H ′ = remf (H (𝜎), 𝜎, 𝑡𝑒 , 𝑓 )
                            𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 [H = H′ , H = H ′ ], R, {h𝑡𝑒 , 𝑓 i}
         SConsumeAccImprecise
         𝜄 (𝜎)      𝜎 𝐸 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R   𝑡𝑒′ , 𝑡 : h𝑓 , 𝑡𝑒 , 𝑡i ∈ H(𝜎) ∪ H (𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 )
                            ′
                          H = remf (H(𝜎), 𝜎, 𝑡𝑒 , 𝑓 )        H ′ = remf (H (𝜎), 𝜎, 𝑡𝑒 , 𝑓 )
                       𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 [H = H′ , H = H ′ ], R; h𝑡𝑒 , 𝑓 i, {h𝑡𝑒 , 𝑓 i}
         SConsumeAccFailure
         ¬𝜄 (𝜎)      𝜎 𝐸 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R            𝑡𝑒′ , 𝑡 : h𝑓 , 𝑡𝑒 , 𝑡i ∈ H(𝜎) ∪ H (𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 )
                                        𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎, {⊥}, {h𝑡𝑒 , 𝑓 i}
Sound Gradual Verification with Symbolic Execution                                                              111:47

                   SConsumeConjunction
                   𝜎, 𝜎𝐸 ⊢ 𝜙 1 ⊲ 𝜎 ′ , R 1 , Θ1      𝜎 ′, 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ⊲ 𝜎 ′′ , R 2, Θ2
                                             (R 1 ∪ R 2 ) ∩ SPerm = ∅
                                   𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ⊲ 𝜎 ′′ , R 1 ∪ R 2 , Θ1 ∪ Θ2
                   SConsumeConjunctionImprecise
                   𝜎, 𝜎𝐸 ⊢ 𝜙 1 ⊲ 𝜎 ′ , R 1 , Θ1      𝜎 ′, 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ⊲ 𝜎 ′′ , R 2, Θ2
                                             (R 1 ∪ R 2 ) ∩ SPerm ≠ ∅
                          𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ⊲ 𝜎 ′′ , R 1 ∪ R 2 ; sep(Θ1 , Θ2 ), Θ1 ∪ Θ2
            SConsumeConditionalA
             𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R        𝑔′ = 𝑔(𝜎) && 𝑡            𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 1 ⊲ 𝜎 ′ , R ′ , Θ
                              𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲ 𝜎 ′, R ∪ R ′ , Θ
           SConsumeConditionalB
            𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R        𝑔′ = 𝑔(𝜎) && ! 𝑡            𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 2 ⊲ 𝜎 ′ , R ′ , Θ
                          𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲ 𝜎 ′, R ∪ R ′ , Θ
  The functions remf , remfp , and alias are deﬁned as follows:
                        remf (H, 𝜎, 𝑡, 𝑓 ) = {h𝑓 ′ , 𝑡 ′ , 𝑡 ′′ i ∈ H : ¬ alias(𝜎, 𝑡, 𝑓 , 𝑡 ′ , 𝑓 ′ )}
                       remfp (H, 𝜎, 𝑡, 𝑓 ) = remf (H, 𝜎, 𝑡, 𝑓 ) ∪ {h𝑝, 𝑡i ∈ H}
                                               (
                                      ′ ′        𝑓 = 𝑓 ′ ∧ (𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ )                 ¬𝜄 (𝜎)
                     alias(𝜎, 𝑡, 𝑓 , 𝑡 , 𝑓 ) =
                                                 (𝑓 = 𝑓 ′ ) ∧ sat(𝑔(𝜎) && 𝑡 == 𝑡 ′ )           𝜄 (𝜎)

  For ease of notation, the judgement 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R applies the rules above, initializing additional
parameters and ignoring the parameters that are internal to consume.
                                                SConsume
                                                𝜎, 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R, _
                                                   𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R

C.10 Execute
Symbolic execution is denoted by the small-step judgement
                                                  𝜎 ⊢ 𝑠 → 𝑠′ ⊣ 𝜎 ′.
where 𝜎 is the symbolic state prior to execution, 𝑠 is the statement to execute, 𝑠 ′ is the statement
remaining after this execution step and 𝜎 ′ is the symbolic state after the execution step.
  Note that as in §C.6 there may be multiple resulting symbolic states 𝜎 ′ for which the judge-
ment applies, and therefore the path condition of 𝜎 ′ must be satisﬁed before assuming that 𝜎 ′
corresponds to a particular execution step.

                                               SExecSeq

                                               𝜎 ⊢ skip; 𝑠 → 𝑠 ⊣ 𝜎
                                   SExecAssign
                                   𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _          𝛾 ′ = 𝛾 (𝜎) [𝑥 ↦→ 𝑡]
                                         𝜎 ⊢ 𝑥 = 𝑒; 𝑠 → 𝑠 ⊣ 𝜎 ′ [𝛾 = 𝛾 ′ ]
            SExecAssignField
            𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _        𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ⊲ 𝜎 ′′ , _          H′ = H(𝜎); h𝛾 (𝜎 ′′ ) (𝑥), 𝑓 , 𝑡i
                                      𝜎 ⊢ 𝑥 .𝑓 = 𝑒; 𝑠 → 𝑠 ⊣ 𝜎 ′′ [H = H′ ]
111:48                                                                          C. Zimmerman, J. DiVincenzo, and J. Aldrich

                     SExecAlloc
                     𝑡 = fresh          𝑇 𝑓 = struct(𝑆)          H′ = H(𝜎); h𝑓 , 𝑡, default(𝑇 )i
                                       𝜎 ⊢ 𝑥 = alloc(𝑆); 𝑠 → 𝑠 ⊣ 𝜎 [H = H′ ]
              SExecCall
              𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , _        𝑥 = params(𝑚)        𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡𝑒 ]] ⊢ pre(𝑚) ⊲ 𝜎 ′ , _
                      𝑡 = fresh           𝜎 [𝛾 = [𝑥 ↦→ 𝑡𝑒 , result ↦→ 𝑡]] ⊢ post(𝑚) ⊳ 𝜎 ′′
                                            ′

                                   𝜎 ⊢ 𝑦 = 𝑚(𝑒); 𝑠 → 𝑠 ⊣ 𝜎 ′′ [𝛾 = 𝛾 (𝜎) [𝑦 ↦→ 𝑡]]
                                       SExecAssert
                                        𝜎 ⊢ ? ∗ 𝜙 ⊲ 𝜎 ′, _           𝜎 ′ ⊢ ? ∗ 𝜙 ⊳ 𝜎 ′′
                                        𝜎 ⊢ assert 𝜙; 𝑠 → 𝑠 ⊣ 𝜎 [𝑔 = 𝑔(𝜎 ′′ )]
         SExecFold
                           𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _      𝑥 = predicate_params(𝑝)
         𝜎 [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ predicate(𝑝) ⊲ 𝜎 ′′ , _
          ′
                                                        𝜎 ′′′ = 𝜎 ′′ [𝛾 = 𝛾 (𝜎), H = H(𝜎 ′′ ); h𝑝, 𝑡i]
                                                𝜎 ⊢ fold 𝑝 (𝑒); 𝑠 → 𝑠 ⊣ 𝜎 ′′′
   SExecUnfold
                                                𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _
    𝜎 ′ ⊢ 𝑝 (𝑒) ⊲ 𝜎 ′′ , _        𝑥 = predicate_params(𝑝)        𝜎 ′′ [𝛾 = [𝑥 ↦→ 𝑡 ]] ⊢ predicate(𝑝) ⊳ 𝜎 ′′′
                                𝜎 ⊢ unfold 𝑝 (𝑒 1 , · · · , 𝑒𝑛 ); 𝑠 → 𝑠 ⊣ 𝜎 ′′′ [𝛾 = 𝛾 (𝜎)]
                         SExecIfA
                                                      𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _
                             𝜎 ⊢ if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠 → 𝑠 1 ; 𝑠 ⊣ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡]
                        SExecIfB
                                                      𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, _
                         𝜎 ⊢ if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠 → 𝑠 2 ; 𝑠 ⊣ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡]
              SExecWhileSkip
                                           𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , _
              𝑥 = modiﬁed(𝑠)     𝜎 [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ fresh]] ⊢ 𝜙˜ ⊳ 𝜎 ′′
                                            ′
                                                                               𝜎 ′′ ⊢ 𝑒 ↓ 𝑡 ⊣ _
                   𝜎 ⊢ while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ → 𝑠 ′ ⊣ 𝜎 ′′ [𝑔 = 𝑔(𝜎 ′′ ) && ! 𝑡]
                                          ˜ returns the set of all permissions remaining in 𝜎 if
Deﬁnition 28. The helper function rem(𝜎, 𝜙)
𝜙˜ is not completely precise:
                       
                       
                        ∅                                       if 𝜙˜ is completely precise
                       
                       
                  ˜                         ′
           rem(𝜎, 𝜙) := {h𝑡, 𝑓 i : h𝑓 , 𝑡, 𝑡 i ∈ H(𝜎) ∪ H (𝜎)} ∪
                       
                       
                        {h𝑝, 𝑡i : h𝑝, 𝑡i ∈ H(𝜎)}                otherwise
                       
This is used to symbolically calculate the required exclusion frame.

C.11 Verification states
Deﬁnition 29. A veriﬁcation state Σ is either an abstract symbol or a triple consisting of a
symbolic state, a statement, and a post-condition.
                                          Σ ::= init     |   final     |          ˜
                                                                           h𝜎, 𝑠, 𝜙i
Sound Gradual Verification with Symbolic Execution                                                    111:49


  The reachability of veriﬁcation transitions, as determined by modular veriﬁcation for a given
program Π, is determined by the judgement
                                                     Π ⊢ Σ → Σ′
where Σ is the beginning veriﬁcation state and Σ′ is the next veriﬁcation state.

                             SVerifyInit

                             h𝑠, 𝑀, 𝑃, 𝑆i ⊢ init → hh⊥, ∅, ∅, ∅, truei, 𝑠, truei
             SVerifyMethod
             𝑚∈𝑀             𝑥 = params(𝑚)           h⊥, ∅, ∅, [𝑥 ↦→ fresh], truei ⊢ pre(𝑚) ⊳ 𝜎
                             h𝑠, 𝑀, 𝑃, 𝑆i ⊢ init → h𝜎, body(𝑚); skip, post(𝑚)i
        SVerifyLoopBody
                        Π ⊢ _ → h𝜎0 , while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ , 𝜙˜0 i
        𝑥 = modiﬁed(𝑠)      h⊥, 𝛾 (𝜎0 ) [𝑥 ↦→ fresh], ∅, ∅, 𝑔(𝜎0 )i ⊢ 𝜙˜ ⊳ 𝜎0′      𝜎0′ ⊢ 𝑒 ↓ 𝑡 ⊣ R
          Π ⊢ h𝜎, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ , 𝜙˜0 i → h𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡], 𝑠; skip, 𝜙i
                                                                     0          0
                                                                                               ˜
            SVerifyLoop
                         Π ⊢ _ → h𝜎, while 𝑒 invariant 𝜙˜′ do 𝑠; 𝑠 ′, 𝜙i
                                                                       ˜
                  ˜′
             𝜎 ⊢𝜙 ⊲𝜎 , _ ′
                             𝑥 = modiﬁed(𝑠)      𝜎 [𝛾 = 𝛾 (𝜎) [𝑥 ↦→ fresh]] ⊢ 𝜙˜ ′ ⊳ 𝜎 ′′
                                                  ′

                          Π ⊢ h𝜎, while 𝑒 invariant 𝜙˜ ′ do 𝑠; 𝑠 ′, 𝜙i
                                                                    ˜ →
                                                          ˜
                                h𝜎 , while 𝑒 invariant 𝜙 do 𝑠; 𝑠 ′ , 𝜙i
                                   ′′                       ′          ˜
                                   SVerifyStep
                                                   ˜
                                   Π ⊢ _ → h𝜎, 𝑠, 𝜙i    𝜎 ⊢ 𝑠 → 𝑠′ ⊣ 𝜎′
                                                    ˜ → h𝜎 ′ , 𝑠 ′ , 𝜙i
                                        Π ⊢ h𝜎, 𝑠, 𝜙i                ˜
                                  SVerifyFinal
                                                    ˜
                                  Π ⊢ _ → h𝜎, skip, 𝜙i            𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, _
                                                          ˜ → final
                                           Π ⊢ h𝜎, skip, 𝜙i
Deﬁnition 30. A veriﬁcation state Σ is reachable from program Π if Σ = init or Π ⊢ _ → Σ, _, _, _.
  A veriﬁcation state Σ is reachable from program Π with valuation 𝑉 if Σ is reachable from Π
and 𝑉 is deﬁned for all symbolic values contained in Σ.

C.12 Guards
A guard judgement determines the set of runtime checks that must be satisﬁed at the given veriﬁ-
cation state before taking the next execution step, and determines the exclusion frame required to
preserve the validity of heap chunks contained by the current symbolic state. This is denoted by
the judgement
                                             Σ ⇀ 𝜎 ′, R, Θ
                                           ′
where Σ is the current veriﬁcation state, 𝜎 is the intermediate state, R is the set of required checks,
and Θ is the exclusion frame (represented as a set of symbolic permissions).

                                      SGuardInit

                                      init ⇀ h⊥, ∅, ∅, ∅, truei ⊣ ∅, ∅
                                           SGuardSeq

                                                        ˜ ⇀ 𝜎 ⊣ ∅, ∅
                                           h𝜎, skip; 𝑠, 𝜙i
111:50                                                                 C. Zimmerman, J. DiVincenzo, and J. Aldrich

                                       SGuardAssign
                                              𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R
                                                      ˜ ⇀ 𝜎 ⊣ R, ∅
                                        h𝜎, 𝑥 = 𝑒; 𝑠, 𝜙i

                            SGuardAssignField
                             𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R ′     𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ⊲ 𝜎 ′′ , R ′′
                                                   ˜ ⇀ 𝜎 ′′ ⊣ R ′ ∪ R ′′ , ∅
                                  h𝜎, 𝑥 .𝑓 = 𝑒; 𝑠, 𝜙i

                                   SGuardAlloc

                                                          ˜ ⇀ 𝜎 ⊣ ∅, ∅
                                    h𝜎, 𝑥 = alloc(𝑆); 𝑠, 𝜙i

           SGuardCall
           𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R      𝑥 = params(𝑚)        𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ pre(𝑚) ⊲ 𝜎 ′′ , R ′
                                     ˜ ⇀ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)] ⊣ R ∪ R ′ , rem(𝜎 ′′ , pre(𝑚))
                    h𝜎, 𝑦 = 𝑚(𝑒); 𝑠, 𝜙i

                                     SGuardAssert
                                            𝜎 ⊢ ? ∗ 𝜙 ⊲ 𝜎 ′, R
                                                      ˜ ⇀ 𝜎 ′ ⊣ R, ∅
                                     h𝜎, assert 𝜙; 𝑠, 𝜙i

  SGuardFold
  𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R      𝑥 = predicate_params(𝑝)          𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡 ]] ⊢ predicate(𝑝) ⊲ 𝜎 ′′ , R ′
                                                                          Ø
                                             ˜ ⇀ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)] ⊣ R ′ ∪
                         h𝜎, fold 𝑝 (𝑒); 𝑠, 𝜙i                                 R, ∅

                             SGuardUnfold
                                 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R   𝜎 ′ ⊢ 𝑝 (𝑒) ⊲ 𝜎 ′′ , R ′
                                                                      Ø
                                                   ˜ ⇀ 𝜎 ′′ ⊣ R ′ ∪
                              h𝜎, unfold 𝑝 (𝑒); 𝑠, 𝜙i                      R, ∅

                                SGuardIf
                                             𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R
                                                                ˜ ⇀ 𝜎 ′ ⊣ R, ∅
                                h𝜎, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠, 𝜙i

SGuardWhile
𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, R ′   𝑥 = modiﬁed(𝑠)      𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ fresh]] ⊢ 𝜙˜ ⊳ 𝜎 ′′         𝜎 ′′ ⊢ 𝑒 ↓ _ ⊣ R ′′
          h𝜎, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜ ′ i ⇀ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′′ )] ⊣ R ′ ∪ R ′′ , rem(𝜎 ′ , 𝜙)
                                                                                                    ˜

                                         SGuardFinish
                                                 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R
                                                      ˜ ⇀ 𝜎 ′ ⊣ R, ∅
                                           h𝜎, skip, 𝜙i

C.13 Valid states
Deﬁnition 31. A veriﬁcation state Σ corresponds with valuation 𝑉 to an execution state Γ if Σ =
Γ, or Γ = h𝐻, h𝛼, 𝜌, 𝑠i · Si for some 𝐻, 𝛼, 𝜌, 𝑠 and Σ = h𝜎, 𝑠, _i for some 𝜎, such that h𝐻, 𝛼, 𝜌i 𝑉 𝜎.

Deﬁnition 32. A partial state Γ = h𝐻, Si is validated by a veriﬁcation state Σ with valuation 𝑉
if one of the following cases apply:
   Part 32.1. S = nil
Sound Gradual Verification with Symbolic Execution                                                            111:51


  Part 32.2. S = h𝜌, 𝛼, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠i · S ∗ for some 𝜌, 𝛼, 𝑦, 𝑚, 𝑘, 𝑒 1 , · · · , 𝑒𝑘 , 𝑠, and S ∗ , and
there exists some Σ′ , 𝑉 ′ , 𝑥 1, · · · , 𝑥𝑘 , 𝑡 1 , · · · , 𝑡𝑘 , 𝜎0, · · · , 𝜎𝑘 and 𝜎 ′ such that:

                              The partial state h𝐻, S ∗ i is validated by Σ′ and 𝑉 ′ ,                            (5)
                         ′                                               ′         ′
                        Σ is reachable from Π with valuation 𝑉 ,              𝑠 (Σ ) = 𝑠 (S),                     (6)
                                            𝑥 1, · · · , 𝑥𝑘 = params(𝑚),                                          (7)
                                ′
                   𝜎0 = 𝜎 (Σ ),      𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1 , _,   ··· ,   𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,                 (8)
                                      ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 (𝛾 (Σ) (𝑥𝑖 )) = 𝑉 ′ (𝑡𝑖 ),                                  (9)
                       𝜎𝑘 ⊢ pre(𝑚) ⊲ 𝜎 ′ , _,         h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )],     and                  (10)
                                                   𝜙˜ (Σ) = post(𝑚)                                             (11)

  Part 32.3. S = h𝜌, 𝛼, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ for some 𝜌, 𝛼, 𝑒, 𝜙,
                                                                                 ˜ 𝑠, 𝑠 ′ , S ∗ , and there
              ′  ′       ′
exists some Σ , 𝑉 , and 𝜎 such that:

                              The partial state h𝐻, S ∗ i is validated by Σ′ and 𝑉 ′                            (12)
                          ′                                              ′             ′
                        Σ is reachable from Π with valuation 𝑉 ,              𝑠 (Σ ) = 𝑠 (S)                    (13)
                                    𝜎 ⊢ 𝜙˜ ⊲ 𝜎 , _,
                                               ′
                                                         and    h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎    ′
                                                                                                                (14)
                                                       𝜙˜ (Σ) = 𝜙˜                                              (15)

Deﬁnition 33. For a program Π, a dynamic state Γ is validated by Σ and valuation 𝑉 if all the
following are true:
   Part 33.1. Σ is reachable from Π with 𝑉
   Part 33.2. Γ corresponds to Σ with 𝑉
   Part 33.3. If Γ = h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i, then the partial state h𝐻, S ∗ i is validated by Σ and 𝑉 .

Deﬁnition 34. Γ is a valid state if Γ is validated by some Σ.

D SOUNDNESS
This section contains the proof of soundness, culminating in theorems 1, 2, and 3.

D.1    Cross-cutting lemmas
Lemma 1 (Relating expression framing and exact footprints). T𝑒U h𝐻, 𝜌 i ⊆ 𝛼 if and only if h𝐻, 𝛼, 𝜌i ⊢frm
𝑒.

  Proof. By induction on the syntax forms of 𝑒:
  Case 1. 𝑙: Then T𝑙U h𝐻, 𝜌 i = ∅, thus T𝑙U h𝐻, 𝜌 i ⊆ 𝛼, and h𝐻, 𝛼, 𝜌i ⊢frm 𝑙 by FrameLiteral.
  Case 2. 𝑣: Then T𝑣U h𝐻, 𝜌 i = ∅, thus T𝑣U h𝐻, 𝜌 i ⊆ 𝛼, and h𝐻, 𝛼, 𝜌i ⊢frm 𝑣 by FrameVar.
  Case 3. 𝑒.𝑓 :
  Suppose that T𝑒.𝑓 U h𝐻, 𝜌 i ⊆ 𝛼. Then by deﬁnition T𝑒U h𝐻, 𝜌 i ⊆ 𝛼 and hℓ, 𝑓 i ∈ 𝛼 for some ℓ such
that h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ. By induction h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, by AssertAcc h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ), and thus by
FrameField, h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.𝑓 .
  Suppose that h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.𝑓 . Then by FrameField, h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 and h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ),
thus by induction T𝑒U h𝐻, 𝑒𝑛𝑣i ⊆ 𝛼 and by AssertAcc, hℓ, 𝑓 i ∈ 𝛼 for some ℓ such that h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ.
Thus T𝑒.𝑓 U h𝐻, 𝜌 i = T𝑒U h𝐻, 𝜌 i ; hℓ, 𝑓 i ⊆ 𝛼.
111:52                                                                 C. Zimmerman, J. DiVincenzo, and J. Aldrich


   Case 4. 𝑒 1 ⊕ 𝑒 2 :
               T𝑒 1 ⊕ 𝑒 2 U h𝐻, 𝜌 i ⊆ 𝛼
                 ⇐⇒ T𝑒 1 U h𝐻, 𝜌 i ⊆ 𝛼 and T𝑒 2 U h𝐻, 𝜌 i ⊆ 𝛼                       by deﬁnition
                 ⇐⇒ h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2                       by induction
                 ⇐⇒ h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 ⊕ 𝑒 2                                         by FrameOp
   Case 5. 𝑒 1 || 𝑒 2 :
           T𝑒 1 || 𝑒 2 U h𝐻, 𝜌 i ⊆ 𝛼 =⇒
            either h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true and T𝑒 1 U h𝐻, 𝜌 i ⊆ 𝛼                          by deﬁnition
                =⇒ h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1                          by induction
                =⇒ h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2                                           by FrameOrA
            or h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false and T𝑒 1 U h𝐻, 𝜌 i ∪ T𝑒 2 U h𝐻, 𝜌 i ⊆ 𝛼            by deﬁnition
                =⇒ h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false, h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1,
                         and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2                                        by induction
                =⇒ h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2                                           by FrameOrB

         h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2 =⇒
          either h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1                             by FrameOrA
              =⇒ h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true and T𝑒 1 U h𝐻, 𝜌 i ⊆ 𝛼                              by induction
              =⇒ T𝑒 1 || 𝑒 2 U h𝐻, 𝜌 i ⊆ 𝛼                                               by deﬁnition
          or h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false, h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 ,
                and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2                                                   by FrameOrB
              =⇒ h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false and T𝑒 1 U h𝐻, 𝜌 i ∪ T𝑒 2 U h𝐻, 𝜌 i ⊆ 𝛼            by induction
              =⇒ T𝑒 1 || 𝑒 2 U h𝐻, 𝜌 i ⊆ 𝛼                                               by deﬁnition
   Case 6. 𝑒 1 && 𝑒 2 : Similar to case 5.
   Case 7. ! 𝑒:
                          T! 𝑒U h𝐻, 𝜌 i ⊆ 𝛼
                            ⇐⇒ T𝑒U h𝐻, 𝜌 i ⊆ 𝛼                                by deﬁnition
                            ⇐⇒ h𝐻, 𝛼, 𝜌i ⊢frm 𝑒                               by induction
                            ⇐⇒ h𝐻, 𝛼, 𝜌i ⊢frm ! 𝑒                             by FrameNeg
                                                                                                                
                                                                                      ˜ h𝐻, 𝛼, 𝜌i ⊢
Lemma 2 (Relating formula assertion/framing and exact footprints). If h𝐻, 𝛼 ′ , 𝜌i  𝜙,                         frmE
˜ and 𝛼 ′ ⊆ 𝛼, then T𝜙U
𝜙,                   ˜ h𝐻, 𝜌 i ⊆ 𝛼.

  Proof. By induction on h𝐻, 𝛼 ′ , 𝜌i  𝜙:˜
  Case 1. AssertImprecise – h𝐻, 𝛼 ′ , 𝜌i  ? ∗ 𝜙:
  By AssertImprecise, h𝐻, 𝛼 ′ , 𝜌i  𝜙 and h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙, therefore by induction T? ∗ 𝜙U h𝐻, 𝜌 i =
T𝜙U h𝐻, 𝜌 i ⊆ 𝛼.
  Case 2. AssertValue – h𝐻, 𝛼 ′ , 𝜌i  𝑒:
  Since h𝐻, 𝛼, 𝜌i ⊢frmE 𝑒, by EFrameExpression h𝐻, 𝛼, 𝜌i ⊢frm 𝑒. Thus by lemma 1, T𝜙U  ˜ h𝐻, 𝜌 i ⊆ 𝛼.
                             ′
  Case 3. AssertIfA – h𝐻, 𝛼 , 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2
Sound Gradual Verification with Symbolic Execution                                               111:53


   By AssertIfA, h𝐻, 𝜌i ⊢ 𝑒 ⇓ true. Then, since h𝐻, 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 ,
h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1 by EFrameConditionalA. Also, by AssertIfA, h𝐻, 𝛼 ′ , 𝜌i  𝜙 1 . Thus, by induc-
tion,
Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i = T𝜙 1 U h𝐻, 𝜌 i ⊆ 𝛼.
   Case 4. AssertIfB – h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 : Similar to case 3.
   Case 5. AssertAcc – h𝐻, 𝛼 ′ , 𝜌i  acc(𝑒.𝑓 )
   Since h𝐻, 𝛼, 𝜌i ⊢frmE acc(𝑒.𝑓 ), by EFrameAcc h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, thus by lemma 1 T𝑒U h𝐻, 𝜌 i ⊆
𝛼. By AssertAcc, h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ and hℓ, 𝑓 i ∈ 𝛼 ′ ⊆ 𝛼. Thus by deﬁnition Tacc(𝑒.𝑓 )U h𝐻, 𝜌 i =
T𝑒U h𝐻, 𝜌 i ; hℓ, 𝑓 i ⊆ 𝛼.
   Case 6. AssertConjunction – h𝐻, 𝛼 ′ , 𝜌i  𝜙 1 ∗ 𝜙 2
   Since h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1 ∗ 𝜙 2 , by EFrameConjunction h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1 and h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 2 .
Also, by AssertConjunction h𝐻, 𝛼 1 , 𝜌i  𝜙 1 and h𝐻, 𝛼 2, 𝜌i  𝜙 2 where 𝛼 1 ∪𝛼 2 ⊆ 𝛼 ′ ⊆ 𝛼. Therefore
by induction T𝜙 1 ∗ 𝜙 2 U h𝐻, 𝜌 i = T𝜙 1 U h𝐻, 𝜌 i ∪ T𝜙 2 U h𝐻, 𝜌 i ⊆ 𝛼.
   Case 7. AssertPredicate – h𝐻, 𝛼 ′ , 𝜌i  𝑝 (𝑒)
   Since h𝐻, 𝛼, 𝜌i ⊢frmE 𝑝 (𝑒), by EFramePredicate h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 and
h𝐻, 𝛼, [𝑥 ↦→ 𝑣]i ⊢frmE predicate(𝑝) where 𝑥 = predicate_params(𝑝). Also, by AssertPredicate
h𝐻, 𝛼 ′ , [𝑥 ↦→ 𝑣]i  predicate(𝑝). Thus by induction, Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑣 ] i ⊆ 𝛼.
   Also, by EFramePredicate h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 thus by 1 T𝑒U h𝐻, 𝜌 i ⊆ 𝛼 for all 𝑒.
                                                                         Ð
   Therefore by deﬁnition T𝑒U h𝐻, 𝜌 i = Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑣 ] i ∪ T𝑒U h𝐻, 𝜌 i ⊆ 𝛼.
                                                                                                     


                                                                       ˜ h𝐻, 𝛼 ′ , 𝜌i  𝜙,
Lemma 3 (Relating iso- and equi-recursive framing). If h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙,               ˜ and
 ′                          ˜
𝛼 ⊆ 𝛼, then h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙.

    Proof. By induction on h𝐻, 𝛼 ′ , 𝜌i  𝜙:  ˜
                                        ′
    Case 1. AssertImprecise – h𝐻, 𝛼 , 𝜌i  ? ∗ 𝜙:
    By AssertImprecise h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙, thus by EFrameImprecise h𝐻, 𝛼, 𝜌i ⊢frmE ? ∗ 𝜙
    Case 2. AssertValue – h𝐻, 𝛼 ′ , 𝜌i  𝑒:
    Since h𝐻, 𝛼, 𝜌i ⊢frmI 𝑒, by IFrameValue h𝐻, 𝛼, 𝜌i ⊢frm 𝑒. Then by EFrameValue h𝐻, 𝛼, 𝜌i ⊢frmE 𝑒.
    Case 3. AssertIfA – h𝐻, 𝛼 ′ , 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 :
    By AssertIfA h𝐻, 𝜌i ⊢ 𝑒 ⇓ true and h𝐻, 𝛼 ′ , 𝜌i  𝜙 1 . Then by IFrameConditionalA h𝐻, 𝛼, 𝜌i ⊢frmI
𝜙 1 . Thus by induction h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1 and then by EFrameConditionalA
h𝐻, 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 .
    Case 4. AssertIfB: Similar to case 3.
    Case 5. AssertAcc – h𝐻, 𝛼 ′ , 𝜌i  acc(𝑒.𝑓 )
    Since h𝐻, 𝛼, 𝜌i ⊢frmI acc(𝑒.𝑓 ), by IFrameAcc h𝐻, 𝛼, 𝜌i ⊢frm 𝑒. Thus by EFrameAcc h𝐻, 𝛼, 𝜌i ⊢frmE
acc(𝑒.𝑓 ).
    Case 6. AssertConjunction – h𝐻, 𝛼 ′ , 𝜌i  𝜙 1 ∗ 𝜙 2 :
    Since h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙 1 ∗ 𝜙 2 , by IFrameConjunction h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙 1 and h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙 2 .
Also, by AssertConjunction h𝐻, 𝛼 1, 𝜌i  𝜙 1 and h𝐻, 𝛼 2, 𝜌i  𝜙 2 where 𝛼 1, 𝛼 2 ⊆ 𝛼. Therefore by in-
duction h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1 and h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 2 , and thus by EFrameConjunction h𝐻, 𝛼, 𝜌i ⊢frmE
𝜙 1 ∗ 𝜙 2.
    Case 7. AssertPredicate – h𝐻, 𝛼 ′ , 𝜌i  𝑝 (𝑒):
    Since h𝐻, 𝛼, 𝜌i ⊢frmI 𝑝 (𝑒), by IFramePredicate h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.
    Also, by AssertPredicate h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 and h𝐻, 𝛼 ′ , [𝑥 ↦→ 𝑣]i  predicate(𝑝). Now, since 𝑝 is a
predicate, predicate(𝑝) must be a speciﬁcation, and thus one of the following cases applies:
111:54                                                                    C. Zimmerman, J. DiVincenzo, and J. Aldrich


   Case 7(a). predicate(𝑝) is precise and self-framed: Then h𝐻, 𝛼, [𝑥 ↦→ 𝑣]i ⊢frmI predicate(𝑝) by
deﬁnition 7. Thus by induction h𝐻, 𝛼, [𝑥 ↦→ 𝑣]i ⊢frmE predicate(𝑝). Then by EFramePredicate
h𝐻, 𝛼, 𝜌i ⊢frmE 𝑝 (𝑒).
   Case 7(b). predicate(𝑝) is imprecise: Then AssertImprecise must apply in order to derive
h𝐻, 𝛼 ′ , [𝑥 ↦→ 𝑣]i  predicate(𝑝), and thus h𝐻, 𝛼 ′ , [𝑥 ↦→ 𝑣]i ⊢frmE predicate(𝑝), and thus by lemma
8 h𝐻, 𝛼, [𝑥 ↦→ 𝑣]i ⊢frmE predicate(𝑝). Then by EFramePredicate h𝐻, 𝛼, 𝜌i ⊢frmE 𝑝 (𝑒).
                                                                                                     

Lemma 4 (Relating speciﬁcation assertion and exact footprints). If 𝜙˜ is a speciﬁcation and h𝐻, 𝛼, 𝜌i 
˜ then T𝜙U
𝜙,      ˜ h𝐻, 𝜌 i ⊆ 𝛼.

   Proof. Since 𝜙˜ is a speciﬁcation, one of the following cases must apply:
   Case 1. 𝜙˜ is precise and self-framed: Then by deﬁnition 7 h𝐻, 𝛼, 𝜌i ⊢frmI 𝜙,˜ and since h𝐻, 𝛼, 𝜌i 
 ˜ by lemma 3 h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙.
𝜙,                                  ˜ Therefore, by lemma 2 T𝜙U˜ h𝐻, 𝜌 i ⊆ 𝛼.
            ˜                         ˜
   Case 2. 𝜙 is imprecise: Then 𝜙 = ? ∗ 𝜙 for some 𝜙 ∈ Formula, and AssertImprecise must apply
in order to derive h𝐻, 𝛼, 𝜌i  𝜙.   ˜ Therefore h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙, and thus by lemma 2 T𝜙U h𝐻, 𝜌 i ⊆ 𝛼.
Thus by deﬁnition T𝜙U   ˜ h𝐻, 𝜌 i = T𝜙U h𝐻, 𝜌 i ⊆ 𝛼.
                                                                                                     

Lemma 5 (Relating speciﬁcation assertion and footprints). If 𝜙˜ is a speciﬁcation and h𝐻, 𝛼, 𝜌i  𝜙,
                                                                                                  ˜
      ˜
then ⌊𝜙⌋ h𝐻, 𝛼, 𝜌 i ⊆ 𝛼.

     Proof. If 𝜙˜ is completely precise then ⌊𝜙⌋
                                              ˜ h𝐻, 𝛼, 𝜌 i = T𝜙U
                                                              ˜ h𝐻, 𝜌 i ⊆ 𝛼.
                   ˜
     Otherwise, ⌊𝜙⌋ h𝐻, 𝛼, 𝜌 i = 𝛼.                                                                                

Lemma 6 (Relating speciﬁcation exact footprints and footprints). If 𝜙˜ is a speciﬁcation and h𝐻, 𝛼, 𝜌i 
˜ then T𝜙U
𝜙,      ˜ h𝐻, 𝜌 i ⊆ ⌊𝜙⌋
                      ˜ h𝐻, 𝛼, 𝜌 i .

     Proof. If 𝜙˜ is completely precise then T𝜙U˜ h𝐻, 𝜌 i = ⌊𝜙⌋ ˜ h𝐻, 𝛼, 𝜌 i .
     Otherwise, by lemma 4 T𝜙U ˜ h𝐻, 𝜌 i ⊆ 𝛼 = ⌊𝜙⌋
                                                 ˜ h𝐻, 𝛼, 𝜌 i .                                                    

Lemma 7 (Monotonicity of expression framing WRT permissions). If h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 and 𝛼 ⊆ 𝛼 ′ ,
then h𝐻, 𝛼 ′ , 𝜌i ⊢frm 𝑒.
     Proof. By 1, T𝑒U h𝐻, 𝜌 i ⊆ 𝛼, thus T𝑒U h𝐻, 𝜌 i ⊆ 𝛼 ′ , and therefore h𝐻, 𝛼 ′ , 𝜌i ⊢frm 𝑒 by 1.                

Lemma 8 (Monotonicity of equi-recursive framing WRT permissions). If h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙˜ and
                                  ˜
𝛼 ⊆ 𝛼 ′ , then h𝐻, 𝛼 ′ , 𝜌i ⊢frmE 𝜙.
                                             ˜
     Proof. By induction on h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙:
     Case 1. EFrameExpression – h𝐻, 𝛼, 𝜌i ⊢frmE 𝑒: By lemma 7.
     Case 2. EFrameConjunction – h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1 ∗ 𝜙 2 : By induction
     Case 3. EFramePredicate – h𝐻, 𝛼, 𝜌i ⊢frmE 𝑝 (𝑒): By induction and lemma 7.
     Case 4. EFrameConditionalA – h𝐻, 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 : By induction and lemma
7.
     Case 5. EFrameConditionalB – h𝐻, 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 : By induction and lemma
7.
     Case 6. EFrameAcc – h𝐻, 𝛼, 𝜌i ⊢frmE acc(𝑒): By lemma 7.
                                                                                                                   
Sound Gradual Verification with Symbolic Execution                                                              111:55


Lemma 9 (Monotonicity of assertions WRT permissions). If h𝐻, 𝛼, 𝜌i  𝜙˜ and 𝛼 ⊆ 𝛼 ′ , then
               ˜
h𝐻, 𝛼 ′ , 𝜌i  𝜙.

  Proof. By induction on h𝐻, 𝛼, 𝜌i  𝜙:    ˜
  Case 1. AssertImprecise – h𝐻, 𝛼, 𝜌i  ? ∗ 𝜙: By induction and lemma 8.
  Case 2. AssertValue – h𝐻, 𝛼, 𝜌i  𝑒: Trivial.
  Case 3. AssertIfA – h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 : By induction.
  Case 4. AssertIfB – h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 : By induction.
  Case 5. AssertAcc – h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ): Then h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ and hℓ, 𝑓 i ∈ 𝛼, thus hℓ, 𝑓 i ∈ 𝛼 ′ .
Therefore h𝐻, 𝛼 ′ , 𝜌i  acc(𝑒.𝑓 ) by AssertAcc.
  Case 6. AssertConjunction – h𝐻, 𝛼, 𝜌i  𝜙 1 ∗ 𝜙 2 : Then h𝐻, 𝛼, 𝜌i  𝜙 1 and h𝐻, 𝛼 2, 𝜌i  𝜙 2
where 𝛼 1 ∩ 𝛼 2 = ∅ and 𝛼 1 ∪ 𝛼 2 ⊆ 𝛼 ⊆ 𝛼 ′ . Therefore h𝐻, 𝛼 ′ , 𝜌i  𝜙 1 ∗ 𝜙 2 by AssertConjunction.
  Case 7. AssertPredicate – h𝐻, 𝛼, 𝜌i  𝑝 (𝑒): By induction.
                                                                                                       


                                                                                ˜ then
Lemma 10 (Exact footprint preserves equi-recursive framing). If h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙,
     ˜                        ˜
h𝐻, T𝜙U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frmE 𝜙.

   Proof. By induction on h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙:        ˜
   Case 1. EFrameExpression – h𝐻, 𝛼, 𝜌i ⊢frmE 𝑒: By EFrameExpression h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, thus
T𝑒U h𝐻, 𝜌 i ⊆ 𝛼 and h𝐻, T𝑒U h𝐻, 𝜌 i , 𝜌i ⊢frm 𝑒 by lemma 1. Then T𝑒U h𝐻, 𝜌 i ∩ 𝛼 = T𝑒U h𝐻, 𝜌 i . Therefore
h𝐻, T𝑒U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frmE 𝑒 by EFrameExpression.
   Case 2. EFrameConjunction – h𝐻, 𝛼, 𝜌i ⊢frmE 𝑒 1 ∗ 𝑒 2 : By EFrameConjunction h𝐻, 𝛼, 𝜌i ⊢frmE 𝑒 1
and h𝐻, 𝛼, 𝜌i ⊢frmE 𝑒 2 , thus by induction h𝐻, T𝑒 1 U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frmE 𝑒 1 and h𝐻, T𝑒 2 U h𝐻, 𝜌 i ∩
𝛼, 𝜌i ⊢frmE 𝑒 2 .
   By deﬁnition T𝑒 1 ∗ 𝑒 2 U h𝐻, 𝜌 i ∩ 𝛼 = (T𝑒 1 U h𝐻, 𝜌 i ∩ 𝛼) ∪ (T𝑒 2 U h𝐻, 𝜌 i ∩ 𝛼), thus h𝐻, T𝑒 1 ∗ 𝑒 2 U h𝐻, 𝜌 i ∩
𝛼, 𝜌i ⊢frmE 𝑒 1 and h𝐻, T𝑒 1 ∗ 𝑒 2 U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frmE 𝑒 2 by lemma 8. Therefore h𝐻, T𝑒 1 ∗ 𝑒 2 U h𝐻, 𝜌 i ∩
𝛼, 𝜌i ⊢frmE 𝑒 1 ∗ 𝑒 2 by EFrameConjunction.
   Case 3. EFramePredicate – h𝐻, 𝛼, 𝜌i ⊢frmE 𝑝 (𝑒): By EFramePredicate h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, thus by
lemma 1 T𝑒U h𝐻, 𝜌 i ⊆ 𝛼, thus T𝑒U h𝐻, 𝜌 i ∩ 𝛼 = T𝑒U h𝐻, 𝜌 i , and then h𝐻, T𝑒U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frm 𝑒.
   By EFramePredicate h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 and h𝐻, 𝛼, [𝑥 ↦→ 𝑣]i ⊢frmE predicate(𝑝) where
𝑥 = predicate_params(𝑝). Thus by induction h𝐻, Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑣] i ∩ 𝛼, [𝑥 ↦→ 𝑣]i ⊢frmE
predicate(𝑝).
                                                                                        Ð
   Now by deﬁnition T𝑝 (𝑒)U h𝐻, 𝛼 i ∩ 𝛼 = (Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑣 ] i ∩ 𝛼) ∪ (T𝑒U h𝐻, 𝜌 i ∩ 𝛼). There-
fore by lemma 8 h𝐻, T𝑝 (𝑒)U h𝐻, 𝜌 i ∩ 𝛼, [𝑥 ↦→ 𝑣]i ⊢frmE predicate(𝑝) and
h𝐻, T𝑝 (𝑒)U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frm 𝑒.
   Thus h𝐻, T𝑝 (𝑒)U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frmE 𝑝 (𝑒) by EFramePredicate.
   Case 4. EFrameConditionalA – h𝐻, 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 : By EFrameConditionalA
h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1 and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, thus by induction h𝐻, T𝜙 1 U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frmE 𝜙 1 , and by
lemma 1 T𝑒U h𝐻, 𝜌 i ⊆ 𝛼, thus T𝑒U h𝐻, 𝜌 i ∩ 𝛼 = T𝑒U h𝐻, 𝜌 i , and ﬁnally h𝐻, T𝑒U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frm 𝑒.
   Also by EFrameConditionalA h𝐻, 𝜌i ⊢ 𝑒 ⇓ true, thus by deﬁnition Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i ∩
𝛼 = (T𝑒U h𝐻, 𝜌 i ∩ 𝛼) ∪ (T𝜙 1 U h𝐻, 𝜌 i ∩ 𝛼). Therefore h𝐻, Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frmE 𝜙 1
by lemma 8 and h𝐻, Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frm 𝑒 by 7, thus
h𝐻, Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 by EFrameConditionalA.
   Case 5. EFrameConditionalB – h𝐻, 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 : Similar to case 4.
111:56                                                                   C. Zimmerman, J. DiVincenzo, and J. Aldrich


   Case 6. EFrameAcc – h𝐻, 𝛼, 𝜌i ⊢frmE acc(𝑒.𝑓 ): By EFrameAcc h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, thus by lemma
1 T𝑒U h𝐻, 𝜌 i ⊆ 𝛼, thus T𝑒U h𝐻, 𝜌 i ∩ 𝛼 = T𝑒U h𝐻, 𝜌 i , and thus h𝐻, T𝑒U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frm 𝑒. By def-
inition T𝑒U h𝐻, 𝜌 i ⊆ Tacc(𝑒.𝑓 )U h𝐻, 𝜌 i , thus h𝐻, Tacc(𝑒.𝑓 )U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frm 𝑒 by 7. Therefore
h𝐻, Tacc(𝑒.𝑓 )U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i ⊢frmE acc(𝑒.𝑓 ) by EFrameAcc.
                                                                                                      
                                                                ˜ then h𝐻, T𝜙U
Lemma 11 (Exact footprint preserves assertions). If h𝐻, 𝛼, 𝜌i  𝜙,          ˜ h𝐻, 𝜌 i ∩ 𝛼, 𝜌i  𝜙.
                                                                                                ˜

   Proof. By induction on h𝐻, 𝛼, 𝜌i  𝜙:              ˜
   Case 1. AssertImprecise – h𝐻, 𝛼, 𝜌i  ? ∗𝜙: By AssertImprecise h𝐻, 𝛼, 𝜌i  𝜙, thus by induction
h𝐻, T𝜙U h𝐻, 𝜌 i ∩ 𝛼, 𝜙i .
   Also by AssertImprecise h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙, thus by lemma 10 h𝐻, T𝜙U h𝐻, 𝜌 i ∩ 𝛼, 𝜙i ⊢frmE.
   By deﬁnition T? ∗ 𝜙U h𝐻, 𝜌 i = T𝜙U h𝐻, 𝜌 i , thus h𝐻, T? ∗ 𝜙U h𝐻, 𝜌 i ∩ 𝛼, 𝜙i  and h𝐻, T? ∗ 𝜙U h𝐻, 𝜌 i ∩
𝛼, 𝜙i ⊢frmE . Therefore h𝐻, T? ∗ 𝜙U h𝐻, 𝜌 i ∩ 𝛼, ? ∗ 𝜙i  by AssertImprecise.
   Case 2. AssertValue – h𝐻, 𝛼, 𝜌i  𝑒: By AssertValue h𝐻, 𝜌i ⊢ 𝑒 ⇓ true, thus h𝐻, T𝑒U h𝐻, 𝜌 i , 𝜌i 
𝑒 by AssertValue.
   Case 3. AssertIfA – h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 : By AssertIfA h𝐻, 𝛼, 𝜌i  𝜙 1 , thus by
induction h𝐻, T𝜙 1 U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i  𝜙 1 .
   Also by AssertIfA h𝐻, 𝜌i ⊢ 𝑒 ⇓ true, thus Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i = T𝑒U h𝐻, 𝜌 i ∪ T𝜙 1 U h𝐻, 𝜌 i .
Therefore h𝐻, Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i  𝜙 1 by 9.
   Thus h𝐻, Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 by AssertIfA.
   Case 4. AssertIfB – h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 : Similar to case 3.
   Case 5. AssertAcc – h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ): By AssertAcc h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ and hℓ, 𝑓 i ∈ 𝛼.
By deﬁnition Tacc(𝑒.𝑓 )U h𝐻, 𝜌 i = T𝑒U h𝐻, 𝜌 i ∪ {hℓ, 𝑓 i}, thus hℓ, 𝑓 i ∈ Tacc(𝑒.𝑓 )U h𝐻, 𝜌 i . Therefore
h𝐻, Tacc(𝑒.𝑓 )U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i  acc(𝑒.𝑓 ) by AssertAcc.
   Case 6. AssertConjunction – h𝐻, 𝛼, 𝜌i  𝜙 1 ∗𝜙 2 : Let 𝛼 1′ = T𝜙 1 U h𝐻, 𝜌 i ∩𝛼 1 and 𝛼 2′ = T𝜙 2 U h𝐻, 𝜌 i ∩𝛼 2 .
By AssertConjunction h𝐻, 𝛼 1, 𝜌i  𝜙 1 and h𝐻, 𝛼 2, 𝜌i  𝜙 2 , thus by induction h𝐻, 𝛼 1′ , 𝜌i  𝜙 1 and
h𝐻, 𝛼 2′ , 𝜌i  𝜙 2 .
   Also by AssertConjunction 𝛼 1 ∩ 𝛼 2 = ∅ and 𝛼 1 ∪ 𝛼 2 ⊆ 𝛼, thus 𝛼 1′ ∩ 𝛼 2′ = ∅ and 𝛼 1′ ∪ 𝛼 2′ ⊆
T𝜙 1 ∗ 𝜙 2 U h𝐻, 𝜌 i = T𝜙 1 U h𝐻, 𝜌 i ∪ T𝜙 2 U h𝐻, 𝜌 i .
   Therefore h𝐻, T𝜙 1 ∗ 𝜙 2 U h𝐻, 𝜌 i , 𝜌i  𝜙 1 ∗ 𝜙 2 by AssertConjunction.
   Case 7. AssertPredicate – h𝐻, 𝛼, 𝜌i  𝑝 (𝑒): By AssertPredicate h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 and
h𝐻, 𝛼, [𝑥 ↦→ 𝑣]i  predicate(𝑝) where 𝑥 = predicate_params(𝑝). Thus by induction
h𝐻, Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑣 ] i ∩ 𝛼, [𝑥 ↦→ 𝑣]i  predicate(𝑝).
   Now by deﬁnition Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑣] i ⊆ T𝑝 (𝑒)U h𝐻, 𝜌 i , thus by lemma 9 h𝐻, T𝑝 (𝑒)U h𝐻, 𝜌 i ∩
𝛼, [𝑥 ↦→ 𝑣]i  predicate(𝑝). Therefore h𝐻, T𝑝 (𝑒)U h𝐻, 𝜌 i ∩ 𝛼, 𝜌i  𝑝 (𝑒) by AssertPredicate.
                                                                                                                 

Lemma 12 (Supersets of exact footprints preserve assertions). If h𝐻, 𝛼, 𝜌i  𝜙˜ and T𝜙U
                                                                                     ˜ h𝐻, 𝜌 i ⊆ 𝛼 ′ ,
                     ˜
then h𝐻, 𝛼 ′ , 𝜌i  𝜙.
                          ˜ h𝐻, 𝜌 i ∩ 𝛼, 𝜌i  𝜙.
  Proof. By lemma 11 h𝐻, T𝜙U                   ˜ Then T𝜙U
                                                       ˜ h𝐻, 𝜌 i ∩ 𝛼 ⊆ 𝛼 ′ , thus h𝐻, 𝛼 ′ , 𝜌i  𝜙˜ by
lemma 9.                                                                                             

Lemma 13 (Footprints preserve speciﬁcation assertions). If 𝜙˜ is a speciﬁcation and h𝐻, 𝛼, 𝜌i  𝜙,
                                                                                                ˜
          ˜                    ˜
then h𝐻, ⌊𝜙⌋ h𝐻, 𝛼, 𝜌 i , 𝜌i  𝜙.
                       ˜ h𝐻, 𝜌 i ⊆ ⌊𝜙⌋
   Proof. By lemma 6, T𝜙U           ˜ h𝐻, 𝛼, 𝜌 i . Therefore h𝐻, ⌊𝜙⌋
                                                                  ˜ h𝐻, 𝛼, 𝜌 i , 𝜌i  𝜙˜ by lemma 12. 
Sound Gradual Verification with Symbolic Execution                                                         111:57


Lemma 14 (Modeling implies ownership). If h𝐻, 𝛼, 𝜌i 𝑉 𝜎 then
                                      ∀ℎ ∈ H(𝜎) ∪ H (𝜎) : 𝑉 LℎM𝐻 ⊆ 𝛼.
  Proof. Let ℎ be an arbitrary element of H(𝜎) or H (𝜎). Then one of the following cases applies:
  Case 1. ℎ = h𝑓 , 𝑡, 𝑡 ′ i for some 𝑓 , 𝑡, 𝑡 ′ :
  Since h𝐻, 𝛼i 𝑉 H(𝜎) (and likewise for H (𝜎)), then h𝑉 (𝑡), 𝑓 i ∈ 𝛼. Therefore 𝑉 Lh𝑓 , 𝑡, 𝑡 ′ iM𝐻 =
{h𝑉 (𝑡), 𝑓 i} ⊆ 𝛼.
  Case 2. ℎ = h𝑝, 𝑡 i for some 𝑝, 𝑡:
  Then ℎ ∈ H(𝜎) since H (𝜎) does not contain predicate chunks. Since h𝐻, 𝛼i 𝑉 H(𝜎),
h𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝). predicate(𝑝) must be a speciﬁcation, thus by lemma 4
𝑉 Lh𝑝, 𝑡iM𝐻 = Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 (𝑡 ) ] i ⊆ 𝛼.
                                                                                                               
Lemma 15 (Correspondence with exclusion implies disjointness). If h𝐻, 𝛼 \ 𝛼 ′ , 𝜌i 𝑉 𝜎, then
                                        ∀ℎ ∈ H(𝜎) : 𝑉 LℎM𝐻 ∩ 𝛼 ′ = ∅.
  Proof. Let ℎ be an arbitrary element of H(𝜎). Then 𝑉 LℎM𝐻 ⊆ 𝛼 \ 𝛼 ′ by lemma 14, thus 𝑉 LℎM𝐻 ∩
𝛼 ′ = ∅.                                                                                       
Lemma 16 (Disjointness implies correspondence with exclusion). If h𝐻, 𝛼i 𝑉 H and ∀ℎ ∈ H :
𝑉 LℎM𝐻 ∩ 𝛼 ′ = ∅, then h𝐻, 𝛼 \ 𝛼 ′ i 𝑉 H.

  Proof. Since h𝐻, 𝛼i 𝑉 H,
                                    ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ).
  Let h𝑓 , 𝑡, 𝑡 ′ i be an arbitrary ﬁeld chunk in H. Then, by deﬁnition, 𝑉 Lh𝑓 , 𝑡, 𝑡 ′ iM𝐻 = {h𝑉 (𝑡), 𝑓 i}.
Thus {h𝑉 (𝑡), 𝑓 i} ∩ 𝛼 ′ = ∅ and then h𝑉 (𝑡), 𝑓 i ∉ 𝛼 ′ . Therefore h𝑉 (𝑡), 𝑓 i ∈ (𝛼 \ 𝛼 ′ ). Thus
                                   ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H : h𝑉 (𝑡), 𝑓 i ∈ (𝛼 \ 𝛼 ′ ).
  Let h𝑝, 𝑡 i be an arbitrary predicate in H. Since h𝐻, 𝛼i 𝑉 H, h𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝).
By deﬁnition, 𝑉 Lh𝑝, 𝑡iM𝐻 = Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 (𝑡 ) ] i . Thus Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 (𝑡 ) ] i ∩𝛼 ′ = ∅,
and therefore Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 (𝑡 ) ] i ⊆ (𝛼 \ 𝛼 ′ ). Thus by lemma 12 h𝐻, 𝛼 \ 𝛼 ′ , [𝑥 ↦→ 𝑉 (𝑡)]i 
predicate(𝑝). Therefore
                         ∀ h𝑝, 𝑡i ∈ H : h𝐻, 𝛼 \ 𝛼 ′ , [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝).
  Finally, since h𝐻, 𝛼i 𝑉 H,
                        ∀ℎ 1 , ℎ 2 ∈ H2 : ℎ 1 ≠ ℎ 2 =⇒ Tℎ 1 U h𝑉 , 𝐻 i ∩ Tℎ 2 U h𝑉 , 𝐻 i = ∅.
  Thus all conditions in (1) are satisﬁed, therefore h𝐻, 𝛼 \ 𝛼 ′ i 𝑉 H.                                        

Lemma 17. If h𝐻, 𝛼i 𝑉 H and 𝛼 ⊆ 𝛼 ′ , then h𝐻, 𝛼i 𝑉 H.

  Proof. Let h𝑓 , 𝑡, 𝑡 ′ i ∈ H. Since h𝐻, 𝛼i          𝑉
                                                          H, 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ) and h𝑉 (𝑡), 𝑓 i ∈ 𝛼 ⊆ 𝛼 ′ .
Therefore
                                ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ )    and
                                                  ′                           ′
                                      ∀ h𝑓 , 𝑡, 𝑡 i ∈ H : h𝑉 (𝑡), 𝑓 i ∈ 𝛼 .
111:58                                                                                         C. Zimmerman, J. DiVincenzo, and J. Aldrich


     Let h𝑝, 𝑡 i ∈ H. Since h𝐻, 𝛼i                 𝑉
                                                         H, h𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝). Then by lemma 9,
         ′
h𝐻, 𝛼 , [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝). Therefore
                                 ∀ h𝑝, 𝑡i ∈ H : h𝐻, 𝛼 ′ , [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝).
     Now, since h𝐻, 𝛼i 𝑉 H,
                                 ∀ℎ 1 , ℎ 2 ∈ H : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 Lℎ 1 M𝐻 ∩ 𝑉 Lℎ 2 M𝐻 = ∅.
     Therefore h𝐻, 𝛼 ′ i     𝑉
                                 H.                                                                                                            

Lemma 18. If h𝐻, 𝛼i 𝑉 H and 𝛼 ⊆ 𝛼 ′ , then h𝐻, 𝛼i 𝑉 H.
     Proof. Similar to proof of 17.                                                                                                            
Lemma 19. If h𝐻, 𝛼, 𝜌i 𝑉 𝜎 and 𝛼 ⊆ 𝛼 ′ , then h𝐻, 𝛼 ′ , 𝜌i 𝑉 𝜎.

     Proof. Since h𝐻, 𝛼, 𝜌i 𝑉 𝜎, 𝑉 (𝑔(𝜎)) = true and 𝜌 𝑉 𝛾 (𝜎).
     Also by lemma 17 h𝐻, 𝛼 ′ i 𝑉 H(𝜎) and by lemma 18 h𝐻, 𝛼 ′ i 𝑉 H (𝜎).
     Therefore h𝐻, 𝛼 ′ , 𝜌i 𝑉 𝜎 ′ .                                                                                                            
Lemma 20 (Statement rearrangement). If 𝑠 = 𝑠 1 ; 𝑠 2 , then 𝑠 = 𝑠 1′ ; 𝑠 2′ such that 𝑠 1′ is not a sequence
statement and 𝑠 2′ = 𝑠 2 or 𝑠 2′ = 𝑠 1′′ ; 𝑠 2 where 𝑠 1 = 𝑠 1′ ; 𝑠 1′′ .
  Proof. Suppose 𝑠 = 𝑠 1 ; 𝑠 2 . Complete the proof by induction on the syntax forms of 𝑠 1 :
  Case 1. 𝑠 1 is not a sequence statement – Let 𝑠 1′ = 𝑠 1 and 𝑠 2′ = 𝑠 2 . Then 𝑠 = 𝑠 1′ ; 𝑠 2′ where 𝑠 1′ is not a
sequence statement and 𝑠 2 = 𝑠 2′ .
  Case 2. 𝑠 1 = 𝑠 11 ; 𝑠 12 – Then 𝑠 = (𝑠 11 ; 𝑠 12 ); 𝑠 2 .
  Applying the inductive hypothesis on 𝑠 1 , 𝑠 1 = 𝑠 11       ′ ; 𝑠 ′ such that 𝑠 ′ is not a sequence statement
                                                                   12            11
and one of the following cases apply:
               ′ = 𝑠 – Let 𝑠 ′ = 𝑠 ′ , 𝑠 ′′ = 𝑠 , and 𝑠 ′ = 𝑠 ; 𝑠 . Then
  Case 2(a). 𝑠 12      12        1    11 1          12       2       12 2
                                               ′      ′
                            𝑠 = 𝑠 1 ; 𝑠 2 = (𝑠 11 ; 𝑠 12 ); 𝑠 2 = (𝑠 1′ ; 𝑠 12 ); 𝑠 2 = 𝑠 1′ ; (𝑠 12 ; 𝑠 2 ) = 𝑠 1′ ; 𝑠 2′
                           𝑠 2′ = 𝑠 12 ; 𝑠 2 = 𝑠 1′′ ; 𝑠 2
                                   ′      ′
                           𝑠 1 = 𝑠 11 ; 𝑠 12 = 𝑠 1′ ; 𝑠 12 = 𝑠 1′ ; 𝑠 1′′
which satisﬁes the original statement.
               ′ = 𝑠 ′′ ; 𝑠 where 𝑠 = 𝑠 ′ ; 𝑠 ′′ – Let 𝑠 ′ = 𝑠 ′ , 𝑠 ′′ = 𝑠 ′′ ; 𝑠 , and 𝑠 ′ = 𝑠 ′′ ; 𝑠 ; 𝑠 . Then
  Case 2(b). 𝑠 12   11 12          11  11 11            1     11 1         11 12          2     11 12 2
                                      ′      ′              ′       ′′                    ′       ′′
                   𝑠 = 𝑠 1 ; 𝑠 2 = (𝑠 11 ; 𝑠 12 ); 𝑠 2 = (𝑠 11 ; (𝑠 11 ; 𝑠 12 )); 𝑠 2 = 𝑠 11 ; (𝑠 11 ; 𝑠 12 ; 𝑠 2 ) = 𝑠 1′ ; 𝑠 2′
                  𝑠 2′ = 𝑠 11
                           ′′                   ′′
                              ; 𝑠 12 ; 𝑠 2 = (𝑠 11 ; 𝑠 12 ); 𝑠 2 = 𝑠 1′′ ; 𝑠 2
                          ′      ′      ′       ′′
                  𝑠 1 = 𝑠 11 ; 𝑠 12 = 𝑠 11 ; (𝑠 11 ; 𝑠 12 ) = 𝑠 1′ ; 𝑠 1′′
which satisﬁes the original statement.
                                                                                                                                               
Lemma 21 (Run-time check monotonicity WRT permissions). If h𝐻, 𝛼i ⊢𝑉                                                         𝑟 and 𝛼 ⊆ 𝛼 ′ , then
h𝐻, 𝛼 ′ i ⊢𝑉 𝑟 .
     Proof. By cases on h𝐻, 𝛼i ⊢𝑉 𝑟 :
     Case 1. CheckValue – h𝐻, 𝛼i ⊢𝑉 𝑡: By CheckValue 𝑉 (𝑡) = true, thus by CheckValue h𝐻, 𝛼 ′ i ⊢𝑉
𝑡.
  Case 2. CheckAcc – h𝐻, 𝛼i ⊢𝑉 h𝑓 , 𝑡i: By CheckAcc h𝑉 (𝑡), 𝑓 i ∈ 𝛼, thus h𝑉 (𝑡), 𝑓 i ∈ 𝛼 ′ and
therefore h𝐻, 𝛼 ′ i ⊢𝑉 h𝑡, 𝑓 i by CheckAcc.
Sound Gradual Verification with Symbolic Execution                                                 111:59


   Case 3. CheckPred – h𝐻, 𝛼i ⊢𝑉 h𝑝, 𝑡i: By CheckPred h𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝) where
𝑥 = predicate_params(𝑝). Then by lemma 9, h𝐻, 𝛼 ′ , [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝). Therefore
h𝐻, 𝛼 ′ i ⊢𝑉 h𝑝, 𝑡 i by CheckPred. CheckSep – h𝐻, 𝛼i ⊢𝑉 sep(Θ1, Θ2 ): By CheckSep 𝑉 LΘ1 M𝐻 ∩
𝑉 LΘ2 M𝐻 = ∅, therefore h𝐻, 𝛼i ⊢𝑉 sep(Θ1 , Θ2 ) by CheckSep.
                                                                                             
Lemma 22 (Run-time checks monotonicity WRT permissions). If h𝐻, 𝛼i ⊢𝑉 R and 𝛼 ⊆ 𝛼 ′ , then
h𝐻, 𝛼 ′ i ⊢𝑉 R.
  Proof. Then by deﬁnition ∀ 𝑟 ∈ R : h𝐻, 𝛼i ⊢𝑉 𝑟 and then by lemma 21 ∀ 𝑟 ∈ R : h𝐻, 𝛼 ′ i ⊢𝑉 𝑟 .
Thus h𝐻, 𝛼 ′ i ⊢𝑉 R.                                                                         
Lemma 23 (Run-time check set implies subsets). If h𝐻, 𝛼i ⊢𝑉 R and R ′ ⊆ R, then h𝐻, 𝛼i ⊢𝑉 R ′ .
    Proof. By deﬁnition ∀ 𝑟 ∈ R : h𝐻, 𝛼i ⊢𝑉 𝑟 and ∀ 𝑟 ∈ R ′ : 𝑟 ∈ R, therefore ∀ 𝑟 ∈ R ′ : h𝐻, 𝛼i ⊢𝑉
𝑟 . Thus h𝐻, 𝛼i ⊢𝑉 R ′ .                                                                           

D.2    Evaluation
Deﬁnition 35. For a judgement 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R, given an initial valuation 𝑉 and heap 𝐻 , the
corresponding valuation is denoted
                                           𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻 ].
This valuation is deﬁned as follows, depending on the rule that proves the derivation. Values are
referenced using the respective name from the rule deﬁnition.
   Note that the corresponding valuation always extends the initial valuation, and is deﬁned for
all fresh symbolic values in the judgement.
 • SEvalLiteral:
                                    𝑉 [𝜎 ⊢ 𝑙 ⇓ 𝑙 ⊣ 𝜎, _ | 𝐻 ] := 𝑉
 • SEvalVar:
                                         𝑉 [𝜎 ⊢ 𝑥 ⇓ _ ⊣ 𝜎, _ | 𝐻 ] := 𝑉
 • SEvalNeg:
                        𝑉 [𝜎 ⊢ ! 𝑒 ⇓ ! 𝑡 ⊣ 𝜎 ′, R | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻 ]
 • SEvalOrA:
                     𝑉 [𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′ , R | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R | 𝐻 ]
 • SEvalOrB:
                          𝑉 [𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 1 ∪ R 2 | 𝐻 ] :=
                                𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R 1 | 𝐻 ]
                                    [𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡 1 ] ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 2 | 𝐻 ]
 • SEvalAndA:
                     𝑉 [𝜎 ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′ , R | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R | 𝐻 ]
 • SEvalAndB:
                           𝑉 [𝜎 ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 1 ∪ R 2 | 𝐻 ] :=
                                 𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′ , R 1 | 𝐻 ]
                                     [𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡 1 ] ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 2 | 𝐻 ]
111:60                                                                       C. Zimmerman, J. DiVincenzo, and J. Aldrich


 • SEvalOp:
                              𝑉 [𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑡 1 ⊕ 𝑡 2 ⊣ 𝜎 ′′ , R 1 ∪ R 2 | 𝐻 ] :=
                                    𝑉 [𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R 1 | 𝐻 ]
                                       [𝜎 ′ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 2 | 𝐻 ]
 • SEvalField or SEvalFieldOptimistic:
                        𝑉 [𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′′ , _ | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, R | 𝐻 ]
 • SEvalFieldImprecise:
             𝑉 [𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′′ , _ | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, R | 𝐻 ] [𝑡 ↦→ 𝐻 (𝑉 (𝑡𝑒 ), 𝑓 )]
 • SEvalFieldFailure:
              𝑉 [𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′ , _ | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, R | 𝐻 ] [𝑡 ↦→ 𝐻 (𝑉 (𝑡𝑒 ), 𝑓 )]
Lemma 24. If 𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, _ then 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
    Proof. By induction on 𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, _:
    Case 1. SEvalLiteral – 𝜎 ⊢ 𝑙 ⇓ _ ⊣ 𝜎, _; SEvalVar – 𝜎 ⊢ 𝑥 ⇓ _ ⊣ 𝜎, _: Trivial since 𝑔(𝜎) =⇒
𝑔(𝜎).
    Case 2. SEvalOrA – 𝜎 ⊢ 𝑒 1 ∨ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′ , _: By SEvalOrA 𝜎 ⊢ 𝑒 1 ⇓ _ ⊣ 𝜎 ′ , _, thus by induction
𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎). Therefore 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ) ∧ 𝑡 1 =⇒ 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
    Case 3. SEvalOrB – 𝜎 ⊢ 𝑒 1 ∨ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′ , _: By SEvalOrB 𝜎 ⊢ 𝑒 1 ⇓ _ ⊣ 𝜎 ′ , _ and 𝜎 ′ ⊢ 𝑒 2 ⇓ _ ⊣
𝜎 , _, thus by induction 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎). Therefore 𝑔(𝜎 ′′′ ) = 𝑔(𝜎 ′′ ) && ! 𝑡 1 =⇒
  ′′

𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎).
    Case 4. SEvalAndA – 𝜎 ⊢ 𝑒 1 ∧ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′ , _: Similar to case 2.
    Case 5. SEvalAndB – 𝜎 ⊢ 𝑒 1 ∧ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′ , _: Similar to case 3.
    Case 6. SEvalOp – 𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′ , _; SEvalNeg – 𝜎 ⊢ ! 𝑒 ⇓ _ ⊣ 𝜎 ′, _; SEvalField,
SEvalFieldOptimistic – 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′ , _; SEvalFieldImprecise – 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′′ , _: By
induction.
                                                                                                        
Lemma 25. If 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R then 𝜄 (𝜎 ′ ) = 𝜄 (𝜎), H(𝜎 ′ ) = H(𝜎), and 𝛾 (𝜎 ′ ) = 𝛾 (𝜎).
   Proof. Trivial by induction on 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R.                                                                
Lemma 26. Let 𝑉 be some initial valuation and h𝐻, 𝛼, 𝜌i be some well-formed evaluation state
such that h𝐻, 𝛼, 𝜌i 𝑉 𝜎.
  If 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R, h𝐻, 𝛼i ⊢𝑉 ′ R, and 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ ⊇ 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R | 𝐻 ],
then
                    h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ , h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡), and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.
   Proof. By induction on 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R:
   Case 1. SEvalLiteral – 𝜎 ⊢ 𝑙 ⇓ 𝑙 ⊣ 𝜎, ∅: Then 𝑉 ′ = 𝑉 , thus h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 by assumption.
   By EvalLiteral h𝐻, 𝜌i ⊢ 𝑙 ⇓ 𝑙, and by deﬁnition 𝑉 ′ (𝑙) = 𝑙.
   By FrameLiteral h𝐻, 𝛼, 𝜌i ⊢frm 𝑙.
   Case 2. SEvalVar – 𝜎 ⊢ 𝑥 ⇓ 𝛾 (𝜎) (𝑥) ⊣ 𝜎, ∅: Then 𝑉 ′ = 𝑉 , thus h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 by assumption.
   By EvalVar h𝐻, 𝜌i ⊢ 𝑥 ⇓ 𝜌 (𝑥), and 𝜌 (𝑥) = 𝑉 ′ (𝛾 (𝜎) (𝑥)) since 𝜌 𝑉 ′ 𝛾 (𝜎).
   By FrameVar h𝐻, 𝛼, 𝜌i ⊢frm 𝑥.
   Case 3. SEvalOrA – 𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′ , R:
   By SEvalOrA 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R.
Sound Gradual Verification with Symbolic Execution                                                             111:61


    Suppose h𝐻, 𝛼i ⊢𝑉 ′ R and 𝑉 ′ (𝑔(𝜎 ′′ )) = true. Then 𝑉 ′ (𝑔(𝜎 ′ )) = true since 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ) &&
𝑡 1 =⇒ 𝑔(𝜎 ′ ) by SEvalOrA. Then by induction h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ .
    Now h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′′ since 𝜎 ′′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡 1 ] by SEvalOrA and 𝑉 ′ (𝑔(𝜎 ′′ )) = true by
assumption.
    By induction h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ). But now 𝑉 ′ (𝑡 1 ) = true since 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ) && 𝑡 1 =⇒ 𝑡 1 .
Thus h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true.
    Then by EvalOrA h𝐻, 𝜌i ⊢ 𝑒 1 || 𝑒 2 ⇓ true and 𝑉 ′ (𝑡 1 ) = true.
    By induction h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 . Thus h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2 by FrameOrA since h𝐻, 𝜌i ⊢ 𝑒 1 ⇓
true.
    Case 4. SEvalOrB – 𝜎 ⊢ 𝑒 1 ∨ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 1 ∪ R 2 :
    By SEvalOrB 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, R 1 and 𝜎ˆ ′ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 2 , where 𝜎ˆ ′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡 1 ].
    Now suppose h𝐻, 𝛼i ⊢𝑉 ′ R 1 ∪ R 2 and 𝑉 ′ (𝑔(𝜎 ′′ )) = true. By lemma 23 h𝐻, 𝛼i ⊢𝑉 ′ R 1 (thus
h𝐻, 𝛼i ⊢𝑉 ′ R 1 ) and h𝐻, 𝛼i ⊢𝑉 ′ R 2 .
    Also, by lemma 24, 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎ˆ ′ ) = 𝑔(𝜎 ′ ) && ! 𝑡 1 =⇒ 𝑔(𝜎 ′ ). Therefore 𝑉 ′ (𝑔(𝜎 ′ )) =
𝑉 (𝑔(𝜎 ′ )) = true, and 𝑉 ′ (𝑔(𝜎 ′′ )) = true by assumption.
  ′

    Now by induction h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ . Also 𝑉 ′ (𝑔(𝜎ˆ ′ )) = true since 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ). Therefore
h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎ˆ ′ . Then also by induction h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′′ .
    By induction h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ) and h𝐻, 𝜌i ⊢ 𝑒 2 ⇓ 𝑉 ′ (𝑡 2 ). But now 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎ˆ ′ ) =
𝑔(𝜎 ′ ) && ! 𝑡 1 =⇒ ! 𝑡 1 , thus 𝑉 ′ (𝑡 1 ) = false. Therefore h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false.
    Thus h𝐻, 𝜌i ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑉 ′ (𝑡 2 ) by EvalOrB.
    By induction h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2 . Thus h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2 by FrameOrB
since h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false.
    Case 5. SEvalAndA – 𝜎 ⊢ 𝑒 1 ∧ 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′ , R: Similar to case 3.
    Case 6. SEvalAndB – 𝜎 ⊢ 𝑒 1 ∧ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 1 ∪ R 2 : Similar to case 4.
    Case 7. SEvalOp – 𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑡 1 ⊕ 𝑡 2 ⊣ 𝜎 ′′ , R 1 ∪ R 2 :
    By SEvalOp 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′ , R 1 and 𝜎 ′ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , R 2 .
    Now suppose h𝐻, 𝛼i ⊢𝑉 ′ R 1 ∪ R 2 and 𝑉 ′ (𝑔(𝜎 ′′ )) = true. By lemma 23 h𝐻, 𝛼i ⊢𝑉 ′ R 1 and
h𝐻, 𝛼i ⊢𝑉 ′ R 2 .
    Also, by lemma 24, 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ). Therefore𝑉 ′ (𝑔(𝜎 ′ )) = 𝑉 ′ (𝑔(𝜎 ′ )) = true, and 𝑉 ′ (𝑔(𝜎 ′′ )) =
true by assumption.
    Now by induction h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ , and then also by induction h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′′ .
    By induction h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ) and h𝐻, 𝜌i ⊢ 𝑒 2 ⇓ 𝑉 ′ (𝑡 2 ). Therefore h𝐻, 𝜌i ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓
𝑉 (𝑡 1 ) ⊕ 𝑉 ′ (𝑡 2 ) and 𝑉 ′ (𝑡 1 ) ⊕ 𝑉 ′ (𝑡 2 ) = 𝑉 ′ (𝑡 1 ⊕ 𝑡 2 ).
  ′

    By induction h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2 . Thus h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 ⊕ 𝑒 2 by FrameOp.
    Case 8. SEvalNeg – 𝜎 ⊢ ! 𝑒 ⇓ ! 𝑡 ⊣ 𝜎 ′ , R:
    By SEvalNeg 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R.
    Suppose that h𝐻, 𝛼i ⊢𝑉 ′ R and 𝑉 ′ (𝑔(𝜎 ′ )) = true.
    Now h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ by induction.
    Also by induction h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡). Thus h𝐻, 𝜌i ⊢ ! 𝑒 ⇓ ¬𝑉 ′ (𝑡) by EvalNeg and 𝑉 ′ (! 𝑡) =
¬𝑉 ′ (𝑡).
    By induction h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, and thus h𝐻, 𝛼, 𝜌i ⊢frm ! 𝑒 by FrameNeg.
    Case 9. SEvalField: 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, R
    By SEvalField 𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′ , R.
    Suppose that h𝐻, 𝛼i ⊢𝑉 ′ R and 𝑉 ′ (𝑔(𝜎 ′ )) = true.
    Then h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ by induction.
111:62                                                                    C. Zimmerman, J. DiVincenzo, and J. Aldrich


    Also by induction h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ). By SEvalField 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒 == 𝑡𝑒′ , therefore 𝑉 ′ (𝑡𝑒 ) =
𝑉 (𝑡𝑒′ ). Also by SEvalField h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎 ′ ). Therefore 𝑉 ′ (𝑡) = 𝐻 (𝑉 ′ (𝑡𝑒′ ), 𝑓 ) = 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) since
  ′

h𝐻, 𝜌, 𝛼i 𝑉 ′ 𝜎 ′ .
    Thus h𝐻, 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) by EvalField and 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) = 𝑉𝜎 ′ (𝑡).
    By induction h𝐻, 𝛼, 𝜌i ⊢frm 𝑒. Also, since h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎 ′ ) and h𝐻, 𝜌, 𝛼i 𝑉 ′ 𝜎 ′ , h𝑉 ′ (𝑡𝑒′ ), 𝑓 i =
h𝑉 ′ (𝑡𝑒 ), 𝑓 i ∈ 𝛼. By AssertAcc, h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ) since h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ). Thus by FrameField
h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.𝑓 .
   Case 10. SEvalFieldOptimistic – 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′ , R: Similar to case 9.
   Case 11. SEvalFieldImprecise – 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′, R; h𝑡𝑒 , 𝑓 i:
   By SEvalFieldImprecise 𝜎 ⊢ 𝑒 ⇓ 𝑡𝑒 ⊣ 𝜎 ′, R, 𝑡 = fresh, and 𝜎 ′′ = 𝜎 ′ [H = H (𝜎 ′ ); h𝑓 , 𝑡𝑒 , 𝑡i].
   Suppose h𝐻, 𝛼i ⊢𝑉 ′ R; h𝑡𝑒 , 𝑓 i and 𝑉 ′ (𝑔(𝜎 ′′ )) = true, thus h𝐻, 𝛼i ⊢𝑉 ′ R by lemma 23. Then
𝑉 (𝑔(𝜎 ′′ )) = 𝑉 ′ (𝑔(𝜎 ′ )) = true.
 ′

   Then by induction h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ , thus h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ .
   By lemma 23 h𝐻, 𝛼i ⊢𝑉 ′ {h𝑡𝑒 , 𝑓 i} and thus h𝐻, 𝛼i ⊢𝑉 ′ h𝑡𝑒 , 𝑓 i. Then by CheckAcc h𝑉 ′ (𝑡𝑒 ), 𝑓 i ∈
𝛼.
   By deﬁnition 35 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) = 𝑉 ′ (𝑡), and also h𝑉 ′ (𝑡𝑒 ), 𝑓 i ∈ 𝛼 and h𝐻, 𝛼i 𝑉 ′ H (𝜎 ′ ), thus
h𝐻, 𝛼i 𝑉 ′ H (𝜎 ′ ); h𝑓 , 𝑡𝑒 , 𝑡i.
  Then h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′′ since 𝜎 ′ and 𝜎 ′′ diﬀer only in their H components and H (𝜎 ′′ ) =
H (𝜎 ′ ); h𝑓 , 𝑡𝑒 , 𝑡i.
  By induction h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ). As shown before, 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) = 𝑉 ′ (𝑡). Thus by EvalField
h𝐻, 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝑉 ′ (𝑡).
  By induction h𝐻, 𝛼, 𝜌i ⊢frm 𝑒. Also, as shown before, h𝑉 ′ (𝑡𝑒 ), 𝑓 i ∈ 𝛼. By AssertAcc, h𝐻, 𝛼, 𝜌i 
acc(𝑒.𝑓 ) since h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ). Thus by FrameField h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.𝑓 .
  Case 12. SEvalFieldFailure – 𝜎 ⊢ 𝑒.𝑓 ⇓ 𝑡 ⊣ 𝜎 ′ , {⊥}:
  h𝐻, 𝛼i ⊢𝑉 {⊥} cannot hold. Since the assumptions cannot be satisﬁed, the statement holds
vacuously.
                                                                                                     

Lemma 27 (Progress). If 𝑉 is some initial valuation and 𝑉 (𝑔(𝜎)) = true, then for some 𝜎 ′ , 𝑡, and
R,
                           𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R and 𝑉 ′ (𝑔(𝜎 ′ )) = true
where 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻 ] for some 𝐻 .
  Proof. By induction on 𝑒:
  Case 1. 𝑙 ∈ Literal: By SEvalLiteral 𝜎 ⊢ 𝑙 ⇓ _ ⊣ 𝜎, _. Then 𝑉 ′ (𝑔(𝜎)) = true by assumptions.
  Case 2. 𝑥 ∈ Var: By SEvalVar 𝜎 ⊢ 𝑥 ⇓ _ ⊣ 𝜎, _. Then 𝑉 ′ (𝑔(𝜎)) = true by assumptions.
  Case 3. 𝑒.𝑓 where 𝑒 ∈ Expr, 𝑓 ∈ Field: By induction, 𝑒 ⊢ 𝑡𝑒 ⇓ 𝜎 ⊣ R, and 𝑉 ′ (𝑔(𝜎 ′ )) = true
where 𝑉 ′ is the corresponding
                                     valuation. Then
                                                      one of the following must apply:
  Case 3(a). If ∃ 𝑡𝑒′ , 𝑡 : 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒 ∧ h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎 ′ ), then SEvalField applies and thus
𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′ , _. Let 𝜎 ′′ = 𝜎 ′ .                           
  Case 3(b). Otherwise,  𝑡𝑒′ , 𝑡 : 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒 ∧ h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎 ′ ). Then, if ∃ 𝑡𝑒′ , 𝑡 :
 ′                     
 𝑔(𝜎 ) =⇒ 𝑡𝑒′ ==𝑡𝑒 ∧h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H (𝜎 ′ ), SEvalFieldOptimistic applies and thus 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′ , _.
Let 𝜎 ′′ = 𝜎 ′ .                                            
  Case 3(c). Otherwise,  𝑡𝑒′ , 𝑡 : 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒 ∧ h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎 ′ ) ∪ H (𝜎 ′ ). Then if 𝜄 (𝜎 ′ ),
SEvalFieldImprecise applies. In this case, 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′′ , _ where
                                                                             𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ).
  Case 3(d). Otherwise, ¬𝜄 (𝜎 ) and  𝑡𝑒 , 𝑡 : 𝑔(𝜎 ) =⇒ 𝑡𝑒 ==𝑡𝑒 ∧ h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎 ′ ) ∪ H (𝜎 ′ ). Thus
                                   ′         ′        ′          ′

SEvalFieldFailure applies and thus 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′, _. Let 𝜎 ′′ = 𝜎 ′ .
Sound Gradual Verification with Symbolic Execution                                                                  111:63


   In all of these subcases, 𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′′ , _ where 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ), and thus 𝑉 ′ (𝑔(𝜎 ′′ )) =
𝑉 ′ (𝑔(𝜎 ′ )) = true. By deﬁnition 35, in all of these subcases 𝑉 [𝜎 ⊢ 𝑒.𝑓 ⇓ _ ⊣ 𝜎 ′′ , _ | 𝐻 ] extends 𝑉 ′ .
    Case 4. 𝑒 1 ⊕ 𝑒 2 ; 𝑒 1, 𝑒 2 ∈ Expr: By induction 𝜎 ⊢ 𝑒 1 ⇓ _ ⊣ 𝜎 ′, _ for some 𝑒 1 , 𝜎 ′ where 𝑉 ′
is the corresponding valuation and 𝑉 ′ (𝑔(𝜎 ′ )) = true. Then by induction 𝜎 ′ ⊢ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′ ,
where 𝑉 ′′ is the corresponding valuation extending 𝑉 ′ and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true. Finally, by SEvalOp
𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′ , _. By deﬁnition 35, 𝑉 [𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ _ ⊣ 𝜎 ′′ , _ | 𝐻 ] extends 𝑉 ′′ .
    Case 5. 𝑒 1 || 𝑒 2 ; 𝑒 1, 𝑒 2 ∈ Expr: By induction 𝜎 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎 ′, _ for some 𝑒 1 , 𝑡𝑒 , 𝜎 ′ where 𝑉 ′ is the
corresponding valuation and 𝑉 ′ (𝑔(𝜎 ′ )) = true. Then one of the following cases must apply since
the program is well-typed:
    Case 5(a). 𝑉 ′ (𝑡 1 ) = true: Then by SEvalOrA, 𝜎 ⊢ 𝑒 1 ∨ 𝑒 2 ⇓ 𝑡 1 ⊣ 𝜎 ′′ , _ where 𝑔(𝜎 ′′ ) = 𝑔(𝜎 ′ ) && 𝑡 1 .
Let 𝑉 ′′ be the corresponding valuation. Now 𝑉 ′′ (𝑔(𝜎 ′′ )) = 𝑉 ′′ (𝑔(𝜎 ′ )) ∧ 𝑉 ′′ (𝑡 1 ) = true, which
completes the proof.
    Case 5(b). 𝑉 ′ (𝑡 1 ) = false: Let 𝜎ˆ ′ = 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && ! 𝑡 1 ]. Then 𝑉 ′ (𝑔(𝜎ˆ ′ )) = 𝑉 ′ (𝜎 ′ ) ∧ ¬𝑉 ′ (𝑡 1 ) =
true. By induction 𝜎ˆ ′ ⊢ 𝑒 2 ⇓ 𝑡 2 ⊣ 𝜎 ′′ , _ for some 𝑒 2 , 𝑡 2 , 𝜎 ′′ where 𝑉 ′′ is the corresponding valuation
and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true. Finally, by SEvalOrB, 𝜎 ⊢ 𝑒 1 || 𝑒 2 ⇓ _ ⊣ 𝜎 ′′ , _. By deﬁnition 35 𝑉 [𝜎 ⊢
𝑒 1 || 𝑒 2 ⇓ _ ⊣ 𝜎 ′′ , _ | 𝐻 ] extends 𝑉 ′′ .
    Case 6. 𝑒 1 && 𝑒 2 ; 𝑒 1, 𝑒 2 ∈ Expr: Similar to case 5.
    Case 7. ! 𝑒; 𝑒 ∈ Expr: By induction 𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, _ and 𝑉 ′ (𝜎 ′ ) = true where 𝑉 ′ is the
corresponding derivation. Then by SEvalNeg, 𝜎 ⊢ ! 𝑒 ⇓ _ ⊣ 𝜎 ′ , _ and the corresponding valuation
extends 𝑉 ′ by deﬁnition 35.
                                                                                                                          

D.3    Deterministic Evaluation
Deﬁnition 36. For a judgement 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ R, given an initial valuation 𝑉 and heap 𝐻 , the
corresponding valuation is denoted
                                               𝑉 [𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ R | 𝐻 ].
This valuation is deﬁned as follows, depending on the rule that proves the derivation.
   Note that the corresponding valuation always extends the initial valuation and is deﬁned for all
fresh symbolic values in the judgement.
 • SEvalPCLiteral:
                                             𝑉 [𝜎 ⊢ 𝑙 ↓ 𝑙 ⊣ ∅ | 𝐻 ] := 𝑉
 • SEvalPCVar:
                                        𝑉 [𝜎 ⊢ 𝑥 ↓ 𝛾 (𝜎) (𝑥) ⊣ ∅ | 𝐻 ] := 𝑉
 • SEvalPCOr:
                   𝑉 [𝜎 ⊢ 𝑒 1 || 𝑒 2 ↓ 𝑡 1 || 𝑡 2 ⊣ R 1 ∪ R 2 | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 1 ↓ 𝑡 1 ⊣ R 1 | 𝐻 ]
                                                                           [𝜎 ⊢ 𝑒 2 ↓ 𝑡 2 ⊣ R 2 | 𝐻 ]
 • SEValPCAnd:
                   𝑉 [𝜎 ⊢ 𝑒 1 && 𝑒 2 ↓ 𝑡 1 && 𝑡 2 ⊣ R 1 ∪ R 2 | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 1 ↓ 𝑡 1 ⊣ R 1 | 𝐻 ]
                                                                           [𝜎 ⊢ 𝑒 2 ↓ 𝑡 2 ⊣ R 2 | 𝐻 ]
 • SEvalPCOp:
                    𝑉 [𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ↓ 𝑡 1 ⊕ 𝑡 2 ⊣ R 1 ∪ R 2 | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 1 ↓ 𝑡 1 ⊣ R 1 | 𝐻 ]
                                                                           [𝜎 ⊢ 𝑒 2 ↓ 𝑡 2 ⊣ R 2 | 𝐻 ]
111:64                                                                     C. Zimmerman, J. DiVincenzo, and J. Aldrich


 • SEvalPCField or SEvalPCFieldOptimistic:
                               𝑉 [𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R | 𝐻 ]
 • SEvalPCFieldImprecise or SEvalPCFieldMissing:
                              𝑉 [𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R | 𝐻 ] := 𝑉 ′ [𝑡 ↦→ 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 )]
    where 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R | 𝐻 ].
Lemma 28 (Soundness). Suppose h𝐻, 𝛼, 𝜌i 𝑉 𝜎.
  If 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ R, 𝑉 ′ ⊇ 𝑉 [𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ R | 𝐻 ], and h𝐻, 𝛼i ⊢𝑉 ′ R, then
                                 h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡)      and    h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.
    Proof. By induction on 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ R:
    Case 1. SEvalPCLiteral – 𝜎 ⊢ 𝑙 ↓ 𝑙 ⊣ ∅:
    Then 𝑉 is the corresponding valuation. By EvalLiteral h𝐻, 𝜌i ⊢ 𝑙 ⇓ 𝑙 and by deﬁnition 𝑉 (𝑙) = 𝑙.
    By FrameLiteral h𝐻, 𝛼, 𝜌i ⊢frm 𝑙.
    Case 2. SEvalPCVar – 𝜎 ⊢ 𝑥 ↓ 𝛾 (𝜎) (𝑥) ⊣ ∅:
    Then 𝑉 is the corresponding valuation. Then h𝐻, 𝜌i ⊢ 𝑥 ⇓ 𝜌 (𝑥) by EvalLiteral, and 𝜌 (𝑥) =
𝑉 (𝛾 (𝜎) (𝑥)) since 𝜌 𝑉 𝛾 (𝜎).
    By FrameVar, h𝐻, 𝛼, 𝜌i ⊢frm 𝑥.
    Case 3. SEvalPCOr – 𝜎 ⊢ 𝑒 1 ∨ 𝑒 2 ↓ 𝑡 1 || 𝑡 2 ⊣ R 1 ∪ R 2 :
    By SEvalPCOr 𝜎 ⊢ 𝑒 1 ↓ 𝑡 1 ⊣ R 1 and 𝜎 ⊢ 𝑒 2 ↓ 𝑡 2 ⊣ R 2 . Let 𝑉1 and 𝑉2 be the respective corresponding
valuations, with 𝑉2 extending 𝑉1 and 𝑉1 extending 𝑉 . Then 𝑉2 is the corresponding valuation for
this case.
    Suppose that h𝐻, 𝛼i ⊢𝑉2 R 1 ∪ R 2 . Then h𝐻, 𝛼i ⊢𝑉1 R 1 and h𝐻, 𝛼i ⊢𝑉2 R 2 by lemma 23.
    Then one of the following cases applies, assuming a well-typed program:
    Case 3(a). 𝑉1 (𝑡 1 ) = true: Then h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true by induction, and then by EvalOrA h𝐻, 𝜌i ⊢
𝑒 1 || 𝑒 2 ⇓ true. Also, 𝑉2 (𝑡 1 || 𝑡 2 ) = (𝑉1 (𝑡 1 ) || 𝑉2 (𝑡 2 )) = true ∨ 𝑉2 (𝑡 2 ) = true. Therefore h𝐻, 𝜌i ⊢
𝑒 1 || 𝑒 2 ⇓ 𝑉2 (𝑡 1 || 𝑡 2 ).
    Also by induction h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 . Since h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true, by FrameOrA h𝐻, 𝛼, 𝜌i ⊢frm
𝑒 1 || 𝑒 2 .
    Case 3(b). 𝑉1 (𝑡 1 ) = false: Then h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false and h𝐻, 𝜌i ⊢ 𝑒 2 ⇓ 𝑉2 (𝑡 2 ) by induction. Thus
h𝐻, 𝜌i ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑉2 (𝑡 2 ) by EvalOrB. Also, 𝑉2 (𝑡 1 || 𝑡 2 ) = 𝑉1 (𝑡 1 ) ∨𝑉2 (𝑡 2 ) = false ∨𝑉2 (𝑡 2 ) = 𝑉2 (𝑡 2 ).
Therefore h𝐻, 𝜌i ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑉2 (𝑡 1 || 𝑡 2 ).
    Also by induction h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2 . Since h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false, by
FrameOrB h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2 .
    Case 4. SEvalPCAnd – 𝜎 ⊢ 𝑒 1 && 𝑒 2 ↓ 𝑡 1 && 𝑡 2 ⊣ R 1 ∪ R 2 : Similar to case 3.
    Case 5. SEvalPCOp – 𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ↓ 𝑡 1 ⊕ 𝑡 2 ⊣ R 1 ∪ R 2
    Use the same proof as in case 3 up to subcases.
    Then h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ 𝑉1 (𝑡 1 ) and h𝐻, 𝜌i ⊢ 𝑒 2 ⇓ 𝑉2 (𝑡 2 ) by induction. Thus h𝐻, 𝜌i ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓
𝑉1 (𝑡 1 ) ⊕ 𝑉2 (𝑡 2 ) by EvalOp. Also, 𝑉1 (𝑡 1 ) ⊕ 𝑉2 (𝑡 2 ) = 𝑉2 (𝑡 1 ⊕ 𝑡 2 ) by deﬁnition, therefore h𝐻, 𝜌i ⊢
𝑒 1 ⊕ 𝑒 2 ⇓ 𝑉2 (𝑡 1 ⊕ 𝑡 2 ).
    Also by induction h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2 . Therefore by FrameOp, h𝐻, 𝛼, 𝜌i ⊢frm
𝑒1 ⊕ 𝑒2 .
    Case 6. SEvalPCNeg – 𝜎 ⊢ ! 𝑒 ↓ ! 𝑡 ⊣ R:
    By SEvalPCNeg 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ R. Let 𝑉 ′ be the corresponding valuation, thus 𝑉 ′ is the correspond-
ing valuation for this case. Suppose that h𝐻, 𝛼i ⊢𝑉 ′ R.
    Then h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) by induction, and then h𝐻, 𝜌i ⊢ ! 𝑒 ⇓ ! 𝑉 ′ (𝑡) by EvalNeg. Also,
¬𝑉 ′ (𝑡) = 𝑉 ′ (! 𝑡) by deﬁnition. Therefore h𝐻, 𝜌i ⊢ ! 𝑒 ⇓ 𝑉 ′ (! 𝑡).
Sound Gradual Verification with Symbolic Execution                                                          111:65


   Also by induction h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, thus h𝐻, 𝛼, 𝜌i ⊢frm ! 𝑒 by FrameNeg.
    Case 7. SEvalPCField – 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R:
    By SEvalPCField 𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R. Let 𝑉 ′ be the corresponding valuation, thus 𝑉 ′ is the corre-
sponding valuation for this case. Suppose that h𝐻, 𝛼i ⊢𝑉 ′ R.
    By SEvalPCField 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒 , thus 𝑉 ′ (𝑡𝑒′ ) = 𝑉 ′ (𝑡𝑒 ). By induction h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 )
[= 𝑉 ′ (𝑡𝑒′ )]. Then by EvalField, h𝐻, 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝐻 (𝑉 ′ (𝑡𝑒′ ), 𝑓 ).
   Also by SEvalPCField h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎). Then 𝐻 (𝑉 ′ (𝑡𝑒′ ), 𝑓 ) = 𝑉 ′ (𝑡) since h𝐻, 𝛼i 𝑉 ′ H(𝜎).
Therefore h𝐻, 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝑉 ′ (𝑡).
   Also, h𝑉 ′ (𝑡𝑒′ ), 𝑓 i ∈ 𝛼 since h𝐻, 𝛼i 𝑉 ′ H(𝜎). Now h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ) by AssertAcc. By induc-
tion h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, therefore h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.𝑓 by FrameField.
    Case 8. SEvalPCFieldOptimistic – 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R: Same as case 7, replacing H with H .
    Case 9. SEvalPCFieldImprecise – 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R ∪ {acc(𝑡𝑒 .𝑓 )}:
    By SEvalPCFieldImprecise 𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R. Let 𝑉 ′ be the corresponding valuation for this case.
Suppose that h𝐻, 𝛼, 𝜌i 𝑉 𝜎 and h𝐻, 𝛼i ⊢𝑉 ′ R; h𝑡𝑒 , 𝑓 i.
    By lemma 23 h𝐻, 𝛼i ⊢𝑉 ′ R and h𝐻, 𝛼i ⊢𝑉 ′ {h𝑡𝑒 , 𝑓 i}.
    By SEvalPCFieldImprecise 𝑡 = fresh. Since h𝐻, 𝛼i ⊢𝑉 ′ h𝑡𝑒 , 𝑓 i, by CheckAcc h𝑉 ′ (𝑡𝑒 ), 𝑓 i ∈ 𝛼.
    By induction h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ), thus h𝐻, 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) by EvalField. But also
𝑉 ′ (𝑡) = 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ) by deﬁnition, therefore h𝐻, 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝑉 ′ (𝑡).
    Finally, h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ) and h𝑉 ′ (𝑡𝑒 ), 𝑓 i ∈ 𝛼, thus h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ) by AssertAcc. Also,
h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 by induction. Therefore h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.𝑓 by FrameField.
    Case 10. SEvalPCFieldMissing – 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R ∪ {⊥}:
    Let 𝑉 ′ be the corresponding valuation for this case. h𝐻, 𝛼i ⊢𝑉 ′ {⊥} cannot hold. Since the
conditions cannot be satisﬁed, the statement vacuously holds.
                                                                                                         

Lemma 29. Suppose that h𝐻, 𝛼, 𝜌i 𝑉 𝜎.
  If h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 and 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ then 𝑣 = 𝑉 ′ (𝑡), where 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ | 𝐻 ].
     Proof. By induction on 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _:
     Case 1. SEvalPCLiteral – 𝜎 ⊢ 𝑙 ↓ 𝑙 ⊣ ∅:
     Suppose h𝐻, 𝜌i ⊢ 𝑙 ⇓ 𝑣 for some 𝑣. By EvalLiteral 𝑣 = 𝑙, and by deﬁnition 𝑉 ′ (𝑙) = 𝑙.
     Case 2. SEvalPCVar – 𝜎 ⊢ 𝑥 ↓ 𝛾 (𝜎) (𝑥) ⊣ ∅:
     Suppose h𝐻, 𝜌i ⊢ 𝑥 ⇓ 𝑣 for some 𝑣. By EvalVar 𝑣 = 𝜌 (𝑥). Also 𝜌 (𝑥) = 𝑉 ′ (𝛾 (𝜎) (𝑥)) since
𝜌 𝑉 𝛾 (𝜎).
     Case 3. SEvalPCOr – 𝜎 ⊢ 𝑒 1 || 𝑒 2 ↓ 𝑡 1 || 𝑡 2 ⊣ R 1 ∪ R 2 :
     By SEvalPCOr 𝜎 ⊢ 𝑒 1 ↓ 𝑡 1 ⊣ R 1 and 𝜎 ⊢ 𝑒 2 ↓ 𝑡 2 ⊣ R 2 . Let 𝑉1 and 𝑉2 be the respective corresponding
valuations, with 𝑉2 extending 𝑉1 and 𝑉1 extending 𝑉 . Then 𝑉2 is the corresponding valuation for
this case.
     Suppose that h𝐻, 𝜌i ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑣. Then one of the following rules must be used:
     Case 3(a). EvalOrA – h𝐻, 𝜌i ⊢ 𝑒 1 || 𝑒 2 ⇓ true thus 𝑣 = true:
     Then 𝑣 = true. By EvalOrA h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true, thus by induction 𝑉1 (𝑡 1 ) = true. Also 𝑉2 (𝑡 1 ||
𝑡 2 ) = (𝑉1 (𝑡 1 ) ∨ 𝑉2 (𝑡 2 )) = true ∨ 𝑉 ′ (𝑡 2 ) = true. Therefore 𝑣 = 𝑉2 (𝑡 1 || 𝑡 2 ).
     Case 3(b). EvalOrB – h𝐻, 𝜌i ⊢ 𝑒 2 || 𝑒 2 ⇓ 𝑣 2 thus 𝑣 = 𝑣 2 :
     By EvalOrB h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false and h𝐻, 𝜌i ⊢ 𝑒 2 ⇓ 𝑣. Thus 𝑉1 (𝑡 1 ) = false and by 𝑉2 (𝑡 2 ) = 𝑣 2
by induction. Also, 𝑉2 (𝑡 1 || 𝑡 2 ) = 𝑉1 (𝑡 1 ) ∨ 𝑉2 (𝑡 2 ) = false ∨ 𝑣 2 = 𝑣 2 . Therefore 𝑣 = 𝑉2 (𝑡 1 || 𝑡 2 ).
     Case 4. SEvalPCAnd – 𝜎 ⊢ 𝑒 1 && 𝑒 2 ↓ 𝑡 1 && 𝑡 2 ⊣ R 1 ∪ R 2 : Similar to case 3.
     Case 5. SEvalPCOp – 𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ↓ 𝑡 1 ⊕ 𝑡 2 ⊣ R 1 ∪ R 2 : Follow the same proof as in case 3, up to
subcases.
111:66                                                                C. Zimmerman, J. DiVincenzo, and J. Aldrich


    Then by EvalOp 𝑣 = 𝑣 1 ⊕ 𝑣 2 for some 𝑣 1, 𝑣 2 such that h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ 𝑣 1 and h𝐻, 𝜌i ⊢ 𝑒 2 ⇓ 𝑣 2 . By
induction 𝑉1 (𝑡 1 ) = 𝑣 1 and 𝑉2 (𝑡 2 ) = 𝑣 2 . Also, 𝑉2 (𝑡 1 ⊕ 𝑡 2 ) = 𝑉1 (𝑡 1 ) ⊕ 𝑉2 (𝑡 2 ) = 𝑣 1 ⊕ 𝑣 2 = 𝑣.
    Case 6. SEvalPCNeg – 𝜎 ⊢ ! 𝑒 ↓ ! 𝑡 ⊣ R:
    By SEvalPCNeg 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ R. Let 𝑉 ′ be the corresponding valuation, thus 𝑉 ′ is the correspond-
ing valuation for this case.
    Suppose h𝐻, 𝜌i ⊢ ! 𝑒 ⇓ 𝑣 for some 𝑣. Then by EvalNeg 𝑣 = ¬𝑣 ′ where h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 ′ . By
induction 𝑣 ′ = 𝑉 ′ (𝑡) and therefore 𝑣 = ¬𝑣 ′ = ¬𝑉 ′ (𝑡) = 𝑉 ′ (! 𝑡).
    Case 7. SEvalPCField: 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R
    By SEvalPCField 𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R. Let 𝑉 ′ be the corresponding valuation, thus 𝑉 ′ is the corre-
sponding valuation for this case.
    Suppose h𝐻, 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝑣 for some 𝑣. Then by EvalField h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 𝑒 for some 𝑣 𝑒 . Therefore
𝑉 ′ (𝑡𝑒 ) = 𝑣 𝑒 by induction. By SEvalPCField 𝑔(𝜎 ′ ) =⇒ 𝑡𝑒′ == 𝑡𝑒 and thus 𝑣 𝑒 = 𝑉 ′ (𝑡𝑒 ) = 𝑉 ′ (𝑡𝑒′ ).
    Now by EvalField 𝑣 = 𝐻 (𝑣 𝑒 , 𝑓 ). Also, h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) by SEvalPCField. Therefore 𝐻 (𝑉 ′ (𝑡𝑒′ ), 𝑓 ) =
  ′
𝑉 (𝑡) since h𝐻, 𝛼i 𝑉 H(𝜎) and 𝑉 ′ extends 𝑉 . Finally, 𝑉 ′ (𝑡) = 𝐻 (𝑉 ′ (𝑡𝑒′ ), 𝑓 ) = 𝐻 (𝑣 𝑒 , 𝑓 ) = 𝑣.
    Case 8. SEvalPCFieldOptimistic: 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R
    Same as case 7, replacing H with H .
    Case 9. SEvalPCFieldImprecise – 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ R; h𝑡𝑒 , 𝑓 i:
    By SEvalPCFieldImprecise 𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R. Let 𝑉𝑒 be the corresponding valuation, and let 𝑉 ′ be
the corresponding valuation for this case, which extends 𝑉𝑒 .
    Suppose h𝐻, 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝑣 for some 𝑣. Then by EvalField h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 𝑒 for some 𝑣 𝑒 . Therefore
𝑉𝑒 (𝑡𝑒 ) = 𝑣 𝑒 by induction.
    Now by EvalField 𝑣 = 𝐻 (𝑣 𝑒 , 𝑓 ). By deﬁnition 36 𝑉 ′ (𝑡) = 𝐻 (𝑉𝑒 (𝑡𝑒 ), 𝑓 ) = 𝐻 (𝑣 𝑒 , 𝑓 ) = 𝑣.
    Case 10. SEvalPCFieldMissing – 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ {⊥}: Same as case 9.
                                                                                                               
Lemma 30. For any 𝜎, 𝑒, 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡.
   Proof. By induction on the syntax forms of 𝑒:
   Case 1. 𝑙 ∈ Literal
   Then 𝑙 ∈ SExpr and by SEvalPCLiteral, 𝜎 ⊢ 𝑙 ↓ 𝑙 ⊣ _.
   Case 2. 𝑥 ∈ Var:
   Since this is a well-formed program, all variables must be assigned before use. Therefore 𝛾 (𝜎) (𝑥)
must be deﬁned, and by SEvalPCVar, 𝜎 ⊢ 𝑒 ↓ 𝛾 (𝜎) (𝑥) ⊣ _.
   Case 3. 𝑒.𝑓 – 𝑒 ∈ Expr, 𝑓 ∈ Field:
   By induction, ∃ 𝑡𝑒 ∈ SExpr : 𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ _. Then one of the following must apply:
   Case 3(a). ∃ 𝑡𝑒′ : h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) ∧ 𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 : Then SEvalPCField applies and thus
𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ _.
   Case 3(b).  𝑡𝑒′ : h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) ∧ 𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 and ∃ 𝑡𝑒′ : h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H (𝜎) ∧ 𝑔(𝜎) =⇒
 ′
𝑡𝑒 == 𝑡𝑒 : Then SEvalPCFieldOptimistic applies and thus 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ _.
   Case 3(c).  𝑡𝑒′ : h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎)∪H (𝜎)∧𝑔(𝜎) =⇒ 𝑡𝑒′ ==𝑡𝑒 and 𝜄 (𝜎): Then SEvalPCFieldImprecise
applies and thus 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ _ where 𝑡 = fresh.
   Case 3(d).  𝑡𝑒′ : h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎)∪H (𝜎)∧𝑔(𝜎) =⇒ 𝑡𝑒′ ==𝑡𝑒 and ¬𝜄 (𝜎): Then SEvalPCFieldMissing
applies and thus 𝜎 ⊢ 𝑒.𝑓 ↓ 𝑡 ⊣ _ where 𝑡 = fresh.
   Case 4. 𝑒 1 ⊕ 𝑒 2 – 𝑒 1 , 𝑒 2 ∈ Expr:
   By induction, ∃ 𝑡 1 ∈ SExpr : 𝜎 ⊢ 𝑒 1 ↓ 𝑡 1 ⊣ _ and ∃ 𝑡 2 ∈ SExpr : 𝜎 ⊢ 𝑒 2 ↓ 𝑡 2 ⊣ _. Then, by
SEvalPCOp, 𝜎 ⊢ 𝑒 1 ⊕ 𝑒 2 ↓ 𝑡 1 ⊕ 𝑡 2 ⊣ _.
   Case 5. 𝑒 1 || 𝑒 2 – 𝑒 1 , 𝑒 2 ∈ Expr:
   By induction, ∃ 𝑡 1 ∈ SExpr : 𝜎 ⊢ 𝑒 1 ↓ 𝑡 1 ⊣ _ and ∃ 𝑡 2 ∈ SExpr : 𝜎 ⊢ 𝑒 2 ↓ 𝑡 2 ⊣ _. Then, by
SEvalPCOr, 𝜎 ⊢ 𝑒 1 || 𝑒 2 ↓ 𝑡 1 || 𝑡 2 ⊣ _.
Sound Gradual Verification with Symbolic Execution                                                   111:67


  Case 6. 𝑒 1 && 𝑒 2 – 𝑒 1 , 𝑒 2 ∈ Expr:
  By induction, ∃ 𝑡 1 ∈ SExpr : 𝜎 ⊢ 𝑒 1 ↓ 𝑡 1 ⊣ _ and ∃ 𝑡 2 ∈ SExpr : 𝜎 ⊢ 𝑒 2 ↓ 𝑡 2 ⊣ _. Then, by
SEvalPCAnd, 𝜎 ⊢ 𝑒 1 && 𝑒 2 ↓ 𝑡 1 && 𝑡 2 ⊣ _.
  Case 7. ! 𝑒 – 𝑒 ∈ Expr:
  By induction, ∃ 𝑡 ∈ SExpr : 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _. Then, by SEvalPCNeg, 𝜎 ⊢ ! 𝑒 ↓ ! 𝑡 ⊣ _.
                                                                                                

D.4 Produce
Deﬁnition 37. For a judgement 𝜎 ⊢ 𝜙˜ ⊳ 𝜎 ′ , given an initial valuation 𝑉 and heap 𝐻 , the corre-
sponding valuation is denoted
                                       𝑉 [𝜎 ⊢ 𝜙˜ ⊳ 𝜎 | 𝐻 ].
This valuation is deﬁned as follows, depending on the rule that proves the derivation. Values are
referenced using the respective name from the rule deﬁnition.
   Note that the corresponding valuation always extends the initial valuation and is deﬁned for all
fresh symbolic values in the judgement.
 • SProduceImprecise:
                           𝑉 [𝜎 ⊢ ? ∗ 𝜙 ⊳ 𝜎 ′ | 𝐻 ] := 𝑉 [𝜎 [𝜄 = ⊤] ⊢ 𝜙 ⊳ 𝜎 ′ | 𝐻 ]
 • SProduceExpr:
                                 𝑉 [𝜎 ⊢ 𝑒 ⊳ 𝜎 ′ | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ | 𝐻 ]
 • SProducePredicate:
                                 𝑉 [𝜎 ⊢ 𝑝 (𝑒) ⊳ 𝜎 ′ ] := 𝑉 [𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ | 𝐻 ]
 • SProduceField:
                       𝑉 [𝜎 ⊢ acc(𝑒.𝑓 ) ⊳ 𝜎 ′ | 𝐻 ] := 𝑉 ′ [𝑡 ↦→ 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 )]
   where 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ | 𝐻 ].
 • SProduceConjunction:
                   𝑉 [𝜎 ⊢ 𝜙 1 ∗ 𝜙 2 ⊳ 𝜎 ′′ | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝜙 1 ⊳ 𝜎 ′ | 𝐻 ] [𝜎 ′ ⊢ 𝜙 2 ⊳ 𝜎 ′′ | 𝐻 ]
 • SProduceIfA:
                         𝑉 [𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊳ 𝜎 ′ | 𝐻 ] :=
                            𝑉 [𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ | 𝐻 ] [𝜎 [𝑔 = 𝑔(𝜎) && 𝑡] ⊢ 𝜙 1 ⊳ 𝜎 ′ | 𝐻 ]
 • SProduceIfB:
                        𝑉 [𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊳ 𝜎 ′ | 𝐻 ] :=
                           𝑉 [𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ | 𝐻 ] [𝜎 [𝑔 = 𝑔(𝜎) && ! 𝑡] ⊢ 𝜙 2 ⊳ 𝜎 ′ | 𝐻 ]
Lemma 31. If 𝜎 ⊢ 𝜙 ⊳ 𝜎 ′ , then 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
    Proof. By induction on 𝜎 ⊢ 𝜙 ⊳ 𝜎 ′ :
    Case 1. SProduceImprecise – 𝜎 ⊢ ? ∗ 𝜙 ⊳ 𝜎 ′ : By SProduceImprecise 𝜎 [𝜄 = ⊤] ⊢ 𝜙 ⊳ 𝜎 ′ , thus by
induction 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
    Case 2. SProduceExpr – 𝜎 ⊢ 𝑒 ⊳ 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡]: Trivially 𝑔(𝜎) && 𝑡 =⇒ 𝑔(𝜎).
    Case 3. SProducePredicate – 𝜎 ⊢ 𝑝 (𝑒) ⊳ 𝜎 ′ : By SProducePredicate 𝜎 ′ = 𝜎 [H = · · · ], thus
𝑔(𝜎 ′ ) = 𝑔(𝜎).
    Case 4. SProduceField – 𝜎 ⊢ acc(𝑒.𝑓 ) ⊳ 𝜎 ′ : Similar to case 3.
    Case 5. SProduceConjunction – 𝜎 ⊢ 𝜙 1 ∗ 𝜙 2 ⊳ 𝜎 ′′ : By SProduceConjunction 𝜎 ⊢ 𝜙 1 ⊳ 𝜎 ′ and
𝜎 ⊢ 𝜙 2 ⊳ 𝜎 ′′ . By induction 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ) and 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎), therefore 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎).
  ′
111:68                                                                C. Zimmerman, J. DiVincenzo, and J. Aldrich


  Case 6. SProduceIfA – 𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊳ 𝜎 ′ : By SProduceIfA 𝜎 [𝑔 = 𝑔(𝜎) &&𝑡] ⊢ 𝜙 1 ⊳ 𝜎 ′ ,
thus by induction 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎) && 𝑡 =⇒ 𝑔(𝜎).
  Case 7. SProduceIfB – 𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊳ 𝜎 ′ : Similar to case 6.
                                                                                                    
Lemma 32. If 𝜎 ⊢ 𝜙˜ ⊳ 𝜎 ′ then 𝛾 (𝜎 ′ ) = 𝛾 (𝜎).
   Proof. Trivial by induction on 𝜎 ⊢ 𝜙˜ ⊳ 𝜎 ′ .                                                               
Lemma 33. Suppose h𝐻, 𝛼 \ T𝜙U     ˜ h𝐻, 𝜌 i , 𝜌i   𝜎.
                                                 𝑉
  If 𝜎 ⊢ 𝜙 ⊳ 𝜎 , h𝐻, 𝛼, 𝜌i  𝜙, and 𝑉 (𝑔(𝜎 )) = true where 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝜙˜ ⊳ 𝜎 ′ | 𝐻 ], then
          ˜   ′              ˜        ′        ′

                                             h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′

  Proof. By induction on 𝜎 ⊢ 𝜙˜ ⊳ 𝜎 ′ :
  Case 1. SProduceImprecise – 𝜎 ⊢ ? ∗ 𝜙 ⊳ 𝜎 ′ :
  By SProduceImprecise 𝜎 [𝜄 = ⊤] ⊢ 𝜙 ⊳ 𝜎 ′ . Let 𝑉 ′ be the corresponding valuation, thus 𝑉 ′ is the
corresponding valuation for this case.
  Then, since h𝐻, 𝛼, 𝜌i  ? ∗ 𝜙, by AssertImprecise h𝐻, 𝛼, 𝜌i  𝜙. Also, T? ∗ 𝜙U h𝐻, 𝜌 i = T𝜙U h𝐻, 𝜌 i .
Therefore h𝐻, 𝛼 \ T𝜙U h𝐻, 𝜌 i , 𝜌i 𝑉 𝜎, and furthermore h𝐻, 𝛼 \ T𝜙U h𝐻, 𝜌 i , 𝜌i 𝑉 𝜎 [𝜄 = ⊤].
  Therefore h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ by induction.
  Case 2. SProduceExpr – 𝜎 ⊢ 𝑒 ⊳ 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡]:
  By SProduceExpr 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _. Let 𝑉 ′ be the corresponding valuation, therefore 𝑉 ′ is the
corresponding valuation for this case.
  Let 𝜎 ′ = 𝜎 [𝑔(𝜎) ∧ 𝑡]. Since 𝑉 ′ extends 𝑉 and h𝐻, 𝛼 \ T𝑒U h𝐻, 𝜌 i , 𝜌i 𝑉 𝜎, h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎. Then,
since 𝜎 ′ and 𝜎 diﬀer only in their 𝑔 components h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ since 𝑉 ′ (𝑔(𝜎 ′ )) = true by
assumptions.
   Case 3. SProducePredicate – 𝜎 ⊢ 𝑝 (𝑒) ⊳ 𝜎 ′ :
   By SProducePredicate, for each 𝑒, 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡𝑖 . Let 𝑉 ′ be the corresponding valuation
for this case, thus 𝑉 ′ extends the corresponding valuation corresponding for each 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _.
   By SProducePredicate 𝜎 ′ = 𝜎 [H = H(𝜎); h𝑝, 𝑡 i]. Since 𝜎 and 𝜎 ′ diﬀer only in their H compo-
nents, proving that (1) holds for H(𝜎 ′ ) is suﬃcient to prove that h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ .
   By assumptions, h𝐻, 𝛼, 𝜌i  𝑝 (𝑒) thus by AssertPredicate h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 for some 𝑣 for all 𝑒.
Then by lemma 29 h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) for all 𝑒. Then
                     T𝑝 (𝑒)U h𝐻, 𝜌 i ⊇ Tpredicate(𝑝)U h𝐻, 𝑥↦→𝑉 ′ (𝑡 ) i = 𝑉 ′ Lh𝑝, 𝑡iM𝐻 ,

where 𝑥 = predicate_params(𝑝) thus h𝐻, 𝛼 \ 𝑉 Lh𝑝, 𝑡iM𝐻 i 𝑉 H(𝜎) by lemma 19. Now by lemma
15 and since 𝑉 ′ extends 𝑉 ,
                               ∀ℎ ∈ H(𝜎) : 𝑉 ′ LℎM𝐻 ∩ 𝑉 ′ Lh𝑝, 𝑡iM𝐻 = ∅.
Since h𝑝, 𝑡i is the only addition to H(𝜎 ′ ) relative to H(𝜎) and 𝑉 ′ extends 𝑉 ,
                      ∀ℎ 1 , ℎ 2 ∈ H(𝜎 ′ ) : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 ′ Lℎ 1 M𝐻 ∩ 𝑉 ′ Lℎ 2 M𝐻 = ∅.
Also by AssertPredicate h𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]i  predicate(𝑝). Therefore, since h𝑝, 𝑡 i is the only
addition to H(𝜎 ′ ) relative to H(𝜎) and 𝑉 ′ extends 𝑉 ,
                       ∀ h𝑝, 𝑡 i ∈ H(𝜎 ′ ) : h𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]i  predicate(𝑝).
Therefore all requirements for (1) are satisﬁed, and therefore h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ .
  Case 4. SProduceField – 𝜎 ⊢ acc(𝑒.𝑓 ) ⊳ 𝜎 ′ :
Sound Gradual Verification with Symbolic Execution                                                              111:69


    By SProduceField 𝜎 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ _ for some 𝑡𝑒 . Let 𝑉𝑒 be the corresponding valuation, and let 𝑉 ′
be the corresponding valuation for this case, thus 𝑉 ′ extends 𝑉𝑒 .
    Also by SProduceField 𝜎 ′ = 𝜎 [H = H(𝜎); h𝑓 , 𝑡𝑒 , 𝑡i] where 𝑡 = fresh. By deﬁnition 𝑉 ′ (𝑡) =
𝐻 (𝑉𝑒 (𝑡𝑒 ), 𝑓 ).
    Since 𝜎 and 𝜎 ′ diﬀer only in their H components, proving that (1) holds for H(𝜎 ′ ) is suﬃcient
to prove that h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ .
    By assumptions h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ), thus by AssertAcc h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 𝑒 for some 𝑣 𝑒 such that
h𝑣 𝑒 , 𝑓 i ∈ 𝛼. By lemma 29 𝑣 𝑒 = 𝑉𝑒 (𝑡𝑒 ), thus h𝑉 ′ (𝑡𝑒 ), 𝑓 i ∈ 𝛼.
    As shown before, 𝑉 ′ (𝑡) = 𝐻 (𝑉 ′ (𝑡𝑒 ), 𝑓 ). Therefore, since h𝑓 , 𝑡𝑒 , 𝑡i is the only addition to H(𝜎 ′ )
relative to H(𝜎) and 𝑉 ′ extends 𝑉 ,
                               ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎 ′ ) : 𝐻 (𝑉 ′ (𝑡), 𝑓 ) = 𝑉 ′ (𝑡 ′ ) and
                                     ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎 ′ ) : h𝑉 ′ (𝑡), 𝑓 i ∈ 𝛼
Since h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) as shown before,
                                  T𝑒U h𝐻, 𝜌 i ⊇ {h𝑉 ′ (𝑡𝑒 ), 𝑓 i} = 𝑉 L(𝑡𝑒 .𝑓 ; 𝑡)M𝐻 .
Therefore h𝐻, 𝛼 \ 𝑉 ′ L(𝑡 .𝑓 ; 𝑡 ′ )M𝐻 i 𝑉 H(𝜎) by lemma 19. Now by lemma 15, and since 𝑉 ′ extends
𝑉,
                                 ∀ℎ ∈ H(𝜎 ′ ) : 𝑉 ′ LℎM𝐻 ∩ 𝑉 ′ Lh𝑓 , 𝑡𝑒 , 𝑡iM𝐻 = ∅.
Finally, since h𝑓 , 𝑡𝑒 , 𝑡i is the only addition to H(𝜎 ′ ) relative to H(𝜎) and 𝑉 ′ extends 𝑉 ,
                         ∀ℎ 1 , ℎ 2 ∈ H(𝜎 ′ ) 2 : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 ′ Lℎ 1 M𝐻 ∩ 𝑉 ′ Lℎ 2 M𝐻 = ∅.
Therefore all requirements for (1) are satisﬁed and therefore h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ .
   Case 5. SProduceConjunction – 𝜎 ⊢ 𝜙 1 ∗ 𝜙 2 ⊳ 𝜎 ′′ :
   By SProduceConjunction 𝜎 ⊢ 𝜙 1 ⊳ 𝜎 ′ and 𝜎 ′ ⊢ 𝜙 2 ⊳ 𝜎 ′′ . Let 𝑉1 and 𝑉2 be the respective corre-
sponding valuations, extending 𝑉 and 𝑉1 , respectively. Then 𝑉2 is the corresponding valuation for
this case.
   Since h𝐻, 𝛼, 𝜌i  𝜙 1 ∗ 𝜙 2 , by AssertConjunction h𝐻, 𝛼, 𝜌i  𝜙 1 and h𝐻, 𝛼, 𝜌i  𝜙 2 where
T𝜙 1 U h𝐻, 𝜌 i ∩ T𝜙 2 U h𝐻, 𝜌 i = ∅. Also, T𝜙 1 ∗ 𝜙 2 U h𝐻, 𝜌 i = T𝜙 1 U h𝐻, 𝜌 i ∪ T𝜙 2 U h𝐻, 𝜌 i .
   Let 𝛼 ′ = 𝛼 \ T𝜙 2 U h𝐻, 𝜌 i . Then h𝐻, 𝛼 ′ , 𝜌i  𝜙 1 by lemma 12 since T𝜙 1 U h𝐻, 𝜌 i ⊆ 𝛼 ′ . Also, h𝐻, 𝛼 ′ \
T𝜙 1 U h𝐻, 𝜌 i , 𝜌i 𝑉 𝜎 since 𝛼 ′ \T𝜙 1 U h𝐻, 𝜌 i = 𝛼 \T𝜙 1 ∗𝜙 2 U h𝐻, 𝜌 i . Finally, by lemma 31, 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ),
and therefore 𝑉2 (𝑔(𝜎 ′ )) = 𝑉1 (𝑔(𝜎 ′ )) = true.
   Now h𝐻, 𝛼 ′ , 𝜌i 𝑉 𝜎 ′ by induction. Also, h𝐻, 𝛼, 𝜌i  𝜙 2 by lemma 12 since T𝜙 2 U h𝐻, 𝜌 i ⊆ 𝛼.
                         1
Finally, 𝑉2 (𝑔(𝜎 ′′ )) = true by assumption, therefore h𝐻, 𝛼, 𝜌i 𝑉 𝜎 ′′ by induction.
                                                                       2
   Case 6. SProduceIfA – 𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊳ 𝜎 ′ :
   By SProduceIfA 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ and 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡] ⊢ 𝜙 1 ⊳ 𝜎 ′ . Let 𝑉1 and 𝑉 ′ be the respective
corresponding valuations extending 𝑉 and 𝑉1 , respectively. Then 𝑉 ′ is the corresponding valuation
in this case.
   By lemma 31, 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎) && 𝑡. By assumptions 𝑉 ′ (𝑔(𝜎 ′ )) = true, thus 𝑉 ′ (𝑔(𝜎) && 𝑡) =
𝑉1 (𝑔(𝜎) && 𝑡) = true.
   Then also 𝑉1 (𝑡) = true. Since h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 , h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 for some 𝑣 by
AssertIfA or AssertIfB. But by lemma 29 𝑣 = 𝑉1 (𝑡) = true. Therefore
T𝜙 1 U h𝐻, 𝜌 i ⊆ Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i by deﬁnition. Therefore, since 𝑉1 extends 𝑉 ,
                                 h𝐻, 𝛼 \ T𝜙 1 U h𝐻, 𝜌 i , 𝜌i 𝑉 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡].
                                                                1

Also, h𝐻, 𝛼, 𝜌i  𝜙 1 by AssertIfA since h𝐻, 𝜌i ⊢ 𝑒 ⇓ true and h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 .
Finally, 𝑉 ′ (𝜎 ′ ) = true by assumption.
111:70                                                             C. Zimmerman, J. DiVincenzo, and J. Aldrich


     Thus h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ by induction.
     Case 7. SProduceIfB: Similar to case 6.
                                                                                                            

Lemma 34 (Progress). If 𝑉 (𝑔(𝜎)) = true, h𝐻, 𝛼, 𝜌i  𝜙,      ˜ and h𝐻, 𝛼, 𝜌i   𝜎, then 𝜎 ⊢ 𝜙˜ ⊳ 𝜎 ′ for
                                                                             𝑉
some 𝜎 ′ where 𝑉 ′ (𝑔(𝜎 ′ )) = true and 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝜙˜ ⊳ 𝜎 ′ | 𝐻 ].
     Proof. Suppose 𝑉 (𝑔(𝜎)) = true and complete the proof by induction on the syntax forms of
˜
𝜙:
   Case 1. ? ∗ 𝜙 – 𝜙 ∈ Formula:
   Let 𝜎ˆ = 𝜎 [𝜄 = ⊤]. Then 𝑉 (𝑔(𝜎))        ˆ = 𝑉 (𝑔(𝜎)) = true. Also, since h𝐻, 𝛼, 𝜌i  ? ∗ 𝜙, by
AssertImprecise h𝐻, 𝛼, 𝜌i  𝜙. Thus by induction 𝜎ˆ ⊢ 𝜙 ⊳ 𝜎 ′ for some 𝜎 ′ where 𝑉 ′ (𝑔(𝜎 ′ )) = true.
Then 𝜎 ⊢ ? ∗ 𝜙 ⊳ 𝜎 ′ by SProduceImprecise, and 𝑉 ′ (𝑔(𝜎 ′ )) = true.
   Case 2. 𝜙 1 ∗ 𝜙 2 – 𝜙 1, 𝜙 2 ∈ Formula:
   Since h𝐻, 𝛼, 𝜌i  𝜙 1 ∗ 𝜙 2 , h𝐻, 𝛼, 𝜌i  𝜙 1 and h𝐻, 𝛼, 𝜌i  𝜙 2 by AssertConjunction and lemma
9.
   By induction 𝜎 ⊢ 𝜙 1 ⊳ 𝜎 ′ , with corresponding valuation 𝑉 ′ where 𝑉 ′ (𝑔(𝜎 ′ )) = true. Then by
induction 𝜎 ′ ⊢ 𝜙 2 ⊳ 𝜎 ′′ , with corresponding valuation 𝑉 ′′ , for some 𝜎 ′′ where 𝑉 ′′ (𝑔(𝜎 ′′ )) = true.
By SProduceConjunction, 𝜎 ⊢ 𝜙 1 ∗ 𝜙 2 ⊳ 𝜎 ′′ , and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true.
   Case 3. 𝑝 (𝑒) – 𝑝 ∈ Predicate, 𝑒 ∈ Expr:
   For each 𝑒, by lemma 30, 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡 ∈ SExpr. Let 𝜎 ′ = 𝜎 [H = H(𝜎); h𝑝, 𝑡i], then
by SProducePredicate, 𝜎 ⊢ 𝑝 (𝑒) ⊳ 𝜎 ′ . Finally, letting 𝑉 ′ be the corresponding valuation extending
𝑉 , 𝑉 ′ (𝑔(𝜎 ′ )) = 𝑉 (𝑔(𝜎)) = true.
   Case 4. 𝑒 ∈ Expr:
   By lemma 30, 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡 ∈ SExpr. Let 𝑉1 be the corresponding valuation and
𝜎 ′ = 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡]. Then by SProduceExpr 𝜎 ⊢ 𝑒 ⊳ 𝜎 ′ . Let 𝑉 ′ be the corresponding valuation
extending 𝑉 , thus 𝑉 ′ extends 𝑉1 .
   Since h𝐻, 𝛼, 𝜌i  𝑒, h𝐻, 𝜌i ⊢ 𝑒 ⇓ true by AssertValue and thus 𝑉 ′ (𝑡) = true by lemma 29.
Finally, 𝑉 ′ (𝜎 ′ ) = 𝑉 ′ (𝜎) ∧ 𝑉 ′ (𝑡) = 𝑉 (𝜎) ∧ true = true.
   Case 5. if 𝑒 then 𝜙 1 else 𝜙 2 – 𝑒 ∈ Expr, 𝜙 1, 𝜙 2 ∈ Formula:
   By lemma 30, 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡 ∈ SExpr. Let 𝑉1 be the valuation corresponding to this
derivation.
   Then one of the following rules must apply to produce h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 :
   Case 5(a). AssertIfA:
   Then h𝐻, 𝜌i ⊢ 𝑒 ⇓ true. Then 𝑉1 (𝑡) = true by lemma 29 and therefore 𝑉1 (𝑔(𝜎) && 𝑡) = true.
Also, h𝐻, 𝛼, 𝜌i  𝜙 1 by AssertIfA.
   Then by induction, for some 𝜎 ′ , 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡] ⊢ 𝜙 1 ⊳ 𝜎 ′ with corresponding valuation 𝑉 ′
(extending 𝑉1 ) where 𝑉 ′ (𝜎 ′ ) = true.
   Now by SProduceIfA, 𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊳ 𝜎 ′ . By deﬁnition 𝑉 ′ is the corresponding
valuation extending 𝑉 , and as shown before, 𝑉 ′ (𝑔(𝜎 ′ )) = true.
   Case 5(b). AssertIfB:
   Then h𝐻, 𝜌i ⊢ 𝑒 ⇓ false. Then 𝑉1 (𝑡) = false by lemma 29 and therefore 𝑉1 (𝑔(𝜎) &&! 𝑡) = true.
Also, h𝐻, 𝛼, 𝜌i  𝜙 2 by AssertIfB.
   Then by induction, for some 𝜎 ′ , 𝜎 [𝑔 = 𝑔(𝜎) && ! 𝑡] ⊢ 𝜙 2 ⊳ 𝜎 ′ with corresponding valuation 𝑉 ′
(extending 𝑉1 ) where 𝑉 ′ (𝜎) = true.
   Now by SProduceIfB, 𝜎 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊳ 𝜎 ′ . By deﬁnition 𝑉 ′ is the corresponding
valuation extending 𝑉 , and as shown before, 𝑉 ′ (𝑔(𝜎 ′ )) = true.
   Case 6. acc(𝑒.𝑓 ) where 𝑒 ∈ Expr, 𝑓 ∈ Field
Sound Gradual Verification with Symbolic Execution                                                 111:71


   By lemma 30, 𝜎 ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡. Let 𝜎 ′ = 𝜎 [H = H(𝜎); h𝑓 , 𝑡, freshi]. Then, by
SProduceField, 𝜎 ⊢ acc(𝑒.𝑓 )⊳𝜎 ′ . Let 𝑉 ′ be the corresponding valuation extending 𝑉 , then 𝑉 ′ (𝑔(𝜎 ′ )) =
𝑉 (𝑔(𝜎)) = true.
                                                                                                       

D.5 Consume
Deﬁnition 38. For a judgement 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ⊲ 𝜎 ′, R, Θ, given an initial valuation 𝑉 and heap 𝐻 , the
corresponding valuation is denoted
                               𝑉 [𝜎, 𝜎𝐸 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R, Θ | 𝐻 ].
This valuation is deﬁned as follows, depending on the rule that proves the derivation. Values are
referenced using the respective name from the rule deﬁnition.
   Note that the corresponding valuation always extends the initial valuation and is deﬁned for all
fresh symbolic values in the judgement.
 • SConsumeImprecision:
                         𝑉 [𝜎, 𝜎𝐸 ⊢ ? ∗ 𝜙 ⊲ h⊤, 𝑔(𝜎 ′ ), 𝛾 (𝜎 ′ ), ∅, ∅i, R, Θ | 𝐻 ] :=
                            𝑉 [𝜎, 𝜎𝐸 ⊢ 𝜙 ⊲ 𝜎 ′ , R, Θ | 𝐻 ]
 • SConsumeValue:
                      𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎, R, ∅ | 𝐻 ] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R]
 • SConsumeValueImprecise:
                 𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡], R; 𝑡, ∅ | 𝐻 ] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R | 𝐻 ]
 • SConsumeValueFailure:
                         𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎, {⊥}, ∅ | 𝐻 ] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R | 𝐻 ]
 • SConsumePredicate:
               𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ⊲ 𝜎 [H = H′ , H = ∅], _, _ | 𝐻 ] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R | 𝐻 ]
 • SConsumePredicateImprecise:
                𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ⊲ 𝜎 [𝐻 = ∅, H = ∅], _, _ | 𝐻 ] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R | 𝐻 ]
 • SConsumePredicateFailure:
                       𝑉 [𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ⊲ 𝜎, {⊥}, _ | 𝐻 ] := 𝑉 [𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R | 𝐻 ]
 • SConsumeAcc, SConsumeAccOptimistic, SConsumeAccImprecise,
   SConsumeAccFailure:
                         𝑉 [𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 [H = H′ , H = H ′ ], _, _ | 𝐻 ] :=
                           𝑉 [𝜎𝐸 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R | 𝐻 ]
 • SConsumeConjunction:
                             𝑉 [𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ⊲ 𝜎 ′′ , _, _ | 𝐻 ] :=
                                𝑉 [𝜎, 𝜎𝐸 ⊢ 𝜙 1 ⊲ 𝜎 ′ , R 1 , Θ1 | 𝐻 ]
                                   [𝜎 ′ , 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ⊲ 𝜎 ′′ , R 2, Θ2 | 𝐻 ]
 • SConsumeConditionalA:
                        𝑉 [𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲ 𝜎 ′ , R ∪ R ′ , _ | 𝐻 ] :=
                           𝑉 [𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 1 ⊲ 𝜎 ′, R ′ , Θ | 𝐻 ]
111:72                                                                   C. Zimmerman, J. DiVincenzo, and J. Aldrich


 • SConsumeConditionalB:
                         𝑉 [𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲ 𝜎 ′ , R ∪ R ′ , _ | 𝐻 ] :=
                           𝑉 [𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 2 ⊲ 𝜎 ′, R ′ , Θ | 𝐻 ]

Deﬁnition 39. For a judgement 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R, given an initial valuation 𝑉 and heap 𝐻 , the
corresponding valuation is denoted
                                            𝑉 [𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R | 𝐻 ].
   The is deﬁned by
                           𝑉 [𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R | 𝐻 ] := 𝑉 [𝜎, 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, R, _ | 𝐻 ]
where 𝜎, 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, R, _ is the judgement used when applying SConsume to derive 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R.

Lemma 35 (Consume results in more speciﬁc path condition (long form)). If 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ⊲ 𝜎 ′ , _, _,
then 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).

   Proof. By induction on 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ⊲ 𝜎 ′, _, _:
   Case 1. SConsumeImprecision – 𝜎, 𝜎𝐸 ⊢ ?∗𝜙⊲h⊤, 𝑔(𝜎 ′ ), 𝛾 (𝜎 ′ ), ∅, ∅i, R, Θ: By SConsumeImprecision
𝜎, 𝜎𝐸 [𝜄 = ⊤] ⊢ 𝜙 ⊲ 𝜎 ′ , R, Θ. Then 𝑔(h⊤, 𝑔(𝜎 ′ ), 𝛾 (𝜎 ′ ), ∅, ∅i) = 𝑔(𝜎 ′ ) and 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎) by in-
duction.
   Case 2. SConsumeValue, SConsumeValueFailure, SConsumePredicateFailure, SConsumeAccFailure
– 𝜎, 𝜎𝐸 ⊢ _ ⊲ 𝜎, _, _: Trivially 𝑔(𝜎) =⇒ 𝑔(𝜎).
   Case 3. SConsumeValueImprecise – 𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡], R; 𝑡, ∅: 𝑔(𝜎 [𝑔 = 𝑔(𝜎) && 𝑡]) =
𝑔(𝜎) && 𝑡 =⇒ 𝑔(𝜎).
   Case 4. SConsumePredicate, SConsumePredicateImprecise, SConsumeAcc, SConsumeAccOptimistic,
SConsumeAccImprecise – 𝜎, 𝜎𝐸 ⊢ _ ⊲ 𝜎 ′, _, _: In each respective rule 𝑔(𝜎 ′ ) = 𝑔(𝜎), therefore
𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
   Case 5. SConsumeConjunction, SConsumeConjunctionImprecise – 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗𝜙 2 ⊲𝜎 ′′ , _, Θ1 ∪Θ2 :
In each respective rule 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ⊲ 𝜎 ′ , R 1, Θ1 and 𝜎 ′ , 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ⊲ 𝜎 ′′ , , , therefore by
induction 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).
   Case 6. SConsumeConditionalA, SConsumeConditionalB – 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲ 𝜎 ′ ,
R ∪ R ′ , Θ: In each respective rule 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡], 𝜎𝐸 ⊢ 𝜙 ′ ⊲ 𝜎 ′ , _, _ for some 𝑡, 𝜙 ′ . Therefore by
induction 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎) && 𝑡 ′ =⇒ 𝑔(𝜎).
                                                                                                             

Lemma 36 (Consume results in more speciﬁc path condition (short form)). If 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , _, then
𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).

   Proof. By SConsume 𝜎, 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, _, _, thus by lemma 35, 𝑔(𝜎 ′ ) =⇒ 𝑔(𝜎).                                   

Lemma 37 (Soundness of remf for precise heaps and imprecise states). If h𝐻, 𝛼, 𝜌i 𝑉 𝜎 and 𝜄 (𝜎)
then h𝐻, 𝛼 \ {(𝑉 (𝑡), 𝑓 )}i 𝑉 remf (H(𝜎), 𝜎, 𝑡, 𝑓 ) for any 𝑡, 𝑓 .
  Proof. Let H′ = remf (H(𝜎), 𝜎, 𝑡, 𝑓 ) and 𝛼 ′ = 𝛼 \ {(𝑉 (𝑡), 𝑓 )}. Then by deﬁnition H′ ⊆ H(𝜎),
therefore h𝐻, 𝛼i 𝑉 H′ . In addition, H′ contains no predicate values. Thus by (1) it suﬃces to show
that ∀ h𝑓 ′ , 𝑡 ′ , 𝑡 ′′ i ∈ H′ : h𝑉 (𝑡 ′ ), 𝑓 ′ i ∈ 𝛼 ′ .
  Let h𝑓 ′ , 𝑡 ′ , 𝑡 ′′ i be some element of H′ . Then by deﬁnition ¬ alias(𝜎, 𝑡, 𝑓 , 𝑡 ′ , 𝑓 ′ ); then by deﬁnition
(𝑓 ≠ 𝑓 ′ ) ∨ ¬ sat(𝑔(𝜎) && [𝑡 == 𝑡 ′ ]).
Sound Gradual Verification with Symbolic Execution                                                           111:73


  Therefore (𝑓 ≠ 𝑓 ′ ) ∨ (𝑉 (𝑔(𝜎) && 𝑡 == 𝑡 ′ ) = false), and thus (𝑓 ≠ 𝑓 ′ ) ∨ (𝑉 (𝑔(𝜎)) = false) ∨
(𝑉 (𝑡) ≠ 𝑉 (𝑡 ′ )). But 𝑉 (𝑔(𝜎)) = true, thus (𝑓 ≠ 𝑓 ′ ) ∨ (𝑉 (𝑡) ≠ 𝑉 (𝑡 ′ )). Therefore h𝑉 (𝑡), 𝑓 i ≠
h𝑉 (𝑡 ′ ), 𝑓 ′ i.
  Also h𝑉 (𝑡 ′ ), 𝑓 ′ i ∈ 𝛼 since h𝐻, 𝛼i 𝑉 H′ . Therefore h𝑉 (𝑡 ′ ), 𝑓 ′ i ∈ 𝛼 \ {(𝑉 (𝑡), 𝑓 )} = 𝛼 ′ .
  Therefore h𝐻, 𝛼 ′ i 𝑉 H′ .                                                                                     

Lemma 38. If 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R, Θ then 𝛾 (𝜎 ′ ) = 𝛾 (𝜎).
   Proof. Trivial by induction on 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ⊲ 𝜎 ′, R, Θ.                                                        

Lemma 39. If 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, R then 𝛾 (𝜎 ′ ) = 𝛾 (𝜎).
   Proof. By SConsume 𝜎, 𝜎 ⊢ 𝜙˜ ⊲ 𝜎, R, _, thus by lemma 38 𝛾 (𝜎 ′ ) = 𝛾 (𝜎).                                    

Lemma 40 (Soundness of remfp for precise heaps). If h𝐻, 𝛼, 𝜌i 𝑉 𝜎 and h𝑓 , 𝑡, _i ∈ H(𝜎), then
h𝐻, 𝛼 \ {h𝑉 (𝑡), 𝑓 i}i 𝑉 remfp (H(𝜎), 𝜎, 𝑡, 𝑓 ) for any 𝑡, 𝑓 .
   Proof. Let H′ = remfp (H(𝜎), 𝜎, 𝑡, 𝑓 ), let H′′ = remf (H(𝜎), 𝜎, 𝑡, 𝑓 ), and let 𝛼 ′ = 𝛼 \ {h𝑉 (𝑡), 𝑓 i}.
By deﬁnition of remfp and remf , H′′ ⊆ H′ ⊆ H(𝜎).
   Let h𝑓 ′ , 𝑡 ′ , _i be an arbitrary ﬁeld chunk in H′ . Thus ¬ alias(𝜎, 𝑡, 𝑓 , 𝑡 ′ , 𝑓 ′ ) by deﬁnition of remf .
Then h𝑉 (𝑡), 𝑓 i ≠ h𝑉 (𝑡 ′ ), 𝑓 ′ i:
 • If 𝜄 (𝜎): Then (𝑓 ≠ 𝑓 ′ ) ∨ ¬ sat(𝑔(𝜎) && 𝑡 == 𝑡 ′ ), therefore (𝑓 ≠ 𝑓 ′ ) ∨ (𝑉 (𝑔(𝜎)) ≠ true) ∨ (𝑉 (𝑡) ≠
     𝑉 (𝑡 ′ )). But 𝑉 (𝑔(𝜎)) = true, thus (𝑓 ≠ 𝑓 ′ ) ∨ (𝑉 (𝑡) ≠ 𝑉 (𝑡 ′ )). Therefore h𝑉 (𝑡), 𝑓 i ≠ h𝑉 (𝑡 ′ ), 𝑓 ′ i.
 • Otherwise ¬𝜄 (𝜎): Then (𝑓 ≠ 𝑓 ′ ) ∨ (𝑔(𝜎) =⇒          Y 𝑡 ==𝑡 ′ ). Thus 𝑓 ≠ 𝑓 ′ or 𝑉 (𝑡) ≠ 𝑉 (𝑡 ′ ). Thus 𝑓 ≠ 𝑓 ′
      or 𝑡 ≠ 𝑡 (using syntactic equivalence). But now {h𝑉 (𝑡), 𝑓 i} ∩ {h𝑉 (𝑡 ′ ), 𝑓 i} = 𝑉 Lh𝑓 , 𝑡, _iM𝐻 ∩
                  ′

     𝑉 Lh𝑓 ′ , 𝑡 ′ , _iM𝐻 = ∅ since h𝐻, 𝛼i 𝑉 H(𝜎), h𝑓 , 𝑡, _i and h𝑓 ′, 𝑡 ′ , _i ∈ H(𝜎), and h𝑓 , 𝑡, _i ≠
      h𝑓 , 𝑡 ′ , _i. Therefore h𝑉 (𝑡), 𝑓 i ≠ h𝑉 (𝑡 ′ ), 𝑓 ′ i.
Therefore h𝑉 (𝑡 ′ ), 𝑓 ′ i ∈ 𝛼 ′ since h𝑓 ′, 𝑡 ′ , _i ∈ H(𝜎).
   Also, let h𝑝 ′ , 𝑡 ′ i be an arbitrary predicate chunk in H′ . By deﬁnition of remfp , h𝑝 ′ , 𝑡 ′ i ∈ H(𝜎);
thus h𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡 ′ )]i  predicate(𝑝 ′ ).
   But also 𝑉 Lh𝑓 , 𝑡, _iM𝐻 ∩ 𝑉 Lh𝑝 ′ , 𝑡 ′ iM𝐻 = ∅ since h𝑓 , 𝑡, _i and h𝑝 ′ , 𝑡 ′ i ∈ H(𝜎) and h𝑓 , 𝑡, _i ≠
h𝑝 ′ , 𝑡 ′ i. Therefore Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 (𝑡 ′ ) ] i ⊆ 𝛼 ′ by lemma 4 and since
{h𝑉 (𝑡), 𝑓 i} ∩ Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 (𝑡 ′ ) ] i = 𝑉 Lh𝑓 , 𝑡, _iM𝐻 ∩ 𝑉 Lh𝑝 ′ , 𝑡 ′ iM𝐻 = ∅. Thus
h𝐻, 𝛼 ′ , [𝑥 ↦→ 𝑉 (𝑡 ′ )]i  predicate(𝑝) by lemma 12.
  Finally, since H′ ⊆ H(𝜎), the remaining conditions of (1) are satisﬁed. Therefore
h𝐻, 𝛼 ′ i 𝑉 H′ .                                                                                                 

Lemma 41 (Soundness of remf for optimistic heaps). If 𝜎 is well-formed and h𝐻, 𝛼, 𝜌i 𝑉 𝜎 then
h𝐻, 𝛼 \ {h𝑉 (𝑡), 𝑓 i}i 𝑉 remf (H (𝜎), 𝜎, 𝑡, 𝑓 ) for any 𝑡, 𝑓 .
   Proof. Case 1. 𝜄 (𝜎): Similar to proof of lemma 37, replacing H with H .
   Case 2. ¬𝜄 (𝜎): Then H (𝜎) = ∅ since 𝜎 is well-formed. Then trivially h𝐻, ∅i 𝑉 H (𝜎) and thus
also h𝐻, 𝛼 \ {h𝑉 (𝑡), 𝑓 i}i 𝑉 H (𝜎) by 18.
                                                                                                                 
Lemma 42 (Soundness of Θ calculation). If 𝜙 is a precise formula, h𝐻, 𝛼 𝐸 , 𝜌i 𝑉 𝜎𝐸 , 𝜎, 𝜎𝐸 ⊢ 𝜙 ⊲𝜎 ′,
R, Θ with corresponding valuation 𝑉 ′ , 𝑉 ′ (𝑔(𝜎 ′ )) = true, and h𝐻, 𝛼 ′ , 𝜌i  𝜙 where 𝛼 ′ ⊆ 𝛼 𝐸 , then
h𝐻, 𝑉 ′ LΘM𝐻 , 𝜌i  𝜙 and 𝑉 LΘM𝐻 ⊆ 𝛼 ′ .
111:74                                                                 C. Zimmerman, J. DiVincenzo, and J. Aldrich


   Proof. By induction on 𝜎, 𝜎𝐸 ⊢ 𝜙 ⊲ 𝜎 ′, R, Θ:
   Case 1. SConsumeImprecision – 𝜎, 𝜎𝐸 ⊢ ? ∗ 𝜙 ⊲ h⊤, 𝑔(𝜎 ′ ), 𝛾 (𝜎 ′ ), ∅, ∅i, R, Θ: ? ∗ 𝜙 is not precise,
therefore this rule cannot apply.
   Case 2. SConsumeValue, SConsumeValueImprecise, SConsumeValueFailure – 𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎, _, ∅:
   Since h𝐻, 𝛼 ′ , 𝜌i  𝑒, h𝐻, 𝜌i ⊢ 𝑒 ⇓ true by AssertValue. Therefore h𝐻, 𝑉 L∅M𝐻 , 𝜌i  𝑒 by
AssertValue.
   Also, 𝑉 L∅M𝐻 = ∅ ⊆ 𝛼 ′ .
   Case 3. SConsumePredicate, SConsumePredicateImprecise, SConsumePredicateFailure – 𝜎, 𝜎𝐸 ⊢
𝑝 (𝑒) ⊲ _, _, {h𝑝, 𝑡i}:
   By the respective rule, 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡 . The corresponding valuation for this case ex-
tends the corresponding valuation for all of these derivation.
   Since h𝐻, 𝛼, 𝜌i  𝑝 (𝑒), h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 for some 𝑣 by AssertPredicate. By assumptions
h𝐻, 𝛼 𝐸 , 𝜌i 𝑉 𝜎𝐸 . Thus by lemma 29 𝑣 = 𝑉 ′ (𝑡), i.e., h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡).
    Let 𝑥 = predicate_params(𝑝). By AssertPredicate h𝐻, 𝛼 ′ , [𝑥 ↦→ 𝑉 ′ (𝑡)]i  predicate(𝑝). Also,
𝑉 Lh𝑝, 𝑡iM𝐻 = Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 ′ (𝑡 ) ] i . Therefore h𝐻, 𝑉 Lh𝑝, 𝑡 i∩𝛼 ′ M𝐻 , [𝑥 ↦→ 𝑉 ′ (𝑡)]i  predicate(𝑝)
by lemma 11.
    But predicate(𝑝) must be a speciﬁcation, thus 𝑉 Lh𝑝, 𝑡iM𝐻 = Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 ′ (𝑡 ) ] i ⊆
𝑉 Lh𝑝, 𝑡iM𝐻 ∩ 𝛼 ′ by lemma 4. Therefore 𝑉 L{h𝑝, 𝑡 i}M𝐻 ⊆ 𝛼 ′ .
    Then h𝐻, 𝑉 L{h𝑝, 𝑡i}M𝐻 , [𝑥 ↦→ 𝑉 ′ (𝑡)]i  predicate(𝑝), and thus h𝐻, 𝑉 L{h𝑝, 𝑡i}M𝐻 , 𝜌i  𝑝 (𝑒) by
AssertPredicate.
    Case 4. SConsumeAcc, SConsumeAccOptimistic, SConsumeAccImprecise, SConsumeAccFailure –
𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 ′ , _, {h𝑡𝑒 , 𝑓 i}:
    By the respective rule, 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ _ for some 𝑡𝑒 . The corresponding valuation for this case
extends the corresponding valuation for this derivation.
    Since h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ), h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 for some 𝑣 by AssertAcc. Thus by lemma 29 𝑣 =
𝑉 ′ (𝑡𝑒 ), i.e. h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ).
    By AssertAcc h𝑉 ′ (𝑡𝑒 ), 𝑓 i ∈ 𝛼 ′ . Also, {h𝑉 ′ (𝑡𝑒 ), 𝑓 i} = 𝑉 ′ L{h𝑡𝑒 , 𝑓 i}M𝐻 , therefore 𝑉 ′ L{h𝑡𝑒 , 𝑓 i}M𝐻 ⊆
𝛼 and also h𝐻, 𝑉 ′ L{h𝑡𝑒 , 𝑓 i}M𝐻 , 𝜌i  acc(𝑒.𝑓 ) by AssertAcc.
  ′

    Case 5. SConsumeConjunction, SConsumeConjunctionImprecise – 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗𝜙 2 ⊲𝜎 ′′ , _, Θ1 ∪Θ2 :
    By the respective rule, 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ⊲ 𝜎 ′, _, Θ1 and 𝜎 ′ , 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ⊲ 𝜎 ′′ , _, Θ2 . Let 𝑉 ′ be
the corresponding valuation for this case, thus 𝑉 ′ extends the corresponding valuations for these
judgements.
    By assumptions, 𝑉 ′ (𝑔(𝜎 ′′ )) = true and 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ) by 35. Therefore h𝐻, 𝛼 𝐸 , 𝜌i 𝑉 ′
𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )].
    Then h𝐻, 𝛼 1, 𝜌i  𝜙 1 and h𝐻, 𝛼 2, 𝜌i  𝜙 2 where 𝛼 1 ∪𝛼 2 ⊆ 𝛼 ′ and 𝛼 1 ∩𝛼 2 = ∅ by AssertConjunction,
since h𝐻, 𝛼 ′ , 𝜌i  𝜙 1 ∗ 𝜙 2 . Then by induction h𝐻, 𝑉 ′ LΘ1 M𝐻 , 𝜌i  𝜙 1 , h𝐻, 𝑉 ′ LΘ2 M𝐻 , 𝜌i  𝜙 2 ,
𝑉 ′ LΘ1 M𝐻 ⊆ 𝛼 1 , and 𝑉 ′ LΘ2 M𝐻 ⊆ 𝛼 1 .
    Now 𝑉 ′ LΘ1 M𝐻 ∩ 𝑉 ′ LΘ2 M𝐻 = ∅ and 𝑉 ′ LΘ1 M𝐻 ∪ 𝑉 ′ LΘ2 M𝐻 = 𝑉 ′ LΘ1 ∪ Θ2 M𝐻 ⊆ 𝛼 ′ . Therefore
h𝐻, 𝑉 ′ LΘ1 ∪ Θ2 M𝐻 , 𝜌i  𝜙 1 ∗ 𝜙 2 by AssertConjunction.
    Case 6. SConsumeConditionalA – 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲ 𝜎 ′, R ∪ R ′ , Θ:
    By SConsumeConditionalA 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡. Let 𝑉1 be the corresponding valuation.
    Also, 𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 ⊢ 𝜙 1 ⊲ 𝜎 ′, _, Θ where 𝑔′ = 𝑔 && 𝑡. Let 𝑉 ′ be the corresponding valuation for
this case, which extends the corresponding valuation for this judgement and 𝑉1 .
    Since h𝐻, 𝛼 ′ , 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 , by AssertIfA h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 for some 𝑣. By lemma 29
𝑣 = 𝑉1 (𝑡). Also, since 𝑉 ′ (𝑔(𝜎 ′ )) = true and 𝑔(𝜎 ′ ) =⇒ 𝑔′ = 𝑔(𝜎) && 𝑡 by lemma 35, 𝑉1 (𝑡) = true.
Therefore h𝐻, 𝜌i ⊢ 𝑒 ⇓ true.
Sound Gradual Verification with Symbolic Execution                                                   111:75


     Also by AssertIfA h𝐻, 𝛼 ′ , 𝜌i  𝜙 1 . Therefore by induction h𝐻, 𝑉 LΘM𝐻 , 𝜌i  𝜙 1 and 𝑉 LΘM𝐻 ⊆ 𝛼 ′ .
     Finally, h𝐻, 𝑉 LΘM𝐻 , 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 by AssertIfA.
     Case 7. SConsumeConditionalB – 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲ 𝜎 ′, R ∪ R ′ , Θ: Similar to case
6.
                                                                                                         

Lemma 43 (Soundness of consume for precise formulas). Let 𝜙 be some precise formula, 𝑉 be
some initial valuation, 𝐻 be some heap, 𝜌 be some environment, 𝛼 𝐸 and 𝛼 be sets of permissions
such that 𝛼 ⊆ 𝛼 𝐸 , and 𝜎 and 𝜎𝐸 be well-formed symbolic states such that h𝐻, 𝛼, 𝜌i 𝑉 𝜎 and
h𝐻, 𝛼 𝐸 , 𝜌i 𝑉 𝜎𝐸 .
  Then, if 𝜎, 𝜎𝐸 ⊢ 𝜙 ⊲ 𝜎 ′, R, Θ with corresponding valuation 𝑉 ′ , h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ R, and 𝑉 ′ (𝑔(𝜎 ′ )) =
true, then

                 h𝐻, 𝛼 𝐸 , 𝜌i  𝜙,   h𝐻, 𝛼 \ 𝑉 LΘM𝐻 , 𝜌i 𝑉 ′ 𝜎 ′,   and h𝐻, 𝛼 𝐸 , 𝜌i ⊢frmI 𝜙 .        (16)

     Furthermore, if the above conditions hold and R ∩ SPerm = ∅, then

                                                 h𝐻, 𝛼, 𝜌i  𝜙 .                                      (17)

   Proof. Suppose that 𝜎, 𝜎𝐸 ⊢ 𝜙 ⊲ 𝜎 ′, R, Θ with corresponding valuation 𝑉 ′ , h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ R, and
𝑉 (𝑔(𝜎 ′ )) = true. Complete the proof by induction on 𝜎, 𝜎𝐸 ⊢ 𝜙 ⊲ R, Θ, :
 ′

   Case 1. SConsumeImprecision – 𝜎, 𝜎𝐸 ⊢ ? ∗ 𝜙 ⊲ h⊤, 𝑔(𝜎 ′ ), 𝛾 (𝜎 ′ ), ∅, ∅i, R, Θ: Since ? ∗ 𝜙 is
imprecise, this rule cannot apply.
   Case 2. SConsumeValue – 𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎, R, ∅:
   By SConsumeValue 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R. Let 𝑉 ′ be the corresponding valuation, with initial valuation
𝑉 . Then 𝑉 ′ is the corresponding valuation for this case.
   Thus by lemma 28 h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡). Also by SConsumeValue 𝑔(𝜎) =⇒ 𝑡. Therefore 𝑉 ′ (𝑡) =
true, and therefore h𝐻, 𝜌i ⊢ 𝑒 ⇓ true. Thus h𝐻, 𝛼 𝐸 , 𝜌i  𝑒 by AssertValue.
   𝑉 L∅M𝐻 = ∅, therefore h𝐻, 𝛼 \ 𝑉 L∅M𝐻 , 𝜌i 𝑉 ′ 𝜎 since 𝑉 ′ extends 𝑉 .
   Finally, h𝐻, 𝛼 𝐸 , 𝜌i ⊢frm 𝑒 by lemma 28. Therefore h𝐻, 𝛼 𝐸 , 𝜌i ⊢frmI 𝑒 by IFrameExpression, which
completes the proof of (16).
   As shown before, h𝐻, 𝜌i ⊢ 𝑒 ⇓ true, thus h𝐻, 𝛼, 𝜌i  𝑒 by AssertValue, which proves (17).
   Case 3. SConsumeValueImprecise – 𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡], R; 𝑡, ∅:
   By SConsumeValueImprecise 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R. Let 𝑉 ′ be the valuation corresponding to this
derivation, with initial valuation 𝑉 . Then 𝑉 ′ is the valuation corresponding to this case.
   Let 𝜎 ′ = 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡].
   By assumptions, h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ {𝑡 } by lemma 23. Thus 𝑉 ′ (𝑡) = true by CheckValue. Also, h𝐻, 𝜌i ⊢
𝑒 ⇓ 𝑉 ′ (𝑡) by lemma 28; therefore h𝐻, 𝜌i ⊢ 𝑒 ⇓ true. Thus, by AssertValue, h𝐻, 𝛼 𝐸 , 𝜌i  𝑒.
   𝑉 L∅M𝐻 = ∅, therefore h𝐻, 𝛼 \ 𝑉 L∅M𝐻 , 𝜌i 𝑉 ′ 𝜎 since 𝑉 ′ extends 𝑉 .
   Furthermore, since 𝑉 ′ (𝑡) = true, 𝑉 ′ (𝑔(𝜎 ′ )) = 𝑉 (𝑔(𝜎)) && 𝑉 ′ (𝑡) = true. Since 𝜎 ′ and 𝜎 diﬀer
only in their 𝑔 components, h𝐻, 𝛼 \ \𝑉 L∅M𝐻 , 𝜌i 𝑉 ′ 𝜎 ′ .
   Finally, h𝐻, 𝛼 𝐸 , 𝜌i ⊢frm 𝑒 by lemma 28. Therefore h𝐻, 𝛼 𝐸 , 𝜌i ⊢frmI 𝑒 by IFrameExpression.
   Case 4. SConsumeValueFailure – 𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎, {⊥}, ∅:
    h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ R ∪ {⊥} is a contradiction, thus the lemma vacuously holds.
                                                        Ð
   Case 5. SConsumePredicate – 𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ⊲ 𝜎 ′ , R, {h𝑝, 𝑡i}:
   By SConsumePredicate, for each 𝑒, 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R for some 𝑡 and R. Let 𝑉 ′ be corresponding
valuation for this case, thus 𝑉 ′ extends the respective individual corresponding valuations and for
each R, h𝐻, 𝛼i ⊢𝑉 ′ R by lemma 23
111:76                                                                     C. Zimmerman, J. DiVincenzo, and J. Aldrich


  Therefore, for each 𝑒 and corresponding 𝑡, h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) by lemma 28. By SConsumePredicate,
for each 𝑡, 𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ for some 𝑡 ′ , thus 𝑉 ′ (𝑡) = 𝑉 ′ (𝑡 ′ ) since 𝑉 ′ (𝑔(𝜎)) = true. Therefore
h𝐻, 𝜌i ⊢ 𝑒𝑖 ⇓ 𝑉 ′ (𝑡𝑖′ ).
  By SConsumePredicate h𝑝, 𝑡 ′ i ∈ H(𝜎). Since h𝐻, 𝛼i 𝑉 𝜎, h𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡 ′ )]i  predicate(𝑝)
where 𝑥 = predicate_params(𝑝). Thus by AssertPredicate h𝐻, 𝛼, 𝜌i  𝑝 (𝑒), which proves (17).
Also, h𝐻, 𝛼 𝐸 , 𝜌i  𝑝 (𝑒) by lemma 9.
  Let 𝛼 ′ = 𝑉 Lh𝑝, 𝑡iM𝐻 , therefore 𝛼 ′ = Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 ′ (𝑡 ) ] i = Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 ′ (𝑡 ′ ) ] i .
   By SConsumePredicate 𝜎 ′ = 𝜎 [H = H′ , H = ∅] where H = H′ ; h𝑝, 𝑡 i. Thus h𝐻, 𝛼i 𝑉 ′ H(𝜎 ′ )
since H(𝜎 ′ ) ⊂ H(𝜎).
   Then 𝑉 ′ LℎM𝐻 ∩ 𝛼 ′ = ∅ for all ℎ ∈ H(𝜎 ′ ) since h𝐻, 𝛼i 𝑉 ′ H(𝜎), h𝑝, 𝑡 i ∈ H(𝜎), and h𝑝, 𝑡 i ∉ H(𝜎 ′ ).
Therefore, by lemma 16, h𝐻, 𝛼 \ 𝛼 ′ i 𝑉 ′ H(𝜎 ′ ).
  Also, since H (𝜎 ′ ) = ∅, h𝐻, 𝛼 \ 𝛼 ′ i 𝑉 ′ H (𝜎 ′ ).
   Therefore h𝐻, 𝛼 \ 𝛼 ′ , 𝜌i 𝑉 ′ 𝜎 ′ since 𝜎 ′ and 𝜎 diﬀer only in their H and H components.
    By lemmas 23 h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ R for each R, thus h𝐻, 𝛼 𝐸 , 𝜌i ⊢frm 𝑒 for each 𝑒 by lemma 28, thus
h𝐻, 𝛼 𝐸 , 𝜌i ⊢frmI 𝑝 (𝑒) by IFramePredicate. Thus (16) holds.
                                                                  Ð
    Case 6. SConsumePredicateImprecise – 𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ⊲ 𝜎 ′, R; h𝑝, 𝑡 i, {h𝑝, 𝑡i}:
    By SConsumePredicateImprecise, for each 𝑒, 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R for some 𝑡 and R. Let 𝑉 ′ be corre-
sponding valuation for this case, thus 𝑉 ′ extends the respective individual corresponding valua-
tions and for each R, h𝐻, 𝛼i ⊢𝑉 ′ R by lemma 23
   Therefore, for each 𝑒 and corresponding 𝑡, h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) by lemma 28. By
SConsumePredicateImprecise, for each 𝑡, 𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ for some 𝑡 ′ , thus 𝑉 ′ (𝑡) = 𝑉 ′ (𝑡 ′ ) since
𝑉 ′ (𝑔(𝜎)) = true. Therefore h𝐻, 𝜌i ⊢ 𝑒𝑖 ⇓ 𝑉 ′ (𝑡𝑖′ ).
   Also, h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ {h𝑝, 𝑡i} by assumptions and lemma 23. Thus h𝐻, 𝛼 𝐸 , [𝑥 ↦→ 𝑉 ′ (𝑡)]i  predicate(𝑝)
by CheckPred. Therefore h𝐻, 𝛼 𝐸 , 𝜌i  𝑝 (𝑒) by AssertPredicate.
    By SConsumePredicateImprecise 𝜎 ′ = 𝜎 [H = ∅, H = ∅], thus h𝐻, 𝛼 \ 𝑉 ′ L{h𝑝, 𝑡 i}M𝐻 i 𝑉 ′ H(𝜎 ′ )
and h𝐻, 𝛼 \ 𝑉 ′ L{h𝑝, 𝑡 i}M𝐻 i 𝑉 ′ H (𝜎 ′ ). Therefore h𝐻, 𝛼 \ 𝑉 L{h𝑝, 𝑡 i}M𝐻 , 𝜌i 𝑉 ′ 𝜎 ′ since 𝜎 ′ and 𝜎
diﬀer only in their H and H components.
    For each 𝑒, h𝐻, 𝛼 𝐸 , 𝜌i ⊢frm 𝑒 by lemma 28. Therefore h𝐻, 𝛼 𝐸 , 𝜌i ⊢frmI 𝑝 (𝑒) by IFramePredicate,
which completes the proof of (16).
    Also, h𝑝, 𝑡i ∈ SPerm is in the resulting set of checks, which contradicts the premises of (17).
Therefore it is vacuously true.
    Case 7. SConsumePredicateFailure – 𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ⊲ 𝜎, {⊥}, {h𝑝, 𝑡i}:
    h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ {⊥} is a contradiction, thus the lemma vacuously holds.
    Case 8. SConsumeAcc – 𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 [H = H′ , H = H ′ ], R, {h𝑡𝑒 , 𝑓 i}:
    By SConsumeAcc 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R. Let 𝑉 ′ be the corresponding valuation, thus 𝑉 ′ is the corre-
sponding valuation for this case.
    Thus h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ) by lemma 28. Also 𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 by SConsumeAcc, thus 𝑉 ′ (𝑡𝑒′ ) =
𝑉 (𝑡𝑒 ) since 𝑉 ′ (𝑔(𝜎)) = true. Therefore, h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒′ ).
  ′

    Since h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) by SConsumeAcc and h𝐻, 𝛼i 𝑉 H(𝜎), h𝑉 ′ (𝑡𝑒′ ), 𝑓 i ∈ 𝛼. Thus h𝐻, 𝛼, 𝜌i 
acc(𝑒.𝑓 ) by AssertAcc, which proves (17). Therefore h𝐻, 𝛼 𝐸 , 𝜌i  acc(𝑒.𝑓 ) by lemma 9 since
𝛼 ⊆ 𝛼𝐸 .
    Let H′ = remfp (H(𝜎), 𝜎, 𝑡𝑒 , 𝑓 ). Therefore h𝐻, 𝛼 \ {h𝑉 ′ (𝑡𝑒 ), 𝑓 i}i 𝑉 ′ H′ by lemma 40. Also,
{h𝑉 ′ (𝑡𝑒′ ), 𝑓 i} = {h𝑉 ′ (𝑡𝑒 ), 𝑓 i} = 𝑉 ′ L{h𝑡𝑒 , 𝑓 i}M𝐻 . Thus h𝐻, 𝛼 \ 𝑉 ′ L{h𝑡𝑒 , 𝑓 i}M𝐻 i 𝑉 ′ H′ .
Sound Gradual Verification with Symbolic Execution                                                       111:77


   Likewise, let H ′ = remf (H (𝜎), 𝜎, 𝑡𝑒 , 𝑓 ). Then similarly h𝐻, 𝛼 \𝑉 L{h𝑡𝑒 , 𝑓 i}M𝐻 i 𝑉 ′ H ′ by lemma
41.
   By SConsumeAcc, 𝜎 ′ = 𝜎 [H = H′ , H = H ′ ]. Now, since 𝜎 and 𝜎 ′ diﬀer only in their H and H
components, using the properties of H′ and H ′ shown above, h𝐻, 𝛼 \ 𝑉 L{h𝑡𝑒 , 𝑓 i}M𝐻 , 𝜌i 𝑉 ′ 𝜎 ′ .
   Finally, h𝐻, 𝛼 𝐸 , 𝜌i ⊢frm 𝑒 by lemma 28. Therefore h𝐻, 𝛼 𝐸 , 𝜌i ⊢frmI acc(𝑒.𝑓 ) by IFrameAcc, which
completes the proof of (16).
   Case 9. SConsumeAccOptimistic – 𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 ′ , R, {h𝑡𝑒 , 𝑓 i}: Similar to case 8, except
to show that h𝐻, 𝛼 \ {h𝑉 ′ (𝑡𝑒′ ), 𝑓 i}i 𝑉 H′ .
   Since h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H (𝜎), H (𝜎) ≠ ∅. Therefore, since 𝜎 is well-formed, 𝜄 (𝜎) = ⊤. Let H′ =
remf (H(𝜎), 𝜎, 𝑡𝑒′ , 𝑓 ). Therefore h𝐻, 𝛼 \ {h𝑉 ′ (𝑡𝑒′ ), 𝑓 i}i 𝑉 H′ by lemma 37.
   Continue as in case 8.
   Case 10. SConsumeAccImprecise – 𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 ′ , R; h𝑡𝑒 , 𝑓 i, {h𝑡𝑒 , 𝑓 i}:
   By SConsumeAcc 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ R. Let 𝑉 ′ be the corresponding valuation, thus 𝑉 ′ is the corre-
sponding valuation for this case.
   Then h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ R by assumptions and lemma 23. Thus h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡𝑒 ) by lemma 28.
   Also, h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ h𝑡𝑒 , 𝑓 i by assumptions and lemma 23. Then h𝑉 ′ (𝑡𝑒 ), 𝑓 i ∈ 𝛼 𝐸 by CheckAcc.
Therefore h𝐻, 𝛼 𝐸 , 𝜌i  acc(𝑒.𝑓 ) by AssertAcc.
   Let H′ = remf (H(𝜎), 𝜎, 𝑡𝑒 , 𝑓 ). By SConsumeAccImprecise 𝜄 (𝜎). Thus h𝐻, 𝛼 \ {h𝑉 ′ (𝑡𝑒 ), 𝑓 i}i 𝑉 ′ H′
by lemma 37. Also, {h𝑉 ′ (𝑡𝑒 ), 𝑓 i} = 𝑉 ′ L{h𝑡𝑒 , 𝑓 i}M𝐻 . Thus h𝐻, 𝛼 \ 𝑉 ′ L{h𝑡𝑒 , 𝑓 i}M𝐻 i 𝑉 ′ H′ .
   Likewise, let H ′ = remf (H (𝜎), 𝜎, 𝑡𝑒 , 𝑓 ). Then h𝐻, 𝛼 \ 𝑉 Lh𝑡𝑒 , 𝑓 iM𝐻 i 𝑉 ′ H ′ by lemma 41.
   By SConsumeAcc, 𝜎 ′ = 𝜎 [H = H′ , H = H ′ ]. Now, since 𝜎 and 𝜎 ′ diﬀer only in their H and H
components, using the properties of H′ and H ′ shown above, h𝐻, 𝛼 \ 𝑉 L{h𝑡𝑒 , 𝑓 i}M𝐻 , 𝜌i 𝑉 ′ 𝜎 ′ .
   By lemma 28 h𝐻, 𝛼 𝐸 , 𝜌i ⊢frm 𝑒, therefore h𝐻, 𝛼 𝐸 , acc(𝑒.𝑓 )i ⊢frmI by IFrameAcc. Thus (16) holds.
   Also, h𝑡𝑒 , 𝑓 i ∈ SPerm is in the resulting set of checks, which contradicts the premises of (17),
therefore it vacuously holds.
   Case 11. SConsumeAccFailure – 𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎, {⊥}, {h𝑡𝑒 , 𝑓 i}:
   h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ {⊥} is a contradiction, thus the lemma vacuously holds.
   Case 12. SConsumeConjunction – 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ⊲ 𝜎 ′′ , R 1 ∪ R 2 , Θ1 ∪ Θ2 :
   By SConsumeConjunction 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ⊲ 𝜎 ′ , R 1, Θ1 and 𝜎 ′ , 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ⊲ 𝜎 ′′ , R 2, Θ2 . Let
𝑉1 and 𝑉 ′ be the respective corresponding valuations, with initial valuations 𝑉 and 𝑉1 , respectively.
Then 𝑉 ′ is the corresponding valuation for this case.
   By lemma 35, 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎 ′ ). Thus 𝑉 ′ (𝑔(𝜎 ′ )) = 𝑉1 (𝑔(𝜎 ′ )) = true. Also, h𝐻, 𝛼 𝐸 i ⊢𝑉1 R 1 by
lemma 23, since 𝑉 ′ extends 𝑉1 .
   By SConsumeConjunction (R 1 ∪ R 2 ) ∩ SPerm = ∅, thus R 1 ∩ SPerm = ∅.
   Let 𝛼 1 = 𝑉 LΘ1 M𝐻 . By induction, using (17), h𝐻, 𝛼, 𝜌i  𝜙 1 . Thus h𝐻, 𝛼 1 , 𝜌i  𝜙 1 and 𝛼 1 ⊆ 𝛼 by
lemma 42.
   Also h𝐻, 𝛼 \ 𝛼 1, 𝜌i 𝑉 𝜎 ′ by induction, h𝐻, 𝛼 𝐸 , 𝜌i 𝑉 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] since 𝑉1 extends 𝑉 and
                            1                                 1
𝑉1 (𝑔(𝜎 ′ )) = true, and h𝐻, 𝛼 𝐸 i ⊢𝑉 R 2 by lemma 23. Finally, by assumptions 𝑉 ′ (𝑔(𝜎 ′′ )) = true,
and (𝛼 \ 𝛼 1 ) ⊆ 𝛼 ⊆ 𝛼 𝐸 . Thus by induction h𝐻, (𝛼 \ 𝛼 1 ) \ 𝑉 LΘ2 M𝐻 , 𝜌i 𝑉 ′ 𝜎 ′′ .
   Also by induction, using (17), h𝐻, 𝛼 \ 𝛼 1 , 𝜌i  𝜙 2 .
   Now (𝛼\𝛼 1 ) ⊆ 𝛼, 𝛼 1 ⊆ 𝛼, and (𝛼\𝛼 1 )∩𝛼 1 = ∅. Therefore h𝐻, 𝛼, 𝜌i  𝜙 1 ∗𝜙 2 by AssertConjunction,
which proves (17). Then by lemma 9 h𝐻, 𝛼 𝐸 , 𝜌i  𝜙 1 ∗ 𝜙 2 .
   As shown before, h𝐻, (𝛼 \ 𝛼 1 ) \ 𝑉 LΘ2 M𝐻 , 𝜌i 𝑉 ′ 𝜎 ′′ , and (𝛼 \ 𝛼 1 ) \ 𝑉 LΘ2 M𝐻 = 𝛼 \ (𝑉 LΘ1 M𝐻 ∪
𝑉 LΘ2 M𝐻 ) = 𝛼 \ 𝑉 LΘ1 ∪ Θ2 M𝐻 , therefore h𝐻, 𝛼 \ 𝑉 LΘ1 ∪ Θ2 M𝐻 , 𝜌i 𝑉 ′ 𝜎 ′′ .
111:78                                                                  C. Zimmerman, J. DiVincenzo, and J. Aldrich


      By induction h𝐻, 𝛼 𝐸 , 𝜌i ⊢frmI 𝜙 1 and h𝐻, 𝛼 𝐸 , 𝜌i ⊢frmI 𝜙 2 . Therefore h𝐻, 𝛼 𝐸 , 𝜌i ⊢frmI 𝜙 1 ∗ 𝜙 2 by
IFrameConjunction, which completes the proof of (16).
   Case 13. SConsumeConjunctionImprecise – 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ⊲ 𝜎 ′′ , R 1 ∪ R 2 ; sep(Θ1 , Θ2 ), Θ1 ∪ Θ2 :
   Similar to case 12, except when showing that h𝐻, 𝛼 𝐸 , 𝜌i  𝜙 1 ∗ 𝜙 2 and when proving (17):
   By induction h𝐻, 𝛼 𝐸 , 𝜌i  𝜙 1 and h𝐻, 𝛼 𝐸 , 𝜌i  𝜙 2 . Thus by lemma 42 h𝐻, 𝑉 ′ LΘ1 M𝐻 , 𝜌i  𝜙 1 ,
h𝐻, 𝑉 ′ LΘ2 M𝐻 , 𝜌i  𝜙 2 , and 𝑉 ′ LΘ1 M𝐻 ∪ 𝑉 ′ LΘ2 M𝐻 ⊆ 𝛼 𝐸 .
   By assumptions h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ sep(Θ1 , Θ2 ). Then by CheckSep 𝑉 ′ LΘ1 M𝐻 ∩ 𝑉 ′ LΘ2 M𝐻 = ∅. Therefore
h𝐻, 𝛼 𝐸 , 𝜌i  𝜙 1 ∗ 𝜙 2 by AssertConjunction.
   By SConsumeConjunctionImprecise (R 1 ∪ R 2 ) ∩ SPerm ≠ ∅. Therefore the premises of (17) do
not hold, therefore it is vacuously true.
   Case 14. SConsumeConditionalA – 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲ 𝜎 ′ , R ∪ R ′ , Θ:
   By SConsumeConditionalA, 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ R and 𝜎 [𝑔 = 𝑔′ ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 1 ⊲ 𝜎 ′, R ′ , Θ where
𝑔 = 𝑔(𝜎) && 𝑡. Let 𝑉1 and 𝑉 ′ be the respective corresponding valuations, with initial valuations 𝑉
 ′

and 𝑉1 , respectively. Then 𝑉 ′ is the corresponding valuation for this case.
   By lemma 35 𝑔(𝜎 ′ ) =⇒ 𝑔′ = 𝑔(𝜎) && 𝑡, thus 𝑉 ′ (𝑔(𝜎) && 𝑡) = 𝑉1 (𝑔(𝜎) && 𝑡) = true. Therefore
h𝐻, 𝛼, 𝜌i 𝑉 𝜎 [𝑔 = 𝑔(𝜎) && 𝑡] and h&&𝑡, 𝐻, 𝛼i 𝑉 𝜎𝐸 [𝑔 = 𝑔(𝜎)]𝜌.
             1                                           1
   By assumptions and lemma 23 h𝐻, 𝛼 𝐸 i ⊢𝑉1 R. Thus h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉1 (𝑡) by lemma 28. Further-
more, 𝑉1 (𝑡) = true since 𝑔(𝜎) && 𝑡 =⇒ 𝑡, thus h𝐻, 𝜌i ⊢ 𝑒 ⇓ true. Finally, h𝐻, 𝛼 𝐸 , 𝜌i  𝜙 1 by
induction. Therefore h𝐻, 𝛼 𝐸 , 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 by AssertIfA.
   Also by induction h𝐻, 𝛼 \ 𝑉 ′ LΘM𝐻 , 𝜌i 𝑉 ′ 𝜎 ′ .
   Finally, h𝐻, 𝛼 𝐸 , 𝜌i ⊢frm 𝜙 1 by induction, and h𝐻, 𝛼 𝐸 , 𝜌i ⊢frm 𝑒 by lemmas 28. As shown before,
h𝐻, 𝜌i ⊢ 𝑒 ⇓ true. Therefore h𝐻, 𝛼 𝐸 , 𝜌i ⊢frm if 𝑒 then 𝜙 1 else 𝜙 2 by FrameIfA, which completes
the proof of (16).
   Now suppose that (R ∪ R ′ ) ∩ SPerm = ∅, thus R ′ ∩ SPerm = ∅. Then by induction h𝐻, 𝛼, 𝜌i  𝜙,
and as before h𝐻, 𝜌i ⊢ 𝑒 ⇓ true, therefore h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 by AssertIfA, which
completes the proof of (17).
   Case 15. SConsumeConditionalB – 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲ 𝜎 ′, R ∪ R ′ , Θ: Similar to case
14.
                                                                                                     


Lemma 44 (Soundness of consume (long form)). Let 𝜙˜ be some speciﬁcation, 𝜎 and 𝜎𝐸 some well-
formed symbolic states such that 𝑔(𝜎) =⇒ 𝑔(𝜎𝐸 ), and h𝐻, 𝛼, 𝜌i some evaluation state such that
h𝐻, 𝛼, 𝜌i 𝑉 𝜎 and h𝐻, 𝛼, 𝜌i 𝑉 𝜎𝐸 .
  If 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ⊲ 𝜎 ′, R, Θ with corresponding valuation 𝑉 ′ , h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ R, and 𝑉 ′ (𝑔(𝜎 ′ )) = true,
then

                             h𝐻, 𝛼 𝐸 , 𝜌i  𝜙˜   and             ˜ h𝐻, 𝜌 i , 𝜌i ′ 𝜎 ′ .
                                                       h𝐻, 𝛼 \ T𝜙U             𝑉


  Proof. Suppose that 𝜎, 𝜎𝐸 ⊢ 𝜙˜ ⊲ 𝜎 ′, R, Θ with corresponding valuation 𝑉 ′ , h𝐻, 𝛼 𝐸 i ⊢𝑉 ′ R, and
𝑉 (𝑔(𝜎 ′ )) = true. Then one of the following cases applies
  ′

  Case 1. 𝜙˜ is imprecise, i.e. 𝜙˜ = ? ∗ 𝜙 for some 𝜙 ∈ Formula:
  Then, since 𝜎, 𝜎𝐸 ⊢ ? ∗ 𝜙 ⊲ 𝜎 ′ , R, Θ, by SConsumeImprecision 𝜎, 𝜎𝐸 [𝜄 = ⊤] ⊢ 𝜙 ⊲ 𝜎0, R, Θ for
some 𝜎0 where 𝜎 ′ = h⊤, 𝑔(𝜎0 ), 𝛾 (𝜎0 ), ∅, ∅i. Let 𝑉 ′ be the corresponding valuation, therefore 𝑉 ′ is
the corresponding valuation for the original derivation.
  Thus by lemma 43, h𝐻, 𝛼 𝐸 , 𝜌i  𝜙, h𝐻, 𝛼 \ 𝑉 ′ LΘM𝐻 , 𝜌i 𝑉 ′ 𝜎0 , and h𝐻, 𝛼 𝐸 , 𝜌i ⊢frmI 𝜙.
  Then h𝐻, 𝛼 𝐸 , 𝜌i ⊢frmE 𝜙 by lemma 3. Therefore h𝐻, 𝛼 𝐸 , 𝜌i  𝜙.
Sound Gradual Verification with Symbolic Execution                                                          111:79


  Also, H(𝜎 ′ ) = H (𝜎 ′ ) = ∅, thus h𝐻, ∅i 𝑉 ′ H(𝜎 ′ ) and h𝐻, ∅i 𝑉 ′ H (𝜎 ′ ). Since h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎0
and 𝛾 (𝜎 ′ ) = 𝛾 (𝜎0 ) and 𝑔(𝜎 ′ ) = 𝑔(𝜎0 ), 𝜌 𝑉 ′ 𝛾 (𝜎 ′ ) and 𝑉 ′ (𝑔(𝜎 ′ )) = true. Therefore h𝐻, ∅, 𝜌i 𝑉 ′ 𝜎 ′ ,
and thus h𝐻, 𝛼 \ T? ∗ 𝜙U h𝐻, 𝜌 i , 𝜌i 𝑉 ′ 𝜎 ′ by lemma 9.
  Case 2. 𝜙˜ is precise, i.e. 𝜙˜ = 𝜙:
   Then by lemma 43 h𝐻, 𝛼 \ 𝑉 ′ LΘM𝐻 , 𝜌i 𝑉 ′ 𝜎 ′ and h𝐻, 𝛼 𝐸 , 𝜌i  𝜙.
   By lemma 42 h𝐻, 𝑉 ′ LΘM𝐻 , 𝜌i  𝜙. Then by lemma 4 T𝜙U h𝐻, 𝛼 i ⊆ 𝑉 ′ LΘM𝐻 , since 𝜙 is a speciﬁca-
tion. Therefore 𝛼 \ 𝑉 ′ LΘM𝐻 ⊆ 𝛼 \ T𝜙U h𝐻, 𝛼 i , thus h𝐻, 𝛼 \ T𝜙U h𝐻, 𝛼 i , 𝜌i 𝑉 ′ 𝜎 ′ .
                                                                                                   

Lemma 45 (Soundness of consume (short form)). Let 𝜙˜ be some speciﬁcation, 𝜎 be some well-
formed symbolic state, h𝐻, 𝛼, 𝜌i some evaluation state, and 𝑉 be some valuation such that
h𝐻, 𝛼, 𝜌i 𝑉 𝜎.
  If 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R with corresponding valuation 𝑉 ′ , h𝐻, 𝛼i ⊢𝑉 ′ R, and 𝑉 ′ (𝑔(𝜎 ′ )) = true then
                            h𝐻, 𝛼, 𝜌i  𝜙˜    and             ˜ h𝐻, 𝜌 i , 𝜌i ′ 𝜎 ′ .
                                                     h𝐻, 𝛼 \ T𝜙U            𝑉

  Proof. Suppose 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, R with corresponding valuation 𝑉 ′ , h𝐻, 𝛼i ⊢𝑉 ′ R, and 𝑉 ′ (𝑔(𝜎 ′ )) =
true. Then 𝜎, 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, R, _ by SConsume. Let 𝑉 ′ be the corresponding valuation, thus 𝑉 ′ is the
corresponding valuation for the original derivation.
  Trivially 𝑔(𝜎) =⇒ 𝑔(𝜎), thus the conditions of lemma 44 are satisﬁed, and thus h𝐻, 𝛼, 𝜌i  𝜙˜
              ˜ h𝐻, 𝜌 i , 𝜌i ′ 𝜎 ′ .
and h𝐻, 𝛼 \ T𝜙U                                                                                      
                            𝑉

Lemma 46 (Progress of consume (long form)). For any heap 𝐻 , 𝜎, 𝜎𝐸 , 𝜙,     ˜ and valuation 𝑉 , if
                                ˜
𝑉 (𝑔(𝜎𝐸 )) = true then 𝜎, 𝜎𝐸 ⊢ 𝜙 ⊲ 𝜎 , _, _ for some 𝜎 such that 𝑉 (𝑔(𝜎 )) = true where 𝑉 ′ is the
                                    ′                 ′           ′    ′

corresponding valuation.
   Proof. By induction on the syntax forms of 𝜙:
   Case 1. 𝑒 ∈ Expr: By lemma 30, 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡. Then one of the following cases
applies to yield 𝜎, 𝜎𝐸 ⊢ 𝑒 ⊲ 𝜎, _, _:
   Case 1(a). 𝑔(𝜎) =⇒ 𝑡: Then SConsumeValue applies.
   Case 1(b). 𝜄 (𝜎) and 𝑔(𝜎) =⇒      Y 𝑡: Then SConsumeValueImprecise applies.
   Case 1(c). ¬𝜄 (𝜎) and 𝑔(𝜎) =⇒      Y 𝑡: Then SConsumeValueFailure applies.
   Case 2. 𝑝 (𝑒) – 𝑝 ∈ Predicate, 𝑒 ∈ Expr:
   By lemma 30, for each 𝑒, 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡. Then one of the following cases applies to
yield 𝜎, 𝜎𝐸 ⊢ 𝑝 (𝑒) ⊲ 𝜎 ′, _, _ where 𝑔(𝜎 ′ ) = 𝑔(𝜎):
   Case 2(a). 𝑝 (𝑡 ′ ) ∈ H(𝜎) and 𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ for some 𝑡 ′ : Then SConsumePredicate applies.
                                                  Ó
   Case 2(b). 𝜄 (𝜎) and  h𝑝, 𝑡 ′ i ∈ H(𝜎) : 𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ : Then SConsumePredicateImprecise
applies.
                                                    Ó
   Case 2(c). ¬𝜄 (𝜎) and  h𝑝, 𝑡 ′ i ∈ H(𝜎) : 𝑔(𝜎) =⇒ 𝑡 == 𝑡 ′ : Then SConsumePredicateFailure
applies.
   Case 3. acc(𝑒.𝑓 ) – 𝑒 ∈ Expr, 𝑓 ∈ Field:
   By lemma 30, 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡𝑒 ⊣ _ for some 𝑡𝑒 . Note that remf and remfp are deﬁned for all inputs.
Then one of the following cases applies to yield 𝜎, 𝜎𝐸 ⊢ acc(𝑒.𝑓 ) ⊲ 𝜎 ′, _, _ where 𝑔(𝜎 ′ ) = 𝑔(𝜎 ′ ):
   Case 3(a). h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) and 𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 for some 𝑡𝑒′ and 𝑡: Then SConsumeAcc applies.
   Case 3(b).  𝑡𝑒′ , 𝑡 : h𝑓 , 𝑡𝑒 , 𝑡i ∈ H(𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 ) and h𝑓 , 𝑡𝑒′ , 𝑡i ∈ H(𝜎) for some 𝑡𝑒′ and
𝑡 where 𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 : Then
SConsumeAccOptimistic applies.
111:80                                                                C. Zimmerman, J. DiVincenzo, and J. Aldrich


     Case 3(c).  𝑡𝑒′ , 𝑡 : h𝑓 , 𝑡𝑒 , 𝑡i ∈ H(𝜎) ∪ H (𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 ) and 𝜄 (𝜎): Then
SConsumeAccImprecise applies.
     Case 3(d).  𝑡𝑒′ , 𝑡 : h𝑓 , 𝑡𝑒 , 𝑡i ∈ H(𝜎) ∪ H (𝜎) ∧ (𝑔(𝜎) =⇒ 𝑡𝑒′ == 𝑡𝑒 ) and ¬𝜄 (𝜎): Then
SConsumeAccFailure applies.
     Case 4. 𝜙 1 ∗ 𝜙 2 – 𝜙 1, 𝜙 2 ∈ Formula
     By induction, 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ⊲ 𝜎 ′, _, _ for some 𝜎 ′ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the
corresponding valuation.
    Then also by induction, 𝜎 ′ , 𝜎𝐸 [𝑔 = 𝑔(𝜎 ′ )] ⊢ 𝜙 2 ⊲ 𝜎 ′′ , _, _ for some 𝜎 ′′ such that 𝑉 ′′ (𝑔(𝜎 ′′ )) =
true where 𝑉 ′′ is the corresponding valuation, with initial valuation 𝑉 ′ . Then one of the following
cases applies to yield 𝜎, 𝜎𝐸 ⊢ 𝜙 1 ∗ 𝜙 2 ⊲ 𝜎 ′′ , _, _:
     Case 4(a). (R 1 ∪ R 2 ) ∩ SPerm ≠ ∅: Then SConsumeConjunctionImprecise applies.
     Case 4(b). (R 1 ∪ R 2 ) ∩ SPerm = ∅: Then SConsumeConjunction applies.
     Case 5. if 𝑒 then 𝜙 1 else 𝜙 2 – 𝑒 ∈ Expr, 𝜙 1, 𝜙 2 ∈ Formula:
     By lemma 30, 𝜎𝐸 ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡. Let 𝑉 ′ be the valuation corresponding to this derivation.
Then since this is a well-typed program, one of the following cases must apply:
     Case 5(a). 𝑉 ′ (𝑡) = true: Let 𝑔′ = 𝑔(𝜎) && 𝑡. Then 𝑉 (𝑔′ ) = true and by induction, 𝜎 [𝑔 =
𝑔 ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 1 ⊲ 𝜎 ′, _, _ for some 𝜎 ′ where 𝑉 ′′ (𝑔(𝜎 ′ )) = true for the corresponding deriva-
  ′

tion 𝑉 ′′ with initial valuation 𝑉 ′ . Then by SConsumeConditionalA, 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲
𝜎 ′ , _, _, and 𝑉 ′′ is the corresponding valuation for this derivation with initial valuation 𝑉 .
     Case 5(b). 𝑉 ′ (𝑡) = false: Let 𝑔′ = 𝑔(𝜎) && ! 𝑡. Then 𝑉 (𝑔′ ) = true and by induction, 𝜎 [𝑔 =
𝑔 ], 𝜎𝐸 [𝑔 = 𝑔′ ] ⊢ 𝜙 2 ⊲ 𝜎 ′, _, _ for some 𝜎 ′ where 𝑉 ′′ (𝑔(𝜎 ′ )) = true for the corresponding deriva-
  ′

tion 𝑉 ′′ with initial valuation 𝑉 ′ . Then by SConsumeConditionalB, 𝜎, 𝜎𝐸 ⊢ if 𝑒 then 𝜙 1 else 𝜙 2 ⊲
𝜎 ′ , _, _, and 𝑉 ′′ is the corresponding valuation for this derivation with initial valuation 𝑉 .
                                                                                                               

                                                                 ˜ and valuation 𝑉 , if 𝑉 (𝑔(𝜎)) =
Lemma 47 (Progress of consume (short form)). For any heap 𝐻 , 𝜎, 𝜙,
               ˜
true then 𝜎 ⊢ 𝜙 ⊲ 𝜎 , _ for some 𝜎 such that 𝑉 (𝑔(𝜎 )) = true where 𝑉 ′ is the corresponding
                   ′              ′            ′    ′

valuation.

  Proof. By lemma 46, 𝜎, 𝜎 ⊢ 𝜙˜ ⊲𝜎 ′ , _, _ for some 𝜎 ′ where 𝑉 ′ (𝑔(𝜎 ′ )) = true. Then by SConsume,
𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , _, and 𝑉 ′ is the corresponding valuation for this derivation.                       

D.6      Progress
Deﬁnition 40. For a derivations Σ ⇀ 𝜎 ⊣ R, Θ, given an initial valuation 𝑉 and heap 𝐻 , the
corresponding valuation is denoted as
                                          𝑉 [Σ ⇀ 𝜎 ⊣ R, Θ | 𝐻 ].
This function is deﬁned as follows, depending on the rule that proves the derivation. Values are
referenced using the respective name from the rule deﬁnition.
 • SGuardInit:
                              𝑉 [init ⇀ h⊥, ∅, ∅, ∅, truei ⊣ ∅, ∅ | 𝐻 ] := 𝑉
 • SGuardSeq:
                                                 ˜ ⇀ 𝜎 ⊣ ∅, ∅ | 𝐻 ] := 𝑉
                                 𝑉 [h𝜎, skip; 𝑠, 𝜙i
 • SGuardAssign:
                                     ˜ ⇀ 𝜎 ⊣ R, ∅ | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R | 𝐻 ]
                    𝑉 [h𝜎, 𝑥 = 𝑒; 𝑠, 𝜙i
Sound Gradual Verification with Symbolic Execution                                                   111:81


 • SGuardAssignField:
                                            ˜ ⇀ 𝜎 ′′ ⊣ R ′ ∪ R ′′ , ∅ | 𝐻 ] :=
                        𝑉 [h𝜎, 𝑥 .𝑓 = 𝑒; 𝑠, 𝜙i
                            𝑉 [𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′ , R ′ | 𝐻 ] [𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ⊲ 𝜎 ′′ , R ′′ | 𝐻 ]
 • SGuardAlloc:
                                                       ˜ ⇀ 𝜎 ⊣ ∅, ∅ | 𝐻 ] := 𝑉
                               𝑉 [h𝜎, 𝑥 = alloc(𝑆); 𝑠, 𝜙i
 • SGuardCall:
                                 ˜ ⇀ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)] ⊣ R ∪ R ′ , rem(𝜎 ′′ , pre(𝑚)) | 𝐻 ] :=
             𝑉 [h𝜎, 𝑦 = 𝑚(𝑒); 𝑠, 𝜙i
                𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R | 𝐻 ] [𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ pre(𝑚) ⊲ 𝜎 ′′ , R ′ | 𝐻 ]
 • SGuardAssert:
                                    ˜ ⇀ 𝜎 ′ ⊣ R, ∅ | 𝐻 ] := 𝑉 [𝜎 ⊢ ? ∗ 𝜙 ⊲ 𝜎 ′, R | 𝐻 ]
                𝑉 [h𝜎, assert 𝜙; 𝑠, 𝜙i
 • SGuardFold:
                                    ˜ ⇀ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)] ⊣ _, ∅ | 𝐻 ] :=
             𝑉 [h𝜎, fold 𝑝 (𝑒); 𝑠, 𝜙i
                𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻 ] [𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡 ]] ⊢ predicate(𝑝) ⊲ 𝜎 ′′ , R ′ | 𝐻 ]
 • SGuardUnfold:
                                                                             Ø
                                                  ˜ ⇀ 𝜎 ′′ ⊣ R ′ ∪
                          𝑉 [h𝜎, unfold 𝑝 (𝑒); 𝑠, 𝜙i                               R, ∅ | 𝐻 ] :=
                              𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R | 𝐻 ] [𝜎 ′ ⊢ 𝑝 (𝑒) ⊲ 𝜎 ′′ , R ′ | 𝐻 ]
 • SGuardIf:
                                                              ˜ ⇀ 𝜎 ′ ⊣ R, ∅ | 𝐻 ] :=
                           𝑉 [h𝜎, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠, 𝜙i
                               𝑉 [𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R | 𝐻 ]
 • SGuardWhile:
              𝑉 [h𝜎, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜′ i ⇀ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′′ )] ⊣ _, _ | 𝐻 ] :=
                 𝑉0 [𝑡 ↦→ 𝑉0 (𝛾 (𝜎 ′ ) (𝑥))] [𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ 𝑡]] ⊢ 𝜙˜ ⊳ 𝜎 ′′ | 𝐻 ]
   where 𝑉0 = 𝑉 [𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R ′ | 𝐻 ].
 • SGuardFinish:
                   𝑉 [h𝜎, skip, 𝜙i  ˜ ⇀ 𝜎 ′ ⊣ R, ∅ | 𝐻 ] := 𝑉 [𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, R | 𝐻 ]

Lemma 48. If h𝐻, 𝛼, 𝜌i  𝜙˜ and h𝐻, 𝛼 \ T𝜙U
                                         ˜ h𝐻, 𝛼 i , 𝜌i
                                                        𝑉
                                                          𝜎, then h𝐻, 𝛼 \𝑉 ′ Lrem(𝜎 ′ , 𝜙˜ ′ )M𝐻 , 𝜌i  𝜙.
                                                                                                        ˜

                                                                                            ˜ h𝐻, 𝜌 i .
  Proof. Let 𝛼𝑉 = 𝑉 ′ Lrem(𝜎 ′ , 𝜙˜ ′ )M𝐻 . By lemma 12 it suﬃces to show that (𝛼 \ 𝛼𝑉 ) ⊆ T𝜙U
               ˜                                                       ˜
By lemma 4 T𝜙U h𝐻, 𝜌 i ⊆ 𝛼, therefore it suﬃces to show that 𝛼𝑉 ∩ T𝜙U h𝐻, 𝜌 i = ∅.
  If pre(𝑚) is completely precise, rem(𝜎 ′ , pre(𝑚)) = ∅, thus 𝛼𝑉 = ∅.
  Otherwise,
            𝛼𝑉 = 𝑉 ′ Lrem(𝜎 ′ , 𝜙˜ ′ )M𝐻
                  = 𝑉 ′ L{h𝑡, 𝑓 i : h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎) ∪ H (𝜎)} ∪ {h𝑝, 𝑡 i : h𝑝, 𝑡i ∈ H(𝜎)}M𝐻
                             Ø                                    Ø
                  =                        𝑉 ′ Lh𝑓 , 𝑡, 𝑡 ′ iM𝐻 ∪      𝑉 Lh𝑝, 𝑡iM𝐻
                      h𝑓 , 𝑡, 𝑡 ′ i ∈H(𝜎 )∪H (𝜎 )                 h𝑝, 𝑡 i ∈H(𝜎 )
                            Ø
                  =                      𝑉 LℎM𝐻
                      ℎ∈H(𝜎 )∪H (𝜎 )
111:82                                                               C. Zimmerman, J. DiVincenzo, and J. Aldrich


But since h𝐻, 𝛼 \𝛼𝑉 , 𝜌i 𝑉 ′ 𝜎 ′ , for each ℎ ∈ H(𝜎) ∪H (𝜎), 𝑉 ′ LℎM𝐻 ∩𝛼 𝐸 = ∅ by lemma 15. Therefore
𝛼𝑉 ∩ 𝛼 𝐸 = ∅.                                                                                      
Theorem 1 (Progress, part 1). Let Γ be some dynamic state validated by Σ and valuation 𝑉 . If Σ ⇀
𝜎 ′ ⊣ R, Θ with corresponding valuation 𝑉 ′ extending 𝑉 , 𝑉 ′ (𝑔(𝜎 ′ )) = true, and h𝐻, 𝛼 (Γ)i ⊢𝑉 ′ R
then
                                     Π ⊢ Γ, 𝑉 ′ LΘM𝐻 (Γ) → Γ ′
for some Γ ′ .
  In other words, if the dynamic state satisﬁes the matching symbolic checks, then dynamic exe-
cution can proceed.
    Proof. We procede by cases on Σ ⇀ 𝜎 ′ ⊣ R, Θ.
    Case 1. SGuardInit: Result is trival by ExecInit.
    Case 2. SGuardSeq: Then Γ = h𝐻, h𝛼, 𝜌, skip; 𝑠i · S ′ i for some 𝐻, 𝛼, 𝜌, 𝑠, S ′ , thus
h𝐻, h𝛼, 𝜌, skip; 𝑠i · S ′ i, 𝑉 ′ L∅M𝐻 → h𝐻, h𝛼, 𝜌, 𝑠i · S ′ i by ExecSeq, and the result is immediate
from ExecStep.
    Case 3. SGuardAssign: Then Γ = h𝐻, h𝛼, 𝜌, 𝑥 = 𝑒; 𝑠i · S ′ i for some 𝐻, 𝛼, 𝜌, S ′ .
    By SGuardAssign 𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R for some 𝑡, 𝜎 ′ , R. Also, 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R | 𝐻 ].
Since Γ corresponds to Σ, by deﬁnition 31 h𝐻, 𝛼, 𝜌i 𝑉 𝜎 (Σ). By assumptions h𝐻, 𝛼i ⊢𝑉 ′ R, and
𝑉 ′ (𝑔(𝜎 ′ )) = true. Then h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 by lemma 26.
   Therefore h𝐻, h𝛼, 𝜌, 𝑥 = 𝑒; 𝑠i · S ′ i, 𝑉 ′ L∅M𝐻 → h𝐻, h𝛼, 𝜌 [𝑥 ↦→ 𝑉 ′ (𝑡)], 𝑠i · S ′ i by ExecAssign,
and the result is immediate from ExecStep.
    Case 4. SGuardAssignField: Then Γ = h𝐻, h𝛼, 𝜌, 𝑥 .𝑓 = 𝑒; 𝑠i · S ′ i for some 𝐻, 𝛼, 𝜌, 𝑥, 𝑓 , 𝑒, 𝑠, S ′ .
    By SGuardAssignField 𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R 1 for some 𝑡, 𝜎 ′, R 1 , and 𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ⊲ 𝜎 ′′ , R 2 for
some 𝜎 ′′ , R 2 . Also, 𝑉 ′ = 𝑉 [𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R 1 | 𝐻 ] [𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ⊲ 𝜎 ′′ , R 2 | 𝐻 ].
    Since Γ corresponds to Σ, by deﬁnition 31 h𝐻, 𝛼, 𝜌i 𝑉 𝜎 (Σ). By assumptions h𝐻, 𝛼i ⊢𝑉 ′ R 1 ∪R 2 ,
thus h𝐻, 𝛼i ⊢𝑉 ′ R 1 and h𝐻, 𝛼i ⊢𝑉 ′ R 2 by lemma 23, and 𝑉 ′ (𝑔(𝜎 ′′ )) = true, thus 𝑉 ′ (𝑔(𝜎 ′ )) = true
by lemma 36.
    Now h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 by lemma 26. Let ℓ = 𝜌 (𝑥), then h𝐻, 𝜌i ⊢ 𝑥 ⇓ 𝜌 (𝑥)
by EvalVar. Finally, h𝐻, 𝛼, 𝜌i  acc(𝑥 .𝑓 ) by lemma 45.
    Let 𝐻 ′ = 𝐻 [hℓ, 𝑓 i ↦→ 𝑉 ′ (𝑡)]. Then h𝐻, h𝛼, 𝜌, 𝑥 .𝑓 = 𝑒; 𝑠i · S ′ i, 𝑉 ′ L∅M𝐻 → h𝐻 ′ , h𝛼, 𝜌, 𝑠i · S ′ i
by ExecAssignField, and the result is immediate from ExecStep.
    Case 5. SGuardAlloc: Then Γ = h𝐻, h𝛼, 𝜌, 𝑥 = alloc(𝑆); 𝑠i · S ′ i for some 𝐻, 𝛼, 𝜌, 𝑥, 𝑆, 𝑠, S ′ .
    Let ℓ = fresh, 𝑇 𝑓 = struct(𝑆), and 𝐻 ′ = 𝐻 [(ℓ, 𝑓 ) ↦→ default(𝑇 )]. Then
h𝐻, h𝛼, 𝜌, 𝑥 = alloc(𝑆); 𝑠i · S ′ i, 𝑉 ′ L∅M𝐻 → h𝐻 ′ , h𝛼, 𝜌, 𝑠i · S ′ i by ExecAlloc, and the result is
immediate from ExecStep.
    Case 6. SGuardCall: Then Γ = h𝐻, h𝛼, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠ii · S for some 𝐻, 𝛼, 𝜌,𝑦, 𝑚, 𝑒, 𝑠, S. Let
𝑥 = params(𝑚).
    By SGuardCall 𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R for some 𝑡, 𝜎 ′ , R, and 𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ pre(𝑚) ⊲ 𝜎 ′′ , R ′
for some 𝜎 ′′ , R ′ .
   Also, by deﬁnition 𝑉 ′ = 𝑉 [𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R | 𝐻 ] [𝜎 ′ [𝛾 = 𝑥 ↦→ 𝑡] ⊢ pre(𝑚) ⊲ 𝜎 ′′ , R ′ | 𝐻 ].
    Since Γ corresponds to Σ, by deﬁnition 31 h𝐻, 𝛼, 𝜌i 𝑉 𝜎 (Σ). By assumptions, 𝑉 ′ (𝑔(𝜎 ′′ )) = true
thus 𝑉 ′ (𝑔(𝜎 ′ )) = true by lemma 36, and h𝐻, 𝛼i ⊢𝑉 ′ R ∪ R ′ , thus h𝐻, 𝛼i ⊢𝑉 ′ R and h𝐻, 𝛼i ⊢𝑉 ′ R ′
by lemma 23.
   Then h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡), h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, and h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ by lemma 26.
   Let 𝛾 ′ = [𝑥 ↦→ 𝑡] and 𝜌 ′ = [𝑥 ↦→ 𝑉 ′ (𝑡)]. Since h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ and 𝜌 ′ 𝑉 ′ 𝛾 ′ by construction,
h𝐻, 𝛼, 𝜌 ′ i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 ′ ].
Sound Gradual Verification with Symbolic Execution                                                           111:83


   Let 𝛼𝑉 = 𝑉 ′ Lrem(𝜎 ′ , pre(𝑚))M𝐻 and 𝛼 𝐸 = Tpre(𝑚)U h𝐻, 𝜌 i .
   As noted before, 𝜎 ′ [𝛾 = 𝛾 ′ ] ⊢ pre(𝑚) ⊲ 𝜎 ′′ , R ′ by SExecCall. Also, 𝑉 ′ (𝑔(𝜎 ′′ )) = true and
h𝐻, 𝛼i ⊢𝑉 ′ R ′ . Therefore h𝐻, 𝛼 \ 𝛼 𝐸 , 𝜌 ′ i 𝑉 ′ 𝜎 ′ and h𝐻, 𝛼, 𝜌i  pre(𝑚) by lemma 45.
   Then h𝐻, 𝛼 \ 𝛼𝑉 , 𝜌i  pre(𝑚) by lemma 48.
   Let 𝛼 ′ = ⌊pre(𝑚)⌋ h𝐻, 𝛼 \𝛼𝑉 , 𝜌 ′ i . Then h𝐻, h𝛼, 𝜌, 𝑦=𝑚(𝑒); 𝑠i·Si, 𝛼𝑉 → h𝐻, h𝛼 ′ , 𝜌 ′, body(𝑚); skipi·
h𝛼 \ 𝛼 ′ , 𝜌, 𝑦 = 𝑚(𝑒); 𝑠i · Si by ExecCallEnter, and the result is immediate from ExecStep.
   Case 7. SGuardAssert: Then Γ = h𝐻, h𝛼, 𝜌, assert 𝜙; 𝑠i · Si for some 𝐻, 𝛼, 𝜌, 𝜙, 𝑠, S.
   By SGuardAssert 𝜎 (Σ) ⊢ ? ∗ 𝜙 ⊲ 𝜎 ′ , R, also 𝑉 ′ = 𝑉 [𝜎 (Σ) ⊢ ? ∗ 𝜙 ⊲ 𝜎 ′ , R | 𝐻 ].
   Since Γ corresponds to Σ, by deﬁnition 31 h𝐻, 𝛼, 𝜌i 𝑉 𝜎 (Σ). Also by assumptions, h𝐻, 𝛼i ⊢𝑉 ′ R,
and 𝑉 ′ (𝑔(𝜎 ′ )) = true. Thus h𝐻, 𝛼, 𝜌i  𝜙 by lemma 45 since ? ∗ 𝜙 is a speciﬁcation.
   Therefore h𝐻, h𝛼, 𝜌, assert 𝜙; 𝑠i · Si, 𝑉 ′ L∅M𝐻 → h𝐻, h𝛼, 𝜌, 𝑠i · Si by ExecAssert, and the
result is immediate from ExecStep.
   Case 8. SGuardFold: Then 𝑠 (Σ) = 𝑠 (Γ) = fold 𝑝 (𝑒) for some 𝑝, 𝑒. Thus ExecFold trivially
applies, and the result is immediate from ExecStep.
   Case 9. SGuardUnfold: Then 𝑠 (Σ) = 𝑠 (Γ) = unfold 𝑝 (𝑒) for some 𝑝, 𝑒. Thus ExecUnfold triv-
ially applies, and the result is immediate from ExecStep.
   Case 10. SGuardIf: Then 𝑠 (Σ) = 𝑠 (Γ) = if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠 for some 𝑒, 𝑠 1, 𝑠 2 , and thus
Γ = h𝐻, h𝛼, 𝜌, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠i · Si for some 𝐻, 𝛼, 𝜌, S.
   By SGuardIf 𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R for some 𝑡, 𝜎 ′, R, and also 𝑉 ′ = 𝑉 [𝜎 (Σ) ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻 ].
   Now by assumptions 𝑉 ′ (𝑔(𝜎 ′ )) = true and h𝐻, 𝛼i ⊢𝑉 ′ R. Then h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) and
h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 by lemma 26.
   Now, since we assume a well-typed program, 𝑉 ′ (𝑡) = true or false. Then either ExecIfA or
ExecIfB applies, and the result is immediate from ExecStep.
   Case 11. SGuardWhile: Then 𝑠 (Σ) = 𝑠 (Γ) = while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ for some 𝑒, 𝜙,          ˜ 𝑠, 𝑠 ′ ,
and thus Γ = h𝐻, h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 i · Si for some 𝐻 , 𝛼, 𝜌, S.
                                                              ′

   Let 𝑥 = modiﬁed(𝑠). By SGuardWhile 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R ′ , 𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ fresh]] ⊢ 𝜙˜ ⊳ 𝜎 ′′ ,
and 𝜎 ′′ ⊢ 𝑒 ↓ 𝑡 ⊣ R ′′ . Then by deﬁnition 40 𝑉 ′ extends the corresponding valuation for these
judgements.
   By assumptions 𝑉 ′ (𝑔(𝜎 ′′ )) = true, thus 𝑉 ′ (𝑔(𝜎 ′ )) = true by lemma 31.
   Also by assumptions h𝐻, 𝛼i ⊢𝑉 ′ R ′ ∪ R ′′ , thus h𝐻, 𝛼i ⊢𝑉 ′ R ′ and h𝐻, 𝛼i ⊢𝑉 ′ R ′′ by lemma 23.
   Therefore h𝐻, 𝛼 \ T𝜙U   ˜ h𝐻, 𝛼 i , 𝜌i ′ 𝜎 ′ and h𝐻, 𝛼, 𝜌i  𝜙. ˜
                                            𝑉
                          ˜ 𝐻 . Then by lemma 48 h𝐻, 𝛼 \ 𝛼,
   Let 𝛼ˆ = 𝑉 ′ Lrem(𝜎 ′, 𝜙)M                                           ˜
                                                                ˆ 𝜌i  𝜙.
   Let 𝑡 be the list of fresh values used in 𝜎 [𝛾 = 𝛾 (𝜎 ) [𝑥 ↦→ fresh]] ⊢ 𝜙˜ ⊳ 𝜎 ′′ when applying
                                                      ′         ′

SGuardWhile. Let 𝛾 ′ = 𝛾 (𝜎 ′ ) [𝑥 ↦→ 𝑡 ]. Then by deﬁnition 40, and since 𝜌                𝛾 (𝜎 ′ ), for each pair
                                                                                       𝑉′
of 𝑥 and 𝑡, 𝑉 ′ (𝛾 ′ (𝑥)) = 𝑉 ′ (𝑡) = 𝑉 ′ (𝛾 (𝜎 ′ ) (𝑥)) = 𝜌 (𝑥).
   Therefore 𝜌 𝑉 ′ 𝛾 ′ , and thus h𝐻, 𝛼 \ T𝜙U       ˜ h𝐻, 𝛼 i , 𝜌i ′ 𝜎 ′ [𝛾 = 𝛾 ′ ].
                                                                  𝑉
   Now by lemma 33 h𝐻, 𝛼, 𝜙i       ˜ ′ 𝜎 ′′ .
                                       𝑉
  Also, as noted before, h𝐻, 𝛼i ⊢𝑉 ′ R ′′ . Therefore h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) by lemma 28.
  Let 𝛼 ′ = T𝜌U h𝐻, 𝛼 \𝛼ˆ i .
  Now, since we assume the program to be properly typed, one of the following subcases apply:
  Case 11(a). 𝑉 ′ (𝑡) = true: Then by ExecWhileSkip h𝐻, h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i ·
Si, 𝛼ˆ → h𝐻, h𝛼 ′ , 𝜌, 𝑠; skipi · h𝛼 \ 𝛼 ′ , 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · Si and the result is
immediate from ExecStep.
  Case 11(b). 𝑉 ′ (𝑡) = false: Then by ExecWhileSkip hΠ, 𝐻 i, h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i·
S → h𝛼,ˆ 𝐻 ih𝛼, 𝜌, 𝑠i · S and the result is immediate from ExecStep.
111:84                                                                     C. Zimmerman, J. DiVincenzo, and J. Aldrich


    Case 12. SGuardFinish: Then 𝑠 (Σ) = 𝑠 (Γ) = skip and thus Γ = h𝐻, h𝛼, 𝜌, skipi · Si for some
𝐻, 𝛼, 𝜌, S.
    By SGuardFinish 𝜎 (Σ) ⊢ 𝜙˜ (Σ) ⊲ 𝜎 ′, R, and 𝑉 ′ = 𝑉 [𝜎 (Σ) ⊢ 𝜙˜ (Σ) ⊲ 𝜎 ′, R | 𝐻 ]. By assumptions,
𝑉 ′ (𝑔(𝜎 ′ )) = true and h𝐻, 𝛼i ⊢𝑉 ′ R. Therefore h𝐻, 𝛼, 𝜌i  𝜙˜ (Σ).
    Since Γ is a valid state, the partial state h𝐻, Si must be validated by Σ and 𝑉 , thus one of the
following subcases must apply:
    Case 12(a). S = nil – then Γ = h𝐻, h𝛼, 𝜌, skipi · nili. Then ExecFinal trivially applies to yield
the result.
    Case 12(b). S = h𝛼 0 , 𝜌 0, 𝑚(𝑒); 𝑠 0 i · S ′ for some 𝛼 0, 𝜌 0, 𝑚, 𝑒, 𝑠 0 , S ′ and 𝜙˜ (Σ) = post(𝑚).
    Since 𝜙˜ (Σ) = post(𝑚), h𝐻, 𝛼, 𝜌i  post(𝑚). Then ExecCallExit applies, and the result is imme-
diate from ExecStep.
    Case 12(c). S = h𝛼 0, 𝜌 0, while 𝑒 invariant 𝜙˜ do 𝑠 0 ; 𝑠 0′ i · S ′ for some 𝛼 0 , 𝜌 0, 𝑒, 𝜙,  ˜ 𝑠 0, 𝑠 ′ , S ′ and
                                                                                                             0
 ˜
𝜙 (Σ) = 𝜙.  ˜
    Since 𝜙˜ (Σ) = post(𝑚), h𝐻, 𝛼, 𝜌i  𝜙.    ˜ Then ExecWhileFinish applies, and the result is immediate
from ExecStep.
                                                                                                                        
Theorem 2 (Progress, part 2). Let Γ be some well-formed dynamic state validated by Σ and valu-
ation 𝑉 . Then if Γ ≠ final,
                                               Σ ⇀ 𝜎 ′, R, Θ
for some 𝜎 ′ , R, Θ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the corresponding valuation extending
𝑉 ′.
   In other words, there is always some matching guard that computes the necessary checks.
   Proof. First, if Γ = init, then SGuardInit applies to yield the desired result.
   Otherwise, Γ = h𝐻, Si for some non-empty stack. Therefore Σ = h𝜎, 𝑠, 𝜙i             ˜ for some 𝜎, 𝑠, and 𝜙˜
such that h𝐻, 𝛼 (Γ), 𝜌 (Γ)i 𝑉 𝜎 and 𝑠 = 𝑠 (Γ).
   Then one of the following cases apply since S is a well-formed stack:
   Case 1. 𝑠 = skip: By lemma 47 𝜎 ⊢ 𝜙˜ ⊲𝜎 ′ , R for some 𝜎 ′ , R such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′
is the corresponding valuation. Then by SGuardFinish Σ ⇀ 𝜎 ′ ⊣ R, ∅ and 𝑉 ′ is the corresponding
valuation for this judgement.
   Case 2. 𝑠 = 𝑠 ′ ; 𝑠 ′′ for some 𝑠 ′ , 𝑠 ′′ : We complete the proof by proving the following statement
by induction on the syntax form of 𝑠 ′ :
   If 𝑠 = 𝑠 ′ ; 𝑠 ′′ then Σ ⇀ 𝜎 ′, R, Θ for some 𝜎 ′ , R, Θ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the
corresponding valuation extending 𝑉 ′ .
   Case 2(a). 𝑠 ′ = 𝑠 1 ; 𝑠 2 : By lemma 20, 𝑠 ′ = 𝑠 1′ ; 𝑠 2′ where 𝑠 1′ is not a sequence statement. Then
𝑠; 𝑠 ′ = 𝑠 1′ ; 𝑠 2′ ; 𝑠 ′ .
   Then the inductive hypothesis applies, which completes the proof.
   Case 2(b). 𝑠 ′ = skip: Then Σ ⇀ 𝜎 ⊣ ∅, ∅ by SGuardSeq.
   Case 2(c). 𝑠 ′ = 𝑥 =𝑒: By lemma 27, 𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′ , R for some 𝜎 ′ and R such that 𝑉1 (𝑔(𝜎 ′ )) = true
for the corresponding valuation 𝑉1 .
   Then Σ ⇀ 𝜎 ′ ⊣ R, ∅ by SGuardAssign. By deﬁnition the corresponding valuation extends 𝑉1 ,
thus 𝑉 ′ (𝑔(𝜎 ′ )) = true.
   Case 2(d). 𝑥 .𝑓 = 𝑒:
   By lemma 27 𝜎 ⊢ 𝑒 ⇓ _ ⊣ 𝜎 ′, R ′ for some 𝜎 ′ and R ′ such that 𝑉1 (𝑔(𝜎 ′ )) = true where 𝑉1 is the
corresponding valuation extending 𝑉 .
   By lemma 47 𝜎 ′ ⊢ acc(𝑥 .𝑓 ) ⊲ 𝜎 ′′ , R ′′ for some 𝜎 ′′ and R ′′ such that 𝑉2 (𝑔(𝜎 ′′ )) = true for
corresponding valuation 𝑉2 , with initial valuation 𝑉1 .
Sound Gradual Verification with Symbolic Execution                                                       111:85


  Then Σ ⇀ 𝜎 ′′ ⊣ R ′ ∪ R ′′ , ∅ by SGuardAssignField. By deﬁnition the corresponding valuation
𝑉 ′ extends 𝑉2 , therefore 𝑉 ′ (𝑔(𝜎 ′′ )) = true.
    Case 2(e). 𝑥 = alloc(𝑆):
    Then Σ ⇀ 𝜎 ⊣ ∅, ∅ by SExecGuardAlloc.
    Case 2(f). 𝑦 = 𝑚(𝑒 1 , · · · , 𝑒𝑛 ):
    Let 𝜎0 = 𝜎 and 𝑉0 = 𝑉 , then for each 𝑒𝑖 , 𝜎𝑖 −1 ⊢ 𝑒 ⇓ 𝑡𝑖 ⊣ 𝜎𝑖 , _ for some 𝜎𝑖 such that 𝑉𝑖 (𝑔(𝜎𝑖 )) =
true for corresponding valuation 𝑉𝑖 , with initial valuation 𝑉𝑖 −1, by lemma 27.
    Let 𝑥 1, · · · , 𝑥𝑛 = params(𝑚). By lemma 47, 𝜎𝑛 [𝛾 = [𝑥𝑖 ↦→ 𝑡𝑖 ]] ⊢ pre(𝑚) ⊲ 𝜎 ′ , _ for some 𝜎 ′ such
that 𝑉 ′ (𝑔(𝜎 ′ )) = true for corresponding valuation 𝑉 ′ , with initial valuation 𝑉𝑛 .
    Then Σ ⇀ 𝜎 ′ [𝛾 = 𝛾 (𝜎)] ⊣ R 1 ∪ · · · ∪ R𝑛 ∪ R ′ , rem(𝜎 ′′ , pre(𝑚)) by SGuardCall and 𝑉 ′ is the
corresponding valuation
    Case 2(g). assert 𝜙:    ˜
    By lemma 47 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , R for some 𝜎 ′ and R where 𝑉 ′ (𝜎 ′ ) = true for the corresponding
valuation 𝑉 ′ .
    Then by SGuardAssert Σ ⇀ 𝜎 ′ ⊣ R, ∅ and 𝑉 ′ is the corresponding valuation.
    Case 2(h). if 𝑒 then 𝑠 1 else 𝑠 2 :
    By lemma 27 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R for some 𝑡, 𝜎 ′ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the
corresponding valuation.
    Then Σ ⇀ 𝜎 ′ ⊣ R, ∅ by SGuardIf and 𝑉 ′ is the corresponding valuation.
    Case 2(i). while 𝑒 invariant 𝜙˜ do 𝑠 for some 𝑒, 𝜙,       ˜ 𝑠:
                             ˜
    By lemma 47 𝜎 ⊢ 𝜙 ⊲ 𝜎 , R for some 𝜎 and R ′ such that 𝑉1 (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the
                                    ′     ′           ′

corresponding valuation.
    Let 𝑥 = modiﬁed(𝑠) and 𝜎 ′′ = 𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 ↦→ fresh]].
    Let 𝑉2 = 𝑉1 [𝑡 ↦→ 𝑉1 (𝛾 (𝜎 ′ ) (𝑥))]. Then 𝑉2 (𝑔(𝜎 ′′ )) = 𝑉1 (𝑔(𝜎 ′ )) = true.
    Then by lemma 34 𝜎 ′′ ⊢ 𝜙˜ ⊳ 𝜎 ′′′ for some 𝜎 ′′′ such that 𝑉3 (𝑔(𝜎 ′′′ )) = true where 𝑉3 is the
corresponding valuation extending 𝑉2 .
    By lemma 30 𝜎 ′′′ ⊢ 𝑒 ↓ 𝑡 ⊣ _ for some 𝑡. Let 𝑉 ′ be the corresponding valuation extending 𝑉3 ,
thus 𝑉 ′ (𝑔(𝜎 ′′′ )) = 𝑉3 (𝑔(𝜎 ′′′ )) = true.
    Then Σ ⇀ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′′′ )] ⊣ R ′ ∪ R ′′ , rem(𝜎 ′ , 𝜙)˜ by SGuardWhile and 𝑉 ′ is the corresponding
valuation.
    Case 2(j). fold 𝑝 (𝑒 1 , · · · , 𝑒𝑛 ):
    Let 𝜎0 = 𝜎 and 𝑉0 = 𝑉 . For each 𝑒𝑖 , 𝜎𝑖 −1 ⊢ 𝑒 ⇓ 𝑡𝑖 ⊣ 𝜎𝑖 , R𝑖 by lemma 27 for some 𝜎𝑖 and R𝑖 such
that 𝑉𝑖 (𝑔(𝜎𝑖 )) = true where 𝑉𝑖 is the corresponding valuation.
    Let 𝑥 1, · · · , 𝑥𝑛 = predicate_params(𝑝). By lemma 47 𝜎𝑛 [𝛾 = [𝑥𝑖 ↦→ 𝑡𝑛 ]] ⊢ predicate(𝑝) ⊲ 𝜎 ′, R ′
for some 𝜎 ′ and R ′ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where 𝑉 ′ is the corresponding valuation extending
𝑉𝑛 .
    Then Σ ⇀ 𝜎 ′ [𝛾 = 𝛾 (𝜎)] ⊣ R 1 ∪ · · · ∪ R𝑛 ∪ R ′ , ∅ by SGuardFold and 𝑉 ′ is the corresponding
valuation.
    Case 2(k). unfold 𝑝 (𝑒 1 , · · · , 𝑒𝑛 ):
    Let 𝜎0 = 𝜎 and 𝑉0 = 𝑉 . For each 𝑒𝑖 , 𝜎𝑖 −1 ⊢ 𝑒 ⇓ 𝑡𝑖 ⊣ 𝜎𝑖 , R𝑖 by lemma 27 for some 𝜎𝑖 and R𝑖 such
that 𝑉𝑖 (𝑔(𝜎𝑖 )) = true where 𝑉𝑖 is the corresponding valuation.
    By lemma 47 𝜎𝑛 ⊢ 𝑝 (𝑒 1, · · · , 𝑒𝑛 ) ⊲ 𝜎 ′ , R ′ for some 𝜎 ′ and R ′ such that 𝑉 ′ (𝑔(𝜎 ′ )) = true where
  ′
𝑉 is the corresponding valuation extending 𝑉𝑛 .
    Then Σ ⇀ 𝜎 ′ ⊣ R 1 ∪ · · · ∪ R𝑛 ∪ R ′ , ∅ by SGuardUnfold and 𝑉 ′ is the corresponding valuation.
                                                                                                             
111:86                                                                             C. Zimmerman, J. DiVincenzo, and J. Aldrich


D.7 Preservation
Lemma 49. Suppose Γ = h𝐻, h𝛼, 𝜌, 𝑠i · Si and Γ ′ = h𝐻, h𝛼 ′ , 𝜌, 𝑠 ′ i · Si.
  If Γ is validated by Σ and 𝑉 , Π ⊢ _, Γ → Γ ′ with valuation 𝑉 ′ , and Π ⊢ Σ → Σ′ for some Σ′ such
that Σ′ corresponds to Γ ′ , 𝜙˜ (Σ′ ) = 𝜙˜ (Σ), and dom(𝛾 (Σ′ )) ⊇ dom(𝛾 (Σ)), then Γ ′ is a valid state.
      Proof. By deﬁnition, it suﬃces to show that Γ ′ is validated by Σ′ and 𝑉 ′ .
      Part 33.1: By assumptions, Σ is reachable and Π ⊢ Σ → Σ′ , thus Σ′ is reachable with valuation
𝑉 . ′

      Part 33.2: By assumptions Σ′ corresponds to Γ ′ with 𝑉 ′ .
      Part 33.3: Since Γ validated by Σ and 𝑉 , the partial state h𝐻, Si is validated by Σ and 𝑉 . Therefore
one of the following cases apply:
      Case 32.1: Then S = nil and trivially the partial state h𝐻, nili is validated by Σ′ and 𝑉 ′ .
      Case 32.2: Then S is of the form h𝛼 ′ , 𝜌 ′, 𝑦=𝑚(𝑒 1 , · · · , 𝑒𝑘 ); 𝑠 ′ i·S ′ and, for some Σ′′ , 𝑉 ′′ , 𝑥 1, · · · , 𝑥𝑘 ,
𝑡 1 , · · · , 𝑡𝑘 , 𝜎0, · · · , 𝜎𝑘 and 𝜎 ′ ,
                              The partial state h𝐻, S ′ i is validated by Σ′′ and 𝑉 ′′ ,
                         Σ′′ is reachable from Π with valuation 𝑉 ′′ ,                    𝑠 (Σ′′ ) = 𝑠 (S),
                                                  𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                     𝜎0 = 𝜎 (Σ′′ ),        𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,      ··· ,    𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                           ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 (𝛾 (Σ) (𝑥𝑖 )) = 𝑉 ′′ (𝑡𝑖 ),
                         𝜎𝑘 ⊢ pre(𝑚) ⊲ 𝜎 ′ , _,           h𝐻, 𝛼 ′ , 𝜌 ′ i 𝑉 ′′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )],     and
                                                        𝜙˜ (Σ) = post(𝑚)
   Now immediately from above,
                              The partial state h𝐻, S ′ i is validated by Σ′′ and 𝑉 ′′ ,
                         Σ′′ is reachable from Π with valuation 𝑉 ′′ ,                    𝑠 (Σ′′ ) = 𝑠 (S),
                                                  𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                                 ′′
                     𝜎0 = 𝜎 (Σ ),          𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,      ··· ,    𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                          𝜎𝑘 ⊢ pre(𝑚) ⊲ 𝜎 ′ , _,           h𝐻, 𝛼, 𝜌i 𝑉 ′′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )],         and

   Also, 𝜌 𝑉 𝛾 (Σ), 𝜌 𝑉 ′ 𝛾 (Σ′ ), and dom(𝛾 (Σ′ )) ⊇ dom(𝛾 (Σ)), and thus
                        ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 ′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝜌 (𝑥𝑖 ) = 𝑉 (𝛾 (Σ) (𝑥𝑖 )) = 𝑉 ′′ (𝑡𝑖 ).
  Also, by assumptions 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = post(𝑚).
  Therefore the partial state h𝐻, h𝛼 ′ , 𝜌 ′, 𝑦 = 𝑚(𝑒 1 , · · · , 𝑒𝑘 ); 𝑠 ′ i · S ′ i is validated by Σ′ and 𝑉 ′ .
  If case 32.3 applies: Then S is of the form h𝜌 ′, 𝛼 ′ , while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ and there
exists some Σ′′ , 𝑉 ′′ , and 𝜎 ′ such that:
                              The partial state h𝐻, S ∗ i is validated by Σ′′ and 𝑉 ′′
                         Σ′′ is reachable from Π with valuation 𝑉 ′′ ,                    𝑠 (Σ′′ ) = 𝑠 (S)
                                      𝜎 (Σ′′ ) ⊢ 𝜙˜ ⊲ 𝜎 ′ , _, h𝐻, 𝛼 ′ , 𝜌 ′ i 𝑉 ′ 𝜎 ′,     and
                                                            𝜙˜ (Σ) = 𝜙˜
  Now 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = 𝜙.
                          ˜ Then, with the conditions listed above, the partial state
h𝐻, h𝜌 , 𝛼 , while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ i is validated by Σ′ and 𝑉 ′ .
      ′   ′
Sound Gradual Verification with Symbolic Execution                                                            111:87


  Therefore Γ ′ is validated by Σ′ .                                                                              
Lemma 50. If h𝐻, 𝛼 \ 𝑉 Lh𝑡, 𝑓 , 𝑡 ′ iM𝐻 , 𝜌i         𝑉
                                                         𝜎, h𝑉 (𝑡), 𝑓 i ∈ 𝛼, and 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ), then
h𝐻, 𝛼, 𝜌i 𝑉 𝜎 [H = H(𝜎); h𝑡, 𝑓 , 𝑡 ′ i].

   Proof. Let 𝜎 ′ = 𝜎 [H = H(𝜎); h𝑡, 𝑓 , 𝑡 ′ i]. We want to show h𝐻, 𝛼, 𝜌i 𝑉 𝜎 ′ .
   By assumptions and lemma 19, it is immediate that h𝐻, 𝛼, 𝜌i 𝑉 𝜎.
   Since the H , 𝛾, and 𝑔 are unchanged in 𝜎 ′ WRT 𝜎, we have h𝐻, 𝛼i 𝑉 H (𝜎 ′ ), 𝜌 𝑉 𝛾 (𝜎 ′ ), and
𝑉 (𝑔(𝜎 ′ )) = true. Thus it suﬃces to show that h𝐻, 𝛼i 𝑉 H(𝜎 ′ ).
   Let ℎ = h𝑡, 𝑓 , 𝑡 ′ i, thus 𝜎 ′ = 𝜎 [H = H(𝜎 ′ ); ℎ].
   We have h𝐻, 𝛼 \ 𝑉 LℎM𝐻 i 𝑉 𝜎. Then by lemma 15,
                                     ∀ℎ ′ ∈ H(𝜎) : 𝑉 Lℎ ′ M𝐻 ∩ 𝑉 LℎM𝐻 = ∅.                                      (18)
  Then for arbitrary ℎ 1, ℎ 2   ∈ H(𝜎 ′ ), if ℎ1 ≠ ℎ 2 one of the following applies:
 • ℎ 1 = ℎ or ℎ 2 = ℎ: WLOG we can assume ℎ 1 = ℎ and thus ℎ 2 ≠ ℎ. Then by (18), 𝑉 Lℎ 1 M𝐻 ∩𝑉 Lℎ 2 M𝐻 =
   ∅.
 • ℎ 1 ≠ ℎ and ℎ 1 ≠ ℎ: Then ℎ 1 ∈ H(𝜎), ℎ 2 ∈ H(𝜎), and h𝐻, 𝛼i 𝑉 H(𝜎), thus 𝑉 Lℎ 1 M𝐻 ∩𝑉 Lℎ 2 M𝐻 = ∅.
  Therefore
                        ∀ℎ 1 , ℎ 2 ∈ H(𝜎 ′ ) : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 Lℎ 1 M𝐻 ∩ 𝑉 Lℎ 2 M𝐻 = ∅.
   Since predicate instances are the same in H(𝜎) and H(𝜎 ′ ), and h𝐻, 𝛼i 𝑉 H(𝜎),
                               ∀ h𝑝, 𝑡i : h𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝).
   Now let h𝑓 , 𝑡, 𝑡 ′ i be an arbitrary ﬁeld instance in H(𝜎 ′ ). Then one of the following applies:
 • h𝑓 , 𝑡, 𝑡 ′ i = ℎ: Then by assumptions 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ) and h𝑉 (𝑡), 𝑓 i ∈ 𝛼.
 • h𝑓 , 𝑡, 𝑡 ′ i ≠ ℎ, and thus h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎): Then 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ) and h𝑉 (𝑡), 𝑓 i ∈ 𝛼 since
   h𝐻, 𝛼i 𝑉 H(𝜎).
  Therefore
                              ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎) : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ) and
                                     ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎) : h𝑉 (𝑡), 𝑓 i ∈ 𝛼.
   Finally, since all requirements have been satisﬁed, h𝐻, 𝛼i 𝑉 H(𝜎 ′ ), which completes the proof.
                                                                                                
Lemma 51. If ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝛼 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) and h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 then h𝐻 ′ , 𝜌i ⊢ 𝑒 ⇓ 𝑣.
   Proof. By induction on h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣:
   Case 1. EvalLiteral – h𝐻, 𝜌i ⊢ 𝑙 ⇓ 𝑙: h𝐻 ′ , 𝜌i ⊢ 𝑙 ⇓ 𝑙 by EvalLiteral.
   Case 2. EvalVar – h𝐻, 𝜌i ⊢ 𝑥 ⇓ 𝜌 (𝑥): h𝐻 ′ , 𝜌i ⊢ 𝑥 ⇓ 𝜌 (𝑥) by EvalVar.
   Case 3. EvalAndA – h𝐻, 𝜌i ⊢ 𝑒 1 && 𝑒 2 ⇓ false:
   By inversion of EvalAndA h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false. Then T𝑒 1 && 𝑒 2 U h𝐻, 𝜌 i = T𝑒 1 U h𝐻, 𝜌 i by deﬁnition.
Thus ∀ hℓ, 𝑓 i ∈ T𝑒 1 U h𝐻, 𝛼 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ), and therefore h𝐻 ′ , 𝜌i ⊢ 𝑒 1 ⇓ false by induction.
   Case 4. EvalAndB – h𝐻, 𝜌i ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑣 2 :
   By inversion of EvalAndB h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true and h𝐻, 𝜌i ⊢ 𝑒 2 ⇓ 𝑣 2 . Now T𝑒 1 && 𝑒 2 U h𝐻, 𝜌 i =
T𝑒 1 U h𝐻, 𝜌 i ∪ T𝑒 2 U h𝐻, 𝜌 i .
   Thus ∀ hℓ, 𝑓 i ∈ T𝑒 1 U h𝐻, 𝛼 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝑒 1 U h𝐻, 𝜌 i ⊆ T𝑒 1 && 𝑒 2 U h𝐻, 𝜌 i . Therefore
h𝐻 ′ , 𝜌i ⊢ 𝑒 1 ⇓ true by induction. Similarly, h𝐻 ′ , 𝜌i ⊢ 𝑒 2 ⇓ 𝑣 2 .
   Therefore h𝐻 ′ , 𝜌i ⊢ 𝑒 1 && 𝑒 2 ⇓ 𝑣 2 by EvalAndB.
   Case 5. EvalOrA – h𝐻, 𝜌i ⊢ 𝑒 1 || 𝑒 2 ⇓ true: Similar to case 3.
111:88                                                                       C. Zimmerman, J. DiVincenzo, and J. Aldrich


   Case 6. EvalOrB – h𝐻, 𝜌i ⊢ 𝑒 1 || 𝑒 2 ⇓ 𝑣 2 : Similar to case 4.
   Case 7. EvalOp – h𝐻, 𝜌i ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑣 1 ⊕ 𝑣 2 :
   By inversion of EvalOp h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ 𝑣 1 and h𝐻, 𝜌i ⊢ 𝑒 2 ⇓ 𝑣 2 . Now T𝑒 1 ⊕ 𝑒 2 U h𝐻, 𝜌 i = T𝑒 1 U h𝐻, 𝜌 i ∪
T𝑒 2 U h𝐻, 𝜌 i .
   Thus ∀ hℓ, 𝑓 i ∈ T𝑒 1 U h𝐻, 𝛼 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝑒 1 U h𝐻, 𝜌 i ⊆ T𝑒 1 && 𝑒 2 U h𝐻, 𝜌 i . Therefore
h𝐻 ′ , 𝜌i ⊢ 𝑒 1 ⇓ 𝑣 1 by induction. Similarly, h𝐻 ′ , 𝜌i ⊢ 𝑒 2 ⇓ 𝑣 2 .
   Therefore h𝐻 ′ , 𝜌i ⊢ 𝑒 1 ⊕ 𝑒 2 ⇓ 𝑒 1 ⊕ 𝑒 2 by EvalOp.
   Case 8. EvalNeg – h𝐻, 𝜌i ⊢ ¬𝑣 ⇓:
   By inversion of EvalNeg h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣. Also, T! 𝑒U h𝐻, 𝜌 i = T𝑒U h𝐻, 𝜌 i by deﬁnition, thus
∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝛼 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ). Therefore h𝐻 ′ , 𝜌i ⊢ 𝑒 ⇓ 𝑣 by induction.
   Therefore h𝐻 ′ , 𝜌i ⊢ ! 𝑒 ⇓ ¬𝑣 by EvalNeg.
   Case 9. EvalField – h𝐻, 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝐻 (ℓ, 𝑓 ):
   By inversion of EvalField h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ. Then T𝑒.𝑓 U h𝐻, 𝜌 i = T𝑒U h𝐻, 𝜌 i ; hℓ, 𝑓 i.
   Thus ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝛼 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝑒U h𝐻, 𝜌 i ⊆ T𝑒.𝑓 U h𝐻, 𝜌 i . Therefore h𝐻 ′ , 𝜌i ⊢
𝑒 ⇓ ℓ by induction.
   Now h𝐻 ′ , 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝐻 ′ (ℓ, 𝑓 ). Also, since hℓ, 𝑓 i ∈ T𝑒.𝑓 U h𝐻, 𝜌 i , 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ). Therefore
h𝐻 ′ , 𝜌i ⊢ 𝑒.𝑓 ⇓ 𝐻 (ℓ, 𝑓 ).
                                                                                                                   
Lemma 52. If ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 then h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒.
    Proof. By induction on h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒:
    Case 1. FrameLiteral – h𝐻, 𝛼, 𝜌i ⊢frm 𝑙: h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑙 by FrameLiteral.
    Case 2. FrameVar – h𝐻, 𝛼, 𝜌i ⊢frm 𝑥: h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑥 by FrameVar.
    Case 3. FrameField – h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.𝑓 :
    By inversion of FrameField h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 and h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ).
    Now since h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ), by inversion of AssertAcc, h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ and hℓ, 𝑓 i ∈ 𝛼. Now
T𝑒.𝑓 U h𝐻, 𝜌 i = T𝑒U h𝐻, 𝜌 i ; hℓ, 𝑓 i by deﬁnition.
    Thus ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝛼 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝑒U h𝐻, 𝜌 i ⊆ T𝑒.𝑓 U h𝐻, 𝜌 i . Therefore h𝐻 ′ , 𝜌i ⊢
𝑒 ⇓ ℓ by lemma 51, and hℓ, 𝑓 i ∈ 𝛼 as noted previously. Now h𝐻 ′ , 𝛼, 𝜌i  acc(𝑒.𝑓 ) by AssertAcc.
    Also, h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 by induction. Therefore h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.𝑓 by FrameField.
    Case 4. FrameOp – h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 ⊕ 𝑒 2 :
    By inversion of FrameOp h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2 .
    Also, T𝑒 1 ⊕𝑒 2 U h𝐻, 𝜌 i = T𝑒 1 U h𝐻, 𝜌 i ∪T𝑒 2 U h𝐻, 𝜌 i by deﬁnition. Thus ∀ hℓ, 𝑓 i ∈ T𝑒 1 U h𝐻, 𝛼 i : 𝐻 ′ (ℓ, 𝑓 ) =
𝐻 (ℓ, 𝑓 ) since T𝑒 1 U h𝐻, 𝜌 i ⊆ T𝑒 1 ⊕ 𝑒 2 U h𝐻, 𝜌 i . Therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 1 by induction. Similarly,
h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 2 .
    Therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 1 ⊕ 𝑒 2 by induction.
    Case 5. FrameOrA – h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2 :
    By inversion of FrameOrA h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ true and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 .
    Now T𝑒 1 || 𝑒 2 U h𝐻, 𝜌 i = T𝑒 1 U h𝐻, 𝜌 i . Thus ∀ hℓ, 𝑓 i ∈ T𝑒 1 U h𝐻, 𝛼 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ). Therefore
h𝐻 ′ , 𝜌i ⊢ 𝑒 1 ⇓ true by lemma 51, and h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 1 by induction.
    Therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2 by FrameOrA.
    Case 6. FrameOrB – h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2 :
    By inversion of FrameOrA h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ false, h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 , and h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 2 .
    Now T𝑒 1 || 𝑒 2 U h𝐻, 𝜌 i = T𝑒 1 U h𝐻, 𝜌 i ∪ T𝑒 2 U h𝐻, 𝜌 i . Thus ∀ hℓ, 𝑓 i ∈ T𝑒 1 U h𝐻, 𝛼 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 )
since T𝑒 1 U h𝐻, 𝜌 i ⊆ T𝑒 1 ||𝑒 2 U h𝐻, 𝜌 i . Therefore h𝐻 ′ , 𝜌i ⊢ 𝑒 1 ⇓ false by lemma 51, and h𝐻 ′ , 𝛼, 𝜌i ⊢frm
𝑒 1 by induction. Similarly, h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 2 .
    Therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 1 || 𝑒 2 by FrameOrB.
    Case 7. FrameAndA – h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 && 𝑒 2 : Similar to case 5.
Sound Gradual Verification with Symbolic Execution                                                         111:89


   Case 8. FrameAndB – h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 1 && 𝑒 2 : Similar to case 6.
   Case 9. FrameNeg – h𝐻, 𝛼, 𝜌i ⊢frm ! 𝑒:
   By inversion of FrameNeg h𝐻, 𝛼, 𝜌i ⊢frm 𝑒. Also, T! 𝑒U h𝐻, 𝜌 i = T𝑒U h𝐻, 𝜌 i . Thus ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝛼 i :
𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ). Therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 by induction.
   Therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frm ! 𝑒 by FrameNeg.
                                                                                                           
                          ˜ h𝐻, 𝛼 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) and h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙˜ then h𝐻 ′ , 𝛼, 𝜌i ⊢frmE
Lemma 53. If ∀ hℓ, 𝑓 i ∈ T𝜙U
˜
𝜙.
    Proof. By induction on h𝐻 ′ , 𝛼, 𝜌i ⊢frmE 𝜙:         ˜
    Case 1. EFrameExpression – h𝐻, 𝛼, 𝜌i ⊢frmE 𝑒:
    By inversion of EFrameExpression h𝐻, 𝛼, 𝜌i ⊢frm 𝑒 and then h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 by assumptions
and lemma 52. Therefore h𝐻, 𝛼, 𝜌i ⊢frmE 𝑒 by EFrameExpression.
    Case 2. EFrameConjunction – h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1 ∗ 𝜙 2 :
    By inversion of EFrameConjunction h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 1 and h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 2 . Also, T𝜙 1 ∗
𝜙 2 U h𝐻, 𝜌 i = T𝜙 1 U h𝐻, 𝜌 i ∪ T𝜙 2 U h𝐻, 𝜌 i by deﬁnition.
                                                                                      ˜ h𝐻, 𝛼 i . Therefore
    Now ∀ hℓ, 𝑓 i ∈ T𝜙 1 U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝜙 1 U h𝐻, 𝛼 i ⊆ T𝜙U
h𝐻 ′ , 𝛼, 𝜌i ⊢frmE 𝜙 1 by induction. Similarly, h𝐻 ′ , 𝛼, 𝜌i ⊢frmE 𝜙 2 .
    Therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frmE 𝜙 1 ∗ 𝜙 2 by EFrameConjunction.
    Case 3. EFramePredicate – h𝐻, 𝛼, 𝜌i ⊢frmE 𝑝 (𝑒):
    By inversion of EFramePredicate h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣, and h𝐻, 𝛼, [𝑥 ↦→ 𝑣]i ⊢frmE
predicate(𝑝), where 𝑥 = predicate_params(𝑝).
                                                               Ð
    Now T𝑝 (𝑒)U h𝐻, 𝜌 i = Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑣 ] i ∪ T𝑒U h𝐻, 𝜌 i .
    Then, for each 𝑒 and corresponding 𝑥, ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝑒U h𝐻, 𝜌 i ⊆
T𝑝 (𝑒)U h𝐻, 𝜌 i . Therefore h𝐻 ′ , 𝜌i ⊢ 𝑒 ⇓ 𝑣 by lemma 51 and h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 by 52.
    Also, ∀ hℓ, 𝑓 i ∈ Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑣] i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ), thus by induction
h𝐻 ′ , 𝛼, [𝑥 ↦→ 𝑣]i ⊢frmE predicate(𝑝).
    Therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frmE 𝑝 (𝑒) by EFramePredicate.
    Case 4. EFrameConditionalA – h𝐻, 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 :
    By inversion of EFrameConditionalA h𝐻, 𝜌i ⊢ 𝑒 ⇓ true, h𝐻, 𝛼, 𝜌i ⊢frm 𝑒, and h𝐻, 𝛼, 𝜌i ⊢frmE
𝜙1.
    Now Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i = T𝑒U h𝐻, 𝜌 i ∪ T𝜙 1 U h𝐻, 𝜌 i .
    Then ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since T𝑒U h𝐻, 𝜌 i ⊆ Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i .
Therefore h𝐻 ′ , 𝜌i ⊢ 𝑒 ⇓ true by lemma 51 and h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 by lemma 52.
    Also, Then ∀ hℓ, 𝑓 i ∈ T𝜙 1 U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) since
T𝜙 1 U h𝐻, 𝜌 i ⊆ Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i . Therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frmE 𝜙 1 by induction.
    Therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 by EFrameConditionalA.
    Case 5. EFrameConditionalB – h𝐻, 𝛼, 𝜌i ⊢frmE if 𝑒 then 𝜙 1 else 𝜙 2 : Similar to case 4.
    Case 6. EFrameAcc – h𝐻, 𝛼, 𝜌i ⊢frmE acc(𝑒.𝑓 ):
    By inversion of EFrameAcc h𝐻, 𝛼, 𝜌i ⊢frm 𝑒.
    Also, T𝑒U h𝐻, 𝜌 i ⊆ Tacc(𝑒.𝑓 )U h𝐻, 𝜌 i by deﬁnition, thus ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ).
Therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frm 𝑒 by lemma 52.
    Thus h𝐻 ′ , 𝛼, 𝜌i ⊢frmE acc(𝑒.𝑓 ) by EFrameAcc.
                                                                                                              
Lemma 54. If h𝐻, 𝛼, 𝜌i  𝜙˜ and ∀ hℓ, 𝑓 i ∈ T𝜙U
                                              ˜ h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) then h𝐻 ′ , 𝛼, 𝜌i  𝜙.
                                                                                                      ˜

                                     ˜
  Proof. By induction on h𝐻, 𝛼, 𝜌i  𝜙.
111:90                                                                   C. Zimmerman, J. DiVincenzo, and J. Aldrich


   Case 1. AssertImprecise – h𝐻, 𝛼, 𝜌i  ? ∗ 𝜙:
   T? ∗ 𝜙U h𝐻, 𝜌 i = T𝜙U h𝐻, 𝜌 i , thus ∀ hℓ, 𝑓 i ∈ T𝜙U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ).
  Also, h𝐻, 𝛼, 𝜌i ⊢frmE 𝜙 by AssertImprecise, therefore h𝐻 ′ , 𝛼, 𝜌i ⊢frmE 𝜙 by lemma 53.
   Finally, h𝐻, 𝛼, 𝜌i  𝜙 by AssertImprecise, therefore h𝐻 ′ , 𝛼, 𝜌i  𝜙 by induction.
   Now h𝐻 ′ , 𝛼, 𝜌i  ? ∗ 𝜙 by AssertImprecise.
   Case 2. AssertValue – h𝐻, 𝛼, 𝜌i  𝑒:
   By AssertValue h𝐻, 𝜌i ⊢ 𝑒 ⇓ true and ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) by assumptions,
therefore h𝐻 ′ , 𝜌i ⊢ 𝑒 ⇓ true by lemma 51. Therefore h𝐻 ′ , 𝛼, 𝜌i  𝑒 by AssertValue.
   Case 3. AssertIfA – h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 :
   By AssertIfA h𝐻, 𝜌i ⊢ 𝑒 ⇓ true, thus Tif 𝑒 then 𝜙 1 else 𝜙 2 U h𝐻, 𝜌 i = T𝑒U h𝐻, 𝜌 i ∪ T𝜙 1 U h𝐻, 𝜌 i .
   Now ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) and h𝐻, 𝜌i ⊢ 𝑒 ⇓ true thus h𝐻 ′ , 𝜌i ⊢ 𝑒 ⇓ true by
lemma 51.
  Also ∀ hℓ, 𝑓 i ∈ T𝜙 1 U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ), and h𝐻, 𝛼, 𝜌i  𝜙 1 by AssertIfA, therefore
h𝐻 ′ , 𝛼, 𝜌i  𝜙 1 by induction.
  Therefore h𝐻 ′ , 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 by AssertIfA.
   Case 4. AssertIfB – h𝐻, 𝛼, 𝜌i  if 𝑒 then 𝜙 1 else 𝜙 2 : Similar to case 3.
   Case 5. AssertAcc – h𝐻, 𝛼, 𝜌i  acc(𝑒.𝑓 ):
   By inversion of AssertAcc h𝐻, 𝜌i ⊢ 𝑒 ⇓ ℓ. Thus Tacc(𝑒.𝑓 )U h𝐻, 𝜌 i = T𝑒U h𝐻, 𝜌 i ; hℓ, 𝑓 i.
   Now ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) thus h𝐻 ′ , 𝜌i ⊢ 𝑒 ⇓ ℓ by lemma 51.
  Also, hℓ, 𝑓 i ∈ 𝛼 by inversion of AssertAcc. Therefore h𝐻 ′ , 𝛼, 𝜌i  acc(𝑒.𝑓 ) by AssertAcc.
   Case 6. AssertConjunction – h𝐻, 𝛼, 𝜌i  𝜙 1 ∗ 𝜙 2 :
   By inversion of AssertConjunction h𝐻, 𝛼 1 , 𝜌i  𝜙 1 and h𝐻, 𝛼 2 , 𝜌i  𝜙 2 for some 𝛼 1, 𝛼 2 such
that 𝛼 1 ∪ 𝛼 2 ⊆ 𝛼 and 𝛼 1 ∩ 𝛼 2 = ∅.
  Also, T𝜙 1 ∗ 𝜙 2 U h𝐻, 𝜌 i = T𝜙 1 U h𝐻, 𝜌 i ∪ T𝜙 2 U h𝐻, 𝜌 i . Therefore ∀ hℓ, 𝑓 i ∈ T𝜙 1 U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) =
𝐻 (ℓ, 𝑓 ) and thus h𝐻 ′ , 𝛼 1, 𝜌i  𝜙 1 by induction. Similarly, h𝐻 ′ , 𝛼 2, 𝜌i  𝜙 2 .
   Now h𝐻 ′ , 𝛼, 𝜌i  𝜙 1 ∗ 𝜙 2 by AssertConjunction.
   Case 7. AssertPredicate – h𝐻, 𝛼, 𝜌i  𝑝 (𝑒):
   By inversion of AssertPredicate h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣 and h𝐻, 𝛼, [𝑥 ↦→ 𝑣]i  predicate(𝑝) where 𝑥 =
predicate_params(𝑝).
                                                               Ð
  Also, T𝑝 (𝑒)U h𝐻, 𝛼 i = Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑣 ] i ∪ T𝑒U h𝐻, 𝜌 i .
   Now for each 𝑒 and corresponding 𝑥, ∀ hℓ, 𝑓 i ∈ T𝑒U h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ). Therefore
h𝐻 ′ , 𝛼i ⊢ 𝑒 ⇓ 𝑣 by lemma 51.
   Now ∀ hℓ, 𝑓 i ∈ Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑣 ] i : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ). Therefore h𝐻 ′ , 𝛼, [𝑥 ↦→ 𝑣]i 
predicate(𝑝) by induction.
  Therefore h𝐻 ′ , 𝛼, 𝜌i  𝑝 (𝑒) by AssertPredicate.
                                                                                                                    
Lemma 55. If h𝐻, 𝛼, 𝜌i  𝜙˜ for some speciﬁcation 𝜙˜ and ∀ hℓ, 𝑓 i ∈ 𝛼 : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) then
               ˜
h𝐻 ′ , 𝛼, 𝜌i  𝜙.
   Proof. By assumptions and lemma 4 T𝜙U           ˜ h𝐻, 𝜌 i ⊆ 𝛼. Therefore ∀ hℓ, 𝑓 i ∈ T𝜙U
                                                                                         ˜ h𝐻, 𝜌 i : 𝐻 ′ (ℓ, 𝑓 ) =
                                                 ˜
𝐻 (ℓ, 𝑓 ) since hℓ, 𝑓 i ∈ 𝛼 =⇒ hℓ, 𝑓 i ∈ T𝜙U h𝐻, 𝜌 i .
   Therefore h𝐻 ′ , T𝜙U ˜ h𝐻, 𝜌 i , 𝜌i  𝜙˜ by lemma 54. Then h𝐻 ′ , 𝛼, 𝜌i  𝜙˜ by lemma 9 since T𝜙U ˜ h𝐻, 𝜌 i ⊆
𝛼.                                                                                                               
Lemma 56. If h𝐻, 𝛼, 𝜌i 𝑉 𝜎 and ∀ hℓ, 𝑓 i ∈ 𝛼 : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ) then h𝐻 ′ , 𝛼, 𝜌i 𝑉 𝜎.
   Proof. From the assumptions, clearly 𝜌 𝑉 𝛾 (𝜎), thus it suﬃces to show that h𝐻 ′ , 𝛼i 𝑉 H(𝜎)
and h𝐻 ′ , 𝛼i 𝑉 H (𝜎).
Sound Gradual Verification with Symbolic Execution                                                       111:91


  Let H = H(𝜎). From assumptions, clearly h𝐻, 𝛼i 𝑉 H. Therefore

                                    ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ )                        (19)
                                                  ′
                                       ∀ h𝑓 , 𝑡, 𝑡 i ∈ H : h𝑉 (𝑡), 𝑓 i ∈ 𝛼                                (20)
                            ∀ h𝑝, 𝑡 i ∈ H : h𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝)                           (21)
                           ∀ℎ 1 , ℎ 2 ∈ H2 : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 Lℎ 1 M𝐻 ∩ 𝑉 Lℎ 2 M𝐻 = ∅                       (22)

  Let h𝑓 , 𝑡, 𝑡 ′ i be an arbitrary ﬁeld value in H. Then by (19) 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ). Also, by (20)
h𝑉 (𝑡), 𝑓 i ∈ 𝛼, thus by our initial assumptions 𝐻 ′ (𝑉 (𝑡), 𝑓 ) = 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ). Therefore

                                   ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H : 𝐻 ′ (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ).                      (23)

  let h𝑝, 𝑡i be an arbitrary predicate instance in H. Then by (21) h𝐻, 𝛼, [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝).
Since predicate(𝑝) is a speciﬁcation, and ∀ hℓ, 𝑓 i ∈ 𝛼 : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ), then
h𝐻 ′ , 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]i  predicate(𝑝) by lemma 55. Therefore

                           ∀ h𝑝, 𝑡i ∈ H : h𝐻 ′ , 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]i  predicate(𝑝).                       (24)

  Therefore by (23), (20), (24), and (22), h𝐻 ′ , 𝛼i 𝑉 H.
  Let H = H (𝜎). From assumptions, clearly h𝐻, 𝛼i 𝑉 H . Therefore

                                   ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ )                         (25)
                                                  ′
                                       ∀ h𝑓 , 𝑡, 𝑡 i ∈ H : h𝑉 (𝑡), 𝑓 i ∈ 𝛼                                (26)

  Let h𝑓 , 𝑡, 𝑡 ′ i be an arbitrary ﬁeld value in H . Then by (25) 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ). Also, by (26)
h𝑉 (𝑡), 𝑓 i ∈ 𝛼, thus by our initial assumptions 𝐻 ′ (𝑉 (𝑡), 𝑓 ) = 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ). Therefore

                                  ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H : 𝐻 ′ (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ).                       (27)

  Therefore by (27) and (26), h𝐻 ′ , 𝛼i 𝑉 H .                                                                

Lemma 57. If h𝐻, h𝛼, 𝜌, 𝑠i · Si is a well-formed state, the partial state h𝐻, Si is validated by Σ
and 𝑉 , and 𝐻 ′ = 𝐻 [hℓ, 𝑓 i ↦→ 𝑣] for some ℓ, 𝑓 , and 𝑣 such that hℓ, 𝑓 i ∈ 𝛼 or ℓ is a fresh value
unused in S, then the partial state h𝐻 ′ , Si is validated by Σ and 𝑉 .

   Proof. For some 𝑛, let S = h𝛼𝑛 , 𝜌𝑛 , 𝑠𝑛 i · . . . · h𝛼 1 , 𝜌 1, 𝑠 1 i · nil.
   If hℓ, 𝑓 i ∈ 𝛼: h𝐻, h𝛼, 𝜌, 𝑠i · Si is a well-formed state, 𝛼, 𝛼𝑛 , · · · , 𝛼 1 are all disjoint. Thus, since
hℓ, 𝑓 i ∈ 𝛼, for all 1 ≤ 𝑖 ≤ 𝑛, hℓ, 𝑓 i ∉ 𝛼𝑖 .
   If ℓ is fresh: Then for all 1 ≤ 𝑖 ≤ 𝑛, hℓ, 𝑓 i ∉ 𝛼𝑖 since ℓ is not referenced in S.
   Therefore, for all 1 ≤ 𝑖 ≤ 𝑛, hℓ, 𝑓 i ∉ 𝛼𝑖 .
   Let S0 = nil, and for all 1 ≤ 𝑖 ≤ 𝑛 let S𝑖 = h𝛼𝑖 , 𝜌𝑖 , 𝑠𝑖 i · S𝑖 −1 .
   We prove by induction that, if 0 ≤ 𝑖 ≤ 𝑛 and h𝐻, S𝑖 i is validated by some Σ and 𝑉 , the partial
state h𝐻 ′ , S𝑖 i is validated by Σ and 𝑉 . This is suﬃcient to prove the main result, since S𝑛 = S and
h𝐻, Si is validated by Σ and 𝑉 .
   Suppose 0 ≤ 𝑖 ≤ 𝑛 and h𝐻, S𝑖 i is validated by some Σ and 𝑉 .
   Case 32.1: Then S𝑖 = nil (and thus 𝑖 = 0), and trivially h𝐻 ′ , nili is validated by Σ and 𝑉 .
111:92                                                                        C. Zimmerman, J. DiVincenzo, and J. Aldrich


  Case 32.2: Then S𝑖 = h𝜌𝑖 , 𝛼𝑖 , 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠i · S𝑖 −1 for some 𝑦, 𝑚, 𝑘, 𝑒 1 , · · · , 𝑒𝑘 , 𝑠, and there
exists some Σ′ , 𝑉 ′ , 𝑥 1, · · · , 𝑥𝑘 , 𝑡 1 , · · · , 𝑡𝑘 , 𝜎0, · · · , 𝜎𝑘 and 𝜎 ′ such that:

                           The partial state h𝐻, S𝑖 −1 i is validated by Σ′ and 𝑉 ′,
                        Σ′ is reachable from Π with valuation 𝑉 ′ ,                𝑠 (Σ′ ) = 𝑠 (S𝑖 )
                                               𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                               ′
                    𝜎0 = 𝜎 (Σ ),     𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1 , _,     ··· ,   𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                      ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 (𝛾 (Σ𝑖 ) (𝑥𝑖 )) = 𝑉 ′ (𝑡𝑖 ),
                       𝜎𝑘 ⊢ pre(𝑚) ⊲ 𝜎 ′ , _,        h𝐻, 𝛼𝑖 , 𝜌𝑖 i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )],       and
                                                   𝜙˜ (Σ𝑖 ) = post(𝑚).

  By induction we can assume that if 0 ≤ 𝑖 − 1 ≤ 𝑛 and h𝐻, S𝑖 −1 i is validated by some Σ and 𝑉 ,
the partial state h𝐻 ′ , S𝑖 −1 i is validated by Σ and 𝑉 .
  Since S𝑖 ≠ nil, 1 ≤ 𝑖 ≤ 𝑛, thus 0 ≤ 𝑖 − 1 ≤ 𝑛. Also, in this case the partial state h𝐻, S𝑖 −1 i is
validated by Σ′ and 𝑉 ′ . Therefore we can conclude that

                          The partial state h𝐻 ′ , S𝑖 −1 i is validated by Σ′ and 𝑉 ′ .

Also, immediately from above,

                        Σ′ is reachable from Π with valuation 𝑉 ′ ,                𝑠 (Σ′ ) = 𝑠 (S𝑖 )
                                               𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                               ′
                    𝜎0 = 𝜎 (Σ ),     𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1 , _,     ··· ,   𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                      ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 (𝛾 (Σ𝑖 ) (𝑥𝑖 )) = 𝑉 ′ (𝑡𝑖 ),
                                           𝜎𝑘 ⊢ pre(𝑚) ⊲ 𝜎 ′, _, and
                                                𝜙˜ (Σ𝑖 ) = post(𝑚).

It remains to be shown that h𝐻 ′ , 𝛼𝑖 , 𝜌𝑖 i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )]. But as noted before, hℓ, 𝑓 i ∉ 𝛼𝑖 (since
1 ≤ 𝑖 ≤ 𝑛 in this case). Thus ∀ hℓ ′ , 𝑓 ′ i ∈ 𝛼𝑖 : 𝐻 ′ (ℓ ′ , 𝑓 ′ ) = 𝐻 (ℓ ′ , 𝑓 ′ ). Therefore by lemma 56,

                                         h𝐻 ′ , 𝛼𝑖 , 𝜌𝑖 i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )].

  Therefore h𝐻 ′ , S𝑖 i is validated by Σ and 𝑉 .
  Case 32.3: Then S𝑖 = h𝜌𝑖 , 𝛼𝑖 , while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S𝑖 −1 for some 𝑒, 𝜙,
                                                                                       ˜ 𝑠, and 𝑠 ′ , and
                    ′     ′       ′
there exists some Σ , 𝑉 , and 𝜎 such that:

                           The partial state h𝐻, S𝑖 −1 i is validated by Σ′ and 𝑉 ′
                        Σ′ is reachable from Π with valuation 𝑉 ′               𝑠 (Σ′ ) = 𝑠 (S𝑖 )
                           𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , _,     h𝐻, 𝛼𝑖 , 𝜌𝑖 i 𝑉 ′ 𝜎 ′,   and 𝜙˜ (Σ𝑖 ) = 𝜙˜

  By induction we can assume that if 0 ≤ 𝑖 − 1 ≤ 𝑛 and h𝐻, S𝑖 −1 i is validated by some Σ and 𝑉 ,
the partial state h𝐻 ′ , S𝑖 −1 i is validated by Σ and 𝑉 .
  Since S𝑖 ≠ nil, 1 ≤ 𝑖 ≤ 𝑛, thus 0 ≤ 𝑖 − 1 ≤ 𝑛. Also, in this case the partial state h𝐻, S𝑖 −1 i is
validated by Σ′ and 𝑉 ′ . Therefore we can conclude that

                          The partial state h𝐻 ′ , S𝑖 −1 i is validated by Σ′ and 𝑉 ′ .
Sound Gradual Verification with Symbolic Execution                                                     111:93


Also, immediately from above,
                       Σ′ is reachable from Π with valuation 𝑉 ′ 𝑠 (Σ′ ) = 𝑠 (S𝑖 )
                                   𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, _, and 𝜙˜ (Σ𝑖 ) = 𝜙˜
It remains to be shown that h𝐻 ′ , 𝛼𝑖 , 𝜌𝑖 i 𝑉 ′ 𝜎 ′ . But as noted before, hℓ, 𝑓 i ∉ 𝛼𝑖 (since 1 ≤ 𝑖 ≤ 𝑛 in
this case). Thus ∀ hℓ ′ , 𝑓 ′ i ∈ 𝛼𝑖 : 𝐻 ′ (ℓ ′ , 𝑓 ′ ) = 𝐻 (ℓ ′ , 𝑓 ′ ). Therefore by lemma 56,
                                                  h𝐻 ′ , 𝛼𝑖 , 𝜌𝑖 i 𝑉 ′ 𝜎 ′ .
  Therefore h𝐻 ′ , S𝑖 i is validated by Σ and 𝑉 .
                                                                                                           
                                          ˜ 𝐻 ⊆ 𝛼.
Lemma 58. If h𝐻, 𝛼, 𝜌i 𝑉 𝜎 then 𝑉 Lrem(𝜎, 𝜙)M

  Proof. If 𝜙˜ is completely precise, then
                                                ˜ 𝐻 = 𝑉 L∅M𝐻 = ∅ ⊆ 𝛼.
                                      𝑉 Lrem(𝜎, 𝜙)M
  Otherwise,
                                 ˜ 𝐻 = 𝑉 L{h𝑓 , 𝑡i : h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎) ∪ H (𝜎)} ∪
                      𝑉 Lrem(𝜎, 𝜙)M
                                                 {h𝑝, 𝑡i : h𝑝, 𝑡i ∈ H(𝜎)}M𝐻
                                           = {h𝑉 (𝑡), 𝑓 i : h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎) ∪ H (𝜎)} ∪
                                                   Ø
                                                            Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 (𝑡 ) ] i
                                                  h𝑝, 𝑡 i ∈H(𝜎 )

  For any h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎) ∪ H (𝜎), h𝑉 (𝑡), 𝑓 i ∈ 𝛼 since h𝐻, 𝛼i            𝑉
                                                                                    H(𝜎) and h𝐻, 𝛼i 𝑉 H (𝜎).
Therefore
                           {h𝑉 (𝑡), 𝑓 i : h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎) ∪ H (𝜎)} ⊆ 𝛼.
  Also, for any h𝑝, 𝑡i ∈ H(𝜎), h𝐻, 𝛼, [𝑥 ↦→ 𝑡 ]i  predicate(𝑝) where 𝑥 = predicate_params(𝑝);
therefore Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 (𝑡 ) ] i ⊆ 𝛼 by 4. Thus
                                Ø
                                           Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 (𝑡 ) ] i ⊆ 𝛼.
                                h𝑝, 𝑡 i ∈H(𝜎 )

                                                     ˜ 𝐻 ⊆ 𝛼.
  Therefore, by the previous calculations, 𝑉 Lrem(𝜎, 𝜙)M                                                   

Lemma 59. Let 𝜙˜ be some speciﬁcation, 𝛼ˆ = 𝑉 Lrem(𝜎, 𝜙)M  ˜ 𝐻 and 𝛼 ′ = ⌊𝜙⌋
                                                                           ˜ h𝐻, 𝛼 \𝛼,ˆ 𝜌 i .
              ˜
  If h𝐻, 𝛼 \ T𝜙U h𝐻, 𝜌 i , 𝜌i 𝑉 𝜎 and h𝐻, 𝛼 \ 𝛼,     ˜                ′
                                              ˆ 𝜌i  𝜙, then h𝐻, 𝛼 \ 𝛼 , 𝜌i 𝑉 𝜎.

  Proof. If 𝜙˜ is completely precise, then
                                                                  ˜ 𝐻
                                                  𝛼ˆ = 𝑉 Lrem(𝜎, 𝜙)M
                                                    = 𝑉 L∅M𝐻
                                                    =∅
                                                        ˜ h𝐻, 𝛼 \𝛼,ˆ 𝜌 i
                                                 𝛼 ′ = ⌊𝜙⌋
                                                         ˜ h𝐻, 𝜌 i .
                                                     = T𝜙U
And thus
                                    ˜ h𝐻, 𝜌 i , 𝜌i
                          h𝐻, 𝛼 \ T𝜙U                𝜎 =⇒ h𝐻, 𝛼 \ 𝛼 ′ , 𝜌i 𝑉 𝜎.
                                                   𝑉
111:94                                                                      C. Zimmerman, J. DiVincenzo, and J. Aldrich


   Otherwise, 𝜙˜ is not completely precise. Now,
                             ˜ 𝐻
             𝛼ˆ = 𝑉 Lrem(𝜎, 𝜙)M
                 = 𝑉 L{h𝑓 , 𝑡i : h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎) ∪ H (𝜎)} ∪ {h𝑝, 𝑡i : h𝑝, 𝑡i ∈ H(𝜎)}M𝐻
                 = {h𝑉 (𝑡), 𝑓 i : h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎) ∪ H (𝜎)} ∪
                         Ø
                                  Tpredicate(𝑝)U h𝐻, [𝑡↦→𝑉 (𝑡 ) ] i
                      h𝑝, 𝑡 i ∈H(𝜎 )

                  ˜ h𝐻, 𝜌 i . Since h𝐻, 𝛼 ∗ i
   Let 𝛼 ∗ = 𝛼 \ T𝜙U                            H(𝜎)𝜌,
                                              𝑉
                                   ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎) : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ )                              (28)
                        ∀ h𝑝, 𝑡 i ∈ H(𝜎) : h𝐻, 𝛼 ∗, [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝)                                  (29)
                           ∀ℎ 1, ℎ 2 ∈ H : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 Lℎ 1 M𝐻 ∩ 𝑉 Lℎ 2 M𝐻 = ∅                                 (30)
where 𝑥 = predicate_params(𝑝).
  Note that by our calculation of 𝛼,
                                  ˆ
                                       ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H(𝜎) : h𝑉 (𝑡), 𝑓 i ∈ 𝛼.
                                                                              ˆ                                   (31)
Also, by deﬁnition Tpredicate(𝑝)U h𝐻, [𝑥↦→𝑉 (𝑡 ) ] i ⊆ 𝛼ˆ for each h𝑝, 𝑡 i ∈ H(𝜎) when
𝑥 = predicate_params(𝑝), thus by (29) and lemma 12
                         ∀ h𝑝, 𝑡i ∈ H(𝜎) : h𝐻, 𝛼,
                                               ˆ [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝)                                     (32)
where 𝑥 = predicate_params(𝑝).
 Therefore, by (28), (31), (32), and (30),
                                                       ˆ 𝑉 H(𝜎).
                                                   h𝐻, 𝛼i
   Since h𝐻, 𝛼 ∗ i 𝑉 H (𝜎)𝜌,
                                  ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H (𝜎) : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ).
By our calculation of 𝛼,
                      ˆ
                                       ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H (𝜎) : h𝑉 (𝑡), 𝑓 i ∈ 𝛼ˆ .
Therefore
                                                      ˆ 𝑉 H (𝜎).
                                                  h𝐻, 𝛼i
                       ˜ h𝐻, 𝜌 i , 𝜌i
  Also, since h𝐻, 𝛼 \ T𝜙U               𝜎,
                                      𝑉

                                       𝜌 𝑉 𝛾 (𝜎)      and 𝑉 (𝑔(𝜎)) = true.
Therefore
                                           ˆ 𝜌i 𝑉 𝜎.
                                      h𝐻, 𝛼,
   Now, since h𝐻, 𝛼 \ 𝛼,     ˜ by lemma 5 ⌊𝜙⌋
                      ˆ 𝜌i  𝜙,             ˜ h𝐻, 𝛼 \𝛼,ˆ 𝜌 i ⊆ 𝛼 \ 𝛼.
                                                                   ˆ Thus
                                                    ˜ h𝐻, 𝛼 \𝛼,ˆ 𝜌 i ⊆ 𝛼 \ 𝛼ˆ
                                            𝛼 ′ = ⌊𝜙⌋
                                           𝛼 \ 𝛼 ′ ⊇ 𝛼 \ (𝛼 \ 𝛼)
                                                              ˆ = 𝛼 ∩ 𝛼ˆ
                     ˜ h𝐻, 𝜌 i ⊆ 𝛼 by lemma 58, thus 𝛼 ∩ 𝛼ˆ = 𝛼ˆ and then 𝛼 \ 𝛼 ′ ⊇ 𝛼.
  Finally, 𝛼ˆ ⊆ 𝛼 \ T𝜙U                                                             ˆ
  Therefore by lemma 19
                                         h𝐻, 𝛼 \ 𝛼 ′ , 𝜌i 𝑉 𝜎.
                                                                                                                     
Sound Gradual Verification with Symbolic Execution                                                  111:95


Lemma 60. Let h𝐻, Si be some dynamic state validated by Σ and valuation 𝑉 for some program
Π. If Σ ⇀ 𝜎 ′ ⊣ R, Θ with 𝑉 ′ = 𝑉 [Σ ⇀ 𝜎 ′ ⊣ R, Θ | 𝐻 ], 𝑉 ′ (𝑔(𝜎 ′ )) = true, h𝐻, 𝛼 (S)i ⊢𝑉 ′ R, and
h𝐻, Si, 𝑉 ′ LΘM𝐻 → h𝐻 ′ , S ′ i then Γ ′ is a valid state.
   Note: This is a simpliﬁcation of theorem 3, restricted to the particular case of a normal program
step (in contrast to a step from init or to final).

     Proof. We proceed by cases on h𝐻, Si, 𝑉 ′ LΘM𝐻 → h𝐻 ′ , S ′ i.
     Case 1. ExecSeq: We have

                        h𝐻, h𝛼, 𝜌, skip; 𝑠i · S ∗ i, 𝑉 ′ LΘM𝐻 → h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i.

                                                                       ˜ for some 𝜎, 𝜙,
     Since the initial state is validated by Σ and𝑉 , Σ = h𝜎, skip; 𝑠, 𝜙i            ˜ where h𝐻, 𝛼, 𝜌i
                                                                                                       𝑉
𝜎.
     Now 𝜎 (Σ) ⊢ skip; 𝑠 → 𝑠 ⊣ 𝜎 by SExecSeq. Therefore Π ⊢ Σ → Σ′ by SVerifyStep where
            ˜
Σ′ = h𝜎, 𝑠, 𝜙i.
   Now, by lemma 49, it suﬃces to show that Σ′ corresponds to h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i (with valuation
𝑉 ).
   Since 𝜎 (Σ′ ) = 𝜎, we have h𝐻, 𝛼, 𝜌i 𝑉 𝜎 (Σ′ ), and 𝑠 (Σ′ ) = 𝑠 by deﬁnition. Therefore Σ′ corre-
sponds to h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i, which completes the proof.
   Case 2. ExecAssign: We have

                   h𝐻, h𝛼, 𝜌, 𝑥 = 𝑒; 𝑠i · S ∗ i, 𝑉 ′ LΘM𝐻 → h𝐻, h𝛼, 𝜌 [𝑥 ↦→ 𝑣], 𝑠i · S ∗ i
                                           where       h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣

                                                                  ˜ for some 𝜎, 𝜙˜ where h𝐻, 𝛼, 𝜌i
     Since the initial state is validated by Σ, Σ = h𝜎, 𝑥 = 𝑒; 𝑠, 𝜙i                                 𝜎.
                                                                                                   𝑉
     The only guard that applies is SGuardAssign, so we have, for some 𝜎 ′ , 𝑡:

                                                      ˜ ⇀ 𝜎 ⊣ R, Θ
                                        h𝜎, 𝑥 = 𝑒; 𝑠, 𝜙i
                     where 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R        and (by assumptions) h𝐻, 𝜌i ⊢𝑉 ′ R.

where 𝑉 ′ is the corresponding valuation, extending 𝑉 .
  Let 𝜎 ′′ = 𝜎 [𝛾 = 𝛾 (𝜎) [𝑥 ↦→ 𝑡]], then 𝜎 ⊢ 𝑥 = 𝑒; 𝑠 → 𝑠 ⊣ 𝜎 ′′ by SExecAssign.
                      ˜ Then Π ⊢ Σ → Σ′ by SVerifyStep, thus Σ′ is reachable from Π.
  Let Σ′ = h𝜎 ′′ , 𝑠, 𝜙i.
 We want to show that h𝐻, h𝛼, 𝜌 [𝑥 ↦→ 𝑣], 𝑠i · S ∗ i is validated by Σ′ with valuation 𝑉 ′ .
  Part 33.1: As shown above, Σ′ is reachable from Π with valuation 𝑉 ′ .
  Part 33.2: By lemma 26 h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡), therefore 𝑉 ′ (𝑡) = 𝑣. Also, 𝜌 𝑉 𝛾 (𝜎), thus 𝜌 [𝑥 ↦→
𝑣] 𝑉 ′ 𝛾 (𝜎) [𝑥 ↦→ 𝑉 ′ (𝑡)]. Rewriting using deﬁnitions, we get 𝜌 [𝑥 ↦→ 𝑣] 𝑉 ′ 𝛾 (𝜎 ′′ ).
     Also by lemma 26, h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ . Thus, since 𝛾 is the only component changed from 𝜎 ′ to 𝜎 ′′
and 𝜌 [𝑥 ↦→ 𝑣] 𝑉 ′ 𝛾 (𝜎 ′′ ), h𝐻, 𝛼, 𝜌 [𝑥 ↦→ 𝑣]i 𝑉 ′ 𝜎 ′′ .
  Also, by deﬁnition Σ′ = h𝜎 ′′ , 𝑠, 𝜙i.˜
  Therefore Σ corresponds to h𝐻, h𝛼, 𝜌 [𝑥 ↦→ 𝑣], 𝑠i · S ∗ i.
                 ′

  Part 33.3: Since the initial state is validated by Σ and 𝑉 , the partial state h𝐻, S ∗ i is validated by
Σ and valuation 𝑉 . Therefore one of 32.1, 32.2, 32.3 applies. We want to show that the partial state
h𝐻, S ∗ i is validated by Σ′ and valuation 𝑉 ′ .
 • Case 32.1: Then S ∗ = nil and trivially h𝐻, nili is validated by Σ′ and valuation 𝑉 ′ .
111:96                                                                             C. Zimmerman, J. DiVincenzo, and J. Aldrich


 • Case 32.2: Then S ∗ = h𝜌 0, 𝛼 0, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠 0 i · S0 for some 𝜌 0 , 𝛼 0 , 𝑦, 𝑚, 𝑘, 𝑒 1 , · · · , 𝑒𝑘 , 𝑠 0 ,
   S0 . Also, there is some Σ0 , 𝑉0 , 𝑥 1, · · · , 𝑥𝑘 , 𝑡 1 , · · · , 𝑡𝑘 and 𝜎0, · · · , 𝜎𝑘 , 𝜎 ′ such that
                              The partial state h𝐻, S0 i is validated by Σ0 and 𝑉0,
                         Σ0 is reachable from Π with valuation 𝑉0,                   𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                                 𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                    𝜎0 = 𝜎 (Σ0 ),      𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,       ··· ,     𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                             ′                                 ′
                        𝜎𝑘 ⊢ pre(𝑚) ⊲ 𝜎 , _,           h𝐻, 𝛼 0, 𝜌 0 i 𝑉 𝜎 [𝛾 = 𝛾 (𝜎0 )],          and
                                                                           0

                                        ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 (𝛾 (Σ) (𝑥𝑖 )) = 𝑉0 (𝑡𝑖 ),
                                                 𝜙˜ (Σ) = post(𝑚).
    We want to show that the partial state h𝐻, h𝜌 0, 𝛼 0, 𝑦 = 𝑚(𝑒 1 , · · · , 𝑒𝑘 ); 𝑠i · S0 i is validated by Σ′
    and valuation 𝑉 ′ . Immediately from above we can conclude that
                              The partial state h𝐻, S0 i is validated by Σ0 and 𝑉0,
                         Σ0 is reachable from Π with valuation 𝑉0,                   𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                                 𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                𝜎0 = 𝜎 (Σ0 ),      𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,       ··· ,     𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,      and
                            𝜎𝑘 ⊢ pre(𝑚) ⊲ 𝜎 ′, _,           h𝐻, 𝛼 0, 𝜌 0 i 𝑉 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )].
                                                                               0

    Also, the frame h𝛼, 𝜌, 𝑥 = 𝑒; 𝑠i must be executing the body of 𝑚, since it is in the stack
    immediately above the frame that contains 𝑦 =𝑚(𝑒 1, · · · , 𝑒𝑘 ). Therefore, since 𝑥 1, · · · , 𝑥𝑘 are all
    parameters of 𝑚, 𝑦 must be distinct from all of 𝑥 1, · · · , 𝑥𝑘 , since we do not allow assignment to
    parameters in a well-formed program. Thus
                  ∀1 ≤ 𝑖 ≤ 𝑘 : 𝑉 ′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉 ′ ((𝛾 (𝜎) [𝑥 ↦→ 𝑡]) (𝑥𝑖 )) = 𝑉 ′ (𝛾 (𝜎) (𝑥𝑖 ))
                                                       = 𝑉 ′ (𝛾 (Σ) (𝑥𝑖 )) = 𝑉 (𝛾 (Σ) (𝑥𝑖 ))
                                                       = 𝑉0 (𝑡𝑖 ).
    Finally, 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) by deﬁnition, thus
                                         𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = post(𝑚).
   Therefore the partial state h𝐻, S ∗ i is validated by Σ′ and 𝑉 ′ in this case.
 • Case 32.3: Then S ∗ = h𝜌 0 , 𝛼 0, while 𝑒 0 invariant 𝜙˜0 do 𝑠 0 ; 𝑠 0′ i · S0 for some 𝜌 0 , 𝛼 0 , 𝑒, 𝜙˜0 , 𝑠 0 ,
   𝑠 0′ , S0 , and there exists some Σ0 , 𝑉0 , and 𝜎0′ such that:
                              The partial state h𝐻, S0 i is validated by Σ0 and 𝑉0
                         Σ0 is reachable from Π with valuation 𝑉0 𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                    𝜎0 ⊢ 𝜙˜0 ⊲ 𝜎0′ , _,      h𝐻, 𝛼 0, 𝜌 0 i 𝑉 𝜎0′       and
                                                                               0

                                                          𝜙˜ (Σ) = 𝜙˜0 .
    Now, by deﬁnition of Σ′′ , 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = 𝜙˜0 . Therefore, using the other assumptions given
    above, the partial state h𝐻, S ∗ i is validated by Σ′ and 𝑉 ′ in this case.
   Therefore deﬁnition part 33.3 is satisﬁed.
   Therefore all parts of deﬁnition 33 are satisﬁed. Thus h𝐻, h𝛼, 𝜌 [𝑥 ↦→ 𝑣], 𝑠i · S ∗ i is validated by
Σ with valuation 𝑉 ′ .
 ′

   Case 3. ExecAssignField:
Sound Gradual Verification with Symbolic Execution                                                               111:97


   We have
                   h𝐻, h𝛼, 𝜌, 𝑥 .𝑓 = 𝑒; 𝑠i · S ∗ i, 𝑉 ′ LΘM𝐻 → h𝐻 ′ , h𝛼, 𝜌, 𝑠i · S ∗ i                           (33)
                   where      h𝐻, 𝜌i ⊢ 𝑥 ⇓ ℓ,           h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣,          h𝐻, 𝛼, 𝜌i  acc(𝑥 .𝑓 ),          (34)
                                                                  ′
                              h𝐻, 𝛼, 𝜌i ⊢frm 𝑒,          and 𝐻 = 𝐻 [hℓ, 𝑓 i ↦→ 𝑣].                                (35)
                                                                ˜ for some 𝜎, 𝜙˜ where h𝐻, 𝛼, 𝜌i
Since the initial state is validated by Σ, Σ = h𝜎, 𝑥 .𝑓 = 𝑒; 𝑠, 𝜙i                                 𝜎.
                                                                                                 𝑉
  The only guard rule that applies is SGuardAssign, so we have
                                    ˜ ⇀ 𝜎 ⊣ R ′ ∪ R ′′ , ∅
                   h𝜎, 𝑥 .𝑓 = 𝑒; 𝑠, 𝜙i                                                                            (36)
                                               ′    ′       ′                          ′′       ′′
                   where 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 , R ,              𝜎 ⊢ acc(𝑥 .𝑓 ) ⊲ 𝜎 , R                                  (37)
                                                                      ′     ′′              ′         ′′
                   and (by assumptions)            h𝐻, 𝛼i ⊢𝑉 ′ R ∪ R ,                 𝑉 (𝑔(𝜎 )) = true           (38)
   Furthermore, since 𝑔(𝜎 ′′ ) =⇒ 𝜎 ′ by lemma 36, and by lemma 23,
                       𝑉 ′ (𝑔(𝜎 ′ )) = true,       h𝐻, 𝛼i ⊢𝑉 ′ R ′ ,      and          h𝐻, 𝛼i ⊢𝑉 ′ R ′′ .
   Now, by SExecAssignField,
                   𝜎 ⊢ 𝑥 .𝑓 = 𝑒; 𝑠 → 𝑠 ⊣ 𝜎 ′′′          where 𝜎 ′′′ = 𝜎 ′′ [H = H′ ],                      and
                                                                      ′           ′′                 ′′
                                                                 H = H(𝜎 ); h𝛾 (𝜎 ) (𝑥), 𝑓 , 𝑡i.
                        ˜ We want to show that h𝐻 ′ , h𝛼, 𝜌, 𝑠i · S ∗ i is validated by Σ′ and 𝑉 ′ .
   Let Σ′ = h𝜎 ′′′ , 𝑠, 𝜙i.
   Part 33.1: By SVerifyStep, Π ⊢ Σ → Σ′ . Therefore Σ′ is reachable from program Π with valuation
 ′
𝑉 .
   Part 33.2: We want to show that Σ′ corresponds to h𝐻 ′ , h𝛼, 𝜌, 𝑠i · S ∗ i. Since Σ′ = h𝜎 ′′′ , 𝑠, _i by
construction, it suﬃces to show that h𝐻 ′ , 𝛼, 𝜌i 𝑉 ′ 𝜎 ′′′ .
   By lemma 26, h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ . By lemma 45, h𝐻, 𝛼 \ Tacc(𝑥 .𝑓 )U h𝐻, 𝜌 i , 𝜌i 𝑉 ′ 𝜎 ′′ .
  Since 𝜌 𝑉 𝛾 (𝜎), 𝜌 (𝑥) = 𝑉 (𝛾 (𝜎) (𝑥)) = 𝑉 ′ (𝛾 (𝜎) (𝑥)). Also, h𝐻, 𝜌i ⊢ 𝑥 ⇓ 𝜌 (𝑥) by EvalVar and
h𝐻, 𝜌i ⊢ 𝑥 ⇓ ℓ by (34), thus
                                            𝑉 ′ (𝛾 (𝜎) (𝑥)) = 𝜌 (𝑥) = ℓ.
Also, 𝛾 (𝜎 ′′ ) = 𝛾 (𝜎) by lemmas 25 and 39. Thus h𝐻, 𝜌i ⊢ 𝑥 ⇓ 𝑉 ′ (𝛾 (𝜎 ′′ ) (𝑥)). Therefore
Tacc(𝑥 .𝑓 )U h𝐻, 𝜌 i = {hℓ, 𝑓 i} = {h𝑉 ′ (𝛾 (𝜎 ′′ ) (𝑥)), 𝑓 i} = 𝑉 ′ Lh𝛾 (𝜎 ′′ ) (𝑥), 𝑓 , 𝑡 ′ iM𝐻 . Now,

                                 h𝐻, 𝛼 \ 𝑉 ′ Lh𝛾 (𝜎 ′′ ) (𝑥), 𝑓 , 𝑡 ′ iM𝐻 , 𝜌i 𝑉 ′ 𝜎 ′′ .

  Also, 𝑣 = 𝑉 ′ (𝑡) by lemma 26, thus 𝐻 ′ (𝑉 ′ (𝛾 (𝜎 ′′ ) (𝑥)), 𝑓 ) = 𝐻 ′ (ℓ, 𝑓 ) = 𝑣 = 𝑉 ′ (𝑡). Now by lemma
50,
                                                   h𝐻 ′ , 𝛼, 𝜌i 𝑉 ′ 𝜎 ′′′
which is suﬃcient to show that Σ′ corresponds to h𝐻 ′ , h𝛼, 𝜌, 𝑠i · S ∗ i.
  Part 33.3:
  By (34) h𝐻, 𝛼, 𝜌i  acc(𝑥 .𝑓 ). This assertion must be given by AssertAcc, therefore hℓ, 𝑓 i ∈ 𝛼.
  Now we show by induction that all partial states are validated, in other words we want to show
that the partial state h𝐻 ′ , S ∗ i is validated by Σ′ . By assumptions, h𝐻, S ∗ i is validated by Σ with
valuation 𝑉 . Also, by lemma 57, h𝐻 ′ , S ∗ i is validated by Σ with 𝑉 .
  Thus, one of the following cases apply:
 • Case 32.1: Then S ∗ = nil, and trivially h𝐻 ′ , nili is validated by Σ′ and 𝑉 .
111:98                                                                     C. Zimmerman, J. DiVincenzo, and J. Aldrich


 • Case 32.2: Then S ∗ = h𝜌, 𝛼, 𝑦 = 𝑚(𝑒 1 , · · · , 𝑒𝑘 ); 𝑠i · S0 for some 𝜌, 𝛼, 𝑦, 𝑚, 𝑒 1 , · · · , 𝑒𝑘 , and there
   exists some Σ0 , 𝑉0 , 𝑥 1, · · · , 𝑥𝑘 , 𝑡 1 , · · · , 𝑡𝑘 , 𝜎0 , · · · , 𝜎𝑘 , and 𝜎0′ such that:
                           The partial state h𝐻 ′ , S0 i is validated by Σ0 and 𝑉0,
                       Σ0 is reachable from Π with valuation 𝑉0,             𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                           𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                   𝜎0 = 𝜎 (Σ0 ),    𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,    ··· ,    𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                     ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 (𝛾 (Σ) (𝑥𝑖 )) = 𝑉0 (𝑡𝑖 ),
                            𝜎𝑘 [𝛾 = [𝑥 1 ↦→ 𝑡 1 , · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]] ⊢ pre(𝑚) ⊲ 𝜎0′ , _,
                                     h𝐻 ′ , 𝛼, 𝜌i 𝑉 𝜎0′ [𝛾 = 𝛾 (𝜎0 )],      and
                                                    0

                                                 𝜙˜ (Σ) = post(𝑚).
    We want to show that the partial state h𝐻 ′ , h𝜌, 𝛼, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠i · S0 i is validated by Σ′ .
    From above,
                           The partial state h𝐻 ′ , S0 i is validated by Σ0 and 𝑉0,
                       Σ0 is reachable from Π with valuation 𝑉0,             𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                           𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                   𝜎0 = 𝜎 (Σ0 ),    𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,    ··· ,    𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                        𝜎𝑘 [𝛾 = [𝑥 1 ↦→ 𝑡 1 , · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]] ⊢ pre(𝑚) ⊲ 𝜎0′ , _,    and
                                            ′
                                          h𝐻 , 𝛼, 𝜌i 𝑉 𝜎0′ [𝛾 = 𝛾 (𝜎0 )].
                                                       0

   𝛾 (Σ′ ) = 𝛾 (𝜎 ′′′ ) = 𝛾 (𝜎 ′′ ) by deﬁnition. Also, 𝛾 (𝜎 ′′ ) = 𝛾 (𝜎 ′ ) = 𝛾 (𝜎 ′ ) by lemmas 25 and 39. Also,
   𝑉 ′ extends 𝑉 . Thus
                           ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 ′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉 (𝛾 (Σ) (𝑥𝑖 )) = 𝑉0 (𝑡𝑖 ).
    Also, by deﬁnition
                                       𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = post(𝑚).
   Therefore the partial state h𝐻 ′ , S ∗ i is validated by Σ′ .
 • Case 32.3: Then S ∗ = h𝜌, 𝛼, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S0 for some 𝜌, 𝛼, 𝑒, 𝜙,
                                                                                        ˜ 𝑠, 𝑠 ′ , and S0 ,
                                           ′
   and there exists some Σ0 , 𝑉0 , and 𝜎0 such that:
                            The partial state h𝐻 ′ , S0 i is validated by Σ and 𝑉
                       Σ0 is reachable from Π with valuation 𝑉0 𝑠 (Σ0 ) = 𝑠 (S ∗ )
                               𝜎 (Σ0 ) ⊢ 𝜙˜ ⊲ 𝜎0′ , _,   and       h𝐻 ′ , 𝛼, 𝜌i 𝑉 𝜎0′
                                                                                  0

                                                     𝜙˜ (Σ) = 𝜙˜
   Now, 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) by deﬁnition, thus 𝜙˜ (Σ′ ) = 𝜙.
                                                        ˜ Therefore the partial state h𝐻 ′ , S ∗ i is vali-
   dated by Σ .′

Now we have shown that Σ′ corresponds to the resulting state, and therefore 𝛾 ′ is validated by Σ′ .
  Case 4. ExecAlloc: We have
             h𝐻, h𝛼, 𝜌, 𝑥 = alloc(𝑆); 𝑠i · S ∗ i, 𝑉 ′ LΘM𝐻 → h𝐻 ′ , h𝛼 ′ , 𝜌 [𝑥 ↦→ ℓ], 𝑠i · S ∗ i
             where 𝑇 𝑓 = struct(𝑆),             ℓ = fresh,    𝐻 ′ = 𝐻 [hℓ, 𝑓 i ↦→ default(𝑇 )],
                       𝛼 ′ = 𝛼 ∪ {hℓ, 𝑓 i}
Sound Gradual Verification with Symbolic Execution                                                                        111:99


                                                                       ˜ for some 𝜎, 𝜙˜ where h𝐻, 𝛼, 𝜌i
      Since the initial state is validated by Σ, Σ = h𝜎, 𝑥 = alloc; 𝑠, 𝜙i                               𝑉
𝜎.
      By SExecAlloc
                  𝜎 ⊢ 𝑥 = alloc(𝑆); 𝑠 → 𝑠 ⊣ 𝜎 ′, where H(𝜎 ′ ) = H(𝜎); h𝑡, 𝑓 , default(𝑇 )i,
                                                                        𝛾 (𝜎 ′ ) = 𝛾 (𝜎) [𝑥 ↦→ 𝑡],          and
                                                                        𝑡 = fresh .
                     ˜ and 𝑉 ′ = 𝑉 [𝑡 ↦→ ℓ]. We want to show that h𝐻 ′ , h𝛼 ′ , 𝜌 [𝑥 ↦→ ℓ], 𝑠i · S ∗ i is
Let Σ′ = h𝜎 ′ , 𝑠, 𝜙i,
                ′
validated by Σ with 𝑉 .
   Part 33.1: By SVerifyStep, Π ⊢ Σ → Σ′ , and all fresh values added to Σ′ are deﬁned in 𝑉 ′ .
Therefore, Σ′ is reachable from Π with valuation 𝑉 ′ .
   Part 33.2: We want to show that Σ′ corresponds to 𝐻 ′ h𝛼 ′ , 𝜌 [𝑥 ↦→ ℓ], 𝑠i · S ∗ . By deﬁnition 𝑠 (Σ′ ) =
𝑠 and 𝜎 (Σ′ ) = 𝜎 ′ , thus it suﬃces to show h𝐻 ′ , 𝛼 ′ , 𝜌 [𝑥 ↦→ ℓ]i 𝑉 ′ 𝜎 ′ .
      By assumptions, 𝜌 𝑉 𝛾 (𝜎). Also,
                   𝑉 ′ (𝛾 (𝜎 ′ ) (𝑥)) = 𝑉 ′ ((𝛾 (𝜎) [𝑥 ↦→ 𝑡]) (𝑥)) = 𝑉 ′ (𝑡) = ℓ = (𝜌 [𝑥 ↦→ ℓ]) (𝑥).
Therefore
                                                 𝜌 [𝑥 ↦→ ℓ] 𝑉 ′ 𝛾 (𝜎) [𝑥 ↦→ 𝑡].
  By assumptions, h𝐻, 𝛼, 𝜌i 𝑉 𝜎. Since 𝑉 ⊆ 𝑉 ′ , h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎. Since ℓ is a fresh value, ℓ ∉ 𝛼.
Thus
                              ∀ hℓ, 𝑓 i ∈ 𝛼 : 𝐻 ′ (ℓ, 𝑓 ) = 𝐻 (ℓ, 𝑓 ).
Thus by lemma 50, h𝐻 ′ , 𝛼, 𝜌i 𝑉 ′ 𝜎. Also, since 𝛼 ⊆ 𝛼 ′ , by lemma 19 h𝐻 ′ , 𝛼 ′ , 𝜌i 𝑉 ′ 𝜎.
   Let h𝑓 ′, 𝑡 ′ , 𝑡 ′′ i ∈ H(𝜎 ′ ). If h𝑓 ′ , 𝑡 ′ , 𝑡 ′′ i ∈ H(𝜎), then since h𝐻 ′ , 𝛼 ′ , 𝜌i 𝑉 ′ 𝜎, 𝐻 ′ (𝑉 ′ (𝑡 ′ ), 𝑓 ′ ) =
𝑉 (𝑡 ′′ ) and h𝑉 ′ (𝑡 ′ ), 𝑓 ′ i ∈ 𝛼 ′ .
  ′

   Otherwise, 𝑡 ′ = 𝑡 and 𝑓 ′ = 𝑓 for some 𝑇 𝑓 ∈ struct(𝑆), and thus 𝑡 ′′ = default(𝑇 ). Now
𝐻 (𝑉 ′ (𝑡 ′ ), 𝑓 ′ ) = 𝐻 ′ (𝑉 ′ (𝑡), 𝑓 ) = 𝐻 ′ (ℓ, 𝑓 ) = default(𝑇 ) = 𝑡 ′′ .
   Therefore
                   ∀ h𝑓 ′, 𝑡 ′ , 𝑡 ′′ i ∈ H(𝜎 ′ ) : 𝐻 ′ (𝑉 ′ (𝑡 ′ ), 𝑓 ′ ) = 𝑉 ′ (𝑡 ′′ ) and h𝑉 ′ (𝑡 ′ ), 𝑓 ′ i ∈ 𝛼 ′ .
      Also, since h𝐻 ′ , 𝛼 ′ , 𝜌i 𝑉 ′ 𝜎 and ∀ h𝑝, 𝑡 i ∈ H(𝜎 ′ ) : h𝑝, 𝑡 i ∈ H(𝜎),

                             ∀ h𝑝, 𝑡 i ∈ H(𝜎 ′ ) : h𝐻 ′ , 𝛼 ′ , [𝑥 ↦→ 𝑉 (𝑡)]i  predicate(𝑝)
where 𝑥 = predicate_params(𝑝).
   Let ℎ 1 , ℎ 2 ∈ H(𝜎 ′ ) and suppose ℎ 1 ≠ ℎ 2 . If ℎ 1 ∈ H(𝜎) and ℎ 2 ∈ H(𝜎), then in this case 𝑉 ′ Lℎ 1 M𝐻 ′ ∩
𝑉 Lℎ 2 M𝐻 ′ = ∅ since h𝐻 ′ , 𝛼 ′ , 𝜌i 𝑉 ′ 𝜎.
 ′

   Otherwise, WLOG ℎ 1 = h𝑡, 𝑓1 , default(𝑇1 )i for some 𝑇1 𝑓1 ∈ struct(𝑆). Thus
                 𝑉 ′ Lℎ 1 M𝐻 ′ = 𝑉 ′ Lh𝑡, 𝑓1 , default(𝑇1 )iM𝐻 ′                       ℎ 1 = h𝑡, 𝑓1 , default(𝑇1 )i
                                      ′
                              = {h𝑉 (𝑡), 𝑓1 i}                                                                    defn.
                              = {hℓ, 𝑓1 i}                                                                    defn. 𝑉 ′
If ℎ 2 ∈ H(𝜎), then
                            𝑉 ′ Lℎ 2 M𝐻 ′ = 𝑉 Lℎ 2 M𝐻                                 𝑉 ⊆ 𝑉 ′, 𝐻 ⊆ 𝐻 ′
                                          ⊆𝛼                                                  Lemma 14
Now hℓ, 𝑓1 i ∉ 𝛼 since ℓ is a fresh value. Therefore 𝑉 ′ Lℎ 1 M𝐻 ′ ∩ 𝑉 ′ Lℎ 2 M𝐻 ′ = ∅ in this case.
111:100                                                                                C. Zimmerman, J. DiVincenzo, and J. Aldrich


  Otherwise, ℎ 2 = h𝑡, 𝑓2, default(𝑇2 )i for some 𝑇2 𝑓2 ∈ struct(𝑆). Then 𝑓1 ≠ 𝑓2 since ℎ 1 ≠ ℎ 2 .
Therefore
             𝑉 ′ Lℎ 1 M𝐻 ′ ∩ 𝑉 ′ Lℎ 2 M𝐻 ′ = 𝑉 ′ Lh𝑡, 𝑓1 , default(𝑇1 )iM𝐻 ′ ∩ 𝑉 ′ Lh𝑡, 𝑓2 , default(𝑇2 )iM𝐻 ′
                                        = {h𝑉 ′ (𝑡), 𝑓1 i} ∩ {h𝑉 ′ (𝑡), 𝑓2 i}
                                        =∅
  Therefore,
                                  ∀ℎ 1 , ℎ 2 ∈ H(𝜎 ′ ) : 𝑉 ′ Lℎ 1 M𝐻 ′ ∩ 𝑉 ′ Lℎ 2 M𝐻 ′ = ∅.
  Now, since we have shown all requirements, we can conclude that

                                                       h𝐻 ′ , 𝛼 ′ i 𝑉 ′ H(𝜎 ′ ).

  Finally, since H is the only component that diﬀers between 𝜎 ′ and 𝜎, h𝐻 ′ , 𝛼 ′ , 𝜌i 𝑉 ′ 𝜎, 𝜌 [𝑥 ↦→
ℓ] 𝑉 ′ 𝛾 (𝜎) [𝑥 ↦→ 𝑡], and h𝐻 ′ , 𝛼 ′ i 𝑉 ′ H(𝜎 ′ ),

                                  h𝐻 ′ , 𝛼 ′ , 𝜌 [𝑥 ↦→ ℓ]i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎) [𝑥 ↦→ 𝑡]]
which is what we wanted to show.
   Part 33.3: First, we show that the partial state h𝐻, S ∗ i is validated by Σ′ and 𝑉 ′ .
   Since the initial state is validated by Σ and 𝑉 , the partial state h𝐻, S ∗ i is validated by Σ and
valuation 𝑉 . Therefore one of 32.1, 32.2, 32.3 applies. We want to show that the partial state h𝐻, S ∗ i
is validated by Σ′ and valuation 𝑉 ′ .
 • Case 32.1: Then S ∗ = nil and trivially h𝐻, nili is validated by Σ′ and valuation 𝑉 ′ .
 • Case 32.2: Then S ∗ = h𝜌 0, 𝛼 0, 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ); 𝑠 0 i · S0 for some 𝜌 0 , 𝛼 0 , 𝑦, 𝑚, 𝑘, 𝑒 1 , · · · , 𝑒𝑘 , 𝑠 0 ,
   S0 . Also, there is some Σ0 , 𝑉0 , 𝑥 1, · · · , 𝑥𝑘 , 𝑡 1 , · · · , 𝑡𝑘 and 𝜎0, · · · , 𝜎𝑘 , 𝜎 ′ such that
                              The partial state h𝐻, S0 i is validated by Σ0 and 𝑉0,
                         Σ0 is reachable from Π with valuation 𝑉0,                         𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                                 𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                    𝜎0 = 𝜎 (Σ0 ),      𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,          ··· ,      𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                             ′                                     ′
                        𝜎𝑘 ⊢ pre(𝑚) ⊲ 𝜎 , _,               h𝐻, 𝛼 0, 𝜌 0 i 𝑉 𝜎 [𝛾 = 𝛾 (𝜎0 )],            and
                                                                            0

                                        ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉 (𝛾 (Σ) (𝑥𝑖 )) = 𝑉0 (𝑡𝑖 ),
                                                 𝜙˜ (Σ) = post(𝑚).
    We want to show that the partial state h𝐻, h𝜌 0, 𝛼 0, 𝑦 = 𝑚(𝑒 1 , · · · , 𝑒𝑘 ); 𝑠i · S0 i is validated by Σ′
    and valuation 𝑉 ′ . Immediately from above we can conclude that
                              The partial state h𝐻, S0 i is validated by Σ0 and 𝑉0,
                         Σ0 is reachable from Π with valuation 𝑉0,                         𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                                 𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                𝜎0 = 𝜎 (Σ0 ),      𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,          ··· ,    𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,          and
                                                   ′                                   ′
                            𝜎𝑘 ⊢ pre(𝑚) ⊲ 𝜎 , _,               h𝐻, 𝛼 0, 𝜌 0 i 𝑉 𝜎 [𝛾 = 𝛾 (𝜎0 )].
                                                                                   0

    Also, the frame h𝛼, 𝜌, 𝑥 = alloc(𝑆); 𝑠i must be executing the body of 𝑚, since it is in the stack
    immediately above the frame that contains 𝑦 =𝑚(𝑒 1, · · · , 𝑒𝑘 ). Therefore, since 𝑥 1, · · · , 𝑥𝑘 are all
Sound Gradual Verification with Symbolic Execution                                                                 111:101


    parameters of 𝑚, 𝑦 must be distinct from all of 𝑥 1, · · · , 𝑥𝑘 , since we do not allow assignment to
    parameters in a well-formed program. Thus
                  ∀1 ≤ 𝑖 ≤ 𝑘 : 𝑉 ′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉 ′ ((𝛾 (𝜎) [𝑥 ↦→ 𝑡]) (𝑥𝑖 )) = 𝑉 ′ (𝛾 (𝜎) (𝑥𝑖 ))
                                                     = 𝑉 ′ (𝛾 (Σ) (𝑥𝑖 )) = 𝑉 (𝛾 (Σ) (𝑥𝑖 ))
                                                     = 𝑉0 (𝑡𝑖 ).

    Finally, 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) by deﬁnition, thus
                                              𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = post(𝑚).
   Therefore the partial state h𝐻, S ∗ i is validated by Σ′ and 𝑉 ′ in this case.
 • Case 32.3: Then S ∗ = h𝜌 0 , 𝛼 0, while 𝑒 0 invariant 𝜙˜0 do 𝑠 0 ; 𝑠 0′ i · S0 for some 𝜌 0 , 𝛼 0 , 𝑒, 𝜙˜0 , 𝑠 0 ,
   𝑠 0′ , S0 , and there exists some Σ0 , 𝑉0 , and 𝜎0′ such that:
                              The partial state h𝐻, S0 i is validated by Σ0 and 𝑉0
                         Σ0 is reachable from Π with valuation 𝑉0,                 𝑠 (Σ0 ) = 𝑠 (S ∗ )
                                   𝜎0 ⊢ 𝜙˜0 ⊲ 𝜎0′ , _,      h𝐻, 𝛼 0, 𝜌 0 i 𝑉 𝜎0′     and
                                                                           0

                                                         𝜙˜ (Σ) = 𝜙˜0 .

    Now, by deﬁnition of Σ′′ , 𝜙˜ (Σ′ ) = 𝜙˜ (Σ) = 𝜙˜0 . Therefore, using the other assumptions given
    above, the partial state h𝐻, S ∗ i is validated by Σ′ and 𝑉 ′ in this case.
   Therefore the partial state h𝐻, S ∗ i is validated by Σ′ and 𝑉 ′ .
   Now, by lemma 57, the partial state h𝐻 ′ , S ∗ i is validated by Σ′ and 𝑉 ′ , which is what we need
to show for this part.
   Therefore h𝐻 ′ , h𝛼 ′ , 𝜌 [𝑥 ↦→ ℓ], 𝑠i · S ∗ i is validated by Σ′ with 𝑉 , which completes the proof.
   Case 5. ExecCallEnter: We have
                      h𝐻, h𝛼, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠i · S ∗ i, 𝑉 ′ LΘM𝐻 →
                          h𝐻, h𝛼 ′ , 𝜌 ′, body(𝑚); skipi · h𝛼 \ 𝛼 ′ , 𝜌, 𝑦 = 𝑚(𝑒); 𝑠i · S ∗ i
                      where 𝑥 = params(𝑚),               h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑣,       h𝐻, 𝛼, 𝜌i ⊢frm 𝑒,
                              ′                                    ′
                             𝜌 = [𝑥 ↦→ 𝑣],                ˆ 𝜌 i  pre(𝑚),
                                                  h𝐻, 𝛼 \ 𝛼,
                            𝛼ˆ = 𝑉 ′ LΘM𝐻 ,      and 𝛼 ′ = ⌊pre(𝑚)⌋ h𝐻, 𝛼 \𝛼,ˆ 𝜌 ′ i .
  By assumptions, the initial state is validated by some Σ and valuation 𝑉 , thus Σ = h𝜎, 𝑦 =
         ˜ for some 𝜎, 𝜙˜ where h𝐻, 𝛼, 𝜌i ′ 𝜎.
𝑚(𝑒); 𝑠, 𝜙i                                𝑉
  The only guard rule that applies is SGuardCall, so we have
                          𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R,     𝜎 ′ [𝛾 = [𝑥 ↦→ 𝑡]] ⊢ pre(𝑚) ⊲ 𝜎 ′′ , R ′ ,
                    Θ = rem(𝜎 ′′ , pre(𝑚)),         and by assumptions,            h𝐻, 𝛼i ⊢𝑉 R ∪ R ′
  For some 𝑘, let 𝑥 1, · · · , 𝑥𝑘 = 𝑥, 𝑒 1 , · · · , 𝑒𝑘 = 𝑒, 𝑣 1 , · · · , 𝑣 𝑘 = 𝑣, and 𝑡 1 = fresh, · · · , 𝑡𝑘 = fresh.
  Also, let 𝜎0 = h⊥, ∅, ∅, [𝑥 1 ↦→ 𝑡 1 , · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ], truei, and let 𝑉0 = [𝑡 1 ↦→ 𝑣 1, · · · , 𝑡𝑘 ↦→ 𝑣 𝑘 ].
Then h𝐻, 𝛼 ′ , 𝜌 ′ i 𝑉 𝜎0 .
                       0
  Tpre(𝑚)U h𝐻, 𝜌 ′ i ⊆ 𝛼 ′ : If pre(𝑚) is completely precise, then 𝛼 ′ = ⌊pre(𝑚)⌋ h𝐻, 𝛼 \𝛼,ˆ 𝜌 ′ i =
Tpre(𝑚)U h𝐻, 𝜌 ′ i . Otherwise, 𝛼 ′ = ⌊pre(𝑚)⌋ h𝐻, 𝛼 \𝛼,ˆ 𝜌 ′ i = 𝛼 \ 𝛼,        ˆ but also Tpre(𝑚)U h𝐻, 𝜌 ′ i ⊆ 𝛼 ′ = 𝛼 \ 𝛼ˆ
by lemma 4 since h𝐻, 𝛼 \ 𝛼,        ′
                                ˆ 𝜌 i  pre(𝑚).
  Now h𝐻, 𝛼 ′ , 𝜌 ′ i  pre(𝑚) by lemma 12, since h𝐻, 𝛼 \ 𝛼,                  ˆ 𝜌 ′ i  pre(𝑚).
111:102                                                                         C. Zimmerman, J. DiVincenzo, and J. Aldrich


  Now h𝐻, 𝛼 ′ , 𝜌 ′ i  pre(𝑚), h𝐻, 𝛼 ′ , 𝜌 ′ i 𝑉 𝜎0 . Thus by lemma 34, for some 𝜎0′ ,
                                                    0

              𝜎0 ⊢ pre(𝑚) ⊳ 𝜎0′ and 𝑉0′ (𝑔(𝜎0 ))         where 𝑉0′ = 𝑉0 [𝜎0 ⊢ pre(𝑚) ⊳ 𝜎0′ | 𝐻 ].
  Let Σ′0 = h𝜎0′ , body(𝑚); skip, post(𝑚)i. We want to show that
                   Γ ′ = h𝐻, h𝛼 ′ , 𝜌 ′, body(𝑚); skipi · h𝛼 \ 𝛼 ′ , 𝜌, 𝑦 = 𝑚(𝑒); 𝑠i · S ∗ i
is validated by Σ′0 with 𝑉0′ .
    Part 33.1: By SVerifyMethod, Π ⊢ init → Σ′0 . Therefore Σ′0 is reachable from Π with valuation
  ′
𝑉0 .
    Part 33.2: We want to show that Γ ′ corresponds to Σ′0 .
    By deﬁnition 𝑠 (Σ′0 ) = body(𝑚); skip = 𝑠 (Γ ′ ). Therefore, since 𝜎 (Σ′0 ) = 𝜎0′ , it suﬃces to show
h𝐻, 𝛼 ′ , 𝜌 ′ i 𝑉 ′ 𝜎0′ .
               0
  Since H(𝜎0 ) = H (𝜎0 ) = ∅, h𝐻, 𝛼 ′ \ Tpre(𝑚)U h𝐻, 𝜌 ′ i i 𝑉 H(𝜎0 ) and h𝐻, 𝛼 ′ \ Tpre(𝑚)U h𝐻, 𝜌 ′ i i 𝑉
                                                                         0                                               0
H (𝜎0 ). Also, for each 1 ≤ 𝑖 ≤ 𝑘, 𝑉0 (𝛾 (𝜎0 ) (𝑥𝑖 )) = 𝑣 𝑖 = 𝜌 ′ (𝑥𝑖 ), thus 𝜌 ′ 𝑉 𝛾 (𝜎0 ). Finally, 𝑉0 (𝑔(𝜎0 )) =
                                                                                          0
𝑉0 (true) = true. Therefore h𝐻, 𝛼 ′ \ Tpre(𝑚)U h𝐻, 𝜌 ′ i , 𝜌 ′ i 𝑉 𝜎0 .
                                                                  0
   Also, as shown before, h𝐻, 𝛼 ′ , 𝜌 ′ i  pre(𝑚). Therefore, by lemma 33,
                                                 h𝐻, 𝛼 ′ , 𝜌 ′ i 𝑉 ′ 𝜎0′ .
                                                                   0

   Part 33.3: We want to show that the partial state h𝐻, h𝛼 \ 𝛼 ′ , 𝜌, 𝑦 = 𝑚(𝑒); 𝑠i · S ∗ i is validated
by Σ′0 with 𝑉0′ , thus it suﬃces to show that case 32.2 is satisﬁed.
   Since h𝛼, 𝜌, 𝑦 = 𝑚(𝑒); 𝑠i · S ∗ was validated by Σ and 𝑉 , the partial state h𝐻, S ∗ i is validated by
Σ and 𝑉 .
   Also, by assumptions, Σ is reachable from Π with valuation 𝑉 and 𝑠 (Σ) = 𝑦 = 𝑚(𝑒); 𝑠 as shown
before.
   Furthermore, by assumptions, 𝑥 1, · · · , 𝑥𝑘 = 𝑥 = params(𝑚)
   Now let 𝜎0 = 𝜎 = 𝜎 (Σ), then 𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R, which was shown before, represents the series
of judgements
                           𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, R 1 , · · · 𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , S𝑘
where 𝜎𝑘 = 𝜎 ′ . Also, as shown before,
                          𝜎𝑘 [𝛾 = [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]] ⊢ pre(𝑚) ⊲ 𝜎 ′′ , R ′ .
Note that by deﬁnition 40 𝑉 ′ = 𝑉 [Σ ⇀ 𝜎 ′ ⊣ R, Θ | 𝐻 ] is the valuation corresponding to the series
of judgements above, extending 𝑉 .
   By lemmas 24 and 36, 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎𝑘 ) =⇒ · · · =⇒ 𝑔(𝜎1 ). Thus, since 𝑉 ′ (𝑔(𝜎 ′′ )) = true by
assumption,
                       𝑉 ′ (𝑔(𝜎 ′′ )) = 𝑉 ′ (𝑔(𝜎𝑘 )) = · · · = 𝑉 ′ (𝑔(𝜎1 )) = true.
Therefore, by lemmas 26 and 45,
          h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎1,     ··· ,     h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎𝑘 ,           h𝐻, 𝛼 \ Tpre(𝑚)U h𝐻, 𝜌 ′ i , 𝜌 ′ i 𝑉 ′ 𝜎 ′′ ,
Furthermore, since 𝛼ˆ = 𝑉 ′ LΘM𝐻 = 𝑉 ′ Lrem(𝜎 ′′ , pre(𝑚))M𝐻 and h𝐻, 𝛼 \ 𝛼, ˆ 𝜌 ′ i  pre(𝑚), we can
apply lemma 59 to get
                                h𝐻, 𝛼 \ 𝛼 ′ , 𝜌 ′ i 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎0 )].
Since 𝜌 𝑉 𝛾 (𝜎0 ) (by assumptions and since 𝜎0 = 𝜎),

                                        h𝐻, 𝛼 \ 𝛼 ′ , 𝜌i 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎0 )].
Sound Gradual Verification with Symbolic Execution                                                                  111:103


   For each 1 ≤ 𝑖 ≤ 𝑘, h𝐻, 𝜌i ⊢ 𝑒𝑖 ⇓ 𝑉 ′ (𝑡𝑖 ) by lemma 26, and h𝐻, 𝜌i ⊢ 𝑒𝑖 ⇓ 𝑣 𝑖 as shown before, thus
𝑉 ′ (𝑡𝑖 ) = 𝑣 𝑖 . Thus

                 ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉0′ (𝛾 (Σ′0 ) (𝑥𝑖 )) = 𝑉0′ (𝛾 (𝜎0′ ) (𝑥𝑖 ))                        by defn.
                                                      = 𝑉0′ (𝛾 (𝜎0 ) (𝑥𝑖 ))                    Lemma 39
                                                      = 𝑉0 (𝛾 (𝜎0 ) (𝑥𝑖 ))                         𝑉 ⊆ 𝑉′
                                                      = 𝑣𝑖                                          by def.
                                                             ′
                                                      = 𝑉 (𝑡𝑖 ).                            shown above

  Finally, by deﬁnition 𝜙˜ (Σ) = post(𝑚).
  Therefore the partial state h𝐻, h𝛼 ′ , 𝜌 ′, body(𝑚); skipi · h𝛼 \𝛼 ′ , 𝜌, 𝑦 =𝑚(𝑒); 𝑠i · S ∗ i is validated
by Σ′0 with 𝑉0′ .
  Therefore Γ ′ is validated by Σ′0 with 𝑉0′ .
  Case 6. ExecCallExit: We have

             h𝐻, h𝛼, 𝜌, skipi · h𝛼 ′ , 𝜌 ′, 𝑦 = 𝑚(𝑒); 𝑠i · Si, 𝑉 ′ LΘM𝐻 → h𝐻, h𝛼 ′′ , 𝜌 ′′, 𝑠i · S ∗ i                (39)
                          where h𝐻, 𝛼, 𝜌i  post(𝑚),               𝜌 ′′ = 𝜌 ′ [𝑦 ↦→ 𝜌 (result)],                      (40)
                                           and 𝛼 ′′ = 𝛼 ′ ∪ ⌊post(𝑚)⌋ h𝐻, 𝛼, 𝜌 i .                                    (41)

    By assumptions, the initial state is validated by some Σ and valuation 𝑉 , thus Σ = h𝜎, skip, 𝜙i                ˜
                   ˜
for some 𝜎, 𝜙 where h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎.
    Also, by 33.3, the partial state h𝐻, h𝛼 ′ , 𝜌 ′, 𝑦 = 𝑚(𝑒); 𝑠i · Si is validated by Σ and 𝑉 . Thus 32.2
must apply, and thus there is some Σ′ reachable from Π and valuation 𝑉 such that Σ′ = h𝜎0 , 𝑦 =
𝑚(𝑒); 𝑠, 𝜙˜ ′ i for some 𝜎0, 𝜙˜ ′ . Also, we can let 𝑒 1 , · · · , 𝑒𝑘 = 𝑒 and then there are sequences 𝜎1, · · · , 𝜎𝑘 ,
𝑥 1, · · · , 𝑥𝑘 , and 𝑡 1 , · · · , 𝑡𝑘 where

                 𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,      ··· ,    𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,                     by (8)           (42)
                                                          ′
                 𝜎𝑘 [𝛾 = [𝑥𝑖 ↦→ 𝑡𝑖 ]] ⊢ pre(𝑚) ⊲ 𝜎 , _,                                                               (43)
                                ′   ′          ′
                 and     h𝐻, 𝛼 , 𝜌 i 𝑉 ′ 𝜎 [𝛾 = 𝛾 (𝜎0 )]                                            by (10)           (44)

where 𝑉 ′ is a valuation corresponding to this series of judgements.
  Let

             𝑡 = fresh,     𝑉ˆ ′ = 𝑉 ′ [𝑡 ↦→ 𝜌 (result)],          𝜌ˆ = [𝑥 1 ↦→ 𝜌 (𝑥 1 ), · · · , 𝑥𝑘 ↦→ 𝜌 (𝑥𝑘 )],
                                and 𝛾ˆ = [𝑥 1 ↦→ 𝑡 1 , · · · , 𝑥𝑘 ↦→ 𝑡𝑘 , result ↦→ 𝑡]

  We have h𝐻, 𝛼, 𝜌i  post(𝑚) by (40). Since 𝜌ˆ is simply the restriction of 𝜌 to params(𝑚) and
result, and post(𝑚) may only reference variables in params(𝑚) as well as result, h𝐻, 𝛼, 𝜌i           ˆ 
post(𝑚) and Tpost(𝑚)U h𝐻, 𝜌ˆ i = Tpost(𝑚)U h𝐻, 𝜌 i .
  By lemma 4 Tpost(𝑚)U h𝐻, 𝜌 i ⊆ 𝛼. Recall that 𝛼 ′′ = 𝛼 ∪ ⌊post(𝑚)⌋ h𝐻, 𝛼, 𝜌 i . If post(𝑚) is com-
pletely precise, then ⌊post(𝑚)⌋ h𝐻, 𝛼, 𝜌 i = Tpost(𝑚)U h𝐻, 𝜌 i . Otherwise, ⌊post(𝑚)⌋ h𝐻, 𝛼, 𝜌 i = 𝛼, but
Tpost(𝑚)U h𝐻, 𝜌 i ⊆ 𝛼 as shown before. In both cases, Tpost(𝑚)U h𝐻, 𝜌 i = Tpost(𝑚)U h𝐻, 𝜌ˆ i ⊆ 𝛼 ′′ .
  Therefore by lemma 12
                                                   h𝐻, 𝛼 ′′ , 𝜌i
                                                              ˆ  post(𝑚).                                            (45)
111:104                                                                                         C. Zimmerman, J. DiVincenzo, and J. Aldrich


  Note that, for all 1 ≤ 𝑖 ≤ 𝑘,
           𝑉ˆ ′ (𝑡𝑖 ) = 𝑉 ′ (𝑡𝑖 )                                                                              by deﬁnition
                     = 𝑉 (𝛾 (Σ) (𝑥𝑖 ))                                                                                 by (9)
                     = 𝜌 (𝑥𝑖 )                              since 𝜌 𝑉 𝛾 (Σ), since initial valid by Σ and 𝑉
                     = 𝜌ˆ (𝑥𝑖 )                                                                                by deﬁnition

Thus 𝜌ˆ ˆ ′ 𝛾 ′ . Also, h𝐻, 𝛼 ′ , 𝜌 ′ i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )] by (44). Therefore h𝐻, 𝛼 ′ , 𝜌i
                                                                                           ˆ ˆ ′ 𝜎 ′ [𝛾 = 𝛾].
                                                                                                          ˆ
          𝑉                                                                                   𝑉
                 ′′    ′
Finally, since 𝛼 ⊆ 𝛼 , by lemma 19,
                                                      h𝐻, 𝛼 ′′ , 𝜌i
                                                                 ˆ           𝜎 ′ [𝛾 = 𝛾].
                                                                                      ˆ                                               (46)
                                                                      𝑉ˆ ′
  Now, by lemma 34, (45), and (46),
                           𝜎 ′ [𝛾 = 𝛾]
                                    ˆ ⊢ post(𝑚) ⊳ 𝜎 ′′ ,                     and 𝑉 ′′ (𝑔(𝜎 ′′′ )) = true                              (47)
where 𝑉 ′′ is the corresponding valuation extending 𝑉ˆ ′ .
  Let 𝜎 ′′′ = 𝜎 ′′ [𝛾 = 𝛾 (𝜎0 ) [𝑦 ↦→ 𝑡]].
  Now (42), (43), and (47), and the deﬁnition of 𝜎 ′′′ satisfy the antecedent for SExecCall, therefore
                                               𝜎0 ⊢ 𝑦 = 𝑚(𝑒 1 , · · · , 𝑒𝑘 ); 𝑠 → 𝑠 ⊣ 𝜎 ′′′ .
Let Σ′′ = h𝜎 ′′′ , 𝑠, 𝜙˜′ i, now by SVerifyStep
                                                             Π ⊢ Σ′ → Σ′′ .
    We want to show that h𝐻, h𝛼 ′′ , 𝜌 ′′ , 𝑠i · S ∗ i is validated by Σ′′ .
    Part 33.1: Since Π ⊢ Σ′ → Σ′′ , Σ′′ is reachable from Π. Let its corresponding valuation be 𝑉 ′′′ .
    Part 33.2: By deﬁnition, 𝑠 (Σ′′ ) = 𝑠.
    By (44) h𝐻, 𝛼 ′ , 𝜌 ′ i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )]. Since the initial state must be well-formed, 𝛼 and 𝛼 ′ are dis-
joint, and as shown before, Tpost(𝑚)U h𝐻, 𝜌 i = Tpost(𝑚)U h𝐻, 𝜌ˆ i ⊆ 𝛼, therefore 𝛼 ′ \Tpost(𝑚)U h𝐻, 𝜌ˆ i =
𝛼 ′ . Also, 𝑉ˆ ′ ⊆ 𝑉 ′ . Thus
                                    h𝐻, 𝛼 ′ \ Tpost(𝑚)U h𝐻, 𝜌ˆ i , 𝜌 ′ i                  𝜎 ′ [𝛾 = 𝛾 (𝜎0 )].
                                                                                 𝑉ˆ ′

  Also, as shown before, 𝜌ˆ                    ˆ therefore
                                               𝛾,
                                        𝑉ˆ ′

                                       h𝐻, 𝛼 ′ \ Tpost(𝑚)U h𝐻, 𝜌ˆ i , 𝜌i
                                                                      ˆ                        𝜎 ′ [𝛾 = 𝛾].
                                                                                                        ˆ
                                                                                    𝑉ˆ ′
  Then, since 𝛼 ′ ⊆ 𝛼 ′′ , 𝛼 ′ \ Tpost(𝑚)U h𝐻, 𝜌ˆ i ⊆ 𝛼 ′′ \ Tpost(𝑚)U h𝐻, 𝜌ˆ i , and thus by lemma 19
                                      h𝐻, 𝛼 ′′ \ Tpost(𝑚)U h𝐻, 𝜌ˆ i , 𝜌i
                                                                      ˆ                        𝜎 ′ [𝛾 = 𝛾].
                                                                                                        ˆ
                                                                                        𝑉ˆ ′
  Now, since it was shown in (45) that h𝐻, 𝛼 ′′ , 𝜌i
                                                   ˆ  post(𝑚) and in (47) that 𝑉 ′′ (𝑔(𝜎 ′′ )) = true,
by lemma 33
                                                  ˆ 𝑉 ′′ 𝜎 ′′ .
                                      h𝐻, 𝛼 ′′ , 𝜌i
  Now by (44) 𝜌 ′ 𝑉 ′ 𝛾 (𝜎0 ), then since 𝑉 ′ ⊆ 𝑉 ′′ , 𝜌 ′ 𝑉 ′′ 𝛾 (𝜎0 ). Now, since 𝛾 (𝜎 ′′′ ) = 𝛾 (𝜎0 ) [𝑦 ↦→ 𝑡],
to show 𝜌 ′′ 𝑉 ′′ 𝛾 (𝜎 ′′′ ) it suﬃces to show that 𝑉 ′′ (𝛾 (𝜎 ′′′ ) (𝑦)) = 𝜌 ′′ (𝑦).
   But now 𝑉 ′′ (𝛾 (𝜎 ′′′ ) (𝑦)) = 𝑉 ′′ (𝑡) = 𝑉ˆ ′ (𝑡) = 𝜌 (result) = 𝜌 ′′ (𝑦), which is what we needed to
show. Therefore, since 𝛾 is the only component changed between 𝜎 ′′ and 𝜎 ′′′ ,
                                                        h𝐻, 𝛼 ′′ , 𝜌 ′′ i 𝑉 ′′ 𝜎 ′′′ .
Sound Gradual Verification with Symbolic Execution                                                                                     111:105


  Therefore, since 𝜎 (Σ′′ ) = 𝜎 ′′′ , we have shown that Σ′′ corresponds to h𝐻, h𝛼 ′′ , 𝜌 ′′ , 𝑠i · S ∗ i with
valuation 𝑉 ′′ .
  Part 33.3: We need to show that the partial state h𝐻, S ∗ i is validated by Σ′′ and 𝑉 ′′ . We already
have that h𝐻, S ∗ i is validated by Σ′ and 𝑉 ′ . Thus one of 32.1, 32.2, or 32.3 must apply.
  If 32.1 applies: Then S ∗ = nil, thus trivially the partial state h𝐻, S ∗ i is validated by Σ′′ and 𝑉 ′′ .
  If 32.2 applies: Then S ∗ = h𝛼 0 , 𝜌 0, 𝑦 ′ =𝑚 ′ (𝑒 1′ , · · · , 𝑒𝑘′ ′ ); 𝑠 ′ i·S0∗ for some 𝑘 ′ , 𝑦 ′ , 𝑚 ′, 𝑒 1′ , · · · , 𝑒𝑘′ ′ , 𝑠 ′, S0∗ .
Also, there exists some Σ′0, 𝑉0′ , 𝑥 1′ , · · · , 𝑥𝑘′ ′ , 𝑡 1′ , · · · , 𝑡𝑘′ ′ , 𝜎0, · · · , 𝜎𝑘 ′ , 𝜎 ′ such that
                                  The partial state h𝐻, S0∗ i is validated by Σ′0 and 𝑉0′ ,
                            Σ′0 is reachable from Π with valuation 𝑉0′,                       𝑠 (Σ′0 ) = 𝑠 (S ∗ ),
                                                     𝑥 1′ , · · · , 𝑥𝑘′ ′ = params(𝑚),
                      𝜎0 = 𝜎 (Σ′0 ),       𝜎0 ⊢ 𝑒 1′ ⇓ 𝑡 1′ ⊣ 𝜎1, _,       ··· ,      𝜎𝑘 ′ −1 ⊢ 𝑒𝑘′ ′ ⇓ 𝑡𝑘′ ′ ⊣ 𝜎𝑘 ′ , _,
                                𝜎𝑘 ′ ⊢ pre(𝑚 ′ ) ⊲ 𝜎 ′, _,          h𝐻, 𝛼 0 , 𝜌 0 i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )],
                                                                                        0

                                       ∀ 1 ≤ 𝑖 ≤ 𝑘 ′ : 𝑉 ′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉0′ (𝑡𝑖′ ),           and
                                                     𝜙˜ (Σ′ ) = post(𝑚 ′ ).
  We want to show that the partial state h𝐻, S ∗ i is validated by Σ′′ and 𝑉 ′′ . Immediately from
above,
                                  The partial state h𝐻, S0∗ i is validated by Σ′0 and 𝑉0′ ,
                            Σ′0 is reachable from Π with valuation 𝑉0′,              𝑠 (Σ′0 ) = 𝑠 (S ∗ ),
                                                      ′           ′
                                                    𝑥 1, · · · , 𝑥𝑘 ′ = params(𝑚),
                      𝜎0 = 𝜎 (Σ′0 ),       𝜎0 ⊢ 𝑒 1′ ⇓ 𝑡 1′ ⊣ 𝜎1, _, · · · , 𝜎𝑘 ′ −1 ⊢ 𝑒𝑘′ ′ ⇓ 𝑡𝑘′ ′ ⊣ 𝜎𝑘 ′ , _,
                                𝜎𝑘 ′ ⊢ pre(𝑚 ′ ) ⊲ 𝜎 ′, _,          h𝐻, 𝛼 0 , 𝜌 0 i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )].
                                                                                        0

Also, the frame h𝛼 ′ , 𝜌 ′, 𝑦 = 𝑚(𝑒 1 , · · · , 𝑒𝑘 ); 𝑠i must be executing the body of 𝑚 ′ , since it is in the
stack immediately above the frame that contains 𝑦 ′ = 𝑚 ′ (𝑒 1′ , · · · , 𝑒𝑘′ ′ ). Therefore, since 𝑥 1′ , · · · , 𝑥𝑘 ′
are all parameters of 𝑚 ′ , 𝑦 must be distinct from all of 𝑥 1′ , · · · , 𝑥𝑘′ ′ , since we do not allow assignment
to parameters in a well-formed program. Thus
                   ∀1 ≤ 𝑖 ≤ 𝑘 ′ : 𝑉 ′′ (𝛾 (Σ′′ ) (𝑥𝑖 )) = 𝑉 ′′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉 ′ (𝛾 (Σ′ ) (𝑥𝑖 )) = 𝑉0′ (𝑡𝑖 ).
   Finally, 𝜙˜ (Σ′′ ) = 𝜙˜ (Σ′ ) by deﬁnition, thus
                                          𝜙˜ (Σ′′ ) = 𝜙˜ (Σ′ ) = post(𝑚 ′ ).
     Therefore the partial state h𝐻, S ∗ i is validated by Σ′′ and 𝑉 ′′ in this case.
     If 32.3 applies: Then S ∗ = h𝜌 0, 𝛼 0, while 𝑒 invariant 𝜙˜0 do 𝑠 0 ; 𝑠 0′ i · S0∗ for some 𝜌 0 , 𝛼 0 , 𝑒, 𝜙˜0 , 𝑠 0 ,
𝑠 0 , S0∗ , and there exists some Σ′0 , 𝑉0′ , and 𝜎0′ such that:
  ′

                                  The partial state h𝐻, S0∗ i is validated by Σ′0 and 𝑉0′
                            Σ′0 is reachable from Π with valuation 𝑉0′,                       𝑠 (Σ′0 ) = 𝑠 (S ∗ ),
                                         𝜎0 ⊢ 𝜙˜0 ⊲ 𝜎0′ , _,        h𝐻, 𝛼 0, 𝜌 0 i 𝑉 ′ 𝜎0′       and
                                                                                       0

                                                               𝜙˜ (Σ′ ) = 𝜙˜0 .
  Now, by deﬁnition of Σ′′ , 𝜙˜ (Σ′′ ) = 𝜙˜ (Σ′ ) = 𝜙˜0 . Therefore, using the other assumptions given
above, the partial state h𝐻, S ∗ i is validated by Σ′′ and 𝑉 ′′ in this case.
  Therefore deﬁnition part 33.3 is satisﬁed.
111:106                                                                C. Zimmerman, J. DiVincenzo, and J. Aldrich


   Therefore all parts of deﬁnition 33 are satisﬁed. Thus h𝐻, h𝛼 ′′ , 𝜌 ′′, 𝑠i · S ∗ i is validated by Σ′′ ,
as we wanted to show.
   Case 7. ExecAssert: We have
                      h𝐻, h𝛼, 𝜌, assert 𝜙; 𝑠i · S ∗ i, 𝑉 ′ LΘM𝐻 → h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i
                                         where      h𝐻, 𝛼, 𝜌i  ? ∗ 𝜙 .
                                                                     ˜ for some 𝜎, 𝜙˜ where h𝐻, 𝛼, 𝜌i
     Since the initial state is validated by Σ, Σ = h𝜎, assert 𝜙; 𝑠, 𝜙i                               𝑉
𝜎.
     The only guard rule that applies is SGuardAssert, so we have, for some 𝜎 ′ ,
                                               𝜎 ⊢ ? ∗ 𝜙 ⊲ 𝜎 ′, R
                      and by assumptions 𝑉 ′ (𝑔(𝜎 ′ )) = true and           h𝐻, 𝛼i ⊢𝑉 ′ R.
Also, by deﬁnition 𝑉 ′ = 𝑉 [𝜎 ⊢ ? ∗ 𝜙 ⊲ 𝜎 ′, R | 𝐻 ].
     Thus by lemma 45 h𝐻, 𝛼 \ T? ∗ 𝜙U h𝐻, 𝜌 i , 𝜌i 𝑉 ′ 𝜎 ′ .
  Thus by lemma 19, h𝐻, 𝛼, 𝜌i          𝑉′
                                            𝜎 ′ . Also, as noted before, h𝐻, 𝛼, 𝜌i  ? ∗ 𝜙. Therefore, by
lemma 33, for some 𝜎 ′′ ,
                               𝜎 ′ ⊢ ? ∗ 𝜙 ⊳ 𝜎 ′′   and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true.
  Now, by SExecAssert, 𝜎 ⊢ assert 𝜙; 𝑠 → 𝑠 ⊣ 𝜎 [𝑔 = 𝑔(𝜎 ′′ )].
                                 ˜ We want to show that h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i is validated by Σ′ and
  Let Σ′ = h𝜎 [𝑔 = 𝑔(𝜎 ′′ )], 𝑠, 𝜙i.
 ′′
𝑉 .
  By SVerifyStep, Σ′ is reachable from Π with valuation 𝑉 ′′ .
  By assumptions, h𝐻, 𝛼, 𝜌i 𝑉 𝜎, and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true, thus h𝐻, 𝛼, 𝜌i 𝑉 ′′ 𝜎 [𝑔 = 𝑔(𝜎 ′′ )].
                                               ˜ Therefore Σ′ corresponds to h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i with
Also, by deﬁnition, Σ′ = h𝜎 [𝑔 = 𝑔(𝜎 ′′ )], 𝑠, 𝜙i.
valuation 𝑉 ′′ .
  Finally, by deﬁnition 𝛾 (Σ′ ) = 𝛾 (Σ) and 𝜙˜ (Σ′ ) = 𝜙˜ = 𝜙˜ (Σ).
  Therefore h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i is a valid state by lemma 49.
  Case 8. ExecIfA: We have
              h𝐻, h𝛼, 𝜌, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠i · S ∗ i, 𝑉 ′ LΘM𝐻 → h𝐻, h𝛼, 𝜌, 𝑠 1 ; 𝑠i · S ∗ i
                           where     h𝐻, 𝜌i ⊢ 𝑒 ⇓ true and          h𝐻, 𝛼, 𝜌i ⊢frm 𝑒
                                                                                 ˜ for some 𝜎, 𝜙˜ where
  Since the initial state is validated by Σ, Σ = h𝜎, if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠, 𝜙i
h𝐻, 𝛼, 𝜌i 𝑉 𝜎.
  The only guard rule that applies is SGuardIf, so we have, for some 𝜎 ′ ,
                                               𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R
                     and by assumptions 𝑉 ′ (𝑔(𝜎 ′ )) = true and             h𝐻, 𝛼i ⊢𝑉 ′ R
where 𝑉 ′ = 𝑉 [𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R | 𝐻 ].
     Now by SExecIfA,
                       𝜎 ⊢ if 𝑒 then 𝑠 1 else 𝑠 2 ; 𝑠 → 𝑠 1 ; 𝑠 ⊣ 𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡].
                                            ˜ Then by SVerifyStep, Σ′ is reachable from Π with valuation
   Let Σ′ = h𝜎 ′ [𝑔 = 𝑔(𝜎 ′ )&&𝑡], 𝑠 1 ; 𝑠, 𝜙i.
 ′
𝑉 .
   Now h𝐻, 𝜌i ⊢ 𝑒 ⇓ 𝑉 ′ (𝑡) and h𝐻, 𝜌i ⊢ 𝑒 ⇓ true, thus 𝑉 ′ (𝑡) = true. Also, h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ , thus
𝑉 ′ (𝑔(𝜎 ′ )) = true, and then 𝑉 ′ (𝑔(𝜎 ′ ) && 𝑡) = 𝑉 ′ (𝑔(𝜎 ′ )) ∧ 𝑉 ′ (𝑡) = true. Therefore h𝐻, 𝛼, 𝜌i 𝑉 ′
𝜎 ′ [𝑔 = 𝑔(𝜎 ′ ) && 𝑡].
Sound Gradual Verification with Symbolic Execution                                                                   111:107


                                                           ˜ Therefore Σ′ corresponds to
  Also, by deﬁnition, Σ′ = h𝜎 [𝑔 = 𝑔(𝜎 ′ ) && 𝑡], 𝑠 1 ; 𝑠, 𝜙i.
                       ∗
h𝐻, h𝛼, 𝜌, 𝑠 1 ; 𝑠i · S i with valuation 𝑉 .  ′′

  Finally, 𝛾 (Σ′ ) = 𝛾 (𝜎 ′ ) = 𝑠𝑒𝑛𝑣 (𝜎) = 𝛾 (Σ) by lemma 25 and 𝜙˜ (Σ′ ) = 𝜙˜ = 𝜙˜ (Σ) by deﬁnition.
  Therefore 𝐻 h𝛼, 𝜌, 𝑠 1 ; 𝑠i · S ∗ is a valid state by lemma 49.
  Case 9. ExecIfB: Similar to case 8, but using SExecIfB.
  Case 10. ExecWhileEnter: We have
                h𝐻, h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ i →
                 h𝐻, h𝛼 ′ , 𝜌, 𝑠; skipi · h𝛼 \ 𝛼 ′ , 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ i
               where h𝐻, 𝜌i ⊢ 𝑒 ⇓ true, h𝐻, 𝛼 \ 𝛼,              ˜
                                                         ˆ 𝜌i  𝜙,
                        𝛼ˆ = 𝑉 LΘM𝐻 ,                 ˜ h𝐻, 𝛼 \𝛼,ˆ 𝜌 i
                                           and 𝛼 ′ = ⌊𝜙⌋
      Since the initial state is validated by Σ, Σ = h𝜎, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜0 i for some 𝜎, 𝜙˜
where h𝐻, 𝛼, 𝜌i 𝑉 𝜎.
      The only guard rule that applies is SGuardWhile, so we have, for some 𝜎 ′ , 𝜎 ′′ , 𝑘, 𝑥 1, · · · , 𝑥𝑘 ,
𝑡 1 , · · · , 𝑡𝑘 , and 𝑡,
                     𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, R ′ , 𝑥 1, · · · , 𝑥𝑘 = modiﬁed(𝑠), 𝑡 1 = fresh, · · · , 𝑡𝑘 = fresh, (48)
                              𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 1 ↦→ 𝑡 1 , · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]] ⊢ 𝜙˜ ⊳ 𝜎 ′′ ,                        (49)
                                      𝜎 ′′ ⊢ 𝑒 ↓ 𝑡 ⊣ R ′′ , Θ = rem(𝜎 ′ , 𝜙),      ˜                                   (50)
                                                ′         ′′                                         ′     ′′
                 and by assumptions 𝑉 (𝑔(𝜎 )) = true and                                h𝐻, 𝛼i ⊢
                                                                                               𝑉′   R ∪R               (51)
where 𝑉 ′ is the corresponding valuation for these judgements (see deﬁnition 40).
  By lemma 23
                                     h𝐻, 𝛼i ⊢𝑉 ′ R ′ and h𝐻, 𝛼i ⊢𝑉 ′ R ′′ .                               (52)
  Let 𝑡 1 = fresh, · · · , 𝑡𝑘 = fresh and 𝜎0 = h⊥, ∅, ∅, 𝛾 (𝜎) [𝑥 1 ↦→ 𝑡 1′ , · · · , 𝑥𝑘 ↦→ 𝑡𝑘′ ], 𝑔(𝜎)i.
        ′                   ′

  Let 𝑉0 = 𝑉 ′ [𝑡 1′ ↦→ 𝜌 (𝑥 1 ), · · · , 𝑡𝑘′ ↦→ 𝜌 (𝑥𝑘 )]. Now, for any 𝑥 ∈ dom(𝛾 (𝜎0 )), if 𝑥 = 𝑥𝑖 for some
𝑖, then 𝑉0 (𝛾 (𝑥)) = 𝑉0 (𝛾 (𝜎0 ) (𝑥𝑖 )) = 𝑉0 (𝑡𝑖 ) = 𝜌 (𝑥𝑖 ) = 𝜌 (𝑥). Otherwise, 𝑥 ∈ dom(𝛾 (𝜎)) and thus
𝑉0 (𝛾 (𝜎) (𝑥)) = 𝑉 (𝛾 (𝜎) (𝑥)) = 𝜌 (𝑥) since 𝜌 𝑉 𝛾 (𝜎). Therefore 𝜌 𝑉 𝛾 (𝜎0 ).
                                                                          0
    Also, since H(𝜎0 ) = H (𝜎0 ) = ∅, h𝐻, 𝛼 ′ \ T𝜙U ˜ h𝐻, 𝜌 i i                         ˜ h𝐻, 𝜌 i i
                                                                  H(𝜎0 ) and h𝐻, 𝛼 ′ \ T𝜙U          H (𝜎0 ).
                                                                           𝑉0                                   𝑉0
Finally, 𝑉0 (𝑔(𝜎0 )) = 𝑉 (𝑔(𝜎)) = true since h𝐻, 𝛼, 𝜌i 𝑉 𝜎.
  Therefore
                                                ˜ h𝐻, 𝜌 i , 𝜌i
                                     h𝐻, 𝛼 ′ \ T𝜙U               𝜎0
                                                               𝑉                    0

and then also h𝐻, 𝛼 ′ , 𝜌i    𝑉0
                                   𝜎0 by lemma 19.
  Furthermore, by assumptions, h𝐻, 𝛼 \ 𝛼,       ˜ thus h𝐻, 𝛼 ′ , 𝜌i  𝜙˜ by lemma 13, since 𝛼 ′ =
                                        ˆ 𝜌i  𝜙,
 ˜
⌊𝜙⌋ h𝐻, 𝛼 \𝛼,ˆ 𝜌 i .
  Therefore, by lemma 34
                           𝜎0 ⊢ 𝜙˜ ⊳ 𝜎 ′ and 𝑉 ′ (𝑔(𝜎 ′ )) = true
                                                    0              0            0

where 𝑉0′ = 𝑉0 [𝜎0 ⊢ 𝜙˜ ⊳ 𝜎0′ | 𝐻 ]. Also, by lemma 33,
                                                    h𝐻, 𝛼 ′ , 𝜌i 𝑉 ′ 𝜎0′ .
                                                                       0

  Now by lemma 30,
                                                        𝜎0′ ⊢ 𝑒 ↓ 𝑡 0 ⊣ _
and let 𝑉0′′ = 𝑉0′ [𝜎0′ ⊢ 𝑒 ↓ 𝑡 0 ⊣ _].
111:108                                                                          C. Zimmerman, J. DiVincenzo, and J. Aldrich


                                                    ˜
  Let Σ0 = h𝜎0′ [𝑔 = 𝑔(𝜎0′ ) && 𝑡 0 ], 𝑠 ′ ; skip, 𝜙i.
  We want to show that
              Γ ′ = h𝐻, h𝛼 ′ , 𝜌, 𝑠; skipi · h𝛼 \ 𝛼 ′ , 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ i
is validated by Σ0 and 𝑉0′′ .
    Part 33.1: By SVerifyLoopBody Π ⊢ Σ → Σ0 . Therefore Σ0 is reachable from Π with valuation
𝑉0′′ .
    Part 33.2: Since h𝐻, 𝜌i ⊢ 𝑒 ⇓ true, by lemma 29, 𝑉0′′ (𝑡 0 ) = true. Therefore 𝑉0′′ (𝑔(𝜎0′ ) && 𝑡 0 ) =
𝑉 ′ (𝑔(𝜎0′ )) ∧ 𝑉 ′ (𝑡 0′ ) = true. Thus, since we have already shown h𝐻, 𝛼 ′ , 𝜌i 𝑉 ′ 𝜎0′ ,
                                                                                                   0

                                       h𝐻, 𝛼 ′ , 𝜌i 𝑉 ′′ 𝜎0′ [𝑔 = 𝑔(𝜎0′ ) && 𝑡 0 ].
                                                        0

  Also, 𝑠 (Σ0 ) = 𝑠; skip by deﬁnition. Therefore Γ ′ corresponds to Σ0 with 𝑉0′′ .
  Part 33.3: We want to show that the partial state
                      Γ ∗ = h𝐻, h𝛼 \ 𝛼 ′ , 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ i
is validated by Σ0 and 𝑉0′′ .
   By assumptions, h𝐻, h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ i was validated by Σ and 𝑉 .
Therefore the partial state h𝐻, S ∗ i was validated by Σ and 𝑉 , Σ is reachable from Π with 𝑉 , 𝑠 (Σ) =
while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ , and h𝐻, 𝛼, 𝜌i 𝑉 𝜎.
   By (48) 𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, R and by (52) h𝐻, 𝛼i ⊢𝑉 ′ R. Therefore h𝐻, 𝛼 \ T𝜙U˜ h𝐻, 𝜌 i , 𝜌i ′ 𝜎 ′ .
                                                                                                          𝑉
                                                     ˜ 𝐻 , 𝛼 ′ = ⌊𝜙⌋
  Furthermore, since 𝛼ˆ = 𝑉 ′ LΘM𝐻 = 𝑉 ′ Lrem(𝜎 ′ , 𝜙)M                ˜ h𝐻, 𝛼 \𝛼,ˆ 𝜌 i , and h𝐻, 𝛼 \ 𝛼,     ˜
                                                                                                      ˆ 𝜌i  𝜙,
we can apply lemma 59 to get
                                       h𝐻, 𝛼 \ 𝛼 ′ , 𝜌i 𝑉 ′ 𝜎 ′ .
  Finally, 𝜙˜ (Σ0 ) = 𝜙˜ by deﬁnition.
  Therefore Γ ∗ is validated by Σ0 and 𝑉0′′ since we have satisﬁed all requirements of case 32.3.
  Therefore Γ ′ is validated by Σ0 and 𝑉0′′ , which completes the proof.
  Case 11. ExecWhileSkip: We have
               h𝐻, h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ i, 𝛼ˆ → h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i
                 where 𝛼ˆ = 𝑉 ′ LΘM𝐻 ,           h𝐻, 𝜌i ⊢ 𝑒 ⇓ false,            h𝐻, 𝛼, 𝜌i ⊢frm 𝑒,      and
                                                           ˆ 𝜌i  𝜙˜
                                                   h𝐻, 𝛼 \ 𝛼,
      Since the initial state is validated by Σ, Σ = h𝜎, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ , 𝜙˜′ i for some 𝜎,
 ˜ ′
𝜙 where h𝐻, 𝛼, 𝜌i 𝑉 𝜎.
      The only guard rule that applies is SGuardWhile, so we have, for some 𝜎 ′ , 𝜎 ′′ , 𝑘, 𝑥 1, · · · , 𝑥𝑘 ,
𝑡 1 , · · · , 𝑡𝑘 , and 𝑡,
                     𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′, R ′ , 𝑥 1, · · · , 𝑥𝑘 = modiﬁed(𝑠), 𝑡 1 = fresh, · · · , 𝑡𝑘 = fresh, (53)
                               𝜎 ′ [𝛾 = 𝛾 (𝜎 ′ ) [𝑥 1 ↦→ 𝑡 1 , · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]] ⊢ 𝜙˜ ⊳ 𝜎 ′′ ,                       (54)
                                       𝜎 ′′ ⊢ 𝑒 ↓ 𝑡 ⊣ R ′′ , Θ = rem(𝜎 ′ , 𝜙),      ˜                                  (55)
                                                 ′      ′′                                         ′     ′′
                 and by assumptions 𝑉 (𝑔(𝜎 )) = true and                            h𝐻, 𝛼i ⊢𝑉 ′ R ∪ R                  (56)
where 𝑉 ′ is the corresponding valuation for these judgements (see deﬁnition 40).
  Let Σ′ = h𝜎 ′′ [𝑔 = 𝑔(𝜎 ′′ ) && ! 𝑡], 𝑠 ′, 𝜙˜ ′ i.
  By SExecWhileSkip
                    𝜎 ⊢ while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ → 𝑠 ′ ⊣ 𝜎 ′′ [𝑔 = 𝑔(𝜎 ′′ ) && ! 𝑡].
Sound Gradual Verification with Symbolic Execution                                                            111:109


Therefore by SVerifyStep Π ⊢ Σ → Σ′ . Thus Σ′ is reachable from Π with valuation 𝑉 ′ .
  By lemma 23
                             h𝐻, 𝛼i ⊢𝑉 ′ R ′ and h𝐻, 𝛼i ⊢𝑉 ′ R ′′ .                                              (57)
   By lemmas 36 and 31, 𝑔(𝜎 ′′ )      =⇒ 𝑔(𝜎 ′ ). Therefore 𝑉 ′ (𝑔(𝜎 ′ )) = true. Now, by lemma 45,
                                                      ˜ h𝐻, 𝛼 i , .i ′ 𝜎 ′
                                             h𝐻, 𝛼 \ T𝜙U            𝑉

   By deﬁnition 40, for all 1 ≤ 𝑖 ≤ 𝑘, 𝑉 ′ (𝑡𝑖 ) = 𝑉 (𝛾 (𝜎) (𝑥𝑖 )). By assumptions, 𝜌                𝑉
                                                                                                         𝛾 (𝜎), thus
𝑉 (𝛾 (𝜎) (𝑥𝑖 )) = 𝜌 (𝑥𝑖 ). Also, as shown above, 𝜌 𝑉 ′      𝛾 (𝜎 ′ ).
    Let 𝛾 ′ = 𝛾 (𝜎 ′ ) [𝑥 1 ↦→ 𝑡 1 , · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ]. Now, for any 𝑥 ∈ dom(𝛾 ′ ), if 𝑥 = 𝑥𝑖 for some 𝑖 then
𝑉 (𝛾 ′ (𝑥)) = 𝑉 ′ (𝑡𝑖 ) = 𝜌 (𝑥𝑖 ). Otherwise, 𝑥 ∈ dom(𝛾 (𝜎 ′ )) and thus 𝑉 ′ (𝛾 ′ (𝑥)) = 𝑉 ′ (𝛾 (𝜎 ′ ) (𝑥)) = 𝜌 (𝑥).
  ′

Therefore 𝜌 𝑉 ′ 𝛾 ′ .
   Therefore h𝐻, 𝛼 \ T, U h𝐻, 𝛼 i 𝜌i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 ′ ]. Using the deﬁnition of 𝛾 ′ and (54), 𝜎 ′ [𝛾 = 𝛾 ′ ] ⊢
𝜙˜ ⊳ 𝜎 ′′ , and by (56), 𝑉 ′ (𝑔(𝜎 ′′ )) = true.
   In addition, as shown before, h𝐻, 𝛼 \ 𝛼,     ˆ 𝜌i  𝜙,                             ˜
                                                       ˜ thus by lemma 9 h𝐻, 𝛼, 𝜌i  𝜙.
   Now by lemma 33, h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 .        ′′

   Since 𝜎 ′′ ⊢ 𝑒 ↓ 𝑡 ⊣ _ and h𝐻, 𝜌i ⊢ 𝑒 ⇓ false, by lemma 29 𝑉 ′ (𝑡) = false. Therefore 𝑉 ′ (𝑔(𝜎 ′′ ) &&
! 𝑡) = 𝑉 ′ (𝑔(𝜎 ′′ )) ∧ ¬𝑉 ′ (𝑡) = true. Therefore
                                     h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′′ [𝑔 = 𝑔(𝜎 ′′ ) && ! 𝑡].
  Now, by deﬁnition, 𝑠 (Σ′ ) = 𝑠 ′ . Therefore h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i corresponds to Σ′ with valuation 𝑉 ′ .
  By deﬁnition 𝜙˜ (Σ′ ) = 𝜙˜′ = 𝜙˜ (Σ). Also, 𝛾 (Σ′ ) = 𝛾 (𝜎 ′′ ) = 𝛾 (𝜎 ′ ) [𝑥 1 ↦→ 𝑡 1 , · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ] by lemma
32 and 𝛾 (𝜎 ′ ) = 𝛾 (𝜎) = 𝛾 (Σ) by lemma 39. Therefore dom(𝛾 (Σ′ )) ⊇ dom(𝛾 (Σ)).
  Thus by lemma 49 h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i is a valid state.
  Case 12. ExecWhileFinish: We have
                   h𝐻, h𝛼 ′ , 𝜌 ′, skipi · h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ i →
                     h𝐻, h𝛼 ′′ , 𝜌 ′, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ i
                   where h𝐻, 𝛼 ′ , 𝜌 ′ i  𝜙˜ and 𝛼 ′′ = 𝛼 ∪ ⌊𝜙⌋  ˜ h𝐻, 𝛼 ′, 𝜌 ′ i .

  By assumptions, the initial state is validated by some Σ and valuation 𝑉 ′ , thus Σ′ = h𝜎 ′ , skip, 𝜙˜ ′ i
for some 𝜎 ′ , 𝜙˜ where h𝐻, 𝛼 ′ , 𝜌 ′ i 𝑉 𝜎 ′ .
  Also, by 33.3, the partial state h𝐻, h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ i is validated by Σ′
and 𝑉 ′ . Thus 32.3 must apply, and thus there is some Σ0 , 𝑉0 , 𝜎0 , 𝜎 ′ , 𝜙˜0 such that
                                                                               0

                                Σ0 = h𝜎0, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′, 𝜙˜0 i
                                  Σ0 is reachable from Π with valuation 𝑉0
                                𝜎0 ⊢ 𝜙˜ ⊲ 𝜎0′ , _,    h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎0′ ,    𝜙˜ ′ = 𝜙,
                                                                                    ˜
                                                                    0

                                      and 𝑉0′ = 𝑉0 [𝜎 ⊢ 𝜙˜ ⊲ 𝜎 ′ , _ | 𝐻 ].
                            ˜ thus by lemma 13h𝐻, ⌊𝜙⌋
  We have h𝐻, 𝛼 ′ , 𝜌 ′ i  𝜙,                     ˜ h𝐻, 𝛼 ′, 𝜌 ′ i , 𝜌 ′ i  𝜙,
                                                                              ˜ and then by lemma 9
                   ˜
h𝐻, 𝛼 ′′ , 𝜌 ′ i  𝜙.
  Also by lemma 19 h𝐻, 𝛼 ′′ , 𝜌i 𝑉 ′ 𝜎0′ .
                                         0
   For some 𝑘, let 𝑥 1, · · · , 𝑥𝑘 be the list of variables in modiﬁed(𝑠). Let 𝑡 1 = fresh, · · · , 𝑡𝑘 = fresh,
let 𝛾ˆ = 𝛾 (𝜎0 ) [𝑥 1 ↦→ 𝑡 1, · · · , 𝑥𝑘 ↦→ 𝑡𝑘 ], and let 𝑉ˆ0′ = 𝑉0′ [𝑡 1 ↦→ 𝜌 ′ (𝑥 1 ), · · · , 𝑡𝑘 ↦→ 𝜌 ′ (𝑥𝑘 )].
111:110                                                                                         C. Zimmerman, J. DiVincenzo, and J. Aldrich


   𝜌 ′ is contained in the stack frame executing the loop body, which is 𝑠, thus for all 𝑥 ∈ dom(𝜌 ′ ),
either 𝜌 (𝑥) = 𝜌 ′ (𝑥) or 𝑥 ∈ modiﬁed(𝑚).
   Also, since 𝜌 𝑉 ′ 𝛾 (𝜎0′ ) and 𝛾 (𝜎0′ ) = 𝛾 (𝜎0 ) by lemma 39, 𝜌 𝑉 𝛾 (𝜎0 ).
                    0                                                  0

   Now, for any 𝑥 ∈ dom(𝛾),   ˆ if 𝑥 = 𝑥𝑖 for some 𝑖, then 𝑉ˆ0′ (𝛾ˆ (𝑥)) = 𝑉ˆ0′ (𝛾ˆ (𝑥𝑖 )) = 𝜌 ′ (𝑥𝑖 ) = 𝜌 ′ (𝑥). Oth-
erwise, 𝑥 ∉ modiﬁed(𝑠), thus 𝜌 ′ (𝑥) = 𝜌 (𝑥), and 𝑥 ∈ dom(𝛾 (𝜎0 )). Thus 𝑉ˆ ′ (𝛾ˆ (𝑥)) = 𝑉0 (𝛾 (𝜎0 ) (𝑥)) =         0
𝜌 (𝑥) = 𝜌 ′ (𝑥𝑖 ) since 𝜌 𝑉 𝛾 (𝜎0 ). Therefore 𝜌 ′                        ˆ Thus h𝐻, 𝛼 ′′ , 𝜌 ′ i
                                                                          𝛾.                                            𝜎0′ [𝛾 = 𝛾 ′ ].
                               0                                  𝑉ˆ0′                                       𝑉ˆ0′
   Therefore by lemma 34 𝜎0′ [𝛾 = 𝛾 ′ ] ⊢ 𝜙˜ ⊳ 𝜎0′′ for some 𝜎0′′ such that 𝑉0′′ (𝑔(𝜎0′′ )) = true where
𝑉0′′ = 𝑉ˆ0′ [𝜎0′ ⊢ 𝜙˜ ⊳ 𝜎0′′ | 𝐻 ].
   Let Σ′0 = h𝜎0′′ , while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ , 𝜙˜0 i. We want to show that


                            Γ ′ = h𝐻, h𝛼 ′′ , 𝜌 ′, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i · S ∗ i

is validated by Σ′0 and 𝑉0′′ .
    Part 33.1: By SVerifyLoop, and since Σ0 is reachable from Π, Π ⊢ Σ0 → Σ′0 . Therefore Σ′0 is
reachable from Π with valuation 𝑉0′′ .
                                       ˜ by lemma 4 T𝜙U
    Part 33.2: Since h𝐻, 𝛼 ′ , 𝜌 ′ i  𝜙,                ˜ h𝐻, 𝜌 ′ i ⊆ 𝛼 ′ . Also, since the stack is well-formed,
𝛼 ′ and 𝛼 are disjoint, thus 𝛼 \ T𝜙˜ U h𝐻, 𝜌 ′ i = 𝛼. Therefore h𝐻, 𝛼 \ T𝜙U   ˜ h𝐻, 𝜌 ′ i , 𝜌i ′ 𝜎 ′ , and now since
                                                                                              𝑉   0
                                                                                                                              0
𝛼 ⊆ 𝛼 ′′ , by lemma lemma 19, and since 𝜌 ′                        𝛾 ′,
                                                           𝑉ˆ0′


                                                     ˜ h𝐻, 𝜌 ′ i , 𝜌 ′ i
                                         h𝐻, 𝛼 ′′ \ T𝜙U                                    𝜎0′ [𝛾 = 𝛾 ′ ].
                                                                                    𝑉ˆ0′


   Now, by lemma 33,

                                                     h𝐻, 𝛼 ′′ , 𝜌 ′ i 𝑉 ′′ 𝜎0′′ .
                                                                                0



   Also, 𝑠 (Σ′0 ) = 𝑠 (Γ ′ ) by construction. Therefore Γ ′ corresponds to Σ′0 .
   Part 33.3: We need to show that the partial state h𝐻, S ∗ i is validated by Σ′0 and 𝑉0′′ . We already
have that h𝐻, S ∗ i is validated by Σ0 and 𝑉0 . Thus one of 32.1, 32.2, or 32.3 must apply.
   If 32.1 applies: Then S ∗ = nil, thus trivially the partial state h𝐻, S ∗ i is validated by Σ′0 and 𝑉0′′ .
   If 32.2 applies: Then S ∗ = h𝛼 ∗ , 𝜌 ∗, 𝑦 = 𝑚(𝑒 1 , · · · , 𝑒𝑘 ); 𝑠 ∗ i · S1∗ for some 𝛼 ∗ , 𝜌 ∗ , 𝑘, 𝑦, 𝑚, 𝑒 1, · · · , 𝑒𝑘 ,
𝑠 , S1∗ . Also, there exists some Σ∗, 𝑉 ∗ , 𝑥 1, · · · , 𝑥𝑘 , 𝑡 1 , · · · , 𝑡𝑘 , 𝜎0, · · · , 𝜎𝑘 , 𝜎 ′ such that
 ∗



                              The partial state h𝐻, S1∗ i is validated by Σ∗ and 𝑉 ∗,
                         Σ∗ is reachable from Π with valuation 𝑉 ∗,                                 𝑠 (Σ∗ ) = 𝑠 (S ∗ ),
                                                  𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                                   ∗
                     𝜎0 = 𝜎 (Σ ),          𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,              ··· ,        𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                                    ′
                             𝜎𝑘 ⊢ pre(𝑚) ⊲ 𝜎 , _,                 h𝐻, 𝛼 , 𝜌 i 𝑉 ∗ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )],
                                                                            ∗        ∗

                                       ∀ 1 ≤ 𝑖 ≤ 𝑘 : 𝑉0 (𝛾 (Σ0 ) (𝑥𝑖 )) = 𝑉 ∗ (𝑡𝑖 ),                   and
                                                    𝜙˜ (Σ0 ) = post(𝑚).
Sound Gradual Verification with Symbolic Execution                                                                111:111


  We want to show that the partial state h𝐻, S ∗ i is validated by Σ′′ and 𝑉 ′′ . Immediately from
above,

                              The partial state h𝐻, S1∗ i is validated by Σ∗ and 𝑉 ∗,
                       Σ∗ is reachable from Π with valuation 𝑉 ∗,                    𝑠 (Σ∗ ) = 𝑠 (S ∗ ),
                                              𝑥 1, · · · , 𝑥𝑘 = params(𝑚),
                                 ∗
                    𝜎0 = 𝜎 (Σ ),       𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, _,          ··· ,   𝜎𝑘 −1 ⊢ 𝑒𝑘 ⇓ 𝑡𝑘 ⊣ 𝜎𝑘 , _,
                                                ′
                              𝜎𝑘 ⊢ pre(𝑚) ⊲ 𝜎 , _,                 ∗      ∗
                                                            h𝐻, 𝛼 , 𝜌 i 𝑉 ∗ 𝜎 ′ [𝛾 = 𝛾 (𝜎0 )].

Also, the frame h𝛼, 𝜌, while 𝑒 invariant 𝜙˜ do 𝑠; 𝑠 ′ i must be executing the body of 𝑚, since
it is in the stack immediately above the frame that contains 𝑦 = 𝑚(𝑒 1, · · · , 𝑒𝑘 ). Therefore, since
𝑥 1, · · · , 𝑥𝑘 are all parameters of 𝑚, modiﬁed(𝑠) cannot contain any of 𝑥 1, · · · , 𝑥𝑘 , since we do not
allow assignment to parameters in a well-formed program. Thus

              ∀1 ≤ 𝑖 ≤ 𝑘 : 𝑉0′′ (𝛾 (Σ′0 ) (𝑥𝑖 )) = 𝑉0′′ (𝛾 (𝜎0′′ ) (𝑥𝑖 ))                             defn. Σ′0
                                                    = 𝑉0′′ (𝛾ˆ (𝑥𝑖 ))                              Lemma 32
                                                    = 𝑉0′′ (𝛾 (𝜎0′ ) (𝑥𝑖 ))                𝑥𝑖 ∉ modiﬁed(𝑠)
                                                    = 𝑉0′′ (𝛾 (𝜎0 ) (𝑥𝑖 ))                          𝐿𝑒𝑚𝑚𝑎39
                                                    = 𝑉0 (𝛾 (𝜎0 ) (𝑥𝑖 ))                              𝑉0 ⊆ 𝑉0′′
                                                    = 𝑉 ∗ (𝑡𝑖 )                                 prev. assump.

   Finally, 𝜙˜ (Σ′0 ) = 𝜙˜ (Σ0 ) by deﬁnition, thus

                                             𝜙˜ (Σ′0 ) = 𝜙˜ (Σ0 ) = post(𝑚).

   Therefore the partial state h𝐻, S ∗ i is validated by Σ′0 and 𝑉0′′ in this case.
   If 32.3 applies: Then S ∗ = h𝜌 ∗, 𝛼 ∗, while 𝑒 ∗ invariant 𝜙˜ ∗ do 𝑠 ∗ ; 𝑠 ∗′ i · S1∗ for some 𝜌 ∗ , 𝛼 ∗ , 𝑒 ∗ , 𝜙˜∗ ,
𝑠 , 𝑠 ∗′ , S1∗ , and there exists some Σ∗ , 𝑉 ∗ , and 𝜎 ′ such that:
 ∗


                               The partial state h𝐻, S1∗ i is validated by Σ∗ and 𝑉 ∗
                        Σ is reachable from Π with valuation 𝑉 ∗
                          ∗
                                                                                    𝑠 (Σ∗ ) = 𝑠 (S ∗ ),
                                 𝜎 (Σ∗) ⊢ 𝜙˜ ∗ ⊲ 𝜎 ′ , _,     h𝐻, 𝛼 ∗, 𝜌 ∗ i 𝑉 ∗ 𝜎 ′      and
                                                       𝜙˜ (Σ∗ ) = 𝜙˜ ∗ .

   Now, by deﬁnition of Σ′0 , 𝜙˜ (Σ′0 ) = 𝜙˜ (Σ0 ) = 𝜙˜ ∗ . Therefore, using the other assumptions given
above, the partial state h𝐻, S ∗ i is validated by Σ′0 and 𝑉0′′ in this case.
   Therefore deﬁnition part 33.3 is satisﬁed.
   Therefore all parts of deﬁnition 33 are satisﬁed. Thus Γ ′ is validated by Σ′0 and 𝑉0′′ , as we wanted
to show.
   Case 13. ExecFold: We have

                      h𝐻, h𝛼, 𝜌, fold 𝑝 (𝑒); 𝑠i · S ∗ i, 𝑉 ′ LΘM𝐻 → h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i

  By assumptions, the initial state is validated by some Σ and valuation 𝑉 ′ , thus
                       ˜ for some 𝜎, 𝜙˜ where h𝐻, 𝛼, 𝜌i
Σ = h𝜎, fold 𝑝 (𝑒); 𝑠, 𝜙i                                   𝜎.
                                                         𝑉
111:112                                                                          C. Zimmerman, J. DiVincenzo, and J. Aldrich


   The only guard that applies is SGuardFold, thus we have
                                𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′ , R,          𝑥 = predicate_params(𝑝),
                                  𝜎 [𝛾 = [𝑥𝑖 ↦→ 𝑡𝑖 ]] ⊢ predicate(𝑝) ⊲ 𝜎 ′′ , R ′ ,
                                    ′

                  and by assumptions             h𝐻, 𝛼i ⊢𝑉 ′ R ∪ R ′          and 𝑉 ′ (𝑔(𝜎 ′′ )) = true
where 𝑉 ′ is the valuation corresponding to this series of judgements, extending 𝑉 (see deﬁnition
40).
  Let 𝑒 1, · · · , 𝑒𝑛 = 𝑒, 𝑡 1 , · · · , 𝑡𝑛 = 𝑡 , and R 1 , · · · , R𝑛 = R. Let 𝜎0 , then for some 𝜎1 , · · · , 𝜎𝑛 we have
                              𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, R 1 , · · · , 𝜎𝑛−1 ⊢ 𝑒𝑛 ⇓ 𝑡𝑛 ⊣ 𝜎𝑛 , R𝑛
where 𝜎𝑛      = 𝜎 ′ . By lemmas 24 and 36 𝑔(𝜎 ′′ )        =⇒ 𝑔(𝜎𝑛 ) =⇒ · · · =⇒ 𝑔(𝜎1 ). Therefore
𝑉 ′ (𝑔(𝜎 ′′ )) = 𝑉 ′ (𝑔(𝜎𝑛 )) = · · · = 𝑉 ′ (𝑔(𝜎1 )) = true. Also, by lemma 23 we have h𝐻, 𝛼i ⊢𝑉 ′ R𝑖 for
all 1 ≤ 𝑖 ≤ 𝑛. Thus, by lemma 26
                             h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ),       ··· ,      h𝐻, 𝜌i ⊢ 𝑒𝑛 ⇓ 𝑉 ′ (𝑡𝑛 )
                              and       h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎1 ,       ··· ,      h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎𝑛 .

Therefore h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ .
   Let 𝛾 ′ = [𝑥 ↦→ 𝑡 ] and 𝜌 ′ = [𝑥 ↦→ 𝑉 ′ (𝑡)]. Then, by construction, 𝜌 ′ 𝑉 ′ 𝛾 ′ . Therefore h𝐻, 𝛼, 𝜌i 𝑉 ′
𝜎 ′ [𝛾 = 𝛾 ′ ].
  From above we have 𝜎 ′ [𝛾 = 𝛾 ′ ] ⊢ predicate(𝑝) ⊲ 𝜎 ′′ , R ′ and h𝛼, 𝜌i ⊢𝐻 R ′′ by lemma 23. Thus,
by lemma 45 h𝐻, 𝛼 \ Tpredicate(𝑝)U h𝐻, 𝜌 ′ i , 𝜌 ′ i 𝑉 ′ 𝜎 ′′ and thus

                             h𝐻, 𝛼 \ Tpredicate(𝑝)U h𝐻, 𝜌 ′ i , 𝜌i 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)].
   Let H′ = H(𝜎 ′′ ); h𝑝, 𝑡i. Expanding deﬁnitions,
                                        𝑉 ′ Lh𝑝, 𝑡 iM𝐻 = Tpredicate(𝑝)U h𝐻, 𝜌 ′ i .
Now h𝐻, 𝛼 \ 𝑉 ′ Lh𝑝, 𝑡 iM𝐻 , 𝜌i 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)], thus
                          ∀ℎ 1 , ℎ 2 ∈ H(𝜎 ′′ ) : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 ′ Lℎ 1 M𝐻 ∩ 𝑉 ′ Lℎ 2 M𝐻 = ∅
and by lemma 16,
                                    ∀ℎ ∈ H(𝜎 ′′ ) : 𝑉 ′ LℎM𝐻 ∩ 𝑉 ′ Lh𝑝, 𝑡 iM𝐻 = ∅.
From these we can deduce that
                            ∀ℎ 1 , ℎ 2 ∈ H′ : ℎ 1 ≠ ℎ 2 =⇒ 𝑉 ′ Lℎ 1 M𝐻 ∩ 𝑉 ′ Lℎ 2 M𝐻 = ∅.
   Also, from lemma 45, h𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]i  predicate(𝑝) since 𝜌 ′ = [𝑥 ↦→ 𝑉 ′ (𝑡)].
   Since h𝐻, 𝛼 \ 𝑉 ′ Lh𝑝, 𝑡 iM𝐻 , 𝜌i 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)],

                          ∀ h𝑝, 𝑡i ∈ H(𝜎 ′′ ) : h𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]i  predicate(𝑝).
From these we can deduce that
                             ∀ h𝑝, 𝑡i ∈ H′ : h𝐻, 𝛼, [𝑥 ↦→ 𝑉 ′ (𝑡)]i  predicate(𝑝).
   Since ﬁeld values are unchanged between H(𝜎 ′′ ) and H′ ,
                                        ∀ h𝑓 , 𝑡, 𝑡 ′ i ∈ H′ : h𝑉 (𝑡), 𝑓 i ∈ 𝛼      and
                                        ∀ h𝑓 , 𝑡, 𝑡 i ∈ H : 𝐻 (𝑉 (𝑡), 𝑓 ) = 𝑉 (𝑡 ′ ).
                                                  ′       ′
Sound Gradual Verification with Symbolic Execution                                                                    111:113


     Therefore h𝐻, 𝛼i 𝑉 ′ H′ , and thus

                                         h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎), H = H′ ].
                                            ˜ By SExecFold 𝜎 ⊢ fold 𝑝 (𝑒); 𝑠 → 𝑠 ⊣ 𝜎 (Σ′ ) (after
   Let Σ′ = h𝜎 ′′ [𝛾 = 𝛾 (𝜎), H = H′ ], 𝑠, 𝜙i.
expanding deﬁnitions). Therefore Π ⊢ Σ → Σ′ by SVerifyStep. Therefore Σ′ is reachable from Π
with valuation 𝑉 ′ .
   Also, as shown before, h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 (Σ′ ), and by deﬁnition 𝑠 (Σ′ ) = 𝑠. Therefore Σ′ corresponds
to h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i.
   By deﬁnition 𝛾 (Σ′ ) = 𝛾 (𝜎) = 𝛾 (Σ) and 𝜙˜ (Σ′ ) = 𝜙˜ = 𝜙˜ (Σ). Therefore by lemma 49 h𝐻, h𝛼, 𝜌, 𝑠i ·
S ∗ i is a valid state.
   Case 14. ExecUnfold: We have
                       h𝐻, h𝛼, 𝜌, unfold 𝑝 (𝑒); 𝑠i · S ∗ i, 𝑉 ′ LΘM𝐻 → h𝐻, h𝛼, 𝜌, 𝑠i · S ∗ i
  By assumptions, the initial state is validated by some Σ and valuation 𝑉 ′ , thus
                         ˜ for some 𝜎, 𝜙˜ where h𝐻, 𝛼, 𝜌i
Σ = h𝜎, unfold 𝑝 (𝑒); 𝑠, 𝜙i                                   𝜎.
                                                            𝑉
  The only guard that applies is SGuardUnfold, thus we have The only guard that applies is
SGuardFold, thus we have

                                      𝜎 ⊢ 𝑒 ⇓ 𝑡 ⊣ 𝜎 ′, R,     𝜎 ′ ⊢ 𝑝 (𝑒) ⊲ 𝜎 ′′ , R ′ ,
                                                                  Ø
                  and by assumptions           h𝐻, 𝛼i ⊢𝑉 ′ R ′ ∪       R and 𝑉 ′ (𝑔(𝜎 ′′ )) = true

     Let 𝑒 1, · · · , 𝑒𝑛 = 𝑒, 𝑡 1 , · · · , 𝑡𝑛 = 𝑡 , and R 1 , · · · , R𝑛 = R. Let 𝜎0 , then for some 𝜎1 , · · · , 𝜎𝑛 we have
                                 𝜎0 ⊢ 𝑒 1 ⇓ 𝑡 1 ⊣ 𝜎1, R 1 , · · · , 𝜎𝑛−1 ⊢ 𝑒𝑛 ⇓ 𝑡𝑛 ⊣ 𝜎𝑛 , R𝑛
where 𝜎𝑛 = 𝜎 ′ . By lemmas 24 and 36 𝑔(𝜎 ′′ ) =⇒ 𝑔(𝜎𝑛 ) =⇒ · · · =⇒ 𝑔(𝜎1 ). Therefore
𝑉 ′ (𝑔(𝜎 ′′ )) = 𝑉 ′ (𝑔(𝜎𝑛 )) = · · · = 𝑉 ′ (𝑔(𝜎1 )) = true. Also, by lemma 23 we have h𝐻, 𝛼i ⊢𝑉 ′ R𝑖 for
all 1 ≤ 𝑖 ≤ 𝑛. Thus, by lemma 26
                               h𝐻, 𝜌i ⊢ 𝑒 1 ⇓ 𝑉 ′ (𝑡 1 ),    ··· ,       h𝐻, 𝜌i ⊢ 𝑒𝑛 ⇓ 𝑉 ′ (𝑡𝑛 )
                                and     h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎1 ,       ··· ,      h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎𝑛 .

Therefore h𝐻, 𝛼, 𝜌i 𝑉 ′ 𝜎 ′ .
  Thus by lemma 45
                             h𝐻, 𝜌, 𝛼i  𝑝 (𝑒)       and     h𝐻, 𝛼 \ T𝑝 (𝑒)U h𝐻, 𝜌 i , .i 𝑉 ′ 𝜎 ′

     Let 𝑥 = predicate_params(𝑝), 𝛾 ′ = [𝑥 ↦→ 𝑡 ], and 𝜌 ′ = [𝑥 ↦→ 𝑉 ′ (𝑡)]. Then, by construction,
𝜌′    𝑉′
         𝛾 ′ . Therefore h𝐻, 𝛼 \ T𝑝 (𝑒)U h𝐻, 𝜌 i , 𝜌 ′ i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 ′ ].
                                                                             Ð
     Now, by deﬁnition, T𝑝 (𝑒)U h𝐻, 𝜌 i = Tpredicate(𝑝)U h𝐻, 𝜌 ′ i ∪ T𝑒U h𝐻, 𝜌 i .
     Therefore Tpredicate(𝑝)U h𝐻, 𝜌 ′ i ⊆ 𝛼 \ T𝑝 (𝑒)U h𝐻, 𝜌 i , thus by lemma 19,

                                 h𝐻, 𝛼 \ Tpredicate(𝑝)U h𝐻, 𝜌 ′ i , 𝜌 ′ i 𝑉 ′ 𝜎 ′ [𝛾 = 𝛾 ′ ]

and h𝜎 ′ [𝛾 = 𝛾 ′ ], 𝐻, 𝛼i 𝑉 ′ 𝜎𝜌 ′ .
  Since h𝐻, 𝛼, 𝜌i  𝑝 (𝑒), by AssertPredicate h𝐻, 𝛼, 𝜌 ′ i  predicate(𝑝).
  Therefore by lemma 34
                          𝜎 ′ [𝛾 = 𝛾 ′ ] ⊢ predicate(𝑝) ⊳ 𝜎 ′′       and 𝑉 ′′ (𝑔(𝜎 ′′ )) = true
111:114                                                               C. Zimmerman, J. DiVincenzo, and J. Aldrich


where 𝑉 ′′ = 𝑉 ′ [𝜎 ′ [𝛾 = 𝛾 ′ ] ⊢ predicate(𝑝) ⊳ 𝜎 ′′ | 𝐻 ]. Also, by lemma 33 h𝐻, 𝛼, 𝜌 ′ i 𝑉 ′′ 𝜎 ′′ , and
thus
                                       h𝐻, 𝛼, 𝜌i 𝑉 ′′ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)].
   Now, by SExecUnfold, 𝜎 ⊢ unfold 𝑝 (𝑒); 𝑠 → 𝑠 ⊣ 𝜎 ′′ [𝛾 = 𝛾 (𝜎)].
                                  ˜ By SVerifyStep Π ⊢ Σ → Σ′ . Therefore Σ′ is reachable from Π
   Let Σ′ = h𝜎 ′′ [𝛾 = 𝛾 (𝜎)], 𝑠, 𝜙i.
with valuation 𝑉 . ′′

   Also, as shown before, h𝐻, 𝛼, 𝜌i 𝑉 ′′ 𝜎 (Σ′ ). Furthermore, 𝑠 (Σ′ ) = 𝑠 by deﬁnition. Thus h𝐻, h𝛼, 𝜌, 𝑠i·
S ∗ i corresponds to Σ′ with valuation 𝑉 ′′ .
   By deﬁnition 𝛾 (Σ′ ) = 𝛾 (𝜎) = 𝛾 (Σ) and 𝜙˜ (Σ′ ) = 𝜙˜ = 𝜙˜ (Σ). Therefore, by lemma 49 h𝐻, h𝛼, 𝜌, 𝑠i ·
  ∗
S i is a valid state.
                                                                                                       
Theorem 3 (Preservation). Let Γ be some dynamic state validated by the Σ and valuation 𝑉 for
some program Π. If Σ ⇀ 𝜎 ′ ⊣ R, Θ with corresponding valuation 𝑉 extending 𝑉 ′ , 𝑉 ′ (𝑔(𝜎 ′ )) =
true, h𝐻, 𝛼 (Γ)i ⊢𝑉 ′ R, and Π ⊢ 𝑉 ′ LΘM𝐻 (Γ) , Γ → Γ ′ then Γ ′ is a valid state.
  In other words, if the dynamic state satisﬁes the matching symbolic checks, and dynamic exe-
cution procedes, then the resulting state is valid.
   Proof. We proceed by cases on the judgement Π ⊢ 𝑉 ′ LΘM𝐻 (Γ) , Γ → Γ ′ .
   Case 1. ExecInit: Then Γ = init and Γ ′ = h∅, h∅, ∅, 𝑠 (Π)i · nili. Since Γ is validated by Σ, then
Σ = init.
   Let Σ′ = hh⊥, ∅, ∅, ∅, truei, 𝑠 (Π), truei. Then by SVerifyInit Π ⊢ init → Σ′ .
   Since Γ ′ has a stack with a sole stack frame, and clearly Σ′ is reachable from Π, in order to
show that Γ ′ is validated by Σ′ it suﬃces to show that Γ ′ corresponds to Σ′ . In turn, since clearly
𝑠 (Γ ′ ) = 𝑠 (Σ′ ), it suﬃces to show that h𝐻 (Γ ′ ), 𝛼 (Γ ′ ), 𝜌 (Γ ′ )i 𝑉 𝜎 (Σ′ ). Since all the requisite sets
or values are trivial, this is immediate from the deﬁnition.
   Case 2. ExecFinal: Then Γ ′ = final and Γ = h𝐻, h𝛼, 𝜌, skipi · nili. Since Γ is validated by Σ,
𝑠 (Γ) = 𝑠 (Σ) = skip. By lemma 47, 𝜎 (Σ) ⊢ 𝜙˜ (Σ) ⊲ 𝜎 ′ , _ for some 𝜎 ′ . Thus Π ⊢ Σ → final by
SVerifyFinal.
   Case 3. ExecStep: Then Γ = h𝐻, Si and Γ ′ = h𝐻 ′ , S ′ i for some 𝐻, S, 𝐻 ′ , S ′ where
h𝐻, Si, 𝑉 ′ LΘM𝐻 → h𝐻 ′ , S ′ i. Therefore Γ ′ is a valid state by lemma 60.
                                                                                                               

Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009
