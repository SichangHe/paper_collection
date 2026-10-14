                                             Borrowing Safe Pointers from Rust in SPARK

                                                  Georges-Axel Jaloyan1⋆ , Yannick Moy2 , and Andrei Paskevich3,4
                                                                       1
                                                                          École Normale Supérieure,
                                                                  PSL Research University, Paris, France
                                                                         2
                                                                           AdaCore, Paris, France
                                                               3
                                                                 Laboratoire de Recherche en Informatique,
                                                               Université Paris-Sud, CNRS, Orsay, F-91405
                                                        4
                                                          Inria Saclay, Université Paris Saclay, Palaiseau, F-91120
arXiv:1805.05576v1 [cs.PL] 15 May 2018




                                                 Abstract. In the ﬁeld of deductive software veriﬁcation, programs with
                                                 pointers present a major challenge due to pointer aliasing. In this paper,
                                                 we introduce pointers to SPARK, a well-deﬁned subset of the Ada lan-
                                                 guage, intended for formal veriﬁcation of mission-critical software. Our
                                                 solution uses a permission-based static alias analysis method inspired
                                                 by Rust’s borrow-checker and affine types, and enforces the Concurrent
                                                 Read, Exclusive Write policy. This analysis has been implemented in the
                                                 GNAT Ada compiler and tested against a number of challenging exam-
                                                 ples. In the paper, we give a formal presentation of the analysis rules for
                                                 a miniature version of SPARK and prove their soundness. We discuss
                                                 the implementation and compare our solution with Rust.


                                         1     Introduction
                                         SPARK [1] is a subset of the Ada programming language targeted at safety-
                                         and security-critical applications. SPARK restrictions ensure that the behavior
                                         of a SPARK program is unambiguously defined, and simple enough that formal
                                         verification tools can perform an automatic diagnosis of conformance between a
                                         program specification and its implementation.
                                             As a consequence of SPARK’s focus on automation and usability, it forbids
                                         the use of programming language features that either prevent automatic proof,
                                         or make it possible only at the expense of extensive user effort in annotating the
                                         program. The lack of support for pointers in SPARK is the main example of this
                                         choice. While it is possible to exclude parts of the programs that manipulate
                                         pointers from analysis, it would be preferable to support pointers when their use
                                         does not prevent formal verification.
                                             Among the various problems related to the use of pointers in the context of
                                         formal program verification, the most difficult problem is the possibility that two
                                         names refer to overlapping memory locations, a.k.a. aliasing. Formal verification
                                         platforms that support pointer aliasing like Frama-C [2] require users to annotate
                                         ⋆
                                             This work is partly supported by the Joint Laboratory ProofInUse (ANR-13-LAB3-
                                             0007) and project VECOLIB (ANR-14-CE28-0018) of the French National Research
                                             Agency (ANR).
2        Georges-Axel Jaloyan et al.

programs to specify when pointers are not aliased. This can take the form of
inequalities between pointers when a typed memory model is used, or the form of
separation predicates between memory zones when an untyped memory model is
used. In both cases, the annotation burden is acceptable for leaf functions which
manipulate single-level pointers, and quickly becomes overwhelming for functions
that manipulate pointer-rich data structures. In parallel to the increased cost of
annotations, the benefits of automation decrease, as automatic provers have
difficulties reasoning explicitly with these inequalities and separation predicates.
    Programs often rely on non-aliasing in general for correctness, when such
aliasing would introduce interferences between two unrelated names. We call such
aliasing potentially harmful when a memory location modified through one name
could be read through another name, within the scope of a verification condition.
Otherwise, the aliasing is benign, when the memory location is only read through
both names. A reasonable restriction for formal program verification is thus to
forbid potentially harmful aliasing of names. The difficulty is then to guarantee
the absence of potentially harmful aliasing. The following code shows an example
where we want analysis to be able to rely on the non-aliasing of parameters X
and Y to prove the postcondition of the procedure Assign_Incr:
    procedure Assign_Incr (X , Y : in out Integer_Poin te r )
       with Post = > Y . all = X . all + 1
    is
    begin
       Y . all := X . all + 1;
    end Assign_Incr ;
     In this work, we present the first step for the inclusion of pointers in the
Ada language subset supported in SPARK. As our main contribution, we show
that it is possible to borrow and adapt the ideas underlying the safe support
for pointers in permission-based languages like Rust, to safely restrict the use
of pointers in usual imperative languages like Ada. This adaptation is based on
a possible division of work between a permission-based anti-aliasing analysis,
lifetime management by typing, and the use of a formal verification platform
for checking non-nullity of accessed pointers. For example, these rules prevent
aliasing between parameters X and Y in the code of procedure Assign_Incr
above, which makes it possible to treat pointers in proof like records with a single
field corresponding to the type of the object pointed to. Thus, the verification
condition corresponding to the postcondition of procedure Assign_Incr has a
form (using get/set to access the field all of variables X and Y) that can readily
be proved by automatic provers:
    hypothesis: Y’ = set(Y, all, get(X, all) + 1)
    goal:       get(Y’, all) = get(X, all) + 1
    In Section 2, we present a formalization of the non-aliasing rules enforced
by the permission-based analysis, including proof of non-aliasing guarantees. In
Section 3, we describe a concrete implementation of the analysis inside the open-
source GNAT compiler for Ada which is part of GCC. We survey related works
in Section 4, in particular with respect to Rust.
                             Borrowing Safe Pointers from Rust in SPARK         3

2   Alias Analysis

In Ada/SPARK code, the access to memory areas is given through paths that
start with an identifier (a variable name) and follow through record fields, array
indices, or through a special field all, which corresponds to pointer dereferenc-
ing. In this paper, we only consider record and pointer types, and discuss the
treatment of arrays in Section 3.
    As an example, we use the following Ada type, describing singly linked lists
