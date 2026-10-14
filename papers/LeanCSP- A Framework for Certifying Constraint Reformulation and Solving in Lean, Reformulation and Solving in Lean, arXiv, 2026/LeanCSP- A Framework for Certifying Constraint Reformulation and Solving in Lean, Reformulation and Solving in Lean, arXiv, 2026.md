                                               LeanCSP: A Framework for Certifying Constraint
                                                     Reformulation and Solving in Lean
                                                                        Pablo Manrique                 Stefan Szeider
                                                                             Algorithms and Complexity Group
                                                                                TU Wien, Vienna, Austria
                                                                          {pmanriqu,sz}@ac.tuwien.ac.at



                                                                                            Abstract
                                                    Constraint programming is a core technology for solving complex combinatorial problems
                                               in scheduling, planning, configuration, and verification. Trusting its results therefore demands
                                               guarantees at two levels: that reformulations applied beforehand are semantics-preserving, and
                                               that solvers produce correct answers. In this work, we introduce a framework that addresses both
arXiv:2607.28459v1 [cs.AI] 30 Jul 2026




                                               verification levels in the Lean theorem prover: it can be used to prove formulation-level proper-
                                               ties, such as equivalence, equisatisfiability, and the correctness of symmetry-breaking constraints,
                                               parametrically for entire problem families; and to check solver-produced certificates for individ-
                                               ual instances via translation backends to external formats such as MiniZinc, SMT-LIB, and OPB.
                                               Combining both levels yields an end-to-end workflow that establishes the satisfiability or unsat-
                                               isfiability of a constraint problem without trusting the external solver. Experimental results show
                                               that our framework’s verified symmetry breaking also pays off in practice: a single parametric
                                               proof per problem family, reused across all instance sizes, reduces solver search effort by a factor
                                               of up to 2 × 107 , while the entire in-Lean certification stays affordable, taking at most a few
                                               minutes for our largest instances.

                                         Code — https://github.com/leansolving/leancsp



                                         1    Introduction
                                         Constraint satisfaction problems (CSPs) constitute a powerful framework for modeling and solving
                                         a wide range of combinatorial problems, from scheduling and resource allocation to hardware ver-
                                         ification and combinatorial design [Tsang, 1993, Dechter, 2003, Rossi et al., 2006]. Operationally,
                                         practitioners often reformulate CSPs to improve solver performance, switching between alterna-
                                         tive encodings or adding symmetry-breaking constraints [Gent et al., 2006]. Moreover, different
                                         symmetry-breaking constraints can be added to the problem, with the intent of pruning symmetric
                                         solutions and speeding up the solving process. Ensuring that these modifications do not contain errors
                                         that can silently eliminate solutions or introduce spurious ones is essential for correctness. Crucially,
                                         such an error can be invisible to testing: we exhibit a plausible symmetry-breaking constraint for
                                         the Schur problem that preserves satisfiability on every instance up to n = 12 yet silently flips the
                                         answer exactly at n = 13, where a solver then certifies a false bound on the third Schur number
                                         S(3). Our proposed framework rejects this constraint, because the required symmetry proof cannot
                                         be given. Furthermore, once the problem is formulated as a CSP, solvers are used to find solutions
                                         that satisfy the specified constraints. However, modern solvers are complex and constantly evolving
                                         software artifacts that might contain bugs [Vanroose et al., 2024, Mansur et al., 2020], so checking
                                         that the answer given by the solver is correct is another important step to obtain formal guarantees.
                                      Lean

   Verified Reformulation                                                                    Verified Solving


                                                                    Lean          SAT
                            CSP P                                                            Solver
                                                                   decide         cert

   equiv/equisat                             (un)satisfiable
       thm                                        thm

                                                                                 UNSAT   .mzn/.smt/.opb
                            CSP P ′                                 PBLean
                                                                                  cert         file


                                                                   translation


Figure 1: Overview of LeanCSP. A CSP P can be formulated in Lean, and a reformulation (an
equivalence or equisatisfiability theorem) that yields another CSP P ′ can be proven correct at the
parametric level. At the instance level, a CSP is translated to an external solver format; the solver’s SAT
or UNSAT certificate is checked back in Lean (by decide or PBLean, respectively), establishing
an (un)satisfiability theorem. The external solvers are outside the trusted Lean base: every certificate
produced is checked back against the original problem inside Lean, so any possible errors or bugs in
the solvers cannot produce a false guarantee, only a check that fails.


     These two formal verification problems are addressed in the literature using two main approaches:
proof assistants and proof logging. Proof assistants (or interactive theorem provers, ITPs), like
Rocq [The Rocq Development Team, 2025], Isabelle/HOL [Nipkow et al., 2002], Agda [Stump,
2016] or Lean [de Moura and Ullrich, 2021], are systems that let users develop formal proofs
validated by a small trusted kernel built on a foundational logic. Their expressivity allows one to
obtain general guarantees independent of the instance size at the formulation level: related work is
verifying SAT encodings, proving that they are equivalent to the mathematical properties that they
represent [Cruz-Filipe et al., 2019, Abdulaziz and Kurz, 2023, Codel et al., 2023, Subercaseaux et al.,
2024]; certified constraint solvers [Carlier et al., 2012, The Colibri Team, 2019]; and, closest to our
work, proving that a transformation of CSPs preserves satisfiability [Dubois, 2020]. In proof logging,
solvers emit certificates of their answers that small separate checkers validate per instance, so one
proof is obtained per solver run. This is a standard practice in SAT [Heule et al., 2013, Wetzler et al.,
2014, Cruz-Filipe et al., 2017] and has been extended to SMT [Barrett et al., 2015], or CP [Gocht
et al., 2022, Flippo et al., 2024]. Proof logging can also be used for certifying reformulations at
the instance level, as VeriPB [Gocht and Nordström, 2021] can certify dominance and symmetry
breaking [Bogaerts et al., 2023]. Checkers are formally verified in some cases [Gocht et al., 2024], and
in Lean, bv_decide [Böving et al., 2025] can be used to check LRAT proofs, and PBLean [Szeider,
2026b] does the same for pseudo-Boolean certificates. These last two approaches rely on reflection: a
checker proved sound once in Lean is run as compiled code, and a successful check yields a reusable
Lean theorem rather than a mere external verdict.
     Our contribution is to tackle both verification problems using the Lean 4 theorem prover [de Moura
and Ullrich, 2021], based on dependent types and the calculus of inductive constructions, and
whose extensive mathlib [The mathlib Community, 2020] library and a growing ecosystem of
development tools [Mohamed et al., 2025, Szeider, 2026a] has enabled landmark formalizations,
including the resolution of Marton’s conjecture [Gowers et al., 2025], the sphere eversion [van Doorn
et al., 2023], and a verified typechecker for Lean itself [Carneiro, 2025]. We develop a formalization of
constraint satisfaction problems in Lean that allows us to specify constraint problems using a library
of over 40 different constraints, and to reason about them in a general way. In particular, we formalize
properties such as equivalence (the preservation of all solutions of a problem) and equisatisfiability


                                                               2
