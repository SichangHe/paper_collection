                                         Neuro-Symbolic Generation and Validation of Memory-Aware Formal Function
                                                                       Specifications


                                                       Liao Zhang 1 Tong Chen 2 Xiwei Wu 1 Qi Liu 2 Xiyu Zhai 3 Xinqi Wang 3 Qinxiang Cao 4


                                                                     Abstract                                   1   /*@ Extern Coq (rev: list Z -> list Z) */
                                                                                                                2
                                                 Formal verification of memory-manipulating pro-                3   struct list *reverse(struct list *p)
arXiv:2603.13414v1 [cs.SE] 12 Mar 2026




                                                 grams critically depends on precise function spec-             4   /*@ With (l: list Z)
                                                                                                                5       Require sll(p, l)
                                                 ifications that capture memory states written by               6       Ensure sll(__return, rev(l)) */
                                                 experts. This requirement has become a major bot-              7   {
                                                                                                                8       struct list * w = (void *) 0, * v = p;
                                                 tleneck as large language models (LLMs) increas-               9       /*@ Inv Assert
                                                 ingly generate low-level systems code whose cor-              10       exists p_v l1 l2, l == app(rev(l1), l2) &&
                                                                                                               11       sll(w, l1) * sll(v, l2) * data_at(&p, p_v) */
                                                 rectness cannot be assumed. To enable scalable                12       while (v) {
                                                 formal verification, we focus exclusively on func-            13         struct list * t = v -> next;
                                                                                                               14         v -> next = w;
                                                 tion specification generation, deliberately avoid-            15         w = v;
                                                 ing the synthesis of complex loop invariants that             16         v = t;
                                                                                                               17       }
                                                 are central to traditional verification pipelines. We         18       return w;
                                                 propose a neuro-symbolic framework for auto-                  19   }
                                                 matically generating memory-aware formal func-
                                                 tion specifications for C programs from natural                    Figure 1. QCP formal verification for singly-linked list re-
                                                 language problem descriptions and function sig-                    versal with separation logic. The specification includes pre-
                                                 natures. The pipeline first produces candidate                     condition Require sll(p, l) and postcondition Ensure
                                                                                                                    sll( return, rev(l)). The loop invariant maintains that
                                                 specifications via in-context learning, and then                   the concatenation of reversed prefix and remaining suffix equals
                                                 iteratively refines them using compiler diagnos-                   the original list. The separation operator (∗) ensures disjoint heap
                                                 tics from symbolic provers and the verification                    regions for memory safety.
                                                 toolchain. In particular, we validate candidate
                                                 specifications by constructing a proof for the nega-
                                                 tion of the specification with concrete examples,                  1. Introduction
                                                 enabling machine-checked rejection of plausible-
                                                 but-incorrect specifications. To support system-                   The advent of large language models (LLMs) has funda-
                                                 atic evaluation, we introduce LeetCode-C-Spec,                     mentally transformed software development, enabling auto-
                                                 a new benchmark of 200 C programming prob-                         mated code generation at unprecedented scale. Systems like
                                                 lems for generating memory-aware formal func-                      Codex , GPT-4 , Code Llama , and StarCoder can synthesize
                                                 tion specifications. Experiments show that itera-                  non-trivial programs from natural language, and are already
                                                 tive refinement substantially improves syntactic                   integrated into widely-used development tools including
                                                 validity, while symbolic prover-based refutation                   GitHub Copilot , Cursor , and Claude Code . Due to the
                                                 significantly enhances correctness assessment by                   probabilistic nature of neural code generation, modern soft-
                                                 filtering false positives that LLM-only judges fre-                ware pipelines can now produce code faster than software
                                                 quently accept. Our results demonstrate that com-                  engineers can reliably trust it.
                                                 bining neural generation with symbolic feedback                    This gap is especially acute for systems code: LLM-
                                                 provides an effective approach to formal specifica-                generated programs may look correct but still contain sub-
                                                 tion synthesis for memory-safe systems software.                   tle errors, including memory safety violations and brittle
                                             1                                                                      edge-case logic . For programs used in security- and safety-
                                             School of Computer Science, Shanghai Jiao Tong University
                                         2
                                          Shanghai Innovation Institute 3 School of Computer Science and            critical settings, a single specification mismatch can man-
                                         Engineering, University of Washington 4 School of Artificial Intel-        ifest as exploitable vulnerabilities. Hence, we need mech-
                                         ligence, Shanghai Jiao Tong University. Correspondence to: Liao            anisms that provide machine-checkable guarantees rather
                                         Zhang <zhangliao714@gmail.com>.                                            than probabilistic confidence.
                                         Preprint. March 17, 2026.                                                  Formal verification is a promising path to provide guaran-

                                                                                                                1
                                    Submission and Formatting Instructions for ICML 2026

