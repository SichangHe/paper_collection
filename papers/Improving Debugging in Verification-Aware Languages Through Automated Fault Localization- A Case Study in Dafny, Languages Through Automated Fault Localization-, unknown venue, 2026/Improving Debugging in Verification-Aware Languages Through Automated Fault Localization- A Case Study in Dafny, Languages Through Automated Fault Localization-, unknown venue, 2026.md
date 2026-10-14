                                             Improving Debugging in Verification-Aware
                                          Languages Through Automated Fault Localization:
                                                      A Case Study in Dafny
                                                1st Álvaro Silva                     2nd Isabel Amaral            3rd João Pascoal Faria         4th Alexandra Mendes∗
                                             INESC TEC, Faculdade                 INESC TEC, Faculdade              INESC TEC, Faculdade           INESC TEC, Faculdade
                                                de Engenharia,                         de Engenharia,                  de Engenharia,                 de Engenharia,
                                              Universidade do Porto                Universidade do Porto             Universidade do Porto          Universidade do Porto
                                                 Porto, Portugal                       Porto, Portugal                  Porto, Portugal                Porto, Portugal
                                            amfpsilva@hotmail.com             isabel.andre.amaral@gmail.com              jpf@fe.up.pt           alexandra@archimendes.com
arXiv:2608.05399v3 [cs.SE] 31 Aug 2026




                                            Abstract—Verification-aware languages, like Dafny, integrate          (requires), postconditions (ensures), and invariants (invariant),
                                         formal specifications directly into source code to enable static         directly into code, allowing verifiers to automatically flag
                                         correctness checks. However, when verification fails, the feedback       specification violations. While this is helpful in warning de-
                                         provided is often limited to the specific condition of the error, such
                                         as a violated postcondition, rather than the root cause of the fault.    velopers that the implementation does not match the expected
                                         For example, in Dafny, while its counterexample features provide         behavior, it often does not indicate the source of the problem.
                                         concrete execution traces, they typically expose a single failing        In fact, a single failing verification condition may result from
                                         path per assertion failure, leaving the developer to manually            many possible fault locations, and the verifier feedback is
                                         inspect the entire trace to locate the error.                            often too coarse for debugging. This limitation is consistent
                                            This paper investigates automated fault localization for
                                         verification-aware languages by comparing two paradigms: state-          with findings from prior work, which identified poor error
                                         based and counterexample-based localization. Our state-based             messages and inadequate feedback as key challenges in the
                                         localization strategy replicates the “snapshot” methodology of           use of verification-aware languages, with users highlighting
                                         AutoFix by inferring invariants and predicates to identify               better debugging tools as an area for improvement [3]. Cur-
                                         suspicious program states. The counterexample-based strategy             rently, verifier feedback provides the violated condition and
                                         consists of a family of techniques that progressively enrich the
                                         use of verifier output: from raw counterexample extraction, to           one representative counterexample path, but not a ranked
                                         structured single-trace ranking, and to multi-trace aggregation.         explanation of which program lines are most likely responsible
                                            To validate these methods, we present an evaluation frame-            for the failure. As a result, developers are left to manually
                                         work that uses MutDafny to generate a diverse mutant dataset             identify the root cause of the problem among many potential
                                         from DafnyBench and measures localization effectiveness using            fault locations. This is especially problematic when multiple
                                         the EXAM score. Our results show that counterexample-based
                                         approaches substantially outperform state-based localization in          branches can satisfy the same failing proof obligation, because
                                         this setting. Structured ranking over a single trace yields the          the first model found by the solver may point to a branch that
                                         largest improvement over raw counterexample output, while                is not the most useful to find the bug.
                                         multi-trace aggregation provides additional gains in robustness             This work investigates automated fault localization (FL) for
                                         and debugging utility by increasing coverage and reducing
                                         path bias introduced by the solver. These findings demonstrate           verification-aware languages by comparing two paradigms:
                                         that effective fault localization in verification-aware languages          • State-based localization (SNAP): Based on an existing
                                         depends both on using counterexample information and on how
                                         that information is structured and diversified.
                                                                                                                      approach implemented in AutoFix [4] for Eiffel [5],
                                            Index Terms—Fault localization, verification-aware languages,             which represents suspicious program states as “snap-
                                         Dafny, counterexamples, design by contract                                   shots” (i.e., abstractions of a concrete property of the
                                                                                                                      program state at a concrete program location) and ranks
                                                              I. I NTRODUCTION                                        them using a combination of static and dynamic evidence.
                                            Software is embedded in all aspects of modern life, from                • Counterexample localization: We evaluate a family of
                                         smartphones to medical devices, making software correctness                  counterexample-based localization techniques with in-
                                         more critical than ever. Yet, writing software free of bugs                  creasing capabilities. These include raw baseline extrac-
                                         remains challenging, and locating the root cause of a bug is                 tion (CNTB), single-trace structured ranking (CNTS),
                                         often an arduous and time-consuming part of debugging.                       and, our primary contribution, a multi-trace aggregation
                                            Verification-aware languages, such as Dafny [1] and                       via iterative path blocking (CNTM).
                                         Verus [2], embed logical constructs, including preconditions
                                                                                                                    We additionally evaluate an LLM-based approach. However,
                                           ∗ Author order follows a senior-author-last convention.                because LLMs are neither deterministic nor verifier-native, this
approach is included only as a baseline for comparison.                 SNAP is a dynamic analysis technique, relying on program
   A key challenge in our comparison is the architectural shift      executions to gather evidence about suspicious program states.
from dynamic to static verification. AutoFix was originally          This analysis is centered on the faulty method, defined as the
designed for Eiffel, where contracts are dynamically checked         method where Dafny’s verifier reports a specification violation.
during program execution. In contrast, Dafny failures manifest       AutoFix was designed for programs with single faults, so if
as unsatisfied proof obligations during static analysis.             the verifier flags multiple violations, SNAP handles only the
   We formalize the fault localization problem in verification-      first. Extending this approach to iteratively handle multiple
aware languages by treating any program that fails to verify as      violations is feasible but left as future work.
containing an implementation fault, i.e., a defect in executable        This approach investigates the possible causes of program
code that violates a correct specification. While specification      faults by building an abstraction of the program state based
errors (e.g., weak postconditions) are common, this study            on boolean predicates collected from multiple sources. Each of
isolates faults at the implementation level, allowing for a          these boolean predicates creates a snapshot, an abstraction of
controlled evaluation with precise ground truth. Each fault          a concrete property of the program state at a concrete program
localization strategy considered in this paper takes as input        location. Each snapshot is assigned a suspiciousness score
a faulty program and produces a ranking of the lines in that         derived from a combination of static and dynamic analysis
program according to suspiciousness, i.e., from the most to          features. The ranking of program lines produced by the
least likely to contain the fault causing the specification vio-     strategy is projected from the snapshot ranking, considering
lation. We evaluate the core techniques with a mutation-based        the program location associated with each snapshot.
framework built on DafnyBench [6] using MutDafny [7].                   While most fault localization techniques that compute sus-
Contributions. The main contributions of this paper are:             piciousness scores do so at the program statement level, SNAP
   • A unified framework for systematic evaluation of fault
                                                                     analyzes specific program states. This finer level of fault
     localization approaches in verification-aware languages.        localization granularity provides more precise guidance for a
   • SNAP: A state-based ranker adapted from the AutoFix
                                                                     future fix generation process. Its goal is to, given one of the
     approach that uses inferred predicates and snapshots for        top-ranked snapshots, attempt to avoid the state it abstracts.
     fault localization.                                             A. Formal Model of Snapshots
   • CNTM: A multi-trace ranker that aggregates evi-
                                                                        Let B be the collection of boolean predicates abstracting
     dence across multiple diverse counterexamples generated
                                                                     the program state, each predicate p ∈ B is evaluated at each
     through iterative path blocking.
                                                                     location l of the program where it is visible, resulting in a
   • A structural ranking heuristic that prioritizes nesting
                                                                     snapshot, i.e., a triple ⟨l, p, v⟩, where v is a boolean value.
     depth and control-flow to isolate root causes from inci-
                                                                        Each snapshot abstracts a program execution in which p
     dental execution steps.
                                                                     evaluates to v at location l. A snapshot with a high suspi-
   • An empirical study characterizing trade-offs between
                                                                     ciousness score indicates there is a high probability of the
     symbolic techniques and LLMs, identifying structural
                                                                     fault being due to predicate p taking value v at location l.
     awareness as a key driver for search efficiency.
                                                                     B. Test Cases
    II. S NAPSHOT S TATE -BASED FAULT L OCALIZATION
                                                                        AutoFix relies on both contracts and tests automatically
   We first present SNAP, a state-based approach that ranks
                                                                     generated from the contracts as the repair oracle. There is con-
program locations by identifying suspicious program states
                                                                     siderable research on test generation from specifications [8]–
through the construction of a program state abstraction. SNAP
                                                                     [11]. Eiffel benefits from its own specification-based test
is a Dafny adaptation of AutoFix’s fault localization approach,
                                                                     generation tool, AutoTest [12], which automatically selects
