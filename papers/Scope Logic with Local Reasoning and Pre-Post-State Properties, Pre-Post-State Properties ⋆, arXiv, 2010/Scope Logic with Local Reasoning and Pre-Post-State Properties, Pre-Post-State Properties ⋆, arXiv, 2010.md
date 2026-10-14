                                                  Scope Logic with Local Reasoning and
                                                       Pre/Post-State Properties ⋆

                                                                      ZHAO Jianhua, LI Xuandong

                                                         State Key Laboratory of Novel Software Technology
arXiv:1012.2553v1 [cs.LO] 12 Dec 2010




                                                         Dept. of Computer Sci. and Tech. Nanjing University
                                                                  Nanjing, Jiangsu, P.R.China 210093
                                                                          zhaojh@nju.edu.cn



                                                Abstract. This paper presents an extension to Hoare logic for pointer
                                                program verification. Logic formulas with user-defined recursive func-
                                                tions are used to specify properties on the program states before/after
                                                program executions.
                                                Three basic functions are introduced to represents memory access, record-
                                                field access and array-element access. Some axioms are introduced to
                                                specify these basic functions in our logic.
                                                The concept Memory Scope Function (MSF) is introduced in our logic.
                                                Given a recursive function f , the MSF of f computes the set of memory
                                                units accessed during the evaluation of f . A set of rules are given to
                                                derive the definition of this MSF syntactically from the definition of f .
                                                As MSFs are also recursive functions, they also have their MSFs. An
                                                axiom is given to specify that an MSF contains its MSF. Based on this
                                                axiom, local reasoning is supported with predicate variables.
                                                Pre-state terms are used to specify the relations between pre-states and
                                                post-states. People can use pre-state terms in post-conditions to repre-
                                                sents the values on the pre-state.
                                                The axiom of assignment statements in Hoare’s logic is modified to deal
                                                with pointers. The basic idea is that during the program execution, a
                                                recursive function is evaluated to the same value as long as no memory
                                                unit in its memory scope is modified. Another proof rule is added for
                                                memory allocation statements.
                                                We use a simple example to show that our logic can deal with pointer
                                                programs in this paper. In the appendix, the Shorre-Waite algorithm is
                                                proved using our logic. We also use the selection-sort program to show
                                                that our logic can be used to prove program with indirectly-specified
                                                components.


                                        1     Introduction

                                        Hoare’s logic[1] can not deal with pointer programs because of pointer alias, i.e.
                                        many pointers may refer to the same location. A few extensions to Hoare logic
                                        have been made to deal with pointers or shared mutable data structures [2][3][4].
                                        ⋆
                                            This paper is supported
Among them, separation logic [5] is famous. That logic uses a memory model
which consists of two parts: the stack and the heap. Pointers can only refer to
data objects in the heap. The Hoare logic is extended with a set of proof rules
for heap lookup, heap mutation and program variable assignment. Separation
logic extends the predicate calculus with the separation-conjunction operator
(*), which can separate the heap into different disjoint parts. To specify the sep-
aration conjunction and related function symbols(7→ and ⇁), totally 14 axioms
and proof rules are introduced. These axioms and rules are not strong enough
to prove most programs. So five special classes of formulas are defined based on
the semantic of separation-conjunctions, 7→ and ⇁. 5 axioms and several seman-
tic theorems are introduced to improve Separation Logic. Yet another two new
           [e] J
symbols (֒→,     ) and 11 axioms are introduced to deal with composite types
(record-types and array-types). Supplemental proof rules for assignment, alloca-
tion/deallocation are also provided. Another disadvantage of Separation Logic,
people still have to deal with low-level address manipulations, which has been
generally avoided in high-level programming languages. A few small programs
have been used to demonstrate the potential of local reasoning for scalability [6].
In that paper, the Shorre-Waite algorithm was proved using Separation Logic,
on the assumption of many complicated logic formulas.
   This paper presents an extension to Hoare logic for verification of pointer
programs. In order to deal with high-level program types abstractly and directly,
we introduce three functions: ∗ (memory unit access), & → (record-field access),
and &[ ] (array-element access). A set of axioms are used to model and specify
the memory layout/access in pointer programs.
    The value stored in the memory unit referred by an address x is ∗x. In
this logic, the memory units for program variables and heap objects are treated
uniformly. A program variable v corresponds to a constant memory address &v.
The value stored in v is expressed as ∗&v. As a consequence, program variables
are no longer treated as logic variables in specifications.
    Recursive functions are used in program specifications. For a recursive func-
tion defined using ∗, its value is relevant to a set of memory units. We show
that this memory unit set can be expressed by another recursive function, called
memory-scope function (MSF). The definition of the memory-scope function of
f can be constructed syntactically from the definition of f .
   The concept pre-state terms are introduced in this paper. They can help
people specify the relations between pre-/post-states.
    This paper is organized as follows. We first introuce the syntax of programs
and specifications in Section 2. In Section 3, we introduce the concepts of memory
scopes and pre-state terms. A proof rule is introduced to specify how definitions
of MSFs are constructed. Two axioms are introduced to specify the properties
about memory scopes. To model memory access and layout in pointer programs,
three functions and a set of axioms are introduced in Section 5. The axioms
and proof rules for program statements are given in Section 6. Some other proof
rules are given in Section 7. Section 8 describes how to write verifications in
2-dimension form. The verification of the running example using our logic is
presented in Section 9. Section 10 concludes this paper.
     Appendix A presents the verification of an implementation of the Schorre-
Waite algorithm. Appendix B presents an verification of a program template,
i.e. a program with indirectly-specified components.


2     Syntax of programs and specifications
In this section, we give a brief description of the small program language used
in this paper.

2.1    The syntax of program expressions
Besides the basic arithmetic and logical operators, three operators are intro-
duced: ∗, &[ ], & → n. The operator ∗ is used to access the content stored in a
memory unit; &[ ] is used to derive the address of an element of an array; & → n
is used to derive the address of a field of a record.
    Formally, The syntax of program expressions is as follow.
 1. For a program variable v, &v is an expression.
 2. A constant (e.g. 1,2, true, false, nil) is an expression.
 3. Let e0 , e1 , e2 be expressions.
    (a) e0 ?e1 : e2 is also an expression;
    (b) e1 +e2 , e1 −e2 , e1 ∗e2 , e1 /e2 , not e1 , e1 and e2 , e1 or e2 are expressions;
    (c) ∗e1 , &e1 [e2 ], &e1 → n are expressions.
If we compare this small language with the programming language C, the op-
erators & → n (or &[ ]) can be viewed as a composition of & and → n (or [ ]
respectively). The semantic of e0 ?e1 : e2 is same as the conditional expression in
C.

2.2    The type system of the program language
The small program language used in this paper is strong-typed. In this paper, it
is supposed that all programs under verification have passed static type check.
Each expression e has a static type t, which means that at the runtime, either e
denotes a value of type t or e is undefined.
    The types used in programs include the basic types: int (for integers) and
bool (for boolean values); pointer-types P(t), array-types ARR(t, c), and record-
types REC((n1 , t1 )×. . .×(nk , tk )), where t, t1 , . . . , tk are types, n1 , n2 , . . . , nk are
k different names, c is a positive integer constant. We use Ptr as the super type of
all pointer-types. People can also define user-types using the form name := type.
    If we view the new operators & → and &[] as compositions of the C operator
&, → and [ ], the type rules and well-formed conditions of program expressions
are similar to that of the programming language C. However, it is required that
∗ can only be applied to values of the set P(int), P(bool) and P(P(t)) for some
t.
Abbreviations Using the operators ∗, &[ ] and & → n, we can fulfill any op-
eration on arrays and records. However, an expression using & → n and &[ ]
directly may be difficult to write/read. For conciseness, we can use the following
abbreviations in the programs such that we can write C-like expressions. (A new
operator (&.) is introduced here.)

 – ∗(&v), ∗(&e → n), ∗(&e.n), and ∗(&e1 [e2 ]) can be abbreviated as v, e → n,
   e.n, and e1 [e2 ] respectively.
 – &(&v) → n, &(&e1 → n1 ) → n2 , &(&e1 .n1 ) → n2 and &(&e1 [e2 ]) → n can be
   abbreviated as &v.n, &(e1 → n1 ).n, &(e1 .n1 ).n2 and &e1 [e2 ].n respectively.
 – &(&v[e2 ])[e3 ], &(&e1 → n)[e3 ], &(&e1 .n)[e3 ], and &(&e1 [e2 ])[e3 ] can be ab-
   breviated as &(v[e2 ])[e3 ], &(e1 → n)[e3 ], &(e1 .n)[e3 ] and &(e1 [e2 ])[e3 ] re-
   spectively.

We can write concise expressions using these abbreviation rules.

