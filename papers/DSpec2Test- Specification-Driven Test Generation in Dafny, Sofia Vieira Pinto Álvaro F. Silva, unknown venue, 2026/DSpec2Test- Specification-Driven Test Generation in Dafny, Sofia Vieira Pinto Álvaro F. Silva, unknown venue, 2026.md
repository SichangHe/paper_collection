                                                DSpec2Test: Specification-Driven Test Generation in Dafny
                                                                       Sofia Vieira Pinto                                               Álvaro F. Silva
                                               INESC TEC, Faculdade de Engenharia, Universidade do                INESC TEC, Faculdade de Engenharia, Universidade do
                                                                       Porto                                                            Porto
                                                                 Porto, Portugal                                                    Porto, Portugal
                                                              sofia.p.pt@gmail.com                                             amfpsilva@hotmail.com

                                                                       João Pascoal Faria                                          Alexandra Mendes∗✉
                                               INESC TEC, Faculdade de Engenharia, Universidade do                INESC TEC, Faculdade de Engenharia, Universidade do
                                                                     Porto                                                              Porto
                                                                 Porto, Portugal                                                    Porto, Portugal
arXiv:2609.29713v1 [cs.SE] 31 Aug 2026




                                                                  jpf@fe.up.pt                                                    afmendes@fe.up.pt
                                         Abstract                                                                 underlying fault [12], costing developers significant time and effort.
                                         Verification-aware languages, such as Dafny, integrate logical con-      Here, tests can serve as a complementary mechanism by providing
                                         structs into code and enable automatic verification of program cor-      concrete executions that help locate and understand the fault.
                                         rectness. However, tests remain helpful in scenarios that verification       Within Dafny, test generation from implementation code is al-
                                         alone does not address (e.g., to support test-driven development).       ready supported by DTest [4], accessible via the generate-tests
                                         Existing Dafny test generation tools are implementation-based,           command. DTest targets code coverage to provide additional assur-
                                         limiting their applicability in this context.                            ance that compilation of Dafny programs to target languages (e.g.,
                                            We present DSpec2Test, a specification-driven test generation         C# or Java) preserves the properties verified in Dafny, attempting
                                         tool for Dafny that automatically derives tests from formal speci-       to mitigate the gap left by Dafny’s unverified compilation pipeline.
                                         fications, without considering implementation details. Our tool          It is part of a broader toolkit that also includes DUnit (unit testing)
                                         extends Dafny’s generate-tests command with a new black-                 and DMock (mock testing).
                                         box mode based on Disjunctive Normal Form (DNF) equivalence                  While DTest is useful for validating compiled implementations,
                                         class partitioning and optional Boundary Value Analysis (BVA).           there are scenarios in which generating tests directly from specifica-
                                         DSpec2Test relies on the Z3 SMT solver to synthesize inputs and          tions is more suitable. Implementation-based tests are constrained
                                         expected outputs that meet the specification-derived constraints.        by the structure and behaviour of the existing code, whereas tests
                                            We evaluate DSpec2Test on programs from DafnyBench mu-                based on the specification focus on the intended semantics of the
                                         tated using MutDafny and compare it against Dafny’s existing             program. This distinction is especially relevant during early stages
                                         implementation-driven Block mode. DSpec2Test achieves a 93.9%            of development, where specifications may already exist but im-
                                         mutation kill rate on a dataset of 131 mutants, outperforming Block’s    plementations are still incomplete or evolving. In such settings,
                                         82.4%, and uniquely killing 17 mutants. These results suggest that       specification-driven tests support a test-driven development (TDD)
                                         specification-driven testing is an effective and complementary ap-       style, where tests are derived from the specification first and guide
                                         proach for testing Dafny programs.                                       the subsequent implementation. This can help to pinpoint errors
                                         Demo: https://youtu.be/mK1EeJfinRQ                                       as soon as implementations deviate from the intended behavior.
                                         Code: https://github.com/VeriFixer/DSpec2Test                                We present DSpec2Test, a tool for specification-driven test gen-
                                         Prebuilt docker image: https://doi.org/10.5281/zenodo.21191158           eration in Dafny. This tool is provided through an additional mode
                                                                                                                  (Spec) for Dafny’s generate-tests command. It analyses the pre-
                                         CCS Concepts                                                             conditions and postconditions of the methods and functions to
                                                                                                                  create Disjunctive Normal Form (DNF) clauses, producing a com-
                                         • Software and its engineering → Formal software verifica-
                                                                                                                  prehensive pool of tests. To the best of our knowledge, there are no
                                         tion; Software testing and debugging; Software verification.
                                                                                                                  other Dafny tools that allow the automatic creation of tests prior
                                         Keywords                                                                 to the program’s implementation being written.
                                                                                                                      Our main contributions are:
                                         Dafny, Verification-aware languages, Test generation, Specification-
                                                                                                                   ⋆ A specification-to-test pipeline (instantiated for Dafny) that
                                         driven test generation, Software verification, Formal methods
                                                                                                                       combines (i) an automatic Safe DNF decomposition of arbitrary
                                         1    Introduction                                                             pre/postconditions, preserving short-circuit guard semantics,
                                                                                                                       (ii) boundary value analysis on the partition-derived constraints,
                                         Verification-aware languages, such as Dafny [7], integrate precondi-
                                                                                                                       and (iii) an encoding of each test goal as an assume/assert
                                         tions (requires), postconditions (ensures), and invariants (invariant)
                                                                                                                       false stub that delegates the search for concrete inputs and
                                         directly into the code, enabling automated detection of specification
                                                                                                                       expected outputs to Z3.
                                         violations during development. However, when verification fails,
                                                                                                                   ⋆ DSpec2Test, the first tool for specification-based conformance
                                         ∗ Author order follows a senior-author-last convention.
                                                                                                                       testing in Dafny. It derives tests from requires/ensures clauses
                                         error messages are often not sufficiently informative to identify the
                                                                              Sofia Vieira Pinto, Álvaro F. Silva, João Pascoal Faria, and Alexandra Mendes


  and can support test-driven development, specification valida-        Applied to ConditionalGet, each implication splits into two cases:
  tion, and fault localisation.                                         • 𝑄 1 : { 𝑥 ≥ 0, 𝑥 < 0 ∧ 𝑟 = −1 }
⋆ Evidence that specification-based and implementation-based            • 𝑄 2 : { 𝑥 < |𝑠 |, 𝑥 ≥ |𝑠 | ∧ 𝑟 = 1 }
  testing reach complementary fault classes gathered through            • 𝑄 3 : { ¬(0 ≤ 𝑥 < |𝑠 |), 0 ≤ 𝑥 < |𝑠 | ∧ 𝑟 = 𝑠 [𝑥] }
  an empirical evaluation on 131 mutants from DafnyBench, in            The cross product, conjoined with the precondition |𝑠 | > 0, yields
  which DSpec2Test kills 93.9 %, outperforming DTest (82.4 %)           eight candidate equivalence classes. Five are infeasible (Z3 returns
  and uniquely killing 17 mutants that DTest misses.                    UNSAT) due to mutually exclusive guards. The three feasible classes,
                                                                        after simplifying the redundant guard negations, are:
2     Formal Specification-Driven Test Generation                       • 𝐶 1 : |𝑠 | > 0 ∧ 𝑥 < 0 ∧ 𝑟 = −1 // below range
Formal specification-driven test generation is an approach that         • 𝐶 2 : |𝑠 | > 0 ∧ 𝑥 ≥ |𝑠 | ∧ 𝑟 = 1 // above range
constructs test cases directly from formal specifications rather        • 𝐶 3 : |𝑠 | > 0 ∧ 0 ≤ 𝑥 < |𝑠 | ∧ 𝑟 = 𝑠 [𝑥] // in range
than relying on existing implementation code. DSpec2Test fol-              If exhaustive combination testing is required and can be safely
lows this approach by actively exercising all preconditions (re-        applied, DSpec2Test also supports Full DNF (–fdnf flag), which
quires) and postconditions (ensures), and by automatically applying     drops short-circuit safety and forces every 𝑛-ary disjunctive opera-
the well-established black-box testing strategies of equivalence        tor to produce all 2𝑛 − 1 non-empty subsets of branch satisfaction.
class partitioning (ECP) and boundary value analysis (BVA) [11].        For instance, 𝐴 ∨ 𝐵 expands to {𝐴 ∧ 𝐵, 𝐴 ∧ ¬𝐵, ¬𝐴 ∧ 𝐵}.
DSpec2Test relies on an SMT-solver (Z3) to find concrete test data
that satisfy the target test conditions produced by ECP and BVA.        2.2      Boundary Value Analysis
                                                                        While equivalence class partitioning provides broad coverage, de-
2.1     DNF-Based Equivalence Class Partitioning
                                                                        fects (such as off-by-one errors) often hide at the edges of these
ECP consists of dividing input data into partitions, called equiva-     partitions. Therefore, when the –bva flag is provided, the tool com-
lence classes, where all values in a class are expected to behave in    plements the DNF phases with Boundary Value Analysis (BVA).
the same way [11]. We automate ECP by analysing the method’s               For every partition, the tool generates multiple test scenarios.
contract clauses and converting them into Disjunctive Normal Form       The first test leaves all variables free, relying only on the base DNF
(DNF). Alternative behaviours (depending on different input classes)    constraints. Subsequent tests pin exactly one variable to a boundary
are typically encoded in the method’s postconditions, which is why      value at a time, leaving all others free. This prevents conflicting
our starting point is the conjunction of all preconditions (requires)   constraints while exploring extreme edge cases.
and postconditions (ensures). Each DNF branch then constrains              The pinned boundary values are determined by each partition’s
both inputs and outputs, allowing us to generate concrete values for    constraints. If the partition restricts a variable to an interval, the
the test inputs and expected outputs (when uniquely determined          tool pins it to its exact valid edges. When a variable is unbounded,
by the contract).                                                       the tool uses default extremes (-100 and 100) for numeric variables.
      Listing 1: Example Dafny contract: ConditionalGet.                Sequences, sets, and maps are tested for lengths 0, 1, and > 1.
1 method ConditionalGet(s: seq<int>, x: int) returns (r:
                                                                           For instance, applied to class 𝐶 3 of ConditionalGet, BVA emits
    int)                                                                four additional scenarios, with the following constraints: 𝑥 = 0
2     requires |s| > 0                                                  (minimum), 𝑥 = |𝑠 |−1 (maximum), |𝑠 | = 1 (minimum), and |𝑠 | > 1
3     ensures x < 0 ==> r == -1          // Q1                          (above minimum).
4     ensures x >= |s| ==> r == 1        // Q2
5     ensures 0 <= x < |s| ==> r == s[x] // Q3
                                                                        2.3      Concrete Test Data Generation
   Conversion to DNF must be done carefully: a naive expansion          Like DTest, DSpec2Test relies on Z3 to find concrete test data that
of an implication 𝐴 ⇒ 𝐵 as ¬𝐴 ∨ 𝐵 produces a branch in which            satisfy each DNF branch and BVA constraint. The relevant con-
𝐵 is evaluated without the guard 𝐴, which may cause runtime             straints are encoded as assume statements in the method’s body,
crashes. For example, naively expanding 𝑄 3 in Listing 1 yields a       followed by an assert false that forces the verifier to emit a coun-
branch where 𝑟 = 𝑠 [𝑥] is evaluated without the guard 0 ≤ 𝑥 < |𝑠 |,     terexample, providing concrete test inputs and expected outputs.
raising an out-of-bounds error. To avoid this, DSpec2Test’s default     For class 𝐶 3 of ConditionalGet, the instrumented body is:
Safe DNF mode applies the short-circuit-safe decomposition rules
of Table 1, which produce mutually exclusive, guarded branches.                    Listing 2: Instrumented body for class 𝐶 3 .
                                                                        1 method ConditionalGet(s: seq<int>, x: int) returns (r:
                                                                          int)
            Table 1: Safe DNF decomposition rules.
                                                                        2   // contract unchanged
                                                                        3 {
     Operator                Branches (mutually exclusive)              4   assume |s| > 0 && 0 <= x < |s| && r == s[x];
     𝐴⇒𝐵                     { ¬𝐴, 𝐴 ∧ 𝐵 }                              5   assert false;
                                                                        6 }
     𝐴∨𝐵                     { 𝐴, ¬𝐴 ∧ 𝐵 }
     𝐴⇔𝐵                     { 𝐴 ∧ 𝐵, ¬𝐴 ∧ ¬𝐵 }                         A counterexample such as s=[3], x=0, r=3 is materialised as a
     if A then B else C      { 𝐴 ∧ 𝐵, ¬𝐴 ∧ 𝐶 }                          runnable Dafny test that sets up the input parameters, calls the
                                                                        method under test, and checks its outputs against concrete expected
DSpec2Test: Specification-Driven Test Generation in Dafny


values produced by Z3 (when –simplify is set, and the postcondi-          and non-determinism (e.g., :| operator), so these constraints were
tions uniquely constrain the outputs) or the original postconditions      also considered during the sampling process. Each program was
instantiated for the known inputs.                                        annotated with {:testEntry} so tests could be generated from the
                                                                          original (unmutated) code.
  Listing 3: Generated test with –simplify flag for class 𝐶 3 .
                                                                             We applied mutation testing, a well-established technique for
1 method {:test} Test_ConditionalGet_C3() {                               evaluating test adequacy [13, 15], using MutDafny [1], a muta-
2   var r := ConditionalGet([3], 0);
3   expect r == 3;                                                        tion tool that injects syntactic faults (relational/arithmetic operator
4 }                                                                       replacement, statement deletion, conditional negation, etc.) into
                                                                          Dafny implementations. For each program, up to 10 mutants were
                                                                          generated, retaining only those that fail verification, yielding 200
2.4     Implementation Pipeline                                           mutants in total. A mutation that fails verification may preserve
Figure 1 summarises how the components described above are                observable behaviour — it may simply break verification constructs.
integrated into Dafny’s generate-tests command, in three stages.          We mark such cases as equivalent mutants.
                                                                             The evaluation pipeline, using Dafny 4.11.0 and Z3 4.12.1, (1) gen-
                                                                          erates tests from the original program, (2) runs a safety check ensur-
                                                                          ing that the tests pass on the original (unmutated) code, and (3) runs
                                                                          each suite against every mutant to determine kill/survive/timeout
                                                                          status.

                                                                          3.2    Results and Discussion
                                                                          We base the comparison on the 17/20 programs supported by both
                                                                          strategies (three were not supported, crashing during test creation
                                                                          for at least one of them due to either exponential complexity or
Figure 1: DSpec2Test pipeline. An input file is processed                 tests not meeting the preconditions), totaling 170 mutants.
by the Verifier, where methods that are marked with                       Analysis of surviving mutants. We manually inspected the mu-
{:testEntry} or fail verification are passed to the Modifier for          tants that survived both strategies to determine if they could be
DNF generation and optional BVA. The Updater iteratively                  realistically killed, and found 22 non-compiling mutants and 17
refines the process by generating additional tests while en-              equivalent mutants (observationally equivalent to the original dur-
suring novelty through added assume clauses.                              ing execution), leaving 131 realistically-killable mutants.
                                                                          Analysis of timeouts. A small number of mutants timed out at the
    The Verifier flags for test generation every method that fails ver-   300 sec kill-check budget, which is vastly longer than a standard
ification or is annotated with {:testEntry}. The implementations          Dafny test execution. A manual inspection confirmed that these
of these methods are then discarded, since they are not used for          were all caused by infinite loops introduced by the mutations, ex-
specification-based test generation.                                      posed when exercised by the generated test inputs. We therefore
    The Modifier instruments each flagged method with the DNF             credit timeouts as kills.
classes and, when –bva is selected, BVA boundary pins derived in          Kill rates. Table 2 reports per-strategy kill rates and the overlap
the previous subsections, as illustrated in Listing 2.                    between the two tools on the 131 that can realistically be killed.
    The Updater drives iteration when –repeat is higher than one          Spec_bva kills 123 (93.9%), Block kills 108 (82.4%); the union covers
and –bva is not selected. After each generated test, it appends a fresh   125 (95.4%), with Spec_bva uniquely killing 17, Block uniquely killing
assume clause that excludes the previous input, so that the next          2, and only 6 mutants killed by neither tool.
solver call returns a different one. For instance, if x was assigned to
0, an assume x != 0; statement is added before the next iteration.        Table 2: Mutation kill rates and kill overlap on 131
                                                                          realistically-killable mutants. Timeouts (TO) are runtime
3 Empirical Evaluation                                                    infinite loops credited as kills. Killed = FAIL + TO.
3.1 Methodology
We compare two strategies of Dafny’s generate-tests: Block,                                            FAIL     TO     Killed    Surv.    Kill%
the existing white-box mode provided by DTest, which targets               Block (WB)                    99      9      108       23      82.4%
path/branch coverage of the implementation; and Spec_bva, the              Spec_bva (BB)                106     17      123        8      93.9%
black-box mode introduced by DSpec2Test (Spec) with the –bva               Union                         —      —       125        6      95.4%
flag, which targets equivalence class and boundary value coverage          Killed by Block only          —      —         2       —        1.5%
of the specification.                                                      Killed by Spec_bva only       —      —        17       —       13.0%
   We evaluate fault-detection capability on a corpus of 20 programs
sampled from DafnyBench [8], selected to contain methods with for-        Test volume vs. kill yield. Spec_bva generates 6.6 tests per file on
mal specifications (pre/postconditions, loop invariants) amenable         average (860 across the 131 files), versus ∼1.6 for Block. However,
to automated test generation. Currently, neither of the tools (DTest      this volume is heavily redundant: extracting the smallest failing
and DSpec2Test) supports mutable state (e.g., arrays), class fields,      test index per mutant from the runner output, we find 52 % of
                                                                                 Sofia Vieira Pinto, Álvaro F. Silva, João Pascoal Faria, and Alexandra Mendes


explicit-failure kills come from the first test, and 73 % from the first   this: for each output-referring 𝑄𝑘 (excluding range guards), search
three.                                                                     for an alternate 𝑖𝑘 ≠ 𝑖 satisfying the other literals but violating 𝑄𝑘 .
Complementarity. Of the 19 mutants killed by exactly one tool out          Equivalently, satisfy the extended contract, as shown in Listing 5.
of 131, 17 (89 %) are unique to Spec_bva and 2 are unique to Block,
                                                                               Listing 5: Extended contract for relevance checking.
indicating that ECP and BVA on the specification reaches faults
                                                                           1 method LastIdx'(a: seq<int>, x: int)
that path coverage on the implementation does not, and vice-versa,         2               returns(i: int, ghost i2:int, ghost i3:int)
highlighting their complementarity.                                        3 requires sorted(a) && x in a
Cost. Spec_bva is approximately 1.6× slower in wall-clock time             4 ensures 0 <= i < |a| && a[i] == x && x !in a[i+1..]
                                                                           5 ensures i2!=i && 0<=i2<|a| && a[i2]!=x && x !in a[i2+1..] //Q2
(7889 s vs. 4867 s), reflecting the larger generated suite.                  rel.
                                                                           6 ensures i3!=i && 0<=i3<|a| && a[i3]==x && x in a[i3+1..] //Q3
4    Related Work                                                            rel.

In addition to DTest [4], Delfy [2] also generates tests for Dafny,        DSpec2Test also lacks function inlining in specifications and (like
using dynamic symbolic execution with Z3 to diagnose verification          DTest) support for mutable state (arrays and class fields). Both are
failures. Concolic tools such as PathCrawler [18] (for C, within           planned to broaden applicability.
Frama-C [6]) similarly generate inputs from executable code for               We also plan to expand the evaluation to a broader sample of
structural coverage. Our approach differs from these as it is fully        programs.
spec-driven and requires no implementation.
   AutoTest [10] is a black-box testing framework for Eiffel that          6   Conclusion
combines random sampling with existing contracts to generate               We presented DSpec2Test, a specification-driven test generation
tests for object-oriented code. We instead use SMT solver calls for        tool for Dafny that derives runnable tests from the requires and
a more directed exploration of the input space.                            ensures clauses of a method, without examining the implemen-
   Other spec-driven test generators apply related techniques to           tation. While specification-based testing is well-established for
formal contracts. Gil et al. [5] target SPARK/Ada (also a verification-    other contract languages (e.g., AutoTest for Eiffel, JMLUnit for
aware language) with ECP guided by user-written Contract_Cases             Java), DSpec2Test is, to the best of our knowledge, the first Dafny
and Z3py called externally, but, unlike our approach, do not au-           tool that supports test generation prior to (or independently of)
tomatically derive DNF-based equivalence classes from arbitrary            the implementation — a capability complementary to the existing
pre/postconditions or reuse the host verifier. Peña et al. [14] use Z3     implementation-driven DTest. As far as we are aware, it is also
to derive test inputs from preconditions in a custom specification         the first tool that performs automatic DNF partitioning of method
language, but do not partition the whole contract via DNF for di-          contracts.
rected, human-readable tests. Rebello de Andrade et al. [16] apply            Our evaluation shows that DTest and DSpec2Test are comple-
Full DNF to axiomatic specifications of Java generics — a precursor        mentary, with DSpec2Test uniquely killing 17 mutants that Block
to our Safe DNF for method contracts — and use Alloy Analyzer              misses out of 131, indicating that specification- and implementation-
(a SAT solver) to find satisfying models for each minterm, but do          based testing reach different fault classes. DSpec2Test is therefore
not target a verification-aware language or apply boundary value           useful both as a stand-alone tool for early-stage and TDD-style
analysis.                                                                  workflows and as a complement to existing white-box tooling such
   Property-based testing tools, such as QuickCheck [3] and Hy-            as DTest, useful for implementation coverage. However, for max-
pothesis [9], also generate tests from properties, but these are ex-       imum fault localisation and rigor, both strategies should be em-
ecutable, partial, and input-centric, not full correctness specifica-      ployed.
tions.
                                                                           Data Availability Statement
5    Future Work
                                                                           The data associated with this work are publicly available through
We plan to refine DNF clauses with additional constraints so that          a Zenodo repository [17]. The dataset can be accessed using the
every postcondition literal genuinely constrains the admissible            following DOI: https://doi.org/10.5281/zenodo.21191158
outputs for the input Z3 picks. Consider finding the last occurrence
of 𝑥 in a sorted sequence 𝑎 known to contain it, as shown in the           Acknowledgments
example in Listing 4.
                                                                           Sofia Vieira Pinto, João Pascoal Faria, and Alexandra Mendes were
     Listing 4: Last occurrence of 𝑥 in a sorted sequence.                 funded by National Funds through the FCT - Fundação para a Ciên-
1 method LastIdx(a: seq<int>, x: int) returns (i: int)                     cia e a Tecnologia, I.P. (Portuguese Foundation for Science and Tech-
2 requires sorted(a) && x in a                                             nology) within the project VeriFixer, with reference 2023.15557.PEX
3 ensures 0 <= i < |a|       // Q1 (range guard)
4 ensures a[i] == x           // Q2                                        (DOI: 10.54499/2023.15557.PEX).
5 ensures x !in a[i+1..]      // Q3                                           Álvaro F. Silva was co-financed by national funds through FCT
                                                                           – Fundação para a Ciência e a Tecnologia, I.P., under the support
Z3 picks the minimal model a=[x], i=0, on which 𝑄 2 and 𝑄 3 hold           UID/50014/2025 (https://doi.org/10.54499/UID/50014/2025), by Na-
vacuously; a buggy implementation returning a[0] passes. Exer-             tional Funds through the FCT - Fundação para a Ciência e a Tec-
cising both non-vacuously requires multiple copies of 𝑥 plus a             nologia, I.P. (Portuguese Foundation for Science and Technology)
distinct element (e.g., a=[5,5,6], x=5). A relevance check forces          within the project VeriFixer, with reference 2023.15557.PEX (DOI:
DSpec2Test: Specification-Driven Test Generation in Dafny


10.54499/2023.15557.PEX), and Fundação para a Ciência e a Tecnolo-                        [9] David R. MacIver, Zac Hatfield-Dodds, and Many Other Contributors. 2019.
gia (Portuguese Foundation for Science and Technology) through                                Hypothesis: A new approach to property-based testing. Journal of Open Source
                                                                                              Software 4, 43 (2019), 1891. doi:10.21105/joss.01891
the Carnegie Mellon Portugal Program under the fellowship refer-                         [10] Bertrand Meyer, Arno Fiva, Ilinca Ciupa, Andreas Leitner, Yi Wei, and Emmanuel
ence PRT/BD/155045/2024.                                                                      Stapf. 2009. Programs That Test Themselves. Computer 42, 9 (2009). doi:10.1109/
                                                                                              MC.2009.296
                                                                                         [11] Glenford J Myers, Tom Badgett, Todd M Thomas, and Corey Sandler. 2012. The art
References                                                                                    of software testing. Vol. 2. John Wiley and Sons, Ltd. doi:10.1002/9781119202486
 [1] Isabel Amaral, Alexandra Mendes, and José Campos. 2026. MutDafny: A                 [12] Francisco Oliveira, Alexandra Mendes, and Carolina Carreira. 2025. What Chal-
     Mutation-Based Approach to Assess Dafny Specifications. In 2026 IEEE/ACM                 lenges Do Developers Face When Using Verification-Aware Programming Lan-
     48th International Conference on Software Engineering (ICSE).                            guages?. In 2025 IEEE 36th International Symposium on Software Reliability Engi-
 [2] Maria Christakis, K. Rustan M. Leino, Peter Müller, and Valentin Wüstholz.               neering (ISSRE). 203–214. doi:10.1109/ISSRE66568.2025.00031
     2016. Integrated Environment for Diagnosing Verification Errors. In Tools and       [13] Mike Papadakis, Marinos Kintis, Jie Zhang, Yue Jia, Yves Le Traon, and Mark
     Algorithms for the Construction and Analysis of Systems, Marsha Chechik and Jean-        Harman. 2019. Chapter Six - Mutation Testing Advances: An Analysis and
     François Raskin (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 424–441.         Survey. Advances in Computers, Vol. 112. Elsevier, 275–378. doi:10.1016/bs.
     doi:10.1007/978-3-662-49674-9_25                                                         adcom.2018.03.015
 [3] Koen Claessen and John Hughes. 2000. QuickCheck: a lightweight tool for             [14] Ricardo Peña, Jaime Sánchez-Hernández, Miguel Garrido, and Javier Sagredo.
     random testing of Haskell programs. SIGPLAN Not. 35, 9 (Sept. 2000), 268–279.            2023. SMT-Based Test-Case Generation and Validation for Programs with Complex
     doi:10.1145/357766.351266                                                                Specifications. Springer Nature Switzerland, Cham, 188–205. doi:10.1007/978-3-
 [4] Aleksandr Fedchin, Tyler Dean, Jeffrey S. Foster, Eric Mercer, Zvonimir Raka-            031-31476-6_10
     marić, Giles Reger, Neha Rungta, Robin Salkeld, Lucas Wagner, and Cassidy           [15] Goran Petrović and Marko Ivanković. 2018. State of mutation testing at
     Waldrip. 2023. A Toolkit for Automated Testing of Dafny. In NASA Formal                  google. In Proceedings of the 40th International Conference on Software En-
     Methods, Kristin Yvonne Rozier and Swarat Chaudhuri (Eds.). Springer Nature              gineering: Software Engineering in Practice (Gothenburg, Sweden) (ICSE-SEIP
     Switzerland, Cham, 397–413. doi:10.1007/978-3-031-33170-1_24                             ’18). Association for Computing Machinery, New York, NY, USA, 163–171.
 [5] Samuel Jiménez Gil, Manuel I. Capel, and Gabriel Olea Olea. 2024. Automatic test         doi:10.1145/3183519.3183521
     cases generation from formal contracts. Information and Software Technology         [16] Francisco Rebello de Andrade, João P. Faria, Antónia Lopes, and Ana C. R. Paiva.
     172 (2024), 107467. doi:10.1016/j.infsof.2024.107467                                     2012. Specification-Driven Unit Test Generation for Java Generic Classes. In
 [6] Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris         Integrated Formal Methods, John Derrick, Stefania Gnesi, Diego Latella, and
     Yakobowski. 2015. Frama-C: A software analysis perspective. Formal aspects of            Helen Treharne (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 296–311.
     computing 27, 3 (2015), 573–609. doi:10.1007/s00165-014-0326-7                           doi:10.1007/978-3-642-30729-4_21
 [7] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Verifier for Functional       [17] Sofia Vieira Pinto, Álvaro F. Silva, João Pascoal Faria, and Alexandra Mendes.
     Correctness. In Logic for Programming, Artificial Intelligence, and Reasoning,           2026. DSpec2Test: Specification-Driven Test Generation in Dafny (Artifact). doi:10.
     Edmund M. Clarke and Andrei Voronkov (Eds.). Springer Berlin Heidelberg,                 5281/zenodo.21191158
     Berlin, Heidelberg, 348–370. doi:10.1007/978-3-642-17511-4_20                       [18] Nicky Williams, Bruno Marre, Patricia Mouy, and Muriel Roger. 2005.
 [8] Chloe Loughridge, Qinyi Sun, Seth Ahrenbach, Federico Cassano, Chuyue Sun,               PathCrawler: Automatic Generation of Path Tests by Combining Static and
     Ying Sheng, Anish Mudide, Md Rakib Hossain Misu, Nada Amin, and Max                      Dynamic Analysis. In Dependable Computing - EDCC 5, Mario Dal Cin, Mo-
     Tegmark. 2024. Dafnybench: A benchmark for formal software verification.                 hamed Kaâniche, and András Pataricza (Eds.). Springer Berlin Heidelberg, Berlin,
     arXiv preprint arXiv:2406.08467 (2024). doi:10.48550/arXiv.2406.08467                    Heidelberg, 281–292. doi:10.1007/11408901_21
