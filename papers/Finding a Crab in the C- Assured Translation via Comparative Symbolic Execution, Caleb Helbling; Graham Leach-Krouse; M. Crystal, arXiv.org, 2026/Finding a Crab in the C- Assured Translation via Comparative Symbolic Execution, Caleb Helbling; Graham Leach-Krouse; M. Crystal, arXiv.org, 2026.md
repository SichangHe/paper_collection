                                             Finding a Crab in the C: Assured Translation via
                                                    Comparative Symbolic Execution
                                                              Caleb Helbling                             Graham Leach-Krouse                                Michael Crystal
                                                                Draper                                           Draper                                         Draper
                                                         Cambridge, MA, USA                               Cambridge, MA, USA                             Cambridge, MA, USA
                                                         chelbling@draper.com                           gleach-krouse@draper.com                          mcrystal@draper.com



                                            Abstract—Modern high-assurance software systems develop-                       once is often impractical. Instead, incremental re-writes are
                                         ment favors memory safe languages such as SPARK (ADA)                             needed to slowly add memory safety. This translation can
arXiv:2605.12731v1 [cs.SE] 12 May 2026




                                         or Rust. However, developers often encounter non-memory safe                      be done by some combination of manual translation, formal
                                         code (e.g., C) in legacy systems and libraries which would
                                         be prohibitively expensive or risky to re-write. In response,                     transpilation [5], or machine learning based translation [6],
                                         developers have begun turning to machine learning/AI systems                      [7], [8], [9]. But even careful incremental rewrites are not
                                         and other automated code translators. Automated translation                       necessarily meaning-preserving. Changes to program behavior
                                         comes with its own risks, however. The original and ported                        can be introduced intentionally by fixing bugs (for example,
                                         code are not precisely the same, semantically - otherwise there                   memory safety violations) found in the original source, or
                                         would be no point in performing the translation. To reduce
                                         these risks, we have developed cozy, a comparative binary                         unintentionally by erroneous translation.
                                         analysis tool that simultaneously analyzes a binary compiled from                    Detecting these changes in program behavior is therefore
                                         “unsafe” source code and a binary compiled from a translation                     growing in importance, and new automated methods are
                                         of the source code to a memory safe language. cozy walks                          needed to obtain comprehensive analysis results. In this paper
                                         the developer through differences in the behavior of the two                      we will discuss our ongoing efforts to adapt our tool, cozy, for
                                         binaries, presenting each difference and asking the user to assess
                                         whether the difference is intentional (good) or erroneous. Outside                comparing C and Rust programs. Although originally designed
                                         of the flagged differences, the binaries are formally verified                    for analysis of binary micropatches [10], cozy can be used to
                                         to be equivalent. Consequently, the review process guarantees                     analyze generic binary software.
                                         equivalence modulo changes approved by the developer. cozy
                                         has applications to automated translation, bug correction, code                             II. C OMPARATIVE S YMBOLIC E XECUTION
                                         reviews, operation authorization, and automatic translation.
                                            Index Terms—Rust, C, verification, symbolic execution, com-                       To make the comparison between two binary programs,
                                         parison, differential, diffing                                                    cozy uses the angr symbolic execution framework [11] to
                                                                                                                           perform comparative symbolic execution 1 (CSE) [12], [13].
                                                               I. I NTRODUCTION                                            During comparative symbolic execution, the pair of programs
                                            For many years, languages such as C and C++ have been the                      under analysis are fed the same symbolic input, and are then
                                         tool of choice for authors of low level or performance critical                   each symbolically executed to completion. During symbolic
                                         software. Unfortunately these languages suffer from memory                        execution, the program state may “split” when control flow
                                         safety issues, which have led to a wide range of security                         depends on the value of a symbolic variable, resulting in
                                         vulnerabilities. Rust has recently emerged as a compelling                        two separate child states each being generated as possible
                                         alternative for the development of low level applications by                      successors to a shared parent state. With repeated branching,
                                         offering exceptional performance and control without compro-                      an execution tree is created, with the initial execution state
                                         mising on memory safety. The push towards using memory                            lying at the tree root, and terminal program states as tree
                                         safe languages has even been taken up by policy makers,                           leaves.
                                         with the National Security Agency (NSA), Cybersecurity and                           Typically at a branch point, one child will add a new
                                         Infrastructure Security Agency (CISA), and the White House                        constraint C, and the other child will add the negation ¬C.
                                         Office of the National Cyber Director (ONCD) all releasing                        As a result, during execution each state accumulates a list of
                                         reports urging adoption [1], [2], [3], [4].                                       constraints (interpreted conjunctively) which can be fed to an
                                            Legacy codebases of C or C++ applications can be very                          SMT solver such as Z3. Solving the system of constraints
                                         large, and simply re-writing the entire codebase to Rust at                       associated with a given state produces a concrete input that
                                                                                                                           would drive the program to enter that particular state during
                                            This material is based upon work supported by the Defense Advanced
                                         Research Projects Agency (DARPA) and the Naval Information Warfare                ordinary, non-symbolic execution.
                                         Center (NIWC) Pacific, under Contract No. N66001-20-C-4018. The views,
                                         opinions and/or findings expressed are those of the author and should not be         1 Prior work sometimes refers to “differential symbolic execution” [12]
                                         interpreted as representing the official views or policies of the Department of   and “relational symbolic execution” [13]. Throughout this work, we use
                                         Defense or the U.S. Government. Distribution Statement “A” (Approved for          “comparative symbolic execution” as a generic term for this family of
                                         Public Release, Distribution Unlimited).                                          techniques.
                                                        cozy Python-based Analysis Framework

                                                                                                                                             Textual
                                                                                                                                             Report

        C Binary
                                                            Symbolically
                                                            execute C

                          User written Python                                    Compatibility checks
                                                                                                            Diff result object
                               harness                                            & Symbolic diffing
                                                                                                                                            Interactive
                                                                                                                                           Visualization
                                                            Symbolically
                                                            execute Rust
      Rust Binary

                                                                                                                                             Concrete
                                                                                                                                            test cases




