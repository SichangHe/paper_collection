                                             CAM-Bench: A Benchmark for Computational and
                                                     Applied Mathematics in Lean


                                             Wentao Long1∗ Yunfei Zhang2∗ Chenyi Li3 Li Zhou4 Chumin Sun4 Zaiwen Wen3 †
                                             1
                                               Fudan University 2 Qingdao University 3 Peking University 4 Huawei Technologies Ltd.
arXiv:2605.17255v1 [cs.AI] 17 May 2026




                                                                                         Abstract
                                                     Formal theorem-proving benchmarks enable mechanically verifiable evaluation of
                                                     mathematical reasoning in large language models. However, existing benchmarks
                                                     mainly focus on Olympiad-style problems and algebraic domains, leaving compu-
                                                     tational and applied mathematics underrepresented. We introduce CAM-Bench 3 , a
                                                     Lean 4 theorem-proving benchmark of 1,000 Lean proof targets in computational
                                                     and applied mathematics, with coverage spanning optimization, numerical linear
                                                     algebra, and numerical analysis. These problems are adapted from textbook exer-
                                                     cises and often depend on locally introduced definitions, notation, algorithms, and
                                                     elementary results. To construct CAM-Bench, we develop a dependency-recovery
                                                     pipeline that reconstructs the local textbook context needed to state each problem
                                                     faithfully. It then normalizes each problem into a standalone informal theorem
                                                     and translates it into a Lean target. We validate the resulting formal problems
                                                     through Lean compilation and semantic review, checking both formal correctness
                                                     and semantic alignment with the original exercises. For each problem, we release
                                                     the raw exercise, recovered context, normalized informal theorem, and final Lean
                                                     target. CAM-Bench complements existing formal mathematics benchmarks by
                                                     targeting applied mathematics problems that rely on textbook concepts and ele-
                                                     mentary theorems, many of which are not directly available as standard Mathlib4
                                                     lemmas. We evaluate widely used large language models and formalization agents
                                                     on CAM-Bench, and analyze common failure modes in tracking local assumptions,
                                                     applying elementary results, decomposing proofs, and maintaining long-horizon
                                                     control in Lean.


                                         1     Introduction
                                         Mathematical reasoning is a core capability for large language models (LLMs) and a central bench-
                                         mark for reliable multi step inference. Recent advances in reasoning models, proof search systems,
                                         and reinforcement learning with verifiable feedback have produced strong results on both informal
                                         mathematical benchmarks and formal theorem proving tasks [13, 12, 10, 6, 5, 32]. Despite this
                                         progress, informal evaluation gives only a partial account of mathematical competence. When the
                                         final answer is insufficient to validate the derivation, it is difficult to determine whether a model has
                                         actually followed a correct line of reasoning. Formal proof assistants such as Lean [26], Isabelle [28],
                                         Coq [14], and HOL [11] address this limitation by checking statements and proofs against a trusted
                                         kernel. They therefore provide a rigorous way to evaluate whether model generated mathematics is
                                         not only plausible, but mechanically verifiable.
                                         Existing formal reasoning benchmarks have been essential for measuring progress, yet they cover only
                                         part of the ability needed for formalization. MiniF2F focuses on olympiad style statements across
                                             ∗ Equal contribution.
                                             † Corresponding author: wenzw@pku.edu.cn.
                                             3 The CAM-Bench is open sourced at https://github.com/optpku/CAM-Bench.




                                         Preprint.
theorem proving systems [43]. ProofNet studies autoformalization for undergraduate mathematics
[3]. PutnamBench targets competition level problems [33]. FormalMATH broadens Lean 4 coverage
through a large autoformalized corpus [42]. More recent evaluations further show that success on
curated formal benchmarks does not necessarily transfer to research level formalization projects or
program verification tasks [29, 4]. These developments motivate benchmarks that test a different
capability. Existing benchmarks mainly focus on Olympiad style problems, algebraic domains, and
isolated theorem statements, leaving computational and applied mathematics underrepresented.
This gap is important since many problems in computational and applied mathematics are not naturally
stated as self contained theorem statements. Textbook exercises in optimization, numerical linear
algebra, and numerical analysis often depend on locally introduced definitions, notation, algorithms,
chapter conventions, and elementary results. These local dependencies may determine not only the
meaning of the problem, but also the assumptions and proof structure needed for a faithful formal
statement. A benchmark in this setting therefore needs to evaluate whether models can track local
assumptions, perform proof decomposition, and produce valid formal proofs.
We introduce CAM-Bench, a Lean 4 theorem-proving benchmark of 1,000 Lean proof targets in
computational and applied mathematics. The benchmark covers optimization, numerical linear
algebra, and numerical analysis. Its problems are adapted from textbook exercises. For each
problem, the local textbook context needed to state the exercise faithfully is recovered during dataset
construction and exposed together with the Lean target. Each task asks a model to construct a proof
for a fixed Lean statement under its associated local context. This design complements existing
formal mathematics benchmarks by targeting applied mathematics problems that rely on textbook
concepts and elementary theorems, many of which are not directly available as standard Mathlib4
lemmas.
To construct CAM-Bench, we develop a dependency recovery pipeline for context dependent textbook
exercises. For each exercise, the pipeline reconstructs the surrounding mathematical context, including
relevant definitions, notation, algorithms, assumptions, and elementary results. It then normalizes
the exercise into a standalone informal theorem and translates it into a Lean 4 target. Compilation
feedback and semantic review are used to check both the formal correctness of the Lean code and
its semantic alignment with the original exercise. For each problem, we release the raw exercise,
recovered context, normalized informal theorem, and final Lean target, together forming a transparent
record of how the textbook exercise is converted into a proof task.
We evaluate widely used large language models and formalization agents on CAM-Bench. The
resulting error analysis identifies failures in tracking local assumptions, applying elementary results,
decomposing proofs, and maintaining long-horizon control in Lean, suggesting that context-dependent
applied mathematics remains challenging even when the target statement is fixed and mechanically
checkable. Our main contributions are as follows.
       • We introduce CAM-Bench, a Lean 4 theorem proving benchmark for computational and
         applied mathematics. The benchmark contains 1,000 Lean proof targets spanning optimiza-
         tion, numerical linear algebra, and numerical analysis, and provides traceable artifacts from
         the raw exercise to the final machine-checked Lean target.
       • We design a dependency recovery and formalization pipeline for constructing faithful Lean
         targets from context-dependent textbook exercises. The pipeline recovers local mathematical
         context, decomposes heterogeneous exercises into semantic blocks, and uses compilation
         feedback, semantic review, and constrained repair to validate correctness and alignment.
       • We evaluate representative LLM proving strategies on CAM-Bench, including direct proof
         generation, iterative repair, and agent-based proving. We further analyze their failures
         in formal representation, missing mathematical infrastructure, proof-artifact fidelity, and
         long-horizon proof control.


2   Preliminaries and Related Work
Formal benchmarks. Formal benchmarks provide targets for measuring mathematical reasoning
under proof assistant verification. MiniF2F established a cross system testbed for olympiad style
formal mathematics, and PutnamBench extends this line of evaluation to university level competition
problems [43, 33]. ProofNet focuses on undergraduate mathematics by pairing informal problems


                                                   2
                                    Figure 1: Pipeline Overview



with formal statements, making it an important resource for studying autoformalization [3]. Other
benchmarks target specialized mathematical domains, including challenging informal to formal
translation, combinatorial identities, and algebraic reasoning across multiple difficulty levels [21,
22, 15]. Large Lean corpora such as FormalMATH broaden coverage across mathematical areas and
support more systematic evaluation of formal reasoning models [42]. Recent evaluations also move
beyond isolated theorem statements toward more realistic settings, including research level Lean
blueprint projects and Lean 4 code verification tasks [29, 4].

Autoformalization for benchmark construction. Autoformalization translates informal mathemat-
ical language into formal statements and proofs, and large language models have made this direction
increasingly practical [37]. Recent methods use retrieval, compiler feedback, process supervision,
structured prompting, and iterative reflection to improve statement translation and proof generation
[36, 23, 19, 44]. For benchmark construction, however, syntactic validity is only one requirement. A
Lean statement may compile while omitting an assumption, weakening the conclusion, changing a
quantifier, or replacing the original exercise with a nearby theorem that is easier to prove. Recent
robustness studies further show that semantically similar paraphrases of the same informal statement
can lead to different formalizations [25].


Proof assistants and neural theorem proving. Systems such as Isabelle, Coq, HOL Light, and
Lean have long supported large scale formal mathematics and program verification [28, 14, 11, 7, 26].
Recent neural theorem provers build on these environments by combining language model generation
with search, retrieval, compiler feedback, and iterative repair. Early systems showed that generative
models can guide proof search in interactive theorem proving [30, 16]. Subsequent Lean based
provers make increasing use of retrieved premises, environment interaction, synthetic data, self
correction, and reinforcement learning [41, 39, 32, 38, 18, 40, 20, 34, 5, 17]. Agent and project scale
systems further emphasize long horizon coordination, tool use, and end to end formal development
[1, 35]. These systems have substantially improved formal proof generation.


3   Main Pipeline for Benchmark Construction

The overall pipeline for constructing a paired informal–formal Lean benchmark is illustrated in
Figure 1. The system is organized into three major steps: (1) informal benchmark construction,
(2) modularization-driven Lean formalization, and (3) postprocessing. The first step converts
raw textbook exercises into dependency-aware, self-contained informal statements. The second step
decomposes each verified statement into semantically typed blocks and incrementally translates them
into Lean through compiler-guided and semantic repair. The final step normalizes and packages the
accepted Lean outputs into the final benchmark.


                                                  3
   Algorithm 1: Recursive Dependency Expansion and Enrichment
   Input: Exercise x, corpus C, depth budget D
   Output: Enriched exercise x e
 1 T ← E XPAND (N EW N ODE (x), C, D);
   b ← NATURALIZE(T .root);
 2 x
 3 return R ECOVER C ONDITIONS (b   x, T );
 4 Function Expand(v, C, d):
 5     if d = 0 then
 6          return v;
 7     foreach ρ ∈ E XTRACT R EFS(T EXT(v)) do
 8          u ← R ETRIEVE N ODE(ρ, C);
 9          if u ̸= ∅ and ρ ∈
                            / PATH(v) then
10              A DD C HILD(v, E XPAND(u, C, d − 1));
11     return v;
12 Function Naturalize(v):
13     M ← {NATURALIZE(u) : u ∈ C HILDREN(v)};
14     z ← I NSERT(T EXT(v), M);
15     return LLM-NATURALIZE(z, I S ROOT(v));


  3.1   Informal Benchmark Construction

  Exercise extraction. The pipeline begins by extracting raw exercise statements from online text-
  books. These raw exercises preserve the surface form of the original problems, but they are often
  not directly suitable for formalization. They may refer to previous theorems, rely on chapter-level
  notation, or omit inherited assumptions. Thus, the goal of this stage is not merely to extract exercises,
  but to transform them into self-contained formalization targets.
  Recursive dependency expansion and enrichment. A central challenge in textbook-based bench-
  mark construction is that exercise statements are rarely self-contained: a cited theorem may itself
  depend on earlier definitions, lemmas, equations, algorithms, or notation conventions, so resolving
  only explicitly mentioned references is insufficient for a Lean-suitable target.
  To address this issue, we introduce a recursive dependency expansion and enrichment procedure,
  shown in Algorithm 1. Starting from a raw exercise x, the procedure builds a bounded dependency
  tree T by repeatedly extracting references, retrieving the corresponding corpus items, and expanding
  their internal references up to depth budget D. Each dependency node records its source text,
  reference label, hop depth, and provenance information, so each inserted item can be traced back to
  the dependency that contributed it. Cyclic expansion is avoided by ignoring references already on the
  expansion path.
  The tree is then processed bottom-up: each node merges the enriched representations of its children,
  and an LLM naturalizer rewrites the result to resolve local references, standardize notation, smooth
  transitions, and remove duplicated material, ensuring lower-level definitions are incorporated before
  they are used by higher-level dependencies.
  At the root, a broader cleanup removes textbook-specific phrasing and pedagogical hints while
  preserving the mathematical objective. An implicit-condition recovery step then makes required
  assumptions explicit—such as domain restrictions, positivity, dimensional compatibility, and convex-
  ity or regularity conditions—but only when supported by the original problem, recovered context,
  or well-formedness requirements of objects already present in the statement. This enrichment is
  source-grounded rather than free-form: inserted definitions, equations, notation, and assumptions
  must be traceable to the source exercise or recovered dependencies; unresolved dependencies are
  held out rather than completed by conjecture. The output x  e is a declarative, self-contained informal
  target that preserves the original assumptions, quantifiers, domains, and conclusion. Additional
  details on statement cleaning, recursive dependency recovery, source-grounded enrichment, and
  implicit-condition completion are provided in Appendix A.1–A.4.
  Multi-round review and constrained repair. Since dependency enrichment is LLM-assisted,
  the resulting informal statements are passed through a validation loop before formalization. Each
  enriched exercise is reviewed against the original source problem for missing assumptions, task drift,


                                                     4
missing dependencies, unresolved definitions, and Lean suitability. The instance is then classified as
accept, revise, or hold.
Repair is used only for local, review-identified defects: it may normalize notation, inline already
recovered dependencies, restore source-supported assumptions, or convert question-style prompts
into theorem-style statements. It may not introduce unsupported assumptions, invent missing de-
pendencies, weaken or strengthen the claim, or change the proof objective. Every repaired item is
re-reviewed before proceeding to Lean formalization; cases with unrecovered dependencies are held
out rather than completed by conjecture. This loop prevents dependency enrichment from becoming
unconstrained rewriting and keeps the informal benchmark faithful to the original textbook intent.
See Appendix B.1 for the review criteria and decision labels, and Appendix B.2 for the constrained
repair and re-review protocol.


3.2   Modularization-Driven Lean Formalization

Semantic block decomposition. Textbook exercises are often het-
erogeneous: a single problem may combine definitions, optimization
objectives, algorithms, intermediate claims, hints, and theorem tar-
gets. Directly translating such mixed content into one Lean fragment
can cause role confusion and makes errors difficult to localize.
We therefore first convert each enriched exercise into a structured
collection of semantic blocks before Lean generation. Each block
is assigned a functional role according to how it should be used in
the formalization process. For example, algorithmic descriptions
and update rules are separated from optimization formulations; for-
malizable concepts and assumptions are separated from the final
theorem target; and informal hints are retained as guidance but ex-
cluded from the generated Lean declarations. This decomposition
turns a heterogeneous exercise into a theorem-centered dependency Figure 2: Semantic block tree.
structure. The target theorem serves as the root, while the remaining blocks serve as branches that
provide supporting definitions, assumptions, constructions, or contextual information, as illustrated
in Figure 2. By making the semantic role of each component explicit before Lean generation, later
stages can focus on the relevant block rather than repeatedly rewriting the entire formalization.

Frozen-context block-wise construction. Lean formalization proceeds incrementally over the
modularized blocks rather than by repeatedly regenerating the full Lean file.
At each step, the system focuses on a single target block, while previously verified declarations,
assumptions, notation, and auxiliary definitions are kept fixed as read-only context.
This frozen-context protocol yields a stable, monotonically growing prefix: local edits cannot corrupt
earlier blocks, cascading errors are reduced, and failures can usually be localized to the current block
or its interface with the frozen prefix.

Translation, compilation repair, and semantic rewriting. For each target block, the translator
generates Lean code according to the block type, using all previously accepted blocks as read-only
context. The generated Lean code is then checked by the Lean compiler.
If the current block fails to compile, a compiler-guided fixer produces a local patch using the compiler
diagnostics and the frozen context of previously accepted blocks. Typical repairs include correcting
syntax, adding missing type annotations, resolving namespace issues, or adjusting declarations to
satisfy Lean’s type system. This compilation repair loop continues until the block becomes compilable
or the repair budget is exhausted.
Every compilable candidate is then passed to a semantic reviewer. The reviewer compares the
Lean candidate with the corresponding block and checks whether the intended meaning is faithfully
preserved. If a mismatch is detected, the candidate is sent to a semantic rewriter, which produces
a local semantic patch for the current block. The patched code is then returned to the compilation
repair loop to ensure that the semantic correction remains Lean-valid. This combined loop ensures
that accepted Lean blocks are both compilable and aligned with the informal statement.


                                                   5