tees for program correctness, but it hinges on a missing              describe input-output relationships at the function boundary,
ingredient: formal specifications. A specification precisely          whereas loop invariants must hold inductively across all
states what a program should do, typically as function speci-         iterations and typically require deeper semantic reasoning.
fications (preconditions and postconditions ) together with           This distinction makes automated loop invariant synthesis
loop invariants for programs with loops or recursion . For            significantly harder than function specification generation,
memory-manipulating C code, specifications must also cap-             motivating our focus on function-level specifications.
ture memory safety, often using separation logic .
                                                                      In contrast to previous work, we focus solely on automati-
In practice, writing these formal specifications is a major           cally generating memory-aware function specifications for
bottleneck that prevents verification from keeping pace with          C programs, deliberately leaving loop invariant generation
the rapid adoption of LLM-generated code. Traditional                 out of scope. This design choice enables (1) validation
specification writing requires deep expertise in both the             through test case execution without full mechanized proofs,
problem domain and formal logic systems. This creates                 (2) layered verification where validated specifications serve
a significant barrier: even experienced programmers may               as foundations for deriving loop invariants, and (3) reinforce-
struggle to articulate precise memory-safety requirements in          ment learning based improvement via test-based reward
separation logic, while formal verification experts may lack          signals.
domain knowledge about the intended program behavior.
                                                                      We target C programs and the QCP verification toolchain,
This expertise gap becomes especially acute when dealing
                                                                      which supports separation-logic specifications and exports
with LLM-generated code, where the volume of code pro-
                                                                      complex proof obligations to Coq. We use LeetCode prob-
duction vastly exceeds the capacity for manual specification
                                                                      lems as they provide standardized data structures, input-
writing. To illustrate these concepts, consider verifying a
                                                                      output formats, and explicit test cases, with substantially
function that reverses a singly-linked list (see Figure 1).
                                                                      higher algorithmic complexity than existing C verification
The precondition must state that the input pointer points
                                                                      benchmarks.
to a valid linked list: in the example, this is expressed as
Require sll(p, l), where sll(p, l) asserts that                       Our Contributions.
pointer p points to a singly-linked list with elements l. The
postcondition must guarantee that the output forms a re-
versed list: here, Ensure sll( return, rev(l))                           • We propose an agentic workflow for generating
ensures the return value is a valid list containing the re-                memory-aware C function specifications, combining
versed sequence. The loop invariant, beginning with Inv                    iterative refinement guided by compiler feedback to en-
Assert, must express that the partially reversed prefix l1                 sure syntactic correctness with counterexample-guided
and remaining suffix l2 together reconstruct the original                  refutation via automated theorem proving for correct-
list l. Finally, memory safety is enforced through the sep-                ness assessment.
aration logic predicate sll, which ensures that each list
node occupies a distinct, non-overlapping memory region.
                                                                         • We construct LeetCode-C-Spec-200, a benchmark of
Since writing formal specifications is a challenging task,                 200 LeetCode problems for formal C specification gen-
it is natural to leverage large language models (LLMs) to                  eration, featuring more complex algorithms than prior
assist with specification generation. Recent work has begun                C verification benchmarks.
exploring LLM-based approaches to formal verification and
specification synthesis. However, these approaches face a
fundamental challenge: the synthesis of loop invariants is               • We empirically demonstrate that the proposed agentic
a well-studied bottleneck in formal verification, and is in                workflow significantly improves the syntactic valid-
general undecidable or highly complex to automate.                         ity of LLM-generated function specifications. Fur-
Our goal is to make memory-aware specification writing                     thermore, our neuro-symbolic validation substantially
for C programs scalable. Given a natural language problem                  enhances correctness assessment, with Coq-based refu-
description and a function signature, we aim to automati-                  tation effectively filtering false positives that are some-
cally generate a separation-logic function specification that              times accepted by LLM-only judges.
is not only syntactically valid, but also robust under adver-
sarial validation. Our key insight is that while proving the          2. Preliminaries
correctness of a candidate specification is difficult, refuting
an incorrect one is often feasible by constructing concrete           In this section, we provide background on separation logic
counterexamples via test execution combined with auto-                and annotation-based program verification, which form the
mated theorem proving. Moreover, function specifications              foundation of our approach to generating memory-aware
                                                                      formal specifications.

                                                                  2
                                   Submission and Formatting Instructions for ICML 2026