Example 1. Let a, i and j be three program variables. The type of i and j is int;
The type of a is ARR(ARR(REC((f 1, int) × (f 2, bool)), 100), 100). We can
write ∗(&(&(&(&a)[∗(&i)])[∗(&j)]) → f 1) to access the field f 1 of the element
in the ith row and the jth column. Using the abbreviation rules above, we can
abbreviate this expression as a[i][j].f 1.


2.3   The syntax of program statements

The syntax of program statements is as follows.

               st ::= skip | ∗ e1 := e2 | ∗ e := alloc(t)
                      | st; st | if (e) st else st | while (e) st

The type-rules and well-conditions of the statements are as follow.

 – For the assignment ∗e1 := e2 , ∗e1 and e2 must have same static type. Further
   more, their type must integer, boolean, or a pointer type.
 – For the memory allocation statement ∗e := alloc(t), the static type of ∗e
   must be P(t).
 – For the while-statement and if -statement, the static type of e must be
   boolean.

The operational semantic of these statements is similar to that of the program-
ming language C.

Example 2. The program depicted in Figure 1 is a running example used in this
paper. The type of k and d is int. The type of root and p is P(Node), where
Node = REC((l, P(Node)) × (r, P(Node)) × (K, int) × (D, int)). This program
first searches a binary search tree for a node of which the field K equals k. Then
it sets the filed D of this node to d.
              pt:=root;
              while (pt →K 6= k)
              {
                    if (k < pt → K ) pt := pt → l else pt := pt → r;
              }
              pt → D := d;



                Fig. 1. The program used as a running example


2.4   Syntax of specifications
In our logic, a specification is a Hoare-Triple of the form
                                     p{c}q
where c is a code fragment, p and q are logic formulas with recursive functions.
The formulas p and q are respectively called the pre-condition and post-condition
of this specification. As we will use recursively-defined partial functions in pro-
gram specifications, p and q should be formulas of some three-value logics that
can deal with undefinedness. In this paper, we use the Logic for Partial Func-
tions (LPF) [7] as the basic logic, i.e. p and q are LPF formula. However, other
three-value logics can also be used.
    There also some other things should be noticed here.
 – Program variables and logic variables are different things in our logic. A
   program variable represents a memory block storing values. The values stored
   in a program variable may changed by code. A logic variable is a place-holder
   for a value. A logic variable appeared in pre-condition and post-condition
   represents the same value.
 – In our logic, the function ∗ is used to represents the program state. So ∗ has
   different interpretations in p and q. Consequently, the recursive functions
   in the specification defined based on ∗ also have different interpretations
   accordingly.
Formulas appeared in specifications are also strong-typed. Each logic variable
has a static type, though we may omit it. The static types of terms in such
formulas can be automatically decided.
Example 3. Let isHBST, Dom, Map and FldD be the recursive functions defined
in Figure 2; P rog be the program depicted in Figure 1. The specification
       Outlying(ρ, {&p} ∪ FldD(root)}) ∧ isHBST(root) ∧ k ∈ Dom(root)
               { P rog }                                                        (1)
                                      ←−−−−−−−
       ρ ∧ isHBST(root) ∧ Map(root) = Map(root)†{k 7→ d}
says that if the program starts it execution when root points to a binary search
and k equals to the field K of some node in this tree, root still points to a binary
search tree after the execution. The finite map represented by this tree is the
same as the original map except that it maps k to d.
    ←−−−−−−−
    Map(root) in the post-condition is a pre-state term. It means the map repre-
sented by the BST on the pre-state. The definition and proof rules of pre-state
terms will be presented later.
    Outlying(ρ, {&p} ∪ FldD(root)}) is an abbreviation for ρ ∧ (M(ρ) ∩ ({&p} ∪
FldD(root))} = ∅). M(ρ) denotes the memory scope of the formula ρ. This spec-
ification shows that the program modifies only the memory units in {&p} ∪
FldD(root). If ρ holds on the pre-state, and is irrelevant to the memory units in
this set, ρ still holds on the post-state. The concept of memory scopes will be
explained in the next section.



NodeSet(x : P(Node)) : SetOf(Ptr)
     , (x = nil)? ∅ : ({x} ∪ NodeSet(x → l) ∪ NodeSet(x → r))

Map(x : P(Node)) : Map(int, int)
     , (x = nil)?∅ : {x → K 7→ x → D}†Map(x → l)†Map(x → r)

MapP(x : P(Node), y : P(Node)) : Map(int, int)
    , (x = nil)?∅ : MapP(x → l)†MapP(x → r)†
          ((x = y)?∅ : {x → K 7→ x → D})

Dom(x : P(Node)) : SetOf(integer)
    , (x = nil)?∅ : ({x → K} ∪ Dom(x → l) ∪ Dom(x → r))

isHBST(x : P(Node)) : boolean
     , (x = nil)?true : InHeap(x) ∧ isHBST(x → l) ∧ isHBST(x → r)∧
                 (Dom(x → l) = ∅?true : MAX(Dom(x → l)) < x → K)∧
                 (Dom(x → r) = ∅?true : x → K < MIN(Dom(x → r)))

FldD(x : P(Node)) : SetOf(Ptr)
     , (x = nil)?∅ : ({&x → D} ∪ FldD(x → l) ∪ FldD(x → r))


             Fig. 2. The definitions of a set of recursive functions




3     Memory scopes and pre-state terms
3.1   Terms denoting pre-state values
In many cases, people are interested in the relationship between the values be-
fore/after program executions. Merely specifying the property of the program
state after program execution is not sufficient for this purpose. In our logic, we
use pre-state terms to denoting values on pre-states in post-conditions.
Definition 1. Pre-state terms Let e be a term containing no pre-state sub-
term, ←
      −
      e is a pre-state term.
Pre-state terms can appear in both pre-conditions and post-conditions. A pre-
state term ←−
            e denoting the value of e interpreted based on the pre-state before
execution. In pre-conditions, ←
                              −
                              e and e is interchangeable. We have the following
two proof rules.
          p[e/x] {s} q                                 p[←−
                                                          e /x] {s} q
                              (PRE-1)                                      (PRE-2)
         p[←−
            e /x] {s} q                                 p[e/x] {s} q
In the rest of this paper, we will inter-change e and ←−
                                                       e in pre-conditions with-
out mentions these proof rules. For convenience, for a formula Q (or a term e)
containing pre-state terms, we use Q (or e respectively) to denote the formula
(or term) derived by replacing all pre-state terms in Q (or e) with their original
forms. For example, ←  − = t is ∗pt = t.
                      ∗pt

3.2   Memory scopes
Memory scope form of terms An execution of a piece of code may change
the values stored in some memory units. The function symbol ∗ has different
interpretations in the pre-condition and post-condition of a specification. So
does the functions defined based on ∗. As a consequence, a term may denote
different values in the pre-condition and the post-condition. However, the value
of a term e relies only on a finite set of memory units. This set can also be
expressed as a term, called the memory scope form of e, denoted as M(e). Given
a term e, M(e) is defined as follow.
 – For any pre-state term ←       −e , M(←   −
                                             e ) is ∅.
 – If e is a logical variable or a constant, M(e) is ∅.
 – If e is of the form f (e1 , . . . , en ), M(e) is M(e1 )∪. . .∪M(en )∪M(f )(e1 , . . . , en ),
   where M(f ) is the memory scope function of f .
 – If e is of the form e0 ?e1 : e2 , M(e) is M(e0 ) ∪ (e0 ?M(e1 ) : M(e2 )).
Though ←  −
          e is evaluated on the pre-state, its value is not modified by the execu-
tion. So, M(← −
              e ) is ∅.

Memory scope functions Intuitively speaking, M(f )(x1 , . . . , ex ) computes
the set of memory units accessed during the evaluation of f (x1 , . . . , xn ). The
argument types of M(f ) is the same as those of f . The result type of M(f ) is
SetOf(Ptr). Given a function f , the definition of M(f ) can be derived as follow.
 – M(f )(x1 , . . . , xn ) , ∅ if f is a function symbol associated with basic types
   or abstract types (for example, +, −, ×, /, >, <, ∈, ⊆ . . .), or & → n, &[ ], &v
   for some program variable, nil.
 – M(∗)(x) , {x}. That is, ∗x access the memory unit referred by {x}.
 – If f is (recursively) defined as f (x1 , . . . , xn ) , e, we have the definition
   M(f )(x1 , . . . , xn ) , M(e).
In LPF, a function definition is also a formula. We have the following proof rule.

                   f (x1 , . . . , xn ) , e
                                                    (SCOPE-FUNC)
                 M(f )(x1 , . . . , xn ) , M(e)

