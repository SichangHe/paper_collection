                                        Scope Logic: Extending Hoare Logic for Pointer
                                                    Program Verification ⋆

                                                                    ZHAO Jianhua, LI Xuandong

                                                         State Key Laboratory of Novel Software Technology
arXiv:0912.4184v1 [cs.LO] 21 Dec 2009




                                                         Dept. of Computer Sci. and Tech. Nanjing University
                                                                  Nanjing, Jiangsu, P.R.China 210093
                                                                          zhaojh@nju.edu.cn



                                                Abstract. This paper presents an extension to Hoare logic for pointer
                                                program verification. First, the Logic for Partial Function (LPF) used by
                                                VDM is extended to specify memory access using pointers and memory
                                                layout of composite types. Then, the concepts of data-retrieve functions (
                                                DRF ) and memory-scope functions (MSF) are introduced in this paper.
                                                People can define DRFs to retrieve abstract values from interconnected
                                                concrete data objects. The definition of the corresponding MSF of a
                                                DRF can be derived syntactically from the definition of the DRF. This
                                                MSF computes the set of memory units accessed when the DRF retrieves
                                                an abstract value. This memory unit set is called the memory scope of
                                                the abstract value. Finally, the proof rule of assignment statements in
                                                Hoare’s logic is modified to deal with pointers. The basic idea is that a
                                                virtual value keeps unmodified as long as no memory unit in its scope is
                                                over-written. Another proof rule is added for memory allocation state-
                                                ments. The consequence rule and the rules for control-flow statements
                                                are slightly modified. They are essentially same as their original version
                                                in Hoare logic.
                                                An example is presented to show the efficacy of this logic. We also give
                                                some heuristics on how to verify pointer programs.


                                        1     Introduction
                                        To reasoning the correctness of programs, C.A.R. Hoare presented an axiomatic
                                        system for specifying and verifying programs[1][2]. However, this logic can not
                                        deal with pointer programs because of pointer alias, i.e. many pointers may
                                        refer to the same location. A few extensions to Hoare logic have been made
                                        to deal with pointers or shared mutable data structures [3][4][5]. Among them,
                                        separation logic [6] is one of the most successful extensions. That logic uses
                                        a memory model which consists of two parts: the stack and the heap. Pointers
                                        can only refer to data objects in the heap. Separation logic extends the predicate
                                        calculus with the separation operator, which can separate the heap into different
                                        disjoint parts. Then the Hoare logic is extended with a set of proof rules for
                                        ⋆
                                            This paper is supported by the Chinese HighTech project, grant no. 2009AA01Z148;
                                            and the HGJ project, grant no. 2009ZX01036-001-001
heap lookup, heap mutation and variable assignment. Though a few programs
have been used to demonstrate the potential of local reasoning for scalability[7],
verifying programs using separation logic is still very difficult.
    This paper presents an extension to Hoare logic for verification of pointer pro-
grams. This logic uses an extension of the Logic for Partial Functions (LPF) [8]
to describe pre- and post-conditions of code fragments. Three type constructors
are introduced to construct composite types and pointer types used in programs.
Several kinds of function symbols associated with these types, together with a
set of proof rules, are introduced to model and specify the memory layout/access
in pointer programs.
    In this logic, people can define recursive functions to retrieve abstract val-
ues from interconnected concrete data objects. These functions are called data-
retrieve functions (DRFs). DRFs are recursively defined based on basic function
symbols and the memory access/layout function symbols. For each DRF f , there
is a memory-scope function M(f ) of which the definition can be constructed syn-
tactically from the definition of f . If an application of f results in an abstract
value, then an application of M(f ) to same arguments results in the set of mem-
ory units accessed during the application of f . During program executions, the
application of f to same arguments results in same abstract value as long as no
memory unit in this set is modified.
    In this logic, program specifications are of the form P ⊢ p{c}r, where P is
a set of LPF formulae (usually a set of function definitions), c is a fragment
of code, and q, r are the pre-condition and post-condition respectively. Such a
specification means that if all the formulae in P hold for arbitrary program states,
and c starts its execution from a program state satisfying q; then the state must
satisfy r when c stops.
    This paper is organized as follows. An extension to LPF is presented in
Section 2. To model memory access and layout in pointer programs, several
kinds of new function symbols and constants are introduced into LPF. A set
of proof rules are introduced to specify these function symbols and constants.
In Section 3, the concept ‘memory scope forms’ of terms and ‘memory scope
functions’ (MSFs) are introduced. A proof rule is introduced to specify how
definitions of MSFs can be constructed. A property about memory scope forms
is also given in this section. The syntax of a small program language is given
in Section 4. The semantic of this program language is also briefly described
in this section. The syntax and meaning of program specifications are given in
Section 5. The extension to Hoare logic is presented in Section 6. The proof rule
for assignment statements is modified to dealing with the pointer alias problem.
Another proof rule is introduced for memory allocation statements. Section 7
presents a formal verification of the running example in this paper. Section 8
gives some heuristics on program verifications using our logic. Section 9 concludes
this paper.
   In Appendix A, we verify another program which inserts a new node to a
binary search tree. In Appendix B, we use a simplified version of the Schorre-
Waite algorithm to show that our logic can help people think about program
verification in different abstract levels.


1.1    Preliminary of the logic for partial functions

The logic for partial functions (LPF) used in Vienna Development Method
(VDM) can reason about undefinedness, (abstract) types, and recursive partial
function definitions. The syntax of LPF terms and formulae is briefly described
here. A term of LPF can be one of the following forms:

1. a variable symbol;
2. f (e1 , . . . , en ) if f is a function symbol, arity(f ) = n and e1 , . . . , en are terms,
3. p ? e1 : e2 , where p is a formula.

A formula of LPF can be one of the following forms:

1. a boolean-typed term,
2. ⊛; (⊛ denotes the neither-true-nor-false value. It is originally represented
   by the symbol ∗ in LPF papers, but ∗ is used to denote the memory access
   function in this paper.)
3. P (e1 , . . . , en ), if P is a predicate symbol and arity(P ) = n, and e1 , . . . , en
   are terms. In this paper, we view a predicate symbol as a boolean-typed
   function symbol.
4. e1 = e2 , where e1 , e2 are terms,
5. e : t, where e is a term and t is a type symbol.
6. ∆A, ¬A, A1 ∧ A2 are formulae if A, A1 , A2 are formulae.
7. ∀x : t · A, where x is a variable, t is a type symbol, and A is a formula.
8. f (x1 : T1 , . . . , xn : Tn ) , e, where e is a term, and all the free variables in t
   are in the set {x1 , . . . , xn }.

For the proof rules, semantics and other detail information of LPF, we refer
readers to [8].
    The LPF formulae used in our logic have a constraint: the logical connectives,
⊛, ∆ and quantifiers can not occur in a term. Specifically, in a conditional form
p?e1 : e2 , p contains no logical connective and quantifier. However, we can use
some operators like cand, cor, . . ., in terms. These operators can be defined
using conditional forms. This constraint makes it possible to define the memory
scope form of terms.


2     The extension of the logic for partial functions

In this paper, LPF is extended to deal with issues about memory access/layout,
composite and pointer program types, data-retrieve functions and memory-scope
functions. Now we first extend LPF with program types and associated function
symbols.
2.1    Program types and associated function symbols

In LPF, a type can be either a basic type such as integer and boolean, or a type
constructed using type constructors such as SetOf, SeqOf and Map. However,
the abstract types constructed using these type constructors can not be used
directly in imperative programs. To deal with types appeared in programs, we
introduce three new type constructors into LPF: pointer (P), array (ARR), and
record (REC). We call the types that can appear in programs as P-types.

 1. integer and boolean are P-types;
 2. Let t, t1 , . . . , tk be P-types, n1 , n2 , . . . , nk are k different names, c is an pos-
    itive integer constant. P(t), ARR(t, c), and REC((n1 , t1 ) × . . . × (nk , tk ))
    are also P-types.

