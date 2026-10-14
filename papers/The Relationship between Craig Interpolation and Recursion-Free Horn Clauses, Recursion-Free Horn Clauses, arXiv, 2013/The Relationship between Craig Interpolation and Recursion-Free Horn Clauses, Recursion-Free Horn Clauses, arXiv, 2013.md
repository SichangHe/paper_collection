                                            The Relationship between Craig Interpolation and
                                                      Recursion-Free Horn Clauses

                                                        Philipp Rümmer1 , Hossein Hojjat2 , and Viktor Kuncak2
                                                                         1
                                                                           Uppsala University, Sweden
arXiv:1302.4187v1 [cs.LO] 18 Feb 2013




                                                          2
                                                              Swiss Federal Institute of Technology Lausanne (EPFL)


                                               Abstract. Despite decades of research, there are still a number of concepts com-
                                               monly found in software programs that are considered challenging for verifica-
                                               tion: among others, such concepts include concurrency, and the compositional
                                               analysis of programs with procedures. As a promising direction to overcome such
                                               difficulties, recently the use of Horn constraints as intermediate representation of
                                               software programs has been proposed. Horn constraints are related to Craig inter-
                                               polation, which is one of the main techniques used to construct and refine abstrac-
                                               tions in verification, and to synthesise inductive loop invariants. We give a survey
                                               of the different forms of Craig interpolation found in literature, and show that all
                                               of them correspond to natural fragments of (recursion-free) Horn constraints. We
                                               also discuss techniques for solving systems of recursion-free Horn constraints.


                                        1 Introduction
                                        Predicate abstraction [13] has emerged as a prominent and effective way for model
                                        checking software systems. A key ingredient in predicate abstraction is analyzing the
                                        spurious counter-examples to refine abstractions [4]. The refinement problem saw a
                                        significant progress when Craig interpolants extracted from unsatisfiability proofs were
                                        used as relevant predicates [18]. While interpolation has enjoyed a significant progress
                                        for various logical constraints [6–8, 21], there have been substantial proposals for more
                                        general forms of interpolation [1, 17, 21].
                                            As a promising direction to extend the reach of automated verification methods to
                                        programs with procedures, and concurrent programs, among others, recently the use
                                        of Horn constraints as intermediate representation has been proposed [14, 15, 25]. This
                                        report examines the relationship between various forms of Craig interpolation and syn-
                                        tactically defined fragments of recursion-free Horn clauses. We systematically exam-
                                        ine binary interpolation, inductive interpolant sequences, tree interpolants, restricted
                                        DAG interpolants, and disjunctive interpolants, and show the recursion-free Horn clause
                                        problems to which they correspond. We present algorithms for solving each of these
                                        classes of problems by reduction to elementary interpolation problems. We also give
                                        a taxonomy of the various interpolation problems, and the corresponding systems of
                                        Horn clauses, in terms of their computational complexity.

                                        2 Related Work
                                        The use of Horn clauses as intermediate representation for verification was proposed in
                                        [26]. The authors is [15] use Horn clauses for verification of multi-threaded programs.
2       Rümmer, Hojjat, Kuncak

The underlying procedure for solving sets of recursion-free Horn clauses, over the com-
bined theory of linear integer arithmetic and uninterpreted functions, was presented
in [16]. A range of further applications of Horn clauses, including inter-procedural
model checking, was given in [14]. Horn clauses are also proposed as intermediate/ex-
change format for verification problems in [5], and are natively supported by the SMT
solver Z3 [10].
    There is a long line of research on Craig interpolation methods, and generalised
forms of interpolation, tailored to verification. For an overview of interpolation in the
presence of theories, we refer the reader to [7, 8]. Binary Craig interpolation for impli-
cations A → C goes back to [9], was carried over to conjunctions A ∧ B in [22], and
generalised to inductive sequences of interpolants in [18, 24]. The concept of tree in-
terpolation, strictly generalising inductive sequences of interpolants, is presented in the
documentation of the interpolation engine iZ3 [21]; the computation of tree interpolants
by computing a sequence of binary interpolants is also described in [17]. Restricted
DAG interpolants [1] and disjunctive interpolants [27] are a further generalisation of
inductive sequences of interpolants, designed to enable the simultaneous analysis of
multiple counterexamples or program paths.
    The use of Craig interpolation for solving Horn clauses is discussed in [25], con-
centrating on the case of tree interpolation. Our paper extends this work by giving a
systematic study of the relationship between different forms of Craig interpolation and
Horn clauses, as well as general results about solvability and computational complexity,
independent of any particular calculus used to perform interpolation.
    Inter-procedural software model checking with interpolants has been an active
area of research for the last decade. In the context of predicate abstraction, it has been
discussed how well-scoped invariants can be inferred [18] in the presence of function
calls. Based on the concept of Horn clauses, a predicate abstraction-based algorithm for
bottom-up construction of function summaries was presented in [14]. Generalisations
of the Impact algorithm [24] to programs with procedures are given in [17] (formulated
using nested word automata) and [2]. Finally, function summaries generated using in-
terpolants have also been used to speed up bounded model checking [28].
    Several other tools handle procedures by increasingly inlining and performing under
and/or over-approximation [19, 29, 30], but without the use of interpolation techniques.


3 Example

We start with an example illustrating the use of Horn clauses to verify a recursive pro-
gram. Fig. 1 shows an example of a recursive program, which is encoded as a set of
(recursive) Horn constraints in Fig. 2. The function f recursively computes the incre-
ment of the argument n by 1.
    For translation to Horn clauses we assign an uninterpreted relation symbol ri to
each state qi of the control flow graph. The arguments of the relation symbol ri act as
placeholders of the visible variables in the state qi . The relation symbol rf corresponds
to the summary of the function f. In the relation symbol rf we do not include the local
variable tmp in the arguments since it is invisible from outside the function f. The first
        The Relationship between Craig Interpolation and Recursion-Free Horn Clauses                3


def f (n : Int )
      returns rec : Int = {
  if (n > 0) {
    tmp = f (n−1)                                                                 
                                             /.-,
                                             ()*+
                                              q1                        n>0      /.-,
                                                                                 ()*+
                                                                                  q5       ¬(n>0)
    rec = tmp + 1
  } else {                  havoc (x) ∧ x′ ≥ 0
    rec = 1                                                                                
                                             /.-,
                                             ()*+q2              /.-,
                                                                 ()*+
                                                                  q6                       /.-,
                                                                                           ()*+
                                                                                            q8
    }
}                                     res′ = f (x)                  tmp′ = f (n − 1)
def main() {                                                      
                                               /.-,
                                               ()*+
                                                q3 ❄            /.-,
                                                                ()*+
                                                                 q7
  var res : Int                  res=x + 1 ⑧⑧
                                              ⑧     ❄❄                                        rec′ =1
  havoc(x: Int ≥ 0)                         ⑧⑧ res,x❄+ ❄❄1
                                         ⑧⑧                    ′                     z
  res = f (x)                        /.-,
                                     ()*+
                                      q4                   e rec =tmp + 1
                                                        /.-,
                                                        ()*+                     +/.-,
                                                                                  ()*+
                                                                                   q9
  assert(res == x + 1)
}

               Fig. 1. A recursive program and its control flow graph (see Sect. 3).

