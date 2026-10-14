                                                                               Bounded Refinement Types ∗

                                                                                  Niki Vazou          Alexander Bakst         Ranjit Jhala
                                                                                                          UC San Diego




                                        Abstract                                                                  bounds checking [21], termination and totality checking [29], pro-
arXiv:1507.00385v1 [cs.PL] 1 Jul 2015




                                                                                                                  tocol validation [2, 9], and securing web applications [10]. Unfor-
                                        We present a notion of bounded quantification for refinement types        tunately, this automation comes at a price. To ensure predictable
                                        and show how it expands the expressiveness of refinement typing           and decidable type checking, we must limit the logical formulas
                                        by using it to develop typed combinators for: (1) relational algebra      appearing in specification types to decidable (typically quantifier
                                        and safe database access, (2) Floyd-Hoare logic within a state trans-     free) first order theories, thereby precluding higher-order specifi-
                                        former monad equipped with combinators for branching and loop-            cations that are essential for modular verification.
                                        ing, and (3) using the above to implement a refined IO monad that
                                        tracks capabilities and resource usage. This leap in expressiveness            In this paper, we introduce Bounded Refinement Types which
                                        comes via a translation to “ghost” functions, which lets us retain        reconcile expressive higher order specifications with automatic
                                        the automated and decidable SMT based checking and inference              SMT based verification. Our approach comprises two key ingre-
                                        that makes refinement typing effective in practice.                       dients. Our first ingredient is a mechanism, developed by [27], for
                                                                                                                  abstracting refinements over type signatures. This mechanism is
                                        Categories and Subject Descriptors D.2.4 [Software/Program                the analogue of parametric polymorphism in the refinement setting:
                                        Verification]; D.3.3 [Language Constructs and Features]: Poly-            it increases expressiveness by permitting generic signatures that are
                                        morphism; F.3.1 [Logics and Meanings of Programs]: Specifying             universally quantified over the (concrete) refinements that hold at
                                        and Verifying and Reasoning about Programs                                different call-sites. However, we observe that for modular verifi-
                                                                                                                  cation, we additionally need to constrain the abstract refinement
                                        Keywords     haskell, refinement types, abstract interpretation           parameters, typically to specify fine grained dependencies between
                                                                                                                  the parameters. Our second ingredient provides a technique for en-
                                        1. Introduction                                                           riching function signatures with subtyping constraints (or bounds)
                                                                                                                  between abstract refinements that must be satisfied by the concrete
                                        Must program verifiers always choose between expressiveness and           refinements at instantiation. Thus, constrained abstract refinements
                                        automation? On the one hand, tools based on higher order logics           are the analogue of bounded quantification in the refinement setting
                                        and full dependent types impose no limits on expressiveness, but          and in this paper, we show that this simple technique proves to be
                                        require user-provided (perhaps, tactic-based) proofs. On the other        remarkably effective.
                                        hand, tools based on Refinement Types [22, 30] trade expressive-
                                        ness for automation. For example, the refinement types
                                                                                                                    • First, we demonstrate via a series of short examples how
                                          type Pos     = { v: Int | 0 < v }                                          bounded refinements enable the specification and verification
                                          type IntGE x = { v: Int | x ≤ v }                                          of diverse textbook higher order abstractions that were hitherto
                                                                                                                     beyond the scope of decidable refinement typing (§ 2).
                                        specify subsets of Int corresponding to values that are positive
                                        or larger than some other value x respectively. By limiting the             • Second, we formalize bounded types and show how bounds are
                                        refinement predicates to SMT-decidable logics [17], refinement               translated into “ghost” functions, reducing type checking and
                                        type based verifiers eliminate the need for explicit proof terms, and        inference to the “unbounded” setting of [27], thereby ensuring
                                        thus automate verification.                                                  that checking remains decidable. Furthermore, as the bounds
                                            This high degree of automation has enabled the use of refine-            are Horn constraints, we can directly reuse the abstract inter-
                                        ment types for a variety of verification tasks, ranging from array           pretation of Liquid Typing [21] to automatically infer concrete
                                                                                                                     refinements at instantiation sites (§ 3).
                                        ∗ This work was supported by NSF grants CCF-1422471, C1223850, CCF-         • Third, to demonstrate the expressiveness of bounded refine-
                                        1218344, a Microsoft Research Ph.D Fellowship and a generous gift from       ments, we use them to build a typed library for extensible dic-
                                        Microsoft Research.                                                          tionaries, to then implement a relational algebra library on top
                                                                                                                     of those dictionaries, and to finally build a library for type-safe
                                                                                                                     database access (§ 4).
                                                                                                                    • Finally, we use bounded refinements to develop a Refined State
                                                                                                                     Transformer monad for stateful functional programming, based
                                                                                                                     upon Filliâtre’s method for indexing the monad with pre- and
                                                                                                                     post-conditions [8]. We use bounds to develop branching and
                                                                                                                     looping combinators whose types signatures capture the deriva-
                                                                                                                     tion rules of Floyd-Hoare logic, thereby obtaining a library for
                                                                                                                     writing verified stateful computations (§ 5). We use this library
                                                                                                                     to develop a refined IO monad that tracks capabilities at a fine-
   granularity, ensuring that functions only access specified re-            a ≤ b ⇒ ( cmp        ⇔    a ≤ b) ⇒ v == cmp ⇒ ( v ⇔
   sources (§ 6).                                                                true )

    We have implemented Bounded Refinement Types in L IQUID -              The first antecedent comes from the input type of b, the second
H ASKELL [29]. The source code of the examples (with slightly              from the type of cmp obtained from the output of leq, the third
more verbose concrete syntax) is at [24]. While the construction           from the actual input passed to assert, and the goal comes from
of these verified abstractions is possible with full dependent types,      the input type required by assert. An SMT solver [17] readily es-
bounded refinements keep checking automatic and decidable, use             tablishes the validity of the above VC, thereby verifying checkGE.
abstract interpretation to automatically synthesize refinements (i.e.,
                                                                           First order refinements prevent modular specifications.          Con-
pre- and post-conditions and loop invariants), and most importantly
                                                                           sider the function that returns the largest element of a list:
enable retroactive or gradual verification as when erase the refine-
ments, we get valid programs in the host language (§ 7). Thus,               maximum           :: List Int → Int
bounded refinements point a way towards keeping our automation,              maximum [x ]      = x
and perhaps having expressiveness too.                                       maximum (x : xs ) = max x ( maximum xs )
                                                                               where max a b = if a < b then b else a

2. Overview                                                                How can one write a first-order refinement type specification for
                                                                           maximum that will let us verify the below code?
We start with a high level overview of bounded refinement types. To
                                                                             posMax :: List Pos → Pos
make the paper self contained, we begin by recalling the notions of          posMax = maximum
abstract refinement types. Next, we introduce bounded refinements,
and show how they permit modular higher-order specifications.              Any suitable specification would have to enumerate the situations
Finally, we describe how they are implemented via an elaboration           under which maximum may be invoked breaking modularity.
process that permits automatic first-order verification.
                                                                           Abstract Refinements overcome the above modularity problems
2.1 Preliminaries                                                          [27]. The main idea is that we can type maximum by observing that it
                                                                           returns one of the elements in its input list. Thus, if every element
Refinement Types let us precisely specify subsets of values, by            of the list enjoys some refinement p then the output value is also
conjoining base types with logical predicates that constrain the           guaranteed to satisfy p. Concretely, we can type the function as:
values. We get decidability of type checking, by limiting these
predicates to decidable, quantifier-free, first-order logics, including    maximum :: ∀<p :: Int → Bool >. List Int <p > → Int <p >
the theory of linear arithmetic, uninterpreted functions, arrays, bit-
                                                                           where informally, Int<p> stands for {v:Int | p v}, and p is an
vectors and so on. Apart from subsets of values, like the Pos and
                                                                           uninterpreted function in the refinement logic [17]. The signature
IntGE that we saw in the introduction, we can specify contracts like
                                                                           states that for any refinement p on Int, the input is a list of ele-
pre- and post-conditions by suitably refining the input and output
                                                                           ments satisfying p and returns as output an integer satisfying p. In
types of functions.
                                                                           the sequel, we will drop the explicit quantification of abstract re-
                                                                           finements; all free abstract refinements will be implicitly quantified
Preconditions are specified by refining input types. We specify
                                                                           at the top-level (as with classical type parameters.)
that the function assert must only be called with True, where the
refinement type TRUE contains only the singleton True:                     Abstract Refinements Preserve Decidability. Abstract refine-
   type TRUE = { v : Bool | v         ⇔    True }                          ments do not require the use of higher-order logics. Instead, ab-
                                                                           stractly refined signatures (like maximum) can be verified by view-
   assert         :: TRUE → a → a                                          ing the abstract refinements p as uninterpreted functions that only
   assert True x = x                                                       satisfy the axioms of congruence, namely:
   assert False _ = error " Provably Dead Code "
                                                                             ∀ x y. x = y ⇒ p x           ⇔    p y

We can specify post-conditions by refining output types. For               As the quantifier free theory of uninterpreted functions is decidable
example, a primitive Int comparison operator leq can be assigned           [17], abstract refinement type checking remains decidable [27].
a type that says that the output is True iff the first input is actually
less than or equal to the second:                                          Abstract Refinements are Automatically Instantiated at call-
                                                                           sites, via the abstract interpretation framework of Liquid Typ-
   leq :: x : Int → y: Int → { v : Bool | v              ⇔    x ≤ y}       ing [27]. Each instantiation yields fresh refinement variables on
                                                                           which subtyping constraints are generated; these constraints are
Refinement Type Checking proceeds by checking that at each                 solved via abstract interpretation yielding the instantiations. Hence,
application, the types of the actual arguments are subtypes of those       we verify posMax by instantiating:
of the function inputs, in the environment (or context) in which the         p 7→ λ v → 0 < v            -- at posMax
call occurs. Consider the function:
   checkGE     :: a : Int → b : IntGE a → Int                              2.2 Bounded Refinements
   checkGE a b = assert cmp b
     where cmp = a ‘leq ‘ b                                                Even with abstraction, refinement types hit various expressiveness
                                                                           walls. Consider the following example from [26]. find takes as