originally proposed for Eiffel and the first designed specifically
                                                                     inputs for the program constructs under test and determines
for verification-aware languages.
   Both languages are grounded in Design by Contract (DbC),          their success or failure by observing whether they satisfy their
but while Eiffel is a pure Object-Oriented (OO) programming          contracts when executed with those inputs. However, no such
language, Dafny has a more imperative character, where OO            approach exists in Dafny, which poses a challenge to the
features are available but not the most commonly used ones.          replication of this fault localization approach.
This distinction is significant because part of AutoFix’s proce-        Dafny itself provides a beta version of a counterexample-
dure for building a program abstraction uses the OO structure.       based test generation command under development1 , resulting
Additionally, Eiffel supports DbC as a runtime mechanism,            from the integration of the work developed first in Delfy [13],
whereas Dafny statically verifies contracts before execution,        [14] and subsequently in DTest [15]. However, this tool is
so feedback regarding contract violations will differ in nature.     insufficient for our needs because it does not support some
The fundamental differences between the two languages mean           of Dafny’s key features, such as arrays, and it only generates
that the same approach may yield different results. Studying         one test case per program path. Our approach requires a broad
these differences is therefore an important foundational step,       and diverse test suite for detecting faulty execution patterns.
establishing a baseline for further research on fault localization     1 https://dafny.org/dafny/DafnyRef/DafnyRef#sec-dafny-generate-tests, ac-
techniques for verification-aware languages.                         cessed Aug. 2026.
Additionally, although it is guided by the specification, it         of different program variables at different program locations.
generates tests based on the implementation’s structure rather       In turn, likely means that the invariants are statistically likely
than independently from it, thus failing to distinguish between      to be true based on a group of observed executions. For
correct and incorrect implementation behavior.                       some programming languages, Daikon provides frontends that
   To address this gap, we developed DafnyCBT, a contract-           automatically produce trace files from a program equipped
based test generator that derives both inputs and expected out-      with test cases. For the remaining languages, including Dafny,
puts from contracts, independently of the implementation. This       a custom frontend2 which converts execution data into a format
ensures that tests fail whenever the implementation deviates         that Daikon can process, must be provided.
from its contract, and that specified behavior unreached by             Our frontend was implemented by instrumenting the input
the code is still exercised.                                         Dafny program with print statements. This way, running it and
   Test generation has two stages. First, the contract is de-        redirecting the output to a file produces a trace file ready to be
composed into Disjunctive Normal Form (DNF) using impli-             fed into Daikon. The first step is to print a header3 consisting
cation splitting that is safe under short-circuit evaluation, with   of program point declarations, i.e., the points of the program
each clause representing an input/output equivalence class.          at which we want Daikon to perform invariant inference.
Z3 solves each satisfiable clause for concrete inputs and,           In our case, these correspond to the faulty method’s entry,
where feasible, expected outputs. A uniqueness probe emits           exit, and every position between statements4 . Each program
either a concrete pin expect result==v, a disjunctive pin            point declaration contains a list of variable declarations for
over a small enumerated set, or the postcondition literals as        the variables visible at that program location, which we
runtime expect assertions. Then, boundary value analysis             identify by analyzing the program prior to its instrumentation.
targets collection sizes (e.g., |a|∈ {0, 1, ≥2}) and numeric         The program traces are expressed after this initial block of
extremes from relational literals, covering off-by-one faults.       declarations. Each trace record5 consists of the identification
Two refinements improve fault detection: an anti-trivial bias        of one of the program points previously declared, and, for
soft-asserted in each SMT query nudges Z3 away from trivial          each of the variables declared in that point, its value in a
values that mask faults, and a literal relevance check inspired      given execution. We achieve this by printing the value of each
by Modified Condition/Decision Coverage strengthens each             visible variable at each location of the faulty method.
clause query so every literal constrains admissible outputs.            Since we want to generate passing and failing invariants sep-
   A runtime check phase splits the suite into Passing and           arately, we perform two runs of this instrumentation process.
Failing methods, containing, respectively, the set of passing        Both runs insert the print statements required for trace genera-
tests P and of failing tests F , which are consumed by SNAP’s        tion. One additionally disables the failing tests by removing the
fault localization procedure.                                        invocation of Failing, while the other disables the passing
   Tool     details     and     sources    are     available    at   tests by removing the invocation of Passing. As a result,
https://github.com/VeriFixer/DafnyCBT.                               in the first run, only passing executions are considered for
                                                                     invariant inference, while in the second, only failing executions
C. Snapshot Generation
                                                                     are considered.
   The set of boolean predicates from which snapshots are
                                                                        2) Snapshot Generation via Enumeration: SNAP comple-
generated is identified by two different processes: (1) inference
                                                                     ments the generation of snapshots via invariant inference
of invariants at each location of the faulty method, and (2)
                                                                     with the enumeration of boolean predicates collected from
enumeration of boolean predicates relevant in the context of
                                                                     different sources throughout the program, motivated by a
the faulty method.
                                                                     study by Pytlik et al. [17] that discusses the limitations
   1) Snapshot Generation via Invariant Inference: An in-            of invariant inference for fault localization. Essentially, the
variant is a property that is always true at a given program         invariants inferred by Daikon enable the discovery of more
location. For SNAP, the distinction between passing and              complex and semantically rich properties about the program,
failing invariants is fundamental in identifying faulty behavior.    while the enumeration process provides completeness due to
The set of passing invariants πl corresponds to properties           its exhaustive coverage of basic conditions.
that are true at program location l in every execution of the
passing tests P . Conversely, the set of failing invariants ϕl          2 https://plse.cs.washington.edu/daikon/download/doc/developer.html#New-

corresponds to properties that hold at location l for every          front-ends, accessed Aug. 2026.
                                                                        3 More information about the expected header format is available at
execution of the failing tests F . The boolean predicates in         https://plse.cs.washington.edu/daikon/download/doc/developer.html#Declarations,
Π = {p | p ∈ ϕl ∧ p ∈      / πl }, i.e., the properties that hold    accessed Aug. 2026.
                                                                        4 By default, Daikon only supports invariant inference at methods’ entries
in failing tests but not in passing ones, are representative of
potentially faulty behavior. For each invariant i ∈ Π inferred       and exits, but the documentation mentions a workaround that can be achieved
                                                                     by inserting dummy method calls, that take all visible variables as parameters,
at location l, a snapshot ⟨l, i, true⟩ is generated.                 at the additional locations we wish to infer invariants at. The invariants
   We collect invariants using Daikon [16], a dynamic likely         produced by Daikon at the dummy method’s entry and exit are the invariants
invariant inference tool. It is dynamic because it operates by       that hold at the call location.
                                                                        5 For more information about the expected trace record format, visit
observing evidence of the program’s behavior during execu-           https://plse.cs.washington.edu/daikon/download/doc/developer.html#Data-
tion, through the analysis of a trace file that records values       trace-records, accessed Aug. 2026.
   The enumeration process is, in principle, similar to invariant      dependence (cd), i.e., the distance between the snapshot’s
