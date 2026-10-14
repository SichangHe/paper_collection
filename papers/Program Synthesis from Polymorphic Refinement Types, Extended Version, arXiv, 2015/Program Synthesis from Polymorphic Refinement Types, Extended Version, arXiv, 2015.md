                                                   Program Synthesis from Polymorphic Refinement Types
                                                                                                Extended Version

                                                                      Nadia Polikarpova            Ivan Kuraj          Armando Solar-Lezama
                                                                                                   MIT CSAIL, USA
                                                                                        {polikarn,ivanko,asolar}@csail.mit.edu
arXiv:1510.08419v3 [cs.PL] 21 Apr 2016




                                         Abstract
                                                                                                                    replicate      :: n: Nat → x: α → {List α | len ν = n}
                                         We present a method for synthesizing recursive functions                   replicate =       λ n . λ x . if n ≤ 0
                                         that provably satisfy a given specification in the form of a                  then Nil
                                         polymorphic refinement type. We observe that such speci-                      else Cons x (replicate (dec n) x)
                                         fications are particularly suitable for program synthesis for
                                         two reasons. First, they offer a unique combination of ex-               Figure 1. Refinement type signature of replicate and the
                                         pressive power and decidability, which enables automatic                 code synthesized from this signature.
                                         verification—and hence synthesis—of nontrivial programs.
                                         Second, a type-based specification for a program can often               sponding verification procedures rarely enjoy the same level
                                         be effectively decomposed into independent specifications                of modularity as type checking, thus fundamentally limiting
                                         for its components, causing the synthesizer to consider fewer            the scalability of these techniques.
                                         component combinations and leading to a combinatorial re-                   In this work we present a novel system that pushes the
                                         duction in the size of the search space. At the core of our              idea of type-directed synthesis one step further by taking
                                         synthesis procedure is a new algorithm for refinement type               advantage of refinement types [13, 32]: types decorated with
                                         checking, which supports specification decomposition.                    predicates from a decidable logic. For example, imagine that
                                            We have evaluated our prototype implementation on a                   a user intends to synthesize the function replicate, which,
                                         large set of synthesis problems and found that it exceeds                given a natural number n and a value x, produces a list that
                                         the state of the art in terms of both scalability and usability.         contains n copies of x. In our system, the user can express
                                         The tool was able to synthesize more complex programs than               this intent by providing the following signature:
                                         those reported in prior work (several sorting algorithms and
                                         operations on balanced search trees), as well as most of the             replicate      :: n : Nat → x : α → {ν : List α | len ν = n}
                                         benchmarks tackled by existing synthesizers, often starting              Here, the return type is refined with the predicate len ν = n,
                                         from a more concise and intuitive user input.                            which restricts the length of the output list to be equal to the
                                         Keywords Program Synthesis, Functional Programming,                      argument n; Nat is a shortcut for {ν : Int | ν ≥ 0}, the
                                         Refinement Types, Predicate Abstraction                                  type of integers that are greater or equal to zero1 . Given this
                                                                                                                  signature, together with the definition of List and a standard
                                         1.   Introduction                                                        set of integer components (which include zero, decrement
                                         The key to scalable program synthesis is modular verifica-               function, and inequalities), our system produces a provably
                                         tion. Modularity enables the synthesizer to prune candidates             correct implementation of replicate, shown in Fig. 1, within
                                         for different subprograms independently, whereby combina-                fractions of a second.
                                         torially reducing the size of the search space it has to consider.           We argue that refinement types offer the user a conve-
                                         This explains the recent success of type-directed approaches             nient interface to a program synthesizer: the signature above
                                         to synthesis of functional programs [12, 14, 15, 27]: not only           is only marginally more complex than a conventional ML
                                         do ill-typed programs vastly outnumber well-typed ones, but              or Haskell type. Contrast that with example-based synthesis,
                                         more importantly, a type error can be detected long before the           which would require a conventional type together with mul-
                                         whole program is put together.                                           tiple input-output pairs, and in return provide much weaker
                                             Simple, coarse-grained types alone are, however, rarely              correctness guarantees.
                                         sufficient to precisely describe a synthesis goal. Therefore,                The replicate example is a perfect illustration of the
                                         existing approaches supplement type information with other               power of parametric polymorphism for specifying program
                                         kinds of specifications, such as input-output examples [1, 12,           1 Hereafter the bound variable of the refinement is always called ν and the

                                         27], or pre- and post-conditions [20, 21]. Alas, the corre-              binding is omitted.


                                                                                                              1                                                                     2016/4/22
behavior. Even though the signature in Fig. 1 never says ex-             case is to find an over-approximate decomposition: that is,
plicitly that each element of the output list must equal x, it           construct requirements on f and x that are necessary but gen-
nevertheless captures the semantics of replicate completely:             erally not sufficient for the correctness of f x, yet are strong
since the function knows nothing about the type parameter α,             enough to filter out many incorrect subterms.
it has no way of constructing any values of this type other                  To address this challenge, we propose a new type checking
than x. This surprising expressiveness of polymorphic types              mechanism for refinement types, which we dub local liquid
had been long known [39], but combined with refinements,                 type checking. At the heart of the new mechanism is a type
it enables full-fledged higher-order reasoning within the type           system inspired by bidirectional type checking [30]. Bidirec-
system: a caller of replicate can instantiate α with any re-             tional systems interleave top-down and bottom-up propaga-
finement type, obtaining the fact that whenever x has a cer-             tion of type information depending on the syntactic structure
tain property, every element of the output list shares that same         of the program; in this work we extend the bottom-up phase
property.                                                                of bidirectional checking with top-down propagation of over-
    Perhaps surprisingly, prior work on liquid types [19, 32,            approximate type information, resulting in a round-trip type
35, 36] has shown that this type of higher-order reasoning               checking mechanism, which promotes modular checking of
can be fully automated for a large class of programs and                 function applications. Additionally, we equip the type system
properties. The liquid type inference algorithm [32] uses a              with a novel liquid abduction rule, which enables modular
combination of Hindley-Milner unification and least-fixpoint             checking of branching terms.
Horn clause solver based on predicate abstraction to discover                Refinement type checking involves solving subtyping
refined instantiations for polymorphic types and ultimately              constraints over unknown refinement types. The modular-
reduce verification to proving quantifier-free formulas over             ity requirement precludes our system from using the two
simple refinement predicates, efficiently decidable by SMT               techniques employed to this end by liquid type inference—
solvers. The unique combination of expressive power and                  Hindley-Milner unification and the least-fixpoint Horn solver—
decidability offered by polymorphic refinement types makes               since both techniques are designed to work on complete pro-
them ideal for program synthesis.                                        grams and propagate type information bottom-up. Instead, lo-
    Technical Challenges. Unfortunately, liquid type infer-              cal liquid type checking incorporates an algorithm for solving
ence cannot be applied out of the box to the context of syn-             subtyping constraints incrementally, as it analyzes different
thesis. Designed for the setting where, given a program, the             parts of the program. Most notably, top-down propagation
goal is to construct its type, the inference algorithm starts            requires finding the greatest fixpoint solution to unknown
from the leaves of the program, whose types are known, and               refinements instead of the least, which is known to be funda-
propagates type information bottom-up, constructing types of             mentally more expensive; we propose a practical implemen-
terms from the types of their subterms. In program synthe-               tation for this fixpoint computation, which we call MUSF IX,
sis, however, the setting is different: here the top-level type is       inspired by an existing algorithm for enumerating minimal
given, and the goal is to construct the program. One way to do           unsatisfiable subsets (MUSes) [22].
so is to exhaustively explore program candidates, performing                 Results. We have combined local liquid type checking
liquid type inference on each one, and then checking if the              and exhaustive enumeration of program terms in a prototype
inferred type matches the given specification. While this ap-            program synthesizer called S YNQUID (for “S YNthesis with
proach does rule out many ill-typed partial programs, it fails           liQUID types”), which we evaluated on 64 synthesis problems
to take advantage of the specification for guiding the search. A         from a variety of sources. The implementation, the bench-
more promising approach would propagate type information                 marks, and a web interface for S YNQUID are available from
top-down from the specification, using it to filter out irrelevant       the tool repository [31].
partial solutions.                                                           Our evaluation indicates that the techniques described
    Some program terms naturally support decomposing a                   above work well for synthesizing programs that manipulate
specification into independent requirements for their sub-               lists and trees, as well as data structures with complex invari-
terms. For example, given a goal type T and assuming that                ants and custom user-defined data structures. S YNQUID was
the top-level construct of the program is a conditional with a           able to synthesize programs that are more complex than those
known guard, we can pass T on to the two branches of the                 previously reported in the literature, including five different
conditional, together with the appropriate path conditions de-           sorting algorithms, and manipulations of binary search trees,
rived from the guard, and proceed to check (or synthesize)               AVL trees, and Red-Black trees. The evaluation also shows
them completely independently. Unfortunately, for other pro-             that the modularity features of local liquid type checking and
gram terms there might be infinitely many ways to precisely              the MUSF IX solver are crucial for the performance of the
decompose a specification. Take a function application, f x:             system.
the specification f x :: Nat can be satisfied by requiring                   We compare our system with the existing synthesizers
that f subtract one and x be positive, or that f add one, and x          based on input-output examples [1, 12, 14, 27], and Hoare-
be greater than negative one, and so on. The challenge in this           style verification [20, 21], and demonstrate that S YNQUID


                                                                     2                                                         2016/4/22
can handle the majority of its competitors’ most challenging           section illustrates the details of this procedure and showcases
benchmarks, taking a similar or shorter amount of time. In ad-         various features of the specification language on a number of
dition, compared with the example-based tools, S YNQUID’s              examples.
specifications are usually more concise and the generated so-             Example 1: Recursive Programs and Condition Abduc-
lutions are provably correct; compared with the tools based on         tion. We first revisit the replicate example from the introduc-
Hoare-style reasoning, S YNQUID can verify (and thus synthe-           tion. We assume that the set of available components includes
size) more complex programs thanks to automatic refinement             functions 0, inc and dec on integers, as well as a list datatype
inference.                                                             whose constructors are refined with length information, ex-
                                                                       pressed by means of an uninterpreted function (or measure)
2.    Overview                                                         len.

S YNQUID operates within a core ML-like language featuring               0 :: {Int | ν = 0}
conditionals, algebraic datatypes, pattern matching, paramet-            inc :: x: Int → {Int | ν = x + 1}
ric polymorphism, and fixpoints. We equip the language with              dec :: x: Int → {Int | ν = x - 1}
general decidable refinement types, closely following the liq-
uid types framework [19, 32, 35]. The type system includes               termination measure len      :: List β → Nat
refined base types of the form {B | ψ}, where ψ is a refine-             data List β where
ment predicate over the program variables and a special value              Nil  :: {List β | len ν = 0}
variable ν, which does not appear in the program. Base types               Cons  :: β → xs: List β →
can be combined into dependent function types of the form                     {List β | len ν = len xs + 1}
x : Tx → T2 , where x may appear in the refinement pred-
icates of T2 . Our framework is agnostic to the exact logic of         Measure len also serves as the termination metric on lists
refinement predicates as long as validity of their boolean com-        (denoted with the termination keyword above): it maps lists
binations is decidable; our prototype implementation uses the          to a type that has a predefined well-founded order in our
quantifier-free logic of arrays2 , uninterpreted functions, and        language and thus enables termination checks for recursion
linear integer arithmetic, which is sufficient for all the exam-       on lists.
ples and benchmarks in this paper.                                        For the rest of the section, let us fix the set of logical
    A synthesis problem is defined by (1) a goal refinement            qualifiers Q to {? ≤ ?, ? 6= ?}, where ? is a placeholder
type T (2) a typing environment Γ and (3) a set of logical qual-       that can be instantiated with any program variable or ν.
ifiers Q. A solution to the synthesis problem is a program term           Given the specification
t that has the type T in the environment Γ. The environment                       n : Nat → x : α → {List α | len ν = n}
contains type signatures of components available to the syn-
thesizer (which may include datatype constructors, “library”           S YNQUID picks λ-abstraction as the top-level construct, and
functions, and local variables) as well as any path conditions         creates a synthesis subproblem for its body with a simpler
that can be assumed when synthesizing t. Qualifiers are pred-          goal type {List α | len ν = n}. The system need not
icates from the refinement logic used as building blocks for           consider other choices of the top-level construct, since every
unknown refinements and branch guards. Our system extracts             terminating program has an equivalent β-normal η-long form,
an initial set of such predicates automatically from the goal          where all functions are fully applied and the head of each
type and the types of components; for all our experiments,             application is a variable; moreover, the above decomposition
the automatically extracted qualifiers were sufficient to syn-         is precise, since any solution to the subproblem will satisfy
thesize all the necessary refinements, but in general the user         the top-level goal.
might have to provide additional predicates.                              As part of the decomposition, the arguments n : Nat and
    Given a synthesis problem, S YNQUID constructs a candi-            x : α are added to the environment, together with the function
date solution, by either by either picking a component in Γ            replicate itself, to account for the possibility that it may be
or decomposing the problem into simpler subproblems and                recursive. In order to ensure termination of recursive calls, the
recursively obtaining a solution ti to each one. Since the de-         system weakens the type of replicate in the environment to
composition is generally incomplete, a candidate obtained by
combining ti ’s is not guaranteed to have the desired type T ;          n0 : {Int | 0 ≤ ν < n} → x0 : α → {List α | len ν = n0 }
to check if the candidate is indeed a solution, the system gen-
                                                                       demanding that the first argument be strictly decreasing.
erates a subtyping constraint. If the constraint cannot be sat-
                                                                       S YNQUID picks n as the termination metric in this case, since
isfied, the system backtracks to pick a different combination
                                                                       it is the only argument whose type has an associated well-
