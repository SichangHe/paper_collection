            Product Programs in the Wild:
        Retrofitting Program Verifiers to Check
               Information Flow Security

              Marco Eilers(B) , Severin Meier, and Peter Müller

                    Department of Computer Science, ETH Zurich,
                                Zurich, Switzerland
                    {marco.eilers,peter.mueller}@inf.ethz.ch



       Abstract. Most existing program veriﬁers check trace properties such
       as functional correctness, but do not support the veriﬁcation of hyper-
       properties, in particular, information ﬂow security. In principle, prod-
       uct programs allow one to reduce the veriﬁcation of hyperproperties to
       trace properties and, thus, apply standard veriﬁers to check them; in
       practice, product constructions are usually deﬁned only for simple pro-
       gramming languages without features like dynamic method binding or
       concurrency and, consequently, cannot be directly applied to verify infor-
       mation ﬂow security in a full-ﬂedged language. However, many existing
       veriﬁers encode programs from source languages into simple intermediate
       veriﬁcation languages, which opens up the possibility of constructing a
       product program on the intermediate language level, reusing the exist-
       ing encoding and drastically reducing the eﬀort required to develop new
       veriﬁcation tools for information ﬂow security.
          In this paper, we explore the potential of this approach along three
       dimensions: (1) Soundness: We show that the combination of an encod-
       ing and a product construction that are individually sound can still be
       unsound, and identify a novel condition on the encoding that ensures
       overall soundness. (2) Concurrency: We show how sequential product
       programs on the intermediate language level can be used to verify infor-
       mation ﬂow security of concurrent source programs. (3) Performance:
       We implement a product construction in Nagini, a Python veriﬁer built
       upon the Viper intermediate language, and evaluate it on a number of
       challenging examples. We show that the resulting tool oﬀers acceptable
       performance, while matching or surpassing existing tools in its combina-
       tion of language feature support and expressiveness.


1    Introduction

Since computer programs increasingly handle sensitive user data and commu-
nicate using encryption, it is vital that programs do not leak secret data such
as private keys to attackers, that is, that they are information ﬂow secure. One
way of formalizing information ﬂow security is noninterference, a so-called 2-
hyperproperty, i.e., a property of pairs of executions of the program.
c The Author(s) 2021
A. Silva and K. R. M. Leino (Eds.) CAV 2021, LNCS 12759, pp. 718–741, 2021.
https://doi.org/10.1007/978-3-030-81685-8_34
                                             Product Programs in the Wild      719

    Noninterference can be checked by type systems [45] and static analyses [22].
However, complex language features (such as concurrency) and noninterference
properties (such as termination sensitivity) generally require the expressiveness
of deductive veriﬁcation. In recent years, many automated and expressive veriﬁ-
cation tools have been developed for a wide range of programming languages, but
most of these tools are limited to trace properties (properties of single program
traces) and cannot prove hyperproperties such as noninterference.
    The problem we address in this paper is how to retroﬁt existing program
veriﬁers to check noninterference. Compared to building noninterference veri-
ﬁers from scratch, which can take years when targeting substantial subsets of
real-world programming languages, this approach would allow us to reuse most
aspects of existing veriﬁers, such as the semantic representation of language fea-
tures and proof search algorithms. Moreover, it naturally allows one to verify
combinations of correctness and noninterference properties.
    In principle, existing program veriﬁers can be used to verify hyperproperties
by reducing them to trace properties via self-composition [6] or product pro-
grams [4,5]. However, self-composition does not allow modular veriﬁcation [48],
and product programs have generally been deﬁned only for simple languages
without features like dynamic method binding or concurrency [4,18]. Applying
product constructions to programs written in complex languages would therefore
require deﬁning and implementing new and complex product constructions for
every new veriﬁer.
    We explore a more eﬃcient approach here: We leverage the fact that most
automatic deductive veriﬁers are organized into a custom frontend, which
encodes a source program into an intermediate veriﬁcation language (IVL),
and a reusable backend, which veriﬁes the IVL program using generic proof
search engines. Boogie [3], Viper [35], and Why3 [21] are examples of such IVLs,
which power a large number of program veriﬁers; for instance Boogie is used by
Dafny [29], VCC [13], Spec# [30], and GPUVerify [8], Why3 [21] by Frama-C [14]
and Krakatoa [20], and Viper [35] by Vercors [10], Prusti [2], and Nagini [17].
The ubiquitiy of this architecture oﬀers a chance to retroﬁt existing veriﬁers to
check noninterference by performing the product construction on the level of the
IVL (an approach that is already used by SymDiﬀ [27] for the related problem
of program equivalence). The resulting architecture, which allows one to reuse
both the frontend and the backend of the existing veriﬁer, is shown in Fig. 1.
    Performing the product construction on the IVL-level has three major advan-
tages over a product construction on the source program: (1) It cleanly separates
the encoding of the source language (which tends to be complex for full-ﬂedged
languages) from the product construction. (2) The product construction is much
simpler since IVLs are small, sequential languages. (3) The product construction
can be reused across all veriﬁers built on the same IVL. Overall, this architecture
therefore has the potential to make existing veriﬁers information ﬂow aware with
substantially less eﬀort than building a new tool from scratch.
    Even though this approach has strong advantages, there are several open
questions that must be addressed to make it useful and widely applicable:
720     M. Eilers et al.




Fig. 1. Proposed architecture for information ﬂow veriﬁers. The existing encoding from
source to IVL (frontend) as well as the proof search (backend) can be reused. The
product construction needs to support only the (relatively small) IVL and can be
reused across diﬀerent veriﬁers.


1. Soundness: Given an IVL encoding and a product construction that are indi-
   vidually sound, is the resulting combination always sound as well?
2. Concurrency: There is a substantial number of veriﬁers that verify concurrent
   source programs by encoding them into (sequential) IVLs. Can we soundly
   verify information ﬂow security of concurrent programs based on the a prod-
   uct program of the sequential IVL encoding?
3. Performance: Product constructions cause a performance penalty for veriﬁca-
   tion. Does this overhead prevent the construction of useful veriﬁcation tools
   in practice?

    In this paper, we answer these three questions. We focus our investigation
on modular product programs [18], a kind of product program that allows mod-
ular veriﬁcation and is well-suited for precise speciﬁcation and veriﬁcation of
information ﬂow security. We make the following contributions:

– We show that the combination of sound IVL encodings and sound product
  constructions can indeed be unsound in practically-relevant cases. We identify
  a novel condition on IVL encodings that ensures the soundness of the overall
  workﬂow. We show how to adjust existing unsound encodings on the example
  of a commonly-used encoding for dynamically-bound method calls (Sect. 3).
– We show for the common case of data race free programs using locks that
  it is possible to verify both possibilistic and probabilistic noninterference for
  concurrent programs using sequential product programs. Furthermore, we
  demonstrate that existing criteria for verifying information ﬂow security are
  insuﬃcient in this setting; we provide alternative criteria that are sound and
  show how to encode them in a product program (Sect. 4).
– We implement the approach for Nagini [17], an automated, modular veriﬁ-
  cation tool for a large subset of Python, built on top of the Viper IVL [35].
  We evaluate the performance impact of the product construction and show
  that, while worse than a custom-made information ﬂow veriﬁer, performance
  is acceptable for real-world use (Sect. 5). Our implementation and evaluation
  are available as an artifact [16].
                                                  Product Programs in the Wild          721

    These results demonstrate that the proposed approach can indeed be used to
retroﬁt an existing veriﬁer to soundly check information ﬂow security, even for
concurrent programs. The resulting tool, made with only a fraction of the eﬀort
required for the development of a new veriﬁer, can compete with custom-made
tools in its expressiveness at an acceptable performance cost.


2     Preliminaries

In this section, we introduce the necessary background about noninterference
and product programs.


2.1   Noninterference

