                                             Improving NLSAT for Nonlinear Real Arithmetic
                                                                                                           Zhonghan Wang∗†
                                                                 ∗ Key Laboratory of System Software (Chinese Academy of Sciences) and State Key

                                                       Laboratory of Computer Science, Institute of Software, Chinese Academy of Sciences, Beijing, China
                                                                         † University of Chinese Academy of Sciences, Beijing, China

                                                                              wangzh@ios.ac.cn, wangzhonghan272@gmail.com




                                            Abstract—The Model-Constructing Satisfiability Calculus                      applications are collected in the SMT-LIB benchmarks [19].
                                         (MCSAT) framework has been applied to SMT problems over                         The high performance of SMT solvers over nonlinear arith-
                                         various arithmetic theories. NLSAT, an implementation us-                       metic has significantly improved these applications.
arXiv:2406.02122v4 [cs.SC] 26 Sep 2025




                                         ing cylindrical algebraic decomposition (CAD) for explanation,
                                         is especially competitive for nonlinear real arithmetic (NRA)                      Decision procedures for solving nonlinear arithmetic are
                                         constraints. However, current Conflict-Driven Clause Learning                   usually based on cylindrical algebraic decomposition (CAD)
                                         (CDCL)-style algorithms only consider literal information when                  [20], a widely used tool for real quantifier elimination. CAD
                                         making decisions, and thus ignore the influence of clauses                      generates the current unsatisfiable cell during the search pro-
                                         on arithmetic variables. This limitation may lead NLSAT to                      cedure and is employed in modern algorithms. Among these,
                                         encounter unnecessary conflicts due to suboptimal literal choices.
                                         To address this issue, we analyze conflicts caused by literal                   NLSAT [21] is a mainstream algorithm that leverages CAD
                                         decisions and incorporate clause-level information that directly                for lemma generation. Its core idea is to assign values directly
                                         affects arithmetic variables. We propose two main algorithmic                   to arithmetic variables, rather than at the literal level as in
                                         improvements: a clause-level feasible-set-based look-ahead mech-                CDCL(T).
                                         anism and an arithmetic propagation-based branching heuristic.                     Although NLSAT introduces the novel approach of directly
                                         We implement our solver, named clauseSMT, based on a dy-
                                         namic variable ordering framework. Experiments indicate that                    assigning arithmetic variables, it still relies on literal deci-
                                         clauseSMT is competitive on nonlinear real arithmetic problems                  sions when processing arithmetic clauses containing several
                                         compared with existing SMT solvers (CVC5, Z3, YICES2),                          unevaluated literals. These decided literals are then used for
                                         and it outperforms all of them on satisfiable instances of                      conflict analysis within the CDCL-style framework. However,
                                         SMT(QF NRA) in SMT-LIB. We also evaluate the effectiveness                      improper literal decisions can sometimes induce conflicts,
                                         of our proposed methods.
                                            Index Terms—NLSAT, nonlinear real arithmetic, SMT, clause                    slowing down the overall search process. Therefore, a heuristic
                                         level.                                                                          for literal decisions is necessary.
                                                                                                                            We identify three central problems and present our solutions
                                                                   I. I NTRODUCTION                                      in the context of algorithmic improvements:
                                         A. Motivation                                                                      • What factors cause conflicts in the NLSAT algorithm, and

                                            Satisfiability Modulo Theories (SMT) refers to the problem                         can some of them be avoided?
                                                                                                                            • Is it possible to assign values directly to arithmetic vari-
                                         of determining the satisfiability of formulas in first-order
                                         logic. SMT problems typically involve theories such as linear                         ables, independent of literal-level decision information,
                                         and nonlinear arithmetic, uninterpreted functions, strings, and                       within a CDCL-style framework?
                                                                                                                            • Can propagation be performed on arithmetic variables,
                                         arrays [1]. As a fundamental problem in software engineer-
                                         ing, formal methods, and programming languages, SMT has                               analogous to unit propagation in SAT solving, and is
                                         widespread applications, including symbolic execution [2], [3],                       this new propagation method effective for guiding assign-
                                         program verification [4], [5], program synthesis [6], automata                        ments and detecting conflicts?
                                         learning [7], [8], and neural network verification [9]–[12].                    B. Contributions
                                            Nonlinear real arithmetic (NRA) is a class of arithmetic
                                         theories. It consists of atoms represented as inequalities over                    To address the questions above, this paper proposes, for
                                         polynomials, and is therefore sometimes referred to as the                      the first time, a new algorithm that incorporates clause-level
                                         theory of polynomial constraints. Variables can take Boolean                    information.
                                         or real values, depending on their types. SMT(NRA) instances                       First, we analyze the conflict problems that arise in NLSAT
                                         are typically generated from both academic and industrial                       and categorize them into two types. As described in [22],
                                         applications. They are commonly used in cyber-physical sys-                     each clause narrows the feasible set1 of an arithmetic variable.
                                         tems [13]–[15], ranking function generation [16], [17], and                     This technique has previously been used to enlarge the oper-
                                         nonlinear hybrid automata analysis [18]. Instances from these                   ation choices in local search algorithms, but it has not been
                                                                                                                         considered in complete methods like NLSAT. Consequently,
                                           This work was conducted during the author’s Master studies at the Institute
                                         of Software, Chinese Academy of Sciences.                                         1 Also called the satisfying domain in [22].
arithmetic variables can sometimes be narrowed to an empty           D. Artifact Availability
search space, causing conflicts. We describe this type of prob-
                                                                        To facilitate reproducibility and further research, we release
lem from the perspective of interval arithmetic and propose a
                                                                     the full implementation of ClauseSMT, together with all
solution based on the computation of feasible intervals. The
                                                                     experimental data and scripts, as an open-source artifact. The
clause-level feasible-set idea extends the spirit of NLSAT by
                                                                     artifact is publicly available on a GitHub repository2 , enabling
directly guiding assignments to arithmetic variables.
                                                                     researchers to replicate our experiments and investigate the
   Second, we introduce an incremental computation of the            solver’s performance on the QF NRA benchmark.
clause-level feasible set, followed by the definition of clause-
level propagation. In SAT solvers, unit propagation is an ef-                               II. P RELIMINARIES
fective tool to deduce assignments and detect conflict clauses.
Analogously, clause-level propagation is employed to fix a             This section introduces the basic definitions of SMT prob-
possible witness for an arithmetic variable or to quickly detect     lems over nonlinear real arithmetic, followed by a review of
empty feasible-set cases.                                            the NLSAT algorithm. In addition, we present the computation
   Finally, we present the structure and implementation de-          of clause-level feasible sets.
tails of our solver, clauseSMT. Although dynamic variable
ordering has been discussed in [23], SMT-RAT [24] solves             A. Syntax of SMT(QF NRA)
fewer instances due to the lack of efficient data structures. We      The syntax of SMT constraints over nonlinear real arith-
present techniques and data structures inspired by SAT solving.      metic is defined as follows:
Our implementation extends the NLSAT module of the Z3
solver [25], relying on existing libraries in Z3 for mathematical          arithmetic variables:    x∈V
operations such as root isolation, polynomial operations, and                boolean variables:     b∈B
algebraic number representation. Experiments on the SMT-                          polynomials:      p := x | c | p + p | p · p
LIB benchmark demonstrate the effectiveness of our proposed
techniques, including the look-ahead mechanism and clause-                               atoms:     a := b | p ≤ 0 | p ≥ 0 | p = 0
level propagation. The results show that clauseSMT solves                               literals:   l := a | ¬a
the most satisfiable instances and is highly competitive against                      formulas:     φ := l | φ ∨ φ | φ ∧ φ
other SMT solvers overall.
   In summary, this paper makes the following contributions:            An atom is either a Boolean atom, defined by a Boolean
                                                                     variable b ∈ B, or an arithmetic atom, defined by a (non-
  • We propose a new MCSAT-based method for nonlinear                strict) inequality or equality of a polynomial over V. A literal
    arithmetic, introducing clause-level feasible sets to avoid      is either an atom or its negation. A clause is a disjunction of
    conflicts caused by literal-level decisions.                     literals, and all input formulas are transformed into conjunctive
  • We define clause-level propagation, which quickly de-
                                                                     normal form (CNF), i.e., a conjunction of clauses. SMT(NRA)
    tects conflict cases or fixes values for arithmetic variables.   refers to the set of formulas over the theory of nonlinear real
  • We integrate the propagation method into the VSIDS
                                                                     arithmetic.
    branching heuristic, guiding the search process and re-
                                                                        For the semantics, we define an assignment α as a mapping
    ducing semantic stages.
                                                                     from variables to values.
  • We implement these ideas in our solver clauseSMT
    and conduct experiments on SMT-LIB benchmarks to                   • A Boolean assignment maps Boolean variables to truth
    demonstrate the effectiveness of our approach.                       values, denoted as αbool : b 7→ {⊤, ⊥}.
                                                                       • An arithmetic assignment maps real variables to real
                                                                         numbers, denoted as αreal : x 7→ R.
