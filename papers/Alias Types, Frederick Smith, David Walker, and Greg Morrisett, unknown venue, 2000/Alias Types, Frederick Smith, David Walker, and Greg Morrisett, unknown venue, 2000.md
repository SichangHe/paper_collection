                                Alias Types ?

                Frederick Smith, David Walker, and Greg Morrisett

                                   Cornell University



        Abstract. Linear type systems allow destructive operations such as ob-
        ject deallocation and imperative updates of functional data structures.
        These operations and others, such as the ability to reuse memory at
        different types, are essential in low-level typed languages. However, tra-
        ditional linear type systems are too restrictive for use in low-level code
        where it is necessary to exploit pointer aliasing. We present a new typed
        language that allows functions to specify the shape of the store that they
        expect and to track the flow of pointers through a computation. Our type
        system is expressive enough to represent pointer aliasing and yet safely
        permit destructive operations.


1     Introduction
Linear type systems [26, 25] give programmers explicit control over memory
resources. The critical invariant of a linear type system is that every linear value
is used exactly once. After its single use, a linear value is dead and the system
can immediately reclaim its space or reuse it to store another value. Although
this single-use invariant enables compile-time garbage collection and imperative
updates to functional data structures, it also limits the use of linear values. For
example, x is used twice in the following expression: let x = h1, 2i in let y =
f st(x) in let z = snd(x) in y + z. Therefore, x cannot be given a linear type,
and consequently, cannot be deallocated early.
    Several authors [26, 9, 3] have extended pure linear type systems to allow
greater flexibility. However, most of these efforts have focused on high-level user
programming languages and as a result, they have emphasized simple typing
rules that programmers can understand and/or typing rules that admit effective
type inference techniques. These issues are less important for low-level typed
languages designed as compiler intermediate languages [22, 18] or as secure mo-
bile code platforms, such as the Java Virtual Machine [10], Proof-Carrying Code
(PCC) [13] or Typed Assembly Language (TAL) [12]. These languages are desi-
gned for machine, not human, consumption. On the other hand, because systems
such as PCC and TAL make every machine operation explicit and verify that
each is safe, the implementation of these systems requires new type-theoretic
mechanisms to make efficient use of computer resources.
?
    This material is based on work supported in part by the AFOSR grant F49620-97-
    1-0013 and the National Science Foundation under Grant No. EIA 97-03470. Any
    opinions, findings, and conclusions or recommendations expressed in this publication
    are those of the authors and do not reflect the views of these agencies.

G. Smolka (Ed.): ESOP/ETAPS 2000, LNCS 1782, pp. 366–381, 2000.
c Springer-Verlag Berlin Heidelberg 2000
                                                                 Alias Types   367

    In existing high-level typed languages, every location is stamped with a single
type for the lifetime of the program. Failing to maintain this invariant has re-
sulted in unsound type systems or misfeatures (witness the interaction between
parametric polymorphism and references in ML [23, 27]). In low-level langu-
ages that aim to expose the resources of the underlying machine, this inva-
riant is untenable. For instance, because machines contain a limited number
of registers, each register cannot be stamped with a single type. Also, when
two stack-allocated objects have disjoint lifetimes, compilers naturally reuse the
stack space, even when the two objects have different types. Finally, in a low-
level language exposing initialization, even the simplest objects change type. For
example, a pair x of type hint, inti may be created as follows:

                   malloc x, 2 ; (* x has type hjunk, junki *)
                   x[1]:=1 ;     (* x has type hint, junki *)
                   x[2]:=2 ;     (* x has type hint, inti *)
                  ..
                   .
    At each step in this computation, the storage bound to x takes on a different
type ranging from nonsense (indicated by the type junk) to a fully initialized pair
of integers. In this simple example, there are no aliases of the pair and therefore
we might be able to use linear types to verify that the code is safe. However,
in a more complex example, a compiler might generate code to compute the
initial values of the tuple fields between allocation and the initializing assign-
ments. During the computation, a register allocator may be forced to move the
uninitialized or partially initialized value x between stack slots and registers,
creating aliases:
       STACK                R1                           STACK            R1




                  OBJECT                                         OBJECT
                                      Copy To Register




    If x is a linear value, one of the pointers shown above would have to be
“invalidated” in some way after each move. Unfortunately, assuming the pointer
on the stack is invalidated, future register pressure may force x to be physically
copied back onto the stack. Although this additional copy is unnecessary because
the register allocator can easily remember that a pointer to the data structure
remains on the stack, the limitations of a pure linear type system require it.
    Pointer aliasing and data sharing also occur naturally in other data structures
introduced by a compiler. For example, compilers often use a top-of-stack pointer
and a frame pointer, both of which point to the same data structure. Compiling
a language like Pascal using displays [1] generalizes this problem to having an
arbitrary (but statically known) number of pointers into the same data structure.
In each of these examples, a flexible type system will allow aliasing but ensure
that no inconsistencies arise. Type systems for low-level languages, therefore,
should support values whose types change even when those values are aliased.
368      F. Smith, D. Walker, and G. Morrisett

    We have devised a new type system that uses linear reasoning to allow me-
mory reuse at different types, object initialization, safe deallocation, and tracking
of sharing in data structures. This paper formalizes the type system and provi-
des a theoretical foundation for safely integrating operations that depend upon
pointer aliasing with type systems that include polymorphism and higher-order
functions.
    We have extended the TAL implementation with the features described in
this paper.1 It was quite straightforward to augment the existing Fω -based type
system because many of the basic mechanisms, including polymorphism and
singleton types, were already present in the type constructor language. Popcorn,
an optimizing compiler for a safe C-like language, generates code for the new
TAL type system and uses the alias tracking features of our type system.
    The Popcorn compiler and TAL implementation demonstrate that the ideas
