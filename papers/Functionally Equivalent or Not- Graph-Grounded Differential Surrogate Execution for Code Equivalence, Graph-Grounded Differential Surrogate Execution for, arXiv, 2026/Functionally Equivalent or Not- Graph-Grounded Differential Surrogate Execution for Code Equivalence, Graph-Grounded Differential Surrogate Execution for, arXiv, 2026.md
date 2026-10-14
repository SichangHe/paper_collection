                                                 Functionally Equivalent or Not?
                                        Graph-Grounded Differential Surrogate Execution for
                                                        Code Equivalence


                                                  Amit Kachroo                           Like Hui                          Haitao Mao
                                                   AWS AI Labs                         AWS AI Labs                        AWS AI Labs
                                            Santa Clara, California, USA        Santa Clara, California, USA       Santa Clara, California, USA
arXiv:2610.04371v1 [cs.AI] 3 Oct 2026




                                              amkachro@amazon.com                 likehui@amazon.com                   maoht@amazon.com

                                                            Yuhao Zhang                                         Nguyen Vo
                                                            AWS AI Labs                                        AWS AI Labs
                                                           New York, USA                                Santa Clara, California, USA
                                                        yhzhangh@amazon.com                                benvox@amazon.com



                                                                                             Abstract
                                                  Determining whether two programs are functionally equivalent or not is central
                                                  not only to code modernization, patch validation, and refactoring, but also to code-
                                                  generation evaluation in general. Yet the usual signals are incomplete: tests cover
                                                  only finite inputs, textual similarity confuses implementation with behavior, and
                                                  unconstrained language model judgments are difficult to audit. Moreover, direct
                                                  execution is often impossible when a program depends on an obsolete, licensed, un-
                                                  available, or unsafe environment. We introduce FEAGENT, a selective equivalence
                                                  assessor agent that combines typed program-graph evidence with differential surro-
                                                  gate execution. FEAGENT first aligns public interfaces and behaviorally relevant
                                                  graph anchors, then issues bounded queries over call-flow, control-flow, data-flow,
                                                  type, import, and effect relations. With this information in context, a branch-aware
                                                  generator agent proposes discriminating inputs, and two blinded language-model
                                                  surrogates independently reason about and predict source and target observables.
                                                  Every claim and predicted divergence is recorded in an evidence ledger. A determin-
                                                  istic reconciler then returns E QUIVALENT, I NEQUIVALENT, or U NCLEAR rather
                                                  than forcing a verdict when paths are uncovered or evidence conflicts. We evaluate
                                                  FEAGENT on function-level equivalence and repository-level bug patches, where
                                                  the existing oracle is a benchmark label or a passing test suite. Every disagreement
                                                  with that oracle is adjudicated by direct execution, revealing errors in benchmark
                                                  labels and behavioral divergences missed by unit-test-only scoring. On EquiBench,
                                                  execution confirms FEAGENT’s disagreements with published labels on 216 of
                                                  1,200 evaluated pairs (18.0%); on SWE-bench Verified, 94 of 331 test-passing
                                                  agent patches (28.4%) diverge from the reference patch. FEAGENT thus serves
                                                  as an audit layer between testing and formal verification, exposing behavioral
                                                  differences that existing oracles miss while keeping its evidence reviewable and its
                                                  uncertainty explicit without claiming a universal proof of equivalence.


                                        1     Introduction
                                        Software engineering repeatedly asks a deceptively simple question: did a change preserve behavior?
                                        The question appears when a patch is compared with a reference fix, a component is ported to a new
                                        language, a legacy system is modernized, or generated code is evaluated. In each case, syntactically

                                        NeurIPS 2026 Workshop on AI for Verifiable Coding.
                                                         Code diff
                                                             ∆
                                 File I/O                        Analysis LLM     File I/O



Source files                                                                                                     Target files

                         Graph tool                                                      Graph tool




                                                          Test data


                           Source LLM                                            Target LLM


          Source graph                                                                                Target graph
                               self-verify                                        self-verify

                                                        Differential
                                                        execution
                         Source execution                                        Target execution



                                                Evidence-aware matcher




                                       Equivalent   /   Inequivalent     /   Unclear

Figure 1: Graph-grounded differential assessment: FEAGENT uses graph evidence to guide
branch-targeting inputs; blinded surrogates independently predict source and target traces, and
deterministic reconciliation returns E QUIVALENT, I NEQUIVALENT, or U NCLEAR judgment.
different programs may be interchangeable, while nearly identical programs may diverge on a single
boundary condition. We therefore care about observable behavior, not textual identity.
The dominant practical oracle is a test suite. Tests are indispensable, but they establish agreement
only on the executed inputs and observations. A patch can pass by exploiting an uncovered shortcut;
a correct alternative can fail because a test encodes an implementation detail. Symbolic and concolic
execution broaden path coverage [Godefroid et al., 2005, Cadar et al., 2008], and translation validation
can prove strong properties for supported transformations [Pnueli et al., 1998, Lopes et al., 2021].
Their applicability, however, depends on executable environments, faithful models of libraries and
side effects, and tractable path conditions. Those assumptions often break for incomplete repositories,
cross-language migrations, legacy runtimes, proprietary dependencies, or unsafe code.
In these settings, large language models (LLMs) offer a complementary capability: they can reason
about code that cannot be run locally and predict execution behavior on concrete inputs [Gu et al.,
2024, Liu et al., 2024a]. But asking a model “are these programs equivalent?” creates a weak
oracle. The model may focus on surface similarity, overlook a distant callee, silently assume a library
contract, or rationalize the two programs jointly. A confident paragraph does not reveal which paths
were checked, which dependency facts support a claim, or what should happen when the evidence is
incomplete.
To address these limitations, this paper studies a more constrained use of model reasoning. We propose
FEAGENT, illustrated in Figure 1, which treats functional equivalence as an evidence acquisition and
selective decision problem. FEAGENT represents the programs as a pair of typed, attributed program
graphs rather than an undifferentiated context window. A structural agent can inspect only bounded
slices and must cite graph nodes, relation paths, and source spans. The behavioral assessment does
not compare the programs directly. Instead, one component proposes inputs from uncovered branch
obligations, while separate and mutually blinded agent surrogates predict the observable trace of
each program. Finally, fixed reconciliation rules distinguish evidence for equivalence, evidence for
divergence, and reasons to abstain.
This design makes the distinction between assessment and proof important. FEAGENT cannot prove
universal equivalence from finitely many queries and model predictions. Instead, it estimates a
scoped relation relative to an explicit input domain and observable schema, exposes its evidence, and


                                                            2
