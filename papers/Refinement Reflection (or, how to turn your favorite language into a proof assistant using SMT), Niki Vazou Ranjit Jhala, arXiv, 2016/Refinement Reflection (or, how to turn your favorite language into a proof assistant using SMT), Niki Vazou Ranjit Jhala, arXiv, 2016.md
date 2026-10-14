                                                                                         Refinement Reflection
                                                      (or, how to turn your favorite language into a proof assistant using SMT)

                                                                                                Niki Vazou           Ranjit Jhala
                                                                                              University of California, San Diego
arXiv:1610.04641v1 [cs.PL] 14 Oct 2016




                                         Abstract                                                                    ing with decidable and predictable verification, and enables users
                                         Refinement Reflection turns your favorite programming language              to reify pencil-and-paper proofs simply as programs in the source
                                         into a proof assistant by reflecting the code implementing a user-          language. Our key insight is dead simple: the code implementing
                                         defined function into the function’s (output) refinement type. As           a user-defined function can be reflected into the function’s (output)
                                         a consequence, at uses of the function, the function definition is          refinement type, thus converting the function’s (refinement) type
                                         unfolded into the refinement logic in a precise, predictable and            signature into a deep specification of the functions behavior. This
                                         most importantly, programmer controllable way. In the logic, we             simple idea has a profound consequence: at uses of the function, the
                                         encode functions and lambdas using uninterpreted symbols pre-               standard rule for (dependent) function application yields a precise,
                                         serving SMT-based decidable verification. In the language, we pro-          predictable and most importantly, programmer controllable means
                                         vide a library of combinators that lets programmers compose proofs          of instantiating the deep specification that is not tethered to brittle
                                         from basic refinements and function definitions. We have imple-             SMT heuristics. Reflection captures deep specifications as refine-
                                         mented our approach in the Liquid Haskell system, thereby con-              ments, but poses challenges for the logic and language.
                                         verting Haskell into an interactive proof assistant, that we used to        Logic: Algorithmic Verification Our first challenge: how can we
                                         verify a variety of properties ranging from arithmetic properties of        encode terms from an expressive higher order language in a decid-
                                         higher order, recursive functions to the Monoid, Applicative, Func-         able refinement logic in order to retain decidable, and hence, pre-
                                         tor and Monad type class laws for a variety of instances.                   dictable, verification? We address this problem by using ideas for
                                                                                                                     defunctionalization from the theorem proving literature which en-
                                         1. Introduction                                                             code functions and lambdas using uninterpreted symbols. This en-
                                                                                                                     coding lets us use (SMT-based) congruence closure to reason about
                                         Wouldn’t it be great to write proofs of programs in your favorite           equality (§ 4). Of course, congruence is not enough; in general, e.g.
                                         language, by writing programs in your favorite language, allowing           to prove two functions extensionally equal, we require facilities for
                                         you to avail of verification, while reusing the libraries, compilers        manipulating function definitions.
                                         and run-times for your favorite language?
                                             Refinement types [9, 26] offer a form of programming with               Language: Proof Composition Thus, as we wish to retrofit proofs
                                         proofs that can be retrofitted into several languages like ML [5, 24,       into existing languages, our second challenge: how can we design a
                                         37], C [8, 25], Haskell [32], TypeScript [34] and Racket [13]. The          library of combinators that lets programmers compose proofs from
                                         retrofitting relies upon restricting refinements to so-called “shal-        basic refinements and function definitions? We develop such a li-
                                         low” specifications that correspond to abstract interpretations of          brary, wherein proofs are represented simply as unit-values refined
                                         the behavior of functions. For example, refinements make it easy            by the proposition that they are proofs of. Refinement reflection
                                         to specify that the list returned by the append function has size           lets us unfold definitions simply by applying the function to the
                                         equal to the sum of those of its inputs. These shallow specifications       relevant inputs, and finally, we show how to build up sophisticated
                                         fall within decidable logical fragments, and hence, can be automat-         proofs using a small library of combinators that permit reasoning
                                         ically verified using SMT based refinement typing.                          in an algebraic or equational style.
                                             Refinements are a pale shadow of what is possible with de-              Implementation & Evaluation We have implemented our approach
                                         pendently typed languages like Coq, Agda and Idris which per-               in the Liquid Haskell system, thereby retrofitting deep verification
                                         mit “deep” specification and verification. These languages come             into Haskell, converting it into an interactive proof assistant. Liquid
                                         equipped with mechanisms that represent and manipulate the exact            Haskell’s refinement types crucially allow us to soundly account
                                         descriptions of user-defined functions. For example, we can repre-          for the dreaded bottom by checking that (refined) functions pro-
                                         sent the specification that the append function is associative, and         duce (non-bottom) values [32]. We evaluate our approach by using
                                         we can manipulate (unfold) its definition to write a small program          Liquid Haskell to verify a variety of properties including arithmetic
                                         that constructs a proof of the specification. Dafny [15], F⋆ [30] and       properties of higher order, recursive functions, textbook theorems
                                         Halo [35] take a step towards SMT-based deep verification, by en-           about functions on inductively defined datatypes, and the Monoid,
                                         coding user-defined functions as universally quantified logical for-        Applicative, Functor and Monad type class laws for a variety of in-
                                         mulas or “axioms”. This axiomatic approach offers significant au-           stances. We demonstrate that our proofs look very much like tran-
                                         tomation but is a devil’s bargain as by relying heavily upon brittle        scriptions of their pencil-and-paper analogues. Yet, the proofs are
                                         heuristics for “triggering” axiom instantiation, it gives away decid-       plain Haskell functions, where case-splitting and induction are per-
                                         able, and hence, predictable verification [16].                             formed by plain pattern-matching and recursion.
                                         Refinement Reflection In this paper, we present a new approach                  To summarize, this paper describes a means of retrofitting deep
                                         to retrofitting deep verification into existing languages. Our ap-          specification and verification into your favorite language, by mak-
                                         proach reconciles the automation of SMT-based refinement typ-               ing the following contributions:


                                                                                                                 1                                                                2016/10/18
 • We start with an informal description of refinement reflection,         Here, the parameters x and y refer to input values; any inhabitant
   and how it can be used to prove theorems about functions, by            of the above type is a proof that Int addition is commutative.
   writing functions (§ 2).                                                Proofs We can now prove the above theorems simply by writing
 • We formalize refinement reflection using a core calculus, and           Haskell programs. To ease this task Liquid Haskell provides prim-
   prove it sound with respect to a denotational semantics (§ 3).          itives to construct proof terms by “casting” expressions to Prop.
 • We show how to keep type checking decidable (§ 4) while using              data QED = QED
   uninterpreted functions and defunctionalization to reason about
   extensional equality in higher-order specifications (§ 5).                 (**) :: a → QED → Prop
 • Finally, we have implemented refinement reflection in Liquid               _ ** _ = ()
   Haskell, a refinement type system for Haskell. We develop a li-         To resemble mathematical proofs, we make this casting post-fix.
   brary of (refined) proof combinators and evaluate our approach          Thus, we can write e ** QED to cast e to a value of Prop. For
   by proving various theorems about recursive, higher-order func-         example, we can prove the above propositions simply by writing
   tions operating over integers and algebraic data types (§ 6).
                                                                              pf_plus_2_2 :: Plus_2_2_eq_4
                                                                              pf_plus_2_2 = trivial ** QED
2. Overview
We begin with a fast overview of refinement reflection and how it             pf_plus_comm :: Plus_comm
allows us to write proofs of and by Haskell functions.                        pf_plus_comm = \x y → trivial ** QED
2.1 Refinement Types                                                          trivial = ()
First, we recall some preliminaries about refinement types and how
                                                                           Via standard refinement type checking, the above code yields the
they enable shallow specification and verification.
                                                                           respective verification conditions (VCs),
Refinement types are the source program’s (here Haskell’s) types
decorated with logical predicates drawn from a(n SMT decidable)                                      2+2=4
logic [9, 26]. For example, we can refine Haskell’s Int datatype                                 ∀xy.x+y =y+x
with a predicate 0 ≤ v, to get a Nat type:                                 which are easily proved valid by the SMT solver, allowing us to
   type Nat = {v:Int | 0 ≤ v}                                              prove the respective propositions.
                                                                           A Note on Bottom: Readers familiar with Haskell’s semantics
The variable v names the value described by the type, hence the            may be feeling a bit anxious about whether the dreaded “bottom”,
above can be read as the “set of Int values v that are greater than        which inhabits all types, makes our proofs suspect. Fortunately,
0”. The refinement is drawn from the logic of quantifier free linear       as described in [32], Liquid Haskell ensures that all terms with
arithmetic and uninterpreted functions (QF-UFLIA [4]).                     non-trivial refinements provably evaluate to (non-bottom) values,
Specification & Verification We can use refinements to define and          thereby making our proofs sound.
type the textbook Fibonacci function as:
                                                                           2.2 Refinement Reflection
   fib   :: Nat → Nat
   fib 0 = 0                                                               Suppose that we wish to prove properties about the fib function,
   fib 1 = 1                                                               e.g. that fib 2 equals 1.
   fib n = fib (n-1) + fib (n-2)                                              type fib2_eq_1 = { fib 2 = 1 }
Here, the input type’s refinement specifies a pre-condition that the       Standard refinement type checking runs into two problems. First,
parameters must be Nat, which is needed to ensure termination,             for decidability and soundness, arbitrary user-defined functions do
and the output types’s refinement specifies a post-condition that          not belong the refinement logic, i.e. we cannot even refer to fib in
the result is also a Nat. Thus refinement type checking, lets us           a refinement. Second, the only information that a refinement type
specify and (automatically) verify the shallow property that if fib        checker has about the behavior of fib is its shallow type specifi-
is invoked with non-negative Int values, then it (terminates) and          cation Nat → Nat which is far too weak to verify fib2_eq_1.
yields a non-negative value.                                               To address both problems, we use the following annotation, which
Propositions We can use refinements to define a data type repre-           sets in motion the three steps of refinement reflection:
senting propositions simply as an alias for unit, a data type that            reflect fib
carries no run-time information:
   type Prop = ()                                                          Step 1: Definition The annotation tells Liquid Haskell to declare
                                                                           an uninterpreted function fib :: Int → Int in the refine-