C. Structure of the Paper                                              A full assignment maps all Boolean and real variables, while
   The paper is organized as follows. In Section II, we in-          a partial assignment only covers a subset. Under a given
troduce SMT problems over nonlinear real arithmetic and              assignment, each atom is evaluated as follows:
review the traditional complete method NLSAT. Section III              1) true, if the assignment satisfies it;
analyzes the conflicts that occur in the NLSAT algorithm. In           2) false, if the assignment violates it;
Section IV, we present a feasible-set based look-ahead mech-           3) undefined or unevaluated, if it contains variables not yet
anism. Building on the concept of clause-level information,               assigned.
Section V introduces the clause-level propagation algorithm            A full assignment that makes all clauses true is called a
and a new branching heuristic. Section VI discusses the details      model (or solution) of the formula, certifying its satisfiability.
of implementation. We compare our solver with other SMT              The SMT(QF NRA) problem is to decide whether such a
solvers and perform an ablation study in Section VII. Related        model exists for a given input formula, or to prove that none
work on solving non-linear real arithmetic is reviewed in            does.
Section VIII. Finally, Section IX concludes the paper and
outlines potential directions for future research.                     2 https://github.com/yogurt-shadow/ClauseSMT ASE2025
B. Feasible Set                                                                  the CDCL framework. Specifically, NLSAT extends traditional
   For nonlinear real arithmetic constraints, a key technique                    unit propagation and boolean decisions to real-variable prop-
for determining the possible values of arithmetic variables is                   agation (R-propagation) and semantic decisions.
root isolation. Given an arithmetic atom of the form                                To select an appropriate value for an arithmetic vari-
                                                                                 able, NLSAT incrementally updates its feasible-set during the
                         p {≤, ≥, =, >, <} 0,                                    search. Let the current feasible-set be curr set, the feasible-
if exactly one variable v remains unassigned under the current                   set of a literal lit be lit set, and real-variable propagation
assignment, we can compute the set of values of v that satisfy                   take effect under the following circumstances:
the atom. We call this set the feasible set.                                        • lit set is empty: the literal is propagated as false, since
   For higher-order polynomial constraints, feasible sets are                          no value can satisfy it.
usually computed via root isolation, which determines the                           • lit set is full: the literal is propagated as true, since any
roots of the polynomial. These roots partition the real line                           value satisfies it.
into intervals3 . Each interval preserves a fixed truth value of                    • curr set is a subset of lit set: the literal is propagated
the atom, and the union of all satisfying intervals forms the                          as true, because the current feasible-set already satisfies
overall feasible set.                                                                  it.
   For negated literals, the feasible set is simply the comple-                     • curr set has no intersection with lit set: the literal
ment of the feasible set of the corresponding positive atom.                           is propagated as false, because all values in the current
By restricting the variable v to any value in the feasible set,                        feasible-set violate the literal.
the atom is guaranteed to be satisfied4 .                                        When processing a clause containing both boolean and arith-
   Besides the literal level, the notion of a feasible set can also              metic variables, NLSAT first applies propagation and evalua-
be extended to the clause level, where it represents the set of                  tion to detect evaluated literals. If one literal is true, the clause
values that make the entire clause satisfied. In this work, we                   is skipped; otherwise, NLSAT decides the first unevaluated
focus on the case where exactly one arithmetic variable in the                   literal and updates the feasible-set accordingly. Algorithm 1
clause is left unassigned; we call such a clause a univariate                    presents the detailed processing steps in NLSAT.
clause.                                                                             For conflict analysis, NLSAT employs cylindrical algebraic
Definition 1 (Feasible Set). Let l be a literal, x an arithmetic                 decomposition (CAD) as an explanation tool. Using model-
variable, and α an assignment that maps all variables in l                       based projection, it identifies the conflict cell and generates a
except x. The feasible set (resp. infeasible set) of l is the union              lemma to prevent the solver from revisiting the same conflict
of intervals over R such that l is satisfied (resp. unsatisfied)                 in the future. Algorithm 2 presents the complete NLSAT
when x is assigned any value from the interval.                                  procedure.
   Similarly, let c be a clause, x an arithmetic variable, and
                                                                                     III. C ONFLICTS D URING THE NLSAT A LGORITHM
α an assignment that maps all variables in c except x. The
feasible set (resp. infeasible set) of c is the set of all values of                In this section, we analyze the sources of conflicts in
x that make c satisfied (resp. unsatisfied). It can be computed                  NLSAT algorithms. Broadly, these conflicts can be categorized
by taking the union (resp. intersection) of the feasible sets                    into two types: those caused by semantic decisions and those
(resp. infeasible sets) of all literals in c.                                    caused by literal decisions.
   Example 1 illustrates the construction of a feasible set.
                                                                                 A. Conflicts Caused by Semantic Decisions
Example 1. Consider an assignment α := {b 7→ ⊥, x 7→ 0}.
                                                                                    In SAT solving, conflicts are typically caused by literal (i.e.,
The feasible set of the clause
                                                                                 boolean variable) decisions. For a satisfiable instance, a SAT
                     b ∨ (y + x > 0) ∨ (y 2 > 2)                                 solver can avoid conflicts if it uses a perfect phase selection
                                                                                 strategy (i.e., assigns variables correctly to true or false). For
is                           √                                                   unsatisfiable instances, conflicts are unavoidable regardless of
                       (−∞, − 2) ∪ (0, ∞),                                       the phase choices. In both cases, when CDCL detects a conflict
since these are the values of y that satisfy the clause given                    due to incorrect decision values, conflict analysis is invoked
the current assignment.                                                          to generate a new lemma that forces a change in the previous
                                                                                 assignment.
C. Original NLSAT Algorithm                                                         Similarly, in the NLSAT algorithm for SMT solving, con-
   NLSAT is the core algorithm for nonlinear real arithmetic                     flicts can arise from incorrect semantic decisions, i.e., selecting
(NRA) within the Z3 solver [25]. It handles both boolean and                     a value from a given interval. As discussed in [26], the
arithmetic variables directly, integrating theory reasoning into                 search space of nonlinear arithmetic is partitioned into sign-
                                                                                 invariant cells. However, in systematic solvers like NLSAT,
   3 In the terminology of cylindrical algebraic decomposition, such intervals
                                                                                 the current cell being explored cannot be predicted in advance,
are also called cells.
   4 The feasible set may also be empty or cover the entire real line, meaning   and therefore conflicts may occur. For unsatisfiable instances,
the atom is always unsatisfiable or always satisfied, respectively.              every cell in the search space is inconsistent with at least
  Algorithm 1: Clause Processing in NLSAT                              Algorithm 2: Original NLSAT
   Input : A set of clauses F                                           Input : A formula F
   Output: Conflict clause conf cls, or No Conflict                     Output: SAT or UNSAT
 1 for each clause c ∈ F do                                           1 while true do
 2     for each literal l ∈ c do                                      2    v ← select next variable according to branching
 3         lit set ← compute feasible-set of l;                              heuristic;
 4         val ← real propagate l using lit set;                      3    conf cls ← process clauses univariate to v
 5         if val = ⊤ then                                                   (Algorithm 1);
 6             break;                                                 4    if conf cls is empty then
               // clause is satisfied, skip                                    // No conflict detected
                   remaining literals                                 5        if v is boolean then
 7          if val = ⊥ then                                           6            perform boolean decision;
 8              continue;                                              7        else if v is arithmetic then
                // literal unsatisfied, check                          8            perform semantic decision;
                    next literal                                       9        else
 9      if exist satisfied literal in c then                          10            return SAT // all variables
10          continue;                                                                   assigned consistently
            // clause satisfied, check next                           11    else
                  clause                                                        // Conflict detected
11      else if exactly one literal undefined in c then               12        new lemma ← conflict analysis via CAD;
12          unit propagate the literal;                               13        if new lemma is empty then
13      else if two or more literals undefined in c then              14            return UNSAT // formula is
14          decide the first undefined literal;                                         unsatisfiable
15      else                                                          15        else
            // all literals are unsatisfied                           16            backtrack;
