                                                  Graded Hoare Logic and its Categorical
                                                               Semantics

                                             Marco Gaboardi1(B) , Shin-ya Katsumata2 , Dominic Orchard3 , and
                                                                       Tetsuya Sato4
arXiv:2007.11235v2 [cs.LO] 26 Jan 2021




                                                           1
                                                            Boston University, Boston, USA gaboardi@bu.edu
                                              2
                                                National Institute of Informatics, Tokyo, Japan s-katsumata@nii.ac.jp
                                             3
                                               University of Kent, Canterbury, United Kingdom d.a.orchard@kent.ac.uk
                                                4
                                                  Tokyo Institute of Technology, Tokyo, Japan tsato@c.titech.ac.jp



                                                  Abstract. Deductive verification techniques based on program logics
                                                  (i.e., the family of Floyd-Hoare logics) are a powerful approach for pro-
                                                  gram reasoning. Recently, there has been a trend of increasing the ex-
                                                  pressive power of such logics by augmenting their rules with additional
                                                  information to reason about program side-effects. For example, general
                                                  program logics have been augmented with cost analyses, logics for proba-
                                                  bilistic computations have been augmented with estimate measures, and
                                                  logics for differential privacy with indistinguishability bounds. In this
                                                  work, we unify these various approaches via the paradigm of grading,
                                                  adapted from the world of functional calculi and semantics. We propose
                                                  Graded Hoare Logic (GHL), a parameterisable framework for augment-
                                                  ing program logics with a preordered monoidal analysis. We develop a
                                                  semantic framework for modelling GHL such that grading, logical asser-
                                                  tions (pre- and post-conditions) and the underlying effectful semantics
                                                  of an imperative language can be integrated together. Central to our
                                                  framework is the notion of a graded category which we extend here, in-
                                                  troducing graded Freyd categories which provide a semantics that can in-
                                                  terpret many examples of augmented program logics from the literature.
                                                  We leverage coherent fibrations to model the base assertion language,
                                                  and thus the overall setting is also fibrational.


                                         1   Introduction

                                         The paradigm of grading is an emerging approach for augmenting language se-
                                         mantics and type systems with fine-grained information [40]. For example, a
                                         graded monad provides a mechanism for embedding side-effects into a pure lan-
                                         guage, exactly as in the approach of monads, but where the types are aug-
                                         mented (“graded”) with information about what effects may occur, akin to
                                         a type-and-effect system [24,42]. As another example, graded comonadic type
                                         operators in linear type systems can capture non-linear dataflow and proper-
                                         ties of data use [7,16,44]. In general, graded types augment a type system with
                                         some algebraic structure which serves to give a parameterisable fine-grained pro-
                                         gram analysis capturing the underlying structure of a type theory or semantics.
2      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

Much of the work in graded types has arisen in conjunction with categorical
semantics, in which graded modal type operators are modelled via graded mon-
ads [13,17,25,36,33], graded comonads (often with additional graded monoidal
structure) [7,16,25,43,44], graded ‘joinads’ [36], graded distributive laws between
graded (co)monads [15], and graded Lawvere theories [27].
    So far grading has mainly been employed to reason about functional lan-
guages and calculi, thus the structure of the λ-calculus has dictated the struc-
ture of categorical models (although some recent work connects graded monads
with classical dataflow analyses on CFGs [21]). We investigate here the paradigm
of grading instead applied to imperative languages. As it happens, there is al-
ready a healthy thread of work in the literature augmenting program logics
(in the family of Floyd-Hoare logics) with analyses that resemble notions of
grading seen more recently in the functional world. The general approach is to
extend the power of deductive verification by augmenting program logic rules
with an analysis of side effects, tracked by composing rules. For example, work
in the late 1980s and early 1990s augmented program logics with an analysis of
computation time, accumulating a cost measure [37,38], with more recent fine-
grained resource analysis based on multivariate analysis associated to program
variables [8]. As another example, the Union Bound Logic of Barthe et al. [5]
defines a Hoare-logic-style system for reasoning about probabilistic computa-
tions with judgments ⊢β c : φ ⇒ ψ for a program c annotated by the maximum
probability β (the union bound) that ψ does not hold. The inference rules of
Union Bound Logic track and compute the union bound alongside the standard
rules of Floyd-Hoare logic. As a last example, Approximate Relational Hoare
Logic [2,6,39,48] augments a program logic with measures of the ǫ-δ bounds for
reasoning about differential privacy.
    In this work, we show how these disparate approaches can be unified by
adapting the notion of grading to an imperative program-logic setting, for which
we propose Graded Hoare Logic (GHL): a parameterisable program logic and
reasoning framework graded by a preordered monoidal analysis. Our core con-
tribution is GHL’s underlying semantic framework which integrates grading,
logical assertions (pre- and post-conditions) and the effectful semantics of an
imperative language. This framework allows us to model, in a uniform way, the
different augmented program logics discussed above.
    Graded models of functional calculi tend to adopt either a graded monadic or
graded comonadic model, depending on the direction of information flow in the
analysis. We use the opportunity of an imperative setting (where the λ-calculus’
asymmetrical ‘many-inputs-to-one-output’ model is avoided) to consider a more
flexible semantic basis of graded categories. Graded categories generalise graded
(co)monadic approaches, providing a notion of graded denotation without im-
posing on the placement (or ‘polarity’) of grading.


Outline Section 2 begins with an overview of the approach, focusing on the exam-
ple of Union Bound Logic and highlighting the main components of our semantic
framework. The next three sections then provide the central contributions:
                           Graded Hoare Logic and its Categorical Semantics          3

 – Section 3 defines GHL and its associated assertion logic which provides a
   flexible, parameterisable program logic for integrating different notions of
   side-effect reasoning, parameterised by a preordered monoidal analysis. We
   instantiate the program logic to various examples.
 – Section 4 explores graded categories, an idea that has not been explored much
   in the literature, and for which there exists various related but not-quite-
   overlapping definitions. We show that graded categories can abstract graded
   monadic and graded comonadic semantics. We then extend graded categories
   to Freyd categories (generally used as a more flexible model of effects than
   monads), introducing the novel structure of graded Freyd categories.
 – Section 5 develops the semantic framework for GHL, based on graded Freyd
   categories in a fibrational setting (where coherent fibrations [22] model the
   assertion logic) integrated with the graded Freyd layer. We instantiate the
   semantic model to capture the examples presented in Section 3 and others
   drawn from the literature mentioned above.
An extended version of this paper provides appendices which include further
examples and proof details [14].

2     Overview of GHL and Prospectus of its Model
As discussed in the introduction, several works explore Hoare logics combined
with some form of implicit or explicit grading for program analysis. Our aim is
to study these in a uniform way. We informally introduce of our approach here.
    We start with an example which can be derived in Union Bound Logic [5]:
    ⊢0.05 {⊤} do v1 ← Gauss(0, 1); do v2 ← Gauss(0, 1); v := max(v1 , v2 ) {v ≤ 2}
This judgment has several important components. First, we have primitives for
procedures with side-effects such as do v1 ← Gauss(0, 1). This procedure samples
a random value from the standard normal distribution with mean 0 and variance
1 and stores the result in the variable v1 . This kind of procedure with side
effects differs from a regular assignment such as v := max(v1 , v2 ), which is instead
considered to be pure (wrt. probabilities) in our approach.
    The judgment has grade ‘0.05’ which expresses a bound on the probability
that the postcondition is false, under the assumption of the precondition, after
executing the program; we can think of it as the probability of failing to guarantee
the postcondition. In our example (call it program P ), since the precondition
is true, this can be expressed as: PrJP K(m) [v > 2] ≤ 0.05 where JP K(m) is the
probability distribution generated in executing the program. The grade of P in
this logic is derived using three components. First, sequential composition:
                       ⊢β {ψ} P1 {ψ1 } ⊢β ′ {ψ1 } P2 {φ}
                             ⊢β+β ′ {ψ} P1 ; P2 {φ}
which sums the failure probabilities. Second, an axiom for Gaussian distribution:
                       ⊢0.025 {⊤} do v ← Gauss(0, 1) {v ≤ 2}
4      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

with a basic constant 0.025 which comes from the property of the Gaussian distri-
bution we are considering. Third, by the following judgment which is derivable
by the assignment and the consequence rules, which are the ones from Hoare
Logic with a trivial grading 0 which is the unit of addition:
                  ⊢0 {v1 ≤ 2 ∨ v2 ≤ 2} v := max(v1 , v2 ) {v ≤ 2}
Judgments for more complex examples can be derived using the rules for condi-
tional and loops. These rules also consider grading, and the grading can depend
on properties of the program. For example the rule for conditionals is:
              ⊢β {ψ ∧ eb = tt} P1 {φ} ⊢β {ψ ∧ eb = ff} P2 {φ}
                       ⊢β {ψ} if eb then P1 else P2 {φ}
This allows one to reason also about the grading in a conditional way, through
the two assumptions ψ ∧ eb = tt and ψ ∧ eb = ff. We give more examples later.
    Other logics share a similar structure as that described above for the Union
Bound logic, for example the relational logic apRHL [2], and its variants [48,49],
for reasoning about differential privacy. Others again use a similar structure
implicitly, for example the Hoare Logic to reason about asymptotic execution
cost by Nielson [37], Quantitative Hoare Logic [8], or the relational logic for
reasoning about program counter security presented by Barthe [3].
    To study the semantics of these logics in a uniform way, we first abstract the
logic itself. We design a program logic, which we call Graded Hoare Logic (GHL),
containing all the components discussed above. In particular, the language is a
standard imperative language with conditional and loops. Since our main focus
is studying the semantics of grading, for simplicity we avoid using a ‘while’ loop,
using instead a bounded ‘loop’ operation (loop e do P ). This allow us to focus
on the grading structures for total functions, leaving the study of the interaction
between grading and partiality to future work. The language is parametric in the
operations that are supported in expressions—common in several treatments of
Hoare Logic—and in a set of procedures and commands with side effects, which
are the main focus of our work. GHL is built over this language and an assertion
logic which is parametric in the basic predicates that can be used to reason about
programs. GHL is also parametric in a preordered monoid of grades, and in the
axioms associated with basic procedures and commands with side effects. This
generality is needed in order to capture the different logics we mentioned before.
    GHL gives us a unified syntax, but our real focus is the semantics. To be
as general as possible we turn to the language of category theory. We give a
categorical framework which can capture different computational models and
side effects, with denotations that are refined by predicates and grades describ-
ing program behaviours. Our framework relates different categories (modelling
different aspects of GHL) as summarized by the following informal diagram (1).

                                        İ    /E
                                  P                                            (1)
                                 p              q
                                        I
                                                
                                  V           /C
                            Graded Hoare Logic and its Categorical Semantics           5

This diagram should not be understood as a commutative diagram in CAT as
E is a graded category and hence not an object of CAT.
     The category V models values and pure computations, the category C models
impure computations, P is a category of predicates, and E is a graded category
whose hom-sets are indexed by grades—elements of a preordered monoid. The
presentation of graded categories is new here, but has some relation to other
structures of the same name (discussed in Section 4).
     This diagram echos the principle of refinement as functors proposed by
Melliès and Zeilberger [32]. The lower part of the diagram offers an interpreta-
tion of the language, while the upper part offers a logical refinement of programs
with grading. However, our focus is to introduce a new graded refinement view.
The ideas we use to achieve this are to interpret the base imperative language
using a Freyd category I : V → C (traditionally used to model effects) with
countable coproducts, to interpret the assertion logic with a coherent fibration
p : P → V, and to interpret GHL as a graded Freyd category I˙ : P → E with
homogeneous coproducts. In addition, the graded category E has a functor5 q
into C which erases assertions and grades and extracts the denotation of effectful
programs, in the spirit of refinements. The benefit of using a Freyd category as
a building block is that they are more flexible than other structures (e.g., mon-
ads) for constructing models of computational effects [47,51]. For instance, in
the category Meas of measurable spaces and measurable functions, we cannot
define state monads since there are no exponential objects. However, we can still
have a model of first-order effectful computations using Freyd categories [46].
     Graded Freyd categories are a new categorical structure that we designed
for interpreting GHL judgments (Section 4.2). The major difference from an
ordinary Freyd category is that the ‘target’ category is now a graded category (E
in the diagram (1)). The additional structure provides what we need in order to
interpret judgments including grading.
     To show the generality of this structure, we present several approaches to in-
stantiating the categorical framework of GHL’s semantics, showing constructions
via graded monads and graded comonads preserving coproducts.
     Part of the challenge in designing a categorical semantics for GHL is to
carve out and implement the implicit assumptions and structures used in the
semantics of the various Hoare logics. A representative example of this challenge
is the interpretation of the rule for conditionals in Union Bound Logic that we
introduced above. We interpret the assertion logic in (a variant of) coherent
fibrations p : P → V, which model the ∧∨∃=-fragment of first-order predicate
logic [22]. In this abstract setup, the rule for conditionals may become unsound as
it is built on the implicit assumption that the type Bool, which is interpreted as
1 + 1, consists only of two elements, but this may fail in general V. For example,
a suitable coherent fibration for relational Hoare logic would take Set2 as the
base category, but we have Set2 (1, 1 + 1) ∼  = 4, meaning that there are four global
elements in the interpretation of Bool. We resolve this problem by introducing
5
    More precisely, this is not quite a functor because E is a graded category; see Defi-
    nition 9 for the precise meaning.
6        Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

a side condition to guarantee the decidability of the boolean expression:
    ⊢m {ψ ∧ eb = tt} P1 {φ} ⊢m {ψ ∧ eb = ff} P2 {φ} ψ ⊢ eb = tt ∨ eb = ff
                        ⊢m {ψ} if eb then P1 else P2 {φ}
This is related to the synchronization condition appearing in the relational Hoare
logic rule for conditional commands (e.g., [6]).
    Another challenge in the design of the GHL is how to assign a grade   W to the
loop command loop e do P . We may naı̈vely give it the grade ml , i∈N mi ,
where m is the grade of P , because P is repeatedly executed some finite number
of times. However, the grade ml is a very loose over-approximation of the grade
of loop e do P . Even if we obtain some knowledge about the iteration count e
in the assertion logic, this cannot be reflected in the grade. To overcome this
problem, we introduce a Hoare logic rule that can estimate a more precise grade
of loop e do P , provided that the value of e is determined:
                 ∀0 ≤ z < N. ⊢m {ψz+1 } P {ψz } ψN ⊢ en = ⌈N ⌉
                          ⊢mN {ψN } loop en do P {ψ0 }
This rule brings together the assertion language and grading, creating a depen-
dency from the former to the latter, and giving us the structure needed for a
categorical model. The right premise is a judgment of the assertion logic (un-
der program variables ΓM and pre-condition ψN ) requiring that e is statically
determinable as N . This premise makes the rule difficult to use in practical ap-
plications where e is dynamic. We expect a more “dependent” version of this
rule is possible with a more complex semantics internalizing some form of data-
dependency. Nevertheless, the above is enough to study the semantics of grading
and its interaction with the Hoare Logic structure, which is our main goal here.


3     Loop Language and Graded Hoare Logic
After introducing some notation and basic concepts used throughout, we out-
line a core imperative loop language, parametric in its set of basic commands
and procedures (Section 3.2). We then define a template of an assertion logic
(Section 3.3), which is the basis of Graded Hoare Logic (Section 3.4).

3.1     Preliminaries
Throughout, we fix an infinite set Var of variables which are employed in the
loop language (as the names of mutable program variables) and in logic (to
reason about these program variables).
    A many-sorted signature Σ is a tuple (S, O, ar) where S, O are sets of sorts
and operators, and ar : O → S + assigns argument sorts and a return value sort
to operators (where S + is a non-empty sequence of sorts, i.e., an operator o with
signature (s1 × . . . × sn ) → s is summarized as ar (o) = hs1 , . . . , sn , si ∈ S + ). We
say that another many-sorted signature Σ ′ = (S ′ , O′ , ar′ ) is an extension of Σ
if S ⊆ S ′ and O ⊆ O′ and ar(o) = ar′ (o) for all o ∈ O.
                           Graded Hoare Logic and its Categorical Semantics          7

      Let Σ = (S, · · · ) be a many-sorted signature. A context for Σ is a (possibly
empty) sequence of pairs Γ ∈ (Var×S)∗ such that all variables in Γ are distinct.
We regard Γ as a partial mapping from Var to S. The set of contexts for Σ is
denoted CtxΣ . For s ∈ S and Γ ∈ CtxΣ , we denote by ExpΣ (Γ, s) the set of
Σ-expressions of sort s under the context Γ . When Σ, Γ are obvious, we simply
write e : s to mean e ∈ ExpΣ (Γ, s). This set is inductively defined as usual.
      An interpretation of a many-sorted signature Σ = (S, O, ar) in a cartesian
