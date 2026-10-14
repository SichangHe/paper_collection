                                         Under consideration for publication in Theory and Practice of Logic Programming               1




                                            Combining Type Checking and Set Constraint
                                         Solving to Improve Automated Software Verification
arXiv:2205.01713v3 [cs.LO] 21 Mar 2024




                                                                          MAXIMILIANO CRISTIÁ
                                                                   Universidad Nacional de Rosario and CIFASIS
                                                                                     Argentina
                                                                       E-mail: cristia@cifasis-conicet.gov.ar

                                                                            GIANFRANCO ROSSI
                                                                               Università di Parma
                                                                                        Italy
                                                                          E-mail: gianfranco.rossi@unipr.it

                                                     submitted 1 January 2003; revised 1 January 2003; accepted 1 January 2003



                                                                                    Abstract
                                         This technical note shows how we have combined prescriptive type checking and constraint
                                         solving to increase automation during software verification. We do so by defining a type system
                                         and implementing a typechecker for {log} (read ‘setlog’), a Constraint Logic Programming
                                         (CLP) language and satisfiability solver based on set theory. The constraint solver is proved to
                                         be safe w.r.t. the type system. Two industrial-strength case studies are presented where this
                                         combination is used with very good results.
                                            Under consideration in Theory and Practice of Logic Programming (TPLP).
                                         KEYWORDS: {log}, set theory, constraint logic programming, type system, typechecker




                                                                                1 Introduction
                                         CLP systems can be used for formal software verification. In general, these systems
                                         provide untyped languages. Adding prescriptive type systems to CLP languages may help
                                         when CLP is used for formal verification because typecheckers are sound and complete.
                                            Prescriptive type checking catch errors at compile time, whereas constraint solving
                                         can catch errors at runtime. Catching errors at runtime might not be acceptable in
                                         certain contexts—e.g., safety-critical systems. In this note we show how prescritive type
                                         checking and set constraint solving can be combined in CLP to automatically found errors
                                         before the program is executed. We do so by defining a type system and implementing a
                                         typechecker for {log} (‘setlog’) (Dovier et al. 2000; Rossi 2008).
                                            {log} is a satisfiability solver implementing decision procedures for several expressive
                                         fragments of the theory of finite sets and finite set relation algebra. Several in-depth
                                         empirical evaluations provide evidence that {log} is able to solve non-trivial problems
                                         (Cristiá and Rossi 2018; 2020; 2021b; 2024; Cristiá et al. 2013); in particular as an
                                         automated verifier of security properties (Cristiá and Rossi 2021a; 2021c) (Cristiá et al.
                                         2023). That is, {log} is able to automatically prove that a program or a model verifies
                                         some complex properties such as the invariance lemmas arising from the verification
2                                M. Cristiá and G. Rossi

of non-trivial state machines. Rooted in CLP and Prolog, {log} essentially provides an
untyped language. The lack of types makes it impossible for {log} to find certain classes
of errors.
   In this note, we show how {log} has been enriched with a (prescriptive) type system.
{log}’s type system is an instance of a Hindley-Milner system including parametric poly-
morphism for function and predicate symbols. Given that in {log} finite sets and set
operators are first-class entities of the language, the type system is defined as to provide
support for them. That is, there are types for sets, binary relations and their elements,
and set and relational operators are typed accordingly. The type system is based on the
type system defined for the Z formal notation (Spivey 1992), which in turn is similar to
B’s (Abrial 1996). Actually, {log} has been proposed as a prototyping language for B and
Z specifications (Cristiá et al. 2013; Cristiá and Rossi 2021c; Cristiá and Rossi 2024).
   Through the combination between type checking and CLP features {log} performs
three important tasks: it type checks a program, it runs the program, and it automati-
cally proves properties of the same program. As far as we understand this is a novel ap-
proach concerning tools for set-based languages. There are tools where types are used to
guarantee some properties (e.g., Atelier-B (Mentré et al. 2012), Rodin (Abrial et al. 2010)
and Zenon Modulo (Bonichon et al. 2007)) but they do not enjoy CLP properties—for
instance, they cannot execute their models. Other tools clearly fit in the CLP paradigm
(e.g., ProB (Leuschel and Butler 2003)), but they cannot prove properties true of the
specification. None of these tools implement decision procedures for set theory as those
implemented in {log}. At the same time, {log} provides a language almost at the same
level of abstraction of formal notations such as B and Z. These features make {log} to
solve real-world problems as shown in Section 5.3.
   As a design choice, we allow the typechecker in {log} to be switched on and off by users;
when switched off, {log} works as usual. This choice is not only a matter of backward
compatibility but the result of understanding that typed and untyped formalisms have
their own advantages and disadvantages (Lamport and Paulson 1999). Hence, being {log}
at the intersection of a specification language, a programming language and an automated
verifier, we think that users can decide when they need types.
   The contents of this note are rather informal and conceptual. All the technical details
can be found in an on-line document (Cristiá and Rossi 2022).


               2 Combining type checking and constraint solving
As we have said, {log} provides an untyped language. For example, if variable X represents
the current value of a traffic light it should always be the case that X in {red,yellow,green}
holds (where in is interpreted as ∈). However, in a {log} program it is possible for X to be
bound to any value, say 2. Then, 2 in {red,yellow,green} will fail making {log} to an-
swer false at runtime—which is potentially dangerous in a safety-critical system. {log}
will also answer false if X is bound to green when X in {red,yellow} holds. Hence, we
have two false answers arising from quite different causes: the first one (X = 2) is clearly
a programming error; the second one (X = green) is just a possible, although unsatisfi-
able, situation. We would like to help the programmer to easily tell these false answers
apart. A (prescriptive) typechecker can signal the user with a type error if there is the
chance of X being bound to something outside of {red,yellow,green}; the constraint
                     Combining Type Checking and Set Constraint Solving                    3

solver can determine whether or not X in {red,yellow} is satisfiable by discharging
a certain proof obligation. Both checks are performed before the program is run, thus
avoiding runtime errors.


        2.1 Typechecking and formally verifying a simple library system
Consider the following {log} clause concerning a simple library system:

addBook(Books,B,T,Books_) :-
  dom(Books,D) & B nin D & Books_ = {[B,T] / Books}.

where Books is a set of ordered pairs mapping books IDs (BID) onto their titles and
Books_ is the state of the library after adding [B,T] to it. In turn, B and T are the book
ID and title of a new book being added to the library. Besides, dom/2 is a {log} constraint
computing the domain of a function; nin is interpreted as ∈; / and {[B,T] / Books} is a
{log} set term interpreted as {(B , T )} ∪ Books, where (B , T ) is an ordered pair. Finally,
& stands for conjunction.
   Without types, T can be bound to any term (e.g., an ordered pair or a list) which is
clearly not the intention. After adding types to {log} we can declare the type of addBook
as follows:

