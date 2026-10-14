                                               CausalSmith: A Formally Grounded, Self-Improving Agentic
                                                 Framework for Automated Research in Causal Inference
                                                                            Jiyuan Tan          Vasilis Syrgkanis
arXiv:2607.22511v4 [stat.ML] 15 Sep 2026




                                                                                           Abstract
                                                    Automating theoretical research requires generating candidate results and evaluating them
                                                reliably. Models keep getting better at the first, while the second remains hard. A common
                                                approach asks one large language model (LLM) to review what another produced, yet such
                                                reviewers are empirically unreliable: they may accept fabricated papers and catch the fabrication
                                                at close to chance rates [21]. We present CausalSmith, a framework for automated theoretical
                                                research in causal inference built on the Lean proof assistant, where a proof is checked by a
                                                program rather than read by a referee. CausalSmith rests on Causalean, a foundational Lean
                                                library for causal inference holding 8,179 machine-checked definitions and theorems, developed
                                                with language-model assistance under human design and review. Around it we build a self-
                                                improving agentic pipeline that selects research topics, proposes results, formalizes statements,
                                                constructs proofs, and presents the resulting artifacts for human inspection. Moreover, the
                                                pipeline pairs Lean verification with a statement audit that compares each formal theorem against
                                                the informal claim behind it. We evaluate the system using artifacts produced by completed
                                                autonomous research runs. The source code, formal library, and run records are available at
                                                https://github.com/Jiyuan-Tan/CausalSmith.


                                           1    Introduction
                                           Language models can now generate research artifacts—conjectures, proofs, experiments, and complete
                                           papers—more rapidly than they can be evaluated. In empirical fields, this primarily increases the
                                           burden of review. In theoretical work, it presents a more direct risk: an incorrect theorem may
                                           be indistinguishable from a correct one until it is verified by an expert, but expert verification is
                                           slow and costly. Many systems for automated mathematical and theoretical research address this
                                           bottleneck by delegating evaluation to another language model: one model proposes and another
                                           reviews.
                                               Empirical evaluations already show the defects of LLM reviewers. Independent evaluations
                                           of the AI-Scientist systems [55] report hallucinated numbers, frequent coding failures, and little
                                           novelty [5]. Jiang et al. [21] further show that LLM reviewers accept deliberately fabricated papers
                                           up to 82% of the time and detect the fabrication at near-chance rates. These findings make LLM
                                           review an unreliable evaluator of correctness.
                                               Formal verification offers a different basis for evaluation. A theorem written in Lean 4 is checked
                                           by a program rather than read by a referee. If Lean 4 accepts the proof, then every step of the
                                           argument has been verified against the axioms, so a gap or a mistake in the reasoning cannot
                                           survive. Grounding a system in Lean 4 takes the correctness of proofs out of a model’s hands entirely.
                                           However, two obstacles stand between that guarantee and an automated system that can use it:
                                           cost and faithfulness.



                                                                                               1
     The first obstacle is cost. Formalizing a result from first principles is slow work, so a system that
proves causal-inference theorems needs a library to start from: identification theorems, estimators,
and asymptotic results already stated and proved in the literature. Without one, every run rebuilds
standard theory before it can reach anything new.
     The second obstacle is faithfulness. Lean 4 checks the proof, but it says nothing about whether the
theorem is the one the system meant to state. As a result, the natural-language statement may not
match the theorem actually proved. Recent work documents this gap from several angles [11, 19, 35],
and we saw it in our own runs. In one, an agent turned the hard lemmas into axioms and produced
Lean 4 code that compiled with axioms standing in for proofs. In another, the model altered a
hypothesis, so the Lean 4 code proved a weaker statement than the paper claimed. Both compile,
and neither is a proof of what was claimed. Our pipeline guards against this with a fine-grained
audit step (Section 5.3) that compares each formal statement with the claim it is meant to express.
Lean 4 checks the proofs the pipeline produces, and the audit checks that the statements they
establish are the ones the paper reports.
     We instantiate this approach in causal inference through CausalSmith, which has two compo-
nents. The first is Causalean, a Lean 4 library covering the causal-inference toolkit, which gives
agents verified pieces to build on. It was itself built with LLM assistance: humans chose what to
formalize and how to state it, agents drafted the definitions, proofs, and docstrings under those
decisions, and a human then reviewed the resulting Lean 4 statements. The second component is a
self-improving agentic pipeline that selects or accepts a research topic, proposes a result, formalizes
it, proves it, and presents it. It audits one statement at a time rather than judging a finished paper
once, and it promotes reusable lemmas into Causalean as they are proved and reviewed.

Contributions.
• Causalean, a broad Lean 4 formalization of causal inference spanning graphical and structural
  causal models, potential outcomes and identification, panel methods, experimentation, estima-
  tion, and statistical theory. It comprises 8,179 machine-checked declarations, meaning named
  definitions and theorems that Lean 4 has verified. It was written with language-model assistance
  under human design, and it provides a retrieval interface for agents (Section 4).
• An end-to-end research pipeline whose Discovery stage can select its own research topic and
  propose a causal-inference result, which the pipeline then formalizes, proves, and presents. It
  also contains a library feedback loop that adds reusable lemmas and theorems proved during a
  run back into Causalean (Sections 5 and 5.3).
• An evaluation drawn from 144 recorded runs: a catalog of machine-checked results and a headline
  result found by the system, which closes a gap in Zeng et al. [60] (Section 6).

CausalSmith pipeline. The pipeline has four stages, shown in Figure 1. Discovery takes a topic
from a researcher or proposes one itself, then solves it in natural language under an adversarial
review of novelty and soundness. We store that solution as a dependency graph: its nodes are the
individual statements of the paper—a setup, a definition, an assumption, a lemma, the headline
theorem—and its edges record which statements a claim uses and which its proof consumes (Figure 2).
Formalization gives every node a Lean 4 declaration, reusing what Causalean already provides,
and the statement audit checks node by node that each declaration says what its node claims. Proof
construction fills those declarations against the compiler and promotes any reusable lemma the
library lacked back into Causalean. Presentation writes the paper from the finished graph, and the
run—accepted, downgraded, or failed—enters the record that screens the next proposal. Section 5
describes the stages in full.

                                                    2
                        novelty                        statement                       convergence
                      + soundness                        match          Prove            review
      Discover                       Formalize                                                           Present
                                                                     fill → review
    propose → solve                 plan → scaffold                                                  assemble & present
                                                                     type-checked
                                     reuse                                   study
                                                                             mode

    screen                                     Causalean verified library                                      record




                                        run record prior proposals & outcomes


Figure 1: The CausalSmith pipeline. A claim moves left to right through discovery, formalization,
proof, and presentation, clearing a review between stages: novelty and mathematical soundness,
statement matching, and a final dual-model convergence review of the frozen graph. Two feedback
channels grow the system (Section 5.4): study mode proves a load-bearing lemma Causalean lacks
and promotes it back into the library, and every run—accepted, downgraded, or failed—enters the
run record that screens the next proposal. Sections C to F give the operational detail.

                                                      theorem T



                                    gated A1           lemma L1             lemma L2



                                      setup             def D1              cited A2


Figure 2: A dependency graph (schematic). Nodes are statements; fill encodes review status
(matched, drift, unreviewed), and a dashed blue border marks a cited node. Solid edges show
what a claim says, dashed edges what its proof uses; the green underlay is the critical path of
must-prove nodes the review must clear.


Availability. The Causalean library, the research pipeline, and the run record backing Section 6
are available at https://github.com/Jiyuan-Tan/CausalSmith. A companion site at https:
//jiyuan-tan.github.io/CausalSmith/ provides a browsable view of the library, including the
natural-language statement of each declaration and the generated write-up of each accepted result.
Each write-up carries a proof map of its own results, a link from every statement to the Lean 4
declaration it was audited against, and a slide deck. Readers can verify, rate, and comment on
individual statements. Section G shows these.


2      Related Work
We discuss four lines of work: language models paired with proof assistants, and whether the
statements they produce mean what was intended; agentic systems for automated research, and the
verifiers their output is judged by; language models applied to causal inference; and formal libraries
for statistics and economics. Table 1 summarizes where CausalSmith sits among the systems
closest to it.

                                                           3
Table 1: Where CausalSmith sits among neighboring systems. “Statement audit?” asks whether
a system checks that the formal statement means the intended claim, beyond type-checking.
    System                              Proposes Machine-checked   Statement     Evaluator         Self-
                                        theorem?     proof?          audit?      soundness      improving?
    AI Scientist [55]                      ✓              —          —           LLM judge          —
    FunSearch / AlphaEvolve [38, 42]     partial          ✓          —           task metric        ✓
    AlphaProof [18]                        —              ✓          n/a            sound         partial
    Causal benchmarks [22, 23]             —              —          —           fixed labels       —
    Causal agents [52]                     —              —          —               none           —
    Lean economics library [15]            —              ✓          —              sound           —
    Asymptotic-statistics agents [53]      —              ✓           ✓        sound + audit        —
    CausalSmith (ours)                     ✓              ✓           ✓        sound + audit        ✓



Autoformalization, theorem proving, and statement matching. Language models have
been paired with proof assistants for neural proof search [27, 40], autoformalization [20, 54],
whole-proof generation and repair [13], retrieval-augmented proving [41, 56], and competition
mathematics [18, 49], and they are measured against benchmarks of known problems [4, 50, 62].
Closest to us is autoformalization, where a model turns an informal statement into a formal one. The
result is compared against a human-written formal version: by expert inspection [54], by roundtrip
and back-translation checks [2, 30, 36], or by learned alignment scorers [33]. Surface-overlap metrics
have been rejected as evidence of a match [39]. Our setting has no such reference. The theorem is new,
so the run writes its own informal claim and then formalizes it, leaving both sides of the comparison
model output. Studies of this gap report formalizations with no remaining proof gaps that still fail
expert review [19], statements a proof assistant accepts that are semantically wrong [11, 35], and
vacuity and reward hacking common enough to benchmark [51]. Our audit therefore back-translates,
inside the discovery loop and localized over a proof-dependency graph, in the style of Lean blueprints
and proof-flow tools [6, 63], within the broader shift toward proof-assistant-grounded reasoning [57].

Automated research agents and verified discovery. Agents that carry out end-to-end
research [55] are vulnerable when an LLM judges their output, whether shown by independent
re-evaluation [5] or by adversarial construction [21]. Other work grounds discovery in a hard verifier:
program search against a fitness function [38, 42], or a proof against a type checker. Those fitness
functions are fixed in advance, so a statement audit is a step they never need. “Co-scientist” agents
fall in between: they propose and refine scientific claims but validate them empirically [16]. The
system closest to ours is a multi-agent pipeline for asymptotic statistics, whose auditor and reviewer
agents already guard against vacuity [53]. It formalizes known theory, whereas CausalSmith
proposes the theorem as well, and CausalSmith localizes the audit over the dependency graph, so
a changed statement re-opens the affected nodes rather than the whole formalization.

LLMs for causal inference. A parallel literature asks whether language models reason causally,
treating causal reasoning as something to test or deploy rather than something to prove; recent
surveys organize it by causal task and intervention level [34]. Benchmarks probe graphical and
correlational reasoning [22, 23], broad and data-grounded question answering [7, 32], and, closest
to our own domain, end-to-end causal inference on real scientific studies [1, 43]. A critical strand
reports that surface accuracy conceals shallow reasoning: models explain causal language while
hallucinating the argument [14], recite memorized facts rather than reason interventionally [59],
commit elementary fallacies [24], and are flattered by benchmarks solvable through lookup [58]. A


                                                      4
third strand builds agents that do causal analysis without a correctness guarantee [9, 26, 44, 52],
including pipelines that map a dataset and question to an estimate [3] and systems that search
for instrumental variables [17, 45]. These share our propose-and-critique structure but validate
statistically or empirically; none produces a machine-checked causal theorem. Pairing language
models with formal verification appears confined to provers for general mathematics [46], and
CausalSmith works at that intersection.

