                                         Under consideration for publication in Theory and Practice of Logic Programming                 1




                                             Solving Horn Clauses on Inductive Data Types
                                                          Without Induction
arXiv:1804.09007v1 [cs.LO] 24 Apr 2018




                                                           EMANUELE DE ANGELIS,                FABIO FIORAVANTI
                                                          DEC, ‘G. d’Annunzio’ University of Chieti-Pescara, Pescara, Italy
                                                           (e-mail: {emanuele.deangelis, fabio.fioravanti}@unich.it)

                                                                           ALBERTO PETTOROSSI
                                                                DICII, University of Rome Tor Vergata, Rome, Italy
                                                                      (e-mail: pettorossi@info.uniroma2.it)

                                                                            MAURIZIO PROIETTI
                                                                               CNR-IASI, Rome, Italy
                                                                     (e-mail: maurizio.proietti@iasi.cnr.it)

                                                     submitted 1 January 2003; revised 1 January 2003; accepted 1 January 2003



                                                                                    Abstract
                                         We address the problem of verifying the satisfiability of Constrained Horn Clauses (CHCs)
                                         based on theories of inductively defined data structures, such as lists and trees. We propose a
                                         transformation technique whose objective is the removal of these data structures from CHCs,
                                         hence reducing their satisfiability to a satisfiability problem for CHCs on integers and booleans.
                                         We propose a transformation algorithm and identify a class of clauses where it always succeeds.
                                         We also consider an extension of that algorithm, which combines clause transformation with
                                         reasoning on integer constraints. Via an experimental evaluation we show that our technique
                                         greatly improves the effectiveness of applying the Z3 solver to CHCs. We also show that our
                                         verification technique based on CHC transformation followed by CHC solving, is competitive
                                         with respect to CHC solvers extended with induction.
                                         This paper is under consideration for acceptance in TPLP.
                                         KEYWORDS: Program verification, constrained Horn clauses, constraint logic programming,
                                         inductively defined data types, program transformation.




                                                                                1 Introduction
                                         Constraint logic programs have become a well-established formalism for solving program
                                         verification problems (Albert et al. 2007, Bjørner et al. 2015, De Angelis et al. 2014, Jaf-
                                         far et al. 2012, Méndez-Lojo et al. 2008, Peralta et al. 1998). In the verification field,
                                         constraint logic programs are often called constrained Horn clauses (CHCs), and here
                                         we will adopt this terminology. The verification method based on CHCs consists in re-
                                         ducing a program verification problem to the satisfiability of a set of CHCs. Since CHC
                                         satisfiability, also called CHC solving, is in general an undecidable problem, some heuris-
                                         tics have been proposed in the literature, such as Counterexample Guided Abstraction
                                         Refinement (CEGAR) (Clarke et al. 2000), Craig interpolation (McMillan 2003), and
                                         Property Directed Reachability (PDR) (Bradley 2011, Hoder and Bjørner 2012). Some
2               E. De Angelis, F. Fioravanti, A. Pettorossi, M. Proietti

tools, called CHC solvers, for verifying the satisfiability of CHCs are available. We recall
Eldarica (Hojjat et al. 2012), HSF (Grebenshchikov et al. 2012), RAHFT (Kafle et al.
2016), VeriMAP (De Angelis et al. 2014), and Z3 (de Moura and Bjørner 2008). CHC
solvers make use of a combination of the above heuristics and have been shown to be
very effective for CHCs with several underlying constraint theories, such as the theory
of Linear Integer Arithmetic (LIA) and the theory of Boolean constraints (Bool).
   Solving techniques have also been developed for CHCs manipulating inductively de-
fined data structures such as lists and trees (see, for instance, https://rise4fun.com/Z3/
tutorial/guide for the Z3 solver). However, CHC solvers acting on those data structures
are usually less effective than CHC solvers for clauses with constraints in LIA or Bool.
This is mainly due to the fact that methods for satisfiability used by CHC solvers are
based on variants of resolution, augmented with ad hoc algorithms for the underlying
constraint theory, and no induction principles for the data structures are used.
   To overcome this difficulty, recent work has proposed the extension of CHC solving by
adding a principle of induction on predicate derivations (Unno et al. 2017). This work
is on the same line of other proposals which extend techniques for Satisfiability Modulo
Theory (SMT) with inductive reasoning (Reynolds and Kuncak 2015, Suter et al. 2011)
by incorporating methods derived from the field of automated theorem proving.
   In this paper we propose an alternative method to solve CHCs on inductively de-
fined data structures. It is based on the application of suitable transformations of CHCs
that have the objective of removing those data structures while preserving satisfiabil-
ity of clauses. Our transformation method makes use of the fold/unfold transformation
rules (Etalle and Gabbrielli 1996, Tamaki and Sato 1984), and it is based on some tech-
niques proposed in the past for improving the efficiency of functional and logic programs,
such as deforestation (Wadler 1990), unnecessary variable elimination (Proietti and Pet-
torossi 1995), and conjunctive partial deduction (De Schreye et al. 1999). However, the
focus of the method presented in this paper is on the improvement of effectiveness of
CHC solvers, rather than the improvement of efficiency of programs.
   In our method we separate the concern of reasoning on inductively defined data struc-
tures from the concern of proving clause satisfiability. This separation of concerns eases
the task of the CHC solvers in many cases. For instance, when the constraints are on trees
of integers, our transformation method, if successful, allows us to derive an equisatisfiable
set of clauses with constraints on integers only.
   The main contributions of our work are the following. (1) We propose a transformation
algorithm, called E, that removes inductively defined data structures from CHCs and
derives new, equisatisfiable sets of clauses whose constraints are from the LIA theory and
the Bool theory (see Section 4). (2) We identify a class of CHCs where Algorithm E is
guaranteed to terminate, and all inductively defined data structures can be removed (see
Section 5). (3) By using reasoning techniques on LIA constraints, we derive an extension
of our transformation algorithm E, called Algorithm EC (see Section 6). (4) We report
on an experimental evaluation of a tool that implements Algorithm EC. We consider
CHCs that encode properties of OCaml functional programs, and we show that our tool
is competitive with the RCaml tool that extends the Z3 solver by adding induction rules
for reasoning on inductive data structures (Unno et al. 2017) (see Section 7).
           Solving Horn Clauses on Inductive Data Types Without Induction                      3

                             2 A Tree Processing Example
As an introductory example to illustrate our technique for proving program properties
without using induction on data structures, let us consider the following Tree-Processing
program, which we write according to the OCaml syntax (Leroy et al. 2017).
type tree = Leaf | Node of int ∗ tree ∗ tree ;;
let min x y = if x < y then x else y ;;
let rec min -leaf t = match t with
                   | Leaf –> 0
                   | Node(x, l, r) –> 1 + min (min-leaf l) (min-leaf r) ;;
let rec left -drop n t = match t with
                   | Leaf –> Leaf
                   | Node(x, l, r) –> if n <= 0 then Node(x, l, r) else left-drop (n−1) l ;;
Let us also consider the following non-trivial property Prop to be verified for the Tree-
Processing program:
                                                                  
   ∀n ∀t. n ≥ 0 ⇒ ((min-leaf (left-drop n t)) + n) ≥ (min-leaf t) .
Now we translate the Tree-Processing program and the property Prop into a set of CHCs
that are satisfiable iff Prop holds for Tree-Processing. We get the following set of clauses
(clauses 1–7 for the program and clause 8 for the property):
1. min(X, Y, Z) ← X < Y, Z = X
2. min(X, Y, Z) ← X ≥ Y, Z = Y
3. min-leaf (leaf , M ) ← M = 0
4. min-leaf (node(X, L, R), M ) ← M = M 3+1, min-leaf (L, M 1), min-leaf (R, M 2),
                          min(M 1, M 2, M 3)
5. left-drop(N, leaf , leaf ) ←
6. left-drop(N, node(X, L, R), node(X, L, R)) ← N ≤ 0
7. left-drop(N, node(X, L, R), T ) ← N ≥ 1, N 1 = N −1, left-drop(N 1, L, T )
8. false ← N ≥ 0, M +N < K, left-drop(N, T, U ), min-leaf (U, M ), min-leaf (T, K)
   In clause 8 the head is false because the relation ‘<’ in the constraint M +N < K
occurring in the body is the negation of the relation ‘≥’ occurring in the property Prop.
   The Z3 solver is not able to prove the satisfiability of clauses 1–8 (which amounts to
show that false is not derivable), because of the presence of variables of type tree. One
can extend the capabilities of Z3 by adding induction rules on trees as done in recent
work (Reynolds and Kuncak 2015, Suter et al. 2011, Unno et al. 2017). Instead, as we
propose in this paper, we can derive by transformation, starting from clauses 1–8, a new,
equisatisfiable set of clauses without variables of type tree and whose constraints are in
LIA only, and then we can use CHC solvers, such as Z3, to show the satisfiability of
this new set of clauses. Starting from clauses 1–8, our transformation algorithm, whose
details are given in Section 4, produces the following clauses, where min is defined by
clauses 1 and 2:
 9. new1(N, M, K) ← M = 0, K = 0