(1)     r1(X, Res) ←     true
(2)     r2(X’ , Res) ←   r1(X, Res) ∧ X’ ≥ 0
(3)     r3(X, Res’) ←    r2(X, Res) ∧ rf(X, Res’)
(4)     r4(X, Res) ←     r3(X, Res) ∧ Res = X + 1
(5)     false        ←   r3(X, Res) ∧ Res , X + 1

(6)     r5(N, Rec, Tmp) ←      true
(7)     r6(N, Rec, Tmp) ←      r5(N, Rec, Tmp) ∧ N > 0
(8)     r7(N, Rec, Tmp’) ←     r6(N, Rec, Tmp) ∧ rf(N − 1, Tmp’)
(9)     r8(N, Rec, Tmp) ←      r5(N, Rec, Tmp) ∧ N ≤ 0
(10)    r9(N, Rec’, Tmp) ←     r7(N, Rec, Tmp) ∧ Rec’ = Tmp + 1
(11)    r9(N, Rec’, Tmp) ←     r8(N, Rec, Tmp) ∧ Rec’ = 1
(12)    rf (N, Rec)      ←     r9(N, Rec, Tmp)


        Fig. 2. The encoding of the program in Fig. 1 into a set of recursive Horn clauses.



argument of rf is the input and the second one is the output. We do not dedicate any
relation symbol to the error state e.
    The initial states of the functions are not constrained at the beginning; they are just
implied by true. The clause that has false as its head corresponds to the assertion in the
program. In order to satisfy the assertion with the head false, the body of the clause
should also be evaluated to false. We put the condition leading to error in the body of
this clause to ensure the error condition is not happening. The rest of the clauses are
one to one translation of the edges in the control flow graph.
    For the edges with no function calls we merely relate the variables in the previous
state to the variables in the next state using the transfer functions on the edges. For
example, the clause (2) expresses that res is kept unchanged in the transition from q1 to
q2 and the value of x is greater than or equal to 0 in q2 . For the edges with function call
4          Rümmer, Hojjat, Kuncak


                               r1 (x, res) ≡ true
                               r2 (x, res) ≡ x ≥ 0
                               r3 (x, res) ≡ res = x + 1
                               r4 (x, res) ≡ true
                          r5 (n, rec, tmp) ≡ true
                          r6 (n, rec, tmp) ≡ n ≥ 1
                          r7 (n, rec, tmp) ≡ n = tmp
                          r8 (n, rec, tmp) ≡ n ≤ 0
                          r9 (n, rec, tmp) ≡ rec = n + 1 ∨ (n ≤ 0 ∧ rec = 1)
                               r f (n, rec) ≡ rec = n + 1 ∨ (n ≤ 0 ∧ rec = 1)


                        Fig. 3. Syntactic solution of the Horn clauses in Fig. 2.


we should also take care of the passing arguments and the return values. For example,
the clause (3) corresponds to the edge containing a function call from q2 to q3 . This
clause sets the value of res in the state q3 to the return value of the function f. Note
that the only clauses in this example that have more than one relation symbols in the
body are the ones related to edges with function calls.
     The solution of the obtained system of Horn clauses demonstrates the correctness
of the program. In a solution each relation symbol is mapped to an expression over
its arguments. If we replace the relation symbols in the clauses by the expressions in
the solution we should obtain only valid clauses. In a system with a genuine path to
error we cannot find any solution to the system since we have no way to satisfy the
assertion clause. Fig. 3 gives one possible solution of the Horn clauses in terms of
concrete formulae, found by our verification tool Eldarica.3
     This paper discusses techniques to automatically construct solutions of Horn clauses.
Although the Horn clauses encoding programs are typically recursive, it has been ob-
served that the case of recursion-free Horn clauses is instrumental for constructing ver-
ification procedures operating on Horn clauses [14, 15, 25]. Sets of recursion-free Horn
clauses are usually extracted from recursive clauses by means of finite unwinding; ex-
amples are given in Sect. 5.3 and 5.5.


4 Formulae and Horn Clauses

Constraint languages. Throughout this paper, we assume that a first-order vocabulary
of interpreted symbols has been fixed, consisting of a set F of fixed-arity function
symbols, and a set P of fixed-arity predicate symbols. Interpretation of F and P is
determined by a class S of structures (U, I) consisting of non-empty universe U, and
a mapping I that assigns to each function in F a set-theoretic function over U, and
to each predicate in P a set-theoretic relation over U. As a convention, we assume
 3
     http://lara.epfl.ch/w/eldarica
       The Relationship between Craig Interpolation and Recursion-Free Horn Clauses                    5

the presence of an equation symbol “=” in P, with the usual interpretation. Given a
countably infinite set X of variables, a constraint language is a set Constr of first-
order formulae over F , P, X For example, the language of quantifier-free Presburger
arithmetic has F = {+, −, 0, 1, 2, . . .} and P = {=, ≤, |}).
    A constraint is called satisfiable if it holds for some structure in S and some as-
signment of the variables X, otherwise unsatisfiable. We say that a set Γ ⊆ Constr of
constraints entails a constraint φ ∈ Constr if every structure and variable assignment
that satisfies all constraints in Γ also satisfies φ; this is denoted by Γ |= φ.
    fv(φ) denotes the set of free variables in constraint φ. We write φ[x1 , . . . , xn ] to state
that a constraint contains (only) the free variables x1 , . . . , xn , and φ[t1 , . . . , tn ] for the
result of substituting the terms t1 , . . . , tn for x1 , . . . , xn . Given a constraint φ containing
the free variables x1 , . . . , xn , we write Cl∀ (φ) for the universal closure ∀x1 , . . . , xn .φ.

Craig interpolation is the main technique used to construct and refine abstractions in
software model checking. A binary interpolation problem is a conjunction A ∧ B of
constraints. A Craig interpolant is a constraint I such that A |= I and B |= ¬I, and
such that fv(I) ⊆ fv(A) ∩ fv(B). The existence of an interpolant implies that A ∧ B is
unsatisfiable. We say that a constraint language has the interpolation property if also
the opposite holds: whenever A ∧ B is unsatisfiable, there is an interpolant I.


4.1 Horn Clauses

To define the concept of Horn clauses, we fix a set R of uninterpreted fixed-arity relation
symbols, disjoint from P and F . A Horn clause is a formula C ∧ B1 ∧ · · · ∧ Bn → H
where

  – C is a constraint over F , P, X;
  – each Bi is an application p(t1 , . . . , tk ) of a relation symbol p ∈ R to first-order terms
    over F , X;
  – H is similarly either an application p(t1 , . . . , tk ) of p ∈ R to first-order terms, or is
    the constraint false.

H is called the head of the clause, C∧B1 ∧· · ·∧Bn the body. In case C = true, we usually
leave out C and just write B1 ∧ · · · ∧ Bn → H. First-order variables (from X) in a clause
are considered implicitly universally quantified; relation symbols represent set-theoretic
relations over the universe U of a structure (U, I) ∈ S. Notions like (un)satisfiability and
entailment generalise straightforwardly to formulae with relation symbols.
    A relation symbol assignment is a mapping sol : R → Constr that maps each n-ary
