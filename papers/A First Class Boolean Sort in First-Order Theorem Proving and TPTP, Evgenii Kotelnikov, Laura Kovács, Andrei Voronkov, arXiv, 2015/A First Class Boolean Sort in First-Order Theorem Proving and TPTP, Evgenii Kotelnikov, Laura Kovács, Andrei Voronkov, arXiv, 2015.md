                                               A First Class Boolean Sort in First-Order
                                                     Theorem Proving and TPTP⋆

                                                 Evgenii Kotelnikov1, Laura Kovács1⋆⋆ , and Andrei Voronkov2⋆ ⋆ ⋆
arXiv:1505.01682v1 [cs.LO] 7 May 2015




                                                      1
                                                          Chalmers University of Technology, Gothenburg, Sweden
                                                           evgenyk@chalmers.se, laura.kovacs@chalmers.se
                                                            2
                                                              The University of Manchester, Manchester, UK
                                                                        andrei@voronkov.com



                                                Abstract. To support reasoning about properties of programs operating
                                                with boolean values one needs theorem provers to be able to natively deal
                                                with the boolean sort. This way, program properties can be translated to
                                                first-order logic and theorem provers can be used to prove program prop-
                                                erties efficiently. However, in the TPTP language, the input language of
                                                automated first-order theorem provers, the use of the boolean sort is
                                                limited compared to other sorts, thus hindering the use of first-order
                                                theorem provers in program analysis and verification. In this paper, we
                                                present an extension FOOL of many-sorted first-order logic, in which the
                                                boolean sort is treated as a first-class sort. Boolean terms are indistin-
                                                guishable from formulas and can appear as arguments to functions. In
                                                addition, FOOL contains if-then-else and let-in constructs. We define
                                                the syntax and semantics of FOOL and its model-preserving translation
                                                to first-order logic. We also introduce a new technique of dealing with
                                                boolean sorts in superposition-based theorem provers. Finally, we discuss
                                                how the TPTP language can be changed to support FOOL.


                                         1    Introduction
                                         Automated program analysis and verification requires discovering and proving
                                         program properties. Typical examples of such properties are loop invariants or
                                         Craig interpolants. These properties usually are expressed in combined theories
                                         of various data structures, such as integers and arrays, and hence require reason-
                                         ing with both theories and quantifiers. Recent approaches in interpolation and
                                         loop invariant generation [14,12,10] present initial results of using first-order the-
                                         orem provers for generating quantified program properties. First-order theorem
                                         provers can also be used to generate program properties with quantifier alter-
                                         nations [12]; such properties could not be generated fully automatically by any
                                         previously known method. Using first-order theorem prover to generate, and not
                                          ⋆
                                            The final publication is available at http://link.springer.com.
                                         ⋆⋆
                                            The first two authors were partially supported by the Wallenberg Academy Fellow-
                                            ship 2014, the Swedish VR grant D0497701, and the Austrian research project FWF
                                            S11409-N23.
                                        ⋆⋆⋆
                                            Partially supported by the EPSRC grant “Reasoning in Verification and Security”.
only prove program properties, opens new directions in analysis and verification
of real-life programs.
    First-order theorem provers, such as iProver [11], E [18], and Vampire [13],
lack however various features that are crucial for program analysis. For example,
first-order theorem provers do not yet efficiently handle (combinations of) theo-
ries; nevertheless, sound but incomplete theory axiomatisations can be used in a
first-order prover even for theories having no finite axiomatisation. Another dif-
ficulty in modelling properties arising in program analysis using theorem provers
is the gap between the semantics of expressions used in programming languages
and expressiveness of the logic used by the theorem prover. A similar gap exists
between the language used in presenting mathematics. For example, a standard
way to capture assignment in program analysis is to use a let-in expression,
which introduces a local binding of a variable, or a function for array assignments,
to a value. There is no local binding expression in first-order logic, which means
that any modelling of imperative programs using first-order theorem provers at
the backend, should implement a translation of let-in expressions. Similarly,
mathematicians commonly use local definitions within definitions and proofs.
Some functional programming languages also contain expressions introducing
local bindings. In all three cases, to facilitate the use of first-order provers, one
needs a theorem prover implementing let-in constructs natively.
    Efficiency of reasoning-based program analysis largely depends on how pro-
grams are translated into a collection of logical formulas capturing the program
semantics. The boolean structure of a program property that can be efficiently
treated by a theorem prover is however very sensitive to the architecture of the
reasoning engine of the prover. Deriving and expressing program properties in
the “right” format therefore requires solid knowledge about how theorem provers
work and are implemented — something that a user of a verification tool might
not have. Moreover, it can be hard to efficiently reason about certain classes of
program properties, unless special inference rules and heuristics are added to the
theorem prover, see e.g. [8] when it comes to prove properties of data collections
with extensionality axioms.
     In order to increase the expressiveness of program properties generated by
reasoning-based program analysis, the language of logical formulas accepted by
a theorem prover needs to be extended with constructs of programming lan-
guages. This way, a straightforward translation of programs into first-order logic
can be achieved, thus relieving users from designing translations which can be
efficiently treated by the theorem prover. One example of such an extension is
recently added to the TPTP language [19] of first-order theorem provers, resem-
bling if-then-else and let-in expressions that are common in programming
languages. Namely, special functions $ite_t and $ite_f can respectively be
used to express a conditional statement on the level of logical terms and for-
mulas, and $let_tt, $let_tf, $let_ff and $let ft can be used to express
local variable bindings for all four possible combinations of logical terms (t) and
formulas (f). While satisfiability modulo theory (SMT) solvers, such as Z3 [6]

                                         2
