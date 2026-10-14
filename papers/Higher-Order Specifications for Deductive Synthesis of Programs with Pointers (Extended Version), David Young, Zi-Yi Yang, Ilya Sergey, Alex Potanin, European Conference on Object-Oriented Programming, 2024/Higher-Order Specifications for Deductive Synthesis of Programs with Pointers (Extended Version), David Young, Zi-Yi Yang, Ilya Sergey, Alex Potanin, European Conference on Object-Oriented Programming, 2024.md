                                         Higher-Order Specifications
                                         for Deductive Synthesis of Programs with
                                         Pointers (Extended Version)
                                         David Young* # 
                                         University of Kansas, USA

                                         Ziyi Yang* # 
                                         National University of Singapore, Singapore

                                         Ilya Sergey # 
                                         National University of Singapore, Singapore

                                         Alex Potanin # 
                                         Australian National University, Australia
arXiv:2407.09143v2 [cs.PL] 15 Jul 2024




                                                 Abstract
                                         Synthetic Separation Logic (SSL) is a formalism that powers SuSLik, the state-of-the-art approach
                                         for the deductive synthesis of provably-correct programs in C-like languages that manipulate heap-
                                         based linked data structures. Despite its expressivity, SSL suffers from two shortcomings that hinder
                                         its utility. First, its main specification component, inductive predicates, only admits first-order
                                         definitions of data structure shapes, which leads to the proliferation of “boiler-plate” predicates
                                         for specifying common patterns. Second, SSL requires concrete definitions of data structures to
                                         synthesise programs that manipulate them, which results in the need to change a specification for
                                         a synthesis task every time changes are introduced into the layout of the involved structures.
                                             We propose to significantly lift the level of abstraction used in writing Separation Logic specific-
                                         ations for synthesis—both simplifying the approach and making the specifications more usable and
                                         easy to read and follow. We avoid the need to repetitively re-state low-level representation details
                                         throughout the specifications—allowing the reuse of different implementations of the same data
                                         structure by abstracting away the details of a specific layout used in memory. Our novel high-level
                                         front-end language called Pika significantly improves the expressiveness of SuSLik.
                                             We implemented a layout-agnostic synthesiser from Pika to SuSLik enabling push-button syn-
                                         thesis of C programs with in-place memory updates, along with the accompanying full proofs that
                                         they meet Separation Logic-style specifications, from high-level specifications that resemble ordinary
                                         functional programs. Our experiments show that our tool can produce C code that is comparable
                                         in its performance characteristics and is sometimes faster than Haskell.

                                         Keywords and phrases Program Synthesis, Separation Logic, Functional Programming


                                             1    Introduction

                                         Recent advances in program synthesis have allowed programmers to concentrate on stating
                                         precise specifications—leaving the job of generating provably correct and efficient imperative
                                         code to the synthesiser, such as SuSLik [6, 9, 13]. Such specifications are usually expressed
                                         using (Synthetic) Separation Logic [7,10] that while hugely successful in verifying properties
                                         of pointer-manipulating programs remains out of reach to many mainstream developers. As
                                         the programs grow in complexity, such SSL specifications can become exceedingly verbose
                                         and complex—making the job of specification writer especially error-prone and defeating
                                         the purpose of a usable proof automation toolchain.


                                         ∗
                                             Contributed equally to this work.
2           Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


        The power of Separation Logic (SL) specifications for the tasks of both verification and
    synthesis, is its mechanism of inductive predicates that concisely capture the shape of pos-
    sibly recursive pointer-based tree-like data structures, determining both induction schemes
    for verification and the shape of recursion for the synthesis tasks of the programs that ma-
    nipulate such data structures [10]. The surprising ability of SL specifications to capture
    precisely the logic of a desired program to be synthesised in the logical assertions comes
    at the price of the involved inductive predicates being (a) first-order and (b) somewhat
    low-level, with both these aspects posing limitations to the usability of SL-based program
    synthesis.
        The first-order nature of the predicates means, for instance, that synthesis tasks that
    involve several data structures with very similar heap layouts would require to use different
    predicate definitions. As a specific example, consider a task synthesising two functions, f
    and g. Both f and g take as an argument a pointer to a linked list of integers; f increments
    all elements of the list by one, while g multiplies all its elements by two. To specify these two
    tasks, the state-of-the-art tools for program synthesis based on SL specifications require the
    user to provide, in addition to the pre-/postconditions, three different inductive predicates:
    one for an arbitrary list, another for a list that carries a known payload, with each element
    incremented by one, and the final capturing the multiplication of each element by two.
        The second aspect, i.e., the low-level nature of the SL inductive predicates used for
    synthesis, shows up when we try to rewrite an already specified synthesis task for a data
    structure with a slightly different layout. As an example, imagine defining the task of
    concatenating two lists. It is natural to expect that the specification will look very similar
    for both singly and doubly linked lists. Yet, since those are two different structures, with
    two different layouts, the user would require to supply two different task specifications.
        A seasoned programmer would immediately notice that both issues (a) and (b) very
    much resemble the struggle that one faces when programming in a language that does not
    provide certain abstractions, which are nowadays mostly taken for granted: higher-order
    functions and abstract data types. Our first example could be streamlined should the SL-
    based specification language offer a way to define a function similar to List.map, available
    in all popular functional programming languages, so it could be used to concisely express
    the two scenarios of manipulating with the payload of a list’s elements. The second example
    would benefit from the ability to specify concatenation of abstract lists, while separately
    handling manipulations with single- or doubly-linked lists in terms of their memory layouts.


    Key Ideas
    The two challenges faced by the SSL specification language for the synthesis of heap-manipulating
    programs—the need for higher-order functions and abstract data types—have provided the
    primary motivation for this work.
        As a solution, we developed Pika: a high-level front-end language and specification
    translation framework built on to of the state-of-the-art SL-based program synthesiser SuS-
    Lik.1 SuSLik is based on a variant of separation logic called synthetic separation logic or
    SSL [9]. Pika has a syntax similar to popular functional programming languages and fea-
    tures specification-level higher-order functions on Algebraic Data Types (ADTs). In addition
    to being more succinct in comparison to Synthetic Separation Logic (SSL), the specification


    1
        Both susliks and pikas are Central Asian mammals. Pikas might look similar to susliks, but are more
        nimble and have longer life expectancy.
       Young et al.                                                                                   3



                                                         Pika code             SuSLik specification   SuSLik synthesis t



   Figure 1 Pika translation pipeline


formalism of SuSLik, Pika also addresses its reusability issues outlined above. First, the use
of specification-level higher-order functions allows the user to abstract over the specific prop-
erties of the payloads of the heap-based data structures, thus, generalising existing inductive
predicates for so they could be employed in a wider range of synthesis tasks. Second, by ma-
nipulating ADTs, the synthesis specifications do not need to deal with the specific memory
layouts of the data structures. This separates the specification of the tasks that operate on
those data structures from the low-level details of their memory representations.
    The Pika pipeline is depicted in Fig. 1. As our goal was to extend the expressivity of
SuSLik by giving it a high-level specification language while retaining its meta-theoretical
guarantees (i.e., the certifiable correctness of the programs it synthesises), we had to over-
come several technical obstacles when designing Pika and implementing it on top of SuSLik.
First, we had to formally define the operational semantics of Pika and its translation to
SSL-based specifications of SuSLik, defining the corresponding soundness result, relating
the behaviour of programs eventually synthesised to that of their high-level counterparts
(Sec. 3). Second, to support the higher-order specifications of Pika, we introduced conservat-
ive extensions to SuSLik’s specification language as well as to its deductive synthesis rules,
to make it capable of handling pre-/postconditions with first-class functions operating on
the payload of heap-stored data types (Sec. 4).


Pika as a Programming Language
Given the close similarity of Pika, our new specification language, to general-purpose func-
tional programming languages, such as Haskell, it is natural to wonder whether it’s possible
to leverage its underlying synthesis pipeline as a way to produce efficient imperative pro-
grams in a language such as C from equivalent high-level functional programs. In other
words, if we decide to use a combination Pika + SuSLik as a compiler, would it be a viable
replacement to many-decades old tools such as Glasgow Haskell Compiler (GHC) [3], for
producing efficient runnable code? To answer this question, we have conducted evaluation
on several list- and tree-manipulating benchmarks, comparing the performance of verified
C code, emitted by SuSLik from Pika specifications, to that of executables produced for
equivalent tasks by GHC.
    Our preliminary results are encouraging: thanks to avoiding unnecessary allocation and
using destructive heap updates whenever possible, the C code synthesised by Pika + SuSLik
outperforms the GHC output (with compiler optimisations flags turned) in the majority
of list-manipulating benchmarks we’ve tried; our synthesis tool also produces strictly more
performant C code for tree-manipulating benchmarks when compared to the corresponding
Haskell programs, compiled by GHC without or with optimisations (Sec. 5). In particular,
we specifically observe this when we compare C code synthesised by Pika + SuSLik with no
C compiler optimisation flags to GHC compiled code with no GHC compiler flags.


Contributions
In this work, we make the following contributions:
4          Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


         We address the expressivity limitations of SSL, the specification formalism of the state-
         of-the-art deductive synthesis tool SuSLik by developing Pika—a high-level specification
         language with higher-order functions and abstract data types.
         We formally define the operational semantics of Pika and prove the soundness of trans-
         lation from Pika to pre-/postconditions in SSL.
         We develop an extension to SuSLik’s specification and synthesis mechanism that enables
         translation from Pika specifications featuring first-class functions.
         We observe that the synthesis tool resulting from the combination Pika + SuSLik enables
         certified memory-layout-agnostic compilation from a functional specification to C code.
         We report on the evaluation of the Pika regarding its expressiveness and performance.
         In particular, we show that the C code it produces frequently outperforms equivalent
         Haskell programs compiled by GHC.

     2      Overview
    2.1     Background
    The Pika language is translated into SuSLik [9], which is a program synthesis tool that uses
    Synthetic Separation Logic (SSL)-a variant of Hoare-style [4] Separation Logic (SL) [7].
        A synthesis task specification in SuSLik is given as a function signature together with
    a pair of pre- and post-conditions, which are both SL assertions [9]. The synthesiser gen-
    erates code that satisfies the given specification, along with the SL proof of its correctness
    by searching in a space of proofs that can be derived by using the rules of the underlying
    logic [13]. A distinguishing feature of Synthetic Separation Logic is the format of its asser-
    tions. An SSL assertion consists of two parts: a pure part and a spatial part. The pure
    part is a Boolean expression constraining the variables of the specification using a few basic
    relations, like equality and the less-than relation for integers. The spatial part is a symbolic
    heap, which consists of a list of heaplets separated by the ∗ symbol.
        Each heaplet takes on one of the following forms [9]:

         emp: This represents the empty heap. It is also the left and right identity for ∗.
         ℓ 7→ a: This asserts that memory location ℓ points to the value a. It also asserts that
         the location ℓ is accessible.
         [ℓ, ι]: At memory location ℓ, there is a block of size ι.
         p(ϕ): This is an application of the inductive predicate p to the arguments ϕ. An induct-
         ive predicate has a collection of branches, guarded by Boolean expressions (conditions)
         on the parameters. The body of each branch is an SSL assertion. The assertion associ-
         ated with the first branch condition that is satisfied is used in place of the application.
         Note that inductive predicates can be (and often are) recursively defined.

    The general form of an SSL assertion is (p; h1 ∗ h2 ∗ · · · ∗ hn ), where p is the pure part and
    h1 , h2 , · · · , hn are the heaplets which are the conjuncts that make up a separated conjunction
    of the spatial part. ∗ is separating conjunction: h1 ∗ h2 means that the heaplets h1 and h2
    apply to disjoint parts of the heap. A syntax definition for SSL is given in Fig. 2, which is
    adapted from Cyclic Program Synthesis by Itzhaky et al. [6]. We will also use the symbol
    ** for separating conjunction and the symbol :-> for 7→.
         As the specification language of SuSLik, SSL serves as the compilation target for the
    Pika language. From there, executable programs are generated through SuSLik’s program
    synthesis. Consider a program that takes an integer x and a result in location r and stores
    x + 1 at location r. This can be written as the SuSLik specification:
        Young et al.                                                                                5



      Variable               x, y Alpha-numeric identifiers ∈ Var
      Size, offset           n, ι Non-negative integers
      Expression             e ::= 0 | true | x | e = e | e ∧ e | ¬e | d
      T -expr.               d ::= n | x | d + d | n · d | {} | d | · · ·
      Command                c ::= let x = *(x + ι) | *(x + ι) = e |
                                   let x = malloc(n) | free(x) | error | f(ei )
      Program                Π ::= f (xi ) { c } ; c
      Logical variable       ν, ω
      Cardinality variable   α
      T -term                κ ::= ν | e | · · ·
      Pure logic term        ϕ, ψ, χ ::= κ | ϕ = ϕ | ϕ ∧ ϕ | ¬ϕ
      Symbolic heap          P, Q, R ::= emp | ⟨e, ι⟩ 7→ e | [e, ι] | pα (ϕi ) | P ∗ Q
      Heap predicate         D ::= pα (xi ) : ej ⇒ ∃y.{χj ; Rj }
      Assertion              P, Q ::= {ϕ; P }
      Environment            Γ ::= ∀xi .∃yj .
      Context                Σ ::= D
      Synthesis goal         G ::= P ⇝ Q

   Figure 2 Syntax of Synthetic Separation Logic



void add1Proc ( int x , loc r )
  { r :-> 0 }
  { y == x + 1 ; r : - > y }
{ ?? }

This example can be written as follows in our tool:
 add1Proc : Int -> Int ;
 add1Proc x := x + 1;

In contrast with SuSLik spec, the Pika one requires no direct manipulation with pointers.

2.2     The Pika Language
While SSL provides a specification language that allows tools like SuSLik to synthesise code,
it is only able to express specifications as pointers. This is useful for some applications, such
as embedded systems, but it does not provide any high-level abstractions. As a result, every
part of a specification is tailored to a specific memory representation of each data structure
involved. To address this shortcoming, we introduce a language with algebraic data types
that gets translated into SSL specifications. Additionally, we introduce a language construct
that allows the programmer to specify a memory representation of an algebraic data type
called a layout. The distinction between algebraic data types and layouts provides the
separation of concerns between the low-level representation of a data structure and code
that manipulates it at a high level.
     Syntactically, Pika resembles a functional programming language of the Miranda [12] and