category (V, 1, ×) consists of an assignment of an object [[s]] ∈ V for each sort
s ∈ S and an assignment of a morphism [[o]] ∈ V([[s1 ]] × · · · × [[sn ]], [[s]]) for
each o ∈ O such that ar(o) = hs1 , . . . , sn , si. Once such an interpretation is
given, we extend it to Σ-expressions in the standard way (see, e.g. [9,45]). First,
for a context Γ = x1 : s1 , · · · , xn : sn ∈ CtxΣ , by [[Γ ]] we mean the product
[[s1 ]]×· · ·×[[sn ]]. Then we inductively define the interpretation of e ∈ ExpΣ (Γ, s)
as a morphism [[e]] ∈ V([[Γ ]], [[s]]).
   Throughout, we write bullet-pointed lists marked with ⋆ for the mathematical
data that are parameters to Graded Hoare Logic (introduced in Section 3.4).

3.2   The Loop Language
We introduce an imperative language called the loop language, with a finite
looping construct. The language is parameterised by the following data:
⋆ a many-sorted signature Σ = (S, O, ar) extending a base signature (S0 , O0 , ar0 )
  of sort S0 = {bool, nat} with essential constants as base operators O0 , shown
  here with their signatures for brevity rather than defining ar 0 directly:

                  O0 = {tt : bool, ff : bool} ∪ {⌈k⌉ : nat | k ∈ N}

  where bool is used for branching control-flow and nat is used for controlling
  loops, whose syntactic constructs are given below. We write ⌈k⌉ to mean the
  embedding of semantic natural numbers into the syntax.
⋆ a set CExp of command names (ranged over by c) and a set PExps of
  procedure names of sort s (ranged over by p) for each sort s ∈ S.
When giving a program, we first fix a context ΓM for the program variables. We
define the set of programs (under a context ΓM ) by the following grammar:

P ::= P ; P | skip | v := e | do c | do v ← p | if eb then P else P | loop en do P

where v ∈ ΓM , eb , en are well-typed Σ-expressions of sort bool and nat under ΓM ,
and c ∈ CExp. In assignment commands, e ∈ ExpΣ (ΓM , Γ (v)). In procedure
call commands, p ∈ PExpΓ (v) . Each program must be well-typed under ΓM .
The typing rules are routine so we omit them.
    Thus, programs can be sequentially composed via ; with skip as the triv-
ial program which acts as a unit to sequencing. An assignment v := e assigns
expressions to a program variable v. Commands can be executed through the
instruction do c which yields some side effects but does not return any value.
8       Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

Procedures can be executed through a similar instruction do v ← p which yields
some side effect but also returns a value which is used to update v. Finally, con-
ditionals are guarded by a boolean expression eb and the iterations of a looping
construct are given by a natural number expression en (which is evaluated once
at the beginning of the loop to determine the number of iterations).
    This language is rather standard, except for the treatment of commands and
procedures of which we give some examples here.
Example 1. Cost Information: a simple example of a command is tick, which
yields as a side effect the recording of one ‘step’ of computation.
    Control-Flow Information: two other simple example of commands are cfTT
and cfFF, which yield as side effects the recording of either true or false to a
log. A program can be augmented with these commands in its branches to give
an account of a program’s control flow. We will use these commands to reason
about control-flow security in Example 3.
    Probability Distributions: a simple example of a procedure is Gauss(x, y),
which yields as a side effect the introduction of new randomness in the program,
and which returns a random sample from the Gaussian distribution with mean
and variance specified by x, y ∈ ΓM . We will see how to use this procedure to
reason about probability of failure in Example 4.
    Concrete instances of the loop language typically include conversion functions
between the sorts in Σ, e.g., so that programs can dynamically change control
flow depending on values of program variables. In other instances, we may have a
language manipulating richer data types, e.g., reals or lists, and also procedures
capturing higher-complexity computations, such as Ackermann functions.


3.3   Assertion Logic

We use an assertion logic to reason about properties of basic expressions. We
regard this reasoning as a meta-level activity, thus the logic can have more sorts
and operators than the loop language. Thus, over the data specifying the loop
language, we build formulas of the assertion logic by the following data:
  ⋆ a many-sorted signature Σl = (Sl , Ol , arl ) extending Σ.
  ⋆ a set Pl of atomic propositions and a function parl : Pl → Sl∗ assigning input
     sorts to them. We then inductively define the set FmlΣl (Γ ) of formulas under
     Γ ∈ CtxΣl as in Figure 1 (over the page), ranged over by ψ and φ.
  ⋆ a CtxΣl -indexed family of subsets Axiom(Γ ) ⊆ FmlΣl (Γ ) × FmlΣl (Γ ).
The assertion logic is a fragment of the many-sorted first-order logic over Σl -
terms admitting: 1) finite conjunctions, 2) countable disjunctions, 3) existential
quantification, and 4) equality predicates. Judgements in the assertion logic have
the form Γ | ψ1 , · · · , ψn ⊢ φ (read as ψ1 ∧ · · · ∧ ψn implies φ), where Γ ∈ CtxΣl
is a context giving types to variables in the formulas ψ1 , · · · , ψn , φ ∈ FmlΣl (Γ ).
The logic has the axiom rule deriving Γ | ψ ⊢ φ for each pair (ψ, φ) of formulas
in Axiom(Γ ). The rest of inference rules of this logic are fairly standard and so
we omit them (see e.g. [22, Section 3.2 and Section 4.1]).
                           Graded Hoare Logic and its Categorical Semantics             9

The set FmlΣl (Γ ) of formulas under Γ ∈ CtxΣl is inductively defined as follows:
 1. For all p ∈ Pl and parl (p) = s1 · · · sn and ti : ExpΣl (Γ, si ) (1 ≤ i ≤ n) implies
    p(t1 , · · · , tn ) ∈ FmlΣl (Γ )
 2. For all s ∈ Sl and t, u ∈ ExpΣl (Γ, s), t = u ∈ FmlΣlV(Γ ).
 3. For all finite families {φi ∈ FmlΣl (Γ )}i∈Λ , we have φi W ∈ FmlΣl (Γ ).
 4. For all countable families {φi ∈ FmlΣl (Γ )}i∈Λ , we have φi ∈ FmlΣl (Γ ).
 5. For all φ ∈ FmlΣl (Γ, x : s), we have (∃x : s . φ) ∈ FmlΣl (Γ ).
                           Fig. 1. Formula formation rules

   In some of our examples we will use the assertion logic to reason about
programs in a relational way, i.e., to reason about two executions of a program
(we call them left and right executions). This requires basic predicates to manage
expressions representing pairs of values in our assertion logic. As an example, we
could have two predicates eqvh1i , eqvh2i , that can assert the equality of the left
and right executions of an expression to some value, respectively. That is, the
formula eqvh1i (eb , true), which we will write using infix notation eb h1i = true,
asserts that the left execution of the boolean expression eb is equal to true.


3.4   Graded Hoare Logic

We now introduce Graded Hoare Logic (GHL), specified by the following data:

 ⋆ a preordered monoid (M, ≤, 1, ·) (pomonoid for short) (where · is monotonic
   with respect to ≤) for the purposes of program analysis, where we refer to
   the elements m ∈ M as grades;
 ⋆ two functions which define the grades and pre- and post-conditions of com-
   mands CExp and procedures PExp:

      Cc : FmlΣl (ΓM ) × M → 2CExp
      Cps : FmlΣl (ΓM ) × M × FmlΣl (r : s) → 2PExps          (s ∈ S ∧ r 6∈ dom(ΓM ))

The function Cc takes a pre-condition and a grade, returning a set of command
symbols satisfying these specifications. A command c may appear in Cc (φ, m) for
different pairs (φ, m), enabling pre-condition-dependent grades to be assigned to
c. Similarly, the function Cps takes a pre-condition, a grade, and a postcondition
for return values, and returns a set of procedure names of sort s satisfying these
specifications. Note, r is a distinguished variable (for return values) not in ΓM .
The shape of Cc and Cc as predicates over commands and procedures, indexed
by assertions and grades, provides a way to link grades and assertions for the
effectful operations of GHL. Section 3.5 gives examples exploiting this.
    From this structure we define a graded Hoare logic by judgments of the form:
⊢m {φ} P {ψ} denoting a program P with pre-condition φ ∈ FmlΣl (ΓM ), post-
condition ψ ∈ FmlΣl (ΓM ) and analysis m ∈ M . Graded judgments are defined
inductively via the inference rules given in Table 1. Ignoring grading, many of the
rules are fairly standard for a Floyd-Hoare program logic. The rule for skip is
standard but includes grading by the unit 1 of the monoid. Similarly, assignment
10        Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato


                         ⊢m {ψ} P1 {ψ1 } ⊢m′ {ψ1 } P2 {φ}
     ⊢1 {ψ} skip {ψ}          ⊢m·m′ {ψ} P1 ; P2 {φ}            ⊢1 {ψ[e/v]} v := e {ψ}

                                                   Γ (v)
              f ∈ Cc (ψ, m)                 p ∈ Cp M (ψ, m, φ)
             ⊢m {ψ} do c {ψ}     ⊢m {ψ} do v ← p {(∃v : ΓM (v) . ψ) ∧ φ[v/r]}

                  ΓM | ψ ′ ⊢ ψ   m ≤ m ′ ΓM | φ ⊢ φ ′      ⊢m {ψ} P {φ}
                                    ⊢m′ {ψ ′ } P {φ′ }

                ∀0 ≤ z < N. ⊢m {ψz+1 } P {ψz } ΓM | ψN ⊢ en = ⌈N ⌉
                           ⊢mN {ψN } loop en do P {ψ0 }

     ⊢m {ψ ∧ eb = tt} P1 {φ} ⊢m {ψ ∧ eb = ff} P2 {φ} ΓM | ψ ⊢ eb = tt ∨ eb = ff
                           ⊢m {ψ} if eb then P1 else P2 {φ}

                       Table 1. Graded Hoare Logic Inference Rules


is standard, but graded with 1 since we do not treat it specially in GHL. Sequen-
tial composition takes the monoid multiplication of the grades of the subterms.
The rules for commands and procedures use the functions Cc and Cp introduced
above. Notice that the rule for commands uses as the pre-condition as its post-
condition, since commands have only side effects and they do not return any
value. The rule for procedures combines the pre- and post-conditions given by
Cp following the style of Floyd’s assignment rule [12].
    The non-syntax-directed consequence rule is similar to the usual consequence
rule, and in addition allows the assumption on the grade to be weakened (ap-
proximated ) according to the ordering of the monoid.
    The shape of the loop rule is slightly different from the usual one. It uses the
assertion-logic judgment ΓM | ψN ⊢ en = ⌈N ⌉ to express the assumption that en
evaluates to ⌈N ⌉. Under this assumption it uses a family of assertions ψz indexed
by the natural numbers z ∈ {0, 1, . . . , N − 1} to conclude the post-condition ψ0 .
This family of assertions plays the role of the classical invariant in the Floyd-
Hoare logic rule for ‘while’. Assuming that the grade of the loop body is m, the
grade of the loop command is then mN , where m0 = 1 and mk+1 = m · mk . By
instantiating this rule with ψz = (θ ∧ en = ⌈z⌉), the loop rule also supports the
following derived rule which is often preferable in examples:

               ∀0 ≤ z < N. ⊢m {θ ∧ en = ⌈z + 1⌉} P {θ ∧ en = ⌈z⌉}
                 ⊢mN {θ ∧ en = ⌈N ⌉} loop en do P {θ ∧ en = ⌈0⌉}

The rule for the conditional is standard except for the condition ΓM | ψ ⊢ eb =
tt ∨ eb = ff. While this condition may seem obvious, it is actually important to
make GHL sound in various semantics (mentioned in Section 2). As an exam-
ple, suppose that a semantics [[−]] of expressions is given in the product category
Set2 , which corresponds to two semantics [[−]]1 , [[−]]2 of expressions in Set. Then
                               Graded Hoare Logic and its Categorical Semantics                   11

the side condition for the conditional is to guarantee that for any boolean ex-
pression eb , and pair of memories (ρ1 , ρ2 ) satisfying the precondition ψ, the pair
([[eb ]]1 (ρ1 ), [[eb ]]2 (ρ2 )) is either [[tt]] = (tt, tt) or [[ff]] = (ff, ff). We note that other
relational logics such as apRHL [6] employ an equivalent syntactic side condition
in their rule for conditionals.

3.5    Example Instantiations of GHL
Example 2 (Simple cost analysis). We can use the tick command discussed in
Example 1 to instrument programs with cost annotations. We can then use
GHL to perform cost analysis by instantiating GHL with the additive natural
number monoid (N, ≤, 0, +) and tick ∈ Cc (φ, 1). Thus, we can form judgments
⊢1 {φ} do tick {φ} which account for cost via the judgment’s grade. Sequential
composition accumulates cost and terms like skip and assignment have 0 cost.
    Let us use this example to illustrate how Cc can assign multiple pre-condition-
grade pairs to a command. Suppose that we modify the semantics of tick so
that it reports unit cost 1 when variable x is 0, otherwise cost 2. We can then
define Cc so that tick ∈ Cc (x = ⌈0⌉, 1) and also tick ∈ Cc (x 6= ⌈0⌉, 2). In this
way, we can give different grades to programs depending on their pre-conditions.

Example 3 (Program Counter Security). We can use the commands cfTT and
cfFF discussed in Example 1 to instrument programs with control flow anno-
tations, recording to an external log. GHL can then be used to reason about
program counter security [35][3, Section 7.2] of instrumented programs. This is
a relational security property similar to non-interference (requiring that private
values do not influence public outputs) but where only programs with the same
control flow are considered.
      Firstly, any conditional statement if eb then Pt else Pf in a program is elab-
orated to a statement if eb then (cfTT; Pt ) else (cfFF; Pf ). We then instantiate
GHL with a monoid of words over {tt, ff} with prefix order: 2∗ , ({tt, ff}∗ , ≤
, ǫ, ·) and we consider cfTT ∈ Cc (φ, tt) and cfTT ∈ Cc (φ, ff). We can thus form
judgments of the shape ⊢tt {φ} do cfTT {φ} and ⊢ff {φ} do cfFF {φ} which
account for control-flow information (forming paths) via the judgment’s grade.
Sequential composition concatenates control-flow paths and terms like skip and
assignment do not provide any control-flow information, i.e. ǫ.
      We then instantiate the assertion logic to support relational reasoning, i.e.,
where the expressions of the language are interpreted as pair of values. For an
expression e, interpreted as a pair (v1 , v2 ) then we write eh1i = v1 to say that
the first component (left execution) equals v1 and eh2i = v2 to say that the
second component (right execution) equals v2 . In the assertion logic, we can
then describe public values which need to be equal, following the tradition in
reasoning about non-interference, by the predicate eh1i = eh2i. Private data
are instead interpreted as a pair of arbitrary values. (Section 3.3 suggested the
notation eqvhii (e, b) for ehii = b, but we use the latter for compactness here).
      As an example, one can prove the following judgment where x is a public
variable and y is a private one, and b ∈ {tt, ff}:
12        Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

⊢b {xh1i=xh2i∧xh1i=b}if x then (cfTT; x=1; y=1) else (cfFF; x=2; y=2){xh1i=xh2i}
 This judgment shows the program is non-interferent, since the value of x is
independent from the value of the private variable y, and secure in the pro-
gram counter model, since the control flow does not depend on the value of y.
Conversely, the following judgment is not derivable for both b = tt and b = ff:
⊢b {xh1i=xh2i∧yh1i=b}if y then (cfTT; x=1; y=1) else (cfFF; x=1; y=2){xh1i=xh2i}

 This program is non-interferent but is not secure in the program counter model
because the control flow leaks information about y which is a private variable.
Example 4 (Union Bound Logic). Section 1 discussed the Union Bound logic by
Barthe et al. [5]. This logic embeds smoothly into GHL by using the pomonoid
(R≥0 , ≤, 0, +) and procedures of the form sampleµ,e as samplings from a prob-
abilistic distribution µ parametrised over the syntax of GHL expressions e. Fol-
lowing Barthe et al. [5], we consider a semantically defined set for Cp :
    Cp (φ, β, ψ) = {sampleµ,e | ∀s.s ∈ [[φ]] =⇒ Prs′ ←Jsampleµ,e K(s) [s′ ∈ [[¬ψ]]] ≤ β)}
This definition captures that, assuming the pre-condition holds for an input
memory state s, then for output value s′ from sampling sampleµ,e , the proba-
bility that the post-condition is false is bounded above by β. This allow us to
consider different properties of the distribution µ with parameter e.


4      Graded Categories
Now that we have introduced GHL and key examples, we turn to the core of its
categorical semantics: graded categories.
    Graded monads provide a notion of sequential composition for morphisms of