withholds a verdict when coverage or agreement is insufficient. This makes selective risk, especially
the rate of false E QUIVALENT decisions, a more meaningful target than raw forced-choice accuracy.
Bug patching on the other hand provides a high-value application of this assessment. Benchmarks
such as SWE-bench Verified [Jimenez et al., 2024] score candidate patches with repository tests.
FEAGENT adds an orthogonal comparison against the reference behavior. A test-passing candidate
that loses reference behavior is a likely evaluation false positive. A test-failing candidate that remains
behaviorally equivalent is a candidate false negative caused by an overly strict or incidental test.
When a patch adds behavior, we use the term E XTENSION candidate; calling it an “improvement”
requires task intent or human adjudication, not equivalence analysis alone.
Building on this assessment approach and its application to bug patching, the main contributions of
this work are:

       • a formulation of scoped observational equivalence that makes the input domain, observable
         behavior, and environment assumptions explicit, and supports E QUIVALENT, I NEQUIVA -
         LENT, and U NCLEAR judgment rather than forcing a binary decision;
       • FEAGENT, a graph-grounded architecture that aligns behavioral anchors, derives checkable
         obligations, generates branch-targeting inputs, and independently predicts source and target
         traces with mutually blinded surrogates;
       • an auditable decision process in which claims cite graph nodes and source spans, predicted
         mismatches identify a concrete input and observable, and deterministic gates prevent an
         LLM from validating its own evidence; and
       • an execution-grounded evaluation on 1,200 EquiBench pairs [Wei et al., 2025] and 331
         test-passing SWE-bench Verified patches [Jimenez et al., 2024], that confirms 216 of 230
         challenged EquiBench labels and 94 of 109 flagged patch divergences.

2   Related Work

Program equivalence and differential testing. Equivalence is undecidable in general, so practical
systems restrict the language, transformation, or observation boundary. Translation validation checks
a concrete compiler output against its input [Pnueli et al., 1998]; Alive2 proves refinement between
LLVM transformations [Lopes et al., 2021]. Differential testing compares multiple implementations
on generated inputs [McKeeman, 1998], while DART and KLEE combine concrete and symbolic
execution to discover path-sensitive failures [Godefroid et al., 2005, Cadar et al., 2008]. These
approaches are stronger than surrogate reasoning when their execution model applies. FEAGENT
targets the complementary setting in which direct execution or complete symbolic models are
unavailable. We evaluate its assessments against execution whenever execution is possible.
Code representations and graph-grounded models. Code property graphs unify syntax, control
flow, and data flow for program analysis [Yamaguchi et al., 2014]. Learned code models also benefit
from structural relations: GraphCodeBERT incorporates data flow [Guo et al., 2021], while repository
systems such as RepoGraph and CodexGraph use graph retrieval to support software-engineering
agents [Ouyang et al., 2025, Liu et al., 2024b]. Our goal differs from repository question answering or
patch generation: we use graph structure to define comparison anchors, derive coverage obligations,
restrict model queries, and make every equivalence claim traceable to program evidence.
LLM execution and code reasoning. CRUXEval measures input/output code reasoning [Gu et al.,
2024], CodeMind studies independent execution and consistency reasoning [Liu et al., 2024a], and
recent work directly benchmarks semantic code equivalence [Maveli et al., 2025]. EquiBench collects
human-written and transformed function pairs across several languages and equivalence categories
[Wei et al., 2025]. These works show both the promise and fragility of model-based execution.
FEAGENT builds on this capability by combining it with repository graphs, cross-program blinding,
structured observables, and selective decision rules.
Patch evaluation and selective prediction. SWE-bench Verified evaluates repository-level issue
resolution [Jimenez et al., 2024], and SWE-agent demonstrates the importance of the agent–computer
interface [Yang et al., 2024]. Tests remain the primary oracle for patch evaluation, although they can
under-specify intent or reject legitimate implementations. We therefore position equivalence evidence


                                                    3
as a second audit layer, not a replacement for tests. Within this layer, our U NCLEAR outcome follows
the principle of selective classification: a system should trade coverage for lower conditional error
instead of forcing uncertain predictions [Geifman and El-Yaniv, 2017]. This trade-off is especially
important because a false equivalence claim can conceal a regression.

3     Problem Formulation

Scoped observational equivalence. We compare a source program Ps and a target program Pt at
aligned entry points. The comparison is defined by an explicit assessment specification
                                         Σ = (D, O, Γ, τ ),
where D is the admissible input domain, O specifies the caller-observable behavior to compare, Γ
states assumptions about external dependencies and state, and τ defines the resource policy for time-
outs and termination. An element x ∈ D denotes one logical invocation, including explicit arguments
and relevant initial state. If the programs expose different concrete APIs or data representations, the
task manifest supplies fixed adapters from this logical invocation to each side.
Under this specification, the ideal equivalence relation is
                                                                        
                    Ps ≡Σ Pt , ∀x ∈ D : O [[Ps ]]Γ,τ (x) = O [[Pt ]]Γ,τ (x) .                      (1)
