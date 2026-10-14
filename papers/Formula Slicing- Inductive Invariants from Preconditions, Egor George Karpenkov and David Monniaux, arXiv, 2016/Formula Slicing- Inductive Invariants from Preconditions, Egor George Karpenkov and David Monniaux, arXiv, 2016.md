                                               Formula Slicing: Inductive Invariants from
                                                             Preconditions?

                                                            Egor George Karpenkov and David Monniaux

                                                      Univ. Grenoble Alpes, VERIMAG, F-38000 Grenoble, France
                                                             CNRS, VERIMAG, F-38000 Grenoble, France
arXiv:1609.09288v2 [cs.LO] 2 Oct 2016




                                                Abstract. We propose a “formula slicing” method for finding inductive
                                                invariants. It is based on the observation that many loops in the program
                                                affect only a small part of the memory, and many invariants which were
                                                valid before a loop are still valid after.
                                                Given a precondition of the loop, obtained from the preceding program
                                                fragment, we weaken it until it becomes inductive. The weakening proce-
                                                dure is guided by counterexamples-to-induction given by an SMT solver.
                                                Our algorithm applies to programs with arbitrary loop structure, and it
                                                computes the strongest invariant in an abstract domain of weakenings of
                                                preconditions. We call this algorithm “formula slicing”, as it effectively
                                                performs “slicing” on formulas derived from symbolic execution.
                                                We evaluate our algorithm on the device driver benchmarks from the Inter-
                                                national Competition on Software Verification (SV-COMP), and we show
                                                that it is competitive with the state-of-the-art verification techniques.


                                        1     Introduction
                                        In automated program verification, one crucial task is establishing inductive
                                        invariants for loops: properties that hold initially, and also by induction for any
                                        number of execution steps.
                                            Abstract-interpretation-based approaches restrict the class of expressible
                                        invariants to a predefined abstract domain, such as intervals, octagons, or convex
                                        polyhedra (all of which can only express convex properties). Any candidate
                                        invariants which can not be expressed in the chosen abstract domain get over-
                                        approximated. Traditionally, this restriction applies at all program locations,
                                        but approaches such as path focusing [1] limit the precision loss only to loop
                                        heads, representing program executions between the loop-heads precisely using
                                        first-order formulas.
                                            This is still a severe restriction: if a property flows from the beginning of the
                                        program to a loop head, and holds inductively after, but is not representable
                                        within the chosen abstract domain, it is discarded. In contrast, our idea exploits
                                        the insight that many loops in the program affect only a small part of the memory,
                                        and many invariants which were valid before the loop are still valid.
                                        ?
                                            The research leading to these results has received funding from the European Research
                                            Council under the European Union’s Seventh Framework Programme (FP/2007-2013)
                                            / ERC Grant Agreement nr. 306595 “STATOR”.
2

int x = input(), p = input();
if (p)
    assume(x >= 0);
else
    assume(x < 0);
for (int i=0; i < input(); i++) x *= 2;


         Fig. 1: Motivating Example for Finding Inductive Weakenings.

   Consider finding an inductive invariant for the motivating example in Fig. 1.
Symbolic execution up to the loop-head can precisely express all reachable states:
                 i = 0 ∧ (p 6= 0 =⇒ x ≥ 0) ∧ (p = 0 =⇒ x < 0)                      (1)
Yet abstraction in a numeric convex domain at the loop head yields i = 0,
completely losing the information that x is positive iff p 6= 0. Observe that this
information loss is not necessary, as the sign of x stays invariant under the
multiplication by a positive constant (assuming mathematical integers for the
simplicity of exposition). To avoid this loss of precision, we develop a “formula
slicing” algorithm which computes inductive weakenings of propagated formulas,
allowing to propagate the formulas representing inductive invariants across
loop heads. In the motivating example, formula slicing computes an inductive
weakening of the initial condition in Eq. 1), which is (p = 6 0 =⇒ x ≥ 0) ∧ (p =
0 =⇒ x < 0), and is thus true at every iteration of the loop. The computation of
inductive weakenings is performed by iteratively filtering out conjuncts falsified
by counterexamples-to-induction, derived using an SMT solver. In the motivating
example, transition i = 1 from i = 0 falsifies the constraint i = 0, and the rest of
the conjuncts are inductive.
     The formula slicing fixpoint computation algorithm is based on performing
abstract interpretation on the lattice of conjunctions over a finite set of predicates.
The computation starts with a seed invariant which necessarily holds at the given
location on the first time the control reaches it, and during the computation
it is iteratively weakened until inductiveness. The algorithm terminates within
a polynomial number of SMT calls with the smallest invariant which can be
expressed in the chosen lattice.
Contributions We present a novel insight for generating inductive invariants,
and a method for creating a lattice of weakenings from an arbitrary formula
describing the loop precondition using a relaxed conjunctive normal form (Def. 2)
and best-effort quantifier elimination (Sec. 4).
     We evaluate (Sec. 7) our implementation of the formula slicing algorithm
on the “Device Drivers” benchmarks from the International Competition on
Software Verification [2], and we demonstrate that it can successfully verify large,
real-world programs which can not be handled with traditional numeric abstract
interpretation, and that it is competitive with state of the art techniques.
Related Work The Houdini [3] algorithm mines the program for a set of
predicates, and then finds the largest inductive subset, dropping the candidate
non-inductive lemmas until the overall inductiveness is achieved. The optimality
                                                                                   3

proof for Houdini is present in the companion paper [4]. A very similar algorithm
is used by Bradley et Al. [5] to generate the inductive invariants from negations
of the counter-examples to induction.
    Inductive weakening based on counterexamples-to-induction can be seen as
an algorithm for performing predicate abstraction [6]. Generalizing inductive
weakening to best abstract postcondition computation Reps et al. [7] use the
weakening approach for computing the best abstract transformer for any finite-
height domain, which we also perform in Sec. 3.1.
    Generating inductive invariants from a number of heuristically generated
lemmas is a recurrent theme in the verification field. In automatic abstraction [8]
a set of predicates is found for the simplified program with a capped number of
loop iterations, and is filtered until the remaining invariants are inductive for
the original, unmodified program. A similar approach is used for synthesizing
bit-precise invariants by Gurfinkel et Al. [9].
    The complexity of the inductive weakening and that of the related template