Formal libraries for statistics and economics. A Lean 4 ecosystem for theoretical statistics
has recently emerged: Statlib on the decision-theoretic foundations of inference [31], StatsMLlib
on concentration, empirical processes, and finite-sample learning guarantees [28], and a statistical-
learning-theory line [61] extending the Rademacher-complexity library that Causalean adapts [47].
A Lean 4 library for economics formalizes established theory in the same spirit [15]. Causalean
overlaps with all of them wherever causal estimation theory needs the same tools—minimax lower-
bound methods, information divergences, empirical-process and concentration lemmas—and we
expect these projects to benefit as they converge on shared upstream infrastructure. Those libraries
formalize classical theory as the end product, whereas Causalean’s statistical clusters exist to
support theorems about causal estimands, and its core—structural causal models, do-calculus,
graphical and partial identification, panel estimand characterizations, and design-based inference
under interference—has no counterpart in any of them. Causalean is also built to be extended
rather than finished: each accepted run can promote its reusable lemmas back into the library for
later runs to use.


3    Background
Causal inference. Causal inference concerns the consequences of intervention rather than ob-
servation alone. Two frameworks are widely used: structural causal models (SCMs) and potential
outcomes (PO). An SCM models causal relationships with a directed acyclic graph and represents
interventions with the do-operator; its classical results include the graphical identification criteria
of do-calculus and the ID algorithm. Potential outcomes instead attach to each unit a family
of counterfactual responses, one per treatment level, and write causal estimands—the average
treatment effect, the effect on the treated, difference-in-differences, the local average treatment
effect—as functionals of their joint distribution. An estimand is identified when it is a function of
the observational distribution alone and partially identified when the data determine only a set
containing it, as with Manski or Balke–Pearl bounds. Causalean (Section 4) formalizes most
classical results under these frameworks.

Lean 4 as a proof checker. Lean 4 is a proof assistant and programming language in which
mathematics is written out in complete formal detail [12]. A proposition is a type and a proof of it
is a value of that type, so checking a proof means checking that a value has the type it claims; this
check is called type-checking. The unit being checked is a declaration, a single named definition
or theorem, and we say a declaration type-checks when it passes. Mathlib, Lean 4’s community
mathematics library, supplies the analysis, probability, and measure theory that our library builds
on [48].
    This makes Lean 4 useful as an evaluator. The check is mechanical and indifferent to how the
proof is written. When a proof of a statement τ passes, τ follows from its stated assumptions
together with the axioms the proof invokes, and Lean 4 reports those axioms on request. We call



                                                  5
this property proof soundness, but it says nothing about whether τ is the proposition the researcher
intended to prove, which Section 5.3 takes up.
     Three things pass the type check while leaving the mathematics incomplete, and all three appear
later in the paper. Writing sorry in place of a proof tells Lean 4 to grant the statement, the formal
counterpart of a TODO. Declaring an axiom asserts a statement without proof. And a statement can
be trivial: a definition that unfolds to True is satisfied by everything, so a theorem about it holds
vacuously. Lean 4 reports the first two on request—sorry raises a warning, and #print axioms
lists what a theorem ultimately rests on—while the third is invisible to Lean 4 and has to be caught
by reading the statement.


4     The Causalean Library
The cost of formalizing results from first principles limits automated discovery. Causalean is a
Lean 4 library for causal inference whose verified results agents can reuse and compose across runs.

4.1    Design and scope
Causalean holds mathematics that belongs to no single paper: the definitions and theorems any
causal result might reuse. One-off lemmas of a particular paper live instead in the pipeline package.
A CausalSmith run reads from the library freely and writes back to it only by promoting a reusable
lemma, which the pipeline does on its own once the lemma clears the checks of Section 5.4, and an
automated check enforces that boundary on every build.
    The library was built with LLM assistance, following the division of labor of Section 1. Humans set
the scope, design the structure of the library, choose which results to formalize, and fix the definitions
that later theorems are stated against; agents draft the statements, proofs, and docstrings. Nothing
enters the library until it passes the Lean 4 type check and clears the axiom check (Section 4.5). A
human then reviews that the formal statement matches the intended claim and that it is stated in a
standard form.
    The compiled environment index records 8,179 declarations: 5,375 theorems, 2,372 definitions,
and 432 structures, instances, and inductive types, across 1,070 files and roughly 302,000 lines
(Table 2).1 The declarations are grouped into ten clusters, from graphical foundations to asymptotic
statistics.

4.2    A tour of the clusters
The library layers from graphical and measure-theoretic foundations up to the estimation and design
methods that depend on them (Figure 3).

Graphs and structural models. The Graph cluster builds directed acyclic graphs with a
decidable edge relation and a stored topological order, on top of which sit the parent, child, and
ancestor operations, d-separation implemented as Bayes-Ball reachability, single-world intervention
graphs, and the c-component decomposition that the identification algorithm needs. The SCM
cluster turns these graphs into structural causal models. It defines interventions and the do-operator,
proves the semi-graphoid axioms that justify do-calculus, represents factored kernels, and develops
graphical identification proper: backdoor and frontdoor adjustment, general adjustment criteria,
   1
     These repository statistics are a snapshot. The totals may increase because the CausalSmith pipeline runs
continuously and can promote newly proved, reusable declarations to Causalean.



                                                      6
Table 2: Causalean coverage by cluster. All figures are read from the compiled environment
index (lake exe library index); the per-cluster kind columns sum to the grand total. “s/c/i”
abbreviates the remaining declaration kinds—structures and classes, inductives, and instances.
                   Cluster                 Files       Lines     Defs   Thms/Lem.     s/c/i
                   Stat                     254       67,065     358         1,229      42
                   Estimation               168       55,788     300           581     100
                   PO                       138       42,587     594           929      79
                   Mathlib (local)          157       39,550     306           894      36
                   SCM                       88       36,901     209           548      66
                   Panel                     68       19,176     260           423      45
                   Experimentation          103       17,212     175           363      12
                   Graph                     21       10,948      70           203      28
                   ML                        49        6,457      56            95      13
                   Discovery                 24        6,441      44           110      11
                   Total                 1,070     302,125          8,179 declarations

                                       Methods
                             estimation (DML, minimax) ·
                           panel · experimentation · discovery


                                    Identification
                             exact (ATE/DiD/LATE) · par-                     Retrieval
                               tial (Manski, Balke–Pearl)
                                                                             8,179 decls
                                                                           concept · type
                                        Models
                                                                           goal · semantic
                              SCM & do-calculus · potential
                             outcomes · asymptotic statistics


                                     Foundations
                       Graph (DAG, d-sep, SWIG) · local Mathlib


Figure 3: Causalean in layers: graphical and measure-theoretic foundations support the model
languages, which support identification, which supports the estimation and design methods on top.
A retrieval index over all 8,179 declarations spans the stack and is the interface the pipeline queries.


and a soundness proof for the ID algorithm. These results take a causal query to a formula in the
observational distribution, or to a nonidentification proof.

Potential outcomes and identification. The PO cluster holds the most definitions, because
it carries the two identification branches the pipeline uses most. Exact identification covers the
standard estimands—ATE, ATT, difference-in-differences and its Callaway–Sant’Anna group-time
refinement, LATE, regression discontinuity, proximal and dynamic-treatment designs—each stated
as an equality between a counterfactual contrast and an estimable functional. Partial identification
provides tight bounds for estimands that cannot be point-identified: Manski’s worst-case bounds
with their monotone-treatment-response and instrument refinements, the sharp Balke–Pearl bounds
for a binary instrument, Lee’s trimming bounds under selection, and marginal-sensitivity models.




                                                        7
Estimation and asymptotic statistics. Estimation, the largest cluster by volume, is the
semiparametric machinery: double/debiased machine learning for the ATE, ATT, and CATE;
efficient influence functions obtained by projection onto a tangent space; structure-agnostic minimax
lower bounds with matching estimators; and convergence rates for nonparametric instrumental
variables. These results draw on the Stat cluster, which formalizes the probability and empirical-
process theory underneath: central limit theorems, U-statistics with their Hájek projections,
Glivenko–Cantelli and bracketing-entropy tools, M- and Z-estimation, concentration inequalities
with localization, and the bootstrap. The localized theory covers star hulls, sub-root envelopes, local
Rademacher complexity, and the critical radius that controls a localized uniform-deviation bound.

Panel, experiments, and discovery. Panel builds general machinery for panel data: potential
outcomes indexed by treatment path, fixed effects, and least squares as projection with a Frisch–
Waugh–Lovell decomposition. Using that machinery, it characterizes the estimands that two-
way fixed-effects and difference-in-differences regressions actually recover, including the negative-
weights decomposition and event-study contamination that motivate modern DiD estimators.
Experimentation covers randomization inference, Horvitz–Thompson estimation, Neyman allocation,
and central limit theorems under network interference. Discovery formalizes identifiability results
for causal structure learning, such as LiNGAM under non-Gaussianity and invariant prediction,
while ML and the local Mathlib supplements provide the learning-theory and measure-theoretic
lemmas the rest of the library draws on.

4.3   Flagship results
The library also formalizes classical results from the literature. Table 3 catalogs the main result
families across its major research areas. Each entry is a named declaration with a machine-checked
proof; Section A gives its source location.

Table 3: Flagship theorems across Causalean’s major research areas. Each entry is a named,
machine-checked declaration; long identifiers may wrap.

   Result                                                 Declaration
   Graphical and structural causal models
   Markov equivalence iff two DAGs have the same          markovEquiv iff sameSkeleton sameImmoralities
   skeleton and immoralities
   Rule 2 of do-calculus under its graphical condition    do rule2 kernel
   Backdoor adjustment identifies an interventional       backdoor identifiable ae
   distribution almost everywhere
   Frontdoor adjustment identifies an interventional      frontdoor identifiable ae
   distribution almost everywhere
   Soundness of the graphical ID algorithm on the         id sound discrete
   discrete positive class
   Causal discovery
   LiNGAM identifiability from nonzero source             lingam identifiability kurtosis
   kurtosis
   Soundness of invariant causal prediction               icp sound
   Completeness of invariant prediction for               icp complete linearGaussian
   linear-Gaussian models


                                                  8
Table 3 continued
Result                                                   Declaration
Identifiability in linear causal disentanglement         disentanglement identifiability

Potential outcomes, exact identification, and partial identification
Wald-ratio identification of the local average         late wald
treatment effect
Difference-in-differences identification of the ATT    att did
Callaway–Sant’Anna group-time ATT identification att csdid
Sharp regression-discontinuity identification          rdd identification
Fuzzy regression-discontinuity identification          frd identification
Wald identification for dynamic treatment timing       whenToTreat wald
Manski worst-case ATE bounds                           manski bounds ATE
Sharpness of the Balke–Pearl bounds for a binary       balkePearl sharp
instrument
Lee bounds for the ATT under selection                 lee bounds ATT AS
Pointwise Imbens–Manski coverage for partially         imbensManski pointwise coverage
identified parameters
Estimation and statistical theory
Asymptotic normality of the debiased-ML ATE              dml ATE tendstoNormal
estimator
Attainment of the Hahn efficiency bound by               dml ATE attains hahn bound
debiased-ML ATE
Asymptotic linearity of debiased-ML ATT                  dml ATT isAsymLinear
estimation
Asymptotic normality of partially linear DML             plr dml tendstoNormal
Asymptotic linearity of sequential doubly robust         seqDR dml isAsymLinear
DTR estimation
Structure-agnostic minimax lower bound for ATE           minimax lower bound var causal
estimation
Optimal weighting for generalized method of              gmm efficiency
moments
Central limit theorem for regular order-m                uStatisticOrder clt
U-statistics
Panel and event-study methods
Causal decomposition of staggered-adoption TWFE          twfe po decomposition
into weighted contrasts
Characterization of linear-unbiased BJS imputation       bjs linear unbiased iff imputation form
estimators
Event-study pretrends induced by post-treatment          apparent pretrends from post treatment of
                                                         cellGrid
effects
Experimentation under interference
Consistency of Horvitz–Thompson estimation under         htEst consistent eate
unknown interference
Central limit theorem for a two-stage interference       directEffect clt
direct effect


                                                9
    Table 3 continued
    Result                                                Declaration
    Stein-method CLT for estimators under network         localDependenceCLT of stein
    interference
    Wald coverage under network interference              wald coverage of stein