To verify the call to assert we check that the actual parameter cmp        input a predicate q, a continuation k and a starting number i; it
is a subtype of TRUE, under the assumptions given by the input types       proceeds to compute the smallest Int (larger than i) that satisfies
for a and b. Via subtyping [29] the check reduces to establishing the      q, and calls k with that value. ex1 passes find a continuation that
validity of the verification condition (VC)                                checks that the “found” value equals or exceeds n.
   ex1 :: ( Int → Bool ) → Int → ()                                         Function Composition
   ex1 q n = find q ( checkGE n ) n
                                                                            First, consider compose. What is a modular specification for
   find q k i                                                               compose that would let us verify that ex2 enjoys the given spec-
     | q i       = k i                                                      ification?
     | otherwise = find q k ( i + 1)
                                                                              compose f g x = f ( g x )
Verification fails as there is no way to specify that k is only called        type Plus x y = { v : Int | v = x + y }
with arguments greater than n. First, the variable n is not in scope          ex2    :: n : Int → Plus n 2
at the function definition and so we cannot refer to it. Second, we           ex2    = incr ‘ compose ‘ incr
could try to say that k is invoked with values greater than or equal
to i, which gets substituted with n at the call-site. Alas, due to the        incr   :: n : Int → Plus n 1
currying order, i too is not in scope at the point where k’s type is          incr n = n + 1
defined and so the type for k cannot depend upon i.
                                                                            The challenge is to chain the dependencies between the input
Can Abstract Refinements Help? Lets try to abstract over the                and output of g and the input and output of f to obtain a relationship
refinement that i enjoys, and assign find the type:                         between the input and output of the composition. We can capture
   ( Int → Bool ) → ( Int <p > → a ) → Int <p > → a                         the notion of chaining in a bound:
which states that for any refinement p, the function takes an input           bound Chain p q r = λx y z →
i which satisfies p and hence that the continuation is also only                    q x y ⇒ p y z ⇒ r x z
invoked on a value which trivially enjoys p, namely i. At the call-
                                                                            which states that for any x, y and z, if (1) x and y are related by q,
site in ex1 we can instantiate
                                                                            and (2) y and z are related by p, then (3) x and z are related by r.
                          p 7→ λv → n ≤ v                            (1)        We use Chain to type compose using three abstract refinements
This instantiated refinement is satisfied by the parameter n, and           p, q and r, relating the arguments and return values of f and g to
sufficient to verify, via function subtyping, that checkGE n will           their composed value. (Here, c<r x> abbreviates {v:c | r x v}.)
only be called with values satisfying p, and hence larger than n.             compose :: ( Chain p q r) ⇒ (y : b → c < p y >)
                                                                                                        → (x : a → b < q x >)
find is ill-typed as the signature requires that at the recursive call                                  → (w : a → c < r w >)
site, the value i+1 also satisfies the abstract refinement p. While
this holds for the example we have in mind (1), it does not hold for
all p, as required by the type of find! Concretely, {v:Int|v=i+1}           To verify ex2    we instantiate, at the call to compose,
is in general not a subtype of Int<p>, as the associated VC                   p , q 7→ λx v → v = x + 1
                                                                                  r 7→ λx v → v = x + 2
                        ... ⇒ p i ⇒ p (i+1)                          (2)
is invalid – the type checker thus (soundly!) rejects find.                 The above instantiation satisfies the bound, as shown by the validity
                                                                            of the VC derived from instantiating p, q, and r in Chain:
We must Bound the Quantification of p to limit it to refinements
satisfying some constraint, in this case that p is upward closed. In          y == x + 1 ⇒ z == y + 1 ⇒ z == x + 2
the dependent setting, where refinements may refer to program val-
                                                                            and hence, we can check that ex2 implements its specified type.
ues, bounds are naturally expressed as constraints between refine-
ments. We define a bound, UpClosed which states that p is a refine-
                                                                            List Filtering
ment that is upward closed, i.e., satisfies ∀ x. p x ⇒ p (x+1),
and use it to type find as:                                                 Next, consider the list filter function. What type signature for
   bound UpClosed ( p :: Int → Bool )                                       filter would let us check positives?
     = λx → p x ⇒ p ( x +1)                                                   filter q ( x : xs )
                                                                                | q x             = x : filter q xs
   find :: ( UpClosed p ) ⇒ ( Int → Bool )                                      | otherwise       = filter q xs
                          → ( Int <p > → a )                                  filter _ []         = []
                          → Int <p > → a
                                                                              positives       :: [ Int ] → [ Pos ]
This time, the checker is able to use the bound to verify the VC (2).
                                                                              positives       = filter isPos
We do so in a way that refinements (and thus VCs) remain quanti-                where isPos x = 0 < x
fier free and hence, SMT decidable (§ 2.4).
                                                                            Such a signature would have to relate the Bool returned by f with
At the call to find in the body of ex1, we perform the instantia-
                                                                            the property of the x that it checks for. Typed Racket’s latent predi-
tion (1) which generates the additional VC (n ≤ x ⇒ n ≤ x+1)
                                                                            cates [25] account for this idiom, but are a special construct limited
by plugging in the concrete refinements to the bound constraint.
                                                                            to Bool-valued “type” tests, and not arbitrary invariants. Another
The SMT solver easily checks the validity of the VC and hence this
                                                                            approach is to avoid the so-called “Boolean Blindness” that accom-
instantiation, thereby statically verifying ex1, i.e., that the assertion
                                                                            panies filter by instead using option types and mapMaybe.
inside checkGE cannot fail.
                                                                            We overcome blindness using a witness bound:
2.3 Bounds for Higher-Order Functions
                                                                              bound Witness p w = λx b → b ⇒ w x b ⇒ p x
Next, we show how bounds expand the scope of refinement typ-
ing by letting us write precise modular specifications for various          which says that w witnesses the refinement p. That is, for any
canonical higher-order functions.                                           boolean b such that w x b holds, if b is True then p x also holds.
filter can be given a type saying that the output values enjoy             2.4 Implementation
a refinement p as long as the test predicate q returns a boolean
witnessing p:                                                              To implement bounded refinement typing, we must solve two prob-
                                                                           lems. Namely, how do we (1) check, and (2) use functions with
   filter :: ( Witness p w ) ⇒ ( x : a → Bool < w x >)                     bounded signatures? We solve both problems via a unifying insight
                             → List a                                      inspired by the way typeclasses are implemented in Haskell.
                             → List a <p >
                                                                           1. A Bound Specifies a function type whose inputs are uncon-
                                                                              strained, and whose output is some value that carries the re-
To verify positives we infer the following type and instantia-
                                                                              finement corresponding to the bound’s body.
tions for the abstract refinements p and w at the call to filter:
                                                                           2. A Bound is Implemented by a ghost function that returns true,
  isPos :: x : Int → { v : Bool | v           ⇔    0 < x}                     but is defined in a context where the bound’s constraint holds
  p     7→ λv      → 0 < v                                                    when instantiated to the concrete refinements at the context.
  w      7→ λx b → b ⇔ 0 < x
                                                                           We elaborate bounds into ghost functions satisfying the bound’s
                                                                           type. To check bounded functions, we need to call the ghost func-
List Folding
                                                                           tion to materialize the bound constraint at particular values of in-
Next, consider the list fold-right function. Suppose we wish to            terest. Dually, to use bounded functions, we need to create ghost
prove the following type for ex3:                                          functions whose outputs are guaranteed to satisfy the bound con-
                                                                           straint. This elaboration reduces bounded refinement typing to the
   foldr :: ( a → b → b ) → b → List a → b                                 simpler problem of unbounded abstract refinement typing [27]. The
   foldr op b []         = b                                               formalization of our elaboration is described in § 3. Next, we illus-
   foldr op b ( x : xs ) = x ‘op ‘ foldr op b xs                           trate the elaboration by explaining how it addresses the problems
   ex3 :: xs : List a → { v : Int | v == len xs }
                                                                           of checking and using bounded signatures like compose.
   ex3 = foldr (λ_ → incr ) 0
                                                                           We Translate Bounds into Function Types called the bound-
where len is a logical or measure function used to represent the           type where the inputs are unconstrained, and the outputs satisfy
number of elements of the list in the refinement logic [29]:               the bound’s constraint. For example, the bound Chain used to type
                                                                           compose in § 2.3, corresponds to a function type, yielding the
   measure len :: List a → Nat                                             translated type for compose:
   len []         = 0
   len ( x : xs ) = 1 + len xs                                               type ChainTy p q r
                                                                               = x:a → y:b → z:c
                                                                               → { v : Bool | q x y ⇒ p y z ⇒ r x z }
We specify induction as a bound. Let (1) inv be an abstract
refinement relating a list xs and the result b obtained by folding           compose :: ( ChainTy p q r ) → ( y : b → c < p y >)
                                                                                                          → ( x : a → b < q x >)
over it, and (2) step be an abstract refinement relating the inputs                                       → ( w : a → c < r w >)
x, b and output b’ passed to and obtained from the accumulator op
respectively. We state that inv is closed under step as:
                                                                           To Check Bounded Functions we view the bound constraints as
   bound Inductive inv step = λx xs b b ’ →
                                                                           extra (ghost) function parameters (cf. type class dictionaries), that
         inv xs b ⇒ step x b b ’ ⇒ inv (x : xs ) b ’
                                                                           satisfy the bound-type. Crucially, each expression where a subtyp-
                                                                           ing constraint would be generated (by plain refinement typing) is
We can give foldr a type that says that the function outputs a             wrapped with a “call” to the ghost to materialize the constraint at
value that is built inductively over the entire input list:                values of interest. For example we elaborate compose into:
   foldr ::     ( Inductive inv step )                                       compose $chain f g x =
         ⇒      ( x: a → acc : b → b < step x acc >)                           let t1 = g x
         →      b < inv [] >                                                       t2 = f t1
         →      xs : List a                                                        _ = $chain x t1 t2                -- materialize
         →      b < inv xs >                                                   in t2

That is, for any invariant inv that is inductive under step, if the        In the elaborated version $chain is the ghost parameter corre-
initial value b is inv-related to the empty list, then the folded output   sponding to the bound. As is standard [21], we perform ANF-
is inv-related to the input list xs.                                       conversion to name intermediate values, and then wrap the function
                                                                           output with a call to the ghost to materialize the bound’s constraint.
