                                            Disjunctive Interpolants for Horn-Clause Verification
                                                        (Extended Technical Report)

                                                        Philipp Rümmer1 , Hossein Hojjat2 , and Viktor Kuncak2
                                                                         1
                                                                           Uppsala University, Sweden
                                                          2
                                                              Swiss Federal Institute of Technology Lausanne (EPFL)
arXiv:1301.4973v1 [cs.LO] 21 Jan 2013




                                               Abstract. One of the main challenges in software verification is efficient and
                                               precise compositional analysis of programs with procedures and loops. Interpo-
                                               lation methods remains one of the most promising techniques for such verifica-
                                               tion, and are closely related to solving Horn clause constraints. We introduce a
                                               new notion of interpolation, disjunctive interpolation, which solve a more general
                                               class of problems in one step compared to previous notions of interpolants, such
                                               as tree interpolants or inductive sequences of interpolants. We present algorithms
                                               and complexity for construction of disjunctive interpolants, as well as their use
                                               within an abstraction-refinement loop. We have implemented Horn clause verifi-
                                               cation algorithms that use disjunctive interpolants and evaluate them on bench-
                                               marks expressed as Horn clauses over the theory of integer linear arithmetic.


                                        1    Introduction
                                        Software model checking has greatly benefited from the combination of a number
                                        of seminal ideas: automated abstraction through theorem proving [13], exploration of
                                        finite-state abstractions, and counterexample-driven refinement [3]. Even though these
                                        techniques can be viewed independently, the effectiveness of verification has been con-
                                        sistently improving by providing more sophisticated communication between these
                                        steps. Often, carefully chosen search aspects are being pushed into a learning-enabled
                                        constraint solver, resulting in better overall verification performance. An essential ad-
                                        vance was to use interpolants derived from unsatisfiability proofs to refine the abstrac-
                                        tion [18]. In recent years, we have seen significant progress in interpolating methods
                                        for different logical constraints [5, 8, 9, 22], and a wealth of more general forms of in-
                                        terpolation [1, 17, 22]. In this paper we identify a new notion, disjunctive interpolants,
                                        which are more general than tree interpolants and inductive sequences of interpolants.
                                        Like tree interpolation [17, 22], a disjunctive interpolation query is a tree-shaped con-
                                        straint specifying the interpolants to be derived; however, in disjunctive interpolation,
                                        branching in the tree can represent both conjunctions and disjunctions. We present an
                                        algorithm for solving the interpolation problem, relating it to a subclass of recursion-
                                        free Horn clauses. We then consider solving general recursion-free Horn clauses and
                                        show that this problem is solvable whenever the logic admits interpolation. We estab-
                                        lish tight complexity bounds for solving recursion-free Horn clauses for propositional
                                        logic (PSPACE) and for integer linear arithmetic (co-NEXPTIME). In contrast, the dis-
                                        junctive interpolation problem remains in coNP for these logics. We also show how
                                        to use solvers for recursion-free Horn clauses to verify recursive Horn clauses using
2       Rümmer, Hojjat, Kuncak

counterexample-driven predicate abstraction. We present an algorithm and experimen-
tal results on publicly available benchmarks.


1.1   Related Work

There is a long line of research on Craig interpolation methods, and generalised forms
of interpolation, tailored to verification. For an overview of interpolation in the pres-
ence of theories, we refer the reader to [8, 9]. Binary Craig interpolation for impli-
cations A → C goes back to [10], was carried over to conjunctions A ∧ B in [23],
and generalised to inductive sequences of interpolants in [18, 24]. The concept of tree
interpolation, strictly generalising inductive sequences of interpolants, is presented in
the documentation of the interpolation engine iZ3 [22]; the computation of tree inter-
polants by computing a sequence of binary interpolants is also described in [17]. In
this paper, we present a new form of interpolation, disjunctive interpolation, which is
strictly more general than sequences of interpolants and tree interpolants. Our imple-
mentation supports Presburger arithmetic, including divisibility constraints [8], which
is rarely supported by existing tools, yet helpful in practice [19].
     A further generalisation of inductive sequences of interpolants are restricted DAG
interpolants [1], which also include disjunctiveness in the sense that multiple paths
through a program can be handled simultaneously. Disjunctive interpolants are incom-
parable in power to restricted DAG interpolants, since the former does not handle in-
terpolation problems in the form of DAGs, while the latter does not subsume tree inter-
polation. A combination of the two kinds of interpolants (“disjunctive DAG interpola-
tion”) is strictly more powerful (and harder) than disjunctive interpolation, see Sect. 5.1
for a complexity-theoretic analysis. We discuss techniques and heuristics to practically
handle shared sub-trees in disjunctive interpolation, extending the benefits of DAG in-
terpolation to recursive programs.
     Inter-procedural software model checking with interpolants has been an active area
of research. In the context of predicate abstraction, it has been discussed how well-
scoped invariants can be inferred [18] in the presence of function calls. Based on the
concept of Horn clauses, a predicate abstraction-based algorithm for bottom-up con-
struction of function summaries was presented in [14]. Verification of programs with
procedures is described in [17] (using nested word automata) as well as in [2].
     The use of Horn clauses as intermediate representation for verification was pro-
posed in [15], with the verification of concurrent programs as main application. The
underlying procedure for solving sets of recursion-free Horn clauses, over the com-
bined theory of linear rational arithmetic and uninterpreted functions, was presented
in [16]. A range of further applications of Horn clauses, including inter-procedural
model checking, was given in [14]. Horn clauses are also proposed as intermediate/ex-
change format for verification problems in [4], and are natively supported by the SMT
solver Z3 [11]. Our paper extends this work by giving general results about solvability
and computational complexity, independent of any particular calculus. Our experiments
are with linear integer arithmetic, arguably a more faithful model of discrete computa-
tion than rationals [19].
       Disjunctive Interpolants for Horn-Clause Verification (Extended Technical Report)   3


(1)    merge(X,Y,Z) ← X = 0 ∧ Y >= 0 ∧ Z = Y
(2)    merge(X,Y,Z) ← Y = 0 ∧ X >= 0 ∧ Z = X
(3)    merge(X,Y,Z) ← Y1 = Y − 1 ∧ merge(X, Y1, Z1) ∧ Z = Z1 + 1
(4)    merge(X,Y,Z) ← X1 = X − 1 ∧ merge(X1, Y, Z1) ∧ Z = Z1 + 1
(5)    false ← merge(X,Y,Z) ∧ Z > X + Y

Fig. 1. Horn Clauses Abstracting the Merge of Two Sorted Lists and an Assertion on Resulting
Length. Variables are universally quantified in each clause.

(1)     merge(X,Y,Z) ← X = 0 ∧ Y >= 0 ∧ Z = Y
(3’)    merge1(X,Y,Z) ← Y1 = Y − 1 ∧ merge(X, Y1, Z1) ∧ Z = Z1 + 1
(4’)    merge1(X,Y,Z) ← X1 = X − 1 ∧ merge(X1, Y, Z1) ∧ Z = Z1 + 1
(5’)    false ← merge1(X,Y,Z) ∧ Z > X + Y

            Fig. 2. Extended recursion-free approximation of the Horn clauses in Fig. 1.


2      Example: Verification of Recursive Predicates
We start by showing how our approach can verify programs encoded as Horn clauses,
by means of predicate abstraction and a theorem prover for Presburger arithmetic. Fig. 1
shows an example of a system of Horn clauses, generated by a straightforward length
abstraction of a merge operation that accepts two sorted lists and produces a new one
by merging them. Addition of an element increases the resulting length (Z) by one
whereas the processing continues with one of the argument lists shorter. After invoking
such an operation, we wish to check whether it is possible for the resulting length Z to
be more than the sum of the lengths of the argument lists X + Y. In general, we encode
error conditions as Horn clauses with false in their head, and refer to such clauses as
error clauses, although such clauses do not have a special semantic status in our system.
When invoked with these clauses as input, our verification tool automatically identifies
that the definition of merge as the predicate X + Y − Z ≥ 0 gives a solution to these
Horn clauses. In terms of safety (partial correctness), this means that the error condition
cannot be reached.
    Our approach uses counterexample-driven refinement to perform verification. In
