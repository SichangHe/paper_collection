                                          Formal Methods in Computer-Aided Design 2026



      DSLean: A Framework for Type-Correct
Interoperability Between Lean 4 and External DSLs
                                Tate Rowney, Riyaz Ahuja, Jeremy Avigad, Sean Welleck
                                       Carnegie Mellon University, Pittsburgh, PA
                                   {trowney, riyaza, avigad, swelleck}@andrew.cmu.edu


   Abstract—Domain-specific languages (DSLs) mediate interac-           We also showcase several applications of DSLean, in the
tions between interactive proof assistants and external automa-      form of Lean automation tactics:
tion, but translating between the prover’s internal representation
                                                                        • The gappa tactic uses DSLean to interface with the
and such DSLs is a tedious engineering chore. To simplify this
task, we present DSLean, a framework for bidirectional transla-           Gappa [6] interval arithmetic solver, automatically prov-
tion between expressions in the Lean proof assistant and external         ing nontrivial bounds on real numbers by translating
syntax. DSLean requires only a specification of an external               Gappa’s proof certificates, emitted in Rocq [31] syntax,
language and its Lean equivalents, abstracting away meta-level            into Lean.
implementation details. We demonstrate DSLean’s capabilities
                                                                        • The desolve tactic connects to the SageMath [32]
by implementing three new automation tactics, providing access
to external solvers for interval arithmetic, ordinary differential        computer algebra system to obtain general solutions to
equations, and ring ideal membership.                                     ordinary differential equations.
                                                                        • The lean_m2 tactic communicates with the Macaulay2
                      I. I NTRODUCTION
                                                                          package [8], providing witnesses to problems involving
   Interactive theorem provers (ITPs) are increasingly used               ring ideal membership and Gröbner bases.
to formally verify claims in mathematics and software. The           Due to DSLean’s capabilities, each example above has a short
process of verification is often assisted by the use of external     and interpretable implementation, using comparatively few
automation, either by reconstructing automatically discovered        lines of code (203 for gappa, 95 for desolve, and 315
proofs within the proof assistant or using them as a trusted         for lean_m2). We believe DSLean’s general nature makes it
oracle. Communication between the ITP and the external               applicable to many forms of proof automation beyond what is
solver is generally mediated by a domain-specific language           presented here.
(DSL) interpretable by both. Examples within Lean 4 [19], a
widely used ITP, include interfacing with external SMT solvers                              II. OVERVIEW
and theorem provers [23], [18], [20], computer algebra systems          We provide a brief overview of the capabilities of DSLean
[3], [14], and specialized tools for program verification [11],      by showcasing a translation between Lean objects and a small
[9] and cryptography [34].                                           fragment of the Python programming language. DSLean is
   Implementing such translations is generally challenging.          used by specifying equivalences between Lean objects and
There is little general infrastructure for exporting such in-        external syntax. These are declared using the external
formation from Lean, so translation often requires the use           keyword, with external syntax on the lefthand side of a <==>
of bespoke intermediate structures. In the other direction,          delimiter and Lean objects on the right, as shown below:
transforming raw serialized data from an external tool into
                                                                     external translate_Python where
Lean expressions requires meta-level code to parse the data            "True" <==> True
into a concrete syntax tree, elaborate it into an abstract syntax      "False" <==> False
tree, and modify or recombine it to form a Lean expression.
This results in application-specific code that is difficult to          Translation into Lean may then be performed using the
maintain and understand, and often requires expertise with           fromExternal function, while the toExternal function
Lean metaprogramming.                                                translates Lean into external syntax (with Lean’s #check
                                                                     command used to show the value and type of these expres-
Contributions. We present DSLean, a framework for bidi-              sions):
rectional translation between Lean 4 and arbitrary domain-           #check fromExternal translate_Python
specific languages. DSLean is implemented fully in Lean using           "True"
its capabilities as a functional programming language, and uses      -- Output: (True : Prop)
Lean’s native parser and metavariable unification algorithm to
allow for robust transformations of type-correct Lean expres-        #check toExternal translate_Python False
                                                                     -- Output: ("False" : String)
sions to well-formed syntax and vice versa. Despite its internal
complexity, DSLean provides a user interface that abstracts            More complicated syntax can be expressed by leaving free
away implementation details such as parsing and elaboration.         variables in both sides: these are iteratively filled in during


                                                                                            This article is licensed under a Creative
                                                                                            Commons Attribution 4.0 International License
translation using the rest of the provided equivalences. For      translation is not reversible due to the absence of the variable
example, the pattern "not" x shown below will translate           b on the righthand side, but functions correctly in the forwards
syntax beginning with "not", then continue to translate the       direction:
remaining syntax corresponding to x (and vice versa):
                                                                  external Python_one_way where
external translate_Python where                                     "(" a "," b ")[0]" ==> a
  ...
  "not" x <==> ¬ x                                                #check fromExternal Python_one_way
                                                                      "(True, False)[0]"
#check fromExternal translate_Python                              -- Output: (True : Prop)
    "not True"
-- Output: (¬True : Prop)
                                                                     Finally, DSLean allows for significant customizability, al-
#check toExternal translate_Python                                lowing for manual changes to the associativity or precedence
    ¬ False                                                       of syntax while automatically determining reasonable values
-- Output: ("not False" : String)                                 when left unspecified. Further documentation on specific con-
                                                                  figuration options may be found accompanying the source
  As DSLean only translates to and from type-correct Lean
                                                                  code.
expressions, the types of the Lean objects in question impose
typing constraints on the external syntax, allowing for repre-                        III. R ELATED W ORK
sentation of complex language specifications. In the previous        Translation between automated theorem provers and
example, "not" x will only be translated if the syntax            domain-specific languages for the purpose of automation is
corresponding to x translates to an object of type Prop.          a highly established paradigm. Programs that use such com-
  DSLean allows specified languages to enjoy levels of poly-      munication to obtain proof certificates are commonplace when