Example 4. Let e be a[i][j].f 1 (i.e. ∗(&(&(&(&a)[∗(&i)])[∗(&j)]) → f 1)), M(e)
is {&i, &j, &(a[i][j].f 1)}.
    The memory scope form of (x = nil)?∅ : ({x}∪NodeSet(x → l)∪NodeSet(x →
r)) is equivalent to (x = nil)?∅ : {&x → l} ∪ M(NodeSet)(x → l) ∪ {&x →
r} ∪ M(NodeSet)(x → r). According to the definition of NodeSet in Figure 2,

              M(NodeSet)(x) , (x = nil)?∅ : {&x → l, &x → r}∪
                     M(NodeSet)(x → l) ∪ M(NodeSet)(x → r)

The definition of M(NodeSet) is equivalent to that of MSFlr depticted in Figure 3
The following table lists the memory scope functions for the functions defined
in Figure 2 and Figure 3.
                Recursive functions             Memory Scope Functions
       NodeSet, MSFlr , MSFlrk , MSFlrkd , FldD        MSFlr
                  Dom, isHBST                          MSFlrk
                        Map                           MSFlrkd
                        MapP                           MPPm
                                                                                


MSFlr (x : P(Node)) : SetOf(Ptr)
     , (x = nil)? ∅ : ({&x → l, &x → r} ∪ MSFlr (x → l) ∪ MSFlr (x → r))

MSFlrk (x : P(Node)) : SetOf(Ptr)
     , (x = nil)?∅ : ({&x → K, &x → l, &x → r} ∪ MSFlrk (x → l) ∪ MSFlrk (x → r))

MSFlrkd (x : P(Node)) : SetOf(Ptr)
     , (x = nil)?∅ : {&x → K, &x → D, &x → l, &x → r} ∪ MSFlrkd (x → l) ∪ MSFlrkd (x → r)

MPPm (x : P(Node), y : P(Node)) : SetOf(Ptr)
    , (x = nil)?∅ : {&x → l, &x → r} ∪ MPPm (x → l) ∪ MPPm (x → r)∪
          ((x = y)?∅ : {&x → K, &x → D})



                           Fig. 3. The scope functions




Memory Scope for Formulae Roughly speaking, the memory scope term
of a formula is the union of the memory scopes of the terms of this formula.
To formally define the memory scope of a formula p, it is required that each
quantified variable in p has a unique name, and is different from the free variables
in p. Please be noticed that for an arbitrary formula p, we can easily get an
equivalent formula satisfying this condition by variable renaming. The memory
scope term of a formula p is defined as follow.

 1. If p is a boolean-typed term e, M(p) is M(e).
 2. If p is e1 = e2 or e1 == e2 , M(p) is M(e1 ) ∪ M(e2 ). The symbol == is
    the strong equivalence in LPF. It means that either both side of == are
    undefined, or they equal to each other.
 3. If p is p1 ∧ p2 , M(p) is M(p1 ) ∪ M(p2 ).
 4. If p is ¬p′ , M(p) is M(p′ )
 5. If p is ∀x · p′ , M(p) is M(p′ ).


An axiom about memory scopes If all the functions in a term e are either
basic functions or recursively defined functions, we can find that the evaluation
of M(e) tracks the evaluation process of e, and records all the memory units
accessed during this process. All the memory units accessed during the evaluation
of M(e) are also accessed during the evaluation of e. We have the following two
axioms about memory scope functions.

                M(p) ↓ ⇒ M(M(p)) ⊆ M(p)                (SCOPE-1)


                M(e) ↓ ⇒ M(M(e)) ⊆ M(e)                (SCOPE-2)
Here, ↓ is an operator in LPF. M(e) ↓ and M(p) ↓ respectively mean that M(e)
and M(p) are denoting.


4   Supporting local reasoning

In our logic, local reasoning is supported using predicate variables. Usually, a
specification is of the form

                    ρ ∧ (M(ρ) ∩ e = ∅) ∧ pre { s } ρ ∧ post

We can substitute ρ with other formulas to get new assertions about s. The
static type of the term e is SetOf(Ptr). It is an over-approximation of the set of
memory units modified by the code s. The premise (M(ρ) ∩ e = ∅) means that
ρ is irrelevant to the values stored in the memory units in e. Thus, ρ still holds
when s halts normally.
    For conciseness, in the rest of this paper, we use Outlying(ρ, e) as an abbre-
viation for ρ ∧ (M(ρ) ∩ e = ∅). The assertion above can be written as

                      Outlying(ρ, e) ∧ pre { s } ρ ∧ post
Example 5. Considering the program depicted in Figure 1. The program changes
only the memory unit &p and the field D of some node of the tree. The specifi-
cation 1 shows that for any predicate ρ which is irrelevant to the memory unit
&p and the field D of any nodes in the tree, if ρ holds on the pre-state, it still
holds on the post-state.
Theorem 1. Let ρ be an arbitrary predicate symbol. Let r be a predicate. As
mentioned previously, r is derived by replacing each pre-state term ←
                                                                    −
                                                                    e with e.

           Outlying(ρ, e) ∧ p { s } ρ ∧ q p ∧ r ⇒ (M(r) ∩ e = ∅)
                               p∧r { s } q∧r
Proof. Substitute ρ with r and expand Outlying in the first premise, we have
                       r ∧ (M(r) ∩ e = ∅) ∧ p { s } r ∧ q
Apply the proof rule PRE-2, we have
                       r ∧ (M(r) ∩ e = ∅) ∧ p { s } r ∧ q
From the second premise and the consequence rule (presented later), we have
                                r∧p { s } r∧q
                                                                                
Theorem 1 will be used frequently to derive global assertions based on the local
assertion of a statement. We call an application of this theorem as an expanding.


5     The axioms about memory access and layout
In this section, we present some axioms about memory access and memory lay-
outs of composite types. In the implementation of real program languages, mem-
ory layouts for composite types are compiler-dependent. So computing the ad-
dress of a component in a composite-typed data by address-offsetting is not a
good choice. In our logic, we use a set of axioms to specify such memory layouts
abstractly.

5.1   The auxiliary function Block
We define an auxiliary function Block : Ptr → setof(Ptr) to denote the set of
memory units in a memory block. The definition of Block is as follows.
Block(r) = ∅ if r = nil. Otherwise Block(r) =
     
     S                              {r} if ∗r is of type int, bool or Ptr
                          Block(&r →  n) if r : P(t) and t is a record type
      n: field name ofStc−1
                         i=0 Block(&r[i]) if r : P(ARR(t′ , c)) for some t′
Intuitively speaking, Block(r) is the set of memory units in the memory block
referred by r.
5.2   The axioms
There is no memory-deallocation statement in our small program language. Each
time a memory block is allocated, the memory units of pointer types in this block
are initialized to nil. Thus, a non-nil pointer always refers to a valid memory
unit or memory block. We have the following axiom.
                 x : P(t) ∧ x 6= nil ⇒ ∗x : t         (MEM-ACC)
According to the type rule of ∗, t can only be int, bool, or pointer types. The
predicate e : t means that the term e denotes a value of the type t.
   Two different memory blocks are either disjoint, or one of them contains
another one. We have the following axiom.
                     Block(x) ∩ Block(y) = ∅∨
  x 6= y ⇒                                                            (MEM-BLK)
             Block(x) ⊂ Block(y) ∨ Block(y) ⊂ Block(x)
Here, the static type of x and y must be pointer types.
   A unique memory block is assigned to each declared program variable. Fur-
thermore, such a memory block is not contained by any other memory blocks.
So we have the following axioms.
                    &v 6= nil                           (PVAR-1)
                    &v1 6= &v2                          (PVAR-2)
                    Block(&v) 6⊂ Block(x)               (PVAR-3)
Here v is a program variable, v1 and v2 are two different program variables. The
static type of x is a pointer type.
    A memory block for a record-typed data is allocated as a whole. That is,
when a record-typed memory block is allocated, the blocks for all its fields are
allocated. We have the following axiom.
                     x 6= nil ⇒ &x → n 6= nil           (REC-1)
Here, the static type of x is P(REC(. . . × (n, t) × . . .))
    In a record-typed memory block, the memory blocks for different fields are
disjoint with each other. If the static type of x is P(REC(. . . × (n1 , t1 ) × . . . ×
(n2 , t2 ) × . . .)), we have the following axiom.
      x 6= nil ⇒ Block(&x → n1 ) ∩ Block(&x → n2 ) = ∅                 (REC-2)
   Similarly, we have the following two axioms. Here, the static type of x is
P(ARR(t, c)). The static type of y, y1 , y2 is int. The axiom ARR-1 says that
an array-typed memory block is allocated as a whole, i.e. when an array-typed
memory block is allocated, all of the memory blocks for its elements are allocated.
The axiom ARR-2 says that the memory blocks allocated for different elements
are disjoint with each other.
              (x 6= nil) ∧ (0 ≤ y < c) ⇒ &x[y] 6= nil          (ARR-1)
      (x 6= nil) ∧ (0 ≤ y1 < c) ∧ (0 ≤ y2 < c) ∧ (y1 6= y2 ) ⇒
                                                                       (ARR-2)
                        Block(&x[y1 ]) ∩ Block(&x[y2 ]) = ∅
