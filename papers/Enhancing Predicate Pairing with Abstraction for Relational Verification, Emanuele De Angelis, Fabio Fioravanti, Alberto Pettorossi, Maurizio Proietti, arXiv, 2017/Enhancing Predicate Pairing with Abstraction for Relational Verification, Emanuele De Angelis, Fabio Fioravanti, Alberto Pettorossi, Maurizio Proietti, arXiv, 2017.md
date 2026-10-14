                                             Enhancing Predicate Pairing with Abstraction
                                                     for Relational Verification?

                                                               Emanuele De Angelis1 , Fabio Fioravanti1 ,
                                                              Alberto Pettorossi2,3 , and Maurizio Proietti3
                                                        1
                                                            DEC, University ‘G. d’Annunzio’, Chieti-Pescara, Italy
                                                            {emanuele.deangelis,fabio.fioravanti}@unich.it
                                                              2
                                                                DICII, University of Rome ‘Tor Vergata’, Italy
                                                                      pettorossi@info.uniroma2.it
                                                                        3
                                                                           IASI-CNR, Rome, Italy
                                                                     maurizio.proietti@iasi.cnr.it
arXiv:1709.04809v1 [cs.LO] 14 Sep 2017




                                                 Abstract. Relational verification is a technique that aims at proving
                                                 properties that relate two different program fragments, or two different
                                                 program runs. It has been shown that constrained Horn clauses (CHCs)
                                                 can effectively be used for relational verification by applying a CHC
                                                 transformation, called predicate pairing, which allows the CHC solver to
                                                 infer relations among arguments of different predicates. In this paper
                                                 we study how the effects of the predicate pairing transformation can be
                                                 enhanced by using various abstract domains based on linear arithmetic
                                                 (i.e., the domain of convex polyhedra and some of its subdomains) during
                                                 the transformation. After presenting an algorithm for predicate pairing
                                                 with abstraction, we report on the experiments we have performed on
                                                 over a hundred relational verification problems by using various abstract
                                                 domains. The experiments have been performed by using the VeriMAP
                                                 transformation and verification system, together with the Parma Poly-
                                                 hedra Library (PPL) and the Z3 solver for CHCs.


                                         1     Introduction

                                         Relational program properties are properties that relate two different programs or
                                         two executions of the same program. Relational properties that have been stud-
                                         ied in the literature include program equivalence, non-interference for software
                                         security, and relative correctness [4, 5, 30].
                                             Recent work has advocated the use of Constrained Horn Clauses (CHCs)
                                         for the verification of relational program properties [16, 21, 36]. These methods
                                         translate a verification problem into a set of Horn clauses with constraints in a
                                         suitable domain (usually, Linear Arithmetic), and then verify the satisfiability
                                         of those clauses by using SMT solvers for Horn clauses, called here CHC solvers,
                                         such as Z3 [17] or Eldarica [27].
                                         ?
                                             This work has been partially funded by INdAM-GNCS (Italy). E. De Angelis,
                                             F. Fioravanti, and A. Pettorossi are research associates at IASI-CNR, Rome, Italy.
2

    The main difficulty encountered by CHC solvers when verifying relational
properties is that these solvers find models of single predicates expressed in
terms of Linear Arithmetic constraints, whereas the proof of relational proper-
ties often requires the discovery of relations among arguments of two (or more)
distinct predicates. To mitigate this difficulty, Predicate Pairing transforms a set
of clauses defining two predicates, say p and q, into a new set of clauses defining
a new predicate, say r, equivalent to the conjunction of p and q [16]. Thus, when
the CHC solver finds a model for the predicate r, it discovers relations among
the arguments of p and q.
    In the approach presented in this paper we use Predicate Pairing together
with Abstraction. Abstraction is a technique that is often used in program anal-
ysis and transformation, and consists in mapping the concrete semantics of a
program into an abstract domain, where some program properties can more
easily be verified [8]. In the context of the verification of relational properties,
Predicate Pairing combined with a basic form of abstraction has been introduced
in a previous paper [16]. In that paper, in fact, Predicate Pairing is performed
by introducing new definitions whose bodies are made out of two atoms whose
predicates are the ones to be paired, together with the equalities between the
arguments of these predicates, and these equality constraints can be viewed as
an abstraction into the domain of equalities.
    Abstraction is also used by CHC Specialization, which is another transfor-
mation technique that has been proposed to increase the effectiveness of CHC
solvers [11, 28]. CHC Specialization propagates constraints through the clauses
of the program, and since propagation often causes strengthening of the con-
straints, it is possible that by first specializing programs, the task of CHC solv-
ing is much facilitated. However, the impact of the specialization process very
much depends on the choices of the particular abstract domain and associated
widening operator, which are used when specialized predicates are introduced or
manipulated.
    In this paper we address the problem of evaluating various combinations of
Predicate Pairing, Abstraction, and CHC Specialization for the specific objective
of verifying relational properties of programs. In order to do so, we introduce a
general algorithm for Predicate Pairing that is parametric with respect to the ab-
stract constraint domain that is used. This domain is taken to be a subdomain of
Linear Arithmetic, such as Convex Polyhedra, Boxes, Bounded Differences, and
Octagons [3, 9, 35]. Our parametric Abstraction-based Predicate Pairing algo-
rithm generalizes the one that makes use of equalities between variables that has
been used in a previous paper of ours [16]. We also consider a CHC Specializa-
tion algorithm that is parametric with respect to the abstract constraint domain.
Then we consider various compositions of Abstraction-based Predicate Pairing
and CHC Specialization, by varying the abstract constraint domain used.
    These compositions of transformations are applied to sets of CHCs encoding
relational properties of imperative programs. The lesson one may learn from the
results of our experiments is that the transformations achieving the best results
make use of constraint domains that are expressive enough to describe relations
                                                                                 3