morphism similar to Lean itself. The addition operator is         interfacing with SMT solvers [18], [1] or when creating “ham-
polymorphic in Lean, and thus so is its translated counterpart:   mers” that rely on first-order theorem provers [36], [23], [21],
external translate_Python where                                   [5], [15], [4]. Such programs transform goals in dependent
  ...                                                             type theory into the propositional or first-order logic syntax
  a "+" b <==> a + b                                              usable by the automation they rely on [17]. Additionally,
                                                                  automation that provides witnesses to a statement [30] or
  "int(1)" <==> (1 : Z)
                                                                  relies on the correctness of established computer algebra
  "float(1)" <==> (1 : Float)
                                                                  systems [14], [3] has received growing interest due to ITPs’
#check fromExternal translate_Python                              ability to verify auxiliary reasoning steps performed on such
   "int(1) + int(1)"                                              problems. Finally, many program verification frameworks seek
-- Output: (1 + 1 : Z)                                            to translate syntax of an unverified programming language into
                                                                  a formal specification to allow proofs about its properties [11],
#check fromExternal translate_Python                              [2], [29], [13], [9]. However, translations performed by the
   "float(1) + float(1)"
                                                                  above works are highly domain-specific: particularly within
-- Output: (1 + 1 : Float)
                                                                  the Lean implementations, this results in large amounts of
   DSLean also shares meta-level information across transla-      opaque and non-generalizable meta-level code.
tion such as identifier names, whose correspondence may also         Lean 4 [19] possesses a native foreign function interface,
be specified (as with variableName below). Translated free        as well as an extensible parser and elaborator to define and
variables are transformed into bound variables when inside        implement new syntax [35], similar to that of Rocq [31],
relevant binders.                                                 [7]. However, these provide information at the implementation
                                                                  level, often necessitating manual manipulation of intermedi-
external translate_Python where                                   ate data structures to allow its use in proofs and requiring
  ...                                                             proficiency in Lean’s more obscure implementation details.
  ($variableName) "=" val ";" rest <==>                           Work in progress on SciLean [33] facilitates communication
    let variableName := val; rest
                                                                  between certain forms of Lean objects and external representa-
#check fromExternal translate_Python                              tions; however, it requires manual specification of intermediate
   "myvar = int(1); myvar"                                        structures, and does not implement parsing. Additionally, prior
-- Output: (let myvar := 1; myvar : Int)                          work has implemented translation between Rocq and specific
                                                                  protocols used by computer algebra systems [12]. However,
   As some applications may require translations that are not     to our knowledge DSLean represents the most comprehensive
fully reversible, DSLean allows non-injective equivalences to     attempt to simplify and streamline the process of translation
be specified in only one direction. Should an equivalence not     between an ITP and arbitrary external DSLs.
be fully reversible (as discussed in Section IV-B), DSLean will      Additionally, we believe the example tactics presented here,
detect this and inform the user. For example, the following       while intended as case studies, nonetheless fill niches not occu-
pied by current Lean automation. Interval arithmetic automa-       substituting equivalent expressions, allowing a higher level of
tion in Rocq is highly capable [16], explaining our decision       assurance that this property holds.
to integrate a solver intended for Rocq [6]. However, Lean            Finally, we attempt to make DSLean as simple and intuitive
lacks an equally capable equivalent: aside from the in-progress    as possible for the user, requiring only the minimum amount
lean-cert project [24] which appears to focus primarily            of non-optional configuration and allowing them to disregard
on bounding and root-finding for functions, complicated real-      metaprogramming-related trivialities. Methods of inferring
valued interval problems are not easily solvable by existing       reasonable values for unspecified parameters are described
automation. Work on formalization of differential equations        below.
in Lean is also sparse, with only minor results in Mathlib            The above goals still allow for substantial flexibility in
[30] and partial formalization of some numerical methods in        the types of language features that DSLean is capable of
SciLean [33]; considering this, we believe an oracle-based         encoding, including binders, loops, representations of state via
tactic as showcased here is appropriate, as similar automation     monads, and representations of weakly-typed languages using
has been used in Isabelle/HOL [10]. Finally, we believe            Lean’s coercion-related typeclasses. However, it still contains
the presented automation for proving ring ideal membership         some limitations, including languages whose syntax changes
represents an improvement in capability over Lean’s grind          depending on the semantics of previous expressions, as well
and Mathlib’s polyrith, which do not include capabilities          as those which use indentation to indicate control flow; future
surrounding polynomials over non-standard rings and fields;        work could improve DSLean by allowing these features to be
and an improvement in interpretability over the automation         encoded too.
given in Shen et al. [26], which utilizes thousands of lines of
bespoke meta-level code.                                           B. Translation: Lean to External
                                                                      Translation from Lean objects to external syntax does not
                        IV. DSL EAN                                use Lean’s default pretty-printing system: rather, we opt to
                                                                   recursively check whether a Lean expression is semantically
   We now provide an overview of DSLean’s design and im-           identical to any equivalences to ensure one-to-one correspon-
plementation. DSLean is implemented in Lean and uses Lean’s        dence with external patterns.
metaprogramming APIs to perform translation from Lean ex-             Each user-specified equivalence, written via the syntax
pressions to external syntax (Section IV-B), and from external     ...<==>..., contains an external pattern on the left in
syntax back to Lean (Section IV-C). Translation into external      the form of a sequence of strings and identifiers, and a
syntax proceeds by partially matching a target expression with     Lean pattern on the right via well-formed Lean syntax. A
an expression corresponding to a pattern, recursively repeating    Lean pattern is stored using Lean’s internal representation of
this process until the entire target is matched. Translation       expressions, the Expr type. An external pattern consists of
into Lean begins by parsing a raw input into an intermediate       a sequence of parts, which fall into one of two categories; a
data structure (Section IV-C1). This data structure is then        terminal part can correspond to a literal or the name of a bound
elaborated, or transformed from a representation of the syntax     variable, while a nonterminal part represents a placeholder
into a data structure representing the expression’s semantics,     to be filled by other equivalences. The following example
by recursively combining the expressions corresponding to          demonstrates how these parts are declared:
each detected pattern (Section IV-C2). These processes are
described in detail below.                                         external simpleExample where

                                                                    "terminal_string" <==> 0
