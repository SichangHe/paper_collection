                                              Cameleer: a Deductive Verification Tool for OCaml
                                                             (extended version)∗
                                                                     Mário Pereira and António Ravara
                                                       NOVA LINCS & DI, Nova School of Science and Technology, Portugal


                                                                                      Abstract
arXiv:2104.11050v2 [cs.LO] 6 Sep 2021




                                                  OCaml is particularly well-fitted for formal verification. On one hand, it is a multi-
                                              paradigm language with a well-defined semantics, allowing one to write clean, concise,
                                              type-safe, and efficient code. On the other hand, it is a language of choice for the imple-
                                              mentation of sensible software, e.g., industrial compilers, proof assistants, and automated
                                              solvers. Yet, with the notable exception of some interactive tools, formal verification has
                                              been seldom applied to OCaml-written programs. In this paper, we present the ongoing
                                              project Cameleer, aiming for the development of a deductive verification tool for OCaml,
                                              with a clear focus on proof automation. We leverage on the recently proposed GOSPEL,
                                              Generic OCaml SPE cification Language, to attach rigorous, yet readable, behavioral spec-
                                              ification to OCaml code. The formally-specified program is fed to our toolchain, which
                                              translates it into an equivalent program in WhyML, the programming and specification
                                              language of the Why3 verification framework. Finally, Why3 is used to compute verifica-
                                              tion conditions for the generated program, which can be discharged by off-the-shelf SMT
                                              solvers. We present successful applications of the Cameleer tool to prove functional cor-
                                              rectness of several significant case studies, like FIFO queues (ephemeral and applicative
                                              implementations) and leftist heaps, issued from existing OCaml libraries.



                                        1    Introduction
                                        Over the past decades, we have witnessed a tremendous development in the field of deductive
                                        software verification [13]. Interactive proof assistants have evolved from obscure and mysterious
                                        tools into de facto standards for proving industrial-size software projects. Notable examples
                                        include the Sel4 verified operating system kernel [25], and the verified compilers CompCert [23]
                                        and CakeML [35]. On the other end of the spectrum, the so-called SMT revolution and the
                                        development of reusable intermediate verification infrastructures contributed decisively to the
                                        development of practical automated deductive verifiers. Remarkable applications of automated
                                        verification tools include the verified version of the Microsoft’s Hypervisor [4] and, more recently,
                                        the use of ghost monitors [9] to analyze installation scenarios of the Debian distribution [3].
                                            Despite all the advances in deductive verification and proof automation, little attention
                                        has been given to the family of functional languages [32]. Taking the example of the OCaml
                                        language, if it is a language well-fitted for verification (given its well-defined semantics, clear
                                        syntax, and state-of-the-art type system), the community still misses an easy to use framework
                                        for the specification and verification of OCaml code.
                                            In this paper, we present Cameleer, a tool for the deductive verification of programs directly
                                        written in OCaml, with a clear focus on proof automation. Cameleer uses the recently proposed
                                        GOSPEL [6], a specification language for the OCaml language. We believe this is one of the
                                        strengths of our approach: firstly, GOSPEL makes a certain number of design choices, that turn
                                           ∗ This work is partly supported by the HORIZON 2020 Cameleer project (Marie Skłodowska-Curie grant

                                        agreement ID:897873) and NOVA LINCS (Ref. UIDB/04516/2020)
Cameleer: a Deductive Verification Tool for OCaml                                   Pereira and Ravara


it into a clean and digestible specification language; secondly, GOSPEL terms are written in
a subset of the OCaml language. In the scope of this work, we have also extended GOSPEL
to include implementation primitives, such as loop invariants and ghost code, evolving the
language from an interface specification language into a more mature proof tool.
    Cameleer takes as input an OCaml program annotated with GOSPEL specification and trans-
lates it into an equivalent counterpart in WhyML, the programming and specification language
of the Why3 framework [18]. Why3 is a toolset for the deductive verification of software, clearly
oriented towards automated proof. A distinctive feature of Why3 is that it can interface with
several different off-the-shelf theorem provers, namely SMT solvers, which greatly increases
proof automation. We believe that proof automation is another strong point of Cameleer, on
that can ease its adoption by regular OCaml programmers. In this paper, we present some case
studies of automatically verified OCaml modules with our tool.
Contributions. To the best of our knowledge, Cameleer is the first deductive verification tool
for annotated OCaml programs. It handles a realistic subset of the language, as demonstrated
by a comprehensive set of case studies. Another contribution of this paper is our translation of
the OCaml module language into WhyML. While sharing many common syntactic constructions,
OCaml and WhyML differ more significantly when it comes to their module systems. This poses
interesting challenges to our translation scheme.
Paper structure. This paper is organized as follows. Sec. 2 presents a simple example of a
verified OCaml program, intended as a smooth introduction to the Cameleer tool and GOSPEL
language. Sec. 3 describes the OCaml to WhyML translation mechanism implemented in the core
of Cameleer. Sec. 4 reports on relevant case studies verified with Cameleer, including ephemeral
and functorial data structures. Finally, we present some related work in Sec. 5 and conclude
with future work in Sec. 6. The source code of Cameleer and verified case studies are publicly
available online on the GitHub repository of the project1 .


2     Warmup Example
In this section, we present the verified implementation of the Fibonacci function. We first
present a purely applicative version of the mathematical definition, and then an efficient imple-
mentation using side-effects. This section is intended as a gentle introduction to the Cameleer
framework, the GOSPEL specification language, and certain important verification concepts
such as ghost code, loop invariants, and function contracts.
A logical definition. The classical mathematical definition can be readily translated, in
OCaml, into the following recursive function:
    let rec fib n =
      if n <= 1 then n else fib (n-1) + fib (n-2)
Though very elegant and concise, the above definition presents some pitfalls and raises a number
of questions: is this a total function (i.e., it terminates and is defined for every integer argument)
and could we avoid repeated computations in recursive calls? We focus now on the former and
shall address the latter in a moment.
    The Fibonacci function is, traditionally, only defined for a non-negative argument and this
is exactly the definition we follow here. Such a constraint on a function arguments is a precon-
dition, i.e., it limits the range of values the function arguments can take. We shall take this
opportunity to show a first piece of OCaml code annotated with GOSPEL specification:

    1 https://github.com/mariojppereira/cameleer
Cameleer: a Deductive Verification Tool for OCaml                               Pereira and Ravara


  let rec fib n =
    if n <= 1 then n else fib (n-1) + fib (n-2)
  (*@ requires n >= 0 *)
A GOSPEL specification is attached to the end of a function definition and is given within special
comments of the form (*@ ... *). The requires clause is used to state the precondition of a
function. In order to prove that every call to fib halts, we must provide a variant that strictly
decreases at each recursive call and has a lower-bound. Here, the value of n decreases at each
recursive call and is bounded from below thanks to the precondition. In GOSPEL, we express
the variant of a function as follows:
  let rec fib n = ...
  (*@ requires n >= 0
      variant n *)
The given precondition and the variant form what we call the function’s contract. Other than
serving as rigorous documentation of the function’s behavior, the interest of providing a contract
is to be able to formally prove that the code respects the given specification. This is where the
Cameleer toolchain enters the scene.
    Assuming function fib is contained in the OCaml file fibonacci.ml, starting a proof is as
easy as typing cameleer fibonacci.ml in a terminal. Cameleer translates the input program
into an equivalent WhyML counterpart and launches the Why3 graphical integrated development
environment. This allows us to visually inspect the verification conditions (VCs) generated by
Why3 for the fib function: two of them state the variant decreases and is not a negative value,
at each recursive call; the other two state the precondition holds for each recursive call. All of
these are easily discharged using SMT solvers, e.g., Alt-Ergo [10], CVC4 [2], or Z3 [12].
    The provided fib function is a naive implementation, as it unnecessarily repeats most inter-
