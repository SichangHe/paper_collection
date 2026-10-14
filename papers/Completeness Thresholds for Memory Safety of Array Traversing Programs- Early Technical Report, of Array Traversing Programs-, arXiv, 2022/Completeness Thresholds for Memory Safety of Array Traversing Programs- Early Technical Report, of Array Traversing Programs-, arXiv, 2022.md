                                         Completeness Thresholds for Memory Safety
                                              of Array Traversing Programs:
                                                  Early Technical Report
arXiv:2211.11885v3 [cs.LO] 3 May 2023




                                                                Tobias Reinhard
                                                   imec-DistriNet Research Group, KU Leuven
                                                          tobias.reinhard@kuleuven.be
                                                                        May 4, 2023


                                                                           Abstract
                                                In this early technical report on an ongoing project, we present – to
                                            the best of our knowledge – the first study of completeness thresholds
                                            for memory safety proofs. Specifically we consider heap-manipulating
                                            programs that iterate over arrays without allocating or freeing mem-
                                            ory. We present the first notion of completeness thresholds for pro-
                                            gram verification which reduce unbounded memory safety proofs to
                                            bounded ones. Moreover, we present some preliminary ideas on how
                                            completeness thresholds can be computed for concrete programs.


                                        Contents
                                        1 Introduction                                                                   2

                                        2 General Notation and Basic Definitions                                         3

                                        3 Syntax                                                                         5

                                        4 Dynamic Semantics                                                              7

                                        5 Assertion Language                                                             9

                                        6 Memory Safety                                                                 12



                                                                               1
7 Verification Conditions                                               12
  7.1 VC Generation . . . . . . . . . . . . . . . . . . . . . . . . . . 13

8 Completeness Thresholds                                                 14
  8.1 Iteratively Extracting Completeness Thresholds . . . . . . . . 18
  8.2 Iterating over Arrays . . . . . . . . . . . . . . . . . . . . . . . 18

9 Roadmap                                                                       19


1     Introduction
In this early technical report on an ongoing project, we present – to the
best of our knowledge – the first study of completeness thresholds for mem-
ory safety proofs. Specifically we consider heap-manipulating programs that
iterate over arrays without allocating or freeing memory. We present the
first notion of completeness thresholds for program verification which reduce
unbounded memory safety proofs to bounded ones. Moreover, we present
some preliminary ideas on how completeness thresholds can be computed for
concrete programs.

Unbounded vs Bounded Proofs Memory safety is a very basic property
we want to hold for every critical program, regardless of its nature or purpose.
Yet, it remains hard to prove and in general requires us to write tedious,
inductive proofs. One way to automate the verification process is to settle
on bounded proofs and accept bounded guarantees.
    Consider a program c that searches through an array of size s. An un-
bounded memory safety proof for c would yield that the program is safe
for any possible input, in particular for any array size, i.e., ∀s. safe(c).
A bounded proof that only considers input sizes smaller than 10 would
only guarantees that the program is safe for any such bounded array, i.e.,
∀s < 10. safe(c).

Completeness Thresholds Approximating unbounded proofs by bounded
ones is a technique often used in model checking. Hence, the relationship be-
tween bounded and unbounded proofs about finite state transition systems
has been studied extensively [3, 5, 9, 4, 1, 8, 2, 10]. For a finite transition sys-
tem T and a property of interest φ, a completeness threshold is any number
k such that we can prove φ by only examining path prefixes of length k in




                                         2
T , i.e., T |=k φ ⇒ T |= φ [5] 1 . Over the years, various works characterised
over-approximations of least completeness thresholds for different types of
properties φ. These over-approximations are typically described in terms of
key attributes of the transition system T , such as the recurrence diameter [9].
    Heap-manipulating programs are essentially infinite state transition sys-
tems. Hence, in general, these key attributes are infinite. This vast structural
difference between the programs we are interested in and the transition sys-
tems for which completeness thresholds have been studied prevents us from
reusing any of the existing definitions or results.
    In § 2 we start by presenting basic definitions and notations that are used
throughout this work. In § 3 and § 4 we present the syntax and semantics
of the programming language we consider. In § 5 and § 6 we formalise
our assertion language as well as the notion of memory safety we consider.
Our study of completeness thresholds relies on verification conditions, which
we define in § 7. We introduce completeness thresholds and study their
properties in § 8. Finally, we describe our envisioned roadmap for this work
in progress in § 9.