A common way of formalizing information ﬂow security is noninterference [23].
Informally, noninterference speciﬁes that the secret (or high) inputs of a pro-
gram do not inﬂuence the values of its public (or low ) outputs. We will not
deﬁne a formal semantics here, but just assume that there is a steps-to relation
s, σ → s , σ   that relates program conﬁgurations consisting of a store σ and
a statement s.
    We formalize noninterference as a property of pairs of program executions
(that is, a 2-hyperproperty [12]) as follows:

Definition 1. A program s with a set of input variables I and output variables
O, of which some subsets Il ⊆ I and Ol ⊆ O are low, satisﬁes noninterference
iﬀ for all σ1 , σ2 and σ1 , σ2 , if ∀x ∈ Il . σ1 (x) = σ2 (x) and s, σ1  →∗ skip, σ1 
and s, σ2  →∗ skip, σ2  then ∀x ∈ Ol .σ1 (x) = σ2 (x).

   Note that in this deﬁnition (and throughout this paper unless stated other-
wise), we do not consider non-terminating executions, i.e., we focus on verifying
termination-insensitive noninterference.

2.2   Modular Product Programs

Proving hyperproperties requires reasoning about multiple (here, two) execu-
tions of a program. However, hyperproperties can be reduced to properties of a
single execution by using self-composition [6] or product programs [4]. The idea
is to duplicate a program’s state space by creating two renamed copies of all
variables, one for each execution (we write x(i) for the ith renaming of variable
x, and lift this notation to expressions), and to transform each statement so that
it has the eﬀect of the original statement on both copies of the state. Unlike self-
composition, which achieves this eﬀect by simply duplicating every statement,
modular product programs [18] do not duplicate loops and method calls, and
instead encode diﬀering control ﬂow through activation variables, which repre-
sent, for each execution, whether or not it is active (i.e., it executes the code) at
the current point in the program. This approach results in a structural alignment
722       M. Eilers et al.




      Fig. 2. A modular product program (on the right) of the program on the left.


of both program executions, which allows one to use method speciﬁcations and
loop invariants that relate both executions, as we discuss below. We denote the
product of statement s under activation variables p1 and p2 as sp̊ .
    Figure 2 shows an example program and the respective product program. For
both functions, the product program duplicates the parameters of the original
function and adds boolean activation variables p1 and p2. Control structures
like conditionals are encoded by creating a set of new activation variables (lines
4–7). For example, p1t represents whether the ﬁrst execution is active in the then-
branch of the conditional, which is the case if it was active at the beginning of
the function and the if-condition is true for the ﬁrst execution. Conversely, p2e
represents whether the second execution is active in the else-branch. Primitive
statements like assignments are then executed under the condition that their
execution is active at the current point in the execution (lines 8–11). Crucially,
the method call to bar is not duplicated; it is executed if at least one execution
is active at the call site, and the values of the current activation variables are
passed to the function, meaning that if an execution is inactive at the call site,
no state changes will be performed for that execution in the called method.
    Because a single method call in the product represents the calls from both
executions, one can reason about method calls modularly in terms of relational
speciﬁcations, i.e., speciﬁcations that relate behavior of two executions of the
method, as opposed to unary speciﬁcations that describe only a single execution.
Relational speciﬁcations are encoded as ordinary speciﬁcations in the product
program that relate parameters from the two diﬀerent executions.
    As an example, assume that bar prints the value of its input z, which must
therefore be low. We can express this as a (relational) precondition low(z), which
can be encoded as the precondition p1 ∧ p2 ⇒ z1 = z2 in the product of bar.
    Events the attacker can observe (such as I/O) must not happen depending on
a secret, to avoid leaking secret data. It is, thus, useful to express in speciﬁcations
that the control ﬂow at the current program point is low, i.e., whether the current
statement is executed does not depend on secret data. This property is denoted in
speciﬁcations as lowEvent. We generally write P p̊ for the encoding of assertion
P under activation variables p1 and p2; lowEvent p̊ is then deﬁned as p1 = p2.
                                              Product Programs in the Wild       723

    A unary (that is, non-relational) predicate Q, such as a standard method
pre- or postcondition, is encoded in the product program as applying to each
active execution, i.e., Q p̊ is deﬁned as p1 ⇒ Q(1) ∧ p2 ⇒ Q(2) .
    Compared to type systems and taint analyses, veriﬁcation based on product
programs allows for much more precise reasoning. Assume for example that foo’s
parameter x is high. Nonetheless, we can show that the example does not leak
information, since the precondition of bar, low(z), will always be fulﬁlled (y > 0
is true independently of the value of x). In contrast, security type systems would
ﬂag y as high, since it is assigned to under a high guard, leading to imprecision.
    In addition to ordinary noninterference, modular product programs can also
be used to encode more advanced security properties, including termination-
sensitive noninterference, value-dependent sensitivity [36], and a form of declas-
siﬁcation [18].


3     Sound Products of IVL Encodings
In this section, we address the ﬁrst question from the introduction, namely,
whether we can soundly combine an existing encoding into an IVL with a product
construction. We ﬁrst describe the proposed architecture in greater detail. Then
we show a potential soundness issue and deﬁne a suﬃcient criterion on the IVL
encoding for the entire approach to be sound. Finally, we discuss an example of
a common encoding pattern that violates the criterion, show that it is indeed
unsound, and propose an alternative sound encoding.

3.1   Proposed Architecture
The architecture proposed in the introduction (Fig. 1) enables the construction of
information ﬂow aware veriﬁers with relatively little eﬀort, by reusing most of the
frontend encoding of the source language to an IVL as well as the entire backend
proof search. The only major change that is necessary is that the frontend and
potentially the IVL have to be extended to allow for the use of information ﬂow
assertions in speciﬁcations. Crucially, the frontend does not have to know their
meaning; it can treat relational source-level assertions like low(e) like ordinary
unary predicates and simply translate them to their counterparts on the IVL
level. IVL-level relational assertions will then be translated to ordinary assertions
during the product transformation.
    In the remainder of this paper, we will generally assume that the existing
IVL encoding is used unchanged, and point out when changes need to be made.

3.2   Soundness Issue
Surprisingly, combining a sound encoding from source language to IVL with
a sound IVL-level product construction may result in a veriﬁcation technique
that is unsound in the presence of relational speciﬁcations. Consider the source
program in Fig. 3 (left), where P is some predicate.
724     M. Eilers et al.




Fig. 3. Example of an encoding that is unsound in our setting. The program on the left
can be encoded into a conditional statement (identical to the source program, modulo
language syntax) or to the program on the right; the latter leads to unsoundness if P
is a relational predicate.


    A frontend could encode the body of foo into an identical (modulo syntax)
conditional statement on the IVL level (assuming the IVL provides conditionals,
assignments, and assert statements). Alternatively, it could produce the encoding
shown in Fig. 3 (right), which directly asserts a suﬃcient precondition of the
source program. If P is a unary predicate, both encodings are sound: If they
verify, the original program is correct. However, if P(y) is a relational predicate,
for instance, low(y), then the encoding on the right is unsound : low(5) and low(7)
are trivially true (since 5 = 5 and 7 = 7), so the assertion in the encoded program
trivially passes, yet the original program is clearly incorrect: If x is greater than
7 in one execution but less in the other, y will have diﬀerent values in both
executions, and will therefore not be low.
    The underlying reason is that the encoding on the right does not encode
the exact behavior of the source program; it encodes a veriﬁcation condition
computed by the frontend that is sound if assertions are unary, but may not be
sound for relational assertions.
    We will now (1) formalize this intuition and derive a suﬃcient condition for
the soundness of an encoding in this approach, and (2) show an example of this
problem occurring in real frontends, and describe how it can be solved.


3.3   Soundness Criterion

We write Σ and S for states and statements of the source language, and σ and s
for states and statements of the IVL. States may contain, for example, a mutable
heap and a variable store. For simplicity, we assume that both source and IVL
statements contain a statement skip that represents a ﬁnished computation. We
also assume that there is a small-step transition relation → for both languages,
and that the standard notion of Hoare triple validity  {P }s{Q} is deﬁned for
the IVL. We let P and Q range over (source and IVL level) assertions from a
standard assertion language extended with low(e) and lowEvent, and assume a
standard deﬁnition of assertion validity for pairs of states.
    We deﬁne an encoding to be a triple α, ∼=, β, where α : S → s is an encoding