relation symbol p ∈ R to a constraint sol(p) = C p [x1 , . . . , xn ] with n free variables. The
instantiation sol(h) of a Horn clause h is defined by:

 sol C ∧ p1 (t¯1 ) ∧ · · · ∧ pn (t¯n ) → p(t¯) = C ∧ sol(p1 )[t¯1 ] ∧ · · · ∧ sol(pn )[t¯n ] → sol(p)[t¯]
                                              

sol C ∧ p1 (t¯1 ) ∧ · · · ∧ pn (t¯n ) → false = C ∧ sol(p1 )[t¯1 ] ∧ · · · ∧ sol(pn )[t¯n ] → false
                                              


Definition 1 (Solvability). Let HC be a set of Horn clauses over relation symbols R.
6          Rümmer, Hojjat, Kuncak

    Form of interpolation                  Fragment of Horn clauses

    Binary interpolation [9, 22]           Pair of Horn clauses
    A∧B                                    A → p( x̄), B ∧ p( x̄) → false with { x̄} = fv(A) ∩ fv(B)

    Inductive interpolant seq. [18, 24]    Linear tree-like Horn clauses
    T1 ∧ T2 ∧ · · · ∧ Tn                   T 1 → p1 ( x̄1 ), p1 ( x̄1 ) ∧ T 2 → p2 ( x̄2 ), . . .
                                           with { x̄i } = fv(T 1 , . . . , T i ) ∩ fv(T i+1 , . . . , T n )

    Tree interpolants [17, 21]             Tree-like Horn clauses

    Restricted DAG interpolants [1]        Linear Horn clauses

    Disjunctive interpolants [27]          Body disjoint Horn clauses

            Table 1. Equivalence of interpolation problems and systems of Horn clauses.




 1. HC is called semantically solvable if for every structure (U, I) ∈ S there is an
    interpretation of the relation symbols R as set-theoretic relations over U such the
    universally quantified closure Cl∀ (h) of every clause h ∈ HC holds in (U, I).
 2. A HC is called syntactically solvable if there is a relation symbol assignment sol
    such that for every structure (U, I) ∈ S and every clause h ∈ HC it is the case that
    Cl∀ (sol(h)) is satisfied.

    Note that, in the special case when S contains only one structure, S = {(U, I)},
semantic solvability reduces to the existence of relations interpreting R that extend the
structure (U, I) in such a way to make all clauses true. In other words, Horn clauses
are solvable in a structure if and only if the extension of the theory of (U, I) by relation
symbols R in the vocabulary and by given Horn clauses as axioms is consistent.
    A set HC of Horn clauses induces a dependence relation →HC on R, defining
p →HC q if there is a Horn clause in HC that contains p in its head, and q in the
body. The set HC is called recursion-free if →HC is acyclic, and recursive otherwise.
In the next sections we study the solvability problem for recursion-free Horn clauses
and then show how to use such results in general Horn clause verification systems.


5 Generalised Forms of Craig Interpolation

It has become common to work with generalised forms of Craig interpolation, such as
inductive sequences of interpolants, tree interpolants, and restricted DAG interpolants.
We show that a variety of such interpolation approaches can be reduced to recursion-
free Horn clauses. Recursion-free Horn clauses thus provide a general framework uni-
fying and subsuming a number of earlier notions. As a side effect, we can formulate
a general theorem about existence of the individual kinds of interpolants in Sect. 6,
applicable to any constraint language with the (binary) interpolation property.
    An overview of the relationship between specific forms of interpolation and specific
fragments of recursions-free Horn clauses is given in Table 1, and will be explained in
        The Relationship between Craig Interpolation and Recursion-Free Horn Clauses                               7

more detail in the rest of this section. Table 1 refers to the following fragments of
recursion-free Horn clauses:
Definition 2 (Horn clause fragments). We say that a finite, recursion-free set HC of
Horn clauses

 1. is linear if the body of each Horn clause contains at most one relation symbol,
 2. is body-disjoint if for each relation symbol p there is at most one clause containing
    p in its body; furthermore, every clause contains p at most once;
 3. is head-disjoint if for each relation symbol p there is at most one clause containing
    p in its head;
 4. is tree-like [16] if it is body-disjoint and head-disjoint.

Theorem 1 (Interpolation and Horn clauses). For each line of Table 1 it holds that:

 1. an interpolation problem of the stated form can be polynomially reduced to (syn-
    tactically) solving a set of Horn clauses, in the stated fragment;
 2. solving a set of Horn clauses (syntactically) in the stated fragment can be polyno-
    mially reduced to solving a sequence of interpolation problems of the stated form.


5.1 Binary Craig Interpolants [9, 22]

The simplest form of Craig interpolation is the derivation of a constraint I such that A |=
I and I |= ¬B, and such that fv(I) ⊆ fv(A)∩fv(B). Such derivation is typically constructed
by efficiently processing the proof of unsatisfiability of A ∧ B. To encode a binary
interpolation problem into Horn clauses, we first determine the set x̄ = fv(A) ∩ fv(B) of
variables that can possibly occur in the interpolant. We then pick a relation symbol p of
arity | x̄|, and define two Horn clauses expressing that p( x̄) is an interpolant:

                                    A → p( x̄),           B ∧ p( x̄) → false

It is clear that every syntactic solution for the two Horn clauses corresponds to an inter-
polant of A ∧ B.


5.2 Inductive Sequences of Interpolants [18, 24]

Given an unsatisfiable conjunction T 1 ∧ . . . ∧ T n (in practice, often corresponding
to an infeasible path in a program), an inductive sequence of interpolants is a se-
quence I0 , I1 , . . . , In of formulae such that

 1. I0 = true, In = false,
 2. for all i ∈ {1, . . . , n}, the entailment Ii−1 ∧ T i |= Ii holds, and
 3. for all i ∈ {0, . . . , n}, it is the case that fv(Ii ) ⊆ fv(T 1 , . . . , T i ) ∩ fv(T i+1 , . . . , T n ).

While inductive sequences can be computed by repeated computation of binary inter-
polants [18], more efficient solvers have been developed that derive a whole sequence
of interpolants simultaneously [7, 8, 21].
8         Rümmer, Hojjat, Kuncak

Inductive sequences as linear tree-like Horn clauses. An inductive sequence of inter-
polants can straightforwardly be encoded as a set of linear Horn clauses, by introducing
a fresh relation symbol pi for each interpolant Ii to be computed. The arguments of the
relation symbols have to be chosen reflecting condition 3 of the definition of interpolant
sequences: for each i ∈ {0, . . . , n}, we assume that x̄i = fv(T 1 , . . . , T i ) ∩ fv(T i+1 , . . . , T n )
is the vector of variables that can occur in Ii . Conditions 1 and 2 are then represented
by the following Horn clauses:

      p0 ( x̄0 ), p0 ( x̄0 ) ∧ T 1 → p1 ( x̄1 ), p1 ( x̄1 ) ∧ T 2 → p2 ( x̄2 ), . . . , pn ( x̄n ) → false

