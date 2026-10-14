Journal of Automated Reasoning (2025) 69:25
https://doi.org/10.1007/s10817-025-09722-z




Reasoning About Incompletely Defined Programs

Christoph Walther1

Received: 29 March 2024 / Accepted: 12 March 2025 / Published online: 25 August 2025
© The Author(s) 2025


Abstract
We consider automated reasoning about recursively defined partial functions with decidable
domain, i.e. functions computed by incompletely defined (or underspecified) but terminating
functional programs. We define an interpreter for those programs, consider termination and
investigate the semantics of incompletely defined programs. The interpreter may halt with a
stuck computation, e.g. when dividing a number by zero, which represents a runtime error in
a conventional programming environment. We show how so-called domain procedures are
synthesized which decide the domain of incompletely defined procedures in almost all cases.
As calls of domain procedures occur in proof obligations, domain procedures are optimized
to make them as simple as possible. We also use domain procedures to refine the program
semantics such that statements causing stuck computations do not hold. Our method to reason
about incompletely defined programs is implemented in the verification tool VeriFun.

Keywords Incompletely defined programs · Underspecification · Loose specification ·
Automated reasoning · Program verification · Theorem proving by induction · VeriFun


1 Introduction

Programs which halt with a runtime error by throwing an exception or printing an error
message are ubiquitous in the use of computers. Division by zero is a common example of
such a fault that programming beginners soon get to know. Formally, the program computes
a partial function where the argument causing the failure is outside the function’s domain.
Other programs may run forever if procedures are called with arguments outside their domain.
   In the former case, the domain of the computed function is decidable. Therefore a program
interpreter can check whether an argument is not in the domain and react appropriately. In
the latter case the domain may be undecidable, and then there is no universal cure to prevent
looping.
   Logics for verification of programs computing partial functions are complicated to under-
stand and to use compared to logics for verification of programs computing total functions.
But if only the harmless cases of partiality have to be dealt with, i.e. all functions computed
by a program have a decidable domain, logics for verification of programs computing total
functions can be used to cope with those partial functions as well.
B Christoph Walther
    Christoph.Walther@tu-darmstadt.de
1   Fachbereich Informatik, Technische Universität Darmstadt, Hochschulstrasse 6, 64283 Darmstadt,
    Hesse, Germany


                                                                                           123
25   Page 2 of 48                                                                      C. Walther




Fig. 1 Program statements with indetermined results



    When restricted to monomorphic types, a procedure computing a partial function with
decidable domain can always be “completed” by providing arbitrary results for arguments
outside the domain. For example, one may define x/0 := x or x/0 := 0 etc., however
for the price of creating nonsense theorems like ∀x, y: N x/0 + y = x + y/0 or ∀x, y:N
x/0 ∗ y = x ∗ y/0. Moreover readability of programs is spoiled by this workaround as a
program user may be in doubt whether a certain result is essential or just arbitrarily chosen as
it does not matter at all. In addition, completion is not an option for polymorphic procedures.
For example, one cannot complete a procedure function last(k:list[@T ]):@T <= . . . com-
puting the last element of a non-empty polymorphic list with type variable @T by providing
an arbitrary result of type @T for last when called with the empty list.
    The remedy is underspecification, a method being widely used in reasoning systems:
Procedures may be underspecified by defining them incompletely, i.e. by being silent about
the results when a procedure is called with arguments outside the procedure’s domain. We
call a result indetermined in such a case.
    Naturally the question arises what holds and does not hold for statements involving inde-
termined result. The answer depends, of course, on the semantics of the formulas specifying
program properties: Let ThPr be the theory of a program Pr defined as ϕ ∈ ThPr iff ϕ is a
true statement about properties of Pr. As ThPr is closed under entailment, statement (1) of
Fig. 1 is true because it is an instance of the reflexivity law. If we define addition + in Pr
and prove commutativity, then statement (2) of Fig. 1 is true as commutativity entails (2).
If we define multiplication ∗ and division / in Pr, then (3) holds claiming that a procedure
call is not evaluated eagerly. If the semantics respect the law of the excluded middle, then
statements (5) and (6) of Fig. 1 must be true as well. But statements (7) and (8) are not in
ThPr (for any decent semantics at least).
    Statements (1)–(6) of Fig. 1 are rather strange and differ not that much from the nonsense
theorems obtained when completing monomorphic functions. This is the main criticism on
the underspecification approach found in the literature. But there is a more severe objection
on assigning truth to those statements: The purpose of formal verification is to prove that a
certain property holds for each result computed by a program (thus making testing obsolete).
For instance, having proved commutativity of + one expects that a program interpreter
computes true for any ground instance of the commutativity law: As an interpreter comes
up with 3 independent of being called with 1 + 2 or with 2 + 1, equation 1 + 2 = 2 + 1
is computed to true. However this does not hold if the theory ThPr does not exactly reflect
the semantics of the programming language. Calling the interpreter with the ground instance
1/0 + 2 = 2 + 1/0 of commutativity results in abortion rather than yielding true because
computation of 1/0 results in a runtime error. Likewise a runtime error instead of true is
obtained for 0 ∗ (1/0) = 0 if the interpreter implements call-by-value for procedure calls.
    Subsequently, we define a semantics for program statements such that disagreements
between true statements and the results computed by an interpreter are avoided. To this
effect, the refined theory Th∗Pr ⊂ ThPr will be defined by excluding certain formulas from
ThPr . We shall prove that the computation of each monomorphic constructor ground instance
of any ϕ ∈ Th∗Pr does not come up with a runtime error, but is computed to true. Consequently,

123
Reasoning About Incompletely Defined Programs                                                  Page 3 of 48    25


none of the statements in Fig. 1 are members of Th∗Pr . Unfortunately, we cannot avoid the
exclusion of certain program statements from ThPr which do not cause runtime errors. But
we will provide evidence that those statements are examples of a bad specification style rather
than of any reasonable interest.
   The remainder of this paper is organized as follows: Our approach is implemented in the
verification tool eriFun1 [26, 28] and we start by giving a short account on the system’s
object language L in Sect. 2. Next we define an interpreter for L-programs, investigate termi-
nation in the presence of incompletely defined procedures and give a semantics for program
statements by defining the theory ThPr of a terminating L-program Pr in Sect. 3. We illustrate
in Sect. 4 how program statements are proved by the system to the extent required for the
sequel. Section 5 presents the automated synthesis of a domain procedure ∇ f for a procedure
 f which computes a predicate whose extension is a subset of the domain of procedure f .
Soundness of domain procedures is proved with Theorem 2. In Sect. 5.1, the notion of a safe
procedure is introduced and it is proved with Theorems 4 and 5 that domain procedure ∇ f
decides the domain of a procedure f iff procedure f is safe. We also provide evidence that
unsafe procedures usually do not occur in programs and are examples of a bad programming
style. We show in Sect. 5.2 how domain procedures are automatically optimized to support
theorem proving as calls of domain procedures occur in proof obligations but may contain
redundant cases and obsolete recursive calls upon initial synthesis. Soundness of recursion
elimination is proved with Theorems 6 and 7. We define in Sect. 5.3 the refined theory Th∗Pr
of an L-program Pr and prove the absence of runtime errors when computing monomorphic
constructor ground instances of members of Th∗Pr with Theorem 8. Section 5.4 illustrates
the implementation of our method. We conclude with a discussion of related work and a
summary in Sects. 6 and 7.


2 The Object Language L

eriFun’s object language L provides principles for defining polymorphic data types,
procedures operating on them and for statements (called “lemmas”) about the data types and
procedures. The language allows Unicode and offers in-, out-, pre- and postfix notation so that
readability is increased by use of the familiar mathematical notation. Function applications
are written in prefix notation if not declared otherwise. If a function symbol is declared as
infix, a priority must be declared as well. Priorities are omitted in examples as we are not
concerned with syntax analysis here. The name of a function as well as its fixity and priority
can always be changed by the system’s Rename command.
    An L-program is a finite and non-empty list Pr of data type, procedure and lemma
definitions:
Data Types A data type op[@T1 , . . . , @Tn ] is defined by an expression of form
                           structure op[@T1 , . . . , @Tn ] <= e1 , . . . , em
with m ≥ 1, where @T1 , . . . , @Tn with n ≥ 0 is a list of pairwise different type varia-
bles and each e ∈ {e1 , . . . , em } is an expression of form cons(sel1 :τ1 , . . . , selh :τh ) with
h ≥ 0.2 An expression e introduces a constructor function symbol cons : τ1 × . . . × τh →
op[@T1 , . . . , @Tn ] and selector function symbols sel j : op[@T1 , . . . , @Tn ] → τ j for each
1 Short for “A Verifier for Functional Programs”.
2 Identifiers of type variables are of form @ . . . and each identifier not denoting a type variable must not have
@ as leading symbol.


                                                                                                    123
25   Page 4 of 48                                                                        C. Walther




Fig. 2 Data types, procedures and lemmas



argument position j of cons. Each argument type τ j of cons either is (an instance of) a
data type whose definition precedes the definition of op[@T1 , . . . , @Tn ] in list Pr but is
different from the predefined data type bool or τ j ∈ {@T1 , . . . , @Tn , op[@T1 , . . . , @Tn ]}
else. A constructor is recursive iff op[@T1 , . . . , @Tn ] is one of its argument types, and
op[@T1 , . . . , @Tn ] is recursive iff it has one recursive constructor at least. It is demanded
that op[@T1 , . . . , @Tn ] has one non-recursive constructor at least and that the type operator
symbol op, the constructor and the selector function symbols of the data type are pairwise
different. We write cons instead of cons( ) for a constructor constant and op instead of op[ ]
for a monomorphic data type, i.e. a data type without type variables.
    For instance, data type bool of Fig. 2 consists of two constructor constants only. Data type
N defines the natural numbers with constructors 0 and + (. . .) for the successor function.
Selector − (. . .) stands for the predecessor function. Data type N is recursive whereas data
type bool is not. Numbers up to 42 may be written in decimal notation and any number is
displayed in decimal notation, e.g. 3 instead of + (+ (+ (0))). Data types with type variables
are called polymorphic. Data type list[@T ] of Fig. 2 with constructors ∅ for the empty list
and :: for creating a list is an example. The functions hd and tl (for head and tail) are the
selectors of :: yielding (if applied to a non-empty list) the leftmost list element and the list
with the leftmost element removed respectively.
    A selector sel of a constructor cons is called recursive iff the result types of sel and cons
are identical. For instance, selector tl of list constructor :: is recursive whereas selector hd
is not. Non-recursive selectors are incompletely defined. For instance, selector hd cannot
be completely defined as no result can be given for hd(∅). Recursive selectors sel could
be completely defined by stipulating sel(cons(. . .)) := cons(. . .) if sel does not belong to
constructor cons. But we let recursive selectors also incompletely defined as complete defi-
nitions like e.g. −(0) := 0 and tl(∅) := ∅ are quite artificial and the different treatment of
selectors could be confusing.
    We let types[Pr] denote the set of all types which can be obtained from the data type
definitions of an L-program Pr. An element of types[Pr] either is a data type defined in

123
Reasoning About Incompletely Defined Programs                                          Page 5 of 48   25


Pr or is obtained as an instance (τ ) of a polymorphic data type τ where the type sub-
stitution  replaces some type variable(s) of τ by some element(s) of types[Pr]\ {bool}.
mtypes[Pr] ⊂ types[Pr] stands for the set of all monomorphic types of Pr. For instance,
N, list[N] and list[list[N]] are elements of mtypes[Pr]. Also bool ∈ mtypes[Pr], but
list[bool] ∈
           / mtypes[Pr] as bool is only used to define predicates and connectives, hence
type variables must not be instantiated with bool (except for the type variable of function
symbol if , see below).
Procedures A procedure is defined by an expression of form

                             function f (x1 :τ1 , . . . , xn :τn ):τ <= Rf

with n ≥ 1 which introduces a procedure function symbol f : τ1 × · · · × τn → τ with
argument types τi ∈ types[Pr]\ {bool} and result type τ ∈ types[Pr] having no other type
variables than in the argument types. Procedure body Rf is a first-order term of type τ
over the pairwise different variable symbols x1 , . . . , xn and function symbols introduced
by data type and procedure definitions preceding the definition of procedure f in list Pr
plus (i) the function symbol f (thus enabling recursive definitions), (ii) the function symbol
if : bool × @T × @T → @T , (iii) the function symbol ¬ : bool → bool, (iv) the function
symbol = : @T × @T → bool and (v) the symbol . The negation function ¬ is formally
not required and used to avoid the clumsy negation if {a, false, true} in procedure and lemma
definitions and in proofs. Function “=” denotes equality of non-boolean terms. Symbol 
must only be used as a result of a procedure call and denotes an indetermined, i.e. unspecified,
result for the respective input. Symbol  is considered as a constant of any type for purpose
of syntax and program analysis. It is demanded that procedure body Rf is in if -normal form
which means that Rf has no subterms of form (i) if {if {a, b, c}, s, t}, (ii) if {¬ a, s, t} and (iii)
g(. . . , if {a, s, t}, . . .) for g = if . A procedure body with those subterms spoils readability of
a procedure and complicates program analysis. This demand does not restrict expressiveness
of L as (i) can be equivalently replaced with if {a, if {b, s, t}, if {c, s, t}}, (ii) with if {a, t, s}
and (iii) with if {a, g(. . . , s, . . .), g(. . . , t, . . .)}.
    Procedure “/” of Fig. 2 is an example of an incompletely defined procedure. Predicates
are defined by procedures with result type bool. Procedure “ >” of Fig. 2 is an example and
“=” is called a predicate as well. As a predicate cannot be used as a parameter of a function,
terms of type bool are not allowed as function arguments except for if and ¬.
Lemmas Properties of constructors, selectors and procedures are specified by expressions
of form

                               lemma  <= ∀x 1 :τ1 , . . . , xn :τn b

with variable types τi ∈ types[Pr]\ {bool} and some Unicode text  for naming the lemma.
Lemma body b is an if -normalized first-order term of type bool over the pairwise different
variable symbols x1 , . . . , xn and function symbols introduced by data type and procedure
definitions preceding the definition of L-lemma  in list Pr plus the function symbols if ,
¬ and “=”. One writes e.g. if {a, b, true} for a → b, if {a, b, false} for a ∧ b , if {a, true, b}
for a ∨ b etc. Only universal quantification is allowed for the variables of an L-lemma, and
Fig. 2 displays an example. The string in the headline (between “lemma ” and “<=”) is
the identifier naming the lemma for reference and must not be confused with the statement
of the lemma which is given as a boolean term in the lemma body. We use the if -notation
in definitions and proofs on the meta-level but write L-lemmas in examples with the usual
connectives in most cases.

                                                                                            123
25   Page 6 of 48                                                                          C. Walther


   There is no overloading of symbols in L, i.e. no definition D may use an identifier for
defining a type operator symbol, a function symbol or a lemma name which already had been
introduced by definitions preceding D in list Pr . The language also allows case-conditionals
and let -expressions which are omitted here as they have no impact on the subject of the paper.
The data types bool and N as well as function symbol “=” and procedure “ >” are predefined
in the system, i.e. these program items belong to each L-program Pr . Data type bool is
predefined to formulate connectives and to define predicates. Data type N and procedure “ >”
are predefined to formulate termination hypotheses for procedures if automated termination
analysis fails, where well-foundedness of “ >” is assumed.
   The system’s pretty printer displays procedure definitions in procedural notation if -then-
else-end_if and lemma bodies in functional notation if {·, ·, ·} and uses N, >, ¬ and =
when displaying L-expressions and we keep these conventions in our examples. But we
write nat, gt, not and eq instead in definitions, theorems and proofs of the meta-language to
avoid confusion.
   The following notions are used subsequently:


 • (Pr) is the signature of the function symbols introduced by the data type and procedure
   definitions of an L-program Pr. We use f ∈ (Pr)τ1 ×···×τn →τ to denote the argument
   types τ1 , . . . , τn and the result type τ of f .
 • (Pr)c is the sub-signature of the constructor function symbols in Pr.
 • (Pr)sel is the sub-signature of the selector function symbols in Pr.
 • (Pr)proc is the sub-signature of the procedure function symbols in Pr.
 • T ((Pr), V )τ denotes the set of first-order terms of type τ over (Pr) and an infinite
   set V of variable symbols. Type subscript τ is omitted if irrelevant in a certain context.
 • T ((Pr))τ ⊂ T ((Pr), V )τ denotes the set of ground terms of type τ .
 • F ((Pr), V ) is the set of closed first-order formulas with function symbols from Pr and
   equality ≡ as the only predicate symbol.
 • S ((Pr), V ) ⊂ F ((Pr), V ) is the set of specification formulas of Pr and defined
   as the smallest set of formulas of form [ ∀x1 :τ1 , . . . , xn :τn b ≡ true ] where b ∈
   T ((Pr), {x 1 , . . . , x n })bool is if -normalized. Such a specification formula is represented
   in the system as an L-lemma lemma  <= ∀x1 :τ1 , . . . , xn :τn b.


3 Semantics

3.1 Formal Preliminaries

To define a semantics for L-programs with incompletely defined procedures function
 f (x1 :τ1 , . . . , xn :τn ):τ <= Rf , we have to get rid of the  – symbol in procedure body
Rf . A  – free procedure body R f is obtained by replacing each occurrence of  in Rf with
 f (x1 , . . . , xn ). Formally, Rf denotes a procedure body given by a programmer (and is dis-
played in the system’s pretty printer for programs). We write Rf for the system’s internal
 – free representation of the procedure body which is used when drawing inferences (and is
displayed in the system’s pretty printer for proofs).
    Subsequently we use occurrences (also called positions) π of a term t which are finite
sequences n 1 · . . . · n k of natural numbers, where ε stands for the empty sequence. An
occurrence π of t represents an “address” in t, t|π denotes the subterm of t at occurrence π,
and t[π ← s] is the term obtained from t by replacing subterm t|π with term s. Occ(t) is

123
Reasoning About Incompletely Defined Programs                                      Page 7 of 48   25


the set of all occurrences of t. See literature from the term rewriting area, e.g. [3], for further
details.
   We call an if - and not-free boolean term an atom, an atom and a negated atom a literal,
and define:
Definition 1 (Result term, condition path,c-path) Let t ∈ T ((Pr), V ) be a term in if -
normal form. Then a subterm r of t is a result term in t iff
(1) r is if -free, and
(2) t = r or if {·, r , ·} is a subterm of t or if {·, ·, r } is a subterm of t.
   If π ∈ Occ(t), then the condition path c-path[t, π] of t|π is the smallest set of literals
given as
                     ⎧
                     ⎨ {b} ∪ c-path[t2 , π  ],    if t = if {b, t2 , t3 } and π = 2 · π  ,
     c-path[t, π] :=   {not(b)} ∪ c-path[t3 , π ], if t = if {b, t2 , t3 } and π = 3 · π  ,
                                                
                     ⎩
                       ∅,                          otherwise.                           
   We demand for a procedure function f (x1 :τ1 , . . . , xn :τn ):τ <= Rf that  occurs in Rf
only in place of result terms, and we let
 • Occres                                                                  
        f denote the set of all π ∈ Occ(Rf ) with Rf |π is a result term in Rf ,
 • Occf denote the set of all π ∈ Occres        
                                         f with Rf |π = ,
 • Occf denote the set of all π ∈ Occf with Rf|π =  and f neither occurs in Rf|π nor
        base                               res

   in the literals of c-path[Rf , π], and
 • Occrec                                            
        f denote the set of all π ∈ Occ(Rf ) with Rf |π = f (. . .).


3.2 An Interpreter for L-Programs

For giving a semantics of an L-program Pr, we first define how computations of monomorphic
ground terms from Pr are performed. Formally, computation means to transform a ground
term of some monomorphic type η to a constructor ground term of type η. To avoid non-
termination, recursive calls stemming from the  – replacement must not be executed. To
this effect, the exception guard except f of a procedure f with procedure body Rf is defined
as
                                                              
                       exceptf :=                           
                                                                    .
                                            π ∈Occf      ∈c-path[Rf ,π ]
                                                                              if
[b]if denotes the conversion of a boolean term b with the usual connectives to a boolean term
b which uses not and if -conditionals only.
   For instance, except/ is obtained as y = 0 for procedure “/” from Fig. 2, exceptmod is
obtained as y = 0 for procedure
            function [infix] mod(x, y : N) : N <=
                                                                                                  (1)
            if y = 0 then  else if y > x then x else ((x − y) mod y) end _if end _if
and exceptlog is computed for procedure log from Fig. 3 as
             if {2 > b, true, if {x = 0, true, if {x = 1, false, ¬ (x mod b) = 0}}}.
   By enabling execution of procedure calls f (λ(x 1 ), . . . , λ(xn )) only if computation of
λ(except f ) yields false, non-termination by the recursive calls stemming from the  –
replacements is avoided.
   The computation of ground terms is defined by the computation calculus:

                                                                                        123
25   Page 8 of 48                                                                             C. Walther




Fig. 3 Incompletely defined procedure log computing the logarithm of powers of b




Fig. 4 Inference rules of the computation calculus