16          return c // conflict detected
17   return No Conflict;
                                                                      B. Conflicts Caused by Literal Decisions
                                                                         A key technique in NLSAT is processing clauses that are
                                                                      univariate with respect to the current arithmetic variable. In
                                                                      a CDCL-style systematic search, literals are assigned either
                                                                      through unit propagation for unit clauses (i.e., clauses with
                                                                      only one unassigned literal) or via decisions for clauses with
                                                                      multiple unassigned literals. However, the literal decision
                                                                      mechanism in NLSAT has received relatively little attention.
                                                                      Improper literal decisions may introduce additional conflicts.
                                                                      We illustrate this situation in Example 3.
                                                                      Example 3. Consider the following three clauses:

                                                                                  c1 : y 2 + x − 2 ≤ 0 ∨ y 2 − x − 2 ≤ 0,
         Fig. 1. Demo of a conflict caused by a semantics decision.                  c2 : x + y = −3,    c3 : x − y = 3.

                                                                         As illustrated in Figure 2, the purple area satisfies both
                                                                      polynomials in c1 , while the red and blue areas satisfy only
one polynomial constraint, making conflicts unavoidable. A
                                                                      y 2 + x − 2 ≤ 0 and y 2 − x − 2 ≤ 0, respectively. The straight
demonstration is provided in Example 2.
                                                                      lines represent the equality constraints in c2 and c3 .
Example 2. Consider the formula y 2 + x + 1 ≤ 0 with the                 Suppose the SMT formula is {c1 , c2 }. The intersection
variable order {x, y}. As depicted in Figure 2, if we decide          occurs only in the red area. If the formula is {c1 , c3 }, the
x 7→ 2, the satisfying region (shaded area) does not intersect        intersection is located only in the blue area. When NLSAT
the line x = 2, resulting in a conflict. This conflict is caused      processes a clause with multiple unassigned literals such as
by an incorrect semantic decision for variable x and could be         c1 , it decides on one literal and branches the search space into
avoided by choosing a correct value, for instance x 7→ −2.            either the red+purple or blue+purple areas. In this scenario,
                                                                     in CS. Formally, the feasible-set of CS can be computed as
                                                                     the intersection of the feasible-sets of individual clauses:
                                                                                                       \
                                                                                feasible set(CS) =          feasible set(c)
                                                                                                      c∈CS

                                                                        By using the feasible-set of a clause set, we can more
                                                                     directly determine the search space of an arithmetic variable.
                                                                     Specifically, when the feasible-set is non-empty, assigning any
                                                                     value from the set to the variable (i.e., a semantics decision)
                                                                     guarantees progress in the search, allowing the algorithm to
                                                                     proceed to the next stage. Conversely, when the feasible-set is
                                                                     empty, no choice of value can avoid inconsistency.
                                                                        We now answer the question posed in Section III with the
                                                                     following formal definition:

        Fig. 2. Demo of a conflict caused by a literal decision.     Definition 3. Given a clause set, if its feasible-set is non-
                                                                     empty, then, in theory, conflicts can be avoided by choosing
                                                                     appropriate literal assignments; we call this a path case. Con-
there is a 50% chance of missing the equality line and               versely, if the feasible-set is empty, conflicts cannot be avoided
encountering a conflict.                                             through literal decisions (caused by semantic decisions); we
   However, the feasible-set of c1 (i.e., the union of red, blue,    call this a block case. Examples 5 and 6 illustrate a path case
and purple areas) has a nonempty intersection with both lines,       and a block case, respectively.
indicating that both formulas {c1 , c2 } and {c1 , c3 } are indeed
                                                                     Example 5.
satisfiable.                                                                                                     )
   Here comes a new problem in this circumstance. Is it pos-         c1 :[−4, −2] ∨ [2, 4] → {[−4, −2] ∪ [2, 4]}, ^
                                                                                                                           → {[2, 4]}
sible to avoid conflicts with a better literal-decision heuristic?   c2 :[−6, −5] ∨ [1, 5] → {[−6, −5] ∪ [1, 5]}
If so, how can this be achieved? The key idea is to view
                                                                     This example shows a path case, since the clauses can be
the literal-decision problem as a satisfiability problem over
                                                                     satisfied by deciding literals in the green boxes.
intervals. Example 4 illustrates this idea.
                                                                     Example 6.
Example 4. Suppose the current assignment is α := {x 7→ 0}.                                                          )
Clauses univariate with respect to y are shown as follows:               c1 :[-4, -2] ∨ [2, 4] → {[−4, −2] ∪ [2, 4]}, ^
                                                                                                                             →∅
       c1 :   (y + 2)(y + 4) ≤ x ∨ (y − 2)(y − 4) ≤ x                    c2 :[-6, -5] ∨ [5, 6] → {[−6, −5] ∪ [5, 6]}
       c2 :   (y + 5)(y + 6) ≤ x ∨ (y − 1)(y − 5) ≤ x                This example shows a block case: the clauses cannot be
By calculating the feasible-set of each literal, the interval view   satisfied regardless of which literals we decide.
of the clauses is:                                                      The feasible-set computation provides a view of the cur-
                                                                     rently consistent search space. However, in a CDCL-style
                       c1 : [−4, −2] ∨ [2, 4]
                                                                     algorithm, literals still need to be assigned to enable future
                       c2 : [−6, −5] ∨ [1, 5]                        conflict analysis. This raises the following question: how
                                                                     should we decide literals once we already know it is a path
Then the problem can be stated as: is there a value that
                                                                     case (i.e., when the green boxes in Example 5 are identified)?
belongs to at least one interval of each clause?
                                                                        In our approach, we employ a look-ahead mechanism that
  IV. F EASIBLE -S ET BASED L OOK -A HEAD M ECHANISM                 first selects a pre-appointed value from the feasible-set. This
                                                                     pre-appointed value is then used to guide the search for a
   In this section, we incorporate the clause-level feasible-set
                                                                     consistent decision path. The detailed procedure is presented
into the NLSAT algorithm and design a look-ahead mecha-
                                                                     in Algorithm 3.
nism.
                                                                        The updated algorithm introduces the additional condition
A. Look-Ahead Before Processing Clauses                              that the feasible-set of the current literal must contain the
                                                                     pre-appointed value. This ensures that the feasible-sets of
   We first extend the definition of feasible-set to a set of
                                                                     all decided literals during the processing procedure intersect
clauses.
                                                                     at the clause-set level, allowing the arithmetic variable to
Definition 2. Given a clause set CS, an arithmetic variable          be assigned the pre-appointed value. In the block case, the
x, and an assignment that maps all variables appearing in any        processing algorithm behaves identically to NLSAT, eventually
clause of CS except x, the feasible-set (resp. infeasible-set) is    triggering the resolve procedure to revise previous arithmetic
the set of values for x that satisfy (resp. unsatisfy) all clauses   assignments.
  Algorithm 3: Deciding Literals Using Pre-Appointed                     Algorithm 4: Process Clauses After a New Lemma
  Value                                                                   Input: A new lemma lemma, arithmetic variable v
   Input : A set of clauses F , pre-appointed value val                 1 lemma feasible set ← compute feasible-set of
             selected from feasible-set                                     clause(lemma);
   Output: Decided literals lits                                        2 feasible set[v] ←
 1 lits ← ∅;                                                                feasible set[v] ∩ lemma feasible set;
 2 for each clause c ∈ F do                                             3 if feasible set[v] is empty then
 3     path literal ← undefined;                                               // Block case: no consistent
 4     for each literal l ∈ c do                                                    assignment possible for v
 5         lit set ← compute feasible-set of l;                                // Proceed as in original NLSAT
 6         val lit ← real propagate literal l;                                      (Algorithm 1)
 7         if val lit = ⊤ then                                          4      original process clauses;
 8             break // clause already
                                                                        5 else
                    satisfied
                                                                              // Path case: a consistent
 9          if val lit = ⊥ then                                                   assignment exists for v
10              continue // literal unsatisfied,                        6     val ← value selection(feasible set[v]);
                     check next literal                                       // Call Algorithm 3 to decide
11          if lit set contains val then                                          literals using the pre-appointed
12               path literal ← l // decide                                       value
                     satisfiable literal under                          7     deciding literals using pre-appointed value (val );
                     pre-appointed value
13      if only one literal undefined in c then
14          unit propagate the literal;                                 new lemma, the updated feasible-set may become inconsistent
15      else if path literal is defined then                            with any literal in the lemma, resulting in a conflict. The
16          lits ← lits ∪ {path literal};                               right column shows a new feasible path after incrementally
                                                                        processing the lemma.
17   return lits;
                                                                           Look-ahead algorithm after conflict analysis is similar to
                                                                        the main search part, as shown in Algorithm 4. The main
                                                                        difference is the incremental computation of decision cases by
