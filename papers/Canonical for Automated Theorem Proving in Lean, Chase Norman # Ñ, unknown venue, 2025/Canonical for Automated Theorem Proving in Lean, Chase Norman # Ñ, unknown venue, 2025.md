Canonical for Automated Theorem Proving in Lean
Chase Norman # Ñ
Carnegie Mellon University, Pittsburgh, PA, USA

Jeremy Avigad # Ñ
Carnegie Mellon University, Pittsburgh, PA, USA

      Abstract
Canonical is a solver for type inhabitation in dependent type theory, that is, the problem of producing
a term of a given type. We present a Lean tactic which invokes Canonical to generate proof terms
and synthesize programs. The tactic supports higher-order and dependently-typed goals, structural
recursion over indexed inductive types, and definitional equality. Canonical finds proofs for 84% of
Natural Number Game problems in 51 seconds total.

2012 ACM Subject Classification Theory of computation → Automated reasoning; Theory of
computation → Type theory

Keywords and phrases Automated Reasoning, Interactive Theorem Proving, Dependent Type
Theory, Inhabitation, Unification, Program Synthesis, Formal Methods

Supplementary Material Software: https://github.com/chasenorman/Canonical [44]
    archived at swh:1:dir:06a599989bad108dc52bfdff704d356badfa63d4
Software: https://github.com/chasenorman/CanonicalLean [45]
    archived at swh:1:dir:98f9920f9b96cabe1c6188b23fd3823d0ad9fb0f

Funding This material is based upon work supported by the National Science Foundation Graduate
Research Fellowship Program under Grant No. DGE2140739. Any opinions, findings, and conclusions
or recommendations expressed in this material are those of the author(s) and do not necessarily
reflect the views of the National Science Foundation.

Acknowledgements Canonical was developed with the direct support of Tesla Zhang, Cheng Zhang,
Anna Zhang, Linxuan Ma, Asher Kornfeld, Abdalrhman Mohamed, Yue Yao, and Shubham Barghava.


 1     Introduction

Interactive theorem provers (ITPs) like Lean [42], Rocq [6], and Agda [8] are often built on
the foundation of dependent type theory (DTT). In these systems, mathematical structures,
function signatures, and theorem statements are represented as types. Therefore, a procedure
to find terms of a given type in DTT can be directly used for witness/counterexample
generation, program synthesis, and automated theorem proving (ATP).
    The problem of finding terms of a given type is known as type inhabitation. Since DTT
can be used to encode arbitrary mathematical theorems, determining whether a type is
inhabited is undecidable. However, this generality indicates the potential of a sufficiently
powerful type inhabitation solver in accelerating and simplifying formalization.
    Automation in ITPs is accomplished with metaprograms, called tactics. Generally, a
tactic is written to solve goals of a common, but specific, form that projects onto a decidable
and well-understood theory. The tactic applies efficient and specialized reasoning to solve
these goals, and builds a proof term which is not meant to be read by the user.
    A powerful class of automation tools are those which translate a goal into first order logic
(FOL) or higher order logic (HOL), invoke a solver like Vampire [32], and reconstruct the
proof to close the goal. These are referred to as hammers [38, 16, 29, 30, 11]. By design, these
systems can only use the built-in logical connectives, cannot directly reason with dependent
2   Canonical for Automated Theorem Proving in Lean


    types, and cannot synthesize functions or objects constructively. Hammers do not present an
    axiomatic proof term to the user, as such a term would be much too large to be read.
        In this paper, we introduce Canonical, the first solver for type inhabitation in dependent
    type theory. Canonical searches exhaustively for terms of any type involving dependent
    products (Π-types), structure types, inductive types, and let definitions. The algorithm,
    discussed in Section 3, follows similarly to a theoretical account of sound and complete type
    inhabitation in DTT given by Dowek [19], proceeding via iterative refinement. In Section 4,
    we introduce a Lean tactic, canonical, which uses Canonical to find a proof term for the
    main goal. When it finds a proof term, it presents it to the user as a suggested replacement.
    While our implementation is not yet fully general,1 our goal is to approach soundness and
    completeness for the entirety of the Lean language, including definitional equality.
        In Section 5, we demonstrate the performance of our tactic on the Natural Number
    Game for Lean 4 [10]. Canonical achieves an 84% on this benchmark, outperforming all
    existing Lean tactics. Canonical accomplishes this without any native support for natural
    numbers, propositional equality, logical connectives, or any other Lean definitions, and is
    instead provided the direct DTT representation at runtime. As such, these capabilities extend
    to user-defined datatypes and axiom schemas. We specifically highlight the higher-order
    reasoning and program synthesis capabilities of Canonical and show examples involving
    indexed inductive types and generalized induction.


        2     Examples
    With each of the following example Lean statements we include a comment showing the
    invocation to Canonical that generated the proof term. The numeric argument is an optional
    timeout parameter, in seconds; we include it here to indicate a bound on the time that
    sufficed to generate the proof.

    Propositional Logic

        example : ( A ∧ ¬A ) → B :=
          -- by canonical 1
          fun a 7→ False . rec ( fun t 7→ B ) ( a . right a . left )

    Like other specialized tactics, Canonical is capable of reasoning with propositional connectives.
    The proof demonstrates how to use the eliminator for False as the principle of explosion, as
    well as how to project out of the And type. Canonical searches for proofs at increasing depth
    levels, so it typically finds a simple proof. Unless explicitly provided with double negation
    elimination, the proof will be constructive.

    Cantor’s Theorem

        theorem Cantor ( f : α → Set α) : ¬Surjective f :=
          -- by canonical 1 [ false_of_a_eq_not_a , congrFun ]
          fun a 7→ Exists . rec ( motive := fun t 7→ False )
            ( fun w h 7→ false_of_a_eq_not_a ( congrFun h w ))
            ( a fun a 7→ f a a → False ) -- { a | a ∈ / f a }



    1
         Specifically, we do not translate quotient types or universe levels; see Section 4.
C. Norman and J. Avigad                                                                          3


Cantor’s theorem states that all functions from α to the power set of α are not surjective.
Canonical generates a proof of this theorem given false_of_a_eq_not_a, a Mathlib [36]
lemma stating that a proposition cannot be equal to its negation, and congrFun, a standard
library lemma stating that two equal functions are equal on any input. The generated proof
follows the textbook proof, including the construction of the Cantor diagonal set in the
last line.

Type-Directed Program Synthesis

inductive Vec (α : Type ) : Nat → Type u where
| vnil : Vec α 0
| vcons : α → { n : Nat } → Vec α n → Vec α ( n + 1)

noncomputable def append : Vec α n → Vec α m → Vec α ( m + n ) :=
  -- by canonical 1
  fun a a_1 7→ Vec . rec ( motive := fun a t 7→ Vec α ( m . add a ))
    a_1 ( fun a { n } a_2 a_ih 7→ Vec . vcons a a_ih ) a

    Canonical is not limited to proving propositions. In this example we have an indexed
inductive type Vec α n, representing vectors of length n with elements of type α. Canonical
is able to synthesize the append function using only the type signature, due to the enforced
length constraints. The definition must be marked “noncomputable” in Lean because the
code generator presently cannot compile recursors. If the return type Vec α (m + n) is
changed to Vec α (n + m), Canonical will instead generate the function that appends the
vectors in the reverse order.

Foundations

theorem Eq . trans { a b c : α} ( h 1 : Eq a b ) ( h 2 : Eq b c ) : Eq a c :=
  -- by canonical 1
  Eq . rec ( motive := fun a_1 t 7→ a = a_1 ) h 1 h 2

    Canonical operates directly on the DTT representation at the foundations of Lean,
including for essential notions like equality. So, Canonical can prove theorems like the
transitivity of equality from first principles. Canonical has no special treatment of equality
or any other constant in Lean.