abstraction problem are analyzed by Lahiri and Qadeer [10].
Overview We introduce the necessary background in Sec. 2 and the weakening
algorithm in Sec. 3. We define the space of all used weakenings in Sec. 4. We
develop the formula slicing algorithm for applying inductive weakening to real
programs in Sec. 5, we describe our implementation and the required optimizations
and improvements in Sec. 6, and we conclude with the empirical evaluation on
the SV-COMP dataset in Sec. 7.

2     Background
2.1   Logic Preliminaries
We operate over first-order, existentially quantified logic formulas within an
efficiently decidable theory. A set of all such formulas over free variables in X is
denoted by F(X). Checking such formulas for satisfiability is NP-hard, but with
modern SMT (satisfiability modulo theories) solvers these checks can often be
performed very fast.
     A formula is said to be an atom if it does not contain logical connectives
(e.g. it is a comparison x ≤ y between integer variables), a literal if it is an atom
or its negation, and a clause if it is a disjunction of literals. A formula is in
negation normal form (NNF) if negations are applied only to atoms, and it is
in conjunctive normal form (CNF) if it is a conjunction of clauses. For a set of
variables X, we denote by X 0 a set where the prime symbol was added to all the
elements of X. With φ[a1 /a2 ] we denote the formula φ after all free occurrences
of the variable a1 have been replaced by a2 . This notation is extended to sets
of variables: φ[X/X 0 ] denotes the formula φ after all occurrences of the free
variables from X were replaced with corresponding free variables from X 0 . For
brevity, a formula φ[X/X 0 ] may be denoted by φ0 . We use the brackets notation
to indicate what free variables can occur in a formula: e.g. φ(X) can only contain
free variables in X. The brackets can be dropped if the context is obvious.
     A formula φ(X), representing a set of program states, is said to be inductive
with respect to a formula τ (X ∪ X 0 ), representing a transition, if Eq. 2 is valid:
4



                            φ(X) ∧ τ (X ∪ X 0 ) =⇒ φ0 (X 0 )                          (2)
    That is, all transitions originating in φ end up in φ0 . We can query an SMT
solver for the inductiveness of φ(X) with respect to τ (X ∪X 0 ) using the constraint
in Eq. 3, which is unsatisfiable iff φ(X) is inductive.
                             φ(X) ∧ τ (X ∪ X 0 ) ∧ ¬φ0 (X 0 )                         (3)

     For a quantifier-free formula φ inductiveness checking is co-NP-complete.
However, if φ is existentially quantified, the problem becomes Π2p -complete. For
efficiency, we shall thus restrict inductiveness checks to quantifier-free formulas.


2.2     Program Semantics and Verification Task

Definition 1 (CFA). A control flow automaton is a tuple (nodes, edges, n0 , X),
where nodes is a set of program control states, modelling the program counter,
n0 ∈ nodes is a program starting point, and X is a set of program variables.
Each edge e ∈ edges is a tuple (a, τ (X ∪ X 0 ), b), modelling a possible transition,
where {a, b} ⊆ nodes, and τ (X ∪ X 0 ) is a formula defining the semantics of a
transition over the sets of input variables X and output variables X 0 .

    A non-recursive program in a C-like programming language can be trivially
converted to a CFA by inlining functions, replacing loops and conditionals with
guarded gotos, and converting guards and assignments to constraints over input
variables X and output variables X 0 .
    A concrete data state m of a CFA is a variable assignment X → Z which
assigns each variable an integral value.1 The set of all concrete data states
is denoted by C. A set r ⊆ C is called a region. A formula φ(X) defines a
region S of all states which it models (S ≡ {c | c |= φ}). A set of all formulas
over X is denoted by F(X). A concrete state c is a tuple (m, n) where m is
a concrete data state, and n ∈ nodes is a control state. A program path is a
sequence of concrete states hc0 , . . . , cn i such that for any two consecutive states
ci = (mi , ni ) and ci+1 = (mi+1 , ni+1 ) there exists an edge (ni , τ, ni+1 ) such
that mi (X) ∪ mi+1 (X 0 ) |= τ (X ∪ X 0 ). A concrete state si = (m, n), and the
contained node n, are both called reachable iff there exists a program path which
contains si .
    A verification task is a pair (P, ne ) where P is a CFA and ne ∈ nodes is an
error node. A verification task is safe if ne is not reachable. Safety is traditionally
decided by finding a separating inductive invariant: a mapping from program
locations to regions which is closed under the transition relation and does not
contain the error state.
1
    The restriction to integers is for the simplicity of exposition, and is not present in
    the implementation.
                                                                                   5

2.3   Invariant and Inductive Invariant
A set of concrete states is called a state-space, and is defined using a mapping
from nodes to regions. A mapping I : nodes → F(X) is an invariant if it contains
all reachable states, and an inductive invariant if it is closed under the transition
relation: that is, it satisfies the conditions for initiation and consecution:

                Initiation: I(n0 ) = >
             Consecution: for all edges (a, τ, b) ∈ edges, for all X, X 0
                            I(a)(X) ∧ τ (X ∪ X 0 ) =⇒ (I(b))0 (X 0 )            (4)
   Intuitively, the initiation condition dictates that the initial program state at
n0 (arbitrary contents of memory) is covered by I, and the consecution condition
dictates that under all transitions I should map into itself. Similarly to Eq. 3,
the consecution condition in Eq. 4 can be verified by checking one constraint for
unsatisfiability using SMT for each edge in a CFA. This constraint is given in
Eq. 5, which is unsatisfiable for each edge (a, τ, b) ∈ edges iff the consecution
condition holds for I.

                       I(a)(X) ∧ τ (X ∪ X 0 ) ∧ ¬(I(b))0 (X 0 )                  (5)

2.4   Abstract Interpretation Over Formulas
Program analysis by abstract interpretation [11] searches for inductive invariants
in a given abstract domain: the class of properties considered by the analysis
(e.g. upper and lower bounds on each numeric variable). The run of abstract
interpretation effectively interprets the program in the given abstract domain,
performing operations on the elements of an abstract domain instead of concrete
values (e.g. the interval x ∈ [1, 2] under the transition x += 1 becomes x ∈ [2, 3]).
    We define the abstract domain D ≡ 2L ∪ {⊥} to be a powerset of the set of
formulas L ⊆ F(X) with an extra element ⊥ attached. A concretization of an
element d ∈ D is a conjunction over all elements of d, or a formula false for ⊥.
    Observe that D forms a complete lattice by using set operations of intersec-
