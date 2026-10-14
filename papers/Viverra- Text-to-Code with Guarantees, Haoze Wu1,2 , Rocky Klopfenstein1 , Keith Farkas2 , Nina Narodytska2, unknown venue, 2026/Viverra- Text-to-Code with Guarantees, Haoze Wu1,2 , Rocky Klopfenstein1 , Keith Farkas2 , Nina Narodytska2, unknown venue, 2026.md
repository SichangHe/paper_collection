                                                       V IVERRA: Text-to-Code with Guarantees


                                                         Haoze Wu1,2 , Rocky Klopfenstein1 , Keith Farkas2 , Nina Narodytska2
                                                                              1
                                                                                Amherst College 2 Broadcom
                                                                          {hwu,rklopfenstein27}@amherst.edu
                                                                     {keith.farkas,nina.narodytska}@broadcom.com
arXiv:2605.14972v1 [cs.SE] 14 May 2026




                                                                                          Abstract
                                                     A fundamental limitation of Text-to-Code is that no guarantee can be obtained
                                                     about the correctness of the generated code. Therefore, to ensure its correctness,
                                                     the generated code still has to be reviewed, tested, and maintained by developers.
                                                     However, parsing through LLM-generated code can be tedious and time-consuming,
                                                     potentially negating the productivity gains promised by AI-coding tools. To address
                                                     this challenge, we present V IVERRA, a system that automatically produces formally
                                                     verified annotations alongside generated code to aid user’s understanding of the
                                                     generated program. Given a natural-language task description, V IVERRA prompts
                                                     an LLM to synthesize a C program together with candidate assertions expressing
                                                     safety and correctness properties. It then verifies those assertions in a compositional
                                                     and best-effort manner via a portfolio of bounded model checkers. Evaluation on
                                                     18 diverse programming tasks suggests that V IVERRA can efficiently generate code
                                                     with verified assertions, and that these assertions improve users’ performance on
                                                     code-comprehension tasks in a user study with more than 400 participants.


                                         1    Introduction
                                         Text-to-Code based on Large Language Models (LLMs) can significantly improve software devel-
                                         opment productivity. However, LLM-generated code is opaque: subtle bugs, incorrect logic, and
                                         violated assumptions can all slip through unnoticed. In practice, developers must manually review
                                         or rewrite LLM-produced programs before they can trust them, an overhead that risks negating the
                                         productivity gains promised by AI coding tools. Since Text-to-Code fundamentally cannot guarantee
                                         that the generated code correctly implements the natural language specification at any level of detail,
                                         human involvement is still unavoidable. We therefore argue that a key bottleneck in Text-to-Code is
                                         that developers lack efficient ways to check the generated code. In this paper, we ask the following
                                         question: How can we help the developer to understand and analyze AI-generated code?
                                         A standard answer to this question is to perform thorough testing. However, generated code can be
                                         large, the logic can be non-trivial, and tests only witness correctness on a finite number of inputs; they
                                         cannot reliably characterize general program behavior across a wide range of execution traces. On
                                         the other hand, full formal verification, e.g., through proof assistants such as Lean or Rocq, has the
                                         potential to provide the user with absolute guarantees about the behavior of the program. However,
                                         requiring a complete formal proof for every generated program is impractical: even with the aid of
                                         LLMs, program verification in proof assistants can still be time-consuming and challenging (First
                                         et al., 2023; Jiang et al., 2022). Therefore, there is room for practical methods between these two
                                         extremes, that is, approaches that provide stronger guarantees than testing without requiring full
                                         formal verification. To explore this gap, we propose V IVERRA, a novel Text-to-Code framework.
                                         The goal of V IVERRA is to provide developers with proven statements about program behavior while
                                         keeping the cost of obtaining that information practical.
                                         The design of V IVERRA makes several important compromises to achieve this goal. First, it puts
                                         forward the idea of partial co-specification: co-generating code together with properties of the code

                                         Preprint.
in the form of assertions. These properties capture requirements from the natural language description
of the program functionality. Usually, they express safety and correctness properties of the code.
These assertions serve simultaneously as partial specifications and as targets for formal verification.
Second, we carefully design a best-effort verification procedure. We propose using bounded program
verification to check these assertions in a best-effort manner: we do not require every assertion to be
fully verified, making our verification incomplete by design. The key insight is that even incomplete
verification is valuable: an assertion confirmed to hold on all executions within a bounded depth is a
formally grounded fact that the developer can rely on, helping them understand the properties of the
code and narrowing what must be reviewed manually.
To test the feasibility of V IVERRA, we perform an evaluation on 18 practical Text-to-C-Code tasks
that goes beyond simple benchmarks seen in canonical datasets such as HumanEval (Chen et al.,
2021) and MBPP (Austin et al., 2021). We found that V IVERRA can efficiently generate complex
programs with multiple verified assertions, and a further user study suggests those verified facts are
meaningful enough to boost program comprehension in practice.
To summarize, our contributions include the following:

       • We introduce V IVERRA, an end-to-end Text-to-Code workflow that synthesizes C pro-
         grams from natural-language descriptions and automatically produces formally verified
         annotations.
       • We propose the idea of partial co-specification: the LLM co-generates both a program and
         partial correctness properties from the same natural-language task description, turning those
         properties into assertions that serve as partial specifications.
       • We design a best-effort compositional verification procedure that uses call-graph structure
         and previously verified assertions as assumptions, allowing bounded model checking to
         produce both unconditional and conditional guarantees.
       • We prove that every verified property is sound within the stated loop-unwind bound, and
         that conditional facts are sound under their recorded dependency assumptions.
       • We evaluate V IVERRA on 18 diverse Text-to-Code benchmarks and show that it can generate
         and verify meaningful annotations efficiently; a user study further shows that these verified
         properties improve code comprehension compared to unannotated generated programs.