We allow a record type t has one or more fields with type P(t) such that we can
deal with recursive data types in our program language. We use Ptr as the super
type of all pointer types P(t), where t is a P-type. The abstract type constructors
Map, SetOf, SeqOf can not be applied to composite program types. However,
these type constructors can be applied to pointer types to form new abstract
types. That is, we can get an abstract SetOf(P(t)) for some P-type t, but can
not get an abstract type SetOf(Rec((n1 , t1 ) × . . . × (nk , tk )).
    The following constant and function symbols associated with P-types are
introduced.

 1. A program can declare a finite set of program variables with P-types. For
    each program variable v declared with P-type t, &v is a constant with type
    P(t).
 2. For each pointer type t, there is a t-typed constant nilt . The type subscript
    t can be omitted if there is no ambiguity caused.
 3. A partial function ∗ : Ptr → Ptr ∪ integer ∪ boolean. We write an ap-
    plication of ∗ to e as ∗e. For a non-nil pointer r with type P(t), where t is
    integer, boolean or a pointer type, ∗r is a t-typed value. An application of
    this function symbol models a memory unit access.
 4. For each array type t = ARR(t′ , c), there is a partial function &[]t : P(t) ×
    integer → P(t′ ). We write an application of such function as &e[i]t instead
    of &[]t (e, i). The type subscripts can be omitted if there is no ambiguity
    caused. These function symbols model the memory layout of array types.
    Intuitively speaking, if e is a non-nil reference to a t-typed data object, &e[i]
    is the reference to the ith element. &e[i] is defined if and only if e 6= nil and
    0 ≤ i < c.
 5. For each record type t = REC((n1 , t1 ) × . . . × (nk , tk )) and a name ni
    (1 ≤ i ≤ k), we have a partial function &→t ni : P(t) → P(ti ). It is only
    undefined on the constant nilt . We write an application of this function
    symbol to e as &e →t ni . The type subscript t can be omitted if there is
    no ambiguity caused. These functions model memory layout of record types.
    Intuitively speaking, if e is a non-nil reference to a record-typed data object,
    &e →t ni is the reference to the field ni .
   The above function (and constant) symbols can be used in both programs
and specifications. For conciseness, we use the following abbreviations.

1. Let v be a program variable declared with type integer, boolean or a
   pointer type, v is an abbreviation for ∗(&v).
2. For a program variable v declared with an array type ARR(t, c), and t is
   integer, boolean, or a pointer type, we use v[e] as an abbreviation for
   ∗(&(&v)[e]).
3. If e is of type P(t), t is a record type of which n is a field name, and the
   field type is integer, boolean or a pointer type, we can use e → n as an
   abbreviation for ∗(&e → n).
4. Let v be a program variable declared with a record type of which n is a field
   name, the field type is integer, boolean or a pointer type, we can use v.n
   as an abbreviation for ∗(&(&v) → n).


2.2   The proof rules about memory access and layout

In this subsection, we present some proof rules to specify memory unit access
and memory layout of composite types. We define an auxiliary function Block :
Ptr → SetOf(Ptr) to denote the set of memory units in a memory block. The
definition of Block is as follows.
Block(r) = ∅ if r = nil. Otherwise Block(r) =
 
 S                              {r} if ∗r is of type integer, boolean or Ptr
                      Block(&r →  n) if r : P(t) and t is a record type
  n: field name ofStc−1
                     i=0 Block(&r[i]) if r : P(ARR(t′ , c)) for some t′

Intuitively speaking, Block(r) is the set of memory units in the memory block
referred by r.
    The rule MEM-ACC says that if r denotes a non-nil pointer referring to a
memory unit storing basic type values or pointer values, ∗r denotes a basic type
value or a pointer value respectively.

                     r : P(t) r 6= nil
   MEM-ACC                               t is integer, boolean, or P(t′ ) for some t′
                          ∗r : t


   The rule MEM-BLK specifies how memory blocks are allocated. Given two
arbitrary different memory blocks, they are either disjoint with each other, or
one is contained by the other.
                                 p : Ptr q : Ptr p 6= q
           MEM-BLK
                                Block(p) ∩ Block(q) = ∅∨
                        Block(p) ⊂ Block(q) ∨ Block(q) ⊂ Block(p)
    The following two rules specify how the memory blocks are allocated for de-
clared program variables. The rule PVAR-1 says that for each program variable,
a memory block with corresponding type is allocated. Furthermore, this block
is not a sub-block of any other memory block. The rule PVAR-2 says that each
program variable is allocated a separate memory block.


 PVAR-1                                           v is a program declared with type t.
                &v : P(t) ∧ &v 6= nil∧
           ∀x : Ptr · Block(&v) 6⊂ Block(x)


       PVAR-2                        v1 , v2 are two different program variables
                   &v1 6= &v2


    The following two rules specify the memory layout for record-typed memory
blocks. The rule RECORD-1 says that a record-typed memory block is allocated
as a whole, i.e. when a record-typed memory block is allocated, all the memory
blocks for its fields are also allocated. The rule RECORD-2 says that the memory
blocks allocated for the fields are disjoint with each other.
                             r : P(REC(. . . × (n, t) × . . .)) r 6= nil
            RECORD-1
                                 (&r → n : P(t)) ∧ (&r → n 6= nil)




                   r : P(REC(. . . × (n1 , t1 ) × . . . × (n2 , t2 ) × . . .)) r 6= nil
   RECORD-2
                           Block(&r → n1 ) ∩ Block(&r → n2 ) = ∅


   The following two rules specify the memory layout for array-typed memory
blocks. The rule ARR-1 says that an array-typed memory block is allocated as
a whole, i.e. when an array-typed memory block is allocated, all of the memory
blocks for its elements are allocated. The rule ARR-2 says that the memory
blocks allocated for different elements are disjoint with each other.
                          r : P(ARR(t, c)) r 6= nil 0 ≤ i < c
              ARR-1
                               (&r[i] : P(t)) ∧ (&r[i] 6= nil)




                r : P(ARR(t, c)) r 6= nil 0 ≤ i < c 0 ≤ j < c                i 6= j
      ARR-2
                         Block(&r[i]) ∩ Block(&r[j]) = ∅
2.3    The interpretation of P-types and new function symbols

Please be noticed that the types of the constant symbols (&v, nilt ) introduced
in this section are integer, boolean, or pointer types. The argument types and
result types of the function symbols introduced in this section are also integer,
boolean, and pointer values. So the terms in our logic do not denote array or
record P-type values. Thus structures for our logic does not have to interpret
record and array types.
    For each P-type t, (P(t))A is a countable infinite set in the universal domain
U satisfying that (nilP(t) )A ∈ (P(t))A . Furthermore, it is required that for
  A

different P-types t1 and t2 , (P(t1 ))A and (P(t2 ))A are disjoint. PtrA is the
union of all such sets.
    The function symbols & → n and &[ ] model the memory layout of records and
arrays respectively. As we do not go into details about memory layout of com-
posite types, we just requires that all the proof rules in the previous subsection
are satisfied by the interpretation of these function symbols.
    The function symbol ∗ models program states. Its interpretation must satisfy
that ∗A (x) ∈ tA if x ∈ (P(t))A and x 6= (nilP(t) )A , where t is integer, boolean,
or P(t′ ) for some t′ ; ∗A (x) = ⊥ otherwise.


3     Memory scope functions

In LPF, a formula f (x1 , . . . , xn ) , e defines a function denoted by f . People can
define data-retrieve functions using such formulae. In definitions for DRFs, we
require that for any conditional sub-term e0 ?e1 : e2 of e, none of the function
symbols occurred in e0 is defined (directly or indirectly) based on f . So for each
DRF definition f (x1 , . . . , xn ) , e, e is continuous in f , thus we can use the proof
rule Func-Ind in [8] to prove properties about DRFs.
    Given an LPF term e, the memory scope form of e, denoted as M(e), is
defined as follow.

 1. If e is a variable, M(e) is ∅.
 2. If e is of the form f (e1 , . . . , en ), M(e) is M(e1 )∪. . .∪M(en )∪M(f )(e1 , . . . , en ),
    where M(f ) represents the MSF symbol of f , which is defined as follow
      – If f is a function symbol associated with basic types or abstract types
         (for example, +, −, ×, /, >, <, ∈, ⊆ . . .), M(f ) is defined as the constant
         ∅.
      – If f is & → n, &[ ], &v for some program variable, nilt for some type t,
         M(f ) is defined as the constant ∅.
      – If f is the memory access function ∗ introduced in sub-section 2.1, M(∗)
         is defined as M(∗)(x) , x.
      – For any other function symbols, M(f ) represents a new function symbol
         denoting the memory scope function of f .
 3. If e is of the form e0 ?e1 : e2 , M(e) is M(e0 ) ∪ (e0 ?M(e1 ) : M(e2 )).
  Given a DRF f defined as f (x1 , . . . , xn ) , e, the memory scope function
M(f ) of f is defined as

                                 M(f )(x1 , . . . , xn ) = M(e)

Formally, it is expressed using the following proof rule.

                                               f (x1 , . . . , xn ) , e
                   SCOPE-FUNC
                                             M(f )(x1 , . . . , xn ) , M(e)
Please be noticed that for any sub-term e0 ?e1 : e2 of M(e), no function symbol
is recursively defined based on M(f ).

Definition 1. We say a structure A with signature Σ conforms to a set of func-
tion definitions P iff for each definition f (x1 , . . . , xn ) , e in P, [[f (x1 , . . . , xn ) ,
e]]A
   α is T , here α is the assignment of A.

The structure A conforms to P means that A interprets the defined function
symbols according to their definition in P.
    In our logic, the function symbol ∗ is used to model program states. The
DRFs used to retrieve abstract values are defined on ∗. One of the basic ideas of
our logic is that the abstract values retrieved by these functions keep unchanged
if no memory unit in their memory scopes is over-written during a program
execution. We have the following lemma and theorem about MSFs and memory
scope forms of terms.

Lemma 1. Let P be a set of recursive function definitions. Let A and A′ be
two structures. They both conform to P and are identical except that they may
have different interpretations for ∗ and for the function symbols defined in P.
Let e be a term satisfying that all function symbols in e are either defined in P,
or associated with basic types, abstract types or P-types. We have that [[e]]A   α =
       ′
                                   A′                                   A′
[[e]]A
     α   and [[M(e)]] A
                      α = [[M(e)]] α  if [[M(e)]] A
                                                  α 6
                                                    = ⊥ and ∗ A
                                                                (x) = ∗    (x) for all
x ∈ [[M(e)]]A α .

Proof. By induction, we first prove that the conclusion holds when e contains
no function symbol defined in P.
BASE: The conclusion holds if e is a variable or a constant symbol.
INDUCTION: Assuming the conclusion holds for all terms shorter than e.
                            A′                        A′
We prove that [[e]]A                      A                        A
                   α = [[e]]α and [[M(e)]]α = [[M(e)]]α if [[M(e)]]α 6= ⊥ and
            ′
 A        A                       A
∗ (x) = ∗ (x) for all x ∈ [[M(e)]]α .

 – If e is of the form f (e1 , . . . , en ), here f is a function symbol other than ∗,
   and f is not defined in P. M(e) is M(e1 ) ∪ . . . ∪ M(en ) because M(f ) is ∅.
                                            A′
   So [[M(ei )]]A                A
                   α 6= ⊥ and ∗ (x) = ∗ (x) for all x ∈ [[M(ei )]]
                                                                          A
                                                                          α for i = 1, . . . , n.
                                                                       A′
   According to the inductive assumption, [[ei ]]α = [[ei ]]α and [[M(ei )]]A
                                                             A
                                                                                          α =
               ′
                                                     A′                            A′
   [[M(ei )]]A
             α′  . It  follows that [[e]] A
                                          α =  [[e]] α  and [[M(e)]] A
                                                                     α =  [[M(e)]] α  because
   fA = fA .
 – If e is of the form ∗e1 . M(e) is defined as {e1 } ∪ M(e1 ). So [[M(e1 )]]A               α 6= ⊥
                          ′
   and ∗A (x) = ∗A (x) for all x ∈ [[M(e1 )]]A             α  . From   the inductive  assumption,
                                          A′                                 A′
   we have that [[e1 ]]A                                       A
                             α = [[e1 ]]α and [[M(e1 )]]α = [[M(e1 )]]α . Because          [[e1 ]]A
                                                                                                  α ∈
                                                                                      A′         ′
   [[M(e)]]α if [[M(e)]]α is not ⊥, we have [[e]]α = ∗ ([[e1 ]]α ) = ∗ ([[e1 ]]A
             A                A                                 A      A      A
                                                                                              α ) =
          ′
                                             A′
   [[e]]A
        α   and   [[M(e)]]  A
                            α   =   [[M(e)]] α  .
 – If e is of the form e0 ?e1 : e2 . M(e) is M(e0 ) ∪ (e0 ?M(e1 ) : M(e2 )). From the
                                                                   A′                              A′
   inductive assumption, we have [[e0 ]]A          α = [[e
                                                                                   A
                                                               0 ]]α and [[M(e0 )]]α = [[M(e0 )]]α .
               ′                                            ′
   So [[e0 ]]A                      A
             α = T iff [[e0 ]]α = T . When         [[e0 ]]A           A
                                                          α = [[e′0 ]]α = T , we have   [[M(e)]]A α =
                                                A′                              A′
   [[M(e0 )]]α ∪ [[M(e1 )]]α , [[M(e)]]α = [[M(e0 )]]α ∪ [[M(e1 )]]α , [[e]]A
              A                    A                                A
                                                                                        α  = [[e1 ]]A
                                                                                                    α
                ′             ′
   and [[e]]Aα     = [[e1 ]]A
                            α   . From the inductive assumption, we have that [[e]]A             α  =
          ′                                     ′
                                                                                             A′
   [[e]]A
        α and [[M(e)]]α =
                            A
                                      [[M(e)]]A                                     A
                                              α . We can also prove that [[e]]α = [[e]]α and
                                 ′
   [[M(e)]]A                  A                  A
             α = [[M(e)]]α when [[e0 ]]α is F or N .

    Second, we prove that the conclusion holds if no function symbol defined in
P is (directly or indirectly) recursively defined on itself. We give a rank to each
term and each function symbol. The rank of a term e is the highest rank of the
function symbols occur in e. The ranks of function symbols associated with basic
types and abstract types are 0. The function symbols ∗, & → n, &[] also have
rank 0. The rank of a function symbol f defined as f (x1 , . . . , xn ) , er in P is
the rank of er plus 1. As no function symbol is recursively defined, each function
symbol and term has a rank. Now, the conclusion is proved by an induction on
the ranks and the lengthes of terms.
BASE: According to the conclusion of the first step, this conclusion holds for
0-rank terms with any length.
INDUCTION: Let e be a k-rank term. If the conclusion holds for all terms
either with a rank less than k, and all k-rank terms shorter than e.
 – If e is of the form f (e1 , . . . , en ) and f is a function symbol with a rank non-
   greater than k, and defined as f (x1 , . . . , xn ) , er . Then the rank of er is less
   than or equal to k − 1. As all the function-definition formulae in P are inter-
   preted to T , according to the semantic model of function definitions of LPF,
                                                               A′
   both [[f (e1 , . . . , en )]]A
                                α and [[f (e1 , . . . , en )]]α are     ⊥ if some of [[ei ]]A
                                                                                            α is′ ⊥. Oth-
                                                                    A′
   erwise, [[f (e1 , . . . , en )]]α and [[f (e1 , . . . , en )]]α are [[er ]]A
                                   A
                                                                               α′  and   [[e     A
                                                                                             r ]]α′ respec-
                                               A                        A
   tively, where α = α(x1 → [[e1 ]]α ) . . . (xn → [[en ]]α ), i.e. α is same as α except
                        ′                                                        ′
                                                                                                       A′
   that α′ maps xi to [[ei ]]A                                        A
                                    α ;′ [[M(f )(e1 , . . . , en )]]α and [[M(f )(e1 , . . . , en )]]α are
             A                      A
   [[M(er )]]α′ and [[M(er )]]α′ respectively. Because [[M(f )(e1 , . . . , en )]]α ⊆ [[e]]A     A
                                                                                                            α,
   we have ∗A (x) = ∗A (x) for all x ∈ [[M(f )(e1 , . . . , en )]]A               α  =  [[M(e      )]]
                                                                                                  r α
                                                                                                       A
                                                                                                        ′ . As
   the rank of er is less than or equal to k − 1, from the inductive assumption,
                                   A′                                       A′                       A′
   we have [[er ]]A                                        A                           A
                    α′ = [[er ]]α′ and [[M(er )]]α′ = [[M(er )]]α′ , i.e. [[e]]α = [[e]]α and
                                                                     ′
                                                                                                      A′
   [[M(f )(e1 , . . . , en )]]A
                              α = [[M(f       )(e1 , . . . , en )]]A               A
                                                                   α . So [[M(e)]]α = [[M(e)]]α be- ′
                                            ′
   cause [[M(ei )]]A                      A                                  A
                      α = [[M(ei )]]α and [[M(f )(e1 , . . . , en )]]α = [[M(f )(e1 , . . . , en )]]α .
                                                                                                             A

 – If e is a conditional form with a rank k, the proof is similar to those of the
   first step.
    Now we are about to prove the general case. For each function symbol f recur-
sively defined in P, we introduce infinite number of function symbols f0 , f1 , . . ..
For the definition of f , i.e. f (x1 , . . . , xn ) , e, we introduce a set of definitions
fi (x1 , . . . , xn ) , ei for i = 1, 2, . . ., where ei is derived by replacing each func-
tion symbol g recursively defined in P by gi−1 (Here g can be f ) in e. We also
introduce a function definition f0 (x1 , . . . , xn ) = ⊛ for each f0 . Notice that fi s
are not recursively defined. Furthermore, M(ei ) is same as the term derived by
replacing g and M(g) respectively by gi−1 and M(gi−1 ) in M(e). Because it is
required that for each definition f (x1 , . . . , xn ) = e in P, e is continuous in f ,
we have that fi is less defined than fi+1 , i.e. fi+1 (x1 , . . . , xn ) = fi (x1 , . . . , xn ) if
fi (x1 , . . . , xn ) is defined for any x1 , . . . , xn . Because M(e) is continuous in M(f ),
we have that M(fi )A is less defined than M(fi+1 ). So f A is the least upper-bound
of the function sequence f0A , f1A , . . ., and M(f )A is the least upper-bound of the
function sequence M(f0 )A , M(f1 )A , . . .. Let e be a term containing recursively
defined function symbols. If [[e]]A     α is not ⊥, there must be a large-enough integer
i such that [[ei ]]A            A                 A         A
                       α = [[e]]α and [[M(ei )]]α = [[e]]α , where ei is derived by replacing
each recursively defined function symbol g by gi−1 . As ei contains no recursively
defined symbols, according to the second conclusion, we have that this lemma
holds in general.                                                                          QED


   The following theorem 1 gives a sufficient condition under which an LPF
formula p keeps unchanged before/after some memory units are modified. A
term occurs in p is called a top-level one if it is not a sub-term of another term
occurs in p.

Theorem 1. Let P be a set of recursive function definitions. Let A and A′ be
two structures. They both conform to P and are identical except that they may
have different interpretations for ∗ and for the function symbols defined in P.
Let p be an LPF formula satisfying that

 – all function symbols in p are either defined in P, or associated with basic
   types, abstract types, or P-types, and
 – p has no sub-formula of the form f (x1 , . . . , xn ) , er .
                                 ′                                             ′
We have that [[p]]A         A            A             A        A
                   α = [[p]]α if [[M(e)]]α′ 6= ⊥ and ∗ (x) = ∗ (x) for all x ∈
        A
[[M(e)]]α′ for each top-level term e of p, and arbitrary assignment α′ .

Proof. This theorem can be proved by an induction on the structure of p.
BASE:

 – If p is of the form f (e1 , . . . , en ), and f is a boolean-typed function sym-
   bol (or a predicate symbol). p itself is the only top-level term of p. From
                              A′
   Lemma 1, [[p]]A   α = [[p]]α .
                                                                      A′
 – If p is of the form e1 = e2 . From Lemma 1, [[ei ]]A    α = [[ei ]]α for i = 1, 2. So
                   ′
   [[p]]A        A
        α = [[p]]α .
                                                                  A′               ′
 – If p is of the form e : t. From Lemma 1, [[e]]A       α = [[e]]α and t
                                                                           A
                                                                              = tA . So
                   ′
   [[p]]A        A
        α = [[p]]α .

INDUCTION:
 – If p is of the form ∀x : t·p′ . A top-level term of p is also a top-level term of p′ .
   From the inductive assumption, for an assignment α(x → v) for an arbitrary
                                         ′ A′
   t-typed value v, [[p′ ]]A
                           α(x→v) = [[p ]]α(x→v) . According to the interpretation
                                                         ′
   rule for ∀x : t · p′ , we conclude that [[p]]A        A
                                                α = [[p]]α .
 – The conclusion can also be proved when p is of the form ∆p′ , ¬p′ , and p1 ∧p2 .

                                                                                  QED



4     Syntax of programs

The small program language used in this paper is strong typed. Each expression
in the programs has a static P-type. An expression e has a static P-type t means
that at the runtime, either e denotes a value of type t or e is non-denoting. The
argument types and result types of function symbols appeared in programs are
definitely specified. The static types of expressions can be decided statically and
automatically. It also can be statically checked (by a compiler, for example) that
each function symbol is applied to arguments with suitable static types. In this
paper, it is supposed that all programs under verification have passed such static
type check.


4.1   The syntax of program expressions

A program expression is an LPF term with following restrictions.

 1. A program expression contains no free variable. Be noticed that a program
    variable v occurs in a term is in fact an abbreviation for ∗(&v).
 2. Only the following function (predicate) symbols can occur in program ex-
    pressions.
    (a) Constant symbols for basic types (integer, boolean), nilt for type t,
        &v for a program variable v;
    (b) Function symbols associated with integer and boolean, like +, −, ∗, ÷, <
        , ≤, =, . . .;
    (c) Memory access/layout function symbols ∗, & → n, &[ ];
    (d) Boolean functions not, cand, cor which are defined using conditional
        forms as follows.
           i. not x , x?false : true
          ii. x cand y , ¬x?false : y
        iii. x cor y , x?true : y.

We define these boolean operators because the semantic of logical connectives ∧
and ∨ of LPF is different from that of the logical operators commonly used in
program languages.
4.2   The syntax of program statements
The syntax of program statements is as follows.
                st ::= skip | ∗ e1 := e2 | ∗ e := alloc(t)
                       | st; st | if (e) st else st
                       | while (e) st
This programming language has two kinds of primitive statements: assignment
statements and memory-allocation statements.
 – An assignment statement ∗e1 := e2 first evaluates e1 and e2 , then assigns
   the value of e2 to the memory unit referred by the value of e1 . The values
   stored in other memory units keep unchanged. It is required that ∗e1 and e2
   has same static type, which is limited to be integer, boolean, or a pointer
   type.
 – A memory-allocation statement ∗e := alloc(t) allocates a memory block of
   type t, and assigns the reference to this memory block to the memory unit
   referred by the value of e. Furthermore, in the new memory block, all the
   memory units storing pointer values are initialized to nil. It is required that
   the static type of ∗e is P(t).
    The semantics of the composite statements st; st, if (e) st else st, and
while (e) st are same as those commonly used in real program languages. It
is required that in if (e) st else st and while (e) st, the static type of e must
be boolean.
Example 1. The program depicted in Figure 1 is a running example used in
this paper. The type of the program variables k and d is integer. The type of
program variables root and p is P(T ), where T is REC((l, P(T )) × (r, P(T )) ×
(K, integer) × (D, integer)). This program first searches a binary search tree
for a node of which the field K equals k. Then it sets the filed D of this node
to d. Please be noticed that p, root, k, d, p → K, p → D, p → l, p → r
are respectively abbreviations for ∗(&p), ∗(&root), ∗(&k), ∗(&d), ∗(&p → K),
∗(&p → D), ∗(&p → l), ∗(&p → r).



                p:=root;
                while (p → K 6= k)
                {
                      if (k < p → K ) p := p → l else p := p → r;
                }
                p → D := d;



               Fig. 1. The program used as a running example
5     Syntax of specifications
A program specification is of the form P ⊢ q{c}r, where c is a program, P is a set
of LPF formulae, q and r are LPF formulae satisfying the following conditions.
 – They contain only function symbols defined in P, the function symbols which
   can occur in program expressions, and the function symbols associated with
   abstract types.
 – q and r contains no sub-formula of the form f (x1 , . . . , xn ) , e.
The formula set P is called the premise of this specification. P usually contains a
set of function definitions. The formulae q and r are respectively called the pre-
condition and post-condition. Intuitively speaking, such a specification means
that if all the formulae in P hold for arbitrary program states, and the program
c starts its execution on a state satisfying q, then the state satisfies r when the
program c stops.
Example 2. Let P be the set of formulae depicted in Figure 2. These formulae
define a set of data retrieve functions. The boolean function InHeap is defined in
sub-section 6.3. InHeap(x) means that x refers to a memory block disjoint with
all memory blocks for program variables. Let

              q = isHBST(root) ∧ Map(root) = M ∧ k ∈ Dom(root)

                  r = isHBST(root) ∧ Map(root) = M †{k 7→ d}
P rog is the program depicted in Figure 1. The specification P ⊢ q{P rog}r says
that if the program state satisfies the following conditions when {P rog} starts.
 1. The value of root points to the root node of a binary search tree stored in
    the heap;
 2. The tree represents a finite map M from integer to integer;
 3. The value stored in k is in the domain of this map,
When P rog stops, root still points to the root node of the binary search tree, and
now the finite map represented by the binary search tree becomes M †{k 7→ d}.


6     Proof rules of program statements
In this section, we present the proof rules for program statements. There are
three rules for primitive statements, one rule for consequences, and three rules
for control flow statements.

6.1    The proof rule for skip statement
The skip statement changes nothing, so we have the following proof rule.

                      SKIP-ST
                                       ∅ ⊢ q{skip}q
NodeSet(x) : P(T ) → SetOf(Ptr)
     , (x = nil)? ∅ : ({x} ∪ NodeSet(x → l) ∪ NodeSet(x → r))

Map(x) : P(T ) → Map integer to integer
     , (x = nil)?∅ : {x → K 7→ x → D}†Map(x → l)†Map(x → r)

MapP(x, y) : P(T ) × P(T ) → Map integer to integer
    , (x = nil)?∅ : MapP(x → l)†MapP(x → r)†
           ((x = y)?∅ : {x → K 7→ x → D})

Dom(x) : P(T ) → SetOf(integer)
    , (x = nil)?∅ : ({x → K} ∪ Dom(x → l) ∪ Dom(x → r))

isHBST(x) : P(T ) → boolean
     , (x = nil)?true : InHeap(x) ∧ isHBST(x → l) ∧ isHBST(x → r)∧
                  (Dom(x → l) = ∅?true : MAX(Dom(x → l)) < x → K)∧
                  (Dom(x → r) = ∅?true : x → K < MIN(Dom(x → r)))



             Fig. 2. The definitions of a set of data retrieve functions


6.2    The proof rule for assignment statements
Let q be an LPF formula and x be the only free variable in q. Let t be the static
type of ∗e1 and e2 . The type t must be integer, boolean, or P(t′ ) for some t′ .
We have the following proof rule for assignment statements.


                P, q[e2 /x] ⊢ e1 6= nil ∧ e1 6∈ M(e1 ) ∧ e2 : t
                P, q[e2 /x] ⊢ e1 6∈ M(e)[e2 /x] for each top-level term e of q
      ASSIGN-ST
                                P ⊢ q[e2 /x]{∗e1 := e2 }q[∗e1 /x]

Here, it is required that all bounded variables in q are different from x. A term
e of q is called a top-level one if it is not a sub-term of another term of q.
Furthermore, it is required that for each conditional term e0 ?e1 : e2 of q, e0 is a
boolean-typed term, so we can construct a memory form of each top-level term
of q.
    Now we briefly prove the soundness of this rule. We can use two structure
A and A′ to denote the program states before/after the assignment statement.
A and A′ are only different in the interpretations of the function symbol ∗ and
the symbols defined in P. The semantic of an assignment ∗e1 = e2 is as fol-
low. It first evaluates the value of e1 and e2 , i.e. [[e1 ]]A               A
                                                                α and [[e2 ]]α , then the
                                                     A                 A
content of the memory unit referred by [[e1 ]]α is set to [[e2 ]]α . Formally, we
       ′
                                                A′
say ∗A ([[e1 ]]A            A        A                                 A
               α ) = [[e2 ]]α , and ∗ (x) = ∗ (x) for all x 6= [[e1 ]]α . ′According to
Lemma 1, the condition e1 6∈ M(e1 ) assures that [[e1 ]]α = [[e1 ]]A
                                                               A                       A
                                                                         α , so [[e2 ]]α =
 A′       A       A′      A′            A′
∗ ([[e1 ]]α ) = ∗ ([[e1 ]]α ) = [[∗e1 ]]α . The condition e1 6= nil ∧ e2 : t assures that
both [[∗e1 ]]A            A
             α and [[e2 ]]α are not ⊥. Together with these conditions, the condition
e1 6∈ M(e)[e2 /x] assures that for each top-level term e, [[e1 ]]A                   A
                                                                 α 6∈ [[M(e)[e2 /x]]]α ,
                             A                                          A
which equals to [[M(e)]]α(x→[[e2 ]]A ) . From Lemma 1, we have [[e]]α(x→[[e2 ]]A ) =
                                       α                                                 α
      ′                  ′                                                          ′
[[e]]A                     A                                        A                A
     α(x→[[e2 ]]A ) = [[e]]α(x→[[∗e ]]A′ ) . So we have [[e[e2 /x]]]α = [[e[∗e1 /x]]]α . As α is
              α                 1 α
                                                                          ′
arbitrary, according to Theorem 1, [[q[e2 /x]]]A                A
                                               α = [[q[∗e1 /x]]]α . So we conclude
that if q[e2 /x] holds before the assignment statement, q[∗e1 /x] holds after.

6.3       The proof rule for memory allocation statements
The memory allocation statement ∗e = alloc(t) first evaluates e, then allocates
an unused memory block and assigns the reference to this block to the memory
unit referred by e. All the memory units storing pointer values are initialized
to nil. This block can not be referred by any pointers stored somewhere before
this allocation. Furthermore, this block is disjoint with all of the memory blocks
allocated for program variables. It is required that the static type of ∗e must be
P(t). Let p be an LPF formula containing no free variable, we have the following
proof rule for memory allocation statements.


                      P ∧ q ⊢ e 6= nil ∧ e 6∈ M(e)
                      P ∧ q ⊢ e 6∈ M(e′ ) for each top-level term e′ of q
           ALLOC-ST                                                      
                                             q ∧ InHeap(∗e) ∧ Unique(e)
                    P ⊢ q {∗e = alloc(t)}
                                             ∧PtrInit(∗e) ∧ (∗e 6= nil)

The predicts Unique, InHeap, and PtrInit are defined as follows.

Unique(x) , ∀y : Ptr·((y 6= x∧y 6= nil∧∗y : Ptr) ⇒ Block(∗y)∩Block(∗x) = ∅)
                              ^
      InHeap(p) ,                           (Block(&v) ∩ Block(p) = ∅)
                   x is a program variable.

   PtrInit(p) , ∀x : Ptr · ((x ∈ Block(p) ∧ x 6= nil ∧ ∗x : Ptr) ⇒ ∗x = nil)
Intuitively speaking, Unique(p) says that the memory block referred by the ref-
erence stored in p can not be accessed by references stored elsewhere. InHeap(p)
says that the memory block referred by p is disjoint with all the memory blocks
for program variables. PtrInit(p) says that all memory units with pointer types
in the memory block referred by p store nil pointers.
    Similarly to the soundness reasoning for the rule ASSIGN-ST, we can con-
clude that q still holds after the allocation statement if it holds before. Because
the allocated memory block is unused, it can not be accessed by any point-
ers stored somewhere before this memory allocation. This allocation statement
assigns the reference to this block only to the memory unit referred by e. So
Unique(e) holds after this allocation statement. The new allocated block is dis-
joint with any blocks for program variables. So InHeap(∗e) holds after this allo-
cation statement. The post condition PtrInit(∗e) holds because the new block
is initialized as described above. So we conclude that this proof rule is sound.
6.4   The consequence rule and the rules for control flow statements

The following proof rules are essentially the same as those presented in [1].
The consequence rule is slightly modified such that the premise of a verified
assertion can be strengthened. The rules for if-statement and while-statement
are modified such that the pre-condition ensures that the condition expression
e is evaluated to either T or F .

                        P ⊢ q{s}r       Q⊢P       P, q ′ ⊢ q    P, r ⊢ r′
           CONSEQ
                                         Q ⊢ q ′ {s}r′




                                  P ⊢ q{s1 }r    P ⊢ r{s2 }r′
                    SEQ-ST
                                       P ⊢ q{s1 ; s2 }r′




                 P, q ⊢ e ∨ ¬e      P ⊢ (q ∧ e){s1 }r P ⊢ (q ∧ ¬e){s2 }r
        IF-ST
                                 P ⊢ q{ if (e) s1 else s2 }r




                                   P, q ⊢ e ∨ ¬e  P ⊢ (q ∧ e){s}q
                WHILE-ST
                                   P ⊢ q{ while (e) s }q ∧ ¬e


7     Verifying the running example

In this section, we verify the program depicted in Figure 1.


7.1   The DRFs, MSFs and their properties.

Example 3. Figure 2 shows the data-retrieve functions for specifying and veri-
fying the program depicted in Figure 1. From the proof rule SCOPE-FUNC in
Section 3, we can derive the definitions of all corresponding MSFs. The defini-
tions of MSFs depicted in Figure 3 are simplified but equivalent to those derived
directly by the rule SCOPE-FUNC. For conciseness, we write M(NodeSet) as
NSm , M(Map) as MPm , M(MapP) as MPPm , M(Dom) as DMm , M(isHBST) as
HBSTm . Some properties about these DRFs and MSFs are depicted in Figure 4.
These properties can be proved in the extended LPF.
NSm (x), (x = nil)? ∅ : ({&x → l, &x → r} ∪ NSm (x → l) ∪ NSm (x → r))

MPm (x) , (x = nil)?∅ :
       {&x → l, &x → r, &x → D, &x → K} ∪ MPm (x → l) ∪ MPm (x → r)

MPPm (x, y) , (x = nil)?∅ :
       {&x → l, &x → r} ∪ MPPm (x → l) ∪ MPPm (x → r)∪
       ((x = y)?∅ : {&x → K, &x → D})

DMm (x) , (x = nil)?∅ : ({&x → K, &x → l, &x → r} ∪ DMm (x → l) ∪ DMm (x → r))

HBSTm (x) , (x = nil)?∅ : {&x → l, &x → r} ∪ HBSTm (x → l) ∪ HBSTm (x → r)∪
       DMm (x → l) ∪ (Dom(x → l) = ∅?∅ : {&x → l} ∪ {&x → K} ∪ DMm (x → l))∪
       DMm (x → r) ∪ (Dom(x → r) = ∅?∅ : {&x → r} ∪ {&x → K} ∪ DMm (x → r)))



                         Fig. 3. The definitons of MSFs




                 P, isHBST(x) ⊢ &p 6∈ HSBTm (x) ∪ MPm (x) ∪ DMm (x)              (1)

             P, isHBST(x) ⊢ &p → D 6∈ HSBTm (x) ∪ MPPm (x, p) ∪ DMm (x)          (2)

              P, isHBST(x), y ∈ Dom(x), y < x → K ⊢ y ∈ Dom(x → l)               (3)

              P, isHBST(x), y ∈ Dom(x), y > x → K ⊢ y ∈ Dom(x → r)               (4)

     P, isHBST(x), y ∈ NodeSet(x) ⊢ Map(x) = MapP(x, y)†{y → K 7→ y → D}         (5)

                   P, NodeSet(x) : SetOf(Ptr) ⊢ x ∈ NodeSet(x)                   (6)

                Fig. 4. Some properties about DRFs and MSFs