10. new1(N, M, K) ← N ≤ 0, M = M 3+1, K = M, new2(M 1), new2(M 2),
                    min(M 1, M 2, M 3)
11. new1(N,M,K) ← N ≥ 1, N 1 = N −1, K = K3+1, new1(N 1,M,K1), new2(K2),
                    min(K1,K2,K3)
4                  E. De Angelis, F. Fioravanti, A. Pettorossi, M. Proietti

12. new2(M ) ← M = 0
13. new2(M ) ← M = M 3+1, new2(M 1), new2(M 2), min(M 1, M 2, M 3)
14. false ← N ≥ 0, M +N < K, new1(N, M, K)
Now, the Z3 solver for CHCs with LIA constraints is able to prove the satisfiability of
clauses 1, 2, 9–14 without using any induction on trees. The details of the transformation
from clauses 1–8 to clauses 1, 2, 9–14 will be presented in Section 4.


                                           3 Preliminaries
Let us consider a typed, first order functional language. We assume that the basic types
of the language are int, for integers, and bool, for booleans. We also have non-basic types,
which are introduced by (possibly recursive) type definitions such as the one for trees of
integers considered in Section 2. The type system of our language can be formally defined
as follows. (One may consider richer type systems including, for instance, parameterized
types, but this system is sufficient for presenting our verification technique.)
    Types 3 τ ::= int | bool | ident | τ1 ∗ . . . ∗ τk
    Type Definitions : ident = c1 of τ1 | . . . | cn of τn
where: (i) ident is a type identifier, (ii) the operator ‘∗’ builds k-tuple types, (iii) c1 , . . . , cn
are distinct constructors with arity, and (iv) in any expression ‘ci of τi ’, if ci has ar-
ity k > 0, then τi is a k-tuple type, and if ci has arity 0, then ‘of τi ’ is absent.
   Every function has a functional type of the form τ1 → τ2 , for some types τ1 and τ2 ,
modulo the usual isomorphism between τ → (τ 0 → τ 00 ) and (τ ∗ τ 0 ) → τ 00 .
   In the following definitions: (i) n is an integer, (ii) b is true or false, (iii) x is a typed
variable, (iv) c is a constructor of arity k (≥ 0), and (v) f is a function of arity k (≥ 0)
or a primitive operator on integers or booleans such as: +, ×, =, 6=, ≤, ¬, ∧, and ⇒.
    Values 3 v ::= n | b | c v1 . . . vk
    Terms 3 t ::= n | b | x | c t1 . . . tk | f t1 . . . tk | if t0 then t1 else t2
                 | let x = t0 in t1 | match x with | p1 –> t1 | . . . | pn –> tn
    Patterns 3 p ::= c (x1 , . . . , xk )
We assume that all values, terms, and patterns are well-typed. In every let-in term x
is a new variable not occurring in t0 and occurring in t1 . In every match-with term
the patterns p1 , . . . , pk are pairwise disjoint and exhaustive. A user-defined function f is
defined by: let rec f x1 . . . xk = t, where the free variables of t are among {x1 , . . . , xk }.
   A program is a (possibly empty) set of type definitions together with a set of user-defined
functions. Given a program P and a term t without free variables and whose functions
are defined in P , the value v of t using P is computed according to the call-by-value se-
mantics. In this case we write t →P v. We say that a program P terminates if, for every
term t without free variables and whose functions are defined in P , there exists a value v
such that t →P v. Given a boolean term q whose free variables are in {x1 , . . . , xn }, a prop-
erty is a universally quantified formula of the form ∀x1 , . . . , xn . q. Given a program P ,
we say that a property ∀x1 , . . . , xn . q, whose functions are defined in P , holds for P iff
for all values v1 , . . . , vn , we have that q [v1 , . . . , vn / x1 , . . . , xn ] →P true, where the square
bracket notation is for substitution.
   Let us consider a typed first order logic (Enderton 1972) which includes: (i) the theory
             Solving Horn Clauses on Inductive Data Types Without Induction                              5

LIA of the linear integer arithmetic constraints, and (ii) the theory Bool of boolean
constraints. A constraint in LIA ∪ Bool is any formula in LIA ∪ Bool.
   An atom is a formula of the form q(t1 , . . . , tm ), where q is a typed predicate symbol not
used in LIA∪Bool, and t1 , . . . , tm are typed terms made out of variables and constructors.
A constrained Horn clause (or simply, a clause, or a CHC) is an implication of the form
A ← c, B (comma denotes conjunction), where the conclusion (or head) A is either an
atom or false, the premise (or body) is the conjunction of a constraint c, and a (possibly
empty) conjunction B of atoms. A clause whose head is an atom is called a definite
clause, and a clause whose head is false is called a goal. A constrained fact is a clause of
the form A ← c. We will write the constrained fact A ← true also as A ←. We assume
that all variables in a clause are universally quantified in front. Given a term t, by vars(t)
we denote the set of variables occurring in t. Similarly for the set of variables occurring
in atoms, or clauses, or sets of atoms, or sets of clauses. A set S of CHCs is said to be
satisfiable if S ∪ LIA ∪ Bool has a model, or equivalently, S ∪ LIA ∪ Bool 6|= false.
   We define a translation Tr from any set P of function definitions into a set of CHCs by:
(i) introducing for each function f of arity k, a new predicate, say p, of arity k+1, and then
(ii) providing the clauses for predicate p so that f (x1 , . . . , xk )=y iff p(x1 , . . . , xk , y) holds.
This translation has been applied in Section 2 for generating clauses 1–7 starting from
the Tree-Processing program. Primitive operations, such as + and −, are translated in
terms of constraints expressed in LIA. Similarly, a property of the form: ∀x. r(x) ⇒ s(x)
is translated into a goal (or a set of goals, in general) as indicated in Section 2 (see
goal 8). If we denote by Tr(P ) and Tr(Prop) the set of CHCs generated from a given
program P and a given property Prop, respectively, we have the following theorem, where
satisfiability is defined within the typed logic we consider.

Theorem 1
Given a program P that terminates, a property Prop holds for P iff the set Tr(P ) ∪
Tr(Prop) of clauses is satisfiable.


                 4 Eliminating Inductively Defined Data Structures
Now we present an algorithm, called Algorithm E, for eliminating from CHCs the predi-
cate arguments that have a non-basic type, such as lists or trees. If Algorithm E termi-
nates, then it transforms a set of clauses into an equisatisfiable set, where the arguments
of all predicates have basic types. The algorithm is based on the fold/unfold strategy for
eliminating unnecessary variables from logic programs (Proietti and Pettorossi 1995).
   Given two terms t1 and t2 , by t1  t2 and t1 ≺ t2 we denote the subterm and strict
subterm relation, respectively. Given an atom A, by nbargs(A) we denote the set of
arguments of non-basic type of A. By nbvars(A) we denote the set of variables of non-basic
type occurring in A. The next definition extends the  and ≺ relations to atoms.

Definition 1 (Atom Comparison)
Given two atoms A1 and A2 , A1  A2 (or A1 ≺ A2 ) holds if there exist t1 ∈ nbargs(A1 )
and t2 ∈nbargs(A2 ) such that: (i) vars(t1 ) ∩ vars(t2 )6= ∅, and (ii) t1 t2 (or t1 ≺t2 ). Given
a set S of atoms, an atom M ∈ S is strictly maximal in S if there exists no atom A ∈ S
such that M ≺ A and there exists an atom A0 ∈ S such that A0 ≺ M .
6                E. De Angelis, F. Fioravanti, A. Pettorossi, M. Proietti

  For example, q([Y |Y s], [ ]) is strictly maximal in the set {p([X], Ys), q([Y |Ys], [ ])}.
Indeed, Ys ≺ [Y |Ys], and hence p([X], Ys) ≺ q([Y |Ys], [ ]), while q([Y |Ys], [ ]) 6≺ p([X], Ys)
(note that [ ] ≺ [X], but vars([ ])∩vars([X]) = ∅). The notion of a strictly maximal atom
will be used in the Unfold procedure of Algorithm E to guide the unfolding process.
  A predicate has basic types if all its arguments have basic type. An atom has basic
types if its predicate has basic types. A clause has basic types if all its atoms have basic
types.
Definition 2 (Sharing Blocks)
Let S be a set (or a conjunction) of atoms. For any two atoms A1 and A2 in S, A1 ↓ A2
holds iff nbvars(A1 ) ∩ nbvars(A2 ) 6= ∅. Let ⇓ be the reflexive transitive closure of ↓. By
SharingBlocks(S) we denote the partition of S into subsets, called sharing blocks, with
respect to ⇓.
  Algorithm E makes use of the well-known transformation rules define, fold, unfold, and
replace for CHCs (Etalle and Gabbrielli 1996, Tamaki and Sato 1984).