from source statements to statements of the target language (i.e., the IVL), β
similarly encodes assertions to the target language, and ∼
                                                         = relates source language
states to corresponding target language states.
                                                Product Programs in the Wild         725

   We ﬁrst deﬁne the desired relational soundness property, which expresses
that if an encoded Hoare triple holds for the encoded program, then the original
property holds for all pairs of executions of the source program:
Definition 2. α, ∼=, β is relationally sound iﬀ, for all S, Σ1 , Σ2 , Σ1 , Σ2 , P, Q,
if  { β(P ) }α(S)p̊ { β(Q) p̊ } and Σ1 , Σ2  P and S, Σ1  →∗ skip, Σ1 
             p̊

and S, Σ2  →∗ skip, Σ2 , then Σ1 , Σ2  Q.
    Product programs represent the operational behavior of two program execu-
tions by the operational behavior of a single product program execution. The
unsoundness shown before is caused by the fact that the encoding into the IVL
does not reﬂect the operational behavior of the conditional statement (replacing
it by an assertion of a suﬃcient precondition) and, thus, the resulting product
does not soundly reﬂect two executions of the source program.
    We call an encoding that preserves the operational behavior of the source
program operational : It encodes every step of the source program into some
number of steps of the target program so that c initial states result in matching
end states. Similarly, it encodes speciﬁcations from the source level into target-
level speciﬁcations that hold in matching states. We can formalize this intuition
by requiring that the source and target programs are connected by the simulation
relation ∼
         =:
Definition 3. α, ∼ =, β is an operational encoding if: (1) for all Σ, Σ  , σ, S, S  ,
if S, Σ → S , Σ  and Σ ∼
                 
                              = σ, then α(S), σ →∗ α(S  ), σ   for some σ  s.t.
    ∼                ∼
Σ = σ , and (2) if Σ = σ then Σ  P iﬀ σ  β(P ).
    Note that this notion allows the encoding to overapproximate the behaviors
of the source program, i.e., admit steps that are not possible on the source level,
but not vice versa.
    For the example in Fig. 3, it is easy to see that this criterion is fulﬁlled by
the left encoding: the source and IVL programs are identical (modulo syntax),
matching states are identical states (modulo state encodings), and the behav-
ior of both programs is identical. The encoding on the right, however, is not
operational: While the left program modiﬁes the state, the right program never
performs any state modiﬁcation.
    We now show that operationality is suﬃcient for relational soundness:
Theorem 1. If α, ∼
                  =, β is operational then it is relationally sound.
Note that operationality is a suﬃcient but not necessary condition; encodings of
veriﬁcation conditions may be sound for relational veriﬁcation as well. The main
advantage of applying the operationality criterion instead of directly reasoning
about relational soundness is that, since operationality represents the simple
notion that the IVL program performs equivalent steps and equivalent state
changes to the source program, it is intuitive and easy to check whether a given
encoding is operational. Additionally, some encodings (like the one Vercors uses
for parallel blocks) are not operational, but can be seen as simpliﬁed versions of
a possible operational encoding that generate the same proof obligations; these
can also be quickly identiﬁed as relationally sound.
726     M. Eilers et al.

3.4   Practical Relevance

In most existing frontends, the encoding of virtually all source language con-
structs is operational; the main appeal of IVLs is, after all, that frontends do
not have to compute veriﬁcation conditions, but can instead “compile” input pro-
grams into an IVL without worrying about the veriﬁcation process itself. How-
ever, many frontends still use non-operational encodings at least for some lan-
guage constructs. Examples for this are VCC’s encoding of local blocks, Dafny’s
encoding of calls on traits, Prusti’s encoding for loops, and Nagini’s encoding of
dynamically-bound calls, which we will discuss in detail in the next subsection.
Additionally, as we will discuss in Sect. 4, all encodings of concurrent source
languages into sequential IVLs necessarily have some non-operational elements.
    Where non-operational encodings are used, this is often intentional to enable
modular veriﬁcation, since operational encodings for some language constructs
are inherently non-modular (see the example in the next subsection). In prac-
tice, one can therefore use the operationality criterion to quickly check that the
existing encoding is sound for the vast majority of source language statements,
and subsequently check the few remaining ones for relational soundness in detail.


3.5   Example: Dynamically-Bound Calls

In this section, we show a real example of an unsound encoding of dynamically-
bound calls that violates the operationality criterion, and show how to derive a
sound alternative.
     Statically-bound method calls, i.e., calls whose exact target is ﬁxed at com-
pile time, can be encoded as procedure calls on the IVL level, which yields an
operational encoding if the operational semantics of the IVL treats calls analo-
gously to the source semantics. The IVL veriﬁer might later reason about calls in
terms of pre- and postconditions instead of actually performing a call, but this
transformation is not relevant here as long as the product program is constructed
before such a desugaring step.
     However, the same approach does not work for dynamically-bound calls,
i.e., calls whose target is chosen at runtime based on the type of the call’s
receiver. Since the implementation to be executed is generally not known during
modular veriﬁcation, it is not possible to encode dynamically-bound calls as
procedure calls with the usual operational semantics (and existing IVLs do not
oﬀer dynamically-bound calls). Therefore, dynamically-bound calls are typically
(e.g., in Dafny and Nagini) directly encoded using the method speciﬁcation.
Additional, separate proof obligations enforce that all overrides of a method
respect behavioral subtyping [33], i.e., live up to the speciﬁcation of the overridden
method.
     Consider method A.foo in Fig. 4 (left), which returns a constant integer and
guarantees in its postcondition that the result is low. A dynamically-bound call
a.foo(), where a has the static type A, will be encoded as an assertion of the
(here, trivial) precondition of A.foo, followed by an assumption of the postcon-
dition (we ignore side eﬀects here for simplicity).
                                                Product Programs in the Wild        727




Fig. 4. Example of a problematic method override. B.foo overrides A.foo and has a
compatible speciﬁcation, but the implementations return diﬀerent values.


    This encoding is sound if foo has a purely unary speciﬁcation, without any
relational parts. However, it does not fulﬁll our operationality criterion: The
semantics of the source program performs a call to an implementation of foo
(selected based on the dynamic type of a), whereas the IVL encoding directly
encodes the proof obligations (similarly to the example from Fig. 3).
    Since the encoding is not operational, we have to check whether it is still
relationally sound. Method B.foo in Fig. 4 (right), which overrides A.foo, shows
that it is not. B.foo’s contract is identical with that of A.foo, so behavioral
subtyping holds trivially. B.foo’s implementation satisﬁes the contract because
it also returns a constant (but, importantly, a diﬀerent one). Now, if a client
calls a.foo() and, depending on a secret, the dynamic type of a is either A or B,
then, depending on the secret, the result will be either 0 or 1. With the standard
encoding of dynamically-bound calls outlined above, however, the client will
assume the postcondition of A.foo and will therefore incorrectly conclude that
the returned result is low.
    To avoid this unsoundness while retaining the ability to use relational speciﬁ-
cations1 , the problematic encoding must be replaced, either with an operational
one, or with a diﬀerent non-operational encoding that is sound for relational spec-
iﬁcations. The former option is not applicable here: An operational encoding for
dynamically-bound calls would essentially have to case split on the dynamic type
of the receiver and invoke the appropriate override. Since such an encoding is
inherently non-modular (all possible overrides need to be known), we follow the
alternative option: we give an example of a non-operational, but sound encoding.
    For our new encoding we exploit the fact that the standard encoding is