Haskell [5] lineage. It supports algebraic data types, pattern matching at top-level function
definitions (though not inside expressions) and Boolean guards. The primary difference
arises due to the existence of layouts and the fact that the language is compiled to an SSL
specification rather than executable code. Beyond algebraic data types and layouts, Pika
has a built-in type for integers as well as Booleans.
6         Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


     data List := Nil | Cons Int List ;

    Sll : List >-> layout [ x ];
    Sll ( Nil ) := emp ;
    Sll ( Cons head tail ) := x : - > head , ( x +1) : - > tail , Sll tail ;


       Figure 3 List algebraic data type together with its singly-linked list layout Sll


        Functions in Pika are only defined by their operations on algebraic data types. Thus, all
    function definitions are “layout-polymorphic” over the particular choices of layouts for their
    arguments and result. Giving a layout polymorphic function, a particular choice of layouts
    is called “instantiation”. Specifying the layout of a non-function value is called “lowering.”
        The code generator is instructed to generate a SuSLik specification for a certain func-
    tion at a certain instantiation by using a %generate directive. For example, if there is
    a function definition with the type signature mapAdd1 : List -> List, a line reading
    %generate mapAdd1 [Sll] Sll would instruct the Pika compiler to generate the SuSLik
    inductive predicate corresponding to mapAdd1 instantiated to the Sll layout for both its
    argument and its result. An example of an ADT definition and a corresponding layout defin-
    ition is given in Fig. 3. There is one unusual part of the syntax in particular that requires
    further explanation: layout type signatures. A layout definition consists of a layout type
    signature and a pattern match (much like a function definition), with lists of SSL heaplets
    on the right-hand sides. A layout type signature has a special form A : α ↣ layout[x].
    This says that the layout A is for the algebraic data type α and the SSL output variable x
    denoting the “head” pointer of the respective structure.


    2.3    Pika by Example
    We demonstrate the characteristic usages of Pika by a series of examples. In these examples,
    we will often make use of the List algebraic data type and its Sll layout from Fig. 3. A
    simple example of Pika code that illustrates algebraic data types and layouts is a function
    which creates a singleton list out of the given integer argument:
    % generate singleton [ Int ] Sll

     singleton : Int -> List ;
     singleton x := Cons x ( Nil );

    This gets compiled to the following SuSLik specification (modulo auto-generated names):
    predicate singleton ( int p , loc r ) {
    | true = > { r : - > p ** ( r +1) : - > 0 ** [r ,2] }
    }

    A slightly more complicated example comes from trying to write a functional-style map
    function directly in SuSLik. Consider a function which adds 1 to each integer in a list of
    integers. Considering the list implementation to be a singly-linked list with a fixed layout,
    one way to express this in SuSLik is shown in Fig. 4. In the mapAdd1 predicate, the input list
    is given as the x parameter and the r parameter points to the output list. In the non-null
    case, the head of r is required to be the successor of the head of x. The predicate is then
    applied recursively to the tails.
       Young et al.                                                                                  7


predicate sll ( loc x ) {
| x == 0 = > { emp }
| not ( x == 0) = > { [x , 2] ** x : - > v ** ( x +1) : - > nxt ** sll ( nxt ) }
}

predicate mapAdd1 ( loc x , loc r ) {
| x == 0 = > { emp }
| not ( x == 0) = > { [x , 2] ** x : - > v ** ( x +1) : - > xNxt ** [r , 2]
    ** r : - > ( v +1) ** ( r +1) : - > rNxt ** mapAdd1 ( xNxt , rNxt ) } }

void mapAdd1_fn ( loc x , loc y )
  { sll ( x ) ** y : - > 0 }
  { y : - > r ** mapAdd1 (x , r ) }
{ ?? }


   Figure 4 Specifying a function that adds one to each element of a singly-linked list in SuSLik.


    Note that inductive predicates are used for two different purposes: the sll inductive
predicate describes a singly-linked list data structure, while the mapAdd1 inductive predicate
describes how the input list relates to the output list. Both are used in the specification of
mapAdd1_fn: sll in the precondition and mapAdd1 in the postcondition.
    Using the mapAdd1 inductive predicate gives us two advantages over attempting to put
the SSL propositions directly into the postcondition of mapAdd1_fn:
 1. We are able to express a conditional on the shape of the list. This is much like pattern
    matching in a language with algebraic data types, but we are examining the pointer
    involved directly.
 2. We are able to express recursion part of the postcondition: the mapAdd1 inductive pre-
    dicate refers to itself in the not (x == 0) branch.
These two features are both reminiscent of features common in functional programming
languages: pattern matching and recursion. However, there are still some significant differ-
ences:

   In traditional pattern matching, the underlying memory representation of the data struc-
   ture is not exposed.
   Compared to a functional programming language, the meaning of the specification is
   more obscured. It is necessary to think about the structure of the linked data structure
   to determine what the specification is saying. This is related to the first point: The
   memory representation is front-and-center.
   In many functional languages, mutation is either restricted or generally discouraged. In
   SuSLik, mutation is commonplace.

  Suppose we want to write the functional program that corresponds to this specification.
One way to do this in a Haskell-like language is by using the List type from Fig. 3.
mapAdd1_fn : List -> List ;
mapAdd1_fn ( Nil ) := 0;
mapAdd1_fn ( Cons head tail ) := Cons ( head + 1) ( mapAdd1_fn tail );

The only missing information is the memory representation of the List data structure. We
do not want the mapAdd1_fn implementation to deal with this directly, however. We want to
8        Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


    separate the more abstract notions of pattern matching and constructors from the concrete
    memory layout that the data structure has.
        To accomplish this, we now extend the code with the definition of Sll from Fig. 3.
    Sll is a layout for the algebraic data type List. Now we have all of the information of
    the original specification but rearranged so that the low-level memory layout is separated
    from the rest of the code. This separation brings us to an important observation about
    the language, manifested throughout these examples: none of the function definitions need
    to directly perform any pointer manipulations. This is relegated entirely to the reusable
    layout definitions for the ADTs. The examples are written entirely as recursive functions
    that pattern match on, and construct, ADTs.
        All that is left is to connect these two parts: the layouts and the function definitions.
    We instruct a SuSLik specification generator to generate a SuSLik specification from the
    mapAdd1_fn function using the Sll layout:
    % generate mapAdd1_fn [ Sll ] Sll

    The [Sll] part of the directive tells the generator which layouts are used for the arguments.
    In this case, the function only has one argument and the Sll layout is used. The Sll at the
    end specifies the layout for the result.


    2.3.1    Synthesising the in-place map function
    We can generalise our mapAdd1 to map arbitrary Int functions over a list and then redefine
    mapAdd1 using the new map.
    % generate mapAdd1 [ Sll ] Sll

    data List := Nil | Cons Int List ;

    Sll : List >-> layout [ x ];
    Sll ( Nil ) := emp ;
    Sll ( Cons head tail ) := x : - > head , ( x +1) : - > tail , Sll tail ;

    map : ( Int -> Int ) -> List -> List ;
    map f ( Nil ) := Nil ;
    map f ( Cons x xs ) := Cons ( instantiate [ Int ] Int f x ) ( map f xs );

    add1 : Int -> Int ;
    add1 x := x + 1;

     mapAdd1 : List -> List ;
     mapAdd1 xs := instantiate [ Int -> Int , Sll ] Sll map add1 xs ;

        The keyword instantiate gives specific layouts to use for the types in function applica-
    tions, e.g., if a function g has type A -> B -> C -> D, then instantiate [L1, L2, L3] L4 g x y z
    will use layout L1 for type A, L2 for type B, L3 for type C and, finally, L4 for the result type
    D, while applying the function g to the three arguments x, y and z.
        This example makes use of instantiate in two places. In the first case where we have the
    call instantiate [Int] Int f x, the builtin Int layout is used for both the input and output.
    In this special case, the Int layout shares a name with the Int type that it represents. This
    is necessary since instantiate is used for all non-recursive calls that are not constructor
    applications.
        Young et al.                                                                             9


predicate filterLt9 ( loc x , loc r ) {
| ( x == 0) = > { r == 0 ; emp }
| not ( x == 0) && head < 9 = >
     { x : - > head ** ( x +1) : - > tail ** [x ,2] ** filterLt9 ( tail , r ) }
| not ( x == 0) && not ( head < 9) = >
     { x : - > head ** ( x +1) : - > tail ** [x ,2] ** filterLt9 ( tail , y )
       ** r : - > head ** ( r +1) : - > y ** [r ,2] } }

void filterLt9 ( loc x1 , loc r )
  { Sll ( x1 ) ** r : - > 0 }
  { filterLt9 ( x1 , r0 ) ** r : - > r0 }
{ ?? }


   Figure 5 SuSLik specification of filterLt9, excluding Sll which is given in Fig. 3


    In the second use, instantiate [Int -> Int, Sll] Sll map add1 xs, we specify that the
second argument uses the Sll layout for the List type from Fig. 3. We also give Sll as the
layout for the result of the call. Note that it is not necessary to use instantiate for the
recursive call to map. This is because the appropriate layout is inferred for recursive calls.
    The type signature of mapAdd1 implies that it is layout polymorphic, as the type does
not refer to any specific layout. It might be surprising that instantiate is required in the
body of mapAdd1 since the type signature of mapAdd1 suggests that it is layout polymorphic
and yet we must pick a specific List layout when we use instantiate to call map. This is
because, in general, a call inside the body of some function fn might use any layout, even
layouts that have no relation to the layouts that fn is instantiated to. Finally, please note
that our benchmarks shown in Figure 18 include a more general version of mapAdd.

2.3.2    Guards
While we have a pattern-matching construct at the top level of a function definition, we
have not seen a way to branch on a Boolean value so far. This is a feature that is readily
available at the level of SuSLik, since the same conditional construct we use to implement
pattern matching can also use other Boolean expressions.
    We can expose this in the functional language using a guard, much like Haskell’s guards.
Suppose we want to write a specialised filter-like function. Specifically, we want a function
that filters out all elements of a list that are less than 9. This is a specific example where
the SuSLik specification is noticeably more difficult to read. For a SuSLik specification of
this example, see Fig. 5
    On the other hand, an implementation of this in Pika is:
% generate filterLt9 [ Sll ] Sll

 filterLt9 : List -> List ;
 filterLt9 ( Nil ) := Nil ;
 filterLt9 ( Cons head tail )
   | head < 9         := filterLt9 tail ;
   | not ( head < 9) := Cons head ( filterLt9 tail );

When translating a guarded function body, the translator takes the conjunction of the
Boolean guard condition with the condition for the pattern match. Finally, please note that
our benchmarks shown in Figure 18 include a more general version of filterLt.
10        Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


        While the SuSLik version of filterLt9 requires working with pointers directly, the Pika
     version uses pattern matching and constructor application. This allows the Pika code to
     work independent of the layout used.

     2.3.3    if-then-else
     Another feature that is common in functional languages is if-then-else expressions. This
     has a straightforward translation into SuSLik. The if-then-else construct corresponds to
     SuSLik’s C-like ternary operator. We can use this feature to implement the even function
     which produces 1 is the argument is even and 0 otherwise.
     % generate even [ Int ] Int

      even : Int -> Int ;
      even ( n ) := if ( n % 2) == 0 then 1 else 0;



     2.3.4    Using multiple layouts
     To show the interaction between multiple algebraic data types, we write a function that
     follows the left branches of a binary tree and collects the values stored in those nodes into
     a list. This example demonstrates a binary tree algebraic data type and a layout that
     corresponds to it.
     % generate leftList [ TreeLayout ] Sll

      data Tree := Leaf | Node Int Tree Tree ;

      TreeLayout : Tree >-> layout [ x ];
      TreeLayout ( Leaf ) := emp ;
      TreeLayout ( Node payload left right ) := x : - > payload , ( x +1) : - > left ,
        ( x +2) : - > right , TreeLayout left , TreeLayout right ;

      leftList : Tree -> List ;
      leftList ( Leaf ) := Nil ;
      leftList ( Node a b c ) := Cons a ( leftList b );



     2.3.5    Synthesising fold
     A fold is a common kind of operation on a data structure in functional programming, where
     a binary function is applied to the elements of a data structure to create a summary value.
     For example, if the binary function is the addition function, it will give the sum of all the
     elements of the data structure. The classic example of such a fold is a fold on a list. In this
     example, we will write a right fold over a List.
     % generate fold_List [ Int , Sll ] Int

      fold_List : Int -> List -> Int ;
      fold_List z ( Nil ) := z ;
      fold_List z ( Cons x xs ) :=
        instantiate [ Int , Int ] Int f x ( fold_List z xs );

     We will specifically look at the specialization where we use the addition function for f so
     that we can focus on way that layouts are used in the translation. This sort of specialization
        Young et al.                                                                                11


corresponds to defunctionalization. The compiler produces the following SuSLik specification
for fold_List:
 predicate fold_List ( int i1 , loc x , int i2 ) {
   | x == 0 = > { i2 == i1 ; emp }
   | not ( x == 0) = > { ( zz4 == i1 ) && (( zz5 == nxt13 ) &&
      ( i2 == ( h + b3 ))) ; [x ,2] ** x : - > h ** ( x + 1) : - > nxt13 **
      fold_List ( zz4 , zz5 , b3 ) } }

   The first two parameters of the SuSLik predicate correspond to the two arguments of the
Pika function. The final parameter of the predicate, i2, corresponds to the output of the
Pika function. There are two cases:

1. The x == 0 case corresponds to the Nil case in Pika. In this case, the pure part of
   the assertion (to the left of the semicolon) requires that the output is equal to the first
   parameter. This is because the Pika function returns the first parameter in its Nil case.
2. The not (x == 0) case corresponds to the Cons case. First, let’s look at the spatial
   part (this is everything to the right of the semicolon). The pattern match destructures
   the Cons into its head and tail. Likewise, in the spatial part of the SuSLik predicate,
   we require that x points to h (the head) and x + 1 points to nxt13 (the tail). We also
   recursively call the predicate on the tail. The pure part does two things: it introduces
   new names for things (these are used internally) and it requires that the output i2 is the
   sum of the head (h) and the value obtained from the output of the recursive call (b3).


 3      Formal Semantics of Pika

In this section, we have the following plan:

     We define abstract machine semantics for executing a subset of Pika programs. This
     semantics is given by the big-step relation 7−→ which we define later.
     We define the translation from that subset of Pika into SSL. This translation is given
     by the function T JeKV,r from Pika expressions into SSL propositions. The r is a variable
     name to be used in the resulting proposition and V is a collection of fresh names.
     We prove a soundness theorem. Given any well-typed expression e and an abstract
     machine reduction producing the store-heap pair (σ ′ , h′ ), the SSL translation of e should
     be satisfied by SSL model (σ ′ , h′ ). This is stated formally, and proven, in Theorem 3.

    This subset of Pika does not have guards or conditional expressions, but it does have
pattern matching. It also has the requirement that functions can only have one argument.
Unlike the implementation, there is no elaboration. As a result, every algebraic data type
value must be lowered to a specific layout at every usage and every function application
must be explicitly instantiated with a layout for the argument and a layout for the result.
We also limit the available integer and Boolean operations for brevity.
    The grammar for this subset is given in Fig. 6. The grammar for types, layout defini-
tions and algebraic data type definitions remain the same as before and are therefore omit-
ted. instA,B (f ) corresponds to instantiate [A] B f. We also include another construct,
lowerA (C e1 · · · en ). This says to use the specific layout A for the given constructor applic-
ation C e1 · · · en .
    The semantics for SSL are largely derived [9] from standard separation logic semantics. [11]