of solutions to subproblems (or a different decomposition al-
                                                                       founded order.
together); the stronger the sub-goals produced during decom-
                                                                           In the body of the function, the top-level construct might
position, the less S YNQUID has to backtrack. The rest of the
                                                                       be a branching term. Rather than exploring this possibility
2 Arrays are used to model sets.                                       explicitly, S YNQUID adds a fresh predicate unknown P0 as


                                                                   3                                                            2016/4/22
a path condition to the environment, and then searches for             generic, we can define the type of binary search trees as fol-
a branch-free program term that satisfies the specification            lows:
assuming P0 . Each candidate branch-free term t is validated
by solving a subtyping constraint; as part of this process,              termination measure size     :: BST α → Int
S YNQUID discovers the weakest P0 that makes t satisfy the               measure keys      :: BST α → Set α
                                                                         data BST α where
specification. In case t is valid unconditionally, the weakest
                                                                           Empty :: {BST α | keys ν = []}
such P0 is True, and no branch is generated.
                                                                           Node :: x: α → l: BST{α | ν < x} → r: BST{α | x < ν}
   Suppose the first branch-free term that S YNQUID consid-
ers is Nil; this choice results in a subtyping constraint                       → {BST α | keys ν = keys l + keys r + [x]}
                                                                       According to this definition, one can obtain a BST either by
  n : Nat; x : α; P0 `                                                 taking an empty tree, or by composing a node with key x and
           {List β 0 | len ν = 0} <: {List α | len ν = n}              two BSTs, l and r, in which all keys are, respectively, strictly
                                                                       less and strictly greater than x. The type is additionally refined
                                                                       by the measure keys, which denotes the set of all keys in the
where β 0 is a free type variable. The constraint imposes two
                                                                       tree, and a termination measure size (size-related refinements
requirements: (i) the shapes of the two types (i.e. their under-
                                                                       are omitted in the interest of space).
lying unrefined types) must have a unifier [29] and (ii) the re-
                                                                          The following type specifies insertion into a BST:
finements of the subtype must subsume those of the supertype
under the assumptions encoded in the environment. The con-               insert :: x: α → t: BST α →
straint above gives rise to a unifier [β 0 7→ {α | P1 }] (where                                {BST α | keys ν = keys t + [x]}
P1 is a fresh predicate unknown) and two Horn constraints:
P0 ∧ P1 ⇒ > and 0 ≤ n ∧ P0 ∧ len ν = 0 ⇒ len ν = n.                    From this specification, S YNQUID generates the following
S YNQUID uses the MUSF IX Horn solver (Sec. 3.6) to find the           implementation within two seconds:
weakest assignment of liquid formulas to P0 and P1 that sat-             insert =    λ x . λ t . match t with
isfies both Horn constraints. A liquid formula is a conjunction             |    Empty → Node x Empty Empty
of atomic formulas, obtained by replacing ?-placeholders in                 |    Node y l r → if x ≤ y ∧ y ≤ x
each qualifier in Q with appropriate variables. If for some Pi                    then t
no valid assignment exists, or the weakest valid assignment is                    else if y ≤ x
a contradiction, the candidate program is discarded.                                then Node y l (insert x r)
    In our example, MUSF IX discovers the weakest assign-                           else Node y (insert x l) r
ment L = [P0 7→ n ≤ 0, P1 7→ >], effectively abducing
the necessary branching condition. Since the condition is not             Pattern matching in this example is synthesized using
trivially true, the system proceeds to synthesize the remaining        a special case of liquid abduction: type-checking the term
branch under the path condition ¬(n ≤ 0). A similar strategy           Node x Empty Empty against the goal type {BST α | keys ν =
for generating branching programs has been successfully em-            keys t + [x]}, causes the system to abduce the condition
ployed in several existing synthesis tools [1, 4, 20, 21] and is       keys t = [], which implies a match on t.
commonly referred to as condition abduction. Each condi-                  The challenging aspect of this example is reasoning about
tion abduction technique faces the challenge of searching a            sortedness. For example, for the term Node y l (insert x r)
large space of potential conditions efficiently; our approach,         to be type-correct, the recursive call must return the type
which we dub liquid abduction, addressed this challenge by             BST {α | y < ν}. This type does not appear explicitly in
restricting conditions to liquid formulas and using MUSF IX            the user-provided signature for insert; in fact, verifying this
to explore the space of liquid formulas efficiently.                   program requires discovering a nontrivial inductive invariant
    The remaining branch has to deal with the harder case              of insert (that adding a key greater than some value z into
of n > 0. When enumerating candidates for this branch,                 a tree with keys greater than z again produces a tree with
S YNQUID eventually decides to apply the replicate com-                keys greater than z), which puts this and similar examples
ponent (that is, make a recursive call), and searches for the          beyond reach of existing synthesizers based on Hoare-style
parameters via recursive application of the synthesis proce-           reasoning [20, 21].
dure. At this point, the strong precondition on the argument              In our framework, this property is easily inferred by the
m, 0 ≤ ν < n, which arises from the termination require-               Horn constraint solver in combination with polymorphic re-
ment, enables filtering candidate arguments locally, before            cursion. When insert is added to the environment, its type is
synthesizing the rest of the branch. In particular, the system         generalized to ∀β.x : β → u : {BST β | size u < size t} →
will discard the candidates n and inc n right away, since they         {BST β | keys ν = keys t + {x}}. At the site of the recur-
fail to produce a value strictly less than n.                          sive call, the precondition of Node y l imposes a constraint
    Example 2: Complex Data Structures and Invariant In-               that simplifies to BST β <: BST {α | y < ν}, which leads to
ference. Assuming comparison operators in our logic are                instantiating [β 7→ {α | P0 }] and [P0 7→ y < ν].


                                                                   4                                                             2016/4/22
    Importantly, due to round-trip type checking (Sec. 3.2),            of list elements. Given the above specification and a compo-
this assignment is discovered before the two arguments to               nent that appends an element to the end of the list (specified
insert are synthesized, which has the effect of propagating             in a similar fashion), S YNQUID synthesizes the standard im-
the requirement imposed by Node top-down through the ap-                plementation of list reversal.
plication of insert onto its arguments. In particular, using the           Example 4: Higher-Order Combinators and Auxiliary
goal type {α | y < ν} for the first argument of insert, the             Function Discovery. Complex programs might require recur-
system can immediately discard the candidate y, while trying            sive auxiliary functions. Discovering specifications for such
x succeeds and leads to the abduction of the branch condition           functions automatically is a difficult task, akin to lemma dis-
y ≤ x. As our evaluation shows, disabling this type of early            covery in theorem proving [7, 16, 25], which largely remains
filtering increases the synthesis time for this example from            an open problem. S YNQUID expects users to provide the high-
less than two seconds to over two minutes.                              level insight about a complex algorithm in the form of auxil-
    Example 3: Abstract Refinements. Using refinement                   iary function signatures. For example, if the goal is to synthe-
types as an interface to synthesis raises the question of their         size a list sorting function with the following signature
expressiveness. Restricting refinements to decidable logics
                                                                          sort :: xs: List α → {IList α | elems ν = elems xs}
fundamentally limits the class of programs they can fully
specify, and for other programs writing a refinement type               (where elems denotes the set of list elements), the user can
might be possible but cumbersome compared to providing a                express the insight behind different sorting algorithms by
set of input-output examples or a specification in a richer lan-        providing different auxiliary functions: insertion into a sorted
guage. The previous examples suggest that refinement types              list for insertion sort, splitting and merging for merge sort,
are effective for specifying programs that manipulate data              or partitioning and concatenation for quick sort. Naturally,
structures with nontrivial universal and inductive invariants.          the implementation of the auxiliary functions can in turn be
In this example we demonstrate how extending the type sys-              synthesized, but coming up with their specification is the
tem with abstract refinements allows us to express a wider              creative step that generally requires user interaction, and can
class of properties, for example, talk about the order of list          be considered a major hurdle on the path to fully automatic
elements.                                                               synthesis.
    Abstract refinements, proposed in [35], enable explicit                 It turns out, however, that replacing general recursion
quantification over refinements of datatypes and function               with higher-order combinators such as map and fold—a style
types. For example, a list datatype can be parameterized by a           widely used and highly encouraged in functional programming—
binary relation r that must hold between any in-order pair of           makes it possible to infer requirements on the auxiliary func-
elements in the list:                                                   tion from the specification of the main program. This is one
                                                                        of the main insights behind the synthesizer λ2 [12], which
  data RList α <r ::α → α → Bool> where
                                                                        relies on hard-coded rules for propagating input-output ex-
   Nil :: RList α <r>
                                                                        amples top-down through common combinators. S YNQUID
   Cons :: x: α → RList {α | r x ν} <r> → RList α <r>
                                                                        supports this top-down propagation of specifications out of
   On the one hand this enables concise definitions of lists            the box thanks to the combination of refinement types and
with various inductive properties as instantiations of RList:           polymorphism.
                                                                            Consider the following type for function foldr, which
  IList α = RList α < λ x λ y . x ≤ y> -- Increasing list               folds a binary operation f over a list ys from right to left:
  UList α = RList α < λ x λ y . x 6= y> -- Unique list
  List α = RList α < λ x λ y . True> -- Unrestricted list                 foldr ::<p :: List β → γ → Bool> .
                                                                             f: (t: List β → h: β → acc: {γ | p t ν} →
    On the other hand, making list-manipulating functions                            {γ | p (Cons h t) ν}) →
polymorphic in this relation, provides an elegant way to spec-               seed: {γ | p Nil ν} →
ify order-related properties. Consider the following type for                ys: List β → {γ | p ys ν}
list reversal:
                                                                        The shape of this type is slightly different from the usual sig-
  reverse :: <r ::α → α → Bool> . xs: RList α <r> →                     nature of foldr: the operation f takes an extra ghost argu-
    {RList α < λ x λ y . r y x> | len ν = len xs}                       ment t, which denotes the part of the list that has already been
                                                                        folded3 . The type of is parametrized by a binary relation p
It says that whatever relation holds between every in-order
                                                                        that foldr establishes between the input list ys and the out-
pair of elements of the input list, also has to hold between ev-
                                                                        put; it requires that the relationship hold between the empty
ery out-of-order pair of elements of the output list. This type
                                                                        list and the seed, and that applying f to a head element h and
does not restrict the applicability of reverse, since at the call
                                                                        the result of folding a tail list t yield a result that satisfies the
site r can always be instantiated with True; the implementa-
tion of reverse, however, has to be correct to any value of r,          3 Extending S YNQUID with bounded refinement types [38] would enable a

which leaves the synthesizer no choice but reverse the order            more natural specification without the ghost argument.


                                                                    5                                                                2016/4/22
relationship with Cons h t (in other words, p plays the role of         how users specify synthesis goals—but cannot rely on any an-
a loop invariant). Note that folding a list left-to-right (foldl)       notations beyond that; in particular, the types of all polymor-
requires a more complex specification that cannot currently             phic instantiations and arguments of anonymous functions
be expressed within the S YNQUID type system.                           must be inferred. The second requirement is to detect type
    What happens if we ask S YNQUID to synthesize sort,                 errors locally: intuitively, if a subterm of a program causes a
while providing foldr as the only component? When trying                type error independently of its context, the algorithm should
out an application of foldr, round-trip type checking handles           be able to report that error without analyzing the context.
its higher-order argument, f, in a special way, since in our               We build our type checking mechanism as an extension to
type system, as in [32], f cannot appear in the result type of          the the liquid types framework [19, 32], which uses a com-
foldr. Consequently, the exact value of f is not required to            bination of Hidley-Milner unification and a Horn solver to
determine the type of the application, which gives S YNQUID             infer refinement types. The original liquid type inference al-
the freedom to synthesize it independently from the rest of the         gorithm is not designed for synthesis, and thus makes differ-
program.                                                                ent trade-offs: in particular it does not satisfy the locality re-
    The tool quickly figures out that foldr ?? Nil xs has the           quirement. Our type checking mechanism achieves locality
required type {IList α | elems ν = elems xs}, given the fol-            based on three key ideas. First, we apply bidirectional type
lowing assignment to foldr’s type and predicate variables:              checking [30] to refinement types and reinforce it with addi-
[β 7→ α, γ 7→ IList α, p 7→ λas.λbs.elems bs = elems as].               tional top-down propagation of type information, arriving at
Now that S YNQUID comes back to the task of filling in the              round-trip type checking (Sec. 3.2); we then further improve
first argument of foldr, its required type has been determined          locality of rules for for function applications and branching
entirely as                                                             statements (Sec. 3.4). Second, we develop a new algorithm for
                                                                        converting subtyping constraints into horn clauses, which is
  t: List α → h: α →
                                                                        able to do so incrementally as the constraints are issued before
     acc: {IList α | elems ν = elems t} →
                                                                        analyzing the whole program (Sec. 3.5). Finally, we propose
     {IList α | elems ν = elems (Cons h t)}
                                                                        a new, efficient implementation for a greatest-fixpoint Horn
(where elems (Cons h t) is expanded into [h] + elems t us-              solver (Sec. 3.6). In the interest of space we omit abstract re-
ing the definition of the elems measure in the type of Cons); in        finements (see Sec. 2) from the formalization; [35] has shown
other words, the auxiliary function must insert h into a sorted         that integrating this mechanism into the type system that al-
list acc. Treating this inferred signature as an independent            ready supports parametric polymorphism is straightforward.
synthesis goal, S YNQUID easily synthesizes a recursive pro-               In Sec. 3.7 we derive synthesis rules from the modular type
gram for insertion into a sorted list, and thus completes the           checking rules; in doing so we follow previous work on type-
following implementation of insertion sort without requir-              directed synthesis [17, 27], which has shown how to turn type
ing any hints from the user, apart from a general recursion             checking rules for a language into synthesis rules for the same
scheme:                                                                 language.

  sort =   λ xs . foldr f Nil xs                                        3.1   Syntax and Types
     where f =   λ t . λ h . λ acc .                                    Fig. 2 shows the syntax of the S YNQUID language.
       match acc with                                                       Terms. Unlike previous work, we differentiate between the
         Nil → Cons h Nil                                               languages of refinements and programs. The former consists
         Cons z zs → if h ≤ z                                           of refinement terms ψ, which have sorts ∆; the exact set of
           then Cons h (Cons z zs)                                      interpreted symbols and sorts depends on the chosen refine-
           else Cons z (f zs h zs)                                      ment logic. We refer to refinement terms of the Boolean sort
                                                                        B as formulas.
   The next section gives a formal account of the S YNQUID
                                                                            The language of programs consists of program terms t,
language and type system, and details its modular type check-
                                                                        which we split, following [27] into elimination and intro-
ing mechanism, which enables scalable synthesis.
                                                                        duction terms (E-terms and I-terms for short). Intuitively, E-
                                                                        terms—variables and applications—propagate type informa-
3.   The S YNQUID Language                                              tion bottom-up, composing a complex property from prop-
The central goal of this section is to develop a type check-            erties of their components; I-terms propagate type informa-
ing algorithm for a core programming language with refine-              tion top-down, decomposing a complex requirement into sim-
ment types that is geared towards candidate validation in the           pler requirements for their components. Note that conditional
context of synthesis. This context imposes two important re-            guards, match scrutinees, and left-hand sides of applications
quirements on the type checking mechanism which are neces-              are restricted to E-terms. We further separate I-terms into
sary for the synthesis procedure to be automatic and scalable.          branching terms—conditionals and matches—and function
The first one has to do with the amount of type inference:              terms—abstractions and fixpoints—and disallow branching
the mechanism can expect top-level type annotations—this is             terms on the right-hand side of application. This normal form


                                                                    6                                                             2016/4/22
                                                                          Well-Formed Types       Γ ` T̂
   ψ    ::=                                    Refinement term:
           | > | ⊥ | 0 | + | . . . (varies)    interpreted symbol                      Γ; ν : B ` ψ                  Γ; C ` T
           |x                                  uninterpreted symbol            WF-S C                    WF-C TX
                                                                                       Γ ` {B | ψ}                 Γ ` let C in T
           |ψψ                                 application
                                                                                           Γ ` {B | ψ}     Γ; x : {B | ψ} ` T
                                                                                   WF-FO
   ∆    ::=                                    Sort:                                              Γ ` x : {B | ψ} → T
           | B | Z | . . . (varies)            interpreted                                  Tx non-scalar Γ ` Tx       Γ`T
                                                                                   WF-HO
           |δ                                  uninterpreted                                          Γ ` Tx → T
   t    ::= e | b | f                          Program term
   e    ::=                                    E-term:                    Subtyping      Γ ` T <: T 0
           |x                                  variable
           | ee | ef                           application                              Γ ` B <: B 0       Valid(JΓKψ⇒ψ0 ∧ ψ ⇒ ψ 0 )
                                                                              <:-S C
   b    ::=                                    Branching term:                                 Γ ` {B | ψ} <: {B 0 | ψ 0 }
           | if e then t else t                conditional                              Γ ` Ty <: Tx     Γ; y : Ty ` [y/x]T <: T 0
           | match e with |i Ci hxji i 7→ ti   match                         <:-F UN
                                                                                         Γ ` x : Tx → T <: y : Ty → T 0
   f    ::=                                    Function term:
                                                                                    Γ ` Ti <: Ti0
           | λx.t                              abstraction                  <:-DT                      <:-R EFL
           | fix x.t                           fixpoint                           Γ ` D Ti <: D Ti0              Γ ` B <: B
   B    ::=                                    Base type:
           | Bool | Int                        primitive                            Figure 3. Well-formedness and subtyping.
           | D Ti                              datatype
           |α                                  type variable
   T    ::=                                    Type:                          Environments, Well-Formedness, and Subtyping. A typ-
           | {B | ψ}                           scalar                     ing environment Γ is a sequence of variable bindings x : T
           | x: T → T                          function                   and path conditions ψ; we denote conjunction of all path
   S    ::= ∀αi .T                             Type schema                conditions in an environment as P(Γ). A formula ψ is well-
   C    ::= · | x : T ; C                      Context                    formed in the environment Γ, written Γ ` ψ, if it is of a
   T̂   ::= let C in T                         Contextual Type            Boolean sort and each of its free variables is bound in Γ to a
                                                                          type that is consistent with its sort in ψ. Well-formedness ex-
                   Figure 2. Terms and types.                             tends to types as shown in Fig. 3. Note the two different rules
                                                                          for first-order and higher-order function types: in a function
                                                                          type x : T1 → T2 , T2 may reference the formal argument x