History-aware repair and rejection control. Because iterative repair can oscillate, the system
maintains a bounded history for each block, including recent attempts, compiler error signatures,
failed patches, semantic review outcomes, and rejection reasons. At each iteration, this history is
provided together with the current feedback, making repair path-aware and discouraging previously
failed edit directions. In this way, failed attempts are not discarded, but are converted into negative
constraints that guide subsequent repairs.
The pipeline also rejects rewrites that introduce semantic degradation, such as strengthening assump-
tions, weakening conclusions, dropping quantifiers, altering variable dependencies, changing notation
in a meaning-changing way, or modifying optimization objectives. This prevents Lean-valid patches
from making the target easier by changing its mathematical content. Together, history-aware repair
and rejection control encourage monotonic progress toward blocks that are both compilable and
faithful to the original textbook semantics.
Postprocessing. The final stage performs lightweight normalization and packaging. Accepted Lean
outputs are cleaned, organized, and assembled into final benchmark files for downstream evaluation.
Additional details on semantic block decomposition, frozen-context construction, compiler-guided
repair, semantic rewriting, history-aware rejection control, and postprocessing are provided in
Appendix C.1 –C.4.

4     Benchmark Analysis
4.1   Overall Dataset Statistics

Our benchmark is a curated Lean 4 bench-
mark for optimization-centric applied mathe-
matics, comprising 1,000 Lean proof targets,
derived from 778 self-contained textbook exer-
cises. Since a single exercise may yield multi-
ple formal theorem targets after decomposition,
the number of released Lean targets is larger
than the number of source exercises; we refer
to each of the 778 retained source exercises af-
ter dependency recovery and formalization as
a benchmark instance, so an instance may con-
tain one or more proof targets. Each retained
target is processed through a hybrid construc-
tion pipeline involving dependency completion,
LLM-assisted semantic review, and Lean 4 for-
malization as discussed in Section 3.
The targets span six broad reasoning categories:          Figure 3: Distribution of benchmark targets
spectral and matrix reasoning; convexity and
geometric inequalities; optimization modeling and duality; optimality conditions and constrained
quadratic reasoning; algorithms and convergence; and applied modeling problems, including robust,
statistical, inverse, and network optimization as well as resource allocation. This organization is based
on the primary formal reasoning demand of each target rather than on textbook chapter headings alone.
Beyond topical breadth, the benchmark is structurally challenging because many targets depend on
recovered local definitions, inherited assumptions, textbook-specific notation, and auxiliary results
that are not directly available as standard Mathlib4 lemmas.

4.2   Preservation and Semantic Validation

We assess construction quality at two levels. Source-level curation asks whether the reviewed informal
target remains faithful to the textbook exercise and self-contained after dependency recovery and
repair. Lean-level semantic validation then asks whether the final Lean declaration preserves that
reviewed target after formal translation. The quantitative statistics below are derived from recorded
semantic-review logs produced by an independent LLM-as-a-judge reviewer and serve as diagnostic
signals for filtering and repair, rather than as the sole correctness criterion. At each semantic-review
stage, every problem that enters the stage is assigned a structured review log recording the resulting


                                                   6
status together with the supporting reasons; representative source-level and Lean-level logs are shown
in Appendix F.8 and Appendix F.7. We retain these logs as diagnostic construction records, and
include representative examples in the appendix to make the source-to-Lean decision process more
auditable.
Source-level review. At the source level, we use the funnel-style process in Figure 4 to filter
and recover candidate exercises. In the first semantic
review round, each candidate is assigned to one of
                                                                      All Candidates
three outcomes: accept, revise, or hold. As shown                           100%
in the figure, 26.5% of candidates are accepted im-
                                                                         First semantic review round
mediately, while 13.6% are marked as revise and
59.9% as hold. Repair-eligible candidates from the      Accepted        Re-
                                                                        vise             Hold
revise branch and non-dependency hold branch then              26.5%   13.6%                             59.9%

undergo targeted repair and re-evaluation. This step
recovers additional Lean-ready informal targets, in-                             Second round


creasing the source-level usable yield from 26.5% to              Targeted Repair & Re-eval.

54.3% before Lean formalization.                                       (Additional Lean-ready Sources +27.8%)




Candidates that remain unsatisfactory after this                                     Finally


source-level review are excluded from the Lean-ready                       Lean-ready sources
source pool. This conservative funnel is designed to                       (54.3% lean-ready sources)

preserve faithfulness to the original source exercise,
self-containment, dependency completeness, and suit-           Figure 4: Source Review Funnel.
ability as Lean theorem targets.
Lean-level validation. After formal translation, we perform a separate semantic validation stage
for the generated Lean declarations. Compilation with sorry checks syntactic and type-theoretic
well-formedness, but does not by itself ensure semantic fidelity. We therefore compare each candidate
Lean declaration against its corresponding reviewed informal target for variables, assumptions,
quantifiers, objectives, constraints, and conclusions. Under the final per-declaration review result,
92.5% of candidate declarations are classified as usable, while 7.5% are classified as not usable and
are excluded from the released and evaluated benchmark unless corrected and re-validated. These
percentages describe the candidate declaration pool at this stage rather than the composition of the
final released benchmark.
In this sense, the released benchmark is a conservatively retained subset of the raw pipeline output
rather than an automatic dump of all generated formalizations. We report source-level validation
details in Appendix B and Lean-level declaration validation details in Appendix C.3.


5     Experiments

We evaluate our benchmark using several frontier large language models. Figure 5 compares verified
Lean accuracy, pass@1 informal accuracy, and average token consumption across frontier models
and solving configurations. All non-agentic baselines are evaluated under the same pass@32 protocol.
Success is measured at the file level: a benchmark instance is counted as solved only if all sorry
blocks in the corresponding Lean file are correctly filled and the resulting file verifies (N = 778
instances containing 1,000 sorry blocks in total). We additionally include an agentic proof-search
setting inspired by FormalProofBench [31], where the model is given the informal problem, the fixed
Lean statement, and the surrounding Lean context, and may iteratively use compiler feedback and
Lean MCP tools before submitting a final proof. Further details and interpretation of the experiment
settings are given in Appendix D.

5.1   Benchmark Performance

Overall performance. Among the non-agentic pass@32 baselines, Deepseek-v4-pro [8]
achieves the highest verified Lean accuracy, reaching 19.67%. It is closely followed by
Claude-sonnet-4.6 [2] at 19.28%. Gemini-3.1-pro-preview [9] obtains 18.38%, while
GPT-5.4 [27] reaches 11.70% and Kimi-k2.6 [24] achieves 2.25%. In contrast, the agentic repair
harness substantially improves verified performance: GPT-5.4/agentic reaches 44.00% verified
Lean accuracy, more than doubling the strongest non-agentic baseline.

                                                  7
                                                                                 Pass@32 Lean accuracy                       Pass@1 Informal accuracy    Avg. tokens / instance


                                                                                                                                                                  83.8
                                                                                                                             79.2                                                           2.0
                                                       80
                                                                      71.9                   71.6                                                 70.0                              1.96




                                                                                                                                                                                                  Avg. tokens / instance (M)
                                        Accuracy (%)
                                                       60                                                                                                                                   1.5

                                                                                                                                                                                   44.00
                                                       40                                                                                                                                   1.0

                                                                                                                     0.59
                                                                                                                                                          0.52
                                                               0.70                                                                       19.28
                                                       20                                                                                                                                   0.5
                                                                                    0.26                                                                  19.67
                                                                                                                     18.38
                                                                                    11.70                                                 0.33
                                                               2.25
                                                        0                                                                                                                                   0.0
                                                               Kimi-k2.6             GPT-5.4                    Gemini-3.1-pro-         Claude-sonnet-    Deepseek-               GPT-5.4
                                                                                                                   preview                   4-6           v4-pro                 agentic


Figure 5: Model performance and token efficiency on CAM-Bench. Pass@32 Lean accuracy and
Pass@1 informal accuracy are shown as percentages (%) on the left y-axis, while average token
usage per evaluated benchmark instance is shown in millions of tokens (M) on the right y-axis. Lean
accuracy is evaluated at the file level, requiring all sorry blocks to be completed and the full Lean file
to verify. The results highlight the gap between informal correctness and verified Lean success.


Informal–formal gap. A clear gap appears between informal mathematical correctness and
machine-checkable Lean correctness. For the non-agentic baselines, pass@1 informal accuracy
remains relatively high, ranging from 70.0% to 83.8%. However, their verified Lean accuracy re-
mains much lower, with the strongest pass@32 baseline below 20%. This discrepancy suggests that
many model outputs capture the high-level mathematical argument but fail to satisfy the stricter
requirements of Lean verification, including Lean syntax, Mathlib conventions, available hypotheses,
and verifier constraints.

Agentic repair and token cost. The agentic configuration yields the largest gain in verified
performance, improving GPT-5.4 from 11.70% under the pass@32 setting to 44.00% under the
agentic setting. This improvement highlights the value of execution-aware refinement: compiler
diagnostics, verifier failures, Lean MCP tool calls, and previous unsuccessful attempts provide
useful signals for targeted proof repair. The gain, however, comes at substantially higher cost:
non-agentic baselines consume 0.26–0.70M tokens per evaluated benchmark instance, whereas
GPT-5.4/agentic requires about 1.96M.

5.2                                     Comparison on Agentic Proof Systems

                                                    We evaluate two external agentic theorem-proving
                                                        Success Rate of Agentic Theorem-Proving Systems
                               80%                  systems, Aristotle [1] and M2F [35], on 200 bench-
 Cumulative success rate (%)




                               70%
                                                    mark instances sampled uniformly at random from
                               60%

                               50%
                                                    the released benchmark. The same instance set, 8-
                               40%                  hour wall-clock budget, and local Lean validation
                               30%                  script are used for both systems to ensure a fair com-
                               20%
                                                    parison. Figure 6 shows the cumulative number of in-
                                                                                   M2F: 143/200 (71.5%)
                               10%                                                 Aristotle: 125/200 (62.5%)

                               0%
                                                    stances that pass our strict validation protocol within
                                    0
                Time budget (hours, log(1+x) scale) the 8-hour budget; to make both the early-time be-
                                                                  1          2       3        4      5     6     7    8


Figure 6: Cumulative solved instances. The hori- havior and the long tail visible, the horizontal axis
zontal axis uses a pseudo-log(1 + x) transform.     is displayed using a pseudo-log(1 + x) transform.
Unlike pass@k decoding, these systems perform long-horizon proof search with Lean compiler
feedback and may construct auxiliary lemmas during the solving process. We therefore adopt a strict
single-problem external validation protocol. An instance is counted as solved only if it is completed
within 8 hours, the returned Lean project recompiles locally, preserves the original theorem statements
and existing definitions, and contains no pseudo-proof artifacts such as sorry, sorryAx, admit,
axiom, or unresolved exact?.


                                                                                                                                    8
Agent performance. Under this protocol, M2F solves 143/200 sampled CAM-Bench instances
(71.5%), while Aristotle solves 125/200 (62.5%). Both substantially outperform direct and
lightweight-agentic baselines, showing the benefit of long-horizon compiler-interactive proof search.
However, the benchmark remains unsaturated: 57 M2F instances and 75 Aristotle instances are
still unsolved, often due to missing mathematical infrastructure, long auxiliary-lemma chains, or
optimization-specific formal reasoning. Detailed validation counts are reported in Appendix E.1.

5.3   Error Analysis

We analyze failed proof attempts from both the pass@32 LLM baselines and the agentic proof-search
systems, inspecting final Lean snapshots for pass@32 and final artifacts for the agentic setting.
Since a single failure may involve multiple symptoms, the labels are multi-label and are used to
summarize recurring bottlenecks rather than disjoint error proportions. We group the dominant failure
patterns into three categories. Detailed definitions and fine-grained error statistics are provided in
Appendix E.2, with representative examples in Appendix F.10.

Library/API Grounding and Infrastructure. Errors in this category arise when the model fails to
ground the proof in the available Lean/Mathlib environment. They include hallucinated or incorrectly
used APIs, unavailable lemmas, missing bridge results, and failures to invoke domain-specific
infrastructure for matrices, spectra, cones, convexity, optimality conditions, or duality.

Formal Representation and Type Discipline. Errors in this category are related to Lean’s formal
representation requirements, including type mismatches, dimension or index errors, coercion failures,
missing typeclass assumptions, notation issues, and unresolved side conditions.

Proof Decomposition and Long-Horizon Control. Errors in this category occur when the model
fails to decompose a proof into appropriate auxiliary lemmas or loses control over a long proof
trajectory. These failures often appear as unfinished helper-lemma chains, residual placeholders, failed
proof plans, or stalled reasoning in optimization, matrix, convergence, and algorithmic arguments.

Table 1: Coarse failure attribution for pass@32 LLM baselines and agentic proof-search systems.
Labels are multi-label and therefore do not sum to 100%.
    Failure attribution                            pass@32 LLMs     M2F (N=57)      Aristotle (N=75)
    Library/API grounding and infrastructure            72.6%       31/57 (54.4%)     38/75 (50.7%)
    Formal representation and type discipline           50.8%       26/57 (45.6%)     29/75 (38.7%)
    Proof decomposition and long-horizon control        71.5%       39/57 (68.4%)     52/75 (69.3%)


Percentages are computed within failed proof blocks for pass@32 (pooled across all baseline models’
failed attempts) and within failed/repair cases for M2F (N =57) and Aristotle (N =75). Overall,
the failures are rarely isolated syntax errors. As shown in Table 1, pass@32 baselines often reach
nontrivial proof attempts but get blocked by the interaction of missing mathematical infrastructure,
hallucinated or misused Mathlib interfaces, and Lean type-system constraints, and insufficient proof
decomposition. Agentic systems alleviate some local repair failures, but the remaining errors are
still dominated by long-horizon proof construction and missing formal infrastructure. This suggests
that CAM-Bench evaluates not only informal mathematical reasoning, but also the ability to ground
applied-mathematics arguments in the actual Lean environment and its available formal infrastructure.

6     Conclusion
We introduce CAM-Bench, a Lean 4 theorem-proving benchmark for computational and applied
mathematics, constructed from textbook problems in optimization, numerical linear algebra, and
numerical analysis. To build it, we develop a dependency-recovery and formalization pipeline that
turns context-dependent exercises into self-contained Lean targets while preserving source traceability.
CAM-Bench remains challenging for current LLM-based theorem provers. Non-agentic pass@32
baselines achieve limited verified accuracy, while agentic proof search improves performance but
leaves many targets unsolved. These results highlight persistent bottlenecks in Mathlib grounding,


                                                    9
Lean type discipline, and long-horizon proof decomposition, and suggest that applied mathematics is
a valuable testbed for evaluating formal proof systems beyond isolated theorem statements.

References
 [1] Tudor Achim, Mingda Sun, Qingxiang Guo, Krunal Guliani, Kush Bhatia, Vineet Kumar,
     Mehran Shakerinava, Haowei Hu, Rohan Daniel, Stella Mai, et al. Aristotle: A recipe for math
     lms. arXiv preprint arXiv:2510.01346, 2025.
 [2] Anthropic.    Claude sonnet 4.6 system               card.       https://anthropic.com/
     claude-sonnet-4-6-system-card, 2026.
 [3] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W Ayers, Dragomir Radev,
     and Jeremy Avigad. Proofnet: Autoformalizing and formally proving undergraduate-level
     mathematics. arXiv preprint arXiv:2302.12433, 2023.
 [4] Slim Barkallah, Srivatsava Daruru, Brando Miranda, Leni Aniva, Allen Nie, and Sanmi Koyejo.
     Veribench-ftp: A formal theorem proving benchmark in lean 4 for code verification. In The 5th
     Workshop on Mathematical Reasoning and AI at NeurIPS 2025, 2025.
 [5] Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran
     Jin, Xing Jin, Chenggang Li, Kaijing Ma, et al. Seed-prover: Deep and broad reasoning for
     automated theorem proving. arXiv preprint arXiv:2507.23726, 2025.
 [6] Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit
     Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the
     frontier with advanced reasoning, multimodality, long context, and next generation agentic
     capabilities. arXiv preprint arXiv:2507.06261, 2025.
 [7] Leonardo De Moura, Soonho Kong, Jeremy Avigad, Floris Van Doorn, and Jakob von Raumer.
     The lean theorem prover (system description). In International Conference on Automated
     Deduction, pages 378–388. Springer, 2015.
 [8] DeepSeek-AI.      Deepseek-v4-pro.              https://huggingface.co/deepseek-ai/
     DeepSeek-V4-Pro, 2026.
 [9] Google. Gemini 3.1 pro preview. https://ai.google.dev/gemini-api/docs/models/
     gemini-3.1-pro-preview, 2026.
[10] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
     Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in
     llms via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025.
[11] John Harrison. Hol light: A tutorial introduction. In International Conference on Formal
     Methods in Computer-Aided Design, pages 265–269. Springer, 1996.