We verify ex3    by inferring, at the call to foldr                        Consequently, the output of compose, namely t2, is checked to be
                                                                           a subtype of the specified output type, in an environment strength-
   inv →7   λxs v    → v == len xs                                         ened with the bound’s constraint instantiated at x, t1 and t2. This
   step → 7 λx b b ’ → b ’ == b + 1                                        subtyping reduces to a quantifier free VC:

The SMT solver validates the VC obtained by plugging the above                  q     x t1
into the bound. Instantiating the signature for foldr yields pre-            ⇒ p      t1 t2
                                                                             ⇒ (q     x t1 ⇒ p t1 t2 ⇒ r x t2 )
cisely the output type desired for ex3.                                      ⇒ v      == t2 ⇒ r x v
    Previously, [27] describes a way to type foldr using abstract
refinements that required the operator op to have one extra ghost ar-      whose first two antecedents are due to the types of t1 and t2 (via
gument. Bounds let us express induction without ghost arguments.           the output types of g and f respectively), and the third comes from
the call to $chain. The output value v has the singleton refinement
                                                                                        Expressions       e     ::=   x | c | λx : t.e | e x
that states it equals to t2, and finally the VC states that the output                                            |   let x : t = e in e
value v must be related to the input x via r. An SMT solver                                                       |   Λα.e | e [t]
validates this decidable VC easily, thereby verifying compose.                                                    |   Λπ : t.e | e [φ]
    Our elaboration inserts materialization calls for all variables (of                   Constants        c    ::=   true | false | crash
the appropriate type) that are in scope at the given point. This could                                            |   0 | 1 | −1 | . . .
introduce upto nk calls where k is the number of parameters in the
                                                                           Parametric Refinements         φ     ::=   r | λx : b.φ
bound and n the number of variables in scope. In practice (e.g., in
compose) this number is small (e.g., 1) since we limit ourselves to                    Predicates         p     ::=   c | ¬p | p = p | . . .
variables of the appropriate types.                                           Atomic Refinements          a     ::=   p | πx
    To preserve semantics we ensure that none of these materializa-                   Refinements         r     ::=   a | a∧r | a⇒ r
tion calls can diverge, by carefully constraining the structure of the                Basic Types         b     ::=   Int | Bool | α
arguments that instantiate the ghost functional parameters.                                 Types         t     ::=   {v : b | r}
                                                                                                                  |   {v : (x : t) → t | r}
At Uses of Bounded Functions our elaboration uses the bound-
type to create lambdas with appropriate parameters that just return                 Bounded Types         ρ     ::=   t
true. For example, ex2 is elaborated to:                                                Schemata          σ     ::=   ρ | ∀α.σ | ∀π : t.σ
   ex2 = compose (λ_ _ _ → true ) incr incr
                                                                                               Figure 1. Syntax of λP
This elaboration seems too naı̈ve to be true: how do we ensure that
the function actually satisfies the bound type?
   Happily, that is automatically taken care of by function sub-                Bounded Types         ρ   ::=    t | {φ} ⇒ ρ
typing. Recalling the translated type for compose, the elaborated                 Expressions         e   ::=    . . . | Λ{φ}.e | e{φ}
lambda (λ_ _ _ → true) is constrained to be a subtype of
ChainTy p q r. In particular, given the call site instantiation
                                                                                      Figure 2. Extending Syntax of λP to λB
  p 7→ λy z → z == y + 1
  q 7→ λx y → y == x + 1
  r 7→ λx z → z == x + 2                                                  The Primitive Constants of λP include true, false, 0, 1, -1, etc..
                                                                          In addition, we include a special untypable constant crash that
this subtyping constraint reduces to the quantifier-free VC:
                                                                          models “going wrong”. Primitive operations return a crash when
        [[Γ]] ⇒ true ⇒ (z == y + 1) ⇒ (y == x + 1)                        invoked with inputs outside their domain, e.g., when / is invoked
                                           ⇒ (z == x + 2)          (3)    with 0 as the divisor, or when an assert is applied to false.
where Γ contains assumptions about the various binders in scope.          Atomic Refinements a are either concrete or abstract refine-
The VC 3 is easily proved valid by an SMT solver, thereby verify-         ments. A concrete refinement p is a boolean valued expression
ing the subtyping obligation defined by the bound, and hence, that        (such as a constant, negation, equality, etc.) drawn from a strict
ex2 satisfies the given type.                                             subset of the language of expressions which includes only terms
                                                                          that (a) neither diverge nor crash, and (b) can be embedded into an
3. Formalism                                                              SMT decidable refinement logic including the quantifier free the-
                                                                          ory of linear arithmetic and uninterpreted functions [29]. An ab-
Next we formalize Bounded Refinement Types by defining a core             stract refinement π x is an application of a refinement variable π
calculus λB and showing how it can be reduced to λP , the core            to a sequence of program variables. A refinement r is either a con-
language of Abstract Refinement Types [27]. We start by defining          junction or implication of atomic refinements. To enable inference,
the syntax (§ 3.1) and semantics (§ 3.2) of λP and the syntax of          we only allow implications to appear within bounds φ (§ 3.6).
λB (§ 3.3). Next, we provide a translation from λB to λP (§ 3.4).
Then, we prove soundness by showing that our translation is se-           The Types of λP written t include basic types, dependent func-
mantics preserving (§ 3.5). Finally, we describe how type inference       tions and schemata quantified over type and refinement variables α
remains decidable in the presence of bounded refinements (§ 3.6).         and π respectively. A basic type is one of Int, Bool, or a type vari-
                                                                          able α. A refined type t is either a refined basic type {v : b | r},
3.1 Syntax of λP                                                          or a dependent function type {v : (x : t) → t | r} where the pa-
                                                                          rameter x can appear in the refinements of the output type. (We
We build our core language on top of λP , the language of Abstract        include refinements for functions, as refined type variables can be
Refinement Types [27]. Figure 1 summarizes the syntax of λP , a           replaced by function types. However, typechecking ensures these
polymorphic λ-calculus extended with abstract refinements.                refinements are trivially true.) In λP bounded types ρ are just a
The Expressions of λP include the usual variables x, primitive            synonym for types t. Finally, schemata are obtained by quantifying
constants c, λ-abstraction λx : t.e, application e e, let bindings        bounded types over type and refinement variables.
let x : t = e in e, type abstraction Λα.e, and type application e [t].
(We add let-binders to λP from [27] as they can be reduced to             3.2 Semantics of λP
λ-abstractions in the usual way.) The parameter t in the type ap-         Figure 3 summarizes the static semantics of λP as described in
plication is a refinement type, as described shortly. Finally, λP in-     [27]. Unlike [27] that syntactically separates concrete (p) from
cludes refinement abstraction Λπ : t.e, which introduces a refine-        abstract (π x) refinements, here, for simplicity, we merge both
ment variable π (with its type t), which can appear in refinements        concrete and abstract refinements to atomic refinements a.
inside e, and the corresponding refinement application e [φ] that
substitutes an abstract refinement with the parametric refinement         A type environment Γ is a sequence of type bindings x : σ. We
φ, i.e., refinements r closed under lambda abstractions.                  use environments to define three kinds of judgments:
Well-Formedness                                                                                                                                    Γ⊢σ

                            Γ, v : b ⊢ r : Bool                        Γ ⊢ r : Bool    Γ ⊢ tx    Γ, x : tx ⊢ t
                                                      WF-BASE                                                        WF-F UN
                             Γ ⊢ {v : b | r}                                 Γ ⊢ {v : (x : tx ) → t | r}
                                                  Γ, π : t ⊢ σ                     Γ⊢σ
                                                                  WF-A BS -π                    WF-A BS -α
                                                  Γ ⊢ ∀π : t.σ                    Γ ⊢ ∀α.σ

Subtyping                                                                                                                                Γ ⊢ σ1  σ2

           ([[Γ]] ⇒ [[r1 ]] ⇒ [[r2 ]]) is valid                              Γ ⊢ t2  t1    Γ, x2 : t2 ⊢ t′1 [x2 /x1 ]  t′2
                                                    -BASE                                                                              -F UN
           Γ ⊢ {v : b | r1 }  {v : b | r2 }                       Γ ⊢ {v : (x1 : t1 ) → t1 | r1 }  {v : (x2 : t2 ) → t′2 | true}
                                                                                          ′


                                      Γ, π : t ⊢ σ1  σ2                                Γ ⊢ σ1  σ2
                                                                     -RVAR                                    -P OLY
                                   Γ ⊢ ∀π : t.σ1  ∀π : t.σ2                         Γ ⊢ ∀α.σ1  ∀α.σ2