mediate computations. Actually, this is not meant to be used as an executable implementation,
but rather as a logical description of the Fibonacci definition. This means fib works more as
mathematical function than a programming one. In order to instruct Cameleer to consider fib
a logical function, we decorate it with the OCaml attribute [@logic], as follows:
  let [@logic] rec fib n = ...
Under this setting, the fib function can now be used both inside specification clauses, as well
as in regular OCaml code.
A verified efficient implementation. Moving on to an efficient Fibonacci function, a clas-
sical approach is to implement it as a loop that goes from 0 to n-1, storing in two auxiliary
variables x and y the values for fib n to fib (n + 1) to compute fib (n + 2). The OCaml
code and GOSPEL specification are as follows:
  let fib_imp n =
    let y = ref 0 in
    let x = ref 1 in
    for i = 0 to n - 1 do
       let aux = !y in
       y := !x; x := !x + aux
    done;
    !y
  (*@ r = fib_imp n
         requires n >= 0
         ensures r = fib n *)
Cameleer: a Deductive Verification Tool for OCaml                                 Pereira and Ravara


As expected, fib_imp has the same precondition as fib. Here, we name the result of the
fibonacci function to mention it in the postcondition, introduced via the ensures clause.
This is exactly where we take advantage of the fact that fib can be used as a logical function,
since we state the returned value of fib_imp n is equal to fib n.
    As usual in deductive verification, the presence of the for loop requires us to supply a loop
invariant. Here, it boils down to
      for i = 0 to n - 1 do
        (*@ invariant !y = fib i && !x = fib (i + 1) *)
When fed to Cameleer, four verification conditions are generated for the given fib_impl im-
plementation: a loop invariant initialization, which states the invariant holds before the first
iteration; a loop invariant preservation, which states the invariant holds after each iteration;
two postcondition, one accounting for the case when the loop does not even execute (n = 0), the
other when the loop performs at least one iteration. All of them are automatically discharged.
The complete OCaml implementation of the Fibonacci implementation can be found online, at
the project’s GitHub repository2 .
The tale of the ghost code. The fib_imp function is a provably correct implementation
of the Fibonacci function. After finishing the proof, the specification has no computational
interest and should no be part of compiled code. This includes the fib function which is
only useful as a logical definition. This duality between parts of the code that are compiled
and other that have only proof interest is a common trait of deductive verification, commonly
known as ghost code [16]. Some parts of a program are marked with a special ghost status and
should be erased from the regular code after completing the proof effort. In Cameleer, we use
the [@ghost] attribute in order to change the status of some functions. For the example of
the fib definition, this is as simple as let [@logic] [@ghost] rec fib n. Building a sound
mechanism for ghost code erasure is far from a trivial task, especially in the presence of effectful
computations [30]. In Sec. 3.3, we discuss several solutions to deal with ghost code that we
could put into practice in the scope of the Cameleer project.


3     Methodology
This section gives an overview on the core of the Cameleer tool, from the OCaml code annotated
with GOSPEL specification to the generation of an equivalent WhyML program. In Sec. 3.1, we
describe how we use the GOSPEL toolchain to attach specification to certain nodes in the OCaml
AST. In Sec. 3.2 we define our OCaml to WhyML translation as a set of inference rules. Finally,
Sec. 3.3 explains how we are currently using Why3 as an intermediate verification framework.

3.1     Using GOSPEL toolchain
The Cameleer tool relies on the use of the GOSPEL toolchain3 to parse and manipulate the
OCaml abstract syntax tree. It provides a patched version of the OCaml parser that recognizes
GOSPEL special comments and converts them to regular OCaml attributes. For instance, the
fib_imp specification from Sec. 2 is translated into the following post-item attribute:
    let fib_imp n = ...
    [@@gospel ‘‘r = fib_main n requires n >= 0 ensures r = fib n’’]

    2 https://github.com/mariojppereira/cameleer/tree/master/examples/fibonacci.ml
    3 https://github.com/vocal-project/vocal
Cameleer: a Deductive Verification Tool for OCaml                                         Pereira and Ravara


The payload of a GOSPEL attribute is, hence, a string that contains the user-supplied specifica-
tion4 . The GOSPEL attributes are processed by a dedicated parser and type-checker [6], where
specifications are attached to nodes of a patched version of the OCaml AST. This custom AST
is the entry-point for our OCaml to WhyML translation, which we describe next.

3.2     Translation into WhyML
We present our translation from OCaml to WhyML as set of inference rules. All the auxiliary
functions and predicates are total definitions. We focus here on a subset of the OCaml and
WhyML languages. The complete definitions are depicted in Fig. 1 and Fig. 2, respectively. On
the WhyML side, we omit the definition of t which stands for the logical subset of WhyML. For
a comprehensive definition of this part of WhyML, we refer the reader to the Why3 reference
manual [36, Chap. 7]. We do not intend to use this section as an heavy formalization of our
translation, but rather as a comprehensive presentation of the OCaml subset that Cameleer can
handle. Cameleer will report a dedicated error message if a user tries to translate an OCaml
program that syntactically falls out of the supported fragment. It is worth noting that our
translation is purely syntactic, as we build on the GOSPEL toolchain which is based on a PPX
approach. In particular, this means that typing the translated OCaml program is left as a task
to Why3. Making our translation type-directed, or at least type-aware, is left as future work.
Expressions. Selected OCaml expressions include variables (x ranges over program variables,
while f is used for function names), the conditional if..then..else, local bindings of (possibly
recursive) expressions, function application, records manipulation (for simplicity, we assume
every field to be mutable), treatment of exceptions, loop construction, and finally the assert
false expression. Values include numerical and Boolean constants, as well as anonymous
functions where arguments are annotated with a ghost status. We only consider functions as
valid recursive definitions and application is limited to the application of a function name to
a list of arguments. The latter is just to ease our presentation; the former is due to recursive
definitions in WhyML being limited to functions. Finally, A notation stands for a (possibly
empty) placeholder of OCaml attributes, representing the original place in the expression where
GOSPEL elements are introduced. For instance, the first A in a let..rec expression can
contain the [@ghost] and [@logic] attribute, while the second one stands for the function
specification. We omit the definition of τ and t, respectively from the OCaml and the WhyML
sides. The former stands for the grammar of OCaml types, while the latter is the logical subset
of WhyML.
    The OCaml and WhyML languages are very similar, hence our translation of expressions
is mostly an isomorphism. We give the complete set of rules in Appendix A and explain
here only the more subtle aspects of this translation. Let us begin with the translation of an
OCaml expression of the form let..rec..in into its WhyML counterpart. The corresponding
translation rule is the following:

                             e0 f unction βx, e00    e1 expression e01
                     ¬is_ghost(A0 )     kind (A0 ) = K     A1 function spec S1
      (ERec)
               let A0 rec f0 = e0 A1 in e1 expression rec K f (βx) S1 = e00 in e01

For the sack of presentation, we use here only a single recursive function and omit any mutually
recursive definition. In fact, translating a set of mutual definitions simply amounts to a recursive

   4 In fact, GOSPEL elements can be directly provided using attributes in the source code.
Cameleer: a Deductive Verification Tool for OCaml                              Pereira and Ravara




 e      ::= x | ν | if e then e else e | match e with 8 p ⇒ e                         Expressions
         | let A x = e A in e
         | let A rec f = e A and f = e A in e | f ē
         | {f = e} | e.f | e.f ← e
         | raise Eē | try e with E x̄ ⇒ e
         | while e do A e done | assert false
 p      ::= _ | x | p | C(p) | p 8 p | p as x | p : τ | exception p                       Patterns
 ν      ::= n | true | false | fun A (xβ) → e                                               Values
 β      ::= reg | ghost                                                           Ghost attribute
 τ      ::= α | τ → τ | τ | τ C                                                  Type expression
 π      ::= βτ                                                            Type with ghost status
 d      ::= exception E : π | type td and td                                Top-level declarations
         | let A f = e A | let A rec f = e A and f = e A
         | module M = m
 td     ::= α T | α T = τ | α T = { f : π } A | α T = 8 C of τ                    Type definition
 m      ::= struct d end | functor(X : mt) → m                                            Modules
 mt ::= sig s end                                                                   Module types
 s      ::= val A f : π A | type td and td                                              Signatures
 p      ::= d                                                                             Program


                                   Figure 1: Syntax of core OCaml.