12          Higher-Order Specifications for Deductive Synthesis of Programs with Pointers



     ⟨i⟩ ::= · · · | -2 | -1 | 0 | 1 | 2 | · · ·
     ⟨b⟩ ::= true | false

     ⟨e⟩ ::= ⟨var⟩ | ⟨i⟩ | ⟨b⟩ | ⟨e⟩ + ⟨e⟩ | C ⟨e⟩ | instA,B (f )(⟨e⟩) | lowerA (⟨e⟩)

     ⟨fn-def ⟩ ::= ⟨fn-case⟩
     ⟨fn-case⟩ ::= f ⟨pattern⟩ := ⟨e⟩


         Figure 6 Grammar for restricted Pika subset



     3.1     Overview of the Two Interpretations
     The soundness theorem will link the abstract machine semantics to the translation. In
     fact, the abstract machine semantics and the translation are similar to each other. For
     the abstract machine we manipulate concrete heaps, while for the translation we generate
     symbolic heaps.
         Comparing the two further, there are two main points (beyond what we’ve already men-
     tioned) where these two interpretations of Pika differ:


     1. When we need to unfold a layout, how do we know which layout branch to choose?
     2. How do we translate function applications (including, but not limited to, recursive ap-
        plications)?

         First, consider the abstract machine semantics. In this case, we are able to choose
     which branch of a layout to use by evaluating the expression we are applying it to until the
     expression is reduced to a constructor value (where a “constructor value” is either a value or
     a constructor applied to constructor values). If the expression is well-typed, this will always
     be a constructor of the algebraic data type corresponding to the layout. The two rules that
     this applies to are AM-Lower and AM-Instantiate. To interpret a function application,
     we interpret its arguments and substitute the results into the body of the function. We
     then proceed to interpret the substituted function body. This process is performed by the
     AM-Instantiate rule.
         Next, consider the SSL translation. Here we can determine which layout branch to use
     by generating a Boolean condition that will be true if and only if the SSL proposition on the
     right-hand side of the branch holds for the heap. Note that we assume that the programmer-
     supplied layout definitions are injective functions from algebraic data types to SSL assertions
     (up to bi-implication). We can directly translate function applications into SSL inductive
     predicate applications. Since inductive predicates already allow for recursive applications,
     there is no special handling necessary for recursion.
         After defining these interpretations, we show how the abstract machine relation 7−→ and
     the SSL interpretation function T JeKV,r relate to each other by the Soundness Theorem 3.


     3.2     Abstract Machine Semantics
     In this section, we will define an abstract machine semantics for Pika and relate this to the
     standard semantics for SSL.
        Young et al.                                                                                       13


3.2.1       Notation and Setup
The set of values is Val = Z ∪ B ∪ Loc. Each of these three sets is disjoint from the other
two. In particular, note that Loc and Z are disjoint.
    There is also a set of Pika values FsVal. This includes all the elements of Val, but also
includes “constructor values” given by the rules in Fig. 7. In addition to the store and heap
of standard SSL semantics, the abstract machine semantics uses an FsStore. This is a partial
function from locations to Pika values: FsStore = Loc ⇀ FsVal. The primary purpose of
this is to recover constructor values when given a location.
    The general format of the transition relation is (e, σ, h, F) 7−→ (v, σ ′ , h′ , F ′ , r), where the
expression e results in the store being updated from σ to σ ′ , the heap being updated from h
to h′ , v is the Val obtained by evaluating e, the initial and final FsStore are F and F ′ and
the result is stored in variable r. We assume that there is a global environment Σ which
contains all layout definition equations and function definition equations.
    Given a heap h and a heap layout H, we will make use of the notation h · [H]. This
extends the heap with the location assignments given in H. We say that the layout body
H is acting on the heap h. This is defined in Fig. 9. The intuition for this is that h gets
updated using the symbolic heap description in H. For example, ∅ · [a :-> 7] will contain
only the value 7 at the location a. It is assumed that H does not have any variables on the
right-hand side of :->.


3.2.2       Abstract Machine Rules
The abstract machine semantics provides big-step operational semantics for evaluating Pika
expressions on a heap machine. Its rules, given by Fig. 8, make use of standard SSL models:


    Model                                          M ::= (σ, h)
    Store                                        σ : Var ⇀ Val
    Heap                                         h : Loc ⇀ Val



Note that a compound expression, consisting of multiple subexpressions, uses disjoint parts
of the heap for each subexpression. This can be seen in the AM-Add, AM-Lower and
AM-Instantiate rules, which is essential for the proof of Soundness Theorem 3.


3.3     Translating Pika Specifications into SSL
We will define two translations: One from Pika expressions into SSL propositions and the
other from Pika definitions into SSL inductive predicate definitions. We start with the
former.


3.3.1       Translating Expressions
In the rules given in Fig. 10, the notation IA,B (f ) gives the name of the inductive predicate
that the Pika function f translates to when it is instantiated to the layouts A and B.
    We start by defining the translation rules for expressions. We use these translation
rules in Lemma 1 to define a translation function T J·KV,r . Then, we will define translation
rules for function definitions. The translation relation for expressions has the form (e, V ) ⇓
14      Higher-Order Specifications for Deductive Synthesis of Programs with Pointers



        x ∈ Val                          x1 ∈ FsVal · · · xn ∈ FsVal
                 FsVal-Base                                           FsVal-Constr
       x ∈ FsVal                             (C x1 · · · xn ) ∈ FsVal


      Figure 7 FsVal judgment rules

     r fresh i ∈ Z σ ′ = σ ∪ {(r, i)}             r fresh b ∈ B σ ′ = σ ∪ {(r, b)}
                                           AM-Int                                       AM-Bool
       (i, σ, ∅, F) 7−→ (i, σ ′ , ∅, F, r)          (b, σ, ∅, F) 7−→ (b, σ ′ , ∅, F, r)

                                    v ∈ dom(σ) σ(v) ̸∈ Loc
                                                                   AM-Var-Base
                               (v, σ, ∅, F) 7−→ (σ(v), σ, ∅, F, v)

                                    v ∈ dom(σ) σ(v) ∈ Loc
                                                                    AM-Var-Loc
                             (v, σ, ∅, F) 7−→ (F(σ(v)), σ, ∅, F, v)

         (x, σ, F, h1 ) 7−→ (x′ , σx , h′1 , F, vx )       (y, σx , F, h2 ) 7−→ (y ′ , σy , h′2 , F, vy )
          r fresh h = h1 ◦ h2             h′ = h′1 ◦ h′2      z = x′ + y ′     σ ′ = σy ∪ {(r, z)}
                                                                                                            AM-Add
                                  (x + y, σ, h, F) 7−→ (z, σ ′ , h′ , F, r)

        (A[x] (C a1 · · · an ) := H) ∈ Σ        (e, σ0 , h0 ) 7−→ (C e1 · · · en , σ1 , h1 , y1 )
                   (ei , σi , hi ) 7−→ (ei , σi+1 , h′i , vi ) for each 1 ≤ i ≤ n
                                         ′

         h′ = h′1 ◦ h′2 ◦ · · · ◦ h′n h = h0 ◦ h1 ◦ · · · ◦ hn σ ′ = σn+1 ∪ {(r, ℓ)}
                                             ℓ fresh r fresh
                 ′
            H = H[x := ℓ][a1 := σ2 (v1 )][a2 := σ3 (v2 )] · · · [an := σn+1 (vn )]
                                    F ′ = F ∪ {(ℓ, (C e′1 · · · e′n ))}
                                                                                                       AM-Lower
                 (lowerA (e), σ0 , h, F) 7−→ ((C e′1 · · · e′n ), σ ′ , h′ · [H ′ ], F ′ , r)

                     (A[x] (C a) := H) ∈ Σ             (f (C b) := ef ) ∈ Σ
                                (e, σ, h) 7−→ (C e1 , σ1 , h1 , y)
                                (e1 , σ1 , h1 ) 7−→ (e′1 , σ2 , h2 , r)
                                   ℓ fresh r fresh y fresh
           H = H[x := ℓ][a := e′1 ] h′ = h1 · [H ′ ] σ ′ = σf ∪ {(r, ℓ)}
             ′

                                    F ′ = F ∪ {(ℓ, (C e′1 ))}
                     (lowerB (ef [b := y]), σ2 , h′ ) 7−→ (e′f , σf , h′′ , r)
                                                                                            AM-Instantiate
                     (instA,B (f )(e), σ, F, h) 7−→ (e′f , σ ′ , h′′ , F ′ , r)

      Figure 8 Abstract machine semantics rules



                                         h′ = h · [H] a ∈ Val
                          L-Emp                                      L-PointsTo
       h · [emp] = h                  h · [ℓ :-> a, H] = h′ [ℓ 7→ a]

                                    e ∈ Val
                                                      L-Apply
                           h · [A[x](e), H] = h · [H]


      Figure 9 Rules for layout bodies acting on heaps
        Young et al.                                                                                   15


(p, s, V ′ , v), where p and s are the pure part and spatial part (respectively) of an SSL assertion
and V, V ′ ∈ P(Var).
     The rules can be thought of as being in two groups:

1. Rules for base type expressions, such as S-Lit and S-Add.
2. Rules for using layouts to translate expressions whose types involve algebraic data types.
   Examples include S-Lower-Constr and S-Inst-Inst.

    In the first group, consider S-Add. In the result of the translation, we’ve included
v == v1 + v2 in the list of conjuncts in the pure part. Here, v1 and v2 are the results of the
two subexpressions in the addition. In the pure part, we also include the pure parts of the
two subexpressions as conjuncts. These are p1 and p2 . The spatial part of the translation
consists of the spatial parts of the two subexpressions, s1 and s2 .
    Now, in the second group, consider S-Lower-Constr. This translates a Pika con-
structor application expression using a specific layout (which is provided by using the
lower− (−) construct). It takes the specific branch of the layout corresponding to the con-
structor in question and puts the right-hand side of that branch into the spatial part, after
applying the appropriate substitutions for the arguments given to the constructor in the
application. The right-hand side of the layout branch is H and, after the substitution, it is
called H ′ .
    The S-Inst-Inst rule is used to translate a function application being applied to the
result of another function application, given particular layouts for each application. In
SuSLik, it does not make sense to directly apply a predicate to another predicate application.
Therefore, we must do an ANF-like translation, where the result does not have “compound”
applications like this. This translation is exactly what S-Inst-Inst is doing.

▶ Lemma 1 (T J·K function). (·, V ) ⇓ (·, ·, ·, r) is a computable function Expr → (Pure ×
Spatial × P(Var)), given fixed V and r where r ̸∈ V .
   By throwing away the third element of the tuple in the codomain, we obtain a function
Expr → (Pure × Spatial) from expressions to SSL propositions.
   Call this function T J·KV,r . That is, we define the function as follows where r ̸∈ V :

    T JeKV,r = (p; s) ⇐⇒ (e, V ) ⇓ (p, s, V ′ , r) for some V ′

    We highlight the computability of this function to emphasise the fact that it can be used
directly in an implementation of this subset of Pika.

3.3.2     Translating Function Definitions
The next step is to define the translation for Pika function definitions. In order to do this, we
must first figure out how to determine the appropriate layout branch to use when unfolding
a layout, a problem we highlighted earlier. Once this is accomplished, the rest of the trans-
lation can be defined. When this problem was solved for the abstract machine semantics, it
was possible to simply evaluate the Pika expression until a constructor application expres-
sion was reached. From there, it is possible to just look at the constructor name and match
it against the appropriate layout branch.
    For the translation, however, we do not have the luxury of being able to evaluate expres-
sions. Instead, we must instead rely on the fact that, in SSL, a “pure” (Boolean) condition
can determine which inductive predicate branch to use. The question becomes: Given an
algebraic data type and a layout for that ADT, how do we generate an appropriate Boolean
condition for a given constructor for the ADT ?
16      Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


                                                   i ∈ Z v fresh
                                                                            S-Int
                                        (i, V ) ⇓ (v == i, emp, V ∪ {v}, v)

                                                 b ∈ B v fresh
                                                                          S-Bool
                                      (b, V ) ⇓ (v == b, emp, V ∪ {v}, v)

                                                      v ∈ Var
                                                                        S-Var
                                            (v, V ) ⇓ (true, emp, V, v)

                  (e1 , V0 ) ⇓ (p1 , s2 , V1 , v1 ) (e2 , V1 ) ⇓ (p2 , s2 , V2 , v2 ) v fresh
                                                                                              S-Add
                  (e1 + e2 , V0 ) ⇓ (v == v1 + v2 ∧ p1 ∧ p2 , s1 ∗ s2 , V2 ∪ {v}, v)

                                                        v ∈ Var
                                                                                    S-Lower-Var
                            (lowerA (v), V ) ⇓ (true, A(v), V ∪ {v}, v)

                                 (A[x] (C a1 · · · an ) := H) ∈ Σ
                       (ei , Vi ) ⇓ (pi , si , Vi+1 , vi ) for each 1 ≤ i ≤ n
                                                 v fresh
                   ′                            ′
                V = Vn+1 ∪ {x}              H = H[a1 := v1 ] · · · [an := vn ]
                                                                                             S-Lower-Constr
      (lowerA (C e1 · · · en ), V1 ) ⇓ (p1 ∧ · · · ∧ pn , H ′ ∗ s1 ∗ · · · ∗ sn , V ′ , x)

                                       v ∈ V r fresh
                                                                              S-Inst-Var
                  (instA,B (f )(v), V ) ⇓ (true, IA,B (f )(v, r), V ∪ {r}, r)

                                   (A[x] (C a1 · · · an ) := H) ∈ Σ
                           (ei , Vi ) ⇓ (pi , si , Vi+1 , vi ) for each 1 ≤ i ≤ n
                                                    x fresh
                       ′                            ′
                  V = Vn+1 ∪ {x}                H = H[a1 := v1 ] · · · [an := vn ]
             (f (C b1 · · · bn ) := ef ) ∈ Σ e′f = ef [b1 := v1 ] · · · [bn := vn ]
                                 (lowerB (e′f ), Vn+1 ) ⇓ (p, s, V ′ , r)
                                                                                                   S-Inst-Constr
     (instA,B (f )(C e1 · · · en ), V1 ) ⇓ (p ∧ p1 ∧ · · · ∧ pn , s ∗ s1 ∗ · · · ∗ sn , V ′ , r)

                                  (instA,B (g)(e), V ) ⇓ (p1 , s1 , V1 , r1 )
                                 (instB,C (f )(r1 ), V1 ) ⇓ (p2 , s2 , V2 , r2 )
                                                                                             S-Inst-Inst
               (instB,C (f )(instA,B (g)(e)), V ) ⇓ (p1 ∧ p2 , s1 ∗ s2 , V2 , r2 )

     Figure 10 Expression Translation Rules




        V = {v1 , · · · , vn } where v1 , · · · , vn are distinct variables
            r ∈ Var r ̸∈ V             c = cond(A, C, x) p1 · · · pn fresh
                       (p, s) = T JinstA,B (f )(C p1 · · · pn )KV,r
                                       fn-def
                                                                                       FnDef
       (f (C a1 · · · an ) := e) 7−−−→A,B (IA,B (f )(x, r) : c ⇒ {p; s})


     Figure 11 Translation rule for function definitions
        Young et al.                                                                                             17




    The solution is to find a Boolean condition which, given that the inductive predicate