but which can be refined with desired propositions about the code.         ment logic. By uninterpreted, we mean that the logical fib is not
For example, the following states the proposition 2 + 2 equals 4.          connected to the program function fib; as far as the logic is con-
                                                                           cerned, fib only satisfies the congruence axiom
   type Plus_2_2_eq_4 = {v: Prop | 2 + 2 = 4}
                                                                                         ∀n, m. n = m ⇒ fib n = fib m
For clarity, we abbreviate the above type by omitting the irrelevant
basic type Prop and variable v:                                            On its own, the uninterpreted function is not terribly useful, as it
                                                                           does not let us prove fib2_eq_1 which requires reasoning about
   type Plus_2_2_eq_4 = {2 + 2 = 4}                                        the definition of fib.
We represent universally quantified propositions as function types:        Step 2: Reflection In the next key step, Liquid Haskell reflects
                                                                           the definition into the refinement type of fib by automatically
   type Plus_com = x:Int→y:Int→{x+y = y+x}                                 strengthening the user defined type for fib to:


                                                                       2                                                             2016/10/18
   fib :: n:Nat → {v:Nat | fibP v n}                                        which we have found, with careful design of proof combinators,
                                                                            to be quite a natural and pleasant experience. To this end, we have
where fibP is an alias for a refinement automatically derived from          developed a library of proof combinators that permits reasoning
the function’s definition:                                                  about equalities and linear arithmetic, inspired by Agda [18].
   predicate fibP v n =                                                     “Equation” Combinators We equip Liquid Haskell with a a fam-
     v = if n = 0 then 0 else                                               ily of equation combinators ⊙. for each logical operator ⊙ in
         if n = 1 then 1 else                                               {=, 6=, ≤, <, ≥, >}, the operators in the theory QF-UFLIA. The
         fib(n-1) + fib(n-2)                                                refinement type of ⊙. requires that x ⊙ y holds and then ensures
                                                                            that the returned value is equal to x. For example, we define =. as:
Step 3: Application With the reflected refinement type, each appli-
cation of fib in the code automatically unfolds the fib definition             (=.) :: x:a → y:{a| x=y} → {v:a| v=x}
once during refinement type checking. We prove fib2_eq_1 by:                   x =. _ = x
   pf_fib2 :: { fib 2 = 1 }                                                 and use it to write the following “equational” proof:
   pf_fib2 = fib 2 == fib 1 + fib 0 ** QED
                                                                               eqPf_fib2 :: { fib 2 = 1 }
We write f to denote places where the unfolding of f’s definition              eqPf_fib2 = fib 2
is important. The proof is verified as the above is A-normalized to                      =. fib 1 + fib 0
                                                                                         =. 1
   let { t0 = fib 0; t1 = fib 1; t2 = fib 2 }
                                                                                         ** QED
   in ( t2 == t1 + t0 ) ** QED
Which via standard refinement typing, yields the following verifi-          “Because” Combinators Often, we need to compose “lemmas”
cation condition that is easily discharged by the SMT solver, even          into larger theorems. For example, to prove fib 3 = 2 we may
though fib is uninterpreted:                                                wish to reuse eqPf_fib2 as a lemma. To this end, Liquid Haskell
                                                                            has a “because” combinator:
(fibP (fib 0) 0) ∧ (fibP (fib 1) 1) ∧ (fibP (fib 2) 2)
 ⇒ (fib 2 = 1)                                                                 (∵) :: (Prop → a) → Prop → a
                                                                               f ∵ y = f y
Note that the verification of pf_fib2 relies merely on the fact
that fib was applied to (i.e. unfolded at) 0, 1 and 2. The SMT              The operator is simply an alias for function application that lets us
solver can automatically combine the facts, once they are in the            write x ⊙. y ∵ p (instead of (⊙.) x y p) where (⊙.) is
antecedent. Hence, the following would also be verified:                    extended to accept an optional third proof argument via Haskell’s
                                                                            type class mechanisms. We can use the because combinator to
   pf_fib2’ :: { fib 2 = 1 }                                                prove that fib 3 = 2 just by writing plain Haskell code:
   pf_fib2’ = [fib 0, fib 1, fib 2] ** QED
                                                                               eqPf_fib3 :: {fib 3 = 2}
Thus, unlike classical dependent typing, refinement reflection does            eqPf_fib3 = fib 3
not perform any type-level computation.                                                  =. fib 2 + fib 1
Reflection vs. Axiomatization An alternative axiomatic approach,                         =. 2                             ∵ eqPf_fib2
used by Dafny, F⋆ and HALO, is to encode the definition of fib                           ** QED
as a universally quantified SMT formula (or axiom):
                                                                            Arithmetic and Ordering SMT based refinements let us go well
                      ∀n. fibP (fib n) n                                    beyond just equational reasoning. Next, lets see how we can use
Axiomatization offers greater automation than reflection. Unlike            arithmetic and ordering to prove that fib is (locally) increasing,
Liquid Haskell, Dafny will verify the equivalent of the following           i.e. for all n, fib n ≤ fib (n + 1)
by automatically instantiating the above axiom at 2, 1 and 0:                  fibUp :: n:Nat → {fib n ≤ fib (n+1)}
   axPf_fib2 :: { fib 2 = 1 }                                                  fibUp n
   axPf_fib2 = trivial ** QED                                                    | n == 0
                                                                                 = fib 0 <. fib 1
    However, the presence of such axioms renders checking the                    ** QED
VCs undecidable. In practice, automatic axiom instantation can
easily lead to infinite “matching loops”. For example, the existence              | n == 1
of a term fib n in a VC can trigger the above axiom, which may                    = fib 1 ≤. fib 1 + fib 0 ≤. fib 2
then produce the terms fib (n − 1) and fib (n − 2), which may                     ** QED
then recursively give rise to further instantiations ad infinitum. To
prevent matching loops an expert must carefully craft “triggers”                  | otherwise
and provide a “fuel” parameter [1] that can be used to restrict the               = fib n
numbers of the SMT unfoldings, which ensure termination, but can                  =. fib (n-1) + fib (n-2)
cause the axiom to not be instantiated at the right places. In short,             ≤. fib n     + fib (n-2) ∵ fibUp (n-1)
the undecidability of the VC checking and its attendant heuristics                ≤. fib n     + fib (n-1) ∵ fibUp (n-2)
makes verification unpredictable [16].                                            ≤. fib (n+1)
2.3 Structuring Proofs                                                            ** QED
In contrast to the axiomatic approach, with refinement reflec-              Case Splitting and Induction The proof fibUp works by induc-
tion, the VCs are deliberately designed to always fall in an SMT-           tion on n. In the base cases 0 and 1, we simply assert the rele-
decidable logic, as function symbols are uninterpreted. It is upto          vant inequalities. These are verified as the reflected refinement un-
the programmer to unfold the definitions at the appropriate places,         folds the definition of fib at those inputs. The derived VCs are


                                                                        3                                                              2016/10/18
(automatically) proved as the SMT solver concludes 0 < 1 and                                     =. Z
1 + 0 ≤ 1 respectively. In the inductive case, fib n is unfolded                                 ** QED
to fib (n-1) + fib (n-2), which, because of the induction
hypothesis (applied by invoking fibUp at n-1 and n-2), and the                zeroR (S n) = add (S n) Z
SMT solvers arithmetic reasoning, completes the proof.                                    =. S (add n Z)
Higher Order Theorems Refinements smoothly accomodate higher-                             =. S n         ∵                         zeroR n
order reasoning. For example, lets prove that every locally increas-                      ** QED
ing function is monotonic, i.e. if f z ≤ f (z+1) for all z, then           The proof goes by induction, splitting cases on whether the number
f x ≤ f y for all x < y.                                                   is zero or non-zero. Consequently, we pattern match on the parame-
   fMono :: f:(Nat → Int)                                                  ter n, and furnish separate proofs for each case. In the “zero” case,
         → fUp:(z:Nat → {f z ≤ f (z+1)})                                   we simply unfold the definition of add. In the “successor” case,
         → x:Nat                                                           after unfolding we (literally) apply the induction hypothesis by us-
         → y:{x < y}                                                       ing the because operator. Liquid Haskell’s termination and totality
         → {f x ≤ f y} / [y]                                               checker verifies that we are in fact doing induction properly, i.e. the
   fMono f inc x y                                                         recursion in zeroR is well-founded (§ 3).
     | x + 1 == y                                                          Commutativity Lets conclude by proving that add is commutative:
     = f x ≤. f (x+1) ∵ fUp x
                                                                           add_com :: a:_ → b:_ → {add a b = add b a}
            ≤. f y
            ** QED                                                         add_com          Z    b = add Z b
                                                                                                   =. b
      | x + 1 < y
                                                                                                   =. add b Z               ∵ zeroR b
      = f x ≤. f (y-1) ∵ fMono f fUp x (y-1)
             ≤. f y    ∵ fUp (y-1)                                                                 ** QED
             ** QED                                                        add_com (S a) b = add (S a) b
We prove the theorem by induction on y, which is specified by the                          =. S (add a b)
annotation / [y] which states that y is a well-founded termina-                            =. S (add b a) ∵ add_com a b
tion metric that decreases at each recursive call [32]. If x+1 == y,                       =. add b (S a) ∵ sucR b a
then we use fUp x. Otherwise, x+1 < y, and we use the induc-                               ** QED
tion hypothesis i.e. apply fMono at y-1, after which transitivity          using a lemma sucR
of the less-than ordering finishes the proof. We can use the general
fMono theorem to prove that fib increases monotonically:                      sucR :: n:Peano → m:Peano →
                                                                                            {add n (S m) = S (add n m)}
   fibMono :: n:Nat → m:{n<m} →                                               sucR = exercise_for_reader
              {fib n ≤ fib m}
   fibMono = fMono fib fibUp                                                   Thus, refinement reflection lets us prove properties of Haskell
                                                                           programs just by writing Haskell programs: lemmas are just func-