[12] Chaoqun He, Renjie Luo, Yuzhuo Bai, Shengding Hu, Zhen Thai, Junhao Shen, Jinyi Hu,
     Xu Han, Yujie Huang, Yuxiang Zhang, et al. Olympiadbench: A challenging benchmark for
     promoting agi with olympiad-level bilingual multimodal scientific problems. In Proceedings of
     the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
     Papers), pages 3828–3850, 2024.
[13] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn
     Song, and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset. In
     Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks,
     volume 1, 2021.
[14] Gérard Huet, Gilles Kahn, and Christine Paulin-Mohring. The coq proof assistant a tutorial.
     Rapport Technique, 178:113, 1997.
[15] Jiedong Jiang, Wanyi He, Yuefeng Wang, Guoxiong Gao, Yongle Hu, Jingting Wang, Nailing
     Guan, Peihao Wu, Chunbo Dai, Liang Xiao, et al. Fate: A formal benchmark series for frontier
     algebra of multiple difficulty levels. arXiv preprint arXiv:2511.02872, 2025.


                                                10
[16] Guillaume Lample, Timothee Lacroix, Marie-Anne Lachaux, Aurelien Rodriguez, Amaury
     Hayat, Thibaut Lavril, Gabriel Ebner, and Xavier Martinet. Hypertree proof search for neural
     theorem proving. Advances in neural information processing systems, 35:26337–26349, 2022.
[17] Chenyi Li, Yanchen Nie, Zhenyu Ming, Gong Zhang, Kun Yuan, and Zaiwen Wen. Optprover:
     Bridging olympiad and optimization through continual training in formal theorem proving,
     2026.
[18] Yang Li, Dong Du, Linfeng Song, Chen Li, Weikang Wang, Tao Yang, and Haitao Mi. Hun-
     yuanprover: A scalable data synthesis framework and guided tree search for automated theorem
     proving. arXiv preprint arXiv:2412.20735, 2024.
[19] Haohan Lin, Zhiqing Sun, Sean Welleck, and Yiming Yang. Lean-star: Learning to interleave
     thinking and proving. arXiv preprint arXiv:2407.10040, 2024.
[20] Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan
     Geng, Jiawei Ge, Jingruo Sun, et al. Goedel-prover-v2: Scaling formal theorem proving with
     scaffolded data synthesis and self-correction. arXiv preprint arXiv:2508.03613, 2025.
[21] Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengying Liu, Ye Yuan, Haiming Wang, Wei Ju,
     Chuanyang Zheng, Yichun Yin, Lin Li, et al. Fimo: A challenge formal dataset for automated
     theorem proving. arXiv preprint arXiv:2309.04295, 2023.
[22] Junqi Liu, Xiaohan Lin, Jonas Bayer, Yael Dillies, Weijie Jiang, Xiaodan Liang, Roman
     Soletskyi, Haiming Wang, Yunzhou Xie, Beibei Xiong, et al. Combibench: Benchmarking llm
     capability for combinatorial mathematics. arXiv preprint arXiv:2505.03171, 2025.
[23] Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang, Jing Xiong, Chengwu Liu, Jianhao
     Shen, Hui Jin, Jipeng Zhang, Haiming Wang, Zhicheng Yang, Jing Tang, and Zhijiang Guo.
     Process-driven autoformalization in lean 4. arXiv preprint arXiv:2406.01940, 2024.
[24] Moonshot AI. Kimi k2.6. https://www.kimi.com/ai-models/kimi-k2-6, 2026.
[25] Hayden Moore and Asfahan Shah. Evaluating autoformalization robustness via semantically
     similar paraphrasing. arXiv preprint arXiv:2511.12784, 2025.
[26] Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming
     language. In International Conference on Automated Deduction, pages 625–635. Springer,
     2021.
[27] OpenAI. Introducing gpt-5.4. https://openai.com/index/introducing-gpt-5-4/,
     2026.
[28] Lawrence C Paulson. Isabelle: A generic theorem prover. Springer, 1994.
[29] Auguste Poiroux, Antoine Bosselut, and Viktor Kunčak. RLMEval: Evaluating research-level
     neural theorem proving. In Findings of the Association for Computational Linguistics: EMNLP
     2025, pages 10946–10957. Association for Computational Linguistics, 2025.
[30] Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving.
     arXiv preprint arXiv:2009.03393, 2020.
[31] Nikil Ravi, Kexing Ying, Vasilii Nesterov, Rayan Krishnan, Elif Uskuplu, Bingyu Xia, Janitha
     Aswedige, and Langston Nashold. Formalproofbench: Can models write graduate level math
     proofs that are formally verified?, 2026.
[32] ZZ Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue
     Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, et al. Deepseek-prover-v2: Advancing formal
     mathematical reasoning via reinforcement learning for subgoal decomposition. arXiv preprint
     arXiv:2504.21801, 2025.
[33] George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings,
     Amitayush Thakur, and Swarat Chaudhuri. Putnambench: Evaluating neural theorem-provers
     on the putnam mathematical competition. Advances in Neural Information Processing Systems,
     37:11545–11569, 2024.


                                                11
[34] Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood
     Sung, Marina Vinyes, Zhenzhe Ying, Zekai Zhu, et al. Kimina-prover preview: Towards large
     formal reasoning models with reinforcement learning. arXiv preprint arXiv:2504.11354, 2025.
[35] Yuefeng Wang, Jiedong Jiang, Wanyi He, Guoxiong Gao, Chenyi Li, Yongle Hu, Mengxiao
     Sun, Jin Tan, Jingting Wang, Liang Xiao, et al. M2f: Proof automation with lean from
     autoformalization to verified complete proofs. arXiv preprint arXiv:2602.17016, 2026.
[36] Ke Weng, Lun Du, Sirui Li, Wangyue Lu, Haozhe Sun, Hengyu Liu, and Tiancheng Zhang. Aut-
     oformalization in the era of large language models: A survey. arXiv preprint arXiv:2505.23486,
     2025.
[37] Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus N Rabe, Charles Staats, Mateja Jamnik,
     and Christian Szegedy. Autoformalization with large language models. Advances in Neural
     Information Processing Systems, 35:32353–32368, 2022.
[38] Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan Ying, Zheng Yuan, Wenwei Zhang, Dahua
     Lin, and Kai Chen. Internlm2. 5-stepprover: Advancing automated theorem proving via
     critic-guided search. In 2nd AI for Math Workshop@ ICML 2025, 2025.
[39] Huajian Xin, ZZ Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu,
     Liyue Zhang, Xuan Lu, Qiushi Du, et al. Deepseek-prover-v1. 5: Harnessing proof assistant feed-
     back for reinforcement learning and monte-carlo tree search. arXiv preprint arXiv:2408.08152,
     2024.
[40] Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang Wu, Xia Xiao, Yifan Sun, Shen Zheng,
     and Ming Ding. Bfs-prover: Scalable best-first tree search for llm-based automatic theorem
     proving. In Proceedings of the 63rd Annual Meeting of the Association for Computational
     Linguistics (Volume 1: Long Papers), pages 32588–32599, 2025.
[41] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
     Godil, Ryan J Prenger, and Animashree Anandkumar. Leandojo: Theorem proving with
     retrieval-augmented language models. Advances in Neural Information Processing Systems,
     36:21573–21612, 2023.
[42] Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li, Zhongyuan Peng, Minghao Liu, Yifan
     Zhang, Zheng Yuan, Huajian Xin, Wenhao Huang, et al. Formalmath: Benchmarking formal
     mathematical reasoning of large language models. arXiv preprint arXiv:2505.02735, 2025.
[43] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for
     formal olympiad-level mathematics. arXiv preprint arXiv:2109.00110, 2021.
[44] Yichi Zhou, Jianqiu Zhao, Yongxin Zhang, Bohan Wang, Siran Wang, Luoxin Chen, Jiahui
     Wang, Haowei Chen, Allan Jie, Xinbo Zhang, et al. Solving formal math problems by decom-
     position and iterative reflection. arXiv preprint arXiv:2507.15225, 2025.




                                                12
A     Details of Informal Benchmark Construction

This appendix supplements Section 3.1 with implementation details for the natural-language construc-
tion stage. While the main text describes the overall extraction, recursive dependency expansion, and
review pipeline, this appendix specifies the intermediate records used to make the process traceable
and auditable.
The goal of this stage is to convert a context-dependent textbook exercise into a self-contained
informal mathematical target before Lean code is generated. The input is a raw exercise statement
extracted from an online textbook. The output is problem_finally, a Lean-facing informal target
that preserves the original mathematical objective while making assumptions, definitions, domains,
notation, and conclusions explicit.

A.1   Intermediate Records

Each exercise is stored as a sequence of intermediate JSON fields rather than as a single rewritten
statement. These fields record the main transformations from the raw textbook exercise to the final
informal target.

    Field                               Role
    problem                             Raw textbook exercise and semantic anchor.
    problem_clean                       Cleaned mathematical task after removing non-essential
                                        hints, remarks, background narrative, plotting instructions, or
                                        implementation-specific guidance.
    problem_with_context                Cleaned task enriched with recovered textbook dependencies,
                                        such as referenced definitions, equations, theorem statements,
                                        algorithms, notation conventions, and surrounding assumptions.
    problem_standardized_math           Dependency-aware statement with normalized mathematical
                                        wording, consistent notation, and clarified locally inherited ob-
                                        jects.
    problem_finally                     Self-contained Lean-facing informal target used as input to later
                                        Lean formalization.
            Table 2: Intermediate natural-language fields used before Lean generation.


These records make different sources of error easier to localize. Cleaning errors can be
identified by comparing problem and problem_clean. Dependency-recovery errors can be
inspected through problem_with_context. Normalization errors can be checked against
problem_standardized_math. Missing assumptions or unsupported additions can then be re-
viewed in problem_finally.

A.2   Cleaning the Raw Exercise

The first transformation produces problem_clean from the raw extracted exercise. This step is
intentionally conservative. It removes non-essential pedagogical material while preserving formulas,
variables, constraints, assumptions, conclusions, numbering, and explicit references.
The purpose of this step is not to solve, simplify, or reinterpret the problem. Rather, it isolates the
mathematical task from surrounding textbook exposition. For example, hints, explanatory remarks,
plotting instructions, and informal implementation advice may be removed, but the mathematical
objective and all relevant hypotheses must remain unchanged.
Illustrative examples are provided in Appendix F.2, and the corresponding cleaning prompt is shown
in Appendix G.1.

A.3   Dependency recovery and Source-grounded enrichment

Starting from problem_clean, the pipeline recovers local textbook dependencies through
the recursive dependency expansion procedure described in Section 3.1. The resulting field
problem_with_context records both the enriched exercise and the dependency information used


                                                  13
to construct it. This includes retrieved source fragments, original reference labels, provenance
information, and, when applicable, multi-hop dependency expansions.
This enrichment step is source-grounded rather than free-form. The model may incorporate retrieved
definitions, equations, notation, or assumptions, but the inserted information must be traceable to the
source exercise or recovered dependencies.
The enriched statement is then converted into problem_standardized_math. This step folds
the recovered context into a more uniform mathematical statement. In particular, it may expand
unresolved references, standardize notation, clarify variables inherited from the textbook environment,
and remove duplicated inserted material. Its role is normalization rather than mathematical rewriting:
it must not introduce unsupported assumptions, change the proof objective, or alter the original
mathematical content.
An illustrative example is provided in Appendix F.3.

A.4   Constructing the Self-Contained Target

The field problem_finally is the candidate self-contained informal target passed to the
next stage of the benchmark construction pipeline.     It is constructed primarily from
problem_standardized_math, with problem_with_context used only for explicitly recovered
dependencies.
This step makes implicit conditions explicit when they are needed for a well-formed Lean-facing state-
ment. Examples include nonemptiness, nonzero denominators, positivity, invertibility, dimensional
compatibility, convexity or regularity assumptions, and domain restrictions. Such conditions may
be added only when supported by the original problem, recovered context, or the well-formedness
requirements of objects already present in the exercise.
The output is a declarative informal target rather than a question-style textbook prompt. However,
this transformation is constrained: the final statement must preserve the original assumptions, task
objective, quantifiers, domains, and conclusions.
An illustrative example is given in Appendix F.4, and the prompt used for this step is shown in
Appendix G.2.

A.5   Source-Level Review and Repair Interface

Before Lean formalization, each problem_finally is reviewed against the original textbook prob-
lem. The review checks whether the candidate target preserves the source assumptions, variables,
domains, quantifiers, objectives, constraints, and conclusions; whether all necessary definitions and
dependencies are present; and whether the statement is suitable as a Lean-facing theorem target.
The reviewer assigns one of three labels: accept, revise, or hold. Accepted items proceed to Lean
formalization. Items marked revise contain local repairable issues, such as a missing assumption, a
limited task drift, or a missing definition. These items enter a constrained repair branch and are then
submitted to re-review.
Items marked hold are handled separately because the label covers different semantic risks. If the
item depends on unresolved external context, such as an unrecovered theorem, tagged equation,
algorithm, or previous exercise, we do not repair it by conjectural completion; the item is excluded
unless the missing context can be recovered from verified source material. If the item is held
only because of Lean-unsuitable wording or failed review parsing, it may enter a separate hold-
repair branch, provided that the original source supports a conservative reformulation into a precise
theorem-style statement.
Repair is not an acceptance step. In both repair branches, only problem_finally may be modified,
while earlier fields such as problem, problem_clean, and problem_standardized_math remain
fixed as audit anchors. The repair may restore missing assumptions, make definitions explicit, inline
already recovered dependencies, or convert an open-ended exercise into an explicit theorem-style
claim. It may not introduce unsupported assumptions, weaken or strengthen the mathematical claim,
change the proof objective, or invent missing dependencies. Every repaired item must pass re-review
before it can be retained for subsequent Lean formalization.


                                                  14
The full classification labels and review protocol are reported in Appendix B. The representative
examples are given in Appendix F.8 and Appendix F.9, and the prompts used for these steps are
shown in Appendix G.3 and Appendix G.4. The statistics are shown in Appendix B.3.

B     Source-Level Semantic Review
This appendix describes the source-level semantic review procedure used during benchmark construc-
tion.

B.1   Review Criteria and Decision Labels

The source-level semantic reviewer compares problem_finally against the original problem. The
goal is not to improve style, but to determine whether the candidate target preserves the original
mathematical meaning, contains the assumptions and definitions needed for self-containedness, and
is suitable for Lean formalization.
The review first records diagnostic issue flags. These flags identify the type of semantic defect, if any,
before the reviewer assigns a final decision label. Table 3 summarizes the issue categories used in
this stage.

              Table 3: Source-level semantic review criteria and diagnostic issue flags.
Review aspect          Issue flag                Criterion
Assumption preserva- missing_assumption          Flags cases where a necessary assumption from the source
tion                                             problem is absent or changed in problem_finally. This
                                                 includes missing domain restrictions, nonzero, nonnegative,
                                                 positivity, positive-definiteness, index range, continuity, dif-
                                                 ferentiability, boundedness, invertibility, existence, unique-
                                                 ness, or other well-posedness assumptions.
Task preservation      task_drift                Flags non-equivalent changes to the original mathemati-
                                                 cal task. This includes changed quantifiers, changed logi-
                                                 cal direction, changed domains, weakened or strengthened
                                                 conclusions, dropped conclusions, added conclusions, or
                                                 replacing the source task by a nearby but different state-
                                                 ment. Equivalent Lean-facing reformulations are allowed
                                                 only when they preserve the same domain, quantifiers, and
                                                 conclusion.
Self-containedness     missing_dependency        Flags unresolved dependencies that prevent the statement
                                                 from standing on its own, such as missing equation tags,
                                                 theorem labels, algorithms, previous exercise references,
                                                 local conventions, or cited facts that are mentioned but not
                                                 restated clearly enough.
Definition complete- missing_def                 Flags technical terms, functions, operators, mappings, ob-
ness                                             jects, or notation that are used without definitions precise
                                                 enough for formalization. This issue is used only when the
                                                 missing definition creates genuine ambiguity or blocks for-
                                                 malization, not for harmless presentation-level refinements.
Formalization suitabil- hold condition           Checks whether the task is suitable as a Lean-facing target.
ity                                              Proof-oriented mathematical claims and precise computa-
                                                 tional statements are suitable. Open-ended or presentation-
                                                 oriented tasks such as “describe”, “formulate”, “compute”,
                                                 “plot”, “sketch”, or informal discussion are held unless they
                                                 have already been converted into a precise theorem-style
                                                 statement.

After these issue flags are recorded, the reviewer assigns one of three final decision labels: accept,
revise, or hold. Table 4 gives the assignment rule for each label.
The prompt for this stage is provided in Appendix G.3. After review, each problem is accompanied by
a review log that records its decision label and the reasons for that decision. An illustrative example
is provided in Appendix F.8.


                                                   15
                       Table 4: Decision labels for source-level semantic review.