is required to enable precise and efficient local type checking,          only if T1 is a scalar type (that is, only first-order function
as explained below. It does not fundamentally restrict the ex-            types are dependent).
pressiveness of the language: every terminating program in                    The subtyping relation Γ ` T <: T 0 is relatively standard
lambda calculus can be translated to S YNQUID by first ap-                (Fig. 3). For simplicity, we consider all datatypes covariant
plying a standard β-normal η-long form [15, 27] and then                  in their type parameters (rule <:-DT); if need be, variance
pushing branching terms outside of applications, guards, and              can be selected per type parameter depending on whether it
scrutinees.                                                               appears positively or negatively in the constructors. The cru-
    Types and Schemas. A S YNQUID type is either a scalar—                cial part is the rule <:-S C, which reduces subtyping between
base type refined with a formula—or a dependent func-                     scalar types to implication between their refinements, under
tion type. Base types include primitives, type variables, and             the assumptions extracted from the environment. Since the re-
user-defined datatypes with zero or more type parameters.                 finements are drawn from a decidable logic, this implication
Datatype constructors are represented simply as functions                 is decidable. The function that extracts assumptions from the
that must have the type ∀α1 . . . αm .T1 → . . . → Tk →                   environment is parametrized by a formula ψ and returns a
D α1 . . . αm . A contextual type is a pair of a sequence of              conjunction of all path conditions and refinements of all vari-
variable bindings and a type that can mention those variables;            ables mentioned in ψ or the path conditions:
contextual types are useful for precise type checking of appli-
cations, as explained in Sec. 3.2.                                                      JΓKψ = P(Γ) ∧ BFV(P(Γ))∪FV(ψ) (Γ)
    S YNQUID features ML-style polymorphism, where type                   where
variables are universally quantified at the outermost level to                                    (
yield type schemas. Unlike ML, we restrict type variables to                                          [x/ν]ψ ∧ Bv\{x}∪FV(ψ) (Γ)        (x ∈ v)
range only over scalars, which gives us the ability to deter-             Bv (Γ; x : {B | ψ}) =
                                                                                                      Bv (Γ) (otherwise)
mine whether a type is a scalar, even if it contains free type
variables. We found this restriction not to be too limiting in                    Bv (Γ; x : T ) = Bv (Γ) (T non-scalar)
practice.                                                                                Bv (·) = >


                                                                      7                                                             2016/4/22
This definition limits the effect of an environment variable            Type Strengthening        Γ `Q e ↓ T ↑ Tˆ0
with an inconsistent refinement to only those subtyping judg-
ments that (transitively) mention that variable.                                        Γ(x) = {B | ψ} Γ ` {B | ψ} <: T
                                                                                 VAR S C
                                                                                            Γ `Q x ↓ T ↑ {B | ν = x}
3.2   Round-Trip Type Checking                                                     Γ(x) = ∀αi .T 0 Γ `Q Ti Γ ` [Ti /α]T 0 <: T
                                                                          VAR∀
                                                                                              Γ `Q x ↓ T ↑ [Ti /α]T 0
This section describes the core of S YNQUID’s type system.
It is inspired by bidirectional type checking [30], which in-                      Γ `Q e1 ↓ {B | ⊥} → T ↑ let C1 in (x : {B | ψ} → T 0 )
                                                                                           Γ; C1 `Q e2 ↓ {B | ψ} ↑ let C2 in Tx
terleaves top-down and bottom-up propagation of type infor-
                                                                                                 Γ; C1 ; C2 ; x : Tx ` T 0 <: T
mation depending on the syntactic structure of the program,             A PP FO
                                                                                          Γ `Q e1 e2 ↓ T ↑ let C1 ; C2 ; x : Tx in T 0
with the goal of making type checks more local. Bidirectional
typing rules use two kinds of typing judgments: an inference                           Γ `Q e ↓ bot → T ↑ let C in (Tx0 → T 0 )
                                                                                                    Γ; C `Q f ↓ Tx0
judgment, written Γ ` e ↑ T , states that the term t gen-                     A PP HO
erates type T in the environment Γ; a checking judgment,                                     Γ `Q e f ↓ T ↑ let C in T 0
Γ ` t ↓ T , states that the term t checks against a known
                                                                        Type Checking       Γ `Q t ↓ S
type T in the environment Γ. Accordingly, all typing rules
can be split into inference and checking rules, depending on                                    Γ `Q e ↓ T ↑ Tˆ0
the judgment they derive. Bidirectional type checking rules                                  IE
                                                                                                    Γ `Q e ↓ T
for S YNQUID are given in Appendix A.
                                                                                              Γ; y : Tx `Q t ↓ [y/x]T
    In a bidirectional system, analyzing a program starts with                         A BS
                                                                                             Γ `Q λy.t ↓ (x : Tx → T )
propagating its top-level type annotation top-down using
                                                                                       Γ `Q e ↓ Bool ↑ let C in {Bool | ψ}
checking rules, until the system encounters a term t to which
                                                                               Γ; C; [>/ν]ψ `Q t1 ↓ T       Γ; C; [⊥/ν]ψ `Q t2 ↓ T
no checking rule applies. At this point the system switches               IF
                                                                                           Γ `Q if e then t1 else t2 ↓ T
to bottom-up mode, infers the type T 0 of t, and checks if T 0
                                                                                         Γ `Q e ↓ top ↑ let C in {D Tk | ψ}
is a subtype of the goal type; if the check fails, t is rejected.                        j
                                                                                  Ci = Ti → {D Tk | ψi }
                                                                                                        0
                                                                                                              Γi = {xji : Tij }; [x0 /ν]ψi0
Bidirectional type propagation is “all-or-nothing”: once a                                            0
                                                                                              Γ; C; [x /ν]ψ; Γi `Q ti ↓ T
checking problem for a term cannot be decomposed perfectly              M ATCH
into checking problems for its subterms, the system abandons                              Γ `Q match e with |i Ci hxji i 7→ ti ↓ T
all information about the goal type and switches to purely                                   Γ `Q t ↓ T      αi not free in Γ
                                                                                      TA BS
bottom-up inference. Our insight is that some information                                          Γ `Q t ↓ ∀αi .T
from the goal type can be retained in the bottom-up phase,                                       Γ; x : S ≺ `Q t ↓ S
                                                                                            F IX
leading to more local error detection. To this end, we mod-                                       Γ `Q fix x.t ↓ S
ify the bidirectional inference judgment into a strengthening
judgment Γ ` t ↓ T ↑ T 0 , which reads as follows: in                             Figure 4. Rules of round-trip type checking.
the environment Γ, term t checks against a known type T and
generates a stronger type T 0 . We call the resulting type system
                                                                            In order to support goals types with an underspecified
round-trip, since it propagates types top-down and then back
                                                                        shape (as required for match scrutinees and higher-order ap-
up.
                                                                        plications), we augment S YNQUID with top and bot types,
    Derivation rules for round-trip type checking are presented
                                                                        which are, respectively, a supertype and a subtype of every
in Fig. 4. All judgments are parametrized by the set of quali-
                                                                        type. Note that these types are ignored when computing the
fiers Q, used to construct unknown refinements as explained
                                                                        logical representation of the environment JΓKψ , since they are
below. Checking rules encode the way a checking judgment
                                                                        not considered scalar. Also note that the precision of round-
for an I-term t is decomposed into simpler checking judg-
                                                                        trip type checking crucially relies on the fact that only E-
ments for its components. Strengthening rules encode the
                                                                        terms appear in strengthening judgments; this is why S YN -
way a goal type for an E-term e is decomposed into over-
                                                                        QUID bans branching terms from function arguments, condi-
approximate goal types for its subterms, which are necessary
                                                                        tional guards, and match scrutinees.
but in general not sufficient for correctness, while the precise
                                                                            Polymorphic instantiations. The rule VAR∀, which han-
type of e is constructed from the inferred types of its subterms.
                                                                        dles polymorphic instantiations, replaces type variables αi
A round-trip type checker starts with a top-down phase, just
                                                                        with types Ti chosen nondeterministically to satisfy all sub-
as a bidirectional one would; when it encounters an E-term,
                                                                        typing checks4 . In order to tame this nondeterminism, follow-
it applies the corresponding strengthening rule and discards
                                                                        ing [32], we restrict Ti s to liquid types. A formula ψ is liquid
the inferred type (see rule IE). Thus, instead of detecting type
                                                                        in Γ with qualifiers Q, written Γ `Q ψ, if it is a conjunction
errors at the boundary between I- and E-terms, the round-trip
system performs local checks for each variable and function             4 The same rule handles monomorphic non-scalar variables, assuming zero

application.                                                            type variables.


                                                                    8                                                                 2016/4/22
