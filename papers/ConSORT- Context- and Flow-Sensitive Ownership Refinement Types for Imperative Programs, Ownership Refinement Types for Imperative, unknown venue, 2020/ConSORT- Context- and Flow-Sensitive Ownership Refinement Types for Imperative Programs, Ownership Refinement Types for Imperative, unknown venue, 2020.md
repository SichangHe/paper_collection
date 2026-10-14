                                             ConSORT: Context- and Flow-Sensitive
                                            Ownership Refinement Types for Imperative
                                                            Programs

                                                          John Toman1 , Ren Siqi1 , Kohei Suenaga1 ,
                                                          Atsushi Igarashi1 , and Naoki Kobayashi2
                                                                 1
                                                                   Kyoto University, Kyoto, Japan,
                                                  {jtoman,shiki,ksuenaga,igarashi}@fos.kuis.kyoto-u.ac.jp
                                                2
                                                  The University of Tokyo, Tokyo, Japan, koba@is.s.u-tokyo.ac.jp



                                              Abstract. We present ConSORT, a type system for safety verification
arXiv:2002.07770v2 [cs.PL] 8 Aug 2026




                                              in the presence of mutability and aliasing. Mutability requires strong
                                              updates to model changing invariants during program execution, but
                                              aliasing between pointers makes it difficult to determine which invariants
                                              must be updated in response to mutation. Our type system addresses
                                              this difficulty with a novel combination of refinement types and fractional
                                              ownership types. Fractional ownership types provide flow-sensitive and
                                              precise aliasing information for reference variables. ConSORT interprets
                                              this ownership information to soundly handle strong updates of potentially
                                              aliased references. We have proved ConSORT sound and implemented a
                                              prototype, fully automated inference tool. We evaluated our tool and found
                                              it verifies non-trivial programs including data structure implementations.

                                               Keywords: refinement types, mutable references, aliasing, strong up-
                                               dates, fractional ownerships, program verification, type systems


                                        1    Introduction
                                        Driven by the increasing power of automated theorem provers and recent high-
                                        profile software failures, fully automated program verification has seen a surge
                                        of interest in recent years [5, 10, 15, 29, 38, 65]. In particular, refinement types
                                        [9, 21, 24, 64], which refine base types with logical predicates, have been shown to
                                        be a practical approach for program verification that are amenable to (sometimes
                                        full) automation [47, 60, 61, 62]. Despite promising advances [26, 32, 46], the sound
                                        and precise application of refinement types (and program verification in general)
                                        in settings with mutability and aliasing (e.g., Java, Ruby, etc.) remains difficult.
                                            One of the major challenges is how to precisely and soundly support strong
                                        updates for the invariants on memory cells. In a setting with mutability, a single
                                        invariant may not necessarily hold throughout the lifetime of a memory cell; while
                                        the program mutates the memory the invariant may change or evolve. To model
                                        these changes, a program verifier must support different, incompatible invariants
                                        which hold at different points during program execution. Further, precise program
                                        verification requires supporting different invariants on distinct pieces of memory.
    2       J. Toman et al.


1   mk(n) { mkref n }                            1  loop(a, b) {
                                                 2    let aold = *a in
3 let p = mk(3) in                                3   b := *b + 1;
4 let q = mk(5) in                                4   a := *a + 1;
5 p := *p + 1;                                    5   assert(*a = aold + 1);
6 q := *q + 1;                                    6   if ⋆ then
7 assert(*p = 4);                                 7     loop(b, mkref ⋆)
                                                  8   else
                                                  9     loop(b,a)
    Fig. 1. Example demonstrating the dif-
                                                 10 }
    ficulty of effecting strong updates in the
                                                 11 loop(mkref ⋆, mkref ⋆)
    presence of aliasing. The function mk is
    bound in the program from sections 1
    to 1; its body is given within the braces.       Fig. 2. Example with non-trivial alias-
                                                     ing behavior.



        One solution is to use refinement types on the static program names (i.e.,
    variables) which point to a memory location. This approach can model evolving
    invariants while tracking distinct invariants for each memory cell. For example,
    consider the (contrived) example in Figure 1. This program is written in an ML-
    like language with mutable references; references are updated with := and allo-
    cated with mkref. Variable p can initially be given the type {ν : int | ν = 3} ref ,
    indicating it is a reference to the integer 3. Similarly, q can be given the type
    {ν : int | ν = 5} ref . We can model the mutation of p’s memory on section 1 by
    strongly updating p’s type to {ν : int | ν = 4} ref .
        Unfortunately, the precise application of this technique is confounded by the
    existence of unrestricted aliasing. In general, updating just the type of the mutated
    reference is insufficient: due to aliasing, other variables may point to the mutated
    memory and their refinements must be updated as well. However, in the presence
    of conditional, may aliasing, it is impossible to strongly update the refinements
    on all possible aliases; given the static uncertainty about whether a variable
    points to the mutated memory, that variable’s refinement may only be weakly
    updated. For example, suppose we used a simple alias analysis that imprecisely
    (but soundly) concluded all references allocated at the same program point might
    alias. Variables p and q share the allocation site on section 1, so on section 1 we
    would have to weakly update q’s type to {ν : int | ν = 4 ∨ ν = 5}, indicating it
    may hold either 4 or 5. Under this same imprecise aliasing assumption, we would
    also have to weakly update p’s type on section 1, preventing the verification of
    the example program.
        Given the precision loss associated with weak updates, it is critical that
    verification techniques built upon refinement types use precise aliasing information
    and avoid spuriously applied weak updates. Although it is relatively simple to
    conclude that p and q do not alias in Figure 1, consider the example in Figure 2.
    (In this example, ⋆ represents non-deterministic values.) Verifying this program
    requires proving a and b never alias at the writes on section 1. In fact, a and b may
    point to the same memory location, but only in different invocations of loop; this
       ConSORT: Context- and Flow-Sensitive Ownership Refinement Types              3

pattern may confound even sophisticated symbolic alias analyses. Additionally, a
and b share an allocation site on section 1, so an approach based on the simple
alias analysis described above will also fail on this example. This must-not alias
proof obligation can be discharged with existing techniques [53, 54], but requires
an expensive, on-demand, interprocedural, flow-sensitive alias analysis.
     This paper presents ConSORT (CONtext Sensitive Ownership Refinement
Types), a type system for the automated verification of program safety in imper-
ative languages with mutability and aliasing. ConSORT is built upon the novel
combination of refinement types and fractional ownership types [55, 56]. Frac-
tional ownership types extend pointer types with a rational number in the range
[0, 1] called an ownership. These ownerships encapsulate the permission of the
reference; only references with ownership 1 may be used for mutation. Fractional
ownership types also obey the following key invariant: any references with a mu-
table alias must have ownership 0. Thus, any reference with non-zero ownership
cannot be an alias of a reference with ownership 1. In other words, ownerships
encode precise aliasing information in the form of must-not aliasing relationships.
     To understand the benefit of this approach, let us return to Figure 1. As mk
returns a freshly allocated reference with no aliases, its type indicates it returns a
reference with ownership 1. Thus, our type system can initially give p and q types
{ν : int | ν = 3} ref 1 and {ν : int | ν = 5} ref 1 respectively. The ownership 1 on
the reference type constructor ref indicates both pointers hold “exclusive” own-
ership of the pointed to reference cell; from the invariant of fractional ownership
types p and q must not alias. The types of both references can be strongly updated
without requiring spurious weak updates. As a result, at the assertion statement
on section 1, p has type {ν : int | ν = 4} ref 1 expressing the required invariant.
     Our type system can also verify the example in Figure 2 without expensive
side analyses. As a and b are both mutated, they must both have ownership 1; i.e.,
they cannot alias. This pre-condition is satisfied by all invocations of loop; on
section 1, b has ownership 1 (from the argument type), and the newly allocated
reference must also have ownership 1. Similarly, both arguments on section 1
have ownership 1 (from the assumed ownership on the argument types).
     Ownerships behave linearly; they cannot be duplicated, only split when aliases
are created. This linear behavior preserves the critical ownership invariant. For
example, if we replace section 1 in Figure 2 with loop(b,b), the program becomes
ill-typed; there is no way to divide b’s ownership of 1 to into two ownerships of 1.
     Ownerships also obviate updating refinement information of aliases at muta-
tion. ConSORT ensures that only the trivial refinement ⊤ is used in reference
types with ownership 0, i.e., mutably-aliased references. When memory is mu-
tated through a reference with ownership 1, ConSORT simply updates the refine-
ment of the mutated reference variable. From the soundness of ownership types,
all aliases have ownership 0 and must therefore only contain the ⊤ refinement.
Thus, the types of all aliases already soundly describe all possible contents.3

3
    This assumption holds only if updates do not change simple types, a condition our
    type-system enforces.
 4         J. Toman et al.

      ConSORT is also context-sensitive, and can use different summaries of func-
  tion behavior at different points in the program. For example, consider the variant
                             of Figure 1 shown in Figure 3. The function get returns
                             the contents of its argument, and is called on section 1.
                             To precisely verify this program, on section 1 get must
1 get(p) { *p }
                             be typed as a function that takes a reference to 3 and
                             returns 3. Similarly, on section 1 get must be typed
3 let p = mkref 3 in
                             as a function that takes a reference to 5 and returns
4 let q = mkref 5 in
                             5. Our type system can give get a function type that
5 p := get(p) + 1;
                             distinguishes between these two calling contexts and
6 q := get(q) + 1;
                             selects the appropriate summary of get’s behavior.
7 assert(*p = 4);
                                 We have formalized ConSORT as a type system
8 assert(*q = 6);
                             for a small imperative calculus and proved the system
                             is sound: i.e., a well-typed program never encounters as-
  Fig. 3.    Example     of sertion failures during execution. We have implemented
  context-sensitivity        a prototype type inference tool targeting this imper-
                             ative language and found it can automatically verify
                             several non-trivial programs, including sorted lists and
  an array list data structure.
      The rest of this paper is organized as follows. Section 2 defines the imperative
  language targeted by ConSORT and its semantics. Section 3 defines our type
  system and states our soundness theorem. Section 4 sketches our implementa-
  tion’s inference algorithm and its current limitations. Section 5 describes an eval-
  uation of our prototype, Section 6 outlines related work, and Section 7 concludes.


 2      Target Language
 This section describes a simple imperative language with mutable references and
 first-order, recursive functions.

 2.1     Syntax
 We assume a set of variables, ranged over by x, y, z, . . . , a set of function names,
 ranged over by f , and a set of labels, ranged over by ℓ1 , ℓ2 , . . . . The grammar of
 the language is as follows.

       d ::= f 7→ (x1 , ... , xn )e
       e ::= x | let x = y in e | let x = n in e | ifz x then e1 else e2
           | let x = mkref y in e | let x = ∗y in e | let x = f ℓ (y1 , . . . , yn ) in e
           | x : = y ; e | alias(x = y) ; e | alias(x = ∗y) ; e | assert(φ) ; e | e1 ; e2
       P ::= ⟨{d1 , ... , dn }, e⟩

 φ stands for a formula in propositional first-order logic over variables, integers
 and contexts; we discuss these formulas later in Section 3.1.
     Variables are introduced by function parameters or let bindings. Like ML, the
 variable bindings introduced by let expressions and parameters are immutable.
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                 5

Mutable variable declarations such as int x = 1; in C are achieved in our lan-
guage with:
                     let y = 1 in(let x = mkref y in . . .) .
As a convenience, we assume all variable names introduced with let bindings and
function parameters are distinct.
     Unlike ML (and like C or Java) we do not allow general expressions on the
right hand side of let bindings. The simplest right hand forms are a variable y or
an integer literal n. mkref y creates a reference cell with value y, and ∗y accesses
the contents of reference y. For simplicity, we do not include an explicit null value;
an extension to support null is discussed in Section 4. Function calls must occur
on the right hand side of a variable binding and take the form f ℓ (x1 , . . . , xn ),
where x1 , . . . , xn are distinct variables and ℓ is a (unique) label. These labels are
used to make our type system context-sensitive as discussed in Section 3.3.
     The single base case for expressions is a single variable. If the variable
expression is executed in a tail position of a function, then the value of that
variable is the return value of the function, otherwise the value is ignored.
     The only intraprocedural control-flow operations in our language are if state-
ments. ifz checks whether the condition variable x equals zero and chooses the
corresponding branch. Loops can be implemented with recursive functions and
we do not include them explicitly in our formalism.
     Our grammar requires that side-effecting, result-free statements, assert(φ)
alias(x = y), alias(x = ∗y) and assignment x := y are followed by a continu-
ation expression. We impose this requirement for technical reasons to ease our
formal presentation; this requirement does not reduce expressiveness as dummy
continuations can be inserted as needed. The assert(φ) ; e form executes e if
the predicate φ holds in the current state and aborts the program otherwise.
alias(x = y) ; e and alias(x = ∗y) ; e assert a must-aliasing relationship between
x and y (resp. x and ∗y) and then execute e. alias statements are effectively an-
notations that our type system exploits to gain added precision. x : = y ; e updates
the contents of the memory cell pointed to by x with the value of y. In addition
to the above continuations, our language supports general sequencing with e1 ; e2 .
     A program is a pair ⟨D, e⟩, where D = {d1 , ... , dn } is a set of first-order,
mutually recursive function definitions, and e is the program entry point. A
function definition d maps the function name to a tuple of argument names
x1 , ... , xn that are bound within the function body e.

Paper Syntax. In the remainder of the paper, we will write programs that are
technically illegal according to our grammar, but can be easily “de-sugared” into
an equivalent, valid program. For example, we will write
  let x = mkref 4 in assert(*x = 4)
as syntactic sugar for:
  let f = 4 in let x = mkref f in
  let tmp = *x in assert(tmp = 4); let dummy = 0 in dummy
6            J. Toman et al.

       D                     E         D                     E   D                              E         D                   E
                      ⃗, x
           H , R, F : F          −→D              ⃗ , F [x ]
                                           H , R, F                             ⃗ , E [x ; e]
                                                                     H , R, F : F                   −→D              ⃗ , E [e]
                                                                                                              H , R, F
                                                   (R-Var)                                                            (R-Seq)

                           x ′ ̸∈ dom(R)                                                   x ′ ̸∈ dom(R)
       D                                 E                              D                                E
                  ⃗
           H , R, F , E [let x = y in e]                                           ⃗
                                                                            H , R, F , E [let x = n in e]
                   D                                          E                     D                                     E
           −→D H , R{x ′ 7→ R(y)}, F       ⃗ , E [[x ′ /x ]e]               −→D H , R{x ′ 7→ n}, F     ⃗ , E [[x ′ /x ]e]
                                                     (R-Let)                                                (R-LetInt)

                                  R(x ) = 0                                         R(x ) ̸= 0
                 D                                         E          D                                      E
                            ⃗ , E [ifz x then e1 else e2 ]
                     H , R, F                                                 ⃗ , E [ifz x then e1 else e2 ]
                                                                       H , R, F
                             D                    E                            D                    E
                     −→D H , R, F      ⃗ , E [e1 ]                      −→D H , R, F     ⃗ , E [e2 ]
                                                   (R-IfTrue)                                       (R-IfFalse)

              a ̸∈ dom(H )       x ′ ̸∈ dom(R)                         R(y) = a       H (a) = v         x ′ ̸∈ dom(R)
         D                                        E                       D                                E
          H , R, F⃗ , E [let x = mkref y in e] −→D                                ⃗ , E [let x = ∗y in e] −→D
                                                                           H , R, F
      D                                                    E                 D                                      E
        H {a 7→ R(y)}, R{x ′ 7→ a}, F   ⃗ , E [[x ′ /x ]e]                     H , R{x ′ 7→ v }, F
                                                                                                 ⃗ , E [[x ′ /x ]e]
                                             (R-MkRef)                                                       (R-Deref)




                                              Fig. 4. Transition Rules (1).


2.2      Operational Semantics
We now introduce the operational semantics for our language. We assume a
countably infinite domain of heap addresses Addr: we denote Dan arbitrary           E
address with a. A runtime state is represented by a configuration H , R, F⃗ , e ,
which consists of a heap, register file, stack, and currently reducing expression
respectively. The register file maps variables to runtime values v, which are either
integers n or addresses a. The heap maps a finite subset of addresses to runtime
values. The runtime stack represents pending function calls as a sequence of return
contexts, which we describe below. While the final configuration component is an
expression, the rewriting rules are defined in terms of E [e], which is an evaluation
context E and redex e, as is standard. The grammar for evaluation contexts is
defined by: E ::= E ′ ; e | [].
    Our operational semantics is given in Figures 4 and 5. We write dom(H ) to
indicate the domain of a function and H {a 7→ v} where a ̸∈ dom(H ) to denote a
map which takes all values in dom(H) to their values in H and which additionally
takes a to v. We will write H {a ←- v} where a ∈ dom(H ) to denote a map
equivalent to H except that a takes value v. We use similar notation for dom(R)
and R{x 7→ v}. We also write ∅ for the empty register file and heap. The step
relation −→D is parameterized by a set of function definitions D; a program ⟨D, e⟩
is executed by stepping the initial configuration ⟨∅, ∅, ·, e⟩ according to −→D .
The semantics is mostly standard; we highlight some important points below.
    Return contexts F take the form E [let y = []ℓ in e]. A return context repre-
sents a pending function call with label ℓ, and indicates that y should be bound to
the return value of the callee during the execution of e within the larger execution
context E . The call stack F⃗ is a sequence of these contexts, with the first such re-
             ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                                                        7

                              f 7→ (x1 , .. , xn )e ∈ D                                      R(x ) = a          a ∈ dom(H )
      D                                                         E                           D                           E
                 ⃗ , E [let x = f ℓ (y1 , . . . , yn ) in e ′ ]
          H , R, F                                                                                   ⃗ , E [x : = y ; e] −→D
                                                                                              H , R, F
                  D                                                                    E     D                                  E
          −→D H , R, E [let x = []ℓ in e ′ ] : F        ⃗ , [y1 /x1 ] · · · [yn /xn ]e         H {a ←- R(y)}, R, F     ⃗ , E [e]
                                                                              (R-Call)                              (R-Assign)

                       R(x ) = R(y)
           D                                   E                        R(y) = a       H (a) = R(x )
                      ⃗ , E [alias(x = y) ; e]
               H , R, F                                  D                                E     D               E
                       D                 E                       ⃗ , E [alias(x = ∗y) ; e] −→D H , R, F
                                                          H , R, F                                     ⃗ , E [e]
               −→D H , R, F     ⃗ , E [e]
                                                                                                   (R-AliasPtr)
                                       (R-Alias)

                           R(x ) ̸= R(y)                                                   R(x ) ̸= H (R(y))
 D                                     E                               D                                 E
            ⃗ , E [alias(x = y) ; e]
     H , R, F                                −→D AliasFail                        ⃗ , E [alias(x = ∗y) ; e]
                                                                           H , R, F                        −→D AliasFail
                                              (R-AliasFail)                                               (R-AliasPtrFail)

                                 |= [R] φ
                   D                               E                                  ̸|= [R] φ
                              ⃗ , E [assert(φ) ; e]
                       H , R, F                             D                                  E
                               D                 E                     ⃗ , E [assert(φ) ; e]
                                                                H , R, F                           −→D AssertFail
                       −→D H , R, F     ⃗ , E [e]
                                                                                                     (R-AssertFail)
                                         (R-Assert)




                                               Fig. 5. Transition Rules (2).



turn context representing the most recent function call. The stack grows at func-
tion calls as described by rule R-Call. For a call E [let x = f ℓ (y1 , . . . , yn ) in e]
where f is defined as (x1 , ... , xn )e ′ , the return context E [let y = []ℓ in e] is
prepended onto the stack of the input configuration. The substitution of formal
arguments for parameters in e′ , denoted by [y1 /x1 ] · · · [yn /xn ]e ′ , becomes the
currently reducing expression in the output configuration. Function returns are
handled by R-Var. Our semantics return values by name; when the currently
executing function fully reduces to a single variable x, x is substituted into the
return context on the top of the stack, denoted by E [let y = []ℓ in e][x].
    In the rules R-Assert we write |= [R] φ to mean that the formula yielded
by substituting the concrete values in R for the variables in φ is valid within
some chosen logic (see Section 3.1); in R-AssertFail we write ̸|= [R] φ when
the formula is not valid. The substitution operation [R] φ is defined inductively
as [∅] φ = φ, [R{x 7→ n}] φ = [R] [n/x ]φ, [R{x 7→ a}] φ = [R] φ. In the case of an
assertion failure, the semantics steps to a distinguished configuration AssertFail.
The goal of our type system is to show that no execution of a well-typed program
may reach this configuration. The alias form checks whether the two references
actually alias; i.e., if the must-alias assertion provided by the programmer is
correct. If not, our semantics steps to the distinguished AliasFail configuration.
We assume that the operands x and y are distinct variables. Our type system does
not guarantee that AliasFail is unreachable; aliasing assertions are effectively
trusted annotations that are assumed to hold.
    In order to avoid duplicate variable names in our register file due to recursive
functions, we refresh the bound variable x in a let expression to x ′ . Take expression
let x = y in e as an example; we substitute a fresh variable x ′ for x in e, then bind
8         J. Toman et al.


       Types τ ::= {ν : int | φ} | τ ref
                                           r   Function Typesσ ::= ∀λ. ⟨x1 : τ1 , . . . , xn : τn ⟩
    Ownership r ∈ [0, 1]                                           → ⟨x1 : τ1′ , . . . , xn : τn′ | τ ⟩
Refinements φ ::= φ1 ∨ φ2 | ¬φ | ⊤         Context Variables λ ∈ CVar
                 | ϕ(bv1 , .. , vbn )      Concrete Context  ⃗
                                                             ℓ ::= ℓ : ⃗
                                                                       ℓ|ϵ
                 | vb1 = vb2                  Pred. Context C ::= ℓ : C | λ | ϵ
                 | CP                        Context Query CP ::= ⃗ℓ⪯C
             b ::= x | n | ν
 Ref. Values v                              Typing Context L ::= λ | ⃗ ℓ

                    Fig. 6. Syntax of types, refinements, and contexts.


x ′ to the value of variable y. We assume this refreshing of variables preserves our
assumption that all variable bindings introduced with let and function parameters
are unique, i.e. x ′ does not overlap with variable names that occur in the program.


3      Typing

We now introduce a fractional ownership refinement type system that guarantees
well-typed programs do not encounter assertion failures.


3.1     Types and Contexts

The syntax of types is given in Figure 6. Our type system has two type con-
structors: references and integers. τ ref r is the type of a (non-null) reference to a
value of type τ . r is an ownership which is a rational number in the range [0, 1].
An ownership of 0 indicates a reference that cannot be written, and for which
there may exist a mutable alias. By contrast, 1 indicates a pointer with exclusive
ownership that can be read and written. Reference types with ownership values
between these two extremes indicate a pointer that is readable but not writable,
and for which no mutable aliases exist. ConSORT ensures that these invariants
hold while aliases are created and destroyed during execution.
    Integers are refined with a predicate φ. The language of predicates is built using
the standard logical connectives of first-order logic, with (in)equality between
variables and integers, and atomic predicate symbols ϕ as the basic atoms. We
include a special “value” variable ν representing the value being refined by the
predicate. For simplicity, we omit the connectives φ1 ∧ φ2 and φ1 =⇒ φ2 ; they
can be written as derived forms using the given connectives. We do not fix a
particular theory from which ϕ are drawn, provided a sound (but not necessarily
complete) decision procedure exists. CP are context predicates, which are used
for context sensitivity as explained below.

Example 1. {ν : int | ν > 0} is the type of strictly positive integers. The type
of immutable references to integers exactly equal to 3 can be expressed by
{ν : int | ν = 3} ref 0.5 .
        ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                                9

    As is standard, we denote a type environment with Γ , which is a finite map
from variable names to type τ . We write Γ [x : τ ] to denote a type environment
Γ such that Γ (x ) = τ where x ∈ dom(Γ ), Γ, x : τ to indicate the extension of
Γ with the type binding x : τ , and Γ [x ←- τ ] to indicate the type environment
Γ with the binding of x updated to τ . We write the empty environment as
•. The treatment of type environments as mappings instead of sequences in a
dependent type system is somewhat non-standard. The standard formulation
based on ordered sequences of bindings and its corresponding well-formedness
condition did not easily admit variables with mutually dependent refinements
as introduced by our function types (see below). We therefore use an unordered
environment and relax well-formedness to ignore variable binding order.