A. Design Principles
   DSLean is designed to achieve three goals. First, rather         "other_terminal_string" $terminal_binder
than require the user to specify type- and structure-related          nonterminal <==> (fun terminal_binder
                                                                      => nonterminal)
constraints in the DSL, we instead utilize Lean’s semantics to
impose such structure. The types of Lean objects induce typing        The above DSL will translate the Lean value of
constraints on corresponding external syntax, allowing for         (for    example)     fun my_binder_name => 0             by
more nuanced structural properties than a simple inductively-      matching with the second equivalence, filling in the $
defined specification. Lean allows users to define and use ob-     terminal_binder with the name of the corresponding
jects with a wide variety of useful signatures should available    binder (my_binder_name), and continuing to match
objects be insufficient to induce the desired structure.           whatever corresponds with nonterminal (in this case,
   Second, we strive for round-trip consistency; that is, trans-   the function body 0), obtaining the external representation
lating an expression out of and back into Lean, or vice            "other_terminal_string my_binder_name
versa, should result in the same object modulo semantically        terminal_string". DSLean elaborates the Lean patterns
irrelevant differences in syntax. As DSLean utilizes Lean’s        of each equivalence, turning them from raw syntax into
parser and other unsafe or unverifiable code, we provide no        expressions, at the time that the equivalences are declared
formal guarantee of this property. However, apart from initial     to ensure that terminal binder and nonterminal parts in the
parsing or final serialization, all processing is performed by     external pattern indeed correspond to names of binders and
free variables in the Lean pattern; in the above example, this          declaration of myvar; however, the recursive call on line
would involve ensuring that the binder terminal_binder                  12 of Algorithm 1 will pass the same argument as the
and the free variable nonterminal indeed exist on                       parent call received modulo reductions (as let myvar
both sides. The two sides may have differing numbers of                 := "myval"; nonterminal is semantically equivalent
nonterminals if the equivalence is specified as only translating        to nonterminal when myvar is not used), causing the
in a single direction (declared with . . .==>. . . or . . .<==. . .).   algorithm to not terminate. To avoid this scenario, patterns
                                                                        that may trivially match with anything are checked last, giving
Algorithm 1 Translation of a Lean expression to external                priority to patterns that allow progress towards translation. It
syntax                                                                  may still be the case that expressions that are untranslatable
 1: procedure L EAN T O E XTERNAL(leanExpr )                            by a given DSL will match only with trivial patterns and cause
 2:   out ← “”                                    ▷ Empty string        such a failure of termination; as there is likely no practical way
 3:   for all (externalPattern, leanPattern) ∈ equivalences             to detect this, we simply impose an upper limit on the number
    do                     ▷ sorted so trivial patterns come last       of recursive calls to prevent stack overflow and automatically
 4:     if D EFINITIONALLY E QUAL (leanExpr , leanPattern )             reject such inputs.
    then                                                                   While the core algorithm is simple, DSLean’s implementa-
 5:       for all part ∈ externalPattern do                             tion relies on several additional implementation details. First,
 6:         if part is a terminal string then                           identifiers like free variable names are translated verbatim
 7:           out ← out ++ part                                         without requiring a dedicated equivalence; when a binder is
 8:         else if part is a terminal binder name then                 translated, its corresponding bound variables are converted into
 9:           out ← out ++ B INDER NAME(part, leanExpr )                free variables with the correct name so they can be translated.
10:         else if part is a nonterminal then                          In the above example, an expression such as fun x =>
11:           target ← C ORRESPONDING S UBEXPRESSION (                  x would be translated to "terminal_string x x" in
    part, leanExpr )                                                    this way, matching the second equivalence and filling in the
12:           out ← out ++ L EAN T O E XTERNAL (target )                nonterminal with the name of the (now) free variable x.
13:         end if                                                         Furthermore, additional metavariables that do not corre-
14:       end for                                                       spond to nonterminals may be present in Lean patterns (such
15:       return out                                                    as the unspecified type of the terminal_binder argument
16:     end if                                                          to the Lean function in the example in IV-B above). Since each
17:   end for                                                           Lean pattern is elaborated in a separate context, metavariables
18:   T HROW E RROR(“No patterns matched; expression is not             in that pattern are not necessarily functions of any bound
    translatable”)                                                      variables that may occur in a target expression, which is
19: end procedure                                                       required by Lean’s unification system for said metavariables’
                                                                        value to be dependent on outside binders. To remedy this,
   The high-level algorithm for using a set of equivalences to          should an outside metavariable ?m potentially be unified with
translate a Lean expression into external syntax is outlined            an expression e with bound variables (b1 , ...bn ) in scope, we
in Algorithm 1: it attempts to match a target expression                perform the substitution e[(λx1 . · · · λxn .?m)b1 · · · bn /?m] to
with each equivalence’s Lean pattern using Lean’s definitional          ensure such dependence can occur. We assert that this remains
equality checker, which reliably determines how to unify se-            definitionally equal to the original expression, as unused bound
mantically equivalent expressions despite syntactic differences.        variables disappear from this sub-expression after β-reduction;
To allow this, the variables in a Lean pattern corresponding            thus, these are equivalent when used by Lean’s definitional
to nonterminals are replaced with metavariables, syntactic              equality checker.
placeholders for as-yet undetermined sub-expressions; assert-
ing definitional equality with a target expression will assign          C. Translation: External to Lean
to each metavariable a value among sub-expressions of the                  Translation from external syntax to Lean proceeds in two
target such that the entire pattern matches. This allows easy           steps: parsing (IV-C1) and elaboration (IV-C2); together, these
determination of what sub-expressions in a pattern correspond           create a shallow embedding of the specified syntax into Lean.
to nonterminals and require further processing. Upon finding a             1) Parsing: External syntax is parsed using Lean’s native
definitionally equal Lean pattern, the algorithm loops through          parser [19], a Pratt parser [22] with additional dynamic infor-
each part of the relevant external pattern, filling in the external     mation in the style of Swierstra and Duponcheel’s combinator
representation and using recursive calls to complete translation        parsers [28]. We chose to use it due to its efficient implemen-
of any nonterminals.                                                    tation, its robustness as already demonstrated by the above
   Certain Lean patterns may be general enough such that                literature, and the fact that it was designed with extensibility