holds, is true if and only if the layout branch corresponding to that ADT constructor is
satisfiable. In more detail, to define the branches of an inductive predicate IA (x), given an
ADT α, a constructor C : β1 → β2 → · · · → βn → α, a layout A : α ↣ layout[x] with
a branch A[x] (C a1 · · · an ) := H and given that IA (x) holds, find a Boolean expression b
with one free variable x such that b ⇐⇒ ∃σ, h. (σ, h) |= H.

▶ Lemma 2 (cond function). There is a computable function cond(·, ·) that takes in any
layout A : α ↣ layout[x] with a branch A[x] (C a1 · · · an ) := H for a given constructor
C : β1 → β2 → · · · → βn → α and it produces a Boolean expression with one free variable x
such that the following holds under the assumption that IA (x) holds.

    cond(A, C) ⇐⇒ ∃σ, h. (σ, h) |= H

Here, IA (x) is the name of the generated inductive predicate corresponding to the layout A.

    With this function in hand, we are now ready to define the translation for Pika function
definitions. This definition is in Fig. 11. In this rule, the fresh variables p1 , · · · , pn will be
substituted for a1 , · · · , an .


3.4     Typing Rules
Typing rules for Pika expressions are given in Fig. 12. These rules differ from standard
typing rules for a functional language due to the existence of layouts and their associated
constructors, like instantiate and lower. If an expression is well-typed, then each use of
instantiate and lower only uses layouts together with the ADT that they are defined for.
    The rules also make use of a concreteness judgment. The rules for this judgment are
given in Fig. 13a. The intuition of this judgment is that a type is “concrete” iff values of
that type can be directly represented in the heap machine semantics. For example, an ADT
type is not concrete because a layout has not been specified. However, once a particular
layout is specified for the ADT type, it becomes concrete. Base types, like Int, are also
concrete.
    Rules for the ensuring that global definitions are well-typed are given in Fig. 13b. In this
figure, ∆ is the set of all (global) constructor type definitions.


3.5     From Pika to SLL Specifications: Soundness of the Translation
We want to show that our abstract machine semantics and our SSL translation fit together.
In particular, our abstract machine semantics should generate models that satisfy the separ-
ation logic propositions given by our SSL translation. Figure 14 gives a high-level overview
of how these pieces fit together. We will give a more specific description of this in Theorem 3.

▶ Theorem 3 (Soundness). For any well-typed expression e, if T JeKV,r is satisfiable for
V = dom(σ ′ ) and (e, σ, h, F) 7−→ (e′ , σ ′ , h′ , F ′ , r), then (σ ′ , h′ ) |= T JeKV,r . That is, given an
expression e with a satisfiable SSL translation, any heap machine state that e transitions to
(by the abstract machine semantics) will be a model for the SSL translation of e (cf. Fig. 14).

Proof. See the Appendices in the extended version of the paper.                                            ◀
18         Higher-Order Specifications for Deductive Synthesis of Programs with Pointers



                      i∈Z                b∈B              (v : α) ∈ Γ
                                T-Int              T-Bool             T-Var
                    Γ ⊢ i : Int       Γ ⊢ b : Bool         Γ⊢v:α

                                      (f : α → β) ∈ Σ
                                                      T-Fn-Global
                                       Γ⊢f :α→β

                                      Γ ⊢ x : Int Γ ⊢ y : Int
                                                              T-Add
                                          Γ ⊢ x + y : Int

                         (v : α) ∈ Γ (A : α ↣ layout[x]) ∈ Σ
                                                             T-Lower-Var
                                   Γ ⊢ lowerA (v) : A

           (C : α1 → · · · → αn → β) ∈ Σ         (B : β ↣ layout[x]) ∈ Σ
                    Γ ⊢ ei concreteαi for each i with 1 ≤ i ≤ n
                                                                                  T-Lower-Constr
                             Γ ⊢ lowerA (C e1 · · · en ) : B

                 (A : α ↣ layout[x]) ∈ Σ         (B : β ↣ layout[y]) ∈ Σ
                                 Γ⊢f :α→β           Γ⊢e:A
                                                                                 T-Instantiate
                                  Γ ⊢ instA,B (f )(e) : B

          (C : α1 → · · · → αn → β) ∈ Σ Γ ⊢ ei : αi for each i with 1 ≤ i ≤ n
                                                                              T-Constr
                                   Γ ⊢ C e 1 · · · en : β


         Figure 12 Typing rules



         The fact that, at the top level, we only translate function definitions suggests an addi-
     tional theorem. We want to specifically show that any possible function application is sound,
     in the sense just described. This immediately follows from Theorem 3.
         Abbreviating instA,B (f ) as fA,B , we can state the following theorem:


     ▶ Theorem 4 (Application soundness). For any well-typed function application fA,B (e), if
     T JfA,B (e)KV,r is satisfiable for V = dom(σ ′ ) and (fA,B (e), σ, h, F) 7−→ (e′ , σ ′ , h′ , F ′ , r), then
     (σ ′ , h′ ) |= T JfA,B (e)KV,r .


     Proof. This follows immediately from Theorem 3.                                                                ◀



          Γ ⊢ e : Int            Γ ⊢ e : Bool
         e concreteInt C-Int    e concreteBool C-Bool
                                                                 (C : α1 → α2 → · · · → αn → β) ∈ ∆
       (A : α ↣ layout[x]) ∈ Σ     Γ⊢e:A                         b1 : α1 , b2 : α2 , · · · , bn : αn ⊢ e : γ
                                              C-Layout                                                       G-Fn
                  e concreteα                                     (f (C b1 · · · bn ) := e) ⇒ f : β → γ
     (a) Concreteness judgment rules                       (b) Global definition typing

         Figure 13 Rules for concreteness judgement and typing global definitions
        Young et al.                                                                              19
                                                             Pika                                      SSL pro




                                            |=
                                            interpretation
                                            translation      Abstract machine semantics




     Figure 14 The relationship between the two Pika semantics given by the soundness theorem


 4      Extensions of SuSLik
We have shown the translation from the functional specifications into SSL specifications.
However, some of the SSL specifications are not supported in the original SuSLik and existing
variants. In this section, we show how to extend the SuSLik to support more features to
make the whole thing work. We will show the extensions on the following three aspects:

     How to describe and call an existing function within SSL predicates.
     How to make the result of one function call as the input of another function call.
     How to synthesise programs with inductive predicates without the help of pure theory.

4.1     Function Predicates
Without any modification upon the implementation, we find the SSL predicate with some
restrictions can be used to describe function relations other than data structures (named
function predicates). The definition of function predicates is as follows:

▶ Definition 5 (Function Predicates). Given any non-higher-order n-ary function f (x1, ..., xn)
in the functional language, the function predicate to synthesise f has the following format:
      predicate predf(T x1, ... ,T xn, T output){...}

where T ∈ {loc, int}. The type of xi (and output) is decided by the type of f . If it is an
integer in f , then its type is int; otherwise, it is loc (for any data structure in Pika).

    Since the input of the whole workflow is functional programs, the “output” in the defin-
ition is to provide another location for the output of the function. And the specification to
synthesise function f should have the following format:
void f(loc x1, ... ,loc xn)
{x1 :-> v1 ** x2 :-> l2 ** sll(l2) ** ... ** xn :-> vn ** output :-> 0}
{x1 :-> v1 ** x2 :-> l2 ** ... ** xn :-> vn ** output :-> output0 **
 predf(v1, l2, ..., vn, output0)}



4.2     SSL Rules for func Structure
As we show in previous examples, the reason we can have func structure is that the points-to
structure in the post-condition is always eliminated after write operations. For example, the
in-placed inc1 functions specification is satisfied via the Write (Fig. 15) on the location.
void inc_y(loc y, loc x)
{x :-> vx ** y :-> vy}
{x :-> vx + vy ** y :-> vy}
20         Higher-Order Specifications for Deductive Synthesis of Programs with Pointers



                     Write
                     Vars (e) ⊆ Γ         e ̸= e′       {ϕ; x 7→ e ∗ P} ⇝ {ψ; x 7→ e ∗ Q}| c
                                            ′
                                {ϕ; x 7→ e ∗ P} ⇝ {ψ; x 7→ e ∗ Q}| ∗x = e ; c


                  Funcwrite
                              ∀i ∈ [1, n], Vars (ei ) ⊆ Γ          {ϕ; P} ⇝ {ψ; Q}| c
                   {ϕ; x 7→ e ∗ P} ⇝ {ψ; func f(e1 , . . . , en , x) ∗ Q}| f(e1 , . . . , en , x) ; c

        Figure 15 The Write and new Funcwrite rules in SSL


         The core insight of func structure is: since the function synthesised by function predicate
     behaves like the pure function, it is the same as the Write rule in the sense that only the
     output location is modified. Thus, we add the new Funcwrite rule into the zoo of SSL
     rules (see Fig. 15). To make the func structure correctly equal to some “write” operation,
     the following restrictions should hold, which are achieved by the translation:

        If func f(x1, ..., xn, output) appears in a post-condition, then no write rule can be
        applied to any xi. This is to avoid the ambiguity of the func.
        The type of function f is consistent.

         Note that based on the setting of the function predicate, the parameters of the function
     call are pointers, while the parameters of the function predicate are content to which pointers
     point. Furthermore, we have the func generated from function predicates and with the
     format defined in Sec. 4.1. As a result, the equivalent original SSL that duplicates points-to
     of one location is not a problem, since they can be merged as one.

     4.3    Temporary Location for the Sequential Application
     Though richly expressive, SSL has difficulty in expressing the sequential application of func-
     tions. For example, given the func structure available, the following function is not express-
     ible within one function predicate:
     f x y = g (h x) y

        If we attempt to express it, we will have the following part in the predicate:
     predicate f(loc x, loc y, loc output)
     {... ** func h(x, houtput) ** func g(houtput, y, output)}

        However, houtput is not a location in the pre-condition, which is not allowed in SSL.
     Thus, we introduce a new keyword temp to denote the temporary location for the sequential
     application. The new definition of func is as follows:
     predicate f(loc x, loc y, loc output)
     {... ** temp houtput ** func h(x, houtput) ** func g(houtput, y, output)}

         Roughly speaking, the temp structure will help to allocate a new location for the output of
     the first function, and then use it as the input of the second function. After all appearances
     of houtput is eliminated, we will deallocate the location.
         Note that the temporary variable is possible to appear in two different structures: re-
     cursive function predicates or func call. The reason we don’t need to consider the basic
     arithmetic operations is that the integer will be directly used as the predicate parameter,
       Young et al.                                                                                   21



         Tempfuncalloc
                {ϕ; x 7→ a ∗ P} ⇝ {ψ; func f (e1 , . . . , en , x) ∗ temp(x, 1) ∗ Q}| c
         {ϕ; P} ⇝ {ψ; func f(e1 , . . . , en , x) ∗ temp(x, 0) ∗ Q}| let x = malloc(1) ; c


 Tempfuncfree
                                         {ϕ; P} ⇝ {ψ; Q}| c
  ̸ ∃x ∈ Q ∧ {ϕ; P} ⇝ {ψ; temp(x, 1) ∗ Q}|        let x0 = ∗x ; type_free(x0); free(x); c

   Figure 16 New allocating and deallocating rule for temp in SSL


instead of the location as the parameter. For example, the sum of a list can be expressed
as:
predicate sum(loc l, int output){
| l == 0 => {output == 0; emp}
| l != 0 => {output == output1 + v; [l, 2] ** l :-> v ** l + 1 :-> lnxt **
    sum(lnxt, output1)} }

   Such sequential application is common in functional programming, especially in the re-
cursive function. For example, it is not elegant to flatten a list of lists without the sequential
application.
     flatten :: [[a]] -> [a]
     flatten [] = []
     flatten (x:xs) = x ++ flatten xs

    We can express this function, but with some strange structure to store all temporary
lists.
predicate flatten(loc x, loc output){
| x == 0 => {output :-> 0}
| x != 0 => {[x, 2] ** x :-> x0 ** sll(x0) ** x + 1 :-> xnxt **
[output, 2] ** func append(x, outputnxt, output) ** output + 1 :-> outputnxt **
flatten(xnxt, outputnxt)} }

    With such a function predicate, though we can synthesise the function whose result
stored in output is the flattened list, the list output is containing a lot of intermediate values,
which is neither consistent with the definition in the source language nor space efficient.
    The new rules consist of allocating and deallocating rules (Fig. 16). Based on the defin-
ition of the func structure and the function predicate, the allocated locations are different,
where the temp location for func is directly used; while the temp location for function predic-
ate should allocate a new location for function predicates. As for the deallocation, not only
the temp location(s) but also the content they point to should be deallocated. That is the
reason we have the type_free function, which is syntax sugar to deallocate the content of
a location based on the type information. For example, if the type of the location is tree,
then the type_free will deallocate the content of the location via tree_free function, which
is synthesised based on the SSL predicate tree as follows.
void tree_free(loc x)
  {tree(x)}
  {emp}