4.4    Retrieval
A library of this size is only usable if its declarations can be found. The library provides a keyword
record for every declaration: its name, kind, module, source text, docstring, cross-references, axiom
dependencies, and whether its proof uses sorry. This index serves readers and agents alike. The
human-readable API documentation is generated from it, and it is also what a search query is
ranked over.
    For agents we build a search engine on top of it, and we train a retrieval encoder on Causalean
itself to drive part of it. The training pairs come from the keyword index: a theorem’s docstring
against the declarations it is built on, and each declaration’s Lean 4 statement against its own
docstring. The split is by module, so the encoder is evaluated only on modules it never saw. All
8,179 declarations are then embedded into a vector index of 1,024 dimensions.
    Search runs in three modes. A concept mode expands a natural-language query with causal-
inference synonyms. A type-pattern mode matches a fragment of Lean 4 syntax against the symbols
in each declaration’s statement. A goal-directed mode ranks candidates against the goal a proof is
stuck on. Concept and goal queries are ranked twice, once by keyword score and once by embedding
similarity, and the two rankings are combined by reciprocal-rank fusion. A fine-tuned cross-encoder
then reorders the leading concept candidates. Type-pattern queries use the keyword index alone.

4.5    Axiom checks
The whole library is sorry-free, and none of the 8,179 declarations rests on a hand-written axiom.
The only non-standard axioms come from native decide, a tactic that settles a finite computation
by running the compiled code and trusting the result; these occur in finite-graph decidability
arguments and several minimax calculations, and we report them explicitly.
    Two parts of the library are not original to Causalean. Both are adapted copies of external
Lean 4 projects, bumped to Causalean’s Lean 4/Mathlib pin. The first is the Karush–Kuhn–
Tucker first-order necessary conditions under LICQ and affine constraint qualifications, taken from
OptSuite’s optlib [29] and consumed by the Estimation cluster’s minimax lower bounds. The
second collects Rademacher complexity, McDiarmid’s inequality, symmetrization, and the Dudley
entropy integral, taken from lean-rademacher [47] and consumed across Stat, Estimation, and
ML.


5     The CausalSmith Pipeline
CausalSmith is a research pipeline with four stages: Discovery, Formalization, Proof Construction,
and Presentation. The pipeline either accepts a researcher-supplied topic or selects one itself, then
proposes a causal-inference result in natural language, formalizes it, and produces a paper linked
to the Lean 4 statements. New results are stored as dependency graphs throughout the pipeline.
Discovery creates this graph; formalization maps its nodes to planned Lean 4 declarations; proof
construction fills those declarations and updates their dependencies; statement matching checks


                                                 10
each formal node against the intended claim; and presentation writes the paper from the reviewed
graph.
    The pipeline runs the stages in a fixed order and retries a failed stage within fixed limits. An
orchestrator launches it and records its verdicts. Figure 1 summarizes the workflow; Sections C to F
give implementation details of the stages, the proof and audit loop, the presentation workflow, and
study mode.

5.1   The Dependency Graph as a Persistent Run Record
Lean blueprints and autoformalization pipelines already represent a development as a dependency
graph of statements, each node carrying a formalization status [6, 63]. We adopt that structure and
extend the node. Each result is stored as an acyclic directed graph whose nodes are statements—a
setup, a definition, an assumption, a lemma, or the headline theorem—and whose edges represent
dependencies. Alongside its Lean 4 declaration, a node carries the intended natural-language
statement and a review status recording whether the two have been compared and whether they
matched, together with a class that separates two kinds of dependency. A must-prove node is a
result the paper proves, and a cited node is a result taken from the literature, carried with its source
and lying outside the paper’s novelty. The graph is therefore both a plan and an audit record. A
typical completed result has on the order of a hundred nodes and a few hundred edges (Figure 2);
Section B gives the full schema.
    Within Discovery, the agents write the new results as natural-language nodes with their depen-
dency edges. Formalization then attaches the intended Lean 4 declarations to each node. Proof
construction adds the proof dependencies and fills in the Lean 4 proof. Statement matching compares
the natural-language statement with the Lean 4 declaration for each node and updates the review
status. Presentation then uses the reviewed graph to link each part of the paper to its code. When a
statement changes, the pipeline marks the downstream nodes unreviewed again and rechecks them.

5.2   Discovery, formalization, and proof
The pipeline supports two entry modes. A researcher may supply a topic anchor, or the main
orchestrator may invoke the topic-selection skill as the first part of Discovery. The selector searches
recent work and previous runs, and reads theoretical papers together with their citing and follow-up
literature in full, to find inspiration and propose a few candidate topics. It then ranks them by
mathematical potential and by whether the result would have a concrete application, and submits
the top candidate to an independent adversarial topic review. The pipeline is started only when the
review passes.
    Once a topic is fixed, the remaining discovery stages derive the result in natural language and
build the graph. A proposer drafts a question and an informal solution; a novelty-and-duplication
review compares it with the literature and judges whether it is novel. Then a solver solves the
proposed open questions in natural language. Their outputs become the initial graph nodes and
edges. When a proposed claim is too strong or too weak, the solver may adjust it to obtain a
meaningful result. A mathematically sound but insufficiently novel proposal is downgraded, whereas
an incorrect or trivial proposal is rejected.
    Formalization turns this graph into a proof plan. Each node receives an intended Lean 4
declaration, a module location, and either a statement to prove or an existing Causalean result
to reuse. The plan becomes a skeleton file in which each statement to prove is left sorry. A
review-and-fill loop then closes those open statements. On each iteration, the reviewer first checks
that every declaration remains aligned with the graph and repairs declarations whose statements


                                                  11
      Table 4: Failures that can pass the Lean 4 type check while changing the intended claim.
 Family              Failure mode                                         How the review catches it
 Wrong      state-   Type-checks but states the wrong proposition.        Per-node comparison with the in-
 ment                                                                     tended claim.
 Vacuity             Concept defined as True and a witness that carries   A witness must carry a real ob-
                     no real obstruction.                                 struction and cannot be True or
                                                                          an empty structure; satisfiability
                                                                          is screened earlier, by the mathe-
                                                                          matical review of the proposal.
 Unproved step       Step asserted as axiom; sorry/admit; a node the      Automatic scan for these key-
                     proof depends on mis-tagged as cited.                words; source check for cited
                                                                          nodes.
 Over-narrow         Dropped hypothesis; hardcoded constant where         Comparison with the intended
 statement           general was intended.                                claim; check for unused hypothe-
                                                                          ses.


are not faithful; it then fills each remaining sorry, using the search engine of Section 4.4 to reuse
existing results. An automatic check flags hypotheses the proof never uses, which may indicate a
vacuous or mis-stated theorem.

5.3    Statement matching
The statement-match review in Figure 1 is where the pipeline guarantees faithfulness. As Section 3
notes, the Lean 4 type check says nothing about whether the formal statement is the one the
researcher meant to prove. A formalization can carry no proof gaps and still fail expert review,
because a definition is too narrow, a hypothesis is vacuous, or an unproven step has been promoted
to an axiom. This review checks each formal statement against the intended claim stored in its
graph node. The main criterion is logical equivalence: the two must have equivalent assumptions
and equivalent conclusions, with neither stronger nor weaker than the other. Table 4 groups the
failure modes into four families and records where the pipeline catches each one.
    The review runs in two layers. The first is mechanical. A scan rejects any completed artifact
that contains axiom, sorry, admit, opaque, or unsafe, and it applies the same test to every library
module the artifact depends on, directly or indirectly. The build itself rejects any artifact with an
unfinished proof. In the second layer, several agents read the Lean 4 declaration text extracted from
the compiled file, compare it against the intended statement, and flag any divergence as drift; the
review requires every claimed witness to carry a concrete obstruction and every cited node to have
a real source match.
    Once every statement has a proof, two independent models recheck the full frozen graph,
including nodes the latest changes did not touch, comparing every statement against the intended
claim without reference to the earlier review. This is the final review in Figure 1 before the result
enters the presentation stage.

5.4    Library feedback
Two feedback channels connect one run to future runs: a run record of what has been attempted,
and a verified library of what has been proved.
   The run record preserves every run regardless of its outcome, from accepted to rejected, together
with its proposal, mathematical core, and review verdicts (Table 5 and section H). Before a


                                                     12
new proposal is drafted, Discovery searches these records for open gaps and near-duplicates, and
the novelty-and-duplication review compares a fresh proposal against prior entries. Failed and
downgraded runs contribute alongside accepted ones: a documented rejection prevents a later run
from repeating the same dead end, and a downgraded result sharpens the novelty target for a related
question.
    The library channel handles reusable lemmas or theorems during the run. When the graph
identifies a missing reusable lemma, the pipeline can prove that lemma and promote it to Causalean.
A library builder (called study mode in our pipeline) first plans the lemmas and writes a file with
the statements left open. A prover then fills in the proofs against the live compiler, and a reviewer
assesses whether the resulting lemma is generic, reusable, non-vacuous, and sorry-free. A build
check confirms this assessment. Section F describes study mode in full.

5.5   Presentation
The presentation stage converts an accepted result into a working paper in which each theorem,
definition, and assumption links to its verified Lean 4 source. Linking prose to code is established
practice [63]. The link records both facts attached to a graph node: the Lean 4 declaration compiles,
and the statement has been checked as matching the English claim. An equivalence check applies
the criterion of Section 5.3: the paper statement and the Lean 4 declaration must express the same
proposition, with neither stronger nor weaker than the other.
    An LLM reviewer at the end of this stage reads the assembled paper the way a journal referee
would, treating the verified theorems as given, and judges the significance of the contribution,
whether each prose claim matches the verified statement in strength and scope, and the exposition,
clarity, and positioning against related work. It returns a recommendation with a score, and findings
on what could be improved. The score is advisory and is recorded in the run record.
    The same stage publishes the result to the companion site. There the paper carries a proof map
in the margin, showing which of the paper’s own results each proof invokes. Every statement links
to the Lean 4 declaration it was audited against, hypothesis by hypothesis. A reader signed in with
a GitHub account can verify a single statement, rate the paper or one of its results, and comment
on any passage. The stage also builds a short slide deck from the same graph. Section G shows
each of these.


6     Results
We analyze the pipeline’s run records and logs in this section. We give the distribution of outcomes
across runs, report which kinds of self-proposed question the system converts into accepted results,
examine one accepted result in depth, report the axiom audit that screens each accepted result, and
trace the library feedback loop closing on a concrete lemma.
    All results reported here come from one base-model lineup, whose members were updated during
the campaign. OpenAI reasoning models carry the main mathematics and the Lean 4 formalization:
GPT-5.5 until 2026-07-10 and GPT-5.6 Sol thereafter. Anthropic’s Claude handles Lean 4 code
review and planning throughout, as Opus 4.7 until 2026-05-28, Opus 4.8 until 2026-07-24, and
Opus 5 after. Nine of the fourteen accepted runs ran entirely under Opus 4.8 and the other five
entirely under Opus 5. Mechanical stages run on GPT-5.6 Terra, and the presentation write-ups are
drafted by GPT-5.5. Section H maps every role to its model and records what the run logs attest.
    The run record holds 144 runs, distributed across three outcomes (Table 5). A run is accepted
only when it is sound, novel at its requested publishable tier, and proved to completion in Lean 4;


                                                 13
Table 5: The run catalog: 144 recorded CausalSmith runs by outcome. A separate literature-
reproduction track adds one reproduced partial-identification result. Counts are entries in the run
record; a re-run that supersedes an earlier attempt at the same question counts separately, and nine
legacy runs from the retired proposal track that predates the current pipeline are excluded.
                  Outcome        Runs   Review that determined it
                  Accepted         14   sound, novel at tier, proved in Lean 4
                  Downgraded       59   sound, below the novelty target
                  Failed           71   rejected at the proposal or the mathematics
                  Total           144


