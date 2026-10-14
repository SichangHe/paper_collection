                                                                                                                                                                A
                                         Incomplete SMT Techniques for Solving Non-Linear Formulas
                                         over the Integers
                                         CRISTINA BORRALLERAS, Universitat de Vic - Universitat Central de Catalunya
                                         DANIEL LARRAZ, ALBERT OLIVERAS,
                                         ENRIC RODRÍGUEZ-CARBONELL and ALBERT RUBIO, Universitat Politècnica de Catalunya


                                         We present new methods for solving the Satisfiability Modulo Theories problem over the theory of
arXiv:2008.13601v1 [cs.LO] 31 Aug 2020




                                         Quantifier-Free Non-linear Integer Arithmetic, SMT(QF-NIA), which consists in deciding the satisfiabil-
                                         ity of ground formulas with integer polynomial constraints. Following previous work, we propose to solve
                                         SMT(QF-NIA) instances by reducing them to linear arithmetic: non-linear monomials are linearized by ab-
                                         stracting them with fresh variables and by performing case splitting on integer variables with finite domain.
                                         For variables that do not have a finite domain, we can artificially introduce one by imposing a lower and an
                                         upper bound, and iteratively enlarge it until a solution is found (or the procedure times out).
                                             The key for the success of the approach is to determine, at each iteration, which domains have to be
                                         enlarged. Previously, unsatisfiable cores were used to identify the domains to be changed, but no clue was
                                         obtained as to how large the new domains should be. Here we explain two novel ways to guide this process
                                         by analyzing solutions to optimization problems: (i) to minimize the number of violated artificial domain
                                         bounds, solved via a Max-SMT solver, and (ii) to minimize the distance with respect to the artificial domains,
                                         solved via an Optimization Modulo Theories (OMT) solver. Using this SMT-based optimization technology
                                         allows smoothly extending the method to also solve Max-SMT problems over non-linear integer arithmetic.
                                         Finally we leverage the resulting Max-SMT(QF-NIA) techniques to solve ∃∀ formulas in a fragment of quan-
                                         tified non-linear arithmetic that appears commonly in verification and synthesis applications.
                                         CCS Concepts: •Mathematics of computing → Solvers; •Theory of computation → Logic and ver-
                                         ification; Automated reasoning; •Computing methodologies → Equation and inequality solving al-
                                         gorithms; Theorem proving algorithms;
                                         Additional Key Words and Phrases: Non-linear arithmetic, satisfiability modulo theories
                                         ACM Reference Format:
                                         Cristina Borralleras, Daniel Larraz, Albert Oliveras, Enric Rodrı́guez-Carbonell, and Albert Rubio, 2016.
                                         Incomplete SMT techniques for solving non-linear formulas over the integers. ACM Trans. Comput. Logic V,
                                         N, Article A (January YYYY), 35 pages.
                                         DOI: http://dx.doi.org/10.1145/0000000.0000000

                                         1. INTRODUCTION
                                         Polynomial constraints are pervasive in computer science. They appear natu-
                                         rally in countless areas, ranging from the analysis, verification and synthesis of
                                         software and hybrid systems [Colón et al. 2003; Sankaranarayanan et al. 2004;
                                         Sankaranarayanan et al. 2008;    Platzer et al. 2009] to,    e.g.,  game   theory

                                         All authors partially supported by Spanish Ministerio de Economı́a y Competitividad under grants TIN2013-
                                         45732-C4-3-P (MINECO) and TIN2015-69175-C4-3-R (MINECO/FEDER). Albert Oliveras is partially
                                         funded by the European Research Council (ERC) under the European Union’s Horizon 2020 research and
                                         innovation programme (grant agreement ERC-2014-CoG 648276 AUTAR).
                                         Author’s addresses: C. Borralleras, Departament Tecnologies Digitals i de la Informació, Escola Politècnica
                                         Superior, Universitat de Vic - Universitat Central de Catalunya; Daniel Larraz, Albert Oliveras, En-
                                         ric Rodrı́guez-Carbonell and Albert Rubio, Departament of Computer Science, Universitat Politècnica de
                                         Catalunya.
                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted
                                         without fee provided that copies are not made or distributed for profit or commercial advantage and that
                                         copies bear this notice and the full citation on the first page. Copyrights for components of this work owned
                                         by others than ACM must be honored. Abstracting with credit is permitted. To copy otherwise, or repub-
                                         lish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request
                                         permissions from permissions@acm.org.
                                         © YYYY ACM. 1529-3785/YYYY/01-ARTA $15.00
                                         DOI: http://dx.doi.org/10.1145/0000000.0000000


                                                           ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:2                                                                                Cristina Borralleras et al.

[Beyene et al. 2014]. In all these cases, it is crucial to have efficient automatic
solvers that, given a formula involving polynomial constraints with integer or real
variables, either return a solution to the formula or report that there is none.
   Therefore, it is of no surprise that solving this sort of non-linear formulas has at-
tracted wide attention over the years. A milestone result of Tarski’s [Tarski 1951] is a
constructive proof that the problem is decidable for the first-order theory of real closed
fields, in particular for the real numbers. Unfortunately the algorithm in the proof
has non-elementary complexity, i.e., its cost cannot be bounded by any finite tower of
exponentials, and is thus essentially useless from a practical point of view. For this
reason, for solving polynomial constraints in R, computer algebra has traditionally
relied on the more workable approach of cylindrical algebraic decomposition (CAD)
[Collins 1975; Basu et al. 2003]. Still, its applicability is hampered by its doubly expo-
nential complexity.
   Due to the limitations of the existing techniques, further research has been car-
ried out in polynomial constraint solving, spurred in the last decade by the irrup-
tion of SAT and its extensions [Biere et al. 2009; Nieuwenhuis et al. 2006]. Thus,
several techniques have emerged in this period which leverage the efficiency and
automaticity of this new technology. E.g., for solving polynomial constraints in
R, interval constraint propagation has been integrated with SAT and SMT en-
gines [Fränzle et al. 2007; Gao et al. 2010; Khanh and Ogawa 2012]. Other works pre-
process non-linear formulas before passing them to an off-the-shelf SMT solver for
quantifier-free linear real arithmetic [Ganai and Ivancic 2009], or focus on partic-
ular kinds of constraints like convex constraints [Nuzzo et al. 2010]. In the imple-
mentation of many of these approaches computations are performed with floating-
point arithmetic. In order to address the ever-present concern that numerical er-
rors can result in incorrect answers, the framework of δ-complete decision proce-
dures has been proposed [Gao et al. 2012; Gao et al. 2013]. In another line of re-
search, as opposed to numerically-driven approaches, symbolic techniques from al-
gebraic geometry such as the aforementioned CAD [Jovanovic and de Moura 2012],
Gröbner bases [Junges et al. 2013; Passmore et al. 2010], Handelman’s representa-
tions [Maréchal et al. 2016] or virtual substitution [Corzilius and Ábrahám 2011] have
been successfully adapted to SAT and SMT. As a result, several libraries and toolboxes
have been made publicly available for the development of symbolically-driven solvers
[Corzilius et al. 2012; de Moura and Passmore 2013; Corzilius et al. 2015].
   On the other hand, when variables have to take integer values, even the prob-
lem of solving a single polynomial equation is undecidable (Hilbert’s 10th prob-
lem, [Cooper 2004]). Despite this theoretical limitation, and following a similar di-
rection to the real case, several incomplete methods that exploit the progress in
SAT and SMT have been proposed for dealing with integer polynomial constraints.
The common idea of these approaches is to reduce instances of this kind of for-
mulas into problems of a simpler language that can be straightforwardly han-
dled by existing SAT/SMT systems, e.g., propositional logic [Fuhs et al. 2007], lin-
ear bit-vector arithmetic [Zankl and Middeldorp 2010] or linear integer arithmetic
[Borralleras et al. 2012]. All these techniques are oriented towards satisfiability, which
makes them convenient in applications where finding solutions is more relevant
than proving that none exists (e.g., in verification when generating ranking func-
tions [Larraz et al. 2013], invariants [Larraz et al. 2013] or other inductive properties
[Larraz et al. 2014; Brockschmidt et al. 2015]).




               ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                          A:3

   In this article1 we build upon our previous method [Borralleras et al. 2012] for decid-
ing SMT(QF-NIA) by reduction to SMT(QF-LIA). In that work, non-linear monomials
are linearized by abstracting them with fresh variables and by performing case split-
ting on integer variables with finite domain. In the case in which variables do not
have finite domains, artificial ones are introduced by imposing a lower and an upper
bound. While the underlying SMT(QF-LIA) solver cannot find a solution (and the time
limit has not been exceeded yet), domain relaxation is applied: some domains are made
larger by weakening the bounds. To guide which bounds have to be relaxed from one
iteration to the following one, unsatisfiable cores are employed: at least one of the ar-
tificial bounds that appear in the unsatisfiable core should be weaker. Unfortunately,
although unsatisfiable cores indicate which bounds should be relaxed, they provide
no hint on how large the new domains have to be made. This is of paramount impor-
tance, since the size of the new linearized formula (and therefore the time needed to
determine its satisfiability) can increase significantly depending on the number of new
cases that must be added.
   A way to circumvent this difficulty could be to find alternative techniques to the
unsatisfiable cores which, when a solution with the current domains cannot be found,
provide more complete information for the domain relaxation. In this paper we pro-
pose such alternative techniques. The key idea is that an assignment of numeri-
cal values to variables that is “closest” to being a true solution (according to some
metric) can be used as a reference as regards to how one should enlarge the do-
mains. Thus, the models generated by the SMT(QF-LIA) engine are put in use in
the search of solutions of the original non-linear problem, with a similar spirit to
[de Moura and Bjørner 2008a] for combining theories or to the model-constructing sat-
isfiability calculus of [de Moura and Jovanovic 2013].
   However, as pointed out above, in our case we are particularly interested
in minimal models, namely those that minimize a cost function that measures
how far assignments are from being a true solution to the non-linear prob-
lem. Minimal models have long been studied in the case of propositional logic
[Ben-Eliyahu and Dechter 1996; Ben-Eliyahu-Zohary 2005; Soh and Inoue 2010]. In
SMT, significant advancements have been achieved towards solving the op-
timization problems of Maximum Satisfiability Modulo Theories (Max-SMT,
[Nieuwenhuis and Oliveras 2006; Cimatti et al. 2010]) and Optimization Modulo
Theories (OMT, [Oliver 2012; Sebastiani and Tomasi 2015]). Thanks to this re-
search, several SMT systems are currently offering optimization functionalities
([Sebastiani and Trentin 2015; Li et al. 2014; Bjørner et al. 2015]). Taking advantage
of these recent developments, in this paper we make the following contributions:
  (1) In the context of solving SMT(QF-NIA), we present different heuristics for guid-
ing the domain relaxation step by means of the analysis of minimal models. More
specifically, we consider two different cost functions:
— the number of violated artificial domain bounds (leading to Max-SMT problems);
— the distance with respect to the artificial domains (leading to OMT problems).
We evaluate these model-guided heuristics experimentally with an exhaustive bench-
mark set and compare them with other techniques for solving SMT(QF-NIA). The re-
sults of this evaluation show the potential of the method.
  (2) Based on the results of the aforementioned experiments, we extend our best
approach for SMT(QF-NIA) to handle problems in Max-SMT(QF-NIA).
  (3) Finally we apply our Max-SMT(QF-NIA) techniques to solve SMT and Max-SMT
problems in the following fragment of quantified non-linear arithmetic: ∃∀ formulas

1 This is the extended version of the conference paper presented at SAT ’14 [Larraz et al. 2014].




ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:4                                                                                 Cristina Borralleras et al.

where ∃ variables are of integer type and ∀ variables are of real type, and non-linear
monomials cannot contain the product of two real variables. Formulas of this kind ap-
pear commonly in verification and synthesis applications [Dutertre 2015], for example
in control and priority synthesis [Cheng et al. 2013], reverse engineering of hardware
[Gascón et al. 2014] and program synthesis [Tiwari et al. 2015].
   This paper is structured as follows. Section 2 reviews basic background on SMT,
Max-SMT and OMT, and also on our previous approach in [Borralleras et al. 2012]. In
Section 3 two different heuristics for guiding the domain relaxation step are presented,
together with experiments and several possible variants. Then Section 4 proposes an
extension of our techniques from SMT(QF-NIA) to Max-SMT(QF-NIA). In turn, in Sec-
tion 5 our Max-SMT(QF-NIA) approach is applied to solving Max-SMT problems with
∃∀ formulas. Finally, Section 6 summarizes the conclusions of this work and sketches
lines for future research.

2. PRELIMINARIES
2.1. SMT, Max-SMT and OMT
Let P be a fixed finite set of propositional variables. If p ∈ P, then p and ¬p are literals.
The negation of a literal l, written ¬l, denotes ¬p if l is p, and p if l is ¬p. A clause
is a disjunction of literals l1 ∨ · · · ∨ ln . A (CNF) propositional formula is a conjunction
of clauses C1 ∧ · · · ∧ Cn . The problem of propositional satisfiability (abbreviated SAT)
consists in, given a propositional formula, to determine whether it is satisfiable, i.e., if
it has a model: an assignment of Boolean values to variables that satisfies the formula.
   The satisfiability modulo theories (SMT) problem is a generalization of SAT. In SMT,
one has to decide the satisfiability of a given (usually, quantifier-free) first-order for-
mula with respect to a background theory. In this setting, a model (which we may also
refer to as a solution) is an assignment of values from the theory to variables that
satisfies the formula. Examples of theories are quantifier-free linear integer arithmetic
(QF-LIA), where literals are linear inequalities over integer variables, and the more
general quantifier-free non-linear integer arithmetic (QF-NIA), where literals are poly-
nomial inequalities over integer variables. Unless otherwise stated, in this paper we
will assume that variables are all of integer type.
   Another generalization of SAT is Max-SAT [Li and Manyà 2009], which extends the
problem by asking for more information when the formula turns out to be unsatisfi-
able: namely, the Max-SAT problem consists in, given a formula F , to find an assign-
ment such that the number of satisfied clauses in F is maximized, or equivalently, that
the number of falsified clauses is minimized. This problem can in turn be generalized
in a number of ways. For example, in weighted Max-SAT each clause of F has a weight
(a positive natural or real number), and then the goal is to find the assignment such
that the cost, i.e., the sum of the weights of the falsified clauses, is minimized. Yet a fur-
ther extension of Max-SAT is the partial weighted Max-SAT problem, where clauses
in F are either weighted clauses as explained above, called soft clauses in this setting,
or clauses without weights, called hard clauses. In this case, the problem consists in
finding the model of the hard clauses such that the sum of the weights of the falsified
soft clauses is minimized. Equivalently, hard clauses can also be seen as soft clauses
with infinite weight.
   The problem of Max-SMT merges Max-SAT and SMT, and is defined from SMT
analogously to how Max-SAT is derived from SAT. Namely, the Max-SMT problem
consists in, given a set of pairs {[C1 , ω1 ], . . . , [Cm , ωm ]}, where each Ci is a clause and
ωi is its weight (a positive number or infinity), to find an assignment that minimizes
the sum of the weights of the falsified clauses in the background theory. As in SMT, in
this context we are interested in assignments of values from the theory to variables.

                ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                          A:5

   Finally, the problem of Optimization Modulo Theories (OMT) is similar to Max-SMT
in that they are both optimization problems, rather than decision problems. It consists
in, given a formula F involving a particular numerical variable called cost , to find the
model of F such that the value assigned to cost is minimized. Note that this framework
allows one to express a wide variety of optimization problems (maximization, piecewise
linear functions, etc.).

