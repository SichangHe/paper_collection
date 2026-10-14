                                                      LLM-Based Invariant Testing for Software
                                                                 Functional Bugs
                                                             Ruogu Yang‡§                                    Yifeng He§                                         Yundi Xu
                                                        Northeastern University                    University of California, Davis                   University of California, Davis
                                                       yang.r4@northeastern.edu                          yfhe@ucdavis.edu                                 xydxu@ucdavis.edu

                                                            Yuqing Wei                                                               Hao Chen
                                         Southern University of Science and Technology                                    The University of Hong Kong
                                                12311043@mail.sustech.edu.cn                                                   chenho@hku.hk



                                            Abstract—Manually writing unit tests to uncover functional                cannot reason about API source or documentation, generalize
                                         bugs in software libraries is not only time-consuming but also               poorly to new libraries, and yield low-diversity, low-coverage
                                         requires a deep understanding of the intended semantics of the               tests [14, 15].
                                         APIs. Heuristic-based test generation methods suffer from low
                                         usability because they cannot reason about program semantics                    Prior automated approaches share common limitations.
                                         or interpret source code and documentation as humans do.                     Coverage-guided fuzzers waste effort exploring shallow error-
arXiv:2607.18711v1 [cs.SE] 21 Jul 2026




                                         Traditional fuzzing techniques like OSS-Fuzz often rely on crashes           handling paths. Meanwhile, although several LLM-based
                                         to detect bugs, but functional bugs do not always cause crashes.             unit test generation (LLM-UT) methods have been proposed
                                         To overcome these limitations, we present L ISA, a novel LLM-                recently [16–19], these approaches frequently produce one-
                                         based invariant testing framework for software functional bugs.
                                         L ISA iteratively generates API sequences and program invariants             shot tests with trivial oracles such as assert(ptr !=
                                         guided by API n-gram feedback, achieving higher bug-detection                NULL) [18, 19]. End-to-end coding agents suffer from search-
                                         rates and competitive code coverage compared with both fuzzing               space explosion when planning, invoking tools, and generating
                                         and prior LLM-based test generation approaches, and reporting                tests jointly [20].
                                         each finding as a high-confidence bug candidate for developer                   Prior LLM-UT work has evolved from generating only
                                         confirmation.
                                            Index Terms—Large language models, software testing, test                 assertions for simple functions [21] to producing complete
                                         generation                                                                   test functions and full test files [16–18], and typically evaluates
                                                                                                                      them by pass rate and coverage [22]. He et al. [18] note
                                                                    I. I NTRODUCTION                                  that this setup lacks a reliable oracle, the long-standing
                                                                                                                      oracle problem [23–25]: when a generated test fails, a reader
                                            Software defects (bugs) cause security vulnerabilities and
                                                                                                                      cannot tell whether the LLM’s predicted input–output pair
                                         unintended behaviors, and testing grows harder as software
                                                                                                                      is wrong or the API is, so these methods cannot reliably
                                         scales [1–3]. Among automated techniques, coverage-guided
                                                                                                                      distinguish incorrect oracles from genuine faults. We define
                                         grey-box fuzzing is the most widely adopted [4–6]: it mutates
                                                                                                                      L ISA’s invariant-based alternative and its scope in Section III-F.
                                         inputs to explore deep paths for crashes and hangs, and has un-
                                                                                                                         To mitigate this oracle ambiguity, we propose decoupling
                                         covered vulnerabilities in thousands of real-world projects [7].
                                                                                                                      LLM-UT into two independent components: 1) sequences
                                            However, fuzzing primarily targets implementation bugs that
                                                                                                                      of API calls representing the testing semantics, 2) assertions
                                         crash the program, which sanitizers can catch [4]. Functional
                                                                                                                      that verify execution results. To maximize code coverage in
                                         bugs, by contrast, stem from incorrect logic and produce wrong
                                                                                                                      the generated API sequences, we follow prior work [12, 26]
                                         results without crashing; they are hard for dynamic testing to
                                                                                                                      by using feedback to guide the LLM in selecting diverse
                                         detect and have been called “machine un-auditable” [8], as
                                                                                                                      API combinations and permuting their orders. Because we
                                         catching them requires domain knowledge of the API’s intended
                                                                                                                      generate only API sequences rather than fuzzing drivers, as
                                         semantics that current automated techniques lack.
                                                                                                                      in P ROMPT F UZZ [26], we introduce a novel n-gram API
                                            Unit testing is the primary method developers use to identify
                                                                                                                      combination coverage as a guidance mechanism (Section III-E).
                                         functional bugs [9]. Unit testing requires developers to manually
                                                                                                                      To improve the reliability of the generated assertions, we
                                         specify three elements: inputs, expected outputs, and the testing
                                                                                                                      relax the requirement for LLMs to predict exact input-output
                                         semantics that sequence the calls; we refer to the tested
                                                                                                                      pairs and instead ask them to infer program invariants [8,
                                         functions as the library’s APIs and their invocation order as
                                                                                                                      27]. We refer to this testing paradigm as invariant testing. To
                                         an API-sequence. Writing tests by hand is costly and often
                                                                                                                      construct valid unit tests from these components, we propose
                                         neglected [10, 11], while heuristic-based generators [12, 13]
                                                                                                                      chunk-invariant reasoning (Section III-G2), which partitions
                                           ‡ Work done while interning at UC Davis. § Equal contribution.             the finalized API sequence into multiple semantically coherent
                                           This is the authors’ extended version of the paper accepted at ISSRE 2026. chunks and instructs the LLM to insert invariants at the end of
each chunk as critical program points. In this setting, invariants   bugs typically exhibit universal rather than domain-specific
serve as oracles that are weaker as specifications yet more          patterns, such as software crashes or hangs. Owing to their
robust as oracles than those required by formal verification (two    universality, such bugs can often be detected by static code
distinct axes, elaborated in Section III-F), enabling us to check    analysis tools with predefined rules [28], or by automated
useful correctness properties without requiring precise input-       dynamic testing techniques targeting behaviors like crashes,
output specifications. By decoupling API-sequence exploration        such as fuzzing [4] and symbolic execution [29].
from invariant construction, this two-stage design diversifies • Functional bugs: These arise when developers make logical
generated tests and improves their practicality. It achieves         errors in the program. When triggered, the API does not
competitive code coverage and enables automated detection            crash or terminate abnormally; instead, it produces incorrect
of functional bugs without precise input-output specifications.      outputs that deviate from the expected behavior described
L ISA provides an end-to-end automated pipeline for unit test        in the documentation. Detecting functional bugs in software
generation. While finding unknown bugs is a significant benefit,     libraries typically requires developers to manually craft
the generated test suites are themselves valuable for regression     expected input-output pairs as test cases [9], or to apply
testing. This invariant-based design mitigates, but does not         formal verification techniques [30] to prove correctness.
fully solve, the oracle problem; accordingly, L ISA reports high-     Due to their context-specific nature, testing for functional
confidence bug candidates that a developer confirms rather bugs is difficult to automate. Manually crafting high-quality test
than acting as a fully autonomous bug detector.                    cases requires developers or domain experts to spend substantial
   We present L ISA, a novel LLM-based invariant testing frame- time writing non-feature testing code. Moreover, there is no
work for software functional bug detection. L ISA generates direct way to optimize these tests for exploring deep program
unit test functions iteratively, guided by n-gram API coverage, states, except by investing additional effort in writing more
and inserts program invariants between API chunks to detect tests. Formal verification also requires manual setup of theorem
functional bugs in the target APIs. We evaluated L ISA on 7 real- provers, and such tools are not as easily integrated into the
world C/C++ libraries. Compared with state-of-the-art fuzzing software development lifecycle (i.e., continuous development
tools (OSS-Fuzz [7]), the unit tests generated by L ISA achieve and continuous integration) as fuzzing and unit testing. A
higher average branch coverage at the library level. Moreover, middle ground for detecting functional bugs automatically
when evaluated on re-introduced historical functional bugs, is property-based testing [31], which allows developers to
L ISA detects nine more bugs than the state-of-the-art LLM- specify the expected properties of APIs and then generates
based unit testing framework CITYWALK [19]. We make the random (or even coverage-guided [32]) inputs to test these APIs
following contributions:                                           against their specified properties. However, no fully automated
• We present L ISA , a novel LLM-based invariant testing frame- testing approach yet exists that can detect functional bugs
   work that detects functional bugs in software libraries. To the while remaining as easy to integrate into modern development
   best of our knowledge, L ISA is the first to recast functional- pipelines as fuzzing tools for implementation bugs.
   bug detection as a decoupled two-stage problem, feedback-
   guided API-sequence synthesis followed by documentation- B. Program Invariants
   grounded invariant insertion at chunk boundaries, so that
   the contribution is the decomposition mechanism rather than        Program invariants are conditions in code that must hold
   the integration of existing components, enabling automated for the program to proceed to the next stage of execution [34].
   detection of functional bugs without precise input-output As the name suggests, these conditions remain invariant with
   specifications.                                                 respect to the program’s state: for all internal states and variable
• We introduce chunk-invariant reasoning and n-gram API            configurations, they must be satisfied. In modern large-scale
   coverage feedback to decouple API-sequence exploration software systems and libraries, developers often assert such
   from invariant construction, enabling accurate and diverse invariants at critical program points, i.e., locations in the code
   unit tests.                                                     where certain conditions must hold for the function to produce
• We present L ISA -B ENCH , the first benchmark for evaluating    correct outputs.
   functional bug detectors. We empirically validate L ISA on         Listing 1 shows an example implementation from the
   L ISA -B ENCH, and its generated tests achieve higher average LLVM [33, 35] library. This example contains two critical
   branch coverage than existing fuzzing approaches and detect program points, where developers use assertions to ensure the
   more functional bugs than LLM-UT methods.                       desired properties of the API. The first critical point occurs
                                                                   after initialization, where developers use invariants to verify
                        II. BACKGROUND
                                                                   that all variables are successfully initialized before proceeding
A. Bugs in Software Supply-Chain                                   to further optimization. The second occurs after compiler
   Bugs in the software supply chain (i.e., upstream libraries) optimization, where developers ensure that the computed results