Definition 2 (Computation calculus) The language of the computation calculus is given as
the set η∈mtypes[Pr] T ((Pr))η of all monomorphic ground terms of an L-program Pr. The
inference rules of the calculus (called computation rules) are displayed in Fig. 4, where q
is a non-boolean constructor ground term, cons and cons are non-boolean constructors with
cons = cons , seli is the i th selector of constructor cons, and b, b , ti , ti , si are ground terms
of appropriate monomorphic types. We write t ⇒Pr t  if t  results from t by application of
some computation rule, ⇒+                                                               ∗
                               Pr denotes the transitive closure of ⇒Pr and ⇒Pr is the reflexive
closure of ⇒+    . t
               Pr ⇓Pr  is the result of the computation    of t  and defined as  t  iff t ⇒∗ t   t 
                                                                                             Pr     Pr
for all ground terms t  . We write t ⇒!Pr t  iff t  = t⇓Pr .
    If C is a finite set of monomorphic ground literals, then C ⇒!Pr true iff  ⇒!Pr true for
each  ∈ C and C ⇒!Pr false iff  ⇒!Pr false for some  ∈ C.                                           

   The computation calculus defines an operational semantics or the interpreter for L-
programs. We demand that the computation rules are tried in the order of presentation, hence

123
Reasoning About Incompletely Defined Programs                                              Page 9 of 48   25


the computation calculus is deterministic and the result t⇓Pr of a computation—if existent—is
uniquely determined. The result either is a constructor ground term, i.e. a value like a natural
number, a truth value or a specific list, or is a stuck term, i.e. a non-constructor ground term
s with s = s⇓Pr . Stuck terms result from application of a selector to a constructor it does
not belong to. For instance, one obtains if {+(−(0)) = +(0), ·, ·} ⇒!Pr if {−(0) = 0, ·, ·} by
computation rules (8) and (3) as no computation rule exists to compute the predecessor of 0.
Therefore −(0) is a stuck term, −(0) = 0 is a stuck term as it cannot be computed to a truth
value, hence if {−(0) = 0, ·, ·} is a stuck term as well.
    Computation rule (11) implements call-by-value as the parameter passing discipline, i.e.
procedure calls are evaluated eagerly. As a consequence, stuck terms result from procedure
calls with a stuck term as actual parameter as e.g. log(−(0), 2) ⇒!Pr log(−(0), 2) for procedure
log from Fig. 3. A call of an incompletely defined procedure f may also yield a stuck term
if called with non-stuck arguments: If the instance λ(except f ) of the exception guard is
not computed to false, f (λ(x1 ), . . . , λ(xn )) ⇒!Pr f (λ(x1 ), . . . , λ(xn )) results. For instance,
log(3, 2) ⇒!Pr log(3, 2) and log(12, 2) ⇒!Pr +(+(log(3, 2))).
    A stuck term is the formal representation of a computation causing a runtime error in a
conventional programming environment. For instance, execution of the program statement
IF 1/0 = 0 THEN x := 42 ELSE x := 42 END of some imperative programming language
results in abortion of the program execution rather than in an assignment of 42 to the program
variable x, and correspondingly if {1/0 = 0, 42, 42} is a stuck term in our setting.
    Note that the rôle of the exception guard is only to disable execution of procedure calls
stemming from a  – replacement. Therefore one cannot conclude that a procedure call
f (λ(x1 ), . . . , λ(xn )) is computed to a constructor ground term if computation of λ(except f )
yields false. For example, λ(exceptlog ) ⇒!Pr false for λ = {x/12, b/2} although computation
of log(12, 2) yields a stuck term.
    Also one cannot conclude that a procedure f is completely defined if procedure body Rf is
 – free. For example, procedure “−” of Fig. 2 is incompletely defined (although except− =
false) and may yield stuck terms like 1 − 3 ⇒!Pr −(0) − 1.

3.3 Termination of L-Programs and Procedures

To define termination, constructor ground terms as computation results are needed. We there-
fore complete the incomplete definitions of selectors and procedures f by assigning arbitrarily
chosen constructor ground terms to indetermined f -calls:


Definition 3 (Extended computation calculus) An extension e of the computation calculus
is obtained by adding the computation rules

                                           ⎧
                                           ⎪
                                           ⎪ for some re [q1 , . . . , qn ] ∈ T ((Pr)c )e (τ  ) if
                                           ⎨
             sel(cons(q1 , . . . , qn ))     selector sel : τ → τ  does not belong to con-
        (12)                             ,
                  re [q1 , . . . , qn ]    ⎪
                                           ⎪ structor cons : τ1 × · · · × τn → τ , where
                                           ⎩
                                             qi ∈ T ((Pr)c )e (τi ) for each i ∈ {1, . . . , n}
                                          ⎧
                                          ⎪
                                          ⎪ for some re [q1 , . . . , qn ] ∈ T ((Pr)c )e (τ ) if
               f (q1 , . . . , qn )       ⎨                                              e
                                            f ∈ (Pr)τ1 ×···×τn →τ and λ(exceptf ) ⇒!Pr
                                                       proc
        (13)                        ,
              re [q1 , . . . , qn ]       ⎪
                                          ⎪ true, where λ(xi ) = qi ∈ T ((Pr) )e (τi ) for
                                                                                    c
                                          ⎩
                                            the formal parameters x1 , . . . , xn of f

                                                                                                123
25   Page 10 of 48                                                                             C. Walther


for a type substitution e with e (τ  ) ∈ mtypes[Pr] and e (τi ) ∈ mtypes[Pr] for each
                    e
i ∈ {1, . . . , n}. ⇒Pr denotes a computation step in the extended computation calculus.3 
   Each extended computation calculus is deterministic as well because computation rules
(12) and (13) cannot apply to a common redex and cannot apply if some computation rule
of the non-extended computation calculus applies.
   We write re [q1 , . . . , qn ] for the arbitrarily chosen constructor ground terms in the succe-
dents of computation rules (12) and (13) to denote that these constructor ground terms
formally depend on the constructor ground terms q1 , . . . , qn in the antecedent of the rules.
For instance, we may find
            e !                         e                       e                       e
       −(0) ⇒
              Pr 2,      hd(tl(1::∅)) ⇒!Pr 5, (0 mod 0) ⇒!Pr 3, (1 mod 0) ⇒!Pr 8
for a certain extension e of the computation calculus.
                                           e
   By the additional computation rules, t ⇒!Pr q for some q ∈ T ((Pr)c ) iff t⇓ePr exists. In
               e
particular, t ⇒!Pr q if t ⇒!Pr q ∈ T ((Pr)c ) because the additional computation rules (12)
and (13) of e are only applicable if t⇓Pr is not constructor ground. Hence we have:
Lemma 1 Let Pr be an L-program and let t ∈ T ((Pr)) be a ground term of monomorphic
type. Then for each extension e of the computation calculus
(1) t⇓ePr = t⇓Pr if t⇓Pr ∈ T ((Pr)c ),
(2) t⇓ePr ∈ T ((Pr)c ) if t⇓ePr exists, and
(3) t⇓Pr exists if t⇓ePr exists (but not vice versa).                            
    An L-program Pr terminates iff it terminates independent of how the monomorphic
 instances of the selectors and procedures in Pr are completed:
Definition 4 (Termination of L-programs) An L-program Pr terminates iff t⇓ePr exists for
each monomorphic ground term t ∈ T ((Pr)) and each extension e of the computation
calculus.                                                                             
   We cannot do without the extensions of the computation calculus when defining termina-
tion but only demand that t⇓Pr exists for each monomorphic ground term t. Such a definition
would ignore the meaning of an indetermined result, viz. that it stands for any value (repre-
sented by a constructor ground term). Consider, for instance, an L-program Pr null with
          function null(x:N):N <= if x = 0 then  else null(null(−(x))) end _if
as only procedure. As null(n) ⇒!Pr null (n+1) (0) for each n ∈ T ((Pr))nat , Pr null
                                                            e
terminates by the modified definition. We find null(n) ⇒!Pr 0 for each n ∈ T ((Pr))nat
with the extension null(0) := 0. But null(0) := 1 is an extension as well and then
null(1) ⇒+
         e                   e +          e +
           Pr null(null(0)) ⇒Pr null(1) ⇒Pr . . . . This example also shows that it is not
enough to demand the existence of t⇓ePr for some extension e of the computation calcu-
lus instead for each extension, and therefore Pr null does not terminate. But L-program Pr zero
with
                   function zero(x:N):N <=
                   if x = 0
                    then 
                    else if x > zero(−(x)) then zero(zero(−(x))) else  end _if
                   end _if
3 Each occurrence of ⇒ in the side conditions of the computation rules of Definition 2 has to be replaced
                      Pr
     e
with ⇒Pr when computing ground terms with an extended computation calculus.


123
Reasoning About Incompletely Defined Programs                                                      Page 11 of 48   25


as only procedure terminates. As zero(n)⇓Pr ∈ T ((Pr))\T ((Pr)c ) for each n ∈
T ((Pr)c )nat , nothing can be computed with procedure zero, but eriFun proves
                                  ∀n:N zero(0) = 0 → zero(n) = 0.                                                  (2)
   Termination of L-programs and termination of procedures are mutual recursively defined.
We start with a program without procedures and define termination of a procedure added to
this program. This yields a terminating program with a procedure which may be extended
by further terminating procedures resulting in a terminating L-program after each extension
step.
   Termination of a recursively defined procedure f requires that the evaluated arguments
of the recursive f -calls are smaller w.r.t. some well-founded relation than the arguments of
the initial procedure call:

Definition 5 (Termination of procedures) Let Pr be a terminating L-program, let function
f (x1 :τ1 , . . . , xn :τn ):τ <= Rf be a procedure with recursive calls Rf|π = f (θπ (x1 ), . . . ,
θπ (xn )) for each π ∈ Occrec                
                                 f and let Pr be obtained by extending Pr with procedure f . Then
procedure f terminates iff some well-founded relation  f on T ((Pr)c )e (τ1 ) × · · · ×
T ((Pr)c )e (τn ) exists such that
                                                              e
                                       λ(c-path[Rf , π]) ⇒!Pr  true
                                                                                                                  (3)
                   (λ(x1 ), . . . , λ(xn ))  f (λ(θπ (x1 ))⇓e  , . . . , λ(θπ (xn ))⇓e  )
                                                                  Pr                      Pr

for each π ∈ Occrec
                  f , each extended computation calculus e with type substitution e and
each substitution λ with λ(xi ) ∈ T ((Pr)c )e (τi ) for each i ∈ {1, . . . , n}.4   

Requirement (3) demands that each monomorphic constructor ground instance
(λ(θπ (x1 )), . . . , λ(θπ (xn ))) of the n-tuple of arguments of a recursive call is computed
with each extended computation calculus e to an n-tuple (λ(θπ (x1 ))⇓e  , . . . , λ(θπ (xn ))⇓e  )
                                                                           Pr                   Pr
which is  f -smaller than the initial n-tuple (λ(x1 ), . . . , λ(xn )) necessitating the recursive
call.

Theorem 1 (Termination of L-programs) Let Pr be a terminating L-program, let function
f (x1 :τ1 , . . . , xn :τn ):τ <= Rf be a procedure and let Pr  be obtained by extending Pr with
procedure f . Then Pr  terminates if procedure f terminates.

Proof Assume that procedure f terminates but L-program Pr  does not. Then there is some
extension e of the computation calculus with type substitution e and some  f -minimal n-
tuple q1 , . . . , qn ∈ T ((Pr)c )e (τ1 ) × · · · × T ((Pr)c )e (τn ) such that f (q1 , . . . , qn )⇓e 
                                                                                                         Pr
does not exist. Hence
         f (q1 , . . . , qn ) ⇒+    · · · f (λ(θπ (x1 ))⇓e  , . . . , λ(θπ (xn ))⇓e  ) · · · ⇒+
                            e                                                                  e
                               Pr                                                              Pr 
                                                                                                     ...
                                                        Pr                       Pr

with λ(xi ) = qi ∈ T ((Pr)c )e (τi ) for some recursive call f (θπ (x1 ), . . . , θπ (xn )) in
                            e
Rf with λ(c-path[Rf , π]) ⇒ !Pr  true. Then f (λ(θπ (x1 ))⇓e  , . . . ,λ(θπ (xn ))⇓e  )⇓e  does
                                                                           Pr                         Pr   Pr
not exist either thus contradicting the  f -minimality of q1 , . . . , qn as (q1 , . . . , qn )  f
(λ(θπ (x1 ))⇓e  , . . . , λ(θπ (xn ))⇓e  ) by (3).                                              
                                                                                                  
              Pr                       Pr


    e!
4 C ⇒                                                    !                e!
     Pr true/false is given as in Definition 2 but with ⇒Pr replaced with ⇒Pr .


                                                                                                           123
25   Page 12 of 48                                                                                C. Walther


3.4 The Theory of an L-Program

The theory ThPr ⊂ F ((Pr), V ) of a terminating L-program Pr is the set of all true state-
ments ϕ about the data types and procedures in Pr which can be written as closed first-order
formulas, and verification of ϕ means to prove that ϕ ∈ Th Pr . As we are interested in a sound
verifier only, verification of ϕ must not succeed if ϕ ∈
                                                       / Th Pr . Completeness of a verification
system means that a proof of ϕ can be obtained whenever ϕ ∈ Th Pr . However, completeness
cannot be achieved by Gödel’s First Incompleteness Theorem.
   The theory Th Pr is defined with the standard models of a terminating L-program Pr:

Definition 6 (Standard model) A standard model Me of a terminating L-program Pr is given
for an extension e of the computation calculus with type substitution e as a (Pr)-Algebra
Me := (M, μe ) freely generated by the constructors of Pr:
(1) M := η∈mtypes[Pr] T ((Pr)c )η , i.e. the carrier M of Me is the family of the sets of
    constructor ground terms of the monomorphic types of Pr.
(2) The interpretation of a function symbol f ∈ (Pr)τ1 ×···×τn →τ is defined for each ti ∈
    T ((Pr))e (τi ) with i ∈ {1, . . . , n} by
                           μe [f (t1 , . . . , tn )] := f (μe [t1 ], . . . , μe [tn ])⇓ePr .            (4)
(3) The interpretation of predicate ≡ is given for each t1 , t2 ∈ T ((Pr))η with η ∈
    mtypes[Pr] as
                              μe [t1 ≡ t2 ] iff μe [t1 ] = μe [t2 ].                                     

   Termination of Pr is demanded to guarantee the existence of a standard model. For
instance, loop(0) = + (loop(0)) must hold for a procedure
                              function loop(x:N):N <= +(loop(x))
but as n = n +1 for each n ∈ N, no standard model exists for a program containing procedure
loop.5
    As μe [t] = t⇓ePr for monomorphic ground terms t, requirement (4) of Definition 6
defines the interpretation of a function call as the constructor ground term computed with
some extension e of the computation calculus. If the non-extended computation calculus
yields a constructor ground term q when evaluating a function call f (. . .), q is the result
of the interpretation of f (. . .) in any standard model of Pr, cf. Lemma 1(1). μe is just
the identity function if applied to constructor ground terms. For the interpretation of non-
constructor ground terms e.g. μe [−(2)] = 1 and μe [log(4, 2)] = 2 are obtained. As
log(4, 2) ⇒!Pr 2, Me  [ log(4, 2) ≡ 2 ] for each standard model Me . If no rule of the
non-extended computation calculus can be applied to a function call f (q1 , . . . , qn ) with
{q1 , . . . , qn } ⊂ T ((Pr)c ), an arbitrarily selected constructor ground term re [q1 , . . . , qn ]
is obtained with the additional computation rules of Definition 3 and used for the interpre-
tation of f (q1 , . . . , qn ). For instance, 0 or 2 or whatever may be the result of interpreting
−(0) by the additional computation rule (12). If log(3, 2) ⇒     e
                                                                   Pr 5 by computation rule (13),
                                                                         e
then μe [log(12, 2)] = 7 because log(12, 2) ⇒Pr ( (log(3, 2))) ⇒!Pr 7. As the constructor
                                                      !  + +

ground terms re [q1 , . . . , qn ] in the computation rules of Definition 3 depend on q1 , . . . , qn ,
e.g. 3 might be the interpretation of log(0, 2). Consequently Me  [ log(12, 2) ≡ log(0, 2) ]

5 Formally, q = +(q) for each q ∈ T ((Pr)c )
                                             nat as the carrier M of each standard model is freely generated
by the constructors of Pr.


123
Reasoning About Incompletely Defined Programs                                           Page 13 of 48   25


but Me  [ log(12, 2) ≡ log(0, 2) ] for another standard model Me with μe [log(3, 2)] = 5
and μe [log(0, 2)] = 7.
   Each standard model defines a theory and the theory of a terminating L-program in turn:

Definition 7 (Theory Th Pr of an L-Program) Let Pr be a terminating L-program. Then the
theory Th(Me ) of a standard model Me of Pr is defined as {ϕ ∈ F ((Pr), V ) | Me |
e (ϕ)}.6 The theory Th Pr of Pr is given as {ϕ ∈ F ((Pr), V ) | ϕ ∈ Th(Me ) for each
standard model Me of Pr}.                                                            

   The theory Th Pr is consistent, i.e. ϕ ∈
                                          / Th Pr or ¬ϕ ∈  / Th Pr for each ϕ ∈ F ((Pr), V ),
because Th(Me ) is consistent for each standard model Me of Pr. The theory Th(Me ) of
each standard model Me is complete, i.e. either ϕ ∈ Th(Me ) or ¬ϕ ∈ Th(Me ) for each
ϕ ∈ F ((Pr), V ). Contrary to this, Th Pr is incomplete, i.e. neither ϕ ∈ Th Pr nor ¬ϕ ∈ Th Pr
for some ϕ ∈ F ((Pr), V ). Incompleteness results from the incompletely defined selectors
and procedures. For instance, some standard model Me of Pr may yield μe [1/0] = 0
whereas μe [1/0] = 1 for another standard model Me , and then Me  [1/0 ≡ 0] but Me 
[1/0 ≡ 0]. As [1/0 ≡ 0] ∈ Th(Me ) and [1/0 ≡ 0] ∈ Th(Me ), neither [1/0 ≡ 0] ∈ Th Pr
nor [1/0 ≡ 0] ∈ Th Pr .

Lemma 2 Let Pr be a terminating L-program, let t1 , t2 ∈ T ((Pr), {x1 , . . . , xn }) and let
ϕ := [∀x1 :τ1 , . . . , xn :τn t1 ≡ t2 ]. If λ(t1 )⇓Pr = λ(t2 )⇓Pr for each monomorphic constructor
ground instance λ(t1 ) and λ(t2 ) of t1 and t2 respectively, then ϕ ∈ Th Pr .

Proof If λ(t1 )⇓Pr = λ(t2 )⇓Pr , then λ(t1 )⇓ePr = λ(t2 )⇓ePr for each extension e of the computa-
tion calculus, hence ϕ ∈ Th(Me ) for each e and ϕ ∈ Th Pr in turn.                              
                                                                                                

   If λ(b) ⇒!Pr true for each monomorphic constructor ground instance λ(b) of a boolean
term b, then ϕ ∈ Th Pr for specification formula ϕ := [ ∀x1 :τ1 , . . . , xn :τn b ≡ true ] by
Lemma 2 in particular. But ϕ ∈ Th Pr does not necessarily entail λ(b) ⇒!Pr true:
If λ(b) is a stuck term, then λ(b) !Pr true although ϕ ∈ Th Pr . Also ϕ ∈ Th Pr
entails [ ∀x1 :τ1 , . . . , xn :τn σ (b) ≡ true ] ∈ Th Pr for each substitution σ with σ (xi ) ∈
T ((Pr), {x 1 , . . . , x n })τi . But if σ instantiates some variables xi with stuck terms, then
some monomorphic constructor ground instance of σ (b) might not be computed to true.

Example 1 (i) We find [ b ≡ true ] ∈ Th Pr for b := if {eq(1/0, 0), true, true} and procedure
                         e
“/” of Fig. 2 because b ⇒ !Pr true for each extension e of the computation calculus, hence
Me  [ b ≡ true ] for each standard model Me , but b⇓Pr = b = true.
   (ii) We find [ ∀x:N eq(x − x, 0) ≡ true ] ∈ Th Pr for procedure “−” of Fig. 2, hence
[ eq(−(0) − −(0), 0) ≡ true ] ∈ Th Pr . But −(0) − −(0) is a stuck term and therefore
eq( −(0) − −(0) , 0) !Pr true.                                                            

   Hence we can only prove:

Lemma 3 Let Pr be a terminating L-program and let ϕ := [∀x 1 :τ1 , . . . , xn :τn b ≡ true]
with ϕ ∈ ThPr . Then λ(b) !Pr false for each monomorphic constructor ground instance
λ(b) of b.

6 (ϕ) is defined for a type substitution  and a formula ϕ ∈ F ((Pr), V) as ∀x:(τ ) (ϕ  ) if ϕ = ∀x:τ
ϕ  , ∃x:(τ ) (ϕ  ) if ϕ = ∃x:τ ϕ  and as ϕ if ϕ is quantifier-free.


                                                                                              123
25   Page 14 of 48                                                                                 C. Walther




Fig. 5 Axioms of an L-program


