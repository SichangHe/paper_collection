                                                                      Detecting Critical Bugs in SMT Solvers
                                                                       Using Blackbox Mutational Fuzzing
                                                          Muhammad Numair Mansur                                                       Maria Christakis
                                                                   MPI-SWS, Germany                                                    MPI-SWS, Germany
                                                                  numair@mpi-sws.org                                                   maria@mpi-sws.org

                                                                 Valentin Wüstholz                                                       Fuyuan Zhang
                                                                ConsenSys, Germany                                                     MPI-SWS, Germany
                                                          valentin.wustholz@consensys.net                                             fuyuan@mpi-sws.org
arXiv:2004.05934v1 [cs.SE] 13 Apr 2020




                                         ABSTRACT
                                         Formal methods use SMT solvers extensively for deciding formula                       SR
                                                                                                                                       sat         unsat      unknown       Crash
                                         satisfiability, for instance, in software verification, systematic test       GT
                                         generation, and program synthesis. However, due to their complex
                                                                                                                       sat                           A            C            D
                                         implementations, solvers may contain critical bugs that lead to
                                                                                                                       unsat            B                         C            D
                                         unsound results. Given the wide applicability of solvers in software
                                         reliability, relying on such unsound results may have detrimental         Table 1: Classes of bugs in SMT solvers. GT stands for ground
                                         consequences. In this paper, we present STORM, a novel blackbox           truth and SR for solver result.
                                         mutational fuzzing technique for detecting critical bugs in SMT
                                         solvers. We run our fuzzer on seven mature solvers and find 29
                                         previously unknown critical bugs. STORM is already being used in
                                         testing new features of popular solvers before deployment.                   We call bugs in class A critical for two main reasons. First, such
                                                                                                                   bugs may cause unsoundness in program analyzers that rely on SMT
                                                                                                                   solvers. As an example, consider a software verifier (e.g., Dafny [35])
                                                                                                                   or a test case generator (e.g., KLEE [19]) that checks reachability of
                                         1   INTRODUCTION                                                          an error location by querying an SMT solver. If the solver unsoundly
                                         The Satisfiability Modulo Theories (SMT) problem [11] is the decision     proves that the error is unreachable (e.g., returns unsat for the path
                                         problem of determining whether logical formulas are satisfiable           condition to the error), then the verifier will verify incorrect code
                                         with respect to a variety of background theories. More specifically,      and the testing tool will not generate inputs that exercise the error.
                                         an SMT formula generalizes a Boolean SAT formula by supplement-              Second, it is much harder to safeguard against bugs in class
                                         ing Boolean variables with predicates from a set of theories. As          A than bugs in other classes. Specifically, consider that, when an
                                         an example, a predicate could express a linear inequality over real       instance is found to be sat, the solver typically provides a model,
                                         variables, in which case its satisfiability is determined with the        that is, an assignment to all free variables in the instance such
                                         theory of linear real arithmetic. Other theories include bitvectors,      that it is satisfiable. Therefore, bugs in class B could be detected
                                         arrays, and integers [29], to name a few.                                 by simply evaluating the instance under the model generated by
                                            SMT solvers, such as CVC4 [10] and Z3 [25], are complex tools          the solver (assuming that the model is correct). If this evaluation
                                         for evaluating the satisfiability of SMT instances. A typical SMT         returns false, then there is a B bug. Bugs in class C are detected
                                         instance contains assertions of SMT formulas and a satisfiability         whenever the solver returns unknown for an instance that lies in a
                                         check (see Figs. 2 and 3 for examples). SMT solvers are extensively       decidable theory fragment, and bugs in class D are detected when
                                         used in formal methods, most notably in software verification (e.g.,      the solver crashes.
                                         Boogie [8] and Dafny [35]), systematic test case generation (e.g.,
                                         KLEE [19] and Sage [31]), and program synthesis (e.g., Alive [37]).          Related work. Early work on testing SMT solvers presented
                                         Due to their high degree of complexity, it is all the more likely         FuzzSMT [15], a blackbox grammar-based fuzzer for generating
                                         that SMT solvers contain correctness issues, and due to their wide        syntactically valid SMT instances (from scratch) for bitvectors and
                                         applicability in software reliability, these issues may be detrimental.   arrays. Since the satisfiability of the generated formulas is unknown,
                                            Tab. 1 shows classes of bugs that may occur in SMT solvers. We         the main goal of this fuzzer is to detect crashes in solver imple-
                                         restrict the classification to bugs that manifest themselves as an        mentations (class D). Critical bugs (class A) may only be detected
                                         incorrect solver result. For bugs in class A, the solver is unsound and   with differential testing, when multiple solvers disagree on the
                                         returns unsat (i.e., unsatisfiable) for instances that are satisfiable.   satisfiability of a generated SMT instance.
                                         Class B refers to bugs where the solver returns sat (i.e., satisfiable)      The above idea was recently extended to enable fuzzing string
                                         for unsatisfiable instances. A solver is incomplete when it returns       solvers by a tool called StringFuzz [13]. Similarly to FuzzSMT, String-
                                         unknown for an instance that lies in a decidable theory fragment.         Fuzz generates formulas from scratch. In addition, it can transform
                                         We categorize such bugs in class C. Finally, bugs in class D indicate     existing string instances, but without necessarily preserving their
                                         crashes where the solver does not return any result.                      satisfiability. Consequently, critical bugs in a single string solver
                                                                           Muhammad Numair Mansur, Maria Christakis, Valentin Wüstholz, and Fuyuan Zhang


cannot be detected given that the satisfiability of the formulas is          even though Z3str3 was being tested with fuzzers exclusively target-
not known a priori—differential testing would again be needed.               ing string solvers [13, 17]. A simplified version of the SMT instance
   Even more recently, there emerged another technique for testing           that revealed the bug is shown on the right of Fig. 2. (We will discuss
string solvers [17], which synthesizes SMT instances such that their         it in detail later in this section.)
satisfiability is known by construction. This ground truth is used to            A third critical bug3 was found in Z3’s tactic for applying dom-
derive test oracles. Violating these oracles indicates bugs of classes       inator simplification rules. The instance that was generated by
A and B.                                                                     STORM and revealed the bug spanned 194 lines. The minimization
   Note that finding bugs in classes C and D does not require know-          component of STORM reduced this instance to 17 lines. A simpli-
ing the ground truth. As a result, any of the above techniques can           fied version of the instance is shown on the left of Fig. 3. (We discuss
in principle detect such bugs as a by-product.                               it later in this section.) A developer of the buggy tactic asked us
                                                                             which application generated this instance, thinking that it was a
   Our approach. In this paper, we present a general blackbox                tool he developed during his PhD thesis. When we mentioned that
fuzzing technique for detecting critical bugs in any SMT solver.             it was STORM, he replied “What? Your random generator could have
In contrast to existing work, our technique does not require a               done my PhD thesis?? &@#%, you should have told me sooner :)”.
grammar to synthesize instances from scratch. Instead, it takes                  In Sect. 5, we describe in more detail our experience of using
inspiration from state-of-the-art mutational fuzzers (e.g., AFL [5])         STORM to test both mature solver implementations as well as new
and generates new SMT instances by mutating existing ones, called            features before their deployment.
seeds. The key novelty is that our approach generates satisfiable
instances from any given seed. As a result, our fuzzer detects a                Under the hood. We now give a high-level overview of our
critical bug whenever an SMT solver returns unsat for one of our             fuzzing technique, which operates in three phases. Fig. 1 depicts
generated instances. We implement our technique in a tool called             each of these phases.
STORM, which has the additional ability to effectively minimize                 The first phase, seed fragmentation, takes as input a seed SMT
the size of bug-revealing instances to facilitate debugging.                 instance S. For instance, imagine an instance with multiple asser-
                                                                             tions. Each assertion contains a logical formula, such as f in the
    Contributions. Our paper makes the following contributions:
                                                                             figure, potentially composed of Boolean sub-formulas (i.e., predi-
     (1) We present a novel blackbox mutational fuzzing technique            cates), such as f 2 ∨ f 3 , f 1 , f 2 , and f 3 in the figure. Initially, STORM
         for detecting critical bugs in SMT solvers.                         generates a random assignment of all free variables in the formulas
     (2) We implement our technique in a fuzzer that is already being        in S. Then, STORM recursively fragments the formulas in S into all
         used for testing new features of solvers before deployment.         their possible sub-formulas. For example, f is broken down into f 1
     (3) We evaluate the effectiveness of our fuzzer on seven mature         and f 2 ∨ f 3 , each of these is in turn broken down into its Boolean
         solvers and 43 logics. We found 29 previously unknown               sub-formulas, and so on. The valuation (i.e., truth value) of each
         critical bugs in three solvers (or nine solver variants) and 15     (sub-)formula, T or F , is computed based on the random assignment.
         different logics.                                                   All formulas together with their valuations are inserted in an initial
   Outline. The next section gives an overview of our approach.              pool as shown in the figure.