of well-formed formulas, each of which is obtained from a              and r—and subtyping on base types, List T0 <: List Pos,
qualifier in Q by substituting ?-placeholders with variables.          which is not vacuous since here l and r are out of scope. The
This notion extends to types, Γ `Q T , in a way analogous to           first argument of append is checked against the type List T0
well-formedness (Fig. 3). Note that the set of all liquid for-         (in the second premise of A PP FO), which imposes a subtyp-
mulas in a given environment is finite, and so is the set of all       ing check Γ ` List Nat <: List T0 . Since no type T0 satis-
liquid types with a fixed shape. Sec. 3.5 and Sec. 3.6 present         fies both subtyping relations, the type checker rejects the term
a deterministic algorithm for finding the types Ti .                   append xs.
    Applications. The application rules A PP FO and AppHO
                                                                           Recursion. Another rule in Fig. 4 that deserves some dis-
are the core of the round-trip type system: they are responsible
                                                                       cussion is F IX, which comes with a termination check. In the
for propagating partial type information down to the left-hand
                                                                       context of synthesis, termination concerns are impossible to
side of an application. The type system distinguishes between
                                                                       ignore, since non-terminating recursive programs are always
first-order and higher-order applications, since in a function
                                                                       simpler than terminating ones, and thus would be synthesized
type x : T1 → T2 , T2 cannot mention x if T1 is a function type
                                                                       first if considered correct. The F IX rule gives the “recursive
(see Fig. 3). As a result, a higher-order application always
                                                                       call” a termination-weakened type S ≺ , which intuitively de-
yields the type T2 independently of the argument. If instead
                                                                       notes “S with strictly smaller arguments”. The exact defini-
T1 is a scalar type, we have to replace x inside T2 with
                                                                       tion of termination-weakening is a parameter to our system.
the actual argument of the application. Unfortunately, we
                                                                       Our implementation provides a predefined well-founded or-
cannot assign the application e1 e2 the type [e2 /x]T2 , since
                                                                       der on primitive base types, and allows the user to define one
e2 is a program term, which does not necessarily have a
                                                                       on datatypes by mapping them to primitive types using termi-
corresponding refinement precisely capturing its semantics.
                                                                       nation metrics; then S ≺ is defined as a lexicographic order on
We address this problem by assigning e1 e2 a contextual type
                                                                       the tuple of all arguments of S that have an associated well-
let C in T2 , where the context C binds the variable x to the
                                                                       founded order.
precise type of e2 .
Example. We demonstrate the local error detection enabled              3.3   Soundness and Completeness
by rule A PP FO on the following type-checking problem:                We show soundness and completeness of round-trip type
       Γ `Q append xs xs ↓ {List Pos | len ν = 5}                      checking relative to purely bottom-up liquid type infer-
                                                                       ence [32]. For detailed proofs see Appendix A.
where Pos is an abbreviation for {Int | ν > 0} and Γ contains              Round-trip type checking is sound in the sense that when-
the following bindings:                                                ever a S YNQUID term t type-checks against a schema S,
     xs : {List Nat | len ν = 2};                                      Γ `Q t ↓ S, there exist a set of qualifiers Q0 and a
                                                                       schema S 0 , such that the bottom-up system infers S 0 for t,
     append : ∀α. l : {List α | len ν ≥ 0}
                                                                       Γ `Q0 t :: S, and Γ ` S 0 <: S. Note that bottom-up infer-
                    → r : {List α | len ν ≥ 0}                         ence might require strictly more qualifiers than type check-
                    → {List α | len ν = len l + len r}                 ing: in the bottom-up system, generating types for branch-
                                                                       ing statements and abstractions imposes the requirement that
Intuitively, the constraint on the length of the output list is        these types be liquid; the round-trip system obtains the types
hard to verify without analyzing the whole expression, while           of those terms by decomposing the goal type, thus the liq-
the mismatch in the type of the list elements can be easily            uid restriction does not apply. In practice the difference is ir-
found without considering the second argument of append.               relevant, since the type inference algorithm can extract the
Refinement types provide precise means to distinguish those            missing qualifiers from the top-level goal type and the pre-
cases: the length-related refinement of append is dependent            conditions of component functions. Thus, if Q contains a suf-
on the arguments l and r, whereas the type of the list elements        ficient set of qualifiers such that the goals schema is liquid
cannot possibly mention l or r, since it has to be well-formed         (Γ `Q S) and the preconditions of component function are
in a scope where these variables are not defined.                      liquid, which we denote as `Q Γ, then we can take Q0 = Q.
   Applying the A PP FO rule twice to the judgment above
yields Γ `Q append ↓ {B0 | ⊥} → {B1 | ⊥} →                             Theorem 1 (Soundness of round-trip type checking). If `Q
{List Pos | len ν = 2}, where the base types B0 and B1                 Γ, Γ `Q S, and Γ `Q t ↓ S, then Γ `Q t :: S 0 and
are yet to be inferred. Applying VAR∀, and decomposing the             Γ `Q S 0 <: S.
resulting subtyping check with <:-F UN, we get                            Unlike liquid type inference, the round-trip system re-
Γ; l : {B0 | ⊥}; r : {B1 | ⊥} `                                        quires a proof of termination for all fixpoints; thus if Γ `Q
                                                                       t :: S, but t’s termination cannot be shown using the cho-
{List T0 | len ν = len l + len r} <: {List Pos | len ν = 2}
                                                                       sen definition of termination weakening, the round-trip type
Using <:-S C, this judgment can be decomposed into an im-              system will reject t. Thus we show completeness for a weak-
plication on refinements—vacuous thanks to the types of l              ened round-trip system, obtained from Fig. 4 by replacing S ≺


                                                                   9                                                            2016/4/22
Consistency     Γ ` T ∧ : T0                                            type-correct boolean expressions as guards and then checking
                                                                        if any of them enables synthesis of a correct branch. The goal
                Γ ` B ∧ : B0    Sat(JΓKψ∧ψ0 ∧ ψ ∧ ψ 0 )                 of this section is to improve the locality of the I F rule in order
      ∧ :-S C
                      Γ ` {B | ψ} ∧ : {B 0 | ψ 0 }                      to avoid such blind enumeration.
                       Γ; x : Tx ` T ∧ : [x/y]T 0                           The idea comes from condition abduction [4, 20, 21]:
         ∧ :-F UN                                                       instead of starting with the guard, for which no information
                Γ ` x : Tx → T ∧ : y : Ty → T 0
            Γ ` Ti ∧ : Ti0
                                                                        can be extracted from the goal type, start by analyzing one of
   ∧ :-DT                     ∧ :-R EFL                                 the branches and use logical abduction to infer the weakest
          Γ ` D Ti ∧ : D Ti0             Γ`B∧:B
                                                                        assumption under which the branch fulfills the goal type.
                                                                        If such a condition does not exist or is a contradiction, the
                 Figure 5. Type consistency.                            branch candidate is deemed ill-typed; otherwise the abduced
                                                                        condition can be used as a specification for the guard.
in the premise of the F IX rule by S. We denote the checking                This strategy relies on the availability of a sufficiently fast
judgment of the modified system as Γ `∗Q t ↓ S.                         mechanism to perform logical abduction, which is generally
Theorem 2 (Completeness of round-trip type checking). If                challenging. In S YNQUID, we treat unknown path conditions
Γ `Q t :: S, then Γ `∗Q t ↓ S.                                          the same way as unknown refinements in polymorphic instan-
                                                                        tiations: we restrict their valuations to liquid formulas over
3.4   Type System Extensions                                            environment variables, and use the greatest-fixpoint Horn
In this section we further improve the locality of type check-          solver (described in Sec. 3.6) to discover the weakest such
ing for function applications and branching terms.                      valuation. We refer to the modified rule for conditionals as
    Type Consistency. Recall the type checking problem                  the liquid abduction rule:

       Γ `Q append xs xs ↓ {List Pos | len ν = 5}                                          Γ `Q ψ           Sat(JΓKψ ∧ ψ)
                                                                                              Γ `Q e ↓ {Bool | ν = ψ}
from Sec. 3.2, and let us change the type of xs to {List Pos |                          Γ; ψ `Q t1 ↓ T      Γ; ¬ψ `Q t2 ↓ T
                                                                               I FA B
len ν = 6}. In this case, xs has the right element type, Pos,                               Γ `Q if e then t1 else t2 ↓ T
but intuitively the partial application append xs can still be
safely rejected, since no second argument with a non-negative           This rule limits completeness of round-trip type checking by
length can fulfill the goal type.                                       restricting valid guard types to the form above. Most notably,
    To formalize this intuition we introduce the notion of type         it excludes guards that contain function composition, and thus
consistency, defined in Fig. 5. Two scalar types are consistent         users have to provide wrapper components to encapsulate
if they have a common inhabitant for some valid valuation of            complex guard predicates; in all our experiments, the set of
environment variables. For function types, the relation is not          required guard components was quite intuitive, thus we con-
symmetric: a type x : Tx → T is consistent with a goal type             clude that the trade-off between expressiveness and efficiency
if their return types are consistent for some value of x of type        offered by liquid abduction is reasonable in the context syn-
Tx .                                                                    thesis.
    We add a premise Γ ` T ∧ : T 0 to every rule in Fig. 4                  Match Abduction. A similar technique can be used to
that already has the premise of the form Γ ` T <: T 0 . The             propose pattern matching, assuming the types of potential
additional premise has no effect on full applications, since            scrutinees are restricted to liquid types. In this case, however,
for scalar types consistency is subsumed by subtyping. The              the liquid restriction imposes more substantial limitations on
consistency check can, however, reject a partial application            the structure of the program: abduction only works if the
e allowed by subtyping, due to goals generated by the rule              scrutinee is a variable and its datatype has at least one scalar
A PP FO, which have a vacuous argument type {B | ⊥}. It is              constructor (such as Nil in List). Thus, S YNQUID employs
easy to show that in the absence of consistency checks, any             a combined approach: it first tries an abduction-based rule,
application of such e would always be rejected by the sub-              but if that fails, the system reverts to the original M ATCH rule
typing check in A PP FO; thus introducing consistency checks            of Fig. 4. As a result, type checking (and synthesis) enjoys
does not affect completeness of type checking. With consis-             the efficiency benefits of abduction without compromising
tency checks in place, the term append xs in the example                completeness.
above is rejected since the formula len xs = 6 ∧ len r ≥
0 ∧ len ν = len xs + len r ∧ len ν = 5 is unsatisfiable.                3.5   The Local Liquid Type Checking Algorithm
    Liquid Abduction. Consider the I F rule in Fig. 4: the              Starting from the round-trip typing rules presented above, this
type checker can analyze the two branches of the conditional            section develops local liquid type checking: a deterministic
independently of each other, but can only proceed with either           algorithm that takes as input a S YNQUID program t, an envi-
branch once the precise type of the guard has been inferred.            ronment Γ, a goal schema S, and a set of qualifiers Q, and
In the context of synthesis this amount to blindly enumerating          either produces a derivation of Γ `Q t ↓ S or rejects


                                                                   10                                                              2016/4/22
the program. The main challenge is to find suitable instan-
tiations for polymorphic components, as required by the rule                       Solve(Γ ` c) = match c with
VAR∀; to this end, the algorithm replaces the type variables                             | {α0 | ψ} <: T, α0 ∈ dom(T ) −→
αi in the component schema with fresh free type variables                                  C ← C ∪ {Γ ` Refine(T (α0 ), ψ) <: T }                    (1)
αi0 5 , extracts subtyping constraints on αi0 from the subtyping
premises of the derivation, and then solves the subtyping con-                           | T <: {α0 | ψ}, α0 ∈ dom(T ) −→ (symmetrical)              (2)
straints to either discover a valid type assignment mapping                              | {α0 | ψ1 } <: {β 0 | ψ2 } −→
free type variables to liquid types, or conclude that such an                              C ← C ∪ {α0 | ψ1 } <: {β 0 | ψ2 }                         (3)
assignment does not exist.                                                                   0
                                                                                         | {α | ψ} <: T, α ∈
                                                                                                           / T −→  0
     For the purpose of constraint solving, we extend the syntax
of refinement terms with predicate unknowns Pi . Local liquid                              T ← T [α0 7→ Fresh(T )];
type checking maintains a set of subtyping constraints C =                                 C := C ∪ {Γ ` {α0 | ψ} <: T }                             (4)
{Γi ` Ti <: Ti0 }, a set of Horn constraints H = {ψi }, a                                          0
                                                                                         | T <: {α | ψ} −→ (symmetrical)                             (5)
type assignment T = [αi0 7→ Ti ], and a liquid assignment
                                                                                         | (x : Tx → T1 ) <: (y : Ty → T2 ) −→
L = [Pi → {ψ}i ]. We denote with JψKL the formula ψ
with all predicate unknowns substituted with conjunctions of                               C ← C ∪ {Γ ` Ty <: Tx , Γ; y : Ty ` [y/x]T1 <: T2 }
                                                                                                                                              (6)
their valuations in L. The type checking process alternates
between the following two steps: it either extends the type                              | {D T1i | ψ1 } <: {D T2i | ψ2 } −→
derivation by applying one of the rules of Fig. 4, adding any                              C ← C ∪ {Γ ` {D | ψ1 } <: {D | ψ2 }, Γ ` T1i <: T2i }
of its subtyping premises to C, or it picks a constraint c from C                                                                             (7)
and solves it; constraint solving is formalized in the procedure                         | {B | ψ1 } <: {B | ψ2 } −→
Solve in Fig. 6.
                                                                                           H ← H ∪ {JΓKψ1 ⇒ψ2 ∧ ψ1 ⇒ ψ2 };                           (8)
     Solve does one of the following, depending on the operands
of a subtyping constraint: it either substitutes a type variable                           L ← Horn(L, H)
for which an assignment already exists (Eq. 1, Eq. 2), uni-                              | otherwise −→ fail                                         (9)
fies a type variable with a type (Eq. 4, Eq. 5), decomposes                                            0                    0
subtyping over compound types (Eq. 6, Eq. 7), or translates                       Refine({B | ψ}, ψ ) = {B | ψ ∧ ψ }
subtyping over scalar types into a Horn constraint and uses                       Fresh(T ) = match T with
the procedure Horn, described in the next section, to find an                               | {α0 | ψ} −→ β 0
L that satisfies all Horn constraints (Eq. 8). Local liquid type
                                                                                            | {D T i | ψ} −→ {D Fresh(T i ) | P },         L ← L[P 7→ ∅]
checking terminates when the entire type derivation has been
built, and all constraints in C are between free type variables                             | {B | ψ} −→ {B | P },              L ← L[P 7→ ∅]
(only Eq. 3 applies).                                                             Horn(L, H) = if ∀h ∈ H.Valid(JhKL ) then L else
     During unification of α0 and T , procedure Fresh inserts                                          let h ← {H | ¬Valid(JhKL )} in
fresh predicate unknowns in place of all refinements in T ;                                                    0
                                                                                                       let L       ← Strengthen(L, h) in Horn(L0 , H)
note that due to the incremental nature of our algorithm, T
might itself contain free type variables, which are simply re-
placed with fresh free type variables to be unified later as more                           Figure 6. Solving subtyping constraints.
subtyping constraints arise. This novel feature of local liquid
type checking, which we call incremental unification, is cru-
                                                                                  the latter is retained in C. If further type checking produces a
cial for early error detection. Existing refinement type check-
                                                                                  subtyping constraint on β 0 , say Nat <: β 0 , T will be extended
ers [13, 32] cannot interleave shape and refinement discov-
                                                                                  with an assignment [β 0 → {Int | P1 }], which in turn will lead
ery, since they rely on the global Hindley-Milner inference
                                                                                  to transforming the constraint on γ 0 into ` γ 0 <: {Int | P1 }
algorithm to fully reconstruct the shapes of all types in the
                                                                                  and instantiating [γ 0 → {Int | P2 }], at which point all free
program before discovering their refinements.
                                                                                  type variables have been eliminated.
Example. Starting from empty T and L, Solve(` α0 <:
List β 0 | len ν > 0) instantiates α0 by Eq. 4 leading to                         3.6   Solving Horn Clauses
T = [α0 7→ {List γ 0 | P0 }], L = [P0 7→ ∅] and recycles the
                                                                                  The set of Horn constraints H produced by Solve in Fig. 6