inference, except that it relies on expressions directly captured      location and the location where the contract violation occurs
from the program and on simpler templates (adopted from                when taking the shortest direct path. The second is expression
AutoFix), rather than using those implemented by a tool, and           dependence (ed), i.e., the similarity between the snapshot’s
then checks whether they hold during execution. The set of             predicate and the violated contract in terms of how many
collected boolean predicates B is defined as follows:                  sub-expressions they share. The dynamic analysis metric (dyn)
   • Boolean expressions. For every boolean expression b ap-           consists of a weighted sum measuring how often the snapshot
      pearing in the faulty method’s contract or implementation,       appears in failing test runs as opposed to passing ones. Its
      b ∈ B.                                                           value is higher the more it appears in failing tests and the
   • Argumentless boolean queries (boolean-valued func-                less it appears in passing tests, following spectrum-based fault
      tions). For every argumentless boolean query q publicly          localization approaches [19], [21].
      available in the faulty method’s scope, q() ∈ B. For                Each of the three metrics, as well as the overall suspicious-
      Dafny, this corresponds to predicates and functions with         ness score for a snapshot ⟨l, p, v⟩, is, respectively, computed
      boolean return type belonging to the same class as the           as follows:
                                                                                                           cdist(l, f )
      faulty method (or scope, in case the program does not                  cd(l, f ) = 1 −
      follow the OO paradigm, as often happens in Dafny).                                    max{cdist(λ, f ) | λ ∈ m ∧ λ ⇝ f }
   • Constructed argumentless boolean queries. For every               where m is the faulty method, f is the location where the
      object o visible in the faulty method’s contract or im-          contract violation occurs, l1 ⇝ l2 represents the existence of
      plementation, and every argumentless boolean query q             a direct path from program location l1 to program location
      publicly available in o’s class, o.q() ∈ B.                      l2 , and cdist(l1 , l2 ) represents the length of the shortest path
   • Boolean expressions constructed from integer expres-              from l1 to l2 .
      sions. For every two integer expressions e and e′ appear-                                           eprox(p, c)
                                                                                    ed(p, c) =
      ing in the faulty method’s contract or implementation, or                                   max{eprox(λ, c) | λ ∈ B}
      resulting from calling each available argumentless integer
                                                                          where c is the violated contract, and eprox(e1 , e2 ) repre-
      query on each object appearing in the faulty method’s
                                                                       sents the number of shared sub-expressions between expres-
      contract or body, {e = e′ , e < e′ , e ≤ e′ } ⊂ B
                                                                       sion e1 and expression e2 .
      (and, by symmetry, {e′ < e, e′ ≤ e} ⊂ B), as well
      as, {e = 0, e < 0, e ≤ 0} ⊂ B (and, by symmetry,                                       α
                                                                       dyn(⟨l, p, v⟩) = γ +       (1−β+βα#p(⟨l,p,v⟩) )−α#f (⟨l,p,v⟩)
      {e′ = 0, e′ < 0, e′ ≤ 0} ⊂ B).                                                        1−α
   • Null checks. For every nullable reference type expres-            where #p(⟨l, p, v⟩) is the number of passing tests where the
      sion e appearing in the faulty method’s contract or              snapshot appears, #f (⟨l, p, v⟩) is the number of failing tests
      implementation, or resulting from calling each available         where the snapshot appears, and α, β, and γ are non-negative
      argumentless nullable reference type query on each ob-           real numbers. AutoFix empirically determined α = 1/3, β =
      ject appearing in the faulty method’s contract or body,          2/3, and γ = 1, which we adopt in our implementation.
      e = null ∈ B.                                                                                              3
   • Logical implications. For each logical implication                susp(⟨l, p, v⟩) =
                                                                                           cd(l, f )−1 + ed(p, c)−1 + dyn(⟨l, p, v⟩)−1
      a =⇒ b appearing in the faulty method’s contract or in
      the contract of the included queries, {a =⇒ b, ¬a =⇒             This suspiciousness score formula takes the dynamic score as
      b, a =⇒ ¬b, b =⇒ a} ⊂ B.                                         the primary source of evidence, and control and expression
   For each program location l, and each boolean predicate             dependence as secondary criteria to discriminate between
p ∈ B capable of being evaluated at l (i.e., every variable            snapshots with similar dynamic score (dynamic score has a
appearing in sub-expressions of p is visible at l), a snapshot         minimum of 1 while the others vary between 0 and 1).
⟨l, p, v⟩ is generated, where the value of v is either true or            Calculating the dynamic score involves knowing how many
f alse, as dynamically observed during test suite execution.           times a snapshot appears in executions of passing and failing
The triple ⟨l, p, true⟩ will be included in the set of snapshots       tests. We collect this information by instrumenting the faulty
if predicate p is true at location l in at least one test execution.   program. For each ⟨l, p⟩ snapshot pair, we insert one print
The same applies to ⟨l, p, f alse⟩.                                    statement evaluating p at location l of the faulty method. The
                                                                       output of the instrumented program allows us to count how
D. Suspiciousness Score Computation                                    many times each snapshot appears across test executions.
   A suspiciousness score is a metric commonly used in
fault localization techniques to estimate how likely a program           III. C OUNTEREXAMPLE -BASED FAULT L OCALIZATION
component is to be the cause of a fault. Several formulas                 Counterexample-based techniques use the diagnostic infor-
for the computation of this metric have been proposed in the           mation produced by the SMT solver when a verification con-
literature [18]–[20]. SNAP’s formula combines three factors.           dition fails. These methods transform the abstract execution
Two static metrics are taken into consideration for calculating        traces (counterexamples) into a ranked list of suspicious pro-
the suspiciousness score of a snapshot. The first is control           gram lines. We categorize these techniques into three levels of
increasing complexity: baseline (CNTB), structured (CNTS),           we prioritize discovering new buggy branches over exploring
and multi-trace (CNTM). CNTM is the primary technique                different data valuations of the same logical error. The aggre-
proposed in this work, while CNTB and CNTS are simplified            gate path set Π = {πi , πj , ..., πn } includes all the collected
variants that isolate the contribution of its components.            independent trace paths.
     a) Counterexample Baseline (CNTB): CNTB extracts
counterexample data directly from the diagnostic mes-                B. Iterative Path Extraction Algorithm (CNTM)
sages produced by the Dafny CLI when run with the                       To address the limitation of the Dafny verifier providing
extract-counterexample flag. This method produces                    a single counterexample path per failing condition, we im-
exactly one counterexample for each failing verification con-        plement an iterative instrumentation strategy to exhaustively
dition (e.g., an assertion or postcondition), providing a single     explore alternative independent failing execution traces. The
witness even if multiple failing paths exist for that same           algorithm prunes previously discovered paths, forcing the SMT
condition. CNTB performs no advanced heuristic weighting, it         solver to find different ways the same verification condition
simply identifies every line involved in the reported execution      might fail. For a failing verification condition v (e.g., an
path and maps it to the corresponding source code, resulting         assertion or postcondition), the process is as follows:
in a raw set of suspicious lines.                                       1) Initial Extraction. The verifier runs to obtain an initial
     b) Counterexample Single-Trace Structured Ranker                       counterexample C for condition v, and its associated ex-
(CNTS): CNTS significantly refines the raw output of the                    ecution path π from the Dafny CLI diagnostic messages.
baseline by introducing code-awareness in a ranking heuristic           2) Path Pruning. Identification of the deepest branch point
that prioritizes program lines based on their structural                    within π, representing the final logical decision (e.g., an
properties. CNTS’s two primary functional improvements                      if branch or loop entry) that led to the failure.
over CNTB consist of its enhanced structural extraction and             3) Instrumentation. Temporary instrumentation of the
formal ranking system. Because the tool is code-aware, it                   source code through the injection of an assume
extends the diagnostic set beyond the literal lines found in the            false statement at this specific branch point, effec-
trace. It identifies and flags as suspicious the condition nodes            tively pruning the discovered path from the search space.
of if, while, and for blocks whenever a line identified                 4) Iterative Discovery. The verifier is re-run on the instru-
in the failing trace exists within their scope. Additionally,               mented version of the code. If a new counterexample
CNTS provides discriminatory power that the baseline lacks                  C ′ for v is identified by the solver, the new path π ′ is
by ranking these lines using structural heuristics based on                 extracted and the process is repeated from Step 2.
line frequency, nesting depth, and node type.                           5) Termination. The loop terminates when condition v ei-
     c) Counterexample Multi-Trace Aggregator (CNTM):                       ther verifies or no further counterexamples are generated,
CNTM addresses the primary limitation of the single-trace                   indicating all unique failing paths have been captured.
approach in that a single counterexample is merely one of
many possible ways a program can fail. Relying on a single           C. Multi-Criteria Ranking Across Counterexamples (CNTS,
trace per verification condition failure can lead to an incom-       CNTM)
plete exploration of the fault space. CNTM improves upon
CNTS by forcing SMT solver diversity through an iterative
                                                                        Once S           S path set Π is collected, we rank each
                                                                              the aggregate
                                                                     line l ∈ Π, where Π denotes the set of all unique program
path blocking mechanism. Upon finding a counterexample, the
                                                                     lines appearing across the paths in Π, using a hierarchical
system identifies the associated execution path and introduces
                                                                     scoring system to prioritize root causes over incidental exe-
a temporary constraint to block that specific path in the solver’s
                                                                     cution steps. This ensures that the most suspicious lines are
next search. This process is repeated to collect multiple,
                                                                     presented to the developer first. The ranking is determined by
independent failing paths. CNTM then aggregates evidence
                                                                     the lexicographical comparison of the following tuple:
across all collected traces, assigning higher suspiciousness to
lines that appear consistently across diverse failure paths.            rank(l) = ⟨−freq(l), −max dep(l), −is cntr(l), ord(l)⟩
A. Formal Model of Counterexamples                                     This order is defined by four metrics:
   A verification failure produces a counterexample C, for-            • Frequency (freq(l)): The number of independent paths
malized as a tuple ⟨σ, π⟩, where σ represents the valuation of           in Π that contain line l serves as the primary filter. Lines
variables and π = {ℓ1 , ℓ2 , . . . , ℓn } the trace path sequence,       recurring across multiple independent paths represent a
defined as the ordered program lines executed in the coun-               “consensus” of suspicion.
terexample.                                                            • Maximum Depth (max dep(l)): The maximum nesting
   1) Path Independence: By default, Dafny only provides                 level of the statement at line l. Targets structural complex-
one counterexample trace per failed verification condition.              ity, based on the heuristic that logical errors frequently
To improve coverage, CNTM seeks a set of independent                     hide within deeply nested blocks.
counterexamples. Two counterexamples Ci = ⟨σi , πi ⟩ and               • Control Statement (is cntr(l)): A boolean indicator
Cj = ⟨σj , πj ⟩ are path-independent if and only if their                of whether line l consists of a branch guard (e.g.,
execution paths differ: πi ̸= πj . This distinction ensures that         if/while/for). These are prioritized to highlight the
       decisions, serving as a tie-break if other lines are at the         Given a verification failure, the model receives the numbered
       same nesting level as these control statements.                     source code and is asked to identify the most likely line(s)
     • Trace Order (ord(l)): The absolute position of line l in            responsible for the failure. In this baseline, the model receives
       the file, used only to break ties.                                  no additional information.
                                                                              Our goal is not to optimize LLM performance, but rather
