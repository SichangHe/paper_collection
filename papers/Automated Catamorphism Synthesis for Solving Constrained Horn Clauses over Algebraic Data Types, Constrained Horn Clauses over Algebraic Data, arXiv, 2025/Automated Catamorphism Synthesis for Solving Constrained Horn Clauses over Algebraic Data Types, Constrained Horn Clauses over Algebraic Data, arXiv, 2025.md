                                          Automated Catamorphism Synthesis for Solving
                                          Constrained Horn Clauses over Algebraic Data
                                                            Types

                                         Hiroyuki Katsura1 , Naoki Kobayashi1 , Ken Sakayori1 , and Ryosuke Sato2

                                                              The University of Tokyo, Tokyo, Japan
                                                              1

                                                        {h.katsura,koba,sakayori}@is.s.u-tokyo.ac.jp
arXiv:2507.20726v1 [cs.LO] 28 Jul 2025




                                                  2
                                                    Tokyo University of Agriculture and Technology, Tokyo, Japan
                                                                          rsato@acm.org



                                               Abstract. We propose a novel approach to satisfiability checking of
                                               Constrained Horn Clauses (CHCs) over Algebraic Data Types (ADTs).
                                               CHC-based automated verification has gained considerable attention in
                                               recent years, leading to the development of various CHC solvers. How-
                                               ever, existing solvers for CHCs over ADTs are not fully satisfactory, due
                                               to their limited ability to find and express models involving inductively
                                               defined functions/predicates (e.g., those about the sum of list elements).
                                               To address this limitation, we consider catamorphisms (generalized fold
                                               functions), and present a framework for automatically discovering ap-
                                               propriate catamorphisms on demand and using them to express a model
                                               of given CHCs. We have implemented a new CHC solver called Catalia
                                               based on the proposed method. Our experimental results for the CHC-
                                               COMP 2024 benchmark show that Catalia outperforms state-of-the-art
                                               solvers in solving satisfiable CHCs over ADTs. Catalia was also used as
                                               a core part of the tool called ChocoCatalia, which won the ADT-LIA
                                               category of CHC-COMP 2025.

                                               Keywords: Constrained Horn Clauses · Algebraic Data Types · Cata-
                                               morphisms · Automated Verification.


                                         1   Introduction

                                         Fully automated verification of programs through satisfiability checking of con-
                                         strained Horn clauses (CHCs) has attracted considerable attention in recent
                                         years, as it offers a uniform and language-agnostic framework for verifying diverse
                                         program properties [13,17,25,1]. For example, consider the following functional
                                         program.

                                         let rec plus m n = if n=0 then m else (plus m (n-1))+1
                                         let main m n = if n>=0 then assert(plus m n >= m)

                                         The lack of assertion failures in the above program can be reduced to the satisfi-
                                         ability of the following CHCs, i.e, the problem of whether there exists a predicate
2        Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

Plus that satisfies them:

                   ∀m. Plus(m, 0, m).
                   ∀m, n, r. Plus(m, n, r + 1) ⇐ Plus(m, n − 1, r).
                   ∀m, n, r. ff ⇐ Plus(m, n, r) ∧ n ≥ 0 ∧ r < m.

Here, ff represents false. The predicate Plus may be considered an invariant
among arguments m, n and the corresponding return value r; indeed, Plus(m, n, r) ≡
m + n = r satisfies the above CHCs. State-of-the-art CHC solvers [22,15,14,5,4]
can quickly solve problems like the above, finding an appropriate invariant
(Plus(m, n, r) ≡ m + n = r or Plus(m, n, r) ≡ r ≥ m in this case), enabling
fully automated program verification.
    Despite various efforts, however, the current CHC solvers are not very good
at dealing with data structures. For example, consider the following variant of
the example above, where natural numbers are represented as data structures.

              ∀m. PlusNat(m, Z, m).
              ∀m, n, r. PlusNat(m, S(n), S(r)) ⇐ PlusNat(m, n, r).
              ∀n. Lt(Z, S(n)).       ∀m, n. Lt(S(m), S(n)) ⇐ Lt(m, n).
              ∀m, n, r. ff ⇐ PlusNat(m, n, r) ∧ Lt(r, m).

Z3 Spacer [22], a state-of-the-art CHC solver, fails to prove the satisfiability of
the CHCs above. A problem is that while a model for Plus can be expressed by
a simple linear arithmetic formula (m + n = r), an inductively defined predicate
is required to express a model for PlusNat, and it is, in general, hard to auto-
matically find such an inductively defined predicate and check that it is indeed
a model (i.e., satisfies all the clauses).
    To address the issue above, we propose a method for abstracting CHCs by
using a catamorphism [26] from data structures to (tuples of) integers, on which
existing CHC solvers perform well in practice. For the example above, we can
abstract Z and S respectively to 0 and λx.x + 13 , and obtain the following
“abstract” CHCs over integers, whose satisfiability implies that of the original
CHCs.

             ∀m. PlusNat(m, 0, m).
             ∀m, n, r. PlusNat(m, n + 1, r + 1) ⇐ PlusNat(m, n, r).
             ∀n. Lt(0, n + 1).      ∀m, n. Lt(m + 1, n + 1) ⇐ Lt(m, n).
             ∀m, n, r. ff ⇐ PlusNat(m, n, r) ∧ Lt(r, m).

Universal quantifiers are now over integers, and for the sake of simplicity, we
have omitted some conditions on the variables; see later sections. State-of-the-art
3
    Actually, we do not lose any information using this abstraction, as the induced cata-
    morphism is injective. In general, however a catamorphism may not be injective,
    hence introducing abstraction.
                   Catamorphism Synthesis for Program Invariants over ADT           3

solvers can instantly deduce its satisfiability, which also implies the satisfiability
of the original CHCs.
    The remaining question is how to automatically find appropriate catamor-
phisms. In the above example, the required catamorphism is just the “size”
function incorporated by default in some CHC solvers like Eldarica [15], but
as we will see later, the size function is not always sufficient. To this end,
we propose a method for automatically finding appropriate catamorphisms in
a counterexample-guided manner. We have implemented the proposed method
and developed a new CHC solver called Catalia. According to our experiments
using the benchmark set of the ADT category of CHC-COMP 2024, Catalia
significantly outperformed state-of-the-art CHC solvers for SAT instances.
    Our contributions are summarized as follows.
 – Formalization of abstraction of CHCs using catamorphisms.
 – Counterexample-guided automatic synthesis of appropriate catamorphisms.
 – Implementation of the proposed method and experimental evaluation.
The idea of using catamorphisms for verification of programs with ADTs itself is
not new [34,30,28,16,9]. Thus, our main contributions lie in the formalization and
implementation of the procedure for automatically discovering catamorphisms
in the context of CHC solving.
    The rest of this paper is organized as follows. Section 2 reviews CHCs over
ADTs and catamorphisms for ADTs. Section 3 gives an overview of our frame-
work. Section 4 formalizes our catamorphism-based abstraction, and Section 5
introduces our template-based catamorphism synthesis procedure. Section 6 re-
ports the experimental results. Section 7 discusses related work, and Section 8
concludes the paper.

2     Preliminaries
2.1    Constrained Horn Clauses modulo Algebraic Data Types and
       Integer Arithmetic