are generally categorized into two classes:                        satisfy necessary correctness properties. In general, if the
• Implementation bugs: These occur when developers make            appropriate program invariants hold at their corresponding
   mistakes in the code implementation, leading to incorrect han- critical program points, it is less likely that the program contains
   dling of types, memory, or system resources. Implementation functional bugs.
 1    template <class GroupT>                                     1    void Purchase_succeeds_when_enough_inventory() {
 2    std::vector<Matcher *>                                      2        // arrange
 3    llvm::gi::optimizeRules(                                    3        Store store; Store_Init(&store);
 4        ArrayRef<Matcher *> Rules,                              4        Store_AddInventory(&store, Product_Shampoo, 10);
 5        std::vector<std::unique_ptr<Matcher>> &                 5        Customer customer = {0};
               MatcherStorage)                                    6
 6    {                                                           7        // act
 7      // setting up                                             8        bool success = Customer_Purchase(&customer, &store
 8      std::vector<Matcher *> OptRules;                                        , Product_Shampoo, 5);
 9      std::unique_ptr<GroupT> CurrentGroup = std::              9
             make_unique<GroupT>();                              10        // assert
10                                                               11        assert(success == true);
11        // invariant to check initialization property          12        assert(Store_GetInventory(&store, Product_Shampoo)
12        assert(CurrentGroup->empty() && "Newly created group                   == 5);
                isn’t empty!");                                  13    }
13        unsigned NumGroups = 0;                                14
14                                                               15    void Purchase_fails_when_not_enough_inventory() {
15        // core logic                                          16        // arrange
16        auto ProcessCurrentGroup = [&]() {...};                17        Store store; Store_Init(&store);
17        for (Matcher *Rule : Rules) {...}                      18        Store_AddInventory(&store, Product_Shampoo, 10);
18        ProcessCurrentGroup();                                 19        Customer customer = {0};
19                                                               20
20        LLVM_DEBUG(dbgs() << "NumGroups: " << NumGroups << "   21        // act
               \n");                                             22        bool success = Customer_Purchase(&customer, &store
21        (void)NumGroups;                                                      , Product_Shampoo, 15);
22                                                               23
23        // invariant to check result of core logic             24        // assert
24        assert(                                                25        assert(success == false);
25           CurrentGroup->empty() && "The last group wasn’t     26        assert(Store_GetInventory(&store, Product_Shampoo)
                  properly processed"                                            == 10);
26        );                                                     27    }
27        return OptRules;
28    }                                                               Listing 2: Examples of AAA-style unit test functions [9].
     Listing 1: Example of program invariants in LLVM [33].

                                                                  sequence generation, which produces reasonable API invocation
C. Unit Testing                                                   sequences for the library under test, and invariant insertion,
                                                                  which converts a structured API knowledge base into assertions
   Unit testing is the primary method developers use to assess inserted into the API-sequence. As depicted in Figure 1, L ISA
functional correctness during software development [9]. A first extracts library API and type definitions (Section III-B),
unit test provides a measure of correctness [9, 36], verifying generates API sequences from selected APIs, project rules,
that an API produces the expected results for given inputs. and successful examples (Section III-C), repairs erroneous
Otherwise, a logical error is present in the implementation. sequences (Section III-D), and iteratively refines them using
Because upstream libraries in the software supply chain are not API n-gram feedback [37] (Section III-E). It then partitions
standalone applications deployed in production environments, each sequence into semantically meaningful segments [38],
where testing often requires mocking, their unit tests typically converts knowledge-base information into invariants inserted
follow the classical style: arrange, act, and assert (AAA) [9]. per segment, and executes each segment to validate the
Previous work on constructing unit test generation datasets [17] invariants (repairing on failure), concatenating the validated
has also adopted this paradigm.                                   segments into the final invariant-enriched test.
   Listing 2 shows two examples of classical AAA-style unit
test functions. Both test functions begin with the arrange stage, B. API Information Extraction
where variables, memories, and objects are initialized. The          We build this component on top of P ROMPT F UZZ [26], a
tests then proceed to the act stage, where the APIs under prior LLM-guided API fuzzing framework for C/C++ libraries.
test are invoked with specified inputs. Together, the arrange P ROMPT F UZZ provides a practical front-end for library analysis
and act stages provide the testing semantics. The examples in and prompt construction, including Clang-based AST parsing
Listing 2 demonstrate invocations of a single API for simplicity; and basic LLM invocation utilities, making it a suitable
however, in practice, the act stage often involves multiple APIs foundation for our pipeline. Importantly, L ISA reuses only
composed in sequence [12]. After invoking the APIs, the final these front-end components for API extraction and prompt
assert stage verifies whether the results match the expected orchestration; we do not use P ROMPT F UZZ’s fuzzing loop,
outputs. A failed assertion indicates the presence of a logical mutation strategy, or coverage-guided driver generation.
error in the code.                                                   Following P ROMPT F UZZ, we use the abstract syntax tree
                                                                  (AST) to extract function and struct definitions from the
                      III. M ETHODOLOGY
                                                                  target library. L ISA extracts structured API metadata by
A. Overview                                                       statically analyzing header files using Clang’s AST dump
   L ISA is a framework for automated unit test generation facility, identifying function declarations, parameter and return
via LLM-based API reasoning, comprising two modules: API- types, and definitions of structs, enums, and typedef aliases by
                       Fig. 1: Overview of L ISA’s iterative feedback-guided API sequence generation.


parsing the generated JSON-formatted AST. All types are then       before use,” which the ablation study (Table V) shows is one of
canonicalized into a standardized representation that preserves    the recurring rules whose removal degrades execution success
pointer mutability and array size information. This metadata is    on stateful libraries. The Successful Examples slot in
serialized into structured schemas that serve as the foundation    the prompt (Section III-C) is populated the same way: L ISA
for API-sequence generation, not fuzzing-driver synthesis.         retains sequences that compiled and executed in previous rounds
                                                                   and injects them as in-context exemplars for the next round,
C. API Sequence Generation
                                                                   so the few-shot pool grows automatically.
   L ISA adopts a self-adaptive few-shot approach [39] to gen-        2) Repair: Rather than discarding erroneous seeds, L ISA
erate API sequences using a generative large language model        performs automatic repair by invoking a large language model
(LLM), leveraging its capability to understand and produce         (LLM) with an error-guided prompt. When the generated
valid code for open-source libraries. We use gpt-5-mini            API sequence fails either during compilation or execution,
for its favorable cost and latency in this exploration-heavy       L ISA extracts the corresponding error message, including the
phase, and switch to the stronger gpt-5.1 for L ISAinv             error type, code, and diagnostic details to construct a verbal
(Section III-G), where invariant reasoning benefits from a         feedback [40, 41]. These fields are substituted into our repair
more capable model. Because L ISA’s gains stem from its            template (Figure 6 in Section A), which instructs the LLM to
architecture rather than the base model, as our Vanilla-LLM        regenerate a fixed version of the same program without altering
ablation indicates (Table IV), these component gains are largely   its overall logic or structure. The template explicitly restricts the
model-agnostic, and L ISA can be paired with a stronger            model from redefining the main function, changing function
model when the budget allows. To generate syntactically and        names or parameters, or introducing control-flow constructs
logically correct code, we construct a comprehensive prompt        such as loops or branches. This constraint ensures the semantic
(Figure 5 in Section A) that restricts the search space using      equivalence between the repaired code and the original while
ground-truth Library Context, Project Rules (e.g.,                 correcting low-level implementation errors (e.g., undeclared
closing opened handles), and specific API Combinations,            variables, mismatched types, or segmentation faults).
while Code Requirements enforce a straight-line ex-                   If the error type indicates an execution failure without de-
ecution policy. Augmented by Successful Examples                   tailed diagnostics, L ISA interprets it as a potential segmentation
and a structured Execution Schema (Initialize →                    fault and prompts the LLM to strengthen pointer and memory
Cleanup), the prompt guides L ISA to generate deterministic,       safety. L ISA recompiles and re-executes each repaired candidate
high-quality API-sequence that reflect a complete usage life-      to verify the fix. If the repaired sequence is still invalid, L ISA
cycle within the library’s actual implementation boundaries.       abandons the seed to prevent unnecessary API invocations and
D. Error Detection and Repair                                      computation overhead. In practice, this sequence-repair loop
                                                                   performs at most one repair attempt per erroneous program: a
   After generating the default number of API sequences, L ISA     single LLM-guided fix recovers most compilation and runtime
attempts to identify and correct errors in these sequences in      errors, whereas further attempts on a still-failing sequence
two steps: detection and repair.                                   rarely succeed and only add cost, so the seed is discarded
   1) Detection: L ISA applies two filters to validate API-        rather than retried.
sequences. Static checks use clang to compile and link the
program, rejecting any sequence that fails. Dynamic checks E. API N-Gram Feedback
run the program in an isolated Docker sandbox with a 30-            To statistically capture the local co-occurrence patterns of
second timeout and catch segmentation faults, assertion failures, API calls in real-world programs, we adopt an API-n-gram
unhandled exceptions, and hangs. Recurring error patterns feed model. Similar to n-gram models in natural language process-
back into project-specific rules for later generation rounds; ing, an API-n-gram represents a contiguous subsequence of N
for zlib, for example, repeated segfaults from calls to API invocations extracted from program traces or source code.
inflate() on uninitialized streams caused L ISA to add the For example, the sequence {open, read, close} con-
rule “ensure the stream is initialized with inflateInit() stitutes an API-3-gram, while {malloc, memcpy, free,
TABLE I: Sensitivity to the n-gram order N on zlib (3-hour          We normalize the energy of a given API function a with min-
budget). #Valid: successfully generated programs; coverage          max normalization, and ensure every API function keeps a
measured with llvm-cov.                                             non-zero selection probability by adding a small constant ε > 0:
              N     #Valid   Line Cov.   Branch Cov.                                                             E(a) − Emin
                                                                     Ê(a) = ε+(1−ε)Ē(a),       where Ē(a) =               . (2)
               2     512     71.48%       59.22%                                                                 Emax − Emin
               3     818     73.01%       60.01%
               4     705     69.89%       57.02%                       We use ε = 0.01 in our implementation, so Ê(a) ∈ [ε, 1]. At
                                                                       the first iteration every API shares the same energy (Emin =
                                                                       Emax ); in this degenerate case we skip normalization and
printf} forms an API-4-gram. By modeling which APIs co- sample APIs uniformly.
occur and in what order, the API-n-gram serves as a lightweight, Definition III.1 (Condensation transformation). Let I = [0, 1]
data-driven dependency model: it captures usage and ordering denote the interval containing the (normalized) energies of
dependencies among APIs without constructing an explicit all API functions. A function f : I → [0, ∞) is a condense
API-dependency or interaction graph, as used by dependency- transformation if it satisfies:
aware approaches such as Hopper [42] and CITYWALK [19]. 1) Strictly monotone increasing (order-preserving): ∀x, y ∈
Integrating such richer dependency models to further improve               I, x < y =⇒ f (x) < f (y).
sequence validity is a promising extension that we leave to 2) Strictly concave: for λ ∈ (0, 1) and ∀x, y ∈ I with x ̸= y,
future work. We set N = 3 for L ISA. Table I reports a                     f (λx + (1 − λ)y) > λf (x) + (1 − λ)f (y).
sensitivity analysis on zlib under an identical 3-hour budget: 3) Endpoint preserving: f (0) = 0.
N = 3 attains the highest line and branch coverage and yields
the most valid programs, whereas N = 2 under-constrains the Proposition 1 (Range compression). Any condense transforma-
sampled API combinations and N = 4 makes them too sparse tion f compresses the range of input values: for any x, y ∈ I
to satisfy, lowering both validity and coverage. We therefore with 0 < x < y ≤ 1, 1 <
                                                                                                   f (y)/f (x) < y/x.

adopt N = 3 throughout; the full sweep is also available in We prove Proposition 1 in Section B-A.
our artifact.                                                                b) Condensation: To mitigate the skewness of the energy
   1) API Scheduling: Let E denote the energy of an API distribution, we apply a condense transformation to the normal-
a. We assign a baseline energy to each API ai to initialize ized energy values. Its properties ensure that 1) API functions
the feedback loop: E(ai ) = 1. When a successful program is with higher energy always have a higher probability of being
generated, we extract all consecutive API 3-grams (triples) from selected by L ISA, and 2) the marginal effect of increasing
its execution trace T = {(ai , ai+1 , ai+2 ) | i = 1, 2, . . . , L−2}, energy decreases as energy grows. A valid condense transfor-
where L is the length of the API call sequence. For each newly mation always reduces the relative differences between energy
discovered 3-gram (ai , aj , ak ) ∈ T that has not been observed values (Proposition 1). In L ISA, we use power condensation:
before, we update the energies of all three constituent APIs:          for a given API function a, with a parameter α controlling the
                                                                       degree of condensation,
          E(a) ← E(a) + 1, for each a ∈ (ai , aj , ak )            (1)
                                                                                          C(a) = Ê(a)α , α ∈ (0, 1).              (3)
This additive reward scheme ensures that APIs appearing in We show that power condensation is a valid condense transfor-
successful execution patterns accumulate higher energy over mation in Section B-A.
time, with each API starting from the same baseline value.                   c) Distribution-aware adaptive condensation: The pa-
   2) Adaptive Condensed Normalization of Energy (ACNE): rameter α controls the degree of condensation: a small α