between variables (such as, Bounded Differences and Octagons), without re-
quiring the higher precision of Convex Polyhedra. Moreover, Abstraction-based
Predicate Pairing essentially incorporates the effect of CHC Specialization, and
thus extra specializations (before or after Abstraction-based Predicate Pairing)
are not cost-effective.
    The paper is organized as follows. In Section 2 we present an introductory
example showing the usefulness of abstraction. Then, in Section 3 we present the
various abstract constraint domains, that is, Convex Polyhedra, Boxes, Bounded
Differences, and Octagons, and the operations defined on them. In Section 4
we present the Abstraction-based transformation techniques for CHCs and we
prove that they preserve satisfiability (and unsatisfiability). The implementation
of the verification method, based on the Parma Polyhedra Library for constraint
manipulation [3] and on the Z3 solver for CHC satisfiability, and its experimental
evaluation are reported in Section 5. Finally, in Section 6, we discuss the related
work on program transformation and verification.


2   An Introductory Example

In this section we present the proof of equivalence of two imperative programs
acting on integer variables. This equivalence can be proved by using our method
based on the Predicate Pairing strategy using a suitable abstract constraint
domain. By using Predicate Pairing without abstraction the proof cannot be
performed.
    Let us consider the programs P 1 and P 2 shown in Figure 2, where pro-
gram P 2 is obtained from program P 1 by applying a compiler optimization
technique, called software pipelining. This technique has the effect of allowing
more parallelism during execution.
    Software pipelining takes as input a program with a loop and produces an
improved program with a new loop whose instructions are taken from differ-
ent iterations of the original loop. Combined with other optimizations, software
pipelining can produce loops whose instructions have no read/write dependen-
cies and thus can be executed in parallel. For example, in program P 2 derived
by pipelining from program P 1, the dependency on x in the instructions of the
loop in P 2 can be removed by: (i) introducing a fresh variable u initialized to
the value of x, and (ii) replacing x by u on the right-hand side of the assign-
ments in the loop. After this replacement the resulting instructions ‘y = y+u;’
and ‘a = a+1; x = u+a;’ can be safely executed in parallel.
    The equivalence of programs P 1 and P 2 with respect to the output value
of x, can be expressed by the following clause F :
F : false ← X1 6= X2, s11(A, B, X, Y, X1, Y 1), s21(A, B, X, Y, X2, Y 2)
where: (i) predicates s11 and s21 represent the input/output relation of pro-
grams P 1 and P 2, respectively; (ii) A, B, X, Y represent the values of the
integer variables a, b, x, y at the beginning of program execution; (iii) X1, Y 1
and X2, Y 2 represent the values of the integer variables x and y at the end of the
4
     P1 :                               P2 :    if (a < b) {
                                                   x = x+a;
              while (a < b) {                      while (a < b-1) {
                 x = x+a;                             y = y+x;
                 y = y+x;                             a = a+1;
                 a = a+1;                             x = x+a;
              }                                    }
                                                   y = y+x;
                                                   a = a+1;
                                                }

Fig. 1. The input program P 1 and the output program P 2 obtained by applying soft-
ware pipelining.


execution of P 1 and P 2, respectively. In order to be processed by the constraint-
based techniques presented in this paper, which do not consider disequality (6=),
clause F is split into the following two clauses:
F 1 : false ← X1 ≤ X2−1, s11(A, B, X, Y, X1, Y 1), s21(A, B, X, Y, X2, Y 2)
F 2 : false ← X2 ≤ X1−1, s11(A, B, X, Y, X1, Y 1), s21(A, B, X, Y, X2, Y 2)
    The clauses defining s11 and s21 (and the predicates s12, s22, and s23 on
which they depend) are reported below. (The unfamiliar reader may refer, for
instance, to [15], where the technique for generating clauses from imperative pro-
grams is presented.) Note, for example, that predicates s12 and s23 correspond
to the loops in programs P 1 and P 2, respectively. Note also that strict inequal-
ities occurring in programs (for instance, a < b in program P 1) are represented
by using non-strict inequalities in clauses (A ≤ B−1 in the first clause for s12).
s11(A, B, X, Y, X2, Y 2) ← s12(A, B, X, Y, A2, B2, X2, Y 2).
s12(A, B, X, Y, A2, B2, X2, Y 2) ← A ≤ B −1, X1 = A+X, Y 1 = Y +X1,
                         A1 = A+1, s12(A1, B, X1, Y 1, A2, B2, X2, Y 2).
s12(A, B, X, Y, A, B, X, Y ) ← A ≥ B.
s21(A, B, X, Y, X2, Y 2) ← s22(A, B, X, Y, A2, B2, X2, Y 2).
s22(A, B, X, Y, A2, B2, X2, Y 2) ← A ≤ B −1, X1 = X +A,
                         s23(A, B, X1, Y, A2, B2, X2, Y 2).
s22(A, B, X, Y, A, B, X, Y ) ← A ≥ B.
s23(A, B, X, Y, A2, B, X, Y 2) ← A ≥ B −1, Y 2 = Y +X, A2 = A+1.
s23(A, B, X, Y, A2, B2, X2, Y 2) ← A ≤ B −2, Y 1 = Y +X, A1 = A+1,
                         X1 = X +A1, s23(A1, B, X1, Y 1, A2, B2, X2, Y 2).
Let P be the set of clauses defining s11 and s21 and the predicates on which they
depend. By proving the satisfiability of {F 1, F 2}∪P , we prove that programs P 1
and P 2 produce identical values for x as output, when provided with the same
input values. For reasons of simplicity we only consider the subset {F 1}∪P . The
satisfiability of the larger set can be proved by applying the same technique.
    Unfortunately, a state-of-the-art CHC solver such as Z3 [17] fails to prove
the satisfiability of {F 1} ∪ P . This inability is due to the fact that Z3 computes
models of single predicates expressed in terms of linear constraints, and it can
be shown that non-linear constraints among the arguments of each predicate s11
                                                                                     5