The Elimination Algorithm E.
Input: A set Cls ∪ Gs, where Cls is a set of definite clauses and Gs is a set of goals;
Output: A set TransfCls of clauses such that: (1) Cls ∪ Gs is satisfiable iff TransfCls is
satisfiable, and (2) every clause in TransfCls has basic types.

Defs := ∅; InCls := Gs; TransfCls := ∅;
while InCls 6= ∅ do
  Define-Fold(Defs, InCls, NewDefs, FldCls);
  Unfold(NewDefs, Cls, UnfCls);
  Replace(UnfCls, Cls, RCls);
  Defs := Defs ∪ NewDefs; InCls := RCls; TransfCls := TransfCls ∪ FldCls;

Starting from a set Cls of definite clauses and a set Gs of goals, Algorithm E applies
iteratively the procedures Define-Fold, Unfold, and Replace, in this order, until it derives
a set TransfCls of clauses whose predicates have basic types only. Algorithm E collects in
Defs the clauses, called definitions, introduced by the Define steps, and collects in InCls
the clauses to be transformed. The set Defs of definitions is initialized to the empty set
and the set InCls of the input goals is initialized to the set Gs of goals.
   Now let us present the various procedures used by Algorithm E.

Procedure Define-Fold(Defs, InCls, NewDefs, FldCls)
Input: A set Defs of definitions and a set InCls of clauses;
Output: A set NewDefs of definitions and a set FldCls of clauses.
NewDefs := ∅; FldCls := ∅;
for each clause C: H ← c, B in InCls do
   if C is a constrained fact then FldCls := FldCls ∪ {C} else
      Define. Let SharingBlocks(B) = {B1 , . . . , Bn };
         for i = 1, . . . , n do
         if there is no clause in Defs ∪ NewDefs whose body is Bi (modulo the names of
         variables and the order and multiplicity of the atoms) then
            Solving Horn Clauses on Inductive Data Types Without Induction                     7

         NewDefs := NewDefs ∪ {newpi (Vi ) ← Bi }
         where: (i) newpi is a new predicate symbol, and (ii) Vi is the tuple of distinct
         variables of basic type occurring in Bi ;
      Fold. C is folded using the definitions in Defs ∪ NewDefs, thereby deriving
         F : H ← c, newp1 (V1 ), . . . , newpn (Vn )
         where, for i = 1, . . . , n, newpi (Vi ) ← Bi is the unique clause in Defs ∪ NewDefs
         whose body is Bi , modulo variable renaming;
         FldCls := FldCls ∪ {F };

   The Define-Fold procedure removes the arguments with non-basic types from each
clause C of InCls in two steps: first, the Define step introduces a new predicate definition
for each sharing block of the body of C (unless a definition with a body equal, modulo
variable renaming, to that block has already been introduced in a previous Define step),
and then, the Fold step replaces each sharing block by the head of the new definition.
Since the heads of these new definitions have basic types, the body of the clause of the
form: H ← c, newp1 (V1 ), . . . , newpn (Vn ), derived from C by the Fold step, has basic types.
Also H has basic types, because: (i) Algorithm E initializes InCls to the set Gs of goals,
whose heads are false, and (ii) the head predicate of each new clause added to InCls has
been introduced by a previous Define step, and hence, by construction, has basic types.

Example 1
(Tree-Processing). Let us consider the introductory example of Section 2. At the first
iteration of the while-do body of Algorithm E, InCls consists of clause 8, which is the
result of translating the property Prop to be verified. The Define step introduces the new
predicate new1 through the following definition:
15. new1(N, M, K) ← left-drop(N, T, U ), min-leaf (U, M ), min-leaf (T, K)
The body of this clause consists of the single sharing block of the body of clause 8
(note that left-drop(N, T, U ) shares the tree variables T and U with min-leaf (T, K) and
min-leaf (U, M ), respectively). Now, the Fold step derives clause 14 of Section 2, where all
predicates have arguments of integer type, and thus it is added to the final set TransfCls.

  The Define step adds to Defs a set NewDefs of new definitions, whose body may have
predicates with non-basic types (see clause 15). Now, Algorithm E proceeds by applying
the Unfold procedure to those clauses.

Procedure Unfold(NewDefs, Cls, UnfCls)
Input: A set NewDefs of definitions and a set Cls of definite clauses;
Output: A set UnfCls of clauses.
UnfCls := NewDefs;
Initially, all atoms in the body of the clauses of UnfCls are marked ‘unfoldable’;
while there exists a clause C in UnfCls of the form H ← c, L, A, R such that either
(i) the atom A is ‘unfoldable’ and is strictly maximal in L, A, R, or
(ii) all atoms in L, A, R are ‘unfoldable’ and not strictly maximal do
    Let K1 ← c1 , B1 , . . . , Km ← cm , Bm be all clauses of Cls (where, without loss of gen-
    erality, we assume vars(Cls) ∩ vars(C) = ∅) such that, for i = 1, . . . , m, (1) there exists
    a most general unifier ϑi of A and Ki , and (2) the constraint (c, ci )ϑi is satisfiable;
8                 E. De Angelis, F. Fioravanti, A. Pettorossi, M. Proietti

    UnfCls := (UnfCls − {C}) ∪ {(H ← c, c1 , L, B1 , R)ϑ1 , . . . , (H ← c, cm , L, Bm , R)ϑm }
    where, for i = 1, . . . , m, (1) an atom Eϑi of (L, R)ϑi is ‘unfoldable’ iff the corresponding
    atom E of (L, R) is ‘unfoldable’ in C, and (2) no atom in Bϑi is ‘unfoldable’;


   The Unfold procedure unfolds the atoms occurring in NewDefs by performing resolu-
tion steps with clauses in Cls. The procedure applies a strategy that consists in unfolding
strictly maximal atoms, if any. In the case where the predicates are defined by induction
on the structure of their arguments with non-basic types, this strategy corresponds to a
form of induction on the arguments structure. The subsequent folding steps correspond
to applications of the inductive hypotheses. A characterization of a class of CHCs where
this strategy is successful will be given in Section 5. The use of the ‘unfoldable’ marking
on atoms enforces a finite number of resolution steps.
   Note that when Case (ii) of the condition of the while-do holds, the Unfold procedure
may unfold any ‘unfoldable’ atom (and in our implementation of the procedure we unfold
the leftmost one). However, in the class of CHCs presented in Section 5, the termination
of Algorithm E is independent of the choice of the atom to be unfolded.

Example 2
(Tree-Processing, continued). Let us continue the derivation presented in Example 1. All
atoms in the body of clause 15 are ‘unfoldable’ and none is strictly maximal (indeed,
no tree argument is a strict superterm of another). In this case the Unfold procedure
may unfold any ‘unfoldable’ atom, and we assume that it unfolds left-drop(N, T, U ). The
following three clauses, where we have underlined the ‘unfoldable’ atoms, are derived:
16. new1(N, M, K) ← min-leaf (leaf , M ), min-leaf (leaf , K)
17. new1(N, M, K) ← N ≤ 0, min-leaf (node(X, L, R), M ), min-leaf (node(X, L, R), K)
18. new1(N, M, K) ← N ≥ 1, N 1 = N −1, left-drop(N 1, L, U ), min-leaf (U, M ),
              min-leaf (node(X, L, R), K)
Now the Unfold procedure continues by selecting more atoms for unfolding. For instance,
in clause 18 it selects min-leaf (node(X, L, R), K), which is strictly maximal because the
argument L of left-drop(N 1, L, U ) is a strict subterm of node(X, L, R) and no atom in
the body of clause 18 has an argument that is a strict superterm of node(X, L, R). Af-
ter five iterations, where all underlined atoms, except min-leaf (U, M ), are unfolded, the
Unfold procedure derives the following clauses:
19. new1(N, M, K) ← M = 0, K = 0
20. new1(N, M, K) ← N ≤0, M =M 3+1, K =K3+1, min-leaf (L, M 1), min-leaf (R, M 2),
           min(M 1, M 2, M 3), min-leaf (L, K1), min-leaf (R, K2), min(K1, K2, K3)
21. new1(N, M, K) ← N ≥1, N 1=N −1 K =K3+1, left-drop(N 1, L, U ), min-leaf (U, M ),
           min-leaf (L, K1), min-leaf (R, K2), min(K1, K2, K3)
In clause 21, min-leaf (U, M ) is an ‘unfoldable’ atom, but the Unfold procedure stops
because that atom is not strictly maximal. Clause 19 is a constrained fact and it is added
to the final set TransfCls (indeed, clause 19 is clause 9 of Section 2).

   After the Unfold procedure Algorithm E may simplify some clauses by exploiting func-
tional dependencies among predicate arguments, which hold by construction for the pred-
icates obtained by translating functional programs.
           Solving Horn Clauses on Inductive Data Types Without Induction                    9

Definition 3 (Predicate Functionality)
Let Cls be a set of definite clauses. A predicate p(X, Y ), where X and Y are tuples of
arguments, is functional in Cls if Cls ∪ {false ← Y 6= Z, p(X, Y ), p(X, Z)} is a satisfiable
set of clauses.