D. Multi-Trace Aggregator Execution Example (CNTM)                         to compare verifier-native fault localization techniques against
   To illustrate the iterative path extraction process, consider           a representative LLM-based approach. Fully optimizing the
the demo method in Listing 1, which contains two distinct                  LLM would introduce additional experimental variables, such
logical errors, in Lines 4 and 8, that violate the postcondition           as prompt engineering, model selection, retrieval mechanisms,
y = x for positive inputs.                                                 and few-shot examples, requiring dedicated ablation studies
                                                                           beyond the scope of this work. Still, to strengthen the com-
 1 method demo(x: int) returns (y: int)
 2   ensures x > 0 ==> y == x {
                                                                           parison, our study includes two additional variants. LLM ER
 3   if x > 1 {      // Path C2: (x=2)                                     augments the original setup with the verifier error message,
 4     y := x + 1;   // Bug: y should be x                                 and LLM ER CN constitutes a hybrid configuration com-
 5     return y;
 6   } if x > 0 {    // Path C1: (x=1)
                                                                           bining verifier error messages with CNTM’s ranking, aiming
 7     // assume false                                                     to capture potential synergies between the two. We used the
 8     y := x + 2;   // Bug: y should be x                                 following prompt:
 9     return y;
10   }                                                                     You are a fault localization model. Rank suspicious
11   return x;                                                             lines from most to least likely to be faulty.
12 }
                                                                           Output contract (strict):
                                                                           1) The list is a ranking: the first element must
Listing 1. Example of path extraction via instrumentation, used by CNTM.   be the line most likely to contain the fault.
                                                                           2) You do not have to return a full list with all
     For this example, the algorithm proceeds as follows:                  the lines, prefer shorter lists.
                                                                           3) Return exactly one JSON array of unique 1-based
1) Initial Counterexample Extraction (C1 ). Upon the first ver-            line numbers.
ification attempt, the SMT solver identifies a counterexample              4) Do not return any explanation, markdown, code
                                                                           fences, labels, or extra text.
where x = 1. The execution path π1 skips the first if block                5) Use integers in the inclusive range[1, t_lines].
(since 1 ≯ 1) and enters the second if block (1 > 0). The                  6) If no suspicious lines are found, return [].
solver returns the trace π1 = {line 6, line 8, line 9}, where              7) Your entire response must match this pattern:
                                                                           ˆ\\[(?:\\s*\\d+\\s*(?:,\\s*\\d+\\s*)*)?\\]$
Line 8 contains the buggy assignment y := x + 2.                           Example valid response: [30, 15, 29]
2) Path Pruning via Instrumentation. To discover other                     {verifier error if LLM_ER variant}
                                                                           The file has {t_lines} lines.
potential faults, the algorithm instruments the second if                  BEGIN_FILE
branch. As shown in Line 7, an assume false statement                      {numbered_source_code}
is dynamically injected at the start of the branch explored by             END_FILE
C1 . This statement instructs the solver to ignore any execution              We used qwen3-coder-next model via OpenRouter
path that enters this specific block during the next iteration.            (tested in April 2026). Generation followed OpenRouter’s
3) Second Counterexample Extraction (C2 ). With the path π1                defaults, with temperature 1.0, top p 0.95, top k 40, a max-
effectively blocked, the verifier is forced to explore alternative         imum output length of 66,000 tokens, and a context window
branches to satisfy the negation of the postcondition, identi-             of 262,144 tokens. We selected it to balance reproducibility,
fying x = 2. This execution path π2 explores the first if                  performance, and cost. Unlike proprietary models, which
block (2 > 1), yielding π2 = {line 3, line 4, line 5}, where               change over time and hinder exact replication, open-weight
Line 4 contains the second buggy assignment y := x + 1.                    models provide fixed, versioned checkpoints that enable re-
Since, after blocking these two branches, no further failing               producibility. At the time of this study, the model was the
paths exist, the iteration terminates.                                     latest Qwen code model and among the strongest open-
Resulting Ranking Input. The algorithm concludes with the                  weight coding LLMs available, achieving competitive results
aggregate set Π = {π1 , π2 }. By forcing the solver to move                on coding benchmarks (e.g., 70% on SWE-bench [22]).
past the first discovered error, we ensure that both if blocks
                                                                                                  V. E VALUATION
are identified as candidates for fault localization. Note that
if a line were shared between these two independent paths,                 A. Research questions
its Frequency count would increase, correctly marking it as a                 Our empirical evaluation aims to answer the following
highly suspicious common point of failure.                                 research questions:
                                                                           RQ1 (State vs. Path): How do state-based FL techniques
            IV. LLM-BASED FAULT L OCALIZATION                              compare to counterexample-based FL techniques?
  As a complement to the verifier-native techniques presented              RQ2 (Ranking Ablation Study): How do the individual
above, we present LLM, a fault localization baseline that relies           ranking components (frequency, depth, and structure) compare
on a large language model to rank suspicious program lines.                in terms of their contribution to FL effectiveness?
RQ3 (Path Diversity): How does multi-trace aggregation                  tants for processing. This sample size is statistically robust,
compare to single-trace analysis in terms of FL effectiveness?          as studies suggest that 300 to 1,000 mutants are sufficient to
RQ4 (LLM Baseline Comparison): How do verifier-native                   yield stable fault localization results and approximate mutation
FL techniques compare to a general-purpose LLM baseline?                scores within narrow error bounds [23], [24].
                                                                           Our dataset of 500 programs comprises a total of 44,242
B. Experimental Procedure
                                                                        lines of code, averaging 88 lines per program file. Additionally,
   We evaluate SNAP, the counterexample techniques (CNTB,               on average, each program contains five non-ghost components,
CNTS, and CNTM), and the LLM techniques (LLM,                           which in Dafny includes methods, functions, and other similar
LLM ER, and LLM ER CN) within a unified experimental                    constructs. Table I summarizes the 23 mutation operators, out
framework on Dafny mutants derived from DafnyBench. As a                of 40 supported by MutDafny, that led to the generation of the
reference point, we include a RAND baseline, which returns              500 mutants included in our dataset, showcasing the variety
all lines of the failing method randomized, serving as a sanity         of types of faults it tries to mimic. These include 16 mutation
check for calibration rather than as a competing technique.             operators previously proposed in mutation tools for other
   We generated our evaluation benchmark using MutDafny [7]             programming languages, as well as seven newly proposed by
and all of its mutation operators to produce mutants from the           MutDafny. These seven operators were selected based on an
785 programs of DafnyBench [6]. The set of generated mutants            analysis of bugfix evidence from Dafny projects available on
includes 68,957 that fail verification, i.e., contain faults de-        GitHub, making the mutants they generate representative of
tected by Dafny’s verifier. However, MutDafny stores mutants            real mistakes Dafny developers make.
in their post-resolution representation and, when converting               For each mutant, the ground truth, i.e., the fault location,
them back to source code, this process can produce invalid              was established by performing a diff against the original
Dafny programs. We, therefore, filtered for valid, compilable           program, to identify the mutated location.
code, reducing the set to 57,925 mutants.                                  Our experimental procedure involves applying each fault
                                                                        localization technique to each of the 500 faulty programs in
                           TABLE I