and s21 need be discovered to prove that the two atoms in the body of clause F 1
imply X1 > X2−1.
    The Predicate Pairing strategy we have introduced in a previous paper [16]
may help in overcoming this difficulty. By Predicate Pairing we may introduce
new predicates defined in terms of two (or more) atoms, and infer relations among
arguments of distinct predicates. Indeed, models of single predicates derived
by Predicate Pairing, correspond to models of pairs (that is, conjunctions) of
predicates before Predicate Pairing. Unfortunately, it is the case that also the
set of clauses derived from {F 1} ∪ P by ‘simple’ Predicate Pairing, that is,
without adding any constraint to the arguments of the paired predicates, cannot
be proved satisfiable by Z3.
    However, if we enhance our Predicate Pairing strategy by allowing in the new
definitions the addition of constraints taken from the abstract domain of Convex
Polyhedra, then Z3 is indeed able to prove the satisfiability of the derived set of
clauses, and hence of the equisatisfiable set {F 1} ∪ P .
    To get this result, we have implemented in the VeriMAP transformation sys-
tem [12] a new version of the Predicate Pairing strategy enhanced with abstrac-
tion techniques based on Convex Polyhedra (as well as other abstract constraint
domains such as Boxes, Bounded Differences, and Octagons). In our example,
Predicate Pairing enhanced with abstraction on Convex Polyhedra introduces
the following definitions (variables are automatically renamed by VeriMAP):
pp1(A, B, C, D, E, F, G, H, A, B, C, D, I, J, K, L) ← G ≤ K −1,
          s12(A, B, C, D, E, F, G, H), s22(A, B, C, D, I, J, K, L).
pp2(A, B, C, D, E, F, G, H, A, B, K, D, M, N, O, P ) ← G ≤ O−1, A ≤ B −1,
          K = A+C, s12(A, B, C, D, E, F, G, H), s23(A, B, K, D, M, N, O, P ).
and derives the following final set of clauses:
false ← X1 ≤ X2−1, pp1(A, B, C, D, E, F, X1, H, A, B, C, D, I, L, X2, N ).
pp1(A, B, C, D, E, F, G, H, A, B, C, D, I, J, K, L) ← G ≤ K −1, A ≤ B −1,
          M = A+C, pp2(A, B, C, D, E, F, G, H, A, B, M, D, I, J, K, L).
pp2(A, B, C, D, E, F, G, H, A, B, K, D, M, N, O, P ) ← G ≤ O−1, A ≤ B −2,
          K = A+C, R = A+1, T = A+C, S = D+T, X = A+1, W = K +X,
          Y = D+K, pp2(R, B, T, S, E, F, G, H, X, B, W, Y, M, N, O, P ).
Now, the satisfiability of this set of clauses is trivial, and is easily checked by Z3,
because it contains no constrained facts (that is, clauses with only constraints
in their body), and hence a model is obtained by taking both pp1 and pp2 to be
false.
    The constraints occurring in the new predicate definitions are crucial for
deriving a set of clauses without constrained facts. Indeed, it can easily be shown
that if we introduce a predicate defined by a conjunction of predicates with
distinct variables as arguments (that is, we perform ‘simple’ Predicate Pairing),
then by unfolding the definition of that predicate we generate constrained facts
derived from those of s12 and s22.
   The equivalence of the two programs P 1 and P 2 with respect to the output
value of y can be proved in a similar way.
6

3   Constrained Horn Clauses over Numerical Domains

Let us recall some basic notions about: (i) abstract domains often used in static
program analysis [8], and (ii) constrained Horn clauses (CHCs).
    We consider the abstract domain of Convex (Closed) Polyhedra [3, 10], CP
for short, whose atomic constraints are of the form a1 · x1 + . . . + an · xn ≤ a,
where a’s and x’s are real coefficients and variables, respectively. A constraint c
is either true, or false, or an atomic constraint, or a conjunction of constraints.
    Given a formula F , by ∀(F ) and ∃(F ) we denote its universal and existential
closure, respectively. By vars(F ) we denote the set of variables occurring in F .
A constraint c is said to be satisfiable if CP |= ∃(c). Given two constraints c
and d, we say that c entails d, and we write c v d, if CP |= ∀(c → d). We say
that c and d are equivalent if c v d and d v c.
    We also consider some other abstract constraint domains, namely Octagons,
Bounded Differences, and Boxes, which are subdomains of Convex Polyhedra
in the sense that they are defined by putting restrictions on the form of the
polyhedra associated with the atomic constraints. These abstract domains have
all true and false as constraints and are closed under conjunction.
    The atomic constraints of the Octagons domain are inequalities of the form
a1 · x1 + a2 · x2 ≤ a, where a ∈ R and ai ∈ {−1, 0, 1}, for i = 1, 2. The atomic
constraints of the Bounded Differences domain are inequalities of the form
a1 · x1 + a2 · x2 ≤ a, where a ∈ R, ai ∈ {−1, 0, 1}, for i = 1, 2, and a1 is dif-
ferent from a2 . The atomic constraints of the Boxes domain are inequalities of
the form x ≤ a, where a ∈ R.
    Each abstract constraint domain D ⊆ CP is endowed with some operators
that we now define. Let c and d be two constraints in D, or D-constraints.
    The least upper bound operator is a function t : D × D → D such that
(i) c v c t d, (ii) d v c t d and (iii) for all D-constraints e, if c v e and d v e,
then c t d v e.
    A widening operator is a function ∇ : D × D → D such that (i) c v c∇d,
(ii) d v c∇d, and (iii) for all chains y0 v y1 v . . ., the chain x0 v x1 v . . . ,
where x0 = y0 and, for i > 0, xi+1 = xi ∇yi+1 , is finite.
    The abstraction operator for a subdomain D of CP, is a function α : CP → D