2   Preliminaries
We consider the following setting. A developer provides a natural-language task description D. An
LLM produces a program P intended to implement D. Our goal is to automatically produce a set
of verified facts, formally grounded statements about the behavior of P, that help the developer
understand and audit the generated code, without requiring the developer to write any specification.
In this section, we introduce the key concepts of V IVERRA.
Definition 1 (Program/Call graph). A program P consists of global code (headers, macros, type
definitions) and a finite set of functions F(P). The call graph G(P) is a directed graph over F(P)
where an edge (f → g) exists if f calls g, annotated with the logical line of the call site in f .
Definition 2 (Assertion). An assertion is a triple a = ⟨f, l, ϕ⟩ where f ∈ F(P) is a function name,
l ∈ N is a line number in f , a position between consecutive non-assertion statements, and ϕ is a
Boolean predicate over program variables in scope at l. We write A(P) for the set of all assertions in
P. The line numbers are counted over the assertion-free skeleton of f , so l is stable under insertion
or removal of assertions.
We adopt the loop-unwinding semantics standard in bounded model checking (Clarke et al., 2004).
Definition 3 (k-Bounded Execution). A k-bounded execution of a program P is any execution in
which every loop back-edge is traversed at most k times; the model checker asserts false at the
(k+1)-th iteration to detect violations of the bound. We write Execk (P) for the set of all k-bounded
executions of P.
Definition 4 (Bounded Invariant). Given a program P, an assertion a = ⟨f, l, ϕ⟩, and a bound k ∈ N,
we say a is a k-bounded invariant of P, written BInvk (P) ∋ a, if ϕ evaluates to true at line l of f
on every execution in Execk (P).


                                                  2
                Partial co-specification

                                                             Best-effort verification                                                          Developer
                     Property                                                                                                                   review
                   elicitation Π
                                                           Call-graph
                                                            traversal

   NL task              Annotated             Bound                                                           verified only
                                                                                  Compositional   Assertion                        Fact        Code with
description D          program P +         reduction Pk+                           verification   statuses                      translation   verified facts



                     Program
                   synthesis P0                                                                               bounds / conditions




                                                   Figure 1: Overview of V IVERRA.

Bounded invariants are decidable and can be checked with a Bounded Model Checker via Definition 3;
full invariance over all executions is undecidable in general. A k-bounded invariant provides a formal
guarantee for all executions within the stated bound.
Definition 5 (Assumption). Given a program P and a set of assertions S                            =
{⟨f1 , l1 , ϕ1 ⟩ , . . . , ⟨fn , ln , ϕn ⟩}, Asm(P, S) denotes the program obtained by treating each
assertion in S as an assumption, which renders any execution on which ϕi is false infeasible,
pruning it from the model checker’s search space. Formally:
                                       
   Execk (Asm(P, S)) = e ∈ Execk (P) ∀ ⟨fi , li , ϕi ⟩ ∈ S, ϕi holds at line li of fi in e .

An assumption restricts the set of executions considered by the model checker to those consistent
with S: only executions in which all ϕi hold are explored, without triggering assertion failures for
those locations.
Definition 6 (Verification Status). Given a program P, an ordered assertion sequence t =
[a1 , . . . , am ], and a bound k, the verification status of ai is one of:

           • V ERIFIED: ai is a k-bounded invariant of P.
           • C-V ERIFIED(S): ai is a k-bounded invariant of Asm(P, S), where S is a set of assertions.
           • FALSIFIED: the model checker finds a k-bounded counterexample to ai even under S.
           • U NKNOWN: verification times out.

3      Methodology
Figure 1 shows an overview of the V IVERRA workflow. In a nutshell, V IVERRA takes a natural-
language description as input and generates a program annotated with a set of formally verified facts,
each tagged with the conditions and bound under which it was established. These additional facts
make the task of analyzing and validating generated code easier for the developer, as our user study
confirms. Next, we describe the workflow in detail.

3.1      The V IVERRA Pipeline

Algorithm 1 describes the V IVERRA workflow, and Figure 1 visualizes its main steps. The figure also
highlights how two central ideas underlying the workflow, partial co-specification and best-effort
verification, are implemented in the framework. V IVERRA starts by generating properties Π (line 1)
and synthesizing the initial program P0 (line 2) from D. The goal of the property elicitation step
is to generate safety and correctness properties that the program should satisfy based on the user
description. As a result, it produces a set of properties Π = {π1 , . . . , πn } in natural language.
Figure 2 shows an example of such a set for an excerpt from the ‘Bubble Sort’ task: π1 and π2 are
two properties for this task formulated in natural language. These serve as a conceptual checklist
for assertion generation. Next, V IVERRA generates a C program P0 . Here, we instruct the LLM to
perform verification-friendly synthesis, e.g., to avoid recursion, with verifiability as a design constraint
(see Appendix C.2 for the prompt). Given P0 and Π, V IVERRA performs assertion generation (line 3).
It annotates P0 with assertions that are expressed as assert statements in C code at appropriate
locations throughout the program, producing P + . Assertions may appear at function boundaries
(preconditions at entry, postconditions before returns), at loop invariant points, or wherever a property


                                                                        3
Algorithm 1 The V IVERRA Pipeline
Require: Natural-language description D, loop-unwind bound k
Ensure: Program P0 annotated with verified facts
1: Π ← P ROPERTY E LICIT(D)                                                                      ▷ LLM: NL safety/correctness properties
2: P0 ← S YNTHESIZE(D)                                                                            ▷ LLM: verification-friendly C program
3: P + ← A NNOTATE(P0 , Π)                                                                          ▷ LLM: embed assert() statements
4: Pk+ ← B OUND R EDUCE(P + , k)                                           ▷ LLM: tighten loop-bound constants so loops iterate ≤ k times
5: t ← CGT RAVERSAL(Pk+ )                                                                                ▷ order assertions by call graph
6: (IG, F ) ← V ERIFYA LL(Pk+ , t, k)
7: M ← M AP TO P ROPERTIES(Pk+ , Π)                                                                        ▷ LLM: assertion → property
8: return E MBED FACTS(P0 , IG, M )                                                                        ▷ translate to NL facts in code



                                  Property elicitation Π                           Annotated program P +
                                                                                   void bubble_sort(int arr[], int n,
                                  π1 : The global swap counter equals the              int *total_swaps) {
                                  total number of adjacent swaps.                     int i, j, swapped;
                                  π2 : After all passes complete, the array is        int local_total_swaps = 0;
                                  sorted in non-decreasing order: ∀k. 0 ≤
                                                                                      for (i = 0; i < n - 1; i++) {
                                  k ∧ k + 1 < n ⇒ arr[k] ≤ arr[k + 1].
                                                                                         swapped = 0;
                                                                                         for (j = 0; j < n - 1 - i; j++) {
  Task description D                                                                        if (arr[j] > arr[j + 1]) {
  “Write a program that im-       Program synthesis P0                                         int tmp = arr[j];
  plements the Bubble Sort                                                                     arr[j] = arr[j + 1];
                                  void bubble_sort(int arr[], int n,
  algorithm to sort an array of                                                                arr[j + 1] = tmp;
                                      int *total_swaps) {
  integers in ascending order.”                                                                local_total_swaps++;
                                    int i, j, swapped;
                                                                                               swapped = 1;}
                                    int local_total_swaps = 0;
                                                                                         }
                                    for (i = 0; i < n - 1; i++) {                        if (!swapped) break;}
                                            ...                                       *total_swaps = local_total_swaps;
                                    }                                              a1 assert(*total_swaps == local_total_swaps);
                                    *total_swaps = local_total_swaps;              a2 assert(is_sorted_non_dec(arr, n));
                                  }                                                }