subtyping constraint; next by Eq. 1 and Eq. 7, the constraint is
                                                                                  consists of implications of the form ψ ⇒ ψ 0 , where each side
decomposed into ` {List | P0 } <: {List | len ν > 0}
                                                                                  is a conjunction of a known formula and zero or more pred-
and ` γ 0 <: β 0 . The former produces a Horn constraint
                                                                                  icate unknowns P . The goal of the procedure Horn is to find
P0 ⇒ len ν > 0, which leads to strengthening L[P0 ], while
                                                                                  a liquid assignment to P that validates all constraints in H or
5 We prime the names of free type variables to differentiate them from the        determine that H is unsatisfiable. The space of possible valu-
bound type variables of the top-level goal schema.                                ations of each P is 2QP , where QP is a set of atomic formu-


                                                                             11                                                                 2016/4/22
las obtained by instantiating qualifiers Q in the environment            prunes out semantically
                                                                                     V       V redundant subsets, i.e. it removes a
where P was created.                                                     subset mi if mi ⇒ mj for some j 6= i.
     Local liquid type checking invokes Horn after every new
Horn constraint is issued, and expects to detect an unsatis-             3.7   Synthesis from Refinement Types
fiable set of constraints—and thus a type error—as early as              From the rules of round-trip type checking we can obtain syn-
possible. Round-trip typing rules—in particular, A PP FO and             thesis rules, following the approach of [27] and reinterpreting
I F -A BD—produce constraints in a specific order, such that             the checking and strengthening judgments in such a way that
for each unknown P , implications where P appears nega-                  the term t is considered unknown. This interpretation yields
tively (on the left) are issued before the ones where it appears         a synthesis procedure, which, given a goal schema S, picks
positively (on the right). To enable early error detection in            a rule where the goal schema in the conclusion matches S,
this setting, procedure Horn looks for the weakest valuation             and constructs the term t from subterms obtained from the
of each P that validates all Horn constraints issued so far, and         rule’s premises. More concretely, starting from the top-level
deems H unsatisfiable if for some P such a valuation does                goal schema S, the algorithm always starts by applying rule
not exist or is inconsistent (an inconsistent valuation can be           F IX (if S ≺ is defined) followed by TA BS (if the schema is
safely discarded since it is guaranteed to violate some future           polymorphic), and finally A BS (if the goal type is a function
constraint where P appears positively).                                  type). Given a scalar goal, the procedure performs exhaustive
     As an optimization, Horn always starts form the current as-         enumeration of well-typed E-terms up to a given bound on
signment L and possibly makes it stronger, since all weaker              their depth, solving subtyping constraints at every node and
assignments are known to be too weak to satisfy the previ-               simultaneously abducing a path condition as per the I F -A BD
ously issued constraints (for a fresh P , L[P ] is initialized           rule. If the resulting condition ψ is trivially true, the algorithm
with ∅). Horn uses an iterative greatest-fixpoint computation,           has found a solution; if ψ is inconsistent, the E-term is dis-
outlined in Fig. 6; in every iteration, Strengthen(L, ψ ⇒                carded; otherwise, the algorithm generates a conditional and
ψ 0 ) produces the weakest consistent assignment L0 strictly             proceeds to synthesize its remaining branch under the fixed
stronger than L, such that JψKL0 ⇒ Jψ 0 KL is valid (or fails            assumption ¬ψ, as well a term of type {Bool | ν = ψ} to be
if this is not possible). In general, L0 is not unique; in this          used as the branch guard. Once all possible E-terms are ex-
case our algorithm simply explores all alternatives indepen-             hausted, the algorithm attempts to synthesize a pattern match
dently, which happens rarely enough in the context of refine-            using an arbitrary E-term as a scrutinee, unless the maximal
ment type checking and synthesis.                                        nesting depth of matches has been reached.
     Implementing Strengthen efficiently is challenging: for                 Soundness and Completeness. Soundness of synthesis
every unknown P in ψ, the algorithm has to find the small-               follows straightforwardly from soundness of round-trip type
est subset of atomic predicates from QP \ L[P ] that validates           checking, since each program candidate is constructed to-
the implication. Existing greatest-fixpoint Horn solvers [33]            gether with a typing derivation in the round-trip system. Com-
use breadth-first search, which is exponential in the cumula-            pleteness is less obvious: due to condition abduction, the
tive size of QP and does not scale sufficiently well to practical        synthesis procedure only explores programs where the left
cases of condition abduction (see Sec. 4). Instead, we observe           branch of each conditional is an E-term. We can show that
that this task is similar to the problem of finding minimal un-          every S YNQUID program can be rewritten to have this form
satisfiable subsets (MUSs) of a a set of formulas; based on this         (by flattening nested conditionals and pushing conditionals
observation, we build a practical algorithm for Strengthen               inside matches). Thus the synthesis procedure is complete in
which we dub MUSF IX.                                                    the following sense: for each schema S, if there exists a term
     S task of Strengthen amounts to finding all MUSs of the
     The                                                                 t, such that the depth of applications and pattern matches in
set κ∈ψ (Qκ \L[κ])∪{¬Jψ 0 KL } under the assumption JψKL .               t are within the given bounds, the procedure is guarantees to
MUSF IX borrows the main insight of the M ARCO algo-                     find some term t0 that also type-checks against S; if such a
rithm [22] for MUS enumeration, which relies on the ability              term t does not exist, the procedure will terminate with a fail-
of the SMT solver to produce unsatisfiable cores from proofs.            ure. Note that the algorithm imposes no a-priori bound on
We modify M ARCO to only produce MUSs that contain the                   the nesting depth of conditionals (which is crucial for com-
negated right-hand side of the Horn constraint, ¬Jψ 0 KL , since         pleteness as stated above); this does not preclude termination,
Horn should only produce consistent solutions. For each re-              since in any given environment, liquid formulas partition the
sulting MUS (stripped of ¬Jψ 0 KL ), MUSF IX finds all pos-              input space into finitely many parts, and every condition ab-
sible partitions into valuations of individual predicate un-             duction is guaranteed to cover a nonempty subset of these
knowns. Since MUSes are normally much smaller than the                   parts.
original set of formulas, a straightforward partitioning algo-
rithm works well and rarely yield more than one valid par-
tition. As an important optimization, when MUS enumera-
                                                                         4.    Evaluation
tion returns multiple syntactically minimal subsets, MUSF IX             We performed an extensive experimental evaluation of S YN -
                                                                         QUID with the goal of assessing usability and scalability of the


                                                                    12                                                              2016/4/22
   Group           Description            #G                     Components                       #M   Spec   Code   T-all   T-def   T-nrt   T-ncc    T-nmus
                         is empty         1                       true, false                     1     6      6      0.02    0.02    0.02    0.02      0.01
                       is member          1                    true, false, =, 6=                 2      6    18      0.11   0.11     0.13   0.10         -
              duplicate each element      1                                                       1     7     16      0.05   0.05       -     0.08      0.04
                         replicate        1                    0, inc, dec, ≤, 6=                 1      4    21      0.05   0.05     9.63   0.05         -
                  append two lists        1                                                       1     8     15      0.15   0.09       -     0.13      0.10
              concatenate list of lists   1                         append                        3     5     12      0.05   0.05     0.22   0.04       0.04
               take first n elements      1                    0, inc, dec, ≤, 6=                 1      8    27      0.12   0.12    55.82   0.12         -
               drop first n elements      1                    0, inc, dec, ≤, 6=                 1     11    20      0.10   0.10     7.87   0.09         -
                      delete value        1                          =, 6=                        2      8    26      0.10   0.10     0.17   0.12         -
                            map           1                                                       1     5     22      0.03   0.03     0.06   0.03       0.02
   List                     zip           1                                                       1     10    22      0.08   0.08       -     0.10      0.07
                 zip with function        1                                                       1     10    33      0.07   0.07       -     0.17      0.06
                 cartesian product        1                      append, map                      3     8     26      0.30   0.29     5.83   0.25       0.23
                      i-th element        1                    0, inc, dec, ≤, 6=                 1     12    20      0.05   0.05     0.38   0.05         -
                  index of element        1                    0, inc, dec, =, 6=                 2      8    20      0.08   0.08     0.14   0.07         -
                      insert at end       1                                                       2     21    19      0.10   0.10     0.24   0.11       0.12
                          reverse         1                      insert at end                    2    15     12      0.09   0.10     0.29   0.12       0.09
                           foldr          1                                                       2     14    32      0.10   0.10       -     0.10      0.44
                 length using fold        1                       0, inc, dec                     2     4     17      0.03   0.07     0.03   0.03       0.02
                 append using fold        1                                                       2     8     20      0.04   2.19     0.05   0.04       0.03
                           insert         1                          =, 6=                        2      8    26      0.27   0.22     0.85   0.20         -
                           delete         1                          =, 6=                        2      8    22      0.18   0.19     1.07   0.26         -
 Unique         remove duplicates         2                       is member                       2     13    47      0.36   0.87     0.72   0.33         -
  list        remove adjacent dupl.       1                          =, 6=                        3      5    32      1.33   1.32       -     1.31        -
                     integer range        1                   0, inc, dec, ≤, 6=                  2     13    23      2.36   2.33    22.27   2.33         -
                           insert         1                            <                          2      8    41      0.18   0.17     0.43   0.16         -
 Strictly                  delete         1                            <                          2      8    29      0.10   0.09     0.21   0.10         -
sorted list              intersect        1                            <                          2      8    40      0.33   0.32     0.68   0.34         -
                    insert (sorted)       1                          ≤, 6=                        2      8    34      0.25   0.24     0.68   0.23         -
                     insertion sort       1                    insert (sorted)                    4     5     12      0.06   0.06     0.20   0.06       0.05
                   sort by folding        1                      foldr, ≤, 6=                     2     11    47      2.14      -       -     2.21        -
                 extract minimum          1                          ≤, 6=                        4     23    40      4.28   4.35       -     7.58        -
                    selection sort        1                   extract minimum                     6     5     16      0.49   0.44       -     0.42      0.38
 Sorting            balanced split        1                                                       4     31    33      0.96   0.51       -     1.40      0.80
                           merge          1                         ≤, 6=                         2     17    41      2.19   14.61      -     6.85        -
                       merge sort         1                      split, merge                     6     11    25      2.10   2.10       -     2.52      1.69
                         partition        1                            ≤                          4     27    40      2.84   7.89       -     3.42        -
                append with pivot         1                                                       2     28    22      0.22   0.15     0.58   0.22       0.19
                        quick sort        1                 partition, append w/pivot             6    11     22      2.71   18.45      -     2.49      4.94
                       is member          1                      false, not, or, =                2      6    28      0.29   0.29     7.90   0.28         -
                       node count         1                           0, 1, +                     1     4     18      0.20   0.20       -     0.91      0.14
  Tree                   preorder         1                           append                      2     5     18      0.21   0.20       -     0.91      0.15
                   create balanced        1                     0, inc, dec, ≤, 6=                2      7    29      0.14   0.15       -     0.21        -
                       is member          1                     true, false, ≤, 6=                2      6    37      0.09   0.08     0.10   0.08         -
                           insert         1                            ≤, 6=                      2      8    55      0.91   0.88       -     0.82        -
  BST                      delete         1                            ≤, 6=                      2      8    68      5.68   5.62       -    10.74        -
                        BST sort          5                            ≤, 6=                      6     51    115     1.38    1.35      -     1.25        -
                       is member          1                    false, not, or, ≤, 6=              2      6    43      0.38   0.38     9.63   0.35         -
                           insert         1                            ≤, 6=                      2      8    55      0.51   0.50     8.83   0.48         -
 Binary
              1-element constructor       1                            ≤, 6=                      2      5     8      0.02    0.02    0.02    0.02      0.02
 Heap
              2-element constructor       1                            ≤, 6=                      2      6    55      0.08   0.08     0.25   0.07         -
              3-element constructor       1                            ≤, 6=                      2      7    246     2.10    2.12      -     1.98        -
                        rotate left       3                             inc                       3    104    91     11.08   12.43      -    17.06     10.08
                       rotate right       3                             inc                       3    107    91     19.23   18.34      -    36.35     17.87
                          balance         1    rotate, nodeHeight, isSkewed, isLHeavy, isRHeavy   4    31     119     1.56      -       -     1.76        -
  AVL                      insert         1                         balance, <                    3     22    47      1.84   1.81       -     1.64        -
                 extract minimum          1                              <                        5     11    25      1.92   1.87       -     1.72        -
                           delete         2               extract minimum, balance, <             5     37    63     15.67      -       -    13.79        -
                      balance left        2                                                       9    143    137     5.62    5.53      -    48.47        -
  RBT                balance right        2                                                       9    144    137     7.63    7.72      -    45.32        -
                           insert         3                balance left, right, ≤, 6=             9     49    112     8.95    8.53      -     7.93        -
                     desugar AST          1                         0, 1, 2                       4     5     46      1.17   1.10       -     1.23      0.78
  User          make address book         1                       is private                      3     5     35      0.62   3.67       -     0.94      0.55
               merge address books        1                        append                         3     8     19      0.35   5.85       -     0.31      0.24