fourteen runs meet this bar. The remaining runs are retained: as Section 5.4 describes, downgraded
and failed runs feed the record that screens later proposals.

6.1   Outcomes by cluster and question type
Discovery files every run under one of six clusters before any mathematics begins. Sorted that
way (Table 6), the accepted results gather in Stat, Experimentation, and Panel. By contrast, the
three identification and structural-model clusters together hold 94 runs and only one acceptance.

Table 6: The run catalog by the cluster Discovery assigned at proposal time. “Accept rate” is
accepted runs over total runs in the cluster.
                    Cluster             Acc.   Down.   Fail.   Total   Accept rate
                    Stat                   8      18      5      31           26%
                    Experimentation        4       7      1      12           33%
                    Panel                  1       0      6       7           14%
                    ExactID                1       8     27      36            3%
                    PartialID              0      24     30      54            0%
                    SCM                    0       2      2       4            0%
                    Total                 14      59     71     144           10%

   We also labeled each run by what its proposal is about, using the following rules. The catalog is
shown in Table 7.
 • Method comparison. The topic compares two or more published estimators or identification
   frameworks and asks how they differ: non-equivalence, strict-extension, or equivalence.
 • Assumption relaxation. The topic weakens a named assumption, under a budget on how far
   it may be violated, and asks for the identification result—an identified set, a threshold, a phase
   transition—as a function of that budget. Sensitivity and ambiguity models are the common
   instances.
 • Gap filling. The setting already exists in the literature, but some gaps are left open: a matching
   bound; an exact rate, order, or constant; a minimax optimum or optimal design; or an explicit
   identifying formula.
 • New setting. Anything else: a newly posed object, criterion, algorithm, or framework, with no
   published counterpart to be matched against.


                                                 14
Table 7: The run catalog by question type. Types are assigned by the rule in the text, applied to
the proposal-time topic string each recorded run carries. We assigned the labels once the runs had
finished (Section H).
                  Question type           Acc.   Down.     Fail.   Total   Accept rate
                  Gap filling               14        22      8      44           32%
                  Assumption relaxation      0        29     22      51            0%
                  New setting                0         6     28      34            0%
                  Method comparison          0         2     13      15            0%
                  Total                     14        59     71     144           10%


    All fourteen acceptances are gap filling. The remaining three types each fail in a characteristic
way. Assumption-relaxation runs usually reach a correct derivation and then lose on novelty, giving
29 downgrades against 22 failures; reviewers describe what comes back as “generic Manski-style
outer containment” or “while correct, a standard finite-dimensional support/projection calculation,”
so the difficulty lies in conception rather than in the proof. Method-comparison and new-setting
runs stop earlier, 13 of 15 and 28 of 34 failing outright, often at the proposal stage. Gap-filling
proposals often have a more quantitative target, such as a better convergence rate or a matched
lower bound, while the other three types do not.

Where the gaps come from. Some gaps are explicitly stated in the literature, and some the
system finds for itself. We read the anchor paper behind each of the fourteen accepted results.
Three inherit a gap the anchor states in its own text: Zeng et al. [60] leave both the closure of
their log2 gap and the sharp minimax dependence on their homogeneity radius to future work,
and Cortez-Rodriguez et al. [10] trace the degree gap between their bounds to “a weakness in
the analyses.” The other eleven aim at a quantity the literature had yet to ask about, such as
the pseudo-true estimand of staggered PPML [37], a differentially private counterpart of a known
conditional average treatment effect rate [25], or the minimax confidence-set length for a transported
complier average causal effect [8].

6.2   A flagship result: closing a minimax gap for the ATE
The strongest accepted result closes a standing gap in the minimax theory of average-treatment-
effect (ATE) estimation under high-dimensional discrete confounding. Zeng et al. [60] established a
                                                 2
minimax lower bound of order n−1 + d/(n log n) for estimating the ATE from n i.i.d. observations
(X, A, Y ) with a discrete confounder X ∈ {1, . . . , d}, binary treatment A and outcome Y , and
strict-interior overlap ϵ ≤ Pr(A = 1 | X = k) ≤ 1 − ϵ. The estimators they analyze, however, leave a
log2 -factor gap between the known upper and lower bounds. The run constructs an estimator that
closes it.
    Under the stated overlap, consistency,
                                       P and conditional-exchangeability assumptions, the target
is the adjustment functional τ (P ) = dk=1 pk (µ1k − µ0k ) = E[Y (1) − Y (0)], where pk = Pr(X = k)
and µak = E[Y | A = a, X = k]. The estimator splits the sample in two and uses a pilot count
to label each covariate cell heavy or light. The two regimes are then handled differently. Heavy,
well-populated cells receive a plug-in ratio estimator, and light, sparsely sampled cells receive a
best-polynomial approximation of the cell functional with unbiased factorial-moment lifting. The




                                                 15
headline theorem states that, for every fixed overlap 0 < ϵ < 1/2, this estimator attains
                                 1  d 2
                     Rn,d,ϵ ≍ϵ     +                   uniformly for d ≲ϵ n log n,
                                 n   n log n
                                                                     √
so the minimax MSE has parametric order n−1 whenever d = O( n log n) and tends to zero if and
only if d = o(n log n).
    The novel part is the hybrid estimator and its matched rate. The minimax lower half is not
checked here; it is cited from the published moment-matching bound of Zeng et al. [60]. In the
Lean 4 code, this imported bound appears as an explicit hypothesis on the headline theorem, which
follows the cited-result discipline of Table 4: an external result the proof depends on is carried as a
hypothesis with source evidence, so a reader sees which part is proved in this work and which is
from the literature.

6.3   Machine-checked soundness
Each accepted result is screened for the unproved-step failures of Table 4 before it is recorded.
Starting from a clean build, we ask Lean 4 which axioms the headline theorem depends on, and we
cross-check the answer by scanning the recorded module and every library module it reaches for
sorry, admit, and axiom (Section H). For the all accepted papers, the formalization contain none
of these, and the theorems reduces to Lean 4’s standard axioms; its single external input, the Zeng
et al. [60] lower bound, is visible as a hypothesis.

6.4   Library feedback in action
The flagship result of Section 6.2 gives a complete instance of the library feedback loop. Its estimator
labels each covariate cell heavy or light by a pilot count, so the proof needs two-sided multiplicative
Chernoff tails for the count of an i.i.d. [0, 1]-valued statistic, which Mathlib does not have. The
run proved them, and promotion moved them into Causalean as Causalean.Stat.Concentration.
TailBounds.BinomialCount, whose bernoulliCount upper tail and bernoulliCount lower tail
the run then applies.
    The next accepted result on the same estimand consumed that promotion. The two-sided
minimax bracket for the discrete ATE under a shrinking heterogeneity radius needs the pilot
argument at greater generality, over an arbitrary finite category set where the flagship had two cell
types. The run then built Causalean.Stat.SampleSplit.FiniteCategoryPilot, which imports
BinomialCount and reuses its moment-generating-function bound. So a run required a lemma, the
system proved it, promotion added it to the library, and a later run on the same problem built
on it instead of repeating it. Twenty-eight further library builds have produced promotions of
their own, including Fano’s inequality, a Bretagnolle–Huber affinity bound for arbitrarily many
hypotheses that a dose-response converse needed and a later Le Cam two-point reduction reuses,
a KL density-tilt expansion, and the Ehlich–Zeller and Bernstein–Szegő tools behind an accepted
Chebyshev rollout design. Estimating how library growth trades off against cost per result remains
future work (Section 7).


7     Discussion and Limitations
Automated theoretical research needs a reliable basis for judging correctness, and LLM reviewers
can be misled. CausalSmith answers that at three separate levels of confidence. The Lean 4 type
check settles whether a proof is valid, and the statement audit guarantees that the Lean 4 statement

                                                  16
matches the intended claim. Whether a finished paper matters stays a human judgment. Keeping
the three apart is what stops a valid proof from being read as an important result.
    Most of the pipeline is domain-general, and only the formal library is specific to causal inference.
Moving to another field means building or adopting a comparable library and retrieval interface.
The graph, the audit, and the library feedback loop should carry over with little change.
    Our current evaluation has the following limitations. First, research quality is rated by the
pipeline itself, and these LLM ratings do not have independent human validation. Second, the
statement-match audit is itself an LLM task; frontier models handled it well in our observations,
but we do not estimate how often they err.
    Taken together, the verified library, the self-directed pipeline, and the feedback loop that grows
the library give machine-checked proofs of self-proposed results with audited statements. We leave
better novelty-evaluation metrics and faithfulness-audit benchmarks to future work.


References
 [1] Sawal Acharya, Terry Jingchen Zhang, others, and Zhijing Jin. CauSciBench: Can LLMs
     automate causal inference in real-world scientific research? arXiv preprint / OpenReview, 2025.
     End-to-end causal-inference benchmark over real-world scientific research; causalNLP group.

 [2] Daneshvar Amrollahi, Jerry Lopez, and Clark Barrett. Faithful autoformalization via roundtrip
     verification and repair. arXiv preprint arXiv:2604.25031, 2026.

 [3] Anonymous. Causal AI scientist: Towards end-to-end causal inference with large language
     models. OpenReview submission (under review), 2026.

 [4] Zhangir Azerbayev, Bartosz Piotrowski, Hailey Schoelkopf, Edward W. Ayers, Dragomir Radev,
     and Jeremy Avigad. ProofNet: Autoformalizing and formally proving undergraduate-level
     mathematics. arXiv preprint arXiv:2302.12433, 2023.

 [5] Joeran Beel, Min-Yen Kan, and Moritz Baumgart. Evaluating Sakana’s AI scientist: Bold
     claims, mixed results, and a promising future? arXiv preprint arXiv:2502.14297, 2025.

 [6] Rafael Cabral, Tuan Manh Do, Xuejun Yu, Wai Ming Tai, Zijin Feng, and Xin Shen. Proof-
     Flow: A dependency graph approach to faithful proof autoformalization. arXiv preprint
     arXiv:2510.15981, 2025.

 [7] Sirui Chen, Bo Peng, Meiqi Chen, Ruiqi Wang, Mengying Xu, Xingyu Zeng, Rui Zhao, Shengjie
     Zhao, Yu Qiao, and Chaochao Lu. Causal evaluation of language models. arXiv preprint
     arXiv:2405.00622, 2024.

 [8] Zhongren Chen and Melody Huang. Generalizing causal effects with noncompliance: Application
     to deep canvassing experiments. arXiv preprint arXiv:2506.00149, 2025.

 [9] Joanie Hayoun Chung, Sumin Lee, and Sungbin Lim. ORCA: ORchestrating causal agent.
     arXiv preprint arXiv:2508.21304, 2025. CHI EA 2026.

[10] Mayleen Cortez-Rodriguez, Matthew Eichhorn, and Christina Lee Yu. Exploiting neighborhood
     interference with low order interactions under unit randomized design. Journal of Causal
     Inference, 11(1):20220051, 2023. arXiv:2208.05553.



                                                  17
[11] Chengxiao Dai, Zhaokun Yan, and Zhanhui Lin. The signal-coverage matrix: Stratifying type
     and semantic errors in statement autoformalization. arXiv preprint arXiv:2606.28013, 2026.

[12] Leonardo de Moura and Sebastian Ullrich. The Lean 4 theorem prover and programming
     language. In Automated Deduction (CADE 28), pages 625–635. Springer, 2021.

[13] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. Baldur: Whole-proof generation
     and repair with large language models. arXiv preprint arXiv:2303.04910, 2023.

[14] Jinglong Gao, Xiao Ding, Bing Qin, and Ting Liu. Is ChatGPT a good causal reasoner? a
     comprehensive evaluation. Findings of the Association for Computational Linguistics: EMNLP,
     2023. arXiv:2305.07375.

[15] Nikhil Garg. EconCSLib: AI-assisted lean formalization for economics and computation
     research. arXiv preprint arXiv:2606.13306, 2026.

[16] Juraj Gottweis, Wei-Hung Weng, Alexander Daryin, Tao Tu, Anil Palepu, Vivek Natarajan,
     et al. Towards an AI co-scientist. arXiv preprint arXiv:2502.18864, 2025.