Label                Assignment rule
accept               Used only when no issue is present and the candidate target is suitable for Lean formaliza-
                     tion. The statement must preserve the original mathematical task, be self-contained, and
                     have a precise formalization-ready conclusion.
revise               Used when the issue is local and repairable. In this workflow, revise is triggered by
                     missing_assumption, task_drift, or missing_def, provided that the needed depen-
                     dency context is available and the task is otherwise formalizable.
hold                 Used when the candidate has unresolved dependencies or is not yet suitable for Lean for-
                     malization. This includes missing external context, unresolved tags or theorem references,
                     open-ended exercise wording, non-formalizable tasks, or failed/uncertain review outputs.



B.2     Constrained Repair and Re-review

Items marked revise are not rewritten freely. Instead, they enter a constrained repair stage limited
to the specific defect identified by the review report. The repair step is not allowed to introduce
unsupported new assumptions, replace the original task by a nearby easier statement, or alter the
intended mathematical objective.
After repair, the updated problem_finally is sent back to the same source-level reviewer for re-
evaluation. This second pass checks whether the reported issue has been resolved without introducing
a new one, and whether the repaired target remains faithful, self-contained, and suitable for Lean
formalization.
Not every hold item enters the repair path. If the review report shows that the candidate still depends
on missing external context, such as an unexpanded theorem reference, algorithm, or tagged formula,
we do not attempt to repair it by conjectural completion. Such cases are filtered out unless the missing
dependency can be recovered from verified source material. For Lean-unsuitable cases, repair is
considered only when the source exercise already supports a conservative reformulation into a precise
theorem-style target; otherwise the item remains on hold and is excluded from the released set.
The prompt for constrained repair and re-review is shown in Appendix G.4. An illustrative example
is shown in Appendix F.9.

B.3     Global Source-Level Statistics

We now summarize the aggregate outcomes of the source-level review, repair, and re-review pipeline
after data correction. The statistics are reported in three steps, corresponding to three different input
pools.
First, the original review is applied to the full source-level input pool. We call this pool OI. Second,
the first-round revise cases are repaired and sent to re-review; this gives the RI pool. Third,
the first-round hold cases are filtered before re-review: cases held for missing_dependency are
removed unless the missing context can be recovered from verified source material. The remaining
hold-derived pool is called HI. Thus,
                    RI = R1 revise,          HI = R1 hold − missing_dependency.

Step 1 reports the final decision distribution for each input pool. As shown in Table 5, the three pools
have different accept, revise, and hold rates, so we report them separately rather than merging them
into a single later-round result.


 Table 5: Outcome distributions for the three source-level review input pools after data correction.
               Input pool      Input size         Accepted           Revised              Held
               OI                    1550      410 (26.5%)       211 (13.6%)       929 (59.9%)
               RI                     211       93 (44.1%)        67 (31.8%)        51 (24.2%)
               HI                     578      338 (58.5%)        94 (16.3%)       146 (25.3%)


                                                      16
Step 2 examines the cases marked revise. Table 6 shows the distribution of revise reasons within
each input pool. Since a single problem may carry more than one issue label, the total number of
issue labels can exceed the number of revised cases.

    Table 6: Reason distributions within the revise subset of each source-level review input pool.
             Input pool      Revised     Missing assumption           Task drift      Missing definition
             OI                  211                45 (21.3%)       118 (55.9%)             112 (53.1%)
             RI                   67                16 (23.9%)        47 (70.1%)              29 (43.3%)
             HI                   94                16 (17.0%)        63 (67.0%)              18 (19.1%)


Step 3 examines the cases marked hold. These cases are not treated as ordinary local repair targets.
Instead, they indicate unresolved dependencies, Lean-unsuitable task forms, or parse failures. Table 7
breaks down the hold reasons for each input pool.

     Table 7: Reason distributions within the hold subset of each source-level review input pool.
              Input pool       Held      Missing dependency           Lean-unsuitable         Parse error
              OI                 929               351 (37.8%)             512 (55.1%)          66 (7.1%)
              RI                  51                20 (39.2%)              12 (23.5%)         19 (37.3%)
              HI                 146                  2 (1.4%)              83 (56.8%)         61 (41.8%)



C      Details of Lean Formalization Pipeline
This section supplements the Lean formalization pipeline in the main text. We describe the record
format, block-wise construction, semantic review, and final packaging used to produce the benchmark
artifacts.

C.1     Lean-Facing Semantic Block Records

After preprocessing, each exercise is represented as an ordered list of Lean-facing semantic records:
                           index,      source,      source_idx,         kind,      content.
The optional term field is used when a block introduces a named definition, optimization problem, or
algorithm. The field kind determines how the block is translated, as summarized in Table 8.

      Kind                 Semantic role                              Lean-level treatment
      hints                Informal guidance.                         Kept for provenance, usually excluded
                                                                      from Lean generation.
      defn                 Definitions, predicates, notation, or      Translated into Lean definitions or auxil-
                           named terms.                               iary declarations.
      opt_prob             Objectives, feasible sets, constraints,    Translated into structures, feasibility predi-
                           or optimality conditions.                  cates, or objective functions.
      algo / alg           Algorithms, updates, or iterative con-     Translated into step functions, states, in-
                           structions.                                variants, or validity predicates.
      thm                  Theorem, lemma, proposition, or final      Translated into a Lean theorem or lemma
                           target.                                    with proof body initialized as by sorry.
                                  Table 8: Lean-facing semantic block records.


A flattened theorem record has the following form:

{
    "index": 3,
    "source": "book/convex_optimization_Chapter3",
    "source_idx": "Exercise 3.24-(c)",


                                                          17
   Algorithm 2: Block-wise Lean translation with local repair
   Input: Semantic blocks B = (b1 , . . . , bm ); Lean scaffold L0 ; repair budget R; few-shot helper E
   Output: Combined Lean file L
 1 L ← L0
 2 for b ∈ B do
 3     if b is non-formalizable then
 4          continue
 5     insert immutable source comment for b into L
 6     F ← F ROZEN C ONTEXT(L, b)
 7     E ← R ETRIEVE F EW S HOT(E, b)
 8     c ← T RANSLATE B LOCK(b, F, E)
 9     L′ ← I NSERT B LOCK(L, b, c)
10     if C OMPILE(L′ ) succeeds then
11          L ← L′ ; freeze b; continue
12     for r = 1 to R do
13          D ← D IAGNOSTICS(L′ )
14          E ← R ETRIEVE F EW S HOT(E, b, D)
15          c ← R EPAIR B LOCK(b, F, c, D, E)
            b
16          L′ ← R EPLACE B LOCK(L, b, b   c)
17          if C OMPILE(L′ ) succeeds then
18              L ← L′ ; freeze b; break
19          c←b   c
20     if b is not frozen then
21          mark b as compilation failure and continue when possible
22 C OMPILE (L)                                                               // final validation
23 return L




       "kind": "thm",
       "content": "Let a_1,...,a_n be real numbers with a_1 < ... < a_n.
                   Prove that f is convex, concave, quasiconvex, and
                   quasiconcave."
   }

   Records are processed in index order. The orchestrator inserts immutable block-boundary comments
   into the Lean file, so each generated declaration can be traced back to its semantic record.

   C.2   Block-Wise Construction and Compilation Repair

   Lean generation proceeds block by block. For each target block, the prefix of already accepted Lean
   code is treated as a frozen context; the model may only generate or repair the current block. The
   combined file is checked by:

   lake env lean --threads=<LEAN_THREADS> <file>

   For theorem-like blocks, by sorry is allowed during construction, so compilation validates the
   statement and declaration interface rather than a completed proof.
   Algorithm 2 summarizes the translation-repair loop. The few-shot helper retrieves similar translation
   or repair examples according to the current block and, during repair, the Lean diagnostics.
   A compact translation prompt is shown in Appendix G.5.

   C.3   Semantic Review and Alternating Repair

   Compilation does not ensure semantic faithfulness. A compilable block may omit assumptions, alter
   quantifiers, change domains, or weaken the intended conclusion. Thus, each compilable block is
   reviewed against its semantic record.
   The reviewer returns a structured report:


                                                     18
   Algorithm 3: Block-wise semantic review and repair
   Input: Lean file L; blocks B = (b1 , . . . , bm ); budgets S, R; few-shot helpers H
   Output: Reviewed Lean file L
 1 A ← []                                                           // accepted previous blocks
 2 for i = 1 to m do
 3     b ← bi
 4     if b is not formalizable then
 5          continue
 6     F ← F ROZEN C ONTEXT(L, b, A)
 7     Histb ← [ ]
 8     for s = 1 to S do
 9          c ← E XTRACT B LOCK(L, b)
10          ρ ← R EVIEW(b, c, F, A)
11          if ρ accepts c then
12               append b to A; mark b accepted; break
13          c′ ← R EWRITE(b, c, ρ, F, A, Histb )
14          L′ ← PATCH C URRENT B LOCK(L, b, c′ )
15          if C OMPILE(L′ ) fails then
16               ∆ ← D IAGNOSTICS(L′ )
17               Histb ← Histb ∪ {(s, c′ , ρ, ∆)}
18               E ← S ELECT F EW S HOTS(H, ∆, ρ)
19               L′ ← C OMPILATION R EPAIR(L′ , b, F, A, R, ∆, Histb , E)
20          if C OMPILE(L′ ) succeeds then
21               L ← L′                              // re-review repaired block next round
22          else
23               mark b failed; break
24 return L




  {
      "math_equivalent": true,
      "truth_judgement": "true|false|unknown|not_applicable",
      "overall_status": "usable|usable_with_revision|not_usable_yet",
      "dominant_issue_types": ["missing_assumption", "task_drift"],
      "top_priority_fix": "...",
      "issues": [
        {
          "severity": "P0|P1|P2",
          "issue_type": "missing_assumption|wrong_boundary_case|task_drift",
          "location": "current declaration",
          "reason": "...",
          "suggested_fix": "..."
        }
      ],
      "confidence": 0.0
  }

  Blocks marked usable are accepted. Otherwise, the current block is semantically rewritten, recom-
  piled, and reviewed again. If semantic rewriting causes Lean errors, compilation repair is invoked
  under the semantic constraint that the intended correction must be preserved. Algorithm 3 summarizes
  this alternating loop.

  C.4   Postprocessing, Packaging, and Validation

  After semantic review, accepted Lean files are conservatively postprocessed and exported. This stage
  standardizes comments, namespaces, formatting, and metadata while leaving accepted declarations
  unchanged.


                                                  19
Each benchmark instance contains the Lean file and a metadata record with the source exercise,
informal statement, block identifiers, validation status, and basic construction statistics. The pipeline
also saves compiler diagnostics, semantic-review reports, repair histories, and failure records. The
final artifacts separate statement construction from proof-generation evaluation: downstream provers
replace only the sorry placeholders while the formalized statements remain fixed.

D     Experimental Settings
D.1   Code and Data Availability

We provide the code and dataset to support reproducibility. The anonymized code repository is
available at: https://anonymous.4open.science/r/CAM-Bench-2D32.
The dataset is hosted separately and can be accessed through the following DOI: https://doi.
org/10.7910/DVN/B5JTZI.

D.2   Baseline Setup

We evaluate Lean proof generation on CAM-Bench instances derived from textbook exercises in
computational and applied mathematics. The benchmark contains 778 source exercises and 1,000
Lean proof targets, each initialized with a sorry placeholder to be filled by the prover.

Pass@1 informal accuracy. Pass@1 informal accuracy is evaluated by prompting each model
once per benchmark instance to produce a natural-language solution for the normalized informal
theorem, without requiring Lean-valid syntax. An LLM evaluator then checks whether the returned
argument correctly establishes the stated result; a response is counted as correct only if the core
mathematical reasoning is valid and addresses the intended conclusion.
All Lean verification is performed with Lean 4 and Mathlib through Lake:
                     leanprover/lean4:v4.28.0,               mathlib:v4.28.0.
Each candidate proof is checked by running lake env lean. A proof attempt is considered success-
ful only if the resulting Lean file compiles and passes integrity checks.
We compare the following baseline models:
gpt-5.4,     claude-sonnet-4-6,         kimi-k2.6,       deepseek-v4-pro,        gemini-3.1-pro-preview.
For the Lean proof-search experiments, we use temperature 0.4, a maximum of 32 repair turns per
sorry block, a file-level token budget of 106 , and a per-call output-token limit of 16,000. Reported
success is still computed at the file level: a benchmark instance is counted as solved only when
all sorry blocks in the corresponding Lean file are filled and the full file verifies. Lean MCP is
enabled with Python transport, targeted tool mode, pool size 1, timeout 5 seconds, and the tools
lean_unified_search and lean_leansearch.
The proof-search solver processes each Lean file sequentially. It detects all sorry tokens, replaces
the current sorry with a placeholder, asks the model to fill only that proof body, inserts the result,
and verifies the prefix with Lean. Once a block is solved, the solver proceeds to the next sorry.
Failed attempts are followed by retry prompts containing Lean error messages and, when available,
MCP search context.

D.3   Prompts for Pass@k Experiments

All pass@k experiments use a fixed proof-generation prompt template. The prompt provides the
model with the informal problem, the target Lean statement, and the surrounding Lean context, and
asks it to return only a proof body for the designated sorry. The complete prompt templates and
formatting constraints are given in Appendix G.6.

D.4   Estimation for Pass@k Results

Table 9 reports the Pass@k results for k ∈ {1, 2, 4, 8, 16, 32}. These values summarize how per-
formance changes as the sampling or repair budget increases. In particular, Pass@1 measures


                                                   20
Table 9: Pass@k results across different attempt budgets. Pass@32 is the main setting used in our
benchmark comparison.
   Model                       Pass@1      Pass@2        Pass@4    Pass@8      Pass@16      Pass@32
   Claude-sonnet-4-6           5.14%        7.07%         9.51%    12.47%       15.42%       19.28%
   Deepseek-v4-pro             5.78%        8.48%        10.41%    12.85%       16.20%       19.67%
   Gemini-3.1-pro-preview      6.04%        8.87%        12.34%    14.27%       16.97%       18.38%
   GPT-5.4                     2.96%        3.60%        5.53%     7.98%        10.55%       11.70%
   Kimi-k2.6                   0.28%        0.28%         0.28%     0.56%        0.56%        2.25%


single-attempt success, while larger values of k measure the probability that at least one valid Lean
solution is found within a larger attempt budget. Our main benchmark comparison uses Pass@32,
but the full Pass@k curve provides a more detailed view of model scaling under repeated attempts.
For each evaluation instance, we record whether the model solves all required sorry blocks within at
most k attempts. An instance is counted as passed if every block is solved within the attempt budget
and the final Lean code passes compilation and integrity checks. Thus, the entries in Table 9 are
empirical success rates under increasing attempt budgets.
For a problem i, let si (k) be the binary success indicator:
                                 
                                   1, if problem i is solved within k attempts,
                        si (k) =
                                   0, otherwise.
Given N evaluated problems, the empirical Pass@k is
                                                         N
                                                 1 X
                                        Pass@k =       si (k).
                                                 N i=1

When multiple independent samples are generated for the same problem, we use the standard unbiased
estimator. If n samples are generated and c of them are correct, then
                                                  n−c
                                                      
                                                   k
                                Pass@k = 1 − n ,
                                 \                           n ≥ k.
                                                     k
This estimator gives the probability that at least one of k sampled candidates is correct. In the
sequential repair setting used by our Lean solver, the reported Pass@32 corresponds to the empirical
probability that the repair trajectory succeeds within 32 turns.

D.5   Agentic Proof-Search Setting

Figure 7 illustrates our agentic proof-search setting. Our setting follows the multiturn, tool-augmented
evaluation style of FormalProofBench [31], where the model is given the natural-language problem,
the Lean 4 formalization, and the required headers and context, and may interact with proof-assistance
tools before submitting a final proof. While FormalProofBench uses Lean Loogle as its theorem-
search tool, our implementation uses Lean search instead.
For each problem, the agent receives the normalized informal theorem, the corresponding Lean target,
and all accepted local declarations recovered during benchmark construction. The agent may query
Lean search for relevant Lean/Mathlib facts, test candidate proof fragments with the Lean executor,
and use compiler diagnostics, unsolved goals, type mismatches, missing-lemma errors, and previous
failed attempts to guide iterative repair. The agent is allowed up to 40 interaction turns per problem.
The final answer must be a proof body starting with by, which is inserted into the original theorem
without modifying the theorem statement or any preceding definitions.
We use a strict verifier for final acceptance. A task is counted as solved only if the completed Lean file
recompiles successfully and the submitted proof contains no prohibited proof shortcuts or unresolved
holes, including sorry, admit, axiom, sorryAx, exact?, or apply?. We also require that the
original theorem name, statement, assumptions, and previously accepted declarations are preserved.
Thus, the agentic setting evaluates interactive proof construction rather than statement rewriting or
benchmark-specific weakening of the target.


                                                    21