Type Checking                                                                                                                                Γ⊢e:σ

                     Γ ⊢ e : σ2      Γ ⊢ σ2  σ1         Γ ⊢ σ1                 Γ ⊢ ex : tx   Γ, x : tx ⊢ e : t      Γ⊢t
                                                                    T-S UB                                                     T-L ET
                                     Γ ⊢ e : σ1                                         Γ ⊢ let x : = ex in e : t
              x : {v : b | r} ∈ Γ                                            x:t∈Γ
                                          T-VAR -BASE                                      T-VAR                                        T-C ONST
            Γ ⊢ x : {v : b | v = x}                                          Γ⊢x:t                                  Γ ⊢ c : tc (c)
        Γ ⊢ e1 : (x : tx ) → t    Γ ⊢ e2 : tx                      Γ, x : tx ⊢ e : t      Γ ⊢ tx                      Γ, α ⊢ e : σ
                                                      T-A PP                                          T-F UN                              T-G EN
                Γ ⊢ e1 e2 : t[e2 /x]                               Γ ⊢ λx : tx .e : (x : tx ) → t                   Γ ⊢ Λα.e : ∀α.σ

      Γ ⊢ e : ∀π : t.σ    Γ ⊢ λx : tx .r ′ : t                     Γ, π : t ⊢ e : σ  Γ⊢t                       Γ ⊢ e : ∀α.σ      Γ⊢t
                                                      T-PI NST                                      T-PG EN                                  T-I NST
                                                                   Γ ⊢ Λπ : t.e : ∀π : t.σ                       Γ ⊢ e [τ ] : σ[t/α]
                       
      Γ ⊢ e λx : tx .r ′ : σ[λx : tx .r ′ /π]

                                Figure 3. Static Semantics: Well-formedness, Subtyping and Type Checking


 • Well-formedness judgments (Γ ⊢ σ) state that a type schema                    Type Checking Rules are standard except for T-PG EN and T-
   σ is well-formed under environment Γ. That is, the judgment                   PI NST , which pertain to abstraction and instantiation of abstract
   states that the refinements in σ are boolean expressions in the               refinements. The rule T-PG EN is the same as T-F UN: we simply
   environment Γ.                                                                check the body e in the environment extended with a binding
 • Subtyping judgments (Γ ⊢ σ1  σ2 ) state that the type schema                 for the refinement variable π. The rule T-PI NST checks that the
   σ1 is a subtype of the type schema σ2 under environment Γ.                    concrete refinement is of the appropriate (unrefined) type τ , and
   That is, the judgment states that when the free variables of σ1               then replaces all (abstract) applications of π inside σ with the
   and σ2 are bound to values described by Γ, the values described               appropriate (concrete) refinement r ′ with the parameters x replaced
   by σ1 are a subset of those described by σ2 .                                 with arguments at that application. In [27] we prove the following
                                                                                 soundness result for λP which states that well-typed programs
 • Typing judgments (Γ ⊢ e : σ) state that the expression e has                  cannot crash:
   the type schema σ under environment Γ. That is, the judgment
   states that when the free variables in e are bound to values de-              Lemma (Soundness of λP [27]). If ∅ ⊢ e : σ then e 6֒→⋆P crash.
   scribed by Γ, the expression e will evaluate to a value described
   by σ.                                                                         3.3 Syntax of λB

The Well-formedness rules check that the concrete and abstract                   Figure 2 shows how we obtain the syntax for λB by extending the
refinements are indeed Bool-valued expressions in the appropriate                syntax of λP with bounded types.
environment. The key rule is WF-BASE , which checks that the
refinement r is boolean.                                                         The Types of λB extend those of λP with bounded types ρ, which
                                                                                 are the types t guarded by bounds φ.
The Subtyping rules stipulate when the set of values described
by schema σ1 is subsumed by (i.e., contained within) the values                  The Expressions of λB extend those of λP with abstraction over
described by σ2 . The rules are standard except for -BASE , which               bounds Λ{φ}.e and application of bounds e{φ}. Intuitively, if an
reduces subtyping of basic types to validity of logical implications,            expression e has some type ρ then Λ{φ}.e has the type {φ} ⇒ ρ.
by translating the refinements r and the environment Γ into logical              We include an explicit bound application form e{φ} to simplify the
formulas:                                                                        formalization; these applied bounds are automatically synthesized
           .              . ^                                                    from the type of e, and are of the form λx : ρ.true.
     [[r]] = r      [[Γ]] =    {r[x/v] | (x, {v : b | r}) ∈ Γ}
Recall that we ensure that the refinements r belong to a decidable               Notation. We write b, bhπ xi, {v : bhπ xi | r} to abbreviate
logic so that validity checking can be performed by an off-the-self              {v : b | true}, {v : b | π x v}, {v : b | r ∧ π x v} respectively. We
SMT solver.                                                                      say a type or schema is non-refined if all the refinements in it are
true. We get the shape of a type t (i.e., the System-F type) by the                 Variable Environment                Γ     ::=         ∅ | Γ, x : τ
function Shape(t) defined:
                                    .                                                 Bound Environment                 Φ     ::=         ∅ | Φ, x : τ
               Shape({v : b | r}) = b
                                    .                                       Translation                                                             Γ; Φ ⊢ e           e
   Shape({v : (x : t1 ) → t2 | r}) = Shape(t1 ) → Shape(t2 )
                                                                                                             VAR                                           C ON
                                                                                     Γ; Φ ⊢ x          x                    Γ; Φ ⊢ c                c
3.4 Translation from λB to λP
Next, we show how to translate a term from λB to one in λP .                           Γ′ = Γ, x : Shape(t)            Γ′ ; Φ ⊢ e              e′
                                                                                                                                                         F UN
We assume, without loss of generality that the terms in λB are in                       Γ; Φ ⊢ λx : t.e        λx : t.Inst(Γ′ , Φ, e′ )
Administrative Normal Form (i.e., all applications are to variables.)
                                                                              Γ; Φ ⊢ ex        e′x     Γ′ = Γ, x : Shape(t)               Γ′ ; Φ ⊢ e              e′
                                                                                                                                                                           L ET
Bounds Correspond To Functions that explicitly “witness” the                  Γ; Φ ⊢ let x : t = ex in e           let x : τ = e′x in Inst(Γ′ , Φ, e′ )
fact that the bound constraint holds at a given set of “input” values.
That is we can think of each bound as a universally quantified re-                        Γ; Φ ⊢ e1   e′1    Γ; Φ ⊢ e2                   e′2
lationship between various (abstract) refinements; by “calling” the                                                                                     A PP
                                                                                                Γ; Φ ⊢ e1 e2     e′1 e′2
function on a set of input values x1 , . . . , xn , we get to instantiate
the constraint for that particular set of values.                                 Γ; Φ ⊢ e           e′                      Γ; Φ ⊢ e                   e′
                                                                                                              TA BS                                               TA PP
Bound Environments Φ are used by our translation to track the                 Γ; Φ ⊢ Λα.e            Λα.e′                Γ; Φ ⊢ e [t]                  e′ [t]
set of bound-functions (names) that are in scope at each program
                                                                                                   Γ; Φ ⊢ e            e′
point. These names are distinct from the regular program variables                                                                         PA BS
that will be stored in Variable Environments Γ. We give bound                                Γ; Φ ⊢ Λπ : t.e           Λπ : t.e′
functions distinct names so that they cannot appear in the regular
                                                                                         Γ; Φ ⊢ e1   e′2      Γ; Φ ⊢ e1                  e′2
source, only in the places where calls are inserted by our trans-                                                                                   PA PP
lation. The translation ignores refinements entirely; both environ-                           Γ; Φ ⊢ e1 [e2 ]     e′1 [e′2 ]
ments map their names to their non-refined types.
                                                                                     fresh f         Γ; Φ, f :Shape(h|φ|i) ⊢ e                 e′
                                                                                                                                     ′
                                                                                                                                                         CA BS
The Translation is formalized in Figure 4 via a relation Γ; Φ ⊢                             Γ; Φ ⊢ Λ{φ}.e             λf : h|φ|i.e
e     e′ , that translates the expression e in λB into e′ in λP . Most
of the rules in figure 4 recursively translate the sub-expressions.                                Γ; Φ ⊢ e    e′
                                                                                                             ′
                                                                                                                                           CA PP
Types that appear inside expressions are syntactically restricted to                         Γ; Φ ⊢ e{φ}    e Const(φ)
not contain bounds, thus types inside expressions do not require
translation. Here we focus on the three interesting rules:                          Figure 4. Translation Rules from λB to λP +let

1. At bound abstractions Λ{φ}.e we convert the bound φ into a               performed by Inst(Γ, Φ, e)
   bound-function parameter of a suitable type,                                                              .
                                                                                         Inst(Γ, Φ, e)       =       Wrap(e, Instances(Γ, Φ))
2. At variable binding sites i.e., λ- or let-bindings, we use the                                            .
   bound functions to materialize the bound constraints for all the          Wrap(e, {e1 , . . . , en })     =       let t1 = e1 in . . . let tn = en in e
   variables in scope after the binding,                                                                             (where ti are fresh Bool binders)
                                                                                                             .
3. At bound applications e{φ} we provide regular functions that                      Instances(Γ, Φ)         =       { f x | f : τ ← Φ, x : ← Γ
   witness that the bound constraints hold.                                                                                , Γ, f : τ ⊢B f x : Bool}
                                                                            The function takes the environments Γ and Φ, an expression e and
                                                                            a variable x of type t and uses let-bindings to materialize all the
1. Rule CA BS translates bound abstractions Λ{φ}.e into a plain             bound functions in Φ that accept the variable x. Here, Γ ⊢B e : τ is
λ-abstraction. In the translated expression λf : h|φ|i.e′ the bound         the standard typing derivation judgment for the non-refined System
becomes a function named f with type h|φ|i defined:                         F and so we elide it for brevity.
                                 .
                   h|λx : b.φ|i = (x : b) → h|φ|i
                                 .                                          3. Rule CA PP translates bound applications e{φ} into plain λ
                           h|r|i = {v : Bool | r}                           abstractions that witness that the bound constraints hold. That is, as
That is, h|φ|i is a function type whose final output carries the refine-    within e, bounds are translated to a bound function (parameter) of
ment corresponding to the constraint in φ. Note that the translation        type h|φ|i, we translate φ into a λ-term that, via subtyping must have
generates a fresh name f for the bound function (ensuring that it           the required type h|φ|i. We construct such a function via Const(φ)
cannot be used in the regular code) and saves it in the bound envi-         that depends only on the shape of the bound, i.e., the non-refined
ronment Φ to let us materialize the bound constraint when translat-         types of its parameters (and not the actual constraint itself).
ing the body e of the abstraction.                                                                               .
                                                                                                    Const(r) = true
                                                                                                                 .
                                                                                              Const(λx : b.φ) = λx : b.Const(φ)
2. Rules F UN and L ET materialize bound constraints at variable
binding sites (λ-abstractions and let-bindings respectively.) If we         This seems odd: it is simply a constant function, how can it possi-
view the bounds as universally quantified constraints over the (ab-         bly serve as a bound? The answer is that subtyping in the translated
stract) refinements, then our translation exhaustively and eagerly          λP term will verify that in the context in which the above con-
instantiates the constraints at each point that a new binder is in-         stant function is created, the singleton true will indeed carry the
troduced into the variable environment, over all the possible can-          refinement corresponding to the bound constraint, making this syn-
didate sets of variables in scope at that point. The instantiation is       thesized constant function a valid realization of the bound function.
Recall that in the example ex2 of the overview (§ 2.4) the subtyping               Title            Director         Year    Star
constraint that decides is the constant true is a valid bound reduces              “Birdman”        “Iñárritu”     2014     8.1
to the equation 3 that is a tautology.                                             “Persepolis”     “Paronnaud”      2007     8.0