call to our expressions translation procedure, as depicted in Appendix A. Let us consider the
following generic expression as a running example to explain the (ERec) rule:
     let rec foo (x [@ghost]) y = e0
     (*@ r = foo x y
           requires ... variant ... ensures           ... *)
     in e1
The second premise of the rule translates expression e1 and it simply amounts to a recursive
call to the translation scheme. The first premise is a bit more evolving, hence we explain it in
more detail. The definition of foo is de-sugared by the OCaml parser into the following Curried
expression:
     let rec foo = fun (x [@ghost]) -> fun y -> e
When translating into WhyML, we revert such an operation: we traverse the body of foo,
building a list of ghost-annotated arguments from the argument of each fun construction. The
body of the translated function is the body of the last fun. This is done in the first premise
of the rule, using the f unction operation. This conversion into multi-argument functions is
justified by the limits of Why3 when it comes to higher-order and anonymous functions. In
WhyML, one can only define pure anonymous functions, i.e., free of any side effects. Hence,
Cameleer: a Deductive Verification Tool for OCaml                               Pereira and Ravara




 e     ::= x | ν | if e then e else e | match e with 8 p ⇒ e end                      Expressions
        | let K βx = e in e
        | rec K f (βx) S = e with K f (βx) = e S in e | f ē
        | {f = e} | e.f | e.f ← e
        | raise Eē | try e with E x̄ ⇒ e end
        | while e do I e done | absurd | ghost e
 p     ::= _ | x | p | Cp | p 8 p | p as x | p : τ | exception p                         Patterns
 ν     ::= n | true | false | fun K (βx) S → e                                             Values
 β     ::= reg | ghost                                                               Ghost status
 τ     ::= α | τ → τ | τ | C τ                                                   Type expression
 π     ::= βτ                                                             Type with ghost status
 K     ::= reg | logic                                                             Function kind
 S     ::= requires t ensures t variant t                                  Function specification
 I     ::= invariant t variant t                                               Loop specification
 d     ::= exception E : π | type td with td                               Top-level declarations
        | let K f = e
        | let rec K f (βx) S = e with K f (βx) S = e
        | val K βf (x : π) S : π | scope M d end
 td ::= T α | T α = τ | T α = { f : π } invariant t̄ | T α = 8 C τ                Type definition
 p     ::= module M d end                                                                Program


                                    Figure 2: Syntax of core WhyML.


directly translating the Curried definition of foo would yield a syntactically correct WhyML
expression, however this would be rejected by the language type-and-effect system.
    The other three premises deal with specification elements. The first uses the is_ghost op-
eration to test whether the [@ghost] attribute is provided in A0 . If that is the case (rule
(ERecGhost) in Appendix A), the function body is translated into ghost e. The kind of a
function is either reg (only usable as a program function) or logic (also usable inside speci-
fication). We introduce the kind (·) operation, which also retrieves the function kind from A0
(in case of a regular function, the attribute can be omitted). The last premise translates the
supplied GOSPEL preconditions, variants, and postconditions into the WhyML specification lan-
guage. We omit the definition of function spec since this is a trivial (syntactic) transformation.
    We highlight two more interesting cases of expressions translation: the assert false con-
struction and local non-recursive bindings. Contrarily to any other assert expression, assert
false is used in OCaml to indicate unreachable points in the code and “is treated in a spe-
cial way by the OCaml type-checker” 5 . WhyML features the absurd construction which has
the exact same semantics, which greatly simplifies our translation effort (rule (EAbsurd) in
Appendix A). Finally, when translating a let..in expression, we need to account for both the

     5 To quote a comment from the OCaml compiler source code itself.
Cameleer: a Deductive Verification Tool for OCaml                                Pereira and Ravara


introduction of a local function, as well as the binding of a non-functional value. The translation
rule for the latter is as follows:

         ¬is_ghost(A)         ¬is_functional(e0 )    e0 expression e00   e1 expression e01
(ELet)
                      let A x = e0 A0 in e1 expression let reg x = e00 in e01

This rule stands for the sub-case where the bound variable is regular, hence the use of the
reg kind. Any GOSPEL specification possibly contained in A0 is ignored. Finally, the use of
the auxiliary predicate is_functional(·) is what allows us to distinguish between locally-bound
variables and functions. This predicate decides whether e0 is a fun x -> ... expression, in
which case we introduce a WhyML local function (rule (ELetFun) in Appendix A). This
approach does not take partial applications into account, which are directly translated into its
WhyML counterpart. If a partial application introduces an effectful computation, this will be
rejected by the Why3 type system.

Top-level declarations. Selected top-level declarations include exceptions and type declara-
tion, (mutually-recursive) function definition, and introduction of sub-modules. An exception
takes a list of π values, types annotated with a ghost status, to account for the possibility
of ghost arguments. In Why3 vocabulary, this is the mask of an exception [30, Chap. 3.1].
The complete set of translation rules for top-level declarations and type definitions is given in
Appendix B. We highlight here the cases of record type definition and sub-modules.
    The attribute A after a record type definition is used to express in GOSPEL a type invariant,
i.e., a predicate that every inhabitant of such type must satisfy. Type invariants are readily
supported by Why3, as depicted in rule (TDRecord) in Fig. 5, Appendix B. Each field of
the record type is also annotated with a ghost status. This is a common practice in deductive
verification: some fields act as logical models of the record value; these can be explored within
the proof to reason about the represented data structure. It is worth noting that in WhyML,
contrarily to OCaml, type arguments are introduced on the right-hand side of the type name.
    Finally, translation of a sub-module definition is guided by the following rule:

                                              m module d
              (DModule)
                             module M = m declaration scope M d end

We translate the module expression m into a list of WhyML declarations. WhyML does not
feature the notion of sub-module, hence we encapsulate the translated declarations into a scope,
the WhyML unit for namespaces management. In what follows, we provide a more detailed
account of the WhyML module system and its differences with respect to that of OCaml.
Modules. The most interesting cases in our translation is how we deal with the modules
language from the OCaml side. A WhyML program is a list of modules, a module is a list of
top-level declarations, and declarations can be organized within scopes.
    The first module expression we take into account is the struct..end construction. This
is translated into a WhyML declarations, as depicted in rule (MStruct) (Appendix C). We
note this does not change the structure and code organization of the original program, since
a struct..end expression follows a module declaration. Hence, a declaration of the form
module M d¯ end is translated into scope M d¯ end.
    Functors are a central notion when programming in OCaml, so it is out of question to develop
a verification tool for OCaml without a (at least minimal) support for functors. WhyML does
   Cameleer: a Deductive Verification Tool for OCaml                                         Pereira and Ravara


   not feature a syntactic construction for functors; instead, these are represented as modules
   containing only abstract symbols [19]. Thus, we propose the following translation rule:

                                     mt module type d        m module d0
             (MFunctor)
                             functor(X : mt) → m module scope X d end d0

   Each functor expression is translated into a WhyML scope followed by a list of declarations.
   For instance, the OCaml functor module Make = functor (X: ...) -> struct ... end, is
   translated into the following WhyML excerpt: scope Make scope X ... end ... end. The
   given transformation is the dual of what is actually implemented in the Why3 extraction
   machinery: every WhyML expression of the form scope A scope B ... is translated into
   module A (B: ...) ..., as long as scope B features only abstract symbols.
   Signatures. The argument of a functor is expressed as a module type, i.e., a signature of
   the form sig..end. This encapsulates a list of declarations belonging to the OCaml signature
   language, which are translated into a list of WhyML expressions, according to rule (MTSig)
   (Appendix C). Contrarily to OCaml, WhyML does not impose a separation between signature
   (interface) and structure (implementation) elements. In particular, the WhyML surface lan-
   guage allows one to include non-defined val functions and regular let definitions in the same
   namespace. We give the following translation rule for val declarations:

         ¬is_ghost(A)       kind(A) = K         A0 function spec S       π, A0 function args x : π 0 , πres