Specifically, if the location contains the value with type int, then the type_free will do
nothing. Thus, the function predicate with temp is much better, in the sense that no extra
space is used, and the synthesised function is consistent with the source language.
22          Higher-Order Specifications for Deductive Synthesis of Programs with Pointers



     predicate flatten(loc x, loc output){
     | x == 0 => {output :-> 0}
     | x != 0 => {[x, 2] ** x :-> x0 ** sll(x0) ** x + 1 :-> xnxt ** temp outputnxt
       ** flatten(xnxt, outputnxt) ** func append(x, outputnxt, output)} }



     4.4     Avoiding Excessive Heap Manipulation with Read-Only Locations
     The existing SuSLik depends on the set theory to express the pure relation. However, it is
     not trivial to automatically generate the pure part of SSL specifications from the functional
     specifications. To see why the set theory is needed, the following simple example shows the
     functionality of the set theory, with sll_n being the single-linked list with no set.
     predicate sll_n(loc x) {
     | x == 0         => {true; emp }
     | not (x == 0) => { [x, 2] ** x :-> v ** (x + 1) :-> xnxt ** sll(xnxt) } }
     predicate copy(loc x, loc y) {
     | x == 0         => {y == 0; emp }
     | not (x == 0) => { [y, 2] ** y :-> v ** (y + 1) :-> ynxt ** [x, 2] ** x :-> v
          ** (x + 1) :-> xnxt ** copy(xnxt, ynxt) } }

        While the intent of the function predicate copy is to copy the list x to y, without the set
     theory, the output program will be somewhat surprising to see:
     {sll_n(x)}
     void copy (loc x, loc y) {
       if (x == 0) {
       } else {
         let n = *(x + 1); copy(n, y); let y01 = *y; let y0 = malloc(2); *y = y0;
         *(y0 + 1) = y01; let vy = *y0 *x = vy; } }
     {copy(x, y)}

         The problem here is that, when we have the pure relation in the predicate to indicate
     that the values are the same, the synthesiser finds another possible way: instead of copying
     the value of x to y, we can just change the value of x to initial value vy after malloc. This
     is not the user intent, and the output program is not correct. Turns out, the solution is not
     that difficult: we simply need add a new kind of heaplet in the specification language, call
     constant points-to, which has a similar idea as read-only borrows [2]. The only difference of
     the constant points-to from the original points-to heaplet is that the value of the location
     is constant, which means that the Write rule in SSL is not applicable. By this way, the
     extended SuSLik will not consider the modification of the input location, thus provides the
     correctness mechanism (in Sec. 3.5) for the translation of Pika.


      5      Evaluation
     In this section, we evaluate Pika’s expressiveness. A secondary objective is to evaluate
     Pika’s performance. The performance evaluation is done largely to put Pika into context by
     comparing it to a prominent functional programming language (Haskell). The main purpose
     of Pika is to increase the expressiveness of SuSLik, which is the reason for the primary
     evaluation objective. Towards these goals, we answer the following research questions:

          RQ1: Is the performance of the synthesised code competitive with code generated from
          traditional functional language compilers?
          RQ2: In concrete terms, how does the tool’s expressivity compare with the expressivity
          of SuSLik specifications for programs written in a functional style?
          RQ3: What are the failure modes of our approach?
                             Young et al.                                                                                                                                             23




                                C -O0                                                                                     C -O3
                                Haskell -O0                                                                        40     Haskell -O2
                       200


                                                                                                                   30
 Execution time (ms)




                                                                                             Execution time (ms)
                       150



                       100                                                                                         20



                       50                                                                                          10



                        0                                                                                          0
                              sum      filterLt   mapAdd       take   leftList   treeSize                               sum      filterLt   mapAdd       take   leftList   treeSize
                                                     Test cases                                                                                Test cases

(a) Benchmarks without optimizations                                                        (b) Benchmarks with optimizations


                  Figure 17 Performance of C functions generated by Pika compared to Haskell/GHC


    Our implementation and benchmarks are available in supplementary material. The ex-
periments were conducted on a 2021 MacBook Pro with an M1 processor and 32 GB of
RAM. We used GHC version 9.8.1 and Apple Clang version 13.0.0.
    For RQ1, we run benchmarks and compare execution time. The benchmarks we selected
are a series of functions that manipulate data structures such as lists and trees, which covers
different common abstract operations (like map, filter, fold). The comparison is between
Haskell functions based on user-defined data structures and C functions generated from
Pika’s specifications (via the extended SuSLik), parameterised with the data structures of
large size. We recorded both execution time with and without optimisation of compilers.
    The results are shown in Fig. 17. Our findings are as follows:

                  When compiled to an executable run without optimisations, the C programs generated by
                  Pika are faster than Haskell programs. And we can also observe that the speed difference
                  is larger for functions with more complex data structures.
                  When compiled to an executable with optimisations:

                             For functions with complex data structures, the comparison is similar to the case
                             without optimisation.
                             For functions for the singly-linked list GHC’s optimisation is very powerful, resulting
                             in much better performance than C programs generated by Pika. With more tests,
                             we found out the performance after GHC’s optimisation is similar to the one using
                             Haskell’s built-in list. We believe this is because GHC’s optimisations are fine-tuned
                             to optimise code manipulating list-like data structures and use the same optimisation
                             as for Haskell’s built-in list. That said, similar observations regarding GHC do not
                             hold on other complex data structures, such as trees.

   To answer RQ2, we first find some common patterns for Pika programs in the bench-