3.5 Soundness                                                                          Figure 5. Example Table of Movies
The Small-Step Operational Semantics of λB are defined by
extending a similar semantics for λP which is a standard call-          4. A Refined Relational Database
by-value calculus where abstract refinements are boolean valued
functions [27]. Let ֒→P denote the transition relation defining the     Next, we use bounded refinements to develop a library for relational
operational semantics of λP and ֒→⋆P denote the reflexive transitive    algebra, which we use to enable generic, type safe database queries.
closure of ֒→P . We thus obtain the transition relation ֒→B :           A relational database stores data in tables, that are a collection of
                                                                        rows, which in turn are records that represent a unit of data stored
        (Λ{φ}.e){φ} ֒→B e                  e ֒→B e′ , if e ֒→P e′       in the table. The tables’s schema describes the types of the values in
Let ֒→⋆B denote the reflexive transitive closure of ֒→B .               each row of the table. For example, the table in Figure 5 organizes
                                                                        information about movies, and has the schema:
The Translation is Semantics Preserving in the sense that if a           Title : String , Dir : String , Year : Int , Star : Double
source term e of λB reduces to a constant then the translated variant
of e′ also reduces to the same constant:                                   First, we show how to write type safe extensible records that
                                                                        represent rows, and use them to implement database tables (§ 4.1).
Lemma. If ∅; ∅ ⊢ e       e   ′
                                 and e ֒→⋆B c then e′ ֒→⋆P c.           Next, we show how bounds let us specify type safe relational
                                                                        operations and how they may be used to write safe database
The Soundness of λB follows by combining the above Semantics            queries (§ 4.2).
Preservation Lemma with the soundness of λP .
                                                                        4.1 Rows and Tables
To Typecheck a λB program e we translate it into a λP program
e′ and then type check e′ ; if the latter check is safe, then we are    We represent the rows of a database with dictionaries, which are
guaranteed that the source term e will not crash:                       maps from a set of keys to values. In the sequel, each key corre-
                                                                        sponds to a column, and the mapped value corresponds to a valua-
Theorem (Soundness). If ∅; ∅ ⊢ e               e′ and ∅ ⊢ e′ : σ then   tion of the column in a particular row.
e 6֒→⋆B crash.
                                                                        A dictionary Dict <r> k v maps a key x of type k to a value of
                                                                        type v that satisfies the property r x
3.6 Inference
                                                                          type Range k v = k → v → Bool
A critical feature of bounded refinements is that we can au-
tomatically synthesize instantiations of the abstract refinements         data Dict k v <r :: Range k v > = D {
by: (1) generating templates corresponding to the unknown types               dkeys :: [ k ]
where fresh variables κ denote the unknown refinements that an              , dfun :: x :{ k | x ∈ elts dkeys } → v < r x >
abstract refinement parameter π is instantiated with, (2) generating        }
subtyping constraints over the resulting templates, and (3) solving
                                                                        Each dictionary d has a domain dkeys i.e., the list of keys for which
the constraints via abstract interpretation.
                                                                        d is defined and a function dfun that is defined only on elements x
                                                                        of the domain dkeys. For each such element x, dfun returns a value
Inference Requires Monotonic Constraints. Abstract interpreta-          that satisfies the property r x.
tion only works if the constraints are monotonic [5], which in this
case means that the κ variables, and correspondingly, the abstract      Propositions about the theory of sets can be decided efficiently
refinements π must only appear in positive positions within refine-     by modern SMT solvers. Hence we use such propositions within
ments (i.e., not under logical negations). The syntax of refinements    refinements [28]. The measures (logical functions) elts and keys
shown in Figure 1 violates this requirement via refinements of the      specify the set of keys in a list and a dictionary respectively:
form π x ⇒ r.
                                                                          elts            :: [a ] → Set a
                                                                          elts ([])       = ∅
We restrict implications to bounds i.e., prohibit them from ap-           elts ( x : xs ) = { x} ∪ elts xs
pearing elsewhere in type specifications. Consequently, the impli-
cations only appear in the output type of the (first order) “ghost”       keys             :: Dict k v → Set k
functions that bounds are translated to. The resulting subtyping          keys d           = elts ( dkeys d )
constraints only have implications inside super-types, i.e., as:
         Γ ⊢ {v:b | a}  {v:b | a1 ⇒ · · · ⇒ an ⇒ aq }                  Domain and Range of dictionaries. In order to precisely define
                                                                        the domain (e.g., columns) and range (e.g., values) of a dictionary
By taking into account the semantics of subtyping, we can push the      (e.g., row), we define the following aliases:
antecedents into the environment, i.e., transform the above into an
equivalent constraint in the form:                                        type RD k v < dom :: Dom k v , rng :: Range k v >
                                                                            = { v : Dict < rng > k v | dom v}
 Γ, x1 :b1 | a′1 , . . . , xn :bn | a′n ⊢ v:b | a′  v:b | a′q
                                                    
                                                                          type Dom k v = Dict k v → Bool
where all the abstract refinements variables π (and hence instance
variables κ) appear positively, ensuring that the constraints are       We may instantiate dom and rng with predicates that precisely
monotonic, hence permitting inference via Liquid Typing [21].           describe the values contained with the dictionary. For example,
  RD < λd → keys d == {" x " }                                             isI _            = False
     , λk v → 0 < v            > String Int
                                                                           toI         :: { v : Univ | isI v} → Int
describes dictionaries with a single field "x" whose value (as deter-      toI ( I n ) = n
mined by dfun) is stricly greater than 0. We will define schemas by      ...
appropriately instantiating the abstract refinements dom and rng.
                                                                         The predicate md describes the domain of the movie schema, re-
An empty dictionary      has an empty domain and a function that         stricting the keys to exactly "year", "star", "dir", and "title".
will never be called:                                                    The range predicate mr describes the types of the values in the
                                                                         schema: a dictionary of type MovieSchema must map "year" to
   empty      :: RD < emptyRD , rFalse > k v                             an Int, "star" to a Double, and "dir" and "title" to Strings.
   empty      = D [] (λx → error " calling empty " )                     The range predicate may be used to impose additional constraints
                                                                         on the values stored in the dictionary. For instance, mr restricts the
   emptyRD = λd → keys d == ∅
   rFalse = λk v → false                                                 year to be not only an integer but also greater than 1888.
                                                                         We populate the Movie Schema by extending the empty dictio-
We define singleton maps as dependent pairs x := y which de-             nary with the appropriate pairs of fields and values. For example,
note the mapping from x to y:                                            here are the rows from the table in Figure 5
  data P k v <r :: Range k v >                                             movie1 , movie2 ::        MovieSchema
    = (:=) { pk :: k , pv :: v < r pk >}                                   movie1 = ( " title "      := S " Persepolis " )
                                                                                  += ( " dir "       := S " Paronnaud ")
Thus, key := val has type P<r> k v only if r key val.                             += ( " star "      := D 8)
                                                                                  += ( " year "      := I 2007)
A dictionary may be extended with a singleton binding (which                      += empty
maps the new key to its new value).
                                                                           movie2 = ( " title "      :=   S   " Birdman " )
  (+=)      :: bind :P <r > k v                                                  += ( " star "       :=   D   8.1)
            → dict :RD < pTrue , r > k v                                         += ( " dir "        :=   S   " Inarritu " )
            → RD < addKey ( pk bind ) dict , r > k v                             += ( " year "       :=   I   2014)
                                                                                 += empty
  ( k := v ) += ( D ks f )
           = D ( k : ks )                                                Typing movie1 (and movie2) as MovieSchema boils down
               (λi → if i == k then v else f i )                         to proving: That keys movie1 = {"year", "star", "dir",
                                                                         "title"}; and that each key is mapped to an appropriate value
   addKey = λk d d ’ → keys d ’ == { k } ∪ keys d                        as determined by mr. For example, declaring movie1’s year to be
   pTrue = λ_ → true                                                     I 1888 or even misspelling "dir" as "Dir" will cause the movie1
                                                                         to become ill-typed. As the (sub)typing relation depends on logical
Thus, (k := v) += d evaluates to a dictionary d’ that extends d          implication (unlike in HList based approaches [12]) key ordering
with the mapping from k to v. The type of (+=) constrains the            does not affect type-checking; in movie1 the star field is added be-
new binding bind, the old dictionary dict and the returned value         fore the director, while movie2 follows the opposite order.
to have the same range invariant r. The return type states that the
output dictionary’s domain is that of the domain of dict extended        Database Tables are collections of rows, i.e., collections of re-
by the new key (pk bind).                                                fined dictionaries. We define a type alias RT s (Refined Table) for
                                                                         the list of refined dictionaries from the field type String to the
To model a row in a table i.e., a schema, we define the unrefined        Universe.
(Haskell) type Schema, which is a dictionary mapping Strings, i.e.,
                                                                           type RT (s :: { dom :: TDom , rng :: TRange })
the names of the fields of the row, to elements of some universe
                                                                             = [ RD <s . dom , s . rng > String Univ ]
Univ containing Int, String and Double. (A closed universe is not
a practical restriction; most databases support a fixed set of types.)     type TDom   = Dom   String Univ
  data Univ        = I Int | S String | D Double                           type TRange = Range String Univ

  type Schema = RD String Univ                                           For brevity we pack both the domain and the range refinements
                                                                         into a record s that describes the schema refinement; i.e., each row
                                                                         dictionary has domain s.dom and range s.rng.
We refine Schema with concrete instantiations for dom and rng,               For example, the table from Figure 5 can be represented as a
in order to recover precise specifications for a particular database.    type MoviesTable which is an RT refined with the domain and
For example, MovieSchema is a refined Schema that describes the          range md and mr described earlier (§ 4.1):
rows of the Movie table in Figure 5:
                                                                           type MoviesTable = RT { dom = md , rng = mr }