Sect. 3 explains the technical details, and Sect. 4 describes our               The second phase, formula generation, uses the formulas in the
implementation. We present our experimental evaluation in Sect. 5,           initial pool to build new formulas. The valuation of each new for-
discuss related work in Sect. 6, and conclude in Sect. 7.                    mula is computed based on the valuations of its constituent initial
                                                                             formulas. All new formulas with their valuations are inserted in
                                                                             a construction pool as shown in the figure. For instance, initial
2      OVERVIEW
                                                                             formulas f 2 and f 3 are used to construct a new formula f 2 ∧ f 3 .
To give an overview of our fuzzing technique for SMT solvers, we                The third phase, instance generation, uses formulas from both
first describe a few interesting examples of STORM in action and             pools to generate new SMT instances. The reason for having the
then explain what happens under the hood on a high level.                    two pools is to be able to control the frequency with which initial
   In action. One of the critical bugs1 found by STORM was in                and constructed formulas appear in the new instances. Instances
Z3’s QF_LIA logic, which stands for quantifier-free linear integer           generated during this phase have a different Boolean structure than
arithmetic. We opened a GitHub issue to report this bug, which re-           the seeds. However, their basic building blocks, that is, the initial
sulted in an eight-comment discussion between two Z3 developers              formulas that could not be fragmented further, remain unchanged.
on how to resolve it. The issue was closed but re-opened a day later         This allows STORM to generate realistic instances as we discuss
with more comments on what still needs to be fixed. The issue was            later in this section. In addition to being realistic, all new instances
closed for the last time three days after that. The fix in Z3 included       are also satisfiable by construction.
changing the implementation of Gomory’s cut.                                    Therefore, a critical bug is detected whenever an SMT solver
   Another critical bug2 was detected in Z3’s Z3str3 string solver [12].     returns unsat for a STORM-generated instance. In such a case,
According to a developer of Z3str3, the bug existed for a long time          STORM uses instance minimization to minimize the size of the
before STORM found it. During this time, it remained undetected              instance revealing the bug.

1 https://github.com/Z3Prover/z3/issues/2871
2 https://github.com/Z3Prover/z3/issues/2994                                 3 https://github.com/Z3Prover/z3/issues/3052
    Detecting Critical Bugs in SMT Solvers Using Blackbox Mutational Fuzzing



                                   Phase 1: Seed fragmentation                                               Phase 2: Formula               Phase 3: Instance
                                                                                                               generation                      generation
                                                    ∧
               assert f                                                                                                                      assert ¬f2
                                                                                    f:F                               f2 ∧ f3:F
                                              f1          ∨                                                 ¬f1:T                            assert ¬f1 ∧ f3
                                                                               f1:F f2:F                        ¬f2:T      ¬f1 ∧ f3:T
               check-sat                                                                      f3:T                                           check-sat
                                                                                  f2 ∨ f3:T                     ¬(¬f1 ∧ f2):T
                                                    f2           f3
                  Seed S                       Formula f                        Initial pool                 Construction pool                New instance


                                                         Figure 1: Overview of the three STORM phases.

1 ( declare-const S String )
                                                                                              ( declare-const S String )
                                                                                              1
2 ( assert ( str . in . re S ( re .++ re . allchar ( re .++
                                                                                              ( assert
                                                                                              2
3    ( str . to . re "7;") ( re .++ re . allchar
                                                                                            3 ( let (( a ( str . in . re S ( re .++ re . allchar ( re .++
4       ( str . to . re " aa "))))))
                                                                                            4    ( str . to . re "7;") ( re .++ re . allchar
5 ( assert ( not ( str . in . re S ( re . union re . allchar
                                                                                            5       ( str . to . re " aa "))))))
6    ( str . to . re "X ' jafa ")))))
                                                                                            6 ( let (( b ( not ( str . in . re S ( re . union re . allchar
7 ( check-sat )
                                                                                            7    ( str . to . re "X ' jafa "))))))
                                                                                            8 ( let (( c ( and ( not b ) ( not a ))))
                                                                                            9 ( not c ))))))
                                                                                           10 ( check-sat )




    Figure 2: Original seed instance from SMT-COMP 2019 on the left, and simplified instance revealing critical bug in Z3’s Z3str3
    string solver on the right.

1   ( declare-fun A () Bool )                                                                 1   ( declare-fun A () Bool )
2   ( declare-fun B () Bool )                                                                 2   ( declare-fun B () Bool )
3                                                                                             3
4 ( assert ( not B ))                                                                         4   ( assert ( and ( not B ) A ))
5 ( assert ( not ( and ( not A ) B )))                                                        5
6 ( assert A)                                                                                 6   ( check-sat-using dom-simplify )
7
8   ( check-sat-using dom-simplify )


    Figure 3: Simplified instance revealing critical bug in Z3’s dom-simplify tactic on the left, and logically equivalent instance
    not revealing the bug on the right.


       Examples. The left of Fig. 2 shows a seed instance from the                                described earlier. It essentially checks the satisfiability of ¬B ∧
    international SMT competition SMT-COMP 2019 [3]. Starting from                                ¬(¬A ∧ B) ∧ A, which is logically equivalent to ¬B ∧ A. Observe,
    this seed, STORM generated the (simplified) instance on the right,                            however, that the logically equivalent formula, shown on the right
    which revealed the critical bug in Z3str3 described above. Z3str3                             of Fig. 3, does not trigger the bug.
    derives length constraints from regular-expression membership                                    Consequently, the benefit of fuzzing the Boolean structure of
    predicates. The bug that STORM exposed here is that such a length                             seed instances is two-fold. First, it is effective in detecting critical
    constraint, which is implied by membership in a regular expression,                           issues in solvers. Such issues are by definition far more serious
    was not asserted by the string solver.                                                        and complex than other types of bugs, such as crashes, since they
       It is easy to see that the first asserted formula on the left corre-                       can, for instance, result in verifying incorrect safety-critical code.
    sponds to variable a on the right, while the second asserted formula                          Second, fuzzing only the Boolean structure of seeds helps generate
    on the left corresponds to variable b on the right. Therefore, the                            realistic SMT instances. This is confirmed by the above comments
    seed essentially checks for satisfiability of a ∧ b. On the right, c                          on the tactic bug from the Z3 developer who thought that the
    is equivalent to ¬a ∧ ¬b, and the instance checks for satisfiability                          STORM instance was generated by his own PhD tool. This was also
    of ¬c, thus, of a ∨ b. This shows that even small mutations to the                            confirmed by other solver developers with whom we interacted.
    Boolean structure of a formula can be effective in revealing critical
    issues in solvers.                                                                            3   OUR APPROACH
       This is also evidenced by the example in Fig. 3. The instance
    on the left reveals the critical bug in Z3’s dom-simplify tactic                              In this section, we describe our fuzzing technique and how it solves
                                                                                                  two key challenges in detecting critical bugs in SMT solvers: (1) how
                                                                           Muhammad Numair Mansur, Maria Christakis, Valentin Wüstholz, and Fuyuan Zhang