M UTATION OPERATORS USED IN THE ARTIFICIAL FAULT DATASET. #M IS
                                                                        our dataset. For each strategy and mutant, we produce a ranked
    THE NUMBER OF MUTANTS GENERATED WITH EACH OPERATOR .                list of lines L = [l1 , . . . , lt ], ordered by suspiciousness, and
                                                                        evaluate it against the ground-truth faulty line lgt .
    Op. Description                                                #M
    AOR Replacement of an arithmetic operator with another         33
    ROR Replacement of a relational operator with another          51   C. Experimental Metrics
    COR Replacement of a conditional operator with another         4
    BBR Replacement of a relational or conditional expression      20      We evaluate fault localization effectiveness using the EXAM
        with true or false                                              score, which captures the effort required to locate the faulty
    AOI Insertion of a unary minus in an arithmetic expression     76
    COI Insertion of a not operator in a conditional expression    21   line, Top-k success rates, and two coverage indicators: Found
    AOD Deletion of a unary minus in an arithmetic expression      1    rate, measuring the proportion of cases where the ground truth
    COD Deletion of a not operator in a conditional expression     1    appears in the model’s ranking, and Empty rate, representing
    LVR Replacement of a numerical literal with its increment,     50
        decrement, or zero, and of a string literal with an             the proportion of cases where the model returns no lines.
        empty one, a default one, or a mutation of the original            For the EXAM score, we adopt a normalized, 0-based
    EVR Replacement of an expression with a default literal        62   formulation. Let N denote the number of candidate lines in the
    VER Replacement of same-type variables                         92
    LBI Insertion of a break statement at the beggining of         5    search scope, and let r be the number of non-fault lines appear-
        the body of a loop                                              ing in the ranked list L inspected before matching the ground-
    MRR Replacement of a call with a default return-type literal   6    truth faulty line lgt . It is defined as EXAM = r/(N − 1),
    MAP Replacement of a call with one of its arguments with       1
        the same type as the return value                               where a value of 0 indicates immediate localization and 1
    MVR Replacement of a call with a same-type variable            8    indicates that the fault is found last in the ranking.
    SAR Swap of a call argument with a same-type one used in       2
        the same call
                                                                           Rankings are computed over absolute line numbers within
    CIR Replacement of a non-empty collection initializer with     6    the active scope (file or method). However, strategies are not
        an empty one, and of an empty initializer with a default        required to return rankings containing every single line. When
        non-empty one
    CBE Extraction of one of the blocks of an if or if-then-else   7
                                                                        the faulty line is absent from an output of size t, we estimate
        statement and deletion of the remaining ones                    the remaining effort by assuming that the developer continues
    DCR Replacement of a datatype constructor with another of      1    inspecting the remaining N − t lines in random order. Under
        the same datatype and with the same signature
    FAR Replacement of a class’s field access with another         1
                                                                        this assumption, the fault is expected to appear at the midpoint
        same-class field                                                of the unranked portion, and the EXAM score is computed
    SDL Deletion of a statement or of an entire code block         28   accordingly, as proposed by Pearson et al. [25].
    ODL Deletion of all occurrences of a binary operator (and      12
        of one of its arguments to preserve program validity)              We assess statistical significance on EXAM scores using
    SWS Swap of a statement with a neighboring one                 12   paired, two-sided Wilcoxon signed-rank tests. We report p-
                                                                        values together with matched rank-biserial correlations as
  Given the high computational cost of iterative SMT solver             effect sizes. For Top-1 localization, we use McNemar’s exact
calls and invariant inference, we randomly sampled 500 mu-              test and report paired odds ratios.
D. Dual-Scope Evaluation                                              as multidimensional arrays, function arguments, and nested
  We perform our empirical evaluation under two scopes,               types (e.g., map<int, (int, int)>). Additionally, in 61
capturing two different debugging scenarios:                          programs, though valid tests are generated, they either do not
                                                                      exercise the faulty method or fail to split the tests into passing
  • File scope: Considers all executable lines in the program
                                                                      and failing, a prerequisite for SNAP. From the remaining, 11
     file, reflecting the standard fault localization setting where
                                                                      timed out after six hours, and another 11 failed after exhausting
     there are no assumptions about the fault location [25].
                                                                      the available memory, since the state-based technique is also
  • Method scope: Considers executable lines within the
                                                                      significantly more computationally expensive than the others.
     faulty method, reflecting a workflow where the developer
                                                                      For the 297 programs for which all techniques produce non-
     has already narrowed the search space using the verifier’s
                                                                      empty outputs, SNAP attains an EXAM score of 0.212 at file
     error message. This evaluates localization performance
                                                                      scope and 0.359 at method scope, which is still substantially
     within the identified faulty method.
                                                                      worse than CNTM.
E. Comparison with State-of-the-Art Methods                              In the file setting, SNAP performs worse than RAND, which
   We focus on verifier-native methods for verification-aware         merely ranks lines uniformly at random among failing meth-
programming languages, where specifications can provide a             ods. Nevertheless, SNAP performs better than RAND when
more reliable correctness oracle than test suites. As a result,       evaluated at the method scope, highlighting RAND’s distinct
our evaluation does not include a comparison to classical             behavior across scopes. RAND restricts its search to the lines
fault localization methods (e.g., spectrum-based (SBFL) and           of the failing method, and, because the method represents
mutation-based (MBFL)) that rely solely on test suites as the         only a fraction of the file, the expected file-scope EXAM for
correctness oracle. Porting test-based methods to Dafny would         RAND is approximately the method-to-file size ratio (around
require a higher-quality test generator capable of producing a        0.19 in our dataset). Consequently, any technique that merely
diverse suite with reliable pass/fail labels, a capability Dafny      identifies the correct method already approaches this baseline.
and even our DafnyCBT prototype currently lack. Because the           However, at method scope, RAND yields a score near 0.5
resulting effectiveness would be dominated by test-generation         (0.483), representative of random line selection. The fact that
quality rather than by the localization technique itself, a fair      SNAP outperforms RAND at this scope (0.359) indicates that,
evaluation would need to distinguish these two factors. We            when the correct method has already been isolated, SNAP’s
therefore consider a systematic comparison of test versus             snapshot-based heuristics do carry a meaningful signal for
specification oracles for fault localization to be a distinct         distinguishing faulty statements from correct ones. Despite
research contribution, outside the scope of this paper.               this, the results still indicate that SNAP’s limitations go beyond
                                                                      incomplete support for certain classes of programs. Even when
                         VI. R ESULTS                                 it produces outputs, its ranking quality remains subpar.
   Tables II-V contain the scores for the different metrics              This discrepancy is also reflected in effectiveness. In ad-
for all the fault localization models. Figure1 illustrates the        dition to SNAP’s high Empty rate (39.20%), it only locates
distribution of results.                                              47.00% of faults, while CNTM achieves a Found rate of 84%
   For EXAM, CNTM significantly outperforms all non-LLM               with only 1.4% of empty outputs. A likely contributing factor
baselines (p < 0.05), while differences with LLM are not              is SNAP’s reliance on test executions, its effectiveness being
significant (p = 0.101) and have a negligible effect size. For        tied to how well the generated tests exercise relevant pro-
Top-1, LLM significantly outperforms CNTM (p < 0.05), with            gram behavior. When paths containing faults are insufficiently
CNTM outperforming all other baselines. Thus, the answers             covered, SNAP may fail to produce meaningful rankings or
to the research questions focus more on CNTM than on the              any output at all. In contrast, counterexample-based tech-
other counterexample-based variants. Full statistical results are     niques operate directly on verifier-provided counterexamples
provided in the Appendix in Tables VI and VII.                        that encode failure-inducing executions, without requiring test
                                                                      generation. As a result, they are less sensitive to coverage
A. RQ1 (State vs. Path): How do state-based FL techniques             limitations. Overall, SNAP’s weaker performance appears to
compare to counterexample-based FL techniques?                        result from both limited coverage in test-based execution and
   Table II shows that our counterexample-based approach out-         lower-quality rankings, even when outputs are available.
performs the state-based approach we adapted from the litera-
ture. At file scope, SNAP achieves an EXAM score of 0.324,              Our novel counterexample-based technique largely out-
compared to 0.109 for CNTM, with a similar gap at method                performs the state-based technique, achieving higher over-
scope. One key factor is SNAP’s high rate of empty predictions          all effectiveness across a larger number of programs.
(39.20%), which are penalized by the EXAM metric (assigned
a default score of 0.5 when no ranking is produced). This high        B. RQ2 (Ranking Ablation Study): How do the individual
Empty rate is mostly due to limitations of the testing tool,          ranking components (frequency, depth, and structure) compare
which, as an early prototype, produces valid test files for only      in terms of their contribution to FL effectiveness?
387 out of the 500 programs in our dataset, lacking support             To isolate the contribution of each ranking component,
for programs involving more complex language features, such           we perform an ablation study on the CNTM approach
                             TABLE II                                                                        TABLE III
 FAULT LOCALIZATION ON A LL (500 PROGRAMS ) AND C OMP. ( THE 297                     FAULT LOCALIZATION PERFORMANCE ACROSS STRATEGIES (500
WITH NON - EMPTY OUTPUTS FROM ALL METHODS ). M ETRICS : EX F /EX M                          PROGRAMS ). M ETRICS AS DEFINED IN TABLE II.
  (EXAM SCORE , FILE / METHOD SCOPE ); T OP -k (% OF FAULTS RANKED
 WITHIN THE TOP K PREDICTIONS ); F (% OF CASES THAT SUCCESSFULLY
     LOCATE THE FAULT ); E (% THAT RETURN AN EMPTY OUTPUT ).
                                                                                   Strat.          EXF      EXM        Top-1/3/5         F/E
                                                                                   CNTM            0.109    0.155     43 / 71 / 78    84.00 / 1.40
  Data              Strat.   EXF     EXM      Top-1/3/5           F/E              CNTM RAW        0.190    0.299     18 / 39 / 58    74.40 / 1.40
                                                                                   CNTM NF         0.109    0.160     36 / 71 / 79    84.00 / 1.40
                    CNTM     0.109   0.155   43 / 71 / 78      84.00 / 1.40        CNTM ND         0.139    0.244     22 / 49 / 64    84.00 / 1.40
  All               SNAP     0.324   0.413    8 / 20 / 32     47.00 / 39.20        CNTM NC         0.113    0.166     37 / 68 / 77    84.00 / 1.40
                    RAND     0.187   0.483    6 / 22 / 35      95.40 / 1.00
                    CNTM     0.092   0.138   46 / 77 / 83      87.54 / 0.00
                                                                                                           TABLE IV
  Comp.             SNAP     0.212   0.359   11 / 33 / 53      77.44 / 0.00
                                                                                     FAULT LOCALIZATION PERFORMANCE ACROSS STRATEGIES (500
                    RAND     0.186   0.479    7 / 26 / 39      98.99 / 0.00                   PROGRAMNS ). M ETRICS AS DEFINES IN II


                                                                                      Strat.    EXF      EXM        Top-1/3/5         F/E
              1.0                                                Median
              0.8                                                Mean                 CNTB      0.243    0.322    12 / 31 / 50     61.40 / 5.20
                                                                                      CNTS      0.127    0.181    27 / 64 / 76     80.80 / 2.60
 EXAM Score




                                                                                      CNTM      0.109    0.155    43 / 71 / 78     84.00 / 1.40
              0.6
              0.4
                                                                                 overall search space.
              0.2
                                                                                   Structured ranking is a major contributor to localization
              0.0                                                                  quality. Neglecting structural context doubles the devel-
                    RAND     CNTB    CNTS     CNTM      LLM        SNAP            oper’s search effort (EXAM) and reduces Top-1 accuracy.
                                       Technique
                                                                                 C. RQ3 (Path Diversity): How does multi-trace aggregation