type MovieSchema = RD <md , mr > String Univ
                                                                           movies :: MoviesTable
  md = λd →                                                                movies = [ movie1 , movie2 ]
      keys d ={ " year " ," star " ," dir " ," title " }
  mr = λk v →
      ( k = " year " ⇒ isI v && 1888 < toI v )                           4.2 Relational Algebra
   && ( k = " star " ⇒ isD v && 0 ≤ toD v ≤ 10)
   && ( k = " dir "    ⇒ isS v )                                         Next, we describe the types of the relational algebra operators
   && ( k = " title " ⇒ isS v )                                          which can be used to manipulate refined rows and tables. For space
                                                                         reasons, we show the types of the basic relational operators; their
  isI ( I _ )      = True                                                (verified) implementations can be found online [24].
   union   ::   RT s → RT s → RT s                                          good_titles = project [" title " ] $ select (λd →
   diff    ::   RT s → RT s → RT s                                                          toDouble ( dfun d $ " star ") > 8
   select  ::   ( RD s → Bool ) → RT s → RT s                                             ) movies
   project ::   ks :[ String ] → RTSubEqFlds ks s
           →    RTEqFlds ks s                                                Finally, note that our entire library – including records, tables,
   product ::   ( Disjoint s1 s2 , Union s1 s2 s                         and relational combinators – is built using vanilla Haskell i.e., with-
                , Range s1 s , Range s2 s )                              out any type level computation. All schema reasoning happens at
              ⇒ RT s1 → RT s2 → RT s                                     the granularity of the logical refinements. That is if the refinements
                                                                         are erased from the source, we still have a well-typed Haskell pro-
union and diff compute the union and difference, respectively            gram but of course, lose the safety guarantees about operations
of the (rows of) two tables. The types of union and diff state that      (e.g., “dynamic” key lookup) never failing at run-time.
the operators work on tables with the same schema s and return a
table with the same schema.                                              5. A Refined IO Monad
select takes a predicate p and a table t and filters the rows of         Next, we illustrate the expressiveness of Bounded Refinements
t to those which that satisfy p. The type of select ensures that p       by showing how they enable the specification and verification of
will not reference columns (fields) that are not mapped in t, as the     stateful computations. We show how to (1) implement a refined
predicate p is constrained to require a dictionary with schema s.        state transformer (RIO) monad, where the transformer is indexed
                                                                         by refinements corresponding to pre- and post-conditions on the
project takes a list of String fields ks and a table t and projects      state (§ 5.1), (2) extend RIO with a set of combinators for imperative
exactly the fields ks at each row of t. project’s type states that for   programming, i.e., whose types precisely encode Floyd-Hoare style
any schema s, the input table has type RTSubEqFlds ks s i.e., its        program logics (§ 5.2) and (3) use the RIO monad to write safe
domain should have at least the fields ks and the result table has       scripts where the type system precisely tracks capabilities and
type RTEqFlds ks s, i.e., its domain has exactly the elements ks.        statically ensures that functions only access specific resources (§ 6).
   type RTSubEqFlds ks s
     = RT s { dom = λz → elts ks ⊆                keys z}                5.1 The RIO Monad

   type RTEqFlds ks s
                                                                         The RIO data type describes stateful computations. Intuitively, a
     = RT s { dom = λz → elts ks == keys z}                              value of type RIO a denotes a computation that, when evaluated
                                                                         in an input World produces a value of type a (or diverges) and a
The range of the argument and the result tables is the same and          potentially transformed output World. We implement RIO a as an
equal to s.rng.                                                          abstractly refined type (as described in [27])
                                                                           type Pre    = World → Bool
product takes two tables as input and returns their (Cartesian)            type Post a = World → a → World → Bool
product. It takes two Refined Tables with schemata s1 and s2
and returns a Refined Table with schema s. Intuitively, the output         data RIO a <p :: Pre , q :: Post a > = RIO {
schema is the “concatenation” of the input schema; we formalize              runState :: w : World <p > → (x :a , World < q w x >)
this notion using bounds: (1) Disjoint s1 s2 says the domains of           }
s1 and s2 should be disjoint, (2) Union s1 s2 s says the domain
of s is the union of the domains of s1 and s2, (3) Range s1 s (resp.     That is, RIO a is a function World→(a, World), where World is
Range s2 s2) says the range of s1 should imply the result range          a primitive type that represents the state of the machine i.e., the
s; together the two imply the output schema s preserves the type of      console, file system, etc. This indexing notion is directly inspired
each key in s1 or s2.                                                    by the method of [8] (also used in [16]).

   bound Disjoint s1 s2 = λx y →                                         Our Post-conditions are Two-State Predicates that relate the
     s1 . dom x ⇒ s2 . dom y ⇒ keys x ∩ keys y == ∅                      input- and output- world (as in [16]). Classical Floyd-Hoare logic,
                                                                         in contrast, uses assertions which are single-state predicates. We
   bound Union s1 s2 s = λx y v →                                        use two-states to smoothly account for specifications for stateful
     s1 . dom x ⇒ s2 . dom y                                             procedures. This increased expressiveness makes the types slightly
                ⇒ keys v == keys x ∪ keys y                              more complex than a direct one-state encoding which is, of course
                ⇒ s . dom v
                                                                         also possible with bounded refinements.
   bound Range si s = λx k v →
     si . dom x ⇒ k ∈ keys x ⇒ si . rng k v
                                                                         An RIO computation is parameterized by two abstract refine-
                ⇒ s . rng k v                                            ments: (1) p :: Pre, which is a predicate over the input world,
                                                                         i.e., the input world w satisfies the refinement p w; and (2) q ::
    Thus, bounded refinements enable the precise typing of re-           Post a, which is a predicate relating the output world with the in-
lational algebra operations. They let us describe precisely when         put world and the value returned by the computation, i.e., the output
union, intersection, selection, projection and products can be com-      world w’ satisfies the refinement q w x w’ where x is the value re-
puted, and let us determine, at compile time the exact “shape” of        turned by the computation. Next, to use RIO as a monad, we define
the resulting tables.                                                    bind and return functions for it, that satisfy the monad laws.

We can query Databases by writing functions that use the rela-           The return operator yields a pair of the supplied value z and the
tional algebra combinators. For example, here is a query that re-        input world unchanged:
turns the “good” titles – with more than 8 stars – from the movies          return   :: z : a → RIO <p , ret z > a
table 1                                                                     return z = RIO $ λw → (z , w )
1 More example queries can be found online [24]                            ret z        = λw x w ’ → w ’ == w && x == z
The type of return states that for any precondition p and any            We Read and Write Mutable Variables via suitable “get” and
supplied value z of type a, the expression return z is an RIO            “set” actions. For example, we can read and write ctr via:
computation with precondition p and a post-condition ret z. The            getCtr       :: RIO < pTrue , rdCtr > Int
postcondition states that: (1) the output World is the same as the         getCtr       = RIO $ λw → ( ctr w , w )
input, and (2) the result equals to the supplied value z. Note that as
a consequence of the equality of the two worlds and congruence,            setCtr   :: Int → RIO < pTrue , wrCtr n > ()
the output world w’ trivially satisfies p w’.                              setCtr n = RIO $ λw → (() , w { ctr = n })

The >>= Operator is defined in the usual way. However, to type           Here, the refinements are defined as:
it precisely, we require bounded refinements.                              pTrue = λw → True
                                                                           rdCtr = λw x w ’ → w ’ == w && x == select w ctr
  ( >>= ) ::   ( Ret q1 r , Seq r q1 p2 , Trans q1 q2 q )                  wrCtr n = λw _ w ’ → w ’ == update w ctr n
          ⇒    m : RIO <p , q1 > a
          →    k :( x :a <r > → RIO < p2 x , q2 x > b )                  Hence, the post-condition of getCtr states that it returns the current
          →    RIO <p , q > b                                            value of ctr, encoded in the refinement logic with McCarthy’s
                                                                         select operator while leaving the world unchanged. The post-
  ( RIO g ) >>= f = RIO $ λx →                                           condition of setCtr states that World is updated at the address
     case g x of { (y , s ) → runState ( f y ) s }
                                                                         corresponding to ctr, encoded via McCarthy’s update operator.
The bounds capture various sequencing requirements (c.f. the             The ifM combinator takes as input a cond action that returns a
Floyd-Hoare rules of consequence). First, the output of the first ac-    Bool and, depending upon the result, executes either the then or
tion m, satisfies the refinement required by the continuation k;         else actions. We type it as:
   bound Ret q1 r = λw x w ’ → q1 w x w ’ ⇒ r x                            bound Pure g = λw x v → ( g w x v ⇒ v == w)
                                                                           bound Then g p1 = λw v → ( g w True v ⇒ p1 v )
                                                                           bound Else g p2 = λw v → ( g w False v ⇒ p2 v )
Second, the computations may be sequenced, i.e., the postcondition
of the first action m implies the precondition of the continuation k       ifM ::    ( Pure g , Then g p1 , Else g p2 )
(which may be dependent upon the supplied value x):                            ⇒     RIO <p , g > Bool         -- cond
                                                                               →     RIO <p1 , q > a           -- then
   bound Seq q1 p2 = λw x w ’ →                                                →     RIO <p2 , q > a           -- else
         q1 w x w ’ ⇒ p2 x w ’                                                 →     RIO <p , q > a

Third, the transitive composition of the two computations, implies       The abstract refinements and bounds correspond exactly to the hy-
the final postcondition:                                                 potheses in the Floyd-Hoare rule for the if statement. The bound
                                                                         Pure g states that the cond action may access but does not modify
   bound Trans q1 q2 q = λw x w ’ y w ’ ’ →                              the World, i.e., the output is the same as the input World. (In clas-
         q1 w x w ’ ⇒ q2 x w ’ y w ’ ’ ⇒ q w y w ’ ’
                                                                         sical Floyd-Hoare formulations this is done by syntactically sepa-
                                                                         rating terms into pure expressions and side effecting statements).
   Both type signatures would be impossible to use if the program-       The bound Then g p1 and Else g p2 respectively state that the
mer had to manually instantiate the abstract refinements (i.e., pre-     preconditions of the then and else actions are established when
and post-conditions.) Fortunately, Liquid Type inference generates       the cond returns True and False respectively.
the instantiations making it practical to use L IQUID H ASKELL to
verify stateful computations written using do-notation.                  We can use ifM to implement a stateful computation that per-
                                                                         forms a division, after checking the divisor is non-zero. We specify
5.2 Floyd-Hoare Logic in the RIO Monad                                   that div should not be called with a zero divisor. Then, L IQUID -
                                                                         H ASKELL verifies that div is called safely:
Next, we use bounded refinements to derive an encoding of Floyd-           div :: Int → { v: Int | v /= 0} → Int
Hoare logic, by showing how to read and write (mutable) variables
and typing higher order ifM and whileM combinators.                        ifTest :: RIO Int
                                                                           ifTest = ifM nonZero divX ( return 10)
We Encode Mutable Variables as fields of the World type. For                 where nonZero = getCtr >>= return . (/= 0)
example, we might encode a global counter as a field:                              divX    = getCtr >>= return . ( div 42)

  data World = { ... , ctr :: Int , ... }                                Verification succeeds as the post-condition of nonZero is in-
                                                                         stantiated to λ_ b w →b ⇔ select w ctr /= 0 and the pre-
We encode mutable variables in the refinement logic using Mc-            condition of divX’s is instantiated to λw →select w ctr /= 0,
Carthy’s select and update operators for finite maps and the as-         which suffices to prove that div is only called with non-zero values.
sociated axiom:                                                          The whileM combinator       formalizes loops as RIO computations:
   select :: Map k v → k → v                                               whileM ::     ( OneState q , Inv p g b , Exit p g q )
   update :: Map k v → k → v → Map k v                                            ⇒      RIO <p , g > Bool      -- cond
                                                                                  →      RIO < pTrue , b > ()   -- body
  ∀ m , k1 , k2 , v .                                                             →      RIO <p , q > ()
        select ( update m k1 v ) k2
    == ( if k1 == k2 then v else select m k2 v )                         As with ifM, the hypotheses of the Floyd-Hoare derivation rule
                                                                         become bounds for the signature. Given a condition with pre-
The quantifier free theory of select and update is decidable and         condition p and post-condition g and body with a true precondi-
implemented in modern SMT solvers [1].                                   tion and post-condition b, the computation whileM cond body has
pread , pwrite , plookup , pcontents ,
                                                                             In this section, we turn to the problem of preventing Shill
pcreateD , pcreateF , pcreateFP :: Priv → Bool                            runtime failures. (In general, the verification of file system resource
                                                                          usage is a rich topic outside the scope of this paper.) That is,
active      :: World → Set FH                                             assuming the Shill runtime and an API as described in [15],
caps        :: World → Map FH Priv                                        how can we use Bounded Refinement Types to encode scripting
                                                                          privileges and reason about them statically?
pset p h = λw → p ( select ( caps w ) h ) &&
                h ∈ active w                                              We use RIO types to specify Shill’s API operations thereby
                                                                          providing compile-time guarantees about privilege and resource
                 Figure 6. Privilege Specification                        usage. To achieve this, we: connect the state (World) of the RIO
                                                                          monad with a privilege specification denoting the set of privileges
                                                                          that a program may use (§ 6.1); specify the file system API in terms
precondition p and post-condition q as long as the bounds (cor-           of this abstraction (§ 6.2); and use the above to specify and verify
responding to the Hypotheses in the Floyd-Hoare derivation rule)          the particular privileges that a client of the API uses (§ 6.3).
hold. First, p should be a loop invariant; i.e., when the condition
returns True the post-condition of the body b must imply the p:
                                                                          6.1 Privilege Specification
   bound Inv p g b = λw w ’ w ’ ’ →
       p w ⇒ g w True w ’ ⇒ b w ’ () w ’ ’ ⇒ p w ’ ’                      Figure 6 summarizes how we specify privileges inside RIO. We
                                                                          use the type FH to denote a file handles, analogous to Shill’s
Second, when the condition returns False the invariant p should           capabilities. An abstract type Priv denotes the sets of privileges
imply the loop’s post-condition q:                                        that may be associated with a particular FH.
   bound Exit p g q = λw w ’ →                                            To connect Worlds with Privileges we assume a set of uninter-
         p w ⇒ g w False w ’ ⇒ q w () w ’
                                                                          preted functions of type Priv → Bool that act as predicates on
Third, to avoid having to transitively connect the guard and the          values of type Priv, each denoting a particular privilege. For ex-
body, we require that the loop post-condition be a one-state predi-       ample, given a value p :: Priv, the proposition pread p denotes
cate, independent of the input world (as in Floyd-Hoare logic):           that p includes the “read” privilege. The function caps associates
                                                                          each World with a Map FH Priv, a table that associates each FH
   bound OneState q = λw w ’ w ’ ’ →                                      with its privileges. The function active maps each World to the
         q w () w ’ ’ ⇒ q w ’ () w ’ ’                                    Set of allocated FHs. Given x:FH and w:World, pwrite (select
                                                                          (caps w)x) denotes that in the state w, the file x may be written.
We can use whileM to implement a loop that repeatedly decre-              This pattern is generalized by the predicate pset pwrite x w.
ments a counter while it is positive, and to then verify that if it was
initially non-negative, then at the end the counter is equal to 0.        6.2 File System API Specification
   whileTest   :: RIO < posCtr , zeroCtr > ()                             A privilege tracking file system API can be partitioned into the priv-
   whileTest = whileM gtZeroX decr                                        ilege preserving operations and the privilege extending operations.
     where gtZeroX = getCtr >>= return . ( > 0)
                                                                          To type the privilege preserving operations, we define a predicate
   posCtr = λw → 0 ≤ select w ctr                                         eqP w w’ that says that the set of privileges and active handles in
   zeroCtr = λ_ _ w ’ → 0 == select w ctr                                 worlds w and w’ are equivalent.
Where the decrement is implemented by decr with type:                       eqP = λw _ w ’ →
                                                                              caps w == caps w ’ && active w == active w ’
   decr :: RIO < pTrue , decCtr > ()
                                                                          We can now specify the privilege preserving operations that read
   decCtr = λw _ w ’ →
     w ’ == update w ctr (( select ctr w ) - 1)
                                                                          and write files, and list the contents of a directory, all of which
                                                                          require the capabilities to do so in their pre-conditions:
L IQUID H ASKELL verifies that at the end of whileTest the counter          read :: { - Read the contents of h -}
is zero (i.e., the post-condition zeroCtr) by instantiating suitable          h: FH → RIO < pset pread h , eqp > String
(i.e., inductive) refinements for this particular use of whileM.
                                                                             write :: { - Write to the file h -}
                                                                               h: FH → String → RIO < pset pwrite h , eqp > ()
6. Capability Safe Scripting via RIO
                                                                             contents :: { - List the children of h -}
Next, we describe how we use the RIO monad to reason about shell               h: FH → RIO < pset pcontents h , eqp > [ Path ]
scripting, inspired by the Shill [15] programming language.

Shill is a scripting language that restricts the privileges with          To type the privilege extending operations, we define predicates
which a script may execute by using capabilities and dynamic con-         that say that the output world is suitably extended. First, each such
tract checking [15] . Capabilities are run-time values that witness       operation allocates a new handle, which is formalized as:
the right to use a particular resource (e.g., a file). A capability is       alloc w ’ w x =
associated with a set of privileges, each denoting the permission              (x 6∈ active w ) && active w ’ == { x } ∪ active w
to use the capability in a particular way (such as the permission
to write to a file). A contract for a Shill procedure describes the       which says that the active handles in (the new World) w’ are those
required input capabilities and any output values. The Shill run-         of (the old World) w extended with the hitherto inactive handle x.
time guarantees that system resources are accessed in the manner          Typically, after allocating a new handle, a script will want to add
described by its contract.                                                privileges to the handle that are obtained from existing privileges.
To create a new file in a directory with handle h we want the           Furthermore, we want to restrict the privileges on newly created
new file to have the privileges derived from pcreateFP (select          files to the write privilege, since copyRec does not need to read
(caps w)h) (i.e., the create privileges of h). We formalize this by     from or otherwise modify these files.
defining the post-condition of create as the predicate derivP:              Even though the above type is sufficient to verify the vari-
  derivP h = λw x w ’ →                                                 ous clients of copySpec it is insufficient to verify copySpec’s im-
    alloc w ’ w x &&                                                    plementation, as the postcondition merely states that copySpec
    caps w ’ == store ( caps w ) x                                      s d w holds. Looking at the recursive call in the last line of
                   ( pcreateFP ( select ( caps w ) ) h )                copySpec’s implementation, the output world w is only known to
                                                                        satisfy copySpec x y w (having substituted the formal parameters
  create :: { - Create a file -}                                        s and d with the actual x and y), with no mention of s or d! Thus, it
    h : FH → Path → RIO < pset pcreateF h , derivP h > FH
                                                                        is impossible to satisfy the postcondition of copyRec, as informa-
Thus, if h is writable in the old World w (pwrite (pcreateFP            tion about s and d has been lost.
(select (caps w)h))) and x is derived from h (derivP w’ w x
                                                                        Framing is introduced to address the above problem. Intuitively,
h both hold), then we know that x is writable in the new World w’
                                                                        because no privileges are ever revoked, if a privilege for a file
(pwrite (select (caps w’)x)).
                                                                        existed before the recursive call, then it exists after as well. We
To lookup existing files or create sub-directories, we want to          thus introduce a notion of framing – assertions about unmodified
directly copy the privileges of the parent handle. We do this by        state that hold before calling copyRec must hold after copyRec
using a predicate copyP as the post-condition for the two functions:    returns. Solidifying this intuition, we define a predicate i to be
                                                                        Stable when assuming that the predicate i holds on w, if i only
  copyP h = λw x w ’ →                                                  depends on the allocated set of privileges, then i will hold on a
    alloc w ’ w x &&                                                    world w’ so long as the set of priviliges in w’ contains those in
    caps w ’ == store ( caps w ) x                                      w. The definition of Stable is derived precisely from the ways in
                      ( select ( caps w ) y )
                                                                        which the file system API may modify the current set of privileges:
  lookup :: { - Open a child of h -}                                      bound Stable i = λx y w w ’ →
    h : FH → Path → RIO < pset plookup h , copyP h > FH                    i w ⇒ ( eqP w () w ’ || copyP y w x w ’
                                                                                   || derivP y w x w ’
  createDir :: { - Create a directory -}                                          ) ⇒ i w’
    h : FH → Path → RIO < pset pcreateD h , copyP h > FH
                                                                        We thus parameterize copyRec by a predicate i, bounded by