Fig. 1. The architecture of how cozy uses comparative symbolic execution in its analysis. The resulting diff object can be used to generate a textual report,
exported for use in the interactive web based visualization software, or converted to concrete test cases for use in a testing suite.



    After both programs are run to completion, cozy then                           A C vs Rust comparison requires flexibility, as the compiler
proceeds in its analysis by comparing pairs of terminal states.                 for each language may produce code that differs in data
We say that a terminal state s from the first program and s′                    layout and storage locations. To account for this difference,
from the second program are compatible if there is a possible                   we introduce the concept of annotations, which enables the
input that satisfies the joint constraints associated with s and                assignment of names to specific memory or data locations. An
s′ . Compatible states are ones that make sense to compare,                     annotation name is simply a sequence of strings and integers,
since two compatible terminal states represent a possible pair                  typically derived from the names of struct fields and array
of behaviors that would have been produced by the same input                    locations. In the current implementation of cozy, annotations
to the two programs under analysis.                                             must be provided by the operator as part of the Python harness.
                                                                                By using annotations to map out semantic correspondences
   Definition 1 (Compatibility):
                                                                                between memory and data locations, cozy is able to align
              Compatible ≜ {(s, s′ ) | compatible(s, s′ )}                      comparisons across language boundaries.

          compatible(s, s′ ) ≜ is_sat(s.constraints ∧                                                    III. V ISUALIZATION
                                                ′                                  cozy exposes a GUI for interactive exploration of the
                                                s .constraints)
                                                                                symbolic execution trees. Direct manipulation of the sym-
      Unsat core optimization: A naı̈ve way to compute the                      bolic execution results is important. Symbolic execution, even