unsound only if the two executions of the program resolve the dynamically-
bound call to two diﬀerent implementations, that is, if the dynamic types of the
receiver diﬀer in the two executions. We reﬂect this observation by adjusting
the encoding of pre- and postconditions as follows: (1) If the postcondition of
a method guarantees that an expression is low, we assume this at the call site
only if the dynamic type of the receiver is also low, that is, the calls in the two
program executions are resolved to the same implementation. (2) Similarly, if a
precondition requires that the call is a low event, we enforce that the receiver
type is low in addition to the usual criterion for low events. Low events typically
perform observable behavior such as I/O; it is therefore important that the same
observable behavior is produced, independent of the receiver type. The meaning
of low-assertions in preconditions remains unchanged, because the requirement of
1
    One could, of course, forbid the use of relational speciﬁcations in some places to
    trivially avoid the unsoundness; this, however, is typically not useful in practice.
728     M. Eilers et al.

a method to receive low arguments is independent of the invoked implementation
and must, thus, not be weakened. lowEvent-assertions are generally not allowed
in postconditions, where they add no expressiveness.
    We encode this adjustment as follows:

         low(e) p̊postr = (p(1) = p(2) ∧ type(r(1) ) = type(r(2) )) ⇒ e(1) = e(2)
       lowEvent p̊prer = p(1) = p(2) ∧ type(r(1) ) = type(r(2) )

where type(e) represents the dynamic type of expression e, P p̊postr is the encod-
ing of P in the postcondition of a call with receiver r, and P p̊prer represents the
same for the precondition. We leave the remaining encoding untouched, meaning
that we can summarize the resulting encoding as follows:

1. We keep the existing check for behavioral subtyping for all overrides; this
   prevents, for example, that A.foo is overridden with a method that simply
   returns a secret value and therefore leaks information into the result.
2. We keep the existing encoding of dynamically-bound calls as an assert fol-
   lowed by an assume, but interpret low(e) in preconditions and lowEvent in
   postconditions as shown above.

   In the example above, this encoding lets the caller assume that the result is
low only if it can prove that the dynamic type of a is low.
   The adjusted encoding is indeed sound:

Theorem 2. Let Sc be of the form x:=r.m(), where r has static type A, and
let preA.m and postA.m be the pre- and postcondition of A.m. Assume that the
implementation of A.m and its overrides fulﬁll their speciﬁcations and satisfy
behavioral subtyping. Then the described encoding of Sc is relationally sound.

   Note that this encoding is incomplete, since it is not aware that two diﬀerent
receiver types can lead to the same implementation being called (e.g., if one
type inherits from the second and does not override the called method). Alter-
native encodings could explicitly represent this possibility. Conversely, one could
approximate further (while remaining sound) by requiring the receiver values to
be low, not just their types, in encodings that do not model dynamic types.


4     Product Programs and Concurrency
Automated veriﬁcation of information ﬂow security for concurrent programs is
challenging because one needs to reason about a pair of executions that may have
diﬀerent thread interleavings. In fact, we are aware of only one tool that currently
allows this, SecC, which automates SecCSL, a concurrent separation logic for
information ﬂow security proofs [19]. A product construction applied directly
to concurrent programs would have to faithfully represent all combinations of
potential thread interleavings, which makes veriﬁcation infeasible. Consequently,
to the best of our knowledge, no such product construction exists.
                                             Product Programs in the Wild      729

    For trace properties, many existing veriﬁers avoid reasoning about all possible
thread interleaving by employing a program logic (such as concurrent separation
logic [38]) that essentially reduces veriﬁcation to sequential reasoning and allows
concurrent veriﬁcation problems to be encoded into sequential IVLs. Examples
for such veriﬁers include Vercors and Nagini (using the Viper IVL), as well as
Chalice [32], VCC, and Spec# (using the Boogie IVL).
    In this section, we show how to use IVL-level product programs to extend
such veriﬁers to handle information ﬂow. We ﬁrst describe how existing IVL
encodings for concurrent languages work, and subsequently show how we can
use similar principles to apply an IVL-based product construction, and which
additional proof obligations we must fulﬁll to ensure that no ﬂows exist as a
result of concurrency. We will do this for two diﬀerent notions of information
ﬂow security for concurrent programs, possibilistic and probabilistic noninterfer-
ence; however, the principles behind the approach may also extend to alternative
notions of information ﬂow security such as observational determinism [49].
    Our goal is to describe a technique that applies to a wide range of source
languages, IVLs, proof techniques, and encodings. Therefore, we focus on the
high-level concepts, instead of formalizing them for one speciﬁc setting.

4.1   Concurrent IVL Encodings
Since all IVLs we are aware of are sequential languages, encodings from con-
current source languages to IVLs do not model the exact behavior of the origi-
nal language, in particular, the aforementioned thread interleavings (i.e., these
encodings are non-operational). Instead, they encode a veriﬁcation condition
that ensures that the original program is correct for every possible thread inter-
leaving.
    While the exact proof techniques diﬀer between frontends, and can be based
for example on Concurrent Separation Logic (CSL) [38] or ownership [13,24,26],
they generally follow a common pattern [31]: They prove that the source pro-
gram is data race free, which ensures that thread interactions need to be con-
sidered only at well-deﬁned synchronization points, for instance, upon acquiring
or releasing a lock. The code between such interaction points can be considered
to execute without interference from other threads, and thus can be reasoned
about as if it were sequential.
    We focus on locks here, but other synchronization primitives are handled
analogously. Program logics based on CSL or ownership systems formally connect
a lock and the heap locations it protects, such that these locations may be
accessed only while holding the respective lock. In addition, they associate locks
with an invariant that constrains the values of the heap locations it protects.
When acquiring a lock, a thread may assume that this lock invariant holds,
and when releasing a lock, it has to prove that the invariant is reestablished. A
frontend can encode this into an IVL as depicted in Fig. 5.
    Our solution for information ﬂow veriﬁcation in concurrent programs follows
the same basic approach: We exploit that code between lock operations can
be considered to execute without interference, and that we can therefore use
730     M. Eilers et al.




Fig. 5. Standard IVL encoding of lock operations. Inv ( l ) denotes the invariant con-
straining the memory protected by lock l .


ordinary sequential product programs to reason about this code. To capture
the thread interactions at synchronization points, we extend lock invariants to
contain relational assertions (which can prescribe that some values protected by
the lock are low), and add additional checks around lock operations to ensure
that they do not give rise to unwanted information ﬂow.


4.2   Possibilistic Noninterference

For concurrent programs, standard noninterference is too strict a prop-
erty because concurrent programs are usually non-deterministic. One way of
approaching this problem is to instead verify possibilistic noninterference, which
enforces that high information does not inﬂuence the possible values of low out-
puts, i.e., if some combination of low output values is reachable from an initial
state, then the same combination of low output values must still be reachable
using some possible thread schedule after arbitrarily changing the high inputs.
Possibilistic noninterference can be deﬁned as follows:
Definition 4. A program s with a set of input variables I and output variables
O, of which some subsets Il ⊆ I and Ol ⊆ O are low, satisﬁes possibilistic
noninterference iﬀ for all σ1 , σ2 and σ1 , if ∀x ∈ Il . σ1 (x) = σ2 (x) and s, σ1  →∗
skip, σ1  then s, σ2  →∗ skip, σ2  for some σ2 s.t. ∀x ∈ Ol .σ1 (x) = σ2 (x).
    Note that this property allows high inputs to inﬂuence the probability of
diﬀerent outputs and may therefore not be desirable in all scenarios; we discuss
a stronger notion of noninterference in the next subsection.
    Since we build on a proof technique that ensures data race freedom, we can
see each program trace as a sequence of local operations and lock operations by
speciﬁc threads, where (1) every local operation depends only on previous (local
or lock) operations of the same thread, and (2) every lock operation depends
only on the previous local operations of the same thread and all previous lock
operations (of arbitrary threads). As a result, we can (akin to partial order
reduction) rearrange segments freely as long as we retain the overall order of lock
operations and the order of operations of every speciﬁc thread; in particular, we
can rearrange a trace so that it consists of a number of segments, such that in
each segment, one thread executes any number of local operations and then one
lock operation.
                                               Product Programs in the Wild        731