this example, the abstraction of Horn clauses starts with a trivial set of predicates, con-
taining only the predicate false, which is assumed to be a valid approximation until
proven otherwise. Upon examining a clause that has a concrete satisfiable formula on
the right-hand side (e.g. X = 0 ∧ Y >= 0 ∧ Z = Y), we rule out false as the approx-
imation of merge. In the absence of other candidate predicates, the approximation of
merge becomes the conjunction of an empty set of predicates, which is true. Using this
approximation the error clause is no longer satisfied. At this point the algorithm checks
whether a true error is reached by directly chaining the clauses involved in comput-
ing the approximation of predicates. This amounts to checking whether the following
recursion-free subset of clauses has a solution:
(1) merge(X,Y,Z) ← X = 0 ∧ Y >= 0 ∧ Z = Y
(5) false ← merge(X,Y,Z) ∧ Z > X + Y

The solution to above problem is any formula I(X, Y, Z) such that
4        Rümmer, Hojjat, Kuncak

I (X,Y,Z) ← X = 0 ∧ Y >= 0 ∧ Z = Y
false ← I(X,Y,Z) ∧ Z > X + Y

This is precisely an interpolant of X = 0∧Y >= 0∧Z = Y and Z > X+Y. If our algorithm
picks the interpolant Z ≤ X + Y, the subsequent check shows it to be a solution and the
program is successfully verified (this is what happens in our current implementation). In
general, however, there is no guarantee about which of the interpolants will be picked,
so another valid solution is P1 (X, Y, Z) ≡ Z = Y ∧ X ≥ 0. For illustration purposes,
suppose P1 is the interpolant picked. The currently considered possible contradiction for
Horn clauses is thereby eliminated, and P1 is added into a list of abstraction predicates
for the relation merge. Because the predicates approximating merge are now updated,
we consider the abstraction of the system in terms of these predicates. Because of the
clause (2), however, P1 is not a conjunct in a valid approximation, which leads us to
consider clauses (2) and (5) and add, for example, P2 (X, Y, Z) ≡ Z = X ∧ Y ≥ 0 as
another predicate in the approximation of merge. Note, however, that both P1 and P2
are ruled out as approximation of clause (3), so the following recursion-free unfolding
is not solved by the approximation so far:
(1)    merge(X,Y,Z) ← X = 0 ∧ Y >= 0 ∧ Z = Y
(3’)   merge1(X,Y,Z) ← Y1 = Y − 1 ∧ merge(X, Y1, Z1) ∧ Z = Z1 + 1
(5’)   false ← merge1(X,Y,Z) ∧ Z > X + Y

This particular problem could be reduced to solving an interpolation sequence, but it is
more natural to think of it simply as a solution for recursion-free Horn clauses. A solu-
tion is an interpretation of the relations merge and merge1 as ternary relations on inte-
gers, such that the clauses are true. Note that this problem could also be viewed as the
computation of tree interpolants, which are also a special case of solving recursion-free
Horn clauses, as are DAG interpolants and a new notion of disjunctive tree interpolants
that we introduce. The general message, in line with [14–16] is that recursion-free
clauses are a perfect fit for counterexample-driven verification: they allow us to provide
the theorem proving procedure with much more information that they can use to refine
abstractions. In fact, we could also provide further recursion-free approximations, such
as in Fig. 2. In the limit, the original set of clauses or its recursive unfoldings are its own
approximations, some of them exact, but the advantage of recursion-free Horn clauses is
that their solvability is decidable under very general conditions. This provides us with a
solid theorem proving building block to construct robust and predictable solvers for the
undecidable recursive case. Our paper describes a new such building block: disjunctive
interpolants, which correspond to a subclass of non-recursive Horn clauses.


3      Formulae and Horn Clauses

Constraint languages. Throughout this paper, we assume that a first-order vocabulary
of interpreted symbols has been fixed, consisting of a set F of fixed-arity function
symbols, and a set P of fixed-arity predicate symbols. Interpretation of F and P is
determined by a class S of structures (U, I) consisting of non-empty universe U, and
a mapping I that assigns to each function in F a set-theoretic function over U, and
to each predicate in P a set-theoretic relation over U. As a convention, we assume
      Disjunctive Interpolants for Horn-Clause Verification (Extended Technical Report)             5

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

Positions. We denote the set of positions in a constraint φ by positions(φ). For instance,
the constraint a ∧ ¬a has 4 positions, corresponding to the sub-formulae a ∧ ¬a, ¬a, and
the two occurrences of a. The sub-formula of a formula φ underneath a position p is
denoted by φ ↓ p, and we write φ[p/ψ] for the result of replacing the sub-formula φ ↓ p
with ψ. Further, we write p ≤ q if position p is above q (that is, q denotes a position
within the sub-formula φ ↓ p), and p < q if p is strictly above q.

Craig interpolation is the main technique used to construct and refine abstractions in
software model checking. A binary interpolation problem is a conjunction A ∧ B of
constraints. A Craig interpolant is a constraint I such that A |= I and B |= ¬I, and
such that fv(I) ⊆ fv(A) ∩ fv(B). The existence of an interpolant implies that A ∧ B is
unsatisfiable. We say that a constraint language has the interpolation property if also
the opposite holds: whenever A ∧ B is unsatisfiable, there is an interpolant I.


3.1    Horn Clauses

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
6        Rümmer, Hojjat, Kuncak

instantiation sol(h) of a Horn clause h is defined by:

 sol C ∧ p1 (t¯1 ) ∧ · · · ∧ pn (t¯n ) → p(t¯) = C ∧ sol(p1 )[t¯1 ] ∧ · · · ∧ sol(pn )[t¯n ] → sol(p)[t¯]
                                              

sol C ∧ p1 (t¯1 ) ∧ · · · ∧ pn (t¯n ) → false = C ∧ sol(p1 )[t¯1 ] ∧ · · · ∧ sol(pn )[t¯n ] → false
                                              

Definition 1 (Solvability). Let HC be a set of Horn clauses over relation symbols R.
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
    Clearly, if a set of Horn clauses is syntactically solvable, then it is also semanti-
cally solvable. The converse is not true in general, because the solution need not be
expressible in the constraint language (see Appendix E for an example).
    A set HC of Horn clauses induces a dependence relation →HC on R, defining
p →HC q if there is a Horn clause in HC that contains p in its head, and q in the
body. The set HC is called recursion-free if →HC is acyclic, and recursive otherwise.
In the next sections we study the solvability problem for recursion-free Horn clauses.
This case is relevant, since solvers for recursion-free Horn clauses form a main compo-
nent of many general Horn-clause-based verification systems [14, 15].


4    Disjunctive Interpolants and Body-Disjoint Horn Clauses
Having defined the classical notions of interpolation and Horn clauses, we now present
our notion of disjunctive interpolants, and the corresponding class of Horn clauses. Our
inspiration are generalized forms of Craig interpolation, such as inductive sequences of
interpolants [18, 24] or tree interpolants [17, 22]. We introduce disjunctive interpolation
as a new form of interpolation that is tailored to the refinement of abstractions in Horn
clause verification, strictly generalising both inductive sequences of interpolants and
tree interpolation. Disjunctive interpolation problems can specify both conjunctive and
disjunctive relationships between interpolants, and are thus applicable for simultaneous
analysis of multiple paths in a program, but also tailored to inter-procedural analysis or
verification of concurrent programs [14].
    Disjunctive interpolation problems correspond to a specific fragment of recursion-
free Horn clauses, namely recursion-free body-disjoint Horn clauses (see Sect. 4.1). The
definition of disjunctive interpolation is chosen deliberately to be as general as possible,
while still avoiding the high computational complexity of solving general systems of
recursion-free Horn clauses. Computational complexity is discussed in Sect. 5.1.
    Disjunctive Interpolants for Horn-Clause Verification (Extended Technical Report)       7

    We introduce disjunctive interpolants as a means of sub-formula abstraction. For
