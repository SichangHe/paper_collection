                                             Diversifying to Verify: When Task-Equivalent
                                                    Programs Differ in Verifiability

                                                                   Shirley Yu1 and Ruben Martins2
                                                            1
                                                              Stanford University, shirleyyu0302@gmail.com
                                                        2
                                                            Carnegie Mellon University, rubenm@andrew.cmu.edu




                                                    Abstract. Program verification is crucial for software correctness,
                                                    but producing fully verified programs remains difficult in practice.
                                                    This paper studies whether implementation structure affects auto-
                                                    mated verifiability when multiple generated programs are intended
                                                    to satisfy the same task-level semantics.
arXiv:2607.09366v1 [cs.SE] 10 Jul 2026




                                                    We present Diversify2Verify, a staged LLM-based pipeline for Why3
                                                    that infers representation-specific contracts, generates and tests di-
                                                    verse recursive and imperative array/list implementations, and at-
                                                    tempts verification with bounded verifier-guided annotation repair.
                                                    We also construct a verification-oriented benchmark of 73 tasks over
                                                    integers, arrays, and lists, yielding 292 implementation variants. Di-
                                                    versify2Verify verifies 96 artifacts initially and 154 after two repair
                                                    passes, improving artifact-level verification from 32.9% to 52.7%. At
                                                    the task level, at least one variant verifies for 49 of 73 tasks, a 67.1%
                                                    success rate. These results show that task-equivalent implementa-
                                                    tions can differ substantially in verifiability and that implementation
                                                    diversity helps find verification-friendly artifacts.

                                               Keywords: Program verification · Implementation diversity · Specifica-
                                               tion generation · Large language models · Why3 · Verifier-guided repair



                                         1   Introduction

                                         Large Language Models (LLMs) have become increasingly effective at synthe-
                                         sizing executable code from natural-language prompts [4]. Generating formally
                                         verified software, however, requires more than code that passes tests. In deduc-
                                         tive verification frameworks such as Why3 [7], a program must be paired with
                                         a formal semantic specification and proof guidance—including preconditions,
                                         postconditions, invariants, variants, assertions, helper predicates, and lemmas—
                                         sufficient for the verifier to prove correctness. This makes verified-code generation
                                         difficult to treat as ordinary code generation. Natural-language tasks are often
                                         ambiguous or incomplete, and concrete examples validate only particular input-
                                         output pairs. A model must therefore infer a mathematical specification [5,15],
                                         implement the algorithm [4,1,13], and synthesize the proof structure needed to
                                         connect the implementation to that specification [16,22]. In a one-shot approach,
2         Yu and Martins

these requirements are entangled. When verification fails, feedback is often am-
biguous, and unconstrained repair may change the specification rather than the
implementation or proof, yielding a program that verifies for the wrong reason.
    This paper asks whether implementation diversity can improve LLM-assisted
deductive verification. Given multiple implementations intended to solve the
same task, do different data representations and control structures lead to differ-
ent verification outcomes? Can generating several variants increase the chance
that at least one has a verification-friendly structure? We use task-equivalent
to mean that variants are generated for the same benchmark task and verified
against representation-specific contracts that are intended to express the same
task-level semantics. We do not prove, as an additional theorem, that the array
and list contracts are equivalent to each other.
    We introduce Diversify2Verify, a staged LLM-based pipeline for generating
and verifying Why3 artifacts from programming tasks and examples. Diver-
sify2Verify separates contract inference, implementation generation, and proof
annotation. It first generates a representation-specific contract with helper def-
initions and test lemmas derived from the examples, then freezes the accepted
contract as the semantic target. It next generates executable WhyML candidates
for the same task, varying representation and implementation style. Finally, it
combines each tested implementation with the frozen contract and adds the
annotations needed for Why3 verification.
    To evaluate this approach, we construct a verification-oriented benchmark
from LeetCodeDataset [27]. Unlike standard code-generation benchmarks that
primarily test executable behavior, our benchmark is designed to study deduc-
tive verification and implementation diversity. We restrict attention to tasks over
integers, arrays, and lists that admit formal contracts, support multiple plausi-
ble implementations, and are suitable for SMT-backed reasoning. The resulting
benchmark contains 73 tasks. For each task, Diversify2Verify generates four vari-
ants, array-recursive, array-imperative, list-recursive, and list-imperative, yield-
ing 292 final verification artifacts.
    Our evaluation shows that implementation structure substantially affects au-
tomated verifiability. Of the 292 generated artifacts, 96 verify initially and 154
verify after two bounded, feedback-guided repair passes, yielding an artifact-level
verification rate of 52.7%. At the task level, at least one variant verifies for 49 of
the 73 tasks, for a success rate of 67.1%. The strongest individual family verifies
44 tasks, indicating that diversity provides a modest but measurable increase in
task coverage. Overall, the results support our central hypothesis: task-equivalent
implementations can differ in verifiability.
    This paper makes the following contributions:

    – A staged LLM pipeline for Why3. We present Diversify2Verify, which
      decomposes verified-code generation into contract inference, implementation
      generation, and proof annotation.
    – Diverse implementation generation. For each task, Diversify2Verify pro-
      duces recursive and imperative variants over array and list representations,
      enabling direct comparison of structurally different programs.
Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability    3

 – A verification-oriented benchmark. We construct a benchmark of 73
   tasks over integers, arrays, and lists, with accepted representation-specific
   contracts and 292 generated implementation artifacts. We release the bench-
   mark, generated Why3 artifacts, and verification logs in a public repository
   available at https://github.com/forge-lab/Diversify2Verify.
 – An empirical study of verifiability. We evaluate how verification success
   varies by representation and implementation style, quantify task-level gains
   from multiple variants, and analyze common remaining proof failures.

2     Background: Why3 and Verification Challenges
This section reviews the Why3 concepts used by Diversify2Verify and explains
how representation and control structure shape proof obligations, causing task-
equivalent implementations to differ in verifiability.

2.1   Deductive Verification in Why3
Deductive verification provides mathematical guarantees about software correct-
ness by proving that an implementation satisfies a formal specification. In Why3,
programs are written in WhyML, which supports both functional and imperative
programming. Why3 generates verification conditions from annotated programs
and delegates them to external SMT solvers and automated theorem provers.
    Correctness is expressed using contracts. A function’s expected input state is
specified with requires clauses, or preconditions, while its guaranteed output
state is specified with ensures clauses, or postconditions. Iterative and recur-
sive constructs usually require additional proof guidance. Loops use invariant
clauses to state properties that hold before the loop and are preserved by every
iteration. They also use variant clauses to provide a strictly decreasing mea-
sure, such as an integer bound or data-structure size, that proves termination.
Recursive functions similarly require contracts and termination arguments.
    Why3 also supports ghost code: proof-only variables, expressions, and state-