B. Look-Ahead After Conflict Analysis                                   considering only the feasible-set of the new lemma. We use
   In addition to processing clauses with multiple literals,            a vector of intervals to cache the previous feasible sets. After
our decision-making algorithm remains effective in conjunc-             calculating the clause-level feasible-set, we must reprocess
tion with cylindrical algebraic decomposition (CAD)-based               the clauses for the path case and find a new decision path.
explanation. CAD projects conflict polynomials to learn a               Because the newly generated lemma adds a new constraint
lemma that eliminates a sign-invariant cell. The learned lemma          on the arithmetic variable, the current decision path might be
includes extended polynomial constraints, referred to as root           blocked as shown in Example 7.
atoms, of the form:
                     y ∼ rooti (p(x1 , . . . , xn )),                                V. C LAUSE -L EVEL P ROPAGATION

where y is the last assigned variable, ∼∈ {=, ̸=, ≤, ≥, <, >},             Following the idea of using a clause-level feasible-set, this
and p is a polynomial generated via model-based projection,             section introduces a new kind of propagation called clause-
involving previously assigned variables x1 , . . . , xn . Specifi-      level propagation. The idea is inspired by unit propagation (or
cally, when the last assigned variable y lies between two               literal propagation) in SAT solving. In a boolean satisfaction
polynomial constraints, multiple root atoms may be generated            problem, boolean variables can be unit propagated to assign
in the learned lemma, making the choice of literal assignment           a value, which allows the solver to detect conflicts as early
particularly critical.                                                  as possible. However, most existing complete algorithms do
                                                                        not perform arithmetic propagation for quick assignment or
Example 7.                                                              conflict detection.
         c1 : [-7, -2] ∨ [2, 8]                c1 : [−7, −2] ∨ [2, 8]      We now formally define clause-level propagation.
         c2 :[−11, −10] ∨ [-6, 5]          c2 : [−11, −10] ∨ [-6, 5]    Definition 4. Given a clause c, an arithmetic variable x, and
                                                                        an assignment α that assigns all variables appearing in c
 learned : [3, 4] ∨ [7, 8]                  learned : [3, 4] ∨ [7, 8]
                                                                        except x, clause-level propagation on x is the computation of
  Before learning a new lemma, the left column highlights               the feasible-set of the clause c, which serves to narrow the
a possible path in the green boxes. After incorporating the             feasible-set of the variable x.
   The main difference between arithmetic and boolean prob-                         Algorithm 5: Clause-Level Propagation
lems lies in the structure of their search spaces. In SAT solving,                   Input: Clause set F , current feasible sets of arithmetic
unit propagation assigns boolean variables to either true or                                  variables
false. In other words, unit propagation always prunes the                          1 for each clause cls ∈ F do
search space of a boolean variable by half, effectively guiding                    2     if cls is univariate to an arithmetic variable v then
the search forward, since there are only two possible values.                      3          cls feasible set ← compute feasible set(cls);
   By contrast, in arithmetic problems, a clause may only elim-                    4          feasible set[v ] ←
inate part of the real-valued domain of a variable, contracting                                 feasible set[v ] ∩ cls feasible set;
the search space without fully deciding the variable. In this                                 // Categorize propagation result
section, we introduce the clause-level propagation algorithm,                      5          if feasible set[v ] is empty then
which computes feasible-sets for arithmetic variables, and then                    6               blocked vars ← blocked vars ∪ {v} ;
show how to use this propagation information to guide the                                           // Block case: conflict
search by selecting the next branching variable.                                                    unavoidable
A. Clause-Level Propagation Method                                                 7           else if feasible set[v ] is a single value then
   In SAT solving, unit propagation is performed after variable                    8               fixed vars ← fixed vars ∪ {v} ;
assignments. In our algorithm, we incrementally compute the                                          // Fixed case: value
feasible-set of a clause whenever it becomes univariate with                                         determined
respect to an arithmetic variable5 .                                               9           else
   A newly generated univariate clause imposes an additional                                       // Other case: search space
constraint on the arithmetic variable, pruning its search space                                       narrowed but not fixed
by taking the intersection with the existing feasible-set. Unlike
boolean search spaces, arithmetic search spaces may only be
partially reduced. We categorize clause-level propagation into
three cases, illustrated in Example 8:
   • Block case: The clause-level feasible-set is empty.
   • Fixed case: The clause-level feasible-set contains exactly
      one real number, e.g., [2, 2].
   • Other case: The clause-level feasible-set is narrowed but
      neither empty nor a single value.
   This propagation information is subsequently used to guide
the branching heuristic. The algorithmic details are shown in
Algorithm 5.
Example 8. An example is shown in Figure 3. When a
variable x is assigned 0, three clauses become univariate to                       Fig. 3. Demo of clause-level propagation for y (normal case), z (fixed case)
other variables {z, y, k}. These three clauses add three new                       and k (block case).
constraints on arithmetic variables, calculated as
                {(−∞, −2] ∪ [2, 6]},           {[2, 2]},     ∅.                    clause processing procedure. Therefore, we record information
These feasible sets indicate that variables are feasible, fixed,                   about fixed and blocked variables and prioritize them in the
or blocked.                                                                        branching heuristic, ensuring that the search addresses these
                                                                                   critical variables as early as possible.
B. Propagation-Based Branching Heuristic                                              For variables in the normal case (neither fixed nor blocked),
   In SAT solving, after unit propagation, an unassigned                           we adopt the Variable State Independent Decaying Sum
boolean variable is either propagated to a value or a con-                         (VSIDS) heuristic [27], as suggested in [23], [28]. The full
flict clause is detected immediately. Similarly, for arithmetic                    procedure is outlined in Algorithm 6. Details on our im-
variables, the clause-level feasible-set allows us to identify                     plementation of dynamic variable ordering are discussed in
propagation and conflict cases, corresponding to the fixed and                     Section VI.
blocked cases introduced above.
   However, unlike boolean unit propagation, clause-level con-                                            VI. I MPLEMENTATION
flicts for arithmetic variables cannot directly return a conflict                    All of the above algorithms are incorporated into our
clause in NLSAT; this task remains the responsibility of the                       new solver, clauseSMT. We describe the solver in detail,
   5 This occurs not only after assigning an arithmetic variable, but also after
                                                                                   including an extended version of conflict analysis and an im-
assigning a boolean variable. Whenever a clause is arithmetically univariate,      plementation of the dynamic variable ordering framework. The
its feasible-set is updated.                                                       overall structure of clauseSMT is illustrated in Figure 4, and
 Algorithm 6: Propagation-Based Branching Heuristic
  Output: A variable v to branch on
1 // Prioritize blocked variables
       (potential conflicts) first
2 if blocked vars ̸= ∅ then
3     v ← select from(blocked vars);
4 // Next, consider fixed variables
       (propagate value)
5 else if fixed vars ̸= ∅ then
6     v ← select from(fixed vars);
  // Otherwise, use VSIDS heuristic for
       normal variables
7 else
8     v ← vsids select();
9    return v


 Algorithm 7: ClauseSMT
  Input : A formula F
  Output: SAT or UNSAT
1 while true do
2    clause-level propagation(F );                                                    Fig. 4. Overall Structure of clauseSMT.
     // call Algorithm 5
3    variable v ← branching heuristic;
     // call Algorithm 6                                                     For these, we keep the resolve algorithm the same as
4    if v’s feasible-set is empty then                                       in the original NLSAT. The search engine backtracks
5        new lemma ← Resolve (Conflict Analysis);                            to the highest decision level of the new lemma and
6        if new lemma is empty then                                          attempts to unit propagate the negation of previously
7             return UNSAT;                                                  decided literals. In other words, this type of conflict
                                                                             occurs purely at the literal level.
 8            else
                                                                          2) Incremental clause conflicts
 9                Process Clauses after a new
                                                                             For literal-decision conflicts considering an incremental
                   lemma(new lemma);
                                                                             clause (i.e., a newly learned lemma), we detect these by
                  // call Algorithm 4
                                                                             recalculating the decision path. Any literals that were
10        else                                                               decided prior to this stage must be reset to allow proper
11            val ← select from feasible-set;                                propagation according to the updated feasible sets.
12            Process Clauses using pre-appointed value val;               To better manage the backtracking process, we introduce
              // call Algorithm 3                                       several new types of trails, commonly used in the NLSAT
13            assign v ← val;                                           algorithm:
14            if all variables are assigned then
                                                                          • path finder: Whenever the feasible-set at the current
15                return SAT;
                                                                            stage is non-empty, a path exists and this trail is recorded.
                                                                          • block finder: When the current stage is blocked, this trail
                                                                            is recorded.
                                                                          • clause feasible updated: Whenever the feasible-set of a