Fig. 1. Distribution of file-scoped EXAM scores. The boxplots illustrate
the median, quartiles, and outlier variability across techniques. Boxplots use
                                                                                 compare to single-trace analysis in terms of FL effectiveness?
Tukey whiskers (1.5×IQR); outliers are not shown.                                   Compared to CNTB and CNTS, CNTM consistently im-
                                                                                 proves across all metrics, as depicted in Table IV. CNTB’s per-
                                                                                 formance is uniformly lower and, thus, not further discussed.
and four variants. CNTM RAW uses only raw CLI coun-                              For CNTS, at file scope, EXAM decreases from 0.127 to 0.109
terexample lines without augmenting them with control-flow                       with significance but moderate effect, and, at method scope,
data, and the three remaining versions respectively ignore                       from 0.181 to 0.155. Figure 1 shows that CNTM outperforms
frequency (CNTM NF), depth (CNTM ND), and control-                               CNTS, exhibiting a lower median and an overall distribution
statement (CNTM NC) priority in the ranking formula.                             shifted closer to zero, indicating it tends to discover faults
   The results, summarized in Table III, demonstrate that                        earlier across the evaluated budget range.
structural awareness is a significant driver of localization                        However, the gains are better reflected in Top-k perfor-
precision. The most significant performance drop occurs in                       mance, with Top-1 improving substantially from 27% (CNTS)
the CNTM RAW variant. By discarding the augmented logical                        to 43% (CNTM), and with corresponding improvements in
context, the EXAM score degrades dramatically (from 0.109 to                     Top-3 and Top-5 accuracy. Coverage also improves, with the
0.190 at file scope), meaning a developer would have to search                   Found rate increasing from 80.80% to 84.00%, and the Empty
almost twice as much code to find the fault. Furthermore, the                    rate decreasing from 2.60% to 1.40%.
Top-1 accuracy collapses from 43% to just 18%.
   Among the individual ranking heuristics, depth proved to be                     Using diverse counterexample paths, multi-trace aggrega-
the most critical. Removing it (CNTM ND) caused the EXAM                           tion significantly improves ranking quality and robustness.
score to worsen significantly (rising to 0.139 at file scope and
0.244 at method scope) and slashed Top-1 performance by                          D. RQ4 (LLM Baseline Comparison): How do verifier-native
half (22%). This confirms that the hierarchical position of a                    FL techniques compare to a general-purpose LLM baseline?
statement is a high-signal indicator of a fault’s root cause.                       We compare CNTM with the LLM localization baseline
   The suppression of both the frequency (CNTM NF) and                           and the LLM ER and LLM ER CN variants to contextualize
control-flow (CTNM NC) heuristics did not cause any statisti-                    verifier-native techniques within a broader landscape. The
cally significant EXAM score changes regarding the baseline.                     results are presented in Table V, and show that LLM achieves
However, in Top-1 accuracy, there is a noticeable dip from                       higher Top-1 accuracy (58%) than CNTM (43%) (statistically
43% to, respectively, 36% and 37%. This suggests that, while                     significant), indicating stronger performance at placing the
these factors help pinpoint the exact bug as the first result,                   faulty line at the very top of the ranking. This behavior is
structural features like depth are more vital for reducing the                   further illustrated in Figure 1, where the LLM variants exhibit
                            TABLE V                                 In contrast, CNTM produces deterministic and reproducible
    FAULT LOCALIZATION PERFORMANCE ACROSS STRATEGIES (500           rankings grounded in counterexample traces and operates
           PROGRAMS ). M ETRICS AS DEFINED IN TABLE II.
                                                                    entirely within the verification pipeline.
  Strat.           EXF     EXM      Top-1/3/5        F/E              LLM achieves higher Top-1 accuracy, while CNTM pro-
  CNTM            0.109    0.155   43 / 71 / 78   84.00 / 1.40        vides more consistent ranking quality and reliability.
  LLM             0.159    0.217   58 / 65 / 68   72.60 / 1.00        These approaches should be viewed as complementary,
  LLM ER          0.264    0.303   37 / 48 / 50   50.80 / 0.00        and future work may explore hybrid methods combining
  LLM ER CN       0.131    0.167   46 / 72 / 76   77.20 / 0.20
                                                                      counterexample information with LLM reasoning.

                                                                                    VII. T HREATS TO VALIDITY
a median closer to zero than CNTM, indicating that they more
frequently rank the faulty line near the top. However, they         Mutation realism. Our mutations are synthetic, generated by
also exhibit substantially longer tails, reflecting many cases in   predefined operators. Real verification bugs may differ: they
which the faulty line is ranked much lower or absent among          might involve complex logic errors, subtle contract misspecifi-
the returned candidate lines.                                       cations, or edge cases not well-modeled by simple mutations.
   In contrast, CNTM achieves better overall ranking quality as     However, mutation-based evaluation is standard practice in
measured by EXAM. At file scope (however, not statistically         fault localization [27] and provides controlled ground truth
significant), CNTM attains an EXAM of 0.109, compared to            unavailable in real-world settings. In addition, the mutation
0.159 for the LLM, suggesting lower average inspection effort       operators used in our dataset are drawn from existing work
across the full ranking. Furthermore, CNTM exhibits higher          [7], where several operators resulted from an analysis of bugfix
reliability, with a higher Found rate (84.00% vs. 72.60%).          evidence from Dafny projects available on GitHub.
   These results highlight complementary strengths between          Dataset characteristics. Since our dataset is drawn from
the approaches. LLM is effective at prioritizing the most likely    DafnyBench, a collection of pedagogical and algorithmic pro-
fault location (Top-1), while CNTM provides more consistent         grams, our results may not generalize, as industrial verification
rankings and broader coverage when the top prediction is            code may exhibit different patterns. However, DafnyBench is
insufficient. However, the LLM baseline is intentionally under-     widely used in prior work and serves as a standard benchmark.
optimized, which likely underestimates the true potential of        LLM comparison setup. The LLM baseline is included as
LLM-based approaches. We use a minimal setup (code-only             a reference point to situate our verifier-native techniques
input without prompt engineering, few-shot examples, or di-         within the emerging landscape of LLM-based fault localization
agnostic signals such as verifier error messages) to provide a      approaches, not as an optimized competitor. Unlike classical
neutral reference point rather than a fully competitive config-     test-based methods, LLMs require no test oracle and can
uration. To strengthen the comparison, we evaluated the two         be applied directly to source code. We deliberately avoid
additional variants LLM ER and LLM ER CN.                           prompt engineering and few-shot examples for two reasons:
   LLM ER performs worse than the baseline, consistent with         (1) optimizing LLM performance is orthogonal to our research
prior observations in Dafny [26]. Error messages are often          focus, and (2) a code-only input represents a lower bound
coarse-grained and typically indicate only the failing method,      on what an LLM can achieve without verifier integration.
which, since the model is usually good at finding the method,       The reported results should be interpreted as indicative of
adds noise rather than a useful localization signal. In practice,   the relative strengths of symbolic and learned approaches, and
for this variant, the model frequently predicts the line of         not as a ranking of which approach is superior. The further
the failing postcondition, an unsurprising but uninformative        exploration of hybrid techniques is left to future work.
answer, since that location cannot correspond to the root cause.
   LLM ER CN also does not improve over either standalone                              VIII. R ELATED W ORK
method, suggesting that simple combinations are insufficient           Traditional fault localization approaches mostly rely on test
and more careful integration is required to realize any benefit.    cases. SBFL [19], [21] compares the execution frequency of
   A plausible explanation for CNTM’s weaker Top-1 perfor-          program statements in failing tests as opposed to passing tests,