Figure 7: Agentic proof-search setting used in CAM-Bench. The model receives both the informal
problem and the formal Lean target, iteratively interacts with Lean search and a Lean executor, and
submits a proof for final Lean-kernel verification. Compared with the FormalProofBench [31] setup,
our setting follows the same multiturn proof-search protocol but replaces Lean Loogle with Lean
search.


Comparison with pass@32. The agentic results should be interpreted as a complementary evalua-
tion setting rather than a direct replacement for the non-agentic pass@32 protocol. In the pass@32
setting, each problem is evaluated through independent proof-generation attempts under a fixed
sampling budget. In contrast, the agentic setting allows the model to adaptively interact with Lean
MCP tools, inspect compiler diagnostics, observe unsolved goals and type mismatches, and revise its
proof attempts over multiple turns. Thus, the two settings measure related but distinct capabilities:
pass@32 primarily evaluates repeated direct proof generation, whereas the agentic setting evaluates
interactive proof construction and execution-guided repair.

Performance–efficiency trade-off. The improvement of GPT-5.4/agentic suggests that many
benchmark failures are repairable when the model receives structured feedback from the Lean envi-
ronment. Compiler errors can reveal local syntax issues, unavailable declarations, type mismatches,
missing coercions, or mismatched hypotheses, while previous failed attempts help avoid repeated
invalid proof patterns. However, the agentic setting is not token-matched with the pass@32 baselines.
The agent spends additional tokens on tool calls, intermediate proof fragments, compiler outputs, and
repair attempts. In our experiments, pass@32 baselines use between 0.26M and 0.70M tokens per
problem on average, whereas GPT-5.4/agentic uses about 1.96M tokens per problem. Therefore,
we report agentic results separately and interpret them as evidence for the benefit of Lean-guided
interactive repair, rather than as a strictly equal-budget comparison.

E     Details of External Agent Evaluation and Failure Analysis
E.1   Details of M2F and Aristotle Evaluation

This appendix reports the raw success counts for the M2F and Aristotle evaluation. These counts
correspond to the strict externally validated results reported in the main text. The 200 evaluation
instances are sampled uniformly at random from the released benchmark and shared by both systems;
the same instance set, 8-hour wall-clock budget, and local Lean validation script are used for M2F
and Aristotle to ensure a fair comparison. Because the evaluation is run on a 200 instances, the
reported success rates should be interpreted as sample estimates for the full benchmark. Table 10
reports the M2F results, and Table 11 reports the Aristotle results.

E.2   Details of Failure Analysis

This appendix provides additional details for the formalization-error analysis in Section 5.3 . We
analyze failed proof attempts from both pass@32 LLM baselines and agentic proof-search systems.


                                                 22
      Table 10: M2F results by solving-time bucket under the strict isolated 8-hour protocol.
                  Time bucket    Total instances   Solved     Unsolved   Success rate
                  < 30 min                  107         102          5        95.3%
                  30–60 min                  17          17          0       100.0%
                  1–2 h                      18          15          3        83.3%
                  2–4 h                      12           8          4        66.7%
                  4–8 h                       4           1          3        25.0%
                  8–12 h                     14           0         14         0.0%
                  > 12 h                     28           0         28         0.0%
                  Total                     200         143         57        71.5%


    Table 11: Aristotle results by solving-time bucket under the strict isolated 8-hour protocol.
                  Time bucket    Total instances   Solved     Unsolved   Success rate
                  < 30 min                   39          37          2        94.9%
                  30–60 min                  42          35          7        83.3%
                  1–2 h                      35          26          9        74.3%
                  2–4 h                      32          18         14        56.2%
                  4–8 h                      26           9         17        34.6%
                  8–12 h                     15           0         15         0.0%
                  > 12 h                     11           0         11         0.0%
                  Total                     200         125         75        62.5%


For pass@32, the unit is a failed proof block and we inspect its final Lean snapshot. For agentic
systems, the unit is a non-clean run whose final artifact does not pass local Lean compilation and
validation. The labels are diagnostic rather than mutually exclusive: a single failed attempt may
involve multiple symptoms.

Library/API Grounding and Mathematical Infrastructure. This category covers failures where
the model cannot ground a plausible mathematical proof in the available Lean/Mathlib environment.

     1. Hallucinated or invalid APIs. The model invokes nonexistent theorem names, invalid
        fields, unsupported API patterns, or real declarations with incompatible signatures.
     2. Missing bridge results. The proof requires intermediate lemmas that connect the current
        goal to available Mathlib facts, but these bridge results are absent or not found.
     3. Domain-specific infrastructure gaps. The failure occurs in higher-level applied-
        mathematics infrastructure, such as matrices, spectra, positive semidefinite cones, convexity,
        optimality conditions, duality, or convergence.

Formal Representation and Type Discipline.              This category covers failures caused by Lean’s
precise representation requirements.

     1. Type, dimension, and index errors. The generated proof uses incompatible types, di-
        mensions, or indexing conventions, especially for vectors, matrices, finite index sets, and
        parameterized constraints.
     2. Coercion and typeclass failures. The proof misses required coercions, scalar casts, subtype
        conversions, order or normed-space instances, or other typeclass obligations.
     3. Notation and side-condition failures. The attempt uses unsuitable notation or leaves side
        conditions generated by rewriting, simplification, inequalities, or algebraic transformations
        unresolved.

Proof Decomposition and Long-Horizon Control. This category covers failures where the proof
requires a longer chain of intermediate claims than the model can reliably organize.

     1. Missing auxiliary lemmas. The model does not introduce the intermediate claims needed
        to connect the assumptions to the final theorem.


                                                   23
      2. Unfinished proof construction. The final artifact still contains residual placeholders,
         incomplete helper lemmas, abandoned branches, or proof plans that exceed the search or
         repair budget.
      3. Loss of long-horizon control. The proof loses consistency across a multi-step argument
         involving optimization models, matrix identities, convexity reasoning, certificates, invariants,
         algorithms, or convergence claims.

Overall, the observed failures are rarely isolated syntax errors. They usually arise from the interaction
of missing or misused Mathlib infrastructure, Lean type-system constraints, and incomplete long-
horizon proof planning.
We give three short case studies that illustrate the coarse error categories used in Table 1 in Ap-
pendix F.10.

F     Illustrative Examples
This appendix provides representative examples for the main construction stages used in our bench-
mark pipeline. The examples are organized in the same order as the pipeline: semantic block
decomposition, raw-to-clean preprocessing, dependency recovery and standardization, self-contained
target construction, source-level review, and constrained repair.

F.1   Example: Semantic Block Decomposition

This example illustrates how a heterogeneous textbook exercise is decomposed into typed semantic
blocks before Lean generation. The raw exercise combines assumptions, notation conventions,
an optimization formulation, a request to derive KKT conditions, and a separate optimality claim.
Directly translating such mixed content into Lean is difficult because these components play different
formal roles and should not be treated as a single undifferentiated problem statement.
Our preprocessing step separates the exercise into reusable mathematical background, problem-
specific data, and theorem targets. General concepts such as KKT conditions, stationarity, primal
feasibility, and complementary slackness are extracted as definition blocks. The logarithmic simplex
program is isolated as an optimization-problem block, and the two requested tasks are separated into
theorem-target blocks.

Raw exercise.      Let n ∈ N with n ≥ 2. Let a = (a1 , . . . , an ) ∈ Rn satisfy
                                        a1 ≥ a2 ≥ · · · ≥ an > 0,
                                   n
and define b = (b1 , . . . , bn ) ∈ R by
                                         1
                                       bk = ,     k = 1, . . . , n.
                                         ak
Let 1 ∈ Rn denote the all-ones vector, and let x ⪰ 0 mean xi ≥ 0 for all i = 1, . . . , n.
The exercise considers the logarithmic simplex program
                                  minimize     − log(aT x) − log(bT x)
                                  subject to   x ⪰ 0, 1T x = 1,
with variable x ∈ Rn . It then asks the solver to write the Karush–Kuhn–Tucker conditions explicitly
and to show that                                                   
                                                1                 1
                                        x=        , 0, . . . , 0,
                                                2                 2
is optimal.
The KKT part of the exercise asks to show that the conditions are the existence of a scalar multiplier
ν ∈ R and inequality multipliers λ = (λ1 , . . . , λn ) ∈ Rn such that
                  1T x = 1,       xi ≥ 0,      λi ≥ 0,      λ i xi = 0   (i = 1, . . . , n),
and, for each i = 1, . . . , n,
                                         ai  bi
                                       − T − T + ν − λi = 0.
                                        a x b x

                                                   24
Preprocessed semantic blocks. After preprocessing, the raw exercise is converted into the follow-
ing typed semantic blocks.

 1. Definition block: Karush–Kuhn–Tucker conditions. For a problem of minimizing f (x)
    subject to inequality constraints gi (x) ≤ 0 and equality constraints hj (x) = 0, the KKT
    conditions are the existence of multipliers λi ≥ 0 and νj such that primal feasibility holds,
    stationarity holds,               X                 X
                            ∇f (x) +       λi ∇gi (x) +   νj ∇hj (x) = 0,
                                        i                   j
      and complementary slackness holds:
                                        λi gi (x) = 0     for all i.
 2. Definition block: complementary slackness. For inequality constraints gi (x) ≤ 0 with
    multipliers λi ≥ 0, complementary slackness means
                                       λi gi (x) = 0     for every i.
 3. Definition block: stationarity. A KKT point satisfies stationarity if the gradient of the La-
    grangian with respect to the primal variable vanishes:
                                            ∇x L(x, λ, ν) = 0.
 4. Definition block: primal feasibility. A point x is primal feasible if it satisfies all original
    constraints of the optimization problem.
 5. Optimization-problem block: logarithmic simplex program. The optimization problem is
    isolated as
                             minimize − log(aT x) − log(bT x)
                             subject to x ⪰ 0, 1T x = 1,
    with variable x ∈ Rn .
 6. Theorem-target block: explicit KKT conditions. Under the assumptions
                                                                           1
                             n ≥ 2,    a1 ≥ a2 ≥ · · · ≥ an > 0,    bk =     ,
                                                                          ak
    the first theorem target asks for an explicit characterization of the KKT conditions for the
    logarithmic simplex program. The target statement asserts the existence of ν ∈ R and λ =
    (λ1 , . . . , λn ) ∈ Rn satisfying
                    1T x = 1,    xi ≥ 0,       λi ≥ 0,          λ i xi = 0   (i = 1, . . . , n),
    together with the stationarity equations
                               ai      bi
                            − T − T + ν − λi = 0,                   i = 1, . . . , n.
                              a x b x
 7. Theorem-target block: optimality of the endpoint mixture. Under the same assumptions and
    for the same logarithmic simplex program, the second theorem target asks to prove that
                                                                  
                                               1                 1
                                         x=      , 0, . . . , 0,
                                               2                 2
      is optimal.

Discussion. This decomposition makes the role of each component explicit before Lean generation.
General mathematical background is separated from problem-specific data, the optimization formula-
tion is isolated from the requested claims, and the two theorem targets can be translated, repaired,
and validated independently.

F.2   Example: Raw-to-Clean Preprocessing

This example illustrates the cleaning step that converts a raw textbook exercise into the
problem_clean field. The cleaning step removes non-essential pedagogical material while preserv-
ing the mathematical statement, notation, assumptions, and objective.


                                                 25
F.2.1   Removing Proof Hints
Raw exercise.

         Exercise 11.5. When r : Rn → Rn , show that the function
                                   ϕ(λ) = (J T J + λI)−1 J T r

         is monotonically decreasing in λ, unless J T r = 0. Hint: Use the singular-value
         decomposition of J.

Cleaned exercise.

         Exercise 11.5. When r : Rn → Rn , show that the function
                                   ϕ(λ) = (J T J + λI)−1 J T r

         is monotonically decreasing in λ, unless J T r = 0.

Discussion. This example illustrates a minimal cleaning operation. The mathematical statement,
notation, and exception condition are preserved exactly, while the proof hint is removed.

F.2.2   Removing Application Narrative
Raw exercise.

         Exercise 17.3. Flux balance analysis in systems biology. Flux balance analysis is
         based on a simple model of reactions in a cell, keeping track only of the gross rate
         of consumption and production of chemical species. Based on known stoichiometry
         and upper bounds on some reaction rates, we can compute bounds on other reaction
         rates or on cell growth.
         We focus on m metabolites M1 , . . . , Mm and n reactions R1 , . . . , Rn , with non-
         negative reaction rates v1 , . . . , vn . The stoichiometry matrix S ∈ Rm×n is defined
         so that Sij is the rate of production of metabolite Mi due to unit reaction rate
         vj = 1, with consumption represented by negative production.
         The last reaction Rn corresponds to biomass creation, so vn is the cell growth rate.
         Conservation of metabolites is expressed as
                                                 Sv = 0.
         We are also given upper limits on some reaction rates, written as
                                        v ⪰ 0,       v ⪯ v max ,
         where vjmax = ∞ if no upper bound on reaction rate j is known.
         The questions below pertain to the data found in fba_data.m.
         (a) Find the maximum possible cell growth rate G⋆ , as well as optimal Lagrange
         multipliers for the reaction rate limits. How sensitive is the maximum growth rate
         to the various reaction rate limits?

Cleaned exercise.

         Exercise 17.3. Let S ∈ Rm×n be the stoichiometry matrix, let v1 , . . . , vn be
         nonnegative reaction rates, and let v max satisfy vjmax = ∞ if no upper bound on
         reaction rate j is known. The last reaction rate vn is the cell growth rate. Consider
         the constraints
                                Sv = 0,        v ⪰ 0,      v ⪯ v max .
         The data are given in fba_data.m.
         (a) Find the maximum possible cell growth rate G⋆ , and optimal Lagrange multipli-
         ers for the reaction rate limits. Determine the sensitivity of the maximum growth
         rate to the reaction rate limits.


                                                   26
Discussion. This example shows a larger cleaning operation. The biological motivation and
illustrative reaction examples are removed, while the formal variables, constraints, data dependency,
and optimization task are retained.

F.3   Example: Dependency Recovery and Standardization

This example illustrates a case in which an exercise depends on both a target problem reference and
an algorithm reference. The algorithm further introduces a second-level formula dependency. The re-
covered record therefore contains four main components: the cleaned exercise, dependency metadata,
the context-enriched statement, and the standardized mathematical statement used downstream.

Source.    book/Numerical Optimization_Chp16, Exercise 16.24.

Recovered dependency metadata. Table 12 summarizes the dependency chain identified during
recursive dependency recovery. The original exercise directly refers to problem (16.76) and Algorithm
16.4, while Algorithm 16.4 introduces an additional formula dependency on (16.58).

                          Table 12: Recovered dependencies for Exercise 16.24.
                  Level     Field                     Label            Evidence
                  1         body_refs                 eq:16.76         problem (16.76)
                  1         theorem_refs              alg:16.4         refs_attr
                  2         inner_body_refs           eq:16.58         (16.58)
                  2         expanded_body_refs        eq:16.58         via:Algorithm 16.4


Recovered record. The following display shows the intermediate records produced by dependency
recovery and standardization.

Input. Cleaned exercise.
          Exercise 16.24. Program Algorithm 16.4 and use it to solve problem (16.76). Set all initial
          variables to be the vector e = (1, 1, . . . , 1)T .

Stage 1. Context-enriched problem.           The context-enriched version keeps the inserted references
explicit and traceable.

Reference formula (16.76).
                           max          6x1 + 4x2 − 13 − x21 − x22 ,
                                                                                                        (16.76)
                           subject to   x1 + x2 ≤ 3,    x1 ≥ 0,              x2 ≥ 0.

Reference result Algorithm 16.4. Algorithm 16.4, the predictor-corrector algorithm for quadratic
programming, computes (x0 , y0 , λ0 ) with (y0 , λ0 ) > 0. For k = 0, 1, 2, . . ., set
                                          (x, y, λ) = (xk , yk , λk )
and solve (16.58) with σ = 0 for
                                          (∆xaff , ∆y aff , ∆λaff ).
Then calculate
                                                   yT λ
                                                 µ=     ,
                                                    m
                      α̂aff = max α ∈ (0, 1] | (y, λ) + α(∆y aff , ∆λaff ) ≥ 0 ,
                                 