6     Axioms and proof rules of program statements

In this section, we present the axioms and proof rules to specify the effect of
program statements. There are three axioms for primitive statements and three
proof rules for control flow statements.


6.1   The axiom for skip

The skip statement changes nothing. If a formula q hold before the execution of
skip, q still holds after the execution. This is specified by the following axiom.

                         q { skip } q          (SKIP-ST)


6.2   The axiom for assignment

For an assignment ∗e1 := e2 , it is required that e1 evaluates to a non-nil pointer,
i.e. it refers to a memory unit, and e2 evaluates to a value on the pre-state. One
the post-state, the memory unit stores the value of e2 evaluated on the pre-state.
Furthermore, if e1 is not in the memory scope of a formula ρ, ρ still holds after
the execution. This is specified by the following axiom.

            Outlying(ρ, {e1 }) ∧ (e1 6= nil) ∧ (e2 ↓)
                {∗e1 := e2 }                             (ASSIGN-ST)
            ρ ∧ (∗←
                  e−1 = ←
                        e−2 )

Here, ↓ is an operator in LPF: e2 ↓ means that e2 is evaluated to some value.

Example 6. Considering the assignment pt := pt → l in the program depicted
in Figure 1. As &pt 6= nil and (pt 6= nil) ⇒ (&pt → l 6= nil) ⇒ (pt → l) ↓, we
can have the following assertion.
                                                            ←−− ←−−−−
      Outlying(ρ, {&pt}) ∧ (pt 6= nil) {pt := pt → l} ρ ∧ (∗&pt = pt → l)
                                                      ←−−
   Because M(&pt) ∩ {&pt} = ∅, substitute ρ with ρ ∧ (&pt = &pt), and apply
the consequence rule (presented later), we have
                                                                 ←−−−−
       Outlying(ρ, {&pt}) ∧ (pt 6= nil) {pt := pt → l} ρ ∧ (pt = pt → l)


6.3   The axiom for memory allocation

For an allocation statement ∗e1 := e2 , it is required that e1 evaluates to a non-nil
pointer. After the execution, the value stored in the memory unit referred by ←   e−1
refers to a memory block that is unreachable on the pre-state. This allocation
statement modifies only the memory unit referred by e1 and the memory unit
newly allocated. If a predicate ρ holds on the pre-state and e1 is not in the
memory scope of ρ, ρ still holds on the post-state. This is specified by the
following axiom.
      Outlying(ρ, {e1 }) ∧ (e1 6= nil)
            {∗e1 := alloc(t)}                                     (ALLOC-ST)
      Outlying(ρ, Block(∗← e−1 )) ∧ (∗←
                                      e−1 6= nil) ∧ Init(∗←
                                                          e−1 )
The predicate Init(x) is defined as ∀y ∈ Block(x) · y : P(P(t)) ⇒ ∗y = nil. It
means that all the pointers stored in the block referred by x is initialized to nil.
Example 7. Considering the sequential statements t := alloc(Node); t → k :=
k; t → d := d. From the axiom ALLOC-ST, we have
       Outlying(ρ, {&t})
              {t := alloc(Node); t → k := k; t → d := d}
       Outlying(ρ, Block(t)) ∧ (t 6= nil) ∧ (t → l = nil) ∧ (t → r = nil)∧
       (t → k = k) ∧ (t → d = d)

6.4   The proof rule for if -statement
The proof rule for if-statement is almost same as the one in Hoare’s logic. The
only difference is that the conditional expression should always evaluate to a
boolean value.
                   (p ∧ e){s1 }q (p ∧ ¬e){s2 }q
                                                                  (IF-ST)
               p ∧ (e ∨ ¬e) { if (e) s1 else s2 } q

6.5   The proof rule for while-statement
The proof rule in our logic is essentially same as the corresponding one in Hoare’s
logic. The only difference is that we require that the invariant implies the de-
finedness of the conditional expression. We have the following rule.

                      (p ∧ e){s}p ∧ (e ∨ ¬e)
                                                            (WHILE-ST)
              p ∧ (e ∨ ¬e) { while (e) s }¬e ∧ p
               where p is a formula containing no pre-state term.

6.6   The proof rule for sequential statements
The two statements in a sequential composition s1 ; s2 execute sequentially. If
we prove the assertions about s1 and s2 respectively, we can compose these two
assertions into an assertion about s1 ; s2 . As the pre-state of s1 is different from
that of s2 , pre-state terms in two assertions should be eliminated.


                       p {s1 } q    q {s2 } r
                                                       (SEQ-ST)
                           p {s1 ; s2 } r
                   where p, q and r contain no pre-state term.
Example 8. In the proof rules for while-statements and sequential statements,
the pre-/post-conditions contain no pre-state terms. To prove the relation be-
tween pre-state and post-state, we can first prove an assertion with free logical
variables, and then put pre-state terms into it using the proof rule SUBSTITU-
TION, which will be presented in Section 7.
   Let x, y, z be three integer program variables. vx , vy , vz be three logic vari-
ables. We have the following two assertions.

               Outlying(ρ1 , {&x}) {x := x + 1; } ρ1 ∧ x = ←
                                                           −
                                                           x +1
                                                           ←
                                                           −
               Outlying(ρ2 , {&y}) {y := y − z; } ρ2 ∧ y = y − z

Substitute ρ1 and ρ2 with Outlying(ρ, {&x, &y}) ∧ (vx = ← −
                                                          x ) ∧ (vy = y) and
                                             ←
                                             −
Outlying(ρ, {&x, &y}) ∧ (x = vx + 1) ∧ (vy = y ) respectively, then apply the
consequence rule (presented later), we have

              Outlying(ρ, {&x, &y}) ∧ (vx = x) ∧ (vy = y)
                 {x := x + 1; }
              Outlying(ρ, {&x, &y}) ∧ (vy = y) ∧ (x = vx + 1)

              Outlying(ρ, {&x, &y}) ∧ (x = vx + 1) ∧ (vy = y)
                 {y := y − z; }
              Outlying(ρ, {&x, &y}) ∧ (x = vx + 1) ∧ (y = vy − z)

Apply the proof rule for sequential statements, we have

              Outlying(ρ, {&x, &y}) ∧ (vx = x) ∧ (vy = y)
                 {x := x + 1; y := y − z; }
              Outlying(ρ, {&x, &y}) ∧ (x = vx + 1) ∧ (y = vy − z)

Applying the rule SUBSTITUTION, substitute vx and vy with ←
                                                          −
                                                          x and ←
                                                                −
                                                                y re-
spectively, we have

              Outlying(ρ, {&x, &y})
                 {x := x + 1; y := y − z; }
              Outlying(ρ, {&x, &y}) ∧ (x = ←−
                                            x + 1) ∧ (y = ←
                                                          −
                                                          y − z)

Substitute ρ with Outlying(ρ0 , {&x, &y}) ∧ (vy′ = z ∗ ←
                                                       −
                                                       x +←
                                                          −
                                                          y ), and applying the
consequence rule, we have

                    Outlying(ρ0 , {&x, &y}) ∧ (vy′ = z ∗ x + y)
                       {x := x + 1; y := y − z; }
                    Outlying(ρ0 , {&x, &y}) ∧ (vy′ = z ∗ x + y)

Apply the proof rule for while-statements, we have

           Outlying(ρ0 , {&x, &y}) ∧ (vy′ = z ∗ x + y)
              {while (y ≥ z) begin x := x + 1; y := y − z; end }
           Outlying(ρ0 , {&x, &y}) ∧ (vy′ = z ∗ x + y) ∧ (y < z)
From the proof rule SUBSTITUTION, we have
           Outlying(ρ0 , {&x, &y}) ∧ (←
                                      −
                                      y = z ∗ x + y)
              {while (y ≥ z) begin x := x + 1; y := y − z; end }
           Outlying(ρ0 , {&x, &y}) ∧ (←
                                      −
                                      y = z ∗ x + y) ∧ (y < z)

7   Other proof rules
In this section, we presents the rest of the proof rules in our logic. Most of them
are adopted directly from Hoare’s Logic. The consequence rule says that provided
an assertion, we can strengthen the pre-condition, or weaken the post-condition.
                 p {s} q   p′ ⇒ p        q ⇒ q′
                                                        (CONSEQ)
                           p′ {s} q ′