ments that help verification without changing executable behavior. Ghost code
is useful for recording logical facts that are implicit in the implementation, such
as which part of the input has been processed, how an accumulator relates to
the specification, or which witness supports a postcondition.

2.2   Representation and Control Structure
The choice of data representation affects the shape of the proof. Array programs
typically require index-based reasoning. Every array access creates bounds obli-
gations, and functional properties often require quantified facts over ranges of
indices. Imperative array algorithms therefore need loop invariants that summa-
rize what is known about processed prefixes, suffixes, or windows.
    List programs shift the burden from index arithmetic to structural reasoning.
They avoid many bounds checks, but specifications often require recursive pred-
icates for properties such as membership, length, occurrences, or substructure.
4        Yu and Martins

       Table 1. Typical proof obligations induced by implementation structure.
    Program choice     Typical proof burden and guidance
    Array + imperative Bounds checks, index arithmetic, and quantified range
                       facts; usually requires loop invariants over processed pre-
                       fixes, suffixes, or windows, sometimes with ghost code to
                       record processed-state summaries.
    Array + recursive Bounds and index obligations remain, but recursive
                       helper contracts can expose smaller subproblems and
                       align proof obligations with recursive calls.
    List + recursive   Structural reasoning over Nil/Cons, length, member-
                       ship, occurrences, and substructure; usually requires re-
                       cursive predicates and helper lemmas.
    List + imperative  Mutable traversal plus structural list reasoning; usually
                       requires invariants and ghost code relating visited ele-
                       ments, remaining elements, and logical summaries used
                       in the specification.



Proofs may then require helper contracts or lemmas that connect these recursive
definitions to the implementation.
    Control structure also matters. Recursive implementations often align with
recursive specifications, allowing proof obligations to follow recursive calls. Im-
perative implementations must instead summarize mutable state with loop in-
variants: an accumulator, index, or reference cell may have an obvious algorith-
mic role, but that role must be made explicit for the verifier.
    Table 1 summarizes the typical proof obligations induced by the four imple-
mentation families studied in this paper. These differences motivate implemen-
tation diversity. Two implementations may be intended to satisfy the same task-
level semantics while producing substantially different verification conditions.
A failed verification attempt may therefore reflect an incorrect implementation,
but it may also reflect a weak invariant, a missing termination argument, or a
helper fact that has not been exposed to the solver. Diversify2Verify tests this
hypothesis by generating array-recursive, array-imperative, list-recursive, and
list-imperative variants for each benchmark task.


3    Diversify2Verify by Example

Figure 1 shows the Diversify2Verify pipeline. Given a task description, target
signature, concrete tests, and target representation, Diversify2Verify separates
generation into three stages: Stage 1 infers a semantic contract, Stage 2 gener-
ates executable implementations, and Stage 3 adds proof annotations to produce
a verification artifact. This separation makes explicit the roles of the three arti-
facts. The contract states what makes a result correct, the implementation com-
putes a candidate result, and the final artifact must provide the proof bridges
that connect local program state to the contract.
Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability                           5

                                 repair spec.                                 repair or
                               or test lemmas                              regenerate code



                    Stage 1 (§4.1)         Run Why3             Stage 2 (§4.2)
   Task +                                                                               Run Why3
                      Contract             on Spec. +          Implementation
  Test Cases                                                                            Test Cases
                     Generation           Test Lemmas            Generation


                                                                                        ✓ Verified
                                                                                       Why3 Artifact
                                          Stage 3 (§4.3)
                                                                 Run Why3
                                               Full
                                                                 Full Verifier
                                           Verification
                                                                                       × Unverified
                                                                                       Why3 Artifact
                                                   repair invariants,             repair budget exhausted
                                                 assertions, or lemmas



Fig. 1. Overview of the Diversify2Verify staged verification pipeline. Why3 is used after
Stage 1 to check the generated specification and test lemmas, during Stage 2 to exe-
cute test cases against candidate implementations, and after Stage 3 to discharge the
verification conditions for the final annotated artifact.


Running example. We use Maximum Distance Between a Pair of Values as a
running example. The function takes two non-increasing, zero-indexed integer
arrays, nums1 and nums2. A pair of indices (i, j) is valid when both indices are
in bounds, i ≤ j, and nums1[i] <= nums2[j]. The distance of a valid pair is
j − i. The task is to return the maximum valid distance, or 0 when no valid pair
has positive distance. For example, given

               nums1 = [30,29,19,5]               nums2 = [25,25,25,25,25],

the index pair (i, j) = (2, 4) is valid because nums1[2] = 19, nums2[4] = 25,
2 ≤ 4, and 19 ≤ 25. Its distance is j − i = 4 − 2 = 2. No valid pair has larger
distance, so the expected output is 2.

Contract generation. Stage 1 defines correctness without describing how to com-
pute the result. For the array version of the running example, the generated
contract captures well-formed inputs, non-increasing arrays, valid index pairs,
pair distances, and maximality.
    The key predicate is maximum_distance_spec. It separates the zero case
from the positive case: a positive result must be realized by some valid pair and
must upper-bound the distance of every valid pair. Thus, the contract specifies
the semantic property of the result, not the algorithm used to compute it. The
full Stage 1 artifact also includes helper definitions and test lemmas derived from
the concrete examples. These test lemmas ensure the contract aligns with the
concrete examples, though passing them does not guarantee the natural-language
task is perfectly captured.
6        Yu and Martins

                                                                                   
1    predicate valid_pair
2      (nums1: array int) (nums2: array int) (i: int) (j: int) =
3      0 ≤ i < length nums1 ∧ 0 ≤ j < length nums2 ∧
4      i ≤ j ∧ nums1[i] ≤ nums2[j]
5
6    predicate has_pair_distance
7      (nums1: array int) (nums2: array int) (d: int) =
8      exists i j: int.
9        valid_pair nums1 nums2 i j ∧ d = pair_distance i j
10
11   predicate distance_upper_bound
12     (nums1: array int) (nums2: array int) (d: int) =
13     forall i j: int. valid_pair nums1 nums2 i j → pair_distance i j ≤ d
14
15   predicate maximum_distance_spec
16     (nums1: array int) (nums2: array int) (res: int) =
17     (res = 0 ∧ no_positive_distance_pair nums1 nums2) ∨
18     (0 < res ∧ has_pair_distance nums1 nums2 res ∧
19      distance_upper_bound nums1 nums2 res)
20
21   val maximum_distance_between_a_pair_of_values_array
22     (nums1: array int) (nums2: array int) : int
23     requires { valid_input nums1 nums2 }
24     ensures { maximum_distance_spec nums1 nums2 result }
                                                                                   