where each node carries a boolean flag and a pointer to a shared integer value.
 type List is record
   Flag : Boolean ;
   Key : access Integer ;
   Next : access List ;
 end record ;

    Given a variable A : List, the paths A.Flag, A.Key.all, A.Next.all.Key
are valid and their respective types are Boolean, Integer, and access Integer
(a pointer to an Integer). The important difference between pointers and records
in Ada is that—similarly to C—assignment of a record copies the values of fields,
whereas assignment of a pointer only copies the address and creates an alias.
    The alias analysis procedure runs after the type checking. The idea is to
associate one of the four permissions—RW, R, W or NO—to each possible path
(starting from the available variables) at each sequence point in the program.
    The read-only permission R allows us to read any value accessible from the
path: use it in a computation, or pass it as an in parameter in a procedure call.
As a consequence, if a given path has the R permission, then each valid extension
of this path also has it.
    The write-only permission W allows us to modify memory occupied by the
value: use it on the left-hand side in an assignment or pass it as an out param-
eter in a procedure call. For example, having a write permission for a path of
type List allows us to modify the Flag field or to change the addresses stored
in the pointer fields Key and Next. However, this does not necessarily give us the
permission to modify memory accessible from those pointers. Indeed, to deref-
erence a pointer, we must read the address stored in it, which requires the read
permission. Thus, the W permission only propagates to path extensions that do
not dereference pointers, i.e., do not contain additional all fields.
    The read-write permission RW combines the properties of the R and W per-
missions and grants the full ownership of the path and every value accessible
from it. In particular, the RW permission propagates to all valid path extensions
including those that dereference pointers. The RW permission is required to pass
a value as an in-out parameter in a procedure call.
    Execution of program statements changes permissions. For example, allo-
cating a new non-initialised memory area assigns the W permission to every
value stored in this area. Thus, after the statement P := new List, the paths P,
P.all, P.all.Flag, P.all.Key, and P.all.Next have permission W. All strict
extensions of P.all.Key and P.all.Next receive permission NO, that is, no
4      Georges-Axel Jaloyan et al.


procedure P1                         procedure P2
  (A , B : in out List ) is            (A , B : in out Integer_Poin te r ) is
begin                                begin
  A := B ;                             while B . all > 0 loop
  B . Flag := True ;                      A . all := A . all + 1;
  B . Key . all := 42;                    B . all := B . all - 1;
end P1 ;                                  A := B ;
                                       end loop ;
                                     end P2 ;

                 Fig. 1. Examples of potentially harmful aliasing.


permission. Indeed, since the pointers P.all.Key and P.all.Next are not ini-
tialised, neither reads nor writes under them make any sense. Another simple
example of permission change is the procedure call: all out parameters must be
assigned by the callee and receive the RW permission after the call.
    The assignment statement is more complicated and several cases must be
considered. If we assign a value that does not contain pointers (say, an integer
or a pointer-free record), the whole value is copied into the left-hand side, and
we only need to check that we have the appropriate permissions: W or RW for
the left-hand side and R or RW for the right-hand side. However, whenever we
copy a pointer, an alias is created. We want to make the left-hand side the
new full owner of the value (i.e., give it the RW permission), and therefore,
after the permission checks, we must revoke the permissions from the right-
hand side, to avoid potentially harmful aliasing. The permission checks are also
slightly different in this case, as we require the right-hand side to have the RW
permission in order to move it to the left-hand side.
    Let us now consider several simple programs and see how the permission
checks allow us to detect potentially harmful aliasing.
    Procedure P1 in Fig. 1 receives two in-out parameters A and B of type
List. At the start of the procedure, all in-out parameters assume permission
RW. In particular, this implies that each in-out parameter is separated from
all other parameters (in fact, only the in parameters may alias each other).
The first assignment copies the structure B into A. Thus, the paths A.Flag,
A.Key, and A.Next are separated, respectively, from B.Flag, B.Key, and B.Next.
However, the paths A.Key.all and B.Key.all are aliased, and A.Next.all and
B.Next.all are aliased as well.
    The first assignment does not change the permissions of A and its extensions:
they retain the RW permission and keep the full ownership of their respective
memory areas, even if the areas themselves have changed. The paths under
B, however, must relinquish (some of) their permissions. The paths B.Key.all
and B.Next.all as well as all their extensions get the NO permission, that
is, lose both read and write permissions. This is necessary, as the ownership
over their memory areas is transferred to the corresponding paths under A. The
paths B, B.Key, and B.Next lose the read permission but keep the write-only W
                              Borrowing Safe Pointers from Rust in SPARK        5

permission. Indeed, we forbid reading from memory that can be altered through
a concurrent path. However, it is allowed to “redirect” the pointers B.Key and
B.Next, either by assigning those fields directly or by copying some different
record into B. The field B.Flag is not aliased, nor has it aliased extensions, and
thus retains the initial RW permission. This RW permission allows us to perform
the assignment B.Flag := True on the next line.
    The third assignment, however, is now illegal, since B.Key.all does not have
the write permission anymore. What is more, at the end of the procedure the
in-out parameters A and B are not separated. This is forbidden, as the caller
assumes that all out and in-out parameters are separated after the call just as
they were before.
    Procedure P2 in Fig. 1 receives two pointers A and B, and manipulates them
inside a while loop. Since the permissions are assigned statically, we must ensure
that at the end of a single iteration, we did not lose the permissions necessary
for the next iteration. This requirement is violated in the example: after the
last assignment A := B, the path B receives permission W and the path B.all,
permission NO, as B.all is now an alias of A.all. The new permissions for
B and B.all are thus weaker than the original ones (RW for both), and the
procedure is rejected. Should it be accepted, we would have conflicting memory
modifications from two aliased paths at the beginning of the next iteration.



2.1     µSPARK language