the form I → Tm J, i.e., with structure on the target/output capturing some in-
formation by the grade m drawn from a pomonoid [24]; dually, graded comonads
provide composition for Dm I → J, i.e. with structure on the source/input with
grade m [43]. We avoid the choice of whether to associate grading with the input
or output by instead introducing graded categories, which are agnostic about the
polarity (or position) of any structure and grading. Throughout this section, we
fix a pomonoid (M, ≤, 1, ·) (with · monotonic wrt. ≤).
Definition 1. An M -graded category C consists of the following data:
 – A class Obj(C) of objects. I ∈ C denotes I ∈ Obj(C).
 – A homset C(I, J)(m) for all objects I, J ∈ C and m ∈ M . We often write
   f : I →m J to mean f ∈ C(I, J)(m), and call m the grade of f ;
 – An upcast functions ↑nm : C(I, J)(m) → C(I, J)(n) for all grades m ≤ n;
 – Identity morphisms idI ∈ C(I, I)(1) for all I ∈ C;
 – Composition ◦ : C(J, K)(n) × C(I, J)(m) → C(I, K)(m · n).
Graded categories satisfy the usual categorical laws of identity and associativity,
                                                           ′     ′
                                                                       m′ ·n′
and also the commutativity of upcast and composition: ↑nn g◦↑m m f = ↑m·n (g◦f ),
corresponding to monotonicity of (·) with respect to ≤.
                             Graded Hoare Logic and its Categorical Semantics                 13

    An intuitive meaning of a graded category’s morphisms is: f ∈ C(A, B)(m) if
the value or the price of a morphism f : A → B is at most m with respect to the
ordering ≤ on M . We do not yet give a polarity or direction to this price, i.e.,
whether the price is consumed or produced by the computation. Thus, graded
categories give a non-biased view; we need not specify whether grading relates
to the source or target of a morphism.
    Graded categories were first introduced by Wood [54, Section 1] (under the
name ‘large V -categories’), and Levy connected them with models of call-by-
push-value [28]. Therefore we do not claim the novelty of Definition 1.

Example 5. A major source of graded categories is via graded (co)monads. Let
(M, ≤, 1, ·) be a pomonoid, regarded as a monoidal category. A graded monad
[50,24] on a category C (or more precisely an M -graded monad ) is a lax monoidal
functor (T, η, µ) : (M, ≤, 1, ·) → ([C, C], Id, ◦). Concretely, this specifies:

 – a functor T : (M, ≤) → [C, C] from the preordered set (M, ≤) to the
   endofunctor category over C. For an ordered pair m ≤ m′ in M then
   T (m ≤ m′ ) : T m → T m′ is a natural transformation;
 – a unit η : Id → T 1 and a multiplication µm,m′ : T m ◦ T m′ → T (m · m′ ),
   natural in m, m′ ∈ M .

They satisfy the graded versions of the usual monad axioms:

           T mηJ                                           µm,m′ ,T m′′ J
   T mJ❖❖      / T m(T 1J)           T m(T m′ (T m′′ J))                / T (m · m′ )(T m′′ J)
         ❖❖❖❖
ηT mJ        ❖❖❖❖        µm,1,J   T mµm′ ,m′′ ,J                                    µmm′ ,m′′ ,J
          µ1,m,J                                      µm,m′ m′′ ,J           
T 1(T mJ)          / T mJ            T m(T (m′ · m′′ )J)              / T (m · m′ · m′′ )J

Graded comonads are dually defined (i.e., as a graded monad on Cop ).
   By mimicking the construction of Kleisli categories, we can construct an
M -graded category CT (we call it the Kleisli M -graded category of T ) from a
category C with an M -graded monad T on C.6

 – Obj(CT ) , Obj(C) and CT (X, Y )(m) , C(X, T mY ).
 – For f : X →m Y and n such that m ≤ n, we define ↑nm f , T (m ≤ n)Y ◦ f .
 – Identity and composition are defined by: idX , ηX : X →1 X and g ◦ f ,
   µm,n,Z ◦ T m g ◦ f for f : X →m Y and g : Y →n Z.

The dual construction is possible. Let D be an M op -graded comonad on a cate-
gory C. We then define CD by CD (X, Y )(m) = C(DmX, Y ); the rest of data is
similar to the case of graded monads. This yields an M -graded category CD .

Remark 1. As an aside (included for completeness but not needed in the rest
of the paper), graded categories are an instance of enriched categories. For the
enriching category, we take the presheaf category [M, Set], together with Day’s
convolution product [10].
6
    Not to be confused with the Kleisli category of graded monads by Fujii et al. [13].
14      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