to generate non-trivial SMT instances, and (2) how to determine              Algorithm 1: Core fuzzing procedure in STORM.
if a critical bug is exposed. The latter demonstrates how STORM                 1 procedure PopulateInitialPool(S, Dmax )
addresses the oracle problem [9] in the context of soundness testing            2   A ← GetAsserts(S)
for solvers. Finally, we describe how we minimize bug-revealing in-             3   M ← RandAssignment(A)
stances to reduce their size. This step is crucial for solver developers        4   P ← EmptyPool()
as it significantly facilitates debugging.                                      5   foreach pred ∈ S
                                                                                6     if ¬ExceedsDepth(pred, Dmax ) then
                                                                                7        v ← IsTrue(M, pred)
3.1    Fuzzing Technique                                                        8        P ← Add(P, pred, v)
Given an SMT instance as seed input, our fuzzing approach pro-                  9   return P
                                                                               10
ceeds in three main phases: (1) seed fragmentation, (2) formula
                                                                               11 procedure Fuzz(S, NC, NM, Dmax , Amax )
generation, and (3) instance generation. Seed fragmentation ex-                12   // Phase 1: Seed fragmentation
tracts sub-formulas from the seed. These will be used as building              13   Pinit ← PopulateInitialPool(S, Dmax )
blocks for generating new formulas in the second phase. Lastly,                14
instance generation creates new, satisfiable SMT instances based               15   // Phase 2: Formula generation
on the generated formulas, invokes the SMT solver under test on                16   Pconstr ← EmptyPool()
each of these instances, and uses the solver result as part of the test        17   while Size(Pconstr ) < NC do
oracle to detect critical bugs.                                                18      f1, v1 ← RandFormula(Pinit, Pconstr )
    Alg. 1 describes these three phases in detail. Function Fuzz takes         19      op ← RandOp()
the initial seed S and several additional parameters that bound                20      if op = AND then
                                                                               21         f2 , v2 ← RandFormula(Pinit, Pconstr )
the fuzzing process (explained below). As a first step, the function
                                                                               22         f ← AND(f1, f2 )
populates an initial pool Pinit of formulas (line 13) with formula             23         v ← v1 ∧ v2
fragments of the seed S.                                                       24      else
    To this purpose, function PopulateInitialPool extracts all as-             25         f ← NOT (f1 )
sertions in the seed and generates a random assignment M, i.e.,                26         v ← ¬v1
an assignment of values to free variables. In our implementation,              27      if ¬ExceedsDepth(f , Dmax ) then
we use a separate SMT solver (i.e., different from the one under               28         Pconstr ← Add(Pconstr, f, v)
test) to generate a model for the assertions (or their negation if the         29
assertions are unsatisfiable). Next, we iterate over all predicates            30   // Phase 3: Instance generation
(i.e., tree-shaped Boolean sub-formulas as in Fig. 1) in the seed. We          31   B ← EmptyList()
use assignment M to evaluate those predicates for which the tree               32   m←0
depth does not exceed a bound Dmax . This valuation v is crucial               33   while m < NM do
for subsequent phases of the fuzzing process, and we add both                  34      // Number of generated assertions
                                                                               35      ac ← (RandInt() % Amax ) + 1
the formula pred and v to the initial pool, which is essentially a
                                                                               36      A ← EmptyList()
map from formulas to valuations. Note that, by fragmenting the                 37      while 0 < ac do
seed, the initial pool already contains a large number of non-trivial          38         f , v ← RandFormula(Pinit, Pconstr )
formulas that would be difficult to generate from scratch (e.g., with          39         if ¬v then
a grammar-based fuzzer).                                                       40             // Negation of f to guarantee assertion satisfiability
    In the second phase, we populate the construction pool Pconstr by          41             f ← NOT (f )
adding NC new formulas of maximum depth Dmax . These formulas                  42         A ← Append(A, f)
are generated randomly by selecting one of two Boolean operators,              43         ac ← ac − 1
logical AND (lines 21–23) and NOT (lines 25–26). Note that this set            44      // Invocation of SMT solver under test
of operators is functionally complete, thus allowing us to generate            45      r ← CheckSAT(A)
any Boolean formula. We construct a new formula by conjoining                  46      // Test oracle
two existing formulas in the case of AND and negating an exist-                47      if r = UNSAT then
                                                                               48         B ← Append(B, A)
ing formula in the case of NOT . Existing formulas are randomly
                                                                               49      m←m+1
selected from the pools. Before adding the resulting formula to the
                                                                               50   return B
construction pool, we derive its valuation v from the valuations of
its sub-formulas (lines 23 and 26).
    In essence, the second phase enriches the set of existing formulas
by generating new ones without requiring a complete grammar for              generating the formulas on lines 8 and 9 that ultimately amount to
all syntactic constructs. Instead, we use a minimal, but functionally        checking the satisfiability of a ∨ b.
complete, grammar for Boolean formulas. This significantly simpli-              Once the two pools are populated, we use them to generate NM
fies formula generation without sacrificing expressiveness. Note             SMT instances that we feed to the solver under test. To assemble
that a separate pool for newly constructed formulas allows having            a new instance, we create a random number of assertions (ac on
control over how many of them are used in the instances generated            line 35) by randomly picking formulas from the pools. If the valua-
in the third phase. On the right of Fig. 2, this step is responsible for     tion of a selected formula is true, we directly assert it, otherwise we
Detecting Critical Bugs in SMT Solvers Using Blackbox Mutational Fuzzing


Algorithm 2: Depth-minimization procedure in STORM.                        4     IMPLEMENTATION
  1 procedure MinimizeDepth(S, NC, NM, Dmin, Dmax , Amax )                    Seeds. STORM uses the Python API in Z3 to manipulate SMT
  2   if Dmax ≤ Dmin then                                                  formulas for generating new instances. It can, therefore, only fuzz
  3      return S                                                          instances within the logics supported by Z3. In practice, this is not
  4   D ← (Dmin + Dmax )/2                                                 an important restriction since Z3 supports a very large number
  5   B ← Fuzz(S, NC, NM, D, Amax )
                                                                           of logics. Moreover, STORM requires seeds to be expressed in an
  6   if 0 < Size(B) then
                                                                           extension of the SMT-LIB v2 input format [4] supported by Z3. Note
  7      Smin ← SelectSeedWithSmallestDepth(B)
  8      return MinimizeDepth(Smin, NC, NM, Dmin, D, Amax )                that SMT-LIB is the standard input format used across solvers.
  9   return MinimizeDepth(S, NC, NM, D + 1, Dmax , Amax )                    Random assignments. Recall that STORM uses Z3 to generate
                                                                           a random model for a given seed (line 3 of Alg. 1). Note, however,
                                                                           that bugs in Z3 resulting in a wrong model do not affect our fuzzer.
                                                                           In fact, given any assignment, our technique just requires correct
                                                                           valuations for predicates in the initial pool. In theory, computing
assert its negation. This ensures that all assertions are satisfiable.     these valuations is relatively straightforward since the assignment
Of course, the same holds for the SMT instance consisting of these         provides concrete values for all free variables; simply substituting
assertions in addition to a satisfiability check. We now leverage this     variables with values should be sufficient for quantifier-free predi-
fact when feeding the SMT instance to the solver under test (line 45).     cates. In practice, we use Z3 to compute predicate valuations and
The oracle reveals a critical bug if the solver returns UNSAT .            have not encountered any bugs in this solver component.
                                                                              Random choices. Our implementation provides concrete in-
3.2     Instance Minimization                                              stantiations of functions RandOp and RandFormula from Alg. 1
                                                                           as follows. RandOp returns AND with probability 50% and NOT
In practice, our fuzzing technique often generates bug-revealing
                                                                           otherwise. Function RandFormula selects a formula from one of
instances that are very large, containing deeply nested formulas
                                                                           the pools uniformly at random, but with probability 30% from the