Compatible set is to check all n2 pairs of terminal states for                  restricting attention to compatible paths, produces a lot of
joint satisfiability. cozy implements a memoization-based op-                   information. When analyzing symbolic execution results, the
timization to enhance performance. When s.constraints∧                          user needs a way to cut out extraneous noise. Typically, only
s′ .constraints is unsatisfiable for a pair of states (s, s′ ),                 a small subset of all of the possible paths through a program
cozy computes the unsat core and caches it. The unsat core                      are of genuine interest.
is the minimal set of clauses for which the conjunction
is unsatisfiable. Later, when we want to know if a new                          A. Focusing Mechanisms
pair (s, s′ ) is compatible, we first check if any previously                      The cozy GUI offers three mechanisms for focusing on
discovered unsat core is a subset of the joint constraints                      the relevant parts of symbolic execution results: highlighting,
s.constraints∧s′ .constraints. If this check succeeds,                          pruning, and compression.
then the joint constraints are immediately unsatisfiable, and                      Several types of program states that are likely to be signif-
we can skip the expensive call to is_sat. Since most state                      icant are automatically highlighted in the GUI. These include
pairs are incompatible in practice, the unsat core optimization                 states that raised errors during execution, states at which a
drastically reduces the number of SMT solver queries.                           syscall or SimProc (modeled function) call occurred, states
    Once a pair of states is determined to be compatible by                     at which the program exceeded user-specified boundaries on
their constraints, we then begin the process of comparing                       loop iteration, and states at which a user-provided assert or
the inner machine state of the pair. As an example, the                         postcondition failed. Colors indicate different categories of
memory contents v and v ′ at a certain address from the                         potentially significant states.
first and second program’s terminal states respectively can be                     Besides calling attention to relevant results, it can be helpful
compared with a SMT query is_sat(s.constraints ∧                                to filter out irrelevant results. Pruning works as follows: cozy
s′ .constraints ∧ v ̸= v ′ ).                                                   prunes (hides) each branch unless it is “interestingly related” to
                                                                                      The sequence of nodes along a symbolic execution path
                                                                                   corresponds to several different kinds of event streams: the
                                                                                   stream of assembly instructions executed, the stream of read
                                                                                   and write operations on memory and registers, and the stream
                                                                                   of modeled IO effects. cozy compares these types of event
                                                                                   streams using a familiar git-style line diff. For each type
                                                                                   of event stream comparison, when the user mouses over an
                                                                                   event in the diff panel, the UI highlights the tree node that
                                                                                   corresponds to that event. This behavior enables the user to
                                                                                   intuitively connect the contents of the tree-view to the contents
                                                                                   of the event stream.
                                                                                      In addition to diffing event streams, cozy supports compar-
                                                                                   isons of terminal states. For example, cozy can compare the
                                                                                   final memory contents of two compatible branches. Figure 2
                                                                                   shows an example of using the memory tab of the diff panel
                                                                                   to compare a pair of selected terminal states. If the symbolic
                                                                                   expressions for the final memory contents of the states are
Fig. 2. In this example we interactively explore the execution trees of a C        equivalent, then cozy reports this fact; if they are not, cozy
implementation of insertion sort with a Rust implementation of bubble sort
containing a bug. After selecting one particular state pair from the execution     generates multiple concretions that each illustrate a possible
tree, we observe in the diff panel that the mutated input arrays differ between    scenario in which the terminal states differ despite an identical
the two versions (i.e., the symbolic num_0 and num_1 are placed in different       initial state.
locations in the mutated input array). This indicates a presence of a difference
in program behavior.                                                                  Finally, the diff panel can display concrete inputs that
                                                                                   exercise each of the branches being compared. Compatibility
                                                                                   guarantees the existence of at least one input that produces