Figure 2: Example of partial co-specification for a function in the ‘Bubble Sort’ program. From the
same task description D, V IVERRA co-generates candidate properties Π and an initial program P0 .
The properties are then inserted into the program as assertions, producing P + . The red labels show
how each elicited property is linked to the corresponding generated assertion.

from Π is most naturally expressed. Helper functions returning bool may be introduced for complex
conditions. Figure 2 shows P + and examples of assert statements a1 and a2 that correspond to
properties π1 and π2 , where a2 asserts a helper function.
The next step is to perform best-effort verification of the generated assertions in P + . We perform it
in two phases. First, we perform a preprocessing step, bound reduction, at line 4. The goal is to make
Pk+ loop-bound tight: no loop should reach its (k+1)-th iteration on any input to Pk+ . As noted in
Definition 3, the model checker asserts false at the (k+1)-th iteration of every loop; if any loop can
legitimately run beyond k iterations, this unwinding assertion is violated, causing a spurious failure
unrelated to the program’s actual properties. In practice, the LLM reduces compile-time loop-bound
constants so that every loop iterates at most k times. Next, we perform compositional verification,
which we discuss in detail in the next section.
The final step is to compile facts for the developer, fact generation, and present them to the user; this
step is described in Section 3.3.

3.2     Compositional Verification

V IVERRA has to verify programs with multiple annotations across different functions. Therefore, we
employ a compositional verification procedure that accounts for and leverages these interdependencies.
To retrieve such dependencies, we first perform an analysis of the program and construct a call graph
(line 5). CGT RAVERSAL produces a linear ordering of A(Pk+ ) by performing a depth-first traversal
of G(Pk+ ) from main, with cycle avoidance. For each function f , its assertions are collected in
logical-line order. When f calls g at logical line lc , the traversal of g is inserted into f ’s assertion
list immediately before f ’s assertions at lines ≥ lc . By construction, for every call edge (f → g)
at line lc , all assertions of g precede all assertions of f at lines ≥ lc in t. This ensures that callee
postconditions are available as assumptions when verifying caller assertions that follow the call.
Given t, we perform the main verification loop in line 6, outlined in Algorithm 2.


                                                                    4
Algorithm 2 processes assertions ai one by one in sequence order. The algorithm maintains an
implication graph IG that stores logical dependencies between the ith assertion and a preceding
assertions in the order. We also keep track of falsified assertions in F . For each ai , Algorithm 2
attempts a standalone check (line 3): does ai hold with no additional assumptions? We denote by
Vk (P, ∅, ai ) a call to the automated reasoning tool that runs the bounded model checker on P with ai
as the target assertion and loop-unwind bound k. It returns one of {Verified, Falsified, Unknown} 1 .
If the check succeeds, we obtain a verified assertion with no dependencies. Otherwise, the algorithm
attempts a compositional check (line 8): does ai hold when all preceding assertions S = {aj : j < i}
are promoted to assume() statements? Here, Asm(P, S) denotes the program obtained by treating
each assertion in S as an assumption. If this check succeeds, we obtain a verified assertion under the
assumption that the assertions in S hold. Otherwise, we mark it as failed and add it to F (line 12).
Promoting earlier assertions to assumptions is sound because they represent facts about earlier
program points that, if verified themselves, are guaranteed to hold. Next, we prove properties of
V ERIFYA LL. We denote index(IG) the set of all keys in the dictionary structure IG.
Theorem 1 (Soundness of V ERIFYA LL). Let P be a program, t = [a1 , . . . , am ] an assertion
sequence, k a bound, and (IG, F ) = V ERIFYA LL(P, t, k). For every i ∈ index(IG) with ai =
⟨fi , li , ϕi ⟩:

       1. If IG[i] = ∅, then ϕi holds at line li of fi on every execution in Execk (P).
       2. If IG[i] = S ̸= ∅, then ϕi holds at line li of fi on every execution in Execk (Asm(P, S)).

Proof. See Appendix A.

The theorem establishes that each assertion is sound with respect to assumptions S that it depends on.

3.3   Fact Generation