they match with nearly any input expression without making              in mind, making it suitable for processing a wide variety of
substantial progress. For example, a Lean pattern such as               reasonably-designed external grammars.
let myvar := "myval"; nonterminal will be def-                             The external syntax portion of each user-specified equiv-
initionally equal to any expression by simply ignoring the              alence is transformed into a single production rule; string
literals and free variables in the specification correspond to        Algorithm 2 Translation of an external syntax tree to a Lean
terminal and nonterminal symbols respectively. For binary op-         expression
erations and production rules with more than one nonterminal           1: procedure E XTERNALT O L EAN (syntaxTree)
in a row (for example, a pattern such as "gcd" a b), the first         2:   (leanPattern, nonterminalTrees, binderNames)        ←
symbol is given higher precedence to avoid potential interfer-            C ORRESPONDING E QUIVALENCE(syntaxTree)
ence with highly generic rules such as function application:           3:   for all placeholderBinder ∈ leanPattern do
we do not wish for "gcd" a b to be interpreted as “gcd                 4:     leanPattern ← R EPLACE B INDER(leanPattern,
of the function a applied to b". This causes operations to                placeholderBinder , binderNames[placeholderBinder ])
be left-associative by default: we believe this is reasonable,         5:   end for
as many of Lean’s standard mathematical operations are left-           6:   for all metavariable ∈ leanPattern do
associative. Users may modify the associativity of a production        7:     if I S N ONTERMINAL(metavariable) then
rule with the +rightAssociative flag, or manually mod-                 8:       nonterminalContents ← E XTERNALT O L EAN (
ify the precedence with the precedence := ... option.                     nonterminalTrees[metavariable])
   Lean’s parser implements optimized parsing of numerals              9:       if      U NIFY(metavariable, nonterminalContents)
via a separate parser category: we retain this behavior for               fails with type mismatch then
performance and convenience, as we believe requiring the              10:          T HROW E RROR(“External syntax is ill-typed;
inductive specification of the definition of base-10 numerals             translation is impossible”)
in every DSL imposes an unnecessary burden on the user. We            11:       end if
also use Lean’s identifier parser at maximum precedence to            12:     end if
parse free variables.                                                 13:   end for
   While powerful, Lean’s parser makes certain assumptions            14:   return leanPattern
about the structure of grammars it parses, causing it to refuse       15: end procedure
certain production rules. These include rules containing certain
reserved terminal symbols such as lone numerals or quotation
marks, as well as identifiers that begin with certain characters
                                                                      and unifies them, assigning the type of the + operation to N
such as punctuation. It is likely that some or all of these
                                                                        → N → N; after the assignments are made, the returned
limitations are caused by certain APIs used to expose them
                                                                      expression becomes the expected 1 + 1 : N.
and not due to limitations of its theoretical foundations. Future
work could address this by modifying or augmenting the parser            During elaboration, bound variables in expressions are
for greater generalizability.                                         temporarily transformed into free variables to allow other
   2) Elaboration: DSLean does not utilize Lean’s default             equivalences to reference outside binders from within their
term elaborator directly, instead creating a custom elaboration       bodies, after which all occurrences of this free variable are
stage built on top of it. Following the structure given by the        turned back into a bound variable. This causes the contexts of
parsed syntax tree, the relevant equivalences’ Lean patterns          some metavariables, which are instantiated before this process,
are merged into a single expression using Lean’s definitional         to become out of date; to remedy this, we manually modify
equality checker.                                                     any metavariable occurring within a binder x to include x in its
   Algorithm 2 describes this process; given a syntax tree            context. Although this could potentially cause another instance
obtained from parsing (see IV-C1), it finds the corresponding         of the metavariable outside this binder to be assigned to a free
Lean pattern and replaces each terminal binder and non-               variable that is not in scope, we assert this transformation is
terminal with, respectively, the proper binder name and a             safe, as such a situation is equivalent to attempting to translate
recursive call to translate the remainder of the syntax. The          an occurrence of a bound variable with no corresponding
result of this recursive call is unified with the parent expression   binder; both situations will be flagged by Lean’s kernel at
using Lean’s definitional equality checker, which automatically       the end as ill-typed expressions.
assigns other metavariables necessary to resolve typing con-             Since Lean’s parser processes numerals as a separate cate-
straints. This process is illustrated in the following DSL:           gory in an optimized fashion (see section IV-C1), elaboration
external simpleExample where                                          of numerals is also handled separately without user specifica-
                                                                      tion. By default, numerals are elaborated into natural numbers
   "one" <==> (1 : N)                                                 (Lean’s Nat type) with coercion applied wherever possible;
                                                                      this behavior may be changed by specifying the numberCast
   x "plus" y <==> x + y                                              option.
Here, the second equivalence contains both metavariables                 Finally, the value of certain expressions such as automation
corresponding to the nonterminals x and y, but also the type          tactics cannot be ascertained until the expression’s type is
of the addition operation (whether it is adding elements of N,        known. Such expressions are treated specially: we disallow
Z, R, etc.). When translating external syntax such as "one            nonterminals, and wait until translation time to elaborate
plus one", the algorithm will use the second equivalence,             them so the rest of the translated expression can be used to
perform recursive calls to resolve both x and y to 1 : N              determine their expected type.
                       V. C ASE S TUDIES                               variety of problems involving these1 that are otherwise diffi-
                                                                       cult or impossible for existing automation. If gappa cannot
   We present three applications of DSLean in the form of              fully solve a problem, it leaves (often substantially simpler)