a compatible branch in the facing tree, where the user specifies                   the two sequences of behaviors that the branches represent.
(via the GUI) which relationships are interesting. For example,                    The concretion view in the GUI’s diff panel displays example
the user can indicate that two branches are interestingly related                  inputs that are shared between the two compatible paths.
when their terminal states have different memory contents;                         This feature, in combination with cozy’s pruning functionality,
pruning will then leave only the branches that differ from at                      make it possible to recover specific inputs that generate
least one compatible branch of the facing tree in terms of their                   execution paths of interest, especially paths where behavior
final memory contents. The relations that the GUI checks are                       differs interestingly between the two binaries being compared.
symmetric, so if a branch b survives pruning because it is                            Compatibility does not guarantee that every input that
partnered with a compatible branch b′ , then b′ will survive                       produces the behavior associated with the first branch also
as well. Therefore, pruning will never result in an orphaned                       produces the behavior associated with the second branch, or
branch.                                                                            vice versa. If we consider the set of concrete inputs that lead to
   Finally, cozy allows compression: merging successive nodes                      a specific brach from the first program and the second program
that represent uninteresting or inevitable computation steps.                      as A and B respectively, then the set difference A \ B may be
There are two available compression levels: the user can (1)                       non-empty. In such scenarios, cozy reports inputs in the sets
merge adjacent nodes that have identical constraints and (2)                       A \ B and B \ A. Based on this information, we can determine
merge every node that has a unique child with that child node,                     if one branch “refines” the other, or if the input sets are exactly
eliminating all straight-line sequences of symbolic states. 2                      equivalent.
Using compression visually reduces the size of the execution
                                                                                                   IV. E XPERIMENTAL R ESULTS
tree, easing the process of interactively exploring program
behavior.                                                                             To validate cozy’s ability to compare C and Rust programs,
                                                                                   we performed several experiments designed to gauge usability
B. The Diff Panel                                                                  and performance characteristics. For each experiment, we de-
                                                                                   signed a program and created a handwritten C implementation,
   After finding the branches or state nodes of interest, cozy’s
                                                                                   a handwritten Rust implementation, and an implementation
user must be able to extract information from them. For
                                                                                   derived from the handwritten C using Galois/Immunant’s
examining individual nodes, we display features of symbolic
                                                                                   automated C2Rust transpiler [5].
state using simple tooltips. The more interesting challenge
is displaying comparative information, when two compatible                            1) In our first experiment, we implemented insertion sort,
branches need to be examined simultaneously. For this, we use                            and were able to verify that the C, Rust, and C2Rust
the Diff Panel.                                                                          versions were equivalent. As a follow up to this test, we
                                                                                         compared a C version of insertion sort with a Rust im-
  2 Symbolic execution can add a constraint without branching when, for                  plementation of bubble sort. cozy was able to verify that