Fig. 6. Statement encoding for possibilistic information ﬂow security. For loops, we
check that the loop guard is low, ensuring that termination is also low.


    Based on this observation, we impose proof obligations that ensure the fol-
lowing property: For every program trace with some schedule and some low and
high inputs, and for arbitrary diﬀerent high inputs, there exists a second trace
such that: (1) Both traces include the same lock operations performed by the
same threads, in the same order, and (2) at each lock operation, the lock’s invari-
ant holds; in particular, the relational assertions of the lock invariant correctly
relate the state protected by the lock in both traces.
    To enforce this property, we devise four proof obligations that can be checked
thread-locally:

1. Every lock operation o is a low event, i.e., if a thread executes o in the ﬁrst
   execution, it will also execute o in the second execution.
2. Termination of the local code before the lock operation does not depend on
   secret data; i.e., if lock operation o is reached in the ﬁrst trace, it will also be
   reached in the second trace.
3. o operates on the same lock in both executions, i.e., the lock is low.
4. If o releases the lock, i.e., makes a new lock state public, this lock state fulﬁlls
   the relational invariant, meaning that heap operations meant to be low are
   indentical in both executions after the lock operation.

Note that, even though the lock operations of both traces are closely aligned,
their local operations may diﬀer. For instance, a thread may branch on a high
guard as long as no lock operation is performed before the control ﬂow re-joins.
    The above checks are suﬃcient to satisfy Deﬁnition 4. The proof goes by
induction on the number of segments of the traces and leverages the soundness
of sequential veriﬁcation within each segment.

Encoding. The aforementioned checks can simply be checked as part of the
encoding of lock operations. We adjust the encoding from Fig. 5 for possibilistic
noninterference as shown in Fig. 6. For thread acquire and release, the assertions
of lowEvent and low(l) directly ensure properties (1) and (3). Assuming and
asserting the lock invariant works as in the standard IVL encoding for concurrent
programs, but now this invariant can be relational, ensuring property (4). The
condition on while loops is used to ensure property (2), which can be done simply
732     M. Eilers et al.




Fig. 7. Possibilistic information ﬂow violation via a secret-dependent lock release. The
Cell state 4 is visible to other threads only if secret is True.


by asserting that the loop condition is low for every loop in the program (we
assume, for simplicity, that there is no inﬁnite recursion).


Discussion. With our veriﬁcation technique, the product construction on the
IVL level does not need to be aware of concurrency in any way; applying the
standard sequential product construction to the updated encoding is suﬃcient
to ensure possibilistic noninterference in concurrent programs.
    To the best of our knowledge, we are the ﬁrst to consider possibilistic infor-
mation ﬂow in a setting with locks, and therefore the ﬁrst to propose that the
order of lock operations must be constrained. The example in Fig. 7 demonstrates
that this requirement is indeed necessary to prevent unwanted information ﬂow:
The CellLock protects the val ﬁeld of a Cell object, which is intended to be low.
The code unconditionally sets the ﬁeld to two constants (ﬁrst to 4, then to 5),
which should be allowed since the constants are low. However, whether the lock
is released while the cell has value 4 depends on a secret. As a result, when a
diﬀerent thread acquires the lock and sees that the value is 4, this leaks that the
secret must have been true.
    Another example that illustrates the requirement to ensure that high data
does not inﬂuence which lock a lock operation accesses can be found in Fig. 8.
Here, two locks are created, and thread 1 acquires the ﬁrst one. Thread 2
acquires, depending on the secret, either the same lock or a diﬀerent one. This
inﬂuences the possible results of the program: If both threads acquire the same
lock, then the print statements of one thread cannot be interleaved with those
of the other, otherwise they can. As a result, if the attacker observes the pattern
1212 (or any other interleaving of 1s and 2s), they know with certainty that the
two threads acquired diﬀerent locks and secret must therefore be False.
    The necessity to prevent termination diﬀerences in a concurrent setting has
been recognized before in work on security type systems [45].
                                                Product Programs in the Wild         733




Fig. 8. Possibilistic information ﬂow violation through locks. If secret is true, both
threads acquire the same lock, and their critical sections cannot be interleaved.




Fig. 9. Example of probabilistic information ﬂow. With a non-deterministic scheduler,
secret does not inﬂuence the set of possible outputs, but a greater secret leads to
higher probability of seeing a ﬁnal cell value of 2.


4.3   Probabilistic Noninterference

Possibilistic noninterference is too imprecise for many applications. Figure 9 illus-
trates the problem: The ﬁnal value of c. val can be either 1 or 2, that is, possi-
bilistic noninterference holds. However, with most schedulers, a ﬁnal value of 2
is much more likely for greater secret values than for lower values because the
assignment of 1 is more likely to happen before the assignment of 2.
    A stronger notion of noninterference that forbids such leaks is probabilistic
noninterference, which requires that two executions from low-equivalent initial
states will produce the same low outputs with the same probabilities.

Definition 5. A program s with a set of input variables I and output variables
O, of which some subsets Il ⊆ I and Ol ⊆ O are low, satisﬁes probabilistic
noninterference iﬀ for all σ1 , σ2 and σ1 , if ∀x ∈ Il . σ1 (x) = σ2 (x) and s, σ1  →∗
skip, σ1  with probability p then s, σ2  →∗ skip, σ2  with probability p for
some σ2 s.t. ∀x ∈ Ol .σ1 (x) = σ2 (x).

   The information ﬂow in Fig. 9 is caused by secret data inﬂuencing the tim-
ing of thread 2, which in turn may aﬀect the relative order of modiﬁcations of
shared variables. To prevent secrets from inﬂuencing the timing of operations, we
additionally assert that every branch condition in the program is low, meaning
that the two executions will always follow the same code path, which leads to
the adjusted encoding in Fig. 10. Note that the check that branch conditions are
low must also be performed for any implicit branches; e.g., with the encoding of
734     M. Eilers et al.




       Fig. 10. Statement encoding for probabilistic information ﬂow security.


dynamically-bound calls shown before, we must now assert that the type of the
receiver of every such call is low. Also note that since we enforce that branches
are low, the lowEvent conditions we showed in the possibilistic encoding will
be trivially fulﬁlled and can be omitted here. However, we still need to assert
that acquired and released lock references are low. This last requirement has not
been discussed in previous work (whereas forbidding high branches is standard
practice in type systems and program logics [36]).
    With this adjusted encoding, probabilistic noninterference can be veriﬁed
using simple assertions in the IVL encoding and subsequently performing a stan-
dard product construction on the IVL level. So, in summary, this approach lets
us extend existing veriﬁers for concurrent programs to verify both possibilistic
and probabilistic noninterference with very small changes in the frontend, and
without requiring any changes on the level of the IVL (except the ability to write
relational speciﬁcations) and the product construction.


5     Implementation and Evaluation

In this section, we evaluate the performance of the proposed architecture, by
extending the previously information ﬂow unaware Nagini veriﬁer for Python [17]
according to our design. We will ﬁrst brieﬂy describe Nagini and the adaptations
we needed to make, then evaluate the performance overhead generated by the
product transformation, and subsequently evaluate the implementation on a
number of information ﬂow examples, comparing it to SecC [19] in the process.

5.1   Nagini

Nagini is an automated veriﬁer for statically-typed Python 3 programs. It sup-
ports a large subset of the Python language, comprising features like exception
handling, polymorphism, dynamic ﬁeld creation, and concurrency. Reasoning
about some of these features is quite intricate even without the overhead of a
product construction, so we believe that Nagini is a good target to evaluate the
performance of the proposed architecture for veriﬁers for complex languages.
                                                Product Programs in the Wild        735

    Nagini encodes Python programs and their speciﬁcations into the Viper IVL