[17] Sukjin Han. Mining causality: AI-assisted search for instrumental variables. arXiv preprint
     arXiv:2409.14202, 2024.

[18] Thomas Hubert, Rishi Mehta, Laurent Sartran, et al. Olympiad-level formal mathematical
     reasoning with reinforcement learning. Nature, 2025. DOI: 10.1038/s41586-025-09833-y.

[19] Vasily Ilin and Brian Nugent. Sorries are not the hard part: An expert-review case study of a
     semi-autonomous formalization. arXiv preprint arXiv:2606.13925, 2026.

[20] Albert Q. Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik,
     Timothée Lacroix, Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding formal
     theorem provers with informal proofs. In International Conference on Learning Representations
     (ICLR), 2023.

[21] Fengqing Jiang, Yichen Feng, Yuetai Li, Luyao Niu, Basel Alomair, and Radha Poovendran.
     BadScientist: Can a research agent write convincing but unsound papers that fool LLM
     reviewers? arXiv preprint arXiv:2510.18003, 2025.

[22] Zhijing Jin, Yuen Chen, Felix Leeb, Luigi Gresele, Ojasv Kamal, Zhiheng Lyu, Kevin Blin,
     Fernando Gonzalez Adauto, Max Kleiman-Weiner, Mrinmaya Sachan, and Bernhard Schölkopf.
     CLadder: Assessing causal reasoning in language models. In Advances in Neural Information
     Processing Systems (NeurIPS), 2023.

[23] Zhijing Jin, Jiarui Liu, Zhiheng Lyu, Spencer Poff, Mrinmaya Sachan, Rada Mihalcea, Mona
     Diab, and Bernhard Schölkopf. Can large language models infer causation from correlation? In
     International Conference on Learning Representations (ICLR), 2024.

[24] Nitish Joshi, Abulhair Saparov, Yixin Wang, and He He. LLMs are prone to fallacies in causal
     inference. arXiv preprint arXiv:2406.12158, 2024.

[25] Edward H. Kennedy, Sivaraman Balakrishnan, James M. Robins, and Larry Wasserman.
     Minimax rates for heterogeneous causal effect estimation. Annals of Statistics, 52(2), 2024.
     arXiv:2203.00837.


                                               18
[26] Emre Kıcıman, Robert Ness, Amit Sharma, and Chenhao Tan. Causal reasoning and large
     language models: Opening a new frontier for causality. Transactions on Machine Learning
     Research, 2023. arXiv:2305.00050.

[27] Guillaume Lample, Marie-Anne Lachaux, Thibaut Lavril, Xavier Martinet, Amaury Hayat,
     Gabriel Ebner, Aurelien Rodriguez, and Timothee Lacroix. HyperTree proof search for neural
     theorem proving. arXiv preprint arXiv:2205.11491, 2022.

[28] Lean-MoDS contributors. StatsMLlib: Verified probability, statistics, and learning theory in
     Lean 4, 2026. https://github.com/Lean-MoDS/StatsMLlib.

[29] Chenyi Li, Shengyang Xu, Chumin Sun, Li Zhou, and Zaiwen Wen. Formalization of optimality
     conditions for smooth constrained optimization problems. arXiv preprint arXiv:2503.18821,
     2025. https://github.com/optsuite/optlib.

[30] Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Xian Zhang, Fan Yang, and Xiaoxing Ma.
     Autoformalize mathematical statements by symbolic equivalence and semantic consistency. In
     Advances in Neural Information Processing Systems (NeurIPS), 2024. arXiv:2410.20936.

[31] Yongxi Lin, Debarghya Mukherjee, Rajarshi Mukherjee, Fred Rajasekaran, and Zixiao Jolene
     Wang. Statlib: A Lean 4 library for theoretical statistics, 2026. https://github.com/
     stat-lib/statlib.

[32] Xiao Liu, Zirui Wu, Xueqing Wu, Pan Lu, Kai-Wei Chang, and Yansong Feng. Are LLMs
     capable of data-based statistical and causal reasoning? benchmarking advanced quantitative
     reasoning with data. In Findings of the Association for Computational Linguistics: ACL, 2024.
     arXiv:2402.17644.

[33] Jianqiao Lu, Yingjia Wan, Yinya Huang, Jing Xiong, Zhengying Liu, and Zhijiang Guo. For-
     malAlign: Automated alignment evaluation for autoformalization. In International Conference
     on Learning Representations (ICLR), 2025. arXiv:2410.10135.

[34] Jing Ma. Causal inference with large language model: A survey. In Findings of the Association
     for Computational Linguistics: NAACL 2025, pages 5901–5913. Association for Computational
     Linguistics, 2025. doi: 10.18653/v1/2025.findings-naacl.327. URL https://aclanthology.
     org/2025.findings-naacl.327/.

[35] Theodore Meek, Siyuan Ge, Di Qiu Xiang, Simon Chess, and Vasily Ilin. Formalizing numerical
     analysis: An agent pipeline and quality audit beyond kernel acceptance. arXiv preprint
     arXiv:2606.14000, 2026. Verify author-name segmentation against the arXiv page.

[36] Noor Islam S. Mohammad and Tamim Sheikh. The faithfulness gap: Certifying semantic
     equivalence between natural-language and formal mathematical statements. arXiv preprint
     arXiv:2606.16541, 2026.

[37] Ninon Moreau-Kastler. Proportional treatment effects in staggered settings: An approach for
     poisson pseudo-maximum likelihood. Working Paper 31, EU Tax Observatory, 2025. SSRN
     5247936.

[38] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt
     Wagner, Sergey Shirobokov, Borislav Kozlovskii, Francisco J. R. Ruiz, Abbas Mehrabian,
     M. Pawan Kumar, Abigail See, Swarat Chaudhuri, George Holland, Alex Davies, Sebastian

                                               19
    Nowozin, Pushmeet Kohli, and Matej Balog. AlphaEvolve: A coding agent for scientific and
    algorithmic discovery. arXiv preprint arXiv:2506.13131, 2025.

[39] Auguste Poiroux, Gail Weiss, Viktor Kunčak, and Antoine Bosselut. Reliable evaluation and
     benchmarks for statement autoformalization. Findings of the Association for Computational
     Linguistics: EMNLP, 2025. arXiv:2406.07222.

[40] Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem
     proving. arXiv preprint arXiv:2009.03393, 2020.

[41] Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue
     Zhang, Zhe Fu, Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang,
     Yuxuan Liu, Wenjun Gao, Daya Guo, and Chong Ruan. DeepSeek-Prover-V2: Advancing
     formal mathematical reasoning via reinforcement learning for subgoal decomposition. arXiv
     preprint arXiv:2504.21801, 2025.

[42] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog,
     M. Pawan Kumar, Emilien Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming Wang,
     Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi. Mathematical discoveries from program
     search with large language models. Nature, 625:468–475, 2024.

[43] Ayush Sawarni, Jiyuan Tan, and Vasilis Syrgkanis. Causalreasoningbenchmark: A real-world
     benchmark for disentangled evaluation of causal identification and estimation, 2026.

[44] ChengAo Shen, Zhengzhang Chen, Dongsheng Luo, Dongkuan Xu, Haifeng Chen, and Jingchao
     Ni. Exploring multi-modal data with tool-augmented LLM agents for precise causal discovery.
     arXiv preprint arXiv:2412.13667, 2024.

[45] Ivaxi Sheth, Zhijing Jin, Bryan Wilder, Dominik Janzing, and Mario Fritz. IV co-scientist:
     Multi-agent LLM framework for causal instrumental variable discovery. arXiv preprint
     arXiv:2602.07943, 2026.

[46] Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Lean copilot: Large language models as
     copilots for theorem proving in lean. arXiv preprint arXiv:2404.12534, 2024.

[47] Sho Sonoda, Kazumi Kasaura, Yuma Mizuno, Kei Tsukamoto, and Naoto Onda. Lean formal-
     ization of generalization error bound by Rademacher complexity and Dudley’s entropy integral.
     arXiv preprint arXiv:2503.19605, 2025. https://github.com/auto-res/lean-rademacher.

[48] The mathlib Community. The Lean mathematical library. In Proceedings of the 9th ACM
     SIGPLAN International Conference on Certified Programs and Proofs (CPP), pages 367–381,
     2020.

[49] Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He, and Thang Luong. Solving olympiad geometry
     without human demonstrations. Nature, 625:476–482, 2024. doi: 10.1038/s41586-023-06747-5.

[50] George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings,
     Amitayush Thakur, and Swarat Chaudhuri. PutnamBench: Evaluating neural theorem-provers
     on the Putnam mathematical competition. Advances in Neural Information Processing Systems
     (NeurIPS), 2024. arXiv:2407.11214.




                                               20
[51] Zeynel A. Uluşan, Burak S. Akbudak, Can S. Erer, and Gözde Gül Şahin. FormalRewardBench:
     A benchmark for formal theorem proving reward models. arXiv preprint arXiv:2605.10141,
     2026.

[52] Xinyue Wang, Kun Zhou, Wenyi Wu, Har Simrat Singh, Fang Nan, Songyao Jin, Aryan Philip,
     Saloni Patnaik, Hou Zhu, Shivam Singh, Parjanya Prashant, Qian Shen, and Biwei Huang.
     Causal-Copilot: An autonomous causal analysis agent. arXiv preprint arXiv:2504.13263, 2025.

[53] Tingzhou Wei, Zeyu Zheng, Ethan X. Fang, and Junwei Lu. Hypothesis-disciplined multi-agent
     automated formalization of asymptotic statistical theory. arXiv preprint arXiv:2606.20642,
     2026.

[54] Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N. Rabe, Charles Staats, Mateja Jamnik,
     and Christian Szegedy. Autoformalization with large language models. In Advances in Neural
     Information Processing Systems (NeurIPS), 2022.

[55] Yutaro Yamada, Robert Tjarko Lange, Cong Lu, Shengran Hu, Chris Lu, Jakob Foerster, Jeff
     Clune, and David Ha. The AI scientist-v2: Workshop-level automated scientific discovery via
     agentic tree search. arXiv preprint arXiv:2504.08066, 2025.

[56] Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
     Godil, Ryan Prenger, and Anima Anandkumar. LeanDojo: Theorem proving with retrieval-
     augmented language models. In Advances in Neural Information Processing Systems (NeurIPS),
     Datasets and Benchmarks Track, 2023.

[57] Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li, Kristin Lauter, Swarat Chaudhuri,
     and Dawn Song. Formal mathematical reasoning: A new frontier in AI. arXiv preprint
     arXiv:2412.16075, 2024.

[58] Linying Yang, Vik Shirvaikar, Oscar Clivio, and Fabian Falck. A critical review of causal
     reasoning benchmarks for large language models. arXiv preprint arXiv:2407.08029, 2024.

[59] Matej Zečević, Moritz Willig, Devendra Singh Dhami, and Kristian Kersting. Causal parrots:
     Large language models may talk causality but are not causal. Transactions on Machine Learning
     Research, 2023. arXiv:2308.13067.

[60] Zhenghao Zeng, Sivaraman Balakrishnan, Yanjun Han, and Edward H. Kennedy. Causal
     inference with high-dimensional discrete covariates. arXiv preprint arXiv:2405.00118, 2024.

[61] Yuanhe Zhang, Jason D. Lee, and Fanghui Liu. AI4SLT: Empirical processes in Lean 4 for
     formal statistical learning theory. arXiv preprint arXiv:2602.02285, 2026.

[62] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. MiniF2F: A cross-system benchmark
     for formal olympiad-level mathematics. arXiv preprint arXiv:2109.00110, 2021.

[63] Thomas Zhu, Pietro Monticone, Jeremy Avigad, and Sean Welleck. LeanArchitect: Automating
     blueprint generation for humans and AI. arXiv preprint arXiv:2601.22554, 2026.




                                               21
A     Flagship theorem locations
Table 8 lists the Lean 4 declaration name and source location of every flagship result named in
Section 4.3, so that a reader can look each one up directly. Paths are relative to the Causalean/
package root, at the pinned toolchain leanprover/lean4:v4.29.0-rc3.

                    Table 8: Source locations of the flagship declarations in Table 3.