We consider a standard first-order logic and a theory of algebraic data types and
integer arithmetic, which is written as TADT+Z . We also denote the theory of
integer arithmetic by TZ . For simplicity, we consider formulas that involve only
integers and a single algebraic data type (ADT) (δ, { C1 , . . . , Ck }) where δ is a
sort and Ci is a function symbol called a constructor.4 Each constructor Ci is
assumed to be a function of mi + ni arguments with its sort specified as
                                m                 n
                          z     }|i       { z }|i {
                         (int × · · · × int × δ × · · · × δ) → δ.
4
    Extending our proposed method to support multiple ADTs is straightforward. As
    detailed in Section 6, our implementation is already capable of handling multiple
    ADTs within a single instance. In a standard theory of algebraic data types, pro-
    jections and testers are used as the standard connectives for algebraic data types
    in addition to constructors. We omit them for simplicity, since they can be easily
    removed by standard preprocessing techniques (c.f. Section 4.5 of [23]).
4          Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

Note that mi + ni can be 0. We often simply write δ to mention the ADT.

Example 1. An algebraic data type for natural numbers nat in the introduction
is defined as (nat, { Z, S }) where Z is a constant of sort nat and S has the sort
nat → nat. An algebraic data type for integer lists, written as ilist, is defined
as (ilist, { nil , cons }) where nil is a constant of sort ilist and cons has the sort
int × ilist → ilist. A list [1; 2] is written as cons(1, cons(2, nil )).            ⊔
                                                                                    ⊓

      The sets of terms and constraint formulas are defined by:

                   (terms) t ::= x | n | Ci (tei ) | t1 op t2
    (constraint formulas) θ ::= tt | ff | θ1 ∧ θ2 | θ1 ∨ θ2 | t1 ▷◁ t2 | ∃xξ . θ | ∀xξ . θ.

Here, x, n, and ξ are metavariables for variables, integers, and sorts respectively,
▷◁ ranges over binary predicates in { =int , ̸=int , >, ≤, =δ } and op ranges over
binary arithmetic operations { +, −, × }. We also write tei for a sequence of terms
t1 , . . . , tk . The predicate =δ takes two terms of sort δ, while others take two
terms of sort int. For technical convenience, we omit the disequality ̸=δ for
ADT; it can be encoded using CHCs. (c.f. Section 4.4 of [23]). We also use
(t1 , . . . , tk ) =int k (t′1 , . . . , t′k ) as a syntax sugar for the conjunction of equalities
t1 =int t′1 ∧ · · · ∧ tk =int t′k .
      We write FV(t) and FV(θ) for the set of free variables, and ∀θ and ∃θ for
the universal and existential closures of θ, respectively. We also write Hδ for
the set of ground terms (i.e., with no free variables) of sort δ. We call non-
ground terms open terms, and terms without constructors arithmetic terms. A
constraint formula θ is quantifier-free if no quantifier occurs in θ. We consider
only well-sorted terms and formulas, where well-sortedness is defined in the stan-
dard manner. Substitutions such as [t/x]t′ and [t/x]θ are defined as usual. The
semantics of terms and formulas are also given in the standard way.
      A constrained Horn clause (CHC) (over algebraic data types and integer
arithmetic) is a formula of the form

                          int , yeδ . H ⇐ θ ∧ P (te ) ∧ · · · ∧ P (te ).
                        ∀xg                    1 1               k k


Here, Pi (tei ) is a predicate application, θ is a quantifier-free constraint formula,
and H is either ff or a predicate application P (tg   k+1 ). For simplicity, universal
quantifiers are often omitted. We call a finite set of CHCs a system of CHCs. We
use C and S as the metavariables for CHCs and systems of CHCs, respectively.
A system of CHCs is (or simply, CHCs are) said to be satisfiable if there is an
interpretation of predicate variables that makes all the clauses valid.

Example 2. Recall the CHCs over the ADT nat in Section 1, consisting of the
predicates PlusNat and Lt. The CHCs are satisfiable under the model:
                       ∆                                               ∆
    PlusNat(x, y, z) = size(x) + size(y) = size(z) Lt(x, y) = size(x) < size(y),

where the function size from nat to integers is defined by size(S n (Z)) = n.                   ⊔
                                                                                                ⊓
                    Catamorphism Synthesis for Program Invariants over ADT                      5

2.2    Catamorphisms
We introduce catamorphisms for δ, which are generalized fold functions that
map instances of Hδ to N -tuples of integers. Here, N is called the approximation
degree. A catamorphism C (for δ) is defined as a map constructed as follows:
               ∆
         C(x) =match x with
                      case C1 (ye1 , z1 , . . . , zn1 ) ⇒ F1 (ye1 , C(z1 ), . . . , C(zn1 ))
                          ..
                           .
                      case Ck (yek , z1 , . . . , znk ) ⇒ Fk (yek , C(z1 ), . . . , C(znk )).

Here, Fi is called a structure map for Ci . Recall that the constructor Ci takes mi
arguments of sort int and ni arguments of sort δ. The structure map Fi takes
mi integers and ni N -tuples of integers, and returns an N -tuple of integers. We
also write C F1 ,...,Fk for C when clarifying the structure maps. Furthermore, if a
                                                                              F1 ,...,Fk
catamorphism has free variables a1 , . . . , al in the definition, we write C { a1 ,...,al } .

Example 3. A catamorphism for ilist is of the form
                           ∆
            C Fnil ,Fcons (x) =match x with
                                    case nil ⇒ Fnil
                                    case cons(x, l) ⇒ Fcons (x, C Fnil ,Fcons (l))

where Fnil and Fcons are structure maps for the two constructors nil and cons,
respectively. For Fnil = 0 and Fcons (x, l) = 1 + l, C Fnil ,Fcons is the list length
function, and for Fnil = 0 and Fcons (x, l) = x + l, C Fnil ,Fcons is the function for
computing the sum of list elements. The catamorphism defined by the structure
maps Fnil = (0, 0) and Fcons (x, (l1 , l2 )) = (1 + l1 , x + l2 ) has the approximation
degree 2; it maps an integer list to a pair consisting of the list length and the
sum of elements.
   Similarly, we define a catamorphism Csize for nat as C FZ ,FS where FZ = 0
and FS (x) = 1 + x. This corresponds to size used in Example 2.                       ⊔
                                                                                      ⊓


3     Overview
This section gives an overview of the proposed procedure, called Catalia, which
follows a framework of template-based synthesis and counterexample-guided ab-
straction refinement (CEGAR) [6], as illustrated in Figure 1.
    Given a system S of CHCs over algebraic data types and integer arithmetic,
we first abstract them to a system S′ of CHCs over integer arithmetic. When S′
is unsatisfiable, Catalia generates a constraint formula θ (called a counterex-
ample), which witnesses the possible unsatisfiability of S, based on a resolution
proof for unsatisfiability of S′ . If θ is satisfiable, S is indeed unsatisfiable; other-
wise, we refine the catamorphism C using θ in the refinement phase.
6        Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato


               CHC over TADT+Z



                Abstraction αC                                           Refinement
                                             Catamorphism C
                 (Section 4)                                             (Section 5)

                                                                    No
                 CHC over TZ                                             Yes
                                                               Is SAT?         UNSAT


         Yes                       No
SAT                Is SAT?                       CEX θ


                                 Fig. 1: Overview of Catalia


   Below, we briefly explain the abstraction, counterexample generation, and
synthesis phases of Catalia. We will provide more details for the abstraction
and synthesis phases in Sections 4 and 5, respectively.


3.1    Abstraction

Recall the following system of CHCs given in Section 1.

                  (i) PlusNat(m, Z, m).
                  (ii) PlusNat(m, S(n), S(r)) ⇐ PlusNat(m, n, r).
                 (iii) Lt(Z, S(n)).        (iv) Lt(S(m), S(n)) ⇐ Lt(m, n).
                  (v) ff ⇐ PlusNat(m, n, r) ∧ Lt(r, m).

   Using the catamorphism C FZ ,FS where FZ = 0 and FS (x) = 1 + x, we obtain
the following abstracted version of CHCs.

    PlusNat(m, 0, m) ⇐ P δ (m).
    PlusNat(m, n + 1, r + 1) ⇐ P δ (m) ∧ P δ (n) ∧ P δ (r) ∧ PlusNat(m, n, r).
    Lt(0, n + 1) ⇐ P δ (n).         Lt(m + 1, n + 1) ⇐ P δ (m) ∧ P δ (n) ∧ Lt(m, n).
    ff ⇐ P δ (m) ∧ P δ (n) ∧ P δ (r) ∧ PlusNat(m, n, r) ∧ Lt(r, m).
    P δ (0).      P δ (n + 1) ⇐ P δ (n).

Here, we have replaced each variable or term of sort nat with one of sort int
by applying the catamorphism. We have also added P δ (x) for each universally
quantified variable x (whose sort is nat in the original CHCs and int after the
abstraction); this is for the purpose of restricting the range of the variable to the
image of the catamorphism. (In other words, a formula ∀xnat .φ(x) is abstracted
                        Catamorphism Synthesis for Program Invariants over ADT               7

to ∀xint .P δ (x) ⇒ φ′ (x) where φ′ (x) is an abstract version of φ(x).) The defini-
tion of P δ , called the C-admissibility predicate, is obtained automatically from
the following predicate that should be satisfied by every variable of sort nat,
which was implicit in the original CHCs.
                                Pδ (Z).      Pδ (S(x)) ⇐ Pδ (x).
Note that, without the predicate P , the abstraction would be too coarse. For
example, consider a CHC ∀xnat . ff ⇐ S(x) = Z, which is valid (as S(x) =
Z never holds). Without the P predicate, however, it would be abstracted to
∀xint . ff ⇐ x + 1 = 0, which is invalid.
   The abstracted CHCs above are satisfiable with the following model:
                            ∆                             ∆                    ∆
      PlusNat(m, n, r) = m + n = r               Lt(x, y) = x < y       P δ (n) = n ≥ 0.
We can therefore conclude that the original CHCs are also satisfiable, with the
following model:
                                ∆                                      ∆
        PlusNat(m, n, r) = C(m) + C(n) = C(r)                 Lt(x, y) = C(x) < C(y).
   A remaining issue is how to abstract the primitive equality predicate =nat .
We can simply replace it with =int ; this is a sound abstraction, since x =nat
y implies C(x) =int C(y). In contrast, x ̸=nat y does NOT imply C(x) ̸=int
C(y); that is why we exclude out ̸=δ from the set of primitive predicates (recall
Section 2), and encode the inequality by using CHCs.

3.2     Counterexample Generation
Now, we consider the case where the abstracted CHCs are unsatisfiable. If the
catamorphism C 0,λx.0 (which maps all the natural numbers to 0) were used
instead of C 0,λx.x+1 , the original CHCs would be abstracted to the following
CHCs over TZ , which are unsatisfiable.
       (i′ ) PlusNat(m, 0, m) ⇐ P δ (m).
      (ii′ ) PlusNat(m, 0, 0) ⇐ P δ (m) ∧ P δ (n) ∧ P δ (r) ∧ PlusNat(m, n, r).
      (iii′ ) Lt(0, 0) ⇐ P δ (n).         (iv ′ ) Lt(0, 0) ⇐ P δ (m) ∧ P δ (n) ∧ Lt(m, n).
       (v ′ ) ff ⇐ P δ (m) ∧ P δ (n) ∧ P δ (r) ∧ PlusNat(m, n, r) ∧ Lt(r, m).
      (vi′ ) P δ (0).      (vii′ ) P δ (0) ⇐ P δ (m).
Notice that the abstracted CHCs (i′ ) − (v ′ ) correspond to the original CHCs
(i) − (v).
    Suppose the following (SLD-)resolution proof was generated by a CHC solver
as a witness of unsatisfiability.
            ff ⇐ P δ (m) ∧ P δ (n) ∧ P δ (r) ∧ PlusNat(m, n, r) ∧ Lt(r, m)
                                                                                     (i′ )
        ff ⇐ P δ (m) ∧ P δ (n) ∧ P δ (r) ∧ n = 0 ∧ m = r ∧ P δ (m) ∧ Lt(r, m)
                                                                                   (iii′ )
ff ⇐ P δ (m) ∧ P δ (n) ∧ P δ (r) ∧ n = 0 ∧ m = r ∧ P δ (m) ∧ m = r = 0 ∧ P δ (n′ )
                                                                                   (vi′ )
                             ff ⇐ m = n = r = n′ = 0
8       Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

The derivation starts with the goal clause, and in the last step, the resolution on
multiple occurrences of P δ has been performed in one step. We have indicated
which CHC has been used in each resolution step. Note that the last clause is
invalid, which indicates that the abstracted CHCs are unsatisfiable.
    From the resolution proof for the abstract CHCs above, we construct the
following candidate of a resolution proof for the unsatisfiability of the origi-
nal CHCs, by applying the corresponding clause of the original CHCs (i.e., the
clauses (i) and (iii) instead of (i’) and (iii’) respectively) except for the clauses
on the C-admissibility predicate.
                     ff ⇐ PlusNat(m, n, r) ∧ Lt(r, m)
                                                      (i)
                      ff ⇐ m = r ∧ n = Z ∧ Lt(r, m)
                                                          (iii)
                 ff ⇐ m = r ∧ n = Z ∧ r = Z ∧ m = S(n′ )
                                                                     ∆
The right-hand side of the last clause can be simplified to: θ = Z = S(n′ ).
We call θ a counterexample (against the satisfiability of the original CHCs); it
serves as a possible witness of the unsatisfiability of the original CHCs, in the
sense that if θ were satisfiable, we could conclude that the original CHCs were
unsatisfiable. In this case, however, θ is unsatisfiable; the abstract CHCs yielded
a spurious resolution proof for the original CHCs.

3.3   Synthesis
For the example in the previous subsection (where θ ≡ Z = S(n′ )), we need to
find a catamorphism C ′ = C FZ ,FS such that
                              ∃nnat . FZ = FS (C ′ (n))
is invalid. By preparing a template FZ = a and FS (n) = b × n + c for FZ and
FS , the problem above is reduced to the satisfiability problem:
                      ∃a, b, c. ∀nnat . a ̸= b × C FZ ,FS (n) + c.
     Solving the above satisfiability problem is costly, since it is an ∃∀-formula
and also involves the recursive function C FZ ,FS . We thus provide a procedure
for solving this ∃∀-formula based on counterexample-guided inductive synthe-
sis (CEGIS), which we will explain in detail in Section 5. This procedure may
return a = 0 and b = c = 1 as a witness and synthesize a new catamorphism
C 0,λx.x+1 . We then go back to the abstraction step of the CEGAR cycle, and in
this case, succeed in proving the satisfiability of the original CHCs, as explained
in Section 3.1.

4     Abstraction
This section explains more details about the abstraction step.
    In this section, we use the following more tricky example as a running exam-
ple. To the best of our knowledge, most of the previous approaches [15,22,23,16]
struggle with the example,while our approach can easily solve it.
                     Catamorphism Synthesis for Program Invariants over ADT                   9

Example 4. We consider the following CHCs:

         G(nil , 0, 0).      G(cons(x, l), x + n, m) ⇐ G(l, m, n).
         Gen(nil , 0).        Gen(cons(x, cons(x − 1, l)), n) ⇐ Gen(l, n − 1).
         ff ⇐ m − n ̸= x ∧ x ≥ 0 ∧ Gen(l, x) ∧ G(l, m, n).

Here, G and Gen are predicate symbols of sorts ilist ×int ×int → bool , and ilist ×
int → bool respectively. Intuitively, G(l, m, n) means that the sums of elements of
l at even and odd indices are m and n respectively (where an index starts from 0).
The predicate Gen(l, n) holds if l is a list of the form [m0 ; m′0 ; · · · ; mn−1 ; m′n−1 ]
where mi = m′i + 1 for each i = 0, . . . , n − 1. The last clause asserts that if
Gen(l, x) holds, then the difference between the sums of elements at even and
odd indices is x. The above system of CHCs is satisfiable, where the models of
G and Gen are as informally explained above.
    Let Ceo be C Fnil ,Fcons where Fnil = 0 and Fcons (x, l) = x − l. This catamor-
phism is sufficient for proving the satisfiability of the CHCs above.                   ⊔
                                                                                        ⊓

    Suppose the approximation degree is N , and we have a catamorphism C F1 ,...,Fk ,
which is a map from Hδ to ZN . We define an abstraction of CHCs αC induced
by C.
    Before applying the abstraction, we add the atom Pδ (x), where Pδ is a unary
predicate that takes a value of sort δ, to the body of each clause, for each
variable x of sort δ. Intuitively, Pδ (x) means that x ranges over the set of
terms of sort δ. We add the following clause for each constructor Ci of sort
       mi                 n
 z     }|        { z }|i {
(int × · · · × int × δ × · · · × δ) → δ.

             Pδ (Ci (x1 , . . . , xmi , y1 , . . . , yni )) ⇐ Pδ (y1 ) ∧ · · · ∧ Pδ (yni ).

It ensures that the least model of Pδ indeed has the meaning described above.
Obviously, the CHCs augmented with Pδ is equi-satisfiable with the original
CHCs. Nonetheless, Pδ is added because the abstraction of Pδ yields the “C-
admissibility predicate” mentioned in Section 3. The abstraction of Pδ (x) ensures
the integer variables obtained by abstracting x to range over the image of the
catamorphism.

Example 5. For the example in Example 4, the augmented CHCs are:

      (i) G(nil , 0, 0).       (ii) G(cons(x, l), x + n, m) ⇐ Pilist (l) ∧ G(l, m, n).
    (iii) Gen(nil , 0).
     (iv) Gen(cons(x, cons(x − 1, l)), n) ⇐ Pilist (l) ∧ Gen(l, n − 1).
      (v) ff ⇐ m − n ̸= x ∧ x ≥ 0 ∧ Pilist (l) ∧ Gen(l, x) ∧ G(l, m, n).
     (vi) Pilist (nil ).     (vii) Pilist (cons(x, l)) ⇐ Pilist (l).

                                                                                              ⊔
                                                                                              ⊓
10        Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

The augmented CHCs are abstracted as follows. Let C be a clause ∀xg               eδ .H ⇐=
                                                                            int , y

θ ∧ P1 (te1 ) ∧ · · · ∧ Pn (ten ), and Ξ be a variable abstraction environment, which is a
finite map from variables to N -tuples of variables, such that Ξ(yi ) = (y1i , . . . , yN
                                                                                        i
                                                                                          )
                        δ          1      l
for each yi ∈ { ye } = { y , . . . , y }. We define αC (C) as

           x, yeji . αC,Ξ (H) ⇐= αC,Ξ (θ) ∧ αC,Ξ (P1 (e
          ∀e                                          t1 )) ∧ · · · ∧ αC,Ξ (Pn (e
                                                                                tn )).

Here, yeji denotes y11 , . . . , yN
                                  1
                                    , . . . , y1l , . . . , yN
                                                             l
                                                               , and the abstraction αC,Ξ for atoms,
constraint formulas, and terms is defined by:

         t)) = P (αC,Ξ (e
αC,Ξ (P (e              t))              αC,Ξ (tt) = tt                   αC,Ξ (ff) = ff
αC,Ξ (t1 =δ t2 ) = αC,Ξ (t1 ) =        int N   αC,Ξ (t2 )
αC,Ξ (p(a1 , . . . , al )) = p(a1 , . . . , al )         (if p is a built-in predicate on integers)
αC,Ξ (φ1 ∧ φ2 ) = αC,Ξ (φ1 ) ∧ αC,Ξ (φ2 )    αC,Ξ (φ1 ∨ φ2 ) = αC,Ξ (φ1 ) ∨ αC,Ξ (φ2 )
           
             Ξ(x) if x ∈ dom(Ξ)
αC,Ξ (x) =                                αC,Ξ (a) = a (if a is an integer term)
             x     otherwise
αC,Ξ (Ci (a1 , . . . , ami , t1 , . . . , tni )) = Fi (a1 , . . . , ami , αC,Ξ (t1 ), . . . , αC,Ξ (tni )).

As defined above, we just recursively replace each constructor Ci with the cor-
responding structure map Fi , and the equality =δ on ADT with the equality
=int N on integer tuples.

Example 6. Recall the augmented CHCs in Example 5 and the catamorphism
Ceo given in Example 4. We obtain the following abstracted CHCs.

         G(0, 0, 0).         G(x − l, x + n, m) ⇐ P ilist (l) ∧ G(l, m, n).
         Gen(0, 0).            Gen(x − ((x − 1) − l), n) ⇐ P ilist (l) ∧ Gen(l, n − 1).
         ff ⇐ m − n ̸= x ∧ x ≥ 0 ∧ P ilist (l) ∧ Gen(l, x) ∧ G(l, m, n).
         P ilist (0).      P ilist (x − l) ⇐ P ilist (l).

They have the following model.
                           ∆                                   ∆                            ∆
             G(l, y, z) = l = y − z                Gen(l, y) = l = y            P ilist (l) = tt.
                         ∆
We have P ilist (l) = tt because the image of Ceo is Z, but we note that this is
not the case in general.5
   By the soundness theorem given below, we can conclude that the original
CHCs given in Example 4 are satisfiable. Indeed, the following is the model for
the original CHCs.
                               ∆                                              ∆
                G(l, y, z) = Ceo (l) = y − z            and Gen(l, y) = Ceo (l) = y.

                                                                                                              ⊔
                                                                                                              ⊓
                                                                                                     ∆
5
     For example, a model for the predicate P δ in Section 3.1 is given by P δ (x) = x ≥ 0.
                    Catamorphism Synthesis for Program Invariants over ADT                 11

  We now discuss the soundness of abstraction. The following lemma follows
immediately from the above construction.
Lemma 1. For any system S of CHCs, αC (S) is a system of CHCs defined over
integer arithmetic.
The following theorem states the soundness, and also describes how a model of
the original CHCs can be constructed from that of the abstract CHCs.
Theorem 1 (Soundness). Let S be a system of CHC over TADT+Z . If αC (S)
is satisfiable, then so is S. Furthermore, from a model M1 of αC (S), we can
construct a model M2 for S. The interpretation of a predicate P : δ m × int n
                                                             M1
in M2 is given as a function P M2 (x1 , . . . , xm , ye) = P    (C(x1 ), . . . , C(xm ), ye),
          M1
where P       is the interpretation of P in M1 .
    A proof is given in Appendix A. Here we provide an informal argument.
Notice that, for any predicate P : δ m × int n , ground terms t1 , . . . , tm and in-
tegers e                       k) holds under M2 (i.e., P M2 (t1 , . . . , tm , e
       k, P (t1 , . . . , tm , e                                                  k) holds) if
and only if αC (P (t1 , . . . , tm , k)) = P (C(t1 ), . . . , C(tm ), k) holds under M1 (i.e.,
                                     e                                e
  M1
P    (C(t1 ), . . . , C(tm ), e
                              k) holds). For any ground constraint formula θ, ¬αC (θ)
implies ¬θ. Thus, for any ground clause H ⇐ θ ∧ P1 (te1 ) ∧ · · · ∧ Pk (tek ), if M1 is
a model of αC (H) ⇐ αC (θ) ∧ αC (P1 (te1 )) ∧ · · · ∧ αC (Pk (tek )), then M2 is a model
of H ⇐ θ ∧ P1 (te1 ) ∧ · · · ∧ Pk (tek ).
    Recall the model of the original CHCs in Example 6. The interpretation
  M2            ∆                                                                M1         ∆
G (l, x, y) = (Ceo (l) = x − y) for G has been obtained from G (l, x, y) =
(l = x − y), by just replacing l with Ceo (l) based on the theorem above.


5     Template-based and Counterexample-guided
      Catamorphism Synthesis
We adopt a template-based approach to catamorphism synthesis; we prepare a
set of predefined template catamorphisms and derive constraints for C to satisfy.
As detailed later, such constraints involve universal quantifiers over ADTs and
recursively defined functions, which are difficult for SMT solvers to handle. To
address this problem, we employ a counterexample-guided approach with testing.

5.1    Template-based Catamorphism Synthesis
We define a template catamorphism as a catamorphism parameterized by inte-
gers. Here, each constructor Ci has an associated template structure map repre-
                                   (1)                 (N )
sented by a tuple of open terms (ti [e x, e
                                          a], . . . , ti [e    a]) of sort int × · · · × int
                                                            x, e
where xe are arguments of the catamorphism and e         a are integer parameters.
    Let T be a template catamorphism, and M be an assignment of the pa-
rameters ea to integers. A catamorphism M(T ), a catamorphism obtained by
substituting each parameter ai with M(ai ) in T , is said to be an instantiation
of the template catamorphism T .
12         Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

    We often use linear template catamorphisms, which are template catamor-
phisms whose associated template structure maps are affine functions. We denote
a linear template catamorphism of degree 1 by L.

Example 7. For ilist, L is given by the template structure maps:

                           Fnil = d,       Fcons (x, l) = a × l + b × x + c

with parameters a, b, c, d.                                                                             ⊔
                                                                                                        ⊓

Remark 1. In practice, we design our templates based on a trade-off between
the expressive power of the abstraction and the cost of catamorphism synthesis.
As explained in Section 6, our implementation uses restricted linear template
catamorphisms L[a,b] to efficiently explore the search space, where the range of
each parameter of L is limited to [a, b]. For example, a restricted linear template
catamorphism for ilist, denoted by L[−1,1] , is given by:

         Fnil = d,       Fcons (x, l) = a × l + b × x + c where a, b, c, d ∈ [−1, 1].

    We gradually increase the expressiveness of the templates by increasing the
parameter ranges and the approximation degree, until they suffice to prove the
satisfiability of the given CHCs. In our implementation, we prepare the following
sequence of template catamorphisms:

      L[−1,1] , (L[−1,1] , L[−1,1] ), (L[−1,1] , L[−1,1] , L[−1,1] ), (L[−2,2] , L[−2,2] , L[−2,2] ),
      (L[−4,4] , L[−4,4] , L[−4,4] ), . . . .

Here, we assume each L[a,b] has its own unique set of parameters, and an N -tuple
of template catamorphisms (T1 , . . . , Tk ) represents a template catamorphism of
N -approximation degree, defined by λλ x           x), . . . , Tk (e
                                           e. (T1 (e               x)).
    We could also consider templates containing disjunctive properties, but in-
ferring such templates would be more costly; it is left for future work.
    Note that the templates are prepared and fixed in advance, and are inde-
pendent of specific CHCs or data structures. The parameters required for each
constructor are determined by its sort, and can be derived automatically.       ⊔
                                                                                ⊓

   We introduce a constraint generation map ⟨·⟩T , which is used later to find
appropriate instantiations of template catamorphisms. It is defined by:

     ⟨∀x.θ⟩T = ∀x.⟨θ⟩T           ⟨t1 =δ t2 ⟩T = (T (t1 ) =int N T (t2 )) ⟨p(e
                                                                            a)⟩T = p(e
                                                                                     a)
     ⟨θ1 ⋆ θ2 ⟩T = ⟨θ1 ⟩T ⋆ ⟨θ2 ⟩T for ⋆ ∈ {∧, ∨}           ⟨¬θ⟩T = ¬⟨θ⟩T .

Here, we assume that T is a symbol of a recursively defined function of sort
δ → int N that encodes the template catamorphism. Note that in Section 5 we
use an extended form of constraint formulas (used only for our catamorphism
synthesis) that allows the negation operator ¬ for convenience.
                 Catamorphism Synthesis for Program Invariants over ADT         13

Procedure 1 Counterexample-Guided Catamorphism Synthesis
 1: Input: CHCs over TADT+Z S
 2: Output: satisfiable / unsatisfiable / unknown
 3: (C, S) ← (C0 , ∅)
 4: for T in T do
 5:     Θ ← tt
 6:     loop
 7:        S′ ← αC (S)
 8:        r ← check_sat_chc(S′ )
 9:        if r = satisfiable then return satisfiable
10:        θ ← get_cex(r, S)
11:        if check_sat_smt(θ) then return unsatisfiable
12:        S ← S ∪ { ∀¬θ }
13:        (C, Θ) ← synthesis( S, C, Θ, T )
                               V
14:        if (C, Θ) is None then break
15:     end loop
16: end for
17: return unknown



Example 8. Let θ be the (extended) constraint formula ¬(cons(0, cons(0, l)) =δ
                                                     Fnil ,Fcons
nil ), and T be the linear template catamorphism C { a,b,c,d } in Example 7. By
applying ⟨·⟩T to θ, we obtain ¬(T (cons(0, cons(0, l))) =int T (nil )), which can
be simplified to

                          a × (a × T (l) + c) + c ̸=int d

by using the defining axioms of T .                                              ⊔
                                                                                 ⊓

5.2   Counterexample-Guided Catamorphism Synthesis
We now discuss the CEGAR procedure of Catalia in more detail, shown in
Procedure 1.
    The procedure maintains two internal states: the current catamorphism C
and a set S of the negations of counterexample formulas. We call elements of
S proof obligations; they are valid formulas over ADTs, whose validity should
be preserved by the catamorphism-based abstraction. Initially, we set C to the
default catamorphism C0 and S to the empty set. The choice of C0 is arbitrary.
    We iterate over a sequence of template catamorphisms T, which is prepared
in advance as described in Remark 1. For now, let us ignore Θ and focus on the
inner loop (line 6-15). The first part of the inner loop (line 7-11) is the same as
described in Section 3. When a candidate counterexample θ for S is spurious,
we add ∀¬θ to the set S and proceed to the synthesis phase (line 12-13). When
the synthesis phase fails to find a new catamorphism, we break the loop and try
another template catamorphism (line 14).
    A notable difference from the standard CEGAR approach is to relax the goal
of the synthesis procedure: to tackle the challenges described below, we allow it
14      Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

Procedure 2 Procedure synthesis
 1: Input: θ, C, Θ, and T
 2: Output: C ′ and Θ′
 3: θ′ ← a quantifier-free formula such that θ ≡ ∀e x. θ′
 4: timeout ← ∞
 5: loop
 6:      x 7→ ve] ← check_sat_with_TO(¬⟨θ′ ⟩C , timeout)
        [e                                                            ▷ Testing
 7:         x 7→ ve] is None or timeout then return (C, Θ)
        if [e
 8:     timeout ← defaultTimeout
 9:     Θ ← Θ ∧ θ′′ where θ′′ ≡ [e    x]⟨θ′ ⟩T
                                   v /e                ▷ T does not occur in θ′′
10:      M ← check_sat(Θ)                                   ▷ SAT modulo NIA
11:      if M is None then return None
12:      C ← M(T )
13: end loop



to return a catamorphism
                    V       C that does not necessarily preserve the validity of
the proof obligation S. As a result, the same spurious counterexample θ might
be encountered multiple times at line 10. To prevent it, we store a constraint
formula Θ, which accumulates information from the synthesis exploration. This
formula represents necessary conditions for the template parameters, enabling
the synthesis process to resume from its previous state when needed, as detailed
below.


Challenges in Catamorphism
                    V          Synthesis Synthesizing a catamorphism from
the proof obligation S faces two main challenges:

 1. The proof obligation involves universal quantifiers over ADTs and recursive
    definitions, which SMT solvers struggle to handle.
 2. Even after Vsynthesizing a catamorphism C, checking whether C preserves the
    validity of S remains costly as it still involves recursively defined functions
    and ADTs.

To address these challenges, we adopt an approach proposed by Reynolds et
al. [31], a variant of counterexample-guided inductive synthesis (CEGIS), com-
bined with a lightweight testing approach.


Procedure synthesis Procedure 2 shows the synthesis procedure. This proce-
dure takes a proof obligation θ, a current catamorphism C, a constraint formula
Θ, and a template catamorphism T as inputs. Here, θ and C satisfy ̸|= ⟨θ⟩C but
|= θ. The goal of the procedure is to find a new catamorphism C ′ that is likely
to satisfy |= ⟨θ⟩C .
    As in ordinary CEGIS, the procedure consists of two phases: (a) verifica-
tion (line 6) and (b) synthesis (line 10). The former checks whether the current
candidate of C satisfies ∀x̃. θ′ by checking whether ¬⟨θ′ ⟩C is satisfiable. If so, we
obtain ground terms ṽ such that [ṽ/x̃]⟨θ′ ⟩C is invalid, and update Θ to (a formula
                    Catamorphism Synthesis for Program Invariants over ADT           15

equivalent to) Θ ∧ [ṽ/x̃]⟨θ′ ⟩T . This enables us to synthesize a new catamorphism
in a counterexample-guided manner on line 10.
    A difference from the standard CEGIS is that we give up checking the satisfi-
ability of ¬⟨θ′ ⟩C upon a time-out on line 6. This is because an SMT prover is not
good at proving the unsatisfiability of ¬⟨θ′ ⟩C . If the satisfiability check times out,
then we optimistically assume that ⟨θ′ ⟩C is valid, and returns the current cata-
morphism C as a candidate solution. In that case, it remains unknown whether
⟨θ⟩C is indeed valid; thus, the same counterexample as the previous might be
encountered in Procedure 1 again.
    To ensure the progress even with this relaxation, we accumulate the necessary
conditions Θ for the template parameters of T inside the synthesis loop (line
9) and return Θ to Procedure 1. This allows Procedure 2 to resume from the
previous state whenever Procedure 1 encounters the same counterexample again.
For the progress, we must additionally require that the given catamorphism is
refined at least once during each synthesis call. To this end, we initialize the
timeout to ∞ (line 4) and later reset it to a default finite value (line 8). This
is justified by the fact that ⟨θ⟩C for the given catamorphism C is already known
to be invalid by Procedure 1; therefore, an SMT solver should be able to find a
model for ¬⟨θ′ ⟩C on line 6.

Example 9. Let C be C Fnil,0 ,Fcons,0 where Fnil,0 = 0 and Fcons,0 (x, l) = 0, θ be
                ∆
∀lδ .θ′ where θ′ = ¬(cons(0, cons(0, l)) =δ nil ), Θ be tt, and T be the linear tem-
plate catamorphism in Example 7 for ilist. We execute Procedure 2 with these
inputs: θ, C, Θ, T . We first check whether ¬⟨θ′ ⟩C ≡ C(cons(0, cons(0, l))) =int
C(nil ) is satisfiable, and find a model [l 7→ nil ]. As all arguments of sort δ in
the catamorphism applications within [nil /l]⟨θ′ ⟩T are ground terms, [nil /l]⟨θ′ ⟩T
can be simplified to: a × (a × d + c) + c ̸= d. We then update Θ to a ×
(a × d + c) + c ̸= d. Suppose an SMT solver yields the following model for
Θ: M ≡ { a 7→ 0, b 7→ 0, c 7→ 1, d 7→ 0 } . Based on this model, we have a new
catamorphism C1 defined by C Fnil,1 ,Fcons,1 where Fnil = 0 and Fcons (x, l) = 1.
Now the backend SMT solver either proves that |= ⟨θ⟩C1 holds or times out.
Therefore, we return C1 and Θ as the result of Procedure 2.                        ⊔
                                                                                   ⊓


5.3   Discussions

We discuss properties of the overall procedure of Catalia in this subsection. We
have already shown the soundness of the procedure in Section 4 (Theorem 1).
Other important questions are:

 1. Relative completeness: Let S be a system of CHCs, and suppose that αC (S)
    is satisfiable for some αC (where C belongs to the class of catamorphisms
    expressed by a given set of templates). Assuming that the backend CHC
    solver over integers and SMT solver were sound and complete, does Catalia
    eventually prove that S is satisfiable?
 2. Refutational completeness: Let S be a system of CHCs, and suppose that S
    is unsatisfiable. Assuming that the backend CHC solver over integers and
16       Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

      SMT solver were sound and complete, does Catalia eventually prove that
      S is unsatisfiable?

We need to make some modifications and further assumptions to guarantee that
relative completeness and refutational completeness hold.
    We can ensure relative completeness by ensuring that the values of template
parameters are chosen from a finite set, and the set and the approximation de-
gree N are gradually increased (as explained in Remark 1) when there is no
solution for the constraints in the current template, so that the whole class of
catamorphisms being considered is eventually covered. Note that given a tem-
plate catamorphism, the same catamorphism is not encountered again since the
necessary conditions are accumulated in Θ in Procedure 2. Thus, if αC (S) is
satisfiable for some αC and such αC is an instance of the current template cata-
morphism, it will eventually be found.
    Refutational completeness holds if the underlying solver for CHC (over inte-
gers) generates resolution proofs in a fair manner, in the sense that, given an
infinite sequence of unsatisfiable CHCs S1 , S2 , . . . if every Si has a resolution proof
of the same “shape” (except for constraint formulas), then that resolution proof
is eventually produced. That is because if S is unsatisfiable, then its augmented
version also has a resolution proof, and all of its abstractions αC1 (S), αC2 (S), . . .
have the resolution proof of the same shape. Thus, by the assumption of fairness,
that resolution proof is eventually generated.
    The assumption on the fairness above may be too strong in practice; in fact,
we do not think an existing CHC solver satisfies that property. A more reasonable
requirement would be to ensure that a CHC solver generates a resolution proof
of the smallest size. Then, it suffices to ensure that a resolution proof of the
same shape is never re-encountered, e.g., by removing a prior bound on the
approximation degree N and removing the timeout on line 9 of Procedure 2.


6     Implementation and Evaluation

We have implemented Catalia, a solver for the satisfiability checking problem
of CHCs over ADT and LIA. In this section, we describe the implementation
details and evaluate Catalia on the benchmark set from CHC-COMP 2024 [10].
As stated in the abstract, Catalia was used as a core part of the tool called
ChocoCatalia, which won the ADT-LIA category of CHC-COMP 2025 (which is
the only category ChocoCatalia participated in). ChocoCatalia relies on another
independent, complementary technique to be reported elsewhere, but Catalia
alone would have won the competition, judging from the evaluation result re-
ported below for the CHC-COMP 2024 benchmark.


6.1    Implementation

The solver consists of the following four components:
                   Catamorphism Synthesis for Program Invariants over ADT         17


                        Table 1: Number of Solved Instances
             Instance              Catalia RInGen Spacer Eldarica
             # SAT                        67       54      48         50
             # UNSAT                      80       46      86         87
             # ALL                       147      100     134        137
             # UNIQUE (SAT)               18       14       3          1
             # UNIQUE (UNSAT)              2        3       4          1



  (i) Preprocessing: To handle testers and selectors that are not directly sup-
      ported by our framework, we have implemented preprocessing steps de-
      scribed in Section 4 of [23].
 (ii) Abstraction: This is an implementation of the procedure described in Sec-
      tion 4. We utilized a portfolio of Spacer [22], Eldarica [15], and HoIce [5] as
      the backend solver for satisfiability checking problems of CHCs over integer
      arithmetic.
(iii) Counterexample Generation: We extract a (hyper-)resolution proof gen-
      erated by Z3/Spacer [27,22], when a system of abstracted CHCs over integer
      arithmetic is unsatisfiable. We parse the result, and obtain a counterexample
      θ as described in Section 3.2.
(iv) Refinement: Our implementation of the synthesis procedure from Section 5
      employs multiple linear templates (see Remark 1). The testing component
      (line 6-8 in Procedure 2) is executed by running Z3 with a timeout of one
      second.
   While the formalization in the previous sections was for CHCs over a single
ADT δ, the implementation can handle general CHCs over ADTs, including
those with mutually recursive definitions.

6.2    Evaluation
We evaluated Catalia on the ADT-LIA division of CHC-COMP 2024 [10],
which consists of 300 benchmark instances of satisfiable and unsatisfiable CHCs
over algebraic data types and linear integer arithmetic. The benchmark set is
publicly available [11]. For comparison, we selected three state-of-the-art CHC
solvers that support the theory of ADTs and LIA: Spacer [22], RInGen [23], and
Eldarica [15]. All the experiments were conducted on a machine with Intel Xeon
Gold 6242 CPU and 64GB of RAM. We set the timeout to 300 seconds. Further
details of the evaluation are publicly available [19].
    The results, summarized in Table 1 and Figure 2, show that Catalia per-
forms particularly well on satisfiable instances. It solved 67 satisfiable instances,
the most among all solvers. Additionally, it uniquely solved 18 satisfiable in-
stances that no other solver could solve successfully within 300 seconds. Our
approach primarily targets satisfiable CHCs, and the results confirm its effective-
ness in this category. Catamorphisms that Catalia successfully found include
18                             Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato


                                   Spacer                                                                            Spacer
                          2        Eldarica                                                           10
                                                                                                           2         Eldarica
                     10                                                                                              RInGen
                                   RInGen
                                   Catalia                                                                           Catalia

                                                                                                           1
                          1                                                                           10




                                                                                 running time [sec]
running time [sec]



                     10



                          0                                                                                0
                     10                                                                               10




                          −1                                                                               −1
                     10                                                                               10




                               0    25        50     75     100      125   150                                   0   10         20   30   40    50    60
                                         number of solved problems                                                        number of solved problems


                          (a) Results for All The Instances                                                     (b) Results for SAT Instances

Fig. 2: Cactus plots. The horizontal axis shows the number of solved instances,
and the vertical axis shows the time required to solve them.



the list length, the sum of an integer list, the evenness of the list length, and their
combinations. In terms of uniquely satisfiable instances, Catalia and RInGen
are complementary because they handle different classes of invariants. For ex-
ample, Catalia can handle the list length, whereas RInGen cannot. Conversely,
RInGen can handle invariants involving the last element of a list, which Catalia
cannot. The latter is due to Catalia’s restriction of template catamorphisms
to linear ones (cf. Remark 1). We expect that, by extending templates with
conditional expressions, Catalia will subsume RInGen’s capability; we leave
this extension for future work. For unsatisfiable instances, Catalia performed
slightly worse than Spacer and Eldarica. We also leave this issue for future work;
random testing techniques [18] may help address it.
    Figure 2 provides a detailed efficiency comparison across solvers. Spacer
demonstrates the fastest solving times overall, efficiently handling numerous in-
stances. However, its advantage lies primarily in speed rather than the number
of solved satisfiable instances; in fact, it uniquely solves only a few problems. In
contrast, Catalia, while slower in terms of solving time than Spacer, success-
fully solves more satisfiable instances, aligning with its design goal of handling
more complex invariants.



7                          Related Work


We discuss related work on SMT solvers and CHC solvers that support ADTs.
                  Catamorphism Synthesis for Program Invariants over ADT         19

7.1   SMT Solvers

The theory of ADT has been incorporated into the SMT-LIB Standard [3], the de
facto standard language specification for SMT solvers, and leading SMT solvers
such as Z3 [27], CVC5 [2] and Princess [33] already support this theory. Since
Oppen’s work [29], various decision procedures [38,34,35,24,32,30,36] have been
proposed to handle ADTs.
    Among these, several approaches [34,35,30,32] address satisfiability modulo
ADT and recursively defined functions (RDFs). The approaches by Reynolds
and Kuncak [32] and Yang et al. [36] tackled automated inductive reasoning
on ADTs and RDFs by an efficient enumeration of lemmas. Suter et al. [34,35]
introduced an abstraction method based on catamorphisms, which is similar to
our approach. They also proposed decision procedures based on the abstraction,
which were later refined by Pham et al. [30]. Our abstraction, however, differs in
that it is tailored for CHCs (e.g., by introducing C-admissibility predicates). In
particular, our approach is capable of automatically synthesizing catamorphisms,
leveraging the result of CHC solving.


7.2   CHC Solvers

Various approaches have been proposed to solve CHCs over ADTs in order to
capture more complex properties of ADTs [15,7,9,23,16,37,5,21]. Eldarica [15]
utilizes size constraints that represent the size of a given term to capture prop-
erties such as the list length. Size functions, which are also utilized in the deci-
sion procedures by Zhang et al. [38], can be seen as a special case of the cata-
morphisms introduced in this paper. De Angelis et al [7] proposed fold/unfold
transformation with techniques such as difference predicates [8] and catamor-
phic abstractions [9] to efficiently transform CHCs over ADTs to those without
ADTs. However, their solver is not capable of yielding a model even when it
successfully proves the satisfiability, and it requires users to manually supply
catamorphisms. Kostyukov et al. [23] reduced satisfiability checking of CHCs
to finite model finding of first-order logic, by approximating constructors with
uninterpreted functions. A notable limitation of this approach is its inability to
combine the theory of ADT with other theories such as linear integer arithmetic
(LIA) and arrays. Krishnan et al. [16] have proposed a Spacer-like procedure
for CHC over ADT and RDFs that preserves the refutational completeness of
the original Spacer algorithm. While their approach requires users to provide
catamorphisms, ours automatically synthesizes them. Some approaches [37,5]
transform predicates in CHCs to RDFs, thereby reducing the problem to check-
ing the satisfiability of formulas over ADTs and RDFs. However, as discussed
above, solving such a formula in SMT solvers can be challenging. Furthermore,
syntactically transforming predicates to functions is difficult especially when the
CHCs are generated from compiler intermediate representations (e.g., LLVM),
where the functional structure is often lost. Kobayashi and Wu [21] employed
a machine learning technique to synthesize inductive invariants over lists. They
train a recurrent neural network using an ICE learning framework and extract
20      Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

a fold (catamorphism) function using the technique proposed by Kobayashi et
al. [20]. Although their approach can, in theory, synthesize general recursive
functions, its scalability remains a significant challenge.


8    Conclusion

We have proposed a method to solve the satisfiability checking problem of con-
strained Horn clauses over algebraic data types and integer arithmetic. To find
models defined inductively on the structure of algebraic data types, we employed
catamorphisms to express inductive properties, and formalized a framework for
automatically discovering appropriate catamorphisms on demand. We also im-
plemented a CHC solver Catalia based on the proposed method, and evaluated
Catalia against the benchmark sets taken from CHC-COMP 2024 ADT-LIA
division. According to the evaluation results, Catalia outperformed the previ-
ous methods in solving SAT instances, indicating that Catalia is superior at
discovering invariants that the previous solvers failed to find.
    In future work, we plan to introduce more expressive catamorphism templates
than linear ones. As this may incur a cost in efficiency, an important direction is
to develop strategies for selectively applying different templates in the refinement
phase of Catalia.


Acknowledgments We would like to thank anonymous reviewers for use-
ful comments. This work was supported by JSPS KAKENHI Grant Numbers
JP23KJ0546 and JP20H05703.


References

 1. Alt, L., Blicha, M., Hyvärinen, A.E.J., Sharygina, N.: SolCMC: Solidity compiler’s
    model checker. In: Shoham, S., Vizel, Y. (eds.) Computer Aided Verification - 34th
    International Conference, CAV 2022, Haifa, Israel, August 7-10, 2022, Proceed-
    ings, Part I. Lecture Notes in Computer Science, vol. 13371, pp. 325–338. Springer
    (2022). https://doi.org/10.1007/978-3-031-13185-1_16
 2. Barbosa, H., Barrett, C.W., Brain, M., Kremer, G., Lachnitt, H., Mann, M., Mo-
    hamed, A., Mohamed, M., Niemetz, A., Nötzli, A., Ozdemir, A., Preiner, M.,
    Reynolds, A., Sheng, Y., Tinelli, C., Zohar, Y.: cvc5: A versatile and industrial-
    strength SMT solver. In: Fisman, D., Rosu, G. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems - 28th International Conference, TACAS
    2022, Held as Part of the European Joint Conferences on Theory and Practice
    of Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part
    I. Lecture Notes in Computer Science, vol. 13243, pp. 415–442. Springer (2022).
    https://doi.org/10.1007/978-3-030-99524-9_24
 3. Barrett, C., Fontaine, P., Tinelli, C.: The SMT-LIB Standard: Version 2.6. Tech.
    rep., Department of Computer Science, The University of Iowa (2017), available
    at www.SMT-LIB.org
                  Catamorphism Synthesis for Program Invariants over ADT             21

 4. Blicha, M., Fedyukovich, G., Hyvärinen, A.E.J., Sharygina, N.: Transition power
    abstractions for deep counterexample detection. In: Fisman, D., Rosu, G. (eds.)
    TACAS 2022, Part I. LNCS, vol. 13243, pp. 524–542. Springer (2022). https://doi.
    org/10.1007/978-3-030-99524-9_29
 5. Champion, A., Chiba, T., Kobayashi, N., Sato, R.: ICE-based refinement type
    discovery for higher-order functional programs. J. Autom. Reason. 64(7), 1393–
    1418 (2020). https://doi.org/10.1007/S10817-020-09571-Y
 6. Clarke, E.M., Grumberg, O., Jha, S., Lu, Y., Veith, H.: Counterexample-guided ab-
    straction refinement for symbolic model checking. J. ACM 50(5), 752–794 (2003).
    https://doi.org/10.1145/876638.876643
 7. De Angelis, E., Fioravanti, F., Pettorossi, A., Proietti, M.: Solving Horn clauses
    on inductive data types without induction. Theory Pract. Log. Program. 18(3-4),
    452–469 (2018). https://doi.org/10.1017/S1471068418000157
 8. De Angelis, E., Fioravanti, F., Pettorossi, A., Proietti, M.: Removing algebraic
    data types from constrained Horn clauses using difference predicates. In: Peltier,
    N., Sofronie-Stokkermans, V. (eds.) Automated Reasoning - 10th International
    Joint Conference, IJCAR 2020, Paris, France, July 1-4, 2020, Proceedings, Part
    I. Lecture Notes in Computer Science, vol. 12166, pp. 83–102. Springer (2020).
    https://doi.org/10.1007/978-3-030-51074-9_6
 9. De Angelis, E., Fioravanti, F., Pettorossi, A., Proietti, M.: Catamorphic abstrac-
    tions for constrained Horn clause satisfiability. Theory Pract. Log. Program. 25(1),
    64–91 (2025). https://doi.org/10.1017/S147106842400019X
10. Ernest, G., Morales, J.F.: CHC COMP 2024 report. https://chc-comp.github.io/
    2024/ (2024)
11. Ernest, G., Morales, J.F.: CHC COMP benchmarks. https://github.com/
    chc-comp/chc-comp24-benchmarks/tree/main/ADT-LIA (2024)
12. Fedyukovich, G., Rümmer, P.: Competition report: CHC-COMP-21. In: Hojjat,
    H., Kafle, B. (eds.) Proceedings 8th Workshop on Horn Clauses for Verification
    and Synthesis, HCVS@ETAPS 2021, Virtual, 28th March 2021. EPTCS, vol. 344,
    pp. 91–108 (2021). https://doi.org/10.4204/EPTCS.344.7
13. Gurfinkel, A., Kahsai, T., Komuravelli, A., Navas, J.A.: The SeaHorn verification
    framework. In: Kroening, D., Pasareanu, C.S. (eds.) Computer Aided Verification
    - 27th International Conference, CAV 2015, San Francisco, CA, USA, July 18-
    24, 2015, Proceedings, Part I. Lecture Notes in Computer Science, vol. 9206, pp.
    343–361. Springer (2015). https://doi.org/10.1007/978-3-319-21690-4_20
14. Hoder, K., Bjørner, N.: Generalized property directed reachability. In: Theory and
    Applications of Satisfiability Testing - SAT 2012 - 15th International Conference,
    Trento, Italy, June 17-20, 2012. Proceedings. pp. 157–171 (2012). https://doi.org/
    10.1007/978-3-642-31612-8_13
15. Hojjat, H., Rümmer, P.: The ELDARICA Horn solver. In: Proceedings of FMCAD
    2018. pp. 1–7. IEEE (2018). https://doi.org/10.23919/FMCAD.2018.8603013
16. K., H.G.V., Shoham, S., Gurfinkel, A.: Solving constrained Horn clauses modulo
    algebraic data types and recursive functions. Proc. ACM Program. Lang. 6(POPL),
    1–29 (2022). https://doi.org/10.1145/3498722
17. Kahsai, T., Rümmer, P., Sanchez, H., Schäf, M.: Jayhorn: A framework for verifying
    Java programs. In: Chaudhuri, S., Farzan, A. (eds.) Computer Aided Verification -
    28th International Conference, CAV 2016, Toronto, ON, Canada, July 17-23, 2016,
    Proceedings, Part I. Lecture Notes in Computer Science, vol. 9779, pp. 352–358.
    Springer (2016). https://doi.org/10.1007/978-3-319-41528-4_19
22      Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

18. Katsura, H., Kobayashi, N., Sakayori, K., Sato, R.: Mode-based reduction from
    validity checking of fixpoint logic formulas to test-friendly reachability problem. In:
    Kiselyov, O. (ed.) Programming Languages and Systems - 22nd Asian Symposium,
    APLAS 2024, Kyoto, Japan, October 22-24, 2024, Proceedings. Lecture Notes in
    Computer Science, vol. 15194, pp. 325–345. Springer (2024). https://doi.org/10.
    1007/978-981-97-8943-6_16
19. Katsura, H., Kobayashi, N., Sakayori, K., Sato, R.: Artifact: Automated cata-
    morphism synthesis for solving constrained horn clauses over algebraic data types
    (2025). https://doi.org/10.5281/zenodo.16220747
20. Kobayashi, N., Sekiyama, T., Sato, I., Unno, H.: Toward neural-network-guided
    program synthesis and verification. In: Dragoi, C., Mukherjee, S., Namjoshi, K.S.
    (eds.) Static Analysis - 28th International Symposium, SAS 2021, Chicago, IL,
    USA, October 17-19, 2021, Proceedings. Lecture Notes in Computer Science, vol.
    12913, pp. 236–260. Springer (2021). https://doi.org/10.1007/978-3-030-88806-0_
    12
21. Kobayashi, N., Wu, M.: Neural network-guided synthesis of recursive list func-
    tions. In: Sankaranarayanan, S., Sharygina, N. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems - 29th International Conference, TACAS
    2023, Held as Part of the European Joint Conferences on Theory and Practice
    of Software, ETAPS 2022, Paris, France, April 22-27, 2023, Proceedings, Part
    I. Lecture Notes in Computer Science, vol. 13993, pp. 227–245. Springer (2023).
    https://doi.org/10.1007/978-3-031-30823-9_12
22. Komuravelli, A., Gurfinkel, A., Chaki, S.: SMT-based model checking for recursive
    programs. Formal Methods in System Design 48(3), 175–205 (2016). https://doi.
    org/10.1007/s10703-016-0249-4
23. Kostyukov, Y., Mordvinov, D., Fedyukovich, G.: Beyond the elementary represen-
    tations of program invariants over algebraic data types. In: Freund, S.N., Yahav, E.
    (eds.) PLDI ’21: 42nd ACM SIGPLAN International Conference on Programming
    Language Design and Implementation, Virtual Event, Canada, June 20-25, 2021.
    pp. 451–465. ACM (2021). https://doi.org/10.1145/3453483.3454055
24. Leino, K.R.M.: Automating induction with an SMT solver. In: Kuncak, V., Ry-
    balchenko, A. (eds.) Verification, Model Checking, and Abstract Interpretation -
    13th International Conference, VMCAI 2012, Philadelphia, PA, USA, January 22-
    24, 2012. Proceedings. Lecture Notes in Computer Science, vol. 7148, pp. 315–331.
    Springer (2012). https://doi.org/10.1007/978-3-642-27940-9_21
25. Matsushita, Y., Tsukada, T., Kobayashi, N.: RustHorn: CHC-based verification for
    rust programs. In: Müller, P. (ed.) Programming Languages and Systems - 29th
    European Symposium on Programming, ESOP 2020, Held as Part of the Euro-
    pean Joint Conferences on Theory and Practice of Software, ETAPS 2020, Dublin,
    Ireland, April 25-30, 2020, Proceedings. Lecture Notes in Computer Science, vol.
    12075, pp. 484–514. Springer (2020). https://doi.org/10.1007/978-3-030-44914-8_
    18
26. Meijer, E., Fokkinga, M.M., Paterson, R.: Functional programming with bananas,
    lenses, envelopes and barbed wire. In: Hughes, J. (ed.) Functional Program-
    ming Languages and Computer Architecture, 5th ACM Conference, Cambridge,
    MA, USA, August 26-30, 1991, Proceedings. Lecture Notes in Computer Science,
    vol. 523, pp. 124–144. Springer (1991). https://doi.org/10.1007/3540543961_7
27. de Moura, L.M., Bjørner, N.S.: Z3: an efficient SMT solver. In: Ramakrishnan,
    C.R., Rehof, J. (eds.) Tools and Algorithms for the Construction and Analysis
    of Systems, 14th International Conference, TACAS 2008, Held as Part of the
                  Catamorphism Synthesis for Program Invariants over ADT            23

    Joint European Conferences on Theory and Practice of Software, ETAPS 2008,
    Budapest, Hungary, March 29-April 6, 2008. Proceedings. Lecture Notes in Com-
    puter Science, vol. 4963, pp. 337–340. Springer (2008). https://doi.org/10.1007/
    978-3-540-78800-3_24
28. Mukai, R., Kobayashi, N., Sato, R.: Parameterized recursive refinement types for
    automated program verification. In: Singh, G., Urban, C. (eds.) Static Analysis -
    29th International Symposium, SAS 2022, Auckland, New Zealand, December 5-7,
    2022, Proceedings. Lecture Notes in Computer Science, vol. 13790, pp. 397–421.
    Springer (2022). https://doi.org/10.1007/978-3-031-22308-2_18
29. Oppen, D.C.: Reasoning about recursively defined data structures. J. ACM 27(3),
    403–411 (1980). https://doi.org/10.1145/322203.322204
30. Pham, T., Gacek, A., Whalen, M.W.: Reasoning about algebraic data types with
    abstractions. J. Autom. Reason. 57(4), 281–318 (2016). https://doi.org/10.1007/
    S10817-016-9368-2
31. Reynolds, A., Deters, M., Kuncak, V., Tinelli, C., Barrett, C.: Counterexample-
    guided quantifier instantiation for synthesis in SMT. In: Computer Aided Verifi-
    cation: 27th International Conference, CAV 2015, San Francisco, CA, USA, July
    18-24, 2015, Proceedings, Part II 27. pp. 198–216. Springer (2015)
32. Reynolds, A., Kuncak, V.: Induction for SMT solvers. In: D’Souza, D., Lal, A.,
    Larsen, K.G. (eds.) Verification, Model Checking, and Abstract Interpretation -
    16th International Conference, VMCAI 2015, Mumbai, India, January 12-14, 2015.
    Proceedings. Lecture Notes in Computer Science, vol. 8931, pp. 80–98. Springer
    (2015). https://doi.org/10.1007/978-3-662-46081-8_5
33. Rümmer, P.: A constraint sequent calculus for first-order logic with linear integer
    arithmetic. In: Proceedings, 15th International Conference on Logic for Program-
    ming, Artificial Intelligence and Reasoning. LNCS, vol. 5330, pp. 274–289. Springer
    (2008)
34. Suter, P., Dotta, M., Kuncak, V.: Decision procedures for algebraic data types with
    abstractions. In: Hermenegildo, M.V., Palsberg, J. (eds.) Proceedings of the 37th
    ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
    POPL 2010, Madrid, Spain, January 17-23, 2010. pp. 199–210. ACM (2010). https:
    //doi.org/10.1145/1706299.1706325
35. Suter, P., Köksal, A.S., Kuncak, V.: Satisfiability modulo recursive programs.
    In: Yahav, E. (ed.) Static Analysis - 18th International Symposium, SAS 2011,
    Venice, Italy, September 14-16, 2011. Proceedings. Lecture Notes in Com-
    puter Science, vol. 6887, pp. 298–315. Springer (2011). https://doi.org/10.1007/
    978-3-642-23702-7_23
36. Yang, W., Fedyukovich, G., Gupta, A.: Lemma synthesis for automating induc-
    tion over algebraic data types. In: Principles and Practice of Constraint Program-
    ming: 25th International Conference, CP 2019, Stamford, CT, USA, September
    30–October 4, 2019, Proceedings 25. pp. 600–617. Springer (2019)
37. Zavalía, L., Chernigovskaia, L., Fedyukovich, G.: Solving constrained Horn clauses
    over algebraic data types. In: Dragoi, C., Emmi, M., Wang, J. (eds.) Verifi-
    cation, Model Checking, and Abstract Interpretation - 24th International Con-
    ference, VMCAI 2023, Boston, MA, USA, January 16-17, 2023, Proceedings.
    Lecture Notes in Computer Science, vol. 13881, pp. 341–365. Springer (2023).
    https://doi.org/10.1007/978-3-031-24950-1_16
38. Zhang, T., Sipma, H.B., Manna, Z.: Decision procedures for term algebras with
    integer constraints. Inf. Comput. 204(10), 1526–1574 (2006). https://doi.org/10.
    1016/J.IC.2006.03.004
24     Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

A    Proof of Soundness
This section proves the soundness of the abstraction (Theorem 1).

Setting and Notation: Throughout this section we fix an approximation degree
N and a catamorphism C : Hδ → ZN . We also fix S = {C1 , . . . Cn }, a system of
CHC over ADTs, and assume that M is a model of S. We suppose that for each
                    k               l
               z }| { z            }|   {
predicate P : δ × · · · × δ × int× → ×int → bool in the signature of ADT, there
exists a predicate P that takes N × k + l integers in the signature of arithmetic.
    Given a structure S, we write JP KS and Jf KS for the interpretation of the
predicate P and the function symbol f in S. The denotation of a term and
formula with respect to S and a valuation ρ are written as JtKS,ρ and JφKS,ρ (∈
{⊤, ⊥}), respectively; we may omit the subscripts if they are clear from the
context. As usual, we write S, ρ |= JφK if JφKS,ρ = ⊤, and S |= φ if S, ρ |= φ for
all ρ.                                                                          ⊔
                                                                                ⊓
   The proof of soundness is given by constructing a model of S from M, the
model of αC (S). For a function (which may be thought of as an interpretation of
an “abstracted predicate”)
                                     k          l
                          z   }|       { z    }|      {
                            N          N
                      f : Z × · · · × Z × Z × · · · × Z → {⊤, ⊥},

we define its concretization with respect to C by
                                         k                       l
                              z    }|       { z     }|      {
                    γC (f ) : Hδ × · · · × Hδ × Z × · · · × Z → {⊤, ⊥}
                                                   def
          γC (f )(t1 , . . . , tk , n1 , . . . , nl ) = f (C(t1 ), . . . , C(tk ), n1 , . . . , nl )

We often omit the subscript C since it is fixed throughout this section. Our goal
is to show that concretizing the interpretation of P gives a model of S.
Definition 1 (Concretization of a Model). We write γ(M) for the structure
over the signature for ADTs in which
 – the universes for δ and int are Hδ and Z, respectively,
 – the interpretation of P is given as γ(JP KM ),
 – the interpretation of =δ is given as the diagonal relation over Hδ , and
 – interpretation of function symbols is the same as that of M.
                                                                                                       ⊔
                                                                                                       ⊓
   Now we relate the interpretation of terms and formulas interpreted in M
and γ(M). To this end, we first prepare a relation over the valuations on M
and γ(M). Let Ξ be a variable abstraction environment. Given valuations ρ
and ζ over the (many-sorted) universes ⟨Hδ , Z⟩ and Z, respectively, we write
ρ ≈C,Ξ ζ if C(ρ(x)) = ζ(Ξ(x)) for all x ∈ dom(Ξ) and ρ(x) = ζ(x) otherwise;
here ζ(Ξ(x)) means (ζ(x1 ), . . . , ζ(xn )) for Ξ(x) = (x1 , . . . , xn ).
                      Catamorphism Synthesis for Program Invariants over ADT                          25

Lemma 2. Let Ξ be a variable abstraction environment and let t be a term
of sort δ such that FV(t) ⊆ dom(Ξ). If ρ ≈C,Ξ ζ, then we have C(JtKρ ) =
JαC,Ξ (t)Kζ .

Proof. By induction on the structure of t. The case t = x with x ∈ dom(Ξ)
holds because

                         C(JxKρ ) = C(ρ(x)) = ζ(Ξ(x)) = JαC,Ξ (x)Kζ

by the definition of ρ ≈C,Ξ ζ.
   We next show the case t = Ci (t1 , . . . , tmi , a1 , . . . , ani ). We have

              JαC,Ξ (Ci (t1 , . . . , tmi , a1 , . . . , ani ))Kζ
               = Fi (JαC,Ξ (t1 )Kζ , . . . , JαC,Ξ (tmi )Kζ , Ja1 Kζ , . . . , Jami Kζ )
               = Fi (C(Jt1 Kρ ), . . . , C(Jtmi Kρ ), Ja1 Kρ , . . . , Jami Kρ )               (by I.H.)
               = C(Ci (Jt1 Kρ , . . . , Jtmi Kρ , Ja1 Kρ , . . . , Jami Kρ ))              (by def. of C)
               = C(JtKρ )                                                              (by def. of JtK)

as desired.
   The other cases are trivial.                                                                        ⊔
                                                                                                       ⊓

Lemma 3. Suppose that ρ ≈C,Ξ ζ. Then we have:

                   t) if and only if M, ζ |= P i (α^
 1. γ(M), ρ |= Pi (e                               C,Ξ (t))
 2. if γ(M), ρ |= t1 =δ t2 , then M, ζ |= αC,Ξ (t1 ) =int N αC,Ξ (t2 )

                                                          t = t1 , . . . , tk , a1 , . . . , al ,
Proof. We only prove 1. since 2. is trivial. Suppose that e
where each ti has sort δ and ai is of sort int. Then we have

      JPi (e
           t)Kγ(M),ρ
       = γ(JPi KM )(Jt1 Kρ , . . . , Jtk Kρ , Ja1 Kρ , . . . , Jak K)
       = JPi KM (C(Jt1 Kρ ), . . . , C(Jtk Kρ ), Ja1 Kρ , . . . , Jak K)           (by the def. of γ)
       = JPi KM JαC,Ξ (t1 )Kζ ), . . . , JαC,Ξ (tk )Kζ ), JαC,Ξ (a1 )Kζ , . . . , JαC,Ξ (ak )Kζ )
                                                            (by Lemma2 and αC,Ξ (ai ) = ai )
       = JP i (α^
                C,Ξ (t))KM,ζ

                                                                                                       ⊔
                                                                                                       ⊓