and several assertions. This can considerably complicate debugging
                                                                           initial pool and from the construction pool otherwise.
for solver developers.
   Adapting established minimization techniques based on delta                Incremental mode. Many solvers support a feature called in-
debugging [46] might seem like a natural fit for this use case. How-       cremental mode. It allows client tools to push and pop constraints
ever, the special nature of critical bugs complicates this task in         when performing a large number of similar satisfiability queries
comparison to other classes of bugs, such as crashes. For mini-            (e.g., checking feasibility of paths with a common prefix during sym-
mizing crashing instances, it is sufficient to minimize the original       bolic execution). To efficiently support this mode, solvers typically
instance (e.g., by dropping assertions) while preserving the crash. In     use dedicated algorithms that reuse results from previous queries;
contrast, for instances that exhibit a critical bug, the behavior that     in fact, SMT-COMP [3] features a separate track to evaluate these
should be preserved is more involved, that is, the instance should         algorithms. To test incremental mode, STORM is able to generate
be minimized such that the buggy solver still returns unsat while          SMT instances that contain push and pop instructions in addition
the ground truth remains sat. This requires either satisfiability-         to regular assertions.
preserving minimizations or a trusted second solver that can act
as a ground-truth oracle by rejecting minimizations that do not            5     EXPERIMENTAL EVALUATION
preserve satisfiability. Unfortunately, the only state-of-the-art delta    In this section, we address the following research questions:
debugger for SMT instances, ddSMT [41], does not preserve satisfi-
ability. (Note that ddSMT is the successor of deltaSMT [2], which                RQ1: How effective is STORM in detecting new critical bugs
was used to minimize instances generated by FuzzSMT [15].) More-                   in SMT solvers?
over, a second trusted solver is not always available (e.g., for new             RQ2: How effective is STORM in detecting known critical bugs
theories or solver-specific features and extensions).                              in SMT solvers?
   To overcome these limitations, we developed a specialized mini-               RQ3: How do the assertion and depth bounds of STORM im-
mization technique that directly leverages the bounds of our fuzzing               pact its effectiveness?
procedure to obtain smaller instances (see Alg. 2 for depth mini-                RQ4: How effective is our instance minimization at reducing
mization). By repeatedly running the fuzzing procedure on a buggy                  the size of bug-revealing instances?
seed instance, this algorithm attempts to find the minimum values                RQ5: To what extent do STORM-generated instances increase
for Dmax and Amax that still reveal a critical bug. It uses binary                 code coverage of SMT solvers?
search to first minimize the number of assertions (analogous to
MinimizeDepth in Alg. 2) and subsequently the depth of asserted            5.1     Solver Selection
formulas. Note that the fuzzing procedure may report multiple              We used STORM to test seven popular SMT solvers, which sup-
bug-revealing instances, and we recursively minimize the smallest          port the SMT-LIB input format [4] and regularly participate in the
with respect to the bound being minimized (line 8). Our evaluation         international SMT competition SMT-COMP [3]. Specifically, we se-
shows that this technique works more reliably than leveraging              lected Boolector [14], CVC4 [10], MathSAT5 [21], SMTInterpol [20],
ddSMT and a second solver (see Sect. 5.5).                                 STP [30], Yices2 [27], and Z3 [25].
                                                                         Muhammad Numair Mansur, Maria Christakis, Valentin Wüstholz, and Fuyuan Zhang


   In addition to the above mature implementations, STORM was              for the extension that allows free sort and function symbols, S for
also used to test new features of solvers. In particular, the develop-     strings, and DT for datatypes.
ers of Yices2 asked us to test the new bitvector theory in the MCSAT
solver [32] of Yices2, which is based on the model-constructing            5.3     Benchmark Selection
satisfiability calculus [26]. MCSAT is an optional component of
                                                                           For our experiments, we used as seeds all non-incremental SMT-
Yices2, which is dedicated to quantifier-free non-linear real arith-
                                                                           LIB instances in SMT-COMP 2019 [3]. We also used all SMT-LIB
metic. STORM did not find bugs in this new theory of MCSAT, and
                                                                           instances in the regression test suites of CVC4, Yices2, and Z3. The
the theory was integrated with the main version of Yices2 shortly
                                                                           second column of Tab. 2 shows how many seeds correspond to each
after. In our experimental evaluation, it is therefore tested as part
                                                                           tested logic. The second to last row of the table (“Unsp.”) refers to
of Yices2.
                                                                           instances in which the logic is unspecified—the solver may use any.
   Moreover, the developers of Z3 asked us to test a new arithmetic
                                                                              In general, we only tested each solver with logics, and thus
solver (let us refer to it as Z3-AS), which they have been preparing
                                                                           instances, it supports. For seeds without a specified logic, we only
for the last two years. It comes with better non-linear theories and
                                                                           generated mutations of those that each solver could handle.
has just replaced the legacy arithmetic solvers in Z3. According to
the Z3 developers, STORM could help expedite the integration of
this new feature by finding bugs early, which it did. Since Z3-AS          5.4     Experimental Setup
has just now been integrated with the current version of Z3 and we         For our experiments, we used the following setting for STORM
have only been testing it independently, we include it separately in       unless stated otherwise: Dmax = 64, Amax = 64, NC between 200
our evaluation.                                                            and 1500, and NM between 300 and 1000 (see Alg. 1). Both NC and
   Due to the success of STORM in detecting intricate critical bugs        NM were adjusted dynamically within the above ranges based on
in Z3-AS, the Z3 developers described our fuzzer as being “extremely       the size of the initial pool. The goal was to use larger values for
useful” and have now asked us to test Z3’s current debug branch            larger initial pools, and thus, larger seeds.
(let us refer to it as Z3-DBG). Z3-DBG implements a variety of new            We performed all experiments on a 32-core Intel ® Xeon ® E5-
solver features in which STORM has already detected a critical bug         2667 v2 CPU @ 3.30GHz machine with 256GB of memory, running
(see Sect. 5.5).                                                           Debian GNU/Linux 10 (buster).
   Finally, the developers of the Z3str3 string solver [12] asked us
to provide them with STORM-generated string instances. They                    Comparison with state of the art. Except for a single tool [17],
became aware of STORM since it detected several critical issues            all existing testing tools for SMT solvers do not use oracles to detect
in Z3str3, which we reported. Note that Z3str3 is developed by             critical bugs. They, therefore, require differential testing of multiple
the same group of people as StringFuzz [13]. We, therefore, sus-           solvers to identify such bugs. In RQ2, we evaluate the effectiveness
pect that STORM found bugs in Z3str3 that StringFuzz could not             of STORM at detecting existing critical bugs, including the only
find, especially since StringFuzz does not target critical bugs. The       publicly reported one found by the most closely related tool [17].
STORM-generated instances that we provided (in addition to the             Recall that this tool supports only the theory of strings.
bug-revealing ones that we reported) were used as a regression
test suite during the development of performance enhancements              5.5     Experimental Results
in Z3str3. According to a developer of Z3str3, our instances helped        We now discuss our experimental results for each of the above
reveal critical bugs introduced by these enhancements. Most of             research questions.
these bugs were due to missing or incorrect axioms in Z3str3.
                                                                              RQ1: New critical bugs. Tab. 3 shows critical bugs found by
                                                                           STORM in the SMT solvers we tested. The first column of the table
                                                                           shows the solvers. We list Z3str3 separately as it is not the default