4.1   Homogeneous Coproducts in Graded Categories
We model boolean values and`natural numbers by the binary coproduct 1 + 1
and the countable coproduct i∈N 1. We thus define what it means for a graded
category to have coproducts. The following definition of binary coproducts easily
extends to coproducts of families of objects.
Definition 2. Let C be an M -graded category. A homogeneous binary coprod-
uct of X1 , X2 ∈ C consists of an object Z ∈ C together with injections ι1 ∈
C(X1 , Z)(1) and ι2 ∈ C(X2 , Z)(1) such that, for any m ∈ M and Y ∈ C, the
function λf . (f ◦ ι1 , f ◦ ι2 ) of type C(Z, Y )(m) → C(X1 , Y )(m)× C(X2 , Y )(m) is
invertible. The inverse is called the cotupling and denoted by [−, −]. It satisfies
the usual law of coproducts (i = 1, 2):

        [f1 , f2 ] ◦ ιi = fi ,                            [ι1 , ι2 ] = idZ ,
         g ◦ [f1 , f2 ] = [g ◦ f1 , g ◦ f2 ],    [↑nm f1 , ↑nm f2 ] = ↑nm [f1 , f2 ].

When homogeneous binary coproducts of any combination of X1 , X2 ∈ C exists,
we say that C has homogeneous binary coproducts.
    The difference between homogeneous coproducts and coproducts in ordinary
category theory is that the cotupling is restricted to take morphisms with the
same grade. A similar constraint is seen in some effect systems, where the typing
rule of conditional expressions require each branch to have the same effect.
Proposition 1. Let {ιi ∈ C(Xi , Z)}i∈I be a coproduct of {Xi }i∈I in an ordinary
category C.
1. Suppose that T is an M -graded monad on C. Then {ηZ ◦ιi ∈ CT (Xi , Z)(1)}i∈I
   is a homogeneous coproduct in CT .
2. Suppose that (D, ε, δ) is an M op -graded comonad on C such that each Dm :
   C → C preserves the coproduct {ιi }i∈I . Then {ιi ◦ εI ∈ CD (Xi , Z)(1)}i∈I is
   a homogeneous coproduct in CD .

4.2   Graded Freyd Categories with Countable Coproducts
We now introduce the central categorical structure of the loop language and GHL
semantics: graded Freyd categories with homogeneous countable coproducts.
Definition 3. An M -graded Freyd category with homogeneous countable co-
products consists of the following data:
 1. A cartesian monoidal category (V, 1, ×, l, r, a) with countable coproducts
    such that for all V ∈ V, the functor V × (−) : V → V preserves coproducts.
 2. An M -graded category C such that Obj(C) = Obj(V) and C has homoge-
    neous countable coproducts.
 3. A function IV,W : V(V, W ) → C(V, W )(1) for each V, W ∈ C. Below we
    may omit writing subscripts of I. The role of this function is to inject pure
    computations into effectful computations.
                             Graded Hoare Logic and its Categorical Semantics          15

 4. A function (∗)V,X,W,Y : V(V, W ) × C(X, Y )(m) → C(V × X, W × Y )(m) for
    each V, W, X, Y ∈ C and m ∈ M . Below we use it as an infix operator and
    sometimes omit its subscripts. The role of this function is to combine pure
    computations and effectful computations in parallel.
The function I and (∗) satisfy the following equations:
    I(idX ) = idX I(g ◦ f ) = Ig ◦ If I(f × g) = f ∗ Ig idV ∗ idX = idV ∗X ,
               (g ◦ f ) ∗ (i ◦ j) = (g ∗ i) ◦ (f ∗ j) f ∗ ↑nm g = ↑nm (f ∗ g)
f ◦ I(lX ) = I(lX ) ◦ (id1 ∗ f ) I(aX ′,Y ′,Z ′) ◦ ((f ×g) ∗ h) = (f ∗ (g∗h)) ◦ I(aX,Y,Z )
These are analogous to the usual Freyd categories axioms. We also require that:
 1. For any countable coproduct {ιi ∈ V(Xi , Y )}i∈A , {I(ιi ) ∈ C(Xi , Y )(1)}i∈A
    is a homogeneous countable coproduct.
 2. For any homogeneous countable coproduct {ιi ∈ C(Xi , Y )(1)}i∈A and V ∈
    V, {idV ∗ιi ∈ C(V ×Xi , V ×Y )(1)}i∈A is a homogeneous countable coproduct.
We denote an M -graded Freyd category with countable coproducts by the tuple
(V, 1, ×, C, I, (∗)) capturing the main details of the cartesian monoidal structure
of V, the base category C, the lifting function I and the action (∗).
If the grading pomonoid M is trivial, C becomes an ordinary category with
countable coproducts. We therefore simply call it a Freyd category with count-
able coproducts. This is the same as a distributive Freyd category in the sense
introduced by Power [46] and Staton [51]. We will use non-graded Freyd cat-
egories to give a semantics of the loop language in Section 4.3. An advantage
of Freyd categories is that they encompasses a broad class of models of com-
putations, not limited to those arising from monads. A recent such example is
Staton’s category of s-finite kernels [52]7 .
    We could give an alternative abstract definition of M -graded Freyd category
using 2-categorical language: a graded Freyd category is an equivariant morphism
in the category of actions from a cartesian category to M -graded categories. The
full detail of this formulation will be discussed elsewhere.
    A Freyd category typically arises from a strong monad on a cartesian category
[47]. We give here a graded analogue of this fact. First, we recall the notion
of strength for graded monads [24, Definition 2.5]. Let (C, 1, ×) be a cartesian
monoidal category. A strong M -graded monad is a pair of an M -graded monad
(T, η, µ) and a natural transformation stI,J,m ∈ C(I ×T mJ, T m(I ×J)) satisfying
graded versions of the four coherence laws in [34, Definition 3.2]. We dually
define a costrong M -graded comonad (D, ε, δ, cs) to be the M -graded comonad
equipped with the costrength csI,J,m ∈ C(Dm(I × J), I × DmJ).
Proposition 2. Let (C, 1, ×) be a cartesian monoidal category.
1. Let (T, η, µ, st) be a strong M -graded monad on C. The Kleisli M -graded
   category CT , together with If = ηW ◦ f and f ∗ g = stW,Y ◦ (f × g) forms
   an M -graded Freyd category with homogeneous countable coproducts.
7
    It is not known whether the category of s-finite kernels is a Kleisli category.
16       Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

2. Let (D, ε, δ, cs) be a costrong M op -graded comonad on C such that each Dm
   preserves countable coproducts. Then the coKleisli M -graded category CD
   together with If = f ◦ εV and f ∗ g = (f × g) ◦ csV,X forms an M -graded
   Freyd category with homogeneous countable coproducts.
We often use the following ‘ext’ operation to structure interpretations of pro-
grams and GHL derivations. Let δX ∈ V(X, X × X) be the diagonal morphism.
Then ext : C(X, Y )(m) → C(X, X × Y )(m) is defined as ext(f ) = (X ∗ f ) ◦ IδX .
When viewing X as a set of environments, ext(f ) may be seen as executing an ef-
fectful procedure f under an environment, then extending the environment with
the return value of f . In a non-graded setting, the definition of ext is analogous.

4.3     Semantics of The Loop Language in Freyd Categories
Towards the semantics of GHL, we first give a more standard, non-graded cate-
gorical semantics of the loop language. We first prepare the following data.
 ⋆ A Freyd category (V, 1, ×, C, I, ∗) with countable coproducts.
 ⋆ A coproduct {tt, ff ∈ V(1, Bool)} of 1 and 1 in V.
 ⋆ A coproduct {⌊k⌋ ∈ V(1, Nat)}k∈N of N-many 1s in V.
 ⋆ An interpretation [[−]] of Σ in V such that

          [[bool]] = Bool     [[tt]] = tt ∈ V(1, Bool)   [[ff]] = ff ∈ V(1, Bool)
            [[nat]] = Nat   [[⌈k⌉]] = ⌊k⌋ ∈ V(1, Nat).

For convenience, we let M , [[ΓM ]] (Section 3.1), i.e., all relevant (mutable) pro-
gram variables are in scope, and write πv ∈ V(M, [[ΓM (v)]]) for the projection
morphism associated to a program variable v ∈ ΓM .
   Pure expressions are interpreted as V-morphisms and impure commands and
procedures are interpreted as C-morphisms, of the form:
 ⋆ (expressions) A morphism [[e]] ∈ V(M, [[s]]) for all e ∈ ExpΣ (ΓM , s); see
   Section 3.1.
 ⋆ (commands) A morphism [[c]] ∈ C(M, 1) for each c ∈ CExp.
 ⋆ (procedures) A morphism [[p]] ∈ C(M, [[s]]) for each s ∈ S and p ∈ PExps .
For the interpretation of programs, we first define some auxiliary morphisms. For
all v ∈ ΓM , let updv ∈ V(M × [[ΓM (v)]], M) to be the unique morphism (capturing
memory updates) satisfying πv ◦updv = π2 and πw ◦updv = πw ◦π1 for any w ∈ ΓM
such that v 6= w. We define sub(v, e) ∈ V(M, M) by sub(v, e) , updv ◦ hidM , [[e]]i,
which updates the memory configuration at variable v with the value of e.
    For the interpretation of conditional and loop commands, we need coproducts
over M. Since V is distributive, we can form a binary coproduct M × Bool and a
countable coproduct M × Nat with injections respectively defined as (∀k ∈ N):

     tm , hidM , tt◦!M i ∈ V(M, M × Bool)   [k] , hidM , ⌊k⌋◦!M i ∈ V(M, M × Nat)
     fm , hidM , ff◦!M i ∈ V(M, M × Bool)
                                  Graded Hoare Logic and its Categorical Semantics                       17

By Condition 1 of Definition 3, these coproducts are mapped to coproducts in
C with injections:
      {I(tm), I(fm) ∈ C(M, M × Bool)},                  {I([k]) ∈ C(M, M × Nat) | k ∈ N}.

The cotuplings of these coproducts (written [f, g] and [f (k) ]k∈N respectively) are
used next to interpret conditionals and loops.
We interpret a program P of the loop language as a morphism [[P ]] ∈ C(M, M):
                         [[P ; P ′ ]] = [[P ′ ]] ◦ [[P ]]               [[skip]] = idM
                    [[do v ← p]] = I(updv ) ◦ ext[[p]]                    [[do c]] = I(π1 ) ◦ ext[[c]]
                        [[v := e]] = I(sub(v, e))
      [[if eb then P else P ′ ]] = [ [[P ]], [[P ′ ]] ] ◦ ext(I[[eb ]])
               [[loop en do P ]] = [ [[P ]](k) ]k∈N ◦ ext(I[[en ]])
Thus, the semantics of loop en doP is such that, if the expression en evaluates to
some natural number ⌈k⌉ then loop en doP is equivalent to the k-times sequential
composition of P .

5      Modelling Graded Hoare Logic
We now define the categorical model of GHL, building on the non-graded Freyd
semantics of Section 4.3. Section 5.1 first models the base assertion logic, for
which we use fibrations, giving an overview of the necessary mathematical ma-
chinery for completeness. Section 5.2 then defines the semantics of GHL and
Section 5.3 instantiates it for the examples discussed previously in Section 3.

5.1      Interpretation of the Assertion Logic using Fibrations
Our assertion logic (Section 3) has logical connectives of finite conjunctions,
countable disjunctions, existential quantification and an equality predicate. A
suitable categorical model for this fragment of first-order logic is offered by a
coherent fibration [22, Def. 4.2.1], extended with countable joins in each fibre.
We recap various key definitions and terminology due to Jacobs’ textbook [22].
    In the following, let P and V be categories and p : P → V a functor.
    We can regard functor p as attaching predicates to each object in V. When
pψ = X, we regard ψ ∈ P as a predicate over X ∈ V. When f ∈ P(ψ, φ) is a
morphism, we regard this as saying that pf maps elements satisfying ψ to those
satisfying φ in V. Parallel to this view of functors assigning predicates is the
notion that entities in P are ‘above’ those in V when they are mapped to by p.
Definition 4 (‘Aboveness’). An object ψ ∈ P is said to be above an object
X ∈ V if pψ = X. Similarly, a morphism8 f˙ ∈ P(ψ, φ) is said to be above a
morphism f in V if pf˙ = f ∈ V(pψ, pφ). A morphism in P is vertical if it is
above an identity morphism. Given ψ, φ ∈ P and f ∈ V(pψ, pφ), then we denote
the set of all morphisms in P above f as Pf (ψ, φ) = {f˙ ∈ P(ψ, φ) | pf˙ = f }.
8
    The dot notation here introduces a new name and should not be understood as
    applying some mathematical operator on f .
18      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

Definition 5 (Fibre category). A fibre category over X ∈ V is a subcategory
of P consisting of objects above X and morphisms above idX . This subcategory
is denoted by PX , and thus the homsets of PX are PX (ψ, φ) = PidX (ψ, φ).

We are ready to recall the central concept in fibrations: cartesian morphisms.

Definition 6 (Cartesian morphism). A morphism f˙ ∈ P(ψ, φ) is cartesian
if for any α ∈ P and g ∈ V(pα, pψ), the post-composition of f˙ in P, regarded as
a function of type f˙ ◦ − : Pg (α, ψ) → Pg◦pf˙ (α, φ), is a bijection. This amounts
to the following universal property of cartesian morphism: for any ḣ ∈ P(α, φ)
above g ◦ pf , there exists a unique morphism ġ ∈ P(α, ψ) above g such that
ḣ = f˙ ◦ ġ. Intuitively, f˙ represents the situation where ψ is a pullback or inverse
image of φ along pf˙, and the universal property corresponds to that of pullback.

Definition 7 (Fibration). Finally, a functor p : P → V is a fibration if for any
ψ ∈ P, X ∈ V, and f ∈ V(X, pψ), there exists an object φ ∈ P and a cartesian
morphism f˙ ∈ P(φ, ψ) above f , called the cartesian lifting of f with ψ. We say
that a fibration p : P → V is posetal if each PX is a poset, corresponding to the
implicational order between predicates. When ψ ≤ φ holds in PX , we denote the
corresponding vertical morphism in P as ψ ր φ.
    Posetal fibrations are always faithful. The cartesian lifting of f ∈ V(X, pψ)
with ψ uniquely exists. We thus write it by f ψ, and its domain by f ∗ ψ. It
can be easily shown that for any morphism f ∈ V(X, Y ) in V, the assignment
ψ ∈ PY 7→ f ∗ ψ ∈ PX extends to a monotone function f ∗ : PY → PX . We call it
the reindexing function (along f ). Furthermore, the assignment f 7→ f ∗ satisfies
the (contravariant) functoriality: id∗X = idPX and (g ◦f )∗ = f ∗ ◦g ∗ . A fibration is
a bifibration if each reindexing function f ∗ : PY → PX for f ∈ V(X, Y ) has a left
adjoint, denoted by f∗ : PX → PY . f∗ ψ is always associated with a morphism
f ψ : f∗ ψ → ψ above f , and this is called the opcartesian lifting of f with ψ. For
the universal property of the opcartesian lifting, see Jacobs [22, Def. 9.1.1].

Fibrations for our Assertion Logic It is widely known that coherent fibrations
are suitable for interpreting the ∧, ∨, ∃, =-fragment of first-order logic (see [22,
Chapter 4, Def. 4.2.1]). Based on this fact, we introduce a class of fibrations that
are suitable for our assertion logic—due to the countable joins of the assertion
logic we modify the definition of coherent fibration accordingly.

Definition 8. A fibration for assertion logic over V is a posetal fibration p :
P → V for cartesian V with distributive countable coproducts, such that:

 1. Each fibre poset PX is a distributive lattice with finite meets ⊤X , ∧ and
    countable joins ⊥X , ∨.
 2. Each reindexing function f ∗ preserves finite meets and countable joins.
 3. The reindexing function c∗X,Y along the contraction cX,Y , hπ1 , π2 , π2 i ∈
    V(X × Y, X × Y × Y ) has a left adjoint EqX,Y ⊣ c∗X,Y . This satisfies Beck-
    Chevalley condition and Frobenius property; we refer to [22, Definition 3.4.1].
                                    Graded Hoare Logic and its Categorical Semantics                          19

                              ∗
 4. The reindexing function wX,Y   along the weakening wX,Y ,π1 ∈ V(X ×Y, X)
                                ∗
    has a left adjoint ∃X,Y ⊣ wX,Y  . This satisfies Beck-Chevalley condition and
    Frobenius property; we refer [22, Definition 1.9.1, 1.9.12].
This is almost the same as the definition of coherent fibrations [22, Definition
4.2.1]; the difference is that 1) the base category V has countable coproducts 2)
we require each fibre to be a poset; this makes object equalities hold on-the-nose,
and 3) we require each fibre to have countable joins. They will be combined with
countable coproducts of V to equip P with a countable coproduct [22].
Example 6. A typical example of a fibration for assertion logic is the subobject
fibration pSet : Pred → Set; the category Pred has objects pairs (X, ψ) of
sets such that ψ ⊆ X, and morphisms of type (X, ψ) → (Y, φ) as functions
f : X → Y such that f (ψ) ⊆ φ. The functor p sends (X, ψ) to X and f to itself.
More examples can be found in the work of Jacobs [22, Section 4].
    For a parallel pair of morphisms f, g ∈ V(X, Y ), we define the equality pred-
icate Eq(f, g) above X to be hidX , f, gi∗ EqX,Y (⊤X×Y ) [22, Notation 3.4.2]. In-
tuitively, Eq(f, g) corresponds to the predicate {x ∈ X | f (x) = g(x)}. In this
paper, we will use some facts about the equality predicate shown by Jacobs [22,
Proposition 3.4.6, Lemma 3.4.5, Notation 3.4.2, Example 4.3.7].

The Semantics of Assertion Logic We move to the semantics of our assertion
logic in a fibration p : P → V for assertion logic. The basic idea is to interpret
a formula ψ ∈ FmlΣl (Γ ) as an object in P[[Γ ]], and an entailment Γ | ψ ⊢ φ as
the order relation [[ψ]] ≤ [[φ]] in P[[Γ ]]. The semantics is given by the following
interpretation of the data specifying the assertion logic (given in Section 3.3):
 ⋆ A fibration p : P → V for assertion logic.
 ⋆ An interpretation [[−]] of Σl in P that coincides with the one [[−]] of Σ in V.
 ⋆ An object [[P ]] ∈ P[[par(P )]] for each atomic proposition P ∈ Pl (recall par
   assigns input sorts to atomic propositions in Pl , parameterising the logic).
 ⋆ We require that for any Γ ∈ CtxΣl and (ψ, φ) ∈ Axiom(Γ ), [[ψ]] ≤ [[φ]]
   holds in P[[Γ ]] . This expresses an implicational axiom in the coherent logic.
The interpretation [[ψ]] of ψ ∈ FmlΣl (Γ ) is inductively defined as a P[[Γ ]]-object:

        [[P (t1 , · · · , tn )]] = h[[t1 ]], · · · , [[tn ]]i∗ [[P ]]      [[t = u]] = Eq([[t]], [[u]])
          V            V                W               W
        [[ ψi ]] = [[ψi ]]            [[ ψi ]] = [[ψi ]]                [[∃x : s . ψ]] = ∃[[Γ ]],[[s]][[ψ]]

5.2   Interpretation of Graded Hoare Logic
We finally introduce the semantics of Graded Hoare logic. This semantics inter-
prets derivations of GHL judgements ⊢m {ψ} P {φ} as m-graded morphisms in
a graded category. Moreover, it is built above the interpretation [[P ]] ∈ C(M, M)
of the program P in the non-graded semantics introduced in Section 4.3. The
underlying structure is given as a combination of a fibration for the assertion
logic and a graded category over C, as depicted in (1) (Section 2, p. 5).
20        Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

Definition 9. A GHL structure over a Freyd category (V, 1, ×, C, I, ∗) with
countable coproducts and a fibration p : P → V for assertion logic comprises:
                                             ˙ ⊛) with homogeneous countable
                                        ˙ E, I,
 1. An M -graded Freyd category (P, 1̇, ×,
    coproducts.
 2. A function qψ,φ,m : E(ψ, φ)(m) → C(pψ, pφ) (subscripts may be omitted),
    which maps to the base denotational model, erasing assertions and grades.
The above data satisfy the following properties:
 1. That q behaves ‘functorialy’ preserving structure from E to V:

               q(idφ ) = idpφ , q(g ◦ f ) = qg ◦ qf, qψ,φ,n (↑nm f ) = qψ,φ,m f
                  ˙ ) = I(pf ), q(f ⊛ g) = pf ∗ qg
               q(If
 2. For any homogeneous countable coproduct {ιi ∈ E(ψi , φ)(1)}i∈Λ , {qιi ∈
    C(pψi , pφ)}i∈Λ is a countable coproduct.
 3. (Ex falso quodlibet) q⊥X ,φ,m : E(⊥X , φ)(m) → C(X, pφ) is a bijection.
The last statement asserts that if the precondition is the least element ⊥X in
the fibre over X ∈ V, which represents the false assertion, we trivially conclude
any postcondition φ and grading m for any morphisms of type X → pφ in C.
    The semantics of GHL then requires a graded Freyd category with countable
coproducts, and morphisms in the graded category guaranteeing a sound model
of the effectful primitives (commands/procedures), captured by the data:
⋆ A GHL structure (P, 1̇, ×,      ˙ ⊛, q) over the Freyd category (V, 1, ×, C, I, ∗)
                             ˙ E, I,
  with countable coproducts and the fibration p : P → V for assertion logic.
⋆ For each c ∈ Cc (ψ, m) a morphism hci ∈ E([[ψ]], 1̇)(m) such that qhci = [[c]].
⋆ For each p ∈ Cps (ψ, m, φ) a morphism hpi ∈ E([[ψ]], [[φ]])(m) such that qhpi = [[p]].
where [[c]], [[p]] and later [[e]] are from the underlying non-graded model (Sec. 4.3).
   We interpret a derivation of GHL judgement ⊢m {φ} P {ψ} as a morphism

[[⊢m {φ} P {ψ}]] ∈ E([[φ]], [[ψ]])(m) such that q[[φ]],[[ψ]],m[[⊢m {φ} P {ψ}]] = [[P ]].

The constraint on the right is guaranteed by the soundness of the interpretation
(Theorem 1). From the functor-as-refinement viewpoint [32], the interpretation
[[⊢m {φ} P {ψ}]] witnesses that [[P ]] respects refinements φ and ψ of M, and
additionally it witnesses the grade of [[P ]] being m. We first cover the simpler
cases of the interpretation of GHL derivations:

                     [[⊢1 {ψ} skip {ψ}]] = id[[ψ]]
              [[⊢m1 ·m2 {ψ} P1 ; P2 {θ}]] = [[⊢m2 {ψ1 } P2 {θ}]] ◦ [[⊢m1 {ψ} P1 {ψ1 }]]
                                             ˙
               [[⊢1 {ψ[e/v]} v := e {ψ}]] = I(sub(v, e)[[ψ]])
                                       ˙ 1 ) ◦ exthci
                 [[⊢m {ψ} do c {ψ}]] = I(π
                                       ˙
  [[⊢m {ψ} do v ← p {(∃v . ψ) ∧ φ}]] = I(upd          ˙
                                             v ([[ψ]] × [[φ]])) ◦ exthpi
                                                   ′
                              ˙
     [[⊢m′ {ψ ′ } P {φ′ }]] = I([[φ]] ր [[φ′ ]]) ◦ ↑m                    ˙ ′
                                                    m [[⊢m {ψ} P {φ}]] ◦ I([[ψ ]] ր [[ψ]])
                             Graded Hoare Logic and its Categorical Semantics               21

The morphisms with upper and lower lines are cartesian liftings and op-cartesian
liftings in the fibration p : P → V of the assertion logic. The codomain of the
interpretation of the procedure call do v ← p is equal to [[(∃v . ψ) ∧ φ]].
     The above interpretations largely follow the form of the underlying model
of Section 4.3, with the additional information and underlying categorical ma-
chinery for grades and assertions here; we now map to E. The interpretation of
conditional and loop commands requires some more reasoning.

Conditionals Let p1 , p2 be the interpretations of each branch of the conditional
command:

            p1 = [[⊢m {ψ ∧ eb = tt} P1 {φ}]] ∈ E([[ψ ∧ eb = tt]], [[φ]])(m)
            p2 = [[⊢m {ψ ∧ eb = ff} P2 {φ}]] ∈ E([[ψ ∧ eb = ff]], [[φ]])(m)

We consider the cocartesian lifting hidM , [[eb ]]i[[ψ]] : [[ψ]] → hidM , [[eb ]]i∗ [[ψ]]. We
name its codomain Im. Next, cartesian morphisms tm(Im) : tm∗ Im → Im and
fm(Im) : fm∗ Im → Im in P are above the coproduct (M × Bool, tm, fm) in V. Then
the interpretations of the preconditions of P1 , P2 are inverse images of Im along
tm, fm : M → M × Bool:
Lemma 1. [[ψ ∧ eb = tt]] = tm∗ Im and [[ψ ∧ eb = ff]] = fm∗ Im.
The side condition of the conditional rule ensures that (Im, tm(Im), fm(Im)) is a
coproduct in P:
Lemma 2. ΓM | ψ ⊢ eb = tt ∨ eb = ff implies Im = tm∗ tm∗ Im ∨ fm∗ fm∗ Im.
Therefore the image of the coproduct (Im, tm(Im), fm(Im)) by I˙ yields a homo-
geneous coproduct in E. We take the cotupling [p1 , p2 ] ∈ E(Im, [[φ]])(m) with
respect to this homogeneous coproduct. We finally define the interpretation of
the conditional rule to be the following composite:
                                                 ˙
[[⊢m {ψ}if eb then P1 else P2 {φ}]] = [p1 , p2 ]◦I(hid M , [[eb ]]i[[ψ]]) ∈ E([[ψ]], [[φ]])(m).


Loops Fix N ∈ N, and suppose that ⊢m {ψi+1 } P {ψi } is derivable in the graded
Hoare logic for each 0 ≤ i < N . Let pi ∈ E([[ψi+1 ]], [[ψi ]])(m) be the interpretation
[[⊢m {ψi+1 } Pi {ψi }]]. We then define a countable family of morphisms (we use
here ex falso quodlibet):
                 −1
                  q⊥M ,[[ψ0 ]],mN ([[P ]](i) ) ∈ E(⊥M , [[ψ0 ]])(mN ) (i 6= N )
           bi =
                  p0 ◦ · · · ◦ pN              ∈ E([[ψN ]], [[ψ0 ]])(mN ) (i = N )

Let θi , cod(bi ). Then i∈N θi = i∈N [i]∗ θi = [N ]∗ [[ψN ]] because [i]∗ θi is either
                          `         W