Generalized Induction

theorem List . recGen ( motive : List α → List α → Prop ) : · · · :=
  List . rec ( motive := fun x 7→ ∀ y , motive x y )

theorem reverse_reverse ( as : List α) : as . reverse . reverse = as :=
  -- by canonical 1 + synth [ List . recGen ]
  List . recGen
    ( fun a a_1 7→ ( a . reverseAux a_1 ). reverseAux [] = a_1 . reverseAux a )
    ( fun y 7→ Eq . refl ( y . reverseAux []))
    ( fun head tail a y 7→ a ( head :: y )) as []

    Canonical’s induction ability is driven not by dedicated support, but rather by a general
inhabitation procedure for DTT. It can therefore extend to more complex induction schemes
like generalized induction, where the inductive hypothesis is strengthened to universally
4   Canonical for Automated Theorem Proving in Lean


    quantify over a term. In this example, we provide Canonical with the generalized induction
    principle for lists, and it proves that list reversal is an involution. Note that Canonical
    is intelligent enough to recognize that this proof must involve reasoning about the helper
    function reverseAux rather than about reverse directly. The synth flag, discussed in
    Section 3.3.1, is necessary for Canonical to use an induction predicate that is only equal to
    the goal type under iota reduction.



    Higher-Order Logic


     theorem sSup_inter_le [ CompleteLattice α] { s t : Set α} :
       sSup ( s ∩ t ) ≤ sSup s ⊓ sSup t :=
       -- by canonical 20
       sSup_le ( fun a 7→ s a ∧ t a )
         ( Lattice . inf ( sSup fun a 7→ s a ) ( sSup fun a 7→ t a ))
         fun b a 7→ Lattice . le_inf b ( sSup fun a 7→ s a ) ( sSup fun a 7→ t a )
            ( le_sSup ( fun a 7→ s a ) b ( And . left a ))
            ( le_sSup ( fun a 7→ t a ) b ( And . right a ))


        Beyond generalizations of induction, Canonical is able to synthesize functions to invoke
    arbitrary higher-order premises. In this example we prove that for any two sets s and t
    of elements from a complete lattice, the supremum of (s ∩ t) is less than or equal to the
    minimum between the supremum of s and the supremum of t. sSup is a higher order function,
    and sSup_le and le_sSup are higher order axioms of complete lattices.



    Multiple Inhabitants


    class Group ’ (α : Type u ) extends Semigroup α, Inv α where
      one : α
      one_mul : ∀ a : α, one * a = a
      inv_mul_cancel : ∀ a : α, a - 1 * a = one

     example [ Group ’ α] : MulHom α α :=
       -- by canonical 1 ( count := 5)
       ⟨ fun a 7→ a , fun x y 7→ Eq . refl ( Mul . mul x y ) ⟩
      ···
       ⟨ fun a 7→ Group ’. one , fun x y 7→ Eq . rec
          ( motive := fun a t 7→ a = Mul . mul Group ’. one Group ’. one )
          ( Eq . refl ( Mul . mul Group ’. one Group ’. one ))
          ( Group ’. one_mul Group ’. one ) ⟩


       Since Canonical searches over inhabitants of a goal type, it can also be used to find
    multiple inhabitants. In this example, we use Canonical to find the two endomorphisms
    that exist over all groups – the identity map and the constant function which returns the
    identity element. Using the count flag, we obtain five inhabitants with two shown above.
    We use a simplified group definition, Group’, to avoid reasoning about auxiliary notions like
    exponents.
C. Norman and J. Avigad                                                                                          5


    3      Canonical
3.1         Format
The first step toward creating a search procedure for DTT is to define the format for
representing terms and types. The format must be expressive enough to represent the
complexity of a language like Lean, while also maintaining structural properties necessary
for efficient search.
    All terms in Canonical are β-normal and η-long (BNEL). This means there are no
reducible expressions, such as (λ x. x) a, and all references to functions must be fully applied
(so, a unary function f is written as λ x. f x). As such, all terms appear in canonical form
and Canonical will only search over terms in canonical form. A term in Canonical has only
one constructor, consisting of a list of parameter bindings, a list of let declarations, a head
symbol, and a list of arguments:

        λ x. let y := M . f A                                                                             (1)

Note that with this definition, we have direct access to the head symbol of any term. The
variables x and let declarations y are in a simultaneous declaration, such that they may
depend on each other in any order, including circularly.2 The variable f must be bound by a
lambda binding or let definition in the term’s local context. A type in Canonical also has
only one constructor, which is a term annotated with types for each of its bound variables:

        Π x : X. let y : Y := M . g B                                                                     (2)

The types X and Y again may depend on any of the bound variables x and y. This
system is similar to the Logical Framework [24], although without universes. The let
definitions are not essential for understanding the theory, but are used to encode constant
symbols, reducible expressions, and let expressions from Lean. For bound variable f of type
Π a : Z. let y ′ : Y ′ := M ′ . h C, we say that the term in line 1 has the type in line 2 when:

        (h C)[A[M /y]/a][M ′ /y ′ ] =β (g B)[M /y]                                                        (3)

and when each of the arguments Ai has the correct type:

        Ai [M /y] : Zi [A[M /y]/a][M ′ /y ′ ]                                                             (4)

using the standard notion of substitution and definitional reduction. Canonical accepts a type
as input, and returns terms of the input type as output. For convenience, type declarations
for bound variables are optional. If the type is omitted, this indicates that Canonical should
not use the variable in constructing a term. The term inside a let definition may also be
omitted, in which case the binding is treated as a constant symbol. To support more complex
reductions, let definitions can be tagged with auxiliary reduction information. This includes
the reduction rules for each recursor or the index of a field accessed by a projection function.
    The most important property of this format is static arity. From only the type signature
of a variable, we can determine the number of parameters it must be supplied. This property
does not hold in Lean, as the type signature can contain definitions that expand to reveal
more parameters (as with Not or Set), or the number of parameters can change (such as
when the polymorphic identity function id is specialized to a function type).


2
    It is the responsibility of the encoding system to provide Canonical with a signature that is type-correct
    in the target language, such that this circularity is not inconsistent.
6   Canonical for Automated Theorem Proving in Lean


    3.2     Refinement
    Canonical builds a term starting from a single metavariable (which can be thought of as
    a “proof hole”). At each step, we pick an unassigned metavariable, select a variable from
    its local context to be its head symbol, and create new metavariables for the arguments
    to that head symbol. This operation is called a refinement. We continue refining until all
    metavariables are assigned.


            ?A←f             ?C←g
       ?A =⇒ (f ?B ?C) =⇒ (f ?B (g (λ x y. ?D)))
       ?B←a                           ?D←x
          =⇒ (f a (g (λ x y. ?D))) =⇒ (f a (g (λ x y. x)))

       Figure 1 An example refinement sequence.


        We know the number of new metavariables needed to fully apply the head symbol by the
    static arity property. We can also eagerly insert the correct number of lambda bindings where
    necessary using the static arity property, ensuring that our generated term is η-expanded.
        It is quite important that all metavariables in the application are generated at once, such
    that Canonical may refine them in an arbitrary order. While synthesizing the arguments
    sequentially would guarantee that the type of the following metavariable is fully specified (as
    all metavariables it depends on have been assigned), we often prefer to synthesize arguments
    in the reverse order. This way, the values of the earlier metavariables is constrained through
    unification.
        We associate with each metavariable a typing constraint. The type of the starting
    metavariable is constrained to be definitionally equal to the goal type. Consider the case
    of a metavariable ?M with the type in line 2 being refined by function symbol f of type
    Π a : Z. let y ′ : Y ′ := M ′ . h C. Let ?A be the newly created metavariables to apply f . We
    generate the following equational constraint to match line 3:

       (h C)[?A[M /y]/a][M ′ /y ′ ] =β (g B)[M /y]                                              (5)

    and the following typing constraints for the newly created metavariables matching line 4:

       ?Ai [M /y] : Zi [?A[M /y]/a][M ′ /y ′ ]                                                  (6)

    at which point the original typing constraint becomes inactive. If we find that one of
    our equational constraints is violated, we immediately backtrack the refinement decision,
    reactivate the original typing constraint, and continue along another path. We do not need
    to backtrack the choices of metavariable, only the choices of head symbol, since a given term
    can be obtained by any ordering of metavariable refinement. The local context of a new
    metavariable ?Ai consists of the local context of ?M appended with the bound variables on
    the right hand side of the typing constraint in line 6.


    3.3     Explicit Substitutions
    How we determine whether an equational constraint has been violated is at present under-
    specified. In lines 5 and 6, we have made frequent use of substitutions on terms containing
    metavariables. The expression ?Ai [M /y], for instance, cannot be evaluated under the stand-
    ard definition of substitution, as it has not yet been determined whether ?Ai uses the variables