Proof If λ(b) ⇒!Pr false for some substitution λ with λ(xi ) ∈ T ((Pr )c )(τi ) for some
                                                                                     e
type substitution  with (τi ) ∈ mtypes[Pr ] for each i ∈ {1, . . . , n}, then λ(b) ⇒!Pr false
for each extension e of the computation calculus by Lemma 1(1). As ϕ ∈ ThPr entails ϕ ∈
Th(Me ) for each standard model Me , [ λ(b) ≡ true ] ∈ Th(Me ) in particular if e =  and
[ false ≡ true ] ∈ Th(Me ) in turn. But the carrier M of a standard model is freely generated
by the constructors of Pr, hence [ false ≡ true ] ∈/ Th(Me ) contradicting λ(b) ⇒!Pr false.  
   Of course, we would rather like to have λ(b) ⇒!Pr true, i.e. that the interpreter yields true
for each monomorphic constructor ground instance of a verified L-lemma. We reconsider
this problem in Sect. 5.3 where we have the needed tools for a repair, see Theorem 8(2).

3.5 Axioms of an L-Program

To prove a statement ϕ ∈ S ((Pr), V ) about an L-program Pr, i.e. to prove whether ϕ ∈
Th Pr , usually induction is required. The base and step cases of the induction then are proved
by first-order reasoning.7 We use a first-order theorem prover tailored for these proofs, cf.
Sect. 4. To formulate soundness of this prover, the axiom set AX Pr of an L-program Pr is
used.
Definition 8 (Axioms of an L-program) Let Pr be a terminating L-program, let τ, τi , τi be
data types of Pr where τi , τi do not refer to bool, let cons and cons be different non-boolean
constructors, let seli be the i th selector of cons, and let f ∈ (Pr)proc with procedure body
Rf and formal parameters x1 , . . . , xn . Then the axiom set AX Pr of Pr is defined as the
smallest subset of F ((Pr), V ) displayed in Fig. 5.                                          
   If all variables in the monomorphic instances of the axioms are replaced with constructor
ground terms, then the constructor ground instances of the axioms can be proved with the
computation calculus. For example, for any monomorphic constructor ground instance of
Axiom (9) with (τi ) ∈ mtypes[Pr] and λ(xi ) ∈ T ((Pr )c )(τi ) for each i ∈ {1, . . . , n}
                                  f (λ(x1 ), . . . , λ(xn )) ⇒Pr λ(R f )
is obtained with computation rule (11) if λ(except f ) ⇒!Pr false. Otherwise

                                  λ(R f ) ⇒!Pr f (λ(x1 ), . . . , λ(xn ))
7 Base and/or step cases may require further induction proofs, but first-order proofs are needed for the most
nested inductions.


123
Reasoning About Incompletely Defined Programs                                           Page 15 of 48   25


by definition of the  – replacement and except f . Therefore f (λ(x1 ), . . . , λ(xn ))⇓Pr =
λ(R f )⇓Pr in either case, hence [ ∀x1 :τ1 , . . . , xn :τn f (x1 , . . . , xn ) ≡ R f ] ∈ Th Pr by Lemma
2. Truth of Axioms (1)−(8) is proved in the same way.
   All specification formulas which the system has already verified are available for first-
order reasoning by Axiom (10), and together with the above considerations AX Pr ⊂ Th Pr
must hold. We call a formula ϕ ∈ F ((Pr), V ) valid iff AX Pr | ϕ and ϕ is true iff
ϕ ∈ Th Pr .


4 Theorem Proving

We give a brief account on how the system verifies program properties: When extending a
terminating L-program Pr by a procedure f with k recursive calls,              eriFun’s automated
termination analysis is invoked for generating termination hypotheses ϕ 1f , . . . , ϕ kf for proce-
dure f such that {ϕ 1f , . . . , ϕ kf } ⊂ T h Pr entails that procedure f terminates. Each termination
hypothesis then must be proved like an L-lemma (see below). Termination analysis is based
on the method of Argument-Bounded Functions [27] which has been enhanced in [29] to
cope with incompletely defined procedures as well. Except for procedure subp of Sect. 6, the
system proves termination for each terminating procedure defined in this paper automatically
because true is obtained for all termination hypotheses except for the termination hypotheses
of procedures mod, / and log which need first-order reasoning. If automated termination
analysis fails (as it does for procedure subp), the user has to provide a termination function
for generating termination hypotheses.
    If an L-lemma lemma  <= ∀x1 :τ1 , . . . , xn :τn b is to be proved, the system heuristically
decides whether to use first-order reasoning or induction. In the latter case, an induction axiom
I f is computed from the recursion structure of some recursively defined and terminating
procedure f where I f ∈ Th Pr . The selection of induction axioms and the variables to induct
upon are heuristically driven. The user may withdraw the system’s decision and suggest
another induction axiom in the rare case that the heuristic fails.8
    The base and step formulas of I f are forwarded to the Symbolic Evaluator which rewrites
terms of any type using the definitions of the data types and procedures of an L-program,
the induction hypotheses and the L-lemmas already verified if called in Simplification mode.
The Symbolic Evaluator is a fully automated tool over which the user has no control. It
is guided by heuristics, e.g. for deciding whether to unfold a procedure call and for spee-
ding up proof search by filtering out useless L-lemmas. Equality reasoning is implemented
by conditional term rewriting with ACI-matching, where the orientation of equations is
heuristically established.
    The Symbolic Evaluator is the working horse of the system and used in almost all system
components. For any terms t, t  ∈ T ((Pr), V )τ , t  t  denotes that t  has been obtained
from t by a symbolic evaluation step. We write + for the transitive closure of  and ∗ for
the reflexive closure of + . t⊥ is defined as t  iff t ∗ t   t  for all terms t  and t ! t 
holds iff t  = t⊥ .
    Symbolic evaluation is sound in the sense that

                               t  t   AX Pr ∪ IH  ∀ . . . t ≡ t                                    (5)

8 The success rate for the induction heuristic is higher than 95% so that 4 user suggested induction axioms
are required in the average when proving 100 L-lemmas by induction.


                                                                                              123
25   Page 16 of 48                                                                                  C. Walther


holds, where ∀ . . . stands for the universal closure, IH is the set of induction hypotheses when
proving a step formula and IH = ∅ otherwise, hence
                            b ! true  AX Pr ∪ IH  ∀ . . . b ≡ true                                      (6)
for boolean terms b in particular. If        k
                                             i=1   bi  ! true for each boolean term bi representing
a base or step formula of I f , then [∀ . . . b ≡ true] ∈ T h Pr because AX Pr ∪ IH  ∀ . . . bi ≡
true for each i ∈ {1, . . . , k} by (6), AX Pr ⊂ Th Pr and I f ∈ ThPr .
    The Symbolic Evaluator is necessarily incomplete, i.e. b ! true although AX Pr ∪ IH 
∀ . . . b ≡ true for certain boolean terms b, because it is frequently called with true but
non-valid proof obligations so that completeness would result in non-termination. In such a
case, the system user must step in to support the system in the search for a proof, see [28]
for details.
    A procedure call f (σ (x1 ), . . . , σ (xn )) must not be executed symbolically if it stems from a
 – replacement. Hence σ (except f ) ! false is formally demanded before the procedure call
is opened.9 Besides termination analysis, this is the only required modification of a first-order
reasoner developed for verification of completely defined programs.
    Work is supported by importing data types, procedures and L-lemmas (with their proofs)
from other case studies with the system’s Import command.                 eriFun also provides a
Disprover [1] which is automatically invoked before a proof attempt for a system ge-
nerated conjecture (like a termination hypothesis) is started. Given a boolean term b ∈
T ((Pr ), {x 1 , . . . , x n })bool with variables xi of type τi for each i ∈ {1, . . . , n}, the Dis-
prover uses a type substitution nat which replaces each type variable in the types τi with
data type nat and searches for a monomorphic constructor ground instance λ(b) of b with
λ(xi ) ∈ T ((Pr )c )nat (τi ) and λ(b) ! false.
    The Symbolic Evaluator may also operate in restricted modes:
 • Weak Simplification (denoted by ws ) works like Simplification except that calls of
   recursively defined procedures are not opened.
 • Weak Normalization (denoted by wn ) works like Simplification except that procedure
   calls are not opened and neither induction hypotheses nor verified L-lemmas are used.
   eriFun uses Weak Simplification when simplifying terms with calls of system syn-
thesized procedures as these procedures quite often are not recursively defined. Weak
Normalization implements propositional reasoning in particular and is very fast. As sys-
tem generated conjectures usually are highly redundant, workload of the Symbolic Evaluator
and of the Disprover is significantly reduced if applied to weakly normalized formulas.


5 Domain Procedures

Non-trivial statements about incompletely defined procedures can only be proved for argu-
ments in the domain of these procedures. Therefore      eriFun synthesizes a domain
procedure ∇f for each procedure f which decides the domain of f in almost all cases.
This allows to formulate (and to prove) a statement like
       ∀b, x, y:N ∇log(x, b) ∧ ∇log(y, b) → log(x ∗ y, b) = log(x, b) + log(y, b)                          (7)
9 The exception guard is a conceptual notion which is too expensive in an implementation as σ (except )
                                                                                                     f
would have to be evaluated symbolically upon each f -call. Hence recursive calls in a procedure body Rf
which stem from a  – replacement are assigned a certain label, and labelled procedure calls are never executed
symbolically.


123
Reasoning About Incompletely Defined Programs                                             Page 17 of 48   25


for the incompletely defined procedure log from Fig. 3. Formula (7) states that the conclusion
of the implication holds, provided (x, b) and (y, b) are in the domain of procedure log.10
   For defining domain procedures, we assume two sub-signatures (Pr)∇proc and (Pr)proc
of (Pr)proc with
 • (Pr)proc defined as (Pr)proc \(Pr)∇proc ,
                 ∇proc
 • ∇sel j ∈ (Pr)τ →bool iff sel j ∈ (Pr)sel
                                          τ →τ j , and
                   ∇proc                            proc
 • ∇f ∈ (Pr)τ1 ×···×τn →bool iff f ∈ (Pr)τ1 ×···×τn →τ .
Domain procedures are only needed for selectors and user defined procedures as the functions
from {eq, not, if } ∪ (Pr)c ∪ (Pr)∇proc are completely defined.
   The body of a domain procedure is obtained with the determination guard:

Definition 9 (Determination guard) Let Pr be a terminating L-program and let t ∈
T ((Pr) ∪ {}, V ) be a term in if -normal form which may contain  in place of result
terms. Then the determination guard dg[t] ∈ T ((Pr), V )bool of t is given as
(1) false if t = ,
(2) true if t ∈ V ,
        n
(3) [ i=1    dg[ti ] ]if if t = g(t1 , . . . , tn ) and g ∈ {eq, not} ∪ (Pr)c ∪ (Pr)∇proc ,
(4) [ dg[t1 ] ∧ if {t1 , dg[t2 ], dg[t3 ]} ]if if t = if {t1 , t2 , t3 }, and
        n
(5) [ i=1    dg[ti ] ∧ ∇f (t1 , . . . , tn ) ]if if t = f (t1 , . . . , tn ) and f ∈ (Pr)proc ∪ (Pr)sel .
                                                                                                        

    Informally, dg[f (t1 , . . . , tn )] states that the result of a procedure (or selector) call
f (t1 , . . . , tn ) is determined iff all arguments are determined (as dg[t1 ] ∧ . . . ∧ dg[tn ] must
hold) and are in the domain of f (as ∇f (t1 , . . . , tn ) must hold).
    The body of domain procedure ∇ f of a procedure f is obtained as the weakly normalized
determination guard of the body of procedure f . The body of domain procedure ∇sel j of a
selector sel j is obtained as an equation expressing that sel j is applied to the constructor it
belongs to:

Definition 10 (Domain procedures)
(1) The domain procedure ∇ f of a procedure function f (x 1 :τ1 , . . . , xn :τn ):τ <= Rf with
    f ∈ (Pr)proc is defined as
                        function ∇ f (x1 :τ1 , . . . , xn :τn ):bool <= dg[Rf ]⊥wn .11
(2) The domain procedure ∇sel j of a selector sel j belonging to a constructor cons:τ1 × · · · ×
    τn → τ with selectors sel 1 , . . . , sel n is defined as
              function ∇sel j (x:τ ):bool <= eq(x, cons(sel 1 (x), . . . , sel n (x))).                   

   Weak normalization is used to satisfy the syntactical requirements of a procedure body,
viz. that each procedure body must be an if -normalized term. In addition, wn  eliminates
redundant if -conditionals which would blow up the procedure body. For example, for pro-
cedure
         function [infix] + (x, y:N):N <= if x = 0 then y else +(−(x) + y) end _if

10 ∇log(x ∗ y, b) must not be demanded as it follows from ∇log(x, b) ∧ ∇log(y, b), see (17) in Sect. 5.3.
11 See (11) in Sect. 5.2.1 for a refinement.



                                                                                               123
25    Page 18 of 48                                                                                            C. Walther

     ] is obtained as