The proof rules CONJUNCTION and DISJUNCTION is same as the ones in
Hoare’s logic.
                  p {s} q p′ {s} q ′
                                                  (CONJUNCTION)
                   p ∧ p′ {s} q ∧ q ′
                   p {s} q p′ {s} q ′
                                                  (DISJUNCTION)
                    p ∨ p′ {s} q ∨ q ′
The proof rules ALL and EXIST are respectively the generalized version of
CONJUNCTION and DISJUNCTION.
                    p {s} q
                                where x is arbitrary         (ALL)
               ∀x · p {s}∀x · q
                  p {s } q
                               where x is arbitrary        (EXIST)
              ∃x · p {s}∃x · q
The proof rule SUBSTITUTION says that we can substitute a variable with
a term e and its pre-state form respectively in the pre-condition and the post-
condition, as long as e is denoting in the pre-state.
       p {s} q p ⇒ e ↓
                             where x is arbitrary         (SUBSTITUTION)
       p[e/x] {s}q[←
                   −
                   e /x]

8   Concise form of proofs
For conciseness, we write code in the following manner.
 – For a sequential composition of s1 ; s2 , we write
                                            {p}
                                             s1
                                            {q}
                                             s2
                                            {r}
  to show that we can first prove p{s1 }q and q{s2 }r, then derive the assertion
  p{s1 , s2 }r by the sequential statement rule. It is required that p, q, r contain
  no pre-state term.
– For a if-statement if (e) s1 else s2 , we write
                                   {p ∧ (e ∨ ¬e)}
                                   if (e)
                                      {p ∧ e}
                                      s1
                                      {q}
                                    else
                                      {p ∧ ¬e}
                                      s2
                                      {q}
                                   {q}
  to show that we can first prove p ∧ e {s1 } q and p ∧ ¬e {s2 }q, then derive
  p ∧ (e ∨ ¬e) {if (e) s1 else s2 } q by the proof rule for if-statements.
– For a while-statement while (e) do s, we write
                                  {p ∧ (e ∨ ¬e)}
                                  while (e)
                                    {p ∧ e}
                                    s
                                    {p ∧ (e ∨ ¬e)}
                                  {p ∧ ¬e}
  to show that we can first prove that p is the invariant of this while-statement,
  then get the assertion p ∧ (e ∨ ¬e) {while (e) do s} p ∧ ¬e.
– An application of the consequence rule
                             p {s} q   p′ ⇒ p       q ⇒ q′
                                       p′ {s} q ′
  is written as
                                         {p′ }
                                       ⇒ {p}
                                         s
                                         {q}
                                       ⇒ {q ′ }
– An substitution of predicate variables or an application of Theorem ??
                    {p′ }                   {p ∧ r}
                      ↑x     e                ↑ρ    r
                    {p}                     {Outlying(ρ, e) ∧ p}
                    s                       s
                    {q}                     {ρ ∧ q}
                      ↓x     ←
                             −
                             e                ↓ρ    r
                    {q ′ }                  {q ∧ r}
     Please be noticed that according to the proof rule SUBSTITUTION, if we
     substitute x with e, q ′ is derived by substitute x in q with ←
                                                                   −
                                                                   e . When substitute
     ρ with r, we must prove the second premise, i.e. p ∧ r ⇒ (M(r) ∩ e = ∅).


9    The proof of the running example in the concise form

Let M Set be
                                 {&pt} ∪ FldD(root)
Let INV be the formula
              Outlying(ρ0 , M Set) ∧ isHBST(root) ∧ Map(root) = x∧
              (pt 6= nil) ∧ (pt ∈ NodeSet(root)) ∧ (k ∈ Dom(pt))

   The proof of the specification 1 in the concise form is depicted in Figure 4.
The following are the properties about the recursive functions used in this proof.

          isHBST(x) ⇒ &pt 6∈ MSFlr (x) ∪ MSFlrk (x) ∪ MSFlrkd (x)

          isHBST(x) ∧ pt ∈ NodeSet(x) ⇒
                &pt → D 6∈ MSFlrk (x) ∪ MSFlr (x) ∪ MPPm (x, pt)

          isHBST(x) ∧ (y ∈ Dom(x)) ∧ (y < x → K) ⇒ y ∈ Dom(x → l)

          isHBST(x) ∧ (y ∈ Dom(x)) ∧ (y > x → K) ⇒ y ∈ Dom(x → r)

          isHBST(x) ∧ (y ∈ NodeSet(x)) ⇒
                Map(x) = MapP(x, y)†{y → K 7→ y → D}

          NodeSet(x) : SetOf(Ptr) ⇒ x ∈ NodeSet(x)



10     Conclusions and further works

In this paper, we present an extension of Hoare logic to deal with pointer pro-
grams. The pre-conditions and post-conditions are logic formulas with recursive
functions.
    Three functions (∗, & → n and &[ ]) are respectively used to represents mem-
ory unit access, record-field access, and array-element access. These functions are
specified by a set of axiom. These axioms formally specify our memory models
with the following properties.

 – A non-nil pointer always refers to a valid memory unit or memory block.
 – Two different memory blocks are either disjoint, or one of them contains
   another one.
 – Each declared program variable is assigned an unique memory block.
  {Outlying(ρ0 , M Set) ∧ isHBST(root)∧
                   ←−−−−−−−
   Map(root) = Map(root) ∧ k ∈ Dom(root)}
      ↑x      Map(root)
  {Outlying(ρ0 , M Set) ∧ isHBST(root)∧
   Map(root) = x ∧ k ∈ Dom(root)}
  pt := root;
  {INV}
  while (pt →K 6= k)
  begin
      {INV ∧ (pt →K 6= k)}
      if (k < pt → K )
           {INV ∧ (pt →K 6= k) ∧ (k < pt → K)}
        ⇒ {Outlying(ρ0 , M Set) ∧ isHBST(root) ∧ Map(root) = x∧
             (pt → l 6= nil) ∧ (pt → l ∈ NodeSet(root)) ∧ (k ∈ Dom(pt → l))}
           pt := pt → l
           {Outlying(ρ0 , M Set) ∧ isHBST(root) ∧ Map(root) = x∧
             (pt 6= nil) ∧ (pt ∈ NodeSet(root)) ∧ (k ∈ Dom(pt))}
        ⇒ {INV}
      else
           {INV ∧ (pt →K 6= k) ∧ ¬(k < pt → K)}
        ⇒ {Outlying(ρ0 , M Set) ∧ isHBST(root) ∧ Map(root) = x∧
             (pt → r 6= nil) ∧ (pt → r ∈ NodeSet(root)) ∧ (k ∈ Dom(pt → r))}
           pt := pt → r;
           {Outlying(ρ0 , M Set) ∧ isHBST(root) ∧ Map(root) = x∧
             (pt 6= nil) ∧ (pt ∈ NodeSet(root)) ∧ (k ∈ Dom(pt))}
        ⇒ {INV}
      {INV}
  end
  {INV ∧ ¬(pt →K 6= k)}
⇒ {Outlying(ρ0 , M Set) ∧ isHBST(root)∧
   MapP(root, pt)†{pt → K 7→ d} = x†{k 7→ d}∧
   (pt 6= nil) ∧ (pt ∈ NodeSet(root)) ∧ (k ∈ Dom(pt))}
           ↑ ρ1     Outlying(ρ0 , M Set) ∧ isHBST(root) ∧ . . . ∧ (k ∈ Dom(pt))
  {Outlying(ρ1 , &pt → D) ∧ pt 6= nil}
  pt → D := d;
  {ρ1 ∧ pt → D = d}
           ↓ ρ1     Outlying(ρ0 , M Set) ∧ isHBST(root) ∧ . . . ∧ (k ∈ Dom(pt))
  {Outlying(ρ0 , M Set) ∧ isHBST(root)∧
   MapP(root, pt)†{pt → K 7→ pt → D} = x†{k 7→ d}∧
   (pt 6= nil) ∧ (pt ∈ NodeSet(root)) ∧ (k ∈ Dom(pt))}
⇒ {ρ0 ∧ isHBST(root) ∧ Map(root) = x†{k 7→ d}}
              ←−−−−−−−
      ↓x      Map(root)
                                        ←−−−−−−−
  {ρ0 ∧ isHBST(root) ∧ Map(root) = Map(root)†{k 7→ d}}



           Fig. 4. The proof in code of the running example
 – A memory block with a composite type is always allocated as a whole. The
   memory blocks allocated for different components of a composite type are
   disjoint with each other.
   To support local reasoning, we use specifications of the form

                    ρ ∧ (M(ρ) ∩ e = ∅) ∧ pre { s } ρ ∧ post

In this specification, e represents an upper bound of the memory set modified by
s. We can substitute ρ with proper predicates in this specification to get global
specifications.
    We use pre-state terms to denoting values before program executions. Pre-