(the preservation of a problem’s satisfiability), the latter capturing symmetry-breaking constraints
as a special case. The expressivity of Lean allows us to prove these properties once for entire
parameterized families of CSPs—e.g., for all n in the n-queens problem—so instances of all possible
sizes automatically inherit them. Our framework, named LeanCSP and illustrated in Figure 1, also
enables the automatic translation of CSPs formulated in Lean into different formats once instantiated,
so that external solvers can solve them. We include translation backends for MiniZinc [Nethercote
et al., 2007], and the SMT-LIB [Barrett et al., 2010] and OPB [Roussel and Manquinho, 2016]
formats, allowing us to use constraint, SMT, and pseudo-Boolean solvers, respectively. Satisfiability
certificates (i.e., solutions) are reimported into Lean after the solver run finishes and are checked
against the original CSP to certify satisfaction. In the case of unsatisfiable problems, which we
will focus on in greater detail in this paper, the pseudo-Boolean solver RoundingSat [Elffers and
Nordström, 2018] is used to produce VeriPB [Bogaerts et al., 2023] proofs that can be independently
checked inside Lean via PBLean [Szeider, 2026b]. Although a SAT path is equally feasible using
bv_decide, we follow this pseudo-Boolean path, which our preliminary experiments (Section 4)
found better suited to the problems we target through its cutting planes reasoning. Since PBLean
can only check the unsatisfiability of a pseudo-Boolean model inside Lean, we prove, for every
constraint in our library, that its pseudo-Boolean representation in Lean is satisfied whenever the
original CSP constraint is. This translation soundness theorem lets us certify the unsatisfiability of
any CSP expressible in our library. This way, and to the best of our knowledge, we establish the
first formally verified end-to-end pipeline for constraint solving at the level of a general constraint
language: a CSP formulated in Lean and taken as the specification of the problem is proved satisfiable
or unsatisfiable by delegating the search to external solvers whose output is checked back against
the CSP itself, so that neither the translation nor the solvers need to be trusted, and uniformly for
every CSP built from our library of constraints. This sets us apart from proof-logging approaches,
whose certificates, even when validated by a formally verified checker, concern the low-level formula
the solver works on rather than yielding an unsatisfiability theorem about the CSP itself, and from
verified solvers built inside a proof assistant, which are correct by construction at the expense of
performance. Furthermore, combining both the reformulation correctness and the certificate checking
layers lets us prove the (un)satisfiability of CSPs that have not been directly solved themselves, by first
proving equisatisfiability with an optimized constraint formulation that may use symmetry-breaking
constraints and other solving speedup techniques, and then solving this second problem via an external
solver and checking its output. We apply this pipeline to certify concrete combinatorial results in
Lean, for instance the Schur number S(4) = 44 and the bounds R(3, 3) ≤ 6 and W (2, 3) ≤ 9. The
complete Lean development is available at https://github.com/leansolving/leancsp.


2    Formalization
In this section, we will describe our formalization of constraint satisfaction problems in Lean, as
well as the definitions of the central reformulation properties that we consider. We assume only a
passing familiarity with Lean, and we will provide high-level explanations of the different concepts.
However, we include some code snippets from the actual Lean formalization that can help illustrate
those concepts. We refer to the original documentation [The Lean Developers, 2026] for further
details about Lean’s syntax. Our implementation is publicly available at
                                https://github.com/leansolving/leancsp.
Code listings in this paper are lightly edited for presentation; the exact statements can be found in
the repository.




                                                    3
Basic Definitions
Following the standard definition [Rossi et al., 2006], a CSP P = (X, D, C) comprises variables
X = (x1 , . . . , xn ), domains D = (D1 , . . . , Dn ) with xi ∈ Di , and constraints C = (C1 , . . . , Cm )
where each Cj is a pair (Sj , Rj ) of a scope Sj ⊆ X and a relation Rj over the domains of variables
in Sj . Since Lean is based on dependent type theory, it is more natural to define CSPs in Lean using
dependent types rather than sets and tuples as in the standard CP definition above. More precisely,
given any type representing the variables VarIndex, and a function DomainType mapping each
variable to its (arbitrary) domain type, we define a CSP as a list of constraints:
    abbrev CSP (VarIndex : Type) (DomainType : VarIndex → Type) :=
      List (DynamicConstraint VarIndex DomainType)

    Since all elements of a list must have the same type, we use the DynamicConstraint wrapper
type that allows expressing constraints without fixing their arity. The underlying Constraint type
is defined by a scope and a checker function that expresses the relation:
    structure Constraint (VarIndex : Type) (DomainType : VarIndex → Type)
        (n : N) where
      scope : Vector VarIndex n
      check : ScopeValues VarIndex DomainType scope → Bool

    Here, ScopeValues is a dependent function that Q     maps each scope index to the corresponding
domain type. Intuitively, it just represents the product xi ∈Sj Di .
    Other basic concepts regarding CSPs are also formalized: an assignment is a function that maps
variables to values in their respective domains; a solution of a CSP is an assignment that satisfies all
constraints of the problem; and a CSP is satisfiable if it has a solution.
Example 1 (Schur triples). Consider the integers {1, . . . , n}. Can they be partitioned into k classes
such that no class contains numbers a, b, c (not necessarily distinct) with a+b = c? We can formulate
this problem as a CSP P using n integer variables x1 , . . . , xn , one per number, each ranging over
the k possible classes (or “colors”) {0, . . . , k − 1}. Then, for every triple (a, b, c) with a + b = c,
we use a constraint stating that xa , xb , and xc are not all equal. The largest n for which this problem
is satisfiable is the Schur number S(k) [Heule, 2018]; for four colors, S(4) = 44, so the instance
with k = 4 is satisfiable for n ≤ 44 and unsatisfiable for n ≥ 45.

CSP Equivalence and Equisatisfiability
Defining precisely when two CSPs are equivalent, or when a CSP encodes a given problem, is not
trivial [Rossi et al., 2006]. Taking equivalence to mean having the same set of solutions would make a
mere renaming of the variables produce a non-equivalent CSP, although the information the problems
encode remains the same. We thus use a different definition of equivalence: two CSPs are equivalent
if there exists a bijection between their solution sets. In Lean, the definition is the following, where
sol_set is the set of solutions of a CSP:
    def equivalent (csp1 : CSP VarIndex1 DomainType1 ) (csp2 : CSP
        VarIndex2 DomainType2 ) : Prop :=
      ∃ f : sol_set csp1 → sol_set csp2 , Function.Bijective f

    Note that this definition is informative only for satisfiable CSPs: any two unsatisfiable CSPs are
