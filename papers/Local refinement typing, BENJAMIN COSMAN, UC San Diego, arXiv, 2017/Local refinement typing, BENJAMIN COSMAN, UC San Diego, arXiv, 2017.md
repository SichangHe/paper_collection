                                         Local Refinement Typing

                                         BENJAMIN COSMAN, UC San Diego
                                         RANJIT JHALA, UC San Diego
                                                                                                                                                                        26
arXiv:1706.08007v1 [cs.PL] 24 Jun 2017




                                         We introduce the Fusion algorithm for local refinement type inference, yielding a new SMT-based method
                                         for verifying programs with polymorphic data types and higher-order functions. Fusion is concise as the
                                         programmer need only write signatures for (externally exported) top-level functions and places with cyclic
                                         (recursive) dependencies, after which Fusion can predictably synthesize the most precise refinement types for
                                         all intermediate terms (expressible in the decidable refinement logic), thereby checking the program without
                                         false alarms. We have implemented Fusion and evaluated it on the benchmarks from the LiqidHaskell
                                         suite totalling about 12KLOC. Fusion checks an existing safety benchmark suite using about half as many
                                         templates as previously required and nearly 2× faster. In a new set of theorem proving benchmarks Fusion
                                         is both 10 − 50× faster and, by synthesizing the most precise types, avoids false alarms to make verification
                                         possible.
                                         Additional Key Words and Phrases: Refinement Types, Program Logics, SMT, Verification
                                         ACM Reference format:
                                         Benjamin Cosman and Ranjit Jhala. 2017. Local Refinement Typing. Proc. ACM Program. Lang. 1, 1, Article 26
                                         (September 2017), 31 pages.
                                         https://doi.org/10.1145/3110270


                                         1   INTRODUCTION
                                         Refinement types are a generalization of Floyd-Hoare logics to the higher-order setting. Assertions
                                         are generalized to types by constraining basic types so that their inhabitants satisfy predicates
                                         drawn from SMT-decidable refinement logics. Assertion checking can then be generalized to a
                                         form of subtyping, where subtyping for basic types reduces to checking implications between
                                         their refinement predicates [Constable 1986; Rushby et al. 1998]. Thus, thanks to the SMT revolu-
                                         tion [Barrett et al. 2016], refinement types have emerged as a modular and programmer-extensible
                                         means of expressing and verifying properties of polymorphic, higher order programs in languages
                                         like ML [Dunfield 2007; Rondon et al. 2008; Xi and Pfenning 1998], Haskell [Vazou et al. 2014b],
                                         Racket [Kent et al. 2016], F ♯ [Bengtson et al. 2008], and TypeScript [Vekris et al. 2016].
                                         The Problem Unfortunately, the expressiveness and extensibility offered by predicate refinements
                                         comes at a price. Existing refinement type systems are either not concise, i.e. require many type
                                         annotations (not just for top-level functions), or not complete, i.e. programs fail to type check
                                         because the checker cannot synthesize suitable types for intermediate terms, or not terminating,
                                         i.e. the checker can diverge while trying to synthesize suitable types for intermediate terms in an
                                         iterative counterexample-guided manner. We show that the presence of logical predicates relating
                                         multiple program variables renders classical approaches like unification or set-constraint based
                                         subtyping – even when used in a bidirectional [Pierce and Turner 1998] or local fashion [Odersky
                                         Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and
                                         the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses,
                                         contact the owner/author(s).
                                         © 2017 Copyright held by the owner/author(s).
                                         2475-1421/2017/9-ART26
                                         https://doi.org/10.1145/3110270


                                                                            Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:2                                                                        Benjamin Cosman and Ranjit Jhala

et al. 2001] – not up to the task of inference. The problem is especially acute for programs that
make ubiquitous use of polymorphic datatypes and higher-order combinators. Consequently, to
use refinement types, the programmer must accept one of several distasteful choices: litter her code
with type annotations (everywhere), or eschew polymorphic combinators (§ 2).
Fusion: Local Refinement Typing In this paper, we introduce the Fusion algorithm that permits
local refinement type inference. Fusion is concise as the programmer need only write signatures
for (externally exported) top-level functions, and places with cyclic dependencies on refinements,
either explicit (e.g. recursive functions) or implicit (e.g. calls to inductive library functions like
fold). Fusion then synthesizes the most precise refinement types for all intermediate terms that
are expressible in the refinement logic, and hence checks the specified signatures. Finally, Fusion
ensures that verification remains decidable by using the framework of Liquid Typing [Rondon et al.
2008] to synthesize refinements from user-defined templates (“qualifiers”) in the presence of cyclic
dependencies. Fusion reconciles concision, precision and decidability with three contributions.
    (1) From Programs to NNF Horn Constraints Our first insight is that we can phrase the
        problem of refinement type checking as that of checking the satisfiability of (nested) Horn
        Clause Constraints in Negation Normal Form (NNF). The NNF constraints are implications
        between refinement variables denoting the unknown, to-be-synthesized refinements; a sat-
        isfying assignment for these constraints yields refinement types for all intermediate terms,
        that satisfy the subtyping obligations that must hold for the program to meet its specification.
        Crucially, our novel NNF constraint formulation retains the scoping structure of bindings that
        makes precise constraint solving practical (§ 4).
    (2) Solving Constraints via Elimination Our second insight is that we can find a satisfying
        assignment for the NNF constraint, by systematically computing the most precise assignment
        for each refinement variable, and using it to eliminate the variable from the constraints.
        Unfortunately, we find that a direct application of the elimination algorithm, inspired by
        the classical notion of “unfolding” from the Logic Programming literature [Burstall and
        Darlington 1977; Tamaki and Sato 1984], leads to an exponential blowup even for simple
        programs that arise in practice. We show that such a blowup cannot be avoided in general
        as the problem of refinement type checking is ExpTime-hard. Fortunately, we show how
        to exploit the scoping structure present in NNF constraints to get compact solutions for
        real-world programs (§ 5).
    (3) Refinement Typing: Faster and without False Alarms We have implemented Fusion
        and evaluated its effectiveness on all the benchmarks from the LiqidHaskell suite [Vazou
        et al. 2014b]. We show that in existing safety benchmarks where qualifiers were supplied or
        extracted from top-level type signatures, Fusion is able to synthesize the types about 2× faster
        and requires only about half the qualifiers (needed e.g. to synthesize types for non-top-level
        recursive functions). Further, in a new set of theorem proving benchmarks which make heavy
        use of polymorphic higher-order functions and data types, global template-based inference
        of LiqidHaskell is both prohibitively slow and unpredictable, failing with false alarms. In
        contrast, Fusion is more than 10× faster and, by synthesizing the most precise types, makes
        verification possible (§ 6).

2    OVERVIEW
We start with a high-level overview illustrating how refinement types can be used to verify programs,
the problems that refinements pose for local inference, and our techniques for addressing them.
We have picked obviously contrived examples that distill the problem down to its essence: for
real-world programs we refer the reader to [Swamy et al. 2011; Vazou et al. 2014a].

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                              26:3

inc      ::   x : Int -> { v : Int | v = x + 1}                  --    increment by one
dec      ::   x : Int -> { v : Int | v = x - 1}                  --    decrement by one
[]       ::   List a                                             --    list : " nil "
(:)      ::   a -> List a -> List a                              --    list : " cons "
last     ::   List a -> a                                        --    last element of a list
map      ::   ( a -> b ) -> List a -> List b                     --    mapping over a list
(.)      ::   ( b -> c ) -> ( a -> b ) -> a -> c                 --    function composition


                             Fig. 1. Type specifications for library functions


Refinement Types We can precisely describe subsets of values corresponding to a type by compos-
ing basic types with logical predicates that are satisfied by values inhabiting the type. For example,
Nat describes the subset of Int comprising (non-negative) natural numbers:
      type Nat = { v : Int | 0 <= v }

Verification Conditions A refinement type checker can use the above signature to check:
      abs :: Int -> Nat
      abs n | 0 <= n    = n
            | otherwise = 0 - n
by generating a verification condition (VC) [Nelson 1981]:
                                ∀n. 0 ≤ n ⇒ ∀ν . ν = n            ⇒0≤ν
                                  ∧ 0 ≰ n ⇒ ∀ν . ν = 0 − n ⇒ 0 ≤ ν
whose validity can be checked by an SMT solver [Barrett et al. 2016; Nelson 1981] to ensure that
the program meets the given specification.

2.1    The Problem
For simple, first-order programs like abs, VC generation is analogous to the classical Floyd-Hoare
approach used e.g. by EscJava [Flanagan et al. 2002]. Namely, we have constraints assuming the
path conditions (and pre-conditions), and asserting the post-conditions. Next, we illustrate how VC
generation and checking is problematic in the presence of local variables, collections, and polymorphic,
higher order functions. We do so with a series of small but idiomatic examples comprising “straight-
line” code (no explicit looping or recursion), decorated with top-level specifications as required for
local type inference. We show how the presence of the above features necessitates the synthesis of
intermediate refinement types, which is beyond the scope of existing approaches.
Library Functions Our examples use a library of functions with types as shown in Fig. 1.
Example 1: Local Variables In ex1 in Figure 2, we illustrate the problem posed by local binders
that lack (refinement) type signatures. Here, we need to check that inc y is a Nat i.e. non-negative,
assuming the input x is. To do so, we must synthesize a sufficiently strong type for the local binder
y which says that its value is an almost-Nat, i.e. that y has the type {y : Int | 0 ≤ y + 1}.
Example 2: Collections In ex2 in Figure 2 we show how the idiom of creating intermediate
collections of values complicates refinement type checking. Here, we use a Nat to create a list ys
whose last element is extracted and incremented, yielding a Nat. The challenge is to infer that the
intermediate collection ys is a list of almost-Nats.

                             Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:4                                                                        Benjamin Cosman and Ranjit Jhala

Example 3: Higher Order Functions Function ex3 shows the idiom of composing two functions
with the (.) operator whose type is in Figure 1. To verify the type specification for ex3 we need
to synthesize suitable instantiations for the type variables a, b and c. Unlike with classical types,
unification is insufficient, as while a and c may be instantiated to Nat, we need to infer that b must
be instantiated with almost-Nat.
Example 4: Iteration Finally ex4 shows how the higher-order map and (.) are used to idiomati-
cally refactor transformations of collections in a “wholemeal” style [Hinze 2009]. This straight-line
function (treating map as a library function, abstracted by its type signature) vexes existing refine-
ment type systems [Knowles and Flanagan 2010; Swamy et al. 2011] that cannot infer that map dec
(resp. map inc) transforms a Nat list (resp. almost-Nat list) into an almost-Nat list (resp. Nat list).

2.2    Existing Approaches
Existing tools use one of three approaches, each of which is stymied by programs like the above.
1. Existentials First, [Kent et al. 2016; Knowles and Flanagan 2009] shows how to use existentials
to hide the types of local binders. In ex1, this yields
                                       y :: ∃0 ≤ t. {ν : Int | ν = t − 1}
As inc y has the type {ν | ν = y + 1} we get the VC:
                          ∀y. (∃t. 0 ≤ t ∧ y = t − 1) ⇒ ∀ν . ν = y + 1 ⇒ 0 ≤ ν
which is proved valid by an SMT solver. Sage [Knowles and Flanagan 2010], F* [Swamy et al. 2011]
and Racket [Kent et al. 2016] use this method to check ex1. However, it is not known how to
scale this method beyond local variable hiding, i.e. to account for collections, lambdas, higher-order
functions etc.. Consequently, the above systems fail to check ex2, ex3 and ex4.
2. Counterexample-Guided Refinement Second, as in Mochi [Unno et al. 2013] we can use
counterexample-guided abstraction-refinement (CEGAR) to iteratively compute stronger refinements
until the property is verified. This approach has two drawbacks. First, it is non-modular in that it
requires closed programs – e.g. the source of library functions like map and (.) – in order to get
counterexamples. Second, more importantly, it is limited to logical fragments like linear arithmetic
where Craig Interpolation based “predicate discovery” is predictable, and is notoriously prone to
divergence otherwise [Jhala and McMillan 2006]. Consequently, the method has only been applied
to small but tricky programs comprising tens of lines, but not scaled to large real-world libraries
spanning thousands of lines, and which typically require refinements over uninterpreted function
symbols or modular arithmetic [Vazou et al. 2014a].
3. Abstract Interpretation Finally, the framework of Liquid Typing [Rondon et al. 2008] shows
how to synthesize suitable refinement types via abstract interpretation. The key idea is to:
   (1) Represent types as templates that use κ variables to represent unknown refinements.
   (2) Generate subtyping constraints over the templates, that reduce to implications between the
       κ variables,
   (3) Solve the implications over an abstract domain, e.g. the lattice of formulas generated by
       conjunctions of user-supplied atomic predicates, to find an assignment for the κ-variables
       that satisfies the constraints.
   Unfortunately, this approach also has several limitations. First, the user must supply atomic