state terms can appear in both pre-conditions and post-conditions. A pre-state
term ← −
       e denoting the value of e interpreted based on the pre-state. In pre-
conditions, ←−
             e and e is interchangeable. The difference between ← −
                                                                  e and e is that
                              ←
                              −
the memory scope form of e is ∅.
    On a specific program state, the value of a term e relies only on a finite set
of memory units. This value of e does not change if the contents stored in these
memory units keep unmodified. We show that such a memory unit set can be
expressed using a term constructed syntactically. Given a user-defined recursive
function, we can construct another recursive function to represents the set of
memory units accessed by this function during its evaluation process. We use an
axiom to specify the properties about memory scope terms and memory scope
functions.
    For the program statements, we present an axiom for assignment statements,
and an axiom for memory allocation statements. Other axioms and proof rules
are same as the ones in Hoare’s logic.
    This logic has the following advantages.
 – The axioms and proof rules in our logic is simpler comparing to those of
   Separation Logic. In Separation Logic, to deal with the separation conjunc-
   tion, 14 axioms are introduced for general cases. Besides these, five special
   classes of formulas are defined based on the semantics of the separation con-
   junction. More axioms and theorems are given for these special formulas. To
   apply these special axioms and rules, people have to judge wether the formula
   is really in the class based on the semantics of separation conjunction.
 – This logic deals with high-level program types (record/array) directly. Sep-
                                                       [e] J
   aration logic introduces two new logical symbols (֒→, ) and 11 axioms to
   deal with records and arrays. People still have to deal with composite types
   with low-level address manipulation.
 – This logic is easy to learn. Most of the knowledge (for example, recursive
   functions, FOL, memory layout of composite P-types.) in this logic have
   been (explicitly or implicitly) taught in undergraduate CS courses. For ex-
   amples, the concept of recursive functions and first order logic are already
   taught in undergraduate CS courses. The proof rules about program vari-
   ables, ∗, & → n, &[ ] are taught informally in the undergraduate courses
   about programming languages and compilers.
 – This logic supports reuse of proofs. Most of recursive functions and their
   proved properties are about data structures. They are independent of the
   code under verification. So these properties can be reused in verification of
   other code using same data structures. It is possible to build a library of pre-
   defined recursive functions, their memory-scope functions, and their verified
   properties.
 – People can easily specify and verify relations between pre-/post-states with
   pre-state terms introduced in our logic.
 – Our logic supports local reasoning precisely. The upper-bound of memory
   units modified by the program can be specified by a term.

     We also use several examples to show the efficacy of our logic. The example
in the Appendix B shows that our logic can also deal with program templates,
i.e. a program with some components indirectly specified.
     In the future, we will extend our logic to deal with more programming lan-
guage concepts: function calls, function pointers, class/object, generics, and so
on. At the mean time, we will try to build a library of pre-defined recursive
functions, their memory scopes, and their properties for frequently used data
structures.



References

 1. C.A.R. Hoare. An axiomatic basis for computer programming. Communications
    of the ACM, 12(10):576-580 and 583, October 1969
 2. Rodney M. Burstall. Some techniques for proving correctness of programs which
    alter data structures. In Machine Intelligence 7, pages 23-50. Edinburgh University
    Press, Edinburgh, Scoland, 1972
 3. Stephen A. Cook and Derek C. Oppen. An assertion language for data structures.
    In Conference Record of 2nd ACM Symposium on Priciples of Programming Lan-
    guages, pages 160-166. New York, 1975
 4. Joseph M. Morris. A general axiom of assignment; assignment and linked data
    structures; a proof of the Schorr-Waite algorithm. In Theoretical Foundations of
    Programming Methodology pages 25-51. D. Reidel, Dordrecht, Holland 1982.
 5. Jonh C. Reynolds An overview of separation logic. In proceedings of Verified
    Software: Theories, Tools, Experiments 2005, Zurich, Switzerland, October 10-13,
    2005 Revised Selected Papers and Discussions
 6. Hongseok Yang. An example of local reasoning in BI pointer logic: The
    Schorr-Waite graph marking algorithm. In Fritz Henglein, John Hughes, Henning
    Makholm, and Henning Niss, editors, SPACE 2001: Informal Proceedings of Work-
    shop on Semantics, Program Analysis and Computing Environments for Memory
    Management, pages 41C68. IT University of Copenhagen, 2001
 7. C.B. Jones and C.A.Middelburg A typed logic of partial functions reconstructed
    classically. In Acta Inform. 31 5 (1994), pp. 399C430
A     Another example: the Schorre-Waite algorithm
A.1    The Program
Types and Variables The Schorre-Waite program to be verified, together with
a type definition and three variable declarations, is depicted in Figure 5. In the
program, we use some abbreviations for conciseness.
          CONDITIONwh (p 6= nil ? true : ((t = nil) ? false : ¬t → mk)
           CONDITION1             (t = nil ? true : t → mk)
           CONDITION2                     (p → chk)
The program is an elaborative implementation of the depth first search algo-
rithm. The search path is stored in a linked list, of which the links reuses the
memory cells for the field l or r.



Type T : Rec(l : P(T), r : P(T), chk : boolean, mk : boolean))
Three variables: root, t, p declared with type P(T).

(1) t := root;
(2) p := nil;
(3) while (CONDITIONwh ) do //stack not empty or t not explored;
(4) begin
(5)     if (CONDITION1 )//t is already explored or t is nil;
(6)     then
(7)          if (CONDITION2 ) then //POP;
(8)             begin q := t; t := p; p := p → r; t → r := q; end
(9)         else //TRY right neighbor;
(10)            begin
(11)                q := t; t := p → r; p → r := p → l;
(12)                p → l := q; p → chk := true;
(13)            end
(14)    else //t is not explored. PUSH t into the stack;
(15)        begin
(16)            q := p; p := t; t := t → l; p → l := q;
(17)            p → mk := true; p → chk := false;
(18)        end
(19) end



                       Fig. 5. The Schorr-Waite Algorithm



A.2    Recursive functions
We use two constants L0 and R0 to represent the edges. They are two maps. For
a node x in the graph, L0 (x) and R0 (x) are respectively the left-neighbor and
right-neighbor of x in the initial graph. The constants r0 is the starting node.
The constant NS0 represents the smallest set satisfying the following properties.
 – r0 ∈ NS0 ;
 – x ∈ NS0 ∧ L0 (x) 6= nil ⇒ L0 (x) ∈ NS0 ;
 – x ∈ NS0 ∧ R0 (x) 6= nil ⇒ R0 (x) ∈ NS0 .
    The definitions of the recursive functions used in the specification and the
proof are depicted in Figure 6. The function Stack(x) retrieves the segment of
the current path starting from x. The boolean-typed function isAcyclic(x) as-
serts that the list x is acyclic. The boolean-typed function PathProp asserts the
properties about the current path.
    The memory scope over-approximations for some functions are as follow.
             Recursive Functions Memory scope over-approximations
                NextNode(x)           (x = nil)?∅ : &x → chk
                 Explored(x)         (x = nil)?∅ : {&x → mk}
                   Stack(x)        {Block(x)|x ∈ rng(Stack(x))}
                 isAcyclic(s)                    ∅
Let MarkedFldMk be {&y → mk|y ∈ NS0 ∧ y → mk}. As
                Explored(x) ∧ x ∈ NS0 ⇒ &x → mk ∈ MarkedFldMk
we have the following properties.
       InPath(x) ∧ rng(Stack(x)) ⊆ NS0 ⇒
            M(InPath)(x) ⊆ {Block(y)|y ∈ rng(Stack(x))} ∪ MarkedFldMk

       OutPath(s) ∧ s ⊆ NS0 ⇒
           M(OutPath)(s) ⊆ {Block(x)|x ∈ s} ∪ MarkedFldMk