2.2. Solving SMT(QF-NIA) with Unsatisfiable Cores
In [Borralleras et al. 2012], we proposed a method for solving SMT(QF-NIA) problems
based on encoding them into SMT(QF-LIA). The basic idea is to linearize each non-
linear monomial in the formula by applying a case analysis on the possible values of
some of its variables. For example, if the monomial x2 yz appears in the input QF-NIA
formula and x must satisfy 0 ≤ x ≤ 2, we can introduce a fresh variable vx2 yz , replace
the occurrences of x2 yz by vx2 yz and add to the clause set the following three case
splitting clauses:
                                           x = 0 → vx2 yz = 0 ,
                                           x = 1 → vx2 yz = yz ,
                                           x = 2 → vx2 yz = 4yz .

   In turn, new non-linear monomials may appear, e.g., yz in this example. All non-
linear monomials are handled in the same way until a formula in QF-LIA is ob-
tained, for which efficient decision procedures exist [Dutertre and de Moura 2006;
Dillig et al. 2011; Griggio 2012].
   Note that, in order to linearize a non-linear monomial, there must be at least one
variable in it which is both lower and upper bounded. When this property does not
hold, new artificial domains can be introduced for the variables that require them (for
example, for unbounded variables one may take {−1, 0, 1}). In principle, this implies
that the procedure is no longer complete, since a linearized formula with artificial
bounds may be unsatisfiable while the original QF-NIA formula is actually satisfiable.
A way to overcome this problem is to proceed iteratively: variables start with bounds
that make the size of their domains small, and then the domains are enlarged on de-
mand if necessary, i.e., if the formula turns out to be unsatisfiable. The decision of
which bounds are to be relaxed is heuristically taken based on the analysis of an un-
satisfiable core (an unsatisfiable subset of the clause set) that is obtained when the
solver reports unsatisfiability. There exist many techniques in the literature for com-
puting unsatisfiable cores (see, e.g., [Ası́n Achá et al. 2010] for a sample of them). In
[Borralleras et al. 2012] we employed the well-known simple and effective approach of
[Zhang and Malik 2003], consisting in writing a trace on disk and extracting a reso-
lution refutation, whose leaves form an unsatisfiable core. Note that the method tells
which bounds should be weakened, but does not provide any guidance in regard to how
large the change on the bounds should be. This is critical, as the size of the formula
in the next iteration (and so the time required to determine its satisfiability) can grow
significantly depending on the number of new case splitting clauses that have to be
added. Therefore, in lack of a better strategy, a typical heuristic is to decrement or in-
crement the bound (for lower bounds and for upper bounds, respectively) by a constant
value.
   Procedure solve SMT QF NIA cores in Algorithm 1 describes more formally the
overall algorithm from [Borralleras et al. 2012] for solving SMT(QF-NIA). First, the
required artificial bounds are computed (procedure artificial bounds, with pseudo-code
in Algorithm 2). Then the linearized formula (procedure linearize, with pseudo-code in
Algorithm 3) together with the artificial bounds are passed to an SMT(QF-LIA) solver

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:6                                                                                    Cristina Borralleras et al.


ALGORITHM 1: Algorithm for solving SMT(QF-NIA) with unsatisfiable cores

status solve SMT QF NIA cores(formula F0 ) { // returns whether F0 is satisfiable
  B = artificial bounds(F0 );                // B are artificial bounds enough to linearize F0
  F = linearize(F0 , B );
  while (not timed out()) {
    hST , UC i = solve SMT QF LIA(F , B);   // unsatisfiable core UC computed here for simplicity
    if (ST == SAT) return SAT;              // is F ∧ B satisfiable?
    else if (B ∩ UC == ∅) return UNSAT;
    else {
      B ′ = new domains cores(B, UC );      // at least one in the intersection is relaxed
      F = update(F , B, B ′ );               // add case splitting clauses
      B =B ; ′
    }
  }
  return UNKNOWN;
}



ALGORITHM 2: Procedure artificial bounds

set artificial bounds(formula F0 ) {        // returns the artificial bounds for linearization
  S = choose linearization variables(F0 ); // choose enough variables to linearize F0
  B = ∅;                                   // set of artificial bounds
  for (V in S) {
    if (lower bound(V , F0 ) == ⊥)          // cannot find lower bound of V in F0
       B = B ∪ { V ≥ L};                   // for a parameter L, e.g. L = −1
    if (upper bound(V , F0 ) == ⊥)          // cannot find upper bound of V in F0
       B = B ∪ { V ≤ U };                   // for a parameter U , e.g. U = 1
  }
  return B;
}



ALGORITHM 3: Procedure linearize
formula linearize(formula F0 , set B ) {         // returns the linearization of F0
  N = nonlinear monomials(F0 );
  F = F0 ;
  while (N 6= ∅) {
    let Q in N ;                                 // non-linear monomial to be linearized next
    VQ = fresh variable();
    F = replace(Q, F , VQ );                     // replace all occurrences of Q in F by VQ
    C = ∅;                                        // clauses of the case splitting
    V = linearization variable(Q);               // choose a finite domain variable in Q to linearize
    for (K in [lower bound(V , F0 ∪ B ), upper bound(V , F0 ∪ B )])
      C = C ∪ { V = K → VQ = evaluate(Q, V , K)};
    F = F ∪ C;
    N = N − {Q} ∪ nonlinear monomials(C);         // new non-linear monomials may be introduced
  }
  return F ;
}


(procedure solve SMT QF LIA), which tests if their conjunction is satisfiable 2 . If the
solver returns SAT, we are done. If the solver returns UNSAT, then an unsatisfiable

2 Note that, in this formulation, the linearization consists of the clauses of the original formula after replac-
ing non-linear monomials by fresh variables, together with the case splitting clauses. On the other hand, it
does not include the artificial bounds, which for the sake of presentation are kept as independent objects.


                   ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                                A:7


ALGORITHM 4: Procedure new domains cores
set new domains cores(set B , set UC ) {                    // returns the new set of artificial bounds
  let S ⊆ B ∩ UC such that S 6= ∅;
  B ′ = B;
  for (V ≥ L in S) B ′ = B ′ − {V ≥ L} ∪ {V ≥ L′ };          // e.g. L′ = L − KL for a parameter KL > 0
  for (V ≤ U in S) B ′ = B ′ − {V ≤ U } ∪ {V ≤ U ′ };        // e.g. U ′ = U + KU for a parameter KU > 0
  return B ′ ;
}


ALGORITHM 5: Procedure update

formula update(formula F , set B , set B ′ ) { // adds cases when relaxing the bounds from B to B ′
  F′ = F;
  for (V such that V ≥ L in B and V ≥ L′ in B ′ and L 6= L′ )
    for (K in [L′ , L − 1])
       for (Q such that V == linearization variable(Q))       // V was used to linearize monomial Q
          F ′ = F ′ ∪ { V = K → VQ = evaluate(Q, V , K)}; // VQ is the variable standing for Q

    for (V such that V ≤ U in B and V ≤ U ′ in B ′ and U 6= U ′ )
      for (K in [U + 1, U ′ ])
         for (Q such that V == linearization variable(Q))
            F ′ = F ′ ∪ { V = K → VQ = evaluate(Q, V , K)};

    return F ′ ;
}


core is also computed. If this core does not contain any of the artificial bounds, then
the original non-linear formula must be unsatisfiable, and we are done too. Otherwise,
at least one of the artificial bounds appearing in the core must be chosen for relaxation
(procedure new domains cores, with pseudo-code in Algorithm 4). Once the domains
are enlarged and the appropriate case splitting clauses are added (procedure update,
with pseudo-code in Algorithm 5), the new linearized formula is tested for satisfiability
again, and the process is repeated (typically, while a predetermined time limit is not
exceeded). We refer the reader to [Borralleras et al. 2012] for further details.
     Example 2.1. Let F0 be the formula
                                 tx + y ≥ 4 ∧ t2 + x2 + w2 + y 2 ≤ 12,
where variables t, x, w, y are integer. Let us also assume that we introduce the follow-
ing artificial bounds so as to linearize: B ≡ −1 ≤ t, x, w, y ≤ 1. Now a linearization F of
F0 could be for example:
                     vtx + y ≥ 4 ∧ vt2 + vx2 + vw2 + vy2 ≤ 12 ∧
                      (t = −1 → vtx = −x)               ∧
                      (t = 0 → vtx = 0)                 ∧
                      (t = 1 → vtx = x)                 ∧

                      (t = −1 → vt2 = 1)                ∧     (w = −1 → vw2 = 1)             ∧
                      (t = 0 → vt2 = 0)                 ∧     (w = 0 → vw2 = 0)              ∧
                      (t = 1 → vt2 = 1)                 ∧     (w = 1 → vw2 = 1)              ∧

                      (x = −1 → vx2 = 1)                ∧     (y = −1 → vy2 = 1)             ∧
                      (x = 0 → vx2 = 0)                 ∧     (y = 0 → vy2 = 0)              ∧
                      (x = 1 → vx2 = 1)                 ∧     (y = 1 → vy2 = 1)              ∧

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:8                                                                                 Cristina Borralleras et al.

where vtx , vt2 , vx2 , vw2 , vy2 are fresh integer variables standing for the non-linear mono-
mials in the respective subscripts.
 In this case the formula F ∧ B turns out to be unsatisfiable. For instance, the
SMT(QF-LIA) solver could produce the following unsatisfiable core:

  {vtx + y ≥ 4,
  t = −1 → vtx = −x,             y ≤ 1,
   t = 0 → vtx = 0,             −1 ≤ t, −1 ≤ x,
  t = 1 → vtx = x,               t ≤ 1,  x ≤ 1}


   Intuitively, if |t|, |x|, y ≤ 1, then it cannot be the case that tx+y ≥ 4. At this stage, one
has to relax at least one of the artificial bounds in the core, for example x ≤ 1. Notice
that, on the other hand, the core does not provide any help in regard to deciding the
new upper bound for x. If, e.g., we chose that it were x ≤ 4, then x ≤ 4 would replace
x ≤ 1 in the set of artificial bounds B , and the following clauses would be added to the
linearization F :
                                          x = 2 → vx2 = 4
                                          x = 3 → vx2 = 9
                                          x = 4 → vx2 = 16
  In the next iteration one could already find solutions to the non-linear formula F0 ,
for instance, t = vt2 = w = vw2 = y = vy2 = 1, x = vtx = 3, and vx2 = 9.            
3. SOLVING SMT(QF-NIA) WITH MINIMAL MODELS
Taking into account the limitations of the method based on cores when domains have
to be extended, in this section we present a model-guided approach to perform this
step. Namely, we propose to replace the satisfiability check in linear arithmetic with
an optimization call, so that the best model found by the linear solver can be used as a
reference for relaxing the bounds.
   This is the key idea of the procedure solve SMT QF NIA min models for solving
SMT(QF-NIA) shown in Algorithm 6 (cf. Algorithm 1; note that all subprocedures
except for optimize QF LIA and new domains min models are the same). Now the
SMT(QF-LIA) black box (procedure optimize QF LIA) does not just decide satisfiabil-
ity, but finds the minimal model of its input formula F according to a certain cost
function. If this model does not satisfy the original non-linear formula, then it can
be employed as a hint in the domain relaxation (procedure new domains min models,
with pseudo-code in Algorithm 7) as follows. Since the non-linear formula is not sat-
isfied, it must be the case that some of the artificial bounds are not respected by the
minimal model. By gathering these bounds, a set of candidates to be relaxed is ob-
tained, as in the approach of Section 2.2. However, and most importantly, unlike with
unsatisfiable cores now for each of these bounds a new value can be guessed too: one
just needs to take the corresponding variable and enlarge its domain up to the value
assigned in the minimal model. That is, let us assume that V ≤ U is an artificial upper
bound on variable V that is falsified in the minimal model. If V is assigned value U ′
in that model (and, hence, U < U ′ ), then V ≤ U ′ becomes the new upper bound of V . A
similar construction applies for lower bounds.
   The intuition behind this approach is that the cost function should measure how far
assignments are from being a solution to the original non-linear formula. Formally, the
function must be non-negative and have the property that the models of the linearized
formula with cost 0 are true models of the original non-linear formula:

                ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                          A:9


ALGORITHM 6: Algorithm for solving SMT(QF-NIA) with minimal models

status solve SMT QF NIA min models(formula F0 ){ // returns whether F0 is satisfiable
  B = artificial bounds(F0 );                   // B are artificial bounds enough to linearize F0
  F = linearize(F0 , B );
  while (not timed out()) {

     // If ST == UNSAT then F is UNSAT
     // If ST == SAT then M is a model of F minimizing function cost below among all models of F
     hST , M i = optimize QF LIA(F , B );

      if (ST == UNSAT)          return UNSAT;
      else if (cost (M ) == 0) return SAT;
      else {
        B ′ = new domains min models(B, M );
        F = update(F , B , B ′ );                           // add case splitting clauses
        B = B ′;
    }}
    return UNKNOWN;
}


   T HEOREM 3.1. Let F0 be an arbitrary formula in QF-NIA, and F be any lineariza-
tion of F0 in QF-LIA obtained using the procedure linearize with artificial bounds B.
   A function cost that takes as input the models of F is admissible if:
(1) cost (M ) ≥ 0 for any M model of F ;
(2) If cost (M ) = 0 then M is a model of F0 .
  If the cost functions in procedure solve SMT QF NIA min models are admissible
then the procedure is correct. That is, given a formula F0 in QF-NIA:
(1) if solve SMT QF NIA min models (F0 ) returns SAT then formula F0 is satisfiable;
    and
(2) if solve SMT QF NIA min models (F0 ) returns UNSAT then formula F0 is unsatis-
    fiable.
     P ROOF.
   (1) Let us assume that solve SMT QF NIA min models (F0 ) returns SAT. Then there
is a set of artificial bounds B such that F , the linearization of F0 using B, satisfies the
following: optimize QF LIA (F , B) returns a model M of F such that cost (M ) = 0. As
cost is admissible we have that M is a model of F0 .
   (2) Let us assume that solve SMT QF NIA min models (F0 ) returns UNSAT. Then
there is a set of artificial bounds B such that F , the linearization of F0 using B, satisfies
that optimize QF LIA (F , B) returns UNSAT. By the specification of optimize QF LIA,
this means that F is unsatisfiable. But since only case splitting clauses are added in
the linearization, any model of F0 can be extended to a model of F . By reversing the
implication we conclude that F0 must be unsatisfiable.


   Under the assumption that cost functions are admissible, note that, if at some iter-
ation in procedure solve SMT QF NIA min models there are models of the lineariza-
tion with null cost (hence satisfying the original non-linear formula), then the search
is over: optimize QF LIA will return such a model, as it minimizes a non-negative cost
function.

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:10                                                                                   Cristina Borralleras et al.


ALGORITHM 7: Procedure new domains min models
set new domains min models(set B , map M ) { // returns the new set of artificial bounds
  let S ⊆ {b | b ∈ B , M 6|= b} such that S 6= ∅; // choose among bounds violated by the model
  B′ = B;
  for (V ≥ L in S) B ′ = B ′ − {V ≥ L} ∪ {V ≥ M (V )}; // L > M (V ) as M 6|= V ≥ L
  for (V ≤ U in S) B ′ = B ′ − {V ≤ U } ∪ {V ≤ M (V )}; // U < M (V ) as M 6|= V ≤ U
  return B ′ ;
}



ALGORITHM 8: Procedure optimize QF LIA Max SMT based on Max-SMT(QF-LIA)

h status, map i optimize QF LIA Max SMT(formula F , set B ) {
  F′ = F;
  for (V ≥ L in B )
    F ′ = F ′ ∪ {[V ≥ L, 1]};        // added as a soft clause, e.g. with weight 1
  for (V ≤ U in B )
    F ′ = F ′ ∪ {[V ≤ U, 1]};        // added as a soft clause, e.g. with weight 1

    return solve Max SMT QF LIA(F ′ );      // call to Max-SMT solver
}


  In what follows we propose two different admissible (classes of) cost functions: the
number of violated artificial bounds (Section 3.1), and the distance with respect to
the artificial domains (Section 3.2). In both cases, to complete the implementation
of solve SMT QF NIA min models the only procedure that needs to be defined is op-
timize QF LIA, since procedure new domains min models is independent of the cost
function (see Algorithm 7).