Linear tree-like Horn clauses as inductive sequences. Suppose HC is a finite, recursion-
free, linear, and tree-like set of Horn clauses. We can solve the system of Horn clauses
by computing one inductive sequence of interpolants for every connected component of
the →HC -graph. First, each clause is normalised in a manner similar to [14]: for every
relation symbol p, we fix a unique vector of variables x̄ p , and rewrite HC such that
p only occurs in the form p( x̄ p ); this is possible since HC is recursion-free and body-
disjoint. We then ensure, through renaming, that every variable x that is not argument of
a relation symbol occurs in at most one clause. A connected component then represents
Horn clauses

C1 → p1 ( x̄1 ), C2 ∧ p1 ( x̄1 ) → p2 ( x̄2 ), C3 ∧ p2 ( x̄2 ) → p3 ( x̄3 ), . . . , Cn ∧ pn ( x̄n ) → false .

(If the first or the last of the clauses is missing, we assume that its constraint is false.)
Any inductive sequence of interpolants for C1 ∧ C2 ∧ C3 ∧ · · · ∧ Cn solves the clauses.


5.3 Tree Interpolants [17, 21]

Tree interpolants strictly generalise inductive sequences of interpolants, and are de-
signed with the application of inter-procedural verification in mind: in this context, the
tree structure of the interpolation problem corresponds to (a part of) the call graph of
a program. Tree interpolation problems correspond to recursion-free tree-like sets of
Horn clauses.
    Suppose (V, E) is a finite directed tree, writing E(v, w) to express that the node w
is a direct child of v. Further, suppose φ : V → Constr is a function that labels each
node v of the tree with a formula φ(v). A labelling function I : V → Constr is called a
tree interpolant (for (V, E) and φ) if the following properties hold:

 1. for the root node v0 ∈ V, it is the case that I(v0 ) = false,
 2. for any node v ∈ V, the following entailment holds:
                                           ^
                                  φ(v) ∧        I(w) |= I(v) ,
                                                  (v,w)∈E


 3. for any node v ∈ V, every non-logical symbol (in our case: variable) in I(v) occurs
    both in some formula φ(w) for w such that E ∗ (v, w), and in some formula φ(w′ ) for
    some w′ such that ¬E ∗ (v, w′ ). (E ∗ is the reflexive transitive closure of E).
         The Relationship between Craig Interpolation and Recursion-Free Horn Clauses              9

   Since the case of tree interpolants is instructive for solving recursion-free sets of
Horn clauses in general, we give a result about the existence of tree interpolants. The
proof of the lemma computes tree interpolants by repeated derivation of binary inter-
polants; however, as for inductive sequences of interpolants, there are solvers that can
compute all formulae of a tree interpolant simultaneously [15, 16, 21].
Lemma 1. Suppose the constraint language Constr that has the interpolation property.
Then a tree (V, E) with labelling function φ : V → Constr has a tree interpolant I if and
       V
only if v∈V φ(v) is unsatisfiable.

Proof. “⇒” follows from the observation that every interpolant I(v) is a consequence
                         V
of the conjunction (v,w)∈E+ φ(w).
    “⇐”: let v1 , v2 , . . . , vn be an inverse topological ordering of the nodes in (V, E), i.e.,
an ordering such that ∀i, j. (E(vi , v j ) ⇒ i > j). We inductively construct a sequence of
formulae I1 , I2 , . . . , In , such that for every i ∈ {1, . . . , n} the following properties hold:
 1. the following conjunction is unsatisfiable:
        ^                                                                                  
           {Ik | k ≤ i, ∀ j. (E(v j , vk ) ⇒ j > i)} ∧ φ(vi+1 ) ∧ φ(vi+2 ) ∧ · · · ∧ φ(vn )       (1)

 2. the following entailment holds:
                                                              ^
                                                φ(vi ) ∧                  I j |= Ii
                                                           (vi ,v j )∈E

 3. every non-logical symbol in Ii occurs both in a formula φ(w) with E ∗ (vi , w), and in
    a formula φ(w′ ) with ¬E ∗ (vi , w′ ).
   Assume that the formulae I1 , I2 , . . . , Ii have been constructed, for i ∈ {0, . . . , n − 1}.
We then derive the next interpolant Ii+1 by solving the binary interpolation problem
                     ^                 
      φ(vi+1 ) ∧                   Ij       ∧
                   E(vi+1 ,v j )
                    ^                                                                         
                      {Ik | k ≤ i, ∀ j. (E(v j , vk ) ⇒ j > i + 1)} ∧ φ(vi+2 ) ∧ · · · ∧ φ(vn ) (2)

That is, we construct Ii+1 so that the following entailments hold:
                 ^
      φ(vi+1 ) ∧       I j |= Ii+1 ,
                       E(vi+1 ,v j )
         ^
             {Ik | k ≤ i, ∀ j. (E(v j , vk ) ⇒ j > i + 1)} ∧ φ(vi+2 ) ∧ · · · ∧ φ(vn ) |= ¬Ii+1

Furthermore, Ii+1 only contains non-logical symbols that are common to the left and the
right side of the conjunction.
    Note that (2) is equivalent to (1), therefore unsatisfiable, and a well-formed interpo-
lation problem. It is also easy to see that the properties 1–3 hold for Ii+1 . Also, we can
easily verify that the labelling function I : vi 7→ Ii is a solution for the tree interpolation
problem defined by (V, E) and φ.                                                              ⊔
                                                                                              ⊓
10        Rümmer, Hojjat, Kuncak

Tree interpolation as tree-like Horn clauses. The encoding of a tree interpolation prob-
lem as a tree-like set of Horn clauses is very similar to the encoding for inductive se-
quences of interpolants. We introduce a fresh relation symbol pv for each node v ∈ V
of a tree interpolation problem (V, E), φ, assuming that for each v ∈ V the vector x̄v =
S                     S
  E∗ (v,w) fv(φ(w)) ∩ ¬E∗ (v,w) fv(φ(w)) represents the set of variables that can occur in the
interpolant I(v). The interpolation problem is then represented by the following clauses:
                                       n        ^                             o
                   p0 ( x̄0 ) → false,   φ(v) ∧       pw ( x̄w ) → pv ( x̄v )
                                                                                 v∈V
                                                    (v,w)∈E


Tree-like Horn clauses as tree interpolation. Suppose HC is a finite, recursion-free, and
tree-like set of Horn clauses. We can solve the system of Horn clauses by computing
a tree interpolant for every connected component of the →HC -graph. As before, we
first normalise the Horn clauses by fixing, for every relation symbol p, a unique vector
of variables x̄ p , and rewriting HC such that p only occurs in the form p( x̄ p ). We also
ensure that every variable x that is not argument of a relation symbol occurs in at most
one clause. The tree interpolation graph (V, E) is then defined by choosing the set V =
R ∪ {false} of relation symbols as nodes, and the child relation E(p, q) to hold whenever
p occurs as head, and q within the body of a clause. The labelling function φ is defined
by φ(p) = C whenever there is a clause with head symbol p and constraint C, and
φ(p) = false if p does not occur as head of any clause.