dg[R+

            if {if {true, true, false},
               if {x = 0,
                  true,
                  if {if {true, x = +(−(x)), false}, if {true, ∇+(−(x), y), false}, false}},
               false}

and weak normalization yields dg[R+           ] wn as if {x = 0, true, ∇+(−(x), y)}.
                                                 ⊥
   As a domain procedure ∇ f is synthesized only after termination of its mother procedure f
has been verified, domain procedure ∇ f terminates as the recursive calls in f and ∇ f coincide
because ∇ f (t1 , . . . , tn ) ⇒+                                                     +                        
                                Pr ∇ f (t1 , . . . , tn ) entails f (t1 , . . . , tn ) ⇒Pr · · · f (t1 , . . . , tn ) · · ·
for all monomorphic ground terms t1 , . . . , tn .
   A domain procedure satisfies the following properties:

Theorem 2 Let Pr be a terminating L-program, let τi ∈ types[Pr] and let  be some type
substitution with (τi ) ∈ mtypes[Pr] for each i ∈ {1, . . . , n}.
   (1) If function f (x1 :τ1 , . . . , xn :τn ):τ <= Rf is a procedure of Pr with f ∈ (Pr)proc ,
then for each substitution λ with λ(xi ) ∈ T ((Pr)c )(τi ) for each i ∈ {1, . . . , n}

       (i) λ(∇ f (x1 , . . . , xn ))⇓Pr ∈ {true, false} ,
       (ii) λ(∇ f (x1 , . . . , xn )) ⇒!Pr true  λ(f (x1 , . . . , xn ))⇓Pr ∈ T ((Pr)c )(τ ) .
   (2) If sel j is a selector of Pr belonging to a constructor cons:τ1 × · · · × τn → τ with
selectors sel 1 , . . . , sel n and x ∈ Vτ , then for each substitution λ with λ(x) ∈ T ((Pr)c )(τ )

         (i) λ(∇sel j (x))⇓Pr ∈ {true, false} ,
         (ii) λ(∇sel j (x)) ⇒!Pr true  λ(sel j (x))⇓Pr ∈ T ((Pr)c )(τ j ) .

Proof See Appendix 8.1.                                                                                                 
                                                                                                                        

    A domain procedure is completely defined by Theorem 2(1.i, 2.i) and consequently no
domain procedure is generated for a domain procedure. By Theorem 2(1.ii, 2.ii), a domain
procedure provides a sufficient requirement for the absence of stuck terms when comput-
ing a procedure or selector call with the interpreter. See Sect. 5.2 for examples of domain
procedures.
    As a consequence of Theorem 2, the computation of the determination guard of a
monomorphic ground term t by the interpreter never yields a stuck term and—if computed
to true—entails that computation of t does not result in a stuck term either:

Corollary 3 Let Pr be a terminating L-program and let t ∈ T ((Pr)) be an if -normalized
ground term of monomorphic type. Then

         (1) dg[t]⇓Pr ∈ {true, false} and (2) dg[t] ⇒!Pr true  t⇓Pr ∈ T ((Pr)c ).

Proof See Appendix 8.1.                                                                                                 
                                                                                                                        

5.1 Safe Procedures and Programs

However, dg[t] ⇒!Pr true is not a necessary requirement for the absence of stuck terms when
evaluating a monomorphic ground term t with the interpreter.

123
Reasoning About Incompletely Defined Programs                                          Page 19 of 48   25


Example 2 (i) We find t1 := eq(∅, 0::tl(∅)) ⇒Pr false with computation rule (4)
of Fig. 4, but dg[t1 ] = [. . . ∧ ∇tl(∅) ∧ . . .]if by Definition 9(3,5) and ∇tl(∅) ⇒+      Pr
eq(∅, hd(∅)::tl(∅)) ⇒Pr false with Definition 10(2) and computation rule (4).
     (ii) We find t2 := hd(0::tl(∅)) ⇒Pr 0 with computation rule (5) of Fig. 4, but dg[t2 ] =
[· · · ∧ ∇tl(∅) ∧ · · · ]if ⇒!Pr false like in (i).                                         

    The problem is caused by computation rules (4) and (5) of Fig. 4: Computation of equation
and selector calls is not strict as rules (4) and (5) do not demand that the arguments of eq(. . .)
and sel j (. . .) are constructor ground terms. Hence stuck term tl(∅) does not result in a stuck
term upon computation of eq(∅, 0::tl(∅)) and hd(0::tl(∅)) in Example 2. Non-strictness
does not spoil soundness because each monomorphic ground term denotes by the semantics
given by Definition 6 and termination is demanded.
    Strict versions (4 ) and (5 ) of computation rules (4) and (5) are obtained by deman-
ding that the constructor arguments t1 , . . . , tn , s1 , . . . , sm in the rules are constructor ground
terms. By the strictness requirement, terms t1 and t2 of Example 2 now become stuck terms
as no computation rule applies. Rules (4 ) and (5 ) do not apply in particular because tl(∅)
is not constructor ground. But worse, computation rule (4 ) makes the determination guard
and domain procedures useless: Now e.g. dg[hd(0::tl(∅))] ⇒!Pr eq(∅, hd(∅)::tl(∅)) ∈                     /
{true, false} because neither computation rule (4 ) nor any other computation rules applies,
hence Theorem 2(1.i, 2.i) and Corollary 3(1) in turn do not hold.
    However, it is a bad programming style to use stuck terms like tl(∅) at irrelevant argument
positions of constructors in a term. We call those terms unsafe where we define:

Definition 11 (Safe terms) Let Pr be a terminating L-program and let t ∈ T ((Pr )) be an
if -normalized ground term of monomorphic type. Then t is safe iff
                                    t⇓Pr ∈ T ((Pr)c )
                                                                                                      (8)
                              c-path[t, π] ⇒ ! true  dg[t ] ⇒! true ,
                   π ∈Occ (t)
                         safe                Pr           |π  Pr

where Occsafe (t) := {π ∈ Occ(t) | t|π = f (. . .) for some f ∈ (Pr)proc ∪ (Pr)sel }.
   An if -normalized term s ∈ T ((Pr ), V ) is safe iff each monomorphic constructor
ground instance t of s is safe. An if -normalized term s is unsafe iff s is not safe.    

   Definition 11 vacuously applies to stuck terms, i.e. each stuck term t is safe as t⇓Pr ∈
                                                                                          /
T ((Pr)c ). An if -normalized term s is unsafe iff s has some monomorphic constructor
ground instance t such that
       (1) t⇓Pr ∈ T ((Pr)c ), (2) c-path[t, π] ⇒!Pr true, and (3) dg[t|π ] ⇒!Pr false
for some π ∈ Occsafe (t), cf. Corollary 3(1). Computation of an unsafe monomorphic ground
term t does not result in a stuck term by (1), but t has a subterm t|π whose determination guard
is computed to false by (3), where the computation of t|π is not disabled upon computation
of t by (2).

 Example 3 (i) s1 := eq(k, i::tl(k)) is unsafe because it has a monomorphic constructor
     ground instance t1 := eq(∅, 0::tl(∅)) such that (1) t1 ⇒!Pr false, (2) c-path[t1 , 2 · 2] =
     ∅ ⇒!Pr true and (3) dg[t1|2·2 ] = dg[tl(∅)] ⇒!Pr false.
(ii) s2 := hd(i::tl(k)) is unsafe because it has a monomorphic constructor ground instance
     t2 := hd(0::tl(∅)) such that (1) t2 ⇒!Pr 0, (2) c-path[t2 , 1 · 2] = ∅ ⇒!Pr true and (3)
     dg[t2|1·2 ] = dg[tl(∅)] ⇒!Pr false.

                                                                                            123
 25   Page 20 of 48                                                                                C. Walther


(iii) s3 := if {false, x/y, y} is safe because for each constructor ground instance t3 :=
      if {false, q/r , r } of s3 , t3 ⇒!Pr r , Occsafe (t3 ) = {2} but c-path[t3 , 2] = {false} ⇒!Pr false.
(iv) s4 := if {eq(y, 0), x, − (x) − − (y)} is safe because for each constructor ground instance
      t4 := if {eq(r , 0), q, − (q) − − (r )} of s4 with not(gt(r , q)) ⇒!Pr true, (t4 )⇓Pr ∈
      T ((Pr)c ), c-path[t4 , π] = {not(eq(r , 0))} for each π ∈ Occsafe (t4 ) = {3, 3 · 1,
      3 · 2} and not(eq(r , 0)) ⇒!Pr true entails
  • dg[t4|3 ] = [ dg[− (q)] ∧ dg[− (r )] ∧ ∇− (− (q), − (r )) ]if ⇒!Pr true,11
  • dg[t4|3·1 ] = dg[− (q)] = [ dg[q] ∧ ∇ − (q) ]if ⇒+            + −         !
                                                      Pr eq(q, ( (q)) ⇒Pr true, and
                     −                    −          +          +  −        !
  • dg[t4|3·2 ] = dg[ (r )] = [ dg[r ] ∧ ∇ (r ) ]if ⇒Pr eq(r , ( (r )) ⇒Pr true.
 The safeness requirement of Definition 11 is satisfied for gt(r , q) ⇒!Pr true as well because
 (t4 )⇓Pr ∈
          / T ((Pr)c ) in this case.                                                        
    Safeness exactly characterizes the monomorphic ground terms t which are computed to
 a constructor ground term and yield dg[t] ⇒!Pr true:
 Theorem 4 Let Pr be a terminating L-program and let t ∈ T ((Pr )) be an if -normalized
 ground term of monomorphic type. Then
                                                          dg[t] ⇒!Pr true.
                          t is safe ∧ t⇓Pr ∈ T ((Pr)c ) 
 Proof See Appendix 8.2.                                                                                   
                                                                                                           
    By presence of unsafe terms, domain procedure ∇ f is not necessarily a decision procedure
 for the domain of a procedure f . For instance, domain procedure
                 function ∇fail(i:@T , k:list[@T ]):bool <= (k = hd(k)::tl(k))
 is synthesized for procedure
                      function fail(i:@T , k:list[@T ]):@T <= hd(i::tl(k))
 whereas true would be the “right” procedure body for ∇fail: For example, ∇fail(0, ∅) ⇒Pr
 (∅ = hd(∅)::tl(∅)) ⇒Pr false but fail(0, ∅) is not a stuck term because fail(0, ∅) ⇒Pr
 hd(0::tl(∅)) ⇒Pr 0, cf. Example 2(ii). We call a procedure like fail unsafe where we define:
 Definition 12 (Safe procedures and programs) A procedure function f (x 1 :τ1 , . . . , xn :τn ):
 τ <= Rf of a terminating L-program Pr is safe iff Rf is safe. A terminating L-program Pr
 is safe iff each procedure of Pr is safe.                                                    
    For instance, procedure “−” from Fig. 2 is safe as demonstrated by Example 3(iv), whereas
 procedure fail is unsafe as shown with Example 3(ii).
    If a function call from a safe program is computed to a constructor ground term, then the
 corresponding domain procedure call is computed to true. Hence each domain procedure of
 a safe L-program is a decision procedure for the domain of its mother procedure:
 Theorem 5 Let Pr be a terminating and safe L-program, let τi ∈ types[Pr] and let  be a
 type substitution with (τi ) ∈ mtypes[Pr] for each i ∈ {1, . . . , n}.
    (1) If function f (x1 :τ1 , . . . , xn :τn ):τ <= Rf is a procedure of Pr with f ∈ (Pr)proc ,
 then for each qi ∈ T ((Pr)c )(τi ) with i ∈ {1, . . . , n}
            (i) ∇ f (q1 , . . . , qn )⇓Pr ∈ {true, false} ,
            (ii) ∇ f (q1 , . . . , qn ) ⇒!Pr true 
                                                   f (q1 , . . . , qn )⇓Pr ∈ T ((Pr)c )(τ ) .

 11 See Fig. 6 for the definition of ∇−.



 123
Reasoning About Incompletely Defined Programs                                               Page 21 of 48    25


   (2) If sel j is a selector of Pr belonging to a constructor cons:τ1 × · · · × τn → τ, then for
each q ∈ T ((Pr)c )(τ )
               (i) ∇sel j (q)⇓Pr ∈ {true, false} ,
               (ii) ∇sel j (q) ⇒!Pr true 
                                          sel j (q)⇓Pr ∈ T ((Pr)c )(τ j ) .

Proof (1) Statement (i) and the “ ”-part of (ii) follow from Theorem 2. For proving the
“ ”-part of (ii) we find that f (q1 , . . . , qn )⇓Pr ∈ T ((Pr)c )(τ ) entails dg[f (q1 , . . . , qn )]
⇒!Pr true by Theorem 4 as Pr is safe. Hence ∇ f (q1 , . . . , qn ) ⇒!Pr true because

                 dg[f (q1 , . . . , qn )] ⇒!Pr true
         iff         n
                 [ i=1     dg[qi ] ∧ ∇f (q1 , . . . , qn ) ]if ⇒!Pr true   ; by Definition 9(5)
         iff     ∇ f (q1 , . . . , qn ) ⇒!Pr true                          ; by Definition 9(3).
(2) is proven in the same way.                                                                                
                                                                                                              

    Unsafeness results from unsafe terms in the body of a procedure, viz. terms of form eq(t, s)
and sel(t) such that t and/or s can be computed to terms of form cons(. . .) with some stuck
argument, cf. Example 2. We consider the use of these terms as a bad programming style
rather than a deficiency of our proposal.
    One may think of analyzing a procedure for safeness, but safeness of procedures even is not
semi-decidable: Unsafeness of a procedure function f (x1 :τ1 , . . . , xn :τn ):τ <= Rf is semi-
decidable as it is enough to replace the type variables in τi with nat yielding monomorphic
types ηi and then to enumerate the elements (q1 , . . . , qn ) of T ((Pr)c )η1 ×· · ·×T ((Pr)c )ηn
to test for
                f (q1 , . . . , qn )⇓Pr ∈ T ((Pr)c )(τ ) ∧ ∇ f (q1 , . . . , qn ) ⇒!Pr false               (9)
until some (q1 , . . . , qn ) satisfying (9) is found. To test for safeness,
                f (q1 , . . . , qn )⇓Pr ∈ T ((Pr)c )(τ )  ∇ f (q1 , . . . , qn ) ⇒!Pr true               (10)
must be proved for each element (q1 , . . . , qn ) of T ((Pr)c )η1 × · · · × T ((Pr)c )ηn , but this
is undecidable by Rice’s Theorem. Therefore Theorem 5 seems not that useful at first glance
as it is based on a non semi-decidable notion. But we dare to say that no one writes an unsafe
procedure if she does not intend to do so. So far, we never encountered an unsafe procedure
in our case studies with  eriFun (see [26] for a collection of case studies computed with
the system). Except for procedure fail, each terminating procedure defined in this article is
safe as well.

5.2 Optimization of Domain Procedures

Domain procedures of procedures are highly redundant as their bodies contain unnecessary
recursive calls and unnecessary calls of other procedures. As domain procedures are used to
formulate L-lemmas like (7), calls of domain procedures appear in proof obligations and the
workload of the system is reduced if unnecessary procedure calls are eliminated.

5.2.1 Simplification of the Procedure Body

It is advantageous to use weak simplification ws  instead of weak normalization wn 
when generating the body of a domain procedure. In particular, conditions created by the

                                                                                                 123
25   Page 22 of 48                                                                     C. Walther




Fig. 6 Domain procedure ∇− of procedure “−” from Fig. 2




Fig. 7 Simplified domain procedure ∇/ of procedure “/” from Fig. 2



determination guard of a subterm t of a procedure body may be verified or falsified by
conditions in the context of t. We therefore redefine the domain procedure ∇f of a procedure
function f (x1 :τ1 , . . . , xn :τn ):τ <= Rf by

                     function ∇ f (x1 :τ1 , . . . , xn :τn ):bool <= dg[Rf ]⊥ws           (11)
which is a sound optimization step as AX Pr  ∀x1 :τ1 , . . . , xn :τn dg[Rf ]⊥wn ≡ dg[Rf ]⊥ws
by soundness of .
   For instance, the body of domain procedure ∇/ initially contains a call ∇−(x, y) of domain
procedure ∇− displayed in Fig. 6. As domain procedure ∇− computes the ≥-relation, we
formulate an L-lemma
           lemma x ≥ y → ∇− (x, y) <= ∀x, y:N if {y > x, true, ∇− (x, y)}                  (12)
(proved automatically by induction) so that weak simplification can use (12) to eliminate
procedure call ∇− (x, y) in the body of domain procedure ∇/, see Fig. 7. Elimination of
recursive calls in result terms (see Sect. 5.2.2) then finally yields
                            function ∇/(x, y:N):bool <= ¬ y = 0.
Domain procedure function ∇mod(x, y:N):bool <= ¬ y = 0 is obtained with the same
reasoning.
   The body of domain procedure ∇log initially contains the procedure calls ∇mod(x, b)
and ∇/(x, b) as the body of procedure log from Fig. 3 contains the procedure calls (x mod b)
and x/b. Both domain procedure calls are replaced with ¬ b = 0 by weak simplification in
the body of domain procedure ∇log, and then with true in turn as ¬ b = 0 follows from the
context ¬ 2 > b of both procedure calls, see Fig. 8.
   Weak simplification ws  instead of simplification  is used because unfolding calls of
recursively defined procedures does not contribute to optimization of domain procedures.
But domain procedures are quite often non-recursively defined—initially or after recursion
elimination—and symbolic execution of calls of non-recursively defined procedures like
∇mod and ∇/ in the ∇log-example supports optimization.
   From our experience, incompletely defined procedures should only be used if needed.
Procedure “−” from Fig. 2 is an example. It is not necessary to let x − y indetermined if

123
Reasoning About Incompletely Defined Programs                               Page 23 of 48   25




Fig. 8 Simplified domain procedure ∇log of procedure log from Fig. 3




Fig. 9 Alternative definition of procedure “−”

x < y. An alternative definition of procedure “−” is displayed in Fig. 9. As this procedure
is completely defined and therefore function ∇− (x, y:N):bool <= true is obtained (after
recursion elimination), L-lemma (12) must not be provided by a user to enable simplifica-
tion of the body of the domain procedures ∇/ and ∇mod. In fact, we used the alternative
definition of procedure “−” in all our case studies and gave the definition from Fig. 2 only
for demonstration purposes.

5.2.2 Recursion Elimination

Weak simplification does not eliminate all redundancies in the body of a domain procedure.
Quite often, recursive calls can be eliminated thus easing subsequent proofs. We implement
2 methods to this effect.
Recursive Calls in Conditions
If a procedure f has a recursive call in a condition, domain procedure ∇f must have a
recursive call in a condition as well. Consider e.g. data type
        structure tree[@T ] <= tip, node(left:tree[@T ], key:@T , right:tree[@T ])
and procedure ∈ with domain procedure ∇∈ of Fig. 10. Although we have different base
results in ∇∈, both recursive calls can be replaced with true: As procedure ∈ and therefore
domain procedure ∇∈ terminate, condition ∇∈(i, left(t)) must be computed to true when
calling domain procedure ∇ ∈ as no other base result is available upon this computation.
Hence base result false is never obtained, and therefore we receive
                        function ∇∈(i:@T , t:tree[@T ]):bool <= true
stipulating that procedure ∈ is completely defined.

                                                                                 123
25    Page 24 of 48                                                                    C. Walther




Fig. 10 (i) Procedure ∈ and (ii) domain procedure ∇∈




Fig. 11 (i) Procedure fib and (ii) domain procedure ∇fib


    Recursive calls in conditions of ∇f not only arise from procedures f with recursive calls
in conditions, but also from procedures with multiple recursive calls or with nested recursions
in a result term.
    Consider, for instance, procedure fib with domain procedure ∇fib from Fig. 11. When
calling ∇fib(n), ∇fib(− (n)) must be evaluated to true as no other base result is available so
that base result false is never obtained. Hence we obtain
                                 function ∇fib(n:N):bool <= true.
   For the Ackermann function and its domain procedure from Fig. 12, computation of
∇ack(x,− (y)) either yields true or results in calls of ∇ack(− (x), 1) or ∇ack(x,− (y)). Further
instances of ∇ack(− (x), 1) or ∇ack(x,− (y)) may be called in the latter case until computa-
tion stops with the only available base result true. Hence base result false is never obtained,
yielding
                               function ∇ack(x, y:N):bool <= true.
     Soundness of these optimizations is proved with
Theorem 6 Let function ∇f (x1 :τ1 , . . . , xn :τn ):bool <= R∇f be a domain procedure in a
terminating L-program Pr and let

123
Reasoning About Incompletely Defined Programs                                                   Page 25 of 48   25




Fig. 12 (i) Procedure ack and (ii) domain procedure ∇ack



(1) Occ∇fcond be all occurrences ρ ∈ Occ(R ) such that
                                                       ∇f
    R∇f |ρ = if {∇ f (θρ·1 (x1 ), . . . , θρ·1 (xn )), sρ·2 , false} where
(2) sρ·2 = if {f (θρ·1 (x1 ), . . . , θρ·1 (xn )), ∇ f (θγ (x1 ), . . . , θγ (xn )), true} or
    sρ·2 = if {f (θρ·1 (x1 ), . . . , θρ·1 (xn )), true, ∇ f (θγ (x1 ), . . . , θγ (xn ))} or
    sρ·2 = ∇ f (θγ (x1 ), . . . , θγ (xn )), and
(3) R∇f |π ∈ {true, ∇f (θπ (x1 ), . . . , θπ (xn ))} for each
    π ∈ Occ∇f res \{ρ · 3 ∈ Occres | ρ ∈ Occcond }.
                                      ∇f               ∇f

Then [∀x1 :τ1 , . . . , xn :τn ∇ f (x1 , . . . , xn ) ≡ true] ∈ ThPr .

Proof See Appendix 8.3.                                                                                         
                                                                                                                

    The body of a domain procedure which satisfies the requirements of Theorem 6 (as the
initial versions of ∇∈, ∇fib and ∇ack do) can be soundly replaced with true. Theorem 6
applies in particular if Occ∇f       cond = ∅. Then each base result in the body of domain procedure

∇f equals true by (3) and procedure body R∇f can be replaced with true. This special case
applies for completely defined procedures like addition, multiplication, list concatenation
and reversal etc.
    If true is replaced with false in requirements (2) and (3) of Theorem 6, then
[∀x1 :τ1 , . . . , xn :τn ∇ f (x1 , . . . , xn ) ≡ false] ∈ ThPr can be proved by a similar argumenta-
tion. Domain procedure function ∇zero(x:N):bool <= false of procedure zero from Sect. 3.3
is obtained by this optimization and states that calls of zero yield indetermined results only.

Recursive Calls in Result Terms
Domain procedures with identical base results or recursive calls in conditions are not the
only cases where recursive calls are superfluous. Consider, for instance, procedure last with
domain procedure ∇last of Fig. 13. If a call of ∇last(k) results in a recursive call ∇last(tl(k)),
then list k has n + 2 elements, hence list tl(k) has n + 1 elements. So the list in the argument
of ∇last is shortened by one element with each recursive call until a singleton list is obtained
yielding the base result true. In other words: If procedure call ∇last(k) results in a recursive
call ∇last(tl(k)), then ∇last(tl(k)) may necessitate further recursive calls but eventually must

                                                                                                     123
25   Page 26 of 48                                                                           C. Walther




Fig. 13 (i) Procedure last and (ii) domain procedure ∇last


end with the base result true. This fact is formally expressed by
               ∀k:list[@T ] k = ∅ ∧ tl(k) = ∅ →
                                                                                                  (13)
                (tl(k) = ∅ ∧ tl(tl(k)) = ∅) ∨ (tl(k) = ∅ ∧ tl(tl(k)) = ∅).
Formula (13) is called a recursion elimination formula for ∇last and is easily proved by weak
normalization.12 The proof of (13) justifies replacement of the recursive call ∇last(tl(k))
in the body of domain procedure ∇last with true. Subsequent weak normalization of the
modified procedure body then yields
                         function ∇last(k:list[@T ]):bool <= ¬ k = ∅.
   In general, there are 2 recursion elimination formulas to investigate for each recursive call,
viz. for base results = true and for base results = false. We did not consider the false-case
for ∇last as the true-case has been proven so that the recursion elimination formula for the
false-case cannot hold.
   For domain procedure ∇− of Fig. 6, the true-case recursion elimination formula reads as
              ∀x, y:N y = 0 ∧ x = 0 → (−(y) = 0 ∧ −(x) = 0) ∨ −(y) = 0.                           (14)
But the recursive call in ∇− cannot be replaced with true as the Disprover computes the
counter example x := 1 and y := 2 for (14). Therefore the false-case recursion elimination
formula
     ∀x, y:N y = 0 ∧ x = 0 → (−(y) = 0 ∧ −(x) = 0) ∨ (−(y) = 0 ∧ −(x) = 0) (15)
is considered. But the Disprover comes up with a counter example x := y := 1 also for (15),
and consequently the recursive call in ∇− cannot be eliminated. Recursion is needed in fact
because x − y is determined iff x ≥ y iff ∇− (x, y), but ≥ cannot be defined non-recursively.
    The recursion in domain procedure ∇log from Fig. 8 is also needed, and the true-case
recursion elimination formula is refuted with x := 6 and b := 2 and x := b := 2 is a counter
example for the false-case.
    Elimination of a recursive call may also fail if a domain procedure has two or more
recursive result terms because a recursive call must not necessarily result in an instance of
the same recursive call. For example, consider procedure min for computing the minimum of
a non-empty number list and its domain procedure ∇min in Fig. 14. The Disprover refutes the
recursion elimination formulae for the first recursive call with k1 := 1::0::1::∅ because a call

12 We write recursion elimination formulas with the usual mathematical notation instead of the formally
required boolean terms to ease readability.


123
Reasoning About Incompletely Defined Programs                                          Page 27 of 48   25




Fig. 14 (i) Procedure min and (ii) domain procedure ∇min



of ∇min(k1 ) results in a call of the first recursion but subsequently in a call of the second one.
Likewise the system disproves the recursion elimination formulae for the second recursive
call with k2 := 1::1::0::∅ because a call of ∇min(k2 ) results in a call of the second recursion
but afterwards in a call of the first one.
   The remedy is to consider a non-empty cluster of recursive calls in the body of a domain
procedure and to demand that each recursive call from the cluster either results in some
recursive call of the cluster or in one of the base results b, where b = true for each of these
result terms or b = false for all of them. If so, all recursive calls of the cluster can be soundly
replaced with b.
   For instance, when having both recursive calls of domain procedure ∇min in the cluster,
the recursion elimination formula for b = true is obtained as displayed in Fig. 15, and is
easily proved by weak normalization.13 Hence both recursive calls in ∇min can be soundly
replaced with true, and

                           function ∇min(k:list[N]):bool <= ¬ k = ∅

is obtained after weak normalization of the modified procedure body as the final definition
of ∇min.

Definition 13 (Recursion elimination formulae) Let function ∇f (x1 :τ1 , . . . , xn :τn ):bool <=
R∇f be a domain procedure in a terminating L-program Pr with

        rec ⊂ Occres , i.e. procedure ∇f has no recursive call in a condition, and
(1) Occ∇f        ∇f
(2) Occb ⊂ Occ∇fbase such that R
                                   ∇f |π = b for each π ∈ Occb , where b = true for each
    π ∈ Occb or b = false for each π ∈ Occb .

13 We have replaced tl(hd(k)::tl(tl(k))) with tl(tl(k)) in Fig. 15 for saving space.



                                                                                            123
25   Page 28 of 48                                                                        C. Walther




Fig. 15 True-case recursion elimination formula for procedure ∇min


                             rec and each b ∈ {true, false} define the recursion elimination
Then each subset  = ∅ of Occ∇f
formula Re,b :=
                                                                         
                                →                                       θρ ()         (16)
           ρ∈        ∈c-path[R∇f ,ρ]          π ∈∪Occb        ∈c-path[R∇f ,π ]
                                                                                           if
where R∇f |ρ = ∇f (θρ (x1 ), . . . , θρ (xn )) for each ρ ∈ Occ∇f
                                                               rec .                             

   Recursion elimination formula (16) expresses that each recursive result term
∇f (θρ (x1 ), . . . , θρ (xn )) in ∇f belonging to cluster  either necessitates a further recursive
call ∇f (θπ (θρ (x1 )), . . . , θπ (θρ (xn ))) belonging to the cluster or yields base result b.
   Elimination of recursive result terms in a domain procedure is a sound optimization step
as proven with

Theorem 7 Let all notions be given as in Definition 13 and let R∇f ,b be obtained from
procedure body R∇f by replacement of each recursive call ∇f (θρ (x1 ), . . . , θρ (xn )) with b
for each ρ ∈  and subsequent weak normalization. Then
                          [ ∀x1 :τ1 , . . . , xn :τn Re,b ≡ true ] ∈ ThPr ,
                                                     
                         [ ∀x1 :τ1 , . . . , xn :τn R∇f ≡ R∇f ,b ] ∈ ThPr .

Proof See Appendix 8.3.                                                                           
                                                                                                  

By Theorem 7, the body R∇f of domain procedure ∇f can be soundly replaced with the
optimized procedure body R∇f ,b if the recursion elimination formula Re,b has been proved.
From our experience with many case studies, true recursion elimination formulae usually
are valid and easily proved by the Symbolic Evaluator.

5.3 Well-Formed Lemmas and Refined Theories

As already discussed in the introduction and in Sect. 3.4, computation of monomorphic
constructor ground instances of verified L-lemmas by the interpreter may result in runtime
errors (represented by stuck terms) instead of true, cf. Example 1. The remedy to eliminate
this disadvantage of our semantics is to remove certain formulas from ThPr . We use the
determination guard to filter out the unwanted statements of ThPr and define to this effect:

Definition 14 (Lemma guard, well-formedness, refined theory Th∗Pr ) Let Pr be a terminating
L-program and let  be an L-lemma with lemma body [∀x 1 :τ1 , . . . , x n :τn b]. Then the lemma
guard ∇ of  is defined as [∀x1 :τ1 , . . . , xn :τn dg[b]⊥ws ] and L-lemma  is well-formed iff

123
Reasoning About Incompletely Defined Programs                                           Page 29 of 48    25


∇ is true. These notions are correspondingly defined for specification formulas ϕ :=
[∀x1 :τ1 , . . . , xn :τn b ≡ true] where ∇ϕ is defined as [∀x1 :τ1 , . . . , xn :τn dg[b]⊥ws ≡ true]
and ϕ is well-formed iff ∇ϕ ∈ ThPr . The refined theory Th∗Pr of Pr is given as {ϕ ∈ ThPr |
∇ϕ ∈ ThPr }.                                                                                       
   The refined theory Th∗Pr excludes each specification formula from ThPr which is not well-
formed. Specification formula ϕ corresponding to L-lemma “ y = 0 ∧ x/z > x/y → y > z”
from Fig. 2 is a witness for such a case because the lemma guard [∀y, z:N y = 0 → z = 0 ]
does not hold and the Disprover comes up with the counter example y := 1 and z := 0.14
For the statements (1), (2), (3), (5), (7) of Fig. 1, [ 0 = 0 ] is obtained as the lemma guard,
formulae (4) and (6) yield [ ∅ = hd(∅)::tl(∅) ] and [ ∀n, m:N n = 0 ∧ m = 0 ] is the lemma
guard of (8). As all lemma guards are false, none of the statements in Fig. 1 is well-formed
and consequently the corresponding specification formulas are not in Th∗Pr . The stuck terms
of Example 1 and statement (2) about procedure zero are not well-formed too.
   An implementation might consider an L-lemma  for verification only if well-formedness
of  has been proven before. It is advantageous to call the Disprover with the lemma guard
before verifying well-formedness as this test avoids proof attempts for false formulas (often
resulting from writing errors or forgotten conditions). Usually a lemma guard is obtained as
true or false, i.e. symbolic evaluation and disproving is enough in most cases to (dis)prove
well-formedness. Nevertheless it may happen in the positive case that induction is needed
like for the lemma guard (‡) [ ∀n:N ∇−(n, n) ] of (†) [ ∀n:N n − n = 0 ].15 As (‡) can be
verified, (†) is well-formed and the corresponding specification formula is in Th∗Pr as (†) can
be verified as well. Induction is also needed to verify the lemma guard
                    ∀b, x, y:N ∇log(x, b) ∧ ∇log(y, b) → ∇log(x ∗ y, b)                                 (17)
computed for L-lemma (7) from Sect. 5.
   The interpreter never comes up with a stuck term if applied to a monomorphic constructor
ground instance of a well-formed L-lemma. Hence absence of runtime errors is guaranteed
when well-formedness is proved. If a well-formed L-lemma is verified, then each monomor-
phic constructor ground instance of the L-lemma is computed to true:
Theorem 8 Let Pr be a terminating L-program and let ϕ := [∀x 1 :τ1 , . . . , xn :τn b ≡ true].
Then for each monomorphic constructor ground instance λ(b) of b
(1) ∇ϕ ∈ ThPr  λ(b)⇓Pr ∈ {true, false} , and
(2) ϕ ∈ Th∗Pr  λ(b) ⇒!Pr true.
Proof (1) Let λ be a substitution with λ(xi ) ∈ T ((Pr )c )(τi ) for any type substitution 
with (τi ) ∈ mtypes[Pr] for each i ∈ {1, . . . , n}. Then λ(dg[b]⊥ws )⇓Pr = λ(dg[b])⇓Pr
by soundness of  and λ(dg[b])⇓Pr = dg[λ(b)]⇓Pr by Definition 9(3) as λ({x1 , . . . , xn }) ⊂
T ((Pr )c ), hence λ(dg[b]⊥ws )⇓Pr = dg[λ(b)]⇓Pr . We find
                      (i) dg[λ(b)]⇓Pr ∈ {true, false} ,
                      (ii) dg[λ(b)] ⇒!Pr true  λ(b)⇓Pr ∈ {true, false}
by Corollary 3, therefore (†) dg [λ(b)] ⇒!Pr true by (i) and Lemma 3 because ∇ϕ :=
[∀x1 :τ1 , . . . , xn :τn dg[b]⊥ws ≡ true] ∈ ThPr , hence (1) holds by (ii). (2) If ϕ ∈ Th∗Pr ,
then λ(b) ⇒!Pr true by (†), (ii) and Lemma 3.                                               
                                                                                            

14 ϕ ∈ Th
        Pr holds for z = 0 in particular as y = 0 entails y > z, but ϕ ∈
                                                                       / ThPr if z = 0 instead of y = 0 is
demanded. Hence both y = 0 and z = 0 are required to obtain ϕ ∈ Th∗Pr .
15 See Fig. 6 for the definition of domain procedure ∇−.



                                                                                             123
25    Page 30 of 48                                                                                          C. Walther


   However, there are statements [∀x1 :τ1 , . . . , xn :τn b ≡ true] in ThPr which do not cause
stuck terms as λ(b) ⇒!Pr true for each monomorphic constructor ground instance λ(b) of b,
but are not well-formed and therefore not in Th∗Pr . L-lemma
                      lemma pointless <= ∀i:@T , k:list[@T ] hd(i::tl(k)) = i                                     (18)
obtained from Example 3(ii) is a witness for such a case as the lemma guard [ ∀k:list[@T ]
k = ∅ ] does not hold. We consider L-lemmas like (18) as examples of a bad specification
style rather than a deficiency of our proposal. The body of L-lemma (18) is an unsafe term,
and we can prove:

Lemma 4 Let Pr be a terminating L-program and let b ∈ T ((Pr), {x 1 , . . . , xn })bool with
λ(b) ⇒!Pr true for each monomorphic constructor ground instance λ(b) of b. If b is safe,
then ϕ := [ ∀x1 :τ1 , . . . , xn :τn b ≡ true] ∈ Th∗Pr .

Proof We find dg[λ(b)] ⇒!Pr true by Theorem 4 as safeness of b entails safeness of λ(b)
by Definition 11. Hence λ(dg[b]⊥ws ) ⇒!Pr true by soundness of  and Definition 9(3) as
λ({x1 , . . . , xn }) ⊂ T ((Pr )c ), therefore ∇ϕ ∈ ThPr by Lemma 2, and then ϕ ∈ Th∗Pr
because ϕ ∈ ThPr by Lemma 2.                                                           
                                                                                       

    Note that well-formedness entails safeness as well-formedness entails the conclusion of
criterion (8) of Definition 11. But safeness does not imply well-formedness because Defini-
tion 11 demands the truth of the conclusion of criterion (8) only for monomorphic ground
terms which are not computed to stuck terms. For instance,
                            lemma x − y ≤ x <= ∀x, y:N ¬ x − y > x                                                (19)
is safe as procedure “−” is safe, cf. Example 3(iv). But L-lemma (19) is not well-formed
as dg[¬ x − y > x]⊥ws = ∇− (x, y) and the Disprover comes up with a counter example
x := 0 and y := 1 for [∀x, y:N ∇− (x, y)], cf. Fig. 6.16
    Another example comes with
                 lemma x/x = 1 → x = 0 <= ∀x:N if {x/x = 1, true, x = 0}                                          (20)
which is not well-formed because the lemma guard is initially obtained as
∀x:N if {∇/(x, x), if {x/x = 1, true, true}, false} and weakly simplifies to [ ∀x:N x = 0 ].
But the contraposition of (20), viz.
                 lemma x = 0 → x/x = 1 <= ∀x:N if {x = 0, true, x/x = 1}                                          (21)
is well-formed because the lemma guard initially obtained as ∀x:N if {true,
if {x = 0, true, ∇/(x, x)}, false} weakly simplifies to true. The reason for this difference
is that AX Pr  ∀ . . . b1 ≡ b2 for boolean terms b1 and b2 does not entail AX Pr 
∀ . . . dg[b1 ] ≡ dg[b2 ]. A determination guard depends on the presentation of connecti-
ves, and we obtain for instance
                      dg[if {a, true, b}] = if {dg[a], if {a, true, dg[b]}, false},
                      dg[if {b, true, a}] = if {dg[b], if {b, true, dg[a]}, false}

16 One may be tempted to give a notion of a well-formed procedure similar to the notion of a well-formed
L-lemma by demanding (∗) [∀x1 :τ1 , . . . , xn :τn dg [R f ]⊥ws ≡ true] ∈ ThPr for a procedure function
 f (x1 :τ1 , . . . , xn :τn ):τ <= Rf with f ∈ (Pr)proc . However, well-formedness of procedures would be
a useless notion as (∗) just means [∀x1 :τ1 , . . . , xn :τn ∇ f (x1 , . . . , xn ) ≡ true] ∈ ThPr by (11), hence proce-
dure f would be well-formed iff f were completely defined.


123
Reasoning About Incompletely Defined Programs                                       Page 31 of 48    25


with AX Pr  if {a, true, b} ≡ if {b, true, a} but AX Pr  dg[if {a, true, b}] ≡ dg[if {b, true,
a}] because dg[a] ≡ dg[b] does not necessarily hold.
    The determination guard dg[t] of a term t is computed recursively with the determina-
tion guards dg[t  ] of the subterms t  of t, cf. Definition 9, and the result depends on the
order in which these subterms are considered. Hence the problem is not caused by using
if -conditionals to write connectives but also exists for the usual connectives where dg[a ∨ b]
differs from dg[b ∨ a].
    Whether different representations of equivalent formulae shall be taken into account when
computing a determination guard depends on the domain of discourse. If concerned with
pure logic, as e.g. in [19], a determination guard is needed which makes commutativity of
connectives explicit. We may define
            dg[if {a, true, b}] = if {dg[a], if {a, true, dg[b]}, if {dg[b], b, false}}             (22)
and then AX Pr  dg[if {a, true, b}] ≡ dg[if {b, true, a}]. The extended definition (22) yields
the lemma guards
                       if {∇/(x, x), if {x/x = 1, true, true}, if {true, x = 0, false}}
             ws +     if {x = 0, true, x = 0}
             ws !     true
for L-lemma (20) and
                     if {true, if {x = 0, true, ∇/(x, x)}, if {∇/(x, x), x/x = 1, false}}
           ws +     if {x = 0, true, x = 0}
           ws !     true
for L-lemma (21) thus proving well-formedness for both of them.
    However, we do not use this enhancement as it does not meet our intention when defin-
ing well-formedness: We use the lemma guard for guaranteeing absence of stuck terms
when computing monomorphic constructor ground instances of L-lemmas. But the extended
definition yields wrong results in our application because the constructor ground instance
if {0/0 = 1, true, 0 = 0} of L-lemma (20) is a stuck term although the extended lemma guard
for (20) yields true, whereas false is obtained correctly with the non-extended lemma guard.
The non-extended lemma guard of L-lemma (21) yields true instead and each constructor
ground instance of (21) is computed to true.

5.4 Implementation

If a procedure function f (x1 :τ1 , . . . , xn :τn ):τ <= Rf is submitted to the system,
(1) a syntax test for procedure f is performed, then (if successful),
(2) termination of procedure f is proved, then (if successful),
(3) domain procedure function ∇f (x1 :τ1 , . . . , xn :τn ):bool <= dg[Rf ]⊥ws is synthesized,
    and finally
(4) domain procedure ∇f is optimized.
   The implementation of step (3) is based on Definition 9 and the refinement (11) of Defini-
tion 10. Optimization step (4) is based on Theorems 6 and 7. The computation of dg[Rf ] is
fast as a determination guard is defined by structural recursion and runtime is proportional to
the size of procedure body Rf . The computation of dg[Rf ]⊥ws is fast as well because weak
simplification does not open calls of recursively defined procedures. Elimination of recur-
sive calls in conditions is fast as only syntactical properties of procedure body dg[Rf ]⊥ws

                                                                                            123
25   Page 32 of 48                                                                              C. Walther


are tested (cf. Theorem 6) and elimination of recursive calls in result terms (cf. Theorem 7)
usually is fast as well as true recursion elimination formulas can be proved by the Symbolic
Evaluator in most cases.
   For instance,   eriFun needs 1sec for processing a file with the procedures >, −, / and
log of Figs. 2 and 3 and needs 3sec if the proofs of L-lemma (7) and its lemma guard (17)
are computed in addition.17 The system needs less than 1sec for processing a file with the
procedures ∈, fib, ack, last and min of Figs. 10 –14. Time refers to computation of termination
proofs as well as generation and optimization of the domain procedures of the procedures in
the files including proofs and refutations of recursion elimination formulas.18
   To eliminate recursive calls in result terms, all non-empty subsets of Occ rec
                                                                              ∇f are considered
for a cluster  with decreasing cardinality: Let CL be the set of all non-empty subsets of
Occ rec
      ∇f . Then the recursion elimination formulas Re,b of Definition 13 are processed as
follows:
(∗) The Disprover is called with Re,true for some  ∈ CL with maximal cardinality;
(1) if successful, the Disprover is called with Re,false ;
     (a) if successful, CL := CL\ {}, recursion elimination halts if CL = ∅ and otherwise
         continues at (∗).
     (b) if not successful, simplification is applied to Re,false ;
           (i) if successful, each recursive call at an occurrence from  is replaced with false
               in procedure body dg[Rf ]⊥ws and CL := CL \ CL  , where CL  is the set of
               all clusters  of CL with  ⊂ . Recursion elimination halts if CL = ∅ and
               otherwise continues at (∗).
          (ii) if not successful, CL := CL\ {}, recursion elimination halts if CL = ∅ and
               otherwise continues at (∗).
(2) if not successful, simplification is applied to Re,true ;
     (a) if successful, each recursive call at an occurrence from  is replaced with true in
         procedure body dg[Rf ]⊥ws and CL := CL \ CL  . Recursion elimination halts if
         CL = ∅ and otherwise continues at (∗).
     (b) if not successful, the Disprover is called with recursion elimination formula Re,false ;
           (i) if successful, recursion elimination continues at (1.a).
          (ii) if not successful, recursion elimination continues at (1.b).
   If recursion elimination succeeds for some  ∈ CL, cf. steps (1.b.i) and (2.a), then the
subsets  of  need not to be considered subsequently because the recursive calls at each
occurrence of  are already replaced with true or false respectively, hence CL is set to
CL \ CL  . As the method considers only elements  of CL with maximal cardinality, the
largest clusters for which recursion elimination succeeds are obtained. Soundness of the
implementation is proved with Theorem 7.
   If a domain procedure ∇ f has k recursive calls, then (2k − 1) · 2 recursion elimination
formulas have to be considered by the system in the worst case, viz. if none of the recursive
calls in dg[Rf ]⊥ws can be eliminated. Consequently recursion elimination becomes unfeasible

17 This time includes computation time for the proofs of the 21 arithmetic L-lemmas which are required for
the proofs of (7) and (17).
18 Time is given for   eriFun 3.5 running under Windows 7 Enterprise with an INTEL Core i5-2520 M
2.50 GHz CPU using Java 1.8.0_311. The smallest time unit displayed in   eriFun’s Statistics Viewer
is 1 sec.


123
Reasoning About Incompletely Defined Programs                                      Page 33 of 48   25


for procedures with many recursive calls. For instance, one of our case studies contains a
domain procedure with 19 recursive result terms none of which can be eliminated, and
one will hardly find a machine which processes 1.048.574 recursion elimination formulas
within tolerable time. Therefore elimination of recursive result terms is restricted if k > N1
for a user changeable number N1 (set to 4 by default). Then only (k + 1) · 2 recursion
elimination formulas are considered, viz. for the clusters  := Occ rec  ∇f and  := {π} for
each π ∈ Occ rec∇f . If k > N 2 for a user changeable  number  N 2 >  N 1 (set to 8 by default),
elimination of recursive result terms is disabled at all.
   Recursion elimination formulas which neither are proved nor falsified in the above steps
may be proved or falsified interactively by the user. Alternatively she may press the Accept-
button in the system’s recursion elimination dialog if she does not care about elimination of
the surviving recursive calls.


6 Related Work

Reasoning about partial functions has a long history in the fields of programming
methodology, formal logic and automated reasoning. The notion of a determination guard
is attributed to Kleene [14] and (variants of) determination guards and domain procedures
appear (under different names) in several works on reasoning about partial functions, see e.g.
[15, 19] for further references. A huge amount of proposals for modelling partial functions
can be found in the literature, e.g. [2, 4, 5, 7–13, 15, 18, 19, 21, 22] (to mention only some
of them), and various logics have been developed to capture partiality adequately. There is
no royal road to reasoning about partial functions as each proposal bringing strength in one
respect shows weakness in another. The literature provides several challenges for a naïve
logic user, to wit
 • non-standard calculi and semantics,
 • different forms of equality in the same logic,
 • strong and weak forms of relational operators,
 • non-standard interpretations for logical operators,
 • invalidity of the law of excluded middle,
 • non-associativity of equivalence,
 • unusual theorems and non-theorems,
 • non-standard connectives and quantifiers,
 • notationally awkward languages,
 • …
   The work of Giesl [8] is an exception as it avoids those obstacles. Calculi are presented
which extend theorem proving by induction to work for non-terminating procedures as well.
The motivation for this (not implemented) proposal is to obtain machine support for proving
properties of partial functions with undecidable domain as e.g. theorems about a programming
language interpreter or algorithms developed for automated reasoning. Krauss [15] used a
similar approach and integrated it into the Isabelle system [20] where his proposal additionally
extends to higher order logic.19 If only total correctness can be proved as many verification
tools demand, auxiliary constructions are required to enforce termination of a program which
originally does not terminate. Such a workaround is unsatisfactory in principle because the

19 Isabelle also allows incomplete definitions by identifying an indetermined result with the symbol
arbitrary (corresponding to  in our setting) as well as by non-exhaustive pattern matching.


                                                                                        123
25   Page 34 of 48                                                                                 C. Walther


original program code is modified, hence logics as in [8, 15] are to be preferred over logics
which cannot be used without such makeshift solutions. But induction theorem provers hea-
vily rely on information obtained from termination analysis for guiding the prover when
searching for a proof. Without this guidance the need for user support increases.
    The proposals in [8, 15] come with a certain formal overhead which is justified as more
complicated proof problems can be solved. But if restricted to partial functions with decid-
able domain, incomplete definitions (also termed loosely specified or underspecified in the
literature) is the method of choice for modelling partiality. This is well recognized in the
automated reasoning community because logics, proof systems and heuristics for reasoning
about total functions apply with minor modifications. Advantages and disadvantages of this
approach are intensively debated in the literature, often discussing problems from a spe-
cific perspective. However, some caution is advisable to avoid misinterpretations when using
incompletely defined functions. The trap some authors step in is to ignore that a function’s
domain is decidable and to compute such a function with a non-terminating procedure.
    For instance, Schieder and Broy [22] define division by a non terminating procedure given
(in our notation) as
                           function [infix] ÷ (x, y:N):N <=
                           if y > x then 0 else +((x − y) ÷ y) end _if .
An interpreter does not halt when called with 1 ÷ 0, hence the result of procedure call 1 ÷ 0
is undefined. But if 1 ÷ 0 is considered as indetermined instead, then 1 ÷ 0 = +(1 ÷ 0) by
definition of ÷ which is in contradiction to ∀n:N n = +(n) as 1 ÷ 0 ∈ N because 1 ÷ 0 stands
for some (unknown) natural number. The deduction of this inconsistency is used in [22] to
argue against underspecification for modelling partiality. But division has a decidable domain
and can be computed by a terminating procedure as we did with procedure “/ ” of Fig. 2.
Then no inconsistency arises as [1/0 ≡ +(1/0) ] ∈ Th Pr (hence [1/0 ≡ +(1/0) ] ∈      / Th Pr by
consistency of Th Pr ) and neither [1/0 ≡ +(1/0) ] ∈ Th∗Pr nor [1/0 ≡ +(1/0) ] ∈ Th∗Pr by
the well-formedness requirement.
    Jones gives a similar example in [12] with expression (23) for defining a function subp
and another one in [11] “which suggest that this [underspecification] approach might be
problematic in a specification language”. A function f : Z → {0} is defined by f (i) :=
if i = 0 then 0 else f (i − 1) fi and Jones argues that the conclusion “ f (−1) = 0” might not
meet the intention of the definition. Then he discusses the (dis)advantages of (dis)allowing
data types with a single element. But non-termination is the problem here, rather than data
types with a single element. Written in our notation, one might define a data type single <= ♦
and a terminating procedure
                             function f (i: Z):single <=
                             if i = 0
                              then ♦
                              else if i > 0 then f (p(i)) else  end _if
                             end _if .
We can prove “ f (−1) = ♦”, in fact we can even prove [∀i: Z f (i) ≡ ♦] ∈ Th Pr . But neither
[ f (−1) ≡ ♦ ] ∈ Th∗Pr nor[ f (−1) ≡ ♦] ∈ Th∗Pr as ∇ f (i) yields false for each negative
integer i, hence none of the formulas is well-formed. However,     eriFun proves [ ∀i:Z
i ≥ 0 → f (i) ≡ ♦ ] ∈ Th∗Pr .20

                           
20 As types are disjoint in eriFun, i.e. T ((Pr )c ) ∩ T ((Pr )c )  = ∅ for monomorphic types η = η ,
                                                     η              η
we cannot define a data type corresponding to {0} and therefore use data type single instead. As a consequence


123
Reasoning About Incompletely Defined Programs                                           Page 35 of 48   25


    Gries and Schneider briefly discuss the advantages of underspecifications, viz.
simplicity and uniformity of concept and notation as well as the use of conventional first-
order logic when modelling partial functions [9]. A semantics is informally indicated which
corresponds to our definition of Th Pr . The need for the determination guard (denoted Dom in
the paper) to formulate predicates which represent the domain of a function by some formula
is informally discussed as well. Domain procedures do not appear in the paper. Termination
of underspecified procedures is not demanded which lead to inconsistencies as illustrated
above.
    Finn, Fourman and Longley investigate how to reason “conveniently but safely” about non-
terminating procedures in classical higher-order logic for the lambda theorem prover [7].
To this effect, domain predicates DOM  f are formulated for procedures f which correspond
to some extent to our domain procedures when restricted to the first-order case. A domain
predicate DOM  f of a procedure f is defined by a set of axioms which is generated according
to the cases of procedure f ’s definition. Additional axioms define the results of procedure
 f relative to the truth of the domain predicate DOM  f . There is no optimization of domain
predicates. Complete definedness is verified by proving DOM  f for any input. The semantics
satisfy statements (1)–(6) of Fig. 1 and are defined by assigning each procedure function
symbol f any total function extending the least fixed-point θ ∞  f of the functional given by the
procedure definition. The domain predicate DOM  f is assigned the characteristic function
of the domain of θ ∞  f . It is proved that these interpretations satisfy the axioms for domain
predicates as well as the axioms relating procedure definitions to domain predicates. Domain
predicates need not to terminate. Instead it is left to the user to guide the system to prove
statements about domain predicates in order to discharge certain premises from the procedure
axioms. Since procedures can be incompletely defined by non-exhaustive patterns, the notions
of definedness and determination are mixed up in one concept but “a non terminating program
is not the same as a program returning an unknown value, but our semantics is not capable
of reflecting this distinction” [7]. Consequently the synthesis of useful induction axioms and
control information for a theorem prover obtained from termination analysis is waived here.
    Without demanding termination for procedures, some substitute is needed to avoid incon-
sistencies. While the inference rules in [8, 15] are carefully designed to circumvent unsound
inferences, Manolios and Moore take another approach for ACL2 [18]. Instead of using
underspecification, a function f  is incompletely defined by giving axioms for f  . To
guarantee consistency, a terminating witness procedure f must be provided for accepting
the axioms in ACL2. Then it must be proved that procedure f satisfies the definition of func-
tion f  , which means to prove that the axioms for f  with f  replaced with f are theorems.
If so, inconsistency cannot result by the axioms for f  . For instance, a function log  might
be given by the axioms
      (1) ∀b, x:N 2 ≤ b ∧ x = 1 → log  (x, b) = 0,
      (2) ∀b, x:N 2 ≤ b ∧ x ≥ 2 ∧ (x mod b) = 0 → log  (x, b) = +(log  (x/b, b)).
These axioms are accepted if (1) and (2) can be proved with the calls of log  replaced with
calls of a terminating witness procedure as e.g. procedure log from Fig. 3. Once consistency
has been established this way, witness procedure f is disregarded when proving properties
of function f  . Using witness procedures, incompletely defined functions can be defined
without underspecification. In fact, this feature is stronger, i.e. it allows to prove more than

of disjointness, function symbols with arguments of type N cannot be used for functions with parameters of
type Z. For sake of readability, we dispense with the introduction of function symbols for Z and reuse the
corresponding function symbols which have been defined for N. Function symbol p : Z → Z stands for the
integer predecessor function.


                                                                                             123
 25   Page 36 of 48                                                                              C. Walther


 with underspecification. This is because only “procedure f satisfies the axioms of function
 f  ” is demanded, which is a weaker requirement than “t⇓ePr exists for each extension e of the
 computation calculus”, cf. Definition 4. For instance, a function null  may be incompletely
 defined with axiom
                           ∀x:N x = 0 → null  (x) = null  (null  (−(x)))
 using a procedure with result = 0 everywhere as witness procedure, whereas we cannot rea-
 son about the incompletely defined procedure null of Sect. 3.3 because of non-termination.
 As proved in [18], witness procedures always exist for tail recursive procedures. Conse-
 quently termination proofs are not needed for these procedures to guarantee consistency and
 a workaround by introducing counters (called clocks in the ACL2 community) to enforce
 termination is not needed. However, by dispensing with termination proofs—being it for
 procedures which are defined by axioms or for tail recursive procedures—relevant control
 information for guiding the theorem prover is lost, creating problems in another corner as
 “This is a two-edged sword. The clock argument makes the statement of theorems more cum-
 bersome but often makes their proofs easier because the resulting theorems are stronger and
 easier to prove by induction” [18].
    Rushby, Owre and Shankar use predicate subtypes for defining procedures incompletely
 in PVS. An example is presented in [21] which we write as
                         function subp(i, j: Z) : N <=
                         if i = j
                          then 0
                          else if j ≤ i then +(subp(i, s( j))) else  end _if
                         end _if
 in our notation. As automated termination analysis fails, termination function λi, j: Z. | i − j |
 is submitted to the system which then generates (and proves) the termination hypothesis
 ∀i, j: Z i = j ∧ j ≤ i → | i − j| > | i − s( j) |.21 The procedure body is written as
                          if i = j then 0 else subp(i, j + 1) + 1 end _if                             (23)
 in PVS and dependent predicate subtyping is used which demands j ≤ i for the formal
 parameters in the procedure head. A user specified termination function, viz. λi, j: Z. i − j,
 is required also here. PVS then generates 3 proof obligations for accepting the definition, viz.
  (i) ∀i, j: Z j ≤ i ∧ i = j → i − j ≥ 0 stipulating that i − j is of type N thus ensuring type
      correctness of the termination function,
 (ii) ∀i, j: Z j ≤ i ∧ i = j → j + 1 ≤ i to ensure type correctness of the recursive call
      subp(i, j + 1), and
(iii) ∀i, j: Z j ≤ i ∧ i = j → i − j > i − ( j + 1) to ensure termination of subp,
 whereas only the termination requirement (iii) is needed in     eriFun . Requirement (i)
 results from the subtype feature of PVS, viz. N ⊂ Z in this example, and (ii) stems from
 the encoding of the condition for non-determination as a predicate subtype in the procedure
 head, whereas this condition is part of the procedure body in our method.
    For proving well-formedness of an L-lemma as for instance
                        lemma j ≤ i + j → subp(i + j, j) = | i | <=
                        ∀i, j: Z if { j ≤ i + j, subp(i + j, j) = | i | , true}

 21 Function symbol s : Z → Z stands for the integer successor function and |. . .| with result type N is a
 selector of data type Z denoting the absolute value of an integer.


 123
Reasoning About Incompletely Defined Programs                                               Page 37 of 48    25


the lemma guard ∀i, j: Z j ≤ i + j → i + j = j ∨ j ≤ i + j is computed because
                                function ∇subp(i, j : Z) : bool <=
                                if i = j then true else j ≤ i end _if
has been synthesized as domain procedure for subp (after elimination of a recursive result
term), whereas PVS generates the type correctness condition ∀i, j: Z j ≤ i + j → j ≤ i + j
to ensure well-formedness. As another example from [21], L-lemma
                 lemma subp(i, j) = | i − j | ∨ subp( j, i) = | j − i | <=
                                                                                                            (24)
                 ∀i, j: Z if {subp(i, j) = | i − j |, true, subp( j, i) = | j − i |}
is not well-formed as the Disprover refutes the lemma guard, and the corresponding lemma
is not well-formed in PVS either.22 Neither the statements of Fig. 1 nor the terms in Example
2 are well-formed in PVS. Except for the type correctness checks in PVS for the recursive
calls in the body of a procedure f and the recursion elimination formulas in           eriFun,
the same proof obligations are obtained with both methods: Well-formedness of statements
involving f -calls are expressed with type correctness conditions in PVS which coincide with
the lemma guards of our proposal.
    Other proposals [6, 16, 17, 24, 25] use refined type systems and/or requires-guards to
restrict the domain of functions. Although the type systems in these works are more developed
and provide a more sophisticated type reasoning, the use of refined types and requires-guards
corresponds in its effect to the PVS approach. In our setting, a requires-guard for a procedure
 f would stipulate a boolean term reqf (referring only to the formal parameters of f ) as a
proof obligation which must be satisfied in the context of a procedure call f (. . .) to ensure
type correctness. These proofs correspond to the proofs required for simplifying domain
procedure ∇g when f is called in the body of some procedure g, cf. Sect. 5.2.1. In addition
it must be proved hat reqf is satisfied for the recursive calls in the body of procedure f . A
type correctness proof corresponds to the proof of a lemma guard when f is called in an L-
lemma, cf. Sect. 5.3. Upon computation of a (non-recursive) procedure call f (q1 , . . . , qn ) with
qi ∈ T ((Pr)c ), the instantiated proof obligation λ(reqf ) with λ(xi ) := qi for the formal
parameters xi of procedure f must be computed to true before the instantiated procedure
body λ(Rf ) is evaluated, and otherwise computation of f (. . .) results in a stuck term. The
disadvantages of this and the PVS approach are that (i) the user has to develop proof obligation
reqf , and that (ii) certain procedure calls might be necessarily executed twice if they occur
in the requires-guard as well as in the procedure body.23
    To give an example, a user has to program a predicate function [infix] is-power-
of (x, b:N):bool <= . . . corresponding to the simplified domain procedure ∇log of Fig. 8
before defining a procedure
            function log (x, b : N) : N <=
            requires (x is-power-of b); if x = 1 then 0 else + (log (x/b, b)) end _if
corresponding to procedure log from Fig. 3, where predicate is-power-of restricts the formal
parameters of log . If (n is-power-of m) with n, m ∈ T ((Pr)c )nat is not computed to true,
then procedure call log (n, m) is a stuck term. Otherwise the result of log (n, m) is obtained

22 L-lemma (24) would be well-formed if commutativity of connectives were respected upon computation of
a determination guard, see (22) in Sect. 5.3. The developers of PVS dispense with such an enhancement “for
reasons of simplicity and efficiency” [21] whereas our intention is to avoid the computation of stuck terms.
23 Double execution of procedure calls does not result, of course, if requires-guards are purely static notions
and do not influence the execution behaviour of a program as implemented in some systems, e.g. [17, 24, 25].


                                                                                                  123
25   Page 38 of 48                                                                              C. Walther


by evaluating the instantiated procedure body of log . Now when computing log (m ˆn, m)
for m ≥ 2, division is executed n times upon computation of (m ˆn is-power-of m) and is
executed another n times when evaluating the body of procedure log . By contrast, we define
procedure log incompletely and let the system synthesize domain procedure ∇log, where
division is only executed n times when computing log(m ˆn, m).24


7 Summary

We introduced a functional programming language L with polymorphism and incomplete
function definitions. We gave an operational semantics for L by defining an interpreter which
may yield stuck terms representing runtime errors when evaluating L-expressions. We inves-
tigated termination in presence of incompletely defined procedures and gave a semantics for
formulae which specify properties of a terminating L-program. The base idea for the seman-
tics is to complete all monomorphic instances of functions by assigning arbitrary values to
indetermined results and then to assign truth only to those statements which hold indepen-
dently of the values substituted for the indetermined results. We defined the determination
guard of a term t and proved that the truth of the determination guard is sufficient for absence
of stuck terms when computing monomorphic constructor ground instances of t with the
interpreter. Using determination guards, we introduced domain procedures of selectors and
procedures. We gave the notion of a safe procedure and proved that a domain procedure ∇f
decides the domain of its mother procedure f iff f is safe. We optimized domain procedures
by elimination of redundant conditions and recursive calls and proved correctness of these
optimizations. We also used the determination guard to define well-formedness of specifica-
tion formulae and proved the absence of runtime errors upon computation of monomorphic
constructor ground instances of well-formed L-lemmas by the interpreter.
    Our method for automated reasoning about incompletely defined programs only uses first-
order logic plus induction and is implemented in the      eriFun system, a Java program
with installers for the most common platforms being available on the web [26].


8 Appendix

8.1 Soundness of Domain Procedures

The following lemmas are needed for the proof of Theorem 2 and Corollary 3:

Lemma 5 Let Pr be a terminating L-program, let t ∈ T ((Pr) ∪ {}, {x 1 , . . . , xk })τ be an
if -normalized term with xi ∈ Vτi and τi ∈ types[Pr] for each i ∈ {1, . . . , k}, where t may
contain  in place of result terms, and assume

     (i) γ (∇g(y1 , . . . , ym ))⇓Pr ∈ {true, false} ,
     (ii) γ (∇g(y1 , . . . , ym )) ⇒!Pr true  γ (g(y1 , . . . , ym ))⇓Pr ∈ T ((Pr)c )(κ) ,

24  We used requires-guards (called assume-declarations) in a former version of         eriFun [23] but
did not continue with this approach as we did not find relevant benefits in the formulation and
proofs of our case studies. Also expressiveness of L is not enhanced with requires-guards as
each procedure function f (x1 :τ1 , . . . , xn :τn ):τ <= requires reqf ; Rf can be defined by a procedure
function f (x1 :τ1 , . . . , xn :τn ):τ <= if reqf then Rf else  end _if .


123
Reasoning About Incompletely Defined Programs                                           Page 39 of 48    25


for each procedure function g(y1 :κ1 , . . . , ym :κm ):κ <= Rg of Pr with g ∈ (Pr)proc
such that g(. . .) or ∇g(. . .) are subterms of t, for each type substitution  with (κi ) ∈
mtypes[Pr] and for each substitution γ with γ (yi ) ∈ T ((Pr)c )(κi ) for each i ∈
{1, . . . , m}. Then
                  (1) λ(dg[t])⇓Pr ∈ {true, false} ,
                  (2) λ(dg[t]) ⇒!Pr true  λ(t[s])⇓Pr ∈ T ((Pr)c )(τ ) ,

for each s ∈ T ((Pr), {x1 , . . . , xk })τ , for each type substitution  with (τi ) ∈
mtypes[Pr] and for each substitution λ with λ(xi ) ∈ T ((Pr)c )(τi ) for each i ∈
{1, . . . , k} , where t[s] results from t by replacement of each occurrence of  in t with s.

Proof The proof is by structural induction upon t: Either t = , t = xi or t = c for a
constructor constant c in the base case: If t = , then dg[t] = false by Definition 9(1), hence
λ(dg[t]) ⇒!Pr false and (2) holds vacuously. If t = xi , then dg[t] = true by Definition 9(2),
hence λ(dg[t]) ⇒!Pr true and λ(t[s])⇓Pr = λ(t) ∈ T ((Pr)c ) by definition of λ. Otherwise
dg[t] = true by Definition 9(3), hence λ(dg[t]) ⇒!Pr true and λ(t[s])⇓Pr = c ∈ T ((Pr)c ).
In the step case, t = h(t1 , . . . , tm ) with m ≥ 1 and (1) and (2) hold for each argument ti by
the induction hypotheses. As t is if -normalized, ti is not a result term for each i ∈ {1, . . . , m}
if h = if , hence ti [s] = ti for each i, and likewise if {t1 , t2 , t3 }[s] = if {t1 , t2 [s], t3 [s]}.
                                                                             m
    Case h ∈ {eq, not} ∪ (Pr)c : Then dg[h(t1 , . . . , tm )] = [ i=1           dg[ti ] ]if by Definition
9(3). (1) λ(dg[ti ])⇓Pr ∈ {true, false} for each i ∈ {1, . . . , m} by the 1st induction hypothe-
sis, hence λ(dg[h(t1 , . . . , tm )])⇓Pr ∈ {true, false}. (2) If λ(dg[h(t1 , . . . , tm )]) ⇒!Pr true, then
λ(dg[ti ]) ⇒!Pr true for each i ∈ {1, . . . , m}, hence λ(ti )⇓Pr ∈ T ((Pr)c ) by the 2nd induc-
tion hypothesis, and then λ(h(t1 , . . . , tm )) ⇒!Pr h(λ(t1 )⇓Pr , . . . , λ(tm )⇓Pr )⇓Pr ∈ T ((Pr)c )
by Definition 2.
    Case h = ∇sel j for a selector sel j belonging to a constructor cons:τ1 ×· · ·×τn → τ with
selectors sel 1 , . . . , sel n , and dg[∇sel j (t1 )] = dg[t1 ] by Definition 9(3). (1) λ(dg[t1 ])⇓Pr ∈
{true, false} by the 1st induction hypothesis, hence λ(dg[∇sel j (t1 )])⇓Pr ∈ {true, false}. (2)
If λ(dg[∇sel j (t1 )]) ⇒!Pr true, then λ(dg[t1 ]) ⇒!Pr true, hence λ(t1 )⇓Pr ∈ T ((Pr)c ) by
the 2nd induction hypothesis. If (∗) λ(t1 ) ⇒!Pr cons(q1 , . . . , qn ) for some qi ∈ T ((Pr)c ),
then with the computation rules of Definition 2

          λ(∇sel j (t1 ))
     ⇒+Pr eq(λ(t1 )⇓Pr , cons(sel 1 (λ(t1 )⇓Pr ), . . . , sel n (λ(t1 )⇓Pr ))) ; by Definition 10(2)
     = eq(cons(q1 , . . . , qn ), cons(sel 1 (λ(t1 )⇓Pr ), . . .))             ; by (∗)
     ⇒Pr [ i∈{1,...,n} eq(qi , seli (λ(t1 )⇓Pr )) ]if                          ; by rule (3)         (25)
     = [ i∈{1,...,n} eq(qi , seli (cons(q1 , . . . , qn ))) ]if                ; by (∗)
     ⇒+Pr [ i∈{1,...,n} eq(qi , qi ) ]if                                       ; by rule (5)
     ⇒!Pr true                                                                 ; by rule (2).

Otherwise λ(t1 ) ⇒!Pr cons (. . .) with cons = cons, and then

                    λ(∇sel j (t1 )) ⇒+                                !
                                     Pr eq(cons (. . .), cons(. . .)) ⇒Pr false                         (26)

by Definition 10(2) and computation rule (4) of Definition 2.
                                                                                      m
   Case h = ∇g for some g ∈ (Pr)proc : Then dg[∇g(t1 , . . . , tm )] = [ i=1             dg[ti ] ]if
by Definition 9(3). (1) λ(dg[ti ])⇓Pr ∈ {true, false} for each i ∈ {1, . . . , m} by
the 1st induction hypothesis, hence λ(dg[∇g(t1 , . . . , tm )])⇓Pr ∈ {true, false}. (2) If
λ(dg[∇g(t1 , . . . , tm )]) ⇒!Pr true, then λ(dg[ti ]) ⇒!Pr true for each i ∈ {1, . . . , m}, hence

                                                                                              123
25   Page 40 of 48                                                                                    C. Walther


λ(ti )⇓Pr ∈ T ((Pr)c ) by the 2nd induction hypothesis, and then λ(∇g(t1 , . . . , tm )) ⇒!Pr
∇g(λ(t1 )⇓Pr , . . . , λ(tm )⇓Pr )⇓Pr ∈ T ((Pr)c )bool by assumption (i).
    Case h = if : Then dg[if {t1 , t2 , t3 }] = [ dg[t1 ] ∧ if {t1 , dg[t2 ], dg[t3 ]} ]if by De-
finition 9(4), and λ(dg[t1 ])⇓Pr ∈ {true, false} by the 1st induction hypothesis. (1) If
λ(dg[t1 ]) ⇒!Pr false, then λ(dg[if {t1 , t2 , t3 }]) ⇒!Pr false. Otherwise λ(dg[t1 ]) ⇒!Pr true,
hence λ(t1 )⇓Pr ∈ {true, false} by the 2nd induction hypothesis. If λ(t1 ) ⇒!Pr true, then
λ(dg[if {t1 , t2 , t3 }]) ⇒!Pr λ(dg[t2 ])⇓Pr ∈ {true, false} by the 1st induction hypothesis,
and similarly λ(dg[if {t1 , t2 , t3 }]) ⇒!Pr λ(dg[t3 ])⇓Pr ∈ {true, false} if λ(t1 ) ⇒!Pr false.
(2) If λ(dg[if {t1 , t2 , t3 }]) ⇒!Pr true, then λ(dg[t1 ]) ⇒!Pr true and either λ(t1 ) ⇒!Pr
true and λ(dg[t2 ]) ⇒!Pr true or λ(t1 ) ⇒!Pr false and λ(dg[t3 ]) ⇒!Pr true. Hence
λ(if {t1 , t2 [s], t3 [s]}) ⇒!Pr λ(t2 [s])⇓Pr ∈ T ((Pr)c ) by the 2nd induction hypothesis in
the former case, and similarly λ(if {t1 , t2 [s], t3 [s]}) ⇒!Pr λ(t3 [s])⇓Pr ∈ T ((Pr)c ) in the
latter one.
    Case h = sel j for a selector belonging to a constructor cons:τ1 × · · · × τn → τ with
selectors sel 1 , . . . , sel n : Then dg[sel j (t1 )] = [ dg[t1 ] ∧ ∇sel j (t1 ) ]if by Definition 9(5),
and λ(dg[t1 ]) ∈ {true, false} by the 1st induction hypothesis. (1) If λ(dg[t1 ]) ⇒!Pr false,
then λ(dg[sel j (t1 )]) ⇒!Pr false . Otherwise (∗) λ(dg[t1 ]) ⇒!Pr true , and then λ(t1 )⇓Pr ∈
T ((Pr)c ) by the 2nd induction hypothesis. If λ(t1 ) ⇒!Pr cons(q1 , . . . , qn ) for some qi ∈
T ((Pr)c ), then

                          λ(dg[sel j (t1 )])
                     = [ λ(dg[t1 ]) ∧ λ(∇sel j (t1 )) ]if ; by Definition 9(5)
                     ⇒+Pr λ(∇sel j (t1 ))                 ; by (∗)
                     ⇒!Pr true                            ; by (25).

Otherwise λ(t1 ) ⇒!Pr cons (. . .) with cons = cons, and then λ(dg[sel j (t1 )]) ⇒+                         Pr
λ(∇sel j (t1 )) ⇒!Pr false by (26). (2) If λ(dg[sel j (t1 )]) ⇒!Pr true , then λ(dg[t1 ]) ⇒!Pr
true and λ(∇sel j (t1 )) ⇒!Pr true, hence λ(t1 )⇓Pr ∈ T ((Pr)c ) by the 2nd induction hy-
pothesis and eq(λ(t1 ), cons(sel 1 (λ(t1 )), . . . ,sel n (λ(t1 )))) ⇒!Pr true by Definition 10(2).
But then λ(t1 ) ⇒!Pr cons(q1 , . . . , qn ) for some qi ∈ T ((Pr)c ), hence λ(sel j (t1 )) =
sel j (λ(t1 )) ⇒!Pr q j ∈ T ((Pr)c ) with computation rule (5).
                                                                        m
    Case h ∈ (Pr)proc : Then dg[h(t1 , . . . , tm )] = [ i=1                 dg[ti ] ∧ ∇h(t1 , . . . , tm ) ]if
by Definition 9(5), and λ(dg[ti ]) ∈ {true, false} for each i ∈ {1, . . . , m} by the
1st induction hypothesis. (1) If λ(dg[ti ]) ⇒!Pr true for each i ∈ {1, . . . , m}, then
λ(ti )⇓Pr ∈ T ((Pr)c ) by the 2nd induction hypothesis, and then λ(dg[ h(t1 , . . . , tm )]) ⇒!Pr
∇h(λ(t1 )⇓Pr , . . . , λ(tm )⇓Pr )⇓Pr ∈ {true, false} by assumption (i). Otherwise λ(dg[ti ]) ⇒!Pr
false for some i ∈ {1, . . . , m}, and then λ(dg[h(t1 , . . . , tm )]) ⇒!Pr false. (2) If
λ(dg[h(t1 , . . . , tm )]) ⇒!Pr true, then λ(dg[ti ]) ⇒!Pr true for each i ∈ {1, . . . , m}
and λ(∇h(t1 , . . . , tm )) ⇒!Pr true. Hence λ(ti )⇓Pr ∈ T ((Pr)c ) by the 2nd induction
hypothesis, therefore λ(∇h(t1 , . . . , tm )) ⇒+                                             !
                                                      Pr ∇h(λ(t1 )⇓Pr , . . . , λ(tm )⇓Pr ) ⇒Pr true, and
                              !
then λ(h(t1 , . . . , tm )) ⇒Pr h(λ(t1 )⇓Pr , . . . , λ(tm )⇓Pr )⇓Pr ∈ T ((Pr) ) by assumption (ii).
                                                                                     c

                                                                                                               
                                                                                                               

Lemma 6 Let function f (x1 :τ1 , . . . , xn :τn ):τ <= Rf with f ∈ (Pr)proc be a procedure
of a terminating L-program Pr and assume

     (i) γ (∇g(y1 , . . . , ym ))⇓Pr ∈ {true, false} ,
     (ii) γ (∇g(y1 , . . . , ym )) ⇒!Pr true  γ (g(y1 , . . . , ym ))⇓Pr ∈ T ((Pr)c )(κ) ,

123
Reasoning About Incompletely Defined Programs                                         Page 41 of 48   25


for each procedure function g(y1 :κ1 , . . . , ym :κm ):κ <= Rg of Pr with g = f and g ∈
(Pr)proc such that g(. . .) or ∇g(. . .) are subterms of Rf , for each type substitution  with
(κi ) ∈ mtypes[Pr] and for each substitution γ with γ (yi ) ∈ T ((Pr)c )(κi ) for each
i ∈ {1, . . . , m}. Then
      (1) λ(∇ f (x1 , . . . , xn ))⇓Pr ∈ {true, false} ,
      (2) λ(∇ f (x1 , . . . , xn )) ⇒!Pr true  λ(f (x1 , . . . , xn ))⇓Pr ∈ T ((Pr)c )(τ ) ,
for each type substitution  with (τi ) ∈ mtypes[Pr] and for each substitution λ with
λ(xi ) ∈ T ((Pr)c )(τi ) for each i ∈ {1, . . . , n}.

Proof The proof is by induction upon the recursion structure of procedure f which is sound
as termination of f is demanded. Hence
                          λ(∇ f (θρ (x1 ), . . . , θρ (xn )))⇓Pr ∈ {true, false}                  (IH1 )

                       λ(∇ f (θρ (x1 ), . . . , θρ (xn ))) ⇒!Pr true
                                                                                                  (IH2 )
                        λ(f (θρ (x1 ), . . . , θρ (xn )))⇓Pr ∈ T ((Pr)c )(τ )

are obtained as induction hypotheses for each recursive call f (θρ (x1 ), . . . , θρ (xn )) in proce-
dure body Rf .
   We find that assumptions (i) and (ii) of Lemma 5 are satisfied by assumptions (i) and (ii)
for procedures g ∈ (Pr)proc with g = f such that g(. . .) or ∇g(. . .) are subterms of Rf ,
and assumptions (i) and (ii) of Lemma 5 are satisfied for each subterm f (θρ (x1 ), . . . , θρ (xn ))
of Rf with γ (xi ) := λ(θρ (xi ))⇓Pr for each i ∈ {1, . . . , n} by (IH1 ) and (IH2 ). Hence

           (3) λ(dg[Rf ])⇓Pr ∈ {true, false} ,
           (4) λ(dg[Rf ]) ⇒!Pr true  λ(Rf [ f (x1 , . . . , xn )])⇓Pr ∈ T ((Pr)c )

by Lemma 5, and therefore (1) holds with (3) because (†) λ(∇ f (x1 , . . . , xn )) ⇒!Pr
λ(dg[Rf ]⊥wn )⇓Pr by Definition 10(1) and (‡) λ(dg[Rf ]⊥wn )⇓Pr = λ(dg[Rf ])⇓Pr by
soundness of . (2) holds with (4), (†) and (‡) as Rf [ f (x1 , . . . , xn )] = Rf and
λ(f (x1 , . . . , xn )) ⇒!Pr λ(Rf )⇓Pr by computation rule (11) of Definition 2 because
λ(∇ f (x1 , . . . , xn )) ⇒!Pr true entails λ(exceptf ) ⇒!Pr false.                   
                                                                                      

Theorem 2 Let Pr be a terminating L-program, let τi ∈ types[Pr] and let  be some type
substitution with (τi ) ∈ mtypes[Pr] for each i ∈ {1, . . . , n}.
(1) If function f (x1 :τ1 , . . . , xn :τn ):τ <= Rf is a procedure of Pr with f ∈ (Pr)proc , then
    for each substitution λ with λ(xi ) ∈ T ((Pr)c )(τi ) for each i ∈ {1, . . . , n}
         (i) λ(∇ f (x1 , . . . , xn ))⇓Pr ∈ {true, false} ,
         (ii) λ(∇ f (x1 , . . . , xn )) ⇒!Pr true  λ(f (x1 , . . . , xn ))⇓Pr ∈ T ((Pr)c )(τ ) .
(2) If sel j is a selector of Pr belonging to a constructor cons:τ1 ×· · ·×τn → τ with selectors
    sel1 , . . . , sel n and x ∈ Vτ , then for each substitution λ with λ(x) ∈ T ((Pr)c )(τ )
          (i) λ(∇sel j (x))⇓Pr ∈ {true, false} ,
          (ii) λ(∇sel j (x)) ⇒!Pr true  λ(sel j (x))⇓Pr ∈ T ((Pr)c )(τ j ) .

Proof (1) Let  be a relation on (Pr )proc defined as g  f iff the definition of g precedes
the definition of f in Pr . Obviously  is transitive and well-founded. In particular, g  f if

                                                                                            123
25   Page 42 of 48                                                                         C. Walther


procedure body Rf contains some procedure call g(. . .). Also g  f if ∇g  f as g  ∇g.
We prove (i) and (ii) by induction upon  :
   If procedure f is -minimal, then (i) and (ii) hold by Lemma 6 because Rf contains
only procedure calls f (. . .) at most so that both assumptions of Lemma 6 vacuously
hold. Otherwise Rf may contain calls g(. . .) and/or ∇g(. . .) of procedures function
g(y1 :κ1 , . . . , ym :κm ):κm <= . . . with g = f and g ∈ (Pr)proc , hence g  f and we
obtain the induction hypotheses


                             γ (∇g(y1 , . . . , ym ))⇓Pr ∈ {true, false}                      (IH1 )

       γ (∇g(y1 , . . . , ym )) ⇒!Pr true  γ (g(y1 , . . . , ym ))⇓Pr ∈ T ((Pr)c )(κ)      (IH2 )
 for any type substitution  with (κi ) ∈ mtypes[Pr] for each i ∈ {1, . . . , m} and for each
substitution γ with γ (yi ) ∈ T ((Pr)c )(κi ) . As both assumptions of Lemma 6 are satisfied
by the induction hypotheses, (i) and (ii) hold by Lemma 6 as well.
   (2) We find (∗) λ(dg[sel j (x)])⇓Pr = λ(∇sel j (x))⇓Pr because
                         λ(dg[sel j (x)])
                     = λ([ dg[x]) ∧ ∇sel j (x)) ]if ) ; by Definition9(5)
                     ⇒+
                      Pr λ(∇sel j (x))                ; by Definition 9(2)
and obtain
         (1 ) λ(dg[sel j (x)])⇓Pr ∈ {true, false} ,
         (2 ) λ(dg[sel j (x)]) ⇒!Pr true  λ(sel j (x)[s])⇓Pr ∈ T ((Pr)c )(τ j ) ,
with Lemma 5, hence (i) holds with (∗) and (1 ) and (ii) holds with (∗) and (2 ) as sel j (x)[s] =
sel j (x) because sel j (x) is −free.                                                             
                                                                                                   

Corollary 3 Let Pr be a terminating L-program and let t ∈ T ((Pr))η be an if -normalized
ground term of monomorphic type η. Then
       (1) dg[t]⇓Pr ∈ {true, false} and (2) dg[t] ⇒!Pr true  t⇓Pr ∈ T ((Pr)c )η .

Proof (1) and (2) hold by Lemma 5 as both assumptions of Lemma 5 are satisfied by Theorem
2(1), λ = ε as t is a ground term and t[s] = t because t is −free.                     
                                                                                        

8.2 Safe Procedures and Programs

Theorem 4 Let Pr be a terminating L-program and let t ∈ T ((Pr )) be an if -normalized
ground term of monomorphic type. Then
                                                      dg[t] ⇒!Pr true.
                      t is safe ∧ t⇓Pr ∈ T ((Pr)c ) 

Proof () We prove the statement by structural induction upon t: t = c for a constructor
constant c in the base case and dg[c] = true by Definition 9(3).
   In the step case, t = h(t1 , . . . , tm ) with m ≥ 1 and dg[ti ] ⇒!Pr true holds for each safe
argument ti with i ∈ {1, . . . , m} and (ti )⇓Pr ∈ T ((Pr)c ) by the induction hypothesis.
   Case h ∈ {eq, not} ∪ (Pr)c ∪ (Pr)∇proc : If i · πi ∈ Occsafe (t) for some i ∈ {1, . . . , m}
and some πi ∈ Occsafe (ti ), then c-path[t, i · πi ] ⇒!Pr true entails dg[t|i·πi ] ⇒!Pr true by
Definition 11 as t⇓Pr ∈ T ((Pr)c ) and t is safe. We find c-path[t, i · πi ] = ∅ ⇒!Pr true by
Definition 1 because h = if , hence (†) dg[t|i·πi ] ⇒!Pr true.

123
Reasoning About Incompletely Defined Programs                                              Page 43 of 48   25


    Assume that (ti )⇓Pr ∈    / T ((Pr)c ) for some i ∈ {1, . . . , m} and let si be a termsize-
minimal subterm of ti with (si )⇓Pr ∈         / T ((Pr)c ). Then si = g(si,1 , . . . , si,n ) for some
g ∈ (Pr) with g = if as t is if -normalized and (‡) (si, j )⇓Pr ∈ T ((Pr)c ) for each
 j ∈ {1, . . . , n} where n ≥ 1 as c = c⇓Pr ∈ T ((Pr)c ) for each constructor constant c.
    Subcase g ∈ {eq, not} ∪ (Pr)c ∪ (Pr)∇proc : Then (si )⇓Pr ∈ T ((Pr)c ) by (‡), Defi-
nition 2 and Theorem 2(1.i, 2.i), hence this subcase is impossible.
    Subcase g ∈ (Pr)proc ∪ (Pr)sel : As si = t|i·πi for some πi ∈ Occ(ti ), i · πi ∈
Occsafe (t) and therefore dg[t|i·πi ] = dg[si ] ⇒!Pr true by (†). But then (si )⇓Pr ∈ T ((Pr)c )
by Corollary 3(2), hence this subcase is impossible as well.
    Therefore (ti )⇓Pr ∈ T ((Pr)c ) for each i ∈ {1, . . . , m}. If πi ∈ Occsafe (ti ) for some
i ∈ {1, . . . , m}, then i · πi ∈ Occsafe (t), hence dg[ti|πi ] = dg[t|i·πi ] ⇒!Pr true by (†),
and consequently each ti is safe. But then dg[ti ] ⇒!Pr true for each i ∈ {1, . . . , m} by the
induction hypothesis and dg[h(t1 , . . . , tm )] = [ i=1     m
                                                                  dg[ti ] ]if ⇒!Pr true with Definition
9(3) in turn.
    Case h = if : Then t = if {t1 , t2 , t3 } with (t1 )⇓Pr ∈ {true, false} as t⇓Pr ∈           / T ((Pr)c )
otherwise. If π1 ∈ Occsafe (t1 ), then 1·π1 ∈ Occsafe (t), therefore c-path[t, 1 · π1 ] ⇒!Pr true
entails dg[t|1·π1 ] ⇒!Pr true as t⇓Pr ∈ T ((Pr)c ) and t is safe. Then dg[t1|π1 ] =
dg[t|1·π1 ] ⇒!Pr true as c-path[t, 1 · π1 ] = ∅ ⇒!Pr true by Definition 1, hence t1 is safe,
and then (†) dg[t1 ] ⇒!Pr true by the induction hypothesis.
    If t1 ⇒!Pr true, then (‡) dg[if {t1 , t2 , t3 }] = [ dg[t1 ] ∧ if {t1 , dg[t2 ], dg[t3 ]} ]if ⇒+Pr dg[t2 ]
by Definition 9(4) and (†), and (t2 )⇓Pr ∈ T ((Pr)c ) because if {t1 , t2 , t3 } ⇒+       Pr  t2 ⇒ ! t
                                                                                                    Pr ⇓Pr ∈
             c                safe                                      !
T ((Pr) ). If π2 ∈ Occ (t2 ) such that c-path[t2 , π2 ] ⇒Pr true, then 2 · π2 ∈ Occsafe (t)
and c-path[t, 2 · π2 ] ⇒!Pr true entails dg[t|2·π2 ] ⇒!Pr true because t⇓Pr ∈ T ((Pr)c )
and t is safe. We find c-path[t, 2 · π2 ] = {t1 } ∪ c-path[t2 , π2 ] by Definition 1, hence
c-path[t2 , π2 ] ⇒!Pr true entails c-path[t, 2 · π2 ] ⇒!Pr true as t1 ⇒!Pr true and therefore t2
is safe as dg[t|2·π2 ] = dg[t2|π2 ] ⇒!Pr true. Then dg[t2 ] ⇒!Pr true by the induction hypothesis
and dg[if {t1 , t2 , t3 }] ⇒!Pr true in turn by (‡). Otherwise t1 ⇒!Pr false and c-path[t, 3 · π3 ] =
{not(t1 )} ∪ c-path[t3 , π3 ] , hence dg[if {t1 , t2 , t3 }] ⇒+  Pr dg[t3 ] by Definition 9(4) and (†),
and dg[t3 ] ⇒!Pr true is proved in the same way.
    Case h ∈ (Pr)proc ∪ (Pr)sel : Then ε ∈ Occsafe (t), hence c-path[t, ε] ⇒!Pr true
entails dg[t|ε ] ⇒!Pr true by Definition 11 because t is safe and t⇓Pr ∈ T ((Pr)c ). As
c-path[t, ε] = ∅ ⇒!Pr true and t|ε = t, dg[t] ⇒!Pr true.
    () We prove “ (t is unsafe ∨ t⇓Pr ∈           / T ((Pr)c )  dg[t] ⇒!Pr false”25 : If t⇓Pr ∈          /
                                !
T ((Pr) ), then dg[t] ⇒Pr false by Corollary 3. Otherwise t is unsafe and we prove “ t is
             c

unsafe  dg[t] ⇒!Pr false” by structural induction upon t:
    t = c for a constructor constant c in the base case, hence the statement holds vacuously as c
is safe. In the step case, t = h(t1 , . . . , tm ) with m ≥ 1 and “ ti is unsafe  dg[ti ] ⇒!Pr false”
is obtained as the induction hypothesis for each i ∈ {1, . . . , m}.
    Case h ∈ {eq, not} ∪ (Pr)c ∪ (Pr)∇proc : Then c-path[t, j · π j ] ⇒!Pr true but
dg[t| j·π j ] ⇒!Pr false for some j ∈ {1, . . . , m} and some π j ∈ Occsafe (t j ) as t is unsafe
and h ∈   / (Pr)proc ∪ (Pr)sel . We find dg[t| j·π j ] = dg[t j|π j ] and c-path[t, j · π j ] =
c-path[t j , π j ] = ∅ ⇒!Pr true by Definition 1 as h = if . If (t j )⇓Pr ∈             / T ((Pr)c ), then
dg[t j ] ⇒Pr false by Corollary 3. Otherwise t j is unsafe, and then dg[t j ] ⇒!Pr false by
              !

the induction hypothesis. Hence dg[h(t1 , . . . , tm )] = [ i=1      m
                                                                           dg[ti ] ]if ⇒!Pr false by Defini-
tion 9(3) in either case.
25 dg[t] ! true iff dg[t] ⇒! false by Corollary 3(1).
          Pr                Pr


                                                                                                 123
25    Page 44 of 48                                                                              C. Walther


   Case h = if : Then c-path[t, i · πi ] ⇒!Pr true and dg[t|i·πi ] = dg[ti|πi ] ⇒!Pr false for
some i ∈ {1, 2, 3} and some πi ∈ Occsafe (ti ) by Definition 11 as t = if {t1 , t2 , t3 } is unsafe.
   If c-path[t, 1 · π1 ] ⇒!Pr true and dg[t1|π1 ] ⇒!Pr false, then c-path[t1 , π1 ] = ∅ ⇒!Pr true
by Definition 1, and (t1 )⇓Pr ∈ {true, false} as t⇓Pr ∈ T ((Pr)c ) because t is unsafe. Hence
t1 is unsafe, then dg[t1 ] ⇒!Pr false by the induction hypothesis and dg[if {t1 , t2 , t3 }] =
[ dg[t1 ] ∧ if {t1 , dg[t2 ], dg[t3 ]} ]if ⇒!Pr false by Definition 9(4).
   If c-path[t, 2 · π2 ] ⇒!Pr true and dg[t2|π2 ] ⇒!Pr false, then t1 ⇒!Pr true and
c-path[t2 , π2 ] ⇒!Pr true because c-path[t, 2 · π2 ] = {t1 } ∪ c-path[t2 , π2 ] by Definition 1.
We find (t2 )⇓Pr ∈ T ((Pr)c ) because if {t1 , t2 , t3 } ⇒+             !
                                                                 Pr t2 ⇒Pr t⇓Pr ∈ T ((Pr) ), hence
                                                                                             c
                                     !
t2 is unsafe, then dg[t2 ] ⇒Pr false by the induction hypothesis and dg[if {t1 , t2 , t3 }] =
[ dg[t1 ] ∧ if {t1 , dg[t2 ], dg[t3 ]} ]if ⇒+                                  !
                                              Pr [ dg[t1 ]⇓Pr ∧ dg[t2 ] ]if ⇒Pr false by Definition
9(4). If c-path[t, 3 · π3 ] ⇒Pr true and dg[t3|π3 ] ⇒Pr false, then dg[t3 ] ⇒!Pr false and
                                     !                          !

dg[if {t1 , t2 , t3 }] ⇒+                                !
                          Pr [ dg[t1 ]⇓Pr ∧ dg[t3 ] ]if ⇒Pr false is proved as in the previous case.
   Case h ∈ (Pr)proc ∪(Pr)sel : If t j is unsafe for some j ∈ {1, . . . , m}, then dg[t j ] ⇒!Pr
                                                                                         n
false by the induction hypothesis, and therefore dg[h(t1 , . . . , tm )] = [ i=1             dg[ti ] ∧
                           !
∇h(t1 , . . . , tn ) ]if ⇒Pr false by Definition 9(5).
   If ti is safe for each i ∈ {1, . . . , m}, then c-path[t, ε] = ∅ ⇒!Pr true and dg[t|ε ] =
dg[t] ⇒!Pr false by Definition 11 as t is unsafe and ε ∈ Occsafe (t).                                
                                                                                                     

8.3 Soundness of Recursion Elimination

Theorem 6 Let function ∇f (x1 :τ1 , . . . , xn :τn ):bool <= R∇f be a domain procedure in a
terminating L-program Pr and let
(1) Occ∇fcond be all occurrences ρ ∈ Occ(R ) such that
                                                       ∇f
    R∇f |ρ = if {∇ f (θρ·1 (x1 ), . . . , θρ·1 (xn )), sρ·2 , false} where
(2) sρ·2 := if {f (θρ·1 (x1 ), . . . , θρ·1 (xn )), ∇ f (θγ (x1 ), . . . , θγ (xn )), true} or
    sρ·2 := if {f (θρ·1 (x1 ), . . . , θρ·1 (xn )), true, ∇ f (θγ (x1 ), . . . , θγ (xn ))} or
    sρ·2 := ∇ f (θγ (x1 ), . . . , θγ (xn )), and
(3) R∇f |π ∈ {true, ∇f (θπ (x1 ), . . . , θπ (xn ))} for each
    π ∈ Occ∇f res \{ρ · 3 ∈ Occres | ρ ∈ Occcond }.
                                      ∇f               ∇f

Then [∀x1 :τ1 , . . . , xn :τn ∇ f (x1 , . . . , xn ) ≡ true] ∈ ThPr .

Proof Let  be a type substitution with (τi ) ∈ mtypes[Pr ] and let λ be a substitution with
λ(xi ) ∈ T ((Pr )c )(τi ) for each i ∈ {1, . . . , n}. We prove ∇ f (λ(x1 ), . . . , λ(xn )) ⇒!Pr true
by induction upon the recursion structure of procedure ∇f which sound because termination
is demanded.

Base case If λ(c-path[R∇f , π]) ⇒!Pr true for some π ∈ Occbase
                                                          ∇f , then ∇ f (λ(x 1 ), . . . , λ(x n ))
  !
⇒Pr true because R∇f |π = true for each π ∈ Occ∇f , by (3).
                                                  base


Step case The induction hypothesis is obtained as
       λ (c-path[R∇f , π]) ⇒!Pr true  ∇ f (λ (θπ (x1 )), . . . , λ (θπ (xn ))) ⇒!Pr true         (IH)
for each substitution λ with λ (xi ) ∈ T ((Pr )c )(τi ) for each i ∈ {1, . . . , n} and each
π ∈ Occrec
         ∇f with recursive call ∇ f (θπ (x 1 ), . . . , θπ (x n )).




123
Reasoning About Incompletely Defined Programs                                             Page 45 of 48    25


   If (†) λ(c-path[R∇f , π]) ⇒!Pr true for some π ∈ Occrec
                                                       ∇f ∩ Occ∇f , then
                                                               res


                     ∇ f (λ(x1 ), . . . , λ(xn ))
                ⇒+Pr λ(R∇f [π ← ∇ f (θπ (x 1 ), . . . , θπ (x n ))]) , by (†)
                =    ∇ f (λ(θπ (x1 )), . . . , λ(θπ (xn )))]         , as π ∈ Occres
                                                                                 ∇f
                  !
                ⇒Pr true                                             , by (IH)
   If (‡) sρ·2      =     if {f (θρ·1 (x1 ), . . . , θρ·1 (xn )), ∇ f (θγ (x1 ), . . . , θγ (xn )), true} and
λ(c-path[R∇f , ρ · 1]) ⇒!Pr true for some ρ ∈ Occcond       ∇f , then

                ∇ f (λ(x1 ), . . . , λ(xn ))
           ⇒+Pr λ(R∇f [ρ ← if {∇ f (θρ·1 (x 1 ), . . . , θρ·1 (x n ), sρ·2 , true}]) , by (‡)
           ⇒+Pr λ(R∇f [ρ ← sρ·2 ])                                                   , by (IH)
                                 if {f (θρ·1 (x1 ), . . . , θρ·1 (xn )),
           =    λ(R∇f [ρ ←                                                           , by (‡)
                                     ∇ f (θγ (x1 ), . . . , θγ (xn )), true}])
We find by Theorem 2(1.ii) that λ(∇ f (θρ·1 (x1 ), . . . , θρ·1 (xn )) ⇒!Pr true entails
λ(f (θρ·1 (x1 ), . . . , θρ·1 (xn )))⇓Pr ∈ {true, false}. If λ(f (θρ·1 (x1 ), . . . , θρ·1 (xn ))) ⇒!Pr true,
then λ(c-path[R∇f , γ ]) ⇒!Pr true because c-path[R∇f , γ ] = c-path[R∇f , ρ · 1] ∪
{f (θρ·1 (x1 ), . . . , θρ·1 (xn ))}, hence
                              if {f (θρ·1 (x1 ), . . . , θρ·1 (xn )),
               λ(R∇f [ρ ←
                                 ∇ f (θγ (x1 ), . . . , θγ (xn )), true}])
        ⇒+Pr   λ(R∇f [ρ ← ∇ f (θγ (x1 ), . . . , θγ (xn ))])
        =      ∇ f (λ(θγ (x1 )), . . . , λ(θγ (xn )))                      , as ρ · 2 · 2 ∈ Occres
                                                                                               ∇f
        ⇒!Pr   true                                                        , by (IH).
Otherwise λ(f (θρ·1 (x1 ), . . . , θρ·1 (xn ))) ⇒!Pr false, and then
                           if {f (θρ·1 (x1 ), . . . , θρ·1 (xn )),
               λ(R∇f [ρ ←
                              ∇ f (θγ (x1 ), . . . , θγ (xn )), true}])
       ⇒!Pr    λ(R∇f [ρ ← true])
       =       true                                                     , as ρ · 2 · 3 ∈ Occres
                                                                                            ∇f .
The remaining cases for sρ·2 are proved analogously.
   As ∇ f (λ(x1 ), . . . , λ(xn )) ⇒!Pr true for each substitution λ with λ({x1 , . . . , xn }) ⊂
T ((Pr )c ), [∀x 1 :τ1 , . . . , x n :τn ∇ f (x 1 , . . . , x n ) ≡ true] ∈ ThPr by Lemma 2.   
                                                                                                
Lemma 7 Let all notions be given as in Definition 13, let  be a type substitution with
(τi ) ∈ mtypes[Pr], and let λ0 be a substitution with λ0 (xi ) ∈ T ((Pr)c )(τi ) for each
i ∈ {1, . . . , n}. Then λ0 (R∇f ) ⇒!Pr b, if
                         (1) ρ1 ∈ ,
                         (2) λ                           !
                              0 (c-path[R∇f , ρ1 ]) ⇒Pr true, and
                         (3) ∀x1 :τ1 , . . . , xn :τn Re,b ≡ true ∈ ThPr .
Proof As ∇f (λ0 (x1 ), . . . , λ0 (xn ))⇓Pr ∈ {true, false} by Theorem 2(1.i) and procedure ∇f is
tail recursive by Definitions 9, 10 and 13(1), there are some t0 , . . . , tk ∈ T ((Pr))bool with
k ≥ 1 and t0 ⇒+             ∗           ∗
                 Pr t1 ⇒Pr . . . ⇒Pr tk such that

                               (i)   t0 = ∇f (λ0 (x1 ), . . . , λ0 (xn )),
                              (ii)   λ j−1 (c-path[R∇f , ρ j ]) ⇒!Pr true,
                                                                                                          (27)
                             (iii)   t j = ∇f (λ j (x1 ), . . . , λ j (xn )),
                              (iv)   (tk )⇓Pr ∈ {true, false} ,

                                                                                                 123
25   Page 46 of 48                                                                              C. Walther


where R∇f |ρ j = f (θ j (x1 ), . . . , θ j (xn )) for each ρ j ∈ Occ∇f
                                                                    rec and λ (x ) = λ
                                                                             j i       j−1 (θ j (x i ))⇓Pr
for each i ∈ {1, . . . , n} and each j ∈ {1, . . . , k}. The existence of computation (27) is
guaranteed because procedure ∇f terminates and then (tk )⇓Pr ∈ {true, false} by Theorem
2(1.i).
   As [ ∀x1 :τ1 , . . . , xn :τn Re,b ≡ true ] ∈ ThPr and ρ1 ∈ , (†) ρi ∈  for each i ∈
{2, . . . , k − 1} and (‡) ρk ∈ Occb . We prove
                          1 ≤ h ≤ k ∧ ρk+1−h ∈   tk+1−h ⇒!Pr b                                     (28)
by induction upon h. If h = 1, then ρk+1−h = ρk ∈ Occb by (‡), hence tk ⇒!Pr b. We have
2 ≤ h ≤ k in the induction step, hence 1 ≤ k + 1 − h ≤ k − 1 and then
                                        tk+1−h ⇒+
                                                Pr tk+2−h                                            (29)
by (27). The induction hypothesis is obtained as
                          2 ≤ h ≤ k ∧ ρk+2−h ∈   tk+2−h ⇒!Pr b.                                   (IH)


   If h = 2, then tk+1−h ⇒!Pr b by (29) because tk+2−h = tk and ρk ∈ Occb by (‡).
Otherwise h ≥ 3, hence 2 ≤ k + 2 − h ≤ k − 1, therefore ρk+2−h ∈  by (†) and then
tk+1−h ⇒!Pr b by (29) and (IH).
   In particular ρ1 ∈   t1 ⇒!Pr b by (28), and the statement is proved because ρ1 ∈ 
and ∇f (λ0 (x1 ), . . . , λ0 (xn )) ⇒Pr λ0 (R∇f ) ⇒+
                                                   Pr t1 .                            
                                                                                      

Theorem 7 Let all notions be given as in Definition 13 and let R∇f ,b be obtained from
procedure body R∇f by replacement of each recursive call ∇f (θρ (x1 ), . . . , θρ (xn )) with b
for each ρ ∈  and subsequent weak normalization. Then
                          [ ∀x1 :τ1 , . . . , xn :τn Re,b ≡ tr ue ] ∈ ThPr ,
                                                     
                          [ ∀x1 :τ1 , . . . , xn :τn R∇f ≡ R∇f ,b ] ∈ ThPr .

Proof We aim to prove
                                  λ0 (R∇f )⇓Pr = λ0 (R∇f ,b )⇓Pr ,                                  (30)
where we assume all notions given in the proof of Lemma 7.
   If ρ j ∈
          /  for each j ∈ {1, . . . , k − 1}, then (30) holds vacuously because ρ j ∈ Occ∇f
                                                                                          rec
                                                                                             ,b
and the difference between R∇f and R∇f ,b has no consequences in this case. Otherwise
ρ ∈  for some  ∈ {1, . . . , k − 1} and then
                       λ0 (R∇f ) ⇒+      ∗                    +
                                  Pr t1 ⇒Pr t ⇒Pr λ (R∇f ) ⇒Pr t+1 .

Further on λ (R∇f ) ⇒!Pr b by Lemma 7, hence λ0 (R∇f )⇓Pr = b. We may assume without
loss of generality that  is minimal, i.e. ρm ∈ /  for each m < . Then λ0 (R∇f ,b ) ⇒∗Pr t
as  is minimal and t ⇒+  Pr b as R∇f ,b |ρ := b, and (30) holds for this case as well.  
                                                                                            


Acknowledgements Thanks to the associate editor and both reviewers for several comments and suggestions
which helped to improve the paper.

Author Contributions CW wrote the manuscript text and prepared all figures.

Funding Open Access funding enabled and organized by Projekt DEAL.


123
Reasoning About Incompletely Defined Programs                                                Page 47 of 48   25


Data Availability No datasets were generated or analysed during the current study.


Declarations
Conflict of interest The authors declare no Conflict of interest.

Open Access This article is licensed under a Creative Commons Attribution 4.0 International License, which
permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give
appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence,
and indicate if changes were made. The images or other third party material in this article are included in the
article’s Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is
not included in the article’s Creative Commons licence and your intended use is not permitted by statutory
regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder.
To view a copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.



References
 1. Aderhold, M., Walther, C., Szallies, D., Schlosser, A.: A fast disprover for eriFun. In: Ahrendt,
    W., Baumgartner, P., de Nivelle, H. (eds.) Proceedings of Workshop on Non-theorems, Non-validity,
    Non-provability (DISPROVING-06), 2006, Seattle, WA, pp. 59–69 (2006). http://verifun.de/documents
 2. Arthan, R.D.: Undefinedness in Z: issues for specification and proof. In: Proceedings of CADE 13 Work-
    shop on Mechanization of Partial Functions, 1996 (1996). http://www.cs.bham.ac.uk/∼mmk/cade96-
    partiality/
 3. Baader, F., Nipkow, T.: Term Rewriting and All That. Cambridge University Press, Cambridge (1998)
 4. de Nivelle, H.: Classical logic with partial functions. J. Autom. Reason. 47(4), 399–425 (2011). https://
    doi.org/10.1007/s10817-011-9236-z
 5. Farmer, W.M.: Mechanizing the traditional approach to partial functions. In: Proceed-
    ings of CADE 13 Workshop on Mechanization of Partial Functions, 1996 (1996).
    http://www.cs.bham.ac.uk/∼mmk/cade96-partiality/
 6. Filliâtre, J.-C., Paskevich, A.: Why3 —where programs meet provers. In: Felleisen, M., Gardner, P. (eds.)
    Programming Languages and Systems, pp. 125–128. Springer (2013). https://doi.org/10.1007/978-3-
    642-37036-6_8
 7. Finn, S., Fourmann, M.P., Longley, J.: Partial functions in a total setting. J. Autom. Reason. 18, 85–104
    (1997). https://doi.org/10.1023/A:1005702928286
 8. Giesl, J.: Induction proofs with partial functions. J. Autom. Reason. 26, 1–49 (2001). https://doi.org/10.
    1023/A:1006408829523
 9. Gries, D., Schneider, F.B.: Avoiding the undefined by underspecification. In: van Leeuwen, J. (ed.) Com-
    puter Science Today: Recent Trends and Developments. Lecture Notes in Computer Science, vol. 1000,
    pp. 366–373. Springer (1995). https://doi.org/10.1007/BFb0015254
10. Hähnle, R.: Many-valued logic, partiality, and abstraction in formal specification languages. Log. J. IGPL
    13(4), 415–433 (2005). https://doi.org/10.1093/jigpal/jzi032
11. Jones, C.B.: Partial functions and logics: a warning. Inf. Process. Lett. (1995). https://doi.org/10.1016/
    0020-0190(95)00042-B
12. Jones, C.B.: Reasoning about partial functions in the formal development of programs. Electron. Notes
    Theor. Comput. Sci. 145, 3–25 (2006). https://doi.org/10.1016/j.entcs.2005.10.002
13. Kapur, D., Musser, D.R.: Inductive reasoning with incomplete specifications. In: Symposium on Logic
    in Computer Science, 1986, vol. 720, pp. 367–377. IEEE Computer Society, Cambridge (1986)
14. Kleene, S.C.: Introduction to Metamathematics. Bibliotheca Mathematica. North Holland, Amsterdam
    (1952)
15. Krauss, A.: Partial and nested recursive function definitions in higher-order logic. J. Autom. Reason.
    44(4), 303–336 (2010). https://doi.org/10.1007/s10817-009-9157-2
16. Lattuada, A., Hance, T., Bosamiya, J., Brun, M., Cho, C., LeBlanc, H., Srinivasan, P., Achermann, R.,
    Chajed, T., Hawblitzel, C., Howell, J., Lorch, J.R., Padon, O., Parno, B.: Verus: a practical foundation for
    systems verification. In: Proceedings of ACM SIGOPS 30th Symposium on Operating Systems Principles,
    2024, Austin, TX, USA, pp. 438–454 (2024). https://doi.org/10.1145/3694715.3695952




                                                                                                   123
25   Page 48 of 48                                                                                 C. Walther


17. Leino, K.R.M.: Dafny: an automatic program verifier for functional correctness. In: Clarke, E.M.,
    Voronkov, A. (eds.) Logic for Programming, Artificial Intelligence, and Reasoning, pp. 348–370. Springer,
    Dakar (2010). https://doi.org/10.1007/978-3-642-17511-4_20
18. Manolios, P., Moore, J.S.: Partial functions in ACL2. J. Autom. Reason. 31, 107–127 (2003). https://doi.
    org/10.1023/B:JARS.0000009505.07087.34
19. Mehta, F.: A practical approach to partiality—a proof based approach. In: Formal Methods and Software
    Engineering, 10th International Conference on Formal Engineering Methods, ICFEM 2008. Lecture Notes
    in Computer Science, 2008, vol. 5256, pp. 238–257. Springer (2008). https://doi.org/10.1007/978-3-540-
    88194-0_16
20. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL—A Proof Assistant for Higher-Order Logic. Lecture
    Notes in Computer Science, vol. 2283. Springer (2002). https://doi.org/10.1007/3-540-45949-9
21. Rushby, J.M., Owre, S., Shankar, N.: Subtypes for specifications: predicate subtyping in PVS. IEEE
    Trans. Softw. Eng. 24(9), 709–720 (1998). https://doi.org/10.1109/32.713327
22. Schieder, B., Broy, M.: Adapting calculational logic to the undefined. Comput. J. 42(2), 73–81 (1999).
    https://doi.org/10.1093/comjnl/42.2.73
23. Schlosser, A., Walther, C., Gonder, M., Aderhold, M.: Context dependent procedures and computed types
    in eriFun. Electron. Notes Theor. Comput. Sci. 174(7), 61–78 (2007). https://doi.org/10.1016/j.entcs.
    2006.10.038
24. Swamy, N., Hriţcu, C., Keller, C., Rastogi, A., Delignat-Lavaud, A., Forest, S., Bhargavan, K., Four-
    net, C., Strub, P.-Y., Kohlweiss, M., Zinzindohoue, J.-K., Zanella-Béguelin, S.: Dependent types and
    multi-monadic effects in F*. In: Proceedings of 43rd Annual ACM SIGPLAN-SIGACT Symposium on
    Principles of Programming Languages, 2016, St. Petersburg, FL, USA, pp. 256–270 (2016). https://doi.
    org/10.1145/2914770.2837655
25. Vazou, N., Seidel, E.L., Jhala, R., Vytiniotis, D., Peyton-Jones, S.: Refinement types for Haskell. In:
    Proceedings of 19th ACM SIGPLAN International Conference on Functional Programming, 2014, pp.
    269–282 (2014). https://doi.org/10.1145/2628136.2628161
26. VeriFun. http://www.verifun.de
27. Walther, C.: On proving the termination of algorithms by machine. Artif. Intell. 71(1), 101–157 (1994).
    https://doi.org/10.1016/0004-3702(94)90063-9
28. Walther, C., Schweitzer, S.: Verification in the classroom. J. Autom. Reason. Spec. Issue Autom. Reason.
    Theorem Proving Educ. 32(1), 35–73 (2004). https://doi.org/10.1023/B:JARS.0000021872.64036.41
29. Walther, C., Schweitzer, S.: Automated termination analysis for incompletely defined programs. In:
    Baader, F., Voronkov, A. (eds.) Proceedings of the 11th International Conference on Logic for Pro-
    gramming, Artificial Intelligence and Reasoning (LPAR-11). Lecture Notes in Artificial Intelligence,
    2005, vol. 3452, pp. 332–346. Springer, Montevideo (2005). https://doi.org/10.1007/978-3-540-32275-
    7_22


Publisher’s Note Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations.




123