Lean automation tactics. Each of the examples below utilizes           subgoals for the user to solve, as with the final example above.
an external solver program to search for solutions to a rele-             The tactic supports standard arithmetic operations, logical
vant Lean problem; they were implemented primarily using               connectives, anonymous functions, and local declarations,
DSLean, with some additional Lean scripting to register them           which are similar in both Lean and Rocq. More complex
as tactics. Each tactic requires its relevant solver to be installed   Lean definitions such as closed intervals, set membership, and
to find new proofs; however, proofs do not rely on the solvers         casting natural numbers to reals are equated with the string
once generated, and can be imported and reused by other users          representations of definitions within Gappa’s dedicated Rocq
once built.                                                            library. These equivalences are easy to specify with DSLean:

                                                                       external Gappa_output where
A. gappa                                                                 ...
                                                                         -- logical connectives
  The gappa tactic provides verified Lean proofs of interval
                                                                         x "/\\" y ==> x ∧ y
bounds on real-valued expressions. It uses DSLean to interface           x "\\/" y ==> x ∨ y
with the Gappa interval arithmetic solver [6]; Gappa outputs             "not" x      ==> ¬ x
proof certificates in Rocq [31] syntax, which DSLean treats              ...
as a DSL to translate these certificates into valid Lean terms.          -- Gappa equivalents of real numbers
Some examples of its usage are shown below:                              "Reals.Rdefinitions.R" ==> R
                                                                         "Gappa.Gappa_definitions.Float2" x y ==>
example (x : R) (y : R) :                                                    (IntCast.intCast x : Real) ∗
  x ∈ Set.Icc 0 1 →                                                        ((2:Real) ^ (y:Int))
  y ∈ Set.Icc (-1) 1 →                                                    ...
  2 ∗ x + y ∈ Set.Icc (-1) 3 := by
    gappa                                                                 Translation from Rocq syntax to Lean includes the large
                                                                       amount of Rocq automation used by Gappa: due to their com-
example (y : R) :                                                      paratively narrow scope, we approximately recreate each one
  y ∈ Set.Icc 0 1 →
  y ∗ y ∗ y ∈ Set.Icc 0 1 := by                                        in Lean using relevant simp lemmas and various arithmetic
    gappa                                                              tactics, as with the example below.2 Although nearly all of
                                                                       these goals are relatively simple and can be solved by compu-
example (y : R) :                                                      tationally intensive tactics such as Mathlib’s nlinarith, we
  y ∈ Set.Icc 0 1 →                                                    attempt to close each goal with a variety of simpler heuristics
  y ∗ (1-y) ∈ Set.Icc 0 0.5 := by                                      for efficiency. Any subgoals left unsolved by this automation
    gappa                                                              are left for the user to fill manually.
example (a b c : R) :                                                       ...
  c ∈ Set.Icc (-0.3 : R) (-0.1 : R) ∧                                       -- tactic equivalents
  (2 ∗ a ∈ Set.Icc 3 4 → b + c ∈ Set.Icc                                    "Gappa.Gappa_pred_bnd.constant1" a b c
   1 2) ∧                                                                   ==> by
  a - c ∈ Set.Icc 1.9 2.05 →                                                      dsimp <;> intros <;> norm_num at ∗
  b + 1 ∈ Set.Icc 2 3.5 := by                                                 <;> (try constructor) <;> simp_all <
    gappa                                                                   ;> sorry -- If sorry ends up being
                                                                            used, the goal is left for the user
example (x : R) (y : R) :                                                   to solve instead
  x ∈ Set.Icc 0 1 →                                                         ...
  y ∈ Set.Icc 0 1 →
  x ∗ x ∗ y ∈ Set.Icc 0 1 := by                                          Combined, these rules allow translation of Gappa’s large
    gappa                                                              Rocq proof terms into Lean. Apart from a short macro to clean
                                                                       the syntax and remove comments, this translation is executed
    /- Some goals left to solve:                                       entirely by DSLean. A truncated example below shows a Rocq
left : 0 ≤ x ∧ x ≤ 1                                                   proof certificate emitted from Gappa:
right : (0 ≤ y ∧ y ≤ 1) ∧ (0 ≤ x∗x∗y →
   1 < x∗x∗y)
⊢ False -/
    have := right.2 (by nlinarith)                                       1 We wish to credit Gappa [6] for the fourth problem above; it is a Lean
    nlinarith
                                                                       encoding of an example found therein.
                                                                         2 The example tactic translation presented here is modified slightly from its
   We use Mathlib’s [30] Set.Icc definition to encode closed           appearance in the accompanying implementation, where sequences of tactics
intervals between two real numbers; gappa solves a wide                have been bundled together as macros to improve the code’s readability.
fun (_y : Reals.Rdefinitions.R) =>                                  example : isODEsolution
    let f1 :=                                                         (fun x => fun y => deriv (deriv y) x +
   Gappa.Gappa_definitions.Float2 (0)                                  2 ∗ deriv y x + y x = 0)
   (0) in                                                             (fun _ K1 K2 x => Real.exp (-x) ∗ (K2 ∗
    let f2 :=                                                          x + K1)) := by
   Gappa.Gappa_definitions.Float2 (1)                                 desolve
   (0) in                                                               /- Goals remaining: ⊢ (fun _ K1 K2 x
    ...                                                                => (K1 + K2 ∗ x)) ∗ Real.exp (-x)) =
    let s1 := p1 /\ s2 in                                              fun _ K1 K2 x => Real.exp (-x) ∗ (K2
    ...                                                                ∗ x + K1) -/
    let t1 : p3 :=                                                    funext
   Gappa.Gappa_pred_bnd.constant1 _ i3 _                              rw [mul_comm]
   in
    ...                                                                 This tactic works primarily with the isODEsolution
                                                                    predicate; isODEsolution f g represents the assertions
   This certificate undergoes translation via DSLean into the       that all solutions to y ′ (x) = f (x, y(x)) are of the form g