6.3 Client Script Verification                                          Stable i, which precisely describes the possible world transfor-
                                                                        mations under which i should be stable:
We now turn to a client script, the program copyRec that copies the       copyFrame i s d = λw → i w && copySpec s d w
contents of the directory f to the directory d.
  copyRec recur s d =                                                     copyRec :: ( Stable i ) ⇒
    do cs <- contents s                                                              Bool → s : FH → d : FH →
       forM_ cs $ λ p → do                                                           RIO < copyFrame i s d ,
         x <- flookup s p                                                                 λ_ _ w → copyFrame i s d w > ()
         when ( isFile x ) $ do
           y <- create d p                                              Now, we can verify copyRec’s body, as at the recursive call that
           s <- fread x                                                 appears in the last line of the implementation, i is instantiated with
           write y s                                                    λw →copySpec s d w.
         when ( recur && ( isDir x )) $ do
           y <- createDir d p
           copyRec recur x y                                            7. Related Work
copyRec executes by first listing the contents of f, and then opening   Higher order Logics and Dependent Type Systems includ-
each child path p in f. If the result is a file, it is copied to the    ing NuPRL [4], Coq [3], Agda [18], and even to some extent,
directory d. Otherwise, copyRec recurses on p, if recur is true.        Haskell [14, 20], occupy the maximal extreme of the expressive-
                                                                        ness spectrum. However, in these settings, checking requires ex-
    In a first attempt to type copyRec we give it the following type:
                                                                        plicit proof terms which can add considerable programmer over-
  copyRec :: Bool → s : FH → d : FH →                                   head. Our goal is to eliminate the programmer overhead of proof
             RIO < copySpec s d ,                                       construction by restricting specifications to decidable, first order
                  λ_ _ w → copySpec s d w > ()                          logics and to see how far we can go without giving up on expres-
                                                                        siveness. The F* system enables full dependent typing via SMT
 copySpec h d = λw →
                                                                        solvers via a higher-order universally quantified logic that permit
   pset pcontents h w && pset plookup h          w &&
   pset pread h      w && pset pcreateFile d w &&                       specifications similar to ours (e.g., compose, filter and foldr).
   pset pwrite d     w && pset pcreateF d        w &&                   While this approach is at least as expressive as bounded refine-
   pwrite ( pcreateFP ( select ( caps w ) d )) )                        ments it has two drawbacks. First, due to the quantifiers, the gener-
                                                                        ated VCs fall outside the SMT decidable theories. This renders the
The above specification gives copyRec a minimal set of privileges.      type system undecidable (in theory), forcing a dependency on the
Given a source directory handle s and destination handle d, the         solver’s unpredictable quantifier instantiation heuristics (in prac-
copyRec must at least: (1) list the contents of s (pcontents),          tice). Second, more importantly, the higher order predicates must
(2) open children of s (plookup), (3) read from children of s           be explicitly instantiated, placing a heavy annotation burden on the
(pread), (4) create directories in d (pcreateD), (5) create files       programmer. In contrast, bounds permit decidable checking, and
in d (pcreateF), an (6) write to (created) files in d (pwrite).         are automatically instantiated via Liquid Types.
Our notion of Refinement Types has its roots in the predicate           Acknowledgments
subtyping of PVS [22] and indexed types (DML [30]) where types
are constrained by predicates drawn from a logic. To ensure decid-      We thank the anonymous reviewers and Colin Gordon for providing
able checking several refinement type systems including [6, 29, 30]     invaluable feedback about earlier drafts of this paper.
restrict refinements to decidable, quantifier free logics. While this   References
ensures predictable checking and inference [21] it severely limits       [1] C. Barrett, A. Stump, and C. Tinelli. http://smt-lib.org.
the language of specifications, and makes it hard to fashion simple      [2] J. Bengtson, K. Bhargavan, C. Fournet, A. D. Gordon, and S. Maffeis.
higher order abstractions like filter (let alone the more complex            Refinement types for secure implementations. ACM TOPLAS, 2011.
ones like relational algebras and state transformers.)                   [3] Y. Bertot and P. Castéran. Coq’Art: The Calculus of Inductive Con-
                                                                             structions. Springer Verlag, 2004.
                                                                         [4] R.L. Constable. Implementing Mathematics with the Nuprl Proof
To Reconcile Expressiveness and Decidability C ATALYST [11]
                                                                             Development System. Prentice-Hall, 1986.
permits a form of higher order specifications where refinements are
relations which may themselves be parameterized by other rela-           [5] P. Cousot and R. Cousot. Abstract interpretation: a unified lattice
                                                                             model for the static analysis of programs. In POPL, 1977.
tions, which allows for example, a way to precisely type filter
by suitably composing relations. However, to ensure decidable            [6] J. Dunfield. Refined typechecking with Stardust. In PLPV, 2007.
checking, C ATALYST is limited to relations that can be specified        [7] R. A. Eisenberg and S. Weirich. Dependently typed programming with
as catamorphisms over inductive types, precluding for example,               singletons. In Haskell, 2012.
theories like arithmetic. More importantly, (like F*), C ATALYST         [8] J.C. Filliâtre. Proof of imperative programs in type theory. In TYPES,
provides no inference: higher order relations must be explicitly in-         1998.
stantiated. Bounded refinements build directly upon abstract refine-     [9] C. Fournet, M. Kohlweiss, and P-Y. Strub. Modular code-based cryp-
ments [27], a form of refinement polymorphism analogous to para-             tographic verification. In CCS, 2011.
metric polymorphism. While [27] adds expressiveness via abstract        [10] A. Guha, M. Fredrikson, B. Livshits, and N. Swamy. Verified security
refinements, without bounds we cannot specify any relationships              for browser extensions. In IEEE S & P, 2011.
between the abstract refinements. The addition of bounds makes it       [11] G. Kaki and S. Jagannathan. A relational framework for higher-order
possible to specify and verify the examples shown in this paper,             shape analysis. In ICFP, 2014.
while preserving decidability and inference.
                                                                        [12] O. Kiselyov, R. Lämmel, and K. Schupke. Strongly typed heteroge-
                                                                             neous collections. In Haskell, 2004.
Our Relational Algebra Library builds on a long line of work            [13] D. Leijen and E. Meijer. Domain specific embedded compilers. In
on type safe database access. The HaskellDB [13] showed how                  DSL, 1999.
phantom types could be used to eliminate certain classes of er-         [14] C. McBride. Simulating dependent types in Haskell. In JFP, 2002.
rors. Haskell’s HList library [12] extends this work with type-level    [15] S. Moore, C. Dimoulas, D. King, and S. Chong. SHILL: A secure
computation features to encode heterogeneous lists, which can be             shell scripting language. In OSDI, 2014.
used to encode database schema, and (unlike HaskellDB) statically       [16] A. Nanevski, G. Morrisett, A. Shinnar, P. Govereau, and L. Birkedal.
reject accesses of “missing” fields. The HList implementation is             Ynot: Dependent types for imperative programs. In ICFP, 2008.
non-trivial, requiring new type-classes for new operations (e.g.,       [17] G. Nelson. Techniques for program verification. Technical Report
appending lists); [19] shows how a dependently typed language                CSL81-10, Xerox Palo Alto Research Center, 1981.
greatly simplifies the implementation. Much of this simplicity can      [18] U. Norell. Towards a practical programming language based on
be recovered in Haskell using the singleton library [7]. Our goal            dependent type theory. PhD thesis, Chalmers, 2007.
is to show that bounded refinements are expressive enough to per-       [19] N. Oury and W. Swierstra. The power of Pi. In ICFP, 2008.
mit the construction of rich abstractions like a relational algebra
and generic combinators for safe database access while using SMT        [20] S. L. Peyton-Jones, D. Vytiniotis, S. Weirich, and G. Washburn. Sim-
                                                                             ple unification-based type inference for GADTs. In ICFP, 2006.
solvers to provide decidable checking and inference. Further, un-
like the HList based approaches, refinements they can be used to        [21] P. Rondon, M. Kawaguchi, and R. Jhala. Liquid types. In PLDI, 2008.
retroactively or gradually verify safety; if we erase the types we      [22] J. Rushby, S. Owre, and N. Shankar. Subtypes for specifications:
still get a valid Haskell program operating over homogeneous lists.          Predicate subtyping in pvs. IEEE TSE, 1998.
                                                                        [23] N. Swamy, J. Weinberger, C. Schlesinger, J. Chen, and B. Livshits.
                                                                             Verifying higher-order programs with the dijkstra monad. In PLDI,
Our Approach for Verifying Stateful Computations using mon-                  2013.
ads indexed by pre- and post-conditions is inspired by the method       [24] UCSD Programming Systems. github.com/ucsd-progsys/liquidhaskell/tree/mas
of Filliâtre [8], which was later enriched with separation logic in    [25] S. Tobin-Hochstadt and M. Felleisen. Logical types for untyped
Ynot [16]. In future work it would be interesting to use separation          languages. In ICFP, 2010.
logic based refinements to specify and verify the complex sharing
                                                                        [26] H. Unno, T. Terauchi, and N. Kobayashi. Relatively complete verifi-
and aliasing patterns allowed by Ynot. F* encodes stateful compu-            cation of higher-order functional programs. In POPL, 2013.
tations in a special Dijkstra Monad [23] that replaces the two as-
sertions with a single (weakest-precondition) predicate transformer     [27] N. Vazou, P. Rondon, and R. Jhala. Abstract refinement types. In
                                                                             ESOP, 2013.
which can be composed across sub-computations to yield a trans-
former for the entire computation. Our RIO approach uses the idea       [28] N. Vazou, E. L. Seidel, and R. Jhala. Liquidhaskell: Experience with
of indexed monads but has two concrete advantages. First, we show            refinement types in the real world. In Haskell, 2014.
how bounded refinements alone suffice to let us fashion the RIO ab-     [29] N. Vazou, E. L. Seidel, R. Jhala, D. Vytiniotis, and S. L. Peyton Jones.
straction from scratch. Consequently, second, we automate infer-             Refinement types for Haskell. In ICFP, 2014.
ence of pre- and post-conditions and loop invariants as refinement      [30] H. Xi and F. Pfenning. Eliminating array bound checking through
instantiation via Liquid Typing.                                             dependent types. In PLDI, 1998.