We assign energy to successive n-grams in the API call largely boosts the probabilities of low-energy API functions
sequence. However, assigning sampling probabilities pro- (encouraging exploration), whereas α close to 1 makes the
portional to raw energy skews the distribution heavily: as effect mild (favoring exploitation). A fixed α is suboptimal
sampling progresses, a few high-energy n-grams dominate because different stages of L ISA require different exploration–
the probabilities and cause premature convergence, leaving exploitation trade-offs: early on we want to identify likely-
other API functions under-explored. To encourage continued useful API functions quickly (exploitation), and once such a
exploration of low-energy, potentially under-explored API set is identified and sufficiently tested we want to explore other
functions, we propose ACNE, which dynamically adjusts energy potentially useful API functions (exploration). We quantify
values based on their distribution to balance exploration and the skewness of the energy distribution at iteration t with the
exploitation.                                                          coefficient of variation st = σt/µt , the ratio of the standard
      a) Normalization: Recall from Equation 1 that our energy deviation σt to the mean µt of the normalized energies at
assignment is additive: each time a successful n-gram is iteration t, and adaptively set
observed, the energies of its constituent APIs are incremented
                                                                                         αt = αmin + (1 − αmin ) e−st .            (4)
by 1. The first step of ACNE normalizes the energy values into
a probability-friendly range. Let Emin and Emax denote the Thus, when the distribution is highly skewed (large st ), αt
minimum and maximum energy values among all API functions. is automatically lowered to encourage exploration. Here αmin
controls the maximum degree of condensation; we set αmin =
0.5 (derived in Section B-B).
      d) Sampling new API functions: Finally, we use the
condensed energy values to sample new API functions. At
iteration t, the probability of selecting an API function a is
                 Ct (a)
      Pt (a) = PN            ,   where Ct (a) = Êt (a)αt .    (5)
                i=1 Ct (ai )                                                   Fig. 2: API knowledge database preparation.
We use these probabilities to sample a subset of APIs as the
API Combinations for API-sequence generation, thereby
guiding the LLM’s attention.                                          than soundness in formal verification: L ISA does not prove φ
                                                                      over all inputs, only that φ is consistent with the documented
F. The Invariants L ISA Generates                                     contract and with observed reference behavior. In that sense
   An invariant in L ISA is a Boolean predicate φ over program        L ISA’s invariants are weaker as specifications, since they
state that must hold every time execution reaches a designated        are partial and unproven, yet more robust as oracles, since
program point [8, 27, 34]. Concretely, for a generated API-           asserting a stable property is less brittle than predicting an
sequence partitioned into chunks C1 ∥ · · · ∥CN (Section III-G2),     exact output [18, 24, 25]. Because L ISA does not prove its
each invariant is a pair ⟨φ, ℓ⟩ in which ℓ is the end of some         invariants, a violation is only a high-confidence bug candidate:
chunk Ci and φ ranges over the variables, return values,              an assertion that survives the verification-and-repair loop yet
and reachable struct fields that are live at ℓ. L ISA compiles        still fails on the target build, and a developer confirms every
each such φ into an executable assert(φ); the assertion               candidate before we count it as a detected bug. We revisit the
is satisfied on a given build when it never fires and violated        residual threats this raises in Section VI-B.
otherwise. An invariant is therefore a partial specification: it
constrains a property the program must preserve, such as a            G. Invariant Generation
size relation, a state flag, or a return-code contract, without          Existing studies demonstrate that LLM-based invariant
pinning down the exact input–output mapping. That partiality          generation without structured guidance struggles to produce
is what makes invariants usable as oracles for functional bugs,       effective and reliable results [27]. To overcome these limitations,
sidestepping the input–output ambiguity long recognized as            L ISA first constructs an API contract documentation knowledge
the obstacle to testing non-testable programs [24, 25].               base to guide invariant generation, as shown in Figure 2 and
   The predicates L ISA emits fall into four kinds of increasing      detailed in Section III-G1.
semantic depth. Structural invariants assert that a handle or state      As shown in Figure 3, L ISA adopts a segment-based
object is well-formed after a constructor-like call. Value-range      invariant generation strategy to incrementally augment API-
invariants keep a field within its documented domain. Relational      level programs with assertions. The target program is first split
and conservation invariants link live values across a call: the       into multiple segments. For the first segment, the LLM takes
bytes a call consumes plus the bytes that remain equal the input      the raw code as input and outputs the code augmented with
size, for example. Documentation-derived semantic contracts           inferred assertions. For each subsequent segment, the input
encode behavioral intent that exact input–output oracles cannot       consists of the previously processed code and assertions, the
easily express, such as the numeric identity of a checksum            current code segment, and relevant API documentation. The
API or the guarantee that a destructor resets a state object. The     model then generates assertions for the current segment by
first two kinds are largely structural; the last two carry the        leveraging both the program context and external knowledge.
intent that lets L ISA detect silent logic errors. L ISA produces     All processed segments are concatenated to produce the final
these predicates by prompting the LLM with the chunk code             unit tests enriched with invariants.
and the relevant API documentation from the knowledge base               Notably, LLM infers likely invariants based on the con-
(Section III-G1), seeded by documentation-mined contracts and         structed API contract documentation. When an execution
Daikon candidates; the algorithm and its verification-and-repair      failure occurs, L ISA starts a repair loop and retries up to
loop are the subject of Section III-G2. A documented read-only        five times to eliminate transient test bugs, such as mistakes in
guarantee, for instance, becomes assert(memcmp(buf,                   the generated test code or invariants. If the failure persists
saved, n) == 0) on the relevant input buffer.                         after all retries, L ISA marks it as a high-confidence bug
   A L ISA invariant is semantically valid when it does not           candidate, since repeated failures are unlikely to be caused by
contradict the documented contract of the APIs in scope               random or temporary test errors. Nevertheless, because semantic
and holds on the reference build of the library, so that a            reasoning is inherently complex, some persistent failures may
later violation signals a behavioral deviation rather than an         still result from subtle test-side inaccuracies rather than actual
over-strong assertion. L ISA enforces the first condition during      implementation defects. These candidates are forwarded to
knowledge-base construction (Section III-G1) and the second           human reviewers for final verification.
automatically, by executing each candidate against the reference         1) Building API Knowledge Database: We build the API
build before retaining it. This is a deliberately weaker guarantee    contract knowledge base through a hybrid approach: 1) Auto-
                             Fig. 3: Overview of L ISA’s incremental invariant generation pipeline.


mated Extraction: Daikon [43] mines likely invariants from unknown bug for human inspection, discard the assertion,
executable API sequences, and an LLM extracts intended in- and proceed. After all chunks are processed, the accumulated
variants from official API documentation [44] (e.g., “read-only” program forms the final invariant-enriched test. Compared with
or “no internal state modified”). 2) Manual Filtering: We one-shot inference over the whole program, this incremental
keep a Daikon candidate only if it does not contradict the scheme shortens each prompt, localizes mistakes, and enables
documentation and does not cause assertion failures when early detection and targeted repair of over-strong assertions
added to the program. 3) Lightweight Manual Curation: We via immediate execution feedback.
supplement explicitly documented invariants missed by Daikon.
                                                                                     IV. E XPERIMENTAL S ETUP
This curation can also be performed incrementally on demand,
rather than exhaustively documenting all APIs upfront. To           A.  Research  Questions
quantify this manual cost, two annotators with 3+ years of             To evaluate L ISA, we pose the following three research
C/C++ experience, after aligning on the annotation protocol, questions. For convenience, we refer to the API sequence
independently curated the knowledge-base entries for 20 APIs, generation stage as L ISAAPI and the invariant generation stage
resolving the few disagreements on which invariants to retain as L ISAinv .
by discussion. They spent 5687 and 6231 seconds in total, i.e., RQ1 How does L ISA perform in C/C++ unit test generation,
4.7 and 5.2 minutes per API respectively (overall mean 5.0                and what advantages does it offer compared to existing
minutes per API), indicating that on-demand curation costs                approaches? We evaluate L ISA’s effectiveness in gener-
only a few minutes per API. We detail how Daikon-mined and                ating valid, meaningful C/C++ unit tests and compare it
documentation-derived invariants are reconciled in Section E.             against state-of-the-art methods.
   2) Chunk-level Invariant Generation: To keep reasoning RQ2 How does each component impact the performance of
local and stable, we partition each generated program into                L ISA? L ISA consists of two stages, each comprising
smaller chunks [45]: during API-sequence construction the                 multiple components that contribute to its overall per-
LLM emits inline step markers (// STEP1, // STEP2, . . . )                formance. We conduct ablation studies to understand
that we use to split the program by regular expressions. We then          the contribution of each component to L ISA’s overall
process the N chunks C1 , . . . , CN left-to-right. For chunk Ci ,        effectiveness.
the prompt contains the already-accepted code and assertions RQ3 How effective is L ISA at detecting real-world functional
from C1 . . . Ci−1 , the raw code of Ci , and the documentation           bugs? We evaluate L ISA’s effectiveness in detecting bugs.
for the APIs it uses; the LLM returns Ci augmented with                   Specifically, we focus on previously reported functional
candidate assertions. This preserves prior state while keeping            bugs in real-world projects, as these cases have been
the context bounded.                                                      manually verified and confirmed by actual developers.
      a) Verification-and-repair loop: Each set of candidate as-         a) Baseline: To address these questions, we compare
sertions for Ci is immediately checked: we compile and execute L ISA with a state-of-the-art unit test generation framework
C1 ∥ · · · ∥Ci and accept the assertions if no failure occurs. When and relevant fuzzing techniques. 1) CITYWALK [19] is
failures arise, we enter a bounded repair loop (the invariant- a recent C/C++ unit test generation framework that uses
repair loop, up to K=5 attempts by default). In contrast to the project-dependency awareness and language-specific knowledge
single-attempt sequence-repair loop (Section III-D), a failing to improve test reliability and quality. 2) OSS-Fuzz [7] is
assertion is often salvageable by weakening or correcting an Google’s continuous fuzzing platform for open-source software.
over-strong invariant, so a few extra attempts recover many It combines coverage-guided fuzzing with continuous integra-
otherwise-discarded tests; we cap at K=5 because gains plateau tion to detect bugs and security vulnerabilities in widely used
beyond that. At each attempt, the LLM receives the failing libraries. CITYWALK represents the state-of-the-art in LLM-
assertion, triggering input (if available), and error trace, and is based unit test generation, making it a natural benchmark for
asked to weaken, repair, or remove the assertion. If the failure assessing L ISA’s ability to generate valid and high-quality unit
persists after K attempts, we flag the seed as a potential tests. OSS-Fuzz serves as a widely adopted industrial standard
TABLE II: Benchmark for evaluation. LoC: line of code. #APIs:    rate and coverage yet detects nothing. Neither family, therefore,
number of public APIs.                                           evaluates whether generated tests can expose functional defects.
               Library   Commit ID   LoC    #APIs                   To fill this gap, we introduce L ISA -B ENCH, a benchmark
                                                                 specifically designed for evaluating functional-bug-oriented
               zlib      5a82f71      30k      87
               libpng    0f07f70      57k     246                unit test generation for C/C++ libraries. We select 7 real-
               libpcap   d81c01c      58k      84                world open-source C/C++ projects from GitHub, five of which
               sqlite3   7efded5     413k     289                include historical bugs. The projects are selected according
               lcms      8888d84      45k     286
               cJSON     c859d25      10k      76                to four criteria: (1) the library exposes a public C/C++
               re2       a4b2aee      28k      70                API; (2) it builds and executes in our environment with
                                                                 reasonable effort; (3) it has sufficient functional complexity
                                                                 for invariant-based testing; and (4) historical bug reports