2.1. Separation Logic                                               updated tree.” These predicates are manually selected from
                                                                    QCP’s standard library based on their relevance to LeetCode
Separation logic is a formal system for reasoning about
                                                                    problems, with a focus on commonly used data structures
programs that manipulate pointers and dynamic memory.
                                                                    such as arrays, linked lists, and binary trees. We do not
Its key innovation is the separating conjunction (∗), which
                                                                    describe all predicates in QCP’s standard library, as many
asserts that P ∗ Q holds when memory can be split into
                                                                    are irrelevant to formal function specification generation
two non-overlapping regions satisfying P and Q. Crucially,
                                                                    (e.g., auxiliary predicates such as increasing aux).
store(p, v) ∗ store(q, u) implies p ̸= q, enabling local
reasoning without aliasing concerns.                                Second, we include few-shot examples demonstrating cor-
                                                                    rect specification patterns for common data structures (ar-
The singly linked list predicate sll(p, l) relates pointer p
                                                                    rays, linked lists, trees) and operations. These examples
to logical list l:
                                                                    are drawn from three sources: (1) QCP’s standard test suite,
  sll(p, l) := ((l = nil ∧ p = null) ∧ emp) ∨                       which includes fundamental operations such as list rever-
                                                                    sal and binary search tree insertion; (2) several synthetic
   (∃v, l′ , p′ . (l = v :: l′ ) ∧ store(addr(p.data), v)∗
                                                                    problems inspired by algorithmic patterns common in com-
              store(addr(p.next), p′ ) ∗ sll(p′ , l′ )).            petitive programming but not directly from LeetCode; and
The base case handles empty lists, while the recursive case         (3) one representative LeetCode problem that is excluded
uses ∗ to enforce disjoint memory for each node.                    from our evaluation benchmark to avoid data leakage. The
                                                                    complete prompt template is provided in Appendix.
2.2. Annotation-Based Program Verification                          Third, we incorporate common error patterns that sum-
Annotation-based verification augments source code with             marize frequent syntactic mistakes made by LLMs when
formal specifications as annotations. A verifier generates          generating separation logic annotations. These error pat-
verification conditions (VCs)—logical formulas whose va-            terns—derived from empirical analysis of failed generation
lidity implies correctness—which can be discharged by               attempts—include issues such as incorrect predicate instanti-
SMT solvers or interactive theorem provers like Coq.                ation, malformed separation conjunctions, type mismatches
                                                                    in Coq predicates, and improper use of quantifiers. By
We use QCP , a state-of-the-art C verifier supporting separa-       providing predicate documentation, positive examples, and
tion logic predicates and exporting complex VCs to Coq for          negative patterns, we significantly reduce the rate of trivial
manual or semi-automated proving.                                   syntactic errors in initial generations.
QCP predicates are defined in Coq. Predicates not in QCP’s          Phase 2: Iterative Refinement with Symbolic Feedback.
standard library must be imported via Extern Coq decla-             When the generated specification fails to compile or is found
rations (e.g., rev in Figure 1).                                    to be semantically incorrect, we apply an iterative refine-
                                                                    ment loop. This loop is guided by tool feedback from both
3. Specification Generation                                         Coq and QCP (addressing syntax and type errors) as well
                                                                    as formal refutation (addressing semantic errors). For user-