marks shown in Fig. 18: (1) pattern matching on ADTs (#9, 10, etc.), (2) code reusability
(#3 vs 5, #7 vs 8). Those features are not directly expressible in SuSLik because of the
low-level nature of SSL. For example, the add1Head and add1HeadDLL functions share the
same function definition, where the only difference is the type layout used; but the SuSLik
specifications need to be treated separately, which makes the codes more complex. To make
24          Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


                                                        |Pika AST|
            #   Task Name     Pika AST SuSLik AST      |SuSLik AST|
                                                                      Compile Time Synthesis Time

            1     cons            76         123         0.618           0.012          5.134
            2     plus            46          91         0.505           0.002          5.992
            3  add1Head           64         109         0.587           0.006          5.114
            4   listId            62         107         0.579           0.005          4.906
            5 add1HeadDLL         74         146         0.507           0.007         10.618
            6     even            19          42         0.452           0.001          3.999
            7    foldr            63         113         0.558           0.005          5.454
            8     sum             58         103         0.563           0.004          5.125
            9  filterLt           84         147         0.571           0.009          6.104
            10  mapAdd            71         116         0.612           0.007          5.031
            11 leftList          116         156         0.744           0.008          7.722
            12 treeSize           78         126         0.619           0.007          5.980
            13    take           119         212         0.561           0.012         10.447


        Figure 18 Statistics on the benchmarks: Pika spec size v, generated SSL spec size, translator
     performance, and synthesiser performance. All times are in seconds.

      selfAppend : List -> List ;
      selfAppend xs := instantiate [ Sll , Sll ] Sll append xs xs ;

     append : List -> List -> List ;
     append ( Nil ) ys := ys ;
     append ( Cons x xs ) ys := instantiate [ Int , Sll [ mutable ]] Sll cons
                                               ( addr x ) ( append xs ys );


          Figure 19 A Pika specification not supported by SuSLik.


     some objective observations on the expressivity, we measure the number of nodes in the in-
     put Pika AST and find it consistently fewer than the number of AST nodes in the generated
     SuSLik specification.
         To address RQ3, note that a particular failure mode occurs when Pika source code
     reuses a variable in a way that the constraints violate separation logic. For example, see the
     selfAppend example in Fig. 19 which uses its argument twice. We could have addressed
     this issue by introducing a lightweight linear type system to Pika, but have not carried
     out this exercise yet. Another kind of failure occurs when SuSLik fails to synthesise an
     implementation of the generated specification: handling these failures is beyond the scope
     of this work.

      6      Discussion
     We have given a translation from a high-level functional language into SSL specifications to
     be given to a program synthesiser.
        In doing so, we have revealed a close connection between, on one hand, algebraic data
     types and recursive pattern-matching functions and, on the other hand, SSL inductive pre-
     dicates. The soundness of this connection is demonstrated by Theorem 3 in Sec. 3.
        Beyond the theory, this connection can be exploited in three directions:
        Young et al.                                                                               25


     Increased type safety: Algebraic data types allow you to distinguish between types that
     have the same runtime heap representation.
     More reusability: An algebraic data type can have multiple layouts, each of which gives a
     different possible runtime heap representation for the ADT. As Pika functions are defined
     only in terms of algebraic data types, they naturally get the polymorphism of the ADT
     by being able to work with any layout of the ADT.
     Greater succinctness: When working at this higher level of abstraction, it generally takes
     less code as you are not frequently manipulating heap locations. The only mention of
     heap locations is in reusable layout definitions. This can also give greater clarity.

 7      Related Work
Pika is built upon the SuSLik synthesis framework. SuSLik provides a synthesis mechanism
for heap-manipulating programs using a variant of Separation Logic [9]. However, it does not
have any high-level abstractions. In particular, writing SuSLik specifications directly involves
a significant amount of pointer manipulation. Further, it does not provide abstraction over
specific memory layouts. As described in Sec. 2.2, Pika addresses these limitations.
    Dargent language [1] also includes a notion of layouts and layout polymorphism for a
class of algebraic data types, which differs from our treatment of layouts in two primary
ways:
1. In Pika, abstract memory locations (with offsets) are used. In contrast, Dargent uses
   offsets that are all relative to a single “beginning” memory location. The Pika approach
   is more amenable to heap allocation, though this requires a separate memory manager
   of some kind. This is exposed in the generated language with malloc and free. On
   the other hand, the technique taken by Dargent allows for greater control over memory
   management. This makes dealing with memory more complex for the programmer, but
   it is no longer necessary to have a separate memory manager.
2. Algebraic data types in the present language include recursive types and, as a result, Pika
   has recursive layouts for these ADTs. This feature is not currently available in Dargent.
    Furthermore, layout polymorphism also works differently. While Dargent tracks layout
instantiations at a type-level with type variables, in the present work we simply only check
to see if a layout is valid for a given type when type-checking. In particular, we cannot
write type signatures that require the same layout in multiple parts of the type (for instance,
in a function type List -> List we have no way at the type-level of requiring that the
argument List layout and the result List layout are the same). This more rudimentary
approach that Pika currently takes could be extended in future work. Overall, the examples
in the Dargent paper tend to focus on the manipulation of integer values. In contrast, we
have focused largely on data structure manipulation, which follow the primary motivation
of SuSLik.
    Synquid is another synthesis framework with a functional surface language. While Synquid
allows an even higher-level program specification than Pika through its liquid types, it does
not provide any access to low-level data structure representation. [8] In contrast, Pika’s level
of abstraction is similar to that of a traditional functional language but, similar to Dargent,
it also allows control over the data structure representation in memory.

 8      Future Work and Conclusion
We make the following observations based on our experience of developing and using Pika.
26        Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


         By allowing layouts to use multiple SSL parameters, we would be able to give a greater
     variety of layouts associated with an ADT. For instance, the List data type used in the
     examples could have a doubly-linked list layout in addition to the singly-linked list layout
     Sll. Note that any existing Pika function defined over List will continue to work with no
     modification with these new layouts. Defunctionalisation and lambda lifting can also be
     used to implement true higher-order functions.
         It is possible to do inference of some layouts, for example in mapAdd1 we would usually
     want to use the same layout as the argument layout, but we leave this for future work.
     Another approach is to introduce type variables that correspond to layouts, as done in the
     series of works on the Dargent tool [1]. We leave this approach for future work as well.
         Reverse transformation deserves further investigation: if we go from an SSL specification
     to Pika program and then compile to, e.g., C, can we synthesise additional programs that
     traditional SSL synthesisers would struggle with? What are the limitations of this approach?
         We may be able to expose more of the synthesis mechanism in the Pika language. For
     example, generate an SSL specification given only a Pika type signature (and corresponding
     %generate directive). This could combine well with additional polymorphism, as we could
     utilise the free theorems that are given by a polymorphic type signature to further constrain
     the resulting specification.
         Finally, is it possible to derive translations for languages such as Pika from abstract
     machine semantics? In this paper, we have given a language with abstract machine semantics.
     We then give a translation of that language into SSL. We then show that the final states
     given by the abstract machine semantics are models for the SSL propositions produced by
     our translation. But is it possible to begin by specifying the abstract machine semantics and
     then mathematically (or automatically) derive an appropriate translation into SSL, with the
     requirement that the translation satisfies the soundness theorem?
         In conclusion, we have presented Pika: a high-level functional specification language that
     paves the way for the efficient synthesis of a verifiably correct imperative code with in-place
     memory updates that is comparable in efficiency to the handwritten C.


          References
      1   Zilin Chen, Ambroise Lafont, Liam O’Connor, Gabriele Keller, Craig McLaughlin, Vincent
          Jackson, and Christine Rizkallah. Dargent: A silver bullet for verified data layout refinement.
          Proc. ACM Program. Lang., 7(POPL), jan 2023. doi:10.1145/3571240.
      2   Andreea Costea, Amy Zhu, Nadia Polikarpova, and Ilya Sergey. Concise Read-Only Specific-
          ations for Better Synthesis of Programs with Pointers. In ESOP, volume 12075 of LNCS,
          pages 141–168. Springer, 2020. doi:10.1007/978-3-030-44914-8\_6.
      3   Cordelia V. Hall, Kevin Hammond, Will Partain, Simon L. Peyton Jones, and Philip Wadler.
          The Glasgow Haskell Compiler: A Retrospective. In Proceedings of the 1992 Glasgow Work-
          shop on Functional Programming, Workshops in Computing, pages 62–71. Springer, 1992.
          doi:10.1007/978-1-4471-3215-8\_6.
      4   C. A. R. Hoare. An axiomatic basis for computer programming.                 Commun. ACM,
          12(10):576–580, oct 1969. doi:10.1145/363235.363259.
      5   Paul Hudak, John Hughes, Simon Peyton Jones, and Philip Wadler. A History of Haskell:
          Being Lazy with Class. In Proceedings of the Third ACM SIGPLAN Conference on History
          of Programming Languages, page 12–1–12–55. ACM, 2007. doi:10.1145/1238844.1238856.
      6   Shachar Itzhaky, Hila Peleg, Nadia Polikarpova, Reuben N. S. Rowe, and Ilya Sergey. Cyclic
          program synthesis. In PLDI, page 944–959. ACV, 2021. doi:10.1145/3453483.3454087.
       Young et al.                                                                                    27


 7   Peter O’Hearn, John Reynolds, and Hongseok Yang. Local reasoning about programs that
     alter data structures. In Laurent Fribourg, editor, Computer Science Logic, pages 1–19, Berlin,
     Heidelberg, 2001. Springer Berlin Heidelberg.
 8   Nadia Polikarpova, Ivan Kuraj, and Armando Solar-Lezama.       Program syn-
     thesis from polymorphic refinement types. In PLDI, page 522–538. ACM, 2016.
     doi:10.1145/2908080.2908093.
 9   Nadia Polikarpova and Ilya Sergey. Structuring the synthesis of heap-manipulating programs.
     Proc. ACM Program. Lang., 3(POPL), jan 2019. doi:10.1145/3290385.
10   John C. Reynolds. Separation logic: a logic for shared mutable data structures. In LICS,
     pages 55–74, 2002. doi:10.1109/LICS.2002.1029817.
11   Reuben N. S. Rowe and James Brotherston. Automatic cyclic termination proofs for recursive
     procedures in separation logic. In Proceedings of the 6th ACM SIGPLAN Conference on
     Certified Programs and Proofs, CPP 2017, page 53–65, New York, NY, USA, 2017. Association
     for Computing Machinery. doi:10.1145/3018610.3018623.
12   David Turner.   An Overview of Miranda.             SIGPLAN Not., 21(12):158–166, 1986.
     doi:10.1145/15042.15053.
13   Yasunari Watanabe, Kiran Gopinathan, George Pîrlea, Nadia Polikarpova, and Ilya Sergey.
     Certifying the synthesis of heap-manipulating programs. Proc. ACM Program. Lang.,
     5(ICFP):1–29, 2021. doi:10.1145/3473589.


 A     Implementation

The translation occurs as a sequence of several stages:
1. Type checking and elaboration. This stage does type-checking. It also annotates
   the abstract syntax tree with the fresh names that will be used in the resulting SuSLik
   code. The number of SuSLik names needed for a given layout is determined during type
   checking, which is why this annotation is performed at this stage. instantiates are also
   instantiated for recursive calls during this stage.
2. Unfold empty constructors. Constructors that are assigned emp by a layout need to
   be handled specially. This is because an == 0 constraint must be generated at the end,
   as opposed to just a emp heaplet.
3. Unfold pattern matches using layouts. This stage partially translates a pattern
   match into its SuSLik equivalent. The AST is annotated with the heaplets correspond-
   ing to the layout branch for the particular constructor in the pattern match. The other
   part of the pattern match translation, the generation of the corresponding Boolean con-
   ditionals, is done during the final stage.
4. Insert copying predicate applications.
5. Translate lets. Each let is turned into a SuSLik equality constraint.
6. Unfold constructor applications. In the expressions that constitute the function
   body, translate the constructor applications into heaplets using the specified layouts.
   Function calls are translated into the corresponding inductive predicate applications.
   For base type expressions (that is, of type Int or Bool), pure SuSLik constraints are
   generated. During this phase, if-then-else expressions are translated into SuSLik
   equality constraints with ... ? ... : ... on the right-hand side of the equalities.
7. Generation. The Boolean conditions corresponding to each pattern match are gener-
   ated and the final inductive predicate is generated.
In Appendix E the filterLt9 example is used to go through each stage, step-by-step.
28         Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


     B      Algebraic Data Type and Layout Definitions For Examples

     data   List := Nil | Cons Int List ;
     data   Tree := Leaf | Node Int Tree Tree ;
     data   ListOfLists := LNil | LCons List ListOfLists ;
     data   Zipped := ZNil | ZCons Int Int Zipped ;

     Sll : List >-> layout [ x ];
     Sll ( Nil ) := emp ;
     Sll ( Cons head tail ) := x : - > head , ( x +1) : - > tail , Sll tail ;

     TreeLayout : Tree >-> layout [ x ];
     TreeLayout ( Leaf ) := emp ;
     TreeLayout ( Node payload left right ) :=
       x : - > payload ,
       ( x +1) : - > left ,
       ( x +2) : - > right ,
       TreeLayout left ,
       TreeLayout right ;

     ListOfListsLayout : ListOfLists >-> layout [ x ];
     ListOfListsLayout ( LNil ) := emp ;
     ListOfListsLayout ( LCons head tail ) :=
       x : - > head , ( x +1) : - > tail ,
       ListOfListsLayout tail ,
       Sll head ;

     ZippedLayout : Zipped >-> layout [ x ];
     ZippedLayout ( ZNil ) := emp ;
     ZippedLayout ( ZCons fst snd rest ) :=
       x : - > fst ,
       ( x +1) : - > snd ,
       ( x +2) : - > rest ,
       ZippedLayout rest ;



     C      Reference Implementation for Examples

     C.1    filterLt9
     tool implementation
     % generate filterLt9 [ Sll ] Sll

     filterLt9 : List -> List ;
     filterLt9 ( Nil ) := Nil ;
     filterLt9 ( Cons head tail )
       | head < 9         := filterLt9 tail ;
       | not ( head < 9) := Cons head ( filterLt9 tail );

         Generated SuSLik
     predicate f i l t e r L t 9 _ _ r w _ S l l _ _ r o _ S l l ( loc __p_x0 , loc __r_x ) {
     | ( __p_x0 == 0) = > { __r_x == 0 ; emp }
     | (( not ( __p_x0 == 0)) && ( head < 9)) = > {
       Young et al.                                                                                29


     __p_x0 : - > head ** ( __p_x0 +1) : - > tail ** [ __p_x0 ,2] **
     f i l t e r L t 9 _ _ r w _ S ll _ _ r o _ S l l ( tail , __r_x ) }
| (( not ( __p_x0 == 0)) && ( not ( head < 9))) = > {
     __p_x0 : - > head ** ( __p_x0 +1) : - > tail ** [ __p_x0 ,2] **
     f i l t e r L t 9 _ _ r w _ S ll _ _ r o _ S l l ( tail , __p_x3 ) **
     __r_x : - > head ** ( __r_x +1) : - > __p_x3 ** [ __r_x ,2] }
}

   Reference SuSLik
predicate filter_base2 ( loc x , loc y ){
| y == 0 = > { x == 0 ; emp }
| ( not ( y == 0)) && ( vy < 9)     => {
     [y ,2] ** y : - > vy ** ( y + 1) : - > ynxt **
     filter_base2 (x , ynxt )}
| ( not ( y == 0)) && ( not ( vy < 9))      => {
      [y , 2] ** y : - > vy ** ( y + 1) : - > ynxt **
      [x , 2] ** x : - > vy ** ( x + 1) : - > xnxt **
      filter_base2 ( xnxt , ynxt )}
}



C.2    fold
tool implementation
% generate fold_List [ Int , Sll ] ( Ptr Int )

fold_List : Int -> List -> Ptr Int ;
fold_List z ( Nil ) := z ;
fold_List z ( Cons x xs ) :=
  instantiate
    [ Ptr Int , Ptr Int ]
    ( Ptr Int )
    f
    ( addr x )
    ( fold_List z xs );

   Generated SuSLik
predicate f o l d _ L i s t _ _ P t r _ I n t _ _ I n t _ _ r o _ S l l ( int __p_0 , loc __p_x1
                                                                          , loc __r ) {
| ( __p_x1 == 0) = > { __r : - > __p_0 }
| ( not ( __p_x1 == 0)) = > {
  __p_x1 : - > x ** ( __p_x1 +1) : - > xs ** [ __p_x1 ,2] **
  func f _ _ P t r _ I n t _ _ P t r _ I n t _ _ P t r _ I n t ( __p_x1 , __p_2 , __r ) **
  f o l d _ L i s t _ _ P t r _ I n t _ _ I n t _ _ r o _ S l l ( __p_0 , xs , __p_2 )
  ** temploc __p_2 }
}

   Reference SuSLik
predicate fold_sll ( int init , loc x , loc ret ){
| x == 0 = > { func sll_copy ( init , ret )}
| not ( x == 0) = > {
    [x , 2] ** x : - > v ** ( x + 1) : - > xnxt ** temploc t **
    func f (x , t , ret ) **
30         Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


            fold_sll ( init , xnxt , t )
     }
     }



     C.3     maximum
     tool implementation
     % generate maximum [ Sll ] Int

     maximum : List -> Int ;
     maximum ( Nil ) := 0;
     maximum ( Cons x xs ) :=
       let i := maximum xs
       in
       if i < x
          then x
          else i ;

          Generated SuSLik
     predicate maximum__Int__ro_Sll ( loc __p_x0 , int __r ) {
     | ( __p_x0 == 0) = > { __r == 0 ; emp }
     | ( not ( __p_x0 == 0)) = > {
            i == __p_1 && __r == (( i < x ) ? x : i ) && __temp_0 == __p_1
               ;
            __p_x0 : - > x ** ( __p_x0 +1) : - > xs ** [ __p_x0 ,2] **
            maximum__Int__ro_Sll ( xs , __temp_0 ) }
     }

          Reference SuSLik
     predicate maximum ( loc x , int ret ) {
     | x == null = > { ret == 0; emp }
     | not ( x == null ) = > {
         ret == ( ret0 <= v ? v : ret0 );
         [x , 2] ** x : - > v ** x + 1 : - > xnxt **
         maximum ( xnxt , ret0 )
     }
     }



      D      More Examples
     D.1     cons
     This example prepends an item to a list. In particular, we have the function instantiated
     with the singly-linked list layout, so it will synthesize a function to perform this task on
     singly-linked lists.
         tool implementation
     % generate cons [ Int , Sll ] Sll

     cons : Int -> List -> List ;
     cons x xs := Cons x xs ;
       Young et al.                                                                                  31


   Generated SuSLik
predicate c o n s _ _ r w _ S l l _ _ I n t _ _ r o _ S l l ( int __p_0 , loc __p_x1 , loc __r_x )
{
| true = > { __r_x : - > __p_0 ** ( __r_x +1) : - > __p_x1 ** [ __r_x ,2] }
}

   Reference SuSLik
predicate cons ( int v , loc x , loc ret ) {
| true = > {[ ret , 2] ** ret : - > v ** func cp (x , ret ) + 1 ** sll_c ( x )}
}



D.2    car
This example would get the head of a list. The synthesizer is currently synthesizing a
recursive function which does not have the correct behavior.
   tool implementation
% generate car [ Sll ] Int

car : List -> Int ;
car ( Nil ) := 0;
car ( Cons x xs ) := x ;

   Generated SuSLik
predicate car__Int__ro_Sll ( loc __p_x0 , int __r ) {
| ( __p_x0 == 0) = > { __r == 0 ; emp }
| ( not ( __p_x0 == 0)) = > {
     __r == x ; __p_x0 : - > x ** ( __p_x0 +1) : - > xs ** [ __p_x0 ,2] }
}



D.3    singleton
A function which creates a singleton list out of the given integer argument.
   tool implementation
% generate singleton [ Int ] Sll

singleton : Int -> List ;
singleton x := Cons x ( Nil );

   Generated SuSLik
predicate si ng le ton __ rw _S ll_ _I nt ( int __p_0 , loc __r_x ) {
| true = > { __r_x : - > __p_0 ** ( __r_x +1) : - > 0 ** [ __r_x ,2] }
}

   Reference SuSLik
predicate singleton_list ( int n , loc x ) {
| true = > { [x , 2] ** x : - > n ** ( x +1) : - > 0 }
}
32         Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


     D.4    map
     tool implementation
     % generate map [ Sll ] Sll

     map : List -> List ;
     map ( Nil ) := Nil ;
     map ( Cons x xs ) := Cons ( instantiate [ Int ] Int f x ) ( map xs );

        Generated SuSLik
     predicate map__rw_Sll__ro_Sll ( loc __p_x0 , loc __r_x ) {
     | ( __p_x0 == 0) = > { __r_x == 0 ; emp }
     | ( not ( __p_x0 == 0)) = > {
          __r_x == __p_1 ; __p_x0 : - > x ** ( __p_x0 +1) : - > xs **
          [ __p_x0 ,2] ** func f__Int__Int (x , __p_1 ) **
          map__rw_Sll__ro_Sll ( xs , __p_x3 ) **
          ( __r_x +1) : - > __p_x3 ** [ __r_x ,2] }
     }

        Reference SuSLik
     predicate sll_map ( loc x , loc          y) {
     | x == 0            = > { y == 0         ; emp }
     | not ( x == 0) = > {
          [x , 2] ** x : - > h ** ( x         + 1) : - > xnxt ** [y , 2] **
          func f (x , y ) ** ( y + 1)         : - > ynxt **
          sll_map ( xnxt , ynxt ) }
     }



     D.5    snoc
     This example prepends an item to a singly-linked list.
        tool implementation
     % generate snoc [ Sll , Int ] Sll

     snoc : List -> Int -> List ;
     snoc ( Nil ) i := Cons i ( Nil );
     snoc ( Cons x xs ) i := Cons x ( snoc xs i );

        Generated SuSLik
     predicate s n o c _ _ r w _ S l l _ _ r o _ S l l _ _ I n t ( loc __p_x0 , int __p_1 , loc __r_x )
     {
     | ( __p_x0 == 0) = > { __r_x : - > __p_1 ** ( __r_x +1) : - > 0 **
                                           [ __r_x ,2] }
     | ( not ( __p_x0 == 0)) = > {
          __p_x0 : - > x ** ( __p_x0 +1) : - > xs ** [ __p_x0 ,2] **
          s n o c _ _ r w _ S l l _ _ ro _ S l l _ _ I n t ( xs , __p_1 , __p_x3 ) **
          __r_x : - > x ** ( __r_x +1) : - > __p_x3 ** [ __r_x ,2] }
     }
       Young et al.                                                                    33


D.6    reverse
This example reverses a singly-linked list.
   tool implementation
% generate reverse [ Sll ] Sll

reverse : List -> List ;
reverse ( Nil ) := Nil ;
reverse ( Cons x xs ) :=
  instantiate [ Sll [ mutable ] , Int ] Sll snoc ( reverse xs ) x ;

   Generated SuSLik
predicate r ev e rs e __ rw _ Sl l __ ro _ Sl l ( loc __p_x0 , loc __r_x ) {
| ( __p_x0 == 0) = > { __r_x == 0 ; emp }
| ( not ( __p_x0 == 0)) = > {
     __p_x0 : - > x ** ( __p_x0 +1) : - > xs ** [ __p_x0 ,2] **
     func s n o c _ _ r w _ S l l _ _ rw _ S l l _ _ I n t ( __p_x1 , x , __r_x ) **
     r ev e rs e_ _ rw _ Sl l_ _ ro _ Sl l ( xs , __p_x1 ) **
     temploc __p_x1 }
}

   Reference SuSLik
predicate reverse ( int init , loc x , loc ret ){
| x == 0 = > { ret : - > init }
| not ( x == 0) = > {
    [x , 2] ** x : - > v ** ( x + 1) : - > xnxt ** temploc t **
    reverse ( init , xnxt , t ) ** func tail (t , x , ret )
}
}

predicate tail ( loc x , int v , loc ret ){
| x == null = > {[ ret , 2] ** ret : - > v ** ret + 1 : - > 0}
| not ( x == null ) = > {
    [x , 2] ** x : - > v ** x +1 : - > xnxt **
    [ ret , 2] ** ret : - > v ** ret +1 : - > retnxt **
    tail ( xnxt , v , retnxt )
}
}



D.7    append
This example appends two singly-linked lists together.
   tool implementation
% generate append [ Sll , Sll ] Sll

append : List -> List -> List ;
append ( Nil ) ys := ys ;
append ( Cons x xs ) ys :=
  instantiate [ Ptr Int , Sll [ mutable ]] Sll
    cons
    ( addr x )
    ( append xs ys );
34         Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


         Generated SuSLik
     predicate a p p e n d _ _ r w _ S l l _ _ r o _ S l l _ _ r o _ S l l ( loc __p_x0 , loc __p_x1
                                                                              , loc __r_x ) {
     | ( __p_x0 == 0) = > { func Sll__copy ( __p_x1 , __r_x ) }
     | ( not ( __p_x0 == 0)) = > {
           __p_x0 : - > x ** ( __p_x0 +1) : - > xs ** [ __p_x0 ,2] **
           func c o n s _ _ r w _ S l l _ _ P t r _ I n t _ _ r w _ S l l ( __p_x0 , __p_x2 , __r_x ) **
           a p p e n d _ _ r w _ S l l _ _ r o _ S l l _ _ r o _ S l l ( xs , __p_x1 , __p_x2 ) **
           temploc __p_x2 }
     }

         Reference SuSLik
     predicate append ( loc x1 , loc x2 , loc ret ){
     | x1 == 0 = > { sll_c ( x2 ) ** func sll_copy ( x2 , ret )}
     | not ( x1 == 0) = > {
         [ x1 , 2] ** x1 : - > v ** x1 + 1 : - > x1nxt **
         temploc t ** append ( x1nxt , x2 , t ) **
         func cons ( x1 , t , ret )

     }
     }



     D.8     zip
     This example takes two lists and zips them into a list of pairs.
        tool implementation
     % generate zip [ Sll , Sll ] ZippedLayout

     zip   : List -> Zipped ;
     zip   ( Nil ) ys := ZNil ;
     zip   xs ( Nil ) := ZNil ;
     zip   ( Cons x xs ) ( Cons y ys ) := ZCons x y ( zip xs ys );

         Generated SuSLik
     predicate z i p _ _ r w _ Z i p p e d L a y o u t _ _ r o _ S l l _ _ r o _ S l l ( loc __p_x0 , loc __p_x1
                                                                                          , loc __r_x ) {
     | ( __p_x0 == 0) = > { __r_x == 0 ; emp }
     | ( __p_x1 == 0) = > { __r_x == 0 ; emp }
     | (( not ( __p_x0 == 0)) && ( not ( __p_x1 == 0))) = > {
           __p_x0 : - > x ** ( __p_x0 +1) : - > xs ** [ __p_x0 ,2] **
           __p_x1 : - > y ** ( __p_x1 +1) : - > ys ** [ __p_x1 ,2] **
           z i p _ _ r w _ Z i p p e d L a y o u t _ _ r o _ S l l _ _ r o _ S l l ( xs , ys , __p_x2 ) **
           __r_x : - > x ** ( __r_x +1) : - > y ** ( __r_x +2) : - > __p_x2 **
           [ __r_x ,3] }
     }



     D.9     zipWith
     This example is similar to zip, but instead of pairing it applies a binary function pairwise
     to the items from the two lists.
         tool implementation
         Young et al.                                                                                   35



% generate zipWith [ Sll , Sll ] Sll

 zipWith : List -> List -> List ;
 zipWith ( Nil ) ( Nil ) := Nil ;
 zipWith ( Nil ) ( Cons y ys ) := Nil ;
 zipWith ( Cons x xs ) ( Nil ) := Nil ;
 zipWith ( Cons x xs ) ( Cons y ys ) :=
   Cons
     ( instantiate [ Int , Int ] Int f x y )
     ( zipWith xs ys );

   Generated SuSLik
predicate z i p W i t h _ _ r w _ S l l _ _ r o _ S l l _ _ r o _ S l l ( loc   __p_x0 , loc __p_x1
                                                                        , loc   __r_x ) {
| (( __p_x0 == 0) && ( __p_x1 == 0)) = > { __r_x                                == 0 ; emp }
| (( __p_x0 == 0) && ( not ( __p_x1 == 0))) = > {                               __r_x == 0
                                                                                ; ro_Sll ( __p_x1 ) }
| (( __p_x1 == 0) && ( not ( __p_x0 == 0))) = > { __r_x == 0
                                                                                ; ro_Sll ( __p_x0 ) }
| (( not ( __p_x0 == 0)) && ( not ( __p_x1 == 0))) = > {
   __r_x == __p_2
       ;
   __p_x0 : - > x ** ( __p_x0 +1) : - > xs ** [ __p_x0 ,2] **
   __p_x1 : - > y ** ( __p_x1 +1) : - > ys ** [ __p_x1 ,2] **
   func f__Int__Int__Int (x , y , __p_2 ) **
   z i p W i t h _ _ r w _ S l l _ _ r o _ S l l _ _ r o _ S l l ( xs , ys , __p_x5 ) **
   ( __r_x +1) : - > __p_x5 ** [ __r_x ,2] }
}

   Reference SuSLik
predicate zip_withf ( loc x , loc y , loc r ) {
| x == 0 && y == 0 = > { r == null ; emp }
| y == 0 && not ( x == 0) = > { r == null ; sll_c ( x ) }
| x == 0 && not ( y == 0) = > { r == null ; sll_c ( y ) }
| ( not ( x == 0)) && ( not ( y == 0)) = > {
     [x , 2] ** x : - > a ** ( x +1) : - > nxtX **
     [y , 2] ** y : - > b ** ( y +1) : - > nxtY **
     [r , 2] ** func f (x , y , r ) ** ( r +1) : - > nxtR **
     zip_withf ( nxtX , nxtY , nxtR )
  }
}



D.10      scanr
This is similar to a right fold, but it collects all of the intermediate results in the result list.
   tool implementation
% generate scanr [ Int , Sll ] Sll

 scanr    : Int -> List -> List ;
 scanr    z ( Nil ) := Cons z ( Nil );
 scanr    z ( Cons x xs ) :=
   let    xs2 := scanr z xs
36        Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


        in
        let x2 := instantiate [ Int , Int ] Int f x
                      ( instantiate [ Sll [ mutable ]] Int head xs2 )
        in
        Cons x2 xs2 ;

        Generated SuSLik
     predicate s c a n r _ _ r w _ S l l _ _ I n t _ _ r o _ S l l ( int __p_0 , loc __p_x1
                                                                      , loc __r_x ) {
     | ( __p_x1 == 0) = > { __r_x : - > __p_0 ** ( __r_x +1) : - > 0 **
                                            [ __r_x ,2] }
     | ( not ( __p_x1 == 0)) = > {
          xs2 == __p_x3 && x2 == __p_7
              ;
          __p_x1 : - > x ** ( __p_x1 +1) : - > xs ** [ __p_x1 ,2] **
          s c a n r _ _ r w _ S l l _ _ I n t _ _ r o _ S l l ( __p_0 , xs , __p_x3 ) **
          func f__Int__Int__Int (x , __p_8 , __p_7 ) **
          func head__Int__rw_Sll ( __p_x3 , __p_8 ) **
          __r_x : - > x2 ** ( __r_x +1) : - > __p_x3 ** [ __r_x ,2] }
     }

        Reference SuSLik
     predicate scanr_sum ( int init , int tmp , loc x , loc ret ){
     | x == 0 = > { init == tmp ; [ ret , 2] ** ret : - > init **
                                     ret + 1 : - > 0}
     | not ( x == 0) = > { tmp == v + tmp0 ;
         [x , 2] ** x : - > v ** ( x + 1) : - > xnxt **
         [ ret , 2] ** ret : - > tmp ** ret + 1 : - > retnxt **
         scanr_sum ( init , tmp0 , xnxt , retnxt )
     }
     }



     D.11     selfAppend
     This example would append a list to itself. Due to the fact that there is currently no exposed
     copy operation, the fact that this function refers to its argument multiple times prevents it
     from synthesizing.
        tool implementation
     % generate selfAppend [ Sll ] Sll

     selfAppend : List -> List ;
     selfAppend xs :=
       instantiate [ Sll , Sll ] Sll append xs xs ;

        Generated SuSLik
     predicate s e l f A p p e n d _ _ r w _ S l l _ _ r o _ S l l ( loc __p_x0 , loc __r_x ) {
     | true = > {
         func a p p e n d _ _ r w _ S l l _ _ r o _ S l l _ _ r o _ S l l ( __p_x0 , __p_x0 , __r_x ) }
     }
       Young et al.                                                                                  37


D.12     take
This would return the first n items of the given list. In the higher-level implementation, we
use a machine Int for the count argument. As SuSLik does not currently have the capability
to reason inductively about machine ints, this does not synthesize. This limitation could
possibly be addressed by using an ADT unary representation for natural numbers.
    tool implementation
% generate take [ Int , Sll ] Sll

take : Int -> List -> List ;
take i ( Nil ) := Nil ;
take i ( Cons head tail )
  | i == 0 := Nil ;
  | not ( i == 0) := Cons head ( take ( i - 1) tail );

   Generated SuSLik
predicate t a k e _ _ r w _ S l l _ _ I n t _ _ r o _ S l l ( int __p_0 , loc __p_x1 , loc __r_x )
{
| ( __p_x1 == 0) = > { __r_x == 0 ; emp }
| (( not ( __p_x1 == 0)) && ( __p_0 == 0)) = > { __r_x == 0
                                                                          ; ro_Sll ( __p_x1 ) }
| (( not ( __p_x1 == 0)) && ( not ( __p_0 == 0))) = > {
      __p_x1 : - > head ** ( __p_x1 +1) : - > tail ** [ __p_x1 ,2] **
      t a k e _ _ r w _ S l l _ _ In t _ _ r o _ S l l (( __p_0 - 1) , tail , __p_x2 ) **
      __r_x : - > head ** ( __r_x +1) : - > __p_x2 ** [ __r_x ,2] }
}

   Reference SuSLik
predicate take ( loc x , int n , int ret ){
| true = > {
    temploc t ** func number (n , t ) ** func take_helper (x , t , ret )
}
}


predicate take_helper ( loc x , loc helper , int ret ){
| x == 0 = > { ret == 0; sll_c ( helper )}
| not ( x == 0) && helper == 0 = > { ret == v ;
    [x , 2] ** x : - > v ** x + 1 : - > xnxt ** sll_c ( xnxt )
}
| not ( x == 0) && not ( helper == 0) = > {
    [x , 2] ** x : - > v ** x + 1 : - > xnxt **
    [ helper , 2] ** helper : - > vv ** helper + 1 : - > helpernxt **
    take_helper ( xnxt , helpernxt , ret )
}
}



D.13     replicate
This has similar problems as take: using a machine Int for a count argument instead of a
unary representation.
   tool implementation
38        Higher-Order Specifications for Deductive Synthesis of Programs with Pointers



     % generate replicate [ Int , Int ] Sll

     replicate : Int -> Int -> List ;
     replicate n i
       | n == 0 := Nil ;
       | not ( n == 0) := Cons i ( replicate ( n - 1) i );

        Generated SuSLik
     predicate r e p l i c a t e _ _ r w _ S l l _ _ I n t _ _ I n t ( int __p_0 , int __p_1
                                                                       , loc __r_x ) {
     | ( __p_0 == 0) = > { __r_x == 0 ; emp }
     | ( not ( __p_0 == 0)) = > {
          r e p l i c a t e _ _ r w _ S l l _ _ I n t _ _ I n t (( __p_0 - 1) , __p_1 , __p_x2 ) **
          __r_x : - > __p_1 ** ( __r_x +1) : - > __p_x2 ** [ __r_x ,2] }
     }

        Reference SuSLik
     predicate replicate_helper ( int n , loc helper , loc ret ){
     | helper == 0 = > { ret == 0 ; emp }
     | not ( helper == 0) = > {
         [ helper , 2] ** helper : - > vv ** helper + 1 : - > helpernxt **
         [ ret , 2] ** ret : - > n ** ret + 1 : - > retnxt **
         replicate_helper (n , helpernxt , retnxt )
     }
     }


     D.14     foldMap
     This example maps a function over a list and then folds the result. This demonstrates nested
     function application.
        tool implementation
     % generate foldMap [ Int , Sll [ mutable ]] Int

     foldMap : Int -> List -> Int ;
     foldMap z ( Nil ) := z ;
     foldMap z ( Cons x xs ) :=
       instantiate [ Int , Sll [ mutable ]] Int fold_List
          z
          ( instantiate [ Sll ] Sll map
              ( lower Sll ( Cons x xs )));

        Generated SuSLik
     predicate f o l d M a p _ _ I n t _ _ I n t _ _ r w _ S l l ( int __p_0 , loc __p_x1 , int __r ) {
     | ( __p_x1 == 0) = > { __r == __p_0 ; emp }
     | ( not ( __p_x1 == 0)) = > {
           __p_x1 : - > x ** ( __p_x1 +1) : - > xs ** [ __p_x1 ,2] **
           func f o l d _ L i s t _ _ I n t _ _ I n t _ _ r w _ S l l ( __p_0 , __p_x2 , __r ) **
           func map__rw_Sll__ro_Sll ( __p_x2 , __p_x2 ) **
           __p_x2 : - > x ** ( __p_x2 +1) : - > xs ** [ __p_x2 ,2] **
           temploc __p_x2 }
     }
        Young et al.                                                                                     39


D.15      mapSum
This example takes a list of lists of Ints and sums up each inner list.
   tool implementation
% generate map_sum [ ListOfListsLayout ] Sll

map_sum : ListOfLists -> List ;
map_sum ( LNil ) := Nil ;
map_sum ( LCons xs xss ) :=
  Cons ( instantiate [ Sll ] Int sum xs )
       ( map_sum xss );

   Generated SuSLik
predicate m a p _ s u m _ _ r w _ S l l _ _ r o _ L i s t O f L i s t s L a y o u t ( loc __p_x0
                                                                                       , loc __r_x ) {
| ( __p_x0 == 0) = > { __r_x == 0 ; emp }
| ( not ( __p_x0 == 0)) = > {
      __r_x == __p_1
          ;
      __p_x0 : - > xs ** ( __p_x0 +1) : - > xss ** ro_Sll ( xs ) **
      [ __p_x0 ,2] **
      func sum__Int__ro_Sll ( xs , __p_1 ) **
      m a p _ s u m _ _ r w _ S l l _ _ r o _ L i s t O f L i s t s L a y o u t ( xss , __p_x4 ) **
      ( __r_x +1) : - > __p_x4 ** [ __r_x ,2] }
}

   Reference SuSLik
predicate map_sum ( loc x , loc y ) {
| x == 0           = > { y == 0 ; emp }
| not ( x == 0) = > {
    [x , 2] ** x : - > h ** ( x + 1) : - > xnxt ** sll_c ( h ) **
    [y , 2] ** func sum (x , y ) ** ( y + 1) : - > ynxt
    ** map_sum ( xnxt , ynxt ) }
}



D.16      leftList
This example takes a binary tree and gives back a list of items along the path going down
only the left subtrees. This demonstrates the interaction between two different data types.
   tool implementation
% generate leftList [ TreeLayout ] Sll

leftList : Tree -> List ;
leftList ( Leaf ) := Nil ;
leftList ( Node a b c ) := Cons a ( leftList b );

   Generated SuSLik
predicate l e f t L i s t _ _ r w _ S l l _ _ r o _ T r e e L a y o u t ( loc __p_x0 , loc __r_x ) {
| ( __p_x0 == 0) = > { __r_x == 0 ; emp }
| ( not ( __p_x0 == 0)) = > {
    __p_x0 : - > a ** ( __p_x0 +1) : - > b ** ( __p_x0 +2) : - > c **
40         Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


          [ __p_x0 ,3] **
          l e f t L i s t _ _ r w _ S l l _ _ r o _ T r e e L a y o u t (b , __p_x1 ) **
          __r_x : - > a ** ( __r_x +1) : - > __p_x1 ** [ __r_x ,2] }
     }

          Reference SuSLik
     predicate left_tree ( loc x , loc y ){
     | x == 0           = > { emp }
     | not ( x == 0) = > {
         [x , 3] ** x := > v ** x + 1 := > l ** x + 2 := > r ** tree_c ( r ) **
         [y , 2] ** y : - > v ** y + 1 : - > ynxt ** left_tree (l , ynxt )
     }
     }



     D.17      sum
     This is effectively a fold specialized to the addition function and 0.
        tool implementation
     % generate sum [ Sll ] Int

     sum : List -> Int ;
     sum ( Nil ) := 0;
     sum ( Cons head tail ) := head + ( sum tail );

          Generated SuSLik
     predicate sum__Int__ro_Sll ( loc __p_x0 , int __r ) {
     | ( __p_x0 == 0) = > { __r == 0 ; emp }
     | ( not ( __p_x0 == 0)) = > {
          __r == ( head + __p_1 ) && __temp_0 == __p_1
            ;
          __p_x0 : - > head ** ( __p_x0 +1) : - > tail ** [ __p_x0 ,2] **
          sum__Int__ro_Sll ( tail , __temp_0 ) }
     }

          Reference SuSLik
     predicate sum ( loc l , int output ){
     | l == null = > { output == 0; emp }
     | l != null = > { output == output1 + v ; [l , 2] ** l : - > v **
         l + 1 : - > lnxt ** sum ( lnxt , output1 )}
     }



      E     Translation Stages Example
     We use the filterLt9 example to illustrate each stage. An additional syntactic construct
     is used in this example to illustrate the internal changes to the AST as the translation goes
     through its stages. The syntax layout{A} & e is a tool expression e annotated with the
     SuSLik assertion A.
     % generate filterLt9 [ Sll [ readonly ]] Sll
      Young et al.                                                               41


data List := Nil | Cons Int List ;

Sll : List >-> layout [ x ];
Sll Nil := emp ;
Sll ( Cons head tail ) := x : - > head , ( x +1) : - > tail , Sll tail

filterLt9 : List -> List ;
filterLt9 p Nil       := Nil ;
filterLt9 p ( Cons head tail )
  | head < 9        := filterLt9 p tail ;
  | not ( head < 9) := Cons head ( filterLt9 p tail );


1. Type checking and elaboration.
   filterLt9 ( Sll [ readonly ; x ] Nil ) := lower Sll [ readonly ; r ] Nil ;
   filterLt9 ( Sll [ readonly ; x ] ( Cons head tail ))
   | head < 9          :=
       instantiate [ Sll [ readonly ; tail ]] Sll [ r ] filter tail ;
   | not ( head < 9) :=
       lower Sll [ readonly ; r ]
         ( Cons head
            ( instantiate [ Sll [ readonly ; tail ]] Sll [ y ]
               filterLt9 tail ));

2. Unfold empty constructors.
   filterLt9 ( Sll [ readonly ; x ] Nil ) := lower Sll [ readonly ; r ] 0;
   filterLt9 ( Sll [ readonly ; x ] ( Cons head tail ))
   | head < 9          :=
       instantiate [ Sll [ readonly ; tail ]] Sll [ r ] filter tail ;
   | not ( head < 9) :=
       lower Sll [ readonly ; r ]
         ( Cons head
            ( instantiate [ Sll [ readonly ; tail ]] Sll [ y ]
               filterLt9 tail ));

3. Unfold pattern matches using layouts.
   filterLt9 Nil         :=
       layout { r == 0 ; emp }
         & 0;
   filterLt9 ( Cons head tail )
     | head < 9          :=
           layout { x := > head , ( x +1) := > tail }
              & instantiate [ Sll [ readonly ; tail ]] Sll [ r ] filter tail ;
     | not ( head < 9) :=
           layout { x := > head , ( x +1) := > tail }
              & lower Sll [ readonly ; r ]
                  ( Cons head
                     ( instantiate [ Sll [ readonly ; tail ]] Sll [ y ]
                        filterLt9 tail ));

4. Insert copying predicate applications. Not applicable.
5. Translate lets. Not applicable.
6. Unfold constructor applications.
42          Higher-Order Specifications for Deductive Synthesis of Programs with Pointers



          filterLt9 Nil        := layout { r == 0 ; emp };
          filterLt9 ( Cons head tail )
            | head < 9         :=
                layout { x := > head , ( x +1) := > tail
                  , filterLt9__Sll_Sll [ tail | r ] tail ));
            | not ( head < 9) :=
                layout { x := > head , ( x +1) := > tail , r : - > head , ( r +1) : - > y ,
                  filterLt9__Sll_Sll [ tail | y ] tail ));

     7. Generation.
          inductive Sll ( loc x ) {
          | x == 0 = > { emp }
          | not ( x == 0) = > { x : - > head ** ( x +1) : - > tail ** Sll ( tail ) }
          }

          inductive filterLt9__Sll_Sll ( loc        x , loc r ) {
          | x == 0 = > { r == 0 ; emp }
          | not ( x == 0) && head < 9 = > {
              x := > head ** ( x +1) := > tail      ** filterLt9__Sll_Sll ( tail , r )
            }
          | not ( x == 0) && not ( head < 9)        => {
              x := > head ** ( x +1) := > tail      ** r : - > head ** ( r +1) : - > y **
              filterLt9__Sll_Sll ( tail , y )
            }
          }



      F      tool Grammar
     ⟨int⟩ ::= · · · | ‘-1’ | ‘0’ | ‘1’ | · · ·
     ⟨natural⟩ ::= ‘0’ | ‘1’ | · · ·
     ⟨bool⟩ ::= ‘false’ | ‘true’
     ⟨expr⟩ ::= ⟨int⟩
       | ⟨bool⟩
       | ⟨var⟩
       | ⟨expr⟩ ⟨expr⟩
       | ⟨expr⟩ ‘+’ ⟨expr⟩
       | ⟨expr⟩ ‘-’ ⟨expr⟩
       | ⟨expr⟩ ‘&&’ ⟨expr⟩
       | ⟨expr⟩ ‘||’ ⟨expr⟩
       | ‘not’ ⟨expr⟩
       | ‘instantiate’ ⟨layout-list⟩ ⟨layout-name⟩ ⟨var⟩ { ⟨expr⟩ }
       | ‘lower’ ⟨moded-layout⟩ ⟨expr⟩
     ⟨generate-directive⟩ ::= ‘%generate’ ⟨var⟩ ⟨layout-list⟩ ⟨layout-name⟩
     ⟨layout-list⟩ ::= ‘[’ { ⟨moded-layout⟩ } ‘]’
     ⟨mode⟩ ::= ‘readonly’
      | ‘mutable’
         Young et al.                                                                                            43