presented in this paper can be integrated with a practical and complete pro-
gramming language. However, for the sake of clarity, we only present a small
fragment of our type system and, rather than formalizing it in the context of
TAL, we present our ideas in terms of a more familiar lambda calculus. Section 2
gives an informal overview of how to use aliasing constraints, a notion which ex-
tends conventional linear type systems, to admit destructive operations such
as object deallocation in the presence of aliasing. Section 3 describes the core
language formally, with emphasis on the rules for manipulating linear aliasing
constraints. Section 4 extends the language with non-linear aliasing constraints.
Finally, Section 5 discusses future and related work.


2     Informal Overview

The main feature of our new type system is a collection of aliasing constraints.
Aliasing constraints describe the shape of the store and every function uses them
to specify the store that it expects. If the current store does not conform to the
constraints specified, then the type system ensures that the function cannot
be called. To illustrate how our constraints abstract a concrete store, we will
consider the following example:
                      SP             STACK                   R1


                                      577

                                     TRUE
                                                  42




Here, sp is a pointer to a stack frame, which has been allocated on the heap (as
might be done in the SML/NJ compiler [2], for instance). This frame contains a
pointer to a second object, which is also pointed to by register r1 .
   In our program model, every heap-allocated object occupies a particular me-
mory location. For example, the stack frame might occupy location `s and the
1
    See http://www.cs.cornell.edu/talc for the latest software release.
                                                                     Alias Types   369

second object might occupy location `o . In order to track the flow of pointers to
these locations accurately, we reflect locations into the type system: A pointer
to a location ` is given the singleton type ptr(`). Each singleton type contains
exactly one value (the pointer in question). This property allows the type sy-
stem to reason about pointers in a very fine-grained way. In fact, it allows us to
represent the graph structure of our example store precisely:
                     SP                  STACK                  R1


                    PTR(ls)        ls:    INT                  PTR(lo)


                                         BOOL
                                                   lo:   INT

                                         PTR(lo)



We represent this picture in our formal syntax by declaring the program variable
sp to have type ptr(`s ) and r1 to have type ptr(`o ). The store itself is described
by the constraints {`s 7→ hint, bool, ptr(`o )i} ⊕ {`o 7→ hinti}, where the type
hτ1 , . . . , τn i denotes a memory block containing values with types τ1 through τn .
     Constraints of the form {` 7→ τ } are a reasonable starting point for an
abstraction of the store. However, they are actually too precise to be useful
for general-purpose programs. Consider, for example, the simple function deref,
which retrieves an integer from a reference cell. There are two immediate pro-
blems if we demand that code call deref when the store has a shape described
by {` 7→ hinti}. First, deref can only be used to derefence the location `, and
not, for example, the locations `0 or `00 . This problem is easily solved by adding
location polymorphism. The exact name of a location is usually unimportant; we
need only establish a dependence between pointer type and constraint. Hence
we could specify that deref requires a store {ρ 7→ hinti} where ρ is a location
variable instead of some specific location `. Second, the constraint {` 7→ hinti}
specifies a store with exactly one location ` although we may want to dereference
a single integer reference amongst a sea of other heap-allocated objects. Since
deref does not use or modify any of these other references, we should be able
to abstract away the size and shape of the rest of the store. We accomplish this
task using store polymorphism. An appropriate constraint for the function deref
is  ⊕ {ρ 7→ hinti} where  is a constraint variable that may instantiated with
any other constraint.
     The third main feature of our constraint language is the capability to distin-
guish between linear constraints {ρ 7→ τ } and non-linear constraints {ρ 7→ τ }ω .
Linear constraints come with the additional guarantee that the location on the
left-hand side of the constraint (ρ) is not aliased by any other location (ρ0 ). This
invariant is maintained despite the presence of location polymorphism and store
polymorphism. Intuitively, because ρ is unaliased, we can safely deallocate its
memory or change the types of the values stored there. The key property that ma-
kes our system more expressive than traditional linear systems is that although
the aliasing constraints may be linear, the pointer values that flow through a
computation are not. Hence, there is no direct restriction on the copying and
reuse of pointers.
370       F. Smith, D. Walker, and G. Morrisett

    The following example illustrates how the type system uses aliasing con-
straints and singleton types to track the evolution of the store across a series of
instructions that allocate, initialize, and then deallocate storage. In this exam-
ple, the instruction malloc x, ρ, n allocates n words of storage. The new storage
is allocated at a fresh location ` in the heap and ` is substituted for ρ in the
remaining instructions. A pointer to ` is substitued for x. Both ρ and x are
considered bound by this instruction. The free instruction deallocates storage.
Deallocated storage has type junk and the type system prevents any future use
of that space.
      Instructions           Constraints (Initially the constraints )
1. malloc sp, ρ1 , 2;         ⊕ {ρ1 7→ hjunk, junki}                  sp : ptr(ρ1 )
2. sp[1]:=1;                  ⊕ {ρ1 7→ hint, junki}
3. malloc r1 , ρ2 , 1;        ⊕ {ρ1 7→ hint, junki, ρ2 7→ hjunki}     r1 : ptr(ρ2 )
4. sp[2]:=r1 ;                ⊕ {ρ1 7→ hint, ptr(ρ2 )i, ρ2 7→ hjunki}
5. r1 [1]:=2;                 ⊕ {ρ1 7→ hint, ptr(ρ2 )i, ρ2 7→ hinti}
6. free r1 ;                  ⊕ {ρ1 7→ hint, ptr(ρ2 )i, ρ2 7→ junk}
7. free sp;                   ⊕ {ρ1 7→ junk, ρ2 7→ junk}
    Again, we can intuitively think of sp as the stack pointer and r1 as a register
that holds an alias of an object on the stack. Notice that on line 5, the initia-
lization of r1 updates the type of the memory at location ρ2 . This has the effect
of simultaneously updating the type of r1 and of sp[1]. Both of these paths are
similarly affected when r1 is freed in the next instruction. Despite the presence
of the dangling pointer at sp[1], the type system will not allow that pointer to
be derefenced.
    By using singleton types to accurately track pointers, and aliasing constraints