Declaration                                     File                                                   Line
markovEquiv iff sameSkeleton sameImmoralities   Graph/MarkovEquiv.lean                                   51
do rule2 kernel                                 SCM/Do/DoCalculus.lean                                   97
backdoor identifiable ae                        SCM/ID/Backdoor.lean                                    377
frontdoor identifiable ae                       SCM/ID/Frontdoor.lean                                  1190
id sound discrete                               SCM/ID/GraphicalThms/IDSoundDiscrete.lean                30
lingam identifiability kurtosis                 Discovery/LiNGAM/LiNGAMKurtosis.lean                     69
icp sound                                       Discovery/InvariantPrediction/Soundness.lean             34
icp complete linearGaussian                     Discovery/InvariantPrediction/.../Completeness.lean     270
disentanglement identifiability                 Discovery/LinearDisentanglement/Identifiability.lean     35
late wald                                       PO/ID/Exact/LATE.lean                                   413
att did                                         PO/ID/Exact/DID.lean                                    150
att csdid                                       PO/ID/Exact/CSDID.lean                                  423
rdd identification                              PO/ID/Exact/RDD/SharpRDD.lean                           295
frd identification                              PO/ID/Exact/RDD/FuzzyRDD.lean                           575
whenToTreat wald                                PO/ID/Exact/DynamicLATE/WhenToTreat.lean                332
manski bounds ATE                               PO/ID/Partial/Manski/NonAsp.lean                         72
balkePearl sharp                                PO/ID/Partial/BalkePearl/Sharp.lean                     852
lee bounds ATT AS                               PO/ID/Partial/Lee/Main.lean                              33
imbensManski pointwise coverage                 PO/ID/Partial/Inference/ImbensManski.lean               171
dml ATE tendstoNormal                           Estimation/ATE/DML.lean                                 899
dml ATE attains hahn bound                      Estimation/Efficiency/ATEVariance.lean                  415
dml ATT isAsymLinear                            Estimation/ATT/DML.lean                                 237
plr dml tendstoNormal                           Estimation/PLR/DML.lean                                 158
seqDR dml isAsymLinear                          Estimation/DTR/DTRInstance.lean                         145
minimax lower bound var causal                  Estimation/MinimaxATE/Causal/Minimax.lean               172
gmm efficiency                                  Stat/GMM/VarianceAlgebra.lean                           106
uStatisticOrder clt                             Stat/UStatistic/OrderM/CLT.lean                          52
twfe po decomposition                           Panel/.../CausalDecomposition.lean                       81
bjs linear unbiased iff imputation form         Panel/.../ImputationEventStudy/PanelBridge.lean         370
apparent pretrends from post treatment of       Panel/.../EventStudyContamination/Contamination.lean     63
cellGrid
htEst consistent eate                           Experimentation/UnknownInterference/Consistency.lean   133
directEffect clt                                Experimentation/.../Asymptotic/CLT.lean                118
localDependenceCLT of stein                     Experimentation/.../SteinInstance.lean                 176
wald coverage of stein                          Experimentation/.../SteinInstance.lean                 252




                                                       22
B        Logic-graph schema
Each result carries one dependency graph (Section 5.1), stored on disk as a FormalizationGraph.
A node has a kind, one of setup, definition, assumption, lemma, theorem, or gate. It also holds
its natural-language statement, its Lean 4 declaration, a review status (unreviewed, matched, or
drift), and a gate class field, either gated or cited, the must-prove and cited classes of Section 5.1.
An assumption node takes one further label, saying whether the assumption refines the claim,
does regularity bookkeeping, or stands in for a library gap. Edges are typed as statement-uses,
proof-uses, or setup-of, and store their two endpoints. Before a graph is written, a validator
checks it: duplicate nodes and edges are rejected, and any structural invariant that has been violated
is reported.


C        Implementation details of the pipeline
Here we describe the pipeline of Section 5 as it was actually implemented for the runs we report. A
theorem run is named by a question identifier together with a specialization, and the orchestrator
walks it through the ordered stages of Figure 4 and table 9. The numbered stages are a finer version
of the four stages of Section 5. Discovery is D-1.1 through D0.5. Formalization is F1, F1.5, and F2,
and proof construction is F3. The statement audit of Section 5.3 runs at three points of the proof
loop, namely F2.5, F3.5, and F4. F5 prepares the finished record, which the presentation state
machine of Section E then picks up as a separate process. The subsections after Table 9 describe
topic selection and the discovery reviews in more detail.

Table 9: Stages of a CausalSmith theorem run. The internal state stores the numerical identifiers
alone; the D and F prefixes are what the command-line interface and the logs use to tell discovery
apart from formalization.

 Stage        Purpose                    Action and acceptance condition            Principal durable
                                                                                    output
 D-1.1        Literature survey          Searches open problems and earlier pro-    Gap record
                                         posals for a question worth solving, be-
                                         fore anything is proposed.
 D-1.2        Proposal construction      Writes a typed proposal together with      Proposal      and
                                         its mathematical core, which names the     typed core
                                         objects, the atomic assumptions, the
                                         statements, and how they depend on
                                         one another.
 D-0.5        Proposal review            Reviews the proposal for novelty, for      Review decisions
                                         duplication, and for whether its mathe-    and     revision
                                         matical direction is viable. If the pro-   record
                                         posal is rejected, or if a finding looks
                                         repairable, it goes back to whichever
                                         discovery work can address it, and for-
                                         malization does not begin.




                                                  23
Table 9 continued
Stage         Purpose                   Action and acceptance condition             Principal durable
                                                                                    output
D0            Mathematical    deriva- Derives the proposed result and writes        Derivation note
              tion                    the research note. Where the deriva-          and updated core
                                      tion warrants it, the solver may nar-
                                      row a claim that turns out to be too
                                      strong, provided what it hands on for
                                      the later Lean 4 proof is still a real sci-
                                      entific claim.
D0-max        Maximality checkpoint Once the derivation goes through                Maximality de-
                                      cleanly, halts the run and puts the           cision (verbatim
                                      whole-paper question to an external re-       reviewer finding
                                      viewer: is a sharper bound, a better          logged)
                                      construction, a stronger reframing, or a
                                      tighter constant available? A concrete
                                      improvement comes back to D0 as a di-
                                      rective, while a reviewer who confirms
                                      the result is already maximal releases
                                      the run into D0.5.
D0.5          Soundness and novelty Keeps a fresh re-derivation of the math-        Mathematical,
              review                  ematics separate from the decisions           structural, and
                                      about structure, novelty, and tier. A         tier reviews
                                      further cold review is added when the
                                      target tier calls for one.
ckpt D/F      D0.5→F1 go/no-go        Halts the run once D0.5 has passed.           Commit decision
                                      The orchestrator weighs whether a re-         and lease re-grant
                                      sult that is now maximized and cleared
                                      for novelty is worth the expense of F1–
                                      F5. Resuming enters F1; stopping ei-
                                      ther records the discovery-only result
                                      or downgrades it.
F1            Formalization plan      Maps every core node, and the ambient         plan.json and
                                      setup it needs, onto a planned Lean 4         dependency graph
                                      object. Where a result can be reused,
                                      the plan names the declaration and
                                      the module it lives in; where a needed
                                      fact is unavailable, the plan records an
                                      openly disclosed obligation to be dis-
                                      charged.




                                                 24
Table 9 continued
Stage         Purpose                    Action and acceptance condition             Principal durable
                                                                                     output
F1.5          Plan and reuse review   Runs deterministic checks on cover-            Plan and reuse re-
                                      age, node kind, dependency closure,            views
                                      whether each declaration it cites ex-
                                      ists, and where modules are placed,
                                      then reviews how well the reuse fits and
                                      whether the abstraction level is right.
                                      A plan that comes back clean can stop
                                      at the first checkpoint so an operator
                                      may audit depth, reuse, and statement
                                      fidelity; in automatic mode it resumes
                                      on its own.
F2            Lean 4 scaffold         Writes or revises a Lean 4 scaffold. The       Tagged Lean     4
                                      first scaffold may still contain proof obli-   source tree
                                      gations. A later revision touches only
                                      the declarations that were flagged and
                                      the dependents it has to follow, so proof
                                      bodies that already work are left alone.
F2.5–F4       Proof and statement re- Checks first that the scaffold really          Proof    reviews,
              view loop               does realize the frozen specification          graph    verdicts,
                                      (F2.5). The proof-review loop then fills       crosswalk,   and
                                      the remaining obligations and rechecks         dependency
                                      the frontier it changed against the live       ledger
                                      Lean 4 compiler (F3). Next come the
                                      deterministic unused-hypothesis lint
                                      and the scan for forbidden proof steps
                                      (F3.5), and last a full dual-model con-
                                      vergence review of the frozen graph
                                      (F4). The numbers F2.5, F3, F3.5, and
                                      F4 survive as labels for these substeps,
                                      but the work belongs to the loop.
F5            Final approval prepara- Begins only once the scans for forbid-         Complete cross-
              tion                    den proof steps and the correspondence         walk and API
                                      checks come back clean. It then writes a       update
                                      final TEX-to-Lean 4 crosswalk covering
                                      lemmas as well as theorems, updates
                                      the API documentation, and stops at
                                      the second checkpoint. Recording, com-
                                      mitting, and promotion each need a
                                      human to say so.


C.1     Topic selection
A run invoked with no topic starts with the topic-selection module, ahead of the numbered D stages.
If a researcher supplies the topic instead, the module is skipped and the run enters D-1.1 directly.


                                                  25
                                                                                    sharpen: re-solve
                                                 reject / revise


                                          D-1.2              D-0.5              D0                                         D0.5
                           D-1.1                                                                       D0-max
       Discovery                        proposal +          proposal         derivation                                  derivation
                           recon                                                                      sharpen?
                                        typed core           review           + note                                      review


                                                                                                           frozen core
                                                                              ckpt D/F
                                    (D0 → F1)                               commit to F?


                                                                                          F2–F4
                          F1                   F1.5                                                                 F5
                                                                   ckpt 1            scaffold + proof                                 ckpt 2
 Formalization          plan +                plan +                                                             recording
                                                                    audit           + statement-review                                record
                   dependency graph        reuse review                                                            prep
                                                                                           loop


                                                                                     F4 fail → F2.5



                                   mismatch → F2                       lint block → F2.5



                         F2                         F2.5                    F3                      F3.5       pass           F4
                        Lean                     scaffold vs.       proof-review loop          unused-hyp lint            convergence
                       scaffold                  frozen spec         (fill ↔ recheck)           + cheat scan                review
  F2–F4 zoom


                                           false claim → D0 (via ckpt 1)



                    work      review     audit        checkpoint       - - → escalate / revise        - - → bounded proof loop



Figure 4: Stage flow of a CausalSmith theorem run, with an inset zoom on the F2–F4 proof and
statement-review loop. Top band: Discovery produces a proposal and a mathematical core, which
D0.5 freezes and hands to Formalization (middle band). An amber review can reject the work or
send it back one stage. The four red diamonds are halts that call for a judgment from outside the
run. D0-max asks an oracle whether the result can be sharpened before D0.5 freezes it; ckpt D/F
decides whether the result is worth the expense of F1–F5; ckpt 1 and ckpt 2 can ask a person to
decide, before F2 and before the run is recorded. Most runs used the automatic mode, where only
ckpt 2 is normally held for a person. Bottom: the substages of the proof loop. A green arc sends
work back for repair, while an amber arc escalates a false or under-specified claim to D0 instead of
quietly rewriting the frozen statement. Table 9 gives the purpose and acceptance condition of each
stage.


Figure 5 shows the flow.
    The module first states a stance in one line. An exploit stance extends a recorded result, or
works in a cluster where many attempts have been accepted. An explore stance goes to an area
with few acceptances. The stance shapes how candidates are drafted, and every candidate is then
ranked and reviewed on the same terms.
    The module then searches recent work in the area and picks one or two anchor papers that carry