tion and union as meet and join operators respectively, and using syntactical
equality for comparing individual formulas. The syntactic comparison is an over-
approximation as it does not take the formula semantics into account. However,
this comparison generates a complete lattice of height kLk + 2.

2.5   Large Block Encoding
The approach of large block encoding [12] for model checking, and the approach of
path focusing [1] for abstract interpretation are based on the observation that by
compacting a control flow and reducing a number of abstraction points, analysis
precision and sometimes even analysis performance can be greatly improved.
Both approaches utilize SMT solvers for performing abstraction afterwards.
    A simplified version of compaction is possible by applying the following two
rules to a CFA until a fixed point is reached:
6

    – Two consecutive edges (a, s1 , b) and (b, s2 , c) with no other existing edge
      entering or leaving b get replaced by a new edge (a, ∃X̂. s1 [X 0 /X̂]∧s2 [X/X̂], c).
    – Two parallel edges (a, s1 , b) and (a, s2 , b) get replaced by (a, s1 ∨ s2 , c).

In our approach, this pre-processing is used on the CFA obtained from the
analyzed program.

3      Counterexample-to-Induction Weakening Algorithm
The approaches [3,5,8,9] mentioned in Sec. 1 are all based on using counterexam-
ples to induction for filtering the input set of candidate lemmas. For completeness,
we restate this approach in Alg. 1.
     In order to perform the weakening without syntactically modifying φ during
the intermediate queries, we perform selector variables annotation: we replace
each lemma li ∈ φ with a disjunction si ∨ li , using a fresh boolean variable
si . Observe that if all selector variables are assumed to be false the annotated
formula φannotated is equivalent to φ, and that assuming any individual selector
si is equivalent to removing (replacing with >) the corresponding lemma li from
φ. Such an annotation allows us to make use of incrementality support by SMT
solvers, by using the solving with assumptions feature.
     Alg. 1 iteratively checks input formula φ for inductiveness using Eq. 3 (line 13).
The solver will either report that the constraint is unsatisfiable, in which case φ
is inductive, or provide a counterexample-to-induction represented by a model
M(X ∪ X 0 ) (line 14). The counterexample-driven algorithm uses M to find
the set of lemmas which should be removed from φ, by removing the lemmas
modelled by M in ¬φ0 (line 20). The visualization of such a filtering step for a
formula φ consisting of two lemmas is given in Fig. 2.
     As shown in related literature [4], Alg. 1 terminates with the strongest possible
weakening within the linear number of SMT calls with respect to kφannotated k.


3.1      From Weakenings to Abstract Postconditions

As shown by Reps et Al. [7], the inductive weakening algorithm can be generalized
for the abstract postcondition computation for any finite-height lattice.
    For given formulas ψ(X), τ (X ∪X 0 ), and φ(X) consider the problem of finding
a weakening φ̂ ⊆ φ, such that all feasible transitions from ψ through τ end up in
φ̂. This is an abstract postcondition of ψ under τ in the lattice of all weakenings
of φ (Sec. 2.4). The problem of finding it is very similar to the problem of finding
an inductive weakening, as similarly to Eq. 3, we can check whether a given
weakening of φ is a postcondition of ψ under τ using Eq. 6,

                          ψ(X) ∧ τ (X ∪ X 0 ) ∧ ¬φ0annotated (X 0 )                    (6)
   Alg. 1 can be adapted for finding the strongest postcondition in the abstract
domain of weakenings of the input formula with very minor modifications. The
required changes are accepting an extra parameter ψ, and changing the queried
constraint (line 6) to Eq. 6. The found postcondition is indeed strongest [7].
                                                                                    7


                                     τ (X ∪ X 0 )

                                      X                                     X0


                                                                  M(X 0 )


                     M(X)

                L1              L2                  L1                 L2


                     L1 ∧ L2                             ¬L01 ∨ ¬L02


Fig. 2: Formula φ(X) ≡ L1 (X)∧L2 (X) is tested for inductiveness under τ (X ∪X 0 ).
Model M identifies a counter-example to induction. From M |= ¬L02 (X 0 ) we
know that the lemma L2 has to be dropped. As weakening progresses, the shaded
region in the left box is growing, while the shaded region in the right box is
shrinking, until there are no more counterexamples to induction.

4    The Space of All Possible Weakenings
We wish to find a weakening of a set of states represented by φ(X), such that it is
inductive under a given transition τ (X ∪ X 0 ). For a single-node CFA defined by
initial condition φ and a loop transition τ such a weakening would constitute an
inductive invariant as by definition of weakening it satisfies the initial condition
and is inductive.
     We start with an observation that for a formula in NNF replacing any subset
of literals with > results in an over-approximation, as both conjunction and
disjunction are monotone operators. E.g. for a formula φ ≡ (la ∧ lb ) ∨ lc such
possible weakenings are >, lb ∨ lc , and la ∨ lc .
     The set of weakenings defined in the previous paragraph is redundant, as it
does not take the formula structure into account — e.g. in the given example if
lc is replaced with > it is irrelevant what other literals are replaced, as the entire
formula simplifies to >. The most obvious way to address this redundancy is to
convert φ to CNF and to define the set of all possible weakenings as conjunctions
over the subsets of clauses in φCNF . E.g. for the formula φ ≡ la ∧ lb ∧ lc possible
weakenings are la ∧ lb , lb ∧ lc , and la ∧ lc . This method is appealing due to
the fact that for a set of lemmas the strongest (implying all other possible
inductive weakenings) inductive subset can be found using a linear number of
SMT checks [5]. However (Sec. 2.1) polynomial-sized CNF conversion (e.g. Tseitin
encoding) requires introducing existentially quantified boolean variables which
make inductiveness checking Π2p -hard.
     The arising complexity of finding inductive weakenings is inherent to the
problem: in fact, the problem of finding any non-trivial (6= >) weakening within
the search space described above is Σ2p -hard (see proof in Appendix A).
8

Algorithm 1 Counterexample-Driven Weakening.
 1: Input: Formula φ(X) to weaken in RCNF, transition relation τ (X ∪ X 0 )
 2: Output: Inductive φ̂ ⊆ φ
 3: . Annotate lemmas with selectors, S is a mapping from selectors to lemmas they
    annotate.
 4: S, φannotated ← Annotate(φ)
 5: T ← SMT solver instance
 6: query ← φannotated ∧ τ ∧ ¬φ0annotated
 7: Add query to constraints in T
 8: assumptions ← ∅
 9: removed ← ∅