and
                                    (y + α̂aff ∆y aff )T (λ + α̂aff ∆λaff )
                               µaff =                                       .
                                                       m
The centering parameter is then set to
                                                       3
                                                  µaff
                                          σ=                .
                                                    µ

                                                      27
Second-level reference formula (16.58).
                                       " # "
                          G 0 −AT         ∆x      −rd
                                                         #
                         A −I       0   ∆y =    −rp      .                                                  (16.58)
                           0 Λ       Y    ∆λ   −ΛYe + σµe

Stage 2. Standardized mathematical statement. The standardized version removes explicit
provenance markers and rewrites the recovered references into a self-contained mathematical task.

         Use the predictor-corrector algorithm for quadratic programming to solve
                            max           6x1 + 4x2 − 13 − x21 − x22 ,
                            subject to    x1 + x2 ≤ 3,    x1 ≥ 0,              x2 ≥ 0.

        Take all initial variables equal to e = (1, 1, . . . , 1)T . Equivalently, compute an initial point
        (x0 , y0 , λ0 ) with all components equal to 1 and with (y0 , λ0 ) > 0.
        For k = 0, 1, 2, . . ., set
                                            (x, y, λ) = (xk , yk , λk )
         and solve, with σ = 0,
                                                                 
                              G       0     −AT   ∆x          −rd
                            A       −I      0  ∆y  =     −rp     ,
                               0     Λ       Y    ∆λ       −ΛYe + σµe

         where
                                rd = Gx − AT λ + c,              rp = Ax − y − b.
         This gives
                                            (∆xaff , ∆y aff , ∆λaff ).
         Next compute
                                                          yT λ
                                                   µ=          ,
                                                           m
                                   n                                            o
                        α̂aff = max α ∈ (0, 1] | (y, λ) + α(∆y aff , ∆λaff ) ≥ 0 ,
         and
                                          (y + α̂aff ∆y aff )T (λ + α̂aff ∆λaff )
                                 µaff =                                           .
                                                             m
         Set the centering parameter to
                                                                3
                                                          µaff
                                                 σ=                   .
                                                           µ
         Solve the given quadratic programming problem with this initialization.

Discussion. This example highlights the distinction between enrichment and normalization. The
context-enriched record preserves the provenance of inserted references in a traceable form, while
the standardized mathematical statement converts those recovered dependencies into a cleaner self-
contained problem for downstream completion and review.

F.4   Example: Self-Contained Target Construction

This example illustrates how a standardized mathematical statement is converted into the final self-
contained informal target. The final target makes domains, definitions, and implicit well-formedness
conditions explicit before Lean formalization.

Input. Cleaned exercise.

         Exercise 8.14. Let C be a polyhedron in Rn described as C = {x | Ax ⪯ b},
         and suppose that {x | Ax ≺ b} is nonempty. (a) Show that the maximum volume
         ellipsoid enclosed in C, expanded by a factor n about its center, contains C.


                                                        28
Stage 1. Standardized mathematical statement.

            Let
                                         C = {x ∈ Rn | Ax ⪯ b},
            and assume that the strict inequality system is feasible, i.e.,
                                          {x ∈ Rn | Ax ≺ b} ̸= ∅.
            Show that if an ellipsoid of maximum volume is contained in C, then the ellipsoid
            obtained by expanding it by a factor n about its center contains C.

Stage 2. Self-contained target.

            Let A ∈ Rm×n and b ∈ Rm , and define
                                          C = {x ∈ Rn | Ax ⪯ b},
            where (Ax)i ≤ bi for all i = 1, . . . , m. Assume
                              {x ∈ Rn | (Ax)i < bi for all i = 1, . . . , m} ̸= ∅.
            An ellipsoid in Rn is a set of the form
                                 E = {x ∈ Rn | (x − c)T P −1 (x − c) ≤ 1},
            where c ∈ Rn and P ∈ Rn×n is symmetric positive definite. For α > 0, define
            the expansion of E about its center c by
                                  c + α(E − c) = {c + α(x − c) | x ∈ E}.
            Show that if E is a maximum-volume ellipsoid contained in C, then c + n(E − c)
            contains C.

Discussion. The final target preserves the original mathematical task while making the objects
needed for a formal theorem statement explicit. In particular, it specifies the dimensions of A and
b, expands the componentwise inequality notation, defines the ellipsoid model, and formalizes the
expansion operation about the center.

F.5       Example: Multi-Block Decomposition

We illustrate the block decomposition (Section C.1) with Exercise 3.12 from the Boyd–Vandenberghe
extra exercises, which concerns a trace-minimization semidefinite program (SDP). The preprocessor
decomposes the exercise into four ordered records:


 index       kind         term                       content (abbreviated)
      4      defn         semidefinite program       A semidefinite program
                                                                           has asymmetric-matrix variable. . .
                                                                          A   B
      5      opt_prob     trace minimization SDP     minimize tr X s.t.            ⪰0
                                                                          B⊤ X
      6      thm          —                          Show X = B ⊤ A−1 B solves the SDP.
      7      thm          —                          Conclude (A, B) 7→ tr(B ⊤ A−1 B) is convex.

The four records are translated according to their semantic roles. Block 4 (defn) is retained as
provenance and contextual information, but it does not necessarily produce a standalone Lean
declaration. Block 5 (opt_prob) is translated into Lean declarations that encode the problem data,
the feasibility predicate, and the objective function. In the generated Lean file, these declarations
appear under explicit block-boundary comments:
/- [BLOCK Exercise 3.12 | 5 | opt_prob] -/
structure TraceMinimizationSDP (m n : N) where
 A    : Matrix (Fin m) (Fin m) R
 A_symm : A⊤ = A
 A_posDef : Matrix.PosDef A
 B    : Matrix (Fin m) (Fin n) R


                                                      29
def TraceMinimizationSDP.isFeasible {m n : N}
  (P : TraceMinimizationSDP m n)
  (X : Matrix (Fin n) (Fin n) R) : Prop :=
 X⊤ = X ∧ Matrix.PosSemidef (P.blockMatrix X)

def TraceMinimizationSDP.traceObjective {m n : N}
  (P : TraceMinimizationSDP m n)
  (X : Matrix (Fin n) (Fin n) R) : R :=
 Matrix.trace X

Blocks 6 and 7 become separate Lean theorem targets with by sorry proof bodies. These proof
placeholders are intentional: they mark the targets that are later passed to downstream proof generation
and verification.

/- [BLOCK Exercise 3.12 | 6 | thm] -/
theorem traceMinimizationSDP_solution
  {m n : N} (P : TraceMinimizationSDP m n) :
  P.isFeasible (P.B⊤ ∗ P.A−1 ∗ P.B) ∧
   ∀ X : Matrix (Fin n) (Fin n) R, P.isFeasible X →
    Matrix.trace (P.B⊤ ∗ P.A−1 ∗ P.B) ≤ Matrix.trace X := by
 sorry

/- [BLOCK Exercise 3.12 | 7 | thm] -/
theorem trace_btranspose_inv_mul_b_convex_on {m n : N} :
  ConvexOn R
   {p : Matrix (Fin m) (Fin m) R × Matrix (Fin m) (Fin n) R |
     p.1⊤ = p.1 ∧ Matrix.PosDef p.1}
   (fun p => Matrix.trace (p.2⊤ ∗ p.1−1 ∗ p.2)) := by
 sorry

The block-boundary comments, such as /- [BLOCK Exercise 3.12 | 6 | thm] -/, are in-
serted by the orchestrator before each generated declaration. They make the Lean artifact traceable
back to the corresponding semantic record.

F.6   Example: One Translation–Repair Cycle

We illustrate the compilation-repair loop (Section C.2) with the thm block for Exercise 3.7-(b), which
asks to show that a power-constraint set is convex. The translator’s first attempt used an invalid
summation form for the target Lean 4 environment:
-- First attempt: compile fails.
theorem power_constraint_set_convex
  (m n : N) (hm : 10 ≤ m) (a : Fin n → Fin m → R)
  (I_des : R) (hI : 0 < I_des) :
  Convex R {p : Fin m → R |
   (∀ j, 0 ≤ p j) ∧
   ∀ S : Finset (Fin m), S.card = 10 →
     Σ j in S, p j ≤ (1 / 2 : R) ∗ Σ j : Fin m, p j} := by
 sorry

Lean emitted the following diagnostic:
unexpected token ′ in′ ; expected ′ ,′
 Σ j in S, p j ≤ (1 / 2 : R) ∗ Σ j : Fin m, p j

The repair step receives this diagnostic together with the frozen Lean prefix. It then rewrites only the
current block, replacing the unsupported notation with a Lean 4-compatible expression:
-- Repair r = 1: compile succeeds.
theorem power_constraint_set_convex
  (m n : N) (hm : 10 ≤ m) (a : Fin n → Fin m → R)
  (I_des : R) (hI : 0 < I_des) :


                                                  30
     Convex R {p : Fin m → R |
      (∀ j, 0 ≤ p j) ∧
      ∀ S : Finset (Fin m), S.card = 10 →
       Finset.sum S p ≤ (1 / 2 : R) ∗ Σ j : Fin m, p j} := by
    sorry

The combined Lean file compiles after one repair attempt, so the corrected block is accepted and
frozen. Later blocks can use it as read-only context, but the repair loop is not allowed to modify it
again.

F.7     Example: One Semantic Review–Rewrite Cycle

We illustrate the semantic review loop (Section C.3) with the thm block for Exercise 9.4-(a) in
Numerical Optimization. The exercise asks to show that six distinct collinear points in R2 do not
uniquely determine a quadratic. The initial translation produced a Lean statement that compiled, but
its hypothesis did not faithfully encode collinearity:
-- Compilable but semantically incorrect.
theorem six_collinear_points_do_not_determine_quadratic_uniquely
  (P : Fin 6 → R × R)
  (hcol : ∃ A B C : R,
   A ̸= 0 ∨ B ̸= 0 ∧
   ∀ i : Fin 6, A ∗ (P i).1 + B ∗ (P i).2 = C)
  (hdistinct : Function.Injective P) :
  ∃ q1 q2 : R × R → R, q1 ̸= q2 ∧
   q1 ̸= q2 ∧
   ∀ i : Fin 6, q1 (P i) = q2 (P i) := by
 sorry

Because ∧ binds more tightly than ∨, the hypothesis hcol is parsed as
                                                                        
                     ∃A B C, A ̸= 0 ∨ B ̸= 0 ∧ ∀i, A(Pi )1 + B(Pi )2 = C .

Thus, in the branch A ̸= 0, the theorem imposes no line constraint on the six points. The semantic
reviewer therefore flags a missing_assumption issue:
{
    "math_equivalent": false,
    "overall_status": "not_usable_yet",
    "dominant_issue_types": ["missing_assumption"],
    "top_priority_fix":
     "Fix logical grouping in hcol: require (A ̸= 0 ∨ B ̸= 0)
         and the pointwise line condition together.",
    "issues": [{
     "severity": "P0",
     "issue_type": "missing_assumption",
     "reason":
       "In the A ̸= 0 branch, no condition is imposed on the points,
           so collinearity is not actually assumed.",
     "suggested_fix":
       "∃ A B C : R, (A ̸= 0 ∨ B ̸= 0) ∧
           ∀ i : Fin 6, A ∗ (P i).1 + B ∗ (P i).2 = C"
    }]
}

The semantic rewrite step corrects the logical grouping while preserving the surrounding theorem
structure:
-- After semantic rewrite: compile succeeds and reviewer accepts.
theorem six_collinear_points_do_not_determine_quadratic_uniquely
  (P : Fin 6 → R × R)
  (hcol : ∃ A B C : R,
   (A ̸= 0 ∨ B ̸= 0) ∧
   ∀ i : Fin 6, A ∗ (P i).1 + B ∗ (P i).2 = C)


                                                 31
  (hdistinct : Function.Injective P) :
  ∃ q1 q2 : R × R → R, q1 ̸= q2 ∧
   q1 ̸= q2 ∧
   ∀ i : Fin 6, q1 (P i) = q2 (P i) := by
 sorry

The rewritten statement compiles immediately, so no additional compilation-repair sub-loop is
triggered. This example shows why semantic review is needed even after Lean accepts the file:
a precedence error can silently weaken a mathematical assumption without causing a compiler
diagnostic.

F.8   Example: Source-Level Review

This example shows representative source-level review records. Each record compares the final
informal target against the original problem and assigns a review label such as accept, revise, or
hold. The records are shown in their original JSON-style format.


  [
      {
        "case": "accept",
        "source_idx": "Exercise 7.2",
        "source": "book/Numerical Optimization_Chp7",
        "problem": "Show that the matrix Ĥk+1 in (7.21) is singular.",
        "problem_finally": "Let f : Rn → R be differentiable, and let sk , yk , pk ∈ Rn
         satisfy ykT sk ̸= 0. Define Ĥk+1 = I − sk ykT /(ykT sk ), where I is the n × n
         identity matrix. Suppose pk+1 = ... = −Ĥk+1 ∇fk+1 . Show that Ĥk+1 is
         singular.",
         "semantic_report": {
           "overall_status": "accept",
           "reason": "The final version preserves the original goal, makes the
         needed nonzero denominator assumption explicit, is self-contained, and
         remains theorem-style. Boundary case check: even for n = 1,
         Ĥk+1 = 1 − (sk yk )/(yk sk ) = 0, so singularity still holds.",
           "issues": []
         }
      },
      {
         "case": "revise / missing_assumption",
         "source_idx": "Exercise 14.8",
         "source": "book/Numerical Optimization_Chp14",
         "problem": "Prove that the coefficient matrix in (14.16) is nonsingular if
         and only if A has full row rank.",
         "problem_finally": "Let m, n ∈ N, let A ∈ Rm×n , and let X, S ∈ Rn×n be
         diagonal matrices. Prove that the block matrix [[0, AT , I], [A, 0, 0], [S, 0, X]] is
         nonsingular if and only if A has full row rank.",
         "semantic_report": {
           "overall_status": "revise",
           "reason": "The final statement drops the interior-point context
         assumption that X and S have positive/nonzero diagonal entries. As
         written it is false: if A has full row rank but X = 0 and S = 0, the block
         matrix is singular.",
           "true_issue": "missing_assumption",
           "suggestion_fix": "Add that X and S are diagonal matrices with strictly
         positive diagonal entries, equivalently invertible diagonal matrices."
         }
      },
      {
         "case": "revise / task_drift",
         "source_idx": "Exercise 7.7",
         "source": "book/Numerical Optimization_Chp7",
         "problem": "Minimum surface problem. Divide each edge of the unit square
         into q intervals, label the (q + 1)2 grid points row by row, approximate



                                                32
         derivatives by finite differences, and show that fj has the displayed form
         involving (xj − xj+q+1 )2 and (xj+1 − xj+q )2 .",
        "problem_finally": "Let q ≥ 1. Divide [0, 1]2 into q × q subsquares. Label the
         (q + 1)2 grid points row by row. For each subsquare Aj , indexed by its
         lower-left vertex, let its four vertices correspond to xj , xj+1 , xj+q ,
         xj+q+1 . Show the approximate area
                                          P contribution formula and determine the
         interior variables minimizing      j fj (x).",
        "semantic_report": {
           "overall_status": "revise",
           "reason": "The final version changes the subsquare vertex indexing. With
         row-by-row indexing on a grid of width q + 1, the vertical offset should be
         q + 1, not q. This is a substantive mathematical drift and conflicts with
         the formula.",
           "true_issue": "task_drift",
           "suggestion_fix": "Use vertices xj , xj+1 , xj+q+1 , xj+q+2 consistently, or
         otherwise repair the indexing."
         }
      },
      {
         "case": "hold / missing_dependency",
         "source_idx": "Exercise 7.3",
         "source": "book/Numerical Optimization_Chp7",
         "problem": "Derive the formula (7.23) under the assumption that line
         searches are exact.",
         "problem_finally": "Let f : Rn → R be differentiable. For each iteration k,
         let xk+1 , pk , yk , and Hk+1 be such that the expressions are defined.
         Assume exact line search, so ∇f (xk+1 )T pk = 0, and assume ykT pk ̸= 0. Derive
         pk+1 = −Hk+1 ∇f (xk+1 ) = −∇f (xk+1 ) + ...pk .",
         "semantic_report": {
           "overall_status": "hold",
           "hold_reason_type": "missing_dependency",
           "reason": "The statement asks to derive formula (7.23) but does not give
         the defining relation for Hk+1 or the algorithmic update context. Thus the
         conclusion does not follow from the stated assumptions.",
           "suggestion_fix": "Restate the missing update relation or prior formula
         defining Hk+1 and pk+1 ."
         }
      },
      {
         "case": "hold / unsuitable_lean",
         "source_idx": "Exercise 18.5",
         "source": "book/Numerical Optimization_Chp18",
         "problem": "Consider the constraint x21 + x22 = 1. Write the linearized
         constraints (18.7b) at the points (0, 0)T , (0, 1)T , (0.1, 0.02)T , and −(0.1, 0.02)T
         .",
         "problem_finally": "Let c : R2 → R be c(x) = x21 + x22 − 1. For a point xk ,
         define ck = c(xk ) and Ak = ∇c(xk )T . The linearized equality constraint is
         Ak p + ck = 0. Write this constraint explicitly at the four listed points.",
         "semantic_report": {
           "overall_status": "hold",
           "hold_reason_type": "unsuitable_lean",
           "reason": "The statement is self-contained and faithful, but the task is
         phrased as a compute/write-out exercise rather than a theorem-style
         proposition suitable for Lean formalization.",
           "suggestion_fix": "Rewrite as explicit theorem statements giving the four
         resulting linearized constraints."
         }
      }
  ]