for fuzzing-based bug detection, providing a strong baseline or commits are available, enabling confirmed functional-bug
for evaluating L ISA’s effectiveness in code coverage and bug cases. We also intentionally include projects from different
detection. For OSS-Fuzz, we use the official fuzzing harnesses application domains and codebase sizes to avoid overfitting the
from the OSS-Fuzz GitHub repository and run libFuzzer evaluation to a single library style. As shown in Table II, these
for 3 hours on the same library version (identical commit) projects span diverse application domains: data compression
as L ISA. We measure branch and line coverage for all tools (zlib [52]), PNG image processing (libpng [53]), network
independently using llvm-cov with identical compiler flags, packet capture (libpcap [54]), an embedded SQL database
following Fuzzbench’s recommendation [46] to use Clang engine (sqlite3 [55]), color management (lcms [56]), structured-
source-based coverage rather than fuzzer-reported metrics. format parsing (cJSON [57]), and regular-expression matching
Section C records the remaining design and measurement (re2 [58]). Spanning small to very large code bases, these
details (harness handling, library-level coverage, and the libraries let us curate historically reported, developer-confirmed
comparison with H OPPER).                                        functional bugs and directly measure whether generated tests
      b) Scope of baselines: We considered agentic SE work- detect real-world defects.
flows (SWE-agent [47], OpenHands [48]) and recent LLM-UT
methods (IntUT [49]) and excluded them for three reasons. C. Metrics
Language: SWE-agent and OpenHands target Python [50]
and IntUT targets Java; none supports C/C++ test generation,        1) Evaluating L ISAAPI : We evaluate L ISAAPI using four
whereas L ISA targets C/C++ library APIs. Toolchain coupling:    standard   metrics [59, 60]: Compilation Success Rate (CSR)
their pipelines rely on language-specific infrastructure (Python and   Execution    Success Rate (ESR) measure the fractions of
execution environments; IntUT’s Java static analysis for test-   generated   API-sequences    that compile and run without runtime
intention derivation), so a fair comparison would require us to  errors, respectively;  Line  Coverage    (LC) and Branch Coverage
re-implement each system for C/C++ rather than run an existing   (BC)   are  measured   with llvm-cov.
tool. Task and oracle mismatch: SWE-agent and OpenHands             2) Evaluating L ISAinv : We evaluate L ISAinv using two
resolve a given issue by patching a known defect rather than     metrics   that reflect both its ability to generate assertions and
discovering unknown functional bugs, whereas IntUT relies        their  quality.
on the exact-output oracle that L ISA explicitly avoids. Our           a) Average Unique Verifications Count (AUVC): AUVC
Vanilla-LLM baseline and component ablations (Table IV, measures the expected number of valid, unique verifications
Table VI) address the orthogonal concern that L ISA’s gains produced per input seed. Let Ttotal be the valid seeds from
might come from its iterative generate-and-repair loop rather L ISAAPI and Tpass ⊆ Ttotal those that still compile and execute
than the invariant oracle: they disable L ISA’s components after invariant insertion; for t ∈ Tpass , let    P U (t) be its number of
while keeping the same underlying LLM. We ground key             unique   verifications.  Then   AUVC     =    t∈Tpass U (t) / |Ttotal |.
parameters similarly: N =3 follows from the sensitivity analysis Test  cases   whose   invariants  are  invalid  or violate intended
in Table I, and the maximum condensation factor αmin =0.5        behavior    are excluded   from   T pass  and thus  contribute zero,
follows from the analytical derivation of ACNE in Section III-E  penalizing    failed  generation.   Uniqueness    is  semantic, not
and Section B-B.                                                 syntactic:  two   annotators  with  3+  years of C/C++    experience
                                                                 label each assertion, treating repeated queries over an evolving
B. L ISA -B ENCH                                                 stream state as distinct while collapsing syntactically different
   Existing benchmarks are insufficient for functional-bug- but equivalent predicates such as x >= 1 and x > 0 for
oriented test generation. Fuzzing benchmarks such as x ∈ Z. Disagreements are resolved by discussion to consensus
Magma [51] and FuzzBench [46] curate only crash-triggering (full protocol in Section D-A).
bugs (e.g., overflows, use-after-free) that manifest as memory         b) Historical Bug Detection Rate (HBDR): We measure
errors, not the silent logic errors functional bugs produce. fault detection via historical bug re-introduction: for five
LLM-UT benchmarks such as TestGenEval [22] rely on libraries, we revert five previously fixed bugs in each (25
pass rate and coverage, which are insensitive to the oracle bugs in total). A bug counts as detected when the generated
problem: an assertion-free suite trivially achieves high pass test passes on the patched branch but fails on the buggy one.
TABLE III: Comparison of Compilation and Execution Success                                                                                 44.3
Rates between Vanilla LLM and L ISA.                                        40            37.4
                                                                                                    L ISA          CITYWALK
                                                                                 34.3
                      Vanilla LLM         L ISA




                                                                     AUVC
           Library                                                                                 23.6     21.9                 20.6
                     Comp.    Exec.   Comp.    Exec.                        20                                          17.7
                                                                                             9.5                                             11.8
           libpcap   80.0%   45.2%    99.3%   90.4%                                 7.4               7.9       8.2        7.6      9.1
           lcms      92.0%   30.6%    95.0%   77.5%
           zlib      94.3%   92.6%    99.5%   98.6%                         0
           sqlite3   88.3%   28.6%    98.3%   91.5%                               zlib      re2    libpng   libpcap      lcms     sqlite   cJSON
           re2       96.4%   73.0%    100%    99.9%                                                         Libraries
           cJSON     56.8%   56.1%    100%    99.4%
           libpng    65.1%   38.2%    93.5%   79.2%               Fig. 4: Comparison of AUVC between L ISA and CITYWALK.
           average   81.8%   52.0%    97.9%   90.9%


TABLE IV: Code Coverage Comparison: L ISA vs. Vanilla           sqlite3 (31.06% vs. 14.40%). This confirms L ISA’s n-gram
LLM vs. OSS-Fuzz. All tools were run for 3 hours. Bold          feedback and repair mechanisms are essential for guiding LLM
indicates the best performance.                                 beyond shallow happy paths to explore deep, unseen code.
                                                                      b) Comparison with Fuzzing: Compared to the industrial
             Vanilla LLM        OSS-Fuzz            L ISA
  Library                                                       standard OSS-Fuzz, L ISA demonstrates remarkable efficiency,
            Line     Branch  Line    Branch    Line     Branch
                                                                achieving higher coverage on the majority of libraries. L ISA
  libpcap  21.06% 24.60% 25.79%      27.51% 27.48% 30.32%
  lcms     30.28% 20.82% 44.74% 34.44% 49.18% 27.59%
                                                                leads OSS-Fuzz in line coverage on five of the seven libraries,
  zlib     53.32% 41.43% 65.99%      52.81% 73.01% 60.01%       with gains ranging from +1.7% on libpcap to +34.5% on
  sqlite3  14.40% 10.54% 35.38% 26.60% 31.06% 22.46%            cJSON (e.g., +7.0% on zlib and +10.0% on re2). For
  re2      36.09% 41.03% 29.77%      31.62% 39.77% 46.54%
  cJSON    51.01% 47.53% 42.28%      45.52% 76.80% 69.07%       libraries requiring structured inputs (cJSON, re2) or complex
  libpng   13.01%     8.92% 22.57% 17.94% 20.21% 14.92%         state transitions (zlib), the LLM’s inherent knowledge of
  average 31.31% 27.84% 38.07%       33.78% 45.36% 38.70%       syntax and state flows bypasses the grammar barriers and state-
                                                                space traps that hinder stochastic fuzzers in short-duration runs.
                                                                Conversely, OSS-Fuzz leads on the two libraries with extensive
To draw the five bugs for each library, we scan developer- error-handling branches for malformed inputs (sqlite3,
fixed commits in reverse chronological order and keep the libpng), where input mutation excels; however, the coverage
first five whose fix message flags a non-crashing functional gained from these error paths rarely translates into the discovery
defect and whose buggy revision reproduces deterministically of functional bugs.
on our toolchain; we skip commits that fail either filter and
examine the next candidate. This protocol fixes the corpus B. Quality of Generated Oracles: AUVC
rather than hand-picking it. We prefer this design to mutation     While code coverage measures how much code is executed,
score, the alternative common in test-generation studies [61]: it does not reflect whether the execution is properly verified. We
synthetic mutants often diverge from the fault distribution of use AUVC (Section IV-C2) to evaluate the semantic richness
real software [62], whereas a developer-verified historical fix of the generated tests. We compare L ISA against CITYWALK,
bounds each bug’s semantics and repair on evidence that a the state-of-the-art LLM-based unit test generation framework.
human maintainer already accepted.                                    a) High Density of Verifications: As illustrated in Fig-
                V. R ESULTS AND A NALYSIS                          ure 4, L ISA demonstrates a substantial advantage in as-
                                                                   sertion density across all evaluated libraries. On average,
A. Coverage and Success Rate                                       L ISA generates 3.25× more unique verifications per test than
   To ensure a fair and rigorous comparison, we enforced a CITYWALK. For example, in cJSON, L ISA achieves an
strict 3-hour time budget for all dynamic execution experiments, AUVC of 44.3 compared to CITYWALK’s 11.8.
including L ISA, the Vanilla LLM baseline, and OSS-Fuzz. We             b) Semantic Depth: This performance gap stems from
present our results in Table III and Table IV. L ISA significantly fundamental differences in generation strategies. CITYWALK
outperforms both the Vanilla LLM and OSS-Fuzz across generates tests in a single pass ("one-test-per-method"), often
multiple dimensions.                                               producing simple checks such as assert(ptr != NULL)
      a) Superiority over Vanilla LLM: Our Vanilla LLM to ensure compilability. In contrast, L ISA’s dual-stage design
baseline disables all of L ISA’s key components (feedback, allows L ISAinv to focus exclusively on logic verification. By
repair, chunking, rules), retaining only basic correctness checks leveraging the constructed API knowledge base, L ISA injects
and a minimal prompt with API knowledge. The results rich, state-aware invariants, for example, validating complex
demonstrate that L ISA’s superior performance stems from its struct fields or return states, that CITYWALK misses. This
architectural design rather than the underlying LLM capability. high AUVC confirms that L ISA not only executes code but
L ISA achieves a 38% higher average execution rate and more rigorously verifies its correctness, directly contributing to its
than doubles the line coverage in complex libraries such as superior bug-finding capability.
TABLE V: Ablation study of L ISAAPI components. w/o                    2) Component of L ISAinv : Unlike L ISAAPI , whose primary
Feedback: the variant with only random selection. Comp.:            goal is to produce valid and diverse execution paths (measured
compile rate. Exec.: execution rate.                                by coverage), the contribution of the invariant generation
 Library   Variant        Comp.   Exec.   Line Cov.   Branch Cov.   component (L ISAinv ) is intrinsically linked to the ability to
           w/o Rules      99.3%   98.1%    66.48%       52.44%
                                                                    detect faults. A simple count of assertions (like AUVC) in
           w/o Feedback   99.0%   98.4%    65.58%       52.48%      ablation variants does not fully capture the correctness or
 zlib      w/o Examples   99.5%   98.3%    67.31%       53.92%      utility of those assertions. Therefore, to provide a realistic
           w/o Repair     98.8%   95.7%    67.58%       54.30%
                                                                    evaluation, we defer the detailed ablation study of L ISAinv
           L ISAAPI       99.5%   98.6%    73.01%       60.01%
                                                                    (analyzing the impact of Repair, Chunking, and Knowledge)
           w/o Rules      99.9%   98.8%    72.54%       66.22%
           w/o Feedback   100%    98.5%    71.80%       63.95%
                                                                    to RQ3. There, we evaluate how each component contributes
 cJSON     w/o Examples   99.3%   98.2%    73.20%       66.60%      to functional-bug detection, including two knowledge-source
           w/o Repair     99.8%   97.0%    72.72%       65.37%      variants: one using only Daikon outputs and one using only
           L ISAAPI       100%    99.4%    76.80%       69.07%      official documentation.
           w/o Rules      97.6%   83.2%    26.88%       19.37%         Although several L ISAAPI components are implemented
           w/o Feedback   98.0%   70.4%    21.40%       15.22%
 sqlite3   w/o Examples   96.2%   74.8%    27.27%       19.68%
                                                                    through prompts, L ISA is not simply a prompt-engineering
           w/o Repair     90.9%   51.4%    25.53%       17.87%      variant. Its main contribution is the two-stage design: it first
           L ISAAPI       98.3%   91.5%    31.06%       22.46%      explores executable API sequences, then performs invariant
                                                                    generation as a separate stage grounded in documentation and
                                                                    chunk-level reasoning. This decomposition changes both the