and CVC4 [2], integrate if-then-else and let-in expressions, in the first-order
theorem proving community so far only Vampire supports such expressions.
    To illustrate the advantage of using if-then-else and let-in expressions in
automated provers, let us consider the following simple example. We are inter-
ested in verifying the partial correctness of the code fragment below:
if (r(a)) {
  a := a + 1
} else {
  a := a + q(a)
}
using the pre-condition ((∀x)P (x) ⇒ x ≥ 0) ∧ ((∀x)q(x) > 0) ∧ P (a) and the
post-condition a > 0. Let a1 denote the value of the program variable a after the
execution of the if-statement. Using if-then-else and let-in expressions, the
next state function for a can naturally be expressed by the following formula:
a1 = if r(a) then let a = a + 1 in a
             else let a = a + q(a) in a
    This formula can further be encoded in TPTP, and hence used by a the-
orem prover as a hypothesis in proving partial correctness of the above code
snippet. We illustrate below the TPTP encoding of the first-order problem cor-
responding to the partial program correctness problem we consider. Note that
the pre-condition becomes a hypothesis in TPTP, whereas the proof obligation
given by the post-condition is a TPTP conjecture. All formulas below are typed
first-order formulas (tff) in TPTP that use the built-in integer sort ($int).
tff(1, type, p : $int > $o).
tff(2, type, q : $int > $int).
tff(3, type, r : $int > $o).
tff(4, type, a : $int).
tff(5, hypothesis, ! [X : $int] : (p(X) => $greatereq(X, 0))).
tff(6, hypothesis, ! [X : $int] : ($greatereq(q(X), 0))).
tff(7, hypothesis, p(a)).
tff(8, hypothesis,
    a1 = $ite_t(r(a), $let_tt(a, $sum(a, 1), a),
                      $let_tt(a, $sum(a, q(a)), a))).
tff(9, conjecture, $greater(a1, 0)).

    Running a theorem prover that supports $ite_t and $let_tt on this TPTP
problem would prove the partial correctness of the program we considered. Note
that without the use of if-then-else and let-in expressions, a more tedious
translation is needed for expressing the next state function of the program vari-
able a as a first-order formula. When considering more complex programs con-
taining multiple conditional expressions assignments and composition, comput-
ing the next state function of a program variable results in a formula of size
exponential in the number of conditional expressions. This problem of comput-
ing the next state function of variables is well-known in the program analysis
community, by computing so-called static single assignment (SSA) forms. Using

                                       3
the if-then-else and let-in expressions recently introduced in TPTP and al-
ready implemented in Vampire [7], one can have a linear-size translation instead.
     Let us however note that the usage of conditional expressions in TPTP is
somewhat limited. The first argument of $ite_t and $ite_f is a logical formula,
which means that a boolean condition from the program definition should be
translated as such. At the same time, the same condition can be treated as a
value in the program, for example, in a form of a boolean flag, passed as an
argument to a function. Yet we cannot mix terms and formulas in the same way
in a logical statement. A possible solution would be to map the boolean type of
programs to a user-defined boolean sort, postulate axioms about its semantics,
and manually convert boolean terms into formulas where needed. This approach,
however, suffers the disadvantages mentioned earlier, namely the need to design
a special translation and its possible inefficiency.
     Handling boolean terms as formulas is needed not only in applications of
reasoning-based program analysis, but also in various problems of formalisation
of mathematics. For example, if one looks at two largest kinds of attempts to for-
malise mathematics and proofs: those performed by interactive proof assistants,
such as Isabelle [16], and the Mizar project [21], one can see that first-order the-
orem provers are the main workhorses behind computer proofs in both cases –
see e.g. [5,22]. Interactive theorem provers, such as Isabelle routinely use quan-
tifiers over booleans. Let us illustrate this by the following examples, chosen
among 490 properties about (co)algebraic datatypes, featuring quantifiers over
booleans, generated by Isabelle and kindly found for us by Jasmin Blanchette.
Consider the distributivity of a conditional expression (denoted by the ite func-
tion) over logical connectives, a pattern that is widely used in reasoning about
properties of data structures. For lists and the contains function that checks
that its second argument contains the first one, we have the following example:
               (∀p : bool)(∀l : listA )(∀x : A)(∀y : A)
                                             .
                contains(l, ite(p, x, y)) =                                            (1)
                    (p ⇒ contains(l, x)) ∧ (¬p ⇒ contains(l, y))
    A more complex example with a heavy use of booleans is the unsatisfiability of
the definition of subset_sorted. The subset_sorted function takes two sorted
lists and checks that its second argument is a sublist of the first one.
  (∀l1 : listA )(∀l2 : listA )(∀p : Bool)
                                 .
   ¬(subset sorted(l1 , l2 ) = p ∧
                           .           .
      (∀l2′ : listA )¬(l1 = nil ∧ l2 = l2′ ∧ p) ∧
                                     .                    .
      (∀x1 : A)(∀l1′ : listA )¬(l1 = cons(x1 , l1′ ) ∧ l2 = nil ∧ ¬p) ∧
      (∀x1 : A)(∀l1′ : listA )(∀x2 : A)(∀l2′ : listA )                                 (2)
             .                     .
       ¬(l1 = cons(x1 , l1′ ) ∧ l2 = cons(x2 , l2′ ) ∧
             .
         p = ite(x1 < x2 , false,
                                     .
                              ite(x1 = x2 , subset sorted(l1′ , l2′ ),
                                            subset sorted(cons(x1 , l1′ ), l2′ )))))

                                            4
    Formulas with boolean terms are also common in the SMT-LIB project [3],