predicates (or more generally, a suitable abstract domain) which should be superfluous in “straight
line” code as in ex1, ex2, ex3, and ex4. Unfortunately, without the atomic predicate hints, Liquid
Typing fails to check any of the above examples. Specifically, unless the user provides the qualifier
or template 0 ≤ v + 1 (which does not appear anywhere in the code or specifications), the system

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                              26:5

           ex1 :: Nat -> Nat                   ex2 :: Nat -> Nat
           ex1 x =                             ex2 x =
             let y =                             let ys = let n = dec x
                let t = x                                     p = inc x
                in                                            xs = n : []
                   dec t                                  in p : xs
             in                                       y = last ys
                inc y                            in
           ∧                                        inc y


                        Fig. 2. Examples: (ex1) Local variables, (ex2) Collections



cannot synthesise the almost-Nat types for the various intermediate terms in the above examples.
Consequently LiqidHaskell (which implements Liquid Typing) rejects safe (and checkable)
programs, leaving the user with the unpleasant task of debugging false alarms. Second, in predicate
abstraction, the so-called abstraction operator “α” makes many expensive SMT queries, which can
slow down verification, or render it impossible when the specifications, and hence predicates, are
complicated (§ 6).

2.3   Our Solution: Refinement Fusion
Next, we describe our Fusion algorithm for local refinement typing and show how it allows us to
automatically, predictably and efficiently check refinement types in the presence of variable hiding,
collections, lambdas and polymorphic, higher order functions. The key insight is two-fold. First,
we present a novel reduction from type inference to the checking the satisfaction of a system of
NNF Horn Constraints (over refinement variables) that preserve the scoping structure of bindings
in the original source program. Second, we show how to check satisfaction of the NNF constraints
by exploiting the scoping structure to compute the strongest possible solutions for the refinement
variables. The above steps yield a method that is concise, i.e. requires no intermediate signatures,
and complete, i.e. is guaranteed to check a program whenever suitable signatures exist, instead of
failing with false alarms when suitable qualifiers are not provided. Finally, the method terminates,
as the acyclic variables can be eliminated (by replacing them with their most precise solution), after
which any remaining cyclic variables can be solved via abstract interpretation [Rondon et al. 2008].

   Example 1: Local Variables. First, let us see how Fusion synthesizes types for local binders that
lack (refinement) type signatures.
1. Templates Fusion starts by generating templates for terms whose type must be synthesized.
From the input type of ex1 (Fig 2), the fact that t is bound to x, and the output type of dec we have:

                                          x :: {ν : Int | 0 ≤ ν }
                                          t :: {ν : Int | ν = x}
                                    dec t :: {ν : Int | ν = t − 1}

The term dec t is bound to y but as t goes out of scope we assign y a template

                                          y :: {ν : Int | κ(ν )}

                             Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:6                                                                        Benjamin Cosman and Ranjit Jhala

with a fresh κ denoting the (unknown) refinement for the expression. That is, y is a Int value ν
that satisfies κ(ν ). We will constrain κ to be a well-scoped super-type of its body dec t. Finally,
the output of ex1 gets assigned

                                          inc y :: {ν : Int | ν = y + 1}

2. Constraints Next, Fusion generates constraints between the various refinements. At each
application, the parameter must be a subtype of the input type; dually, in each function definition,
the body must be a subtype of the output type, and at each let-bind the body must be a subtype of
the whole let-in expression. For base types, subtyping is exactly implication between the refinement
formulas [Constable 1986; Rushby et al. 1998]. For ex1 we get two constraints. The first relates the
body of the let-in with its template; the second the body of ex1 with the specified output:

                             ∀x. 0 ≤ x ⇒                      ∀ν . ν = x − 1 ⇒ κ(ν )                     (1)
                                           ∧ ∀y. κ(y) ⇒ ∀ν . ν = y + 1 ⇒ 0 ≤ ν                           (2)

    Fusion ensures that the constraints preserve the scoping structure of bindings. Each subtyping
(i.e. implication) happens under a context where the program variables in scope are bound and
required to satisfy the refinements from their previously computed templates. Further, shared
binders are explicit in the NNF constraint. For example, in the NNF constraint above, the shared
binder x in the source program is also shared across the two implications 1 and 2. This sharing
crucially allows Fusion to compute the most precise solution.
3. Solution To solve the constraints we need to find a well-formed assignment mapping each
κ-variable to a predicate over variables in scope wherever the κ-variable appears, such that the
formula obtained by replacing the κ with its assignment is valid. If no such interpretation exists,
then the constraints are unsatisfiable and the program is ill-typed.
   Fusion computes an interpretation called the strongest refinements using a method inspired by
the classical notion of “unfolding” from the Logic Programming literature [Burstall and Darlington
1977; Tamaki and Sato 1984]. In essence, if we have implications of the form: Pi ⇒ κ(ν ) then we
can assign κ to the disjunction κ(x)  ∨i Pi after taking care to existentially quantify variables. In
our example, κ is a unary refinement predicate, and so we use (1) to obtain the assignment

                                κ(z)  ∃x . 0 ≤ x ∧ (∃ν . ν = x − 1 ∧ ν = z)                             (3)

which simplifies to 0 ≤ z + 1. The computed assignment above is simply the (existentially quantified)
hypotheses arising in the conjunction where κ(·) is the goal. The “simplification” done above and in
the sequel is purely for exposition: to compute it we would have to resort to quantifier elimination
procedures which are prohibitively expensive in practice, and hence avoided by Fusion.
   It is easy to check that the above assignment renders the constraint valid (post-substitution). In
particular, the solution (3) precisely captures the almost-Nat property which allows an SMT solver to
prove (2) valid. While the substituted VC contains existential quantifiers, the SMT solver can handle
the resulting validity query easily as the quantifiers appear negatively, i.e. in the antecedents of the
implication. Consequently, they can be removed by a simple variable renaming (“skolemization”)
as the VC (∃x .P(x)) ⇒ Q is equivalent to the VC P(z) ⇒ Q, where z is a fresh variable name.
   Thus, for local variables, Fusion synthesizes the same intermediate types as the existentials-
based method of [Kent et al. 2016; Knowles and Flanagan 2009], and, unlike Liquid Types, is able to
verify ex1 without requiring any predicate templates. However, as we see next, Fusion generalizes
the existentials based approach to handle collections, lambdas, and polymorphic, higher order
functions.

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                               26:7

  Example 2: Collections. Next, let us see how Fusion precisely synthesizes types for intermediate
collections without requiring user-defined qualifiers or annotations.
1. Templates From the output types of inc and dec we get

                                          n :: {ν : Int | ν = x − 1}
                                          p :: {ν : Int | ν = x + 1}

The lists xs and ys are created by invoking the nil and cons constructors (Fig 1.) In the two cases,
we respectively instantiate the polymorphic type variable a (in the constructors’ signatures from
Figure 1) with the (unknown) templates over fresh κ variables to get

                                        xs :: List {ν : Int | κ x (ν )}
                                        ys :: List {ν : Int | κy (ν )}

as the output of last has the same type its input list, we get:

                                          y :: {ν : Int | κy (ν )}
                                    inc y :: {ν : Int | ν = y + 1}


2. Constraints We get four implication constraints from ex2.

                                    ∀x. 0 ≤ x ⇒
                                      ∧ ∀n. n = x − 1 ⇒
                                             ∀p. p = x + 1 ⇒
                                                ∧ ∀ν . ν = n ⇒ κ x (ν)                                          (4)
                                                ∧ ∀ν . ν = p ⇒ κy (ν)                                           (5)
                                                ∧ ∀ν . κ x (ν) ⇒ κy (ν)                                         (6)
                                       ∧ ∀y. κy (y) ⇒
                                             ∀ν . ν = y + 1 ⇒ 0 ≤ ν                                             (7)

As n is passed into “cons” to get xs, we get that {ν | ν = n} must be a subtype of {ν | κ x (ν )}, yielding
(4). Similarly, as p is “cons”-ed to xs to get ys, we get that {ν | ν = p} and {ν | κ x (ν )} must be
subtypes of {ν | κy (ν)} yielding (5) and (6) respectively. Finally, the type of the return value y+1
must be a subtype of Nat yielding (7). Each implication appears under a context in which the
variables in scope are bound to satisfy their template’s refinement.
3. Solution Again, we compute the strongest refinements as the (existentially quantified) disjunc-
tions of the hypotheses under which each κ appears. Thus, implication (4) yields:

                          κ x (z)  ∃x. 0 ≤ x ∧
                                      ∃n. n = x − 1 ∧
                                         ∃p. p = x + 1 ∧
                                            ∃ν . ν = n ∧ ν = z          . . . from (4)


                              Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:8                                                                        Benjamin Cosman and Ranjit Jhala

    ex3 :: Nat -> Nat                                         ex4 :: List Nat -> List Nat
    ex3 = let fn = \ a -> dec a                               ex4 = let fn = \ a -> dec a
              fp = \ b -> inc b                                         fp = \ b -> inc b
          in fp . fn                                                in map fp . map fn


              Fig. 3. Examples: (ex3) Higher-Order Composition, (ex4) Higher-Order Iteration.


which is essentially 0 ≤ z + 1, or almost-Nat, and the disjunction of (5, 6) yields
                             κy (z)  ∃x. 0 ≤ x ∧
                                          ∃n. n = x − 1 ∧
                                             ∃p. p = x + 1 ∧
                                                 ∨ ∃ν . ν = p ∧ ν = z . . . from (5)
                                                 ∨ ∃ν . ν = n ∧ ν = z . . . from (6)
which is also 0 ≤ z + 1. Substituting the strongest refinements into (7) yields a valid formula,
verifying ex2.
   Example 3: Composition. Next, we describe how Fusion synthesizes precise types for inner
lambda-terms like those bound to fn and fp, and simultaneously determines how the polymorphic
type variables for the (.) combinator can be instantiated in order to verify ex3
1. Templates Fusion scales up to polymorphic higher-order operators like “compose” (.) by using
the same approach as for collections: create κ-variables for the unknown instantiated refinements,
and then find the strongest solution. In ex3, this process works by respectively instantiating the a,
b and c in the signature for (.) (Fig 1) with fresh templates {ν | κa (ν)}, {ν | κb (ν )}, and {ν | κc (ν )}
respectively. Consequently, the arguments and output to . at this instance get the templates:
                                      fn :: {a : Int | κa (a)} → {ν : Int | κb (ν )}                     (8)
                                      fp :: {b : Int | κb (b)} → {ν : Int | κc (ν )}                     (9)
                               fp . fn :: {a : Int | κa (a)} → {ν : Int | κc (ν )}

2. Constraints Next, the bodies of fn and fp must be subtypes of the above templates. By decom-
posing function subtyping into input- and output- subtyping, we get the following implications.
We omit the trivial constraints on the input types; the above correspond to checking the output
types in an environment assuming the stronger (super-) input type:
                                       ∀a. κa (a) ⇒ ∀ν . ν = a − 1 ⇒ κb (ν)                             (10)
                                  ∧ ∀b. κb (b) ⇒ ∀ν . ν = b + 1 ⇒ κc (ν)                                (11)
Finally, fp . fn must be a subtype of the (function) type ascribed to ex3 yielding input and output
constraints:
                                  ∧ ∀ν . 0 ≤ ν ⇒ κa (ν )                                                (12)
                                  ∧ ∀ν . κc (ν ) ⇒ 0 ≤ ν                                                (13)