C. Ablation Study                                                   exploration target and how test oracles are constructed. The
                                                                    benefit is evident in the L ISAAPI ablations (Table V) and in
   We perform an ablation study on L ISA’s components,              the bug-finding results, where removing L ISAinv components
denoted L ISAAPI and L ISAinv .                                     consistently reduces detection effectiveness. These results
   1) Components of L ISAAPI : To rigorously assess the contri-     suggest the gains come from the overall framework design, with
bution of each component within L ISAAPI , we conduct an            prompting serving as merely one implementation mechanism.
ablation study on three representative libraries: sqlite3,
cJSON, and zlib. We choose these three for three reasons: D. Bug-Finding Ability
they span the complexity spectrum of our benchmark, ranging          We evaluate the practical bug-finding ability of L ISA on
from a small structured-format parser (cJSON), through a L ISA -B ENCH, targeting 25 reproduced historical functional
stateful streaming codec (zlib), to a large and highly stateful bugs across five libraries. To ensure a fair comparison, we
database engine (sqlite3); they all belong to the bug-finding aligned the execution constraints with the operational nature of
benchmark and thus reflect the settings where L ISA is ultimately each tool: • OSS-Fuzz: Guaranteed a continuous 6-hour fuzzing
evaluated; and limiting the ablation to three subjects keeps the window to maximize mutation depth. • CITYWALK: Allowed
cost of running every component variant tractable. We derive to run to completion, processing the entire set of focal methods
four variants by selectively disabling specific modules from without time truncation. • L ISA: Operated within a strict 3
the full framework: • w/o Rules: Removes project-specific hours pipeline for L ISAAPI seed generation and generated final
constraints and headers from the prompt. • w/o Feedback: unit tests through L ISAinv with the total runtime capped at 6
Replaces the n-gram guided feedback mechanism with random hours.
selection. • w/o Repair: Disables the error detection and            As shown in Table VI, L ISA (Full) achieved a total
repair loop. • w/o Examples: Removes the few-shot successful detection rate of 48% (12/25), significantly outperforming both
examples from the prompt context. We evaluate these variants CITYWALK (12%) and OSS-Fuzz (8%).
using the same metrics as RQ1. As shown in Table V, every            Fisher’s exact test confirms that these differences are
component within L ISAAPI is indispensable for effective API statistically significant: L ISA vs. OSS-Fuzz (p = 0.0036, odds
sequence generation.                                              ratio = 10.6) and L ISA vs. CITYWALK (p = 0.0121, odds
   For simpler libraries (cJSON, zlib), execution stays above ratio = 6.77). Both p-values are below 0.05.
95% even under ablation, yet the full framework still yields         The baselines’ poor performance reveals their structural
the best coverage (e.g., +7.43% line coverage over random limitations. OSS-Fuzz (2/25) detects only crash-inducing faults
selection on zlib). For complex, state-sensitive libraries such (e.g., memory corruption) and misses functional logic errors
as sqlite3, the components become critical: removing repair that do not trigger runtime aborts. Tellingly, the single libpng
(w/o Repair) drops execution to 51.4% and line coverage to defect that OSS-Fuzz caught but L ISA missed was a use-
25.53%, as LLMs frequently hallucinate invalid states. The after-free that aborts at runtime rather than a silent logic
n-gram feedback is the single most important component for error, underscoring the complementary scopes of the two
coverage: its removal yields the lowest coverage across all tools. CITYWALK (3/25), despite using LLMs, achieves a
libraries (e.g., 21.40% line coverage on sqlite3), since low detection rate because its "one-test-per-method" strategy
it otherwise steers generation toward under-explored API prioritizes compilability through extensive mocking and isolated
combinations.                                                     testing [19]. While this yields good coverage for focal functions,
                                                   TABLE VI: Bug-finding results.
                           Baselines                   Ours                                Ablation of L ISAinv
    Library   Total
                      CITYWALK OSS-Fuzz            L ISA (Full)   w/o Repair   w/o Chunk    w/o Knowledge Daikon Only          Doc Only
    cJSON       5          1              0             3              1            2               1                2             2
    lcms        5          1              0             3              1            1               1                1             1
    zlib        5          0              1             2              1            0               0                1             0
    sqlite3     5          1              0             2              1            1               1                1             1
    libpng      5          0              1             2              0            0               0                0             0
    Total      25       3 (12%)        2 (8%)       12 (48%)       4 (16%)       4 (16%)         3 (12%)          5 (20%)       4 (16%)



it cannot construct the complex, multi-step API sequences              • API Sequence Construction: L ISA first generated a valid
necessary to trigger state-related functional bugs.                      call sequence to prepare and execute the specific query
   In contrast, L ISA’s dual-stage design enables superior               "SELECT 0 OR 2" using the sqlite3_prepare_v2
detection. L ISAAPI ’s feedback-guided exploration constructs            and sqlite3_step APIs.
diverse, valid API sequences that penetrate deep program states,       • Invariant Assertion: Crucially, instead of merely checking
while L ISAinv injects invariants that reveal silent logic errors,       for a successful return code (e.g., SQLITE_ROW), L ISA
helping L ISA find nine more bugs than the best baseline.                inferred the semantic invariant of the SQL operation. It gen-
   The ablation study validates the necessity of L ISAinv ’s three       erated the strict assertion assert(val == 1), enforcing
core components. First, repair is critical for test survivability:       that the logical OR operation must yield a Boolean True
without it (w/o Repair, 4 bugs), many tests terminate pre-               (normalized to 1 by L ISA).
maturely due to minor assertion failures or syntax errors and          Consequently, although the buggy version returned 2 due to
never reach the API calls that trigger bugs. Second, chunking is       an incorrect bitwise optimization and would pass crash-based
necessary for long sequences (w/o Chunk, 4 bugs): without it,          fuzzing, L ISA’s test triggered an assertion failure.
the model struggles to maintain attention across the entire
program, missing intermediate states and failing to place              B. Threats to Validity and Limitations
assertions at key points. Third, the knowledge base provides              We organize the residual threats along the standard three axes.
essential semantic guidance (w/o Knowledge, 3 bugs). Neither           Internal validity: LLM non-determinism (Reproducibility) and
source alone suffices: Daikon-only introduces substantial noise        hyperparameter choices (Hyperparameter Settings) could bias
(5 bugs), while documentation-only covers basic requirements           the measured effect; the variance study (Table VII) shows the
but misses semantic constraints (4 bugs). Combining both               residual noise is well below L ISA’s margin over the baselines.
gives L ISA broader semantic coverage and stronger filtering           External validity: the 25-bug, five-library, C/C++-only corpus
of spurious invariants.                                                limits generalization (Benchmark scale); we mitigate this with
              VI. D ISCUSSION AND F UTURE W ORK                        a fixed selection protocol (Section IV-C) and consistent per-
                                                                       library gains rather than aggregate-only claims. Construct
A. Case Study: Silent Logic Error in SQLite                            validity: a violated invariant is a high-confidence bug candidate,
                                                                       not a proven defect (Final oracle verification), and L ISA’s recall
1    sqlite3 *db = nullptr;                                            is bounded by documentation completeness (Section III-F).
2    sqlite3_stmt *stmt = nullptr;                                           a) Benchmark scale and representativeness: L ISA -
3    sqlite3_open(":memory:", &db);
4    sqlite3_prepare_v2(db, "SELECT 0 OR 2", -1, &stmt,                B ENCH currently comprises 25 developer-confirmed historical
          nullptr);                                                    functional bugs spanning five libraries from distinct domains.
5    sqlite3_step(stmt);
6    int val = sqlite3_column_int(stmt, 0);                            While modest in absolute size, the set is assembled by a
7    assert(val == 1);                                                 fixed protocol rather than hand-picked: each bug is drawn
Listing 3: Simplified PoC derived from L ISA’s generated test          from a previously fixed historical commit, included only if
that triggers the SQLite logic bug.                                    it reproduces deterministically on our toolchain and exhibits
                                                                       a non-crashing functional symptom, and excluded otherwise.
                                                                       L ISA’s advantage is consistent across the per-library breakdown
   To illustrate L ISA’s ability to find functional bugs, we analyze   (Table VI) rather than driven by any single library, and its
a logic regression in SQLite (commit d443f0a). As described in         margin over both baselines remains statistically significant
the commit message, a regression in the query optimizer caused         (Fisher’s exact test, p < 0.05). Nonetheless, the absolute scale
the SQL expression "0 OR 2" to be erroneously evaluated as 2           limits the precision of the point estimates, and evaluation on a
(the integer value of the second operand) instead of 1 (Boolean        larger and more varied bug corpus is an important direction
TRUE). This is a classic logic error: the program executes             for future work.
valid CPU instructions and manages memory correctly, but the                 b) Reproducibility and non-determinism: Although the
mathematical result is wrong. As shown in Listing 3, L ISA             underlying LLM is non-deterministic, this affects only which
exposed this defect as follows:                                        tests L ISA generates, not their stability once generated: every
TABLE VII: Run-to-run variance of L ISA over three repetitions            e) Automation: Constructing the API knowledge database
on three representative libraries. Comp./Exec.: compilation/ex-      requires one-time manual effort, so the overall pipeline is not
ecution success rate (mean±std, %); Cov. in %; Bugs: number          yet fully automated. In principle, this step could be delegated
of the 5 historical bugs detected in each of the three runs.         to an AI agent to further reduce manual effort. However, it
 Library      Comp.       Exec.    Line Cov.   Branch Cov.    Bugs
                                                                     remains unclear whether such automation can match the quality
                                                                     and reliability of human curation. Developing and evaluating
 zlib        99.8±0.3   98.3±0.5   70.5±2.1     57.1±2.5     2, 2, 2
 cJSON       100±0.0    98.9±0.5   74.6±3.5     67.5±2.9     3, 3, 2 agent-based alternatives for this stage is an important direction
 sqlite3     98.5±0.9   90.0±3.3   31.4±1.8     22.8±1.5     2, 2, 2 for future work.

                                                                    C. Future Work
                                                                       Beyond automating knowledge-base curation and mining
generated test is a fixed C/C++ program that compiles and
                                                                    undocumented conventions, as discussed above, two extensions
executes identically on every run, so L ISA does not produce
                                                                    look promising. First, integrating richer API-dependency mod-
flaky tests. Non-determinism during generation is further
                                                                    els, such as those used by Hopper [42] and CITYWALK [19],
dampened by the two repair loops, which execute each
                                                                    could further raise the validity of generated sequences beyond
candidate against the reference build and discard transient
                                                                    what the n-gram model captures. Second, extending L ISA