trivially equivalent, since their empty solution sets are in bijection. The notion becomes meaningful
through the characterization of equivalence introduced next, which exhibits an explicit correspon-
dence between the solutions of the two problems rather than a mere counting argument. Given two
CSPs P and P ′ , and a projection π that maps assignments of P ′ to assignments of P, we say that P
and P ′ are π-equivalent if:



                                                     4
   1. Solutions of P ′ map to solutions of P,
   2. Every solution of P has a preimage, and
   3. π is injective on solutions.

     If we prove that two CSPs P and P ′ are π-equivalent, then they are equivalent via the bijection
π|sol(P ′ ) . The π-equivalence definition is slightly more convenient to use when reasoning on concrete
CSPs, since it is usually easier to define a map between the assignment sets explicitly than between
the solution sets, where constraint satisfaction is implicit.
     Under the natural assumption that the assignment type of P is non-empty, i.e., every variable has
at least one domain value, we prove that two CSPs are equivalent if and only if they are π-equivalent.
    theorem equivalent_iff_pi_equivalent [Nonempty (Assignment VarIndex1
        DomainType1 )]
        (csp1 : CSP VarIndex1 DomainType1 ) (csp2 : CSP VarIndex2
        DomainType2 ) :
      equivalent csp2 csp1 ↔
        ∃ π, pi_equivalent csp1 csp2 π
    On the other hand, the definition of equisatisfiability that we use is the natural one: two CSPs
are equisatisfiable if both are satisfiable or both are unsatisfiable. If two CSPs are equivalent, in
particular they are equisatisfiable.
Example 2 (Schur triples, continued). An alternative formulation P ′ of the Schur problem of
example 1 uses n · k Boolean
                        P      variables yi,d , one per number i and color d (a one-hot encoding): a
cardinality constraint d yi,d = 1 states that each number receives exactly one color, and for every
triple (a, b, c) with a + b = c and every color d, the constraint ya,d + yb,d + yc,d ≤ 2 forbids the
monochromatic triple. The projection π maps an assignment of P ′ to the assignment of P that gives
each number i the unique color d with yi,d = 1. We prove in Lean that P and P ′ are π-equivalent,
parametrically for all n and k, so equivalence follows by the characterization above.

Symmetry
Symmetry in CSPs has been widely studied, and many definitions have appeared in the literature [Co-
hen et al., 2005]. We define a symmetry as a permutation on the variables or the domain sets that
preserves solutions, and a symmetry-breaking constraint as a constraint such that, given a solution of
the original problem, there exists a symmetry that transforms it into a solution of the extended CSP
that includes the new constraint.
    We distinguish between variable symmetries, which are permutations of the variable indices, and
domain symmetries, which are permutations of the values in the domains. A variable symmetry β
is a bijection on the variable index set such that for any solution, permuting the variables according
to β yields another solution. Note that, since in general the value domains may be different for each
variable, it is required that, for each variable v, the domain type of v is the same as the domain type
of β(v). Domain symmetries are defined similarly, but instead of permuting variable indices, they
permute the values in the domains. Since, in the case of domains, they are not necessarily the same
for all variables, we need to provide permutations for the domain of each variable. In Lean, we do
this by defining a domain equivalence (or permutation) family: a dependent function that assigns
each variable a permutation of its domain type. In order to apply a domain permutation family δ to
an assignment α, we need to map each variable v to the value δ(v)(α(v)) (this is what the apply
function does in Lean). A domain symmetry is then a domain equivalence family δ such that for any
solution, applying δ to it yields another solution.
    def DomainSymmetry (csp : CSP VarIndex DomainType)
        (δ : DomainEquivFamily VarIndex DomainType) : Prop :=


                                                   5
       ∀ assignment, is_solution csp assignment → is_solution csp
         (δ.apply assignment)
    Once the variable and domain symmetries on CSPs are defined, we can formalize the symmetry-
breaking constraints (SBCs) described at the start of this subsection. In Lean, we define domain
symmetry-breaking constraints in the following way (the variable case is analogous):
    def domainSymmetryBreakingConstraint (csp : CSP VarIndex DomainType)
        (c : DynamicConstraint VarIndex DomainType) : Prop :=
      ∀ assignment : Assignment VarIndex DomainType, is_solution csp
        assignment →
        ∃ δ : DomainEquivFamily VarIndex DomainType, DomainSymmetry csp δ
        ∧ is_solution (extended_csp csp c) (δ.apply assignment)
    Finally, these definitions allow us to prove that adding a symmetry-breaking constraint to a CSP
preserves satisfiability, since the underlying symmetry transforms solutions of the original problem
into solutions of the extended problem.
Example 3 (Schur triples, continued). In the Schur CSP P of Example 1, the k colors are inter-
changeable: permuting the colors {0, . . . , k − 1} in any solution yields another solution, since the
not-all-equal triple constraints depend only on which numbers share a color, not on the color names.
Every such color permutation is therefore a domain symmetry of P, and the value-precedence con-
straint of the next subsection breaks the whole symmetry group at once by forcing the colors to first
appear in increasing order, keeping a single representative of each class. Discharging this obliga-
tion, that the permutation really maps solutions to solutions, is exactly the step that the cautionary
example of Section 3 cannot complete for its reversal candidate, which is not a symmetry of the Schur
problem.

Examples and Proof Effort
To demonstrate the applicability of our formalization, we model several standard problem families
as parameterized CSPs in Lean and prove reformulation properties about them. These problems
are formulated using a library of more than 40 predefined constraints, organized into five families:
comparison constraints (eq, ne, lt, le, . . . ), arithmetic constraints (linear combinations, products,
absolute values), global constraints (alldifferent, cardinality, element), Boolean gates and
logical constraints such as implication and equivalence, and bound constraints that restrict the value
ranges of the variables.
    We prove two kinds of results. For six families we provide two different CSP formulations
of the same problem and prove them equivalent through the π-equivalence characterization of
Section 2: n-queens, mutilated chessboard, Latin squares, graph coloring, Schur triples, and Sudoku
(we consider classical constraint formulations with several possible integer values versus one-hot
formulations with binary values). For these problem families and five more (perfect matchings,
Langford, pigeonhole principle, and Ramsey and van der Waerden numbers), we define symmetry-
breaking constraints and prove them sound, thereby obtaining an equisatisfiability result between
the base CSP and its extension. One of them deserves special mention: value precedence—already
mentioned in Example 3—an SBC that targets problems whose values are interchangeable. The idea
is to force the values to first appear in a fixed order, thus keeping a single representative of each
value symmetry class. We prove this constraint sound once, generically and parametrically in the
number of interchangeable values, and then reuse it across five families through short per-family glue
lemmas that exhibit the relevant value permutation as a symmetry.
    All these proofs are parametric in the instance size, so each property is discharged once and