For the purposes of formal presentation, we introduce µSPARK, a small subset
of SPARK featuring pointers, records, loops, and procedure calls. We present
the syntax and semantics of µSPARK, and define the rules for static analysis of
alias safety.
    The data types of µSPARK are as follows:

          type ::= Integer | Real | Boolean         scalar type
                 | access type                      access type (pointer)
                 | ident                            record type

      Every µSPARK program starts with a list of record type declarations:

                  record ::= type ident is record f ield⋆; end
                   f ield ::= ident : type

    We require all field names to be distinct. The field types must not refer to
the record types declared later in the list. Recursive record types are allowed:
a field of a record type R can contain pointers to R (written access R). We
discuss the handling of array types in Section 3.
6        Georges-Axel Jaloyan et al.

     The syntax of µSPARK statements is defined by the following rules:

    path ::= ident                                         variable
           | path . ident                                  record field
           | path . all                                    pointer dereference

    expr ::= path                                          l-value
           | 42 | 3.14 | True | False | . . .              scalar value
           | expr ( + | - | < | = | . . . ) expr           binary operator
           | path’Access                                   address of an l-value
           | null                                          null pointer

    stmt ::= path := expr                                  assignment
           | path := new type                              allocation
           | if expr then stmt⋆; else stmt⋆; end           conditional
           | while expr loop stmt⋆; end                    “while” loop
           | ident ( expr ⋆, )                             procedure call

  Following the record type declarations, a µSPARK program contains a set of
mutually recursive procedure declarations:

    procedure ::= procedure ident ( param⋆; ) is local;⋆ begin stmt⋆; end
       param ::= ident : ( in | in-out | out ) type
          local ::= ident : type

We require all formal parameters and local variables in a procedure to have
distinct names. A procedure call can only pass left-values (i.e., paths) for in-out
and out parameters. The execution starts from a procedure named Main with
the empty parameter list.
    The type system for µSPARK is rather standard and we do not present it here
in full. We assume that binary operators only operate on scalar types. The null
pointer can have any pointer type access τ . The dereference operator .all
converts a pointer type access τ to τ . The access operator ’Access applied
to an l-value of type τ returns the corresponding pointer type access τ . The
allocation statement p := new τ requires the path p to have type access τ . In
what follows, we only consider well-typed µSPARK programs.
    On the semantic level, we need to distinguish the units of allocation, such as
whole records, from the units of access, such as individual record fields. We use
the term location to refer to the memory area occupied by an allocated value.
We treat locations as elements of an abstract infinite set, and denote them with
letter ℓ. We use the term address to designate either a location, denoted ℓ, or a
specific component inside the location of a record, denoted ℓ.f.g, where f and
g are field names (assuming that at ℓ we have a record whose field f is itself a
record with a field g). A value is either a scalar, an address, a null pointer or a
record, that is, a finite mapping from field names to values.
    A µSPARK program is executed in the context defined by a binding Υ that
maps variable names to addresses and a store Σ that maps locations to values.
                               Borrowing Safe Pointers from Rust in SPARK           7

By a slight abuse of notation, we apply Σ to arbitrary addresses, so that Σ(ℓ.f )
is Σ(ℓ)(f ), the value of the field f of the record value stored in Σ at ℓ. Similarly,
we write Σ[ℓ.f 7→ v] to denote an update of a single field in a record, that is,
Σ[ℓ 7→ Σ(ℓ)[f 7→ v]].
     We use big-step operational semantics and write Υ · Σ · s ⇓ Σ ′ to denote that
µSPARK statement s, when evaluated under binding Υ and store Σ, terminates
with the state of the store Σ ′ . We extend this notation to sequences of statements
s̄ in an obvious way. In this paper, we do not consider diverging statements.
     The evaluation of expressions is effect-free and is denoted JeKΥΣ . We also need
to evaluate l-values to the corresponding addresses in the store, written hpiΥΣ ,
where p is the evaluated path. Illicit operations, such as dereferencing a null
pointer, cannot be evaluated and stall the execution (blocking semantics). In the
formal rules below, c stands for a scalar constant and ⊙, for a binary operator:

      hxiΥΣ = Υ (x)        hp.f iΥΣ = hpiΥΣ .f                hp.alliΥΣ = JpKΥΣ

      JcKΥΣ = c              JpKΥΣ = Σ(hpiΥΣ )            Jp’AccessKΥΣ = hpiΥΣ

                       Je1 ⊙ e2 KΥΣ = Je1 KΥΣ ⊙ Je2 KΥΣ        JnullKΥΣ = null

    Allocation adds a fresh address to the store, mapping it to a default value
for the corresponding type: 0 for Integer, False for Boolean, null for the
access types, and for the record types, a record value where each field has the
default value. Notice that since pointers are initialised to null, there is no deep
allocation. We write τ to denote the default value of type τ .
    The evaluation rules are given in Figure 2. In the (E-call) rule, we evaluate
the procedure body in the dedicated context ΥP · ΣP . This context binds the
in parameters to fresh locations containing the values of the respective expres-
sion arguments, binds the in-out and out parameters to the addresses of the
respective l-value arguments, and allocates memory for the local variables. For
simplicity, we do not reclaim memory on return from a procedure call, and thus
avoid dangling pointers. In Ada and SPARK, this issue is handled separately,
using scope-based memory pools, and does not need to be addressed by our
analysis procedure.

2.2    Access policies, transformers, and alias safety rules
We denote paths with letters p and q. We write p ⊏ q to denote that p is a strict
prefix of q or, equivalently, q is a strict extension of p. In what follows, we always
mean strict prefixes and extensions, unless explicitly said otherwise.
    In the typing context of a given procedure, a well-typed path is said to be