(SVal)
                             val A f : π A0 signature val K f (x : π) S : πres

   The name of the arguments are retrieved from the function specification (Sec. 4.2 features an
   example of such case). Non-defined functions can also be declared as ghost and/or logical
   functions. For brevity, the case of ghost val is omitted. The complete set of translation rule
   for signature items can be found in Appendix D.
   Programs. An OCaml program is simply a list of top-level declarations. These are translated
   into a WhyML module, as follows:

                                               d declaration d0
                          (Program)         program
                                        d              module M d0 end

   The name M of the generated module is issued from the OCaml file that contains the original
   program. If file foo.ml contains the program p, it gets translated into module Foo p end. In
   summary, we generate a WhyML program containing a single module, which represents the
   top-level module of an OCaml file. In turn, each sub-module is translated into a WhyML scope,
   with a special treatment for functorial definitions.

   3.3     Interaction with Why3
   Why3 front-end. One distinguished feature of the Why3 architecture is that it can be ex-
   tended to accommodate new front-end languages [36, Chap. 4]. Building on the translation
   scheme presented in previous section, we use the Why3 API to build an in-memory representa-
   tion of the WhyML program and to register OCaml as an admissible input format for Why3. We
   can use any Why3 tool, out of the box, to process a .ml file. For instance, one could use directly
   the command why3 ide bar.ml to trigger our OCaml input format and to call the Why3 IDE
   on the translation of the bar.ml file.
Cameleer: a Deductive Verification Tool for OCaml                                 Pereira and Ravara


    Other than the ide, we could use the extract command to erase any trace of ghost from the
original code and print an equivalent OCaml implementation. This would provide us with the
necessary guarantees about the semantics and typedness of the extracted program. However, we
believe a solution that is directly integrated with the OCaml compilation chain is more organic
and natural to the programmer. We currently working on a PPX that generates a new OCaml
AST without ghost code, which uses the Why3 extraction as an internal ingredient.
Limitations of using Why3. WhyML and GOSPEL are very similar specification language.
Moreover, they share some fundamental principals, namely the arguments of functions are not-
aliased by construction and each data structure carries an implicit representation predicate.
This makes the translation from GOSPEL to WhyML a very natural process. However, one
can use GOSPEL to formally specify some OCaml programs which cannot be translated into
WhyML. This is much evident when it comes to recursive ephemeral data structures. Consider,
for instance, the cell type definition from the Queue module of the OCaml standard library6 :
    type ’a cell = Nil | Cons of { content: ’a; mutable next: ’a cell }
As we attempt to translate such data type into WhyML, we get the following error:
    This field has non-pure type, it cannot be used in a recursive type definition
Recursive mutable data types are beyond the scope of Why3’s type-and-effect discipline [15].
The solution would be to resort to an axiomatic memory model of OCaml in Why3 [20], or to
employ a richer program logic, e.g., Separation Logic [33] or Implicit Dynamic Frames [34]. We
leave such an extension to the Cameleer infrastructure for future work.


4     Case Studies
4.1     FIFO Queue
Our first case study is the implementation of a FIFO queue, implemented as an ephemeral
data-structure. The complete OCaml development and GOSPEL specification are presented at
Cameleer’s GitHub repository 7 . We also publish online a simpler, purely applicative version of
this data structure 8 , which we picked from the OCamlGraph library9 . This case study follows
the standard approach of using a pair of lists to store the elements of the queue, as follows:
  type ’a t = { mutable front: ’a list; mutable rear : ’a list;
                mutable view : ’a list [@ghost]; }
 (*@ invariant (front = [] -> rear = []) && view = front ++ List.rev rear *)
In order to formally express the behavior of the queue data structure, we equip type t with a
model field and a GOSPEL invariant. The view field is used to represent the whole queue as a
single list. This is a ghost field since it has no computational interest. Front elements are stored
in the correct order and rear elements are stored in reversed order. Elements are pushed into
the head of the rear list and popped off the head of front. This data structure also maintains
the invariant that if front is empty, then so is rear.
    In what follows, the specification of operations on a queue is solely given in terms of the
view field. The push operation is implemented and specified as follows:

    6 https://caml.inria.fr/pub/docs/manual-ocaml/libref/Queue.html
    7 https://github.com/mariojppereira/cameleer/blob/master/examples/ephemeral_queue.ml
    8 https://github.com/mariojppereira/cameleer/blob/master/examples/applicative_queue.ml
    9 https://github.com/backtracking/ocamlgraph
Cameleer: a Deductive Verification Tool for OCaml                              Pereira and Ravara


  let push x q =
    if is_empty q then q.front <- [x] else q.rear <- x :: q.rear;
    q.view <- q.view @ [x]
  (*@ push x q
        ensures q.view = (old q.view) @ [x] *)
The postcondition asserts the updated view field of q consists of the value of view before the
call (old q.view), extended with the new element x. If the queue is empty, then x is pushed
into the front list; otherwise, the new element is added as the new head of rear.
    Next, we present the implementation of the pop operation. This is as follows:
  let pop q = match q.front with
    | [] -> raise Not_found
    | [x] ->
        q.front <- List.rev q.rear; q.rear <- []; q.view <- tail_list q.view;
        x
    | x :: f ->
        q.front <- f; q.view <- tail_list q.view;
        x
  (*@ x = pop q
        raises Not_found -> is_empty (old q)
        ensures x :: q.view = (old q).view *)
If the queue is empty we raise the Not_found exception from the OCaml standard library. A
raises clause is used to introduce what we call an exceptional postcondition. We must be
careful enough to specify that the is_empty property is verified by pre-state of q. Otherwise,
had we used is_empty q, this would propagate into our proof context that the queue is not
empty after the execution of pop. This would prevent proving the safety of the next function.
    The most interesting function in our development of ephemeral queues is the concatenation
of two such queues. The implementation is as follows:
  let transfer (q1: ’a t) (q2: ’a t) : unit =
    while not (is_empty q1) do push (pop q1) q2 done
  (*@ transfer q1 q2
        raises   Not_found -> false
        ensures q1.view = [] && q2.view = old q2.view @ old q1.view *)
The transfer operation takes queues q1 and q2 as arguments, and migrates the elements of
the former to the end of the latter. Moreover, it clears the contents of its first argument. By
design, GOSPEL assumes q1 and q2 are two separated queues, i.e., not aliased. The raises
clause states no Not_found exception is raised during execution of transfer. In fact, since the
while loop is guarded by the not (is_empty q1) property, we know it is safe to call pop q1.
Feeding this program to Cameleer generates a total of 8 VCs, from which we are only able to
prove the exceptional postcondition and the first clause of the regular postcondition condition.
With no surprise, this comes from the fact that we are missing a suitable loop invariant. In
what follows, we refine the specification to completely prove the transfer function.
    In order to prove termination, we use the length of the view model from q1 as a decreasing
measure, as follows:
     (*@ variant List.length q1.view *)
In order to prove the remaining VCs, it comes with no surprise that we need a suitable loop
Cameleer: a Deductive Verification Tool for OCaml                               Pereira and Ravara


invariant. First, we turn the type invariant property into a loop invariant, as follows:
      (*@ invariant (q1.front = [] -> q1.rear = []) &&
                    (q2.front = [] -> q2.rear = []) *)
      (*@ invariant q1.view = q1.front @ List.rev q1.rear &&
                    q2.view = q2.front @ List.rev q2.rear *)
Although this makes the loop invariant more cumbersome, it is actually almost a mechanical
process to include the type invariant in the loop invariant. With such a specification, we are
able to discharge every VC of transfer, except for the second postcondition.
   To complete this proof, we need to be a little more creative. The idea is the following: if we