7.2   Verifying the program
In this section, we will prove that if root points to a binary search tree, and we
view this binary tree as a finite map, and k is in the domain of this map, the
program depicted in Figure 1 set the co-value of k to d. In this section, we use
P to denote the set of the function definitions in Figure 2. The specification is
as follow.
      P ⊢ PRE-COND {Prog} isHBST(root) ∧ Map(root) = M †{k 7→ d}

Here, PRE-CON is the abbreviation for isHBST(root) ∧ Map(root) = M ∧ k ∈
Dom(root), M is a constant with type Map integer to integer. The verification
steps are given below.
   From ASSIGN-ST, 1 and &p 6∈ {&root, &k}:
                                                                 
              (PRE-COND ∧ x ∈ NodeSet(root) ∧ k ∈ Dom(x))[root/x]
       P⊢        {p = root; }                                           (7)
              (PRE-COND ∧ x ∈ NodeSet(root) ∧ k ∈ Dom(x))[p/x]
From ∧-I, 7, CONSEQ, 6:

 P ⊢ PRE-COND {p = root; } PRE-COND ∧ p ∈ NodeSet(root) ∧ k ∈ Dom(p) (8)
From ASSIGN-ST, 1, and &p 6∈ {&root, &k}:
                                                               
           (PRE-COND ∧ x ∈ NodeSet(root) ∧ k ∈ Dom(x))[p → l/x]
     P⊢      {p := p → l; }                                                 (9)
           (PRE-COND ∧ x ∈ NodeSet(root) ∧ k ∈ Dom(x))[p/x]