⊥M×Nat or [N ]∗ [[ψN ]]. We then send the coproduct θi → i∈N θi by I˙ and obtain
                                                          `
a homogeneous coproduct in E. By taking the cotupling of all bi with this ho-
mogeneous coproduct, we obtain a morphism [bi ]i∈N ∈ E([N ]∗ [[ψN ]], [[ψ0 ]])(mN ).


Lemma 3. ΓM | ψN ⊢ en = ⌈N ⌉ implies hidM , [[eN ]]i∗ [[ψN ]] = [N ]∗ [[ψN ]].
22      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

                                                             ˙
We then define [[⊢mN {ψN } loop en do P {ψ0 }]] = [bi ]i∈N ◦ I(hid M , [[en ]]i[[ψN ]]).

Theorem 1 (Soundness of GHL). For any derivation of a GHL judgement
⊢m {φ} P {ψ}, we have q[[φ]],[[ψ]],m[[⊢m {φ} P {ψ}]] = [[P ]].

5.3   Instances of Graded Hoare Logic
We first present a construction of GHL structures from graded monad liftings,
which are a graded version of the concept of monad lifting [11,19,26].
Definition 10. [Graded Liftings of Monads] Consider two cartesian categories
E and C and a functor q : E → C strictly preserving finite products. We say
that a strong M -graded monad (Ṫ , η̇, µ̇m,m′ , st  ˙ m ) on E is an M -graded lifting
of a strong monad (T, η T , µ, st) on C along q if q ◦ Ṫ m = T ◦ q, q(η̇ψ ) = ηqψ ,
                                                  ˙ ψ,φ,m ) = stqψ,qφ .
q(µ̇m,m′ ,ψ ) = µqψ , q(Ṫ (m1 ≤ m2 )ψ ) = id, q(st
Theorem 2. Let V be cartesian category with distributive countable coproducts,
and let p : P → V be a fibration for assertion logic. Let T be a strong monad
on V and Ṫ be an M -graded lifting of T along p. Then the M -graded Freyd
                ˙ PṪ , J, ⊛) with homogeneous countable coproducts, together with
category (P, 1, ×,
the function qψ,φ,m : PṪ (ψ, φ)(m) → VT (pψ, pφ) defined by qψ,φ,m (f ) = pf is a
GHL structure over (V, 1, ×, VT , I, ∗) and p.
    Before seeing examples, we introduce a notation and fibrations for the asser-
tion logic. Let p : P → V be a fibration for the assertion logic. Below we use the
following notation: for f ∈ V(I, J) and ψ ∈ PI and φ ∈ PJ , by f : ψ →     ˙ φ we
mean the statement “there exists a morphism f˙ ∈ P(ψ, φ) such that pf˙ = f ”.
Such f˙ is unique due to the faithfulness of p : P → V.
Example 7 (Example 4: Union Bound Logic). To derive the GHL structure suit-
able for the semantics of the Union Bound Logic discussed in Example 4, we
invoke Theorem 2 by letting p be pSet : Pred → Set (Example 6), T be the
subdistribution monad D and Ṫ be the strong (R≥0 , ≤, 0, +)-graded lifting U of
D defined by U(δ)(X, P ) , (D(X), {d | d(X \ P ) ≤ δ}). The induced GHL struc-
ture is suitable for the semantics of GHL for Union Bound Logic in Example
4. The soundness of inference rules follow from the GHL structure as we have
showed in Section 5.2. To complete the semantics of GHL for the Union Bound
Logic, we give the semantics hpi of procedures p ∈ Cps . Example 4 already gave
a semantic condition for these operators:

       Cps (φ, β, ψ)
        = {sampleµ,e | ∀s.s ∈ [[φ]] =⇒ Prs′ ←Jsampleµ,e K(s) [s′ ∈ [[¬ψ]]] ≤ β)}
        = {sampleµ,e | [[sampleµ,e ]] ∈ PredU ([[φ]], [[ψ]])(β)}

For any sampleµ,e ∈ Cp (φ, β, ψ), the interpretation hsampleµ,e i is [[sampleµ,e ]].
Example 8 (Example 3: Program Counter Security). To derive the GHL struc-
ture suitable for GHL with program counter security, we invoke Theorem 2 with:
                             Graded Hoare Logic and its Categorical Semantics               23

– The category ERel of endorelations defined as follows: an object (X, R) is a
  pair of X ∈ Set and R ⊆ X × X (i.e. an endorelation R on X) and an arrow
  f : (X, R) → (Y, S) is a function f : X → Y such that (f × f )(R) ⊆ S.
– The fibration for the assertion logic e : ERel → Set given by (X, R) 7→ X and
  f 7→ f .
– The writer monad Ws X = X × {tt, ff}∗ on Set with the monoid of bit strings.
– The strong 2∗ -graded lifting of Ws along e : ERel → Set, given by
  Ẇs σ(X, R) = (Ws X, {((x, σ ′ ), (y, σ ′ )) | (x, y) ∈ R ∧ σ ′ ≤ σ}).
 The derived GHL structure is suitable for the semantics of GHL in Example 3.
 To complete the structure of the logic, we need to interpret two commands
 cfTT, cfFF ∈ CExp and set the axioms of commands Cc .
     First [[cfTT]], [[cfFF]] : [[M]] → 1 in ERelẆ are defined by [[cfTT]] ≡ (∗, tt) and
 [[cfFF]] ≡ (∗, ff). Finally, we define Cc by (recall ≤ is prefix ordering of strings):
                   Cc (ψ, σ) = {cfTT | tt ≤ σ} ∪ {cfFF | ff ≤ σ}.
 Note, the graded lifting Ẇs σ relates only the pair of (x, σ ′ ) and (y, σ ′ ) with
 common strings of control flow. Hence, the derivation of proof tree of this logic
 forces the target program to have the same control flow under the precondition.
 Example 9 (GHL Structure from the product comonad). In the category Set, the
 functor CX , X × N forms a coproduct-preserving comonad called the product
 comonad. The right adjoint I : Set → SetC of the coKleisli resolution of C yields
 a Freyd category with countable coproducts. We next introduce a (N, ≤, 0 max)-
 graded lifting Ċ of the comonad C along the fibration pSet : Pred → Set. It is
 defined by Ċn(X, P ) , (CX, {(x, m) ∈ X × N | x ∈ P, m ≥ n}). Similarly, we
 give an (N, ≤, 0 max)-graded Freyd category (J, ⊛) induced by the graded lifting
 Ċ. In this way we obtain a GHL structure.
     By instantiating GHL with the above GHL structure, we obtain a program
 logic useful for reasoning about security levels. For example, when program P1
 requires security level 3 and P2 requires security level 7, the sequential compo-
 sition P1 ; P2 requires the higher security level 7 (= max(3, 7)).
     We give a simple structure for verifying security levels determined by mem-
 ory access. Fix a function VarLV : dom(ΓM ) → N assigning security levels to
 variables. For any expression e, we define its required security level SecLV(e) =
 sup{VarLV(x) | x ∈ FV(e)}. Using this, for each expression e of sort s ∈ S we
 introduce a procedure secre ∈ PExps called secured expression. It returns the
 value of e if the level is high enough, otherwise it returns a meaningless contant:
       [[secre ]](n, ξ) = if n ≥ SecLV(e) then [[e]](ξ) else a fixed constant cs .
 Secured expressions can be introduced through the following Cp :
     Cps (φ, l, ψ) = {secre | e : s, [[secre ]] ∈ PredC ([[φ]], [[ψ]])(l), SecLV(e) ≤ l}.
 The pomonoid (N, ≤, 0, max) in the above can also be replaced with a join semi-
 lattice with a least element (Q, ≤, ⊥, ∨). Thus, GHL can be instantiated to a
 graded comonadic model of security and its associated reasoning.
24      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

6    Related Work
Several works have studied abstract semantics of Hoare Logic. Martin et al. [31]
give a categorical framework based on traced symmetric monoidal closed cat-
egories. They also show that their framework can handle extensions such as
separation logic. However their framework does not directly model effects and it
cannot accommodate grading as is. Goncharov and Shröder [18] study a Hoare
Logic to reason in a generic way about programs with side effects. Their logic
and underlying semantics is based on an order-enriched monad and they show
a relative completeness result. Similarly, Hasuo [20] studies an abstract weakest
precondition semantics based on order-enriched monad. A similar categorical
model has also been used by Jacobs [23] to study the Dijkstra monad and the
Hoare monad. In the logic by Goncharov and Shröder [18] effects are encapsu-
lated in monadic types, while the weakest precondition semantics by Hasuo [20]
and the semantics by Jacobs [23] have no underlying calculus. Moreover, none
of them is graded. Maillard et al. [29] study a semantics framework based on
the Dijkstra monad for program verification. Their framework enables reason-
ing about different side effects and it separates specification from computation.
Their Dijkstra monad has a flavor of grading but the structure they use is more
complex than a pomonoid. Maillard et al. [30] focus on relational program log-
ics for effectful computations. They show how these logics can be derived in a
relational dependent type theory, but their logics are not graded.
    As we discussed in the introduction, several works have used grading struc-
tures similar to the one we study in this paper, although often with differ-
ent names. Katsumata studied monads graded by a pomonoid as a semantic
model for effects system [24]. A similar approach has also been studied else-
where [36,42]. Formal categorical properties of graded monads are pursued by
Fujii et al. [13]. Zhang defines a notion of graded category, but it differs to ours,
and is instead closer to a definition of a graded monad [55]. As we showed in
Section 4, graded categories can be constructed both by monads and comonads
graded by a pomonoid, and it can also capture graded structures that do not arise
from either of them. Milius et al. [33] also studied monads graded by a pomonoid
in the context of trace semantics where the grading represents a notion of depth
corresponding to trace length. Exploring whether there is a generalization of our
work to traces is an interesting future work.
    Various works study comonads graded with a semiring structure as a semantic
model of contextual computations captured by means of type systems [7,16,44].
In contrast, our graded comonads are graded by a pomonoid. The additive struc-
ture of the semiring in those works is needed to merge the gradings of different
instances of the same variable. This is natural for the λ-calculus where the con-
text represent multiple inputs, but there is only one conclusion (output). Here
instead, we focus on an imperative language. So, we have only one input, the
starting memory, and one output, the updated memory. Therefore, it is natural
to have just the multiplicative structure of the semiring as a pomonoid. The
categorical axiomatics of semiring-graded comonads are studied by Katsumata
from the double-category theoretic perspective [25].
                         Graded Hoare Logic and its Categorical Semantics      25

    Apart from graded monads, several generalizations of monads has been pro-
posed. Atkey introduces parameterized monads and corresponding parameterized
Freyd categories [1], demonstrating that parameterized monads naturally model
effectful computations with preconditions and postconditions. Tate defines pro-
ductors with composability of effectful computations controlled by a relational
‘effector’ structure [53]. Orchard et al. define category-graded monads, general-
izing graded and parameterised monads via lax functors and sketch a model of
Union Bound Logic in this setting (but predicates and graded-predicate inter-
action are not modelled, as they are here) [41]. Interesting future work is to
combine these general models of computational effects with Hoare logic.

7   Conclusion
We have presented a Graded Hoare Logic as a parameterisable framework for
reasoning about programs and their side effects, and studied its categorical se-
mantics. The key guiding idea is that grading can be seen as a refinement of
effectful computations. This has brought us naturally to graded categories but
to fully internalize this refinement idea we further introduced the new notion
of graded Freyd categories. To show the generality of our framework we have
shown how different examples are naturally captured by it.
    We conclude with some reflections on possible future work.

Future work Carbonneaux et al. present a quantitative verification approach for
amortized cost analysis via a Hoare logic augmented with multivariate quantities
associated to program variables [8]. Judgments ⊢ {Γ ; Q}S{Γ ′; Q′ } have pre- and
post-conditions Γ and Γ ′ and potential functions Q and Q′ . Their approach can
be mapped to GHL with a grading monoid representing how the potential func-
tions change. However, the multivariate nature of the analysis requires a more
fine-grained connection between the structure of the memory and the structure
of grades, which have not been developed yet. We leave this for future work.
    GHL allows us to capture the dependencies between assertions and grading
that graded program logics usually use. However, some graded systems (e.g. [4])
use more explicit dependencies by allowing grade variables—which are also used
for grading polymorphism. We plan to explore this direction in future work.
    The setting of graded categories in this work subsumes both graded mon-
ads and graded comonads and allows flexibility in the model. However, most
of our examples in Section 5.3 are related to graded monads. The literature
contains various graded comonad models of data-flow properties: like liveness
analysis [44], sensitivities [7], timing and scheduling [16], and information-flow
control [40]. Future work is to investigate how these structures could be adopted
to GHL for reasoning about programs.

Acknowledgements Katsumata and Sato carried out this research supported
by ERATO HASUO Metamathematics for Systems Design Project (No. JPM-
JER1603), JST. Orchard is supported by EPSRC grant EP/T013516/1. Gaboardi
is supported by the National Science Foundation under Grant No. 2040222.
26      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

References
 1. Atkey, R.: Parameterised notions of computation. J. Funct. Program. 19(3-4),
    335–376 (2009). https://doi.org/10.1017/S095679680900728X
 2. Barthe, G., Gaboardi, M., Grégoire, B., Hsu, J., Strub, P.: Proving differ-
    ential privacy via probabilistic couplings. In: 2016 31st Annual ACM/IEEE
    Symposium on Logic in Computer Science (LICS). pp. 1–10 (2016).
    https://doi.org/10.1145/2933575.2934554
 3. Barthe, G.: An introduction to relational program verification (2020),
    http://software.imdea.org/∼ gbarthe/ introrelver.pdf, working Draft
 4. Barthe, G., Gaboardi, M., Arias, E.J.G., Hsu, J., Roth, A., Strub, P.: Higher-
    order approximate relational refinement types for mechanism design and differen-
    tial privacy. In: Rajamani, S.K., Walker, D. (eds.) Proceedings of the 42nd An-
    nual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Lan-
    guages, POPL 2015, Mumbai, India, January 15-17, 2015. pp. 55–68. ACM (2015).
    https://doi.org/10.1145/2676726.2677000
 5. Barthe, G., Gaboardi, M., Grégoire, B., Hsu, J., Strub, P.: A Program Logic for
    Union Bounds. In: 43rd International Colloquium on Automata, Languages, and
    Programming, ICALP 2016, July 11-15, 2016, Rome, Italy. pp. 107:1–107:15 (2016).
    https://doi.org/10.4230/LIPIcs.ICALP.2016.107
 6. Barthe, G., Köpf, B., Olmedo, F., Zanella-Béguelin, S.: Probabilistic relational
    reasoning for differential privacy. ACM Trans. Progr. Lang. Syst. 35(3), 9:1–9:49
    (Nov 2013). https://doi.org/10.1145/2492061
 7. Brunel, A., Gaboardi, M., Mazza, D., Zdancewic, S.: A core quantitative coeffect
    calculus. In: Shao, Z. (ed.) Programming Languages and Systems - 23rd European
    Symposium on Programming, ESOP 2014, ETAPS 2014, Grenoble, France, April
    5-13, 2014, Proceedings. Lecture Notes in Computer Science, vol. 8410, pp. 351–
    370. Springer (2014). https://doi.org/10.1007/978-3-642-54833-8 19
 8. Carbonneaux, Q., Hoffmann, J., Shao, Z.: Compositional certified resource bounds.
    In: Proceedings of the 36th ACM SIGPLAN Conference on Programming Language
    Design and Implementation, Portland, OR, USA, June 15-17, 2015. pp. 467–478
    (2015). https://doi.org/10.1145/2737924.2737955
 9. Crole, R.L.: Categories for types. Cambridge University Press (1993)
10. Day, B.: Construction of Biclosed Categories. Ph.D. thesis, School of Mathematics
    of the University of New South Wales (1970)
11. Filinski, A.: Controlling Effects. Ph.D. thesis, Carnegie Mellon University (1996)
12. Floyd, R.W.: Assigning meanings to programs. Proceedings of Symposium on Ap-
    plied Mathematics 19, 19–32 (1967). https://doi.org/10.1007/978-94-011-1793-7 4
13. Fujii, S., Katsumata, S.y., Mellies, P.A.: Towards a formal theory of
    graded monads. In: International Conference on Foundations of Soft-
    ware Science and Computation Structures. pp. 513–530. Springer (2016).
    https://doi.org/10.1007/978-3-662-49630-5 30
14. Gaboardi, M., Katsumata, S., Orchard, D., Sato, T.: Graded Hoare
    Logic and its Categorical Semantics. CoRR abs/2007.11235 (2020),
    https://arxiv.org/abs/2007.11235
15. Gaboardi, M., Katsumata, S., Orchard, D.A., Breuvart, F., Uustalu, T.: Combin-
    ing effects and coeffects via grading. In: Garrigue, J., Keller, G., Sumii, E. (eds.)
    Proceedings of the 21st ACM SIGPLAN International Conference on Functional
    Programming, ICFP 2016, Nara, Japan, September 18-22, 2016. pp. 476–489. ACM
    (2016). https://doi.org/10.1145/2951913.2951939
                           Graded Hoare Logic and its Categorical Semantics        27

16. Ghica, D.R., Smith, A.I.: Bounded linear types in a resource semiring. In: Shao,
    Z. (ed.) Programming Languages and Systems - 23rd European Symposium on
    Programming, ESOP 2014, Held as Part of the European Joint Conferences on
    Theory and Practice of Software, ETAPS 2014, Grenoble, France, April 5-13, 2014,
    Proceedings. Lecture Notes in Computer Science, vol. 8410, pp. 331–350. Springer
    (2014). https://doi.org/10.1007/978-3-642-54833-8 18
17. Gibbons, J.: Comprehending ringads - for phil wadler, on the occasion of his 60th
    birthday. In: Lindley, S., McBride, C., Trinder, P.W., Sannella, D. (eds.) A List
    of Successes That Can Change the World - Essays Dedicated to Philip Wadler on
    the Occasion of His 60th Birthday. Lecture Notes in Computer Science, vol. 9600,
    pp. 132–151. Springer (2016). https://doi.org/10.1007/978-3-319-30936-1 7
18. Goncharov, S., Schröder, L.: A Relatively Complete Generic Hoare Logic for Order-
    Enriched Effects. In: 28th Annual ACM/IEEE Symposium on Logic in Computer
    Science, LICS 2013, New Orleans, LA, USA, June 25-28, 2013. pp. 273–282. IEEE
    Computer Society (2013). https://doi.org/10.1109/LICS.2013.33
19. Goubault-Larrecq, J., Lasota, S., Nowak, D.: Logical relations for monadic
    types. Mathematical Structures in Computer Science 18(6), 1169–1217 (2008).
    https://doi.org/10.1017/S0960129508007172
20. Hasuo, I.: Generic weakest precondition semantics from monads en-
    riched with order. Theoretical Computer Science 604, 2 – 29 (2015).
    https://doi.org/https://doi.org/10.1016/j.tcs.2015.03.047,    coalgebraic    Meth-
    ods in Computer Science
21. Ivašković, A., Mycroft, A., Orchard, D.: Data-Flow Analyses as Effects and
    Graded Monads. In: Ariola, Z.M. (ed.) 5th International Conference on For-
    mal Structures for Computation and Deduction (FSCD 2020). Leibniz In-
    ternational Proceedings in Informatics (LIPIcs), vol. 167, pp. 15:1–15:23.
    Schloss Dagstuhl–Leibniz-Zentrum für Informatik, Dagstuhl, Germany (2020).
    https://doi.org/10.4230/LIPIcs.FSCD.2020.15
22. Jacobs, B.: Categorical Logic and Type Theory. Elsevier (1999)
23. Jacobs, B.: Dijkstra and Hoare monads in monadic computation. Theor. Comput.
    Sci. 604, 30–45 (2015). https://doi.org/10.1016/j.tcs.2015.03.020
24. Katsumata, S.: Parametric effect monads and semantics of effect systems.
    In: Jagannathan, S., Sewell, P. (eds.) The 41st Annual ACM SIGPLAN-
    SIGACT Symposium on Principles of Programming Languages, POPL ’14,
    San Diego, CA, USA, January 20-21, 2014. pp. 633–646. ACM (2014).
    https://doi.org/10.1145/2535838.2535846
25. Katsumata, S.: A Double Category Theoretic Analysis of Graded Linear Ex-
    ponential Comonads. In: Baier, C., Lago, U.D. (eds.) Foundations of Software
    Science and Computation Structures - 21st International Conference, FOSSACS
    2018, ETAPS 2018, Thessaloniki, Greece, April 14-20, 2018, Proceedings. Lec-
    ture Notes in Computer Science, vol. 10803, pp. 110–127. Springer (2018).
    https://doi.org/10.1007/978-3-319-89366-2 6
26. Katsumata, S., Sato, T., Uustalu, T.: Codensity lifting of monads
    and its dual. Logical Methods in Computer Science 14(4) (2018).
    https://doi.org/10.23638/LMCS-14(4:6)2018
27. Kura, S.: Graded Algebraic Theories. In: International Conference on Foundations
    of Software Science and Computation Structures. pp. 401–421. Springer (2020).
    https://doi.org/10.1007/978-3-030-45231-5 21
28. Levy,       P.B.:  Locally      graded     categories.   Slides    available    at
    http://www.cs.bham.ac.uk/∼ pbl/papers/locgrade.pdf (2019)
28      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

29. Maillard, K., Ahman, D., Atkey, R., Martı́nez, G., Hritcu, C., Rivas, E., Tanter,
    É.: Dijkstra monads for all. Proc. ACM Program. Lang. 3(ICFP), 104:1–104:29
    (2019). https://doi.org/10.1145/3341708
30. Maillard, K., Hritcu, C., Rivas, E., Muylder, A.V.: The next 700 rela-
    tional program logics. Proc. ACM Program. Lang. 4(POPL), 4:1–4:33 (2020).
    https://doi.org/10.1145/3371072
31. Martin, U., Mathiesen, E.A., Oliva, P.: Hoare Logic in the Abstract. In: Ésik, Z.
    (ed.) Computer Science Logic. pp. 501–515. Springer Berlin Heidelberg, Berlin,
    Heidelberg (2006). https://doi.org/10.1007/11874683 33
32. Melliès, P., Zeilberger, N.: Functors are Type Refinement Systems. In: Ra-
    jamani, S.K., Walker, D. (eds.) Proceedings of the 42nd Annual ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
    POPL 2015, Mumbai, India, January 15-17, 2015. pp. 3–16. ACM (2015).
    https://doi.org/10.1145/2676726.2676970
33. Milius, S., Pattinson, D., Schröder, L.: Generic Trace Semantics and Graded Mon-
    ads. In: Moss, L.S., Sobocinski, P. (eds.) 6th Conference on Algebra and Coal-
    gebra in Computer Science (CALCO 2015). Leibniz International Proceedings in
    Informatics (LIPIcs), vol. 35, pp. 253–269. Schloss Dagstuhl–Leibniz-Zentrum fuer
    Informatik (2015). https://doi.org/10.4230/LIPIcs.CALCO.2015.253
34. Moggi, E.: Notions of computation and monads. Inf. Comput. 93(1), 55–92 (1991).
    https://doi.org/10.1016/0890-5401(91)90052-4
35. Molnar, D., Piotrowski, M., Schultz, D., Wagner, D.A.: The program counter secu-
    rity model: Automatic detection and removal of control-flow side channel attacks.
    In: Won, D., Kim, S. (eds.) Information Security and Cryptology - ICISC 2005, 8th
    International Conference, Seoul, Korea, December 1-2, 2005, Revised Selected Pa-
    pers. Lecture Notes in Computer Science, vol. 3935, pp. 156–168. Springer (2005).
    https://doi.org/10.1007/11734727 14
36. Mycroft, A., Orchard, D.A., Petricek, T.: Effect Systems Revisited - Control-
    Flow Algebra and Semantics. In: Probst, C.W., Hankin, C., Hansen, R.R.
    (eds.) Semantics, Logics, and Calculi - Essays Dedicated to Hanne Riis
    Nielson and Flemming Nielson on the Occasion of Their 60th Birthdays.
    Lecture Notes in Computer Science, vol. 9560, pp. 1–32. Springer (2016).
    https://doi.org/10.1007/978-3-319-27810-0 1
37. Nielson, H.R.: A Hoare-like proof system for analysing the computation
    time of programs. Science of Computer Programming 9(2), 107–136 (1987).
    https://doi.org/10.1016/0167-6423(87)90029-3
38. Nielson, H.R., Nielson, F.: Semantics with applications, vol. 104. Springer (1992)
39. Olmedo, F.: Approximate Relational Reasoning for Probabilistic Programs. Ph.D.
    thesis, Technical University of Madrid (2014)
40. Orchard, D., Liepelt, V., III, H.E.: Quantitative program reasoning with
    graded modal types. Proc. ACM Program. Lang. 3(ICFP), 110:1–110:30 (2019).
    https://doi.org/10.1145/3341714
41. Orchard, D., Wadler, P., III, H.E.: Unifying graded and parameterised mon-
    ads. In: New, M.S., Lindley, S. (eds.) Proceedings Eighth Workshop on
    Mathematically Structured Functional Programming, MSFP@ETAPS 2020,
    Dublin, Ireland, 25th April 2020. EPTCS, vol. 317, pp. 18–38 (2020).
    https://doi.org/10.4204/EPTCS.317.2
42. Orchard, D.A., Petricek, T., Mycroft, A.: The semantic marriage of monads and
    effects. CoRR abs/1401.5391 (2014), http://arxiv.org/abs/1401.5391
                           Graded Hoare Logic and its Categorical Semantics        29

43. Petricek, T., Orchard, D.A., Mycroft, A.: Coeffects: Unified static analysis of
    context-dependence. In: Fomin, F.V., Freivalds, R., Kwiatkowska, M.Z., Peleg,
    D. (eds.) Automata, Languages, and Programming - 40th International Col-
    loquium, ICALP 2013, Riga, Latvia, July 8-12, 2013, Proceedings, Part II.
    Lecture Notes in Computer Science, vol. 7966, pp. 385–397. Springer (2013).
    https://doi.org/10.1007/978-3-642-39212-2 35
44. Petricek, T., Orchard, D.A., Mycroft, A.: Coeffects: a calculus of context-
    dependent computation. In: Jeuring, J., Chakravarty, M.M.T. (eds.) Proceed-
    ings of the 19th ACM SIGPLAN international conference on Functional pro-
    gramming, Gothenburg, Sweden, September 1-3, 2014. pp. 123–135. ACM (2014).
    https://doi.org/10.1145/2628136.2628160
45. Pitts, A.M.: Categorical logic. Tech. rep., University of Cambridge, Computer Lab-
    oratory (1995)
46. Power, J.: Generic models for computational effects. Theoretical Computer Science
    364(2), 254–269 (2006). https://doi.org/10.1016/j.tcs.2006.08.006
47. Power, J., Thielecke, H.: Environments, continuation semantics and indexed cat-
    egories. In: Abadi, M., Ito, T. (eds.) Theoretical Aspects of Computer Software.
    pp. 391–414. Springer Berlin Heidelberg, Berlin, Heidelberg (1997)
48. Sato, T.: Approximate Relational Hoare Logic for Continuous Random Sam-
    plings. In: Birkedal, L. (ed.) The Thirty-second Conference on the Mathe-
    matical Foundations of Programming Semantics, MFPS 2016, Carnegie Mel-
    lon University, Pittsburgh, PA, USA, May 23-26, 2016. Electronic Notes
    in Theoretical Computer Science, vol. 325, pp. 277–298. Elsevier (2016).
    https://doi.org/10.1016/j.entcs.2016.09.043
49. Sato, T., Barthe, G., Gaboardi, M., Hsu, J., Katsumata, S.: Approximate
    Span Liftings: Compositional Semantics for Relaxations of Differential Pri-
    vacy. In: 34th Annual ACM/IEEE Symposium on Logic in Computer Sci-
    ence, LICS 2019, Vancouver, BC, Canada, June 24-27, 2019. pp. 1–14 (2019).
    https://doi.org/10.1109/LICS.2019.8785668
50. Smirnov, A.: Graded monads and rings of polynomials. J. Math. Sci. 151(3), 3032–
    3051 (2008). https://doi.org/10.1007/s10958-008-9013-7
51. Staton, S.: Freyd categories are Enriched Lawvere Theories. Elec-
    tronic Notes in Theoretical Computer Science 303, 197 – 206 (2014).
    https://doi.org/https://doi.org/10.1016/j.entcs.2014.02.010,      proceedings   of
    the Workshop on Algebra, Coalgebra and Topology (WACT 2013)
52. Staton, S.: Commutative semantics for probabilistic programming. In: Yang, H.
    (ed.) Programming Languages and Systems - 26th European Symposium on Pro-
    gramming, ESOP 2017, ETAPS 2017, Uppsala, Sweden, April 22-29, 2017, Pro-
    ceedings. Lecture Notes in Computer Science, vol. 10201, pp. 855–879. Springer
    (2017). https://doi.org/10.1007/978-3-662-54434-1 32
53. Tate, R.: The sequential semantics of producer effect systems. In: Giacobazzi, R.,
    Cousot, R. (eds.) The 40th Annual ACM SIGPLAN-SIGACT Symposium on Prin-
    ciples of Programming Languages, POPL ’13, Rome, Italy - January 23 - 25, 2013.
    pp. 15–26. ACM (2013). https://doi.org/10.1145/2429069.2429074
54. Wood, R.J.: V-indexed categories, chap. 2, pp. 126–140. No. 661 in Lecture Notes
    in Mathematics, Springer (1978). https://doi.org/10.1007/BFb0061362
55. Zhang, J.J.: Twisted graded algebras and equivalences of graded cate-
    gories. Proceedings of the London Mathematical Society 3(2), 281–311 (1996).
    https://doi.org/10.1112/plms/s3-72.2.281
30      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
    The images or other third party material in this chapter are included in the chapter’s
Creative Commons license, unless indicated otherwise in a credit line to the material. If
material is not included in the chapter’s Creative Commons license and your intended
use is not permitted by statutory regulation or exceeds the permitted use, you will need
to obtain permission directly from the copyright holder.
                          Graded Hoare Logic and its Categorical Semantics              31

A    Further examples

Example 10 (Dataflow-aware Bounded Reading). Via our grading, we can im-
plement classical-style dataflow analyses. For simplicity, we consider a counting
analysis akin to the usage analysis in Bounded Linear Logic [?], where instead of
counting the number of times a variable is used, we count the number of times
that variables are read from, in a dataflow-aware fashion.
    Let N be the number of variables in ΓM . An expression analysis is a func-
tion counts : ExpΣ (ΓM , s) → NN (s ∈ S) which computes an N -vector whose
elements correspond to the number of times that each program variable is read
by an expression:

      count(vi ) = hi|   count(o(e1 , · · · , en )) = count(e1 ) + · · · + count(en )   (2)

where vi is the ith variable in ΓM and hi| computes a single-entry vector where
hi|j = 1 if i = j otherwise hi|j = 0. For example, in a program with three variables
x, y, and z (taken in that order for the analysis), then count(x+y +y) = h1, 2, 0i.
    We define a dataflow-aware analysis by grading GHL with a pomonoid M of
square matrices N × N with the all-zeros matrix 0̄N ×N as the unit, preordering
≤ pointwise on N, and multiplication:

                             A # B , (B ∗ A) + A + B.

To integrate the analysis to GHL, we analyse assignments via procedures such
that do v ← #(e) denotes the assignment of an expression e of sort ΓM (v) to
variable v incurring an analysis in the GHL:
                                                           T
         PExps = {#(e) | e : s},       #(e) ∈ Cps (ψ, hi| ∗ count(e), r = e)

where the analysis of an assignment to vi of expression e is given by the grade
   T
hi| ∗ count(e) which multiplies the transpose of the single-entry basis vector for
i with the analysis count(e), yielding an N × N data flow matrix. For example,
take the program do x ← #(y + 2); do z ← #(x + y). The first assignment has
grade:
                                                             
                                        1                0 1 0
                   T                              
                hx| ∗ count(y + 2) = 0 ∗ 0 1 0 = 0 0 0
                                        0                0 0 0

The resulting matrix can read as follows: the columns correspond to the source
of the dataflow and the rows the target, thus in this case we see that y (second
variable) is used once to form x (first variable). The second assignment has the
analysis:
                                                             
                                         0                0 0 0
                   T                                
                hz| ∗ count(x + y) = 0 ∗ 1 0 1 = 0 0 0
                                         1                1 1 0
32        Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

Taken together using # from the sequential composition, the full program then
has the analysis:
                                                                
  0 1 0      0 0 0       0 0 0    0 1 0       0 1 0       0 0 0        0 1 0
0 0 0 # 0 0 0 = 0 0 0∗0 0 0 + 0 0 0 + 0 0 0 = 0 0 0
  0 0 0      1 1 0       1 1 0    0 0 0       0 0 0       1 1 0        1 2 0

Thus, y flows once to x and twice to z and x flows once to z. The analysis of each
assignment gives an adjacency matrix for the dataflow graph of the statement
and # computes the two-hop paths between two dataflow graphs (B ∗ A) plus the
original adjacency/flows A and B for each statement.

Semantic model in our framework Let Var be the set of variables in ΓM and
M be the set of functions Var × Var → N, regarded as a square matrix over
P We define a binary operation # on M by (A # B)(x, y) = A(x, y) + B(x, y) +
N.
    z∈Var A(x, z)·B(z, y). The operation # is associative, and everywhere-0 matrix
∅ is the unit of this operation. The componentwise numerical order between
matrices makes (M, ≤, ∅, #) a partially ordered monoid.
     We now invoke Theorem 2 by letting p be the fibration pSet : Pred → Set, T
be the M -valued writer monad WM X = X × M and Ṫ be the strong M -graded
lifting ẆM given by ẆM (A)(X, P ) , (WM X, {(x, B) ∈ WM X | x ∈ P, B ≤ A}).
Using the semantics of GHL with this GHL structure, we develop a program
logic for verification of dataflow-aware reuse bounds.
     Expressions with reuse bounds are given as procedures. For each expression
e, we define a function #e : Var → N that inductively counts variable usages.
We introduce a procedure name asgn(e) ∈ PExps for each expression e of sort
s. Its interpretation [[asgn(e)]] : M → WM (M) is [[asgn(e)]] = ([[e]], Ae ) where
Ae (y, z) , #e(y) · dx (z). We then define Cps by

     Cps (φ, A, ψ) = {asgn(e) | e : s, [[asgn(e)]] ∈ PredẆM ([[φ]], [[ψ]])(Ae ), Ae ≤ A}.
                          Graded Hoare Logic and its Categorical Semantics              33

A    Further examples

Example 11 (Dataflow-aware Bounded Reading). Via our grading, we can im-
plement classical-style dataflow analyses. For simplicity, we consider a counting
analysis akin to the usage analysis in Bounded Linear Logic [GSS92], where in-
stead of counting the number of times a variable is used, we count the number
of times that variables are read from, in a dataflow-aware fashion.
    Let N be the number of variables in ΓM . An expression analysis is a func-
tion counts : ExpΣ (ΓM , s) → NN (s ∈ S) which computes an N -vector whose
elements correspond to the number of times that each program variable is read
by an expression:

      count(vi ) = hi|   count(o(e1 , · · · , en )) = count(e1 ) + · · · + count(en )   (3)

where vi is the ith variable in ΓM and hi| computes a single-entry vector where
hi|j = 1 if i = j otherwise hi|j = 0. For example, in a program with three variables
x, y, and z (taken in that order for the analysis), then count(x+y +y) = h1, 2, 0i.
    We define a dataflow-aware analysis by grading GHL with a pomonoid M of
square matrices N × N with the all-zeros matrix 0̄N ×N as the unit, preordering
≤ pointwise on N, and multiplication:

                             A # B , (B ∗ A) + A + B.

To integrate the analysis to GHL, we analyse assignments via procedures such
that do v ← #(e) denotes the assignment of an expression e of sort ΓM (v) to
variable v incurring an analysis in the GHL:
                                                           T
         PExps = {#(e) | e : s},       #(e) ∈ Cps (ψ, hi| ∗ count(e), r = e)

where the analysis of an assignment to vi of expression e is given by the grade
   T
hi| ∗ count(e) which multiplies the transpose of the single-entry basis vector for
i with the analysis count(e), yielding an N × N data flow matrix. For example,
take the program do x ← #(y + 2); do z ← #(x + y). The first assignment has
grade:
                                                             
                                        1                0 1 0
                   T                              
                hx| ∗ count(y + 2) = 0 ∗ 0 1 0 = 0 0 0
                                        0                0 0 0

The resulting matrix can read as follows: the columns correspond to the source
of the dataflow and the rows the target, thus in this case we see that y (second
variable) is used once to form x (first variable). The second assignment has the
analysis:
                                                             
                                         0                0 0 0
                   T                                
                hz| ∗ count(x + y) = 0 ∗ 1 0 1 = 0 0 0
                                         1                1 1 0
34        Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

Taken together using # from the sequential composition, the full program then
has the analysis:
                                                                
  0 1 0      0 0 0       0 0 0    0 1 0       0 1 0       0 0 0        0 1 0
0 0 0 # 0 0 0 = 0 0 0∗0 0 0 + 0 0 0 + 0 0 0 = 0 0 0
  0 0 0      1 1 0       1 1 0    0 0 0       0 0 0       1 1 0        1 2 0
Thus, y flows once to x and twice to z and x flows once to z. The analysis of each
assignment gives an adjacency matrix for the dataflow graph of the statement
and # computes the two-hop paths between two dataflow graphs (B ∗ A) plus the
original adjacency/flows A and B for each statement.

Semantic model in our framework Let Var be the set of variables in ΓM and
M be the set of functions Var × Var → N, regarded as a square matrix over
P We define a binary operation # on M by (A # B)(x, y) = A(x, y) + B(x, y) +
N.
    z∈Var A(x, z)·B(z, y). The operation # is associative, and everywhere-0 matrix
∅ is the unit of this operation. The componentwise numerical order between
matrices makes (M, ≤, ∅, #) a partially ordered monoid.
     We now invoke Theorem 2 by letting p be the fibration pSet : Pred → Set, T
be the M -valued writer monad WM X = X × M and Ṫ be the strong M -graded
lifting ẆM given by ẆM (A)(X, P ) , (WM X, {(x, B) ∈ WM X | x ∈ P, B ≤ A}).
Using the semantics of GHL with this GHL structure, we develop a program
logic for verification of dataflow-aware reuse bounds.
     Expressions with reuse bounds are given as procedures. For each expression
e, we define a function #e : Var → N that inductively counts variable usages.
We introduce a procedure name asgn(e) ∈ PExps for each expression e of sort
s. Its interpretation [[asgn(e)]] : M → WM (M) is [[asgn(e)]] = ([[e]], Ae ) where
Ae (y, z) , #e(y) · dx (z). We then define Cps by

     Cps (φ, A, ψ) = {asgn(e) | e : s, [[asgn(e)]] ∈ PredẆM ([[φ]], [[ψ]])(Ae ), Ae ≤ A}.

B       Proofs for Section 4 (Graded Categories)
Proof. (Proof of Proposition 1) (1) Let Y ∈ CT and fi : Xi →m Y be I-indexed
morphisms. Then the cotupling [fi ]i∈I taken in C is a morphism of type Z →m Y
in CT . It is easy to verify that {fi }i∈I 7→ [fi ]i∈I is the inverse of λh . (µ1,m,Z ◦
T 1h ◦ ηZ ◦ ιi )i∈I .
   (2) This case can be proven similarly, using the fact that Dm preserves
coproducts.

C       Coherence Laws of Strength
1 × T mX
       ❖❖❖
               / T m(1 × X) X × (Y × T mZ)                    / X × T m(Y × Z)           / T m(X × (Y × Z))
          ❖❖❖
             ❖❖❖
                 ❖❖' 
                                                                                                  
                    T mX    (X × Y ) × T mZ                                              / T m((X × Y ) × Z)
                                 Graded Hoare Logic and its Categorical Semantics                     35

X × Y▼        / X × T 1Y X × T m(T m′Y )                           / T m(X × T m′ Y )             / T m(T m′ (X × Y ))
      ▼▼▼
         ▼▼▼
            ▼▼▼
                ▼&                                                                                        
             T 1(X × Y ) X × T (mm′ )Y                                                            / T (mm′ )(X × Y )

Proof. (Proof of Proposition 2) Thanks to the strong graded monad structure
of T , we easily satisfy the equalities for M -graded Freyd category.
           T
I(idX ) = ηX = idX ,         I(g ◦ f ) = (η T ◦ g)♯ ◦ (η T ◦ f ) = Ig ◦CT If,
idV ∗ idX = stTV,X ◦ (idV × ηX
                             T
                               ) = ηVT ×X = idC
                                              V ×X ,
                                                T



(g ◦ f ) ∗ (i ◦CT j) = stT ◦ (g ◦ f × i♯ ◦ j) = (stT ◦ (g × i))♯ ◦ stT ◦ (f × j) = (g ∗ i) ◦CT (f ∗ j),
f ∗ ↑nm g = stT ◦ (f × T (m ≤ n) ◦ g) = T (m ≤ n) ◦ stT (f × g) = ↑nm (f ∗ g),
I(lX ) ◦CT (id1 ∗ f ) = T (lX ) ◦ stT ◦ (id1 × f ) = lT Y ◦ (id1 × f ) = f ◦ lX = f ◦CT I(lX )
I(aX ′ ,Y ′ ,Z ′ ) ◦CT ((f × g) ∗ h) = T (aX ′ ,Y ′ ,Z ′ ) ◦ stTX ′ ×Y ′ ,T Z ′ ◦ ((f × g) × h)
= stTX ′ ,Y ′ ×Z ′ ◦ (idX ′ × stTY ′ ,T Z ′ ) ◦ aX ′ ,Y ′ ,T Z ′ ◦ ((f × g) × h)
= stTX ′ ,Y ′ ×Z ′ ◦ (idX ′ × stTY ′ ,T Z ′ ) ◦ (f × (g × h)) ◦ aX,Y,Z = (f ∗ (g ∗ h)) ◦CT I(aX,Y,Z )
I(f × g) = η T ◦ (f × g) = stT ◦ (f × η T ◦ g) = f ∗ Ig,

Proof. (Proof of Proposition 2) We next suppose that the underlying category C
has coproducts. Then, the Kleisli grade` category CT has homogeneous coprod-
ucts. From the` coprojections ιi : X i →  i∈A Xi in C, The tuple of morphisms
I(ιi ) : Xi →1 i∈A Xi in CT forms a countable homogeneous coproduct.


      [fi ]i∈A ◦CT I(ιi ) = [fi ]♯i∈A ◦ (η T̀            ◦ ιi ) = [fi ]i∈A ◦ ιi = fi
                                                i∈I Xi

              [I(ιi )]i∈A = η T̀            ◦ [ιi ]i∈A = η T̀            = idC
                                                                             `T        ,
                                   i∈I Xi                       i∈A Xi        i∈A Xi

          h ◦CT [fi ]i∈A = h♯ ◦ [fi ]i∈I = [h♯ ◦ fi ]i∈A = [h ◦CT fi ]i∈I ,
           [↑nm (fi )]i∈A = [T (m ≤ n) ◦ fi ]i∈A = T (m ≤ n)[fi ]i∈A =↑nm [fi ]i∈A .

