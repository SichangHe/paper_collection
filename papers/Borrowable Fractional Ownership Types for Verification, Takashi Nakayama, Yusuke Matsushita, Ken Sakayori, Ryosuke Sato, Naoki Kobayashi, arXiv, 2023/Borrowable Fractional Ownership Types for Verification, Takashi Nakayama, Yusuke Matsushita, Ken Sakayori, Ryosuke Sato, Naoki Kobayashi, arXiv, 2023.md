                                               Borrowable Fractional Ownership Types for
                                                              Verification

                                         Takashi Nakayama1, Yusuke Matsushita1 , Ken Sakayori1, Ryosuke Sato1 , and
                                                                   Naoki Kobayashi1
arXiv:2310.20430v1 [cs.PL] 31 Oct 2023




                                                               The University of Tokyo, Tokyo, Japan
                                             {takashi-nakayama, yskm24t, sakayori, rsato, koba}@is.s.u-tokyo.ac.jp



                                                Abstract. Automated veriﬁcation of functional correctness of impera-
                                                tive programs with references (a.k.a. pointers) is challenging because of
                                                reference aliasing. Ownership types have recently been applied to address
                                                this issue, but the existing approaches were limited in that they are eﬀec-
                                                tive only for a class of programs whose reference usage follows a certain
                                                style. To relax the limitation, we combine the approaches of ConSORT
                                                (based on fractional ownership) and RustHorn (based on borrowable own-
                                                ership), two recent approaches to automated program veriﬁcation based
                                                on ownership types, and propose the notion of borrowable fractional own-
                                                ership types. We formalize a new type system based on the borrowable
                                                fractional ownership types and show how we can use it to automatically
                                                reduce the program veriﬁcation problem for imperative programs with
                                                references to that for functional programs without references. We also
                                                show the soundness of our type system and the translation, and conduct
                                                experiments to conﬁrm the eﬀectiveness of our approach.

                                                Keywords: Automated program veriﬁcation · Ownership types · Im-
                                                perative programs


                                         1     Introduction

                                         Various notions of ownership types have been used to prevent race conditions
                                         in concurrent programs and also to enable strong updates of knowledge in se-
                                         quential programs by controlling references (or pointers) aliases [5,7,28,4,12,8].
                                         Among others, Boyland [6] introduced fractional ownership (a.k.a. fractional
                                         permissions), where a fractional value in r0, 1s is associated with each reference
                                         and the full ownership (of 1) allows write access whereas a non-zero ownership
                                         allows read access. The Rust programming language [1,21] incorporates owner-
                                         ship with the borrow mechanism (which we call borrowable ownership), where
                                         ownership for a mutable reference can be borrowed during a specific lifetime, and
                                         the borrowed reference can be used for write access during the lifetime.
                                             Both notions of ownership (i.e., fractional ownership and borrowable own-
                                         ership) have recently been used for fully automated verification of the func-
                                         tional correctness of imperative programs [31,22,9,14,3,20]. Among them, Con-
                                         SORT [31] used fractional ownership to enable strong updates of refinement
2         T. Nakayama et al.

types for automated verification of the absence of assertion failures, whereas
RustHorn [22] used borrowable ownership to reduce assertion verification to
CHC solving. Although both approaches have been shown effective, they also
have unavoidable limitations: they are inadequate when a given program does
not follow a specific pattern of reference usage, i.e., when the type system con-
servatively rejects the program. Therefore, relaxing this limitation by extending
the expressive power of ownership type systems is essential for automated veri-
fication of imperative programs leveraging ownership types.

   In this paper, we propose the notion of borrowable fractional ownership, which
combines both approaches to extend the expressive power of ownership types
and develop a new method to verify the functional correctness of programs.
Hereafter, we first review the ideas of ConSORT and RustHorn, showing how
their ownership types work for automated verification, and then explain our new
approach.

    In ConSORT, each reference is given a type of the form τ ref r , where r,
called (fractional) ownership, ranges over r0, 1s, and τ is a refinement type that
describes the content of the reference. Additionally, a reference type should sat-
isfy the well-formedness that no refinement information (that is, only true) is
allowed for zero-ownership references. Fig. 1 shows an example program of Con-
SORT and how it is typed. The type of x on the first line shows that x is a
reference with full ownership, pointing to a cell holding the value 0. On the
second line, the aliasing reference y is created, and all the ownership has been
transferred to y, which deprives x of refinement information in its type. On the
third line, the type of y can be strongly updated, as y has the full ownership. The
alias command on the fourth line tells the type system that x and y are aliases;
based on that, the information on y is propagated to x, and the ownership of y
and its refinement information is redistributed between x and y. The fifth line
type-checks, as the types of x and y say that they both store 1. In this manner,
ConSORT uses fractional ownership to allow strong updates of refinement types
and share information among references based on alias annotations (which may
automatically be inserted by a separate pointer analysis).




    let x = mkref 0 in // x : tν : int | ν “ 0u ref 1
    let y = x in       // x : tν : int | trueu ref 0 , y : tν : int | ν “ 0u ref 1
    y := 1;            // x : tν : int | trueu ref 0 , y : tν : int | ν “ 1u ref 1
    alias(x = y);      // x : tν : int | ν “ 1u ref 0.5 , y : tν : int | ν “ 1u ref 0.5
    assert( *x + *y = 2 ) // ok


                         Fig. 1. A program example of ConSORT
                      Borrowable Fractional Ownership Types for Veriﬁcation          3

    let x = mkref 0 in // x : int ref α
    let y = x in       // y : int ref β ; x is invalidated during β
    y := 1;
    endlft β;          // dispose y; x : int ref α
    assert( *x = 1 )


                              Fig. 2. Typing in RustHorn


     On the other hand, the type system of RustHorn (which inherits that of Rust
1
  ) expresses the reference type as of the form τ ref α , where α is a lifetime, a
symbol representing an abstract time period during which the reference is valid.
In addition, the borrowed references are invalidated during the corresponding
lifetime in Rust. Fig. 2 shows a variation of the program in Fig. 1 and how it
is typed in the type system of RustHorn. On the first line, a reference x with
lifetime α is created. On the second line, y is created as an alias, and the (full)
ownership of x is borrowed to y during the lifetime β, which invalidates x. On the
third line, y can be safely updated as it has temporally borrowed ownership. On
the fourth line, the lifetime β ends, and the borrowed ownership is returned to x,
and thus x can be safely accessed on the fifth line. In reality, endlft commands
are automatically inserted by the Rust compiler.
     To verify the assertions, RustHorn uses the technique of prophecy [2,7,17]
to reduce the problem of verification to that of CHC solving. Here, for the sake
of clarity, we instead reduce them to the verification problem for functional
programs. In the reduction, a mutably borrowing reference y is modeled as a
pair of xv, y˝ y, where the first component v is the current value of the reference
y and the second component y˝ , called y’s prophecy, expresses the future value at
the end of y’s lifetime. For verification, the prophecy is encoded by standard non-
determinism. Fig. 3 shows how the translation works for the program in Fig. 2.
Notice that on the second line, the mutably borrowing reference y becomes a pair
of the current value (x) and the prophecy value initialized non-deterministically
(represented by _), then x takes the prophecy value of y on the third line. After
the value of y is changed on the fourth line, the assume command on the fifth
line, which is converted from endlft β in the original program, resolves the
prophecy value of y; in other words, the formally non-deterministic second value
of y is determined by the current value (1) so that x recover its correct value
and the last assertion succeeds. Note that this program has no references and is
easier to verify than the original one.
     As mentioned, both approaches have their limitations: ConSORT relies on
alias annotations and thus works effectively only for programs where exact
alias information is available statically (Fig. 4 shows one such program), and
RustHorn relies on Rust’s type system, hence is inapplicable to programs writ-
ten in other imperative languages like C.
1
    For formalization, RustHorn inherits the type system of λRust , a core calculus for
    Rust by Jung et al. [16].
4        T. Nakayama et al.

    let x = 0 in           // x “ 0
    let y = (x, _) in      // x “ 0, y “ x0, _y
    let x = snd y in       // x “ _, y “ x0, _y
    let y = (1, snd y) in // x “ _, y “ x1, _y
    assume(fst y = snd y); // x “ 1, y “ x1, 1y
    assert(x = 1) // ok


                Fig. 3. A pure functional program equivalent to Fig. 2



    In this paper, to overcome the limitations and take the best of both ap-
proaches, we introduce borrowable fractional ownership types. The type of a
reference is now of the form int ref α,r
                                      B , where α is the lifetime of the reference,
r is the (fractional) ownership of the reference ranging over r0, 1s, and B is the
borrowing information of the reference. A borrowing B is either a pair pβ, sq or
H, where β is the lifetime for which the reference lends the ownership and s
is the amount of (fractional) ownership others borrow from the reference. Our
type system extends those of both ConSORT and Rust ; for the sake of sim-
plicity, however, we consider only integer references, excluding nested reference
types like int ref α,r    β,s
                   B1 ref B2 . (We briefly discuss this in Section 7.) The reference
types of ConSORT can be considered a particular case where B is always H,
and all the lifetimes are identical.2 And those of Rust can be considered a par-
ticular case where the ownership r is always 0 or 1. 3 Fig. 4 shows an example
program that can be handled by neither ConSORT nor RustHorn but by our
new type system. (We will show how the program is typed in our type system
in Section 3.) Together with the type system, we develop a verification method
to prove the absence of assertion failures by a type-directed translation from
imperative programs with mutable references into stateless functional programs
without references, in a similar way to RustHorn.


    minmax(x, y) { if *x < *y then (x, y) else (y, x) }
    rand_choose(x, y) { if _ then x else y }
    let x = mkref _ in let y = mkref _ in
    let (p, q) = minmax(x, y) in
    let z = rand_choose(x, y) in
    assert( *p <= *z && *z <= *q );
    z := 1


Fig. 4. Example program that can be handled by neither ConSORT nor RustHorn but
by our method

2
  Unlike ConSORT, we do not have reﬁnement predicates because we follow the
  translation-based approach of RustHorn for veriﬁcation.
3
  This is not the case for shared (a.k.a. immutable) references in Rust, but our type
  system also subsumes these references.
                      Borrowable Fractional Ownership Types for Veriﬁcation              5

      Our main contributions are:
 1. Proposal of the new notion of borrowable fractional ownership.
 2. Formalization of a type system with borrowable fractional ownership and
    proof of the preservation of types and ownership invariants.
 3. Type-directed translation from imperative programs to functional programs
    without references, and proof of its soundness: if the target program has no
    assertion failures, neither does the source program.
   The rest of this paper is organized as follows. Section 2 introduces the source
language. Section 3 formalizes the type system with borrowable fractional own-
ership. Section 4 shows the reduction to stateless functional programs. Section 5
reports preliminary experimental results. Section 6 discusses related work and
Section 7 concludes the paper and discusses future work.


2      Source Language
This section introduces a simple imperative language with mutable references
and recursive functions with lifetime polymorphism, which serves as the target
of our type-based verification method.

2.1     Syntax
The syntax of the language is as follows:

                    o (arithmetic expressions) ::“ n | x | o1 op o2
    e (expressions) ::“ x | let x “ o in e | let x “ y in e
                       | let x “ mkref y in e | let x “ ‹y in e | x :“ y; e
                       | ifz x then e1 else e2 | let x “ f xÝ
                                                            Ñ
                                                            α ypy1 , . . . , yn q in e
                       | alias px “ yq; e | newlft α in e | endlft α; e | fail
                 d (function definitions) ::“ f ÞÑ xÝ
                                                    Ñ
                                                    α y px1 , . . . , xn qe
                         P (programs) ::“ xtd1 , . . . , dn u, ey

The meta-variables x, y, . . . range over the set Var of program variables, f ranges
over the set of function names, and α, β P LftVar range over a set of symbols
called lifetime variables.
    Program variables are introduced by function parameters or let bindings,
and the lifetime variables are bound by newlft. We assume that all program
and lifetime variables are alpha-renamed as necessary, so that each variable is
unique for each binder.
    For simplicity, an expression e is restricted to a de-nested, simplified form.