Discussion. These examples show how the semantic reviewer separates faithful, self-contained
targets from cases requiring repair or exclusion. The revise cases are locally repairable, while the
hold cases require missing dependencies or task-form issues to be resolved before formalization.


                                                33
F.9     Example: Constrained Repair and Re-review

This example shows two representative repair cases. The first is a local assumption-restoration case
that remains in the revise path. The second begins as a hold case because the task form is not yet
suitable for Lean and a missing definition issue must also be resolved before a precise theorem-style
target can be stated.

F.9.1     Case 1: Revise / Missing Assumption

      {
           "source_idx": "Exercise 14.8",
           "repair_type": "revise / missing_assumption",
           "original_problem": "Exercise 14.8. Prove that the coefficient matrix in (14.16) is nonsingular
        if and only if A has full row rank.",
           "before_repair_problem_finally": "Let m, n ∈ N, let A ∈ Rm×n , and let X, S ∈
           n×n
        R       be diagonal matrices. Prove that the block matrix
                                                                
                                                    0 AT I
                                                  A      0    0
                                                    S     0   X
        is nonsingular if and only if A has full row rank.",
           "repair_reason": "The original context needs X and S to be positive/invertible diagonal
        matrices. Without this, e.g. X = 0 and S = 0 gives a singular block matrix even when A has full
        row rank.",
           "after_repair_problem_finally": "Let m, n ∈ N, let A ∈ Rm×n , and let X, S ∈ Rn×n
        be diagonal matrices with strictly positive diagonal entries. Prove that the block matrix
                                                                 
                                                     0 AT I
                                                   A     0    0
                                                     S    0    X
      is nonsingular if and only if A has full row rank."
      }