From the construction of the homogeneous coproducts and the unit law of the
tensorial strength (stTX,Y ◦ (idX × ηYT ) = ηX×Y
                                             T
                                                 ), I preserves the distributivity.
                                                                     `
Hence, idV ∗ I(ιi ) = I(idV × ιi ), where idV × ιi : V ×
                                                       ` Xi → V × i∈A Xi are
coprojections. Hence (idV ∗ I(ιi ) : V × Xi →1 V × i∈A Xi )i∈A also forms a
countable homogeneous coproduct. Since homogeneous coproduct are unique
up to isomorphisms, we then conclude that (C, 1, ×, CT , I, ∗) has homogeneous
countable coproducts.


D      Proofs for Section 5 (Modelling Graded Hoare Logic)
We formally state various known facts in coherent posetal fibrations:
Proposition 3. For any morphism f, g ∈ V(X, Y ), the following holds.
36      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

1. [Jac99, Proposition 3.4.6] Eq(f, g) = Eq(hid, f i, hid, gi).
2. [Jac99, Lemma 3.4.5] For any ψ ∈ PY , f ∗ ψ ∧ Eq(f, g) 6 g ∗ ψ.
3. [Jac99, Notation 3.4.2] For any h ∈ V(Z, X), h∗ Eq(f, g) = Eq(f ◦ h, g ◦ h).
4. [Jac99, Example 4.3.7] For f ∈ V(X, Y ), the function f∗ : PX → PY defined
   below is a left adjoint to the reindexing function f ∗ : PY → PX (hence p is
   a bifibration).
                                      ′
                       f∗ ψ , ∃Y,X ((πY,X )∗ ψ ∧ Eq(f ◦ πY,X
                                                         ′
                                                             , πY,X )).                (4)