pick an arbitrary loop iteration, at that point of execution we would have already transferred a
prefix of the elements from q1 and would have concatenated those into q2. In order to represent
such prefix of q1, we introduce an auxiliary ghost variable, as follows:
  let transfer q1 q2 =
    let [@ghost] done_view = ref [] in ...
At each iteration, we must update the value of done_view as follows:
     while not (is_empty q1) do (*@ variant ... invariant ... *)
       done_view := !done_view @ [head_list q1.view];
       push (pop q1) q2
    done
Once again, the done_view is a ghost variable, so any part of the program that manipulates it
should be erased from the code. Thus, the above assignment should not incur a penalty on the
execution time of transfer. Finally, we complete the loop invariant as follows:
        (*@ invariant old q1.view = !done_view @ q1.view *)
        (*@ invariant q2.view = old q2.view @ !done_view *)
The first condition maintains that todo_view is indeed a prefix of q1.view; the second condition
states that the current state of q2 consists of the elements from todo_view concatenated to the
sequence of original elements of q2. With the updated invariant, we are finally able to discharge
every generated VC for transfer.

4.2     Leftist Heap
Functor definition. The next case study is the implementation of a heap data structure.
We adopt the leftist heap variant [11, 26], which we picked from the OCaml-containers library10 .
This is an applicative implementation, following the approach by C. Okasaki [29, Chap. 3.1].
    The fundamental interest of using heaps is to be able to quickly access the minimum element
of the collection. Thus, the elements of this data structure must be equipped with a total
preorder, which is crucial to guarantee the correct behavior of the heap implementation. In
OCaml, such kind of restrictions on types are naturally implemented using functors. For leftist
heaps, we begin by introducing the following module type to represent a total preorder:
  module type TOTAL_PRE_ORD = sig
    type t
    (*@ function le : t -> t -> bool *)
    (*@ axiom reflexive : forall x. le x x *)

  10 https://github.com/c-cube/ocaml-containers
Cameleer: a Deductive Verification Tool for OCaml                                Pereira and Ravara


     (*@ axiom total     : forall x y. le x y \/ le y x *)
     (*@ axiom transitive: forall x y z. le x y -> le y z -> le x z *)

    val leq : t -> t -> bool
    (*@ b = leq x y
          ensures b <-> le x y *)
  end
Using GOSPEL, we introduce a purely logical function le defined using the classic axioms of
reflexivity, totality, and transitivity. Next, the specification of the regular function leq should
be read as “this function implements the logical function le”. Using the above TOTAL_PRE_ORD
type, the implementation of leftist heaps is encapsulated in the following functor Make:
  module Make(E : TOTAL_PRE_ORD) = struct type elt = E.t ... end
The type equation elt = E.t ensures that elements of type elt (used to represent the elements
of the heap) are inherit the total preorder relation from module E.
Leftist property. We use the following data type definition to represent leftist heaps:
     type t = E | N of int * elt * t * t
A leftist heap is represented as a binary tree where each node is attached a rank value. Generally
speaking, the rank of a node is defined as the length of the shortest path from that node to an
empty node. In GOSPEL, this is as simple as follows:
     (*@ function rank (h: t) : integer =
           match h with E -> 0 | N _ _ l r -> 1 + min (rank l) (rank r) *)
Using the general notion of rank, one can define the notion of leftist property: the rank of any
left child is always greater or equal to the rank of the right sibling. This is captured by the
following GOSPEL definition:
     (*@ predicate leftist (h: t) = match h with
           | E -> true
           | N n _ l r ->
               n = rank h && leftist l && leftist r && rank l >= rank r *)
This property also gives the value of the element storing the rank in the structure. Other than
the leftist property, leftist heaps should obey the general laws of heaps: the element in each
node is less or equal to the elements at its children. The GOSPEL definition is as follows:
     (*@ predicate is_heap (h: t) = match h with
           | E -> true
           | N _ x l r -> le_root x l && is_heap l && le_root x r && is_heap r *)
where le_root is a predicate that states a given element is less or equal to the root of a heap:
     (*@ predicate le_root (e: elt) (h: t) =
           match h with E -> true | N _ x _ _ -> E.le e x *)
Finally, we define what is a leftist heap:
     (*@ predicate leftist_heap (h: t) = is_heap h && leftist h *)
Logical definition of minimum element. When describing the logical behavior of a heap
data structure, one must pay particular attention to the definition of the minimum element.
We need to define what is the physical minimum element of the heap, as follows:
Cameleer: a Deductive Verification Tool for OCaml                                      Pereira and Ravara


      (*@ function minimum (h: t) : elt *)
      (*@ axiom minimum_def: forall l x r n. minimum (N n x l r) = x *)
The minimum function is only significantly defined for the case of non-empty heaps11 . We have
now the necessary building blocks to formally specify leftist heaps operations.
Heap operations. We present here only two heap operations, _make_node and merge. The
complete OCaml development can be found online12 . The first function builds a new node,
given an element x and subtrees a and b:
  let _make_node x a b =
    if _rank a >= _rank b then N (_rank b + 1, x, a, b)
    else N (_rank a + 1, x, b, a)
  (*@ h = _make_node x a b
      requires leftist_heap a && leftist_heap b && le_root x a && le_root x b
      ensures leftist_heap h && minimum h = x
      ensures occ x h = 1 + occ x a + occ x b
      ensures forall y. x <> y -> occ y h = occ y a + occ y b *)
The leftist property is ensured by the if..then..else expression, where _rank is a function
that simply retrieves the rank of a node, i.e., the first argument of the N constructor or 0 in
case the heap is empty. Both a and b must be leftist_heaps and x must no greater than
the roots of the two arguments. We give a specification of the heap in terms of the multiset of
its elements. The resulting heap h is a leftist_heap, with minimum element x. The number
of occurrences of x increases by one, whereas the occurrences of any element different from x
remain the same. Finally, the nuclear operation merge is defined as follows:
      let rec merge t1 t2 = match t1, t2 with
        | t, E | E, t -> t
        | N (_, x, a1, b1), N (_, y, a2, b2) ->
            if E.leq x y then _make_node x a1 (merge b1 t2)
            else _make_node y a2 (merge t1 b2)
      (*@ h = merge t1 t2
            requires leftist_heap t1 && leftist_heap t2
            variant size t1 + size t2
            ensures leftist_heap t && forall x. occ x h = occ x t1 + occ x t2 *)
If the root x of heap t1 is no greater than the root of t1, we build a new heap with root x;
otherwise, we the new root is the root of t2. The call to function _make_node ensures the
leftist_heap property for the returned heap. We use the logical function size in the variant
of merge, which is the straightforward definition of the number of nodes in a heap.
    Addition and removal of the minimal element are straightforwardly defined. Due to space
constraints, we do not present those here and refer the reader to the online repository for the
complete OCaml development. This also includes the filter and delete_all higher-order
functions. All the generated VCs for leftist heap operations were automatically discharged.

4.3     Other case studies
Table 1 in Appendix E summarizes the case studies performed with Cameleer. The second
column features the number of non-blank lines of OCaml code, while the third one stands for
   11 In GOSPEL, logical functions are total. The value returned by minimum E exists, but one can prove no

property about it.
   12 https://github.com/mariojppereira/cameleer/blob/master/examples/leftist_heap.ml
Cameleer: a Deductive Verification Tool for OCaml                               Pereira and Ravara


the number of non-blank lines of GOSPEL specification. We have put an effort to use Cameleer to
verify programs of different natures. These include numerical programs (binary multiplication,
different factorial implementations, fast exponentiation, and integer square root), sorting and
searching algorithms, data structures implemented as functors, historical algorithms (checking
a large routine by Turing, Boyer-Moore’s majority algorithm, and binary tree same fringe), and
logical algorithms (conversion of a propositional formula into conjunctive normal form).