Figure 2 presents the overall architecture of our LLM-based         defined Coq predicates, we leverage Coq compiler diagnos-
formal specification generation and validation system. The          tics to localize syntax errors, type mismatches, and unre-
system takes as input a natural language problem descrip-           solved identifiers; we pair these diagnostics with curated
tion and a C function signature, and produces formal spec-          repair examples in the prompt to steer the model toward
ifications and additionally necessary Coq predicates. The           minimal fixes. For QCP annotations, we collect diagnos-
pipeline consists of two main phases: initial specification         tics from the QCP checker and categorize failures into two
generation and iterative refinement guided by compiler feed-        primary cases. (1) Annotation syntax errors: We utilize a
back and counterexample-guided refutation.                          taxonomy of common QCP mistakes and corresponding re-
Phase 1: Initial Specification Generation. The generation           pair patterns to guide the model. Specifically, we target two
phase employs prompt engineering with carefully curated             frequent error classes: (a) language confusion between QCP
examples to guide the LLM in producing syntactically and            and Coq syntax (e.g., using = instead of QCP’s ==); and
semantically correct QCP specifications.                            (b) QCP-specific annotation mistakes, such as malformed
                                                                    Require/Ensure clauses or incorrect predicate instan-
Our prompts incorporate three key components. First,                tiation. The full error taxonomy and repair patterns are
we provide natural-language descriptions of QCP’s pre-              detailed in Appendix. (2) Predicate import errors: To re-
defined predicates, including their types, parameters, and          solve these, we first strip existing import annotations from
intended usage contexts. For example, we describe                   the C file, then employ a dedicated prompt to regenerate the
tree insert(v: Z, t: tree): tree as “in-                            required Extern Coq declarations from the synthesized
serts a value v into a binary search tree t and returns the

                                                                3
                                     Submission and Formatting Instructions for ICML 2026

Coq definitions. These are then reinserted into the original             based test case generation with automated theorem proving
C file alongside the QCP specification. Errors outside these             in Coq, as illustrated in Figure 4. The workflow proceeds in
categories are currently treated as unrecoverable and lead to            two stages:
generation failure.
                                                                         Negation and Test Case Generation. Given a spec-
4. Specification Validation                                              ification with postcondition post, we construct the
                                                                         negated verification goal ¬post and generate concrete
Validating LLM-generated specifications presents a funda-                test cases—specific heap configurations and input val-
mental challenge: determining whether a specification cor-               ues—designed to expose potential specification errors.
rectly captures the intended program behavior. We address
this challenge through a multi-method validation framework               Since input examples can be complex, directly prompting
that combines formal proof-based techniques with LLM-                    LLMs to convert natural language descriptions into correct
based semantic reasoning.                                                Coq representations may introduce errors. We employ a
                                                                         three-stage pipeline to improve reliability. First, we prompt
While LLM judges can assess high-level semantic alignment                an LLM to type the natural language examples, producing
between specifications and natural language requirements,                structured typed examples with explicit type annotations.
they struggle to reliably validate the intricate logical relation-       The typed example Second, we apply deterministic Python
ships encoded in separation logic predicates. For instance,              programs to translate these typed examples into canonical
an LLM may fail to detect that a specification incorrectly               Coq format, ensuring syntactic correctness. Third, we pro-
allows aliasing between supposedly disjoint heap regions,                vide the LLM with both the typed Coq examples and the
or that a postcondition is too weak to establish necessary               original natural language description to generate refutation
memory-safety guarantees. Conversely, formal methods                     test cases.
provide rigorous guarantees but require concrete test cases
to instantiate symbolic specifications.                                  We use a carefully designed prompt to convert QCP spec-
                                                                         ifications into refutation test cases in Coq. The prompt
Our key insight is that input-output test cases—ubiquitous in            provides several examples, each following the same mecha-
competitive programming and software testing—can bridge                  nized structure to facilitate the conversion. Each example be-
this gap by providing concrete program behaviors against                 gins with let arg := ... to bind each input variable
which specifications can be formally checked. Each test                  to concrete values. After introducing the input variables,
case grounds abstract separation logic assertions in concrete            it uses let result := ... to compute the output ob-
heap configurations, enabling automated theorem provers to               tained from the specification. Finally, we assert that this
either validate the specification or discover counterexamples            result is not equal to the expected output value from the
that definitively refute it.                                             LeetCode problem description.
                                                                         Figure 3 illustrates the standard format of a refutation ex-
4.1. Counterexample-Guided Refutation
                                                                         ample. Here, tr and val denote the input tree and the