3.1. A Max-SMT(QF-LIA) Approach to Domain Relaxation
As sketched out above, a possibility is to define the cost of an assignment as the num-
ber of violated artificial bounds. A natural way of implementing this is to transform
the original non-linear formula into a linearized weighted formula and use a Max-
SMT(QF-LIA) tool. In this setting, the clauses of the linearization are hard, while
the artificial bounds are considered to be soft (e.g., with weight 1 if we literally count
the number of violated bounds). Procedure optimize QF LIA Max SMT is described
formally in Algorithm 8. It is worth highlighting that not only is the underlying Max-
SMT(QF-LIA) solver required to report the optimum value of the cost function, but it
must also produce an assignment in the theory for which this optimum value is at-
tained (so that it can be used in the domain relaxation). A direct and effective way of
accomplishing this task is by performing branch-and-bound on top of an SMT(QF-LIA)
solver, as done in [Nieuwenhuis and Oliveras 2006]3 .
   The next lemma justifies, together with Theorem 3.1, that procedure
solve SMT QF NIA min models, when instantiated with optimize QF LIA Max SMT,
is correct:
   L EMMA 3.2. Let F0 be an arbitrary formula in QF-NIA, and F be any linearization
of F0 in QF-LIA obtained using the procedure linearize with artificial bounds B.

3 Other approaches could also employed for solving Max-SMT(QF-LIA); for example, one could iteratively
obtain unsatisfiable cores and add relaxation variables and cardinality or pseudo-Boolean constraints to the
instance until a SAT answer is obtained [Fu and Malik 2006; Ansótegui et al. 2013; Morgado et al. 2013].
Nevertheless, here we opted for branch-and-bound for its simplicity and because it can be easily adapted to
meet the requirements for solving Max-SMT(QF-NIA); see Section 4.


                   ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                          A:11

  The function cost that takes as an input a model M of F and returns the number of
bounds from B that are not satisfied by M is admissible.
    P ROOF. It is obvious that the function is non-negative. It remains to be proved that,
if cost (M ) = 0, then M |= F0 . Indeed, if cost (M ) = 0 then all bounds in B are satisfied.
But since F is a linearization of F0 with artificial bounds B, we have that all additional
variables standing for non-linear monomials have values in M that are consistent with
the theory. Hence, we conclude that M |= F0 .
  Regarding the weights of the soft clauses, as can be observed from the proof of
Lemma 3.2, it is not necessary to have unit weights. One may use different val-
ues, provided they are positive, and then the cost function corresponds to a weighted
sum. Moreover, note that weights can be different from one iteration of the loop of
solve SMT QF NIA min models to the next one.
   Example 3.3. Let us consider the same formula as in Example 2.1:
                                 tx + y ≥ 4 ∧ t2 + x2 + w2 + y 2 ≤ 12.
Recall that, in this case, the artificial bounds are −1 ≤ t, x, w, y ≤ 1. We obtain the
weighted formula consisting of the clauses of F (as defined in Example 2.1) as hard
clauses, and

                     [−1 ≤ t, 1] ∧ [−1 ≤ x, 1] ∧ [−1 ≤ w, 1] ∧ [−1 ≤ y, 1] ∧
                       [t ≤ 1, 1] ∧ [x ≤ 1, 1] ∧ [w ≤ 1, 1] ∧ [y ≤ 1, 1] ,
as soft clauses (written following the format [clause, weight]).
  In this case minimal solutions have cost 1: at least one of the artificial bounds has to
be violated so as to satisfy vtx +y ≥ 4. For instance, the Max-SMT(QF-LIA) solver could
return the assignment: t = vt2 = 1, x = vtx = 4 and w = vw2 = y = vy2 = vx2 = 0, where
the only soft clause that is violated is [x ≤ 1, 1]. Note that, as x = 4 is not covered by
the case splitting clauses for vx2 , the values of vx2 and x are unrelated. Now the new
upper bound for x would become x ≤ 4 (so the soft clause [x ≤ 1, 1] would be replaced
by [x ≤ 4, 1]), and similarly to Example 2.1, the following hard clauses would be added:
                                               x = 2 → vx2 = 4
                                               x = 3 → vx2 = 9
                                               x = 4 → vx2 = 16
  As seen in Example 2.1, in the next iteration there are solutions with cost 0, e.g.,
t = vt2 = w = vw2 = y = vy2 = 1, x = vtx = 3 and vx2 = 9.                           
  One of the disadvantages of this approach is that potentially the Max-SMT(QF-LIA)
solver could return models with arbitrarily large numerical values: note that what the
cost function takes into account is just whether a bound is violated or not, but not by
how much. For instance, in Example 2.1, it could have been the case that the Max-
SMT(QF-LIA) solver returned w = y = 0, t = 1, x = 105 , vx2 = 0, etc. Since the model is
used for extending the domains, a large number would involve adding a prohibitive
number of case splitting clauses, and at the next iteration the Max-SMT(QF-LIA)
solver would not able to handle the formula with a reasonable amount of resources.
However, having said that, as far as we have been able to experiment, this kind of
behaviour is rarely observed in our implementation; see Section 3.3 for more details.
On the other hand, the cost function in Section 3.2 below does not suffer from this
drawback.

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:12                                                                                     Cristina Borralleras et al.


ALGORITHM 9: Procedure optimize QF LIA OMT based on OMT(QF-LIA)

h status, map i optimize QF LIA OMT(formula F , set B ) {

    F′ = F;
    E = 0;                                            // expression for the cost function

    for (V ≥ L in B ) {
      lV = fresh variable();
      F ′ = F ′ ∪ {lV ≥ 0, lV ≥ L − V };
      E = E + lV ;
    }

    for (V ≤ U in B ) {
      uV = fresh variable();
      F ′ = F ′ ∪ {uV ≥ 0, uV ≥ V − U };
      E = E + uV ;
    }

    F ′ = F ′ ∪ {cost = E};                               // cost is the variable to be minimized

    return solve OMT QF LIA(hcost , F ′ i));           // call to OMT solver
}


3.2. An OMT(QF-LIA) Approach to Domain Relaxation
Another possibility of cost function for models of the linearization is to measure the dis-
tance with respect to the artificial domains. This can be cast as a problem in OMT(QF-
LIA) as follows.
  Given a non-linear formula F0 , let us consider a linearization F obtained after apply-
ing procedure linearize with artificial bounds B . Now, let vars(B ) be the set of variables
V for which an artificial
                    P domain [lV , UV ] ∈ B is added for the linearization. Formally,