Since a dependency set of an assertion a may itself contain independently verified and conditionally
verified assertions, we can tighten the set of assertions that a depends on by iteratively back-tracing
its dependencies to “root” assertions. We formalize this via the dependency closure.
Definition 7 (Dependency Closure). Given an implication graph IG output by V ERIFYA LL, the
dependency closure of assertion ai is defined inductively:
                                                  [
                                 Deps(ai ) =            Deps(aj ).
                                                           aj ∈IG[i]

When i ̸∈ index(IG) (i.e., ai is unverified), Deps(ai ) = {ai }; and when IG[i] = ∅ (i.e., ai is
V ERIFIED), Deps(ai ) = ∅.

Because Algorithm 2 records IG explicitly, the dependency closure Deps(ai ) is checkable automati-
cally. We now prove that soundness is preserved under this tightened set of assumptions.
Theorem 2 (Sound assumptions). Under the hypotheses of Theorem 1, for every i ∈ index(IG)
with ai = ⟨fi , li , ϕi ⟩, ϕi holds at line li of fi on every execution in Execk (Asm(P, Deps(ai ))).

Proof. See Appendix A.

After verification and dependency analysis, each V ERIFIED or C-V ERIFIED assertion is translated
by V IVERRA into a natural-language statement and embedded as a comment in P0 , where K is the
bound under which it was established:

        • A V ERIFIED statement is tagged //FACT[k=K ].
        • A C-V ERIFIED statement is tagged //FACT[k=K, cond] and is accompanied by the index
          set Deps(ai ) (Definition 7).
   1 In practice, U NKNOWN indicates that the solver exhausted its time budget without reaching a conclusion; such assertions

are excluded from the output.


                                                             5
Algorithm 2 V ERIFYA LL: Compositional Verification
Require: Program P, assertion sequence t = [a1 , . . . , am ], bound k
Ensure: Implication graph IG, falsified set F
 1: IG ← {}; F ← {}
 2: for i ← 1 to m do        
 3:     r ← Vk P, ∅, ai                                                             ▷ standalone: no assumptions
 4:     if r = Verified then
 5:         IG[i] ← ∅
 6:     else
 7:         S ← {aj : j < i}              
 8:         r ← Vk Asm(P, S), ∅, ai                                         ▷ compositional: assume all preceding
 9:         if r = Verified then
10:              IG[i] ← S
11:          else if r = Falsified then
12:              F ← F ∪ {i}
13: return (IG, F )



By Theorem 2, every presented fact is formally grounded: a developer who accepts the stated
conditions for C-V ERIFIED facts obtains a sound guarantee for all k-bounded executions of the
program. These fact-annotated programs are what developers receive and empirically improve
developers’ comprehension of the program.

4     Implementation
We implemented a prototype of V IVERRA in Python. We now describe the key implementation
choices for V IVERRA’s LLM backend and verification engine.
LLM backend. All prompting stages (property elicitation, synthesis, annotation, bound reduction,
assertion-to-property mapping, and fact translation) call the OpenAI API. Responses are cached by
a hash of the prompt and model so that repeated runs are reproducible and cost-free. Reasoning
effort is set to low for synthesis and annotation to reduce latency, and can be increased for harder
benchmarks.
Portfolio model checker. Vk is implemented as a parallel portfolio of two bounded model checkers:
CBMC (Clarke et al., 2004) (run with and without the Bitwuzla (Niemetz and Preiner, 2023) SMT
back-end) and ESBMC (Cordeiro et al., 2012) (with Bitwuzla). All three solver configurations are
launched concurrently; the portfolio returns as soon as any solver reaches a definitive answer. If all
solvers time out within a per-assertion budget, the status is U NKNOWN. We use a default unwind
bound of k = 5 and a per-solver timeout of 60 s.
Assertion normalization. Before handing P + to the model checker, V IVERRA flattens multi-line
assert(...) statements onto a single line. This ensures that the logical line numbers in Definition 2
correspond exactly to the source positions seen by the parser, and that libclang can unambiguously
identify each assertion’s location.
Call-graph extraction. V IVERRA parses Pk+ with libclang to obtain the call graph and per-function
source extents. Assertions are extracted by regex, stripped from the function body to compute logical
line numbers (Definition 2), and re-inserted during verification as either assert or assume by the
Method.generate_with_assertions routine. Global code is preserved verbatim and prepended
to every verification query.
Compilation checks. Between every LLM-generation step, V IVERRA compiles the output with gcc
and re-prompts on failure, feeding the compiler error back as additional context. This ensures that
both P0 and P + are syntactically valid before any verification is attempted.

5     Experimental Evaluation
In this section, we perform experimental evaluation of V IVERRA on a diverse set of Text-to-Code
tasks. Concretely, we evaluate V IVERRA along two axes:
         • (Feasibility): can V IVERRA generate programs and derive verified annotations for non-trivial
           Text-to-Code tasks?
         • (Utility): do those verified annotations help developers understand the generated code?


                                                                   6
Table 1: Verification results per benchmark. LLM (s) is total wall-clock time for all LLM calls
(synthesis, annotation, bound reduction, mapping, translation); Verify (s) is total verification time.
      Benchmark               #Assert    V ERIFIED   C-V ERIFIED   Unverified     LLM (s)      Verify (s)
      bubblesort                10          10             0           0            36.6            2.9
      condorcet                 25          22             0          3            172.5          253.0
      connected_component       21          21             0          0             95.7          127.5
      shortest_path             25          24             0           1           143.0           32.8
      knapsack                  23          15             4           4           125.3          879.3
      sudoku                    49          43             0          6            164.9         2077.6
      tictactoe                 85          85             0           0           182.0           21.6
      connect4                  59          56             0          3            459.3          981.0
      numberle                  34          32             0           2           345.3            8.6
      gaussian_elimination      17          17             0           0            89.8          139.7
      simplex                   21          21             0           0           234.0          163.2
      log_timestamp_filter      20          18             1           1           223.0            9.3
      sort_timestamp            34          34             0           0           121.3           24.0
      shift_letter              19          19             0           0           104.9            2.4
      base_addition             23           9             0          14            44.5           12.6
      cellular_automata         17          17             0           0           159.3          206.9
      maze                      32          31             0           1            65.4          436.2
      Mean±Std               30.2±18.6   27.9±19.0    0.3±1.0      1.3±3.4      162.8±108.0   316.4±542.7



5.1    Experimental Setup

We evaluate on 18 diverse Text-to-Code tasks, from implementing the Simplex algorithm for deciding
the feasibility of linear systems to parsing and filtering lines in a log file. Each task is specified by a
natural-language description, which can be found in Appendix B; V IVERRA takes the description as
input and automatically generates the corresponding program and verified assertions. We use GPT-5.1
with low reasoning for LLM calls and set the loop-unwind bound to k = 5. The portfolio verification
engine uses a per-assertion wall-clock timeout of 60 s. Experiments were run on a workstation
equipped with AMD Ryzen Threadripper PRO 5945WX processors.


5.2    Performance of V IVERRA on program-annotation co-synthesis

Table 1 shows the per-task breakdown of assertion statuses. Depending on the complexity of the
generated code, V IVERRA generates 10 to 85 assertions. The vast majority of generated assertions
are verified by the model checker without any assumptions, confirming that V IVERRA can produce
programs with assertions that are automatically verifiable. A small fraction cannot be verified in
isolation but hold conditionally on earlier established facts. For most benchmarks the number of
unverified assertions (falsified or timed out) is small, but base_addition is a clear outlier with 14 of
23 assertions falsified. Upon closer examination, these failures are not due to bugs in the program
logic, but due to the over-approximation of certain operators by the verification tool which led to
spurious counter-examples.
LLM synthesis time ranges from 36.6 s to 459.3 s across benchmarks, which is reasonable given that
each run involves multiple sequential LLM invocations (property elicitation, synthesis, annotation,
bound reduction). Verification time varies considerably more, from 2.4 s (shift_letter) to 2077.6 s
(sudoku), driven by the complexity of the properties and programs. For example, sudoku timed out on
assertions like board_is_partial_valid, which requires the model checker to reason about global
row, column, and subgrid uniqueness simultaneously; similarly, knapsack’s costliest assertion checks
that the entire item array is sorted by density after a comparison-based sort. Such global relational
properties are inherently harder for bounded model checking than local invariants. Nonetheless, as
shown in the next section, V IVERRA was able to generate and verify meaningful assertions that help
developers with program understanding.
The current implementation verifies assertions sequentially, so total verification time grows linearly
with the number of assertions. Parallelizing the verification loop—running independent assertion
checks concurrently—is the most direct path to reducing wall-clock time, since each call to Vk is
independent. More aggressive strategies include tightening the loop-unwind bound for assertions
identified as expensive, or limiting the assertion budget per function to focus verification effort on the
most informative properties.


                                                       7
5.3   Can verified annotations aid comprehension?

We conducted a user study to evaluate whether verified annotations improve code comprehension.
Concretely, we manually generated 10 multiple-choice questions, each anchored to a single verified
assertion. Questions were designed to reference the underlying assertion without quoting it directly
(e.g., “When the program prints the vertices of a connected component (line 159), what order are
they in?”). We then manually constructed three distractors per question, leading to a four-choice
multiple-choice format. The raw surveys can be found in the supplementary materials.
Each multiple-choice question was evaluated using Human Intelligence Tasks (HITs) on Mturk. Each
HIT consisted of a single survey containing basic instructions, a C program with lines numbered
for readability, and one multiple choice question. For each question, we consider two cases, one
where the program is not annotated with verified facts, the other where the C program was annotated
with //FACT: comments, which are natural language statements translated from verified assertions.
For this experiment, we only added assertions that are independently verified (without assumptions).
These translations were intended to preserve only the logic described by an assertion. The survey was
set up such that there is no overlap between participants of the two HITs with respect to the same
question. Each HIT was completed by at least 20 workers. All HITs shared the same basic worker
qualifications: a HIT approval rate > 95%, a minimum of 1,000 approved HITs, and the MTurk job
function qualifier Information Technology, targeting tech-adjacent participants. Each worker was
allowed 3 minutes to complete the survey and paid $0.50 per HIT.
Figure 3 summarizes the results. The top-left plot shows the fraction of participants that answer
correctly for each question (accuracy). The accuracy is higher when the programs are annotated with
verified facts on all but two questions. This suggests that the verified annotations denote information
that is not immediately obvious to the participants and that can improve code comprehension.
The remaining three plots examine response timing. Participants overall take less time to answer
a question when annotations are present (top right). Among participants who answered correctly
(bottom left), Group B is faster on 6/10 benchmarks, in particular, Group B participants are on
average faster on the last two questions where the accuracy between Group A and group B is the
same. Interestingly, on the first question (connected-comps[Vertice order]), Group B users spent
significantly longer (96s vs. 82s) while achieving a significantly higher accuracy (100% vs. 40%).
We speculate this is due to the overhead the user spent on reading the annotations. Overall, our
experiment suggests that V IVERRA can improve practical code comprehension both in terms of
accuracy in answering questions about the program and the response speed.

6     Related Work
LLM-based code synthesis. LLMs have demonstrated strong code generation capability across
benchmarks spanning algorithmic problems (Chen et al., 2021; Austin et al., 2021; Li et al., 2022)
and real-world repositories (Jimenez et al., 2024). These systems provide no correctness guarantees;
developers must audit the output themselves. V IVERRA is orthogonal to any synthesis back-end: it
augments generated code with formally verified annotations rather than improving generation quality.

Verified code generation. A growing line of work pursues code generation with formal cor-
rectness guarantees. Misu et al. (2024) evaluate LLMs on synthesizing Dafny methods with full
contracts; Chen et al. (2024) synthesize Verus proof annotations for Rust via self-evolving fine-tuning;
Clover (Sun et al., 2024) iteratively verifies LLM-generated Dafny in a closed loop; Baldur (First
et al., 2023) generates and repairs whole Isabelle proofs with LLMs; Bursuc et al. (2025) introduce a
large benchmark spanning Dafny, Verus, and Lean. All these approaches require verification-aware
languages or complete formal proofs. V IVERRA instead targets C with push-button bounded model
checking, trading proof completeness for practical accessibility.

Specification generation. Daikon (Ernst et al., 2007) discovers likely invariants from concrete exe-
cutions, but these are heuristically inferred and may not hold on unobserved inputs. Lemur (Wu et al.,
2024) integrates LLMs with automated verifiers to discharge invariants, but targets full verification
of existing programs rather than co-synthesis. Recent work generates formal contracts (Richter and
Wehrheim, 2025) or Hoare-style annotations (Bouras et al., 2025) alongside code without formally
verifying them. V IVERRA conducts best-effort formal verification for each generated specification.


                                                   8
                             Group A (unannotated)         Group B (annotated)




Figure 3: Comparison of correctness and user-timing between treatment and control HITs. The plots
visualize overall correctness (top-left) and total completion time (top-right), with further breakdowns
of timing for correct (bottom-left) and incorrect (bottom-right) responses across all benchmarks.
7   Conclusion
We presented V IVERRA, an end-to-end pipeline that augments LLM-generated C programs with
formally verified annotations to aid developer comprehension. Starting from a natural-language
description, V IVERRA co-generates a program and candidate assertions, verifies them compositionally
using a call-graph-aware procedure backed by a portfolio of bounded model checkers, and surfaces
only the verified facts to the developer as natural-language comments. On 18 diverse Text-to-
Code benchmarks, V IVERRA was able to successfully generate and verify a significant number of
assertions. A user study with crowdworkers confirms that programs annotated with verified facts
improve both answer accuracy and response speed compared to unannotated programs, demonstrating
that V IVERRA produces verified annotations that are meaningful in practice.

Limitations and future work. A fundamental limitation of V IVERRA is that it only provides
guarantees up to a certain depth. This is a deliberate trade-off that keeps verification feasible for
complex programs. In the future, it might be interesting to consider invoking AI-driven proof
assistants to fully verify properties in a best-effort manner. While the scalability of bounded model
checkers has improved significantly in the past two decades, V IVERRA can still be bottlenecked
by the underlying verifiers and can only work with programs supported by the verifiers. Extending
the approach to richer languages such as Python or Rust, and to heap properties and quantified
invariants, are natural next steps. Finally, the quality of verified annotations depends on the LLM
generating meaningful assertions. In the future, it would be interesting to consider alternative property
elicitation strategies or design metrics to evaluate the quality of the generated assertions. Due to
budget constraints, the human study was conducted with crowdworkers and at a relatively small scale.
While the patterns we observed are clear and consistent, expanding the user study with professional
developers in an offline setting on a larger set of questions would further establish the effectiveness
of V IVERRA.


                                                     9
References
Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan,
  Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, et al. 2021. Program synthesis with large language
  models. arXiv preprint arXiv:2108.07732 (2021).
Dimitrios Stamatios Bouras, Yihan Dai, Tairan Wang, Yingfei Xiong, and Sergey Mechtaev. 2025.
  HoarePrompt: Structural Reasoning About Program Correctness in Natural Language. arXiv
  preprint arXiv:2503.19599 (2025).
Sergiu Bursuc, Theodore Ehrenborg, Shaowei Lin, Lacramioara Astefanoaei, Ionel Emilian Chiosa,
  Jure Kukovec, Alok Singh, Oliver Butterley, Adem Bizid, Quinn Dougherty, et al. 2025. A
  benchmark for vericoding: formally verified program synthesis. arXiv preprint arXiv:2509.22908
  (2025).
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared
 Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. 2021. Evaluating
 large language models trained on code. arXiv preprint arXiv:2107.03374 (2021).
Tianyu Chen, Shuai Lu, Shan Lu, Yeyun Gong, Chenyuan Yang, Xuheng Li, Md Rakib Hossain
  Misu, Hao Yu, Nan Duan, Peng Cheng, et al. 2024. Automated proof generation for rust code via
  self-evolution. arXiv preprint arXiv:2410.15756 (2024).
Edmund Clarke, Daniel Kroening, and Flavio Lerda. 2004. A Tool for Checking ANSI-C Programs.
  In International Conference on Tools and Algorithms for the Construction and Analysis of Systems
  (TACAS). Springer, 168–176.
Lucas Cordeiro, Bernd Fischer, and João Marques-Silva. 2012. SMT-based Bounded Model Checking
  for Embedded ANSI-C Software. IEEE Transactions on Software Engineering 38, 4 (2012), 957–
  974.
Michael D Ernst, Jeff H Perkins, Philip J Guo, Stephen McCamant, Carlos Pacheco, Matthew S
 Tschantz, and Chen Xiao. 2007. The Daikon System for Dynamic Detection of Likely Invariants.
 Science of Computer Programming 69, 1–3 (2007), 35–45.
Emily First, Markus N Rabe, Talia Ringer, and Yuriy Brun. 2023. Baldur: Whole-Proof Generation
  and Repair with Large Language Models. In Proceedings of the ACM on Software Engineering
 (ESEC/FSE). ACM.
Albert Q Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée
  Lacroix, Yuhuai Wu, and Guillaume Lample. 2022. Draft, sketch, and prove: Guiding formal
  theorem provers with informal proofs. arXiv preprint arXiv:2210.12283 (2022).
Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik
  Narasimhan. 2024. SWE-bench: Can Language Models Resolve Real-World GitHub Issues?. In
  International Conference on Learning Representations (ICLR).
Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom
  Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, et al. 2022. Competition-level code
  generation with alphacode. Science 378, 6624 (2022), 1092–1097.
Md Rakib Hossain Misu, Cristina V Lopes, Iris Ma, and James Noble. 2024. Towards ai-assisted
 synthesis of verified dafny methods. Proceedings of the ACM on Software Engineering 1, FSE
 (2024), 812–835.
Aina Niemetz and Mathias Preiner. 2023. Bitwuzla. In International Conference on Computer Aided
  Verification. Springer, 3–17.
Cedric Richter and Heike Wehrheim. 2025. Beyond Postconditions: Can Large Language Models
  infer Formal Contracts for Automatic Software Verification? arXiv preprint arXiv:2510.12702
  (2025).
Chuyue Sun, Ying Sheng, Oded Padon, and Clark Barrett. 2024. Clover: Closed-Loop Verifiable
  Code Generation. In International Workshop on AI Verification (SAIV). Springer.


                                                 10
Haoze Wu, Clark Barrett, and Nina Narodytska. 2024. Lemur: Integrating Large Language Mod-
  els in Automated Program Verification. In The Twelfth International Conference on Learning
  Representations (ICLR). https://openreview.net/forum?id=Q3YaCghZNt




                                            11
A    Proofs
Theorem 1 (Soundness of V ERIFYA LL). Let P be a program, t = [a1 , . . . , am ] an assertion
sequence, k a bound, and (IG, F ) = V ERIFYA LL(P, t, k). For every i ∈ index(IG) with ai =
⟨fi , li , ϕi ⟩:

      1. If IG[i] = ∅, then ϕi holds at line li of fi on every execution in Execk (P).
      2. If IG[i] = S ̸= ∅, then ϕi holds at line li of fi on every execution in Execk (Asm(P, S)).

Proof. Both cases follow directly from the soundness of the underlying bounded model checker
(Definitions 3–5): Vk returns Verified only when it finds no counterexample within bound k, meaning
the assertion holds on all k-bounded executions of the submitted program (P in case 1; Asm(P, S)
in case 2).

Theorem 2 (Sound assumptions). Under the hypotheses of Theorem 1, for every i ∈ index(IG)
with ai = ⟨fi , li , ϕi ⟩, ϕi holds at line li of fi on every execution in Execk (Asm(P, Deps(ai ))).

Proof. By structural induction on the definition of Deps(ai ) (Definition 7). The induction is well-
founded because Algorithm 2 ensures IG[i] ⊆ {aj : j < i}, so the dependency graph is acyclic.
Base case: IG[i] = ∅. Then Deps(ai ) = ∅, and Theorem 1 (1) gives that ϕi holds on every execution
in Execk (P) = Execk (Asm(P, ∅)) = Execk (Asm(P, Deps(ai ))).
                                              S
Inductive step: IG[i] = S ̸= ∅, so Deps(ai ) = aj ∈S Deps(aj ) by Definition 7. By Theorem 1 (2),
ϕi holds on every execution in Execk (Asm(P, S)). It therefore suffices to show
                        Execk (Asm(P, Deps(ai ))) ⊆ Execk (Asm(P, S)).
Let e ∈ Execk (Asm(P, Deps(ai ))) and aj ∈ S. We show ϕj holds on e:

       • If j ∈
              / index(IG), then Deps(aj ) = {aj }, so aj ∈ Deps(ai ), and ϕj is assumed in
         Asm(P, Deps(ai )); hence ϕj holds on e.
       • If IG[j] = ∅, then Theorem 1 (1) gives ϕj on all of Execk (P) ∋ e.
       • If IG[j] ̸= ∅, the inductive hypothesis gives ϕj on every execution in
         Execk (Asm(P, Deps(aj ))).    Since Deps(aj ) ⊆ Deps(ai ), we have e ∈
         Execk (Asm(P, Deps(ai ))) ⊆ Execk (Asm(P, Deps(aj ))), so ϕj holds on e.

Since ϕj holds on e for every aj ∈ S, the execution e satisfies all assumptions of Asm(P, S), i.e.,
e ∈ Execk (Asm(P, S)). Therefore ϕi holds on every execution in Execk (Asm(P, Deps(ai ))).

B    Benchmark Descriptions
The following 18 benchmarks are used in the evaluation (§5). Each entry gives the full natural-
language task description used as input to V IVERRA. The descriptions are the verbatim prompts
passed to the LLM; no other specification is provided to the system.

bubblesort. Implement the Bubble Sort algorithm to sort an array of integers in ascending order.
The program reads an integer n (1 ≤ n ≤ 100) followed by n integers from stdin. It applies the
standard Bubble Sort—repeatedly comparing adjacent elements and swapping if out of order—then
prints “Sorted Array:” followed by the sorted elements and the total number of swaps performed.

connected_component. Read an adjacency matrix of an undirected graph and identify all connected
components. Input: an integer V (1 ≤ V ≤ 100) followed by a V × V binary adjacency matrix.
The matrix must be symmetric; if A[i][j] ̸= A[j][i], print “Invalid adjacency matrix” and
terminate. For each connected component, print the vertex indices (0-indexed) in ascending order,
one component per line, in discovery order.


                                                 12
shortest_path. Find the shortest path between two vertices in an unweighted graph using BFS.
Input: an integer V (2 ≤ V ≤ 100), a V × V adjacency matrix, and source/destination indices start
and end. Validate that start and end are in [0, V −1]. Output “Path: u -> ...-> v” or “No
path found”.

knapsack. Implement the Greedy algorithm for the Fractional Knapsack problem. Input: the
number of items n and capacity W (double), followed by n pairs of value and weight (doubles). Sort
items by value-to-weight ratio (descending); take items or fractions thereof until the knapsack is full.
Print the total value to two decimal places and a breakdown of items used.

sudoku. Implement a playable 4 × 4 Sudoku game using digits 1–4 with a hardcoded partially filled
initial board. On each turn, display the board, prompt for row, column, and value (each in 1–4), and
reject moves that violate Sudoku rules (out-of-range, pre-filled cell, or duplicate in row/column/2 × 2
subgrid). The game ends when the board is fully and correctly filled.

tictactoe. Implement a two-player Tic-Tac-Toe game on a 3 × 3 grid (Player 1: X, Player 2: O).
Alternately prompt each player for a row/column pair (1–3), reject out-of-range or occupied moves,
check for three-in-a-row (horizontal, vertical, diagonal) after each valid move, and announce the
winner or a draw. The game loop runs for at most MAX_TURN iterations.

connect4. Implement a two-player Connect Four game on a 6 × 7 grid (X vs. O, X first). On each
turn, display the board, prompt for a column (1–7), and reject invalid or full columns. Apply gravity
(piece falls to lowest available row), then check for four consecutive pieces horizontally, vertically, or
diagonally. Announce the winner or a draw if the board is full; the loop runs for at most MAX_TURN
turns.

numberle. Implement a “Numberle” guessing game. The target is a hardcoded 6-character mathe-
matical equation (e.g., 4*2=08). The player has 6 attempts; each guess must be 6 characters, contain
exactly one =, and be mathematically true. After each valid guess, print a 6-character feedback string:
G (correct position), Y (wrong position), or X (not present). End with a victory message or reveal the
target after 6 failures.

condorcet. Determine the Condorcet winner of an election. Input: n candidate names (n ≤ 10),
then v voter ballots (v ≤ 100), each ballot a permutation of candidate indices from most to least
preferred. Build a pairwise win matrix; a candidate is the Condorcet winner if they beat every other
candidate head-to-head. Print “Condorcet Winner: [Name]” or “No Condorcet winner”.

gaussian_elimination. Solve an n × n system of linear equations using Gaussian elimination with
partial pivoting. Input: integer n, then the n × (n+1) augmented matrix (doubles). Before each
elimination step, swap the current row with the row having the largest absolute pivot value. If the
pivot falls below 10−9 , print “No unique solution”. Otherwise perform back-substitution and
print x1 , . . . , xn to 4 decimal places.

simplex. Check satisfiability of Ax = b with x ≥ 0 using the Simplex method. Input: integers m
and n (m, n ≤ 10), then the m × (n+1) augmented matrix. Use Bland’s rule (lowest index) for pivot
selection to prevent cycling. If a row has all non-positive coefficients and a positive b value, print
“UNSATISFIABLE”; otherwise print “SATISFIABLE” and the variable values.

log_timestamp_filter. Read a log file from stdin and print all lines whose timestamp year is strictly
before 2024. Each log line begins with a timestamp in YYYY-MM-DD HH:MM:SS format; lines shorter
than 19 characters or longer than 248 characters are skipped. Parse the year from the first four
characters; print matching lines verbatim.

sort_timestamp. Read N ISO 8601 timestamps with UTC offsets in the format
YYYY-MM-DDTHH:MM:SS[+/-]HH:MM (1 ≤ N ≤ 100), normalize each to UTC (handling
date rollovers), sort chronologically, and print the original strings in sorted order. Timestamps
violating the format or containing invalid values (e.g., month 13) are skipped with “Invalid
Timestamp”.


                                                   13
shift_letter. Read a single line of text from stdin (up to 1024 characters) and print the result of
shifting every alphabetic character one step forward in the alphabet, wrapping z → a and Z → A.
Non-alphabetic characters are unchanged. If the input exceeds 1024 characters, print “Input too
long” and exit with a nonzero code.

base_addition. Perform addition on two positive integers represented as strings in base n (2 ≤
n ≤ 10). Input: three space-separated tokens—the base n and two digit strings (up to 256 characters
each). Validate the base and digits; perform column-by-column addition with carry; print the result in
base n. Invalid base or digit triggers an error message and termination.

cellular_automata. Simulate Conway’s Game of Life on a 2D toroidal grid (max 50 × 50). Read
grid dimensions R and C and the initial state (. = dead, # = alive) from stdin. Repeatedly compute
the next generation using toroidal boundary conditions (neighbors wrap via modulo), display the grid
with ANSI escape codes, and sleep 100 ms between iterations.

maze. Find the shortest path from S to E in a maze (max 50 × 50) using BFS. Input: integers R
and C, followed by R lines of C characters (# = wall, . = open, S = start, E = exit). Movement is
restricted to four cardinal directions. If a path exists, print its length and display the maze with path
cells replaced by *; otherwise print “No path found”.

C     LLM Prompts
This appendix contains the four main prompts used by V IVERRA. Italicized placeholders ({descrip-
tion}, {program}, {properties}) are filled at runtime with the corresponding artifact.

C.1    Property Elicitation

Used in Stage 1 (Section 3) to enumerate natural-language safety and correctness properties from the
task description.
    You are an expert C programmer. You need to generate a C program
    based on the following natural language description:

      {description}

    List safety/correctness properties of the program that performs
    this task in succinct natural language. The properties should be
    expressible as assertions in the code.

    Your answer should just be:
    1. ...
    2. ...


C.2    Verification-Friendly Program Synthesis

Used in Stage 2 to generate the C program P0 . The prompt enforces the structural constraints required
for bounded verification.
    You are an expert C programmer and verification-aware developer.

    Task: Generate a complete, working C program that implements the
    following specification:

    SPEC:
    {description}

    Constraints (must follow all):
    1) Avoid using any third-party/external libraries.
    2) Keep the program verification-friendly:
       - No recursion.


                                                   14
     - No dynamic allocation (malloc/free).
     - No floating point.
     - No pointer arithmetic beyond array indexing.
     - Avoid undefined behavior (signed overflow, out-of-bounds,
       shifting by >= width, uninitialized reads).
     - Use fixed maximum sizes for arrays/buffers; validate lengths.
     - For strings, use strnlen() instead of strlen().
  3) Deterministic control flow for bounded verification:
     - Every loop must have clear static bounds (constants or
       validated input capped at a constant).
     - If a bound is configurable, declare it as a macro at the top
       (e.g., #define MAX_N 100).
  4) Decomposable structure:
     - Provide small functions for each subtask (parsing, validation,
       core logic, output formatting).
  5) I/O:
     - Read from stdin and write to stdout.
     - On invalid input, print an error and exit with nonzero code.
  6) Output:
     - Return ONLY the full program as a single C file, wrapped in
       triple-backtick ‘‘‘c formatting.
     - Include a brief comment at the top stating assumptions and bounds.