the collection of benchmarks for SMT-solvers. Its core logic is a variant of first-
order logic that treats boolean terms as formulas, in which logical connectives
and conditional expressions are defined in the core theory.
    In this paper we propose a modification FOOL of first-order logic, which in-
cludes a first-class boolean sort and if-then-else and let-in expressions, aimed
for being used in automated first-order theorem proving. It is the smallest logic
that contains both the SMT-LIB core theory and the monomorphic first-order
subset of TPTP. The syntax and semantics of the logic are given in Section 2. We
further describe how FOOL can be translated to the ordinary many-sorted first-
order logic in Section 3. Section 4 discusses superposition-based theorem proving
and proposes a new way of dealing with the boolean sort in it. In Section 5 we
discuss the support of the boolean sort in TPTP and propose changes to it re-
quired to support a first-class boolean sort. We point out that such changes can
also partially simplify the syntax of TPTP. Section 6 discusses related work and
Section 7 contains concluding remarks.
    The main contributions of this paper are the following:

 1. the definition of FOOL and its semantics;
 2. a translation from FOOL to first-order logic, which can be used to support
    FOOL in existing first-order theorem provers;
 3. a new technique of dealing with the boolean sort in superposition theorem
    provers, allowing one to replace boolean sort axioms by special rules;
 4. a proposal of a change to the TPTP language, intended to support FOOL
    and also simplify if-then-else and let-in expressions.


2     First-Order Logic with Boolean Sort

First-order logic with the boolean sort (FOOL) extends many-sorted first-order
logic (FOL) in two ways:

 1. formulas can be treated as terms of the built-in boolean sort; and
 2. one can use if-then-else and let-in expressions defined below.

FOOL is the smallest logic containing both the SMT-LIB core theory and the
monomorphic first-order part of the TPTP language. It extends the SMT-LIB
core theory by adding let-in expressions defining functions and TPTP by the
first-class boolean sort.


2.1   Syntax

We assume a countable infinite set of variables.

Definition 1. A signature of first-order logic with the boolean sort is a triple
Σ = (S, F, η), where:

                                        5
 1. S is a set of sorts, which contains a special sort bool. A type is either a sort
    or a non-empty sequence σ1 , . . . , σn , σ of sorts, written as σ1 × . . . × σn → σ.
    When n = 0, we will simply write σ instead of → σ. We call a type assignment
    a mapping from a set of variables and function symbols to types, which maps
    variables to sorts.
 2. F is a set of function symbols. We require F to contain binary function
    symbols ∨, ∧, ⇒ and ⇔, used in infix form, a unary function symbol ¬,
    used in prefix form, and nullary function symbols true, false.
 3. η is a type assignment which maps each function symbol f into a type τ .
    When the signature is clear from the context, we will write f : τ instead of
    η(f ) = τ and say that f is of the type τ .
    We require the symbols ∨, ∧, ⇒, ⇔ to be of the type bool × bool → bool, ¬
    to be of the type bool → bool and true, false to be of the type bool.              ❏

In the sequel we assume that Σ = (S, F, η) is an arbitrary but fixed signature.
    To define the semantics FOOL, we will have to extend the signature and also
assign sorts to variables. Given a type assignment η, we define η, x : σ to be
the type assignment that maps a variable x to σ and coincides otherwise with
η. Likewise, we define η, f : τ to be the type assignment that maps a function
symbol f to τ and coincides otherwise with η.
    Our next aim to define the set of terms and their sorts with respect to a type
assignment η. This will be done using a relation η ⊢ t : σ, where σ ∈ S, terms
can then be defined as all such expressions t.

Definition 2. The relation η ⊢ t : σ, where t is an expression and σ ∈ S is
defined inductively as follows. If η ⊢ t : σ, then we will say that t is a term of
the sort σ w.r.t. η.
 1. If η(x) = σ, then η ⊢ x : σ.
 2. If η(f ) = σ1 × . . . × σn → σ, η ⊢ t1 : σ1 , . . . , η ⊢ tn : σn , then η ⊢
    f (t1 , . . . , tn ) : σ.
 3. If η ⊢ φ : bool, η ⊢ t1 : σ and η ⊢ t2 : σ, then η ⊢ (if φ then t1 else t2 ) : σ.
 4. Let f be a function symbol and x1 , . . . , xn pairwise distinct variables. If
    η, x1 : σ1 , . . . , xn : σn ⊢ s : σ and η, f : (σ1 × . . . × σn → σ) ⊢ t : τ , then
    η ⊢ (let f (x1 : σ1 , . . . , xn : σn ) = s in t) : τ .
                                                 .
 5. If η ⊢ s : σ and η ⊢ t : σ, then η ⊢ (s = t) : bool.
 6. If η, x : σ ⊢ φ : bool, then η ⊢ (∀x : σ)φ : bool and η ⊢ (∃x : σ)φ : bool.        ❏

We only defined a let-in expression for a single function symbol. It is not hard
to extend it to a let-in expression that binds multiple pairwise distinct function
symbols in parallel, the details of such an extension are straightforward.
    When η is the type assignment function of Σ and η ⊢ t : σ, we will say that t
is a Σ-term of the sort σ, or simply that t is a term of the sort σ. It is not hard
to argue that every Σ-term has a unique sort.
    According to our definition, not every term-like expression has a sort. For
example, if x is a variable and η is not defined on x, then x is a not a term
w.r.t. η. To make the relation between term-like expressions and terms clear,

                                           6