A fundamental asymmetry exists between proving and dis-                  value to be inserted, respectively. The variable result
proving specifications: establishing correctness requires rea-           represents the tree produced by the insertion function, while
soning over all possible inputs, whereas refuting it requires            expected denotes the tree described by the natural lan-
only a single counterexample. We exploit this asymmetry                  guage specification. The goal asserts that result is not
through a refutation-based validation strategy. While pass-              equal to expected, thereby refuting an incorrect candi-
ing validation on many test cases provides no guarantee                  date specification.
of correctness, finding a single input-output pair that vio-
                                                                         To ensure correctness, we apply automated sanity checks
lates the postcondition definitively proves the specification
                                                                         before validation: (i) for each input variable x appearing in
incorrect.
                                                                         the natural language test case, we verify a corresponding
Formally, let post denote the postcondition of a candidate               let x := ... binding exists in the generated Coq file;
specification. The specification is incorrect if there exists an         and (ii) we reject any generated code containing admit,
input-output pair (in, out) that violates the postcondition:             Parameter, or Axiom declarations that would trivialize
                                                                         the proof.
                  ∃in, out · ¬post(in, out)                   (1)
                                                                         Automated Counterexample Validation. For each can-
For leetcode problem, every problem several examples
                                                                         didate test case, we instantiate the negated specification and
(mostly 2 or 3) are provided. We can direcly use those
                                                                         attempt to discharge the proof goal using Coq’s hammer
examples in generating ¬post(in, out).
                                                                         tactic . Hammer bridges Coq with external automated theo-
We implement this refutation strategy by combining LLM-                  rem provers (ATPs) including Z3 , E prover , CVC4 , and

                                                                     4
                                         Submission and Formatting Instructions for ICML 2026


                                                                                                                                 Grammarly correct
                                                    Coq Predicates                        Compile by Coq
                                                                                                                                  Coq Predicates

                                                                 Refine
               C Function Signature                                             LLM
                                         LLM
                Natural Language
                   Description                            Refine
                                                                          LLM

                                                    QCP                                                                       Grammaly Correct QCP
                                                                                      Compile by QCP
                                                 Specification                                                                    Specification



    Figure 2. System architecture for LLM-based generation and refinement of memory-aware formal specifications. The pipeline consists of
    two main phases: (1) Specification Generation using LLM with in-context learning, and (2) Iterative Refinement guided by compiler
    feedback, symbolic execution, and counterexample-guided refutation to ensure both syntactic correctness.


1   Example example2:
2     let tr := empty in
                                                                                             Natural Language Description            QCP specification
3     let val := 4 in
4     let result := tree_insert (val + 1) tr in
5     let expected := (make_tree empty 4 empty) in                                                         LLM
6     result <> expected.
7   Proof.
8   Admitted.                                                                                      Typed Examples



    Figure 3. Example format of a Coq refutation test case (tree                          Judge the Format by Python programs
    insertion). The test binds concrete inputs, computes result, and
    asserts it differs from the expected output.

                                                                                                                           LLM

    Vampire . It translates Coq goals into first-order logic, in-
                                                                                                       Judge the Format by Python programs
    vokes these ATPs to find proofs, and reconstructs successful
    proofs in Coq’s native format. If hammer discharges the                                                      Refuted Coq Test Cases
    negated goal for any test case, the specification is formally                                                Can be proven by hammer
    refuted—the test case serves as a machine-checked coun-
                                                                                                                  Incorrect Specification
    terexample. While hammer cannot prove all theorems, it
    has demonstrated strong performance on verification-related
    goals in large-scale projects .
                                                                                Figure 4. Counterexample-guided refutation workflow. Given a
                                                                                candidate specification, we negate the postcondition and attempt
    5. Dataset Construction                                                     to find a test case satisfying the precondition but violating the
                                                                                postcondition. If such a counterexample exists, symbolic execution
    A major bottleneck in evaluating LLM-based formal spec-                     in Coq can concretely demonstrate the specification’s incorrectness
    ification generation is the scarcity of suitable benchmarks.                by exhibiting the violating heap state.
    Existing C programming datasets often lack formal function
    signatures, focus primarily on implementation correctness,
                                                                                implicit memory layout assumptions.
    or are limited in scale and algorithmic diversity. To address
    these limitations, we introduce L EET C ODE -C-S PEC, a com-                From the initial collection, we identified 439 problems (with
    prehensive benchmark designed specifically for memory-                      IDs below 837) whose data structures are compatible with
    aware formal specification generation.                                      QCP’s built-in separation logic predicates. To standardize
                                                                                the problems, we manually removed constraints from the
    We first scraped 2,766 C-language problems from LeetCode,
                                                                                problem descriptions that are irrelevant to functional (input-
    capturing natural language descriptions, input/output exam-
                                                                                output) correctness. These constraints (e.g., 0 <= m, n
    ples, and function signatures. We then manually sanitized
                                                                                <= 200) are introduced primarily to bound execution time
    the problem descriptions and signatures to ensure syntactic
                                                                                or memory usage on the LeetCode platform, and do not
    consistency. Unlike existing datasets that prioritize solution
                                                                                affect the intended semantic behavior of correct solutions.
    code, our benchmark focuses on function signatures as the
    primary target for specification generation, which necessi-                 We further restrict our dataset to problems with a single
    tates reasoning about parameter types, return values, and                   return value, as supporting multiple output values would

                                                                            5
                                   Submission and Formatting Instructions for ICML 2026