Procedure Replace(UnfCls, Cls, RCls)
Input: A set UnfCls of clauses and a set Cls of definite clauses;
Output: A set RCls of clauses.
RCls := UnfCls;
while there is a clause C ∈ RCls of the form: H ← c, G1 , p(t, u), G2 , p(t, w), G3 , where
predicate p(X, Y ) is functional in Cls do
  Replace C by (H ← c, G1 , p(t, u), G2 , G3 )ϑ, where ϑ is a most general unifier of u and w;

Example 3
(Tree-Processing, continued). By the functionality of the predicates min-leaf (T, M ) and
min(X, Y, Z), clause 20 is replaced by the following one:
22. new1(N,M,K) ← N≤ 0, M=M 3+1, K=M, min-leaf(L,M 1), min-leaf(R,M 2),
                  min(M 1,M 2,M 3)
Now, Algorithm E performs a second iteration by executing again the Define-Fold, Unfold,
and Replace procedures. The Define step introduces the following definition:
23. new2(M 1) ← min-leaf (L, M 1)
whose body consists of a sharing block in the body of clause 22 (note that the tree
variable L is not shared with any other atom). No other definitions are introduced, as
all other sharing blocks in the clauses currently in InCls (namely, clauses 19, 21, and 22)
are variants of the body of the definitions 15 and 23. The Fold step derives clauses 10
and 11 of Section 2 from clauses 22 and 21, respectively.
   Finally, Algorithm E performs an Unfold step followed by a Fold step on clause 23 and
derives clauses 12 and 13 of Section 2. Note that Replace steps are not applicable, and
no new definitions are introduced by the Define step. Thus, Algorithm E terminates and
returns clauses 1, 2, 9–14 of Section 2.


             5 Correctness and Termination of the Transformation
The partial correctness of Algorithm E follows from well-known satisfiability preservation
results that hold for the fold/unfold transformation rules (Etalle and Gabbrielli 1996,
Tamaki and Sato 1984) (see the Appendix for a proof).
Theorem 2 (Partial Correctness)
Let Cls be a set of definite clauses and let Gs be a set of goals. If Algorithm E terminates
for the input clauses Cls ∪ Gs, returning a set TransfCls of clauses, then (1) Cls ∪ Gs is
satisfiable iff TransfCls is satisfiable, and (2) all clauses in TransfCls have basic types.
  Now we introduce a class of CHCs where Algorithm E is guaranteed to terminate.
  First we need the following terminology and notation. An atom is said to be linear if
each variable occurs in it at most once. By arity(p) we denote the arity of predicate symbol p.
10                  E. De Angelis, F. Fioravanti, A. Pettorossi, M. Proietti

Definition 4 (Slice Decomposition)
Let C be a clause of the form A0 ← c, A1 , . . . , Am , and let Pred be the set of predicate
symbols in the atoms A0 , A1 , . . . , Am of C. A slice of C is a total function σ : Pred → N
such that, for every predicate p∈Pred: (1) 0≤σ(p)≤arity(p), and (2) if σ(p)=i>0, then
the i-th argument of p has a non-basic type. For any atom p(t1 , . . . , tk ) in C, we define:
                           
                             p0       if σ(p) = 0
  σ(p(t1 , . . . , tk )) =
                             pi (ti ) if σ(p) = i > 0
where p0 (of arity 0) and pi (of arity 1) are fresh, new predicate symbols.
   We also define σ(C) to be the new clause σ(A0 ) ← σ(A1 ), . . . , σ(Am ). The slice σ
of C is quasi-descending if σ(A0 ), σ(A1 ), . . . , σ(Am ) are linear atoms and, for i = 1, . . . , m,
(1) for j = 1, . . . , m, vars(σ(Ai )) ∩ vars(σ(Aj )) = ∅, if i 6= j, and (2) either vars(σ(A0 )) ∩
vars(σ(Ai )) = ∅ or σ(A0 )  σ(Ai ).
   A slice decomposition of clause C is a set ΣC = {σ1 , . . . , σn }, where σ1 , . . . , σn are slices
of C and, for all p ∈ Pred, for all i ∈ {1, . . . , arity(p)}, if the i-th argument of p has non-
basic type, then there exists σj ∈ ΣC such that σj (p) = i. A slice decomposition ΣC of
a clause C is said to be disjoint if, for any two slices σh and σk in ΣC , we have that
vars(σh (C)) ∩ vars(σk (C)) = ∅, whenever h 6= k. ΣC is said to be quasi-descending if all
slices in ΣC are quasi-descending.
  The following are slices of clauses 4 and 7 (see Section 2):
  σ1 (clause 4) = min-leaf1 (node(X,L,R)) ← min-leaf 1 (L), min-leaf1 (R), min 0
  σ2 (clause 7) = left-drop2 (node(X, L, R)) ← left-drop2 (L)
  σ3 (clause 7) = left-drop3 (T ) ← left-drop3 (T )
We have that Σ4 = {σ1 } is a disjoint, quasi-descending slice decomposition of clause 4,
and so is Σ7 = {σ2 , σ3 } for clause 7.
  Now we define a class of goals for which Algorithm E terminates.
Definition 5 (Sharing Cycle)
Let G be a goal of the form false ← c, A1 , . . . , Am . We say that G has a sharing cycle
if there is a sequence of k (> 1) distinct variables X0 , . . . , Xk−1 of non-basic type, and a
sequence A00 , . . . , A0k of atoms in A1 , . . . , Am , such that: (i) A00 =A0k , (ii) A01 , . . . , A0k are all
distinct, and (iii) for i = 0, . . . , k−1, A0i and A0i+1 share the non-basic variable Xi .
  Now, if we represent the body of goal 8 of Section 2 as the following labeled graph:
                              T                                       U
     min -leaf (T, K)                   left -drop(N, T, U )                   min -leaf (U, M )
where the arc from a node A to a node B has label X iff X ∈ nbvars(A) ∩ nbvars(B),
then it is easy to see that goal 8 has no sharing cycle (indeed, there are no cycles in the
above graph).
  We have the following result, whose proof is given in the Appendix.
Theorem 3 (Termination)
Let Cls be a set of definite clauses such that every clause in Cls has a disjoint, quasi-
descending slice decomposition. Let Gs be a set of goals such that, for each goal G ∈ Gs,
(i) G is of the form false ← c, A1 , . . . , Am , where for i = 1, . . . , m, Ai is an atom whose
arguments are distinct variables, and (ii) G has no sharing cycles. Then Algorithm E
terminates for the input clauses Cls ∪ Gs.
           Solving Horn Clauses on Inductive Data Types Without Induction                 11

   Note that all definite clauses (clauses 1–7) of our introductory example have a quasi-
descending slice decomposition (see above for clauses 4 and 7). These slice decompositions
are also disjoint, except for the one of clause 6 where the second and third argument of
left-drop share some variables. However, clause 6 can be rewritten as:
  left-drop(N, node(X, L, R), node(X1, L1, R1)) ← N ≤ 0, X = X1, eqt(L, L1), eqt(R, R1)
  eqt(leaf , leaf ) ←
  eqt(node(X1, L1, R1), node(X2, L2, R2)) ← X1 = X2, eqt(L1, L2), eqt(R1, R2)
where predicate eqt defines the equality between binary trees. These three clauses have a
disjoint, quasi-descending slice decomposition, and after this rewriting the termination of
Algorithm E is guaranteed. The rewriting of any constrained fact, such as clause 6, into a
clause that has a disjoint, quasi-descending slice decomposition can be done automatically
as a pre-processing step, by introducing an equality predicate for each non-basic type.
However, in the benchmark set presented in Section 7, this pre-processing step has no
effect on the termination behavior of our transformation algorithms.


                    6 Adding Integer and Boolean Constraints
Algorithm E is not guaranteed to terminate outside the class of definite clauses and goals
considered in Theorem 3. Let us consider, for instance, the following set of clauses which
specifies a verification problem on lists:
append([ ], Ys, Ys) ←                     take(N, [ ], [ ]) ←
append([X|Xs], Ys, [Z|Zs]) ← X = Z,       take(N, [X|Xs], [ ]) ← N = 0
   append(Xs, Ys, Zs)                     take(N, [X|Xs], [Y |Ys]) ← N 6= 0, X = Y,
                                               N 1 = N −1, take(N 1, Xs, Ys)
drop(N, [ ], [ ]) ←                       diff--list([ ], [Y |Ys]) ←
drop(N, [X|Xs], [Y |Xs]) ← N = 0, X = Y   diff--list([X|Xs], [ ]) ←
drop(N, [X|Xs], Ys) ← N 6= 0, N 1 = N −1, diff--list([X|Xs], [Y |Ys]) ← X 6= Y
    drop(N 1, Xs, Ys)                     diff--list([X|Xs], [Y |Ys]) ← X = Y,
                                               diff--list(Xs, Ys)