following Lean proof:                                               modulo up to three constants of integration. For example, the
fun (_y : R) =>                                                     first problem above proves the assertion that all solutions to
    let f1 := (0 : R) ∗ 2 ^ (0 : Z);                                y ′ (x) = 1 are of the form x ↦→ x + C for an arbitrary C ∈ R.
    let f2 := (1 : R) ∗ 2 ^ (0 : Z);                                Once a general solution is obtained, it is instantiated in Lean
    ...                                                             via DSLean as a function of these constants. Should this not be
    let s1 := p1 ∧ s2;
                                                                    equivalent to the purported solution in the theorem statement,
    ...
                                                                    showing their equivalence is left as a goal for the user (as in
      let t1 := (by . . .) : t3;                                    the last example above).
      ...                                                               desolve supports equations constructed from a wide
                                                                    variety of Mathlib’s differentiable real-valued functions, using
   While Gappa is best known for its ability to work with           DSLean to specify their SageMath representations:
floating-point arithmetic, we choose to make use of its capa-
bilities in handling exact interval arithmetic in this case study   external desolve_out where
due to the current lack of developed Lean results concerning           ...
                                                                       "e^(" x ")" <== Real.exp x
floating-point numbers. We emphasize that this does not com-           "sqrt(" x ")" <== Real.sqrt x
promise the soundness of the translated Lean proofs; they do           "sin(" x ")" <== Real.sin x
not rely on outside axioms, preventing concerns about roundoff         "diff(" fn "," var ")" <== deriv fn var
errors and numerical imprecision. We believe DSLean will also          ...
prove useful in creating automation for floating-point libraries
                                                                       Functions of a declared variable in SageMath are translated
once they are in place.
                                                                    into anonymous functions in Lean; underscore symbols rep-
B. desolve                                                          resent unused constants of integration that are ignored by the
   The desolve tactic provides witnesses to general solutions       Lean function. Some examples are given below:
of ordinary differential equations. DSLean transforms a target      >>> x+1                  -- SageMath
problem into a format readable by the SageMath computer
algebra system [32], as well as translating computed solutions      fun _ _ _ x =>           -- Lean translation
back into Lean.                                                       x + 1
example : isODEsolution
  (fun x => fun y => deriv y x = 1)                                 >>> (_K2∗ x + _K1)∗ e^(-x) -- SageMath
  (fun C _ _ x => x + C) := by
  desolve                                                           fun _ K1 K2 x =>       -- Lean translation
                                                                      (K2 ∗ x + K1) ∗ Real.exp(-x)
example : isODEsolution
  (fun x => fun y => x ∗ deriv y x + y x =
    0)                                                              -- SageMath
  (fun C _ _ x => C/x) := by                                        >>> -1/120∗ x^5 + 1/6∗ x^3 - x + sin(x) + C
  desolve
                                                                    -- Lean translation
example : isODEsolution                                             fun C _ _ x =>
  (fun x => fun y => deriv y x + y x = 1)                             (-1/120) ∗ x^5 + 1/6 ∗ x^3 - x +
  (fun C _ _ x => (C + Real.exp x) ∗                                   Real.sin(x) + C
   (Real.exp (-x))) := by
  desolve                                                             SageMath’s differential equations library does not provide
                                                                    any form of proof certificate beyond the solution itself; and
moreover, Lean does not yet possess many foundational results          lean_m2
on the theory of ODEs. As such, unlike all other examples in           Additionally, lean_m2 detects and reports when asserted
this paper, the desolve tactic treats SageMath as an oracle,        statements about membership do not hold:
using an axiom of its assumed correctness to complete the
proof, and explicitly informing users of such. Despite this, we     example (x y z : R) : x^2 ∗ y + z^3 ∈
believe it serves as an example of DSLean’s ability to allow           Ideal.span {x, y} := by
                                                                        lean_m2
communication between Lean and computer-algebra systems;            /-
similar tactics remain useful even without additional axioms,       lean_m2: Macaulay2 reports nonzero
such as those which provide proof witnesses (for example,              remainder (| x2^3 |) - element is not
Mathlib’s polyrith).                                                   in the ideal
                                                                    -/
C. lean_m2
                                                                       This tactic works with Mathlib’s definitions concerning ring
   The lean_m2 tactic automatically proves statements about         and field algebra, using DSLean and auxiliary scripting to turn
membership in ring ideals, a core part of algorithms that use       goals into an imperative script for Macaulay2 to compute. In
Gröbner bases to attack problems in program verification [25]       addition to the equivalences below, DSLean facilitates trans-
and kinematics [27]. By communicating with the Macaulay2            lation of a variety of more complicated rings and expressions;
computer algebra package [8] using DSLean, it finds and             this vocabulary allows lean_m2 to solve a broader range of
reconstructs Lean proofs of membership in a wide variety of         problems than existing polynomial reasoning tactics such as
user-specified fields and rings. Problems are expressed using       polyrith [30], including polynomials over quotient rings.
Mathlib’s API (with Ideal.span representing the ideal
generated by a set of elements); some examples of its usage         external M2_out where
are given below.                                                       ...
                                                                      "ZZ" <== Z
example (x y : Z) : 2 * x + 3 * y ∈
                                                                      "QQ" <== Q
   Ideal.span {x, y} := by lean_m2
                                                                      "RR" <== R
                                                                      "CC" <== C
example (x y : Q) : x^2 * y + y^3 ∈
   Ideal.span {x, y} := by lean_m2
                                                                       "ii" <== Complex.I
                                                                       "a0" <== Polynomial.X -- a polynomial
example (a b c d e f : Q) : a^4+a^2*b*c
                                                                        indeterminate
   -a^2*d*e
    +a*b^3 + b^2*c*d -b^2*e*f + a*c^3 +
                                                                       "(" x ")" <== Polynomial.C x --
   b*c^2*d -c^2*f^2
                                                                        constant polynomial
    ∈ Ideal.span {a^2+b*c-d*e,
   a*b+c*d-e*f, a*c+b*d-f^2} := by
                                                                         R "/" x <== R / Ideal.span ({x} : Set
   lean_m2
                                                                         R)
  It also supports problems over finite fields, polynomial rings,        ...
and quotients of any of these:
                                                                      After translation back into Lean by similar methods,