deep if it has an extension of an access type, otherwise it is called shallow. We
extend these notions to types: a type τ is deep (resp. shallow) if and only if a
τ -typed path is deep (resp. shallow). In other words, a path or a type is deep if
a pointer can be reached from it, and shallow otherwise. For example, the List
type in Section 2 is a deep type, and so is access Integer, whereas any scalar
type or any record with scalar fields only is shallow.
8       Georges-Axel Jaloyan et al.

                                                   JeKΥΣ = v
                                                                                                            (E-assign)
                                    Υ · Σ · p := e ⇓ Σ[ hpiΥΣ 7→ v ]
                                                  ℓ 6∈ dom Σ
                                                                                                            (E-alloc)
                           Υ · Σ · p := new τ ⇓ Σ[ hpiΥΣ 7→ ℓ, ℓ 7→ τ ]

                                  JeKΥΣ = True             Υ · Σ · s̄1 ⇓ Σ ′
                                                                                                            (E-ifTrue)
                                Υ · Σ · if e then s̄1 else s̄2 ⇓ Σ ′

                                  JeKΥΣ = False            Υ · Σ · s̄2 ⇓ Σ ′
                                                                                                        (E-ifFalse)
                                Υ · Σ · if e then s̄1 else s̄2 ⇓ Σ ′

             JeKΥΣ = True           Υ · Σ · (s̄ ; while e loop s̄ end) ⇓ Σ ′
                                                                                                   (E-whileTrue)
                               Υ · Σ · while e loop s̄ end ⇓ Σ ′

                                               JeKΥΣ = False
                                                                                                  (E-whileFalse)
                                  Υ · Σ · while e loop s̄ end ⇓ Σ
       procedure P ( a1 : in τa1 ; . . . ; b1 : in-out τb1 ; . . . ; c1 : out τc1 ; . . . )
                   is d1 : τd1 ; . . . begin s̄ end is declared in the program
                 ℓa1 , . . . , ℓd1 , . . . 6∈ dom Σ              Jea1 KΥΣ , . . . = va1 , . . .
       ΥP = [ a1 7→ ℓa1 , . . . , b1 7→ hpb1 iΥΣ , . . . , c1 7→ hqc1 iΥΣ , . . . , d1 7→ ℓd1 , . . . ]
        ΣP = Σ[ ℓa1 7→ va1 , . . . , ℓd1 7→ τd1 , . . . ]                     ΥP · ΣP · s̄ ⇓ Σ ′
                                                                                                              (E-call)
                           Υ · Σ · P (ea1 , . . . , pb1 , . . . , qc1 , . . .) ⇓ Σ ′

                 Fig. 2. Semantics of µSPARK (terminating statements).



    An extension q of a path p is called a near extension if it has as many pointer
dereferences as p, otherwise it is a far extension. For instance, given a variable
A of type List, the paths A.Flag, A.Key, and A.Next are the near extensions
of A, whereas A.Key.all, A.Next.all, and their extensions are far extensions,
since they all create an additional pointer dereference by passing through all.
    We say that sequence points are the program points before or after a given
statement. For each sequence point in a given µSPARK program, we statically
compute an access policy: a partial function that maps each well-typed path to
one of the four permissions: RW, R, W, and NO, which form a diamond lattice:
RW > R|W > NO. We denote permissions with π and access policies with Π.
    Permission transformers modify policies at a given path, as well as its prefixes
                                            T
and extensions. Symbolically, we write Π −  →p Π ′ to denote that policy Π ′ results
                                                                                                  T1 # T2
from application of transformer T to Π at path p. We write Π −−−−→p Π ′ as an
                    1      T
                           2   ′     T              ′′    1   ′′ 2  ′                       T                T
abbreviation for Π −→ p # −→p Π (that is, for some Π , Π −→p Π −→p Π ).
                T                                                      T        T
We write Π − →p,q Π ′ as an abbreviation for Π − →p # −→q Π ′ .
   Permission transformers can also apply to expressions, which consists in up-
dating the policy for every path in the expression. This only includes paths that
occur as sub-expressions: in an expression X.f.g + Y.h, only the paths X.f.g
                                        Borrowing Safe Pointers from Rust in SPARK                         9

                                    move         check W # fresh RW # lift
                                Π −−−→e # −−−−−−−−−−−−−−→p Π ′
                                                                                               (P-assign)
                                              Π · p := e → Π ′
                                   check W        fresh W # cut # block
                              Π −−−−−→p # −−−−−−−−−−−−→p.all Π ′
                                                                                               (P-alloc)
                                           Π · p := new τ → Π ′
   check R
Π −−−−→e Π           Π · s̄1 → Π1              Π · s̄2 → Π2            ∀p. Π ′ (p) = Π1 (p) ∧ Π2 (p)
                                                                                                       (P-if)
                            Π · if e then s̄1 else s̄2 end → Π ′
                       check R
                   Π −−−−→e Π                 Π · s̄ → Π ′           ∀π. Π ′ (π) > Π(π)
                                                                                               (P-while)
                                     Π · while e loop s̄ end → Π

     procedure P ( a1 : in τa1 ; . . . ; b1 : in-out τb1 ; . . . ; c1 : out τc1 ; . . . )
                          is · · · begin s̄ end is declared in the program
       check R # observe              check RW # borrow                check W # borrow
    Π −−−−−−−−−−→ea1 ,... # −−−−−−−−−−−→pb1 ,... # −−−−−−−−−−→qc1 ,... Π ′′
                                     fresh RW # lift
                                Π −−−−−−−−→pb1 ,...,qc1 ,... Π ′
                                                                                                 (P-call)
                           Π · P (ea1 , . . . , pb1 , . . . , qc1 , . . .) → Π ′

                            Fig. 3. Alias safety rules for statements.



and Y.h are concerned, whereas X, X.f and Y are not. The order in which the
individual paths are treated must not affect the final result.
    We define the rules of alias safety for µSPARK statements in the context of