The observable projection includes the return value, exception behavior, external effects, mutations
of caller-reachable objects, and termination status. Each enabled field has a declared comparator,
such as exact equality, tolerance-bounded numeric equality, canonicalized collection equality, or an
application-specific projection.
Equation (1) makes the scope of a claim explicit. Behavior outside D is not automatically a coun-
terexample; internal implementation details matter only when exposed by O; and calls into libraries,
services, files, databases, or clocks are interpreted under Γ. The specification must be fixed indepen-
dently of the assessment, so it cannot be changed after observing a disagreement.
Selective assessment. Universal program equivalence is undecidable in general, and finite model
predictions cannot prove Equation (1). We therefore seek a bounded, evidence-backed decision:
                   h(Ps , Pt , Σ) ∈ {E QUIVALENT, I NEQUIVALENT, U NCLEAR}.
FEAGENT returns this verdict together with cited evidence and an assessment confidence score. A
I NEQUIVALENT verdict requires a supported structural contradiction or a stable behavioral mismatch
for an input in D. A E QUIVALENT verdict requires coverage of all mandatory comparison obligations
without a known contradiction. When alignment, dependency behavior, path coverage, or surrogate
predictions remain unresolved, the correct output is U NCLEAR rather than a forced judgment. Thus,
E QUIVALENT denotes support under the declared scope and finite assessment budget, not a universal
proof.
Patch-specific interpretation. When Ps is the program with a reference patch and Pt is the program
with a candidate patch, equivalence means that the candidate preserves the reference observables
under Σ. A supported loss or change of required reference behavior is a R EGRESSION candidate.
Additional candidate behavior not represented by the reference is an E XTENSION candidate. Whether
an extension is desirable cannot be decided from equivalence alone; it additionally requires the issue
specification, tests, or human review.

4     FEAGENT
FEAGENT has five phases: graph construction, alignment and obligation extraction, bounded struc-
tural evidence channel, two-channel evidence acquisition, and deterministic reconciliation. Ap-
pendix B gives the complete graph and observable schemas.

4.1   Typed, attributed program-pair graph