Example 1. We consider a subset of the Horn clauses given in Fig. 2:
  (1)    r1(X, Res) ← true
  (2)    r2(X’, Res) ← r1(X, Res) ∧ X’ ≥ 0
  (3)    r3(X, Res’) ← r2(X, Res) ∧ rf(X, Res’)
  (5)    false        ← r3(X, Res) ∧ Res , X + 1
  (6)    r5(N, Rec, Tmp) ← true
  (9)    r8(N, Rec, Tmp) ← r5(N, Rec, Tmp) ∧ N ≤ 0
  (11)   r9(N, Rec’, Tmp) ← r8(N, Rec, Tmp) ∧ Rec’ = 1
  (12)   rf (N, Rec)      ← r9(N, Rec, Tmp)

     Note that this recursion-free subset of the clauses is body-disjoint and head-disjoint,
and thus tree-like. Since the complete set of clauses in Fig. 2 is solvable, also any subset
is; in order to compute a (syntactic) solution of the clauses, we set up the corresponding
tree interpolation problem. Fig. 4 shows the tree with the labelling φ to be interpolated
(in grey), as well as the head literals of the clauses generating the nodes of the tree. A
tree interpolant solving the interpolation problem is given in Fig. 5. The tree interpolant
can straightforwardly be mapped to a solution of the original tree-like Horn, for instance
we set r8 (n8 , rec8 , tmp8 ) = (n8 ≤ 0) and r9 (n9 , rec9 , tmp9 ) = (n9 ≤ −1 ∨ (rec9 = 1 ∧ n9 =
0)).


Symmetric Interpolants A special case of tree interpolants, symmetric interpolants,
was introduced in [23]. Symmetric interpolants are equivalent to tree interpolants with
a flat tree structure (V, E), i.e., V = {root, v1 , . . . , vn }, where the nodes v1 , . . . , vn are the
direct children of root.
         The Relationship between Craig Interpolation and Recursion-Free Horn Clauses              11

                                                         r5 (n5 , rec5 , tmp5 ):
                                                                   true


                                                        r8 (n8 , rec8 , tmp8 ):
                                          n8 = n5 ∧ n8 ≤ 0 ∧ rec8 = rec5 ∧ tmp8 = tmp5


                     r1 (x1 , res1 ):                     r9 (n9 , rec9 , tmp9 ):
                          true                    n9 = n8 ∧ rec9 = 1 ∧ tmp9 = tmp8


                     r2 (x2 , res2 ):                       r f (n f , rec f ):
                 x2 ≥ 0 ∧ res2 = res1                  n f = n9 ∧ rec f = rec9


                                         r3 (x3 , res3 ):
                               x3 = x2 ∧ x3 = n f ∧ res3 = rec f


                                             false:
                                         res3 , x3 + 1



                   Fig. 4. Tree interpolation problem for the clauses in Example 1