3. Solution Finally Fusion computes the strongest refinements by assigning κa to its single
hypothesis:
                               κa (z)  ∃ν . 0 ≤ ν ∧ ν = z

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                              26:9

which simplifies to 0 ≤ z, which plugged into (10) gives:
                          κb (z)  ∃a. 0 ≤ a ∧ ∃ν . ν = a − 1 ∧ ν = z
which simplifies to 0 ≤ z + 1, which in (11) yields
                          κc (z)  ∃b. 0 ≤ b + 1 ∧ ∃ν . ν = b + 1 ∧ ν = z
which is just 0 ≤ z, rendering implication (13) valid.


   Example 4: Iteration. Finally, Fusion uses types to scale up to higher-order iterators over collec-
tions. As in ex3 we generate fresh templates for fn (8) and fp (9). When applied to map the above
return as output the templates:
                               map fn :: List {a | κa (a)} → List {ν | κb (ν)}
                               map fp :: List {b | κb (b)} → List {ν | κc (ν )}
which are the templates from ex3 lifted to lists, yielding
                    map fp . map fn :: List {a | κa (a)} → List {ν | κc (ν )}
  Consequently, the subtyping constraints for ex4 are the same as for ex3 but lifted to lists. Co-
variant list subtyping reduces those into the exact same set of implications as ex3. Thus, Fusion
computes the same strongest refinements as in ex3 and hence, verifies ex4.

2.4    Avoiding Exponential Blowup
The reader may be concerned that substituting the strongest solution may cause the formulas
to expand, leading to an exponential blowup. Recall that, in our examples, we “simplified” the
formulas before substituting to keep the exposition short. In general this is not possible as it
requires expensive quantifier elimination. We show that the concern is justified in theory, and that
a direct substitution strategy leads to a blowup even in practice. Fortunately, we show that a simple
optimization that uses the scoping structure of bindings that we have carefully preserved in the
NNF constraints allows us to avoid blowups in practice.
Local Refinement Typing is ExpTime-Hard The bad news is that local refinement typing in
general, and thus, constraint solving in particular are both ExpTime-hard. This result follows from
the result that reachability (i.e. safety) of non-recursive first order boolean programs is ExpTime-
complete [Godefroid and Yannakakis 2013]. We can encode the reachability problem directly as
checking a given refinement type signature over programs using just boolean valued data, and so
local refinement typing is ExpTime-hard. Thus, deciding constraint satisfaction is also ExpTime-
hard, which means that we cannot avoid exponential blowups in general. Propositional validity
queries are in Np so ExpTime-hardness means we must make an exponential number of queries, or
a polynomial number of exponential size queries.
Let-chains cause exponential blowup Indeed, the direct “unfolding” based approach [Burstall
and Darlington 1977; Tamaki and Sato 1984] that we have seen so far blows up due to a simple and
ubiquitous pattern: sequences of let-binders. Consider the constraint generated by the program:
      exp :: Nat -> Nat
      exp x0 = let x1 = id x0
                    ..
                     .
                    xn = id xn−1
                in xn

                             Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:10                                                                       Benjamin Cosman and Ranjit Jhala

The i t h invocation of id :: a -> a creates a fresh κi , which is then used as the template for xi .
Consequently, we get the NNF constraint:
      ∀x0 . 0 ≤ x0 ⇒ ∀ν . ν = x0 ⇒ κ 1 (ν )
                   ∧ ∀x1 . κ 1 (x1 ) ⇒ ∀ν . ν = x1 ⇒ κ 2 (ν )
                                     ..
                                      .
                                       ∧ ∀xn−1 . κn−1 (xn−1 ) ⇒ ∀ν . ν = xn−1 ⇒ κn (ν )
                                                              ∧ ∀xn . κn (xn ) ⇒ ∀ν . ν = xn ⇒ 0 ≤ ν
                                                                                                      (14)
Since each κi has in its hypotheses, all of κ 1 . . . κi−1 , the strongest solution for κi ends up with 2i
copies of 0 ≤ x 0 ! While this example is contrived, it represents an idiomatic pattern: long sequences
of let-binders (e.g. introduced by ANF-conversion) with polymorphic instantiation. Due to the
ubiquity of the pattern, a direct unfolding based computation of the strongest refinement fails for
all but the simplest programs.
Sharing makes Solutions Compact This story has a happy ending. Fortunately, our constraints
preserve the scoping structure of binders. Thus, the exponentially duplicated 0 ≤ x 0 is “in scope”
everywhere each κi appears. Consequently, we can omit it entirely from the strongest solutions,
collapsing each to the compact solution (15), κi (z)  z = x i−1 . In § 4 we formalize our algorithm
for generating such nested constraints, and in § 5 we show how to use the above insight to derive
an optimized solving algorithm, which yields compact, shared solutions and hence, dramatically
improves refinement type checking in practice § 6.
The Importance of Preserving Scope Note that the sharing observation and optimization seem
obvious at this juncture, precisely because of our novel NNF formulation which carefully preserves
the scoping structure of binders. Previous approaches for constraint based refinement synthesis
[Hashimoto and Unno 2015; Knowles and Flanagan 2007; Polikarpova et al. 2016; Rondon et al. 2008]
yield constraints that discard the scoping structure, yielding the flat (i.e. non-nested) constraints
     ∀x0,0 . 0 ≤ x0,0 ⇒ ∀ν . ν = x0,0 ⇒ κ 1 (ν)
 ∧ ∀x1,0 . 0 ≤ x1,0 ⇒ ∀x1,1 . κ 1 (x1,1 ) ⇒ ∀ν . ν = x1,1 ⇒ κ 2 (ν )
  ..
   .
 ∧ ∀xn−1,0 . 0 ≤ xn−1,0 ⇒ . . . ⇒ ∀xn−1,n−1 . κn−1 (xn−1,n−1 ) ⇒ ∀ν . ν = xn−1,n−1 ⇒ κn (ν )
 ∧ ∀xn,0 . 0 ≤ xn,0 ⇒ . . . ⇒ ∀xn,n−1 . κn−1 (xn,n−1 ) ⇒ ∀xn,n . κn (xn,n ) ⇒ ∀ν . ν = xn,n ⇒ 0 ≤ ν
in which the sharing is not explicit as the shared variables are alpha-renamed. Absent sharing,
unfolding yields a solution for each κi that is exponential in i without any syntactic duplication of
a common conjunct, rendering the computation of precise solutions infeasible.

2.5     Relatively Complete Local Refinement Typing
By fusing together the constraints appearing as hypotheses for each refinement variable κ, our
approach synthesizes the most precise refinements expressible in the decidable refinement logic
(Lemma 5.6), and hence, makes local refinement typing relatively complete. That is, (assuming no
recursion) if there exist type ascriptions for intermediate binders and terms that allow a program to
typecheck, then Fusion is guaranteed to find them. The above examples do in fact typecheck with
existing systems but only if the user annotated local variables with their signatures. For example,
[Swamy et al. 2011] can check ex2 (Figure 2) if the programmer annotates the type of the local xs
as an almost Nat. Unfortunately, such superfluous annotations impose significant overhead in code
size as well as effort: the user must painstakingly debug false alarms to find where information
was lost due to incompleteness. In contrast, our completeness guarantee means that once the user

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                            26:11

has annotated top-level and recursive binders, Fusion will not return false alarms due to missing
templates, i.e. will typecheck the program if and only if it can be, which crucially makes verification
concise, precise and decidable, enabling the results in § 6.
Precise Refinements vs. Pre- and Post-Conditions As discussed in § 7, our notion of most precise
refinements can be viewed as the analog of the method of strongest postconditions from Floyd-Hoare
style program logics. F* introduces the notion of Dijkstra Monads [Swamy et al. 2013] as a way to
generalize the dual notion of weakest preconditions (WP) to the higher-order setting. Hence, F*
can use the notion of Dijkstra Monads to verify the following variant of ex3 that uses Floyd-Hoare
style specification instead of refinement types:
    let inc x = x + 1
    let dec x = x - 1
    let compose f g x = f (g x)

    let ex3 : i : int -> Pure int
      ( requires (0 <= i)) ( ensures ( fun j -> 0 <= j))
      = compose inc dec

However, this approach has a key limitation relative to Fusion in that it requires an implementation
or logically equivalent strong specification of the compose operator (.), instead of the weaker
polymorphic type signature required by Fusion. The WP machinery crucially relies upon the
strong specification to makes the chaining of functions explicit. When the chaining is obscured, e.g.
by the use of map in ex4, the WP method is insufficient, and so F* fails to verify ex4. In contrast,
Fusion uses only the implicit subtyping dependencies between refinement types. Hence, the same
compositional, type-directed machinery that checks ex3 carries over to successfully verify ex4.

3     PROGRAMS
We start by formalizing the syntax and operational semantics of a core source language λ R [Knowles
and Flanagan 2010; Vazou et al. 2014b].

3.1    Syntax
Terms Figure 4 summarizes the syntax of the terms of λ R . The values of λ R comprise primitive
constants c and functions λx :τ .e. The terms of λ R include values and additionally, variables x, y, z
. . . , let-binders let x = e in e, applications e x (in ANF, to simplify the application rule [Rondon
et al. 2008]). Polymorphism is accounted for via type abstraction Λα .e and instantiation [e] τ . We
assume that the source program has been annotated with unrefined types at λ-abstractions and type
abstraction and instantiations, either by the programmer or via classical (unrefined) type inference.
Types The types of λ R include unrefined types, written τ , and refined types, written t. The unrefined
types include basic types like Int, Bool, type variables α, functions x :τ → τ ′ where the input is
bound to the name x, and type schemes ∀α .τ . We refine basic types with refinement predicates r to
get refined types. The formulas r are drawn from a decidable refinement logic, e.g. QF_UFLIA: the
quantifier free theory of linear arithmetic and uninterpreted functions.
Notation We write {ν | r } when the base b is clear from the context. We write b to abbreviate
{ν :b | true}, and write t → t ′ to abbreviate x :t → t ′ if x does not appear in t ′.
Typing Constants We assume that each constant c is equipped with a type prim(c) that charac-
terizes its semantics [Knowles and Flanagan 2010; Vazou et al. 2014b]. For example, literals are
assigned their corresponding singleton type and operators have types representing their pre- and

                             Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:12                                                                       Benjamin Cosman and Ranjit Jhala

                               Values v         ::= c                           constants
                                                   | λx :τ .e                   function
                                Terms      e    ::= v                           values
                                                   | x, y, z, . . .             variables
                                                   | let x = e in e ′           let-bind
                                                   | ex                         application
                                                   | Λα .e                      type-abstraction
                                                   | [e] τ                      type instantiation
                       Refinements         r    ::=   . . . varies . . .
                        Basic Types        b    ::=   Int | Bool | . . .
                                Types      t    ::= α                           variable
                                                   | {x :b | r }                base
                                                   | x :t → t                   function
                                                   | ∀α .t                      scheme
                  Unrefined Types          τ    ::= α                           variable
                                                   | b                          base
                                                   | x :τ → τ                   function
                                                   | ∀α .τ                      scheme

                                                 Fig. 4. Syntax of λ R




post-conditions:

                                   prim(7)  {ν : Int | ν = 7}
                                   prim(+)  x : Int → y : Int → {ν | ν = x + y}
                                   prim(/)  Int → {ν : Int | ν , 0} → Int
                           prim(assert)  {ν : Bool | ν } → Unit

3.2     Semantics
λ R has a standard small-step, contextual call-by-value semantics; we write e ,→ e ′ to denote that
term e steps to e ′. We write e ,→j e ′ if there exists e 1 , . . . , e j such that e ≡ e 1 , e ′ ≡ e j , and for all
1 ≤ i < j, we have ei ,→ ei+1 . We write e ,→∗ e ′ if for some (finite) j we have e ,→j e ′.

Constants We assume that when values are applied to a primitive constant, the expression is
reduced to the output of the primitive constant operation in a single step. For example, consider
+, the primitive Int addition operator. We assume that J+K(n) equals +n where for all m, J+n K(m)
equals the integer sum of n and m.