automatically inherited by every instance of the family. Table 1 reports the size of the resulting
development, in lines of Lean code, broken down by family and by kind of result. In total, the
equivalence proofs comprise 6,183 lines, the non-value-precedence symmetry-breaking soundness


                                                  6
                               Family              Equiv.       SB    VP
                               n-queens            1,791        367    —
                               Mutilated           1,216        323    —
                               Latin square          978        486    —
                               Graph coloring        791        254    71
                               Schur                 754        228    91
                               Sudoku                653        203    —
                               Matching               —         275    —
                               Langford               —         213    —
                               Pigeonhole             —          —     90
                               Ramsey                 —          —     64
                               Van der Waerden        —          —     64
                               Generic value-precedence proof         149
                               Total               6,183    2,349     529

Table 1: Proof effort, in lines of Lean code, per problem family: equivalence proof (Equiv.), symmetry-
breaking soundness proof in general (SB), and value-precedence (VP). The per-family VP entries are
glue that instantiates a single generic value-precedence proof (149 lines), established once for any
CSP and any number of interchangeable values. For Schur and graph coloring, we provide a weaker
symmetry constraint that only fixes the first color, alongside VP. A dash means no such result was
developed for that family.


proofs 2,349 lines, and the value-precedence glue 380 lines; the latter apply the generic value-
precedence proof (149 lines) established once and for all. The general formalization, which includes
the basic definitions and reformulation properties, and the general results that relate symmetry,
equisatisfiability and equivalence, sum up to about 2000 lines of Lean code.


3    Certificate Generation and Checking
Our framework supports the translation of CSPs to external solver formats for a subclass of CSPs
that is expressive enough to formulate a wide variety of combinatorial problems. We require the
variables to range over finite types, their values to be integers, and the constraints to come from the
library of predefined constraints introduced in Section 2. Any CSP following this structure can be
translated to the supported external formats once instantiated.
    We distinguish two kinds of translation. For MiniZinc and SMT-LIB, each predefined constraint
of our Lean library is mapped to a string, in the corresponding output format, that represents that
constraint. In the case of the OPB translation, we include an extra step to support unsatisfiability
certification: since PBLean can only check proofs against pseudo-Boolean formulas, we first encode
to an intermediate PB model inside Lean. This CSP to PB translation is verified to be sound: we prove
in Lean that whenever a CSP built from constraints in our library is satisfiable, the corresponding
PB model is satisfiable as well. Then, as in the case of MiniZinc and SMT-LIB, we can generate an
OPB file from the intermediate PB model. These mappings to the external formats are not formally
verified, but they do not need to be trusted: once the solver ran on an instance and produced either
a satisfiability (a solution) or an unsatisfiability (a proof) certificate, it can be reimported back
into Lean and checked against the original CSP, by directly verifying that the assignment satisfies
all constraints in the SAT case, or in the UNSAT case by using PBLean to check a VeriPB proof
generated by the solver against the intermediate PB representation, which implies that the original
CSP is unsatisfiable by the CSP to PB soundness result. A successful check yields an end-to-end
(un)satisfiability result inside Lean, so a faulty translation or an incorrect certificate can only make


                                                   7
the check fail, never certify a wrong answer.
    In both pipelines, then, the translation steps and the external solvers lie outside the trusted base.
What remains trusted is the Lean kernel, which checks every theorem in our library, including the
soundness of the PB translation, together with the Lean compiler: PBLean is proved sound in Lean
once and then run by reflection as compiled code, so each certified theorem adds to Lean’s standard
axioms only the two reflection axioms Lean.ofReduceBool and Lean.trustCompiler,
which admit the compiled checker’s verdict into the kernel and thereby place the Lean compiler in
the trusted base, exactly as the bv_decide tactic does [Böving et al., 2025]. Note that PBLean
checks the VeriPB proof against the in-Lean PB model rather than against the emitted OPB file, so
the OPB serialization also lies outside the trusted base. The CSP itself is also trusted, in the sense
that we take it directly as the specification of the problem, its “mathematical definition”, rather than
as an encoding of some separate ground truth.
Example 4 (Schur triples, continued). Applying both pipelines together lets us certify Schur numbers.
On the value-precedence formulation of Example 3 with k = 4 colors, the satisfiability pipeline
checks a solution at n = 44 while the unsatisfiability pipeline checks a VeriPB proof that n = 45
is already too many; its equisatisfiability with the plain Schur CSP carries both verdicts over,
establishing S(4) = 44 in Lean. The SAT witnesses were produced via MiniZinc (Gecode [Schulte
et al., 2019] for S(2) and S(3), Chuffed [Chu et al., 2023] for S(4)) and the UNSAT certificates
by RoundingSat [Elffers and Nordström, 2018]. The ∼98 MB UNSAT certificate for n = 45 is too
large to ship with the repository; it can be regenerated with experiments/run.py schur,
after which Lean re-checks it.
    theorem schur_4_exact :
      (schur_csp 44 4).isSatisfiableInt ∧
      ¬ (schur_csp 45 4).isSatisfiableInt


Cautionary Example: An Unsound Reformulation
The reversal mapping i 7→ n + 1 − i is a genuine variable symmetry of the van der Waerden
problem and of the modular variant of the Schur problem, so it is tempting to reuse a reversal-based
symmetry-breaking constraint, the strict lexicographic leader x <lex rev(x), on the ordinary Schur
problem of Example 1. The reformulation survives some tests one would run: for k = 3 it stays
satisfiable for all n ≤ 12 (45 solutions still satisfy the constraint at n = 12), and it first fails at
n = 13 = S(3), whose solutions are all palindromes and are therefore all deleted by the strict
constraint. If we considered this reformulated CSP as the specification of the problem, we could
check an unsatisfiability certificate and falsely “prove” that S(3) < 13.
    Our framework refuses this reformulation. Adding the leader as a sound symmetry-breaking
constraint (Section 2) requires two facts: (i) the reversal is a symmetry of the Schur CSP, for every n;
and (ii) the leader breaks that symmetry, meaning every solution can be mapped by the symmetry to
one that satisfies the leader. Both are false. Fact (i) already fails at n = 3, as one checks by hand: the
solution [0, 1, 1] reverses to [1, 1, 0], which colors the numbers 1, 1, and 2 alike although 1 + 1 = 2.
    theorem reversal_not_schur_symmetry :
        ¬ VariableSymmetry (schur_csp 3 3) (reversal 3)
    This disproof at n = 3 already refutes the family-level obligation that the reversal is a symmetry