From 3, substitution:
          P, PRE-COND, p ∈ NodeSet(root), k ∈ Dom(p), k < p → K ⊢
                                                                             (10)
              p → l ∈ NodeSet(root) ∧ k ∈ Dom(p → l)
From 9, 10, and CONSEQ:
                                                              
         PRE-COND ∧ p ∈ NodeSet(root) ∧ k ∈ Dom(p) ∧ k < p → K
   P⊢       {p := p → l; }                                                 (11)
         PRE-COND ∧ p ∈ NodeSet(root) ∧ k ∈ Dom(p)
Similarly, we can prove:
                                                               
          PRE-COND ∧ p ∈ NodeSet(root) ∧ k ∈ Dom(p) ∧ k > p → K
   P⊢        {p := p → r; }                                                (12)
          PRE-COND ∧ p ∈ NodeSet(root) ∧ k ∈ Dom(p)

k ∈ Dom(p) implies p 6= nil, thus k < p → K ∨ k ≥ p → K. From IF-ST, 11, 12,
and :
                                                                 
        PRE-COND ∧ p ∈ NodeSet(root) ∧ k ∈ Dom(p) ∧ p → K 6= k
   P⊢      {if (k < p → K) p := p → l; else p := p → r; }            (13)
        PRE-COND ∧ p ∈ NodeSet(root) ∧ k ∈ Dom(p)