we introduce a notion of free and bound occurrences of variables and function
symbols. We call the following occurrences of variables and function symbols
bound:

 1. any occurrence of x in (∀x : σ)φ or in (∃x : σ)φ;
 2. in the term let f (x1 : σ1 , . . . , xn : σn ) = s in t any occurrence of a variable
    xi in f (x1 : σ1 , . . . , xn : σn ) or in s, where i = 1, . . . , n.
 3. in the term let f (x1 : σ1 , . . . , xn : σn ) = s in t any occurrence of the
    function symbol f in f (x1 : σ1 , . . . , xn : σn ) or in t.

All other occurrences are called free. We say that a variable or a function symbol
is free in a term t if it has at least one free occurrence in t. A term is called closed
if it has no occurrences of free variables.

Theorem 1. Suppose η ⊢ t : σ. Then
 1. for every free variable x of t, η is defined on x;
 2. for every free function symbol f of t, η is defined on f ;
 3. if x is a variable not free in t, and σ ′ is an arbitrary sort, then η, x : σ ′ ⊢ t : σ;
 4. if f is a function symbol not free in t, and τ is an arbitrary type, then
    η, f : τ ⊢ t : σ.                                                                     ❏

Definition 3. A predicate symbol is any function symbol of the type σ1 × . . . ×
σn → bool. A Σ-formula is a Σ-term of the sort bool. All Σ-terms that are not
Σ-formulas are called non-boolean terms.                                       ❏

   Note that, in addition to the use of let-in and if-then-else, FOOL is a
proper extension of first-order logic. For example, in FOOL formulas can be used
as arguments to terms and one can quantify over booleans. As a consequence,
every quantified boolean formula is a formula in FOOL.

2.2   Semantics
As usual, the semantics of FOOL is defined by introducing a notion of interpre-
tation and defining how a term is evaluated in an interpretation.

Definition 4. Let η be a type assignment. A η-interpretation I is a map, defined
as follows. Instead of I(e) we will write J e KI , for every element e in the domain
of I.
 1. Each sort σ ∈ S is mapped to a nonempty domain J σ KI . We require J bool KI =
    {0, 1}.
 2. If η ⊢ x : σ, then J x KI ∈ J σ KI .
 3. If η(f ) = σ1 ×. . .×σn → σ, then J f KI is a function from J σ1 KI ×. . .×J σn KI
    to J σ KI .
 4. We require J true KI = 1 and J false KI = 0. We require J ∧ KI , J ∨ KI , J ⇒ KI ,
    J ⇔ KI and J ¬ KI respectively to be the logical conjunction, disjunction, im-
    plication, equivalence and negation, defined over {0, 1} in the standard way.


                                             7
   Given a η-interpretation I and a function symbol f , we define Ifg to be the
mapping that maps f to g and coincides otherwise with I. Likewise, for a variable
x and value a we define Ixa to be the mapping that maps x to a and coincides
otherwise with I.