a current access policy. An alias-safe statement yields an updated policy which
is used to check the subsequent statement. We write Π · s → Π ′ to denote that
statement s is safe with respect to policy Π and yields the updated policy Π ′ . We
extend this notation to sequences of statements s̄ in an obvious way. The rules
for checking the alias safety of statements are given in Fig. 3. These rules use
a number of permission transformers such as ‘fresh’, ‘check’, ‘move’, ‘observe’,
and ‘borrow’, which we define and explain below.
    Let us start with the (P-assign) rule. Assignments grant the full ownership
over the copied value to the left-hand side. If we copy a value of a shallow
type, we merely have to ensure that the right-hand side has the read permission.
Whenever we copy a deep-typed value, aliases may be created, and we must
check that the right-hand side is initially the sole owner of the copied value
(that is, possesses the RW permission) and revoke the ownership from it.
    To define the ‘move’ transformer that handles permissions for the right-hand
side of an assignment, we need to introduce several simpler transformers.

Definition 1. Permission transformer check π does not modify the access policy
and only verifies that a given path p has permission π or greater. In other words,
   check π
Π −−−−→p Π ′ if and only if Π(p) > π and Π = Π ′ . This transformer also
                                    check π                                  check π
applies to expressions: Π −−−−→e Π ′ states that Π −−−−→p Π ′ (= Π) for every
path p occurring in e.
10     Georges-Axel Jaloyan et al.

Definition 2. Permission transformer fresh π assigns permission π to a given
path p and all its extensions.

Definition 3. Permission transformer cut assigns restricted permissions to a
deep path p and its extensions: the path p and its near deep extensions receive
permission W, the near shallow extensions keep their current permissions, and
the far extensions receive permission NO.

    Going back to the procedure P1 in Fig. 1, the change of permissions on the
right-hand side after the assignment A := B corresponds to the definition of ‘cut’.
In the case where the right-hand side of an assignment is not simply a variable,
but a deep path or a ’Access expression, we also need to change permissions of
the prefixes, to reflect the ownership transfer.

Definition 4. Permission transformer block propagates the loss of the read per-
mission from a given path to all its prefixes. Formally, it is defined by the fol-
lowing rules, where x stands for a variable and f for a field name:
                                                           block
                                            Π[p 7→ W] −−−→p Π ′
                   block                           block
                Π −−−→x Π                       Π −−−→p.all Π ′
                                                                   block
                Π(p) = NO            Π(p) > W       Π[p 7→ W] −−−→p Π ′
                  block                            block
                Π −−−→p.f Π                     Π −−−→p.f Π ′

Definition 5. Permission transformer drop propagates the loss of both read and
write permissions from a given path to its prefixes up to the first pointer, and
propagates the loss of the read permission afterwards:
                                        block                                 drop
                           Π[p 7→ W] −−−→p Π ′               Π[p 7→ NO] −−−→p Π ′
         drop                    drop                                  drop
      Π −−−→x Π               Π −−−→p.all Π ′                      Π −−−→p.f Π ′

Definition 6. Permission transformer move applies to expressions:
                                        move                 check R
 – if e has a shallow type, then Π −−−→e Π ′ ⇔ Π −−−−→e Π ′ ;
                                  move         check RW # cut # block
 – if e is a deep path p, then Π −−−→e Π ′ ⇔ Π −−−−−−−−−−−−−→p Π ′ ;
                                move                check RW # fresh NO # drop
 – if e is p’Access, then Π −−−→e Π ′ ⇔ Π −−−−−−−−−−−−−−−−→p Π ′ ;
                         move
 – if e is null, then Π −−−→e Π ′ ⇔ Π ′ = Π.

    To further illustrate the ‘move’ transformer, let us consider two variables P
and Q of type access List and an assignment P := Q.all.Next. We assume
that Q and all its extensions have full ownership (RW) before the assignment. We
apply the second case in the definition of ‘move’ to the deep path Q.all.Next.
The ‘check RW’ condition is verified, and the ‘cut’ transformer sets the per-
mission for Q.all.Next to W and the permission for Q.all.Next.all and all
its extensions to NO. Indeed, P.all becomes an alias of Q.all.Next.all and
steals the full ownership for this memory area. However, we still can reassign
                                 Borrowing Safe Pointers from Rust in SPARK    11

Q.all.Next to a different address. Moreover, we still can write some new values
into Q.all or Q, without compromising safety. This is enforced by the application
of the ‘block’ transformer at the end. We cannot keep the read permission for Q
or Q.all, since it implies the read access to the data under Q.all.Next.all.
    Now, let a variable R have type access Boolean and consider the assignment
R := Q.all.Flag’Access. We apply the third case in the definition of ‘move’.
Assuming once again that Q has full ownership over its value, the ‘check RW’
condition for Q.all.Flag is verified. Since the ownership of this Boolean value is
now transferred to R.all, we must revoke all permissions from Q.all.Flag (and
its extensions, if it had any), which is enforced by ‘fresh NO’. Moreover, since
writing into the record Q.all overwrites the Flag field, we must also revoke all
permissions from Q.all. This is done by the ‘drop’ transformer. Notice that the
permissions for Q.all.Key and Q.all.Next are not affected: we can still read
and modify those fields, as they are not aliased with other paths. Furthermore,
modifying the pointer Q itself is allowed, which is why ‘drop’ becomes ‘block’
after rising past all.
    Finally, we need to describe the change of permissions on the left-hand side