Safety We say a term e is stuck if there does not exist any e ′ such that e ,→ e ′. We say that a term
e is safe, if whenever e ,→∗ e ′ then either e ′ is a value or e ′ is not stuck. We write safe(e) to denote
that e is safe. Informally, we assume that the primitive operations (e.g. division) get stuck on values
that do not satisfy their input refinements (e.g. when the divisor is 0). Thus, e is safe when every
(primitive) operation is invoked with values on which it is defined (e.g. there are no divisions by 0.)

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                               26:13

Constraint Syntax                                                                                                  c
                                      Predicates       p   ::= r
                                                              | κ(y)
                                                              | p1 ∧ p2
                                     Constraints       c   ::= p
                                                              | c1 ∧ c2
                                                              | ∀x :b. p ⇒ c
                               Environments            Γ   ::=   ∅ | Γ; x :t
                                     Assignment        σ   ::= K → R
                                   Assumption G            ::= σ | G, {x :b | p}

Well-formedness                                                                                                Γ⊢c
                           W-Ref            W-And                W-Imp
                           Γ ⊢ r : Bool     Γ ⊢ c1     Γ ⊢ c2    Γ; x :b ⊢ c   Γ; x :b ⊢ r
                              Γ⊢r             Γ ⊢ c1 ∧ c2           Γ ⊢ ∀x :b. r ⇒ c

Satisfaction                                                                                                 G |= c
                Sat-Base                          Sat-Ext                  Sat-Many
                ∅ ⊢ σ (c) SmtValid(σ (c))         G |= ∀x :b. p ⇒ c        G |= c for each c ∈ cs
                            σ |= c                   G, {x :b | p} |= c            G |= cs

                                     Fig. 5. Constraints: Syntax and Semantics


4     CONSTRAINTS
Local refinement typing proceeds in two steps. First, we use λ R terms to generate a system of
constraints (§ 4.1) whose satisfiability (§ 4.2) implies that the term is safe (§ 4.4). Second, we solve
the constraints to find a satisfying assignment (§ 5).

4.1    Syntax
Refinement Variables Figure 5 describes the syntax of constraints. A refinement variable repre-
sents an unknown n-ary relation, i.e. is an unknown refinement over the free variables z 1 , . . . , zn
(abbreviated to z). We refer to z :τ as the parameters of a variable κ, written params(κ), and say
that n is the arity of κ. We write K for the set of all refinement variables.
Predicates A predicate is a refinement r from a decidable logic, or a refinement variable application
κ(x 1 , . . . , x n ), or a conjunction of two sub-predicates. We assume each κ is applied to the same
number of variables as its arity.
Constraints A constraint is a “tree” where each “leaf” is a goal and each “internal” node either (1)
universally quantifies some variable x of a basic type b, subjecting it to satisfy a hypothesis p, or (2)
conjoins two sub-constraints.
NNF Horn Clauses Our constraints are Horn Clauses in Negation Normal Form [Bjørner et al.
2015]. NNF constraints are a generalization of the “flat” Constraint Horn Clause (CHC) formulation
used in Liquid Typing [Rondon et al. 2008]. Intuitively, each root-to-leaf path in the tree is a CHC
that requires that the leaf’s goal be implied by the internal nodes’ hypotheses. The nesting structure
of NNF permits the scope-based optimization that makes Fusion practical (§ 5.1).

                                Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:14                                                                       Benjamin Cosman and Ranjit Jhala

4.2     Semantics
We describe the semantics of constraints by formalizing the notion of constraint satisfaction.
Intuitively, a constraint is satisfiable if there is an interpretation or assignment of the κ-variables to
concrete refinements r such that the resulting logical formula is well-formed and valid.
Well-formedness An environment Γ is a set of type bindings x :τ . We write Γ ⊢ c to denote that c is
well-formed under environment Γ. Figure 5 summarizes the rules for establishing well-formedness.
We write Γ ⊢ r : Bool if r can be typed as a Bool using the standard (non-refined) rules, and use
it to check individual refinements (W-Ref). A conjunction of sub-constraints is well-formed if
each conjunct is well-formed (W-And). Finally, each implication is well formed if the hypothesis is
well-formed and the consequent is well-formed under the extended environment (W-Imp). (Note
that a constraint containing a κ-application is not well-formed.)
Assignments An assignment σ is a map from the set of refinement variables K to the set of
refinements R. An assignment is partial if its range is predicates (containing κ-variables, not just
refinements). The function σ (·) substitutes κ-variables in predicates p, constraints c, and sets of
constraints C with their σ -assignments:
                         σ (κ(y))               σ (κ) [y/x] where x = params(κ)
                         σ (r )                 r
                         σ (p ∧ p ′)            σ (p) ∧ σ (p ′)
                         σ (∀x :b. p ⇒ c)       ∀x :b. σ (p) ⇒ σ (c)
                         σ (c 1 ∧ c 2 )         σ (c 1 ) ∧ σ (c 2 )
                         σ (C)                  {σ (c) | c ∈ C}
Satisfaction A verification condition (VC) is a constraint c that has no κ applications; i.e. kvars(c) =
∅. We say that an assignment σ satisfies constraint c, written σ |= c, if σ (c) is a VC that is: (a) well-
formed, and (b) logically valid [Nelson 1981]. Figure 5 formalizes the notion of satisfaction and lifts
it to sets of constraints. We say that c is satisfiable if some assignment σ satisfies c. The following
lemmas follow from the definition of satisfaction and validity:
   Lemma 4.1 (Weaken). If G |= p then G |= p ∨ p ′.
   Lemma 4.2 (Strengthen). If σ |= ∀x :b. p ⇒ c and σ |= ∀x :b. p ′ ⇒ p then σ |= ∀x :b. p ′ ⇒ c.
Composing Assignments For two assignments σ and σ ′ we write σ ·σ ′ to denote the assignment:
                                              (σ ·σ ′)(κ)  σ (σ ′(κ))
The following Lemmas, proved by induction on the structure of c, characterize the relationship
between assignment composition and satisfaction.
   Lemma 4.3 (Composition-Preserves-Sat). If σ |= c then σ ′ ·σ |= c.
   Lemma 4.4 (Composition-Validity). σ ·σ ′ |= c if and only if σ |= σ ′(c).

4.3     Dependencies and Decomposition
Next, we describe various properties of constraints that we will exploit to determine satisfiability.
Flat Constraints A flat or non-nested constraint c is of the form:
                                    ∀x 1 :b1 . p1 ⇒ . . . ⇒ ∀x n :bn . pn ⇒ p
By induction on the structure of c we can show that the procedure flat(c), shown in Figure 12,
returns a set of flat constraints that are satisfiable exactly when c is satisfiable.
   Lemma 4.5 (Flattening). σ |= c if and only if σ |= flat(c).

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                               26:15

Heads and Bodies Let c ≡ ∀x 1 :b1 . p1 ⇒ . . . ⇒ ∀x n :bn . pn ⇒ p be a flat constraint. We write
head(c) for the predicate p that is the right-most “consequent” of c. We write body(c) for the set of
predicates p1 , . . . , pn that are the “antecedents” of c.
Dependencies Let kvars(c) denote the the set of κ-variables in a constraint c. We can define the
following sets of dependencies:
                 deps(σ )  {(κ, κ ′) | κ ∈ σ (κ ′)}                                              (of a solution σ )
                  deps(c)  {(κ, κ ′) | κ ∈ body(c), κ ′ ∈ head(c)}                        (of a flat constraint c)
                  deps(c)  ∪c ′ ∈flat(c) deps(c ′)                                     (of an NNF constraint c)
              deps(K̂, c)  deps(c) \ (K × K̂ ∪ K̂ × K)                           (of a constraint excluding K̂)

We write deps∗ (c) (resp. deps∗ (K̂, c)) for the reflexive and transitive closure of deps(c) (resp.
deps(K̂, c)). Intuitively, the dependencies of a constraint comprise the set of pairs (κ, κ ′) where κ
appears in a body (hypothesis) for a clause where κ ′ is in the head (goal).
Cuts and Cycles A set of variables K̂ cuts c if the relation deps∗ (K̂, c) is acyclic. A set of variables
K ′ is acyclic in c if K − K ′ cuts c. Intuitively, a set K ′ is acyclic in c if the closure of dependencies
restricted to K ′ (i.e. excluding variables not in K ′) has no cycles. A single variable κ is acyclic in c if
{κ} is acyclic in c. Intuitively, a single variable κ is acyclic in c if there is no clause in c where κ
appears in both the head and the body. A constraint is acyclic if the set of all K is acyclic in c, i.e. if
deps∗ (c) is acyclic. In the sequel, for clarity of exposition we assume the invariant that whenever
relevant, κ is acyclic in c. (Of course, our algorithm maintains this property, as described in § 5.5.)
Definitions and Uses The definitions (resp. uses) of κ in c, written c ↓κ (resp. c ↑κ), are the subset
of flat(c) such that the head contains (resp. does not contain) κ:
                                 c ↓κ  {c ′ | c ′ ∈ flat(c), κ ∈ head(c ′)}                          (definitions)
                                 c ↑κ  {c | c ∈ flat(c), κ < head(c )}
                                             ′    ′                           ′
                                                                                                              (uses)
By induction on the structure of c we can check that:
  Lemma 4.6 (Flatten-Definitions). ∀x . p ⇒ c ↓κ ≡ (∀x . p ⇒ c)↓κ
  Since the definitions and uses of a κ partition flat(c), we can show that σ satisfies c if it satisfies
the definitions and uses of κ in c:
  Lemma 4.7 (Partition). If κ is acyclic in c then σ |= c if and only if σ |= c ↓κ and σ |= c ↑κ.

4.4   Generation
Next, we show how to map a term e into a constraint c whose satisfiability implies the safety of e.
Shapes (shape) Procedure shape, elided for brevity, takes as input a refined type t and returns as
output the non-refined version obtained by erasing the refinements from t.
Templates (fresh) Procedure fresh(Γ, τ ) (Figure 6) takes as input an environment and a non-refined
type τ , and returns a template whose shape is τ . Recall that each refinement variable denotes an
n-ary relation. For example, a refinement variable that appears in the output type of a function can
refer to the input parameter, i.e. can be a binary relation between the input and the output value.
We track the allowed parameters by using the environment Γ. In the base case, fresh generates a
fresh κ whose parameters correspond to the binders of Γ. In the function type case, fresh recursively
generates templates for the input and output refinements, extending the environment for the output
with the input binder.

                                Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:16                                                                            Benjamin Cosman and Ranjit Jhala


                               fresh                        :       (Γ × T ) → T̂
                               fresh([y1 :τ1 , . . .], b)          {ν :b | κ(y1 , . . . , ν )}
                                  where
                                    κ                       =       fresh K variable
                                    s.t. params(κ)          =       [z 1 :τ1 , . . . , z :b]
                               fresh(Γ, x :τ → τ ′)                x :t → t ′
                                  where
                                    t                       =       fresh(Γ, τ )
                                    t′                      =       fresh(Γ; x :τ , τ ′)
                               fresh(Γ, α)                         α
                               fresh(Γ, ∀α .τ )                    ∀α .fresh(Γ, τ )


Fig. 6. Fresh Templates: T̂ denotes templates, i.e. types with κ-variables representing unknown refinements.



                             sub                                :       (T × T ) → C
                             sub({x :b | p}, {y :b | q})               ∀x :b. p ⇒ q [x/y]
                             sub(x :s → s ′, y :t → t ′)         c ∧ ((y :: t) ⇒ c ′)
                                where
                                 c                              =       sub(t, s)
                                 c′                             =       sub(s ′ [y/x] , t ′)
                             sub(α, α)                                 true
                             sub(∀α .t, ∀α .t ′)                       sub(t, t ′)


                                           Fig. 7. Subtyping Constraints


Subtyping (sub) Procedure sub(t, t ′) (Figure 7) returns the constraint c that must be satisfied for
t to be a subtype of t ′, which intuitively means, the set of values denoted by t to be subsumed
by those denoted by t ′. (See [Knowles and Flanagan 2010; Vazou et al. 2014b] for details.) In the
base case, the sub-type’s predicate must imply the super-type’s predicate. In the function case, we
conjoin the contra-variant input constraint and the co-variant output constraint. For the latter, we
additionally add a hypothesis assuming the stronger input type, using a generalized implication that
drops binders with non-basic types as they are not supported by the first-order refinement logic:
                                (x :: {y :b | p}) ⇒ c        ∀x :b. p [x/y] ⇒ c
                                (x :: t) ⇒ c                 c