10: . In the beginning, all of the lemmas are present
11: for all (selector , lemma) ∈ S do
12:     assumptions ← assumptions ∪ {¬selector }
13: while T is satisfiable with assumptions do
14:     M ← model of T
15:     assumptions ← ∅
16:     for all (selector , lemma) ∈ S do
17:        if M |= ¬lemma 0 or lemma 0 is irrelevant to satisfiability then
18:           . lemma has to be removed.
19:           assumptions ← assumptions ∪ {selector }
20:           removed ← removed ∪ {lemma}
21:        else
22:           assumptions ← assumptions ∪ {¬selector }
23: . Remove all lemmas which were filtered out
24: return φ[removed />]


   Thus instead we use an over-approximating set of weakenings, defined by all
possible subsets of lemmas present in φ after the conversion to relaxed conjunctive
normal form.

Definition 2 (Relaxed Conjunctive Normal Form (RCNF)). A formula
φ(X) is in relaxed conjunctive normal form if it is a conjunction of quantifier-free
formulas (lemmas).

    For example, the formula φ ≡ la ∧ (lb ∨ (lc ∧ ld )) is in RCNF. The over-
approximation comes from the fact that non-atomic parts of the formula are
grouped together: the only possible non-trivial weakenings for φ are la and
lb ∨ (lc ∧ ld ), and it is impossible to express la ∧ (lb ∨ lc ) within the search space.
    We may abuse the notation by treating φ in RCNF as a set of its conjuncts,
and writing l ∈ φ for a lemma l which is an argument of the parent conjunction
of φ, or φ1 ⊆ φ2 to indicate that all lemmas in φ1 are contained in φ2 , or kφk
for the number of lemmas in φ. For φ in RCNF we define a set of all possible
weakenings as conjunctions over all sets of lemmas contained in φ. We use an
existing, optimal counter-example based algorithm in order to find the strongest
weakening of φ with respect to τ in the next section.
                                                                                    9

    A trivially correct conversion to a relaxed
                                           V       conjunctive normal is to convert
an input formula φ to a conjunction {φ}. However, this conversion is not
very interesting, as it gives rise to a very small set of weakenings: φ and >.
Consequently, with such a conversion, if φ is not inductive with respect to the
transition of interest, no non-trivial weakening can be found. On the other extreme,
φ can be converted to CNF explicitly using associativity and distributivity laws,
giving rise to a very large set of possible weakenings. Yet the output of such a
conversion is exponentially large.
    We present an algorithm which converts φ into a polynomially-sized conjunc-
tion of lemmas. The following rules are applied recursively until a fixpoint is
reached:

Flattening All nested conjunctions are flattened. E.g. a ∧ (b ∧ c) 7→ a ∧ b ∧ c.
Factorization When processing a disjunction over multiple conjunctions we
   find and extract a common factor. E.g. (a ∧ b) ∨ (b ∧ c) 7→ b ∧ (a ∨ c).
                                                        W
Explicit expansion with size limit A disjunction L, where each l ∈ L is
   a conjunction, can be converted to a conjunction over disjunctions over all
   elements in the cross product over L. E.g. (a ∧ b) ∨ (c ∧ d) can be converted
   (a ∨ c) ∧ (a ∨ d) ∧ (b ∨ c) ∧ (b ∨ d).
   Applying such an expansion results in an exponential blow-up, but we only
   perform it if the resulting formula size is smaller than a fixed constant, and
   we limit the expansion depth to one.

Eliminating Existentially Quantified Variables The formulas resulting
form large block encoding (Sec. 2.5) may have intermediate (neither input nor
output), existentially bound variables. In general, existential quantifier elimination
(with e.g. Fourier-Motzkin) is exponential. However, for many cases such as
simple deterministic assignments, existential quantifier elimination is easy: e.g.
∃t. x0 = t + 3 ∧ t = x + 2 can be trivially replaced by x0 = x + 5 using substitution.
    We use a two-step method to remove the quantified variables: we run a
best-effort pattern-matching approach, removing the bound variables which can
be eliminated in polynomial time, and in the second step we drop all the lemmas
which still contain the existentially bound variables. The resulting formula is an
over-approximation of the original one.

5    Formula Slicing: Overall Algorithm
We develop the formula slicing algorithm in order to apply the inductive weaken-
ing approach for generating inductive invariants in large, potentially non-reducible
programs with nested loops.
     “Classical” Houdini-based algorithms consist of two steps: candidate lemmas
generation, followed by counterexample-to-induction-based filtering. However,
in our case candidate lemmas representing postconditions depend on previous
filtering steps, and careful consideration is required in order to generate unique
candidate lemmas which do not depend on the chosen iteration order.
10

Abstract Reachability Tree In order to solve this problem we use abstract
reachability tree [13] (ART) as a main datastructure for our algorithm. For the
simplicity of notation we introduce the projection function πi , which projects
the ith element of the tuple. An ART describes the current invariant candidate
processed by the analysis for a fixed CFA (nodes, edges, n0 , X), and is defined
by a set of nodes T . Each node t ∈ T is a triple, consisting of a CFA node
n ∈ nodes, defining which location t corresponds to, an abstract domain element
d ∈ D, defining the reachable state space at t, and an optional backpointer
b ∈ (T ∪ {∅}), defining the tree structure. The tree topology has to be consistent
with the structure of the underlying CFA: node a ∈ T can have a backpointer
to the node b ∈ T only if there exists an edge (π1 (a), , π1 (b)) in the CFA. The
starting tree node t0 is (n0 , >, ∅).
    An ART is sound if the output of each transition over-approximates the
strongest postcondition: that is, for each node t ∈ T with non-empty backpointer
b = π3 (t), an edge e = (π1 (b), τ, π1 (t)) must exist in edges, and the abstract
domain element associated with t must over-approximate the strongest post-
condition of b under τ . Formally, the following must hold: ∃X. Jπ2 (b)K ∧ τ =⇒
        0
Jπ2 (t)K (recall that priming is a renaming operation [X/X 0 ]). A node b ∈ T is
fully expanded if for all edges (π1 (t), τ, n) ⊆ edges there exists a node t ∈ T ,
where π1 (t) = n, and π2 (t) over-approximates the strongest post-condition of
π2 (b) under τ . A node (a, d1 , ) covers another node (a, d2 , ) iff Jd2 K =⇒ Jd1 K.
A sound labelled ART where all nodes are either fully expanded or covered
represents an inductive invariant.
    The transfer relation for the formula slicing is given in Alg. 3. In order