5     Related Work
Automated deductive verification tools. One can cite Why3, F* [1], Dafny [27], and
Viper [28] as well-succeed automated deductive verification tools. Formal proofs are conducted
in the proof-aware language of these frameworks, and then executable reliable code can be
automatically extracted. In the Cameleer project, we chose to develop a verification tool that
accepts as input a program written directly in OCaml, instead of a dedicated proof language.
Our specification language, GOSPEL, is very close to the OCaml language itself, hence we believe
this does not impose a big burden for the regular OCaml practitioner.
    Regarding verification tools that tackle the verification of programs written in mainstream
languages, we can cite Frama-C [24] and VeriFast [22]. The former is a framework for the
static analysis of C code; the latter can be used to verify functional correctness of C and Java
programs. Despite the remarkable case studies verified with these tools, C and Java code can
quickly degenerate into a nightmare of pointer manipulation and tricky semantic issues. We
argue OCaml is a language better suited for formal verification.
Deductive verification of OCaml programs. To the best of our knowledge, CFML [5] was
the only tool available for the deductive verification of code directly written in OCaml. It takes
as input an OCaml program and translates it into Coq, together with its characteristic formulae.
A characteristic formulae is a higher-order statement that captures the semantics of the original
program. Proofs are conducted using an embedding of Separation Logic inside Coq. The CFML
tool has already been used to verify several interesting OCaml modules, including ephemeral
data structures and higher-order functions. Recently, CFML was extended with support for
time credits and it was successfully applied in the verification of functional correctness and
time complexity claims of non-trivial data structures and algorithms [8, 21].
    The VOCaL project aims at developing a mechanically verified OCaml library [7]. One
of the main novelties of this project is the combined use of three different verification tools:
Why3, CFML, and Coq. The GOSPEL specification language was developed in the scope of this
project, as a tool-agnostic language that could be manipulated by any of the three mentioned
frameworks. It was our participation on the VOCaL project that inspired us, in the first place,
to develop Cameleer. We believe Cameleer can be readily included in the VOCaL ecosystem,
complementing the toolchains [14] that are currently used to build the verified library.


6     Conclusions and Future Work
In this paper we presented Cameleer, a tool for deductive verification of OCaml-written code.
The core of Cameleer is a translation from OCaml annotated code into WhyML, the program-
ming and specification language of the Why3 verification framework. OCaml and WhyML have
many common traits (both in their syntax and semantics), which provides us with good guaran-
tees about soundness of Cameleer translation. We have already applied Cameleer to successfully
verify functional correctness and safety of 14 realistic OCaml modules. These include implemen-
tations issued from existing libraries, and scale up to data structures implemented as functors
Cameleer: a Deductive Verification Tool for OCaml                               Pereira and Ravara


and tricky effectful computations. These results encourage us to continue developing Cameleer
and apply it to the verification of larger case studies.
What we do not support. Currently, we target a subset of the OCaml language which
roughly corresponds to caml-light, with basic support for the module language (including
functors). Also, WhyML limits effectful computations to the cases where alias is statically
known, which limits our support for higher-order functions and mutable recursive data struc-
tures. Adding support for the objective layer of the OCaml language would require a major
extension to the GOSPEL language and a redesign of our translation into WhyML. Nonetheless,
Why3 has been used in the past to verify Java-written programs [17], so in principle an encoding
of OCaml objects in WhyML is possible.
    GADTs extend usual algebraic data types with a lightweight form of dependent typing in
OCaml. The use of GADTs allows one to logically constraint the values that can inhabit a
type in a certain point of the program. The WhyML type system does not, currently, include
a notion close to GADTs. However, since this a proof-aware language an interesting route for
future work would be to explore if it is possible to encode in WhyML the reasoning of GADTs
without extending its type system. In particular, if it would be possible to leverage on the
notion of type invariant to achieve similar results as those statically provided by GADTs.
    Another interesting feature of OCaml we currently do not support are polymorphic variants.
Polymorphic variants are more flexible than ordinary variants, as they are not tied to a par-
ticular type declaration and can be easily extended according to use scenarios. This flexibility,
however, leads to a more complicated typing process for polymorphic variants, when compared
to regular ones. Once again, extending Cameleer to deal with polymorphic variants requires
extending Why3 itself. This would likely mean a considerable redesign of its type system.
    Finally, Why3 constrains the use of higher-order functions to pure computations and this is
also the case with Cameleer. A possible solution for such limitation would be to use defunc-
tionalization to convert an higher-order program into an equivalent first-order one. In previous
work, we have already explored the use of defunctionalization for verification of stateful higher-
order programs in Why3 [31]. However, defunctionalization is a whole-program transformation
which severally constrains its applicability. Next, we describe a more robust solution, which
amounts at using a richer verification framework to reason about higher-order with effects.
Interface with Viper and CFML. We want to keep improving Cameleer with the ability to
verify a growing class of OCaml implementations. This includes pointer-based data structures
and effectful higher-order computations. Given the limitations of Why3 to deal with such class
of programs, we believe the solution is to extend Cameleer to include translation into different
intermediate verification languages. We are considering targeting the Viper infrastructure and
the CFML tool. On one hand, Viper is an intermediate verification language based on Separa-
tion Logic but oriented towards SMT-based software verification, allowing one to automatically
verify heap-dependent programs. On the other hand, the CFML tool already provides a trans-
lation from OCaml into Coq, allowing one to verify effectful higher-order functions. Even if it
relies on an interactive proof assistant, CFML provides a comprehensive library of tactics that
ease the proof effort. Our ultimate goal is to turn Cameleer into a verification tool that can
simultaneously benefit from the best features of different verification frameworks. Our motto:
we want Cameleer to be able to verify parts of an OCaml module using Why3, others with Viper,
and finally some specific functions with CFML.

Acknowledgements. We thank Jean-Christophe Filliâtre and the anonymous reviewers for
feedback on previous versions of this paper. We also thank Simon Cruanes for encouraging us
to prove the Leftist Heaps implementation from the ocaml-containers library.
Cameleer: a Deductive Verification Tool for OCaml                                    Pereira and Ravara


References
 [1] Danel Ahman, Catalin Hritcu, Kenji Maillard, Guido Martínez, Gordon Plotkin, Jonathan
     Protzenko, Aseem Rastogi, and Nikhil Swamy. Dijkstra monads for free. In 44th ACM SIGPLAN
     Symposium on Principles of Programming Languages (POPL), pages 515–529. ACM, January
     2017.
 [2] Clark Barrett, Christopher L. Conway, Morgan Deters, Liana Hadarean, Dejan Jovanovi’c, Tim
     King, Andrew Reynolds, and Cesare Tinelli. CVC4. In Ganesh Gopalakrishnan and Shaz Qadeer,
     editors, Proceedings of the 23rd International Conference on Computer Aided Verification (CAV
     ’11), volume 6806 of Lecture Notes in Computer Science, pages 171–177. Springer, July 2011.
     Snowbird, Utah.
 [3] Benedikt F. H. Becker, Nicolas Jeannerod, Claude Marché, Yann Régis-Gianas, Mihaela Sighire-
     anu, and Ralf Treinen. Analysing installation scenarios of debian packages. In Armin Biere and
     David Parker, editors, Tools and Algorithms for the Construction and Analysis of Systems - 26th
     International Conference, TACAS 2020, Held as Part of the European Joint Conferences on The-
     ory and Practice of Software, ETAPS 2020, Dublin, Ireland, April 25-30, 2020, Proceedings, Part
     II, volume 12079 of Lecture Notes in Computer Science, pages 235–253. Springer, 2020.
 [4] Bernhard Beckert and Michał Moskal. Deductive verification of system software in the Verisoft
     XT project. KI, 24(1):57–61, February 2010.
 [5] Arthur Charguéraud. Characteristic formulae for the verification of imperative programs. In
     Proceedings of the 16th ACM SIGPLAN international conference on Functional programming,
     pages 418–430, 2011.
 [6] Arthur Charguéraud, Jean-Christophe Filliâtre, Cláudio Lourenço, and Mário Pereira. GOSPEL
     — Providing OCaml with a Formal Specification Language. In Maurice H. ter Beek, Annabelle
     McIver, and José N. Oliveira, editors, Formal Methods - The Next 30 Years - Third World Congress,
     FM 2019, Porto, Portugal, October 7-11, 2019, Proceedings, volume 11800 of Lecture Notes in
     Computer Science, pages 484–501. Springer, 2019.
 [7] Arthur Charguéraud, Jean-Christophe Filliâtre, Mário Pereira, and François Pottier. VOCAL –
     A Verified OCAml Library, September 2017. ML Family Workshop 2017.
 [8] Arthur Charguéraud and François Pottier. Verifying the correctness and amortized complexity of a
     union-find implementation in separation logic with time credits. Journal of Automated Reasoning,
     62(3):331–365, 2019.
 [9] Martin Clochard, Claude Marché, and Andrei Paskevich. Deductive verification with ghost moni-
     tors. Proc. ACM Program. Lang., 4(POPL), December 2019.