C. Norman and J. Avigad                                                                                 7


in y. Indeed, this fact may change over the course of the algorithm as ?Ai is backtracked and
reassigned. Even worse, a simple equational constraint with an application:

   (λ x. f ?X) a =β b                                                                            (7)

cannot be reduced as it is not clear whether ?X contains x. It is essential that the algorithm
be able to observe that this equation is violated since f and b are not equal, so that we may
cut the branch and backtrack. Canonical depends on the ability to determine whether an
equational constraint has been violated as early as is possible, so that we only search over
partial terms that are type correct.
    To support this, Canonical internally uses the calculus of explicit substitutions [1, 43, 20].
All terms and types in Canonical are de Bruijn indexed [17]. To determine what a de Bruijn
index refers to, we accompany all terms with an explicit substitution, which maps de Bruijn
indices to variables or other terms with an explicit substitution. For example, we may write
the term (λ x. f ?X) a in the following way:

   ⟨0 1, [⟨λ 1 ?X, [f ]⟩, a]⟩

The first component, 0 1, indicates that we should apply the first element of the explicit
substitution ⟨λ 1 ?X, [f ]⟩ to the subterm ⟨1, [⟨λ 1 ?X, [f ]⟩, a]⟩, which denotes the term a in this
explicit substitution. To β-reduce this, we extend the explicit substitution of the function,
[f ], with the argument(s):

   ⟨1 ?X, [⟨1, [⟨λ 1 ?X, [f ]⟩, a]⟩, f ]⟩

This operation can be performed in constant time with respect to the size of the terms
and the number of arguments. Furthermore, β-reduction never creates new terms, only
appending existing terms to existing explicit substitutions. If the first component of this
term is a metavariable, β-reduction cannot continue and we say the reduction is stuck. The
let definitions from the input format encode nicely into this representation, simply extending
the explicit substitution with each definition term.
    Using explicit substitutions, we can represent substitutions on metavariables and applica-
tions on partial terms. For any term in this system, we can either determine the head symbol
and arguments of that term or reduction is stuck on a metavariable. If neither side of an
equation is stuck, we can check if the head symbols on either side are equal. If they are not
equal, we report that the equation is violated. Otherwise, we propagate the equation into
equations of the subterms:

   f M =β f N =⇒ Mi =β Ni for all i

When a metavariable is refined, we reduce the equations that are stuck on that metavariable.
When this refinement is backtracked, we recover the original equation. We say a metavariable
has an equation if the equation is stuck on that metavariable.

3.3.1     Equations
Canonical does not have a dedicated unification procedure or domain-specific reasoning, so
equational constraints are the only guidance that the search has. It is therefore critical that
we determine how best to glean information from them. We call an equation rigid if, when it
is fully reduced, it has one side which is not stuck on a metavariable. Only rigid equations
can directly constrain the search, as otherwise there are two degrees of freedom.
8   Canonical for Automated Theorem Proving in Lean


       As mentioned previously, Canonical also contains reduction rules for let definitions,
    recursors, and projections. This leaves an important question as to whether the following
    equation should be considered violated or stuck:

       Nat.rec a (λn h. b) ?t =β a

    While both sides have reduced to a head symbol, we cannot be sure that the major argument
    to the recursor ?t will not be assigned to 0, causing the term on the left hand side to
    reduce to a. For completeness, it is necessary to consider the equation stuck. However, if
    this equation is not allowed to constrain the search, then Nat.rec becomes a valid head
    symbol for almost any metavariable, as it projects into any type and does not cause equation
    violations.
        By default, Canonical considers such equations to be violated, which is generally the
    desired behavior for type-directed problems like theorem proving. However, Canonical
    additionally provides a program synthesis mode where these equations are considered stuck,
    so it can synthesize functions that speculatively use recursors and projections even in
    situations where there are rigid equations. Additionally, Canonical is always forbidden from
    using a constructor as the head symbol of the major argument of a recursor or projection, as
    the resulting term would not be in canonical form.

    3.4     Search
    Canonical uses iterative deepening to exhaustively search for terms. Rather than directly
    searching in increasing order of tree depth, we use a metric which we call entropy. Entropy
    is high for partial terms that we expect are difficult to complete. By searching in this order,
    we consider more promising branches before less promising ones.
        Beginning with a certain entropy threshold, we perform depth-first search (DFS) to search
    through all paths below the threshold. If we anticipate that the branches from a node will
    be large, we can add them as jobs to be completed asynchronously with fork-join parallelism.
    We maintain a sufficient number of jobs such that all CPU cores are utilized on independent
    branches of the search tree.
        We use iterative-deepening DFS so that refinement may be performed by directly mutating
    the assignment of a metavariable, rather than updating a persistent data structure. The
    cost of this is that we must retrace the steps of the prior levels each time we increase the
    entropy threshold. To mitigate this, we choose the threshold such that each level searches
    twice as many nodes as the previous. If this factor were smaller, there would be too much
    overhead from the redundant searching of prior levels. If it were larger, we might overshoot
    the number of steps necessary to find the proof term by a significant amount. This factor
    of 2 minimizes the product of these effects.

    3.4.1    Entropy
    We compute our custom entropy metric separately on each metavariable of a partial term.
    We then define the entropy of the partial term to be the product of the entropy of all of
    these metavariables. The metavariables of a partial term can be split into two groups: those
    which have already been refined and those which have yet to be refined. We treat these two
    groups differently from the perspective of entropy computation.
        The entropy of an already refined metavariable is equal to the number of potential
    refinements we could have chosen for that metavariable, i.e. the branching factor at that
    point in the tree search. The rationale behind this is that for a branching factor b, we
C. Norman and J. Avigad                                                                           9


can only dedicate a 1/b fraction of our computational resources to each branch, making it
more difficult to find a proof term. The result is that we penalize partial terms under large
amounts of branching decisions, and prioritize partial terms with more forced moves that
represent a larger fraction of the entire search tree. This strategy is also employed by sauto
in Rocq [15].
    For the metavariables that have yet to be refined, we would like the entropy to be
an estimate the number of refinements that it will take to completely solve them. Under
the assumption that these metavariables are independent, the total refinement count to
complete this branch will be the product of the individual refinement counts. To perform
this estimate, we take advantage of the fact that our search has likely seen many similar
metavariables in the past. While each metavariable may have a unique type and local context,
we can bin metavariables into groups based on properties that have a small, finite number of
combinations. Canonical bins metavariables according to whether they have a rigid equation,
and their type ignoring the explicit substitution, representing the type in the original input
program that this metavariable derives from. Each time a recursive DFS call returns, we
accumulate search information about the metavariable being refined, such as the number
of refinements performed on it or its children, whether the metavariable was successfully
completed, or whether all branches resulted in an equation violation. After each iteration of
the iterative-deepening search, we accumulate the statistics from all of the threads into the
statistics used for entropy calculation.
    Armed with these statistics, we can now compute the entropy for a metavariable that has