5.2    Logic Selection                                                     string solver in Z3. The second column denotes whether bugs were
In our experimental evaluation, for each solver, we test the inter-        found in the incremental mode of a solver, which essentially corre-
section of all logics supported by the solver, all logics supported        sponds to a different solver variant. The third column lists the logics
by the SMT-LIB input format, and all logics supported by Z3. The           in which bugs were found, and the last column shows the number of
latter constraint emerges because our implementation relies on Z3          bugs. Overall, STORM found 29 critical bugs in three mature
for generating the mutated SMT instances (see Sect. 4).                    solvers (or nine solver variants) and 15 different logics.
   Tab. 2 shows the tested logics for each solver. (The second co-            All of these bugs are previously unknown, unique, and confirmed
lumn and second to last row of the table should be ignored for             by the solver developers. Out of the 29 critical bugs, 19 have already
now.) The logic abbreviations are explained in the SMT-LIB stan-           been fixed in the latest solver versions. Note that the bugs were only
dard [4], but generally speaking, the following rules hold. QF stands      detected by STORM-generated instances, i.e., none were detected
for quantifier-free formulas, A for arrays, AX for arrays with ex-         by the seeds. In addition to the bugs in the table, STORM was also
tensionality, BV for bitvectors, FP for floating-point arithmetic, IA      able to detect known bugs as well as other issues (i.e., of classes C
for integer arithmetic, RA for real arithmetic, IRA for integer real       and D) as a by-product, which we do not report here.
arithmetic, IDL for integer difference logic, RDL for rational diffe-         The feedback we receive from solver developers is very positive,
rence logic, L before IA, RA, or IRA for the linear fragment of these      and we have been discussing it throughout the paper. As another
arithmetics, N before IA, RA, or IRA for the non-linear fragment, UF       example, a Yices2 developer told us that STORM found real bugs
Detecting Critical Bugs in SMT Solvers Using Blackbox Mutational Fuzzing


                                                                                     SMT Solvers
                               Logic        Seeds      Boolector      CVC4      MathSAT5 SMTInterpol       STP    Yices2   Z3
                             ALIA               42                         ✓                     ✓                         ✓
                             AUFNIA              3                         ✓                                               ✓
                             LRA              2444                         ✓                     ✓                         ✓
                             QF_ALIA            42                         ✓                     ✓                  ✓      ✓
                             QF_AUFNIA           3                         ✓       ✓                                       ✓
                             QF_DT            1602                         ✓                                               ✓
                             QF_LRA           1049                         ✓                     ✓                  ✓      ✓
                             QF_RDL            261                         ✓                                        ✓      ✓
                             QF_UFIDL          444                         ✓                                        ✓      ✓
                             QF_UFNRA           38                         ✓       ✓                                ✓      ✓
                             UFDTLIA           327                         ✓                                               ✓
                             AUFDTLIA          728                         ✓                                               ✓
                             AUFNIRA          1490                         ✓                                               ✓
                             NIA                14                         ✓                                               ✓
                             QF_ANIA             8                         ✓       ✓                                       ✓
                             QF_AX             555                         ✓       ✓             ✓                  ✓      ✓
                             QF_FP           40418                         ✓       ✓                                       ✓
                             QF_NIA          23901                         ✓       ✓                                ✓      ✓
                             QF_S            24323                         ✓                                               ✓
                             QF_UFLIA          580                         ✓                     ✓                  ✓      ✓
                             UFLIA            9524                         ✓                     ✓                         ✓
                             AUFLIA           3273                         ✓                     ✓                         ✓
                             BV               5750         ✓               ✓                                               ✓
                             NRA              3813                         ✓                                               ✓
                             QF_AUFBV           49         ✓               ✓                                        ✓      ✓
                             QF_BV            3872         ✓               ✓                                ✓       ✓      ✓
                             QF_IDL            843                         ✓                     ✓                  ✓      ✓
                             QF_NIRA             3                         ✓       ✓                                ✓      ✓
                             QF_UF            7481                         ✓                     ✓                  ✓      ✓
                             QF_UFLRA          936                         ✓                     ✓                  ✓      ✓
                             UF               7596                         ✓                     ✓                         ✓
                             UFLRA              17                         ✓                     ✓                         ✓
                             AUFLIRA          2268                         ✓                     ✓                         ✓
                             LIA               388                         ✓                     ✓                         ✓
                             QF_ABV           8310         ✓               ✓                                        ✓      ✓
                             QF_AUFLIA        1310                         ✓                     ✓                         ✓
                             QF_BVFP         17196                         ✓       ✓                                       ✓
                             QF_LIA           2104                         ✓                     ✓                  ✓      ✓
                             QF_NRA           4067                         ✓       ✓                                ✓      ✓
                             QF_UFBV          1238         ✓               ✓                                        ✓      ✓
                             QF_UFNIA          478                         ✓       ✓                                ✓      ✓
                             UFDT             4527                         ✓                                               ✓
                             UFNIA            4446                         ✓                                               ✓
                             Unsp.            5825          –              –       –             –          –       –      –
                             Total         193586           5              43      10           17          1       19     43

                              Table 2: The tested logics per solver and the number of seed instances per logic.



and that it is especially useful to have the ability to test the incre-             however, does not target critical bugs, and for this reason, they
mental mode of solvers. He also mentioned that they used to run                     run VoteSMT [6] to differentially test solvers and detect incorrect
FuzzSMT [15] on all theories, and that now this fuzzer runs conti-                  Yices2 results. Despite this, STORM detected four new critical bugs
nuously on new theories generating “infinite” instances. FuzzSMT,                   in Yices2.
                                                                          Muhammad Numair Mansur, Maria Christakis, Valentin Wüstholz, and Fuyuan Zhang


            SMT        Incremental                  Critical                all bug-revealing instances against the first solver version with the
                                         Logics
           Solver         Mode                       Bugs                   corresponding fix. If the solver now returned sat for at least one
                                                                            of the instances, we counted the bug as reproduced.
                                         QF_FP
         MathSAT5                                       2                       For each of the three solvers, STORM was able to reproduce 1
                                         QF_BVFP
                                                                            (CVC4), 1 (Yices2), and 4 (Z3) critical bugs, so 6 out of a total of
                                         QF_UFIDL                           21. Therefore, if STORM had run on these solver versions, it
           Yices2                                       2
                                         QF_UF                              would have prevented approximately 1/3 of the critical-bug
                                         QF_UFIDL
                                                                            reports in a three-month period. Given that during this period
           Yices2             ✓                         2                   we reported 10 additional bugs detected by STORM in these solvers,
                                         QF_UFLRA
                                                                            it is possible that our fuzzer would have been able to reproduce
                                         QF_UFLIA                           more bugs if it had run longer or if it was being run continuously.
                                         QF_BV                                  We also tried to find the bugs reported by Bugariu and Müller [17]
                                         UF                                 (regardless of when they were reported). There was only one GitHub
             Z3                                         8
                                         LIA                                issue opened by these authors about a critical bug, namely in the
                                         QF_BVFP                            Z3str3 string solver. STORM was able to reproduce this bug.
                                         QF_LIA
                                                                               RQ3: Fuzzing bounds. To evaluate the effect of the fuzzing
                                         QF_FP
             Z3               ✓                         3                   bounds of STORM, we only considered closed bugs. We used all
                                         QF_S
                                                                            19 closed bugs reported by us from RQ1 except for those in Z3-AS
           Z3str3                        QF_S           6                   (the original commits could not be retrieved due to a rebase in
                                                                            the branch) for a remaining of 14 bugs. In addition, we used all 7
                                         AUFNIRA
                                                                            reproduced bugs (including the one reported by Bugariu et. al. [17])
                                         QF_NIA
           Z3-AS                                        4                   from RQ2 for a total of 21 bugs.
                                         AUFLIRA
                                                                               For each of these bugs we randomly selected a seed file that had
                                         QF_NRA
                                                                            allowed STORM to detect the bug in RQ1 or RQ2. We performed
           Z3-AS              ✓          AUFNIRA        1                   eight independent runs of STORM (with random seeds different
          Z3-DBG                         QF_NIA         1                   from the ones used in RQ1 and RQ2 to avoid bias) to evaluate
                                                                            the effect of the different fuzzing bounds. None of the STORM
Table 3: Previously unknown, unique, and confirmed critical                 configurations was able to reproduce two of the Yices2 bugs from
bugs found by STORM in the tested SMT solvers.                              RQ1 with any of the eight random seeds; we therefore do not include
                                                                            those in the results shown in Fig. 4.
                                                                               For the assertion and depth bounds Amax and Dmax , we used
   Another Yices2 developer commented on the severity of two of             five different settings: 4, 8, 16, 32, and 64. Fig. 4 shows the median