example (x y : ZMod 5) : x^3 + y^3 ∈                                lean_m2 then synthesizes proof based on the output, or
   Ideal.span {x + y} := by lean_m2
                                                                    reports if the goal is unsatisfiable.
example (x y : C) : x^2 + y^2 ∈                                       The lean_m2 tactic was originally prototyped without
   Ideal.span {x - Complex.I * y} := by                             using DSLean. 3 After substituting DSLean in place of a large
   lean_m2                                                          bespoke translation script, the number of lines of code in its
                                                                    implementation was decreased by a factor of 5.
example (p q : Polynomial Z) : p^2 * q +
   p * q^2 ∈ Ideal.span {p * q} := by                                                     VI. C ONCLUSION
   lean_m2                                                            We present DSLean, an extensible and user-friendly frame-
                                                                    work for bridging between Lean 4 and arbitrary external DSLs.
open Polynomial in
                                                                    We additionally introduce three Lean automation tactics made
example (x y : Q[X] \ (Ideal.span
   {(X:Q[X])^2})) : x * y ∈ Ideal.span                              using DSLean, which take advantage of communication with
   {x^3, y} := by lean_m2                                           external solvers to address a range of nontrivial mathematics
                                                                    problems.
example (x y : Q) (h_sum : x+y = 0) :                                 While automation via external solvers is itself sufficient
   x^3 + y^3 = 0 := by                                              motivation for the use of such a system, there are undoubt-
  suffices h : x^3 + y^3 ∈ Ideal.span {x                            edly other applications of communication between ITPs and
   + y} by
    simp [h_sum] at h                                                  3 The original version of the tactic is hosted at https://github.com/riyazahuja/
    exact h                                                         lean-m2, and is not included in the supplementary material.
external languages. Future research could expand on this work                  [15] Fredrik Lindblad and Marcin Benke. A tool for automated theorem
by utilizing similar methods to, for example, translate syntax                      proving in Agda. In Types for Proofs and Programs, pages 154–169,
                                                                                    Berlin, Heidelberg, 2006. Springer Berlin Heidelberg. doi:10.1007/
of unverified programming languages into a form amenable                            11617990_10.
to verification. Additionally, although DSLean uses provably                   [16] Guillaume Melquiond.         Proving bounds on real-valued functions
correct definitional equality checks to implement almost every                      with computations. In Automated Reasoning, pages 2–17, Berlin,
                                                                                    Heidelberg, 2008. Springer Berlin Heidelberg.         doi:10.1007/
stage of translation, it still relies on some unverifiable code, the                978-3-540-71070-7_2.
chief example being Lean’s native parser. Future work could                    [17] Jia Meng and Lawrence C. Paulson. Translating higher-order clauses
focus on modifying the implementation so that properties                            to first-order clauses. Journal of Automated Reasoning, 40(1):35–60,
                                                                                    January 2008. doi:10.1007/s10817-007-9085-y.
about translations such as round-trip consistency could be                     [18] Abdalrhman Mohamed, Tomaz Mascarenhas, Harun Khan, Haniel Bar-
formally proven.                                                                    bosa, Andrew Reynolds, Yicheng Qian, Cesare Tinelli, and Clark Barrett.
                                                                                    lean-smt: An SMT tactic for discharging proof goals in Lean. In
                   VII. ACKNOWLEDGEMENTS                                            Computer Aided Verification, pages 197–212, Cham, 2025. Springer
                                                                                    Nature Switzerland. doi:10.1007/978-3-031-98682-6_11.
  Work partially supported by NSF Grant DMS-2434614,                           [19] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover
                                                                                    and programming language. In Automated Deduction – CADE 28: 28th