a theorem. Subagents read each anchor in full, together with the papers that cite it. Each read
returns a short digest: the central theorems and their load-bearing proof steps, one or two questions
left open at the boundary of the proof, and one or two directions where the same technique could


                                                                       26
                                                               vague: sharpen and review again



 explore or exploit?            deep read                   propose              adversarial review                presolve
      a one-line stance     anchor papers in full,     about four candidates,     a different model looks     the top model builds
   that steers drafting   and the papers citing them          ranked               for a reason to stop      and attacks the result



                                                                                                                         launch
                                                                  refuted: take the runner-up


                                                                                                   a ready-to-run command
                                                                                                      an operator starts the run



Figure 5: Topic selection. Blue boxes do the work, the amber box is the adversarial review, and red
dashed arrows send a candidate back. Only a launch verdict from the presolve produces a command.


reach a new target or setting. From these digests the module drafts about four candidates. It ranks
them by evidence, mathematical depth, novelty, feasibility, and value to a named consumer, that
is, a published applied work or a software default whose practice would change if the result holds.
Each candidate is also checked against the runs that are already active or recorded.
     The top candidate goes to an adversarial review run on a different model. The reviewer looks
for a concrete reason to stop: a counterexample, a reduction to something trivial, or a paper that
already has the result. It also asks whether the conjecture is stated precisely, whether the result
would clear its target tier if true, and whether the consumer is real. A vague candidate comes back
to be sharpened and is reviewed again, up to three times. A refuted candidate is dropped and the
runner-up takes its place. If both fall, the module drafts one fresh slate, with the rejected topics
and their failure modes as constraints.
     A candidate that passes review goes to a presolve. In a single call the strongest available model
attempts the result, attacks its own attempt with counterexamples and a fresh literature search,
and writes the strongest supported theorem at full precision, with every gap listed. The call returns
launch, pivot, or drop. Learning at this point that a result is out of reach costs one model call, while
learning it during derivation costs a day of pipeline time. A launch verdict produces a ready-to-run
command whose topic string carries a short summary of the presolve and the path to its draft, and
an operator starts the run from it. Discovery treats the draft as evidence that still has to be verified.

C.2       Proposal review
D-0.5 reviews the proposal against a rubric written in advance. A mechanical check has already
confirmed that the proposal is well formed, so the reviewer spends its effort on meaning. Every
finding carries one code from one of three families, and the family decides where the finding goes.
    Structure findings check that the strongest result of the proposal is its headline target, instead
of a lemma on the way to a weaker theorem. They lead to a structural patch.
    Novelty findings are judged per statement on two axes, our own past runs and the published
literature, and a statement counts as new only when it is new on both. A finding that a result is
already known names the run or the paper. A finding that the proposal misstates a cited paper, or
that the result is already published, has to come with a receipt giving the exact source version and
a page, section, or equation. These findings send the proposal back for a redraft or a pivot.
    Soundness findings ask whether each statement is well defined, whether it reduces correctly in
the special cases it claims, and whether each assumption tagged as standard really is the standard
condition under that name. At this stage soundness concerns the question itself; the truth of each
statement is settled later, in D0. These findings lead to a redraft of the statement.

                                                             27
    The review closes with a tier rating, scored against the target tier fixed when the run was
launched. A repairable proposal returns to drafting a bounded number of times. A proposal that is
already known, or too thin for its tier, is recorded and dropped.

C.3    Solving and derivation review
D0 solves the frozen proposal core, which already fixes the statements to prove and the dependencies
between them. The solver groups the open statements into units (Figure 6), one per connected
component of their dependency graph, so two open statements share a unit when a chain of open
dependencies joins them. Each unit goes to its own agent, and the units run concurrently. An agent
owns only the targets of its unit. It may add helper lemmas with their own proofs, and it declares
every lemma and assumption its proofs rely on, so that the outputs of all units merge into one
graph. A classical published theorem enters as a cited leaf, carried with its source and its exact
statement. Each round regroups whatever is still open.
                                             one agent per connected component

                                                           unit 1

                                                                                       one merged graph
                    frozen core
                                                           unit 2                       statements, proofs,
               open statements to prove
                                                                                       and their dependencies


                                                           unit 3



                                          each round regroups whatever is still open



Figure 6: Solving at D0. The open statements are split by the connected components of their
dependency graph, the units are solved concurrently, and their outputs merge back into one graph.

    When a claim turns out to be too strong, the solver weakens it to something true and still
interesting, or corrects the definition behind it. When a claim turns out to be too weak, the solver
strengthens it. Either way the changed statement goes through the reviews again.
    D0.5 splits the review of the derivation across separate referees (Figure 7). Correctness, fit with
the rubric, and interest pull in different directions, and a single reviewer asked all three tends to
pass a correct but dull result on correctness alone. The math reviewer re-derives each load-bearing
step from the definitions, then compares its own derivation with the note term by term and reports
every difference. The rubric reviewer checks structure, novelty, and positioning against the written
rubric. When the target tier calls for it, a general referee reads the note cold. It sees the note
and plain tier definitions and nothing else. The solver itself works toward the rubric, so a note
can satisfy every item and still fall short, and the general referee is kept away from the rubric for
that reason. It grades what is proved over what is promised, and it calibrates against a spread of
accepted papers together with the scores their final referee gave them.
    A failure from the math reviewer sends the run back to D0. A general referee that places the
result below the target tier, but judges it salvageable, sends the run back to D0 with a directed
improvement, at most twice by default. A result judged below the target tier and beyond repair
halts the run for a decision.




                                                             28
                                   math reviewer: does the derivation hold?
                                   re-derives each load-bearing step from the definitions,
                                   then compares its derivation with the note term by
                                   term



           derived note
                                   rubric reviewer: does it clear the written bar?            go
         statements and proofs,
                                   structure, novelty, and positioning                       to F1
              as a graph



                                   general referee: would a referee care?
                                   a cold read with plain tier definitions and no rubric,
                                   calibrated on scored accepted papers; its tier caps the
                                   result



Figure 7: The derivation review at D0.5. Each referee answers one question. The general referee
joins when the target tier calls for it. A math failure, or a salvageable result below the target tier,
sends the run back to D0.

D     How the graph drives formalization, proof, and audit
The pipeline is built around the graph. The D stages create it in natural language. The typed core
of D-1.2 names the objects, assumptions, and statements together with the edges between them,
D0 extends it while deriving the result, and D0.5 freezes the argument, one node per claim. The F
stages attach Lean 4 to it. F1 gives every node an intended declaration and module, F2 emits the
scaffold, and each pass of the proof loop reads the emitted declarations and dependencies back into
the graph. Formalization also adds nodes for the intermediate lemmas the derivation never had
to name. The graph thus maps each planned object to what it should become, and each emitted
declaration to what it realizes.
    At F1.5, code checks what has a definite answer: whether each cited declaration exists, whether
every node is covered, and whether the dependencies close. The model judges the rest. It asks
whether a reused lemma sits at the right level of abstraction, whether the plan searched the library
before rebuilding, and whether a missing fact should be built or carried as an openly disclosed
assumption.
    The statement audit runs at F2.5, F3.5, and F4; a second audit, in Presentation, checks the
paper against the frozen graph (Section E). Each node is unreviewed, matched, or drift. An
accepted review is stamped with a fingerprint of the content it reviewed, so a change to a node or
its realization sends that node and its downstream nodes back to review.
    In the statement phase, the reviewer compares each frozen statement and definition with the
Lean 4 scaffold. Typical drift is a dropped hypothesis, a constant fixed where the claim was general,
or a definition narrowed until the claim becomes easy. A mechanical mismatch goes back to F2 for
a local revision. A false or under-specified claim, or a missing library fact, is escalated. The frozen
natural-language statement stays as written throughout, since it is the contract the audit protects.
    Proof filling starts once the statement phase is clean. One prover session runs at a time, because
the statements of one result sit in a single import chain, and each session starts from a summary
of the earlier ones. Each iteration reviews the frontier it changed, attempts the open obligations
against the live compiler, refreshes the graph, and checks for progress. The loop finishes with a
successful build, no sorry or admit, the frozen theorems and their dependency closures proved and
matched, a clean scan for axiom, opaque, and unsafe, and a passing unused-hypothesis lint. An
unused hypothesis suggests that the assumption is decoration or that the statement says less than
intended. A blocking finding returns the loop to the statement phase, and the rest are recorded for


                                                        29
the orchestrator.
    The final convergence review runs independently of the incremental one, on GPT and on Opus.
It revisits every object that originates in the paper, each theorem, definition, lemma, and symbol
with its assumptions, and judges helper lemmas through the statements that use them. Two different
models share fewer blind spots than one model asked twice. When they disagree, the orchestrator
reproduces the complaint. A correct complaint is fixed in the code, and a mistaken one becomes a
general fix to the reviewer prompt. The review also records how each library dependency was treated.
A gated dependency appears as an explicit conditional assumption or as a visible build obligation.
A cited dependency is checked against its source and blocks approval if its encoding is mismatched
or underspecified. F5 then writes the complete crosswalk, updates the API documentation with a
doc comment on every public declaration, and records the run as accepted, downgraded, or failed.


E       Presentation pipeline
The theorem pipeline and the paper pipeline are separate state machines. The paper pipeline takes
a recorded result and runs stages P0 through P5, with an optional P6 for slides (Figure 8). The
paper is generated from the checked code, and every later pass asks whether the prose has drifted
from it.
           P0                  P1                    P2                  P3                    P4                 P5              P6
       literature            render                 write               check                 emit              referee          slides
       verify each       each declaration,      prose, proofs,     code checks and       build, and link      read it as a   optional deck
    bibliography entry    then freeze it        related work        a prose rubric       claims to code      journal would   from the paper



                                             each finding returns to the earliest stage that can act on it



Figure 8: Stages of the presentation pipeline. Blue boxes produce the paper, amber boxes review it,
and the red dashed arrow is the revision route taken after the referee review.

    P0 assembles the literature. A model proposes the bibliography, and code looks up each entry
in Crossref, arXiv, and OpenAlex and drops any entry that fails to resolve. Every citation in the
paper has to come from this verified pool.
    P1 builds the formal layer of the paper. It walks the graph and renders each verified declaration
as a displayed theorem, definition, or assumption in ordinary mathematical notation, ordered so that
every object appears before anything that uses it. Each rendered statement is judged against its
Lean 4 declaration at the moment it is rendered. The English statement and its Lean 4 counterpart
have to be logically equivalent in assumptions and in conclusion alike. If either one is the stronger,
the pipeline halts for adjudication and keeps the declaration it was aiming at. The accepted layer is
then frozen. Later passes rewrite the prose around it freely, and every frozen statement is restored
byte for byte afterwards.
    P2 writes everything else: the introduction and abstract, the motivation, the proof of each result,
and the comparison with related work. The prose that describes proofs is audited against the graph.
When that audit fails, the pipeline runs one promotion round. It adds the statements the proofs
need to the formal layer, renders them at P1, and retries P2 once.
    P3 reads the assembled draft as one document. Code checks first that every citation key lies in
the verified pool, that every cross-reference resolves, and that the statements stand in the order
P1 fixed. A model then asks whether any sentence claims more than the theorems prove, whether
each cited source supports the sentence that cites it, and how the draft scores on a rubric covering



                                                                       30
claims, positioning, assumptions, and writing. Revisions touch the prose alone, and the draft gets
at most two rounds.
    P4 emits the rendered paper with its links to the code. Links are assembled from the graph
first. For each object it displays, the presentation system pulls the relevant declaration and its
statement-uses neighbors out of the verified graph, emits a source anchor, and checks that the
dependencies and assumptions on display have links of their own. A link therefore resolves to an
object that has passed the statement audit. P4 also ties each prose statement to its declaration
hypothesis by hypothesis, which drives the crosswalk of Section G.
    P5 reads the paper as a journal referee would, taking the theorems as given. It asks whether the