of an assignment, in order to reflect the gain of the full ownership. The idea is
that as soon as we have the full ownership for each field of a record, we can
assume the full ownership of the whole record, and similarly for pointers.
Definition 7. Permission transformer lift propagates the RW permission from
a given path to its prefixes, wherever possible:
                                                                       lift
                                                         Π[p 7→ RW] −−→p Π ′
                         lift                                  lift
                      Π −−→x Π                              Π −−→p.all Π ′
                                            lift
      ∀q ⊐ p. Π(q) = RW         Π[p 7→ RW] −−→p Π ′      ∃q ⊐ p. Π(q) 6= RW
                        lift                                    lift
                    Π −−→p.f Π ′                             Π −−→p.f Π

    In the (P-assign) rule, we revoke the permissions from the right-hand side of
an assignment before granting the ownership to the left-hand side. This is done
in order to prevent creation of circular data structures. Consider an assignment
A.Next := A’Access, where A has type List. According to the definition of
‘move’, path A and all its extensions receive permission NO. This makes the
left-hand side A.Next fail the write permission check.
    Allocations p := new τ are handled by the (P-alloc) rule. As long as the
memory area under the pointer p is not explicitly initialised by the program code,
no read permission is granted for p, nor its extensions and prefixes. Moreover,
since the pointer fields (if any) in the allocated memory are not accessible yet,
no permission at all can be given for the far extensions of p. This is enforced by
the ‘cut’ transformer.
    In a conditional statement, the policies at the end of the two branches are
merged selecting the most restrictive permission for each path. Loops require
that no permissions are lost at the end of a loop iteration, compared to the
entry, as explained above for procedure P2 in Fig. 1.
12     Georges-Axel Jaloyan et al.

    Procedure calls guarantee to the callee that every argument with mode in,
in-out, or out has at least permission R, RW or W, respectively. To ensure
the absence of potentially harmful aliasing, we revoke the necessary permissions
using the ‘observe’ and ‘borrow’ transformers.

Definition 8. Permission transformer borrow assigns permission NO to a given
path p and all its prefixes and extensions.

Definition 9. Permission transformer freeze removes the write permission from
a given path p and all its prefixes and extensions. In other words, freeze assigns
to each path q comparable to p the minimum permission Π(q) ∧ R.

Definition 10. Permission transformer observe applies to expressions:
                                               observe
 – if e has a shallow type, then Π −−−−→e Π ′ ⇔ Π ′ = Π;
                                         observe                    freeze
 – if e is a deep path p, then Π −−−−→e Π ′ ⇔ Π −−−→p Π ′ ;
                                     observe                    freeze
 – if e is p’Access, then Π −−−−→e Π ′ ⇔ Π −−−→p Π ′ ;
                             observe
 – if e is null, then Π −−−−→e Π ′ ⇔ Π ′ = Π.

    We remove the write permission from the deep-typed in parameters using
the ‘observe’ transformer, in order to allow aliasing between the read-only paths.
As for the in-out and out parameters, we transfer the full ownership over them
to the callee, which is reflected by dropping every permission on the caller’s side
using ‘borrow’.
    In the (P-call) rule, we revoke permissions right after checking them for
each parameter. In this way, we cannot pass, for example, the same path as an
in and in-out parameter in the same call. Indeed, the ‘observe’ transformer
will remove the write permission, which is required by ‘check RW’ later in the
transformer chain. At the end of the call, the callee transfers to the caller the
full ownership over each in-out and out parameter.
    We apply our alias safety analysis to each procedure declaration. We start
with an empty access policy, denoted ∅. Then we fill the policy with the permis-
sions for the formal parameters and the local variables and check the procedure
body. At the end, we verify that every in-out and out parameter has the RW
permission. Formally, this is expressed with the following rule:

          fresh R         fresh RW              fresh W # cut            fresh W # cut
      ∅ −−−−→a1 ,... # −−−−−→b1 ,... # −−−−−−−−→c1 ,... # −−−−−−−−→d1 ,... Π ′
            Π ′ · s̄ → Π ′′    Π ′′ (b1 ) = · · · = Π ′′ (c1 ) = · · · = RW
     procedure P ( a1 : in τa1 ; . . . ; b1 : in-out τb1 ; . . . ; c1 : out τc1 ; . . . )
                                   is d1 : τd1 ; . . . begin s̄ end is alias-safe


We say that a µSPARK program is alias-safe if all its procedures are.
                              Borrowing Safe Pointers from Rust in SPARK         13

2.3    Soundness
As the end of the analysis, an alias-safe program has an access policy associ-
ated to each sequence point in it. We say that an access policy Π is consistent
whenever it satisfies the following conditions for all valid paths π, π.f , π.all:

      Π(π) = RW =⇒ Π(π.f ) = RW          Π(π) = RW =⇒ Π(π.all) = RW             (1)
       Π(π) = R =⇒ Π(π.f ) = R            Π(π) = R =⇒ Π(π.all) = R              (2)
       Π(π) = W =⇒ Π(π.f ) ≥ W                                                  (3)

These invariants correspond to the informal explanations given in Section 2.
Invariant (1) states that the full ownership over a value propagates to all values
reachable from it. Invariant (2) states that the read-only permission must also
propagate to all extensions. Indeed, a modification of a reachable component
can be observed from any prefix. Invariant (3) states that write permission over
a record value implies a write permission over each of its fields. However, the
write permission does not necessarily propagate across pointer dereference.
Lemma 1 (Policy consistency). The alias safety rules in Fig. 3 preserve
policy consistency.
    When, during an execution, we arrive at a given sequence point with the set
of variable bindings Υ , store Σ, and statically computed and consistent access
policy Π, we say that the state of the execution respects the Concurrent Read,
Exclusive Write condition (CREW), if and only if for any two distinct valid
paths p and q, hpiΥΣ = hqiΥΣ ∧ Π(p) ≥ W =⇒ Π(q) = NO.
    The main result about the soundness of our approach is as follows:
Theorem 1 (Soundness). A terminating evaluation of a well-typed alias-safe
µSPARK program respects the CREW condition at every sequence point.
    The full proof, for a slightly different definition of µSPARK, is given in [3].