Lemma 4. Let Ξ be a variable abstraction environment and assume that ρ ≈C,Ξ
ζ. Then γ(M), ζ |= θ implies M, ρ |= αC,Ξ (θ).

Proof. By straightforward induction on the structure of θ. The case for t1 =δ t2
follows from Lemma 3.                                                         ⊔
                                                                              ⊓

    We show that P δ (x1 , . . . , xN ), the abstraction of Pδ (x) represents the image
of C.
26         Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

Lemma 5. Let Peδ be the system of CHCs defining Pδ . Suppose that Mmin be
the minimum model of αC (Peδ ) Then, JP δ KMmin (n1 , . . . , nN ) = ⊤ if and only if
there exists t ∈ Hδ such that (n1 , . . . , nN ) = C(t).

Proof. Observe that for each constructor Ci , we have the following clause in
αC (Peδ ).

              ∀ye1 . . . yek x                              e)) ⇐= P δ (ye1 ) ∧ · · · ∧ P δ (yek )
                             e.P δ (Fi (ye1 , . . . , yek , x

where yei is a sequence of integer variables yi1 , . . . , yiN .
   One can easily check that the structure Mmin defined by
                                      (
                                        ⊤ if (n1 , . . . , nN ) = C(t) for some t
       JPδ KMmin (n1 , . . . , nN ) =
                                        ⊥ otherwise

is a model by checking the denotation of the each clause of αC (Peδ ).
    To check that this is indeed a minimum model, it suffices to show that for
every model M of αC (Peδ ) and every term t ∈ Hδ , we have JPδ KM (C(t)) = ⊤.
This is proved by induction on the size of t with a case analysis on the shape of
t. Suppose that t = Ci (t1 , . . . , tk , a1 , . . . , al ). Since M is a model of αC (Peδ ), we
have

                 M, ρ |= Pδ (Fi (ye1 , . . . , yek , x
                                                     e)) ⇐= Pδ (ye1 ) ∧ · · · ∧ Pδ (yek )

where ρ = [ye1 7→ C(t1 ), . . . yek 7→ C(tk ), x          ^
                                                    e 7→ JaK M ]. We have JPδ KM (C(ti ))
= ⊤ for i ∈ {1, . . . , k} by the induction hypothesis, which implies M, ρ |=
                            e)). From this and C(t) = Fi (C(t1 ), . . . , C(tk ), Ja1 K, . . . , Jal K),
Pδ (Fi (ye1 , . . . , yek , x
we must have JPδ KM (C(t)) = ⊤.                                                                       ⊔
                                                                                                      ⊓

      Finally, we show that γ(M) is indeed a model.
Theorem 2. The structure γ(M) is a model of S = {C1 , . . . , Cn }.

Proof. It suffices to prove that γ(M) |= Ci for every i. Suppose that Ci is of the
form

             ∀xδ1 . . . xδp y1int . . . yqint .Pi0 (tf
                                                     i0 ) ⇐= θ ∧ Pi1 (tf
                                                                       i1 ) ∧ · · · ∧ Pir (tf
                                                                                            ir ).

Here we have assumed that the head of the clause is a predicate application, but
the case where the head is false can be proved in similar manner. The clause
αC (Ci ) is then of the form6

 ∀f                                 ^
           fp , y1 . . . yq .P i0 (αC,Ξ
  x1 . . . x                            (ti0 )) ⇐= αC,Ξ (θ) ∧ φadm
                                                                 ^
                                                        ∧ P i1 (αC,Ξ                          ^
                                                                     (ti1 )) ∧ · · · ∧ P ir (αC,Ξ (tir ))
                                                                        def
                                                                        x1 ) ∧ · · · ∧ P δ (f
                                                      where φadm = P δ (f                   xp ).
6
     In this proof universal quantifiers are explicitly written.
                      Catamorphism Synthesis for Program Invariants over ADT                            27


                            Table 2: Tools used in the evaluation
                                  Tool     Version
                                  Z3       4.12.2
                                  Spacer Z3 version 4.12.2
                                  Eldarica v2.1
                                  HoIce    1.10.0
                                  Vampire 4.6.1 (Z3: 4.8.13.0)


Here xei = xi1 , . . . , xiN and Ξ = [x1 7→ x      f1 , . . . , xp 7→ x
                                                                      fp ].
   Our goal is to show γ(M), ρ |= Pi0 (tf           i0 ) ⇐= θ ∧ Pi1 (tf   i1 ) ∧ · · · ∧ Pir (tf
                                                                                               ir ) for all
valuation ρ. Let t1 , . . . , tp ∈ Hδ , n1 , . . . , nq and
                      def
                   ρ = [x1 7→ t1 , . . . , xp 7→ tp , y1 7→ n1 , . . . , yq 7→ nq ].

Let ζ be a valuation defined by
             def
           ζ = [Ξ(x1 ) 7→ C(t1 ), . . . , Ξ(xp ), 7→ C(tp ), y1 7→ n1 , . . . , yq 7→ nq ]

Clearly, we have ρ ≈C,Ξ ζ. By the assumption that M is a model of αC (S), we
have M |= αC (Ci ). In particular, we have

               ^
M, ζ |= P i0 (αC,Ξ                              ^
                   (ti0 )) ⇐= αC,Ξ (θ) ∧ P i1 (αC,Ξ                          ^
                                                    (ti1 )) ∧ · · · ∧ P ir (αC,Ξ (tir )) ∧ φadm

Thanks to Lemma 5, we also know that M, ζ |= φadm . From this, it follows that

                   ^
    M, ζ |= P i0 (αC,Ξ                              ^
                       (ti0 )) ⇐= αC,Ξ (θ) ∧ P i1 (αC,Ξ                          ^
                                                        (ti1 )) ∧ · · · ∧ P ir (αC,Ξ (tir ))

Applying Lemma 3 and 4 to the above satisfaction relation, we get

                   γ(M), ρ |= Pi0 (tf
                                    i0 ) ⇐= θ ∧ Pi1 (tf
                                                      i1 ) ∧ · · · ∧ Pir (tf
                                                                           ir )

as desired.                                                                                             ⊔
                                                                                                        ⊓


B      Additional Material for Evaluation
We listed the versions of the tools used in our evaluation in Table 2. We used
the following option for z3 to use Spacer:
 – fp.xform.tail_simplifier_pve=false
 – fp.validate=true
 – fp.spacer.mbqi=false
 – fp.spacer.use_iuc=true
 – fp.spacer.global=true
 – fp.spacer.expand_bnd=true
 – fp.spacer.q3.use_qgen=true
28     Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato

 – fp.spacer.q3.instantiate=true
 – fp.spacer.q3=true
 – fp.spacer.ground_pobs=false
which can be found in the competition report for CHC COMP 2021 [12]. We en-
abled -portfolio option for Eldarica, -t –no-isolation –solver vampire
option for RInGen. We utilized the default options for the other tools.