[35], and then uses Viper’s backend veriﬁers to automatically verify those pro-
grams using the Z3 SMT solver [34]. For concurrent programs, Nagini uses
an encoding similar to the one described in Sect. 4, using implicit dynamic
frames [44] (a ﬂavor of separation logic [38,40]) to prove data race freedom; as a
result, we could modify its existing encoding as shown in Sect. 4 to prove both
possibilistic and probabilistic noninterference for concurrent programs. Nagini’s
existing encoding from Python to Viper is almost entirely operational, we only
adapted the encoding of dynamically-bound calls as shown in Sect. 3.5.
    We extended Nagini’s existing speciﬁcation language to include information
ﬂow speciﬁcations and implemented the modular product program transforma-
tion for 2-hyperproperties for the existing Viper AST (enriched, again, with new
AST nodes for information ﬂow speciﬁcations). For convenience, we also slightly
extended the Viper-based product transformation to directly transform state-
ments that Nagini previously encoded using gotos, such as break and continue
statements. The Viper extension for product programs2 and the extended version
of Nagini3 are open source and available online.


5.2     Performance Overhead of the Product Construction

Our ﬁrst goal is to evaluate the performance overhead generated by the product
construction. We compared the veriﬁcation times of Nagini’s entire functional
test suite with and without the product transformation enabled. The test cases
range from small programs targeting speciﬁc language or speciﬁcation constructs,
to realistic code examples taken from programming tutorials. We ran each test
ﬁve times on a warmed up JVM with the information ﬂow extension enabled and
disabled, without adding any information ﬂow speciﬁcations. Our test system
was a 12 core AMD Ryzen 3900X with 32 GB of RAM running Ubuntu 20.04.1.
    All tests report the same results with and without the product transforma-
tion, meaning that completeness is not impacted by the extension, and that we can
indeed still reason about the entire language subset supported by Nagini. With-
out the product transformation, each test case takes between 3 and 9 s, with the
majority taking between 3 and 5. For most cases, enabling the product construc-
tion leads to an increase in veriﬁcation time that is clearly acceptable (less than
11% for half the tests, less than 30% for three quarters, and less than 100% for 90%
of the tests). For ﬁve test cases, the slowdown is a factor between 5 and 12, and a
single outlier (a quicksort implementation) has a slowdown factor of 17.5 and a
resulting veriﬁcation time of two minutes. We believe that the main reason for the
large slowdown for these particular test cases is the use of quantiﬁers in their spec-
iﬁcations (e.g., to specify properties of all elements in a list). Quantiﬁer handling is
diﬃcult for automated veriﬁcation in general, because unbounded chains of quan-
tiﬁer instantiations can occur during the proof search [15], and this problem seems
to be exacerbated when using the product encoding.
2
    https://github.com/viperproject/silver-sif-extension.
3
    https://github.com/marcoeilers/nagini.
736     M. Eilers et al.

Table 1. Programs evaluated for proving information ﬂow security. We show the total
lines of code (LOC) including implementation and speciﬁcation but excluding whites-
pace, lines of speciﬁcation and proof annotation (Ann.), the property we proved (Prop.,
where NI = noninterference, TNI = termination sensitive noninterference, PS = pos-
sibilistic noninterference) and the veriﬁcation time in seconds (T ), averaged over ﬁve
runs.

                 LOC Ann. Prop.     T
                                                                 LOC Ann. Prop.      T
  banerjee       77   21    NI    5.19
                                                kusters          28   12   NI      4.35
  constanzo      21   12    NI    5.39
                                                naumann          27   17   NI      8.46
  darvas         38   18    NI    4.20
                                                product          39   18   NI     11.35
  example        27   12    NI    5.39
                                                smith            39   21   NI      6.81
  Example-decl   27   12    NI    5.76
                                                terauchi1        10    3   NI      3.59
  Example-term    8    4    TNI   3.59
                                                terauchi3        19    6   NI      3.69
  joana-1-tl     22    7    NI    3.87
                                                terauchi4        18    8   NI      3.97
  joana-2-bl     13    5    NI    3.64
                                                Fig. 4           19    6   NI      3.82
  joana-2-t      12    4    NI    3.72
                                                loop leak [45]   53   17   PS      4.92
  joana-3-bl     36   15    TNI   3.55
                                                high loop        24   11   PS      4.19
  joana-3-br     33   14    TNI   4.60
                                                Fig. 7           23    8   PS      4.37
  joana-3-tl     23    9    TNI   4.50
                                                Fig. 8           36   15   PS      4.40
  joana-3-tr     25   10    TNI   4.19
                                                Fig. 9           34   15   PS      4.57
  joana-13-l     11    2    NI    4.54




   We conclude that the performance impact of the product transformation is
acceptable for most examples, but can be signiﬁcant for programs with complex
functional speciﬁcations.

5.3   Expressiveness and Comparison with SecC
In a second step, we evaluated the expressiveness and performance of our imple-
mentation on a number of challenging examples from the literature. In partic-
ular, we use the examples from the original paper about modular product pro-
grams [18] (sequential examples collected from various previous papers, trans-
lated to Python) and from this paper, both shown in Table 1, as well as examples
taken from SecC [19], the only other automated veriﬁcation tool for concurrent
programs we are aware of, shown in Table 2. The latter table includes the CDDC
case study [36], which models an embedded device that interacts simultaneously
with multiple users and classiﬁed networks. Our examples represent the state
of the art in automated information ﬂow veriﬁcation, requiring semantic rea-
soning that would not be possible in a type system, and using complex infor-
mation ﬂow speciﬁcations including declassiﬁcation, termination-sensitive non-
interference, and value-dependent sensitivity [36]. As mentioned before, these
features can be easily encoded into modular product programs using existing
techniques [18].
    Nagini was able to verify all examples, which demonstrates that our approach
can handle concurrent implementations and express complex noninterference
properties. For the examples from Table 1, Nagini takes only between 3 and 12 s
each. As for the tests from SecC, Nagini takes around ﬁve seconds for three
                                              Product Programs in the Wild       737

Table 2. Comparison with SecC. We show the total lines of code and lines of speci-
ﬁcation for Nagini (LOCN , AnnN ) and SecC (LOCS , AnnS ), the property we proved
(Prop., where NI = noninterference, PR = probabilistic noninterference) and the veri-
ﬁcation time in seconds in both tools (TN and TS ) and in Nagini without the product
construction (TN P ), averaged over ﬁve runs.

                     LOCN AnnN LOCS AnnS Prop. TS                  TN    TN P
      SecC CAV         40      13     50      11    PR      1.33    4.21 3.56
      SecC CDDC      278      105    214      47    PR     21.20   52.20 8.60
      SecC CT          64      35    211     159    PR      1.87    5.41 3.97
      SecC DB        100       48    256     167    NI      2.75 182.60 6.23
      SecC Encrypt     29      12     49      18    NI      1.45    4.76 3.66



of them, 52 s for the CDDC case study, and 183 s for an example involving a
large number of quantiﬁers. We believe that 52 s for a complex case study is
still acceptable, whereas the slowest example demonstrates that extensive use of
quantiﬁers will lead to problematic performance in practice.
     Table 2 shows that SecC is much faster than our implementation. How-
ever, SecC was designed and implemented for information ﬂow veriﬁcation from
scratch, without being able to reuse code from an existing veriﬁer, whereas
our extended Nagini implementation could be implemented with minimal eﬀort.
Besides this crucial diﬀerence, Nagini and SecC diﬀer in many other ways, e.g., in
their supported language features, automation (see the table for required anno-
tations), and speciﬁcation styles. As a result, direct performance comparisons
between the two are diﬃcult; in fact, the unmodiﬁed version of Nagini without
the product construction already takes more time than SecC on four out of ﬁve
examples, likely as a result of the overhead required for modeling more complex
language features.