the bugs that STORM found. He mentioned that one was in the                 number of iterations (i.e., generated instances) until the bug was
pre-processing component and “easy to fix (and an obvious mistake           found for different combinations of these settings. We can observe
in retrospect) but it was in a part of Yices that had probably not been     that a large assertion bound reduces the number of iterations
exercised much”. “The other one was much more tricky to trace and           significantly (e.g., up to 11x for Dmax = 4). In contrast, the trend
fix, it was related to a combination of features and optimization in        for the depth bound is less clear, which suggests that it has a less
the E-graph, not localized to a single module”.                             significant effect and is mostly useful for minimizing instances. We
                                                                            can observe very similar trends when comparing the median time
    RQ2: Known critical bugs. In this research question, we evalu-
                                                                            to find the bug (see Fig. 5).
ate the effectiveness of STORM in reproducing known critical bugs.
We, therefore, collected all critical bugs that were reported for the          RQ4: Instance minimization. We now evaluate the effective-
solvers under test during the three-month period between Nov 15             ness of our instance minimization. To this end, we collect all in-
and Feb 15, 2020. We focused only on bugs with a subsequent fix             stances revealing the 19 bugs of RQ3 that are generated by STORM
(i.e., closed issues on GitHub). Out of the seven solvers, we exclude       with its default configuration (Sect. 5.4).
MathSAT5 because it is closed source, and bugs may only be re-                 The results of minimizing these instances using binary search
ported via email. We also exclude Boolector, SMTInterpol, and STP           (BS) and delta debugging (ddSMT [41]) are shown in Tab. 4. Instance
because no critical bugs were reported for these solvers during the         size is measured in terms of the number of bytes, the number of
above time period. For the remaining three solvers, CVC4, Yices2,           assertions, and the maximum formula depth in an assertion. A dash
and Z3, there were 6, 1, and 14 critical bugs with a fix, respectively,     for ddSMT means either that the instance could not be minimized
after excluding all the bugs that we reported.                              or that ddSMT does not support a construct in the instance. As
    We ran STORM on the solver version in which each bug was                outlined in Sect. 3.2, we had to adapt ddSMT for this use case by
found. Since developers typically add fixed bugs to their regression        invoking a second solver to reject minimizations that would not
tests, we removed all seeds that revealed any of these bugs (without        preserve satisfiability; we used the version of the solver that fixed
being mutated). We collected all generated instances for which              the corresponding bug for this purpose.
each solver incorrectly returned unsat. To ensure that STORM                   Despite these adaptations, we observed that ddSMT could not
actually found the reported bug (and not a different one), we ran           minimize the instances for bugs 2, 3, 4, 5, 13, 14, and 18. We suspect
Detecting Critical Bugs in SMT Solvers Using Blackbox Mutational Fuzzing


                                                1,000
                                                                                                                                                                                                                                                4       8            16             32              64
     Number of iterations to bug


                                                                                                                                                                                                        Depth bound Dmax

                                                                                         737.90
                                                 750                           678.30
                                                           662.60
                                                                     612.20                        633.30



                                                 500                                                         461.60
                                                                                                                       434.60
                                                                                                                                 392.80 387.30 409.30                      387.10
                                                                                                                                                          360.60 359.10
                                                                                                                                                                                     315.70
                                                                                                                                                                                               251.50
                                                 250                                                                                                                                                        195.20
                                                                                                                                                                                                                                    149.30
                                                                                                                                                                                                                      109.00 130.00        121.30                                 116.70               100.10
                                                                                                                                                                                                                                                                         83.50              66.25
                                                                                                                                                                                                                                                             60.00

                                                      0
                                                                                   4                                                 8                              16                                                        32                                                   64
                                                                                                                                                          Assertion bound Amax
Figure 4: Median number of iterations to find bugs with different configurations of STORM. Each bar corresponds to a confi-
guration with a certain depth and assertion bound.
                                                                                        59.20
                                                 60                                                                                                                                                   Depth bound Dmax                      4       8              16             32              64
                     Time to bug (in seconds)




                                                                              51.10               51.70     50.60
                                                 50       44.60
                                                                    46.10                                                                        45.40
                                                                                                                      44.30
                                                                                                                                         41.50
                                                                                                                                39.50
                                                 40
                                                                                                                                                         29.50            30.90
                                                 30                                                                                                              25.40              26.80
                                                                                                                                                                                              24.80

                                                 20                                                                                                                                                        15.50
                                                                                                                                                                                                                                    17.40   16.60
                                                                                                                                                                                                                                                                                 12.40
                                                                                                                                                                                                                            10.60
                                                                                                                                                                                                                                                                                                    9.00
                                                 10                                                                                                                                                                  7.90
                                                                                                                                                                                                                                                            5.80
                                                                                                                                                                                                                                                                        7.80               6.60


                                                  0
                                                                               4                                                 8                                 16                                                       32                                                   64
                                                                                                                                                         Assertion bound Amax
Figure 5: Median time (in seconds) to find bugs with different configurations of STORM. Each bar corresponds to a confi-
guration with a certain depth and assertion bound.

that its search space of possible minimizations might not contain                                                                                                               We selected one of the solvers (Z3) and four random logics in
more complex transformations that would be required to both pre-                                                                                                             which we found bugs (QF_UFLIA, AUFNIRA, UF, LIA). We then
serve satisfiability and the bug. We observed the same outcome                                                                                                               computed the line and function coverage when running Z3 on all
when running ddSMT on instances that were first minimized using                                                                                                              the instances from SMT-COMP 2019 [3] for these logics (10054
binary search.                                                                                                                                                               seeds). The result is shown in the first row of Tab. 5. At the same
   For bugs 10 and 11, ddSMT does not support str . to . re, which                                                                                                           time, we randomly selected 5 instances from each logic and ran
is supported by Z3’s Z3str3 solver. For the remaining bugs (7, 8,                                                                                                            STORM with N M = 500 and a single new random seed to ge-
9, 12, 15, and 16), ddSMT does not support check-sat-using,                                                                                                                  nerate exactly 500 new instances for each of the 20 seed instances.
which is supported by Z3. Recall that STORM accepts seed instances                                                                                                           Tab. 5 shows that, as more instances are generated, coverage in-
expressed in the extension of the SMT-LIB format that is supported                                                                                                           creases noticeably (2958 more lines and 1149 more functions after
by Z3 (Sect. 4), whereas ddSMT only supports the standard.                                                                                                                   only 500 generated instances). This demonstrates that running
   Overall, this experiment shows that our minimization proce-                                                                                                               STORM on only a small number of seed instances is able to
dure works more reliably and is able to significantly reduce                                                                                                                 result in a noticeable coverage increase over a large number
buggy instances (median reduction of 86.1%). However, for the                                                                                                                of instances from a well known benchmark set.
cases where both procedures produced results, the ddSMT-based
minimization procedure was able to produce smaller instances.                                                                                                                5.6              Threats to Validity
This is not entirely surprising given that BS uses the fuzzer, which
                                                                                                                                                                             We identify the following threats to the validity of our experiments.
treats predicates not containing other predicates (i.e., ground- or
leaf-predicates) as atomic building blocks. For instance, for Bug 17,                                                                                                           Selection of seeds. STORM requires seed instances as input,
the instance that was minimized with BS contains several complex                                                                                                             and our experimental results do not necessarily generalize to other
ground-predicates that ddSMT is able to minimize further. We ex-                                                                                                             seeds [43]. However, we selected as seeds all supported instances
pect that more involved combinations of the two approaches could                                                                                                             from SMT-COMP 2019 [3] as well as regression test suites of solvers.
produce even better results.                                                                                                                                                 We believe that our selection is sufficiently broad to mitigate this
                                                                                                                                                                             threat.
   RQ5: Code coverage. A Yices2 developer mentioned that they