example, given an unsatisfiable constraint φ[α] containing α as a sub-formula in a pos-
itive position, the goal is to find an abstraction α0 such that α |= α0 and α[α0 ] |= false,
and such that α0 only contains variables common to α and φ[true]. Generalizing this to
any number of subformulas, we obtain the following.

Definition 2 (Disjunctive interpolant). Let φ be a constraint, and pos ⊆ positions(φ)
a set of positions in φ that are only underneath the connectives ∧ and ∨. A disjunctive
interpolant is a map I : pos → Constr from positions to constraints such that:

 1. For each position p ∈ pos, with direct children
    {q1 , . . . , qn } = {q ∈ pos | p < q and ¬∃r ∈ pos. p < r < q} we have

                            φ[q1 /I(q1 ), . . . , qn /I(qn )] ↓ p |= I(p) ,
                                                             


 2. For the topmost positions {q1 , . . . , qn } = {q ∈ pos | ¬∃r ∈ pos. r < q} we have

                              φ[q1 /I(q1 ), . . . , qn /I(qn )] |= false ,

 3. For each position p ∈ pos, we have fv(I(p)) ⊆ fv(φ ↓ p) ∩ fv(φ[p/true]).

Example 1. Consider A p ∧ B, with position p pointing to the sub-formula A, and pos =
{p}. The disjunctive interpolants for A ∧ B and pos coincide with the ordinary binary
interpolants for A ∧ B.

Example 2. Consider the formula φ = · · · T 1 p1 ∧ T 2 p2 ∧ T 3 p3 ∧ · · · pn−1 ∧ T n and
                                                                          
positions pos = {p1 , . . . , pn−1 }. Disjunctive interpolants for φ and pos correspond to
inductive sequences of interpolants [18, 24]. Note that we have the entailments
T 1 |= I(p1 ), I(p1 ) ∧ T 2 |= I(p2 ), . . . , I(pn−1 ) ∧ T n |= false.

Example 3. A tree interpolation problem [17,22] is given by a finite directed tree (V, E),
writing E(v, v0 ) to express that the node v0 is a direct child of v, together with a function
φ : V → Constr that labels each node v of the tree with a constraint φ(v). A tree
interpolant is a function I : V → Constr such that 1. I(v0 ) = false for the root node
v0 ∈ V, 2. for any node v ∈ V, the entailment φ(v) ∧ (v,w)∈E I(w) |= I(v), holds, and
                                                            V
3. for any node v ∈ V, every variable in I(v) occurs both in some formula φ(w) for w
such that E ∗ (v, w), and in some formula φ(w0 ) for some w0 such that ¬E ∗ (v, w0 ). (E ∗ is
the reflexive transitive close of E).
    It can be shown that a tree interpolant I exists if and only if v∈V φ(v) is unsatisfi-
                                                                        V
able. Tree interpolation problems [17, 22] correspond to disjunctive interpolation with
a set pos of positions that are only underneath ∧ (and never underneath ∨).

Example 4. We consider the example given in Fig. 2, Sect. 2. To compute a solution
for the Horn clauses, we first expand the Horn clauses into a constraint, by means of
8        Rümmer, Hojjat, Kuncak

exhaustive inlining (see Sect. 5), obtaining a disjunctive interpolation problem:

false { merge1(X, Y, Z) ∧ Z > X + Y
              Y1 = Y − 1 ∧ merge(X, Y1, Z1) ∧ Z = Z1 + 1 
                                                             
                                      ∨                          ∧ Z > X + Y
                                                           
      { 
                   X1 = X − 1 ∧ merge(X1, Y, Z1) ∧ Z = Z1 + 1
                 

          Y1 = Y − 1 ∧ (X = 0 ∧ Y1 >= 0 ∧ Z1 = Y1)q ∧ Z = Z1 + 1 
                                                                              
                                             ∨                                    ∧ Z > X + Y
                                                                            
      { 
                   X1 = X − 1 ∧ (X1 = 0 ∧ Y >= 0 ∧ Z1 = Y)r ∧ Z = Z1 + 1 p
             

In the last formula, the positions p, q, r corresponding to the relation symbol merge1
and the two occurrences of merge are marked. It can be observed that the last formula
is unsatisfiable, and that I = {p 7→ X + Y ≥ Z, q 7→ X + Y1 ≥ Z1, r 7→ X1 + Y ≥ Z1}
is a disjunctive interpolant. A solution for the Horn clauses can be derived from the
interpolant by conjoining the constraints derived for the two occurrences of merge:

      merge1(X, Y, Z) = X + Y ≥ Z,        merge(X, Y, Z) = X + Y ≥ Z ∧ X + Y ≥ Z
                                                           = X+Y ≥Z

Theorem 1. Suppose φ is a constraint, and suppose pos ⊆ positions(φ) is a set of
positions in φ that are only underneath the connectives ∧ and ∨. If Constr is a constraint
language that has the interpolation property, then a disjunctive interpolant I exists for
φ and pos if and only if φ is unsatisfiable.

Proof. “⇒” By means of simple induction, we can derive that φ ↓ p |= I(p) holds for
every disjunctive interpolant I for φ and pos, and for every p ∈ pos. From Def. 2, it then
follows that φ is unsatisfiable.
    “⇐” Suppose φ is unsatisfiable. We encode the disjunctive interpolation problem
into a (conjunctive) tree interpolation problem [17, 22] (also see Example 3) by adding
auxiliary Boolean variables. Wlog, we assume that pos contains the root position root
of φ. The graph of the tree interpolation problem is (pos, E), with the edge relation
E = {(p, q) | p < q and ¬∃r.p < r < q}. For every p ∈ pos, let a p be a fresh Boolean
variable. We label the nodes of the tree using the function φL : pos → Constr. For each
position p ∈ pos, with direct children {q1 , . . . , qn } = {q ∈ pos | E(p, q)} we define
                           
                           φ[q1 /aq1 , . . . , qn /aqn ]
                                                                    if p = root
               φL (p) = 
                           
                           ¬a p ∨ φ[q1 /aq1 , . . . , qn /aqn ] ↓ p otherwise
                                                               

Observe that p∈pos φL (p) is unsatisfiable. As explained in Example 3, a tree inter-
               V
polant IT exists for this labelling function. By construction, for non-root positions p ∈
pos \ {root} the interpolant labelling is equivalent to IT (p) ≡ ¬a p ∨ I p , where I p does
not contain any further auxiliary Boolean variables. We can then construct a disjunctive
interpolant I for the original problem as
                                        
                                        false if p = root
                                        
                               I(p) = 
                                        
                                        I p
                                                otherwise
      Disjunctive Interpolants for Horn-Clause Verification (Extended Technical Report)                        9

To see that I is a disjunctive interpolant, observe that for each position p ∈ pos with
direct children {q1 , . . . , qn } = {q ∈ pos | E(p, q)} the following entailment holds (since
IT is a tree interpolant): φL (p) ∧ (¬aq1 ∨ Iq1 ) ∧ · · · ∧ (¬aqn ∨ Iqn ) |= IT (p)
Via Boolean reasoning this implies: φ[q1 /Iq1 , . . . , qn /Iqn ] ↓ p |= I(p).
                                                                   
                                                                                             t
                                                                                             u

4.1    Solvability of Body-Disjoint Horn Clauses
The relationship between Craig interpolation and (syntactic) solutions of Horn clauses
has been observed in [16]. Disjunctive interpolation corresponds to a specific class of
recursion-free Horn clauses, namely Horn clauses that are body disjoint:
Definition 3. A finite, recursion-free set HC of Horn clauses is body disjoint if for each
relation symbol p there is at most one clause containing p in its body, and every clause
contains p at most once.
An example for body-disjoint clauses is the subset {(1), (2), (5)} of clauses in Fig. 1.
Syntactic solutions of a set HC of body-disjoint Horn clauses can be computed by
solving a disjunctive interpolation problem; vice versa, every disjunctive interpolation
problem can be translated into an equivalent set of body-disjoint clauses.
    In order to extract an interpolation problem from HC, we first normalise the clauses:
for every relation symbol p ∈ R, we fix a unique vector of variables x̄ p , and rewrite HC
such that p only occurs in the form p( x̄ p ). This is possible due to the fact that HC is
body disjoint. The translation from Horn clauses to a disjunctive interpolation problem
is done recursively, similar in spirit to inlining of function invocations in a program;
thanks to body-disjointness, the encoding is polynomial.
                                   _
           enc HC =                             C ∧ enc0 (B1 ) ∧ · · · ∧ enc0 (Bn )
                     
                                (C∧B1 ∧···∧Bn →false) ∈HC
                                                                                                       
                                          _                                                          
          enc0 p( x̄ p ) =                                  C ∧ enc0 (B1 ) ∧ · · · ∧ enc0 (Bn )
                        
                                 (C∧B1 ∧···∧Bn →p( x̄ p )) ∈HC                                            lp

Note that the resulting formula enc(HC) contains a unique position l p at which the def-
inition of a relation symbol p is inlined; in the second equation, this position is marked
with l p . Any disjunctive interpolant I for this set of positions represents a syntactic
solution of HC, and vice versa.


5     Solvability of Recursion-free Horn Clauses
The previous section discussed how the class of recursion-free body-disjoint Horn
clauses can be solved by reduction to disjunctive interpolation. We next show that this
construction can be generalised to arbitrary systems of recursion-free Horn clauses. In
absence of the body-disjointness condition, however, the encoding of Horn clauses as
interpolation problems can incur a potentially exponential blowup. We give a complexity-
theoretic argument justifying that this blowup cannot be avoided in general. This puts
disjunctive interpolation (and, equivalently, body-disjoint Horn clauses) at a sweet spot:
10         Rümmer, Hojjat, Kuncak

preserving the relatively low complexity of ordinary binary Craig interpolation, while
carrying much of the flexibility of the Horn clause framework.
     We first introduce the exhaustive expansion exp(HC) of a set HC of Horn clauses,
which generalises the Horn clause encoding from the previous section. We write C 0 ∧
B01 ∧ · · · ∧ B0n → H 0 for a fresh variant of a Horn clause C ∧ B1 ∧ · · · ∧ Bn → H,
i.e., the clause obtained by replacing all free first-order variables with fresh variables.
Expansion is then defined by the following recursive functions:
                                _
         exp HC =                           C 0 ∧ exp0 (B01 ) ∧ · · · ∧ exp0 (B0n )
                  
                        (C∧B1 ∧···∧Bn →false) ∈HC
                                  _
         exp p(t¯) =
             0
                                                     C 0 ∧ exp0 (B01 ) ∧ · · · ∧ exp0 (B0n ) ∧ t¯ = s̄0
                   
                        (C∧B1 ∧···∧Bn →p( s̄)) ∈HC

Note that exp is only well-defined for finite and recursion-free sets of Horn clauses,
since the expansion might not terminate otherwise.
Theorem 2 (Solvability of recursion-free Horn clauses). Let HC be a finite, recursion-
free set of Horn clauses. If the underlying constraint language has the interpolation
property, then the following statements are equivalent:
 1. HC is semantically solvable;
 2. HC is syntactically solvable;
 3. exp(HC) is unsatisfiable.
Proof. 2 ⇒ 1 holds because a syntactic solution gives rise to a semantic solution by
interpreting the solution constraints. ¬3 ⇒ ¬1 holds because a model of exp(HC) wit-
nesses domain elements that every semantic solution of HC has to contain, but which
violate at least one clause of the form C ∧ B1 ∧ · · · ∧ Bn → false, implying that no
semantic solution can exist. 3 ⇒ 2 is shown by encoding HC into a disjunctive inter-
polation problem (Sect. 4), which can solved with the help of Theorem 1. To this end,
clauses are first duplicated to obtain a problem that is body-disjoint, and subsequently
normalised as described in Sect. 4.1. More details are given in Appendix A.           t
                                                                                      u

5.1     The Complexity of Recursion-free Horn Clauses
Theorem 2 gives rise to a general algorithm for (syntactically) solving recursion-free
sets HC of Horn clauses, over constraint languages for which interpolation procedures
are available. The general algorithm requires, however, to generate and solve the ex-
pansion exp(HC) of the Horn clauses, which can be exponentially bigger than HC (in
case HC is not body disjoint), and might therefore require exponential time. This leads
to the question whether more efficient algorithms are possible for solving Horn clauses.
    We give a number of complexity results about (semantic) Horn clause solvability;
proofs of the results are given in Appendix B, C, and D. Most importantly, we can ob-
serve that solvability is PSPACE-hard, for every non-trivial constraint language Constr:3

 3
     A similar observation was made in the introduction of [21], for the case of programs with
     procedures.
    Disjunctive Interpolants for Horn-Clause Verification (Extended Technical Report)   11

Lemma 1. Suppose a constraint language can distinguish at least two values, i.e., there
are two ground terms t0 and t1 such that t0 , t1 is satisfiable. Then the semantic solv-
ability problem for recursion-free Horn clauses is PSPACE-hard.
    Looking for upper bounds, it is easy to see that solvability of Horn clauses is in
co-NEXPTIME for any constraint language with satisfiability problem in NP (for in-
stance, quantifier-free Presburger arithmetic). This is because the size of the expan-
sion exp(HC) is at most exponential in the size of HC. Individual constraint languages
admit more efficient solvability checks:
Theorem 3. Semantic solvability of recursion-free Horn clauses over the constraint
language of Booleans is PSPACE-complete.
    Constraint languages that are more expressive than the Booleans lead to a significant
increase in the complexity of solving Horn clauses. The lower bound in the following
theorem can be shown by simulating time-bounded non-deterministic Turing machines.

Theorem 4. Semantic solvability of recursion-free Horn clauses over the constraint
language of quantifier-free Presburger arithmetic is co-NEXPTIME-complete.
    The lower bounds in Lemma 1 and Theorem 4 hinge on the fact that sets of Horn
clauses can contain shared relation symbols in bodies. Neither result holds if we restrict
attention to body-disjoint Horn clauses, which correspond to disjunctive interpolation
as introduced in Sect. 4. Since the expansion exp(HC) of body-disjoint Horn clauses is
linear in the size of the set of Horn clauses, also solvability can be checked efficiently:
Theorem 5. Semantic solvability of a set of body-disjoint Horn clauses, and equiv-
alently the existence of a solution for a disjunctive interpolation problem, is in co-NP
when working over the constraint languages of Booleans and quantifier-free Presburger
arithmetic.
Body-disjoint Horn clauses are still expressive: they can directly encode acyclic control-
flow graphs, as well as acyclic unfolding of many simple recursion patterns.
    For proofs of all results of this section, please consult the Appendix.


6   Model Checking with Recursive Horn Clauses
Whereas recursion-free Horn clauses generalise the concept of Craig interpolation,
solving recursive Horn clauses corresponds to the verification of general programs with
loops, recursion, or concurrency features [14]. Procedures to solve recursion-free Horn
clauses can serve as a building block within model checking algorithms for recursive
Horn clauses [14], and are used to construct or refine abstractions by analysing spu-
rious counterexamples. In particular, our disjunctive interpolation can be used for this
purpose, and offers a high degree of flexibility due to the possibility to analyse coun-
terexamples combining multiple execution traces. We illustrate the use of disjunctive
interpolation within a predicate abstraction-based algorithms for solving Horn clauses.
Our model checking algorithm is similar in spirit to the procedure in [14], and we ex-
plain it in Sect. 6.1.
12       Rümmer, Hojjat, Kuncak

And/or trees of clauses. For sake of presentation, in our algorithm we represent coun-
terexamples (i.e., recursion-free sets of Horn clauses) in the form of and/or trees labelled
with clauses. Such trees are defined by the following grammar:

         AOTree ::= And(h, AOTree, . . . , AOTree) | Or(AOTree, . . . , AOTree)

where h ranges over (possibly recursive) Horn clauses. We only consider well-formed
trees, in which the children of every And-node have head symbols that are consistent
with the body literals of the clause stored in the node, and the sub-trees of an Or-node
all have the same head symbol. And/or trees are turned into body-disjoint recursion-free
sets of clauses by renaming relation symbols appropriately.
Example 5. Referring to the clauses in Fig. 1, a possible and/or tree is
                                                                   
                      And (5), And (3), Or(And((1)), And((2)))

A corresponding set of body-disjoint recursion-free clauses is:
(1’)   merge2(X,Y,Z) ← X = 0 ∧ Y >= 0 ∧ Z = Y
(2’)   merge2(X,Y,Z) ← Y = 0 ∧ X >= 0 ∧ Z = X
(3’)   merge1(X,Y,Z) ← Y1 = Y − 1 ∧ merge2(X, Y1, Z1) ∧ Z = Z1 + 1
(5’)   false ← merge1(X,Y,Z) ∧ Z > X + Y


Solving and/or dags. Counterexamples extracted from model checking problems often
assume the form of and/or dags, rather than and/or trees. Since and/or-dags correspond
to Horn clauses that are not body-disjoint, the complexity-theoretic results of the last
section imply that it is in general impossible to avoid the expansion of and/or-dags
to and/or-trees; there are, however, various effective techniques to speed-up handling
of and/or-dags (somewhat related to the techniques in [21]). We highlight two of the
techniques we use in our interpolation engine Princess [8], which we used in our exper-
imental evaluation of the next section:
     1) counterexample-guided expansion expands and/or-dags lazily, until an unsatisfi-
able fragment of the fully expanded tree has been found; such a fragment is sufficient to
compute a solution. Counterexamples can determine which or-branch of an and/or-dag
is still satisfiable and has to be expanded further.
     2) and/or dag restructuring factors out common sub-dags underneath an Or-node,
making the and/or-dag more tree-like.


6.1    A Predicate Abstraction-based Model Checking Algorithm

Our model checking algorithm is in Fig. 3, and similar in spirit as the procedure in [14];
it has been implemented in the model checker Eldarica.4 Solutions for Horn clauses are
constructed in disjunctive normal form by building an abstract reachability graph over
a set of given predicates. When a counterexample is detected (a clause with consistent
body literals and head false), a theorem prover is used to verify that the counterexample
 4
     http://lara.epfl.ch/w/eldarica
    Disjunctive Interpolants for Horn-Clause Verification (Extended Technical Report)           13

is genuine; spurious counterexamples are eliminated by generating additional predicates
by means of disjunctive interpolation.
    In Fig. 3, Π : R → 2P denotes a mapping from relation symbols to the current
set of predicates used to approximate the relation symbol. Given a (possibly recursive)
set HC of Horn clauses, we define an abstract reachability graph (ARG) as a hyper-
graph (S , E), where
 – S ⊆ {(p, Q) | p ∈ R, Q ⊆ Π(p)} is the set of nodes, each of which is a pair consisting
   of a relation symbol and a set of predicates.
 – E ⊆ S ∗ × HC × S is the hyper-edge relation, with each edge being labelled with
   a clause. An edge E(hs1 , . . . , sn i, h, s), with h = (C ∧ B1 ∧ · · · ∧ Bn → H) ∈ HC,
   implies that
     • si = (pi , Qi ) and Bi = pi (t¯i ) for all i = 1, . . . , n, and
     • s = (p, Q), H = p(t¯), and Q = {φ ∈ Π(p) | C ∧ Q1 [t¯1 ] ∧ · · · ∧ Qn [t¯n ] |= φ[t¯]},
        where we write Qi [t¯i ] for the conjunction of the predicates Qi instantiated for
        the argument terms ti .
    An ARG (S , E) is called closed if the edge relation represents all Horn clauses in
HC. This means, for every clause h = (C ∧ p1 (t¯1 ) ∧ · · · ∧ pn (t¯n ) → H) ∈ HC and every
sequence (p1 , Q1 ), . . . , (pn , Qn ) ∈ S of nodes one of the following properties holds:
  – C ∧ Q1 [t¯1 ] ∧ · · · ∧ Qn [t¯n ] |= false, or
  – there is an edge E(h(p1 , Q1 ), . . . , (pn , Qn )i, C, s) such that s = (p, Q), H = p(t¯), and
    Q = {φ ∈ Π(p) | C ∧ Q1 [t¯1 ] ∧ · · · ∧ Qn [t¯n ] |= φ[t¯]}.
Lemma 2. A set HC of Horn clauses has a closed ARG (S , E) if and only if HC is
syntactically solvable.
    A proof is given in Appendix F. The function ExtractCEX (non-deterministically)
extracts an and/or-tree representing a set of counterexamples, which can be turned into a
recursion-free body-disjoint set of Horn clauses, and solved as described in Sect. 4.1. In
general, the tree contains both conjunctions (from clauses with multiple body literals)
and disjunctions, generated when following multiple hyper-edges (the case |T | > 1).
Disjunctions make it possible to eliminate multiple counterexamples simultaneously.
The algorithm is parametric in the precise strategy used to compute counterexamples,
choices evaluated in the experiments are
TI extraction of a single counterexamples with minimal depth
   (which means that disjunctive interpolation reduces to Tree Interpolation), and
DI simultaneous extraction of all counterexamples with minimal depth
   (so that genuine Disjunctive Interpolation is used).
    We remark that we have also implemented a simpler “global” algorithm (see Sect. 2),
which approximates each relation symbol globally with a single conjunction of inferred
predicates. In contrast, the above algorithm allows multiple nodes, each of which con-
tains a different conjunction, thus allowing a disjunction of conjunctions of predicates.
Both algorithms behave similarly in our experience, with the global one occasionally
slower, but conceptually simpler. Note that, what allowed us to use a simpler algorithm
at all is the fact that the interpolation problem considered is more general. Thus, another
advantage of more expressive forms of interpolation is the simplicity of the resulting
verification algorithms built on top of them.
14          Rümmer, Hojjat, Kuncak

     S := ∅, E := ∅                                                                      . Empty graph
     function ConstructARG
        while true do
            pick clause h = (C ∧ p1 (t¯1 ) ∧ · · · ∧ pn (t¯n ) → H) ∈ HC
                 and nodes (p1 , Q1 ), . . . , (pn , Qn ) ∈ S
                 such that ¬∃s. (h(p1 , Q1 ), . . . , (pn , Qn )i, h, s) ∈ E
                 and C ∧ Q1 [t¯1 ] ∧ · · · ∧ Qn [t¯n ] 6|= false
             if no such clauses and nodes exist then return HC is solvable
             if H = false then                                                    . Refinement needed
                 tree := And(h, ExtractCEX(p1 , Q1 ), . . . , ExtractCEX(pn , Qn )
                 if tree is unsatisfiable then
                      extract disjunctive interpolant from tree, add predicates to Π
                      delete part of (S , E) used to construct tree
                 else return HC is unsolvable, with counterexample trace tree
             else                                                                  . Add edge to ARG
                 then H = p(t¯)
                 Q := {φ ∈ Π(p) | {C} ∪ Q1 ∪ . . . ∪ Qn |= φ}
                 e := (h(p1 , Q1 ), . . . , (pn , Qn )i, h, (p, Q))
                 S := S ∪ {(p, Q)}, E := E ∪ {e}

     function ExtractCEX(root : S )                    . Extract disjunctive interpolation problem
        pick ∅ , T ⊆ E with ∀e ∈ T. e = ( , , root)
        return Or And(h, ExtractCEX(s1 ), . . . , ExtractCEX(sn )) | (hs1 , . . . , sn i, h, root) ∈ T
                  

                   Fig. 3. Algorithm for construction of abstract reachability graphs.



6.2      Experimental Evaluation

We have evaluated our algorithm on a set of benchmarks5 in integer linear arithmetic
from the NTS library [20]. The (a) benchmarks are recursive algorithms, (b) bench-
marks are extracted from programs with singly-linked lists, (c) benchmarks are models
extracted from VHDL models of circuits, (d) benchmarks are verification conditions
for programs with arrays, (e) benchmarks are in the NECLA static analysis suite, (f)
C programs with asynchronous procedure calls translated into NTS using the approach
of [12] (the examples with extension .opt are obtained via an optimised translation
method [Pierre Ganty, personal communication]. The results are given in Fig. 4.
    The experiments show comparable verification times and performance for the Tree
Interpolation and Disjunctive Interpolation runs. Studying the results more closely, we
observed that DI consistently led to a smaller number of abstraction refinement steps
(the scatter plot in Fig. 4); this indicates that DI is indeed able to eliminate multiple
counterexamples simultaneously, and to rapidly generate predicates that are useful for
abstraction. The experiments also showed that there is a trade-off between the time
spent generating predicates, and the quality of the predicates. In TI, on average 31% of
the verification is used for predicate generation (interpolation), while with DI 42% is
used; in some of the benchmarks in (f), this led to the phenomenon that DI was slower

 5
     https://svn.sosy-lab.org/software/sv-benchmarks/trunk/clauses/LIA/
    Disjunctive Interpolants for Horn-Clause Verification (Extended Technical Report)                              15



                              Time [s]                                                            Time [s]
  Model                                                                  Model
                         TI      DI HSF                                                        TI     DI   HSF
  (a) Recursive Models                                                   (f) Examples from [12]
  addition (C)         0.46 0.47     0.19                                h1 (E)              8.32 15.90    0.65
  binarysearch (C)     0.52 0.53     0.16                                h1.opt (E)          1.19 1.00     0.26
  mccarthy-91 (C)      1.19 1.01     0.17                                h1h2 (E)           16.49 30.98    1.10
  mccarthy-92 (C)     10.43 5.90     ERR                                 h1h2.opt (E)        3.63 2.00     0.33
  palindrome (C)       0.92 1.66     0.16                                simple (E)         10.94 16.80    1.07
  remainder (C)        0.77 0.76     ERR                                 simple.opt (E)      1.23 1.02     0.25
  identity (C)         0.73 0.93     0.16                                test0 (C)          21.78 110.11   1.57
  merge (C)            0.76 1.50     0.16                                test0.opt (C)       2.98 3.00     0.29
  parity (C)           0.80 0.80     ERR                                 test0 (E)           9.35 35.42    0.62
  running (C)          0.60 0.60     0.15                                test0.opt (E)       1.14 0.99     0.25
  triple (C)           1.92 1.96     ERR                                 test1.opt (C)       4.99 10.84    0.66
  (b) Examples from L2CA [6]                                             test1 (E)        117.41 364.48 102.88
  bubblesort (E)       2.32 2.52      2.51                               test1.opt (E)       4.33 4.89     0.54
  insdel (E)           0.38 0.35      0.18                               test2 1 (E)        55.67 145.07 189.31
  insertsort (E)       1.31 1.47      0.46                               test2 1.opt (E)     3.36 3.40     0.41
  listcounter (E)      0.44 0.48      0.19                               test2 2 (E)      145.79 127.21 132.55
  listreversal (C)     1.28 1.34      0.32                               test2 2.opt (E)     4.54 4.52     0.36
  listreversal (E)     1.55 1.54      1.54                               test2.opt (C)      46.41 163.41   2.65
  mergesort (E)        0.64 0.78      0.29                               wrpc.manual (C)     0.55 0.68     0.17
  selectionsort (E)    1.72 1.46      1.24                               wrpc (E)           21.00 26.73    2.99
  (c) VHDL models from [25]                                              wrpc.opt (E)        2.40 2.35     0.52
  counter (C)          0.87 0.94      0.16
                                                                       100
  register (C)         0.80 0.86      0.17
  (d) Verification conditions for
  array programs [7]
                                             Tree interpolation (TI)




  rotation vc.1 (C)    2.13 2.58      0.32
  rotation vc.2 (C)    3.21 3.74      0.34
  rotation vc.3 (C)    3.36 3.29      0.31
  rotation vc.1 (E)    1.94 1.97      0.30
                                                                        10
  split vc.1 (C)       5.23 5.83      0.97
  split vc.2 (C)           - 4.45     0.69
  split vc.3 (C)           - 4.93     0.65
  split vc.1 (E)       4.46 3.42      1.11
  (e) NECLA benchmarks
  inf1 (E)             0.89 0.87      0.24
  inf4 (E)             1.07 1.53      0.38                               1
  inf6 (C)             1.30 1.34      0.19                                   1                10                  100
  inf8 (C)             1.73 1.89      0.22                                       Disjunctive interpolation (DI)


Fig. 4. Benchmarks for model checking Horn clauses. The letter after the model name distin-
guishes Correct from models with a reachable Error state. “-” indicates timeout. The scatter plot
illustrates the required number of refinement steps, for the case of single counterexamples (TI)
and simultaneous extraction of all minimal-depth counterexamples (DI). All experiments were
done on an Intel Core i5 2-core machine with 3.2GHz and 8Gb, with a timeout of 500s.
16       Rümmer, Hojjat, Kuncak

than TI, despite fewer refinement steps. We expect this will change as we make further
improvements to our prototypical implementation of disjunctive interpolation.
    We compared our results to the performance of HSF,6 a sophisticated state-of-the-art
verification engine for problems expressed as Horn clauses. We observe similar perfor-
mance on many benchmarks, with HSF notably faster on many (f) benchmarks but the
difference less pronounced for large benchmarks. We were unable to process with HSF
the benchmarks in (a) containing modular arithmetic; we marked those with ERR.


Conclusions
We have introduced disjunctive interpolation as a new form of Craig interpolation tai-
lored to model checkers based on the paradigm of Horn clauses. Disjunctive interpola-
tion can be identified as solving body-disjoint systems of recursion-free Horn clauses,
and subsumes a number of previous forms of interpolation, including tree interpolation
and inductive sequences of interpolants. We believe that the flexibility of disjunctive in-
terpolation is highly beneficial for building interpolation-based model checkers. In par-
ticular, when implementing more intelligent techniques (than used in our experiments)
to select sets of counterexamples handed over to interpolation, significant speed-ups can
be expected. We plan to explore this direction in future work, together with improve-
ments in the implementation of disjunctive interpolation itself.




 6
     http://www7.in.tum.de/tools/hsf/
    Disjunctive Interpolants for Horn-Clause Verification (Extended Technical Report)            17

References

 1. A. Albarghouthi, A. Gurfinkel, and M. Chechik. Craig interpretation. In SAS, 2012.
 2. A. Albarghouthi, A. Gurfinkel, and M. Chechik. Whale: An interpolation-based algorithm
    for inter-procedural verification. In VMCAI, pages 39–55, 2012.
 3. T. Ball, A. Podelski, and S. K. Rajamani. Relative completeness of abstraction refinement
    for software model checking. In TACAS’02, volume 2280 of LNCS, page 158, 2002.
 4. N. Bjørner, K. McMillan, and A. Rybalchenko. Program verification as satisfiability modulo
    theories. In SMT Workshop at IJCAR, 2012.
 5. M. P. Bonacina and M. Johansson. On interpolation in automated theorem proving. (submit-
    ted), 2012.
 6. A. Bouajjani, M. Bozga, P. Habermehl, R. Iosif, P. Moro, and T. Vojnar. Programs with lists
    are counter automata. In CAV, pages 517–531, 2006.
 7. M. Bozga, P. Habermehl, R. Iosif, F. Konečný, and T. Vojnar. Automatic verification of
    integer array programs. In CAV, pages 157–172, 2009.
 8. A. Brillout, D. Kroening, P. Rümmer, and T. Wahl. An interpolating sequent calculus for
    quantifier-free Presburger arithmetic. Journal of Automated Reasoning, 47:341–367, 2011.
 9. A. Cimatti, A. Griggio, and R. Sebastiani. Efficient generation of Craig interpolants in satis-
    fiability modulo theories. ACM Trans. Comput. Log., 12(1):7, 2010.
10. W. Craig. Linear reasoning. A new form of the Herbrand-Gentzen theorem. The Journal of
    Symbolic Logic, 22(3):250–268, September 1957.
11. L. de Moura and N. Bjørner. Z3: An efficient SMT solver. In TACAS, pages 337–340.
    Springer-Verlag, 2008.
12. P. Ganty and R. Majumdar. Algorithmic verification of asynchronous programs. CoRR,
    abs/1011.0551, 2010.
13. S. Graf and H. Saidi. Construction of abstract state graphs with PVS. In CAV, pages 72–83,
    1997.
14. S. Grebenshchikov, N. P. Lopes, C. Popeea, and A. Rybalchenko. Synthesizing software
    verifiers from proof rules. In PLDI, 2012.
15. A. Gupta, C. Popeea, and A. Rybalchenko. Predicate abstraction and refinement for verifying
    multi-threaded programs. In POPL, 2011.
16. A. Gupta, C. Popeea, and A. Rybalchenko. Solving recursion-free horn clauses over LI+UIF.
    In APLAS, pages 188–203, 2011.
17. M. Heizmann, J. Hoenicke, and A. Podelski. Nested interpolants. In POPL, 2010.
18. T. A. Henzinger, R. Jhala, R. Majumdar, and K. L. McMillan. Abstractions from proofs. In
    POPL, pages 232–244. ACM, 2004.
19. H. Hojjat, R. Iosif, F. Konečný, V. Kuncak, and P. Rümmer. Accelerating interpolants. In
    Automated Technology for Verification and Analysis (ATVA), 2012.
20. H. Hojjat, F. Konečný, F. Garnier, R. Iosif, V. Kuncak, and P. Rümmer. A verification toolkit
    for numerical transition systems (tool paper). In FM, 2012.
21. A. Lal, S. Qadeer, and S. K. Lahiri. Corral: A solver for reachability modulo theories. In
    CAV, 2012.
22. K. L. McMillan. iZ3 documentation.
    http://research.microsoft.com/en-us/um/redmond/projects/z3/
    iz3documentation.html.
23. K. L. McMillan. Interpolation and SAT-based model checking. In CAV, 2003.
24. K. L. McMillan. Lazy abstraction with interpolants. In CAV, 2006.
25. A. Smrcka and T. Vojnar. Verifying parametrised hardware designs via counter automata. In
    Haifa Verification Conference, pages 51–68, 2007.
18         Rümmer, Hojjat, Kuncak

A      Solving Recursion-free Horn Clauses: Proof of Theorem 2
We outline a proof for Theorem 2, direction 3 ⇒ 2. Suppose the expansion exp(HC)
of a set HC of recursion-free Horn clauses is unsatisfiable. As before, we compute a
solution of the Horn clauses separately for every connected component of the →HC -
graph. Wlog we can therefore assume that the →HC -graph is connected.

Elimination of duplicated relation symbols. Furthermore, we can assume that every
relation variable occurs at most once in the body of a clause. Otherwise we duplicate
the relation variable (and all clauses defining it), and solve the resulting simpler system.
E.g., if we have clauses

              p(x, y) ∧ p(y, z) → r(x, z),            q(x, y) → p(x, y),            x ≥ 0 → q(x, x)
we first expand the system to

     p1 (x, y) ∧ p2 (y, z) → r(x, z),
     q1 (x, y) → p1 (x, y),       x ≥ 0 → q1 (x, x),          q2 (x, y) → p2 (x, y),          x ≥ 0 → q2 (x, x)

and solve the expanded system. Afterwards we construct a solution of the original sys-
tem as

             C p [x, y] = C p1 [x, y] ∧ C p2 [x, y],          Cq [x, y] = Cq1 [x, y] ∧ Cq2 [x, y]

This is possible because the space of (syntactic) solutions of a Horn clause is closed
under conjunction.

Renaming of first-order variables and normalisation. We normalise the resulting clauses
like in Sect. 4.1: for every relation symbol p, we fix a unique vector of variables x̄ p , and
rewrite HC such that p only occurs in the form p( x̄ p ); by renaming variables, we then
ensure that every variable x that is not argument of a relation symbol occurs in at most
one clause.

Encoding into a disjunctive interpolation problem. The translation from Horn clauses
to a disjunctive interpolation problem is done by adapting the expansion function exp
from Sect. 5:
                                  _
           enc HC =                          C 0 ∧ enc(B1 ) ∧ · · · ∧ enc(Bn )
                    
                                 (C∧B1 ∧···∧Bn →false) ∈HC
                                                                                                      
                                           _                                                        
            enc p( x̄ p ) =                                  C 0 ∧ enc(B1 ) ∧ · · · ∧ enc(Bn )
                         
                                  (C∧B1 ∧···∧Bn →p( x̄ p )) ∈HC                                          lp

Note that the resulting formula enc(HC) contains a unique position l p at which the
definition of a relation symbol p is inlined; in the second equation, this position is
marked with l p . We then derive a disjunctive interpolant I for this set of positions in
enc(HC). A syntactic solution of HC is then given by the definition ∀ x̄ p . p( x̄ p ) ↔
       
I(l p ) , for all relation symbols p.
     Disjunctive Interpolants for Horn-Clause Verification (Extended Technical Report)                          19

B     Solvability of Recursion-free Horn Clauses is PSPACE-hard:
      Proof of Lemma 1

We reduce the unsatisfiability problem of quantified boolean formulae (known to be
PSPACE-hard) to solvability of recursion-free Horn clauses. Assume an arbitrary QBF
of the shape φ = Q1 x1 .Q2 x2 ....Qn xn .F, where Qi ∈ ∃, ∀ are quantifiers, xi are all vari-
ables occurring in the formula, and F is a quantifier-free Boolean formula in CNF.
    We translate φ into a recursion-free set of Horn clauses:

 – a literal xi of a clause C j in F becomes a Horn clause
   xi = t1 → Ci, j (x1 , x2 , . . . , xi−1 , t1 , xi+1 , . . . , xn )
 – a literal ¬xi of a clause C j in F becomes a Horn clause
   xi = t0 → Ci, j (x1 , x2 , . . . , xi−1 , t0 , xi+1 , . . . , xn )
 – a clause C j in F becomes a set of Horn clauses
   C1, j (x1 , . . .) → C j (x1 , . . .), C2, j (x1 , . . .) → C j (x1 , . . .), . . .
 – the body F becomes the Horn clause
   C1 (x1 , . . .) ∧ C2 (x1 , . . .) ∧ · · · → Fn (x1 , . . .)
 – a quantifier Qi = ∃ is translated as the two clauses
   Fi+1 (x1 , . . . , xi−1 , 0) → Fi (x1 , . . . , xi−1 ), Fi+1 (x1 , . . . , xi−1 , 1) → Fi (x1 , . . . , xi−1 )
 – a quantifier Qi = ∀ is translated as the clause
   Fi+1 (x1 , . . . , xi−1 , 0) ∧ Fi+1 (x1 , . . . , xi−1 , 1) → Fi (x1 , . . . , xi−1 )
 – finally, we add the clause F1 () ∧ t0 , t1 → false.

It is now easy to see that the expansion exp(HC) of the Horn clauses coincides with the
result of expanding all quantifiers in φ. By Theorem 2, unsatisfiability of the expansion
is equivalent to solvability of the set of Horn clauses.


C     Succinct Expansion of Recursion-free Horn Clauses

The following lemma implies that solvability of recursion-free Horn clauses over the
theory of Booleans is PSPACE-complete:
Lemma 3 (Succinct expansion). Let HC be a finite, recursion-free set of Horn clauses.
If the underlying constraint language provides quantifiers, in (deterministic) linear time
a formula sexp(HC) can be extracted that is equivalent to exp(HC). The number of
quantifier alternations in sexp(HC) is at most two times the number of relation symbols
in HC.

Proof. We assume that the Horn clauses are connected, i.e., the →HC -graph consists
of a single connected component. Further, we assume that the first-order variables in
any two clauses in HC are disjoint. The encoding of Horn clause as a QBF formula is
then defined by the following algorithm in pseudo-code. The algorithm maintains a list
quantifiers of quantifiers that have to be added in front of the formula.

    quantifiers ← , checksRequired ← ∅
    function Encode(HC)
20         Rümmer, Hojjat, Kuncak

         Order clauses HC in topological order, starting from clauses with head false
         matrix ← EncodeBodies({C ∧ p1 (t¯1 ) ∧ · · · ∧ pn (t¯n ) → false ∈ HC}, )
         remaining ← {C ∧ p1 (t¯1 ) ∧ · · · ∧ pn (t¯n ) → p(t¯) ∈ HC}
         while remaining , ∅ do
            Pick first clause C ∧ p1 (t¯1 ) ∧ · · · ∧ pn (t¯n ) → p(t¯) ∈ HC in topological order
            nextClauses ← {c ∈ HC | head symbol of c is p}
            remaining ← remaining \ nextClauses
            for i ← 1, . . . , arity(p) do
                Create fresh variable xi
                quantifiers ← quantifiers . ∀xi
            guard ← false
            for ( f, p( s̄)) ∈ requiredChecks do                           . Checks with symbol p
                guard ← guard ∨ ( f ∧ s̄ = hx1 , . . . , xn i)
            matrix ← matrix ∧ (guard → EncodeBodies(nextClauses, hx1 , . . . , xn i))
          return quantifiers . matrix

     function EncodeBodies(clauses, s̄)
        result ← false
        for C ∧ p1 (t¯1 ) ∧ · · · ∧ pn (t¯n ) → p(t¯) ∈ clauses do
            quantifiers ← quantifiers . ∃ fv(C ∧ p1 (t¯1 ) ∧ · · · ∧ pn (t¯n ) → p(t¯))
            for i ← 1, . . . , n do
                Create fresh Boolean flag fi
                quantifiers ← quantifiers . ∃ fi
                checksRequired ← checksRequired ∪ {( fi , pi (t¯i ))}
            disjunct ← t¯ = s̄ ∧ C ∧ f1 ∧ · · · ∧ fn
            result ← result ∨ disjunct
         return result


      We illustrate the succinct encoding using an example. Consider the clauses
(C1) r (X,Y) ← Y = X + 1
(C2) r (X,Y) ← Y = X + 2
(C3) s(X,Z) ← r(X, Y) ∧ r(Y, Z)
(C4) false ← s(X, Z) ∧ X >= 0 ∧ Z <= 0

The formula resulting from the succinct encoding is:
         ∃ x0, x1, f1. ∀ x3, x4. ∃ x5, x6, x7, f2, f3 . ∀ x10, x11. ∃ x12, x13, x14, x15.
(C4)     (x1 >= 0 ∧ 0 >= x0 ∧ f1 ∧
           (( f1 ∧ x1 = x3 ∧ x0 = x4) →
(C3)        (x7 = x3 ∧ x6 = x4 ∧ f2 ∧ f3)) ∧
           ((( f2 ∧ x7 = x10 ∧ x5 = x11) ∨
              (f3 ∧ x5 = x10 ∧ x6 = x11)) →
(C1)        (( x13 = x10 ∧ x12 = x11 ∧ x12 = x13 + 1) ∨
(C2)          (x15 = x10 ∧ x14 = x11 ∧ x14 = x15 + 2))))
    Disjunctive Interpolants for Horn-Clause Verification (Extended Technical Report)                                     21

D    Solvability of Recursion-free Horn Clauses over Presburger
     Arithmetic is co-NEXPTIME-Complete: Proof of Theorem 4

It has already been observed that solvability is in co-NEXPTIME, so we proceed to
show hardness by direct reduction of exponential-time-bounded Turing machines (pos-
sibly non-deterministic, with binary tape) to recursion-free Horn clauses over quantifier-
free PA. A Turing machine M = (Q, δ, q0 , F) is defined by

 – a finite non-empty set Q of states,
 – an initial state q0 ∈ Q,
 – a final state f ∈ Q,
 – a transition relation δ ⊆ ((Q \ { f }) × {0, 1}) × (Q × {0, 1} × {L, R}).

Wlog, we assume that Q = {0, 1, . . . , f } ⊆ Z and q0 = 0.
    We define a relation symbol step(q, l, r, q0 , l0 , r0 ) to represent single execution steps
of the machine. The parameters l, r, l0 , r0 represent the tape, which is encoded as non-
negative integers; the bits in the binary representation of the integers are the contents
of the tape cells. l is the tape left of the head, r the tape right of the head. The least-
significant bit of r is the tape cell at the head position. l0 , r0 are the corresponding post-
state variables after one execution step.
    A tuple (q, b, q0 , b0 , L) ∈ δ (moving the tape to the left) is represented by a clause

                                       step(q, x, b + 2y, q0 , b0 + 2x, y)

where x, y are the implicitly universally quantified variables of the clause, and q, b, q0 , b0
concrete numeric constants. Similarly, a tuple (q, b, q0 , b0 , R) ∈ δ is encoded as

                     0 ≤ x ≤ 1 → step(q, x + 2y, b + 2z, q0 , y, x + 2b0 + 4z)

To represent termination, we add a clause step( f, x, y, f, x, y), implying that the machine
will stay in the final state f forever.
    We then introduce n further clauses to model an execution sequence of length 2n :

             step(x, y, z, x0 , y0 , z0 ) ∧ step(x0 , y0 , z0 , x00 , y00 , z00 ) → step1 (x, y, z, x00 , y00 , z00 )
           step1 (x, y, z, x0 , y0 , z0 ) ∧ step1 (x0 , y0 , z0 , x00 , y00 , z00 ) → step2 (x, y, z, x00 , y00 , z00 )
                                                                                   ···
    step   n−1
                 (x, y, z, x , y , z ) ∧ step
                           0   0   0            n−1
                                                      (x , y , z , x , y , z ) → stepn (x, y, z, x00 , y00 , z00 )
                                                        0   0   0   00   00   00



    The final clauses expresses that the Turing machine does not terminate within 2n
steps, when started with the initial tape t: stepn (0, 0, t, f, x, y) → false.
    Clearly, the expansion exp(HC) of the resulting set HC of Horn clauses is unsatisfi-
able (i.e., HC can be solved) if and only if no execution of the Turing machine, starting
with the initial tape t, terminates within 2n steps.
22      Rümmer, Hojjat, Kuncak

E    Clauses Solvable Semantically but not Syntactically

Consider the following clause set HC:
multA(X,Y,Z) ← X = 0 ∧ Z = 0
multA(X,Y,Z) ← multA(X1,Y,Z1) ∧ X1 = X − 1 ∧ Z = Z1 + Y
multB(X,Y,Z) ← X = 0 ∧ Z = 0
multB(X,Y,Z) ← multB(X1,Y,Z1) ∧ X1 = X − 1 ∧ Z = Z1 + Y
false ← multA(X,Y,Z1) ∧ multB(X,Y,Z2) ∧ Z1 , Z2

The clauses define two version of a multiplication and assert that the result is function-
ally determined by the first two arguments. Let a, b ⊆ Z3 denote the interpretations of
multA and multB, respectively, in any solution that satisfies all Horn clauses. We show
that the only possibility is that a = b = m where m = {(x, y, z) ∈ Z3 | z = xy} is
the multiplication relation. Indeed, by induction we can easily prove that m ⊆ a and
m ⊆ b, using the first four clauses. To show the converse, suppose on the contrary, that
(x, y, z) ∈ a where z , xy (the case for (x, y, z) ∈ b is symmetrical). Because (x, y, xy) ∈ b
and x , z, the last clause does not hold, a contradiction.
     Therefore, the clauses have a unique solution a = b = m, but this solution is not
definable in a Presburger arithmetic (e.g. by semilinearity of the solution sets, or by
decidability of Presburger arithmetic vs undecidability of its extension with multiplica-
tion). Therefore, the above clauses give an example of clauses that are semantically but
not syntactically solvable in Presburger arithmetic.
     Further such examples can be constructed by using Horn clauses to define other
total computable functions that are not definable in Presburger arithmetic alone.


F    Completeness of Horn Clause Verification: Proof of Lemma 2
                                                           W      V
“⇒”: Define each relation symbol p as the disjunction (p,Q)∈S Q. Since S is closed
under the edge relation, this yields a solution for the set HC of Horn clauses.
     “⇐”: Suppose HC is syntactically solvable, with each relation symbol p being
mapped to the constraint C p . We define the predicate abstraction Π(p) = {C p }, and
construct the ARG with nodes S = {(p, C p )}, and the maximum edge relation E, which
is closed.