2.4 Case Study: Peano Numerals                                             tions, case-splitting is just branching and pattern matching, and in-
                                                                           duction is just recursion. Next, we formalize refinement reflection
Refinement reflection is not limited to programs operating on in-          and describe how to keep type checking decidable and predictable.
tegers. We conclude the overview with a small library for Peano
numerals, defined via the following algebraic data type:                   3. Refinement Reflection
   data Peano = Z | S Peano                                                Our first step towards formalizing refinement reflection is a core
We can add two Peano numbers via:                                          calculus λR with an undecidable type system based on denotational
                                                                           semantics. We show how the soundness of the type system allows
   reflect add :: Peano → Peano → Peano                                    us to prove theorems using λR .
   add Z     m = m
   add (S n) m = S (add n m)                                               3.1 Syntax
In § 3.5 we will describe exactly how the reflection mechanism (il-        Figure 1 summarizes the syntax of λR , which is essentially the
lustrated via fibP) is extended to account for ADTs like Peano.            calculus λU [32] with explicit recursion and a special reflect
Note that Liquid Haskell automatically checks that add is to-              binding form to denote terms that are reflected into the refinement
tal [32], which lets us safely reflect it into the refinement logic.       logic. In λR refinements r are arbitrary expressions e (hence r ::=
                                                                           e in Figure 1). This choice allows us to prove preservation and
Add Zero to Left As an easy warm up, lets show that adding zero
                                                                           progress, but renders typechecking undecidable. In § 4 we will see
to the left leaves the number unchanged:
                                                                           how to recover decidability by soundly approximating refinements.
   zeroL :: n:Peano → { add Z n == n }                                         The syntactic elements of λR are layered into primitive con-
   zeroL n = add Z n                                                       stants, values, expressions, binders and programs.
           =. n                                                            Constants The primitive constants of λR include all the primitive
           ** QED                                                          logical operators ⊙, here, the set {=, <}. Moreover, they include
                                                                           the primitive booleans True, False, integers −1, 0, 1, etc., and
Add Zero to Right It is slightly more work to prove that adding            logical operators ∧, ∨, ¬, etc..
zero to the right also leaves the number unchanged.
                                                                           Data Constructors We encode data constructors as special con-
   zeroR :: n:Peano → { add n Z == n }                                     stants. For example the data type [Int], which represents finite lists
   zeroR Z     = add Z Z                                                   of integers, has two data constructors: [] (“nil”) and : (“cons”).


                                                                       4                                                                2016/10/18
                                                                                 function types; the above only appears in refinements and allows us
       Operators          ⊙   ::=   =|<
                                                                                 to state and prove facts about extensional equality § 5.2.
       Constants          c   ::=   ∧ | ¬ | ⊙ | +, −, . . .
                                |   True | False | 0, 1, −1, . . .               3.3 Types
         Values           w   ::=   c | λx.e | D w                               λR types include basic types, which are refined with predicates,
    Expressions           e   ::=   w | x | ee                                   and dependent function types. Basic types B comprise integers,
                                |   case x = e of {D x → e}                      booleans, and a family of data-types T (representing lists, trees
        Binders           b   ::=   e | let rec x : τ = b in b                   etc..) For example the data type [Int ] represents lists of integers.
       Program            p   ::=   b | reflect x : τ = e in p                   We refine basic types with predicates (boolean valued expressions
                                                                                 e) to obtain basic refinement types {v : B | e}. Finally, we have
    Basic Types           B   ::=   Int | Bool | T                               dependent function types x : τx → τ where the input x has the type
  Refined Types           τ   ::=   {v : B | e} | x : τ → τ                      τx and the output τ may refer to the input binder x. We write B to
                                                                                 abbreviate {v : B | True}, and τx → τ to abbreviate x : τx → τ
                                                                                 if x does not appear in τ . We use r to refer to refinements.
                         Figure 1. Syntax of λR
                                                                                 Denotations Each type τ denotes a set of expressions [[τ ]], that are
                                                                                 defined via the dynamic semantics [14]. Let ⌊τ ⌋ be the type we
                                                                                 get if we erase all refinements from τ and e : ⌊τ ⌋ be the standard
Contexts                                                                 C       typing relation for the typed lambda calculus. Then, we define the
              C    ::=     •                                                     denotation of types as:
                                                                                                  .
                     |     C e | cC | DeC e                                      [[{x : B | r}]] = {e | e : B, if e ֒→⋆ w then r[x 7→ w] ֒→⋆ True}
                     |     case y = C of {Di x → ei }                                             .
                                                                                  [[x : τx → τ ]] = {e | e : ⌊τx → τ ⌋, ∀ex ∈ [[τx ]]. e ex ∈ [[τ [x 7→ ex ]]]}
Reductions                                                       p ֒→ p′         Constants For each constant c we define its type Ty(c) such that
                                                       ′             ′
                                                                                 c ∈ [[Ty(c)]]. For example,
                           C[p]           ֒→       C[p ], if p ֒→ p                            .
                             cv           ֒→       δ(c, v)                         Ty(3) = {v : Int | v = 3}
                                                                                               .
                       (λx.e) e′          ֒→       e[x 7→ e′ ]                     Ty(+) = x : Int → y : Int → {v : Int | v = x + y}
                                                                                               .
 case y = Dj e of {Di xi → ei }           ֒→       ej [y 7→ Dj e][xi 7→ e]         Ty(≤) = x : Int → y : Int → {v : Bool | v ⇔ x ≤ y}
         reflect x : τ = e in p           ֒→       p[x 7→ fix (λx.e)]            So, by definition we get the constant typing lemma
         let rec x : τ = bx in b          ֒→       b[x 7→ fix (λx.bx )]
                          fix p           ֒→       p (fix p)                     Lemma 1. [Constant Typing] Every constant c ∈ [[Ty(c)]].
                                                                                                    .
                                                                                    Thus, if Ty(c) = x : τx → τ , then for every value w ∈ [[τx ]],
             Figure 2. Operational Semantics of λR                               we require δ(c, w) ∈ [[τ [x 7→ w]]].
                                                                                 3.4 Refinement Reflection
                                               R
Values & Expressions The values of λ include constants, λ-                       The simple, but key idea in our work is to strengthen the out-
abstractions λx.e, and fully applied data constructors D that wrap               put type of functions with a refinement that reflects the defini-
values. The expressions of λR include values and variables x,                    tion of the function in the logic. We do this by treating each
applications e e, and case expressions.                                          reflect-binder: reflect f : τ = e in p as a let rec-binder:
                                                                                 let rec f : Reflect(τ, e) = e in p during type checking (rule
Binders & Programs A binder b is a series of possibly recursive                  T-R EFLECT in Figure 3).
let definitions, followed by an expression. A program p is a series
of reflect definitions, each of which names a function that can                  Reflection We write Reflect(τ, e) for the reflection of term e into
be reflected into the refinement logic, followed by a binder. The                the type τ , defined by strengthening τ as:
                                                                                                                  .
stratification of programs via binders is required so that arbitrary               Reflect({v : B | r}, e)        = {v : B | r ∧ v = e}
                                                                                                                  .
recursive definitions are allowed but cannot be inserted into the                  Reflect(x : τx → τ, λy.e) = x : τx → Reflect(τ, e[y 7→ x])
logic via refinements or reflection. (We can allow non-recursive
                                                                                 As an example, recall from § 2 that the reflect fib strength-
let binders in e, but omit them for simplicity.)
                                                                                 ens the type of fib with the reflected refinement fibP.
3.2 Operational Semantics                                                        Consequences for Verification Reflection has two consequences
                                                                                 for verification. First, the reflected refinement is not trusted; it is
Figure 1 summarizes the small step contextual β-reduction seman-                 itself verified (as a valid output type) during type checking. Second,
tics for λR . We write e ֒→j e′ if there exist e1 , . . . , ej such that e       instead of being tethered to quantifier instantiation heuristics or
is e1 , e′ is ej and ∀i, j, 1 ≤ i < j, we have ei ֒→ ei+1 . We write             having to program “triggers” as in Dafny [15] or F⋆ [30] the
e ֒→⋆ e′ if there exists some finite j such that e ֒→j e′ . We define            programmer can predictably “unfold” the definition of the function
 ≈β to be the reflexive, symmetric, transitive closure of ֒→ .                   during a proof simply by “calling” the function, which we have
Constants Application of a constant requires the argument be re-                 found to be a very natural way of structuring proofs § 6.
duced to a value; in a single step the expression is reduced to
the output of the primitive constant operation. For example, con-                3.5 Refining & Reflecting Data Constructors with Measures
sider =, the primitive equality operator on integers. We have δ(=                We assume that each data type is equipped with a set of measures
       .
, n) = =n where δ(=n , m) equals True iff m is the same as n.                    which are unary functions whose (1) domain is the data type, and
We assume that the equality operator is defined for all values, and,             (2) body is a single case-expression over the datatype [32]:
for functions, is defined as extensional equality. That is, for all f
                                                                                         measure f : τ = λx.case y = x of {Di z → ei }
and f ′ we have (f = f ′ ) ֒→ True iff ∀v. f v ≈β f ′ v. We as-
sume source terms only contain implementable equalities over non-                For example, len measures the size of an [Int ]:


                                                                             5                                                                  2016/10/18
   measure len :: [Int] → Nat
   len = \x → case x of
                 []     → 0
                 (x:xs) → 1 + len xs