not been refined. First, we determine the probability that this metavariable will obtain a
rigid equation by the time it is refined, by comparing the count of entries in its bin against
that of the equivalent bin for identical metavariables but with a rigid equation. We consider
metavariables with a rigid equation to have entropy 1, as their value is essentially determined
by the rigid equation. If a metavariable has probability p to gain a rigid equation, we take a
weighted average of 1 with weight p and the average number of refinements per completed
metavariable in its bin with weight 1 − p. We bound the entropy of a metavariable by 1,000
to prevent branches from becoming so penalized that they are never explored.
    We similarly bin metavariables that have been refined in order to collect statistics about
how often the refinement leads to a successful completion of the metavariable. We add
an additional penalty to the subterm of a refined metavariable that infrequently leads to
successful completions, which is removed if a completion is found. Taking the product of the
entropy values of refined metavariables and metavariables that are not refined defines the
total entropy for the partial term.

3.4.2    Metavariable Ordering
At each node in the DFS tree, we must decide which metavariable to attempt the possible
refinements on. This decision does not need to be backtracked, as any completed term can be
created by refinements of the metavariables in any order. However, it is quite important that
we choose a good ordering, as it can have drastic effects on the search tree. We call this the
metavariable ordering problem, from the similar “variable ordering” problem in constraint
satisfaction problems [9].
    In general, we would like to refine metavariables that occur later in the partial term
first, since the types of later metavariables are permitted to depend on the values of earlier
metavariables in DTT. It is typically much easier to refine the later metavariable and
determine the value of the earlier metavariable by unification than it is to search over values
for the earlier metavariable and check if each allows inhabitants of the later metavariable.
10   Canonical for Automated Theorem Proving in Lean


     As an example, consider a metavariable ?n : Nat and another ?p : ?n = 1000. We would
     much prefer to refine ?p to refl and therefore determine that ?n must be 1000 than to iterate
     over natural numbers n and attempt proofs of n = 1000 for each. It is therefore essential
     that our explicit substitution calculus allows us to refine metavariables in an arbitrary order,
     even when the metavariables in the type of another have yet to be assigned.
         Beyond this, our priority is to terminate this search branch as quickly as possible, in
     the fail-fast style of SAT solving [7]. We unconditionally refine metavariables with rigid
     equations, as they usually either have a single refinement or no refinements at all, terminating
     the branch. Furthermore, this propagates the equation potentially generating constraints
     on other metavariables. This is the equivalent of unit propagation in SAT solving. If no
     metavariables have rigid equations, we look for a metavariable with a high probability of
     having no valid refinements, using the metavariable’s statistics.
         Barring the rare case of an immediately terminating branch, the only way to stop the
     search is by increasing the entropy of the partial term as quickly as possible, to convince
     the DFS that the branch is unpromising. To do this, we prioritize metavariables with high
     entropy, as they likely are the most difficult to solve and harbor child metavariables with high
     entropy which accelerate the branch toward termination. If a metavariable has sufficiently
     high entropy, we prefer it over a metavariable that occurs later in the partial term but with
     less entropy. So, when selecting variables for refinement, we prefer selections that keep the
     entropy low, and when selecting the metavariable to refine, we prefer selections that increase
     the entropy as fast as possible.

      4      Lean Tactic
     Canonical is a Rust program, which is linked to Lean via the Foreign Function Interface. For
     structures in the input format of Canonical (subsection 3.1), like terms and types, we create
     equivalent structures in Lean:
            structure Term where                      structure Typ where
                params : Array Var                        params : Array ( Option Typ )
                lets : Array Let                          lets : Array ( Option Typ )
                head : String                             codomain : Term
                args : Array Term

          Translating a Lean Expr into these structures proceeds by pattern matching on the Expr:
      inductive Expr where
        | forallE : Name → Expr → Expr → BinderInfo → Expr
        | lam : Name → Expr → Expr → BinderInfo → Expr
        | letE : Name → Expr → Expr → Expr → Bool → Expr
        | app : Expr → Expr → Expr
        | fvar : FVarId → Expr
        | const : Name → List Level → Expr
        | sort : Level → Expr
        ...

         The forallE constructor represents Pi types, function types, universal quantification, or
     implication. When translating into a Typ we append forallE bindings to params, with the
     parameter Typ being the recursive translation of the type of the forallE binding. Likewise,
     lam represents a lambda expression. When translating into a Term, we append lam bindings
     to params. Let definitions, with the constructor letE, are treated similarly but are added to
     lets, and their definition is recursively translated into a Term.
C. Norman and J. Avigad                                                                             11


    The app constructor represents the application of a function expression to an argument
expression. When translating (app e1 e2 ), we append the translation of the argument e2
to args, and continue translation on the function expression e1 . Finally, once a constant
symbol (const) or free variable (fvar) is reached, we set head to the name of the symbol,
and return the complete Term.
    There are a number of additional considerations in this translation. If we encounter
a lambda expression inside the function Expr of an application (i.e. we are translating a
β-redex), we pair the lambda binding and latest applied argument as a let expression. For
example, this translates (λx. x) y into let x := y. x, preventing pervasive reduction while
remaining in BNEL form.
    Canonical has no built-in object-theoretic notion of Sort. We add a let definition at
the top level for Sort with no implementation and type Sort. This is similar to Lean’s
judgment Sort u : Sort (u + 1), but removing the universe level annotation. In some
circumstances this leads to unsoundness by Girard’s paradox, but in practice we have not
seen Canonical solve a goal in this way. When we encounter a Nat or String literal, we
create a let declaration to represent it, with the appropriate type. Due to the size of literals,
we generally do not include a definition for the let declaration, unless it is a natural number
less than or equal to 5. In this case, we provide a definition in terms of the constructors
of Nat.


4.1    Arrow Types
When translating a term, if we encounter a forall expression (a : A) → B a, we convert it to
Pi A (λa. B a) for the following definition of Pi:

 structure Pi ( A : Type u ) ( B : A → Type v ) where
     f : (a : A) → B a


   When we reach a constant symbol or free variable, we check the number of applied
arguments against the arity of the symbol. Since Lean does not have static arity, we choose
the minimum arity, which is the number of forall expressions in the type of the symbol. If
fewer arguments were supplied than are necessary, we η-expand by adding parameters and
supplying those as arguments until the symbol is fully applied. If more arguments were
supplied than the arity, this implies that the return type of the function was a Pi type. So,
we convert the applications of the excess arguments into invocations of Pi.f. We also ensure
that each argument supplied to the constant symbol or free variable has the correct arity. If
an argument has fewer parameters than necessary, we add new parameters which become
arguments on its head symbol. If an argument has more parameters than necessary, the
argument must be a Pi type. So, we replace the innermost arguments with an application to
Pi.mk. As an example of these translations, we translate id (A → B) f a to:

   Pi.f A (λa. B) (id (Pi A (λa. B)) (Pi.mk A (λa. B) (λx. f x))) a

    Unnecessary uses of Pi negatively affect the performance of Canonical. So, we pervasively