false ← M = N, take(M, Xs, Ys), drop(N, Xs, Zs), append(Ys, Zs, A), diff--list(A, Xs)
In these clauses: (i) take(M, Xs, Ys) holds if the list Ys is the prefix of the list Xs up to
its M -th element, (ii) drop(N, Xs, Zs) holds if list Zs is a suffix of Xs starting from its
(N +1)-th element, (iii) append(Ys, Zs, A) holds if A is the concatenation of the lists Ys
and Zs, and (iv) diff--list(A, Xs) holds if A and Xs are different lists.
   The definite clauses listed above satisfy the hypothesis of Theorem 3 (after rewriting
some constrained facts as done at the end of the previous section), but the goal does not.
Indeed, that goal has the following sharing cycle:
  take(M,Xs,Ys) Xs drop(N,Xs,Zs) Zs append(Ys,Zs,A) Ys take(M,Xs,Ys)
Algorithm E does not terminate on this example. Indeed, starting from the definition:
  new0(M, N ) ← take(M, Xs, Ys), drop(N, Xs, Zs), append(Ys, Zs, A), diff--list(A, Xs)
infinitely many new predicates with unbounded lists are generated by Algorithm E. How-
ever, these predicates correspond to cases where M 6= N , and if we keep the constraint
M =N between the first arguments of take and drop, then a finite set of new predicates
is generated. In particular, if we start from the definition:
12                E. De Angelis, F. Fioravanti, A. Pettorossi, M. Proietti

 new1(M, N ) ← M=N, take(M, Xs, Ys), drop(N, Xs, Zs), append(Ys, Zs, A), diff--list(A, Xs)
the transformation terminates after a few steps and derives the following equisatisfiable
set of clauses, where an equality constraint holds for the two arguments of each occurrence
of new1:
     new2 ← new2
     new1(M, N ) ← M =N, M =0, new2
     new1(M, N ) ← M =N, M 6= 0, M =1+M 1, N =1+N 1, new1(M 1, N 1)
     false ← M =N, new1(M, N )
The satisfiability of this set of clauses is trivial, because it does not contain any con-
strained fact, and is easily proved by the Z3 solver.
   The above example motivates the introduction of a variant of Algorithm E, called
Algorithm EC, which is obtained by allowing in the Define step the introduction of
definitions whose bodies may include constraints in LIA ∪ Bool, and hence applying Fold
steps with respect to these definitions. The rest of Algorithm EC is equal to Algorithm E.
   As usual in constraint-based transformation techniques (see (De Angelis et al. 2017a)
for a recent paper), the computation of a suitable constraint when introducing a new
definition is done by means of a constraint generalization function Gen. We say that a
constraint g is more general than, or it is a generalization of, a constraint c, if LIA∪Bool |=
∀(c → g). Given a constraint c, a conjunction B of atoms, and a set Defs of definitions, the
function Gen matches the constraint c against the constraint d occurring in a definition
in Defs whose body is of the form d, B (modulo variable renaming), and returns a new
constraint Gen(c, B, Defs) which is more general than both c and d.
   The details of how the constraint generalization function Gen is actually implemented
are not necessary for understanding Algorithm EC, which is parametric with respect
to such a function. Let us only mention here that the function Gen used for the ex-
periments reported in Section 7 makes use on the widening operator based on bounded
difference shapes, which is a standard operator on convex polyhedra considered in the
field of abstract interpretation (Bagnara et al. 2008, Cousot and Halbwachs 1978). The
use of widening avoids the introduction of infinitely many definitions that differ for the
constraints only.
   The Define and Fold steps for Algorithm EC are as follows.

Let C: H ← c, B in InCls be a clause which is not a constrained fact.
   Define. Let SharingBlocks(B) = {B1 , . . . , Bn };
        for i = 1, . . . , n do
        gi := Gen(c, Bi , Defs ∪NewDefs);
        if there is no clause in Defs ∪NewDefs whose body is gi , Bi
        then NewDefs := NewDefs ∪ {newpi (Vi ) ← gi , Bi }
        where: (i) newpi is a new predicate symbol, and (ii) Vi is the tuple of distinct
        variables of basic type occurring in Bi ;
     Fold. C is folded using the definitions in Defs ∪ NewDefs, thereby deriving
        F : H ← c, newp1 (V1 ), . . . , newpn (Vn )
        where, for i = 1, . . . , n, newpi (Vi ) ← gi , Bi is the unique clause in Defs ∪ NewDefs
        whose body is gi , Bi , modulo variable renaming;
        FldCls := FldCls ∪ {F };
           Solving Horn Clauses on Inductive Data Types Without Induction              13

The partial correctness of Algorithm E (see Theorem 2) carries over to Algorithm EC,
because also EC can be expressed as a sequence of applications of the fold/unfold trans-
formation rules for CHCs (Etalle and Gabbrielli 1996). Also the termination result for
Algorithm E (see Theorem 3) extends to EC, as long as the function Gen guarantees that,
for a given conjunction B of atoms, finitely many definitions of the form newp(V ) ← g, B
can be introduced.


                            7 Experimental Evaluation
In this section we present the results of an experimental evaluation we have performed for
assessing the effectiveness of our approach and, in particular, for comparing it with the
approach that extends CHC solvers by adding inductive rules, as done in the RCaml tool
(Unno et al. 2017) based on the Z3 solver.

Implementation. We have implemented the transformation strategy presented in Sec-
tion 4 using the VeriMAP system (De Angelis et al. 2014) together with the Parma
Polyhedra Library (PPL) (Bagnara et al. 2008) for performing constraint generalizations.
Then, we have used the Z3 solver v4.6.0 with the Spacer fixed-point engine (Komuravelli
et al. 2013) to check the satisfiability of the transformed CHCs.
   The tool and the benchmark suite are available at https://fmlab.unich.it/iclp2018/.