Implementation generation. Stage 2 generates executable WhyML candidates for
the same semantic task. For the running example, the array-imperative variant
uses the standard two-pointer scan, maintaining indices i and j and a reference
best for the largest distance found so far. When nums1[i] <= nums2[j], the
implementation updates best and advances j; otherwise, it advances i.

Full verification. Stage 3 combines an accepted contract with a tested imple-
mentation and adds the annotations needed for Why3 verification. For the array-
imperative variant, the main challenge is to prove that the local two-pointer scan
establishes the global maximality condition required by maximum_distance_spec.
                                                                                  
1    while !i < length nums1 && !j < length nums2 do
2      invariant { 0 ≤ !i ≤ length nums1 }
3      invariant { 0 ≤ !j ≤ length nums2 }
4      invariant { 0 ≤ !best }
5      invariant { !best = 0 ∨ has_pair_distance nums1 nums2 !best }
6      invariant { processed_j_upper_bound nums1 nums2 !j !best }
7      invariant { left_future_excluded nums1 nums2 !i !j }
8      variant   { (length nums1 - !i) + (length nums2 - !j) }
9    (* loop body *)
10   done
                                                                                   
   The initial invariants establish basic safety facts about the loop indices and
the current value of best. The witness invariant connects best to the contract by
Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability          7

                    Table 2. Repair boundaries in Diversify2Verify.
    Stage          Policy
    Stage 1:       Repair syntax/type errors, helper definitions, example lem-
    Contract       mas, and semantic mistakes before freezing; the accepted
                   representation-specific contract is then fixed.
    Stage 2:       Repair or regenerate executable code only within the same
    Implementation representation and control-structure family.
    Stage 3:       Add proof scaffolding such as invariants, assertions, ghost code,
    Verification   internal helper contracts, and lemmas; preserve the contract,
                   implementation family, and executable behavior.

requiring that any positive value of best is realized by some valid pair. The final
two invariants provide the main proof bridge. processed_j_upper_bound states
that all valid pairs with already processed right indices have distance at most
best, while left_future_excluded justifies discarding left indices that cannot
produce better future pairs. Together, these annotations connect the local state
of the two-pointer scan to the global maximality condition in the postcondition.
    For this task, the array-imperative and array-recursive variants verify without
repair, whereas the list-recursive and list-imperative variants require two repair
attempts. Since the task is naturally array-oriented, this example should not be
read as evidence that arrays are generally easier to verify. It instead illustrates
the broader point studied in our evaluation: representation and control-structure
choices can substantially change verification effort.


4      Generation and Repair Policies
Section 3 described the pipeline through one task. We now summarize the policies
used across all benchmarks. These policies define what each stage may generate,
what each stage may repair, and which semantic boundaries must be preserved.
    Table 2 summarizes the policy enforced at each stage. The central rule is a
frozen-contract discipline: once a Stage 1 contract is accepted for a representa-
tion, later stages may repair implementations and proof annotations, but they
may not change the public semantic target for that representation.

4.1     Contract generation policy
Stage 1 takes a natural-language problem statement, a target signature, con-
crete examples, and a target representation. It produces a representation-specific
Why3 contract containing the target declaration, preconditions, postconditions,
and any helper predicates or logical functions needed to express the task.
    The natural-language description is treated as the primary source of semantic
intent. Examples are used as concrete checks and as limited evidence for resolv-
ing ambiguity, but not as a complete behavioral specification. Stage 1 therefore
separates assumptions about valid inputs from requirements on the output. In-
put assumptions become requires clauses or explicit validity predicates, while
output requirements become ensures clauses.
8      Yu and Martins

    The contract is written in the reasoning style of the target representation.
Array contracts use lengths, explicit bounds, and bounded quantification over
indices. List contracts use structural definitions over Nil and Cons, or standard
list-library notions when they match the task. The goal is not to mechanically
translate between arrays and lists, but to produce representation-appropriate
contracts that capture the same underlying task. Thus, we use task-equivalent to
mean that the array and list variants target the same benchmark-level semantics
through representation-specific contracts; we do not additionally prove that the
two formal contracts are logically equivalent.
    Stage 1 favors direct mathematical characterizations over executable-looking
specifications. For optimization tasks, the postcondition usually separates feasi-
bility from optimality: the result must be achieved by a valid witness, and no
valid witness may have a better value. For Boolean, counting, and transformation
tasks, the postcondition states the exact semantic relation between the inputs
and the returned value.
    After generation, the Stage 1 artifact is first parsed and type-checked by
Why3. We then run a separate Stage 1 validation pass that attempts to prove the
example-derived test lemmas. These lemmas instantiate the generated contract
on concrete benchmark examples and serve as a lightweight consistency check
between the contract and the examples. They do not prove that the contract
fully captures the natural-language task. We therefore use accepted contract to
mean a representation-specific contract that is well formed in Why3 and whose
example-derived test lemmas are discharged by the Stage 1 validation procedure,
possibly after one repair attempt. Acceptance is not a proof of full semantic
correctness with respect to the natural-language task.
    Repair is guided by the kind of Stage 1 failure. Syntax and type errors are
fixed directly. If the artifact type-checks but the separate Stage 1 validation
pass fails to prove the example-derived lemmas, its diagnostics are passed to
at most one Stage 1 repair call. This repair may add assertions, unfold helper
definitions, or simplify logically equivalent helper predicates. Semantic repair is
allowed only before freezing, and only when the contract is inconsistent with the
task statement or examples. Once the artifact is well formed and its example-
derived lemmas are proved, the accepted contract is frozen for later stages.

4.2   Implementation diversity policy
Stage 2 generates executable WhyML candidates. For each benchmark task,
Diversify2Verify generates four implementation families: array-recursive, array-
imperative, list-recursive, and list-imperative. Recursive variants use structural
recursion or recursive helpers. Imperative variants use loops, mutable references,
and explicit state updates.
   Within a fixed family, the implementation may choose the algorithmic strat-
egy, traversal order, helper decomposition, and accumulator structure. Dur-
ing repair, however, it must preserve the accepted Stage 1 contract, the re-
quested representation, and the requested control-structure family. Thus, an
array-imperative candidate may be repaired into a different array-imperative
Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability      9

algorithm, but it may not become list-based or recursive, and it may not modify
the contract it is checked against.
    Diversity is introduced to preserve the proof-obligation differences summa-
rized in Table 1. By generating one recursive and one imperative implementation
for each representation, the evaluation can measure how data representation and
control structure affect verifiability while keeping the accepted Stage 1 contract
fixed within each representation.
    Each candidate is checked by type checking and by executable tests derived