dec_p_type(addBook(rel(bid,title),bid,title,rel(bid,title)).
addBook(Books,B,T,Books_) :-
  dom(Books,D) & B nin D & Books_ = {[B,T] / Books}.

That is, the clause is preceded by a dec_p_type fact asserting the type of each argument1 .
As can be seen, dec_p_type takes one argument corresponding to the head predicate of
the clause being declared. In turn, each argument of the predicate inside dec_p_type is
a type. In this way, rel(bid,title) is the type of Books, bid is the type of B, etc.
   rel(bid,title) corresponds to the type of the binary relations from bid to title,
which in turn are basic types. Values of basic type x are of the form x?atom where atom
is any Prolog atom.
   When the file containing addBook/4 is consulted, the typechecker checks the type of
addBook/4. Later, users can issue queries involving the clauses declared in the file. In this
case, users have to give the types of all the variables involved in the query. For example:

dec(NewBooks,rel(bid,title)) & addBook({},bid?b1,title?aleph,NewBooks)

where dec(NewBooks,rel(bid,title)) declares NewBooks’s type and {} denotes the
empty set. Before executing the query, {log} calls the typechecker to check whether
the query is type correct or not. In this case, the typechecker uses the dec_p_type of
addBook/4, the dec predicates and the arguments in the query to control that each
argument in the query has the right type.
  Types ensure that programs “are free from certain kinds of misbehavior” (Pierce 2002).
However, types cannot catch all kinds of errors. Concerning the library system, observe
that Books is supposed to be a function but its type declaration states that it is a binary

1 dec   p type stands for ‘declare predicate type’.
4                                M. Cristiá and G. Rossi

relation. Then, this type declaration cannot catch the error of putting in Books two
ordered pairs sharing the same BID but different titles.
   One may think in a type system where functions are first-class entities. However, in
set-based formal notations such as B and Z binary relations are first-class entities whereas
functions are defined as a subclass of binary relations. Hence, in this context this problem
is approached by asking the user to discharge proof obligations ensuring that, for instance,
a binary relation is actually a function. {log} follows the same approach. Actually, {log}
uses its automated proving power to discharge those proof obligations. Hence, {log}
combines type checking and constraint solving to ensure program correctness.
   In this way, if we want Books to be a function we can use the pfun constraint in com-
bination with a type declaration: dec(Books,rel(bid,title)) & pfun(Books). pfun
is a {log} constraint asserting that its argument is a partial function.
   This approach is particularly amenable to work with invariance lemmas. An invariance
lemma states that some property, the invariant, is preserved along all program executions.
Indeed, one can propose a typing property that cannot be enforced by the type system as
a program invariant. Afterwards, one proves that the program preserves that invariant by
discharging the corresponding invariance lemma. The obvious problem with this approach
is the fact that discharging an invariance lemma requires, in general, a manual proof.
However, if the invariance lemma corresponds to a formula belonging to some decidable
theory, it can, in principle, be automatically discharged. Here is where {log} constraint
solving capabilities come into play.
Example 1
The type system ensures that, for instance, [B,12] cannot be added to Books, but it
cannot ensure that Books is a function. On the other hand, {log} (without types) can
automatically prove that pfun(Books) is a type invariant for that operation but it cannot
check that [B,12] cannot be an element of Books before the program is executed. In
order to prove that pfun(Books) is a type invariant the following is (automatically)
proved to be unsatisfiable:
dec([Books,Books_],rel(bid,title)) & dec(B,bid) & dec(T,title) &
pfun(Books) & addBook(Books,B,T,Books_) & npfun(Books_)
where npfun is interpreted as ¬ pfun. We know this can be automatically proved because
the formula belongs to a decidable fragment implemented in {log} (see Section 4.1). 2
   Furthermore, types simplify some proof obligations thus further reducing the verifica-
tion effort. The following is an example.
Example 2
Consider that in the library system Books ∈ bid →  7 title should be an invariant of
the system. This invariant can be mathematically rewritten as: dom Books ⊆ bid ∧
ran Books ⊆ title ∧ pfun(Books). With the type declaration dec(Books,rel(bid,title))
the first two conjuncts are proved by the typechecker. Then, pfun(Books) is the only
property the constraint solver has to prove.                                      2
  As set constraint solving is always less efficient than type checking, the combination be-
tween type checking and constraint solving makes a better use of the computing resources
because type checking finds errors before constraint solving is called.
  Once {log} has been used to verify the program, it can also be used to run simulations.
                   Combining Type Checking and Set Constraint Solving                                 5

Example 3
The predicate addBook can be called as a normal subroutine.

{log}=> addBook({},bid?b1,title?the_farm,Books_).
Books_ = {[bid?b1,title?the_farm]}
{log}=> addBook({},bid?b1,title?the_farm,Books1)
        & addBook(Books1,bid?b2,title?houses,Books_).
Books_ = {[bid?b1,title?the_farm],[bid?b2,title?houses]}
{log}=> addBook({},bid?b1,title?the_farm,Books1)
        & addBook(Books1,bid?b1,title?houses,Books_).    % same ID
false

We can also define other operations on the library:

dec_p_type(title(rel(bid,title),bid,title)).
title(Books,B,T) :- applyTo(Books,B,T).

where applyTo(F,X,Y) is true when F (X ) = Y . Then we can run the program calling
all the operations:

{log}=> addBook({},bid?b1,title?the_farm,Books1)
        & addBook(Books1,bid?b2,title?houses,Books_)
        & title(Books_,bid?b1,T).
T = title?the_farm

                                                                                                      2


                                  3 A type system for {log}
In this section we describe the type system defined for {log}. After the introduction of
types, every variable, term and predicate is of or has a type2 . The type system includes
types for a subclass of Prolog atoms, integer numbers, sum types3 , ordered pairs and
sets, which can be recursively combined. This recursion enables the definition of types
corresponding to sets of ordered pairs which allow the correct typing of binary relations.
Terms of any type can be used to build set terms as long as they are all of the same
type, no nesting restrictions being enforced (in particular, membership chains of any
finite length can be modeled). In this and the following section we use a more abstract,
math-oriented notation, instead of the {log} code shown in the previous section and in
Section 5. A fully detailed presentation can be found in the on-line document (Cristiá
and Rossi 2022).
   The type system is given by the following grammar:
                                                  ≥2
                                            z }| {
                       τ ::= int | b | sum([C , . . . , C ]) | prod(τ, τ ) | set(τ )
                       C ::= a | a(τ )


2 The type of a predicate is given by the type of each of its arguments. See examples in Section 2.
3 Tagged union, variant, variant record, choice type, discriminated union, disjoint union, or coproduct.
6                                        M. Cristiá and G. Rossi

                                                                Γ⊢x :τ    Γ ⊢ A : set(τ )
                                                         Ext
                     Γ ⊢ {} : set(τ )                             Γ ⊢ {x /A} : set(τ )
                 Γ ⊢ m : int  Γ ⊢ n : int                                n∈Z
          Int
                 Γ ⊢ int([m, n) : set(int)                             Γ ⊢ n : int

                 Γ ⊢ m : int Γ ⊢ n : int                           Γ ⊢ x : τ1      Γ ⊢ y : τ2
          Ar                                              Prod
                     Γ ⊢ m ⊞ n : int                               Γ ⊢ [x , y] : prod(τ1 , τ2 )

                    b∈B    a ∈ A0                     v ∈ Var       τ ∈ Types{·}        v∈
                                                                                         / dom Γ
                     Γ ⊢ b?a : b                                {dec(v , τ )} ∪ Γ ⊢ v : τ

                {a1 , a2 } ⊂ A     τ = . . . sum([a1 , a2 (τ2 )]) . . . {a1 , a2 } ∥ (τ ∪ Γ)      x : τ2
        Sum
                                 {dec(v , τ )} ∪ Γ ⊢ a1 , a2 (x ) : sum([a1 , a2 (τ2 )])

Fig. 1. Type rules for function symbols



where b ∈ B and a ∈ A whereas A represent the set of Prolog atoms and B is a countable
set of type names.
   Intuitively, int corresponds to the type of integer numbers; sum([C1 , . . . , Cn ]) with
2 ≤ n defines a sum type given by all the values that can be built by each constructor
Ci ; prod(T1 , T2 ) defines the product type given by the Cartesian product T1 × T2 ; and
set(T ) defines the powerset type of type T . Each constant b ∈ B represents the type
name of a basic type interpreted as the set {b?a | a ∈ A}. An example of a sum type is
sum([nil, some(int)]) representing the set {nil} ∪ {some(i ) | i ∈ Z}. We write rel(τ1 , τ2 )
as a shortcut for set(prod(τ1 , τ2 )). Clearly, rel represents the type of binary relations. This
type system is aligned with those of Z (Spivey 1992) and B (Abrial 1996).
   The type of the main {log} function symbols is defined in Figure 1, where: dec(v , t)
is a predicate interpreted as “variable v is of type t”; a typing context Γ is a set of dec
predicates; Γ ⊢ s : τ can be read as ‘in typing context Γ, s is of or has type τ ’; v ∈    / dom Γ
means that v is not one of the variables declared in Γ; τ = . . . sum([a1 , a2 (τ2 )]) . . . asserts
that sum([a1 , a2 (τ2 )]) is part of the definition of τ ; and {a1 , a2 } ∥ (τ ∪ Γ) asserts that
{a1 , a2 } is disjoint w.r.t. the union of the constructors of any other sum used in τ and Γ
(except itself). Symbols {}, [·, ·] and {·/·} were introduced in Section 2; int(m, n) stands
for the set {z ∈ Z | m ≤ z ≤ n}; and ⊞ stands for any integer binary operator.
   Rule Sum is given for a simple case to keep the presentation manageable; it can be
easily extended to any number of constructors. Note that a sum constructor can be used
in only one sum type, and that there must be at least two constructors in a sum type.
   As can be seen, several function symbols are polymorphic. In particular, the type of
a term of the form u?a is given by its first argument. As terms must have exactly one
type, any a ∈ A can be used as the constructor of at most one sum in Γ. The type of
a variable is the type given in its declaration through the dec predicate in Γ. With this
type system a set such as {a, 1, {2}, (5, 4)} is ruled out because not all of its elements are
of the same type. However, that set can be encoded as {a, n(1), s({2}), p((5, 4))}, where
a, n, s and p are constructors of a sum type. If in a sum all constructors are nullary
terms then we write enum([a1 , . . . , an ]) to emphasize the fact that the sum is actually
defining an enumeration.
                   Combining Type Checking and Set Constraint Solving                             7

Example 4
The following are some examples on how terms are typed.
 {dec(k , int)} ∪ Γ ⊢ k + 1 : int
 {dec(A, set(int))} ∪ Γ ⊢ {4, 9/A} : set(int)
 {dec(m, int), dec(x , sum([a, e(int)])} ⊢ ({m}, e(m + 1)) : prod(set(int), sum([a, e(int)]))
 Γ ⊢ {u?a, u?aa, u?ab} : set(u)
 {u?a, v?a} : cannot be typed because u?a has type u and v?a has type v
 u?10 : cannot be typed because 10 ∈
                                   /A
 {dec(x , sum([a, b, a(t)]))} ∪ Γ ⊢ . . .
       is an ill-formed typing context because a appears twice
 {dec(x , prod(enum([a, b]), sum([q, a(t)]))} ∪ Γ ⊢ . . .
       is an ill-formed typing context because a appears in two different sum
 {dec(x , enum([a,b])), dec(y, enum([q, a]))} ∪ Γ ⊢ . . .
       is an ill-formed typing context because a appears in two different enum
In the last three examples the problem is that the terms a, b and q cannot be typed
because no type rule can be applied to infer their types.                         2
   The type of each primitive constraint available in {log} is given in Figure 2. If τ1 , . . . , τn
are types, a type judgment such as Γ ⊢ π(τ1 , . . . , τn ) can be read as ‘predicate π is
correctly typed’. Constraints are interpreted as follows: x neq y as x ̸= y; x in A as x ∈ A;
x nin A as x ∈ / A; un(A, B , C ) is interpreted as C = A ∪ B ; disj (A, B ) as A ∩ B = ∅;
size(A, m) as |A| = m; id (A, R) as R = {(x , x ) | x ∈ A}, i.e., the identity relation on
set A; inv (R, S ) as S = {(y, x ) | (x , y) ∈ R}, i.e., the converse of a binary relation; and
comp(R, S , T ) as T = {(x , z ) | ∃ y((x , y) ∈ R ∧ (y, z ) ∈ S )}, i.e., composition of binary
relations. Again, several constraints are polymorphic. Besides, it is worth to be noticed
that in untyped formalisms a constraint such as 1 ̸= (2, 4) would usually be deemed as a
true proposition while in {log} such a constraint is ill-typed and thus rejected.
   In {log}, formulas are built in the usual way by connecting constraints (i.e., predefined
predicates) by means of conjunction (∧), disjunction (∨) and negation (¬ ). Formulas can
also contain user-defined predicates (addBook/4 in Section 2 is an example). A well-typed
formula is a formula where all its constraints are typed according to the rules given in
Figure 2 and user-defined predicates are typed by means of dec_p_type declarations.
Example 5
The following are well-typed {log} formulas:
        id ({x /A}, R) ∧ id (R, A) ∧ dec(x , t) ∧ dec(A, set(t)) ∧ dec(R, rel(t, t))             (1)
        dec([A, B , C ], set(int)) ∧ dec([n, k ], int) ∧                                         (2)
             un(A, B , C ) ∧ n + k > 5 ∧ size(C , n) ∧ B ̸= {}
        dec(y, t) ∧ dec(R, rel(t, int)) ∧ dec([S , T ], rel(int, t)) ∧ dec(x , prod(int, t)) ∧   (3)
             [y, 5] ∈ R ∧ [2, t?b] ∈
                                   / S ∧ inv (R, S ) ∧ S = {x /T }
On the contrary, dec(x , t) ∧ dec(y, int) ∧ x neq y is not well-typed because x neq y cannot
be typed as neq expects arguments of the same type (rule Eq in Figure 2).                 2
8                                      M. Cristiá and G. Rossi

               Γ⊢x :τ      Γ⊢y :τ                                        Γ⊢x :τ     Γ ⊢ A : set(τ )
        Eq                                                     Mem
                Γ ⊢ x = y, x neq y                                         Γ ⊢ x in A, x nin A

                            Γ ⊢ A : set(τ )       Γ ⊢ B : set(τ )  Γ ⊢ C : set(τ )
                      Un
                                                 Γ ⊢ un(A, B , C )
             Γ ⊢ A : set(τ )   Γ ⊢ B : set(τ )                     Γ ⊢ A : set(τ ) Γ ⊢ m : int
                                                              Sz
                     Γ ⊢ disj (A, B )                                    Γ ⊢ size(A, m)

             Γ ⊢ A : set(τ )   Γ ⊢ R : rel(τ, τ )           Γ ⊢ R : rel(τ1 , τ2 ) Γ ⊢ S : rel(τ2 , τ1 )
       Id
                       Γ ⊢ id (A, R)                                     Γ ⊢ inv (R, S )

                      Γ ⊢ R : rel(τ1 , τ2 )      Γ ⊢ S : rel(τ2 , τ3 )    Γ ⊢ T : rel(τ1 , τ3 )
                 Rc
                                                Γ ⊢ comp(R, S , T )

                                    Leq
                                              Γ ⊢ m : int Γ ⊢ n : int
                                                    Γ⊢m≤n

Fig. 2. Type rules for predicate symbols in ΠC


Expressiveness. As we have said, Figure 2 presents the type of each {log} primitive
constraint. These constraints are used to define a number of integer, set and relational
constraints by means of suitable formulas. Dovier et al. (2000) proved that un, ∈ and
disj are enough to define constraints implementing the set operators ∩, ⊆ and \. For
example, A ⊆ B can be defined by the formula un(A, B , B ). In turn, these constraints
plus id , inv and comp are as expressive as the class of finite set relation algebras (Cristiá
and Rossi 2020). Within this class of algebras it is possible to define many relational
operators such as domain, range, domain restriction, relational image, etc. Finally, by
adding the size constraint and integer intervals, it is possible to define operators such as
the minimum of a set, the successor function on a set, partition of a set w.r.t. a given
number, etc. (Cristiá and Rossi 2024).
  The negated versions of set, relational and integer operators can be introduced in
the same way (Dovier et al. 2000) (Cristiá and Rossi 2020; 2023; 2024). For example,
¬ (A ∪ B = C ) is introduced as:

                b in C ∧ n nin A ∧ n nin B ) ∨ (n in A ∧ n nin C ) ∨ (n in B ∧ n nin C ) (4)
 nun(A, B , C ) =(n

  The combination between sum and product types permit to encode arbitrary com-
pound terms. For instance, a term of the form p(2, {4}) can be encoded as p([2, {4}])
whose type is sum([p(prod(int, set(int))), . . . ]).



                                               4 Type safety

The definition of a type system for a CLP language entails to prove that the operational
semantics of the language preserves the types of variables and terms as it processes any
well-typed formula. This is called type soundness or type safety (Harper 2016, Chapter
4). The operational semantics of a CLP language is given primarily by its constraint
solving procedure.
                   Combining Type Checking and Set Constraint Solving                              9

                             4.1 The {log} constraint solver
The constraint solver for {log} with types is the same solver for {log} without types4 .
In {log} with types, the solver is simply run once the type checking phase has finished
successfully and ignores dec predicates. The solver for {log} without types has been
thoroughly studied elsewhere (Dovier et al. 2000 and Cristiá and Rossi 2020; 2023; 2024).
Several results on the decidability of the satisfiability problem for these languages have
been put forward and several empirical studies showing the practical capabilities of {log}
have also been reported (Cristiá and Rossi 2021a; 2021c; Cristiá et al. 2013). For this
reason here we give only an overview of the {log} solver.
   The {log} solver is essentially a rewriting system whose core is a collection of specialized
rewriting procedures. Each rewriting procedure applies a few non-deterministic rewrite
rules which reduce the syntactic complexity of {log} constraints of one kind. {log} takes
as input a formula, Φ. In each iteration, {log} rewrites Φ into a new formula, called Φ′ ,
which becomes the input formula for the next iteration.
   As is shown in the aforementioned papers, there are three possible outcomes when
{log} is applied to Φ:
   1. {log} returns false meaning that Φ is unsatisfiable.
   2. {log} cannot rewrite Φ′ anymore and it is not false, so Φ′ is returned as it is.
      Since {log} can open a number of non-deterministic choices, many such Φ′ can
      be returned to the user. The disjunction of all these Φ′ is equivalent to Φ. The
      constraints making these formulas are of a particular kind called irreducible (Dovier
      et al. 2000 and Cristiá and Rossi 2020; 2023; 2024).
   3. If Φ belongs to an undecidable fragment of the language supported by {log}, then
      the above steps will not terminate.
   As we have said, the core of {log} is a collection of rewriting procedures which in turn
contain a collection of rewrite rules. There are about 60 of such rules which can be found
online (Cristiá and Rossi 2019). Figure 3 lists some representative rewrite rules for the
reader to have an idea of what they look like. As can be seen, each rule has the form:
ϕ −→ Φ1 ∨ · · · ∨ Φn , where ϕ is a {log} constraint and Φi , i ≥ 1, are {log} formulas.
Besides, each rule is applied depending on some syntactic conditions on the constraint
arguments. For example, rule (6) applies only when the first argument is an extensional
set and the third is a variable (noted as Ḃ ); the second argument can be any set term.
On the right-hand side of the rules, n, ni , N , Ni represent new variables.
   Rule (5) is the main rule of set unification (Dovier et al. 2006), a concept at the base of
{log}. It states when two non-empty, non-variable sets are equal by non-deterministically
and recursively computing four cases. As an example, by applying rule (5) to {1} = {1, 1}
we get: (1 = 1 ∧ {} = {1}) ∨ (1 = 1 ∧ {1} = {1}) ∨ (1 = 1 ∧ {} = {1, 1}) ∨ ({} =
{1/N } ∧ {1/N } = {1}), which turns out to be true (due to the second disjunct).
   Rule (6) is one of the main rules for un constraints. Observe that this rule is based on
set unification, as well. It computes two cases: x does not belong to A and x belongs to
A (in which case A is of the form {x /N2 } for some set N2 ). In the latter case x nin N2
prevents {log} from generating infinite terms denoting the same set.

4 From now on, we will talk of {log} as both the constraint language and its solver whenever is clear
  from context.
10                                    M. Cristiá and G. Rossi


      {x /A} = {y/B } −→
           x =y ∧A=B
            ∨ x = y ∧ {x /A} = B                                                                   (5)
            ∨ x = y ∧ A = {y/B }
            ∨ A = {y/N } ∧ {x /N } = B

      un({x /C }, A, Ḃ ) −→
           {x /C } = {x /N1 } ∧ x nin N1 ∧ B = {x /N }                                             (6)
            ∧ (x nin A ∧ un(N1 , A, N )
                 ∨ A = {x /N2 } ∧ x nin N2 ∧ un(N1 , N2 , N ))

      size({x ⊔ A}, m) −→
           x nin A ∧ m = 1 + n ∧ size(A, n) ∧ 0 ≤ n                                                (7)
            ∨ A = {x /N } ∧ x nin N ∧ size(N , m)

Fig. 3. Some rewrite rules implemented by SAT {·}


  Rule (7) computes the size of any extensional set by counting the elements that belong
to it while taking care of avoiding duplicates. This means that, for instance, the first
non-deterministic choice for a formula such as size({1, 2, 3, 1, 4}, m) will be:
        1 nin {2, 3, 1, 4} ∧ m = 1 + n ∧ size({2, 3, 1, 4}, n) ∧ 0 ≤ n
which will eventually lead to a failure due to the presence of 1 nin {2, 3, 1, 4}.


                                     4.2 Proving type safety
The theorem stating type safety for {log} follows the guidelines set forth by Harper
(2016, Chapter 6). However, due to the peculiarities of CLP we have to introduce some
modifications to the theorem. Indeed, most of the foundational work on type systems has
been done in a framework where programs are functions (Milner 1978; Martin-Löf 1984;
Wright and Felleisen 1994; Pierce 2002; Barendregt et al. 2013), so it is natural to adapt
some of its concepts and results to CLP.
  Intuitively, Harper’s theorem states that: the type of any given term remains the same
during the execution of the program; and if a term is well-typed, either it is a value
or it can be further rewritten by the system. The first property is called preservation
(or subject reduction) and the second is called progress. This theorem is adapted to our
context as follows.
Theorem 1 ({log} is type safe)
Consider any {log} constraint π. Let t1 : τ1 , . . . , tk : τk be such that π(t1 , . . . , tk ) is a
well-typed constraint. Then (−→ denotes any {log} rewrite rule):
     (I) If π(t1 , . . . , tk ) −→ Φ, then there exist types τ1′ , . . . , τm
                                                                            ′
                                                                              (0 ≤ m) such that:
                dec(n1 , τ1′ ) ∧ · · · ∧ dec(nm , τm
                                                   ′
                                                     )∧Φ
         is a well-typed formula, were n1 , . . . , nm are the new variables of Φ.
                          Combining Type Checking and Set Constraint Solving                                                   11
                    all disjunctions ok
   well-typed                                      all constraints ok                    all arguments ok

                                 phase 2
    phase 1         ok                                                       phase 3     constraint          phase 4
                              analyze logical        conjunction of
   check dec                                                                constraint                  term typechecking
                           structure of formula       constraints
   constraints                                                            typechecking                (constraint arguments)
                             [write into DNF]

           not ok                             types of arguments don't unify                 one argument of wrong type
                            type error



Fig. 4. Graphical depiction of the four phases implemented by the typechecker

 (II) π(t1 , . . . , tk ) is irreducible, or there exists Φ such that π(t1 , . . . , tk ) −→ Φ                                 2
  The proof can be found in the on-line document (Cristiá and Rossi 2022). As Theorem
1 suggests, the proof entails to prove that each of the 60 rewrite rules present in {log}
are type safe.


                                                  5 Implementation
A typechecker for {log} has been implemented in Prolog. The program comprises about
1.1 KLOC of which 200 are devoted to error printing. It uses only basic, standard Prolog
predicates. The typechecker can be downloaded from the {log} web site (Rossi 2008, file
setlog tc.pl). As we have pointed out in Section 2, the typechecker can be activated
and deactivated by users at their will. If the typechecker is not active dec predicates are
ignored and {log} works as usual.
   The typechecker is implemented in four phases (see Figure 4): phase 1, the typechecker
analyzes the dec predicates in the formula; phase 2, the logical structure of the formula
is analyzed; phase 3, once we have a conjunction of atomic constraints the typechecker
goes to check the type of each atomic constraint using rules in Figure 2; and phase 4,
the type of each argument, of a given constraint, is checked using rules in Figure 1.
   Going deeply into implementation details, in phase 1, dec predicates that are found
correct by the typechecker are turned into ‘type’ facts of the form type(Var,type),
asserting that the type of the variable is the one declared by the user.
   Phases 3 and 4 are solved as unification problems. For example, the following clause
typechecks id constraints (i.e., phase 3):
typecheck_constraint(id(X,Y)) :- !,
  typecheck_term(X,Tx),
  typecheck_term(Y,Ty),
  (Tx = set(T), Ty = set(prod(T,T)),!
   ;
   print_type_error(id(X,Y),Tx,Ty)
  ).
As can be seen, if the inferred types of X and Y cannot be unified in terms of a common
type T (as indicated in rule Id of Figure 2), a type error is issued.


                              5.1 Introducing parametric polymorphism
Consider the following clause:
12                                   M. Cristiá and G. Rossi

applyTo(F,X,Y) :- F = {[X,Y] / G} & [X,Y] nin G & comp({[X,X]},G,{}).

It states minimum conditions for applying binary relation F to a given point X whose
image is Y. applyTo is meant to be a polymorphic definition in the sense that F is
expected to be a binary relation of any rel type, X is expected to be of the domain
type of F and Y of the range type. This is usually called parametric polymorphism.
   Clauses that are meant to be polymorphic must be preceded by a dec_pp_type fact
asserting the type of each argument5 . For example, the typed version of applyTo is the
following:

dec_pp_type(applyTo(rel(T,U),T,U)).
applyTo(F,X,Y) :- F = {[X,Y] / G} & [X,Y] nin G & comp({[X,X]},G,{}).

Differently from dec_p_type declarations, the types written in a dec_pp_type declara-
tion can contain variables (e.g., T).
   Users can query polymorphic clauses such as applyTo by giving types unifying with
those declared in the corresponding dec_pp_type declarations.


                                 5.2 Dealing with finite types
When working in typechecking mode, the following goal is unsatisfiable:

dec(Z,enum([t,f])) & Z neq t & Z neq f.

because the only two values Z can take are exactly t and f. In this case, {log} automat-
ically transforms that goal into:

Z in {t,f} & Z neq t & Z neq f.

However, if the typechecker is not active, the first given goal is found to be satisfiable
because the dec predicate is ignored and Z can take any value beyond t and f.
  As another example, consider the following goal:

dec(F,rel(enum([t,f]),int)) & dec([X1,X2,X3],[enum([t,f]),int]) &
pfun(F) & F = {X1,X2,X3} & X1 neq X2 & X1 neq X3 & X2 neq X3.

As F is a partial function and given the neq constraints, the first components of X1,
X2 and X3 must be different from each other. At the same time, these first components
have type enum([t,f]). So at least two of these first components must have the same
value. Consequently the goal is unsatisfiable. As with the first goal, when working in
typechecking mode, {log} identifies this situation and automatically conjoin suitable
membership constraints to make type information available to the constraint solver.
  These situations arise when the formula involves variables whose types are finite and
entails, in a way or another, “too many” neq constraints. In these situations the constraint
solver retrieves the type information generated by the typechecker transforming it into
suitable membership constraints. This interplay between these two components is crucial
to the correctness of {log} when working in typechecking mode.


5 dec   pp type stands for ‘declare polymorphic predicate type’.
                  Combining Type Checking and Set Constraint Solving                        13

                                    5.3 Case studies
The combination between typechecking and constraint solving as presented in this note
has been applied to some case studies. Here we briefly present two of them. Both case
studies are based on problems, specifications and verification conditions proposed by
others, thus reducing a possible bias towards our method. We use these case studies
as benchmarks to empirically evaluate {log}. Each case study shows a {log} program
taking the form of a state machine. Transitions of these state machines are encoded as
{log} predicates—e.g., as addBook. In turn, these predicates constitute an executable
API from which the program can be run—as shown in Example 3. At the same time,
these {log} programs behave as specifications over which the verification conditions are
automatically discharged—as shown in Example 1.

The Landing Gear System. The first case study is based on the Landing Gear System
(LGS) problem (Boniol and Wiels 2014). Mammar and Laleau (2014; 2017) developed
an Event-B (Abrial 2010) specification formally verified using Rodin (Abrial et al. 2010),
ProB (Leuschel and Butler 2003) and AnimB6 . They were able to automatically discharge
72% of the proof obligations by calling Rodin. Hence, we encoded in {log} the entire
Event-B specification of the LGS and used {log} to automatically discharge 100% of the
proof obligations generated by the Rodin tool in roughly 290 s (Cristiá and Rossi 2024).
The {log} encoding of the LGS7 comprises 7.8 KLOC plus 465 proof obligations. In order
to discharge all those proof obligations we used the combination between types and CLP
as discussed above. Many proof obligations could be avoided while many others were
simpler, due to the combined work between the typechecker and the constraint solver—
as shown in Example 2; see also (Cristiá and Rossi 2024, Section 4.5). The net result is
an automatically verified {log} prototype of the LGS.

Android Permission System. A model of the Android permission system has been de-
veloped and certified in Coq (Betarte et al. 2015; Betarte et al. 2016; Luna et al. 2018;
De Luca and Luna 2020). As with the previous case study, we translated the Coq model
into {log} and used it to run all the verification conditions proposed in Coq8 (Cristiá
et al. 2023). {log} is able to automatically prove 24 of the 27 properties (≈ 90%) in ap-
proximately 21 m. The 3 properties that cannot be proved by {log} require 500 LOC of
Coq proof commands (≈ 2% of all proof commands). That is, {log} automatically proves
90% of the properties covering 98% of the proof effort in terms of proof commands. As
can be seen, the gain in terms of human effort is considerable. The type system proposed
for {log} can encode all the types used in the Coq model. This is important given that
Coq is prized by its powerful type system. Then, concerning the Android model, our
typechecker can prove the same type properties that are proved by Coq, whereas the
constraint solver is able to automatically prove most of the properties that are manually
proved in Coq.


6 http://www.animb.org
7 https://www.clpset.unipr.it/SETLOG/APPLICATIONS/lgs.zip
8 {log} code of Android 10’s permission system: http://www.clpset.unipr.it/SETLOG/APPLICATIONS/
 android.zip
14                                   M. Cristiá and G. Rossi

                              6 Discussion and related work
The inclusion of prescriptive type systems in logic programming9 can be traced back
to the seminal work of Mycroft and O’Keefe (1984); later on Lakshman and Reddy
(1991) define the formal semantics for that type system. At some point in time, these
ideas started to be part of different logic programming languages (Hill and Lloyd 1994;
Schrijvers et al. 2008), and even they made through all the way to functional logic pro-
gramming languages (Somogyi et al. 1996; Hanus 2013). Schrijvers et al. (2008) propose
types to be optional in SWI-Prolog and Yap, as we do for {log}.
   Descriptive type systems provide an approximation of the semantics of a given program,
usually, as a set of terms greater than (cf. set inclusion) the one provided by the semantics.
Answers of a descriptive typechecker are necessarily approximate. These type systems
(Zobel 1987; Bruynooghe and Janssens 1988; Frühwirth et al. 1991; Dart and Zobel 1992;
Yardeni et al. 1992; Heintze and Jaffar 1992; Gallagher and de Waal 1994; Barbosa et al.
2021) have been used in the context of abstract interpretation and program analysis of
logic programs (Vaucheret and Bueno 2002; Hermenegildo et al. 2005; Pietrzak et al.
2008).
   It is worth to be noted that some other works on program approximation, e.g., (Heintze
and Jaffar 1990; Talbot et al. 1997), use a technique called set-based analysis. This is not
to be confused with our approach. We use sets and binary relations as the main data
structures for programming and specification, while in these other works sets are used to
analyze general logic programs. In other words, we use sets and binary relations to write
programs, they use sets to analyze them. Descriptive type systems were also applied to
CLP, e.g., as a means to find certain classes of errors in programs (Drabent et al. 2002).
   Fages and Coquery (2001) study a prescriptive type system for CLP programs that
is independent from any constraint domain. The authors prove that their type system
verifies subject reduction (i.e., type preservation) w.r.t. the abstract execution model
of CLP (cf. accumulation of constraints), and w.r.t. an execution model of CLP with
substitutions. As far as we understand, Fages and Coquery do not prove progress—cf.
Theorem 1. Clearly, Fages and Coquery’s preservation result reliefs us of proving that
{log}’s CLP engine preserves types because it is just an implementation of the general
CLP scheme addressed by these authors. On the other hand, Fages and Coquery’s result
depends on the well-typedness of each rewrite rule of the execution model. This is exactly
what we prove in Theorem 1: that the execution model of our CLP language verifies type
safety—i.e., preservation and progress. However, instead of typing each rewrite rule we
prove that they preserve types. We are not aware of previous works in the field of CLP
featuring a formulation of type safety like that of Theorem 1.
   As we have said, {log}’s type system is inspired in the type system of Z and B. Borrow-
ing ideas from these notations is quite natural as {log} is based on a set theory similar to
those underlying Z and B. In Z and B type inference, in the sense of deducing the type of
some variable from the terms where it participates in, is not allowed; all variables must
be declared. Subtyping is also nonexistent in Z and B. So we do in {log}. Differently from
Z and B, in {log} elements of basic types have a known form (e.g., b?a). This is useful


9 The technical report by Cirstea et al. (2004) provides an introduction and survey about types in logic
  programs. There is also a comprehensive book on the matter edited by Pfenning (1992).
                  Combining Type Checking and Set Constraint Solving                          15

when {log} is used as a programming language because users can give values to input
variables of basic types. Obviously, tools for Z and B implement typecheckers similar to
ours. Leuschel (2020) shows snippets of the Prolog implementation of a B typechecker.
   Finally, we use the combination between type checking and constraint solving in a
different way compared to works in logic programming. For example, Drabent et al.
(2002) or Pietrzak et al. (2008) mentioned above, solve a system of constraints (sometimes
based on set-analysis) to find out whether or not the program verifies some properties
given by means of types. In {log}, type checking is used to rule out wrong programs or
specifications, and constraint solving is used as the mechanism of a sort of automated
theorem prover. In {log}, programs, specifications and properties are set formulas as in
Z and B.


                                       7 Conclusions
We have defined a type system and a typechecker for the CLP tool {log}. Type checking
can be activated or not according to the users needs. The type system is based on the
type systems of formal notations such as B and Z. We have proved that the operational
semantics of {log} is type safe by adapting the type safety theorem of functional pro-
gramming to the CLP context. Although the typechecker and the constraint solver are
mostly independent from each other, they work together when formulas include finite
types in order to ensure soundness. It is our understanding that the results presented
in this paper show that the combination between a type system and CLP might be a
practical approach to software verification. The case studies based on the LGS problem
and the Android permission system provide empirical evidence about this claim.
   As future work we want to study how the introduction of types may help with the
problem of computing the negation of formulas. For example, the negation of p(x ) :- x =
(a, y) yields ∀ y(x ̸= (a, y)), which lies outside the decision procedures implemented in
{log}. However, if types are brought into the game, the negation of p(x ) can be turned
into a formula that {log} can solve. In effect, x = (a, y) is type-correct iff a is part of a sum
type, say sum([a, b(int)]), y is of some type τy , and x is of type prod(sum([a, b(int)]), τy ).
Then, if x is different from (a, y) for all y, it can only be equal to (b(z ), w ) for some z and
some w , because otherwise it would lie outside its type. Therefore, ∀ y(x ̸= (a, y)) can be
turned into ∃ z , w (x = (b(z ), w )). {log} is able to deal with formulas including the latter,
meaning that it would be able to deal with formulas including the negation of p(x )—
something that, without types, could not be achieved. Then, we will work in finding
the class of formulas whose negation can be safely computed when type information is
available. This would be another area where the interplay between the typechecker and
the constraint solver produces good results.
   We think that the combination between type checking and constraint solving can
be improved through the introduction of subtypes. For example, if 0 ≤ x is a type
invariant and we have x ′ = x + 3 we need to prove 0 ≤ x ∧ x ′ = x + 3 ⇒ 0 ≤ x ′ .
However, by introducing nat as a subtype of int, typing + : nat × nat → nat and declaring
dec([x , x ′ ], nat), it would be possible for the typechecker to automatically discharge the
invariant by deciding whether the program is type-correct or not. The greatest gains along
this line would be the introduction of a type for functions (say fun) as a subtype of rel
and a library of function-based constraints that would typecheck when their arguments
16                                M. Cristiá and G. Rossi

are functions. This would make unnecessary the introduction of a number of invariance
lemmas ensuring that a given binary relation is indeed a function. For instance, the
update or override operator available in B (◁+) and Z (⊕) is known to be closed for
functions. Hence, a type declaration such as ◁+ : fun(T , U ) × fun(T , U ) → fun(T , U ) can
be added to the system. In this case, many proof obligations that today are passed to a
prover could be easily discharged by the typechecker, instead.

Competing interests: The authors declare none



                                        References
Abrial, J., Butler, M. J., Hallerstede, S., Hoang, T. S., Mehta, F., and Voisin, L.
  2010. Rodin: an open toolset for modelling and reasoning in Event-B. Int. J. Softw. Tools
  Technol. Transf. 12, 6, 447–466.
Abrial, J.-R. 1996. The B-book: Assigning Programs to Meanings. Cambridge University Press,
  New York, NY, USA.
Abrial, J.-R. 2010. Modeling in Event-B: System and Software Engineering, 1st ed. Cambridge
  University Press, New York, NY, USA.
Barbosa, J., Florido, M., and Costa, V. S. 2021. Data type inference for logic programming.
  In Logic-Based Program Synthesis and Transformation - 31st International Symposium, LOP-
  STR 2021, Tallinn, Estonia, September 7-8, 2021, Proceedings, E. D. Angelis and W. Vanhoof,
  Eds. Lecture Notes in Computer Science, vol. 13290. Springer, 16–37.
Barendregt, H. P., Dekkers, W., and Statman, R. 2013. Lambda Calculus with Types.
  Perspectives in logic. Cambridge University Press.
Betarte, G., Campo, J. D., Luna, C., and Romano, A. 2016. Formal analysis of Android’s
  permission-based security model,. Sci. Ann. Comp. Sci. 26, 1, 27–68.
Betarte, G., Campo, J. D., Luna, C. D., and Romano, A. 2015. Verifying Android’s
  permission model. In Theoretical Aspects of Computing - ICTAC 2015 - 12th International
  Colloquium Cali, Colombia, October 29-31, 2015, Proceedings, M. Leucker, C. Rueda, and
  F. D. Valencia, Eds. Lecture Notes in Computer Science, vol. 9399. Springer, 485–504.
Bonichon, R., Delahaye, D., and Doligez, D. 2007. Zenon : An extensible automated
  theorem prover producing checkable proofs. In Logic for Programming, Artificial Intelligence,
  and Reasoning, 14th International Conference, LPAR 2007, Yerevan, Armenia, October 15-
  19, 2007, Proceedings, N. Dershowitz and A. Voronkov, Eds. Lecture Notes in Computer
  Science, vol. 4790. Springer, 151–165.
Boniol, F. and Wiels, V. 2014. The landing gear system case study. In ABZ 2014: The
  Landing Gear Case Study - Case Study Track, Held at the 4th International Conference on
  Abstract State Machines, Alloy, B, TLA, VDM, and Z, Toulouse, France, June 2-6, 2014.
  Proceedings, F. Boniol, V. Wiels, Y. A. Ameur, and K. Schewe, Eds. Communications in
  Computer and Information Science, vol. 433. Springer, 1–18.
Bruynooghe, M. and Janssens, G. 1988. An instance of abstract interpretation integrating
  type and mode inferencing. In Logic Programming, Proceedings of the Fifth International
  Conference and Symposium, Seattle, Washington, USA, August 15-19, 1988 (2 Volumes),
  R. A. Kowalski and K. A. Bowen, Eds. MIT Press, 669–683.
Cirstea, H., Coquery, E., Drabent, W., Fages, F., Kirchner, C., Maluszynski, J., and
  Wack, B. 2004. Types for Web Rule Languages: a preliminary study. Contract A04-R-560
  —— cirstea04e, Inria. Rapport de contrat.
Cristiá, M., Luca, G. D., and Luna, C. 2023. An automatically verified prototype of the
  Android permissions system. J. Autom. Reason. 67, 2, 17.
                   Combining Type Checking and Set Constraint Solving                          17

Cristiá, M. and Rossi, G. 2018. A set solver for finite set relation algebra. In Relational
 and Algebraic Methods in Computer Science - 17th International Conference, RAMiCS 2018,
 Groningen, The Netherlands, October 29 - November 1, 2018, Proceedings, J. Desharnais,
 W. Guttmann, and S. Joosten, Eds. Lecture Notes in Computer Science, vol. 11194. Springer,
 333–349.
Cristiá, M. and Rossi, G. 2019. Rewrite rules for a solver for sets, binary relations and partial
 functions. Tech. rep. https://www.clpset.unipr.it/SETLOG/calculus.pdf.
Cristiá, M. and Rossi, G. 2020. Solving quantifier-free first-order constraints over finite sets
 and binary relations. J. Autom. Reason. 64, 2, 295–330.
Cristiá, M. and Rossi, G. 2021a. Automated proof of Bell-LaPadula security properties. J.
 Autom. Reason. 65, 4, 463–478.
Cristiá, M. and Rossi, G. 2021b. Automated reasoning with restricted intensional sets. J.
 Autom. Reason. 65, 6, 809–890.
Cristiá, M. and Rossi, G. 2021c. An automatically verified prototype of the Tokeneer ID
 station specification. J. Autom. Reason. 65, 8, 1125–1151.
Cristiá, M. and Rossi, G. 2022. Combining type checking and set constraint solving to
 improve automated software verification. CoRR abs/2205.01713.
Cristiá, M. and Rossi, G. 2023. Integrating cardinality constraints into constraint logic
 programming with sets. Theory Pract. Log. Program. 23, 2, 468–502.
Cristiá, M. and Rossi, G. 2024. A decision procedure for a theory of finite sets with finite
 integer intervals. ACM Trans. Comput. Log. 25, 1, 3:1–3:34.
Cristiá, M. and Rossi, G. 2024. From computational logic to computational biology: Essays
 dedicated to Alfredo Ferro to celebrate his scientific career. Springer Nature Switzerland,
 Chapter An Automatically Verified Prototype of a Landing Gear System, 56–81.
Cristiá, M., Rossi, G., and Frydman, C. S. 2013. {log} as a test case generator for the
 Test Template Framework. In SEFM, R. M. Hierons, M. G. Merayo, and M. Bravetti, Eds.
 Lecture Notes in Computer Science, vol. 8137. Springer, 229–243.
Dart, P. W. and Zobel, J. 1992. A regular type language for logic programs. In Types in
 Logic Programming, F. Pfenning, Ed. The MIT Press, 157–187.
De Luca, G. and Luna, C. 2020. Towards a certified reference monitor of the Android 10
 permission system. In 26th International Conference on Types for Proofs and Programs,
 TYPES 2020, March 2-5, 2020, University of Turin, Italy, U. de’Liguoro, S. Berardi, and
 T. Altenkirch, Eds. LIPIcs, vol. 188. Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 3:1–
 3:18.
Dovier, A., Piazza, C., Pontelli, E., and Rossi, G. 2000. Sets and constraint logic pro-
 gramming. ACM Trans. Program. Lang. Syst. 22, 5, 861–931.
Dovier, A., Pontelli, E., and Rossi, G. 2006. Set unification. Theory Pract. Log. Pro-
 gram. 6, 6, 645–701.
Drabent, W., Maluszynski, J., and Pietrzak, P. 2002. Using parametric set constraints
 for locating errors in CLP programs. Theory Pract. Log. Program. 2, 4-5, 549–610.
Fages, F. and Coquery, E. 2001. Typing constraint logic programs. Theory Pract. Log.
  Program. 1, 6, 751–777.
Frühwirth, T. W., Shapiro, E., Vardi, M. Y., and Yardeni, E. 1991. Logic programs as
  types for logic programs. In Proceedings of the Sixth Annual Symposium on Logic in Computer
  Science (LICS ’91), Amsterdam, The Netherlands, July 15-18, 1991. IEEE Computer Society,
  300–309.
Gallagher, J. P. and de Waal, D. A. 1994. Fast and precise regular approximations of logic
 programs. In Logic Programming, Proceedings of the Eleventh International Conference on
 Logic Programming, Santa Marherita Ligure, Italy, June 13-18, 1994, P. V. Hentenryck, Ed.
 MIT Press, 599–613.
18                                M. Cristiá and G. Rossi

Hanus, M. 2013. Functional logic programming: From theory to Curry. In Programming Logics
  - Essays in Memory of Harald Ganzinger, A. Voronkov and C. Weidenbach, Eds. Lecture
  Notes in Computer Science, vol. 7797. Springer, 123–168.
Harper, R. 2016. Practical Foundations for Programming Languages (2nd. Ed.). Cambridge
  University Press.
Heintze, N. and Jaffar, J. 1990. A finite presentation theorem for approximating logic
  programs. In Conference Record of the Seventeenth Annual ACM Symposium on Principles
  of Programming Languages, San Francisco, California, USA, January 1990, F. E. Allen, Ed.
  ACM Press, 197–209.
Heintze, N. and Jaffar, J. 1992. Semantic types for logic programs. In Types in Logic
  Programming, F. Pfenning, Ed. The MIT Press, 141–155.
Hermenegildo, M. V., Puebla, G., Bueno, F., and López-Garcı́a, P. 2005. Integrated
  program debugging, verification, and optimization using abstract interpretation (and the Ciao
  system preprocessor). Sci. Comput. Program. 58, 1-2, 115–140.
Hill, P. M. and Lloyd, J. W. 1994. The Gödel programming language. MIT Press.
Lakshman, T. L. and Reddy, U. S. 1991. Typed Prolog: A semantic reconstruction of the
  Mycroft-O’Keefe type system. In Logic Programming, Proceedings of the 1991 International
  Symposium, San Diego, California, USA, Oct. 28 - Nov 1, 1991, V. A. Saraswat and K. Ueda,
  Eds. MIT Press, 202–217.
Lamport, L. and Paulson, L. C. 1999. Should your specification language be typed? ACM
  Trans. Program. Lang. Syst. 21, 3, 502–526.
Leuschel, M. 2020. Prolog for verification, analysis and transformation tools. In Proceedings
  8th International Workshop on Verification and Program Transformation and 7th Workshop
  on Horn Clauses for Verification and Synthesis, VPT/HCVS@ETAPS 2020, Dublin, Ireland,
  25-26th April 2020, L. Fribourg and M. Heizmann, Eds. EPTCS, vol. 320. 80–94.
Leuschel, M. and Butler, M. 2003. ProB: A model checker for B. In FME, A. Keijiro,
  S. Gnesi, and D. Mandrioli, Eds. Lecture Notes in Computer Science, vol. 2805. Springer-
  Verlag, 855–874.
Luna, C., Betarte, G., Campo, J. D., Sanz, C., Cristiá, M., and Gorostiaga, F. 2018. A
  formal approach for the verification of the permission-based security model of Android. CLEI
  Electron. J. 21, 2.
Mammar, A. and Laleau, R. 2014. Modeling a landing gear system in Event-B. In ABZ 2014:
  The Landing Gear Case Study - Case Study Track, Held at the 4th International Conference
  on Abstract State Machines, Alloy, B, TLA, VDM, and Z, Toulouse, France, June 2-6, 2014.
  Proceedings, F. Boniol, V. Wiels, Y. A. Ameur, and K. Schewe, Eds. Communications in
  Computer and Information Science, vol. 433. Springer, 80–94.
Mammar, A. and Laleau, R. 2017. Modeling a landing gear system in Event-B. Int. J. Softw.
  Tools Technol. Transf. 19, 2, 167–186.
Martin-Löf, P. 1984. Intuitionistic type theory. Studies in proof theory, vol. 1. Bibliopolis.
Mentré, D., Marché, C., Filliâtre, J.-C., and Asuka, M. 2012. Discharging proof obliga-
  tions from Atelier B using multiple automated provers. In ABZ, J. Derrick, J. A. Fitzgerald,
  S. Gnesi, S. Khurshid, M. Leuschel, S. Reeves, and E. Riccobene, Eds. Lecture Notes in
  Computer Science, vol. 7316. Springer, 238–251.
Milner, R. 1978. A theory of type polymorphism in programming. J. Comput. Syst. Sci. 17, 3,
  348–375.
Mycroft, A. and O’Keefe, R. A. 1984. A polymorphic type system for Prolog. 23, 3,
  295–307.
Pfenning, F., Ed. 1992. Types in Logic Programming. The MIT Press.
Pierce, B. C. 2002. Types and programming languages. MIT Press.
Pietrzak, P., Correas, J., Puebla, G., and Hermenegildo, M. V. 2008. A practical
  type analysis for verification of modular prolog programs. In Proceedings of the 2008 ACM
                  Combining Type Checking and Set Constraint Solving                      19

  SIGPLAN Symposium on Partial Evaluation and Semantics-based Program Manipulation,
  PEPM 2008, San Francisco, California, USA, January 7-8, 2008, R. Glück and O. de Moor,
  Eds. ACM, 61–70.
Rossi, G. 2008. {log}. http://www.clpset.unipr.it/setlog.Home.html. Last access 2022.
Schrijvers, T., Costa, V. S., Wielemaker, J., and Demoen, B. 2008. Towards typed
  Prolog. In Logic Programming, 24th International Conference, ICLP 2008, Udine, Italy,
  December 9-13 2008, Proceedings, M. G. de la Banda and E. Pontelli, Eds. Lecture Notes in
  Computer Science, vol. 5366. Springer, 693–697.
Somogyi, Z., Henderson, F., and Conway, T. C. 1996. The execution algorithm of Mercury,
  an efficient purely declarative logic programming language. 29, 1-3, 17–64.
Spivey, J. M. 1992. The Z notation: a reference manual. Prentice Hall International (UK)
  Ltd., Hertfordshire, UK, UK.
Talbot, J., Tison, S., and Devienne, P. 1997. Set-based analysis for logic programming
  and tree automata. In Static Analysis, 4th International Symposium, SAS ’97, Paris, France,
  September 8-10, 1997, Proceedings, P. V. Hentenryck, Ed. Lecture Notes in Computer Science,
  vol. 1302. Springer, 127–140.
Vaucheret, C. and Bueno, F. 2002. More precise yet efficient type inference for logic pro-
  grams. In Proceedings of the 12th International Workshop on Logic Programming Environ-
  ments, WLPE 2002, Copenhagen, Denmark, July 31, 2002, A. Tessier, Ed. 63–76.
Wright, A. K. and Felleisen, M. 1994. A syntactic approach to type soundness. Inf.
  Comput. 115, 1, 38–94.
Yardeni, E., Frühwirth, T. W., and Shapiro, E. 1992. Polymorphically typed logic pro-
  grams. In Types in Logic Programming, F. Pfenning, Ed. The MIT Press, 63–90.
Zobel, J. 1987. Derivation of polymorphic types for PROLOG programs. In Logic Programming,
  Proceedings of the Fourth International Conference, Melbourne, Victoria, Australia, May 25-
  29, 1987 (2 Volumes), J. Lassez, Ed. MIT Press, 817–838.