for all n (the same witness pattern applies for every 3 ≤ n ≤ 12). The leader is thus not an SBC:
there is no symmetry to break in the first place. This missing symmetry is not, however, the real cause
of the false result at n = 13: for this specific value of n, the reversal actually is a symmetry, since
every solution is a palindrome and is fixed by it. What fails at n = 13 is fact (ii). Keeping the SBC
sound would require mapping each solution, by the symmetry, onto one that satisfies x <lex rev(x);



                                                    8
                        Pigeonhole                             Mutilated chessboard                              Odd cycle
                                                         107
                        VeriPB                                       VeriPB                              103     VeriPB
proof steps             DRAT                                         DRAT                                        DRAT




                                           proof steps




                                                                                           proof steps
              105                                        104                                             102

                                                                                                         101
                                                         101
              100                                                                                        100
                    5     10     15   20                       2       4      6        8                       101    102    103
                           n                                       k (board 2k × 2k)                                 n

Figure 2: Proof length (proof steps, log scale) versus instance size for the pseudo-Boolean (VeriPB)
and SAT (DRAT) pipelines.


but a palindrome equals its own reversal, so it never satisfies the strict inequality, and the symmetry
sends it only to itself. No solution survives the leader, so the extended problem is unsatisfiable.
    Note that the framework does not merely detect the flaw after the fact; it refuses to add the
constraint at all, because neither obligation can be proved. This is not to say that proof-logging
methods would miss the error: a fully proof-logged reformulation [Bogaerts et al., 2023] would
reject the constraint instance by instance. The vulnerable case is the common workflow, in which a
symmetry-breaking constraint is simply added to the model and only the final answer is certified, so
that an unsound reformulation silently certifies the wrong result.


4              Experimental Evaluation
We evaluate, on unsatisfiable instances, three aspects of our pipeline: the scalability of the pseudo-
Boolean certification path against a SAT-based alternative, the effect of the verified symmetry-
breaking constraints of Section 2 on solving, and also the cost of our end-to-end pipeline. All
experiments ran on an AMD Ryzen 5 PRO 8540U and 32GB of memory under Ubuntu 24.04, with
a timeout of 600 s per solver/checker invocation; each wall-clock time measurement was taken as the
median of three runs (deterministic operation counts are run-invariant).
    As LeanCSP is a general framework, the purpose of these experiments is not to obtain formal
proofs of open problems, but to discuss our design decisions and the feasibility of our methodology.

Scaling of Pseudo-Boolean versus SAT Proofs
Before committing to a certification backend, we compared a pseudo-Boolean and a SAT pipeline
on a few families. For each problem we generate UNSAT proofs at several instance sizes, solving
PB encodings with RoundingSat [Elffers and Nordström, 2018] (commit d4edbf7, checked by
VeriPB 3.0.2) and CNF encodings with CaDiCaL 1.7.3 [Biere et al., 2024] (DRAT proofs checked
by drat-trim [Wetzler et al., 2014]), measuring proof length in proof steps.
    Figure 2 shows the outcome. On the pigeonhole principle and the mutilated chessboard the
pseudo-Boolean proofs stay near-constant while the DRAT proofs grow exponentially, timing out
at moderate sizes. This is expected: cutting planes refutePthe pigeonhole principle compactly [Cook
et al., 1987, Haken, 1985], and our cardinality-based ( i xi = 1) mutilated-chessboard encoding
admits similar counting arguments [Bryant et al., 2022, Alekhnovich, 2004]. On odd-cycle non-2-
colorability, which is not a counting problem, both proofs scale linearly, suggesting that the gap
comes from resolution rather than our encoding.
    These observations motivated our choice, rather than dictated it: the pseudo-Boolean pipeline
suited the problem examples we had in mind and is the one we develop in full. They are not a verdict


                                                                      9
                     w/o SBC (lg.)          w/ SBC (lg.)      Speedup (lg.)      Speedup (geo.)   Check (native, s)    Check (in-Lean, s)
Family     SBC           det wall (s)         det wall (s)        det     wall      det    wall      w/o          w/    w/o           w/
Clique     vp      1.1×1010       186     5.5×102   0.0062 19,863,281 30,049 11,043         42       183 0.00503  197               1.95
Myciel.    vp       4.4×109       63.8    1.4×107      0.71       303      90     48       6.6        131    1.35  145              8.14
Schur      vp            t/o        t/o   1.0×109      42.9         —      —     7.5      0.83         —     47.7   —               67.7
Odd cyc.   x0 =0    4.6×102    0.0034     5.2×101    0.003         8.8    1.1    8.6       1.0 0.00081 0.000606 5.29                5.41
Ramsey     x0 =0    1.2×103    0.0037     6.8×102   0.0036         1.8    1.0    1.9      0.96 0.00109 0.00105 4.29                 4.29
vdW        vp       4.3×106     0.121     3.0×106    0.155         1.4  0.78     2.1      0.87     0.304    0.275 2.35              2.47
Match.     transp. 1.9×109        14.5    1.1×109      8.43        1.8    1.7  0.99        1.0       33.3    21.5 74.5                62
Langf.     rev.     3.0×108       4.56    2.0×108      3.26        1.6    1.4    1.4       1.1       19.4    15.7 21.3              17.3
Mutil.     refl.    3.3×102    0.0064     3.3×102   0.0076         1.0  0.84   0.99       0.94    0.0012 0.00162 16.3               16.4
PHP        vp       2.4×101    0.0041     3.9×102   0.0037      0.062    1.1   0.12        1.1 0.000352 0.00383 0.794              0.617


Table 2: Effect of a verified symmetry-breaking constraint (SBC) per family, and UNSAT certificates
checking times. SBCs: vp value precedence, x0 =0 first-variable fixing (the two-color case of value
precedence), transp. transposition, rev. reversal, refl. reflection. Sizes: Clique K3 –K15 ; Myciel. M2 –
M4 ; Schur n=5–45 (colors 2–4); Odd cyc. C5 –C51 ; Ramsey K6 –K10 (R(3, 3)); vdW n=9–28
(colors 2, 3); Match. K5 –K19 ; Langf. n=2–10; Mutil. 4×4–12×12; PHP n=2–12. Columns report,
without / with the SBC at the largest instance solved (“lg.”), RoundingSat’s deterministic operation
count and wall time (s); the speedups, at that instance and as a geometric mean over the range
(“geo.”), with a speedup >1 in bold; “Check (native)”, PBLean’s compiled checker time (s) on each
problem’s largest certificate; and “Check (in-Lean)”, the entire in-Lean checking pipeline against the
CSP, also on largest instances. t/o marks a 600 s timeout. Schur’s largest instance (c=4, n=45) is
unsolved without the SBC, so it admits no speedup and is excluded from the geo. means.