⟨moded-layout⟩ ::= ⟨layout-name⟩ ‘[’ ⟨mode⟩ ‘]’
⟨base-type⟩ ::= ‘Int’
  | ‘Bool’
⟨type⟩ ::= ⟨base-type⟩
  | ⟨var⟩
  | ⟨type⟩ -> ⟨type⟩
⟨fn-decl⟩ ::= ⟨var⟩ ‘:’ ⟨type⟩ ‘;’
⟨fn-def ⟩ ::= ⟨fn-case⟩ ‘;’ ⟨fn-def ⟩ | ⟨fn-case⟩ ‘;’
⟨fn-case⟩ ::= ⟨var⟩ ⟨pattern⟩ ⟨guarded-bodies⟩
⟨guarded-bodies⟩ ::= ⟨guarded-body⟩ ⟨guarded-bodies⟩ | ⟨guarded-body⟩
⟨guarded-body⟩ ::= ‘|’ ⟨expr⟩ ‘:=’ ⟨expr⟩
⟨layout-sig⟩ ::= ⟨layout-name⟩ ‘:’ ⟨data-name⟩ ‘>->’ ‘layout’ ‘[’ ⟨vars⟩ ‘]’ ‘;’
⟨layout-def ⟩ ::= ⟨layout-case⟩ ‘;’ ⟨layout-def ⟩ | ⟨layout-case⟩ ‘;’
⟨layout-case⟩ ::= ⟨layout-name⟩ ⟨pattern⟩ ‘:=’ ⟨layout-body⟩
⟨layout-body⟩ ::= ⟨heaplet⟩ ‘,’ ⟨layout-body⟩ | ⟨heaplet⟩
⟨heaplet⟩ ::= ‘emp’ | ⟨loc⟩ ‘:->’ ⟨var⟩ | ⟨var⟩ ⟨var⟩
⟨loc⟩ ::= ⟨var⟩ | ‘(’ ⟨var⟩ + ⟨natural⟩ ‘)’
⟨pattern⟩ ::= ‘(’ ⟨constructor-name⟩ ⟨var⟩ ‘)’
⟨data-def ⟩ ::= ‘data’ ⟨data-name⟩ ‘:=’ ⟨data-alts⟩ ‘;’
⟨data-alts⟩ ::= ⟨data-alt⟩ | ⟨data-alt⟩ ‘|’ ⟨data-alts⟩
⟨data-alt⟩ ::= ⟨constructor-name⟩ { ⟨type⟩ }

 G       Soundness Proof