[10] Sylvain Conchon, Albin Coquereau, Mohamed Iguernlala, and Alain Mebsout. Alt-Ergo 2.2. In
     SMT Workshop: International Workshop on Satisfiability Modulo Theories, Oxford, United King-
     dom, July 2018.
[11] Clark Allan Crane. Linear Lists and Priority Queues as Balanced Binary Trees. PhD thesis,
     Stanford, CA, USA, 1972. AAI7220697.
[12] Leonardo de Moura and Nikolaj Bjørner. Z3: An efficient smt solver. In C. R. Ramakrishnan and
     Jakob Rehof, editors, Tools and Algorithms for the Construction and Analysis of Systems, pages
     337–340, Berlin, Heidelberg, 2008. Springer Berlin Heidelberg.
[13] Jean-Christophe Filliâtre. Deductive software verification. International Journal on Software Tools
     for Technology Transfer (STTT), 13(5):397–403, August 2011.
[14] Jean-Christophe Filliâtre, Léon Gondelman, Cláudio Lourenço, Andrei Paskevich, Mário Pereira,
     Simão Melo De Sousa, and Aymeric Walch. A Toolchain to Produce Verified OCaml Libraries.
     working paper or preprint, January 2020.
[15] Jean-Christophe Filliâtre, Léon Gondelman, and Andrei Paskevich. A pragmatic type sys-
     tem for deductive verification. Research report, Université Paris Sud, 2016. https://hal.
     archives-ouvertes.fr/hal-01256434v3.
Cameleer: a Deductive Verification Tool for OCaml                                   Pereira and Ravara


[16] Jean-Christophe Filliâtre, Léon Gondelman, and Andrei Paskevich. The spirit of ghost code.
     Formal Methods in System Design, 48(3):152–174, 2016.
[17] Jean-Christophe Filliâtre and Claude Marché. The why/krakatoa/caduceus platform for deductive
     program verification. In Werner Damm and Holger Hermanns, editors, Computer Aided Verifi-
     cation, 19th International Conference, CAV 2007, Berlin, Germany, July 3-7, 2007, Proceedings,
     volume 4590 of Lecture Notes in Computer Science, pages 173–177. Springer, 2007.
[18] Jean-Christophe Filliâtre and Andrei Paskevich. Why3 - where programs meet provers. In Matthias
     Felleisen and Philippa Gardner, editors, Programming Languages and Systems - 22nd European
     Symposium on Programming, ESOP 2013, Held as Part of the European Joint Conferences on
     Theory and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013. Proceedings,
     volume 7792 of Lecture Notes in Computer Science, pages 125–128. Springer, 2013.
[19] Jean-Christophe Filliâtre and Andrei Paskevich. Abstraction and genericity in why3. In Tiziana
     Margaria and Bernhard Steffen, editors, 9th International Symposium On Leveraging Applica-
     tions of Formal Methods, Verification and Validation (ISoLA), volume 12476 of Lecture Notes in
     Computer Science, Rhodes, Greece, October 2020. Springer. http://why3.lri.fr/isola-2020/.
[20] Jean-Christophe Filliâtre, Mário Pereira, and Simão Melo de Sousa. Vérification de programmes
     fortement impératifs avec Why3. In Sylvie Boldo and Nicolas Magaud, editors, Vingt-neuvièmes
     Journées Francophones des Langages Applicatifs, Banyuls-sur-mer, France, January 2018.
[21] Armaël Guéneau, Jacques-Henri Jourdan, Arthur Charguéraud, and François Pottier. Formal
     proof and analysis of an incremental cycle detection algorithm. In John Harrison, John O’Leary,
     and Andrew Tolmach, editors, 10th International Conference on Interactive Theorem Proving,
     ITP 2019, September 9-12, 2019, Portland, OR, USA, volume 141 of LIPIcs, pages 18:1–18:20.
     Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 2019.
[22] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank
     Piessens. Verifast: A powerful, sound, predictable, fast verifier for C and java. In Mihaela Ghe-
     orghiu Bobaru, Klaus Havelund, Gerard J. Holzmann, and Rajeev Joshi, editors, NASA Formal
     Methods - Third International Symposium, NFM 2011, Pasadena, CA, USA, April 18-20, 2011.
     Proceedings, volume 6617 of Lecture Notes in Computer Science, pages 41–55. Springer, 2011.
[23] Jacques-Henri Jourdan, Vincent Laporte, Sandrine Blazy, Xavier Leroy, and David Pichardie.
     A formally-verified C static analyzer. In Sriram K. Rajamani and David Walker, editors, Pro-
     ceedings of the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming
     Languages, POPL 2015, Mumbai, India, January 15-17, 2015, pages 247–259. ACM, 2015.
[24] Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris Yakobowski.
     Frama-c: A software analysis perspective. Formal Aspects Comput., 27(3):573–609, 2015.
[25] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock, Philip Derrin,
     Dhammika Elkaduwe, Kai Engelhardt, Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey
     Tuch, and Simon Winwood. Sel4: Formal verification of an os kernel. In Proceedings of the ACM
     SIGOPS 22nd Symposium on Operating Systems Principles, SOSP ’09, page 207–220, New York,
     NY, USA, 2009. Association for Computing Machinery.
[26] Donald E Knuth. The art of computer programming: Volume 3: Sorting and Searching. Addison-
     Wesley Professional, 1998.
[27] K. Rustan M. Leino. Dafny: An automatic program verifier for functional correctness. In Ed-
     mund M. Clarke and Andrei Voronkov, editors, Logic for Programming, Artificial Intelligence, and
     Reasoning, pages 348–370, Berlin, Heidelberg, 2010. Springer Berlin Heidelberg.
[28] Peter Müller, Malte Schwerhoff, and Alexander J. Summers. Viper: A verification infrastructure
     for permission-based reasoning. In Barbara Jobstmann and K. Rustan M. Leino, editors, Ver-
     ification, Model Checking, and Abstract Interpretation - 17th International Conference, VMCAI
     2016, St. Petersburg, FL, USA, January 17-19, 2016. Proceedings, volume 9583 of Lecture Notes
     in Computer Science, pages 41–62. Springer, 2016.
[29] Chris Okasaki. Purely Functional Data Structures. Cambridge University Press, 1998.
Cameleer: a Deductive Verification Tool for OCaml                                    Pereira and Ravara


[30] Mário José Parreira Pereira. Tools and Techniques for the Verification of Modular Stateful Code.
     Theses, Université Paris Saclay (COmUE), December 2018.
[31] Mário Pereira. Défonctionnaliser pour prouver. In Sylvie Boldo and Julien Signoles, editors, Vingt-
     huitièmes Journées Francophones des Langages Applicatifs, Gourette, France, January 2017.
[32] Yann Régis-Gianas and François Pottier. A hoare logic for call-by-value functional programs. In
     Philippe Audebaud and Christine Paulin-Mohring, editors, Mathematics of Program Construction,
     9th International Conference, MPC 2008, Marseille, France, July 15-18, 2008. Proceedings, volume
     5133 of Lecture Notes in Computer Science, pages 305–335. Springer, 2008.