against the SAT route, which is a perfectly feasible alternative that we leave as a natural extension
for future work.

Verified Symmetry Breaking and Pipeline Cost
As discussed in Section 2, adding a symmetry-breaking constraint to a CSP has a one-time cost
in terms of proof effort. Here, we analyze when that cost is repaid in solving speed. Moreover,
we measure the cost of our end-to-end verification pipeline in the same experiment. We consider
ten different unsatisfiable problem families as our benchmark: we split the graph coloring problem
into three parameterized graph families, the clique Kn with n − 1 colors, the Mycielski graph
Mj (obtained from M0 = K2 by j Mycielskian iterations, so of chromatic number j + 2) with
j + 1 colors, and the odd cycle C2n+1 with 2 colors; upper bounds for Schur, Ramsey, and van der
Waerden numbers; perfect matchings for K2m+1 ; Langford pairings for n ≡ 1, 2 mod 4; mutilated
chessboard for even sizes; and the pigeonhole principle. For each we solve every instance with and
without an SBC, reporting RoundingSat’s deterministic operation count alongside wall time. We
check each generated certificate with PBLean v0.3.1 (Lean 4.30.0, Mathlib v4.30.0), timing both the
compiled checker alone and the full in-Lean pipeline, which adds elaboration and compilation of the
reflected model. Table 2 reports the speedups, at the largest instance and as a geometric mean over
the range, which we weigh against the one-time proof effort per family of Table 1.
    Symmetry breaking pays off most where it is theoretically most powerful. Value precedence
removes the whole group of permutations of the k interchangeable values, reducing the search space
by up to a factor of k!, and the measured speedup grows accordingly whenever the base instance
requires search. In the clique and Mycielski families the number of colors grows with the instance,
and so does the payoff, up to 2 × 107 on K15 and 303× on M4 ; it is also what makes the four-color
Schur instance at n=45 solvable at all. Where the symmetry group has a fixed size instead, the
speedup is bounded and does not grow with the instance, as in the two-color Ramsey (1.8–1.9×) and
odd cycle (8.8–8.6×) families or in Langford’s reversal (1.4–1.6×).
    The gain disappears in two cases. First, when the solver needs no search: RoundingSat settles the


                                                                  10
pigeonhole principle in 24 deterministic operations, so value precedence only adds constraints and
slows it, and the mutilated chessboard, dispatched by the same cutting-planes reasoning as above,
gives an identical operation count with and without its reflection SBC. Second, when the constraint
breaks only a small part of the symmetries: for instance, the matching transposition removes one
symmetry out of the factorially many of K2m+1 .
    Wall-clock speedups run consistently closer to one, because wall time cannot fall below a fixed
floor of about 3 ms. A search space reduction shows in time when the solving time stays above it,
and it hides regressions such as the pigeonhole slowdown entirely as well. We therefore read the
deterministic operation count as the primary measure of a constraint’s effect on search.
    Finally, PBLean’s compiled checker runs in the same order of magnitude as the solving it certifies
(from 0.98× on the clique to 4.3× on Langford), and symmetry breaking shrinks it by the same
mechanism, since less search yields a shorter proof: the clique certificate falls from 391 MB to 10 kB
and its checking from 183 s to 5 ms. On top of checking, the full pipeline must compile the reflected
model, a cost that grows with the size of the encoding rather than with the proof: in comparison, it
is minor when the certificate is large (matching: 33 s within 74 s) and dominant when the instance
is solved by propagation but its encoding is large, as in mutilated chessboard, whose 1.6 ms of
checking sit inside 16.4 s. When using SBCs, certifying the largest instance stays under two minutes
throughout.


5    Conclusion
We presented LeanCSP, a framework for certifying both constraint reformulation and constraint
solving inside the Lean theorem prover. It allows one to prove equivalence, equisatisfiability, and
symmetry-breaking soundness once for entire parameterized families of CSPs, and to certify the
(un)satisfiability of individual instances through translation to external solvers, yielding an end-to-
end pipeline that verifies these results inside Lean. As the cautionary example of Section 3 shows,
our framework rejects reformulations whose correctness is not proved. We hope that researchers
will build on LeanCSP to formulate and settle open verification and combinatorial problems with
end-to-end formal guarantees.


Acknowledgements
This research was funded in whole or in part by the Austrian Science Fund (FWF) 10.55776/COE12.


References
M. Abdulaziz and F. Kurz. Formally Verified SAT-Based AI Planning. Proceedings of the AAAI
 Conference on Artificial Intelligence, 37(12):14665–14673, June 2023. ISSN 2374-3468. doi:
 10.1609/aaai.v37i12.26714.
M. Alekhnovich. Mutilated chessboard problem is exponentially hard for resolution. Theoretical
 Computer Science, 310(1-3):513–525, Jan. 2004. ISSN 03043975. doi: 10.1016/S0304-3975(03)
 00395-5.
C. Barrett, A. Stump, and C. Tinelli. The SMT-LIB Standard: Version 2.0. Technical report,
  Department of Computer Science, The University of Iowa, 2010.

C. Barrett, L. de Moura, and P. Fontaine. Proofs in Satisfiability Modulo Theories. In All about
  Proofs, Proofs for All, volume 55 of Mathematical Logic and Foundations, pages 23–44. College
  Publications, London, UK, Jan. 2015. ISBN 978-1-84890-166-7.


                                                  11
A. Biere, T. Faller, K. Fazekas, M. Fleury, N. Froleyks, and F. Pollitt. CaDiCaL 2.0. In A. Gurfinkel
  and V. Ganesh, editors, Computer Aided Verification, volume 14681, pages 133–152. Springer
  Nature Switzerland, Cham, 2024. ISBN 978-3-031-65626-2 978-3-031-65627-9. doi: 10.1007/
  978-3-031-65627-9_7.
B. Bogaerts, S. Gocht, C. McCreesh, and J. Nordström. Certified Dominance and Symmetry Breaking
   for Combinatorial Optimisation. Journal of Artificial Intelligence Research, 77:1539–1589, Aug.
   2023. ISSN 1076-9757. doi: 10.1613/jair.1.14296.
H. Böving, S. Bhat, L. Cicolini, A. Keizer, L. Frenot, A. Mohamed, L. Stefanesco, H. Khan,
  J. Clune, C. Barrett, and T. Grosser. Interactive Bitvector Reasoning using Verified Bit-Blasting.
  Proceedings of the ACM on Programming Languages, 9(OOPSLA2):3259–3285, Oct. 2025. ISSN
  2475-1421. doi: 10.1145/3763167.