First, we introduce an operator that will make it more convenient to talk about the conjunc-
tion of two SSL propositions:

     (p1 ; s1 ) ⊗ (p2 ; s2 ) = (p1 ∧ p2 ; s1 ∗ s2 )

Next, we present a lemma regarding this operator that will be used in the soundness proof:

▶ Lemma 6 (⊗ pairing). If (σ1 , h1 ) |= p and (σ2 , h2 ) |= q and σ1 ⊆ σ2 and h1 ⊥ h2 ,
then (σ2 , h1 ◦ h2 ) |= p ⊗ q

Now we proceed to soundness.

▶ Theorem 3 (Soundness). For any well-typed expression e, if T JeKV,r is satisfiable for
V = dom(σ ′ ) and (e, σ, h, F) 7−→ (e′ , σ ′ , h′ , F ′ , r), then (σ ′ , h′ ) |= T JeKV,r . That is, given an
expression e with a satisfiable SSL translation, any heap machine state that e transitions to
(by the abstract machine semantics) will be a model for the SSL translation of e (cf. Fig. 14).

Proof. Proceeding by induction on e:
44      Higher-Order Specifications for Deductive Synthesis of Programs with Pointers


      e = i for some i ∈ Z.
      We have
         T JiKV,r = (v == i; emp)
         v#V
         v=r
         σ ′ = σ ∪ {(r, i)}
         h′ = h = ∅
      Plugging these in, we find that we want to prove

          (σ ∪ {(r, i)}, ∅) |= (r == i; emp)

      This immediately follows from the rules of separation logic.
      e = b for some b ∈ B. This case proceeds exactly as the previous case.
      e = e1 + e2 . From the T J·K hypothesis, we have
         (e1 , V0 ) ⇓ (p1 , s2 , V1 , v1 )
         (e2 , V1 ) ⇓ (p2 , s2 , V2 , v2 )
         v # V2
         v=r
         T Je1 + e2 KV,r = (v == v1 + v2 ∧ p1 ∧ p2 ; s1 ∗ s2 )
         T Je1 KV0 ,v1 = (p1 ; s1 )
         T Je2 KV1 ,v2 = (p2 ; s2 )
      Plugging these in, we want to show

          (σ ′ , h′ ) |= (v == v1 + v2 ∧ p1 ∧ p2 ; s1 ∗ s2 )

      Furthermore, we see that

          T JeKV,r = (v == v1 + v2 ; emp) ⊗ T Je1 KV0 ,v1 ⊗ T Je2 KV1 ,v2

      From the AM relation hypothesis we have
     1. σ ′ = σy ∪ {(r, z)}
     2. z = x′ + y ′
     3. (x, σ, F, h1 ) 7−→ (x′ , σx , h′1 , F, vx )
     4. (y, σx , F, h2 ) 7−→ (y ′ , σy , h′2 , F, vy )
     5. v1 = vx
     6. v2 = vy
     7. h = h1 ◦ h2
     8. h′ = h′1 ◦ h′2
      From the first six items, we can derive

          (σ ′ , ∅) |= (v == v1 + v2 ; emp)

      From the inductive hypotheses, we get
        (σx , h′1 ) |= T Je1 Kdom(σx ),vx
        (σy , h′2 ) |= T Je2 Kdom(σy ),vy
      By Lemma 6

          (σy , h′1 ◦ h′2 ) |= T Je1 Kdom(σx ),vx ⊗ T Je2 Kdom(σy ),vy

      and we know that σx ⊆ σy .
      By Lemma 6, we conclude

          (σy ∪ {(r, z)}, h′ ) |= (v == v1 + v2 ; emp) ⊗ T Je1 Kdom(σx ),v1 ⊗ T Je2 Kdom(σy ),v2
   Young et al.                                                                                  45


e = v for some v ∈ Var. Therefore the only two AM rules that apply are AM-Base-Var
and AM-Loc-Var. Both cases proceed in the same way.
We know
   h = h′ = ∅
So we want to show

   (σ ′ , ∅) |= (true; emp)

This trivially holds.
e = lowerA (v) for some layout A and v ∈ Var. The applicable AM rule is AM-Lower.
From the premises of AM-Lower, we have
   h′ = ĥ · H ′
where H ′ comes from applying the layout A to the constructor application expression
obtained by reducing e. As a result, H ′ exactly fits the specification of one of the branches
of the A layout.
v must be associated with some high-level value in F and ĥ is the part of the heap that
is updated when this is reduced. Since all expressions are required to be well-typed, ĥ
must satisfy some collection of heaplets in the A layout branch that is associated to H ′ .
Note that T JeKV,r = A(v)
From these facts, we can conclude

   (σ ′ , h′ ) |= A(v)

e = lowerA (C e1 · · · en ). This case is similar to the previous case, except that we do not
need to lookup a variable in the store before dealing with the constructor application.
e = instA,B (f )(v) for some v ∈ Var. The rule AM-Instantiate applies here.
The S-Inst-Var rule requires that we satisfy the inductive predicate associated to f ,
that is IA,B (f )(v). Note that the SSL propositions in the definition of such an inductive
predicate, given by FnDef, will always not only explicitly describe the memory used in
its result (given by the layout B) but also the memory used in its argument (given by
the layout A).
Now, consider that the AM-Instantiate rule uses the layout A to the function argument
to update the heap and uses the B layout to produce the function’s result on the heap.
This will match the inductive predicate associated to f instantiated at the layouts A and
B, as required.
e = instA,B (f )(C e1 · · · en ). This is much like the previous case. The only difference
is that the S-Inst-Constr rule unfolds the inductive predicate IA,B (f )(C e1 · · · en ).
The resulting SSL proposition will still be satisfied by the model (σ ′ , h′ ) given by AM-
Instantiate.
e = instB,C (f )(instA,B (g)(e0 )). This case combines to instantiates together. The main
condition we need to check here is that the two instantiate applications use disjoint parts
of the heap in (σ ′ , h′ ) in AM-Instantiate.
This can be seen to be true by the fact that the resulting heap is built up out of the
subexpressions using ◦, ensuring that the parts of the heap are disjoint.
                                                                                           ◀