unfold definitions that alias a forall expression. For example, Set α is unfolded to its
definition α → Prop and Not P is unfolded to its definition P → False. In this way, they
will be translated to native Π-types in Canonical where possible. We also unfold reducible
definitions and typeclass instances to reduce the complexity of the generated problem.
12   Canonical for Automated Theorem Proving in Lean


     4.2      Definitions
     As discussed in Section 3.1, all constant symbols used by Canonical must be included as
     top-level let declarations. As such, we must add a let declaration when we encounter a
     constant symbol for the first time. If the constant symbol is a definition, we recursively
     translate the definition and include it in the let declaration.
         In general, if we provide a let declaration with a definition, it is inadvisable to allow
     Canonical to use the let definition in a proof. This is because it allows for redundant ways
     of expressing the same term, by either using the let declaration or rewriting its definition.
     For instance, we do not provide a type for the let declaration let 0 := Nat.zero as this
     would allow Canonical to write 0 in two distinct ways. However, we choose to provide the
     type of any let declaration that uses a recursor or auxiliary recursor, as these definitions are
     a suitably complex abstraction. If a constant symbol is only used in the definition of a let
     declaration, we do not provide it a type as it is not directly relevant to the problem.
         For constant symbols with special reduction behavior, like recursors, projection functions,
     and constructors, we annotate the associated let declaration with information about the
     reduction. For instance, we recursively translate the reduction rules for recursors on inductive
     types. Whenever we define an inductive type (resp. structure type) we automatically define
     the constructor(s) and recursor (resp. projection functions).
         We also automatically add all declarations in the local context of the main goal as let
     declarations. Users may supply additional constant symbols to be defined in square brackets.
         It is important to emphasize that the recursive translation of constant symbols and their
     definitions continues until primitive declarations are reached. This can violate abstraction
     barriers and lead to an explosion in the number of declarations if, for instance, real numbers
     are used. Deciding on which definitions to include is a question of relevance filtering and
     is beyond the scope of this work. We currently use a faithful recursive translation for
     completeness, but it is straightforward to limit the definitions that Canonical receives.


         5    Results
     It is a rite of passage for many Lean beginners to play the Natural Number Game. This
     Lean tutorial involves proving elementary properties of natural numbers in 79 “levels” over 9
     “worlds” about topics like addition, multiplication, exponentiation, and inequalities. The game
     introduces a number of essential Lean tactics, with proofs involving induction, equational
     rewrites, and propositional logic.
         We have composed a Lean file with the 74 unique statements proven in the Natural
     Number Game.3 The Natural Number Game uses a custom definition of natural numbers
     and the operations on them for pedagogical reasons. Our file instead uses the Lean standard
     library definition of Nat to allow fair comparison with tactics that have dedicated Nat logic,
     to more accurately represent real use cases, and to allow definitional reduction of some
     functions that the Natural Number Game defines axiomatically. It is important to note
     that Canonical does not have specialization toward natural numbers or equality, and indeed
     (automatically) receives the inductive definition of these types separately with each problem.
         The Natural Number Game was chosen as a benchmark because it has a mixture of
     propositional, first-order, and higher-order reasoning problems. On first-order problems,
     we can observe the capabilities of Canonical compared to tools dedicated towards this


     3
         Some statements are duplicated to showcase the use of specialized tactics.
C. Norman and J. Avigad                                                                          13


task. On higher-order problems, we can observe the benefits of the generality of Canonical.
Furthermore, the statements in the Natural Number Game involve simple objects that are
close to the foundations of Lean, and therefore admit reasonably short proof terms. In
general, the Natural Number Game represents a basic level of proficiency with the Lean
language.
    We have manually selected the premises required to solve each problem and have supplied
them to each tool. In most cases, these are derived from the reference solutions and consist
of theorems proven in earlier levels. However, we must occasionally provide theorems from
the standard library, such as Nat.le.intro and Nat.le.dest which convert between the
standard library definition of ≤ and the one used in the natural number game. Canonical
additionally requires Classical.byContradiction for one level in which a proof by contra-
diction is required. A number of problems require induction where the induction predicate is
an implication. To allow canonical to represent implications, as they are written in Lean as
arrow types, we provide Canonical with the following definition of If in these levels, similar
to the definition of Pi in Section 4.1:
 structure If ( a b : Prop ) : Prop where
   h : a → b

   We compare against Lean tactics Aesop [33] and Duper [12]. Since Aesop can use simp [42],
we manually removed the simp attribute from Lean standard library theorems about natural
numbers until after the associated level in the game where that theorem is proven. Duper
requires that the definitional reduction rules be provided as propositional equalities, so we
provide these where necessary. All of our experiments are performed on a Mac Mini with M4
Pro and 24GB of RAM. We use Lean and Mathlib version 4.16.0, and Duper version 0.0.23.
We use the default options for Aesop, portfolio mode for Duper, and we provide Canonical a
timeout of 15 seconds.

   Table 1 Natural Number Game problems solved by each tactic, separated by world.

             Tut    Add    Impl    Mul    Algo   Add2    Pow    LEQ     Mul2       Total
 Canonical   6/6    5/5    10/10   9/9    6/7     6/6    7/10   7/11    6/10    62/74 (84%)
  Aesop      6/6    0/5     9/10   0/9    4/7     0/6    2/10   5/11    1/10    27/74 (36%)
  Duper      6/6    1/5     9/10   4/9    7/7     4/6    5/10   5/11    4/10    45/74 (61%)


    Table 1 shows the problems solved by each tactic, separated by world. Aesop solves 36%
of the problems, Duper solves 61%, and Canonical solves 84%. This difference is primarily
because Aesop and Duper are not intended to perform induction, and were not able to solve
any problems requiring it. The first problem that Canonical fails on is in the Algorithm
world:
example ( a b c d e f g h : Nat ) :
( d + f ) + ( h + ( a + c )) + ( g + e + b ) = a + b + c + d + e + f + g + h

    Canonical cannot use tactics, and therefore cannot solve this problem in the intended
manner with simp. Solving this problem therefore requires too a large number of Eq.rec
invocations. Duper, with special support for equational reasoning, can solve this problem.
Requiring too many invocations of induction or generalized induction is the most common
reason that Canonical did not solve a problem. Several problems also are affected by the
incompleteness in our handling of iota reduction (see Section 3.3.1), causing Canonical to be
unable to solve some problems that admit a short proof.
14   Canonical for Automated Theorem Proving in Lean


         In total, Canonical takes 51 seconds to generate the 62 proofs. Only 9 proofs take longer
     than a second. While solving these 9 problems, Canonical attempts an average of 23 million
     refinements per second, with 2.1 million per second not resulting in a violated equation. Of
     these, an average of 1.2 million refinements per second resulted in a partial term still below
     the entropy threshold, triggering a recursive DFS call. The average branching factor is 1.6,
     owing to the fact that most metavariables are solved by unification (rigid equations). On
     these 9 problems, the final iteration of iterative deepening accounts for only 17% of solve
     time, suggesting a bias for proofs to be found early in an iteration.
         We computed the length of the proofs generated by each tactic by counting the number
     of constant symbols, free variables, bound variables, sorts, literals, and projections in the
     term, excluding the types of lambda and let bindings. On problems where both Duper
     and Canonical found a proof, the proof found by Canonical was on average 251x shorter.
     For Aesop, the proofs found by Canonical were on average 18x shorter. On top of this,
     Canonical only uses constant symbols provided to it or those needed to define the problems
     statement. Aesop and Duper make frequent use of custom, domain-specific constant symbols.
     For instance, Aesop would use lemmas about subtraction when subtraction is not a part of
     the Natural Number Game. We see a potential use case for Canonical in proof minimization
     and repair for these reasons.
         We have also tested Canonical on definitions from the Prelude of the Lean standard library.
     These problems are generally not in scope for other tools, as they are often not propositions
     and they require reasoning directly about the inductive definitions of types in advance of
     basic lemmas being proven. For non-propositions, we generate multiple inhabitants using the
     count option, and consider Canonical to have solved the example if one of the inhabitants
     is definitionally equal to the standard library implementation. We also supply proofs that
     constructors of an inductive type are disequal to each other, in lieu of noConfusion. Of the
     first 50 statements in the library, Canonical solves 46 (92%). Three failures are caused by
     our tactic not encoding the eta rules for structures, and one is caused by our incompleteness
     with respect to iota reduction. A selection of terms generated by Canonical are shown below.
     theorem eq_false_of_ne_true :
       { b : Bool } → Not ( Eq b true ) → Eq b false :=
       -- by canonical 3 [ Pi ]
       fun { b } a 7→ Bool . rec ( motive := fun t 7→ b = t → t = false )
          ( fun a 7→ Eq . refl false )
          ( fun a_1 7→ False . rec ( fun t 7→ true = false ) ( a a_1 ))
          b ( Eq . refl b )

     instance Pi . instNonempty {α : Sort u } {β : α → Sort v }
       [( a : α) → Nonempty (β a )] : Nonempty (( a : α) → β a ) :=
       -- by canonical 1 [ Nonempty . intro , Classical . ofNonempty ]
       Nonempty . intro fun a 7→ Classical . ofNonempty

     theorem decide_eq_true [ inst : Decidable p ] :
       p → Eq ( decide p ) true :=
       -- by canonical 1
       fun a 7→ Decidable . rec ( motive := fun t 7→ decide p = true )
           ( fun h 7→ False . rec ( fun t 7→ false = true ) ( h a ))
           ( fun h 7→ Eq . refl true ) inst

     def ite {α : Sort u } ( c : Prop ) [ h : Decidable c ] ( t e : α) : α :=
       -- by canonical 1 ( count := 5)
       Decidable . rec ( motive := fun t 7→ α) ( fun h 7→ e ) ( fun h →
                                                                      7 t) h