Algorithm 7 presents the integrated heuristics implemented in               clause for an arithmetic variable is updated, this trail is
the solver.                                                                 recorded.
A. Resolve
                                                                        B. Dynamic Variable Ordering Framework
   Although the look-ahead based processing algorithm is
introduced in the previous section, practical implementation               1) Watched Variables: We implement two watched vari-
involves more complex cases. As discussed, conflicts in NL-             ables, inspired by the two-watched-literals scheme, to detect
SAT can be categorized into two types:                                  univariate clauses and lemmas. Each clause or lemma is
   1) Literal-decision conflicts 6                                      watched by two variables (boolean or arithmetic) appearing
                                                                        in it. Watchers are updated whenever one of them is assigned.
     6 For the look-ahead mechanism, this occurs only in block cases.   The cases are as follows:
  •   There exists a third variable unassigned: we replace the        (version 1.0.2) [29], and YICES2 (version 2.6.2) [30]. We
      assigned watcher with this variable.                            also present an ablation study to analyze the impact of various
   • No other variable is unassigned: this clause is univariate       improvements.
      to the remaining unassigned watcher.
                                                                      A. Experiment Preliminaries
   • Both watchers are assigned: no action is taken.
                                                                         The standard benchmark for evaluating SMT solvers is
   Whenever a univariate clause is detected, its feasible-set is
                                                                      SMT-LIB7 . The full benchmark for the QF NRA theory
updated eagerly, which helps the search engine gather more
                                                                      consists of 12,134 instances, originating from various applica-
clause-level information.
   2) Projection Order: A common challenge in nonlinear               tions, including nonlinear hybrid automata, ranking function
arithmetic is the strict variable-order relationship of root          generation for program analysis, and other mathematical prob-
atoms, which are generated by model-based projection. Given           lems. Most instances are labeled as SAT or UNSAT, though
a polynomial set ps and a projection order {v1 , v2 , . . . , vk },   some remain UNKNOWN. It should be noted that instances
each time the projection method eliminates a variable, it             from SMT-LIB exhibit significant variation in clause numbers,
generates a root atom corresponding to that variable.                 literal counts, and polynomial degrees. Our experiments are
   As discussed in [23], in most cases, the variable not appear-      conducted on a server equipped with an Intel Xeon Platinum
ing in the polynomial should be assigned last. Specifically,          8153 processor running at 2.00 GHz. Each instance is limited
when all atoms are in root format, the projection order should        to a maximum runtime of 1,200 seconds, consistent with the
exactly be the inverse of the assignment order, which is how          SMT-COMP settings.
it is implemented in our solver.                                      B. RQ1: Comparison with mainstream Solvers
   3) Branching Heuristic: VSIDS is a particularly effective             We compare our algorithm with other SMT solvers in
branching heuristic. Each time a conflict is detected, we             Table II. When evaluating our approach using Z3, we dis-
increase the activities of the involved variables of all types.       able all other tactics such as CDCL(T) and any incomplete
Following the design in [23], we employ several branching             algorithms. The solvers Z3, CVC5, and YICES2 are tested
heuristics and use the uniform heuristic to compare the               without modifications, each employing its portfolio of different
activity of boolean and arithmetic variables on the same scale.       algorithms. We also evaluate the original NLSAT solver by
   4) Parameter Settings: Values of the tunable parameters are        disabling all other tactics.
summarized in Table I.                                                   Our algorithm demonstrates competitive performance com-
                                                                      pared to state-of-the-art solvers such as Z3 and CVC5. In
  Symbol               Description                           Value
                                                                      particular, clauseSMT solves the largest number of satisfiable
  arith decay          Decay factor for arithmetic vari-     0.95     instances and ranks third for unsatisfiable ones.
                       ables
  bool decay           Decay factor for boolean vari-        0.95        Figure 5 presents pairwise scatter plots of solving times,
                       ables                                          where each point’s x-coordinate corresponds to clauseSMT
  arith bump           Incremental amount of arith-           1       and the y-coordinate to a competing solver. Points below the
                       metic activity                                 diagonal (y = x) indicate instances where clauseSMT is faster.
  bool bump            Incremental amount of boolean          1          The plots show that clauseSMT efficiently handles satisfi-
                       activity
  lemma conf           Initial conflict count for deleting   100
                                                                      able instances (blue points), often outperforming mainstream
                       lemmas                                         solvers, consistent with the results in Table II. The compar-
  lemma conf inc       Incremental factor for lemma           1.5     ison with the original NLSAT baseline further highlights the
                       conflicts                                      benefits of our look-ahead and arithmetic-aware propagation
                            TABLE I                                   techniques, which reduce solving time on most instances.
                      T UNABLE PARAMETERS                                1) Comparison with CVC5: CVC5 solves the largest num-
                                                                      ber of instances overall, particularly excelling in unsatisfiable
                                                                      cases due to incomplete techniques such as interval constraint
C. Shortcut for UNSAT Instances
                                                                      propagation and incremental linearization. Notably, the MBO
   For the block case discussed in Section IV, we process             category [31], which contains single clauses with very high
blocked clauses the same way as in NLSAT. As concluded                degrees, remains challenging for CAD-based algorithms.
earlier, conflicts in this scenario occur because previous vari-         2) Comparison with Original NLSAT: Our solver performs
ables (arithmetic or boolean) were assigned incorrect values.         slightly worse on instances with high-degree polynomials,
In our implementation, we introduce a shortcut mechanism to           where feasible-set computations are relatively costly. Never-
directly return UNSAT if the blocked clauses involve only a           theless, it demonstrates significant gains in LassoRanker and
single variable. In this situation, there are no previous stages,     Hycomp, which contain thousands of instances with com-
and thus the instance is guaranteed to be unsatisfiable.              plex feasible-set relationships. For LassoRanker, our solver
                       VII. E VALUATION                               improves solved instances by 50%, and overall it solves almost
                                                                      300 more instances compared to the original NLSAT.
  In this section, we compare our algorithm with several