C.3   Assertion Generation

Used in Stage 3 to annotate P0 with assert() statements expressing the properties Π.
  You are an expert C programmer.

  You are given:
    Description: {description}
    A C program that implements the task: {program}
    Safety and correctness properties: {properties}

  Annotate the C program with assertions that express these properties
  as function contracts.

  Rules:
  - Treat each C function (including static functions and main) as a
    method.
  - Add preconditions as assert(...) at the very start of each function.
  - Add postconditions as assert(...) immediately before each return.
    For void functions, place postconditions before the closing brace.
  - Use only standard C assertions: assert(condition);
  - Include <assert.h>.
  - Do not add, remove, or modify existing code except for inserting
    assertions.
  - Helper functions (returning bool, called within assert, containing
    no assert themselves) are allowed.
  - Assertions may reference function parameters, return values (via
    existing variables), and globals in scope.

  Applicability:
  - Add an assertion only if it meaningfully applies to the function
    and can be soundly checked at the function boundary.
  - Do not add trivial assertions (assert(true), assert(1), x == x).
  - Only add assertions that enforce one of the listed properties.

  Output:
  - Output only the annotated C program in triple-backtick C formatting.
  - Do not include any explanation outside the code block.



                                              15
C.4   Verified Fact Translation

Used in Stage 5 to translate verified assert() statements into natural-language //FACT: comments
for the developer.
  You are an expert C programmer converting assertions in a C program
  into easily understandable natural-language facts.

  Goal: make assertions easier to understand for non-experts.
  Facts should represent the technical content of the assertion but
  be written in simple, accessible language.
  Do not give MORE information than the assertion. Do not interpret
  it---just translate it into simple natural language.

  Format: "//FACT: At this point in the program, ..."

  Replace each assertion statement with a //FACT: comment.
  Keep all other code exactly the same.
  Do not add code fences.

  C Program:
  {program}




                                              16