R. E. Bryant, A. Biere, and M. J. H. Heule. Clausal Proofs for Pseudo-Boolean Reasoning. In
  D. Fisman and G. Rosu, editors, Tools and Algorithms for the Construction and Analysis of
  Systems, volume 13243, pages 443–461. Springer International Publishing, Cham, 2022. ISBN
  978-3-030-99523-2 978-3-030-99524-9. doi: 10.1007/978-3-030-99524-9_25.

M. Carlier, C. Dubois, and A. Gotlieb. A Certified Constraint Solver over Finite Domains. In
 D. Giannakopoulou and D. Méry, editors, FM 2012: Formal Methods, pages 116–131, Berlin,
 Heidelberg, 2012. Springer. ISBN 978-3-642-32759-9. doi: 10.1007/978-3-642-32759-9_12.
M. Carneiro. Lean4Lean: Verifying a Typechecker for Lean, in Lean. arXiv:2403.14064, Sept. 2025.

G. Chu, P. J. Stuckey, A. Schutt, T. Ehlers, G. Gange, and K. Francis. Chuffed, a lazy clause generation
  solver. https://github.com/chuffed/chuffed, 2023.
C. R. Codel, J. Avigad, and M. J. H. Heule. Verified Encodings for SAT Solvers. In 2023 Formal
  Methods in Computer-Aided Design (FMCAD), pages 141–151, Oct. 2023. doi: 10.34727/2023/
  isbn.978-3-85448-060-0_22.

D. Cohen, P. Jeavons, C. Jefferson, K. E. Petrie, and B. M. Smith. Symmetry Definitions for Con-
  straint Satisfaction Problems. In D. Hutchison, T. Kanade, J. Kittler, J. M. Kleinberg, F. Mattern,
  J. C. Mitchell, M. Naor, O. Nierstrasz, C. Pandu Rangan, B. Steffen, M. Sudan, D. Terzopoulos,
  D. Tygar, M. Y. Vardi, G. Weikum, and P. Van Beek, editors, Principles and Practice of Con-
  straint Programming - CP 2005, volume 3709, pages 17–31. Springer Berlin Heidelberg, Berlin,
  Heidelberg, 2005. ISBN 978-3-540-29238-8 978-3-540-32050-0. doi: 10.1007/11564751_5.
W. Cook, C. Coullard, and Gy. Turán. On the complexity of cutting-plane proofs. Discrete Applied
  Mathematics, 18(1):25–38, Sept. 1987. ISSN 0166218X. doi: 10.1016/0166-218X(87)90039-4.
L. Cruz-Filipe, M. J. H. Heule, W. A. Hunt, M. Kaufmann, and P. Schneider-Kamp. Efficient
  Certified RAT Verification. In L. de Moura, editor, Automated Deduction – CADE 26, pages 220–
  236, Cham, 2017. Springer International Publishing. ISBN 978-3-319-63046-5. doi: 10.1007/978-
  3-319-63046-5_14.
L. Cruz-Filipe, J. Marques-Silva, and P. Schneider-Kamp. Formally Verifying the Solution to the
  Boolean Pythagorean Triples Problem. Journal of Automated Reasoning, 63(3):695–722, Oct.
  2019. ISSN 1573-0670. doi: 10.1007/s10817-018-9490-4.

L. de Moura and S. Ullrich. The Lean 4 Theorem Prover and Programming Language. In A. Platzer
   and G. Sutcliffe, editors, Automated Deduction – CADE 28, pages 625–635, Cham, 2021. Springer
   International Publishing. ISBN 978-3-030-79876-5. doi: 10.1007/978-3-030-79876-5_37.



                                                  12
R. Dechter. Constraint Processing. Morgan Kaufmann Publishers Inc., San Francisco, CA, USA,
  Apr. 2003. ISBN 978-1-55860-890-0.
C. Dubois. Formally Verified Transformation of Non-binary Constraints into Binary Constraints.
  arXiv:2009.00583, Sept. 2020.
J. Elffers and J. Nordström. Divide and conquer: Towards faster Pseudo-Boolean solving. In J. Lang,
   editor, Proceedings of the 27th International Joint Conference on Artificial Intelligence, IJCAI
   2018, pages 1291–1299. ijcai.org, 2018. doi: 10.24963/ijcai.2018/180.
M. Flippo, K. Sidorov, I. Marijnissen, J. Smits, and E. Demirović. A Multi-Stage Proof Logging
 Framework to Certify the Correctness of CP Solvers. In P. Shaw, editor, 30th International
 Conference on Principles and Practice of Constraint Programming (CP 2024), volume 307 of
 Leibniz International Proceedings in Informatics (LIPIcs), pages 11:1–11:20, Dagstuhl, Germany,
 2024. Schloss Dagstuhl – Leibniz-Zentrum für Informatik. ISBN 978-3-95977-336-2. doi:
 10.4230/LIPIcs.CP.2024.11.
I. P. Gent, K. E. Petrie, and J.-F. Puget. Symmetry in Constraint Programming. In F. Rossi, P. van
   Beek, and T. Walsh, editors, Handbook of Constraint Programming, volume 2 of Foundations of
   Artificial Intelligence, pages 329–376. Elsevier, 2006. doi: 10.1016/S1574-6526(06)80014-3.
S. Gocht and J. Nordström. Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs.
   Proceedings of the AAAI Conference on Artificial Intelligence, 35(5):3768–3777, May 2021. ISSN
   2374-3468. doi: 10.1609/aaai.v35i5.16494.
S. Gocht, C. McCreesh, and J. Nordström. An Auditable Constraint Programming Solver. In C. Sol-
   non, editor, 28th International Conference on Principles and Practice of Constraint Programming
   (CP 2022), volume 235 of Leibniz International Proceedings in Informatics (LIPIcs), pages 25:1–
   25:18, Dagstuhl, Germany, 2022. Schloss Dagstuhl – Leibniz-Zentrum für Informatik. ISBN
   978-3-95977-240-2. doi: 10.4230/LIPIcs.CP.2022.25.
S. Gocht, C. McCreesh, M. O. Myreen, J. Nordström, A. Oertel, and Y. K. Tan. End-to-End
  Verification for Subgraph Solving. Proceedings of the AAAI Conference on Artificial Intelligence,
  38(8):8038–8047, Mar. 2024. ISSN 2374-3468, 2159-5399. doi: 10.1609/aaai.v38i8.28642.
W. T. Gowers, B. Green, F. Manners, and T. Tao. On a conjecture of Marton. Annals of Mathematics,
  201(2):515–549, Mar. 2025. ISSN 0003-486X, 1939-8980. doi: 10.4007/annals.2025.201.2.5.