such that (i) c v α(c), and (ii) for all D-constraints e, if c v e, then α(c) v e.
    The projection of a D-constraint c onto a set X of variables, denoted c ⇓ X,
is a D-constraint c0 , with variables in X, which is equivalent to ∃Y.c, where
Y = vars(c)−X. Clearly, c v c0 .
    An atom is a formula of the form p(X1 , . . . , Xm ), where p is a predicate
symbol different from ‘≤’ and X1 , . . . , Xm are distinct variables.
    A constrained Horn clause (or simply, a clause, or a CHC) is an implication
of the form A ← c, G (comma denotes conjunction), where the conclusion (or
head) A is either an atom or false, the premise (or body) is the conjunction
of a constraint c and a (possibly empty) conjunction G of atoms. The empty
conjunction is identified with true.
                                                                                   7

    We assume that variables occur distinct in the atoms of a clause, although
in the examples, for ease of reading, we feel free to write clauses with repeated
occurrences of the same variable.
    A set S of CHCs is said to be satisfiable if S ∪ CP has a model, or equiva-
lently, S ∪ CP 6|= false (as done above, we identify convex polyhedra with linear
arithmetic formulas).


4   Predicate Pairing with Abstraction

In this section we present an algorithm for transforming CHCs, called Abstrac-
tion-based Predicate Pairing (or APP strategy, for short), which combines Pred-
icate Pairing [16] with abstraction operators acting on a given constraint do-
main (see Figure 2). The APP transformation strategy preserves satisfiability of
clauses and has the objective of increasing the effectiveness of the satisfiability
check that is performed by the subsequent application of a CHC solver.
    The APP transformation strategy tuples together two or more predicates
into a single new predicate which is equivalent to their conjunction. As shown
in the example of Section 2, the interaction between the Predicate Pairing tech-
nique and the constraints among the variables of the predicates paired together
(or tupled together, if more than two), may ease the discovery of the relations
existing among the arguments of the individual predicates.
    The APP strategy is parametric with respect to: (i) the abstract constraint
domain which is considered, and (ii) a Partition operator that determines, given a
clause, which are the atoms to be tupled together by splitting any conjunction G
of atoms in the body of the clause into n (≥ 1) subconjunctions G1 , . . . , Gn . By
choosing the abstract constraint domain and the Partition operator in a suitable
way, we can derive other transformations, and in particular, the Predicate Pair-
ing strategy introduced in a previous paper [16], Linearization [13], and CHC
Specialization [11, 28]. For example, the Predicate Pairing strategy is derived by
taking the constraint domain to be the set of equalities between variables, and
the Partition operator to be the one which, given a clause, returns a suitable set
of pairs of atoms in its body [16].
    The APP strategy is realized by performing a sequence of applications of the
well-known unfold/fold rules [19]. In order to be self-contained, now we present
the version of the Unfolding rule used in this paper. The other rules will be
presented when describing the APP strategy. In the definition of the Unfolding
rule and in the definitions of the other rules as well, we assume, without loss of
generality, that: (i) every atom in a clause has distinct variables as arguments,
and (ii) two atoms have pairwise disjoint sets of variables, and hence the relations
among variables (including equalities) are explicitly written as constraints in the
body of the clause.
Unfolding Rule. Let P be a set of clauses and C be a clause of the form
H ← c, L, A, R, where A is an atom and L and R are (possibly empty) con-
junctions of atoms. Let us consider the set {A ← ci , Bi | i = 1, . . . , m} made out
8

of all the clauses in P whose head is A (after renaming). By unfolding C w.r.t. A
using P , we derive the set of clauses {(H ← c, ci , L, Bi , R) | i = 1, . . . , m}.
    The APP strategy constructs a tree Defs of definitions, that is, clauses whose
head predicates do not occur in the input set P of clauses. A definition D is said
to be a child of a definition C, and equivalently, C is said to be the parent of D,
if D is introduced to fold a clause derived by unfolding from clause C.
    The ancestor relation on Defs is the reflexive, transitive closure of the parent
relation.

Input: A set P ∪ {C} of clauses where C is a clause whose head predicate does not
occur in P .
Output: A set TransfCls of clauses.
Initialization: InCls := {C }; Defs is the tree made out of the root clause C only;
TransfCls := P ;
while there is a clause C in InCls of the form H ← c, B do
  • Unfolding: From clause C derive a set U(C) of clauses by unfolding C with
    respect to each atom occurring in its body using P ;
    • Clause Deletion: Remove from U (C) all clauses with an unsatisfiable constraint;
    • Definition & Folding:
      for every clause E ∈ U (C) of the form H ← d, G do
          Partition the conjunction G into n (≥ 1) subconjunctions G1 , . . . , Gn ;
          for i = 1, . . . , n do
             di := α(d) ⇓ Vi , where Vi is the set of variables in Gi ;
             if in Defs there is no clause newpi (Vi ) ← ei , Gi such that di v ei then
                if in Defs there is an ancestor clause of C of the form newq(Vi ) ← fi , Gi
                then Di := (newpi (Vi ) ← ai , Gi ), where ai = fi ∇(fi t di )
                else Di := (newpi (Vi ) ← di , Gi );
                InCls := InCls ∪ {Di }; add Di as a child of C in Defs;
          end-for;
          TransfCls := TransfCls ∪ {H ← d, newp1 (V1 ), . . . , newpn (Vn )};
          U (C) := U (C) − {E};
      end-for;
  InCls := InCls − {C};
end-while

        Fig. 2. The Predicate Pairing with Abstraction algorithm (APP strategy)

    Note that, by construction, every constraint, either ai or di , occurring in a
new definition Di introduced during the Definition & Folding phase, belongs
to the abstract constraint domain.
    The APP strategy terminates if there exists an integer k such that, for any