Checking and Projection We assume the existence of measures
that check the top-level constructor, and project their individual
fields. In § 4.2 we show how to use these measures to reflect
functions over datatypes. For example, for lists, we assume the              Well Formedness                                                        Γ⊢τ
existence of measures:
   isNil []              = True
   isNil (x:xs)          = False                                              Γ, v : B ⊢ e : Bool                    Γ ⊢ τx   Γ, x : τx ⊢ τ
                                                                                                        WF-BASE                                         WF-F UN
                                                                               Γ ⊢ {v : B | e}                          Γ ⊢ x : τx → τ
   isCons (x:xs) = True
   isCons []     = False                                                     Subtyping                                                     Γ ⊢ τ1  τ2

   sel1 (x:xs)           = x
   sel2 (x:xs)           = xs                                                   ∀θ ∈ [[Γ]].[[θ · {v : B | e1 }]] ⊆ [[θ · {v : B | e2 }]]
                                                                                                                                              -BASE
Refining Data Constructors with Measures We use measures to                             Γ ⊢ {v : B | e1 }  {v : B | e2 }
strengthen the types of data constructors, and we use these strength-
ened types during construction and destruction (pattern-matching).                       Γ ⊢ τx′  τx   Γ, x : τx′ ⊢ τ  τ ′
                                                                                                                                    -F UN
Let: (1) D be a data constructor, with unrefined type x : τ → T                            Γ ⊢ x : τx → τ  x : τx′ → τ ′
(2) the i-th measure definition with domain T is:
                                                                             Typing                                                          Γ⊢p:τ
       measure fi : τ = λx.case y = x of {D z → ei }
Then, the refined type of D is defined:                                               x:τ ∈Γ
                                                                                                    T-VAR                                  T-C ON
                 .                                                                    Γ⊢x:τ                         Γ ⊢ c : Ty(c)
        Ty(D) = x : τ → {v : T | ∧i fi v = ei [z 7→ x]}
                                                                                              Γ ⊢ p : τ′ Γ ⊢ τ′  τ
   Thus, each data constructor’s output type is refined to reflect                                                             T-S UB
the definition of each of its measures. For example, we use the                                       Γ⊢p:τ
measures len, isNil, isCons, sel1, and sel2 to strengthen                                      Γ ⊢ e : {v : B | er }
the types of [] and : to:                                                                                                       T-E XACT
              .                                                                            Γ ⊢ e : {v : B | er ∧ v = e}
     Ty([]) = {v : [Int] | r[] }
              .                                                                                   Γ, x : τx ⊢ e : τ
      Ty(:) = x : Int → xs : [Int ] → {v : [Int] | r: }                                                                       T-F UN
                                                                                               Γ ⊢ λx.e : x : τx → τ
where the output refinements are
                                                                                         Γ ⊢ e1 : (x : τx → τ ) Γ ⊢ e2 : τx
            .                                                                                                                          T-A PP
        r[] = len v = 0 ∧ isNil v ∧ ¬isCons v                                                        Γ ⊢ e1 e2 : τ
            .
        r: = len v = 1 + len xs ∧ ¬isNil v ∧ isCons v                                    Γ, x : τx ⊢ bx : τx  Γ, x : τx ⊢ τx
            ∧ sel1 v = x ∧ sel2 v = xs                                                      Γ, x : τx ⊢ b : τ       Γ⊢τ
                                                                                                                                       T-L ET
It is easy to prove that Lemma 1 holds for data constructors, by                          Γ ⊢ let rec x : τx = bx in b : τ
construction. For example, len [] = 0 evaluates to true.
                                                                                 Γ ⊢ let rec f : Reflect(τf , e) = e in p : τ
3.6 Typing Rules                                                                                                                           T-R EFLECT
                                                                                      Γ ⊢ reflect f : τf = e in p : τ
Next, we present the type-checking judgments and rules of λR .
Environments and Closing Substitutions A type environment Γ is                        Γ ⊢ e : {v : T | er }              Γ⊢τ
a sequence of type bindings x1 : τ1 , . . . , xn : τn . An environment                  ∀i.Ty(Di ) = yj : τj → {v : T | eri }
denotes a set of closing substitutions θ which are sequences of                       Γ, yj : τj , x : {v : T | er ∧ eri } ⊢ ei : τ
                                                                                                                                            T-C ASE
expression bindings: x1 7→ e1 , . . . , xn 7→ en such that:                           Γ ⊢ case x = e of {Di yi → ei } : τ
                   .
             [[Γ]] = {θ | ∀x : τ ∈ Γ.θ(x) ∈ [[θ · τ ]]}                                                Γ⊢τ                        T-F IX
Judgments We use environments to define three kinds of rules:                               Γ ⊢ fix : x : τ → y : τ → τ
Well-formedness, Subtyping, and Typing [14, 32]. A judgment
Γ ⊢ τ states that the refinement type τ is well-formed in the                                      Figure 3. Typing of λR
environment Γ. Intuitively, the type τ is well-formed if all the
refinements in τ are Bool-typed in Γ. A judgment Γ ⊢ τ1  τ2
states that the type τ1 is a subtype of τ2 in the environment Γ.
Informally, τ1 is a subtype of τ2 if, when the free variables of τ1
and τ2 are bound to expressions described by Γ, the denotation of
τ1 is contained in the denotation of τ2 . Subtyping of basic types
reduces to denotational containment checking. That is, for any
closing substitution θ in the denotation of Γ, for every expression


                                                                         6                                                                      2016/10/18
e, if e ∈ [[θ · τ1 ]] then e ∈ [[θ · τ2 ]]. A judgment Γ ⊢ p : τ states that
                                                                                          Predicates         r     ::=    r ⊕2 r | ⊕1 r
the program p has the type τ in the environment Γ. That is, when
                                                                                                                     |    n | b | x | D | xr
the free variables in p are bound to expressions described by Γ, the
                                                                                                                     |    if r then r else r
program p will evaluate to a value described by τ .
                                                                                           Integers        n       ::=    0, −1, 1, . . .
Rules All but three of the rules are standard [14, 32]. First, rule
T-R EFLECT is used to strengthen the type of each reflected binder                        Booleans         b       ::=    True | False
with its definition, as described previously in § 3.4. Second, rule                  Bin Operators        ⊕2       ::=    = | < | ∧ | + | − | ...
T-E XACT strengthens the expression with a singleton type equat-                      Un Operators        ⊕1       ::=    ¬ | ...
ing the value and the expression (i.e. reflecting the expression                             Model         σ       ::=    σ, (x : r) | ∅
in the type). This is a generalization of the “selfification” rules
                                                                                    Sort Arguments        sa       ::=    Int | Bool | U | Fun sa sa
from [14, 21], and is required to equate the reflected functions
with their definitions. For example, the application (fib 1) is                               Sorts        s       ::=    sa → s
typed as {v : Int | fibP v 1 ∧ v = fib 1} where the first con-
junct comes from the (reflection-strengthened) output refinement                                        Figure 4. Syntax of λS
of fib § 2, and the second conjunct comes from rule T-E XACT .
Finally, rule T-F IX is used to type the intermediate fix expres-
sions that appear, not in the surface language but as intermediate                 By Theorem 1 on 1 we get
terms in the operational semantics.
                                                                                                                                θ(d) ∈ [[Γ(d)]]            (2)
Soundness Following λU [32], we can show that evaluation pre-
serves typing and that typing implies denotational inclusion.                      Furthermore, by the typing rules 1 implies Γ(d) ⊢ b : τ and hence,
Theorem 1. [Soundness of λR ]                                                      via Theorem 1
 • Denotations If Γ ⊢ p : τ then ∀θ ∈ [[Γ]].θ · p ∈ [[θ · τ ]].                                                  ∀θ ∈ [[Γ(d)]]. θ · b ∈ [[θ · τ ]]         (3)
 • Preservation If ∅ ⊢ p : τ and p ֒→⋆ w then ∅ ⊢ w : τ .
                                                                                   Together, 2 and 3 imply
3.7 From Programs & Types to Propositions & Proofs
The denotational soundness Theorem 1 lets us interpret well typed                                                        θ(d) · b ∈ [[θ(d) · τ ]]          (4)
programs as proofs of propositions.                                                By the definition of type denotations, we have
“Definitions” A definition d is a sequence of reflected binders:                                                  .
                                                                                                    [[θ(d) · τ ]] = {f | τ is valid under d}               (5)
                 d ::= • | reflect x : τ = e in d
                                                                                   By 4, the above set is not empty, and hence τ is valid under d.
A definition’s environment Γ(d) comprises its binders and their
reflected types:
                                 .                                                 Example: Fibonacci is increasing In § 2 we verified that under a
                           Γ(•) = ∅                                                definition d that includes fib, the term fibUp proves
                                 .
      Γ(reflect f : τ = e in d) = (f, Reflect(τ, e)), Γ(d)                                        n : Nat → {fib n ≤ fib (n + 1)}
                                                                                   Thus, by Theorem 2 we get
A definition’s substitution θ(d) maps each binder to its definition:
                                    .                                                  ∀n.0 ≤ n ֒→⋆ True ⇒ fib n ≤ fib (n + 1) ֒→⋆ True
                              θ(•) = []
                                    .
      θ(reflect f : τ = e in d) = [[f 7→ fix f e], θ(d)]
“Propositions” A proposition is a type                                             4. Algorithmic Verification
          x1 : τ1 → . . . → xn : τn → {v : Unit | prop}                            Next, we describe λS , a conservative approximation of λR where
                                                                                   the undecidable type subsumption rule is replaced with a decidable
For brevity, we abbreviate propositions like the above to x : τ →                  one, yielding an SMT-based algorithmic type system that enjoys
{prop} and we call prop the proposition’s refinement. For simplic-                 the same soundness guarantees.
ity we assume that fv(τi ) = ∅.
“Validity”                                                                         4.1 The SMT logic λS
    A proposition x : τ → {prop} is valid under d if
                                                                                   Syntax: Terms & Sorts Figure 4 summarizes the syntax of λS , the
             ∀w ∈ [[τ ]]. θ(d) · prop[x 7→ w] ֒→⋆ True                             sorted (SMT-) decidable logic of quantifier-free equality, uninter-