existing solvers, including Z3 (version 4.13.1) [25], CVC5              7 https://smt-lib.org/
            Category                     #inst        Z3    YICES2   CVC5    NLSAT    Ours
                                             SAT       0        0      0        0      0
      20161105-Sturm-MBO         405        UNSAT    124      285     285      44      39
                                           SOLVED    124      285     285      44      39
                                             SAT       2        0      0        2      2
      20161105-Sturm-MGC          9         UNSAT      7        0      0        7      6
                                           SOLVED      9        0      0        9      8
                                             SAT       2        0      1        1      2
       20170501-Heizmann          69        UNSAT      1       12      9       10      19
                                           SOLVED      3       12      10      11      21
                                             SAT      93       91      89      93      92
   20180501-Economics-Mulligan   135        UNSAT     39       39      35      41      41
                                           SOLVED    132      130     124      134    131
                                             SAT      56       52      50      58      36
           2019-ezsmt             63        UNSAT      2        2      2        2      2
                                           SOLVED     58       54      52      60      38
                                             SAT     234      235     199      235    234
          20200911-Pine          245        UNSAT      6        8      5        7      5
                                           SOLVED    240      243     204      242    239
                                             SAT     110       99      91      110     98
                                                                                             Fig. 6. Conflict counts of look-ahead NLSAT versus original and random
       20211101-Geogebra         112        UNSAT      0        0      0        0      0     NLSAT (blue: satisfiable, red: unsatisfiable).
                                           SOLVED    110       99      91      110     98
                                             SAT      69       70      62      68      70
         20220314-Uncu           225        UNSAT    155      153     148      155    152               Category             #inst   Decide Lower Degree   Random Decide   Look-Ahead
                                           SOLVED    224      223     210      223    222        20161105-Sturm-MBO          405              44                 45            44
                                             SAT       0        0      0        0      0         20161105-Sturm-MGC            9              9                  9              9
              hong                20        UNSAT      8       20      20      12      14         20170501-Heizmann           69              11                 5              7
                                           SOLVED      8       20      20      12      14     20180501-Economics-Mulligan    135             134                134            134
                                             SAT     307      227     225      244    291              2019-ezsmt             63              60                 59            58
             hycomp              2752       UNSAT    2242     2201   2212     2088   2181            20200911-Pine           245             242                242            243
                                           SOLVED    2549     2428   2437     2332   2472          20211101-Geogebra         112             110                109            110
                                             SAT      33       10      17      12      14            20220314-Uncu           225             223                224            224
             kissing              45        UNSAT      0        0      0        0      0                  hong                20              12                 12            12
                                           SOLVED     33       10      17      12      14               hycomp               2752            2332               2272          2388
                                             SAT     167      122     305      220    302                kissing              45              12                 14            15
          LassoRanker            821        UNSAT    151      260     470      174    311
                                                                                                      LassoRanker            821             394                393            389
                                           SOLVED    318      382     775      394    613
                                                                                                       meti-tarski           7006            7002               7001          7002
                                             SAT     4391     4369   4343     4391   4372
                                            UNSAT    2605     2588   2581     2611   2588
                                                                                                   UltimateAutomizer          61              58                 44            57
           meti-tarski           7006
                                           SOLVED    6996     6957   6924     7002   6960                 zankl              166              89                 89            87
                                             SAT      35       39      35      45      39                 Total             12134           10732              10652         10778
        UltimateAutomizer         61        UNSAT     11       12      10      13      12
                                           SOLVED     46       51      45      58      51                              TABLE III
                                             SAT      70       58      58      62      56
              zankl              166        UNSAT     28       32      32      27      30
                                                                                             C OMPARISON OF SOLVED INSTANCES FOR DIFFERENT LITERAL DECISION
                                           SOLVED     98       90      90      89      86                             MECHANISMS .
                                             SAT     5569     5372   5475     5541   5608
              Total              12134      UNSAT    5379     5612   5809     5191   5397
                                           SOLVED   10948    10984   11284   10732   11005

                          TABLE II
 S UMMARY OF RESULTS FOR ALL INSTANCES IN SMT-LIB (QF NRA).                                     •  Lower Degree: Decide literals with the lowest polyno-
                                                                                                   mial degree (default NLSAT heuristic).
                                                                                                • Random Decide: Randomly select literals when process-
                                                                                                   ing clauses.
                                                                                                Although the difference in solved instances across most
                                                                                             categories is small, our algorithm solves about 50 more
                                                                                             instances in the Hycomp category [18], which contains nu-
                                                                                             merous nonlinear equalities. These instances often exhibit
                                                                                             literal path cases, highlighting the advantage of the look-ahead
                                                                                             mechanism.
                                                                                                The look-ahead mechanism proactively detects blocking
                                                                                             cases and mitigates conflicts during path exploration. Figure 6
                                                                                             presents a scatter plot comparing the number of conflicts
                                                                                             incurred by the two algorithms, with the green line indicating
                                                                                             parity. For most instances, the look-ahead strategy reduces
                                                                                             conflicts, which—although not substantially impacting the
                                                                                             1200-second timeout—enables a more efficient systematic
                                                                                             search, particularly when handling clauses with multiple lit-
                                                                                             erals. Interestingly, a few instances exhibit increased conflicts
                                                                                             under the look-ahead mechanism. This arises from differences
                                                                                             in sampling intervals used to select arithmetic assignments:
Fig. 5. Run time comparison against CVC5, Z3, YICES2 and nlsat (blue
points: satisfiable instances, red points: unsatisfiable instances).                         the look-ahead algorithm employs the intersected interval for
                                                                                             witness selection, whereas the baseline relies on the literal
                                                                                             interval. Consequently, even with identical random seeds, the
C. RQ2: Effectiveness of Look-Ahead Mechanism                                                arithmetic variables may be assigned different values, leading
                                                                                             to divergent subsequent search processes.
  To evaluate the impact of the look-ahead mechanism, we
implement several variants summarized in Table III:                                          D. RQ3: Effectiveness of Clause-Level Propagation
  •   Look-Ahead: Feasible-set based look-ahead on original                                    To evaluate clause-level propagation, we compare three
      NLSAT with static variable order.                                                      solver versions: (1) original NLSAT with static variable order
                                                                     (and found uncompetitive, as discussed). Key metrics such as
                                                                     conflict counts and search stages are reported via scatter plots.

                                                                                           VIII. R ELATED W ORK
                                                                        SMT-solving methods can be categorized into complete
                                                                     and incomplete approaches. Incomplete methods are fast
                                                                     due to specialized techniques. Interval constraint propagation
                                                                     (ICP) [33], [34], as implemented in dReal [35], is widely used
                                                                     for quickly detecting unsatisfiable instances. Local search has
                                                                     also been extended from SAT to arithmetic theories, including
Fig. 7. Stage comparison of prop-VSIDS against VSIDS (blue points:   integer [36], [37], linear/multilinear real [22], and nonlinear
satisfiable instances, red points: unsatisfiable instances).         real arithmetic [26], [38].
                                                                        Complete methods dominate modern SMT solvers, per-
            Category         #inst   Static   VSIDS   prop-VSIDS
     20161105-Sturm-MBO      405      44        38         39        forming well on both satisfiable and unsatisfiable instances.
     20161105-Sturm-MGC        9       9        6          8         CDCL(T) [39] and NLSAT [21] rely on CAD for theory rea-
      20170501-Heizmann       69       7        20         21
     20180501-Economics-     135      134      133        133        soning [40], while MCSAT maintains high performance across
            Mulligan                                                 diverse applications using lighter explanation modules [41].
           2019-ezsmt          63     58        30        38
        20200911-Pine         245     243      239       239         Recent work has focused on improving NLSAT efficiency, e.g.,
      20211101-Geogebra       112     110      101        98         by optimizing variable projection orders [42]–[44], designing
        20220314-Uncu         225     224      222       222
              hong             20     12        11        11         innovative projection operators [45], generating larger literal-
            hycomp           2752    2388      2426     2472         invariant cells [46], [47], and exploring dynamic branching
             kissing           45     15        14        14
          LassoRanker         821     389      571       613         heuristics [23].
           meti-tarski       7006    7002      6974     6960
       UltimateAutomizer       61     57        52        51
              zankl           166     87        83        86
                                                                                              IX. C ONCLUSION
              Total          12134   10778    10920     11005
                                                                        We presented a clause-level NLSAT algorithm for SMT
                            TABLE IV
   C OMPARISON OF SOLVED INSTANCES FOR DIFFERENT BRANCHING
                                                                     solving over nonlinear real arithmetic. We categorized con-
                          HEURISTICS .                               flicts in NLSAT and analyzed the challenges of literal de-
                                                                     cisions faced by many CDCL-style algorithms. To address
                                                                     these challenges, we introduced a feasible-set-based look-
                                                                     ahead mechanism and clause-level propagation for branching.
based on degree (static), (2) dynamic NLSAT with VSIDS               Experimental results show that our solver is competitive with
(VSIDS), and (3) dynamic NLSAT with clause-level propaga-            mainstream solvers, demonstrating the effectiveness of the
tion (prop-VSIDS). Results are summarized in Table IV.               proposed techniques.
   The data show that VSIDS significantly improves perfor-              In future work, we aim to develop a clause-level approach
mance within the MCSAT framework. Incorporating clause-              for block cases, which are closely related to quantifier elimina-
level propagation further accelerates conflict detection and         tion. We anticipate that lighter alternatives to CAD may allow
increases the number of solved instances across most cat-            connecting literals across clauses, revising previous decisions,
egories. In particular, prop-VSIDS excels on hycomp [18],            and constructing consistent decision paths.
LassoRanker [16], [17], and meti-tarski [32], all of
which contain numerous arithmetic clauses prone to block                                 X. ACKNOWLEDGMENTS
cases. Figure 7 illustrates the reduction in search stages
(semantic decision steps) for prop-VSIDS compared to tradi-             The author gratefully acknowledges the use of computing
tional VSIDS, showing that inconsistent branching choices are        resources provided by the Institute of Software, Chinese
detected earlier and overall stages are significantly reduced.       Academy of Sciences. The author also sincerely thanks the
                                                                     anonymous reviewers for their constructive comments and
E. Threats to Validity                                               suggestions, which helped to improve the quality of this paper.
Correctness of implementation. Developing clauseSMT
                                                                                                 R EFERENCES
required substantial effort. All comparisons with other solvers
were executed in the same environment. Results were carefully         [1] C. W. Barrett and C. Tinelli, “Satisfiability modulo theories,” in
verified, and satisfiable instances were validated to ensure              Handbook of Model Checking, E. M. Clarke, T. A. Henzinger, H. Veith,
                                                                          and R. Bloem, Eds. Springer, 2018, pp. 305–343. [Online]. Available:
correctness.                                                              https://doi.org/10.1007/978-3-319-10575-8 11
Randomness. NLSAT uses internal randomness for semantic               [2] C. Cadar, D. Dunbar, and D. Engler, “Klee: unassisted and automatic
decisions and clause/literal reordering. These mechanisms are             generation of high-coverage tests for complex systems programs,” in
                                                                          Proceedings of the 8th USENIX Conference on Operating Systems