The argument proceeds by induction on the evaluation derivation, following the
rules in Figure 2. The only difficult cases are assignment, where the required
permission withdrawal is ensured by the ‘move’ transformer, and procedure call,
where the chain of ‘observe’ and ‘borrow’ transformers, together with the cor-
responding checks, on the caller’s side, ensures that the CREW condition is
respected at the beginning of the callee.


3     Implementation
We have implemented the permission rules in the GNAT compiler for Ada, which
is part of GCC. The implementation consists in 3700 lines in Ada. The analysis is
triggered by using the debug switch -gnatdF and setting the context for formal
verification of SPARK code with switch -gnatd.F and aspect SPARK_Mode.
    Access policies are infinitely big in presence of recursive types, which we took
into account in our implementation with a lazy implementation of permission
trees. Permission trees start with a depth of one, and are expanded on demand.
14     Georges-Axel Jaloyan et al.

    The permission rules presented in Section 2 only address a subset of SPARK.
Complete SPARK differs from µSPARK on several points, which have been
taken into account when designing the full set of rules. For arrays, permission
rules are adapted to apply to all elements, without taking into account the exact
index of that element, which may not be known statically in general. Besides
procedures, SPARK has functions, which return values and cannot perform side-
effects. Functions take only parameters of mode in and can be called inside
expressions. Our permission rules are augmented with an implicit move of the
values returned by functions, which allows us to support constructors.
    In our formalization, we considered that every shallow in parameter is passed
by-copy, which is not the case in SPARK. In our implementation, we correctly
distinguish parameters of by-copy types (typically scalars) and parameters which
may be passed by-copy or by-reference, which we treat as deep parameters (ex-
cept for function in parameters, as functions cannot have side effects, and in
particular cannot write in their parameters even under dereference).
    Loops in SPARK also differ on two accounts from the loops in our formaliza-
tion: besides ‘while’ loops, SPARK also defines ‘for’ loops and plain loops (with
no exit condition), and exit statements inside a loop allow exiting any enclosing
loop. In our implementation, we take these into account to create the correct
merged context for analyzing the code after the loop.
    The analysis has been tested on four test suites, including the regression
testsuite of the GNAT compiler (17041 tests [4]) and the regression testsuite of
the SPARK product (2087 tests), which detected 30 regressions, most of them
related to object oriented features that the current analysis is not able to han-
dle. We also wrote a dedicated testsuite [5] containing 20 tests inspired by the
examples given in the Rust borrow-checker documentation [6].


4     Related Works
4.1   Comparison with Rust
The following section compares Rust and SPARK on some features and con-
structs that seem relevant to the authors. Both prevent harmful aliasing in the
source code, whereas different design choices affect their respective expressive-
ness. In SPARK, an additional limitation was the choice not to add any anno-
tation or keyword to the language.
    The main differences come from the fact that SPARK uses other compiler
passes to handle many safety features, whereas they are handled directly by
Rust’s borrow-checker and type-checker. A benefit of our work is that it unam-
biguously defines the rules for SPARK while there exists no official document
specifying Rust’s borrow-checker, in all details, especially as Rust continues to
go through significant evolutions, such as non-lexical lifetimes [7]. We must note,
however, a significant recent effort to provide a rigorous formal description of
the foundations of Rust [8].
    In SPARK, the duration of borrows is limited to the duration of procedure
calls. The mechanism of renaming in SPARK can be used to shorten long paths,
                              Borrowing Safe Pointers from Rust in SPARK         15

and thus it is less important to be able to create several local copies of the same
deep variable. It turns out, however, that this restriction forbids traversing a
linked data structure with only R permission, and that even with RW permission
the structure needs to be reconstructed after traversal. We are working on the
rules for local application of borrow and observe inside a block to allow these.
    Rust has sophisticated lifetime checks, allowing to precisely control the du-
ration of a borrowed pointer. In SPARK, similar checks are implemented as a
separate analysis pass of GNAT compiler, with their own set of rules that are
less expressive: the lifetime of a pointer is limited to the block in which its type
has been declared.
    There are no null pointers in Rust, whereas they are allowed in SPARK.
Dereferencing a null pointer is a runtime error, and the null-pointer safety must
be proved by a separate analysis by the SPARK verification tools [9].
    Another difference is that mutable borrows in Rust guarantee the ownership
of the underlying memory at any time, whereas in SPARK borrow guarantees
ownership only at the entry and exit of the procedure. In particular, it is not
possible in Rust to move out a borrowed variable without assigning it in the
same statement. In SPARK, any borrowed variable can be moved as long as it
is assigned before the end of the procedure, which grants it the RW permission.
This allows us to directly implement the swap procedure in SPARK, whereas
the Rust implementation relies on unsafe operations:
  procedure Swap (X , Y        : in out T ) is
    Temp : T := Y ; --         Move Y . X : RW , Y :W , Temp : RW
  begin
    Y := X ;         --        Move X . X :W , Y : RW , Temp : RW
    X := Temp ;      --        Move Temp . X : RW , Y : RW , Temp : W
  end Swap ;         --        Both arguments X and Y are RW .

    Finally, it is impossible to implement cycling constructs in SPARK (the right-
hand side of an assignment cannot be an ancestor of the left-hand side). Rust
has a similar limitation and requires some workarounds like reference counting to
implement structures like graphs [10]. Nevertheless, both Rust and SPARK allow
compiling with parts of code written in an unsafe superset of the language. This
is the case for some standard library containers (hash tables, iterators, smart
pointers, etc.) that have an interface specified in SPARK and Rust, and can be
called safely from safe Rust/SPARK.


4.2   Other Related Works