from the benchmark examples. Failed candidates are repaired or regenerated
within a bounded budget of five attempts while preserving their representation
and implementation style. Passing these tests does not establish correctness; it
only determines which candidates are submitted to Stage 3.

4.3   Final verification repair policy
Stage 3 turns one tested implementation into a deductive verification artifact.
It combines the Stage 1 contract with the Stage 2 implementation and removes
the executable tests, which are no longer part of the final proof artifact. It then
adds proof scaffolding such as internal helper contracts, loop invariants, variants,
assertions, ghost code, and auxiliary lemmas. These annotations may strengthen
the proof context, but they may not weaken or replace the Stage 1 contract.
    The main proof obligation is to bridge local program state to the semantic
contract generated in Stage 1. Local state includes loop indices, recursive argu-
ments, accumulators, partial results, and mutable references. Stage 3 annotations
are therefore proof guidance: they expose the relationship between these local
quantities and the specification without changing the meaning of the program.
    The generated verification conditions cover safety, termination, and func-
tional correctness. Safety obligations prove that operations such as array accesses
and pattern matches are well defined. Termination obligations are discharged
using loop or recursion variants. Functional-correctness obligations require the
proof scaffolding to imply the Stage 1 postconditions at loop exits, recursive base
cases, and helper returns.
    If verification fails, Stage 3 repair is restricted to proof-oriented changes us-
ing two repair attempts. Typical repairs strengthen loop invariants, add missing
variants, insert local assertions, introduce ghost code, or prove helper lemmas
that expose facts needed by the SMT solvers. Local implementation edits are per-
mitted only when they are semantics-preserving refactorings or proof-enabling
local changes that preserve the implementation family and executable behavior
on valid inputs. Stage 3 may not weaken the Stage 1 contract, add stronger
preconditions to the target entry point, change the target signature, switch be-
tween array and list representations, or replace a recursive implementation with
an imperative one or vice versa to make verification easier.
    These restrictions are imposed by the Stage 3 prompts and repair driver, but
the LLM is not a trusted enforcement mechanism. We therefore treat preserva-
tion of the frozen Stage 1 contract as a property to be checked after generation,
rather than as something guaranteed by the prompt alone. A successful Stage 3
10      Yu and Martins

                  Table 3. Summary of the verification benchmark.

       Property                                                           Value
       Unique tasks                                                          73
       Available tests per task     min 25, median 109, mean 106.7, max 178
       Input arity              30 one-arg, 34 two-arg, 7 three-arg, 2 four-arg
       Return shape                                 58 integer, 15 array or list


run produces a fully verified Why3 artifact. A failed run produces the best un-
verified artifact together with verifier diagnostics and repair traces.


5    Benchmark Construction

We construct the benchmark from LeetCodeDataset [27], which provides Leet-
Code-style Python programming problems with natural-language descriptions
and executable test cases. Because LeetCode problems are public, we do not
claim that this benchmark is contamination-free or that it measures a model’s
ability to solve unseen programming tasks. The descriptions, standard algo-
rithms, or Python solutions may have appeared in model training data. We
instead use LeetCodeDataset as a source of task descriptions and tests for con-
structing a controlled verification benchmark. The evaluated artifacts—Why3
contracts, WhyML implementations, proof annotations, repair traces, and ver-
ifier outcomes—are generated by our pipeline and are not part of the original
dataset. While potential contamination might help the model recognize the un-
derlying algorithmic task, our main measurement is comparative: whether dif-
ferent representation and control-structure choices lead to different verification
outcomes under the same verifier and repair budget.
     Starting from roughly 2,900 tasks, we first filtered for problems over primitive
values and integer sequences, such as arrays and lists, excluding strings, trees,
floating-point values, and other structures that would require additional Why3
modeling. This type-based pruning produced approximately 1,000 candidates.
We then used an LLM-assisted triage pass to retain tasks whose behavior ap-
peared expressible with arithmetic and integer-sequence properties and that ad-
mitted multiple plausible implementation strategies, reducing the set to around
150 benchmarks. Finally, we applied the Stage 1 contract-generation and valida-
tion procedure from Section 4.1. We retained only benchmarks for which Stage 1
produces accepted contracts for the target representations used in the evalua-
tion. As in Section 4.1, acceptance means that the contract is well formed in
Why3 and that the example-derived validation lemmas are discharged, possibly
after repair. This filter yielded 73 benchmark tasks and is part of the benchmark
construction process rather than an independent Stage 1 success result.
     Table 3 summarizes the final benchmark. The retained set contains 73 tasks
with varying input arities, return shapes, and test-suite sizes. For each task, Di-
versify2Verify generates four implementation variants, yielding 292 artifacts. The
benchmark should therefore be read as a controlled verification benchmark, not
Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability   11

as a representative sample of arbitrary LeetCode tasks: it is intentionally biased
toward SMT-friendly data types, tractable specifications, and tasks with ac-
cepted Stage 1 contracts. This selection lets us isolate the paper’s main question:
how representation and control-structure choices affect deductive verifiability.


6   Implementation

Diversify2Verify is implemented as a scripted, non-interactive pipeline around
Codex. We use Codex as the programming agent: it receives a stage prompt,
applies the local stage instructions, creates or edits WhyML files, and returns
a candidate artifact. The underlying model configuration is selected per stage.
Stages 1 and 3 use GPT-5.5 with high reasoning, because these stages involve
formal specification and proof construction. Stage 2 uses GPT-5.4 with medium
reasoning, because this stage primarily generates executable implementations
that are later checked against the accepted contract.
    Each stage is invoked by a driver script. The driver builds a prompt from the
benchmark description, target signature, examples, target representation, and,
when applicable, the implementation family. It then invokes Codex, extracts the
WhyML artifact, runs the checks, and either accepts the artifact or launches a
bounded repair attempt. The drivers are non-interactive: all inputs, model con-
figurations, checker commands, and repair budgets are fixed before evaluation.
    The Codex context includes a local skill for each stage. A skill is a stage-
specific instruction file that describes the expected WhyML artifact shape, per-
mitted Why3 libraries, representation-specific idioms, checker commands, and
common failure patterns. The Stage 1 skills focus on contract structure, helper
predicates, and example-derived test lemmas. The Stage 2 skills focus on exe-
cutable recursive or imperative WhyML code for the selected representation. The
Stage 3 skills focus on proof-oriented annotations, including invariants, variants,
assertions, ghost state, internal helper contracts, and auxiliary lemmas.
    During generation, each driver performs only the checks needed to reject
malformed artifacts early. Stage 1 contracts and Stage 3 verification artifacts
must parse and type-check in Why3. Stage 2 implementations must additionally
pass the selected executable tests. These fast checks prevent invalid artifacts
from flowing to later stages, but they do not require all proof obligations to be
discharged.
    For each representation-specific Stage 1 contract, the validation pass at-