Table 1. Benchmarks and S YNQUID results. For each benchmark, we report the number of synthesis goals #G; the set of
provided Components; the number of defined measures #M; cumulative size of Specification and synthesized Code (in AST
nodes) for all goals; as well as S YNQUID running times (in seconds) with minimal bounds (T-all), with default bounds (T-def ),
without round-trip checking (T-nrt), without type consistency checking (T-ncc), and without MUSF IX (T-nmus). “-” denotes
timeout of 2 minutes or out of memory.




                                                                                        13                                                           2016/4/22
proposed synthesis technique compared to existing alterna-               helper functions) serves as a synthesis goal in another bench-
tives. This goal materializes into the following research ques-          mark; refinements in datatype definitions are also excluded,
tions:                                                                   since those definitions are reusable between all benchmarks
                                                                         in the same problem domain. Full specifications are available
(1) Are refinement types supported by S YNQUID expressive
                                                                         from the S YNQUID repository [31].
    enough to specify interesting programs, including bench-
                                                                             The benchmarks are drawn from a variety of problem do-
    marks proposed in prior work?
                                                                         mains with the goal of exercising different features in S YN -
(2) How concise are S YNQUID’s input specifications com-                 QUID . List and tree benchmarks demonstrate pattern match-
    pared both to the synthesized solutions and to inputs re-            ing, structural recursion, the ability to generate and use poly-
    quired by existing techniques?                                       morphic and higher-order functions (such as map and fold),
(3) Are S YNQUID’s inputs intuitive: in particular, is the algo-         as well as reasoning about nontrivial properties of data struc-
    rithm applicable to specifications not tailored for synthe-          tures, both universal (e.g. all elements are non-negative) and
    sis?                                                                 recursive (e.g. size and set of elements). Our most advanced
                                                                         benchmarks include sorting and operations over data struc-
(4) How scalable is S YNQUID: can it handle benchmarks
                                                                         tures with complex representation invariants, such as binary
    tackled by existing synthesizers? Can it scale to more
                                                                         search trees, heaps, and balanced trees. These benchmarks
    complex programs than those previously reported in the
                                                                         showcase expressiveness of refinement types, exercise S YN -
    literature?
                                                                         QUID ’s ability to perform nontrivial reasoning through re-
(5) How is synthesis performance impacted by various fea-                finement discovery, and represent a scalability challenge be-
    tures of S YNQUID and its type system?                               yond the current state of the art in synthesis. Finally, we in-
                                                                         cluded several benchmarks operating on “custom” datatypes
4.1   Benchmarks
                                                                         (including the “address book” case study from [20]) in order
In order to answer the research questions stated above, we               to demonstrate that S YNQUID’s applicability is not limited to
arranged a benchmark suite that consists of 64 synthesis chal-           standard textbook examples.
lenges from various sources, representing a range of problem
domains. In the interest of direct comparison with existing              4.2   Results
synthesis tools, our suite includes benchmarks that had been             Evaluation results are summarized in Tab. 1. S YNQUID was
used in the evaluation of those tools [1, 4, 12, 14, 20, 21, 24,         able to synthesize (and fully verify) solutions for all 64 bench-
27]. From each of these papers, we picked top three most com-            marks; the table lists sizes of these solutions in AST nodes
plex challenges (judging by the reported synthesis times) that           (Code) as well as synthesis times in seconds (T-all).
were expressible in S YNQUID’s refinement logic, plus several                The results demonstrate that S YNQUID is efficient in syn-
easier problems that were common or particularly interesting.            thesizing a variety of programs: all but 7 benchmarks are syn-
    Our second source of benchmarks are verification case                thesized within 5 seconds; it also scales to programs of non-
studies from the LiquidHaskell tutorial [18]. The purpose                trivial size, including complex recursive (red-black tree in-
of this second category is two-fold: first, these problems are           sertion of size 69) and non-recursive functions (3-value bi-
larger and more complex than existing synthesis benchmarks,              nary heap constructor of size 246). Even though specification
and thus can show whether S YNQUID goes beyond the state of              sizes for some benchmarks are comparable with the size of the
the art in synthesis; second, the specifications for these prob-         synthesized code, for many complex problems the benefits of
lems have been written by independent researchers and for a              describing computations as refinement types are significant:
different purpose, and thus can serve as evidence that input ac-         for example, the type-based specifications of the three main
cepted by S YNQUID is sufficiently general and intuitive. Out            operations on binary-search trees are over six times more con-
of the total of 14 case studies, we picked 5 that came with suf-         cise than their implementations.
ficiently strong functional specifications (list sorting, binary-            The synthesis times discussed above were obtained for op-
search trees, content-aware lists, unique lists, and AVL trees),         timal exploration bounds, which could differ across bench-
erased all implementations, and made relatively straightfor-             marks. Tab. 1 also reports synthesis times T-def for a setting
ward syntactic changes in order to obtain valid S YNQUID in-             where all benchmarks in the same category share the same ex-
put.                                                                     ploration bounds. Although this inevitably slows down syn-
    Tab. 1 lists the 64 benchmarks together with some met-               thesis, on most of the benchmarks the performance penalties