mance is that its heuristic scoring effectively identifies the      to pinpoint those most likely to be the cause of the fault. This
relevant code region, but assigns equal suspicion to all lines      is measured, for each statement, by a suspiciousness score, its
in that block with an associated counterexample state, being        value being higher the more a statement appears in failing tests
incapable of finer-grained findings. In other words, CNTM is        and the less it appears in passing tests. In turn, a statement is
good at narrowing down where the fault lies, but less effective     more suspicious the higher its suspiciousness score is. Several
at deciding which specific line is most suspicious. This is         coefficients for computing this score have been proposed, e.g.,
precisely where LLMs may have an advantage, given their             Tarantula [18], Ochiai [21], and Barinel [28].
ability to reason over local code semantics.                           MBFL [29] extends SBFL by considering, in addition to
   Advantages and Disadvantages. LLMs can use learned               execution frequency, how often mutating a statement affects
semantic patterns to achieve strong Top-1 performance, but are      the outcome of failing and passing tests. The more often
inherently non-deterministic and depend on external inference.      mutating a statement changes the outcome of failing tests and
the less it changes the outcome of passing tests, the more               The comparison with the LLM baseline should be inter-
suspicious the statement is considered. The idea behind this is       preted as contextual rather than competitive. The primary
that these statements contribute to test failures and, therefore,     goal of this work is to study deterministic, verifier-native
to the faulty behavior.                                               fault localization techniques, and not to develop or optimize
   AutoFix [4], for Eiffel, is the first Automated Program Re-        LLM-based methods. Accordingly, the LLM is evaluated in
pair (APR) tool to directly incorporate contracts into the fault      a minimal configuration, serving as a reference point rather
localization process, along with tests automatically generated        than a tuned baseline. In this setting, the LLM achieves higher
from those contracts. Instead of ranking suspicious statements,       Top-1 accuracy, while CNTM provides better overall ranking
it ranks suspicious expressions that hold at certain locations,       quality (lower EXAM) and higher reliability (Found rate).
representing specific program states in which the program does           Overall, these results suggest that counterexample-based
not behave as expected. The goal of the fix generation phase          techniques provide a robust and consistent foundation for
is to attempt to avoid this state. Candidate fixes are generated      fault localization in verification-aware languages. At the same
from templates that account for the suspicious expression.            time, the observed strengths of LLMs in prioritization indicate
   Maple [30] is an APR tool whose fault localization stage           potential benefits in combining the two approaches. Exploring
uses Hoare logic to determine the program state properties that       hybrid methods that integrate counterexample information
hold at each point, and then identify violations of expected          with LLM reasoning is a promising direction for future work.
logical entailments regarding the specification. This approach
has also been adapted for Dafny [31]. However, in both cases,                      X. DATA AVAILABILITY S TATEMENT
it suffers from the limitation of only identifying the path             The full package required to reproduce the results is avail-
containing the faulty location, rather than specific statements.      able in a pre-built, self-contained Docker image at Zenodo.
   Sullivan et al. [32] studied test and mutation generation