application of the Partition operator producing G1 , . . . , Gn , the size of each
Gi is bounded by k. For instance, the Predicate Pairing strategy presented in a
previous paper [16], guarantees that k = 2 is such an integer bound. Indeed, if this
bound exists, by the properties of the widening operator, the set of definitions
that can be introduced by APP (and hence the number of executions of the while
loop of the strategy) is finite.
                                                                                   9

    Moreover, from well-known correctness results for the unfold/fold rules [19],
it follows that the APP strategy preserves satisfiability.
Theorem 1 (Soundness of Predicate Pairing with Abstraction). Let the
set P ∪{C} of clauses be the input of the APP strategy. If the strategy terminates
and returns a set TransfCls of clauses, then P ∪ {C} is satisfiable iff TransfCls
is satisfiable.
    A CHC Specialization strategy with Abstraction, which we call ASp strategy,
can be derived by instantiating the APP strategy. The ASp strategy is obtained
by using the Partition operator that, given a conjunction of atoms A1 , . . . , An
in the body of a clause, returns n subconjunctions, each consisting of a single
atom Ai , for i = 1, . . . , n (that is, no predicate pairing is made). It has been
shown that CHC Specialization can be very useful for increasing the effectiveness
of satisfiability checkers [11, 15, 28].
    In the next section we will present the results of the experiments we have
performed by combining the APP strategy and the ASp strategy in various ways.
In particular, these results illustrate the role of abstract constraint domains for
Predicate Pairing, and they also show the usefulness of the APP strategy for
making CHC solvers more effective when performing satisfiability checking.

5   Experimental Evaluation
In this section we present the results of the experimental evaluation we have
performed for assessing the effectiveness and the efficiency of the APP strategy.
    We have implemented that strategy using the VeriMAP transformation sys-
tem [12] and the Parma Polyhedra Library [3]. Then, in order to check the
satisfiability of the clauses generated by the APP strategy we have used the Z3
solver [17]. The verification process is depicted in Figure 3.




Fig. 3. The verification process based on: (i) the APP strategy, (ii) the Parma Poly-
hedra Library, and (iii) the CHC solver Z3.


Implementation of the APP strategy. We have ported the VeriMAP tool from
SICStus Prolog 3.12.5 to SWI-Prolog 7.4.2 and we have extended its transfor-
mation engine so to use the abstract domains and the associated operations
provided by the Parma Polyhedra Library (PPL).
10

    In particular, we have considered the following abstract domains: (i) Universe
(that is, the whole n-dimensional space), (ii) Boxes, (iii) Bounded Differences
(also called Bounded Difference Shapes, or BDS, for short), (iv) Octagons (also
called Octagonal Shapes, or OS, for short), and (v) Convex Polyhedra, together
with the operations of projection, least upper bound, inclusion check (that is,
entailment), emptiness check (that is, satisfiability), and widening. We have used
Convex Polyhedra with the widening operator of Halbwachs [25] (CP-H), and
with the widening operator of Bagnara et al. [2] (CP-B). Predicate Pairing with
the Universe domain is the ‘simple’ Predicate Pairing we mentioned in Section 2,
that introduces new definitions having no constraints in their body.
    Since VeriMAP natively represents constraints using the Constraint Logic
Programming (CLP) syntax, we had to use the facilities provided by PPL for
constructing objects of the abstract domains starting from constraints repre-
sented in CLP, and vice versa, for constructing constraints represented in CLP
starting from PPL objects. We are currently working for overcoming the ineffi-
ciency due to these translations of representation.
Benchmark suite. We have considered a benchmark suite consisting of 136 sets
of CHCs, for a total number of 1655 clauses, representing verification problems
of various relational properties, such as loop optimizations, equivalence, mono-
tonicity, injectivity, functional dependency, and non-interference [4, 5, 13, 16, 21].
Experiments. We have performed the following six experiments, where the pa-
rameter x stands for an abstract constraint domain, which is either Universe, or
Boxes, or BDS, or OS, or CP-H, or CP-B:
0. Z3
1. ASp(x) ; Z3
2. ASp(x) ; APP(x) ; Z3
3. ASp(x) ; APP(x) ; ASp(x) ; Z3
4. APP(x) ; Z3
5. APP(Universe) ; ASp(x) ; Z3
Experiment 0 consists in running Z3 directly on the 1655 clauses that encode the
136 problems. Z3 solved 28 problems, either positively or negatively, by providing
the answer ‘satisfiable’ or ‘unsatisfiable’, respectively, in an average time of 2.36
seconds per problem (see Frame 0 in Table 1).
    The other experiments with domain x have been performed as we now explain
for Experiments 1 and 2 with domain x = OS (see Frames 1 and 2, respectively,
in Table 1). By using VeriMAP we have run ASp(OS) on the initial 1655 clauses.
Then, on the resulting 3540 clauses (with an average time of 0.73 seconds per
problem), either (Experiment 1) we have run Z3 that solved 28 problems (with
an average time of 4.10 seconds per problem) or (Experiment 2) by using again
VeriMAP, we have run APP(OS) that produced 20361 clauses (with an average
time of 4.60 seconds per problem). Finally, acting on these 20361 clauses, Z3
solved 121 problems out of 136 (with an average time of 3.90 seconds per solved
problem). In Column SizeRatio we reported the increase in the number of clauses
due to the transformations performed by VeriMAP. In particular, ASp(OS) en-
                                                                                 11

larged the size of about 2.14 (= 3540/1655) times, and APP(OS) of about 5.83
times.
    During an experiment it may be the case that VeriMAP does not complete
the execution of the ASp(x) strategy, or the APP(x) strategy, within the given
timeout of 300 seconds. In that case the clauses of the problem for which the
timeout occurred, are not passed to the subsequent step of the experiment (and
they are not considered in the computation of the average times and the size
ratios).
    We have used the Z3 4.5.0 solver with the Duality fixed-point engine [33] on
an Intel Xeon CPU E5-2640 2.00GHz processor with 64GB of memory under the
GNU/Linux 64 bit operating system CentOS 7.