C. Norman and J. Avigad                                                                               15


 6     Related Work
There are a number of existing theorem proving systems that are based on type inhabitation.
There are sauto [15] for Rocq, Agsy [35], Mimer [52], and Auto [31] for Agda, and TWELF [51]
for the Logical Framework [24]. An essential subroutine for these systems is unification, in
which two terms with existentially quantified variables are made equal to each other by a
substitution on those variables. An algorithm for first-order unification was described by
Robinson in 1965 [49]. In the higher-order setting, unification can have multiple (or infinitely
many) solutions and is undecidable [25, 22]. Nonetheless, Huet provided a procedure to
enumerate higher-order unifiers in 1975 [26]. To date, no theorem provers use this algorithm on
account of its inefficiency, and instead elect for decidable and efficient pattern unification [39]
(or extensions thereof, e.g. [2]). In particular, the restriction to pattern unification ensures
that the solutions to unification problems are unique. While this handles many common
cases, this means that these systems cannot perform general higher-order reasoning, such
as the synthesis of induction predicates. Beyond this, these systems are not designed to
handle the complexity of problems we are interested in solving with Canonical, such as those
involving definitional equalities and requiring several nested recursors.
    Some tools offer similar functionality for specialized use cases. ELPI [23] is an interpreter
for the higher-order logic programming language λProlog for use in elaboration and type
inference of programming languages. It uses the higher-order capabilities of λProlog to
instantiate metavariables in some cases, but is not intended for theorem proving on its own.
An extension of the program synthesis tool Herb to dependent types [28] can write simple
recursive programs using goal-directed search with pattern unification. The Theorem Proving
System [3] has native support for simple type theory as well as first-order logic, and is able
to prove a wide range of theorems with this capability.
    While these systems all have type theory support, they each sacrifice completeness or
generality in some way. The only account of a complete search procedure for dependent type
theory was given by Dowek [19]. Our algorithm is conceptually that of Dowek, although
we use a custom explicit substitution representation for performance. To our knowledge,
Dowek’s algorithm has not been implemented.
    The most common approach for ATP in proof assistants is called a hammer. In these
systems, a goal is monomorphized into first-order logic [37, 14] which is then fed to a first-
order theorem prover [32, 54, 50] or SMT solver [41, 5]. If the statement holds, a proof
reconstruction tool builds a proof in the target language, often by re-proving the goal with a
proof-producing first-order solver [27, 12]. This approach has been successful in languages
that are built on higher-order logic [38, 29, 30] but has also been implemented in Rocq [16]
and Metamath [11]. These tools are adept at solving goals in the first-order fragment of
the target language. There are also standalone tactics that invoke SMT solvers to solve
first-order goals [40, 21].
    An entirely different class of ATP system are those that search over tactic proofs.
Aesop [33] performs such a search in Lean using hand-tuned heuristics. More recently, Large
Language Models have been used to predict tactics [18, 34, 53, 56, 55]. Since Canonical can
be invoked via a Lean tactic, we hope that Canonical can be beneficial to tactic prediction
tools and human formalizers alike.

 7     Future Work
The canonical tactic applies an exhaustive backward search directly on the DTT representa-
tion of a Lean goal. It does so proficiently, but many goals are not best solved in this manner.
Canonical generates cut-free proofs (i.e. it does not create its own let declarations) and it
16   Canonical for Automated Theorem Proving in Lean


     has difficulty reasoning about structure types as it must first apply the correct projection
     function to access the field. The solution to this is a complementary system that performs
     forward reasoning. Forward reasoning moves are fundamentally different from backward
     reasoning moves in that they do not need to be backtracked (and thus do not form a search
     tree) and they require a level of prescience that cannot be achieved by a fail-fast approach.
     For this reason, we believe a separate, learning-based technique for forward reasoning is
     needed. We envision Canonical as being a buffer between AI systems and type theory, such
     that they do not need to worry about soundness or completeness, or about goals that can
     easily be solved via search.
         Similarly, Canonical cannot apply tactics or other domain-specific reasoning. A direct
     approach to add tactic support to Canonical will not succeed, as the types of metavariables
     for which domain-specific reasoning would be useful often contain multiple metavariables at
     the time they are attempted, halting most tactics. Enriching tactics such that they may be
     performed progressively as refinements are made is a question of programming languages
     theory [48] and is beyond the scope of this work.
         With the exception of statistical information, there is little communication between the
     branches of the DFS search in Canonical. Established formal methods techniques like conflict
     clauses in SAT [7] and tabled logic programming in TWELF [47] do not have an immediate
     generalization to this setting. Finding such a generalization would help to eliminate a
     substantial amount of redundancy from the search space.
         Finally, while we have targeted Lean for its popularity and usability, we do not foresee
     any intrinsic limitation in invoking Canonical to solve goals in other languages built on DTT,
     including advanced theories like cubical type theory [13] and those with modal types [46].
     This further showcases the potential of Canonical as an AI gym [4, 57], as data can be
     sourced from all of these languages (or generated, using ATP) to train models that are also
     language-agnostic. We leave this to future work.


      8     Conclusion
     Canonical is the first system capable of searching through terms in DTT, the foundations of
     Lean, Rocq, and Agda. The expressiveness of DTT and the generality of Canonical allows
     it to perform generalized induction on indexed inductive types, use higher-order axioms,
     and generate multiple constructive inhabitants of a type – all by exhaustive enumeration
     at the foundational level. We believe that search is a core technology that is useful for
     automated proof, program synthesis, witness/counterexample generation, pedagogy, proof
     minimization, and data generation for AI. Beyond this, robust goal-directed reasoning is a
     necessary capability to reason at the human level.


          References
      1   Martin Abadi, Luca Cardelli, P.L. Curien, and Jean-Jacques Levy. Explicit substitutions.
          Technical Report RR-1176, INRIA, March 1990. Projet PARA. URL: https://inria.hal.
          science/inria-00075382.
      2   Andreas Abel and Brigitte Pientka. Extensions to Miller’s pattern unification for dependent
          types and records. Mathematical Structures in Computer Science, 28(7):1262–1300, 2018.
          doi:10.1017/S0960129518000158.
      3   Peter B. Andrews, Matthew Bishop, Sunil Issar, Dan Nesmith, Frank Pfenning, and Hongwei
          Xi. TPS: A theorem-proving system for classical type theory. Journal of Automated Reasoning,
          16(3):321–353, June 1996. doi:10.1007/BF00252180.