Function Types, Contexts, and Context Polymorphism. Our type system achieves
context sensitivity by allowing function types to depend on where a function is
called, i.e., the execution context of the function invocation. Our system represents
a concrete execution contexts with strings of call site labels (or just “call strings”),
defined by ⃗ℓ ::= ϵ | ℓ : ⃗ℓ. As is standard (e.g., [49, 50]), the string ℓ : ⃗ℓ abstracts an
execution context where the most recent, active function call occurred at call site
ℓ which itself was executed in a context abstracted by ⃗ℓ; ϵ is the context under
which program execution begins. Context variables, drawn from a finite domain
CVar and ranged over by λ1 , λ2 , . . ., represent arbitrary, unknown contexts.
     A function type takes the form ∀λ. ⟨x1 : τ1 , . . . , xn : τn ⟩ → ⟨x1 : τ1′ , . . . , xn : τn′ | τ ⟩.
The arguments of a function are an n-ary tuple of types τi . To model side-effects on
arguments, the function type includes the same number of output types τi′ . In ad-
dition, function types have a direct return type τ . The argument and output types
are given names: refinements within the function type may refer to these names.
Function types in our language are context polymorphic, expressed by universal
quantification “∀λ.” over a context variable. Intuitively, this context variable repre-
sents the many different execution contexts under which a function may be called.
     Argument and return types may depend on this context variable by including
context query predicates in their refinements. A context query predicate CP
usually takes the form ⃗ℓ ⪯ λ, and is true iff ⃗ℓ is a prefix of the concrete context
represented by λ. Intuitively, a refinement ⃗ℓ ⪯ λ =⇒ φ states that φ holds in any
concrete execution context with prefix ⃗ℓ, and provides no information in any other
context. In full generality, a context query predicate may be of the form ⃗ℓ1 ⪯ ⃗ℓ2
or ⃗ℓ ⪯ ℓ1 . . . ℓn : λ; these forms may be immediately simplified to ⊤, ⊥ or ⃗ℓ′ ⪯ λ.

Example 2. The type {ν : int | (ℓ1 ⪯ λ =⇒ ν = 3) ∧ (ℓ2 ⪯ λ =⇒ ν = 5)} rep-
resents an integer that is 3 if the most recent active function call site is ℓ1 , 5 if
the most recent call site is ℓ2 , and is otherwise unconstrained. This type may be
used for the argument of f in, e.g., fℓ1 (3) + fℓ2 (5).

    As types in our type system may contain context variables, our typing
judgment (introduced below) includes a typing context L, which is either a
single context variable λ or a concrete context ⃗ℓ. This typing context represents
the assumptions about the execution context of the term being typed. If the
10      J. Toman et al.

 typing context is a context variable λ, then no assumptions are made about the
 execution context of the term, although types may depend upon λ with context
 query predicates. Accordingly, function bodies are typed under the context
variable universally quantified over in the corresponding function type; i.e., no
 assumptions are made about the exact execution context of the function body.
As in parametric polymorphism, consistent substitution of a concrete context
⃗ℓ for a context variable λ in a typing derivation yields a valid type derivation
 under concrete context ⃗ℓ.

Remark 1. The context-sensitivity scheme described here corresponds to the
standard CFA approach [50] without a priori call-string limiting. We chose this
scheme because it can be easily encoded with equality over integer variables (see
Section 4), but in principle another context-sensitivity strategy could be used
instead. The important feature of our type system is the inclusion of predicates
over contexts, not the specific choice for these predicates.

   Function type environments are denoted with Θ and are finite maps from
function names (f ) to function types (σ).

 Well Formedness. We impose two well-formedness conditions on types: ownership
well-formedness and refinement well-formedness. The ownership condition is
 purely syntactic: τ is ownership well-formed if τ = τ ′ ref 0 implies τ ′ = ⊤n for
 some n. ⊤i is the “maximal” type of a chain of i references, and is defined
 inductively as ⊤0 = {ν : int | ⊤} , ⊤i = ⊤i−1 ref 0 .
     The ownership well-formedness condition ensures that aliases introduced via
 heap writes do not violate the invariant of ownership types and that refinements
 are consistent with updates performed through mutable aliases. Recall our own-
 ership type invariant ensures all aliases of a mutable reference have 0 ownership.
Any mutations through that mutable alias will therefore be consistent with the
“no information” ⊤ refinement required by this well-formedness condition.
     Refinement well-formedness, denoted L | Γ ⊢WF φ, ensures that free program
variables in refinement φ are bound in a type environment Γ and have integer type.
 It also requires that for a typing context L = λ, only context query predicates
 over λ are used (no such predicates may be used if L = ⃗ℓ). Notice this condition
 forbids refinements that refer to references. Although ownership information can
 signal when refinements on a mutably-aliased reference must be discarded, our
 current formulation provides no such information for refinements that mention
 mutably-aliased references. We therefore conservatively reject such refinements
 at the cost of some expressiveness in our type system.
     We write L | Γ ⊢WF τ to indicate a well-formed type where all refinements are
well-formed with respect to L and Γ . We write L ⊢WF Γ for a type environment
where all types are well-formed. A function environment is well-formed (written
 ⊢WF Θ) if, for every σ in Θ, the argument, result, and output types are well-
 formed with respect to each other and the context variable quantified over in σ.
As the formal definition of refinement well-formedness is fairly standard, we omit
 it for space reasons (the full definition may be found in Section B).
         ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                                             11

                                                                                                              (T-Var)
                          Θ | L | Γ [x : τ1 + τ2 ] ⊢ x : τ1 ⇒ Γ [x ←- τ2 ]

  Θ | L | Γ [y ←- τ1 ∧y y =τ1 x ], x : (τ2 ∧x x =τ2 y) ⊢ e : τ ⇒ Γ ′                x ̸∈ dom(Γ ′ )
                                                                             ′                                (T-Let)
                       Θ | L | Γ [y : τ1 + τ2 ] ⊢ let x = y in e : τ ⇒ Γ

               Θ | L | Γ, x : {ν : int | ν = n} ⊢ e : τ ⇒ Γ ′          x ̸∈ dom(Γ ′ )
                                                                                                          (T-LetInt)
                                Θ | L | Γ ⊢ let x = n in e : τ ⇒ Γ ′

                    Θ | L | Γ [x ←- {ν : int | φ ∧ ν = 0}] ⊢ e1 : τ ⇒ Γ ′
                    Θ | L | Γ [x ←- {ν : int | φ ∧ ν ̸= 0}] ⊢ e2 : τ ⇒ Γ ′
                                                                                                                  (T-If)
                 Θ | L | Γ [x : {ν : int | φ}] ⊢ ifz x then e1 else e2 : τ ⇒ Γ ′

       Θ | L | Γ [y ←- τ1 ], x : (τ2 ∧x x =τ2 y) ref 1 ⊢ e : τ ⇒ Γ ′              Θ | L | Γ ⊢ e1 : τ ′ ⇒ Γ ′
                                x ̸∈ dom(Γ ′ )                                   Θ | L | Γ ′ ⊢ e2 : τ ′′ ⇒ Γ ′′
         Θ | L | Γ [y : τ1 + τ2 ] ⊢ let x = mkref y in e : τ ⇒ Γ ′      Θ | L | Γ ⊢ e1 ; e2 : τ ′′ ⇒ Γ ′′
                                                           (T-MkRef)                            (T-Seq)
                         (
                           τ1 ∧y y =τ1 x r > 0
                   τ′ =
                           τ1                   r=0                      Γ |= φ      ϵ | Γ ⊢WF φ
            Θ | L | Γ [y ←- τ ′ ref r ], x : τ2 ⊢ e : τ ⇒ Γ ′            Θ | L | Γ ⊢ e : τ ⇒Γ′
                            x ̸∈ dom(Γ ′ )                          Θ | L | Γ ⊢ assert(φ) ; e : τ ⇒ Γ ′
      Θ | L | Γ [y : (τ + τ ) ref r ] ⊢ let x = ∗y in e : τ ⇒ Γ ′                            (T-Assert)
                      1     2
                                                       (T-Deref)




                                     Fig. 7. Expression typing rules.


3.2      Intraprocedural Type System

We now introduce the type system for the intraprocedural fragment of our
language. Accordingly, this section focuses on the interplay of mutability and
refinement types. The typing rules are given in Figures 7 and 8. A typing judgment
takes the form Θ | L | Γ ⊢ e : τ ⇒ Γ ′ , which indicates that e is well-typed under
a function type environment Θ, typing context L, and type environment Γ , and
evaluates to a value of type τ and modifies the input environment according to Γ ′ .
Any valid typing derivation must have L ⊢WF Γ , L ⊢WF Γ ′ , and L | Γ ′ ⊢WF τ ,
i.e., the input and output type environments and result type must be well-formed.
     The typing rules in Figure 7 handle the relatively standard features in our
language. The rule T-Seq for sequential composition is fairly straightforward
except that the output type environment for e1 is the input type environment for
e2 . T-LetInt is also straightforward; since x is bound to a constant, it is given
type {ν : int | ν = n} to indicate x is exactly n. The output type environment Γ ′
cannot mention x (expressed with x ̸∈ dom(Γ ′ )) to prevent x from escaping its
scope. This requirement can be met by applying the subtyping rule (see below) to
weaken refinements to no longer mention x . As in other refinement type systems
[47], this requirement is critical for ensuring soundness.
     Rule T-Let is crucial to understanding our ownership type system. The
body of the let expression e is typechecked under a type environment where
the type of y in Γ is linearly split into two types: τ1 for y and τ2 for the newly
created binding x . This splitting is expressed using the + operator. If y is a ref-
erence type, the split operation distributes some portion of y’s ownership infor-
12        J. Toman et al.

mation to its new alias x . The split operation also distributes refinement infor-
mation between the two types. For example, type {ν : int | ν > 0} ref 1 can be
split into (1) {ν : int | ν > 0} ref r and {ν : int | ν > 0} ref (1−r) (for r ∈ (0, 1)),
i.e., two immutable references with non-trivial refinement information, or (2)
{ν : int | ν > 0} ref 1 and {ν : int | ⊤} ref 0 , where one of the aliases is mutable
and the other provides no refinement information. How a type is split depends
on the usage of x and y in e. Formally, we define the type addition operator as
the least commutative partial operation that satisfies the following rules:

        {ν : int | φ1 } + {ν : int | φ2 } = {ν : int | φ1 ∧ φ2 }                (Tadd-Int)
                             r1             r2                      r1 +r2
                    τ1 ref        +τ2 ref        = (τ1 + τ2 ) ref              (Tadd-Ref)

Viewed another way, type addition describes how to combine two types for the
same value such that the combination soundly incorporates all information from
the two original types. Critically, the type addition operation cannot create or
destroy ownership and refinement information, only combine or divide it between
types. Although not explicit in the rules, by ownership well-formedness, if the
entirety of a reference’s ownership is transferred to another type during a split,
all refinements in the remaining type must be ⊤.
    The additional bits ∧y y =τ1 x and ∧x x =τ2 y express equality between x and
y as refinements. We use the strengthening operation τ ∧x φ and typed equality
proposition x =τ y, defined respectively as:

     {ν : int | φ} ∧y φ′ = {ν : int | φ ∧ [ ν /y] φ′ }              (x ={ν : int|φ} y) = (x = y)
            τ ref r ∧y φ′ = τ ref r                                    (x =τ ref r y) = ⊤

We do not track equality between references or between the contents of aliased
reference cells as doing so would violate our refinement well-formedness condition.
These operations are also used in other rules that can introduce equality.
    Rule T-MkRef is very similar to T-Let, except that x is given a reference
type of ownership 1 pointing to τ2 , which is obtained by splitting the type of y. In
T-Deref, the content type of y is split and distributed to x . The strengthening
is conditionally applied depending on the ownership of the dereferenced pointer,
that is, if r = 0, τ ′ has to be a maximal type ⊤i .
    Our type system also tracks path information; in the T-If rule, we update the
refinement on the condition variable within the respective branches to indicate
whether the variable must be zero. By requiring both branches to produce the
same output type environment, we guarantee that these conflicting refinements
are rectified within the type derivations of the two branches.
    The type rule for assert statements has the precondition Γ |= φ which is
defined to be |= JΓ K =⇒ φ, i.e., the logical formula JΓ K =⇒ φ is valid in the
chosen theory. JΓ K lifts the refinements on the integer valued variables into a
proposition in the logic used for verification. This denotation operation is defined
as:
                        J•K = ⊤             J{ν : int | φ}Ky = [y/ ν ] φ
                JΓ, x : τ K = JΓ K ∧ Jτ Kx        Jτ ′ ref r Ky = ⊤
        ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                                              13

                           (The shapes of τ ′ and τ2 are similar)
                Θ | L | Γ [x ←- τ1 ][y ←- (τ2 ∧y y =τ2 x ) ref 1 ] ⊢ e : τ ⇒ Γ ′
                                                                                                              (T-Assign)
                  Θ | L | Γ [x : τ1 + τ2 ][y : τ ′ ref 1 ] ⊢ y : = x ; e : τ ⇒ Γ ′
                                                             ′             ′
                       (τ1 ref r1 +τ2 ref r2 ) ≈ (τ1′ ref r1 +τ2′ ref r2 )
                                            ′                 ′
                   Θ | L | Γ [x ←- τ1′ ref r1 ][y ←- τ2′ ref r2 ] ⊢ e : τ ⇒ Γ ′
                                                                                                               (T-Alias)
             Θ | L | Γ [x : τ1 ref r1 ][y : τ2 ref r2 ] ⊢ alias(x = y) ; e : τ ⇒ Γ ′
                                                             ′             ′
                       (τ1 ref r1 +τ2 ref r2 ) ≈ (τ1′ ref r1 +τ2′ ref r2 )
                                        ′                  ′
               Θ | L | Γ [x ←- τ1′ ref r1 ][y ←- (τ2′ ref r2 ) ref r ] ⊢ e : τ ⇒ Γ ′
                                                                                                         (T-AliasPtr)
         Θ | L | Γ [x : τ1 ref r1 ][y : (τ2 ref r2 ) ref r ] ⊢ alias(x = ∗y) ; e : τ ⇒ Γ ′

                 Γ ≤ Γ′        Θ | L | Γ ′ ⊢ e : τ ⇒ Γ ′′        Γ ′′ , τ ≤ Γ ′′′ , τ ′
                                                                                                                (T-Sub)
                                   Θ | L | Γ ⊢ e : τ ′ ⇒ Γ ′′′

                                  τ1 ≈ τ2 iff • ⊢ τ1 ≤ τ2 and • ⊢ τ2 ≤ τ1 .



                           Fig. 8. Pointer manipulation and subtyping

          Γ |= φ1 =⇒ φ2                                     ∀ x ∈ dom(Γ ′ ).Γ ⊢ Γ (x ) ≤ Γ ′ (x )
                                               (S-Int)                                                        (S-TyEnv)
 Γ ⊢ {ν : int | φ1 } ≤ {ν : int | φ2 }                                          Γ ≤ Γ′

      r1 ≥ r 2     Γ ⊢ τ 1 ≤ τ2                             Γ, x : τ ≤ Γ ′ , x : τ ′           x ̸∈ dom(Γ )
                                               (S-Ref)                                                           (S-Res)
      Γ ⊢ τ1 ref r1 ≤ τ2 ref r2                                                Γ, τ ≤ Γ, τ ′

                                         Fig. 9. Subtyping rules.


If the formula JΓ K =⇒ φ is valid, then in any context and under any valuation
of program variables that satisfy the refinements in JΓ K, the predicate φ must be
true and the assertion must not fail. This intuition forms the foundation of our
soundness claim (Section 3.4).

Destructive Updates, Aliasing, and Subtyping. We now discuss the handling
of assignment, aliasing annotations, and subtyping as described in Figure 8.
Although apparently unrelated, all three concern updating the refinements of
(potentially) aliased reference cells.
    Like the binding forms discussed above, T-Assign splits the assigned value’s
type into two types via the type addition operator, and distributes these types
between the right hand side of the assignment and the mutated reference contents.
Refinement information in the fresh contents may be inconsistent with any
previous refinement information; only the shapes must be the same. In a system
with unrestricted aliasing, this typing rule would be unsound as it would admit
writes that are inconsistent with refinements on aliases of the left hand side.
However, the assignment rule requires that the updated reference has an ownership
of 1. By the ownership type invariant, all aliases with the updated reference have 0
ownership, and by ownership well-formedness may only contain the ⊤ refinement.

Example 3. We can type the program as follows:
let x = mkref 5 in                    // x : {ν : int | ν = 5} ref 1
let y = x in                          // x : ⊤1 , y : {ν : int | ν = 5} ref 1
14        J. Toman et al.

     y := 4; assert(*y = 4) // x : ⊤1 , y : {ν : int | ν = 4} ref 1
In this and later examples, we include type annotations within comments. We
stress that these annotations are for expository purposes only; our tool can infer
these types automatically with no manual annotations.

    As described thus far, the type system is quite strict: if ownership has been
completely transferred from one reference to another, the refinement information
found in the original reference is effectively useless. Additionally, once a mutable
pointer has been split through an assignment or let expression, there is no
way to recover mutability. The typing rule for must alias assertions, T-Alias
and T-AliasPtr, overcomes this restriction by exploiting the must-aliasing
information to “shuffle” or redistribute ownerships and refinements between two
                                                                        ′           ′
aliased pointers. The typing rule assigns two fresh types τ1′ ref r1 and τ2′ ref r2 to
the two operand pointers. The choice of τ1′ , r1′ , τ2′ , and r2′ is left open provided
                                           ′              ′
that the sum of the new types, (τ1′ ref r1 ) + (τ2′ ref r2 ) is equivalent (denoted ≈)
to the sum of the original types. Formally, ≈ is defined as in Figure 8; it implies
that any refinements in the two types must be logically equivalent and that
ownerships must also be equal. This redistribution is sound precisely because the
two references are assumed to alias; the total ownership for the single memory
cell pointed to by both references cannot be increased by this shuffling. Further,
any refinements that hold for the contents of one reference must necessarily hold
for contents of the other and vice versa.

Example 4 (Shuffling ownerships and refinements). Let φ=n be ν = n.
let x = mkref 5 in // x : {ν : int | φ=5 } ref 1
let y = x in          // x : ⊤1 , y : {ν : int | φ=5 } ref 1
  y := 4; alias(x = y) // x : {ν : int | φ=4 } ref 0.5 , y : {ν : int | φ=4 } ref 0.5
The final type assignment for x and y is justified by

       ⊤1 + {ν : int | φ=4 } ref 1 = {ν : int | ⊤ ∧ φ=4 } ref 1 ≈
       {ν : int | φ=4 ∧ φ=4 } ref 1 = {ν : int | φ=4 } ref 0.5 + {ν : int | φ=4 } ref 0.5 .

    The aliasing rules give fine-grained control over ownership information. This
flexibility allows mutation through two or more aliased references within the
same scope. Provided sufficient aliasing annotations, the type system may shuffle
ownerships between one or more live references, enabling and disabling mutability
as required. Although the reliance on these annotations appears to decrease the
practicality of our type system, we expect these aliasing annotations can be
inserted by a conservative must-aliasing analysis. Further, empirical experience
from our prior work [56] indicates that only a small number of annotations are
required for larger programs.

Example 5 (Shuffling Mutability). Let φ=n again be ν = n. The following
program uses two live, aliased references to mutate the same memory location:
        ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                                     15



           Θ(f ) = ∀λ. ⟨x1 : τ1 , . . . , xn : τn ⟩ → ⟨x1 : τ1′ , . . . , xn : τn′ | τ ⟩
                    σα = [ℓ : L/λ]          σx = [y1 /x1 ] · · · [yn /xn ]
      Θ | L | Γ [yi ←- σα σx τi′ ], x : σα σx τ ⊢ e : τ ′ ⇒ Γ ′              x ̸∈ dom(Γ ′ )
                                                                                                      (T-Call)
          Θ | L | Γ [yi : σα σx τi ] ⊢ let x = f ℓ (y1 , . . . , yn ) in e : τ ′ ⇒ Γ ′

             Θ(f ) = ∀λ. ⟨x1 : τ1 , . . . , xn : τn ⟩ → ⟨x1 : τ1′ , . . . , xn : τn′ | τ ⟩
              Θ | λ | x1 : τ1 , . . . , xn : τn ⊢ e : τ ⇒ x1 : τ1′ , . . . , xn : τn′
                                                                                               (T-FunDef)
                                    Θ ⊢ f 7→ (x1 , .. , xn )e

 ∀f 7→ (x1 , .. , xn )e ∈ D.Θ ⊢ f 7→ (x1 , .. , xn )e                          Θ⊢D           ⊢WF Θ
                dom(D) = dom(Θ)                                                Θ | ϵ | • ⊢ e : τ ⇒Γ
                          Θ⊢D                                                          ⊢ ⟨D, e⟩
                                                (T-Funs)                                  (T-Prog)


                                      Fig. 10. Program typing rules


let x = mkref 0 in
let y = x in           // x : {ν : int | φ=0 } ref 1 , y : ⊤1
  x := 1; alias(x = y); // x : ⊤1 , y : {ν : int | φ=1 } ref 1
  y := 2; alias(x = y); // x : {ν : int | φ=2 } ref 0.5 , y : {ν : int | φ=2 } ref 0.5
  assert(*x = 2)
After the first aliasing statement the type system shuffles the (exclusive) mutability
between x and y to enable the write to y. After the second aliasing statement
the ownership in y is split with x ; note that transferring all ownership from y to
x would also yield a valid typing.

    Finally, we describe the subtyping rule. The rules for subtyping types and
environments are shown in Figure 9. For integer types, the rules require the
refinement of a supertype is a logical consequence of the subtype’s refinement
conjoined with the lifting of Γ . The subtype rule for references is covariant in
the type of reference contents. It is widely known that in a language with un-
restricted aliasing and mutable references such a rule is unsound: after a write
into the coerced pointer, reads from an alias may yield a value disallowed by
the alias’ type [43]. However, as in the assign case, ownership types prevent un-
soundness; a write to the coerced pointer requires the pointer to have ownership
1, which guarantees any aliased pointers have the maximal type and provide no
information about their contents beyond simple types.


3.3     Interprocedural Fragment and Context-Sensitivity

We now turn to a discussion of the interprocedural fragment of our language,
and how our type system propagates context information. The remaining typing
16      J. Toman et al.

rules for our language are shown in Figure 10. These rules concern the typing of
function calls, function bodies, and entire programs.
    We first explain the T-Call rule. The rule uses two substitution maps. σx
translates between the parameter names used in the function type and actual
argument names at the call-site. σα instantiates all occurrences of λ in the callee
type with ℓ : L, where ℓ is the label of the call-site and L the typing context of
the call. The types of the arguments yi ’s are required to match the parameter
types (post substitution). The body of the let binding is then checked with
the argument types updated to reflect the changes in the function call (again,
post substitution). This update is well-defined because we require all function
arguments be distinct as described in Section 2.1. Intuitively, the substitution σα
represents incrementally refining the behavior of the callee function with partial
context information. If L is itself a context variable λ′ , this substitution effectively
transforms any context prefix queries over λ in the argument/return/output
types into a queries over ℓ : λ′ . In other words, while the exact concrete execution
context of the callee is unknown, the context must at least begin with ℓ which
can potentially rule out certain behaviors.
    Rule T-FunDef type checks a function definition f 7→ (x1 , .. , xn )e against
the function type given in Θ. As a convenience we assume that the parameter
names in the function type match the formal parameters in the function definition.
The rule checks that under an initial environment given by the argument types the
function body produces a value of the return type and transforms the arguments
according to the output types. As mentioned above, functions may be executed
under many different contexts, so type checking the function body is performed
under the context variable λ that occurs in the function type.
    Finally, the rule for typing programs (T-Prog) checks that all function
definitions are well typed under a well-formed function type environment, and
that the entry point e is well typed in an empty type environment and the typing
context ϵ, i.e., the initial context.

Example 6 (1-CFA). Recall the program in Figure 3 in Section 1; assume the
function calls are labeled as follows:
p := getℓ1 (p) + 1;
// ...
q := getℓ2 (q) + 1;
Taking τp to be the type shown in Example 2:

              {ν : int | (ℓ1 ⪯ λ =⇒ ν = 3) ∧ (ℓ2 ⪯ λ =⇒ ν = 5)}

we can give get the type ∀λ. z : τp ref 1 → z : τp ref 1 | τp .

Example 7 (2-CFA). To see how context information propagates across multiple
calls, consider the following change to the code considered in Example 6:
     get_real(z) { *z }
     get(z) { get_realℓ3 (z) }
       ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                          17

The type of get remains as in Example 6, and taking τ to be

            {ν : int | (ℓ3 ℓ1 ⪯ λ′ =⇒ ν = 3) ∧ (ℓ3 ℓ2 ⪯ λ′ =⇒ ν = 5)}

the type of get_real is: ∀λ′ . z : τ ref 1 → z : τ ref 1 | τ .
   We focus on the typing of the call to get_real in get; it is typed in context
λ and a type environment where p is given type τp from Example 6.
   Applying the substitution [ℓ3 : λ/λ′ ] to the argument type of get_real yields:

    {ν : int | (ℓ3 ℓ1 ⪯ ℓ3 : λ =⇒ ν = 3) ∧ (ℓ3 ℓ2 ⪯ ℓ3 : λ =⇒ ν = 5)} ref 1 ≈
      {ν : int | (ℓ1 ⪯ λ =⇒ ν = 3) ∧ (ℓ2 ⪯ λ =⇒ ν = 5)} ref 1

which is exactly the type of p. A similar derivation applies to the return type of
get_real and thus get.

3.4    Soundness
We have proven that any program that type checks according to the rules above
will never experience an assertion failure. We formalize this claim with the
following soundness theorem.

Theorem 1 (Soundness). If ⊢ ⟨D, e⟩, then ⟨∅, ∅, ·, e⟩ ̸−→∗D AssertFail.
    Further, any well-typed program either diverges, halts in the configuration
AliasFail, or halts in a configuration ⟨H , R, ·, x ⟩ for some H , R and x , i.e.,
evaluation does not get stuck.

Proof (Sketch). By standard progress and preservation lemmas; the full proof has
been omitted for space reasons and can be found in the accompanying appendix.


4     Inference and Extensions
We now briefly describe the inference algorithm implemented in our tool Con-
SORT. We sketch some implemented extensions needed to type more interesting
programs and close with a discussion of current limitations of our prototype.

4.1    Inference
Our tool first runs a standard, simple type inference algorithm to generate type
templates for every function parameter type, return type, and for every live
variable at each program point. For a variable x of simple type τS ::= int | τS ref
at program point p, ConSORT generates a type template JτS Kx ,0,p as follows:

    JintKx ,n,p = {ν : int | φx ,n,p (ν; FVp )}   JτS ref Kx ,n,p = JτS Kx ,n+1,p ref rx ,n,p

φx ,n,p (ν; FVp ) denotes a fresh relation symbol applied to ν and the free variables
of simple type int at program point p (denoted FVp ). rx ,n,p is a fresh ownership
18      J. Toman et al.

variable. For each function f , there are two synthetic program points, f b and f e
for the beginning and end of the function respectively. At both points, ConSORT
generates type template for each argument, where FVf b and FVf e are the names
of integer typed parameters. At f e , ConSORT also generates a type template
for the return value. We write Γ p to indicate the type environment at point p,
where every variable
                V        is mapped to its corresponding type template. JΓ p K is thus
equivalent to x ∈FVp φx ,0,p (x ; FVp ).
    When generating these type templates, our implementation also generates own-
ership well-formedness constraints. Specifically, for a type template of the form
{ν : int | φx ,n+1,p (ν; FVp )} ref rx ,n,p ConSORT emits the constraint: rx ,n,p =
0 =⇒ φx ,n+1,p (ν; FVp ) and for a type template (τ ref rx ,n+1,p ) ref rx ,n,p Con-
SORT emits the constraint rx ,n,p = 0 =⇒ rx ,n+1,p = 0.
    ConSORT then walks the program, generating constraints between relation
symbols and ownership variables according to the typing rules. These constraints
take three forms, ownership constraints, subtyping constraints, and assertion
constraints. Ownership constraints are simple linear (in)equalities over ownership
variables and constants, according to conditions imposed by the typing rules.
For example, if variable x has the type template τ ref rx ,0,p for the expression
x : = y ; e at point p, ConSORT generates the constraint rx ,0,p = 1.
    ConSORT emits subtyping constraints between the relation symbols at
related program points according to the rules of the type system. For example, for
the term let x = y in e at program point p (where e is at program point p′ , and x
has simple type int ref ) ConSORT generates the following subtyping constraint:
          JΓ p K ∧ φy,1,p (ν; FVp ) =⇒ φy,1,p′ (ν; FVp′ ) ∧ φx ,1,p′ (ν; FVp′ )
in addition to the ownership constraint ry,0,p = ry,0,p′ + rx ,0,p′ .
    Finally, for each assert(φ) in the program, ConSORT emits an assertion
constraint of the form: JΓ p K =⇒ φ which requires the refinements on integer
typed variables in scope are sufficient to prove φ.

Encoding Context Sensitivity. To make inference tractable, we require the user
to fix a priori the maximum length of prefix queries to a constant k (this choice
is easily controlled with a command line parameter to our tool). We supplement
the arguments in every predicate application with a set of integer context vari-
ables c1 , . . . , ck ; these variables do not overlap with any program variables.
     ConSORT uses these variables to infer context sensitive refinements as
follows. Consider a function call let x = f ℓ (y1 , . . . , yn ) in e at point p where e
is at point p′ . ConSORT generates the following constraint for a refinement
φyi ,n,p (ν, c1 , . . . , ck ; FVp ) which occurs in the type template of yi :
      φyi ,n,p (ν, c0 , . . . , ck ; FVp ) =⇒ σx φxi ,n,f b (ν, ℓ, c0 , . . . , ck −1 ; FVf b )
      σx φxi ,n,f e (ν, ℓ, c0 , . . . , ck −1 ; FVf e ) =⇒ φyi ,n,p′ (ν, c0 , . . . , ck ; FVp′ )
      σx = [y1 /x1 ] · · · [yn /xn ]
Effectively, we have encoded ℓ1 . . . ℓk ⪯ λ as ∧0<i≤k ci = ℓi . In the above, the
shift from c0 , . . . , ck to ℓ, c0 , . . . , ck −1 plays the role of σα in the T-Call rule.
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                19

The above constraint serves to determine the value of c0 within the body of the
function f . If f calls another function g, the above rule propagates this value of
c0 to c1 within g and so on. The solver may then instantiate relation symbols
with predicates that are conditional over the values of ci .

Solving Constraints. The results of the above process are two systems of con-
straints; real arithmetic constraints over ownership variables and constrained Horn
clauses (CHC) over the refinement relations. Under certain assumptions about the
simple types in a program, the size of the ownership and subtyping constraints will
be polynomial to the size of the program. These systems are not independent; the
relation constraints may mention the value of ownership variables due to the well-
formedness constraints described above. The ownership constraints are first solved
with Z3 [16]. These constraints are non-linear but Z3 appears particularly well-
engineered to quickly find solutions for the instances generated by ConSORT. We
constrain Z3 to maximize the number of non-zero ownership variables to ensure as
few refinements as possible are constrained to be ⊤ by ownership well-formedness.
    The values of ownership variables inferred by Z3 are then substituted into the
constrained Horn clauses, and the resulting system is checked for satisfiability
with an off-the-shelf CHC solver. Our implementation generates constraints in
the industry standard SMT-Lib2 format [8]; any solver that accepts this format
can be used as a backend for ConSORT. Our implementation currently supports
Spacer [37] (part of the Z3 solver [16]), HoICE [13], and Eldarica [48] (adding a
new backend requires only a handful of lines of glue code). We found that different
solvers are better tuned to different problems; we also implemented parallel mode
which runs all supported solvers in parallel, using the first available result.

4.2   Extensions
Primitive Operations. As defined in Section 2, our language can compare integers
to zero and load and store them from memory, but can perform no meaningful
computation over these numbers. To promote the flexibility of our type system
and simplify our soundness statement, we do not fix a set of primitive operations
and their static semantics. Instead, we assume any set of primitive operations
used in a program are given sound function types in Θ. For example, under the
assumption that + has its usual semantics and the underlying logic supports +, we
can give + the type ∀λ. ⟨x : ⊤0 , y : ⊤0 ⟩ → ⟨x : ⊤0 , y : ⊤0 | {ν : int | ν = x + y}⟩.
Interactions with a nondeterministic environment or unknown program inputs
can then be modeled with a primitive that returns integers refined with ⊤.

Dependent Tuples. Our implementation supports types of the form: (x1 : τ1 , . . . ,
xn : τn ), where xi can appear within τj (j =       ̸ i) if τi is an integer type. For
example, (x : {ν : int | ⊤} , y : {ν : int | ν > x }) is the type of tuples whose second
element is strictly greater than the first. We also extend the language with tuple
constructors as a new value form, and let bindings with tuple patterns as the LHS.
   The extension to type checking is relatively straightforward; the only signifi-
cant extensions are to the subtyping rules. Specifically, the subtyping check for a
20      J. Toman et al.

tuple element xi : τi is performed in a type environment elaborated with the types
and names of other tuple elements. The extension to type inference is also straight-
forward; the arguments for a predicate symbol include any enclosing dependent
tuple names and the environment in subtyping constraints is likewise extended.

Recursive Types. Our language also supports some unbounded heap structures
via recursive reference types. To keep inference tractable, we forbid nested recur-
sive types, multiple occurrences of the recursive type variable, and additionally
fix the shape of refinements that occur within a recursive type. For recursive re-
finements that fit the above restriction, our approach for refinements is broadly
similar to that in [35], and we use the ownership scheme of [56] for handling
ownership. We first use simple type inference to infer the shape of the recursive
types, and automatically insert fold/unfold annotations into the source program.
As in [35], the refinements within an unfolding of a recursive type may refer to
dependent tuple names bound by the enclosing type. These recursive types can
express, e.g., the invariants of a mutable, sorted list. As in [56], recursive types
are unfolded once before assigning ownership variables; further unfoldings copy
existing ownership variables.
    As in Java or C++, our language does not support sum types, and any
instantiation of a recursive type must use a null pointer. Our implementation
supports an ifnull construct in addition to a distinguished null constant. Our
implementation allows any refinement to hold for the null constant, including
⊥. Currently, our implementation does not detect null pointer dereferences, and
all soundness guarantees are made modulo freedom of null dereferences. As JΓ K
omits refinements under reference types, null pointer refinements do not affect
the verification of programs without null pointer dereferences.

Arrays. Our implementation supports arrays of integers. Each array is given an
ownership describing the ownership of memory allocated for the entire array. The
array type contains two refinements: the first refines the length of the array itself,
and the second refines the entire array contents. The content refinement may
refer to a symbolic index variable for precise, per-index refinements. At reads
and writes to the array, ConSORT instantiates the refinement’s symbolic index
variable with the concrete index used at the read/write.
    As in [56], our restriction to arrays of integers stems from the difficulty of
ownership inference. Soundly handling pointer arrays requires index-wise tracking
of ownerships which significantly complicates automated inference. We leave
supporting arrays of pointers to future work.

4.3   Limitations
Our current approach is not complete; there are safe programs that will be rejected
by our type system. As mentioned in Section 3.1, our well-formedness condition
forbids refinements that refer to memory locations. As a result, ConSORT
cannot in general express, e.g., that the contents of two references are equal.
Further, due to our reliance on automated theorem provers we are restricted to
       ConSORT: Context- and Flow-Sensitive Ownership Refinement Types               21

Table 1. Description of benchmark suite adapted from JayHorn. Java are programs
that test Java-specific features. Inc are tests that cannot be handled by ConSORT, e.g.,
null checking, etc. Bug includes a “safe” program we discovered was actually incorrect.

                         Set Orig. Adapted Java Inc Bug
                        Safe     41      32       6    2    1
                       Unsafe    41      26       13   2    0




logics with sound but potentially incomplete decision procedures. ConSORT
also does not support conditional or context-sensitive ownerships, and therefore
cannot precisely handle conditional mutation or aliasing.


5     Experiments

We now present the results of preliminary experiments performed with the imple-
mentation described in Section 4. The goal of these experiments was to answer the
following questions: i) is the type system (and extensions of Section 4) expressive
enough to type and verify non-trivial programs? and ii) is type inference feasible?
    To answer these questions, we evaluated our prototype implementation on two