the cost function is V ∈vars(B ) δ(V, [lV , UV ]), where δ(z, [l, U ]) is the distance of z with
respect to [l, U ]:

                                                          l − z if z < l
                                                      (
                                    δ(z, [l, U ]) =       0     if l ≤ z ≤ U
                                                          z − U if z > U

Note that, in the definition of the cost function, one can safely also include bounds
which are not artificial but derived from the non-linear formula: the contribution to
the cost of these is null, since they are part of the original formula and therefore must
always be respected.
  The approach is implemented in the procedure optimize QF LIA OMT shown
in Algorithm 9. In this procedure, an OMT(QF-LIA) solver is called (procedure
solve OMT QF LIA). Such a system can be built upon an existing SMT(QF-LIA) solver
by adding an optimization simplex phase II [Schrijver 1998] when the SAT engine
reaches a leaf of the search space. For the OMT(QF-LIA) solver to handle the cost
function, the problem requires the following reformulation. Let cost be the variable
that the solver minimizes. For each variable V ∈ vars(B ) with domain [lV , UV ], let us
introduce once and for all two extra integer variables lV and uV (meaning the distance
with respect to the lower and to the upper bound of the domain of V , respectively) and
the auxiliary constraints lV ≥ 0, lV ≥ lV − V ,P    uV ≥ 0, uV ≥ V − UV . Then the cost
function is determined by the equation cost = V ∈vars(B ) (lV + uV ), which is added to
the formula together with the aforementioned auxiliary constraints.

                     ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                              A:13

  The following result claims that the proposed cost function is admissible. Hence,
by virtue of Theorem 3.1, if procedure optimize QF LIA OMT is implemented as in
Algorithm 9, then procedure solve SMT QF NIA min models is sound:
   L EMMA 3.4. Let F0 be an arbitrary formula in QF-NIA, and F be any linearization
of F0 in QF-LIA obtained using the procedure linearize with artificial bounds B.
   The function cost that takes as an input a model of F and returns its distance to the
artificial domains:
                                                X
                                                          δ(V, [lV , UV ])
                                            V ∈vars(B )

  is admissible.
   P ROOF. The proof is analogous to that of Lemma 3.2.
  Intuitively the proposed cost function corresponds to the number of new
cases that will have to be added in the next iteration of the loop in
solve SMT QF NIA min models. However, it is also possible to consider slightly dif-
ferent cost functions: for instance, one could count the number of new clauses that will
have to be added. For this purpose, it is only necessary to multiply variables lV , uV
in the equation that defines cost by the number of monomials that were linearized by
case splitting on V . In general, similarly
                                   P         to Section 3.1, one may have a template of
cost function of the form cost = V ∈vars(B ) (αV lV + βV uV ), where αV , βV > 0 for all
V ∈ vars(B ). Further, again these coefficients may be changed from one iteration to the
next one.
   Example 3.5. Yet again let us take the same non-linear formula from Example 2.1:
                                 tx + y ≥ 4 ∧ t2 + x2 + w2 + y 2 ≤ 12.
Let us also recall the artificial bounds: −1 ≤ t, x, w, y ≤ 1. By using the linearization
F as defined in Example 2.1, one can express the resulting OMT(QF-LIA) problem as
follows:
          min δ(t, [−1, 1]) + δ(x, [−1, 1]) + δ(w, [−1, 1]) + δ(y, [−1, 1]) subject to F ,
or equivalently,
                                             min cost subject to
                                                       F ∧
                  lt ≥ 0     ∧     lt ≥ −1 − t         ∧ ut ≥ 0              ∧   ut ≥ t − 1          ∧
                 lx ≥ 0      ∧    lx ≥ −1 − x          ∧ ux ≥ 0              ∧   ux ≥ x − 1          ∧
                 lw ≥ 0      ∧    lw ≥ −1 − w          ∧ uw ≥ 0              ∧   uw ≥ w − 1          ∧
                  ly ≥ 0     ∧     ly ≥ −1 − y         ∧ uy ≥ 0              ∧   uy ≥ y − 1          ∧
                             cost = lt + ut + lx + ux + lw + uw + ly + uy

  In this case, it can be seen that minimal solutions have cost 1. For example, the
OMT(QF-LIA) solver could return the assignment: x = vx2 = 1, t = 2, vtx = 4 and
w = vw2 = y = vy2 = vt2 = 0. Note that, as t = 2 is not covered by the case splitting
clauses, the values of vtx and vt2 are unrelated to t. Now the new upper bound for t is
t ≤ 2, and clauses
                                               t = 2 → vtx = 2x
                                               t = 2 → vt2 = 4

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:14                                                                                   Cristina Borralleras et al.

are added to the linearization.
   At the next iteration there is still no solution with cost 0, so at least another further
iteration is necessary before a true model of the non-linear formula can be found. 
   One of the drawbacks of this approach is that, as the previous example suggests,
domains may be enlarged very slowly. This implies that, in cases where solutions have
large numbers, many iterations are needed before one of them is discovered. See Sec-
tion 3.3 below for more details on the performance of this method in practice.
3.3. Experimental Evaluation of Model-guided Approaches
Here we evaluate experimentally our approaches for SMT(QF-NIA) and compare them
with other non-linear solvers, namely those participating in the QF-NIA division of
the 2016 edition of SMT-COMP (http://smtcomp.sourceforge.net). More in detail, we
consider the following tools:
— AProVE-NIA [Fuhs et al. 2007] with its default configuration;
— CVC4 [Barrett et al. 2011] version of 05-27-2016;
— ProB [Krings et al. 2015];
— SMT-RAT [Corzilius et al. 2015];
— yices-2 [Dutertre 2014] version 2.4.2;
— raSAT [Tung et al. 2016], with two different versions: raSAT-0.3 and raSAT-0.4 exp;
— z3 [de Moura and Bjørner 2008b] version 4.4.1;
— bcl-cores, our core-based algorithm [Borralleras et al. 2012];
— bcl-maxsmt, our Max-SMT-based algorithm from Section 3.1;
— bcl-omt, our OMT-based algorithm from Section 3.2.
  All bcl-* solvers4 share essentially the same underlying SAT engine and QF-LIA
theory solver. Moreover, some strategies are also common:
— procedure artificial bounds uses a greedy algorithm for approximating the mini-
  mum set of variables that have to be introduced in the linearization (as shown
  in [Borralleras et al. 2012], computing a set with minimum size is NP-complete).
  For each of these variables we force the domain [−1, 1], even if variables have true
  bounds (for ease of presentation, we will assume here that true bounds always con-
  tain [−1, 1]). This turns out to be useful in practice, as quite often satisfiable formu-
  las have solutions with small coefficients. By forcing the domain [−1, 1], unnecessary
  case splitting clauses are avoided and the size of the linearized formula is reduced.
— the first time a bound is chosen to be relaxed is handled specially. Let us assume
  it is the first time that a lower bound (respectively, an upper bound) of V has to
  be relaxed. By virtue of the remark above, the bound must be of the form V ≥ −1
  (respectively, V ≤ 1). Now, if V has a true bound of the form V ≥ L (respectively,
  V ≤ U ), then the new bound is the true bound. Otherwise, if V does not have a true
  lower bound (respectively, upper bound), then the lower bound is decreased by one
  (respectively, the upper bound is increased by one). Again, this is useful to capture
  the cases in which there are solutions with small coefficients.
— from the second time on, domain relaxation of bcl-maxsmt and bcl-omt follows ba-
  sically what is described in Section 3, except for a correction factor aimed at in-
  stances in which solutions have some large values. Namely, if V ≤ u has to be re-
  laxed and in the minimal model V is assigned value U , then the new upper bound is
                  n
  U + α · min(β, m  ), where α and β are parameters, n is the number of times the upper
  bound of V has been relaxed, and m is the number of occurrences of V in the origi-
  nal formula. As regards bcl-cores, a similar expression is used in which the current
4 Available at http://www.lsi.upc.edu/∼albert/tocl2017.tgz.




                   ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                          A:15

   bound u is used instead of U , since there is no notion of “best model”. The analogous
   strategy is applied for lower bounds.
  The experiments were carried out on the StarExec cluster [Stump et al. 2014], whose
nodes are equipped with Intel Xeon 2.4GHz processors. The memory limit was set to
60 GB, the same as in the 2016 edition of SMT-COMP. As regards wall clock time,
although in SMT-COMP jobs were limited to 2400 seconds, in our experiments the
timeout was set to 1800 seconds, which is the maximum that StarExec allowed us.
  Two different sources of benchmarks were considered in this evaluation. The first
benchmark suite (henceforth referred to as Term) was already used in the confer-
ence version of this paper [Larraz et al. 2014] and consists of 1934 instances generated
by the constraint-based termination prover described in [Larraz et al. 2013]. In these
problems non-linear monomials are quadratic.
  The other benchmarks are the examples of QF-NIA in the SMT-LIB
[Barrett et al. 2016], which are grouped into the following families:
— AProVE: 8829 instances
— calypto: 177 instances
— LassoRanker: 120 instances
— leipzig: 167 instances
— mcm: 186 instances
— UltimateAutomizer: 7 instances
— UltimateLassoRanker: 32 instances
— LCTES: 2 instances
  Results are displayed in two tables (Tables I and II) for the sake of presentation.
Rows represent systems and distinguish between SAT and UNSAT outcomes. Columns
correspond to benchmark families. For each family, the number of instances is indi-
cated in parentheses. The cells either show the number of problems of a given family
that were solved by a particular system with a certain outcome, or the total time (in
seconds) to process all of them. The best solver for each family (for SAT and for UNSAT
examples) is highlighted in bold face.



Due to lack of space, the results for family LCTES do not appear in the tables. This
family consists of just two benchmarks, one of which was not solved by any system.
The other instance was only solved by CVC4, which reported UNSAT in 0.5 seconds.
   As the tables indicate, overall our techniques perform well on SAT instances, being
the results particularly favourable for the Term family. This is natural: linearizing by
case splitting is aimed at finding solutions quickly without having to pay the toll of
heavy-weight non-linear reasoning. If satisfiable instances have solutions with small
domains (which is often the case, for instance, when they come from our program anal-
ysis applications), our techniques usually work well. On the other hand, for families
Aprove, leipzig and mcm the results are only comparable or slightly worse than those
obtained with other tools5 . One of the reasons could be that, at least for Aprove and
leipzig, formulas have a very simple Boolean structure: they are essentially conjunc-
tions of literals and few clauses (if any). For this particular kind of problems CAD-
based techniques such as those implemented in yices-2 and z3, which are precisely
targeted at conjunctions of non-linear literals, may be more adequate.

5 However, it must be remarked that we detected several inconsistencies between raSAT-0.3 and the rest of
the solvers in the family mcm, which makes the results of this tool unreliable.


ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
   A:16                                                                                            Cristina Borralleras et al.


Table I. Experimental evaluation of SMT(QF-NIA) solvers on benchmark families Term, AProVE, calypto and Lasso-
Ranker.
                                          Term                        AProVE                   calypto                LassoRanker
                                         (1934)                       (8829)                    (177)                    (120)
                                  # p.            time         # p.           time      # p.          time          # p.        time
                       SAT           0            0.00       8,028        4,242.65       77       1,715.02             3        1.97
  AProVE-NIA
                      UNSAT          0            0.00            0            0.00       0           0.00             0        0.00
                       SAT         45         8,898.80       7,892      144,767.87       25          78.29             4     692.98
     CVC4
                      UNSAT          0            0.00          10             0.18      35           0.71           71         1.26
                       SAT           0            0.00       7,415       19,715.86       41          85.52             3        3.07
     ProB
                      UNSAT          0            0.00          16           15.70       13         498.51             0        0.00
                       SAT        232        82,122.64       8,026          313.44       79         163.58             3        0.64
   SMT-RAT
                      UNSAT        15         1,377.74         221        7,654.78       89         663.89           21        12.59
                       SAT      1,830        79,764.09       7,959        3,293.65       79           6.53             4        0.16
    yices-2
                      UNSAT        69           940.15         764        4,964.66       97         488.38           97      875.44
                                                                ¯             ¯           ¯            ¯
                       SAT         20         2,444.87       7,421       35,053.18       32       3,393.93             3        2.41
   raSAT-0.3
                      UNSAT          0            0.00         320      554,482.86       47      30,232.16           43   75,603.23
                       SAT         36         5,161.97       7,745       50,695.06       31         954.16             3        1.54
 raSAT-0.4 exp
                      UNSAT          4        2,454.21          18          105.59       31         547.26             2        2.46
                       SAT        194        77,397.16       8,023       14,790.21       79         943.03             4       13.16
      z3
                      UNSAT        70         3,459.77         286        7,989.62       96       1,932.11          100    3,527.34
                                    ¯             ¯
                       SAT      1,857         4,396.09       8,028        1,726.49       80           6.20             4        0.09
   bcl-cores                                                   ¯15            ¯0.41
                      UNSAT          0            0.00                                   94       1,596.99           72         2.53
                       SAT      1,857           811.54       8,027        1,763.70       80           5.74             4        0.08
  bcl-maxsmt
                      UNSAT       ¯67               ¯
                                                 31.33         202           51.50        ¯
                                                                                         97              ¯
                                                                                                    994.17          103¯          ¯
                                                                                                                                2.96
                                                                                                                     ¯            ¯
                       SAT      1,854         6,420.59       8,013       25,274.94       80           6.75             4        0.10
    bcl-omt
                      UNSAT        67            34.99         203           36.18       97       1,327.95          103         3.59


    Table II. Experimental evaluation of SMT(QF-NIA) solvers on benchmark families leipzig, mcm, UltimateAu-
    tomizer (UA) and UltimateLassoRanker (ULR).
                                              leipzig                   mcm                   UA                     ULR
                                               (167)                    (186)                 (7)                    (32)
                                      # p.            time      # p.            time     # p. time           # p.          time
                          SAT         161         1,459.27         0             0.00      0      0.00          6          5.02
      AProVE-NIA
                         UNSAT          0             0.00         0             0.00      0      0.00          0          0.00
                          SAT         162           237.63       48       22,899.02        0      0.00          6          3.76
           CVC4                        ¯0              ¯          ¯0           ¯ 0.00
                         UNSAT                        0.00                                 6      0.06        22          69.19
                          SAT          50          54.81           1       1,631.89        0      0.00          4          5.58
            ProB
                         UNSAT          0           0.00           0             0.00      1      1.02          1          1.34
                          SAT         160       2,827.37         21        2,516.21        0      0.00          6          0.86
          SMT-RAT
                         UNSAT          0           0.00           0             0.00      1      2.44        24         186.14
                          SAT          92         715.04         11        5,816.44        0      0.00          6          0.05
           yices-2
                         UNSAT          1           0.01           0             0.00      7      0.02        26¯             ¯
                                                                                                                          11.07
                                         ¯            ¯                                     ¯       ¯          ¯             ¯
                          SAT          32      15,758.07           2       1,787.57        0      0.00          2          5.88
        raSAT-0.3
                         UNSAT          1       1,800.07         99      178,204.54        1      5.28          1      1,351.68
                                                                  ¯           ¯
                          SAT         134      17,857.21           8       3,309.13        0      0.00          3          1.60
      raSAT-0.4 exp
                         UNSAT          0           0.00           0             0.00      1      8.08          1          1.50
                          SAT         162       1,472.00         23        3,906.84        0      0.00          6          0.34
              z3
                         UNSAT          0           0.00           7       7,127.61        7      0.54        26          45.20
                          SAT         158       3,596.74         15        1,160.10        0      0.00          6          0.33
          bcl-cores
                         UNSAT          0           0.00           0             0.00      1      0.06        24          32.87
                          SAT         153       4,978.91         17        1,004.25        0      0.00          6          0.31
       bcl-maxsmt
                         UNSAT          0           0.00           0             0.00      1      0.02        26          28.56
                          SAT         148       7,351.45         19        2,937.99        0      0.00          6          0.34
           bcl-omt
                         UNSAT          0           0.00           0             0.00      1      0.02        26          29.36



                        ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                           A:17

   Regarding UNSAT instances, it can be seen that our approaches, while often compet-
itive, can be outperformed by other tools in some families. Again, this is not surprising:
linearizing may not be sufficient to detect unsatisfiability when deep non-linear rea-
soning is required. On the other hand, sometimes there may be a purely linear argu-
ment that proves that an instance is unsatisfiable. Our techniques can be effective in
these situations, which may be relatively frequent depending on the application. This
would be the case of families Term, calypto, LassoRanker and ULR.
   Comparing our techniques among themselves, overall bcl-maxsmt tends to give the
best results in terms of number of solved SAT and UNSAT instances and timings. For
example, we can see that bcl-cores proves many fewer unsatisfiable instances than
model-guided approaches. The reason is the following. Let F0 be a formula in QF-NIA,
and F be a linearization of F0 computed with artificial bounds B. Let us assume that
F is unsatisfiable. In this case, when the algorithm in bcl-cores tests the satisfiability
of F ∧ B, it finds that it is unsatisfiable. Then, if we are lucky and an unsatisfiable
core that only uses clauses from F is obtained, then it can be concluded that F0 is
unsatisfiable immediately. However, there may be other unsatisfiable cores of F ∧ B,
which use artificial bounds 6 . Using such a core leads to performing yet another (use-
less) iteration of domain relaxation. Unfortunately the choice of the unsatisfiable core
depends on the way the search space is explored, which does not take into account
whether bounds are original or artificial so as not to interfere with the Boolean en-
gine heuristics. On the other hand, model-guided approaches always detect when the
linearization is unsatisfiable. As for SAT instances, the number of solved problems of
bcl-cores is similar to that of bcl-maxsmt, but the latter tends to be faster.
   Regarding bcl-omt, it turns out that, in general, the additional iterations required
in the simplex algorithm to perform the optimization are too expensive. Moreover,
after inspecting the traces we have confirmed that as Example 3.5 suggested, bcl-omt
enlarges the domains too slowly, which is hindering the search.
3.4. Variants
According to the experiments in Section 3.3, altogether the approach based on Max-
SMT(QF-LIA) gives the best results among our methods. In this section we propose
several ideas for improving it further.
   3.4.1. Non-incremental Strategy. A common feature of the procedures for solving
SMT(QF-NIA) described in Sections 2.2, 3.1 and 3.2 is that, when no model of the
linearization is found that satisfies all artificial bounds, the domains are enlarged.
Thus, iteration after iteration, the number of case splitting clauses increases. In this
sense, the aforementioned methods are incremental. A disadvantage of this incremen-
tality is that, after some iterations, the formula size may easily become too big to be
manageable.
   On the other hand, instead of enlarging a domain, one can follow a non-incremental
strategy and replace the domain by another one that might not include it. For example,
in the model-guided approaches, when computing the new domain for a variable one
may discard the current domain and for the next iteration take an interval centered
at the value in the minimal model (procedure new domains min models non inc, de-
scribed in Algorithm 10). The procedure for updating the formula has to be adapted
accordingly too, so that the case splitting clauses correspond to the values in the arti-
ficial domains (procedure update non inc, shown in Algorithm 11). In this fashion one

6 For the sake of efficiency, bcl-cores does not guarantee that cores are minimal with respect to subset in-
clusion: computing minimal unsatisfiable sets [Belov et al. 2012] to eliminate irrelevant clauses implies an
overhead that in our experience does not pay off. But even if minimality were always achieved, there could
still be unsatisfiable cores in F ∧ B using artificial bounds.


ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:18                                                                                  Cristina Borralleras et al.


ALGORITHM 10: Procedure new domains min models non inc
set new domains min models non inc(set B , map M ) { // returns the new set of artificial bounds
  let S ⊆ {b | b ∈ B , M 6|= b} such that S 6= ∅;   // choose among bounds violated by the model
  W = {var(b) | b ∈ S};                             // variables with domain to be relaxed
    ′
  B = {b | b ∈ B ∧ var(b) 6∈ W };
  for (V in W )
    B ′ = B ′ ∪ {M (V ) − R ≤ V ≤ M (V ) + R};      // for a parameter R > 0
  return B ′ ;
}



ALGORITHM 11: Procedure update non inc

formula update non inc(formula F , set B, set B ′ ) {
  W = {var(b) | b ∈ B ′ − B };                              // variables whose domain has changed
  F ′ = remove case splits(F , W );                         // remove outdated case splitting clauses
  for (V in W ) {
    let L, U such that L ≤ V ≤ U ∈ B ′ ;
    for (K in [L, U ])
        for (Q such that V == linearization variable(Q))   // V was used to linearize monomial Q
           F ′ = F ′ ∪ { V = K → VQ = evaluate(Q, V , K)}; // VQ is the variable standing for Q
  }               W
  return F ′ ∪ { b∈B ¬b};                                   // forbid B : no solution there
}



can control precisely the number of case splitting clauses, and therefore the size of the
formula.
  Since monotonicity of domains from one iteration to the next one is now not main-
tained, this approach requires bookkeeping so as to avoid repeating the same choice of
artificial domains. One way to implement this is to add clauses that forbid each of the
combinations of domains that have already been tried and with which no model of the
original formula was found. Namely, let B be such a combination of artificial bounds.
We add the (hard) clause ∨b∈B ¬b, which forces that at least one of the bounds in B can-
not hold. Now, in any following iteration, if the minimal model M of the linearization
does not satisfy the non-linear formula, the new set of artificial bounds B ′ is such that
M |= B ′ . This together with M 6|= B implies B ′ 6|= B , and therefore artificial bounds
cannot be repeated. See procedure update non inc in Algorithm 11.
  Finally note that, although this alternative strategy for producing new artificial
bounds can in principle be adapted to either of the model-guided methods, it makes
the most sense for the Max-SMT(QF-LIA)-based procedure. The reason is that, being
model-guided, in this approach the next domains to be considered are determined by
the minimal model and, as already observed in Section 3.1, this minimal model may
assign large values to variables and thus lead to intractable formula growth.

   Example 3.6. Let us take the formula and artificial bounds of the running example.
We resume Example 3.3, where the following minimal solution of cost 1 was shown:
t = vt2 = 1, x = vtx = 4 and w = vw2 = y = vy2 = vx2 = 0, being x ≤ 1 the only
violated artificial bound. Now, taking a radius R = 2 for the interval around x = 4, in
the next iteration the following artificial bounds would be considered: −1 ≤ t, w, y ≤ 1
and 2 ≤ x ≤ 6. Moreover, the following clause would be added to the linearization:

  −1 > t ∨ 1 < t ∨ −1 > x ∨ 1 < x ∨ −1 > w ∨ 1 < w ∨ −1 > y ∨ 1 < y

                  ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                          A:19

together with
                                          (x = 2 → vx2 = 4)              ∧
                                          (x = 3 → vx2 = 9)              ∧
                                          (x = 4 → vx2 = 16)             ∧
                                          (x = 5 → vx2 = 25)             ∧
                                          (x = 6 → vx2 = 36),
while clauses
                                          (x = −1 → vx2 = 1)             ∧
                                          (x = 0 → vx2 = 0)              ∧
                                          (x = 1 → vx2 = 1)
would be removed.                                                                                      

   3.4.2. Optimality Cores. When following the approach presented in Section 3.4.1, one
needs to keep track of the combinations of domains that have already been attempted,
in order to avoid repeating work and possibly entering into cycles. As pointed out
above, this can be achieved for instance by adding clauses that exclude these combi-
nations of domains. From the SMT perspective, these clauses can be viewed as conflict
explanations, if one understands a conflict as a choice of artificial domains that does
not lead to a solution to the original non-linear problem. Following the SMT analogy,
it is important that explanations are as short as possible. In this section we present a
technique aimed at reducing the size of these explanations.
   Let us focus on the model-guided procedures, in which at each iteration one mini-
mizes a cost function.

   Definition 3.7. Let F be a clause set with variables X, and let cost : X → R be a
function. Let C ⊆ F be a subset of the clauses and cost ′ : X → R be another func-
tion. We say that the pair (C, cost′ ) is an optimality core of the minimization problem
min{cost(M ) | M |= F } if the following conditions hold:

(1) cost′ ≤ cost; and
(2) min{cost ′ (M ) | M |= C} = min{cost(M ) | M |= F }.

   The interest of optimality cores in our context is that they allow identifying a subset
of the artificial bounds that is enough for soundly discarding the current combina-
tion of domains (and possibly many more). Let us now describe how optimality cores
and these subsets of artificial bounds may be obtained in the Max-SMT approach. In
this case, one searches the minimum number of violated artificial bounds. In a simi-
lar way to resolution refutations obtained from unsatisfiable instances, after each call
to the Max-SMT(QF-LIA) solver on the linearization with soft artificial bounds one
may retrieve a lower bound certificate [Larrosa et al. 2011]. This certificate consists
essentially of a tree of cost resolution steps, and proves that any model of the lineariza-
tion will violate at least as many artificial bounds as the reported optimal model. Now
consider the leaves of this tree. Let H be those leaves which are hard clauses (corre-
sponding to clauses of the linearization), and S be those which are soft (corresponding
to soft bounds). If we call cost S the function that counts the number of bounds from S
that are not satisfied, from the definition it follows that (H, cost S ) is an optimality core.
In particular, we are interested in the set of artificial bounds S: if the optimal model
of the Max-SMT problem has positive cost, then there is no model of the linearization
that can also satisfy S. So we can soundly add the clause ∨b∈S ¬b, which replaces the
(potentially much) longer clause ∨b∈B ¬b in Algorithm 11.

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:20                                                                                Cristina Borralleras et al.

  Example 3.8. Once more let us consider the running example. We proceed as in
Example 3.6, but instead of adding the clause
  −1 > t ∨ 1 < t ∨ −1 > x ∨ 1 < x ∨ −1 > w ∨ 1 < w ∨ −1 > y ∨ 1 < y
we add
                     −1 > t ∨ 1 < t ∨ −1 > x ∨ 1 < x ∨ 1 < y,
i.e., we discard the literals −1 > w, 1 < w and −1 > y. Following the above notation,
we can do that since (H, cost S ) is an optimality core, where H is
         {vtx + y ≥ 4,    t = −1 → vtx = −x,            t = 0 → vtx = 0,         t = 1 → vtx = x}
and S is
              {[−1 ≤ t, 1],     [t ≤ 1, 1],    [−1 ≤ x, 1],       [x ≤ 1, 1],     [y ≤ 1, 1]}.
                                                                                                               
3.5. Experimental Evaluation of Max-SMT(QF-LIA)-based Approaches
In this section we evaluate experimentally the variations of the Max-SMT(QF-LIA)
approach proposed in Sections 3.4.1 and 3.4.2. In addition to the benchmarks used in
Section 3.3, we have also considered instances produced by our constraint-based termi-
nation prover VeryMax (http://www.cs.upc.edu/∼albert/VeryMax.html) on the divisions
of the termination competition termCOMP 2016 [Termination Competition ] in which
it participated, namely Integer Transition Systems and C Integer. Since internally Very-
Max generates Max-SMT(QF-NIA) rather than SMT(QF-NIA) problems, soft clauses
were removed. Given the huge number of obtained examples, of the order of tens of
thousands, we could not afford carrying out the experiments will all the tools consid-
ered in Section 3.3, and had to restrict the evaluation to the competing solvers that
overall performed the best, namely z3 and yices-2. Hence, in addition to these two, the
following solvers are considered here:
— bcl-maxsmt, the Max-SMT(QF-LIA)-based approach as in Section 3.3;
— bcl-ninc, the non-incremental algorithm from Section 3.4.1;
— bcl-ninc-cores, the non-incremental algorithm that uses optimality cores from Sec-
  tion 3.4.2.
   Moreover, to further reduce the time required by the experiments, we decided to dis-
card those benchmarks which could be solved both by yices-2 and bcl-maxsmt in neg-
ligible time (less than 0.5 seconds). After this filtering, finally 20354 and 2019 bench-
marks were included in families Integer Transition Systems and C Integer, respectively.
   Results are displayed in Tables III, IV and V, following the same format as in Section
3.3.




   These results confirm that, in general, our techniques work well on SAT instances:
except for families leipzig, mcm and UA, the best tool is one of the bcl-* solvers. The gap
with respect to yices-2 and z3 is particularly remarkable on benchmarks coming from
our termination proving applications (families Term, Integer Transition Systems and C
Integer).
   On the other hand, as was already justified in Section 3.3, regarding UNSAT prob-
lems, in some families the bcl-* solvers are clearly outperformed by the CAD-based

                ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
 Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                                                 A:21

Table III. Experimental evaluation of SMT(QF-NIA) solvers on benchmark families Term, AProVE, calypto and Lasso-
Ranker.
                                           Term                      AProVE                   calypto            LassoRanker
                                          (1934)                      (8829)                   (177)                 (120)
                                   # p.          time            # p.         time       # p.        time       # p.       time
                        SAT      1,830      79,764.09          7,959      3,293.65        79          6.53         4       0.16
    yices-2
                       UNSAT        69         940.15            764      4,964.66        97       488.38        97     875.44
                                                                   ¯          ¯
                        SAT        194      77,397.16          8,023     14,790.21        79       943.03          4      13.16
       z3
                       UNSAT        70       3,459.77            286      7,989.62        96 1,932.11           100 3,527.34
                                     ¯           ¯
                        SAT      1,857         811.54          8,027      1,763.70        80          5.74         4       0.08
  bcl-maxsmt
                       UNSAT        67          31.33            202         51.50        97       994.17       103¯         ¯
                                                                                                                           2.96
                                                                                                                 ¯           ¯
                        SAT      1,857         276.20          8,028      1,777.97        80          5.50         4       0.10
    bcl-ninc                       ¯67             ¯             ¯            ¯            ¯            ¯
                       UNSAT                   191.66            202         51.72        97       155.32       103       13.63
                                                                                           ¯          ¯
                        SAT      1,857         349.48          8,028      1,825.93        80          5.54         4       0.10
 bcl-ninc-cores
                       UNSAT        67         184.41            202         57.52        97       273.15       103        9.31

      Table IV. Experimental evaluation of SMT(QF-NIA) solvers on benchmark families leipzig, mcm, Ulti-
      mateAutomizer (UA) and UltimateLassoRanker (ULR).
                                                 leipzig                 mcm                  UA                  ULR
                                                  (167)                  (186)                (7)                 (32)
                                          # p.         time       # p.        time       # p. time           # p.     time
                               SAT         92        715.04        11     5,816.44         0      0.00          6     0.05
            yices-2
                              UNSAT          1          0.01         0        0.00         7      0.02        26¯        ¯
                                                                                                                     11.07
                                             ¯            ¯                                 ¯       ¯          ¯        ¯
                               SAT        162      1,472.00        23     3,906.84         0      0.00          6     0.34
               z3                          ¯0          ¯0.00        ¯7        ¯
                              UNSAT                                       7,127.61         7      0.54        26 45.20
                                                                     ¯        ¯
                               SAT        153      4,978.91        17     1,004.25         0      0.00          6     0.31
         bcl-maxsmt
                              UNSAT          0          0.00         0        0.00         1      0.02        26 28.56
                               SAT        155      5,193.20        23     3,983.74         0      0.00          6     0.33
            bcl-ninc
                              UNSAT          0          0.00         0        0.00         1      0.02        26 28.47
                               SAT        156      3,602.32        19     2,037.77         0      0.00          6     0.40
        bcl-ninc-cores
                              UNSAT          0          0.00         0        0.00         1      0.02        26 31.28

            Table V. Experimental evaluation of SMT(QF-NIA) solvers on benchmark families LCTES,
            Integer Transition Systems (ITS) and C Integer (CI).
                                                   LCTES                       ITS                       CI
                                                      (2)                    (20354)                   (2019)
                                                 # p. time            # p.              time    # p.          time
                                  SAT               0     0.00      8,408        471,160.33     714      84,986.50
                    yices-2
                                 UNSAT              0     0.00      4,085        142,965.19     246      24,498.79
                                                                       ¯              ¯
                                  SAT               0     0.00      5,993        784,681.66     566      16,827.79
                      z3
                                 UNSAT              0     0.00      2,249        504,022.31     504      17,919.88
                                                                                                 ¯           ¯
                                  SAT               0     0.00     11,321        262,793.96     895       6,530.07
                bcl-maxsmt
                                 UNSAT              0     0.00      2,618         35,838.06     148      14,481.72
                                  SAT               0     0.00     11,522        246,918.87     943      15,074.33
                  bcl-ninc                                            ¯               ¯          ¯           ¯
                                 UNSAT              0     0.00      2,502         51,699.62     129       1,722.72
                                  SAT               0     0.00     11,504        244,201.03     941      12,174.59
               bcl-ninc-cores
                                 UNSAT              0     0.00      2,573         49,572.32     142       7,394.77

 techniques of yices-2 and z3. This suggests that a mixed approach that used our meth-
 ods as a filter and that fell back to CAD after some time threshold could possibly take
 the best of both worlds.
   Comparing our techniques among themselves, there is not an overall clear winner.
 For SAT examples, it can be seen that the non-incremental approach is indeed a use-
 ful heuristic: bcl-ninc tends to perform better, being the biggest difference in the Inte-
 ger Transition Systems and C Integer families. As regards optimality cores, as could be
 expected on SAT instances they do not prove profitable and result into a slight over-

 ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:22                                                                                   Cristina Borralleras et al.


ALGORITHM 12: Algorithm for solving Max-SMT(QF-NIA)

hstatus, mapi solve Max SMT QF NIA(formula F0 ) { // returns if H0 is satisfiable and best model wrt. S0
                                                             // H0 are the hard clauses of F0 and S0 the soft ones
  B = artificial bounds(F0 );
  hH, Si = linearize(F0 , B );
  best so far = ⊥;                                         // best model found so far
  max soft cost = ∞;                                       // maximum soft cost we can afford
  while (not timed out()) {
    hST , M i = optimize QF LIA Max SMT threshold(H, S, B, max soft cost);
    if (ST == UNSAT)
      if (best so far == ⊥) return hUNSAT, ⊥i;
      else                     return hSAT, best so far i;
    else if (cost B (M ) == 0) {
      best so far = M ;
      max soft cost = cost S (M ) − 1;                      // let us assume costs are natural numbers
    }
    else {
      B ′ = new domains min models(B , M );
      H = update(H, B , B ′ );                             // add case splitting clauses to the hard part
      B = B ′;
    }
  }
  return hUNKNOWN, ⊥i;
}


head of bcl-ninc-cores with respect to bcl-ninc. On the other hand, on UNSAT examples
quite often (namely, families Term, LassoRanker, Integer Transition Systems and C Inte-
ger) the shorter conflict clauses discarding previous combinations of artificial domains
help in detecting unsatisfiability more efficiently. Still, for this kind of instances bcl-
maxsmt is usually the best of the three, since fewer iterations of the loop in procedure
solve SMT QF NIA min models are required to prove that the formula is unsatisfi-
able.
4. SOLVING MAX-SMT(QF-NIA)
This section is devoted to the extension of our techniques for SMT(QF-NIA) to Max-
SMT(QF-NIA), which has a wide range of applications, e.g. in termination and non-
termination proving [Larraz et al. 2013; Larraz et al. 2014] as well as safety analysis
[Brockschmidt et al. 2015]. Taking into account the results of the experiments in Sec-
tions 3.3 and 3.5, we will choose the Max-SMT(QF-LIA) approaches as SMT(QF-NIA)
solving engines for the rest of this article. In particular, in the description of the fol-
lowing algorithms we will take as a reference the first version explained in Section 3.1,
since adapting the algorithms to the variations from Sections 3.4.1 and 3.4.2 is easy.
4.1. Algorithm
We will represent the input F0 of a Max-SMT(QF-NIA) instance as a conjunc-
tion of a set of hard clauses H0 = {C1 , · · · , Cn } and a set of soft clauses S0 =
{[D1 , Ω1 ], · · · , [Dm , Ωm ]}. The aim is to decidePwhether there exist assignments α such
that α |= H0 , and if so, to find one such that {Ω | [D, Ω] ∈ S0 , α 6|= D} is minimized.
   Procedure solve Max SMT QF NIA for solving Max-SMT(QF-NIA) is shown in Algo-
rithm 12. In its first step, as usual the initial artificial bounds B 7 are chosen (procedure
artificial bounds), with which the input formula F0 ≡ H0 ∧ S0 is linearized (procedure

7 We will abuse notation and represent with B both the set of artificial bounds and also the corresponding
set of weighted clauses. The exact meaning will be clear from the context.


                   ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                          A:23


ALGORITHM 13: Procedure optimize QF LIA Max SMT threshold

hstatus, mapi optimize QF LIA Max SMT threshold(formula H, formula S, set B , number msc) {
  F ′ = H ∪ S;                             // H are hard clauses, S are soft
  for (V ≥ L in B)
    F ′ = F ′ ∪ {[V ≥ L, 1]};              // added as a soft clause, e.g. with weight 1
  for (V ≤ U in B )
    F ′ = F ′ ∪ {[V ≤ U, 1]};              // added as a soft clause, e.g. with weight 1

    return solve Max SMT QF LIA(F ′ , msc);          // call to Max-SMT solver
}


linearize). As a result, a weighted linear formula is obtained with hard clauses H and
soft clauses S, where:
— H results from replacing the non-linear monomials in H0 by their corresponding
  fresh variables, and adding the case splitting clauses;
— S results from replacing the non-linear monomials in S0 by their corresponding fresh
  variables.
   Now notice that there are two kinds of weights: those from the original soft clauses,
and those introduced in the linearization. As they have different meanings, it is con-
venient to consider them separately. Thus, given an assignment    P α, we define its (total)
cost as cost (α) = (cost B (α), cost S (α)), where cost B (α) =     {ω | [b, ω] ∈ B , α 6|= b}
is the bound P  cost, i.e., the contribution to the total  cost due to artificial bounds, and
cost S (α) = {Ω | [D, Ω] ∈ S, α 6|= D} is the soft cost, corresponding to the original soft
clauses. Equivalently, if weights are written as pairs, so that artificial bound clauses
become of the form P [C, (ω, 0)] and soft clauses become of the form [C, (0, Ω)], we can
write cost(α) =       {(ω, Ω) | [C, (ω, Ω)] ∈ S ∪ B , α 6|= C}, where the sum of the pairs
is component-wise. In what follows, pairs (cost B (α), cost S (α)) will be lexicographically
compared, so that the bound cost (which measures the consistency with respect to the
theory of QF-NIA) is more relevant than the soft cost. Hence, by taking this cost func-
tion and this ordering, we have a Max-SMT(QF-LIA) instance in which weights are
not natural or non-negative real numbers, but pairs of them.
   In the following step of the algorithm solve Max SMT QF NIA, the procedure
optimize QF LIA Max SMT threshold (described in Algorithm 13) dispatches this
Max-SMT instance. This procedure is like that presented in Algorithm 8, with the
only difference that now a parameter max soft cost is passed to the Max-SMT(QF-
LIA) solver. This parameter restrains the models of the hard clauses the solver will
consider: only assignments α such that cost S (α) ≤ max soft cost will be taken into ac-
count. That is, this adapted Max-SMT solver computes, among the models α of the hard
clauses such that cost S (α) ≤ max soft cost (if any), one that minimizes cost (α). Thus,
the search can be pruned when it is detected that it is not possible to improve the best
soft cost found so far. This adjustment is not difficult to implement if the Max-SMT
solver follows a branch-and-bound scheme (see Section 3.1), as it is our case.
   Then the algorithm examines the result of the call to the Max-SMT solver. If
it is UNSAT, then there are no models of the hard clauses with soft cost at most
max soft cost . Therefore, the algorithm can stop and report the best solution found
so far, if any.
   Otherwise, M satisfies the hard clauses and has soft cost at most max soft cost . If
it has null bound cost, and hence is a true model of the hard clauses of the original
formula, then the best solution found so far and max soft cost are updated, in order to
search for a solution with better soft cost. Finally, if the bound cost is not null, then

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:24                                                                               Cristina Borralleras et al.

domains are relaxed as described in Section 3.1, in order to widen the search space. In
any case, the algorithm jumps back and a new iteration is performed.
  For the sake of simplicity, Algorithm 12 returns hUNKNOWN, ⊥i when time is ex-
hausted. However, the best model found so far best so far can also be reported, as it
can still be useful in practice.
  The following theorem states the correctness of procedure solve Max SMT QF NIA:

  T HEOREM 4.1. Procedure solve Max SMT QF NIA is correct. That is, given a
weighted formula F0 in QF-NIA with hard clauses H0 and soft clauses S0 :

(1) if solve Max SMT QF NIA(F0 ) returns hSAT, M i then H0 is satisfiable, and M is a
    model of H0 that minimizes the sum of the weights of the falsified clauses in S0 ; and
(2) if solve Max SMT QF NIA(F0 ) returns hUNSAT, ⊥i then H0 is unsatisfiable.

   P ROOF.
   Let us assume that solve Max SMT QF NIA(F0 ) returns hSAT, M i. The assign-
ment M is different from ⊥, and hence has been previously computed in a call to
optimize QF LIA Max SMT threshold(H, S, B, max soft cost ) such that cost B (M ) = 0.
So M respects all artificial bounds in B. Thanks to the case splitting clauses in H, this
ensures that auxiliary variables representing non-linear monomials have the right
values. Therefore M satisfies H0 , which is what we wanted to prove. Now we just need
to check that indeed M minimizes the sum of the weights of the falsified clauses in S0 .
Notice that, from the specification of optimize QF LIA Max SMT threshold, we know
that there is no model of H such that its soft cost is strictly less than cost S (M ). Now
let M ′ be a model of H0 . By extending M ′ so that auxiliary variables representing non-
linear monomials are assigned to their corresponding values, we have M ′ |= H. By the
previous observation, cost S0 (M ′ ) = cost S (M ′ ) ≥ cost S (M ) = cost S0 (M ).
   Now let us assume that solve Max SMT QF NIA(F0 ) returns hUNSAT, ⊥i. Let
us also assume that there exists M ′ a model of H0 , and we will get a con-
tradiction. Indeed, again extending M ′ as necessary, we have that M ′ |=
H. If solve Max SMT QF NIA(F0 ) returns hUNSAT, ⊥i, then the previous call
to optimize QF LIA Max SMT threshold(H, S, B, max soft cost ) has returned
hUNSAT, ⊥i, and moreover no previous call to optimize QF LIA Max SMT threshold
has produced a model with null bound cost. This means that max soft cost has not
changed its initial value, namely ∞. Therefore H must be unsatisfiable, a contradic-
tion.

  Example 4.2. Let F0 be the weighted formula with hard clauses

                        H0 ≡ tx + y ≥ 4 ∧ t2 + x2 + w2 + y 2 ≤ 12

(the same of previous examples) and a single soft clause

                                    S0 ≡ [t2 + x2 + y 2 ≤ 1, 1].

Let us take −1 ≤ t, x, w, y ≤ 1 as artificial bounds. After linearization, we get a
weighted linear formula with hard clauses:

               ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                              A:25
                                                                                                    
                         vtx + y ≥ 4 ∧ vt2 + vx2 + vw2 + vy2 ≤ 12 ∧
                    (t = −1 → vtx = −x)                   ∧
                                                                                                  
                                                                                                   
                    (t = 0 → vtx = 0)                     ∧
                                                                                                  
                                                                                                   
                    (t = 1 → v = x)                       ∧                                       
                               tx                                                                 
                                                                                                  
                                                                                                  
               H ≡  (t = −1 → vt2 = 1)                    ∧     (w = −1 → vw2 = 1)              ∧ 
                   
                                                                                                   
                    (t = 0 → vt2 = 0)                     ∧     (w = 0 → vw2 = 0)               ∧ 
                    (t = 1 → vt2 = 1)                     ∧     (w = 1 → vw2 = 1)               ∧ 
                                                                                                  
                                                                                                  
                                                                                                  
                    (x = −1 → v 2 = 1)                    ∧     (y = −1 → vy2 = 1)              ∧ 
                               x                                                                  
                    (x = 0 → v 2 = 0)                     ∧     (y = 0 → vy2 = 0)               ∧ 
                                x
                     (x = 1 → vx2 = 1)                     ∧     (y = 1 → vy2 = 1)               ∧
and soft clauses
                           S ≡ [vt2 + vx2 + vy2 ≤ 1, (0, 1)]
                                                                                      
                              [−1 ≤ t, (1, 0)]            ∧ [t ≤ 1, (1, 0)] ∧ 
                                [−1 ≤ x, (1, 0)]           ∧ [x ≤ 1, (1, 0)] ∧  ,
                                                                              
                           B≡
                                                                              
                              [−1 ≤ w, (1, 0)]            ∧ [w ≤ 1, (1, 0)] ∧ 
                                [−1 ≤ y, (1, 0)]           ∧ [y ≤ 1, (1, 0)]
where weights are already represented as pairs (bound cost, soft cost) as explained
above.
   In the first call to optimize QF LIA Max SMT threshold(H, S, B, ∞), the optimal
cost is (1, 0). An assignment with this cost that may be returned is, for example, t =
vt2 = 1, x = vtx = 4 and w = vw2 = y = vy2 = vx2 = 0, the same in as Example 3.3. In
this assignment, the only soft clause that is violated is [x ≤ 1, (1, 0)].
   Since the bound cost is not null, new artificial bounds should be introduced. Follow-
ing Example 3.3, the new upper bound for x becomes x ≤ 4. Hence, the soft clause
[x ≤ 1, (1, 0)] is replaced by [x ≤ 4, (1, 0)]), and the following hard clauses are added:
                                               x = 2 → vx2 = 4
                                               x = 3 → vx2 = 9
                                               x = 4 → vx2 = 16
  The following call to optimize QF LIA Max SMT threshold returns an assignment
with cost (0, 1), e.g., t = vt2 = w = vw2 = y = vy2 = 1, x = vtx = 3, 1 and vx2 = 9. Since
the bound cost is null, this assignment is recorded as the best model found so far and
max soft cost is set to 0. This forces that, from now on, only solutions with null soft cost
are considered, i.e., the soft clause vt2 + vx2 + vy2 ≤ 1 must hold. Since t2 + x2 + y 2 ≤ 1
implies |t|, |x|, |y| ≤ 1, which contradicts tx + y ≥ 4, there is actually no solution of
cost (0, 0). Hence next calls to optimize QF LIA Max SMT threshold will unsuccess-
fully look for non-linear models with null soft cost. If additional case splitting clauses
considering values outside the finite domain are introduced, such as for instance
                                             x ≤ −2 → vx2 ≥ 4
                                             x ≥ 5 → vx2 ≥ 25 ,
unsatisfiability will be detected by optimize QF LIA Max SMT threshold. Then proce-
dure solve Max SMT QF NIA will terminate reporting that the minimum cost (with
respect to the original soft clauses S0 ) is 1, and that a model with that cost is given by
t = w = y = 1 and x = 3.                                                                  

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:26                                                                                  Cristina Borralleras et al.

Table VI. Experimental evaluation of Max-SMT(QF-NIA) solvers on benchmark family Integer Transition Systems
(20354 benchmarks).
                    bcl-maxsmt                    bcl-ninc           bcl-ninc-cores                    z3
                  # p.          time       # p.           time      # p.          time          # p.         time
  UNSAT         2,618     32,947.80      2,490       49,351.13    2,573     46,750.26         2,571    624,204.13
   OPT            ¯
                7,644          ¯
                         449,806.47      6,720      174,062.35    6,908    228,974.31             0          0.00
 OPT + SAT        ¯
                8,311         ¯
                         490,204.00      7,390      218,202.00    7,583    276,237.00         2,165    652,295.00
                  ¯           ¯
       Table VII. Experimental evaluation of Max-SMT(QF-NIA) solvers on benchmark family C Integer
       (2019 benchmarks).
                         bcl-maxsmt                bcl-ninc        bcl-ninc-cores                z3
                       # p.       time      # p.          time   # p.         time     # p.          time
         UNSAT         144    9,027.27      121       3,993.28   136      8,930.16     257       7,855.24
          OPT          453    9,090.26      466       9,177.07   469 10,768.57          ¯0           ¯0.00
        OPT + SAT      522    9,108.00      535       9,194.00    ¯
                                                                 539         ¯
                                                                         10,797.00     207      23,579.00
                                                                  ¯          ¯
4.2. Experimental Evaluation
In this section we evaluate experimentally the approach proposed in Section 4.1 for
solving Max-SMT(QF-NIA). We adapt the method to each of the three Max-SMT(QF-
LIA)-based variants for solving SMT(QF-NIA). Thus, following the same names as in
Section 3.5, here we consider the solvers bcl-maxsmt, bcl-ninc and bcl-ninc-cores. We
also include in the experiments z3, which is the only competing tool that, up to our
knowledge, can handle Max-SMT(QF-NIA) too. As regards benchmarks, we use the
original Max-SMT(QF-NIA) versions (that is, keeping soft clauses) of the examples
Integer Transition Systems and C Integer employed in Section 3.5.




   Tables VI and VII show the results of the experiments on the families Integer Transi-
tion Systems and C Integer, respectively. In each table, row UNSAT indicates the num-
ber of instances that were proved to be unsatisfiable, and row OPT counts the instances
for which optimality of the reported model could be established. A third row OPT+ SAT
adds to row OPT the number of problems in which a model was found, but could not
be proved to be optimal. For the sake of succinctness, as in previous tables other out-
comes (timeouts, UNKNOWN answer, etc.) are not made explicit. Columns represent
systems and show either the number of problems that were solved with a certain out-
come, or the total time (in seconds) to process all of them. The best solver in each case
is highlighted in bold face.
   From the tables it can be observed that bcl-ninc-cores is more effective than bcl-
ninc for Max-SMT. This is natural: proving the optimality of the best model found so
far implicitly involves proving unsatisfiability, more precisely that there cannot be a
model with a better cost. And as was already remarked in Section 3.5, optimality cores
help the non-incremental approach to detect unsatisfiability more quickly. Regarding
the incremental approach, the results are inconclusive: depending on the benchmarks,
bcl-maxsmt may perform better than bcl-ninc-cores, or the other way around. Finally,
z3 is competitive or even superior when dealing with unsatisfiable problems, while it
significantly lags behind for the rest of the instances.

5. SOLVING SMT AND MAX-SMT(∃Z ∀R-NIRA)
In this section we will extend our techniques for SMT and Max-SMT(QF-NIA) to the
theory of ∃Z ∀R-NIRA. In this fragment of first-order logic, formulas are of the form
∃x ∀y F (x, y), where F is a quantifier-free formula whose literals are polynomial in-

                  ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                          A:27

equalities. Moreover, the existentially quantified variables have integer type, whereas
the universally quantified ones are real. In particular we will focus on a subset of this
logic, namely, those formulas in which monomials never contain the product of two
universally quantified variables.
  This fragment of quantified non-linear arithmetic is relevant to many applications.
For example, it appears in verification and synthesis problems when the so-called
template-based method [Colón and Sipma 2002] is employed. In this framework, one
attempts to discover an object of interest (e.g., an invariant, or a ranking function) by
introducing a template, usually a linear inequality or expression, and solving a for-
mula that represents the conditions the object should meet. For instance, let us find
an invariant for the next loop:
                                       double y = 0; while (y ≤ 2) y = y+1;

A loop invariant I(y) must satisfy the following initiation and inductiveness conditions:
— Initiation:    ∀y0 (y0 = 0 → I(y0 ))
— Inductiveness: ∀y1 , y2 (I(y1 ) ∧ y1 ≤ 2 ∧ y2 = y1 + 1 → I(y2 ))
  Now a linear template x0 y ≤ x1 is introduced as a candidate for I(y), where x0 , x1
are unknowns and y is the program variable. Then the conditions needed for I(y) to be
an invariant can be expressed in terms of template unknowns and program variables
as an ∃∀ formula:
           ∃x0 , x1 ∀y0 , y1 , y2    (y0 = 0 → x0 y0 ≤ x1 ) ∧                        
                                    (x0 y1 ≤ x1 ∧ y1 ≤ 2 ∧ y2 = y1 + 1 → x0 y2 ≤ x1 )
This falls into the logical fragment considered here. Indeed note that, since the tem-
plate is linear, the non-linear monomials in the formula always consist of the product
of a template unknown and a program variable. Moreover, we can regard that we are
interested in integer coefficients, so the existential variables are integers, while the
universal variables are reals, since the program variable is a double. On the other
hand, if one is interested in finding models with other type patterns, the following can
be taken into account: in general, if a formula
                                           ∃x ∈ Z ∀y ∈ R F (x, y)
is satisfiable, then so are
— ∃x ∈ R ∀y ∈ R F (x, y),
— ∃x ∈ Z ∀y ∈ Z F (x, y),
— ∃x ∈ R ∀y ∈ Z F (x, y),
since the same witness x can be taken.

5.1. Algorithm
Let us first describe how to deal with the satisfiability problem given a formula
∃x ∀y F (x, y), and then the technique will extend to the more general Max-SMT(∃Z ∀R-
NIRA) problem naturally. Note that the requirement that monomials cannot contain
the product of two universal variables allows writing the literals in F as linear poly-
nomials in variables y, i.e., in the form a1 (x) y1 + · · · + an (x) yn ≤ b(x). Hence, if for
instance F is a clause, we can write it as
      m
     ^                                            l
                                                   ^                                         
    ¬   ai1 (x) y1 + · · · + ain (x) yn ≤ bi (x) ∧   cj1 (x) y1 + · · · + cjn (x) yn < dj (x) ,
        i=1                                                   j=1


ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:28                                                                                  Cristina Borralleras et al.
                                                                         
or more compactly using matrix notation as ¬ A(x) y ≤ b(x) ∧ C(x) y < d(x) .
  The key idea (borrowed from [Colón and Sipma 2002]8 ) is to apply the following re-
sult from polyhedral geometry to eliminate the quantifier alternation and transform
the problem into a purely existential one:
  T HEOREM 5.1 (M OTZKIN ’ S T RANSPOSITION T HEOREM [S CHRIJVER 1998]).
Let A ∈ Rm×n , y ∈ Rn , b ∈ Rm , C ∈ Rl×n and d ∈ Rl . The system A(x) y ≤ b(x)
∧ C(x) y < d(x) is unsatisfiable if and only if there are λ ∈ Rm and µ ∈ Rl such that
λ ≥ 0, µ ≥ 0, λT A(x) + µT C(x) = 0, λT b(x) + µT d(x) ≤ 0, and either λT b(x) < 0 or µ 6= 0.
  Thanks to Motzkin’s Transposition Theorem, we have that formulas
                              ∃x ∀y ¬ A(x) y ≤ b(x) ∧ C(x) y < d(x))
and
                                                                                     
∃x ∃λ ∃µ λ, µ ≥ 0 ∧ λT A(x)+µT C(x) = 0 ∧ λT b(x)+µT d(x) ≤ 0 ∧ (λT b(x) < 0 ∨ µ 6= 0)

are equisatisfiable. In general, if the formula F in ∃x ∀y F (x, y) is a CNF, this transfor-
mation is applied locally to each of the clauses with fresh multipliers.
   Note that the formula resulting from applying Motzkin’s Transposition Theorem is
non-linear, but the existentially quantified variables λ and µ have real type. Fortu-
nately, our techniques from Section 3 do not actually require that all variables are
integer: it suffices that there are enough finite domain variables to perform the lin-
earization. And this is indeed the case, since every non-linear monomial of the trans-
formed formula has at most one occurrence of a λ or a µ variable, and all other variables
are integer. All in all, we have reduced the problem of satisfiability of the fragment of
∃Z ∀R-NIRA under consideration to satisfiability of non-linear formulas that our ap-
proach can deal with.
   Finally, regarding Max-SMT the technique extends clause-wise in a natural way.
Given a weighted CNF, hard clauses are transformed using Motzkin’s Transposition
Theorem as in the SMT case. As for soft clauses, let [S, Ω] be such a clause, where S is
of the form ¬(A(x) y ≤ b(x) ∧ C(x) y < d(x)). Then a fresh propositional symbol pS is
introduced, and [S, Ω] is replaced by a soft clause [pS , Ω] and hard clauses corresponding
to the double implication
                                                                                   
 λ, µ ≥ 0 ∧ λT A(x)+ µT C(x) = 0 ∧ λT b(x)+ µT d(x) ≤ 0 ∧ (λT b(x) < 0 ∨ µ 6= 0) ↔ pS .

Therefore, similarly to satisfiability, we can solve the Max-SMT problem for the frag-
ment of ∃Z ∀R-NIRA of interest by reducing it to instances that can be handled with
the techniques presented in Section 4.
   Example 5.2. Let us consider again the problem of finding an invariant for the
loop:
                                     double y = 0; while (y ≤ 2) y = y+1;

  However, now we will make the initiation condition soft, say with weight 1, while
the inductiveness condition will remain hard (as done in [Brockschmidt et al. 2015]).
The rationale is that, if the initiation condition can be satisfied, then we have a true
invariant; and if it is not, then at least we have a conditional invariant: a property
that, if at some iteration holds, then from that iteration on it always holds.

8 In [Colón and Sipma 2002], Farkas’ Lemma is used instead of the generalization presented here.




                  ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                          A:29

  Using the same template as above, the formula to be solved is (quantifiers are omit-
ted for the sake of presentation):
                        [y0 = 0 → x0 y0 ≤ x1 , 1] ∧
                        (x0 y1 ≤ x1 ∧ y1 ≤ 2 ∧ y2 = y1 + 1 → x0 y2 ≤ x1 )
After moving the right-hand side of the implication to the left, and applying some
simplifications, it results into:
                              [0 ≤ x1 , 1] ∧
                              ¬(x0 y1 ≤ x1 ∧ y1 ≤ 2 ∧ x0 (y1 + 1) > x1 )
Now the transformation is performed clause by clause. Since the first clause [0 ≤ x1 , 1]
does no longer contain universally quantified variables, it can be left as it is. As regards
the second one, we introduce three fresh multipliers λ1 , λ2 , and µ and replace
                              ¬(x0 y1 ≤ x1 ∧ y1 ≤ 2 ∧ x0 (y1 + 1) > x1 )
by
                         
                             λ1 ≥ 0 ∧ λ2 ≥ 0 ∧ µ ≥ 0 ∧ λ1 x0 + λ2 − µx0 = 0 ∧
                                                                               
                     λ1 x1 + 2λ2 + µ(x0 − x1 ) ≤ 0 ∧ (λ1 x1 + 2λ2 < 0 ∨ µ 6= 0)

All in all, the following Max-SMT instance must be solved:
                                                  [0 ≤ x1 , 1] ∧
                         
                             λ1 ≥ 0 ∧ λ2 ≥ 0 ∧ µ ≥ 0 ∧ λ1 x0 + λ2 − µx0 = 0 ∧
                                                                               
                     λ1 x1 + 2λ2 + µ(x0 − x1 ) ≤ 0 ∧ (λ1 x1 + 2λ2 < 0 ∨ µ 6= 0)

There exist many solutions with cost 0, each of them corresponding to a loop invariant;
for instance, x0 = 1, x1 = 3, λ1 = 0, λ2 = 1, µ = 1 (which represents the invariant y ≤ 3).

5.2. Experimental Evaluation
In this section we evaluate experimentally the approach proposed in Section 5.1 for
solving Max-SMT(∃Z ∀R-NIRA). Similarly to Section 4.2, again we instantiate the
method for the three Max-SMT(QF-LIA)-based variants for solving SMT(QF-NIA). So,
using the same names as in Sections 3.5 and 4.2, in this evaluation we consider the
solvers bcl-maxsmt, bcl-ninc and bcl-ninc-cores. Unfortunately, as far as we know no
competing tool can handle the problems of Max-SMT(∃Z ∀R-NIRA) effectively. Hence,
we have to limit our experiments to our own tools.
  Regarding benchmarks, again we use the weighted formulas of the families Integer
Transition Systems and C Integer, employed in Section 4.2. However, here problems are
expressed in Max-SMT(∃Z ∀R-NIRA) rather than in Max-SMT(NIA); that is, Motzkin’s
Transposition Theorem is applied silently inside the solver, and not in the process of
generating the instances. Moreover, as illustrated in Example 5.2, Max-SMT(∃Z ∀R-
NIRA) problems coming from the application of the template-based method can usually
be simplified, e.g., by using equations to eliminate variables. In order to introduce some
variation with respect to the evaluation in Section 4.2, we decided to experiment with
the Max-SMT(∃Z ∀R-NIRA) problems in raw form, without simplifications. Another
difference is that, while in Section 4.2 multipliers were considered integer variables
(so that purely integer problems were obtained), in this evaluation they have real type.



ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:30                                                                                Cristina Borralleras et al.

        Table VIII. Experimental evaluation of Max-SMT(∃Z ∀R-NIRA) solvers on benchmark family
        Integer Transition Systems (20354 benchmarks).
                              bcl-maxsmt                     bcl-ninc            bcl-ninc-cores
                           # p.            time       # p.           time       # p.          time
          UNSAT          2,196       89,259.58      2,119      121,556.46     2,031     140,585.27
           OPT             ¯
                         6,707            ¯
                                  1,002,816.92      5,902      405,813.78     5,856     401,333.33
         OPT + SAT         ¯
                         7,337          ¯
                                  1,071,480.43      6,536      475,622.68     6,485     467,898.84
                           ¯            ¯
             Table IX. Experimental evaluation of Max-SMT(∃Z ∀R-NIRA) solvers on bench-
             mark family C Integer (2019 benchmarks).
                                  bcl-maxsmt                bcl-ninc         bcl-ninc-cores
                               # p.        time      # p.           time    # p.         time
               UNSAT            88    10,095.79       64        1,992.78     76     2,545.89
                OPT              ¯
                               360        ¯
                                      11,928.57      374      13,223.96     379 15,173.59
              OPT + SAT        429    13,985.45      442      13,811.42      ¯
                                                                            447         ¯
                                                                                   15,818.40
                                                                             ¯          ¯


   Results are shown in Tables VIII and IX, following the same format as in Section 4.2.
It is worth noticing that the number of solved instances is significantly smaller than
in Tables VI and VII, respectively. This shows the usefulness of the simplifications
performed when generating the Max-SMT(NIA) instances. Regarding which tool for
Max-SMT(∃Z ∀R-NIRA) among the three is the most powerful, on SAT instances there
is not a global winner, while on unsatisfiable ones bcl-maxsmt has the best results for
both families.
6. CONCLUSIONS AND FUTURE WORK
In this article we have proposed two strategies to guide domain relaxation in the
instantiation-based approach for solving SMT(QF-NIA) [Borralleras et al. 2012]. Both
are based on computing minimal models with respect to a cost function, namely: the
number of violated artificial domain bounds, and the distance with respect to the artifi-
cial domains. We have experimentally argued that the former gives better results than
the latter and previous techniques, and have devised further improvements, based on
weakening the invariant that artificial domains should grow monotonically, and ex-
ploiting optimality cores. Finally, we have developed and implemented algorithms for
Max-SMT(QF-NIA) and for Max-SMT(∃Z ∀R-NIRA), logical fragments with important
applications to program analysis and termination but which are missing effective tools.
  As for future work, several directions for further research can be considered. Re-
garding the algorithmics, it would be interesting to look into different cost functions
following the model-guided framework proposed here, as well as alternative ways
for computing those minimal models (e.g., by means of minimal correction subsets
[Marques-Silva et al. 2013; Bjørner and Narodytska 2015]). On the other hand, one of
the shortcomings of our instantiation-based approach for solving Max-SMT/SMT(QF-
NIA) is that unsatisfiable instances that require non-trivial non-linear reasoning can-
not be captured. In this context, the integration of real-goaled CAD techniques adapted
to SMT [Jovanovic and de Moura 2012] as a fallback or run in parallel appears to be a
promising line of work.
  Another direction for future research concerns applications. So far we
have applied Max-SMT/SMT(QF-NIA/∃Z ∀R-NIRA) to array invariant gen-
eration    [Larraz et al. 2013],    safety    [Brockschmidt et al. 2015],   termination
[Larraz et al. 2013] and non-termination [Larraz et al. 2014] proving. Other problems
in program analysis where we envision these techniques could help in improving
the state-of-the-art are, e.g., the analysis of worst-case execution time and resource
analysis. Also, so far we have only considered sequential programs. The extension of

                ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                          A:31

Max-SMT-based techniques to concurrent programs is a promising line of work with a
potentially high impact in the industry.

ACKNOWLEDGMENTS
The authors would like to thank the anonymous referees of the conference version of this paper for their
helpful comments.


REFERENCES
Carlos Ansótegui, Maria Luisa Bonet, and Jordi Levy. 2013. SAT-based MaxSAT algorithms. Artif. Intell.
    196 (2013), 77–105. DOI:http://dx.doi.org/10.1016/j.artint.2013.01.002
Roberto Ası́n Achá, Robert Nieuwenhuis, Albert Oliveras, and Enric Rodrı́guez-Carbonell. 2010. Practical
    algorithms for unsatisfiability proof and core generation in SAT solvers. AI Communications 23, 2-3
    (2010), 145–157.
Clark Barrett, Christopher L. Conway, Morgan Deters, Liana Hadarean, Dejan Jovanovic, Tim King,
    Andrew Reynolds, and Cesare Tinelli. 2011. CVC4. In Computer Aided Verification - 23rd Interna-
    tional Conference, CAV 2011, Snowbird, UT, USA, July 14-20, 2011. Proceedings (Lecture Notes in
    Computer Science), Ganesh Gopalakrishnan and Shaz Qadeer (Eds.), Vol. 6806. Springer, 171–177.
    DOI:http://dx.doi.org/10.1007/978-3-642-22110-1 14
Clark Barrett, Pascal Fontaine, and Cesare Tinelli. 2016. The Satisfiability Modulo Theories Library (SMT-
    LIB). www.SMT-LIB.org. (2016).
S. Basu, R. Pollack, and M.-F. Roy. 2003. Algorithms in Real Algebraic Geometry. Springer-Verlag, Berlin.
Anton Belov, Inês Lynce, and João Marques-Silva. 2012. Towards efficient MUS extraction. AI Commun. 25,
    2 (2012), 97–116.
Rachel Ben-Eliyahu and Rina Dechter. 1996. On Computing Minimal Models. Ann. Math. Artif. Intell. 18, 1
    (1996), 3–27. DOI:http://dx.doi.org/10.1007/BF02136172
Rachel Ben-Eliyahu-Zohary. 2005. An incremental algorithm for generating all minimal models. Artif. Intell.
    169, 1 (2005), 1–22. DOI:http://dx.doi.org/10.1016/j.artint.2005.06.003
Tewodros Beyene, Swarat Chaudhuri, Corneliu Popeea, and Andrey Rybalchenko. 2014. A Constraint-based
    Approach to Solving Games on Infinite Graphs. In Proceedings of the 41st ACM SIGPLAN-SIGACT
    Symposium on Principles of Programming Languages (POPL ’14). ACM, New York, NY, USA, 221–233.
    DOI:http://dx.doi.org/10.1145/2535838.2535860
Armin Biere, Marijn J. H. Heule, Hans van Maaren, and Toby Walsh (Eds.). 2009. Handbook of Satisfiability.
    Frontiers in Artificial Intelligence and Applications, Vol. 185. IOS Press. 980 pages.
Nikolaj Bjørner and Nina Narodytska. 2015. Maximum Satisfiability Using Cores and Correction Sets. In
    Proceedings of the Twenty-Fourth International Joint Conference on Artificial Intelligence, IJCAI 2015,
    Buenos Aires, Argentina, July 25-31, 2015, Qiang Yang and Michael Wooldridge (Eds.). AAAI Press,
    246–252. http://ijcai.org/Abstract/15/041
Nikolaj Bjørner, Anh-Dung Phan, and Lars Fleckenstein. 2015. νZ - An Optimizing SMT Solver. In Tools
    and Algorithms for the Construction and Analysis of Systems - 21st International Conference, TACAS
    2015, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS 2015,
    London, UK, April 11-18, 2015. Proceedings (Lecture Notes in Computer Science), Christel Baier and
    Cesare Tinelli (Eds.), Vol. 9035. Springer, 194–199. DOI:http://dx.doi.org/10.1007/978-3-662-46681-0 14
Roderick Bloem and Natasha Sharygina (Eds.). 2010. Proceedings of 10th International Conference on For-
    mal Methods in Computer-Aided Design, FMCAD 2010, Lugano, Switzerland, October 20-23. IEEE.
Maria Paola Bonacina (Ed.). 2013. Automated Deduction - CADE-24 - 24th International Conference on
    Automated Deduction, Lake Placid, NY, USA, June 9-14, 2013. Proceedings. Lecture Notes in Computer
    Science, Vol. 7898. Springer. DOI:http://dx.doi.org/10.1007/978-3-642-38574-2
Cristina Borralleras, Salvador Lucas, Albert Oliveras, Enric Rodrı́guez-Carbonell, and Albert Rubio. 2012.
    SAT Modulo Linear Arithmetic for Solving Polynomial Constraints. J. Autom. Reasoning 48, 1 (2012),
    107–131.
Marc Brockschmidt, Daniel Larraz, Albert Oliveras, Enric Rodrı́guez-Carbonell, and Albert Rubio. 2015.
    Compositional Safety Verification with Max-SMT. In Formal Methods in Computer-Aided Design, FM-
    CAD 2015, Austin, Texas, USA, September 27-30, 2015., Roope Kaivola and Thomas Wahl (Eds.). IEEE,
    33–40.
Chih-Hong Cheng, Natarajan Shankar, Harald Ruess, and Saddek Bensalem. 2013. EFSMT: A Logical
    Framework for Cyber-Physical Systems. CoRR abs/1306.3456 (2013). http://arxiv.org/abs/1306.3456


ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:32                                                                                  Cristina Borralleras et al.

Alessandro Cimatti, Anders Franzén, Alberto Griggio, Roberto Sebastiani, and Cristian Stenico. 2010. Sat-
    isfiability Modulo the Theory of Costs: Foundations and Applications. In TACAS (Lecture Notes in Com-
    puter Science), Javier Esparza and Rupak Majumdar (Eds.), Vol. 6015. Springer, 99–113.
George E. Collins. 1975. Hauptvortrag: Quantifier elimination for real closed fields by cylindrical alge-
    braic decomposition. In Automata Theory and Formal Languages (Lecture Notes in Computer Science),
    H. Barkhage (Ed.), Vol. 33. Springer, 134–183.
Michael Colón, Sriram Sankaranarayanan, and Henny Sipma. 2003. Linear Invariant Generation Using
    Non-linear Constraint Solving. In CAV (Lecture Notes in Computer Science), Warren A. Hunt Jr. and
    Fabio Somenzi (Eds.), Vol. 2725. Springer, 420–432.
Michael Colón and Henny Sipma. 2002. Practical Methods for Proving Program Termination. In CAV (Lec-
    ture Notes in Computer Science), Ed Brinksma and Kim Guldstrand Larsen (Eds.), Vol. 2404. Springer,
    442–454.
S. Barry Cooper. 2004. Computability Theory. Chapman Hall/CRC Mathematics Series.
Florian Corzilius and Erika Ábrahám. 2011. Virtual Substitution for SMT-Solving. In Fundamentals of
    Computation Theory - 18th International Symposium, FCT 2011, Oslo, Norway, August 22-25, 2011.
    Proceedings (Lecture Notes in Computer Science), Olaf Owe, Martin Steffen, and Jan Arne Telle (Eds.),
    Vol. 6914. Springer, 360–371. DOI:http://dx.doi.org/10.1007/978-3-642-22953-4 31
Florian Corzilius, Gereon Kremer, Sebastian Junges, Stefan Schupp, and Erika Ábrahám. 2015. SMT-RAT:
    An Open Source C++ Toolbox for Strategic and Parallel SMT Solving. In Theory and Applications of
    Satisfiability Testing - SAT 2015 - 18th International Conference, Austin, TX, USA, September 24-27,
    2015, Proceedings (Lecture Notes in Computer Science), Marijn Heule and Sean Weaver (Eds.), Vol.
    9340. Springer, 360–368. DOI:http://dx.doi.org/10.1007/978-3-319-24318-4 26
Florian Corzilius, Ulrich Loup, Sebastian Junges, and Erika Ábrahám. 2012. SMT-RAT: An SMT-Compliant
     Nonlinear Real Arithmetic Toolbox - (Tool Presentation). In SAT (Lecture Notes in Computer Science),
     Alessandro Cimatti and Roberto Sebastiani (Eds.), Vol. 7317. Springer, 442–448.
Leonardo Mendonça de Moura and Nikolaj Bjørner. 2008a. Model-based Theory Combination. Electr. Notes
     Theor. Comput. Sci. 198, 2 (2008), 37–49. DOI:http://dx.doi.org/10.1016/j.entcs.2008.04.079
Leonardo Mendonça de Moura and Nikolaj Bjørner. 2008b. Z3: An Efficient SMT Solver. In TACAS (Lecture
     Notes in Computer Science), C. R. Ramakrishnan and Jakob Rehof (Eds.), Vol. 4963. Springer, 337–340.
Leonardo Mendonça de Moura and Dejan Jovanovic. 2013. A Model-Constructing Satisfiability Calculus. In
     VMCAI (Lecture Notes in Computer Science), Roberto Giacobazzi, Josh Berdine, and Isabella Mastroeni
     (Eds.), Vol. 7737. Springer, 1–12.
Leonardo Mendonça de Moura and Grant Olney Passmore. 2013. Computation in Real Closed
     Infinitesimal and Transcendental Extensions of the Rationals, See Bonacina [2013], 178–192.
     DOI:http://dx.doi.org/10.1007/978-3-642-38574-2
Isil Dillig, Thomas Dillig, and Alex Aiken. 2011. Cuts from proofs: a complete and practical technique
     for solving linear inequalities over integers. Formal Methods in System Design 39, 3 (2011), 246–260.
     DOI:http://dx.doi.org/10.1007/s10703-011-0127-z
Bruno Dutertre. 2014. Yices 2.2. In Computer-Aided Verification (CAV’2014) (Lecture Notes in Computer
     Science), Armin Biere and Roderick Bloem (Eds.), Vol. 8559. Springer, 737–744.
Bruno Dutertre. 2015. Solving Exists/Forall Problems With Yices. In 13th International Workshop on Satis-
     fiability Modulo Theories (SMT 2015).
Bruno Dutertre and Leonardo Mendonça de Moura. 2006. A Fast Linear-Arithmetic Solver for DPLL(T). In
     CAV (Lecture Notes in Computer Science), Thomas Ball and Robert B. Jones (Eds.), Vol. 4144. Springer,
     81–94.
Martin Fränzle, Christian Herde, Tino Teige, Stefan Ratschan, and Tobias Schubert. 2007. Efficient Solv-
     ing of Large Non-linear Arithmetic Constraint Systems with Complex Boolean Structure. JSAT 1, 3-4
     (2007), 209–236.
Zhaohui Fu and Sharad Malik. 2006. On Solving the Partial MAX-SAT Problem. In SAT. 252–265.
Carsten Fuhs, Jürgen Giesl, Aart Middeldorp, Peter Schneider-Kamp, René Thiemann, and Harald Zankl.
     2007. SAT Solving for Termination Analysis with Polynomial Interpretations. In SAT (Lecture Notes in
     Computer Science), João Marques-Silva and Karem A. Sakallah (Eds.), Vol. 4501. Springer, 340–354.
Malay K. Ganai and Franjo Ivancic. 2009. Efficient decision procedure for non-linear arithmetic constraints
     using CORDIC. In FMCAD. IEEE, 61–68.
Sicun Gao, Jeremy Avigad, and Edmund M. Clarke. 2012. δ-Complete Decision Procedures for Satisfiability
     over the Reals. In IJCAR (Lecture Notes in Computer Science), Bernhard Gramlich, Dale Miller, and Uli
     Sattler (Eds.), Vol. 7364. Springer, 286–300.




                  ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                           A:33

Sicun Gao, Malay K. Ganai, Franjo Ivancic, Aarti Gupta, Sriram Sankaranarayanan, and Edmund M.
    Clarke. 2010. Integrating ICP and LRA solvers for deciding nonlinear real arithmetic problems, See
    Bloem and Sharygina [2010], 81–89.
Sicun Gao, Soonho Kong, and Edmund M. Clarke. 2013. dReal: An SMT Solver for Nonlinear Theories over
    the Reals, See Bonacina [2013], 208–214. DOI:http://dx.doi.org/10.1007/978-3-642-38574-2 14
Adria Gascón, Pramod Subramanyan, Bruno Dutertre, Ashish Tiwari, Dejan Jovanovic, and
    Sharad Malik. 2014. Template-based circuit understanding. In Formal Methods in Computer-
    Aided Design, FMCAD 2014, Lausanne, Switzerland, October 21-24, 2014. IEEE, 83–90.
    DOI:http://dx.doi.org/10.1109/FMCAD.2014.6987599
Alberto Griggio. 2012. A Practical Approach to Satisability Modulo Linear Integer Arithmetic. JSAT 8, 1/2
    (2012), 1–27. http://jsat.ewi.tudelft.nl/content/volume8/JSAT8 1 Griggio.pdf
Dejan Jovanovic and Leonardo Mendonça de Moura. 2012. Solving Non-linear Arithmetic. In IJCAR (Lecture
    Notes in Computer Science), Bernhard Gramlich, Dale Miller, and Uli Sattler (Eds.), Vol. 7364. Springer,
    339–354.
Sebastian Junges, Ulrich Loup, Florian Corzilius, and Erika Ábrahám. 2013. On Gröbner Bases in the
    Context of Satisfiability-Modulo-Theories Solving over the Real Numbers. In Algebraic Informatics -
    5th International Conference, CAI 2013, Porquerolles, France, September 3-6, 2013. Proceedings (Lecture
    Notes in Computer Science), Traian Muntean, Dimitrios Poulakis, and Robert Rolland (Eds.), Vol. 8080.
    Springer, 186–198. DOI:http://dx.doi.org/10.1007/978-3-642-40663-8 18
To Van Khanh and Mizuhito Ogawa. 2012. SMT for Polynomial Constraints on Real Numbers. Electr. Notes
    Theor. Comput. Sci. 289 (2012), 27–40.
Sebastian Krings, Jens Bendisposto, and Michael Leuschel. 2015. From Failure to Proof: The ProB
    Disprover for B and Event-B. In Software Engineering and Formal Methods - 13th Interna-
    tional Conference, SEFM 2015, York, UK, September 7-11, 2015. Proceedings (Lecture Notes in
    Computer Science), Radu Calinescu and Bernhard Rumpe (Eds.), Vol. 9276. Springer, 199–214.
    DOI:http://dx.doi.org/10.1007/978-3-319-22969-0 15
Daniel Larraz, Kaustubh Nimkar, Albert Oliveras, Enric Rodrı́guez-Carbonell, and Albert Rubio. 2014.
    Proving Non-termination Using Max-SMT. In Computer Aided Verification - 26th International Con-
    ference, CAV 2014, Held as Part of the Vienna Summer of Logic, VSL 2014, Vienna, Austria, July 18-22,
    2014. Proceedings (Lecture Notes in Computer Science), Armin Biere and Roderick Bloem (Eds.), Vol.
    8559. Springer, 779–796. DOI:http://dx.doi.org/10.1007/978-3-319-08867-9 52
Daniel Larraz, Albert Oliveras, Enric Rodrı́guez-Carbonell, and Albert Rubio. 2013. Proving termination of
    imperative programs using Max-SMT. In FMCAD. IEEE, 218–225.
Daniel Larraz, Albert Oliveras, Enric Rodrı́guez-Carbonell, and Albert Rubio. 2014. Minimal-Model-
    Guided Approaches to Solving Polynomial Constraints and Extensions. In Theory and Applica-
    tions of Satisfiability Testing - SAT 2014 - 17th International Conference, Held as Part of the
    Vienna Summer of Logic, VSL 2014, Vienna, Austria, July 14-17, 2014. Proceedings (Lecture
    Notes in Computer Science), Carsten Sinz and Uwe Egly (Eds.), Vol. 8561. Springer, 333–350.
    DOI:http://dx.doi.org/10.1007/978-3-319-09284-3 25
Daniel Larraz, Enric Rodrı́guez-Carbonell, and Albert Rubio. 2013. SMT-Based Array Invariant Genera-
    tion. In VMCAI (Lecture Notes in Computer Science), Roberto Giacobazzi, Josh Berdine, and Isabella
    Mastroeni (Eds.), Vol. 7737. Springer, 169–188.
Javier Larrosa, Robert Nieuwenhuis, Albert Oliveras, and Enric Rodrı́guez-Carbonell. 2011. A Frame-
    work for Certified Boolean Branch-and-Bound Optimization. J. Autom. Reasoning 46, 1 (2011), 81–102.
    DOI:http://dx.doi.org/10.1007/s10817-010-9176-z
Chu Min Li and Felip Manyà. 2009. MaxSAT, Hard and Soft Constraints. In Handbook of
    Satisfiability, Armin Biere, Marijn Heule, Hans van Maaren, and Toby Walsh (Eds.).
    Frontiers in Artificial Intelligence and Applications, Vol. 185. IOS Press, 613–631.
    DOI:http://dx.doi.org/10.3233/978-1-58603-929-5-613
Yi Li, Aws Albarghouthi, Zachary Kincaid, Arie Gurfinkel, and Marsha Chechik. 2014. Symbolic optimiza-
    tion with SMT solvers. In The 41st Annual ACM SIGPLAN-SIGACT Symposium on Principles of Pro-
    gramming Languages, POPL ’14, San Diego, CA, USA, January 20-21, 2014, Suresh Jagannathan and
    Peter Sewell (Eds.). ACM, 607–618. DOI:http://dx.doi.org/10.1145/2535838.2535857
Alexandre Maréchal, Alexis Fouilhé, Tim King, David Monniaux, and Michaël Périn. 2016. Polyhedral Ap-
    proximation of Multivariate Polynomials Using Handelman’s Theorem. In Verification, Model Check-
    ing, and Abstract Interpretation - 17th International Conference, VMCAI 2016, St. Petersburg, FL, USA,
    January 17-19, 2016. Proceedings (Lecture Notes in Computer Science), Barbara Jobstmann and K. Rus-
    tan M. Leino (Eds.), Vol. 9583. Springer, 166–184. DOI:http://dx.doi.org/10.1007/978-3-662-49122-5 8




ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
A:34                                                                                  Cristina Borralleras et al.

João Marques-Silva, Federico Heras, Mikolás Janota, Alessandro Previti, and Anton Belov. 2013. On Com-
     puting Minimal Correction Subsets. In IJCAI 2013, Proceedings of the 23rd International Joint Con-
     ference on Artificial Intelligence, Beijing, China, August 3-9, 2013, Francesca Rossi (Ed.). IJCAI/AAAI.
     http://www.aaai.org/ocs/index.php/IJCAI/IJCAI13/paper/view/6922
António Morgado, Federico Heras, Mark H. Liffiton, Jordi Planes, and João Marques-Silva. 2013. Itera-
     tive and core-guided MaxSAT solving: A survey and assessment. Constraints 18, 4 (2013), 478–534.
     DOI:http://dx.doi.org/10.1007/s10601-013-9146-2
Robert Nieuwenhuis and Albert Oliveras. 2006. On SAT Modulo Theories and Optimization Problems. In
     SAT (Lecture Notes in Computer Science), Armin Biere and Carla P. Gomes (Eds.), Vol. 4121. Springer,
     156–169.
Robert Nieuwenhuis, Albert Oliveras, and Cesare Tinelli. 2006. Solving SAT and SAT Modulo Theories:
     from an Abstract Davis-Putnam-Logemann-Loveland Procedure to DPLL(T). J. ACM 53, 6 (Nov. 2006),
     937–977.
Pierluigi Nuzzo, Alberto Puggelli, Sanjit A. Seshia, and Alberto L. Sangiovanni-Vincentelli. 2010. CalCS:
     SMT solving for non-linear convex constraints, See Bloem and Sharygina [2010], 71–79.
Roc Oliver. 2012. Optimization Modulo Theories. Master’s thesis. Universitat Politècnica de Catalunya,
     Spain. (January 2012).
Grant Olney Passmore, Leonardo Mendonça de Moura, and Paul B. Jackson. 2010. Gröbner Basis Con-
     struction Algorithms Based on Theorem Proving Saturation Loops. In Decision Procedures in Soft-
     ware, Hardware and Bioware, 18.04. - 23.04.2010 (Dagstuhl Seminar Proceedings), Nikolaj Bjørner,
     Robert Nieuwenhuis, Helmut Veith, and Andrei Voronkov (Eds.), Vol. 10161. Schloss Dagstuhl - Leibniz-
     Zentrum für Informatik, Germany. http://drops.dagstuhl.de/opus/volltexte/2010/2734/
André Platzer, Jan-David Quesel, and Philipp Rümmer. 2009. Real World Verification. In CADE (Lecture
     Notes in Computer Science), Renate A. Schmidt (Ed.), Vol. 5663. Springer, 485–501.
Sriram Sankaranarayanan, Henny Sipma, and Zohar Manna. 2004. Non-linear loop invariant generation
     using Gröbner bases. In POPL, Neil D. Jones and Xavier Leroy (Eds.). ACM, 318–329.
Sriram Sankaranarayanan, Henny B. Sipma, and Zohar Manna. 2008. Constructing invariants for hybrid
     systems. Formal Methods in System Design 32, 1 (2008), 25–55.
Alexander       Schrijver.    1998.      Theory    of    Linear    and     Integer   Programming.       Wiley.
     http://www.amazon.com/exec/obidos/redirect?tag=citeulike07-20&path=ASIN/0471982326
Roberto Sebastiani and Silvia Tomasi. 2015. Optimization Modulo Theories with Linear Rational Costs.
     ACM Trans. Comput. Log. 16, 2 (2015), 12:1–12:43. DOI:http://dx.doi.org/10.1145/2699915
Roberto Sebastiani and Patrick Trentin. 2015. OptiMathSAT: A Tool for Optimization Modulo Theories. In
     Computer Aided Verification - 27th International Conference, CAV 2015, San Francisco, CA, USA, July
     18-24, 2015, Proceedings, Part I (Lecture Notes in Computer Science), Daniel Kroening and Corina S.
     Pasareanu (Eds.), Vol. 9206. Springer, 447–454. DOI:http://dx.doi.org/10.1007/978-3-319-21690-4 27
Takehide Soh and Katsumi Inoue. 2010. Identifying Necessary Reactions in Metabolic Pathways by
     Minimal Model Generation. In ECAI 2010 - 19th European Conference on Artificial Intelligence,
     Lisbon, Portugal, August 16-20, 2010, Proceedings (Frontiers in Artificial Intelligence and Applica-
     tions), Helder Coelho, Rudi Studer, and Michael Wooldridge (Eds.), Vol. 215. IOS Press, 277–282.
     http://www.booksonline.iospress.nl/Content/View.aspx?piid=17757
Aaron Stump, Geoff Sutcliffe, and Cesare Tinelli. 2014. StarExec: a cross-community infrastructure for logic
     solving. In IJCAR.
Alfred Tarski. 1951. A decision method for elementary algebra and geometry. Bull. Amer. Math. Soc. 59
     (1951).
Termination Competition. (????). http://termination-portal.org/wiki/Termination Competition.
Ashish Tiwari, Adria Gascón, and Bruno Dutertre. 2015. Program Synthesis Using Dual Interpretation.
     In Automated Deduction - CADE-25 - 25th International Conference on Automated Deduction, Berlin,
     Germany, August 1-7, 2015, Proceedings (Lecture Notes in Computer Science), Amy P. Felty and Aart
     Middeldorp (Eds.), Vol. 9195. Springer, 482–497. DOI:http://dx.doi.org/10.1007/978-3-319-21401-6 33
Vu Xuan Tung, To Van Khanh, and Mizuhito Ogawa. 2016. raSAT: An SMT Solver for Polynomial Con-
     straints. In Automated Reasoning - 8th International Joint Conference, IJCAR 2016, Coimbra, Portugal,
     June 27 - July 2, 2016, Proceedings (Lecture Notes in Computer Science), Nicola Olivetti and Ashish
     Tiwari (Eds.), Vol. 9706. Springer, 228–237. DOI:http://dx.doi.org/10.1007/978-3-319-40229-1 16
Harald Zankl and Aart Middeldorp. 2010. Satisfiability of Non-linear (Ir)rational Arithmetic. In LPAR
     (Dakar) (Lecture Notes in Computer Science), Edmund M. Clarke and Andrei Voronkov (Eds.), Vol. 6355.
     Springer, 481–500.




                  ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
Incomplete SMT Techniques for Solving Non-Linear Formulas over the Integers                          A:35

Lintao Zhang and Sharad Malik. 2003. Validating SAT Solvers Using an Independent Resolution-Based
    Checker: Practical Implementations and Other Applications. 2008 Design, Automation and Test in Eu-
    rope 1 (2003), 10880.




ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: January YYYY.