use fuzzer-generated instances to enrich their regression tests such                                                                                                            Selection of solvers. The bugs found by STORM depend on the
that they achieve higher coverage. In this research question, we                                                                                                             solvers and logics that we tested. However, we selected a wide
therefore evaluate whether STORM is able to increase coverage.                                                                                                               range of different, mature solvers and logics to mitigate this threat.
                                                                         Muhammad Numair Mansur, Maria Christakis, Valentin Wüstholz, and Fuyuan Zhang


    Bug    Unminimized            Minimized         Minimized                              Generated         Line         Function
     ID     Instances               by BS           by ddSMT                               Instances       Coverage       Coverage
      1   56832/    51/   12    11687/   38/    6   272/   3/   3                                 0           43607          21238
      2   11623/    30/    2     7541/   24/    2     –/   –/   –                               100           45433          22005
      3   15156/    30/    2     5663/   24/    2     –/   –/   –                               200           45575          22067
      4   73656/    63/    3    12983/   15/    1     –/   –/   –                               300           45582          22068
      5   75040/    54/   10    15972/   50/    3     –/   –/   –                               400           46402          22369
      6   54326/    27/    4     8466/    6/    3   507/   3/   1                               500           46565          22387
      7   13160/    37/    5     1253/    5/    3     –/   –/   –
      8    9301/    26/    2      629/    3/    2     –/   –/   –          Table 5: Code coverage increase as more instances are gene-
      9    8209/    21/    6     1138/    3/    3     –/   –/   –          rated by STORM.
     10     401/     1/    1      401/    1/    1     –/   –/   –
     11   15322/    33/    4     8342/   16/    3     –/   –/   –          detect critical bugs. In contrast to both FuzzSMT and StringFuzz,
     12   13682/    40/    3      282/    1/    2     –/   –/   –          the satisfiability of all STORM-generated instances is known.
     13    8677/    57/    2      660/    4/    1     –/   –/   –             Recently, Bugariu and Müller [17] proposed an automated testing
     14   12294/    32/    3     1698/    6/    2     –/   –/   –          technique that synthesizes small SMT instances for the string the-
     15   26110/    23/    4     1171/    1/    2     –/   –/   –          ory. The true satisfiability of the generated instances is derived by
     16   55423/    29/    5    22660/   12/    2     –/   –/   –          construction and used as a test oracle. In contrast, STORM performs
     17   96844/    55/   59     2204/    4/    2   260/   1/   1          mutational fuzzing and supports a wide range of theories.
     18   20282/    38/    4      791/    4/    1     –/   –/   –             Unlike the above approaches that fuzz the input instances of
     19    7117/    22/    4      384/    1/    1   172/   1/   1          solvers, Artho et al. [7] and Niemetz et al. [42] develop model-based
                                                                           API testing frameworks for SAT and SMT solvers. These focus on
Table 4: Size of original and minimized bug-revealing in-                  testing various API parameters and solver options.
stances. Instance size is shown in terms of the number of
bytes / number of assertions / maximum formula depth.                         Testing program analyzers. Kapus and Cadar [33] combine
                                                                           random program generation with differential testing [40] to find
                                                                           bugs in symbolic-execution engines. Their technique is inspired by
   Randomness in fuzzing. A common threat when evaluating                  existing compiler-testing techniques (e.g., Csmith [45]) and used to
fuzzers is related to the internal validity [43] of their results. To      test KLEE [19], CREST [1], and FuzzBALL [39].
mitigate systematic errors that may be introduced due to random               Cuoq et al. [24] use randomly generated programs to test the
choices of our fuzzer, we used random seeds to ensure deterministic        Frama-C static-analysis platform [22]. Bugariu et al. [18] present
results and performed experiments for eight different seeds.               a fuzzing technique for detecting soundness and precision issues
                                                                           in implementations of abstract domains—the core components of
6   RELATED WORK                                                           abstract interpreters [23]. They use algebraic properties of abstract
                                                                           domains as test oracles and find bugs in widely used domains.
SMT solvers are core components in many program analyzers,
                                                                           Recently, Taneja et al. [44] proposed a testing technique for identi-
and as a result, their reliability is of crucial importance. Although
                                                                           fying soundness and precision issues in static dataflow analyses by
it is feasible to verify SAT and SMT algorithms [28, 36, 38], it is
                                                                           comparing results with a sound and maximally precise SMT-based
challenging and time consuming to verify even very basic SAT-
                                                                           analysis; they rely on the SMT solver to provide correct results.
or SMT-solver implementations. Verifying state-of-the-art, high-
                                                                              Zhang et al. [47] develop a practical and automated fuzzing
performance solver implementations, such as CVC4 [10] and Z3 [25],
                                                                           technique to test software model checkers. They focus on testing
is completely impractical. For these reasons, there is a growing in-
                                                                           control-flow reachability properties of programs. More specifically,
terest in testing such solvers, alongside related efforts that focus
                                                                           they synthesize valid branch reachability properties using concrete
on testing entire program analyzers.
                                                                           program executions and then fuse individual properties of different
    Testing SAT and SMT solvers. FuzzSMT [15] focuses on find-             branches into a single safety property.
ing crashes of SMT solvers for bitvector and array instances. It              Klinger et al. [34] propose an automated technique to test the
uses grammar-based blackbox fuzzing to generate crash-inducing             soundness and precision of program analyzers in general. Their
instances and minimizes any such instances with delta debug-               approach is based on differential testing. From seed programs, they
ging [2, 46]. Brummayer et al. [16] extend this line of work to            generate program-analysis benchmarks on which they compare
SAT and QBF solvers. In contrast, STORM performs mutational                the results of different analyzers.
fuzzing, and its minimization procedure leverages the fuzzer and its
bounds regarding the number of assertions and the formula depth.           7    CONCLUSION
    StringFuzz [13] targets testing of string solvers. In addition to      In this paper, we have presented a novel fuzzing technique for de-
randomly generating syntactically valid instances using a grammar,         tecting critical bugs in SMT solvers—key components of many state-
it is also able to mutate or transform formulas in existing instances.     of-the-art program analyzers. Conceptually, STORM is a blackbox
However, since not all of its transformations preserve satisfiability,     mutational fuzzer that uses fragments of existing SMT instances
it is not easily possible to leverage metamorphic testing [9] to           to generate new, realistic instances. Its formula-generation phase
Detecting Critical Bugs in SMT Solvers Using Blackbox Mutational Fuzzing


takes inspiration from grammar-based fuzzers; it leverages a mini-                         [31] Patrice Godefroid, Michael Y. Levin, and David A. Molnar. 2008. Automated
mal, but functionally complete, grammar for Boolean formulas to                                 Whitebox Fuzz Testing. In NDSS. The Internet Society, 151–166.
                                                                                           [32] Dejan Jovanovic, Clark Barrett, and Leonardo de Moura. 2013. The Design and
generate new formulas from fragments found in seeds. Finally, it                                Implementation of the Model-Constructing Satisfiability Calculus. In FMCAD.
solves the oracle problem by generating instances that are satisfi-                             IEEE Computer Society, 173–180.
                                                                                           [33] Timotej Kapus and Cristian Cadar. 2017. Automatic Testing of Symbolic Execution
able by construction. STORM found 29 previously unknown critical                                Engines via Program Generation and Differential Testing. In ASE. IEEE Computer
bugs in three solvers (or nine solver variants) and 15 different logics.                        Society, 590–600.
                                                                                           [34] Christian Klinger, Maria Christakis, and Valentin Wüstholz. 2019. Differentially
                                                                                                Testing Soundness and Precision of Program Analyzers. In ISSTA. ACM, 239–250.
                                                                                           [35] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Verifier for Functional