5. [Jac99] The category P has finite products and distributive countable coprod-
   ucts that are strictly preserved by p.
Proof. We briefly prove point (5). Let {ψi }i∈N ∈ P. For a countable coproduct
{ιi : pψi → X}i∈N in V, the following family is a countable coproduct in P above
                            ιi (ψi )               ր        W
coproduct {ιi }i∈N : { ψi            / (ιi )∗ ψi          /
                                                             i∈N (ιi )∗ ψi }i∈N .


Interpretation of Graded Hoare Logic
Proof. In this proof [[ψ]], [[eb ]] are abbreviated to ψ, eb respectively. First, we ob-
tain one direction:
                                     ψ ∧ Eq(eb , tt ◦ !)
                   Proposition 3-1 = ψ ∧ Eq(hid, eb i, tm)
                                      6 hid, eb i∗ Im ∧ Eq(hid, eb i, tm)
                   Proposition 3-2 6 tm∗ Im.
We show the other direction tm∗ Im 6 ψ ∧ Eq(eb , tt ◦ !).
                       tm∗ Im
     Pushforward (4) = tm∗ (π ′ )∗ (π ∗ ψ ∧ Eq(hid, eb i ◦ π, π ′ ))
      Beck-Chevalley = (π ′ )∗ (M × tm)∗ (π ∗ ψ ∧ Eq(hid, eb i ◦ π, π ′ ))
                     = (π ′ )∗ ((M × tm)∗ π ∗ ψ ∧ (M × tm)∗ Eq(hid, eb i ◦ π, π ′ ))
                PBEQ = (π ′ )∗ (π ∗ ψ ∧ Eq(hid, eb i ◦ π, tm ◦ π ′ ))
                     = (π ′ )∗ (π ∗ ψ ∧ Eq(hπ, eb ◦ πi, hπ ′ , tt ◦ ! ◦ πi))
      Proposition 3-1 = (π ′ )∗ (π ∗ ψ ∧ Eq(eb ◦ π, tt ◦ ! ◦ π ′ ) ∧ Eq(π, π ′ ))
                      = (π ′ )∗ (π ∗ ψ ∧ Eq(eb ◦ π, tt ◦ ! ◦ π) ∧ Eq(π, π ′ ))
              PBEQ = (π ′ )∗ (π ∗ ψ ∧ π ∗ Eq(eb , tt ◦ !) ∧ Eq(π, π ′ ))
      Proposition 3-2 = (π ′ )∗ ((π ′ )∗ ψ ∧ (π ′ )∗ Eq(eb , tt ◦ !))
                         6 ψ ∧ Eq(eb , tt ◦ !).
Proof. In this proof we abbreviate [[ψ]], [[eb ]] to ψ, eb respectively. The direction
tm∗ tm∗ Im ∨ fm∗ fm∗ Im ≤ Im is immediate. We thus show the converse. Assume
ψ 6 Eq(eb , tt◦!) ∨ Eq(eb , ff◦!). This is equivalent to
                      ψ = (ψ ∧ Eq(eb , tt◦!)) ∨ (ψ ∧ Eq(eb , ff◦!)).
                                  Graded Hoare Logic and its Categorical Semantics                    37

By applying hid, ei∗ both sides, which preserves joins, we obtain
      Im = hid, eb i∗ ψ = hid, eb i∗ (ψ ∧ Eq(eb , tt◦!)) ∨ hid, eb i∗ (ψ ∧ Eq(eb , ff◦!));
From this, we aim to show
                             hid, eb i∗ (ψ ∧ Eq(eb , tt◦!)) 6 tm∗ tm∗ Im;
the case for ff and fm is similar. Using the adjoint mate, the goal is equivalent
to
                   ψ ∧ Eq(eb , tt◦!) 6 hid, eb i∗ tm∗ tm∗ hid, eb i∗ ψ.
   Then we proceed as follows.
                        ψ ∧ Eq(eb , tt◦!)
      Proposition 3-1 = ψ ∧ Eq(hid, eb i, tm) ∧ Eq(tm, hid, eb i)
                      6 hid, eb i∗ hid, eb i∗ ψ ∧ Eq(hid, eb i, tm) ∧ Eq(tm, hid, eb i)
      Proposition 3-2 6 tm∗ hid, eb i∗ ψ ∧ Eq(tm, hid, eb i)
                      6 tm∗ tm∗ tm∗ hid, eb i∗ ψ ∧ Eq(tm, hid, eb i)
      Proposition 3-2 6 hid, eb i∗ tm∗ tm∗ hid, eb i∗ ψ.
Proof. Assume [[ψN ]] ≤ Eq([[en ]], ⌊N ⌋). Then we proceed as follows:
                    [[ψN ]] = [[ψN ]] ∧ Eq([[en ]], ⌊N ⌋)
          Proposition 3-1 = [[ψN ]] ∧ Eq(hidM , [[en ]]i, [N ])
                          ≤ hidM , [[en ]]i∗ hidM , [[en ]]i∗ [[ψN ]] ∧ Eq(hidM , [[en ]]i, [N ])
          Proposition 3-2 ≤ [N ]∗ hidM , [[en ]]i∗ [[ψN ]].
We thus conclude [N ]∗ [[ψN ]] ≤ hidM , [[en ]]i∗ [[ψN ]]. We obtain the other direction
similarly.
Proof. By induction over the interpretation.

D.1        Further instances of Graded Hoare Logic
Proof. Checking the equalities in Definition 9 is routine. We only check the
ex-falso-quodlibet. For all φ and m, the mapping q⊥X ,φ,m : PṪ (⊥X , φ)(m) →
VT (X, pφ) is bijective:
                PṪ (⊥X , φ)(m) = P(⊥X , Ṫ mφ) ∼
                                                = V(X, T pφ) = VT (X, pφ).
Notice that the functor ⊥(X) , ⊥X is a left adjoint to p.
   Using Example 6, we derive fibrations for assertion logic by change-of-base:

   ERel✤                / BRel             BRel✤             / Pred      Pred(Meas)                 / Pred
     ❴                                       ❴                                 ❴✤
      e                      r              r                     p        pMeas                        p
      diagonal                                        ×                               |−|         
    Set        / Set × Set              Set × Set             / Set           Meas                  / Set
38      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

Example 12 (A continuous model of the Union Bound Logic.). We can also define
a continuous model of the Union Bound Logic. Let G be the subprobabilistic
variant of the Giry monad (called the sub-Giry monad) [Gir82] on the category
Meas of measurable spaces and measurable functions. In a similar way as U,
we also define a strong ([0, ∞], +, 0, ≤)-graded lifting V of G along the fibration
pMeas : Pred(Meas) → Meas for assertion logic.

 V δ (X, P ) = (G(X), {µ ∈ G(X)|∀A ⊆measurable X. P ⊆ A =⇒ µ(X \ A) ≤ δ})
                                                                           (L1’)
               \      −1   ′                      ′
             = {(f ♯ ) (S δ +δ )|f : (X, P ) →
                                             ˙ S δ measurable, δ ′ ∈ R≥0 } (L2’)
                                                                                      ′
[(L1′ ) ⊆ (L2′ )] Suppose µ ∈ (L1′ ). For any measurable f : (X, P ) →            ˙ S δ , we
should have P ⊆ X \ f −1 ([δ ′ , 1]). Therefore µ(f −1 ([δ ′ , 1])) ≤ δ. Hence f ♯ (µ) ≤
µ(f −1 ([δ ′ , 1]))+δ ′ ≤ δ +δ ′ . Hence, µ ∈ (L2′ ). [(L1′ ) ⊇ (L2′ )] For any measurable
subset A with P ⊆ A, define a measurable function fA : (X, P ) →          ˙ S 0 by f (x) = 0
                                                                   ♯
when x ∈ A and f (x) = 1 otherwise. We then have δ ≥ fA (µ) = µ(X \ A).
   Technically, we handle X and [0, 1] as a measurable space and a standard