preserved in our solver, so they do not affect comparisons.               Design and Implementation, ser. OSDI’08. USA: USENIX Association,
Additionally, a fully random literal-decision variant was tested          2008, p. 209–224.
 [3] P. Godefroid, N. Klarlund, and K. Sen, “Dart: directed automated             [18] A. Cimatti, S. Mover, and S. Tonetta, “A quantifier-free SMT encoding
     random testing,” in Proceedings of the 2005 ACM SIGPLAN Conference                of non-linear hybrid automata,” in Formal Methods in Computer-
     on Programming Language Design and Implementation, ser. PLDI ’05.                 Aided Design, FMCAD 2012, Cambridge, UK, October 22-25, 2012,
     New York, NY, USA: Association for Computing Machinery, 2005, p.                  G. Cabodi and S. Singh, Eds. IEEE, 2012, pp. 187–195. [Online].
     213–223. [Online]. Available: https://doi.org/10.1145/1065010.1065036             Available: https://ieeexplore.ieee.org/document/6462573/
 [4] P. Yao, Q. Shi, H. Huang, and C. Zhang, “Program analysis via efficient      [19] C. Barrett, P. Fontaine, and C. Tinelli, “The Satisfiability Modulo
     symbolic abstraction,” Proc. ACM Program. Lang., vol. 5, no. OOPSLA,              Theories Library (SMT-LIB),” www.SMT-LIB.org, 2016.
     oct 2021. [Online]. Available: https://doi.org/10.1145/3485495               [20] B. F. Caviness and J. R. Johnson, “Quantifier elimination and cylin-
 [5] D. Beyer, M. Dangl, and P. Wendler, “A unifying view on smt-based                 drical algebraic decomposition,” in Texts and Monographs in Symbolic
     software verification,” J. Autom. Reason., vol. 60, no. 3, p. 299–335, mar        Computation, 2004.
     2018. [Online]. Available: https://doi.org/10.1007/s10817-017-9432-6         [21] D. Jovanovic and L. M. de Moura, “Solving non-linear arithmetic,”
 [6] J. Wang and C. Wang, “Learning to synthesize relational invariants,”              in Automated Reasoning - 6th International Joint Conference, IJCAR
     in Proceedings of the 37th IEEE/ACM International Conference on                   2012, Manchester, UK, June 26-29, 2012. Proceedings, ser. Lecture
     Automated Software Engineering, ser. ASE ’22. New York, NY,                       Notes in Computer Science, B. Gramlich, D. Miller, and U. Sattler,
     USA: Association for Computing Machinery, 2023. [Online]. Available:              Eds., vol. 7364. Springer, 2012, pp. 339–354. [Online]. Available:
     https://doi.org/10.1145/3551349.3556942                                           https://doi.org/10.1007/978-3-642-31365-3 27
 [7] M. Tappler, B. K. Aichernig, and F. Lorber, “Timed automata learning         [22] B. Li and S. Cai, “Local search for smt on linear and multi-linear
     via smt solving,” in NASA Formal Methods: 14th International                      real arithmetic,” in 2023 Formal Methods in Computer-Aided Design
     Symposium, NFM 2022, Pasadena, CA, USA, May 24–27, 2022,                          (FMCAD), 2023, pp. 1–10.
     Proceedings. Berlin, Heidelberg: Springer-Verlag, 2022, p. 489–507.          [23] J. Nalbach, G. Kremer, and E. Ábrahám, “On variable orderings in mcsat
     [Online]. Available: https://doi.org/10.1007/978-3-031-06773-0 26                 for non-linear real arithmetic,” in SC-square@SIAM AG, 2019. [Online].
 [8] R. Xu, J. An, and B. Zhan, “Active learning of one-clock timed                    Available: https://api.semanticscholar.org/CorpusID:204767299
     automata using constraint solving,” in Automated Technology for              [24] F. Corzilius, G. Kremer, S. Junges, S. Schupp, and E. Ábrahám,
     Verification and Analysis: 20th International Symposium, ATVA                     “Smt-rat: An open source c++ toolbox for strategic and parallel smt
     2022, Virtual Event, October 25–28, 2022, Proceedings. Berlin,                    solving,” in Theory and Applications of Satisfiability Testing – SAT 2015,
     Heidelberg: Springer-Verlag, 2022, p. 249–265. [Online]. Available:               M. Heule and S. Weaver, Eds. Cham: Springer International Publishing,
     https://doi.org/10.1007/978-3-031-19992-9 16                                      2015, pp. 360–368.
 [9] G. Amir, H. Wu, C. Barrett, and G. Katz, “An smt-based approach for          [25] L. M. de Moura and N. S. Bjørner, “Z3: an efficient SMT solver,” in
     verifying binarized neural networks,” in Tools and Algorithms for the             Tools and Algorithms for the Construction and Analysis of Systems,
     Construction and Analysis of Systems: 27th International Conference,              14th International Conference, TACAS 2008, Held as Part of the Joint
     TACAS 2021, Held as Part of the European Joint Conferences on                     European Conferences on Theory and Practice of Software, ETAPS
     Theory and Practice of Software, ETAPS 2021, Luxembourg City,                     2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings, ser.
     Luxembourg, March 27 – April 1, 2021, Proceedings, Part II. Berlin,               Lecture Notes in Computer Science, C. R. Ramakrishnan and J. Rehof,
     Heidelberg: Springer-Verlag, 2021, p. 203–222. [Online]. Available:               Eds., vol. 4963. Springer, 2008, pp. 337–340. [Online]. Available:
     https://doi.org/10.1007/978-3-030-72013-1 11                                      https://doi.org/10.1007/978-3-540-78800-3 24
[10] G. Katz, C. Barrett, D. L. Dill, K. Julian, and M. J. Kochenderfer,          [26] H. Li, B. Xia, and T. Zhao, “Local search for solving satisfiability
     “Reluplex: An efficient smt solver for verifying deep neural networks,”           of polynomial formulas,” in Computer Aided Verification - 35th
     in Computer Aided Verification, R. Majumdar and V. Kunčak, Eds.                  International Conference, CAV 2023, Paris, France, July 17-22, 2023,
     Cham: Springer International Publishing, 2017, pp. 97–117.                        Proceedings, Part II, ser. Lecture Notes in Computer Science, C. Enea
[11] B. Paulsen and C. Wang, “Linsyn: Synthesizing tight linear bounds for             and A. Lal, Eds., vol. 13965. Springer, 2023, pp. 87–109. [Online].
     arbitrary neural network activation functions,” in Tools and Algorithms           Available: https://doi.org/10.1007/978-3-031-37703-7 5
     for the Construction and Analysis of Systems: 28th International             [27] M. Moskewicz, C. Madigan, Y. Zhao, L. Zhang, and S. Malik, “Chaff:
     Conference, TACAS 2022, Held as Part of the European Joint                        engineering an efficient sat solver,” in Proceedings of the 38th Design
     Conferences on Theory and Practice of Software, ETAPS 2022,                       Automation Conference (IEEE Cat. No.01CH37232), 2001, pp. 530–535.
     Munich, Germany, April 2–7, 2022, Proceedings, Part I. Berlin,               [28] D. Jovanovic, C. Barrett, and L. de Moura, “The design and implemen-
     Heidelberg: Springer-Verlag, 2022, p. 357–376. [Online]. Available:               tation of the model constructing satisfiability calculus,” in 2013 Formal
     https://doi.org/10.1007/978-3-030-99524-9 19                                      Methods in Computer-Aided Design, 2013, pp. 173–180.
[12] ——, “Example guided synthesis of linear approximations for neural            [29] H. Barbosa, C. W. Barrett, M. Brain, G. Kremer, H. Lachnitt,
     network verification,” in Computer Aided Verification: 34th International         M. Mann, A. Mohamed, M. Mohamed, A. Niemetz, A. Nötzli,
     Conference, CAV 2022, Haifa, Israel, August 7–10, 2022, Proceedings,              A. Ozdemir, M. Preiner, A. Reynolds, Y. Sheng, C. Tinelli, and
     Part I. Berlin, Heidelberg: Springer-Verlag, 2022, p. 149–170.                    Y. Zohar, “cvc5: A versatile and industrial-strength SMT solver,” in
     [Online]. Available: https://doi.org/10.1007/978-3-031-13185-1 8                  Tools and Algorithms for the Construction and Analysis of Systems
[13] K. Bae and S. Gao, “Modular smt-based analysis of nonlinear hybrid                - 28th International Conference, TACAS 2022, Held as Part of the
     systems,” in 2017 Formal Methods in Computer Aided Design (FM-                    European Joint Conferences on Theory and Practice of Software,
     CAD), 2017, pp. 180–187.                                                          ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part