to generate a successor for an element (na , d, b), and an edge (na , τ, nb ) we
first traverse the chain of backpointers up the tree. If we can find a “sibling”
element s where π1 (s) = na 2 by following the backpointers, we weaken s until
inductiveness (line 4) relative to the new incoming transition τ , and return that as
a postcondition. Such an operation effectively performs widening [11] to enforce
convergence. Alternatively, if no such sibling exists, we convert ∃X. ∧τ to RCNF
form (line 6), and this becomes a new element of the abstract domain.
    The main fixpoint loop performs the following calculation: for every leaf in
the tree which is not yet expanded or covered, all successors are found using the
transfer relation defined in Alg. 3, and for each newly created element, coverage
relation is checked against all elements in the same partition. A simplified version
of this standard fixpoint iteration on ART is given in Alg. 2.
    Observe that our algorithm has a number of positive features. Firstly, be-
cause our main datastructure is an ART, in case of a counterexample we get
a path to a property violation (though due to abstraction used, not all taken
transitions are necessarily feasible, similarly to the leaping counterexamples of
LoopFrog [14]). Secondly, our approach for generating initial candidate invariants
ensures uniqueness, even in the case of a non-reducible CFA.

2
      In the implementation, the sibling is defined by a combination of callstack, CFA
     node and loopstack.
                                                                                 11

Algorithm 2 Formula Slicing: Overall Algorithm
1: Input: CFA (nodes, edges, n0 , X)
2: . Expanded.
3: E ← ∅
4: . Covered.
5: C ← ∅
6: t0 ← (n0 , >, ∅)
7: T ← {t0 }
8: while ∃t ∈ (T \ E \ C) do
 9:    . Expand.
10:    for all edge e ∈ edges where π1 (e) = π1 (t) do
11:       T ← T ∪ { TransferRelation(e, t) }
12:    E ← E ∪ {t}
13:    . Check Coverage.
14:    for all t1 ∈ (T \ C) where π1 (t1 ) = π1 (t) do
15:       if Jπ2 (t1 )K =⇒ Jπ2 (t)K then
16:           C ← C ∪ {t1 }
17:       if Jπ2 (t)K =⇒ Jπ2 (t1 )K then
18:           C ← C ∪ {t}



Algorithm 3 Formula Slicing: Postcondition Computation.
1: function TransferRelation(edge e ≡ (na , τ, nb ), state t ≡ (na , d, b))
2:    sibling s ← FindSibling(b, n0 )
3:    if s 6= ∅ then
4:        . Abstract postcondition of d under τ in weakenings of s (Sec. 3.1).
5:        e ← Weaken(d, τ ∧ nb , s)
6:     else
 7:        . Convert the current invariant candidate to RCNF.
 8:        e ← ToRCNF(JdK ∧ τ )
 9:    return (nb , e, t)
10: function FindSibling(state b, CFA node n)
11:    if π1 (b) = n then
12:        return b
13:    else if π3 (b) = ∅ then
14:        return ∅
15:    else
16:        return FindSibling(π3 (b), n)



   As a downside, tree representation may lead to the exponential state-space
explosion (as a single node in a CFA may correspond to many nodes in an ART).
However, from our experience in the evaluation (Sec. 7), with a good iteration
order (stabilizing inner components first [15]) this problem does not occur in
practice.
12

int p, c, s=nondet(), x = 0, y = 0;
p = s ? 1 : 2;                                                       I
while (nondet()) { // A(X)
    x++;                                                                 τ1
    c = 100;
    while (nondet()) { // B(X)
                                                             τe      A
        if (p != 1 && p != 2) {
            c = 0;                                                       τ2   τ4
        }
        y++;                                                τ3       B
    }
    assert(c == 100);
}
assert((s && p == 1) || (!s && p == 2));


        Fig. 3: Example Program with Nested Loops: Listing and CFA.

5.1   Example Formula Slicing Run
Consider running formula slicing on the program in Fig. 3, which contains two
nested loops. The corresponding edge encoding is given in Eq. 7:

               τ1 ≡x0 = 0 ∧ y 0 = 0 ∧ (p0 = 1 ∧ s0 ∨ p0 = 2 ∧ ¬s0 )
               τ2 ≡x0 = x + 1 ∧ c0 = 100
               τ3 ≡(¬(p 6= 1 ∧ p 6= 2) ∨ (p 6= 1 ∧ p 6= 2 ∧ c0 = 0))
                    ∧ y 0 = y + 1 ∧ p0 = p
               τ4 ≡x0 = x ∧ y 0 = y ∧ p0 = p ∧ c0 = c                              (7)
    Similarly to Eq. 3, we can check candidate invariants A(X), B(X) for induc-
tiveness by posing an SMT query shown in Eq. 8. The constraint in Eq. 8 is
unsatisfiable iff {A : A(X), B : B(X)} is an inductive invariant (Sec. 2.3).

                                              τ1 (X 0 ) ∧ ¬A(X 0 )
                              _ A(X) ∧ τ2 (X ∪ X 0 ) ∧ ¬B(X 0 )
                   ∃X ∪ X 0                                                        (8)
                                 B(X) ∧ τ3 (X ∪ X 0 ) ∧ ¬B(X 0 )
                                 B(X) ∧ τ4 (X ∪ X 0 ) ∧ ¬A(X 0 )
   Eq. 8 is unsatisfiable iff all of the disjunction arguments are unsatisfiable,
and hence the checking can be split into multiple steps, one per analyzed edge.
Each postcondition computation (Alg. 3) either generates an initial seed invariant
candidate, or picks one argument of Eq. 8, and weakens the right hand side until
the constraint becomes unsatisfiable. Run of the formula slicing algorithm on the
example is given below:
 – Traversing
           V τ1 , we get the initial candidate invariant
   I(A) ← {x = 0, y = 0, p = 1 ∨ p = 2, s =⇒ p = 1}.
 – Traversing
           V τ2 , the candidate invariant for B becomes
   I(B) ← {x = 1, y = 0, p = 1 ∨ p = 2, s =⇒ p = 1, c = 100}.
                                                                                13

 – After traversing τ3 , we weaken the candidate invariant I(B) by dropping the
   lemma y = 0 which gives rise   V to the counterexample to induction (y gets
   incremented). The result is {x = 1, p = 1 ∨ p = 2, s =⇒ p = 1, c = 100},
   which is inductive under τ3 .
 – The edge τ4 is an identity, and the postcondition computation
                                                             V         results in
   lemmas x = 0 and y = 0 dropped from I(A), resulting in {y = 0, p = 1 ∨ p =
   2, s =⇒ p = 1}.
 – After traversing τ2 , we obtain Vthe weakening of I(A) by dropping the lemma
   x = 1 from I(B), resulting in {p = 1 ∨ p = 2, s =⇒ p = 1, c = 100}.
 – Finally, the iteration converges, as all further postconditions are already
   covered by existing invariant candidates. Observe that the computed invariant
   is sufficient for proving the asserted property.