[33] John C. Reynolds. Separation logic: A logic for shared mutable data structures. In Proceedings
     of the 17th Annual IEEE Symposium on Logic in Computer Science, LICS ’02, page 55–74, USA,
     2002. IEEE Computer Society.
[34] Jan Smans, Bart Jacobs, and Frank Piessens. Implicit dynamic frames: Combining dynamic frames
     and separation logic. In European Conference on Object-Oriented Programming, pages 148–172.
     Springer, 2009.
[35] Yong Kiam Tan, Magnus O. Myreen, Ramana Kumar, Anthony C. J. Fox, Scott Owens, and
     Michael Norrish. The verified cakeml compiler backend. J. Funct. Program., 29:e2, 2019.
[36] The Why3 Development Team. The Why3 platform, version 1.3.3. LRI, CNRS & Univ. Paris-Sud
     & INRIA Saclay, version 1.3.3 edition, September 2020. http://why3.lri.fr/manual.pdf.
Cameleer: a Deductive Verification Tool for OCaml                                                       Pereira and Ravara


A      Translation of expressions


                            (EAbsurd)
                                             assert false expression absurd

                 ghost(A) = β          A function spec S        e expression e0            e expression e0
       (EFun)                                                                                                     (EApp)
                                          expression
                         fun A x → e                   fun (βx) S = e   0
                                                                                         f ē expression f e0

    (ERec)
                ¬is_ghost(A0 )         kind(A0 ) = K     A1 function spec         S1     e0 f unction   xβ, e00
                              f unction                function spec                  expression 0
                         e1               βy, e01   A2               S2            e2            e2
    let A0 rec f0 = e0 A1 and f1 = e1 A2 in e2 expression rec K f (βx) S1 = e00 with K f1 (βy) = e01 S2 in e02

 (ERecGhost)
                 is_ghost(A0 )         kind(A0 ) = K     A1 function spec        S1     e0 f unction    xβ, e00
                              f unction                function spec                  expression 0
                         e1               βy, e01   A2               S2            e2            e2
 let A0 rec f0 = e0 A1 and f1 = e1 A2 in e2 expression rec K f (βx) S1 = ghost e00 with K f1 (βy) = e01 S2 in e02

                                ¬is_ghost(A)        kind(A) = K             ¬is_functional(e0 )
                                          e0 expression e00       e1 expression e01
                    (ELet)
                                 let A x = e0 A0 in e1 expression let K x = e00 in e01

                                is_ghost(A)         kind(A) = K         ¬is_functional(e0 )
                                          e0 expression e00       e1 expression e01
           (ELetGhost)
                              let A x = e0 A0 in e1 expression let K x = ghost e00 in e01

                                 is_ghost(A)        kind(A) = K             is_functional(e0 )
                          A0 function spec S           e0 f unction βx, e00       e1 expression e01
(ELetGhostFun)
                    let A f = e0 A0 in e1 expression let K f = fun(βx) S → ghost e00 in e01

                                 ¬is_ghost(A)          kind(A) = K          is_functional(e0 )
                          A0 function spec S           e0 f unction xβ, e00       e1 expression e01
         (ELetFun)
                        let A f = e0 A0 in e1 expression let K f = fun(βx) S → e00 in e01

                          A loop annotation I            e0 expression e00        e1 expression e01
             (EWhile)
                                while e0 do A e1 done expression while e00 do I e01 done

                              e0 expression e00        e1 expression e01        e2 expression e02
                    (EIf)
                                if e0 then e1 else e2 expression if e00 then e01 else e02

                                          e0 expression e00       e1 expression e01
             (EMatch)
                                                        expression
                          match e0 with 8 p ⇒ e1                     match e00 with 8 p ⇒ e01 end
                                                                                                                  0
                   ē expression ē0                      e expression e0         E x̄ ⇒ e expression E x̄ ⇒ e
(ERaise)                                                                                                          0
                                                                                                                      (ETry)
           raise Eē expression raise Eē0             try e with E x̄ ⇒ e expression try e0 with E x̄ ⇒ e end



                     Figure 3: Translation of OCaml expressions into WhyML.
Cameleer: a Deductive Verification Tool for OCaml                                                          Pereira and Ravara


B      Translation of top-level declarations and type definitions


                                                   m module d
                (DModule)
                                 module M = m declaration scope M d end

                             is_ghost(A)        kind(A0 ) = K          is_functional(e)
                                        function spec              f unction
                                    A                   S      e               βx, e0
     (DLetGhost)
                      let A f = e A0 declaration         let f K = fun(βx) S → ghost e0

                          ¬is_ghost(A)           kind(A0 ) = K          is_functional(e)
                                    A function spec S          e f unction βx, e0
               (DLet)
                         let A f = e A0 declaration let f K = fun(βx) S → e0

    (DRec)
            ¬is_ghost(A0 )       kind(A0 ) = K    A1 function spec S1      e0 f unction xβ, e00
                                    f unction   0          function spec
                            e1          y : π, e1     A2                 S2
    let A0 rec f0 = e0 A1 and f1 = e1 A2 declaration rec K f (βx) S1 = e00 with K f1 (y : π) = e01 S2

 (DRecGhost)
             is_ghost(A0 )      kind(A0 ) = K           A1 function spec S1              e0 f unction xβ, e00
                                    f unction                       function spec
                               e1             y : π, e01       A2                       S2
 let A0 rec f0 = e0 A1 and f1 = e1 A2       declaration     rec K f (βx) S1 = ghost e00 with K f1 (y : π) = e01 S2

                              td0 type definition td00         td1 type definition td01
                 (DType)
                               type td0 and td1    declaration      type td00 with td01

                    (DExn)
                                exception E : π declaration exception E : π



               Figure 4: Translation of OCaml top-level declarations into WhyML.




  (TDAbstract)                                                                                       (TDAlias)
                     α T type definition T α                α T = τ type definition T α = τ

                                                A type invariant t̄
      (TDRecord)
                      α T = { f : π } A declaration T α = { f : π } invariant t̄

             (TDVariant)
                                α T = 8 C of τ type definition T α = 8 C τ



                  Figure 5: Translation of OCaml type definitions into WhyML.
Cameleer: a Deductive Verification Tool for OCaml                                Pereira and Ravara


C      Translation of module expressions and module types

                                           d declaration d0
                         (MStruct)
                                       struct d end module d0

                                  mt module type d       m module d0
           (MFunctor)
                          functor(X : mt) → m        module   scope X d end d0

                                            s signature d
                            (MTSig)
                                       sig s end module type d


      Figure 6: Translation of OCaml module expressions and module types into WhyML.
Cameleer: a Deductive Verification Tool for OCaml                                 Pereira and Ravara


D      Translation of signatures

                                  ¬is_ghost(A)     kind(A) = K
                        A0 function spec S   π, A0 function args x : π 0 , πres
               (SVal)
                           val A f : π A0 signature val K f (x : π) S : πres

                                  ¬is_ghost(A)     kind(A) = K
                        A0 function spec S   π, A0 function args x : π 0 , πres
       (SValGhost)
                        val A f : π A0 signature val K ghostf (x : π) S : πres

                           td0 type definition td00   td1 type definition td01
                (SType)
                            type td0 and td1 signature type td00 with td01


                     Figure 7: Translation of OCaml signatures into WhyML.
Cameleer: a Deductive Verification Tool for OCaml                                  Pereira and Ravara


E     Summary of Cameleer case studies

               Case Study                       Lines of Code   Lines of Specification
               Applicative Queue                           25                       21
               Binary Multiplication                       10                        6
               Binary Search                               15                       10
               Checking a Large Routine                    25                       15
               CNF Convertion                             113                       47
               Ephemeral Queue                             39                       32
               Factorial                                   10                       13
               Fast Exponentiation                         19                       47
               Fibonacci                                   46                       58
               Insertion Sort                              13                       80
               Integer Square Root                          8                       14
               Leftist Heap                                68                      108
               Mjrty                                       45                       32
               Same Fringe                                 23                       16
               total                                      459                      499

                       Table 1: Case studies verified with the Cameleer tool.