Permission-based programming languages generalize the issue of avoiding harm-
ful aliasing to the more general problem of preventing harmful sharing of re-
sources (memory, but also network connections, files, etc.). Cyclone and Rust
achieve absence of harmful aliasing by enforcing an ownership type system on
the memory pointed to by objects [11,12].
    Dafny associates each object with its dynamic frame, the set of pointers
that it owns [13]. This dynamic version of ownership is enforced by modeling
16      Georges-Axel Jaloyan et al.

the ownership of pointers in logic, generating verification conditions to detect
violations of the single-owner model, and proving them using SMT provers. In
Spec#, ownership is similarly enforced by proof, to detect violations of the so-
called Boogie methodology [14].
    Separation logic [15] is an extension of Hoare-Floyd logic that allows reason-
ing about pointers. In general, it is difficult to integrate into automated deductive
verification: in particular, it is not directly supported by SMT provers.
    In our work, we use a permission-based mechanism for detecting potentially
harmful aliasing, in order to make the presence of pointers transparent for au-
tomated provers. In addition, our approach does not require additional user
annotations, that are required in some of the previously mentioned techniques.
We thus expect to achieve high automation and usability, which was our goal
for supporting pointers in SPARK.


5    Conclusion
In this paper, we have presented anti-aliasing rules that allow supporting pointers
in SPARK. We showed a systematic analysis that allows a wide range of use
cases with pointers and dynamic allocation. To the best of our knowledge, this
is a novel approach for controlling aliasing introduced by arbitrary pointers in a
programming language supported by proof. Our approach does not require user
annotations or proof of verification conditions, which makes it much simpler to
adopt. Moreover, we provided a formalization of our rules on a subset of SPARK
in order to mathematically prove the safety of our analysis. Finally, we compared
our method to the Rust language which provides a similar analysis.
    More work needs to be done to fully support pointers in SPARK. Both flow
analysis and proof need to be adapted to account for the presence of pointers.
This work has started and is expected to be completed by the end of 2018.
This will make it possible to use formal verification with SPARK on industrial
programs with pointers, something that was long believed to be impossible.
    We also need to extend our formalism and proof to non-terminating execu-
tions. For that purpose, we can provide a co-inductive definition of the big-step
semantics and perform a similar co-inductive soundness proof, as described by
Leroy and Grall [16].
    The formal study of the constructs that can be implemented using this
borrow-checker has not been discussed in this paper. Such a study could al-
low a formalization of anti-aliasing analyses through classes of expressiveness.
Another long-term goal would be extending our analysis so that it could handle
automatic reclamation, parallelism, initialization and lifetime checks, instead of
relying on external checks.
    The proposed anti-aliasing rules are being discussed by the Ada Rapporteur
Group for inclusion in the next version of Ada [17].
                            Borrowing Safe Pointers from Rust in SPARK      17

References
 1. McCormick, J.W., Chapin, P.C.: Building High-Integrity Applications with
    SPARK. Cambridge University Press (2015)
 2. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.: Frama-C:
    A software analysis perspective. Formal Aspects of Computing 27(3) (May 2015)
    573–609
 3. Jaloyan,     G.A.:           Safe    pointers    in     SPARK      2014    (2017)
    https://arxiv.org/abs/1710.07047.
 4. ACATS: Test suite. http://www.ada-auth.org/acats-files/4.1/ACATS41.ZIP
 5. Georges-Axel       Jaloyan:               SPARK        aliasing     test    suite.
    https://github.com/GAJaloyan/SPARKtestsuite
 6. Rust     community:           Documentation       for    Rust’s    borrow-checker.
    https://github.com/rust-lang/rust/blob/master/src/librustc_borrowck/borrowck/README.md
 7. Rust community: Non-lexical lifetimes. https://github.com/rust-lang/rfcs/pull/2094
 8. Ralf Jung, Jacques-Henri Jourdan, Robbert Krebbers, Derek Dreyer: RustBelt:
    Securing the foundations of the Rust programming language. 2(Issue POPL, 66)
    (2018)
 9. AdaCore, Thales:      Implementation Guidance for the Adoption of SPARK,
    http://www.adacore.com/uploads/technical-papers/ePDF-ImplementationGuidanceSPARK.pdf
10. Rust: Graphs and arena allocation. https://github.com/nrc/r4cppp/blob/master/graphs/README.md
11. Grossman, D., Morrisett, G., Jim, T., Hicks, M., Wang, Y., Cheney, J.: Region-
    based memory management in Cyclone. SIGPLAN Not. 37(5) (May 2002) 282–293
12. Balasubramanian, A., Baranowski, M.S., Burtsev, A., Panda, A., Rakamarić, Z.,
    Ryzhyk, L.: System programming in Rust: Beyond safety. SIGOPS Oper. Syst.
    Rev. 51(1) (September 2017) 94–99
13. Leino, K.R.M. In: Dafny: An Automatic Program Veriﬁer for Functional Correct-
    ness. Springer Berlin Heidelberg, Berlin, Heidelberg (2010) 348–370
14. Barnett, M., Chang, B.Y.E., DeLine, R., Jacobs, B., Leino, K.R.M. In: Boogie: A
    Modular Reusable Veriﬁer for Object-Oriented Programs. Springer Berlin Heidel-
    berg, Berlin, Heidelberg (2006) 364–387
15. Reynolds, J.C.: Separation logic: A logic for shared mutable data structures. In:
    Proceedings of the 17th Annual IEEE Symposium on Logic in Computer Science.
    LICS ’02, Washington, DC, USA, IEEE Computer Society (2002) 55–74
16. Leroy, X., Grall, H.: Coinductive big-step operational semantics. Information and
    Computation 207(2) (Feb 2009) 284–304
17. AdaCore:         Access value ownership and parameter aliasing (2018)
    http://www.ada-auth.org/cgi-bin/cvsweb.cgi/ai12s/ai12-0240-1.txt.