2       General Notation and Basic Definitions
The following definitions and notations will be used throughout this work.
Definition 2.1 (Tuples). For any set X we denote the set of tuples over X
as                     [
              X ∗ :=      {(x1 , . . . xn ) | x1 , . . . , xn ∈ X}.
                           n∈N

We denote tuples by overlining the variable name, i.e., x ∈ X ∗ , except if it
is clear from the context.
    For any set X and for any tuple t = (x1 , . . . , xn ) ∈ X ∗ , we denote the
tuple’s length by len(t) = n.
    We define the following notation for appending a single element e ∈ X to
a tuple:
                            t · e := (x1 , . . . , xn , e).
Definition 2.2 (Non-Empty Tuples). For any set X we denote the set of
non-empty tuples over X as
                         X + := {t ∈ X ∗ | len(t) > 0}.
    1
    Note that the term completeness threshold is used inconsistently in literature. Some
papers such as [5] use the definition above, according to which completeness thresholds
are not unique. Others such as [9] define them as the minimal number k such that T |=k
φ ⇒ T |= φ, which makes them unique.

                                           3
Definition 2.3 (Disjoint Union). Let A, B be sets. We define their disjoint
union as
                           A ⊔ B := A ∪ B
if A ∩ B = ∅ and leave it undefined otherwise.

Definition 2.4 (Equivalence Classes). Let R ⊆ X × X be an equivalence
relation. For any x ∈ X, we define the notation

                      hxiR := {x′ ∈ X | R(x, x′ )} ∈ X/R.

We omit R whenever it is clear from the context and write hxi instead of
hxiR .

Notation 2.5 (Homomorphic & Isomorphic). Let A, B be algebraic struc-
tures. We define the following notations:

   • A ∼ B expresses that A and B are homomorphic.

   • A ≃ B expresses that A and B are isomorphic.

Remark 2.6 (Canonical Homomorphism from Tuples to Sets). Let X be a
set. Then, X ∗ with concatenation and P(X) with union are both monoids and
the canonical homomorphism from X ∗ to P(X) is (x1 , . . . , xn ) 7→ {x1 , . . . , xn }.

Definition 2.7 (Congruence Relation between Tuples and Sets). Let X be
a set and let hX : X ∗ → P(X) be the canonical homomorphism. We define
the congruence relation ∼ =X ⊆ (X ∗ × P(X)) ∪ (P(X) × X ∗ ) such that the
following holds for all t ∈ X ∗ and all S ∈ P(X):

                    S∼
                     =X t      ⇔     t∼
                                      =X S       ⇔     hX (t) = S

Whenever the base set X is clear from the context, we write ∼
                                                            = instead of ∼
                                                                         =X .




                                          4
3    Syntax
In this section we define the syntax of the programming language that we
use in the rest of this work.
Definition 3.1 (Variables). We define X to be an infinite set of variable
symbols.
   Our language allows for simple pointer arithmetic of the form l +LZ z
where l is a heap location and z is an offset.
Definition 3.2 (Structured Heap Locations). We define the sets of heap
objects HObjs and heap indices HIdxs to be infinite sets with N ⊂ HIdxs.
Further, we define the set of heap locations as
                        L    :=   HObjs × HIdxs.
We denote heap locations by l, heap objects by o and heap indices by idx.
Definition 3.3 (Unit Type). We define the unit type as Unit := {()}.
Definition 3.4 (Types). We define the set of types T ypes syntactically as
follows:
            T ∈ T ypes := L | HObjs | Z | B | Unit
   Operations are pure functions that map inputs to output and cannot
access the heap.
Definition 3.5 (Operations). We define Ops to be a set of operations with
Ops ⊆ {f : D → C | D ∈ T ypes∗ , C ∈ T ypes} and with <, + ∈ Ops.
   For each f : D → C ∈ Ops, we use the following notation dom(f ) = D
and codom(f ) = C.
    While this work currently only deals with arrays, our plan is to investi-
gate completeness thresholds for programs that deal with arbitrary tree-like
inductive data structures. In order to keep the semantics of our language
modular and to allow for easy extensions, we introduce an unspecified set
of heap commands that captures the APIs of the data structures we are
interested in.
Definition 3.6 (Heap Commands). We define HCmds to be a set of sym-
bols. Every hc ∈ HCmds represents a command that accesses the heap.
Definition 3.7 (Program syntax). We define the set of commands Cmds,
expressions Exps and values V syntactically by the grammar presented in
Fig. 1.


                                     5
l∈L                                                   Heap locations
o ∈ HObjs                                             Heap Objects
z∈Z
b∈B
x∈X                                                   Variables
op ∈ Ops                                              Primitive Operations
hc ∈ HCmds                                            Heap Commands

v∈V            ::= l | o | z | b | ()                 Values
e ∈ Exps       ::= v | x | op(e)                      Expressions

c ∈ Cmds       ::= e | let x := c in c |
                   if e then c else c |
                   while !e do c |
                   for x in [e to e] do c |
                   !e | !e := e | hc(e)               Heap access

                  (a) Values, expressions and commands.
           ′
        c; c      :=   let x := c in c′    where x is not free in c′
    if e then c   :=   if e then c else ()

                           (b) Syntactic sugar.

                       Figure 1: Program syntax.




                                    6
4     Dynamic Semantics
In order to keep things simple, our language uses a heap but no store. Hence,
variables are actually constants that can be bound to values via let com-
mands. As a consequence, the entire evaluation state of a program is rep-
resented by the heap and the program itself. Further, expressions are pure,
hence their evaluation does not depend on the heap.

Definition 4.1 (Evaluation of Closed Expressions). We define a partial eval-
uation function [[·]] : Exps ⇀ V on expressions by recursion on the structure
of expressions as follows:

 [[v]]                    := v                            if v ∈ V,
 [[op(e1 , . . . , en )]] := op([[e1 ]], . . . , [[en ]]) if ⊥ 6∈ {[[e1 ]], . . . , [[en ]]}
                                                          and ([[e1 ]], . . . , [[en ]]) ∈ dom(op),
 [[e]]                    := ⊥                            otherwise.

We identify closed expressions e with their ascribed value [[e]].

Definition 4.2 (Evaluation Context). We define the set of evaluation con-
texts EvalCtxts syntactically as follows:

                        E ∈ EvalCtxts           ::= let x :=  in c

For any c ∈ Cmds and E ∈ EvalCtxts, we define E[c] := E[ 7→ c].

Definition 4.3 (Free Variables (Commands)). We define free variables in
the usual way. For any command c we denote the set of variables that occur
freely in c by freeVars(c).

Definition 4.4 (Substitution (Commands)). We define substitution in the
usual way. For any command c, variable x and expression e, we denote the
result of substituting every free occurrence of x in c with e by c[x 7→ e].
Further, we extend substitutions to tuples of variables and expressions in the
canonical way.

    We explicitly model memory errors in our operational semantics. This
way we know that (i) any execution which ends in a value does not involve
memory errors and (ii) any execution that does involve memory errors ends
in the dedicated error state error.

Definition 4.5 (Memory Errors). We denote the memory error state by error
and the set of potentially erroneous commands by Cmds+ := Cmds∪{error}.
We denote potentially erroneous commands by c+ .

                                                 7
  Heaps are finite collections of resources that can be manipulated by com-
mands.

Definition 4.6 (Physical Resources). We define the set of physical resources
Rphys syntactically as follows:

                           r p ∈ Rphys   ::=    l 7→ v

                                l∈L            v∈V

Definition 4.7 (Physical Heaps). We define the set of physical heaps as

                            Heaps phys := Pfin (Rphys )

and the function locspRes : Heaps phys → Pfin (L) mapping physical heaps to the
sets of allocated heap locations as

               locspRes (h) := {l ∈ L | ∃v ∈ V. l 7→ v ∈ h}.

We denote physical heaps by h.

Definition 4.8 (Basic Commands). We define the set of basic commands
BCmds syntactically as follows:

                bc ∈ BCmds ::= e | let x := bc in bc |
                               if e then bc else bc |
                               while !e do bc |
                               for x in [e to e] do bc |
                               !e | !e := e

   The set of basic commands is the subset of Cmds that consists exactly of
those commands that do not involve any heap command call hc(e). Remem-
ber that the set of heap commands captures the APIs of data structures.
We do not want to change our operational semantics each time we want to
consider a new data structure. Hence, we assume that there exists an inter-
pretation for each heap command that describes its behaviour in terms of
basic commands.

Assumption 4.9 (Heap Command Interpretation). We assume that there
exists a function Ihcmds : HCmds → (BCmds × X ∗ ) that maps each heap
command to a basic command and a vector of variables. Further, for every
mapping of the form Ihcmds (hc) = (bc, (x1 , . . . , xn )) the following two proper-
ties hold:


                                         8
        ^
    •          xi 6= xj
        i6=j

    • freeVars(bc) ⊆ {x1 , . . . , xn }.
Definition 4.10 (Command Reduction Relation). We define a command re-
duction relation cmd according to the rules presented in Fig. 2. A reduction
step has the form
                             h, c cmd h′ , c′ .
                          ∗
    We define             cmd as the reflexive transitive closure of       cmd .




5       Assertion Language
In the previous sections we introduced heap commands that capture the
APIs of data structures. In a similar way, we introduce heap predicates that
describe their memory layout.
Assumption 5.1 (Heap Predicates). We assume that there is a set of sym-
bols P . Every p ∈ P represents a predicate characterising the heap. Further,
we assume that there is a function Ihpreds : P → P(Heaps phys × V ∗ ) that maps
each heap predicate symbol to a predicate over heaps and value tuples.
Definition 5.2 (Assertions). We define the set of assertions A according to
the syntax presented in Figure 3.
    We omit the index set I in quantifications when its choice becomes clear
from the context and write ∃i. a(i) and ∀i. a(i) instead of ∃i ∈ I. a(i) and
∀i ∈ I. a(i),

Definition 5.3. Assertion Model Relation We define the assertion model
relation A ⊆ Heaps phys × A by recursion over the structure of assertions
according to the rules presented in Fig. 4.

Definition 5.4 (Free Variables (Assertions)). We define the notion of free
variables for assertions analogously to that of commands (cf. 4.3).
Definition 5.5 (Substitution (Assertions)). We define substitution for as-
sertions analogously to substitution for commands (cf. 4.4).
Notation 5.6. Free Variables of Tuples For convenience we define the fol-
lowing notation for any tuple of commands and assertions (y1 , . . . , yn ) ∈
(Cmds ∪ A)∗ :
                freeVars(y1 , . . . , yn ) := freeVars(y1 ) ∪ · · · ∪ freeVars(yn ).

                                                 9
          CmdRed-EvalCtxt                           CmdRed-EvalCtxt-Fail
                            ′ ′
              h, c     cmd h , c                     h, c cmd h′ , error
                            ′     ′
           h, E[c]     cmd h , E[c ]                h, E[c] cmd h′ , error

                       CmdRed-IfTrue
                       h, if True then ct else cf             cmd h, ct


                       CmdRed-IfFalse
                       h, if False then ct else cf            cmd h, cf


     CmdRed-While
                                     x 6∈ freeVars(c)
     h, while !l do c        cmd h, let x :=!l in if x then (c; while !l do c)


CmdRed-For
h, for x in [n to n′ ] do c                      ′                             ′
                                  cmd h, if n ≤ n then (c; for x in [n + 1 to n ] do c)


                                                            CmdRed-ReadHeapLoc
     CmdRed-Let                                              l 7→ v ∈ h
     h, let x := v in c       cmd h, c[x 7→ v]
                                                            h, !l cmd h, v

                           CmdRed-ReadHeapLoc-Fail
                              l 6∈ locspRes (h)
                            h, !l cmd h, error

                  CmdRed-AssignHeapLoc
                  h ⊔ {l 7→ }, !l := v             cmd h ⊔ {l    7→ v}, ()

                          CmdRed-AssignHeapLoc-Fail
                                 l 6∈ locspRes (h)
                           h, !l := v cmd h, error

           CmdRed-Desugar-HeapCmdCall
                              Ihcmds (hc) = (bc, (x1 , . . . , xn ))
           h, hc(v1 , . . . , vn ) cmd h, bc[(x1 , . . . , xn ) 7→ (v1 , . . . , vn )]


                       Figure 2: Command reduction rules.




                                              10
                                          e ∈ Exps
                                            p∈P
                                           A⊆A
                                       Index set I ⊆ Z

 a∈A      ::=    True | False | e W
                                  | ¬a | a ∧ a | a ∨ a | a ∗ a | a −∗ a |
                 e 7→ e | p(e) |    A | a

                                 (a) Assertion syntax.
                  a1 → a2             :=      ¬a1 ∨ a2
                  a1 ↔ a2             :=      W 1 → a2 ) ∧ (a2 → a1 )
                                              (a
                  ∃i ∈ I. a(i)        :=        {a(i) | i ∈ I}
                  ∀i ∈ I. a(i)        :=      ¬∃i ∈ I. ¬a(i)

                                 (b) Syntactic sugar.

                                Figure 3: Assertions.




           h A True
           h 6A False
           h A e                    iff   ∅ A [[e]]
           h A ¬a                   iff   h 6A a
           h A a1 ∧ a2              iff   h A a1 ∧ h A a2
           h A a1 ∨ a2              iff   h A a1 ∨ h A a2
           h A a1 ∗ a2              iff   ∃h1 , h2 . h = h1 ⊔ h2
                                                      ∧ h1 A a1 ∧ h2 A a2
           h A a1 −∗ a2             iff   ∀h1 . h1 ∩ h = ∅ ∧ h1 A a1
                                                  → h1 ⊔ h A a2
           h A l 7→ v               iff   l 7→ v ∈ h
           h A p(e
                W 1 , . . . , en )   iff   Ihpreds (p)(h, [[e1 ]], . . . , [[en ]])
           h A A                    iff   ∃a ∈ A. h A a
           h A  a                  iff   ∅ A a


Figure 4: Assertion model relation. We write h 6A a if h A a does not hold.



                                             11
Definition 5.7 (Validity). Let a ∈ A be an assertion with freeVars(a) ∼         =
x = (xi )i . For each i = 1, . . . , n, let Ti be the type of variables xi and let
T = (Ti )i . We call assertion a valid if the following holds:

                          ∀h. ∀v ∈ T . h A a[x 7→ v]

We denote validity of a by writing A a.


6     Memory Safety
Definition 6.1 (Memory Safety of Commands and Heaps). We define the
safety relation for commands safe ⊆ Heaps phys × Cmds as follows:
    Let x = (xi )i ∼= freeVars(c) be the variables occurring freely in c. For
each i, let Ti be the type of variable xi and let T = (Ti )i . Then,

           safe(h, c) ⇔ ∀v ∈ T . ¬∃h′ . h, c[x 7→ v],     ∗    ′
                                                          cmd h , error

We say that a command c is safe under a physical heap h if safe(h, c) holds.

    We consider a command safe under a heap if its execution does not lead
to a memory error. Note that a command’s execution can get stuck without
any memory error occurring. Such cases arise for not-well-typed commands
such as if 13 then . . .. For this work, we only consider well-typed programs.
Hence, we do not care about cases in which a program gets stuck as long as
no memory error occurs.

Definition 6.2 (Memory Safety of Commands and Assertions). We define
the safety relation for commands safeA ⊆ A × Cmds as follows:
    Let x = (xi )i ∼
                   = freeVars(a, c) be the variables occurring freely in a and c.
For each i, let Ti be the type of variable xi and let T = (Ti )i . Then,
                                                                             
   safeA (a, c) ⇐⇒ ∀v ∈ T . ∀h. h A a[x 7→ v] ⇒ safe(h, c[x 7→ v])

We say that a command c is safe under a assertion a if safeA (a, c) holds.

Notation 6.3. We denote preconditions by M. Further, we aggregate pre-
conditions M and programs c into tuples {M} c.


7     Verification Conditions
A common approach in program verification is to derive a verification con-
dition vc from the program c and correctness property φ in question [7, 11].

                                       12
Instead of verifying the program directly, we prove the verification condi-
tion. In general, vc describes an over-approximation of all possible program
behaviours. The process is sound iff truth of the verification condition in-
deed implies that our program is correct, i.e., |= vc ⇒ c |= φ. We proceed
analogously during our study of completeness thresholds.

Definition 7.1 (Verification Condition). We call an assertion vc ∈ A a
verification condition for {M} c if the following holds:

                          A vc    ⇒        safeA (M, c)

We denote verification conditions by vc.

Definition 7.2 (Precise Verification Conditions). Let vc be a verification
condition for {M} c and let x ∈ freeVars(M, c) be a free variable of type T .
We call vc precise in x for {M} c if the following holds for every value v ∈ T :

               safeA (M[x 7→ v], c[x 7→ v])     ⇒ A vc[x 7→ v]

Assumption 7.3 (Array Predicate). We assume that there exists a predi-
cate symbol array ∈ P . We further assume that Ihpreds (array) ⊆ Heaps phys ×
HObjs × N is the minimal relation for which the following holds:

              Ihpreds (array)(h, a, s) ⇐⇒ h A
                                                    ∗
                                                    0≤i<s
                                                           (a, i) 7→


We identify the assertion array(a, s) with the assertion
                                                               ∗
                                                              0≤i<s
                                                                      (a, i) 7→ .


7.1    VC Generation
We use weakest liberal preconditions [7, 6] as verification conditions.

Definition 7.4. Assertion Lambdas We define the set of assertion lambda
terms as Aλ := {λx. a | x ∈ X , a ∈ A}. For convenience we define the
notation λ . a := λxf resh . a for xf resh 6∈ freeVars(a).

    We use assertion lambda terms λr.Q to denote postconditions referring
to a result value r.

Definition 7.5. Weakest Liberal Precondition We define the weakest liberal
precondition function wlp : Cmds × Aλ → A by recursion over the structure



                                       13
of commands as follows:

 wlp(e, λr. Q)                        := Q[r 7→ e],
 wlp(let x := c1 in c2 , λr. Q)       := wlp(c1 , λx. wlp(c2 , λr. Q)),
 wlp(if e then ct else cf , λr. Q)    := (e → wlp(ct , λr. Q))
                                         ∧ (¬e → wlp(cf , λr. Q)),
 wlp(while !e inv I do c, λr. Q)      := I
                                         ∗ (I −∗ e 7→ )
                                         ∗ (I ∧ e 7→ True −∗ wlp(c, λ . I))
                                         ∗ (I ∧ e 7→ False −∗ Q),
 wlp(for x in [e1 to e2 ] inv I do c, := I
     λr. Q)                              ∗ (∀x. e1 ≤ x < e2 ∧ I −∗ wlp(c, λ . I))
                                         ∗ (I −∗ Q),
 wlp(!e, λr. Q)                       := ∃y. e 7→ y ∧ Q[r 7→ y]
                                         where y 6∈ freeVars(e, Q),
 wlp(!e1 := e2 , λr. Q)               := e1 7→     ∗ (e1 7→ e2 −∗ Q),
 wlp(hc(e), λr. Q)                    := wlp(bc[x 7→ e], λr. Q)
                                         where Ihcmds (hc) = (bc, x)

   Note that our weakest precondition for for loops does not allow the
postcondition to depend on the knowledge that any work was done. This
simplified precondition is sufficient to reason about the memory safety of
array-traversing programs that do not allocate nor free memory.


8    Completeness Thresholds
Now that we have an intuition for what a completeness threshold should be
and for how we want to use it, let’s formalise this intuition.

Definition 8.1 (Completeness Thresholds for Quantified Assertions). Let
Q ∈ {∀, ∃} be a quantifier and let Qx ∈ T. a be a quantified assertion. Fur-
ther, let R ⊆ T be a restriction of the domain of x. We call R a completeness
threshold for a if the following holds:

                     A Qx ∈ R. a      ⇒ A Qx ∈ T. a.

Definition 8.2 (Completeness Thresholds for Programs). Let T be the type
of x in {M} c and let R ⊆ T be a restriction of this type. We call R a
completeness threshold for x in {M} c if the following holds:

∀v ∈ R. safeA (M[x 7→ v], c[x 7→ v])   ⇒    ∀v ∈ T. safeA (M[x 7→ v], c[x 7→ v])


                                       14
Lemma 8.3 (Precision). Let ∀x ∈ T. vc be a verification condition for {M} c
and let R ⊆ T be a completeness threshold for vc. Further, let vc be precise
in x for {M} c. Then R is a completeness threshold for {M} c.
Proof. Assume that ∀v ∈ R. safeA (M[x 7→ v], c[x 7→ v]) holds. We have to
prove that the program is safe for the unrestricted domain, i.e., safeA (M, c).
    Together with the precision of vc in x, this assumption implies ∀v ∈
R. A vc[x 7→ v] (cf. Def. 7.2), which is equivalent to A ∀x ∈ R. vc.
    R is a completeness threshold for vc. According to Def. 8.1, this means A
∀x ∈ T. vc. Since the latter is a verification condition for {M} c, proposition
safeA (M, c) holds by Def. 7.1. Hence, R is a completeness threshold for
{M} c.
    Finding completeness threshold for a non-precise verification condition
∀x. vc does not allow us to conclude that we found a completeness threshold
for the actual program {M} c. However, as long as our ultimate goal is to
verify the program by proving an assertion A that is at least as strong as
our verification condition, i.e., A ⇒ ∀x. vc, we can leverage the complete-
ness threshold. Hence, it makes sense to first concentrate on completeness
thresholds for verification conditions. Later, we can try to relate our results
to completeness thresholds for programs.
Lemma 8.4. Let ∀x ∈ T. a be an assertion. Let R ⊆ T be such that

              ∀v1 , v2 ∈ R.   (A a[x 7→ v1 ] ⇔ A a[x 7→ v2 ]).

Then, for every r ∈ R it holds that

               A ∀x ∈ (T \ R) ∪ {r}. a     ⇔    A ∀x ∈ T. a.

Proof. Let r ∈ R. With the assumption from the lemma, we get

                 ∀v ∈ R. (A a[x 7→ r] ⇔ A a[x 7→ v])

and hence
                       A a[x 7→ r] ⇔ A ∀x ∈ R. a
Further, ∀x ∈ T. a is valid iff both ∀x ∈ (T \ R). a and ∀x ∈ R. a are valid.
As we can reduce validity of the latter to validity of a[x 7→ r], we get

                  (A ∀x ∈ (T \ R). a) ∧ (A a[x 7→ r])
               ⇐⇒ (A ∀x ∈ (T \ R). a) ∧ (A ∀x ∈ R. a)
               ⇐⇒ A ∀x ∈ T. a.



                                      15
Corollary 8.5. Let ∀x ∈ T. a be an assertion. Let R ⊆ T be such that

               ∀v1 , v2 ∈ R.    (A a[x 7→ v1 ] ⇔ A a[x 7→ v2 ]).

Then, for every r ∈ R, the set (T \ R) ∪ {r} is a completeness threshold for
assertion a.

Proof. Follows from Lem. 8.4 and Def. 8.1.
    Consider a verification condition ∀x ∈ T. vc and suppose we are interested
in a completeness threshold for x. By definition, the threshold is a restriction
of x’s domain, i.e., R ⊆ T . The lemmas and corollary above show us that
one way forward is to identify a validity-preserving subset of T . That is, we
need to look for a subset R ⊆ T of the domain within which the concrete
choice for x does not affect the validity of the verification condition. Once
we got this, we can collapse R to any representative r ∈ R and we found our
completeness threshold (T \ R) ∪ {r}.
    Notice that validity preservation of domain restrictions is a transitive
property. Hence, we can easily turn the search for completeness thresholds
for a fixed variable into an iterative approach.

Lemma 8.6 (Transitivity of Completeness Thresholds for Fixed Variable).
Let R0 , R1 , R2 be sets with R2 ⊆ R1 ⊆ R0 . Let ai = ∀x ∈ Ri . a be assertions.
Let R1 and R2 be completeness thresholds for x in a0 and a1 , respectively.
Then, R2 is also a completeness threshold for x in a0 .

Proof. Since R1 is a completeness threshold for x in a0 = ∀x ∈ R0 . a, we get

                     A ∀x ∈ R1 . a     ⇒ A ∀x ∈ R0 . a.

Since R2 is a completeness threshold for x in a1 = ∀x ∈ R1 . a, we get

                     A ∀x ∈ R2 . a     ⇒ A ∀x ∈ R1 . a.

That is,

           A ∀x ∈ R2 . a      ⇒ A ∀x ∈ R1 . a    ⇒ A ∀x ∈ R0 . a

and hence R2 ⊂ R0 is a completeness threshold for x in a0 = ∀x ∈ R0 . a

Corollary 8.7. Let T be a type and let (Ri )i be a family of sets with R0 = T
and Ri+1 ⊆ Ri . Let (ai )i = (∀x ∈ Ri . a)i be a family of assertions such
that each Ri+1 is a completeness threshold for x in ai . Then, each Ri is a
completeness threshold for x in a0 = ∀x ∈ T. a.

                                        16
Proof. Follows from Lem. 8.6 by induction.
    Consider a program that traverses an array a of size sa and an array b of
size sb . When we analyse the verification condition of this program we find
that it contains distinct parts that describe memory safety of the accesses to
array a and distinct parts for the accesses to b. Since both arrays describe
separate parts of the heap, we can bring the verification condition into a form
that reflects this. Thereby, we get a formula of the form vc ≡ vca ∗ vcb where
vca and vcb describe memory safety in respect to a and b, respectively.
    Suppose, we want to find a completeness threshold for sa . In some cases,
the manipulation of both arrays is entangled which means that sa potentially
affects the validity of vcb . In such a case, we have no choice but to analyse
the entire formula to find our completeness threshold. However, often that’s
not the case and sa only shows up in the subformula vca that actually con-
cerns array a. In this case, it is sufficient to analyse vca in order to find a
completeness threshold for sa .
Lemma 8.8 (Elimination). Let a, ax , a′ be assertions with ∀x ∈ T. a ≡ ∀x ∈
T. ax ∗ a′ . Suppose the choice of x does not affect the validity of a′ , i.e.,
                    ∀v ∈ T.     (A a′    ⇔ A a′ [x 7→ v]).
Let R ⊆ T be a completeness threshold for x in ∀x ∈ T. ax . Then, R is also
a completeness threshold for x in ∀x ∈ T. a.
Proof. Since R is a completeness threshold for x in ∀x ∈ R. ax , we get
                              A ∀x ∈ R. ax ∗ a′
                     ⇒        A (∀x ∈ R. ax ) ∗ (∀x ∈ R. a′ )
                     ⇒        A (∀x ∈ T. ax ) ∗ (∀x ∈ R. a′ ).
By using the assumption that the choice of x does not affect the validity of
a′ we can conclude
                              A (∀x ∈ T. ax ) ∗ (∀x ∈ R. a′ )
                     ⇒        A (∀x ∈ T. ax ) ∗ (∀x ∈ T. a′ )
                     ⇒        A ∀x ∈ T. ax ∗ a′ .


Corollary 8.9 (VC Slicing). Let a, ax , a′ be assertions with ∀x ∈ T. a ≡
∀x ∈ T. ax ∗ a′ . Suppose x is not free in a′ . Let R ⊆ T be a completeness
threshold for x in ∀x ∈ T. ax . Then, R is also a completeness threshold for
x in ∀x ∈ T. a.
Proof. Follows from Lem. 8.8.

                                         17
8.1    Iteratively Extracting Completeness Thresholds
What we saw so far, gives us the tools to define an iterative process to extract
completeness thresholds.
Workflow 8.10. Let {M} c be a program with variables x1 , . . . , xn for which
we would like to extract completeness thresholds.
  1. Compute a verification condition for {M} c, e.g., by using weakest
     preconditions. The result has the form ∀x ∈ T . vc.
  2. Iteratively extract completeness thresholds for each xi .
     For all i ∈ {1, . . . , n}:
      (a) Let R ⊆ T be the completeness thresholds extracted so far. (Ini-
          tially R = T .)
      (b) Bring the verification condition into the form
          ∀x ∈ R. vc ≡ ∀x ∈ R.
                                      ′
                                           ∗     vcj .
                                               0≤j≤m
      (c) Identify a subformula vc whose validity is not affected by the
          choice of xi . Bring the verification condition into the form
          ∀x ∈ R. vc ≡ ∀x ∈ R. vci ∗ vc′ .
          In the remaining steps it suffices to analyse ∀x ∈ R. vci .
      (d) Examine vci and extract a completeness threshold. This can either
          be done purely manually or by identifying patterns for which we
          previously proved that we can extract completeness thresholds.
          This step yields a completeness threshold Ri′ which, in the worst
          case, does not yield an improvement, i.e., Ri′ = Ri .
      (e) Repeat this process iteratively until the extracted completeness thresh-
          old does not improve in respect to the last iteration.

8.2    Iterating over Arrays
In the following, we study patterns encountered in verification conditions of
programs that iterate over arrays. The goal of this section is to formulate
reusable lemmas that allow us to automate the extraction of completeness
thresholds.
Lemma 8.11 (VC-CT for Bounded, Unconditional Array Access). Let z, a, b ∈
Z be constants and vc(s) = ∀i ∈ Z. a ≤ i < s + b → 0 ≤ i + z < s. Then,
for every r ∈ Z with r > a − b it holds that
                      A ∀s ∈ Z. vc(s)         ⇔ A vc(r)
That is, {r} is a completeness threshold for vc(s).

                                          18
Proof. For s ≤ a − b it holds a ≤ i < s + b ≡ False and hence vc(s) ≡ True.
   For s > a − b we get:

    vc(s) ≡   ∀i. a ≤ i < s + b → 0 ≤ i + z < s
          ≡   ∀i. (a ≤ i < s + b → 0 ≤ i + z) ∧ (a ≤ i < s + b → i + z < s)
          ≡   ∀i. (a ≤ i → 0 ≤ i + z) ∧ (i < s + b → i + z < s)
          ≡   ∀i. (a ≤ i → 0 ≤ i + z) ∧ ∀i. (i < s + b → i + z < s)
          ≡   ∀i. (a ≤ i → 0 ≤ i + z) ∧ ∀i. (i < b → i + z < 0)
         =:   vc+

s does not occur in vc+ and, hence, the concrete value of s does not impact
the validity of vc+ . By Lem. 8.5, for any choice of r ∈ Z with r > l − r, the
set {r} is a completeness threshold for vc(s).


9     Roadmap
This report describes a work in progress. We are currently studying pat-
terns encountered in programs that traverse arrays. Once sufficiently many
patterns have been identified, we are going to prove that we can extract com-
pleteness thresholds for a relevant class of array-traversing programs. After-
wards, we are going to generalize our findings to arbitrary tree-like inductive
data structures.


References
 [1] Mohammad Abdulaziz, Michael Norrish, and Charles Gretton. Formally
     verified algorithms for upper-bounding state space diameters. Journal
     of Automated Reasoning, 61:485–520, 2018.

 [2] Mohammad Awedh and F. Somenzi. Proving more properties with
     bounded model checking. In CAV, 2004.

 [3] Armin Biere, Alessandro Cimatti, Edmund M. Clarke, and Yunshan
     Zhu. Symbolic model checking without bdds. In International Confer-
     ence on Tools and Algorithms for Construction and Analysis of Systems,
     1999.

 [4] Daniel Bundala, Joël Ouaknine, and James Worrell. On the magnitude
     of completeness thresholds in bounded model checking. 2012 27th An-
     nual IEEE Symposium on Logic in Computer Science, pages 155–164,
     2012.

                                      19
 [5] Edmund M. Clarke, Daniel Kroening, Joël Ouaknine, and Ofer Strich-
     man. Completeness and complexity of bounded model checking. In
     International Conference on Verification, Model Checking and Abstract
     Interpretation, 2004.

 [6] Edsger W. Dijkstra. A discipline of programming. Pentice Hall, 1976.

 [7] Cormac Flanagan and James B. Saxe. Avoiding exponential explosion:
     generating compact verification conditions. In ACM-SIGACT Sympo-
     sium on Principles of Programming Languages, 2001.

 [8] Keijo Heljanko, Tommi A. Junttila, and Timo Latvala. Incremental
     and complete bounded model checking for full pltl. In International
     Conference on Computer Aided Verification, 2005.

 [9] Daniel Kroening and Ofer Strichman. Efficient computation of recur-
     rence diameters. In International Conference on Verification, Model
     Checking and Abstract Interpretation, 2003.

[10] Kenneth L. McMillan. Interpolation and sat-based model checking. In
     International Conference on Computer Aided Verification, 2003.

[11] Gaurav Parthasarathy, Peter Müller, and Alexander J. Summers. For-
     mally validating a practical verification condition generator. In Inter-
     national Conference on Computer Aided Verification, 2021.




                                     20