sets of benchmarks.4 The first set is adapted from JayHorn [32, 33], a verification
tool for Java. This test suite contains a combination of 82 safe and unsafe
programs written in Java. We chose this benchmark suite as, like ConSORT,
JayHorn is concerned with the automated verification of programs in a language
with mutable, aliased memory cells. Further, although some of their benchmark
programs tested Java specific features, most could be adapted into our low-level
language. The tests we could adapt provide a comparison with existing state-of-
the-art verification techniques. A detailed breakdown of the adapted benchmark
suite can be found in Table 1.

Remark 2. The original JayHorn paper includes two additional benchmark sets,
Mine Pump and CBMC. Both our tool and recent JayHorn versions time out on
the Mine Pump benchmark. Further, the CBMC tests were either subsumed by
our own test programs, tested Java specific features, or tested program synthesis
functionality. We therefore omitted both of these benchmarks from our evaluation.

   The second benchmark set consists of data structure implementations and
microbenchmarks written directly in our low-level imperative language. We
developed this suite to test the expressive power of our type system and inference.
The programs included in this suite are:

 – Array-List Implementation of an unbounded list backed by an array.
4
    Our experiments and the ConSORT source code are available at https://www.fos.
    kuis.kyoto-u.ac.jp/projects/consort/.
22     J. Toman et al.

Table 2. Comparison of ConSORT to JayHorn on the benchmark set of [32] (top) and
our custom benchmark suite (bottom). T/O indicates a time out.

                                      ConSORT       JayHorn
                   Set   N. Tests Correct T/O Correct T/O Imp.
                 Safe        32         29   3    24     5        3
                Unsafe       26         26   0    19     0        7
Name          Safe? Time(s) Ann JH Name                      Safe? Time(s) Ann JH
Array-Inv      ✓     10.07        0   T/O Array-Inv-BUG       X       5.29   0   T/O
Array-List     ✓     16.76        0   T/O Array-List-BUG      X       1.13   0   T/O
Intro2         ✓      0.08        0   T/O Intro2-BUG          X       0.02   0   T/O
Mut-List       ✓      1.45        3   T/O Mut-List-BUG        X       0.41   3   T/O
Shuffle        ✓      0.13        3    ✓ Shuffle-BUG          X       0.07   3    X
Sorted-List    ✓      1.90        3   T/O Sorted-List-BUG     X       1.10   3   T/O




 – Sorted-List Implementation of a mutable, sorted list maintained with an
   in-place insertion sort algorithm.
 – Shuffle Multiple live references are used to mutate the same location in
   program memory as in Example 5.
 – Mut-List Implementation of general linked lists with a clear operation.
 – Array-Inv A program which allocates a length n array and writes the value
   i at every index i.
 – Intro2 The motivating program shown in Figure 2 in Section 1.

We introduced unsafe mutations to these programs to check our tool for unsound-
ness and translated these programs into Java for further comparison with JayHorn.
    Our benchmarks and JayHorn’s require a small number of trivially identi-
fied alias annotations. The adapted JayHorn benchmarks contain a total of 6
annotations; the most for any individual test was 3. The number of annotations
required for our benchmark suite are shown in column Ann. of Table 2.
    We first ran ConSORT on each program in our benchmark suite and ran
version 0.7 of JayHorn on the corresponding Java version. We recorded the final
verification result for both our tool and JayHorn. We also collected the end-to-end
runtime of ConSORT for each test; we do not give a performance comparison
with JayHorn given the many differences in target languages. For the JayHorn
suite, we first ran our tool on the adapted version of each test program and ran
JayHorn on the original Java version. We also did not collect runtime information
for this set of experiments because our goal is a comparison of tool precision, not
performance. All tests were run on a machine with 16 GB RAM and 4 Intel i5
CPUs at 2GHz and with a timeout of 60 seconds (the same timeout was used in
[32]). We used ConSORT’s parallel backend (Section 4) with Z3 version 4.8.4,
HoICE version 1.8.1, and Eldarica version 2.0.1 and JayHorn’s Eldarica backend.
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types             23

5.1   Results
The results of our experiments are shown in Table 2. On the JayHorn benchmark
suite ConSORT performs competitively with JayHorn, correctly identifying 29
of the 32 safe programs as such. For all 3 tests on which ConSORT timed out
after 60 seconds, JayHorn also timed out (column T/O). For the unsafe programs,
ConSORT correctly identified all programs as unsafe within 60 seconds; JayHorn
answered Unknown for 7 tests (column Imp.).
    On our own benchmark set, ConSORT correctly verifies all safe versions of
the programs within 60 seconds. For the unsafe variants, ConSORT was able to
quickly and definitively determine these programs unsafe. JayHorn times out on
all tests except for Shuffle and ShuffleBUG (column JH). We investigated the
cause of time outs and discovered that after verification failed with an unbounded
heap model, JayHorn attempts verification on increasingly larger bounded heaps.
In every case, JayHorn exceeded the 60 second timeout before reaching a pre-
configured limit on the heap bound. This result suggests JayHorn struggles in
the presence of per-object invariants and unbounded allocations; the only two
tests JayHorn successfully analyzed contain just a single object allocation.
    We do not believe this struggle is indicative of a shortcoming in JayHorn’s
implementation, but stems from the fundamental limitations of JayHorn’s memory
representation. Like many verification tools (see Section 6), JayHorn uses a single,
unchanging invariant to for every object allocated at the same syntactic location;
effectively, all objects allocated at the same location are assumed to alias with one
another. This representation cannot, in general, handle programs with different
invariants for distinct objects that evolve over time. We hypothesize other tools
that adopt a similar approach will exhibit the same difficulty.


6     Related Work
The difficulty in handling programs with mutable references and aliasing has been
well-studied. Like JayHorn, many approaches model the heap explicitly at ver-
ification time, approximating concrete heap locations with allocation site labels
[14, 20, 32, 33, 46]; each abstract location is also associated with a refinement. As
abstract locations summarize many concrete locations, this approach does not in
general admit strong updates and flow-sensitivity; in particular, the refinement
associated with an abstract location is fixed for the lifetime of the program. The
techniques cited above include various workarounds for this limitation. For exam-
ple, [14, 46] temporarily allows breaking these invariants through a distinguished
program name as long as the abstract location is not accessed through another
name. The programmer must therefore eventually bring the invariant back in
sync with the summary location. As a result, these systems ultimately cannot
precisely handle programs that require evolving invariants on mutable memory.
    A similar approach was taken in CQual [23] by Aiken et al. [2]. They used
an explicit restrict binding for pointers. Strong updates are permitted through
pointers bound with restrict, but the program is forbidden from using any pointers
which share an allocation site while the restrict binding is live.
24      J. Toman et al.

    A related technique used in the field of object-oriented verification is to declare
object invariants at the class level and allow these invariants on object fields to be
broken during a limited period of time [7, 22]. In particular, the work on Spec#
[7] uses an ownership system which tracks whether object a owns object b; like
ConSORT’s ownership system, these ownerships contain the effects of mutation.
However, Spec#’s ownership is quite strict and does not admit references to b
outside of the owning object a.
    Viper [30, 42] (and its related projects [31, 39]) uses access annotations (ex-
pressed as permission predicates) to explicitly transfer access/mutation permis-
sions for references between static program names. Like ConSORT, permissions
may be fractionally transferred, allowing temporary shared, immutable access to
a mutable memory cell. However, while ConSORT automatically infers many
ownership transfers, Viper requires extensive annotations for each transfer.
    F*, a dependently typed dialect of ML, includes an update/select theory of
heaps and requires explicit annotations summarizing the heap effects of a method
[44, 57, 58]. This approach enables modular reasoning and precise specification of
pre- and post-conditions with respect to the heap, but precludes full automation.
    The work on rely–guarantee reference types by Gordon et al. [26, 27] uses re-
finement types in a language mutable references and aliasing. Their approach ex-
tends reference types with rely/guarantee predicates; the rely predicate describes
possible mutations via aliases, and the guarantee predicate describes the admissi-
ble mutations through the current reference. If two references may alias, then the
guarantee predicate of one reference implies the rely predicate of the other and
vice versa. This invariant is maintained with a splitting operation that is similar
to our + operator. Further, their type system allows strong updates to reference
refinements provided the new refinements are preserved by the rely predicate.
Thus, rely–guarantee refinement support multiple mutable, aliased references
with non-trivial refinement information. Unfortunately this expressiveness comes
at the cost of automated inference and verification; an embedding of this system
into Liquid Haskell [62] described in [27] was forced to sacrifice strong updates.
    Work by Degen et al. [17] introduced linear state annotations to Java. To effect
strong updates in the presence of aliasing, like ConSORT, their system requires
annotated memory locations are mutated only through a distinguished reference.
Further, all aliases of this mutable reference give no information about the state
of the object much like our 0 ownership pointers. However, their system cannot
handle multiple, immutable aliases with non-trivial annotation information; only
the mutable reference may have non-trivial annotation information.
    The fractional ownerships in ConSORT and their counterparts in [55, 56]
have a clear relation to linear type systems. Many authors have explored the
use of linear type systems to reason in contexts with aliased mutable references
[18, 19, 52], and in particular with the goal of supporting strong updates [1].
A closely related approach is RustHorn by Matsushita et al. [40]. Much like
ConSORT, RustHorn uses CHC and linear aliasing information for the sound
and—unlike ConSORT—complete verification of programs with aliasing and
mutability. However, their approach depends on Rust’s strict borrowing discipline,
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                  25

and cannot handle programs where multiple aliased references are used in the
same lexical region. In contrast, ConSORT supports fine-grained, per-statement
changes in mutability and even further control with alias annotations, which
allows it to verify larger classes of programs.
    The ownerships of ConSORT also have a connection to separation logic
[45]; the separating conjunction isolates write effects to local subheaps, while
ConSORT’s ownership system isolates effects to local updates of pointer types.
Other researchers have used separation logic to precisely support strong updates
of abstract state. For example, in work by Kloos et al. [36] resources are associated
with static, abstract names; each resource (represented by its static name) may
be owned (and thus, mutated) by exactly one thread. Unlike ConSORT, their
ownership system forbids even temporary immutable, shared ownership, or
transferring ownerships at arbitrary program points. An approach proposed by
Bakst and Jhala [4] uses a similar technique, combining separation logic with
refinement types. Their approach gives allocated memory cells abstract names, and
associates these names with refinements in an abstract heap. Like the approach
of Kloos et al. and ConSORT’s ownership 1 pointers, they ensure these abstract
locations are distinct in all concrete heaps, enabling sound, strong updates.
    The idea of using a rational number to express permissions to access a refer-
ence dates back to the type system of fractional permissions by Boyland [12]. His
work used fractional permissions to verify race freedom of a concurrent program
without a may-alias analysis. Later, Terauchi [59] proposed a type-inference algo-
rithm that reduces typing constraints to a set of linear inequalities over rational
numbers. Boyland’s idea also inspired a variant of separation logic for a concurrent
programming language [11] to express sharing of read permissions among several
threads. Our previous work [55, 56], inspired by that in [11, 59], proposed meth-
ods for type-based verification of resource-leak freedom, in which a rational num-
ber expresses an obligation to deallocate certain resource, not just a permission.
    The issue of context-sensitivity (sometimes called polyvariance) is well-studied
in the field of abstract interpretation (e.g., [28, 34, 41, 50, 51], see [25] for a recent
survey). Polyvariance has also been used in type systems to assign different behav-
iors to the same function depending on its call site [3, 6, 63]. In the area of refine-
ment type systems, Zhu and Jagannathan developed a context-sensitive dependent
type system for a functional language [66] that indexed function types by unique
labels attached to call-sites. Our context-sensitivity approach was inspired by this
work. In fact, we could have formalized context-polymorphism within the frame-
work of full dependent types, but chose the current presentation for simplicity.


7    Conclusion

We presented ConSORT, a novel type system for safety verification of imperative
programs with mutability and aliasing. ConSORT is built upon the novel combi-
nation of fractional ownership types and refinement types. Ownership types flow-
sensitively and precisely track the existence of mutable aliases. ConSORT admits
sound strong updates by discarding refinement information on mutably-aliased
26      J. Toman et al.