5.4 Restricted (and Unrestricted) DAG Interpolants [1]
Restricted DAG interpolants are a further generalisation of inductive sequence of inter-
polants, introduced for the purpose of reasoning about multiple paths in a program si-
multaneously [1]. Suppose (V, E, en, ex) is a finite connected DAG with entry node en ∈
V and exit node ex ∈ V, further LE : E → Constr a labelling of edges with constraints,
and LV : V → Constr a labelling of vertices. A restricted DAG interpolant is a mapping
I : V → Constr with
 1. I(en) = true, I(ex) = false,
 2. for all (v, w) ∈ E the entailment I(v) ∧ LV (v) ∧ LE (v, w) |= I(w) ∧ LV (w) holds, and
 3. for all v ∈ V it is the case that4
                                 [                   [                   
                    fv(I(v)) ⊆         fv(LE (a, v)) ∩         fv(LE (v, a)) .
                                        (a,v)∈E                     (v,a)∈E

    The UFO verification system [3] is able to compute DAG interpolants, based on
the interpolation functionality of MathSAT [8]. We can observe that DAG interpolants
(despite their name) are incomparable in expressiveness to tree interpolation. This is
 4
     The definition of DAG interpolants in [1, Def. 4] implies that fv(I(v)) = ∅ for every inter-
     polant I(v), v ∈ V, i.e., only trivial interpolants are allowed. We assume that this is a mistake
     in [1, Def. 4], and corrected the definition as shown here.
12      Rümmer, Hojjat, Kuncak

                                                            true


                                                        n8 ≤ 0


                                            n9 ≤ −1 ∨ (rec9 = 1 ∧ n9 = 0)


                       x2 ≥ 0               n f ≤ −1 ∨ (rec f = 1 ∧ n f = 0)


                                     res3 = x3 + 1


                                          false


              Fig. 5. Tree interpolant solving the interpolation problem in Fig. 4


because DAG interpolants correspond to linear Horn clauses, and might have shared
relation symbol in bodies, while tree interpolants correspond to possibly nonlinear tree-
like Horn clauses, but do not allow shared relation symbols in bodies. Nevertheless, it
is possible to reduce DAG interpolants to tree interpolants, but only at the cost of a
potentially exponential growth in the number of clauses.

Encoding of restricted DAG interpolants as linear Horn clauses. For every v ∈ V, let
                            [                  [                  
                 { x̄v } =       fv(LE (a, v)) ∩       fv(LE (v, a))
                                (a,v)∈E                      (v,a)∈E

be the variables allowed in the interpolant to be computed for v, and pv be a fresh
relation symbol of arity | x̄v |. The interpolation problem is then defined by the following
set of linear Horn clauses:

        For each (v, w) ∈ E:         LV (v) ∧ LE (v, w) ∧ pv ( x̄v ) → pw ( x̄w ),
                                     LV (v) ∧ ¬LV (w) ∧ LE (v, w) ∧ pv ( x̄v ) → false,
             For en, ex ∈ V:         true → pen ( x̄en ),          pex ( x̄ex ) → false

Encoding of linear Horn clauses as DAG interpolants. Suppose HC is a finite, recursion-
free, and linear set of Horn clauses. We can solve the system of Horn clauses by com-
puting a DAG interpolant for every connected component of the →HC -graph. As in
Sect. 5.2, we normalise Horn clauses by fixing a unique vector x̄ p of argument vari-
ables for each relation symbol p, and ensure that every non-argument variable x occurs
in at most one clause. We also assume that multiple clauses C ∧ p( x̄ p ) → q( x̄q ) and
D ∧ p( x̄ p ) → q( x̄q ) with the same relation symbols are merged to (C ∨ D) ∧ p( x̄ p ) →
q( x̄q ).
      The Relationship between Craig Interpolation and Recursion-Free Horn Clauses          13

    Let {p1 , . . . , pn } be all relation symbols of one connected component. We then define
the DAG interpolation problem (V, E, en, ex), LE , LV by

 – the vertices V = {p1 , . . . , pn } ∪ {en, ex}, including two fresh nodes en, ex,
 – the edge relation

                E =     {(p, q) | there is a clause C ∧ p( x̄ p ) → q( x̄q ) ∈ HC}
                      ∪ {(en, p) | there is a clause D → p( x̄ p ) ∈ HC}
                      ∪ {(p, ex) | there is a clause E ∧ p( x̄ p ) → false ∈ HC} ,

 – for each (v, w) ∈ E, the edge labelling
                   
                   
                   
                   
                    C ∧ x̄v = x̄v ∧ x̄w = x̄w    if C ∧ v( x̄v ) → w( x̄w ) ∈ HC
                   
     LE (v, w) =    D ∧ x̄w = x̄w                if v = en and D → w( x̄w ) ∈ HC
                   
                   
                   
                   
                   E ∧ x̄v = x̄v
                                                 if w = ex and E ∧ v( x̄v ) → false ∈ HC

   Note that the labels include equations like x̄v = x̄v to ensure that the right variables
   are allowed to occur in interpolants.
 – for each v ∈ V, the node labelling LV (v) = true.

By checking the definition of DAG interpolants, it can be verified that every interpolant
solving the problem (V, E, en, ex), LE , LV is also a solution of the linear Horn clauses.


5.5 Disjunctive Interpolants [27]

Disjunctive interpolants were introduced in [27] as a generalisation of tree interpolants.
Disjunctive interpolants resemble tree interpolants in the sense that the relationship of
the components of an interpolant is defined by a tree; in contrast to tree interpolants,
however, this tree is an and/or-tree: branching in the tree can represent either conjunc-
tions or disjunctions. Disjunctive interpolants correspond to sets of body-disjoint Horn
clauses; in this representation, and-branching is encoded by clauses with multiple body
literals (like with tree interpolants), while or-branching is interpreted as multiple clauses
sharing the same head symbol. For a detailed account on disjunctive interpolants, we
refer the reader to [27].
     The solution of body-disjoint Horn clauses can be computed by solving a sequence
of tree-like sets of Horn clauses:

Lemma 2. Let HC be a finite set of recursion-free body-disjoint Horn clauses. HC
has a syntactic/semantic solution if and only if every maximum tree-like subset of HC
has a syntactic/semantic solution.

Proof. We outline direction “⇐” for syntactic solutions. Solving the tree-like subsets of
HC yields, for each relation symbol p ∈ R, a set SC p of solution constraints. A global
solution of HC can be constructed by forming a positive Boolean combination of the
constraints in SC p for each p ∈ R.                                                    ⊔
                                                                                       ⊓
14          Rümmer, Hojjat, Kuncak

Example 2. We consider a recursion-free unwinding of the Horn clauses in Fig. 2. To
make the set of clauses body-disjoint, the clause (6), (9), (11), (12) were duplicated,
introducing primed copies of all relation symbols involved. The clauses are not head-
disjoint, since (10) and (11) share the same head symbol:

  (1)      r1(X, Res) ←        true
  (2)      r2(X’, Res) ←       r1(X, Res) ∧ X’ ≥ 0
  (3)      r3(X, Res’) ←       r2(X, Res) ∧ rf(X, Res’)
  (5)      false       ←       r3(X, Res) ∧ Res , X + 1

  (6)      r5(N, Rec, Tmp) ←        true
  (7)      r6(N, Rec, Tmp) ←        r5(N, Rec, Tmp) ∧ N > 0
  (8)      r7(N, Rec, Tmp’) ←       r6(N, Rec, Tmp) ∧ rf’(N − 1, Tmp’)
  (9)      r8(N, Rec, Tmp) ←        r5(N, Rec, Tmp) ∧ N ≤ 0
  (10)     r9(N, Rec’, Tmp) ←       r7(N, Rec, Tmp) ∧ Rec’ = Tmp + 1
  (11)     r9(N, Rec’, Tmp) ←       r8(N, Rec, Tmp) ∧ Rec’ = 1
  (12)     rf (N, Rec)      ←       r9(N, Rec, Tmp)

  (6’)          r5 ’( N, Rec, Tmp) ←    true
  (9’)          r8 ’( N, Rec, Tmp) ←    r5’(N, Rec, Tmp) ∧ N ≤ 0
  (11’)         r9 ’( N, Rec’, Tmp) ←   r8’(N, Rec, Tmp) ∧ Rec’ = 1
  (12’)         rf ’( N, Rec)       ←   r9’(N, Rec, Tmp)


There are two maximum tree-like subsets: T 1 = {(1), (2), (3), (5), (6), (9), (11), (12)},
and T 2 = {(1), (2), (3), (5), (6), (7), (8), (10), (12), (6′), (9′ ), (11′), (12′)}. The subset T 1
has been discussed in Example 1. In the same way, it is possible to construct a solution
for T 2 by solving a tree interpolation problem. The two solutions can be combined to
construct a solution of T 1 ∪ T 2 :


                      T1                         T2                         T1 ∪ T2
r1 (x, r)             true                       true                       true
r2 (x, r)             x≥0                        true                       x≥0
r3 (x, r)             r = x+1                    r = x+1                    r = x+1
r5 (n, c, t)          true                       true                       true
r6 (n, c, t)          −                          n≥1                        n≥1
r7 (n, c, t)          −                          t=n                        t=n
r8 (n, c, t)          n≤0                        −                          n≤0
r9 (n, c, t)          n ≤ −1 ∨ (c = 1 ∧ n = 0)   c= n+1                     n ≤ −1 ∨ c = n + 1
r f (n, c)            n ≤ −1 ∨ (c = 1 ∧ n = 0)   c= n+1                     n ≤ −1 ∨ c = n + 1
r5′ (n, c, t)         −                          true                       true
r8′ (n, c, t)         −                          n≤0                        n≤0
r9′ (n, c, t)         −                          n ≤ −1 ∨ (c = 1 ∧ n = 0)   n ≤ −1 ∨ (c = 1 ∧ n = 0)
r′f (n, c, t)         −                          n ≤ −1 ∨ (c = 1 ∧ n = 0)   n ≤ −1 ∨ (c = 1 ∧ n = 0)


    In particular, the disjunction of the two interpretations of r9 (n, c, t) has to be used,
in order to satisfy both (10) and (11) (similarly for r f (n, c)). In contrast, the conjunction
of the interpretations of r2 (n, c, t) is needed to satisfy (3).
      The Relationship between Craig Interpolation and Recursion-Free Horn Clauses                    15




                                                                                        co-NEXPTIME
                                                      General recursion-free


                                                                      Head-disjoint


   (Restricted) DAG interpolation                 Linear


              Disjunctive interpolation                    Body-disjoint




                                                                                        co-NP
                 Tree interpolation                                     Tree-like


           Inductive interpolant sequences         Linear tree-like


                Binary interpolation

                 Craig interpolation               Recursion-free Horn clauses



Fig. 6. Relationship between different forms of Craig interpolation, and different fragments of
recursion-free Horn clauses. An arrow from A to B expresses that problem A is (strictly) sub-
sumed by B. The complexity classes “co-NP” and “co-NEXPTIME” refer to the problem of
checking solvability of Horn clauses over quantifier-free Presburger arithmetic.



6 The Complexity of Recursion-free Horn Clauses

We give an overview of the considered fragments of recursion-free Horn clauses, and
the corresponding interpolation problem, in Fig. 6. The diagram also shows the com-
plexity of deciding (semantic or syntactic) solvability of a set of Horn clauses, for Horn
clauses over the constraint language of quantifier-free Presburger arithmetic. Most of
the complexity results occur in [27], but in addition we use the following two observa-
tions:

Lemma 3. Semantic solvability of recursion-free linear Horn clauses over the con-
straint language of quantifier-free Presburger arithmetic is in co-NP.

Proof. A set HC of recursion-free linear Horn clauses is solvable if and only if the
expansion exp(HC) is unsatisfiable [27]. For linear clauses, exp(HC) is a disjunction of
(possibly) exponentially many formulae, each of which is linear in the size of exp(HC).
Consequently, satisfiability of exp(HC) is in NP, and unsatisfiability in co-NP.      ⊔
                                                                                      ⊓

Lemma 4. Semantic solvability of recursion-free head-disjoint Horn clauses over the
constraint language of quantifier-free Presburger arithmetic is co-NEXPTIME-hard.
16         Rümmer, Hojjat, Kuncak

Proof. The proof given in [27] for co-NEXPTIME-hardness of recursion-free Horn
clauses over quantifier-free Presburger arithmetic can be adapted to only require head-
disjoint clauses. This is because a single execution step of a non-deterministic Turing
machine can be expressed as quantifier-free Presburger formula.                       ⊔
                                                                                      ⊓


7 Beyond Recursion-free Horn Clauses

It is natural to ask whether the considerations of the last sections also apply to clauses
that are not Horn clauses (i.e., clauses that can contain multiple positive literals), pro-
vided the clauses are “recursion-free.” Is it possible, like for Horn clauses, to com-
pute solutions of recursion-free clauses in general by means of computing Craig inter-
polants?
     To investigate the situation for clauses that are not Horn, we first have to generalise
the concept of clauses being recursion-free: the definition provided in Sect. 4, formu-
lated with the help of the dependence relation →HC , only applies to Horn clauses. For
non-Horn clauses, we instead choose to reason about the absence of infinite proposi-
tional resolution derivations. Because the proposed algorithms [27] for solving recursion-
free sets of Horn clauses all make use of exhaustive expansion or inlining, i.e., the con-
struction of all derivations for a given set of clauses, the requirement that no infinite
derivations exist is fundamental.5
     Somewhat surprisingly, we observe that all sets of clauses without infinite deriva-
tions have the shape of Horn clauses, up to renaming of relation symbols. This means
that procedures handling Horn clauses cover all situations in which we can hope to
compute solutions with the help of Craig interpolation.
    Since constraints and relation symbol arguments are irrelevant for this observation,
the following results are entirely formulated on the level of propositional logic:

 – a propositional literal is either a Boolean variable p, q, r (positive literals), or the
   negation ¬p, ¬q, ¬r of a Boolean variable (negative literals).
 – a propositional clause is a disjunction p ∨ ¬q ∨ p of literals. The multiplicity of a
   literal is important, i.e., clauses could alternatively be represented as multi-sets of
   literals.
 – a Horn clause is a clause that contains at most one positive literal.
 – given a set HC of Horn clauses, we define the dependence relation →HC on Boolean
   variables by setting p →HC q if and only if there is a clause in HC in which p
   occurs positively, and q negatively (like in Sect. 4). The set HC is called recursion-
   free if →HC is acyclic.

   We can now generalise the notion of a set of clauses being “recursion-free” to non-
Horn clauses:
 5
     We do not take subsumption between clauses, or loops in derivations into account. This means
     that a set of clauses might give rise to infinite derivations even if the set of derived clauses is
     finite. It is conceivable that notions of subsumption, or more generally the application of ter-
     minating saturation strategies [12], can be used to identify more general fragments of clauses
     for which syntactic solutions can effectively be computed. This line of research is future work.
         The Relationship between Craig Interpolation and Recursion-Free Horn Clauses             17

Definition 3. A set C of propositional clauses has the termination property if no infinite
sequence c0 , c1 , c2 , c3 , . . . of clauses exists, such that
  – c0 ∈ C is an input clause, and
  – for each i ≥ 1, the clause ci is derived by means of binary resolution from ci−1 and
    an input clause, using the rule

                                         C∨p      D ∨ ¬p
                                                         .
                                                C∨D

Lemma 5. A finite set HC of Horn clauses has the termination property if and only if
it is recursion-free.
Proof. “⇐” The acyclic dependence relation →HC induces a strict well-founded or-
der < on Boolean variables: q →HC p implies p < q. The order < induces a well-
founded order ≪ on Horn clauses:

                   (p ∨ C) ≪ (q ∨ D) ⇔ p > q or (p = q and C <ms D)
                        C ≪ (q ∨ D) ⇔ true
                               C ≪ D ⇔ C <ms D

where C, D only contain negative literals, and <ms is the (well-founded) multi-set ex-
tension of < [11].
    It is easy to see that a clause C ∨ D derived from two Horn clauses C ∨ p and D ∨ ¬p
using the resolution rule is again Horn, and (C ∨ D) ≪ (C ∨ p) and (C ∨ D) ≪ (D ∨ ¬p).
The well-foundedness of ≪ implies that any sequence of clauses as in Def. 3 is finite.
    “⇒” If the dependence relation →HC has a cycle, we can directly construct a non-
terminating sequence c0 , c1 , c2 , . . . of clauses.                                  ⊔
                                                                                       ⊓
Definition 4 (Renamable-Horn [20]). If A is a set of Boolean variables, and C is a
set of clauses, then rA (C) is the result of replacing in C every literal whose Boolean
variable is in A with its complement. C is called renamable-Horn if there is some set A
of Boolean variables such that rA (C) is Horn.
Theorem 2. If a finite set C of clauses has the termination property, then it is renamable-
Horn.
Proof. Suppose C is formulated over the (finite) set p1 , p2 , . . . , pn of Boolean variables.
We construct a graph (V, E), with V = {p1 , p2 , . . . , pn , ¬p1 , ¬p2 , . . . , ¬pn } being the set
of all possible literals, and (l, l′ ) ∈ E if and only if there is a clause ¬l ∨ l′ ∨ C ∈ C (that
means, a clause containing the literal l′ , and the literal l with reversed sign).6
     The graph (V, E) is acyclic. To see this, suppose there is a cycle l1 , l2 , . . . , lm , lm+1 =
l1 in (V, E). Then there are clauses c1 , c2 , . . . , cm ∈ C such that each ci contains the liter-
als ¬li and li+1 . We can then construct an infinite sequence c1 = d0 , d1 , d2 , . . . of clauses,
where each di (for i > 1) is obtained by resolving di−1 with c(i mod m)+1 , contradicting the
assumption that C has the termination property.
 6
     This graph could equivalently be defined as the implication graph of the 2-sat problem intro-
     duced in [20], as a way of characterising whether a set of clauses is Horn.
18       Rümmer, Hojjat, Kuncak

     Since (V, E) is acyclic, there is a strict total order < on V that is consistent with E,
i.e., (l, l′ ) ∈ E implies l < l′ .
     Claim: if p < ¬p for every Boolean variable p ∈ {p1 , p2 , . . . , pn }, then C is Horn.
     Proof of the claim: suppose a non-Horn clause pi ∨ p j ∨ C ∈ C exists (with i , j).
Then (¬pi , p j ) ∈ E and (¬p j , pi ) ∈ E, and therefore ¬pi < p j and ¬p j < pi . Then also
¬pi < pi or ¬p j < p j , contradicting the assumption that p < ¬p for every Boolean
variable p.
     In general, choose A = {pi | i ∈ {1, . . . , n}, ¬pi < pi }, and consider the set rA (C) of
clauses. The set rA (C) is Horn, since changing the sign of a Boolean variable p ∈ A
has the effect of swapping the nodes p, ¬p in the graph (V, E). Therefore, the new
graph (V, E ′ ) has to be compatible with a strict total order < such that p < ¬p for
every Boolean variable p, satisfying the assumption of the claim above.                       ⊔
                                                                                              ⊓

Example 3. We consider the following set of clauses:

                    C = {¬a ∨ s, a ∨ ¬p, p ∨ ¬b, b ∨ p ∨ r, ¬p ∨ q}

By constructing all possible derivations, it can be shown that the set has the termination
property. The graph (V, E), as constructed in the proof, is:
                                                     s

                                         q           a

                                               p              r

                                        b             ¬b

                                ¬r            ¬p

                                      ¬a              ¬q

                                      ¬s

A strict total order that is compatible with the graph is:

                ¬s < ¬q < ¬r < ¬a < ¬p < b < ¬b < r < p < q < a < s

From the order we can read off that we need to rename the variables A = {s, q, r, a, p}
in order to obtain a set of Horn clauses:

               rA (C) = {a ∨ ¬s, ¬a ∨ p, ¬p ∨ ¬b, b ∨ ¬p ∨ ¬r, p ∨ ¬q}


References
 1. A. Albarghouthi, A. Gurfinkel, and M. Chechik. Craig interpretation. In SAS, 2012.
 2. A. Albarghouthi, A. Gurfinkel, and M. Chechik. Whale: An interpolation-based algorithm
    for inter-procedural verification. In VMCAI, pages 39–55, 2012.
      The Relationship between Craig Interpolation and Recursion-Free Horn Clauses          19

 3. A. Albarghouthi, Y. Li, A. Gurfinkel, and M. Chechik. Ufo: A framework for abstraction-
    and interpolation-based software verification. In CAV, pages 672–678, 2012.
 4. T. Ball, A. Podelski, and S. K. Rajamani. Relative completeness of abstraction refinement
    for software model checking. In TACAS’02, volume 2280 of LNCS, page 158, 2002.
 5. N. Bjørner, K. McMillan, and A. Rybalchenko. Program verification as satisfiability
    modulo theories. In SMT Workshop at IJCAR, 2012.
 6. M. P. Bonacina and M. Johansson. On interpolation in automated theorem proving.
    (submitted), 2012.
 7. A. Brillout, D. Kroening, P. Rümmer, and T. Wahl. An interpolating sequent calculus for
    quantifier-free Presburger arithmetic. Journal of Automated Reasoning, 47:341–367, 2011.
 8. A. Cimatti, A. Griggio, and R. Sebastiani. Efficient generation of Craig interpolants in
    satisfiability modulo theories. ACM Trans. Comput. Log., 12(1):7, 2010.
 9. W. Craig. Linear reasoning. A new form of the Herbrand-Gentzen theorem. The Journal of
    Symbolic Logic, 22(3):250–268, September 1957.
10. L. de Moura and N. Bjørner. Z3: An efficient SMT solver. In TACAS, pages 337–340.
    Springer-Verlag, 2008.
11. N. Dershowitz and Z. Manna. Proving termination with multiset orderings. Commun. ACM,
    22(8):465–476, 1979.
12. C. Fermüller, A. Leitsch, U. Hustadt, and T. Tammet. Resolution decision procedures. In
    A. Robinson and A. Voronkov, editors, Handbook of Automated Reasoning, chapter 25,
    pages 1791–1850. Elsevier, 2001.
13. S. Graf and H. Saidi. Construction of abstract state graphs with PVS. In CAV, pages 72–83,
    1997.
14. S. Grebenshchikov, N. P. Lopes, C. Popeea, and A. Rybalchenko. Synthesizing software
    verifiers from proof rules. In PLDI, 2012.
15. A. Gupta, C. Popeea, and A. Rybalchenko. Predicate abstraction and refinement for
    verifying multi-threaded programs. In POPL, 2011.
16. A. Gupta, C. Popeea, and A. Rybalchenko. Solving recursion-free Horn clauses over
    LI+UIF. In APLAS, pages 188–203, 2011.
17. M. Heizmann, J. Hoenicke, and A. Podelski. Nested interpolants. In POPL, 2010.
18. T. A. Henzinger, R. Jhala, R. Majumdar, and K. L. McMillan. Abstractions from proofs. In
    POPL, pages 232–244. ACM, 2004.
19. A. Lal, S. Qadeer, and S. K. Lahiri. Corral: A solver for reachability modulo theories. In
    CAV, 2012.
20. H. R. Lewis. Renaming a set of clauses as a Horn set. J. ACM, 25(1):134–135, Jan. 1978.
21. K. L. McMillan. iZ3 documentation.
    http://research.microsoft.com/en-us/um/redmond/projects/z3/iz3documentation.html.
22. K. L. McMillan. Interpolation and SAT-based model checking. In CAV, 2003.
23. K. L. McMillan. Applications of craig interpolation to model checking. In J. Marcinkowski
    and A. Tarlecki, editors, CSL, volume 3210 of Lecture Notes in Computer Science, pages
    22–23. Springer, 2004.
24. K. L. McMillan. Lazy abstraction with interpolants. In CAV, 2006.
25. K. L. McMillan and A. Rybalchenko. Solving constrained Horn clauses using interpolation.
    Technical Report MSR-TR-2013-6, Jan. 2013.
    http://research.microsoft.com/apps/pubs/default.aspx?id=180055.
26. M. Méndez-Lojo, J. A. Navas, and M. V. Hermenegildo. A flexible, (c)lp-based approach to
    the analysis of object-oriented programs. In LOPSTR, pages 154–168, 2007.
27. P. Rümmer, H. Hojjat, and V. Kuncak. Disjunctive Interpolants for Horn-Clause Verification
    (Extended Technical Report). ArXiv e-prints, Jan. 2013. http://arxiv.org/abs/1301.4973.
28. O. Sery, G. Fedyukovich, and N. Sharygina. Interpolation-based function summaries in
    bounded model checking. In Haifa Verification Conference (HVC), Haifa, 2011. Springer.
20       Rümmer, Hojjat, Kuncak

29. P. Suter, A. S. Köksal, and V. Kuncak. Satisfiability modulo recursive programs. In Static
    Analysis Symposium (SAS), 2011.
30. M. Taghdiri and D. Jackson. Inferring specifications to detect errors in code. Autom. Softw.
    Eng., 14(1):87–121, 2007.