for Alloy. Although Alloy and Dafny operate under different                                 ACKNOWLEDGMENTS
paradigms (relational modeling versus imperative verification),          Isabel Amaral, João Pascoal Faria, and Alexandra Mendes
their work aligns with ours in exploring the generation of            were funded by National Funds through the FCT - Fundação
diverse inputs from formal constraints and using mutation             para a Ciência e a Tecnologia, I.P. (Portuguese Foundation for
analysis to evaluate verification frameworks. Zheng et al.            Science and Technology) within the project VeriFixer, with
propose FLACK [33], which localizes faults in Alloy models            reference 2023.15557.PEX (DOI: 10.54499/2023.15557.PEX).
by analyzing counterexamples produced by bounded analysis                Álvaro F. Silva was co-financed by national
and ranking model elements. Our work shares the high-level            funds through FCT – Fundação para a Ciência e a
idea that counterexamples are first-class debugging artifacts,        Tecnologia, I.P., under the support UID/50014/2025
but differs in two core ways: (1) we target verified imperative       (https://doi.org/10.54499/UID/50014/2025), and Fundação
programs (Dafny) rather than relational models; (2) we local-         para a Ciência e a Tecnologia (Portuguese Foundation
ize source-code lines and incorporate control-structure-aware         for Science and Technology) through the Carnegie
ranking extracted from Dafny traces and instrumentation.              Mellon Portugal Program under the fellowship reference
   Beyer et al. [34] study fault localization using verification      PRT/BD/155045/2024.
witnesses, i.e., artifacts that certify reachability properties and
can be post-processed to identify likely fault sites. The witness                                A PPENDIX A
perspective is complementary to ours, since it generalizes                                          A NNEX
across verifiers and intermediate formats, whereas we exploit
Dafny-specific counterexamples to directly rank source lines.                                         TABLE VI
                                                                        PAIRWISE W ILCOXON SIGNED - RANK TESTS FOR FILE - LEVEL EXAM
                       IX. C ONCLUSION                                     SCORES . C OLUMNS REPORT COMPARED METHODS (M.A, M.B),
                                                                      NON - ZERO DIFFERENCES (NZ), STATISTIC (W), p- VALUE , RANK - BISERIAL
   This paper presents a study of automated fault localiza-                   EFFECT SIZE (R- BI ), AND SIGNIFICANCE (S IG ., α = 0.05).
tion for the Dafny verification-aware language. We evaluated
state-based, counterexample-based, and LLM-based baselines                   M.A      M.B      NZ       W             p     R-bi   Sig.
                                                                             RAND     CNTB     476   48048       0.0037   -0.154   yes
across 500 mutants to better understand their relative strengths             RAND     CNTS     464   29196        1e-17    0.459   yes
in identifying root causes of verification failures.                         RAND     CNTM     467   24135        1e-25    0.558   yes
                                                                             RAND     LLM      468   44330    0.000317     0.192   yes
   Our results show that counterexample-based localization                   RAND     SNAP     467   26946        2e-21   -0.507   yes
is substantially more reliable than state-based approaches in                CNTB     CNTS     352    5284        2e-41    0.830   yes
                                                                             CNTB     CNTM     403    8116        4e-44    0.801   yes
this setting. SNAP exhibits a high Empty output rate due                     CNTB     LLM      452   29727        1e-14    0.419   yes
to its reliance on a test suite, whereas counterexample-based                CNTB     SNAP     442   32633         1e-9   -0.333   yes
                                                                             CNTS     CNTM     288   11302        2e-11    0.457   yes
techniques consistently produce actionable results, with Found               CNTS     LLM      404   37547        0.153    0.082    no
rates exceeding 84%. Within this family, moving from raw                     CNTS     SNAP     445   11546        1e-44   -0.767   yes
                                                                             CNTM     LLM      338   25696        0.101   -0.103    no
traces (CNTB) to structured ranking (CNTS) yields a signifi-                 CNTM     SNAP     450    9126        2e-51   -0.820   yes
cant improvement, and multi-path aggregation (CNTM) further                  LLM      SNAP     462   20552        2e-30   -0.616   yes
improves effectiveness, reaching a Top-1 accuracy of 43%.
                              TABLE VII                                              tional Symposium, NFM 2023, Houston, TX, USA, May 16–18, 2023,
   PAIRWISE M C N EMAR TESTS FOR FILE - LEVEL T OP -1 LOCALIZATION                   Proceedings, (Berlin, Heidelberg), p. 397–413, Springer-Verlag, 2023.
SUCCESS . C OLUMNS REPORT METHODS (M.A, M.B), DISCORDANT PAIRS                  [16] M. D. Ernst, J. H. Perkins, P. J. Guo, S. McCamant, C. Pacheco, M. S.
(D ISC .), A/B CORRECT ONLY (A-O, B-O), p- VALUE , PAIRED ODDS RATIO                 Tschantz, and C. Xiao, “The daikon system for dynamic detection of
                (OR), AND SIGNIFICANCE (S IG ., α = 0.05).                           likely invariants,” Science of Computer Programming, vol. 69, no. 1,
                                                                                     pp. 35–45, 2007. Special issue on Experimental Software and Toolkits.
     M.A       M.B      Disc.     A-O   B-O            p      OR    Sig.        [17] B. Pytlik, M. Renieris, S. Krishnamurthi, and S. P. Reiss, “Automated
     RAND      CNTB       76       24    52     0.00176     0.467   yes              fault localization using potential invariants,” in AADEBUG 2003: Fifth
     RAND      CNTS      143       21   122       2e-18     0.176   yes              International Workshop on Automated and Algorithmic Debugging,
     RAND      CNTM      216       17   199       1e-40     0.088   yes              (Ghent, Belgium), pp. 273–276, Sept. 2003.
     RAND      LLM       270        7   263       2e-68     0.028   yes
                                                                                [18] J. Jones, M. Harrold, and J. Stasko, “Visualization of test information
     RAND      SNAP       56       25    31        0.504    0.810    no
     CNTB      CNTS      105       16    89       2e-13     0.184   yes              to assist fault localization,” in Proceedings of the 24th International
     CNTB      CNTM      186       16   170       1e-33     0.097   yes              Conference on Software Engineering. ICSE 2002, pp. 467–477, 2002.
     CNTB      LLM       276       24   252       4e-49     0.097   yes         [19] R. Abreu, P. Zoeteweij, and A. J. Van Gemund, “An evaluation of sim-
     CNTB      SNAP       62       42    20     0.00715     2.073   yes              ilarity coefficients for software fault localization,” in 2006 12th Pacific
     CNTS      CNTM      111       15    96       1e-15     0.161   yes              Rim International Symposium on Dependable Computing (PRDC’06),
     CNTS      LLM       265       55   210       2e-22     0.264   yes              pp. 39–46, 2006.
     CNTS      SNAP      133      114    19       1e-17     5.872   yes         [20] W. E. Wong, V. Debroy, R. Gao, and Y. Li, “The dstar method for
     CNTM      LLM       208       67   141         3e-7    0.477   yes
                                                                                     effective software fault localization,” IEEE Transactions on Reliability,
     CNTM      SNAP      204      190    14       1e-40    13.138   yes
     LLM       SNAP      268      259     9       7e-65    27.316   yes              vol. 63, no. 1, pp. 290–308, 2014.
                                                                                [21] R. Abreu, P. Zoeteweij, and A. J. van Gemund, “On the accuracy
                                                                                     of spectrum-based fault localization,” in Testing: Academic and In-
                                                                                     dustrial Conference Practice and Research Techniques - MUTATION
                                R EFERENCES                                          (TAICPART-MUTATION 2007), pp. 89–98, 2007.
                                                                                [22] R. Cao, M. Chen, J. Chen, Z. Cui, Y. Feng, B. Hui, Y. Jing, K. Li,
 [1] K. R. M. Leino, “Dafny: An automatic program verifier for functional            M. Li, J. Lin, et al., “Qwen3-coder-next technical report,” arXiv preprint
     correctness,” in Logic for Programming, Artificial Intelligence, and            arXiv:2603.00729, 2026.
     Reasoning (E. M. Clarke and A. Voronkov, eds.), (Berlin, Heidelberg),      [23] R. Gopinath, A. Alipour, I. Ahmed, C. Jensen, and A. Groce, “How
     pp. 348–370, Springer Berlin Heidelberg, 2010.                                  hard does mutation analysis have to be, anyway?,” in 2015 IEEE 26th
 [2] A. Lattuada, T. Hance, C. Cho, M. Brun, I. Subasinghe, Y. Zhou,                 International Symposium on Software Reliability Engineering (ISSRE),
     J. Howell, B. Parno, and C. Hawblitzel, “Verus: Verifying rust programs         pp. 216–227, 2015.
     using linear ghost types,” Proc. ACM Program. Lang., vol. 7, Apr. 2023.    [24] F. Steimann, M. Frenkel, and R. Abreu, “Threats to the validity and
 [3] F. Oliveira, A. Mendes, and C. Carreira, “What challenges do developers         value of empirical assessments of the accuracy of coverage-based fault
     face when using verification-aware programming languages?,” in 2025             locators,” in Proceedings of the 2013 International Symposium on
     IEEE 36th International Symposium on Software Reliability Engineering           Software Testing and Analysis, ISSTA 2013, (New York, NY, USA),
     (ISSRE), pp. 203–214, 2025.                                                     p. 314–324, Association for Computing Machinery, 2013.
 [4] Y. Pei, C. A. Furia, M. Nordio, Y. Wei, B. Meyer, and A. Zeller,           [25] S. Pearson, J. Campos, R. Just, G. Fraser, R. Abreu, M. D. Ernst,
     “Automated fixing of programs with contracts,” IEEE Transactions on             D. Pang, and B. Keller, “Evaluating and improving fault localization,”
     Software Engineering, vol. 40, no. 5, pp. 427–449, 2014.                        in 2017 IEEE/ACM 39th International Conference on Software Engi-
 [5] B. Meyer, “Eiffel**eiffel is a trademark of interactive software engi-          neering (ICSE), pp. 609–620, 2017.
     neering inc.: A language and environment for software engineering,”        [26] E. Mugnier, E. A. Gonzalez, N. Polikarpova, R. Jhala, and Z. Yuanyuan,
     Journal of Systems and Software, vol. 8, no. 3, pp. 199–246, 1988.              “Laurel: Unblocking automated verification with large language mod-
 [6] C. Loughridge, Q. Sun, S. Ahrenbach, F. Cassano, C. Sun, Y. Sheng,              els,” Proc. ACM Program. Lang., vol. 9, Apr. 2025.
     A. Mudide, M. R. H. Misu, N. Amin, and M. Tegmark, “Dafnybench:            [27] Z. Li, L. Yan, Y. Liu, Z. Zhang, and B. Jiang, “Mure: Making use of
     A benchmark for formal software verification,” 2024.                            mutations to refine spectrum-based fault localization,” in 2018 IEEE
 [7] I. Amaral, A. Mendes, and J. Campos, “Mutdafny: A mutation-based                International Conference on Software Quality, Reliability and Security
     approach to assess dafny specifications,” in 2026 IEEE/ACM 48th                 Companion (QRS-C), pp. 56–63, 2018.
     International Conference on Software Engineering (ICSE), 2026.             [28] R. Abreu, P. Zoeteweij, and A. J. van Gemund, “Spectrum-based multi-
 [8] D. Peters and D. Parnas, “Using test oracles generated from program             ple fault localization,” in 2009 IEEE/ACM International Conference on
     documentation,” IEEE Transactions on Software Engineering, vol. 24,             Automated Software Engineering, pp. 88–99, 2009.
     no. 3, pp. 161–173, 1998.                                                  [29] S. Moon, Y. Kim, M. Kim, and S. Yoo, “Ask the mutants: Mutating
 [9] Y. Cheon and G. T. Leavens, “A simple and practical approach to unit            faulty programs for fault localization,” in 2014 IEEE Seventh Inter-
     testing: The jml and junit way,” in ECOOP 2002 — Object-Oriented                national Conference on Software Testing, Verification and Validation,
     Programming (B. Magnusson, ed.), (Berlin, Heidelberg), pp. 231–255,             pp. 153–162, 2014.
     Springer Berlin Heidelberg, 2002.                                          [30] T.-T. Nguyen, Q.-T. Ta, and W.-N. Chin, “Automatic program repair
[10] D. Richardson, O. O’Malley, and C. Tittle, “Approaches to specification-        using formal verification and expression templates,” in Verification,
     based testing,” SIGSOFT Softw. Eng. Notes, vol. 14, p. 86–96, Nov.              Model Checking, and Abstract Interpretation (C. Enea and R. Piskac,
     1989.                                                                           eds.), (Cham), pp. 70–91, Springer International Publishing, 2019.
[11] A. K. Petrenko, “Specification based testing: Towards practice,” in        [31] V. Wu, A. Mendes, and A. Abreu, “Specification-guided repair of
     Perspectives of System Informatics (D. Bjørner, M. Broy, and A. V.              arithmetic errors in dafny programs using LLMs,” in Software Engi-
     Zamulin, eds.), (Berlin, Heidelberg), pp. 287–300, Springer Berlin              neering and Formal Methods: 23rd International Conference, SEFM
     Heidelberg, 2001.                                                               2025, Toledo, Spain, November 10–14, 2025, Proceedings, (Berlin,
[12] B. Meyer, A. Fiva, I. Ciupa, A. Leitner, Y. Wei, and E. Stapf, “Programs        Heidelberg), p. 261–278, Springer-Verlag, 2025.
     that test themselves,” Computer, vol. 42, no. 9, pp. 46–55, 2009.          [32] A. Sullivan, K. Wang, R. N. Zaeem, and S. Khurshid, “Automated test
[13] P. Spettel, “Delfy: Dynamic test generation for dafny,” Master’s thesis,        generation and mutation testing for alloy,” in 2017 IEEE International
     Eidgenössische Technische Hochschule Zürich, 2013.                            Conference on Software Testing, Verification and Validation (ICST),
[14] M. Christakis, K. R. M. Leino, P. Müller, and V. Wüstholz, “Integrated        pp. 264–275, 2017.
     environment for diagnosing verification errors,” in Tools and Algorithms   [33] G. Zheng, T. Nguyen, S. Gutiérrez Brida, G. Regis, M. F. Frias,
     for the Construction and Analysis of Systems (M. Chechik and J.-                N. Aguirre, and H. Bagheri, “Flack: Counterexample-guided fault lo-
     F. Raskin, eds.), (Berlin, Heidelberg), pp. 424–441, Springer Berlin            calization for alloy models,” in 2021 IEEE/ACM 43rd International
     Heidelberg, 2016.                                                               Conference on Software Engineering (ICSE), pp. 637–648, 2021.
[15] A. Fedchin, T. Dean, J. S. Foster, E. Mercer, Z. Rakamarić, G. Reger,     [34] D. Beyer, M. Kettl, and T. Lemberger, “Fault localization on verification
     N. Rungta, R. Salkeld, L. Wagner, and C. Waldrip, “A toolkit for                witnesses,” in Model Checking Software (T. Neele and A. Wijs, eds.),
     automated testing of dafny,” in NASA Formal Methods: 15th Interna-              (Cham), pp. 205–224, Springer Nature Switzerland, 2025.