references as indicated by ownership types. Our type system is amenable to auto-
matic type inference; we have implemented a prototype of this inference tool and
found it can verify several non-trivial programs and outperforms a state-of-the-art
program verifier. As an area of future work, we plan to investigate using fractional
ownership types to soundly allow refinements that mention memory locations.

Acknowledgments The authors would like to the reviewers for their thoughtful feedback
and suggestions, and Yosuke Fukuda and Alex Potanin for their feedback on early drafts.
This work was supported in part by JSPS KAKENHI, grant numbers JP15H05706 and
JP19H04084, and in part by the JST ERATO MMSD Project.


Bibliography

 [1] Ahmed, A., Fluet, M., Morrisett, G.: L3 : a linear language with locations.
     Fundamenta Informaticae 77(4), 397–449 (2007)
 [2] Aiken, A., Foster, J.S., Kodumal, J., Terauchi, T.: Checking and
     inferring local non-aliasing. In: Conference on Programming Lan-
     guage Design and Implementation (PLDI). pp. 129–140 (2003).
     https://doi.org/10.1145/781131.781146
 [3] Amtoft, T., Turbak, F.: Faithful translations between polyvariant flows and
     polymorphic types. In: European Symposium on Programming (ESOP). pp.
     26–40. Springer (2000). https://doi.org/10.1007/3-540-46425-5 2
 [4] Bakst, A., Jhala, R.: Predicate abstraction for linked data struc-
     tures. In: Conference on Verification, Model Checking, and Abstract In-
     terpretation (VMCAI). pp. 65–84. Springer Berlin Heidelberg (2016).
     https://doi.org/10.1007/978-3-662-49122-5 3
 [5] Ball, T., Levin, V., Rajamani, S.K.: A decade of software model check-
     ing with SLAM. Communications of the ACM 54(7), 68–76 (2011).
     https://doi.org/10.1145/1965724.1965743
 [6] Banerjee, A.: A modular, polyvariant and type-based closure analysis. In:
     International Conference on Functional Programming (ICFP). pp. 1–10
     (1997). https://doi.org/10.1145/258948.258951
 [7] Barnett, M., Fähndrich, M., Leino, K.R.M., Müller, P., Schulte, W., Venter,
     H.: Specification and verification: the Spec# experience. Communications
     of the ACM 54(6), 81–91 (2011). https://doi.org/10.1145/1953122.1953145
 [8] Barrett, C., Fontaine, P., Tinelli, C.: The Satisfiability Modulo Theories
     Library (SMT-LIB). www.SMT-LIB.org (2016)
 [9] Bengtson, J., Bhargavan, K., Fournet, C., Gordon, A.D., Maffeis, S.: Re-
     finement types for secure implementations. ACM Transactions on Pro-
     gramming Languages and Systems (TOPLAS) 33(2), 8:1–8:45 (2011).
     https://doi.org/10.1145/1890028.1890031
[10] Bhargavan, K., Bond, B., Delignat-Lavaud, A., Fournet, C., Hawblitzel,
     C., Hriţcu, C., Ishtiaq, S., Kohlweiss, M., Leino, R., Lorch, J., Mail-
     lard, K., Pan, J., Parno, B., Protzenko, J., Ramananandro, T., Rane, A.,
     Rastogi, A., Swamy, N., Thompson, L., Wang, P., Zanella-Béguelin, S.,
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types          27

     Zinzindohoué, J.K.: Everest: Towards a verified, drop-in replacement of
     HTTPS. In: Summit on Advances in Programming Languages (SNAPL
     2017). pp. 1:1–1:12. Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik (2017).
     https://doi.org/10.4230/LIPIcs.SNAPL.2017.1
[11] Bornat, R., Calcagno, C., O’Hearn, P.W., Parkinson, M.J.: Per-
     mission accounting in separation logic. In: Symposium on Prin-
     ciples of Programming Languages (POPL). pp. 259–270 (2005).
     https://doi.org/10.1145/1040305.1040327
[12] Boyland, J.: Checking interference with fractional permissions. In:
     Symposion on Static Analysis (SAS). pp. 55–72. Springer (2003).
     https://doi.org/10.1007/3-540-44898-5 4
[13] Champion, A., Kobayashi, N., Sato, R.: HoIce: An ICE-based non-linear Horn
     clause solver. In: Asian Symposium on Programming Languages and Systems
     (APLAS). pp. 146–156. Springer (2018). https://doi.org/10.1007/978-3-030-
     02768-1 8
[14] Chugh, R., Herman, D., Jhala, R.: Dependent types for JavaScript. In: Confer-
     ence on Object Oriented Programming Systems Languages and Applications
     (OOPSLA). pp. 587–606 (2012). https://doi.org/10.1145/2384616.2384659
[15] Cousot, P., Cousot, R., Feret, J., Mauborgne, L., Miné, A., Monniaux, D.,
     Rival, X.: The ASTRÉE analyzer. In: European Symposium on Programming
     (ESOP). pp. 21–30. Springer (2005). https://doi.org/10.1007/978-3-540-
     31987-0 3
[16] De Moura, L., Bjørner, N.: Z3: An efficient SMT solver. In: Conference on
     Tools and Algorithms for the Construction and Analysis of Systems (TACAS).
     pp. 337–340. Springer (2008). https://doi.org/10.1007/978-3-540-78800-3 24
[17] Degen, M., Thiemann, P., Wehr, S.: Tracking linear and affine resources
     with JAVA(X). In: European Conference on Object-Oriented Programming
     (ECOOP). pp. 550–574. Springer (2007). https://doi.org/10.1007/978-3-540-
     73589-2 26
[18] DeLine, R., Fähndrich, M.: Enforcing high-level protocols in low-level soft-
     ware. In: Conference on Programming Language Design and Implementation
     (PLDI). pp. 59–69 (2001). https://doi.org/10.1145/378795.378811
[19] Fähndrich, M., DeLine, R.: Adoption and focus: Practical linear
     types for imperative programming. In: Conference on Programming
     Language Design and Implementation (PLDI). pp. 13–24 (2002).
     https://doi.org/10.1145/512529.512532
[20] Fink, S.J., Yahav, E., Dor, N., Ramalingam, G., Geay, E.: Effective type-
     state verification in the presence of aliasing. ACM Transactions on Soft-
     ware Engineering and Methodology (TOSEM) 17(2), 9:1–9:34 (2008).
     https://doi.org/10.1145/1348250.1348255
[21] Flanagan, C.: Hybrid type checking. In: Symposium on Prin-
     ciples of Programming Languages (POPL). pp. 245–256 (2006).
     https://doi.org/10.1145/1111037.1111059
[22] Flanagan, C., Leino, K.R.M., Lillibridge, M., Nelson, G., Saxe, J.B.,
     Stata, R.: Extended static checking for Java. In: Conference on Program-
28      J. Toman et al.

     ming Language Design and Implementation (PLDI). pp. 234–245 (2002).
     https://doi.org/10.1145/512529.512558
[23] Foster, J.S., Terauchi, T., Aiken, A.: Flow-sensitive type qualifiers. In:
     Conference on Programming Language Design and Implementation (PLDI).
     pp. 1–12 (2002). https://doi.org/10.1145/512529.512531
[24] Freeman, T., Pfenning, F.: Refinement types for ML. In: Conference on
     Programming Language Design and Implementation (PLDI). pp. 268–277
     (1991). https://doi.org/10.1145/113445.113468
[25] Gilray, T., Might, M.: A survey of polyvariance in abstract interpretations.
     In: Symposium on Trends in Functional Programming. pp. 134–148. Springer
     (2013). https://doi.org/10.1007/978-3-642-45340-3 9
[26] Gordon, C.S., Ernst, M.D., Grossman, D.: Rely–guarantee references for
     refinement types over aliased mutable data. In: Conference on Program-
     ming Language Design and Implementation (PLDI). pp. 73–84 (2013).
     https://doi.org/10.1145/2491956.2462160
[27] Gordon, C.S., Ernst, M.D., Grossman, D., Parkinson, M.J.: Verifying invari-
     ants of lock-free data structures with rely–guarantee and refinement types.
     ACM Transactions on Programming Languages and Systems (TOPLAS)
     39(3), 11:1–11:54 (2017). https://doi.org/10.1145/3064850
[28] Hardekopf, B., Wiedermann, B., Churchill, B., Kashyap, V.: Widening for
     control-flow. In: Conference on Verification, Model Checking, and Abstract
     Interpretation (VMCAI). pp. 472–491 (2014). https://doi.org/10.1007/978-
     3-642-54013-4 26
[29] Hawblitzel, C., Howell, J., Kapritsos, M., Lorch, J.R., Parno, B., Roberts,
     M.L., Setty, S., Zill, B.: IronFleet: proving practical distributed systems
     correct. In: Symposium on Operating Systems Principles (SOSP). pp. 1–17.
     ACM (2015). https://doi.org/10.1145/2815400.2815428
[30] Heule, S., Kassios, I.T., Müller, P., Summers, A.J.: Verification condition gen-
     eration for permission logics with abstract predicates and abstraction func-
     tions. In: European Conference on Object-Oriented Programming (ECOOP).
     pp. 451–476. Springer (2013). https://doi.org/10.1007/978-3-642-39038-8 19
[31] Heule, S., Leino, K.R.M., Müller, P., Summers, A.J.: Abstract read per-
     missions: Fractional permissions without the fractions. In: Conference on
     Verification, Model Checking, and Abstract Interpretation (VMCAI). pp.
     315–334 (2013). https://doi.org/10.1007/978-3-642-35873-9 20
[32] Kahsai, T., Kersten, R., Rümmer, P., Schäf, M.: Quantified heap invariants
     for object-oriented programs. In: Conference on Logic for Programming
     Artificial Intelligence and Reasoning (LPAR). pp. 368–384 (2017)
[33] Kahsai, T., Rümmer, P., Sanchez, H., Schäf, M.: JayHorn: A framework for
     verifying Java programs. In: Conference on Computer Aided Verification
     (CAV). pp. 352–358. Springer (2016). https://doi.org/10.1007/978-3-319-
     41528-4 19
[34] Kashyap, V., Dewey, K., Kuefner, E.A., Wagner, J., Gibbons, K., Sarracino,
     J., Wiedermann, B., Hardekopf, B.: JSAI: a static analysis platform for
     JavaScript. In: Conference on Foundations of Software Engineering (FSE).
     pp. 121–132 (2014). https://doi.org/10.1145/2635868.2635904
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types           29

[35] Kawaguchi, M., Rondon, P., Jhala, R.: Type-based data structure verification.
     In: Conference on Programming Language Design and Implementation
     (PLDI). pp. 304–315 (2009). https://doi.org/10.1145/1542476.1542510
[36] Kloos, J., Majumdar, R., Vafeiadis, V.: Asynchronous liquid separation
     types. In: European Conference on Object-Oriented Programming (ECOOP).
     pp. 396–420. Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik (2015).
     https://doi.org/10.4230/LIPIcs.ECOOP.2015.396
[37] Komuravelli, A., Gurfinkel, A., Chaki, S., Clarke, E.M.: Automatic ab-
     straction in SMT-based unbounded software model checking. In: Confer-
     ence on Computer Aided Verification (CAV). pp. 846–862. Springer (2013).
     https://doi.org/10.1007/978-3-642-39799-8 59
[38] Leino, K.R.M.: Dafny: An automatic program verifier for functional correct-
     ness. In: Conference on Logic for Programming Artificial Intelligence and Rea-
     soning (LPAR). pp. 348–370. Springer (2010). https://doi.org/10.1007/978-
     3-642-17511-4 20
[39] Leino, K.R.M., Müller, P., Smans, J.: Deadlock-free channels and locks. In:
     European Symposium on Programming (ESOP). pp. 407–426. Springer-
     Verlag (2010). https://doi.org/10.1007/978-3-642-11957-6 22
[40] Matsushita, Y., Tsukada, T., Kobayashi, N.: RustHorn: CHC-based verifica-
     tion for Rust programs. In: European Symposium on Programming (ESOP).
     Springer (2020)
[41] Milanova, A., Rountev, A., Ryder, B.G.: Parameterized object sen-
     sitivity for points-to analysis for Java. ACM Transactions on Soft-
     ware Engineering and Methodology (TOSEM) 14(1), 1–41 (2005).
     https://doi.org/10.1145/1044834.1044835
[42] Müller, P., Schwerhoff, M., Summers, A.J.: Viper: A verification infrastruc-
     ture for permission-based reasoning. In: Conference on Verification, Model
     Checking, and Abstract Interpretation (VMCAI). pp. 41–62. Springer-Verlag
     (2016). https://doi.org/10.1007/978-3-662-49122-5 2
[43] Pierce, B.C.: Types and programming languages. MIT press (2002)
[44] Protzenko, J., Zinzindohoué, J.K., Rastogi, A., Ramananandro, T., Wang,
     P., Zanella-Béguelin, S., Delignat-Lavaud, A., Hriţcu, C., Bhargavan, K.,
     Fournet, C., Swamy, N.: Verified low-level programming embedded in F*.
     Proceedings of the ACM on Programming Languages 1(ICFP), 17:1–17:29
     (2017). https://doi.org/10.1145/3110261
[45] Reynolds, J.C.: Separation logic: A logic for shared mutable data structures.
     In: Symposium on Logic in Computer Science (LICS). pp. 55–74. IEEE
     (2002). https://doi.org/10.1109/LICS.2002.1029817
[46] Rondon, P., Kawaguchi, M., Jhala, R.: Low-level liquid types. In: Symposium
     on Principles of Programming Languages (POPL). pp. 131–144 (2010).
     https://doi.org/10.1145/1706299.1706316
[47] Rondon, P.M., Kawaguci, M., Jhala, R.: Liquid types. In: Conference on
     Programming Language Design and Implementation (PLDI). pp. 159–169
     (2008). https://doi.org/10.1145/1375581.1375602
[48] Rümmer, P., Hojjat, H., Kuncak, V.: Disjunctive interpolants for Horn-
     clause verification. In: Conference on Computer Aided Verification (CAV).
     pp. 347–363. Springer (2013). https://doi.org/10.1007/978-3-642-39799-8 24
30     J. Toman et al.

[49] Sharir, M., Pnueli, A.: Two approaches to interprocedural data flow analysis.
     In: Muchnick, S.S., Jones, N.D. (eds.) Program Flow Analysis: Theory and
     Applications, chap. 7, pp. 189–223. Prentice Hall (1981)
[50] Shivers, O.: Control-flow analysis of higher-order languages. Ph.D. thesis,
     Carnegie Mellon University (1991)
[51] Smaragdakis, Y., Bravenboer, M., Lhoták, O.: Pick your con-
     texts well: Understanding object-sensitivity. In: Symposium on
     Principles of Programming Languages (POPL). pp. 17–30 (2011).
     https://doi.org/10.1145/1926385.1926390
[52] Smith, F., Walker, D., Morrisett, G.: Alias types. In: European
     Symposium on Programming (ESOP). pp. 366–381. Springer (2000).
     https://doi.org/10.1007/3-540-46425-5 24
[53] Späth, J., Ali, K., Bodden, E.: Context-, flow-, and field-sensitive
     data-flow analysis using synchronized pushdown systems. Proceedings
     of the ACM on Programming Languages 3(POPL), 48:1–48:29 (2019).
     https://doi.org/10.1145/3290361
[54] Späth, J., Nguyen Quang Do, L., Ali, K., Bodden, E.: Boomerang:
     Demand-driven flow-and context-sensitive pointer analysis for Java. In:
     European Conference on Object-Oriented Programming (ECOOP). pp.
     22:1–22:26. Schloss Dagstuhl-Leibniz-Zentrum fuer Informatik (2016).
     https://doi.org/10.4230/LIPIcs.ECOOP.2016.22
[55] Suenaga, K., Fukuda, R., Igarashi, A.: Type-based safe resource dealloca-
     tion for shared-memory concurrency. In: Conference on Object Oriented
     Programming Systems Languages and Applications (OOPSLA). pp. 1–20
     (2012). https://doi.org/10.1145/2384616.2384618
[56] Suenaga, K., Kobayashi, N.: Fractional ownerships for safe memory deal-
     location. In: Asian Symposium on Programming Languages and Systems
     (APLAS). pp. 128–143. Springer (2009). https://doi.org/10.1007/978-3-642-
     10672-9 11
[57] Swamy, N., Hriţcu, C., Keller, C., Rastogi, A., Delignat-Lavaud, A., Forest,
     S., Bhargavan, K., Fournet, C., Strub, P.Y., Kohlweiss, M., Zinzindohoué,
     J.K., Zanella-Béguelin, S.: Dependent types and multi-monadic effects in
     F*. In: Symposium on Principles of Programming Languages (POPL). pp.
     256–270 (2016). https://doi.org/10.1145/2837614.2837655
[58] Swamy, N., Weinberger, J., Schlesinger, C., Chen, J., Livshits, B.: Verifying
     higher-order programs with the Dijkstra monad. In: Conference on Program-
     ming Language Design and Implementation (PLDI). pp. 387–398 (2013).
     https://doi.org/10.1145/2491956.2491978
[59] Terauchi, T.: Checking race freedom via linear programming. In: Conference
     on Programming Language Design and Implementation (PLDI). pp. 1–10
     (2008). https://doi.org/10.1145/1375581.1375583
[60] Unno, H., Kobayashi, N.: Dependent type inference with interpolants. In:
     Conference on Principles and Practice of Declarative Programming (PPDP).
     pp. 277–288. ACM (2009). https://doi.org/10.1145/1599410.1599445
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                  31

[61] Vazou, N., Rondon, P.M., Jhala, R.: Abstract refinement types. In: Euro-
     pean Symposium on Programming (ESOP). pp. 209–228. Springer (2013).
     https://doi.org/10.1007/978-3-642-37036-6 13
[62] Vazou, N., Seidel, E.L., Jhala, R., Vytiniotis, D., Peyton-Jones, S.: Refine-
     ment types for Haskell. In: International Conference on Functional Program-
     ming (ICFP). pp. 269–282 (2014). https://doi.org/10.1145/2628136.2628161
[63] Wells, J.B., Dimock, A., Muller, R., Turbak, F.: A calculus with polymorphic
     and polyvariant flow types. Journal of Functional Programming 12(3), 183–
     227 (2002). https://doi.org/10.1017/S0956796801004245
[64] Xi, H., Pfenning, F.: Dependent types in practical programming. In: Sympo-
     sium on Principles of Programming Languages (POPL). pp. 214–227. ACM
     (1999). https://doi.org/10.1145/292540.292560
[65] Zave, P.: Using lightweight modeling to understand Chord. ACM
     SIGCOMM Computer Communication Review 42(2), 49–57 (2012).
     https://doi.org/10.1145/2185376.2185383
[66] Zhu, H., Jagannathan, S.: Compositional and lightweight dependent
     type inference for ML. In: Conference on Verification, Model Check-
     ing, and Abstract Interpretation (VMCAI). pp. 295–314. Springer (2013).
     https://doi.org/10.1007/978-3-642-35873-9 19




Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium or
format, as long as you give appropriate credit to the original author(s) and the source,
provide a link to the Creative Commons license and indicate if changes were made.
    The images or other third party material in this chapter are included in the chapter’s
Creative Commons license, unless indicated otherwise in a credit line to the material. If
material is not included in the chapter’s Creative Commons license and your intended
use is not permitted by statutory regulation or exceeds the permitted use, you will need
to obtain permission directly from the copyright holder.
32      J. Toman et al.



      Θ | [] : τ ⇒ Γ | L ⊢ectx E : τ ′ ⇒ Γ ′       Θ | L | Γ ′ ⊢ e : τ ′′ ⇒ Γ ′′
                                                                                     (TE-Seq)
                    Θ | [] : τ ⇒ Γ | L ⊢ectx E ; e : τ ′′ ⇒ Γ ′′

                                                                                   (TE-Hole)
                       Θ | [] : τ ⇒ Γ | L ⊢ectx [] : τ ⇒ Γ

                    Θ | [] : τ ′ ⇒ Γ ′ | L ⊢ectx E : τ ′′ ⇒ Γ ′′
                         Θ | L | Γ, x : τ ⊢ e : τ ′ ⇒ Γ ′
                                  x ̸∈ dom(Γ ′ )
                                                                                   (TE-Stack)
            Θ | [] : τ ⇒ Γ | L ⊢ectx E [let x = []ℓ in e] : τ ′′ ⇒ Γ ′′


                                     (E ; e)[e ′ ] = E [e ′ ] ; e
                                           [][e ′ ] = e′
                         E [let y = []ℓ in e][x ] = E [let y = x in e]


                        Fig. 11. Context typing and substitution




A     Proof of Type Soundness (Theorem 1)
                                                                 D            E
We first define a typing relation for machine configurations H , R, F⃗ , e as shown
in Figure 12. The critical component of this typing relation is the consistency
relation Cons. Intuitively, Cons expresses that the current heap and registers are
consistent with the ownership and refinement information implied by Γ . We say
triple (H , R, Γ ) is consistent, and write Cons (H , R, Γ ). In the definitions for own
we write {a 7→ r} to denote a function Addr → Q≥0 which returns r for a, and 0
otherwise. We write ∅ to denote a constant function Addr → Q≥0 which always
returns 0. We define the addition between two functions O1 , O2 : Addr → Q≥0
as: (O1 + O2 )(a) = O1 (a) + O2 (a). Individual ownership annotations remain
rationals in [0, 1], but an intermediate pointwise sum need not itself lie in [0, 1];
the final inequality in Cons is what bounds the total live ownership. Finally, if a
summation Σ has no summands, we take its result to be ∅.
    The proof of Theorem 1 requires the following four key lemmas. These lemmas
are stated with respect to some well-typed program ⟨D, e⟩, i.e. ⊢ ⟨D, e⟩.
Lemma 1. ⊢D
          conf ⟨∅, ∅, ·, e⟩

Proof. Trivial, taking Γ = • and by inversion on ⊢ ⟨D, e⟩.

Lemma 2. ⊢D
          conf C implies C ̸= AssertFail

Proof. Simple proof by contradiction, as the AssertFail is not well-typed.
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                      33