tempts to prove seven example-derived lemmas. For Stage 2, each candidate
implementation is checked on 20 executable tests selected from the benchmark
test suite. These tests are used only as filtering checks before Stage 3; they are
not part of the final deductive verification artifact.
    Full verification is run by a separate Why3 verifier driver rather than by
Codex itself. In our experiments, we used Why3 1.8.2 together with the SMT
solvers Z3 4.8.6, Alt-Ergo 2.4.0, and CVC4 1.8, using a 10-second timeout per
solver call. The verifier first attempts direct proving with this solver portfolio.
For goals that remain, it applies increasingly aggressive Why3 transformations,
12     Yu and Martins

            Table 4. Generation configuration used by Diversify2Verify.
Stage          Task and feedback                    Model                 Budget
Stage 1:       Generate a representation-specific   GPT-5.5 (high)        1 repair
Contract       contract; type-check it and validate
               example lemmas.
Stage 2:       Generate executable WhyML;           GPT-5.4               5 attempts
Implementation check with type checking and         (medium)
               executable tests.
Stage 3:       Add proof annotations; repair using GPT-5.5 (high)         2 repairs
Verification   Why3 verification diagnostics.


first splitting large verification conditions and then inlining helper definitions
when needed. An artifact is counted as verified only if all generated verification
conditions are discharged by this verifier configuration. When Stage 3 verification
fails, the verifier diagnostics are passed back to Codex only as feedback for the
bounded repair calls summarized in Table 4.
    When verification or filtering fails, Diversify2Verify relies on bounded, log-
guided Codex calls for repair (summarized in Table 4). Each repair prompt
includes the failed artifact, the relevant checker or verifier diagnostics, and the
stage inputs needed to preserve context. For Stage 3, this includes the fail-
ing Why3 file, the verifier log, the benchmark description, the frozen Stage 1
specification, and the tested Stage 2 implementation. The first repair attempt
addresses the initial failure. Later attempts use the updated diagnostics to focus
on the remaining unproved goals. Each repaired artifact is then rechecked by the
corresponding driver.


7    Evaluation

Our evaluation focuses on Stage 3, where Diversify2Verify attempts to turn exe-
cutable WhyML implementations into deductively verified artifacts. Stage 1 and
Stage 2 serve as prerequisite filters for this experiment. Stage 1 admits tasks for
which both array and list contracts are accepted, and Stage 2 admits only imple-
mentations that pass type checking and executable tests. The main evaluation
therefore begins after these filters: given an accepted contract and a diverse set
of tested implementations, can Stage 3 produce fully verified artifacts, and which
representation or implementation style is easiest to verify?

Pipeline setup results. The benchmark contains 73 tasks after the Stage 1 ac-
ceptance filter described in Section 5. Because each retained task has accepted
array and list contracts by construction, the evaluation uses 146 representation-
specific Stage 1 contracts. Of these accepted contracts, 85 required no repair
and 61 required one contract-repair attempt. The array contracts account for 45
initially accepted contracts and 28 accepted after repair, while the list contracts
account for 40 initially accepted contracts and 33 accepted after repair.
Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability          13

Table 5. Overall Stage 3 verification results. Repair increases the number of verified
artifacts from 96 initially to 154 after two repair passes.

      Attempt           Newly verified Cumulative verified Remaining Cumulative rate
      Initial Stage 3              96                 96        196           32.9%
      After repair 1               35                131        161           44.9%
      After repair 2               23                154        138           52.7%


    Stage 2 targets four variants per task: array-recursive, array-imperative, list-
recursive, and list-imperative. Within the five-attempt Stage 2 budget, Diver-
sify2Verify obtains one type-checked, test-passing implementation for each vari-
ant, yielding 292 candidates for Stage 3. The main evaluation therefore centers
on the 292 final verification artifacts produced by combining these tested imple-
mentations with the accepted Stage 1 contracts.

Research Questions. We evaluate three research questions:
RQ1: Verification effectiveness. How often does Stage 3 verify the imple-
  mentations, and how much do repair passes improve the verification rate?
RQ2: Representation and implementation diversity. How does verifica-
  tion success vary across array and list representations and across recursive
  and imperative implementations? Does generating multiple variants increase
  the chance of obtaining at least one verified artifact for a task?
RQ3: Remaining proof failures. For artifacts that remain unverified after
  repair, what kinds of proof obligations are left?

7.1     RQ1: Verification effectiveness
Table 5 summarizes the overall Stage 3 results. Of the 292 verification artifacts,
96 verify as generated. The first Codex-assisted repair pass verifies 35 additional
artifacts, and the second repair pass verifies 23 more. Overall, Diversify2Verify
verifies 154 artifacts after repair, corresponding to a final artifact-level verifica-
tion rate of 52.7%.
    Repair is therefore responsible for a substantial fraction of the final successes.
Among the 154 verified artifacts, 58 require at least one repair pass. The first
repair pass gives the larger improvement, but the second pass still verifies 23
artifacts that remain unproved after the first repair.
    Most artifacts are proved without requiring the most aggressive Why3 trans-
formations. Among the 154 verified artifacts, 133 are proved directly, 13 require
splitting verification conditions, and 8 require both splitting and inlining helper
definitions. This suggests that once the right contracts, invariants, and assertions
are present, most verified artifacts are within reach of the base SMT portfolio.

7.2     RQ2: Representation and implementation diversity
At the task level, diversity increases the chance of obtaining a verified solution.
For each task, we generate four variants, corresponding to the cross-product of
14      Yu and Martins

Table 6. Task-level verification outcomes over the 73 benchmark tasks. A task is
counted as solved if at least one of its four variants verifies after repair.

                   Task-level outcome                Tasks % of tasks
                   No variant verified                  24     32.9%
                   Exactly one variant verified          5      6.8%
                   Exactly two variants verified         7      9.6%
                   Exactly three variants verified      13     17.8%
                   All four variants verified           24     32.9%
                   At least one variant verified        49     67.1%

Table 7. Stage 3 verification results by representation and implementation style. Re-
cursive variants verify more often than imperative variants, while array and list repre-
sentations have similar final verification rates.

     Variant            Total Initial Repair 1 Repair 2 Verified Unverified Rate
     Array recursive      73     28        11          5      44         29 60.3%
     Array imperative     73     21         7          7      35         38 47.9%
     List recursive       73     30         7          3      40         33 54.8%
     List imperative      73     17        10          8      35         38 47.9%
     Total               292     96        35         23     154        138 52.7%