k ∈ Dom(p) implies that p 6= nil, thus p → K 6= k ∨ p → K = k. From WHILE-
ST, 13:
                                                                  
          PRE-COND ∧ p ∈ NodeSet(root) ∧ k ∈ Dom(p)
   P⊢       {the while statement}                                    (14)
          PRE-COND ∧ p ∈ NodeSet(root) ∧ k ∈ Dom(p) ∧ p → K = k

From 8 and the properties of finite map:

              P, isHBST(x), p ∈ NodeSet(x), k = p → K ⊢
                                                                            (15)
                   TMapP(x, p)†{p → K 7→ y} = Map(x)†{k 7→ y}

From 15, substitution:

         P, PRE-COND, p ∈ NodeSet(root), k = p → K ⊢
                                                                            (16)
         isHBST(root) ∧ MapP(root, p)†{p → K 7→ d} = M †{k 7→ d})

From the rule ASSIGN-ST, 2 and &p → D 6∈ {&root, &p, &p → K, &k, &d}:
                                                                       
     (isHBST(root) ∧ MapP(root, p)†{p → K 7→ x} = M †{k 7→ d})[d/x]
P⊢       {p → D := d}                                                  
     (isHBST(root) ∧ MapP(root, p)†{p → K 7→ x} = M †{k 7→ d})[p → D/x]
                                                                     (17)