[14] Y. Shoukry, M. Chong, M. Wakaiki, P. Nuzzo, A. Sangiovanni-                       I, ser. Lecture Notes in Computer Science, D. Fisman and G. Rosu,
     Vincentelli, S. A. Seshia, J. A. P. Hespanha, and P. Tabuada,                     Eds., vol. 13243. Springer, 2022, pp. 415–442. [Online]. Available:
     “Smt-based observer design for cyber-physical systems under sensor                https://doi.org/10.1007/978-3-030-99524-9 24
     attacks,” ACM Trans. Cyber-Phys. Syst., vol. 2, no. 1, jan 2018.             [30] B. Dutertre, “Yices 2.2,” in Computer Aided Verification - 26th
     [Online]. Available: https://doi.org/10.1145/3078621                              International Conference, CAV 2014, Held as Part of the Vienna
[15] A. Cimatti, “Application of smt solvers to hybrid system verification,”           Summer of Logic, VSL 2014, Vienna, Austria, July 18-22, 2014.
     in 2012 Formal Methods in Computer-Aided Design (FMCAD), 2012,                    Proceedings, ser. Lecture Notes in Computer Science, A. Biere and
     pp. 4–4.                                                                          R. Bloem, Eds., vol. 8559. Springer, 2014, pp. 737–744. [Online].
[16] J. Leike and M. Heizmann, “Ranking templates for linear loops,”                   Available: https://doi.org/10.1007/978-3-319-08867-9 49
     Log. Methods Comput. Sci., vol. 11, no. 1, 2015. [Online]. Available:        [31] T. Akutsu, M. Hayashida, and T. Tamura, “Algorithms for inference,
     https://doi.org/10.2168/LMCS-11(1:16)2015                                         analysis and control of boolean networks,” in Algebraic Biology,
[17] M. Heizmann, J. Hoenicke, J. Leike, and A. Podelski, “Linear                      Third International Conference, AB 2008, Castle of Hagenberg,
     ranking for linear lasso programs,” in Automated Technology for                   Austria, July 31-August 2, 2008, Proceedings, ser. Lecture Notes in
     Verification and Analysis - 11th International Symposium, ATVA                    Computer Science, K. Horimoto, G. Regensburger, M. Rosenkranz,
     2013, Hanoi, Vietnam, October 15-18, 2013. Proceedings, ser.                      and H. Yoshida, Eds., vol. 5147. Springer, 2008, pp. 1–15. [Online].
     Lecture Notes in Computer Science, D. V. Hung and M. Ogawa,                       Available: https://doi.org/10.1007/978-3-540-85101-1 1
     Eds., vol. 8172. Springer, 2013, pp. 365–380. [Online]. Available:           [32] B. Akbarpour and L. C. Paulson, “Metitarski: An automatic
     https://doi.org/10.1007/978-3-319-02444-8 26                                      theorem prover for real-valued special functions,” J. Autom. Reason.,
     vol. 44, no. 3, pp. 175–205, 2010. [Online]. Available: https:
     //doi.org/10.1007/s10817-009-9149-2
[33] T. V. Khanh and M. Ogawa, “SMT for polynomial constraints on
     real numbers,” in Third Workshop on Tools for Automatic Program
     Analysis, TAPAS 2012, Deauville, France, September 14, 2012,
     ser. Electronic Notes in Theoretical Computer Science, B. Jeannet,
     Ed., vol. 289. Elsevier, 2012, pp. 27–40. [Online]. Available:
     https://doi.org/10.1016/j.entcs.2012.11.004
[34] V. X. Tung, T. V. Khanh, and M. Ogawa, “raSAT: an SMT
     solver for polynomial constraints,” Formal Methods Syst. Des.,
     vol. 51, no. 3, pp. 462–499, 2017. [Online]. Available: https:
     //doi.org/10.1007/s10703-017-0284-9
[35] S. Gao, S. Kong, and E. M. Clarke, “dreal: An SMT solver for
     nonlinear theories over the reals,” in Automated Deduction - CADE-24
     - 24th International Conference on Automated Deduction, Lake Placid,
     NY, USA, June 9-14, 2013. Proceedings, ser. Lecture Notes in Computer
     Science, M. P. Bonacina, Ed., vol. 7898. Springer, 2013, pp. 208–214.
     [Online]. Available: https://doi.org/10.1007/978-3-642-38574-2 14
[36] S. Cai, B. Li, and X. Zhang, “Local search for SMT on linear
     integer arithmetic,” in Computer Aided Verification - 34th International
     Conference, CAV 2022, Haifa, Israel, August 7-10, 2022, Proceedings,
     Part II, ser. Lecture Notes in Computer Science, S. Shoham and
     Y. Vizel, Eds., vol. 13372. Springer, 2022, pp. 227–248. [Online].
     Available: https://doi.org/10.1007/978-3-031-13188-2 12
[37] ——, “Local search for satisfiability modulo integer arithmetic
     theories,” ACM Trans. Comput. Logic, vol. 24, no. 4, jul 2023.
     [Online]. Available: https://doi.org/10.1145/3597495
[38] Z. Wang, B. Zhan, B. Li, and S. Cai, “Efficient local search for
     nonlinear real arithmetic,” in Verification, Model Checking, and Abstract
     Interpretation: 25th International Conference, VMCAI 2024, London,
     United Kingdom, January 15–16, 2024, Proceedings, Part I. Berlin,
     Heidelberg: Springer-Verlag, 2024, p. 326–349. [Online]. Available:
     https://doi.org/10.1007/978-3-031-50524-9 15
[39] R. Nieuwenhuis, A. Oliveras, and C. Tinelli, “Solving SAT and SAT
     modulo theories: From an abstract Davis–Putnam–Logemann–Loveland
     procedure to DPLL(T),” J. ACM, vol. 53, no. 6, pp. 937–977, 2006.
     [Online]. Available: https://doi.org/10.1145/1217856.1217859
[40] G. Kremer, “Cylindrical algebraic decomposition for nonlinear
     arithmetic problems,” Ph.D. dissertation, RWTH Aachen University,
     Germany, 2020. [Online]. Available: https://publications.rwth-aachen.
     de/record/792185
[41] L. M. de Moura and D. Jovanovic, “A model-constructing satisfiability
     calculus,” in Verification, Model Checking, and Abstract Interpretation,
     14th International Conference, VMCAI 2013, Rome, Italy, January
     20-22, 2013. Proceedings, ser. Lecture Notes in Computer Science,
     R. Giacobazzi, J. Berdine, and I. Mastroeni, Eds., vol. 7737.
     Springer, 2013, pp. 1–12. [Online]. Available: https://doi.org/10.1007/
     978-3-642-35873-9 1
[42] H. Li, B. Xia, H. Zhang, and T. Zheng, “Choosing better variable
     orderings for cylindrical algebraic decomposition via exploiting chordal
     structure,” J. Symb. Comput., vol. 116, pp. 324–344, 2023. [Online].
     Available: https://doi.org/10.1016/j.jsc.2022.10.009
[43] C. Chen, Z. Zhu, and H. Chi, “Variable ordering selection for
     cylindrical algebraic decomposition with artificial neural networks,” in
     Mathematical Software – ICMS 2020: 7th International Conference,
     Braunschweig, Germany, July 13–16, 2020, Proceedings. Berlin,
     Heidelberg: Springer-Verlag, 2020, p. 281–291. [Online]. Available:
     https://doi.org/10.1007/978-3-030-52200-1 28
[44] F. Jia, Y. Dong, M. Liu, P. Huang, F. Ma, and J. Zhang,
     “Suggesting variable order for cylindrical algebraic decomposition
     via reinforcement learning,” in Thirty-seventh Conference on Neural
     Information Processing Systems, 2023. [Online]. Available: https:
     //openreview.net/forum?id=vNsdFwjPtL
[45] H. Li and B. Xia, “Solving satisfiability of polynomial formulas by
     sample-cell projection,” 2020.
[46] E. Ábrahám, J. H. Davenport, M. England, and G. Kremer, “Deciding
     the consistency of non-linear real arithmetic constraints with a conflict
     driven search using cylindrical algebraic coverings,” J. Log. Algebraic
     Methods Program., vol. 119, p. 100633, 2021. [Online]. Available:
     https://doi.org/10.1016/j.jlamp.2020.100633
[47] J. Nalbach, E. Ábrahám, P. Specht, C. W. Brown, J. H. Davenport, and
     M. England, “Levelwise construction of a single cylindrical algebraic
     cell,” J. Symb. Comput., vol. 123, no. C, may 2024. [Online]. Available:
     https://doi.org/10.1016/j.jsc.2023.102288