representation and implementation style: array-recursive, array-imperative, list-
recursive, and list-imperative. Table 6 groups the 73 tasks by how many of these
variants verify after repair. At least one variant verifies for 49 tasks, giving a
task-level success rate of 67.1%. Among these 49 solved tasks, 25 are solved
by only a subset of the variants, showing that different implementations make
different tasks amenable to verification.
    Shifting from task-level success to individual artifact performance, Table 7
breaks down verification by representation and implementation style. Overall,
recursive implementations verify more often than imperative implementations.
Across both representations, 84 of 146 recursive artifacts verify, compared with
70 of 146 imperative artifacts. Array and list representations are closer overall:
79 of 146 array artifacts verify, compared with 75 of 146 list artifacts. The
strongest individual variant family is array-recursive with 44 verified artifacts,
followed closely by list-recursive with 40. Both imperative families trail behind,
verifying 35 artifacts each.
    This difference is not surprising in a deductive-verification setting. Many
Stage 1 specifications are expressed using recursive logical functions or induc-
tive predicates. Recursive implementations often follow the same structure, so
the proof can proceed by exposing the contract of each recursive call. In con-
trast, imperative implementations require loop invariants that summarize the
entire processed portion of the input and relate mutable program state to the
logical specification. These invariants are often the hardest part of the proof to
synthesize automatically.
Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability    15

    The repair results suggest that imperative implementations are not worse
executable candidates; they are harder to verify automatically. Before repair, re-
cursive variants verify substantially more often than imperative variants. Repair
narrows this gap by verifying 26 additional recursive artifacts and 32 additional
imperative artifacts. This suggests that many imperative failures are due to
missing proof structure, such as loop invariants, variants, and bridge assertions,
rather than an incorrect implementation strategy.
    Thus, diversity helps not because one representation dominates, but because
different variants expose different proof opportunities. Recursive implementa-
tions often align better with recursive specifications, while imperative ones can
become competitive once repair adds the missing loop-level proof structure.


7.3   RQ3: Remaining proof failures

After two repair passes, 138 artifacts remain unverified, even though all cor-
responding Stage 2 implementations passed type checking and executable tests.
These failures are therefore not failures to obtain type-checked, test-passing can-
didates; they arise at the deductive verification stage.
     Many of these failures are close to verification. Among the 138 unverified
artifacts, 62 have only one remaining unproved root goal, and 110 have at most
three. The average number of remaining root goals is 2.5. This suggests that
many failures are localized proof gaps rather than evidence of fundamentally
incorrect implementations.
     The array-imperative artifact for the Longest Turbulent Subarray benchmark
illustrates this pattern. The task is to return the length of the longest contiguous
segment whose adjacent comparisons strictly alternate; equal adjacent elements
break the segment. The implementation performs the standard linear scan, track-
ing the current turbulent suffix and the best length seen so far. Its last remaining
obligation arises when the current comparison alternates with the previous one,
so the suffix is extended. The missing bridge is that any turbulent interval ending
at i+1 can be shortened to one ending at i; the previous maximality invariant
then bounds its length by old_current + 1. We confirmed this diagnosis in a
manual follow-up: adding proof-only helper lemmas for suffix-shortening and for
lifting the previous bound to all intervals ending at i+1 discharged the remaining
goal, without changing the executable code or weakening the specification. This
repair was not included in the reported results, but it shows that at least some
failures are due to missing proof structure rather than incorrect artifacts.
     This example illustrates a common remaining failure mode: the generated
proof scaffolding does not expose the semantic bridge needed by the SMT solvers.
Across the remaining failures, we see similar gaps involving insufficient loop
invariants, missing helper contracts, array bounds or index arithmetic, structural
list reasoning, and reasoning about counting, cardinality, or optimality.
     Overall, the remaining failures suggest two directions for improvement. Re-
pair prompts could target bridge obligations more directly, such as connecting
helper postconditions, loop invariants, or accumulator meanings to the specifi-
16      Yu and Martins

cation. The pipeline could also include specialized proof patterns for recurring
domains such as index-range reasoning, counting, and optimization.

7.4   Discussion and limitations
The Stage 3 results show that both repair and implementation diversity matter.
Repair increases artifact-level verification from 96 of 292 artifacts, or 32.9%, to
154 of 292 artifacts, or 52.7%. At the task level, using all four variants yields at
least one verified artifact for 49 of 73 tasks, or 67.1%, compared with 44 tasks
for the strongest individual family.
    Importantly, these results are relative to the accepted Stage 1 contracts. De-
ductive verification proves that a Stage 3 implementation satisfies its contract,
not that the contract fully captures the natural-language benchmark description.
To assess this specification risk, we ran a screening audit using GPT-5.5 (con-
figured for high reasoning) on the 292 final artifacts. The judge evaluated two
criteria: whether the Stage 1 specification matched the benchmark description,
and whether Stage 3 preserved that specification.

Specification Match The judge flagged 10 potential mismatches. Because the 146
Stage 1 contracts are reused across variants, we manually inspected these flagged
cases to find the root cause. Only one case corresponded to a specification that
was genuinely too weak and could potentially accept incorrect programs. Seven
cases involved missing input-bound constraints typical of LeetCode problems;
however, these omissions did not affect the intended behavior on valid inputs.
The remaining two cases involved inconsistencies between generated tests and
stated input constraints; these tests were preemptively excluded before Stage 2
testing.

Specification Preservation The judge flagged only one artifact for failing to pre-
serve the contract. Here, Stage 3 added preconditions that were implied by the
benchmark description but absent from the frozen Stage 1 contract—a clear vi-
olation of our strict Stage 3 policy. Overall, this 291-of-292 success rate demon-
strates that the pipeline reliably preserves the boundary between specification
generation and proof repair.

Limitations Several threats to validity remain. First, the LLM judge is an au-
dit mechanism, not a formal guarantee; subtle specification errors may persist.
Second, all generation, repair, and evaluation steps use GPT-family models;
other LLMs may yield different verification and repair behaviors. Third, passing
Stage 2’s finite executable tests does not establish functional correctness, which
is only attempted in Stage 3. Fourth, because the benchmark is filtered through
Stage 1, our results specifically measure verification on tasks where both array
and list contracts were successfully accepted. Finally, our focus on integer and
sequence tasks means these conclusions may not directly transfer to programs
requiring richer heap structures, floating-point arithmetic, concurrency, or ex-
ternal libraries. Furthermore, some remaining failures likely reflect limitations of
the SMT portfolio rather than fundamentally unprovable implementations.
Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability    17

8   Related Work