Definition 5. Let I be a η-interpretation, and η ⊢ t : σ. The value of t in I,
denoted as evalI (t), is a value in J σ KI inductively defined as follows:


                                                evalI (x) = J x KI .
                                evalI (f (t1 , . . . , tn )) = J f KI (evalI (t1 ), . . . , evalI (tn )).
                                                               (
                                                                  evalI (s), if evalI (φ) = 1;
                     evalI (if φ then s else t) =
                                                                  evalI (t), otherwise.
  evalI (let f (x1 : σ1 , . . . , xn : σn ) = s in t) = evalIfg (t),

where g is such that for all i = 1, . . . , n and ai ∈ J σi KI , we have g(a1 , . . . , an ) =
evalIxa1...x
        ...an (s).
             n
      1

                                                (
                                     .              1, if evalI (s) = evalI (t);
                            evalI (s = t) =
                                            0, otherwise.
                                          
                                           1, if evalIx (φ) = 1
                                                      a


                      evalI ((∀x : σ)φ) =         for all a ∈ I(σ);
                                          
                                           0, otherwise.
                                          

                                           1, if evalIx (φ) = 1
                                                      a


                      evalI ((∃x : σ)φ) =         for some a ∈ I(σ);
                                          
                                            0, otherwise.
                                          


Theorem 2. Let η ⊢ φ : bool and I be a η-interpretation. Then

 1. for every free variable x of φ, I is defined on x;
 2. for every free function symbol f of φ, I is defined on f ;
 3. if x is a variable not free in φ, σ is an arbitrary sort, and a ∈ J σ KI then
    evalI (φ) = evalIxa (φ);
 4. if f is a function symbol not free in φ, σ1 , . . . , σn , σ are arbitrary sorts and
    g ∈ J σ1 KI × . . . × J σn KI → J σ KI , then evalI (φ) = evalIfg (φ).             ❏

    Let η ⊢ φ : bool. A η-interpretation I is called a model of φ, denoted by
I |= φ, if evalI (φ) = 1. If I |= φ, we also say that I satisfies φ. We say that φ is
valid, if I |= φ for all η-interpretations I, and satisfiable, if I |= φ for at least one
η-interpretation I. Note that Theorem 2 implies that any interpretation, which
coincides with I on free variables and free function symbols of φ is also a model
of φ.

                                                     8
3    Translation of FOOL to FOL

FOOL is a modification of FOL. Every FOL formula is syntactically a FOOL
formula and has the same models, but not the other way around. In this section
we present a translation from FOOL to FOL, which preserves models of φ.
This translation can be used for proving theorems of FOOL using a first-order
theorem prover. We do not claim that this translation is efficient – more research
is required on designing translations friendly for first-order theorem provers.
    We do not formally define many-sorted FOL with equality here, since FOL
is essentially a subset of FOOL, which we will discuss now.
    We say that an occurrence of a subterm s of the sort bool in a term t is in
a formula context if it is an argument of a logical connective or the occurrence
in either (∀x : σ)s or (∃x : σ)s. We say that an occurrence of s in t is in a term
context if this occurrence is an argument of a function symbol, different from a
logical connective, or an equality. We say that a formula of FOOL is syntactically
first order if it contains no if-then-else and let-in expressions, no variables
occurring in a formula context and no formulas occurring in a term context.
By restricting the definition of terms to the subset of syntactically first-order
formulas, we obtain the standard definition of many-sorted first-order logic, with
the only exception of having a distinguished boolean sort and constants true and
false occurring in a formula context.
    Let φ be a closed Σ-formula of FOOL. We will perform the following steps to
translate φ into a first-order formula. During the translation we will maintain a
set of formulas D, which initially is empty. The purpose of D is to collect a set of
formulas (definitions of new symbols), which guarantee that the transformation
preserves models.

 1. Make a sequence of translation steps obtaining a syntactically first order
    formula φ′ . During this translation we will introduce new function symbols
    and add their types to the type assignment η. We will also add formulas
    describing properties of these
                              V    symbols to D. The translation will guarantee
    that the formulas φ and ψ∈D ψ ∧ φ′ are equivalent, that is, have the same
    models restricted to Σ.
 2. Replace the constants true and false, standing in a formula context, by
    nullary predicates ⊤ and ⊥ respectively, obtaining a first-order formula.
 3. Add special boolean sort axioms.

During the translation, we will say that a function symbol or a variable is fresh
if it neither appears in φ nor in any of the definitions, nor in the domain of η.
     We also need the following definition. Let η ⊢ t : σ, and x be a variable
occurrence in t. The sort of this occurrence of x is defined as follows:

 1. any free occurrence of x in a subterm s in the scope of (∀x : σ ′ )s or (∃x : σ ′ )s
    has the sort σ ′ .
 2. any free occurrence of xi in a subterm s1 in the scope of
    let f (x1 : σ1 , . . . , xn : σn ) = s1 in s2 has the sort σi , where i = 1, . . . , n.

                                            9
 3. a free occurrence of x in t has the sort η(x).
If η ⊢ t : σ, s is a subterm of t and x a free variable in s, we say that x has a
sort σ ′ in s if its free occurrences in s have this sort.
    The translation steps are defined below. We start with an empty set D and an
initial FOOL formula φ, which we would like to change into a syntactically first-
order formula. At every translation step we will select a formula χ, which is either
φ or a formula in D, which is not syntactically first-order, replace a subterm in
χ it by another subterm, and maybe add a formula to D. The translation steps
can be applied in any order.
                                                                                            .
 1. Replace a boolean variable x occurring in a formula context, by x = true.
 2. Suppose that ψ is a formula occurring in a term context such that (i) ψ is
     different from true and false, (ii) ψ is not a variable, and (iii) ψ contains no
     free occurrences of function symbols bound in χ. Let x1 , . . . , xn be all free
     variables of ψ and σ1 , . . . , σn be their sorts. Take a fresh function symbol g,
                                                                                        .
     add the formula (∀x1 : σ1 ) . . . (∀xn : σn )(ψ ⇔ g(x1 , . . . , xn ) = true) to D
     and replace ψ by g(x1 , . . . , xn ). Finally, change η to η, g : σ1 ×. . .×σn → bool.
 3. Suppose that if ψ then s else t is a term containing no free occurrences
     of function symbols bound in χ. Let x1 , . . . , xn be all free variables of this
     term and σ1 , . . . , σn be their sorts. Take a fresh function symbol g, add
                                                                                    .
     the formulas (∀x1 : σ1 ) . . . (∀xn : σn )(ψ ⇒ g(x1 , . . . , xn ) = s) and (∀x1 :
                                                              .
     σ1 ) . . . (∀xn : σn )(¬ψ ⇒ g(x1 , . . . , xn ) = t) to D and replace this term by
     g(x1 , . . . , xn ). Finally, change η to η, g : σ1 × . . . × σn → σ0 , where σ0 is such
     that η, x1 : σ1 , . . . , xn : σn ⊢ s : σ0 .
 4. Suppose that let f (x1 : σ1 , . . . , xn : σn ) = s in t is a term containing no
     free occurrences of function symbols bound in χ. Let y1 , . . . , ym be all free
     variables of this term and τ1 , . . . , τm be their sorts. Note that the variables
     in x1 , . . . , xn are not necessarily disjoint from the variables in y1 , . . . , ym .
     Take a fresh function symbol g and fresh sequence of variables z1 , . . . , zn . Let
     the term s′ be obtained from s by replacing all free occurrences of x1 , . . . , xn
     by z1 , . . . , zn , respectively. Add the formula (∀z1 : σ1 ) . . . (∀zn : σn )(∀y1 :
                                                                  .
     τ1 ) . . . (∀ym : τm )(g(z1 , . . . , zn , y1 , . . . , ym ) = s′ ) to D. Let the term t′ be
     obtained from t by replacing all bound occurrences of y1 , . . . , ym by fresh
     variables and each application f (t1 , . . . , tn ) of a free occurrence of f in t by
     g(t1 , . . . , tn , y1 , . . . , ym ). Then replace let f (x1 : σ1 , . . . , xn : σn ) = s in t
     by t′ . Finally, change η to η, g : σ1 × . . . × σn × τ1 × . . . × τm → σ0 , where σ0
     is such that η, x1 : σ1 , . . . , xn : σn , y1 : τ1 , . . . , ym : τm ⊢ s : σ0 .
The translation terminates when none of the above rules apply.
   We will now formulate several of properties of this translation, which will
imply that, in a way, it preserves models. These properties are not hard to
prove, we do not include proofs in this paper.
Lemma 1. Suppose that a single step of the translation changes a formula φ1
into φ2 , δ is the formula added at this step (for step 1 we can assume true = true
is added), η is the type assignment before this step and η ′ is the type assignment
after. Then for every η ′ -interpretation I we have I |= δ ⇒ (φ1 ⇔ φ2 ).         ❏

                                                10
   By repeated applications of this lemma we obtain the following result.
Lemma 2. Suppose that the translation above changes a formula φ into φ′ ,
D is the set of definitions obtained during the translation, η is the initial type
assignment and η ′ is the final type
                                 V assignment of the  translation. Let I ′ be any
                   ′         ′
interpretation of η . Then I |= ψ∈D ψ ⇒ (φ ⇔ φ ).  ′
                                                                                ❏
   We also need the following result.
Lemma 3. Any sequence of applications of the translation rules terminates. ❏
    The lemmas proved so far imply that the translation terminates and the
final formula is equivalent to the initial formula in every interpretation satisfying
all definitions in D. To prove model preservation, we also need to prove some
properties of the introduced definitions.
Lemma 4. Suppose that one of the steps 2–4 of the translation translates a
formula φ1 into φ2 , δ is the formula added at this step, η is the type assignment
before this step, η ′ is the type assignment after, and g is the fresh function
symbol introduced at this step. Let also I be η-interpretation. Then there exists
a function h such that Igh |= δ.                                                ❏
   These properties imply the following result on model preservation.
Theorem 3. Suppose that the translation above translates a formula φ into φ′ ,
D is the set of definitions obtained during the translation, η is the initial type
assignment and η ′ is the final type assignment of the translation.
                                                        ′                  ′
  1. Let I be any η-interpretation. Then V there is ′a η -interpretation I such that
      ′                              ′
     I is an extension of I and I |= ψ∈D V        ψ∧φ.
  2. Let I ′ be a η ′ -interpretation and I ′ |= ψ∈D ψ ∧ φ′ . Then I ′ |= φ.      ❏
                                      V
This theorem implies that φ and ψ∈D ψ ∧φ′ have the same models, as far as the
original
V         type assignment (the type assignment of Σ) is concerned. The formula
              ′
   ψ∈D ψ ∧ φ in this theorem is syntactically first-order. Denote this formula by
γ. Our next step is to define a model-preserving translation from syntactically
first-order formulas to first-order formulas.
     To make γ into a first-order formula, we should get rid of true and false
occurring in a formula context. To preserve the semantics, we should also add
axioms for the boolean sort, since in first-order logic all sorts are uninterpreted,
while in FOOL the interpretations of the boolean sort and constants true and
false are fixed.
     To fix the problem, we will add axioms expressing that the boolean sort has
two elements and that true and false represent the two distinct elements of this
sort.
                                   .            .             .
                   ∀(x : bool)(x = true ∨ x = false) ∧ true =6 false.            (3)
Note that this formula is a tautology in FOOL, but not in FOL.
    Given a syntactically first-order formula γ, we denote by fol(γ) the formula
obtained from γ by replacing all occurrences of true and false in a formula
context by logical constants ⊤ and ⊥ (interpreted as always true and always
false), respectively and adding formula (3).

                                         11
Theorem 4. Let η is a type assignment and γ be a syntactically first-order
formula such that η ⊢ γ : bool.

 1. Suppose that I is a η-interpretation and I |= γ in FOOL. Then I |= fol(γ)
    in first-order logic.
 2. Suppose that I is a η-interpretation and I |= fol(γ) in first-order logic.
    Consider the FOOL-interpretation I ′ that is obtained from I by changing
    the interpretation of the boolean sort bool by {0, 1} and the interpretations
    of true and false by the elements 1 and 0, respectively, of this sort. Then
    I ′ |= γ in FOOL.                                                          ❏

    Theorems 3 and 4 show that our translation preserves models. Every model
of the original formula can be extended to a model of the translated formulas
by adding values of the function symbols introduced during the translation.
Likewise, any first-order model of the translated formula becomes a model of
the original formula after changing the interpretation of the boolean sort to
coincide with its interpretation in FOOL.


4   Superposition for FOOL

In Section 3 we presented a model-preserving syntactic translation of FOOL
to FOL. Based on this translation, automated reasoning about FOOL formulas
can be done by translating a FOOL formula into a FOL formula, and using an
automated first-order theorem prover on the resulting FOL formula. State-of-
the-art first-order theorem provers, such as Vampire [13], E [18] and Spass [23],
implement superposition calculus for proving first-order formulas. Naturally, we
would like to have a translation exploiting such provers in an efficient manner.
    Note however that our translation adds the two-element domain axiom ∀(x :
         .           .
bool)(x = true ∨ x = false) for the boolean sort. This axioms will be converted
to the clause
                                 .          .
                              x = true ∨ x = false,                           (4)
where x is a boolean variable. In this section we explain why this axiom requires
a special treatment and propose a solution to overcome problems caused by its
presence.
    We assume some basic understanding of first-order theorem proving and su-
perposition calculus, see, e.g. [1,15]. We fix a superposition inference system for
first-order logic with equality, parametrised by a simplification ordering ≻ on
literals and a well-behaved literal selection function [13], that is a function that
guarantees completeness of the calculus. We denote selected literals by underlin-
ing them. We assume that equality literals are treated by a dedicated inference
rule, namely, the ordered paramodulation rule [17]:
                      .
                    l =r∨C         L[s] ∨ D
                                                if θ = mgu(l, s),
                        (L[r] ∨ C ∨ D)θ


                                        12
where C, D are clauses, L is a literal, l, r, s are terms, mgu(l, s) is a most general
unifier of l and s, and rθ 6 lθ. The notation L[s] denotes that s is a subterm of
L, then L[r] denotes the result of replacement of s by r.
    Suppose now that we use an off-the-shelf superposition theorem prover to
reason about FOL formulas obtained by our translation. W.l.o.g, we assume that
true ≻ false in the term ordering used by the prover. Then self-paramodulation
(from true to true) can be applied to clause (4) as follows:
                      .            .                 .          .
                    x = true ∨ x = false           y = true ∨ y = false
                                .        .              .
                             x = y ∨ x = false ∨ y = false
                        .        .             .
The derived clause x = y ∨ x = f alse ∨ y = false is a recipe for disaster, since the
           .
literal x = y must be selected and can be used for paramodulation into every
non-variable term of a boolean sort. Very soon the search space will contain many
clauses obtained as logical consequences of clause (4) and results of paramod-
ulation from variables applied to them. This will cause a rapid degradation of
performance of superposition-based provers.
    To get around this problem, we propose the following solution. First, we
will choose term orderings ≻ having the following properties: true ≻ false and
true and false are the smallest ground terms w.r.t. ≻. Consider now all ground
                                              .            .
instances of (4). They have the form s = true ∨ s = false, where s is a ground
term. When s is either true or false, this instance is a tautology, and hence
redundant. Therefore, we should only consider instances for which s ≻ true.
This prevents self-paramodulation of (4).
    Now the only possible inferences with (4) are inferences of the form
                               .            .
                            x = true ∨ x = false C[s] ,
                                                 .
                                  C[true] ∨ s = false

where s is a non-variable term of the sort bool. To implement this, we can remove
clause (4) and add as an extra inference rule to the superposition calculus the
following rule:
                                      C[s]          ,
                                            .
                              C[true] ∨ s = false
where s is a non-variable term of the sort bool.


5    TPTP support for FOOL
The typed monomorphic first-order formulas subset, called TFF0, of the TPTP
language [20], is a representation language for many-sorted first-order logic. It
contains if-then-else and let-in constructs (see below), which is useful for
applications, but is inconsistent in its treatment of the boolean sort. It has a
predefined atomic sort symbol $o denoting the boolean sort. However, unlike
all other sort symbols, $o can only be used to declare the return type of pred-
icate symbols. This means that one cannot define a function having a boolean
argument, use boolean variables or equality between booleans.

                                         13
    Such an inconsistent use of the boolean sort results in having two kinds of
if-then-else expressions and four kinds of let-in expressions. For example,
a FOOL-term let f (x1 : σ1 , . . . , xn : σn ) = s in t can be represented using
one of the four TPTP alternatives $let_tt, $let_tf, $let_ft and $let_ff,
depending on whether s and t are terms or formulas.
    Since the boolean type is second-class in TPTP, one cannot directly represent
formulas coming from program analysis and interactive theorem provers, such
as formulas (1) and (2) of Section 1.
    We propose to modify the TFF0 language of TPTP to coincide with FOOL.
It is not late to do so, since there is no general support for if-then-else and
let-in. To the best of our knowledge, Vampire is currently the only theorem
prover supporting full TFF0. Note that such a modification of TPTP would
make multiple forms of if-then-else and let-in redundant. It will also make
it possible to directly represent the SMT-LIB core theory.
    We note that our changes and modifications on TFF0 can also be applied to
the TFF1 language of TPTP [4]. TFF1 is a polymorphic extension of TFF0 and
its formalisation does not treat the boolean sort. Extending our work to TFF1
should not be hard but has to be done in detail.



6   Related work


Handling boolean terms as formulas is common in the SMT community. The
SMT-LIB project [3] defines its core logic as first-order logic extended with the
distinguished first-class boolean sort and the let-in expression used for local
bindings of variables. The core theory of SMT-LIB defines logical connectives
as boolean functions and the ad-hoc polymorphic if-then-else (ite) function,
used for conditional expressions. The language FOOL defined here extends the
SMT-LIB core language with local function definitions, using let-in expressions
defining functions of arbitrary, and not just zero, arity. This, FOOL contains both
this language and the TFF0 subset of TPTP. Further, we present a translation
of FOOL to FOL and show how one can improve superposition theorem provers
to reason with the boolean sort.
    Efficient superposition theorem proving in finite domains, such as the boolean
domain, is also discussed in [9]. The approach of [9] sometimes falls back to enu-
merating instances of a clause by instantiating finite domain variables with all
elements of the corresponding domains. We point out here that for the boolean
(i.e., two-element) domain there is a simpler solution. However, the approach
of [9] also allows one to handle domains with more than two elements. One can
also generalise our approach to arbitrary finite domains by using binary encod-
ings of finite domains, however, this will necessarily result in loss of efficiency,
since a single variable over a domain with 2k elements will become k variables
in our approach, and similarly for function arguments.

                                        14
7   Conclusion
We defined first-order logic with the first class boolean sort (FOOL). It extends
ordinary many-sorted first-order logic (FOL) with (i) the boolean sort such that
terms of this sort are indistinguishable from formulas and (ii) if-then-else and
let-in expressions. The semantics of let-in expressions in FOOL is essentially
their semantics in functional programming languages, when they are not used
for recursive definitions. In particular, non-recursive local functions can be de-
fined and function symbols can be bound to a different sort in nested let-in
expressions.
    We argued that these extensions are useful in reasoning about problems com-
ing from program analysis and interactive theorem proving. The extraction of
properties from certain program definitions (especially in functional program-
ming languages) into FOOL formulas is more straightforward than into ordinary
FOL formulas and potentially more efficient. In a similar way, a more straight-
forward translation of certain higher-order formulas into FOOL can facilitate
proof automation in interactive theorem provers.
    FOOL is a modification of FOL and reasoning in it reduces to reasoning
in FOL. We gave a translation of FOOL to FOL that can be used for proving
theorems in FOOL in a first-order theorem prover. We further discussed a mod-
ification of superposition calculus that can reason efficiently in presence of the
boolean sort. Finally, we pointed out that the TPTP language can be changed
to support FOOL, which will also simplify some parts of the TPTP syntax.
    Implementation of theorem proving support for FOOL, including its superpo-
sition-friendly translation to CNF, is an important task for future work. Further,
we are also interested in extending FOOL with theories, such as the theory of
integer linear arithmetic and arrays.


References
 1. Bachmair, L., Ganzinger, H.: Resolution Theorem Proving. In: Handbook of Au-
    tomated Reasoning, pp. 19–99. Elsevier and MIT Press (2001)
 2. Barrett, C., Conway, C.L., Deters, M., Hadarean, L., Jovanovic, D., King, T.,
    Reynolds, A., Tinelli, C.: CVC4. In: Proc. of CAV. pp. 171–177 (2011)
 3. Barrett, C., Stump, A., Tinelli, C.: The SMT-LIB Standard: Version 2.0. Tech.
    rep., Department of Computer Science, The University of Iowa (2010), available
    at www.SMT-LIB.org
 4. Blanchette, J.C., Paskevich, A.: TFF1: The TPTP Typed First-Order Form with
    Rank-1 Polymorphism. In: Proc. of CADE-24. pp. 414–420. Springer (2013)
 5. Böhme, S., Nipkow, T.: Sledgehammer: Judgement Day. In: Proc. of IJCAR. pp.
    107–121 (2010)
 6. de Moura, L., Bjørner, N.: Z3: An Efficient SMT Solver. In: Proc. of TACAS. pp.
    337–340 (2008)
 7. Dragan, I., Kovács, L.: Lingva: Generating and Proving Program Properties Using
    Symbol Elimination. In: Proc. of PSI. pp. 67–75 (2014)
 8. Gupta, A., Kovács, L., Kragl, B., Voronkov, A.: Extensionality Crisis and Proving
    Identity. In: Proc. of ATVA. pp. 185–200 (2014)


                                         15
 9. Hillenbrand, T., Weidenbach, C.: Superposition for Bounded Domains. In: Auto-
    mated Reasoning and Mathematics - Essays in Memory of William W. McCune.
    pp. 68–100 (2013)
10. Hoder, K., Kovács, L., Voronkov, A.: Playing in the grey area of proofs. In: Proc.
    of POPL. pp. 259–272 (2012)
11. Korovin, K.: iProver - An Instantiation-Based Theorem Prover for First-Order
    Logic (System Description). In: Proc. of IJCAR. pp. 292–298 (2008)
12. Kovács, L., Voronkov, A.: Finding Loop Invariants for Programs over Arrays Using
    a Theorem Prover. In: Proc. of FASE. pp. 470–485 (2009)
13. Kovács, L., Voronkov, A.: First-Order Theorem Proving and Vampire. In: Proc. of
    CAV. pp. 1–35 (2013)
14. McMillan, K.L.: Quantified Invariant Generation Using an Interpolating Saturation
    Prover. In: Proc. of TACAS. pp. 413–427 (2008)
15. Nieuwenhuis, R., Rubio, A.: Paramodulation-Based Theorem Proving. In: Robin-
    son, A., Voronkov, A. (eds.) Handbook of Automated Reasoning, vol. I, chap. 7,
    pp. 371–443. Elsevier Science (2001)
16. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL - A Proof Assistant for
    Higher-Order Logic (2002)
17. Robinson, G., Wos, L.: Paramodulation and theorem-proving in first-order theories
    with equality. Machine intelligence 4, 135–150 (1969)
18. Schulz, S.: System Description: E 1.8. In: Proc. of LPAR. pp. 735–743 (2013)
19. Sutcliffe, G.: The TPTP Problem Library and Associated Infrastructure. J. Autom.
    Reasoning 43(4), 337–362 (2009)
20. Sutcliffe, G., Schulz, S., Claessen, K., Baumgartner, P.: The TPTP Typed First-
    Order Form with Arithmetic. In: Proc. of LPAR. pp. 406–419. Springer (2012)
21. Trybulec, A.: Mizar. In: The Seventeen Provers of the World, Foreword by Dana
    S. Scott. pp. 20–23 (2006)
22. Urban, J., Hoder, K., Voronkov, A.: Evaluation of Automated Theorem Proving
    on the Mizar Mathematical Library. In: ICMS. pp. 155–166 (2010)
23. Weidenbach, C., Dimova, D., Fietzke, A., Kumar, R., Suda, M., Wischnewski, P.:
    Spass version 3.5. In: CADE. pp. 140–145 (2009)




                                          16