contribution is significant and delivered, whether each prose claim matches the verified statement in
strength and scope, whether the paper engages the actual results of its closest competitors, and
whether each condition is stated where it is claimed. Each finding is routed to the earliest stage
that can act on it. The orchestrator then revises the sources by hand and re-enters the pipeline at
that stage, after which the downstream reviews run again. P1 and P2 double as outline and draft
checkpoints: resuming from either one approves going on, and re-entering explicitly at P0, P1, or
P2 allows a targeted revision. Once the paper settles, P6 can build the slide deck, taking every
statement verbatim from the frozen layer.


F    Study mode
Partway through a proof, formalization can reach a step that needs a lemma nobody has written.
Three responses are reasonable. The run can record the gap and ship as an openly conditional result,
leaving the lemma for a later run. It can prove the lemma in place, next to the paper, which is the
quickest route to a finished result. Or it can build the lemma for the library, stated at its natural
generality, so that later runs find it ready. The choice turns on how wide the gap is and how many
results are likely to want the same fact. The orchestrator sends a fact of general use to study mode,
and builds a fact that is specific to one model and of manageable size in a helper file inside the run.
The theorem run carries on with the fact assumed. Once the lemma lands, the new declaration
returns to F1 as a candidate for reuse, and the statements that use it are reviewed again.
    A study starts from a short requirement written in plain English (Figure 9). It states the fact
that is needed, the generality it should have, and how the literature states it. The requirement
leaves the home of the code open. A scaffolder plans the lemmas and their order and writes a file
with every statement present and every proof left open. A prover then fills the proofs against the
live compiler. Provers run one at a time for the same reason as in F3, since the new files usually
form one import chain. After each round the scaffolder reads the build report and decides whether
to run another round or send the module to review, with at most ten build rounds.
    A reviewer then judges the module against seven checks, all of which have to hold. The module
is generic: it states the general fact, at the level where the fact holds. It is reusable: a clean,
well-named statement whose hypotheses are the ones a later proof would reach for. It is standard:
it matches how the literature states the result. It is non-vacuous: its hypotheses are satisfiable by
real inputs, and the statement keeps its full strength on the hard case. It fulfills the requirement,
with sharp constants intact; the reviewer judges the result delivered and accepts a proof route that
differs from the one the requirement sketched. It is free of sorry. And it is layered: its imports stay
within Mathlib, Causalean, and the files of the study itself. The last check protects the direction
of dependency, since a library lemma that imports a research file would carry that paper into the
library for good. The build confirms a passing verdict on its own, so a module that fails to compile
or still has an open proof goes back to the scaffolder. The review allows three rounds.


                                                  31
                                                                             rework, up to three rounds




      a written requirement                    plan and scaffold                        prover                       reviewer
      the fact, its generality,            which lemmas, in what order;          one at a time, against             seven checks,
      how the literature states it        statements written, proofs open           the live compiler           confirmed by the build




                                  pass     integration gate                          coordinator
           in Causalean                  build, index, embeddings,            reuses what exists, picks the
                                          documentation checks              narrowest home, writes docstrings



                                                   fail: roll back and retry, up to three times



Figure 9: A study-mode build. The top row writes and proves the module; the bottom row places it
in Causalean. Red dashed arrows are the bounded rework routes.

     A coordinator then places the module. It searches Causalean for declarations that already
prove the same statement and reuses them. It picks the narrowest existing file or subject area
that fits, and merges into an existing file where it can. Its edits are additive, consisting of new
files and inserted blocks, so every existing line of the library stays as it was. It also writes the
docstrings that the library explorer and the retrieval index read. Code then runs the integration
gate: a full build, re-indexing, the retrieval embeddings, and the documentation checks. A failure
rolls Causalean back to its prior state, and the coordinator retries with the failure log, up to three
times. A gate that hangs stops for the orchestrator, since rolling back in the middle of a build is
unsafe. Concurrent studies take turns at this step, because each one edits the shared library. Once
the gate passes, the lemma is part of Causalean. The library therefore grows out of what the
pipeline demands, with a boundary one can audit between a result specific to a single run and a
theorem the library will reuse.


G     The reading interface
A finished run leaves three things behind: a paper, a Lean 4 development, and the frozen graph
that ties them together. The companion site at https://jiyuan-tan.github.io/CausalSmith/
presents all three on one page. It adds four things on top of the text. It draws the dependency
structure of the paper’s own proofs. It puts each English statement next to the Lean 4 declaration
that was audited against it. It lets a reader record what they checked and what they thought of it.
And it presents the same result as a short 20mins talk. The screenshots in this section all come from
one accepted run, “Sharp Minimax Rates for Average Treatment Effects with Discrete Confounding
under Fixed Overlap”, and show the site as it stands.

G.1    The paper page
Figure 10 shows a paper page. The middle column is the paper itself. The left rail holds the table of
contents and the proof map. The right rail holds reader comments, each one beside the passage it is
about. The byline carries the pipeline’s own reviewer score, the reader rating, the commit version
number the page is pinned to, and links to the PDF, the Lean 4 development, and the slides.




                                                                     32
Figure 10: A paper page. Contents and proof map on the left, the paper in the middle, reader
comments on the right. The byline gives the reviewer score, the reader rating (four of five stars
from two readers), the pinned commit, and links to the PDF, the Lean 4 code, and the slides.




                                               33
G.2    Proof map
The proof map (Figure 11) is the reader-facing view of the frozen graph of Figure 2, restricted to
the results the paper displays. Each node is a theorem, proposition, or lemma of the paper. An
edge means that one proof invokes the other. The layout is layered: a result sits one rank above the
deepest result its proof invokes, and the theorems are pulled to the top row, so the paper’s headline
results read as the roof of the structure. The paper shown here has 22 statements and 29 such edges.
    Selecting a node highlights the results its proof invokes and the results that invoke it. It also fills
a card underneath with the statement, both lists as links, and the reader marks on that statement.
Every node is also a link, so a reader can go straight from the map to the statement it names.




Figure 11: The proof map, with one lemma selected. Left: the map itself, with the selected node’s
dependencies drawn in and the rest of the graph faded. Blue edges run to the results the selected
proof invokes; red edges run to the two theorems whose proofs invoke it. Right: the card the
selection fills, giving the statement, both dependency lists as links, and the reader marks. The
header counts how many of the 22 statements a reader has verified.




                                                    34
G.3    Natural-language statement and Lean 4 declaration
Every statement in the paper is clickable, and clicking it opens the Lean 4 side of it (Figure 12).
The panel gives the declaration name, its file and line, whether a scan of that source finds it free of
sorry, and the statement itself, split into its hypotheses and its conclusions. Where a symbol in
the paper is realized by a Lean 4 definition, that definition is shown too, with a link back to the
place in the paper that introduces it. Two kinds of gap carry an explicit label: a hypothesis the
Lean 4 statement holds that the paper leaves unstated, and a declaration in the development that
no paper statement cites.
   The pipeline claims that the English statement and the Lean 4 one express the same proposition.
The crosswalk puts the two side by side, so a reader can make the same comparison and disagree
with it. A separate page lists the complete development for the paper, module by module, including
the helper lemmas the paper never cites.




Figure 12: A statement in the paper (left, outlined) next to its Lean 4 declaration (right). The panel
gives the source location, the sorry scan, the hypotheses and the conclusion, and the definitions
the statement rests on, each linked back to the paper. The last rows list declarations the Lean 4
development uses and the paper leaves unstated.




                                                  35
G.4    Reader Interaction
A reader signed in with a GitHub account can leave three kinds of mark. All are public and all are
attributed.
    The first is a verification of a single statement, in the site’s own words: I read this statement
and its proof and found them correct, taking the results the proof invokes as given. The unit is
deliberately one statement. The results a proof invokes are somebody else’s to check, so the work is
small enough that a reader can finish it in one sitting. The proof map shows how far this has gone,
both as a count in its header and as a dot on each node. The paper in Figure 11 has 12 of its 22
statements verified.
    The second is a rating of one to five stars, on the paper as a whole or on a single statement, one
per account and withdrawable by clicking the same star again. The page shows the average and
the count. This sits beside the pipeline’s own reviewer score and answers a different question. The
score is one model’s judgment at the end of the run. The rating is what readers thought afterwards.
The paper of Figure 10 has four of five stars from two ratings.
    Selecting any passage of the paper offers to comment on it, and the comment is filed in the
margin beside the passage it quotes (Figure 13). A comment can be left plain, or tagged as a
verification or as a problem, and replies thread underneath it.




Figure 13: A reader comment. The quoted passage is shaded in the proof and the comment sits
beside it in the margin, with its author, its date, and a reply thread.


G.5    Slides
Each accepted result also ships as a short deck, built from the same graph as the paper (Figure 14).
The deck for this paper runs to 17 slides: the setting, the literature position, the idea, the main
result, a proof sketch, and what follows.




                                                 36
Figure 14: A slide carrying the main result. The one-sentence restatement at the top is labeled
informal, and the audited statement follows below it, with its definitions linked back to the paper.




                                                37
H     Reproducibility
The library and the pipeline are both pinned to Lean 4 toolchain leanprover/lean4:v4.29.0-rc3.
We read the declaration counts of Table 2 from the compiled environment index, which lake exe
library index prints. The axiom checks of Section 6.3 come from running #print axioms on each
headline theorem in a clean build, and we cross-check them with a comment-aware scan for sorry,
admit, and axiom over every recorded module and the library closure it imports.
     We release the source, the library, and the run record at https://github.com/Jiyuan-Tan/
CausalSmith, and https://jiyuan-tan.github.io/CausalSmith/ gives a browsable view of the
library and of the accepted results. The run catalog behind Tables 5 and 6 is the set of banked run
directories under CausalSmith/doc/research/ bank/, one directory per run, filed under accepted/,
downgraded/, or failed/. Each directory carries the run’s artifacts verbatim, that is, the state
file, the proposal, the review log, and the derivation note, and it is from these that we read the
dispositions and the downgrade reasons we quote. Legacy runs, meaning the ones that predate the
current pipeline, are left out of both tables.
     The cluster labels in Table 6 are CausalSmith’s own six clusters. Each run’s state file records
its cluster, and the run identifier carries it as a prefix (stat , exp , panel , eid , pid , scm ).
Discovery assigns the cluster at proposal time and picks the cluster-specific setup prompt from it,
so the grouping is fixed before anyone knows the run’s mathematics or how it will turn out. The
question-type labels of Table 7 are a different matter, since the pipeline does not produce them.
We assigned them ourselves, by the rule of Section 6.1, from each run’s proposal-time topic string.
That string is the topic field in the banked run’s README.md, and it too is fixed before the run’s
mathematics, so a reader who would draw the boundaries elsewhere can apply their own rule to the
same text. For the stated-versus-inferred provenance reported in Section 6.1 we read the anchor
paper of each accepted run; we did not repeat that reading for the downgraded and failed runs.

Base models. Every pipeline stage dispatches to one of two agent runners, OpenAI codex or
Anthropic claude. Each logical role maps to a model id that is committed in the pipeline source
and can be overridden per role by an environment variable (CAUSALEAN MODEL *). By the close of
the campaign the assignment stood as follows. GPT-5.6 Sol held the hard-mathematics tier, which
is the proposal, the derivation, the referee review, and the Lean 4 proof filler, and it also served as
the codex half of the dual convergence review. GPT-5.6 Terra held the mechanical tier: scaffold
translation, banking, proposal screening, and artifact emission. GPT-5.5 drafted and revised the
presentation. Claude did the planning, the Lean 4 code review, the second convergence review, and
the presentation rubric scoring.
    Both sides were updated during the campaign. On the OpenAI side the hard-mathematics tier
moved from GPT-5.5 to GPT-5.6 Sol on 2026-07-10, and for the day before that the proof-filler
role sat on the mechanical tier as well. On the Anthropic side the Claude roles ran as Opus 4.7
until 2026-05-28, as Opus 4.8 until 2026-07-24, and as Opus 5 thereafter. Our campaign ran from
2026-05-14 to 2026-08-26, so cut at those two dates the 144 runs of Table 5 divide into 81 under
Opus 4.7, 45 under Opus 4.8, and 18 under Opus 5, with none spanning a change; of the fourteen
accepted runs, nine sit entirely under Opus 4.8 and the other five entirely under Opus 5.




                                                  38