or unstable assertions, retaining only invariants that pass stably.
                                                                    to managed-language libraries (Python, Java) would test the
To quantify the residual variance, we repeat the full pipeline
                                                                    portability of the two-stage decomposition beyond the C/C++
three times on the three representative libraries (Table VII).
                                                                    setting we studied here.
Compilation and execution success rates are highly stable, while
line and branch coverage vary by only a few percentage points                             VII. R ELATED W ORK
(standard deviation ≤ 3.5), far smaller than L ISA’s margin A. Automated Software Testing for Libraries
over the baselines; in every run L ISA exceeds the Vanilla
baseline on all three libraries and its ranking against OSS-Fuzz          a) Library fuzzing: Library fuzzing typically uses
is unchanged. Bug detection is likewise stable (Table VII, last     LLVM’s    libFuzzer [4], for which developers write fuzz drivers
column): all but one of the detected bugs recurs in every run.      that  parse  inputs and invoke APIs; OSS-Fuzz [7] maintains
The main tables report one representative run from this set.        such  drivers  for over 1000 projects. As writing drivers requires
                                                                    expert knowledge of library semantics, recent work automates
      c) Hyperparameter Settings: The choice of hyperparame- their generation [26, 42, 63]: Hopper [42] models API calls
ters, such as the value of n in n-gram and the repair attempt with a lightweight interpreter and grammar to explore valid
limit (5), along with the selected LLM, relies on preliminary API compositions (API sequences in this paper), and P ROMPT-
tuning and prior studies. We acknowledge that these settings F UZZ [26] prompts an LLM to generate fuzz drivers, iteratively
may not be optimal. However, to mitigate bias, we maintained mutating the API combinations under coverage feedback to
fixed configurations across all comparative methods. Future reach deep implementation bugs.
work could investigate automated hyperparameter optimization              b) Automated unit testing: Heuristic-based unit test gen-
or sensitivity analysis to better understand their impact on eration has been studied for decades but targets mainly object-
L ISA’s performance.                                                oriented software (Java, C#), generalizing poorly to C/C++
      d) Final oracle verification and documentation coverage: because it focuses on object internal state rather than library-
Although L ISA uses invariants and iterative repair to mitigate level API interactions [12, 13]. R ANDOOP [12] mutates method-
the oracle problem, final verification still requires human call sequences and checks language-level oracle properties,
inspection. In particular, a failing assertion may indicate either while µTEST and EvoSuite generate finer-grained oracles via
a genuine implementation defect or a misinterpretation of mutation analysis; however, the injected artificial bugs are
the specification by the LLM. By design, L ISA’s chunk- often unrealistic [15, 16], leaving these heuristics with low
invariant reasoning and verification-and-repair loop produce maintainability and usability [15].
high-confidence assertions; nevertheless, residual false positives
cannot be fully eliminated. A second, orthogonal limit is recall: B. LLM-Based Unit Test Generation
L ISA can only assert what documentation (plus filtered Daikon         To overcome the limitations of heuristic-based unit test
candidates) makes explicit, so conventional-but-undocumented generation, recent studies have proposed using the code under
contracts that experienced developers take for granted yield test as prompts to LLMs to automatically generate unit
no invariant, and L ISA can miss bugs that violate only such tests [16–19, 21, 38, 64, 65]. This line of work has evolved from
unwritten conventions. Grounding invariants in documentation generating only assertions [21, 64, 65] to producing complete
is a deliberate trade-off, keeping them semantically valid and test functions and even full test files [16–19].
low-noise at the cost of leaving undocumented intent to future         Several benchmarks have been proposed to evaluate LLM-
work on mining usage patterns and existing test suites. More based software testing [22, 66, 67]. TestEval [66] and SWT-
broadly, the test oracle problem remains a fundamental open Bench [67] focus on generating single test functions, whereas
challenge in software testing [25], and resolving it more fully TestGenEval [22] evaluates the generation of complete test
is an important direction for future work.                          suites, similar to EvoSuite. SWT-Bench measures bug detection
capability by generating tests for bug-fixing pull requests (PRs), it borrows, but this decomposition, separating reachability
where the generated tests should fail before the PR is merged (sequence synthesis) from oracle construction, guiding the
and pass afterward. TestGenEval incorporates mutation score former with n-gram API-combination coverage and grounding
to assess whether the generated tests can detect behavioral the latter in documentation-derived chunk invariants, which no
changes in the code. However, no existing benchmark provides prior approach provides.
a ground-truth oracle for test generation, which is necessary
                                                                                              VIII. C ONCLUSION
for evaluating whether generated tests can detect real-world
functional bugs in the current versions of software libraries.         We presented L ISA, a novel LLM-based unit testing frame-
Moreover, all existing benchmarks support only Python, while work for detecting functional bugs in software libraries. By
more widely used languages in the software supply chain, such decoupling API-sequence exploration from invariant construc-
as C and C++, remain largely neglected.                            tion in unit tests, L ISA leverages n-gram API-combination
                                                                   coverage feedback and chunk-invariant reasoning to generate
C. Invariant Generation                                            diverse and semantically meaningful test functions. Across 7
   Program invariant generation methods can be broadly cate- C/C++ libraries, it attains higher average branch coverage than
gorized into dynamic execution-based [34], search-based [68], OSS-Fuzz, and on 25 historical functional bugs it detects 12
and learning-based approaches [8, 27, 68]. Execution-based (48%), versus 3 for CITYWALK and 2 for OSS-Fuzz. Its
methods, such as Daikon [34], capture invariants of the current novelty lies in this decomposition rather than in any single
version of the software and are therefore better suited for borrowed component, and it mitigates rather than solves the
generating regression tests rather than detecting functional bugs. oracle problem, emitting high-confidence bug candidates for
LLM-based approaches, such as SmartInv [8], infer invariants developer confirmation.
that should hold according to the developer’s intent by                                      DATA AVAILABILITY
reasoning over both source code semantics and corresponding
natural language descriptions [69]. Such invariants can be             Our artifacts and source code to reproduce the data are
used to detect functional bugs in software libraries. L ISA is a   available     at [70] and on GitHub.1 This public digital repository
generic framework capable of integrating any style of invariant includes: (1) the L ISA implementation and prompts, (2) the full
generation method based on user preference, supporting both list of the 25 re-introduced historical bugs (IDs, links, and cor-
regression testing with Daikon and functional bug detection responding patches/commits), (3) the generated test programs
using LLM-based invariant generalization. L ISA reconciles the for the bugs found by L ISA, (4) all scripts/configurations used
two lines: Daikon supplies candidate relations that L ISA filters for coverage measurement and reporting, and (5) the rationale
against documentation, while the LLM supplies intent-level and sensitivity data for choosing the n-gram parameter N .
contracts from the same documentation, checked in turn against                                    R EFERENCES
the reference build. Neither source alone flags functional bugs,
                                                                     [1] N.E. Fenton and N. Ohlsson. “Quantitative analysis of
but their documentation-grounded reconciliation does.
                                                                             faults and failures in a complex software system”. In:
D. Positioning of L ISA                                                      IEEE    Transactions on Software Engineering 26.8 (2000),
                                                                             pp. 797–814.
   L ISA shares individual building blocks with prior work, but
                                                                     [2] Andy Chou et al. “An empirical study of operating
its contribution lies in how it decomposes functional-bug detec-
                                                                             systems errors”. In: SIGOPS Oper. Syst. Rev. 35.5 (Oct.
tion rather than in any single component. P ROMPT F UZZ [26]
                                                                             2001), pp. 73–88.
generates fuzz drivers for crash detection and steers exploration
                                                                     [3] Hao-Nan Zhu et al. From Bugs to Benchmarks: A
by mutating API combinations under code-coverage feedback;
                                                                             Comprehensive Survey of Software Defect Datasets. 2025.
L ISA instead synthesizes API sequences (not drivers), targets
                                                                             arXiv: 2504.17977 [cs.SE].
functional bugs, steers exploration with a new n-gram API-
                                                                     [4] Kosta Serebryany. “Continuous Fuzzing with libFuzzer
combination coverage (Section III-E), and supplies the invariant
                                                                             and AddressSanitizer”. In: 2016 IEEE Cybersecurity
oracle that P ROMPT F UZZ lacks, reusing only P ROMPT F UZZ’s
                                                                             Development (SecDev). 2016, pp. 157–157.
front-end API extraction, not its fuzzing loop. SmartInv [8]
                                                                     [5] Andrea Fioraldi et al. “AFL++ combining incremental
infers invariants for smart contracts from code and intent;
                                                                             steps of fuzzing research”. In: Proceedings of the 14th
L ISA instead targets C/C++ library APIs, derives invariants
                                                                             USENIX Conference on Offensive Technologies. 2020,
from API documentation as executable test oracles, and,
                                                                             pp. 10–10.
unlike monolithic inference, decouples oracle construction from
                                                                     [6] Marcel Böhme et al. “Directed Greybox Fuzzing”. In:
sequence generation, inserting invariants incrementally at chunk
                                                                             Proceedings of the 2017 ACM SIGSAC Conference on
boundaries under a verify-and-repair loop (Section III-G2).
                                                                             Computer and Communications Security. CCS ’17. Dal-
LLM-UT methods such as CITYWALK [19] follow a one-
                                                                             las, Texas, USA: Association for Computing Machinery,
test-per-method scheme whose oracles are frequently trivial
                                                                             2017, pp. 2329–2344.
(e.g., assert(ptr != NULL)) and cannot construct the
multi-step API sequences required to reach stateful functional        1 https://github.com/SecurityLab-UCD/CNTG  and https://github.com/
bugs. The novelty of L ISA is therefore not any single technique   SecurityLab-UCD/CGNTG
 [7]   Kostya Serebryany. “OSS-Fuzz - Google’s continuous          [19] Yuwei Zhang et al. “CITYWALK: Enhancing LLM-
       fuzzing service for open source software”. In: Vancouver,        Based C++ Unit Test Generation via Project-Dependency
       BC: USENIX Association, Aug. 2017.                               Awareness and Language-Specific Knowledge”. In: ACM
 [8]   Sally Junsong Wang, Kexin Pei, and Junfeng Yang.                 Trans. Softw. Eng. Methodol. (Aug. 2025). Just Accepted.
       “ SmartInv: Multimodal Learning for Smart Contract          [20] Chunqiu Steven Xia et al. “Demystifying LLM-Based
       Invariant Inference”. In: 2024 IEEE Symposium on                 Software Engineering Agents”. In: Proc. ACM Softw.
       Security and Privacy (SP). Los Alamitos, CA, USA:                Eng. 2.FSE (June 2025).
       IEEE Computer Society, May 2024, pp. 2217–2235.             [21] Pengyu Nie et al. “Learning Deep Semantics for Test
 [9]   Vladimir Khorikov. Unit Testing Principles, Practices,           Completion”. In: Proceedings of the 45th International
       and Patterns. Simon and Schuster, 2020.                          Conference on Software Engineering. ICSE ’23. Mel-
[10]   Yangyang Zhao et al. “The impact of continuous                   bourne, Victoria, Australia: IEEE Press, 2023, pp. 2111–
       integration on other software development practices: A           2123.
       large-scale empirical study”. In: 2017 32nd IEEE/ACM        [22] Kush Jain, Gabriel Synnaeve, and Baptiste Roziere.
       International Conference on Automated Software Engi-             “TestGenEval: A Real World Unit Test Generation
       neering (ASE). 2017.                                             and Test Completion Benchmark”. In: The Thirteenth