LLM-based code generation. Large language models have been widely studied
for generating executable programs from natural-language prompts. Benchmarks
and systems such as Codex and HumanEval [4], MBPP [1], and AlphaCode [13]
established test-based functional correctness as the dominant evaluation crite-
rion for LLM code generation. In this setting, diversity is usually a sampling
mechanism: generating many candidates increases the chance that one passes
the available tests. Diversify2Verify uses tests only as an intermediate filter. The
final artifact must also include a formal contract and enough proof guidance for
Why3 to prove that the implementation satisfies that contract. Thus, our use of
diversity is different from pass@k-style sampling: we study whether alternative
representations and control structures lead to verification conditions that are
easier or harder for SMT-backed deductive verification.


Deductive verification and formal proof systems. Diversify2Verify is built on
Why3 [7] and is related to other deductive verification systems such as Dafny [12],
Viper [19], and Verus [11], as well as proof assistants such as Lean [17] and
Rocq [20]. These systems provide languages for programs, specifications, and
proofs, but also expose the central challenge addressed in this paper: verified
programming requires not only code, but also contracts, invariants, lemmas,
ghost state, and other proof structure. We use Why3 because WhyML sup-
ports both functional and imperative programming while making the separation
between executable code, specifications, and proof artifacts explicit. Although
other deductive verifiers could serve this role, Why3 allows us to compare re-
cursive and imperative implementations over arrays and lists within a single,
unified framework. Our goal is not to introduce a new verifier, but to study how
LLM-generated program variants interact with an existing deductive verifier.


LLMs for formal reasoning and verified program synthesis. Recent work has
used LLMs for autoformalization, theorem proving, and verifier-guided program
generation. Autoformalization translates informal mathematical statements into
formal languages [26,9], while systems such as LeanDojo [29] and Baldur [8] use
LLMs together with proof-assistant feedback, retrieval, or automated provers to
construct formal proofs. Other systems integrate LLMs directly with program
verifiers. A large body of work focuses on Dafny, including systems that gener-
ate assertions (Laurel [18], Daisy [23]), evaluate annotation generation (Dafny-
Bench [14]), study AI-assisted method synthesis (Misu et al. [16]), and check con-
sistency between code and docstrings (Clover [24]). Similar efforts target Rust
via Verus (AutoVerus [28]) or integrate LLMs broadly with automated reason-
ers (Lemur [25]).Diversify2Verify is complementary to these systems. Rather than
asking only whether an LLM can produce one verified program or missing an-
notations for a fixed program, we ask whether the form of the implementation
affects verifiability.
18      Yu and Martins

Specification generation, proof guidance, and repair. Our first stage builds on
prior work translating informal intent into formal postconditions [5] and LLM-
based specification generation with verification-guided selection [15]. These sys-
tems highlight a central risk in LLM-assisted verification: a specification can be
verifiable while failing to capture the intended behavior. Diversify2Verify miti-
gates this risk by using examples to check the specification against the natural-
language task and by using an LLM judge, followed by manual inspection, to
analyze cases where the specification may not match the intended semantics.
    Our final stage is related to invariant generation and proof guidance. Clas-
sical tools such as Daikon [6] dynamically infer likely invariants, while recent
work studies LLM generation and ranking of loop invariants [3,10,21] and neu-
ral synthesis for SMT-assisted proof-oriented programming [2]. Diversify2Verify
also performs bounded repair, but with stage-specific boundaries: Stage 1 may
repair the specification before freezing, Stage 2 may regenerate code only within
the chosen representation and family, and Stage 3 may refine proof scaffolding
while preserving the contract and implementation family. These boundaries pre-
vent verification from succeeding by weakening the specification or replacing a
difficult implementation with an easier one.



9    Conclusion

Generating verified programs from natural language requires more than infer-
ring a correct specification: it also requires an implementation whose structure
is amenable to deductive verification. This paper introduced Diversify2Verify, a
staged LLM-based approach that exploits this observation by generating multi-
ple task-equivalent implementations across representation and control-structure
families and checking them against fixed representation-specific contracts.
     The main result is that implementation diversity improves task coverage.
Across 73 benchmark tasks and 292 generated artifacts, Diversify2Verify verifies
96 artifacts initially(32.9%), and 154 after two repair passes(52.7%). At the task
level, at least one variant verifies for 49 tasks, yielding a 67.1% success rate.
Recursive variants verify more often than imperative variants, while array and
list representations have similar aggregate rates. These results demonstrate that
task-equivalent implementations can differ substantially in verifiability, and that
generating diverse variants increases the chance of finding one a verifier can prove
correct.
     Future work should extend this diversity-oriented methodology to richer
data structures, strings, floating-point arithmetic, and library-based programs.
It should also explore stronger invariant generation, better failure classification,
and formal equivalence between representation-specific contracts. Applying this
approach to other systems, such as Verus, would help distinguish Why3-specific
engineering effects from a broader principle: implementation diversity is a pow-
erful, practical tool for LLM-assisted verified programming.
Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability        19

Acknowledgments

This work was partially supported by the National Science Foundation (NSF)
under Award CCF2427581 and DARPA under Agreement FA8750-24-9-1000.


References

 1. Austin, J., Odena, A., Nye, M.I., Bosma, M., Michalewski, H., Dohan, D., Jiang, E.,
    Cai, C.J., Terry, M., Le, Q.V., Sutton, C.: Program Synthesis with Large Language
    Models. CoRR abs/2108.07732 (2021)
 2. Chakraborty, S., Ebner, G., Bhat, S., Fakhoury, S., Fatima, S., Lahiri, S.K., Swamy,
    N.: Towards Neural Synthesis for SMT-Assisted Proof-Oriented Programming. In:
    ICSE. pp. 1755–1767. IEEE (2025)
 3. Chakraborty, S., Lahiri, S.K., Fakhoury, S., Musuvathi, M., Lal, A., Rastogi, A.,
    Senthilnathan, A., Sharma, R., Swamy, N.: Ranking LLM-Generated Loop Invari-
    ants for Program Verification. CoRR abs/2310.09342 (2023)
 4. Chen, M., Tworek, J., Jun, H., Yuan, Q., de Oliveira Pinto, H.P., Kaplan, J.,
    Edwards, H., Burda, Y., Joseph, N., Brockman, G., Ray, A., Puri, R., Krueger,
    G., Petrov, M., Khlaaf, H., Sastry, G., Mishkin, P., Chan, B., Gray, S., Ryder, N.,
    Pavlov, M., Power, A., Kaiser, L., Bavarian, M., Winter, C., Tillet, P., Such, F.P.,
    Cummings, D., Plappert, M., Chantzis, F., Barnes, E., Herbert-Voss, A., Guss,
    W.H., Nichol, A., Paino, A., Tezak, N., Tang, J., Babuschkin, I., Balaji, S., Jain,
    S., Saunders, W., Hesse, C., Carr, A.N., Leike, J., Achiam, J., Misra, V., Morikawa,
    E., Radford, A., Knight, M., Brundage, M., Murati, M., Mayer, K., Welinder, P.,
    McGrew, B., Amodei, D., McCandlish, S., Sutskever, I., Zaremba, W.: Evaluating
    large language models trained on code. CoRR abs/2107.03374 (2021)
 5. Endres, M., Fakhoury, S., Chakraborty, S., Lahiri, S.K.: Can Large Language Mod-
    els Transform Natural Language Intent into Formal Method Postconditions? Proc.
    ACM Softw. Eng. 1(FSE), 1889–1912 (2024)
 6. Ernst, M.D., Perkins, J.H., Guo, P.J., McCamant, S., Pacheco, C., Tschantz, M.S.,
    Xiao, C.: The Daikon system for dynamic detection of likely invariants. Sci. Com-
    put. Program. 69(1-3), 35–45 (2007)
 7. Filliâtre, J.C., Paskevich, A.: Why3—where programs meet provers. In: ESOP. pp.
    125–128. Springer (2013)
 8. First, E., Rabe, M.N., Ringer, T., Brun, Y.: Baldur: Whole-proof generation and
    repair with large language models. In: FSE. pp. 1229–1241. ACM (2023)
 9. Kabra, A., Laurent, J., Bharadwaj, S., Martins, R., Mitsch, S., Platzer, A.: Can
    Large Language Models Autoformalize Kinematics? In: FMCAD. TU Wien Aca-
    demic Press (2025)