Borel space respectively, and we apply the graded version of codensity lifting
[Sat16,KSU18] instead of the graded ⊤⊤-lifting to construct V. At all, we obtain
a GHL structure induced from V, G and pMeas : Pred(Meas) → Meas. In-
stantiating GHL with this structure yields a continuous version of Union Bound
Logic.

Example 13 (Example 2: Simple Cost analysis). We introduced a cost counting
with a natural-number monoid and the tick command graded by 1 ∈ N. To ob-
tain a GHL structure suitable for the GHL for cost counting, we invoke Theorem
2 with:

 – The fibration for assertion logic given by p : Pred → Set.
 – The monad is the natural-number writer monad (W, η, µ) on Set where
   W X = X × N.
 – The strong N-graded lifting Ẇ is given by Ẇ n(X, P ) = (W X, {(x, m) ∈
   W X | x ∈ P, m ≤ n})

The derived GHL structure is suitable for the GHL for simple cost analysis. To
complete the semantics of the GHL, we give the semantics of the tick command.
Semantics [[tick]] : ψ →
                       ˙ 1 1̇ in PredẆ of the tick command is defined by [[tick]](ξ) =
(∗, 1) for every ξ ∈ M, and we have the soundness of the axiom ⊢1 {ψ}do tick{ψ}
for every ψ.

     (GHL structure on Example 9)
Lemma 4. (1) the tuple (Set, 1, ×, SetC , I, ∗) induced by C forms a Freyd cat-
egory with coproduct; (2) the tuple (Pred, 1̇, ×, ˙ PredĊ , J, ⊛) induced by the
graded lifting Ċ forms an (N, max, 0, ≤)-graded Freyd category with homogeneous
coproduct; (3) they form a GHL structure.
                              Graded Hoare Logic and its Categorical Semantics                  39

Proof. (1) We need to show the equalities on J and ∗. From the counit law of
comonad, we have I(idX ) = idX and I(g ◦ f ) = Ig ◦ If . We also have:

idV ∗ idX = (idV × π1 ) ◦ hπ1 ◦ π1 , hπ2 ◦ π1 , π2 ii = hπ1 ◦ π1 , π2 ◦ π1 i = π1 = idV ∗X
(g ◦ f ) ∗ (i ◦ j) = (g ◦ f ) × (i ◦ hj, π2 i) ◦ hπ1 ◦ π1 , hπ2 ◦ π1 , π2 ii
      = (g × i) ◦ hf ◦ π1 ◦ π1 , hj, π2 i ◦ hπ2 ◦ π1 , π2 ii
      = (g × i) ◦ hf ◦ π1 ◦ π1 , hj ◦ hπ2 ◦ π1 , π2 i, π2 ii
      = (g × i) ◦ hπ1 ◦ (f × j) ◦ h π1 ◦ π1 , hπ2 ◦ π1 , π2 ii, hπ2 ◦ (f × j) ◦ h π1 ◦ π1 , hπ2 ◦ π1 , π2 ii, π2 ii
      = (g × i) ◦ h π1 ◦ π1 , hπ2 ◦ π1 , π2 ii ◦ h (f × j) ◦ h π1 ◦ π1 , hπ2 ◦ π1 , π2 ii, π2 i
      = (g ∗ i) ◦ (f ∗ j),
f ◦ I(lX ) = f ◦ hπ2 ◦ π1 , π2 i = π2 ◦ π1 ◦ h (id1 × f ) ◦ h π1 ◦ π1 , hπ2 ◦ π1 , π2 ii, π2 i = I(lX ) ◦ (id1 ∗ f ),
I(aX ′ ,Y ′ ,Z ′ ) ◦ ((f × g) ∗ h) = aX ′ ,Y ′ ,Z ′ ◦ (f × g) × h ◦ h π1 ◦ π1 , hπ2 ◦ π1 , π2 ii
      = aX ′ ,Y ′ ,Z ′ ◦ (f × g) × h ◦ aX×Y,Z,N = f × (g × h) ◦ (idX × aY,Z,N ) ◦ aX,Y ×Z,N ◦ (aX,Y,Z × idN )
     = (f ∗ (g ∗ h)) ◦ haX,Y,Z ◦ π1 , π2 i = (f ∗ (g ∗ h)) ◦ I(aX,Y,Z )
I(f × g) = (f × g) ◦ π1 = (f × g ◦ π1 ) ◦ hπ1 ◦ π1 , hπ2 ◦ π1 , π2 ii = f ∗ Ig
                                                                                `
      Next, we show the coproducts
                               `         in SetC . For coprojections ιi : Xi → i∈I Xi ,
we define I(ιi ) : CXi → ` i∈I Xi . For given fi : CX`      i → X (i ∈ I),`    we define
[fi ]∗i∈I = [fi ]i∈I ◦dist : C( i∈I Xi ) → X where dist : ( i∈I Xi )×N → i∈I (Xi ×
N) is the inverse of [hιi ◦ π1 , π2 i]i∈I . We show that I(ιi ) and [fi ]∗i∈I satisfy the
conditions of coprojections and cotuplings:

      [fi ]∗i∈I ◦ I(ιi ) = [fi ]i∈I ◦ dist ◦ (ιi × idN ) = [fi ]i∈I ◦ ιi = fi
      [I(ιi )]∗i∈I = [ιi × idN ]i∈I ◦ dist = id(`i∈I Xi )×N
      g ◦ [fi ]∗i∈I = g ◦ h[fi ]i∈I ◦ dist, π2 i = [g ◦ hfi , π2 i]i∈I ◦ dist = [g ◦ fi ]∗i∈I

Hence, (Set, 1, ×, SetC , I, ∗) is a Freyd category with products.
    (2) Since Ċ is a lifting of C, we inherit the structure of the Freyd category
with products (The mapping J and ⊛ are the same as I and ∗, as mappings of
arrows). We need to check that the gradings of J and ⊛ are well-defined, and
the mappings ⊑m≤n : Ċn → Ċm behave well.
    First, we check that we have I(f ) : Ċ0(X, P ) →          ˙ (Y, P ) for given f : (X, P ) →
(Y, Q). Let (x, m) in the predicate part of Ċ0(X, P ). We then have x ∈ P and
m ≥ 0. Since f : (X, P ) → (Y, Q), f (x) ∈ Q. Hence I(f )(x, m) = f ◦ π1 (x, m) =
f (x) ∈ Q. This implies I(f ) : Ċ0(X, P ) →       ˙ (Y, P ).
    Next, for all f : (X, P ) →    ˙ (X ′ , P ′ ) and g : Ċm(Y, Q) → (Y ′ , Q′ ), we have
f ∗ g : Ċm((X, P ) ×   ˙ (Y, Q)) →              ˙ (Y ′ , Q′ ). Let ((x, y), n) in the predicate
                                  ˙ (X ′ , P ′ ) ×
part of Ċm((X, P ) ×(Y, ˙    Q)), that is, x ∈ P , y ∈ Q and n ≥ m. Since f : (X, P ) →       ˙
(X ′ , P ′ ) and g : Ċm(Y, Q) → (Y ′ , Q′ ), we have f (x) ∈ P ′ and g(y, n) ∈ Q′ . Hence
(f ∗ g)((x, y), n) = (f (x), g(y, n)) ∈ P ′ × Q′ .
    We can inherit the conditions of coprojections and cotuplings on C to ones for
homogeneous coproducts, but we need to check`the gradings of coprojections and
cotuplings. It is easy to see that I(ιi ) : CXi → i∈I Xi forms I(ιi ) : Ċ0(Xi , Pi ) →
40      Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

˙
`
  i∈I (Xi , Pi ). Next, we show that when fi : Ċm(Xi , Pi ) → ˙ (X, P ) (i ∈ I), we
          ∗
                     `˙
have [fi ]i∈I : Ċm( i∈I (Xi , Pi )) →
                                     ˙ (X, P ). Let (x, n) in the predicate part of
Ċm( ˙ i∈I (Xi , Pi )). Then, n ≥ m and there is a unique i ∈ I such that x ∈ X
     `
and x ∈ Pi . Hence [fi ]∗i∈I (x, n) = fi (x, n) ∈ P .
    Finally, we check the`law of homogeneous          coproduct on ⊑m≤n : Ċn → Ċm.
                           ˙
We first have dist : Ċm( i∈I (Xi , Pi )) →
                                              `˙
                                            ˙ i∈I Ċm(Xi , Pi ). To show this, we need
to check
                                      ȧ                    ȧ
            [hιi ◦ π1 , π2 i]−1
                             i∈I (Ċm(       (Xi , Pi )) ⊆ (           Ċm(Xi , Pi )).
                                       i∈I                       i∈I
                 `
Let (x, n) ∈         i∈I (Xi × N) with x ∈ Xi . We have [hιi ◦ π1 , π2 i]i∈I (x, n) =
(ιi (x), n). If (ιi (x), n) ∈ Ċm( ˙ i∈I (Xi , Pi ), x ∈ Pi and n ≥ m. Then (x, n) ∈
                                  `
`˙                                              m≤n
                                                      = ˙ i∈I ⊑m≤n ◦dist. To show this,
                                                        `
   i∈I Cm(Xi , Pi ). Next, we show dist◦ ⊑
it suffices to check ⊑m≤n ◦[hιi ◦ π1 , π2 i] = [hιi ◦ π1 , π2 i] ◦ ˙ i∈I ⊑m≤n , but
                                                                     `
it is straightforward. Then we can check the remaining law of homogeneous
coproduct:
                                                                                         ȧ
[↑nm fi ]∗i∈I = [fi ◦ ⊑m≤n ]i∈I ◦dist = [fi ]i∈I ◦ ⊑m≤n ◦dist = [fi ]i∈I ◦dist◦                 ⊑m≤n =↑nm [fi ]∗i∈I
                                                                                          i∈I

                      ˙ PredĊ , J, ⊛) forms a Freyd category with homogeneous
Therefore, (Pred, 1̇, ×,
coproducts.
   (3) The functor q : PredĊ → SetC is defined by f 7→ pf . The ex falso
quodlibet is obvious. The rest of proof is straightforward.

Example 14 (A Program Logic for Differential Privacy). Program logics for rea-
soning about differential privacy can be seen as instantiations of GHL with a
relational model. For example, the continuous version of the logic apRHL by
Sato [Sat16] is based on the strong [0, ∞] × [0, ∞]-graded lifting G ⊤⊤ of G × G,
which is a graded extension of the codensity lifting given in [KSU18, Section
4.3.2]:

G ⊤⊤(ε,δ) (X, Y, R) = (G(X), G(Y ), {(µ1 , µ2 )|∀A ∈ ΣX , B ∈ ΣY . R(A) ⊆ B =⇒ µ1 (A) ≤ eε µ2 (B) + δ})
                      \            −1       ′    ′                   ′ ′
                                                                ˙ S ε ,δ , measurable, ε′ , δ ′ ∈ [0, ∞]}
                    = {(f ♯ × g ♯ ) (S ε+ε ,δ+δ )|f : (X, Y, R) →
                         where S ε,δ = ([0, 1], [0, 1], {(r, s)|r ≤ eε s + δ})

along the fibration rMeas : BRel(Meas) → Meas × Meas for assertion logic
defined by the following change-of-base

                             BRel(Meas)                 / BRel
                                   ❴✤
                              r Meas                         r
                                      (|−|,|−|)     
                            Meas × Meas        / Set × Set
                             Graded Hoare Logic and its Categorical Semantics              41

Thus, we have a GHL structure corresponding the semantic model of continuous
apRHL:
                                          (J,⊛)
                  BRel(Meas)                        / BRel(Meas)G ⊤⊤

                    r Meas                                        q
                                          (I,∗)            
                  Meas × Meas                      / Meas × MeasG×G

   We can introduce distributions as procedures, e.g. PExp ::= Gauss(eµ , eσ ) |
Laplace(eµ , eλ ) | · · · , and give the following partial definition of Cp corresponding
the [rand] rule in [Sat16]:

           Cp (φ, (ε, δ), xh1i = yh2i) = {p|[[p]] : [[φ]] →
                                                          ˙ (ε,δ) [[xh1i = yh2i]]}

Example 15 (Span-apRHL for Relaxations of Differential Privacy). GHL allows
the flexibility of separating the model of logical assertions from the one of
judgments. We demonstrate this flexibility by instantiating it to capture span-
apRHL [SBG+ 19], a variant of the continuous apRHL useful to formally reason
about relaxations of differential privacy. In this logic, assertions are modeled
as binary relation, while judgments are modeled as morphism between spans,
which are richer than just relations. The semantic models of span-apRHL given
in [SBG+ 19] can be regarded the following GHL structure.

                                                          ˆˆ
                        / Span(Meas)|BRel(Meas) (J,⊛) / Span(Meas)
 BRel(Meas)
                    K                                                          (−)♯(−,−)∆ |BRel(Meas)

         r Meas                          p̂|Span(Meas)|BRel(Meas) q=q̂|Span(Meas)(−)♯(−,−)∆ |BRel(Meas)
                                                                               
Meas × Meas                   / Meas × Meas                             / Meas × MeasG×G
                                                          (I,∗)


Here, rMeas : BRel(Meas) → Meas × Meas is a fibration for assertion logic;
Span(Meas) is the category of measurable spans (X ← R → Y ); p̂ : Span(Meas) →
Meas × Meas is a functor sending (X ← R → Y ) to the underlying spaces
(X, Y ); (−)♯(−,−)∆ is an approximate span-lifting for an M -graded family ∆ =
{∆m }m∈M of reflexive composable divergences. The approximate span-lifting is
a strong M × R-graded lifting of the product monad G × G along p̂, where G is
the subprobabilistic variant of the Giry monad [Gir82].
     The functor K : BRel(Meas) → Span(Meas) embeds binary relations (X, Y, R)
to measurable spans (X ← R → Y ) where R is regarded as the subspace of
X × Y . This functor preserves products and coproducts strictly. The codomain
of K can be restricted to the image Span(Meas)|BRel(Meas) , the subcategory
whose objects are restricted to binary relations embedded by K.
     The M × R-graded category Span(Meas)(−)♯(−,−)∆ |BRel(Meas) is the restric-
tion of the Kleisli graded category Span(Meas)(−)♯(−,−)∆ of approximate span-
lifting whose objects are restricted to binary relations embedded by K.
     The Freyd category (I, ∗) with product is induced from the structure of
strong monad G ×G. The M ×R-graded Freyd category (J, ⊛) with homogeneous
42       Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Tetsuya Sato

coproducts is given by composing the embedding K and the M ×R-graded (J,        ˆ ⊛)
                                                                                  ˆ
with homogeneous coproduct induced by the structure of M × R-graded monad
(−)♯(−,−)∆ on Span(Meas). Namely, we define J = Jˆ◦ K and f ⊛ g = (Kf )⊛g.       ˆ
It is straightforward to check the conditions of the GHL structure.
    By instantiating GHL with this GHL structure, we obtain a part of span-
apRHL for a divergence ∆. We can introduce distributions as procedures, e.g.
PExp ::= Gauss(eµ , eσ ) | Laplace(eµ , eλ ) | · · · , and give the following partial
definition of Cp as follows (f is called witness function):

Cp (φ, (m, δ), ψ) = {p|∃f s.t. ([[p]], f ) ∈ (Span(Meas)(−)♯(−,−)∆ |BRel(Meas) )([[φ]], [[ψ]])(m, δ)}.


References for the Appendix
Gir82.   Michèle Giry. A categorical approach to probability theory. In B. Ba-
         naschewski, editor, Categorical Aspects of Topology and Analysis, pages 68–
         85, Berlin, Heidelberg, 1982. Springer Berlin Heidelberg.
GSS92. Jean-Yves Girard, Andre Scedrov, and Philip J Scott. Bounded linear logic:
         a modular approach to polynomial-time computability. Theoretical computer
         science, 97(1):1–66, 1992.
Jac99.   Bart Jacobs. Categorical Logic and Type Theory. Elsevier, 1999.
KSU18. Shin-ya Katsumata, Tetsuya Sato, and Tarmo Uustalu. Codensity lifting of
         monads and its dual. Logical Methods in Computer Science, 14(4), 2018.
Sat16.   Tetsuya Sato. Approximate Relational Hoare Logic for Continuous Ran-
         dom Samplings. In Lars Birkedal, editor, The Thirty-second Conference
         on the Mathematical Foundations of Programming Semantics, MFPS 2016,
         Carnegie Mellon University, Pittsburgh, PA, USA, May 23-26, 2016, volume
         325 of Electronic Notes in Theoretical Computer Science, pages 277–298. El-
         sevier, 2016.
SBG+ 19. Tetsuya Sato, Gilles Barthe, Marco Gaboardi, Justin Hsu, and Shin-ya Kat-
         sumata. Approximate Span Liftings: Compositional Semantics for Relax-
         ations of Differential Privacy. In 34th Annual ACM/IEEE Symposium on
         Logic in Computer Science, LICS 2019, Vancouver, BC, Canada, June 24-
         27, 2019, pages 1–14, 2019.