F.9.2     Case 2: Hold / Unsuitable Lean and Missing Definition

      {
          "source_idx": "Exercise 7.4",
          "repair_type": "hold / unsuitable_lean + missing_def",
          "original_problem": "Exercise 7.4. Consider limited-memory SR1 updating based on (7.30).
        Explain how the storage can be cut in half if the basic matrix B0k is kept fixed for all k. (Hint:
        Consider the matrix Qk = [q0 , . . . , qk−1 ] = Yk − B0 Sk .)",
          "before_repair_problem_finally": "Consider the limited-memory SR1 update with mem-
        ory parameter m ∈ N. For iteration k, let p = min{k, m}, and let the stored quasi-Newton pairs
        be sℓ , yℓ ∈ Rn . Define Sk = [ sk−m , . . . , sk−1 ] ∈ Rn×p and Yk = [ yk−m , . . . , yk−1 ] ∈ Rn×p ,
        and define the strictly lower-triangular matrix Lk by
                                               (
                                                 (sk−m−1+i )T yk−m−1+j , i > j,
                                   (Lk )i,j =
                                                 0,                         i ≤ j.

        Assume that the basic matrix is fixed for all k, so B0k = B0 ∈ Rn×n for every k. Define
        Qk = [q0 , . . . , qp−1 ] = Yk − B0 Sk , with qi = yi − B0 si for each stored pair. Explain how the
        storage can be reduced by one-half under the assumption that B0k is fixed for all k.",
           "repair_reason": "Before repair, the statement remains open-ended because it asks the reader
        to explain how the storage reduction works, which is not suitable as a Lean theorem target. In
        addition, the column indices qi of Qk are inconsistent with the storage-window indexing used for Sk
        and Yk .",
           "after_repair_problem_finally": "Let m ∈ N, let k ∈ N, and let p = min{k, m}. For
        the stored quasi-Newton pairs (sj , yj ) ∈ Rn × Rn , define Sk = [sk−p , . . . , sk−1 ] ∈ Rn×p and
        Yk = [yk−p , . . . , yk−1 ] ∈ Rn×p . Assume the basic matrix is fixed, i.e. B0k = B0 ∈ Rn×n for all



                                                         34
       k. For i = 0, . . . , p − 1, define
                                             qi := yk−p+i − B0 sk−p+i ,
       and let
                                       Qk = [q0 , . . . , qp−1 ] = Yk − B0 Sk .
       Define the strictly lower-triangular matrix Lk ∈ Rp×p by
                                     (
                                      sTk−p+i yk−p+j , i > j,
                         (Lk )i,j =                                    (i, j = 0, . . . , p − 1).
                                      0,                    i ≤ j,

       Prove that for all i > j,
                                      (Lk )i,j = sTk−p+i qj + sTk−p+i B0 sk−p+j .
       Hence, when B0 is fixed, the information needed to form Lk can be recovered from Sk , Qk , and
       B0 , so it is unnecessary to store both Yk and Qk ; equivalently, one may replace storage of the pair
       (Sk , Yk ) by storage of (Sk , Qk ), which cuts the storage for the update pairs in half."
       }


Discussion. These two cases illustrate the intended boundary of constrained repair. In the first case,
the reviewer identifies a single missing assumption, and the repair restores the positivity condition
needed for the original equivalence to be correct. In the second case, the original target is not merely
incomplete but also unsuitable for direct formalization: the open-ended instruction must be converted
into a precise theorem-style statement, and the indexing of the stored quantities must be aligned
before re-review can succeed.

F.10     Examples: Representative formalization failures

Library/API grounding. For example, in a convexity target about monotonicity of gradients, the
final snapshot contains:
theorem gradient_monotone_of_convex_differentiable
    {n : N}
    {f : EuclideanSpace R (Fin n) → R}
    (hconv : ConvexOn R Set.univ f)
    (hfdiff : Differentiable R f) :
    MonotoneMap (fun x => gradient f x) := by
  intro x y
  simpa [gradient, sub_eq_add_neg, inner_add_left, inner_add_right,
    inner_neg_left, inner_neg_right]
    using hconv.monotoneOn_gradient hfdiff x (by simp) y (by simp)


The intended mathematical route is reasonable: convex differentiable functions have monotone
gradients. However, the proof is not grounded in actual Lean/Mathlib declarations. The compiler
reports an invalid-field error for monotoneOn_gradient.
Formal representation and type discipline. Matrix-analysis targets often expose the gap between
informal linear algebra notation and Lean’s exact representation of dimensions, indices, rank, and
positive-definiteness predicates.
theorem full_column_rank_iff_transpose_mul_self_posDef
    {m n : Type∗ } [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]
    (h : Fintype.card n ≤ Fintype.card m) (J : Matrix m n R) :
    J.rank = Fintype.card n ↔
      Matrix.PosDef (J.transpose ∗ J) := by
  simpa [Matrix.posDef_iff]
    using Matrix.rank_transpose_mul_self_eq_card_iff_posDef
      (m := m) (n := n) J


This proof mirrors the standard informal theorem that full column rank is equivalent to positive
definiteness of J ⊤ J. The Lean attempt fails because the required representation bridge is not
available under these names: the compiler reports unknown constants such as Matrix.posDef_iff
and Matrix.rank_transpose_mul_self_eq_card_iff_posDef. The failure is therefore not
just a missing algebraic idea; it reflects the need to align the informal matrix theorem with Mathlib’s
actual rank API, matrix index types, and positive-definiteness definitions.


                                                           35
Proof decomposition and long-horizon control. Agentic systems also fail when a proof requires
a long chain of auxiliary analytic lemmas. In an Aristotle run on problem-77.lean, the target is
Q-linear convergence of Newton’s method at a multiple root:
theorem classicalNewtonIteration_multipleRoot_qLinear
    (N : ClassicalNewtonIteration)
    (hroot : IsMultipleRoot N.f 0)
    (hf′ _correct : ∀ x : R, N.f′ x = deriv N.f x)
    (hC1 : ∃ s : Set R, s ∈ K 0 ∧ ContDiffOn R 1 N.f s) :
    IsQLinearlyConvergentTo N.xSeq 0 := by
  sorry

The run did make structured progress: its summary reports helper lemmas such as
f_zero_of_multipleRoot,      hasDerivAt_zero_of_multipleRoot,       seq_ne_zero,
newton_step_eq, and newton_contraction_ratio. The remaining gap was the analytic
lemma newton_ratio_tendsto, which must show that
                                    xm−1
                                     k   g(xk )/f ′ (xk ) → 1/m
along the Newton sequence. This is not a local syntax error: closing the proof requires maintaining a
convergence argument through multiple helper lemmas, derivative facts, and asymptotic estimates.
It is representative of long-horizon proof-control failures on optimization and numerical-analysis
targets.

G     Prompt Templates
This appendix lists the prompt templates used in the benchmark construction and evaluation pipeline.
The prompts are organized in the same order as the pipeline: raw exercise cleaning, self-contained
target construction, source-level review, constrained repair, JSON-to-Lean translation, and pass@k
proof generation.

G.1   Raw-to-Clean Prompt

This prompt is used to construct the problem_clean field from the raw extracted exercise. Its purpose
is to remove non-essential hints, remarks, background narrative, and implementation-oriented text
while preserving the mathematical statement and all meaningful references.

Prompt template.

  You are a preprocessing cleaner for optimization and mathematics exercise
      statements.
  Role.
  Your task is to remove hint/remark prompt-like information and background
      narrative from the original problem statement, while keeping all valid
      mathematical information unchanged, keeping all tags unchanged, and
      cleaning the original problem text only.
  Input.
  A single JSON object with a field problem containing raw exercise text.
  Rules.
  1. Preserve the mathematical meaning exactly.
  2. Preserve symbols, formulas, numbering, and mathematically meaningful
      references.
  3. Do not delete, alter, renumber, or rewrite any referenced identifier or
      index, including equation numbers, theorem numbers, algorithm numbers,
      exercise numbers, part labels, and cross-references such as "as in (4.13)",
      "part (b)", "Theorem 12.1", or "Algorithm 3.2".
  4. Preserve referential links exactly: if a clause refers to an earlier object
      by number or label, keep that number or label unchanged and attached to the
      same object.
  5. Do not change the task intent, target, or scope. For example, do not convert
      "prove" to "compute", do not replace "minimum and maximum" with only
      "minimum", and do not weaken or strengthen quantifiers or assumptions.
  6. Cleaning only: remove noise, wrappers, and non-mathematical exposition, but
      do not rewrite core mathematical content into a different statement.



                                                 36
7. Do not introduce new claims, examples, explanations, or solution steps.
8. Mandatory boundary-case safeguard: before treating a cleaned statement as
    acceptable, explicitly check edge cases such as nonemptiness and
    zero-valued conditions. If an edge case fails, construct a concrete
    counterexample and treat the item as needing revise with a clear reason in
    downstream review.
You must always produce a cleaned version that is shorter or at least
    meaningfully rewritten compared to the input. Never return the input text
    unchanged.
Primary objective.
Keep only mathematically essential content. Delete all irrelevant exposition.
    The cleaned result should read like a compact mathematical problem
    statement, not like textbook narration, software instructions, or
    pedagogical commentary.
Lean-oriented principle.
Treat the input as material to be normalized before formalization.
Prefer content that can later become:
1. definitions;
2. hypotheses;
3. variables and domains;
4. assumptions and constraints;
5. equations and inequalities;
6. precise goals and conclusions.
Delete anything that does not help identify or formalize these items. Default
    to deletion.
Keep only the following content:
1. exercise numbers, part labels, and mathematically meaningful
    cross-references such as 4.13, (a), Theorem X.Y, Algorithm X.Y, equation
    (15), or part (b);
2. definitions, notation, symbol declarations, and domain declarations;
3. assumptions, hypotheses, regularity conditions, feasibility assumptions, and
    rank or positivity assumptions;
4. optimization variables, objectives, constraints, equalities, inequalities,
    quantifiers, and formulas;
5. dual problems, KKT conditions, conjugates, SDP/QP/SOCP/LP formulations,
    feasibility claims, and exact statements of derived reformulations when
    they are part of the problem;
6. explicit problem data needed for the statement, including matrices, vectors,
    dimensions, constants, tolerances, and named data files when required to
    define the task;
7. the actual task directives, such as show, prove, derive, find, compute,
    determine, formulate, verify, construct, characterize, or solve;
8. minimal clarifying text only if removing it would destroy mathematical
    meaning.
Delete aggressively:
1. motivational background, applications, interpretation, intuition, historical
    remarks, and storytelling, including introductory sentences that describe
    why a topic is useful or interesting;
2. audience-directed wording such as "you may", "you will", "you should", "you
    need", "your job is", "we seek", "we consider", "we are interested in", "as
    a courtesy", "answer the following", "you should feel free to", and similar
    phrases;
3. all Hint, Hints, Remark, Remarks, Note, and Notes sections as labeled
    discourse, including multi-language hint blocks such as Matlab/Python/Julia
    subsections inside a Hints section;
4. solution strategies, method suggestions, and pedagogical advice, including
    phrases such as "you can do this by", "one approach is to", "a standard
    method", or "a typical method";
5. explanatory prose that merely paraphrases formulas already present;
6. software-tutorial language such as "Hello World", "how to use CVX", "tricks
    for using CVX", or similar presentation wording;
7. MATLAB, Python, Julia, CVX, CVXPY, Convex.jl, solver, and implementation
    instructions, except for mathematical data or tolerances that are part of
    the problem statement;
8. code snippets, random-seed commands, API usage directions, and
    multi-language code blocks, unless the exact numeric instance defined there
    is essential problem data;




                                       37
  9. comments such as "it is easy to see", "roughly speaking", "you can think
      of", "in a few very simple cases", "evidently", "of course", and similar
      non-mathematical narration;
  10. all plotting, graphing, figure-generation, and visualization instructions,
      such as "Plot X vs Y", "Generate a figure", or "Graph the trajectory".
      These are presentation tasks, not mathematical content for formalization;
  11. comparison-to-baseline instructions such as "compare it to the non-hybrid
      version" or "compare with the naive method", unless the comparison itself
      is a mathematical claim to prove;
  12. "Briefly explain why" and "explain your reasoning" wrappers. Keep only the
      underlying mathematical task, such as "Determine whether. . ." or "Show
      that. . .".
  Mandatory treatment of Hint and Remark.
  Delete the labels Hint, Hints, Remark, Remarks, Note, and Notes from the output.
  Do not preserve hint or remark paragraphs as paragraphs.
  If a Hint, Remark, or Note contains indispensable mathematical content, such as
      a formula, inequality, or fact needed to state the problem, extract only
      that mathematical content and merge it into the cleaned problem statement
      without the discourse wrapper.
  If a Hint or Remark section consists entirely of software instructions, such as
      MATLAB code, Python snippets, Julia variable declarations, or CVX API
      directions, delete the entire section with no extraction.



G.2   Self-Contained Target Construction Prompt

This prompt is used to construct problem_finally from problem_standardized_math, with
problem_with_context used only for explicitly recovered dependencies. Its purpose is to produce
a condition-complete, self-contained informal target before Lean formalization.


Prompt template.

  You are given one optimization exercise statement.
  Rewrite it into a condition-complete, self-contained, textbook-style problem.
  Input use rule.
  - Primary source: problem_standardized_math. Preserve its task intent, core
      assumptions, and structure first.
  - Secondary source: problem_with_context. Use it only to supplement missing
      dependency assumptions or formulas, including Reference, Double, Third, or
      More reference lines, when clearly relevant.
  - Before all other processing, ignore any hint/hints content entirely; hint
      text is disposable and must not be used in rewriting.
  - If problem_standardized_math and problem_with_context differ, prefer
      problem_standardized_math unless context provides explicit supporting
      mathematics needed for completeness.
  - If problem_standardized_math lacks necessary mathematical support, such as
      assumptions, formulas, or definitions, explicitly retrieve and integrate
      that support from problem_with_context.
  - Keep strict dependency folding: third-hop to second-hop, second-hop to
      first-hop, and first-hop to the original problem. If more-level
      dependencies exist, unfold and fold them layer-by-layer before final
      rewrite.
  - Carefully check that every concept, symbol, function, and operator used in
      the problem is defined. If any definitions are missing, add precise
      definitions so the problem is fully self-contained and suitable for
      formalization.
  Hard constraints.
  - Do not solve the problem.
  - Do not use, preserve, paraphrase, or output any hint/hints text; discard
      hints directly.
  - Do not rewrite, split, reorder, or restate the original task objective in any
      form.
  - The task objective must remain strictly identical to
      problem_standardized_math.
  - Only identify and explicitly add implicit assumptions or conditions that are
      directly supported by input context.



                                              38
  - Add only information that is genuinely useful for mathematical completeness,
      dependency resolution, or precise definition; do not add irrelevant
      background, commentary, examples, or decorative exposition.
  - Keep the original mathematical intent and task type.
  - Do not add unnecessary stronger assumptions.



G.3   Source-Level Review Prompt

This prompt is used to review each problem_finally against the original problem. The reviewer
checks mathematical faithfulness, self-containedness, missing assumptions, unresolved dependencies,
and suitability for Lean formalization.

Prompt template.

  Role.
  You are reviewing a mathematical exercise for Lean formalization readiness.
  Your task is to determine whether the candidate final version preserves the
      original mathematical meaning, includes all necessary assumptions, is fully
      self-contained, and is suitable for Lean formalization.
  You are not asked to improve wording for style alone. Focus on mathematical
      faithfulness, completeness, self-containedness, and formalizability.
  Before deciding accept, you must explicitly check boundary cases such as
      nonemptiness and zero-valued edge conditions. If a boundary case fails,
      provide a concrete counterexample.
  Core objective.
  Compare problem_finally against problem.
  Your review must answer four questions:
  1. Does problem_finally preserve all assumptions from the original problem?
  2. Does problem_finally preserve the original task and conclusion without drift?
  3. Is problem_finally fully self-contained?
  4. Is the resulting task suitable for Lean formalization?
  Review scope.
  You must check:
  - whether any assumption has been lost;
  - whether any assumption has been changed;
  - whether any quantifier or logical direction has changed;
  - whether any domain restriction has changed;
  - whether any conclusion has been dropped;
  - whether any conclusion has been added;
  - whether any required dependency is missing;
  - whether any technical term or function is used without definition;
  - whether the task is actually formalizable in Lean.
  Detailed review criteria.
  1. Assumption preservation.
  Check whether problem_finally is missing any assumption that is explicit or
      implicit in problem. Examples include nonzero assumptions, nonnegative
      assumptions, positivity assumptions, positive-definite assumptions, domain
      restrictions, index range restrictions, quantifier scope restrictions,
      existence conditions, uniqueness conditions, continuity, differentiability,
      integrability, measurability, boundedness, invertibility, and other
      regularity or well-posedness conditions. If a necessary assumption from
      problem is absent in problem_finally, flag missing_assumption.
  2. Task preservation.
  Check whether the mathematical task in problem_finally is still the same as in
      problem. Pay special attention to non-equivalent drift, including changing
      exists to forall, changing equivalence to one-way implication, dropping one
      direction of a two-sided result, changing the domain or scope of variables,
      weakening or strengthening the conclusion, removing a conclusion, or adding
      a new conclusion. Equivalent reformulations are acceptable only when they
      are genuinely mathematically equivalent. If the final version changes the
      task in a non-equivalent way, flag task_drift.



                                                39
  3. Self-containedness.
  Check whether problem_finally can be understood and formalized on its own. Flag
      missing_dependency if the statement relies on something not actually
      included or specified, such as a missing tag or unresolved reference, a
      missing theorem, lemma, proposition, corollary, or algorithm, a missing
      dependency on another exercise or previous result, or a required cited fact
      that is not stated clearly enough to use. When judging missing_dependency,
      read the full text carefully and confirm that the dependency is genuinely
      absent, rather than merely named while its relevant mathematical content
      has already been restated in the problem itself. Also flag
      missing_dependency if problem_finally refers to a tag, Theorem X.Y, Alg.
      X.Y, Algorithm X.Y, part (b), or another exercise-internal reference, but
      does not explain or restate the referenced content clearly enough for the
      statement to stand on its own.
  4. Missing definitions.
  Check whether problem_finally uses a specialized, uncommon, or technical term
      without defining it. Also flag this issue if a function, operator, mapping,
      object, or construction is used without a definition precise enough for
      formalization. Examples include uncommon terms or symbols such as
      ill-conditioned, L(x,y), or similarly specialized notation introduced
      without any definition. If this happens, flag missing_def.
  5. Formalizability.
  Judge whether the task is suitable for Lean formalization. Usually suitable:
      proof-oriented mathematical statements, precisely stated claims with
      explicit mathematical objects and conclusions, and mathematically precise
      computational statements. Usually not suitable: give a description,
      formulate, compute, plot, sketch, discuss informally, open-ended
      explanatory tasks, or tasks whose result is mainly visual, rhetorical, or
      pedagogical rather than formally mathematical. If problem_finally contains
      verbs such as formulate, compute, or similar wording that is not suitable
      for Lean formalization as a precise theorem-style target, judge the task as
      not suitable for Lean formalization and choose hold. If the task itself is
      not suitable for Lean formalization, the overall status should be hold.



G.4   Constrained Repair and Re-review Prompt

This prompt is used when the source-level reviewer classifies an instance as repairable. The repair
step is constrained to modify only problem_finally; earlier fields remain fixed as audit anchors.

Prompt template.

  Your task is to rewrite only problem_finally, using the review result and the
      provided fix suggestions, so that the final statement is mathematically
      faithful to the original task, self-contained, and easier to formalize in
      Lean.
  You must read the input very carefully. You will be audited after your rewrite.
  Be precise, conservative, and faithful to the given instructions.
  Rewrite problem_finally according to the repair suggestions.
  Your goal is to produce a corrected problem_finally that:
  1. preserves the original mathematical meaning of problem;
  2. follows the correction instructions in value_true_issues;
  3. remains consistent with problem_clean and problem_standardized_math;
  4. is self-contained, mathematically precise, and suitable for Lean
      formalization.
  You must rewrite problem_finally.
  You must not change any other field.
  Do not output overall_status, reason, or value_true_issues.
  Do not introduce any new correction that is not required by the provided review
      reasons and suggestions.
  Do not add extra assumptions, conclusions, definitions, or reformulations
      beyond what is needed to carry out the stated repair.
  Do not improve style for its own sake.



                                                40
  You must read reason and value_true_issues carefully.
  Use them as the direct authority for what needs to be fixed.
  Add back the missing assumption exactly as needed, without changing the
      mathematical task.
  Rewrite problem_finally so that it matches the original task in problem again.
  Restore the correct variables, domain, quantifiers, logical direction, and
      conclusion.
  Add the missing definition or make the relevant notion explicit, but only to
      the extent required by the repair suggestion.
  Apply all repair suggestions together, but keep the final statement minimal and
      faithful.
  Priority of authority:
  1. problem is the source of truth for the original mathematical task.
  2. value_true_issues and reason tell you exactly what must be repaired.
  3. problem_standardized_math helps preserve the already standardized
      mathematical structure.
  4. problem_clean helps remove irrelevant textbook narrative.
  5. problem_with_context may be consulted only when needed to resolve ambiguity,
      not to invent new content.
  If these sources conflict, preserve the original mathematical intent of problem
      and follow the explicit repair instructions.
  Do not:
  - modify problem, problem_clean, or problem_standardized_math;
  - add new assumptions not justified by the repair feedback;
  - weaken the conclusion;
  - strengthen the conclusion;
  - introduce a new proof strategy;
  - insert hints or remarks;
  - output analysis, commentary, or explanation outside the JSON.
  All fields except problem_finally must remain unchanged from the input.
  Before you output, verify all of the following:
  1. Only problem_finally has been changed.
  2. The rewrite follows the provided repair suggestions.
  3. The rewritten problem_finally does not introduce any extra content beyond
      the required repair.
  4. The rewritten problem_finally is self-contained and suitable for Lean
      formalization.
  5. The output is valid JSON.
  6. Mandatory boundary-case safeguard: explicitly check edge conditions such as
      nonemptiness and zero-valued cases for the repaired statement. If an edge
      case fails, produce a concrete counterexample in your verification and
      treat the item as requiring revise with a clear reason in downstream review.
  Your job is not to generate a better problem in general.
  Your job is to repair problem_finally, and only problem_finally, so that it
      correctly reflects the original task and the given review suggestions.



G.5   Compact Translator Prompt

This prompt is used for the initial JSON-to-Lean translation stage. It translates one semantic block at
a time into a Lean declaration while reusing previously accepted declarations from the frozen context.

Prompt template.

  You are a JSON-to-Lean block translator.
  Input.
  - current JSON semantic block with fields such as index, source, source_idx,
      kind, term, content, and problem;
  - section_context: previously accepted Lean declarations in the same namespace;
  - optional mcp_context or external source context.
  Task.



                                                  41
  Translate exactly one JSON semantic block into one Lean 4 declaration, plus
      helper declarations only when necessary. Reuse existing declarations from
      section_context whenever possible. Output only the Lean code fragment for
      the current block.
  Use semantic content in this priority order:
  1. content;
  2. problem;
  3. term, only as a naming or contextual hint.
  Declaration rules by kind:
  - defn: produce one source-faithful Lean def. Do not use sorry or vacuous
      bodies.
  - thm: produce exactly one theorem as the primary declaration. Keep all source
      assumptions explicit. Use a concise, semantic, Lean-safe name. The proof
      body must be exactly "by sorry".
  - algo: produce one structure encoding source-grounded algorithmic state,
      parameters, and invariants. Do not encode theorem conclusions as fields.
  - opt_prob: produce one structure encoding decision variables, objectives,
      constraints, and source-grounded optimization components.
  Context reuse rules.
  Before generating code, scan section_context. Reuse matching definitions,
      structures, theorem names, notation, helper predicates, and directives. Do
      not redefine equivalent symbols unless the meaning differs.
  Lean and safety constraints:
  - Output only Lean code for insertion inside the shared namespace.
  - Do not output imports, namespace wrappers, closing "end"s, block comments,
      Markdown fences, JSON/YAML, or explanations.
  - Do not introduce vacuous placeholders such as "def X := True", empty Prop
      wrappers, or meaningless predicates.
  - Do not use axiom, admit, unsafe, opaque, or fake mathematical content.
  - For theorem blocks, the only allowed unfinished proof is "by sorry".
  - Preserve source assumptions, equalities, relations, constructions, and
      boundary conditions.
  - Do not weaken or strengthen the source statement except minimally to obtain a
      well-typed Lean formalization.
  - Add open, open scoped, variable, or set_option directives only when needed
      and not already provided by section_context.
  - Prefer Mathlib-native notation and fully qualified names when they avoid
      unnecessary directives.
  - Use "fun" instead of lambda symbols.
  - In structures, put each field on its own line.
  - For Euclidean inner products, use the notation supported by the current Lean
      environment; do not add unsupported scalar-field subscripts.
  Final check.
  The output must preserve the source intent, reuse available context, match the
      required declaration shape for the block kind, avoid placeholders, and
      contain only the Lean fragment for the current block.



G.6     Pass@k Proof-Generation Prompts

These prompts are used in the non-agentic pass@k experiments. Each model receives a Lean block
with one designated proof placeholder, FILL_PROOF_HERE, and returns only the proof body that
replaces it. Other sorry tokens in the template are left untouched.

G.6.1    System Prompt
Prompt template.

  You are a Lean 4 proof assistant. Your task is to fill in exactly one proof
      placeholder.
  Rules.
  - Output only the Lean proof term or tactic body that should replace the /-
      FILL_PROOF_HERE -/ marker.
  - Do not output the surrounding theorem, lemma, or def block.



                                             42
  - Do not output thinking, reasoning, chain-of-thought, analysis, or any hidden
      deliberation; output the code directly.
  - Do not output imports, namespaces, sections, declarations, comments,
      explanations, or Markdown outside one Lean code block.
  - The code you output will be inserted verbatim at the marker. It must fit
      exactly at that position.
  - Do not modify, repeat, comment out, delete, rename, weaken, or otherwise
      alter the original theorem, lemma, or def statement, hypotheses, target,
      imports, namespace, or surrounding code.
  - Do not touch any other sorry tokens already present in the template; they
      belong to later steps.
  - Do not add or use axiom, admit, unsafe, opaque, or proof-search/suggestion
      commands such as apply?, exact?, rw?, simp?, aesop?, solve_by_elim?, or
      library_search.
  - Never use sorry.
  - Before using any lemma, theorem, or definition name, verify it is resolvable
      in the current context.
  - Never guess or invent lemma names based on similarity.
  - If a needed lemma is not resolvable from the search results, either switch to
      available lemmas or define a helper first without sorry, axiom, admit,
      unsafe, or opaque.
  - Wrap your code in a Lean code block.


G.6.2   First-Turn User Prompt
Prompt template.

  Here is a Lean 4 block containing a proof placeholder /- FILL_PROOF_HERE -/ and
      possibly other sorry tokens, which you must leave untouched.
  Lean block.

  {block_code}

  Available tool/search context.

  {mcp_sections}

  Output only the Lean proof term or tactic body that should replace /-
      FILL_PROOF_HERE -/.
  Do not output thinking, reasoning, chain-of-thought, analysis, or any hidden
      deliberation; output the code directly.
  Do not output the theorem, lemma, or def block itself.
  The proof body will be inserted verbatim at the marker.
  If the required lemma or definition is not found in the search results, define
      it yourself first before using it.
  Use exact identifier names from searchable context; do not use similar-looking
      names that are not resolvable.
  Do not use sorry, axiom, admit, unsafe, opaque, apply?, exact?, rw?, simp?,
      aesop?, solve_by_elim?, or library_search.
  Return only the proof body in a Lean code block.


G.6.3   Retry-Turn User Prompt
Prompt template.

  Your previous proof body produced compile errors.
  Here is the original template, your last proof body, and the compiler
      diagnostics.
  Original template with placeholder.

  {block_template}
  Your previous proof body.



                                         43
    {prev_code}
    Compile errors.

    {compile_errors}

    Available tool/search context.

    {mcp_sections}

    Output only the corrected Lean proof term or tactic body that should replace /-
        FILL_PROOF_HERE -/ in the original template.
    Do not output thinking, reasoning, chain-of-thought, analysis, or any hidden
        deliberation; output the code directly.
    Do not output the theorem, lemma, or def block itself.
    The proof body will be inserted verbatim at the marker.
    Keep any other sorry tokens unchanged by not mentioning them.
    If the required lemma or definition is not found in the search results, define
        it yourself first before using it.
    Before writing the final proof, ensure every new identifier you use is
        resolvable; otherwise revise the approach.
    Do not use sorry, axiom, admit, unsafe, opaque, apply?, exact?, rw?, simp?,
        aesop?, solve_by_elim?, or library_search.
    Do not add comments, explanations, or text outside the Lean code block.
    Output only the corrected proof body in a Lean code block.



H     Limitations
CAM-Bench has several limitations. First, although CAM-Bench targets computational and applied
mathematics, its source material is still optimization-centric, with coverage mainly in optimization,
numerical linear algebra, and numerical analysis. Other areas of applied mathematics, such as PDEs,
control, and scientific computing, are not yet systematically covered.
Second, benchmark construction uses an LLM-assisted pipeline for dependency recovery, normal-
ization, Lean formalization, and semantic review. We reduce this risk through source-grounded
dependency expansion, constrained repair, Lean compilation, and semantic validation. However,
subtle mismatches, such as boundary cases may still remain.
Finally, due to computational cost, the external agentic systems are evaluated on 200 uniformly
sampled instances rather than the full benchmark. These results are informative but should be
interpreted as sampled estimates rather than complete measurements over all benchmark instances.

I    Boarder Impacts
CAM-Bench aims to support reliable evaluation of mathematical reasoning systems by providing
Lean-verified proof targets in computational and applied mathematics. By focusing on context-
dependent textbook problems, it helps diagnose failures in assumption tracking, library grounding,
type discipline, and long-horizon proof decomposition. The benchmark may encourage progress
in formal applied mathematics, including stronger Mathlib infrastructure, more capable theorem-
proving agents, and more faithful autoformalization pipelines. It also complements existing formal
benchmarks that primarily emphasize Olympiad-style problems, algebraic domains, or isolated
theorem statements. CAM-Bench should therefore be used as one component of a broader evaluation
suite. Strong performance on this benchmark indicates progress in Lean-based proof generation for
context-dependent applied mathematics.




                                                 44