That is, the proposition is valid if its refinement evaluates to True              preted functions and linear arithmetic (QF-EUFLIA) [4, 19]. The
for every (well typed) interpretation for its parameters x under d.                terms of λS include integers n, booleans b, variables x, data con-
                                                                                   structors D (encoded as constants), fully applied unary ⊕1 and bi-
“Proofs” A binder b proves a proposition τ under d if
                                                                                   nary ⊕2 operators, and application x r of an uninterpreted function
             ∅ ⊢ d[let rec x : τ = b in unit] : Unit                               x. The sorts of λS include built-in integer Int and Bool for rep-
That is, if the binder b has the proposition’s type τ under the                    resenting integers and booleans. The interpreted functions of λS ,
definition d’s environment.                                                        e.g. the logical constants = and <, have the function sort s → s.
                                                                                   Other functional values in λR , e.g. reflected λR functions and λ-
Theorem 2. [Proofs] If b proves τ under d then τ is valid under d.                 expressions, are represented as first-order values with uninterpreted
                                                                                   sort Fun s s. The universal sort U represents all other values.
Proof. As b proves τ under d, we have
                                                                                   Semantics: Satisfaction & Validity An assignment σ is a mapping
             ∅ ⊢ d[let rec x : τ = b in unit] : Unit                    (1)                                    .
                                                                                   from variables to terms σ = {x1 7→ r1 , . . . , xn 7→ rn }. We write


                                                                               7                                                                     2016/10/18
Transformation                                                           Γ⊢e         r        Embedding Applications Dually, we embed applications via de-
                                                                                              functionalization [23] using an uninterpreted apply function app
                                  T-B OOL                               T-I NT                as shown in rule T-A PP. The term e e′ , where e and e′ have types
           Γ⊢b           b                               Γ⊢n    n
                                                                                              τx → τ and τx , is transformed to appssx r r ′ : s where s and sx
                  Γ ⊢ e1   r1   Γ ⊢ e2      r2                                                are respectively (|τ |) and (|τx |), the appssx is a special uninterpreted
                   Γ ⊢ e1 ⊕2 e2   r 1 ⊕2 r 2
                                                               T-B IN                         function of sort Fun sx s → sx → s, and r and r ′ are the respec-
                                                                                              tive translations of e and e′ .
            Γ⊢e           r          T-U N                               T-VAR                Embedding Data Types Rule T-DC translates each data construc-
         Γ ⊢ ⊕1 e         ⊕1 r                           Γ⊢x        x                         tor to a predefined λS constant sD of sort (|Ty(D)|). Let Di be a
                                                                                              non-boolean data constructor such that
                                  T-O P                                 T-DC                                              .
          Γ⊢c            sc                         Γ⊢D        sD                                             Ty(Di ) = τi,1 → · · · → τi,n → τ

       Γ, x : τx ⊢ e          r     Γ ⊢ (λx.e) : (x : τx → τ )                                Then the check function isDi has the sort Fun (|τ |) Bool, and the
                                                                           T-F UN             select function selDi,j has the sort Fun (|τ |) (|τi,j |). Rule T-C ASE
                                                (|τ |)
                    Γ ⊢ λx.e              lam(|τx|) x r                                       translates case-expressions of λR into nested if terms in λS , by
                                                                                              using the check functions in the guards, and the select functions
        Γ ⊢ e′      r′        Γ⊢e           r        Γ ⊢ e : τx → τ                           for the binders of each case. For example, following the above, the
                                                                           T-A PP             body of the list append function
                                                (|τ |)
                    Γ ⊢ e e′          app(|τx|) r r ′
                                                                                                 []     ++ ys = ys
                 Γ⊢e     r    Γ ⊢ ei [x 7→ e] ri                                                 (x:xs) ++ ys = x : (xs ++ ys)
                                                                                 T-I F
    Γ     ⊢      case x = e of {True → e1 ; False → e2 }                                      is reflected into the λS refinement:
                 if r then r1 else r2
                                                                                                 if isNil xs then ys else sel1 xs : (sel2 xs ++ ys)
                            Γ⊢e    r                                                          We favor selectors to the axiomatic translation of HALO [35] and
              Γ ⊢ ei [yi 7→ selDi x][x 7→ e]                   ri                             F⋆ [30] to avoid universally quantified formulas and the resulting
                                                                                    T-C ASE   instantiation unpredictability.
   Γ      ⊢      case x = e of {Di yi → ei }
                 if app isD1 r then r1 else . . . else rn                                     4.3 Correctness of Translation
                                                                                              Informally, the translation relation Γ ⊢ e    r is correct in the sense
              Figure 5. Transforming λR terms into λS .                                       that if e is a terminating boolean expression then e reduces to True
                                                                                              iff r is SMT-satisfiable by a model that respects β-equivalence.