[11]   Moritz Beller et al. “When, How, and Why Developers              International Conference on Learning Representations.
       (Do Not) Test in Their IDEs”. In: Proceedings of the             2025.
       2015 10th Joint Meeting on Foundations of Software En-      [23] William E. Howden. “Theoretical and Empirical Studies
       gineering. ESEC/FSE 2015. Bergamo, Italy: Association            of Program Testing”. In: Proceedings of the 3rd Inter-
       for Computing Machinery, 2015, pp. 179–190.                      national Conference on Software Engineering (ICSE).
[12]   Carlos Pacheco et al. “Feedback-Directed Random                  ICSE ’78. Atlanta, Georgia, USA: IEEE Press, 1978,
       Test Generation”. In: 29th International Conference on           pp. 305–311.
       Software Engineering (ICSE’07). 2007, pp. 75–84.            [24] Elaine J. Weyuker. “On Testing Non-testable Programs”.
[13]   Gordon Fraser and Andrea Arcuri. “EvoSuite: automatic            In: The Computer Journal 25.4 (1982), pp. 465–470.
       test suite generation for object-oriented software”. In:    [25] Earl T. Barr et al. “The Oracle Problem in Software
       Proceedings of the 19th ACM SIGSOFT Symposium                    Testing: A Survey”. In: IEEE Transactions on Software
       and the 13th European Conference on Foundations of               Engineering 41.5 (2015), pp. 507–525.
       Software Engineering. ESEC/FSE ’11. Szeged, Hungary:        [26] Yunlong Lyu et al. “Prompt Fuzzing for Fuzz Driver
       Association for Computing Machinery, 2011, pp. 416–              Generation”. In: Proceedings of the 2024 on ACM
       419.                                                             SIGSAC Conference on Computer and Communications
[14]   Sina Shamshiri et al. “How Do Automatically Generated            Security. CCS ’24. Salt Lake City, UT, USA: Association
       Unit Tests Influence Software Maintenance?” In: 2018             for Computing Machinery, 2024, pp. 3793–3807.
       IEEE 11th International Conference on Software Testing,     [27] Kexin Pei et al. “Can Large Language Models Reason
       Verification and Validation (ICST). 2018, pp. 250–261.           about Program Invariants?” In: Proceedings of the 40th
[15]   Annibale Panichella et al. “Revisiting test smells in            International Conference on Machine Learning. Vol. 202.
       automatically generated tests: limitations, pitfalls, and        Proceedings of Machine Learning Research. PMLR, 23–
       opportunities”. In: 2020 IEEE international conference           29 Jul 2023, pp. 27496–27520.
       on software maintenance and evolution (ICSME). IEEE.        [28] Al Bessey et al. “A Few Billion Lines of Code Later:
       2020, pp. 523–533.                                               Using Static Analysis to Find Bugs in the Real World”.
[16]   Nikitha Rao et al. “CAT-LM Training Language Models              In: Communications of the ACM 53.2 (2010), pp. 66–75.
       on Aligned Code and Tests”. In: Proceedings of the 38th     [29] Cristian Cadar, Daniel Dunbar, and Dawson R. Engler.
       IEEE/ACM International Conference on Automated Soft-             “KLEE: Unassisted and Automatic Generation of High-
       ware Engineering. ASE ’23. Echternach, Luxembourg:               Coverage Tests for Complex Systems Programs”. In: 8th
       IEEE Press, 2024, pp. 409–420.                                   USENIX Symposium on Operating Systems Design and
[17]   Yifeng He et al. “UniTSyn: A Large-Scale Dataset Capa-           Implementation (OSDI). 2008, pp. 209–224.
       ble of Enhancing the Prowess of Large Language Models       [30] K. Rustan M. Leino. “Dafny: An Automatic Program
       for Program Testing”. In: Proceedings of the 33rd ACM            Verifier for Functional Correctness”. In: 16th Interna-
       SIGSOFT International Symposium on Software Testing              tional Conference on Logic for Programming, Artificial
       and Analysis. ISSTA 2024. Vienna, Austria: Association           Intelligence, and Reasoning (LPAR). Springer, 2010,
       for Computing Machinery, 2024, pp. 1061–1072.                    pp. 348–370.
[18]   Yifeng He et al. “FuzzAug: Data Augmentation by             [31] Koen Claessen and John Hughes. “QuickCheck: A
       Coverage-guided Fuzzing for Neural Test Generation”.             Lightweight Tool for Random Testing of Haskell Pro-
       In: Findings of the Association for Computational Lin-           grams”. In: 5th ACM SIGPLAN International Confer-
       guistics: EMNLP 2025. Suzhou, China: Association for             ence on Functional Programming (ICFP). ACM, 2000,
       Computational Linguistics, Nov. 2025, pp. 15642–15655.           pp. 268–279.
[32] Leonidas Lampropoulos, Michael Hicks, and Benjamin               Association for Computational Linguistics 12 (2024),
     C. Pierce. “Coverage Guided, Property Based Testing”.            pp. 157–173.
     In: Proceedings of the ACM on Programming Languages       [46]   Jonathan Metzman et al. “FuzzBench: an open fuzzer
     (OOPSLA) 3 (2019), pp. 1–29.                                     benchmarking platform and service”. In: Proceedings
[33] The LLVM Compiler Infrastructure. https://github.com/            of the 29th ACM Joint Meeting on European Software
     llvm/llvm-project, accessed 2025-10-12.                          Engineering Conference and Symposium on the Founda-
[34] M.D. Ernst et al. “Dynamically discovering likely                tions of Software Engineering. ESEC/FSE 2021. Athens,
     program invariants to support program evolution”. In:            Greece: Association for Computing Machinery, 2021,
     IEEE Transactions on Software Engineering 27.2 (2001),           pp. 1393–1403.
     pp. 99–123.                                               [47]   John Yang et al. “SWE-agent: Agent-Computer Inter-
[35] Chris Lattner and Vikram Adve. “LLVM: A Com-                     faces Enable Automated Software Engineering”. In:
     pilation Framework for Lifelong Program Analysis                 Advances in Neural Information Processing Systems
     & Transformation”. In: International Symposium on                (NeurIPS). 2024.
     Code Generation and Optimization (CGO). IEEE, 2004,       [48]   Xingyao Wang et al. “OpenHands: An Open Platform
     pp. 75–86.                                                       for AI Software Developers as Generalist Agents”. In:
[36] Edsger W. Dijkstra. “Notes on Structured Programming”.           The Thirteenth International Conference on Learning
     In: Structured Programming. Academic Press, 1972,                Representations (ICLR). 2025.
     pp. 1–82.                                                 [49]   Zifan Nan et al. “Test Intention Guided LLM-based Unit
[37] André L. Santos et al. “Stepwise API usage assistance            Test Generation”. In: Proceedings of the IEEE/ACM
     using n-gram language models”. In: Journal of Systems            47th International Conference on Software Engineering
     and Software 131 (2017), pp. 461–474.                            (ICSE). 2025.
[38] Gabriel Ryan et al. “Code-Aware Prompting: A Study of     [50]   Carlos E. Jimenez et al. “SWE-bench: Can Language
     Coverage-Guided Test Generation in Regression Setting            Models Resolve Real-World GitHub Issues?” In: The
     using LLM”. In: Proc. ACM Softw. Eng. 1.FSE (July                Twelfth International Conference on Learning Represen-
     2024).                                                           tations (ICLR). 2024.
[39] Xingchen Wan et al. “Better Zero-Shot Reasoning with      [51]   Ahmad Hazimeh, Adrian Herrera, and Mathias Payer.
     Self-Adaptive Prompting”. In: Findings of the Associa-           “Magma: A Ground-Truth Fuzzing Benchmark”. In:
     tion for Computational Linguistics: ACL 2023. Toronto,           vol. 4. 3. New York, NY, USA: Association for Com-
     Canada: Association for Computational Linguistics, July          puting Machinery, Nov. 2020.
     2023, pp. 3493–3514.                                      [52]   Jean-loup Gailly and Mark Adler. ZLIB DATA COM-
[40] Noah Shinn et al. “Reflexion: language agents with               PRESSION LIBRARY. https://zlib.net/. 2025.
     verbal reinforcement learning”. In: Thirty-seventh Con-   [53]   PNG Development Group. LIBPNG: Portable Network
     ference on Neural Information Processing Systems. 2023.          Graphics Reference Library. https : / / github . com /
[41] Jicheng Wang, Yifeng He, and Hao Chen. RepoGen-                  pnggroup/libpng. 2025.
     Reflex: Enhancing Repository-Level Code Completion        [54]   The Tcpdump Group. libpcap: Portable Packet Capture
     with Verbal Reinforcement and Retrieval-Augmented                Library. https://github.com/the-tcpdump-group/libpcap.
     Generation. 2024. arXiv: 2409.13122 [cs.SE].                     2025.
[42] Peng Chen et al. “Hopper: Interpretative Fuzzing for      [55]   SQLite Development Team. SQLite. https://github.com/
     Libraries”. In: Proceedings of the 2023 ACM SIGSAC               sqlite/sqlite. 2025.
     Conference on Computer and Communications Secu-           [56]   Marti Maria. Little CMS: A Free Color Management
     rity. CCS ’23. Copenhagen, Denmark: Association for              Engine. https://github.com/mm2/Little-CMS. 2025.
     Computing Machinery, 2023, pp. 1600–1614.                 [57]   Dave Gamble. cJSON: Ultralightweight JSON Parser in
[43] Michael D. Ernst et al. “Quickly detecting relevant              ANSI C. https://github.com/DaveGamble/cJSON. 2025.
     program invariants”. In: Proceedings of the 22nd Inter-   [58]   Google team. RE2: Efficient Regular Expression Match-
     national Conference on Software Engineering. ICSE ’00.           ing. https://github.com/google/re2. 2025.
     Limerick, Ireland: Association for Computing Machinery,   [59]   Max Schäfer et al. “An Empirical Evaluation of Using
     2000, pp. 449–458.                                               Large Language Models for Automated Unit Test Gener-
[44] Danning Xie et al. “DocTer: documentation-guided                 ation”. In: IEEE Transactions on Software Engineering
     fuzzing for testing deep learning API functions”. In:            50.1 (2024), pp. 85–105.
     Proceedings of the 31st ACM SIGSOFT International         [60]   Runlin Liu et al. LLM-based Unit Test Generation for
     Symposium on Software Testing and Analysis. ISSTA                Dynamically-Typed Programs. 2025. arXiv: 2503.14000
     2022. Virtual, South Korea: Association for Computing            [cs.SE].
     Machinery, 2022, pp. 176–188.                             [61]   J. H. Andrews, L. C. Briand, and Y. Labiche. “Is
[45] Nelson F. Liu et al. “Lost in the Middle: How Language           mutation an appropriate tool for testing experiments?”
     Models Use Long Contexts”. In: Transactions of the               In: Proceedings of the 27th International Conference
                                                                      on Software Engineering. ICSE ’05. St. Louis, MO,
       USA: Association for Computing Machinery, 2005,
       pp. 402–411.
[62]   Mike Papadakis et al. “Are Mutation Scores Correlated
       with Real Fault Detection? A Large Scale Empiri-
       cal Study on the Relationship Between Mutants and
       Real Faults”. In: 2018 IEEE/ACM 40th International
       Conference on Software Engineering (ICSE). 2018,
       pp. 537–548.
[63]   Hongxiang Zhang et al. “LLAMAFUZZ: Large
       Language Model Enhanced Greybox Fuzzing”. In:
       ACM/IEEE International Conference on Automation of
       Software Test (AST). 2026.
[64]   Cody Watson et al. “On learning meaningful assert
       statements for unit test cases”. In: Proceedings of the
       ACM/IEEE 42nd International Conference on Software
       Engineering. ICSE ’20. Seoul, South Korea: Association
       for Computing Machinery, 2020, pp. 1398–1409.