Results. The results of the experiments are summarized in Table 1. In order to
have a more detailed understanding of the results, for the Experiments 2, 3,
and 5, we have adopted an incremental presentation in the sense that, for in-
stance, Frame 2 presents the results for ‘APP(x) ; Z3’, and the results concerning
the first step ‘ASp(x)’ are to be read in the first five columns of Frame 1 where
the experiment ‘ASp(x) ; Z3’ is presented.
    First we observe that the use of the ASp and APP strategies significantly
increases the number of problems which Z3 can solve (see Frames 0 and 2 of
Table 1). Indeed, for Experiment 2 with domain OS the number of problems
solved by Z3 is 121, while Z3 alone solved 28 problems only.
    Our results show that the use of abstract domain Boxes is not very effective.
Indeed, in Frame 2 we see that 73 problems only are solved (with respect to 121
for OS). Similarly, in Frame 3, only 77 problems are solved (with respect to 121
for BDS). The poor performance of Boxes with respect to those of OS and BDS
can be explained by the fact that Boxes (that is, intervals of individual variables)
are not expressive enough to represent relations among variables of programs.
Hence, they are of little help for proving the given relational property. Note,
however, that if precision is further increased, from BDS and OS to Convex
Polyhedra, the performance does not increase. Indeed, the number of solved
problems decreases because the computations required for CP-H and CP-B are
more expensive and the timeout limit is reached more often.
    Looking at frames 1, 2, and 3 (Columns for Z3) we see that the main contri-
bution to the increase of efficacy in proving the desired properties is due to the
APP strategy (when used with a suitable domain, such as BDS, OS, CP-H, and
CP-B), rather then the ASp strategy. Indeed, the comparison of Frames 2 and 3
(Column SolvedProbls) shows that the use of ASp after APP does not make any
significant change in the efficacy. Note also that applying ASp before APP for
BDS and OS does not really pay off. Indeed, the comparison of Frame 2 with
Frame 4 shows that more problems can be solved with lower verification time
by directly applying the APP strategy starting from the clauses encoding the
verification problems.
    The comparison between Frames 4 and 5 (Columns for Z3) tells us that the
effect of the APP(x) strategy, for a given abstract domain x, can also be obtained
12

                          VeriMAP                              Z3
Domain x InProbls OutProbls OutCls AvgTime1 SizeRatio SolvedProbls AvgTime2
0.        Z3
              136      —      —         —        —             28       2.36
1.        ASp(x) ; Z3
 Boxes        136      136 3111         0.67     1.88          29       3.15
 BDS          136      136 2629         0.66     1.59          28       3.79
 OS           136      136 3540         0.73     2.14          28       4.10
 CP-H         136      136 3021         0.66     1.83          34       3.95
 CP-B         136      136 3633         0.69     2.20          36      10.14
2.        Assuming ASp(x) already performed:                APP(x) ; Z3
 Boxes        136      134 27753        1.85     9.37          73       2.20
 BDS          136      136 12793        2.60     4.87         119       3.69
 OS           136      134 20361        4.60     5.83         121       3.90
 CP-H         136      135 16193        3.09     5.39         113       0.93
 CP-B         136      127 12554        2.82     3.80         114       3.65
3.        Assuming ASp(x) ; APP(x) already performed: ASp(x) ; Z3
 Boxes        134      134 45970        2.57     1.66          77       3.54
 BDS          136      136 26683        3.30     2.09         121       3.86
 OS           134      134 36871        4.89     1.81         119       3.06
 CP-H         135      135 31521        3.91     1.95         115       2.05
 CP-B         127      127 25495        4.59     2.03         112       1.27
4.        APP(x) ; Z3
 Universe     136      136 4097         0.71     2.48          73       2.00
 Boxes        136      136 20296        2.27    12.26          78       2.01
 BDS          136      136 8630         1.38     5.21         121       2.45
 OS           136      135 13762        2.97     8.37         120       1.77
 CP-H         136      135 13823        2.59     8.40         110       1.57
 CP-B         136      131 11718        2.22     7.35         113       2.19
5.        Assuming APP(Universe) already performed:         ASp(x) ; Z3
 Boxes        136      136 19932        2.23     4.87          74       3.07
 BDS          136      136 8387         1.46     2.05         120       1.63
 OS           136      135 14065        2.93     3.46         118       1.39
 CP-H         136      135 14111        2.57     3.47         112       1.44
 CP-B         136      129 9831         2.41     2.53         113       2.05
Table 1. Frame 0 reports the results obtained by using Z3 on the input clauses.
Frames 1–5 report the results obtained by transforming the clauses using VeriMAP
and then checking their satisfiability using Z3. Column ‘Domain x’ reports the cho-
sen abstract domain. Column ‘InProbls’ (‘OutProbls’) reports the number of problems
given as input to (produced as output by) VeriMAP. Columns ‘OutCls’ and ‘AvgTime1’
report the number of output clauses and the average time taken by VeriMAP. Col-
umn ‘SizeRatio’ reports the value OutCls/InCls, where InCls is the number of clauses
of the problems for which VeriMAP terminates within the timeout. Columns ‘Solved-
Probls’ and ‘AvgTime2’ report the number of solved problems and the average time
taken by Z3. The times are the CPU seconds spent in user mode. A timeout of 300
seconds has been set for each run of VeriMAP and Z3.
                                                                               13

in two steps: (i) performing ‘simple’ Predicate Pairing, that is, APP(Universe),
and (ii) applying ASp(x) which realizes the abstraction on the domain x.
    The large values in Column OutCls show that in our implementation more
effort should be put in keeping the number of clauses generated by the APP and
ASp strategies small, and indeed ongoing work is devoted to the design of new
transformation techniques that have that effect.


6   Related Work and Conclusions