to model the shape of the store, our type system can represent sharing and
simultaneously ensure safety in the presence of destructive operations.


3     The Language of Locations

This section describes our new type-safe “language of locations” formally. The
syntax for the language appears in Figure 1.


3.1     Values, Instructions, and Programs

A program is a pair of a store (S ) and a list of instructions (ι). The store maps
locations (`) to values (v). Normally, the values held in the store are memory
blocks (hτ1 , . . . , τn i), but after the memory at a location has been deallocated,
that location will point to the unusable value junk. Other values include integer
constants (i), variables (x or f ), and, of course, pointers (ptr(`)).
   Figure 2 formally defines the operational semantics of the language.2 The
main instructions of interest manipulate memory blocks. The instruction
2
    Here and elsewhere, the notation X[c1 , . . . , cn /x1 , . . . , xn ] denotes capture-avoiding
    substitution of c1 , . . . , cn for variables x1 , . . . , xn in X.
                                                                             Alias Types          371


    ` ∈ Locations       ρ ∈ LocationVar            ∈ ConstraintVar           x, f ∈ ValueVar

  locations      η ::= ` | ρ
  constraints    C ::= ∅ |  | {η 7→ τ } | C1 ⊕ C2
  types          τ ::= int | junk | ptr(η) | hτ1 , . . . , τn i | ∀[∆; C].(τ1 , . . . , τn )→0
  value ctxts    Γ ::= · | Γ, x:τ
  type ctxts     ∆ ::= · | ∆, ρ | ∆, 
  values         v ::= x | i | junk | ptr(`) | hv1 , . . . , vn i | fix f [∆; C; Γ ].ι | v[η] | v[C]
  instructions    ι ::= malloc x, ρ, n; ι | x=v[i]; ι | v[i]:=v 0 ; ι | free v; ι |
                        v(v1 , . . . , vn ) | halt
  stores         S ::= {`1 7→ v1 , . . . , `n 7→ vn }
  programs       P ::= (S , ι)


                          Fig. 1. Language of Locations: Syntax


malloc x, ρ, n allocates an unitialized memory block (filled with junk) of size n
at a new location `, and binds x to the pointer ptr(`). The location variable ρ,
bound by this instruction, is the static representation of the dynamic location
`. The instruction x=v[i] binds x to the ith component of the memory block
pointed to by v in the remaining instructions. The instruction v[i]:=v 0 stores v 0
in the ith component of the block pointed to by v. The final memory mana-
gement primitive, free v, deallocates the storage pointed to by v. If v is the
pointer ptr(`) then deallocation is modeled by updating the store (S) so that
the location ` maps to junk.
    The program ({}, malloc x, ρ, 2; x[1]:=3; x[2]:=5; free x; halt ) allocates, in-
itializes and finally deallocates a pair of integers. Its evaluation is shown below:
Store                     Instructions
{}                        malloc x, ρ, n         (* allocate new location `,      *)
                                                 (* substitute ptr(`), ` for x, ρ *)
{` 7→ hjunk, junki}       ptr(`)[1]:=3           (* initialize field 1            *)
{` 7→ h3, junki}          ptr(`)[2]:=5           (* initialize field 2            *)
{` 7→ h3, 5i}             free ptr(`)            (* free storage                  *)
{` 7→ junk}
    A sequence of instructions (ι) ends in either a halt instruction, which stops
computation immediately, or a function application (v(v1 , . . . , vn )). In order to
simplify the language and its typing constructs, our functions never return. Ho-
wever, a higher-level language that contains call and return statements can be
compiled into our language of locations by performing a continuation-passing
style (CPS) transformation [14, 15]. It is possible to define a direct-style lan-
guage, but doing so would force us to adopt an awkward syntax that allows
functions to return portions of the store. In a CPS style, all control-flow trans-
fers are handled symmetrically by calling a continuation.
    Functions are defined using the form fix f [∆; C; Γ ].ι. These functions are
recursive (f may appear in ι). The context (∆; C; Γ ) specifies a pre-condition
372        F. Smith, D. Walker, and G. Morrisett

that must be satisfied before the function can be invoked. The type context ∆
binds the set of type variables that can occur free in the term; C is a collection
of aliasing constraints that statically approximates a portion of the store; and Γ
assigns types to free variables in ι.
    To call a polymorphic function, code must first instantiate the type variables
in ∆ using the value form: v[η] or v[C]. These forms are treated as values because
type application has no computational effect (types and constraints are only used
for compile-time checking; they can be erased before executing a program).



(S, malloc x, ρ, n; ι)             7−→ (S{` 7→ hjunk1 , . . . , junkn i}, ι[`/ρ][ptr(`)/x])
     where ` 6∈ S
(S{` 7→ v}, free ptr(`); ι) 7−→ (S{` 7→ junk}, ι)
     if v = hv1 , . . . , vn i
(S{` 7→ v}, ptr(`)[i]:=v 0 ; ι) 7−→ (S{` 7→ hv1 , . . . , vi−1 , v 0 , vi+1 , . . . , vn i}, ι)
     if v = hv1 , . . . , vn i and 1 ≤ i ≤ n
(S{` 7→ v}, x=ptr(`)[i]; ι) 7−→ (S{` 7→ v}, ι[vi /x])
     if v = hv1 , . . . , vn i and 1 ≤ i ≤ n
(S, v(v1 , . . . , vn ))            7−→ (S, ι[c1 , . . . , cm /β1 , . . . , βm ][v 0 , v1 , . . . , vn /f, x1 , . . . , xn ])
     if v = v 0 [c1 , . . . , cm ]
     and v 0 = fix f [∆; C; x1 :τ1 , . . . , xn :τn ].ι
     and Dom(∆) = β1 , . . . , βm            (where β ranges over ρ and )


                      Fig. 2. Language of Locations: Operational Semantics




3.2     Type Constructors

There are three kinds of type constructors: locations3 (η), types (τ ), and aliasing
constraints (C). The simplest types are the base types, which we have chosen
to be integers (int). A pointer to a location η is given the singleton type ptr(η).
The only value in the type ptr(η) is the pointer ptr(η), so if v1 and v2 both have
type ptr(η), then they must be aliases. Memory blocks have types (hτ1 , . . . , τn i)
that describe their contents.
    A collection of constraints, C, establishes the connection between pointers of
type ptr(η) and the contents of the memory blocks they point to. The main form
of constraint, written {η 7→ τ }, models a store with a single location η containing
a value of type τ . Collections of constraints are constructed from more primitive
constraints using the join operator (⊕). The empty constraint is denoted by ∅.
We often abbreviate {η 7→ τ } ⊕ {η 0 7→ τ 0 } with {η 7→ τ, η 0 7→ τ 0 }.
3
    We use the meta-variable ` to denote concrete locations, ρ to denote location varia-
    bles, and η to denote either.
                                                                            Alias Types      373

3.3    Static Semantics
Store Typing The central invariant maintained by the type system is that the
current constraints C are a faithful description of the current store S. We write
this store-typing invariant as the judgement ` S : C. Intuitively, whenever a
location ` contains a value v of type τ , the constraints should specify that location
` maps to τ (or an equivalent type τ 0 ). Formally:

                        ·; · `v v1 : τ1        ···       ·; · `v vn : τn
                 ` {`1 7→ v1 , . . . , `n 7→ vn } : {`1 7→ τ1 , . . . , `n 7→ τn }

where for 1 ≤ i ≤ n, the locations `i are all distinct. And,

                                  ` S : C0     · ` C0 = C
                                             `S:C

Instruction Typing Instructions are type checked in a context ∆; C; Γ . The jud-
gement ∆; C; Γ `ι ι states that the instruction sequence is well-formed. A related
judgement, ∆; Γ `v v : τ , ensures that the value v is well-formed and has type
τ. 4
    Our presentation of the typing rules for instructions focuses on how each rule
maintains the store-typing invariant. With this invariant in mind, consider the
rule for projection:

                         ∆; Γ `v v : ptr(η)
                                                                           
       ∆ ` C = C 0 ⊕ {η 7→ hτ1 , . . . , τn i} ∆; C; Γ, x:τi `ι ι    x 6∈ Γ
                       ∆; C; Γ `ι x=v[i]; ι                         1≤i≤n

The first pre-condition ensures that v is a pointer. The second uses C to deter-
mine the contents of the location pointed to by v. More precisely, it requires that
C equal a store description C 0 ⊕ {η 7→ hτ1 , . . . , τn i}. (Constraint equality uses ∆
to denote the free type variables that may appear on the right-hand side.) The
store is unchanged by the operation so the final pre-condition requires that the
rest of the instructions be well-formed under the same constraints C.
    Next, examine the rule for the assignment operation:

            ∆; Γ `v v : ptr(η)                ∆; Γ `v v 0 : τ 0
             0
∆ ` C = C ⊕ {η 7→ hτ1 , . . . , τn i}         ∆; C 0 ⊕ {η 7→ τafter }; Γ `ι ι
                                                                                     (1 ≤ i ≤ n)
                            ∆; C; Γ `ι v[i]:=v 0 ; ι

                  where τafter is hτ1 , . . . , τi−1 , τ 0 , τi+1 , . . . , τn i
Once again, the value v must be a pointer to some location η. The type of the
contents of η are given in C and must be a block with type hτ1 , . . . , τn i. This
time the store has changed, and the remaining instructions are checked under
the appropriately modified constraint C 0 ⊕ {η 7→ τafter }.
4
    The subscripts on `v and `ι are used to distinguish judgement forms and for no
    other purpose.
374     F. Smith, D. Walker, and G. Morrisett

    How can the type system ensure that the new constraints C 0 ⊕ {η 7→ τafter }
correctly describe the store? If v 0 has type τ 0 and the contents of the location
η originally has type hτ1 , . . . , τn i, then {η 7→ τafter } describes the contents of
the location η after the update accurately. However, we must avoid a situation
in which C 0 continues to hold an outdated type for the contents of the location
η. This task may appear trivial: Search C 0 for all occurrences of a constraint
{η 7→ τ } and update all of the mappings appropriately. Unfortunately, in the
presence of location polymorphism, this approach will fail. Suppose a value is
stored in location ρ1 and the current constraints are {ρ1 7→ τ, ρ2 7→ τ }. We
cannot determine whether or not ρ1 and ρ2 are aliases and therefore whether
the final constraint set should be {ρ1 7→ τ 0 , ρ2 7→ τ 0 } or {ρ1 7→ τ 0 , ρ2 7→ τ }.
    Our solution uses a technique from the literature on linear type systems.
Linear type systems prevent duplication of assumptions by disallowing uses of
the contraction rule. We use an analogous restriction in the definition of con-
straint equality: The join operator ⊕ is associative, and commutative, but not
idempotent. By ensuring that linear constraints cannot be duplicated, we can
prove that ρ1 and ρ2 from the example above cannot be aliases. The other equa-
lity rules are unsurprising. The empty constraint collection is the identity for ⊕
and equality on types τ is syntactic up to α-conversion of bound variables and
modulo equality on constraints. Therefore:
       ∆ ` {ρ1 7→ hinti} ⊕ {ρ2 7→ hbooli} = {ρ2 7→ hbooli} ⊕ {ρ1 7→ hinti}
but,
∆ 6` {ρ1 7→ hinti}⊕{ρ2 7→ hbooli} = {ρ1 7→ hinti}⊕{ρ1 7→ hinti}⊕{ρ2 7→ hbooli}
   Given these equality rules, we can prove that after an update of the store
with a value with a new type, the store typing invariant is preserved:
Lemma 1 (Store Update). If ` S{` 7→ v} : C ⊕ {` 7→ τ } and ·; · `v v 0 : τ 0
then ` S{` 7→ v 0 } : C ⊕ {` 7→ τ 0 } .
where S{` 7→ v} denotes the store S extended with the mapping ` 7→ v (provided
` does not already appear on the left-hand side of any elements in S).

Function Typing The rule for function application v(v1 , . . . , vn ) is the rule one
would expect. In general, v will be a value of the form v 0 [c1 ] · · · [cn ] where v 0
is a function polymorphic in locations and constraints and the type construc-
tors c1 through cn instantiate its polymorphic variables. After substituting c1
through cn for the polymorphic variables, the current constraints must equal
the constraints expected by the function v. This check guarantees that the no-
duplication property is preserved across function calls. To see why, consider the
polymorphic function foo where the type context ∆ is (ρ1 , ρ2 , ) and the con-
straints C are  ⊕ {ρ1 7→ hinti, ρ2 7→ hinti}:
    fix foo[∆; C; x:ptr(ρ1 ), y:ptr(ρ2 ), cont:∀[·; ].(int)→0].
         free x;      (* constraints =  ⊕ {ρ2 7→ hinti}                 *)
         z=y[0];      (* ok because y : ptr(ρ2 ) and {ρ2 7→ hinti} *)
         free y;      (* constraints =                                  *)
         cont(z)      (* return/continue                                 *)
                                                                 Alias Types      375

This function deallocates its two arguments, x and y, before calling its continua-
tion with the contents of y. It is easy to check that this function type-checks,
but should it? If foo is called in a state where ρ1 and ρ2 are aliases, a run-time
error will result when the second instruction is executed because the location
pointed to by y will already have been deallocated. Fortunately, our type system
guarantees that foo can never be called from such a state.
    Suppose that the store currently contains a single integer reference: {` 7→
h3i}. This store can be described by the constraints {` 7→ hinti}. If the program-
mer attempts to instantiate both ρ1 and ρ2 with the same label `, the function
call foo[`, `, ∅](ptr(`)) will fail to type check because the constraints {` 7→ hinti}
do not equal the pre-condition ∅ ⊕ {` 7→ hinti, ` 7→ hinti}.
    Figure 3 contains the typing rules for values and instructions. Note that the
judgement ∆ `wf τ indicates that ∆ contains the free type variables in τ .

3.4     Soundness
Our typing rules enforce the property that well-typed programs cannot enter
stuck states. A state (S, ι) is stuck when no reductions of the operational seman-
tics apply and ι 6= halt . The following theorem captures this idea formally:
Theorem 1 (Soundness) If ` S : C and ·; C; · `ι ι and (S, ι) 7−→ . . . 7−→
(S 0 , ι0 ) then (S 0 , ι0 ) is not a stuck state.
  We prove soundness syntactically in the style of Wright and Felleisen [28].
The proof appears in the companion technical report [19].

4      Non-linear Constraints
Most linear type systems contain a class of non-linear values that can be used
in a completely unrestricted fashion. Our system is similar in that it admits
non-linear constraints, written {η 7→ τ }ω . They are characterized by the axiom:
                      ∆ ` {η 7→ τ }ω = {η 7→ τ }ω ⊕ {η 7→ τ }ω
Unlike the constraints of the previous section, non-linear constraints may be
duplicated. Therefore, it is not sound to deallocate memory described by non-
linear constraints or to use it at different types. Because there are strictly fewer
operations on non-linear constraints than linear constraints, there is a natural
subtyping relation between the two: {η 7→ τ } ≤ {η 7→ τ }ω . We extend the
subtyping relationship on single constraints to collections of constraints with
rules for reflexivity, transitivity, and congruence. For example, assume add has
type ∀[ρ1 , ρ2 , ; {ρ1 7→ hinti}ω ⊕ {ρ2 7→ hinti}ω ⊕ ].(ptr(ρ1 ), ptr(ρ2 ))→0 and
consider this code:
Instructions              Constraints (Initially ∅)
malloc x, ρ, 1;           C1 = {ρ 7→ hjunki}, x : ptr(ρ)
x[0]:=3;                  C2 = {ρ 7→ hinti}
add[ρ, ρ, ∅](x, x)        C2 ≤ {ρ 7→ hinti}ω = {ρ 7→ hinti}ω ⊕ {ρ 7→ hinti}ω ⊕ ∅
      Typing rules for non-linear constraints are presented in Figure 4.
376         F. Smith, D. Walker, and G. Morrisett



∆; Γ `v v : τ

                    ∆; Γ `v i : int             ∆; Γ `v x : Γ (x)         ∆; Γ `v junk : junk

                   ∆ `wf η                          ∆; Γ `v v1 : τ1        ···        ∆; Γ `v vn : τn
            ∆; Γ `v ptr(η) : ptr(η)                     ∆; Γ `v hv1 , . . . , vn i : hτ1 , . . . , τn i


                      ∆ `wf ∀[∆0 ; C].(τ1 , . . . , τn )→0
      ∆, ∆ ; C; Γ, f :∀[∆0 ; C].(τ1 , . . . , τn )→0, x1 :τ1 , . . . , xn :τn `ι ι
             0
                                                                                         (f, x1 , . . . , xn 6∈ Γ )
 ∆; Γ `v fix f [∆0 ; C; x1 :τ1 , . . . , xn :τn ].ι : ∀[∆0 ; C].(τ1 , . . . , τn )→0


                          ∆ `wf η              ∆; Γ `v v : ∀[ρ, ∆0 ; C].(τ1 , . . . , τn )→0
                                 ∆; Γ `v v[η] : ∀[∆0 ; C].(τ1 , . . . , τn )→0[η/ρ]


 ∆ `wf C              ∆; Γ `v v : ∀[, ∆; C 0 ].(τ1 , . . . , τn )→0         ∆; Γ `v v : τ 0   ∆ ` τ0 = τ
                                      0
       ∆; Γ `v v[C] : ∀[∆; C ].(τ1 , . . . , τn )→0[C/]                             ∆; Γ `v v : τ

∆; C; Γ `ι ι

                 ∆, ρ; C ⊕ {ρ 7→ hjunk1 , . . . , junkn i}; Γ, x:ptr(ρ) `ι ι
                                                                             (x 6∈ Γ, ρ 6∈ ∆)
                             ∆; C; Γ `ι malloc x, ρ, n; ι


                                        ∆; Γ `v v : ptr(η)
                 ∆ ` C = C 0 ⊕ {η 7→ hτ1 , . . . , τn i} ∆; C 0 ⊕ {η 7→ junk}; Γ `ι ι
                                                 ∆; C; Γ `ι free v; ι


           ∆; Γ `v v : ptr(η)        ∆ ` C = C 0 ⊕ {η 7→ hτ1 , . . . , τn i}
      ∆; Γ `v v 0 : τ 0 ∆; C 0 ⊕ {η 7→ hτ1 , . . . , τi−1 , τ 0 , τi+1 , . . . , τn i}; Γ `ι ι
                                                                                                 (1 ≤ i ≤ n)
                                          ∆; C; Γ `ι v[i]:=v 0 ; ι


                           ∆; Γ `v v : ptr(η 0 )
                            0         0                                       
            ∆ ` C = C ⊕ {η 7→ hτ1 , . . . , τn i} ∆; C; Γ, x:τi `ι ι    x 6∈ Γ
                           ∆; C; Γ `ι x=v[i]; ι                        1≤i≤n


           ∆; Γ `v v : ∀[·; C 0 ].(τ1 , . . . , τn )→0    ∆ ` C = C0
               ∆; Γ `v v1 : τ1           ···        ∆; Γ `v vn : τn
                                ∆; C; Γ `ι v(v1 , . . . , vn )                       ∆; C; Γ `ι halt



                   Fig. 3. Language of Locations: Value and Instruction Typing
                                                                                Alias Types       377



                             ∆; Γ `v v : ptr(η)
                                                                                             
          ∆ ` C = C 0 ⊕ {η 7→ hτ1 , . . . , τn i}ω         ∆; C; Γ, x:τi `ι ι        x 6∈ Γ
                                ∆; C; Γ `ι x=v[i]; ι                                1≤i≤n


               ∆; Γ `v v : ptr(η)                  ∆; Γ `v v 0 : τ 0
   ∆ ` C = C ⊕ {η 7→ hτ1 , . . . , τn i}ω
                 0
                                                    ∆ ` τ 0 = τi       ∆; C; Γ `ι ι
                                                       0
                                                                                       (1 ≤ i ≤ n)
                                 ∆; C; Γ `ι v[i]:=v ; ι


      ∆; Γ `v v : ∀[·; C 0 ].(τ1 , . . . , τn )→0    ∆ ` C ≤ C0
          ∆; Γ `v v1 : τ1           ···        ∆; Γ `v vn : τn          ` S : C0   ` C0 ≤ C
                      ∆; C; Γ `ι v(v1 , . . . , vn )                            `S:C



                     Fig. 4. Language of Locations: Non-linear Constraints


4.1     Non-linear Constraints and Dynamic Type Tests
Although data structures described by non-linear constraints cannot be deal-
located or used to store objects of varying types, we can still take advantage
of the sharing implied by singleton pointer types. More specifically, code can
use weak constraints to perform a dynamic type test on a particular object and
simultaneously refine the types of many aliases of that object.
    To demonstrate this application, we extend the language discussed in the
previous section with a simple form of option type ?hτ1 , . . . , τn i (see Figure 5).
Options may be null or a memory block hτ1 , . . . , τn i. The mknull operation
associates the name ρ with null and the tosum v, τ instruction injects the value v
(a location containing null or a memory block) into a location for the option type
?hτ1 , . . . , τn i. In the typing rules for tosum and ifnull, the annotation φ may
either be ω, which indicates a non-linear constraint or ·, the empty annotation,
which indicates a linear constraint.
    The ifnull v then ι1 else ι2 construct tests an option to determine whether
it is null or not. Assuming v has type ptr(η), we check the first branch (ι1 )
with the constraint {η 7→ null }φ and the second branch with the constraint
{η 7→ hτ1 , . . . , τn i}φ where hτ1 , . . . , τn i is the appropriate non-null variant. As
before, imagine that sp is the stack pointer, which contains an integer option.

(* constraints = {η 7→ hptr(η 0 )i, η 0 7→ ?hinti}, sp:ptr(η)                                     *)
r1 =sp[1];          (* r1 :ptr(η 0 )                                                              *)
ifnull r1 then halt (* null check                                                                 *)
else · · ·          (* constraints = {η 7→ hptr(η 0 )i}⊕{η 0 7→ hinti}ω                           *)
Notice that a single null test refines the type of multiple aliases; both r1 and
its alias on the stack sp[1] can be used as integer references in the else clause.
Future loads of r1 or its alias will not have to perform a null-check.
378       F. Smith, D. Walker, and G. Morrisett

   These additional features of our language are also proven sound in the com-
panion technical report [19].


Syntax:

             types            τ ::= . . . | ?hτ1 , . . . , τn i | null
             values           v ::= . . . | null
             instructions     ι ::= . . . | mknull x, ρ; ι | tosum v, ?hτ1 , . . . , τn i |
                                    ifnull v then ι1 else ι2

Operational semantics:

        (S, mknull x, ρ; ι)                  7−→ (S{` 7→ null}, ι[`/ρ][ptr(`)/x])
             where ` 6∈ S
        (S, tosum v, ?hτ1 , . . . , τn i; ι)  7−→ (S, ι)
        (S{` 7→ null},
             ifnull ptr(`) then ι1 else ι2 ) 7−→ (S{` 7→ null}, ι1 )
        (S{` 7→ hv1 , . . . , vn i},
             ifnull ptr(`) then ι1 else ι2 ) 7−→ (S{` 7→ hv1 , . . . , vn i}, ι2 )

Static Semantics:
                                 ∆, ρ; C ⊕ {ρ 7→ null }; Γ, x:ptr(ρ) `ι ι
                                                                          (x 6∈ Γ, ρ 6∈ ∆)
      ∆; Γ `v null : null               ∆; C; Γ `ι mknull x, ρ; ι


                   ∆; Γ `v v : ptr(η)       ∆ ` C = C 0 ⊕ {η 7→ null }φ
               ∆ `wf ?hτ1 , . . . , τn i ∆; C 0 ⊕ {η 7→ ?hτ1 , . . . , τn i}φ ; Γ `ι ι
                              ∆; C; Γ `ι tosum v, ?hτ1 , . . . , τn i; ι


                                        ∆; Γ `v v : ptr(η)
      ∆ ` C = C 0 ⊕ {η 7→ hτ1 , . . . , τn i}φ    ∆; C 0 ⊕ {η 7→ ?hτ1 , . . . , τn i}φ ; Γ `ι ι
                              ∆; C; Γ `ι tosum v, ?hτ1 , . . . , τn i; ι


               ∆; Γ `v v : ptr(η)     ∆ ` C = C 0 ⊕ {η 7→ ?hτ1 , . . . , τn i}φ
               0             φ
          ∆; C ⊕ {η 7→ null } ; Γ `ι ι1   ∆; C 0 ⊕ {η 7→ hτ1 , . . . , τn i}φ ; Γ `ι ι2
                             ∆; C; Γ `ι ifnull v then ι1 else ι2


               Fig. 5. Language of Locations: Extensions for option types




5     Related and Future Work
Our research extends previous work on linear type systems [26] and syntactic
control of interference [16] by allowing both aliasing and safe deallocation. Se-
veral authors [26, 3, 9] have explored alternatives to pure linear type systems
                                                              Alias Types      379

to allow greater flexibility. Wadler [26], for example, introduced a new let-form
let ! (x) y = e1 in e2 that permits the variable x to be used as a non-linear
value in e1 (i .e. it can be used many times, albeit in a restricted fashion) and
then later used as a linear value in e2 . We believe we can encode similar behavior
by extending our simple subtyping with bounded quantification. For instance,
if a function f requires some collection of aliasing constraints  that are boun-
ded above by {ρ1 7→ hinti}ω ⊕ {ρ2 7→ hinti}ω , then f may be called with a
single linear constraint {ρ 7→ hinti} (instantiating both ρ1 and ρ2 with ρ and
 with {ρ 7→ hinti}). The constraints may now be used non-linearly within the
body of f . Provided f expects a continuation with constraints , its continuation
will retain the knowledge that {ρ 7→ hinti} is linear and will be able to deallo-
cate the storage associated with ρ when it is called. However, we have not yet
implemented this feature.
    Because our type system is constructed from standard type-theoretic building
blocks, including linear and singleton types, it is relatively straightforward to
implement these ideas in a modern type-directed compiler. In some ways, our new
mechanisms simplify previous work. Previous versions of TAL [12, 11] possessed
two separate mechanisms for initializing data structures. Uninitialized heap-
allocated data structures were stamped with the type at which they would be
used. On the other hand, stack slots could be overwritten with values of arbitrary
types. Our new system allows us to treat memory more uniformly. In fact, our
new language can encode stack types similar to those described by Morrisett
et al. [11] except that activation records are allocated on the heap rather than
using a conventional call stack. The companion technical report [19] shows how
to compile a simple imperative language in such a way that it allocates and
deletes its own stack frames.
    This research is also related to other work on type systems for low-level
languages. Work on Java bytecode verification [20, 8] also develops type systems
that allows locations to hold values of different types. However, the Java bytecode
type system is not strong enough to represent aliasing as we do here.
    The development of our language was inspired by the Calculus of Capa-
bilities (CC) [4]. CC provides an alternative to the region-based type system
developed by Tofte and Talpin [24]. Because safe region deallocation requires
that no aliases be used in the future, CC tracks region aliases. In our new lan-
guage we adapt CC’s techniques to track both object aliases and object type
information.
    Our work also has close connections with research on alias analyses [5, 21,
17]. Much of that work aims to facilitate program optimizations that require
aliasing information in order to be correct. However, these optimizations do not
necessarily make it harder to check the safety of the resulting program. Other
work [7, 6] attempts to determine when programs written in unsafe languages,
such as C, perform potentially unsafe operations. Our goals are closer to the
latter application but differ because we are most interested in compiling safe
languages and producing low-level code that can be proven safe in a single pass
over the program. Moreover, our main result is not a new analysis technique,
380    F. Smith, D. Walker, and G. Morrisett

but rather a sound system for representing and checking the results of analysis,
and, in particular, for representing aliasing in low-level compiler-introduced data
structures rather than for representing aliasing in source-level data.
    The language of locations is a flexible framework for reasoning about sharing
and destructive operations in a type-safe manner. However, our work to date is
only a first step in this area and we are investigating a number of extensions. In
particular, we are working on integrating recursive types into the type system as
they would allow us to capture regular repeating structure in the store. When
we have completed this task, we believe our aliasing constraints will provide us
with a safe, but rich and reusable, set of memory abstractions.

Acknowledgements
This work arose in the context of implementing the Typed Assembly Language
compiler. We are grateful for the many stimulating discussions that we have
had on this topic with Karl Crary, Neal Glew, Dan Grossman, Dexter Kozen,
Stephanie Weirich, and Steve Zdancewic. Sophia Drossopoulou, Kathleen Fisher,
Andrew Myers, and Anne Rogers gave helpful comments on a previous draft of
this work.


References
 [1] Alfred V. Aho, Ravi Sethi, and Jeffrey D. Ullman. Compilers: Principles, Tech-
     niques, and Tools. Addison-Wesley, 1986.
 [2] Andrew W. Appel and David B. MacQueen. Standard ML of New Jersey. In
     Martin Wirsing, editor, Third International Symposium on Programming Langu-
     age Implementation and Logic Programming, pages 1–13, New York, August 1991.
     Springer-Verlag. Volume 528 of Lecture Notes in Computer Science.
 [3] Erik Barendsen and Sjaak Smetsers. Conventional and uniqueness typing in graph
     rewrite systems (extended abstract). In Thirteenth Conference on the Foundations
     of Software Technology and Theoretical Computer Science, pages 41–51, Bombay,
     1993. In Shyamasundar, ed., Springer-Verlag, LNCS 761.
 [4] Karl Crary, David Walker, and Greg Morrisett. Typed memory management in
     a calculus of capabilities. In Twenty-Sixth ACM Symposium on Principles of
     Programming Languages, pages 262–275, San Antonio, January 1999.
 [5] Alain Deutsch. Interprocedural may-alias analysis for pointers: Beyond k-limiting.
     In ACM Conference on Programming Language Design and Implementation, pages
     230–241, Orlando, June 1994.
 [6] Nurit Dor, Michael Rodeh, and Mooly Sagiv. Detecting memory errors via sta-
     tic pointer analysis (preliminary experience). In ACM Workshop on Program
     Analysis for Software Tools and Engineering (PASTE’98), Montreal, June 1998.
 [7] David Evans. Static detection of dynamic memory errors. In ACM Conference
     on Programming Language Design and Implementation, Philadelphia, May 1996.
 [8] Stephen N. Freund and John C. Mitchell. A formal framework for the Java
     bytecode language and verifier. In Conference on Object-Oriented Programming,
     Systems, Languages, and Applications, pages 147–166, Denver, November 1999.
 [9] Naoki Kobayashi. Quasi-linear types. In Twenty-Sixth ACM Symposium on Prin-
     ciples of Programming Languages, pages 29–42, San Antonio, January 1999.
                                                                Alias Types      381

[10] Tim Lindholm and Frank Yellin. The Java Virtual Machine Specification.
     Addison-Wesley, 1996.
[11] Greg Morrisett, Karl Crary, Neal Glew, and David Walker. Stack-based Typed
     Assembly Language. In Second International Workshop on Types in Compilation,
     pages 95–117, Kyoto, March 1998. Published in Xavier Leroy and Atsushi Ohori,
     editors, Lecture Notes in Computer Science, volume 1473, pages 28-52. Springer-
     Verlag, 1998.
[12] Greg Morrisett, David Walker, Karl Crary, and Neal Glew. From System F to
     Typed Assembly Language. ACM Transactions on Programming Languages and
     Systems, 3(21):528–569, May 1999.
[13] George Necula. Proof-carrying code. In Twenty-Fourth ACM Symposium on
     Principles of Programming Languages, pages 106–119, Paris, 1997.
[14] G. D. Plotkin. Call-by-name, call-by-value, and the lambda calculus. Theoretical
     Computer Science, 1:125–159, 1975.
[15] John C. Reynolds. Definitional interpreters for higher-order programming langu-
     ages. In Conference Record of the 25th National ACM Conference, pages 717–740,
     Boston, August 1972.
[16] John C. Reynolds. Syntactic control of interference. In Fifth ACM Symposium
     on Principles of Programming Languages, pages 39–46, Tucson, 1978.
[17] M. Sagiv, T. Reps, and R. Wilhelm. Solving shape-analysis problems in languages
     with destructive updating. ACM Transactions on Programming Languages and
     Systems, 20(1):1–50, January 1996.
[18] Z. Shao. An overview of the FLINT/ML compiler. In Workshop on Types in Com-
     pilation, Amsterdam, June 1997. ACM. Published as Boston College Computer
     Science Dept. Technical Report BCCS-97-03.
[19] Frederick Smith, David Walker, and Greg Morrisett. Alias types. Technical Report
     TR99-1773, Cornell University, October 1999.
[20] Raymie Stata and Martı́n Abadi. A type system for Java bytecode subroutines.
     In Twenty-Fifth ACM Symposium on Principles of Programming Languages, San
     Diego, January 1998.
[21] B. Steensgaard. Points-to analysis in linear time. In Twenty-Third ACM Sympo-
     sium on Principles of Programming Languages, January 1996.
[22] D. Tarditi, G. Morrisett, P. Cheng, C. Stone, R. Harper, and P. Lee. TIL: A
     type-directed optimizing compiler for ML. In ACM Conference on Programming
     Language Design and Implementation, pages 181–192, Philadelphia, May 1996.
[23] Mads Tofte. Type inference for polymorphic references. Information and Com-
     putation, 89:1–34, November 1990.
[24] Mads Tofte and Jean-Pierre Talpin. Region-based memory management. Infor-
     mation and Computation, 132(2):109–176, 1997.
[25] David N. Turner, Philip Wadler, and Christian Mossin. Once upon a type. In ACM
     International Conference on Functional Programming and Computer Architecture,
     San Diego, CA, June 1995.
[26] Philip Wadler. Linear types can change the world! In M. Broy and C. Jones,
     editors, Programming Concepts and Methods, Sea of Galilee, Israel, April 1990.
     North Holland. IFIP TC 2 Working Conference.
[27] A. K. Wright. Simple imperative polymorphism. LISP and Symbolic Computation,
     8(4), December 1995.
[28] Andrew K. Wright and Matthias Felleisen. A syntactic approach to type so-
     undness. Information and Computation, 115(1):38–94, 1994.