10. Kamath, A., Senthilnathan, A., Chakraborty, S., Deligiannis, P., Lahiri, S.K., Lal,
    A., Rastogi, A., Roy, S., Sharma, R.: Finding inductive loop invariants using large
    language models. CoRR abs/2311.07948 (2023)
11. Lattuada, A., Hance, T., Cho, C., Brun, M., Subasinghe, I., Zhou, Y., Howell, J.,
    Parno, B., Hawblitzel, C.: Verus: Verifying rust programs using linear ghost types.
    Proc. ACM Program. Lang. 7(OOPSLA1), 286–315 (2023)
12. Leino, K.R.M.: Dafny: An Automatic Program Verifier for Functional Correctness.
    In: LPAR. pp. 348–370. LNCS, Springer (2010)
20      Yu and Martins

13. Li, Y., Choi, D.H., Chung, J., Kushman, N., Schrittwieser, J., Leblond, R., Ec-
    cles, T., Keeling, J., Gimeno, F., Lago, A.D., Hubert, T., Choy, P., de Mas-
    son d’Autume, C., Babuschkin, I., Chen, X., Huang, P., Welbl, J., Gowal, S.,
    Cherepanov, A., Molloy, J., Mankowitz, D.J., Robson, E.S., Kohli, P., de Freitas,
    N., Kavukcuoglu, K., Vinyals, O.: Competition-Level Code Generation with Al-
    phaCode. CoRR abs/2203.07814 (2022)
14. Loughridge, C., Sun, Q., Ahrenbach, S., Cassano, F., Sun, C., Sheng, Y., Mudide,
    A., Misu, M.R.H., Amin, N., Tegmark, M.: DafnyBench: A Benchmark for Formal
    Software Verification. Trans. Mach. Learn. Res. 2025 (2025)
15. Ma, L., Liu, S., Li, Y., Xie, X., Bu, L.: Specgen: Automated generation of formal
    program specifications via large language models. In: ICSE. pp. 16–28. IEEE (2025)
16. Misu, M.R.H., Lopes, C.V., Ma, I., Noble, J.: Towards ai-assisted synthesis of
    verified dafny methods. Proc. ACM Softw. Eng. 1(FSE), 812–835 (2024)
17. de Moura, L., Ullrich, S.: The Lean 4 Theorem Prover and Programming Language.
    In: CADE. pp. 625–635. LNCS, Springer (2021)
18. Mugnier, E., Gonzalez, E.A., Polikarpova, N., Jhala, R., Zhou, Y.: Laurel: Unblock-
    ing Automated Verification with Large Language Models. Proc. ACM Program.
    Lang. 9(OOPSLA1), 1519–1545 (2025)
19. Müller, P., Schwerhoff, M., Summers, A.J.: Viper: A Verification Infrastructure for
    Permission-Based Reasoning. In: Dependable Software Systems Engineering, pp.
    104–125. IOS Press (2017)
20. Paulin-Mohring, C.: Introduction to the Coq Proof-Assistant for Practical Soft-
    ware Verification. In: Tools for Practical Software Verification, LASER. pp. 45–95.
    LNCS, Springer (2011)
21. Pirzada, M.A.A., Reger, G., Bhayat, A., Cordeiro, L.C.: LLM-Generated Invariants
    for Bounded Model Checking Without Loop Unrolling. In: ASE. pp. 1395–1407.
    ACM (2024)
22. Poesia, G., Loughridge, C., Amin, N.: dafny-annotator: Ai-assisted verification of
    dafny programs. CoRR abs/2411.15143 (2024)
23. Silva, Á.F., Mendes, A., Martins, R.: Inferring multiple helper dafny assertions
    with llms. CoRR abs/2511.00125 (2025)
24. Sun, C., Sheng, Y., Padon, O., Barrett, C.W.: Clover: Closed-Loop Verifiable Code
    Generation. In: AI Verification. pp. 134–155. LNCS, Springer (2024)
25. Wu, H., Barrett, C.W., Narodytska, N.: Lemur: Integrating large language models
    in automated program verification. In: ICLR. OpenReview.net (2024)
26. Wu, Y., Jiang, A.Q., Li, W., Rabe, M.N., Staats, C., Jamnik, M., Szegedy, C.:
    Autoformalization with Large Language Models. In: NeurIPS (2022)
27. Xia, Y., Shen, W., Wang, Y., Liu, J.K., Sun, H., Wu, S., Hu, J., Xu, X.: Leetcode-
    dataset: A temporal dataset for robust evaluation and efficient training of code
    llms. CoRR abs/2504.14655 (2025)
28. Yang, C., Li, X., Misu, M.R.H., Yao, J., Cui, W., Gong, Y., Hawblitzel, C., Lahiri,
    S.K., Lorch, J.R., Lu, S., Yang, F., Zhou, Z., Lu, S.: Autoverus: Automated proof
    generation for rust code. Proc. ACM Program. Lang. 9(OOPSLA2), 3454–3482
    (2025)
29. Yang, K., Swope, A.M., Gu, A., Chalamala, R., Song, P., Yu, S., Godil, S., Prenger,
    R.J., Anandkumar, A.: LeanDojo: Theorem Proving with Retrieval-Augmented
    Language Models. In: NeurIPS (2023)