require additional specification machinery that is orthogonal        Table 1. Distribution of the L EET C ODE -C-S PEC -200 benchmark
                                                                     across difficulty levels (as assigned by LeetCode) and data struc-
to the focus of this work. This restriction still preserves          tures. Note that a single problem may involve multiple data struc-
substantial complexity: many problems involve intricate              tures.
memory operations, such as in-place array manipulation,
tree restructuring, and linked list transformations.                         Category             Count     Percentage (%)
Despite this restriction, the selected problems involve non-                 Difficulty
trivial algorithms and complex data structures, and are sub-                 Easy                     62                 31.0
stantially more challenging than benchmarks used in prior                    Medium                   97                 48.5
work on C program verification. Prior benchmarks typically                   Hard                     41                 20.5
focus on simple algorithms like list reversal, array copy-
                                                                             Data Structure
ing, or basic tree traversals. In contrast, our benchmark
                                                                             Integer/Number          147                 73.5
includes algorithmic challenges such as dynamic program-
                                                                             Array                    75                 37.5
ming over arrays, graph algorithms on tree structures, and
                                                                             String                   53                 26.5
complex string manipulations requiring precise reasoning
                                                                             Tree                     41                 20.5
about memory boundaries and pointer arithmetic.
                                                                             Linked List              14                  7.0
From this candidate pool, we randomly sampled 200 prob-
lems to form our core evaluation benchmark, L EET C ODE -
C-S PEC -200. This benchmark spans five data structure                 CA, 2000. Morgan Kaufmann.
categories: integers, strings, one-dimensional arrays, linked
lists, and binary trees. We manually verified each entry in
the benchmark to ensure accuracy.
To bridge the gap between LeetCode’s native C types and
formal logic, we developed systematic transformations for
QCP compatibility. For example, the LeetCode TreeNode
structure is mapped to QCP’s tree predicate, which formal-
izes both tree topology and node content using separation
logic. For boolean types, we employ a preprocessor-based
macro that aliases bool to integers, preserving the origi-
nal LeetCode signatures while enabling formal verification.
Detailed transformation rules are provided in Appendix.
We will release L EET C ODE -C-S PEC -200 to the research
community to support further work in automated formal ver-
ification. Table 1 summarizes the distribution of the bench-
mark; it reflects a realistic difficulty range, with medium
problems accounting for 48.5%, followed by easy (31.0%)
and hard (20.5%) problems. We classify a problem as in-
volving a specific data structure if that type appears in any
input or output argument. Consequently, the majority of
problems (73.5%) involve integers or numbers, underscor-
ing the demand for arithmetic and logical reasoning. Arrays
are present in 37.5% of problems, strings in 26.5%, binary
trees in 20.5%, and linked lists in 7.0%. These categories are
not mutually exclusive, as many problems require reasoning
about multiple data structures—such as manipulating an
array while returning an integer result—leading to a total
percentage exceeding 100%.

References
Langley, P. Crafting papers on machine learning. In Pro-
  ceedings of the 17th International Conference on Ma-
  chine Learning (ICML 2000), pp. 1207–1216, Stanford,


                                                                 6