REFERENCES                                                                                      Correctness. In LPAR (LNCS), Vol. 6355. Springer, 348–370.
 [1] [n.d.]. CREST: Concolic Test Generation Tool for C. http://www.burn.im/crest/.        [36] Stéphane Lescuyer and Sylvain Conchon. 2008. A Reflexive Formalization of a
 [2] [n.d.]. DeltaSMT. http://fmv.jku.at/deltasmt.                                              SAT Solver in Coq. In TPHOLs.
 [3] [n.d.]. The International Satisfiability Modulo Theories Competition. https:          [37] Nuno P. Lopes, David Menendez, Santosh Nagarakatte, and John Regehr. 2015.
     //smt-comp.github.io.                                                                      Provably Correct Peephole Optimizations with Alive. In PLDI. ACM, 22–32.
 [4] [n.d.]. The Satisfiability Modulo Theories Library. http://smtlib.cs.uiowa.edu.       [38] Filip Maric. 2010. Formal Verification of a Modern SAT Solver by Shallow Em-
 [5] [n.d.]. Technical “Whitepaper” for AFL.          http://lcamtuf.coredump.cx/afl/           bedding into Isabelle/HOL. TCS 411 (2010), 4333–4356. Issue 50.
     technical_details.txt.                                                                [39] Lorenzo Martignoni, Stephen McCamant, Pongsin Poosankam, Dawn Song, and
 [6] [n.d.]. VoteSMT. http://fmv.jku.at/votesmt.                                                Petros Maniatis. 2012. Path-Exploration Lifting: Hi-Fi Tests for Lo-Fi Emulators.
 [7] Cyrille Artho, Armin Biere, and Martina Seidl. 2013. Model-Based Testing for               In ASPLOS. ACM, 337–348.
     Verification Back-Ends. In TAP (LNCS), Vol. 7942. Springer, 39–55.                    [40] William M. McKeeman. 1998. Differential Testing for Software. Digital Technical
 [8] Michael Barnett, Bor-Yuh Evan Chang, Robert DeLine, Bart Jacobs, and K. Rus-               Journal 10 (1998), 100–107. Issue 1.
     tan M. Leino. 2005. Boogie: A Modular Reusable Verifier for Object-Oriented           [41] Aina Niemetz and Armin Biere. 2013. ddSMT: A Delta Debugger for the SMT-LIB
     Programs. In FMCO (LNCS), Vol. 4111. Springer, 364–387.                                    v2 Format. In SMT. 36–45.
 [9] Earl T. Barr, Mark Harman, Phil McMinn, Muzammil Shahbaz, and Shin Yoo.               [42] Aina Niemetz, Mathias Preiner, and Armin Biere. 2017. Model-Based API Testing
     2015. The Oracle Problem in Software Testing: A Survey. TSE 41 (2015), 507–525.            for SMT Solvers. In SMT. 10 pages.
     Issue 5.                                                                              [43] Janet Siegmund, Norbert Siegmund, and Sven Apel. 2015. Views on Internal and
[10] Clark W. Barrett, Christopher L. Conway, Morgan Deters, Liana Hadarean, Dejan              External Validity in Empirical Software Engineering. In ICSE. IEEE Computer
     Jovanovic, Tim King, Andrew Reynolds, and Cesare Tinelli. 2011. CVC4. In CAV               Society, 9–19.
     (LNCS), Vol. 6806. Springer, 171–177.                                                 [44] Jubi Taneja, Zhengyang Liu, and John Regehr. 2020. Testing Static Analyses for
[11] Clark W. Barrett and Cesare Tinelli. 2018. Satisfiability Modulo Theories. In              Precision and Soundness. In CGO. ACM, 81–93.
     Handbook of Model Checking. Springer, 305–343.                                        [45] Xuejun Yang, Yang Chen, Eric Eide, and John Regehr. 2011. Finding and Under-
[12] Murphy Berzish, Vijay Ganesh, and Yunhui Zheng. 2017. Z3str3: A String Solver              standing Bugs in C Compilers. In PLDI. ACM, 283–294.
     with Theory-Aware Heuristics. In FMCAD. IEEE Computer Society, 55–59.                 [46] Andreas Zeller. 2009. Why Programs Fail, Second Edition: A Guide to Systematic
[13] Dmitry Blotsky, Federico Mora, Murphy Berzish, Yunhui Zheng, Ifaz Kabir, and               Debugging. Morgan Kaufmann.
     Vijay Ganesh. 2018. StringFuzz: A Fuzzer for String Solvers. In CAV (LNCS),           [47] Chengyu Zhang, Ting Su, Yichen Yan, Fuyuan Zhang, Geguang Pu, and Zhendong
     Vol. 10982. Springer, 45–51.                                                               Su. 2019. Finding and Understanding Bugs in Software Model Checkers. In
[14] Robert Brummayer and Armin Biere. 2009. Boolector: An Efficient SMT Solver                 ESEC/FSE. ACM, 763–773.
     for Bit-Vectors and Arrays. In TACAS (LNCS), Vol. 5505. Springer, 174–177.
[15] Robert Brummayer and Armin Biere. 2009. Fuzzing and Delta-Debugging SMT
     Solvers. In SMT. ACM, 1–5.
[16] Robert Brummayer, Florian Lonsing, and Armin Biere. 2010. Automated Testing
     and Debugging of SAT and QBF Solvers. In SAT (LNCS), Vol. 6175. Springer,
     44–57.
[17] Alexandra Bugariu and Peter Müller. 2020. Automatically Testing String Solvers.
     In ICSE. To appear.
[18] Alexandra Bugariu, Valentin Wüstholz, Maria Christakis, and Peter Müller. 2018.
     Automatically Testing Implementations of Numerical Abstract Domains. In ASE.
     ACM, 768–778.
[19] Cristian Cadar, Daniel Dunbar, and Dawson R. Engler. 2008. KLEE: Unassisted and
     Automatic Generation of High-Coverage Tests for Complex Systems Programs.
     In OSDI. USENIX, 209–224.
[20] Jürgen Christ, Jochen Hoenicke, and Alexander Nutz. 2012. SMTInterpol: An
     Interpolating SMT Solver. In SPIN (LNCS), Vol. 7385. Springer, 248–254.
[21] Alessandro Cimatti, Alberto Griggio, Bastiaan Joost Schaafsma, and Roberto Se-
     bastiani. 2013. The MathSAT5 SMT Solver. In TACAS (LNCS), Vol. 7795. Springer,
     93–107.
[22] Loïc Correnson, Pascal Cuoq, Florent Kirchner, Virgile Prevosto, Armand Puccetti,
     Julien Signoles, and Boris Yakobowski. 2011. Frama-C User Manual. http://frama-
     c.com//support.html.
[23] Patrick Cousot and Radhia Cousot. 1977. Abstract Interpretation: A Unified
     Lattice Model for Static Analysis of Programs by Construction or Approximation
     of Fixpoints. In POPL. ACM, 238–252.
[24] Pascal Cuoq, Benjamin Monate, Anne Pacalet, Virgile Prevosto, John Regehr, Boris
     Yakobowski, and Xuejun Yang. 2012. Testing Static Analyzers with Randomly
     Generated Programs. In NFM (LNCS), Vol. 7226. Springer, 120–125.
[25] Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In
     TACAS (LNCS), Vol. 4963. Springer, 337–340.
[26] Leonardo de Moura and Dejan Jovanovic. 2013. A Model-Constructing Satisfia-
     bility Calculus. In VMCAI (LNCS), Vol. 7737. Springer, 1–12.
[27] Bruno Dutertre. 2014. Yices 2.2. In CAV (LNCS), Vol. 8559. Springer, 737–744.
[28] Jonathan Ford and Natarajan Shankar. 2002. Formal Verification of a Combination
     Decision Procedure. In CADE (LNCS), Vol. 2392. Springer, 347–362.
[29] Vijay Ganesh. 2007. Decision Procedures for Bit-Vectors, Arrays and Integers. Ph.D.
     Dissertation. Stanford University, USA.
[30] Vijay Ganesh and David L. Dill. 2007. A Decision Procedure for Bit-Vectors and
     Arrays. In CAV (LNCS), Vol. 4590. Springer, 519–531.