Generation (cgen) Finally, procedure cgen(Γ, e) (Figure 8) takes as input an environment Γ and
term e and returns as output a pair (c, t) where e typechecks if c holds, and has the (refinement)
template t. The procedure computes the template and constraint by a syntax-directed traversal of
the input term. The key idea is two-fold. First: generate a fresh template for each position where
the (refinement) types cannot be directly synthesized – namely, function inputs, let-binders, and

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                              26:17

polymorphic instantiation sites. Second: generate subtyping constraints at each position where
values flow from one position into another.
    • Constants and Variables yield the trivial constraint true, and templates corresponding to
      their primitive types, or environment bindings respectively. (The helper single strengthens
      the refinement to state the value equals the given variable, dubbed “selfification” by [Ou et al.
      2004], enabling path-sensitivity [Knowles and Flanagan 2010; Rondon et al. 2008].)
    • Let-binders (let x = e 1 in e 2 ) yield the conjunction of three sub-constraints. First, we
      get a constraint c 1 and template t 1 from e 1 . Second, we get a constraint c 2 and template t 2
      from e 2 checked under the environment extended with t 1 for x. Third, to hide x which may
      appear in t 2 , we generate a fresh template tˆ with the shape of t 2 and use sub to constrain t 2
      to be a subtype of tˆ. The well-formedness requirement ensures tˆ, which is returned as the
      expression’s template, is assigned a well-scoped refinement type.
    • Functions (λx :τ .e) yield a template where the input is assigned a fresh template of shape τ ,
      and the output is the template for e.
    • Applications (e y) yield the output template with the formal x substituted for the actual y.
      (ANF ensures the substitution does not introduce arbitrary expressions into the refinements.)
      Furthermore, the input value y is constrained to be a subtype of the function’s input type.
    • Type-Instantiation (e[τ ]) is handled by generating a fresh template whose shape is that of
      the polymorphic instance τ , and substituting that in place of the type variable α in the type
      (scheme) obtained for e.
Soundness of Constraint Generation We can prove by induction on the structure of e that the
NNF constraints generated by cgen capture the refinement type checking obligations of [Knowles
and Flanagan 2010; Vazou et al. 2014b]. Let cgen(e) denote the constraint returned by cgen(∅, e).
We prove that if cgen(e) is satisfiable, then ∅ ⊢ e : t for some refinement type t. This combined with
the soundness of refinement typing (Theorem 1, [Vazou et al. 2014b]) yields:
    Theorem 4.8. If cgen(e) is satisfiable then e is safe.

5     ALGORITHM
Next, we describe our algorithm for solving the constraints generated by cgen, i.e. for for finding a
satisfying assignment – and hence inferring suitable refinement types. Our algorithm is an instance
of the classical “unfolding” method for logic programs [Burstall and Darlington 1977; Pettorossi
and Proietti 1994; Tamaki and Sato 1984]. We show how to apply unfolding to the NNF constraints
derived from refinement typing, in a scoped fashion that avoids the blowup caused by long let-chains.
First, we describe a procedure for computing the scope of a κ variable (§ 5.1). Second, we show how
to use the scope to compute the strongest solution for a single κ variable (§ 5.2). Third, we describe
how we can eliminate a κ by replacing it with its strongest solution (§ 5.3). Fourth, we show how
the above procedure can be repeated when the constraints are acyclic (§ 5.4). Finally, we describe
how to use our method when the constraints have cycles (§ 5.5).

5.1    The Scope of a Variable
Procedure scope(κ, c) (Fig. 9) returns a sub-constraint of c of the form: ∀(x i :pi ) ⇒ c ′ such that
(1) κ does not occur in any pi , and (2) all occurrences of κ in c occur in c ′. As occurrences of κ in c
occur under x i :pi , we can omit these binders from the solution of κ, thereby avoiding the blowup
from unfolding let-chains described in § 2.4. Restricting unfolding to scope(κ, c) does not affect
satisfiability. The omitted hypotheses are redundant as they are already present at all uses of κ.
This intuition is captured by the following lemmas that follow by induction on c.

                               Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:18                                                                          Benjamin Cosman and Ranjit Jhala


                          cgen                               :    (Γ × E) → (C × T )
                          cgen(Γ, c)                             (true, prim(c))
                          cgen(Γ, x)                             (true, single(Γ, x))
                          cgen(Γ, let x = e 1 in e 2 )           (c ∧ sub(t 2 , tˆ), tˆ)
                            where
                              c                              = c 1 ∧ ((x :: t 1 ) ⇒ c 2 )
                              tˆ                             = fresh(∅, shape(t 2 ))
                              (c 1 , t 1 )                   = cgen(Γ, e 1 )
                              (c 2 , t 2 )                   = cgen(Γ; x :t 1 , e 2 )
                          cgen(Γ, λx :τ .e)                   (c, x : tˆ → t)
                            where
                              (c, t)                         =    cgen(Γ; x : tˆ, e)
                              tˆ                             =    fresh(∅, τ )
                          cgen(Γ, e y)                           (c ∧ cy , t ′ [y/x])
                            where
                              cy                             =    sub(single(Γ, y), t)
                              (c, x :t → t ′)                =    cgen(Γ, e)
                          cgen(Γ, Λα .e)                         (c, ∀α .t)
                            where
                              (c, t)                         =    cgen(Γ; α, e)
                          cgen(Γ, e[τ ])                          (c, t tˆ/α )
                                                                         
                                                             
                            where
                              (c, ∀α .t)                     =    cgen(Γ, e)
                              tˆ                             =    fresh(∅, τ )

                          single                             :    (Γ × X ) → T
                          single(Γ, x)
                             | t = {x :b | p}                 {ν :b | p [ν /x] ∧ ν = x }
                             | otherwise                      t
                             where t                         = Γ(x)


                                           Fig. 8. Constraint Generation


   Lemma 5.1 (Scoped-Definitions). c ↓κ ≡ scope(κ, c)↓κ
   Lemma 5.2 (Scoped-Uses). c ↑κ ≡ scope(κ, c)↑κ ∪ C for some flat constraints C such that κ < C.
   Lemma 5.3 (Scoped-Satisfaction). If σ |= c then σ |= scope(κ, c).

5.2     The Strongest Solution
Procedure sol1(κ, c) (Fig. 10) returns a predicate that is guaranteed to satisfy all the clauses where
κ appears as the head. The procedure recursively traverses c to compute the returned predicate as
the disjunction of those bodies in c where κ appears as the head. When the head does not contain κ,
the output predicate is the empty disjunction, false.

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                               26:19


                          scope                           :       (K × C) → C
                          scope(κ, c 1 ∧ c 2 )
                             | κ ∈ c1, κ < c2                    scope(κ, c 1 )
                             | κ < c1, κ ∈ c2                    scope(κ, c 2 )
                          scope(κ, ∀x :b. p ⇒ c ′)
                             | κ <p                              ∀x :b. p ⇒ scope(κ, c ′)
                          scope(κ, c)                      c


                                    Fig. 9. The scope of a κ in constraint c.


                   sol1                          :   (K × C) → P
                   sol1(κ, c 1 ∧ c 2 )              sol1(κ, c 1 ) ∨ sol1(κ, c 2 )
                   sol1(κ, ∀x :b. p ⇒ c)            ∃x :b. p ∧ sol1(κ, c)
                   sol1(κ, κ(y))                       i x i = yi where x = params(κ)
                                                     Ó
                                                 
                   sol1(κ, p)                       false


                               Fig. 10. The Strongest Solution for a κ-Variable.

The Strongest Solution The strongest (resp. scoped) solution for κ in c, written σκc (resp. σ̂κc ) is:
              σκc  [κ 7→ λx .sol1(κ, c)]
              σ̂κc  [κ 7→ λx .sol1(κ, c ′)] where scope(κ, c) ≡ ∀(x i :pi ) ⇒ c ′s.t. κ < pi
The name “strongest solution” is justified by the following theorems. First, we prove that σκc satisfies
the definitions of κ in c.
  Lemma 5.4 (Strongest-Sat-Definitions). σκc |= c ↓κ
  As an example, consider the constraint: c 5  ∀a. p a ⇒ ∀b. q b ⇒ κ(a) ∧ κ(b). Below, we show
each sub-constraint c i , and the corresponding solution returned by sol1(κ, c i ):
        c1    κ(a)                       sol1(κ, c 1 )           x =a
        c2    κ(b)                       sol1(κ, c 2 )           x =b
        c3    c1 ∧ c2                    sol1(κ, c 3 )           x =a ∨x =b
        c4    ∀b. q b ⇒ c 4              sol1(κ, c 4 )           ∃b. q b ∧ (x = a ∨ x = b)
        c5    ∀a. p a ⇒ c 4              sol1(κ, c 5 )           ∃a. p a ∧ (∃b. q b ∧ (x = a ∨ x = b))
Note that in essence, σκc 5  [κ 7→ λx .sol1(κ, c 5 )] maps κ to the disjunction of the two hypotheses
(bodies) under which κ appears, thereby satisfying both implications, and hence satisfying c 5 ↓κ.
The Strongest Scoped Solution The addition of hypotheses – the binders x i :pi under which κ
always occurs – preserves validity. Thus, Lemma 5.4 implies that the strongest scoped solution
satisfies the definitions of κ in c.
  Theorem 5.5 (Strongest-Scoped-Sat-Definitions). σ̂κc |= c ↓κ.
   Furthermore, if there exists a solution σ that satisfies c then the composition of σ and the
strongest scoped solution also satisfies c.

                                Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:20                                                                        Benjamin Cosman and Ranjit Jhala


                          elim1                           :   (K × C) → C
                          elim1(κ, c)                        elim∗ (σ̂κc , c)
                             where
                              σ̂κc                       =    [κ 7→ λx .sol1(κ, c ′)]
                              ∀(x i :pi ) ⇒ c ′          =    scope(κ, c)
                              x                          =    params(κ)
                          elim∗                           :   (Σ × C) → C
                          elim∗ (σ , c   1 ∧ c2)             elim∗ (σ , c 1 ) ∧ elim∗ (σ , c 2 )
                          elim∗ (σ , ∀x :b. p ⇒ c)           ∀x :b. σ (p) ⇒ elim∗ (σ , c)
                          elim∗ (σ , κ(y))
                              | κ ∈ domain(σ )               true
                          elim∗ (σ , p)                   p


                                             Fig. 11. Eliminating Variables.


   Theorem 5.6 (Strongest-Scoped-Sat-Uses). If σ |= c then σ · σ̂κc |= c.
  By Theorem 5.5 and Lemma 4.7 it suffices to restrict attention to uses of κ, i.e. to prove that if
σ |= c ↑ κ then σ · σ̂κc |= c ↑ κ. We show this via a key lemma that states that any solution σ that
satisfies c, must assign κ to a predicate that is implied by, i.e. weaker than, sol1(κ, c).
   Lemma 5.7 (Strongest-Solution). If σ , x i :pi |= c then σ , x i :pi |= σκc (p) ⇒ p.
  We use the above lemma to conclude that the hypotheses in c ↑κ are strengthened under σ · σ̂κc ,
and hence, that each corresponding goal remains valid under the composed assignment.

5.3     Eliminating One Variable
Next, we show how to eliminate a single κ variable by replacing it with its strongest solution.
Variable Elimination (elim∗ (σ , c)) Procedure elim∗ (σ , c) (Fig. 11) eliminates from c all the κ
variables defined in σ by replacing them with σ (κ). That is, the procedure returns as output a
constraint c ′ where: (1) every body-occurrence of a κ i.e. where κ appears as a hypothesis, is replaced
by σ (κ), and (2) every head-occurrence of a κ i.e. where κ appears as a goal, is replaced by true if κ
is in the domain of σ , and left unchanged otherwise. We prove by induction over c that eliminating
a single variable κ yields a constraint over just the uses of that variable:
   Lemma 5.8 (elim∗ ). If domain(σ ) = {κ} and c ′ = elim∗ (σ , c) then κ < c ′ and flat(c ′) = σ (c ↑κ).