6     Implementation
We have developed the Slicer tool, which runs the formula slicing algorithm on
an input C program. Slicer performs inductive weakenings using the Z3 [16]
SMT solver, and best-effort quantifier elimination using the qe-light Z3 tac-
tic. The source code is integrated inside the open-source verification frame-
work CPAchecker [17], and the usage details are available at http://slicer.
metaworld.me. Our tool can analyze a verification task (Sec. 2.2) by finding an
inductive invariant and reporting true if the found invariant separates the initial
state from the error property, and unknown otherwise.
    We have implemented the following optimizations:
Live Variables We precompute live variables, and the candidate lemmas gen-
   erated during RCNF conversion (Alg. 3, line 6) which do not contain live
   variables are discarded.
Non-Nested Loops When performing the inductive weakening (Alg. 3, line 4)
   on the edge (N, τ, N ) we annotate and weaken the candidate invariants on
   both sides (without modifications described in Sec. 3.1), and we cache the
   fact that the resulting weakening is inductive under τ .
CFA Reduction We pre-process the input CFA and we remove all nodes from
   which there exists no path to an error state.

6.1   Syntactic Weakening Algorithm
A syntactic-based approach is possible as a faster and less precise alternative
which does not require SMT queries. For an input formula φ(X) in RCNF, and a
transition τ (X ∪ X 0 ), syntactic weakening returns a subset of lemmas in φ, which
are not syntactically modified by τ : that is, none of the variables are modified
or have their address taken. For example, the lemma x > 0 is not syntactically
modified by the transition y 0 = y + 1 ∧ x ≥ 1, but it is modified by x0 = x + 1.

7     Experiments and Evaluation
We have evaluated the formula slicing algorithm on the “Device Drivers” category
from the International Competition on Software Verification (SV-COMP) [2].
14

The dataset consists of 2120 verification tasks, of which 1857 are designated as
correct (the error property is unreachable), and the rest admit a counter-example.
All the experiments were performed on Intel Xeon E5-2650 at 2.00 GHz, and
limits of 8GB RAM, 2 cores, and 600 seconds CPU time per program. We compare
the following three approaches:
Slicer-CEX (rev 21098) Formula slicing algorithm running counterexample-
   based weakening (Sec. 3).
Slicer-Syntactic Same, with syntactic weakening (Sec. 6.1).
Predicate Analysis (rev 21098) Predicate abstraction with interpolants [18],
   as implemented inside CPAchecker [19]. We have chosen this approach for
   comparison as it represents state-of-the-art in model checking, and was found
   especially suitable for analyzing device drivers.
PAGAI [20] (git hash e44910) Abstract interpretation-based tool, which im-
   plements the path focusing [1] approach.
Unabridged experimental results are available at http://slicer.metaworld.me.
    In Tab. 1 we show overall precision and performance of the four compared
approaches. As formula slicing is over-approximating, it is not capable of finding
counterexamples, and we only compare the number of produced safety proofs.
    From the data in the table we can see that predicate analysis produces the
most correct proofs. This is expected since it can generate new predicates, and it is
driven by the target property. However, formula slicing and abstract interpretation
have much less timeouts, and they do not require target property annotation,
making them more suitable for use in domains where a single error property is
not available (advanced compiler optimizations, multi-property verification, and
boosting another analysis by providing an inductive invariant). The programs
verified by different approaches are also different, and formula slicing verifies 22
programs predicate analysis could not.
    The performance of the four analyzed approaches is shown in the quantile
plot in Fig. 4a. The plot shows that predicate analysis is considerably more time
consuming than other analyzed approaches. Initially, PAGAI is much faster than
other tools, but around 15 seconds it gets overtaken by both slicing approaches.
Though the graph seems to indicate that PAGAI overtakes slicing again around
100 seconds, in fact the bend is due to out of memory errors.
    The quantile plot also shows that the time taken to perform inductive weak-
ening does not dominate the overall analysis time for formula slicing. This can be
seen from the small timing difference between the syntactic and counterexample-
based approaches, as the syntactic approach does not require querying the SMT
solver in order to produce a weakening.
    Finally, we present data on the number of SMT calls required for computing
inductive weakenings in Fig. 4b. The distribution shows that the overwhelming
majority of weakenings can be found within just a few SMT queries.

8    Conclusion and Future Work
We have proposed a “formula slicing” algorithm for efficiently finding potentially
disjunctive inductive invariants in programs, which performs abstract interpreta-
                                                                                                                                             15


                           Tool                   # proofs # incorrect # timeouts # memory outs
                           Slicer-CEX                 1253                                    0            475                    0
                           Slicer-Syntactic           1166                                    0            407                    0
                           Predicate Analysis         1301                                    0            657                    0
                           PAGAI                      1214                                    3            409                  240

                  Table 1: Evaluation results. The “# incorrect” column shows the number of
                  safety proofs the tool has produced where the analyzed program admitted a
                  counterexample.


                 103
                           Slicer-CEX
                           Slicer-Syntactic
                                                                                              105




                                                                  Required for # weakenings
                           Predicate Analysis
                           PAGAI
                 102