Benchmark suite and experiments. Our benchmark suite is a collection of 105 verification
problems, each one consisting of an OCaml functional program manipulating inductively
defined data structures (such as lists or trees) together with a property to be verified.
Most of the problems (70 out of 105) derive from the benchmark suite of RCaml (see
http://www.cs.tsukuba.ac.jp/~uhiro/, Software RCaml, [web demo (induction)]). This
suite, in turn, includes problems from the suite of IsaPlanner (Dixon and Fleuriot 2003)
which is a generic framework for proof planning in the Isabelle theorem prover. We
divide our benchmark suite into four sets of problems (see Table 1): (1) FirstOrder,
the set of problems relative to first-order programs (57 out of 70) in the RCaml suite,
(2) HigherOrderInstances, the set of problems relative to first-order programs (13 out of
70) that have been obtained by instantiating higher-order programs in the RCaml suite,
(3) MoreLists, a set of 16 verification problems on lists, and (4) MoreTrees, a set of 19
verification problems on trees. In our benchmark 94 programs do satisfy the associated
property and the remaining 11 do not.
  By using the preprocessor provided by the RCaml system, each verification problem
has been translated into a set of CHCs (see the translation Tr of Section 3). Then, for
each derived set, call it I, of CHCs we have performed the following three experiments,
whose results are summarized in Table 1. (A table with the detailed results for each
problem of the benchmark is available at https://fmlab.unich.it/iclp2018/.)
• We have run Z3 (which does not use any structural induction rule) for checking the
  satisfiability of I (see the two columns for Z3).
• We have applied the transformation algorithm EC to I, thereby producing a set T
  of CHCs, and then we have run Z3 for checking the satisfiability of T (see the two
  columns for EC;Z3).
• We have run RCaml on I (see the two columns for RCaml).
14               E. De Angelis, F. Fioravanti, A. Pettorossi, M. Proietti

                                     Z3                  EC; Z3               RCaml
      Problem Set           n      SZ3     TZ3      SEC;Z3      TEC;Z3    SRCaml   TRCaml
(1) FirstOrder           57          3     0.09         47      37.64          41      216.59
(2) HigherOrderInstances 13          1     0.04         11       8.33          10       45.40
(3) MoreLists            16          3    13.87         14      11.27          10      119.01
(4) MoreTrees            19          5    20.18         19      26.79           5       55.16
          Total         105         12    34.18         91      84.03          66      436.17
          Avg time                         2.85                  0.92                    6.61

Table 1. Column n reports the number of problems in each Problem Set. Columns SZ3 and TZ3
report the number of problems which have been solved by Z3 and the total time needed for their
solution. Analogously, for the two columns referring to EC; Z3 and the two columns referring to
RCaml. Times are in seconds. The timeout occurs after 300s.


For each verification problem we have set a timeout limit of 300 seconds. Z3 and VeriMAP
have run on an Intel Xeon CPU E5-2640 2.00GHz with 64GB under CentOS. RCaml has
run in a Linux virtual machine on an Intel i5 2.3GHz with 8GB memory under macOS.

Results. The figures in Table 1 show that our approach considerably increases the effec-
tiveness of CHC satisfiability checking. Indeed, when directly applied to the CHCs that
encode the given verification problems, Z3 is able to solve 12 problems, while it solves 91
problems when it is applied to the CHCs produced by our transformation algorithm EC
(compare Columns SZ3 and SEC;Z3 ). For the remaining 14 problems, Algorithm EC does
not terminate within the time limit, and thus no CHCs are produced. Note that these 14
problems fall outside the class of programs for which Algorithm E, and also Algorithm EC,
is guaranteed to terminate.
   Table 1 shows that our approach compares quite well with respect to the induction
based approach implemented in the RCaml system (Unno et al. 2017). Indeed, EC; Z3
proves 65 out of 66 problems that are also proved by RCaml, and in addition it proves
26 problems, 7 of which belong to the RCaml benchmark suite. Also the average times
appear to be favorable to EC; Z3 with respect to RCaml. In particular, on the set of 67
problems where both EC; Z3 and RCaml provide the solution within the timeout, EC; Z3
is about six times faster than RCaml, having taken into account the fact that the machine
on which we have run RCaml is approximately 13% slower.
   Now let us report on some other important facts not shown in Table 1. When solving
verification problems via EC; Z3, a substantial portion of work is performed by Algo-
rithm EC. Indeed, the total time spent by Z3 for solving the 91 problems is only 6% of
the total solving time (84.03s). Moreover, for 42 problems the set of clauses produced
by EC does not contain constrained facts, and thus its satisfiability can immediately be
checked by Z3.
   Unfortunately, it may happen that our transformation prevents the solution of some
verification problems. Indeed, the transformation algorithm EC does not terminate within
the timeout on two problems that can be proved using Z3 alone. However, on the 10
problems that are solved by both Z3 and EC; Z3, the average time taken by EC; Z3
(3.41s) to solve one problem is much lower than that taken by Z3 alone (9.74s).
   Finally, let us comment on our benchmark suite. Many of the problems are small,
           Solving Horn Clauses on Inductive Data Types Without Induction                15

but the properties to be verified are not trivial, such as those presented in Sections 2
and 6. One of the most difficult problems solved by EC; Z3, but not by RCaml, consists
in showing that the insertion of a node in a binary search tree produces again a binary
search tree. That solution took about 5s. The solution of some of the 13 problems on
which both EC; Z3 and RCaml run out of time, requires the use of suitable lemmas. For
instance, one of these problems can be proved by using a lemma stating that the sum of
the elements of the concatenation of two lists is equal to the sum of the elements of the
first list plus the sum of the elements of the second list. The extension of our approach
to support automatic lemma discovery is left for future work.


                         8 Related Work and Conclusions
We have presented a two-step approach to the verification of programs that manipulate
inductively defined data structures, such as lists and trees. The first step consists in the
transformation of the set of clauses that encodes the given verification problem, into a
new, equisatisfiable set of clauses whose variables do no longer refer to inductive data
structures. The second step consists in the application of a CHC solver to the derived set
of clauses with integer and boolean constraints only. Thus, in our approach we can take
full advantage of the many efficient solvers that exist for clauses with integer and boolean
constraints (de Moura and Bjørner 2008, Grebenshchikov et al. 2012, Hoder and Bjørner
2012, Hojjat et al. 2012, Komuravelli et al. 2013). Through some experiments we have
shown that, using an implementation of our algorithm and the Z3 solver, our two-step
approach is competitive with respect to other techniques that extend CHC solvers by
adding deduction rules for reasoning on inductive data structures (Unno et al. 2017).
   Our transformation technique is related to methods proposed in the past for improv-
ing the efficiency of functional and logic programs, such as deforestation (Wadler 1990),
unnecessary variable elimination (UVE) (Proietti and Pettorossi 1995), and conjunctive
partial deduction (De Schreye et al. 1999). Among these techniques, the UVE transfor-
mation, which makes use of the fold/unfold rules, is the most similar to the one presented
in this paper. However, in this paper we have introduced several technical novelties with
respect to UVE: (i) the use of type information, (ii) the use of constraints, and (iii) a
better characterization of the termination of the main algorithm (in particular, here we
have introduced the notions of a slice decomposition and a circular sharing). At a more
general level, the objective of the work presented in this paper is to show the usefulness
of our transformation techniques for the improvement of the effectiveness of CHC solvers,
rather than the improvement of the execution of logic programs.
   The idea of using a transformation-based approach for the verification of software
comes from the area of Constraint Logic Programming, where program specialization
has been applied as a means of deriving CLP programs from interpreters of imperative
languages (Albert et al. 2007, De Angelis et al. 2017b, Méndez-Lojo et al. 2008, Peralta
et al. 1998). CHC solvers based on combinations of transformations and abstract inter-
pretation have also been developed (De Angelis et al. 2014, Kafle et al. 2016) and have
been shown to be competitive with solvers based on CEGAR, Interpolation, and PDR.
   Recently, CHCs have been proposed for verifying relational program properties (Felsing
et al. 2014), that is, properties that relate two programs, such as equivalence. It has
also been shown that predicate pairing, which is a fold/unfold transformation for CHCs,
16               E. De Angelis, F. Fioravanti, A. Pettorossi, M. Proietti

greatly improves the effectiveness of CHC solvers for relational verification (De Angelis
et al. 2015, De Angelis et al. 2016). A related CHC transformation technique, called CHC
product, works by composing pairs of clauses with an effect similar to predicate pairing,
although in some cases it may derive sets of clauses with fewer predicates (Mordvinov and
Fedyukovich 2017). Neither predicate pairing nor CHC product can remove inductively
defined data structures, as done by the transformation technique presented in this paper.
   Similarly to the technique presented in this paper, fold/unfold transformations and
constraint generalization have also been used in a verification technique for imperative
programs that compute over arrays (De Angelis et al. 2017a). However, the above men-
tioned technique is not able to remove array data structures, and unlike the one presented
here, it does not consider inductively defined data structures.
   We plan to extend our transformation-based verification method in a few directions,
and in particular we plan: (i) to study the problem of automatically generating the
lemmas which are sometimes needed for removing data structures, and (ii) to consider
the verification problem for higher-order functional programs.


                                  9 Acknowledgements
We would like to thank Hiroshi Unno for his support in the use of the RCaml system. We
thank the anonymous reviewers for their constructive comments. The authors are mem-
bers of the INdAM Research group GNCS. E. De Angelis, F. Fioravanti and A. Pettorossi
are research associates at CNR-IASI, Rome, Italy.


                                        References
Albert, E., Gómez-Zamalloa, M., Hubert, L., and Puebla, G. 2007. Verification of
  Java bytecode using analysis and transformation of logic programs. In Proc. of PADL ’07,
  LNCS 4354. Springer, 124–139.
Bagnara, R., Hill, P. M., and Zaffanella, E. 2008. The Parma Polyhedra Library: Toward
  a complete set of numerical abstractions for the analysis and verification of hardware and
  software systems. Science of Computer Programming, 72(1–2):3–21, 2008.
Bjørner, N., Gurfinkel, A., McMillan, K. L., and Rybalchenko, A. 2015. Horn clause
  solvers for program verification. In Fields of Logic and Computation II, LNCS 9300. Springer,
  24–51.
Bradley, A. R. 2011. SAT-based model checking without unrolling. In Proc. of VMCAI ’11,
  LNCS 6538. Springer, 70–87.
Clarke, E. M., Grumberg, O., Jha, S., Lu, Y., and Veith, H. 2000. Counterexample-
  Guided Abstraction Refinement. In Proc. of CAV ’00, LNCS 1855. Springer, 154–169.
Cousot, P. and Halbwachs, N. 1978. Automatic discovery of linear restraints among variables
  of a program. In Proc. of POPL ’78. ACM, 84–96.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2014. VeriMAP: A
  tool for verifying programs through transformations. In Proc. of TACAS ’14, LNCS 8413.
  Springer, 568–574.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2015. Proving correct-
  ness of imperative programs by linearizing constrained Horn clauses. Theory and Practice of
  Logic Programming 15, 635–650.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2016. Relational ver-
  ification through Horn clause transformation. In Proc. of SAS ’16, LNCS 9837. Springer,
  147–169.
            Solving Horn Clauses on Inductive Data Types Without Induction                    17

De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2017a. Program Ver-
  ification using Constraint Handling Rules and array constraint generalizations. Fundamenta
  Informaticae 150, 73–117.
De Angelis, E., Fioravanti, F., Pettorossi, A., and Proietti, M. 2017b. Semantics-
  based generation of verification conditions via program specialization. Science of Computer
  Programming 147, 78–108.
de Moura, L. M. and Bjørner, N. 2008. Z3: An efficient SMT solver. In Proc. of TACAS ’08.
  LNCS 4963. Springer, 337–340.
De Schreye, D., Glück, R., Jørgensen, J., Leuschel, M., Martens, B., and Sørensen,
  M. H. 1999. Conjunctive partial deduction: Foundations, control, algorithms, and experi-
  ments. Journal of Logic Programming 41, 2–3, 231–277.
Dixon, L. and Fleuriot, J. D. 2003. IsaPlanner: A prototype proof planner in Isabelle. In
  Proc. of CADE-19, LNCS 2741. Springer, 279–283.
Enderton, H. 1972. A Mathematical Introduction to Logic. Academic Press.
Etalle, S. and Gabbrielli, M. 1996. Transformations of CLP modules. Theoretical Computer
  Science 166, 101–146.
Felsing, D., Grebing, S., Klebanov, V., Rümmer, P., and Ulbrich, M. 2014. Automating
  regression verification. In Proc. of ACM/IEEE Conf. ASE ’14. 349–360.
Grebenshchikov, S., Lopes, N. P., Popeea, C., and Rybalchenko, A. 2012. Synthesizing
  software verifiers from proof rules. In Proc. of ACM SIGPLAN PLDI ’12. 405–416.
Hoder, K. and Bjørner, N. 2012. Generalized property directed reachability. In Proc. of
  SAT ’12, LNCS 7317. Springer, 157–171.
Hojjat, H., Konecný, F., Garnier, F., Iosif, R., Kuncak, V., and Rümmer, P. 2012. A
  verification toolkit for numerical transition systems. In Proc. of FM ’12, LNCS 7436. Springer,
  247–251.
Jaffar, J., Navas, J. A., and Santosa, A. E. 2012. Unbounded symbolic execution for
  program verification. In Proc. of RV ’11. LNCS 7186. Springer, 396–411.
Kafle, B., Gallagher, J. P., and Morales, J. F. 2016. RAHFT: A tool for verifying
  Horn clauses using abstract interpretation and finite tree automata. In Proc. of CAV ’16.
  LNCS 9779. Springer, 261–268.
Komuravelli, A., Gurfinkel, A., Chaki, S., and Clarke, E. M. 2013. Automatic abstrac-
  tion in SMT-based unbounded software model checking. In Proc. of CAV ’13, LNCS 8044.
  Springer, 846–862.
Leroy, X., Doligez, D., Frisch, A., Garrigue, J., Rémy, D., and Vouillon, J. 2017. The
  OCaml system, Release 4.06. INRIA, France.
McMillan, K. L. 2003. Interpolation and SAT-based model checking. In Proc. of CAV ’03.
  LNCS 2725. Springer, 1–13.
Méndez-Lojo, M., Navas, J. A., and Hermenegildo, M. V. 2008. A flexible, (C)LP-based
  approach to the analysis of object-oriented programs. In Proc. of LOPSTR’07. LNCS 4915.
  Springer, 154–168.
Mordvinov, D. and Fedyukovich, G. 2017. Synchronizing constrained Horn clauses. In Proc.
  of LPAR-21 EPiC Series in Computing Vol. 46. EasyChair, 338–355.
Peralta, J. C., Gallagher, J. P., and Saglam, H. 1998. Analysis of imperative programs
  through analysis of constraint logic programs. In Proc. of SAS ’98, LNCS 1503. Springer,
  246–261.
Proietti, M. and Pettorossi, A. 1995. Unfolding-definition-folding, in this order, for avoiding
  unnecessary variables in logic programs. Theoretical Computer Science 142, 1, 89–124.
Reynolds, A. and Kuncak, V. 2015. Induction for SMT solvers. In Proc. of VMCAI ’15,
  LNCS 8931. Springer, 80–98.
Suter, P., Köksal, A. S., and Kuncak, V. 2011. Satisfiability modulo recursive programs.
  In Proc. of SAS ’11, LNCS 6887. Springer, 298–315.
18              E. De Angelis, F. Fioravanti, A. Pettorossi, M. Proietti

Tamaki, H. and Sato, T. 1984. Unfold/fold transformation of logic programs. In Proc. of
  ICLP ’84, S.-Å. Tärnlund, Ed., Uppsala University, Sweden, 127–138.
Unno, H., Torii, S., and Sakamoto, H. 2017. Automating induction for solving Horn clauses.
  In Proc. of CAV ’17. LNCS 10427. Springer, 571–591.
Wadler, P. L. 1990. Deforestation: Transforming programs to eliminate trees. Theoretical
  Computer Science 73, 231–248.
            Solving Horn Clauses on Inductive Data Types Without Induction                      19

                                              Appendix
In order to prove Theorem 2, we first recall some notions and results regarding the
transformation rules and their correctness.
   A transformation sequence is a sequence S0 , S1 , . . . , Sn of sets of CHCs, whose con-
straints are in LIA ∪ Bool, where, for i = 0, . . . , n−1, Si+1 is derived from Si by applying
one of the following rules R1–R5.
   Let Defsi denote the set of all the clauses, called definitions, introduced by rule R1 dur-
ing the construction of the transformation sequence S0 , S1 , . . . , Si . In particular, Defs0 =∅.
(R1) Define. We introduce a clause D: newp(X1 , . . . , Xk ) ← c, G, where: (i) newp is a
predicate symbol not occurring in the sequence S0 , S1 , . . . , Si , (ii) c is a constraint in
LIA ∪ Bool, (iii) G is a non-empty conjunction of atoms whose predicate symbols occur
in S0 , and (iv) X1 , . . . , Xk are distinct variables occurring in (c, G). Then, we derive the
new set Si+1 = Si ∪ {D} and Defsi+1 = Defsi ∪ {D}.
(R2) Unfold. Let C: H ← c, L, A, R be a variant of a clause in Si . Let K1 ← c1 , B1 , . . . ,
Km ← cm , Bm be all clauses of Si (without loss of generality, we assume vars(Si ) ∩
vars(C) = ∅) such that, for j = 1, . . . , m, (1) there exists a most general unifier ϑj of A
and Kj , and (2) the constraint (c, cj )ϑj is satisfiable. By unfolding the atom A in C
using Si we derive the new set Si+1 = (Si \ {C}) ∪ {(H ← c, c1 , L, B1 , R)ϑ1 , . . . , (H ←
c, cm , L, Bm , R)ϑm }.
(R3) Fold. Let C: H ← c, L, Q, R be a clause in Si , where Q is a non-empty conjunction of
atoms, and let D: K ← d, B be (a variant of) a clause in Defsi with vars(C) ∩ vars(D)=∅.
Suppose that there exist a substitution ϑ and a constraint e such that: (i) Q = Bϑ,
(ii) LIA ∪ Bool |= ∀(c ↔ (e∧dϑ)), and (iii) for every variable X ∈ vars(d, B) \ vars(K),
the following conditions hold: (iii.1) Xϑ is a variable not occurring in {H, c, L, R}, and
(iii.2) Xϑ does not occur in the term Y ϑ, for any variable Y occurring in (d, B) and dif-
ferent from X. By folding C using the definition D, we derive clause E: H ← e, L, Kϑ, R.
In this case we also say that E is derived by folding Q in C. We derive the new set
Si+1 = (Si \ {C}) ∪ {E}.
(R4) Replace Equivalent Constraints. Let us consider a subset of Si of the form
{(H ← c1 , G), . . . , (H ← ck , G)}. Suppose that, for some constraints d1 , . . . , dm ,
  LIA ∪ Bool |= ∀ (∃Y1 . . . ∃Yr (c1 ∨ . . . ∨ ck ) ↔ ∃Z1 . . . ∃Zs (d1 ∨ . . . ∨ dm ))
where {Y1 , . . . ,Yr }=vars(c1 ∨. . .∨ck )\vars({H,G}) and {Z1 , . . . ,Zs }=vars(d1 ∨. . .∨dm )\
vars({H, G}). Then, we derive the new set Si+1 = (Si \ {(H ← c1 , G), . . . , (H ← ck , G)})
∪ {(H ← d1 , G), . . . , (H ← dm , G)}.
  Note that rule R4 enables the deletion of a clause with an inconsistent constraint in its
body. Indeed, if c1 is unsatisfiable, then LIA ∪ Bool |= ∀ (c1 ↔ d1 ∨ . . . ∨ dm ) with m = 0.
(R5) Replace Functional Predicates. Let C: H ← c, G1 , p(t, u), G2 , p(t, w), G3 , be a clause
in Si and let p(X, Y ) be functional in Si (see Definition 3). Then, we derive the new set
Si+1 = (Si \ {C}) ∪ {(H ← c, G1 , p(t, u), G2 , G3 )ϑ}, where ϑ is the most general unifier of
u and w.
 The following theorem sums up various results presented in the literature (Etalle and
Gabbrielli 1996, Tamaki and Sato 1984).
20               E. De Angelis, F. Fioravanti, A. Pettorossi, M. Proietti

Theorem 4 (Equivalence with respect to satisfiability)
Let S0 , S1 , . . ., Sn be a transformation sequence such that every definition in Defsn is
unfolded during the construction of this sequence. Then, S0 ∪ LIA ∪ Bool is satisfiable if
and only if Sn ∪ LIA ∪ Bool is satisfiable.

     Now, we prove Theorems 2 and 3 of Section 5.
Theorem 2 (Partial Correctness)
Let Cls be a set of definite clauses and let Gs be a set of goals. If Algorithm E terminates
for the input clauses Cls ∪ Gs, returning a set TransfCls of clauses, then (1) Cls ∪ Gs is
satisfiable iff TransfCls is satisfiable, and (2) all clauses in TransfCls have basic types.
Proof
Point (1) follows from Theorem 4 by taking into account that: (i) Algorithm E can be
viewed as a particular sequence of applications of Rules R1–R5, and (ii) every definition
in Defs is unfolded during the execution of E.
Point (2) follows from the fact that, by construction, every clause introduced in TransfCls
has basic types. To see this, let us consider a clause C in TransfCls. Clause C belongs
to the set FldCls of clauses obtained by a Define-Fold step. Looking at the Define-Fold
procedure, we have that: (i) the head of C is either false (because C ∈ Gs) or its head
predicate has been introduced by the Define step, and hence, by construction, has basic
types, and (ii) the body of C has the form: c, newp1 (V1 ), . . . , newpn (Vn ), where c is a
constraint which has basic types (because it belongs to LIA ∪ Bool) and newp1 , . . . , newpn
are predicates that, by construction, have basic types.                                     
Theorem 3 (Termination)
Let Cls be a set of definite clauses such that every clause in Cls has a disjoint, quasi-
descending slice decomposition. Let Gs be a set of goals such that, for each goal G ∈ Gs,
(i) G is of the form false ← c, A1 , . . . , Am , where for i = 1, . . . , m, Ai is an atom whose
arguments are distinct variables, and (ii) G has no sharing cycles. Then Algorithm E
terminates for the input clauses Cls ∪ Gs.
Proof (Sketch)
Without loss of generality, we assume that for every clause H ← c, B every variable of
basic type has at most one occurrence in H, B.
   For any tree t, by height(t) we denote the height of t, that is, the maximal length of a
path from the root of t to one of its leaves. We extend the function height to terms and
atoms, viewed as trees. First of all, we observe that Algorithm E terminates iff there exists
two non-negative integers H and N such that, for every definition newp(V ) ← A1 , . . . , An
added to Defs during the execution of E, we have that, for i = 1, . . . n, height(Ai )≤H, and
n ≤ N . Indeed, the existence of H and N implies the finiteness of the set of definitions
introduced by E, and hence the finiteness of the number of iterations of the body of the
while-do loop of E itself.
   Let us consider a clause D: newp(V ) ← A1 , . . . , An added to Defs during the execution
of E. Then D satisfies the following properties:
  P1. The goal false ← A1 , . . . , An obtained from D by replacing newp(V ) by false, has
      no sharing cycles;
  P2. All atoms in the body of D are linear;
  P3. For any two distinct atoms Ai and Aj in the body of D, if Ai and Aj share a
            Solving Horn Clauses on Inductive Data Types Without Induction                            21

     non-basic variable, then they are of the form p(. . . , ti , . . .) and q(. . . , tj , . . .), where
     either ti  tj or tj  ti , and Ai and Aj do not share any variable besides the ones
     in vars(ti ) ∩ vars(tj );
 P4. For any atom Ai in the body of D, height(Ai )≤H, where H is the maximal height
     of an atom in Cls ∪ Gs;
 P5. Let VG be the number of occurrences of non-basic variables in a goal G, and let M
     be max{VG | G ∈ Gs}+1. Then, in the body of D, (P5.1) every non-basic variable
     has at most M occurrences, and (P5.2) there exist K ≤ M predicate arguments
     such that every non-basic variable that occurs more than once, also occurs in one
     of those K arguments.

Property P1 holds for each clause D initially in Defs by the hypothesis that Gs is a set of
goals that have no sharing cycles. This property, when referred to the body of the clauses,
is preserved by the Unfold and Replace steps, due to the hypothesis on the clauses in Cls,
and hence it also holds for each new definition added to Defs by the Define step after
Unfold and Replace.
   Property P2 holds for each clause D initially in Defs by Hypothesis (i) on Gs. This
property is preserved by the Unfold and Replace steps, due to the hypothesis on the
clauses in Cls. Note, in particular, that the existence of a disjoint, quasi-descending slice
decomposition for all clauses in Cls implies that each atom in the body of a clause in Cls
is linear, and hence only linear atoms are introduced by Unfold steps. The linearity of
the atoms different from the one replaced by an Unfold step is enforced by the existence
of a disjoint, quasi-descending slice decomposition for all clauses in Cls. Linearity is also
preserved by Replace steps. Thus, Property P2 follows from the fact that the body of D
consists of atoms taken from the body of a clause derived by Unfold and Replace steps.
   Property P3 holds for each clause D initially in Defs by Hypothesis (i) on Gs. Prop-
erty P3 also holds for each clause derived by the Unfold and Replace steps by Property P1
and by the hypothesis that every clause in Cls has a disjoint, quasi-descending slice de-
composition. Then, Property P3 follows from the fact that the body of D consists of
atoms taken from the body of clauses derived by Unfold and Replace steps.
   Property P4 holds for each clause D initially in Defs because the body of clause D is
the set of atoms occurring in the body of a goal in Gs. This property also holds for each
clause derived by Unfold steps. Indeed, suppose that we unfold an atom A in the clause C
of the form H ← c, L, A, R such that either (i) A is strictly maximal in L, A, R, or (ii) all
atoms in L, A, R are not strictly maximal. Both in case (i) and case (ii), by Property P3,
A is of the form p(. . . , ti , . . .) and any atom Q in L, R that shares a non-basic variable
with A is of the form q(. . . , tj , . . .), with tj  ti , and A and Q do not share any variable
besides the ones in vars(ti ) ∩ vars(tj ). Let K1 ← c1 , B1 , . . . , Km ← cm , Bm be all clauses
of Cls (with vars(Cls) ∩ vars(C) = ∅) such that, for i = 1, . . . , m, (i) there exists a most
general unifier ϑi of A and Ki , and (ii) the constraint (c, ci )ϑi is satisfiable. Then, by un-
folding A in C we derive the clauses (H ← c, c1 , L, B1 , R)ϑ1 , . . . , (H ← c, cm , L, Bm , R)ϑm .
By Property P2 A is a linear atom, and by the hypothesis that every clause in Cls has
a disjoint, quasi-descending slice decomposition, we have that, for i = 1, . . . , m, for ev-
ery atom E in L, Bi , R, height(Eϑi ) ≤ max({height(E), height(A), height(Ki )}). Thus, if
Property P4 holds for C, then it also holds for the clauses (H ← c, c1 , L, B1 , R)ϑ1 , . . . ,
(H ← c, cm , L, Bm , R)ϑm . Property P4 also holds for each clause derived by Replace steps,
22               E. De Angelis, F. Fioravanti, A. Pettorossi, M. Proietti

and hence it also holds for D, whose body consists of atoms taken from the body of clauses
derived by Unfold and Replace steps.
   Property P5 holds for each clause D initially in Defs because the body of clause D
is the set of atoms occurring in the body of a goal G in Gs for which Hypothesis (i)
holds. Now we prove that the following two properties, which generalize Property P5,
hold for each clause E derived by an Unfold step: in each sharing block in the body of E,
(P5.1) every non-basic variable has at most M occurrences, and (P5.2) there exist K ≤M
predicate arguments such that every non-basic variable with more than one occurrence
in the body of E, also occurs in one of those K arguments.
   Suppose that P5.1 and P5.2 hold for a clause C of the form H ← c, L, A, R, and we
unfold A in C. Let K1 ← c1 , B1 , . . . , Km ← cm , Bm be all clauses of Cls (with vars(Cls) ∩
vars(C) = ∅) such that, for i=1, . . . , m, (i) there exists a most general unifier ϑi of A and
Ki , and (ii) the constraint (c, ci )ϑi is satisfiable. Then, by unfolding A in C we derive the
clauses C1 : (H ← c, c1 , L, B1 , R)ϑ1 , . . . , Cm : (H ← c, cm , L, Bm , R)ϑm . By Properties P2
and P3, and by the existence of a disjoint, quasi-descending slice decomposition, for
i = 1, . . . , m, the number of occurrences of any variable with more than one occurrence
in the body of Ci , is not larger than the maximal number of occurrences of any variable
in the body of C, and hence Property P5.1 holds for the body of Ci .
   Moreover, suppose that in every sharing block in the body of C there exist K ≤ M
arguments t1 , . . . , tK such that every variable variable with more than one occurrence,
also occurs in one of those K arguments. By Property P3, we may assume that t1 , . . . , tK
are maximal with respect to the  relation and do not share any variable. Looking at
the Unfold procedure, the atom A selected for unfolding must have one among t1 , . . . , tK
as an argument, say t1 . By our hypotheses, if by unfolding A the argument t1 is replaced
by more than one term, these new terms must appear in different sharing blocks, and
hence the number of maximal arguments in each sharing block does not increase. Thus,
Property P5.2 holds for C1 , . . . , Cm . Similarly, we can prove that Properties P5.1 and
P5.2 hold for each clause derived by Replace steps, and hence Property 5 holds for D,
whose body consists of a sharing block of a clause derived by Unfold and Replace steps.
   Now, from Properties P4 and P5 it follows that there exists an integer J, depending
on H and M , such that in the body of D there are at most J distinct variables. Thus,
there exists N such that the body of D has at most N atoms of height not larger than
H, and hence the thesis holds.                                                                  