An arithmetic expression o consists of integer constants, integer variables, and
arithmetic binary operations (`, ´, etc.) denoted by op. The expression let x “
y in e creates a new alias x of y and evaluates e. We have primitives mkref y for
6       T. Nakayama et al.

creating a new reference, ‹y for reading from a reference, and x :“ y for updating
a reference. The conditional branch ifz x then e1 else e2 evaluates e1 if the
value of z is 0, and evaluates e2 otherwise. A function call f xÝ
                                                                Ñ
                                                                α ypy1 , . . . , yn q takes
                      Ñ
                      Ý
lifetime arguments α along with program arguments y1 , . . . , yn . The expression
fail aborts program execution with an error.
   An alias assumption alias px “ yq has been inherited from ConSORT[31]; it
assumes that x and y are aliasing references. This information is exploited by our
type system described in Section 3. Moreover, we inherit newlft α and endlft α,
which respectively introduces and eliminates a lifetime α, from λRust [16]. They
play essential roles in our type system but do not affect program execution.
   A function declaration d consists of the function name f , the parameter
variables x1 , . . . , xn , and the function body e. We allow mutual recursion between
functions. A program P is a pair xD, ey where D “ td1 , . . . , dn u is a set of
function definitions and e is the main expression.
   Henceforth, we write programs in an abbreviated, sugared style to avoid
unnecessary complications. For example, the program in Fig. 1 is a valid abbre-
viated program in our source language. Here, the expression assert pe1 “ e2 q is
syntactic sugar of plet c “ e1 ´ e2 in ifz c then 0 else failq.



2.2   Operational Semantics


We now introduce the operational semantics of our source language. Let Addr
be a countable set of heap addresses. We define a set of runtime values Valsrc
as Z Y Addr.
                                                                              Ñ
                                                                              Ý
                                                                       A          E
    A configuration (runtime state) of this language is a quadruple H, R, F , e ,
consisting of a heap, a register, a call stack, and a currently reducing expression.
A heap H is a partial function from Addr to Valsrc . A register R is a partial
                                               Ñ
                                               Ý
mapping from Var to Valsrc . A call stack F is a sequence of return contexts of
the form plet x “ rs in eq. A program xD, ey is executed by repeatedly stepping
from the initial configuration xH, H, ¨, ey according to the one-step reduction
relation ÝÑD , which is defined by the rules in Fig. 5. We write Hta ÞÑ vu for the
heap that maps the address a to v and behaves as H for the other addresses. We
also use a similar notation Rtx ÞÑ vu for registers. In (Rs-Arith), we write JoKR
for the computed integer value of o, where variables are interpreted according
to the register R. By (Rs-Fail), we fall into the ‘hard’ failure state Fail out of
fail. Also, by (Rs-AliasFail), in case the alias assumption alias px “ yq is not
satisfied, we fall into AliasFail, a ‘soft’ failure state distinct from Fail.
   The goal of our verification method is to check that a given program does not
reach Fail. To that end, we introduce a type system based on the new notion of
borrowable fractional ownership types in the next section and use it to reduce
the verification problem to that for functional programs in Section 4.
                             Borrowable Fractional Ownership Types for Veriﬁcation           7

                                                                             (Rs-Var)
                                       Ñ
                                       Ý               Ñ
                                                       Ý
        A                                   E   A                   E
            H, R, plet x1 “ rs in eq : F , x ÝÑD H, R, F , rx{x1 se

                        JoKR “ n   x1 R dompRq
                                                                             (Rs-Arith)
              Ñ
              Ý                                     Ñ
                                                    Ý
    A                           E    A                           E
        H, R, F , let x “ o in e ÝÑD H, Rtx1 ÞÑ nu, F , rx1 {xse

                             x1 R dompRq
                                                                                 (Rs-Let)
          Ñ
          Ý                                        Ñ
                                                   Ý
A                           E       A                           E
    H, R, F , let x “ y in e ÝÑD H, Rtx1 ÞÑ Rpyqu, F , rx1 {xse

             f ÞÑ xÝ
                   Ñα y px1 , . . . , xn qe P D        x1 R dompRq
                                                                                 (Rs-Call)
          Ý
          Ñ
A                                                      E
    H, R, F , let x “ f xÝÑ
                          α y py1 , . . . , yn q in e1
                                                     Ñ
                                                     Ý
           A                                                               E
    ÝÑD H, R, plet x1 “ rs in rx1 {xse1 q : F , ry1 {x1 s ¨ ¨ ¨ ryn {xn se

                            a R dompHq        x1 R dompRq
                                                                       (Rs-MkRef)
                           Ñ
                           Ý
                 A                                  E
                     H, R, F , let x “ mkref y in e
                                                       Ñ
                                                       Ý
                            A                                   E
                     ÝÑD Hta ÞÑ Rpyqu, Rtx1 ÞÑ au, F , rx1 {xse

                      Rpyq “ a
                            Hpaq “ v   x1 R dompRq
                                                                              (Rs-Deref)
           Ñ
           Ý                                      Ñ
                                                  Ý
A                             E      A                         E
     H, R, F , let x “ ‹y in e ÝÑD H, Rtx1 ÞÑ vu, F , rx1 {xse

                             Rpxq “ a   a P dompHq
                                                                        (Rs-Assign)
                       Ý
                       Ñ                                  Ñ
                                                          Ý
             A                      E   A                       E
                 H, R, F , x :“ y; e ÝÑD Hta ÞÑ Rpyqu, R, F , e

                                   Rpxq “ 0
                                                                          (Rs-IfTrue)
                   Ý
                   Ñ                                   Ñ
                                                       Ý
         A                                  E   A             E
             H, R, F , ifz x then e1 else e2 ÝÑD H, R, F , e1

                                  Rpxq ‰ 0
                                                                         (Rs-IfFalse)
                  Ý
                  Ñ                                   Ñ
                                                      Ý
        A                                  E   A             E
            H, R, F , ifz x then e1 else e2 ÝÑD H, R, F , e2

                                       Rpxq “ Rpyq
                                                                       (Rs-Alias)
                            Ý
                            Ñ                              Ñ
                                                           Ý
                  A                             E   A            E
                      H, R, F , alias px “ yq; e ÝÑD H, R, F , e

                                    Rpxq ‰ Rpyq
                                                                   (Rs-AliasFail)
                           Ý
                           Ñ
                 A                             E
                     H, R, F , alias px “ yq; e ÝÑD AliasFail

                                                                    (Rs-Newlft)
                           Ñ
                           Ý                           Ñ
                                                       Ý
                 A                          E   A            E
                     H, R, F , newlft α in e ÝÑD H, R, F , e

                                                                   (Rs-Endlft)
                               Ñ
                               Ý                         Ñ
                                                         Ý
                     A                        E   A            E
                         H, R, F , endlft α; e ÝÑD H, R, F , e

                                                           (Rs-Fail)
                                       Ñ
                                       Ý
                                A              E
                                 H, R, F , fail ÝÑD Fail


                      Fig. 5. Operational semantics of the source language
8        T. Nakayama et al.

3     Type System

In this section, we introduce our borrowable fractional ownership type system for
the source language. This type system will be used for the translation described
later in Section 4 to verify programs.


3.1    Syntax of Types

The syntax of types is given as follows:

                           τ (types) ::“ int | int ref α,r
                                                       B
                     r (ownership) P r0, 1s
                   B (borrowings) ::“ H | pα, rq
                σ (function types) ::“ @Ý
                                        Ñ
                                        α : L. xτ1 , . . . , τn y Ñ xτ 1 , . . . , τ 1 | τ y
                                                                            1        n
       L (lifetime environment) ::“ H | L, α1 ă α2
          Γ (type environment) ::“ H | Γ, x : τ

     Our type system has the integer type int and the reference type of integer
int ref α,rB , where α, r indicates that the reference has the lifetime α and the frac-
tional ownership r. The borrowing B specifies how much ownership is borrowed
by variables during which lifetime. If B “ H, no borrowing for other lifetime
occurred. Otherwise, B “ pβ, sq, which indicates that the reference is lending
ownership s to variables with lifetime β. For example, int ref α,0.5     β,0.5 is a reference
with the lifetime α that has the ownership of 0.5 and lends the ownership of 0.5
to other variables during the lifetime β.
     A lifetime environment L is a strict partial order on the set of valid lifetime
variables, each element of which is denoted α ă β. We impose the constraint
that when a reference type int ref α,r  β,s exists, the lifetimes α and β are ordered
β ă α under the lifetime environment L at the point. A type environment Γ is
a finite set of type bindings of the form x : τ .
     A function type σ takes the form @Ý     Ñα : L. xτ1 , . . . , τn y Ñ xτ11 , . . . , τn1 | τ y.
This indicates that the i-th argument has the type τi before the function call
and changes its type to τi1 when the function returns. In addition, the function
type has a direct return type τ . The function types are parameterized over
lifetime variables Ý Ñ
                     α with an ordering L, and the lifetime variables appearing in
τ, τi , τi must be included in Ý
         1                      Ñα.

Notations. Hereafter, we will identify the borrowing of pα, 0q with H and de-
note int ref α,r
             H by int ref
                          α,r
                              . Given a reference type τ “ int ref α,r
                                                                   B , we define
        def                    def                                                             def
Lftpτ q :“ α and Ownpτ q :“ r; Lftpintq is undefined and we define Ownpintq :“
0 for technical convenience. For x : τ P Γ , we write LftΓ pxq and OwnΓ pxq for
Lftpτ q and Ownpτ q, respectively.
                           Borrowable Fractional Ownership Types for Veriﬁcation                             9

                                                 (T-Var)                                            (T-Fail)
Θ | L | Γ ` Γ1 ` x:τ $ x:τ ⊲ L | Γ1                           Θ | L | Γ $ fail : τ ⊲ L1 | Γ 1

                               τ “ τx ` τy           x R dompΓ 1 q
                         Θ | L | Γ, x : τx , y : τy $ e : ρ ⊲ L1 | Γ 1
                                                                                   (T-Let)
                     Θ | L | Γ, y : τ $ let x “ y in e : ρ ⊲ L1 | Γ 1

      Γ $ o : int          Θ | L | Γ, x : int $ e : ρ ⊲ L1 | Γ 1               x R dompΓ 1 q
                                                                                                (T-Arith)
                                                                      1   1
                       Θ | L | Γ $ let x “ o in e : ρ ⊲ L | Γ

   Θ | L | Γ, x : int $ e1 : ρ ⊲ L1 | Γ 1             Θ | L | Γ, x : int $ e2 : ρ ⊲ L1 | Γ 1
                                                                                                    (T-If)
                Θ | L | Γ, x : int $ ifz x then e1 else e2 : ρ ⊲ L1 | Γ 1
             Ñ Ñ
             Ý               Ñ Ñ
                             Ý                     Ñ Ñ 1
                                                   Ý
        ρ “ r β {Ý
                 α sτ, ρi “ r β {Ý  α sτi , ρ1i “ r β {Ý α sτi                  x R dompΓ 1 q
                Ñ
                Ý                                                              Ñ Ñ
                                                                               Ý
      Θpf q “ @ α : M. xτ1 , . . . , τn y Ñ xτ1 , . . . , τn1 | τ y
                                                 1
                                                                              r β {Ý
                                                                                   α sM Ď L
              Θ | L | Γ, x : ρ, y1 : ρ11 , . . . , yn : ρ1n $ e : ξ ⊲ L1 | Γ 1
                                                                                                   (T-Call)
                                                      Ñ
                                                      Ý
 Θ | L | Γ, y1 : ρ1 , . . . , yn : ρn $ let x “ f x β ypy1 , . . . , yn q in e : ξ ⊲ L1 | Γ 1


                         Fig. 6. Typing rules for standard expressions


3.2     Typing Rules

The typing rules for expressions are defined in Figures 6, 8 and 9. A type judg-
ment for expressions is of the form Θ | L | Γ $ e : τ ⊲ L1 | Γ 1 where Θ, called a
function type environment, is a map from function names, ranging over by f , to
function types. The judgment indicates that an expression e is well-typed with
a type τ under the environments Θ, L, and Γ , and further that the lifetime and
type environments change to L1 and Γ 1 after evaluating e.
    We tacitly assume that every type judgment is well-formed. A type judgment
Θ | L | Γ $ e : τ ⊲ L1 | Γ 1 is well-formed if L $WF Γ , L1 $WF Γ 1 , and L $WF τ ,
which mean the type τ or every type used in Γ, Γ 1 should satisfy the order of the
corresponding lifetime environment, L or L1 , and every reference type int ref α,r
                                                                                 β,s
should satisfy r ` s ď 1. For example, if β ă α P L, then a type int ref β,r  α,s is
invalid because the smaller lifetime β lends ownership to the larger lifetime α.
(The necessity of the ordering is discussed in Remark 1.)
    We explain our type system using (T-Let) as a representative example. The
let expression allows an ownership transfer. The expression let x “ y in e is
well-typed only when the body e is typed under a type environment where x
and y have types τx and τy that are obtained as split of τ , which is the type y
originally had. The split expressed by the type addition τ “ τx ` τy (described
below) intuitively means that some portion of y’s ownership is passed to its new
alias x. The condition x R dompΓ 1 q ensures that x does not escape its scope.
    Type addition τ1 ` τ2 is an essential feature in this type system to handle the
ownership transfers. The type addition is defined by the rules in Fig. 7. The rules
(A-Share) and (A-Borrow) express ownership distribution between two aliasing
10        T. Nakayama et al.

                                             (A-Int)
                                                         τ1 “ τ2
                                                                      (A-Ex)
                         int “ int ` int                 τ2 “ τ1

                            r1 ` r2 ď 1        s1 ` s2 ď 1
                                                                        (A-Share)
                                1 `r2
                    int ref α,r                α,r1           α,r2
                            β,s1 `s2 “ int ref β,s1 ` int ref β,s2

                                                                     (A-Borrow)
                     int ref α,r`s
                             H     “ int ref α,r           β,s
                                             β,s ` int ref H



                                  Fig. 7. Type addition rules

       Θ | L | Γ, x : int ref α,1                    1
                              H , y : int $ e : ρ ⊲ L | Γ
                                                          1
                                                                     x R dompΓ 1 q
                                                                                     (T-MkRef)
             Θ | L | Γ, y : int $ let x “ mkref y in e : ρ ⊲ L1 | Γ 1

                 Θ | L | Γ, x : int, y : int ref α,r        1
                                                 B $ e : ρ⊲L | Γ
                                                                 1
                                                                                (T-Deref)
             Θ | L | Γ, y : int ref α,r                        1
                                    B $ let x “ ‹y in e : ρ ⊲ L | Γ
                                                                    1



              Θ | L | Γ, y : int $ e : ρ ⊲ L1 | Γ 1      OwnΓ pxq “ 1
                                                                               (T-Assign)
                     Θ | L | Γ, y : int $ x :“ y; e : ρ ⊲ L1 | Γ 1


                      Fig. 8. Typing rules for reference manipulations


references but are conceptually different. Sharing distributes ownership between
references of the same lifetime, whereas borrowing is done between references of
different lifetimes. For example, int ref α,1 “ int ref α,0.5
                                                        β,0.5 ` int ref
                                                                        β,0.5
                                                                              means
that a reference with lifetime α is lending half of its ownership to a reference
with lifetime β, where we have α ą β due to the well-formedness condition. Type
addition is extended to an operation on type environments, written Γ ` Γ 1 , in a
pointwise manner.4
    Since we believe that most of the rules in Fig. 6 are self-explanatory, we
only explain a few nontrivial points. In (T-Var), we allow some variables in the
initial type environment or part of their ownership to be discarded. This allows
us to meet the condition x1 R dompΓ 1 q that appears in rules such as (T-Let).
The premise Γ $ o : int in (T-Arith) expresses that each free variable x of
                                                                  Ñ Ñ
                                                                  Ý
an arithmetic expression o has type int in Γ . The condition r β {Ý   α sM Ď L in
(T-Call) means that the lifetime variables contained in the arguments’ types
must follow the function’s constraint M under the lifetime environment L. As
already explained, τi and τi1 of a function type represent how the type of the
arguments change by calling the function. Types of yi , therefore, need to match
τi and τi1 (up-to substitution) before and after the function call, respectively.
    Fig. 8 shows the typing rules for reference manipulations. A newly created
reference has the full ownership as expressed by x : int ref α,1H in the premise
of (T-MkRef). The rule (T-Assign) has the condition Ownpxq “ 1 to ensure
4
     If a variable x only appears in one of the type environment, say x P dompΓ q but
     x R dompΓ 1 q, pΓ ` Γ 1 qpxq is given as Γ pxq.
                        Borrowable Fractional Ownership Types for Veriﬁcation                11

                 τx ` τy “ int ref α,r
                                   B          int ref α,r
                                                      B “ ρx ` ρy

                     Θ | L | Γ, x : ρx , y : ρy $ e : ρ ⊲ L1 | Γ 1
                                                                            (T-Alias)
             Θ | L | Γ, x : τx , y : τy $ alias px “ yq; e : ρ ⊲ L1 | Γ 1

       Θ | M | Γ $ e : ρ ⊲ L1 | Γ 1       M “ L Y tαu               α “ min M
                                                                                (T-NewLft)
                                                           1    1
                   Θ | L | Γ $ newlft α in e : ρ ⊲ L | Γ

                Θ | LÒα | Γ Òα $ e : ρ ⊲ L1 | Γ 1        α “ min L
                                                                       (T-EndLft)
                     Θ | L | Γ $ endlft α; e : ρ ⊲ L1 | Γ 1


                        Fig. 9. Typing rules for ghost instructions


that only a reference with full ownership is updated. Dereferencing can be done
regardless of the ownership. 5
    The rule (T-Alias) allows us to transfer the ownership of references based on
alias information. Rules (T-NewLft) and (T-EndLft) are rules for lifetime in-
troduction and termination, which do not exist in the type system of ConSORT.
The expression newlft α in e is typed when e is typed under the lifetime en-
vironment M such that M “ L Y tαu and α “ min M, which mean that the
newly introduced lifetime variable α becomes a minimal lifetime in typing of e.
The operator Òα in (T-EndLft) removes all information concerning α from the
environment and gives back the ownership that references with lifetime α have
been borrowing. Concretely, Γ Òα is defined by
                                            #
               def                β,r   def   int ref β,r`s
                                                        H      pif B “ pα, sqq
         intÒα :“ int    int ref B Òα :“                β,r
                                              int ref B        potherwiseq
                                          #
               def                    def   Γ Òα               pif α “ Lftpτ qq
          HÒα :“ H      pΓ, x : τ qÒα :“
                                            Γ Òα , x : pτ Òα q pif α ‰ Lftpτ qq

whereas LÒα is the subposet induced by Lztαu. The premise α “ min L says
that we can only end a minimal lifetime. This ensures that only a lifetime with
which references are not lending their ownership can be ended.
     The typing rules for functions and programs are defined in Fig. 10.
     Here, the rule (T-Fundef) stipulates the contract that a function cannot have
free variables and should end all lifetimes introduced in the function body by
requiring L Ď Ý Ñα and setting L to both initial and ending lifetime context. The
rule (T-Prog) checks that all the function definitions and the main expression
are well-typed. It also checks that the main expression does not have any free
(lifetime) variables.
     Fig. 11 and Fig. 12 show the examples in Fig. 1 and Fig. 2 typed under our
type system, respectively. The typings are mostly the same as those of ConSORT
5
    If we want to disallow dereferencing references of ownership 0 we may add a premise
    r ą 0 to (T-Deref); it is a matter of preference.
12         T. Nakayama et al.

           Θpf q “ @Ý
                    Ñ
                    α : L. xτ1 , . . . , τn y Ñ xτ11 , . . . , τn1 | τ y      LĎÝ
                                                                                Ñ
                                                                                α
            Θ | L | x1 : τ1 , . . . , xn : τn $ e : τ ⊲ L | x1 : τ11 , . . . , xn : τn1
                                                                                          (T-FunDef)
                               Θ $ f ÞÑ xÝ
                                         Ñ
                                         α y px1 , . . . , xn qe

           Θ $ d1     ¨¨¨      Θ $ dn
           dompΘq “ domptd1 , . . . , dn uq       Θ |H|H$e:τ ⊲H|H
                                                                                            (T-Prog)
                                $ xtd1 , . . . , dn u, ey


                        Fig. 10. Typing rules for functions and programs


and RustHorn. The difference between Fig. 2 and Fig. 12 is that the reference
x is not simply invalidated by the type system like in Rust but given a type of
x : int ref α,0
            β,1 . This demonstrates that our type system can express the lending
references as a type, which is not possible in Rust. We will utilize this difference
in a later example. Additionally, it is noteworthy that the typing of Fig. 11 is
obtained just by giving the identical lifetime to both references. (Recall that
ConSORT can be seen as a specific case of our type system.)



     let x = mkref 0 in                                   let x = mkref 0 in
     // x : int ref α,1                                   // x : int ref α,1
     let y = x in                                         let y = x in
     // x : int ref α,0 , y : int ref α,1                 // x : int ref α,0
                                                                         β,1 , y : int ref
                                                                                           β,1

     y := 1;                                              y := 1;
     alias(x = y);                                        endlft β;
     // x : int ref α,0.5 , y : int ref α,0.5             // x : int ref α,1
     assert( *x + *y = 2 )                                assert( *x = 1 )


      Fig. 11. Typed example of Fig. 1                     Fig. 12. Typed example of Fig. 2


    Another example of typing is given in Fig. 13. This example is the program
in Fig. 4 typed under our type system (extended with pair types). This program
cannot be typed under ConSORT nor RustHorn (namely, Rust) because Con-
SORT cannot insert alias statements after the use of z since z is a dynamic
alias of either x or y, and in Rust, we cannot touch x or y after the creation
of p and q. Our type system can type this program by employing borrowing
information and expressing partially lending references as a type of int ref α,0.5
                                                                             β,0.5 .



3.3      Type Preservation

As usual, reduction preserves well-typedness, and, in our type system, well-
typedness ensures the ownership invariant of fractional types:
                        Borrowable Fractional Ownership Types for Veriﬁcation                13

                                     int ref α,1 , int ref α,1
                                       @                       D
    // Θpminmaxq “A@α, β : β ă α.
                         α,0.5           α,0.5
                                                                               DE
                                               | int ref β,0.5 , int ref β,0.5
                                                @
    //         Ñ int ref β,0.5 , int ref β,0.5
    minmax(x, y) { if *x < *y then (x,    A y) else (y, x) }             E
                                                    α,0.5           α,0.5
    // Θprand_chooseq “ @α, β : β ă α. int ref β,0.5      , int ref β,0.5
                 A                                         E
                                                     α,0.5
    //         Ñ int ref α,0 , int ref α,0 | int ref β,0.5
    rand_choose(x, y) { if _ then x else y }
    let x = mkref _ in                        // x : int ref α,1
    let y = mkref _ in                        // y : int ref α,1
    let (p, q) = minmax(x, y) in
                   α,0.5               α,0.5
    // x : int ref β,0.5 , y : int ref β,0.5 , p : int ref β,0.5 , q : int ref β,0.5
                                                                                     α,0.5
    let z = rand_choose(x, y) in // x : int ref α,0 , y : int ref α,0 , z : int ref β,0.5
    assert( *p <= *z && *z <= *q );
    endlft β;                                  // dispose p, q; z : int ref α,1
    z := 1


                             Fig. 13. Typed example of Fig. 4


                                                             Ñ
                                                             Ý
Theorem 1. Suppose that $ xD, ey and xH, H, ¨, ey ։D xH, R, F , e1 y. Then we
                  1       1   1                 1      1
have Θ | L | Γ $ e : τ ⊲ Lř| Γ for some Θ, Γ , Γ , L, L and τ . Moreover, for
any a P dompHq, we have xPVar;Rpxq“a OwnΓ pxq ď 1.                          \
                                                                            [

The proof of this theorem is given in Appendix A . In the theorem above, Θ, L1 ,
Γ 1 and τ are fixed, whereas L and Γ differ at each step of the execution.6 This is
because, along the execution, we may introduce or terminate lifetime variables
or change ownership of variables. What is important, however, is that Γ always
gives an assignment of ownership so that the sum of the ownerships of references
pointing to an address a does not exceed 1. This is a key property we exploit to
show the soundness of the translation introduced in the next section.

Remark 1. We introduced the lifetime ordering because Thm. 1 does not hold if
we have cyclic borrows. Fig. 14 shows an example of such programs.        \
                                                                          [



    let x = mkref 0 in // x : int ref α,1
    let y = x in       // x : int ref α,0
                                      β,1 , y : int ref
                                                        β,1
                                      β,0               α,1
    let z = y in       // y : int ref α,1 , z : int ref
    endlft β           // x : int ref α,1 , z : int ref α,1
    // ownership sum of x and z becomes 2


                     Fig. 14. An example where cyclic borrows occur



6
    Strictly speaking, L1 , Γ 1 and τ also changes when a function is called.
14        T. Nakayama et al.

4      Translation

This section introduces our translation from the source language into a standard
functional language with non-deterministic assignments but without references.
Our translation is mainly based on RustHorn [22]. We convert all references to
a pair of current and prophecy values as described in Section 1 and exploit the
prophecy technique when borrowings occur. Employing this translation, we can
verify that a well-typed program in the source language will not fail by checking
the safety of the translated program using existing verifiers that can efficiently
verify functional programs such as Why3 [10] or MoCHi [27].
    We first define our target language, then formulate translation rules, and
finally state its soundness.


4.1     Target Language

In this subsection, we introduce the target language of our translation.


Syntax The syntax of the target language is as follows:

                        o (arithmetic terms) ::“ n | x | o1 op o2
    t (terms) ::“ x | let x “ o in t | let x “ y in t | let x “ f py1 , . . . , yn q in t
                 | let x “ xy, zy in t | let x “ fst y in t | let x “ snd y in t
                 | let x “ _ in t | assume px “ yq; t | ifz x then t1 else t2 | fail
                     d (function definitions) ::“ f ÞÑ px1 , . . . , xn qt
                           P (programs) ::“ xtd1 , . . . , dn u, ty

We only describe the differences from the source language. First, this language
uses a non-deterministic value _, whose exact value is not determined until a
corresponding assume instruction appears. For example, in Fig. 15, x and y
can be any integer on their initialization. But after running the third and fourth
lines, we have x “ 3 and y “ 3. Once the value of a non-deterministic value
gets fixed, we can no longer change it. So if we add assume px “ 5q at the end
of this program, the program execution raises an error. Second, this language is
free of references (or lifetimes). We no longer handle the heap memory in the
operational semantics (described later), and thus, the verification problem for
the target language is much more tractable than that for the source language.
Third, the target language has pairs, created by xx, yy and decomposed by fst
and snd. Pairs will be used to model references using prophecy variables.


Operational Semantics We now introduce the operational semantics for our
target language. The set of runtime values Valtgt is defined recursively as follows:

                                 Valtgt Q v ::“ n | xv1 , v2 y
                           Borrowable Fractional Ownership Types for Veriﬁcation     15

  let x = _ in let y = _ in
  assume(x = y); assume(y = 3);
  // ‘assume(x = 5)’ here causes an error


                     Fig. 15. Example demonstrating non-determinism


                                                                           Ñ
                                                                           Ý
                                                                    A           E
      A configuration (runtime state) of this language has the form  D, S, F , t ,
                                                                         Ñ
                                                                         Ý
consisting of function definitions D, a set of registers S, a call stack F , and
the currently reducing term t. The main difference to the source language is
that a configuration has a set of registers S to handle the non-determinism.
Each register S P S is a partial mapping from Var to Valtgt . Important rules
of the operational semantics are given by the rules in Fig. 16; the rules for
other constructs are standard and are defined similarly to those for the source
language. (See Appendix B.1 for the complete definition.)


                               S 1 “ tStx ÞÑ Spyqu | S P Su
                                                                       (Rt-Let)
                              Ý
                              Ñ                              Ñ
                                                             Ý
                    A                           E     A            E
                        D, S, F , let x “ y in t ÝÑ D, S 1 , F , t

                       S 1 “ tStx ÞÑ nu | S P S, n P Zu
                                                                  (Rt-LetNondet)
                        Ñ
                        Ý                               Ñ
                                                        Ý
              A                           E      A           E
                  D, S, F , let x “ _ in t ÝÑ D, S 1 , F , t

                            S 1 “ tS P S | Spxq “ Spyqu
                                                                       (Rt-Assume)
                        Ñ
                        Ý                                 Ñ
                                                          Ý
              A                               E     A           E
                  D, S, F , assume px “ yq; t ÝÑ D, S 1 , F , t


            Fig. 16. Operational semantics of the target language (excerpt)




4.2     Translation Rules

Here, we define our type-directed translation. Fig. 17 shows some notable trans-
lation rules; the translation is almost homomorphic for the other constructs (see
Appendix B.2 for details). The translation relation is of the form L | Γ $ e : τ ñ
t, meaning that e is translated to t under the type environment Γ . Note that if
we ignore the “ñ t” part, the rules are essentially the same as the typing rules
given in Section 3. We omitted the function type environment and the resulting
environments “⊲L1 | Γ 1 ” for simplicity. These environments are not needed to
define the translation for the intraprocedual fragment of the source language. To
ease the presentation, we focus on this fragment in the rest of Section 4.
    As briefly explained, a reference x is translated into a pair xx, x˝ y, where the
first and the second elements (are supposed to) represent the current value of
16       T. Nakayama et al.

                    L | Γ, x : int ref α,1
                                       H , y : int $ e : ρ ñ t
                                                                                  (C-MkRef)
        L | Γ, y : int $ let x “ mkref y in e : ρ ñ let x “ xy, _y in t

             L | Γ, x : int, y : int ref α,r
                                         B $ e : ρ ñ t          rą0
                                                                                 (C-Deref-Pos)
      L | Γ, y : int ref α,r
                         B $ let x “ ‹y in e : ρ ñ let x “ fst y in t


                  L | Γ, x : int, y : int ref α,0
                                              B $ e : ρ ñ t
                                                                               (C-Deref-Zero)
       L | Γ, y : int ref α,0
                          B $ let x “ ‹y in e : ρ ñ let x “ _ in t

                     L|Γ $e:ρñt             OwnΓ pxq “ 1
                                                                         (C-Assign)
                L | Γ $ x :“ y; e : ρ ñ let x “ xy, snd xy in t

                  τx ` τy “ int ref α,r
                                    B       int ref α,r
                                                    B “ ρx ` ρy

              L | Γ, x : ρx , y : ρy $ e : ρ ñ t   t1 “ Tττxx ρ
                                                              ρy px, y, tq
                                                                 x

                                                                              (C-Alias)
                  L | Γ, x : τx , y : τy $ alias px “ yq; e : ρ ñ t1

     LÒα | Γ Òα $ e : ρ ñ t     α “ minpLq     Γ zΓ Òα “ tx1 , . . . , xn u
                                                                                      (C-EndLft)
        L | Γ $ endlft α; e : ρ ñ assume1ďiďn pfst xi “ snd xi q; t


                            Fig. 17. Translation rules (excerpt)



x and the future (or prophesized) value of x, respectively. We treat the future
value as if x has the value stored in x when x’s lifetime ends. To help readers
understand this idea, let us look at the rule (C-MkRef). A new reference created
by mkref y is translated to a pair xy, _y. The first element is y because the
current value stored in the reference is the value y is bound to. We set a non-
deterministic value for the second element because, at the time of creation, we
do not know what the value stored in this reference will be when its lifetime
ends. In other words, we randomly guess the future value. We check if the guess
was correct by confirming whether the first and second elements of the pair
coincide when we drop this reference. These checks are conducted by inserting
assume pfst xi “ snd xi q that is obtained by translating endlft α as expressed
in the rule (C-EndLft). Here, xi is a variable with the lifetime α.
    Our translation obeys the following two principles:

 – Trustable XOR Zero (TXZ): If a reference x has non-zero ownership, then
   the first element of the translation of x indeed holds the current value.
 – Prophecy for Zero (PFZ): The translation of a reference with zero ownership
   holds a prophesized value of a borrowing reference.

    TXZ resembles ConSORT’s idea that only a type with non-zero ownership
can have a non-trivial refinement predicate. The fact that we do not trust a
reference with zero ownership is reflected in the rule (C-Deref-Zero), where
dereferencing is translated into an assignment of a non-deterministic value. TXZ
enables us to express an update of a reference with full ownership as an update
                     Borrowable Fractional Ownership Types for Veriﬁcation       17

of the first element of the pair as in (C-Assign). (Note that, by Thm. 1, aliases
of a reference with ownership 1 must have ownership 0.)
    PFZ is the core of the RustHorn-style prophecy technique. A reference of
ownership 0 can regain some ownership in two ways: by retrieving the lending
ownership through endlft or by ownership transfer through alias annotations.
PFZ handles the former case. (How the latter is handled will be explained below.)
Suppose a reference x is lending its ownership to y. PFZ says that fst x “
snd y in the translated program. When the lifetime of y ends, in the translated
program, the current value of y must equal the prophesized value because of
assume pfst y “ snd yq. Hence, at this moment, we have fst x “ snd y “ fst y,
which means that x also holds the correct value. Therefore, TXZ is not violated
when the ownership of x becomes non-zero.
    We now explain the rule (C-Alias), which is the key rule to understand
how our translation deals with ownership transfers. The rule (C-Alias) uses an
auxiliary function Tττyxρ
                        ρx
                          y
                            px, y, tq defined as follows:
                        $
                        ’
                        ’ t                             pOwnpτx q “ Ownpρx q “ 0q
                        ’
                        ’                               ˆ                       ˙
                        ’
                        ’                                    Ownpτy q
                        ’ let x “ xfst y, snd xy in t                        ą0
                                                         Ownpρx q, Ownpρy q
                        ’
                        ’
                        ’
                        ’
                        ¨
                        &
                    def
Tττyx ρ
      ρx
          px, y, tq :“      let y “ xfst x, snd yy in   ˜
                                                          Ownpτx q ą 0
                                                                       ¸
        y
                            let x “ xsnd y, snd xy in        and
                        ˚
                        ’
                        ’
                        ˝
                        ’
                                                          Ownpρx q “ 0
                        ’
                        ’
                        ’
                        ’
                        ’
                        ’   t
                        ’
                        % τy ρy
                        ’
                          Tτx ρx py, x, tq             potherwiseq

The essential case is when Ownpτx q ą 0 and Ownpρx q “ 0, that is, when y takes
all the ownership of x. In this case, x takes the future value of y to obey PFZ. At
the same time, to ensure TXZ, y takes the old value of x so that y has the correct
value. (Note that Ownpτy q, the previous ownership of y, can be zero.) Similarly,
when Ownpτy q, Ownpρx q, Ownpρy q ą 0, the value y holds is passed to x to
ensure TXZ (Ownpρy q ą 0 is necessary to avoid case overlapping.) Fig. 18 and
Fig. 19 show the translated example of Fig. 11 and Fig. 12.



  let x = (0, _) in                         let x = (0, _) in
  let y = (fst x, _) in                     let y = (fst x, _) in
  let x = (snd y, snd x) in                 let x = (snd y, snd x) in
  let y = (fst y + 1, snd y) in             let y = (1, snd y) in
  let x = (fst y, snd x) in                 assume(fst y = snd y);
  assert(fst x + fst y = 2)                 assert(fst x = 1)


 Fig. 18. Translated example of Fig. 11 Fig. 19. Translated example of Fig. 12
18        T. Nakayama et al.

Remark 2 (Difference from RustHorn). The main difference between our trans-
lation and RustHorn’s method is that our method converts all references to
pairs, whereas RustHorn only converts mutably borrowing references. This gap
emerges because our type system enables an immutable reference to recover its
ownership by alias; meanwhile, in Rust, once a mutable reference becomes im-
mutable, it cannot be changed to mutable. Note that in Fig. 19, both references
x and y become pairs unlike in RustHorn (Fig. 3).


4.3     Soundness
Our translation is sound, that is, if the translated program does not reach Fail
neither does the original program.
    As we are considering the intraprocedual fragment, we omit the stacks from
configurations. For clarity, we write the reduction in the source language and the
                               src                            tgt
target language as xH, R, ey ÝÝÑ xH 1 , R1 , e1 y and xS, ty ÝÝÑ xS 1 , t1 y, respectively.

Theorem 2 (Soundness of the translation). Assume H | H $ e : τ ñ t
              tgt                       src
and xtHu, ty ÝXÝÑ
                Ñ Fail, then xH, H, ey ÝXÝÑ
                                          Ñ Fail holds.

We briefly explain the proof strategy below; the proof is given in Appendix C .
                                    sim
We define an (indexed) simulation ùL,Γ between the configurations of the two
                                          sim
languages. The relation xH, R, ey ùL,Γ xS, ty not only requires L | Γ $ e : τ ñ
t to hold, but also requires that TXZ and PFZ hold; without them the relation
                                                             src
is too weak to be an invariant. Whenever xH, R, ey ÝÝÑ xH 1 , R1 , e1 y we show that
                                           tgt                                  sim
there exists xS 1 , t1 y such that xS, ty ÝÝÑÑ xS 1 , t1 y and xH 1 , R1 , e1 y ùL1 ,Γ 1 xS 1 , t1 y
            1  1
for some L , Γ . Such environments can be chosen by an argument identical to
the proof of type preservation (Thm. 1).


5      Preliminary Experiments

We conducted preliminary experiments to evaluate the effectiveness of our trans-
lation. In this experiment, we first typed the benchmark programs and translated
them into OCaml programs by hand7 (with slight optimizations). After that, we
measured the time of the safety verification of the translated programs using
MoCHi [27], a fully-automated verifier for OCaml programs. The experiments
were conducted on a machine with AMD Ryzen 7 5700G 3.80 GHz CPU and
32GB RAM. We used MoCHi of build a3c7bb9d as frontend solver, which used
Z3 [23] (version 4.11.2) and HorSat2 [19] (version 0.95) as backend solvers.
    We ran experiments on small but representative programs with mutable refer-
ences and summerized the results in Table 1. Columns ‘program’ and ‘safety’ are
the name of programs and whether they involve fail in assertions, respectively.
When two programs have the same name but different safeties, they represent
7
     This translation process can be automated if we require programmers to provide
     type annotations or if the type inference mentioned in Section 7 is worked out.
                    Borrowable Fractional Ownership Types for Veriﬁcation        19

slightly modified variations of a single program with different safety. Columns
‘ConSORT?’ and ‘RustHorn?’ indicate that the program can be typed by Con-
SORT or RustHorn, respectively. Columns Bo and Bt are the byte counts of the
original and translated programs, respectively. The column ‘time(sec)’ shows how
many seconds MoCHi takes to verify translated programs. These results show
that our method works in practical time for representative programs, though it
increases the program size by 2 to 4 by translation.
    Below, we describe each benchmark briefly. ‘consort-demo,’ ‘rusthorn-demo,’
and ‘minmax’ are the sample programs in Figures 1, 2 and 4. ‘simple-loop’ and
‘shuffle-in-call’, both included in ConSORT’s benchmark, are the programs uti-
lizing fractional ownership. ‘just-rec’ and ‘inc-max’ are from RustHorn, which
exploits borrowable ownership. ‘linger-dec’ is the program with loop and dy-
namic allocating of references and adopted by both ConSORT and RustHorn
benchmark. ‘hhk2008’ is a SeaHorn [13] test to check whether the verifier can
find an invariant on the loop. See Appendix D for benchmark programs.


                         Table 1. Experimental results

     program    safety ConSORT?     RustHorn?    Bo      Bt Bt {Bo   time(sec)
  consort-demo safe        X            ˆ        76      285 3.75      ă 0.1
 rusthorn-demo safe        X            X        68      276 4.06       0.8
 borrow-merge safe         ˆ            ˆ        216     756 3.5        1.0
                 safe                            194     347 1.79      ă 0.1
   simple-loop             X            X
                unsafe                           150     320 2.13       0.2
                 safe                            156     362 2.32       0.6
      just-rec             X            X
                unsafe                           157     372 2.37       0.2
                 safe                            121     395 3.26       0.8
  shuﬄe-in-call            X            ˆ
                unsafe                           121     395 3.26       0.2
                 safe                            143     550 3.85       1.2
     inc-max               ˆ            X
                unsafe                           143     549 3.84       0.4
                 safe                            251     920 3.67       0.2
     minmax                ˆ            ˆ
                unsafe                           251     920 3.67       0.6
                 safe                            239     836 3.5        1.1
    linger-dec             X            X
                unsafe                           243     841 3.46       0.3
     hhk2008     safe      X            X        321     630 1.96       2.7




6   Related Work
As introduced in Section 1, ConSORT [31] and RustHorn [22] are the direct
ancestor of this work. We have combined the two approaches as borrowable
fractional ownership types.
    Creusot [9] and Aeneas [14] are verification toolchains for Rust programs
based on a translation to functional programs. Creusot removes references and
translates Rust programs to Why3 [10] programs using RustHorn’s prophecy
20      T. Nakayama et al.

technique. Our translation is closer to that of Creusot than that of RustHorn
in that the target is a functional program rather than CHCs. But very unlike
Creusot, our translation accommodates the ConSORT-style fractional own-
ership and alias annotations. Aeneas uses a different encoding to translate
Rust programs to pure functional programs for interactive verification (in Coq,
F*, etc.). However, they can’t support advanced patterns like nested borrow-
ing because their model of a mutable reference is not a first-class value, unlike
RustHorn’s prophecy-based approach.
    There are other verification methods and tools that utilize some notion of
ownership for imperative program verification, such as Steel [11,30], Viper [24],
and RefinedC [26]. Still, their approaches and design goals are quite different
from ours in that they do semi-automated program verification in F* or low-level
separation logic, requiring more user intervention, such as annotations of loop
invariants and low-level proof hints about ownership.
    SeaHorn [13] and JayHorn [18] both introduce a fully automated verification
framework for programs with mutable references. SeaHorn is for LLVM-based
languages (C, C++, Rust, etc.) and JayHorn is for Java. Both do not use
ownership types but model the heap memory directly as a finite array. As a
result, they are ineffective or imprecise for programs with dynamic memory
allocation, as shown in the experiments of ConSORT and RustHorn.
    The work by Suenaga and Kobayashi [29] and Cyclone [15] used ownership
types to ensure memory safety for a language with explicit memory deallocation.
We expect that our borrowable fractional ownership types can also be used to
improve their methods.


7    Conclusion and Future Work

We have presented a type system based on the new notion of borrowable frac-
tional ownership, and a type-directed translation to reduce the verification of
imperative programs to that of programs without mutable references. Our ap-
proach combines that of ConSORT [31] and RustHorn[22], enabling automated
verification of a larger class of programs.
    Future work includes automated type inference and an extension of the type
system to allow nested references. Type inference would not be so difficult if
we assume some lifetime annotations as in Rust. Concerning nested references,
as a naive extension of reference types from int ref α,r             α,r
                                                         B to τ ref B seems too
restrictive, we plan to introduce a reference type of the form ξzτ {ρ ref α,r
                                                                          β,s , where
ξ is the borrowing type, τ is the current content type, and ρ is the lending type
to others. The point is that, instead of just keeping the amount of ownership
being borrowed, we should keep in what type a reference is being borrowed.


Acknowledgements We would like to thank anonymous referees for their use-
ful comments. This work was supported by JSPS KAKENHI Grant Number
JP20H05703 and JP22KJ0561.
                      Borrowable Fractional Ownership Types for Veriﬁcation          21

References
 1. Rust, https://www.rust-lang.org/, accessed: 2023-8-20
 2. Abadi,     M.,   Lamport,      L.:    The    existence     of  reﬁnement      map-
    pings. Theoretical computer science 82(2), 253–284 (May 1991).
    https://doi.org/10.1016/0304-3975(91)90224-P
 3. Astrauskas, V., Bílý, A., Fiala, J., Grannan, Z., Matheja, C., Müller, P., Poli, F.,
    Summers, A.J.: The Prusti project: Formal veriﬁcation for Rust. In: NASA Formal
    Methods: 14th International Symposium, NFM 2022, Pasadena, CA, USA, May
    24–27, 2022, Proceedings. pp. 88–108. Springer-Verlag, Berlin, Heidelberg (May
    2022). https://doi.org/10.1007/978-3-031-06773-0_5
 4. Bao, Y., Wei, G., Bračevac, O., Jiang, Y., He, Q., Rompf, T.: Reach-
    ability types: Tracking aliasing and separation in higher-order functional
    programs. Proc. ACM Program. Lang. 5(OOPSLA), 1–32 (Oct 2021).
    https://doi.org/10.1145/3485516
 5. Boyapati, C., Lee, R., Rinard, M.: Ownership types for safe programming: Pre-
    venting data races and deadlocks. In: Proceedings of the 17th ACM SIGPLAN
    conference on Object-oriented programming, systems, languages, and applications.
    pp. 211–230. OOPSLA ’02, Association for Computing Machinery, New York, NY,
    USA (Nov 2002). https://doi.org/10.1145/582419.582440
 6. Boyland, J.: Checking interference with fractional permissions. In:
    Static    Analysis.   pp.    55–72.     Springer    Berlin    Heidelberg    (2003).
    https://doi.org/10.1007/3-540-44898-5_4
 7. Calcagno, C., Parkinson, M., Vafeiadis, V.: Modular safety checking for Fine-
    Grained concurrency. In: Static Analysis. pp. 233–248. Springer Berlin Heidelberg
    (2007). https://doi.org/10.1007/978-3-540-74061-2_15
 8. Crichton, W., Patrignani, M., Agrawala, M., Hanrahan, P.: Modular information
    ﬂow through ownership. In: Proceedings of the 43rd ACM SIGPLAN International
    Conference on Programming Language Design and Implementation. ACM, New
    York, NY, USA (Jun 2022). https://doi.org/10.1145/3519939.3523445
 9. Denis, X., Jourdan, J.H., Marché, C.: Creusot: A foundry for the deductive ver-
    iﬁcation of Rust programs. In: Formal Methods and Software Engineering: 23rd
    International Conference on Formal Engineering Methods, ICFEM 2022, Madrid,
    Spain, October 24–27, 2022, Proceedings. pp. 90–105. Springer-Verlag, Berlin, Hei-
    delberg (Oct 2022). https://doi.org/10.1007/978-3-031-17244-1_6
10. Filliâtre, J.C., Paskevich, A.: Why3 — where programs meet provers.
    In: Programming Languages and Systems, pp. 125–128. Lecture notes in
    computer science, Springer Berlin Heidelberg, Berlin, Heidelberg (2013).
    https://doi.org/10.1007/978-3-642-37036-6_8
11. Fromherz, A., Rastogi, A., Swamy, N., Gibson, S., Martínez, G., Merigoux, D., Ra-
    mananandro, T.: Steel: Proof-oriented programming in a dependently typed con-
    current separation logic. Proc. ACM Program. Lang. 5(ICFP), 1–30 (Aug 2021).
    https://doi.org/10.1145/3473590
12. Gäher, L., Sammler, M., Spies, S., Jung, R., Dang, H.H., Krebbers, R., Kang,
    J., Dreyer, D.: Simuliris: A separation logic framework for verifying concurrent
    program optimizations. Proc. ACM Program. Lang. 6(POPL), 1–31 (Jan 2022).
    https://doi.org/10.1145/3498689
13. Gurﬁnkel, A., Kahsai, T., Komuravelli, A., Navas, J.A.: The SeaHorn veriﬁcation
    framework. In: Computer Aided Veriﬁcation. pp. 343–361. Springer International
    Publishing (2015). https://doi.org/10.1007/978-3-319-21690-4_20
22      T. Nakayama et al.

14. Ho, S., Protzenko, J.: Aeneas: Rust veriﬁcation by functional trans-
    lation. Proc. ACM Program. Lang. 6(ICFP), 711–741 (Aug 2022).
    https://doi.org/10.1145/3547647
15. Jim, T., Morrisett, J.G., Grossman, D., Hicks, M.W., Cheney, J., Wang, Y.: Cy-
    clone: A safe dialect of C. In: Proceedings of the General Track of the Annual
    Conference on USENIX Annual Technical Conference. pp. 275–288. ATEC ’02,
    USENIX Association, USA (2002)
16. Jung, R., Jourdan, J.H., Krebbers, R., Dreyer, D.: RustBelt: Securing the founda-
    tions of the Rust programming language. Proc. ACM Program. Lang. 2(POPL),
    1–34 (Dec 2017). https://doi.org/10.1145/3158154
17. Jung, R., Lepigre, R., Parthasarathy, G., Rapoport, M., Timany, A., Dreyer, D.,
    Jacobs, B.: The future is ours: Prophecy variables in separation logic. Proc. ACM
    Program. Lang. 4(POPL), 1–32 (Dec 2019). https://doi.org/10.1145/3371113
18. Kahsai, T., Rümmer, P., Sanchez, H., Schäf, M.: JayHorn: A framework for verify-
    ing Java programs. In: Computer Aided Veriﬁcation. pp. 352–358. Springer Inter-
    national Publishing (2016). https://doi.org/10.1007/978-3-319-41528-4_19
19. Kobayashi, N.: HorSat2: A saturation-based higher-order model checker (2015),
    http://www-kb.is.s.u-tokyo.ac.jp/~koba/horsat2, accessed: 2023-9-06
20. Lehmann, N., Geller, A.T., Vazou, N., Jhala, R.: Flux: Liquid types
    for Rust. Proc. ACM Program. Lang. 7(PLDI), 1533–1557 (Jun 2023).
    https://doi.org/10.1145/3591283
21. Matsakis, N.D., Klock, F.S.: The Rust language. In: Proceedings of the 2014 ACM
    SIGAda annual conference on High integrity language technology. pp. 103–104.
    HILT ’14, Association for Computing Machinery, New York, NY, USA (Oct 2014).
    https://doi.org/10.1145/2663171.2663188
22. Matsushita, Y., Tsukada, T., Kobayashi, N.: RustHorn: CHC-based veriﬁcation for
    Rust programs. ACM transactions on programming languages and systems 43(4),
    1–54 (Dec 2021). https://doi.org/10.1145/3462205
23. de Moura, L., Bjørner, N.: Z3: An eﬃcient SMT solver. In: Ramakrishnan,
    C.R., Rehof, J. (eds.) Tools and Algorithms for the Construction and Analysis
    of Systems. pp. 337–340. Springer Berlin Heidelberg, Berlin, Heidelberg (2008).
    https://doi.org/10.1007/978-3-540-78800-3_24
24. Müller, P., Schwerhoﬀ, M., Summers, A.J.: Viper: A veriﬁcation infras-
    tructure for permission-based reasoning. In: Veriﬁcation, Model Checking,
    and Abstract Interpretation. pp. 41–62. Springer Berlin Heidelberg (2016).
    https://doi.org/10.1007/978-3-662-49122-5_2
25. Nakayama, T., Matsushita, Y., Sato, R., Sakayori, K., Kobayashi, N.: Borrowable
    Fractional Ownership Types for Veriﬁcation (2023)
26. Sammler, M., Lepigre, R., Krebbers, R., Memarian, K., Dreyer, D., Garg, D.: Re-
    ﬁnedC: Automating the foundational veriﬁcation of C code with reﬁned ownership
    types. In: Proceedings of the 42nd ACM SIGPLAN International Conference on
    Programming Language Design and Implementation. ACM, New York, NY, USA
    (Jun 2021). https://doi.org/10.1145/3453483.3454036
27. Sato,      R.,    Unno,      H.,     Kobayashi,      N.:     MoCHi:        Software
    model       checker      for     a     higher-order      functional       language,
    http://www.kb.is.s.u-tokyo.ac.jp/~ryosuke/papers/ml2012.pdf, accessed:
    2023-08-03
28. Sergey, I., Clarke, D.: Gradual ownership types. In: Programming Lan-
    guages and Systems. pp. 579–599. Springer Berlin Heidelberg (2012).
    https://doi.org/10.1007/978-3-642-28869-2_29
                    Borrowable Fractional Ownership Types for Veriﬁcation      23

29. Suenaga, K., Kobayashi, N.: Fractional ownerships for safe memory deallocation
    (2009). https://doi.org/10.1007/978-3-642-10672-9_11
30. Swamy, N., Rastogi, A., Fromherz, A., Merigoux, D., Ahman, D., Martínez,
    G.: SteelCore: An extensible concurrent separation logic for eﬀectful depen-
    dently typed programs. Proc. ACM Program. Lang. 4(ICFP), 1–30 (Aug 2020).
    https://doi.org/10.1145/3409003
31. Toman, J., Siqi, R., Suenaga, K., Igarashi, A., Kobayashi, N.: ConSORT:
    Context- and ﬂow-sensitive ownership reﬁnement types for imperative pro-
    grams. In: Programming Languages and Systems, pp. 684–714. Lecture
    notes in computer science, Springer International Publishing, Cham (2020),
    https://link.springer.com/10.1007/978-3-030-44914-8_25
24        T. Nakayama et al.

Appendicies

A Proof of Type Preservation (Thm. 1) . . . . . . . . . . . . . . . . . . . . . . . . . . . . .              24
  A.1 Configuration Typing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .       24
  A.2 Auxiliary Lemmas . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .     26
  A.3 Main Proof of Type Preservation . . . . . . . . . . . . . . . . . . . . . . . . . . . .                31
B Definitions Omitted from Section 4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           36
  B.1 Operational Semantics for the Target Language . . . . . . . . . . . . . . .                            36
  B.2 Translation Rules . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    39
C Proof of Soundness (Theorem 2) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .           40
D Benchmark programs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   46

A      Proof of Type Preservation (Thm. 1)
This section first defines the typing relation of configurations, prepares some
lemmas, and then proves the type preservation.

A.1      Configuration Typing
Here, we explain how a configuration is typed. The typing rule for configurations
is as follows:
Θ$D       Θ | r¨s : pτi ⊲ Li | Γi q $ Fi : τi´1 ⊲ Li´1 | Γi´1 p1 ď i ď nq
 Γtot “ Γ ` ∆        L | Γtot $ xH, Ry       Θ | L | Γ $ e : τn ⊲ Ln | Γn
                                                                                                     pT-Confq
                                $D xH, R, Fn : ¨ ¨ ¨ : F1 , ey
Premises Θ $ D, Θ | r¨s : pτi ⊲ Li | Γi q $ Fi : τi´1 ⊲ Li´1 | Γi´1 and Θ |
L | Γ $ e : τn ⊲ Ln | Γn just say that the function definitions, call stack, and
currently reducing expression are all well-typed. The notable part of this rule is
L | Γtot $ xH, Ry, which intuitively expresses that the current heap and registers
are consistent with the information implied by the types in Γtot . For example,
if L | Γtot $ xH, Ry and x : int ref α,0.5
                                        β,0.5 P Γtot , then Rpxq must be an address
that is in dompHq and there must be an aliasing reference pointing to Rpxq with
a lifetime β. The addition Γtot “ Γ ` ∆ represents the fact that we also keep
track of the information of variables that may have been discarded because of
the rule (T-Var).
    The rest of this subsection is devoted to the explanation of the judgments
that have not been introduced so far, namely L | Γtot $ xH, Ry and Θ | r¨s :
pτi ⊲ Li | Γi q $ Fi : τi´1 ⊲ Li´1 | Γi´1 .

Heap and register typing: We now formally define the relation L | Γtot $
xH, Ry. Notations for ownership used in the definition are defined in Fig. 20.
Definition 1. We say that a heap H and a register R are consistent with a
lifetime environment L and a type environment Γ , written L | Γ $ xH, Ry, if
L $WF Γ and the following conditions hold:
                     Borrowable Fractional Ownership Types for Veriﬁcation           25

                        #
                    def  β         pB “ pβ, sqq            def
   BLftpint ref α,r
                B q :“                           BLftpintq :“ undeﬁned
                         undeﬁned pB “ Hq
                        #
                    def  s pB “ pβ, sqq              def
 BOwnpint ref α,r
              B   q :“                     BOwnpintq :“ 0
                         0 pB “ Hq


                    def ÿ
    BrrR
       Γ pα ñ β; aq :“      tBOwnpτ q | x : τ P Γ, Lftpτ q “ α, BLftpτ q “ β, Rpxq “ au
                    def ÿ
       BByR
          Γ pα, aq :“      tBOwnpτ q | x : τ P Γ, BLftpτ q “ α, Rpxq “ au
                   def    ÿ
      BFrmR
          Γ pα, aq :“      tBOwnpτ q | x : τ P Γ, Lftpτ q “ α, Rpxq “ au


                    def ÿ
       OwnR
          Γ pα, aq :“   tOwnpτ q | x : τ P Γ, Lftpτ q “ α, Rpxq “ au
                   def ÿ
          OwnR
             Γ paq :“   tOwnpτ q | x : τ P Γ, Rpxq “ au


Fig. 20. Operations for calculating ownership. (Here the set-builder notation should
be interpreted as a multiset.)



(fraction consistency) for every a P dompHq, OwnR    Γ paq ď 1.
(borrow consistency) for every a P dompHq and α P L, BByR         Γ pα; aq ď
    OwnR  Γ pα; aq ` BFrmR
                         Γ pα; aq.
(type consistency) for each x : τ P Γ , if τ “ int then Rpxq P Z, and other-
    wise, Rpxq P Addr.
(memory consistency) for every x : τ P Γ such that τ is a reference type,
    Rpxq P dompHq and HpRpxqq P Z.

Fraction consistency says that the sum of the ownership of references pointing
to an address a cannot exceed 1. This is the property we want to prove. On
the other hand, borrow consistency is just a technical invariant that is exploited
in the proof. Roughly speaking, it expresses the fact that an ownership that is
borrowed cannot be discarded. Borrow consistency will be used to ensure that
the ownership that was borrowed will be given back properly.


Return context typing: The typing rule for return context is given as

           Θ | L | Γ, x : τ $ e : ρ ⊲ L1 | Γ 1    x R dompΓ 1 q
                                                                   pTC-Let)
          Θ | r¨s : pτ ⊲ L | Γ q $ let x “ r¨s in e : ρ ⊲ L1 | Γ 1

As usual, the judgment Θ | r¨s : pτ ⊲ L | Γ q $ F : ρ ⊲ L1 | Γ 1 describes that if the
hole has a type τ under a type environment Γ , then the context F has a type ρ
under Γ .
26        T. Nakayama et al.

A.2      Auxiliary Lemmas

We now prepare some lemmas that are used to prove type preservation. Some of
the lemmas are not minor propositions that are used to help prove the theorem,
but rather (essentially) are some cases of the case analysis made in the proof of
the theorem. We have separated these cases as lemmas for clarity.


Basic properties of the type system
Lemma 1 (Weakening). Let Θ | L | Γ $ e : ρ ⊲ L1 | Γ 1 . If x R dompΓ q and
τ is of the form int or int ref α,0 for α P L, then we have Θ | L | Γ, x : τ $
e : ρ ⊲ L1 | Γ 1 .

Proof. By straightforward induction on the structure of the type derivation. [
                                                                             \

Lemma 2 (Weakening2). Let Θ | L | Γ $ e : ρ ⊲ L1 | Γ 1 . If L $LF Γ ` Γ 2
and L1 $LF Γ 1 ` Γ 2 , then we have Θ | L | Γ ` Γ 2 $ e : ρ ⊲ L1 | Γ 1 ` Γ 2 .

Proof. By straightforward induction on the structure of the type derivation. [
                                                                             \



Lemma 3 (Weakening of lifetime variables). Let Θ | L | Γ $ e : ρ⊲L | Γ 1 .
If L Ď L1 ,8 then we have Θ | L1 | Γ $ e : ρ ⊲ L1 | Γ 1 .

Proof. By straightforward induction on the structure of the type derivation. [
                                                                             \

Lemma 4 (Substitution). If Θ | L | Γ $ e : τ ⊲ L1 | Γ 1 and x1 R dompΓ q,
then Θ | L | rx1 {xsΓ $ rx1 {xse : τ ⊲ L1 | rx1 {xsΓ 1 .

Proof. By straightforward induction on the structure of the type derivation. [
                                                                             \

Lemma 5 (Substitution of lifetime variables). If Θ | L | Γ $ e : τ ⊲L1 | Γ 1
and β R L, then Θ | rβ{αsL | rβ{αsΓ $ e : rβ{αsτ ⊲ rβ{αsL1 | rβ{αsΓ 1 .

Proof. By straightforward induction on the structure of the type derivation. [
                                                                             \


Lemmas about L | Γ $ xH, Ry
Lemma 6. Suppose that L $WF Γ . Given a heap H and a register R, for each
a P dompHq, we have

 1. BByR                   R
                   ř
        Γ pα; aq “  βPL BrrΓ pα ñ β; aq for every α P L,
 2. BFrmΓ pα; aq “ βPL BrrR
          R         ř
                             Γ pβ ñ α; aq for every α P L, and
        R        ř        R
 3. OwnΓ paq “ αPL OwnΓ pα; aq for each a P dompHq.
8
     Here the inclusion means the existence of an injection from L to L1 that preserves
     and reﬂects the strict order.
                     Borrowable Fractional Ownership Types for Veriﬁcation        27

Proof. Obvious from the definitions. (The only condition of L $WF Γ we use
is the type consistency, so the assumption is unnecessarily strong; this will,
however, not cause any problem.)                                           \
                                                                           [

   The following two lemmas are about lifetime termination. Lem. 8 states
that the consistency relation is preserved under lifetime termination, and is
the key lemma to show the type preservation under the reduction caused by
(RS-Endlft).

Lemma 7. Suppose that L | Γ $ xH, Ry and α P minpLq. Then we have
BByR             R
   Γ pα; aq ď OwnΓ pα; aq.

Proof. Because of the well-formedness condition and the minimality of α, we
must have BFrmR                                                   R
                Γ pα; aq “ 0 for all a P dompHq. Thus, we have BByΓ pα; aq ď
     R
OwnΓ pα; aq by the borrow consistency.                                     \
                                                                           [

Lemma 8. Suppose that L | Γ $ xH, Ry and α P minpLq.
1. We have BrrR                     R
                 Γ pβ ñ γ; aq “ BrrΓ Òα pβ ñ γ; aq for every a P dompHq and
   β, γ P LÒα .
2. For all a P dompHq and β P LÒα ,

                  OwnR                R             R
                     Γ Òα pβ; aq “ OwnΓ pβ; aq ` BrrΓ pβ ñ α; aq.                 (1)

   Hence, for any a P dompHq, we have
                                 ÿ
                 OwnR Γ Òα paq “   OwnR             R
                                      Γ pβ; aq ` BByΓ pα; aq.                     (2)
                                   β‰α


3. We have LÒα | Γ Òα $ xH, Ry.

Proof. The statement 1 is a straightforward consequence of the definition of Brr
and Γ Òα .
   (Proof of 2) The proof is by an easy calculation. Concretely, for each a P
dompHq and β P LÒα , we have:

 OwnR
    Γ Ò pβ; aq
   ÿ α
 “ tOwnpτ q | x : τ P Γ Òα , Lftpτ q “ β, Rpxq “ au                (by def. of Own)
   ÿ
 “ tOwnpτ 1 Òα q | x : τ 1 P Γ, Lftpτ q “ β, Rpxq “ au (by def. Γ Òα and β ‰ α)
   ÿ
 “   tOwnpτ 1 Òα q | x : τ 1 P Γ, Lftpτ 1 q “ β, Rpxq “ a, BLftpτ 1 q “ αu
     ÿ
   ` tOwnpτ 1 Òα q | x : τ 1 P Γ, Lftpτ 1 q “ β, Rpxq “ a, BLftpτ 1 q ‰ αu
                                                        (case analysis on BLftpτ 1 q)
   ÿ
 “   tOwnpτ 1 q ` BOwnpτ 1 q | x : τ 1 P Γ, Lftpτ 1 q “ β, Rpxq “ a, BLftpτ 1 q “ αu
     ÿ
   ` tOwnpτ 1 q | x : τ 1 P Γ, Lftpτ 1 q “ β, Rpxq “ a, BLftpτ 1 q ‰ αu
                                                                       (by def. Γ Òα )
28        T. Nakayama et al.
      ÿ
       tOwnpτ 1 q | x : τ 1 P Γ, Lftpτ 1 q “ β, Rpxq “ au
  “    ÿ
      ` tBOwnpτ 1 q | x : τ 1 P Γ, Lftpτ 1 q “ β, BLftpτ 1 q “ α, Rpxq “ au
  “ OwnR             R
       Γ pβ; aq ` BrrΓ pβ ñ α; aq.

    Equation (2) follows by taking the sum over β P LÒα in the each side of
Equation (1) and applying Lemma 6.
(Proof of 3) It is easy to show LÒα $WF Γ Òα from L $WF Γ , and the memory
and type consistencies are trivial as we are not modifying the heap nor the
register. Hence, we only check the fraction and borrow consistency.
    The fraction consistency holds by the following (in)equalities (which holds
for every a P dompHq):
                         ÿ
         OwnΓ Òα paq “       OwnR               R
                                 Γ pβ; aq ` BByΓ pα; aq                  (by 2)
                           β‰α
                           ÿ
                       ď         OwnR             R
                                    Γ pβ; aq ` OwnΓ pα; aq             (by Lemma 7)
                           β‰α

                       “ OwnR
                            Γ paq                                (by Lemma 6)
                       ď1       (by the fraction consistency of L | Γ $ xH, Ry)

   We now show the borrow consistency. Take a P dompHq and β P LÒα . We
have

     BByR                R
        Γ Òα pβ; aq “ BByΓ pβ; aq                                (by 1 and Lemma 6)
                    ď OwnR              R
                         Γ pβ; aq ` BFrmΓ pβ; aq
                                  (by the borrow consistency of L | Γ $ xH, Ry)
                                                         ÿ
                    “ OwnR                R
                         Γ Òα pβ; aq ´ BrrΓ pβ ñ α; aq `    BrrRΓ pβ ñ γ; aq
                                                               γPL
                                                                 (by 2 and Lemma 6)
                                           ÿ
                    “ OwnR
                         Γ Òα pβ; aq `            BrrR
                                                     Γ pβ ñ γ; aq
                                          γPLÒα
                                           ÿ
                    “ OwnR
                         Γ Òα pβ; aq `            BrrR
                                                     Γ Òα pβ ñ γ; aq          (by 1)
                                          γPLÒα

                    “ OwnR                 R
                         Γ Òα pβ; aq ` BFrmΓ Òα pβ; aq                 (by Lemma 6)


as desired.                                                                       \
                                                                                  [

We now prove that ownership transfers between aliasing references in Γ pre-
serves L | Γ $ xH, Ry. This is the lemma used to prove the preservation under
reductions caused by (RS-Let) and (RS-Alias).

Lemma 9. Suppose that L | Γ $ xH, Ry.
                       Borrowable Fractional Ownership Types for Veriﬁcation                29

 1. If Γ “ Γ0 , y : τ , τ “ τx ` τy and x R dompRq, then L | Γ0 , x : τx , y : τy $
    xH, Rtx ÞÑ Rpyquy
 2. If Γ “ Γ0 , x : τx , y : τy , Rpxq “ Rpyq, τx ` τy “ τ and τx1 ` τy1 “ τ for some
    τ , then L | Γ0 , x : τx1 , y : τy1 $ xH, Ry

Proof. We only prove 1 because 2 can be proved in a similar manner. The case
where τ “ τx “ τy “ int is trivial, so let us assume that τ is a reference type.
To simplify the notation, we write a for Rpyq, R1 for Rtx ÞÑ Rpyquand Γ 1 for
Γ0 , x : τx , y : τy . We first check the memory consistency. It suffices to show that
Rpxq P dompHq. Since a P dompHq and Hpaq P Z due to the memory consistency
of L | Γ $ xH, Ry, we have Rpxq “ a P dompHq and HpRpxqq P Z as desired.
To show the fraction and borrow consistencies, we proceed by a case analysis on
the rule used to derive τ “ τx ` τy .
     Suppose that the rule used was (A-Share). Then it must be the case that τ “
           α,r1 `r2
int ref β,s   1 `s2
                    , τx “ int ref α,r 1                  α,r2
                                   β,s1 and τy “ int ref β,s2 for some fractions r1 , r2 , s1 ,
s2 and a lifetime variable α. We therefore have Ownpτ q “ Ownpτx q ` Ownpτy q.
                                                       R1
From this it follows that OwnR                                                     R 1
                                         Γ paq “ OwnΓ 1 paq; we also have OwnΓ pa q “
         1
OwnR          1            1             1
       Γ 1 pa q for any a such that a ‰ a because x and y do not have any ownership
for this address. Thus, the fraction consistency of L | Γ 1 $ xH, R1 y follows from
that of L | Γ $ xH, Ry. Similarly, by Ownpτ q “ Ownpτx q ` Ownpτy q and
                                                                                   R1
BOwnpτ q “ BOwnpτx q ` BOwnpτy q, we have OwnR                   Γ pα; aq “ OwnΓ 1 pα; aq,
                               R1                                    R1
BFrmR                                                R
         Γ pα; aq “ BFrmΓ 1 pα; aq and BByΓ pβ; aq “ BByΓ 1 pβ; aq. Using these
equations we get the borrow consistency of L | Γ 1 $ xH, R1 y from that of L |
Γ $ xH, Ry.
     Now we show the case for (A-Borrow). In this case, we have τ “ int ref α,r`s ,
τx “ int ref β,s and τy “ int ref α,r      β,s for some fractions r, s and a lifetime vari-
ables α and β; the case where x lends some ownership to y is symmetric and
is proved similarly. Again, we have Ownpτ q “ Ownpτx q ` Ownpτy q and, from
this, the fraction consistency follows as in the case for (A-Share). Observe that
we have
           1                    1
   OwnR                R                R                    R
      Γ 1 pα; aq ` BFrmΓ 1 pα; aq “ pOwnΓ pα; aq ´ sq ` pBFrmΓ pα; aq ` sq

                                        “ OwnR              R
                                             Γ pα; aq ` BFrmΓ pα; aq

                                        ě BByR Γ pα; aq
                                           (by borrow consistency of L | Γ $ xH, Ry)
                                                   1
                                        “ BByR
                                             Γ 1 pα; aq

and
               1                    1
       OwnR                R                R                   R
          Γ 1 pβ; aq ` BFrmΓ 1 pβ; aq “ pOwnΓ pβ; aq ` sq ` BFrmΓ pβ; aq

                                           ě BByRΓ pβ; aq ` s
                                           (by borrow consistency of L | Γ $ xH, Ry)
                                                       1
                                           “ BByR
                                                Γ 1 pβ; aq.
30      T. Nakayama et al.

Since x and y does not have any ownership for address other than a, the above
two inequality is enough to conclude that the borrow consistency of L | Γ 1 $
xH, R1 y holds.                                                             \
                                                                            [


Lemmas about return contexts We prove two lemmas (Lemmas 10 and 11)
about return contexts. Lemmas 10 and 11 are the key lemmas for the return,
i.e. (RS-Var), and call cases, respectively; we have separated them into separate
lemmas for clarity.

Lemma 10. Suppose that

                          Θ | L | Γ $ x : τ ⊲ L1 | Γ 1         and
              Θ | r¨s : pτ ⊲ L | Γ q $ let y “ r¨s in e : ρ ⊲ L2 | Γ 2 .
                              1    1


Then Γ can be split as Γ “ Γ0 ` ∆ such that

                     Θ | L | Γ0 $ let y “ x in : ρ ⊲ L2 | Γ 2 .

Proof. Since Θ | r¨s : pτ ⊲ L1 | Γ 1 q $ let y “ r¨s in e : ρ ⊲ L2 | Γ 2 , we must have

                         Θ | L1 | Γ 1 , y : τ $ e : ρ ⊲ L2 | Γ 2 .                 (3)

On the other hand, by inversion on Θ | L | Γ $ x : τ ⊲ L1 | Γ 1 , it must be the
case that

                        Γ “ ∆ ` Γ1 ` x : τ         and L1 “ L

for some ∆. Without loss of generality, assume that x P dompΓ 1 q, i.e. Γ 1 “ Γ01 , x :
τx1 for some τx1 ; otherwise we can extend Γ 1 with x using the weakening lemma
(Lemma 1). We take Γ 1 ` x : τ as Γ0 . Since L1 “ L and Γ 1 “ Γ01 , x : τx1 , the
judgment (3) is of the form

                     Θ | L | Γ01 , x : τx1 , y : τ $ e : ρ ⊲ L2 | Γ 2 ,

and, since Γ0 pxq “ τx1 ` τ , applying (T-Let) yields

                Θ | L | Γ 1 ` x : τ $ let y “ x in e : ρ ⊲ L2 | Γ 2 .

                                                                                     \
                                                                                     [

Lemma 11. Suppose that
                                   Ñ
                                   Ý
            Θ | L | Γ $ let x “ f x β ypy1 , . . . , yn q in e1 : ρ ⊲ L1 | Γ 1     (4)
                     $WF Θ     Θ $ f ÞÑ xÝ      Ñ
                                                α y px1 , . . . , xn qe            (5)
                         Ñ
                         Ý
                Θpf q “ @ α : M. xτ1 , . . . , τn y Ñ xτ 1 , . . . , τ 1 | τ y     (6)
                                                           1         n
                             f ÞÑ xÝ
                                   Ñ
                                   α y px1 , . . . , xn qe P D                     (7)
                         Borrowable Fractional Ownership Types for Veriﬁcation                    31

Then we have

                           Θ | L | Γ $ rỹ{x̃se : rβ̃{α̃sτ ⊲ L | Γ 2                             (8)
                                            2                          1          1    1
              Θ | r¨s : prβ̃{α̃sτ ⊲ L | Γ q $ let x “ r¨s in e : ρ ⊲ L | Γ                       (9)

where
                           def
                      Γ 2 :“ ry1 : ρ11 {x1 : ρ1 s ¨ ¨ ¨ ryn : ρ1n {xn : ρn sΓ
                           def                     def
                       ρi :“ rβ̃{α̃sτi          ρ1i :“ rβ̃{α̃sτi1

Proof. Note that by inversion on (4), we have

                  Θ | L | Γ0 , x : ρ, y1 : ρ11 , . . . , yn : ρ1n $ e : ρ ⊲ L1 | Γ 1            (10)
                                  1
                     x R dompΓ q          Γ “ Γ0 , x : ρ, y1 : ρ1 , . . . , yn : ρn             (11)

   We first show that (9) holds. By the definition of (TC-Let), it suffices to
show that

                 Θ | L | Γ 2 , x : τ $ e : ρ ⊲ L1 | Γ 1        and x R dompΓ 1 q

These are exactly what (10) and (11) assert.
   Now we show that (8) holds. By inversion on (5) together with (6), we have

            Θ | M | x1 : τ1 , . . . , xn : τn $ e : τ ⊲ M | x1 : τ11 , . . . , xn : τn1

Thanks to substitution lemmas (Lemmas 4 and 5), from the above judgment,
we obtain

Θ | rβ̃{α̃sM | y1 : ρ1 , . . . , yn : ρn $ rỹ{x̃se : rβ̃{α̃sτ ⊲ rβ̃{α̃sM | y1 : ρ11 , . . . , yn : ρ1n

Then, by the weakening lemmas (Lemmas 2 and 3), we have

                           Θ | L | Γ $ rỹ{x̃se : rβ̃{α̃sτ ⊲ L | Γ 2

                                                                                                   \
                                                                                                   [


A.3     Main Proof of Type Preservation

Finally, we prove that the one-step reduction relation preserves well-typedness
(of configurations). By repeatedly applying this result, we obtain Thm. 1 because
$D xHH, ¨, ey holds for any program xD, ey such that $ xD, ey
                         A
                           Ý
                           Ñ
                                E      A
                                              Ñ
                                              Ý
                                                    E        A       Ý
                                                                     Ñ E
Lemma 12. If $ H, R, F , e and H, R, F , e ÝÑD H 1 , R1 , F 1 , e1 , then
   A          Ý
              Ñ E
$ H 1 , R 1 , F 1 , e1 .
32      T. Nakayama et al.

Proof. The proof is by a case analysis on the reduction rules.
   Before we proceed to each case, we explain the overall structure of the proof.
Our goal is to find find L2 , Γtot
                               1
                                   , Γ 2 such that

             L2 | Γtot
                    1
                       $ H 1 , R1         Θ | L2 | Γ 2 $ e1 : ρ ⊲ L1 | Γ 1
                          @        D

                                                                    Ý
                                                                    Ñ
            1
such that Γtot  Γ 2 ` ∆1 forEsome ∆1 , and also to show that stack F 1 is well-
               “A
                       Ñ
                       Ý
typed by using $ H, R, F , e . (In case of (Rs-Var) and (Rs-Call), we also need
to find suitable τ , L1 and Γ 1 as the function we are reducing at that moment
changes.) A
                     Ñ
                     Ý
                         E
    From $ H, R, F , e , as assumptions, we have

                                  L | Γtot $ xH, Ry                               (12)
                                                    1    1
                             Θ |L |Γ $e:ρ⊲L |Γ                                    (13)

where Γtot “ Γ ` ∆. (Throughout the proof we will fix Θ, Γ and Γtot to be the
environments satisfying the above relations.) In most cases, L2 , Γ 2 , Γtot1
                                                                              are the
same as L, Γ , Γtot , respectively or simple modifications of L, Γ , Γtot .
   We first consider the two cases that involves some reasoning on stacks.
Case: (Rs-Var) In this case, we must have
                                 Ý
                                 Ñ                      Ý
                                                        Ñ
         H 1 “ H,    R1 “ R,      F “ Fn : ¨ ¨ ¨ : F1 , F 1 “ Fn´1 : ¨ ¨ ¨ : F1
                                 e “ x, e1 “ Fn rxs

                                                                Ñ
                                                                Ý
                                                         A           E
for some n ě 1. Moreover, by the definition of $          H, R, F , e , we must also
have

         Θ | r¨s : pτi ⊲ Li | Γi q $ Fi : τi´1 ⊲ Li´1 | Γi´1      p1 ď i ď nq
                             Θ | L | Γ $ x : τn ⊲ Ln | Γn .

where τn “ ρ, Ln “ L1 and Γn “ Γ 1 . Therefore, by Lemma 10, we can split Γ
as Γ0 ` ∆1 satisfying

                     Θ | L | Γ0 $ Fn rxs : τn´1 ⊲ Ln´1 | Γn´1 .

Hence, we can take Γ0 as Γ 2 , L as L2 and Γtot as Γtot
                                                    1
                                                        . Note that Γtot “ Γ ` ∆ “
Γ0 `p∆ `∆q for some ∆. The relation L | Γtot $ xH 1 , R1 y trivially holds because
       1                                2    1

we have L | Γtot $ xH, Ry.
Case: (Rs-Call) In this case, we must have

                                H 1 “ H, R1 “ R,
                             Ñ
                             Ý
              e “ let x “ f x β ypy1 , . . . , yn q in e0 , e1 “ rÝ
                                                                  Ñ
                                                                  y {Ý
                                                                     Ñ
                                                                     x sef
                      Ñ1
                      Ý              1                 1       Ñ
                                                               Ý
                       F “ plet x “ r¨s in rx {xse0 q : F
                        Borrowable Fractional Ownership Types for Veriﬁcation       33

for some f ÞÑ xÝÑ
                α y px1 , . . . , xn qef P D. Let Fn be the return context on the top
             Ñ
             Ý
of the stack F . Note that Fn needs to be typed as follows:

                    Θ | r¨s : pρ ⊲ L1 | Γ 1 q $ Fn : τn´1 ⊲ Ln´1 | τn´1

for some τn´1 , Ln´1 and τn´1 . Since Θ $ D, we also have

                       $W F Θ         Θ $ f ÞÑ xÝ
                                                Ñ
                                                α y px1 , . . . , xn qef           (14)

    For L2 , Γ 2 and Γtot , we take L, Γ and Γtot , respectively.
    Our task is to show that

          Θ | r¨s : pτn`1 ⊲ L | Γn`1 q $ let x1 “ r¨s in rx1 {xse0 : ρ ⊲ L | Γ
                        Θ | L | Γ $ rÝ
                                     Ñy {Ý
                                         Ñ
                                         x sef : τn`1 ⊲ L | Γn`1

for some τn`1 and Γn`1 . These type and type environment can be obtained by
applying Lemma 11 to (14) and to the type judgment of e, i.e. (13) (with the
help of substitution lemma, i.e. Lemma 4, to substitute x1 to x). Concretely,
                     Ñ Ñ
                     Ý
             τn`1 “ r β {Ý
                         α sτf and
                           Ñ Ñ 1
                           Ý                                Ñ Ñ 1
                                                            Ý
             Γn`1 “ ry1 : r β {Ý
                               α sτ {x1 : τ1 s ¨ ¨ ¨ ryn : r β {Ý
                                      1                         α sτ {xn : τn sΓ
                                                                      n

provided that Θpf q “ @Ý
                       Ñ
                       α : M. xτ1 , . . . , τn y Ñ xτ11 , . . . , τn1 | τf y.

   So far we are done with the case (Rs-Var) and (Rs-Call). The remaining
cases do not involve function calls or returns. Therefore, in what follows, we will
omit the reasoning on call stacks.
Case: (Rs-Let) It must be the case that

                                       H 1 “ H,
                           R1 “ Rtx1 ÞÑ Rpyqu, x1 R dompRq                         (15)
                                                          1           1
                          e “ let x “ y in e0 , rx {xse0 “ e
                                     Γ “ Γ0 , y : τ                                (16)

for some x, y, τ , e0 and Γ0 .
    By inversion on the typing rule, we obtain

                        Θ | L | Γ0 , y : τy , x : τx $ e0 : ρ ⊲ L1 | Γ 1
                                          τ “ τx ` τy                              (17)
                                          x R dompΓ 1 q                            (18)

By the substitution lemma (Lemma 4) and (18), we also have

                       Θ | L | Γ0 , y : τy , x1 : τx $ e1 : ρ ⊲ L1 | Γ 1 .
              def                                                                   def
We set L2 :“ L and Γ 2 “ Γ0 , y : τy , x1 : τx . Furthermore, we define Γtot  1  :“
                1                                               1
pΓ0 , y : ρy , x : ρx q ` ∆. The remaining goal is to show L | Γtot $ xH, Ry, which
34      T. Nakayama et al.

can be shown by 1 of Lemma 9 together with (15), (17) and Γtot “ pΓ, y : τ q` ∆.
(Note that x1 R domp∆q because of type consistency.)
Case: (Rs-Arith) Similar (but also easier compared) to the previous case.
Case: (Rs-MkRef) In this case we have,

     H 1 “ Hta ÞÑ Rpyqu,       a R dompHq,            R1 “ Rtx1 ÞÑ au,        x1 R dompRq
                     e “ let x “ mkref y in e0 ,             rx1 {xse0 “ e1
                                        Γ “ Γ0 , y : int

for some a, x, x1 and y. By inversion on the typing rule, we must also have

                  Θ | L | Γ0 , x : int ref α,1 , y : int $ e0 : ρ ⊲ L1 | Γ 1
                                         x R dompΓ 1 q                                   (19)

Again, by applying the substitution lemma (Lemma 4) together with (19) to this
judgment gives

                  Θ | L | Γ0 , x1 : int ref α,1 , y : int $ e1 : ρ ⊲ L1 | Γ 1

We take Γ0 , x1 : int ref α,1 , y : int as Γ 2 , L as L2 and Γtot , x1 : int ref α,1 as Γtot
                                                                                         1
                                                                                             .
                                                1          α,1        1    1
     Our goal is to show that L | Γtot , x : int ref           $ xH , R y under the as-
sumption that L | Γtot $ xH, Ry. To check the memory consistency, we need
to check that the newly introduced variable x1 does not cause any out-of-bound
access. Since R1 px1 q “ a, we have R1 px1 q P dompH 1 q as desired. We also have
H 1 pRpx1 qq “ Rpyq P Z from the type consistency of y. Type consistency for x1 is
also clearly met.
     Now we verify the fraction and borrow consistency. Observe that,

                                @z P dompΓtot q. Rpzq ‰ a                                (20)

because of the memory consistency of L | Γtot $ xH, Ry together with a R
dompHq. Therefore,
                                    1
                                                 α,1
                         OwnR1 paq “ Ownpint ref
                            Γtot                     q“1
                                                  1
For a1 ‰ a, it is easy to check that OwnR     1
                                          1 pa q “ OwnΓ
                                         Γtot
                                                        R
                                                         tot
                                                             pa1 q, which does not
exceed 1 because of the fraction consistency of L | Γtot $ xH, Ry. Hence, the
fraction consistency holds. To check the borrow consistency, it suffices to check
                         1                    1                       1
                 BByR
                    Γtot
                                   R
                                    tot
                                                    R
                     1 pα; aq ď OwnΓ 1 pα; aq ` BFrmΓ 1 pα; aq
                                                     tot
                                                                                         (21)

because the other cases follows from the borrow consistency of L | Γtot $ xH, Ry.
By (20), we have
                                1                        1
                        BByR               R
                            1 pα; aq “ BFrmΓ 1 pα; aq “ 0.
                           Γtot             tot


Hence, (21) holds because the left-hand side is 0 whereas the right-hand side is
1.
                       Borrowable Fractional Ownership Types for Veriﬁcation           35

Case: (Rs-Alias) It must be the case that
                                    Ñ1 Ý
                                    Ý   Ñ
                   H 1 “ H, R1 “ R, F “ F , e “ alias px “ yqe1

with Rpxq “ Rpyq “ a for some a. Moreover, the type environment Γ must be
of the form Γ0 , x : τx , y : τy for some τx and τy . By inversion on the typing of e,
that is (13), we have

                      Θ | L | Γ0 , y : ρy , x : ρx $ e1 : ρ ⊲ L1 | Γ 1 .

such that τ “ τx ` τy and τ “ ρx ` ρy . We take L, Γ0 , y : ρy , x : ρx pΓ0 , y : ρy , x :
ρx q ` ∆ for L2 , Γ 2 and Γtot
                           1
                               , respectively. Note that we have Γtot pxq ` Γtot pyq “
τ “ Γtot pxq`Γtot pyq for some τ 1 because Γtot “ pΓ0 , x : τx , y : τy q`∆. From this
 1     1          1

and R1 pxq “ R1 pyq, we can use 2 of Lemma 9 to conclude L2 | Γtot      1
                                                                          $ xH 1 , R1 y.
Case: (Rs-Newlft) In this case, we must have

                        H 1 “ H, R1 “ R, e “ newlft α in e1 .

By inversion on the typing rule, we have

              Θ | L Y tα ă β | β P LftVarpLqu | Γ $ e : ρ ⊲ L1 | Γ 1 .
             def                                       def                 def
We set L2 :“ L Y tα ă β | β P Lqu, Γ 2 :“ Γ and Γtot        1   :“ Γtot . Because
L $WF Γ and L $WF Γtot it follows that L2 $WF Γ and L2 $WF Γtot . The
well-formedness also ensures that α does not appear in Γ nor Γtot . This implies
that
            BByR                   R                 R
                  Γtot pα, aq “ OwnΓtot pα, aq “ BFrmΓtot pα, aq “ 0

for every address a. Therefore, L2 | Γtot
                                        1
                                          $ xH 1 , R1 y immediately follows from
L | Γtot $ xH, Ry.
Case: (Rs-Endlft) In this case, we have

                       H 1 “ H,     R1 “ R,      e “ endlft α; e1 .

We must also have

                    Θ | LÒα | Γ Òα $ e1 : ρ ⊲ L1 | Γ 1       α P minpLq
                                                 def           def    1
by inversion on the typing rule. We set L2 :“ LÒα , Γ 2 :“ Γ Òα and Γtot “ Γtot Òα .
It remains to show that LÒα | Γtot Òα $ xH, Ry, and this is exactly what Lemma 8
states.
Case: (Rs-Deref) It must be the case that

           H 1 “ H,     R1 “ Rtx1 ÞÑ vu, HpRpyqq “ v, x1 R dompRq
                        e “ let x “ ‹y in e0 e1 “ rx1 {xse0

for some x, y and x1 . By inversion on 13, we have

                   Θ | L | Γ0 , x : int, y : int ref α,r       1
                                                     B $ e: ρ⊲L |Γ
                                                                   1
36      T. Nakayama et al.

                       x R dompΓ 1 q    Γ “ Γ0 , y : int ref α,r
                                                             B

for some reference type y : int ref α,r
                                    B and type environment Γ0 . Applying the
substitution lemma (Lemma 4) to the above judgment yields

             Θ | L | Γ0 , x1 : int, y : int ref α,r   1            1
                                                B $ rx {xse : ρ ⊲ L | Γ
                                                                        1


                                         def         def
because x1 R dompΓ 1 q. We define L2 :“ L, Γ 2 :“ Γ0 , x1 : int, y : int ref α,r
                                                                              B and
  1
Γtot “ pΓ0 , x1 : int, y : int ref α,r
                                   B q ` ∆.
                                       1
    We are left to show that L | Γtot      $ xH, Rtx1 ÞÑ vuy. Fraction, borrow, mem-
                                                                                  1
ory consistency obviously hold since the only difference between Γtot and Γtot
                                         1
is the additional integer variable x . The type consistency also holds because
R1 px1 q “ HpRpyqq P Z from the memory consistency of (12).
Case: (Rs-Assign) In this case, we have

                   H 1 “ Hta ÞÑ Rpyqu,         R1 “ R,     Rpxq “ a
                                    e “ x :“ y; e1

Furthermore, we have

                             Θ | L | Γ $ e1 : ρ ⊲ L1 | Γ 1

by inversion on (13) (the typing of e). Therefore, we can take L, Γ and Γtot for
L2 , Γ 2 and Γtot , respectively.
    It remains to show that L | Γtot $ xH 1 , Ry. Since the type environment hasn’t
changed from Γtot , the fraction, borrow and type consistency trivially hold. We
need to check the memory consistency since the value stored in a has changed.
We have HpRpxqq “ Rpyq P Z because of the type consistency of y.
Case: (Rs-IfTrue) In this case, we have

                                 H 1 “ H, R1 “ R
                             e “ ifz x then e1 else e2

for some x and e2 . By inversion on (13) (the typing of e) we have

                             Θ | L | Γ $ e1 : ρ ⊲ L1 | Γ 1 .

Hence, we can simply take L, Γ and Γtot for L2 , Γ 2 and Γtot , respectively.
Case: (Rs-IfFalse) Almost identical to the previous case.
Cases: (Rs-AliasFail) and (Rs-Fail) These cases contradict with the assumption.
                                                                              \
                                                                              [


B     Definitions Omitted from Section 4
B.1   Operational Semantics for the Target Language
Here, we give the complete definition of the reduction semantics of the target
language that has been omitted from Section 4.1. The rules are given in Fig. 21.
                    Borrowable Fractional Ownership Types for Veriﬁcation     37

We write Stx ÞÑ vu (where x P Var and v P Valtgt ) for a register that maps
the variable x to v and inherits S for the other variables. We write RefreshS ptq
for the term taken by renaming all the bound variables in t to fresh names
(not contained in dompSq for any S P S). This is for avoiding name conflicts
in recursive function calls. The partial functions π1 , π2 : Valtgt Ñ Valtgt are
projections for pairs.
38   T. Nakayama et al.



                                                                             (Rt-Var)
                                      Ñ
                                      Ý              Ñ
                                                     Ý
       A                                   E  A                   E
           D, S, plet x1 “ rs in tq : F , x ÝÑ D, S, F , rx{x1 st

           @S P S. JoKS “ n        S 1 “ tStx ÞÑ nu | S P Su
                                                             (Rt-LetArith)
                    Ñ
                    Ý                                Ñ
                                                     Ý
            A                          E     A           E
              D, S, F , let x “ o in t ÝÑ D, S 1 , F , t

                             S 1 “ tStx ÞÑ Spyqu | S P Su
                                                                       (Rt-Let)
                            Ñ
                            Ý                              Ñ
                                                           Ý
                  A                           E     A            E
                      D, S, F , let x “ y in t ÝÑ D, S 1 , F , t

              f ÞÑ px1 , . . . , xn qt P D        t2 “ RefreshS ptq
                                                                             (Rt-Call)
                Ñ
                Ý
      A                                                E
          D, S, F , let x “ f py1 , . . . , yn q in t1
                                                 Ñ
                                                 Ý
               A                                                         E
          ÝÑ D, S, plet x “ rs in t1 q : F , ry1 {x1 s ¨ ¨ ¨ ryn {xn st2

                   S 1 “ tStx1 ÞÑ xSpyq, Spzqyu | S P Su
                                                                       (Rt-LetPair)
                     Ñ
                     Ý                                   Ñ
                                                         Ý
           A                                E    A             E
               D, S, F , let x “ xy, zy in t ÝÑ D, S 1 , F , t

                      S 1 “ tStx1 ÞÑ π1 pSpyqqu | S P Su
                                                                       (Rt-LetFst)
                      Ñ
                      Ý                                  Ñ
                                                         Ý
            A                               E      A           E
                D, S, F , let x “ fst y in t ÝÑ D, S 1 , F , t

                      S 1 “ tStx1 ÞÑ π2 pSpyqqu | S P Su
                                                                       (Rt-LetSnd)
                     Ñ
                     Ý                                   Ñ
                                                         Ý
           A                                E      A          E
               D, S, F , let x “ snd y in t ÝÑ D, S 1 , F , t

                  S 1 “ tStx ÞÑ nu | S P S, n P Zu
                                                                 (Rt-LetNondet)
                   Ñ
                   Ý                               Ñ
                                                   Ý
            A                        E     A            E
             D, S, F , let x “ ‹ in t ÝÑ D, S 1 , F , t

                          S 1 “ tS P S | Spxq “ Spyqu
                                                                       (Rt-Assume)
                      Ñ
                      Ý                                 Ñ
                                                        Ý
            A                               E     A           E
                D, S, F , assume px “ yq; t ÝÑ D, S 1 , F , t

                 S 1 “ tS P S | Spxq “ 0u    S1 ‰ H
                                                                         (Rt-IfTrue)
                 Ñ
                 Ý                                     Ñ
                                                       Ý
          A                               E   A               E
           D, S, F , ifz x then t1 else t2 ÝÑ D, S 1 , F , t1

                 S 1 “ tS P S | Spxq ‰ 0u    S1 ‰ H
                                                                         (Rt-IfFalse)
                 Ñ
                 Ý                                     Ñ
                                                       Ý
       A                                  E   A               E
           D, S, F , ifz x then t1 else t2 ÝÑ D, S 1 , F , t2

                                                           (Rt-Fail)
                                        Ñ
                                        Ý
                              A                 E
                                  D, S, F , fail ÝÑ Fail


                 Fig. 21. Operational semantics of the target language
                        Borrowable Fractional Ownership Types for Veriﬁcation                      39

B.2     Translation Rules


                                                                            qρx
L | Γ, x : τx , y : τy $ e : ρ ñ t     τ “ τx ` τy          t1 “ TNullifypτ
                                                                  τ ρy          px, y, tq
                                                                                             (C-Let)
             L | Γ, y : τ $ let x “ y in e : ρ ñ let x “ x_, _y in t1

                           L | Γ, x : int $ e : ρ ñ t
                                                                        (C-Arith)
                  L | Γ $ let x “ o in e : ρ ñ let x “ o in t

                   L | Γ $ e1 : ρ ñ t1     L | Γ $ e2 : ρ ñ t2
                                                                                   (C-If)
            L | Γ $ ifz x then e1 else e2 : ρ ñ ifz x then t1 else t2
                                                            (C-Fail)
                              L | Γ $ fail : τ ñ fail

                    L | Γ, x : int ref α,1
                                       H , y : int $ e : ρ ñ t
                                                                                  (C-MkRef)
       L | Γ, y : int $ let x “ mkref y in e : ρ ñ let x “ xy, _y in t

            L | Γ, x : int, y : int ref α,r
                                        B $ e : ρ ñ t           rą0
                                                                                 (C-Deref-Pos)
      L | Γ, y : int ref α,r
                         B $ let x “ ‹y in e : ρ ñ let x “ fst y in t


                 L | Γ, x : int, y : int ref α,0
                                             B $ e : ρ ñ t
                                                                               (C-Deref-Zero)
       L | Γ, y : int ref α,0
                          B $ let x “ ‹y in e : ρ ñ let x “ _ in t

                     L|Γ $e:ρñt             OwnΓ pxq “ 1
                                                                         (C-Assign)
                L | Γ $ x :“ y; e : ρ ñ let x “ xy, snd xy in t

                  τx ` τy “ int ref α,r
                                    B       int ref α,r
                                                    B “ ρx ` ρy

              L | Γ, x : ρx , y : ρy $ e : ρ ñ t   t1 “ Tττxx ρ
                                                              ρy px, y, tq
                                                                 x

                                                                              (C-Alias)
                 L | Γ, x : τx , y : τy $ alias px “ yq; e : ρ ñ t1

                     L1 | Γ $ e : ρ ñ t    L1 “ L Y tαu
                                                                  (C-NewLft)
                          L | Γ $ newlft α in e ñ t

   LÒα | Γ Òα $ e : ρ ñ t     α “ minpLq     Γ zΓ Òα “ tx1 , . . . , xn u
                                                                                      (C-EndLft)
      L | Γ $ endlft α; e : ρ ñ assume1ďiďn pfst xi “ snd xi q; t


              Fig. 22. Translation rules for the intraprocedural fragment


   Fig. 22 shows the translation rules for the intraprocedual fragment of the
source language. As in Section 4.2, we omit the environments Θ, L1 and Γ 1 to
simplify the notation. (Hence, the side condition x R dompΓ 1 q is also omitted.)
The type Nullifypτ q in (C-Let) is a new type obtained by depriving all the
ownership of the type τ . Concretely, Nullifypτ q is defined below.
                             def                                       def
             Nullifypintq :“ int          Nullifypint ref α,r            α,0
                                                          B q :“ int ref H
40       T. Nakayama et al.

          Γ 1 “ y1 : τ1 , . . . , yn      tx1 , . . . , xn u “ RefVarpΓ ` x : τ qzRefVarpΓ 1 q
                                                                                                             (C-Var)
 Θ | L | Γ ` Γ ` x : τ $ x : τ ⊲ L | Γ 1 ñ assume1ďiďn pfst xi “ snd xi q; xx, y1 , . . . , yn y
                  1


               Ñ Ñ
               Ý               Ñ Ñ
                               Ý                     Ñ Ñ 1
                                                     Ý
          ρ “ r β {Ý
                   α sτ, ρi “ r β {Ý  α sτi , ρ1i “ r β {Ý  α sτi            x R dompΓ 1 q
                                                                            Ñ Ñ
                                                                            Ý
        Θpf q “ @ÝÑ
                  α : M. xτ1 , . . . , τn y Ñ xτ11 , . . . , τn1 | τ y     r β {Ý
                                                                                α sM Ď L
                Θ | L | Γ, x : ρ, y1 : ρ11 , . . . , yn : ρ1n $ e : ξ ⊲ L1 | Γ 1 ñ t
                       t1 ” let xx, y1 , ¨ ¨ ¨ , yn y “ f py1 , ¨ ¨ ¨ , yn q in t
                                                                                                      (C-Call)
                                                       Ñ
                                                       Ý
 Θ | L | Γ, y1 : ρ1 , . . . , yn : ρn $ let x “ f x β ypy1 , . . . , yn q in e : ξ ⊲ L1 | Γ 1 ñ t1

         Θpf q “ @Ý
                  Ñ
                  α : L. xτ1 , . . . , τn y Ñ xτ11 , . . . , τn1 | τ y     LĎÝ
                                                                             Ñ
                                                                             α
       Θ | L | x1 : τ1 , . . . , xn : τn $ e : τ ⊲ L | x1 : τ11 , . . . , xn : τn1 ñ t
                                                                                         (C-FunDef)
                Θ $ f ÞÑ xÝ
                          Ñ
                          α y px1 , . . . , xn qe ñ f ÞÑ px1 , . . . , xn qt



                      Fig. 23. Translation rules for the interprocedural part


    Fig. 23 shows the rules related to function calls and returns. We include the
translation for variables in this figure as a variable is the program point where the
function returns. For these rules, we do not omit the environments Θ, L1 , and Γ 1
because they play roles in the translation. The tuple xx1 , x2 , x3 , . . .y in (C-Var)
is an abbreviation of a nested pair xx1 , xx2 , xx3 , . . .yyy. After the translation, a
function returns its arguments in addition to the original returned value because
the arguments may be updated in the function body. The RefVarpΓ q indicates
all variable names that are typed as references in the typing context Γ . We add
assume1ďiďn pfst xi “ snd xi q for the references that are dropped at this point.


C     Proof of Soundness (Theorem 2)

This section proves the soundness of our type-directed translation. As in the
body of the paper, we do not consider the interprocedural rules of the reduction
relation for simplicity.
    The following is a technical definition that corresponds to the idea of PFZ.
Since our type system allows reborrowing, we define a relation over sequence of
(aliasing) references rather than considering a relation over two references.

Definition 2 (Prophecy Chain). Let Γ be a typing context, R be a register
in the source language, and S be a register in the target language. A sequence x1 :
τ1 , . . . , xn : τn P Γ is called a prophecy chain and denoted ChainR,S
                                                                     Γ px1 , . . . , xn q
iff

1. Rpx1 q “ ¨ ¨ ¨ “ Rpxn q P Addr
2. Ownpτn q ą 0 ^ Ownpτ1 q “ ¨ ¨ ¨ “ Ownpτn´1 q “ 0
3. π1 pSpxi qq “ π2 pSpxi`1 qq pfor all i “ 1, . . . , n ´ 1q
                      Borrowable Fractional Ownership Types for Veriﬁcation        41

 4. LftΓ pxi`1 q “ BLftΓ pxi q when BLftΓ pxi q is defined, and otherwise, LftΓ pxi`1 q “
    LftΓ pxi q pfor all i “ 1, . . . , n ´ 1q
We write ChainR,S                          R,S
              Γ px1 , . . . , xn q if ChainΓ px1 , . . . , xn q holds for each S P S.
                                                                                    \
                                                                                    [
   We now formally define the simulation:
Definition 3. Let xH, R, ey and xS, ty be any configurations of source and target
language, respectively. Configurations xH, R, ey and xS, ty are called to be in
                                          sim
simulating relation and denoted xH, R, ey ùL,Γ xS, ty iff
 1. (S-Conv) L | Γ $ e : τ ñ t
 2. (S-Prop) @x : int ref α,0                n
                              β,r P Γ. Dtyi ui“1 Ď dompΓ q such that
         R,S
    ChainΓ px, y1 , . . . , yn q
and for any pn1 , . . . , nd q P Zd there exists Sn1 ,...,nd P S such that
 4. (S-Rich) π2 pSn1 ,...,nd pxi qq “ ni pi “ 1, . . . , dq
 5. (S-Int) @x : int P Γ. Sn1 ,...,nd pxq “ Rpxq
 6. (S-Acc) @x : int ref α,r
                           B P Γ. r ą 0 ñ π1 pSn1 ,...,nd pxqq “ HpRpxqq
provided that tx1 , . . . , xd u “ tx P dompΓ q | x : int ref α,r
                                                              B P Γ u.
                                                   sim
We often omit the indices L and/or Γ in ùL,Γ when they are not impor-
tant or the environments we are referring to are clear from the context. If
           sim
xH, R, T y ùL,Γ xS, ty, then we have S ‰ H by the existence of Sñ ; note that
we require such register to exist even when d “ 0. The condition (S-Rich) says
that any integer can be a future value of a reference. In other words, it assures
that we are not accidentally cutting off some non-deterministic branches. The
condition (S-Acc) corresponds to the TXZ principle we explained in Section 4.2.
Remark 3 (On the simplification). The above definition is tailored for the in-
traprocedural fragment. If we consider function calls/returns, then we need to
(i) take stacks into account and (ii) keep the “discarded environment ∆” as we
did in Appendix A .
Lemma 13 (Simulation). Assume
                         sim                        src @
               xH, R, ey ùL,Γ xS, ty and xH, R, ey ÝÝÑ H 1 , R1 , e1
                                                                     D

Then there exists a configuration of the target language xS 1 , t1 y, a lifetime envi-
ronment L, and a type environment Γ 1 such that
             @ 1 1 1 D sim                             tgt @ 1 1 D
               H , R , e ùL1 ,Γ 1 S 1 , t1 and xS, ty ÝÝÑ
                                   @      D
                                                         Ñ S ,t
                                                                             src
Proof. We prove this by case analysis on the reduction xH, R, ey ÝÝÑ xH 1 , R1 , e1 y.
In each case, once we choose t1 , L1 and Γ 1 , we need to show that L1 | Γ 1 $
e1 : τ ñ t1 . However, we will omit this argument as it is essentially identical to
the argument we did in the proof of Thm. 1. (We also implicitly assume that
L | Γ $ xH, Ry holds.) We focus on the proof of the preservation for conditions
such as (S-Prop) or (S-Acc), as these are the key properties of the translation.
We start with the important cases.
42       T. Nakayama et al.

Case: (Rs-Alias) In this case, the translation is given by the following derivation.
        L | Γ0 , x : ρx , y : ρy $ e : ρ ñ t1         t “ Tττyxρ
                                                               ρx
                                                                 y
                                                                   px, y, t1 q
                                                                                 (C-Alias)
              L | Γ0 , x : τx , y : τy $ alias px “ yq; e : ρ ñ t
Note that Ownpτx q ` Ownpτy q “ Ownpρx q ` Ownpρy q. As expected, we take
Γ0 , x : ρx , y : ρy as Γ 1 and L as L1 . We do a case analysis according to the cases
used in the definition of Tττyxρρx
                                   y
                                     .
Subcase: Ownpτx q “ Ownpρx q “ 0
   This case is trivial.
Subcase: Ownpρx q, Ownpρy q ą 0 and Ownpτy q ą 0
   In this case, we choose the following matching reduction:
                                                       D tgt @ 1 1 D
               xS, ty ” S, let x “ xfst y, snd xy in t1 ÝÝÑ
                         @
                                                           Ñ S ,t
   where S 1 :“ tStx ÞÑ xπ1 pSpyqq, π2 pSpxqqyu | S P Su. We have π1 pSñ pyqq “
   HpRpyqq for the registers Sñ P S satisfying (S-Acc) (as well as (S-Rich) and
   (S-Int)), which implies that Sñ tx ÞÑ xπ1 pSñ pyqq, π2 pSñ pxqqyu also satisfy
   (S-Acc). It is easy to see that Sñ tx ÞÑ xπ1 pSñ pyqq, π2 pSñ pxqqyu satisfies (S-
   Rich) and (S-Int) as well. We have to show that (S-Prop) is preserved.
   It suffices to consider all chains containing x. Let y1 , . . . , yn P dompΓ q
   such that ChainR,S         Γ py1 , . . . , yn q and x “ yk for some k “ 1, . . . , n. Then
               1
   ChainR,SΓ 1   py 1 , . . . , yk q holds so we can use this chain instead.
Subcase: Ownpτx q ą 0 and Ownpρx q “ 0
   We have Ownpρy q ą 0 and
                                       $
                                       & let y “ xfst x, snd yy in
                                   t ” let x “ xsnd y, snd xy in
                                       % 1
                                           t
                                                tgt
     for some t1 . Therefore we take xS, ty ÝÝÑ
                                              Ñ xS 1 , t1 y, as the matching transition,
     where
       S 1 :“ Stx ÞÑ xπ2 pSpyqq, π2 pSpxqqy , y ÞÑ xπ1 pSpxqq, π2 pSpyqqyu | S P S
                                                                                     (

     For registers Sñ that satisfy the condition such as (S-Acc), let us define
             def
         Sñ1 :“ Sñ tx ÞÑ xπ2 pSñ pyqq, π2 pSñ pxqqy , y ÞÑ xπ1 pSñ pxqqπ2 pSñ pyqqy .
     We have
                     π1 pSñ1 pyqq “ π1 pSñ pxqq                       (by the def. of Sñ1 pyq)
                                  “ HpRpxqq                                        (by (S-Acc))
                                  “ HpRpyqq.                         (since y is an alias of x)
     Hence, (S-Acc) also holds for every Sñ1 , and we can choose these regis-
     ters as the registers that satisfy the conditions (S-Rich), (S-Int) and (S-
     Acc). To show that (S-Prop) is preserved, we have to confirm that for any
                        Borrowable Fractional Ownership Types for Veriﬁcation                  43

  z P RefVarpΓ 1 q such that OwnΓ 1 pzq “ 0, there exists a prophecy chain
                                                                 1
  z, w1 , . . . , wm P dompΓ q on S 1 . If z “ x, ChainR,S   Γ 1 pz, yq holds. Otherwise,
  OwnΓ pzq “ 0, which implies that by (S-Prop), there exists z1 , . . . , zn P
  dompΓ 1 q such that ChainR,S    Γ pz, z1 , . . . , zn q. We assume x P tz, z1 , . . . , zn u
  because otherwise, it is obvious as we can take this prophecy chain also on
  S 1 . Then we must have zn “ x since Ownpτx q ą 0. In addition, π1 pS 1 pxqq “
  π2 pS 1 pyqq holds for any S 1 P S 1 . If y borrowed the ownership from x, then we
  have BLftΓ 1 pxq “ LftΓ 1 pyq; otherwise the ownership was shared and we have
                                                                    1
  LftΓ 1 pxq “ LftΓ 1 pyq. Therefore, we have ChainR,S          Γ 1 pz, z1 , . . . , zn´1 , x, yq,
  which is a prophecy chain for z on S 1 .
Remaining subcases:
  Symmetric to the previous cases.

Case: (Rs-Endlft) In this case, we must have

                         t ” assume1ďiďn pfst xi “ snd xi q; t1 ,

for some t1 where tx1 , . . . , xn u “ Γ zΓ Òα . As the matching transition, we take
           tgt
               Ñ xS 1 , t1 y where
xS, ty ÝÝÝÝÝÝÝÝÑ
        pRt-Assumeq

                 S 1 :“ S P S | π1 pSpxi qq “ π2 pSpxi qq pi “ 1, . . . , nq
                                                                            (

Note that we can chose L1 :“ LÒα and Γ 1 :“ Γ Òα in this case.
     We show that (S-Acc) and (S-Prop) hold for xS 1 , t1 y; the other conditions
are easy to check.
     First, we show that (S-Prop) holds. Let x : τ 1 P Γ 1 such that τ 1 is a reference
type. We need to find a prophecy chain starting from x. By the definition of
Γ 1 , τ 1 “ τ Òα for some τ “ int ref β,r
                                      B such that β ‰ α. When r ą 0, it is
straightforward. We consider the case where τ “ int ref β,r   B (β ‰ α) and r “ 0.
                                                                                  sim
We start by taking a prophecy chain of S; (S-Prop) of xH, R, ey ùL,Γ xS, ty
implies that there exists y1 , . . . , yn P dompΓ q such that ChainR,S  Γ px, y1 , . . . , yn q.
Let us consider the subsequence of y1 , . . . , yn obtained by removing all elements
such that LftΓ pyi q “ α. By the minimality of α such a subsequence is a prefix of
y1 , . . . , yn , say y1 , . . . , ym and BLftΓ pym q “ α. Hence we have OwnΓ 1 pym q ą 0,
                                          1
which implies that ChainR,S           Γ 1 px, y1 , . . . , ym q.
     To show (S-Acc) holds, it suffices to show that π1 pSñ pxqq “ HpRpxqq for
x : int ref β,0  α,s P Γ (s ą 0), which is a reference that regained non-zero ownership
after the lifetime termination. Here Sñ P S is the register that satisfies (S-Rich),
(S-Int) and (S-Acc), and moreover, we assume that Sñ P S 1 . (In other words,
Sñ is the register that correctly guessed the future values of x1 , . . . , xn , which
always exists.) Observe that there is a prophecy chain ChainR,S          Γ px, y1 , . . . , yn q
such that LftΓ py1 q “ ¨ ¨ ¨ “ LftΓ pyn q “ α because α is a minimal lifetime. In
this case, we have

             π1 pSñ pxqq “ π2 pSñ py1 qq      pby ChainR,S
                                                         Γ px, y1 , . . . , yn qq
44      T. Nakayama et al.

                        “ π1 pSñ py1 qq     psince Sñ P S 1 q
                           ..
                            .
                        “ π1 pSñ pyn´1 qq
                        “ π2 pSñ pyn qq
                        “ π1 pSñ pyn qq                                        (Sñ P S 1 )
                        “ HpRpyn qq                                       (by (S-Acc))
                        “ HpRpxqq                                 (since Rpxq “ Rpyn q)
                                                           sim
Therefore, (S-Acc) also stands. Hence xH 1 , R1 , T 1 y ùL1 ,Γ 1 xS 1 , t1 y holds.

Case: (Rs-Assign) We only show the preservation of (S-Acc) because preser-
vations of the other conditions are straightforward to see. In this case, there
exists x, y P Var such that t ” let x “ xy, snd xy in t1 . We take the matching
reduction from xS, ty as follows
                       tgt @
                         Ñ tStx ãÑ xSpyq, π2 pSpxqqyu | S P Su, t1
                                                                   D
               xS, ty ÝÝÑ
                                                                                        def
For each ñ P Zd , the register Sñ P S that satisfy (S-Int) is updated as Sñ1 :“
Sñ tx ãÑ xRpyq, π2 pSñ pxqqyu because Sñ pyq “ Rpyq. Hence, we have π1 pSñ1 pxqq “
Rpyq “ H 1 pRpyqq as desired. It remains to consider references aliasing to x. By
Thm. 1, no references are aliasing to x with positive ownership. Thus (S-Acc)
holds for these aliasing registers.

Case: (Rs-Deref) In this case, e must be of the form let x “ ‹y in e1 . We must
also have H 1 “ H and R1 “ Rtx ÞÑ HpRpyqqu, where HpRpyqq P Z. We proceed
by a case analysis on OwnΓ pyq.
     If OwnΓ pxq ą 0, then the last rule applied for the derivation of the transla-
tion must be (C-Deref-Pos). So we must have t ” let x “ fst y in t1 for some
t1 . We take the matching transition as
                                   D tgt @
             S, let x “ fst y in t1 ÝÝÑÑ tStx ÞÑ π1 pSpyqqu | S P Su, t1
           @                                                             D

It is easy to see that xS 1 , t1 y satisfies (S-Prop), and we are left to choose Sñ1 P S 1
satisfying (S-Rich), (S-Int) and (S-Acc). For any pn1 , . . . , nd q P Zd , we take
Sñ tx ÞÑ HpRpyqqu as such register, where Sñ P S is the register that satisfies (S-
Rich), (S-Int) and (S-Acc). Note that Sñ tx ÞÑ HpRpyqqu P S 1 because Sñ P S
and π1 pSñ pyqq “ HpRpyqq by (S-Acc). The register Sñ tx ÞÑ HpRpyqqu satisfies
(S-Rich) and (S-Acc) because Sñ does. Obviously, (S-Acc) also holds because
HpRpyqq “ R1 pxq.
     Now we consider the case where OwnΓ pyq “ 0. The last rule applied for the
derivation of the translation must be (C-Deref-Zero), and thus t must be of
the shape let x “ _ in t1 . In this case, we use (Rt-LetNondet) to match the
transition. That is, we take
                                      D tgt @
                S, let x “ _ in t1 ÝÝÑ tStx ÞÑ nu | S P S, n P Zu, t1
              @                                                            D
                     Borrowable Fractional Ownership Types for Veriﬁcation          45

as the matching transition. As in the case where OwnΓ pyq ą 0, the only non-
triviality is how to choose Sñ1 P S 1 satisfying (S-Rich), (S-Int) and (S-Acc) for
each pn1 , . . . , nd q P Zd . Again we take Sñ tx ÞÑ HpRpyqqu as such register, where
Sñ P S is the register that satisfies (S-Rich), (S-Int) and (S-Acc). Note that
Sñ tx ÞÑ HpRpyqqu P S 1 because S 1 contains all the possible integer assignment
to x.


Cases: (Rs-IfTrue), (Rs-IfFalse) We only give proof for (Rs-IfTrue). In this case,
e ” ifz x then e1 else e2 , t ” ifz x then t1 else t2 , and e1 “ e1 . We take
                                                      tgt
             xS, ty “ xS, ifz x then t1 else t2 y ÝÝÝÝÝÝÝÝÑ S 1 , t1
                                                           @         D
                                                    pRt-IfTrueq

where
                              S 1 “ tS P S | Spxq “ 0u
as the matching transition. Note that we have Sñ P S 1 for each ñ because Sñ pxq “
                             sim
Rpxq “ 0. Hence, xH, R, e1 y ùL,Γ xS 1 , t1 y is straightforward to check.

Case: (Rs-Let) This case is easily reduced to the (Rs-Alias) case.

Case: (Rs-Arith), (Rs-Newlft), (Rs-MkRef) These cases are trivial.

Cases: (Rs-Var) (Rs-Call), (Rs-AliasFail) These cases do not happen because we
omit functions and assume progression.
                                                                             \
                                                                             [
46       T. Nakayama et al.

D      Benchmark programs



     rand_choose(x, y) {            let nondet () = Random.int(0)
       if _ then x else y           let rec assume x n =
     }                                if x = n then () else assume x n

     let a = _ in                   let rand_choose x y =
     if a < 0 then () else            if nondet() < 0 then (
     let x = mkref a in                 let x’ = (fst x, nondet()) in
     let y = rand_choose(x,             let x = (snd x’, snd x) in
         mkref _) in                    (x’, x, y)
     let z = y in                     ) else (
     let b = *y + *z in                 let y’ = (fst y, nondet()) in
     alias(y = z);                      let y = (snd y’, snd y) in
     y := *y + b;                       (y’, x, y)
     assert( *x <= 3 * a )            )

                                    let main a = (
 Fig. 24. original ‘borrow-merge’     if a < 0 then () else
                                      let x = (a, nondet()) in
                                      let w = (nondet(), nondet()) in
                                      let (y, x, w) = rand_choose x w
                                        in
                                      let z = (fst y, nondet()) in
                                      let b = fst y + fst z in
                                      let y = (fst z, snd y) in
                                      let z = (snd y, snd z) in
                                      let y = (fst y + b, snd y) in
                                      assume (fst y) (snd y);
                                      assume (fst z) (snd z);
                                      assume (fst w) (snd w);
                                      assert(fst x <= 3 * a)
                                    )


                                       Fig. 25. converted ‘borrow-merge’
                      Borrowable Fractional Ownership Types for Veriﬁcation         47




  loop(a, b) {                           let nondet () = Random.int(0)
    let a_ = *a in                       let rec assume x n =
    let b_ = *b in                         if x = n then () else assume x n
    b := *b + 1;
    a := *a + 1;                         let rec loop a b =
    assert( *a = (a_ + 1));                let a_ = fst a in
    if _ then                              let b = (fst b + 1, snd b) in
      loop(b, mkref _)                     let a = (fst a + 1, snd a) in
    else                                   assert(fst a = a_ + 1);
      loop(b, a)                           if nondet() < 0 then
  }                                          loop b (nondet(), nondet())
  loop((mkref _), (mkref _))               else
                                             loop b a

Fig. 26. original ‘simple-loop’ (safe)   let main =
                                           loop (nondet(), nondet()) (nondet
                                             (), nondet())


                                          Fig. 27. converted ‘simple-loop’ (safe)




  just_rec(x) {                          let nondet () = Random.int(0)
    if _ then () else (                  let rec assume x n =
      let y = mkref _ in                   if x = n then () else assume x n
      just_rec(x)
    )                                    let rec just_rec x =
  }                                        if nondet() < 0 then ((), x) else
  let x = mkref _ in                         let y = (nondet(), nondet()) in
  let x0 = *x in                             let (r, y) = just_rec y in
  just_rec(x);                               (r, x)
  assert(x0 = *x)
                                         let main =
                                           let x = (nondet(), nondet()) in
 Fig. 28. original ‘just-rec’ (safe)       let x0 = fst x in
                                           let (_, x) = just_rec x in
                                           assert(fst x = x0)


                                            Fig. 29. converted ‘just-rec’ (safe)
48       T. Nakayama et al.



     f(p, q) {                           let nondet () = Random.int(0)
       alias(p = q);                     let rec assume x n =
       q := *q + 3                         if x = n then () else assume x n
     }
                                         let rec f p q =
     let x = mkref 1 in                    let q = (fst p, snd q) in
     let y = x in                          let p = (snd q, snd p) in
     assert( *y = *x );                    let q = (fst q + 3, snd q) in
     f(x, y);                              ((), p, q)
     assert(*x = 4)
                                         let main =
                                           let x = (1, nondet()) in
Fig. 30.    original   ‘shuﬄe-in-call’     let y = (fst x, nondet()) in
(safe)                                     assert(fst x = fst y);
                                           let (_, x, y) = f x y in
                                           assume (fst y) (snd y);
                                           assert(fst x = 4)


                                         Fig. 31. converted ‘shuﬄe-in-call’ (safe)



     takemax(x, y) {                     let nondet () = Random.int(0)
       if *x >= *y then x else           let rec assume x n =
         y                                 if x = n then () else assume x n
     }
     let x = mkref _ in                  let takemax x y =
     let y = mkref _ in                    if fst x >= fst y then (
     let z = takemax(x, y) in                let x’ = (fst x, nondet()) in
     z := *z + 1;                            let x = (snd x’, snd x) in
     assert( *x != *y )                      (x’, x, y)
                                           ) else (
                                             let y’ = (fst y, nondet()) in
 Fig. 32. original ‘inc-max’ (safe)          let y = (snd y’, snd y) in
                                             (y’, x, y)
                                           )

                                         let main =
                                           let x = (nondet(), nondet()) in
                                           let y = (nondet(), nondet()) in
                                           let (z, x, y) = takemax x y in
                                           let z = ((fst z) + 1, snd z) in
                                           assume (fst z) (snd z);
                                           assert (fst x <> fst y)


                                           Fig. 33. converted ‘inc-max’ (safe)
                      Borrowable Fractional Ownership Types for Veriﬁcation         49



  f(p, q) {                             let nondet () = Random.int(0)
    alias(p = q);                       let rec assume x n =
    q := *q + 3                           if x = n then () else assume x n
  }
                                        let rec f p q =
  let x = mkref 1 in                      let q = (fst p, snd q) in
  let y = x in                            let p = (snd q, snd p) in
  assert( *y = *x );                      let q = (fst q + 3, snd q) in
  f(x, y);                                ((), p, q)
  assert( *x = 4 )
                                        let main =
                                          let x = (1, nondet()) in
Fig. 34.   original   ‘shuﬄe-in-call’     let y = (fst x, nondet()) in
(safe)                                    assert(fst x = fst y);
                                          let (_, x, y) = f x y in
                                          assume (fst y) (snd y);
                                          assert(fst x = 4)


                                        Fig. 35. converted ‘shuﬄe-in-call’ (safe)



  loop(res, cnt) {                let nondet () = Random.int(0)
    if *cnt > 0 (                 let rec assume x n =
      cnt := cnt - 1;               if x = n then () else assume x n
      res := res + 1;
      loop(res, cnt)              let rec loop res cnt =
    ) else ()                       if fst cnt > 0 then (
  }                                   let cnt = (fst cnt - 1, snd cnt) in
                                      let res = (fst res + 1, snd res) in
  let a = _ in                        let (r, res, cnt) = loop res cnt in
  let b = _ in                        (r, res, cnt)
  let res = mkref a in              ) else ((), res, cnt)
  let cnt = mkref b in
  if b < 0 then () else           let main a b =
      (                             let res = (a, nondet()) in
    loop(res, cnt);                 let cnt = (b, nondet()) in
    assert(a + b = *res)            if b < 0 then () else (
  )                                   let res’ = (fst res, nondet()) in
                                      let res = (snd res’, snd res) in
                                      let ((), res’, cnt) = loop res’ cnt
 Fig. 36. original ‘hhk2008’          in
                                      assume (fst res’) (snd res’);
                                      assert(a + b = fst res)
                                    )


                                           Fig. 37. converted ‘hhk2008’
50        T. Nakayama et al.




     let nondet () = Random.int(0)
     let rec assume x n =
         if x = n then () else assume x n

     let minmax x y =
         if fst x < fst y then (
             let x’ = (fst x, nondet()) in
             let y’ = (fst y, nondet()) in
             ((x’, y’), x, y)
         ) else (
             let x’ = (fst x, nondet()) in
             let y’ = (fst y, nondet()) in
             ((y’, x’), x, y)
         )

     let rand_choose x y =
         if nondet() < 0 then (
             let x’ = (fst x, nondet()) in
             let x = (snd x’, snd x) in
             (x’, x, y)
         ) else (
             let y’ = (fst y, nondet()) in
             let y = (snd y’, snd y) in
             (y’, x, y)
         )

     let main =
         let x = (nondet(), nondet()) in
         let y = (nondet(), nondet()) in
         let ((p, q), x, y) = minmax x y in
         let (z, x, y) = rand_choose x y in
         assert(fst p <= fst z && fst z <= fst q);
         assume (fst p) (snd p);
         assume (fst q) (snd q);
         let z = (1, snd z) in
         assert(fst z = 1)


                               Fig. 38. converted ‘minmax’
                    Borrowable Fractional Ownership Types for Veriﬁcation     51




  rand_choose(x, y) {            let nondet () = Random.int(0)
    if _ then x else y           let rec assume x n =
  }                                if x = n then () else assume x n
  linger_dec(x) {
    x := *x - 1;                 let rand_choose x y =
    if _ then () else (            if nondet() < 0 then (
      let y = mkref _ in             let x’ = (fst x, nondet()) in
      linger_dec(                    let x = (snd x’, snd x) in
      rand_choose(x, y))             (x’, x, y)
    )                              ) else (
  }                                  let y’ = (fst y, nondet()) in
  let x = mkref _ in                 let y = (snd y’, snd y) in
  let x0 = *x in                     (y’, x, y)
  linger_dec(x);                   )
  assert(x0 > *x)
                                 let rec linger_dec x =
                                   let x = (fst x - 1, snd x) in
Fig. 39. original ‘linger-dec’     if nondet() < 0 then ((), x) else (
(safe)                               let y = (nondet(), nondet()) in
                                     let (z, x, y) = rand_choose x y in
                                     let (r, z) = linger_dec z in
                                     assume (fst z) (snd z);
                                     (r, x)
                                   )

                                 let main =
                                   let x = (nondet(), nondet()) in
                                   let x0 = fst x in
                                   let x’ = (fst x, nondet()) in
                                   let x = (snd x’, snd x) in
                                   let (_, x’) = linger_dec x’ in
                                   assume (fst x’) (snd x’);
                                   assert(x0 > fst x)


                                     Fig. 40. converted ‘linger-dec’ (safe)