C. Norman and J. Avigad                                                                                17


 4   Leni Aniva, Chuyue Sun, Brando Miranda, Clark Barrett, and Sanmi Koyejo. Pantograph: A
     machine-to-machine interaction interface for advanced theorem proving, high level reasoning,
     and data extraction in Lean 4, 2025. arXiv:2410.16429.
 5   Clark Barrett, Leilani Hadarean, Tim King, Aina Nötzli, Andrew Reynolds, and Cesare
     Tinelli. cvc5: A versatile and industrial-strength SMT solver. In International Conference
     on Computer Aided Verification (CAV), volume 13371 of Lecture Notes in Computer Science,
     pages 415–442. Springer, 2022. doi:10.1007/978-3-031-13185-1_5.
 6   Yves Bertot and Pierre Castran. Interactive Theorem Proving and Program Development:
     Coq’Art The Calculus of Inductive Constructions. Springer Publishing Company, Incorporated,
     1st edition, 2010.
 7   Armin Biere, Marijn Heule, Hans van Maaren, and Toby Walsh, editors. Handbook of
     Satisfiability, volume 185 of Frontiers in Artificial Intelligence and Applications. IOS Press,
     2009. URL: http://dblp.uni-trier.de/db/series/faia/faia185.html.
 8   Ana Bove, Peter Dybjer, and Ulf Norell. A brief overview of agda – a functional language
     with dependent types. In Stefan Berghofer, Tobias Nipkow, Christian Urban, and Makarius
     Wenzel, editors, Theorem Proving in Higher Order Logics, pages 73–78, Berlin, Heidelberg,
     2009. Springer Berlin Heidelberg. doi:10.1007/978-3-642-03359-9_6.
 9   Sally C. Brailsford, Chris N. Potts, and Barbara M. Smith. Constraint satisfaction problems:
     Algorithms and applications. European Journal of Operational Research, 119(3):557–581, 1999.
     doi:10.1016/S0377-2217(98)00364-6.
10   Kevin Buzzard, Jon Eugster, Alexander Bentkamp, Mohammad Pedramfar, and Patrick Massot.
     Natural number game. Available at https://adam.math.hhu.de/#/g/leanprover-community/
     nng4 (2025/03).
11   Mario Carneiro, Chad E. Brown, and Josef Urban. Automated Theorem Proving for Metamath.
     In Adam Naumowicz and René Thiemann, editors, 14th International Conference on Interactive
     Theorem Proving (ITP 2023), volume 268 of Leibniz International Proceedings in Informatics
     (LIPIcs), pages 9:1–9:19, Dagstuhl, Germany, 2023. Schloss Dagstuhl – Leibniz-Zentrum für
     Informatik. doi:10.4230/LIPIcs.ITP.2023.9.
12   Joshua Clune, Yicheng Qian, Alexander Bentkamp, and Jeremy Avigad. Duper: A Proof-
     Producing Superposition Theorem Prover for Dependent Type Theory. In Yves Bertot, Temur
     Kutsia, and Michael Norrish, editors, 15th International Conference on Interactive Theorem
     Proving (ITP 2024), volume 309 of Leibniz International Proceedings in Informatics (LIPIcs),
     pages 10:1–10:20, Dagstuhl, Germany, 2024. Schloss Dagstuhl – Leibniz-Zentrum für Informatik.
     doi:10.4230/LIPIcs.ITP.2024.10.
13   Cyril Cohen, Thierry Coquand, Simon Huber, and Anders Mörtberg. Cubical Type Theory:
     A Constructive Interpretation of the Univalence Axiom. In Tarmo Uustalu, editor, 21st
     International Conference on Types for Proofs and Programs (TYPES 2015), volume 69 of
     Leibniz International Proceedings in Informatics (LIPIcs), pages 5:1–5:34, Dagstuhl, Germany,
     2018. Schloss Dagstuhl – Leibniz-Zentrum für Informatik. doi:10.4230/LIPIcs.TYPES.2015.
     5.
14   Lukasz Czajka. A shallow embedding of pure type systems into first-order logic. In Types for
     Proofs and Programs, 2016. URL: https://api.semanticscholar.org/CorpusID:53242790.
15   Łukasz Czajka. Practical proof search for Coq by type inhabitation. In Automated
     Reasoning: 10th International Joint Conference, IJCAR 2020, Paris, France, July 1–4,
     2020, Proceedings, Part II, pages 28–57, Berlin, Heidelberg, 2020. Springer-Verlag. doi:
     10.1007/978-3-030-51054-1_3.
16   Łukasz Czajka and Cezary Kaliszyk. Hammer for Coq: Automation for dependent
     type theory. Journal of Automated Reasoning, 61(1):423–453, June 2018. doi:10.1007/
     s10817-018-9458-4.
17   N.G de Bruijn. Lambda calculus notation with nameless dummies, a tool for automatic formula
     manipulation, with application to the church-rosser theorem. Indagationes Mathematicae
     (Proceedings), 75(5):381–392, 1972. doi:10.1016/1385-7258(72)90034-0.
18   Canonical for Automated Theorem Proving in Lean


     18   Kefan Dong and Tengyu Ma. Stp: Self-play llm theorem provers with iterative conjecturing
          and proving. ArXiv, abs/2502.00212, 2025. doi:10.48550/arXiv.2502.00212.
     19   Gilles Dowek. A complete proof synthesis method for the cube of type systems. Journal of
          Logic and Computation, 3(3):287–315, June 1993. doi:10.1093/logcom/3.3.287.
     20   Gilles Dowek, Thérèse Hardin, and Claude Kirchner. Higher order unification via explicit
          substitutions. Information and Computation, 157(1):183–235, 2000. doi:10.1006/inco.1999.
          2837.
     21   Burak Ekici, Alain Mebsout, Cesare Tinelli, Chantal Keller, Guy Katz, Andrew Reynolds,
          and Clark Barrett. SMTCoq: A plug-in for integrating SMT solvers into Coq. In Computer
          Aided Verification - 29th International Conference, Heidelberg, Germany, July 2017. URL:
          https://hal.science/hal-01669345.
     22   Warren D. Goldfarb. The undecidability of the second-order unification problem. Theoretical
          Computer Science, 13(2):225–230, 1981. doi:10.1016/0304-3975(81)90040-2.
     23   Ferruccio Guidi, Claudio Sacerdoti Coen, and Enrico Tassi. Implementing Type Theory in
          Higher Order Constraint Logic Programming. working paper or preprint, November 2017.
          URL: https://inria.hal.science/hal-01410567.
     24   Robert Harper, Furio Honsell, and Gordon Plotkin. A framework for defining logics. J. ACM,
          40(1):143–184, January 1993. doi:10.1145/138027.138060.
     25   Gerard P. Huet. The undecidability of unification in third order logic. Information and Control,
          22(3):257–267, 1973. doi:10.1016/S0019-9958(73)90301-X.
     26   G.P. Huet. A unification algorithm for typed λ-calculus. Theoretical Computer Science,
          1(1):27–57, 1975. doi:10.1016/0304-3975(75)90011-0.
     27   Joe Hurd. First-order proof tactics in higher-order logic theorem provers. Design and
          Application of Strategies/Tactics in Higher Order Logics, number NASA/CP-2003-212448 in
          NASA Technical Reports, pages 56–68, 2003.
     28   Luka Janjić. Program synthesis with dependent types. Master’s thesis, Delft University of
          Technology, Delft, Netherlands, 2024.
     29   Cezary Kaliszyk and Josef Urban. Hol(y)hammer: Online atp service for hol light. Mathematics
          in Computer Science, 9(1):5–22, March 2015. doi:10.1007/s11786-014-0182-0.
     30   Cezary Kaliszyk and Josef Urban. Mizar 40 for mizar 40. Journal of Automated Reasoning,
          55(3):245–256, October 2015. doi:10.1007/s10817-015-9330-8.
     31   Wen Kokke and Wouter Swierstra. Auto in agda. In Ralf Hinze and Janis Voigtländer, editors,
          Mathematics of Program Construction, pages 276–301, Cham, 2015. Springer International
          Publishing.
     32   Laura Kovács and Andrei Voronkov. First-order theorem proving and Vampire. In Natasha
          Sharygina and Helmut Veith, editors, Computer Aided Verification, pages 1–35, Berlin,
          Heidelberg, 2013. Springer Berlin Heidelberg. doi:10.1007/978-3-642-39799-8_1.
     33   Jannis Limperg and Asta Halkjær From. Aesop: White-box best-first proof search for lean.
          In Proceedings of the 12th ACM SIGPLAN International Conference on Certified Programs
          and Proofs, CPP 2023, pages 253–266, New York, NY, USA, 2023. Association for Computing
          Machinery. doi:10.1145/3573105.3575671.
     34   Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
          Xia, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-prover: A frontier model for open-source
          automated theorem proving, 2025. doi:10.48550/arXiv.2502.07640.
     35   Fredrik Lindblad and Marcin Benke. A tool for automated theorem proving in Agda. In
          Jean-Christophe Filliâtre, Christine Paulin-Mohring, and Benjamin Werner, editors, Types for
          Proofs and Programs, pages 154–169, Berlin, Heidelberg, 2006. Springer Berlin Heidelberg.
     36   The mathlib Community. The Lean mathematical library. In Proceedings of the 9th ACM
          SIGPLAN International Conference on Certified Programs and Proofs, CPP 2020, pages
          367–381, New York, NY, USA, 2020. Association for Computing Machinery. doi:10.1145/
          3372885.3373824.