example, the result of adding the negation of the constraint is unsatisfiable.           the sorted outputs were equivalent, despite a difference
     in both implementation language and algorithm choice.        language. We ameliorated the lack of Rust support in three
     Input array lengths were bounded by a small constant         ways: (1) through judicious use of repr(C) annotations on
     to ensure execution termination.                             data structures, (2) by requiring the use of extern "C" on
  2) In our second experiment, we wrote a simple watch            functions to obtain a stable calling convention, and (3) by
     program to test branching, arithmetic operations, and        using DWARF debug data for memory layout information and
     basic data structures. We first defined a datetime           to reduce the burden to provide type information. While we
     struct, which contained an hour, minute, second, month,      cannot claim that we support all Rust datatypes, we do have
     day, year and day of week field. We then created             sufficient support for many basic use cases.
     a second_tick function, which returned a new                    Besides challenges related to the ABI, we also encountered
     datetime, incremented by 1 second from the in-               issues with the use of compiler optimizations. In our watch
     put. The bulk of the second_tick function revolved           example, the Rust compiler was able to optimize one of the
     around rollover of the different fields. Rollover occured    modulo calculations away, replacing it with an equivalent
     in multiple places: seconds to minutes, minutes to hours,    calculation using only bitwise and multiplication operations
     etc. Extra logic was required to account for the variable    [14]. The GCC version did not use this particular optimization.
     number of days in each month, and for the determination      When the Z3 solver was asked to verify the equivalence of
     of the number of days in February for leap years.            the two implementations, it was unable to make progress
  3) In our third experiment, we created a box blur algorithm,    due to the lack of understanding of the theory underlying
     which returned a blurred version of an input image. A        this particular optimization. The situation was resolved by
     kernel size parameter was also used as input to control      turning off all optimizations on all compilers, including MLIR
     the size of box inside the algorithm (and therefore the      optimization in rustc.
     blurriness of the resulting image). This experiment was
     created to exercise analysis of programs with nested                              VI. R ELATED W ORK
     loops and more complex data structures. We modeled              One alternative for verifying program equivalence is to
     the input image as an array of pixels from the array2d       create a single harness function which runs the two functions
     crate. This particular crate used a dynamically sized Rust   in sequence, then assert equivalence in the return results. This
     vector, so modeling this more complex data structure         can be accomplished in the Kani Rust bounded model checker
     was necessary to construct the input to feed to the          [15] with a sequential equality harness, and some experimental
     program. Once again, we were able to verify that the box     features that enable bounded model checking of code linking
     blur implementations were equivalent for small input         to C:
     images and kernel sizes.
                                                                   1   fn sequential_equality_harness() {
                      V. C HALLENGES                               2       // Create a nondeterministic input
                                                                   3       let input_val: u8 = kani::any();
   In our second experiment we encountered some differences
                                                                   4       let out_c = c_fun(input_val);
in program behavior, due to how arithmetic overflows are han-
                                                                   5       let out_rust = rust_fun(input_val);
dled in C vs Rust. In the C programming language overflows
                                                                   6       assert!(out_c == out_rust);
are undefined behavior, whereas in Rust, the program will
                                                                   7   }
either panic (if compiled in debug mode) or perform two’s
complement overflow (if compiled in release mode). The net           A sequential equality harness approach was taken by Yang
result is that the program outputs will almost always diverge     et al. in their VERT system [16] to verify equivalence of
due to differences in how edge cases are handled in arithmetic    LLM translated C programs. Although this approach may
operations. Under the assumptions appropriate for the inputs      look simple at first glance, it has some hidden downsides.
to this kind of algorithm, these differences would not actually   Since the harness runs the two functions one after the other,
be exposed during execution; so, to improve our modeling          a copy of the execution tree of the second function is made
of the watch program, we simply inserted some assumptions         for every leaf of the execution tree of the first function. Even
bounding the input (for example bounding the years field to       with early pruning of unsat paths, programs with degenerate
sensible ranges), thereby constraining the program to never       compatibility (i.e., all pairs are compatible) will result in
enter an overflow state. At this point, the Z3 solver was         unnecessary re-computation.
sufficiently constrained to prove the equality of the resulting      In addition to the issue with the blowup of the number
program outputs.                                                  of simulation paths, sequential equality harnesses do not give
   On the software engineering side, we encountered chal-         insights into all paths that lead to equality failure, only a fairly
lenges in adapting cozy to interact with the Rust ABI. To make    coarse success/failure signal, and perhaps a counterexample
accurate comparisons, the cozy Python library needs to know       to equivalence. Because cozy has access to the details of
where to place data in preparation for program execution, and     symbolic state evolution, we can identify the branches that
where the return results are placed once execution is complete.   make sense to compare—the ones that accumulate compatible
The angr library has some support for the C programming           pairs of constraints—and directly inspect the course of each
language, but offers no support for the Rust programming          possible execution interactively or via textual report. cozy
focuses not on whether the functions are equivalent, but on                                   R EFERENCES
how they differ.                                                     [1]   “Software memory safety,” National Security Agency,
   Bai and Palit took another approach with their work on                  Tech. Rep., Apr. 2023. [Online]. Available: https : / /