6   Related Work
There are various existing type systems (e.g., [37,45]) and static analyses
(e.g., [11,22]) for proving information ﬂow security. Compared to veriﬁcation
based on product programs, these are more automated, but less precise. More-
over, there are dedicated program logics for information ﬂow veriﬁcation, such
as SecCSL [19], Covern [36], and Veronica [42], all of which allow proving prob-
abilistic noninterference for concurrent programs based on diﬀerent reasoning
techniques. The implementation of the former in SecC is the only existing tool
that automates information ﬂow veriﬁcation for concurrent programs, see Sect. 5.
    Relational logics, such as Relational Hoare Logic [7] and Cartesian Hoare
Logic [46], allow proving general relational program properties, which includes
noninterference. However, while they tackle a more general problem, they gen-
erally work only for sequential programs. Some tools automate information ﬂow
veriﬁcation using self-composition, e.g., for C [9] and for Java [41]. Compared to
738    M. Eilers et al.

modular product programs, this approach generally does not allow for modular
proofs of information ﬂow security [18,48].
    Modular product programs were presented by Eilers et al. [18]. Other forms of
product programs diﬀer in the way executions are interleaved. While some keep
executions in lock step [4], like modular product programs, others do not describe
a deterministic product construction and allow for arbitrary interleavings [5]. In
particular, Shemer et al. [43] propose property-directed self-composition, which
dynamically determines how to compose and interleave diﬀerent executions
based on the property to be veriﬁed. Similarly, Strichman and Veitsman [47]
propose a product-like construction that interleaves recursive functions whose
executions are not in lock step. Recently, Pick et al. [39] showed how to auto-
matically infer information ﬂow speciﬁcations on modular product programs,
which can likely be combined with the approach examined in this paper.
    To the best of our knowledge, SymDiﬀ [27] for the Boogie IVL is the only
existing tool that constructs product programs on an IVL-level. SymDiﬀ is a
tool for diﬀerential program veriﬁcation, which requires reasoning about pairs of
executions of two diﬀerent (but related) programs and is thus similar to hyper-
property veriﬁcation; in fact, SymDiﬀ has also been used to verify noninterfer-
ence in the past [1]. The authors of SymDiﬀ have proposed diﬀerent techniques
for modularly proving mutual function summaries, similar to relational speciﬁ-
cations, one of which uses a kind of product construction [25,28]. However, they
do not examine potential soundness problems arising from this approach, nor do
they discuss if it can be applied to concurrent source programs.


7     Conclusion
We presented an approach for retroﬁtting existing IVL-based program veriﬁers
to check information ﬂow security using product programs. This approach allows
reusing existing frontends to reduce the required implementation eﬀort. We have
shown when this technique is sound, that it can incorporate concurrency, and
that it can be implemented in an existing veriﬁer with acceptable performance.


References
 1. Almeida, J.B., Barbosa, M., Barthe, G., Dupressoir, F., Emmi, M.: Verifying
    constant-time implementations. In: USENIX Security Symposium, pp. 53–70.
    USENIX Association (2016)
 2. Astrauskas, V., Müller, P., Poli, F., Summers, A.J.: Leveraging Rust types for
    modular speciﬁcation and veriﬁcation. Proc. ACM Program. Lang. 3(OOPSLA),
    147:1–147:30 (2019)
 3. Barnett, M., Chang, B.-Y.E., DeLine, R., Jacobs, B., Leino, K.R.M.: Boogie: a
    modular reusable veriﬁer for object-oriented programs. In: de Boer, F.S., Bon-
    sangue, M.M., Graf, S., de Roever, W.-P. (eds.) FMCO 2005. LNCS, vol. 4111, pp.
    364–387. Springer, Heidelberg (2006). https://doi.org/10.1007/11804192 17
                                                Product Programs in the Wild         739

 4. Barthe, G., Crespo, J.M., Kunz, C.: Relational veriﬁcation using product programs.
    In: Butler, M., Schulte, W. (eds.) FM 2011. LNCS, vol. 6664, pp. 200–214. Springer,
    Heidelberg (2011). https://doi.org/10.1007/978-3-642-21437-0 17
 5. Barthe, G., Crespo, J.M., Kunz, C.: Beyond 2-safety: asymmetric product pro-
    grams for relational program veriﬁcation. In: Artemov, S., Nerode, A. (eds.) LFCS
    2013. LNCS, vol. 7734, pp. 29–43. Springer, Heidelberg (2013). https://doi.org/10.
    1007/978-3-642-35722-0 3
 6. Barthe, G., D’Argenio, P.R., Rezk, T.: Secure information ﬂow by self-composition.
    Math. Struct. Comput. Sci. 21(6), 1207–1252 (2011)
 7. Benton, N.: Simple relational correctness proofs for static analyses and program
    transformations. In: POPL, pp. 14–25. ACM (2004)
 8. Betts, A., Chong, N., Donaldson, A.F., Qadeer, S., Thomson, P.: GPUVerify: a
    veriﬁer for GPU kernels. In: OOPSLA, pp. 113–132. ACM (2012)
 9. Blatter, L., Kosmatov, N., Le Gall, P., Prevosto, V., Petiot, G.: Static and dynamic
    veriﬁcation of relational properties on self-composed C code. In: Dubois, C., Wolﬀ,
    B. (eds.) TAP 2018. LNCS, vol. 10889, pp. 44–62. Springer, Cham (2018). https://
    doi.org/10.1007/978-3-319-92994-1 3
10. Blom, S., Huisman, M.: The VerCors tool for veriﬁcation of concurrent programs.
    In: Jones, C., Pihlajasaari, P., Sun, J. (eds.) FM 2014. LNCS, vol. 8442, pp. 127–
    131. Springer, Cham (2014). https://doi.org/10.1007/978-3-319-06410-9 9
11. Chen, Z., Chen, L., Xu, B.: Hybrid information ﬂow analysis for Python bytecode.
    In: IEEE WISA, pp. 95–100. IEEE Computer Society (2014)
12. Clarkson, M.R., Schneider, F.B.: Hyperproperties. J. Comput. Secur. 18(6), 1157–
    1210 (2010)
13. Cohen, E., Moskal, M., Schulte, W., Tobies, S.: Local veriﬁcation of global invari-
    ants in concurrent programs. In: Touili, T., Cook, B., Jackson, P. (eds.) CAV
    2010. LNCS, vol. 6174, pp. 480–494. Springer, Heidelberg (2010). https://doi.org/
    10.1007/978-3-642-14295-6 42
14. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.: Frama-C:
    a software analysis perspective. Formal Aspects Comput. 27(3), 573–609 (2015).
    https://doi.org/10.1007/s00165-014-0326-7
15. Detlefs, D., Nelson, G., Saxe, J.B.: Simplify: a theorem prover for program check-
    ing. J. ACM 52(3), 365–473 (2005)
16. Eilers, M., Meier, S., Müller, P.: Product Programs in the Wild: Retroﬁtting Pro-
    gram Veriﬁers to Check Information Flow Security (Artifact) (2021). https://doi.
    org/10.5281/zenodo.4724854
17. Eilers, M., Müller, P.: Nagini: a static veriﬁer for Python. In: Chockler, H., Weis-
    senbacher, G. (eds.) CAV 2018. LNCS, vol. 10981, pp. 596–603. Springer, Cham
    (2018). https://doi.org/10.1007/978-3-319-96145-3 33
18. Eilers, M., Müller, P., Hitz, S.: Modular product programs. In: Ahmed, A. (ed.)
    ESOP 2018. LNCS, vol. 10801, pp. 502–529. Springer, Cham (2018). https://doi.
    org/10.1007/978-3-319-89884-1 18
19. Ernst, G., Murray, T.: SecCSL: security concurrent separation logic. In: Dillig,
    I., Tasiran, S. (eds.) CAV 2019. LNCS, vol. 11562, pp. 208–230. Springer, Cham
    (2019). https://doi.org/10.1007/978-3-030-25543-5 13
20. Filliâtre, J.-C., Marché, C.: The Why/Krakatoa/Caduceus platform for deductive
    program veriﬁcation. In: Damm, W., Hermanns, H. (eds.) CAV 2007. LNCS, vol.
    4590, pp. 173–177. Springer, Heidelberg (2007). https://doi.org/10.1007/978-3-
    540-73368-3 21