Eliminating One Variable Procedure elim1(κ, c) (Fig. 11) eliminates κ from a constraint c by
invoking elim on the strongest (scoped) solution for κ in c. We prove that if κ is acyclic in c then
elim1(κ, c) returns an constraint without κ that is satisfiable if and only if c is satisfiable.
   Theorem 5.9 (Elim-Preserves-Satisfiability). elim1(κ, c) is satisfiable iff c is satisfiable.
  Intuitively, if σ |= elim1(κ, c) then, via Theorem 5.6 and Lemma 4.3, we have σ · σ̂κc satisfies c.
Dually, if σ |= c then we show that σ |= elim1(κ, c). See § A for details.

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                                  26:21

5.4     Eliminating Acyclic Variables
When the constraint c is acyclic, we can iteratively eliminate all the variables in K to obtain a VC
whose validity determines the satisfiability of c, as each elimination preserves acyclicity:
  Lemma 5.10 (Elim-Acyclic). If K ′ is acylic in c, deps(σ ) ⊆ deps(c) then K ′ is acyclic in elim∗ (σ , c).
Eliminating Many Variables Procedure elim(K, c) (Fig. 12) eliminates a set of acyclic K variables
by iteratively eliminating each variable via elim1. Using Theorem 5.9, Lemma 5.8 and Lemma 5.10
we show that the elimination of multiple acyclic κ-variables also preserves satisfiability.
  Corollary 5.11 (Exact-Satisfaction). Let c ′  elim(K, c).
  (1) kvars(c ′) = ∅, i.e. c ′ is a VC, and
  (2) c ′ is satisfiable iff c is satisfiable.
Unavoidable Worst-Case Blowup Note that in the worst case, the elim procedure can cause an
exponential blowup in the constraint size. In general some form of blowup is unavoidable as even the
Boolean version of the constraint satisfaction problem is complete for exponential time. A boolean
constraint is an acyclic constraint where each variable is of type Bool. The Boolean Constraint
Satisfaction (BcSat) problem is to decide whether a given boolean constraint is satisfiable.
  Theorem 5.12. BcSat is ExpTime-complete.
   The above is a corollary of [Godefroid and Yannakakis 2013] and the fact that reachability of
(non-recursive) boolean programs is equivalent to the satisfaction of (acyclic) boolean constraints
via the correspondence of [Jhala et al. 2011]. Thus, as validity checking is in Np, it is not possible
to always generate compact (polynomial sized) formulas, assuming ExpTime , Np.
Avoiding Let-Chain Blowup Recall the example from § 2.4. Let c be the NNF constraint in (14)
and consider the sequence of intermediate constraints produced by eliminating κ 1 , . . . , κn from c:
                c1  c
             c i+1  elim1(κi , c i ) for i ∈ 1, . . . , n
At each step, the strongest solution for κi is computed from scope(κ, c i ), i.e. the part of the constraint
derived from the subterm where the binder xi is in scope. Thus, for each i ∈ 1, . . . , n we get solutions
      sol1(κi , c i )  ∃ν . ν = xi−1 ∧ z = ν                                                                       (15)
where params(κi ) = z. For brevity of exposition, we simplify the above to
      sol1(κi , c i )  z = xi−1
and hence, note that elim([κ 1 , . . . , κn ], c,) yields the linear-sized VC
             c n+1  ∀x0 . 0 ≤ x0 ⇒ ∀x1 . x1 = x0 ⇒ . . . ⇒ ∀xn . xn = xn−1 ⇒ ∀ν . ν = xn ⇒ 0 ≤ ν
that is easily proved valid by the SMT solver.

5.5     Eliminating Cyclic Variables
When the constraint c is cyclic, the satisfaction problem is undecidable via a reduction from the
problem of checking the safety of while-programs [Bjørner et al. 2015]. Consequently, we can only
compute over-approximate or conservative solutions via abstract interpretation [Jhala et al. 2011].
Our approach is to (1) compute the set of variables that make the constraints cyclic (i.e. whose
absence would make the constraints acyclic), (2) eliminate all except those variables, and (3) use
predicate abstraction to solve the resulting constraint, yielding a method that is much faster and
more precise (§ 6), than “global” Liquid Typing [Rondon et al. 2008].

                                   Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:22                                                                       Benjamin Cosman and Ranjit Jhala


                           sat                      :    (C × 2R ) → {True, False}
                           sat(c, Q)                    solve(cs, Q)
                             where
                                c′                  =    elim(K̂, c) where K̂ cuts c
                                cs                  =    flat(c ′)

                           flat                     :   C → 2C
                           flat(true)                   ∅
                           flat(p)                      {p}
                           flat(c ∧ c ′)                flat(c) ∪ flat(c ′)
                           flat(∀x :b. p ⇒ c)           {∀x :b. p ⇒ c ′ | c ′ ∈ flat(c)}

                           elim                     :    (2K × C) → C
                           elim([], c)               c
                           elim(κ : κs, c)              elim(κs, elim1(κ, c))


                                     Fig. 12. Checking Constraint Satisfaction




Cut Variables A set of refinement variables K̂ cuts a constraint c if K − K̂ is acyclic in c. We
cannot compute the minimum set of cut variables as this is the NP-Complete minimum feedback
vertex set problem [Karp 1972]. Instead we use a greedy heuristic to compute K̂. We compute the
strongest connected component (SCC) digraph for deps∗ (c), and iteratively remove κ-variables (and
recompute the digraph) until each SCC has a single vertex i.e. the graph is acyclic. The reasoning
for Lemma 5.11 yields the following corollary:

  Corollary 5.13. If K̂ cuts c then elim(K − K̂, c) returns a constraint c ′ such that kvars(c ′) ⊆ K̂
and c ′ is satisfiable iff c is satisfiable.


Exact and Approximate Constraint Satisfaction Procedure sat(c, Q) (Fig. 12) computes a set
of cut variables K̂, and then uses elim to compute exact solutions for non-cut variables, and finally
computes approximate solutions for the residual cut variables left over after elimination, using
the solve procedure from [Rondon et al. 2008] which computes the satisfaction of (non-nested)
constrained Horn Clauses (CHC) (obtained via flat) using predicate abstraction [Flanagan et al.
2001; Graf and Saïdi 1997].

   Theorem 5.14 (Satisfaction).
   (1) If sat(c, Q) then c is satisfiable.
   (2) If c is acyclic, then sat(c, Q) iff c is satisfiable.

  These results follow from Corollary 5.11, 5.13, the properties of solve (Theorem 2, [Rondon et al.
2008]), and as solve reduces to SmtValid(c) when kvars(c) is empty.

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                                  26:23

6   EVALUATION
We have implemented Fusion within the LiqidHaskell refinement type checker [Vazou et al.
2014b]. It is used by default in the current version 1 . We evaluate the speed and precision of Fusion
on two sets of benchmarks from the LiqidHaskell project totalling more than 12KLOC. Our
formalism based on call-by-value evaluation is sound for Haskell as we also simultaneously prove
termination for all potentially bottom-inhabited terms, as described in [Vazou et al. 2014b]. Our
results show that Fusion yields nearly 2× speedups for safety verification benchmarks and, by
synthesizing the most precise types more than 10× faster, actually enables theorem proving.
Safety Property Benchmarks The first set of benchmarks are drawn from the Haskell standard
libraries and detailed in [Vazou et al. 2014a]. Data-Struct comprises applicative data structures
like red-black trees, lists (Data.List), splay trees (Data.Set.Splay), and binary search trees
(Data.Map.Base); we verify termination and structure specific invariants like ordering and balance.
Vector-Algorithms comprises a suite of imperative (i.e. monadic) array-based sorting algorithms;
we verify termination and the correctness of array accesses. Text and Bytestring are the standard
libraries for high-performance unicode text and byte-array processing which are implemented via
low-level pointer arithmetic; we verify termination, memory safety and correctness properties
specified by the library API.
Theorem Proving Benchmarks Recent work shows how refinement typing can convert legacy
languages like Haskell into proof assistants where ordinary programs can be used to write arbitrary
proofs of correctness about the “deep specifications” of other programs, and have the proofs checked
via refinement typing [Vazou and Jhala 2016]. The second set of benchmarks corresponds to a
set of programs corresponding to such proofs. Arith includes theorems about the growth of the
fibonacci and ackermann functions; Fold includes theorems about the universality of traversals;
Monoid, Functor, Applicative and Monad includes proofs of the respective category-theoretic
laws for the Maybe, List, and Id instances of the respective typeclasses; and finally, SatSolver
and Unification are fully verified implementations of the respective algorithms from the Zombie
suite which, absent SMT support, requires significantly more local annotations (proof terms) from
the user [Casinghino et al. 2014; Sjöberg and Weirich 2015].
Methodology For each benchmark, we compare the performance of LiqidHaskell using the (L)
global refinement inference from [Rondon et al. 2008], and using our (F) local refinement algorithm.
We compare the amount of Time(s), in seconds, it took to check each benchmark. Each benchmark
represents several Haskell files (modules); we report Qualifiers, the average number of qualifiers
(predicates) that were required to synthesize the types needed for verification per file. In addition to
the variables needed to eliminate cycles, we aggressively mark all refinement variables appearing
in templates for “top-level” types as cut-variables to ensure that simple refinements (over qualifiers)
are synthesized for such functions. All benchmarks were run on a MacBook Pro with a 2.2 GHz
Intel Core i7 processor, using the Z3 SMT solver for checking validity. Table 1 summarizes the
results.
Safety Verification Results Two points emerge from the safety verification benchmarks. First,
for the larger benchmarks (text and bytestring), for which there already exist suitable qualifiers
permitting global inference, the new local Fusion algorithm yields significant speedups – often
halving the time taken for verification. (Note this includes end-to-end time, including name res-
olution, plain type checking etc., and so the actual speedup for just refinement checking is even
greater.) Second, even for these benchmarks, Fusion reduces (nearly halves) the number of required
qualifiers. This makes the checker significantly easier to use, as the programmer does not have
1 https://github.com/ucsd-progsys/liquidhaskell



                                   Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:24                                                                       Benjamin Cosman and Ranjit Jhala

Table 1. Comparing Liquid inference (L) [Rondon et al. 2008] with Fusion (F). The number of modules
(files) per benchmark is listed in parentheses. Code is the total number of lines of non-comment and non-
whitespace lines of code and Spec is the total number of lines of specification (i.e. top-level signatures),
computed by sloccount. Qualifiers is the number of qualifiers needed for refinement inference; * means a
false-positive, i.e. the benchmark could not be verified using the qualifiers provided as the intermediate terms
have refinements not expressible using the given qualifiers. Time(s) is the total time in seconds needed to
verify the benchmark (or to return a false positive, for times with a *).


                      Benchmark                Code      Spec     Qualifiers        Time(s)
                                                                  L     F           L    F
                      Data-Struct (8)           1818       408 5              4     126 94
                      Vec-Algos (11)            1252       279 4              4      78 61
                      Bytestring (11)           4811       726 18            11     233 136
                      Text (17)                 3157       818 9              5     349 231
                      Arith (2)                  270        46     *          0     *63   5
                      Fold (1)                    70        29     0          0      78   1
                      Monoid (2)                  85        16     0          0       3   1
                      Functor (3)                137        28     0          0      55   3
                      Applicative (2)            146        36     *          0     *70   2
                      Monad (3)                  180        42     *          0     *35   3
                      Sat-Solver (1)              98        31     *          0     *48   1
                      Unification (1)            139        53     *          1    *240   3




reason about which qualifiers to use for intermediate terms. By synthesizing strongest refinements,
Fusion removes a key source of unpredictability and hard-to-diagnose false alarms.