[65]   Elizabeth Dinella et al. “TOGA: A Neural Method for
       Test Oracle Generation”. In: Proceedings of the 44th
       International Conference on Software Engineering. ICSE
       ’22. Pittsburgh, Pennsylvania: Association for Computing
       Machinery, 2022, pp. 2130–2141.
[66]   Wenhan Wang et al. “TestEval: Benchmarking Large
       Language Models for Test Case Generation”. In: Find-
       ings of the Association for Computational Linguistics:
       NAACL 2025. Albuquerque, New Mexico: Association
       for Computational Linguistics, Apr. 2025, pp. 3547–
       3562.
[67]   Niels Mündler et al. “SWT-Bench: Testing and Vali-
       dating Real-World Bug-Fixes with Code Agents”. In:
       Advances in Neural Information Processing Systems.
       Vol. 37. Curran Associates, Inc., 2024, pp. 81857–81887.
[68]   Xujie Si et al. “Code2Inv: A Deep Learning Frame-
       work for Program Verification”. In: Computer Aided
       Verification: 32nd International Conference, CAV 2020,
       Los Angeles, CA, USA, July 21–24, 2020, Proceedings,
       Part II. Los Angeles, CA, USA: Springer-Verlag, 2020,
       pp. 151–164.
[69]   Yifeng He et al. “Evaluating Program Semantics Rea-
       soning with Type Inference in System $F$”. In: The
       Thirty-ninth Annual Conference on Neural Information
       Processing Systems Datasets and Benchmarks Track.
       2025.
[70]   Ruogu Yang et al. Lisa Artifacts. Zenodo, https://doi.
       org/10.5281/zenodo.20839021. Jan. 2026.
                              A PPENDIX A                                          We conclude that any strictly monotone increasing concave
                          P ROMPT T EMPLATES                                       function with left-endpoint preserved compresses the range of
                                                                                   input values.
   Your task is to write a complete, logically correct C++ function named “int     Proof that power condense is a condense transformation.
   test_{project}_api_sequence()” using the {project} library.
   The API sequence should focus on the usage of the {project} library, and        We prove that power condense is a condense transformation.
   several essential aspects of the library are provided below. {headers} {APIs}
   {context}
                                                                                   We write the power condense C(a) = Ê(a)α as f (x) = xα
   Please use the following API functions in your function {combinations}          for α ∈ (0, 1) for simplification.
   Here is a successful example function: {successful_example}
   Below is basic function requirements: {Function Requirements} and project’s     • Strictly monotone increasing: We take the first derivative of
   specific rules:{project_rules}                                                    f with respect to x,
   Code Quality Rules:
   • The API sequence should follow a realistic and complete usage pattern:
                                                                                                                     dxα
      – Initialize → Configure → Operate → Validate → Cleanup                                            f ′ (x) =       = αxα−1 .
   • Ensure data flows meaningfully between API calls (no dummy or unused                                             dx
      variables).
   • Do not use placeholders like ‘// your code here’.                               Since α > 0, f ′ (x) > 0 for all x > 0. Thus, f is strictly
   • If you have to write any helper functions, begin them with static
   • Only output the function body ‘int test_{project}_api_sequence()’ { ... }’      monotone increasing.
   Example output:                                                                 • Strictly concave: For concavity, we take the second derivative
   int test_{project}_api_sequence() {
   // Step 1: Initializations                                                        of f with respect to x,
   // Step ...
   // Step ... : Cleanup                                                                                 d2 xα   dαxα−1
   return 66;                                                                               f ′′ (x) =       2
                                                                                                               =        = α(α − 1)xα−2 .
   }                                                                                                      dx       dx
                                                                                     Since α ∈ (0, 1), we have α − 1 < 0, thus f ′′ (x) < 0 for
Fig. 5: The structured prompt template employed in our                               all x > 0. Therefore, we conclude that f is strictly concave.
                                                                                                                                  α
                                                                                   • Left-endpoint preserved: We have f (0) = 0 = 0.
framework. Dynamic fields are denoted by brackets.
                                                                                   Thus, we conclude that power condense satisfies Definition III.1.

   The previous attempt to generate code failed with the following error:
   Error code:{error_code}                                                         B. Choice of Maximum Condensation Factor
   Error Type: {error_type}                                                           In this section, we illustrate how we choose the maximum
   Error Details:{error_details}
   Please regenerate a new program to repair the error without changing            condensation factor αmin in Equation 4. Let x, y ∈ I be the
   the logic, do not redefine main function and any other parameters               energies of two API functions such that x < y, then their
   even if the error is not defined, and do not change the function name.          relative ratio after power condense is given by
   If error type is execution error without error details, you can regard
   it as Segmentation fault (core dumped).                                                                      yα     y α
   Do not include if branches or loops; the function should be a straight-                                R= α =             .
   line sequence of API calls.                                                                                  x       x
                                                                                   Let us consider the extreme case after normalization, where
                                                                                   x = ε and y = 1, so y/x = 1/ε = 100. Since R = (y/x)α
Fig. 6: The structured repair prompt template for correcting
                                                                                   is increasing in α, the strongest condensation (α = αmin )
erroneous API sequences. Dynamic fields are denoted by
                                                                                   yields the smallest selection ratio between the highest- and
brackets.
                                                                                   lowest-energy API function:
                                                                                                                  αmin
                        A PPENDIX B                                                                                1
                                                                                                        Rαmin =            .
            D ETAILS OF API N-G RAM F EEDBACK                                                                      ε
A. Proofs of Condense Transformation                           We choose αmin so that, even under this strongest condensation,
Proof of Proposition 1. Let x, y ∈ I such that 0 < x < y ≤ 1. the highest-energy API function stays a useful factor more
Let λ = x/y ∈ (0, 1), then x = λy + (1 − λ) · 0. By strict likely to be selected than the lowest-energy one, preventing
concavity,                                                     over-condensation. For example, to keep that factor at 10×,
                                                                                             αmin
λf (y) = λf (y) + (1 − λ)f (0) < f (λy + (1 − λ) · 0) = f (x).                                1
                                                                                   Rαmin =              = 10,
Rearranging the above inequality gives                                                        ε
                                                                            
                                                                            1                               log(10)
                             f (x)    y            f (y)    y     αmin log      = log(10) =⇒ αmin =                 = 0.5.
λf (y) < f (x) =⇒ f (y) <          = f (x) =⇒            < .                ε                              log(1/ε)
                               λ      x            f (x)    x
Since f is strictly monotone increasing, we have 0 < f (x) <      Through this feedback loop, the API energy distribution
f (y), thus                                                    dynamically  evolves based on the success and novelty of
                            f (y)   y                          generated 3-grams, enabling the model to balance correctness
                       1<         < .                          reinforcement with exploratory diversity.
                            f (x)   x
                      A PPENDIX C                                   group of senior software researchers and library maintainers.
            D ESIGN AND M EASUREMENT N OTES                         Disagreements were resolved through discussion to reach a
A. Comparison with H OPPER                                          consensus.
   L ISA builds on Hopper’s [42] distinction between Intra-API B. HBDR vs. Mutation Score
(argument validity) and Inter-API (call dependencies). L ISA’s         While mutation score is a widely adopted metric in evaluating
advantage lies in its “decoupling” strategy, which delegates unit test generation techniques [61], synthetic mutants may not
resolution of Inter-API constraints entirely to L ISAAPI . L ISAAPI fully represent the complexity of real-world software faults [62].
focuses on generating valid and high-quality API sequences We therefore prefer historical bug re-introduction as a more
(solving the “reachability” problem) through LLM reasoning faithful proxy for real-world fault detection.
and API n-gram feedback before invariant generation. This pro-
cess drastically reduces the search space complexity, allowing                                A PPENDIX E
the subsequent stage to concentrate entirely on verifying Intra-             API C ONTRACT D OCUMENTATION D ETAILS
API behaviors through invariants, thereby ensuring high-quality        We construct API contract documentation through two
assertions.                                                         complementary ways: dynamic analysis and natural-language
B. Straight-Line Execution Policy                                   documentation analysis.
                                                                          a) Invariants generated by Daikon: Daikon [43] is a
   We acknowledge that straight-line programs cannot explicitly
                                                                    dynamic analysis tool designed to detect likely invariants
encode branches. However, the library under test can still take
                                                                    in programs by observing their runtime behavior. It reports
different internal branches based on internal state, call order,
                                                                    properties that hold during the observed executions. However,
and implicit conditions, even when the generated driver itself
                                                                    the properties extracted from observed executions cannot be
is straight-line. This is an intentional trade-off to prioritize
                                                                    directly used to detect functional bugs, since they only capture
correctness and executability while still enabling substantial
                                                                    the snapshot of the current program development stage. Even
state evolution and control-flow coverage.
                                                                    more critically, if researchers mistakenly treat incorrect or
C. Measurement Setup                                                spurious properties as true invariants, correct code with correct
   For OSS-Fuzz, we used the official fuzzing harnesses from logic may be falsely flagged as buggy, leading to misleading
the OSS-Fuzz project for each library and did not modify them. or invalid conclusions. Nevertheless, if these Daikon-generated
All coverage metrics reported in the main text are measured invariants are further manually reviewed and validated, they
at the library level. That is, the coverage only reflects the can still serve as valuable references for understanding program
execution of the target library code, not the fuzzing harness or behavior and guiding subsequent analysis, such as refining test
the test driver. In our implementation, we used gpt-5-mini oracles or identifying potential correctness properties.
for the API sequence generation phase (L ISAAPI ), since this             b) Inferring Invariants From Documentation: In open-
phase focuses on fast, large-scale exploration of API sequences.    source   libraries, developers provide official documentation
We used gpt-5.1 for the invariant generation phase (L ISAinv ),     that describes   each API’s purpose, parameters, return values,
since this phase requires stronger reasoning to produce correct     and  expected   behavior. These expert-crafted manuals include
and meaningful invariants.                                          statements   such  as “this method is read-only” or “this API
                                                                    does not modify internal state”, thereby implicitly defining the
                          A PPENDIX D                               behavior invariants of the API. Because the documentation
    M ETRIC D EFINITIONS AND A NNOTATION P ROTOCOL                  already tells what the API does and what it guarantees, we
   This appendix supplements the metric definitions in Sec- leverage these descriptions to manually infer invariants (i.e.,
tion IV-C with the annotation protocols used for AUVC and properties that should always hold when the API is used
HBDR; the core L ISAAPI metrics (CSR, ESR, LC, BC) are correctly). For example, if the documentation states that an API
defined there.                                                      is read-only, then a concrete invariant in natural language might
                                                                    be “no internal state is modified”. Prior work [44] provides
A. AUVC Uniqueness Annotation Protocol                              evidence that leveraging documentation can effectively support
   Multiple invariant statements may be considered unique program analysis.
even if they query the same program state. For example,                Daikon captures empirical invariants based on runtime
repeated queries over the same zlib stream state following a behavior, while API documentation provides intended invariants
sequence of API operations are considered distinct. Conversely, that reflect the developer’s design. In practice, we first run
syntactically different invariants may be non-unique if they Daikon on automatically generated executable API sequences
express equivalent conditions (e.g., x >= 1 and x > 0 for to obtain candidate properties. We use a filtering step to keep
x ∈ Z). The uniqueness of verifications is determined through invariant candidates that match the official documentation
manual analysis by two authors with more than three years of and do not break the program when added as assertions.
C/C++ development experience, who independently inspected In our current method, checking if candidates match the
and categorized the generated invariants based on their semantic documentation requires only a small, one-time human check
meaning. Their results are discussed and confirmed by a per API. This step needs no training data or model tuning,
and the effort does not grow with the number of tests. This
combination improves both the accuracy and coverage of the
inferred invariants.