740     M. Eilers et al.

21. Filliâtre, J.-C., Paskevich, A.: Why3—where programs meet provers. In: Felleisen,
    M., Gardner, P. (eds.) ESOP 2013. LNCS, vol. 7792, pp. 125–128. Springer, Hei-
    delberg (2013). https://doi.org/10.1007/978-3-642-37036-6 8
22. Giﬀhorn, D., Snelting, G.: A new algorithm for low-deterministic security. Int. J.
    Inf. Secur. 14(3), 263–287 (2014). https://doi.org/10.1007/s10207-014-0257-6
23. Goguen, J.A., Meseguer, J.: Security policies and security models. In: IEEE Sym-
    posium on Security and Privacy, pp. 11–20. IEEE Computer Society (1982)
24. Goubault, É., Ledent, J., Mimram, S.: Concurrent speciﬁcations beyond lineariz-
    ability. In: OPODIS. LIPIcs, vol. 125, pp. 28:1–28:16. Schloss Dagstuhl - Leibniz-
    Zentrum für Informatik (2018)
25. Hawblitzel, C., Kawaguchi, M., Lahiri, S.K., Rebêlo, H.: Towards modularly com-
    paring programs using automated theorem provers. In: Bonacina, M.P. (ed.) CADE
    2013. LNCS (LNAI), vol. 7898, pp. 282–299. Springer, Heidelberg (2013). https://
    doi.org/10.1007/978-3-642-38574-2 20
26. Jacobs, B., Piessens, F., Leino, K.R.M., Schulte, W.: Safe concurrency for aggregate
    objects with invariants. In: SEFM, pp. 137–147. IEEE Computer Society (2005)
27. Lahiri, S.K., Hawblitzel, C., Kawaguchi, M., Rebêlo, H.: SYMDIFF: a language-
    agnostic semantic diﬀ tool for imperative programs. In: Madhusudan, P., Seshia,
    S.A. (eds.) CAV 2012. LNCS, vol. 7358, pp. 712–717. Springer, Heidelberg (2012).
    https://doi.org/10.1007/978-3-642-31424-7 54
28. Lahiri, S.K., McMillan, K.L., Sharma, R., Hawblitzel, C.: Diﬀerential assertion
    checking. In: ESEC/SIGSOFT FSE, pp. 345–355. ACM (2013)
29. Leino, K.R.M.: Dafny: an automatic program veriﬁer for functional correctness.
    In: Clarke, E.M., Voronkov, A. (eds.) LPAR 2010. LNCS (LNAI), vol. 6355, pp.
    348–370. Springer, Heidelberg (2010). https://doi.org/10.1007/978-3-642-17511-
    4 20
30. Leino, K.R.M., Müller, P.: Using the Spec# language, methodology, and tools
    to write bug-free programs. In: Müller, P. (ed.) LASER 2007-2008. LNCS, vol.
    6029, pp. 91–139. Springer, Heidelberg (2010). https://doi.org/10.1007/978-3-642-
    13010-6 4
31. Leino, K.R.M., Müller, P.: A basis for verifying multi-threaded programs. In:
    Castagna, G. (ed.) ESOP 2009. LNCS, vol. 5502, pp. 378–393. Springer, Heidelberg
    (2009). https://doi.org/10.1007/978-3-642-00590-9 27
32. Leino, K.R.M., Müller, P., Smans, J.: Veriﬁcation of concurrent programs with
    Chalice. In: Aldini, A., Barthe, G., Gorrieri, R. (eds.) FOSAD 2007-2009. LNCS,
    vol. 5705, pp. 195–222. Springer, Heidelberg (2009). https://doi.org/10.1007/978-
    3-642-03829-7 7
33. Liskov, B., Wing, J.M.: A behavioral notion of subtyping. ACM Trans. Program.
    Lang. Syst. 16(6), 1811–1841 (1994)
34. de Moura, L., Bjørner, N.: Z3: an eﬃcient SMT solver. In: Ramakrishnan, C.R.,
    Rehof, J. (eds.) TACAS 2008. LNCS, vol. 4963, pp. 337–340. Springer, Heidelberg
    (2008). https://doi.org/10.1007/978-3-540-78800-3 24
35. Müller, P., Schwerhoﬀ, M., Summers, A.J.: Viper: a veriﬁcation infrastructure for
    permission-based reasoning. In: Jobstmann, B., Leino, K.R.M. (eds.) VMCAI 2016.
    LNCS, vol. 9583, pp. 41–62. Springer, Heidelberg (2016). https://doi.org/10.1007/
    978-3-662-49122-5 2
36. Murray, T.C., Sison, R., Engelhardt, K.: COVERN: a logic for compositional ver-
    iﬁcation of information ﬂow control. In: EuroS&P, pp. 16–30. IEEE (2018)
37. Myers, A.C., Zheng, L., Zdancewic, S., Chong, S., Nystrom, N.: Jif: Java informa-
    tion ﬂow. Software release (2006). http://www.cs.cornell.edu/jif
                                                Product Programs in the Wild        741

38. O’Hearn, P.W.: Resources, concurrency, and local reasoning. Theor. Comput. Sci.
    375(1–3), 271–307 (2007)
39. Pick, L., Fedyukovich, G., Gupta, A.: Automating modular veriﬁcation of secure
    information ﬂow. In: FMCAD, pp. 158–168. IEEE (2020)
40. Reynolds, J.C.: Separation logic: a logic for shared mutable data structures. In:
    LICS, pp. 55–74. IEEE Computer Society (2002)
41. Scheben, C., Schmitt, P.H.: Veriﬁcation of information ﬂow properties of Java
    programs without approximations. In: Beckert, B., Damiani, F., Gurov, D. (eds.)
    FoVeOOS 2011. LNCS, vol. 7421, pp. 232–249. Springer, Heidelberg (2012).
    https://doi.org/10.1007/978-3-642-31762-0 15
42. Schoepe, D., Murray, T., Sabelfeld, A.: VERONICA: expressive and precise con-
    current information ﬂow security. In: CSF, pp. 79–94. IEEE (2020)
43. Shemer, R., Gurﬁnkel, A., Shoham, S., Vizel, Y.: Property directed self composi-
    tion. In: Dillig, I., Tasiran, S. (eds.) CAV 2019. LNCS, vol. 11561, pp. 161–179.
    Springer, Cham (2019). https://doi.org/10.1007/978-3-030-25540-4 9
44. Smans, J., Jacobs, B., Piessens, F.: Implicit dynamic frames. ACM Trans. Program.
    Lang. Syst. 34(1), 2:1-2:58 (2012)
45. Smith, G.: Principles of secure information ﬂow analysis. In: Christodorescu, M.,
    Jha, S., Maughan, D., Song, D., Wang, C. (eds.) Malware Detection. Advances in
    Information Security, vol. 27. Springer, Boston (2007). https://doi.org/10.1007/
    978-0-387-44599-1 13
46. Sousa, M., Dillig, I.: Cartesian hoare logic for verifying k-safety properties. In:
    PLDI, pp. 57–69. ACM (2016)
47. Strichman, O., Veitsman, M.: Regression veriﬁcation for unbalanced recursive func-
    tions. In: Fitzgerald, J., Heitmeyer, C., Gnesi, S., Philippou, A. (eds.) FM 2016.
    LNCS, vol. 9995, pp. 645–658. Springer, Cham (2016). https://doi.org/10.1007/
    978-3-319-48989-6 39
48. Terauchi, T., Aiken, A.: Secure information ﬂow as a safety problem. In: Hankin,
    C., Siveroni, I. (eds.) SAS 2005. LNCS, vol. 3672, pp. 352–367. Springer, Heidelberg
    (2005). https://doi.org/10.1007/11547662 24
49. Zdancewic, S., Myers, A.C.: Observational determinism for concurrent program
    security. In: CSFW, p. 29. IEEE Computer Society (2003)




Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
     The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