A.3     The specification
Let M Set be {&p, &t, &q} ∪ {Block(x)|x ∈ NS0 }. Notice that M(Set) is ∅. The
program can be specified as follow.
      Outlying(ρ  0 , M Set) ∧ root = r0
        x∈NS0 ((¬x → mk) ∧ (¬x → chk) ∧ (x → l = L0 (x)) ∧ (x → r = R0 (x)))
      V

          V{the program}
      ρ ∧ x∈NS0 (x → mk ∧ x → chk ∧ (x → l = L0 (x) ∧ (x → r = R0 (x))

A.4     The proof
The main part of the program under verification is a while-statement. The in-
variant of this while-statement is as follow.
   Outlying(ρ0 , M Set) ∧ Acyclic(Stack(p)) ∧ OutPath(NS0 − rng(Stack(p)))∧
   InPath(p) ∧ (NextNode(p) = t)
  NextNode(x : P(T )) : P(T )) , (x = nil)?r0 : (x → chk?R0 (x) : L0 (x))
  Explored(x : P(T )) : boolean , (x = nil)?true : x → mk
  Stack(x : P(T )) : SeqOf(P(T )) ,
        (x = nil)?[ ] : x⌢ Stack(x → chk?x → r : x → l)

  isAcyclic(s : SeqOf(P(T ))) : boolean ,
          s = []?true : head(s) 6∈ rng(tail(s)) ∧ isAcyclic(tail(s))

  InPath(x : P(T )) : boolean , x = nil?true :
      x ∈ NS0 ∧ x → mk = true∧
                                                                              
        x → chk?((NextNode(x → r) = x) ∧ (x → l = L0 (x)) ∧ Explored(L0 (x)) :
                                                                                 ∧
               ((NextNode(x → l) = x) ∧ (x → r = R0 (x))
      InPath(x → chk?x → r : x → l)

            : SetOf(P(T )) : boolean ,
  OutPath(x                                                                  
      V       x → l = L0 (x) ∧ x → r = R0 (x)∧
        y∈x   (x → mk?(x → chk ∧ Explored(L0 (x)) ∧ Explored(R0 (x))) : true)




                 Fig. 6. The recursive functions used in the proof



In the rest of this paper, we use SW INV to denote this formula. The framework
of our proof is depicted in Figure 7. In the rest part of this section, we will prove
the assertions about the sequential statements in line (7), (9) and (11).



A.5    The assertions about the assignment sequences


The assignments in line (8). Let EXPAND1 be the following formula.

      Outlying(ρ0 , M Set) ∧ Acyclic(Stack(← p−→−−r)) ∧ InPath(←
                                                               p−
                                                                →−−r)∧
      (NextNode(p → r) = p ) ∧ OutPath(NS0 − { p } − rng(Stack(←
                  ← −−−     ←
                            −                       ←−              p−→−−r)))∧
               ←−                  ←−     ←−       ←−    ←−
      Explored( t ) ∧ Explored(L0 ( p )) ∧ t = R0 ( p ) ∧ p → mk

Form the definition of memory scope terms, and the properties about over-
approximation of M(InPath) and M(OutPath),



   EXPAND1 ⇒ (M(EXPAND1 ) ∩ M Set) ⊆
             {Block(x)|x ∈ NS0 − {p}} ∪ MarkedFldMk ∪ {&p → mk}∪
             (t = nil?∅ : {&t → chk}) ∪ (L0 (p) = nil?∅ : {&L0 (p) → chk})
     {Outlying(ρ
      V            0 , M Set) ∧ (root = r0 )∧

         x∈NS0 ((¬x   → mk) ∧ (¬x → chk) ∧ (x → l = L0 (x)) ∧ (x → r = R0 (x)))}
(1) t := root;
(2) p := nil;
     {Outlying(ρ0 , M Set} ∧ t = root ∧ p = nil}
  ⇒ {SW INV}
(3) while (CONDITIONwh ) do //stack not empty or t not explored;
(4) begin
        {SW INV ∧ CONDITIONwh }
(5)     if (CONDITION1 )//t is already explored or t is nil;
(6)     then
            {SW INV ∧ CONDITIONwh ∧ CONDITION1 }
(7)          if (CONDITION2 ) then //POP;
                {SW INV ∧ CONDITIONwh ∧ CONDITION1 ∧ CONDITION2 }
(8)             begin q := t; t := p; p := p → r; t → r := q; end
                {SW INV}
(9)         else //TRY right neighbor;
                {SW INV ∧ CONDITIONwh ∧ CONDITION1 ∧ ¬CONDITION2 }
(10)            begin
(11)                   q := t; t := p → r; p → r := p → l;
(12)                   p → l := q; p → chk := true;
(13)            end
                {SW INV}
            {SW INV}
(14)    else //t is not explored. PUSH t into the stack;
            {SW INV ∧ CONDITIONwh ∧ ¬CONDITION1 }
(15)        begin
(16)            q := p; p := t; t := t → l; p → l := q;
(17)            p → mk := true; p → chk := false;
(18)        end
            {SW INV}
        {SW INV}
(19) end
     {SWVINV ∧ ¬CONDITIONwh }
⇒ ρ ∧ x∈NS0 (x → mk ∧ x → chk ∧ (x → l = L0 (x) ∧ (x → r = R0 (x))


                 Fig. 7. The Schorr-Waite Algorithm with Proof
So we have M(EXPAND1 ) ∩ {&q, &t, &p, &p → r} = nil, thus

         {SW INV ∧ CONDITIONwh ∧ CONDITION1 ∧ CONDITION2 }
       ⇒ EXPAND1 ∧ (p 6= nil)
           ↑ ρ1    EXPAND1
         Outlying(ρ1 , {&q, &t, &p, &p → r}) ∧ (p 6= nil)
               begin q := t; t := p; p := p → r; t → r := q; end
         ρ1 ∧ (q = ←
                   −t ) ∧ (t = ←−
                                p ) ∧ (p = ←
                                           p−→−−r) ∧ (t → r = ←
                                                              −
                                                              t)
           ↓ ρ1    EXPAND1
         EXPAND1 ∧ (t = ←  −
                           p ) ∧ (p = ←
                                      p−→−−r) ∧ (t → r = ←
                                                         −t)
       ⇒ {SW INV}


The assignments in line (10-13). Let EXPAND2 be the formula

            Outlying(ρ0 , M Set) ∧ Acyclic(Stack(←
                                                 p−
                                                  →−−r))∧
                                          ←−−−             ←−−−
            OutPath(NS0 − p − rng(Stack(p → l))) ∧ InPath(p → l)∧
                      ←−−−
            (NextNode(p → l) = p) ∧ (←−
                                      t = L0 (p)) ∧ (←
                                                     p−
                                                      →−−r = R0 (p))

We have

     EXPAND2 ⇒ (M(EXPAND2 ) ∩ M Set) ⊆
               {Block(x)|x ∈ NS0 − {p}} ∪ {&p → mk, &p}
             ⇒ M(EXPAND2 ) ∩ {&q, &t, &p → l, &p → r, &p → chk} = ∅

Thus we have the following proof,


     {SW INV ∧ (CONDITIONwh ) ∧ (CONDITION1 ) ∧ ¬(CONDITION2 )}
⇒ {EXPAND2 ∧ (p 6= nil)}
        ↑ ρ2    EXPAND2
     {Outlying(ρ2 , {&q, &t, &p → l, &p → r, &p → chk}) ∧ (p 6= nil)}
(10) begin
(11)    q := t; t := p → r; p → r := p → l;
(12)    p → l := q; p → chk := true;
(13) end
     {ρ2 ∧ (q = ←−
                 t ) ∧ (t = ←
                            p− →−−r) ∧ (p → r = ←  −−−
                                                  p → l)} ∧ (p → l = ←−
                                                                      t )∧
      (p → chk = true)}
        ↑ ρ2    EXPAND2
     {EXPAND2 ∧ (q = ←    −
                          t ) ∧ (t = p←−→−−r) ∧ (p → r = ← −−−
                                                          p → l)} ∧ (p → l = ←
                                                                             −
                                                                             t )∧
      (p → chk = true)}
⇒ {SW INV}


The assignments in line (11) Let EXPAND3 be the formula

   Outlying(ρ0 , M Set) ∧ OutPath(NS0 − ←   −
                                            t − rng(Stack(← −p ))) ∧ InPath(←
                                                                            −
                                                                            p )∧
             ←−     ←
                    −     ← −−−       ←−     ← −−−       ←−
   (NextNode( p ) = t ) ∧ t → l = L0 ( t ) ∧ t → r = R0 ( t )
Because
          EXPAND3 ⇒ (M(EXPAND3 ) ∩ M Set) ⊆
                    {Block(x)|x ∈ NS0 − t} ∪ (p = nil?∅ : {p → mk})
                  ⇒ M(EXPAND3 ) ∩ {&q, &p} ∪ Block(&t) = ∅
Thus

     {SW INV ∧ (CONDITIONwh ) ∧ ¬(CONDITION1 )}
⇒ {(t 6= nil) ∧ EXPAND3 }
        ↑ ρ3    EXPAND3
     Outlying(ρ3 , {&q, &p} ∪ Block(&t)) ∧ (t 6= nil)
(15) begin
(16)    q := p; p := t; t := t → l; p → l := q;
(17)    p → mk := true; p → chk := false;
(18) end
                                         ←−−−
     {ρ3 ∧ (q = ←p ) ∧ (p = ←
                 −           −t ) ∧ (t = t → l) ∧ (p → l = ←
                                                           −
                                                           p )∧
      (p → mk = true) ∧ (p → chk = false)}
        ↓ ρ3    EXPAND3
                                    ←−−−
     {(q = ←p ) ∧ (p = ←
            −           −
                        t ) ∧ (t = t → l) ∧ (p → l = ←−
                                                      p ) ∧ (p → mk = true)∧
      (p → chk = false) ∧ EXPAND3 }
⇒ {SW INV}

B      Yet another example: selection-sort program with
       indirectly specified code
In this section, we verify an implementation of the selection-sort algorithm. This
example shows that Scope Logic can verify a template, which is a program with
a implicitly specified expression.

B.1    the program
Variables This program has five variables: four variables tmp, i, j, and k with
type int, and the variable a with type ARR(int, 100).
    The boolean expression order appeared in this program is an implicitly spec-
ified expression containing two free variables x1 and x2 . This expression satisfies
the following conditions
 1. ∀x, y · order[x/x1 ][y/x2 ] ∨ order[y/x1 ][y/x2 ];
 2. ∀x, y, z · order[x/x1 ][y/x2 ] ∧ order[y/x1 ][z/x2 ] ⇒ order[x/x1 ][z/x2 ];
 3. ∀x, y · order[x/x1 ][y/x2 ] ∧ order[y/x1 ][x/x2 ] ⇒ x = y;
 4. M(order) ∩ M Set = ∅, where M Set is {&tmp, &i, &j, &k} ∪ Block(&a).
 5. F V (M(order)) = ∅
The expression specifies a total order. Further more, the memory scope term of
order contains no free variables, and is disjoint with the memory units that may
be modified by this program.
Variables:
i, j, k, tmp declared with type int.
a declared with type ARR(int, 100)

(1) i := 0;
(2) while (i < 100) do
(3) begin
(4)     j := i + 1; k := i;
(5)     while (j < 100) do
(6)     begin
(7)         if order(a[j], a[k]) then k := j; else skip;
(8)         j := j + 1;
(9)     end
(10)    tmp := a[i]; a[i] := a[k]; a[k] := tmp; i := i + 1;
(11) end



                       Fig. 8. The Selection-Sort Algorithm


B.2    The Recursive Functions and Their Memory Scope Functions

The recursive functions used in this proof are depicted in Figure 9. OrderSet(x, y)
means that x is less than or equal to all the elements in y w.r.t. order. The func-
tion OrderSetSet(s1 , s2 ) means that all elements in s1 is less than all elements in
s2 w.r.t. order. The function DataSet(l, r) represents the set of elements indexed
from l to r in a. AllBut(l, r, i, j) represents the set of elements indexed from l to
r in the array a except that a[i] and a[j] are excluded. The function arrLocs(l, r)
computes the set memory units used by the array elements index from l to r.
The corresponding simplified memory scope functions (or over-approximation)
are depicted in Figure 10.


OrderSet(x : int, s : SetOf(int)) : bool , y∈s order(x, y)
                                                 V

OrderSetSet(s1 : SetOf(int), s2 : SetOf(int)) : bool , y∈s1 OrderSet(y, s2 )
                                                           V

Sorted(l : int, r : int) : bool
         , (r ≤ l)?true : order(a[l], a[l + 1]) ∧ Sorted(l + 1, r)
DataSet(l : int, r : int) : SetOf(int)
         , (r < l)?∅ : {a[l]} ∪ DataSet(l + 1, r)
AllBut(l : int, r : int, i : int, j : int) : SetOf(int)
         , (r < l)?∅ : ((l = i ∨ l = j)?∅ : {a[i]}) ∪ AllData(l + 1, r)
arrLocs(l : int, r : int) : SetOf(Ptr)
         , (r < l)?∅ : {&a[l]} ∪ arrLocs(l + 1, r)


   Fig. 9. The recursive functions used to prove the selection-sort algorithm
        Recursive functions Memory Scope functions (or over-aproximation)
       OrderSet, OrderSetSet                  M(order)
                arrLocs                            ∅
      Sorted(l, r), DataSet(l, r)           arrLocs(l, r)
           AllBut(l, r, i, j)       arrLocs(l, r) − {&a[i], &a[j]}


          Fig. 10. The memory scope functions or over-approximations




                     Fig. 11. The properties used in the proof




B.3    The Specification
This is an implementation of the selection-sort algorithm. This algorithm sort
the integers in the array. It modifies only the memory units in M Set. So the
specification is as follow.
            Outlying(ρ0 , M Set) ∧ S0 = DataSet(0, 99)
                {The program}
            Outlying(ρ0 , M Set) ∧ S0 = DataSet(0, 99) ∧ Sorted(0, 99)

B.4    The Proof in Code
The invariant of the outer while-statement, denoted as INVo , is as follow.
         Outlying(ρo , M Set) ∧ (i ≤ 100)∧
         Sorted(0, i − 1) ∧ OrderSetSet(DataSet(0, i − 1), DataSet(i, 99))∧
         S0 = DataSet(0, 99)

M(INVo ) is
                     M(ρo ) ∪ {&i} ∪ M(order) ∪ arrLocs(0, 99)
The invariant of the inner while-statement, denoted as INVi , is as follow.
       Outlying(ρi , {&k, &j})∧
       OrderSet(a[k], DataSet(i, j − 1)) ∧ (0 ≤ i ≤ k < 100) ∧ (0 ≤ j ≤ 100)

Let EXP be the formula
                                          ←−
      Outlying(ρ0 , M Set) ∧ Sorted(0, i − 1)∧
                               ←−                ←
                                                 −      ←
                                                        −          ← − ←−
      OrderSetSet(DataSet(0, i − 1), AllBut( i , 99, i , k) ∪ {a[i], a[k]})∧
               ←−           ←−      ←−               ←− ←   −            ←− ←−
      OrderSet(a[k], AllBut( i , 99, i , k)) ∧ order(a[k], a[i]) ∧ order(a[k], a[k])
M(EXP) is
                                                             ←−
                 M(ρo ) ∪ {&k} ∪ arrLocs(0, 99) − {&a[k], &a[ i ]}
    Figure 12 presents the proof of this program with indirectly specified expres-
sion. The following is some properties used in this proof.

       0 ≤ l < i, j < r ≤ 99 ⇒ DataSet(l, r) = AllBut(l, r, i, j) ∪ {a[i], a[j]}

               order(x, y) ∧ OrderSet(x, s) ⇒ OrderSet(x, s ∪ {y})
       OrderSetSet(s1 , s2 ) ∧ OrderSet(x, s2 ) ⇒ OrderSetSet(s1 ∪ {x}, s2 )
     {Outlying(ρ0 , M Set) ∧ S0 = DataSet(0, 99)}
(1) i := 0;
     {Outlying(ρ0 , M Set) ∧ S0 = DataSet(0, 99) ∧ (i = 0)}
⇒ {INVo }
(2) while (i < 100) do
(3) begin
        {INVo ∧ (i < 100)}
(4)     j := i + 1; k := i;
        {INVo ∧ OrderSet(a[k], DataSet(i, j − 1)) ∧ (0 ≤ i ≤ k < 100) ∧ (0 ≤ j ≤ 100)}
            ↑ ρi    INV0
        {INVi }
(5)     while (j < 100) do
(6)     begin
            {INVi ∧ (j < 100)}
(7)         if order(a[j], a[k]) then k := j; else skip;
            {Outlying(ρi , {&k, &j}) ∧ order(a[k], a[j]) ∧ (0 ≤ i ≤ k < 100)∧
              OrderSet(a[k], DataSet(i, j − 1)) ∧ (j < 100)}
(8)         j := j + 1;
            {INVi }
(9)     end
        {INVi ∧ ¬(j < 100)}
     ⇒ {Outlying(ρi , {&k, &j}) ∧ OrderSet(a[k], DataSet(i, 99))}
             ↓ ρi    INV0
        {INVo ∧ OrderSet(a[k], DataSet(i, 99)) ∧ (0 ≤ i ≤ k < 100)}
     ⇒ {(0 ≤ i ≤ k < 100) ∧ EXP}
            ↑ ρ2     EXP
        {Outlying(ρ2 , {&i, &tmp, &a[i], &a[k]}) ∧ (0 ≤ i, k < 100)}
(10)    tmp := a[i]; a[i] := a[k]; a[k] := tmp; i := i + 1;
                         ←−              ←−          ←
                                                     −
        {ρ2 ∧ (a[i-1] = a[k]) ∧ (a[k] = a[i]) ∧ (i = i + 1)}
            ↓ ρ2     EXP
                    ←−              ←
                                    −          ←−
        {(a[i-1] = a[k]) ∧ (a[k] = a[i]) ∧ (i = i + 1) ∧ EXP}
     ⇒ {INVo }
(11) end
     {INVo ∧ ¬(i < 100)}
⇒ {Outlying(ρ0 , M Set) ∧ S0 = DataSet(0, 99) ∧ Sorted(0, 99)}


                Fig. 12. The Selection-Sort Algorithm with Proof