We have proposed various ways of combining transformation and abstraction
techniques for constrained Horn clauses with the goal of verifying relational
properties of imperative programs. To this aim we have presented Predicate
Pairing and Specialization algorithms that are parameterized with respect to a
given abstract constraint domain and its operators. Then we have presented an
extensive experimental evaluation of CHC satisfiability problems encoding rela-
tional verification problems. Our experiments show that suitable combinations of
transformations and abstraction dramatically increase the effectiveness of the Z3
solver on the given benchmark. The most effective techniques combine Predicate
Pairing and Abstraction based on Bounded Differences or Octagons [2, 35], that
is, constraint domains that are quite simple, but expressive enough to capture
the relations between predicate arguments.
    Relational verification has been extensively studied, and still receives much
attention as a relevant problem in the field of software engineering [4, 6, 7, 16,
20, 21, 23, 30, 32, 39, 40, 41]. In particular, during the software development
process it may be helpful to prove that the semantics of a new program version
has some specified relation with the semantics of an old version.
    Among the various methods to prove relational properties, those by Mordvi-
nov and Fedyunkovich [36] and by Felsing et al. [21] are the most closely related
to ours. The method proposed in the former paper [36] introduces the notion of
CHC product (somewhat related to our Predicate Pairing strategy), that is, a
CHC transformation that synchronizes computations to improve the effective-
ness of the CHCs satisfiability check. The latter method proposed by Felsing
et al. [21] presents proof rules for relations between imperative programs that
are translated into constrained Horn clauses. The satisfiability of these clauses
which entails the relation of interest, is then checked by state-of-the-art CHC
solvers.
    In the literature there are also partially automated approaches that reduce
the problem of verifying relational properties (in particular, program equiva-
lence) to a standard verification problem by using some composition operator
between imperative programs [4, 30, 39, 41].
    The reuse of existing verification techniques for proving relational program
properties can also be realized by first computing summaries of the two pro-
grams, that is, relations between the input and output values of the programs,
and then proving relational properties of these summaries. This approach is fol-
lowed by: (i) Ganty et al. [22], whose method also supports a restricted class
14

of recursive programs, (ii) Hawblitzel et al. [26], who use automated theorem
provers for proving relative termination, and (iii) Lopes and Monteiro [32], who
use (possibly nonlinear) integer polynomials and recurrences for summarizing
loops of programs acting on integers.
    A method that, like ours, is parametric with respect to the semantics of
the programming languages in which the programs to be verified are written, is
proposed by S. Ciobâcă et al. [7], who present a language-independent deductive
system for proving mutual equivalence of programs.
    The Predicate Pairing technique we present in this paper is a descendant
of well-known techniques for logic program transformation, such as Tupling [38]
and Conjunctive Partial Deduction [18], which derive new predicates defined in
terms of conjunctions of atoms. The goal of these techniques is the derivation
of efficient logic programs by: (i) avoiding multiple traversals of data structures
and repeated evaluations of predicate calls, and (ii) producing specialized pro-
gram versions that take into account partial information on the input values. An
integration of Conjunctive Partial Deduction and abstract interpretation, called
Abstract Conjunctive Partial Deduction, has also been presented in the liter-
ature [31]. Recent work has shown that the extension of these transformation
techniques to constrained Horn clauses can play a significant role in improving
the effectiveness of CHC solvers for proving properties of imperative programs,
and in particular for verifying relational properties [14, 16].
    The CHC Specialization strategy we consider in this paper is a variant of
specialization techniques for (constraint) logic programs which have been pro-
posed to support program verification [1, 11, 13, 15, 24, 28, 29, 34, 37]. However,
these techniques are focused on the verification of partial or total correctness of
single programs, and not on the relational verification.


References

 1. E. Albert, M. Gómez-Zamalloa, L. Hubert, and G. Puebla. Verification of Java
    bytecode using analysis and transformation of logic programs. In Proc. PADL ’07,
    LNCS 4354, pages 124–139. Springer, 2007.
 2. R. Bagnara, P. M. Hill, E. Ricci, and E. Zaffanella. Precise widening operators for
    convex polyhedra. Science of Computer Programming, 58(1):28 – 56, 2005.
 3. R. Bagnara, P. M. Hill, and E. Zaffanella. The Parma Polyhedra Library: Toward a
    complete set of numerical abstractions for the analysis and verification of hardware
    and software systems. Science of Computer Programming, 72(1–2):3–21, 2008.
 4. G. Barthe, J. M. Crespo, and C. Kunz. Relational verification using product
    programs. In Proc. FM ’11, LNCS 6664, pages 200–214. Springer, 2011.
 5. N. Benton. Simple relational correctness proofs for static analyses and program
    transformations. In Proc. POPL ’04, pages 14–25. ACM, 2004.
 6. S. Chaki, A. Gurfinkel, and O. Strichman. Regression verification for multi-
    threaded programs. Proc. VMCAI ’12, LNCS 7148, pages 119–135. Springer, 2012.
 7. S. Ciobâcă, D. Lucanu, V. Rusu, and G. Rosu. A language-independent proof
    system for mutual program equivalence. In Proc. ICFEM ’14, LNCS 8829, pages
    75–90. Springer, 2014.
                                                                                      15

 8. P. Cousot and R. Cousot. Abstract interpretation: A unified lattice model for
    static analysis of programs by construction of approximation of fixpoints. In Proc.
    POPL ’77, pages 238–252. ACM, 1977.
 9. P. Cousot, R. Ganty, and J.-F. Raskin. Fixpoint-guided abstraction refinements.
    In Proc. SAS ’07, LNCS 4634, pages 333–348. Springer, 2007.
10. P. Cousot and N. Halbwachs. Automatic discovery of linear restraints among
    variables of a program. In Proc. POPL ’78, pages 84–96. ACM, 1978.
11. E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti. Program verification
    via iterated specialization. Sci. Comput. Program., 95, Part 2:149–175, 2014.