C. Norman and J. Avigad                                                                               19


37   Jia Meng and Lawrence C. Paulson. Translating higher-order problems to first-order clauses.
     Journal of Automated Reasoning, 40(1):35–60, 2008. doi:10.1007/s10817-007-9085-y.
38   Jia Meng, Claire Quigley, and Lawrence C. Paulson. Automation for interactive proof: First
     prototype. Information and Computation, 204(10):1575–1596, 2006. Combining Logical
     Systems. doi:10.1016/j.ic.2005.05.010.
39   Dale Miller. Unification of simply typed lambda-terms as logic programming. In Proceedings
     of the Eighth International Logic Programming Conference, pages 255–269. MIT Press, 1991.
40   Abdalrhman Mohamed, Tomaz Mascarenhas, Harun Khan, Haniel Barbosa, Andrew Reynolds,
     Yicheng Qian, Cesare Tinelli, and Clark Barrett. Lean-SMT: An SMT tactic for discharging
     proof goals in Lean, 2025. doi:10.48550/arXiv.2505.15796.
41   Leonardo De Moura and Nikolaj Bjørner. Z3: An efficient SMT solver. In Tools and Algorithms
     for the Construction and Analysis of Systems (TACAS), volume 4963 of Lecture Notes in
     Computer Science, pages 337–340. Springer, 2008. doi:10.1007/978-3-540-78800-3_24.
42   Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming
     language. In André Platzer and Geoff Sutcliffe, editors, Automated Deduction – CADE 28, pages
     625–635, Cham, 2021. Springer International Publishing. doi:10.1007/978-3-030-79876-5_
     37.
43   Gopalan Nadathur and Debra Sue Wilson. A notation for lambda terms a generalization of en-
     vironments. Theoretical Computer Science, 198(1):49–98, 1998. doi:10.1016/S0304-3975(97)
     00184-9.
44   Chase       Norman.               Canonical.               Software,      swhId:        ]Soft-
     wareswh:1:dir:06a599989bad108dc52bfdff704d356badfa63d4 (visited on 2025-09-09).
     URL: https://github.com/chasenorman/Canonical, doi:10.4230/artifacts.24703.
45   Chase Norman.              CanonicalLean.            Software,    version v4.22.0.,   swhId:
     swh:1:dir:98f9920f9b96cabe1c6188b23fd3823d0ad9fb0f (visited on 2025-09-09). URL:
     https://github.com/chasenorman/CanonicalLean, doi:10.4230/artifacts.24708.
46   Frank Pfenning and Rowan Davies. A judgmental reconstruction of modal logic. Mathematical
     Structures in Computer Science, 11(4):511–540, 2001. doi:10.1017/S0960129501003322.
47   Brigitte Pientka. Tabling for higher-order logic programming. In Robert Nieuwenhuis, editor,
     Automated Deduction – CADE-20, pages 54–68, Berlin, Heidelberg, 2005. Springer Berlin
     Heidelberg. doi:10.1007/11532231_5.
48   G. Plotkin. Building-in equational theories. In Bernard Metlzner and Donald Michie, editors,
     Machine Intelligence, volume 7, pages 73–90. Edinburgh University Press, 1972.
49   J. A. Robinson. A machine-oriented logic based on the resolution principle. Journal of the
     ACM, 12(1):23–41, 1965. doi:10.1145/321250.321253.
50   Stephan Schulz, Simon Cruanes, and Petar Vukmirović. Faster, higher, stronger: E 2.3. In
     Pascal Fontaine, editor, Proc. of the 27th CADE, Natal, Brasil, number 11716 in LNAI, pages
     495–507. Springer, 2019. doi:10.1007/978-3-030-29436-6_29.
51   Carsten Schürmann and Frank Pfenning. Automated theorem proving in a simple meta-logic for
     LF. In Claude Kirchner and Hélène Kirchner, editors, Automated Deduction — CADE-15, pages
     286–300, Berlin, Heidelberg, 1998. Springer Berlin Heidelberg. doi:10.1007/BFB0054266.
52   Lukas Skystedt. A new synthesis tool for Agda. Master’s thesis, Chalmers University of
     Technology and University of Gothenburg, Gothenburg, Sweeden, 2022.
53   Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Lean copilot: Large language models as
     copilots for theorem proving in lean, 2025. arXiv:2404.12534.
54   Petar Vukmirović, Alexander Bentkamp, Jasmin Blanchette, Simon Cruanes, Visa Nummelin,
     and Sophie Tourret. Making higher-order superposition work. Journal of Automated Reasoning,
     66:541–564, 2022. doi:10.1007/s10817-021-09613-z.
55   Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan Ying, Jiayu Wang, Dahua Lin, and Kai
     Chen. Internlm2.5-stepprover: Advancing automated theorem proving via expert iteration on
     large-scale lean problems, 2024. doi:10.48550/arXiv.2410.15700.
20   Canonical for Automated Theorem Proving in Lean


     56   Huajian Xin, Z.Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu,
          Liyue Zhang, Xuan Lu, Qiushi Du, Wenjun Gao, Haowei Zhang, Qihao Zhu, Dejian Yang,
          Zhibin Gou, Z.F. Wu, Fuli Luo, and Chong Ruan. Deepseek-prover-v1.5: Harnessing proof
          assistant feedback for reinforcement learning and monte-carlo tree search. In The Thirteenth
          International Conference on Learning Representations, 2025. URL: https://openreview.net/
          forum?id=I4YAIwrsXa.
     57   Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
          Ryan Prenger, and Anima Anandkumar. LeanDojo: Theorem proving with retrieval-augmented
          language models. In Neural Information Processing Systems (NeurIPS), 2023.