Wall Time (s)




                                                                                              104


                                                                                              103
                 101
                                                                                              102


                 100                                                                          101
                       0       500      1,000     1,500   2,000                                     1 4 8 12 16 20 24 28 32 36 40 44 48 52 56 60 64
                                       Programs                                                                     # SMT queries


                (a) Quantile plot showing performance of          (b) Distribution of the number of iterations
                the compared approaches. Shows analysis           of inductive weakening (Sec. 3) required for
                time for each benchmark, where the data           convergence across all benchmarks. Horizon-
                series are sorted by time separately for each     tal axis represents the number of SMT calls
                tool. For readability, the dot is drawn for       required for convergence of each weakening,
                every 20th program, and the time is rounded       and vertical axis represents the count of the
                up to one second.                                 number of such weakenings.

                  tion in the space of weakenings over the formulas representing the “initial” state.
                  We have demonstrated that it could verify many programs other approaches
                  could not, and that the algorithm can be run on real programs.
                      The motivation for our approach is addressing the limitation of abstract
                  interpretation which forces it to perform abstraction after each analysis step,
                  which often results in a very rough over-approximation. Thus we believe our
                  method is well-suited for augmenting numeric abstract interpretation.
                      As with any new inductive invariant generation technique, a possible future
                  work is investigating whether formula slicing can be used for increasing the
                  performance and precision of other program analysis techniques, such as k-
                  induction, predicate abstraction or property-directed reachability. An obvious
                  approach would be feeding the invariants generated by formula slicing to a convex
                  analysis running abstract interpretation or policy iteration [21].
16

    Furthermore, the inductive weakening approach could also be used for the
generalization of the k-induction algorithm over multiple properties. If weVcheck
a set of properties P for inductiveness under the loop transition τ , and P is
not inductive, the weakening can find the largest inductive subset.
Acknowledgements The authors wish to thank Grigory Fedyukovich and
Alexey Bakhirkin for proof-reading and providing valuable feedback, and the
anonymous reviewers for their helpful suggestions.

References
 1. D. Monniaux and L. Gonnord, “Using bounded model checking to focus fixpoint
     iterations,” in SAS. Springer, 2011.
 2. D. Beyer, “Reliable and reproducible competition results with benchexec and
    witnesses (Report on SV-COMP 2016),” in TACAS. Springer, 2016.
 3. C. Flanagan and K. R. M. Leino, “Houdini, an annotation assistant for ESC/Java,”
     in FME, 2001, pp. 500–517.
 4. C. Flanagan, R. Joshi, and K. R. M. Leino, “Annotation inference for modular
     checkers,” Information Processing Letters, 2001.
 5. A. R. Bradley and Z. Manna, “Checking safety by inductive generalization of
     counterexamples to induction,” in FMCAD, 2007, pp. 173–180.
 6. S. Graf and H. Saı̈di, “Construction of abstract state graphs with PVS,” in CAV,
    1997, pp. 72–83.
 7. T. Reps, M. Sagiv, and G. Yorsh, “Symbolic implementation of the best transformer,”
     in VMCAI, 2004.
 8. A. Komuravelli, A. Gurfinkel, S. Chaki, and E. M. Clarke, “Automatic abstraction
     in SMT-based unbounded software model checking,” in CAV, 2013, pp. 846–862.
 9. A. Gurfinkel, A. Belov, and J. Marques-Silva, “Synthesizing safe bit-precise invari-
     ants,” in TACAS, 2014, pp. 93–108.
10. S. K. Lahiri and S. Qadeer, “Complexity and algorithms for monomial and clausal
     predicate abstraction,” in CADE, 2009, pp. 214–229.
11. P. Cousot and R. Cousot, “Abstract Interpretation: A Unified Lattice Model for
     Static Analysis of Programs by Construction or Approximation of Fixpoints,” in
    POPL, 1977, pp. 238–252.
12. D. Beyer, A. Cimatti, A. Griggio, M. E. Keremoglu, and R. Sebastiani, “Software
     model checking via large-block encoding,” in FMCAD, 2009, pp. 25–32.
13. D. Beyer, T. A. Henzinger, R. Jhala, and R. Majumdar, “The software model
     checker Blast,” STTT, vol. 9, no. 5-6, pp. 505–525, 2007.
14. D. Kroening, N. Sharygina, S. Tonetta, A. Tsitovich, and C. M. Wintersteiger,
    “Loop summarization using abstract transformers,” in ATVA, 2008, pp. 111–125.
15. F. Bourdoncle, “Efficient chaotic iteration strategies with widenings,” in Formal
    Methods in Programming and Their Applications, ser. Lecture Notes in Computer
     Science. Springer Berlin Heidelberg, 1993, vol. 735, pp. 128–141.
16. L. M. de Moura and N. Bjørner, “Z3: an efficient SMT solver,” in TACAS, 2008,
     pp. 337–340.
17. D. Beyer and M. E. Keremoglu, “CPAchecker: A tool for configurable software
    verification,” in CAV, 2011, pp. 184–190.
18. K. L. McMillan, “Lazy abstraction with interpolants,” in CAV, 2006, pp. 123–136.
19. D. Beyer, M. E. Keremoglu, and P. Wendler, “Predicate abstraction with adjustable-
     block encoding,” in FMCAD, 2010, pp. 189–197.
                                                                                 17

20. J. Henry, D. Monniaux, and M. Moy, “PAGAI: A path sensitive static analyser,”
    Electr. Notes Theor. Comput. Sci., vol. 289, pp. 15–25, 2012.
21. E. G. Karpenkov, D. Monniaux, and P. Wendler, “Program analysis with local
    policy iteration,” in VMCAI. Springer, 2016, pp. 127–146.
22. L. J. Stockmeyer, “The polynomial-time hierarchy,” Theoretical Computer Science,
    vol. 3, no. 1, pp. 1–22, 1976.
18

A     Complexity of Finding a Non-Trivial Inductive
      Weakening Over Literals
As we have mentioned in Sec. 4, a more expressive space of weakenings over
formulas is to consider replacing any subset of literals with > after a NNF
conversion. In this appendix we show that it leads to a number of undesirable
properties, including the absence of strongest inductive weakening (Ex. 1), and
Σ2p complexity for finding any non-trivial inductive weakening (Thm. 1).

Example 1 (No Strongest Inductive Weakening). Consider a program over four
Boolean variables a, b, c, d and the transition relation τ ≡ a ∧ b ∧ c ∧ d ∧ ¬a0 ∧
b0 ∧ ¬c0 ∧ d0 (the only possible transition is from a ∧ b ∧ c ∧ d to ¬a ∧ b ∧ ¬c ∧ d).
Consider finding the weakening of φ ≡ (a ∧ b) ∨ (c ∧ d), Both the {a}-weakening
(b∨(c∧d)) and the {c}-weakening ((a∧b)∨d) are inductive, but their intersection
(a ∧ b) ∨ (b ∧ d) ∨ (c ∧ d) (obviously inductive) is not a weakening of φ and there
is no inductive weakening stronger than either of these.

Theorem 1 (Σ2p -completeness). The problem of deciding, given quantifier-
free SMT formulas φ(X) and τ (X ∪ X 0 ), whether there exists a non-trivial (6≡ >)
weakening of φ that is inductive with respect to τ is Σ2p -complete.