rics of our type-based specifications: the number of synthe-             were not drastic: only three benchmarks failed to terminate
sis goals including auxiliary functions, the set of components           within the two-minute timeout.
provided, the number of measures used, and the cumulative                    In order to assess the impact on performance of vari-
size of refinements. Note that the reported specification size           ous aspects of our algorithm and implementation, Tab. 1
only includes refinements in the signatures of the synthesis             reports synthesis times using three variants of S YNQUID,
goals; refinements in component functions are excluded since             where certain features were disabled: the column T-nrt cor-
every such function (except trivial arithmetic operations and            responds to replacing round-trip type checking with bidirec-


                                                                    14                                                            2016/4/22
                 Benchmark            Spec   SpecS   Time     TimeS           hardly be explained by improvements in single-core hardware
          strict sorted list delete    14      8      15.1     0.10           performance.
L EON



          strict sorted list insert    14      8      14.1     0.18               We split the tools into two categories according to the
                  merge sort            9     11      14.3      2.1           specification and verification mechanism they rely on.
                   BST find            51      6      64.8     0.09               Formal Specifications with Deductive Verification. The
J EN




            bin. heap 1-element        80      5      61.6     0.02           first category includes L EON [20] and J ENNISYS [21]; both
                bin. heap find         76      6      51.9     0.38           tools use pre- and post-conditions (and data structure in-
              sorted list insert       12      8      0.12     0.25           variants) to describe computations, and rely on unbounded,
M YTH




           list rm adjacent dupl.      13      5      0.07     1.33           SMT-based verification to validate candidate programs (and
                  BST insert           20      8      0.37     0.91           thus provide the same correctness guarantees as S YNQUID).
          list remove duplicates        7     13      231      0.36           Unlike L EON and S YNQUID, J ENNISYS targets imperative,
                                                                              heap-based programs; the evaluation in [21], however, fo-
λ2




                   list drop            6     11     316.4      0.1
                   tree find           12      6       4.7     0.29           cuses on side-effect free benchmarks. Both tools use variants
           list rm adjacent dupl.      n/a     5        1      1.33           of condition abduction, which makes their exploration strate-
E SC




            tree create balanced       n/a     7      0.24     0.14           gies similar to S YNQUID’s.
             list duplicate each       n/a     7      0.16     0.05               For both tools, translating their three most complex bench-
                                                                              marks into S YNQUID proved to be straightforward. This sug-
M YTH 2




                  BST insert           n/a     8      1.81     0.91
              sorted list insert       n/a     8      1.02     0.25           gests that our decidable refinement logic is not too limiting
              tree count nodes         n/a     4      0.45     0.20           in practice, compared to other formal specification languages
                                                                              used for synthesis. Our specifications are on average slightly
Table 2. Comparison to other synthesizers. For each benchmark                 more concise than L EON’s and significantly more concise
we report: Spec, specification size (or the number of input-output ex-        than those in J ENNISYS; the latter is largely due to the heap-
amples) for respective tool; SpecS, specification size for S YNQUID           based language, but the results still indicate that embedding
(from Tab. 1); Time, reported running time for respective tool; TimeS,        predicates into types can help curb the verboseness of tradi-
running time for S YNQUID (from Tab. 1).                                      tional Hoare-style specifications.
                                                                                  S YNQUID was able to synthesize solutions to all problems
                                                                              tackled by the other two tools in this category. The converse is
tional type checking (that is, disabling subtyping checks for                 not true: automatic verification of some of S YNQUID’s bench-
partial applications); T-ncc corresponds to disabling type con-               marks (such as the binary-search tree example in Sec. 2)
sistency checks; T-nmus corresponds to replacing MUSF IX                      requires invariant discovery, which is not supported by the
with naive breadth-first search. The results demonstrate that                 other two tools. This suggests that S YNQUID qualitatively
the most significant contribution comes from using MUS-                       differs from other state-of-the-art synthesizers in terms of the
F IX: without this feature 37 out of 64 benchmarks time out,                  class of programs for which a verified solution can be syn-
since breadth-first search cannot handle condition abduction                  thesized. On the benchmarks where the other tools are appli-
even with a moderate number of logical qualifiers. The sec-                   cable, S YNQUID demonstrates considerably smaller running
ond most significant feature is round-trip type checking, with                times, which suggests that fast verification and early prun-
33 benchmarks timing out when disabled, while consistency                     ing enabled by type-based specifications indeed improve the
checks only bring significant speedups for the most complex                   scalability of synthesis.
examples.                                                                         Input/Output Examples. Our second category of tools in-
                                                                              cludes M YTH [27], λ2 [12] and E SCHER [1], which synthe-
                                                                              size programs from concrete input-output examples, as well
4.3       Comparative Evaluation
                                                                              as M YTH 2 [14], which uses generalized input-output exam-
We compared S YNQUID with state-of-the-art synthesis tools                    ples. Using refinement types, we were able to express 3 out of
that target recursive functional programs and offer a compara-                3, 10, 5, and 7 of their most complex benchmarks, receptively.
ble level of automation. The results are summarized in Tab. 2.                The functions we failed to specify either manipulate nested
For each tool, we list the three most complex benchmarks re-                  structures in a representation-specific way (such as “insert
ported in the respective paper that were expressible in S YN -                a tree under each leaf of another tree”), or perform filtering
QUID ’s refinement logic; for each of the three benchmarks we                 (“list of nodes in a tree that match a predicate”).
report the specification size (if available) and the synthesis                    At the same time, we found cases where refinement types
time; for ease of comparison, we repeat the same two met-                     are concise and intuitive, while providing input-output ex-
rics for S YNQUID (copied over from Tab. 1). Note that the                    amples is extremely tedious. One of those cases is insertion
synthesis times are not directly comparable, since the results                into a binary search tree: M YTH requires 20 examples, each
for other tools are taken from respective papers and were ob-                 of which contains two bulky tree instances and has to de-
tained on different hardware; however, the differences of an                  fine the precise position where the new element is to be in-
order of magnitude or more are still significant, since they can


                                                                         15                                                           2016/4/22
                                                 maxn                                                      array searchn
                          103                                                        103
                                eSolver                                                    eSolver

                          102                           Alloy*                       102                                            Alloy*


                          101                                    Synquid
             Time (s )



                                                                                     101
                                                                                                                                  Synquid

                          100                                                        100

                         10−1                                     Puffin         10−1                                                Puffin


                          n =   2         3       4         5         6              n =    2          3           4          5          6

                                              Figure 7. Evaluation on non-recursive benchmarks.


serted; the type-based specification for this problem, given                    A LLOY * [24], and P UFFIN [4], a specialized synthesizer
in Sec. 2, is straightforward and only defines the abstract ef-                 for conditional integer-arithmetic expressions6 . The results
fect of the operation relevant to the user. This suggests that in               show that S YNQUID’s condition abduction scales relatively
general, logic-based specification techniques, including re-                    well compared to general synthesizers, but loses to P UFFIN’s
finement types in S YNQUID, are a better fit for describing                     theory-specific abduction engine.
operations that maintain a complex representation invariant
but have a simple abstract effect, while example-based ap-                      5.     Related Work
proaches fare better when describing operations that inher-
ently expose the complex representation of a data structure.                    Our work is the first to leverage general decidable refinement
    Experiments with example-based tools only report the                        types for synthesis, but it builds on a number of ideas from
number of examples required for synthesis and not their sizes;                  prior work as has been highlighted already throughout the
however, we can safely assume that each example contains                        paper. Specifically, our work combines ideas from two areas:
multiple AST nodes, and thus conclude that type-based spec-                     synthesis of recursive functional programs and refinement
ifications for the benchmarks in Tab. 2 are more concise. By                    type inference.
imposing more constraints on the set of examples (such as                          Synthesis of Recursive Functional Programs. A num-
trace completeness [27]) and increasing its size, example-                      ber of recent systems target recursive functional programs
based synthesizers can trade off user effort for synthesis time.                and use type information in some form to restrict the search
On the benchmarks under comparison, M YTH appears to                            space. The most closely related to our work are M YTH [27],
favor performance, while λ2 prefers smaller example sets.                       M YTH 2 [14], and L EON [20].
S YNQUID tries to offer the best of both world and achieves                         M YTH pioneered the idea of leveraging bidirectional type
good performance with concise specifications.                                   checking for synthesis. However, M YTH does not support
                                                                                polymorphism or refinement types. Instead, the system relies
                                                                                on examples in order to specify the desired functionality. For
4.4   Evaluation on Non-recursive Benchmarks
                                                                                certain functions, providing examples is easy whereas writing
In order to asses the scalability of MUSF IX on larger search                   a refinement type is cumbersome or, due to the limitations of
spaces, we evaluated S YNQUID on two parametrized bench-                        decidable refinement logic, even impossible. That said, exam-
marks from the linear integer arithmetic track of the Sy-                       ples in general do not fully specify a program; thus program-
GuS’14 competition [3]: maxn (find maximum of n integer                         ming by example always involves a manual verification step.
arguments) and array_searchn (find the position of a value                      Moreover, for some less intuitive problems, such as insertion
in a sorted array with n elements). Both benchmarks target                      into a balanced tree or AST transformations, providing input-
non-recursive programs that consist of a series of nested con-                  output examples requires familiarity with all details and cor-
ditionals; moreover, the search space for the branch guards                     ner cases of the algorithm, whereas refinement types enable a
grows exponentially with n. This makes the two problems                         more abstract specification. Additionally, M YTH expects the
ideal benchmarks for condition abduction techniques.                            set of examples to be trace complete, which means that for
    Fig. 7 shows S YNQUID synthesis times on the two bench-                     any example the user provides, there should also be examples
marks for n = 2, 3, . . . , 6. For reference, we also plot the
results for the enumerative solver (the fastest of the Sy-                      6 The results for these tools are taken from their respective papers; only

GuS baseline solvers), as well as the higher-order solver                       differences in the order of magnitude are significant.


                                                                           16                                                                    2016/4/22
corresponding to any recursive calls made on that input. Other           gram synthesis [4, 20, 21]. Abduction techniques based on
systems that use a combination of types and input-output ex-             quantifier elimination [2, 10] and theory-specific unification
amples, and thus have similar advantages and disadvantages               operators [4], are precise and efficient, but only applicable
relative to our system, include λ2 [12] and E SCHER [1].                 to restricted domains. S YNQUID performs abduction using
    M YTH 2 generalizes example-based synthesis: it treats ex-           predicate abstraction and MUS enumeration, which can be
amples as singleton types, and extends the input language                applied to a wider range of specification logics, but its preci-
with intersection and union types, as well as parametric poly-           sion is limited to the given set of logical qualifiers.
morphism. This addresses some of the shortcomings of con-
crete input-output examples (in particular, their verboseness),          Acknowledgements
however, in the absence of dependent function types most in-             We thank Aleksandar Milicevic, Shachar Itzhaky, Ranjit
teresting programs still cannot be fully speficied. Combin-              Jhala, and the anonymous reviewers for their valuable input.
ing S YNQUID’s dependent types with singletons, intersec-                This work was funded by DARPA Grant FA8750-14-2-0242
tion, and unions found in M YTH 2 is an interesting direction            (MUSE) and NSF Grants CCF-1139056 and CCF-1438969.
for future work.
    In L EON, synthesis problems are defined by first-order              References
specifications with recursive predicates, and verification is             [1] A. Albarghouthi, S. Gulwani, and Z. Kincaid. Recursive pro-
based on a semi-decision procedure [34], implemented on                       gram synthesis. In CAV, 2013.
top of an SMT solver. L EON’s verification engine does not
                                                                          [2] A. Albarghouthi, I. Dillig, and A. Gurfinkel. Maximal specifi-
support invariant inference, which prevents it from generat-                  cation synthesis. In POPL, 2016.
ing provably correct implementations for problems such as
                                                                          [3] R. Alur, R. Bodík, G. Juniwal, M. M. K. Martin,
insertion into a sorted list or a binary search tree. The general
                                                                              M. Raghothaman, S. A. Seshia, R. Singh, A. Solar-Lezama,
synthesis strategy is similar to ours: first decompose the spec-              E. Torlak, and A. Udupa. Syntax-guided synthesis. In FM-
ification and then switch to generate-and-check mode, en-                     CAD, 2013.
hanced with condition abduction. Unlike our system, L EON
                                                                          [4] R. Alur, P. Černý, and A. Radhakrishna. Synthesis through
does not perform systematic specification decomposition in                    unification. In CAV, 2015.
the generate-and-check mode, and lacks support for polymor-
                                                                          [5] L. Augustsson. djinn, the official Haskell package webpage.
phism and high-order functions.
                                                                              http://hackage.haskell.org/package/djinn, 2014.
    The use of type information has also proved extremely
                                                                          [6] E. Brady. Idris, a general-purpose dependently typed program-
useful for code completion [15, 23, 28], although none of
                                                                              ming language: Design and implementation. J. Funct. Pro-
these systems rely on a type system as expressive as ours,
                                                                              gram., 23(5):552–593, 2013.
and they are designed for a very different set of tradeoffs
                                                                          [7] K. Claessen, M. Johansson, D. Rosén, and N. Smallbone. Hip-
compared to S YNQUID. For example, because the problem
                                                                              spec: Automating inductive proofs of program properties. In
is highly under-constrained, these systems place significant
                                                                              ATx/WInG, 2012.
emphasis on the ranking of solutions.
                                                                          [8] T. Coquand. An algorithm for type-checking dependent types.
    Another important body of related work related is hole
                                                                              Sci. Comput. Program., 26(1-3):167–177, 1996.
driven development, as embodied in systems like Agda [26]
and Idris [6], which leverage a rich type system to aid devel-            [9] R. Davies and F. Pfenning. Intersection types and computa-
                                                                              tional effects. In ICFP, 2000.
opment, but are meant to be used interactively rather than to
perform complete synthesis. Djinn [5] serves a similar pur-              [10] I. Dillig, T. Dillig, B. Li, and K. L. McMillan. Inductive
pose but uses the less expressive Haskell type system.                        invariant generation via abductive inference. In OOPSLA,
                                                                              2013.
    Refinement Type Checking. Our type checking algorithm
is based on liquid type inference [19, 32, 35–37], which pi-             [11] J. Dunfield and F. Pfenning. Tridirectional typechecking. In
oneered combining Hindley-Miler unification with predicate                    POPL, 2004.
abstraction. We integrate their ideas with bidirectional type            [12] J. K. Feser, S. Chaudhuri, and I. Dillig. Synthesizing data struc-
checking [30], which has been used before both for other                      ture transformations from input-output examples. In PLDI,
flavors of refinement types [9, 11, 40] and for unrestricted                  2015.
dependent types [8], but not for general decidable refine-               [13] C. Flanagan. Hybrid type checking. In POPL, 2006.
ment types. Another difference with liquid types is that we              [14] J. Frankle, P. Osera, D. Walker, and S. Zdancewic. Example-
use greatest-fixpoint predicate abstraction procedure inspired                directed synthesis: a type-theoretic interpretation. In POPL,
by [33], and improved using an algorithm for efficient MUS                    2016.
enumeration [22].                                                        [15] T. Gvero, V. Kuncak, I. Kuraj, and R. Piskac. Complete com-
    Logical Abduction. The concept of abduction in logical                    pletion using types and weights. In PLDI, 2013.
reasoning has found numerous applications in programming                 [16] J. Heras, E. Komendantskaya, M. Johansson, and E. Maclean.
languages, including specification inference [2, 10] and pro-                 Proof-pattern recognition and lemma discovery in ACL2. In
                                                                              LPAR, 2013.


                                                                    17                                                                 2016/4/22
[17] J. P. Inala, X. Qiu, B. Lerner, and A. Solar-Lezama. Type              A.    Soundness and Completeness of
     assisted synthesis of recursive transformers on algebraic data               Round-trip Type Checking
     types. CoRR, abs/1507.05527, 2015.
                                                                            We show properties of round-trip type checking (Fig. 4) rel-
[18] R. Jhala, E. Seidel, and N. Vazou. Programming with re-
                                                                            ative to the purely bottom-up liquid type inference (Fig. 8),
     finement types (an introduction to liquidhaskell). https://
     ucsd-progsys.github.io/liquidhaskell-tutorial, 2015.
                                                                            using a bidirectional type checking system (Fig. 9) as an in-
                                                                            termediate step.
[19] M. Kawaguchi, P. M. Rondon, and R. Jhala. Type-based data
     structure verification. In PLDI, 2009.                                 A.1   Soundness of round-trip type checking
[20] E. Kneuss, I. Kuraj, V. Kuncak, and P. Suter. Synthesis modulo         Theorem 1 (Soundness of Round-Trip Type Checking). If
     recursive functions. In OOPSLA, 2013.                                  `Q Γ, Γ `Q S, and Γ `Q t ↓ S, then Γ `Q t :: S 0 and
[21] K. R. M. Leino and A. Milicevic. Program extrapolation with            Γ ` S 0 <: S.
     Jennisys. In OOPSLA, 2012.
                                                                               We prove the theorem in two steps. In step 1, assuming
[22] M. Liffiton, A. Previti, A. Malik, and J. Marques-Silva. Fast,         Γ `Q t ↓ S, we build a derivation of Γ `Q t ↓b S in
     flexible mus enumeration. Constraints, pages 1–28, 2015.               the bidirectional type system given in Fig. 9. The main differ-
[23] D. Mandelin, L. Xu, R. Bodík, and D. Kimelman. Jungloid                ence between the two derivations is that the bidirectional sys-
     mining: Helping to navigate the api jungle. In PLDI, 2005.             tem performs a subtyping check on the boundary of the two
[24] A. Milicevic, J. P. Near, E. Kang, and D. Jackson. Alloy*: A           directions, while the round-trip system performs subtyping
     general-purpose higher-order relational constraint solver. In          checks more locally. To show that the latter subsumes the for-
     ICSE, 2015.                                                            mer, we prove that whenever the round-trip system concludes
[25] O. Montano-Rivas, R. L. McCasland, L. Dixon, and A. Bundy.             Γ `Q t ↓ T ↑ let C in T 0 , then Γ; C ` T 0 <: T . In step
     Scheme-based theorem discovery and concept invention. Ex-              2, we build a derivation of Γ `Q t :: S 0 from Γ `Q t ↓b S.
     pert Syst. Appl., 39(2):1637–1646, 2012.
                                                                            Lemma 1 (Type Strengthening). If Γ `Q t              ↓    T     ↑
[26] U. Norell. Dependently typed programming in agda. In AFP,              let C in T 0 then Γ; C ` T 0 <: T .
     2009.
[27] P. Osera and S. Zdancewic. Type-and-example-directed pro-              Proof. By induction on the structure of the derivation. Cases
     gram synthesis. In PLDI, 2015.                                         VAR S C, VAR∀, and A PP FO are trivial, since the subtyping
                                                                            check is one of the premises. For A PP HO, from the first
[28] D. Perelman, S. Gulwani, T. Ball, and D. Grossman. Type-
     directed completion of partial expressions. In PLDI, 2012.             premise by induction hypothesis we have Γ; C ` (Tx0 →
                                                                            T 0 ) <: (bot → T ); by definition of function subtyping (<:-
[29] B. C. Pierce. Types and Programming Languages. MIT Press,
                                                                            F UN in Fig. 3) we get Γ; C ` T 0 <: T .
     2002.
[30] B. C. Pierce and D. N. Turner. Local type inference. ACM               Lemma 2 (Round-trip to Bidirectional). If Γ `Q t ↓ S
     Trans. Program. Lang. Syst., 22(1):1–44, 2000.                         then Γ `Q t ↓b S; additionally, if t is an E-term and
[31] N. Polikarpova and I. Kuraj. Synquid code repository. https:           Γ `Q t ↓ T ↑ Tˆ0 , then Γ `Q t ↑b Tˆ0 .
     //bitbucket.org/nadiapolikarpova/synquid/, 2015.
                                                                               Note that there is a one-to-one correspondence between
[32] P. M. Rondon, M. Kawaguchi, and R. Jhala. Liquid types. In
                                                                            the rules of the two systems (given by their names); our
     PLDI, 2008.
                                                                            construction always uses corresponding rules.
[33] S. Srivastava and S. Gulwani. Program verification using
     templates over predicate abstraction. In PLDI, 2009.                   Proof. By induction on the structure of the derivation. Let us
[34] P. Suter, A. S. Köksal, and V. Kuncak. Satisfiability modulo           first assume an E-term e and a derivation of Γ `Q e ↓ T ↑
     recursive programs. In SAS, 2011.                                      Tˆ0 ; we will build a derivation of Γ `Q e ↑b Tˆ0 . Cases VAR S C
[35] N. Vazou, P. M. Rondon, and R. Jhala. Abstract refinement              and VAR∀ are trivial since the bidirectional premises for these
     types. In ESOP, 2013.                                                  rules are a subset of the round-trip premises. Rule A PP HO
                                                                            has the same structure in the two systems, thus we invoke the
[36] N. Vazou, E. L. Seidel, and R. Jhala. Liquidhaskell: experience
     with refinement types in the real world. In Haskell, 2014.             induction hypothesis in a straightforward manner. Finally, in
                                                                            the rule A PP FO, we obtain the first two premises from the
[37] N. Vazou, E. L. Seidel, R. Jhala, D. Vytiniotis, and S. L. P.
                                                                            induction hypothesis; the third premise, Γ; C1 ; C2 ` Tx <:
     Jones. Refinement types for haskell. In ICFP, 2014.
                                                                            {B | ψ}, follows from the round-trip premise Γ; C1 `Q e2 ↓
[38] N. Vazou, A. Bakst, and R. Jhala. Bounded refinement types.            {B | ψ} ↑ let C2 in Tx and Lemma 1.
     In ICFP, 2015.                                                              We are left to deal with the checking rules. For all check-
[39] P. Wadler. Theorems for free! In FPCA, 1989.                           ing rules except IE we can obtain the required bidirectional
[40] H. Xi and F. Pfenning. Dependent types in practical program-           premises in a straightforward manner from the induction hy-
     ming. In POPL, 1999.                                                   pothesis. For IE, we obtain the first premise from the induc-
                                                                            tion hypothesis; the second premise, Γ; C ` T 0 <: T , follows


                                                                       18                                                            2016/4/22
Type Inference (Contextual Types)             Γ `Q e :: T̂                         Type Inference      Γ `Q e ↑b T̂

                               Γ(x) = {B | ψ}                                                                  Γ(x) = {B | ψ}
                    VAR S C                                                                        VAR S C
                            Γ `Q x :: {B | ν = x}                                                           Γ `Q x ↑b {B | ν = x}
                          Γ(x) = ∀αi .T 0   Γ `Q Ti                                                       Γ(x) = ∀αi .T 0  Γ `Q Ti
                  VAR∀                                                                            VAR∀
                              Γ `Q x :: [Ti /α]T 0                                                           Γ `Q x ↑b [Ti /α]T 0
                      Γ `Q e :: let C1 in (x : Tx → T )                                             Γ `Q e1 ↑b let C1 in (x : {B | ψ} → T )
                         Γ; C1 `Q t :: let C2 in Tx0                                                      Γ; C1 `Q e2 ↑b let C2 in Tx
                           Γ; C1 ; C2 ` Tx0 <: Tx                                                         Γ; C1 ; C2 ` Tx <: {B | ψ}
             A PP                                                                         A PP FO
                      Γ `Q e t :: let C1 ; C2 ; x : Tx0 in T                                          Γ `Q e1 e2 ↑b let C1 ; C2 ; x : Tx in T
                                                                                                         Γ `Q e ↑b let C in (Tx → T )
Type Inference (Context-Free Types)             Γ `Q t :: S                                                     Γ; C `Q f ↓b Tx
                                                                                                A PP HO
                                                                                                             Γ `Q e f ↑b let C in T
                 Γ `Q e :: let C in T 0    Γ; C ` T 0 <: T
         S UBT
                                Γ `Q e :: T                                        Type Checking       Γ `Q t ↓b S
                Γ `Q (x : Tx → T )      Γ; x : Tx `Q t :: T
         A BS                                                                                    Γ `Q e ↑b let C in T 0    Γ; C ` T 0 <: T
                       Γ `Q λx.t :: (x : Tx → T )                                           IE
            Γ `Q e :: let C in {Bool | ψ}            Γ `Q T                                                    Γ `Q e ↓b T
         Γ; C; [>/ν]ψ `Q t1 :: T      Γ; C; [⊥/ν]ψ `Q t2 :: T                                            Γ; y : Tx `Q t ↓b [y/x]T
   IF                                                                                             A BS
                    Γ `Q if e then t1 else t2 :: T                                                      Γ `Q λy.t ↓b (x : Tx → T )
                       Γ `Q e :: let C in {D Tk | ψ}                                                  Γ `Q e ↑b let C in {Bool | ψ}
                  j
           Ci = Ti → {D Tk | ψi }
                                  0
                                         Γi = {xji : Tij }; [x0 /ν]ψi0                    Γ; C; [>/ν]ψ `Q t1 ↓b T       Γ; C; [⊥/ν]ψ `Q t2 ↓b T
                                                                                     IF
               Γ `Q T             Γ; C; [x0 /ν]ψ; Γi `Q ti :: T                                       Γ `Q if e then t1 else t2 ↓b T
M ATCH
                      Γ `Q match e with |i Ci hxji i 7→ ti :: T                                         Γ `Q e ↑b let C in {D Tk | ψ}
                                                                                                    j
                        Γ `Q t :: T    αi not free in Γ                                      Ci = Ti → {D Tk | ψi }
                                                                                                                   0
                                                                                                                          Γi = {xji : Tij }; [x0 /ν]ψi0
                 TA BS                                                                                           0
                              Γ `Q t :: ∀αi .T                                                           Γ; C; [x /ν]ψ; Γi `Q ti ↓b T
                                                                                   M ATCH
                        Γ `Q S     Γ; x : S `Q t :: S                                                Γ `Q match e with |i Ci hxji i 7→ ti ↓b T
                  F IX
                             Γ `Q fix x.t :: S                                                          Γ `Q t ↓b T     αi not free in Γ
                                                                                                 TA BS
                                                                                                              Γ `Q t ↓b ∀αi .T
            Figure 8. Rules of liquid type inference.                                                       Γ; x : S ≺ `Q t ↓b S
                                                                                                       F IX
                                                                                                             Γ `Q fix x.t ↓b S

from the round-trip premise Γ `Q e ↓ T ↑                       let C in T 0
and Lemma 1.                                                                              Figure 9. Rules of bidirectional type checking.

Lemma 3 (Bidirectional to Bottom-up). If `Q Γ, Γ `Q S,
                                                                                   derivation of Γ `Q λx.t ↓b (x : Tx → T ), we construct
and Γ `Q t ↓b S, then Γ `Q t :: S 0 and Γ ` S 0 <: S;
                                                                                   the derivation of Γ `Q λx.t :: (x : Tx → T ) (i.e. we
additionally if t is an E-term and Γ `Q t ↑b T̂ then Γ `Q t ::
                                                                                   pick the bidirectional goal type as the inferred type); this is
T̂ .
                                                                                   possible since by the assumptions of the lemma the type is
Proof. By induction on the structure of the derivation. Let us                     liquid: Γ `Q x : Tx → T , which satisfies the first premise
first assume an E-term e and a derivation of Γ `Q e ↑b T̂ ; we                     of the bottom-up rule. To satisfy the second premise, from
                                                                                   the induction hypothesis we infer Γ; x : Tx `Q t :: T 0 ,
will build a derivation of Γ `Q e :: T̂ . Cases VAR S C, VAR∀,
                                                                                   where Γ; x : Tx ` T 0 <: T , and then using the S UBT
and A PP FO are trivial (in the latter case, A PP FO is replaced
                                                                                   rule we get Γ; x : Tx `Q t :: T . To apply the induction
by A PP). For the A PP HO case, we also construct a derivation
                                                                                   hypothesis, we need to show that T is liquid, which follows
using A PP as the root; from the second premise of A PP HO,
                                                                                   from the assumption that x : Tx → T is liquid and the
Γ; C `Q f ↓b Tx , by induction hypothesis we obtain Tx0 such
                                                                                   definition of liquid function types. The cases I F, M ATCH,
that Γ; C `Q f :: Tx0 and Γ; C ` Tx0 <: Tx . Thus, we obtain
                                                                                   TA BS are analogous to A BS. For F IX we additionally rely
the two missing premises of A PP (with C2 empty). Note that
                                                                                   on the fact that Γ ` S <: S ≺ ; this follows from the definition
to apply the induction hypothesis, we need to show that the
                                                                                   of termination weakening, which only adds refinements to
argument type Tx is liquid (Γ `Q Tx ); this follows from the
                                                                                   preconditions inside S.
assumption `Q Γ (since Tx is a precondition of a function
from Γ).
    For rule IE it is straightforward to obtain the inferred type                  Proof of Theorem 1. Straightforward by combining Lemma 2
T 0 from the induction hypothesis. For rule A BS, from the                         and Lemma 3.


                                                                              19                                                                 2016/4/22
A.2   Completeness of round-trip type checking                          e ↑b let C in T , Γ ` U , and Γ; C ` T <: U ; we will build
As noted in Sec. 3.3, we show completeness for a termination-           a derivation of Γ `Q e ↓ U ↑ let C in T . Cases VAR S C
oblivious variant of the round-trip system, obtained from               and VAR∀ are trivial.
Fig. 4 by replacing S ≺ in the premise of the F IX rule by S.               Consider the rule A PP FO: to get the first premise of the
We denote the checking judgment of the modified system as               round-trip version, we apply the induction hypothesis, pick-
Γ `∗Q t ↓ S.                                                            ing {B | ⊥} → U as the goal; it is easy to show that this type
                                                                        is well-formed in Γ (since so is U ); the challenging part is to
Theorem 2 (Completeness of round-trip type checking). If                show Γ; C1 ` (x : {B | ψ} → T ) <: (x : {B | ⊥} → U ).
Γ `Q t :: S, then Γ `∗Q t ↓ S.                                          By the definition of function subtyping, this simplifies to
   Like in the case of soundness, we do the proof in two                Γ; C1 ` {B | ⊥} <: {B | ψ} (trivial), and Γ; C1 ; x :
steps. We first go from a bottom-up derivation to a bidirec-            {B | ⊥} ` T <: U . We know by the assumption the lemma
tional derivation, essentially by replacing all inference judg-         makes about U that Γ; C1 ; C2 ; x : Tx ` T <: U , so the
ments for I-terms with checking judgments. Going from a                 only thing left to show is that JΓ; C1 ; x : {B | ⊥}KT <:U ⇒
bidirectional derivation to a round-trip one is more com-               JΓ; C1 ; C2 ; x : Tx KT <:U (note that C2 only contains bindings
plex: it amounts to proving that the “early” checks of the              for variables that appear inside Tx and nowhere else). We con-
round-trip system—that is, subtyping checks on incomplete               sider two cases: if x does not actually appear in T , then both
applications—only reject terms that would be later rejected             formulas above are equivalent to JΓ; C1 KT <:U , and thus the
by the bidirectional IE rule.                                           implication holds; otherwise, one of the conjuncts in the left-
                                                                        hand side is ⊥, and thus the implication also holds.
Lemma 4 (Bottom-up to Bidirectional). If Γ `Q t :: S, then                  To get the second second premise of A PP FO, we pick
Γ `∗Q t ↓b S; additionally if t is an E-term and Γ `Q t :: T̂ ,         {B | ψ} (the precondition from the inferred type of e1 ) as
then Γ `∗Q t ↑b T̂ .                                                    the goal. It is easy to show that this type is well-formed in
Proof. By induction on the structure of the derivation. Let us          Γ; C1 ; and moreover Γ; C1 ; C2 ` Tx <: {B | ψ} by the
                                                                        third premise of the bidirectional rule. The third premise of
first assume an E-term e and a derivation of Γ `Q e :: T̂ ;
                                                                        A PP FO follows directly from the lemma’s assumption about
we will build a derivation of Γ `∗Q e ↑b T̂ . Cases VAR S C
                                                                        U.
and VAR∀ are trivial. For A PP, we have to consider two
                                                                            Consider the rule A PP HO. Obtaining its first premise is
cases, depending on whether the argument is an E-term or a
                                                                        similar to the case of A PP FO, except it is easier to show
function term (remember, branching terms are disallowed on
                                                                        that Γ; C ` Tx → T <: bot → U , since these function
right-hand sides of applications). In the former case, we can
                                                                        types are not dependent and thus the above is equivalent to
build a derivation with A PP FO in a straightforward manner.
                                                                        Γ; C ` T <: U (which we get directly from the lemma’s
In the latter case, note that the context C2 has to be empty,
                                                                        assumption about U ). The second premise is obtained directly
because the only rule that could have inferred the type of t is
                                                                        from the induction hypothesis.
A BS, and that rule does not generate contextual types. With
                                                                            For the rule IE, we construct the required premise Γ `Q
that observation, we can build a derivation with A PP HO: we
                                                                        e ↓ T ↑ let C in T 0 from the bidirectional derivation
get Γ; C1 `Q t :: Tx0 and Γ; C1 ` Tx0 <: Tx , yielding
                                                                        for Γ `Q e ↑b let C in T 0 , taking into account that Γ; C `
Γ; C1 `Q t :: Tx by S UBT, which gives us the required
                                                                        T 0 <: T is required by the bidirectional rule, and thus T is a
second premise of A PP HO by the induction hypothesis.
                                                                        valid goal type for the round-trip derivation.
    For all the context-free inference rules, it is straightfor-
                                                                            The rest of the rules are trivial, since they have the same
ward to construct a bidirectional derivation using the corre-
                                                                        shape in both systems; the only two exceptions are the first
sponding checking rule, since the premises of these rules are
                                                                        premises of I F and M ATCH, which require a strengthening
a subset of the premises of their bottom-up counterparts.
                                                                        judgment; in both cases it is straightforward to show that the
Lemma 5 (Bidirectional to Round-Trip). If Γ `Q t ↓b S                   respective goal types (Bool and top) are supertypes of the type
then Γ `Q t ↓ S; additionally if t is an E-term and                     inferred by the bidirectional system.
Γ `Q t ↑b let C in T and there exists a type U such that
Γ ` U and Γ; C ` T <: U then Γ `Q t ↓ U ↑ let C in T .                  Proof of Theorem 2. Straightforward by combining Lemma 4
Proof. By induction on the structure of the derivation. Let             and Lemma 5.
us first assume an E-term e and a type U , such that Γ `Q




                                                                   20                                                           2016/4/22