RustAssure [17]. In RustAssure, the C and Rust programs                    media . defense . gov / 2022 / Nov / 10 / 2003112742/ - 1/ -
were independently symbolically executed using KLEE, and                   1/0/CSI SOFTWARE MEMORY SAFETY.PDF
the symbolic return values were dumped to an external file           [2]   “Memory safe languages: Reducing vulnerabilities
for analysis. After that point, no further queries to the SMT              in modern software development,” National Security
solver were made, and the return symbols were compared                     Agency, Tech. Rep., Jun. 2025. [Online]. Available:
for similarity via a graph distance metric. Our approach                   https://media.defense.gov/2025/Jun/23/2003742198/-
differs as we use a compatible state check utilizing the path              1/ - 1 / 0 / CSI MEMORY SAFE LANGUAGES
conditions and perform symbolic diffing using Z3. We believe               REDUCING VULNERABILITIES IN MODERN
that punting equality checking to the SMT solver is the most               SOFTWARE DEVELOPMENT.PDF
flexible approach and leads to more accurate results than            [3]   “The case for memory safe roadmaps: Why both c-suite
a graph edit distance metric. Bai and Palit make a similar                 executives and technical experts need to take memory
argument in their paper when assessing their approach, and                 safe coding seriously,” Cybersecurity and Infrastructure
note that moving to an SMT based approach is part of their                 Security Agency, Tech. Rep., Dec. 2023. [Online].
future work.                                                               Available: https://www.cisa.gov/sites/default/files/2023-
             VII. D ISCUSSION & C ONCLUSION                                12/The-Case-for-Memory-Safe-Roadmaps-508c.pdf
                                                                     [4]   “Back to building blocks: A path towards secure and
   In this paper we have described how our tool, cozy, can be
                                                                           measurable software,” Office of the National Cyber
used to compare C and Rust programs through symbolic ex-
                                                                           Director, Tech. Rep., Feb. 2024. [Online]. Available:
ecution. Comparison is achieved by compiling both programs
                                                                           https : / / web. archive . org / web / 20240227002908 / https :
to a common language—in this case assembly—and running
                                                                           //www.whitehouse.gov/wp- content/uploads/2024/02/
the programs in angr. Our approach detects differences in all
                                                                           Final-ONCD-Technical-Report.pdf
explored paths, and concrete examples can be extracted for
                                                                     [5]   Galois and Immunant, C2rust demonstration. [Online].
further use in debugging or in a test suite. Since our framework
                                                                           Available: https://c2rust.com/
is built as a Python library, it is easy to extract the reported
                                                                     [6]   M. Farrukh, S. Shah, B. Coskun, and M. Polychronakis,
data for downstream use. For example, a large language model
                                                                           “SafeTrans: LLM-assisted transpilation from C to rust,”
could consume the textual report output from our tool to
                                                                           arXiv [cs.CR], May 2025.
refine a C to Rust translation. Alternatively, a human operator
                                                                     [7]   M. Weiss, J. Hecking-Harbusch, J. Quante, and M.
can browse the program execution tree using our web based
                                                                           Woehrle, “Feedback loops and code perturbations in
visualization software to quickly gain an understanding of
                                                                           LLM-based software engineering: A case study on a
program behavior.
                                                                           C-to-rust translation system,” arXiv [cs.SE], Dec. 2025.
   Problems with execution performance are currently the most
                                                                     [8]   F. Luo et al., “Integrating rules and semantics for LLM-
significant limitation in using cozy for comparing C and Rust.
                                                                           based C-to-rust translation,” in 2025 IEEE International
We should note here that the performance bottleneck is almost
                                                                           Conference on Software Maintenance and Evolution
always in the interpretation of the binary program itself, not in
                                                                           (ICSME), IEEE, Sep. 2025, pp. 685–696.
the solving of constraints by the SMT solver. We suggest that
                                                                     [9]   T. Zhou et al., “SACTOR: LLM-driven correct and
the most fruitful path forward would be to port the strategies
                                                                           idiomatic C to rust translation with static analysis and