From the rule CONSEQ, 16, 17
                                                                
         PRE-COND ∧ p ∈ NodeSet(root) ∧ k ∈ Dom(p) ∧ p → K = k
   P⊢       {p → D := d}                                           (18)
         isHBST(root) ∧ Map(root) = M †{k 7→ d}

From the rule SEQ-ST, 8, 14, 18:

    P ⊢ PRE-COND {Prog} isHBST(root) ∧ Map(root) = M †{k 7→ d}              (19)


8   Heuristics: virtual variables and pragmatic meaning of
    program statements
Generally speaking, a pointer program may create unbounded number of data
objects during its execution. These data objects usually interconnected through
pointers. They are usually used to represent abstract values which can be re-
trieved using recursively defined DRFs. We can view a set of interconnected
data objects as a virtual variable, which holds an abstract value retrieved using
a DRF. Usually, such a data object set maintains a set of structural properties
during the program execution. These properties can also be expressed using a
set of boolean-typed DRFs. As we did in our running example, a DRF isHBST
is used to state that a set of data objects form a binary search tree, while the
DRF Map is used to retrieve a finite map from this binary search tree.
    Usually, assigning new values to such a virtual variable is performed by a
group of program statements. These statements change the values stored in a
few number of the data objects, thus change the abstract value ‘stored’ in the
virtual variable. As to the structural properties, either none of the statements
changes their values, or some statements change their values, but some other
statements restore them afterwards. To reasoning the effect of these statements
on the abstract value, we can define some auxiliary data-retrieve functions.

 – These auxiliary DRFs do not accessed the memory units modified by these
   statements. So the abstract values retrieved by these auxiliary DRFs keep
   unchanged.
 – The relationship between the abstract value retrieved by the main DRFs,
   those retrieved by auxiliary DRFs, and the values stored in the modified
   memory units can be proved based on the definitions of the DRFs. For
   example, the property

     P, isHBST(x), y ∈ NodeSet(x) ⊢ Map(x) = MapP(x, y)†{y → K 7→ y → D}

   shows the relation between the main DRF Map, the auxiliary DRF MapP,
   and the values stored in &y → K and &y → D.
 – The values retrieved by auxiliary DRFs keep unchanged. The effect of these
   statements on the modified memory units can be relatively easily derived.
   So, the effect of these statements on the abstract value retrieved by main
   DRF can be reason based on the relations between main DRFs, auxiliary
   DRFs and the value stored in modified memory units.

To specify and verify these statements, we should understand and reason these
statements as a whole, as these statements work together to assign a new value
to a virtual variable. Understanding the effects of such statement groups can
help us understand the whole program abstractly. In the appendix B, we briefly
describe such an example. We say the effect of a group of program statements on
a virtual variable as the pragmatic meaning of these statements. Understanding
and verifying the pragmatic meanings of small statement groups first, then we
can verify code with larger size step by step.


9   Conclusion and future works

In this paper, we present an extension of Hoare logic for verification of pointer
programs. The pre-conditions and post-conditions are formulae of an extended
version of the LPF logic, which can deal with undefinedness, recursive function
definitions, and types. Program types and function symbols (∗, &→ n and &[ ])
associated with these types are introduced to model memory unit access and
memory layout for composite types. A set of proof rules are introduced to specify
these function symbols. Using these functions, people can deal with high-level
program types (record, array) directly.
    People can define recursive functions to retrieve abstract values from concrete
interconnected data objects. We call these functions as data-retrieve functions
(DRFs). Such functions can also be defined to specify the properties of data
structures. For each data-retrieve function f , we can derive the definition of its
corresponding memory-scope function (MSF) syntactically. When an abstract
value is retrieved by applying f to a set of arguments, applying the MSF of
f to same arguments results in a set of memory units accessed during the re-
trievement. As long as no memory unit in this set is modified during program
executions, applying f to same arguments results in same abstract value.
    We present a new proof rule for assignment statements, and another rule for
memory allocation statements. The proof rule for assignment statements says
that after the assignment, the memory unit referred by the left-hand stores the
value of the right-hand computed before the assignment. It also says that the
abstract values keep unchanged if the memory unit referred by the left-hand is
not in their memory scopes. The proof rule for memory allocation says that after
the allocation, the memory unit referred by the left-hand stores a reference to a
newly allocated memory block.
    This logic has the following advantages.

 – This logic is easy to learn. Most of the knowledge encoded in this logic
   have been (explicitly or implicitly) taught in undergraduate CS courses.
   For examples, the concept of recursive functions and first order logic are
   already taught in undergraduate CS courses. The proof rules about program
   variables, ∗, &→ n, &[] are taught informally in the undergraduate courses
   about programming languages and compilers.
 – This logic supports reuse of proofs. Most of the proved properties of DRFs are
   about data structures. They are independent of the code under verification.
   So these properties can be reused in verification of other code using same
   data structures. It is possible to build a library of pre-defined DRFs, MSFs,
   and their properties.
 – Verification can be performed on different abstract levels. A group of state-
   ments change the abstract value represented by a set of interconnected data
   objects, but keep the structural properties of these data objects. People can
   first understand the pragmatic meaning of these statements, i.e. the effect of
   these statements on the relevant abstract values. Then, they may view these
   data objects as a virtual variable, and the statements as an abstract state-
   ment assigning new value to this virtual variable. Thus, people can reasoning
   the program at a more abstract level.
 – Make use of the research results on pointer analysis. Many of the premises
   when applying proof rules can be proved automatically by pointer analy-
   sis. For example, for all assignment statements of the form ∗(&v) = e, the
   premise that &v 6= nil can be proved by pointer analyer easily. For assign-
   ment statements of the form ∗p = e, the premise p 6= nil of the proof rule
   ASSIGN-ST can also be verified automatically in many cases.

   In the future, we will extended our logic to deal with more programming