For each program, we construct graph G = (V, E, A), where nodes, V , represent repository, file,
namespace, type, function, parameter, statement, variable, literal, and external-symbol entities.


                                                  4
 Before: frequency-only validation                     After: exact-value validation
  1   from collections import Counter                   1   n = int(input())
                                                        2   A = sorted(map(int, input().split()))
  3 n = int(input())
  4 a = list(map(int, input().split()))                 4 if n % 2 == 1:
  5 c = Counter(a)                                      5     ex = [0]
  6 d = list(c.values())                                6     for i in range(n // 2):
                                                        7         a = 2 * (i + 1)
  8 if (                                                8         ex += [a, a]
  9     n % 2 == 1                                      9 else:
 10     and c[0] == 1                                  10     ex = []
 11     and d.count(2) == (n - 1) // 2                 11     a = 1
 12     or n % 2 == 0                                  12     for i in range(n // 2):
 13     and d.count(2) == n // 2                       13         ex += [a, a]
 14 ):                                                 14         a += 2
 15     print(pow(2, n // 2, 10**9 + 7))
 16 else:                                              16 ans = 0
 17     print(0)                                       17 if A == ex :
                                                       18     ans = 2**(n // 2) % (10**9 + 7)
                                                       19 print(ans)


Figure 2: Combined algorithm–data divergence (OJ-VA case 370): For n = 4 and [0, 0, 2, 2],
multiplicity-only validation discards the Counter keys and returns 4, whereas exact sequence
validation rejects the values and returns 0.
Directed edges, E encode CONTAINS, DECLARES, CALLS, IMPORTS, INHERITS, OVERRIDES,
control-flow successors, def–use links, reads, writes, returns, throws, and externally visible effects.
Attributes, A, retain language, type, signature, source span, branch predicate, symbol resolution
status, and parser confidence. The graph is deliberately loss-aware: an unresolved call is an explicit
node rather than a silently missing edge.
The graph serves two roles, 1) It compresses repository context into behaviorally meaningful neigh-
borhoods, and 2) it defines what the assessor has and has not inspected. Every query records its graph
version, seed nodes, edge types, depth or budget, returned nodes, and source spans. Evidence can
therefore be replayed after a graph or program update.

4.2    Anchor alignment and proof obligations

We first align declared entry points using qualified names, signatures, type compatibility, docu-
mentation, and call-context similarity. We then expand from each entry point to find behavior
anchors:

        • public inputs, outputs, exceptions, mutations, and effectful calls;
        • branch and loop predicates that can change an observable;
        • transitive callees and data dependencies on an observable path; and
        • environment assumptions, including unresolved external symbols.

Cross-program candidate anchors are scored from symbol, type, role, and local graph context.
Ambiguous many-to-many alignments remain explicit.
The aligned anchors induce a set of obligations, B = Binterface ∪ Bcontrol ∪ Bdata ∪ Beffects ∪
Benvironment . An obligation is not a proof theorem; it is a checkable question such as “do both
programs reject a zero denominator with the same observable exception?”, “can this write reach the
returned object?”, or “does the target preserve the source’s overflow guard?” Each obligation has
status SUPPORTED, CONTRADICTED, UNRESOLVED, or OUT- OF - SCOPE.
Figure 2 illustrates why algorithmic and data obligations must be considered together: a frequency-
based rewrite changes both the validation procedure and the exact values retained for the final
comparison.

4.3    Bounded structural evidence channel

The structural analyst receives Σ, the aligned anchors, and a graph query API. It does not receive
a flattened repository. Available operations include bounded neighborhood expansion, typed path


                                                   5
search, callers/callees, control dependence, backward data slices, symbol lookup, and source retrieval
for returned nodes. A response is accepted into the ledger only if it contains:
              e = (claim, polarity, node IDs, relation path, source spans, assumptions).
Unsupported prose is discarded. Query depth, result count, and total tokens are bounded; hitting a
bound marks the affected obligation unresolved.
The analyst compares behavioral roles, not graph isomorphism. Different loop forms or helper
decompositions can support equivalence when their observable slices agree. Conversely, a one-token
predicate change can contradict an obligation even when the surrounding graphs align.

4.4   Differential surrogate execution

Branch-aware input proposals. The input generator converts uncovered control and data obligations
into typed input constraints. It proposes ordinary cases, boundary values, values immediately around
branch thresholds, aliasing and mutation cases, empty and singleton structures, exceptional inputs
permitted by D, and combinations that distinguish mismatched predicates. Each proposal identifies
the targeted obligation and includes a rationale. Proposals are de-duplicated using canonical typed
representations rather than string equality.
Blinded simulation. For every x ∈ X , separate source and target surrogates receive only one
program slice, the same input, the observable schema, and relevant environment contracts. They
predict a structured trace
                                       TP (x) = (r, e, s, m, t, π),
where r is the return value, e the exception, s external side effects, m reachable-parameter mutations,
t termination status, and π a stepwise trace anchored to graph nodes. Neither surrogate sees the
other program or prediction. This prevents the common failure mode in which a joint judge assumes
agreement and bends both explanations toward that prior.
Each prediction undergoes a self-verification pass that checks type consistency, branch feasibility,
trace-to-graph citations, and agreement between the claimed path and final observables. We sample
repeated predictions only where the initial trace is low-confidence or self-inconsistent. Persistent
within-program disagreement marks the case unresolved rather than selecting the majority answer
without qualification.
Observable comparison. A non-generative comparator applies the field-specific rules in O. It
returns MATCH, MISMATCH, or UNKNOWN per field. A mismatch record contains the concrete input,
the first divergent observable, both predicted values, cited trace nodes, and any assumptions. The
comparator does not infer intent and cannot relabel an extension as an improvement.

4.5   Deterministic reconciliation and confidence

Reconciliation is ordered to privilege identifiable failures over broad similarity:
1. Validity gate. If required graphs, entry-point alignments, or observable comparators are missing,
   return U NCLEAR.
2. Contradiction gate. Return I NEQUIVALENT when a structurally supported interface contradiction
   or a stable behavioral mismatch lies inside D and does not depend on an unresolved environment
   fact.
3. Conflict gate. If the structural and behavioral channels disagree, or repeated simulations are
   unstable, return U NCLEAR and retain the conflict.
4. Coverage gate. Return E QUIVALENT only if every mandatory obligation is supported or be-
   haviorally exercised, no contradiction exists, and aggregate confidence exceeds the acceptance
   threshold.
5. Otherwise return U NCLEAR with the remaining obligations.
Confidence is computed from observable-comparison stability, obligation coverage, graph resolution
quality, and evidence completeness. It is calibrated on a development partition and frozen before test
evaluation. The threshold is swept for risk–coverage analysis; one operating point is selected from a
preregistered upper bound on false-equivalence risk. No LLM is asked to override these gates.


                                                   6
5     Benchmarking Results
We evaluate the reliability and utility of FEAGENT through four questions:
• RQ1: Are disagreements with benchmark labels genuine label errors or FEAGENT errors?
• RQ2: Can FEAGENT find execution-confirmed behavioral divergences in test-passing patches?
• RQ3: Do generated witnesses turn predicted discrepancies into execution-confirmed divergences?
• RQ4: How does graph context help localize observable differences and the paths that reach them?
We study RQ1 and RQ3 on EquiBench (Section 5.3) and RQ2 on SWE-bench Verified (Section 5.4).
We address RQ4 through an execution-verified SWE-bench Verified case study (Section 5.5); a
quantitative graph ablation remains future work.
Model configuration. All model-backed components of FEAGENT in the reported experiments used
Claude Opus 4.6 with a 32,000-token thinking budget and prompt caching enabled.

5.1   Benchmarks

We use EquiBench [Wei et al., 2025] to audit labeled program pairs and SWE-bench Verified [Jimenez
et al., 2024] to audit test-passing patches. Our EquiBench evaluation covers the Python OJ_A, OJ_V,
and OJ_VA subsets; Appendix Table 4 reports their composition. We exclude the C/DCE, CUDA,
and x86-64 subsets because our current graph front end does not support them. Section 5.4 describes
the SWE-bench Verified construction and execution audit.

5.2   Evaluation metrics

Published labels can be wrong, so accuracy against them conflates method and label errors. We
instead report three execution-grounded metrics:
• Disagreement Rate (DR): fraction of pairs where FEAGENT disagrees with the label; U NCLEAR
  counts because it does not confirm the label.
• Verified Genuine (VG): fraction of disagreements confirmed as label errors or execution-confirmed
  divergence.
• Execution-confirmed Divergence (ECD): fraction of all evaluated cases for which FEAGENT
  identifies a divergence that direct execution confirms.
Let P be all pairs, S the disagreements or say the inequivalent flags, and D(S) = {i ∈ S : div(i)}
the execution-confirmed divergences in set S. Then
                               |S|             |D(S)|              |D(S)|
                        DR =        ,   VG =          ,   ECD =           ,                         (2)
                               |P |              |S|                 |P |

5.3   Label quality verification

To answer RQ1, and as Section 5.2 anticipated, ground-truth labels can be unreliable. For every pair
where FEAGENT disagrees with the provided label, we apply the asymmetric verification behind the
verified-as-genuine metric:
• Label equivalent, prediction inequivalent. We produce at least one concrete input on which the
  “before” and “after” programs yield different outputs and execute it in a real environment to confirm
  the divergence.
• Label inequivalent, prediction equivalent. We attempt to reproduce the labeled divergence
  by executing both programs on inputs derived from FEAGENT’s reasoning trace. If no input
  reproduces it, the evidence is inconclusive; we retain the original label and count the pair as a
  method failure.
Table 1 combines the EquiBench label-quality results with the SWE-bench Verified execution audit.
OJ_A and OJ_VA show high disagreement rates (29% and 27.25%) paired with very high verification
rates (95.7% and 96.3%), indicating that the vast majority of disagreements stem from incorrect
ground-truth labels rather than from FEAGENT errors.


                                                  7
 Before: exact long division                           After: floating-point conversion
  1   import sys                                        1   while True:
  2   f = sys.stdin                                     2       try:
                                                        3           a, b, n = map(int, input().split())
  4 for line in f:                                      4       except:
  5     a, b, n = map(int, line.split())                5           break
  6     s = 0
  7     for i in range(n):                              7       s = str(a/b)
  8         a = a % b * 10                              8       sum = 0
  9           s += a // b % 10                          9       x = s.index(".")+1
 10       print(s)                                     10       for i in s[x:x+n]:
                                                       11           sum += int(i)

                                                       13       print(sum)

Figure 3: Algorithmic divergence from numeric semantics (OJ-A case 10): For a benchmark-
labeled equivalent pair, a = 10, b = 3, and n = 16 produce 48 versus 50: replacing exact long
division with rounded floating-point conversion changes the digit sum.

Table 1: Execution-grounded audit on EquiBench and SWE-bench Verified. ECD = execution-
confirmed divergences / evaluated cases as defined in 2. On SWE-bench Verified we evaluate the 331
instances resolved (i.e. every patch passes its tests) by mini-SWE-agent with GPT-OSS-120B.

                Audit Set            Evaluated Disagreement Rate Verified Genuine ECD
                OJ_A                   400       116 (29%)            111 (95.7%)         27.8%
                OJ_VA                  400      109 (27.25%)          105 (96.3%)         26.3%
                OJ_V                   400        5 (1.25%)             0 (0%)             0%
                EquiBench Total       1,200      230 (19.2%)          216 (93.9%)         18.0%
                SWE-bench Verified     331       109 (32.9%)          94 (86.2%)          28.4%

Again, in each confirmed case we found at least one concrete input on which the “before” and “after”
programs produce different outputs and executed the code to validate the agent’s reasoning. OJ_V, by
contrast, has a low disagreement rate (1.25%) and none of its disagreements were genuine mislabels.
Across all 1,200 evaluated EquiBench pairs, ECD is 18.0% (216/1,200): at least this fraction of pairs
carries a published label contradicted by an executed counterexample.
Figures 2, 3 and 4, give representative execution-verified disagreements, including combined algo-
rithm with variable divergences algorithmic divergences, and variable-level divergences.

5.4    SWE-bench Verified regression audit

We generate candidate fixes for the 500 SWE-bench Verified issues [Jimenez et al., 2024] with
mini-SWE-agent [Yang et al., 2024], retaining 331 patches that pass all tests. We compare each with
its reference patch, and FEAGENT flags 109 (32.9%) as inequivalent. For each flag, its reasoning
trace guides an adversarial input that we execute against both revisions in separate subprocesses.
Execution confirms 94 flags (86.2%); 14 do not reproduce because the change is compensated
elsewhere, unreachable, or observably equivalent, and one remains inconclusive. Since all 331
candidates passed the tests, the 94 confirmed divergences give an execution-confirmed divergence
yield of 94/331 = 28.4% (Table 1).

5.5    Value of surrogate execution and code graph

EquiBench’s self-contained programs make each generated witness directly checkable. For a chal-
lenged pair, the branch-aware generator targets an unresolved control or data obligation, and blinded
surrogates predict each program’s trace independently. Executing the proposed input confirmed every
disagreement counted as genuine, converting a predicted discrepancy into a reproducible counterex-
ample. Figures 2 , 3, and 4 illustrate combined- boundary and algorithm, boundary-reference and
algorithmic failures. This establishes practical value; causal attribution requires a matched ablation.
Figure 5 shows why graph context matters when return values match. The slice links
RenameContentType._rename to the effectful clear_cache call and its router, lookup, and
save guards. This guides generation of an existing content type with a successful save, reaching


                                                   8
    Before: clamped index references                             After: explicit neighbor references
    1 H, W = map(int, input().split())                           1 H, W = map(int, input().split())
    2 canvas = []                                                2 L = [’.’ + input() + ’.’ for A in range(H)]
    3 for i in range(H):                                         3 L = [’.’ * (W + 2)] + L + [’.’ * (W + 2)]
    4     canvas.append(list(input()))
                                                                 5 for i in range(1, H + 1):
  6 for i in range(H):                                           6     for j in range(1, W + 1):
  7     for j in range(W):                                       7         if L[i][j] == ’#’:
  8         cnt = 0                                              8             l = [
  9         if canvas[i][j] == ’#’:                              9                  L[i-1][j],
 10             for h in range(-1, 2):
                                                                10                  L[i+1][j],
 11                 for w in range(-1, 2):
 12                     row = min(max(i+h, 0), H - 1)           11                  L[i][j-1],
 13                     col = min(max(j+w, 0), W - 1)           12                  L[i][j+1]
 14                     if (                                    13             ]
 15                          canvas[row][col] == ’#’            14             if ’#’ not in l:
 16                          and                                15                  print(’No’)
 17                          (abs(h) + abs(w)) % 2 == 1         16                  break
 18                     ):                                      17     else:
 19                          cnt += 1                           18         continue
 20             if cnt == 0:                                    19     break
                                                                20 else:
 21                 print(’No’)
 22                 exit()                                      21     print(’Yes’)
 23 print(’Yes’)



Figure 4: Boundary-reference divergence (OJ-VA case 288): On {#.., ..., ...}, boundary
clamping makes the corner cell count itself as a neighbor and output Yes, whereas padded neighbor
references correctly output No.
clear_cache() in the reference and clear_cache(using=’default’) in the candidate. Inputs
taking the not-found or integrity-error branches never reach the call. The graph thus provides both
the observable effect and its reachability conditions, although quantitative attribution still requires an
ablation.

 (a) Graph slice of _rename                               (b) Witness: content type exists, save succeeds
           router denies       allow_migrate_model                   Reference                         Candidate
                                                               clear_cache()             clear_cache(using='default')
          DoesNotExist          get_by_natural_key
                                                                 returns None       =                  returns None
        IntegrityError          content_type.save
                                                               clears all aliases   ̸=           clears 'default' only
         witness path
                                 clear_cache(...)         ⇒ Inequivalent: identical returns hide a cache-state divergence
         never reaches call


Figure 5: Graph-guided divergence in django-11066. (a) Only guard-satisfying inputs reach
clear_cache. (b) Both revisions return None, but the candidate clears only the default alias.

6      Discussion and Conclusion

Findings. The evidence supports a focused conclusion: FEAGENT is an effective second oracle for
finding behavioral differences missed by benchmark labels and unit tests. Direct execution confirmed
216 of 230 EquiBench disagreements and 94 of 109 divergences flagged among test-passing SWE-
bench Verified patches. As a fraction of all evaluated cases, this gives an ECD of 18.0% (216/1,200)
on EquiBench and 28.4% (94/331) on SWE-bench Verified, where every evaluated patch had already
passed its tests. On SWE-bench Verified, more than one quarter of test-passing patches therefore hide
an execution-confirmed divergence from the reference patch.
Scope and limitation. FEAGENT is a selective audit layer, not a formal verifier. A I NEQUIVALENT
verdict prioritizes a concrete candidate counterexample, E QUIVALENT requires covered obligations
without a stable contradiction, and U NCLEAR exposes missing evidence. Surrogate traces only
propose witnesses: every divergence we report was reproduced by direct execution, and it holds
only within the declared input domain, observables, and environment contract. Incomplete graphs,
unresolved symbols, and surrogate errors can still lead FEAGENT to miss a divergence or abstain.
Conclusion. By combining graph-grounded obligations, blinded surrogate execution, and deter-
ministic reconciliation, FEAGENT turns model reasoning into concrete, inspectable evidence while
keeping uncertainty explicit. The results show that this audit layer can expose substantial blind spots
in labels and unit tests while direct execution prevents unsupported relabeling. The next priorities are
matched-budget component ablations and execution audits of unflagged cases.


                                                           9
References
Cristian Cadar, Daniel Dunbar, and Dawson Engler. KLEE: Unassisted and automatic generation
  of high-coverage tests for complex systems programs. In 8th USENIX Symposium on Operating
  Systems Design and Implementation, 2008.
Yonatan Geifman and Ran El-Yaniv. Selective classification for deep neural networks. In Advances
  in Neural Information Processing Systems, 2017.
Patrice Godefroid, Nils Klarlund, and Koushik Sen. DART: Directed automated random testing. In
  Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implemen-
  tation, 2005.
Alex Gu, Baptiste Roziere, Hugh Leather, Armando Solar-Lezama, Gabriel Synnaeve, and Sida I.
  Wang. CRUXEval: A benchmark for code reasoning, understanding and execution. In Proceedings
  of the 41st International Conference on Machine Learning, 2024.
Daya Guo, Shuo Ren, Shuai Lu, Zhangyin Feng, Duyu Tang, Shujie Liu, Long Zhou, Nan Duan,
  Alexey Svyatkovskiy, Shengyu Fu, Michele Tufano, Shao Kun Deng, Colin Clement, Dawn Drain,
  Neel Sundaresan, Jian Yin, Daxin Jiang, and Ming Zhou. GraphCodeBERT: Pre-training code
  representations with data flow. In International Conference on Learning Representations, 2021.
Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik
  Narasimhan. SWE-bench: Can language models resolve real-world GitHub issues? In International
  Conference on Learning Representations, 2024.
Changshu Liu, Yang Chen, and Reyhaneh Jabbarvand. CodeMind: Evaluating large language models
  for code reasoning. arXiv preprint arXiv:2402.09664, 2024a.
Xiangyan Liu, Bo Lan, Zhiyuan Hu, Yang Liu, Zhicheng Zhang, Fei Wang, Michael Shieh, and
  Wenmeng Zhou. CodexGraph: Bridging large language models and code repositories via code
  graph databases. arXiv preprint arXiv:2408.03910, 2024b.
Nuno P. Lopes, Juneyoung Lee, Chung-Kil Hur, Zhengyang Liu, and John Regehr. Alive2: Bounded
  translation validation for LLVM. In Proceedings of the 42nd ACM SIGPLAN International
  Conference on Programming Language Design and Implementation, 2021.
Nickil Maveli, Antonio Vergari, and Shay B. Cohen. What can large language models capture
  about code functional equivalence? In Findings of the Association for Computational Linguistics:
  NAACL 2025, pages 6880–6918. Association for Computational Linguistics, 2025. doi: 10.18653/
  v1/2025.findings-naacl.382.
William M. McKeeman. Differential testing for software. Digital Technical Journal, 10(1):100–107,
 1998.
Siru Ouyang, Wenhao Yu, Kaixin Ma, Zilin Xiao, Zhihan Zhang, Mengzhao Jia, Jiawei Han,
  Hongming Zhang, and Dong Yu. RepoGraph: Enhancing AI software engineering with repository-
  level code graph. In International Conference on Learning Representations, 2025.
Amir Pnueli, Michael Siegel, and Eli Singerman. Translation validation. In Bernhard Steffen,
 editor, Tools and Algorithms for the Construction and Analysis of Systems, volume 1384 of
 Lecture Notes in Computer Science, pages 151–166, Berlin, Heidelberg, 1998. Springer. doi:
 10.1007/BFb0054170.
Anjiang Wei, Jiannan Cao, Ran Li, Hongyu Chen, Yuhui Zhang, Ziheng Wang, Yuan Liu, Thiago S.
  F. X. Teixeira, Diyi Yang, Ke Wang, and Alex Aiken. EquiBench: Benchmarking large language
  models’ reasoning about program semantics via equivalence checking. In Proceedings of the
  2025 Conference on Empirical Methods in Natural Language Processing, pages 33868–33881.
 Association for Computational Linguistics, 2025. doi: 10.18653/v1/2025.emnlp-main.1718.
Fabian Yamaguchi, Nico Golde, Daniel Arp, and Konrad Rieck. Modeling and discovering vulnera-
  bilities with code property graphs. In 2014 IEEE Symposium on Security and Privacy, 2014.
John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan,
  and Ofir Press. SWE-agent: Agent-computer interfaces enable automated software engineering.
  arXiv preprint arXiv:2405.15793, 2024.


                                               10
A     Artifact and Protocol Details
A.1   End-to-end assessment procedure

The assessment follows the same ordered procedure for every pair. Run-level settings are recorded
before evaluation and held fixed within each benchmark suite. Capitalized returns are machine-
readable verdicts with typed reason codes.

1. Parse Ps and Pt with language-specific front ends. Build Gs and Gt and record unresolved
   symbols. If either required entry point cannot be represented, return A BSTAIN :G RAPH FAILURE.
2. Load Σ = (D, O, Γ, τ ) from the task manifest. Check that every observable has a comparator.
   Otherwise return A BSTAIN :I NCOMPLETE S PECIFICATION.
3. Align entry points and behavior anchors. If a mandatory alignment is ambiguous after the query
   budget, return A BSTAIN :A LIGNMENT.
4. Extract interface, control, data, effect, and environment obligations. Run the structural analyst
   through the bounded graph API. Reject ledger entries without valid node IDs, paths, and spans.
5. Generate typed inputs targeting unresolved obligations. Canonicalize and deduplicate them. Inputs
   outside D may be retained for a separate robustness analysis but cannot determine the primary
   verdict.
6. Independently simulate each program on each input. Apply the self-verification pass described in
   Appendix C.4 to validate the trace schema, branch feasibility, types, and citations. Re-sample only
   cases selected by the predefined instability rule.
7. Compare observable fields with deterministic comparators. Record the first mismatch and all
   unknown fields.
8. Apply the ordered gates in Section 4.5. Emit the verdict, confidence, obligation matrix, evidence
   ledger, token/query usage, and all abstention reasons.

A.2   Run and audit records

A reproducible run record contains the graph front end and language version, model identifier
and access date, decoding policy, graph-query and token budgets, maximum generated inputs,
simulation repetition rule, and direct execution timeout and resource policy. The corresponding
pair record contains immutable source and target identifiers; the scoped specification Σ; entry-point
alignments; graph-resolution warnings; extracted obligations; generated inputs; source and target
traces; comparator outputs; the first mismatching observable, if any; cited graph evidence; and the
final verdict with every abstention or unresolved reason. Keeping configuration, proposed evidence,
and observed outcomes separate prevents an incomplete run from being mistaken for an equivalent
result.

B     Graph and Evidence Schemas
B.1   Evidence-ledger record

Each record is serialized as:

{
    "obligation_id": "...",
    "channel": "structural | source_sim | target_sim | comparator",
    "claim": "...",
    "polarity": "support | contradict | unresolved",
    "graph_version": "...",
    "node_ids": ["..."],
    "relation_path": ["CALLS", "CONTROL_DEPENDS", "..."],
    "source_spans": [{"file": "...", "start": ..., "end": ...}],
    "input_id": "...",
    "observable_field": "...",


                                                 11
     "assumptions": ["..."],
     "confidence_components": {"...": ...}
}
The artifact validator rejects dangling node IDs, spans outside the frozen source snapshot, relation
paths absent from the graph, and observable fields not declared in O.

Table 2: Minimum typed program-graph schema. Front ends may add language-specific nodes and
relations, but cannot silently omit unresolved entities.

    Family                  Required values                      Core attributes
    Nodes                   repository, file, namespace, type,   stable ID, language, qualified name, source span,
                            function, parameter, statement,      parser confidence
                            variable, literal, external symbol
    Structural edges        contains, declares, imports,         source, target, resolution status
                            inherits, overrides
    Behavioral edges        calls, CFG successor,                source, target, guard/label, static/dynamic confi-
                            control-depends, defines, uses,      dence
                            reads, writes, returns, throws,
                            mutates, emits effect
    Function attributes     signature, visibility, modifiers,    normalized and original forms
                            return type, effect summary
    Statement attributes    syntax kind, branch predicate,       source text hash and span
                            constants, operators
    External attributes     package/module, version              resolved, unresolved, or assumed
                            constraint, contract source


Table 3: Observable fields and default comparison behavior. Every task manifest explicitly enables,
disables, or overrides each field.

    Field                     Representation                             Default comparator
    Return                    typed, canonical value                     exact after type-aware canonicalization;
                                                                         declared tolerance for floating point
    Exception                 type, message projection, phase            exact type; configurable message projec-
                                                                         tion
    External effects          ordered events over files, network,        order-sensitive unless specification de-
                              database, logs, processes, callbacks       clares commutativity
    Input mutation            before/after reachable object              structural equality with alias identities re-
                              projection                                 tained
    Persistent state          selected state projection                  task-defined equality
    Termination               normal, exception, timeout,                exact class under resource policy τ
                              divergence



C       Agent Contracts and Information Boundaries
The implementation may phrase prompts differently across model providers, but the following
role separation, information boundaries, and machine-readable outputs are invariant. In particular,
a blinded surrogate never sees the other program or its prediction, and no model may override
deterministic reconciliation.
Model-use scope. Models are used to analyze graph-grounded obligations, propose discriminating
inputs, predict one program’s trace at a time, and check trace consistency. They do not directly certify
a benchmark label or amend it: deterministic comparators produce the method verdict, and direct
execution supplies every reported verification result. The run record binds each model output to the
exact model identifier, provider revision or access date, and decoding configuration.

C.1         Structural analyst
              Role: assess one comparison obligation using only the supplied graph query API. Do not
              claim whole-program equivalence.


                                                          12
          Inputs: scoped specification, aligned anchors, unresolved obligation, remaining query
          budget.
          Requirements: query before concluding; distinguish code fact from environment assump-
          tion; cite every supporting node, path, and source span; mark missing or ambiguous relations
          unresolved.
          Output: obligation ID, status {SUPPORTED, CONTRADICTED, UNRESOLVED, OUT- OF -
          SCOPE}, concise claim, evidence records, assumptions, and suggested discriminating inputs.


C.2    Branch-aware input generator
          Role: propose valid inputs likely to distinguish the programs or cover an unresolved
          obligation.
          Inputs: input types and preconditions, aligned branch predicates, constants and operators,
          data dependencies, already covered cases.
          Requirements: include ordinary and boundary values; target both sides of a predicate;
          preserve cross-parameter constraints; do not invent invalid objects; identify the targeted
          obligation; do not predict either output.
          Output: canonical typed input, construction steps, targeted obligation, relevant graph nodes,
          expected path constraints, and validity rationale.


C.3    Blinded execution surrogate
          Role: predict the observable execution of exactly one program on the given input. You are
          not told whether the program is the source or target and you do not see another program’s
          prediction.
          Inputs: one program slice, graph neighborhood, input, environment contracts, resource
          policy, and observable schema.
          Requirements: trace values and control decisions step by step; cite nodes for each decisive
          step; report unresolved external behavior rather than guessing; include mutations and side
          effects even when the return value matches; check the final value against the trace.
          Output: trace events, return, exception, effects, mutations, termination, unresolved assump-
          tions, citations, and fieldwise confidence.


C.4    Trace verifier
          Role: find internal inconsistencies in a proposed trace, not rewrite it into a preferred answer.
          Checks: input and intermediate types; branch feasibility; definition before use; called-
          function contract; trace-to-node citation; final observable; missed mutation/effect; depen-
          dence on an unresolved symbol.
          Output: VALID, INVALID, or UNCERTAIN, with localized errors. An invalid trace is
          re-simulated without revealing a prediction from the other program.


D     Benchmark and Execution-Verification Details

    Table 4: EquiBench subsets used in the study. Equiv./Inequiv. give the published class balance.

              Dataset    Language      Pairs    Equiv.    Inequiv.    Labeling source
              OJ_A       Python         400      200          200     EquiBench [Wei et al., 2025]
              OJ_V       Python         400      200          200     EquiBench [Wei et al., 2025]
              OJ_VA      Python         400      200          200     EquiBench [Wei et al., 2025]



D.1    Pair manifest

Every comparison is represented by a manifest containing stable source and target revisions; entry
points; D, O, Γ, and τ ; expected language/toolchain; provenance; published label if any; split key;
execution availability; and hashes of all code and tests. For SWE-bench Verified, the manifest
additionally records the issue ID, reference and candidate patch identifiers, test command and
outcome, isolated execution harness, and any generated counterexample.


                                                         13
D.2   Execution-grounded verification

A surrogate trace proposes a witness; it is not the verification oracle. Every reported disagreement is
audited against immutable program revisions as follows:
1. Check that the proposed input lies in D and that the differing field is enabled by O.
2. Execute both sides under the same recorded environment contract and resource policy. Return
   values, exceptions, selected mutations, and effects are serialized with the comparators in Table 3.
3. Classify the audit as confirmed only when direct observations reproduce an in-scope difference;
   otherwise record not reproduced or inconclusive, together with the failed precondition, unreachable
   path, unresolved symbol, timeout, or harness limitation.
Verification is intentionally asymmetric. If an EquiBench pair labeled equivalent yields an executed
counterexample, the published label is demonstrably incorrect for the declared scope. If a pair labeled
inequivalent does not yield a counterexample, the absence of one does not prove equivalence; we
retain the published label and count the disagreement against FEAGENT. For SWE-bench Verified, an
executed difference establishes non-equivalence to the reference patch, but does not by itself establish
that the candidate violates the issue intent. This distinction prevents reference-patch divergence from
being silently promoted to a task-level correctness judgment.

D.3   Audit trail and failure attribution

Each challenged pair retains the published label or test status, method verdict, proposed witness,
graph citations, predicted traces, direct observations, first mismatching observable, verification status,
and reason codes. Original benchmark labels are never overwritten; any corrected interpretation is
stored as a provenance-preserving amendment.
Unconfirmed and unresolved cases are attributed to the component that blocks the claim: graph
construction or symbol resolution; invalid or out-of-domain input; infeasible surrogate trace; nonlocal
compensation in the full patch; unsupported environment behavior; execution-harness failure; or an
ambiguous specification. This record separates benchmark defects from method errors and from
cases that available evidence cannot decide.

E     Claim Boundaries, Safety, and Reproducibility

What the evidence establishes. A concrete, execution-confirmed counterexample establishes
inequivalence for the declared domain, observables, and environment. In contrast, an E QUIVALENT
verdict is a bounded empirical conclusion based on covered obligations and generated inputs, not a
proof of universal functional equivalence. Moreover, because unflagged pairs were not exhaustively
executed, the reported audits estimate the precision of challenged cases rather than overall recall.
Residual model and representation risk. Blinding reduces direct anchoring between the source and
target predictions, but two surrogates can still share the same mistaken assumption. Likewise, the
code graph can omit or misresolve dynamic behavior. Typed unresolved symbols, trace validation,
repeated simulation for unstable cases, and U NCLEAR outcomes expose some of these failures;
none makes surrogate execution a sound verifier. Direct execution, symbolic execution, or formal
verification remains preferable when it is available and applicable.
Security and privacy. The execution audit runs the two revisions in separate subprocesses under a
recorded timeout. Running untrusted code additionally requires process, filesystem, memory, and
network isolation appropriate to the deployment. Proprietary-code deployments require an approved
model endpoint, local inference, or source-redaction policy, and evidence records should omit secrets
embedded in literals, configuration, and runtime state.
Reproducibility record. The run and pair records defined in Appendix A are sufficient to identify the
exact inputs to graph construction, model inference, reconciliation, and direct execution. Reproduction
additionally requires the program snapshots, pair manifests, parser and model versions, provider
access dates, decoding and budget settings, execution environment, raw evidence ledgers, and scripts
that regenerate reported tables and figures. Parse failures, exclusions, timeouts, non-reproduced flags,
and abstentions remain in the machine-readable output rather than being dropped from the audit trail.


                                                   14