Theorem Proving Results The improvement is more stark for the theorem proving benchmarks:
most of them can only be checked using local inference. There are several reasons for this. The
proofs are made possible by heavy use of polymorphic proof combinators. As the specifications
are much more complicated, the combinators’ type variables must be (automatically) instantiated
with significantly more complex refinements that relate many program variables. Thus, it is very
difficult for the user to even determine the relevant qualifiers. Even if they could, the qualifiers have
many free variable (parameters) which causes an exponential blowup when matching against actual
program variables, making global, abstract interpretation based refinement synthesis impossible.
In contrast, since the theorem proving benchmarks have almost no cyclic dependencies, Fusion
makes short work of automatically synthesizing the relevant refinement instantiations, making
complex proofs possible.

Comparison with other Tools We are not aware of any other tool that scales up to these programs.
F* [Swamy et al. 2011] requires local annotations as described in § 2, Mochi [Unno et al. 2013]
requires no annotations but may diverge, and does not support uninterpreted functions which
precludes all of our benchmarks. Similarly, existing Horn Solvers like µZ3 may diverge, while
Eldarica [Rümmer et al. 2015], HSF [Grebenshchikov et al. 2012], and Spacer [Komuravelli et al.
2016] do not support uninterpreted functions.

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                             26:25

7   RELATED WORK
Floyd-Hoare Logics and Model Checking The process of eliminating refinement variables to get
a single verification condition (checked by SMT) is analogous to the VC-generation step used in ESC-
style checkers [Flanagan et al. 2002; Nelson 1981]. Indeed we use the term “strongest refinement”
or “solution” for the intermediate types to highlight the analogy with the notion of “strongest
postconditions” from Floyd-Hoare Logic. While Fusion seeks to minimize the size of the generated
VC, unlike in the intra-procedural case [Flanagan and Saxe 2000; Leino 2005], ExpTime-completeness
means we cannot get compact VCs (Theorem 5.12). In the presence of loops, direct VC generation
is insufficient, and one must compute over-approximations. Fusion’s elimination procedure can
be viewed as a generalization of the large block encoding method [Beyer et al. 2009] where over-
approximation is performed not at each instruction, but only at “back edges” in the control-flow
graph. Similarly, in program analyses it is common to “inline” the code for a procedure at a call site
to improve precision. In [Swamy et al. 2013], the authors show how to generalize the notions of
composing weakest preconditions across higher-order functions via the notion of a Dijkstra Monad.
Fusion’s elimination procedure is a way to systematically generalize and lift the Floyd-Hoare
notions of strongest-postconditions (dually, weakest-preconditions), large block encodings, and
procedure inlining to the typed, higher order setting. However, unlike Dijkstra Monads, Fusion
exploits the compositional structure of types to locally synthesize precise refinements (i.e. invariants)
in the presence of polymorphic collections and higher-order functions, to allow checking examples
like ex2, ex3, and ex4 (§ 2).
Local Type Inference Fusion performs a local inference in that if the constraints are acyclic, then
Fusion is able to synthesize all intermediate refinement types exactly. However, refinements render
the problem (and our solution) quite different than classical local typing [Pierce and Turner 1998],
even with subtyping [Odersky et al. 2001]. First, even when all top-level (recursive) functions have
signatures, the constraints may get cycles, for example, at instantiation sites for fold functions
(whose polymorphic type variables must be instantiated with the analogue of a “loop invariant”.)
Second, our approach is orthogonal to bidirectional type checking. Indeed, they can be (and in our
implementation, are) combined to yield a simpler system of constraints, but we still need solK and
elim to synthesize the strongest refinements relating different program variables.
Refinement Inference There are several other approaches to synthesizing refinements. First,
[Knowles and Flanagan 2009] shows how existentials can be used to type let-binders. Second,
[Bengtson et al. 2008] shows how a form of bidirectional typing can be used to infer some interme-
diate types. Third, [Rondon et al. 2008] introduces the liquid typing framework for synthesizing
refinements via abstract interpretation. Fourth, [Polikarpova et al. 2016] shows that liquid typing
can be made bidirectional and presents a new demand driven (“round trip”) algorithm for doing
the abstract interpretation (and also solving for the weakest solution.) However, none of the above
approaches is able to handle the idiomatic examples shown in § 2, or can only do so if given a
suitable abstract domain (via templates). We can try to infer such templates via abstraction refine-
ment [Jhala et al. 2011; Kobayashi et al. 2011; Unno et al. 2013] but that approach is notoriously
unpredictable and prone to diverging, especially in the presence of uninterpreted functions which
are ubiquitous in our examples. Finally, [Zhu et al. 2015] shows how machine learning over dynamic
traces can be used to learn refinements (in a generalization of the approach pioneered by [Ernst
et al. 2001]). However, this needs closed programs (that can be run), which can limit applicability
to higher order functions.
Horn Clauses Horn clauses have recently become a popular “intermediate representation” for
verification problems [Bjørner et al. 2015], as they can be used to encode the proof rules for classical
imperative Floyd-Hoare logics, and concurrent programs [Grebenshchikov et al. 2012] among

                              Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:26                                                                            Benjamin Cosman and Ranjit Jhala

others. However, current Horn Clause solvers e.g. [Grebenshchikov et al. 2012; Hoder and Bjørner
2012; Rümmer et al. 2015] are based on CEGAR and interpolation and hence, to quote a recent
survey [Bjørner et al. 2015]: “mainly tuned for real and linear integer arithmetic and Boolean
domains” rendering them unable to check any of our benchmarks which make extensive use
of uninterpreted functions. Our work shows how to (1) algorithmically generate NNF clauses
from typed, higher-order programs, in a way that preserves scoping, (2) use an optimized form of
“unfolding” [Burstall and Darlington 1977; Pettorossi and Proietti 1994; Tamaki and Sato 1984] to
synthesize the most precise type and (3) thereby, obtain a method for improving the speed, precision
and completeness of refinement type checking.

ACKNOWLEDGMENTS
We thank the anonymous referees, Nadia Polikarpova, Eric Seidel and Niki Vazou for their invaluable
feedback on earlier drafts of this paper. This material is based upon work supported by the National
Science Foundation under Grant Numbers CCF-1422471, CCF-1223850, and CCF-1218344, and a
generous gift from Microsoft Research.

REFERENCES
C. Barrett, P. Fontaine, and C. Tinelli. 2016. The Satisfiability Modulo Theories Library (SMT-LIB). www.SMT-LIB.org.
    (2016).
J. Bengtson, K. Bhargavan, C. Fournet, A.D. Gordon, and S. Maffeis. 2008. Refinement Types for Secure Implementations. In
    CSF.
Dirk Beyer, Alessandro Cimatti, Alberto Griggio, M. Erkan Keremoglu, and Roberto Sebastiani. 2009. Software model
    checking via large-block encoding. In FMCAD.
Nikolaj Bjørner, Arie Gurfinkel, Ken McMillan, and Andrey Rybalchenko. 2015. Horn Clause Solvers for Program Verification.
    In Fields of Logic and Computation.
Rod M. Burstall and John Darlington. 1977. A Transformation System for Developing Recursive Programs. J. ACM 24, 1
    (1977), 44–67.
Chris Casinghino, Vilhelm Sjöberg, and Stephanie Weirich. 2014. Combining Proofs and Programs in a Dependently Typed
    Language. In POPL.
R.L. Constable. 1986. Implementing Mathematics with the Nuprl Proof Development System. Prentice-Hall.
J. Dunfield. 2007. Refined typechecking with Stardust. In PLPV.
M.D. Ernst, J. Cockrell, W. G. Griswold, and D. Notkin. 2001. Dynamically Discovering Likely Program Invariants to Support
    Program Evolution. IEEE TSE 27(2) (2001), 1–25.
C. Flanagan, R. Joshi, and K. R. M. Leino. 2001. Annotation inference for modular checkers. Inform. Process. Lett. (2001).
C. Flanagan, K.R.M. Leino, M. Lillibridge, G. Nelson, J. B. Saxe, and R. Stata. 2002. Extended static checking for Java. In PLDI.
C. Flanagan and J.B. Saxe. 2000. Avoiding exponential explosion: generating compact verification conditions. In POPL.
Patrice Godefroid and Mihalis Yannakakis. 2013. Analysis of Boolean Programs. In TACAS.
S. Graf and H. Saïdi. 1997. Construction of abstract state graphs with PVS. In CAV. Springer, 72–83.
Sergey Grebenshchikov, Nuno P. Lopes, Corneliu Popeea, and Andrey Rybalchenko. 2012. Synthesizing software verifiers
    from proof rules. In PLDI.
Kodai Hashimoto and Hiroshi Unno. 2015. Refinement Type Inference via Horn Constraint Optimization. In Static Analysis -
    22nd International Symposium, SAS 2015, Saint-Malo, France, September 9-11, 2015, Proceedings. 199–216. https://doi.org/
    10.1007/978-3-662-48288-9_12
Ralf Hinze. 2009. Functional pearl: la tour d’Hanoï. In ICFP.
Kryštof Hoder and Nikolaj Bjørner. 2012. Generalized Property Directed Reachability. In SAT.
Ranjit Jhala, Rupak Majumdar, and Andrey Rybalchenko. 2011. HMC: Verifying Functional Programs Using Abstract
    Interpreters. In CAV. https://doi.org/10.1007/978-3-642-22110-1_38
R. Jhala and K.L. McMillan. 2006. A Practical and Complete Approach to Predicate Refinement. In TACAS 06.
Richard M. Karp. 1972. Reducibility Among Combinatorial Problems. In Proceedings of a symposium on the Complexity of
    Computer Computations.
Andrew M. Kent, David Kempe, and Sam Tobin-Hochstadt. 2016. Occurrence typing modulo theories. In PLDI.
K. Knowles and C. Flanagan. 2007. Type Reconstruction for General Refinement Types. In ESOP. http://kenn.frap.net/
    publications/knowles-flanagan.esop.07.type.pdf
K.W. Knowles and C. Flanagan. 2010. Hybrid type checking. ACM TOPLAS (2010).


Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                                    26:27

K. W. Knowles and C. Flanagan. 2009. Compositional reasoning and decidable checking for dependent contract types. In
    PLPV.
Naoki Kobayashi, Ryosuke Sato, and Hiroshi Unno. 2011. Predicate abstraction and CEGAR for higher-order model checking.
    In PLDI.
Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. 2016. SMT-based model checking for recursive programs. Formal
    Methods in System Design 48, 3 (2016), 175–205. https://doi.org/10.1007/s10703-016-0249-4
K. Rustan M. Leino. 2005. Efficient weakest preconditions. Inf. Process. Lett. 93, 6 (2005).
G. Nelson. 1981. Techniques for program verification. Technical Report CSL81-10. Xerox Palo Alto Research Center.
Martin Odersky, Christoph Zenger, and Matthias Zenger. 2001. Colored local type inference. In POPL.
X. Ou, G. Tan, Y. Mandelbaum, and D. Walker. 2004. Dynamic Typing with Dependent Types. In IFIP TCS.
Alberto Pettorossi and Maurizio Proietti. 1994. Transformation of logic programs: Foundations and techniques. The Journal
    of Logic Programming 19 (1994), 261 – 320.
B. C. Pierce and D. N. Turner. 1998. Local Type Inference. In POPL.
Nadia Polikarpova, Ivan Kuraj, and Armando Solar-Lezama. 2016. Program synthesis from polymorphic refinement types.
    In PLDI.
P. Rondon, M. Kawaguchi, and R. Jhala. 2008. Liquid Types. In PLDI.
Philipp Rümmer, Hossein Hojjat, and Viktor Kuncak. 2015. On recursion-free Horn clauses and Craig interpolation. Formal
    Methods in System Design 47, 1 (2015), 1–25.
J. Rushby, S. Owre, and N. Shankar. 1998. Subtypes for Specifications: Predicate Subtyping in PVS. IEEE TSE (1998).
Vilhelm Sjöberg and Stephanie Weirich. 2015. Programming up to Congruence. In POPL.
N. Swamy, J. Chen, C. Fournet, P-Y. Strub, K. Bhargavan, and J. Yang. 2011. Secure distributed programming with value-
    dependent types. In ICFP.
N. Swamy, J. Weinberger, C. Schlesinger, J. Chen, and B. Livshits. 2013. Verifying Higher-order Programs with the Dijkstra
    Monad. In PLDI.