language concepts: function calls, function pointers, class/object, generics, . . ..
At the mean time, we will try to build a library of pre-defined DRFs, MSFs, and
their properties for frequently used data structures.
References
 1. C.A.R. Hoare. An axiomatic basis for computer programming. Communications
    of the ACM, 12(10):576-580 and 583, October 1969
 2. C.A.R. Hoare. Proof of a program: FIND. Communications of the ACM, 14(1):39-
    45, January 1971.
 3. Rodney M. Burstall. Some techniques for proving correctness of programs which
    alter data structures. In Machine Intelligence 7, pages 23-50. Edinburgh University
    Press, Edinburgh, Scoland, 1972
 4. Stephen A. Cook and Derek C. Oppen. An assertion language for data structures.
    In Conference Record of 2nd ACM Symposium on Priciples of Programming Lan-
    guages, pages 160-166. New York, 1975
 5. Joseph M. Morris. A general axiom of assignment; assignment and linked data
    structures; a proof of the Schorr-Waite algorithm. In Theoretical Foundations of
    Programming Methodology pages 25-51. D. Reidel, Dordrecht, Holland 1982.
 6. Jonh C. Reynolds An overview of separation logic. In proceedings of Verified
    Software: Theories, Tools, Experiments 2005, Zurich, Switzerland, October 10-13,
    2005 Revised Selected Papers and Discussions
 7. Hongseok Yang. An example of local reasoning in BI pointer logic: The
    Schorr-Waite graph marking algorithm. In Fritz Henglein, John Hughes, Henning
    Makholm, and Henning Niss, editors, SPACE 2001: Informal Proceedings of Work-
    shop on Semantics, Program Analysis and Computing Environments for Memory
    Management, pages 41C68. IT University of Copenhagen, 2001
 8. C.B. Jones and C.A.Middelburg A typed logic of partial functions reconstructed
    classically. In Acta Inform. 31 5 (1994), pp. 399C430
 9. David Gries The Schorr-Waite Graph Marking Algorithm. In Program Construc-
    tion, International Summer School, pp 58-69, LNCS 69.


A    Another example: inserting a node to a binary search
     tree

Example 4. The program depicted in Figure 5 add a new tuple (k, d) into the
map represented by a binary search tree. The types of the program variables k
and d are both integer. The type of program variables rt and tmp are P(T ),
where T is REC((l, P(T )) × (r, P(T )) × (K, integer) × (D, integer)). The type
of p is P(P(T )).

    The DRFs depicted in Figure 6 are used in the specification and verification
of the program depicted in Figure 5. If ∗x points to the root node of a binary
search tree, and y is the address of a child-field of a node of this tree. The
DRF PNodeSet(x, y) retrieve the set of the children-pointer-field addresses (i.e.
addresses of the fields l and r) of all the nodes in the binary search tree derived
by setting ∗y to nil. The argument x is also in this set. MapPP(x, y) retrieve the
map represented by this modified binary search tree.
    The boolean-typed DRF isHBSTK(x, y) says that if we make ∗y point to a
newly allocated node {nil, nil, k, d}, ∗x is still the root node of a binary search
tree. The DRF DomK(x, y) retrieve the keys stored in this tree.
           p:=&rt;
           while (∗p! = nil)
           {
                 if (k < p → K ) p := &(∗p) → l else p := &(∗p) → r;
           }
           tmp = alloc(T );
           tmp → K := k; tmp → D := d;
           ∗p=tmp;



                            Fig. 5. Another program



   The (simplified) definitions of the corresponding MSFs are depicted in Fig-
ure 7. We use DMKm , STKm , MPPPm as M(DomK), M(isSTK), and M(MapPP)
respectively. Let P′ be the set of function definitions depicted in Figure 2 and
Figure 6. Some of the properties about the DRFs in P′ and corresponding MSFs
are depicted in Figure 8. Some of the DRFs and MSFs in Section 7, together
with their properties, are reused in this verification.



DomK(x, y) : P(P(T )) × P(P(T )) → SetOf(integer)
  , (x = y)     ? {k} :
    (∗x = nil) ? ∅ : {(∗x) → K} ∪ DomK(&(∗x) → l, y) ∪ DomK(&(∗x) → r, y)

isHBSTK(x, y) : P(P(T )) × P(P(T )) → boolean
   , (x = y)    ? TRUE :
     (∗x = nil) ? TRUE :
                InHeap(∗x) ∧ isHBSTK(&(∗x) → l, y) ∧ isHBSTK(&(∗x) → r, y)∧
                (DomK(&(∗x) → l) = ∅?TRUE : MAX(DomK(&(∗x) → l)) < (∗x) → K)∧
                (DomK(&(∗x) → r) = ∅?TRUE : (∗x) → K < MIN(DomK(&(∗x) → r)))

MapPP(x, y) : P(P(T )) × P(P(T )) → Map integer to integer)
  , (x = y)     ?∅ :
    (∗x = nil) ? ∅ :
               MapPP(&(∗x) → l, y)†MapPP(&(∗x) → r, y)†{(∗x) → K 7→ (∗x) → D}

PNodeSet(x, y) : P(P(T )) × P(P(T )) → SetOf(Ptr)
  , {x} ∪ ((x = y)?∅ : (∗x = nil) ? ∅ : (PNodeSet(&(∗x) → l, y) ∪ PNodeSet(&(∗x) → r, y))))



      Fig. 6. DRFs for specifying and verifying the program in Figure 5
DMKm (x, y) : P(P(T )) × P(P(T )) → SetOf(Ptr)
   , (x = y)      ?{&k}
     ({x} ∪ (∗x = nil)?∅ : {x, &(∗x) → K} ∪ DMKm (&(∗x) → l, y) ∪ DMKm (&(∗x) → r, y))

HBSTKm (x, y) : P(P(T )) × P(P(T )) → SetOf(Ptr)
   , (x = y)      ?∅ :
     {x} ∪ (∗x = nil) ? ∅ : HBSTKm (&(∗x) → l, y) ∪ HBSTKm (&(∗x) → r, y)∪
                  DMKm (&(∗x) → l) ∪ (DomK(&(∗x) → l) = ∅?∅ : {&(∗x) → K})∪
                  DMKm (&(∗x) → r) ∪ (DomK(&(∗x) → r) = ∅?∅ : {&(∗x) → K})

MPPPm (x, y) : P(P(T )) × P(P(T )) → SetOf(Ptr)
   , (x = y) ?∅ :
     {x} ∪ (∗x = nil) ? ∅ :
                  MPPPm (&(∗x) → l, y) ∪ MPPPm (&(∗x) → r, y) ∪ {&(∗x) → K, &(∗x) → D}

PNSm (x, y) : P(P(T )) × P(P(T )) → SetOf(Ptr)
   , (x = y)?∅ : {x} ∪ (∗x = nil) ? ∅ : (PNSm (&(∗x) → l, y) ∪ PNSm (&(∗x) → r, y))



                      Fig. 7. MSFs of the DRFs in Figure 6




P′ , isHBST(∗x), isHBSTK(x, y) ⊢ y 6∈ DMKm (x, y)∪HBSTKm (x, y)∪MPPPm (x, y)∪PNSm (x, y)
                                                                                  (20)

           P′ , isHBST(∗x), y ∈ PNodeSet(x, y), ∗y 6= nil ⊢ ∗y ∈ NodeSet(∗x)      (21)

      P′ , isHBST(∗x), y ∈ PNodeSet(x, y) ∧ isHBSTK(x, y) ∧ k < (∗y) → K ⊢
                                                                                  (22)
             &(∗y) → l ∈ PNodeSet(x, &(∗y) → l) ∧ isHBSTK(x, &(∗y) → l)

      P′ , isHBST(∗x), y ∈ PNodeSet(x, y) ∧ isHBSTK(x, y) ∧ k > (∗y) → K ⊢
                                                                                  (23)
             &(∗y) → r ∈ PNodeSet(x, &(∗y) → r) ∧ isHBSTK(x, &(∗y) → r)

          P′ , isHBSTK(x, y), y ∈ PNodeSet(x, y), inHeap(∗y),
                                                              ⊢ isHBST(∗x)        (24)
          (∗y) → K = k ∧ (∗y) → l = nil ∧ (∗y) → r = nil

     P′ , isHBST(∗x), y ∈ PNodeSet(x, y) ⊢ Map(∗x) = MapPP(x, y)†Map(∗y)          (25)

           P′ , isHBST(∗x) ⊢ &p 6∈ DMKm (x, y) ∪ HBSTKm (x, y) ∪ MPPPm (x, y)     (26)

          P′ , isHBST(∗x) ⊢ &tmp 6∈ DMKm (x, y) ∪ HBSTKm (x, y) ∪ MPPPm (x, y)    (27)

               Fig. 8. Some properties about the DRFs and MSFs
  We use PRE-COND as the abbreviation for isHBST(rt) ∧ k 6∈ Dom(rt) ∧
Map(rt) = M0 . The specification of this program is

        PRE-COND{The Program}isHBST(rt) ∧ Map(rt) = M0 †{k 7→ d}

The sketch of the proof is as follows. The common premise of these assertions is
P′ , which is omitted for conciseness.

From the rule ASSIGN-ST, 1, 26, and &p 6∈ {&rt, &k}, we get following two
assertions:

      (PRE-COND ∧ isHBSTK(&rt, x) ∧ x ∈ PNodeSet(&rt, x))[&rt/x]
           {p = &rt; }                                                     (28)
      (PRE-COND ∧ isHBSTK(&rt, x) ∧ x ∈ PNodeSet(&rt, x))[p/x]


 (PRE-COND ∧ (x ∈ PNodeSet(&rt, x)) ∧ isHBSTK(&rt, x))[&(∗p) → r/x]
     {p = &(∗p) → r}                                                (29)
 (PRE-COND ∧ (x ∈ PNodeSet(&rt, x)) ∧ isHBSTK(&rt, x))[p/x]