σ |= r if the assignment σ is a model of r, intuitively if σ r “is                            Definition 1 (β-Model). A β−model σ β is an extension of a model
true” [19]. A predicate r is satisfiable if there exists σ |= r. A                            σ where lam and app satisfy the axioms of β-equivalence:
predicate r is valid if for all assignments σ |= r.                                                            ∀x y e.lam x e          =    lam y (e[x 7→ y])
                                                                                                    ∀x ex e.(app (lam x e) ex          =    e[x 7→ ex ]
4.2 Transforming λR into λS
                                                                                              Semantics Preservation We define the translation of a λR term
The judgment Γ ⊢ e       r states that a λR term e is transformed,                                                                             .
                                                                                              into λS under the empty environment as (|e|) = r if ∅ ⊢ e         r.
under an environment Γ, into a λS term r. The transformation rules                                                   ⊥
                                                                                              A lifted substitution θ is a set of models σ where each “bottom”
are summarized in Figure 5.
                                                                                              in the substitution θ is mapped to an arbitrary logical value of the
Embedding Types We embed λR types into λS sorts as:                                           respective sort [32]. We connect the semantics of λR and translated
           .
   (|Int|) = Int
                                         .
                                 (|T |) = U                                                   λS via the following theorems:
           .                             .
 (|Bool|) = Bool       (|x : τx → τ |) = Fun (|τx |) (|τ |)                                   Theorem 3. If Γ ⊢ e         r, then for every θ ∈ [[Γ]] and every
                                                                                              σ ∈ θ⊥ , if θ⊥ · e ֒→⋆ v then σ β |= r = (|v|).
Embedding Constants Elements shared on both λR and λS trans-
late to themselves. These elements include booleans (T-B OOL ), in-                           Corollary 1. If Γ ⊢ e : Bool, e reduces to a value and Γ ⊢ e r,
tegers (T-I NT ), variables (T-VAR), binary (T-B IN) and unary (T-                            then for every θ ∈ [[Γ]] and every σ ∈ θ⊥ , θ⊥ · e ֒→⋆ True iff
U N) operators. SMT solvers do not support currying, and so in λS ,                           σ β |= r.
all function symbols must be fully applied. Thus, we assume that                              4.4 Decidable Type Checking
all applications to primitive constants and data constructors are sat-
urated, i.e. fully applied, e.g. by converting source level terms like                        Figure 6 summarizes the modifications required to obtain decidable
(+ 1) to (\z → z + 1).                                                                        type checking. Namely, basic types are extended with labels that
                                                                                              track termination and subtyping is checked via an SMT solver.
Embedding Functions As λS is a first-order logic, we embed
λ-abstraction and application using the uninterpreted functions                               Termination Under arbitrary beta-reduction semantics (which in-
lam and app. We embed λ-abstractions using lam as shown                                       cludes lazy evaluation), soundness of refinement type checking re-
in rule T-F UN. The term λx.e of type τx → τ is transformed                                   quires checking termination, for two reasons: (1) to ensure that re-
to lamssx x r of sort Fun sx s, where sx and s are respectively                               finements cannot diverge, and (2) to account for the environment
(|τx |) and (|τ |), lamssx is a special uninterpreted function of sort                        during subtyping [32]. We use ⇓ to mark provably terminating com-
sx → s → Fun sx s, and x of sort sx and r of sort s are the em-                               putations, and extend the rules to use refinements to ensure that if
bedding of the binder and body, respectively. As lam is just an                               Γ ⊢S e : {v : B ⇓ | r}, then e terminates [32].
SMT-function, it does not create a binding for x. Instead, the binder                         Verification Conditions The verification condition (VC) (|Γ|) ⇒ r
x is renamed to a fresh name pre-declared in the SMT environment.                             is valid only if the set of values described by Γ, is subsumed


                                                                                          8                                                                   2016/10/18
                                                                             α-instances For each syntactic term lam xi e, and λ-binder xj
        Refined Types      τ   ::=   {v : B [⇓] | e} | x : τ → τ             such that i < j appearing in the VC, we generate an α-equivalence
                                                                             instance predicate (or α-instance):
Well Formedness                                              Γ ⊢S τ                           lam xi e = lam xj e[xi 7→ xj ]
                                                                                 The conjunction of α-instances can be more precise than De
                    Γ, v : B ⊢S e : Bool⇓                                    Bruijn representation, as they let the SMT solver deduce more
                                             WF-BASE
                       Γ ⊢S {v : B | e}                                      equalities via congruence. For example, consider the VC needed
                                                                             to prove the applicative laws for Reader:
Subtyping                                              Γ ⊢S τ  τ ′
                                                                                    d = lam x1 (x x1 )
    .                                                                                 ⇒ lam x2 ((lam x1 (x x1 )) x2 ) = lam x1 (d x1 )
    ′
  Γ = Γ, v : {B ⇓ |e}  Γ′ ⊢ e ′  r′    Valid((|Γ′ |) ⇒ r ′ )
                                                                       -BASE
             Γ ⊢S {v : B | e}  {v : B | e′ }                                The α instance lam x1 (d x1 ) = lam x2 (d x2 ) derived from the
                                                                             VC’s hypothesis, combined with congruence immediately yields
  Figure 6. Algorithmic Typing (other rules in Figs 1 and 3.)                the VC’s consequence.
                                                                             β-instances For each syntactic term app (lam x e) ex , with ex not
                                                                             containing any λ-abstractions, appearing in the VC, we generate an
by the set of values described by r. Γ is embedded into logic                β-equivalence instance predicate (or β-instance):
by conjoining (the embeddings of) the refinements of provably
terminating binders [32]:                                                            app (lam xi e) ex = e[xi 7→ ex ], s.t. ex is λ-free
         . ^                                                                 We require the λ-free restriction as a simple way to enforce that the
   (|Γ|) =     (|Γ, x|)
                                                                             reduced term e[xi 7→ e′ ] enjoys the representation invariant.
              x∈Γ
                                                                                For example, consider the following VC needed to prove that
where we embed each binder as                                                the bind operator for lists satisfies the monadic associativity law.
           (                                                                            (f x ≫= g) = app (lam y (f y ≫= g)) x
         .   r     if Γ(x) = {v : B ⇓ | e}, Γ ⊢ e[v 7→ x]          r
(|Γ, x|) =                                                                   The right-hand side of the above VC generates a β-instance that
             True otherwise.
                                                                             corresponds directly to the equality, allowing the SMT solver to
Subtyping via SMT Validity We make subtyping, and hence, typ-                prove the (strengthened) VC.
ing decidable, by replacing the denotational base subtyping rule             Normalization The combination of α- and β-instances is often
 -BASE with a conservative, algorithmic version that uses an                required to discharge proof obligations. For example, when proving
SMT solver to check the validity of the subtyping VC. We use                 that the bind operator for the Reader monad is associative, we
Corollary 1 to prove soundness of subtyping.                                 need to prove the VC:
Lemma 2. If Γ ⊢S {v : B | e1 }  {v : B | e2 } then                             lam x2 (lam x1 w) = lam x3 (app (lam x2 (lam x1 w)) w)
Γ ⊢ {v : B | e1 }  {v : B | e2 }.
                                                                             The SMT solver proves the VC via the equalities corresponding to
Soundness of λS Lemma 2 directly implies the soundness of λS .               an α and then β-instance:

Theorem 4 (Soundness of λS ). If Γ ⊢S e : τ then Γ ⊢ e : τ .                 lam x2 (lam x1 w) =α lam x3 (lam x1 w)
                                                                                               =β lam x3 (app (lam x2 (lam x1 w)) w)
5. Reasoning About Lambdas                                                   5.2 Extensionality
Though λS , as presented so far, is sound and decidable, it is im-           Often, we need to prove that two functions are equal, given the
precise: our encoding of λ-abstractions and applications via unin-           definitions of reflected binders. For example, consider
terpreted functions makes it impossible to prove theorems that re-
quire α- and β-equivalence, or extensional equality. Next, we show              reflect id
how to address the former by strengthening the VCs with equal-                  id x = x
ities § 5.1, and the latter by introducing a combinator for safely
asserting extensional equality § 5.2. In the rest of this section, for       Liquid Haskell accepts the proof that id x = x for all x:
clarity we omit app when it is clear from the context.                          id_x_eq_x :: x:a → {id x = x}
                                                                                id_x_eq_x = \x → id x =. x ** QED
5.1 Equivalence
As soundness relies on satisfiability under a σ β (see Definition 1),        as “calling” id unfolds its definition, completing the proof. How-
we can safely instantiate the axioms of α- and β-equivalence on              ever, consider this η-expanded variant of the above proposition:
any set of terms of our choosing and still preserve soundness                   type Id_eq_id = {(\x → id x) = (\y → y)}
(Theorem 4). That is, instead of checking the validity of a VC
p ⇒ q, we check the validity of a strengthened VC, a ⇒ p ⇒ q,                Liquid Haskell rejects the proof:
where a is a (finite) conjunction of equivalence instances derived
from p and q, as discussed below.                                               fails :: Id_eq_id
                                                                                fails = (\x → id x) =. (\y → y) ** QED
Representation Invariant The lambda binders, for each SMT sort,
are drawn from a pool of names xi where the index i = 1, 2, . . ..           The invocation of id unfolds the definition, but the resulting equal-
When representing λ terms we enforce a normalization invariant               ity refinement {id x = x} is trapped under the λ-abstraction.
that for each lambda term lam xi e, the index i is greater than any          That is, the equality is absent from the typing environment at the
lambda argument appearing in e.                                              top level, where the left-hand side term is compared to \y → y.


                                                                         9                                                              2016/10/18
    CATEGORY                                              LOC                Ackermann’s Function
                                                                                       
    I.     Arithmetic                                                                   x + 2 , if n = 0                          
                                                                                     .                                         .       x , if h = 0
                                                                              An (x) =    2       , if x = 0           Ahn (x) =            h−1
           Fibonacci          §2                             48                         A     (A (x − 1))                             An (An   (x))
                                                                                                n−1    n
           Ackermann          [31] , Fig. 8                 280
                                                                             Properties
    II.    Algebraic Data Types
                                                                               1.                               An+1 (x)     =     Axn (2)
           Fold Universal     [18]                          105
                                                                               2.                                 x+1        <     An (x)
           Fold Fusion        [18]
                                                                               3.                                 An (x)     <     An (x + 1)
    III.   Typeclasses        Fig 9                                            4.                 x<y      ⇒      An (x)     <     An (y)
           Monoid             Peano, Maybe, List            189                5.                 0<x      ⇒      An (x)     <     An+1 (x)
           Functor            Maybe, List, Id, Reader       296                6.         0 < x, n < m     ⇒     An (x)      <     Am (x)
           Applicative        Maybe, List, Id, Reader       578                7.                                 Ahn (x)    <     Ah+1
                                                                                                                                     n   (x)
           Monad              Maybe, List, Id, Reader       435                8.                                 Ahn (x)    <     Ahn (x + 1)
                                                                               9.                x<y       ⇒      Ahn (x)    <     Ahn (y)
    IV.    Functional Correctness
                                                                               10.                         ⇒      Ahn (x)    <     Ahn+1 (x)
           SAT Solver         [7]                           133                11.   0 < n, l − 2 < x      ⇒       x+l       <     An (x)
           Unification        [27]                          200                12.   0 < n, l − 2 < x      ⇒     Aln (x)     <     An+1 (x)
    TOTAL                                                  2264                13.                                Axn (y)    <     An+1 (x + y)

                                                                               Figure 8. Ackermann Properties [31], ∀n, m, x, y, h, l ≥ 0
              Figure 7. Summary of Case Studies

                                                                              • Lemma Application which is carried out by using the “because”
Note that the above equality requires the definition of id and hence
                                                                                combinator (∵) to instantiate some fact at some inputs;
is outside the scope of purely the α- and β-instances.
                                                                              • SMT Reasoning in particular, arithmetic, ordering and congru-
An Exensionality Operator To allow function equality via exten-
sionality, we provide the user with a (family of) function compar-              ence closure which kicks in automatically (and predictably!),
ison operator(s) that transform an explanation p which is a proof               allowing us to simplify proofs by not having to specify, e.g.
that f x = g x for every argument x, into a proof that f = g.                   which subterms to rewrite.

   =∀ :: f:(a → b) → g:(a → b)                                               6.1 Arithmetic Properties
      → exp:(x:a → {f x = g x})                                              The first category of theorems pertains to the textbook Fibonacci
      → {f = g}                                                              and Ackermann functions. The former were shown in § 2. The
Of course, =∀ cannot be implemented; its type is assumed. We can             latter are summarized in Figure 8, which shows two alternative
use =∀ to prove Id_eq_id by providing a suitable explanation:                definitions for the Ackermann function. We proved equivalence
                                                                             of the definition (Prop 1) and various arithmetic relations between
pf_id_id :: Id_eq_id                                                         them (Prop 2 — 13), by mechanizing the proofs from [31].
pf_id_id = (\y → y) =∀ (\x → id x) ∵ expl
                                                                             Monotonicity Prop 3. shows that An (x) is increasing on x. We
    ** QED                                                                   derived Prop 4. by applying fMono theorem from § 2 with input
  where
                                                                             function the partially applied Ackermann Function An (⋆). Simi-
    expl = (\x → id x =. x ** QED)
                                                                             larly, we derived the monotonicity Prop 9. by applying fMono to
The explanation is the second argument to ∵ which has the follow-            the locally increasing Prop. 8 and Ahn (⋆). Prop 5. proves that An (x)
ing type that syntactically fires β-instances:                               is increasing on the first argument n. As fMono applies to the last
                                                                             argument of a function, we cannot directly use it to derive Prop 6.
   x:a → {(\x → id x) x = ((\x → x) x}                                       Instead, we define a variant fMono2 that works on the first argu-
                                                                             ment of a binary function, and use it to derive Prop 6.
6. Evaluation                                                                Constructive Proofs In [31] Prop 12. was proved by constructing an
                                                                             auxiliary ladder that counts the number of (recursive) invocations
We have implemented refinement reflection in Liquid Haskell. In
this section, we evaluate our approach by using Liquid Haskell to            of the Ackermann function, and uses this count to bound Ahn (x)
verify a variety of deep specifications of Haskell functions drawn           and An (x). It turned out to be straightforward and natural to for-
from the literature and categorized in Figure 7, totalling about 2500        malize the proof just by defining the ladder function in Haskell,
lines of specifications and proofs. Next, we detail each of the four         reflecting it, and using it to formalize the algebra from [31].
classes of specifications, illustrate how they were verified using           6.2 Algebraic Data Properties
refinement reflection, and discuss the strengths and weaknesses of
our approach. All of these proofs require refinement reflection, i.e.        The second category of properties pertain to algebraic data types.
are beyond the scope of shallow refinement typing.                           Fold Univerality Next, we proved properties of list folding, such as
Proof Strategies. Our proofs use three building blocks, that are             the following, describing the universal property of right-folds [18]:
seamlessly connected via refinement typing:
                                                                             foldr_univ
 • Un/folding definitions of a function f at arguments e1...en,                :: f:(a → b → b)
   which due to refinement reflection, happens whenever the term               → h:([a] → b)
   f e1 ... en appears in a proof. For exposition, we render                   → e:b
   the function whose un/folding is relevant as f;                             → ys:[a]


                                                                        10                                                               2016/10/18
                             Monoid                                        Haskell to prove that Peano (with add and Z), Maybe (with a
   Left Ident.    mempty x ♦ ≡ x                                           suitable mappend and Nothing), and List (with append ++
  Right Ident.    x ♦ mempty ≡ x                                           and []) satisfy the monoid laws. For example, we prove that ++
 Associativity    (x ♦ y) ♦ z ≡ x ♦ (y ♦ z)                                (§ 3.5) is associative by reifying the textbook proof [12] into a
                                                                           Haskell function, where the induction corresponds to case-splitting
                            Functor                                        and recurring on the first argument:
         Ident.   fmap id xs ≡ id xs
   Distribution   fmap (g ◦ h) xs ≡ (fmap g ◦ fmap h) xs                   assoc :: xs:[a] → ys:[a] → zs:[a] →
                                                                                  {(xs ++ ys) ++ zs = xs ++ (ys ++ zs)}
                          Applicative
        Ident.    pure id ⊛ v ≡ v                                          assoc [] ys zs     = ([] ++ ys) ++ zs
     Compos.      pure (◦) ⊛ u ⊛ v ⊛ w ≡ u ⊛ (v ⊛ w)                                          =. [] ++ (ys ++ zs)
 Homomorph.       pure f ⊛ pure x ≡ pure (f x)                                                ** QED
  Interchange     u ⊛ pure y ≡ pure ($ y) ⊛ u                              assoc (x:xs) ys zs = ((x: xs)++ ys) ++ zs
                            Monad                                                             =. (x: (xs ++ ys))++ zs
   Left Ident.    return a ≫= f ≡ f a                                                         =. x:((xs ++ ys) ++ zs)
  Right Ident.    m ≫= return ≡ m                                                             =. x: (xs ++ (ys ++ zs))
 Associativity    (m ≫= f ) ≫= g ≡ m ≫= (λx → f x ≫= g)                                           ∵ assoc xs ys zs
                                                                                              =. (x:xs) ++ (ys ++ zs)
                                                                                              ** QED
   Figure 9. Typeclass Laws verified using Liquid Haskell
                                                                           Functor Laws A type is a functor if it has a function fmap that sat-
                                                                           isfies the identity and distribution (or fusion) laws in Figure 9. For
   → base:{h [] = e }                                                      example, consider the proof of the fmap distribution law for the
   → stp:(x:a →l:[a]→{h(x:l) = f x (h l)})                                 lists, also known as “map-fusion”, which is the basis for important
   → {h ys = foldr f e ys}                                                 optimizations in GHC [36]. We reflect the definition of fmap:
Our proof foldr_univ differs from the one in Agda, in two                     reflect map :: (a → b) → [a] → [b]
ways. First, we encode Agda’s universal quantification over x and l           map f []     = []
in the assumption stp using a function type. Second, unlike Agda,             map f (x:xs) = f x : fmap f xs
Liquid Haskell does not support implicit arguments, so at uses of
foldr_univ the programmer must explicitly provide arguments                and then specify fusion and verify it by an inductive proof:
for base and stp, as illustrated below.
                                                                              map_fusion
Fold Fusion Let us define the usual composition operator:                       :: f:(b → c) → g:(a → b) → xs:[a]
                                                                                → {map (f . g) xs = (map f . map g) xs}
reflect . :: (b → c) → (a → b) → a → c
f . g     = \x → f (g x)
                                                                           Monad Laws The monad laws, which relate the properties of the
We can prove the following foldr_fusion theorem (that shows                two operators ≫= and return (Figure 9), refer to λ-functions,
operations can be pushed inside a foldr), by applying foldr_univ           thus their proof exercises our support for defunctionalization and
to explicit bas and stp proofs:                                            η- and β-equivalence. For example, consider the proof of the asso-
                                                                           ciativity law for the list monad. First, we reflect the bind operator:
   foldr_fusion
    :: h:(b → c)                                                              reflect (>>=) :: [a] → (a → [b]) → [b]
    → f:(a → b → b)                                                           (x:xs) >>= f = f x ++ (xs >>= f)
    → g:(a → c → c)                                                           []     >>= f = []
    → e:b → z:[a] → x:a → y:b
                                                                           Next, we define an abbreviation for the associativity property:
    → fuse: {h (f x y) = g x (h y)})
    → {(h . foldr f e) z = foldr g (h e) z}                                type AssocLaw m f g =
                                                                             {m >>= f >>= g = m >>= (\x → f x >>= g)}
   foldr_fusion h f g e ys fuse
     = foldr_univ g (h . foldr f e) (h e) ys                               Finally, we can prove that the list-bind is associative:
         (fuse_base h f e)                                                 assoc :: m:[a] → f:(a →[b]) → g:(b →[c])
         (fuse_step h f e g fuse)                                                → AssocLaw m f g
where fuse_base and fuse_step prove the base and inductive                 assoc [] f g
cases, and for example fuse_base is a function with type                     = [] >>= f >>= g
                                                                             =. [] >>= g
fuse_base :: h:(b→c) → f:(a→b→b) → e:b                                       =. []
          → {(h . foldr f e) [] = h e}                                       =. [] >>= (\x → f x >>= g) ** QED
                                                                           assoc (x:xs) f g
6.3 Typeclass Laws                                                           = (x:xs) >>= f >>= g
                                                                             =. (f x ++ xs >>= f) >>= g
We used Liquid Haskell to prove the Monoid, Functor, Applicative             =. (f x >>= g) ++ (xs >>= f >>= g)
and Monad Laws, summarized in Figure 9, for various user-defined                ∵ bind_append (f x) (xs >>= f) g
instances summarized in Figure 7.                                            =. (f x >>= g) ++ (xs >>= \y → f y >>= g)
Monoid Laws A Monoid is a datatype equipped with an associative                 ∵ assoc xs f g
binary operator ♦ and an identity element mempty. We use Liquid              =. (\y → f y >>= g) x ++


                                                                      11                                                               2016/10/18
      (xs >>= \y → f y >>= g)                                                7. Related Work
      ∵ βeq f g x
   =. (x:xs) >>= (\y → f y >>= g) ** QED                                     SMT-Based Verification SMT-solvers have been extensively used
Where the bind-append fusion lemma states that:                              to automate program verification via Floyd-Hoare logics [19]. Our
                                                                             work is inspired by Dafny’s Verified Calculations [17], a frame-
bind_append ::                                                               work for proving theorems in Dafny [15], but differs in (1) our use
  xs:[a] → ys:[a] → f:(a → [b]) →                                            of reflection instead of axiomatization, and (2) our use of refine-
  {(xs++ys) >>= f = (xs >>= f)++(ys >>= f)}                                  ments to compose proofs. Dafny, and the related F⋆ [30] which like
Notice that the last step requires β-equivalence on anonymous                Liquid Haskell, uses types to compose proofs, offer more automa-
functions, which we get by explicitly inserting the redex in the             tion by translating recursive functions to SMT axioms. However,
logic, via the following lemma with trivial proof                            unlike reflectionm this axiomatic approach renders typechecking
                                                                             / verification undecidable (in theory) and leads to unpredictability
   βeq :: f:_ → g:_ → x:_ →                                                  and divergence (in practice) [16].
      {bind (f x) g = (\y → bind (f y) g) x}
   βeq _ _ _ = trivial                                                       Dependent types Our work is inspired by dependent type systems
                                                                             like Coq [6] and Agda [20]. Reflection shows how deep specifica-
6.4 Functional Correctness                                                   tion and verification in the style of Coq and Agda can be retrofitted
                                                                             into existing languages via refinement typing. Furthermore, we can
Finally, we proved correctness of two programs from the literature:          use SMT to significantly automate reasoning over important theo-
a SAT solver and a Unification algorithm.                                    ries like arithmetic, equality and functions. It would be interesting
SAT Solver We implemented and verified the simple SAT solver                 to investigate how the tactics and sophisticated proof search of Coq
used to illustrate and evaluate the features of the dependently typed        etc. can be adapted to the refinement setting.
language Zombie [7]. The solver takes as input a formula f and
returns an assignment that satisfies f if one exists.                        Dependent Types for Non-Terminating Programs Zombie [7, 27]
                                                                             integrates dependent types in non terminating programs and sup-
solve :: f:Formula → Maybe {a:Asgn|sat a f}                                  ports automatic reasoning for equality. Vazou et al. have previ-
solve f = find ( 8 sat 8 f) (assignments f)                                  ously [32] shown how Liquid Types can be used to check non-
Function assignments f returns all possible assignments of                   terminating programs. Reflection makes Liquid Haskell at least as
the formula f and sat a f returns True iff the assignment a                  expressive as Zombie, without having to axiomatize the theory of
satisfies the formula f:                                                     equality within the type system. Consequently, in contrast to Zom-
                                                                             bie, SMT based reflection lets Liquid Haskell verify higher-order
   reflect sat :: Asgn → Formula → Bool                                      specifications like foldr_fusion.
   assignments :: Formula → [Asgn]
                                                                             Dependent Types in Haskell Integration of dependent types into
Verification of solve follows simply by reflecting sat into the re-          Haskell has been a long standing goal that dates back to Cayenne [3],
finement logic, and using (bounded) refinements to show that find            a Haskell-like, fully dependent type language with undecidable
only returns values on which its input predicate yields True [33].           type checking. In a recent line of work [10] Eisenberg et al. aim
   find :: p:(a → Bool) → [a]                                                to allow fully dependent programming within Haskell, by mak-
        → Maybe {v:a | p v}                                                  ing “type-level programming ... at least as expressive as term-level
                                                                             programming”. Our approach differs in two significant ways. First,
Unification As another example, we verified the unification of first         reflection allows SMT-aided verification which drastically simpli-
order terms, as presented in [27]. First, we define a predicate alias        fies proofs over key theories like linear arithmetic and equality.
for when two terms s and t are equal under a substitution su:                Second, refinements are completely erased at run-time. That is,
   eq_sub su s t = apply su s == apply su t                                  while both systems automatically lift Haskell code to either un-
                                                                             interpreted logical functions or type families, with refinements,
Now, we can define a Haskell function unify s t that can di-                 the logical functions are not accessible at run-time, and promo-
verge, or return Nothing, or return a substitution su that makes             tion cannot affect the semantics of the program. As an advantage
the terms equal:                                                             (resp. disadvantage) our proofs cannot degrade (resp. optimize) the
   unify :: s:Term → t:Term                                                  performance of programs.
         → Maybe {su| eq_sub su s t}
                                                                             Proving Equational Properties Several authors have proposed
For the specification and verification we only needed to reflect             tools for proving (equational) properties of (functional) programs.
apply and not unify; thus we only had to verify that the former              Systems [29] and [2] extend classical safety verification algo-
terminates, and not the latter.                                              rithms, respectively based on Floyd-Hoare logic and Refinement
   As before, we prove correctness by invoking separate helper               Types, to the setting of relational or k-safety properties that are
lemmas. For example to prove the post-condition when unifying                assertions over k-traces of a program. Thus, these methods can
a variable TVar i with a term t in which i does not appear, we               automatically prove that certain functions are associative, com-
apply a lemma not_in:                                                        mutative etc.. but are restricted to first-order properties and are
   unify (TVar i) t2                                                         not programmer-extensible. Zeno [28] generates proofs by term
     | not (i ∈ freeVars t2)                                                 rewriting and Halo [35] uses an axiomatic encoding to verify con-
     = Just (const [(i, t2)] ∵ not_in i t2)                                  tracts. Both the above are automatic, but unpredictable and not
                                                                             programmer-extensible, hence, have been limited to far simpler
i.e. if i is not free in t, the singleton substitution yields t:             properties than the ones checked here. Hermit [11] proves equal-
   not_in :: i:Int                                                           ities by rewriting GHC core guided by user specified scripts. In
          → t:{Term | not (i ∈ freeVars t)}                                  contrast, our proofs are simply Haskell programs, we can use SMT
          → {eq_sub [(i, t)] (TVar i) t}                                     solvers to automate reasoning, and, most importantly, we can con-
                                                                             nect the validity of proofs with the semantics of the programs.


                                                                        12                                                              2016/10/18
8. Conclusions & Future Directions                                                  [14] K.W. Knowles and C. Flanagan.        Hybrid type checking.     ACM
                                                                                         TOPLAS, 2010.
We have shown how refinement reflection – namely reflecting the
definitions of functions in their output refinements – can be used                  [15] K. Rustan M. Leino. Dafny: An automatic program verifier for func-
                                                                                         tional correctness. LPAR, 2010.
to convert a language into a proof assistant, while ensuring (re-
finement) type checking stays decidable and predictable via careful                 [16] K. Rustan M. Leino and Clément Pit-Claudel. Trigger selection
design of the logic and proof combinators.                                               strategies to stabilize program verifiers. In CAV, 2016.
    Our evaluation shows that refinement reflection lets us prove                   [17] K. Rustan M. Leino and Nadia Polikarpova. Verified calculations. In
deep specifications of a variety of implementations, and identifies                      VSTTE, 2016.
important avenues for research. First, while proofs are possible,                   [18] Shin-cheng Mu, Hsiang-shang Ko, and Patrik Jansson. Algebra of Pro-
they can sometimes be cumbersome. For example, in the proof of                           gramming in Agda: Dependent Types for Relational Program Deriva-
associativity of the monadic bind operator for the Reader monad                          tion. J. Funct. Program., 2009.
three of eight (extensional) equalities required explanations, some                 [19] G. Nelson. Techniques for program verification. Technical Report
nested under multiple λ-abstractions. Thus, it would be valuable                         CSL81-10, Xerox Palo Alto Research Center, 1981.
to use recent advances in refinement-based synthesis [22] to au-                    [20] U. Norell. Towards a practical programming language based on
tomate proof construction. Second, while our approach to α- and                          dependent type theory. PhD thesis, Chalmers, 2007.
β-equivalence is sound, we do not know if it is complete. We con-                   [21] X. Ou, G. Tan, Y. Mandelbaum, and D. Walker. Dynamic typing with
jecture it is, due to the fact that our refinement terms are from the                    dependent types. In IFIP TCS, 2004.
simply typed lambda calculus (STLC). Thus, it would be interest-                    [22] Nadia Polikarpova, Ivan Kuraj, and Armando Solar-Lezama. Program
ing to use the normalization of STLC to develop a sound and com-                         synthesis from polymorphic refinement types. In PLDI, 2016.
plete SMT axiomatization, thereby automating proofs predictably.                    [23] John C. Reynolds. Definitional interpreters for higher-order program-
                                                                                         ming languages. In 25th ACM National Conference, 1972.
References                                                                          [24] P. Rondon, M. Kawaguchi, and R. Jhala. Liquid types. In PLDI, 2008.
                                                                                    [25] P. Rondon, M. Kawaguchi, and R. Jhala. Low-level liquid types. In
 [1] Nada Amin, K. Rustan M. Leino, and Tiark Rompf. Computing with
                                                                                         POPL, 2010.
     an SMT Solver. In TAP, 2014.
                                                                                    [26] J. Rushby, S. Owre, and N. Shankar. Subtypes for specifications:
 [2] Kazuyuki Asada, Ryosuke Sato, and Naoki Kobayashi. Verifying                        Predicate subtyping in pvs. IEEE TSE, 1998.
     relational properties of functional programs by first-order refinement.
     In PEPM, 2015.                                                                 [27] Vilhelm Sjöberg and Stephanie Weirich. Programming up to congru-
                                                                                         ence. POPL, 2015.
 [3] L. Augustsson. Cayenne - a language with dependent types. In ICFP,
     1998.                                                                          [28] W. Sonnex, S. Drossopoulou, and S. Eisenbach. Zeno: An automated
                                                                                         prover for properties of recursive data structures. In TACAS, 2012.
 [4] C. Barrett, A. Stump, and C. Tinelli. The SMT-LIB Standard: Version
     2.0. 2010.                                                                     [29] Marcelo Sousa and Isil Dillig. Cartesian hoare logic for verifying k-
                                                                                         safety properties. In PLDI, 2016.
 [5] J. Bengtson, K. Bhargavan, C. Fournet, A.D. Gordon, and S. Maffeis.
     Refinement types for secure implementations. In CSF, 2008.                     [30] Nikhil Swamy, Cătălin Hriţcu, Chantal Keller, Aseem Rastogi, An-
                                                                                         toine Delignat-Lavaud, Simon Forest, Karthikeyan Bhargavan, Cédric
 [6] Y. Bertot and P. Castéran. Coq’Art: The Calculus of Inductive Con-                 Fournet, Pierre-Yves Strub, Markulf Kohlweiss, Jean-Karim Zinzin-
     structions. Springer Verlag, 2004.                                                  dohoue, and Santiago Zanella-Béguelin. Dependent types and multi-
 [7] C. Casinghino, V. Sjöberg, and S. Weirich. Combining proofs and                    monadic effects in F*. In POPL, 2016.
     programs in a dependently typed language. In POPL, 2014.                       [31] George   Tourlakis.         Ackermanns  Function.
 [8] Jeremy Condit, Matthew Harren, Zachary R. Anderson, David Gay,                      http://www.cs.yorku.ca/˜gt/papers/Ackermann-function.pdf,
     and George C. Necula. Dependent types for low-level programming.                    2008.
     In ESOP, 2007.                                                                 [32] N. Vazou, E. L. Seidel, R. Jhala, D. Vytiniotis, and S. Peyton-Jones.
 [9] R. L. Constable and S. F. Smith. Partial objects in constructive type               Refinement Types for Haskell. In ICFP, 2014.
     theory. In LICS, 1987.                                                         [33] Niki Vazou, Alexander Bakst, and Ranjit Jhala. Bounded refinement
[10] Richard A. Eisenberg and Jan Stolarek. Promoting functions to type                  types. In ICFP, 2015.
     families in Haskell. In Haskell, 2014.                                         [34] Panagiotis Vekris, Benjamin Cosman, and Ranjit Jhala. Refinement
[11] Andrew Farmer, Neil Sculthorpe, and Andy Gill. Reasoning with                       types for typescript. In PLDI, 2016.
     the HERMIT: Tool support for equational reasoning on GHC Core                  [35] D. Vytiniotis, S.L. Peyton-Jones, K. Claessen, and D. Rosén. Halo:
     programs. Haskell, 2015.                                                            haskell to logic through denotational semantics. In POPL, 2013.
[12] Graham Hutton. Programming in Haskell. Cambridge University                    [36] GHC           Wiki.                       GHC          optimisations.
     Press, 2007.                                                                        https://wiki.haskell.org/GHC_optimisations.
[13] Andrew M. Kent, David Kempe, and Sam Tobin-Hochstadt. Occur-                   [37] H. Xi and F. Pfenning. Eliminating array bound checking through
     rence typing modulo theories. In PLDI, 2016.                                        dependent types. In PLDI, 1998.




                                                                               13                                                                   2016/10/18