A. Haken. The intractability of resolution. Theoretical Computer Science, 39:297–308, 1985. ISSN
  03043975. doi: 10.1016/0304-3975(85)90144-6.
M. J. Heule, W. A. Hunt, and N. Wetzler. Trimming while checking clausal proofs. In 2013 Formal
 Methods in Computer-Aided Design, pages 181–188, Oct. 2013. doi: 10.1109/FMCAD.2013.
 6679408.
M. J. H. Heule. Schur number five. In Proceedings of the Thirty-Second AAAI Conference on Artificial
 Intelligence and Thirtieth Innovative Applications of Artificial Intelligence Conference and Eighth
 AAAI Symposium on Educational Advances in Artificial Intelligence, AAAI’18/IAAI’18/EAAI’18,
 pages 6598–6606, New Orleans, Louisiana, USA, Feb. 2018. AAAI Press. ISBN 978-1-57735-
 800-8. doi: 10.1609/aaai.v32i1.12209.
M. N. Mansur, M. Christakis, V. Wüstholz, and F. Zhang. Detecting critical bugs in SMT solvers
 using blackbox mutational fuzzing. In Proceedings of the 28th ACM Joint Meeting on European
 Software Engineering Conference and Symposium on the Foundations of Software Engineering,
 ESEC/FSE 2020, pages 701–712, New York, NY, USA, Nov. 2020. Association for Computing
 Machinery. ISBN 978-1-4503-7043-1. doi: 10.1145/3368089.3409763.


                                                13
A. Mohamed, T. Mascarenhas, H. Khan, H. Barbosa, A. Reynolds, Y. Qian, C. Tinelli, and C. W.
  Barrett. Lean-SMT: An SMT tactic for discharging proof goals in Lean. In Computer Aided
  Verification – 37th International Conference, CAV 2025, Proceedings, Part III, volume 15933 of
  Lecture Notes in Computer Science, pages 197–212. Springer, 2025. doi: 10.1007/978-3-031-
  98682-6_11.

N. Nethercote, P. J. Stuckey, R. Becket, S. Brand, G. J. Duck, and G. Tack. MiniZinc: Towards a
  Standard CP Modelling Language. In C. Bessière, editor, Principles and Practice of Constraint
  Programming – CP 2007, pages 529–543, Berlin, Heidelberg, 2007. Springer. ISBN 978-3-540-
  74970-7. doi: 10.1007/978-3-540-74970-7_38.
T. Nipkow, L. C. Paulson, and M. Wenzel. Isabelle/HOL: A Proof Assistant for Higher-Order Logic.
   Number 2283 in Lecture Notes in Computer Science. Springer, Berlin New York, 2002. ISBN
   978-3-540-45949-1.
F. Rossi, P. van Beek, and T. Walsh, editors. Handbook of Constraint Programming. Foundations of
   Artificial Intelligence. Elsevier, 2006. ISBN 978-0-444-52726-4.

O. Roussel and V. Manquinho. Input/Output Format and Solver Requirements for the Competitions
  of Pseudo-Boolean Solvers. https://www.cril.univ-artois.fr/PB16/format.pdf, 2016.
C. Schulte, G. Tack, and M. Z. Lagerkvist. Modeling and Programming with Gecode. https:
  //github.com/Gecode/gecode, 2019. Corresponds to Gecode 6.2.0.
A. Stump. Verified Functional Programming in Agda. Number 9 in ACM Books. Association
  for Computing Machinery, New York, NY, 2016. ISBN 978-1-970001-27-3 978-1-970001-26-6
  978-1-970001-25-9. doi: 10.1145/2841316.
B. Subercaseaux, W. Nawrocki, J. Gallicchio, C. Codel, M. Carneiro, and M. J. H. Heule. Formal
  Verification of the Empty Hexagon Number. LIPIcs, Volume 309, ITP 2024, 309:35:1–35:19,
  2024. ISSN 1868-8969. doi: 10.4230/LIPICS.ITP.2024.35.

S. Szeider. Leanback: MCP server for Lean 4 theorem proving — check, prove, goals, eval, search.
   https://pypi.org/project/leanback/, 2026a.
S. Szeider. PBLean: Pseudo-Boolean Proof Certificates for Lean 4. In 17th International Workshop
   on Pragmatics of SAT (PoS 2026), a workshop of SAT 2026 and FLoC 2026, Lisbon, Portugal,
   July 2026b. To appear. Preprint available at https://arxiv.org/abs/2602.08692.

The Colibri Team.          Colibrics: A Formally Verified Constraint Programming Engine.
  https://colibri.frama-c.com/, 2019.
The Lean Developers. The Lean Language Reference. https://lean-lang.org/doc/reference/latest/,
  2026.

The mathlib Community. The lean mathematical library. In Proceedings of the 9th ACM SIGPLAN
  International Conference on Certified Programs and Proofs, CPP 2020, pages 367–381, New
  York, NY, USA, Jan. 2020. Association for Computing Machinery. ISBN 978-1-4503-7097-4.
  doi: 10.1145/3372885.3373824.
The Rocq Development Team. The Rocq Prover. Zenodo, Apr. 2025.

E. Tsang. Foundations of Constraint Satisfaction. Academic Press, London San Diego, 1993. ISBN
   978-0-12-701610-8.




                                              14
F. van Doorn, P. Massot, and O. Nash. Formalising the h-Principle and Sphere Eversion. In
   Proceedings of the 12th ACM SIGPLAN International Conference on Certified Programs and
   Proofs, CPP 2023, pages 121–134, New York, NY, USA, Jan. 2023. Association for Computing
   Machinery. ISBN 979-8-4007-0026-2. doi: 10.1145/3573105.3575688.
W. Vanroose, I. Bleukx, J. Devriendt, D. Tsouros, H. Verhaeghe, and T. Guns. Mutational Fuzz Testing
  for Constraint Modeling Systems. In P. Shaw, editor, 30th International Conference on Principles
  and Practice of Constraint Programming (CP 2024), volume 307 of Leibniz International Pro-
  ceedings in Informatics (LIPIcs), pages 29:1–29:25, Dagstuhl, Germany, 2024. Schloss Dagstuhl
  – Leibniz-Zentrum für Informatik. ISBN 978-3-95977-336-2. doi: 10.4230/LIPIcs.CP.2024.29.
N. Wetzler, M. J. H. Heule, and W. A. Hunt. DRAT-trim: Efficient Checking and Trimming Using
  Expressive Clausal Proofs. In C. Sinz and U. Egly, editors, Theory and Applications of Satisfiability
  Testing – SAT 2014, pages 422–429, Cham, 2014. Springer International Publishing. ISBN 978-
  3-319-09284-3. doi: 10.1007/978-3-319-09284-3_31.




                                                  15