Proof (Belonging to Σ2p ). Let S be some subset of literals of φ. Let φ̂ be the
weakening of φ where all literals in S are replaced with >. Checking that φ̂
is inductive with respect to τ is in co-NP, therefore the problem of finding a
non-trivial φ̂ is in Σ2p

   We show completeness by constructing from an arbitrary closed ∃∗ ∀∗ formula
ψ a loop τ and a precondition I such that the existence of a non-trivial (6≡ >)
weakening of the precondition is equivalent to the truth of ψ. Without loss of
generality, let ψ have m Boolean variables x0 , . . . , xm−1 bound by the existential
quantifier and n Boolean variables y0 , . . . , yn−1 bound by the universal one:
                  ψ ≡∃x0 , . . . , xm−1 .
                                                                                        (9)
                       ∀y0 , . . . , yn−1 .G(x0 , . . . , xm−1 , y0 , . . . , yn−1 )
Let us denote the bitvector (x0 , . . . , xm−1 ) as X and the bitvector (y0 , . . . , yn−1 )
as Y . Let enc : Bm → [0, 2m − 1] denote the function for standard integer
encoding of the X bitvector, x0 being the lowest-order bit and xm−1 the highest-
order one. Let succ : Bm \ {>m } → Bm be the successor function such that
enc(succ(X)) = 1 + enc(succ(X)), which is only defined for non-overflowing
values.
   Now we define the transition system over the set of boolean variables X and
the overflow bit o. Let the initial state I(X, o) be X = ⊥ ∧ o = ⊥, and let the
transition relation τ (X, X 0 , o, o0 ) to be:
              ¬(∀Y.G(X, Y ))∧
             ((X 6= > ∧ X 0 = succ(X) ∧ o0 = o) ∨ (X = > ∧ o0 = >))
                                                                   
                                                                                       (10)
             _
                 X 0 = X ∧ o0 = o
                                  
                                                                                      19



    bitvector X = ⊥;
    boolean o = ⊥ ;
    while ( nondet ( ) ) {
        // Non−d e t e r m i n i s t i c c h o i c e .
        b i t v e c t o r Y = nondet ( ) ;
        i f ( not G(X, Y ) ) {
                i f ( X == > ) {                                            I(X, o)
                        // S e t t h e o v e r f l o w
                        // b i t .                                      A
                        o = >;
                        X = nondet ( ) ;
                                                                τ (X, X 0 , o, o0 )
                } else {
                        // Increment a g i v e n
                        // b i t v e c t o r .
                        X = succ (X ) ;
                }
        }
    }


                   Fig. 4: Counter Program and Transition System
In plain terms, the transition relation may increment X as long as it is not
overflowing and the guard can be falsified for some Y , and X is forced to stay
constant on overflow or when it reaches some X̂ such that ∀Y.G(X̂, Y ). Initial-
ization and transition relation for the transition system, and the corresponding
program are shown in Fig. 4.
Lemma 1. There exists a non-trivial (6≡ >) inductive invariant for the program
in Fig. 4 if and only if ψ (Eq. 9) is satisfiable.
    Observe that τ can be satisfied for all possible values of X by a suitable choice
of X 0 . Let f (X) be the largest (under enc) possible value of X 0 which satisfies
τ (X, X 0 , o, o0 ).
Proof. Sufficient Condition. Assume ψ is satisfiable for some X̂. Then X̂ is a
fixed point under f (as it satisfies G for all possible values of Y ). Consider the
set of values defined by R ≡ ¬o ∧ enc(X) ≤ X̂}. It is inductive, since the largest
value in R set maps to itself under f , and all other values map to the “next”
(under enc) value in R. It is also non-trivial, since the bit o is defined not to be
>.
Proof. Necessary Condition. Assume there exists a non-trivial inductive invariant
for the program in Fig. 4. At every transition, X either stays constant or is
incremented by 1. Since we have assumed the existence of a non-trivial inductive
invariant, there exists X̂ such that it is a fixpoint under f and enc(X̂) ≤
2m − 1 (otherwise the entire state space is reachable, and the only possible
inductive invariant is >). This is only possible if ∀Y.G(X̂, Y ) (otherwise x̂ may
be incremented). But this is exactly the condition for ψ being satisfiable.
20

Corollary 1. For every non-trivial inductive invariant of the program in Fig. 4
there exists some X̂ such that {X | enc(X) < enc(X̂)} is inductive. Furthermore,
the reachable state space is exactly all X smaller (under enc) than X̂, and
{X | X 6= X̂} is inductive (as the states larger than X̂ are not reachable).
    Now consider finding inductive (with respect to τ Fig. 4) weakenings of the
following formula φ:               _
                              φ ≡ (xi ∧ ¬xi )                              (11)
Each xi represents i’th bit of X. Observe that for any X̂ ∈ [0, 2m − 1], we can
weaken φ to be equivalent to X 6= X̂, by making a suitable weakening choice for
every i’th bit of X̂ (if the i-th bit in X̂ is ⊥ we replace ¬xi by >, if it is > we
replace xi by >).
    From Corollary 1 we know that for every non-trivial inductive invariant there
exists X̂, s.t. the set of all X not equal to X̂ is inductive. Thus if a non-trivial
inductive invariant exists, there exists a non-trivial inductive weakening of φ. In
Lemma 1 we have shown that deciding the existence of a non-trivial inductive
invariant is as hard as deciding the satisfiability of an arbitrary ∃∗ ∀∗ formula ψ,
thus deciding an existence of a non-trivial inductive weakening is as hard as well.

Proof (Σ2p -completeness). Membership in Σ2p is proved in Lemma 1. Reduction
from the Σ2p -complete problem is done from deciding the truth of ∃∗ ∀∗ propo-
sitional formulas [22, Th. 4.1]. Transforming G into τ can be done within a
logarithmic working space.

Relationship to Template Abstraction Complexity Lahiri and Qadeer
[10] consider the problem of template abstraction: given a precondition, a post-
condition, a transition relation and a formula φ(C, X), C and X being sets of
Boolean variables, check whether an appropriate choice of C makes φ an induc-
tive invariant. They show this problem to be Σ2p -complete as well. Our class of
problems is a strict subset of theirs (our weakening problems can be immediately
translated into template abstraction problems, but not all template abstraction
problems correspond to weakenings), but we still show completeness.