Hisao Tamaki and Taisuke Sato. 1984. Unfold/Fold Transformation of Logic Programs. In Proceedings of the Second
    International Logic Programming Conference, Uppsala University, Uppsala, Sweden, July 2-6, 1984. 127–138.
H. Unno, T. Terauchi, and N. Kobayashi. 2013. Relatively complete verification of higher-order functional programs. In
    POPL.
N. Vazou and R. Jhala. 2016. Refinement Reflection (or, how to turn your favorite language into a proof assistant using
    SMT). ArXiv e-prints (Oct. 2016). arXiv:cs.PL/1610.04641
N. Vazou, E. L. Seidel, and R. Jhala. 2014a. LiquidHaskell: Experience with refinement types in the real world. In Haskell.
N. Vazou, E. L. Seidel, R. Jhala, D. Vytiniotis, and S. L. Peyton Jones. 2014b. Refinement Types for Haskell. In ICFP.
Panagiotis Vekris, Benjamin Cosman, and Ranjit Jhala. 2016. Refinement types for TypeScript. In PLDI.
H. Xi and F. Pfenning. 1998. Eliminating Array Bound Checking Through Dependent Types.. In PLDI.
He Zhu, Aditya V. Nori, and Suresh Jagannathan. 2015. Learning refinement types. In ICFP.



A    APPENDIX: PROOFS
We include below the proofs of the key theorems.


    Proof. (Lemma 5.7) Assume that p ≡ κ(z) where z = params(κ) The other cases are trivial as
σκc (p) = p, and σ (p1 ) ⇒ p1 and σ (p2 ) ⇒ p2 implies σ (p1 ∧ p2 ) ⇒ p1 ∧ p2 . The proof is by induction
on the structure of c.


    Case: c ≡ κ(y).

                          By definition of sol1(c, κ)             σκc (κ(z)) = z = y                                 (16)
                                                Assume             σ , x i :pi |= κ(y)
                                                  Hence            σ , x i :pi |= z = y ⇒ κ(z)
                                                   By 16           σ , x i :pi |= σκc (κ(z)) ⇒ κ(z)


                                   Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:28                                                                         Benjamin Cosman and Ranjit Jhala

   Case: c ≡ p ′, such that κ < p ′.
                           By definition of validity              σ , x i :pi |= false ⇒ κ(z)
                     By the definition of sol1(c, κ)             σκc (κ(z)) = false
                                                 Hence,           σ , x i :pi |= σκc (κ(z)) ⇒ κ(z)
   Case: c ≡ c 1 ∧ c 2 .
      Let p j = sol1(c j , κ) for j = 1, 2
              Thus, by the definition of sol1(c, κ)              σκc (κ(z)) = p1 ∨ p2                            (17)
                                  Assume, for j = 1, 2            σ , x i :pi |= ∧j c j
                                   That is, for j = 1, 2          σ , x i :pi |= c j
                                    By IH, for j = 1, 2           σ , x i :pi |= p j ⇒ κ(z)
                                                 Hence,           σ , x i :pi |= (p1 ∨ p2 ) ⇒ κ(z)
                                          Thus, by 17,            σ , x i :pi |= σκc (κ(z)) ⇒ κ(z)
   Case: c ≡ ∀x :b. p ⇒ c ′.
      Let p ′ = sol1(c ′, κ).
                                                                σκc (κ(z)) = p ′
                                                                   ′
              Thus, by the definition of sol1(c, κ)                                                              (18)
                                                                 σκc (κ(z)) = ∃x :b. p ∧ p ′                     (19)
                                                Assume            σ , x i :pi |= ∀x :b. p ⇒ c    ′

                                          By Sat-Ext σ , x i :pi , x :p |= c ′
                                                  By IH σ , x i :pi , x :p |= σκc (κ(z)) ⇒ κ(z)
                                                                                       ′



                                                  By 18 σ , x i :pi , x :p |= p ′ ⇒ κ(z)
                                          By Sat-Ext              σ , x i :pi |= ∀x :b. p ⇒ p ′ ⇒ κ(z)
                                                That is,          σ , x i :pi |= ∀x :b. (p ∧ p ′ ⇒ κ(z))
                                             As x < κ(z)          σ , x i :pi |= (∃x :b. p ∧ p ′) ⇒ κ(z)
                                                  By 19           σ , x i :pi |= σκc (κ(z)) ⇒ κ(z)
                                                                                                                   □
   Proof. (Theorem 5.4) The proof is an induction on the structure of c.
   Case: c ≡ κ(y).
                                By definition           c ↓κ  κ(y)
                                         and          σκc (κ)  λx . ∧i x i = yi           where x = params(κ)
                                      Hence,       σκc (c ↓κ)  ∧i yi = yi                                       (20)
                     As 20 is a tautology                  σκc |= c ↓κ
   Case: c ≡ p.
                                By definition           c ↓κ  true
                                      Hence,       σκc (c ↓κ)  true                                             (21)
                     As 21 is a tautology                  σκc |= c ↓κ

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                               26:29

Case: c ≡ c 1 ∧ c 2 .

   For i ∈ {1, 2}, let pi = sol1(κ, c i ), σκc i (κ) = λx .pi .

                           By definition             c ↓κ  c 1 ↓κ ∪ c 2 ↓κ                                      (22)
                                    By IH             σκc i |= c i ↓κ                                            (23)

Let c ′ ∈ c i ↓κ. As κ only in head, c ′ ≡ ∀(y :p) ⇒ κ(x).

                                    By 23             y :p |= σκc i (κ(x))
                          By Lemma 4.1                y :p |= σκc 1 (κ(x)) ∨ σκc 2 (κ(x))
                                  That is             y :p |= σκc (κ(x))
                  So for any c ′ ∈ c i ↓κ              σκc |= c ′
                                   Hence               σκc |= c i ↓κ
                        and hence, by 22               σκc |= c ↓κ

Case: c ≡ ∀x :b. p ⇒ c ′.

   Let p ′ = sol1(κ, c ′), σ ′ = [κ 7→ λz.p ′], and σκc = [κ 7→ λz.∃x :b. p ∧ p ′],

                                    By IH              σ ′ |= c ′ ↓κ                                             (24)

   Consider any arbitrary c ′′ ∈ c ′ ↓κ.

                        As κ ∈ head(c ′′)              c ′′  ∀x 1 . p1 ⇒ . . . ⇒ ∀x n . pn ⇒ κ(y)               (25)
                                    By 24              σ |= ∀x 1 . p1 ⇒ . . . ⇒ ∀x n . pn ⇒ κ(y)
                                                          ′

                           By Sat-Base                  [] |= ∀x 1 . p1 ⇒ . . . ⇒ ∀x n . pn ⇒ p ′ [y/z]
                            By Sat-Ext              x i :pi |= p ′ [y/z]                                         (26)
                                Trivially,            x :p |= p                                                  (27)
                        Hence, by 26, 27 x :p, x i :pi |= p ∧ p [y/z]   ′

     and so by definition of validity x :p, x i :pi |= ∃x :b. p ∧ p ′ [y/z]
                                    by 25              σκc |= ∀x :b. p ⇒ c ′′

   As the above holds for an arbitrary c ′′ ∈ c ′ ↓κ, we get σκc |= c ↓κ.                                           □

Proof. (Theorem 5.5)

                                             Let    scope(κ, c)  ∀(x :p) ⇒ c ′s.t. κ < p                        (28)
                                 By definition                σ̂κc = σκ     c′

                             By Theorem 5.4                   σ̂κc |= c ′ ↓κ
                   By definition of validity                  σ̂κc |= ∀(x :p) ⇒ (c ′ ↓κ)
                               By Lemma 4.6                   σ̂κc |= (∀(x :p) ⇒ c ′)↓κ
                    By (28) and Lemma 5.1                     σ̂κc |= c ↓κ

                                                                                                                    □

                                Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
26:30                                                                                 Benjamin Cosman and Ranjit Jhala

   Proof. (Theorem 5.6) By Theorem 5.5 it suffices to prove that if σ |= c then σ · σ̂κc |= c ↑κ.
                                                     scope(κ, c)  ∀(y :q) ⇒ c ′s.t. κ < q and σ̂κc = σκc
                                                                                                              ′
                                             Let                                                                   (29)
                                       Assume                         σ |= c                                       (30)
                       By (29), Lemma 5.3                             σ |= ∀(y :q) ⇒ c   ′
                                                                                                                   (31)
                       By Lemma 5.2, (29)                      c ↑κ = ∀(y :q) ⇒ (c ↑κ) ∪ C′
                                                                                                     where κ < C   (32)
                  Hence, by (35) and (37)                     σ · σ̂κc |= c ↑κ
   Case:     σ · σ̂κc |= ∀(y :q) ⇒ (c ′ ↑κ) (35)
                   By (30,32), Lemma 4.7                              σ |= ∀(y :q) ⇒ (c ′ ↑κ)                      (33)
                         Let c ′′ ∈ c ′ ↑κ s.t.                  c ≡ ∀(x i :pi ) ⇒ p and κ < p
                                                                      ′′
                                                                                                                   (34)
                                       By (33)                        σ |= ∀(y :q) ⇒ ∀(x i :pi ) ⇒ p
                                   By Sat-Ext               σ , y :q |= ∀(x i :pi ) ⇒ p
                                       By (31)              σ , y :q |= c ′
                                                            σ , y :q |= σκc (pi ) ⇒ pi
                                                                               ′
     By (29), Lemma 5.7, for i = 1 . . . n
                           As σ̂κc = σκc (29)               σ , y :q |= σ̂κc (pi ) ⇒ pi
                                         ′



    By repeating Lemma 4.2 and κ < p                        σ , y :q |= σ̂κc (∀(x i :pi ) ⇒ p)
                                        That is             σ , y :q |= σ̂κc (c ′′)
                           As by (29) κ < q                           σ |= σ̂κc (∀(y :q) ⇒ c ′′)
                                  Thus, by (34)                       σ |= σ̂κc (∀(y :q) ⇒ c ′ ↑κ)
                       And by Lemma 4.4                       σ · σ̂κc |= ∀(y :q) ⇒ c ′ ↑κ                         (35)
   Case:     σ · σ̂κc |= C (37)
                   By (30, 32), Lemma 4.7                             σ |= C                                       (36)
            As κ < C, domain(σ̂κc ) = {κ}                    σ̂κc (C) = C
                                       By (36)                        σ |= σ̂κc (C)
                             By Lemma 4.4                     σ · σ̂κc |= C                                        (37)
                                                                                                                     □
   Lemma A.1 (Eliminate-Definitions). flat(elim1(κ, c)) = σ̂κc (c ↑κ).
   Proof. (Lemma A.1) The above follows from the observations that: (a) domain(σ̂κc ) = {κ},
(b) elim1(κ, c) = elim∗ (σ̂κc , c), and (c) Lemma 5.8, as domain(σ̂κc ) = {κ}.            □
   Proof. (Theorem 5.9) Let c ′ = elim1(κ, c) = elim∗ (σ̂κc , c). We prove the two directions separately.
   Case: c ′ is satisfiable implies c is satisfiable
           Assume c ′ is satisfiable with                σ ′ |= c ′
                          (by Lemma 4.5)                 σ ′ |= flat(c ′)
                         (by Lemma A.1)                  σ ′ |= σ̂κc (c ↑κ)
                          (by Lemma 4.4) σ ′ · σ̂κc |= c ↑κ                                                        (38)
        (by Theorem 5.5, Lemma 4.3)                σ · σ̂κc |= c ↓κ
                                                     ′
                                                                                                                   (39)
                  By 38, 39, Lemma 4.7             σ ′ · σ̂κc |= c i.e. c is satisfiable.

Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
                                                                                                             26:31

Case: c is satisfiable implies c ′ is satisfiable
       Assume c is satisfiable with             σ |= c
                     by Theorem 5.6         σ · σ̂κc |= c
                       by Lemma 4.7         σ · σ̂κc |= c ↑κ
                       by Lemma 4.4             σ |= σ̂κc (c ↑κ)
                      by Lemma A.1              σ |= flat(c ′)     i.e. by Lemma 4.5 c ′ is satisfiable.
                                                                                                                  □




                              Proc. ACM Program. Lang., Vol. 1, No. 1, Article 26. Publication date: September 2017.