taken by cozy to a more performant symbolic execution engine
                                                                           FFI-based verification,” arXiv [cs.SE], Dec. 2025.
for a suitable IR like Ghidra’s P-code or Valgrind’s VEX -
                                                                    [10]   C. Helbling, G. Leach-Krouse, S. Lasser, and G. Sulli-
perhaps an engine written in Rust rather than angr’s Python.
                                                                           van, “Cozy: Comparative symbolic execution for binary
   Despite these scalability limitations, we are excited that our
                                                                           programs,” in Proceedings of the 2025 Workshop on
existing micropatch analysis tool could be so easily adopted
                                                                           Binary Analysis Research, Reston, VA: Internet Soci-
to compare C and Rust programs. Our tool shows promise in
                                                                           ety, 2025. DOI: 10 . 14722 / bar. 2025 . 23004 [Online].
not only cross-language comparison, but also cross-algorithm
                                                                           Available: https://doi.org/10.14722/bar.2025.23004
comparison. We believe that the techniques outlined in this
                                                                    [11]   Y. Shoshitaishvili et al., “SoK: (State of) The Art of
paper could be extended with additional software engineering,
                                                                           War: Offensive Techniques in Binary Analysis,” in IEEE
leading to broader support of Rust features and capabilities.
                                                                           Symposium on Security and Privacy, 2016. DOI: 10 .
   VIII. M ANDATORY DATA AVAILABILITY S TATEMENT                           1109/SP.2016.17 [Online]. Available: https://doi.org/10.
   The cozy comparative symbolic execution engine is avail-                1109/SP.2016.17
able on our GitHub at draperlaboratory/cozy, and as a               [12]   S. Person, M. B. Dwyer, S. Elbaum, and C. S.
PyPI package under the name cozy-re. The programs from                     Păsăreanu, “Differential Symbolic Execution,” in Foun-
the experimental results section are available on Zenodo at                dations of Software Engineering (FSE), 2008, ISBN:
10.5281/zenodo.19669436.                                                   9781595939951. DOI: 10 . 1145 / 1453101 . 1453131
       [Online]. Available: https://doi.org/10.1145/1453101.
       1453131
[13]   G. P. Farina, S. Chong, and M. Gaboardi, “Relational
       Symbolic Execution,” in Principles and Practice of
       Programming Languages (PPDP), 2019. DOI: 10.1145/
       3354166.3354175 [Online]. Available: https://doi.org/
       10.1145/3354166.3354175
[14]   T. Granlund and P. L. Montgomery, “Division by in-
       variant integers using multiplication,” in Proceedings of
       the ACM SIGPLAN 1994 Conference on Programming
       Language Design and Implementation, ser. PLDI ’94,
       Orlando, Florida, USA: Association for Computing
       Machinery, 1994, 61–72, ISBN: 089791662X. DOI: 10.
       1145/178243.178249 [Online]. Available: https://doi.
       org/10.1145/178243.178249
[15]   A. VanHattum, D. Schwartz-Narbonne, N. Chong, and
       A. Sampson, “Verifying dynamic trait objects in rust,”
       in Proceedings of the 44th International Conference on
       Software Engineering: Software Engineering in Prac-
       tice, ser. ICSE-SEIP ’22, Pittsburgh, Pennsylvania: As-
       sociation for Computing Machinery, 2022, 321–330,
       ISBN : 9781450392266. DOI : 10.1145/3510457.3513031
       [Online]. Available: https://doi.org/10.1145/3510457.
       3513031
[16]   A. Z. Yang, Y. Takashima, B. Paulsen, J. Dodds, and D.
       Kroening, “Vert: Verified equivalent rust transpilation
       with large language models as few-shot learners,” arXiv
       preprint arXiv:2404.18852, 2024.
[17]   Y. Bai and T. Palit, “RustAssure: Differential sym-
       bolic testing for LLM-transpiled C-to-rust code,” arXiv
       [cs.SE], Oct. 2025.