DARPA ExpMath Grant HR0011262E028, and a gift from                                  International Conference on Automated Deduction, Virtual Event, July
Convergent Research.                                                                12–15, 2021, Proceedings, page 625–635, Berlin, Heidelberg, 2021.
                                                                                    Springer-Verlag. doi:10.1007/978-3-030-79876-5_37.
                             R EFERENCES                                       [20] Chase Norman and Jeremy Avigad. Canonical for automated theorem
                                                                                    proving in Lean. In 16th International Conference on Interactive
 [1] Michaël Armand, Germain Faure, Benjamin Grégoire, Chantal Keller,              Theorem Proving (ITP 2025), volume 352 of Leibniz International
     Laurent Théry, and Benjamin Werner. A modular integration of                   Proceedings in Informatics (LIPIcs), pages 14:1–14:20, 2025. doi:
     SAT/SMT solvers to Coq through proof witnesses. In Certified Programs          10.4230/LIPIcs.ITP.2025.14.
     and Proofs (CPP 2011), pages 135–150, Kenting, Taiwan, December           [21] Lawrence Paulson and Jasmin Blanchette. Three years of experience
     2011. Springer. doi:10.1007/978-3-642-25379-9_12.                              with Sledgehammer, a practical link between automatic and interactive
 [2] Clark Barrett, Swarat Chaudhuri, Fabrizio Montesi, Jim Grundy, Push-           theorem provers. In Proceedings of the 8th International Workshop on
     meet Kohli, Leonardo de Moura, Alexandre Rademaker, and Sorrachai              the Implementation of Logics, February 2015. doi:10.29007/tnfd.
     Yingchareonthawornchai. CSLib: The Lean computer science library,         [22] Vaughan R. Pratt. Top down operator precedence. In Proceedings
     2026. arXiv:2602.04846.                                                        of the 1st Annual ACM SIGACT-SIGPLAN Symposium on Principles
 [3] Alexander Bentkamp, Ramon Fernández Mir, and Jeremy Avigad. Ver-               of Programming Languages, POPL ’73, page 41–51, New York, NY,
     ified reductions for optimization. In International Conference on Tools        USA, 1973. Association for Computing Machinery. doi:10.1145/
     and Algorithms for the Construction and Analysis of Systems, pages             512927.512931.
     74–92. Springer, 2023. doi:10.1007/978-3-031-30820-8_8.                   [23] Yicheng Qian, Joshua Clune, Clark Barrett, and Jeremy Avigad. Lean-
 [4] Joshua Clune, Yicheng Qian, Alexander Bentkamp, and Jeremy Avigad.             Auto: An interface between Lean 4 and automated theorem provers.
     Duper: A proof-producing superposition theorem prover for dependent            In Computer Aided Verification, pages 175–196, Cham, 2025. Springer
     type theory. In 15th International Conference on Interactive Theorem           Nature Switzerland. doi:10.1007/978-3-031-98682-6_10.
     Proving (ITP 2024), volume 309 of Leibniz International Proceedings       [24] Alejandro Radisic. LeanCert: Verified computation & interval arithmetic,
     in Informatics (LIPIcs), pages 10:1–10:20, Dagstuhl, Germany, 2024.            2026. URL: https://github.com/alerad/leancert.
     Schloss Dagstuhl – Leibniz-Zentrum für Informatik. doi:10.4230/           [25] E. Rodríguez-Carbonell and D. Kapur. Generating all polynomial
     LIPIcs.ITP.2024.10.                                                            invariants in simple loops. Journal of Symbolic Computation, 42(4):443–
 [5] Łukasz Czajka and Cezary Kaliszyk. Hammer for Coq: Automation for              476, 2007. doi:10.1016/j.jsc.2007.01.002.
     dependent type theory. Journal of Automated Reasoning, 61(1):423–453,     [26] Hao Shen, Junyu Guo, Junqi Liu, and Lihong Zhi. Automated tactics
     June 2018. doi:10.1007/s10817-018-9458-4.                                      for polynomial reasoning in Lean 4, 2026. arXiv:2604.13514.
 [6] Marc Daumas and Guillaume Melquiond. Certification of bounds on           [27] Sabine Stifter. Algebraic methods for computing inverse kinematics.
     expressions involving rounded operators. ACM Trans. Math. Softw.,              Journal of Intelligent and Robotic Systems, 11(1):79–89, March 1994.
     37(1), January 2010. doi:10.1145/1644001.1644003.                              doi:10.1007/BF01258295.
 [7] Emilio Jesús Gallego Arias. SerAPI: Machine-Friendly, Data-Centric        [28] S. Doaitse Swierstra and Luc Duponcheel. Deterministic, error-
     Serialization for COQ. working paper or preprint, October 2016. URL:           correcting combinator parsers. In Advanced Functional Programming,
     https://minesparis-psl.hal.science/hal-01384408.                               pages 184–207, Berlin, Heidelberg, 1996. Springer Berlin Heidelberg.
 [8] Daniel R. Grayson and Michael E. Stillman. Macaulay2, a software               doi:10.1007/3-540-61628-4_7.
     system for research in algebraic geometry. Available at http://www2.      [29] Yong Kiam Tan, Scott Owens, and Ramana Kumar. A verified type
     macaulay2.com.                                                                 system for CakeML. In Proceedings of the 27th Symposium on the
 [9] David Greenaway. Automated proof-producing abstraction of C code.              Implementation and Application of Functional Programming Languages,
     PhD thesis, CSE, UNSW, August 2014. doi:10.5281/zenodo.                        IFL ’15, New York, NY, USA, 2015. Association for Computing
     50621.                                                                         Machinery. doi:10.1145/2897336.2897344.
[10] Thomas Hickman, Christian Pardillo Laursen, and Simon Foster. Certi-      [30] The Mathlib Community. The Lean mathematical library. In Proceedings
     fying differential equation solutions from computer algebra systems in         of the 9th ACM SIGPLAN International Conference on Certified Pro-
     Isabelle/HOL, 2021. arXiv:2102.02679.                                          grams and Proofs, CPP 2020, page 367–381, New York, NY, USA, 2020.
[11] Son Ho and Jonathan Protzenko. Aeneas: Rust verification by functional         Association for Computing Machinery. doi:10.1145/3372885.
     translation. Proc. ACM Program. Lang., 6(ICFP), August 2022. doi:              3373824.
     10.1145/3547647.                                                          [31] The Rocq Development Team. The Rocq prover, September 2025. doi:
[12] Vladimir Komendantsky, Alexander Konovalov, and Steve Linton. View             10.5281/zenodo.15149628.
     of computer algebra data from Coq. In Intelligent Computer Mathemat-      [32] The SageMath Developers. SageMath, February 2026. URL: https:
     ics, pages 74–89, Berlin, Heidelberg, 2011. Springer Berlin Heidelberg.        //github.com/sagemath/sage, doi:10.5281/zenodo.8042260.
     doi:10.1007/978-3-642-22673-1_6.                                          [33] Tomáš Skřivan. Scientific computing in Lean, 2025. URL: https://github.
[13] Xavier Leroy. Formal verification of a realistic compiler. Communica-          com/lecopivo/SciLean.
     tions of the ACM, 52, 07 2009. doi:10.1145/1538788.1538814.               [34] Ming-Hsien Tsai, Yu-Fu Fu, Jiaxiang Liu, Xiaomu Shi, Bow-Yaw
[14] Robert Y. Lewis and Minchao Wu.               A bi-directional extensi-        Wang, and Bo-Yin Yang. Coqcryptoline: A verified model checker
     ble interface between Lean and Mathematica.            Journal of Au-          with certified results. In Computer Aided Verification, pages 227–
     tomated Reasoning, 66(2):215–238, May 2022. doi:10.1007/                       240, Cham, 2023. Springer Nature Switzerland. doi:10.1007/
     s10817-021-09611-1.                                                            978-3-031-37703-7_11.
[35] Sebastian Andreas Ullrich. An Extensible Theorem Proving Frontend.
     PhD thesis, Karlsruher Institut für Technologie (KIT), 2023. doi:10.
     5445/IR/1000161074.
[36] Thomas Zhu, Joshua Clune, Jeremy Avigad, Albert Q. Jiang, and Sean
     Welleck. Premise selection for a Lean hammer. In The Fourteenth
     International Conference on Learning Representations, 2026. URL:
     https://openreview.net/forum?id=m04JJNeRK6.