12. E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti. VeriMAP: A tool for
    verifying programs through transformations. Proc. TACAS ’14, LNCS 8413, pages
    568–574. Springer, 2014. Available at: http://www.map.uniroma2.it/VeriMAP.
13. E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti. Proving correctness of
    imperative programs by linearizing constrained Horn clauses. Theory and Practice
    of Logic Programming, 15(4-5):635–650, 2015.
14. E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti. A rule-based ver-
    ification strategy for array manipulating programs. Fundamenta Informaticae,
    140(3-4):329–355, 2015.
15. E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti. Semantics-based
    generation of verification conditions by program specialization. In: Selected and
    Extended papers from the International Symposium on Principles and Practice of
    Declarative Programming 2015, Sci. Comput. Program., 147 (78–108), 2017.
16. E. De Angelis, F. Fioravanti, A. Pettorossi, and M. Proietti. Relational verification
    through Horn clause transformation. In Proc. SAS ’16, LNCS 9837, pages 147–169.
    Springer, 2016.
17. L. M. de Moura and N. Bjørner. Z3: An efficient SMT solver. In Proc. TACAS ’08,
    LNCS 4963, pages 337–340. Springer, 2008.
18. D. De Schreye, R. Glück, J. Jørgensen, M. Leuschel, B. Martens, and M. H.
    Sørensen. Conjunctive partial deduction: Foundations, control, algorithms, and
    experiments. Journal of Logic Programming, 41(2–3):231–277, 1999.
19. S. Etalle and M. Gabbrielli. Transformations of CLP modules. Theoretical Com-
    puter Science, 166:101–146, 1996.
20. G. Fedyukovich, A. Gurfinkel, and N. Sharygina. Property directed equivalence
    via abstract simulation. CAV ’16, LNCS 9780, pages 433–453. Springer, 2016.
21. D. Felsing, S. Grebing, V. Klebanov, P. Rümmer, and M. Ulbrich. Automating
    regression verification. Proc. ASE ’14, pages 349–360. ACM, 2014.
22. P. Ganty, R. Iosif, and F. Konečný. Underapproximation of procedure summaries
    for integer programs. TACAS ’13, LNCS 7795, pages 245–259. Springer, 2013.
23. B. Godlin and O. Strichman. Inference rules for proving the equivalence of recursive
    procedures. Acta Informatica, 45(6):403–439, 2008.
24. M. Gómez-Zamalloa, E. Albert, and G. Puebla. Decompilation of Java bytecode
    to Prolog by partial evaluation. Inf. Softw. Technol., 51(10):1409–1427, 2009.
25. N. Halbwachs, Y. E. Proy, and P. Roumanoff. Verification of real-time systems
    using linear relation analysis. Formal Methods in Sys. Design, 11:157–185, 1997.
26. C. Hawblitzel, M. Kawaguchi, S. K. Lahiri, and H. Rebêlo. Towards modu-
    larly comparing programs using automated theorem provers. In Proc. CADE ’13,
    LNCS 7898, pages 282–299. Springer, 2013.
27. H. Hojjat, F. Konecný, F. Garnier, R. Iosif, V. Kuncak, and P. Rümmer. A ver-
    ification toolkit for numerical transition systems. In Proc. FM ’12, LNCS 7436,
    pages 247–251. Springer, 2012.
16

28. B. Kafle and J. P. Gallagher. Constraint specialisation in Horn clause verification.
    Science of Computer Programming, 137:125–140, 2017.
29. B. Kafle and J. P. Gallagher. Horn clause verification with convex polyhedral
    abstraction and tree automata-based refinement. Computer Languages, Systems
    & Structures, 47:2–18, 2017.
30. S. K. Lahiri, K. L. McMillan, R. Sharma, and C. Hawblitzel. Differential assertion
    checking. In Proc. ESEC/FSE ’13, pages 345–355. ACM, 2013.
31. M. Leuschel. A framework for the integration of partial evaluation and abstract
    interpretation of logic programs. ACM TOPLAS, 26(3):413–463, 2004.
32. N. P. Lopes and J. Monteiro. Automatic equivalence checking of programs with
    uninterpreted functions and integer arithmetic. Software Tools for Technology
    Transfer, 18(4):359–374, 2016.
33. K. L. McMillan and A. Rybalchenko. Solving constrained Horn clauses using
    interpolation. MSR Technical Report 2013-6, Microsoft Report, 2013.
34. M. Méndez-Lojo, J. A. Navas, and M. V. Hermenegildo. A flexible, (C)LP-based
    approach to the analysis of object-oriented programs. In Proc. LOPSTR ’07, LNCS
    4915, pages 154–168. Springer, 2008.
35. A. Miné. The octagon abstract domain. Higher-Order and Symbolic Computation,
    19(1):31–100, 2006.
36. D. Mordvinov and G. Fedyukovich. Synchronizing constrained Horn clauses. In
    Proc. LPAR ’17, EPiC Series in Computing 46, pages 338–355. EasyChair, 2017.
37. J. C. Peralta, J. P. Gallagher, and H. Saglam. Analysis of imperative programs
    through analysis of constraint logic programs. In Proc. SAS ’98, LNCS 1503, pages
    246–261. Springer, 1998.
38. A. Pettorossi and M. Proietti. Transformation of logic programs: Foundations and
    techniques. Journal of Logic Programming, 19,20:261–320, 1994.
39. O. Strichman and M. Veitsman. Regression verification for unbalanced recursive
    functions. In Proc. FM ’16, LNCS 9995, pages 645–658. Springer, 2016.
40. S. Verdoolaege, G. Janssens, and M. Bruynooghe. Equivalence checking of static
    affine programs using widening to handle recurrences. ACM TOPLAS, 34(3):11,
    2012.
41. A. Zaks and A. Pnueli. CoVaC: Compiler validation by program analysis of the
    cross-product. In Proc. FM ’08, LNCS 5014, pages 35–51. Springer, 2008.