From the rule CONSEQUENCE, 29, and 23:

   PRE-COND ∧ (p ∈ PNodeSet(&rt, p)) ∧ isHBSTK(&rt, p) ∧ ∗p 6= nil∧
   (k > ∗y → K)
                                                                           (30)
        {p = &(∗p) → r}
   PRE-COND ∧ (p ∈ PNodeSet(&rt, p)) ∧ isHBSTK(&rt, p)

Similarly to the way we get 30, we have:

   PRE-COND ∧ (p ∈ PNodeSet(&rt, p)) ∧ isHBSTK(&rt, p) ∧ ∗p 6= nil∧
   (k < ∗y → K)
                                                                           (31)
        {p = &(∗p) → l}
   PRE-COND ∧ (p ∈ PNodeSet(&rt, p)) ∧ isHBSTK(&rt, p)

As ∗p 6= nil implies k < p → K ∨ k ≥ p → K. From the rule IF-ST, 30 and 31:

    PRE-COND ∧ (p ∈ PNodeSet(&rt, p)) ∧ isHBSTK(&rt, p) ∧ ∗p 6= nil
        {if (k < p → K) p := &(∗p) → l else p := &(∗p) → r; }              (32)
    PRE-COND ∧ (p ∈ PNodeSet(&rt, p)) ∧ isHBSTK(&rt, p)

p ∈ PNodeSet(&rt, p)) implies p 6= nil, thus ∗p = nil ∨ ∗p 6= nil, From the rule
WHILE-ST, 32:

    PRE-COND ∧ (p ∈ PNodeSet(&rt, p)) ∧ isHBSTK(&rt, p)
        {the while statement}                                              (33)
    PRE-COND ∧ (p ∈ PNodeSet(&rt, p)) ∧ isHBSTK(&rt, p) ∧ ∗p = nil
From the rule CONSEQUENCE, 25, ∗p = nil, and Map(nil) = ∅, we have

      PRE-COND ∧ (p ∈ PNodeSet(&rt, p)) ∧ isHBSTK(&rt, p)
           {the while statement}                                            (34)
      p ∈ PNodeSet(&rt, p) ∧ isHBSTK(&rt, p) ∧ MapPP(&rt, p) = M0

From the rule ALLOC-ST and the fact that tmp is not relevant to any terms,
we have:
     p ∈ PNodeSet(&rt, p) ∧ isHBSTK(&rt, p) ∧ MapPP(&rt, p) = M0
           {tmp = alloc(T ); }
                                                                            (35)
     p ∈ PNodeSet(&rt, p) ∧ isHBSTK(&rt, p) ∧ MapPP(&rt, p) = M0 ∧
     tmp 6= nil ∧ InHeap(tmp) ∧ Unique(&tmp) ∧ PtrInit(tmp)


     p ∈ PNodeSet(&rt, p) ∧ isHBSTK(&rt, p) ∧ MapPP(&rt, p) = M0 ∧
     tmp 6= nil ∧ InHeap(tmp) ∧ Unique(&tmp) ∧ PtrInit(tmp)
           {tmp → K := k; tmp → D := d; }                                   (36)
     p ∈ PNodeSet(&rt, p) ∧ isHBSTK(&rt, p) ∧ MapPP(&rt, p) = M0 ∧
     isHBST(tmp) ∧ Map(tmp) = {k 7→ d}

From the rule ASSIGN-ST, 20, and p 6∈ {&p}, we have:

     p ∈ PNodeSet(&rt, p) ∧ isHBSTK(&rt, p) ∧ MapPP(&rt, p) = M0 ∧
     isHBST(tmp) ∧ Map(tmp) = {k 7→ d}
          {∗p := tmp; }                                                     (37)
     p ∈ PNodeSet(&rt, p) ∧ isHBSTK(&rt, p) ∧ MapPP(&rt, p) = M0 ∧
     isHBST(∗p) ∧ Map(∗p) = {k 7→ d}

From the rule CONSEQUENCE, 24, and 25, we have:

     p ∈ PNodeSet(&rt, p) ∧ isHBSTK(&rt, p) ∧ MapPP(&rt, p) = M0 ∧
     isHBST(tmp) ∧ Map(tmp) = {k 7→ d}
                                                                            (38)
          {∗p := tmp; }
     isHBST(rt) ∧ Map(rt) = M0 †{k 7→ d}

From the rule SEQ-ST, and 28, 34, 35, 36, 38, we prove the specification.

        PRE-COND{The Program}isHBST(rt) ∧ Map(rt) = M †{k 7→ d}             (39)


B    Verifying programs abstractly: the simplified
     Schorr-Waite algorithm
The Schorr-Waite algorithm marks all nodes of a directed graph that are reach-
able form one given node. The program depicted in Figure 9 is rewrite from a
simplified version presented by David Gries[9]. The variables tmp, p, q, root, vroot
are declared with type P(T ), and T = REC((m, integer)×(l, P(T ))×(r, P(T )).
In this program, it is simplified that each node has exactly two non-nil pointers
(i.e. the field l and r). We use this program to show how to verify a program in
an abstract level. The verification presented here is just a sketch, many details
are omitted.



                p=root; q=vroot; /*vroot → l = vroot → r = root*/
                while(p 6= vroot)
                {
                     p → m = p → m + 1;
                     if (p → m = 3 or (&p → l) → m = 0)
                     {
                                  tmp := p; p := p → l;
                                  p → l = p → r; p → r := q; q = tmp;
                     }
                     else
                     {
                                  tmp := p → l; p → l := p → r;
                                  p → r := q; q := tmp
                     }
                }



                 Fig. 9. The simplified Schorr-Waite algorithm



    The DRFs used in (partial) specification and verification of this algorithm
are depicted in Figure 10. Intuitively speaking, the DRF StackPath(p) retrieve
the path from the virtual root vroot to the current node p. Pred(x) is used to
compute the predecessor of a node in the path. AcyclicSeq(x) is used to assert
that the path retrieved by StackPath(p) is acyclic.
    Let G be the node set of the graph; L(p) for original value of p → l; R(p)
for original value of p → r; SUCC(x) , (x → m = 1) ? R(x) : L(x). From [9], the
following invariant of the while statement holds.

         ∀x ∈ G · ( (x → m = 0 ∧ x → l = L(x) ∧ x → r = R(x))∨
                    (x → m = 1 ∧ x → l = R(x) ∧ SUCC(x → r) = x)∨
                    (x → m = 2 ∧ SUCC(x → l) = x ∧ x → r = L(x))∨
                    (x → m = 3 ∧ x → l = L(x) ∧ x → r = R(x)) )
         V                                                                     (40)
           (
             (p → m = 0 ∧ (L(q) = p ∨ R(q) = p))∨
         V (p → m = 1 ∧ q = L(p)) ∨ (p → m = 2 ∧ q = R(p)) )
           AcyclicSeq(StackPath(p)) ∧ p = head(StackPath(p))
           StackPath(x) : P(T ) → SeqOf(P(T ))
              , (x = vroot) ? [vroot] : [x]⌢ StackPath(Pred(x)))

           Pred(x) : P(T ) → P(T )
              , (x → m = 0) ? q : ((x → m = 1) ? x → r : x → l)

           AcyclicSeq(x) : SeqOf(P(T ))
              , head(x) 6∈ tail(x) ∧ AcyclicSeq(tail(x))


           Fig. 10. The functions defined to prove Schorr-Waite al-
           gorithm



   We write this invariant as INV. The following specifications of the body of
                                                            ←     ←
the while statement can be proved. In these specifications, p and S are constants
used to denote the original value of p and the path.
                                                                   ←   ←
      INV ∧ p → m = 0 ∧ L(p) → m = 0 ∧ StackPath(p) = S ∧p = p
        {The body of the while statement}                                   (41)
           ←                              ←    ←
      INV∧ p → m = 1 ∧ StackPath(p) = L( p ) ⌢ S

                                                                   ←   ←
      INV ∧ p → m = 1 ∧ R(p) → m = 0 ∧ StackPath(p) = S ∧p = p
        {The body of the while statement}                                   (42)
           ←                              ←    ←
      INV∧ p → m = 2 ∧ StackPath(p) = R( p ) ⌢ S
                                                             ←
               INV ∧ p → m = 2 ∧ StackPath(p) = p ⌢ S
                 {The body of the while statement}                          (43)
                           ←     ←                         ←
               INV ∧ p = R( p )∧ p → m = 3 ∧ StackPath(p) = S
If we view StackPath(p) as a virtual variable, it can be seen that the body
of the while statement have different pragmatic meanings when the value of
p → m equals to 0, 1, 2. Based on these properties, we can view the abstract
program depicted in Figure 11 as an abstract version of the program in Figure 9.
From this abstract level, it is clear that the program in Figure 9 is in fact an
efficient and elaborative implementation of the depth-first-search algorithm. We
can continue proving the algorithm based on this abstract program. Though
assignment statements to abstract variables are not allowed in the code, the
abstract program can help us thinking.
     p:=root; S=∅; push(vroot, S); push(p, S);
     while (p 6= vroot) do {
           p → m = p → m + 1;
           if (p → m = 1 ∧ L(p) → m = 0 )       {push(L(p), S); }
           else if (p → m = 2 ∧ R(p) → m = 0 )      {push(R(p), S); }
                 else if (p → m = 3)    {pop(S);}
                      else skip
           p = top(S)
           }



Fig. 11. The abstract version of the simplified Schorr-Waite algorithm