⃗
ℓ = Trace (F⃗)      n = |⃗
                         ℓ| = |F ⃗|       Θ⊢D       ∀j ∈ {1..n} .⃗
                                                                 ℓj = tailn−j+1 (⃗
                                                                                 ℓ)
   Cons (H , R, Γ )                                    ⃗
                       ∀i ∈ {1..n} .Θ | [] : τi ⇒ Γi | ℓi ⊢ectx Fi : τi−1 ⇒ Γi−1
                ⃗ = Fn : · · · : F1 : ·
                F                          Θ|⃗ ℓ | Γ ⊢ e : τn ⇒ Γ n
                                        D          E
                                  D           ⃗
                                ⊢conf H , R, F , e

                               ⊢D
                                conf AliasFail




                                              Trace (·) = ϵ
                                          ℓ       ⃗ ) = ℓ : Trace (F
                     Trace (E [let x = [] in e] : F                ⃗)



                     def
  Cons (H , R, Γ ) ⇐⇒ SAT (H , R, Γ ) ∧ ∀ a ∈ dom(H ).Own (H , R, Γ )(a) ≤ 1
                     def
  SAT (H , R, Γ ) ⇐⇒ ∀ x ∈ dom(Γ ).x ∈ dom(R) ∧ SATv(H , R, R(x ), Γ (x ))
                        (
                    def   v ∈ Z ∧ [R] [v/ν]φ                   τ = {ν : int | φ}
SATv(H , R, v, τ ) ⇐⇒
                          a ∈ dom(H ) ∧ SATv(H , R, H (a), τ ) τ = τ ′ ref r ∧v = a
                                                            ′


              [∅] φ = φ
    [R{y 7→ n}] φ = [R] [n/y]φ
    [R{y 7→ a}] φ = [R] φ
  Own (H , R, Γ ) = Σx ∈dom(Γ ) own (H , R(x ), Γ (x ))
                      (
                        {a 7→ r} + own (H , H (a), τ ′ )      v = a ∧ a ∈ dom(H ) ∧ τ = τ ′ ref r
   own (H , v , τ ) =
                        ∅                                     o.w.




                             Fig. 12. Machine state typing
34       J. Toman et al.
                      D             E   D             E
Lemma 3. If ⊢D
             conf      H , R, F⃗ , e and H , R, F⃗ , e −→D C, then ⊢D
                                                                    conf C


Lemma 4. If ⊢D
             conf C, then, one of the following conditions hold:

 1. ∃C′ , C −→D C′ , or
 2. C = AliasFail, or
 3. C = ⟨H , R, ·, x ⟩

Lemmas 3 and 4 are the heart of proof effort, we give their proofs in Sections C
and D respectively.
   We can now prove Theorem 1:
Proof (Theorem 1: Soundness). From Lemmas 1 and 3 and an inductive argument,
any configuration reachable from the initial state must be well-typed. Then,
by Lemma 2 every configuration reachable from the initial state cannot be
AssertFail, i.e., a well-typed program never experiences an assertion failure.
This completes the first part of the proof.
   To prove the second portion of the theorem, it suffices to show that any
configuration reachable from the initial state can step or is a final configuration.
Again from Lemmas 1 and 3 and a simple inductive argument, we must have
that for any state C such that ⟨∅, ∅, ·, e⟩ −→∗D C ⊢D
                                                    conf C. Then by Lemma 4 we
have the configuration may step or is one of the final configurations.
   The remainder of this appendix proves Lemmas 3 and 4. We introduce some
auxiliary definitions and lemmas in Section B, give the proof of Lemma 3 in
Section C, and prove Lemma 4 in Section D.


B    Auxiliary Lemmas and Definitions

The well-formedness rules omitted from the main paper are found in Figure 13.
We write L ⊢WF τ ⇒ Γ as shorthand for L ⊢WF Γ and L | Γ ⊢WF τ .
   We first prove that the subtyping relations are transitive.

Lemma 5.

 1. If Γ ≤ Γ ′ then |= JΓ K =⇒ JΓ ′ K.
 2. If Γ ⊢ τ1 ≤ τ2 and Γ ⊢ τ2 ≤ τ3 , then Γ ⊢ τ1 ≤ τ3
 3. If Γ ≤ Γ ′ and Γ ′ ⊢ τ1 ≤ τ2 , then Γ ⊢ τ1 ≤ τ2
 4. If Γ ≤ Γ ′ , Γ ⊢ τ1 ≤ τ2 , and Γ ′ ⊢ τ2 ≤ τ3 , then Γ ⊢ τ1 ≤ τ3 .
 5. If Γ ≤ Γ ′ and Γ ′ ≤ Γ ′′ , then Γ ≤ Γ ′′ .

Proof.

 1. It suffices to show that |= JΓ K =⇒ [x / ν ] φ′ for any x ∈ dom(Γ ′ ) where
    Γ ′ (x ) = {ν : int | φ′ }. From Γ ≤ Γ ′ we have |= JΓ K∧φ =⇒ φ′ where Γ (x ) =
    {ν : int | φ}. We must then have |= JΓ K ∧ [x / ν ] φ =⇒ [x / ν ] φ′ . From the
    definition of JΓ K we have JΓ K ∧ [x / ν ] φ ⇐⇒ JΓ K, giving the desired result.
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                                     35


          ∀ x ∈ dom(Γ ).L | Γ ⊢WF Γ (x )                   L | Γ ⊢WF φ                 L | Γ ⊢WF τ
                   L ⊢WF Γ                            L | Γ ⊢WF {ν : int | φ}        L | Γ ⊢WF τ ref r
                              (WF-Env)                             (WF-Int)                 (WF-Ref)

              ∀ x ∈ FPV (φ) \ {ν} .Γ (x ) = {ν : int | }
                                                                        L | Γ ⊢WF τ    L ⊢WF Γ
                       FCV (φ) ⊆ CV (L)
                                                                              L ⊢WF τ ⇒ Γ
                          L | Γ ⊢WF φ
                                                                                    (WF-Result)
                                              (WF-Phi)

                         λ ⊢WF x1 : τ1 , . . . , xn : τn
                                                                                ∀ f ∈ dom(Θ). ⊢WF Θ(f )
                       λ ⊢WF τ ⇒ x1 : τ1′ , . . . , xn : τn′
                                                                                        ⊢WF Θ
       ⊢WF ∀λ. ⟨x1 : τ1 , . . . , xn : τn ⟩ → x1 : τ1′ , . . . , xn : τn′ | τ
                                                                                          (WF-FunEnv)
                                                         (WF-FunType)


                                Simple Types              τS ::= int | τS ref
                                Erasure      L{ν : int | φ}M = int
                                                    Lτ ref r M = Lτ M ref
                      Free Ctxt Vars FCV (φ1 ∨ φ2 ) = FCV (φ1 ) ∪ FCV (φ2 )
                                         FCV (¬φ) = FCV (φ)
                                     FCV (b
                                          v1 = vb2 ) = FCV (ϕ(b         bn )) = ∅
                                                              v1 , .. , v
                                       FCV (⃗ℓ ⪯ C) = FCV (C)
                                        FCV (ℓ : C) = FCV (C)
                                          FCV (L) = CV (L)
                           Ctxt Vars        CV (⃗ℓ) = ∅
                                            CV (λ) = {λ}


                    Fig. 13. Well-formedness of types and environments.


 2. By induction on Γ ⊢ τ1 ≤ τ2 . We only consider the base case where τ1 =
    {ν : int | φ1 } and τ2 = {ν : int | φ2 }, the case for reference types follows from
    the induction hypothesis. By further inversion on Γ ⊢ τ2 ≤ τ3 we therefore
    have:
      τ3 = {ν : int | φ3 }
      |= JΓ K ∧ φ1 =⇒ φ2           |= JΓ K ∧ φ2 =⇒ φ3
    From which it is immediate that we must have |= JΓ K ∧ φ1 =⇒ φ3 , whereby
    S-Int gives Γ ⊢ τ1 ≤ τ3 .
 3. By induction on Γ ′ ⊢ τ1 ≤ τ2 . The case for reference types is immediate from
    the inductive hypothesis, we focus on the base case where τ1 = {ν : int | φ1 }
    and τ2 = {ν : int | φ2 }, and where |= JΓ ′ K ∧ φ1 =⇒ φ2 . From Γ ≤ Γ ′
    and Item 1 above, we have |= JΓ K =⇒ JΓ ′ K from which we can derive
    JΓ K ∧ φ1 =⇒ φ2 , i.e., Γ ⊢ τ1 ≤ τ2 .
 4. Immediate from Items 2 and 3.
 5. Immediate corollary of Item 4.
Definition 1. A value v reaches an integer with n dereferences in heap H when
it is in the relation H ⊢ v ⇓ n defined as the smallest relation closed under the
following rules:
 1. If v ∈ Z then H ⊢ v ⇓ 0
 2. If H ⊢ v ⇓ n and H (a) = v then H ⊢ a ⇓ n + 1
We will write H ⊢ v ⇓ |τ | to indicate a value v is shape consistent with τ in heap
H , where |τ | is the number of reference constructors in the type τ .
36       J. Toman et al.

   It is straightforward to show that n is uniquely determined by H and v .
   We also prove a standard inversion lemma to handle the fact our typing rules
are not syntax directed.

Lemma 6 (Inversion). If Θ | L | Γ ⊢ e0 : τ ⇒ Γ ′ , then there exists some Γp ,
τp , and Γp′ such that Γ ≤ Γp , L ⊢WF Γp , Γp′ , τp ≤ Γ ′ , τ , and:
 1. If e0 = x then Γp (x ) = τp + τ ′ , Γp′ = Γp [x ←- τ ′ ].
 2. If e0 = let x = y in e, then Θ | L | Γp [y ←- τ1 ∧y y =τ1 x ], x : (τ2 ∧x x =τ2
    y) ⊢ e : τp ⇒ Γp′ and x ̸∈ dom(Γp′ ) where Γp (y) = τ1 + τ2 .
 3. If e0 = let x = n in e then Θ | L | Γp , x : {ν : int | ν = n} ⊢ e : τp ⇒ Γp′ and
    x ̸∈ dom(Γp′ ).
 4. If e0 = ifz x then e1 else e2 then:
      – Γp (x ) = {ν : int | φ}
      – Θ | L | Γp [x ←- {ν : int | φ ∧ ν = 0}] ⊢ e1 : τp ⇒ Γp′
      – Θ | L | Γp [x ←- {ν : int | φ ∧ ν ̸= 0}] ⊢ e2 : τp ⇒ Γp′
 5. If e0 = let x = mkref y in e, then Γp (y) = τ1 + τ2 , Θ | L | Γp [y ←- τ1 ], x :
    (τ2 ∧x x =τ2 y) ref 1 ⊢ e : τp ⇒ Γp′ , and x ̸∈ dom(Γp′ )
 6. If e0 = let x = ∗y in e, then:
      – Γp (y) = τ1 + τ2 ref r
      – Θ | L | Γp [y ←- τ ′′ ref r ], x : τ2 ⊢ e : τp ⇒ Γp′
      – x ̸∈ dom(Γp′ )
      –                                  (
                                            (τ1 ∧y y =τ1 x ) r > 0
                                τ ′′ =
                                            τ1                r=0
 7. If e0 = let x = f ℓ (y1 , . . . , yn ) in e then:
      – Γp (yi ) = σα σx τi for each i ∈ {1, . . . , n}
      – Θ | L | Γp [yi ←- σα σx τi′ ], x : σα σx τ ⊢ e : τp ⇒ Γp′
      – Θ(f ) = ∀λ. ⟨x1 : τ1 , . . . , xn : τn ⟩ → ⟨x1 : τ1′ , . . . , xn : τn′ | τ ⟩
      – σα = [ℓ : L/λ]
      – σx = [y1 /x1 ] · · · [yn /xn ]
      – x ̸∈ dom(Γp′ )
 8. If e0 = y : = x ; e then:
      – x ̸= y
      – Γp (x ) = τ1 + τ2
      – Γp (y) = τ ′ ref 1
      – Θ | L | Γp [x ←- τ1 ][y ←- (τ2 ∧y y =τ2 x ) ref 1 ] ⊢ e : τp ⇒ Γp′
      – The shapes of τ ′ and τ2 are similar, i.e, Lτ ′ M = Lτ2 M.
 9. If e0 = alias(x = y) ; e then there exist some τ1 , τ2 , τ1′ , τ2′ , r1 , r2 , r1′ , r2′ such
    that:
      – x ̸= y
                                             ′           ′
      – τ1 ref r1 +τ2 ref r2 ≈ τ1′ ref r1 +τ2′ ref r2
      – Γp (x ) = τ1 ref r1 and Γp (y) = τ2 ref r2
                                       ′               ′
      – Θ | L | Γp [x ←- τ1′ ref r1 ][y ←- τ2′ ref r2 ] ⊢ e : τp ⇒ Γp′
10. If e0 = alias(x = ∗y) ; e then there exist some τ1 , τ2 , τ1′ , τ2′ , r1 , r2 , r1′ , r2′ , r,
    such that:
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                 37

                                        ′         ′
      – τ1 ref r1 +τ2 ref r2 ≈ τ1′ ref r1 +τ2′ ref r2
      – Γp (x ) = τ1 ref r1 and Γp (y) = (τ2 ref r2 ) ref r
                                   ′                 ′
      – Θ | L | Γp [x ←- τ1′ ref r1 ][y ←- (τ2′ ref r2 ) ref r ] ⊢ e : τp ⇒ Γp′
11. If e0 = e1 ; e2 then Θ | L | Γp ⊢ e1 : τ1 ⇒ Γ1 and Θ | L | Γ1 ⊢ e2 : τp ⇒ Γp′
12. If e0 = x ; e ′ then Θ | L | Γp [x : τ ′ + τ0 ] ⊢ x : τ1 ⇒ Γp [x ←- τ0 ] and
    Θ | L | Γp [x ←- τ0 ] ⊢ e ′ : τp ⇒ Γp′
13. If e0 = assert(φ) ; e then Γp |= φ and Θ | L | Γp ⊢ e : τp ⇒ Γp′

Proof. By straightforward induction on the typing relation and the transitivity
of the subtyping relation Lemma 5.
    The only case of note is the case for e0 = x ; e2 . If the subderivation for x
has applications of T-Sub then the subtypings on the output environment can
be pushed into application subtyping on input environments when typing e ′ .
Similarly, any input subtypings on the input environment of the derivation of x
can be pushed into T-Sub rules such that Γ ≤ Γp [x : τ ′ + τ0 ].

   Lemmas 7 and 8 prove some standard properties of execution contexts: any
decomposition of a well-typed expression into a execution context and redex can
be well-typed, and substituting a well-typed expression matching a context’s hole
type yields a well-typed expression

Lemma 7. For any E and e ′ such that E [e ′ ] = e where Θ | L | Γ ⊢ e : τ ⇒ Γ ′
there exists some τ0 , Γ0 such that Θ | [] : τ0 ⇒ Γ0 | L ⊢ectx E : τ ⇒ Γ ′ and
Θ | L | Γ ⊢ e ′ : τ0 ⇒ Γ0 .

Proof. By induction on the structure of E .
Case E = []:
Trivial, by taking τ0 = τ and Γ0 = Γ ′ .
Case E = E ′ ; e ′′ :
Then E [e ′ ] = E ′ [e ′ ] ; e ′′ = e. By Lemma 6 we have

           Θ | L | Γp ⊢ E ′ [e ′ ] : τ1 ⇒ Γ1   Θ | L | Γ1 ⊢ e ′′ : τp ⇒ Γp′
           Γ ≤ Γp                              Γp′ , τp ≤ Γ ′ , τ

for some Γp , Γp′ , and τp .
    By the induction hypothesis we then have Θ | L | Γp ⊢ e ′ : τ0 ⇒ Γ0 and
Θ | [] : τ0 ⇒ Γ0 | L ⊢ectx E ′ : τ1 ⇒ Γ1 . for some τ0 and Γ0 .
    Next, as Γp′ , τp ≤ Γ ′ , τ by an application of T-Sub, we have Θ | L | Γ1 ⊢ e ′′ :
τ ⇒ Γ ′ . By TE-Seq, we therefore have: Θ | [] : τ0 ⇒ Γ0 | L ⊢ectx E ′ ; e ′′ : τ ⇒ Γ ′ .
    Finally, from Γ ≤ Γp and Θ | L | Γp ⊢ e ′ : τ0 ⇒ Γ0 , and application of T-Sub,
we have Θ | L | Γ ⊢ e ′ : τ0 ⇒ Γ0 .

Lemma 8. If Θ | [] : τ ⇒ Γ ′ | L ⊢ectx E : τ ′′ ⇒ Γ ′′ and Θ | L | Γ ⊢ e : τ ⇒ Γ ′
for some Γ , then Θ | L | Γ ⊢ E [e] : τ ′′ ⇒ Γ ′′ .

Proof. By induction on the typing derivation of E .
38       J. Toman et al.

Case TE-Seq:         E = E ′ ; e′
                     E [e] = E ′ [e] ; e ′
                     Θ | [] : τ ⇒ Γ ′ | L ⊢ectx E ′ : τ0 ⇒ Γ0
                     Θ | L | Γ0 ⊢ e ′ : τ ′′ ⇒ Γ ′′
By the induction hypothesis we have Θ | L | Γ ⊢ E ′ [e] : τ0 ⇒ Γ0 . We then have
our result via an application of T-Seq.
Case TE-Hole:
Trivial, as τ = τ ′′ and Γ ′ = Γ ′′ and E [e] = e.

Lemma 9 (Context Variable Substitution).

 1. If τ3 = τ1 + τ2 then [L/λ] τ3 = [L/λ] τ1 + [L/λ] τ2
 2. For any ⃗ℓ:
    (a) If λ ⊢WF Γ then ⃗ℓ ⊢WF [⃗ℓ/λ]Γ
    (b) If λ | Γ ⊢WF τ then ⃗ℓ | [⃗ℓ/λ]Γ ⊢WF [⃗ℓ/λ] τ
    (c) If λ ⊢WF τ ⇒ Γ then ⃗ℓ ⊢WF [⃗ℓ/λ] τ ⇒[⃗ℓ/λ]Γ
 3. For any Γ , τ1 , τ2 , λ and ⃗ℓ, If Γ ⊢ τ1 ≤ τ2 , then [⃗ℓ/λ]Γ ⊢ [⃗ℓ/λ] τ1 ≤ [⃗ℓ/λ] τ2
 4. If Γ |= φ where λ ̸∈ FCV (φ) then [⃗ℓ/λ]Γ |= φ
 5. If Θ | λ | Γ ⊢ e : τ ⇒ Γ ′ then Θ | ⃗ℓ | [⃗ℓ/λ]Γ ⊢ e : [⃗ℓ/λ] τ ⇒[⃗ℓ/λ]Γ ′

Proof.

 1. By straightforward induction on the definition of τ1 + τ2 = τ3 .
 2. Observe that any substitution of context variables cannot change simple
    types within Γ and thus all types and refinements remain well-formed with
    respect to integer variables in Γ . It thus suffices to show that FCV ([⃗ℓ/λ] φ) ⊆
    CV (⃗ℓ) = ∅ for any refinement φ appearing in τ or a type in Γ . By the
    assumed well-formedness of τ with respect to context variable λ (resp. Γ ),
    after substitution all free context variables in τ (resp. the types in Γ ) will
    be replaced with ⃗ℓ. Thus, post-substitution no free context variables appear
    in the refinement of [⃗ℓ/λ] τ (resp. refinements of types in [⃗ℓ/λ]Γ ), trivially
    satisfying our requirements.
 3. If λ does not appear free in τ1 , τ2 or Γ , then the result trivially holds. Let
    us then assume λ appears free. We prove the result by induction on the
    subtyping derivation.
     Case S-Ref:       τ1 = τ1′ ref r1                    τ2 = τ2′ ref r2
                       [⃗ℓ/λ] τ1 = ([⃗ℓ/λ] τ1′ ) ref r1   [⃗ℓ/λ] τ2 = ([⃗ℓ/λ] τ2′ ) ref r2
                       Γ ⊢ τ1′ ≤ τ2′                      r2 ≤ r1
     We must show that [⃗ℓ/λ]Γ ⊢ [⃗ℓ/λ] τ1′ ≤ [⃗ℓ/λ] τ2′ which holds immediately from
     the induction hypothesis.
     ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                   39

   Case S-Int:      τ1 = {ν : int
                               n | φ1 }            o       τ2 = {ν : int
                                                                      n | φ2 }            o
                    [ℓ/λ] τ1 = ν : int | [⃗ℓ/λ] φ1
                     ⃗                                     [ℓ/λ] τ2 = ν : int | [⃗ℓ/λ] φ2
                                                            ⃗
                    Γ |= φ1 =⇒ φ2
                                                                    r       z
  We must show that [⃗ℓ/λ]Γ |= [⃗ℓ/λ] φ1 =⇒ [⃗ℓ/λ] φ2 , i.e. |= [⃗ℓ/λ]Γ ∧
  [⃗ℓ/λ] φ1 =⇒ [⃗ℓ/λ] φ2 . From our assumption that Γ |= φ1 =⇒ φ2 we have
  that |= JΓ K∧φ1 =⇒ φ2 is valid, whereby the formula JΓ K∧φ1 =⇒ φ2 is true
  for any possible concrete valuation of the free context              ⃗
                    r        z                                z λ. As [ℓ/λ] JΓ K
                                                       r variable
  is equivalent to [⃗ℓ/λ]Γ we have the formula [⃗ℓ/λ]Γ ∧ [⃗ℓ/λ] φ1 =⇒
   [⃗ℓ/λ] φ2 must also be valid.
4. If λ does not appear free in JΓ K, then the result trivially holds. Otherwise
   |= JΓ K =⇒ φ holds forr any concrete
                                 z       valuation of the free context variable λ.
                           ⃗
   Then the formula |= [ℓ/λ]Γ =⇒ φ must be valid from the equivalence of
                  r       z
   [⃗ℓ/λ] JΓ K and [⃗ℓ/λ]Γ .
5. By induction on the typing derivation Θ | λ | Γ ⊢ e : τ ⇒ Γ ′ . In every case,
   that ⃗ℓ ⊢WF [⃗ℓ/λ] τ ⇒[⃗ℓ/λ]Γ ′ and ⃗ℓ ⊢WF [⃗ℓ/λ]Γ holds from Item 2.
   Case T-Var:       e=x                          τ = τ2
                     Γ = Γ0 [x : τ1 + τ2 ]        Γ ′ = Γ0 [x ←- τ2 ]
   By application of Item 1.
   Case T-LetInt:         e = let x = n in e ′       Θ | λ | Γ, x : {ν : int | ν = n} ⊢ e ′ : τ ⇒ Γ ′
                          x ̸∈ dom(Γ ′ )

  The induction hypothesis gives

              Θ | ⃗ℓ | [⃗ℓ/λ]Γ, x : {ν : int | ν = n} ⊢ e : [⃗ℓ/λ] τ ⇒[⃗ℓ/λ]Γ ′

  We conclude Θ | ⃗ℓ | [⃗ℓ/λ]Γ ⊢ let x = n in e : [⃗ℓ/λ] τ ⇒[⃗ℓ/λ]Γ ′ as required.
   Case T-Let:             e = let x = y in e ′            x ̸∈ dom(Γ ′ )
                           Θ | λ | Γ1 ⊢ e ′ : τ ⇒ Γ ′      Γ1 = Γ [y ←- (τ1 ∧y y =τ1 x )], x : (τ2 ∧x x =τ2 y)
                           Γ (y) = y : τ1 + τ2

   By Item 1, ([⃗ℓ/λ]Γ )(y) = [⃗ℓ/λ] (τ1 + τ2 ) = ([⃗ℓ/λ] τ1 + [⃗ℓ/λ] τ2 ). We must then
   show that Θ | ⃗ℓ | Γ1′ ⊢ e ′ : [⃗ℓ/λ] τ ⇒[⃗ℓ/λ]Γ ′ where

           Γ1′ = ([⃗ℓ/λ]Γ )[y ←- [⃗ℓ/λ] τ1 ∧y y = x ], x : ([⃗ℓ/λ] τ2 ∧x x = y)

  As Γ1′ = [⃗ℓ/λ]Γ1 the induction hypothesis gives the required typing judgment.
   Case T-If,T-Seq:
   By trivial application of the inductive hypothesis.
   Case T-MkRef,T-Deref:
   By reasoning similar to T-Let.
40       J. Toman et al.

     Case T-Call:          e = let x = f ℓ (y1 , . . . , yn ) in e ′
                           σx = [y1 /x1 ] · · · [yn /xn ]
                           σα = [ℓ : λ/λ′ ]
                           Θ | λ | Γ1 ⊢ e ′ : τ ⇒ Γ ′
                           y ̸∈ dom(Γ ′ )
                           Θ(f ) = ∀λ′ . ⟨x1 : τ1 , . . . , xn : τn ⟩ → ⟨x1 : τ1′ , . . . , xn : τn′ | τ ′ ⟩
                           Γ1 = Γ [yi ←- σα σx τi′ ], x : σα σx τ ′
     We must first show that for σα′ = [ℓ : ⃗ℓ/λ′ ]:

                                Θ | ⃗ℓ | Γ3 ⊢ e ′ : [⃗ℓ/λ] τ ⇒[⃗ℓ/λ]Γ ′

     where Γ3 = ([⃗ℓ/λ]Γ )[yi ←- σα′ σx τi′ ], x : σα′ σx τ ′ .
     We first observe that Γ3 = [⃗ℓ/λ]Γ1 (this follows from the equivalence of
     [⃗ℓ/λ] [ℓ : λ/λ′ ] and [ℓ : ⃗ℓ/λ′ ]) whereby the induction hypothesis gives the
     required typing derivation.
     We must also show that ∀i ∈ {1..n} .([ℓ : ⃗ℓ/λ]Γ )(yi ) = σα′ σx τi . From the
     assumed well-typing of the term under λ we have that ∀i ∈ {1..n} .Γ (yi ) =
     σα σx τi . Recall that σα′ is equivalent to [⃗ℓ/λ] σα , whereby we have [⃗ℓ/λ]Γ (yi ) =
     [⃗ℓ/λ] σα σx τi = σα′ σx τi for any i as equality is preserved by consistent sub-
     stitution.
     Case T-Assign:
     By the inductive hypothesis and application of Item 1.
     Case T-Alias: Θ | λ | Γ [x : τ1 ref r1 ][y : τ2 ref r2 ] ⊢ alias(x = y) ; e : τ ⇒ Γ
                                                           ′             ′
                           τ1 ref r1 +τ2 ref r2 ≈ τ1′ ref r1 +τ2′ ref r2
                                                    ′                 ′
                           Θ | λ | Γ [x ←- τ1′ ref r1 ][y ←- τ2′ ref r2 ] ⊢ e : τ ⇒ Γ
     From Item 1 we have that [⃗ℓ/λ] (τ1 ref r1 )+[⃗ℓ/λ] (τ2 ref r2 ) = [⃗ℓ/λ] (τ1 ref r1 +τ2 ref r2 )
                                ′           ′
     and similarly for τ1′ ref r1 +τ2′ ref r2 . It therefore remains to show that:
                                                                     ′           ′
                   [⃗ℓ/λ] (τ1 ref r1 +τ2 ref r2 ) ≈ [⃗ℓ/λ] (τ1′ ref r1 +τ2′ ref r2 )
                                                                                                ′          ′
     For which it suffices to show that • ⊢ [⃗ℓ/λ] (τ1 ref r1 +τ2 ref r2 ) ≤ [⃗ℓ/λ] (τ1′ ref r1 +τ2′ ref r2 )
                                ′            ′
     and • ⊢ [⃗ℓ/λ] (τ1′ ref r1 +τ2′ ref r2 ) ≤ [⃗ℓ/λ] (τ1 ref r1 +τ2 ref r2 ). From τ1 ref r1 +τ2 ref r2 ≈
              ′           ′
     τ1′ ref r1 +τ2′ ref r2 these both follow from Item 3, whereby the result follows
     from the inductive hypothesis.
     Case T-AliasPtr:
     By similar reasoning to the T-Alias case.
     Case T-Sub:            Θ | λ | Γ1 ⊢ e : τ1 ⇒ Γ2        Γ ≤ Γ1
                            Γ2 , τ1 ≤ Γ ′ , τ
     By the induction hypothesis we have that: Θ | ⃗ℓ | [⃗ℓ/λ]Γ1 ⊢ e : [⃗ℓ/λ] τ1 ⇒[⃗ℓ/λ]Γ2 .
     If we show that [⃗ℓ/λ]Γ ≤ [⃗ℓ/λ]Γ1 and [⃗ℓ/λ]Γ2 , [⃗ℓ/λ] τ1 ≤ [⃗ℓ/λ]Γ ′ , [⃗ℓ/λ] τ
     we will have the required result. To show the first requirement, for any
     x ∈ dom(Γ ) we have that [⃗ℓ/λ]Γ ⊢ [⃗ℓ/λ]Γ (x ) ≤ [⃗ℓ/λ]Γ1 (x ) from Item 3 so
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                       41

    we have [⃗ℓ/λ]Γ ≤ [⃗ℓ/λ]Γ1 . To show the latter requirement, we observe that
    [⃗ℓ/λ]Γ2 , [⃗ℓ/λ] τ1 ≤ [⃗ℓ/λ]Γ ′ , [⃗ℓ/λ] τ is equivalent to showing [⃗ℓ/λ](Γ2 , x : τ1 ) ≤
    [⃗ℓ/λ](Γ ′ , x : τ ) for some x ̸∈ dom(Γ2 ), whereby we have the required subtyp-
    ing relationship from the application of Item 3.
    Case T-Assert:           Θ | λ | Γ ⊢ assert(φ) ; e : τ ⇒ Γ ′
                                                              Γ |= φ
                             Θ | λ | Γ ⊢ e : τ ⇒Γ′            ϵ | Γ ⊢WF φ
    By induction hypothesis, the result holds if we can show [⃗ℓ/λ]Γ |= φ which
    follows from Item 4 (that λ ̸∈ FCV (φ) follows from the well-formedness of
    φ with respect to ϵ).

Lemma 10 (Substitution). If Θ | L | Γ ⊢ e : τ ⇒ Γ ′ and x ′ ̸∈ dom(Γ ), then
Θ | L | [x ′ /x ] Γ ⊢ [x ′ /x ]e : [x ′ /x ] τ ⇒[x ′ /x ] Γ ′ .

Proof. By straightforward induction of typing rules.

Lemma 11. If Θ | ⃗ℓ | Γ ⊢ x : τ ⇒ Γ ′ , then Θ | ⃗ℓ′ | Γ ⊢ x : τ ⇒ Γ ′ .

Proof. Induction on the variable typing derivation.

  We now prove that if every variable satisfies its refinement in a type environ-
ment Γ , we must have |= [R] JΓ K.

Lemma 12. If SAT (H , R, Γ ) then |= [R] JΓ K.

Proof. To show |= [R] JΓ K, it suffices to show that for any x ∈ dom(Γ ) where
Γ (x ) = {ν : int | φ} |= [R] [x / ν ] φ holds. From SAT (H , R, Γ ), we must have
SATv(H , R, R(x ), Γ (x )), whereby we have R(x ) ∈ Z and [R] [R(x )/ν]φ. As
[R] [x / ν ] φ is equivalent to [R] [R(x )/ν]φ, and we have the desired result.

   We prove that subtyping preserves the consistency relation in the following
sense.

Lemma 13. If Γ ≤ Γ ′ and Cons (H , R, Γ ) then:

1. For any x ∈ dom(Γ ′ ), ∀ a ∈ dom(H ).own (H , R(x ), Γ ′ (x ))(a) ≤ own (H , R(x ), Γ (x ))(a)
2. ∀ a ∈ dom(H ).Own (H , R, Γ ′ )(a) ≤ 1
3. If Γ ⊢ τ ≤ τ ′ and SATv(H , R, v , τ ) then SATv(H , R, v , τ ′ )
4. SAT (H , R, Γ ′ )
5. Cons (H , R, Γ ′ )

Proof.

 1. By induction on Γ ⊢ Γ (x ) ≤ Γ ′ (x ).
 2. Direct consequence of 1 and that ∀ a ∈ dom(H ).Own (H , R, Γ )(a) ≤ 1 from
    Cons (H , R, Γ ).
 3. From Cons (H , R, Γ ) we have SAT (H , R, Γ ) which by Lemma 12 we have
    |= [R] JΓ K. We now proceed by induction on Γ ⊢ τ ≤ τ ′ .
42      J. Toman et al.

     Case:      τ = {ν : int | φ}          τ ′ = {ν : int | φ′ }
                |= JΓ K ∧ φ =⇒ φ′
     From SATv(H , R, v , τ ) we have |= [R] [v /ν]φ. We must show that |= [R] [v /ν]φ′ .
     From |= JΓ K ∧ φ =⇒ φ′ we must have |= [R] [v /ν] JΓ K ∧ [R] [v /ν]φ =⇒
     [R] [v /ν]φ′ is valid. As ν does not appear free in JΓ K, we have |= [R] JΓ K ∧
     [R] [v /ν]φ =⇒ [R] [v /ν]φ′ is valid whereby the result is immediate.
     Case:    τ = τp ref r1  τ ′ = τp′ ref r2
              r2 ≤ r1
    Immediate from the induction hypothesis.
 4. Immediate consequence of 3 and that Γ ≤ Γ ′ implies that Γ ⊢ Γ (x ) ≤ Γ ′ (x )
    for any x ∈ dom(Γ ′ ).
 5. Immediate from 2 and 4.

   To show consistency is preserved during evaluation, Lemmas 14 and 15 show
types equivalent according to ≈ are equivalent for the purposes of own and SATv.
Then Lemmas 16 and 17 show that the type addition operator + “distributes”
over SATv and own.

Lemma 14 (Type Equivalence Preserves Satisfiability). If τ1 ≈ τ2 , then
SATv(H , R, v , τ1 ) ⇐⇒ SATv(H , R, v , τ2 ).

Proof. We prove the forward case by induction on • ⊢ τ1 ≤ τ2 as implied by
τ1 ≈ τ2 . The inductive case follows from the IH. In the the base case where τ1 =
{ν : int | φ1 } and τ2 = {ν : int | φ2 }, from • ⊢ τ1 ≤ τ2 we have that |= φ1 =⇒ φ2
is valid, from which we must have |= [R] [v /ν]φ1 =⇒ [R] [v /ν]φ2 , where from
the definition of SATv(H , R, v , τ1 ) we must then have SATv(H , R, v , τ2 ).
    The backwards case follows similar reasoning by induction on • ⊢ τ2 ≤ τ1 .

Lemma 15. If τ1 ≈ τ2 , then own (H , v , τ1 ) = own (H , v , τ2 ).

Proof. By reasoning similar to that in Lemma 14.

Lemma 16. If τp = τ1 +τ2 , then own (H , v , τp ) = own (H , v , τ1 )+own (H , v , τ2 ).

Proof. By induction on the rules used to derive τ1 + τ2 = τp .
Case Tadd-Int:
We have own (H , v , τp ) = own (H , v , τ1 + τ2 ), where τ1 + τ2 = {ν : int | φ1 ∧ φ2 },
own (H , v , τ1 ) and own (H , v , τ2 ), where τ1 = {ν : int | φ1 } , τ2 = {ν : int | φ2 }.
   From the definition of ownership, we have own (H , v , τp ) = own (H , v , τ1 ) =
own (H , v , τ2 ) = ∅. It is thus trivial that own (H , v , τp ) = own (H , v , τ1 ) +
own (H , v , τ2 ).
Case Tadd-Ref:
We assume v = a and a ∈ dom(H ), otherwise the result trivially holds.
   We have own (H , v , τp ) = own (H , v , τ1 +τ2 ), where τ1 +τ2 = (τ1′ +τ2′ ) ref r1 +r2 ,
and τ1 = τ1′ ref r1 , τ2 = τ2′ ref r2 .
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                    43

  From the definition of ownership, we have own (H , v , τp ) = {a 7→ r1 + r2 } +
own (H , H (v ), τ1′ + τ2′ ) and:

own (H , v , τ1 ) + own (H , v , τ2 ) = {a 7→ r1 } + own (H , H (v ), τ1′ ) + {a 7→ r2 } + own (H , H (v ), τ2′ )
                                    = {a 7→ r1 + r2 } + own (H , H (v ), τ1′ ) + own (H , H (v ), τ2′ )

By the induction hypothesis, have that own (H , H (v ), τ1′ +τ2′ ) = own (H , H (v ), τ1′ )+
own (H , H (v ), τ2′ ) and can conclude that own (H , v , τp ) = own (H , v , τ1 ) +
own (H , v , τ2 ).

Lemma 17. If τp = τ1 + τ2 , we have SATv(H , R, v, τp ) iff. SATv(H , R, v, τ1 )
and SATv(H , R, v, τ2 )

Proof. By induction on the rules used to derive τ1 + τ2 . In the following we
only prove the forward direction of the implication; the backwards direction is
symmetric.
Case Tadd-Int:
We have SATv(H , R, v, τ1 + τ2 ), where τ1 + τ2 = {ν : int | φ1 ∧ φ2 }, we must
show SATv(H , R, v, τ1 ) and SATv(H , R, v, τ2 ), where τ1 = {ν : int | φ1 } , τ2 =
{ν : int | φ2 }.
    From the definition of SATv, we must show [R] [v/ν]φ1 and [R] [v/ν]φ2 .
From SATv(H , R, v, τ1 + τ2 ) we have [R] [v /ν](φ1 ∧ φ2 ). It is immediate that
for any value v such that [R] [v /ν](φ1 ∧ φ2 ), we must have [R] [v /ν]φ1 and
[R] [v /ν]φ2 . We then conclude SATv(H , R, v, τ1 + τ2 ) implies SATv(H , R, v, τ1 )
and SATv(H , R, v, τ2 ).
Case Tadd-Ref:
Immediate from the definition of SATv and the inductive hypothesis.

Definition 2. The valid substitution relation, written R ⊢vs τ is the smallest
relation closed under the following rules:

                   ∀ x ∈ FPV (φ) \ {ν} .∃ n.R(x ) = n
                           R ⊢vs {ν : int | φ}

                                  R ⊢vs τ
                                R ⊢vs τ ref r

Lemma 18. If ⃗ℓ ⊢WF Γ and Cons (H , R, Γ ), then ∀ x ∈ dom(Γ ).R ⊢vs Γ (x ).

Proof. By Cons (H , R, Γ ), all integer variables in Γ must be in the domain of R
and must be an integer. From ⃗ℓ ⊢WF Γ , any free variables in any refinement of any
type in Γ must be an integer valued variable in Γ , which gives the required result.

Definition 3. We will write R ⊑ R ′ to denote two register files such that:
 1. dom(R) ⊆ dom(R ′ ), and
44       J. Toman et al.

 2. ∀ x ∈ dom(R).R(x ) = R ′ (x )

Definition 4. Two heaps H and H ′ are equivalent modulo a, written H ≈a H ′
if:

 1. dom(H ) = dom(H ′ )
 2. ∀ a ′ ∈ dom(H ).a ′ ̸= a =⇒ H (a ′ ) = H ′ (a ′ )
 3. For any n, H ⊢ a ⇓ n iff H ′ ⊢ a ⇓ n

Lemma 19 (Same-shape heap update). Suppose H (a) = v , H ⊢ v ⇓ n,
and H ⊢ v ′ ⇓ n. If H ′ = H {a ←- v ′ }, then H ≈a H ′ .

Proof. Easy.

Lemma 20. For any type τ = ⊤n , H , v , own (H , v , ⊤n ) = ∅.

Proof. By induction on τ . In the base case, the result is trivial. Then consider the
case where τ = ⊤n−1 ref 0 . If v ̸∈ Addr, or if v = a and a ̸∈ dom(H ), then the
result trivially holds. Otherwise the result holds from the inductive hypothesis,
the definition of + and {a 7→ 0}.

Lemma 21 (Heap Update Ownership Preservation). If L | Γ ⊢WF τ ,
H ≈a H ′ , and own (H , v , τ )(a) = 0, then own (H , v , τ ) = own (H ′ , v , τ ).

Proof. By induction on the shape of τ . If τ = {ν : int | φ} then the result trivially
holds. Otherwise, τ = τ ′ ref r . We assume that v = a ′′ and a ′′ ∈ dom(H )
(otherwise the result trivially holds, as dom(H ) = dom(H ′ ) by H ≈a H ′ ).
Consider the case where a ′′ = a. By definition own (H , a, τ ) = {a 7→ r} +
own (H , H (a), τ ′ ), and by the assumption that own (H , a, τ )(a) = 0 we must
have that r = 0. Further, by the ownership well-formedness of types, we must
have τ ′ = ⊤n for some n, thus by Lemma 20 we have own (H , v , τ ) = ∅ = {a 7→
0} + own (H ′ , H ′ (a), ⊤n ) = own (H ′ , v , τ ).
    Finally, consider the case where a ′′ ̸= a. Then from the definition of
own (H , a ′′ , τ ) and our assumption that own (H , a ′′ , τ )(a) = 0, we have own (H , H (a ′′ ), τ ′ )(a) =
0, and the result holds from the inductive hypothesis and that H (a ′′ ) = H ′ (a ′′ ).

Lemma 22. For any H , R, v , and τ , if SATv(H , R, v , τ ) then H ⊢ v ⇓ |τ |

Proof. By induction on τ and the definition of SATv.

Lemma 23. For any n, if H ⊢ v ⇓ n then for any R, SATv(H , R, v, ⊤n ).

Proof. By induction on n. In the base case, by inversion on H ⊢ v ⇓ 0 we have
v ∈ Z and as [R] [v/ν]⊤ =⇒ ⊤, we conclude SATv(H , R, v, ⊤0 ).
   For n > 0, by inversion on H ⊢ v ⇓ n we have that v = a, a ∈ dom(H ), and
H ⊢ H (a) ⇓ n − 1, whereby the result holds from the inductive hypothesis.

Lemma 24 (Heap Update Consistency Preservation). If L | Γ ⊢WF τ ,
H ≈a H ′ , own (H , v , τ )(a) = 0, and SATv(H , R, v , τ ), then SATv(H ′ , R, v , τ ).
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                   45

Proof. By induction on the shape of τ . The base case where τ = {ν : int | φ} is
trivial. We therefore consider the case where v = a ′ and τ = τ ′ ref r .
    We first consider the case where a ′ = a, then by our assumption that
own (H , a, τ )(a) = 0, we must have that τ = τ ′ ref 0 , whereby τ = ⊤n for some
n. From SATv(H , R, a, τ ) and Lemma 22, we must have that H ⊢ a ⇓ |τ |, and
from H ≈a H ′ , we therefore have that H ′ ⊢ a ⇓ |τ | whereby the result holds
from Lemma 23.
    Otherwise, we have that a ′ =        ̸ a, and by definition we must have that
own (H , H (a ′ ), τ ′ )(a) = 0 and H ′ (a ′ ) = H (a ′ ) hence the result follows from the
inductive hypothesis.

Lemma 25 (Register Weakening). If SATv(H , R, v, τ ) and R ⊢vs τ , then
for any R ′ such that R ⊑ R ′ , SATv(H , R ′ , v, τ ).

Proof. By induction on the shape of τ . If τ = τ ′ ref r , then the result follows from
the inductive hypothesis. We therefore consider the case where τ = {ν : int | φ}.
Without loss of generality, we consider the case where dom(R ′ ) \ dom(R) = {x},
and R ′ (x ) = n. (If R ′ (x ) = a, the extra binding also has no effect, and the
case where more than one binding is added follows from n applications of the
following argument.)
    From SATv(H , R, v, τ ), we conclude that v ∈ Z and that [R] [v/ν]φ. If
x ̸∈ FPV (φ) then [R] [v/ν]φ ⇐⇒ [R ′ ] [v/ν]φ and the result holds trivially.
Otherwise, if x ∈ FPV (φ) and x ̸∈ dom(R) then R is not a valid substitution,
violating our assumption.

Lemma 26 (Heap Extension Consistency Preservation). If we have heap
H, such that SATv(H , R, v , τ ), for any heap H ′ = H {a 7→ v ′ }, a ̸∈ dom(H ),
then we have SATv(H ′ , R, v , τ ).

Proof. By induction on the shape of τ . The base case where τ = {ν : int | φ}
is trivial. Next, we consider the case where τ = τ ′ ref r . We must show that
v ∈ dom(H ′ ) and SATv(H ′ , R, H ′ (v ), τ ′ ). The first condition is immediately
satisfied by inversion on SATv(H , R, v , τ ′ ), and from a ̸∈ dom(H ), we have v =
                                                                                  ̸ a,
which gives that H ′ (v) = H(v). That is we must show SATv(H ′ , R, H (v ), τ ′ ),
which is follows from the induction hypothesis.

Lemma 27 (Full-reference exclusion). Suppose L ⊢WF Γ , Cons (H , R, Γ ),
Γ (y) = τ ref 1 , and R(y) = a. Then H (a) is defined, own (H , H (a), τ )(a) = 0,
and for every x ∈ dom(Γ ) with x ̸= y, own (H , R(x ), Γ (x ))(a) = 0.

Proof. Satisfaction of y gives the heap lookup. Its contribution at a is 1 +
own (H , H (a), τ )(a). All remaining contributions, including the recursive contri-
bution of τ , are nonnegative, while consistency bounds their total by one. Hence
every contribution other than the displayed 1 is zero.

Lemma 28 (Heap Extension Ownership Preservation). If SATv(H , R, v , τ ),
then for any a ̸∈ dom(H ) own (H , v , τ ) = own (H {a 7→ v ′ }, v , τ ) for any value
v ′.
46       J. Toman et al.

Proof. By induction on τ . The base case is trivial as own (H , v , {ν : int | φ}) =
∅ = own (H {a 7→ v }, v , {ν : int | φ}). We therefore consider the case where
τ = τ ′ ref r .
    From SATv(H , R, v , τ ) we must have that v = a ′ and a ′ ∈ dom(H ) (and
by extension a ′ ∈ dom(H {a 7→ v ′ })). From the definition of the ownership
function, we have that own (H , v , τ ) = own (H , H (a ′ ), τ ′ ) + {a ′ 7→ r}. and
own (H {a 7→ v ′ }, v , τ ) = own (H {a 7→ v ′ }, H {a 7→ v ′ }(a ′ ), τ ′ ) + {a ′ 7→ r}
Then from our requirement that a ̸∈ dom(H ), we have a ̸= a ′ and therefore
H (a ′ ) = H {a 7→ v ′ }(a ′ ), whereby the result holds from the inductive hypothesis.

Lemma 29 (Environment Weakening). Define the partial operation Γ1 ⊎ Γ2
for two environments such that dom(Γ1 ) ∩ dom(Γ2 ) = ∅:
                                        
                                         Γ1 (x )
                                                       x ∈ dom(Γ1 )
                    (Γ1 ⊎ Γ2 )    (x ) = Γ2 (x )        x ∈ dom(Γ2 )
                                        
                                          undef         o.w.
                                        


     Then, for any Γ and Γ ′′ where dom(Γ ) ∩ dom(Γ ′′ ) = ∅:

 1. Γ ⊢ τ1 ≤ τ2 implies Γ ⊎ Γ ′′ ⊢ τ1 ≤ τ2
 2. Γ ≤ Γ ′ implies Γ ⊎ Γ ′′ ≤ Γ ′ ⊎ Γ ′′
 3. If Θ | L | Γ ⊢ e : τ ⇒ Γ ′ , L ⊢WF Γ ⊎ Γ ′′ , and L ⊢WF Γ ′ ⊎ Γ ′′ , then
    Θ | L | Γ ⊎ Γ ′′ ⊢ e : τ ⇒ Γ ′ ⊎ Γ ′′

Proof.

 1. As in the proof of Lemma 9 (part 3), at the root of the subtyping derivation
    is a logical judgment of the form |= JΓ K ∧ φ1 =⇒ φ2 which can be shown
    to be valid. We must then show that |= JΓ ⊎ Γ ′′ K ∧ φ1 =⇒ φ2 is valid. As
    JΓ ′′ ⊎ Γ K ∧ φ1 = JΓ ′′ K ∧ JΓ K ∧ φ only strengthens the pre-condition JΓ K ∧ φ1 ,
    |= JΓ ′′ ⊎ Γ K ∧ φ1 =⇒ φ2 must also be valid.
 2. It suffices to show that Γ ⊎ Γ ′′ ⊢ (Γ ⊎ Γ ′′ )(x ) ≤ (Γ ′ ⊎ Γ ′′ )(x ) for any arbitrary
    x ∈ dom(Γ ′ ⊎ Γ ′′ ). If x ∈ dom(Γ ′ ) then we must have Γ ⊢ Γ (x ) ≤ Γ ′ (x ) by
    inversion on Γ ≤ Γ ′ , whereby Γ ⊎ Γ ′′ ⊢ (Γ ⊎ Γ ′′ )(x ) = Γ (x ) ≤ Γ ′ ⊎ Γ ′′ (x ) =
    Γ ′ (x ) from part 1.
    If x ̸∈ dom(Γ ′ ), then we must show (Γ ⊎ Γ ′′ ) ⊢ Γ ′′ (x ) ≤ Γ ′′ (x ), which
    trivially holds.
 3. By induction on the typing derivation of Θ | L | Γ ⊢ e : τ ⇒ Γ ′ . We assume
    that the variables bound in any let expressions that appear within e are not
    in the domain of Γ ′′ ; this requirement can be easily enforced with consistent
    renaming and is preserved during evaluation. The only interesting cases are
    T-Sub and T-Assert and the let bindings; the other cases follow from the
    induction hypothesis.
    We now prove the relevant cases.
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types              47

    Case T-Let:       Θ | L | Γ ⊢ let x = y in e : τ ⇒ Γ ′
                      Θ | L | Γ [y ←- τ1 ∧y y =τ1 x ], x : τ2 ∧x x =τ2 y ⊢ e : τ ⇒ Γ ′
                      Γ (y) = τ1 + τ2      x ̸∈ dom(Γ ′ )

    Let Γ ′′′ = Γ ′′ ⊎ Γ [y ←- τ1 ∧y y =τ1 x ], x : τ2 ∧x x =τ2 y. To use the in-
    ductive hypothesis, we must show that L ⊢WF Γ ′′′ and L ⊢WF Γ ′ ⊎ Γ ′′ .
    The latter holds by assumption. To show the former, it suffices to show
    L | Γ ′′′ ⊢WF τ1 ∧y y =τ1 x and L | Γ ′′′ ⊢WF τ2 ∧x x =τ2 y. From the as-
    sumed well-formedness L ⊢WF Γ ⊎ Γ ′′ , we must have L | Γ ⊎ Γ ′′ ⊢WF τ1 + τ2 ,
    and in particular L | Γ ⊎ Γ ′′ ⊢WF τ1 and L | Γ ⊎ Γ ′′ ⊢WF τ2 . From this
    we conclude both conditions hold. To show the well-typing of the overall let
    expression, we must show x ̸∈ dom(Γ ′ ⊎ Γ ′′ ), which follows from our assump-
    tion and x ̸∈ dom(Γ ′ ). Finally, we must also show that L | Γ ′ ⊎ Γ ′′ ⊢WF τ .
    From L | Γ ′ ⊢WF τ and the fact that∀ x ∈ dom(Γ ′ ).Γ ′ (x ) = {ν : int | } iff
    (Γ ′ ⊎ Γ ′′ )(x ) = {ν : int | }, we must have L | Γ ′ ⊎ Γ ′′ ⊢WF τ .
    Cases T-LetInt, T-Mkref, T-Mkref, T-Deref, T-Call:
    Similar to the reasoning in T-Let.
    Case T-Sub:        Γ ≤ Γ1              Θ | L | Γ1 ⊢ e : τ2 ⇒ Γ2
                       Γ2 , τ2 ≤ Γ ′ , τ
    From the rules for subtyping, we must have dom(Γ1 ) ⊆ dom(Γ ) and dom(Γ ′ ) ⊆
    dom(Γ2 ). A simple inductive argument gives that dom(Γ2 ) ⊆ dom(Γ1 ), there-
    fore we have dom(Γ ′ ) ⊆ dom(Γ1 ). Let LV be the set of free variables in the
    refinements of Γ ′′ that are not in the domain of Γ ′′ . From the assumed well-
    formedness of L ⊢WF Γ ′ ⊎ Γ ′′ , we must have that ∀x ∈ LV.x ∈ dom(Γ ′ ) ∧
    Γ ′ (x ) = {ν : int | }. Thus, LV ⊆ Γ1 and LV ⊆ Γ2 . Further, by definition, for
    any Γp ≤ Γq , if Γq (x ) = {ν : int | } then Γp (x ) = {ν : int | }, i.e. subtyping
    preserves simple types. We conclude that L ⊢WF Γ1 ⊎ Γ ′′ and L ⊢WF Γ2 ⊎ Γ ′′ ,
    whereby the inductive hypothesis gives Θ | L | Γ1 ⊎ Γ ′′ ⊢ e : τ2 ⇒ Γ2 ⊎ Γ ′′ .
    To prove the overall result, we must show that Γ ⊎ Γ ′′ ≤ Γ1 ⊎ Γ ′′ and
    Γ2 ⊎ Γ ′′ , τ2 ≤ Γ ′ ⊎ Γ ′′ , τ which follow from parts 1 and 2 above. That
    L | Γ2 ⊎ Γ ′′ ⊢WF τ2 follows by reasoning to the case for T-Let above.
    Case T-Assert:
    We must show that |= JΓ ′′ ⊎ Γ K =⇒ φ which is equivalent to |= JΓ ′′ K ∧
    JΓ K =⇒ φ. As the source term was well typed, |= JΓ K =⇒ φ is valid, we
    must then have |= JΓ ′′ K ∧ JΓ K =⇒ φ whereby the inductive hypothesis gives
    the required result.


C    Proof of Lemma 3

We first prove two additional lemmas. Lemmas 30 and 31 give key facts used
in the return and call cases respectively; we have separated them into separate
lemmas for clarity.
48       J. Toman et al.

Lemma 30. For any Γ0 such that Θ | ℓ : ⃗ℓ | Γ0 ⊢ x : τ1 ⇒ Γ1 and Θ | [] :
τ1 ⇒ Γ1 | ⃗ℓ ⊢ectx E [let y = []ℓ in e] : τ2 ⇒ Γ2 then Θ | ⃗ℓ | Γ0 ⊢ E [let y =
[]ℓ in e][x ] : τ2 ⇒ Γ2 .

Proof. It suffices to show that Θ | ⃗ℓ | Γ0 ⊢ let y = x in e : τ1′ ⇒ Γ1′ and Θ | [] :
τ1′ ⇒ Γ1′ | ⃗ℓ ⊢ectx E : τ2 ⇒ Γ2 for some τ1′ and Γ1′ whereby the result will hold
from Lemma 8.
    By inversion on Θ | [] : τ1 ⇒ Γ1 | ⃗ℓ ⊢ectx E [let y = []ℓ in e] : τ2 ⇒ Γ2 we have

                           Θ | ⃗ℓ | Γ1 , y : τ1 ⊢ e : τ1′′ ⇒ Γ1′′                     (1)
                           Θ | [] : τ ′′ ⇒ Γ ′′ | ⃗ℓ ⊢ectx E : τ2 ⇒ Γ2
                                    1        1                                        (2)
                           y ̸∈ dom(Γ1′′ )                                            (3)

We take Γ1′ = Γ1′′ , τ1′ = τ1′′ , and then Equation (2) gives the necessary typing for E .
   It remains to to show that

                           Θ | ⃗ℓ | Γ0 ⊢ let y = x in e : τ1′ ⇒ Γ1′

(That ⃗ℓ ⊢WF τ1′ ⇒ Γ1′ follows from Equation (1))
   By Lemma 6 and Lemma 11, from Θ | ℓ : ⃗ℓ | Γ0 ⊢ x : τ1 ⇒ Γ1 we conclude
there exists some Γp , τp , and Γp′ such:

                                        Γ0 ≤ Γp                                       (4)
                                        Γp′ , τp ≤ Γ1 , τ1                            (5)
                                        Γp′ = Γp [x ←- τp′ ]                          (6)
                                        Γp (x ) = τp + τp′                            (7)
                                        ⃗ℓ ⊢WF Γp                                     (8)

     We first apply T-Sub with Equations (4) and (8), so it remains to show

                  Θ | ⃗ℓ | Γp [x : τp + τp′ ] ⊢ let y = x in e : τ1′ ⇒ Γ1′

which, by T-Let holds if we show that:

           Θ | ⃗ℓ | Γp [x ←- τp′ ∧x x =τp′ y], y : τp ∧y y =τp x ⊢ e : τ1′ ⇒ Γ1′

(y ̸∈ dom(Γ1′ ) follows from Equation (3), and the well-formedness of Γp [x ←-
τp′ ∧x x =τp′ y], y : τp ∧y y =τp x follows from the well-formedness of Γp , τp and
τp′ and that x and y appear in the refinements iff they are mapped to integer
types in the new type environment.)
    We can use T-Sub to weaken the type environment to:

                       Θ | ⃗ℓ | Γp [x ←- τp′ ], y : τp ⊢ e : τ1′ ⇒ Γ1′

From Equation (5) above, we have that Γp [x ←- τp′ ], y : τp ≤ Γ1 , y : τ1 , whereby
one final application of T-Sub allows us to use to Equation (1) above.
       ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                              49

Lemma 31. Let E [let x = f ℓ (y1 , . . . , yn ) in e ′ ] be a term such that:
    Θ | ⃗ℓ | Γ0 ⊢ let x = f ℓ (y1 , . . . , yn ) in e ′ : τ1 ⇒ Γ1          σα = [ℓ : ⃗ℓ/λ]
                         ⃗
    Θ | [] : τ1 ⇒ Γ1 | ℓ ⊢ectx E : τ2 ⇒ Γ2                                 σx = [y1 /x1 ] · · · [yn /xn ]
    f 7→ (x1 , .. , xn )e ∈ D                                              Θ ⊢ f 7→ (x1 , .. , xn )e
    ⊢WF Θ
  where Θ(f ) = ∀λ. ⟨x1 : τ1 , . . . , xn : τn ⟩ → ⟨x1 : τ1′ , . . . , xn : τn′ | τq ⟩.
  Then there exist some τ3 and Γ3 :
                  Θ | ℓ : ⃗ℓ | Γ0 ⊢ σx e : τ3 ⇒ Γ3
                  Θ | [] : τ3 ⇒ Γ3 | ⃗ℓ ⊢ectx E [let x = []ℓ in e ′ ] : τ2 ⇒ Γ2

Proof. From Lemma 6 on Θ | ⃗ℓ | Γ0 ⊢ let x = f ℓ (y1 , . . . , yn ) in e ′ : τ1 ⇒ Γ1 we
have, for some Γp , τp , Γp′ , that:

                   Γ0 ≤ Γp                                                                          (9)
                   Γp′ , τp ≤ Γ1 , τ1                                                             (10)
                   Γp (yi ) = σα σx τi                                                            (11)
                  ⃗ℓ ⊢WF Γp                                                                       (12)
                   Θ | ⃗ℓ | Γp [yi ←- σα σx τi′ ], x : σα σx τq ⊢ e ′ : τp ⇒ Γp′                  (13)
                   x ̸∈ dom(Γp′ )                                                                 (14)
     To prove the first part, from the well-typing of the function body, we
 have Θ | λ | x1 : τ1 , . . . , xn : τn ⊢ e : τq ⇒ x1 : τ1′ , . . . , xn : τn′ . From our assump-
 tion that all variable names are distinct, by n applications of the substitu-
 tion lemma (Lemma 10) we have: Θ | λ | y1 : σx τ1 , . . . , yn : σx τn ⊢ σx e :
 σx τq ⇒ y1 : σx τ1′ , . . . , yn : σx τn′ . By Lemma 9 (part 5) we then have Θ | ℓ :
⃗ℓ | y1 : σα σx τ1 , . . . , yn : σα σx τn ⊢ σx e : σα σx τq ⇒ y1 : σα σx τ ′ , . . . , yn : σα σx τ ′ .
                                                                                 1                  n
We take τ3 = σα σx τq and Γ3 = Γp [yi ←- σα σx τi′ ].
     By the well-formedness of function types and well-formedness of Γp , we must
 have that ℓ : ⃗ℓ ⊢WF Γ3 . Then by Equations (11) and (12) and lemma 29 we have
 Θ | ℓ : ⃗ℓ | Γp ⊢ σx e : τ3 ⇒ Γ3 , whereby Equation (9) and an application of T-Sub
 gives Θ | ℓ : ⃗ℓ | Γ0 ⊢ σx e : τ3 ⇒ Γ3 , i.e., the first result.
     To prove the second part, from the typing rule for TE-Stack we must show:
                             Θ | [] : τ1 ⇒ Γ1 | ⃗ℓ ⊢ectx E : τ2 ⇒ Γ2                              (15)
                             x ̸∈ dom(Γ1 )                                                        (16)
                             Θ | ⃗ℓ | Γ3 , x : τ3 ⊢ e ′ : τ1 ⇒ Γ1                                 (17)
Equation (15) holds by assumption, and Equation (16) follows from Equation (14)
and that Γp′ ≤ Γ1 implies dom(Γ1 ) ⊆ dom(Γp′ ). ⃗ℓ ⊢WF τ1 ⇒ Γ1 follows from
the well-typing of the function call term, and ⃗ℓ ⊢WF Γ3 , x : τ3 follows from
Equation (13).
   From Equations (10) and (13) we then have Equation (17) via an application
of T-Sub.
50       J. Toman et al.

Proof (Preservation; Lemma 3). The proof is organized by cases analysis on
the transition rule used of e, and showing that the output configuration is well
                                                      ′′                         ′      ′
typed by ⊢D      conf . We must therefore find a Γ that is consistent with H and R
                                                                               D
and also satisfies the other conditions imposed by the definition of ⊢conf . Here
Γ ′′ , H ′ , R ′ represent the type environment, heap and register after the transition
respectively. We identify the heap and register file before transition with H and R
respectively. In order to show that the ownership invariant is preserved, we need to
prove that ∀ a ∈ dom(H ′ ).Own (H ′ , R, Γ ′′ )(a) ≤ 1. In many cases, we will show
that Own (H , R, Γ ) = Own (H ′ , R ′ , Γ ′′ ), whereby from the assumption that
Cons (H , R, Γ ) as implied by ⊢D       conf we have ∀ a ∈ dom(H ).Own (H , R, Γ )(a) ≤
1, giving the desired result.
                              D                     E D                    E    D                     E
Case R-Var: ⊢D           conf   H , R, Fn−1 : F⃗ , x , H , R, Fn−1 : F⃗ , x −→D H , R, F⃗ , Fn−1 [x ]
                                                     D                    E
By inversion on configuration typing ⊢D
                                      conf            H , R, Fn−1 : F⃗ , x , we have:

              Θ | ⃗ℓ | Γ ⊢ x : τn ⇒ Γn
              ∀i ∈ {1..n} .Θ | [] : τi ⇒ Γi | ⃗ℓi−1 ⊢ectx Fi−1 : τi−1 ⇒ Γi−1

  Using Lemma 30, we can conclude that Θ | ⃗ℓn−1 | Γ ⊢ Fn−1 [x ] : τn−1 ⇒ Γn−1 .
We therefore take Γ ′′ = Γ .
  It remains to show that Cons (H , R, Γ ′′ ) which follows immediately from
Cons (H , R, Γ ).
                           D                                  E
Case R-Deref: ⊢D             H  , R,  ⃗ , E [let x = ∗y in e]
                                      F
                   Dconf                              E         D                              E
                      H , R, F⃗ , E [let x = ∗y in e] −→D H , R{x ′ 7→ v }, F⃗ , E [[x ′ /x ]e]
                   H (a) = v            R(y) = a         R ′ = R{x ′ 7→ v }
By inversion on the configuration typing relationship, we have that:

          Θ | ⃗ℓ | Γ0 ⊢ E [let x = ∗y in e] : τn ⇒ Γn               Cons (H , R, Γ0 )

By Lemma 7, we have some τ, Γ0′ such that:

     Θ | [] : τ ⇒ Γ0′ | ⃗ℓ ⊢ectx E : τn ⇒ Γn      Θ | ⃗ℓ | Γ0 ⊢ let x = ∗y in e : τ ⇒ Γ0′

Using Lemma 6, we have some Γp , Γp′ and τp such that:


                       Γ0 ≤ Γp         ⃗ℓ ⊢WF Γp        Γp′ , τp ≤ Γ0′ , τ
                       Γp (y) = (τ1 + τ2 ) ref r     x ̸∈ dom(Γp′ )
                                   (
                                     (τ1 ∧y y =τ1 x ) r > 0
                            τ ′′ =
                                     τ1                 r=0
                      Θ | ⃗ℓ | Γp [y ←- τ ′′ ref r ], x : τ2 ⊢ e : τp ⇒ Γp′
       ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                             51

    From Lemma 13, we then have Cons (H , R, Γp ). We will now show that:

                        Cons (H , R{x ′ 7→ v }, Γ ′′ )                                        (18)
                        Θ | ⃗ℓ | Γ ′′ ⊢ [x ′ /x ]e : [x ′ /x ] τp ⇒[x ′ /x ] Γ ′
                                                                              p               (19)

where Γ ′′ = Γp [y ←- ([x ′ /x ] τ ′′ ) ref r ], x ′ : τ2 .
     Together these give our desired result. To see how, from Θ | ⃗ℓ | Γp [y ←-
τ ref r ], x : τ2 ⊢ e : τp ⇒ Γp′ above, we must have that ⃗ℓ ⊢WF τp ⇒ Γp′ . From
 ′′

x ̸∈ dom(Γp′ ) we must therefore have that [x ′ /x ] τp = τp and [x ′ /x ] Γp′ = Γp′ . As
Γp′ , τp ≤ Γ0′ , τ an application of T-Sub gives Θ | ⃗ℓ | Γ ′′ ⊢ [x ′ /x ]e : τ ⇒ Γ0′ . Then
Lemma 8 will give that Θ | ⃗ℓ | Γ ′′ ⊢ E [[x ′ /x ]e] : τn ⇒ Γn .
     As E andD the stack F⃗ remained unchanged,        E    combined with Equation (18) this
gives ⊢Dconf      H , R{x ′ 7→ v }, F⃗ , E [[x ′ /x ]e] as required. As the above argument
is used almost completely unchanged in all of the following cases, we will invert
the redex without regard for the T-Sub rule, with the understanding that the
subtyping rule is handled with an argument identical to the above.
      We now show that Θ | ⃗ℓ | Γ ′′ ⊢ [x ′ /x ]e : [x ′ /x ] τp ⇒[x ′ /x ] Γp′ and Cons (H , R{x ′ 7→
v }, Γ ′′ ). The first is easy to obtain using Lemma 10; from Cons (H , R, Γp ), we
have that ∀ x ∈ dom(Γp ).x ∈ dom(R), whereby from x ̸∈ dom(R) we have
x ′ ̸∈ dom(Γp ). It therefore remains to show Cons (H , R{x ′ 7→ v }, Γ ′′ ).
      To show SAT (H , R ′ , Γ ′′ ), it suffices to show that SATv(H , R ′ , R ′ (x ′ ), τ2 ) and
SATv(H , R ′ , H (R ′ (y)), τ ′′ ) (that SATv holds for all other variables z follows
from Γp (z ) = Γ ′′ (z ) and Lemmas 18 and 25). If τ1 is an integer type and r > 0,
then by the definition of the strengthening operator, the latter is equivalent to
show that SATv(H , R ′ , H (R ′ (y)), τ1 ) and that R ′ (x ′ ) = H (R ′ (y)) = H (R(y)),
which is immediate from the definition of R-Deref. If τ1 is not an integer or if
r = 0, then we must only show that SATv(H , R ′ , H (R ′ (y)), τ1 ).
      From Cons (H , R, Γp ), we know that SAT (H , R, Γp ), in particular, SATv(H , R, R(y), Γp (y)).
Then by Lemmas 17, 18 and 25, from R ⊑ R ′ , ⃗ℓ ⊢WF Γp , and SATv(H , R, v , τ1 +
τ2 ) we obtain that SATv(H , R ′ , v , τ1 ) and SATv(H , R ′ , v , τ2 ), where v =
H (R(y)). We thus have that SATv(H , R ′ , R ′ (x ′ ), τ2 ) and SATv(H , R ′ , H (R ′ (y)), τ1 )
are satisfied.
      We must also show that the ownership invariant is preserved. Then, it’s to
show ∀ a ∈ dom(H ).Own (H , R ′ , Γ ′′ )(a) ≤ 1. Define O0′ and O1′ as follows:

    Own (H , R, Γp ) = O0′ + own (H , R(y), Γp (y))
   Own (H , R ′ , Γ ′′ ) = O1′ + own (H , R ′ (y), Γ ′′ (y)) + own (H , R ′ (x ′ ), Γ ′′ (x ′ ))
                    O0′ = Σz ∈dom(Γp )\{y} own (H , R(z ), Γp (z ))
                    O1′ = Σz ∈dom(Γ ′′ )\{y,x ′ } own (H , R ′ (z ), Γ ′′ (z ))

Since R ′ agrees with R on all old variables and the corresponding types are
unchanged, O0′ = O1′ . Then it suffices to show that own (H , R(y), Γp (y)) =
own (H , R ′ (y), Γ ′′ (y)) + own (H , R ′ (x ′ ), Γ ′′ (x ′ )).
52       J. Toman et al.

     As R ′ (x ′ ) = H (R ′ (y)) = H (R(y)) and from the definition of Γ ′′ , we have:

            own (H , R ′ (x ′ ), Γ ′′ (x ′ )) = own (H , H (R(y)), τ2 )
             own (H , R ′ (y), Γ ′′ (y)) = {a 7→ r} + own (H , H (R(y)), τ1 )

From the definition of the ownership function, we have that

          own (H , R(y), Γp (y)) = {a 7→ r} + own (H , H (R(y)), τ1 + τ2 )

which, by Lemma 16, is equivalent to:

             {a 7→ r} + own (H , H (R(y)), τ1 ) + own (H , H (R(y)), τ2 )

We therefore have own (H , R(y), Γp (y)) = own (H , R ′ (y), Γ ′′ (y))+own (H , R ′ (x ′ ), Γ ′′ (x ′ )),
and conclude that Own (H , R, Γp ) = Own (H , R ′ , Γ ′′ ).
                         D                      E
Case R-Seq:       ⊢Dconf   H , R, F⃗ , E [x ; e]
                  D                      E        D            E
                    H , R, F⃗ , E [x ; e] −→D H , R, F⃗ , E [e]
By inversion (see R-Deref) we have for some Γ that:

                       Θ | ⃗ℓ | Γ [x : τ0 + τ1 ] ⊢ x : τ0 ⇒ Γ [x ←- τ1 ]
                       Θ | ⃗ℓ | Γ [x ←- τ1 ] ⊢ e : τ ′ ⇒ Γ ′
                       Cons (H , R, Γ )

We take Γ ′′ = Γ [x ←- τ1 ].
    It suffices to show (see R-Deref) that Θ | ⃗ℓ | Γ ′′ ⊢ e : τ ′ ⇒ Γ ′ , and
Cons (H , R, Γ ′′ ). The first is immediate from the inversion above, and Cons (H , R, Γ ′′ )
follows from Lemmas 16      D and 17.                       E
Case R-Let: ⊢D        conf   H , R, F⃗ , E [let x = y in e]
                    D                               E         D                                  E
                      H , R, F⃗ , E [let x = y in e] −→D H , R{x ′ 7→ R(y)}, F⃗ , E [[x ′ /x ]e]
                    x ′ ̸∈ dom(R)         R ′ = R{x ′ 7→ R(y)}
By inversion (see R-Deref) we have that for some Γ that:
            ⃗ℓ ⊢WF Γ
            Γ (y) = τ1 + τ2
            Θ | ⃗ℓ | Γ [y ←- τ1 ∧y y =τ1 x ], x : (τ2 ∧x x =τ2 y) ⊢ e : τ ⇒ Γ ′
            Cons (H , R, Γ )        x ̸∈ dom(Γ ′ )

We give Γ ′′ = Γ [y ←- τ1 ∧y y =τ1 x ′ ], x ′ : (τ2 ∧x ′ x ′ =τ2 y).
   It suffices to show (see R-Deref) that Θ | ⃗ℓ | Γ ′′ ⊢ [x ′ /x ]e : τ ⇒ Γ ′ and
Cons (H , R{x ′ 7→ R(y)}, Γ ′′ ). The first is easy to obtain using reasoning as in
the R-Deref case. It therefore remains to show Cons (H , R ′ , Γ ′′ ).
   To show that the output environment is consistent, we must show that
SATv(H , R ′ , R ′ (x ′ ), τ2 ∧x ′ x ′ =τ2 y) and SATv(H , R ′ , R ′ (y), τ1 ∧y y =τ1 x ′ ). By
       ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                             53

reasoning similar to that in R-Deref, it suffices to show that SATv(H , R ′ , R ′ (x ′ ), τ2 )
and SATv(H , R ′ , R ′ (y), τ1 ). We know that Cons (H , R, Γ ), from which we have
SAT (H , R, Γ ), in particular y ∈ dom(R) and SATv(H , R, R(y), Γ (y)). As R ⊑
R ′ and ⃗ℓ ⊢WF Γ , from Lemmas 17, 18 and 25, we obtain from SATv(H , R, v , τ1 +
τ2 ) that SATv(H , R ′ , v , τ1 ) and SATv(H , R ′ , v , τ2 ) where v = R(y). We then
have SATv(H , R ′ , R ′ (x ′ ), τ2 ) and SATv(H , R ′ , R ′ (y), τ1 ) are satisfied.
    We must also show that the ownership invariant is preserved. Then, it’s to
show ∀ a ∈ dom(H ).Own (H , R ′ , Γ ′′ )(a) ≤ 1. Define O0′ and O1′ as follows:

     Own (H , R, Γ ) = O0′ + own (H , R(y), Γ (y))
   Own (H , R ′ , Γ ′′ ) = O1′ + own (H , R ′ (y), Γ ′′ (y)) + own (H , R ′ (x ′ ), Γ ′′ (x ′ ))
                    O0′ = Σz ∈dom(Γ )\{y} own (H , R(z ), Γ (z ))
                    O1′ = Σz ∈dom(Γ ′′ )\{y,x ′ } own (H , R ′ (z ), Γ ′′ (z ))

Since R ′ agrees with R on old variables and their types are unchanged, O0′ = O1′
holds. That own (H , R ′ (x ′ ), τ2 ) + own (H , R ′ (y), τ1 ) = own (H , R(y), τ1 + τ2 )
follows immediately from Lemma 16 and the condition R(y) = R ′ (x ′ ) = R ′ (y).
We therefore conclude that Own (H , R, Γ ) = Own (H , R ′ , Γ ′′ ).
                            D                                E
Case R-LetInt: ⊢D              H  , R, ⃗ , E [let x = n in e]
                                       F
                      Dconf                           E        D                              E
                       H , R, F⃗ , E [let x = n in e] −→D H , R{x ′ 7→ n}, F⃗ , E [[x ′ /x ]e]

By inversion (see R-Deref) we have that, for some Γ :

                       Θ | ⃗ℓ | Γ, x : {ν : int | ν = n} ⊢ e : τ ⇒ Γ ′
                       Cons (H , R, Γ )         x ̸∈ dom(Γ ′ )

   We give that Γ ′′ = Γ, x ′ : {ν : int | ν = n}, and it thus suffices to show that
Θ | ⃗ℓ | Γ ′′ ⊢ [x ′ /x ]e : τ ⇒ Γ ′ and Cons (H , R{x ′ 7→ n}, Γ ′′ ). The first one is
easy to obtain using the Lemma 10 (see R-Deref) and the latter is trivial by
reasoning similar to the T-Let and T-Deref cases.
                                 D                                        E
Case R-IfTrue: ⊢D           conf   H , R, F⃗ , E [ifz y then e1 else e2 ]
                          D                                       E         D              E
                            H , R, F⃗ , E [ifz y then e1 else e2 ] −→D H , R, F⃗ , E [e1 ]

By inversion (see R-Deref) we have that for some Γ :

                   Γ (x ) = {ν : int | φ}
                   Θ | ⃗ℓ | Γ [x ←- {ν : int | φ ∧ ν = 0}] ⊢ e1 : τ ⇒ Γ ′
                   Cons (H , R, Γ )

We take Γ ′′ = Γ [x ←- {ν : int | φ ∧ ν = 0}], and want to show that Cons (H , R, Γ ′′ )
(that Θ | ⃗ℓ | Γ ′′ ⊢ e1 : τ ⇒ Γ ′ is immediate).
    By definition, from Cons (H , R, Γ ) we have SAT (H , R, Γ ), in particular
x ∈ dom(R), R(x ) ∈ Z and [R] [R(x )/ν]φ. The refinement predicates φ still holds
54       J. Toman et al.

in the output environment, since nothing changes in the register after transition.
Also from precondition of R-IfTrue, we have R(x ) = 0, thus x satisfies the
refinement that ν = 0. Thus [R] [R(x )/ν](φ ∧ ν = 0) is trivially satisfied.
Case R-IfFalse:
Similar to the case for R-IfTrue.
                            D                                       E
Case R-MkRef: ⊢D       conf   H , R, F⃗ , E [let x = mkref y in e]
                      D                                      E        D                        E
                       H , R, F⃗ , E [let x = mkref y in e] −→D H ′ , R ′ , F⃗ , E [[x ′ /x ]e]
                      a ̸∈ dom(H )         x ′ ̸∈ dom(R)
                         ′
                      H = H {a 7→ R(y)}             R ′ = R{x ′ 7→ a}
By inversion (see R-Deref) we have that for some Γ :

               ⃗ℓ ⊢WF Γ
               Γ (y) = τ1 + τ2
               Θ | ⃗ℓ | Γ [y ←- τ1 ], x : (τ2 ∧x x =τ2 y) ref 1 ⊢ e : τ ⇒ Γ ′
               Cons (H , R, Γ )          x ̸∈ dom(Γ ′ )

We give Γ ′′ = Γ [y ←- τ1 ], x ′ : (τ2 ∧x ′ x ′ =τ2 y) ref 1 , and must show that Θ | ⃗ℓ |
Γ ′′ ⊢ [x ′ /x ]e : τ ⇒ Γ ′ and Cons (H ′ , R ′ , Γ ′′ ). The first follows from Lemma 10
and the reasoning found in R-Deref, so it remains to show Cons (H ′ , R ′ , Γ ′′ ). To
show that the output environment is consistent, we must show that SATv(H ′ , R ′ , R ′ (x ′ ), (τ2 ∧x ′
x ′ =τ2 y) ref 1 ) and SATv(H ′ , R ′ , R ′ (y), τ1 ). By reasoning similar to that in
R-Deref, it suffices to show that SATv(H ′ , R ′ , R ′ (x ′ ), τ2 ref 1 ) and SATv(H ′ , R ′ , R ′ (y), τ1 ).
We know that Cons (H , R, Γ ), from which we have SAT (H , R, Γ ), in particular
y ∈ dom(R) and SATv(H , R, R(y), Γ (y)). As R ⊑ R ′ and ⃗ℓ ⊢WF Γ , from Lem-
mas 18 and 25, we have SATv(H , R, R(y), τ1 +τ2 ) implies SATv(H , R ′ , R ′ (y), τ1 +
τ2 ). By Lemma 26, we then have SATv(H ′ , R ′ , R(y), τ1 +τ2 ). Then by Lemma 17,
we have SATv(H ′ , R ′ , v , τ1 ) and SATv(H ′ , R ′ , v , τ2 ) where v = R(y). We then
have SATv(H ′ , R ′ , R ′ (x ′ ), τ2 ref 1 ) and SATv(H ′ , R ′ , R ′ (y), τ1 ) are satisfied.
     We must also show that the ownership invariant is preserved. Then, it’s
to show ∀ a ′ ∈ dom(H ′ ).Own (H ′ , R ′ , Γ ′′ )(a ′ ) ≤ 1. From Cons (H , R, Γ ) and
Lemmas 16 and 28 we have:

         Own (H ′ , R ′ , Γ ′′ ) = Σz ∈dom(Γ ′′ ) own (H ′ , R ′ (z ), Γ ′′ (z ))
                                = Σz ∈dom(Γ ) own (H , R(z ), Γ (z )) + {a 7→ 1}
                                = Own (H , R, Γ ) + {a 7→ 1}

   Since a ̸∈ dom(H ) and ∀ a ′ ∈ dom(H ).Own (H ′ , R, Γ )(a ′ ) ≤ 1, we have
∀ a ∈ dom(H ′ ).Own (H ′ , R ′ , Γ ′′ )(a ′ ) ≤ 1.
     ′
                           D                             E
Case R-Assign:     ⊢Dconf     H , R, F⃗ , E [y : = x ; e]
                   D                               E       D               E
                     H , R, F⃗ , E [y : = x ; e] −→D H ′ , R ′ , F⃗ , E [e]
                   a = R(y)               H ′ = H {a ←- R(x )}    R′ = R
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                    55

By inversion (see the R-Deref case) we have that

             Θ | ⃗ℓ | Γ [x : τ1 + τ2 ][y : τ ′ ref 1 ] ⊢ y : = x ; e : τ ⇒ Γ ′
             Θ | ⃗ℓ | Γ [x ←- τ1 ][y ←- (τ2 ∧y y =τ x ) ref 1 ] ⊢ e : τ ⇒ Γ ′
                                                     2
                            ′
             x ̸= y      Lτ M = Lτ2 M
             Cons (H , R, Γ ).

We give Γ ′′ = Γ [x ←- τ1 ][y ←- (τ2 ∧y y =τ2 x ) ref 1 ]. That Θ | ⃗ℓ | Γ ′′ ⊢ e : τ ⇒ Γ ′
is immediate.
     We must therefore show that Cons (H ′ , R ′ , Γ ′′ ). To show that the output
environment is consistent, we must show that SATv(H ′ , R, R(y), (τ2 ∧y y =τ2
x ) ref 1 ) and SATv(H ′ , R, R(x ), τ1 ). By reasoning similar to that in R-Deref,
it suffices to show that SATv(H ′ , R, R(y), τ2 ref 1 ) and SATv(H ′ , R, R(x ), τ1 ).
     From Cons (H , R, Γ ), we know that SAT (H , R, Γ ), in particular SATv(H , R, R(x ), τ1 +
τ2 ) and SATv(H , R, R(y), τ ′ ref 1 ). Since x ̸= y, Lemma 27 gives

        own (H , R(x ), τ1 + τ2 )(a) = 0      and    own (H , H (a), τ ′ )(a) = 0,

and also gives own (H , R(z ), Γ (z ))(a) = 0 for every other z ̸= y.
      By Lemmas 17 and 22, the old contents H (a) have shape Lτ ′ M and R(x ) has
shape Lτ2 M. These shapes are equal by the assignment premise, so Lemma 19
gives H ≈a H ′ . We may now apply Lemma 24 to the binding of x , and then
Lemma 17, to obtain SATv(H ′ , R, R(x ), τ1 ) and SATv(H ′ , R, R(x ), τ2 ). Since
H ′ (R(y)) = R(x ), the binding of y, including its equality refinement, is satisfied.
Every other binding is transported by Lemma 24 using the zero-ownership facts
above. Thus SAT (H ′ , R, Γ ′′ ) holds.
      It remains to show that the ownership bound is preserved. We retain the
decomposition used for the input and output ownership maps, and we define
O0′ , O0′′ , O1′ and O1′′ as below:

        Own (H , R, Γ ) = O0′ + O0′′
      Own (H ′ , R, Γ ′′ ) = O1′ + O1′′
                      O0′ = Σz ∈dom(Γ )\{y,x } own (H , R(z ), Γ (z ))
                      O0′′ = own (H , R(y), Γ (y)) + own (H , R(x ), Γ (x ))
                      O1′ = Σz ∈dom(Γ ′′ )\{y,x } own (H ′ , R(z ), Γ ′′ (z ))
                      O1′′ = own (H ′ , R(y), Γ ′′ (y)) + own (H ′ , R(x ), Γ ′′ (x ))

By the definition of the ownership function, Γ (y) = τ ′ ref 1 and Γ (x ) = τ1 + τ2 ,
we have:

        O0′′ = own (H , H (R(y)), τ ′ ) + {a 7→ 1} + own (H , R(x ), τ1 + τ2 )
        O1′′ = own (H ′ , H ′ (R(y)), τ2 ) + {a 7→ 1} + own (H ′ , R(x ), τ1 )

For every z ∈ dom(Γ ) \ {y, x }, full-reference exclusion gives zero ownership at a,
so Lemma 21 gives O0′ = O1′ . Then, from ∀ a ′ ∈ dom(H ).Own (H , R, Γ )(a ′ ) =
56       J. Toman et al.

O0′ (a ′ ) + O0′′ (a ′ ) ≤ 1, it suffices to show that O1′′ (a′ ) ≤ O0′′ (a′ ) for every a ′ ∈
dom(H ′ ).
     We first consider the case for a ′ = a:

       O1′′ (a) = own (H ′ , H ′ (R(y)), τ2 )(a) + own (H ′ , R(x ), τ1 )(a) + 1
       O0′′ (a) = own (H , R(x ), τ1 + τ2 )(a) + own (H , H (R(y)), τ ′ )(a) + 1.

The two nonconstant terms in O0′′ (a) are zero by Lemma 27. By Lemmas 16
and 21,

        own (H , R(x ), τ1 + τ2 ) = own (H ′ , R(x ), τ1 ) + own (H ′ , R(x ), τ2 ).

Since this map is zero at a, nonnegativity implies that both summands are zero
there. Using H ′ (R(y)) = R(x ), we therefore have O1′′ (a) = 1 = O0′′ (a).
   Next, consider a ′ ̸= a:

        O1′′ (a ′ ) = own (H ′ , H ′ (R(y)), τ2 )(a ′ ) + own (H ′ , R(x ), τ1 )(a ′ )
        O0′′ (a ′ ) = own (H , R(x ), τ1 + τ2 )(a ′ ) + own (H , H (R(y)), τ ′ )(a ′ ).

Again using Lemmas 16 and 21 and H ′ (R(y)) = R(x ), O1′′ (a ′ ) equals own (H , R(x ), τ1 +
τ2 )(a ′ ) ≤ own (H , R(x ), τ1 + τ2 )(a ′ ) + own (H , H (R(y)), τ ′ )(a ′ ). We therefore
conclude that ∀ a ′ ∈ dom(H ′ ).Own (H ′ , R, Γ ′′ )(a ′ ) ≤ 1.
                              D                                 E
Case R-Alias:          ⊢D      H  , R, F⃗ , E [alias(x = y) ; e]
                       Dconf                            E         D               E
                        H , R, F⃗ , E [alias(x = y) ; e] −→D H , R, F⃗ , E [e]
                       R(x ) = R(y)
By inversion (see R-Deref) we have for some Γ that:

            Θ | ⃗ℓ | Γ [x : τ1 ref r1 ][y : τ2 ref r2 ] ⊢ alias(x = y) ; e : τ ⇒ Γ ′
                                      ′                 ′
            Θ | ⃗ℓ | Γ [x ←- τ1′ ref r1 ][y ←- τ2′ ref r2 ] ⊢ e : τ ⇒ Γ ′
                                              ′            ′
            τ1 ref r1 +τ2 ref r2 ≈ τ1′ ref r1 +τ2′ ref r2
            x ̸= y
            Cons (H , R, Γ )
                                    ′                 ′
We give Γ ′′ = Γ [x ←- τ1′ ref r1 ][y ←- τ2′ ref r2 ], and must show Θ | ⃗ℓ | Γ ′′ ⊢ e :
τ ⇒ Γ ′ and Cons (H , R, Γ ′′ ). The first is immediate.
   To show Cons (H , R, Γ ′′ ) we first define:

                                        τp 1 =τ1 ref r1
                                        τp 2 =τ2 ref r2
                                                       ′
                                        τq 1 =τ1′ ref r1
                                                       ′
                                        τq 2 =τ2′ ref r2
                                         τq =τq 1 + τq 2
                                         τp =τp 1 + τp 2
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types                    57

We thus have τq ≈ τp .
    We know that Cons (H , R, Γ ), from which we have SAT (H , R, Γ ), in par-
ticular SATv(H , R, R(y), τ2 ref r2 ) and SATv(H , R, R(x ), τ1 ref r1 ). From τp 1 +
τp 2 = τp and Lemma 17, we have SATv(H , R, v , τp 1 ) and SATv(H , R, v , τp 2 )
imply SATv(H , R, v , τp ), where v = R(y) = R(x ). From τq ≈ τp and Lemma 14,
we have that SATv(H , R, v , τp ) implies SATv(H , R, v , τq ). From Lemma 17 we
also have that SATv(H , R, v , τq ) implies SATv(H , R, v , τq 1 ) and SATv(H , R, v , τq 2 ),
where again v = R(y) = R(x ).
    Then from the reasoning above, the refinements of τq 1 and τq 2 are valid and
SAT (H , R, Γ ′′ ) holds.
    We now show ∀ a ∈ dom(H ).Own (H , R, Γ ′′ )(a) ≤ 1. To prove that Own (H , R, Γ ) =
Own (H , R, Γ ′′ ) follows from:

               own (H , R(x ), τ1 ref r1 ) + own (H , R(y), τ2 ref r2 ) =
                                          ′                             ′
                 own (H , R(x ), τ1′ ref r1 ) + own (H , R(y), τ2′ ref r2 )
                                                                                   ′           ′
which follows immediately from the conditions τ1 ref r1 +τ2 ref r2 ≈ τ1′ ref r1 +τ2′ ref r2 ,
R(x ) = R(y), and Lemmas 15 and 16.
Case R-AliasPtr:
By reasoning similar to the R-Alias case.
Case R-AliasFail,R-AliasPtrFail:
The result configuration AliasFail is trivially well-typed.
                            D                               E
Case R-Assert:        ⊢D
                       conf   H , R, F⃗ , E [assert(φ) ; e]     Γ |= [R] φ
                      D                             E         D            E
                       H , R, F , E [assert(φ) ; e] −→D H , R, F⃗ , E [e]
                              ⃗

By inversion (see R-Deref) we can obtain Θ | ⃗ℓ | Γ ⊢ assert(φ) ; e : τ ⇒ Γ ′ and
Θ | ⃗ℓ | Γ ⊢ e : τ ⇒ Γ ′ , and the result follows immediately by taking Γ ′′ = Γ .
                                      D                               E
Case R-AssertFail:            ⊢Dconf    H , R, F⃗ , E [assert(φ) ; e]
                              D                               E
                                H , R, F⃗ , E [assert(φ) ; e] −→D AssertFail
                              Θ | ⃗ℓ | Γ ⊢ assert(φ) ; e : τ ⇒ Γ ′
By inversion (see the R-Deref case) we have that Γ |= φ, i.e., |= JΓ K =⇒ φ,
for some Γ such that Cons (H , R, Γ ). From Lemma 12 we therefore have |=
[R] JΓ K. From the precondition of R-AssertFail we have that ̸|= [R] φ. But
from |= JΓ K =⇒ φ and |= [R] JΓ K we can conclude that |= [R] φ, yielding a
contradiction. We therefore conclude that this case is impossible.
                         D                                                       E
Case R-Call: ⊢D     conf   H , R, F⃗ , E [let x = f ℓ (y1 , . . . , yn ) in e ′ ]
                  fD 7→ (x1 , .. , xn )e ∈ D                              E
                    H , R, F⃗ , E [let x = f ℓ (y1 , . . . , yn ) in e ′ ]
                             D                                                             E
                      −→D H , R, E [let x = []ℓ in e ′ ] : F⃗ , [y1 /x1 ] · · · [yn /xn ]e
58        J. Toman et al.
                                    D                                                                E
We must show that ⊢D
                   conf              H , R, E [let x = []ℓ in e ′ ] : F⃗ , [y1 /x1 ] · · · [yn /xn ]e for
some Γ ′′ .
   By inversion on the configuration typing, we have that, for some Γ :

                   Θ | ⃗ℓ | Γ ⊢ E [let x = f ℓ (y1 , . . . , yn ) in e ′ ] : τn ⇒ Γn .

By Lemma 7, we then have for some τ , and Γ ′ that:

                      Θ | ⃗ℓ | Γ ⊢ let x = f ℓ (y1 , . . . , yn ) in e ′ : τ ⇒ Γ ′
                      Θ | [] : τ ⇒ Γ ′ | ⃗ℓ ⊢ectx E : τn ⇒ Γn

Taking τ1 = τ, Γ1 = Γ ′ , Γ0 = Γ, Γ2 = Γn , τ2 = τn , by Lemma 31 we have, for
some τ ′′′ , Γ ′′′ :

                 Θ | ℓ : ⃗ℓ | Γ ⊢ σx e : τ ′′′ ⇒ Γ ′′′
                 Θ | [] : τ ′′′ ⇒ Γ ′′′ | ⃗ℓ ⊢ectx E [let x = []ℓ in e ′ ] : τn ⇒ Γn

where:

                   σx = [y1 /x1 ] · · · [yn /xn ]
                Θ(f ) = ∀λ. ⟨x1 : τi , . . . , xn : τn ⟩ → ⟨x1 : τ1′ , . . . , xn : τn′ | τp ⟩

We therefore take Γ ′′ = Γ .
   We must also prove that ∀i ∈ {1..n + 1} .Θ | [] : τi ⇒ Γi | ⃗ℓi−1 ⊢ectx Ei−1              ′
                                                                                                 :
                        ′                    ℓ       ′            ′
τi−1 ⇒ Γi−1 where En = E [let x = [] in e ] and Ei = Ei (0 ≤ i < n), which can be
divided into proving ∀i ∈ {1..n} .Θ | [] : τi ⇒ Γi | ⃗ℓi−1 ⊢ectx Ei−1            ′
                                                                                    : τi−1 ⇒ Γi−1
                                ⃗              ′
and Θ | []D : τn+1 ⇒ Γn+1 | ℓn ⊢ectx En : τn ⇒ Γn E              . The first follows by inversion
on ⊢Dconf  H , R, F⃗ , E [let x = f ℓ (y1 , . . . , yn ) in e ′ ] . To show the latter, we define
Γn+1 = Γ ′′′ and τn+1 = τ ′′′ , whereby the well-typing holds from the result of
applying Lemma 31 above.
   Finally, Cons (H , R, Γ ′′ ) follows immediately from Cons (H , R, Γ ) and Γ ′′ =
Γ.


D      Proof of Progress

We first state the standard decomposition lemma.
Lemma 32 (Decomposition). For any term e, either e = x for some x or
there exists some E and e ′ where E [e ′ ] = e and one of the following cases hold:

 1. e ′ = let x = mkref y in e ′′
 2. e ′ = let x = y in e ′′
 3. e ′ = let x = n in e ′′
 4. e ′ = let x = ∗y in e ′′
 5. e ′ = let x = f ℓ (y1 , . . . , yn ) in e ′′
      ConSORT: Context- and Flow-Sensitive Ownership Refinement Types            59

 6. e ′ = x ; e ′′
 7. e ′ = alias(x = y) ; e ′′
 8. e ′ = alias(x = ∗y) ; e ′′
 9. e ′ = ifz x then e1 else e2
10. e ′ = assert(φ) ; e ′′
11. e ′ = x : = y ; e

Proof. Straightforward induction on e.

Proof (Progress; Lemma 4). By inversion on ⊢D      conf C, either C = AliasFail or
     D             E
             ⃗
C = H , R, F , e . In the former case the result is immediate. In the latter case
we have that Θ | ⃗ℓ | Γ ⊢ e : τ ⇒ Γ ′ for some τ, Γ and Γ ′ , and further from
Lemma 32, we have that either e = x for some x or there exists some E or e ′
where e = E [e ′ ] and e ′ meets one of the cases in Lemma 32.
   In the case e = x , we further make case analysis on the form of F⃗ . The case
where F⃗ = ϵDis immediate; In                          ⃗       ⃗′
                                E the other case where F = F : F , the configuration
can step to H , R, F⃗ ′ , F [x ] according to R-Var.
   For the remaining cases where e = E [e ′ ], by the well-typing of e with respect
to Γ and Lemma 7, we have that Θ | ⃗ℓ | Γ ⊢ e ′ : τ0 ⇒ Γ0 some τ0 and Γ0 .
   We now treat the remaining forms of e ′
Case:      e ′ = let x = ∗y in e ′′
By inversion (Lemma 6) and Lemma 13 we must have that for some Γp where
Cons (H , R, Γp ) that y ∈ dom(Γp ) and Γp (y) = τ ′ ref r . From Cons (H , R, Γp )
                                                                 ′
we must have y ∈ dom(R) and further SATv(H , R, R(y), τ ′ ref r ), from which we
must have R(y) = a and a ∈ dom(H ). Then C can step according to R-Deref.
Case:      e ′ = let x = y in e ′′
Again, by Lemmas 6 and 13 and the definition of Cons, we must have that
y ∈ dom(R), and the system can step according to R-LetVar.
Case:      e ′ = let x = mkref y in e ′′
Similar to the R-LetVar case above.
Case:      e ′ = let x = n in e ′′
           e ′ = x ; e ′′
           e ′ = assert(φ) ; e ′′
The first two can trivially step according to R-LetInt and R-Seq, respectively.
The last can step according to R-Assert or R-AssertFalse (although by
Lemmas 2 and 3 the latter is impossible).
Case:      e ′ = alias(x = y) ; e ′′
Again by Lemmas 6 and 13 and that Cons (H , R, Γp ) implies x and y are bound
to addresses in the register file, we have that the configuration can step according
to R-Alias or R-AliasFail.
60      J. Toman et al.

Case:     e ′ = alias(x = ∗y) ; e ′′
Similar to the case above, we must have that x is bound to an address in the
register file, and that y is bound to an address that is itself mapped to an address
in the heap H . Then the configuration may step according to R-AliasPtr or
R-AliasPtrFail
Case:     e = ifz x then e1 else e2
As above, from the well-typing we must have that x is bound in R to some
integer n. Then the configuration may step according to R-IfTrue or R-IfFalse
depending on whether n = 0 or n ̸= 0.
Case:     e ′ = x : = y ; e ′′
From the well-typing of e ′ , Lemmas 6 and 13 and the definition of Cons, we
must have that y ∈ dom(R), x ∈ dom(R), R(x ) = a, and a ∈ dom(H ). Then
the configuration can step according R-Assign.
Case:     e ′ = let x = f ℓ (y1 , . . . , yn ) in e ′′
From the well-typing of the function call we must have that f ∈ dom(Θ). From
                                                                              ′′′
Θ ⊢ D in the precondition of ⊢D
                              conf C, we must have that f 7→ (x1 , .. , xj )e     ∈ D.
Then from T-FunDef we must have that j = n whereby the configuration can
step according to R-Call.
